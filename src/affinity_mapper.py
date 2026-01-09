"""
Affinity Mapping Module
Clusters interview observations into themes
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict
import re
from collections import Counter
from config import *

class AffinityMapper:
    """
    Performs affinity mapping on interview transcripts
    """
    
    def __init__(self):
        """Initialize affinity mapper"""
        self.observations = []
        self.clusters = []
        
    def extract_observations(self, transcript: str, interview_id: str) -> List[Dict]:
        """
        Extract key observations from interview transcript
        
        Args:
            transcript: Interview transcript text
            interview_id: Interview identifier
            
        Returns:
            List of observation dictionaries
        """
        observations = []
        
        # Extract participant responses (everything after "PARTICIPANT: ")
        participant_responses = re.findall(
            r'PARTICIPANT: (.*?)(?=INTERVIEWER:|END OF INTERVIEW|$)', 
            transcript, 
            re.DOTALL
        )
        
        # Process each response
        for response in participant_responses:
            # Split into sentences
            sentences = re.split(r'[.!?]+', response)
            
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 20:  # Meaningful observations only
                    observations.append({
                        "text": sentence,
                        "interview_id": interview_id,
                        "theme": None,  # To be assigned
                        "sentiment": self._analyze_sentiment(sentence)
                    })
        
        return observations
    
    def _analyze_sentiment(self, text: str) -> str:
        """
        Simple sentiment analysis based on keywords
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment (negative, neutral, positive)
        """
        negative_words = [
            'overwhelm', 'guilt', 'frustrat', 'confus', 'stress', 'anxious',
            'fail', 'terrible', 'exhaust', 'burden', 'judg', 'bad', 'worse'
        ]
        positive_words = [
            'love', 'great', 'help', 'empower', 'accomplish', 'success',
            'excit', 'perfect', 'liberating', 'better'
        ]
        
        text_lower = text.lower()
        
        neg_count = sum(1 for word in negative_words if word in text_lower)
        pos_count = sum(1 for word in positive_words if word in text_lower)
        
        if neg_count > pos_count:
            return "negative"
        elif pos_count > neg_count:
            return "positive"
        else:
            return "neutral"
    
    def assign_themes(self, observations: List[Dict]) -> List[Dict]:
        """
        Assign themes to observations based on keywords
        
        Args:
            observations: List of observation dictionaries
            
        Returns:
            Observations with themes assigned
        """
        # Theme keyword mappings
        theme_keywords = {
            "Feature Overwhelm": [
                "too many", "options", "features", "buttons", "complex",
                "hundred", "overwhelm", "menus", "settings"
            ],
            "Productivity Guilt": [
                "guilt", "feel bad", "failure", "judg", "terrible",
                "incomplete", "overdue", "failing", "inadequate"
            ],
            "Setup Fatigue": [
                "setup", "hours", "tutorial", "setting up", "configure",
                "blank screen", "empty", "template", "getting started"
            ],
            "Context Switching": [
                "work and personal", "different", "context", "switch",
                "separate", "work vs", "home vs"
            ],
            "Prioritization Difficulty": [
                "don't know what", "where to start", "which one",
                "prioritize", "focus", "urgent", "important"
            ],
            "Tool Hopping Behavior": [
                "tried", "switch", "looking for", "another one",
                "next tool", "abandoned", "gave up"
            ],
            "Social Comparison Anxiety": [
                "everyone", "youtube", "other people", "should",
                "supposed to", "better than", "instagram"
            ],
            "Lack of Flexibility": [
                "rigid", "force", "must", "structure", "template",
                "can't", "doesn't let", "won't allow"
            ]
        }
        
        for obs in observations:
            text_lower = obs["text"].lower()
            
            # Score each theme
            theme_scores = {}
            for theme, keywords in theme_keywords.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                if score > 0:
                    theme_scores[theme] = score
            
            # Assign highest scoring theme
            if theme_scores:
                obs["theme"] = max(theme_scores, key=theme_scores.get)
            else:
                obs["theme"] = "Other"
        
        return observations
    
    def process_all_interviews(self) -> pd.DataFrame:
        """
        Process all interview transcripts
        
        Returns:
            DataFrame with all observations and themes
        """
        print("🗂️ Processing interviews for affinity mapping...")
        
        all_observations = []
        
        # Load all interview transcripts
        interview_files = sorted(INTERVIEW_DIR.glob("interview_*.txt"))
        
        for interview_file in interview_files:
            interview_id = interview_file.stem  # e.g., "interview_01"
            
            with open(interview_file, 'r', encoding='utf-8') as f:
                transcript = f.read()
            
            # Extract observations
            observations = self.extract_observations(transcript, interview_id)
            all_observations.extend(observations)
        
        # Assign themes
        all_observations = self.assign_themes(all_observations)
        
        # Convert to DataFrame
        observations_df = pd.DataFrame(all_observations)
        
        print(f"✅ Extracted {len(observations_df)} observations from {len(interview_files)} interviews")
        
        # Save to file
        observations_df.to_csv(PROCESSED_DATA_DIR / "affinity_clusters.csv", index=False)
        print(f"💾 Saved to: {PROCESSED_DATA_DIR / 'affinity_clusters.csv'}")
        
        # Print summary
        self._print_theme_summary(observations_df)
        
        return observations_df
    
    def _print_theme_summary(self, observations_df: pd.DataFrame) -> None:
        """Print theme distribution summary"""
        print("\n" + "="*60)
        print("AFFINITY MAPPING SUMMARY")
        print("="*60)
        
        theme_counts = observations_df['theme'].value_counts()
        sentiment_counts = observations_df['sentiment'].value_counts()
        
        print(f"\nTotal Observations: {len(observations_df)}")
        print(f"\nTheme Distribution:")
        for theme, count in theme_counts.items():
            pct = (count / len(observations_df)) * 100
            print(f"  {theme}: {count} ({pct:.1f}%)")
        
        print(f"\nSentiment Distribution:")
        for sentiment, count in sentiment_counts.items():
            pct = (count / len(observations_df)) * 100
            print(f"  {sentiment.title()}: {count} ({pct:.1f}%)")
    
    def generate_clusters_for_visualization(self) -> pd.DataFrame:
        """
        Generate cluster data for Streamlit visualization
        
        Returns:
            DataFrame with cluster summaries
        """
        observations_df = pd.read_csv(PROCESSED_DATA_DIR / "affinity_clusters.csv")
        
        cluster_summary = []
        
        for theme in observations_df['theme'].unique():
            theme_obs = observations_df[observations_df['theme'] == theme]
            
            # Get representative quotes (top 3 by sentiment)
            negative_obs = theme_obs[theme_obs['sentiment'] == 'negative'].head(3)
            
            cluster_summary.append({
                "theme": theme,
                "observation_count": len(theme_obs),
                "percentage": (len(theme_obs) / len(observations_df)) * 100,
                "sentiment_negative": len(theme_obs[theme_obs['sentiment'] == 'negative']),
                "sentiment_neutral": len(theme_obs[theme_obs['sentiment'] == 'neutral']),
                "sentiment_positive": len(theme_obs[theme_obs['sentiment'] == 'positive']),
                "sample_quotes": negative_obs['text'].tolist()
            })
        
        cluster_df = pd.DataFrame(cluster_summary)
        cluster_df = cluster_df.sort_values('observation_count', ascending=False)
        
        return cluster_df

if __name__ == "__main__":
    print("="*60)
    print("AFFINITY MAPPING PROCESSOR")
    print("="*60)
    print()
    
    mapper = AffinityMapper()
    observations_df = mapper.process_all_interviews()
    
    print("\n" + "="*60)
    print("Sample Observations by Theme:")
    print("="*60)
    
    for theme in observations_df['theme'].unique()[:3]:  # Show top 3 themes
        print(f"\n{theme}:")
        samples = observations_df[observations_df['theme'] == theme].head(2)
        for _, obs in samples.iterrows():
            print(f"  - \"{obs['text'][:100]}...\"")