#!/bin/bash
set -e

echo "Starting API server..."
exec uv run -- granian \
  --interface asgi \
  --host 0.0.0.0 \
  --port 8000 \
  --reload \
  --log-level info \
  --access-log \
  src.app:app
