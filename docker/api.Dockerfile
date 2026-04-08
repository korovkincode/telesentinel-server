# Stage 1: Build dependencies
FROM python:3.14-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=2.1.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends curl build-essential

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --only main

# Stage 2: Runtime
FROM python:3.14-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

RUN useradd -m -u 1000 appuser
USER appuser

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY . .

USER root
RUN chmod +x docker/entrypoint.sh
USER appuser

ENTRYPOINT ["docker/entrypoint.sh"]
