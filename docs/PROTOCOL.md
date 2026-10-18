# Eufy Clean cloud protocol (Omni / "novel" devices)

Tags: **[C]** confirmed live against this account's devices · **[R]** taken from the
reference implementations (jeppesens/eufy-clean, martijnpoppen/eufy-clean) and not yet
exercised here · **[?]** inferred.

Devices on the test account: Omni C28 (`T211A`, firmware 4.9.1) and X10 Pro Omni
(`T2351`, firmware 3.4.85). Both are "AIoT" devices: status and commands travel over
MQTT; the older Tuya-cloud path is not used.

## 1. HTTPS

All calls use `User-Agent: EufyHome-Android-3.1.3-753` and an `openudid` header, a
random 32-hex string generated once per installation.

| Step | Request | Notes |
|---|---|---|
| Login **[C]** | `POST https://home-api.eufylife.com/v1/user/email/login` JSON `{email, password, client_id: "eufyhome-app", client_secret: "GQCpr9dSp3uQpsOMgJ4xQ"}`; headers `category: Home`, `clientType: 1` | Returns `access_token`, `refresh_token`, `expires_in`, `user_id`, `user_info`. The v2 endpoint (`/v1/user/v2/email/login`, client `eufy-app`) refused this account. |
| User centre **[C]** | `GET https://api.eufylife.com/v1/user/user_center_info`; headers `token: <access_token>`, `category: Home`, `clienttype: 2` | Returns `user_center_id` and `user_center_token`. `gtoken = md5(user_center_id)`. |
| Device list **[C]** | `POST https://aiot-clean-api-pr.eufylife.com/app/devicerelation/get_device_list` JSON `{"attribute": 3}`; headers `x-auth-token: <user_center_token>`, `gtoken`, `app-name: eufy_home`, `os-version: Android`, `model-type: PHONE` | `data.devices[].device` with `device_sn`, `device_model`, `device_name`, `main_sw_version`, `device_status`, `wifi_mac`, `local_ip`, `time_zone` and a full `dps` snapshot. |
| Legacy list **[C]** | `GET https://api.eufylife.com/v1/device/v2`; same headers as user centre | Only lists older-registered devices (the X10 here, not the C28). Carries `product.product_code` / `product.name`. |
| MQTT credentials **[C]** | `POST .../app/devicemanage/get_user_mqtt_info` (empty JSON body, AIoT headers) | `data`: `endpoint_addr` (`aiot-mqtt-us.anker.com`), `thing_name` (`<user_id>-eufy_home`), `app_name`, `user_id`, `certificate_pem`, `private_key` (RSA), `aws_root_ca1_pem`, `certificate_id`, `pkcs12`, `public_key`, `origin`. |

## 2. MQTT

* Broker: `endpoint_addr`:8883, TLS 1.2+, **mutual TLS** with the account certificate
  and key from the step above. Server chain validates against Amazon Root CA 1 (system
  store or the `aws_root_ca1_pem` supplied). **[C]**
* Client id: `android-eufy_home-eufy_android_<openudid>_<user_id>-<ms>`; username
  `thing_name`, no password. **[C]**
* Topics per device: **[C subscribed]**
  * `cmd/eufy_home/{model}/{sn}/req` – app → robot (data point writes)
  * `cmd/eufy_home/{model}/{sn}/res` – robot → app (data point reports)
  * `biz/eufy_home/{model}/{sn}/res` – robot → app map stream ("protocol 41")
* Envelope, JSON: `{"head": {client_id, cmd: 65537, cmd_status: 2, msg_seq, seed: "",
  sess_id, sign_code: 0, timestamp, version: "1.0.0.1"}, "payload": "<JSON string>"}`
  with payload `{"account_id", "device_sn", "protocol": 2, "t", "data": {dp: value}}`. **[R]**
* The robot publishes only on change; an idle docked robot is silent. **[C]**

## 3. Data points

Values are either plain scalars or base64 of `varint(len) + protobuf`. Schemas live in
`proto/cloud/` (upstream licence in `proto/LICENSE-eufy-clean-protos.md`); the generated
modules are `eufy_omni_cloud/pb/`.

