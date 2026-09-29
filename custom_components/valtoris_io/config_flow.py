"""UI config flow."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from .const import DOMAIN
from .hub import ValtorisHub

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input:
            try:
                unit_id = int(user_input["unit_id"])
                if not 0 <= unit_id <= 247:
                    raise ValueError
            except (TypeError, ValueError):
                errors["unit_id"] = "invalid_unit_id"
            else:
                user_input["unit_id"] = unit_id
                hub = ValtorisHub(user_input["host"], user_input["port"], unit_id)
                try:
                    await hub.async_check_connection()
                except (OSError, TimeoutError):
                    errors["base"] = "cannot_connect"
                else:
                    await self.async_set_unique_id(f"{user_input['host']}:{user_input['port']}:{unit_id}")
                    self._abort_if_unique_id_configured()
                    return self.async_create_entry(title=user_input["name"], data=user_input)
                finally: hub.close()
        schema = vol.Schema({
            vol.Required("name", default="Valtoris I/O"): str,
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_PORT, default=502): vol.All(int, vol.Range(min=1, max=65535)),
            vol.Required("unit_id", default="1"): str,
            vol.Required("ai_profile", default="standard"): vol.In({
                "standard": "AI1–4: 0–5 V; AI5–8: 4–20 mA",
                "0_5v": "All channels: 0–5 V",
                "0_10v": "All channels: 0–10 V",
                "4_20ma": "All channels: 4–20 mA",
            }),
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
