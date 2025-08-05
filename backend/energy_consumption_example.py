#!/usr/bin/env python3
"""
Energy Consumption Example Script
================================

This script demonstrates how to find energy consumption for any location or device
using the available APIs in the Inferrix system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

def demonstrate_energy_consumption():
    """Demonstrate how to find energy consumption for locations and devices"""
    
    print("Energy Consumption Demo")
    print("=" * 50)
    
    # Initialize the agent
    agent = EnhancedAgenticInferrixAgent()
    
    # Example 1: Get energy consumption for a specific device
    print("\n1. Getting energy consumption for a specific device:")
    print("-" * 45)
    
    device_id = "300186"  # IAQ Sensor V2 - 300186
    energy_data = agent._get_device_telemetry_data(device_id, "energy")
    print(f"Device ID: {device_id}")
    print(f"Energy Data: {energy_data}")
    
    # Example 2: Get available telemetry keys for a device
    print("\n2. Getting available telemetry keys for a device:")
    print("-" * 45)
    
    keys = agent._get_available_telemetry_keys(device_id)
    print(f"Available telemetry keys for device {device_id}:")
    for key in keys:
        print(f"  - {key}")
    
    # Example 3: Get devices for a location
    print("\n3. Getting devices for a location:")
    print("-" * 45)
    
    location = "Room 50 2nd floor"
    devices = agent._get_devices_for_location(location)
    print(f"Devices in {location}:")
    for device in devices:
        device_id = device.get('id', {}).get('id') if isinstance(device.get('id'), dict) else device.get('id')
        device_name = device.get('name', 'Unknown')
        print(f"  - {device_name} (ID: {device_id})")
    
    # Example 4: Calculate total energy for a location
    print("\n4. Calculating total energy consumption for a location:")
    print("-" * 45)
    
    total_energy = 0
    energy_devices = []
    
    for device in devices:
        device_id = device.get('id', {}).get('id') if isinstance(device.get('id'), dict) else device.get('id')
        device_name = device.get('name', 'Unknown')
        
        if device_id:
            # Get available keys for this device
            device_keys = agent._get_available_telemetry_keys(device_id)
            
            # Check for energy-related keys
            energy_keys = [key for key in device_keys if 'energy' in key.lower() or 'power' in key.lower()]
            
            if energy_keys:
                for energy_key in energy_keys:
                    energy_value = agent._get_device_telemetry_data(device_id, energy_key)
                    if energy_value and energy_value != 'None':
                        try:
                            energy_float = float(energy_value)
                            total_energy += energy_float
                            energy_devices.append({
                                'name': device_name,
                                'key': energy_key,
                                'value': energy_float
                            })
                            print(f"  - {device_name}: {energy_value} ({energy_key})")
                        except ValueError:
                            print(f"  - {device_name}: Invalid energy value '{energy_value}'")
    
    print(f"\nTotal energy consumption for {location}: {total_energy:.2f} kWh")
    
    # Example 5: Energy optimization workflow
    print("\n5. Executing energy optimization workflow:")
    print("-" * 45)
    
    optimization_result = agent._execute_energy_optimization_workflow({})
    print(optimization_result)
    
    # Example 6: Get energy consumption by device type
    print("\n6. Getting energy consumption by device type:")
    print("-" * 45)
    
    # Get all devices
    all_devices = agent._get_devices_list()
    
    # Group by device type
    device_types = {}
    for device in all_devices:
        device_type = device.get('type', 'Unknown')
        if device_type not in device_types:
            device_types[device_type] = []
        device_types[device_type].append(device)
    
    print("Devices by type:")
    for device_type, type_devices in device_types.items():
        print(f"  {device_type}: {len(type_devices)} devices")
        
        # Check energy consumption for first few devices of each type
        for device in type_devices[:3]:  # Limit to first 3 devices per type
            device_id = device.get('id', {}).get('id') if isinstance(device.get('id'), dict) else device.get('id')
            device_name = device.get('name', 'Unknown')
            
            if device_id:
                keys = agent._get_available_telemetry_keys(device_id)
                energy_keys = [key for key in keys if 'energy' in key.lower() or 'power' in key.lower()]
                
                if energy_keys:
                    for energy_key in energy_keys:
                        energy_value = agent._get_device_telemetry_data(device_id, energy_key)
                        if energy_value and energy_value != 'None':
                            print(f"    - {device_name}: {energy_value} ({energy_key})")
    
    # Example 7: Time-based energy queries
    print("\n7. Time-based energy queries:")
    print("-" * 45)
    
    # This would require additional API parameters for time ranges
    print("For time-based energy queries, you would need to:")
    print("  - Add startTs and endTs parameters to API calls")
    print("  - Use the timeseries endpoint with time range")
    print("  - Aggregate data over the specified time period")
    
    # Example 8: Energy consumption patterns
    print("\n8. Energy consumption patterns:")
    print("-" * 45)
    
    print("Common energy consumption patterns to look for:")
    print("  - Peak usage times (usually 12:00-14:00)")
    print("  - Off-peak usage patterns")
    print("  - Weekend vs weekday patterns")
    print("  - Seasonal variations")
    print("  - Anomaly detection (sudden spikes)")
    
    print("\n" + "=" * 50)
    print("Energy Consumption Demo Complete!")
    print("\nKey Takeaways:")
    print("1. Use _get_device_telemetry_data() for specific device energy")
    print("2. Use _get_available_telemetry_keys() to discover energy keys")
    print("3. Use _get_devices_for_location() for location-based queries")
    print("4. Aggregate energy data across multiple devices for locations")
    print("5. Check for various energy-related telemetry keys")
    print("6. Implement error handling for missing energy data")
    print("7. Use time-based parameters for historical analysis")

if __name__ == "__main__":
    demonstrate_energy_consumption() 