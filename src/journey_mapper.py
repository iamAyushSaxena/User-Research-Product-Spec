"""
Journey Mapping Module
Creates current state and future state journey maps
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List
from config import *

class JourneyMapper:
    """
    Creates detailed journey maps for user experience
    """
    
    def __init__(self):
        """Initialize journey mapper"""
        self.journey_maps = {}
        
    def create_journey_maps(self) -> Dict:
        """
        Create both current and future state journey maps
        
        Returns:
            Dictionary with current and future state maps
        """
        print("🗺️ Creating journey maps...")
        
        self.journey_maps = {
            "current_state": self._create_detailed_current_state(),
            "future_state": self._create_detailed_future_state()
        }
        
        # Save to file
        self._save_journey_maps()
        
        print(f"✅ Created journey maps (Current + Future state)")
        return self.journey_maps
    
    def _create_detailed_current_state(self) -> List[Dict]:
        """Create detailed current state journey with all touchpoints"""
        
        detailed_stages = []
        
        for stage_data in JOURNEY_STAGES["current_state"]:
            # Enrich with additional details
            detailed_stage = {
                **stage_data,
                "duration": self._estimate_duration_current(stage_data["stage"]),
                "channels": self._get_channels(stage_data["stage"], "current"),
                "tools_used": self._get_tools_used(stage_data["stage"], "current"),
                "stakeholders": self._get_stakeholders(stage_data["stage"]),
                "opportunities": self._identify_opportunities(stage_data),
                "quotes": self._get_stage_quotes(stage_data["stage"], "current")
            }
            
            detailed_stages.append(detailed_stage)
        
        return detailed_stages
    
    def _create_detailed_future_state(self) -> List[Dict]:
        """Create detailed future state journey with solutions"""
        
        detailed_stages = []
        
        for stage_data in JOURNEY_STAGES["future_state"]:
            # Enrich with additional details
            detailed_stage = {
                **stage_data,
                "duration": self._estimate_duration_future(stage_data["stage"]),
                "channels": self._get_channels(stage_data["stage"], "future"),
                "tools_used": self._get_tools_used(stage_data["stage"], "future"),
                "stakeholders": self._get_stakeholders(stage_data["stage"]),
                "key_features": self._get_key_features(stage_data["stage"]),
                "success_metrics": self._get_stage_metrics(stage_data["stage"]),
                "quotes": self._get_stage_quotes(stage_data["stage"], "future")
            }
            
            detailed_stages.append(detailed_stage)
        
        return detailed_stages
    
    def _estimate_duration_current(self, stage: str) -> str:
        """Estimate time spent in each current state stage"""
        duration_map = {
            "Discovery": "1-2 days (research and comparison)",
            "Signup": "5 minutes",
            "Setup": "2-4 hours (spread over 1-2 days)",
            "Initial Use": "1 week (honeymoon period)",
            "Reality Check": "3-5 days (declining engagement)",
            "Abandonment": "Permanent (average 12.3 days from signup)"
        }
        return duration_map.get(stage, "Unknown")
    
    def _estimate_duration_future(self, stage: str) -> str:
        """Estimate time spent in each future state stage"""
        duration_map = {
            "Discovery": "1 day (clear value proposition)",
            "Signup": "2 minutes (streamlined onboarding)",
            "First Task": "5 minutes (immediate value)",
            "Early Usage": "1 week (building habit)",
            "Habit Formation": "2-3 weeks (consistent use)",
            "Long-term": "Ongoing (sustainable engagement)"
        }
        return duration_map.get(stage, "Unknown")
    
    def _get_channels(self, stage: str, state: str) -> List[str]:
        """Get channels/touchpoints for stage"""
        if state == "current":
            channel_map = {
                "Discovery": ["YouTube", "Reddit", "Twitter/X", "Friend recommendation"],
                "Signup": ["Website", "App Store/Play Store"],
                "Setup": ["In-app tutorial", "YouTube tutorials", "Help docs"],
                "Initial Use": ["Mobile app", "Desktop app", "Browser"],
                "Reality Check": ["Push notifications", "Email reminders", "App badge"],
                "Abandonment": ["None (stopped engagement)"]
            }
        else:
            channel_map = {
                "Discovery": ["Social media", "Word of mouth", "App Store"],
                "Signup": ["Website", "Mobile app"],
                "First Task": ["In-app guided flow", "Mobile notifications"],
                "Early Usage": ["Daily app usage", "Contextual prompts"],
                "Habit Formation": ["Smart reminders", "Weekly reviews"],
                "Long-term": ["Background integration", "Minimal touchpoints"]
            }
        
        return channel_map.get(stage, [])
    
    def _get_tools_used(self, stage: str, state: str) -> List[str]:
        """Get tools used at each stage"""
        if state == "current":
            tools_map = {
                "Discovery": ["Google Search", "YouTube", "ProductHunt"],
                "Signup": ["Notion/Todoist/Trello"],
                "Setup": ["Template gallery", "Tutorial videos", "Community forums"],
                "Initial Use": ["Task lists", "Basic features only"],
                "Reality Check": ["App (rarely opened)", "Notifications (ignored)"],
                "Abandonment": ["Pen and paper", "Mental notes", "Basic reminders"]
            }
        else:
            tools_map = {
                "Discovery": ["App Store", "Social proof"],
                "Signup": ["Progressive onboarding"],
                "First Task": ["Minimal task view", "Quick add"],
                "Early Usage": ["Context-aware interface", "Progressive features"],
                "Habit Formation": ["Smart automation", "Adaptive UI"],
                "Long-term": ["Seamless integration", "Background intelligence"]
            }
        
        return tools_map.get(stage, [])
    
    def _get_stakeholders(self, stage: str) -> List[str]:
        """Get stakeholders involved at each stage"""
        stakeholder_map = {
            "Discovery": ["Friends", "Content creators", "Community"],
            "Signup": ["User (solo decision)"],
            "Setup": ["User", "Tutorial creators", "Help docs"],
            "Initial Use": ["User", "Possibly teammates"],
            "Reality Check": ["User (internal struggle)"],
            "Abandonment": ["User"],
            "First Task": ["User", "Onboarding system"],
            "Early Usage": ["User", "Smart assistant"],
            "Habit Formation": ["User", "Accountability features"],
            "Long-term": ["User", "Team (if collaborative)"]
        }
        return stakeholder_map.get(stage, ["User"])
    
    def _identify_opportunities(self, stage_data: Dict) -> List[str]:
        """Identify opportunities for improvement at each stage"""
        stage = stage_data["stage"]
        
        opportunity_map = {
            "Discovery": [
                "Highlight simplicity and quick setup in messaging",
                "Show before/after of overwhelmed → calm users",
                "Emphasize 'anti-guilt' positioning"
            ],
            "Signup": [
                "Ask 1-2 questions max (not 10-question onboarding)",
                "Show immediate value preview",
                "No empty workspace anxiety"
            ],
            "Setup": [
                "**CRITICAL OPPORTUNITY**: Reduce setup to <5 minutes",
                "Guided walkthrough, not documentation dump",
                "Smart defaults, minimal choices",
                "Progressive disclosure of features"
            ],
            "Initial Use": [
                "Limit visible tasks to 3 at a time",
                "Celebrate first completion immediately",
                "Prevent task list from growing too fast"
            ],
            "Reality Check": [
                "**CRITICAL OPPORTUNITY**: Change notification tone",
                "Show completed tasks, not incomplete",
                "Gentle re-engagement, not guilt",
                "Reduce visual noise"
            ],
            "Abandonment": [
                "Prevent with earlier interventions",
                "Exit survey to learn why",
                "Win-back campaign (if appropriate)"
            ]
        }
        
        return opportunity_map.get(stage, [])
    
    def _get_key_features(self, stage: str) -> List[str]:
        """Get key features for future state stages"""
        features_map = {
            "Discovery": [
                "Clear 'no overwhelm' promise",
                "2-minute setup guarantee",
                "Social proof from real users"
            ],
            "Signup": [
                "Single-screen onboarding",
                "Optional personalization (not required)",
                "Immediate access to tool"
            ],
            "First Task": [
                "Guided first task creation",
                "Instant completion celebration",
                "No complexity visible"
            ],
            "Early Usage": [
                "Max 3 visible tasks at once",
                "Progressive feature unlocking",
                "Context-aware suggestions",
                "Focus mode by default"
            ],
            "Habit Formation": [
                "Weekly reflection (wins highlighted)",
                "Adaptive difficulty",
                "Streak tracking (optional, non-guilt)",
                "Smart task scheduling"
            ],
            "Long-term": [
                "Auto-organization",
                "Zero-maintenance mode",
                "Deep integration with workflow",
                "Invisible productivity"
            ]
        }
        return features_map.get(stage, [])
    
    def _get_stage_metrics(self, stage: str) -> List[str]:
        """Get success metrics for each future state stage"""
        metrics_map = {
            "Discovery": [
                "Click-through rate on 'simple' messaging",
                "Time on landing page > 30 seconds"
            ],
            "Signup": [
                "Signup completion rate > 80%",
                "Time to signup < 2 minutes"
            ],
            "First Task": [
                "% completing 1 task in first session > 70%",
                "Time to first completion < 5 minutes"
            ],
            "Early Usage": [
                "Day 7 retention > 60%",
                "Tasks completed in first week ≥ 3"
            ],
            "Habit Formation": [
                "3-week active streak > 40%",
                "Weekly task completion rate > 50%"
            ],
            "Long-term": [
                "Day 90 retention > 35%",
                "NPS score > 50"
            ]
        }
        return metrics_map.get(stage, [])
    
    def _get_stage_quotes(self, stage: str, state: str) -> List[str]:
        """Get representative user quotes for each stage"""
        if state == "current":
            quotes_map = {
                "Discovery": [
                    "Everyone on YouTube seems to have their life together with Notion",
                    "Maybe this tool will finally make me productive"
                ],
                "Signup": [
                    "Okay, created account... now what?",
                    "Why is this workspace completely empty?"
                ],
                "Setup": [
                    "I've been watching tutorials for 2 hours and still don't get it",
                    "Should I use tags or folders? Or both? Or databases?"
                ],
                "Initial Use": [
                    "I added 25 tasks! This feels organized!",
                    "Wait, which one should I start with?"
                ],
                "Reality Check": [
                    "Why do I have 15 overdue tasks already?",
                    "I feel worse every time I open this app"
                ],
                "Abandonment": [
                    "I'm just not disciplined enough for this",
                    "Back to pen and paper I guess"
                ]
            }
        else:
            quotes_map = {
                "Discovery": [
                    "A productivity tool that promises NOT to overwhelm me? I'm in.",
                    "Finally, someone gets it"
                ],
                "Signup": [
                    "That was fast. I'm already in?",
                    "This doesn't feel scary like other tools"
                ],
                "First Task": [
                    "I just completed my first task in 3 minutes!",
                    "This actually feels good"
                ],
                "Early Usage": [
                    "I love that I only see 3 tasks at a time",
                    "It's helping me focus instead of overwhelming me"
                ],
                "Habit Formation": [
                    "I've been using this for 3 weeks straight",
                    "It just... works. No stress."
                ],
                "Long-term": [
                    "I don't even think about it anymore, it's just part of my routine",
                    "It adapts to me, I don't adapt to it"
                ]
            }
        
        return quotes_map.get(stage, [])
    
    def _save_journey_maps(self) -> None:
        """Save journey maps to JSON"""
        output_file = PROCESSED_DATA_DIR / "journey_map_data.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.journey_maps, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved journey maps to: {output_file}")
    
    def create_comparison_table(self) -> pd.DataFrame:
        """Create side-by-side comparison table"""
        
        current = self.journey_maps["current_state"]
        future = self.journey_maps["future_state"]
        
        comparison_data = []
        
        # Align stages (some differ between current/future)
        max_stages = max(len(current), len(future))
        
        for i in range(max_stages):
            row = {}
            
            if i < len(current):
                row["current_stage"] = current[i]["stage"]
                row["current_emotion"] = current[i]["emotion"]
                row["current_pain"] = current[i]["pain"]
                row["current_duration"] = current[i]["duration"]
            else:
                row["current_stage"] = "-"
                row["current_emotion"] = "-"
                row["current_pain"] = "-"
                row["current_duration"] = "-"
            
            if i < len(future):
                row["future_stage"] = future[i]["stage"]
                row["future_emotion"] = future[i]["emotion"]
                row["future_delight"] = future[i]["delight"]
                row["future_duration"] = future[i]["duration"]
            else:
                row["future_stage"] = "-"
                row["future_emotion"] = "-"
                row["future_delight"] = "-"
                row["future_duration"] = "-"
            
            comparison_data.append(row)
        
        comparison_df = pd.DataFrame(comparison_data)
        return comparison_df

if __name__ == "__main__":
    print("="*60)
    print("JOURNEY MAPPER")
    print("="*60)
    print()
    
    mapper = JourneyMapper()
    journey_maps = mapper.create_journey_maps()
    
    print("\n" + "="*60)
    print("Current State Journey:")
    print("="*60)
    for stage in journey_maps["current_state"]:
        print(f"\n{stage['stage']}: {stage['emotion']}")
        print(f"  Pain: {stage['pain']}")
        print(f"  Duration: {stage['duration']}")
    
    print("\n" + "="*60)
    print("Future State Journey:")
    print("="*60)
    for stage in journey_maps["future_state"]:
        print(f"\n{stage['stage']}: {stage['emotion']}")
        print(f"  Delight: {stage['delight']}")
        print(f"  Duration: {stage['duration']}")