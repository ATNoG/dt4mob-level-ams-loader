## Environment Variables

All settings can be overridden via environment variables with the prefix `LEVEL_AMS_LOADER_` and `__` as the nested delimiter.

| Environment Variable                | Config Path       | Example                           |
| ----------------------------------- | ----------------- | --------------------------------- |
| `LEVEL_AMS_LOADER_LOG_LEVEL`        | `log_level`       | `DEBUG`                           |
| `LEVEL_AMS_LOADER_LOADER__BASE_URL` | `loader.base_url` | `https://api.example.com`         |
| `LEVEL_AMS_LOADER_LOADER__JWT`      | `loader.jwt`      | `eyJhbGciOiJIUzI1NiIs...`         |
| `LEVEL_AMS_LOADER_HONO__HOST`       | `hono.host`       | `mqtt.example.com`                |
| `LEVEL_AMS_LOADER_HONO__PORT`       | `hono.port`       | `8883`                            |
| `LEVEL_AMS_LOADER_HONO__DEVICE`     | `hono.device`     | `my-device`                       |
| `LEVEL_AMS_LOADER_HONO__TENANT`     | `hono.tenant`     | `my-tenant`                       |
| `LEVEL_AMS_LOADER_HONO__PASSWORD`   | `hono.password`   | `secret`                          |
| `LEVEL_AMS_LOADER_DITTO__BASE_URL`  | `ditto.base_url`  | `https://ditto.example.com/api/2` |
| `LEVEL_AMS_LOADER_DITTO__NAMESPACE` | `ditto.namespace` | `org.example`                     |
| `LEVEL_AMS_LOADER_HISTORY__ENABLED` | `history.enabled` | `true`                            |
| `LEVEL_AMS_LOADER_OIDC__USERNAME`   | `oidc.username`   | `admin`                           |
