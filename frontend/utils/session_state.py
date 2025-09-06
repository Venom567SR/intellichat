"""
Session state management utilities
"""

import streamlit as st
from datetime import datetime

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    
    # Chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # UI settings
    if "show_debug" not in st.session_state:
        st.session_state.show_debug = False
    
    if "auto_scroll" not in st.session_state:
        st.session_state.auto_scroll = True
    
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "groq/llama-3.1-70b-versatile"
    
    # Conversation tracking
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = None
    
    if "session_start_time" not in st.session_state:
        st.session_state.session_start_time = datetime.now()
    
    # Agent activity tracking
    if "agent_activity" not in st.session_state:
        st.session_state.agent_activity = {}

def reset_conversation():
    """Reset the conversation state"""
    st.session_state.messages = []
    st.session_state.conversation_id = None
    st.session_state.agent_activity = {}

def get_session_stats():
    """Get session statistics"""
    total_messages = len(st.session_state.messages)
    user_messages = sum(1 for msg in st.session_state.messages if msg.get("role") == "user")
    assistant_messages = sum(1 for msg in st.session_state.messages if msg.get("role") == "assistant")
    
    session_duration = datetime.now() - st.session_state.session_start_time
    
    return {
        "total_messages": total_messages,
        "user_messages": user_messages,
        "assistant_messages": assistant_messages,
        "session_duration": session_duration,
        "messages_per_minute": total_messages / max(session_duration.total_seconds() / 60, 1)
    }
