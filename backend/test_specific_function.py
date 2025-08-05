#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

# Import the specific function
from tools import get_devices_inferrix, get_device_telemetry_inferrix

def test_specific_functions():
    """Test specific functions from tools.py"""
    token = os.getenv('INFERRIX_API_TOKEN')
    print(f"Testing with token: {token[:50] if token else 'None'}...")
    
    try:
        # Test get_devices_inferrix
        print("\n🔍 Testing get_devices_inferrix...")
        devices = get_devices_inferrix(token)
        print(f"✅ Success! Found {len(devices)} devices")
        
        if devices:
            # Test with first device
            device = devices[0]
            device_id = device['id']['id'] if isinstance(device['id'], dict) else device['id']
            device_name = device.get('name', 'Unknown')
            print(f"Testing with device: {device_name} (ID: {device_id})")
            
            # Test get_device_telemetry_inferrix
            print("\n🔍 Testing get_device_telemetry_inferrix...")
            telemetry = get_device_telemetry_inferrix(device_id, ["temperature"], token)
            print(f"✅ Telemetry call successful!")
            print(f"Telemetry data: {telemetry}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_specific_functions() 