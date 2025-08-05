#!/usr/bin/env python3
"""
Test Hinglish temperature setpoint fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

def test_hinglish_temp_setpoint_fix():
    """Test that Hinglish temperature setpoint commands work correctly after the fix"""
    agent = EnhancedAgenticInferrixAgent()
    
    # Test the original user query that was failing
    test_queries = [
        "Room 50 2nd floor ka temperature 22 degree par set karo",
        "Room 50 2nd floor ka temperature 22 degree par set kare",
        "Room 50 2nd floor me temperature 22 degree set karo",
        "Room 50 2nd floor me temperature 22 degree set kare"
    ]
    
    print("=== TESTING HINGLISH TEMPERATURE SETPOINT FIX ===")
    
    for query in test_queries:
        print(f"\n--- Testing: {query} ---")
        try:
            result = agent.process_query(query)
            print(f"Result: {result}")
            
            # Check if it's working correctly
            if "set to" in result.lower() and "22" in result.lower():
                print("✅ CORRECT - Temperature setpoint command detected")
            elif "unable to find a device" in result.lower():
                print("❌ INCORRECT - Device mapping failed")
            elif "unable to process" in result.lower():
                print("❌ INCORRECT - Pattern matching failed")
            else:
                print("⚠️ UNKNOWN - Need to check the response format")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_hinglish_temp_setpoint_fix() 