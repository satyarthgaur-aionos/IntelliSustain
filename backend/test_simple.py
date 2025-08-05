#!/usr/bin/env python3
"""
Simple test for device mapping
"""

import os
import requests

def test_device_mapping():
    """Test device mapping with direct API call"""
    print("🔍 TESTING DEVICE MAPPING")
    print("="*50)
    
    # Get API token
    api_token = os.getenv("INFERRIX_API_TOKEN")
    base_url = "https://cloud.inferrix.com/api"
    
    if not api_token:
        print("❌ INFERRIX_API_TOKEN not set")
        return
    
    # Test device endpoint
    endpoint = "user/devices?page=0&pageSize=100"
    url = f"{base_url}/{endpoint}"
    headers = {"Authorization": f"Bearer {api_token}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'data' in data:
                devices = data['data']
                print(f"Total devices: {len(devices)}")
                
                # Look for device with "300186" in name
                target_device = None
                for device in devices:
                    name = device.get('name', '')
                    if '300186' in name:
                        target_device = device
                        break
                
                if target_device:
                    print(f"✅ Found device: {target_device.get('name')}")
                    print(f"   ID: {target_device.get('id')}")
                    print(f"   Type: {target_device.get('type')}")
                    print(f"   Status: {target_device.get('status')}")
                else:
                    print("❌ No device with '300186' found")
                    
                    # Show first few devices
                    print("\nFirst 5 devices:")
                    for i, device in enumerate(devices[:5]):
                        print(f"  {i+1}. {device.get('name', 'Unknown')} - {device.get('id')}")
                        
        else:
            print(f"❌ API request failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_device_mapping() 