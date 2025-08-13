#!/usr/bin/env python3
"""
Test Complete Local Setup - All 3 Servers
"""
import requests
import json
import time

def test_complete_local_setup():
    """Test all 3 servers in the local setup"""
    print("🚀 TESTING COMPLETE LOCAL SETUP")
    print("=" * 60)
    print("📍 Testing all 3 servers:")
    print("   - Backend API: http://localhost:8000")
    print("   - MCP Server:  http://localhost:8001") 
    print("   - Frontend:    http://localhost:5173")
    print("=" * 60)
    
    # Test 1: Backend API Health
    print("\n1️⃣ Testing Backend API Health...")
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Backend API: {data.get('status', 'Unknown')}")
            print(f"   Database: {data.get('database_available', False)}")
            print(f"   AI Magic: {data.get('ai_magic_available', False)}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Backend API Info
    print("\n2️⃣ Testing Backend API Info...")
    try:
        response = requests.get('http://localhost:8000/api/info', timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API Name: {data.get('name', 'Unknown')}")
            print(f"   Version: {data.get('version', 'Unknown')}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: MCP Server Health
    print("\n3️⃣ Testing MCP Server...")
    try:
        response = requests.get('http://localhost:8001/health', timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ MCP Server: {data.get('status', 'Unknown')}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Frontend (basic connectivity)
    print("\n4️⃣ Testing Frontend...")
    try:
        response = requests.get('http://localhost:5173', timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Frontend: React dev server running")
        else:
            print(f"   ❌ Error: {response.text[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Login Functionality
    print("\n5️⃣ Testing Login...")
    try:
        login_data = {
            "email": "satyarth.gaur@aionos.ai",
            "password": "Satya2025#"
        }
        response = requests.post('http://localhost:8000/login', json=login_data, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Login successful!")
            print(f"   Token type: {data.get('token_type', 'Unknown')}")
            return data.get('access_token')  # Return token for further tests
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return None

def test_with_authentication(token):
    """Test authenticated endpoints"""
    if not token:
        print("\n❌ No token available, skipping authenticated tests")
        return
    
    print(f"\n🔐 Testing Authenticated Endpoints...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test chat endpoint
    print("\n6️⃣ Testing Chat Endpoint...")
    try:
        chat_data = {
            "query": "Show me battery status of all devices",
            "user": "satyarth.gaur@aionos.ai",
            "device": None
        }
        response = requests.post('http://localhost:8000/chat/enhanced', json=chat_data, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Chat response received!")
            print(f"   Response: {data.get('response', '')[:100]}...")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("⏳ Waiting 3 seconds for servers to be ready...")
    time.sleep(3)
    
    token = test_complete_local_setup()
    test_with_authentication(token)
    
    print("\n" + "=" * 60)
    print("🎯 LOCAL SETUP TEST COMPLETE!")
    print("=" * 60)
    print("✅ If all tests passed, your local setup is working correctly!")
    print("🌐 Access your application at: http://localhost:5173")
    print("📚 API Documentation at: http://localhost:8000/docs")
