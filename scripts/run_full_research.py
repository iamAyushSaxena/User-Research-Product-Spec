"""
Complete Research Pipeline
Generates all research data: interviews, affinity mapping, personas, journey maps, and insights

Run this script to generate all project data from scratch
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from interview_generator import InterviewGenerator
from affinity_mapper import AffinityMapper
from persona_builder import PersonaBuilder
from journey_mapper import JourneyMapper
from insights_synthesizer import InsightsSynthesizer
from config import *

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*80)
    print(text.center(80))
    print("="*80 + "\n")

def main():
    """Run complete research pipeline"""
    
    print_header("USER RESEARCH PROJECT - FULL PIPELINE")
    print("This script will generate all research data for the project.")
    print("Estimated time: 2-3 minutes")
    print()
    
    # --- FIX: Removed input() so CI/CD doesn't crash ---
    # input("Press Enter to start generation...")
    print("Starting generation automatically...")
    
    # Step 1: Generate Interviews
    print_header("STEP 1/5: GENERATING INTERVIEW TRANSCRIPTS")
    generator = InterviewGenerator(num_interviews=NUM_INTERVIEWS)
    generator.generate_all_interviews()
    
    # Step 2: Affinity Mapping
    print_header("STEP 2/5: PERFORMING AFFINITY MAPPING")
    mapper = AffinityMapper()
    observations_df = mapper.process_all_interviews()
    
    # Step 3: Build Personas
    print_header("STEP 3/5: BUILDING USER PERSONAS")
    builder = PersonaBuilder()
    personas = builder.build_personas()
    
    # Step 4: Create Journey Maps
    print_header("STEP 4/5: CREATING JOURNEY MAPS")
    journey_mapper = JourneyMapper()
    journey_maps = journey_mapper.create_journey_maps()
    
    # Step 5: Synthesize Insights
    print_header("STEP 5/5: SYNTHESIZING INSIGHTS")
    synthesizer = InsightsSynthesizer()
    synthesis_report = synthesizer.synthesize_all_insights()
    
    # Complete!
    print_header("✅ PIPELINE COMPLETE!")
    
    print("All research data has been generated successfully!")
    print()
    print("📁 Generated Files:")
    print(f"   - {NUM_INTERVIEWS} interview transcripts")
    print(f"   - Affinity mapping clusters")
    print(f"   - {len(personas)} user personas")
    print(f"   - Journey maps (current + future state)")
    print(f"   - Synthesized insights and recommendations")
    print()
    print("🚀 Next Steps:")
    print("   1. Run the Streamlit dashboard: streamlit run dashboard.py")
    print("   2. Explore the research findings")
    print("   3. Review the PRD and recommendations")
    print()
    print("💡 Tip: You can regenerate data anytime by running this script again.")
    print()

if __name__ == "__main__":
    main()
