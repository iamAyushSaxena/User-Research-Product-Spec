"""
Main Streamlit Dashboard
User Research to Product Spec: Reducing Productivity Tool Abandonment

Author: Ayush Saxena
Date: January 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from config import *
from streamlit_components import *

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title=STREAMLIT_CONFIG["page_title"],
    page_icon=STREAMLIT_CONFIG["page_icon"],
    layout=STREAMLIT_CONFIG["layout"],
    initial_sidebar_state=STREAMLIT_CONFIG["initial_sidebar_state"]
)

# ===== CUSTOM CSS =====
st.markdown("""
<style>
    /* Main title styling */
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* Subtitle styling */
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    /* Quote box */
    .quote-box {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-radius: 5px;
        font-style: italic;
        color: #333;
    }
    
    /* Stat box */
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Section divider */
    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        margin: 3rem 0;
        border-radius: 2px;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Improve spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ===== DATA LOADING FUNCTIONS =====
@st.cache_data
def load_interview_metadata():
    """Load interview metadata"""
    return pd.read_csv(RAW_DATA_DIR / "interview_metadata.csv")

@st.cache_data
def load_affinity_data():
    """Load affinity mapping data"""
    return pd.read_csv(PROCESSED_DATA_DIR / "affinity_clusters.csv")

