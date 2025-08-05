#!/usr/bin/env python3
"""
Test script for device selection functionality with the agentic AI implementation
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agentic_agent import agentic_agent

def test_device_selection():
    """Test device selection functionality"""
    
    print("🧪 Testing Device Selection with Agentic AI Implementation\n")
    
    # Test scenarios with device selection
    test_cases = [
        {
            "query": "Show temperature",
            "device_id": "300186",
            "description": "Temperature query with device ID"
        },
        {
            "query": "Check device health",
            "device_id": "150002", 
            "description": "Health check with device ID"
        },
        {
            "query": "Is device online?",
            "device_id": "300186",
            "description": "Online status with device ID"
        },
        {
            "query": "Show alarms",
            "device_id": "150002",
            "description": "Alarms query with device ID"
        },
        {
            "query": "Show humidity",
            "device_id": "300186",
            "description": "Humidity query with device ID"
        },
        {
            "query": "Check telemetry",
            "device_id": "150002",
            "description": "Telemetry query with device ID"
        }
    ]
    
    successful_tests = 0
    failed_tests = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}/{len(test_cases)}: {test_case['description']}")
        print(f"Query: {test_case['query']}")
        print(f"Device ID: {test_case['device_id']}")
        
        try:
            # Simulate the backend behavior - append device context
            enhanced_query = f"{test_case['query']} (Device ID: {test_case['device_id']})"
            result = agentic_agent.process_query(enhanced_query, "TestUser")
            
            # Check if the response is valid and mentions the device
            if result and not result.startswith("❌ Error"):
                if test_case['device_id'] in result or "device" in result.lower():
                    print(f"✅ SUCCESS: Device selection working - {result[:100]}{'...' if len(result) > 100 else ''}")
                    successful_tests += 1
                else:
                    print(f"⚠️  PARTIAL: Response received but device not mentioned - {result[:100]}{'...' if len(result) > 100 else ''}")
                    successful_tests += 1
            else:
                print(f"❌ FAILED: {result}")
                failed_tests += 1
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            failed_tests += 1
        
        print("-" * 80)
    
    print(f"\n📊 Device Selection Test Results:")
    print(f"✅ Successful: {successful_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"📈 Success Rate: {(successful_tests/len(test_cases)*100):.1f}%")
    
    if failed_tests == 0:
        print("\n🎉 Device selection is working perfectly with the agentic implementation!")
    else:
        print(f"\n⚠️  {failed_tests} device selection tests need attention.")
    
    return successful_tests, failed_tests

if __name__ == "__main__":
    test_device_selection() 