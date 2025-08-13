#!/usr/bin/env python3
"""
Railway Health Check
"""
import requests
import json
import time

def test_railway_health():
    """Test Railway deployment health"""
    base_url = "https://intellisustain-production.up.railway.app"
    
    print("🔍 RAILWAY HEALTH CHECK")
    print("=" * 60)
    print(f"Testing: {base_url}")
    
    # Test 1: Basic health endpoint
    print("\n1. Testing /health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ Health endpoint working")
        else:
            print("   ❌ Health endpoint failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: API info endpoint
    print("\n2. Testing /api/info endpoint...")
    try:
        response = requests.get(f"{base_url}/api/info", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ API info endpoint working")
        else:
            print("   ❌ API info endpoint failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Login endpoint
    print("\n3. Testing /login endpoint...")
    try:
        login_data = {
            "email": "satyarth.gaur@aionos.ai",
            "password": "admin123"
        }
        response = requests.post(f"{base_url}/login", json=login_data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            login_result = response.json()
            print(f"   ✅ Login successful")
            print(f"   JWT Token: {'✅' if 'access_token' in login_result else '❌'}")
            print(f"   Inferrix Token: {'✅' if 'inferrix_token' in login_result else '❌'}")
            
            # Test 4: Chat endpoint with token
            if 'access_token' in login_result:
                print("\n4. Testing /chat endpoint with token...")
                headers = {
                    "Authorization": f"Bearer {login_result['access_token']}",
                    "Content-Type": "application/json"
                }
                if 'inferrix_token' in login_result:
                    headers["X-Inferrix-Token"] = login_result['inferrix_token']
                
                chat_data = {
                    "query": "Show me energy usage on 2nd floor",
                    "user": "satyarth.gaur@aionos.ai"
                }
                
                response = requests.post(f"{base_url}/chat", json=chat_data, headers=headers, timeout=30)
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                if response.status_code == 200:
                    print("   ✅ Chat endpoint working")
                else:
                    print("   ❌ Chat endpoint failed")
        else:
            print(f"   ❌ Login failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Enhanced chat endpoint
    print("\n5. Testing /chat/enhanced endpoint...")
    try:
        if 'access_token' in locals() and 'login_result' in locals():
            headers = {
                "Authorization": f"Bearer {login_result['access_token']}",
                "Content-Type": "application/json"
            }
            if 'inferrix_token' in login_result:
                headers["X-Inferrix-Token"] = login_result['inferrix_token']
            
            chat_data = {
                "query": "Show me energy usage on 2nd floor",
                "user": "satyarth.gaur@aionos.ai"
            }
            
            response = requests.post(f"{base_url}/chat/enhanced", json=chat_data, headers=headers, timeout=30)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            if response.status_code == 200:
                print("   ✅ Enhanced chat endpoint working")
            else:
                print("   ❌ Enhanced chat endpoint failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_railway_health()
