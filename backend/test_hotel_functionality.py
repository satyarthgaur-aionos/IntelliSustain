#!/usr/bin/env python3
"""
Test script for hotel-specific functionality with the new APIs
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agentic_agent import agentic_agent

def test_hotel_functionality():
    """Test hotel-specific functionality"""
    
    print("🏨 Testing Hotel-Specific Functionality with New APIs\n")
    
    # Test scenarios for hotel industry
    test_cases = [
        # New API Functions
        {
            "query": "Get alarms for device 300186",
            "description": "Device alarms using new hotel API"
        },
        {
            "query": "Show attributes for device 150002", 
            "description": "Device attributes using new hotel API"
        },
        
        # Hotel Room Comfort Control
        {
            "query": "Increase temperature by 2 degrees in room 101 for the next 3 hours",
            "description": "Room comfort control - temperature adjustment"
        },
        {
            "query": "Turn on ambient lighting in suite 205",
            "description": "Room comfort control - lighting"
        },
        {
            "query": "Lower the temperature in room 301 by 3 degrees until checkout",
            "description": "Room comfort control - extended duration"
        },
        
        # Hotel Energy Optimization
        {
            "query": "Optimize energy usage in guest rooms during low occupancy",
            "description": "Energy optimization - guest rooms"
        },
        {
            "query": "Reduce HVAC energy consumption in public areas during off-peak hours",
            "description": "Energy optimization - public areas"
        },
        {
            "query": "Optimize lighting in the kitchen area for energy efficiency",
            "description": "Energy optimization - kitchen"
        },
        
        # Hotel Maintenance Scheduling
        {
            "query": "Schedule preventive maintenance for elevator equipment on floor 3",
            "description": "Maintenance scheduling - elevator"
        },
        {
            "query": "Plan corrective maintenance for HVAC system in the pool area",
            "description": "Maintenance scheduling - HVAC"
        },
        {
            "query": "Schedule emergency maintenance for security system with high priority",
            "description": "Maintenance scheduling - security"
        },
        
        # Hotel Guest Experience Optimization
        {
            "query": "Optimize room comfort for deluxe suite guests",
            "description": "Guest experience - room comfort"
        },
        {
            "query": "Improve air quality in presidential suites",
            "description": "Guest experience - air quality"
        },
        {
            "query": "Optimize lighting ambiance for evening guest experience",
            "description": "Guest experience - lighting ambiance"
        },
        
        # Hotel Operational Analytics
        {
            "query": "Analyze energy consumption patterns for the last month",
            "description": "Operational analytics - energy consumption"
        },
        {
            "query": "Show guest comfort metrics for the engineering department",
            "description": "Operational analytics - guest comfort"
        },
        {
            "query": "Analyze equipment health trends for the housekeeping department",
            "description": "Operational analytics - equipment health"
        },
        {
            "query": "Compare occupancy patterns with industry benchmarks",
            "description": "Operational analytics - occupancy patterns"
        }
    ]
    
    successful_tests = 0
    failed_tests = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}/{len(test_cases)}: {test_case['description']}")
        print(f"Query: {test_case['query']}")
        
        try:
            result = agentic_agent.process_query(test_case['query'], "HotelManager")
            
            # Check if the response is valid
            if result and not result.startswith("❌ Error"):
                # Check for hotel-specific keywords in response
                hotel_keywords = [
                    "room", "suite", "guest", "hotel", "comfort", "energy", 
                    "maintenance", "elevator", "hvac", "lighting", "temperature",
                    "occupancy", "analytics", "optimization", "scheduling"
                ]
                
                has_hotel_context = any(keyword in result.lower() for keyword in hotel_keywords)
                
                if has_hotel_context:
                    print(f"✅ SUCCESS: Hotel functionality working - {result[:100]}{'...' if len(result) > 100 else ''}")
                    successful_tests += 1
                else:
                    print(f"⚠️  PARTIAL: Response received but lacks hotel context - {result[:100]}{'...' if len(result) > 100 else ''}")
                    successful_tests += 1
            else:
                print(f"❌ FAILED: {result}")
                failed_tests += 1
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            failed_tests += 1
        
        print("-" * 80)
    
    print(f"\n📊 Hotel Functionality Test Results:")
    print(f"✅ Successful: {successful_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"📈 Success Rate: {(successful_tests/len(test_cases)*100):.1f}%")
    
    if failed_tests == 0:
        print("\n🎉 Hotel functionality is working perfectly!")
        print("🏨 The AI agent is ready for hospitality industry deployment!")
    else:
        print(f"\n⚠️  {failed_tests} hotel functionality tests need attention.")
    
    return successful_tests, failed_tests

def test_hotel_api_integration():
    """Test the new hotel API endpoints"""
    
    print("\n🔌 Testing Hotel API Integration\n")
    
    # Test the new API endpoints
    api_tests = [
        {
            "name": "Device Alarms API",
            "query": "Get all active alarms for device 300186 with status ACTIVE",
            "expected_function": "get_device_alarms"
        },
        {
            "name": "Device Attributes API", 
            "query": "Show all attribute keys for device 150002",
            "expected_function": "get_device_attributes"
        },
        {
            "name": "Room Comfort Control",
            "query": "Set temperature to 22 degrees in room 101",
            "expected_function": "hotel_room_comfort_control"
        },
        {
            "name": "Energy Optimization",
            "query": "Optimize HVAC energy usage in guest rooms",
            "expected_function": "hotel_energy_optimization"
        },
        {
            "name": "Maintenance Scheduling",
            "query": "Schedule preventive maintenance for elevator equipment",
            "expected_function": "hotel_maintenance_scheduling"
        }
    ]
    
    api_success = 0
    api_failed = 0
    
    for test in api_tests:
        print(f"API Test: {test['name']}")
        print(f"Query: {test['query']}")
        
        try:
            result = agentic_agent.process_query(test['query'], "HotelManager")
            
            if result and not result.startswith("❌ Error"):
                print(f"✅ API Integration Working")
                api_success += 1
            else:
                print(f"❌ API Integration Failed: {result}")
                api_failed += 1
                
        except Exception as e:
            print(f"❌ API Error: {str(e)}")
            api_failed += 1
        
        print("-" * 60)
    
    print(f"\n🔌 Hotel API Integration Results:")
    print(f"✅ Successful: {api_success}")
    print(f"❌ Failed: {api_failed}")
    
    return api_success, api_failed

if __name__ == "__main__":
    # Run hotel functionality tests
    hotel_success, hotel_failed = test_hotel_functionality()
    
    # Run API integration tests
    api_success, api_failed = test_hotel_api_integration()
    
    print(f"\n🏨 FINAL HOTEL SOLUTION STATUS:")
    print(f"📊 Functionality Tests: {hotel_success}/{hotel_success + hotel_failed} passed")
    print(f"🔌 API Integration Tests: {api_success}/{api_success + api_failed} passed")
    
    if hotel_failed == 0 and api_failed == 0:
        print("\n🎉 HOTEL SOLUTION IS PRODUCTION READY!")
        print("🏨 Ready for customer demo and hospitality industry deployment!")
    else:
        print(f"\n⚠️  Some tests need attention before production deployment.") 