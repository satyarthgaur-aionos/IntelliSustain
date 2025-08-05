#!/usr/bin/env python3
"""
Test script to verify device integration between frontend and backend
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_device_integration():
    """Test the device integration between frontend and backend"""
    
    # Test configuration
    base_url = "http://localhost:8000"
    
    # First, get a JWT token
    print("🔐 Getting JWT token...")
    login_response = requests.post(f"{base_url}/login", json={
        "email": "tech@inferrix.com",
        "password": "admin@123"
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.text)
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("✅ Login successful")
    
    # Test 1: Get available devices
    print("\n📱 Getting available devices...")
    devices_response = requests.get(f"{base_url}/inferrix/devices", headers=headers)
    
    if devices_response.status_code != 200:
        print(f"❌ Failed to get devices: {devices_response.status_code}")
        print(devices_response.text)
        return
    
    devices = devices_response.json().get("devices", [])
    print(f"✅ Found {len(devices)} devices")
    
    if not devices:
        print("❌ No devices found - cannot test device integration")
        return
    
    # Get the first device for testing
    test_device = devices[0]
    device_id = test_device.get('id', {})
    if isinstance(device_id, dict):
        device_id = device_id.get('id', '')
    device_name = test_device.get('name', 'Unknown')
    
    print(f"🔧 Using test device: {device_name} (ID: {device_id})")
    
    # Test 2: Test chat with device parameter
    print(f"\n💬 Testing chat with device parameter...")
    
    test_queries = [
        f"Show temperature for {device_name}",
        f"Check humidity for device {device_id}",
        f"What's the battery level of {device_name}?",
        "Show all devices"  # Test without device
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test {i}: {query} ---")
        
        payload = {
            "query": query,
            "user": "tech@inferrix.com",
            "device": device_id if device_id in query else ""
        }
        
        print(f"📤 Sending payload: {json.dumps(payload, indent=2)}")
        
        chat_response = requests.post(f"{base_url}/chat", json=payload, headers=headers)
        
        if chat_response.status_code != 200:
            print(f"❌ Chat request failed: {chat_response.status_code}")
            print(chat_response.text)
            continue
        
        response_data = chat_response.json()
        response_text = response_data.get("response", "")
        
        print(f"📥 Response: {response_text[:200]}...")
        
        # Check if response contains device-specific information
        if device_id in query and device_id in response_text:
            print("✅ Device ID found in response - integration working!")
        elif "device" not in query.lower():
            print("✅ General query response received")
        else:
            print("⚠️ Device ID not found in response - may need investigation")
    
    # Test 3: Debug devices endpoint
    print(f"\n🔍 Testing debug devices endpoint...")
    debug_response = requests.get(f"{base_url}/debug/devices", headers=headers)
    
    if debug_response.status_code == 200:
        debug_data = debug_response.json()
        print(f"✅ Debug endpoint working - {debug_data['total_devices']} devices found")
        for device in debug_data['devices'][:3]:  # Show first 3 devices
            print(f"  - {device['name']} (ID: {device['id']})")
    else:
        print(f"❌ Debug endpoint failed: {debug_response.status_code}")

if __name__ == "__main__":
    test_device_integration() 