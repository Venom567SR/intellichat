"""
Settings page for IntelliSupport
"""

import streamlit as st
import yaml
from pathlib import Path
import os

st.set_page_config(
    page_title="Settings - IntelliSupport",
    page_icon="⚙️",
    layout="wide"
)

def load_config():
    """Load current configuration"""
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    if config_path.exists():
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    return {}

def save_config(config):
    """Save configuration to file"""
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)

def main():
    """Main settings page"""
    
    st.title("⚙️ IntelliSupport Settings")
    st.markdown("Configure your IntelliSupport instance")
    
    # Load current config
    config = load_config()
    
    # Create tabs for different settings sections
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 LLM Settings", "🔍 Retrieval", "🛡️ Safety", "🎨 UI"])
    
    with tab1:
        st.header("LLM Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            primary_model = st.selectbox(
                "Primary Model",
                [
                    "groq/llama-3.1-70b-versatile",
                    "groq/llama-3.1-8b-instant",
                    "google/gemini-1.5-flash",
                    "google/gemini-1.5-pro",
                    "openai/gpt-4",
                    "openai/gpt-3.5-turbo"
                ],
                index=0,
                help="Primary LLM model for responses"
            )
            
            max_tokens = st.number_input(
                "Max Tokens",
                min_value=256,
                max_value=4096,
                value=config.get("llm", {}).get("max_tokens", 1024),
                step=128,
                help="Maximum tokens in response"
            )
        
        with col2:
            fallback_model = st.selectbox(
                "Fallback Model",
                [
                    "google/gemini-1.5-flash",
                    "groq/llama-3.1-8b-instant",
                    "openai/gpt-3.5-turbo"
                ],
                index=0,
                help="Backup model if primary fails"
            )
            
            timeout_seconds = st.number_input(
                "Timeout (seconds)",
                min_value=10,
                max_value=120,
                value=config.get("llm", {}).get("timeout_seconds", 20),
                step=5,
                help="Request timeout duration"
            )
        
        # Temperature and other advanced settings
        with st.expander("Advanced LLM Settings"):
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=config.get("llm", {}).get("temperature", 0.7),
                step=0.1,
                help="Creativity vs consistency (0=conservative, 1=creative)"
            )
            
            top_p = st.slider(
                "Top P",
                min_value=0.1,
                max_value=1.0,
                value=config.get("llm", {}).get("top_p", 0.9),
                step=0.1,
                help="Nucleus sampling parameter"
            )
    
    with tab2:
        st.header("Retrieval Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            collection_name = st.text_input(
                "ChromaDB Collection",
                value=config.get("retrieval", {}).get("chroma_collection", "org_docs_v1"),
                help="Name of the ChromaDB collection"
            )
            
            top_k = st.number_input(
                "Top K Results",
                min_value=1,
                max_value=20,
                value=config.get("retrieval", {}).get("top_k", 5),
                step=1,
                help="Number of documents to retrieve"
            )
        
        with col2:
            persist_dir = st.text_input(
                "Persist Directory",
                value=config.get("retrieval", {}).get("persist_directory", "db/chroma"),
                help="Directory for ChromaDB persistence"
            )
            
            score_threshold = st.slider(
                "Score Threshold",
                min_value=0.0,
                max_value=1.0,
                value=config.get("retrieval", {}).get("score_threshold", 0.3),
                step=0.05,
                help="Minimum similarity score for retrieved documents"
            )
        
        # Embedding settings
        with st.expander("Embedding Settings"):
            embedding_model = st.selectbox(
                "Embedding Model",
                [
                    "sentence-transformers/all-MiniLM-L6-v2",
                    "sentence-transformers/all-mpnet-base-v2",
                    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
                ],
                index=0,
                help="Model for generating text embeddings"
            )
            
            batch_size = st.number_input(
                "Batch Size",
                min_value=8,
                max_value=64,
                value=config.get("embedding", {}).get("batch_size", 16),
                step=8,
                help="Batch size for embedding generation"
            )
    
    with tab3:
        st.header("Safety & PII Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            confidence_threshold = st.slider(
                "Safety Confidence Threshold",
                min_value=0.5,
                max_value=1.0,
                value=config.get("safety", {}).get("confidence_threshold", 0.6),
                step=0.05,
                help="Minimum confidence for safety checks"
            )
            
            pii_redaction = st.checkbox(
                "Enable PII Redaction",
                value=config.get("safety", {}).get("pii_redaction", True),
                help="Automatically redact personally identifiable information"
            )
        
        with col2:
            content_filtering = st.checkbox(
                "Enable Content Filtering",
                value=config.get("safety", {}).get("content_filtering", True),
                help="Filter potentially harmful content"
            )
            
            escalation_keywords = st.text_area(
                "Escalation Keywords",
                value=", ".join(config.get("safety", {}).get("escalation_keywords", ["urgent", "complaint", "angry", "lawsuit"])),
                help="Keywords that trigger human escalation (comma-separated)"
            )
    
    with tab4:
        st.header("User Interface Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            theme = st.selectbox(
                "Theme",
                ["light", "dark", "auto"],
                index=0,
                help="UI theme preference"
            )
            
            show_debug_default = st.checkbox(
                "Show Debug by Default",
                value=config.get("ui", {}).get("show_debug_default", False),
                help="Show debug information by default"
            )
        
        with col2:
            auto_scroll = st.checkbox(
                "Auto Scroll",
                value=config.get("ui", {}).get("auto_scroll", True),
                help="Automatically scroll to new messages"
            )
            
            message_limit = st.number_input(
                "Message History Limit",
                min_value=50,
                max_value=1000,
                value=config.get("ui", {}).get("message_limit", 200),
                step=50,
                help="Maximum messages to keep in history"
            )
    
    # Save configuration
    st.divider()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("💾 Save Configuration", type="primary", use_container_width=True):
            # Build new config
            new_config = {
                "llm": {
                    "primary_model": primary_model,
                    "fallback_model": fallback_model,
                    "max_tokens": max_tokens,
                    "timeout_seconds": timeout_seconds,
                    "temperature": temperature,
                    "top_p": top_p
                },
                "embedding": {
                    "model_name": embedding_model,
                    "batch_size": batch_size
                },
                "retrieval": {
                    "chroma_collection": collection_name,
                    "persist_directory": persist_dir,
                    "top_k": top_k,
                    "score_threshold": score_threshold
                },
                "safety": {
                    "confidence_threshold": confidence_threshold,
                    "pii_redaction": pii_redaction,
                    "content_filtering": content_filtering,
                    "escalation_keywords": [kw.strip() for kw in escalation_keywords.split(",")]
                },
                "ui": {
                    "theme": theme,
                    "show_debug_default": show_debug_default,
                    "auto_scroll": auto_scroll,
                    "message_limit": message_limit
                },
                "logging": {
                    "file_path": "logs/app.log",
                    "log_level": "INFO"
                }
            }
            
            try:
                save_config(new_config)
                st.success("✅ Configuration saved successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Error saving configuration: {str(e)}")
    
    # Configuration preview
    with st.expander("📄 Configuration Preview"):
        st.code(yaml.dump(config, default_flow_style=False), language="yaml")

if __name__ == "__main__":
    main()
