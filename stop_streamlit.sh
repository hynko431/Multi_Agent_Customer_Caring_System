#!/bin/bash
# Script to stop Streamlit frontend app

echo "🛑 Stopping Streamlit frontend app..."

# Kill all streamlit processes
STREAMLIT_PIDS=$(pgrep -f "streamlit run")
if [ -n "$STREAMLIT_PIDS" ]; then
    echo "📍 Found Streamlit processes: $STREAMLIT_PIDS"
    pkill -f "streamlit run"
    sleep 2
    
    # Check if processes are still running
    REMAINING_PIDS=$(pgrep -f "streamlit run")
    if [ -n "$REMAINING_PIDS" ]; then
        echo "⚠️  Some processes still running, force killing..."
        pkill -9 -f "streamlit run"
        sleep 1
    fi
    
    echo "✅ Streamlit app stopped successfully"
else
    echo "ℹ️  No Streamlit processes found running"
fi

# Kill any processes on port 8501
PORT_8501_PIDS=$(lsof -ti:8501 2>/dev/null)
if [ -n "$PORT_8501_PIDS" ]; then
    echo "📍 Found processes on port 8501: $PORT_8501_PIDS"
    kill -9 $PORT_8501_PIDS 2>/dev/null
    echo "✅ Port 8501 cleared"
fi

# Verify port is free
if lsof -i:8501 >/dev/null 2>&1; then
    echo "❌ Port 8501 is still in use!"
    lsof -i:8501
else
    echo "✅ Port 8501 is now free"
fi

echo "🔄 Streamlit shutdown complete"