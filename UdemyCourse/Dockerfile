# Stage 1: Builder
FROM python:3.12 AS builder

WORKDIR /app

# Install uv
RUN pip install uv

# Verify uv installation
RUN pip show uv

# Copy dependency files and install dependencies
COPY uv.lock pyproject.toml /app/
RUN uv sync --frozen
COPY requirements.txt /app/

# Copy the application source code
COPY . .

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copy the virtual environment and necessary files from the builder stage
COPY --from=builder /app /app

# Set the default command
CMD ["python", "--version"]