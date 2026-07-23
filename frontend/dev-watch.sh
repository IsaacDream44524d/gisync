#!/bin/bash

# Dev server auto-restart script
# This script will automatically restart the dev server if it crashes
#modify with flask

echo "🚀 Starting Gentelella dev server with auto-restart..."

while true; do
    echo "📡 Starting dev server on http://localhost:3000"
    npm run dev
    
    exit_code=$?
    echo "⚠️  Dev server stopped with exit code: $exit_code"
    
    if [ $exit_code -eq 0 ]; then
        echo "✅ Dev server stopped normally"
        break
    else
        echo "🔄 Dev server crashed, restarting in 2 seconds..."
        sleep 2
    fi
done