"""
Main chat interface component
"""

import streamlit as st
import time
from datetime import datetime
import requests
import json
from utils.api_client import APIClient
from utils.message_handler import MessageHandler

class ChatInterface:
    @staticmethod
    def render():
        """Render the main chat interface"""
        
        st.header("💬 Chat with IntelliSupport")
        
        # Chat container
        chat_container = st.container()
        
        with chat_container:
            # Display chat messages
            ChatInterface._display_messages()
            
            # Chat input
            ChatInterface._render_chat_input()
            
            # Debug information
            if st.session_state.get("show_debug", False):
                ChatInterface._render_debug_info()
    
    @staticmethod
    def _display_messages():
        """Display all chat messages"""
        
        if not st.session_state.messages:
            # Welcome message
            st.info("""
            👋 **Welcome to IntelliSupport!**
            
            I'm your intelligent customer support assistant. I can help you with:
            - ❓ General questions about our products and services
            - 💳 Billing and subscription inquiries
            - 🛠️ Technical support and troubleshooting
            - 📝 Account management
            
            Just type your question below to get started!
            """)
        else:
            # Display conversation
            for message in st.session_state.messages:
                ChatInterface._render_message(message)
    
    @staticmethod
    def _render_message(message):
        """Render a single message"""
        
        role = message.get("role", "user")
        content = message.get("content", "")
        timestamp = message.get("timestamp", "")
        metadata = message.get("metadata", {})
        
        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.write(content)
                if timestamp:
                    st.caption(f"*{timestamp}*")
        
        elif role == "assistant":
            with st.chat_message("assistant", avatar="🤖"):
                st.write(content)
                
                # Show metadata if available
                if metadata and st.session_state.get("show_debug", False):
                    with st.expander("Debug Info", expanded=False):
                        st.json(metadata)
                
                if timestamp:
                    st.caption(f"*{timestamp}*")
        
        elif role == "system":
            st.info(f"ℹ️ {content}")
    
    @staticmethod
    def _render_chat_input():
        """Render the chat input area"""
        
        # Chat input
        user_input = st.chat_input("Type your message here...")
        
        if user_input:
            ChatInterface._handle_user_message(user_input)
    
    @staticmethod
    def _handle_user_message(user_input):
        """Handle user message submission"""
        
        # Add user message
        user_message = {
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.messages.append(user_message)
        
        # Show user message
        with st.chat_message("user", avatar="👤"):
            st.write(user_input)
        
        # Get AI response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                try:
                    response = APIClient.send_message(user_input)
                    
                    # Add assistant message
                    assistant_message = {
                        "role": "assistant",
                        "content": response.get("response", "I'm sorry, I couldn't process your request."),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "metadata": response.get("metadata", {})
                    }
                    st.session_state.messages.append(assistant_message)
                    
                    # Display response
                    st.write(assistant_message["content"])
                    
                    # Show debug info if enabled
                    if st.session_state.get("show_debug", False) and assistant_message.get("metadata"):
                        with st.expander("Debug Info", expanded=False):
                            st.json(assistant_message["metadata"])
                
                except Exception as e:
                    error_message = {
                        "role": "system",
                        "content": f"Error: {str(e)}",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.messages.append(error_message)
                    st.error(f"Error: {str(e)}")
    
    @staticmethod
    def _render_debug_info():
        """Render debug information"""
        
        with st.expander("🔍 Debug Information", expanded=False):
            st.subheader("Session State")
            debug_state = {
                "Total Messages": len(st.session_state.messages),
                "Selected Model": st.session_state.get("selected_model", "Not set"),
                "Conversation ID": st.session_state.get("conversation_id", "None"),
                "Auto Scroll": st.session_state.get("auto_scroll", False)
            }
            st.json(debug_state)
            
            if st.session_state.messages:
                st.subheader("Message History")
                for i, msg in enumerate(st.session_state.messages):
                    st.text(f"Message {i + 1}: {msg.get('role')} - {len(msg.get('content', ''))} chars")
