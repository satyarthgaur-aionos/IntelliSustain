#!/usr/bin/env python3
"""
Energy Consumption Demo Script
==============================

This script demonstrates how to find energy consumption for any location or device
using the available APIs in the Inferrix system.
"""

import sys
import os
import time
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

def get_energy_consumption_demo():
    """Demonstrate energy consumption functionality"""
    
    print("Energy Consumption Demo")
    print("=" * 50)
    
    # Initialize the agent
    agent = EnhancedAgenticInferrixAgent()
    
    # Example 1: Get energy consumption for a specific device
    print("\n1. Getting energy consumption for a specific device...")
    device_id = "4505c680-4c26-11f0-816d-85352a7c91ff"  # Room 50 Thermostat
    
    # Get available telemetry keys for this device
    keys_endpoint = f"plugins/telemetry/DEVICE/{device_id}/keys/timeseries"
    available_keys = agent._make_api_request(keys_endpoint)
    
    print(f"Available telemetry keys for device {device_id}:")
    for key in available_keys:
        print(f"  - {key}")
    
    # Check if energy-related keys are available
    energy_keys = [key for key in available_keys if any(energy_term in key.lower() 
                  for energy_term in ['energy', 'power', 'kwh', 'voltage', 'current'])]
    
    if energy_keys:
        print(f"\nEnergy-related keys found: {energy_keys}")
        
        # Get energy consumption data
        energy_endpoint = f"plugins/telemetry/DEVICE/{device_id}/values/timeseries"
        energy_data = agent._make_api_request(energy_endpoint, data={
            "keys": ",".join(energy_keys),
            "limit": 10
        })
        
        print(f"\nEnergy consumption data for device {device_id}:")
        if energy_data and 'values' in energy_data:
            for reading in energy_data['values']:
                print(f"  {reading.get('key')}: {reading.get('value')} at {reading.get('ts')}")
        else:
            print("  No energy data available")
    else:
        print("  No energy-related telemetry keys found for this device")
    
    # Example 2: Find devices by location and check their energy consumption
    print("\n2. Finding devices by location and checking energy consumption...")
    
    # Get all devices
    devices_response = agent._make_api_request("deviceInfos/all")
    
    if devices_response:
        print(f"Total devices found: {len(devices_response)}")
        
        # Find devices in Room 50 or 2nd floor
        room_devices = []
        for device in devices_response:
            device_name = device.get('name', '')
            if 'Room 50' in device_name or '2nd floor' in device_name.lower():
                room_devices.append(device)
        
        print(f"\nDevices found in Room 50/2nd floor: {len(room_devices)}")
        
        for device in room_devices[:3]:  # Show first 3 devices
            device_id = device.get('id', {}).get('id') if isinstance(device.get('id'), dict) else device.get('id')
            device_name = device.get('name', 'Unknown')
            
            print(f"\nDevice: {device_name} (ID: {device_id})")
            
            # Get available keys for this device
            try:
                device_keys = agent._make_api_request(f"plugins/telemetry/DEVICE/{device_id}/keys/timeseries")
                energy_device_keys = [key for key in device_keys if any(energy_term in key.lower() 
                                   for energy_term in ['energy', 'power', 'kwh', 'voltage', 'current'])]
                
                if energy_device_keys:
                    print(f"  Energy keys available: {energy_device_keys}")
                    
                    # Get latest energy data
                    device_energy = agent._make_api_request(f"plugins/telemetry/DEVICE/{device_id}/values/timeseries", 
                                                          data={"keys": ",".join(energy_device_keys[:2]), "limit": 1})
                    
                    if device_energy and 'values' in device_energy:
                        for reading in device_energy['values']:
                            print(f"  {reading.get('key')}: {reading.get('value')}")
                    else:
                        print("  No energy data available")
                else:
                    print("  No energy-related keys available")
            except Exception as e:
                print(f"  Error getting device data: {e}")
    
    # Example 3: Demonstrate how to query energy consumption through the AI agent
    print("\n3. Energy consumption queries through AI agent...")
    
    # Example queries that could be implemented
    example_queries = [
        "What is the energy consumption for Room 50?",
        "Show me the power usage for device 4505c680-4c26-11f0-816d-85352a7c91ff",
        "Get energy consumption for all devices on the 2nd floor",
        "What is the total energy usage for the building?",
        "Show me historical energy consumption for the last 7 days"
    ]
    
    print("Example energy consumption queries that could be implemented:")
    for i, query in enumerate(example_queries, 1):
        print(f"  {i}. {query}")
    
    print("\n" + "=" * 50)
    print("Energy Consumption Demo Complete!")
    print("\nTo implement energy consumption queries:")
    print("1. Add energy-related telemetry keys to the agent's key mapping")
    print("2. Create energy consumption query handlers")
    print("3. Add energy analysis and reporting functions")
    print("4. Implement energy efficiency recommendations")

if __name__ == "__main__":
    get_energy_consumption_demo() 