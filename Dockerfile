# Базовый образ
FROM python:3.13-slim-bookworm AS base
ENV POETRY_VERSION=2.1.1 \
    PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Стадия сборки
FROM base AS builder
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"
WORKDIR /app
# COPY pyproject.toml poetry.lock ./
COPY . .
RUN poetry config virtualenvs.create false \
    && poetry install --no-root \
    && chmod +x entrypoint.sh wait-for-it.sh

# Финальный образ
FROM base AS final
WORKDIR /app
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH"

