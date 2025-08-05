#!/usr/bin/env python3
"""
Debug Thermostat Filtering
Test why "Show me all thermostats" returns "No devices found"
"""

import os
from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

def debug_thermostat_issue():
    """Debug the thermostat filtering issue"""
    print("🔍 DEBUGGING THERMOSTAT FILTERING ISSUE")
    print("="*60)
    
    # Initialize agent
    agent = EnhancedAgenticInferrixAgent()
    
    # 1. Check what devices are available
    print("\n1️⃣ CHECKING AVAILABLE DEVICES:")
    try:
        devices = agent._get_devices_list()
        print(f"Total devices found: {len(devices)}")
        
        if devices:
            print("\nFirst 10 devices:")
            for i, device in enumerate(devices[:10]):
                name = device.get('name', 'Unknown')
                device_type = device.get('type', 'Unknown')
                status = device.get('status', 'Unknown')
                print(f"  {i+1}. {name} (Type: {device_type}, Status: {status})")
        else:
            print("❌ No devices found in the system")
            return
            
    except Exception as e:
        print(f"❌ Error getting devices: {str(e)}")
        return
    
    # 2. Test device type extraction
    print("\n2️⃣ TESTING DEVICE TYPE EXTRACTION:")
    test_query = "Show me all thermostats"
    device_type = agent._extract_device_type(test_query)
    print(f"Query: '{test_query}' -> Device Type: '{device_type}'")
    
    # 3. Test the actual filtering logic
    print("\n3️⃣ TESTING FILTERING LOGIC:")
    device_type = 'thermostat'
    filtered_devices = []
    
    for device in devices:
        device_name = device.get('name', '').lower()
        device_type_api = device.get('type', '').lower()
        
        print(f"Checking: {device.get('name', 'Unknown')}")
        print(f"  - Name: '{device_name}'")
        print(f"  - Type: '{device_type_api}'")
        
        if device_type == 'thermostat' and ('thermostat' in device_name or 'thermostat' in device_type_api):
            filtered_devices.append(device)
            print(f"  ✅ MATCH FOUND!")
        else:
            print(f"  ❌ No match")
    
    print(f"\nFiltered thermostats: {len(filtered_devices)}")
    for device in filtered_devices:
        print(f"  - {device.get('name', 'Unknown')}")
    
    # 4. Test the full query processing
    print("\n4️⃣ TESTING FULL QUERY PROCESSING:")
    try:
        response = agent.process_query("Show me all thermostats", user="TestUser")
        print(f"Response: {response}")
    except Exception as e:
        print(f"❌ Error processing query: {str(e)}")
    
    print("\n" + "="*60)
    print("🎯 DEBUG COMPLETE")

if __name__ == "__main__":
    debug_thermostat_issue() 