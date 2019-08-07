#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z postgres 5432; do
  sleep 0.1
done

sleep 3

echo "PostgreSQL started, now running flask service"

python run.py run -h 0.0.0.0
