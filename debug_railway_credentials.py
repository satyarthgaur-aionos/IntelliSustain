#!/usr/bin/env python3
"""
Debug Railway Credentials and Environment
"""
import os
import requests
import json

def debug_railway_credentials():
    """Debug what credentials and environment are available"""
    print("🔍 DEBUGGING RAILWAY CREDENTIALS")
    print("=" * 50)
    
    # Check environment variables
    print("1. Environment Variables:")
    env_vars = [
        "INFERRIX_API_TOKEN",
        "DATABASE_URL", 
        "OPENAI_API_KEY",
        "GEMINI_API_KEY"
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {value[:20]}..." if len(value) > 20 else f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: Not set")
    
    # Test Inferrix API directly
    print("\n2. Testing Inferrix API Credentials:")
    
    # Test 1: User credentials
    print("   Testing user credentials (satyarth.gaur@aionos.ai)...")
    try:
        response = requests.post(
            "https://cloud.inferrix.com/api/auth/login",
            json={"email": "satyarth.gaur@aionos.ai", "password": "Satya2025#"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Token: {data.get('token', 'No token')[:20]}...")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Environment variable token
    env_token = os.getenv("INFERRIX_API_TOKEN")
    if env_token:
        print(f"\n   Testing environment variable token...")
        try:
            # Test if the token works by making a simple API call
            headers = {"X-Authorization": f"Bearer {env_token}"}
            response = requests.get(
                "https://cloud.inferrix.com/api/user/devices",
                headers=headers,
                params={"page": 0, "pageSize": 1},
                timeout=10
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Environment token works!")
            else:
                print(f"   ❌ Environment token failed: {response.text}")
        except Exception as e:
            print(f"   ❌ Error testing environment token: {e}")
    else:
        print("   ⚠️  No environment token to test")
    
    # Test 3: Network connectivity
    print("\n3. Network Connectivity:")
    try:
        response = requests.get("https://cloud.inferrix.com/api", timeout=10)
        print(f"   ✅ Can reach cloud.inferrix.com (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Cannot reach cloud.inferrix.com: {e}")
    
    print("\n" + "=" * 50)
    print("🔧 RECOMMENDATIONS:")
    print("1. Check if INFERRIX_API_TOKEN is set in Railway environment variables")
    print("2. Verify the token value is correct")
    print("3. Check if the user credentials work with the actual Inferrix API")
    print("4. Consider using a different approach for Railway deployment")

if __name__ == "__main__":
    debug_railway_credentials()
