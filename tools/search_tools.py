"""Search tools using Google Gemini API for web search capabilities."""

import asyncio
import aiohttp
import logging
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)

class SearchTools:
    """Tools for web search using Gemini API."""
    
    def __init__(self):
        if GEMINI_API_KEY:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
            self.model_id = GEMINI_MODEL
            print(f"Gemini client initialized: {self.client}")
        else:
            logger.warning("Gemini API key not configured - search will use mock responses")
            self.client = None
    
    async def search_web(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search the web for current information."""
        if not self.client:
            return self._mock_web_search(query)
        
        try:
            # Use Gemini to search and summarize web information
            search_prompt = f"""
            Search for current information about: {query}
            
            Please provide relevant, up-to-date information in a structured format.
            Focus on factual, helpful information that would be useful for customer service.
            
            Format your response as a summary of key points.
            """
            
            # Fix: Ensure tool_choice is auto if we were to use tools, 
            # and use the new SDK generate_content method.
            config = types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                tool_config=types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(
                        mode='AUTO'
                    )
                )
            )

            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_id,
                contents=search_prompt,
                config=config
            )
            
            return [{
                "title": "Web Search Results",
                "content": response.text,
                "source": "Gemini AI Search",
                "relevance": 0.9
            }]
            
        except Exception as e:
            logger.error(f"Web search failed: {e}")
            return self._mock_web_search(query)
    
    async def find_deals(self, product_type: str) -> List[Dict[str, Any]]:
        """Search for current deals on specific product types."""
        if not self.client:
            return self._mock_deals_search(product_type)
        
        try:
            deals_prompt = f"""
            Find current deals and promotions for {product_type}.
            Look for:
            - Price comparisons
            - Current promotions
            - Seasonal sales
            - Bundle offers
            
            Provide practical information that would help a customer make a purchasing decision.
            """
            
            config = types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                tool_config=types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(
                        mode='AUTO'
                    )
                )
            )

            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_id,
                contents=deals_prompt,
                config=config
            )
            
            return [{
                "title": f"Current Deals for {product_type}",
                "content": response.text,
                "source": "Gemini AI Search",
                "deal_type": "general"
            }]
            
        except Exception as e:
            logger.error(f"Deals search failed: {e}")
            return self._mock_deals_search(product_type)
    
    async def search_competitors(self, product: str) -> List[Dict[str, Any]]:
        """Search for competitor information and alternatives."""
        if not self.client:
            return self._mock_competitor_search(product)
        
        try:
            competitor_prompt = f"""
            Find information about alternatives and competitors for {product}.
            Include:
            - Similar products from other brands
            - Price comparisons
            - Feature comparisons
            - Customer reviews and ratings
            
            Focus on helping customers understand their options.
            """
            
            config = types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                tool_config=types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(
                        mode='AUTO'
                    )
                )
            )

            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_id,
                contents=competitor_prompt,
                config=config
            )
            
            return [{
                "title": f"Alternatives to {product}",
                "content": response.text,
                "source": "Gemini AI Search",
                "comparison_type": "competitive_analysis"
            }]
            
        except Exception as e:
            logger.error(f"Competitor search failed: {e}")
            return self._mock_competitor_search(product)
    
    def _mock_web_search(self, query: str) -> List[Dict[str, Any]]:
        """Mock web search results when API is not available."""
        mock_results = {
            "laptop repair": [
                {
                    "title": "Common Laptop Issues and Solutions",
                    "content": "Power issues are often related to battery or adapter problems. Try different power sources first.",
                    "source": "TechSupport.com",
                    "relevance": 0.8
                }
            ],
            "techbook reviews": [
                {
                    "title": "TechBook Product Reviews",
                    "content": "TechBook laptops are known for reliability and performance. Pro series rated highly for business use.",
                    "source": "LaptopReviews.com",
                    "relevance": 0.9
                }
            ]
        }
        
        # Find matching mock results
        for key, results in mock_results.items():
            if key.lower() in query.lower():
                return results
        
        return [{
            "title": "General Search Results",
            "content": f"Search results for '{query}' - comprehensive information available online.",
            "source": "Mock Search",
            "relevance": 0.5
        }]
    
    def _mock_deals_search(self, product_type: str) -> List[Dict[str, Any]]:
        """Mock deals search when API is not available."""
        return [
            {
                "title": f"Current {product_type} Deals",
                "content": f"Winter sale: 15% off select {product_type} models. Free shipping on orders over $500. Extended warranty available.",
                "source": "Mock Deals",
                "deal_type": "seasonal"
            }
        ]
    
    def _mock_competitor_search(self, product: str) -> List[Dict[str, Any]]:
        """Mock competitor search when API is not available."""
        return [
            {
                "title": f"Alternatives to {product}",
                "content": f"Similar products include various brands with comparable specs. Price range varies from budget to premium options.",
                "source": "Mock Comparison",
                "comparison_type": "competitive_analysis"
            }
        ]

# Global search tools instance
search_tools = SearchTools()