## Code Conventions

### Type Hints

The project uses strict mypy checking. All functions and methods should have complete type annotations.

### Pydantic Models

- Use `pydantic` v2 models for data validation
- Use `pydantic-settings` for configuration loading
- Use `pydantic.v1` only for `pydantic-argparse` compatibility

### Async/Await

- Use `asyncio.TaskGroup` for concurrent operations
- Use `httpx.AsyncClient` for HTTP requests
- Use context managers for resource cleanup

### Logging

- Use `loguru` for structured logging
- Log levels: `trace` for raw data, `debug` for flow, `info` for progress, `success` for completion, `error` for failures

### Error Handling

- Raise `RuntimeError` for unrecoverable errors
- Use `logger.error()` before raising for visibility
- Let exceptions propagate through `TaskGroup` for proper cleanup
