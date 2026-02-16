#!/bin/sh
set -e

# ---------------------------------------------------------------------------
# Signal handling: forward SIGTERM/SIGINT to uvicorn so it shuts down
# gracefully (flushes DB connections, finishes in-flight requests).
# ---------------------------------------------------------------------------
UVICORN_PID=""
NGINX_PID=""

cleanup() {
    echo "=== Caught shutdown signal ==="
    if [ -n "$UVICORN_PID" ] && kill -0 "$UVICORN_PID" 2>/dev/null; then
        echo "Sending SIGTERM to uvicorn (PID $UVICORN_PID)..."
        kill -TERM "$UVICORN_PID" 2>/dev/null || true
        # Wait up to 30s for graceful shutdown
        GRACE=30
        while [ $GRACE -gt 0 ] && kill -0 "$UVICORN_PID" 2>/dev/null; do
            sleep 1
            GRACE=$((GRACE - 1))
        done
        if kill -0 "$UVICORN_PID" 2>/dev/null; then
            echo "Uvicorn did not stop in time, sending SIGKILL"
            kill -9 "$UVICORN_PID" 2>/dev/null || true
        fi
    fi
    echo "=== Stopping Nginx ==="
    if [ -n "$NGINX_PID" ] && kill -0 "$NGINX_PID" 2>/dev/null; then
         kill -QUIT "$NGINX_PID" 2>/dev/null || true
    fi
    exit 0
}

trap cleanup TERM INT QUIT

# Ports: public 3000 (nginx), backend 8000 (FastAPI) – keep different to avoid confusion
BACKEND_PORT=${BACKEND_PORT:-8000}
# FORCE public port to 3000. Ignoring $PORT env var to prevent mismatch if Dokploy passes unique internal ports.
# User MUST set Dokploy Container Port to 3000.
PUBLIC_PORT=3000

# ---------------------------------------------------------------------------

# Dynamic Nginx Configuration
# ---------------------------------------------------------------------------
# Replace hardcoded ports in nginx.conf with environment variables
# This allows Dokploy to assign a random port (e.g. 3000 -> $PORT) and we match it.
echo "=== Container Startup ==="
echo "Date: $(date)"
echo "User: $(whoami) (ID: $(id -u))"
echo "Arch: $(uname -m)"
echo "Working directory: $(pwd)"
echo "Python: $(python3 --version 2>/dev/null || true)"
echo "Configuration:"
echo "  - PUBLIC_PORT (Nginx): ${PUBLIC_PORT}"
echo "  - BACKEND_PORT (FastAPI): ${BACKEND_PORT}"
echo "  - DATABASE_URL: ${DATABASE_URL:0:15}..."

echo "Configuring Nginx with PORT=${PUBLIC_PORT}..."
# Reset config to template if needed (optional, but good for restarts if file persisted)
# We assume pure container restart here.

if ! sed -i "s/listen 3000;/listen ${PUBLIC_PORT};/g" /etc/nginx/nginx.conf; then
    echo "ERROR: Failed to patch Nginx PORT. Check permissions on /etc/nginx"
    sleep 30
    exit 1
fi
if ! sed -i "s/listen \[::\]:3000;/listen \[::\]:${PUBLIC_PORT};/g" /etc/nginx/nginx.conf; then
    echo "ERROR: Failed to patch Nginx [::] PORT. Check permissions on /etc/nginx"
    sleep 30
    exit 1
fi

echo "Configuring Nginx upstream to BACKEND_PORT=${BACKEND_PORT}..."
if ! sed -i "s/server 127.0.0.1:8000;/server 127.0.0.1:${BACKEND_PORT};/g" /etc/nginx/nginx.conf; then
    echo "ERROR: Failed to patch Nginx backend port. Check permissions on /etc/nginx"
    sleep 30
    exit 1
fi

if [ -z "$DATABASE_URL" ]; then
    echo "CRITICAL ERROR: DATABASE_URL is NOT set in the environment!"
    sleep 10 # Wait for logs to flush
    exit 1
else
    if echo "$DATABASE_URL" | grep -q "localhost"; then
        echo "WARNING: DATABASE_URL contains 'localhost'. In Docker, this usually fails."
        echo "Use the service name or host IP instead."
    fi
fi

if [ -z "$SECRET_KEY" ]; then
    echo "CRITICAL ERROR: SECRET_KEY is NOT set!"
    sleep 10
    exit 1
fi

if [ -z "$FIRECRAWL_API_KEY" ]; then
    echo "WARNING: FIRECRAWL_API_KEY is NOT set. Search features will fail."
fi

if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "WARNING: OPENROUTER_API_KEY is NOT set. AI features will fail."
fi

# Verify we're at project root and backend is present
if [ ! -d "backend" ] || [ ! -f "backend/main.py" ]; then
    echo "ERROR: backend/ or backend/main.py not found in $(pwd)"
    ls -la
    sleep 10
    exit 1
fi

if [ ! -f "frontend/dist/index.html" ]; then
    echo "ERROR: frontend/dist/index.html not found (Vite build missing or failed)"
    ls -la frontend/dist 2>/dev/null || true
    sleep 30
    exit 1
fi

echo "Testing Nginx configuration..."
nginx -t

echo "Running database migrations..."

if ! command -v alembic >/dev/null 2>&1; then
    echo "ERROR: 'alembic' command not found. Ensure it is in requirements.txt"
    sleep 30
    exit 1
fi

if ! (cd backend && alembic upgrade head); then

    echo "ERROR: Database migrations failed!"
    echo "Check your DATABASE_URL and ensure the database is running."
    sleep 10 # Important: wait to ensure logs are captured by deployment tool
    exit 1
fi
echo "Database migrations completed successfully."

echo "Starting FastAPI on port ${BACKEND_PORT}..."
uvicorn backend.main:app \
    --host 0.0.0.0 \
    --port "${BACKEND_PORT}" \
    --loop asyncio \
    --timeout-keep-alive 65 \
    --log-level info &
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
        sleep 5
        exit 1
    fi
    sleep 1
    WAIT_COUNT=$((WAIT_COUNT + 1))
done

if [ $WAIT_COUNT -eq $MAX_WAIT ]; then
    echo "ERROR: FastAPI did not start within ${MAX_WAIT}s"
    sleep 5
    exit 1
fi

echo "Starting Nginx on port ${PUBLIC_PORT}..."
nginx -g 'daemon off;' &
NGINX_PID=$!
echo "Nginx PID: $NGINX_PID"

# Wait for either process to exit
wait -n $UVICORN_PID $NGINX_PID 2>/dev/null || wait $UVICORN_PID
echo "A child process exited, shutting down..."
cleanup

