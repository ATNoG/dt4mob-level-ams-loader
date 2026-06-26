## Running the Service

### Local Execution

```bash
# Ensure config.toml is configured
uv run main.py --geo-asset-id <ASSET_ID>
```

### Docker Execution

```bash
# Build
docker build -t level-ams-loader .

# Run
docker run level-ams-loader --geo-asset-id <ASSET_ID>

# Run with correct files and environment variables
docker run \
  -v ./config.toml:/app/config.toml:ro \
  -e LEVEL_AMS_LOADER_LOG_LEVEL="DEBUG" \
  level-ams-loader --geo-asset-id <ASSET_ID>
```

Alternatively you may use the existing docker image like this:

```bash
docker run atnog-harbor.av.it.pt/dt4mob/level-ams-loader --geo-asset-id <ASSET_ID>
```

### Helm Deployment

There is a Helm Chart at the [dt4mob-platform repository](https://github.com/ATNoG/dt4mob-platform/tree/main/charts/dt4mob-level-ams-loader), that is recommended for deploying the script as a Kubernetes CronJob for periodicly synchronizing the digital twin platform with the most recent LevelAMS values.
