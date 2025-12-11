"""Session memory management for conversation context."""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import json
from .user_profile_memory import user_profiles  # Import global instance

@dataclass
class Message:
    """Represents a single message in the conversation."""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime
    agent_used: Optional[str] = None
    tools_used: List[str] = field(default_factory=list)
    plan_executed: Optional[Dict[str, Any]] = None

@dataclass
class Session:
    """Represents a conversation session."""
    session_id: str
    user_id: Optional[str] # Link to long-term profile
    created_at: datetime
    last_activity: datetime
    messages: List[Message] = field(default_factory=list)
    customer_context: Dict[str, Any] = field(default_factory=dict)
    preferences: Dict[str, Any] = field(default_factory=dict)
    issues_mentioned: List[str] = field(default_factory=list)
    orders_discussed: List[str] = field(default_factory=list)
    orders_discussed: List[str] = field(default_factory=list)
    products_discussed: List[str] = field(default_factory=list)
    products_discussed: List[str] = field(default_factory=list)
    agent_performance: Dict[str, Dict[str, int]] = field(default_factory=lambda: {})  # {agent_name: {"success": 0, "failure": 0}}
    intent_history: List[str] = field(default_factory=list)

class SessionMemory:
    """Manages conversation sessions and context."""
    
    def __init__(self, session_timeout: int = 3600):
        self.sessions: Dict[str, Session] = {}
        self.session_timeout = session_timeout
    
    def create_session(self, session_id: Optional[str] = None) -> str:
        """Create a new session and return its ID."""
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        session = Session(
            session_id=session_id,
            user_id=None, # Default to anonymous
            created_at=datetime.now(),
            last_activity=datetime.now()
        )
        
        self.sessions[session_id] = session
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID if it exists and is not expired."""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Check if session has expired
        if datetime.now() - session.last_activity > timedelta(seconds=self.session_timeout):
            del self.sessions[session_id]
            return None
        
        return session
    
    def get_or_create_session(self, session_id: Optional[str] = None, user_id: Optional[str] = None) -> tuple[str, Session]:
        """Get existing session or create new one."""
        if session_id:
            session = self.get_session(session_id)
            if session:
                # Update user_id if provided and not set
                if user_id and not session.user_id:
                    session.user_id = user_id
                return session_id, session
        
        # Create new session
        new_session_id = self.create_session(session_id)
        session = self.sessions[new_session_id]
        if user_id:
            session.user_id = user_id
        return new_session_id, session
    
    def add_message(self, session_id: str, role: str, content: str, 
                   agent_used: Optional[str] = None, tools_used: List[str] = None,
                   plan_executed: Optional[Dict[str, Any]] = None) -> None:
        """Add a message to the session."""
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found or expired")
        
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now(),
            agent_used=agent_used,
            tools_used=tools_used or [],
            plan_executed=plan_executed
        )
        
        session.messages.append(message)
        session.last_activity = datetime.now()
        
        # Update context based on message content
        self._update_context(session, content)
    
    def get_conversation_history(self, session_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get conversation history for a session."""
        session = self.get_session(session_id)
        if not session:
            return []
        
        messages = session.messages
        if limit:
            messages = messages[-limit:]
        
        return [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "agent_used": msg.agent_used,
                "tools_used": msg.tools_used,
                "plan_executed": msg.plan_executed
            }
            for msg in messages
        ]
    
    def get_context_for_agents(self, session_id: str) -> Dict[str, Any]:
        """Get relevant context for agents to use."""
        session = self.get_session(session_id)
        if not session:
            return {}
        
        # Get recent conversation for context
        recent_messages = session.messages[-5:] if len(session.messages) > 5 else session.messages
        
        return {
            "session_id": session_id,
            "customer_context": session.customer_context,
            "preferences": session.preferences,
            "issues_mentioned": session.issues_mentioned,
            "orders_discussed": session.orders_discussed,
            "orders_discussed": session.orders_discussed,
            "products_discussed": session.products_discussed,
            "products_discussed": session.products_discussed,
            "intent_history": session.intent_history,
            "user_profile": user_profiles.get_profile(session.user_id).to_dict() if session.user_id else None,
            "recent_conversation": [
                {"role": msg.role, "content": msg.content}
                for msg in recent_messages
            ],
            "conversation_length": len(session.messages)
        }
    
    def update_customer_context(self, session_id: str, context_updates: Dict[str, Any]) -> None:
        """Update customer context information."""
        session = self.get_session(session_id)
        if session:
            session.customer_context.update(context_updates)
            session.last_activity = datetime.now()
    
    def clear_session(self, session_id: str) -> bool:
        """Clear a specific session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def clear_all_sessions(self) -> None:
        """Clear all sessions."""
        self.sessions.clear()
    
    def get_all_session_ids(self) -> List[str]:
        """Get all active session IDs."""
        current_time = datetime.now()
        active_sessions = []
        
        for session_id, session in list(self.sessions.items()):
            if current_time - session.last_activity <= timedelta(seconds=self.session_timeout):
                active_sessions.append(session_id)
            else:
                # Clean up expired session
                del self.sessions[session_id]
        
        return active_sessions
    
    def _update_context(self, session: Session, content: str) -> None:
        """Update session context based on message content."""
        content_lower = content.lower()
        
        # Extract order numbers
        import re
        order_pattern = r'order\s*#?(\d+)'
        order_matches = re.findall(order_pattern, content_lower)
        for order_id in order_matches:
            if order_id not in session.orders_discussed:
                session.orders_discussed.append(order_id)
        
        # Extract common issues
        issues = [
            "won't turn on", "not turning on", "overheating", "slow", "wifi", 
            "screen", "display", "battery", "charging", "keyboard", "trackpad"
        ]
        new_issues = []
        for issue in issues:
            if issue in content_lower and issue not in session.issues_mentioned:
                session.issues_mentioned.append(issue)
                new_issues.append(issue)
        
        # Extract product mentions
        new_products = []
        products = ["techbook", "techpad", "watch pro", "earbuds"]
        for product in products:
            if product in content_lower and product not in session.products_discussed:
                session.products_discussed.append(product)
                new_products.append(product)
                
        # Update Long-Term Profile
        if session.user_id:
             updates = {}
             if new_products:
                 updates["products"] = new_products
             if new_issues:
                 updates["issues"] = new_issues
             
             if updates:
                 user_profiles.update_profile(session.user_id, updates)
    
    def record_agent_success(self, session_id: str, agent_name: str, success: bool = True) -> None:
        """Record success or failure for an agent."""
        session = self.get_session(session_id)
        if not session:
            return
            
        if agent_name not in session.agent_performance:
            session.agent_performance[agent_name] = {"success": 0, "failure": 0}
            
        key = "success" if success else "failure"
        session.agent_performance[agent_name][key] += 1
        
    def get_agent_success_rate(self, session_id: str, agent_name: str) -> float:
        """Get success rate for an agent (0.0 to 1.0). Returns 0.5 if no history."""
        session = self.get_session(session_id)
        if not session or agent_name not in session.agent_performance:
            return 0.5
            
        stats = session.agent_performance[agent_name]
        total = stats["success"] + stats["failure"]
        
        if total == 0:
            return 0.5
            
        return stats["success"] / total
        
    def add_intent(self, session_id: str, intent: str) -> None:
        """Record the primary intent (agent type) for the current turn."""
        session = self.get_session(session_id)
        if session:
            session.intent_history.append(intent)

# Global memory instance
memory = SessionMemory()