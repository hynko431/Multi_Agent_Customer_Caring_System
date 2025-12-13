#!/bin/bash
# Script to stop FastAPI backend server

echo "🛑 Stopping FastAPI backend server..."

# Kill all python main.py processes
BACKEND_PIDS=$(pgrep -f "python main.py")
if [ -n "$BACKEND_PIDS" ]; then
    echo "📍 Found backend processes: $BACKEND_PIDS"
    pkill -f "python main.py"
    sleep 2
    
    # Check if processes are still running
    REMAINING_PIDS=$(pgrep -f "python main.py")
    if [ -n "$REMAINING_PIDS" ]; then
        echo "⚠️  Some processes still running, force killing..."
        pkill -9 -f "python main.py"
        sleep 1
    fi
    
    echo "✅ Backend server stopped successfully"
else
    echo "ℹ️  No backend processes found running"
fi

# Kill any processes on port 8000
PORT_8000_PIDS=$(lsof -ti:8000 2>/dev/null)
if [ -n "$PORT_8000_PIDS" ]; then
    echo "📍 Found processes on port 8000: $PORT_8000_PIDS"
    kill -9 $PORT_8000_PIDS 2>/dev/null
    echo "✅ Port 8000 cleared"
fi

# Verify port is free
if lsof -i:8000 >/dev/null 2>&1; then
    echo "❌ Port 8000 is still in use!"
    lsof -i:8000
else
    echo "✅ Port 8000 is now free"
fi

echo "🔄 Backend shutdown complete"