#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_inferrix_api():
    """Test Inferrix API connectivity"""
    token = os.getenv('INFERRIX_API_TOKEN')
    print(f"Token exists: {bool(token)}")
    print(f"Token length: {len(token) if token else 0}")
    print(f"Token preview: {token[:50] + '...' if token else 'None'}")
    
    if not token:
        print("❌ No token found")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test devices endpoint
    print("\n🔍 Testing devices endpoint...")
    try:
        response = requests.get(
            'https://cloud.inferrix.com/api/user/devices?page=0&pageSize=10',
            headers=headers,
            timeout=10
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API call successful! Found {len(data.get('data', []))} devices")
        else:
            print(f"❌ API call failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test alarms endpoint
    print("\n🔍 Testing alarms endpoint...")
    try:
        response = requests.get(
            'https://cloud.inferrix.com/api/v2/alarms?pageSize=10&page=0',
            headers=headers,
            timeout=10
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Alarms API call successful! Found {len(data.get('data', []))} alarms")
        else:
            print(f"❌ Alarms API call failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_inferrix_api() 