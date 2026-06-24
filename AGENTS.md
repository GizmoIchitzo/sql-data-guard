# SQL Data Guard Agent Guidelines

This guide focuses on repository-specific gotchas, commands, and architecture that an AI agent might otherwise miss or guess wrong.

## Development Setup & Quirks

### Critical: pyproject.toml Version Gotcha
- `pyproject.toml` contains `version = "UPDATED-BY-WORKFLOW"`. This is non-PEP-440 compliant.
- **Consequence**: Modern strict workspace commands like `uv sync` will fail with TOML parsing errors.
- **Remedy**:
  - **Option A (Standard/Recommended)**: Temporarily change the version string in `pyproject.toml` to a valid PEP-440 compliant version like `"0.1.0"` (or use the already patched version in dev), then use standard `uv add` and `uv sync` workspace commands:
    ```bash
    # Synchronize all workspace dependency groups
    UV_NATIVE_TLS=true uv sync --all-groups

    # Add a new dependency to a specific group
    UV_NATIVE_TLS=true uv add --group dev <package>
    ```

---

## Verifying Changes (Testing)

### Run Unit Tests
Unit tests are located under `tests/unit/`:
```bash
PYTHONPATH=src pytest --color=yes tests/unit/
```

### Run a Focused Test
```bash
PYTHONPATH=src pytest tests/unit/test_verification_utils.py -k "test_split_to_expressions_matching"
```

### LLM Integration Tests
- Location: `tests/integration/test_sql_guard_llm.py`
- **Quirk**: Requires AWS Bedrock permissions configured via AWS environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`, and optionally `AWS_SESSION_TOKEN`). Do not run them locally if AWS credentials are missing.
- Command:
  ```bash
  PYTHONPATH=src pytest --color=yes tests/integration/test_sql_guard_llm.py
  ```

---

## Compiling Documentation

To build the interactive HTML documentation locally:
```bash
PYTHONPATH=src sphinx-build -b html docs/ docs/_build/html
```
The output will be generated under `docs/_build/html/index.html`.

---

## Architecture & Sub-project Boundaries

### Core Library
- Located in `src/sql_data_guard/core/`.
- No FastAPI, Uvicorn, or Docker imports are permitted here to ensure library users have zero dependency overhead beyond `sqlglot`.
- Uses the `sqlglot` library to parse, analyze, and rewrite SQL queries.

### REST API Service
- Located in `src/sql_data_guard/api/main.py`.
- Built using **FastAPI** and **Pydantic V2**.
- Configured via `Dockerfile` and run using Uvicorn.
- Runs locally via:
  ```bash
  uvicorn sql_data_guard.api.main:app --host 0.0.0.0 --port 5000 --reload
  ```

### MCP Wrapper Service
- Located in `src/sql_data_guard/mcp/wrapper.py`.
- Managed/packaged via `wrapper.Dockerfile`.
- Runs locally via:
  ```bash
  python -m sql_data_guard.mcp.wrapper
  ```

### Dify Plugin
- Located in `plugins/dify/`.
- Packaged locally using Dify CLI:
  ```bash
  dify plugin package ../dify --output_path sql_data_guard.difypkg
  ```
