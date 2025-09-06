"""
Configuration management utilities
"""

import streamlit as st
import yaml
import os
from pathlib import Path

@st.cache_data
def load_config():
    """Load configuration from config.yaml"""
    
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    
    if config_path.exists():
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    else:
        # Default configuration
        return {
            "llm": {
                "primary_model": "groq/llama-3.1-70b-versatile",
                "fallback_model": "google/gemini-1.5-flash",
                "max_tokens": 1024,
                "timeout_seconds": 20
            },
            "api": {
                "base_url": "http://localhost:8000",
                "timeout": 30
            },
            "ui": {
                "theme": "light",
                "auto_scroll": True,
                "show_debug": False
            }
        }

def get_api_config():
    """Get API configuration"""
    config = load_config()
    return config.get("api", {
        "base_url": "http://localhost:8000",
        "timeout": 30
    })

def get_ui_config():
    """Get UI configuration"""
    config = load_config()
    return config.get("ui", {
        "theme": "light",
        "auto_scroll": True,
        "show_debug": False
    })
