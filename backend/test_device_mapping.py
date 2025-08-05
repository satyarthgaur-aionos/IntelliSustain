#!/usr/bin/env python3
"""
Test Device Mapping and Telemetry
"""

import os
from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

def test_device_mapping():
    """Test device mapping functionality"""
    print("🔍 TESTING DEVICE MAPPING")
    print("="*50)
    
    agent = EnhancedAgenticInferrixAgent()
    
    # Test cases
    test_cases = [
        "300186",
        "150002", 
        "f40e0f90-592c-11ef-b890-bf853c6e5747",
        "IAQ Sensor V2 - 300186",
        "RH/T Sensor - 150002"
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: '{test_case}'")
        try:
            device_id = agent._map_device_name_to_id(test_case)
            print(f"  Mapped to: {device_id}")
            
            if device_id:
                # Test telemetry
                telemetry = agent._get_device_telemetry_data(device_id, 'temperature')
                print(f"  Temperature: {telemetry}")
                
                # Get available keys
                keys = agent._get_available_telemetry_keys(device_id)
                print(f"  Available keys: {keys}")
            else:
                print("  ❌ No device found")
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
    
    print("\n" + "="*50)

def test_telemetry_function():
    """Test the telemetry function directly"""
    print("\n🌡️ TESTING TELEMETRY FUNCTION")
    print("="*50)
    
    agent = EnhancedAgenticInferrixAgent()
    
    # Test with the working device ID from your example
    working_device_id = "f40e0f90-592c-11ef-b890-bf853c6e5747"
    
    print(f"Testing telemetry for device: {working_device_id}")
    
    try:
        # Test temperature
        temp_result = agent._get_device_telemetry_data(working_device_id, 'temperature')
        print(f"Temperature result: {temp_result}")
        
        # Test humidity
        humidity_result = agent._get_device_telemetry_data(working_device_id, 'humidity')
        print(f"Humidity result: {humidity_result}")
        
        # Get all available keys
        keys = agent._get_available_telemetry_keys(working_device_id)
        print(f"Available telemetry keys: {keys}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    test_device_mapping()
    test_telemetry_function() 