#!/bin/bash
# Backend startup script

cd "$(dirname "$0")"

echo "Starting FireCrawl Agent Backend API..."
echo ""

# Check if virtual environment exists
if [ -d "../venv" ]; then
    echo "Activating virtual environment..."
    source ../venv/bin/activate
fi

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "[FAIL] FastAPI not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Check environment variables
if [ -z "$FIRECRAWL_API_KEY" ] || [ -z "$OPENROUTER_API_KEY" ]; then
    echo "[WARN] Environment variables not set!"
    echo "   Make sure FIRECRAWL_API_KEY and OPENROUTER_API_KEY are set"
    echo ""
fi

echo "Starting server on http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run uvicorn from project root for correct module resolution
# Use asyncio loop instead of uvloop to avoid nest_asyncio conflicts
cd ..
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --loop asyncio

