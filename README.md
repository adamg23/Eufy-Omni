<p align="center"><img src="custom_components/eufy_omni/brand/icon@2x.png" width="160" alt="Eufy Omni C28"></p>

# Eufy Omni C28 for Home Assistant

A from-scratch Home Assistant integration for Eufy Clean "Omni" robot vacuums (tested on the
Omni C28 `T211A` and X10 Pro Omni `T2351`). Talks to the Eufy Clean cloud the way the app
does: HTTPS login, then a mutual-TLS MQTT connection that pushes the robot's state as
protobuf-encoded data points. No polling in normal operation.

* `eufy_omni_cloud/` – standalone async client (aiohttp + paho-mqtt + protobuf).
* `custom_components/eufy_omni/` – the integration: vacuum, sensors, binary sensors,
  buttons, selects, volume, services `eufy_omni.start_scene` / `eufy_omni.start_rooms`.
* `proto/cloud/` – message schemas extracted from the Eufy app by Martijn Poppen
  (licence in `proto/LICENSE-eufy-clean-protos.md`). Compile with `tools/build_protos.py`.
* `docs/PROTOCOL.md` – what the protocol looks like and what has been verified live.
* `tools/probe_*.py` – probes that read `EUFY_USERNAME` / `EUFY_PASSWORD` from the
  environment and write only sanitised fixtures.

## Install with HACS

1. In HACS open the three-dot menu, choose **Custom repositories**, paste
   `https://github.com/adamg23/Eufy-Omni` and pick category **Integration**.
2. Install **Eufy Omni C28** from the HACS store and restart Home Assistant.
3. Go to Settings → Devices & services → Add integration → **Eufy Omni C28** and sign in with
   the email and password you use in the eufy app. Every robot on the account is added.

## Install (manual)

1. `powershell -File tools/deploy.ps1` vendors the client into the component.
2. Copy `custom_components/eufy_omni` into your Home Assistant `config/custom_components/`.
3. Restart Home Assistant, add the **Eufy Omni C28** integration, sign in with your Eufy account.

## Icon

The integration ships its own icon in `custom_components/eufy_omni/brand/` (`icon.png`,
`icon@2x.png`). Home Assistant 2026.3 and newer serve it locally; older versions show the
generic placeholder.

## Licence

MIT for everything in this repository except the protobuf schemas under `proto/cloud/`,
which keep their upstream licence (`proto/LICENSE-eufy-clean-protos.md`).

## Notes

* Eufy rate-limits logins (HTTP 429). The integration stores its session token and only logs
  in again when the token is rejected.
* The live map stream (`biz/` topic) is not rendered yet.
* Data points 166 and 169 carry the Matter pairing code and the robot's MAC/SSID/IP; they are
  never written to fixtures or diagnostics.
