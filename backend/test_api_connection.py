#!/usr/bin/env python3
"""
Test Inferrix API Connection
"""

import os
import requests

def test_api_connection():
    """Test the Inferrix API connection"""
    print("🔍 TESTING INFERRIX API CONNECTION")
    print("="*50)
    
    # Get API token
    api_token = os.getenv("INFERRIX_API_TOKEN")
    base_url = "https://cloud.inferrix.com/api"
    
    print(f"API Token: {'Set' if api_token else 'Not set'}")
    print(f"Base URL: {base_url}")
    
    if not api_token:
        print("❌ INFERRIX_API_TOKEN not set")
        return
    
    # Test device endpoint
    endpoint = "user/devices?page=0&pageSize=100"
    url = f"{base_url}/{endpoint}"
    headers = {"Authorization": f"Bearer {api_token}"}
    
    print(f"\nTesting endpoint: {endpoint}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API connection successful")
            
            if isinstance(data, dict):
                if 'data' in data:
                    devices = data['data']
                    print(f"Devices found: {len(devices)}")
                    
                    if devices:
                        print("\nFirst few devices:")
                        for i, device in enumerate(devices[:3]):
                            name = device.get('name', 'Unknown')
                            device_type = device.get('type', 'Unknown')
                            status = device.get('status', 'Unknown')
                            print(f"  {i+1}. {name} ({device_type}) - {status}")
                    else:
                        print("No devices in the account")
                else:
                    print("Response structure:", list(data.keys()))
            else:
                print("Response is not a dictionary")
                
        elif response.status_code == 401:
            print("❌ Authentication failed - check your API token")
        elif response.status_code == 403:
            print("❌ Access forbidden - check your permissions")
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - check your internet connection")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_api_connection() 