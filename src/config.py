"""
Configuration file for User Research Project
Author: Ayush Saxena
Date: January 2026
"""

import os
from pathlib import Path
from datetime import datetime

# ===== PROJECT ROOT =====
PROJECT_ROOT = Path(__file__).parent.parent

# ===== DIRECTORY PATHS =====
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SYNTHETIC_DATA_DIR = DATA_DIR / "synthetic"

INTERVIEW_DIR = RAW_DATA_DIR / "interview_transcripts"
PRD_DIR = PROJECT_ROOT / "prd"
ASSETS_DIR = PROJECT_ROOT / "assets"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
REPORTS_DIR = OUTPUTS_DIR / "reports"

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, SYNTHETIC_DATA_DIR, 
                  INTERVIEW_DIR, PRD_DIR, ASSETS_DIR, FIGURES_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ===== RESEARCH PARAMETERS =====
NUM_INTERVIEWS = 22  # Total interviews conducted
INTERVIEW_DURATION_MIN = 30  # Minimum interview duration (minutes)
INTERVIEW_DURATION_MAX = 45  # Maximum interview duration (minutes)

# ===== USER PERSONAS =====
PERSONA_DEFINITIONS = {
    "The Overwhelmed Optimizer": {
        "age_range": "21-25",
        "occupation": "Engineering student / Young professional",
        "behavior": "Downloads every productivity app, abandons within 2 weeks",
        "pain": "Spends more time organizing than doing",
        "frequency": 0.40  # 40% of interviewees
    },
    "The Serial Abandoner": {
        "age_range": "18-22",
        "occupation": "College student",
        "behavior": "Starts strong with new tools, stops using within days",
        "pain": "Guilt from seeing incomplete tasks",
        "frequency": 0.35  # 35% of interviewees
    },
    "The Analog Holdout": {
        "age_range": "23-28",
        "occupation": "Creative professional / Graduate student",
        "behavior": "Prefers pen and paper, tried digital but reverted",
        "pain": "Digital tools feel too cold and rigid",
        "frequency": 0.25  # 25% of interviewees
    }
}

# ===== PAIN POINTS (From Research) =====
PAIN_POINTS = [
    {
        "theme": "Feature Overwhelm",
        "description": "Tools have 100+ features but users only need 5-10",
        "severity": "Critical",
        "frequency": 0.82,  # 82% of users mentioned
        "quotes": [
            "I spend hours trying to figure out which template to use",
            "There are so many buttons and options, I don't know where to start"
        ]
    },
    {
        "theme": "Productivity Guilt",
        "description": "Seeing uncompleted tasks causes stress and anxiety",
        "severity": "High",
        "frequency": 0.68,
        "quotes": [
            "Every time I open the app, I feel bad about myself",
            "The red badges on incomplete tasks make me want to delete the app"
        ]
    },
    {
        "theme": "Setup Fatigue",
        "description": "Takes 2-4 hours to set up, users give up before seeing value",
        "severity": "Critical",
        "frequency": 0.73,
        "quotes": [
            "I watched 3 YouTube tutorials and still couldn't get it right",
            "By the time I set it up, I lost motivation to actually use it"
        ]
    },
    {
        "theme": "Context Switching",
        "description": "Tools don't adapt to different life contexts (work/personal/study)",
        "severity": "Medium",
        "frequency": 0.55,
        "quotes": [
            "I need different systems for work and personal life",
            "My brain works differently at work vs home, but the tool doesn't"
        ]
    },
    {
        "theme": "Difficulty Prioritizing",
        "description": "Users don't know what to focus on when faced with long task lists",
        "severity": "High",
        "frequency": 0.64,
        "quotes": [
            "I have 50 tasks and no idea which one to start with",
            "Everything feels equally important and equally urgent"
        ]
    }
]

# ===== KEY INSIGHTS (Counter-Intuitive) =====
KEY_INSIGHTS = [
    {
        "insight": "Users don't want more features—they want less cognitive load",
        "evidence": "82% abandoned tools citing 'too complicated' as primary reason",
        "implication": "Progressive disclosure > Feature richness"
    },
    {
        "insight": "Tool abandonment happens in first 14 days, not gradually",
        "evidence": "Average abandonment: 12.3 days. 64% abandoned before Day 14",
        "implication": "First 2 weeks are critical—optimize for early wins"
    },
    {
        "insight": "Users blame themselves, not the tool",
        "evidence": "73% said 'I'm just not disciplined enough to use it'",
        "implication": "Design must prevent self-blame and guilt"
    },
    {
        "insight": "Fewer features = Higher completion rate",
        "evidence": "Users with 5-7 features active completed 3x more tasks than those with 20+",
        "implication": "Constrain choices to drive action"
    },
    {
        "insight": "Users need 'quick wins' in first 24 hours",
        "evidence": "Users who completed 1 task in Day 1 had 2.5x better Day 14 retention",
        "implication": "Time-to-first-win is the most critical metric"
    }
]

# ===== AFFINITY MAPPING THEMES =====
AFFINITY_THEMES = [
    "Feature Overwhelm",
    "Productivity Guilt", 
    "Setup Fatigue",
    "Context Switching",
    "Prioritization Difficulty",
    "Tool Hopping Behavior",
    "Social Comparison Anxiety",
    "Lack of Flexibility"
]

