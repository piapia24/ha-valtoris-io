"""Constants."""
from homeassistant.const import Platform
DOMAIN = "valtoris_io"
PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR, Platform.SWITCH, Platform.SELECT]

AI_TYPES = {"0_5v": "0–5 V", "0_10v": "0–10 V", "4_20ma": "4–20 mA"}

def ai_type_for_channel(entry, index: int) -> str:
    """Return the selected measurement type for one AI channel."""
    selected = entry.options.get(f"ai{index + 1}_type")
    if selected:
        return selected
    profile = entry.data.get("ai_profile", "standard")
    if profile == "standard":
        return "0_5v" if index < 4 else "4_20ma"
    return profile
