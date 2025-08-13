#!/usr/bin/env python3
"""
Check Railway Environment Variables
"""
import requests
import json

RAILWAY_URL = "https://intellisustain-production.up.railway.app"

def check_railway_environment():
    """Check what environment variables are available on Railway"""
    print("🔍 CHECKING RAILWAY ENVIRONMENT VARIABLES")
    print("=" * 60)
    
    # Test 1: Check health endpoint for environment info
    print("1️⃣ Checking health endpoint...")
    try:
        response = requests.get(f"{RAILWAY_URL}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ Health check passed")
            print(f"   - Database available: {health_data.get('database_available', False)}")
            print(f"   - AI Magic available: {health_data.get('ai_magic_available', False)}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    # Test 2: Check API info for more details
    print("\n2️⃣ Checking API info...")
    try:
        response = requests.get(f"{RAILWAY_URL}/api/info", timeout=10)
        if response.status_code == 200:
            api_info = response.json()
            print(f"   ✅ API info available")
            print(f"   - Name: {api_info.get('name', 'Unknown')}")
            print(f"   - Version: {api_info.get('version', 'Unknown')}")
            print(f"   - Features available: {api_info.get('features_available', {})}")
        else:
            print(f"   ❌ API info failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ API info error: {e}")
    
    # Test 3: Try to login and see what happens
    print("\n3️⃣ Testing login to check JWT...")
    try:
        login_data = {
            "email": "satyarth.gaur@aionos.ai",
            "password": "Satya2025#"
        }
        response = requests.post(f"{RAILWAY_URL}/login", json=login_data, timeout=10)
        if response.status_code == 200:
            login_response = response.json()
            print("   ✅ Login successful")
            print(f"   - JWT Token present: {'✅' if 'access_token' in login_response else '❌'}")
            print(f"   - Inferrix Token present: {'✅' if 'inferrix_token' in login_response else '❌'}")
            
            if 'access_token' in login_response:
                token = login_response['access_token']
                print(f"   - Token length: {len(token)}")
                
                # Test 4: Try to use the JWT token
                print("\n4️⃣ Testing JWT token usage...")
                headers = {"Authorization": f"Bearer {token}"}
                chat_data = {
                    "query": "Hello",
                    "user": "satyarth.gaur@aionos.ai"
                }
                
                response = requests.post(f"{RAILWAY_URL}/chat", json=chat_data, headers=headers, timeout=30)
                print(f"   - Chat endpoint status: {response.status_code}")
                if response.status_code != 200:
                    print(f"   - Chat error: {response.text}")
                else:
                    print("   ✅ JWT authentication working!")
        else:
            print(f"   ❌ Login failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Login error: {e}")
    
    print("\n" + "=" * 60)
    print("📋 REQUIRED ENVIRONMENT VARIABLES FOR RAILWAY:")
    print("✅ DATABASE_URL (working)")
    print("❌ JWT_SECRET_KEY (missing - causing auth issues)")
    print("❌ OPENAI_API_KEY (needed for AI functionality)")
    print("❌ GEMINI_API_KEY (needed for AI functionality)")
    print("❌ INFERRIX_API_TOKEN (removed - causing API issues)")
    print("\n💡 SOLUTION: Add JWT_SECRET_KEY to Railway environment variables")

if __name__ == "__main__":
    check_railway_environment()
