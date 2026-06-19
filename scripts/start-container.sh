#!/bin/sh

set -eu

echo "Starting ContextOps container initialization..."

attempt=1
max_attempts=10

until python -m alembic upgrade head; do
    if [ "$attempt" -ge "$max_attempts" ]; then
        echo "Database migration failed after ${max_attempts} attempts."
        exit 1
    fi

    echo "Database is not ready. Retrying migration in 3 seconds..."
    attempt=$((attempt + 1))
    sleep 3
done

echo "Database migrations completed."
echo "Starting ContextOps API on port ${PORT:-8000}..."

exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port "${PORT:-8000}" \
    --proxy-headers \
    --forwarded-allow-ips="*"