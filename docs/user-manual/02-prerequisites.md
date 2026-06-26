## Prerequisites

Before using Level AMS Loader, ensure you have:

| Requirement            | Version/Details                                                       |
| ---------------------- | --------------------------------------------------------------------- |
| Python                 | 3.13 or higher                                                        |
| uv package manager     | [Install uv](https://docs.astral.sh/uv/getting-started/installation/) |
| Level AMS API access   | Valid credentials or JWT token                                        |
| Eclipse Hono           | Instance with an MQTT broker                                          |
| Eclipse Ditto          | Instance with API access                                              |
| Instrument coordinates | CSV file with ETRS89 TM06 coordinates                                 |

**Optional requirements:**

- History API with OIDC/Keycloak authentication (for historical data recovery)
- Grafana dashboards (for instrument visualization URLs)
