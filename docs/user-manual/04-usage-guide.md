## Usage Guide

### Standard Run (Load a single geotechnical asset)

The loader requires a geotechnical asset ID to synchronize. This is the primary operation mode.

```bash
uv run main.py --geo-asset-id <ASSET_ID>
```

**Example:**

```bash
uv run main.py --geo-asset-id "geo-asset-123"
```

**What happens:**

1. Fetches asset details and instrument list from Level AMS API
2. Creates the geotechnical asset as a Ditto thing
3. Creates each instrument as a Ditto thing with coordinates and dashboard URLs
4. Fetches latest measurement values for each parameter and calculates monitoring state
5. Publishes all data to Eclipse Ditto via Eclipse Hono's MQTT adapter

### Filter Specific Instruments

To load only specific instruments from an asset:

```bash
uv run main.py --geo-asset-id <ASSET_ID> --instrument-ids <ID1> [<ID2> ...]
```

**Example:**

```bash
uv run main.py --geo-asset-id "geo-asset-123" --instrument-ids "A25.1" "A25.2" "I1C"
```

> **Note:** `--instrument-ids` requires `--geo-asset-id` to be set.

### History Loading Mode

History loading is reserved for manual data recovery operations (e.g., after data loss). This mode fetches all historical parameter values the API has to offer and sends them to the history API.

**To enable history loading:**

1. Set `history.enabled = true` in `config.toml`
2. Configure the `[oidc]` section with valid credentials
3. Run the loader:

```bash
uv run main.py --geo-asset-id <ASSET_ID>
```

> **Important:** History loading should only be run when explicitly needed. Under normal operations, history loading remains disabled.

### Docker Execution

```bash
# Build the image
docker build -t level-ams-loader .

# Run the container
docker run level-ams-loader --geo-asset-id <ASSET_ID>
```
