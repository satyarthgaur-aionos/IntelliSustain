#!/usr/bin/env python3
"""
Test script for telemetry fixes
"""

from dotenv import load_dotenv
load_dotenv()

from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

def test_telemetry_fixes():
    """Test the telemetry fixes"""
    print("=== Testing Telemetry Fixes ===")
    
    agent = EnhancedAgenticInferrixAgent()
    
    # Test cases for single device telemetry
    single_device_tests = [
        "Show temperature in Second Floor Room No. 50",
        "Give temperature of 2F-Room50-Thermostat", 
        "What's the humidity in Room 33?",
        "Show battery for 2F-Room50-Thermostat",
        "Temperature in 2F-Room50-Thermostat"
    ]
    
    print("\n--- Single Device Telemetry Tests ---")
    for test_query in single_device_tests:
        print(f"\nQuery: {test_query}")
        try:
            response = agent.process_query(test_query, "test@example.com")
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")
    
    # Test cases for multi-device telemetry
    multi_device_tests = [
        "Show temperature for all thermostats",
        "Give humidity for all sensors",
        "Show battery for all devices"
    ]
    
    print("\n--- Multi-Device Telemetry Tests ---")
    for test_query in multi_device_tests:
        print(f"\nQuery: {test_query}")
        try:
            response = agent.process_query(test_query, "test@example.com")
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")
    
    # Test cases for fallback scenarios
    fallback_tests = [
        "Show temperature in NonExistentRoom",
        "Give humidity for InvalidDevice",
        "Temperature in Unknown Location"
    ]
    
    print("\n--- Fallback Scenario Tests ---")
    for test_query in fallback_tests:
        print(f"\nQuery: {test_query}")
        try:
            response = agent.process_query(test_query, "test@example.com")
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_telemetry_fixes() 