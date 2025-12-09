#!/bin/sh
set -e
cd /app/server
. .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 &
cd /app/client
export PORT=9000
node build # No need for "&" as we want to keep the server running in the foreground
