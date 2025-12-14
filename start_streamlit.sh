#!/bin/bash
# Script to start Streamlit frontend app

echo "🚀 Starting Streamlit frontend app..."

# Check if port 8501 is already in use
if lsof -i:8501 >/dev/null 2>&1; then
    echo "❌ Port 8501 is already in use!"
    echo "📍 Processes using port 8501:"
    lsof -i:8501
    echo ""
    echo "💡 Run './stop_streamlit.sh' first to stop existing processes"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "💡 Please create virtual environment first: python -m venv venv"
    exit 1
fi

# Check if streamlit_app.py exists
if [ ! -f "streamlit_app.py" ]; then
    echo "❌ streamlit_app.py not found!"
    echo "💡 Make sure you're in the correct directory"
    exit 1
fi

# Activate virtual environment and start app
echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "🔍 Checking dependencies..."
if ! python -c "import streamlit" 2>/dev/null; then
    echo "❌ Streamlit not installed!"
    echo "💡 Install dependencies: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Starting Streamlit app on http://localhost:8501"
echo "💬 Beautiful chat interface with agent visualization"
echo "🔄 Press Ctrl+C to stop the app"
echo ""

# Start the Streamlit app
streamlit run streamlit_app.py --server.port 8501