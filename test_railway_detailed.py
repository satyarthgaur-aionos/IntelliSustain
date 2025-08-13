#!/usr/bin/env python3
"""
Detailed Railway Test with Authentication Debugging
"""
import requests
import json

RAILWAY_URL = "https://intellisustain-production.up.railway.app"

def test_railway_detailed():
    """Test Railway with detailed authentication debugging"""
    print("🔍 DETAILED RAILWAY TESTING")
    print("=" * 60)
    
    # Test 1: Login and get token
    print("1️⃣ Login and token analysis...")
    try:
        login_data = {
            "email": "satyarth.gaur@aionos.ai",
            "password": "Satya2025#"
        }
        response = requests.post(f"{RAILWAY_URL}/login", json=login_data, timeout=10)
        print(f"   Login status: {response.status_code}")
        
        if response.status_code == 200:
            login_response = response.json()
            print(f"   Login response keys: {list(login_response.keys())}")
            
            if 'access_token' in login_response:
                token = login_response['access_token']
                print(f"   Token length: {len(token)}")
                print(f"   Token preview: {token[:50]}...")
                
                # Test 2: Try different authentication headers
                print("\n2️⃣ Testing different authentication methods...")
                
                # Method 1: Bearer token
                headers1 = {"Authorization": f"Bearer {token}"}
                chat_data = {
                    "query": "Hello, can you help me?",
                    "user": "satyarth.gaur@aionos.ai"
                }
                
                print("   Trying Bearer token...")
                response = requests.post(f"{RAILWAY_URL}/chat", json=chat_data, headers=headers1, timeout=30)
                print(f"   Status: {response.status_code}")
                if response.status_code != 200:
                    print(f"   Error: {response.text}")
                
                # Method 2: Different header format
                headers2 = {"Authorization": f"bearer {token}"}
                print("   Trying lowercase bearer...")
                response = requests.post(f"{RAILWAY_URL}/chat", json=chat_data, headers=headers2, timeout=30)
                print(f"   Status: {response.status_code}")
                
                # Method 3: No user field
                chat_data_no_user = {
                    "query": "Hello, can you help me?"
                }
                print("   Trying without user field...")
                response = requests.post(f"{RAILWAY_URL}/chat", json=chat_data_no_user, headers=headers1, timeout=30)
                print(f"   Status: {response.status_code}")
                
                # Test 3: Check what endpoints work
                print("\n3️⃣ Testing available endpoints...")
                
                # Health endpoint
                response = requests.get(f"{RAILWAY_URL}/health", timeout=10)
                print(f"   Health: {response.status_code}")
                
                # API info endpoint
                response = requests.get(f"{RAILWAY_URL}/api/info", timeout=10)
                print(f"   API Info: {response.status_code}")
                
                # Try chat without authentication
                print("   Trying chat without auth...")
                response = requests.post(f"{RAILWAY_URL}/chat", json=chat_data, timeout=30)
                print(f"   Chat without auth: {response.status_code}")
                
        else:
            print(f"   Login failed: {response.text}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("📋 ANALYSIS:")
    print("The issue appears to be with JWT token authentication")
    print("Railway deployment is working but authentication is failing")

if __name__ == "__main__":
    test_railway_detailed()
