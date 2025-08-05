#!/usr/bin/env python3
"""
Final Test for All 23 Prompts
Verify all prompts are properly structured and ready for demo
"""

from TOP_20_PRACTICAL_PROMPTS import PRACTICAL_PROMPTS

# Weather and Risk Analysis Prompts (New)
weather_risk_prompts = [
    "What is the weather prediction in Mumbai for tomorrow?",
    "What HVAC risks if it rains in Mumbai this week?",
    "Show me weather forecast for Delhi this week",
    "What are the lighting risks if temperature drops in Bangalore?",
    "What are the electrical risks if there's a storm in Chennai?",
    "What HVAC risks if temperature rises above 35°C in Hyderabad?",
    "What are the facility risks if humidity exceeds 80% in Kolkata?",
]

# Hotel-Specific Scenarios
hotel_scenarios = [
    "Increase temperature by 2 degrees in room 101 for the next 3 hours",
    "Optimize energy usage in guest rooms during low occupancy",
    "Schedule preventive maintenance for elevator equipment on floor 3",
    "Optimize room comfort for deluxe suite guests",
    "Analyze energy consumption patterns for the last month",
    "Get alarms for device 300186 with status ACTIVE",
    "Show attributes for device 150002",
]

# Conversational AI Scenarios
conversational_prompts = [
    "Turn off HVAC and dim lights in the east wing on Saturday and Sunday. Send me a report Monday.",
    "Lower the temperature by 2 degrees in Conference Room B for the next 3 hours.",
    "Are any HVAC or lighting systems likely to fail in the next 7 days?",
    "How much carbon emissions did we reduce this week? Are we on track for our Q3 target?",
    "What are the least used restrooms on the 3rd floor today?",
    "Why is the east wing warm and noisy today?",
]

# Device and Alarm Management
device_alarm_prompts = [
    "Show me all critical alarms for Tower A",
    "Acknowledge the high temperature alarm for Device X",
    "List of all active devices",
    "List devices with low battery",
    "Show top 3 alarm types",
    "Show temperature",
    "Check device health",
    "Show humidity",
    "Check if device is online",
    "Show battery level",
]

# Advanced Analytics
analytics_prompts = [
    "What are the energy consumption trends for the last quarter?",
    "Analyze occupancy patterns in conference rooms",
    "Show me predictive maintenance recommendations",
    "What are the root causes of recent HVAC failures?",
    "Generate a facility health report",
    "What are the cost savings from energy optimization?",
    "Show me anomaly detection results",
]

# Combine all prompts
all_prompts = weather_risk_prompts + hotel_scenarios + conversational_prompts + device_alarm_prompts + analytics_prompts

def test_all_prompts():
    """Test all 23 prompts for proper structure"""
    print("🧪 TESTING ALL 23 PROMPTS")
    print("="*60)
    
    total_prompts = 0
    valid_prompts = 0
    issues = []
    
    for complexity, prompts in PRACTICAL_PROMPTS.items():
        print(f"\n📋 {complexity} PROMPTS ({len(prompts)} prompts)")
        print("-" * 40)
        
        for i, prompt_data in enumerate(prompts, 1):
            total_prompts += 1
            
            # Check required fields
            required_fields = ['prompt', 'scenario', 'use_case', 'expected_response', 'complexity', 'frequency']
            missing_fields = [field for field in required_fields if field not in prompt_data]
            
            if missing_fields:
                issues.append(f"Prompt {total_prompts} missing: {missing_fields}")
                print(f"   ❌ {i}. Missing fields: {missing_fields}")
            else:
                valid_prompts += 1
                prompt = prompt_data['prompt']
                scenario = prompt_data['scenario']
                print(f"   ✅ {i}. {scenario}")
                
                # Check prompt quality
                if len(prompt) < 10:
                    issues.append(f"Prompt {total_prompts} too short")
                elif len(prompt) > 500:
                    issues.append(f"Prompt {total_prompts} too long")
                
                # Check expected response quality
                expected = prompt_data['expected_response']
                if len(expected) < 50:
                    issues.append(f"Prompt {total_prompts} expected response too short")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Prompts: {total_prompts}")
    print(f"Valid Prompts: {valid_prompts}")
    print(f"Issues Found: {len(issues)}")
    
    if issues:
        print(f"\n⚠️  Issues Found:")
        for issue in issues:
            print(f"   • {issue}")
    
    success_rate = (valid_prompts / total_prompts) * 100
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("🎉 ALL PROMPTS ARE PROPERLY STRUCTURED!")
        print("✅ Ready for demo!")
    else:
        print("⚠️  Some prompts need attention.")
    
    return success_rate == 100

def show_sample_prompts():
    """Show sample prompts from each category"""
    print(f"\n{'='*60}")
    print("📝 SAMPLE PROMPTS FROM EACH CATEGORY")
    print(f"{'='*60}")
    
    for complexity, prompts in PRACTICAL_PROMPTS.items():
        print(f"\n🎯 {complexity.upper()}:")
        for i, prompt_data in enumerate(prompts[:2], 1):  # Show first 2 from each category
            print(f"   {i}. {prompt_data['scenario']}")
            print(f"      Prompt: {prompt_data['prompt'][:80]}...")
            print()

def main():
    """Run the test"""
    success = test_all_prompts()
    show_sample_prompts()
    
    if success:
        print("🎉 VERIFICATION COMPLETE - ALL PROMPTS READY!")
        print("🚀 Ready to impress the client with all 23 prompts!")
    else:
        print("⚠️  VERIFICATION COMPLETE - SOME ISSUES FOUND")

if __name__ == "__main__":
    main() 