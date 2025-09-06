"""
Message handling utilities
"""

from datetime import datetime
from typing import Dict, Any, List
import streamlit as st

class MessageHandler:
    """Handles message processing and formatting"""
    
    @staticmethod
    def create_message(role: str, content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a formatted message object"""
        
        return {
            "role": role,
            "content": content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "metadata": metadata or {}
        }
    
    @staticmethod
    def format_response(response: Dict[str, Any]) -> str:
        """Format API response for display"""
        
        content = response.get("response", "No response received.")
        
        # Add formatting based on response type
        if response.get("error"):
            return f"⚠️ **Error**: {content}"
        
        # Add confidence indicator if available
        metadata = response.get("metadata", {})
        confidence = metadata.get("confidence")
        
        if confidence and confidence < 0.7:
            content = f"🤔 {content}

*Note: I'm not entirely sure about this answer. You might want to verify with our support team.*"
        
        return content
    
    @staticmethod
    def extract_intent(message_text: str) -> str:
        """Extract intent from message text (simple keyword matching)"""
        
        message_lower = message_text.lower()
        
        billing_keywords = ["billing", "payment", "subscription", "invoice", "price", "cost", "refund", "cancel"]
        technical_keywords = ["technical", "bug", "error", "problem", "issue", "troubleshoot", "api", "integration"]
        
        if any(keyword in message_lower for keyword in billing_keywords):
            return "billing"
        elif any(keyword in message_lower for keyword in technical_keywords):
            return "technical"
        else:
            return "general"
    
    @staticmethod
    def get_message_stats(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about messages"""
        
        if not messages:
            return {"total": 0, "user": 0, "assistant": 0, "avg_length": 0}
        
        user_messages = [msg for msg in messages if msg.get("role") == "user"]
        assistant_messages = [msg for msg in messages if msg.get("role") == "assistant"]
        
        total_length = sum(len(msg.get("content", "")) for msg in messages)
        avg_length = total_length / len(messages) if messages else 0
        
        return {
            "total": len(messages),
            "user": len(user_messages),
            "assistant": len(assistant_messages),
            "avg_length": avg_length
        }
    
    @staticmethod
    def export_conversation(messages: List[Dict[str, Any]]) -> str:
        """Export conversation to text format"""
        
        if not messages:
            return "No conversation to export."
        
        lines = ["IntelliSupport Conversation Export", "=" * 40, ""]
        
        for i, msg in enumerate(messages, 1):
            role = msg.get("role", "unknown").capitalize()
            content = msg.get("content", "")
            timestamp = msg.get("timestamp", "")
            
            lines.append(f"{i}. {role} ({timestamp}):")
            lines.append(content)
            lines.append("")
        
        lines.extend(["", "=" * 40, f"Total messages: {len(messages)}"])
        
        return "\n".join(lines)