@st.cache_data
def load_personas():
    """Load personas"""
    with open(PROCESSED_DATA_DIR / "personas.json", 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def load_journey_maps():
    """Load journey maps"""
    with open(PROCESSED_DATA_DIR / "journey_map_data.json", 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def load_insights():
    """Load synthesized insights"""
    with open(PROCESSED_DATA_DIR / "insights_synthesis.json", 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def load_interview_transcript(interview_num):
    """Load a specific interview transcript"""
    file_path = INTERVIEW_DIR / f"interview_{interview_num:02d}.txt"
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# ===== SIDEBAR NAVIGATION =====
def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        st.markdown("# 📊 Navigation")
        st.markdown("---")
        
        page = st.radio(
            "Select Section:",
            [
                "🏠 Home",
                "🔍 Research Process",
                "💬 Interview Insights",
                "🗂️ Affinity Mapping",
                "👥 User Personas",
                "🗺️ Journey Maps",
                "💡 Key Insights",
                "📄 Product Requirements",
                "📊 Impact & Metrics"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### 📌 Quick Stats")
        
        metadata = load_interview_metadata()
        
        st.metric("Total Interviews", len(metadata))
        st.metric("Observations", "180+")
        st.metric("Personas Created", "3")
        
        st.markdown("---")
        st.markdown("### 🎯 Project Info")
        st.markdown("**Author:** Ayush Saxena")
        st.markdown("**Date:** January 2026")
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.8rem;'>
            © 2026 Ayush Saxena. All rights reserved.
        </div>
        """, unsafe_allow_html=True)
    
    return page

# ===== PAGE FUNCTIONS =====

def render_home_page():
    """Render home/executive summary page"""
    st.markdown("<h1 class='main-title'>User Research to Product Spec</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Reducing Productivity Tool Abandonment in the Critical First 14 Days</p>", unsafe_allow_html=True)
    
    # Hero section
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='stat-box'>
            <div style='font-size: 3rem; margin-bottom: 0.5rem;'>64%</div>
            <div style='font-size: 1rem;'>Abandon by Day 14</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='stat-box'>
            <div style='font-size: 3rem; margin-bottom: 0.5rem;'>82%</div>
            <div style='font-size: 1rem;'>Cite "Too Complex"</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='stat-box'>
            <div style='font-size: 3rem; margin-bottom: 0.5rem;'>2.5x</div>
            <div style='font-size: 1rem;'>Better Retention with Day-1 Win</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Executive Summary
    st.markdown("## 📋 Executive Summary")
    
    st.markdown("""
    This research project investigates **why students and young professionals abandon productivity tools** 
    within the first 14 days, despite strong initial motivation. Through **22 qualitative interviews**, 
    **affinity mapping of 180+ observations**, and **behavioral pattern analysis**, this study uncovers 
    the root causes of abandonment and proposes a **product specification** to achieve **20+ percentage point 
    improvement in Day-14 retention**.
    """)
    
    st.markdown("### 🎯 Research Objectives")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Primary Questions:**
        - Why do users abandon productivity tools?
        - What specific moments trigger abandonment?
        - What emotional factors drive the decision?
        - How can product design prevent abandonment?
        """)
    
    with col2:
        st.markdown("""
        **Success Criteria:**
        - Identify root causes (not symptoms)
        - Quantify pain point prevalence
        - Create actionable personas
        - Generate testable product recommendations
        """)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Key Findings
    st.markdown("## 🔍 Key Findings")
    
    findings = [
        {
            "title": "Critical 14-Day Window",
            "description": "Tool abandonment happens rapidly in first 14 days, not gradually. 64% abandon before Day 14.",
            "icon": "⏰"
        },
        {
            "title": "Cognitive Overload, Not Lack of Discipline",
            "description": "82% cite 'too complicated' as primary reason. Users with 5-7 features complete 3x more tasks than those with 20+.",
            "icon": "🧠"
        },
        {
            "title": "Guilt-Driven Abandonment",
            "description": "68% report guilt from incomplete tasks. Users blame themselves ('not disciplined enough'), not the tool.",
            "icon": "😔"
        },
        {
            "title": "Setup Fatigue Prevents Usage",
            "description": "73% spend 2-4 hours on setup. Users exhausted before doing actual work.",
            "icon": "😫"
        },
        {
            "title": "First 24 Hours Predict Success",
            "description": "Users completing 1 task on Day 1 have 2.5x better Day-14 retention (45% vs 18%).",
            "icon": "🎯"
        }
    ]
    
    for finding in findings:
        st.markdown(f"""
        <div style='
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        '>
            <div style='display: flex; align-items: start;'>
                <div style='font-size: 2.5rem; margin-right: 1rem;'>{finding['icon']}</div>
                <div>
                    <h4 style='margin-top: 0; color: #667eea;'>{finding['title']}</h4>
                    <p style='margin-bottom: 0; color: #333;'>{finding['description']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Methodology Overview
    st.markdown("## 🔬 Methodology Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        **1. Interviews**
        - 22 participants
        - 30-45 min each
        - Semi-structured
        - Nov-Dec 2025
        """)
    
    with col2:
        st.markdown("""
        **2. Affinity Mapping**
        - 180+ observations
        - 8 major themes
        - Sentiment analysis
        - Pattern recognition
        """)
    
    with col3:
        st.markdown("""
        **3. Persona Development**
        - 3 behavioral personas
        - Journey mapping
        - Pain point analysis
        - Needs identification
        """)
    
    with col4:
        st.markdown("""
        **4. Synthesis**
        - 7 key insights
        - 5 behavioral patterns
        - 7 product recommendations
        - PRD creation
        """)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Proposed Solution
    st.markdown("## 💡 Proposed Solution: Progressive Productivity Tool")
    
    st.markdown("""
    Based on research findings, I propose a **progressive onboarding and task visibility model** 
    that addresses the root causes of abandonment:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Core Principles")
        st.markdown("""
        - **Start Minimal:** 3 visible tasks maximum
        - **Quick Setup:** < 2 minutes to first task
        - **Progressive Disclosure:** Unlock features based on usage
        - **Anti-Guilt Design:** No overdue badges or red notifications
        - **Immediate Wins:** First task completion in first session
        """)
    
    with col2:
        st.markdown("### 🎯 Target Metrics")
        st.markdown("""
        - **Day 14 Retention:** 38% (vs 18% baseline) → **+20pp**
        - **Time to First Win:** < 5 min (vs 180 min baseline)
        - **Task Completion Rate:** 55% (vs 22% baseline)
        - **Stress Score:** 3.2/10 (vs 6.8/10 baseline)
        """)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Impact
    st.markdown("## 📈 Expected Business Impact")
    
    st.markdown("""
    Improving Day-14 retention from **18% to 38%** (+20pp) has significant business implications:
    """)
    
    impact_data = pd.DataFrame({
        'Metric': ['30-Day Retention', '90-Day Retention', 'LTV per User', 'Referral Rate'],
        'Baseline': ['12%', '8%', '$15', '5%'],
        'Target': ['25%', '20%', '$45', '15%'],
        'Improvement': ['+108%', '+150%', '+200%', '+200%']
    })
    
    st.dataframe(impact_data, use_container_width=True, hide_index=True)
    
    st.info("💡 **Note:** This is a research project demonstrating PM skills in user research, synthesis, and product specification—not a startup pitch.")

def render_research_process_page():
    """Render research process page"""
    st.markdown("# 🔍 Research Process")
    st.markdown("Detailed methodology and approach")
    st.markdown("---")
    
    # Research Plan
    st.markdown("## 📋 Research Plan")
    
    st.markdown("""
    ### Objectives
    1. **Understand abandonment patterns:** Why do users stop using productivity tools?
    2. **Identify critical moments:** What specific events trigger abandonment?
    3. **Uncover emotional drivers:** What feelings contribute to the decision?
    4. **Generate actionable insights:** What product changes would prevent abandonment?
    """)
    
    st.markdown("### Research Questions")
    
    questions = [
        "What productivity tools have you tried, and what happened?",
        "Walk me through your typical experience with a new productivity tool.",
        "What specific moment made you stop using the tool?",
        "How did the tool make you feel? (emotions, not just functionality)",
        "If you could design the perfect productivity tool, what would it look like?"
    ]
    
    for i, q in enumerate(questions, 1):
        st.markdown(f"**{i}.** {q}")
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Interview Guide
    st.markdown("## 📝 Interview Guide")
    
    with st.expander("View Complete Interview Script", expanded=False):
        st.markdown("""
        ### Introduction (2 minutes)
        - Thank participant
        - Explain research purpose
        - Emphasize no right/wrong answers
        - Get consent
        
        ### Warm-Up (5 minutes)
        - Tell me about yourself
        - How do you currently manage your tasks?
        - What's your relationship with productivity?
        
        ### Tool History (10 minutes)
        - What productivity tools have you tried?
        - Walk me through discovering and starting with [Tool X]
        - What was the setup experience like?
        - How did you use it in the first week?
        
        ### Abandonment Deep-Dive (15 minutes)
        - What changed after the first week?
        - Can you pinpoint the moment you started using it less?
        - How did that make you feel?
        - What did you tell yourself about why you stopped?
        - Did you try to restart? What happened?
        
        ### Ideal Solution (5 minutes)
        - What would the perfect tool look like?
        - What would need to change for you to stick with a tool?
        - What features would you remove, not add?
        
        ### Closing (3 minutes)
        - Anything else to share?
        - Can I follow up if needed?
        - Thank you!
        """)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Participant Demographics
    st.markdown("## 👥 Participant Demographics")
    
    metadata = load_interview_metadata()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Age distribution
        fig_age = px.histogram(metadata, x='age', nbins=10,
                               title="Age Distribution",
                               labels={'age': 'Age', 'count': 'Number of Participants'})
        fig_age.update_traces(marker_color='#667eea')
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        # Persona distribution
        persona_counts = metadata['persona'].value_counts()
        fig_persona = px.pie(values=persona_counts.values, 
                            names=persona_counts.index,
                            title="Persona Distribution",
                            hole=0.4)
        st.plotly_chart(fig_persona, use_container_width=True)
    
    # Tools abandoned
    st.markdown("### Tools Abandoned Distribution")
    fig_tools = px.histogram(metadata, x='tools_abandoned',
                            title="Number of Tools Previously Abandoned per Participant",
                            labels={'tools_abandoned': 'Tools Abandoned', 'count': 'Participants'})
    fig_tools.update_traces(marker_color='#764ba2')
    st.plotly_chart(fig_tools, use_container_width=True)
    
    # Interview timeline
    st.markdown("### Interview Timeline")
    metadata['date'] = pd.to_datetime(metadata['date'])
    timeline_data = metadata.groupby('date').size().reset_index(name='count')
    timeline_data['cumulative'] = timeline_data['count'].cumsum()
    
    fig_timeline = go.Figure()
    fig_timeline.add_trace(go.Scatter(x=timeline_data['date'], y=timeline_data['cumulative'],
                                     mode='lines+markers',
                                     name='Cumulative Interviews',
                                     line=dict(color='#667eea', width=3)))
    fig_timeline.update_layout(title="Interview Timeline (Cumulative)",
                              xaxis_title="Date",
                              yaxis_title="Cumulative Interviews",
                              height=400)
    st.plotly_chart(fig_timeline, use_container_width=True)

def render_interview_insights_page():
    """Render interview insights page"""
    st.markdown("# 💬 Interview Insights")
    st.markdown("Explore all 22 interview transcripts and key quotes")
    st.markdown("---")
    
    metadata = load_interview_metadata()
    
    # Interview selector
    st.markdown("## 📂 Browse Interviews")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_interview = st.selectbox(
            "Select Interview:",
            range(1, len(metadata) + 1),
            format_func=lambda x: f"Interview {x:02d}"
        )
    
    with col2:
        interview_meta = metadata[metadata['interview_id'] == f"INT_{selected_interview:03d}"].iloc[0]
        st.markdown(f"""
        **Date:** {interview_meta['date']}  
        **Duration:** {interview_meta['duration_minutes']} minutes  
        **Persona:** {interview_meta['persona']}  
        **Tools Abandoned:** {interview_meta['tools_abandoned']}
        """)
    
    # Display transcript
    transcript = load_interview_transcript(selected_interview)
    
    with st.expander(f"📄 View Full Transcript - Interview {selected_interview:02d}", expanded=True):
        st.text(transcript)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Key Quotes
    st.markdown("## 💭 Most Revealing Quotes")
    
    quotes = [
        {
            "quote": "I spend more time organizing than doing. I've watched 10 YouTube tutorials on the 'perfect' Notion setup, but I've completed maybe 5 actual tasks.",
            "theme": "Over-Organization Paradox",
            "persona": "The Overwhelmed Optimizer"
        },
        {
            "quote": "Every time I open the app and see those red overdue badges, I feel like a failure. So I just... stop opening it.",
            "theme": "Productivity Guilt",
            "persona": "The Serial Abandoner"
        },
        {
            "quote": "I spent 3 hours setting up my workspace. By the time I was done, I was exhausted and hadn't actually done any work. That's when I knew it wasn't working.",
            "theme": "Setup Fatigue",
            "persona": "The Overwhelmed Optimizer"
        },
        {
            "quote": "I don't think I'm disciplined enough. Everyone else seems to have their life together with these apps, but I can't stick with anything for more than a week.",
            "theme": "Self-Attribution Bias",
            "persona": "The Serial Abandoner"
        },
        {
            "quote": "Digital tools just feel... cold. I can't doodle, can't violently cross things out when I'm frustrated. It's too rigid.",
            "theme": "Lack of Flexibility",
            "persona": "The Analog Holdout"
        },
        {
            "quote": "There are like 50 features and I use maybe 3 of them. But I feel like I SHOULD be using all of them to be 'productive.' It's overwhelming.",
            "theme": "Feature Overwhelm",
            "persona": "The Overwhelmed Optimizer"
        }
    ]
    
    for quote in quotes:
        st.markdown(f"""
        <div class='quote-box'>
            "{quote['quote']}"
            <div style='margin-top: 1rem; font-size: 0.9rem; color: #666; font-style: normal;'>
                <strong>Theme:</strong> {quote['theme']} | <strong>Persona:</strong> {quote['persona']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Search Functionality
    st.markdown("## 🔍 Search Transcripts")
    
    search_query = st.text_input("Search for keywords across all interviews:", placeholder="e.g., guilt, overwhelm, setup")
    
    if search_query:
        results = []
        for i in range(1, len(metadata) + 1):
            transcript = load_interview_transcript(i)
            if search_query.lower() in transcript.lower():
                # Find context around keyword
                lines = transcript.split('\n')
                matching_lines = [line for line in lines if search_query.lower() in line.lower()]
                results.append({
                    'interview': i,
                    'matches': len(matching_lines),
                    'snippets': matching_lines[:3]  # First 3 matches
                })
        
        if results:
            st.success(f"Found {len(results)} interviews mentioning '{search_query}'")
            
            for result in results:
                with st.expander(f"Interview {result['interview']:02d} ({result['matches']} matches)"):
                    for snippet in result['snippets']:
                        st.markdown(f"- {snippet.strip()}")
        else:
            st.warning(f"No interviews found mentioning '{search_query}'")

def render_affinity_mapping_page():
    """Render affinity mapping page"""
    st.markdown("# 🗂️ Affinity Mapping")
    st.markdown("180+ observations clustered into themes")
    st.markdown("---")
    
    observations_df = load_affinity_data()
    
    # Overview stats
    st.markdown("## 📊 Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate counts
    total_obs = len(observations_df)
    unique_themes = observations_df['theme'].nunique()
    neg_sentiment = (observations_df['sentiment'] == 'negative').sum()
    pos_sentiment = (observations_df['sentiment'] == 'positive').sum()
    
    with col1:
        st.metric("Total Observations", total_obs)
        
    with col2:
        # Grey color (delta_color="off")
        pct = (unique_themes / total_obs) * 100
        st.metric("Unique Themes", unique_themes, delta=f"{pct:.1f}%", delta_color="off")
        
    with col3:
        # Red color (delta_color="inverse" makes positive values red)
        pct = (neg_sentiment / total_obs) * 100
        st.metric("Negative Sentiment", neg_sentiment, delta=f"{pct:.1f}%", delta_color="inverse")
        
    with col4:
        # Green color (delta_color="normal" makes positive values green)
        pct = (pos_sentiment / total_obs) * 100
        st.metric("Positive Sentiment", pos_sentiment, delta=f"{pct:.1f}%", delta_color="normal")
    
    # Theme Distribution
    st.markdown("## 🎨 Theme Distribution")
    
    theme_counts = observations_df['theme'].value_counts()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_theme = create_theme_distribution_chart(theme_counts)
        st.plotly_chart(fig_theme, use_container_width=True)
    
    with col2:
        st.markdown("### Top Themes")
        for theme, count in theme_counts.head(5).items():
            pct = (count / len(observations_df)) * 100
            st.markdown(f"""
            <div style='background: #f8f9fa; color: #333333; padding: 0.75rem; border-radius: 5px; margin-bottom: 0.5rem;'>
                <strong>{theme}</strong><br>
                {count} observations ({pct:.1f}%)
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Sentiment Analysis
    st.markdown("## 😊😐😔 Sentiment Analysis")
    
    sentiment_counts = observations_df['sentiment'].value_counts().to_dict()
    fig_sentiment = create_sentiment_chart(sentiment_counts)
    st.plotly_chart(fig_sentiment, use_container_width=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Theme Deep Dive
    st.markdown("## 🔍 Theme Deep Dive")
    
    selected_theme = st.selectbox("Select a theme to explore:", theme_counts.index.tolist())
    
    theme_observations = observations_df[observations_df['theme'] == selected_theme]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Observations", len(theme_observations))
    with col2:
        pct = (len(theme_observations) / len(observations_df)) * 100
        st.metric("Percentage", f"{pct:.1f}%")
    with col3:
        neg_pct = (theme_observations['sentiment'] == 'negative').sum() / len(theme_observations) * 100
        st.metric("Negative Sentiment", f"{neg_pct:.0f}%")
    
    # Sample observations
    st.markdown(f"### Sample Observations from '{selected_theme}'")
    
    sample_obs = theme_observations.sample(n=min(10, len(theme_observations)))
    
    for _, obs in sample_obs.iterrows():
        sentiment_emoji = {"negative": "😔", "neutral": "😐", "positive": "😊"}
        st.markdown(f"""
        <div style='background: #f8f9fa; color: #333333; padding: 1rem; border-radius: 5px; margin-bottom: 0.5rem; border-left: 3px solid {"#dc3545" if obs["sentiment"] == "negative" else "#28a745" if obs["sentiment"] == "positive" else "#ffc107"};'>
            {sentiment_emoji[obs['sentiment']]} {obs['text']}
            <div style='font-size: 0.85rem; color: #666; margin-top: 0.5rem;'>
                Source: {obs['interview_id']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Interactive Data Table
    st.markdown("## 📋 All Observations (Searchable)")
    
    # Add search filter
    search_term = st.text_input("Filter observations by keyword:", placeholder="e.g., guilt, setup, overwhelm")
    
    if search_term:
        filtered_df = observations_df[observations_df['text'].str.contains(search_term, case=False, na=False)]
    else:
        filtered_df = observations_df
    
    display_df = filtered_df[['theme', 'sentiment', 'text', 'interview_id']].copy()
    display_df.index = range(1, len(display_df) + 1)

    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )
    
    st.markdown(f"*Showing {len(filtered_df)} of {len(observations_df)} observations*")

def render_personas_page():
    """Render user personas page"""
    st.markdown("# 👥 User Personas")
    st.markdown("3 behavioral personas from research")
    st.markdown("---")
    
    personas = load_personas()
    
    # Persona selector
    persona_names = [p['name'] for p in personas]
    selected_persona_name = st.selectbox("Select Persona:", persona_names)
    
    selected_persona = next(p for p in personas if p['name'] == selected_persona_name)
    
    # Persona Header
    st.markdown(f"## {selected_persona['name']}")
    st.markdown(f"*\"{selected_persona['tagline']}\"*")
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Demographics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Demographics")
        demo = selected_persona['demographics']
        st.markdown(f"""
        - **Age:** {demo['age']} ({demo['age_range']})
        - **Occupation:** {demo['occupation']}
        - **Education:** {demo['education']}
        - **Location:** {demo['location']}
        - **Tech Savviness:** {demo['tech_savviness']}
        """)
    
    with col2:
        st.markdown("### 🎯 Behavioral Patterns")
        behavior = selected_persona['behavioral_patterns']
        st.markdown(f"""
        - **Tools Abandoned:** {behavior['avg_tools_abandoned']}
        - **Typical Abandonment:** {behavior['typical_abandonment_time']}
        - **Primary Pain:** {behavior['primary_pain']}
        """)
    
    with col3:
        st.markdown("### 🧠 Psychographics")
        psycho = selected_persona['psychographics']
        st.markdown(f"""
        - **Personality:** {psycho['personality']}
        """)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Goals and Frustrations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Goals")
        for goal in selected_persona['goals']:
            st.markdown(f"- {goal}")
    
    with col2:
        st.markdown("### ❌ Frustrations")
        for frustration in selected_persona['frustrations']:
            st.markdown(f"- {frustration}")
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Typical Day
    st.markdown("### 📅 A Day in the Life")
    st.markdown(selected_persona['typical_day'])
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Current Tools
    st.markdown("### 🔧 Current Tools")
    for tool in selected_persona['current_tools']:
        st.markdown(f"- {tool}")
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Pain Points
    st.markdown("### 💥 Top Pain Points")
    
    for pain_point in selected_persona['pain_points']:
        st.markdown(f"""
        <div style='background: #fff3cd; color: #333333; padding: 1rem; border-radius: 5px; border-left: 4px solid #ffc107; margin-bottom: 0.5rem;'>
            <strong>{pain_point['theme']}</strong><br>
            Mentioned {pain_point['mentions']} times in interviews
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Quotes
    st.markdown("### 💬 Representative Quotes")
    
    for quote in selected_persona['quotes']:
        st.markdown(f"""
        <div style='background: #f8f9fa; color: #333333; border-left: 4px solid #667eea; padding: 1rem 1.5rem; margin: 1rem 0; border-radius: 5px; font-style: italic;'>
            "{quote}"
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Needs and Success Criteria
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎁 What They Need")
        for need in selected_persona['needs']:
            st.markdown(f"✓ {need}")
    
    with col2:
        st.markdown("### 🏆 Success Looks Like")
        for criterion in selected_persona['success_criteria']:
            st.markdown(f"✓ {criterion}")

def render_journey_maps_page():
    """Render journey maps page"""
    st.markdown("# 🗺️ Journey Maps")
    st.markdown("Current state (pain) vs Future state (delight)")
    st.markdown("---")
    
    journey_data = load_journey_maps()
    
    # Toggle between current and future state
    view_mode = st.radio(
        "Select View:", 
        ["Current State (Pain)", "Future State (Delight)", "Side-by-Side Comparison"],
        horizontal=True
    )
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    if view_mode == "Current State (Pain)":
        st.markdown("## 😔 Current State Journey")
        st.markdown("*What users experience with existing productivity tools*")
        st.markdown("")
        
        for stage in journey_data['current_state']:
            render_journey_stage(stage, state="current")
    
    elif view_mode == "Future State (Delight)":
        st.markdown("## 😊 Future State Journey")
        st.markdown("*What users would experience with the proposed solution*")
        st.markdown("")
        
        for stage in journey_data['future_state']:
            render_journey_stage(stage, state="future")
    
    else:  # Side-by-Side Comparison
        st.markdown("## ⚖️ Side-by-Side Comparison")
        
        max_stages = max(len(journey_data['current_state']), len(journey_data['future_state']))
        
        for i in range(max_stages):
            col1, col2 = st.columns(2)
            
            with col1:
                if i < len(journey_data['current_state']):
                    st.markdown("### Current State")
                    render_journey_stage(journey_data['current_state'][i], state="current")
            
            with col2:
                if i < len(journey_data['future_state']):
                    st.markdown("### Future State")
                    render_journey_stage(journey_data['future_state'][i], state="future")
            
            if i < max_stages - 1:
                st.markdown("---")

def render_key_insights_page():
    """Render key insights page"""
    st.markdown("# 💡 Key Insights")
    st.markdown("Synthesized findings from research")
    st.markdown("---")
    
    insights_data = load_insights()
    
    # Counter-Intuitive Insights
    st.markdown("## 🔮 Counter-Intuitive Insights")
    st.markdown("*Findings that challenge conventional wisdom*")
    
    for insight in KEY_INSIGHTS:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='color: white; margin-top: 0;'>✨ {insight['insight']}</h3>
            <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 5px; margin-top: 1rem;'>
                <strong>Evidence:</strong> {insight['evidence']}
            </div>
            <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 5px; margin-top: 0.5rem;'>
                <strong>💡 Implication:</strong> {insight['implication']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Detailed Insights
    st.markdown("## 📊 Detailed Insights")
    
    for insight in insights_data['key_insights']:
        render_insight_card(insight)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Behavioral Patterns
    st.markdown("## 🔄 Behavioral Patterns")
    
    for pattern in insights_data['behavioral_patterns']:
        st.markdown(f"""
                    <div style='background: white; color: #333333; border: 2px solid #667eea; border-radius: 10px; padding: 1.5rem; margin-bottom: 1.5rem;'>
                    <h3 style='color: #667eea; margin-top: 0;'>{pattern['name']}</h3>
                    <p style='font-size: 1.05rem; color: #333333;'>{pattern['description']}</p>
                    <div style='background: #f8f9fa; color: #333333; padding: 1rem; border-radius: 5px; margin-top: 1rem;'>
                    <strong>Prevalence:</strong> {pattern['prevalence']}<br>
                    <strong>Root Cause:</strong> {pattern['root_cause']}
                    </div>
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Critical Moments
    st.markdown("## ⚡ Critical Moments")
    st.markdown("*Key decision points that determine success or failure*")
    
    for moment in insights_data['critical_moments']:
        importance_color = {"Critical": "#dc3545", "High": "#ff9800", "Medium": "#ffc107"}
        color = importance_color.get(moment['importance'], "#6c757d")
        
        st.markdown(f"""
                    <div style='border-left: 5px solid {color}; background: white; color: #333333; padding: 1.5rem; border-radius: 5px; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                    <h4 style='margin: 0; color: {color};'>{moment['moment']}</h4>
                    <span style='background: {color}; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem;'>{moment['importance']}</span>
                    </div>
                    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;'>
                    <div>
                    <strong>❌ Current Outcome:</strong><br>
                    {moment['current_outcome']}
                    </div>
                    <div>
                    <strong>✅ Desired Outcome:</strong><br>
                    {moment['desired_outcome']}
                    </div>
                    </div>
                    <div style='background: #e7f3ff; color: #333333; padding: 1rem; border-radius: 5px; margin-top: 1rem;'>
                    <strong>🔧 Intervention:</strong> {moment['intervention']}<br>
                    <strong>📊 Success Metric:</strong> {moment['success_metric']}
                    </div>
                    </div>
                """, unsafe_allow_html=True)

def render_prd_page():
    """Render PRD page"""
    st.markdown("# 📄 Product Requirements Document")
    st.markdown("Progressive Productivity Tool: Reducing First-14-Day Abandonment")
    st.markdown("---")
    
    # PRD Header
    st.markdown("## 📋 Document Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Product Name:** Progressive Productivity Tool  
        **Version:** 1.0  
        **Author:** Ayush saxena  
        **Date:** January 2026  
        **Status:** Research-Based Proposal
        """)
    
    with col2:
        st.markdown("""
        **Target Users:** Students & Young Professionals (18-28)  
        **Problem:** 64% abandon productivity tools by Day 14  
        **Solution:** Progressive onboarding + Task visibility limits  
        **Goal:** Improve Day-14 retention from 18% to 38%
        """)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Problem Statement
    st.markdown("## 🎯 Problem Statement")
    
    st.markdown("""
    <div style='background: #fff3cd; padding: 2rem; border-radius: 10px; border-left: 5px solid #ffc107;'>
        <h3 style='margin-top: 0; color: #856404;'>The Problem</h3>
        <p style='font-size: 1.1rem; color: #333; margin-bottom: 0;'>
            Students and young professionals abandon productivity tools within the first 14 days because 
            <strong>initial setup complexity and task visibility creates cognitive overload and guilt</strong>, 
            leading to an 82% abandonment rate.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Evidence")
    st.markdown("""
    - 64% of users abandon before Day 14 (industry baseline: 82% eventually abandon)
    - 82% cite "too complicated" as primary reason
    - 73% spend 2-4 hours on setup before seeing any value
    - 68% experience guilt from incomplete tasks
    - 18% Day-14 retention (industry baseline)
    """)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Solution Overview
    st.markdown("## 💡 Solution Overview")
    
    st.markdown("""
    A productivity tool that **starts minimal and grows progressively**, addressing the root causes of abandonment:
    
    1. **< 2-Minute Onboarding:** Guided setup ending with one completed task
    2. **3-Task Visibility Limit:** Enforced focus, prevents overwhelm
    3. **Progressive Feature Disclosure:** Unlock features based on usage patterns
    4. **Anti-Guilt Design:** No overdue badges, focus on wins not failures
    5. **Context-Aware Intelligence:** Adapt UI to time/location/calendar
    """)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # User Stories
    st.markdown("## 📖 User Stories")
    
    user_stories = [
        {
            "as": "A new user",
            "want": "Complete onboarding in under 2 minutes",
            "so": "I can see value immediately without feeling overwhelmed",
            "priority": "P0",
            "acceptance_criteria": [
                "Onboarding consists of exactly 3 steps",
                "Step 1: 'What's your first task today?' (30 sec max)",
                "Step 2: Help complete that task (2 min max)",
                "Step 3: Celebrate completion + prompt for next task (30 sec)",
                "Total time: < 2 minutes measured",
                "90% of users complete onboarding"
            ]
        },
        {
            "as": "An active user",
            "want": "See only 3 tasks at a time",
            "so": "I can focus without feeling overwhelmed by my entire task list",
            "priority": "P0",
            "acceptance_criteria": [
                "Default view shows max 3 tasks",
                "Completed tasks auto-hide after celebration",
                "New task addition only after completing one (or explicit 'show more')",
                "Users can override limit but with clear warning",
                "Task completion rate > 60% (vs 22% baseline)"
            ]
        },
        {
            "as": "A returning user",
            "want": "Be greeted positively when I come back after absence",
            "so": "I don't feel guilty about not using the app",
            "priority": "P0",
            "acceptance_criteria": [
                "No 'overdue task' concept exists",
                "Welcome message: 'Welcome back! Ready to start?' not punishment",
                "Show completed tasks from last session, not incomplete",
                "No red badges or alarming notifications",
                "Self-reported stress score < 4/10"
            ]
        },
        {
            "as": "A growing user",
            "want": "Unlock features gradually as I use the tool",
            "so": "I'm not overwhelmed by options I don't understand yet",
            "priority": "P1",
            "acceptance_criteria": [
                "Week 1: Only task add/complete visible",
                "Week 2: Tags unlock (if 5+ tasks completed)",
                "Week 3: Projects unlock (if tags used)",
                "Feature discovery is contextual, never forced",
                "Average active features < 7 for 70% of users"
            ]
        },
        {
            "as": "A first-day user",
            "want": "Complete at least one task in my first session",
            "so": "I feel successful and want to return",
            "priority": "P0",
            "acceptance_criteria": [
                "Onboarding MUST end with one completed task",
                "Celebration moment triggers (confetti/positive message)",
                "Immediate prompt: 'Great! What's next?'",
                "90% complete 1+ task in first session",
                "Day-1 completion predicts 2.5x better retention"
            ]
        }
    ]
    
    for i, story in enumerate(user_stories, 1):
        # Define colors
        # P0 = Red Border / Light Red Background (#ffebee)
        # P1/P2 = Orange/Yellow Border / Light Yellow Background (#fff3cd)
        color_map = {
            "P0": {"main": "#dc3545", "light_bg": "#ffebee"},
            "P1": {"main": "#ff9800", "light_bg": "#fff3cd"},
            "P2": {"main": "#ffc107", "light_bg": "#fff3cd"}
        }
        
        # Get colors for this story
        colors = color_map.get(story['priority'], {"main": "#6c757d", "light_bg": "#ffffff"})
        
        st.markdown(f"""
        <div style='border: 2px solid {colors['main']}; background: {colors['light_bg']}; color: #333333; border-radius: 10px; padding: 1.5rem; margin-bottom: 1.5rem;'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; width: 100%;'>
                <h4 style='margin: 0; color: #333333;'>Story #{i}</h4>
                <span style='background: {colors['main']}; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem;'>{story['priority']}</span>
            </div>
            <p style='font-size: 1.05rem; margin-bottom: 1rem; color: #333333;'>
                <strong>As</strong> {story['as']},<br>
                <strong>I want</strong> {story['want']},<br>
                <strong>So that</strong> {story['so']}
            </p>
            <div style='background: #f8f9fa; color: #333333; padding: 1rem; border-radius: 5px; border: 1px solid rgba(0,0,0,0.05);'>
                <strong>Acceptance Criteria:</strong>
                <ul style='margin-top: 0.5rem; margin-bottom: 0;'>
                    {''.join([f'<li>{ac}</li>' for ac in story['acceptance_criteria']])}
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Success Metrics
    st.markdown("## 📊 Success Metrics")
    
    metrics_data = pd.DataFrame([
        {
            "Metric": "Day 14 Retention",
            "Baseline": "18%",
            "Target": "38%",
            "Improvement": "+20pp",
            "Priority": "Primary"
        },
        {
            "Metric": "Time to First Win",
            "Baseline": "180 min",
            "Target": "< 5 min",
            "Improvement": "97% reduction",
            "Priority": "Primary"
        },
        {
            "Metric": "Task Completion Rate",
            "Baseline": "22%",
            "Target": "55%",
            "Improvement": "+150%",
            "Priority": "Secondary"
        },
        {
            "Metric": "Self-Reported Stress",
            "Baseline": "6.8/10",
            "Target": "3.2/10",
            "Improvement": "-53%",
            "Priority": "Secondary"
        },
        {
            "Metric": "Day 7 Retention",
            "Baseline": "35%",
            "Target": "60%",
            "Improvement": "+25pp",
            "Priority": "Secondary"
        }
    ])
    
    st.dataframe(metrics_data, use_container_width=True, hide_index=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Product Recommendations
    st.markdown("## 🔧 Product Recommendations")
    
    insights_data = load_insights()
    
    for rec in insights_data['product_recommendations']:
        priority_color = {
            "P0 (Critical)": "#dc3545",
            "P1 (High)": "#ff9800",
            "P2 (Medium)": "#ffc107"
        }
        color = priority_color.get(rec['priority'], "#6c757d")
        
        st.markdown(f"""
        <div style='border-left: 5px solid {color}; background: white; color: #333333; padding: 1.5rem; border-radius: 5px; margin-bottom: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                <h4 style='margin: 0; color: {color};'>{rec['title']}</h4>
                <span style='background: {color}; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem;'>{rec['priority']}</span>
            </div>
            <p style='font-size: 1.05rem; color: #333333;'>{rec['description']}</p>
            <div style='background: #f8f9fa; color: #333333; padding: 1rem; border-radius: 5px; margin-top: 1rem; margin-bottom: 1rem;'>
                <strong>Rationale:</strong> {rec['rationale']}
            </div>
            <div style='background: #e7f3ff; color: #333333; padding: 1rem; border-radius: 5px;'>
                <strong>📈 Expected Impact:</strong> {rec['expected_impact']}<br>
                <strong>📊 Success Metric:</strong> {rec['success_metric']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Out of Scope
    st.markdown("## 🚫 Out of Scope (V1)")
    
    st.markdown("""
    The following features are intentionally excluded from V1 to maintain simplicity:
    
    - Team collaboration / shared workspaces
    - Advanced automation / AI features
    - Calendar integration (beyond context awareness)
    - File attachments
    - Subtasks / hierarchical structures
    - Custom themes / extensive personalization
    - Native integrations (Slack, email, etc.)
    - Time tracking / Pomodoro timer
    
    **Rationale:** Feature richness contributes to abandonment. V1 focuses exclusively on solving the abandonment problem.
    """)

def render_impact_metrics_page():
    """Render impact and metrics page"""
    st.markdown("# 📊 Impact & Success Metrics")
    st.markdown("Expected outcomes and business impact")
    st.markdown("---")
    
    # North Star Metric
    st.markdown("## 🌟 North Star Metric")
    
    st.markdown("""
<style>
@keyframes rise {
0% { bottom: -10px; opacity: 0; transform: translateX(0) rotate(0deg); }
50% { opacity: 0.5; }
100% { bottom: 100%; opacity: 0; transform: translateX(-20px) rotate(45deg); }
}
.star-anim {
position: absolute;
color: white;
font-weight: bold;
animation: rise infinite ease-in;
z-index: 1;
user-select: none;
}
</style>
<div style="position: relative; overflow: hidden; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 3rem; border-radius: 15px; text-align: center; box-shadow: 0 6px 12px rgba(0,0,0,0.15); margin-bottom: 2rem;">

<div class="star-anim" style="font-size: 14px; left: 10%; animation-duration: 4s; animation-delay: 0s;">★</div>
<div class="star-anim" style="font-size: 18px; left: 20%; animation-duration: 7s; animation-delay: 1s;">★</div>
<div class="star-anim" style="font-size: 12px; left: 35%; animation-duration: 5s; animation-delay: 2s;">★</div>
<div class="star-anim" style="font-size: 20px; left: 50%; animation-duration: 8s; animation-delay: 0.5s;">★</div>
<div class="star-anim" style="font-size: 15px; left: 65%; animation-duration: 6s; animation-delay: 3s;">★</div>
<div class="star-anim" style="font-size: 18px; left: 80%; animation-duration: 5s; animation-delay: 1.5s;">★</div>
<div class="star-anim" style="font-size: 12px; left: 90%; animation-duration: 9s; animation-delay: 2.5s;">★</div>
<div class="star-anim" style="font-size: 16px; left: 15%; animation-duration: 6s; animation-delay: 4s;">★</div>
<div class="star-anim" style="font-size: 14px; left: 45%; animation-duration: 5s; animation-delay: 3.5s;">★</div>
<div class="star-anim" style="font-size: 22px; left: 75%; animation-duration: 7s; animation-delay: 1s;">★</div>

<div style="position: relative; z-index: 10;">
<div style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 1rem;">North Star Metric</div>
<div style="font-size: 4rem; font-weight: bold; margin-bottom: 0.5rem;">Day 14 Retention</div>
<div style="font-size: 1.5rem; display: flex; justify-content: center; align-items: center; gap: 1rem; margin-top: 1rem;">
<span style="background: rgba(255, 75, 75, 0.2); color: #ff4b4b; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">18% baseline</span>
<span>→</span>
<span style="background: rgba(33, 195, 84, 0.2); color: #4ade80; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">38% target</span>
</div>
<div style="font-size: 2.5rem; margin-top: 1.5rem; font-weight: bold;">+20 percentage points</div>
</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("### Why Day 14 Retention?")
    st.markdown("""
    - 64% of users make abandonment decision by Day 14
    - Predicts long-term retention (90-day, 180-day)
    - Directly addresses root cause (early cognitive overload)
    - Measurable within 2 weeks of launch
    - Industry-standard metric for habit-forming products
    """)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Metrics Dashboard
    st.markdown("## 📈 Key Metrics Dashboard")
    
    metrics = SUCCESS_METRICS
    
    # Primary Metric
    st.markdown("### Primary Metric")
    
    primary = metrics['primary']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Baseline", f"{primary['baseline']*100:.0f}%")
    with col2:
        st.metric("Target", f"{primary['target']*100:.0f}%", 
                 delta=f"+{(primary['target']-primary['baseline'])*100:.0f}pp",
                 delta_color="normal")
    with col3:
        improvement = ((primary['target'] - primary['baseline']) / primary['baseline']) * 100
        st.metric("Improvement", f"+{improvement:.0f}%")
    
    st.progress(primary['target'])
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Secondary Metrics
    st.markdown("### Secondary Metrics")
    
    secondary_df = pd.DataFrame([
        {
            "Metric": m['name'],
            "Baseline": m['baseline'],
            "Target": m['target'],
            "Measurement": m['description']
        }
        for m in metrics['secondary']
    ])
    
    st.dataframe(secondary_df, use_container_width=True, hide_index=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Funnel Analysis
    st.markdown("## 🔽 User Funnel Analysis")
    
    st.markdown("### Current State vs Target State")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Current State (Baseline)")
        funnel_current = create_funnel_chart(
            stages=["Signup", "Day 1 Active", "Day 7 Active", "Day 14 Active", "Day 30 Active"],
            values=[100, 75, 35, 18, 12],
            title="Current User Funnel"
        )
        st.plotly_chart(funnel_current, use_container_width=True)
    
    with col2:
        st.markdown("#### Target State (With Solution)")
        funnel_target = create_funnel_chart(
            stages=["Signup", "Day 1 Active", "Day 7 Active", "Day 14 Active", "Day 30 Active"],
            values=[100, 90, 60, 38, 25],
            title="Target User Funnel"
        )
        st.plotly_chart(funnel_target, use_container_width=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Business Impact
    st.markdown("## 💼 Business Impact")
    
    st.markdown("""
    Improving Day-14 retention from 18% to 38% creates significant downstream business value:
    """)
    
    impact_data = pd.DataFrame({
        'Metric': [
            'Day 30 Retention',
            'Day 90 Retention',
            'Average LTV per User',
            'Organic Referral Rate',
            'Support Ticket Volume'
        ],
        'Baseline': ['12%', '8%', '$15', '5%', '100 tickets/week'],
        'Target': ['25%', '20%', '$45', '15%', '40 tickets/week'],
        'Improvement': ['+108%', '+150%', '+200%', '+200%', '-60%'],
        'Business Value': [
            '2x more retained users',
            'Sustainable growth',
            '3x lifetime value',
            'Viral coefficient > 1',
            'Reduced support costs'
        ]
    })
    
    st.dataframe(impact_data, use_container_width=True, hide_index=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Measurement Plan
    st.markdown("## 📏 Measurement Plan")
    
    st.markdown("### Data Collection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Quantitative:**
        - User analytics (signup, sessions, task completion)
        - Retention cohorts (Day 1, 7, 14, 30, 90)
        - Feature usage tracking
        - Time-to-first-win measurement
        - Funnel drop-off analysis
        """)
    
    with col2:
        st.markdown("""
        **Qualitative:**
        - Post-task completion micro-surveys
        - Weekly NPS surveys
        - Exit surveys for churned users
        - User interview program (ongoing)
        - Support ticket sentiment analysis
        """)
    
    st.markdown("### Testing Plan")
    
    st.markdown("""
    **Phase 1: Alpha (Weeks 1-2)**
    - 50 users from target demographic
    - Heavy instrumentation and feedback loops
    - Daily check-ins with users
    - Rapid iteration on friction points
    
    **Phase 2: Beta (Weeks 3-6)**
    - 500 users, randomized to control/treatment
    - A/B test: Progressive onboarding vs traditional
    - Measure Day-14 retention delta
    - Collect qualitative feedback
    
    **Phase 3: Launch (Week 7+)**
    - Full rollout if Day-14 retention > 30%
    - Continue monitoring and optimization
    - Iterate based on user feedback
    """)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Success Criteria
    st.markdown("## ✅ Success Criteria")
    
    st.markdown("""
    **This project is successful if:**
    
    1. ✅ **Primary:** Day-14 retention improves to ≥ 35% (stretch goal: 38%)
    2. ✅ **Secondary:** 90%+ of users complete 1 task in first session
    3. ✅ **Secondary:** Self-reported stress score < 4/10
    4. ✅ **Tertiary:** NPS score > 30 (promoters > detractors)
    
    **This project has failed if:**
    
    1. ❌ Day-14 retention < 20% (no meaningful improvement)
    2. ❌ Users report feeling "just as overwhelmed" as before
    3. ❌ Retention improvements come at cost of engagement quality
    4. ❌ Solution increases complexity despite intentions
    """)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Next Steps
    st.markdown("## 🚀 Next Steps")
    
    st.markdown("""
    **If This Were a Real Product:**
    
    1. **Validate with Prototype (2 weeks)**
       - Build clickable Figma prototype
       - Test with 20 users from target demographic
       - Validate core assumptions
    
    2. **Build MVP (6 weeks)**
       - Progressive onboarding flow
       - 3-task visibility limit
       - Anti-guilt design elements
       - Basic analytics
    
    3. **Alpha Test (2 weeks)**
       - 50 users, heavy feedback
       - Daily iteration
       - Refine UX based on real usage
    
    4. **Beta Test (4 weeks)**
       - 500 users, A/B test vs control
       - Measure Day-14 retention
       - Statistical significance validation
    
    5. **Launch Decision (Week 15)**
       - Go/No-Go based on beta results
       - If successful: Full rollout
       - If unsuccessful: Iterate or pivot
    """)
    
    st.success("💡 **Portfolio Note:** This is a research project demonstrating PM skills in user research, synthesis, and product specification—not a startup pitch.")

# ===== MAIN APP =====
def main():
    """Main application logic"""
    
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Route to appropriate page
    if page == "🏠 Home":
        render_home_page()
    elif page == "🔍 Research Process":
        render_research_process_page()
    elif page == "💬 Interview Insights":
        render_interview_insights_page()
    elif page == "🗂️ Affinity Mapping":
        render_affinity_mapping_page()
    elif page == "👥 User Personas":
        render_personas_page()
    elif page == "🗺️ Journey Maps":
        render_journey_maps_page()
    elif page == "💡 Key Insights":
        render_key_insights_page()
    elif page == "📄 Product Requirements":
        render_prd_page()
    elif page == "📊 Impact & Metrics":
        render_impact_metrics_page()

if __name__ == "__main__":
    main()

# --- FOOTER ---
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 20px;'>
        <p>📊 <strong>User Research Product Spec</strong> - Reducing Productivity Tool Abandonment</p>
        <p>Built with Python, Streamlit, Plotly, Pandas & Numpy <strong>| Last Updated:</strong> {}</p>
        <p>© 2026 <strong>Ayush Saxena</strong>. All rights reserved.</p>
    </div>
""".format(datetime.now().strftime("%d-%b-%Y At %I:%M %p")), unsafe_allow_html=True)