#!/bin/bash
set -eu

DIR=/usr/local/etc/redis

# Start Redis
echo Starting Redis.

"${@}" sed -e "s/{BACKING_REDIS_HOST}/${BACKING_REDIS_HOST}/g" -e "s/{BACKING_REDIS_PORT}/${BACKING_REDIS_PORT}/g" <  $DIR/redis.conf | redis-server -

exec "${@}"
