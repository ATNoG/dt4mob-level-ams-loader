## Troubleshooting

### Common Issues

| Issue                                        | Solution                                                                                          |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `Provide at least one of jwt or credentials` | Set either `jwt` or `[loader.credentials]` in config.toml                                         |
| `Login failed with status code: 401`         | Verify credentials and base_url in `[loader]`                                                     |
| `Connection refused` to MQTT                 | Check `[hono]` host/port and TLS certificate paths as well as the device, tenant and password     |
| `Failed getting details for id`              | Verify the geotechnical asset ID exists in Level AMS API                                          |
| Weird responses from the API                 | Decrease the number of instrument and parameter chunks as the API might be rate limiting requests |

### Logging

Increase verbosity by setting `log_level = "DEBUG"` or `log_level = "TRACE"` in `config.toml`.
