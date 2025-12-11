"""
User Profile Memory Management.
Tracks long-term user preferences, issues, and sentiment history.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class MemoryFact:
    """Represents a discrete piece of information with confidence."""
    value: Any
    confidence: float = 1.0  # 0.0 to 1.0
    last_confirmed: str = field(default_factory=lambda: datetime.now().isoformat())
    count: int = 1
    
    def decay(self, days: float, decay_rate: float = 0.1) -> float:
        """Apply decay based on time passed."""
        new_conf = self.confidence - (days * decay_rate)
        return max(0.0, new_conf)

@dataclass
class UserProfile:
    """Represents a user's long-term profile."""
    user_id: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_interaction: str = field(default_factory=lambda: datetime.now().isoformat())
    # Storing facts: key -> MemoryFact
    product_preferences: Dict[str, MemoryFact] = field(default_factory=dict)
    issue_history: Dict[str, MemoryFact] = field(default_factory=dict)
    interaction_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "created_at": self.created_at,
            "last_interaction": self.last_interaction,
            "product_preferences": {k: v.value for k, v in self.product_preferences.items()}, # Simplified for view
            "product_preferences_details": {k: vars(v) for k, v in self.product_preferences.items()},
            "issue_history": {k: v.value for k, v in self.issue_history.items()},
            "issue_history_details": {k: vars(v) for k, v in self.issue_history.items()},
            "interaction_count": self.interaction_count
        }
        
    def get_active_facts(self, threshold: float = 0.3) -> Dict[str, Any]:
        """Retrieve facts that meet the confidence threshold after decay."""
        active_products = []
        now = datetime.fromisoformat(datetime.now().isoformat())
        
        for key, fact in self.product_preferences.items():
            last = datetime.fromisoformat(fact.last_confirmed)
            days = (now - last).total_seconds() / 86400
            current_conf = fact.decay(days)
            if current_conf >= threshold:
                active_products.append(fact.value)
                
        active_issues = []
        for key, fact in self.issue_history.items():
            last = datetime.fromisoformat(fact.last_confirmed)
            days = (now - last).total_seconds() / 86400
            current_conf = fact.decay(days)
            if current_conf >= threshold:
                active_issues.append(fact.value)
                
        return {
            "products": active_products,
            "issues": active_issues
        }

class UserProfileMemory:
    """Manages persistent user profiles."""
    
    def __init__(self):
        # In-memory storage for demo purposes (would be a DB in prod)
        self.profiles: Dict[str, UserProfile] = {}
        
    def get_profile(self, user_id: str) -> UserProfile:
        """Get existing profile or create new one."""
        if user_id not in self.profiles:
            logger.info(f"Creating new profile for user {user_id}")
            self.profiles[user_id] = UserProfile(user_id=user_id)
        return self.profiles[user_id]
    
    def update_profile(self, user_id: str, updates: Dict[str, Any]) -> None:
        """
        Update a user's profile with new interaction data.
        updates format: {
            "products": [{"value": "name", "confidence": 0.8}, ...], 
            "issues": [{"value": "issue", "confidence": 0.8}, ...]
        }
        """
        if not user_id:
            return
            
        profile = self.get_profile(user_id)
        profile.last_interaction = datetime.now().isoformat()
        profile.interaction_count += 1
        
        # Update preferences
        if "products" in updates:
            for item in updates["products"]:
                val = item["value"]
                conf = item.get("confidence", 1.0)
                
                if val in profile.product_preferences:
                    # Reinforce
                    fact = profile.product_preferences[val]
                    fact.count += 1
                    fact.last_confirmed = datetime.now().isoformat()
                    # Boost confidence (bounded at 1.0)
                    fact.confidence = min(1.0, fact.confidence + (conf * 0.2)) 
                else:
                    # Create new
                    profile.product_preferences[val] = MemoryFact(value=val, confidence=conf)
        
        # Update issue history
        if "issues" in updates:
            for item in updates["issues"]:
                val = item["value"]
                conf = item.get("confidence", 1.0)
                
                if val in profile.issue_history:
                    # Reinforce
                    fact = profile.issue_history[val]
                    fact.count += 1
                    fact.last_confirmed = datetime.now().isoformat()
                    fact.confidence = min(1.0, fact.confidence + (conf * 0.2))
                else:
                    # Create new
                    profile.issue_history[val] = MemoryFact(value=val, confidence=conf)
                
        logger.info(f"Updated profile for {user_id}")

# Global instance
user_profiles = UserProfileMemory()
