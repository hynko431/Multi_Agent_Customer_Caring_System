# 🚀 Multi-Agent Customer Care System - Setup Instructions

**Thank you for downloading the Multi-Agent Customer Care System!** This document will guide you through setting up and running the system on your machine.

## 📋 **Quick Overview**

This is a production-ready demonstration of coordinated AI agents providing comprehensive customer support:
- **5 AI Agents** working together (Orchestrator + 4 specialists)
- **Beautiful Streamlit Interface** with agent visualization  
- **FastAPI Backend** with comprehensive API documentation
- **Real AI Integration** (OpenAI GPT-4 + Google Gemini)
- **Mock Data** for immediate demonstration (no database required)

## 🔧 **Prerequisites**

- **Python 3.10+** (Python 3.13 recommended)
- **Internet connection** (for AI API calls)
- **Terminal/Command Line** access

## ⚡ **Quick Start (5 minutes)**

### **Step 1: Extract and Navigate**
```bash
# Extract the zip file and navigate to the project
cd Multi-Agent-Customer-Care-System
```

### **Step 2: Set Up Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **Step 3: Configure API Keys (Optional)**
```bash
# Copy the template
cp .env.example .env

# Edit .env file and add your API keys (optional):
# OPENAI_API_KEY=your_openai_api_key_here
# GEMINI_API_KEY=your_gemini_api_key_here
```

**Note**: The system works without API keys using intelligent mock responses for demonstration.

### **Step 4: Start the System**
```bash
# Option A: Use convenience scripts (recommended)
./start_backend.sh     # Terminal 1 - Backend
./start_streamlit.sh   # Terminal 2 - Frontend

# Option B: Manual start
python main.py                           # Terminal 1 - Backend
streamlit run streamlit_app.py           # Terminal 2 - Frontend
```

### **Step 5: Access the Demo**
- **🎨 Streamlit Demo**: http://localhost:8501 (Beautiful chat interface)
- **📖 API Documentation**: http://localhost:8000/docs (Interactive API docs)

## 🎭 **Demo Instructions**

### **Try These Example Questions:**

#### **Primary Demo (Multi-Agent Coordination):**
```
"My laptop order #12345 won't turn on, I need help!"
```
This demonstrates all agents working together:
1. **Order Agent** → Retrieves order details and warranty
2. **Tech Support Agent** → Provides troubleshooting steps  
3. **Solutions Agent** → Offers resolution options
4. **Orchestrator** → Synthesizes unified response

#### **Follow-up Questions (Memory Test):**
```
"What other laptops do you have in similar price range?"
"What would you recommend for gaming instead?"
```

#### **Other Scenarios:**
- `"Compare TechBook Pro 15 vs TechBook Air 13"`
- `"I want to track my order #12346"`
- `"My laptop is overheating, what should I do?"`
- `"Show me all laptops under $1000"`

## 🔧 **Service Management**

### **Start Services:**
```bash
./start_backend.sh      # Starts FastAPI on port 8000
./start_streamlit.sh    # Starts Streamlit on port 8501
```

### **Stop Services:**
```bash
./stop_backend.sh       # Stops all backend processes
./stop_streamlit.sh     # Stops all Streamlit processes
```

### **Check Status:**
```bash
lsof -i :8000          # Check backend port
lsof -i :8501          # Check frontend port
```

## 🎯 **API Usage**

### **Test API Directly:**
```bash
# Health check
curl http://localhost:8000/

# Run demo scenario
curl http://localhost:8000/demo

# Chat with the system
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Help me with order 12345"}'
```

## 🧪 **System Validation**

### **Run Tests:**
```bash
# Basic system test
python test_system.py

# Interactive launcher
python start_demo.py
```

## 🔑 **API Keys Setup (Optional but Recommended)**

### **Get Your Keys:**

#### **OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Create account or sign in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

#### **Google Gemini API Key:**
1. Go to https://makersuite.google.com/app/apikey
2. Create or sign in to Google account
3. Click "Create API key"
4. Copy the key (starts with `AIza`)

### **Add Keys to .env:**
```bash
# Edit the .env file
OPENAI_API_KEY=sk-your-openai-key-here
GEMINI_API_KEY=AIza-your-gemini-key-here
```

**Without API keys**: System uses intelligent mock responses for demonstration.
**With API keys**: Full AI-powered responses (may take 20-30 seconds per complex request).

## 🛠️ **Troubleshooting**

### **Common Issues:**

#### **"Module not found" errors:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

#### **Port already in use:**
```bash
# Kill existing processes
./stop_backend.sh
./stop_streamlit.sh

# Or manually:
pkill -f "python main.py"
pkill -f "streamlit run"
```

#### **Permission denied on scripts:**
```bash
# Make scripts executable
chmod +x *.sh
```

#### **Slow responses:**
- With API keys: 20-30 seconds normal (real AI processing)
- Without API keys: Instant responses (mock data)

### **Getting Help:**

1. **Check Logs**: Run services in separate terminals to see error messages
2. **Read Documentation**: CLAUDE.md has comprehensive technical details
3. **API Documentation**: http://localhost:8000/docs for API reference

## 📊 **System Architecture**

### **Agent Overview:**
- **🎯 Orchestrator**: Coordinates all specialist agents
- **📦 Order Agent**: Order tracking, modifications, returns
- **🔧 Tech Support**: Troubleshooting and technical assistance  
- **🛍️ Product Agent**: Product information and comparisons
- **💡 Solutions Agent**: Returns, exchanges, problem resolution

### **Execution Modes:**
- **Sequential**: Agents run one after another
- **Parallel**: Multiple agents run simultaneously
- **Conditional**: Agents run based on dependencies

### **Tech Stack:**
- **Backend**: FastAPI with async/await
- **Frontend**: Streamlit with real-time visualization
- **AI**: OpenAI GPT-4 + Google Gemini 2.0-flash
- **Memory**: Session-based conversation context
- **Data**: Mock data (3 orders, 4 products, knowledge base)

## 🎉 **What's Next?**

### **For Learning:**
- Explore the code architecture in different modules
- Try different demo questions to see agent coordination
- Check the execution plans in the Streamlit interface

### **For Development:**
- Read `REPLICATION_PROMPT.md` for complete implementation guide
- Modify mock data in `data/mock_data.py`
- Extend agents with new capabilities
- Add new tools in the `tools/` directory

### **For Production:**
- Add database integration for persistent storage
- Implement user authentication and authorization
- Add monitoring and logging systems
- Scale with Docker and orchestration platforms

---

## 🚀 **Ready to Explore!**

Your Multi-Agent Customer Care System is now ready! Start with the Streamlit interface at **http://localhost:8501** and try the demo question: **"My laptop order #12345 won't turn on, I need help!"**

Watch as multiple AI agents coordinate to provide comprehensive customer support! 🎭

**Enjoy exploring the future of AI customer service!** ✨