#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z postgres 5432; do
  sleep 0.1
done

sleep 3

echo "PostgreSQL started, now running flask service"

gunicorn -b 0.0.0.0:5000 run:app
