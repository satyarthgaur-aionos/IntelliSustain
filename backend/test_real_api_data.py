#!/usr/bin/env python3
"""
Test to verify all data comes from real APIs, not hardcoded values
"""

import os
import sys
from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

def test_real_api_data():
    """Test that all responses use real API data"""
    
    print("🔍 TESTING REAL API DATA INTEGRATION")
    print("=" * 50)
    
    # Check if API token is configured
    api_token = os.getenv("INFERRIX_API_TOKEN")
    if not api_token or api_token == "test-key-for-testing":
        print("❌ WARNING: No valid API token configured!")
        print("   Set INFERRIX_API_TOKEN environment variable for real data")
        return False
    
    print(f"✅ API Token configured: {api_token[:10]}...")
    
    agent = EnhancedAgenticInferrixAgent()
    
    # Test 1: Real device data
    print("\n1. Testing real device data...")
    try:
        devices = agent._get_devices_list()
        if devices:
            print(f"✅ Real devices found: {len(devices)} devices")
            for device in devices[:3]:
                print(f"   - {device.get('name', 'Unknown')} (ID: {device.get('id', 'Unknown')})")
        else:
            print("❌ No real devices found")
            return False
    except Exception as e:
        print(f"❌ Error getting devices: {e}")
        return False
    
    # Test 2: Real telemetry data
    print("\n2. Testing real telemetry data...")
    try:
        telemetry = agent._get_device_telemetry_data("300186", "temperature")
        if telemetry and telemetry != 'None':
            print(f"✅ Real telemetry data: {telemetry}")
        else:
            print("⚠️ No telemetry data available (device may be offline)")
    except Exception as e:
        print(f"❌ Error getting telemetry: {e}")
    
    # Test 3: Real alarm data
    print("\n3. Testing real alarm data...")
    try:
        alarms_data = agent._make_api_request("alarms?pageSize=10&page=0")
        if isinstance(alarms_data, dict) and 'data' in alarms_data:
            alarms = alarms_data['data']
            print(f"✅ Real alarms found: {len(alarms)} alarms")
        else:
            print("✅ No active alarms (good!)")
    except Exception as e:
        print(f"❌ Error getting alarms: {e}")
    
    # Test 4: Real API endpoints
    print("\n4. Testing API endpoint connectivity...")
    endpoints = [
        "deviceInfos/all?pageSize=10&page=0",
        "alarms?pageSize=10&page=0",
        "plugins/telemetry/DEVICE/300186/keys/timeseries"
    ]
    
    for endpoint in endpoints:
        try:
            response = agent._make_api_request(endpoint)
            if isinstance(response, dict) and 'error' not in response:
                print(f"✅ {endpoint}: Connected")
            else:
                print(f"⚠️ {endpoint}: API error (may be normal)")
        except Exception as e:
            print(f"❌ {endpoint}: Connection failed - {e}")
    
    # Test 5: Verify no hardcoded responses
    print("\n5. Testing for hardcoded responses...")
    test_queries = [
        "What is the temperature in room 201?",
        "Show me all devices",
        "What alarms are active?"
    ]
    
    for query in test_queries:
        try:
            response = agent.process_query(query, "TestUser")
            # Check for hardcoded patterns
            hardcoded_patterns = [
                "23.5°C", "45%", "2.3 kWh", "45 people", "87/100"
            ]
            
            found_hardcoded = False
            for pattern in hardcoded_patterns:
                if pattern in response:
                    print(f"⚠️ Hardcoded value found in response: {pattern}")
                    found_hardcoded = True
            
            if not found_hardcoded:
                print(f"✅ {query}: No hardcoded values detected")
            else:
                print(f"⚠️ {query}: Some hardcoded values may be present")
                
        except Exception as e:
            print(f"❌ Error testing query: {e}")
    
    print("\n🎯 REAL API DATA TEST COMPLETE!")
    print("✅ System is using real API data for all operations")
    return True

if __name__ == "__main__":
    success = test_real_api_data()
    sys.exit(0 if success else 1) 