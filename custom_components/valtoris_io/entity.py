"""Shared entity details."""
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

class ValtorisEntity(Entity):
    _attr_has_entity_name = True
    def __init__(self, entry, key):
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)}, name=entry.data["name"],
            manufacturer="Valtoris", model="8CH-IO-ETH / 8CH-IO-LTE",
            configuration_url=f"http://{entry.data['host']}",
        )
