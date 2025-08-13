#!/usr/bin/env python3
"""
Test Local Server
"""
import requests
import json

def test_local_server():
    """Test if local server is working"""
    print("🔍 TESTING LOCAL SERVER")
    print("=" * 50)
    
    # Test 1: Health endpoint
    print("\n1️⃣ Testing health endpoint...")
    try:
        response = requests.get('http://127.0.0.1:8000/health', timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: API info endpoint
    print("\n2️⃣ Testing API info endpoint...")
    try:
        response = requests.get('http://127.0.0.1:8000/api/info', timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Name: {data.get('name', 'Unknown')}")
            print(f"   Version: {data.get('version', 'Unknown')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Login endpoint (should work)
    print("\n3️⃣ Testing login endpoint...")
    try:
        login_data = {
            "email": "satyarth.gaur@aionos.ai",
            "password": "Satya2025#"
        }
        response = requests.post('http://127.0.0.1:8000/login', json=login_data, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Login successful!")
            print(f"   Token type: {data.get('token_type', 'Unknown')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_local_server()
