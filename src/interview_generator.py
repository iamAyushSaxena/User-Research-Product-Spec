"""
Interview Generator
Generates realistic interview transcripts with authentic user pain points
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple
from faker import Faker
from config import *

fake = Faker()
np.random.seed(42)
random.seed(42)

class InterviewGenerator:
    """
    Generates realistic user interview transcripts
    """
    
    def __init__(self, num_interviews: int = NUM_INTERVIEWS):
        """
        Initialize interview generator
        
        Args:
            num_interviews: Number of interviews to generate
        """
        self.num_interviews = num_interviews
        self.interviews = []
        self.metadata = []
        
    def _assign_persona(self) -> Dict:
        """
        Randomly assign a persona based on frequency distribution
        
        Returns:
            Dictionary with persona details
        """
        personas = list(PERSONA_DEFINITIONS.keys())
        frequencies = [PERSONA_DEFINITIONS[p]["frequency"] for p in personas]
        
        selected_persona = np.random.choice(personas, p=frequencies)
        persona_data = PERSONA_DEFINITIONS[selected_persona]
        
        # Generate realistic demographics
        age_range = persona_data["age_range"].split("-")
        age = random.randint(int(age_range[0]), int(age_range[1]))
        
        return {
            "persona": selected_persona,
            "age": age,
            "occupation": persona_data["occupation"],
            "behavior": persona_data["behavior"],
            "primary_pain": persona_data["pain"]
        }
    
    def _generate_opening(self, participant: Dict) -> str:
        """Generate interview opening"""
        return f"""INTERVIEWER: Thanks for joining me today! Let's start with some basics. Can you tell me about yourself?

PARTICIPANT: Sure! I'm {participant['age']} years old, and I'm a {participant['occupation'].lower()}. I've been trying to get better at managing my tasks and projects.

INTERVIEWER: Great! Have you used any productivity tools before?

PARTICIPANT: """
    
    def _generate_tool_history(self, persona_type: str) -> str:
        """Generate tool usage history based on persona"""
        
        tools_tried = random.sample([
            "Notion", "Todoist", "Trello", "Asana", "ClickUp", 
            "Microsoft To Do", "Google Keep", "Evernote"
        ], k=random.randint(3, 6))
        
        if persona_type == "The Overwhelmed Optimizer":
            return f"""Oh yes, I've tried so many! {', '.join(tools_tried[:4])}... probably more that I'm forgetting. I'm always looking for the 'perfect' system. I spend hours watching YouTube tutorials and setting things up, but somehow I never stick with any of them for more than a couple weeks.

INTERVIEWER: Interesting. What happens after those couple of weeks?

PARTICIPANT: I guess I just... lose steam? Like, I spend so much time organizing and reorganizing that I barely get any actual work done. And then I see all these unfinished tasks piling up, and it feels overwhelming. So I think 'maybe this tool isn't right for me' and I try another one. It's exhausting."""
        
        elif persona_type == "The Serial Abandoner":
            return f"""Yeah, I've tried {', '.join(tools_tried[:3])}. I get really excited at first—like, THIS is going to be the thing that changes everything! I spend the first few days adding all my tasks, color-coding things, setting up reminders. But then... I don't know, life gets busy, I miss a few days, and when I come back there's this huge list of overdue tasks with red notifications everywhere. It makes me feel terrible, so I just stop opening the app.

INTERVIEWER: So the notifications make you feel guilty?

