#!/bin/sh

echo "Waiting for MongoDB..."

while ! nc -z mongo 27017; do
  sleep 0.1
done

echo "MongoDB started!"

echo "Waiting for Redis..."

while ! nc -z redis 6379; do
  sleep 0.1
done

echo "Redis started!"

exec "$@"