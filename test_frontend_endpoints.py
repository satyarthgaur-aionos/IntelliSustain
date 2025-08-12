#!/usr/bin/env python3
"""
Test frontend endpoints with token authentication
"""
import requests
import json

def test_frontend_endpoints():
    """Test the frontend endpoints with proper token authentication"""
    print("🧪 Testing Frontend Endpoints...")
    print("=" * 50)
    
    # Step 1: Login
    print("1. Logging in...")
    login_data = {
        "email": "satyarth.gaur@aionos.ai",
        "password": "Satya2025#"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            login_result = response.json()
            print("✅ Login successful!")
            
            jwt_token = login_result.get('access_token')
            inferrix_token = login_result.get('inferrix_token')
            
            if not inferrix_token:
                print("❌ No Inferrix token received")
                return
            
            # Step 2: Test devices endpoint
            print("\n2. Testing /inferrix/devices endpoint...")
            headers = {
                "Authorization": f"Bearer {jwt_token}",
                "X-Inferrix-Token": inferrix_token,
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                "http://localhost:8000/inferrix/devices",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                devices_result = response.json()
                print("✅ Devices endpoint successful!")
                print(f"   - Devices found: {len(devices_result.get('devices', []))}")
            else:
                print(f"❌ Devices endpoint failed: {response.status_code}")
                print(f"   Error: {response.text}")
            
            # Step 3: Test alarms endpoint
            print("\n3. Testing /inferrix/alarms endpoint...")
            response = requests.get(
                "http://localhost:8000/inferrix/alarms",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                alarms_result = response.json()
                print("✅ Alarms endpoint successful!")
                print(f"   - Alarms found: {len(alarms_result.get('data', []))}")
            else:
                print(f"❌ Alarms endpoint failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    test_frontend_endpoints() 