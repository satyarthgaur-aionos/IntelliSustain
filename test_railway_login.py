#!/usr/bin/env python3
"""
Test Railway login directly
"""

import requests
import json

def test_railway_login():
    """Test login on Railway"""
    print("🔍 Testing Railway Login")
    print("=" * 40)
    
    # Railway URL
    base_url = "https://intellisustain-production.up.railway.app"
    
    # Test credentials
    test_credentials = [
        {
            "email": "tech@intellisustain.com",
            "password": "Demo@1234"
        },
        {
            "email": "admin@inferrix.com", 
            "password": "admin123"
        },
        {
            "email": "demo@inferrix.com",
            "password": "demo123"
        }
    ]
    
    print(f"🌐 Testing against: {base_url}")
    print("-" * 40)
    
    # Test health endpoint first
    try:
        health_response = requests.get(f"{base_url}/health", timeout=10)
        print(f"✅ Health check: {health_response.status_code}")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   Database available: {health_data.get('database_available', 'Unknown')}")
            print(f"   AI Magic available: {health_data.get('ai_magic_available', 'Unknown')}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test login endpoints
    for i, creds in enumerate(test_credentials, 1):
        print(f"\n👤 Test {i}: {creds['email']}")
        print("-" * 30)
        
        try:
            # Test login
            login_response = requests.post(
                f"{base_url}/login",
                json=creds,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            print(f"Status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                print("✅ Login successful!")
                response_data = login_response.json()
                print(f"   Token: {response_data.get('access_token', 'No token')[:20]}...")
            else:
                print("❌ Login failed")
                try:
                    error_data = login_response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Error: {login_response.text}")
                    
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    print(f"\n🚀 Next Steps:")
    print("1. Check Railway logs for deployment status")
    print("2. Verify DATABASE_URL is set correctly")
    print("3. Check if users were created in database")

if __name__ == "__main__":
    test_railway_login() 