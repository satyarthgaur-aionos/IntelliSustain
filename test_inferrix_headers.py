#!/usr/bin/env python3
"""
Test to verify the correct header name for Inferrix API
"""
import requests
import json

def test_inferrix_headers():
    """Test different header names for Inferrix API"""
    print("🔍 Testing Inferrix API Headers...")
    print("=" * 50)
    
    # Step 1: Login to get token
    print("1. Logging in to get token...")
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
            
            print(f"   - Token: {inferrix_token[:50]}...")
            
            # Step 2: Test different header names
            print("\n2. Testing different header names...")
            
            # Test 1: X-Authorization (what we're currently using)
            print("\n   Test 1: X-Authorization header")
            headers1 = {"X-Authorization": f"Bearer {inferrix_token}"}
            try:
                response = requests.get(
                    "https://cloud.inferrix.com/api/v2/alarms",
                    headers=headers1,
                    params={"pageSize": 10, "page": 0},
                    timeout=10
                )
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Success! Alarms found: {len(data.get('data', []))}")
                else:
                    print(f"   ❌ Failed: {response.text[:100]}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # Test 2: Authorization header
            print("\n   Test 2: Authorization header")
            headers2 = {"Authorization": f"Bearer {inferrix_token}"}
            try:
                response = requests.get(
                    "https://cloud.inferrix.com/api/v2/alarms",
                    headers=headers2,
                    params={"pageSize": 10, "page": 0},
                    timeout=10
                )
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Success! Alarms found: {len(data.get('data', []))}")
                else:
                    print(f"   ❌ Failed: {response.text[:100]}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # Test 3: X-Inferrix-Token header
            print("\n   Test 3: X-Inferrix-Token header")
            headers3 = {"X-Inferrix-Token": inferrix_token}
            try:
                response = requests.get(
                    "https://cloud.inferrix.com/api/v2/alarms",
                    headers=headers3,
                    params={"pageSize": 10, "page": 0},
                    timeout=10
                )
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Success! Alarms found: {len(data.get('data', []))}")
                else:
                    print(f"   ❌ Failed: {response.text[:100]}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    test_inferrix_headers() 