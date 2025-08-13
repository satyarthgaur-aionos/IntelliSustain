#!/usr/bin/env python3
"""
Simple Railway Deployment Test
"""
import requests
import json

RAILWAY_URL = "https://intellisustain-production.up.railway.app"

def test_railway_simple():
    """Simple test to check Railway deployment"""
    print("🔍 SIMPLE RAILWAY DEPLOYMENT TEST")
    print("=" * 50)
    print(f"📍 URL: {RAILWAY_URL}")
    
    # Test 1: Health endpoint
    print("\n1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{RAILWAY_URL}/health", timeout=10)
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
        response = requests.get(f"{RAILWAY_URL}/api/info", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Name: {data.get('name', 'N/A')}")
            print(f"   Version: {data.get('version', 'N/A')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Login endpoint (without checking tokens)
    print("\n3️⃣ Testing login endpoint...")
    login_data = {
        "email": "satyarth.gaur@aionos.ai",
        "password": "Satya2025#"
    }
    
    try:
        response = requests.post(
            f"{RAILWAY_URL}/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response keys: {list(data.keys())}")
            print(f"   Has access_token: {'access_token' in data}")
            print(f"   Has inferrix_token: {'inferrix_token' in data}")
            if 'inferrix_token' in data:
                print(f"   Inferrix token: {data['inferrix_token'][:50]}...")
            else:
                print(f"   ❌ No inferrix_token in response")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_railway_simple()
