#!/bin/bash
# Frontend startup script

cd "$(dirname "$0")"

echo "🚀 Starting FireCrawl Agent Frontend..."
echo ""

# Check if bun is installed
if ! command -v bun &> /dev/null; then
    echo "❌ Bun is not installed!"
    echo "   Install it from: https://bun.sh"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    bun install
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Creating .env from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
    else
        echo "VITE_API_URL=http://localhost:8000" > .env
    fi
fi

echo "🌐 Starting development server on http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

bun run dev

