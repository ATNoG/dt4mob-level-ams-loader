## Configuration

Configuration is loaded from `config.toml` in the project root. Environment variables can override any setting using the prefix `LEVEL_AMS_LOADER_` with `__` as the nested delimiter.

**Environment variable format:**

```
LEVEL_AMS_LOADER_<SECTION>__<FIELD>=value
```

**Example:**

```bash
export LEVEL_AMS_LOADER_LOG_LEVEL=DEBUG
export LEVEL_AMS_LOADER_LOADER__JWT=my-jwt-token
export LEVEL_AMS_LOADER_HONO__HOST=mqtt.example.com
```

### General Settings

| Setting     | Type   | Default  | Description                                                                                             |
| ----------- | ------ | -------- | ------------------------------------------------------------------------------------------------------- |
| `log_level` | String | `"INFO"` | Application log verbosity. Options: `TRACE`, `DEBUG`, `INFO`, `SUCCESS`, `WARNING`, `ERROR`, `CRITICAL` |

### Loader Settings `[loader]`

| Setting                  | Type    | Default                   | Description                                                         |
| ------------------------ | ------- | ------------------------- | ------------------------------------------------------------------- |
| `base_url`               | URL     | `"http://localhost"`      | Base URL of the Level AMS API                                       |
| `jwt`                    | String  | `null`                    | JWT token for API authentication. Provide this **OR** `credentials` |
| `http_timeout`           | Float   | `30.0`                    | HTTP request timeout in seconds. Set to `null` to disable           |
| `start_page_idx`         | Integer | `1`                       | Starting page index for pagination (must be >= 1)                   |
| `instrument_coords_file` | Path    | `"instrument_coords.csv"` | Path to CSV file with instrument coordinates                        |
| `parameters_chunk_size`  | Integer | `10`                      | Number of parameters processed in parallel per instrument           |
| `instruments_chunk_size` | Integer | `10`                      | Number of instruments processed in parallel                         |

#### Loader Credentials `[loader.credentials]`

Used when `jwt` is not provided. The loader will perform a login request to obtain a JWT token.

| Setting    | Type   | Default | Description  |
| ---------- | ------ | ------- | ------------ |
| `username` | String | -       | API username |
| `password` | String | -       | API password |

### Eclipse Hono Settings `[hono]`

MQTT connection to Eclipse Hono for publishing Ditto protocol messages.

| Setting    | Type    | Default       | Description                                                                       |
| ---------- | ------- | ------------- | --------------------------------------------------------------------------------- |
| `host`     | String  | `"127.0.0.1"` | MQTT broker hostname                                                              |
| `port`     | Integer | `null`        | MQTT broker port. Set to `null` for default                                       |
| `device`   | String  | `null`        | MQTT device identifier. Combined with `tenant` to form username (`device@tenant`) |
| `tenant`   | String  | `null`        | MQTT tenant identifier. Combined with `device` to form username (`device@tenant`) |
| `password` | String  | `null`        | Optional MQTT authentication password                                             |
| `cafile`   | Path    | `null`        | Path to CA certificate file for TLS                                               |
| `certfile` | Path    | `null`        | Path to client certificate file for TLS                                           |
| `keyfile`  | Path    | `null`        | Path to client private key file for TLS                                           |
| `topic`    | String  | `"telemetry"` | MQTT topic to publish messages to                                                 |

### Eclipse Ditto Settings `[ditto]`

Configuration for the Ditto API and thing creation.

| Setting          | Type   | Default                    | Description                                                          |
| ---------------- | ------ | -------------------------- | -------------------------------------------------------------------- |
| `base_url`       | URL    | `"http://localhost/api/2"` | Ditto REST API base URL                                              |
| `namespace`      | String | `"namespace"`              | Namespace prefix for thing IDs (e.g., `"namespace:subject:assetId"`) |
| `default_policy` | String | `"dt4mob:default"`         | Policy ID assigned to all created things                             |
| `subject`        | String | `"test"`                   | Subject prefix for thing names                                       |
| `username`       | String | `null`                     | Optional Ditto API authentication username                           |
| `password`       | String | `null`                     | Optional Ditto API authentication password                           |
| `cafile`         | Path   | `null`                     | Optional CA certificate file for Ditto API TLS                       |
| `cadata`         | String | `null`                     | Optional PEM-encoded CA certificate data                             |

