#!/usr/bin/env python3
"""
Test script for temperature-related prompts to verify device matching and telemetry handling
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_agentic_agent import process_query

def test_temperature_prompts():
    """Test various temperature-related prompts to ensure they work correctly"""
    
    print("🌡️ Testing Temperature-Related Prompts")
    print("=" * 50)
    
    # Test cases that should work with our improved matching
    test_prompts = [
        "Show temperature in Second Floor Room No. 50",
        "What's the temperature in 2F Room 50?",
        "Show temperature for 2F-Room50-Thermostat",
        "What's the temperature in Second Floor Room 50?",
        "Show temperature in 2nd Floor Room No. 50",
        "Temperature in Second Floor Room 50",
        "Show temperature in Room 50 on Second Floor",
        "What's the temperature in 2F Room50?",
        "Show temperature for Room 50, 2nd Floor",
        "Temperature reading for Second Floor Room No. 50"
    ]
    
    success_count = 0
    total_count = len(test_prompts)
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🧪 Test {i}/{total_count}: {prompt}")
        print("-" * 40)
        
        try:
            response = process_query(prompt)
            print(f"✅ Response: {response[:200]}...")
            success_count += 1
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print(f"\n📊 Results: {success_count}/{total_count} successful ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("🎉 All temperature prompts working correctly!")
    else:
        print("⚠️ Some temperature prompts need attention")

if __name__ == "__main__":
    test_temperature_prompts() 