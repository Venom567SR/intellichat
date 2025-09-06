"""
Sidebar component for IntelliSupport
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

class Sidebar:
    @staticmethod
    def render():
        """Render the sidebar with controls and information"""
        
        st.sidebar.header("🛠️ Controls")
        
        # Chat settings
        with st.sidebar.expander("Chat Settings", expanded=True):
            st.session_state.show_debug = st.checkbox("Show Debug Info", value=False)
            st.session_state.auto_scroll = st.checkbox("Auto Scroll", value=True)
            
            # Model selection
            model_options = [
                "groq/llama-3.1-70b-versatile",
                "google/gemini-1.5-flash",
                "openai/gpt-4"
            ]
            st.session_state.selected_model = st.selectbox(
                "Select Model",
                model_options,
                index=0
            )
        
        # Clear chat button
        if st.sidebar.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.messages = []
            st.session_state.conversation_id = None
            st.rerun()
        
        # Session statistics
        st.sidebar.header("📊 Session Stats")
        
        # Calculate stats
        total_messages = len(st.session_state.messages)
        user_messages = sum(1 for msg in st.session_state.messages if msg.get("role") == "user")
        assistant_messages = sum(1 for msg in st.session_state.messages if msg.get("role") == "assistant")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Total", total_messages)
            st.metric("User", user_messages)
        with col2:
            st.metric("Assistant", assistant_messages)
            st.metric("Active", "✅" if total_messages > 0 else "⏸️")
        
        # Agent activity
        if st.session_state.get("agent_activity"):
            st.sidebar.header("🤖 Agent Activity")
            
            # Create sample activity data
            activity_data = pd.DataFrame({
                "Agent": ["Manager", "Intent", "Sentiment", "RAG", "Safety"],
                "Calls": [10, 8, 6, 12, 4],
                "Avg Time (ms)": [120, 80, 60, 200, 40]
            })
            
            # Agent usage chart
            fig = px.bar(
                activity_data, 
                x="Agent", 
                y="Calls",
                title="Agent Usage",
                color="Calls",
                color_continuous_scale="viridis"
            )
            fig.update_layout(height=300, showlegend=False)
            st.sidebar.plotly_chart(fig, use_container_width=True)
        
        # System status
        st.sidebar.header("🟢 System Status")
        
        status_items = [
            ("Backend API", "🟢 Online"),
            ("ChromaDB", "🟢 Connected"),
            ("LLM Service", "🟢 Available"),
            ("Safety Check", "🟢 Active")
        ]
        
        for service, status in status_items:
            st.sidebar.text(f"{service}: {status}")
        
        # Recent activity
        if total_messages > 0:
            st.sidebar.header("📝 Recent Activity")
            recent_messages = st.session_state.messages[-3:] if len(st.session_state.messages) >= 3 else st.session_state.messages
            
            for i, msg in enumerate(reversed(recent_messages)):
                with st.sidebar.expander(f"Message {len(recent_messages) - i}", expanded=False):
                    st.text(f"Role: {msg.get('role', 'unknown')}")
                    content_preview = msg.get('content', '')[:100] + "..." if len(msg.get('content', '')) > 100 else msg.get('content', '')
                    st.text(f"Content: {content_preview}")
                    if msg.get('timestamp'):
                        st.text(f"Time: {msg['timestamp']}")
        
        # Footer
        st.sidebar.markdown("---")
        st.sidebar.markdown(
            '<p style="text-align: center; color: #6b7280; font-size: 0.8rem;">'
            'IntelliSupport v1.0<br>'
            'Powered by AI</p>',
            unsafe_allow_html=True
        )
