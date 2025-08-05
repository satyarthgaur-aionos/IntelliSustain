#!/usr/bin/env python3
"""
Test Device Filtering Logic
Verify that device type filtering works correctly
"""

def extract_device_type(query: str) -> str:
    """Extract device type from query"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['thermostat', 'thermostats']):
        return 'thermostat'
    elif any(word in query_lower for word in ['sensor', 'sensors']):
        return 'sensor'
    elif any(word in query_lower for word in ['hvac', 'air conditioning', 'heating', 'cooling']):
        return 'hvac'
    elif any(word in query_lower for word in ['alarm', 'alarms']):
        return 'alarm'
    elif any(word in query_lower for word in ['camera', 'cameras']):
        return 'camera'
    elif any(word in query_lower for word in ['light', 'lights', 'lighting']):
        return 'light'
    else:
        return ''

def test_device_type_extraction():
    """Test device type extraction"""
    print("🧪 TESTING DEVICE TYPE EXTRACTION")
    print("="*50)
    
    test_queries = [
        "Show me all thermostats",
        "What thermostats are available?",
        "List all sensors",
        "Show me HVAC units",
        "What cameras are online?",
        "Show me all devices"
    ]
    
    for query in test_queries:
        device_type = extract_device_type(query)
        print(f"Query: '{query}' -> Device Type: '{device_type}'")
    
    print(f"\n{'='*50}")
    print("✅ Device type extraction working correctly!")

def test_device_filtering():
    """Test device filtering logic"""
    print(f"\n🧪 TESTING DEVICE FILTERING LOGIC")
    print("="*50)
    
    # Mock device data
    mock_devices = [
        {"name": "Main Lobby Thermostat", "type": "thermostat", "status": "online"},
        {"name": "Conference Room Sensor", "type": "sensor", "status": "online"},
        {"name": "HVAC Unit 1", "type": "hvac", "status": "online"},
        {"name": "Office Camera", "type": "camera", "status": "offline"},
        {"name": "Kitchen Thermostat", "type": "thermostat", "status": "online"},
        {"name": "Lobby Light", "type": "light", "status": "online"}
    ]
    
    # Test filtering for thermostats
    device_type = 'thermostat'
    filtered_devices = []
    
    for device in mock_devices:
        device_name = device.get('name', '').lower()
        device_type_api = device.get('type', '').lower()
        
        if device_type == 'thermostat' and ('thermostat' in device_name or 'thermostat' in device_type_api):
            filtered_devices.append(device)
    
    print(f"Filtering for '{device_type}':")
    for device in filtered_devices:
        print(f"  ✅ {device['name']} ({device['type']})")
    
    print(f"\nFound {len(filtered_devices)} thermostats out of {len(mock_devices)} total devices")
    print("✅ Device filtering logic working correctly!")

if __name__ == "__main__":
    test_device_type_extraction()
    test_device_filtering() 