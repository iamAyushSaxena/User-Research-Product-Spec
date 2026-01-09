"""
Streamlit Custom Components
Reusable UI components for the dashboard
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict

def render_metric_card(title: str, value: str, delta: str = None, 
                       delta_color: str = "normal", icon: str = "📊"):
    """
    Render a metric card with optional delta
    
    Args:
        title: Metric title
        value: Main value to display
        delta: Change value (optional)
        delta_color: Color of delta (normal, inverse, off)
        icon: Emoji icon
    """
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: white;
        margin-bottom: 1rem;
    ">
        <div style="font-size: 2rem;">{icon}</div>
        <div style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem;">{title}</div>
        <div style="font-size: 2rem; font-weight: bold; margin-top: 0.5rem;">{value}</div>
        {f'<div style="font-size: 0.9rem; margin-top: 0.5rem;">▲ {delta}</div>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)

def render_persona_card(persona: Dict):
    """
    Render a detailed persona card
    
    Args:
        persona: Persona dictionary
    """
    st.markdown(f"""
    <div style="
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <h2 style="color: #667eea; margin-bottom: 0.5rem;">{persona['name']}</h2>
        <p style="color: #666; font-style: italic; margin-bottom: 1.5rem;">"{persona['tagline']}"</p>
        
        <div style="margin-bottom: 1rem;">
            <strong>Age:</strong> {persona['demographics']['age']} | 
            <strong>Occupation:</strong> {persona['demographics']['occupation']}
        </div>
        
        <div style="margin-bottom: 1rem;">
            <strong>Tech Savviness:</strong> {persona['demographics']['tech_savviness']}
        </div>
        
        <div style="margin-top: 1.5rem;">
            <h4>Primary Pain Point</h4>
            <p style="background: #fff3cd; padding: 1rem; border-radius: 5px; border-left: 4px solid #ffc107;">
                {persona['behavioral_patterns']['primary_pain']}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_journey_stage(stage: Dict, state: str = "current"):
    """
    Render a journey map stage
    
    Args:
        stage: Stage dictionary
        state: 'current' or 'future'
    """
    if state == "current":
        color = "#dc3545"  # Red for pain points
        pain_key = "pain"
    else:
        color = "#28a745"  # Green for delights
        pain_key = "delight"
    
    st.markdown(f"""
                <div style="background: white; color: #333333; border-left: 4px solid {color}; padding: 1.5rem; margin-bottom: 1rem; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="margin: 0; color: {color};">{stage['stage']}</h3>
                <div style="font-size: 2rem;">{stage['emotion']}</div>
                </div>
                <div style="margin-bottom: 0.5rem;">
                <strong>Action:</strong> {stage['action']}
                </div>
                <div style="margin-bottom: 0.5rem;">
                <strong>Duration:</strong> {stage['duration']}
                </div>
                <div style="background: {'#ffebee' if state == 'current' else '#e8f5e9'}; color: #333333; padding: 1rem; border-radius: 5px; margin-top: 1rem;">
                <strong>{pain_key.title()}:</strong> {stage[pain_key]}
                </div>
                </div>
            """, unsafe_allow_html=True)

def render_insight_card(insight: Dict):
    """
    Render an insight card with evidence and implications
    """
    priority_colors = {
        "Critical": "#dc3545",
        "High": "#ff9800",
        "Medium": "#ffc107"
    }
    
    priority_color = priority_colors.get(insight['priority'], "#6c757d")
    
    st.markdown(f"""
                <div style="background: white; color: #333333; border: 2px solid {priority_color}; border-radius: 10px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                <h3 style="color: {priority_color}; margin: 0;">{insight['title']}</h3>
                <span style="background: {priority_color}; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; font-weight: bold;">{insight['priority']}</span>
                </div>
                <p style="color: #333333; font-size: 1.05rem; margin-bottom: 1rem;">
                {insight['description']}
                </p>
                <div style="background: #f8f9fa; color: #333333; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                <strong>Evidence:</strong>
                <ul style="margin-top: 0.5rem; margin-bottom: 0;">
                {''.join([f'<li>{e}</li>' for e in insight['evidence']])}
                </ul>
                </div>
                <div style="background: #e7f3ff; color: #333333; padding: 1rem; border-radius: 5px; border-left: 4px solid #2196f3;">
                <strong>💡 Implication:</strong> {insight['implication']}
                </div>
                </div>
            """, unsafe_allow_html=True)

def create_funnel_chart(stages: List[str], values: List[float], title: str = "User Funnel"):
    """
    Create a funnel chart
    
    Args:
        stages: List of stage names
        values: List of values (percentages or counts)
        title: Chart title
    """
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textinfo="value+percent initial",
        marker=dict(
            color=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe'],
        )
    ))
    
    fig.update_layout(
        title=title,
        height=400,
        showlegend=False
    )
    
    return fig

def create_timeline_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str):
    """
    Create a timeline/line chart
    
    Args:
        df: DataFrame with data
        x_col: Column for x-axis
        y_col: Column for y-axis
        title: Chart title
    """
    fig = px.line(df, x=x_col, y=y_col, 
                  title=title,
                  markers=True)
    
    fig.update_traces(line_color='#667eea', line_width=3)
    fig.update_layout(height=400)
    
    return fig

def create_sentiment_chart(sentiment_counts: Dict):
    """
    Create sentiment distribution chart
    
    Args:
        sentiment_counts: Dictionary with sentiment counts
    """
    colors = {
        'negative': '#dc3545',
        'neutral': '#ffc107',
        'positive': '#28a745'
    }
    
    # 1. Calculate the maximum value to set dynamic range
    max_count = max(sentiment_counts.values()) if sentiment_counts else 0
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(sentiment_counts.keys()),
            y=list(sentiment_counts.values()),
            marker_color=[colors.get(k, '#6c757d') for k in sentiment_counts.keys()],
            text=list(sentiment_counts.values()),
            textposition='outside',
            # 2. Prevent text from being clipped if it hits the very edge
            cliponaxis=False 
        )
    ])
    
    fig.update_layout(
        title="Sentiment Distribution",
        xaxis_title="Sentiment",
        yaxis_title="Count",
        height=300,
        showlegend=False,
        # 3. Add headroom to Y-axis (15-20% extra space)
        yaxis=dict(range=[0, max_count * 1.2]), 
        margin=dict(t=40, b=20) 
    )
    
    return fig

def create_theme_distribution_chart(theme_counts: pd.Series):
    """
    Create theme distribution pie chart
    
    Args:
        theme_counts: Series with theme counts
    """
    fig = px.pie(
        values=theme_counts.values,
        names=theme_counts.index,
        title="Pain Point Theme Distribution",
        hole=0.3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    
    return fig