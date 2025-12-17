# Multi-Agent Customer Care System - CLAUDE.md

This file provides comprehensive guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Overview

This is a **Multi-Agent Customer Care System** - a production-ready demonstration of coordinated AI agents providing comprehensive customer support. The system showcases advanced multi-agent coordination, natural language processing, and comprehensive customer service automation.

### 🏗️ **System Architecture**
- **Language**: Python 3.10+ (currently 3.13)
- **Backend**: FastAPI with async/await patterns
- **Frontend**: Streamlit with beautiful chat interface
- **AI Models**: OpenAI GPT-4 + Google Gemini 2.0-flash
- **Total LOC**: ~2,861 lines across 27 Python files
- **Agent Coordination**: Sequential, Parallel, and Conditional execution modes

## Environment Setup

### Virtual Environment
The project uses a Python virtual environment located in `venv/`:
- **Activate virtual environment**: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)  
- **Install dependencies**: `pip install -r requirements.txt`

### API Keys Configuration
1. Copy `.env.example` to `.env`
2. Add your API keys:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### Python Version
- Requires Python 3.10+
- Currently configured for Python 3.13

## 🚀 **Running the Application**

### **Bash Scripts (Recommended)**
The project includes dedicated bash scripts for service management:

```bash
# Stop any existing services
./stop_backend.sh
./stop_streamlit.sh

# Start backend (Terminal 1)
./start_backend.sh

# Start Streamlit (Terminal 2) 
./start_streamlit.sh
```

### **Manual Commands**

#### **Option 1: Streamlit Demo (Recommended for Demos)**
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies  
pip install -r requirements.txt

# Start Streamlit interface
streamlit run streamlit_app.py --server.port 8501
```
**✅ Demo interface: http://localhost:8501**

#### **Option 2: FastAPI Server (For API Access)**
```bash
# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
python main.py
```
**✅ API server: http://localhost:8000**
**✅ Interactive docs: http://localhost:8000/docs**

### **Debugging with Separate Terminals**
For debugging purposes, run services in separate terminals to see console errors clearly:

#### **Terminal 1 - Backend Server**
```bash
cd /path/to/project
source venv/bin/activate
python main.py
```

#### **Terminal 2 - Streamlit Frontend**
```bash
cd /path/to/project  
source venv/bin/activate
streamlit run streamlit_app.py --server.port 8501
```

### **Service Management Commands**
```bash
# Kill processes if needed
pkill -f "python main.py"
pkill -f "streamlit run"

# Check what's running on ports
lsof -i :8000  # Backend port
lsof -i :8501  # Streamlit port
```

### Testing the System
```bash
# Run demo scenario
curl -X GET http://localhost:8000/demo

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "My laptop order #12345 won'\''t turn on, I need help!"}'

# Check system status
curl -X GET http://localhost:8000/
```

## Project Architecture

### Multi-Agent System Components

1. **Orchestrator Agent** (`agents/orchestrator.py`)
   - Main coordinator that receives requests and manages specialist agents
   - Creates execution plans and synthesizes responses

2. **Specialist Agents**:
   - **Order Agent** (`agents/order_agent.py`) - Order lookups, tracking, returns
   - **Tech Support Agent** (`agents/tech_support_agent.py`) - Troubleshooting and technical help
   - **Product Agent** (`agents/product_agent.py`) - Product info, comparisons, recommendations  
   - **Solutions Agent** (`agents/solutions_agent.py`) - Returns, exchanges, problem resolution

3. **Supporting Systems**:
   - **Memory System** (`memory/session_memory.py`) - Conversation context and history
   - **Planning Module** (`planning/planner.py`) - Creates and validates execution plans
   - **Tool Library** (`tools/`) - Reusable functions for all agents

### Project Structure
```
├── main.py                     # FastAPI application entry point
├── config.py                   # Configuration and API keys
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── agents/                    # All agent implementations
│   ├── base_agent.py         # Base class for all agents
│   ├── orchestrator.py       # Main coordinator
│   ├── order_agent.py        # Order specialist
│   ├── tech_support_agent.py # Technical support
│   ├── product_agent.py      # Product expert
│   └── solutions_agent.py    # Solutions specialist
├── data/                     # Mock data and sample content
│   └── mock_data.py         # Orders, products, knowledge base
├── memory/                   # Session and conversation management
│   └── session_memory.py    # Memory system implementation
├── planning/                 # Agent coordination and planning
│   └── planner.py           # Plan creation and execution
├── tools/                    # Tool library for agents
│   ├── search_tools.py      # Web search using Gemini
│   ├── order_tools.py       # Order management functions
│   ├── product_tools.py     # Product queries and comparison
│   └── knowledge_tools.py   # Knowledge base and policies
├── utils/                    # Utility modules
│   ├── logging_config.py     # Colored logging setup
│   └── formatters.py         # Response formatting
├── streamlit_app.py          # Streamlit frontend interface
├── demo_questions.md         # Demo scenarios and questions
├── start_backend.sh          # Backend startup script
├── start_streamlit.sh        # Streamlit startup script
├── stop_backend.sh           # Backend shutdown script
├── stop_streamlit.sh         # Streamlit shutdown script
├── start_demo.py             # Interactive launcher
└── test_system.py            # System validation tests
```

## API Endpoints

- `GET /` - Health check and system status
- `POST /chat` - Process customer messages with multi-agent coordination
- `GET /session/{id}` - Retrieve conversation history
- `GET /agents` - List all available agents and capabilities
- `GET /demo` - Run pre-scripted demo scenario
- `POST /reset` - Clear all sessions for demo reset
- `GET /sessions` - List active session IDs

**Interactive API Documentation**: http://localhost:8000/docs

## Demo Scenario

The system demonstrates multi-agent collaboration through this scenario:
1. Customer: "My laptop order #12345 won't turn on, I need help!"
2. **Order Agent** retrieves order details and warranty info
3. **Tech Support Agent** provides troubleshooting steps
4. **Solutions Agent** offers resolution options (repair/replace/refund)
5. **Orchestrator** synthesizes all responses into coherent answer

## Key Features

- **Async/await** throughout for performance
- **Colored console logging** for demo visibility  
- **Type hints and docstrings** for code clarity
- **30-second timeout** per request
- **Graceful error handling** with fallbacks
- **Mock data** for demonstration (no database required)
- **Session memory** maintains conversation context

## Development Notes

- The system works with or without API keys (uses mock responses as fallback)
- All agents extend `BaseAgent` for consistent behavior
- Planning module supports sequential, parallel, and conditional execution
- Memory system automatically extracts context from conversations
- Comprehensive logging shows agent decisions and tool usage
- Response synthesis creates natural, unified customer service experience

## 🛠️ **Technical Implementation Details**

### **Multi-Agent Coordination**
- **Sequential Execution**: Steps run one after another (dependencies required)
- **Parallel Execution**: Steps run simultaneously (independent tasks)
- **Conditional Execution**: Steps run based on previous results (smart coordination)

### **Session Management**
- Each conversation maintains session state and memory
- Context automatically extracted: orders discussed, products mentioned, issues identified
- Memory persists across conversation turns
- Session cleanup and expiration handling

### **Error Handling & Resilience**
- 30-second timeout protection per request
- Graceful fallbacks to mock responses if API keys missing
- Comprehensive error handling in FastAPI with JSONResponse objects
- Session validation and automatic creation

### **Code Architecture Patterns**
- **Base Agent Pattern**: All agents extend `BaseAgent` for consistent behavior
- **Tool Library Pattern**: Reusable functions across all agents
- **Async/Await**: Throughout for high performance
- **Type Hints**: Complete type annotations for code clarity
- **Dependency Injection**: Configuration and API keys centralized

## 🐛 **Bug Fixes Implemented**

### **Critical Fixes**
1. **Session Management**: Added `memory.get_or_create_session()` in orchestrator to prevent "Session not found" errors
2. **FastAPI Error Handlers**: Changed to return `JSONResponse` objects instead of dictionaries
3. **Gemini API Model**: Updated from deprecated `"gemini-pro"` to `"gemini-2.0-flash"`

### **Performance Optimizations**
- Async/await patterns throughout
- Efficient session memory management
- Proper error response handling
- Resource cleanup and timeout protection

## 🧪 **Testing & Validation**

### **System Tests**
```bash
# Test API endpoints
curl -X GET http://localhost:8000/demo

