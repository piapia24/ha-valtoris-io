"""Valtoris 8-channel I/O integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from .const import DOMAIN, PLATFORMS
from .hub import ValtorisHub

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hub = ValtorisHub(entry.data["host"], entry.data["port"], entry.data["unit_id"])
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = hub
    await hub.async_check_connection()
    registry = er.async_get(hass)
    for entity in er.async_entries_for_config_entry(registry, entry.entry_id):
        if "_ai_" in entity.unique_id and entity.unique_id.endswith("_precise"):
            registry.async_remove(entity.entity_id)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id).close()
    return ok

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)
