## Scripts & Commands

### Development

```bash
# Run the loader
uv run main.py --geo-asset-id <ASSET_ID>

# Run with instrument filtering
uv run main.py --geo-asset-id <ASSET_ID> --instrument-ids <ID1,ID2>

# Run with history loading (requires config changes)
# 1. Set history.enabled = true in config.toml
# 2. Configure [oidc] section
uv run main.py --geo-asset-id <ASSET_ID>
```

### Code Quality

```bash
# Lint check
uv run ruff check

# Lint check with auto-fix
uv run ruff check --fix

# Type check (strict mode)
uv run mypy
```

### Docker

```bash
# Build image
docker build -t level-ams-loader .

# Run container
docker run level-ams-loader --geo-asset-id <ASSET_ID>

# Run with environment variable and external file overrides overrides
docker run \
  -e LEVEL_AMS_LOADER_LOG_LEVEL=DEBUG \ # You may provide other variables in a similar way
  -v ./config.toml:/app/config.toml:ro \ # You may provide other files in a similar way
  level-ams-loader \
  --geo-asset-id <ASSET_ID>
```
