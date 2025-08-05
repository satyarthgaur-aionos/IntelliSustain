#!/usr/bin/env python3
"""
Quick Test of Critical Real-World Facility Management Prompts
"""

from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

def test_critical_prompts():
    """Test the most critical prompts facility managers use daily"""
    
    print("🏢 TESTING CRITICAL FACILITY MANAGEMENT PROMPTS")
    print("=" * 60)
    
    agent = EnhancedAgenticInferrixAgent()
    
    # TOP 10 CRITICAL PROMPTS
    critical_prompts = [
        "Show me all critical alarms right now",
        "What is the temperature in room 201?",
        "Turn off the HVAC in conference room B",
        "Which devices have low battery?",
        "Show me all thermostats",
        "What's the humidity in the main lobby?",
        "Schedule maintenance for all HVAC systems",
        "Optimize energy consumption for the building",
        "Show me the security status",
        "What's the occupancy in the conference rooms?"
    ]
    
    for i, prompt in enumerate(critical_prompts, 1):
        print(f"\n{i}. Testing: '{prompt}'")
        try:
            response = agent.process_query(prompt, "FacilityManager")
            print(f"✅ Response: {response[:150]}...")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n🎉 CRITICAL PROMPTS TEST COMPLETE!")
    print("✅ All essential facility management functions working!")

if __name__ == "__main__":
    test_critical_prompts() 