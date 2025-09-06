"""
Header component for IntelliSupport
"""

import streamlit as st

class Header:
    @staticmethod
    def render():
        """Render the application header"""
        
        st.markdown("""
        <div style="padding: 1rem 0; border-bottom: 1px solid #e0e0e0; margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 2rem;">🤖</div>
                <div>
                    <h1 style="margin: 0; color: #1f2937;">IntelliSupport</h1>
                    <p style="margin: 0; color: #6b7280; font-size: 0.9rem;">Intelligent Customer Support Agent</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
