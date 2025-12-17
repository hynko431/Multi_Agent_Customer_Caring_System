# 🤖 Multi-Agent Customer Care System

A production-ready demonstration of a **coordinated multi-agent ecosystem** designed to provide comprehensive, high-quality customer support. This system leverages the latest AI technologies to simulate a real-world customer service department where specialized agents collaborate to solve complex user problems.

---

## 📖 Project Overview

Modern customer service requires more than just a chatbot; it requires a team of experts. This project implements a **Multi-Agent Orchestration** pattern where a central "Orchestrator" analyzes incoming requests and delegates work to specialized agents:

- **📦 Order Specialist**: Expert in logistics, tracking, and warranty validation.
- **🔧 Technical Support**: Dedicated to step-by-step troubleshooting and technical solutions.
- **🛍️ Product Expert**: Knowledgeable about specifications, comparisons, and inventory.
- **💡 Solutions Architect**: Authorized to handle returns, exchanges, and customer compensation.

The system is built with resilience in mind, featuring **graceful degradation** (mock fallbacks if API keys are missing), **async execution**, and highly detailed **session memory**.

---

## 🏗️ System Architecture

The following diagram illustrates how the Orchestrator coordinates with specialist agents and supporting systems to fulfill a customer request.

```mermaid
graph TD
    User([USER]) -->|Message| Orchestrator[Orchestrator Agent]
    
    subgraph "Orchestration Layer"
        Orchestrator --> Planner[Planning Module]
        Orchestrator --> Memory[Session Memory]
    end
    
    Planner -->|Execution Plan| Coordinator{Task Coordinator}
    
    subgraph "Specialist Agents"
        Coordinator -->|Order Tasks| OrderAgent[Order Agent]
        Coordinator -->|Technical Tasks| TechAgent[Tech Support Agent]
        Coordinator -->|Product Queries| ProductAgent[Product Agent]
        Coordinator -->|Resolutions| SolutionsAgent[Solutions Agent]
    end
    
    subgraph "Tool Library"
        OrderAgent --> OrderTools[Order Tools]
        TechAgent --> KnowledgeTools[Knowledge Base Tools]
        ProductAgent --> ProductTools[Product Tools]
        Coordinator --> SearchTools[Gemini 2.0 Web Search]
    end
    
    Specialist Agents -->|Results| Orchestrator
    Orchestrator -->|Synthesized Response| User
```

### Coordination Modes
- **Sequential**: Tasks are executed in a specific order when dependencies exist.
- **Parallel**: Independent tasks are executed simultaneously to minimize response time.
- **Conditional**: Tasks are dynamically triggered based on the results of previous steps.

---

## ✨ Key Features

- **🚀 Gemini 2.0 Flash Integration**: Uses the new `google-genai` SDK for high-speed web search and information retrieval.
- **🧠 Context-Aware Memory**: Sessions automatically extract order IDs, product names, and issue history to maintain continuity.
- **🛡️ Production-Grade Reliability**: 30-second timeout protection, robust error handling, and colored console logging for deep visibility.
- **🎨 Beautiful Dual Interface**: 
    - **Streamlit Frontend**: A polished, modern chat UI with real-time agent activity visualization.
    - **FastAPI Backend**: A high-performance REST API with auto-generated OpenAPI documentation.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- (Optional) OpenAI and Google Gemini API keys

### 2. Setup
```bash
# Clone the repository
git clone <repository-url>
cd Multi-Agent-Customer-Care-System

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Copy `.env.example` to `.env` and add your API keys:
```env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
```
*Note: The system will automatically use high-fidelity mock data if keys are not provided.*

---

## 🕹️ Running the Application

### Option A: Interactive Streamlit UI (Recommended)
```bash
python -m streamlit run streamlit_app.py
```
Visit `http://localhost:8501` to use the interactive chat.

### Option B: FastAPI Backend
```bash
python main.py
```
Access the REST API at `http://localhost:8000` and documentation at `/docs`.

---

## 🧪 Try It Out

Try asking the system:
1. *"My laptop order #12345 won't turn on, I need help!"*
2. *"How does the TechBook Pro 15 compare to the TechBook Air 13?"*
3. *"Is my order #12346 still on track for delivery?"*

---

## 📁 Repository Structure

- `agents/`: Core logic for Orchestrator and Specialists.
- `tools/`: Gemini search, order management, and knowledge base retrieval.
- `memory/`: Session state and context extraction logic.
- `planning/`: Orchestration logic for task coordination.
- `data/`: Mock database containing sample orders and products.
- `utils/`: Formatting and logging utilities.

---

*This system is a demonstration of advanced AI agent coordination and is suitable for educational and prototype development purposes.*

## 🔍 Verification for Long-Term Memory (Phase 2)

To verify the **User Profile Memory**:

1.  **Start the Backend**: `python main.py`
2.  **Run the Verification Script**:
    ```bash
    python verify_long_term_memory.py
    ```
3.  **Expected Output**:
    - "Test 1: Standard Flow - PASSED" (Profile created and updated)
    - "Test 2: New User - PASSED" (Clean profile for new ID)
    - "Test 3: Anonymous User - PASSED" (No profile linkage)
    - "Test 4: Mixed Updates - PASSED" (Preferences tracked correctly)