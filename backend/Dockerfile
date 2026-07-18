# Use a standard slim python image with uv pre-installed or install it
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

WORKDIR /build

# Copy configuration and package details
COPY pyproject.toml ./

# Install dependencies using uv sync to build virtualenv
RUN uv sync --no-dev --no-install-project

# Runtime stage
FROM python:3.13-alpine

WORKDIR /app

# Copy virtualenv from builder
COPY --from=builder /build/.venv /app/.venv

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Copy application source code
COPY app /app/app
# We also copy agents.md or AGENTS.md so it can be loaded
COPY agents.md /app/agents.md

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
