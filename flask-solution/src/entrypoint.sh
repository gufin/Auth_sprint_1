#!/bin/bash

# Wait for PostgreSQL
echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Apply database migrations
echo "Apply database migrations"
flask db upgrade

# some initialization code

if [ $# == 0 ]; then
  python3 app.py
else
  exec "$@"
fi