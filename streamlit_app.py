"""
Streamlit Demo Application for Multi-Agent Customer Care System
A beautiful, interactive chat interface showcasing coordinated AI agents.
"""

import streamlit as st
import asyncio
import time
import json
from datetime import datetime
from typing import Dict, Any, List
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.orchestrator import orchestrator
from memory.session_memory import memory
from config import REQUEST_TIMEOUT

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Customer Care Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Global base text color - light for dark background */
    .stApp {
        color: #f8f9fa;
    }
    
    /* Target markdown elements that appear on the main dark background */
    .stApp [data-testid="stMarkdownContainer"] p,
    .stApp [data-testid="stMarkdownContainer"] h1,
    .stApp [data-testid="stMarkdownContainer"] h2,
    .stApp [data-testid="stMarkdownContainer"] h3,
    .stApp [data-testid="stMarkdownContainer"] span,
    .stApp label {
        color: #f8f9fa;
    }
    
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .agent-badge {
        display: inline-block;
        padding: 4px 12px;
        margin: 2px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        color: white !important;
    }
    
    .agent-order { background-color: #4CAF50; }
    .agent-tech { background-color: #2196F3; }
    .agent-product { background-color: #FF9800; }
    .agent-solutions { background-color: #9C27B0; }
    .agent-orchestrator { background-color: #607D8B; }
    
    /* ENHANCED: Target EVERYTHING inside light-background cards to be dark */
    /* We use highly specific selectors to override global heading styles */
    .execution-step, .memory-item, .chat-message, .agent-activity,
    .execution-step *[data-testid="stMarkdownContainer"] *,
    .memory-item *[data-testid="stMarkdownContainer"] *,
    .chat-message *[data-testid="stMarkdownContainer"] *,
    .agent-activity *[data-testid="stMarkdownContainer"] *,
    .execution-step *, .memory-item *, .chat-message *, .agent-activity * {
        color: #1A1C24 !important;
    }
    
    .execution-step {
        padding: 12px;
        margin: 8px 0;
        border-left: 5px solid #667eea;
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    
    .memory-item {
        background-color: #f0f7ff;
        padding: 10px;
        margin: 6px 0;
        border-radius: 8px;
        font-size: 14px;
        border: 1px solid #d1e9ff;
    }
    
    .chat-message {
        padding: 1.2rem;
        margin: 1rem 0;
        border-radius: 12px;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background-color: #f0f9ff;
        border: 1px solid #c2e7ff;
    }
    
    .assistant-message {
        background-color: #f7fee7;
        border: 1px solid #d9f99d;
    }
    
    .agent-activity {
        background-color: #fffaf0;
        border: 1px solid #fed7aa;
        border-radius: 12px;
        padding: 18px;
        margin: 12px 0;
    }
    
    .status-executing { 
        background-color: #ffc107; 
        animation: pulse 1.5s infinite;
    }
    
    .status-completed { background-color: #28a745; }
    .status-pending { background-color: #6c757d; }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"streamlit-{int(time.time())}"
    
    if "agent_activity" not in st.session_state:
        st.session_state.agent_activity = []
    
    if "memory_context" not in st.session_state:
        st.session_state.memory_context = {}
    
    if "execution_plan" not in st.session_state:
        st.session_state.execution_plan = None

def display_header():
    """Display the main header."""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Multi-Agent Customer Care System</h1>
        <p>Watch AI agents collaborate to solve customer problems</p>
    </div>
    """, unsafe_allow_html=True)

def get_agent_badge_html(agent_type: str, status: str = "active") -> str:
    """Generate HTML for agent badge."""
    status_class = f"status-{status}" if status != "active" else ""
    return f'<span class="agent-badge agent-{agent_type} {status_class}">🤖 {agent_type.title()}</span>'

def display_agent_activity():
    """Display current agent activity in sidebar."""
    st.sidebar.markdown("### 🔄 Agent Activity")
    
    if st.session_state.agent_activity:
        for activity in st.session_state.agent_activity[-5:]:  # Show last 5 activities
            agent = activity.get("agent", "unknown")
            status = activity.get("status", "active")
            action = activity.get("action", "Processing...")
            
            badge_html = get_agent_badge_html(agent, status)
            st.sidebar.markdown(f"{badge_html}", unsafe_allow_html=True)
            st.sidebar.caption(f"_{action}_")
            st.sidebar.markdown("---")
    else:
        st.sidebar.info("No agent activity yet. Send a message to see agents in action!")

def display_memory_context():
    """Display current memory context in sidebar."""
    st.sidebar.markdown("### 🧠 Memory Context")
    
    if st.session_state.memory_context:
        context = st.session_state.memory_context
        
        # Orders discussed
        if context.get("orders_discussed"):
            st.sidebar.markdown("**Orders Discussed:**")
            for order_id in context["orders_discussed"][-3:]:
                st.sidebar.markdown(f'<div class="memory-item">📦 Order #{order_id}</div>', 
                                  unsafe_allow_html=True)
        
        # Products discussed
        if context.get("products_discussed"):
            st.sidebar.markdown("**Products Mentioned:**")
            for product in context["products_discussed"][-3:]:
                st.sidebar.markdown(f'<div class="memory-item">💻 {product}</div>', 
                                  unsafe_allow_html=True)
        
        # Issues mentioned
        if context.get("issues_mentioned"):
            st.sidebar.markdown("**Issues Identified:**")
            for issue in context["issues_mentioned"][-3:]:
                st.sidebar.markdown(f'<div class="memory-item">⚠️ {issue}</div>', 
                                  unsafe_allow_html=True)
        
        # Conversation length
        conv_length = context.get("conversation_length", 0)
        st.sidebar.metric("Conversation Length", f"{conv_length} messages")
        
    else:
        st.sidebar.info("Memory context will appear as you chat")

def display_execution_plan():
    """Display the current execution plan."""
    if st.session_state.execution_plan:
        plan = st.session_state.execution_plan
        
        st.markdown("### 📋 Execution Plan")
        st.markdown(f"**Plan ID:** `{plan.get('plan_id', 'N/A')}`")
        st.markdown(f"**Execution Mode:** `{plan.get('execution_mode', 'unknown')}`")
        
        if plan.get("steps"):
            st.markdown("**Agent Coordination Steps:**")
            for i, step in enumerate(plan["steps"], 1):
                agent = step.get("agent", "unknown")
                status = step.get("status", "pending")
                task = step.get("task", "Processing...")
                
                badge_html = get_agent_badge_html(agent, status)
                st.markdown(f"""
                <div class="execution-step">
                    <strong>Step {i}:</strong> {badge_html}<br>
                    <em>{task}</em>
                </div>
                """, unsafe_allow_html=True)

async def process_message(user_message: str) -> Dict[str, Any]:
    """Process user message through the orchestrator."""
    
    # Clear previous agent activity
    st.session_state.agent_activity = []
    
    # Add activity tracking
    st.session_state.agent_activity.append({
        "agent": "orchestrator",
        "status": "executing",
        "action": "Analyzing request and creating plan..."
    })
    
    # Process the message
    result = await orchestrator.process_request(user_message, st.session_state.session_id)
    
    # Update memory context
    context = memory.get_context_for_agents(st.session_state.session_id)
    st.session_state.memory_context = context
    
    # Update execution plan
    if result.get("plan_executed"):
        st.session_state.execution_plan = result["plan_executed"]
        
        # Add agent activities from plan
        for step in result["plan_executed"].get("steps", []):
            st.session_state.agent_activity.append({
                "agent": step.get("agent", "unknown"),
                "status": step.get("status", "completed"),
                "action": step.get("task", "Completed task")
            })
    
    return result

def display_chat_interface():
    """Display the main chat interface."""
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display conversation history
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Assistant message with agent info
                agent_info = ""
                if message.get("agents_used"):
                    agent_badges = " ".join([
                        get_agent_badge_html(agent) 
                        for agent in message["agents_used"]
                    ])
                    agent_info = f"<br><small>Agents used: {agent_badges}</small>"
                
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>Assistant:</strong> {message["content"]}{agent_info}
                </div>
                """, unsafe_allow_html=True)
                
                # Show execution details in expander
                if message.get("plan_executed"):
                    with st.expander("🔍 View Agent Coordination Details"):
                        plan = message["plan_executed"]
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Agents Used", len(plan.get("agents_involved", [])))
                        with col2:
                            st.metric("Tools Used", len(plan.get("tools_used", [])))
                        with col3:
                            st.metric("Execution Time", f"{message.get('execution_time', 0):.1f}s")
                        
                        if plan.get("steps"):
                            st.markdown("**Execution Steps:**")
                            for step in plan["steps"]:
                                status_emoji = "✅" if step.get("status") == "completed" else "⏳"
                                st.write(f"{status_emoji} **{step.get('agent', 'Unknown')}**: {step.get('task', 'Task')}")

def display_example_questions():
    """Display example questions for easy testing."""
    st.markdown("### 💡 Try These Demo Questions")
    
    examples = [
        {
            "category": "🛒 Order Support",
            "questions": [
                "My laptop order #12345 won't turn on, I need help!",
                "I want to track my order #12346",
                "How do I return order #12345?",
                "Is my order #12345 still under warranty?"
            ]
        },
        {
            "category": "💻 Product Questions", 
            "questions": [
                "Compare TechBook Pro 15 vs TechBook Air 13",
                "What laptops do you have under $1000?",
                "I need a laptop for gaming, what do you recommend?",
                "What are the specs of the TechBook Gaming 17?"
            ]
        },
        {
            "category": "🔧 Technical Support",
            "questions": [
                "My laptop is overheating, what should I do?",
                "The WiFi on my laptop isn't working",
                "My laptop is running very slowly",
                "The screen on my laptop is flickering"
            ]
        },
        {
            "category": "🔄 Follow-up Questions",
            "questions": [
                "What other options do I have?",
                "Can you explain that in more detail?",
                "What would you recommend instead?",
                "How long will this take?"
            ]
        }
    ]
    
    for category in examples:
        with st.expander(category["category"]):
            for question in category["questions"]:
                if st.button(question, key=f"btn_{hash(question)}"):
                    st.session_state.selected_question = question
                    st.rerun()

def main():
    """Main Streamlit application."""
    
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Right sidebar content
    with st.sidebar:
        st.markdown("### 🎯 System Status")
        # Session info
        st.info(f"**Session:** `{st.session_state.session_id}`")
        # Display agent activity
        display_agent_activity()
        # Display memory context  
        display_memory_context()
        # Reset conversation button
        if st.button("🔄 Reset Conversation", key="reset_conv_btn", type="secondary"):
            st.session_state.messages = []
            st.session_state.agent_activity = []
            st.session_state.memory_context = {}
            st.session_state.execution_plan = None
            memory.clear_session(st.session_state.session_id)
            st.success("Conversation reset!")
            st.rerun()
    
    # Main area
    st.markdown("### 💬 Chat with Multi-Agent System")
    
    # Display chat interface
    display_chat_interface()
    
    # Handle selected question from examples
    if hasattr(st.session_state, 'selected_question'):
        user_message = st.session_state.selected_question
        delattr(st.session_state, 'selected_question')
    else:
        # Chat input
        user_message = st.chat_input("Ask me anything about orders, products, or technical support...")
    
    if user_message:
        # Add user message
        st.session_state.messages.append({
            "role": "user", 
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Show processing indicator
        with st.spinner("🤖 Agents are working on your request..."):
            # Process message
            try:
                result = asyncio.run(process_message(user_message))
                
                # Add assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result.get("response", "I apologize, but I encountered an issue processing your request."),
                    "agents_used": result.get("plan_executed", {}).get("agents_involved", []),
                    "plan_executed": result.get("plan_executed", {}),
                    "execution_time": result.get("execution_time", 0),
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                st.error(f"Error processing request: {str(e)}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "I apologize, but I encountered a technical issue. Please try again.",
                    "timestamp": datetime.now().isoformat()
                })
        
        # Rerun to update the display
        st.rerun()
    
    # Display example questions at the bottom
    st.markdown("---")
    display_example_questions()
    
    # Display execution plan if available
    if st.session_state.execution_plan:
        with st.expander("📋 Latest Execution Plan", expanded=False):
            display_execution_plan()

if __name__ == "__main__":
    main()