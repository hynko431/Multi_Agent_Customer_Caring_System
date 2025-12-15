#!/bin/bash
# Script to create a clean, shareable zip package of the Multi-Agent Customer Care System

echo "🎁 Creating Multi-Agent Customer Care System - Share Package"
echo "================================================================="

PROJECT_DIR="$(pwd)"
PROJECT_NAME="Multi-Agent-Customer-Care-System"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ZIP_NAME="${PROJECT_NAME}_${TIMESTAMP}.zip"

echo "📍 Project Directory: $PROJECT_DIR"
echo "📦 Creating package: $ZIP_NAME"
echo ""

# Create temporary directory for clean copy
TEMP_DIR="/tmp/${PROJECT_NAME}_temp"
echo "🔧 Creating temporary directory: $TEMP_DIR"
rm -rf "$TEMP_DIR" 2>/dev/null
mkdir -p "$TEMP_DIR"

# Copy project files (excluding sensitive and unnecessary files)
echo "📂 Copying project files..."

# Copy all files except excluded ones
rsync -av --progress "$PROJECT_DIR/" "$TEMP_DIR/" \
  --exclude='.env' \
  --exclude='.claude/' \
  --exclude='venv/' \
  --exclude='__pycache__/' \
  --exclude='logs/' \
  --exclude='.DS_Store' \
  --exclude='*.pyc' \
  --exclude='*.pyo' \
  --exclude='*.log' \
  --exclude='test_api_keys.py' \
  --exclude='*.tmp' \
  --exclude='*.temp'

echo ""
echo "✅ Files copied successfully"

# Create the zip file in the parent directory
PARENT_DIR=$(dirname "$PROJECT_DIR")
ZIP_PATH="$PARENT_DIR/$ZIP_NAME"

echo "🗜️  Creating zip file: $ZIP_PATH"
cd "$(dirname "$TEMP_DIR")"
zip -r "$ZIP_PATH" "$(basename "$TEMP_DIR")" -q

# Clean up temporary directory
echo "🧹 Cleaning up temporary files..."
rm -rf "$TEMP_DIR"

# Get zip file size
ZIP_SIZE=$(du -h "$ZIP_PATH" | cut -f1)

echo ""
echo "================================================================="
echo "🎉 Package created successfully!"
echo "📁 Location: $ZIP_PATH"
echo "📏 Size: $ZIP_SIZE"
echo ""
echo "📋 What's included:"
echo "   ✅ All source code (agents/, tools/, memory/, planning/, utils/, data/)"
echo "   ✅ Main application files (main.py, config.py, streamlit_app.py)"
echo "   ✅ Documentation (README.md, CLAUDE.md, REPLICATION_PROMPT.md)"
echo "   ✅ Demo files (demo_questions.md, start_demo.py)"
echo "   ✅ Configuration template (.env.example)"
echo "   ✅ Dependencies (requirements.txt)"
echo "   ✅ Bash scripts (start/stop services)"
echo "   ✅ Testing files (test_system.py)"
echo ""
echo "🔒 What's excluded (for security/size):"
echo "   ❌ .env file (contains your API keys)"
echo "   ❌ venv/ directory (542MB - users recreate this)"
echo "   ❌ logs/ and __pycache__/ (auto-generated)"
echo "   ❌ .claude/ personal configuration"
echo ""
echo "📝 Recipients should:"
echo "   1. Extract the zip file"
echo "   2. Copy .env.example to .env and add their API keys"
echo "   3. Create virtual environment: python -m venv venv"
echo "   4. Activate environment: source venv/bin/activate"
echo "   5. Install dependencies: pip install -r requirements.txt"
echo "   6. Start the system: ./start_backend.sh and ./start_streamlit.sh"
echo ""
echo "🚀 Ready to share!"
echo "================================================================="