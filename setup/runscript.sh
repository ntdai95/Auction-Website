#!/bin/sh
# Build the images and start the whole stack.
#
# Every service retries the database or broker it depends on, so they can all
# start together. This used to build each image by hand with Windows-style
# paths, bring the databases up on their own, and then sleep for two minutes
# hoping MySQL had finished initialising.
set -e

cd "$(dirname "$0")"

if [ ! -f .env ]; then
    echo "setup/.env is missing. Copy .env.example to .env and fill it in."
    exit 1
fi

docker compose build
docker compose up -d
docker compose ps

echo
echo "The site is at http://localhost:3309"
