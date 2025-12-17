ARG UV_VERSION=0.9.15
ARG PYTHON_VERSION=3.12

FROM ghcr.io/astral-sh/uv:${UV_VERSION}-python${PYTHON_VERSION}-bookworm-slim AS builder

ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1 UV_PYTHON_CACHE_DIR=/root/.cache/uv/python

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv/python \
    uv sync --frozen --no-dev --no-install-project

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv/python \
    uv sync --frozen --no-dev

FROM python:${PYTHON_VERSION}-slim-bookworm AS runtime

RUN groupadd -r appgroup &&  \
    useradd -r -g appgroup appuser

ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder --chown=appuser:appgroup /app /app

USER appuser
EXPOSE 8000
CMD ["gunicorn", "main:app", "-c", "gunicorn.conf.py"]