#!/usr/bin/env python3
"""
Debug fan speed patterns
"""

import re

def test_fan_speed_patterns():
    """Test fan speed patterns"""
    print("🧪 Testing Fan Speed Patterns")
    print("=" * 50)
    
    # Test queries
    test_queries = [
        "Set fan speed to 0 in 2F-Room50-Thermostat",
        "set fan to lowest speed for 2nd floor room 50",
        "Set fan speed in 2F-Room50-Thermostat to 0"
    ]
    
    # Fan speed patterns
    fan_speed_patterns = [
        r"set (?:the )?(?:fan speed|speed) (?:in|at|for)? ?([\w\- ]+)? to (low|medium|high|lowest|minimum|highest|maximum|\d{1,2}(?:\.\d+)?)",
        r"set (?:the )?(?:fan speed|speed) to (low|medium|high|lowest|minimum|highest|maximum|\d{1,2}(?:\.\d+)?) in ([\w\- ]+)",
        r"set (?:the )?fan to (low|medium|high|lowest|minimum|highest|maximum|\d{1,2}(?:\.\d+)?) speed (?:for|in|at) ([\w\- ]+)",
        r"set (?:the )?fan to (low|medium|high|lowest|minimum|highest|maximum|\d{1,2}(?:\.\d+)?) speed",
        r"fan (?:speed|) (?:to|set to) (low|medium|high|lowest|minimum|highest|maximum|\d{1,2}(?:\.\d+)?) (?:for|in|at) ([\w\- ]+)",
        r"fan (?:speed|) (?:to|set to) (low|medium|high|lowest|minimum|highest|maximum|\d{1,2}(?:\.\d+)?)"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing: '{query}'")
        print("-" * 40)
        
        matched = False
        for i, pattern in enumerate(fan_speed_patterns):
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                print(f"✅ Pattern {i+1} matched!")
                print(f"   Pattern: {pattern}")
                print(f"   Groups: {match.groups()}")
                matched = True
                break
        
        if not matched:
            print("❌ No pattern matched!")
            print("   Available patterns:")
            for i, pattern in enumerate(fan_speed_patterns):
                print(f"   {i+1}. {pattern}")

if __name__ == "__main__":
    test_fan_speed_patterns() 