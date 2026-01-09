"""
Persona Builder Module
Creates detailed user personas from interview data
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from typing import Dict, List
from config import *

class PersonaBuilder:
    """
    Builds user personas from interview data and affinity mapping
    """
    
    def __init__(self):
        """Initialize persona builder"""
        self.personas = []
        
    def build_personas(self) -> List[Dict]:
        """
        Build complete personas with all details
        
        Returns:
            List of persona dictionaries
        """
        print("👥 Building user personas...")
        
        # Load interview metadata
        metadata_df = pd.read_csv(RAW_DATA_DIR / "interview_metadata.csv")
        
        # Load affinity clusters
        observations_df = pd.read_csv(PROCESSED_DATA_DIR / "affinity_clusters.csv")
        
        personas = []
        
        for persona_name, persona_data in PERSONA_DEFINITIONS.items():
            # Filter metadata for this persona
            persona_metadata = metadata_df[metadata_df['persona'] == persona_name]
            
            # Get observations from this persona's interviews
            interview_ids = persona_metadata['interview_id'].tolist()
            
            # --- FIX STARTS HERE ---
            # Create a normalized ID column to match "interview_01" to "INT_001"
            observations_df['normalized_id'] = observations_df['interview_id'].apply(
                lambda x: f"INT_{int(x.split('_')[1]):03d}"
            )
            
            persona_observations = observations_df[
                observations_df['normalized_id'].isin(interview_ids)
            ]
            # --- FIX ENDS HERE ---
            
            # Build complete persona
            persona = self._build_single_persona(
                persona_name, 
                persona_data, 
                persona_metadata,
                persona_observations
            )
            personas.append(persona)
        
        # Save personas
        self.personas = personas
        self._save_personas()
        
        print(f"✅ Built {len(personas)} personas")
        return personas
    
    def _build_single_persona(self, name: str, base_data: Dict, 
                             metadata: pd.DataFrame, observations: pd.DataFrame) -> Dict:
        """
        Build a single complete persona
        
        Args:
            name: Persona name
            base_data: Base persona data from config
            metadata: Filtered metadata for this persona
            observations: Filtered observations for this persona
            
        Returns:
            Complete persona dictionary
        """
        # Calculate statistics
        avg_age = int(metadata['age'].mean())
        avg_tools_abandoned = metadata['tools_abandoned'].mean()
        
        # Get top pain points for this persona
        top_themes = observations['theme'].value_counts().head(3)
        
        # Select representative quotes
        quotes = self._select_representative_quotes(observations)
        
        # Define goals and frustrations
        goals, frustrations = self._define_goals_frustrations(name)
        
        # Define typical day
        typical_day = self._define_typical_day(name)
        
        # Define tools currently used
        current_tools = self._define_current_tools(name)
        
        persona = {
            "name": name,
            "tagline": base_data["behavior"],
            "demographics": {
                "age": avg_age,
                "age_range": base_data["age_range"],
                "occupation": base_data["occupation"],
                "education": self._get_education(name),
                "location": "Urban area (Metro city)",
                "tech_savviness": self._get_tech_savviness(name)
            },
            "psychographics": {
                "personality": self._get_personality(name),
                "values": self._get_values(name),
                "attitudes": self._get_attitudes(name)
            },
            "behavioral_patterns": {
                "tool_usage": base_data["behavior"],
                "avg_tools_abandoned": round(avg_tools_abandoned, 1),
                "typical_abandonment_time": self._get_abandonment_time(name),
                "primary_pain": base_data["pain"]
            },
            "goals": goals,
            "frustrations": frustrations,
            "typical_day": typical_day,
            "current_tools": current_tools,
            "pain_points": [
                {"theme": theme, "mentions": count} 
                for theme, count in top_themes.items()
            ],
            "quotes": quotes,
            "needs": self._define_needs(name),
            "success_criteria": self._define_success_criteria(name)
        }
        
        return persona
    
    def _select_representative_quotes(self, observations: pd.DataFrame, n: int = 5) -> List[str]:
        """Select most representative quotes"""
        # Get negative sentiment quotes (they're most revealing)
        negative_obs = observations[observations['sentiment'] == 'negative']
        
        if len(negative_obs) >= n:
            return negative_obs.sample(n=n)['text'].tolist()
        else:
            return observations.sample(n=min(n, len(observations)))['text'].tolist()
    
    def _define_goals_frustrations(self, persona_name: str) -> tuple:
        """Define goals and frustrations for persona"""
        
        goals_map = {
            "The Overwhelmed Optimizer": [
                "Find the 'perfect' productivity system that works long-term",
                "Stop wasting time setting up tools and start actually doing work",
                "Feel in control of tasks without constant reorganization",
                "Use a tool that grows with needs without becoming overwhelming"
            ],
            "The Serial Abandoner": [
                "Build consistent habits without guilt when falling off track",
                "Complete tasks without feeling overwhelmed by long lists",
                "Get quick wins that motivate continued use",
                "Feel successful rather than judged by the tool"
            ],
            "The Analog Holdout": [
                "Find a digital tool that matches the flexibility of paper",
                "Reduce reliance on physical notebooks for shareable items",
                "Have a backup system that doesn't require daily maintenance",
                "Use technology when it adds value, not because 'I should'"
            ]
        }
        
        frustrations_map = {
            "The Overwhelmed Optimizer": [
                "Spends more time organizing than doing actual work",
                "Constantly second-guesses system setup and structure",
                "Feels like needs to watch hours of tutorials to use basic features",
                "Gets distracted by new 'better' tools and switches frequently"
            ],
            "The Serial Abandoner": [
                "Feels guilty seeing incomplete tasks pile up",
                "Gets overwhelmed by red notification badges and overdue items",
                "Loses motivation after missing a few days of use",
                "Blames self for 'not being disciplined enough'"
            ],
            "The Analog Holdout": [
                "Digital tools feel cold, rigid, and impersonal",
                "Too many clicks and menus to do simple things",
                "Can't doodle, cross out, or freely organize like on paper",
                "Forced into structures that don't match thinking style"
            ]
        }
        
        return goals_map[persona_name], frustrations_map[persona_name]
    
    def _define_typical_day(self, persona_name: str) -> str:
        """Define typical day for persona"""
        
        day_map = {
            "The Overwhelmed Optimizer": """
