#!/bin/bash
# Script to start FastAPI backend server

echo "🚀 Starting FastAPI backend server..."

# Check if port 8000 is already in use
if lsof -i:8000 >/dev/null 2>&1; then
    echo "❌ Port 8000 is already in use!"
    echo "📍 Processes using port 8000:"
    lsof -i:8000
    echo ""
    echo "💡 Run './stop_backend.sh' first to stop existing processes"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "💡 Please create virtual environment first: python -m venv venv"
    exit 1
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found!"
    echo "💡 Make sure you're in the correct directory"
    exit 1
fi

# Activate virtual environment and start server
echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "🔍 Checking dependencies..."
if ! python -c "import fastapi, uvicorn" 2>/dev/null; then
    echo "❌ Missing dependencies!"
    echo "💡 Install dependencies: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Starting FastAPI server on http://localhost:8000"
echo "📖 Interactive docs available at: http://localhost:8000/docs"
echo "🔄 Press Ctrl+C to stop the server"
echo ""

# Start the server
python main.py