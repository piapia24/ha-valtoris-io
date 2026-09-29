"""Digital input channels."""
from datetime import timedelta

from homeassistant.components.binary_sensor import BinarySensorEntity
from .const import DOMAIN
from .entity import ValtorisEntity

SCAN_INTERVAL = timedelta(milliseconds=500)

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities(
        [DigitalInput(hass.data[DOMAIN][entry.entry_id], entry, i) for i in range(8)],
        update_before_add=True,
    )

class DigitalInput(ValtorisEntity, BinarySensorEntity):
    def __init__(self, hub, entry, index):
        super().__init__(entry, f"di_{index+1}")
        self.hub, self.index = hub, index
        self._attr_name = f"DI{index+1}"
        self._attr_icon = "mdi:electric-switch"
    @property
    def is_on(self): return bool(self._bits[self.index])
    async def async_update(self): self._bits = await self.hub.async_read_di()
    @property
    def extra_state_attributes(self): return {"electrical_state": "low/active when on (per manual)"}
