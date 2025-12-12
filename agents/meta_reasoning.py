"""Meta-reasoning module for self-reflection and execution review."""

import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class ReviewResult(BaseModel):
    """Result of a meta-reasoning review."""
    is_valid: bool = Field(..., description="Whether the execution results are valid and complete")
    issues: List[str] = Field(default_factory=list, description="List of issues found if any")
    suggested_action: Optional[str] = Field(None, description="Suggested action to resolve issues")
    missing_intent: Optional[str] = Field(None, description="Description of any user intent that was missed")
    contradictions: List[str] = Field(default_factory=list, description="List of contradictions found between agents")

class MetaReasoning:
    """
    Meta-reasoning layer that reviews agent execution results.
    
    This class performs a self-reflective pass to:
    1. Detect contradictions between different agents
    2. Ensure the user's full intent has been addressed
    3. Suggest remedial actions if issues are found
    """
    
    def __init__(self, agent_instance):
        """
        Initialize with a reference to the parent agent (usually Orchestrator).
        
        Args:
            agent_instance: The agent instance (must have generate_response method)
        """
        self.agent = agent_instance
    
    async def review_execution(self, user_message: str, agent_results: List[Dict[str, Any]], 
                             context: Dict[str, Any]) -> ReviewResult:
        """
        Review the execution results against the user message.
        
        Args:
            user_message: The original user request
            agent_results: List of results from agent execution
            context: Execution context
            
        Returns:
            ReviewResult object containing validation status and issues
        """
        try:
            # Prepare review context
            review_context = {
                "user_request": user_message,
                "agent_results": [
                    {
                        "agent": result.get("agent_used", "unknown"),
                        "response": result.get("response", ""),
                        "tools_used": result.get("tools_used", [])
                    }
                    for result in agent_results if result.get("response")
                ]
            }
            
            # Generate review
            prompt = self._create_review_prompt(review_context)
            response = await self.agent.generate_response(
                prompt,
                {**context, "review_context": review_context}
            )
            
            # Parse response into ReviewResult
            # Note: Since the base agent returns a dict/text, we parse it manually
            # In a production system with structured output support, this would be cleaner
            raw_response = response["response"]
            
            return self._parse_review_response(raw_response)
            
        except Exception as e:
            logger.error(f"Error in meta-reasoning review: {e}")
            # Fail safe: assume valid if review fails
            return ReviewResult(is_valid=True, issues=[f"Review failed: {e}"])
    
    def _create_review_prompt(self, context: Dict[str, Any]) -> str:
        """Create the prompt for the review task."""
        prompt = f"""
        Meta-Reasoning Review Task
        
        Original User Request: "{context['user_request']}"
        
        Agent Execution Results:
        """
        
        for i, result in enumerate(context['agent_results'], 1):
            prompt += f"{i}. Agent {result['agent']}: {result['response']}\n"
            
        prompt += """
        Analyze the above execution results for:
        1. CONTRADICTIONS: Do any agents provide conflicting information? (e.g., one says order is shipped, another says cancelled)
        2. MISSING INTENT: Did the agents miss any part of the user's request? (e.g., user asked for refund AND tech support, but only got tech support)
        3. ERROR STATES: Did any agent return an error or fail to help?
        
        Format your response exactly as follows:
        VALID: [TRUE/FALSE]
        ISSUES: [List specific issues or "None"]
        CONTRADICTIONS: [List specific contradictions or "None"]
        MISSING_INTENT: [Describe what is missing or "None"]
        SUGGESTED_ACTION: [Describe what should be done next to fix it, e.g., "Call Solutions Agent" or "None"]
        """
        
        return prompt
    
    def _parse_review_response(self, response_text: str) -> ReviewResult:
        """Parse the text response into a ReviewResult object."""
        try:
            lines = response_text.strip().split('\n')
            data = {
                "is_valid": True,
                "issues": [],
                "contradictions": [],
                "missing_intent": None,
                "suggested_action": None
            }
            
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if line.upper().startswith("VALID:"):
                    is_valid_str = line.split(":", 1)[1].strip().upper()
                    data["is_valid"] = "TRUE" in is_valid_str
                elif line.upper().startswith("ISSUES:"):
                    content = line.split(":", 1)[1].strip()
                    if content and content.lower() != "none":
                        data["issues"].append(content)
                    current_section = "issues"
                elif line.upper().startswith("CONTRADICTIONS:"):
                    content = line.split(":", 1)[1].strip()
                    if content and content.lower() != "none":
                        data["contradictions"].append(content)
                    current_section = "contradictions"
                elif line.upper().startswith("MISSING_INTENT:"):
                    content = line.split(":", 1)[1].strip()
                    if content and content.lower() != "none":
                        data["missing_intent"] = content
                    current_section = "missing_intent"
                elif line.upper().startswith("SUGGESTED_ACTION:"):
                    content = line.split(":", 1)[1].strip()
                    if content and content.lower() != "none":
                        data["suggested_action"] = content
                    current_section = "suggested_action"
                else:
                    # Append continuation lines to current section
                    if current_section == "issues":
                        data["issues"].append(line)
                    elif current_section == "contradictions":
                        data["contradictions"].append(line)
                    elif current_section == "missing_intent" and data["missing_intent"]:
                        data["missing_intent"] += " " + line
            
            # Post-process lists to remove empty/None entries
            data["issues"] = [i for i in data["issues"] if i and i.lower() != "none"]
            data["contradictions"] = [c for c in data["contradictions"] if c and c.lower() != "none"]
            
            # If explicit False was not found but issues exist, mark as invalid
            if data["is_valid"] and (data["issues"] or data["contradictions"] or data["missing_intent"]):
                data["is_valid"] = False
                
            return ReviewResult(**data)
            
        except Exception as e:
            logger.error(f"Error parsing review response: {e}")
            # Fallback to valid to prevent system blockage, but log error
            return ReviewResult(is_valid=True, issues=[f"Parse error: {str(e)}"])