PARTICIPANT: Exactly! It's like the app is judging me. I know that sounds silly, but seeing all those incomplete tasks just reminds me that I'm failing. So eventually I just... stop using it. And then I feel guilty about abandoning THAT too. It's a vicious cycle."""
        
        else:  # The Analog Holdout
            return f"""I've tried {', '.join(tools_tried[:2])}, but honestly? I always go back to pen and paper. There's something about writing things down by hand that just works better for my brain. Digital tools feel so... cold? Mechanical? I tried using Notion for a few weeks because everyone at work uses it, but I found myself constantly switching between the app and my notebook. Eventually I just gave up on the digital stuff.

INTERVIEWER: What specifically made you go back to paper?

PARTICIPANT: The digital tools just don't have that flexibility, you know? With a notebook, I can doodle, draw arrows, cross things out violently when I'm frustrated—it's more human. Plus, I don't have to worry about which template to use or how to structure everything. I just... write. It's liberating compared to all those menus and buttons and settings."""
        
    def _generate_pain_points_section(self, persona_type: str) -> str:
        """Generate detailed pain points discussion"""
        
        # Select 3-4 pain points that resonate with this persona
        relevant_pains = random.sample(PAIN_POINTS, k=random.randint(3, 4))
        
        conversation = """
INTERVIEWER: Let's dig deeper into what specifically didn't work. Can you walk me through a typical experience?

PARTICIPANT: """
        
        # First pain point (setup)
        if any(p["theme"] == "Setup Fatigue" for p in relevant_pains):
            conversation += """Sure. So I download the app, create an account, and then... blank screen. It's like, 'okay, now what?' I usually end up watching a 30-minute YouTube tutorial just to understand the basics. Then I spend another hour or two trying to recreate what I saw in the video. By the time I'm done setting it up, I'm mentally exhausted and I haven't actually DONE anything productive yet.

INTERVIEWER: So the setup process itself is draining?

PARTICIPANT: Completely. And the worst part? I'm never sure if I set it up 'correctly.' Like, am I using the right template? Should I use tags or folders? Should I create separate workspaces for work and personal? There's no right answer, so I keep second-guessing myself.

INTERVIEWER: What happens after you've set everything up?

PARTICIPANT: """
        
        # Second pain point (feature overwhelm)
        if any(p["theme"] == "Feature Overwhelm" for p in relevant_pains):
            conversation += """Well, then I start using it, and I realize there are all these features I didn't even know existed. Pop-ups telling me about databases, templates, integrations, AI features... it's overwhelming. I feel like I should be using all these advanced features to be 'productive,' but I don't even understand what half of them do. So I just... ignore them and stick to basic task lists.

INTERVIEWER: So you're not using most of the features?

PARTICIPANT: Not at all. Maybe 5-10% of what the tool can do. Which makes me wonder why I'm even using this complex tool when I could just use a simpler one. But everyone says these advanced tools are 'better,' so I feel like I should figure them out. It's confusing.

INTERVIEWER: How does that make you feel?

PARTICIPANT: """
        
        # Third pain point (guilt)
        if any(p["theme"] == "Productivity Guilt" for p in relevant_pains):
            conversation += """Honestly? Like a failure. I see people on YouTube with these beautiful, organized Notion workspaces tracking every aspect of their lives, and I can't even keep up with a basic task list for more than a week. I start thinking 'what's wrong with me?' It's not just about the tool anymore—it's about feeling like I'm not disciplined enough or organized enough or smart enough to use it properly.

INTERVIEWER: That's a strong emotional response. Does the tool itself contribute to those feelings?

PARTICIPANT: Absolutely. Every time I open it and see that list of incomplete tasks—with all the red overdue badges—it's like a visual representation of my failures. And the more tasks pile up, the more paralyzed I feel. I don't know where to start, so I just... don't. And then the guilt gets worse.

INTERVIEWER: What would need to change for you to stick with a tool?

PARTICIPANT: """
        
        return conversation
    
    def _generate_ideal_solution(self, persona_type: str) -> str:
        """Generate participant's vision of ideal solution"""
        
        if persona_type == "The Overwhelmed Optimizer":
            return """I think I need something that just... starts simple. Like, really simple. Show me three things to do today, that's it. Don't give me a hundred options until I ask for them. And maybe guide me through setup instead of throwing me into an empty workspace. Like, 'here's your first task, let's add it together.' Make it feel less like I'm building a system and more like I'm just getting started.

INTERVIEWER: So progressive disclosure of features?

PARTICIPANT: Yes! Exactly that. Start with the absolute basics—just tasks—and then as I use it, maybe introduce ONE new feature at a time. 'Hey, looks like you're using this a lot, would tags help you?' Not all at once.

INTERVIEWER: What about the guilt and overwhelm you mentioned?

PARTICIPANT: The tool should feel like a partner, not a judge. Maybe hide completed tasks by default so I see what I've accomplished, not what I haven't? Or limit how many tasks I can see at once—like, force me to focus on three things instead of showing me all 50. Sometimes constraints are actually freeing."""
        
        elif persona_type == "The Serial Abandoner":
            return """I need something that won't make me feel bad when I fall off the wagon. Like, if I don't use it for three days, don't punish me with scary red notifications. Just... gently welcome me back. 'Hey, want to add one task for today?' Not 'YOU HAVE 15 OVERDUE ITEMS.'

INTERVIEWER: So it's about the tone and approach?

PARTICIPANT: Yeah, and also maybe about setting realistic expectations. Don't let me add 30 tasks on day one. Stop me and say 'let's start with three.' Protect me from myself, you know? Because I WILL go overboard in the honeymoon phase, and then I'll crash.

INTERVIEWER: Interesting. Any other features?

PARTICIPANT: Quick wins. I need to feel successful fast—like within the first session. Not after a week of using it perfectly. If I can add a task and check it off in the first five minutes, and the app celebrates that somehow, I'd be so much more likely to come back tomorrow."""
        
        else:  # The Analog Holdout
            return """Honestly, I might never fully switch from paper. But if a digital tool could give me the flexibility of paper—like, not force me into rigid structures—I might use it alongside my notebook. Maybe for things that need reminders or sharing with others.

INTERVIEWER: What would that flexibility look like?

PARTICIPANT: Less 'you must use our system' and more 'use it however makes sense to you.' Don't make me choose between 10 template types. Just give me a blank space and let me write. If I want to add structure later, I can. But don't force it.

INTERVIEWER: Would you ever fully switch to digital?

PARTICIPANT: Only if it could replicate the feeling of paper—the freedom, the tactile satisfaction, the lack of options paralysis. Right now, digital tools try to do everything, which means they do nothing particularly well. I'd rather have a tool that does one thing perfectly than tries to be everything to everyone."""
        
    def _generate_closing(self) -> str:
        """Generate interview closing"""
        return """
INTERVIEWER: This has been incredibly helpful. Is there anything else you'd like to add?

PARTICIPANT: Just... please make something that doesn't make people feel stupid or inadequate. That's the biggest thing. Productivity tools should empower you, not make you feel worse about yourself.

INTERVIEWER: That's a perfect note to end on. Thank you so much for your time!

PARTICIPANT: Thanks for listening!"""
    
    def generate_single_interview(self, interview_num: int) -> Tuple[str, Dict]:
        """
        Generate a single complete interview
        
        Args:
            interview_num: Interview number (1-22)
            
        Returns:
            Tuple of (transcript, metadata)
        """
        # Assign persona
        participant = self._assign_persona()
        
        # Generate metadata
        interview_date = datetime(2025, 11, 1) + timedelta(days=random.randint(0, 45))
        
        metadata = {
            "interview_id": f"INT_{interview_num:03d}",
            "date": interview_date.strftime("%Y-%m-%d"),
            "duration_minutes": random.randint(INTERVIEW_DURATION_MIN, INTERVIEW_DURATION_MAX),
            "participant_id": f"P{interview_num:03d}",
            "age": participant["age"],
            "occupation": participant["occupation"],
            "persona": participant["persona"],
            "tools_abandoned": random.randint(2, 7),
            "current_tool": random.choice(["None", "Pen and paper", "Google Keep", "Basic notes app"]),
            "interview_method": random.choice(["Video call", "In-person", "Phone"])
        }
        
        # Generate full transcript
        transcript = f"""INTERVIEW TRANSCRIPT
Interview ID: {metadata['interview_id']}
Date: {metadata['date']}
Duration: {metadata['duration_minutes']} minutes
Participant: {metadata['participant_id']} (Anonymous)
Method: {metadata['interview_method']}

─────────────────────────────────────────────────────────────

"""
        transcript += self._generate_opening(participant)
        transcript += self._generate_tool_history(participant["persona"])
        transcript += self._generate_pain_points_section(participant["persona"])
        transcript += self._generate_ideal_solution(participant["persona"])
        transcript += self._generate_closing()
        
        transcript += f"""

─────────────────────────────────────────────────────────────
END OF INTERVIEW
Interviewer Notes: {random.choice([
    'Very passionate about the topic. Clear frustration with current tools.',
    'Participant became emotional when discussing guilt. Important insight.',
    'Strong advocate for simplicity. Mentioned "less is more" multiple times.',
    'Extremely detailed responses. Clearly has thought about this a lot.',
    'Hesitant at first but opened up. Good rapport established.'
])}
"""
        
        return transcript, metadata
    
    def generate_all_interviews(self) -> None:
        """Generate all interviews and save to files"""
        print(f"📝 Generating {self.num_interviews} interview transcripts...")
        
        for i in range(1, self.num_interviews + 1):
            transcript, metadata = self.generate_single_interview(i)
            
            # Save transcript
            transcript_file = INTERVIEW_DIR / f"interview_{i:02d}.txt"
            with open(transcript_file, 'w', encoding='utf-8') as f:
                f.write(transcript)
            
            self.interviews.append(transcript)
            self.metadata.append(metadata)
            
            if i % 5 == 0:
                print(f"  ✓ Generated {i}/{self.num_interviews} interviews")
        
        # Save metadata
        metadata_df = pd.DataFrame(self.metadata)
        metadata_df.to_csv(RAW_DATA_DIR / "interview_metadata.csv", index=False)
        
        print(f"✅ All interviews generated successfully!")
        print(f"📁 Transcripts: {INTERVIEW_DIR}")
        print(f"📊 Metadata: {RAW_DATA_DIR / 'interview_metadata.csv'}")
        
        # Generate summary statistics
        self._print_summary()
    
    def _print_summary(self) -> None:
        """Print summary statistics"""
        metadata_df = pd.DataFrame(self.metadata)
        
        print("\n" + "="*60)
        print("INTERVIEW SUMMARY STATISTICS")
        print("="*60)
        print(f"Total Interviews: {len(self.metadata)}")
        print(f"Date Range: {metadata_df['date'].min()} to {metadata_df['date'].max()}")
        print(f"Average Duration: {metadata_df['duration_minutes'].mean():.1f} minutes")
        print(f"\nPersona Distribution:")
        print(metadata_df['persona'].value_counts())
        print(f"\nAge Range: {metadata_df['age'].min()} - {metadata_df['age'].max()}")
        print(f"Average Tools Abandoned: {metadata_df['tools_abandoned'].mean():.1f}")

if __name__ == "__main__":
    print("="*60)
    print("USER RESEARCH INTERVIEW GENERATOR")
    print("="*60)
    print()
    
    generator = InterviewGenerator(num_interviews=NUM_INTERVIEWS)
    generator.generate_all_interviews()