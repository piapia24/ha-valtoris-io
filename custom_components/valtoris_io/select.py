"""Per-channel analog input range selection for display conversion."""
from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity import EntityCategory
from .const import AI_TYPES, DOMAIN, ai_type_for_channel
from .entity import ValtorisEntity

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([AIProfileSelect(entry, i) for i in range(8)])

class AIProfileSelect(ValtorisEntity, SelectEntity):
    _attr_entity_category = EntityCategory.CONFIG
    _attr_icon = "mdi:tune-variant"
    _attr_options = list(AI_TYPES.values())

    def __init__(self, entry, index):
        super().__init__(entry, f"ai_{index+1}_profile")
        self.entry, self.index = entry, index
        self._attr_name = f"AI{index+1} measurement range"

    @property
    def current_option(self):
        return AI_TYPES[ai_type_for_channel(self.entry, self.index)]

    async def async_select_option(self, option):
        reverse = {label: key for key, label in AI_TYPES.items()}
        options = dict(self.entry.options)
        options[f"ai{self.index+1}_type"] = reverse[option]
        self.hass.config_entries.async_update_entry(self.entry, options=options)