# ===== JOURNEY MAP STAGES =====
JOURNEY_STAGES = {
    "current_state": [
        {
            "stage": "Discovery",
            "action": "Hears about productivity tool from friend/YouTube",
            "emotion": "😊 Excited",
            "pain": "Overwhelmed by options (Notion vs Todoist vs Trello)",
            "touchpoint": "Social media, YouTube tutorials"
        },
        {
            "stage": "Signup",
            "action": "Creates account, sees empty workspace",
            "emotion": "😐 Neutral",
            "pain": "No guidance on where to start",
            "touchpoint": "Onboarding flow"
        },
        {
            "stage": "Setup",
            "action": "Spends 2-3 hours creating perfect system",
            "emotion": "😫 Frustrated",
            "pain": "Choice paralysis: templates, databases, tags, folders",
            "touchpoint": "Template gallery, tutorial videos"
        },
        {
            "stage": "Initial Use",
            "action": "Adds 20+ tasks, organizes by project/priority",
            "emotion": "😌 Hopeful",
            "pain": "Unclear which task to start with",
            "touchpoint": "Task list view"
        },
        {
            "stage": "Reality Check",
            "action": "Opens app after 2 days, sees 15 incomplete tasks",
            "emotion": "😔 Guilty",
            "pain": "Feels like failure, tool becomes reminder of incompletion",
            "touchpoint": "Push notifications, email reminders"
        },
        {
            "stage": "Abandonment",
            "action": "Stops opening app, returns to pen and paper",
            "emotion": "😞 Defeated",
            "pain": "Tool feels like burden, not help",
            "touchpoint": "Abandoned account"
        }
    ],
    "future_state": [
        {
            "stage": "Discovery",
            "action": "Hears about progressive productivity tool",
            "emotion": "😊 Curious",
            "delight": "Promise of 'no overwhelm' and 'quick setup'",
            "touchpoint": "Social media, word of mouth"
        },
        {
            "stage": "Signup",
            "action": "Creates account, sees 3 simple prompts",
            "emotion": "😌 Relieved",
            "delight": "No empty workspace anxiety, clear starting point",
            "touchpoint": "Guided onboarding (< 2 minutes)"
        },
        {
            "stage": "First Task",
            "action": "Adds first task, completes it in 5 minutes",
            "emotion": "😊 Accomplished",
            "delight": "Immediate win, positive reinforcement",
            "touchpoint": "Minimal task view (max 3 visible)"
        },
        {
            "stage": "Early Usage",
            "action": "Uses tool 3-5 times in first week",
            "emotion": "😃 Confident",
            "delight": "Tool adapts to behavior, reveals features gradually",
            "touchpoint": "Context-aware task suggestions"
        },
        {
            "stage": "Habit Formation",
            "action": "Completes 3+ tasks per week consistently",
            "emotion": "💪 Empowered",
            "delight": "Sees progress without guilt, tool feels helpful",
            "touchpoint": "Weekly reflection, wins highlighted"
        },
        {
            "stage": "Long-term",
            "action": "Integrated into daily workflow",
            "emotion": "😌 Calm",
            "delight": "Tool invisible, habits visible",
            "touchpoint": "Contextual intelligence, zero maintenance"
        }
    ]
}

# ===== SUCCESS METRICS =====
SUCCESS_METRICS = {
    "primary": {
        "name": "Day 14 Retention",
        "description": "% of users still active after 14 days",
        "baseline": 0.18,  # 18% industry average
        "target": 0.38,    # 38% target (20pp improvement)
        "measurement": "Users with 1+ action on Day 14"
    },
    "secondary": [
        {
            "name": "Time to First Win",
            "description": "Minutes to complete first meaningful task",
            "baseline": 180,  # 3 hours (current tools)
            "target": 5,      # 5 minutes
            "measurement": "Time from signup to first task completion"
        },
        {
            "name": "Task Completion Rate",
            "description": "% of users completing 3+ tasks in first week",
            "baseline": 0.22,
            "target": 0.55,
            "measurement": "Users with 3+ completed tasks by Day 7"
        },
        {
            "name": "Self-Reported Stress Score",
            "description": "User-reported stress level (1-10 scale)",
            "baseline": 6.8,
            "target": 3.2,
            "measurement": "Post-task completion survey"
        }
    ]
}

# ===== STREAMLIT CONFIGURATION =====
STREAMLIT_CONFIG = {
    "page_title": "User Research: Reducing Productivity Tool Abandonment",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# ===== COLOR SCHEME =====
COLORS = {
    "primary": "#1f77b4",      # Blue
    "secondary": "#ff7f0e",    # Orange
    "success": "#2ca02c",      # Green
    "danger": "#d62728",       # Red
    "warning": "#ff9800",      # Amber
    "info": "#17a2b8",         # Teal
    "light": "#f8f9fa",        # Light gray
    "dark": "#343a40"          # Dark gray
}

print(f"✅ Configuration loaded successfully")
print(f"📁 Project Root: {PROJECT_ROOT}")
print(f"📊 Total Interviews: {NUM_INTERVIEWS}")
print(f"👥 Personas: {len(PERSONA_DEFINITIONS)}")
print(f"💡 Key Insights: {len(KEY_INSIGHTS)}")