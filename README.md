# Valtoris Remote I/O for Home Assistant

Custom Home Assistant integration for Valtoris 8CH-IO-ETH and 8CH-IO-LTE modules. Configure it from the Home Assistant UI; no `configuration.yaml` edits are needed.

Licensed under the [MIT License](LICENSE). This community integration is not affiliated with or endorsed by Valtoris.

> Community integration. It is not part of Home Assistant Core and is not officially supported by Home Assistant. It communicates locally with the module over Modbus TCP.

## Install with HACS

1. In HACS, open **Integrations** and select the three-dot menu.
2. Choose **Custom repositories**.
3. Paste this repository's GitHub URL and choose **Integration** as the category.
4. Add **Valtoris Remote I/O** from HACS and restart Home Assistant.
5. Go to **Settings → Devices & services → Add integration**, search for Valtoris, and enter the module's host, Modbus TCP port (usually `502`), Unit ID, and initial analog profile.

HACS custom repositories must be public on GitHub. See the [HACS publishing requirements](https://www.hacs.xyz/docs/publish/start/) and [integration requirements](https://www.hacs.xyz/docs/publish/integration/).

## Manual install

Copy `custom_components/valtoris_io` into the `custom_components` directory under your Home Assistant configuration, restart Home Assistant, and add the integration from **Settings → Devices & services**.

## Entities

- 8 binary sensors for digital inputs DI1–DI8.
- 8 switches for relay outputs DO1–DO8.
- 8 analog sensors AI1–AI8, displayed in V or mA.
- 8 configurable range selectors, one for each AI channel: 0–5 V, 0–10 V, or 4–20 mA.
- 8 32-bit digital-input counters.
- A switch for the module's built-in DI-to-corresponding-DO mode.

Analog sensors poll every 0.5 seconds. Range selectors change how Home Assistant converts the reading; they do not reconfigure the module's hardware. The selected type must match the channel configuration in Valtoris VirCOM. The initial profile follows the standard model: AI1–AI4 0–5 V and AI5–AI8 4–20 mA.

## Requirements and notes

- The module must be reachable from Home Assistant as a Modbus TCP server. Use a stable IP address or DHCP reservation.
- The Modbus Unit ID must match the I/O controller's station address.
- An LTE connection alone does not make the module reachable from the local network.
- Configure network parameters, DI polarity, active reporting, output power-on behavior, and the transparent RS485 gateway with the manufacturer's tools.
- Avoid controlling the same relays concurrently from multiple clients unless their behavior is coordinated.
- Verify the connected load and wiring against the module's ratings and the manufacturer's manual.

## Documentation

- [8CH-IO-ETH product page](https://valtoris.com/product/8-channel-ethernet-remote-io-module/)
- [8CH-IO-ETH / 8CH-IO-LTE user manual](https://valtoris.com/wp-content/uploads/2026/03/8CH-IO-ETH-8CH-IO-LTE-digital-input-output-module%E2%80%8B-User-Manual-EN.pdf)
- [Advanced I/O application note](https://valtoris.com/downloads/User%20Manual/IO%20port%20advanced%20function%20application.pdf)

## Polski

Integracja obsługuje moduły Valtoris 8CH-IO-ETH oraz 8CH-IO-LTE przez Modbus TCP. Konfiguracja odbywa się w interfejsie HA — bez zmian w `configuration.yaml`. Instrukcja instalacji przez HACS znajduje się powyżej.

Udostępnia 8 wejść DI, 8 przekaźników DO, 8 pomiarów AI, 8 liczników DI, selektory zakresu dla każdego kanału AI oraz przełącznik wbudowanej funkcji DI→DO. Selektory zmieniają sposób przeliczania wartości w Home Assistant, ale nie konfigurują sprzętu; zakres wejścia w HA musi odpowiadać ustawieniu w VirCOM. Czujniki analogowe odświeżają się co 0,5 s.

Ustawienia sieciowe, polaryzacja wejść, aktywne raportowanie, zachowanie przekaźników po starcie i przezroczysty gateway RS485 pozostają w konfiguracji producenta. Ustaw modułowi stały adres IP i sprawdź Unit ID kontrolera I/O.

## Issues and support

Please open a GitHub issue with your Home Assistant version, module model, connection settings (omit secrets), and relevant log entries. Do not post public IP addresses, passwords, or access tokens.
