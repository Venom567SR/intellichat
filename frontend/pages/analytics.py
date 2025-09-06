"""
Analytics page for IntelliSupport
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="Analytics - IntelliSupport",
    page_icon="📊",
    layout="wide"
)

def generate_sample_data():
    """Generate sample analytics data"""
    
    # Generate date range
    dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
    
    # Sample conversation data
    conversations_data = []
    for date in dates:
        for _ in range(random.randint(5, 20)):
            conversations_data.append({
                "date": date,
                "intent": random.choice(["billing", "technical", "general", "complaint", "feedback"]),
                "sentiment": random.choice(["positive", "neutral", "negative"]),
                "resolution_time": random.randint(30, 600),  # seconds
                "satisfaction": random.randint(1, 5),
                "agent_confidence": random.uniform(0.6, 1.0)
            })
    
    return pd.DataFrame(conversations_data)

def main():
    """Main analytics page"""
    
    st.title("📊 IntelliSupport Analytics")
    st.markdown("Real-time insights into customer support interactions")
    
    # Generate sample data
    df = generate_sample_data()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_conversations = len(df)
        st.metric("Total Conversations", total_conversations)
    
    with col2:
        avg_satisfaction = df["satisfaction"].mean()
        st.metric("Avg Satisfaction", f"{avg_satisfaction:.1f}/5")
    
    with col3:
        avg_resolution_time = df["resolution_time"].mean()
        st.metric("Avg Resolution Time", f"{avg_resolution_time:.0f}s")
    
    with col4:
        positive_sentiment = (df["sentiment"] == "positive").sum() / len(df) * 100
        st.metric("Positive Sentiment", f"{positive_sentiment:.1f}%")
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Intent Distribution")
        intent_counts = df["intent"].value_counts()
        fig = px.pie(
            values=intent_counts.values,
            names=intent_counts.index,
            title="Query Intents"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Sentiment Analysis")
        sentiment_counts = df["sentiment"].value_counts()
        colors = {"positive": "#22c55e", "neutral": "#6b7280", "negative": "#ef4444"}
        fig = px.bar(
            x=sentiment_counts.index,
            y=sentiment_counts.values,
            title="Sentiment Distribution",
            color=sentiment_counts.index,
            color_discrete_map=colors
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Time series
    st.subheader("Conversations Over Time")
    daily_counts = df.groupby(df["date"].dt.date).size().reset_index()
    daily_counts.columns = ["date", "conversations"]
    
    fig = px.line(
        daily_counts,
        x="date",
        y="conversations",
        title="Daily Conversation Volume"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed data
    st.subheader("Recent Conversations")
    
    # Display sample of recent data
    recent_data = df.head(100).copy()
    recent_data["date"] = recent_data["date"].dt.strftime("%Y-%m-%d %H:%M")
    
    st.dataframe(
        recent_data,
        use_container_width=True,
        hide_index=True
    )

if __name__ == "__main__":
    main()
