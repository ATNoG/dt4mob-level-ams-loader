## Project Structure

### Key Files

| File/Directory             | Purpose                                                                                 |
| -------------------------- | --------------------------------------------------------------------------------------- |
| `main.py`                  | Entry point. Parses CLI args, instantiates Hono and LevelAMSLoader, runs async loader   |
| `app/level_ams_loader.py`  | Core business logic. Orchestrates API fetching, Ditto message creation, MQTT publishing |
| `app/hono_connection.py`   | Async context manager for MQTT connection lifecycle                                     |
| `app/settings/__init__.py` | Root Settings class. Loads config.toml, validates credentials, configures logging       |
| `app/models/common.py`     | Shared types including Coordinates with ETRS89 TM06 to WGS84 conversion                 |
| `app/models/`              | Stores all relevant data models                                                         |
| `app/dependencies/`        | Connection logic for any dependencies to external services                              |
| `app/docs/`                | Documentation files                                                                     |
