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

# Install project dependencies with the api optional dependency group using uv system python
RUN uv pip install --system .[api]

# Copy the application source code
COPY src/ ./src/

# Install the project package itself without dependencies
RUN uv pip install --system --no-deps .

# Expose the API port
EXPOSE 5000

# Start the FastAPI application using uvicorn
CMD ["uvicorn", "sql_data_guard.api.main:app", "--host", "0.0.0.0", "--port", "5000"]
