#!/bin/sh
set -e

# Ports: public 3000 (nginx), backend 8000 (FastAPI) – keep different to avoid confusion
BACKEND_PORT=${BACKEND_PORT:-8000}
PUBLIC_PORT=${PORT:-3000}

echo "=== Container Startup ==="
echo "Working directory: $(pwd)"
echo "Python: $(python3 --version 2>/dev/null || true)"
echo "Ports: public=${PUBLIC_PORT} (nginx) backend=${BACKEND_PORT} (FastAPI)"

# Verify we're at project root and backend is present
if [ ! -d "backend" ] || [ ! -f "backend/main.py" ]; then
    echo "ERROR: backend/ or backend/main.py not found in $(pwd)"
    ls -la
    exit 1
fi

if [ ! -d "frontend/dist" ]; then
    echo "ERROR: frontend/dist not found (Vite build missing)"
    ls -la frontend/ 2>/dev/null || true
    exit 1
fi

echo "Starting FastAPI on port ${BACKEND_PORT}..."
uvicorn backend.main:app --host 0.0.0.0 --port "${BACKEND_PORT}" &
UVICORN_PID=$!
echo "Uvicorn PID: $UVICORN_PID"

# Wait for backend to be ready (max 60s)
MAX_WAIT=60
WAIT_COUNT=0
while [ $WAIT_COUNT -lt $MAX_WAIT ]; do
    if nc -z 127.0.0.1 "${BACKEND_PORT}" 2>/dev/null; then
        echo "FastAPI is ready on port ${BACKEND_PORT}"
        break
    fi
    if [ $((WAIT_COUNT % 10)) -eq 0 ] && [ $WAIT_COUNT -gt 0 ]; then
        echo "Waiting for FastAPI... ($WAIT_COUNT s)"
    fi
    if ! kill -0 $UVICORN_PID 2>/dev/null; then
        echo "ERROR: Uvicorn process exited"
        exit 1
    fi
    sleep 1
    WAIT_COUNT=$((WAIT_COUNT + 1))
done

if [ $WAIT_COUNT -eq $MAX_WAIT ]; then
    echo "ERROR: FastAPI did not start within ${MAX_WAIT}s"
    exit 1
fi

echo "Starting Nginx on port ${PUBLIC_PORT}..."
exec nginx -g 'daemon off;'
