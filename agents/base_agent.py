"""Base agent class for all specialized agents."""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, AGENT_CONFIGS

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all customer service agents."""
    
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.config = AGENT_CONFIGS.get(agent_type, AGENT_CONFIGS["orchestrator"])
        
        if GROQ_API_KEY:
            self.client = ChatGroq(
                api_key=GROQ_API_KEY,
                model_name=self.config["model"],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"]
            )
        else:
            logger.warning(f"Groq API key not configured - {agent_type} agent will use mock responses")
            self.client = None
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent."""
        pass
    
    @abstractmethod
    async def process_request(self, user_message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a user request and return response."""
        pass
    
    async def generate_response(self, user_message: str, context: Dict[str, Any], 
                             tools_used: List[str] = None) -> Dict[str, Any]:
        """Generate AI response using Groq API."""
        if not self.client:
            return await self._generate_mock_response(user_message, context)
        
        try:
            # Prepare conversation history in LangChain format
            messages = [
                ("system", self.get_system_prompt()),
            ]
            
            # Add recent conversation history if available
            if context.get("recent_conversation"):
                for msg in context["recent_conversation"][-3:]:  # Last 3 messages
                    messages.append((msg["role"], msg["content"]))
            
            # Add current user message
            messages.append(("user", self._format_user_message(user_message, context)))
            
            # Add format instruction
            format_instruction = """
            IMPORTANT: You must format your response as a JSON object with the following structure:
            {
                "response": "Your natural language response here",
                "confidence": <float between 0.0 and 1.0>,
                "evidence": ["list", "of", "sources", "used", "e.g. order_db, policy_doc, previous_chat"]
            }
            """
            messages.append(("system", format_instruction))

            # Generate response
            response = await self.client.ainvoke(messages)
            
            # Parse JSON response
            import json
            import re
            
            content = response.content
            parsed_result = {}
            
            try:
                # cleaner parsing logic
                content = content.strip()
                if content.startswith("```json"):
                    content = content.split("```json")[1]
                if content.endswith("```"):
                    content = content.rsplit("```", 1)[0]
                
                parsed_result = json.loads(content)
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON response from {self.agent_type}, falling back to text")
                parsed_result = {
                    "response": response.content,
                    "confidence": self._estimate_confidence(response.content),
                    "evidence": []
                }
            
            return {
                "response": parsed_result.get("response", ""),
                "agent_type": self.agent_type,
                "tools_used": tools_used or [],
                "confidence": parsed_result.get("confidence", 0.5),
                "evidence": parsed_result.get("evidence", []),
                "thinking_process": f"Analyzed request using {self.agent_type} expertise and provided structured response"
            }
            
        except Exception as e:
            logger.error(f"Error generating response for {self.agent_type}: {e}")
            return await self._generate_mock_response(user_message, context)
    
    def _format_user_message(self, user_message: str, context: Dict[str, Any]) -> str:
        """Format user message with context for the AI."""
        formatted_message = f"Customer Message: {user_message}\n\n"
        
        # Add relevant context
        if context.get("customer_context"):
            formatted_message += f"Customer Context: {context['customer_context']}\n\n"
        
        if context.get("orders_discussed"):
            formatted_message += f"Orders Previously Discussed: {', '.join(context['orders_discussed'])}\n\n"
        
        if context.get("issues_mentioned"):
            formatted_message += f"Issues Previously Mentioned: {', '.join(context['issues_mentioned'])}\n\n"
        
        return formatted_message
    
    def _estimate_confidence(self, response: str) -> float:
        """Estimate confidence level based on response characteristics."""
        # Simple heuristic - longer, more detailed responses tend to be more confident
        if len(response) > 200 and ("specific" in response.lower() or "recommend" in response.lower()):
            return 0.9
        elif len(response) > 100:
            return 0.7
        else:
            return 0.5
    
    async def _generate_mock_response(self, user_message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock response when OpenAI API is not available."""
        mock_responses = {
            "order": "I've located your order information and can help with any questions about status, tracking, or modifications.",
            "tech_support": "I can help troubleshoot your technical issue. Let me provide some steps to resolve this problem.",
            "product": "I can provide detailed product information and help you compare different options to find the best fit.",
            "solutions": "I understand you need assistance with a return or exchange. Let me help you with the best solution for your situation."
        }
        
        return {
            "response": mock_responses.get(self.agent_type, "I'm here to help with your request."),
            "agent_type": self.agent_type,
            "tools_used": [],
            "confidence": 0.6,
            "evidence": ["mock_data"],
            "thinking_process": f"Generated mock response using {self.agent_type} agent (API not configured)"
        }
    
    def format_final_response(self, agent_response: Dict[str, Any], 
                            tool_results: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format the final response with tool results."""
        return {
            "response": agent_response["response"],
            "agent_used": self.agent_type,
            "tools_used": agent_response.get("tools_used", []),
            "tool_results": tool_results or [],
            "confidence": agent_response.get("confidence", 0.5),
            "evidence": agent_response.get("evidence", []),
            "thinking_process": agent_response.get("thinking_process", "")
        }