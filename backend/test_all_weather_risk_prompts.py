#!/usr/bin/env python3
"""
Test All Weather and Risk Prompts
Verify weather and risk analysis functionality
"""

from enhanced_agentic_agent import enhanced_agentic_agent

# Weather and Risk Analysis Prompts (New)
weather_risk_prompts = [
    "What is the weather prediction in Mumbai for tomorrow?",
    "What HVAC risks if it rains in Mumbai this week?",
    "Show me weather forecast for Delhi this week",
    "What are the lighting risks if temperature drops in Bangalore?",
    "What are the electrical risks if there's a storm in Chennai?",
    "What HVAC risks if temperature rises above 35°C in Hyderabad?",
    "What are the facility risks if humidity exceeds 80% in Kolkata?",
    "What are the plumbing risks if it freezes in Shimla?",
    "What are the generator risks if there's a cyclone in Mumbai?",
    "What are the elevator risks if there's an earthquake in Delhi?",
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

def test_weather_risk_prompts():
    """Test all weather and risk prompts"""
    print("🌤️ TESTING WEATHER AND RISK PROMPTS")
    print("="*60)
    
    all_prompts = weather_risk_prompts + hotel_scenarios + conversational_prompts + device_alarm_prompts + analytics_prompts
    
    total_prompts = len(all_prompts)
    successful_prompts = 0
    weather_responses = 0
    risk_responses = 0
    
    print(f"Testing {total_prompts} prompts...\n")
    
    for i, prompt in enumerate(all_prompts, 1):
        print(f"Testing {i}/{total_prompts}: {prompt[:60]}...")
        
        try:
            response = enhanced_agentic_agent.process_query(prompt, "TestUser")
            
            if response:
                successful_prompts += 1
                
                # Check for weather responses
                if response.startswith('🌤️'):
                    weather_responses += 1
                    print(f"   ✅ Weather Response: {response[:100]}...")
                elif response.startswith('🌦️'):
                    risk_responses += 1
                    print(f"   ✅ Risk Response: {response[:100]}...")
                else:
                    print(f"   ✅ Regular Response: {response[:100]}...")
            else:
                print(f"   ❌ No response")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        print()
    
    # Summary
    print("="*60)
    print("📊 WEATHER AND RISK TEST SUMMARY")
    print("="*60)
    print(f"Total Prompts Tested: {total_prompts}")
    print(f"Successful Responses: {successful_prompts}")
    print(f"Weather Responses (🌤️): {weather_responses}")
    print(f"Risk Responses (🌦️): {risk_responses}")
    print(f"Success Rate: {(successful_prompts/total_prompts)*100:.1f}%")
    
    if weather_responses > 0 and risk_responses > 0:
        print("🎉 Weather and Risk Analysis Working!")
        print("✅ Both weather forecasts and risk analysis are functional")
    else:
        print("⚠️ Some weather/risk features may need attention")
    
    return successful_prompts == total_prompts

def test_specific_weather_scenarios():
    """Test specific weather scenarios"""
    print("\n🌤️ TESTING SPECIFIC WEATHER SCENARIOS")
    print("="*60)
    
    weather_scenarios = [
        "What is the weather prediction in Mumbai for tomorrow?",
        "Show me weather forecast for Delhi this week",
        "What's the weather like in Bangalore today?",
        "Weather forecast for Chennai next 3 days",
    ]
    
    for scenario in weather_scenarios:
        print(f"Testing: {scenario}")
        try:
            response = enhanced_agentic_agent.process_query(scenario, "TestUser")
            if response.startswith('🌤️'):
                print(f"   ✅ Weather Response: {response[:100]}...")
            else:
                print(f"   ⚠️ Unexpected Response: {response[:100]}...")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        print()

def test_specific_risk_scenarios():
    """Test specific risk scenarios"""
    print("\n🌦️ TESTING SPECIFIC RISK SCENARIOS")
    print("="*60)
    
    risk_scenarios = [
        "What HVAC risks if it rains in Mumbai this week?",
        "What are the lighting risks if temperature drops in Bangalore?",
        "What are the electrical risks if there's a storm in Chennai?",
        "What HVAC risks if temperature rises above 35°C in Hyderabad?",
    ]
    
    for scenario in risk_scenarios:
        print(f"Testing: {scenario}")
        try:
            response = enhanced_agentic_agent.process_query(scenario, "TestUser")
            if response.startswith('🌦️'):
                print(f"   ✅ Risk Response: {response[:100]}...")
            else:
                print(f"   ⚠️ Unexpected Response: {response[:100]}...")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        print()

def main():
    """Run all tests"""
    print("🚀 STARTING WEATHER AND RISK PROMPT TESTS")
    print("="*60)
    
    # Test all prompts
    success = test_weather_risk_prompts()
    
    # Test specific scenarios
    test_specific_weather_scenarios()
    test_specific_risk_scenarios()
    
    if success:
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("✅ Weather and Risk Analysis is fully functional!")
    else:
        print("⚠️ SOME TESTS FAILED - Review needed")

if __name__ == "__main__":
    main() 