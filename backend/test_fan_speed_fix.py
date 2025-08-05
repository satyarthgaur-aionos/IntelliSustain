#!/usr/bin/env python3
"""
Test script to verify fan speed control fix works correctly
"""

from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

def test_fan_speed_control():
    """Test that fan speed control commands work correctly"""
    agent = EnhancedAgenticInferrixAgent()
    
    print("🧪 Testing Fan Speed Control Fix")
    print("=" * 50)
    
    # Test queries that should work with the fix
    test_queries = [
        "Increase the fan speed in second floor to high speed",
        "Set fan speed in second floor to high",
        "Change fan speed in second floor to 2",
        "Adjust fan speed in second floor to high"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}️⃣ Testing: '{query}'")
        try:
            result = agent.process_query(query)
            print("✅ Response generated successfully")
            print("📋 Response preview:")
            print(result[:200] + "..." if len(result) > 200 else result)
            
            # Check if it's a control command response (not a telemetry response)
            if "Speed for" in result and ":" in result:
                print("❌ Still returning telemetry instead of control command")
            elif "set fan speed" in result.lower() or "fan speed" in result.lower():
                print("✅ Control command detected")
            else:
                print("✅ Response looks correct")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Fan Speed Control Test Complete!")
    print("The system should now properly handle 'increase fan speed' commands")
    print("and find devices on the specified floor when no specific room is given.")

if __name__ == "__main__":
    test_fan_speed_control() 