"""
API client for communicating with the backend
"""

import requests
import streamlit as st
from typing import Dict, Any
from utils.config import get_api_config

class APIClient:
    """Client for IntelliSupport backend API"""
    
    @staticmethod
    def send_message(message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send message to the backend API"""
        
        config = get_api_config()
        base_url = config.get("base_url", "http://localhost:8000")
        timeout = config.get("timeout", 30)
        
        try:
            # Prepare request data
            data = {
                "message": message,
                "context": context or {},
                "model": st.session_state.get("selected_model", "groq/llama-3.1-70b-versatile"),
                "conversation_id": st.session_state.get("conversation_id"),
                "session_id": st.session_state.get("session_id", "default")
            }
            
            # Make API request
            response = requests.post(
                f"{base_url}/api/chat",
                json=data,
                timeout=timeout,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Update conversation ID if provided
                if result.get("conversation_id"):
                    st.session_state.conversation_id = result["conversation_id"]
                
                return result
            else:
                return {
                    "response": f"API Error: {response.status_code} - {response.text}",
                    "error": True,
                    "metadata": {"status_code": response.status_code}
                }
        
        except requests.exceptions.ConnectionError:
            return APIClient._get_mock_response(message)
        except requests.exceptions.Timeout:
            return {
                "response": "Request timed out. Please try again.",
                "error": True,
                "metadata": {"error_type": "timeout"}
            }
        except Exception as e:
            return {
                "response": f"Unexpected error: {str(e)}",
                "error": True,
                "metadata": {"error_type": "unexpected", "error_message": str(e)}
            }
    
    @staticmethod
    def _get_mock_response(message: str) -> Dict[str, Any]:
        """Generate a mock response when backend is not available"""
        
        import time
        import random
        
        # Simulate processing time
        time.sleep(random.uniform(0.5, 1.5))
        
        mock_responses = {
            "billing": "For billing inquiries, our current plans are: Basic ($99/month), Pro ($199/month), and Enterprise (custom pricing). How can I help you with your billing needs?",
            "technical": "I'd be happy to help with technical issues. Can you please describe the specific problem you're experiencing? Include any error messages if available.",
            "general": "Thank you for contacting IntelliSupport! I'm here to help with any questions about our products and services. What would you like to know?",
            "default": "I understand you're asking about: '{message}'. While I don't have access to the backend right now, I'm designed to help with billing, technical support, and general inquiries. Could you provide more details about what you need help with?"
        }
        
        # Simple keyword matching for mock responses
        message_lower = message.lower()
        if any(word in message_lower for word in ["billing", "payment", "subscription", "invoice", "price"]):
            response_type = "billing"
        elif any(word in message_lower for word in ["technical", "bug", "error", "problem", "issue", "troubleshoot"]):
            response_type = "technical"
        elif any(word in message_lower for word in ["hello", "hi", "help", "start", "welcome"]):
            response_type = "general"
        else:
            response_type = "default"
        
        response_text = mock_responses[response_type]
        if response_type == "default":
            response_text = response_text.format(message=message)
        
        return {
            "response": f"🔄 **Demo Mode Active** (Backend not connected)

{response_text}",
            "metadata": {
                "mock": True,
                "response_type": response_type,
                "intent": response_type,
                "confidence": random.uniform(0.7, 0.95),
                "model_used": "mock",
                "processing_time": random.uniform(0.5, 1.5)
            }
        }
    
    @staticmethod
    def health_check() -> bool:
        """Check if the backend API is available"""
        
        config = get_api_config()
        base_url = config.get("base_url", "http://localhost:8000")
        
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
