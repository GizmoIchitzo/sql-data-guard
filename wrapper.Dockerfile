# Use the official uv image for installing dependencies rapidly
FROM ghcr.io/astral-sh/uv:latest AS uv_setup

# Use a lightweight python alpine base image
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Copy the uv binary into the final container
COPY --from=uv_setup /usr/bin/uv /usr/bin/uv

# Set the working directory
WORKDIR /app

# Copy pyproject.toml and uv.lock to install dependencies
COPY pyproject.toml uv.lock* ./

# Install project dependencies with the mcp optional dependency group using uv system python
RUN uv pip install --system .[mcp]

# Copy the application source code
COPY src/ ./src/

# Install the project package itself without dependencies
RUN uv pip install --system --no-deps .

# Start the MCP Wrapper
CMD ["python", "-u", "-m", "sql_data_guard.mcp.wrapper"]
