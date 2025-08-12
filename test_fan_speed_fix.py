#!/usr/bin/env python3
"""
Test the fan speed fix for the specific failing pattern
"""

import sys
sys.path.append('backend')

from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

def test_fan_speed_fix():
    """Test the specific failing fan speed pattern"""
    agent = EnhancedAgenticInferrixAgent()
    
    print("🧪 Testing Fan Speed Fix for Specific Pattern")
    print("=" * 60)
    
    # Test the exact failing pattern
    test_query = "Set fan speed to 0 in 2F-Room50-Thermostat"
    
    print(f"Testing: '{test_query}'")
    print("-" * 40)
    
    try:
        result = agent.process_query(test_query)
        print("✅ Response generated successfully")
        print("📋 Full Response:")
        print(result)
        
        # Check if it's a control command response
        if "set fan speed" in result.lower() and "0" in result:
            print("✅ Control command detected with correct value (0)")
        elif "❌" in result:
            print("❌ Still returning error response")
        else:
            print("⚠️ Response format unclear")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test other variations to make sure they still work
    print(f"\n🧪 Testing Other Variations")
    print("-" * 40)
    
    other_tests = [
        "Set fan speed in 2F-Room50-Thermostat to 0",
        "Set fan speed to 1 in 2F-Room50-Thermostat", 
        "Set fan speed to 2 in 2F-Room50-Thermostat",
        "Set fan speed to low in 2F-Room50-Thermostat",
        "Set fan speed to high in 2F-Room50-Thermostat"
    ]
    
    for i, query in enumerate(other_tests, 1):
        print(f"\n{i}️⃣ Testing: '{query}'")
        try:
            result = agent.process_query(query)
            if "set fan speed" in result.lower():
                print("✅ Control command detected")
            else:
                print("❌ Not a control command")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n🎯 Fan Speed Fix Test Complete!")
    print("The system should now handle both patterns:")
    print("• 'Set fan speed to [value] in [location]'")
    print("• 'Set fan speed in [location] to [value]'")

if __name__ == "__main__":
    test_fan_speed_fix() 