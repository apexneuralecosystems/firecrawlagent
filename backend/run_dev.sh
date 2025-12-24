#!/bin/bash
# Development server with hot reload
# Run from project root: ./backend/run_dev.sh

cd "$(dirname "$0")/.."

echo "🚀 Starting FireCrawl Agent Backend API (with reload)..."
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Check environment variables
if [ -z "$FIRECRAWL_API_KEY" ] || [ -z "$OPENROUTER_API_KEY" ]; then
    echo "⚠️  Warning: Environment variables not set!"
    echo "   Make sure FIRECRAWL_API_KEY and OPENROUTER_API_KEY are set"
    echo ""
fi

echo "🌐 Starting server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔄 Hot reload enabled"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run from project root so module path is correct
# Use asyncio loop instead of uvloop to avoid nest_asyncio conflicts
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 --loop asyncio

