#!/bin/sh
set -e

echo "Waiting for PostgreSQL on $POSTGRES_HOST:$POSTGRES_PORT..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.5
done
echo "PostgreSQL is available!"

if [ "$INIT_DB" = "true" ]; then
  echo "Initializing database..."

  if [ ! -d "/app/migrations" ]; then
    mkdir -p /app/migrations
  fi
  
  if ! aerich -c src.adapters.database.db_config.TORTOISE_ORM list >/dev/null 2>&1; then
    echo "Initializing Aerich migrations..."
    aerich init -t src.adapters.database.db_config.TORTOISE_ORM
    aerich init-db
  fi
  
  echo "Applying existing migrations..."
  aerich upgrade
fi

if [ "$USE_GUNICORN" = "true" ]; then
  echo "Running with Gunicorn..."
  exec gunicorn src.main:app \
    --workers $GUNICORN_WORKERS \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
else
  echo "Running with Uvicorn..."
  exec uvicorn src.main:app --host 0.0.0.0 --port 8000
fi 