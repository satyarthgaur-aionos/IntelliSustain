#!/usr/bin/env python3
"""
Test script to check available telemetry keys for device 410601
"""

import os
import requests

# Set environment variables
os.environ['MOCK_MODE'] = 'false'
INFERRIX_API_TOKEN = os.getenv("INFERRIX_API_TOKEN")
INFERRIX_BASE_URL = "https://cloud.inferrix.com/api"

def get_available_telemetry_keys(device_id: str) -> list:
    """Fetch all available telemetry keys for a device."""
    try:
        endpoint = f"plugins/telemetry/DEVICE/{device_id}/keys/timeseries"
        url = f"{INFERRIX_BASE_URL}/{endpoint}"
        headers = {"Authorization": f"Bearer {INFERRIX_API_TOKEN}"}
        
        print(f"🔍 Fetching telemetry keys for device {device_id}...")
        print(f"📡 URL: {url}")
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        keys_data = response.json()
        print(f"📊 Raw response: {keys_data}")
        
        if isinstance(keys_data, dict):
            keys = list(keys_data.keys()) if keys_data else []
        elif isinstance(keys_data, list):
            keys = keys_data
        else:
            keys = []
            
        return keys
    except Exception as e:
        print(f"❌ Error fetching telemetry keys: {str(e)}")
        return []

def get_device_info(device_id: str) -> dict:
    """Get device information"""
    try:
        endpoint = f"deviceInfos/{device_id}"
        url = f"{INFERRIX_BASE_URL}/{endpoint}"
        headers = {"Authorization": f"Bearer {INFERRIX_API_TOKEN}"}
        
        print(f"🔍 Fetching device info for {device_id}...")
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        device_data = response.json()
        print(f"📊 Device info: {device_data}")
        
        return device_data
    except Exception as e:
        print(f"❌ Error fetching device info: {str(e)}")
        return {}

if __name__ == "__main__":
    # Test both the numeric ID and the UUID it maps to
    device_ids = ["410601", "00dc99c0-d179-11ef-92c0-61370650ea3a"]
    
    for device_id in device_ids:
        print(f"🧪 Testing Device {device_id}")
        print("=" * 50)
        
        # Get device info first
        device_info = get_device_info(device_id)
        if device_info:
            print(f"📱 Device Name: {device_info.get('name', 'Unknown')}")
            print(f"📱 Device Type: {device_info.get('type', 'Unknown')}")
            print(f"📱 Device Status: {device_info.get('status', 'Unknown')}")
        
        print("\n" + "=" * 50)
        
        # Get available telemetry keys
        keys = get_available_telemetry_keys(device_id)
        
        print(f"\n📊 Available Telemetry Keys for Device {device_id}:")
        if keys:
            for i, key in enumerate(keys, 1):
                print(f"  {i}. {key}")
        else:
            print("  ❌ No telemetry keys found")
        
        print(f"\n✅ Test completed for device {device_id}")
        print("\n" + "=" * 80 + "\n") 