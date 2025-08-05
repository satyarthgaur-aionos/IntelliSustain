#!/usr/bin/env python3
"""
Comprehensive test for enhanced fan speed control with all variations
"""

from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

def test_enhanced_fan_speed_control():
    """Test all fan speed variations work correctly"""
    agent = EnhancedAgenticInferrixAgent()
    
    print("🧪 Testing Enhanced Fan Speed Control - All Variations")
    print("=" * 60)
    
    # Test all speed variations
    test_queries = [
        # English variations
        "Increase the fan speed in second floor to high speed",
        "Set fan speed in second floor to highest",
        "Change fan speed in second floor to maximum",
        "Adjust fan speed in second floor to low",
        "Set fan speed in second floor to lowest",
        "Change fan speed in second floor to minimum",
        "Set fan speed in second floor to medium",
        "Set fan speed in second floor to 2",
        "Set fan speed in second floor to 1",
        "Set fan speed in second floor to 0",
        
        # Hindi/Hinglish variations
        "Second floor mein fan speed high karo",
        "Second floor mein fan speed highest karo",
        "Second floor mein fan speed maximum karo",
        "Second floor mein fan speed low karo",
        "Second floor mein fan speed lowest karo",
        "Second floor mein fan speed minimum karo",
        "Second floor mein fan speed medium karo",
    ]
    
    expected_values = {
        'high': 2,
        'highest': 2,
        'maximum': 2,
        'medium': 1,
        'low': 0,
        'lowest': 0,
        'minimum': 0,
        '2': 2,
        '1': 1,
        '0': 0
    }
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}️⃣ Testing: '{query}'")
        try:
            result = agent.process_query(query)
            print("✅ Response generated successfully")
            print("📋 Response preview:")
            print(result[:200] + "..." if len(result) > 200 else result)
            
            # Check if it's a control command response
            if "set fan speed" in result.lower() or "fan speed" in result.lower():
                print("✅ Control command detected")
                
                # Try to extract the speed value from the response
                import re
                speed_match = re.search(r'set fan speed.*?(\d+)', result.lower())
                if speed_match:
                    speed_value = int(speed_match.group(1))
                    print(f"🎯 Speed value detected: {speed_value}")
                    
                    # Check if it matches expected value
                    for keyword, expected in expected_values.items():
                        if keyword in query.lower():
                            if speed_value == expected:
                                print(f"✅ Correct speed value: {speed_value} (expected {expected})")
                            else:
                                print(f"❌ Wrong speed value: {speed_value} (expected {expected})")
                            break
                else:
                    print("⚠️ Could not extract speed value from response")
            else:
                print("❌ Not a control command response")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Enhanced Fan Speed Control Test Complete!")
    print("All speed variations should now work correctly:")
    print("• high/highest/maximum → 2")
    print("• medium → 1") 
    print("• low/lowest/minimum → 0")
    print("• Direct numbers (0,1,2) → as specified")

if __name__ == "__main__":
    test_enhanced_fan_speed_control() 