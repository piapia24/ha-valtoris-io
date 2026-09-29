"""Minimal async Modbus TCP client using Valtoris documented register map."""
import asyncio
import struct
import time

class ValtorisHub:
    def __init__(self, host: str, port: int, unit_id: int) -> None:
        self.host, self.port, self.unit_id = host, port, unit_id
        self._lock = asyncio.Lock()
        self._cache_lock = asyncio.Lock()
        self._cache = {}
        self._transaction = 0

    async def request(self, function: int, address: int, count: int = 1, value: int = 0):
        pdu = struct.pack(">BHH", function, address, count) if function in (1, 3, 4) else struct.pack(">BHH", function, address, (0xFF00 if value else 0) if function == 5 else value)
        async with self._lock:
            self._transaction = (self._transaction + 1) & 0xffff
            writer = None
            try:
                reader, writer = await asyncio.wait_for(asyncio.open_connection(self.host, self.port), 4)
                writer.write(struct.pack(">HHHB", self._transaction, 0, len(pdu)+1, self.unit_id) + pdu)
                await writer.drain()
                header = await asyncio.wait_for(reader.readexactly(7), 4)
                tid, proto, length, unit = struct.unpack(">HHHB", header)
                if tid != self._transaction or proto != 0 or unit != self.unit_id or length < 2:
                    raise OSError("Invalid Modbus TCP response")
                response = await asyncio.wait_for(reader.readexactly(length-1), 4)
                if response[0] & 0x80:
                    raise OSError(f"Modbus exception {response[1]}")
                if response[0] != function:
                    raise OSError("Unexpected Modbus function")
                if function == 1:
                    return [(response[2+i//8] >> (i%8)) & 1 for i in range(count)]
                if function in (3, 4):
                    payload = response[2:2+response[1]]
                    if len(payload) != count*2: raise OSError("Incomplete register response")
                    return list(struct.unpack(">" + "H"*count, payload))
                return []
            finally:
                if writer:
                    writer.close()
                    try: await writer.wait_closed()
                    except OSError: pass

    async def async_check_connection(self):
        await self.request(1, 0, 8)
        await self.request(4, 0, 8)
    async def _cached(self, key, function, address, count):
        async with self._cache_lock:
            cached = self._cache.get(key)
            if cached and time.monotonic() - cached[0] < 0.4:
                return cached[1]
            result = await self.request(function, address, count)
            self._cache[key] = (time.monotonic(), result)
            return result
    async def async_read_di(self): return await self._cached("di", 1, 0, 8)
    async def async_read_do(self): return await self._cached("do", 1, 16, 8)
    async def async_read_ai(self): return await self._cached("ai", 4, 0, 8)
    async def async_read_counts(self): return await self._cached("counts", 3, 256, 16)
    async def async_read_link(self): return await self._cached("link", 3, 72, 1)
    async def async_write_do(self, channel, state):
        await self.request(5, 16+channel, value=int(state))
        # The relay state is read from a cached block of eight coils. Keep that
        # block in sync with a successful write so a just-toggled entity cannot
        # be reverted by a poll that sees the old cached value.
        async with self._cache_lock:
            cached = self._cache.get("do")
            if cached and time.monotonic() - cached[0] < 0.4:
                states = list(cached[1])
                states[channel] = int(state)
                self._cache["do"] = (time.monotonic(), states)
            else:
                self._cache.pop("do", None)

    async def async_write_link(self, state):
        await self.request(6, 72, value=256 if state else 0)
        async with self._cache_lock:
            self._cache["link"] = (time.monotonic(), [256 if state else 0])
    def close(self): pass
