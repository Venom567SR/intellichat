"""
IntelliSupport Streamlit Frontend
Main application entry point
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from components.chat_interface import ChatInterface
from components.sidebar import Sidebar
from components.header import Header
from utils.session_state import initialize_session_state
from utils.config import load_config

# Page configuration
st.set_page_config(
    page_title="IntelliSupport",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function"""
    
    # Initialize session state
    initialize_session_state()
    
    # Load configuration
    config = load_config()
    
    # Render header
    Header.render()
    
    # Create layout
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        # Render sidebar
        Sidebar.render()
    
    with col2:
        # Main chat interface
        ChatInterface.render()
    
    with col3:
        # Additional info or controls
        st.empty()

if __name__ == "__main__":
    main()