**Morning (7 AM - 9 AM):** Wakes up, checks productivity app, feels overwhelmed by yesterday's incomplete tasks. Spends 20 minutes reorganizing priorities and tags. Watches a YouTube video about a 'better' productivity system.

**Midday (12 PM - 2 PM):** Takes lunch break, researches new productivity tool recommended by a colleague. Downloads it, spends 30 minutes exploring features. Thinks about migrating from current tool.

**Evening (6 PM - 8 PM):** Opens current productivity app, sees mess of tasks across multiple projects. Spends an hour restructuring workspace with new database views. Completes only 1 of 5 planned tasks.

**Night (10 PM - 11 PM):** Feels unproductive despite working all day. Watches another tutorial about productivity systems. Plans to start fresh tomorrow with a 'better' setup.
        """,
            "The Serial Abandoner": """
**Morning (8 AM - 10 AM):** Opens productivity app excitedly (it's Day 3 of new system!). Sees 8 overdue tasks from yesterday. Feels immediate guilt. Closes app. Checks Instagram instead.

**Afternoon (2 PM - 4 PM):** Gets notification: "You have 12 overdue tasks!" Feels worse. Opens app briefly, adds 3 more tasks to the list. Doesn't complete any. Closes app again.

**Evening (7 PM - 9 PM):** Tries to use app again. List has grown to 15 tasks. Feels paralyzed—doesn't know where to start. Completes one easy task, but doesn't feel accomplished seeing 14 remaining.

**Night (11 PM):** Thinks "I'll do better tomorrow." Plans to wake up early and tackle the list. (Spoiler: Won't open app for 3 days after this.)
        """,
            "The Analog Holdout": """
**Morning (6 AM - 9 AM):** Morning coffee with physical journal. Writes down 3 tasks for the day using favorite pen. Feels grounded and clear-headed. Crosses out yesterday's completed tasks with satisfaction.

**Midday (1 PM - 3 PM):** Colleague sends shared Notion document. Opens app reluctantly. Feels lost in the interface. Copies relevant info to notebook. Closes Notion.

**Evening (5 PM - 7 PM):** Needs to share task list with team. Tries using digital tool. Gets frustrated with formatting. Takes photo of handwritten notes instead. Sends via email.

**Night (9 PM - 10 PM):** Reviews day in journal. Doodles thoughts and ideas. Feels satisfied. Briefly considers trying digital again but remembers the frustration. Sticks with paper.
        """
        }
        
        return day_map[persona_name].strip()
    
    def _define_current_tools(self, persona_name: str) -> List[str]:
        """Define current tools used by persona"""
        
        tools_map = {
            "The Overwhelmed Optimizer": [
                "Currently: Notion (3rd week, considering switching)",
                "Previously: Todoist, Trello, Asana, ClickUp, Obsidian",
                "Also uses: Multiple YouTube channels, Reddit r/productivity",
                "Phone: 15+ productivity apps downloaded (uses 2)"
            ],
            "The Serial Abandoner": [
                "Currently: Google Keep (basic, no pressure)",
                "Abandoned: Notion (2 weeks), Todoist (1 week), Trello (3 days)",
                "Sometimes: Apple Reminders (when guilt is low)",
                "Mostly: Mental notes and hoping for the best"
            ],
            "The Analog Holdout": [
                "Primary: Physical journal/notebook (Moleskine or similar)",
                "Backup: Sticky notes, index cards",
                "Forced to use: Google Docs (for team collaboration)",
                "Tried and abandoned: Notion, Evernote, OneNote"
            ]
        }
        
        return tools_map[persona_name]
    
    def _define_needs(self, persona_name: str) -> List[str]:
        """Define what persona needs from solution"""
        
        needs_map = {
            "The Overwhelmed Optimizer": [
                "Progressive onboarding—start simple, add complexity gradually",
                "Clear guidance on 'correct' way to set up (reduce decision fatigue)",
                "Built-in constraints to prevent over-organization",
                "Focus on doing, not organizing"
            ],
            "The Serial Abandoner": [
                "Gentle re-engagement when returning after absence",
                "No guilt-inducing notifications or overdue badges",
                "Quick wins within first session",
                "Limits on task adding (prevent overcommitment)"
            ],
            "The Analog Holdout": [
                "Flexibility—no forced structures or templates",
                "Simple, minimal interface (less is more)",
                "Option to use alongside paper (not replacement)",
                "Fast, frictionless task entry"
            ]
        }
        
        return needs_map[persona_name]
    
    def _define_success_criteria(self, persona_name: str) -> List[str]:
        """Define what success looks like for this persona"""
        
        success_map = {
            "The Overwhelmed Optimizer": [
                "Uses same tool for 3+ months without switching",
                "Spends <10 minutes per day on organization",
                "Completes 70%+ of planned tasks",
                "Feels tool is 'good enough' (stops searching for perfect)"
            ],
            "The Serial Abandoner": [
                "Still using tool after 30 days (key milestone)",
                "Opens app without feeling guilt or dread",
                "Completes 3+ tasks per week consistently",
                "Feels successful even with imperfect adherence"
            ],
            "The Analog Holdout": [
                "Uses digital tool for specific use cases (sharing, reminders)",
                "Doesn't feel forced to abandon paper entirely",
                "Tool integrates seamlessly with notebook workflow",
                "Minimal time spent in digital tool (efficiency)"
            ]
        }
        
        return success_map[persona_name]
    
    def _get_education(self, persona_name: str) -> str:
        """Get education level for persona"""
        education_map = {
            "The Overwhelmed Optimizer": "Bachelor's in Engineering/Computer Science (current or recent grad)",
            "The Serial Abandoner": "Undergraduate student (2nd-3rd year)",
            "The Analog Holdout": "Bachelor's in Design/Arts or Master's student"
        }
        return education_map[persona_name]
    
    def _get_tech_savviness(self, persona_name: str) -> str:
        """Get tech savviness rating"""
        tech_map = {
            "The Overwhelmed Optimizer": "High (7/10) - Comfortable with tech but overwhelmed by options",
            "The Serial Abandoner": "Medium (5/10) - Can use apps but doesn't explore deeply",
            "The Analog Holdout": "Medium-Low (4/10) - Prefers simplicity over features"
        }
        return tech_map[persona_name]
    
    def _get_personality(self, persona_name: str) -> str:
        """Get personality traits"""
        personality_map = {
            "The Overwhelmed Optimizer": "Perfectionist, analytical, detail-oriented, self-critical",
            "The Serial Abandoner": "Enthusiastic starter, easily discouraged, seeks validation",
            "The Analog Holdout": "Creative, tactile, traditional, values simplicity"
        }
        return personality_map[persona_name]
    
    def _get_values(self, persona_name: str) -> List[str]:
        """Get core values"""
        values_map = {
            "The Overwhelmed Optimizer": [
                "Efficiency and optimization",
                "Continuous improvement",
                "Being organized and prepared",
                "Making data-driven decisions"
            ],
            "The Serial Abandoner": [
                "Authenticity and self-acceptance",
                "Progress over perfection",
                "Flexibility and adaptability",
                "Kindness to self"
            ],
            "The Analog Holdout": [
                "Craftsmanship and quality",
                "Simplicity and minimalism",
                "Tangible experiences",
                "Personal touch"
            ]
        }
        return values_map[persona_name]
    
    def _get_attitudes(self, persona_name: str) -> List[str]:
        """Get attitudes toward productivity tools"""
        attitudes_map = {
            "The Overwhelmed Optimizer": [
                "Believes the 'right' tool will solve everything",
                "Thinks needs to use advanced features to be productive",
                "Feels pressure to optimize every aspect of life",
                "Afraid of missing out on better systems"
            ],
            "The Serial Abandoner": [
                "Wants to be organized but doubts own discipline",
                "Blames self when tools don't work",
                "Skeptical of own ability to maintain habits",
                "Hopeful that 'this time will be different'"
            ],
            "The Analog Holdout": [
                "Believes digital lacks soul and authenticity",
                "Values quality over quantity of tools",
                "Skeptical of tech-driven productivity culture",
                "Trusts own methods over trendy solutions"
            ]
        }
        return attitudes_map[persona_name]
    
    def _get_abandonment_time(self, persona_name: str) -> str:
        """Get typical abandonment timeline"""
        time_map = {
            "The Overwhelmed Optimizer": "2-3 weeks (then switches to new tool)",
            "The Serial Abandoner": "5-10 days (returns to basics or nothing)",
            "The Analog Holdout": "2-7 days (returns to paper)"
        }
        return time_map[persona_name]
    
    def _save_personas(self) -> None:
        """Save personas to JSON file"""
        output_file = PROCESSED_DATA_DIR / "personas.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.personas, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved personas to: {output_file}")

if __name__ == "__main__":
    print("="*60)
    print("PERSONA BUILDER")
    print("="*60)
    print()
    
    builder = PersonaBuilder()
    personas = builder.build_personas()
    
    print("\n" + "="*60)
    print("Persona Summary:")
    print("="*60)
    
    for persona in personas:
        print(f"\n{persona['name']}")
        print(f"  Tagline: {persona['tagline']}")
        print(f"  Age: {persona['demographics']['age']}")
        print(f"  Tools Abandoned: {persona['behavioral_patterns']['avg_tools_abandoned']}")
        print(f"  Primary Pain: {persona['behavioral_patterns']['primary_pain']}")