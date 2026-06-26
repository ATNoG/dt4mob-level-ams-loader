## Deployment

### Docker Build

The Dockerfile builds a single-stage image:

1. **Base image**: `python:3.13-slim`
2. **Package manager**: Copies `uv` from official image
3. **Dependencies**: Copies `pyproject.toml`, `uv.lock`, `.python-version` first for caching, then runs `uv sync --frozen --no-cache`
4. **Application**: Copies source code
5. **Entrypoint**: `uv run main.py`

### Helm Deployment

TODO
