## Local Setup

**1. Prerequisites**

- Python 3.13+
- uv package manager

**2. Clone and install**

```bash
git clone https://github.com/ATNoG/dt4mob-level-ams-loader.git
cd dt4mob-level-ams-loader
uv sync
```

**3. Configure environment**

```bash
cp config.example.toml config.toml
```

Edit `config.toml` with your environment-specific settings. See [user manual](../user-manual/05-configuration.md) for all options.

**4. Verify installation**

```bash
# Lint check
uv run ruff check

# Type check
uv run mypy
```
