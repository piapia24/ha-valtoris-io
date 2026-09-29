"""Analog measurements and 32-bit DI counters."""
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import UnitOfElectricCurrent, UnitOfElectricPotential
from .const import DOMAIN
from .const import ai_type_for_channel
from .entity import ValtorisEntity

SCAN_INTERVAL = timedelta(milliseconds=500)

async def async_setup_entry(hass, entry, async_add_entities):
    hub = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [AnalogInput(hub, entry, i) for i in range(8)]
        + [InputCounter(hub, entry, i) for i in range(8)],
        update_before_add=True,
    )

class AnalogInput(ValtorisEntity, SensorEntity):
    def __init__(self, hub, entry, index):
        super().__init__(entry, f"ai_{index+1}")
        self.hub, self.index = hub, index
        self._attr_name = f"AI{index+1}"
        self.ai_type = ai_type_for_channel(entry, index)
        self.current = self.ai_type == "4_20ma"
        self._attr_device_class = SensorDeviceClass.CURRENT if self.current else SensorDeviceClass.VOLTAGE
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.MILLIAMPERE if self.current else UnitOfElectricPotential.VOLT
        self._attr_suggested_display_precision = 4
    @property
    def native_value(self): return self._value
    async def async_update(self):
        raw = (await self.hub.async_read_ai())[self.index]
        maximum = 10 if self.ai_type == "0_10v" else 5
        self._raw = raw
        self._value = round(raw * (25/1024 if self.current else maximum/1024), 4)

class InputCounter(ValtorisEntity, SensorEntity):
    _attr_icon = "mdi:counter"
    _attr_native_unit_of_measurement = "pulses"
    def __init__(self, hub, entry, index):
        super().__init__(entry, f"di_{index+1}_count")
        self.hub, self.index = hub, index
        self._attr_name = f"DI{index+1} counter"
    @property
    def native_value(self): return self._value
    async def async_update(self):
        regs = await self.hub.async_read_counts()
        self._value = (regs[self.index*2] << 16) | regs[self.index*2+1]