| DP | Type | Message | C28 snapshot (2026-10-17) |
|---|---|---|---|
| 150 | null | – | |
| 151 | bool | – | true |
| 152 | pb | `ModeCtrlResponse` **[C]** | `{method: RESUME_TASK, seq: 101}` |
| 153 | pb | `WorkStatus` **[C]** | `state: CHARGING, charging.state: DONE` |
| 154 | pb | `CleanParamResponse` **[C]** | SWEEP_AND_MOP, mop level MIDDLE, fan TURBO |
| 155 | null | direction (remote control) **[R]** | |
| 156 | bool | multi-map switch **[R]** | true |
| 157 | pb | `UndisturbedResponse` **[C]** | DND on, end 06:00 |
| 158 | str | clean speed index **[R]** `0 quiet 1 standard 2 turbo 3 max 4 boost_iq` | "2" |
| 159 | bool | ? | true |
| 160 | bool | find robot **[R]** | false |
| 161 | int | volume % **[R]** | 80 |
| 162 | pb | `LanguageResponse` **[C]** | ids 1201 |
| 163 | int | battery % **[R]** | 100 |
| 164 | pb | `MapEditResponse` **[C]** | empty |
| 165 | pb | map data (`MultiMaps*`/rooms) **[?]** | 314 bytes |
| 166 | pb | device/Matter info **[?]** – contains the Matter pairing code; never store | |
| 167 | pb | `CleanStatistics` **[C]** | last 56 min / 56 m²; total 46 runs, 2219 m² |
| 168 | pb | `ConsumableResponse` **[C]** | brushes/filter 47 h, mop 30 h, dust bag 1 |
| 169 | pb | `DeviceInfo` **[C]** – product name, MAC, SSID, IP, user id; redact | "eufy Omni C28", 4.9.1, station 0.7.0 |
| 170 | pb | ? (5 bytes, `{4,…}`) | |
| 172 | pb | `MultiMapsManageResponse` **[R]** | null on C28 |
| 173 | pb | `StationResponse` **[C]** | wash by time 10 min, dry MEDIUM, detergent, dust collect by time 45, clean water 54 % |
| 176 | pb | `UnisettingResponse` **[C]** | AI see on, suggest zones on, dust-full remind 36000 |
| 177 | pb | `ErrorCode` **[C]** | no error |
| 178 | pb | ? (12 bytes) | |
| 179 | pb | telemetry, no schema **[R]** | 25 bytes |
| 180 | pb | `SceneResponse` **[C]** | 7 scenes: 3 built-in templates (not valid until configured) + 4 user routines on map 2; names are made generic in fixtures |

## 4. Commands **[R]** (to be confirmed one by one)

* Mode control: write dp 152 = `ModeCtrlRequest{method, seq, …}`; methods `START_AUTO_CLEAN 0`,
  `START_SELECT_ROOMS_CLEAN 1`, `START_GOHOME 6`, `STOP_TASK 12`, `PAUSE_TASK 13`,
  `RESUME_TASK 14`, `START_SCENE_CLEAN 24`.
* Clean parameters: dp 154 = `CleanParamRequest`.
* Fan speed: dp 158 = index string. Volume: dp 161 int. Find robot: dp 160 bool.
* Consumable reset, DND, child lock, off-peak charging via their request messages.

## 5. Verified on this account (2026-10-17)

| What | Result |
|---|---|
| Login v1 (`eufyhome-app`) | OK, returns user_center via `user_center_info` |
| Login v2 (`eufy-app`) | OK on a later attempt; the first attempts hit **HTTP 429** after three logins with fresh `openudid`s in a few minutes. Reuse the session; do not log in per request. |
| `get_device_list` | both robots with full `dps` snapshot (31 keys, 150–180) |
| `device/v2` | only the X10 Pro Omni (older registration), product code `T2351` |
| `get_user_mqtt_info` | endpoint `aiot-mqtt-us.anker.com`, RSA client cert + key, Amazon Root CA 1 |
| MQTT connect | CONNACK 0 with mutual TLS; `SUBSCRIBE` to `cmd/…/res` and `biz/…/res` granted QoS 0 |
| Idle traffic | none in 90 s with both robots docked |
| Write dp 160 = true (find robot) to the C28 | robot echoed `{"160": true}` within 1 s, then `{"160": false}` and a full `WorkStatus` (dp 153) report 43 s later when the chime finished |
| Snapshot decoding | every protobuf data point with a known schema parsed without error on both firmware generations (C28 4.9.1, X10 3.4.85) |
| Write dp 152 = `ModeCtrlRequest{START_GOHOME}` while docked | accepted; the robot re-published WorkStatus and station state within a second, no movement |
| Mop drying cycle | reported as `WorkStatus.state = CLEANING` with `station.washing_drying_system.state = 1`; mapped to activity `docked`, dock activity `drying` |
| Login from a second client (Home Assistant) within minutes of the probes | refused twice (as `invalid_auth`, not 429), succeeded ~5 min later. Treat repeated logins as the enemy: persist the session. |
| Home Assistant integration | config flow, 30 entities per robot, push updates and the Locate button all verified live on 2026-10-17 |
| Write dp 152 = `ModeCtrlRequest{START_SCENE_CLEAN, scene_id}` via `eufy_omni.start_scene` | full cycle observed by push: dock washing (2 min) → CLEANING → GO_HOME → docked collecting dust → washing → drying; CleanStatistics and consumables updated on return |

## 6. Compatibility notes

* Home Assistant 2026.10 pins `protobuf==7.36.0`; generated modules must come from protoc
  ≤ 36.0 or the runtime version guard refuses to import them. `tools/build_protos.py`
  takes `--protoc`.
* `grpcio-tools` has no Windows arm64 wheel; use the protoc release binary instead.
* The broker closes idle connections cleanly on `disconnect()`; paho's automatic reconnect
  (1–60 s backoff) is enabled.
