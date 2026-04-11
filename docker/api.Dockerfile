# Stage 1: Base
FROM python:3.14-slim AS base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"
WORKDIR /app

# Stage 2: Builder
FROM base AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl build-essential
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root --with dev

# Stage 3: Development/Testing
FROM base AS development
COPY --from=builder /app/.venv /app/.venv
COPY . .

ENTRYPOINT ["docker/entrypoint.sh"]

# Stage 4: Production
FROM base AS production
RUN useradd -m -u 1000 appuser
USER appuser

COPY --from=builder /app/.venv /app/.venv 
COPY . .

ENTRYPOINT ["docker/entrypoint.sh"]