### Dashboard Settings `[dashboard]`

Configuration for instrument dashboard URLs. These URLs are stored as attributes in each instrument in Ditto things.

| Setting                    | Type   | Default               | Description                                           |
| -------------------------- | ------ | --------------------- | ----------------------------------------------------- |
| `inclinometer_base_url`    | URL    | `"http://127.0.0.1"`  | Base URL for inclinometer dashboard                   |
| `inclinometer_query_param` | String | `"var-instrument_id"` | Query parameter for instrument ID in inclinometer URL |
| `load_cell_base_url`       | URL    | `"http://127.0.0.1"`  | Base URL for load cell dashboard                      |
| `load_cell_query_param`    | String | `"var-instrument_id"` | Query parameter for instrument ID in load cell URL    |

### History Loading Settings `[history]`

Controls historical data loading behavior. Reserved for manual data recovery operations.

| Setting    | Type    | Default                       | Description                 |
| ---------- | ------- | ----------------------------- | --------------------------- |
| `enabled`  | Boolean | `false`                       | Enable history data loading |
| `base_url` | URL     | `"http://127.0.0.1/historic"` | History API base URL        |

### OIDC Settings `[oidc]`

Required when `history.enabled = true`. Configures authentication with the history API via OIDC/Keycloak.

| Setting     | Type   | Default              | Description            |
| ----------- | ------ | -------------------- | ---------------------- |
| `username`  | String | `"admin"`            | OIDC/Keycloak username |
| `password`  | String | `"admin"`            | OIDC/Keycloak password |
| `client_id` | String | `"client"`           | OAuth2 client ID       |
| `realm`     | String | `"realm"`            | Keycloak realm name    |
| `base_url`  | String | `"http://localhost"` | OIDC provider base URL |

### Instrument Thresholds `[instrument_thresholds]`

Optional per-instrument alert/alarm thresholds. Keyed by instrument matricula.

**Priority:** Instrument-specific thresholds override instrument-type thresholds.

```toml
[instrument_thresholds."A25.1"]
parameter_types = ["INCL01"]
alert = { threshold_type = "GT", value = 5.0 }
alarm = { threshold_type = "GT", value = 10.0 }
```

### Instrument Type Thresholds `[instrument_type_thresholds]`

Optional per-instrument-type alert/alarm thresholds. Applied when no instrument-specific threshold exists.

**Supported instrument types:**

- `InstrumentoTipoInstrumento_Inclinometro`
- `InstrumentoTipoInstrumento_CelulaCarga`

```toml
[instrument_type_thresholds."InstrumentoTipoInstrumento_Inclinometro"]
parameter_types = ["INCL01", "INCL02"]
alert = { threshold_type = "GT", value = 5.0 }
alarm = { threshold_type = "GT", value = 10.0 }
```

### Threshold Configuration Reference

| Field             | Type          | Description                                                                                               |
| ----------------- | ------------- | --------------------------------------------------------------------------------------------------------- |
| `parameter_types` | Set\[String\] | Matches against parameter keys without trailling numbers, as those are considered the same parameter type |
| `threshold_type`  | String        | Comparison type. See below                                                                                |
| `value`           | Float         | Threshold value                                                                                           |

**Threshold types:**

| Type    | Behavior       | Example                                |
| ------- | -------------- | -------------------------------------- |
| `GT`    | Greater Than   | Triggers when `value > threshold`      |
| `LT`    | Less Than      | Triggers when `value < threshold`      |
| `DELTA` | Absolute Delta | Triggers when `abs(value) > threshold` |

**Measurement states:**

| State   | Description                   |
| ------- | ----------------------------- |
| `OK`    | Value within normal range     |
| `ALERT` | Value exceeds alert threshold |
| `ALARM` | Value exceeds alarm threshold |
