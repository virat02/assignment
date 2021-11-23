#!/bin/bash
set -eu

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn wsgi:proxy_app \
    --worker-connections ${MAX_CLIENTS} \
    --max-requests ${MAX_REQUESTS} \
    -b ${PROXY_ADDRESS}