# Validate both AI models
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from google import genai

# Test OpenAI
client_oa = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
print('OpenAI:', client_oa.chat.completions.create(model='gpt-4', messages=[{'role':'user','content':'test'}]).choices[0].message.content)

# Test Gemini  
client_g = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
print('Gemini:', client_g.models.generate_content(model='gemini-2.0-flash', contents='test').text)
"
```

### **Demo Scenarios**
Primary test: `"My laptop order #12345 won't turn on, I need help!"`
- Tests order lookup, technical support, and solution coordination
- Demonstrates all three execution modes
- Shows tool integration and response synthesis

## 🎯 **Best Practices & Conventions**

### **Code Style**
- Use type hints for all function parameters and returns
- Async/await for all I/O operations
- Comprehensive error handling with specific exception types
- Clear docstrings for all classes and methods

### **Agent Design**
- Each agent has specific domain expertise
- Tools are shared across agents via tool library
- System prompts define agent behavior and personality
- Response format should be consistent across agents

### **Configuration Management**
- Environment variables for sensitive data (API keys)
- Centralized configuration in `config.py`
- Graceful degradation when API keys missing
- Model configurations per agent type

## 🚨 **Known Issues & Limitations**

- **API Rate Limits**: OpenAI and Gemini APIs have rate limits for free tiers
- **Response Time**: Complex requests can take 20-30 seconds with real AI calls
- **Mock Data**: Limited to demonstration scenarios (3 orders, 4 products)
- **Memory Persistence**: Sessions cleared on restart (no database persistence)

## 🔧 **Troubleshooting**

### **Common Issues**
- **"Module not found"**: Ensure virtual environment is activated and dependencies installed
- **"Session not found"**: Fixed in current version, use updated orchestrator.py
- **API errors**: Check `.env` file has valid API keys
- **Port conflicts**: Use bash scripts or change ports in config
- **Timeout errors**: Complex requests may need adjustment in `config.py`

### **Service Issues**
- **Backend won't start**: Check port 8000 availability, use `./stop_backend.sh` first
- **Streamlit errors**: Ensure backend is running, check console for connection errors
- **API key validation**: Both OpenAI and Gemini keys are validated on startup

### **Debugging Commands**
```bash
# Check service status
./stop_backend.sh && ./stop_streamlit.sh
lsof -i :8000,8501

# View logs in separate terminals
./start_backend.sh    # Terminal 1 - shows API logs
./start_streamlit.sh  # Terminal 2 - shows frontend logs
```

## 📊 **Performance Metrics**
- **Total Lines of Code**: ~2,861 lines across 27 Python files
- **Average Response Time**: 15-30 seconds with real AI APIs
- **Memory Usage**: ~100MB per session
- **Concurrent Sessions**: Supports multiple simultaneous users
- **API Calls**: 2-4 API calls per complex request (depending on agents involved)