"""Relay controls and built-in DI-to-DO linking mode."""
from datetime import timedelta
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN
from .entity import ValtorisEntity

SCAN_INTERVAL = timedelta(seconds=1)

async def async_setup_entry(hass, entry, async_add_entities):
    hub = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [Relay(hub, entry, i) for i in range(8)] + [InputOutputLink(hub, entry)],
        update_before_add=True,
    )

class Relay(ValtorisEntity, SwitchEntity):
    def __init__(self, hub, entry, index):
        super().__init__(entry, f"do_{index+1}")
        self.hub, self.index = hub, index
        self._attr_name = f"DO{index+1} relay"
    @property
    def is_on(self): return self._state
    async def async_update(self): self._state = bool((await self.hub.async_read_do())[self.index])
    async def async_turn_on(self, **kwargs): await self.hub.async_write_do(self.index, True); self._state = True
    async def async_turn_off(self, **kwargs): await self.hub.async_write_do(self.index, False); self._state = False

class InputOutputLink(ValtorisEntity, SwitchEntity):
    _attr_icon = "mdi:source-branch"
    def __init__(self, hub, entry):
        super().__init__(entry, "di_controls_do")
        self.hub = hub
        self._attr_name = "DI controls corresponding DO"
    @property
    def is_on(self): return self._state
    async def async_update(self): self._state = bool((await self.hub.async_read_link())[0])
    async def async_turn_on(self, **kwargs): await self.hub.async_write_link(True); self._state = True
    async def async_turn_off(self, **kwargs): await self.hub.async_write_link(False); self._state = False
