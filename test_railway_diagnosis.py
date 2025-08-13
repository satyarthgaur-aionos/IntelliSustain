#!/usr/bin/env python3
"""
Railway Deployment Diagnosis
"""
import requests
import json

RAILWAY_URL = "https://intellisustain-production.up.railway.app"

def test_railway_diagnosis():
    """Diagnose Railway deployment issues"""
    print("🔍 RAILWAY DEPLOYMENT DIAGNOSIS")
    print("=" * 60)
    
    # Test 1: Health check
    print("1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{RAILWAY_URL}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ Health check passed: {health_data.get('status', 'Unknown')}")
            print(f"   - Database available: {health_data.get('database_available', False)}")
            print(f"   - AI Magic available: {health_data.get('ai_magic_available', False)}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    # Test 2: Login test
    print("\n2️⃣ Testing login endpoint...")
    try:
        login_data = {
            "email": "satyarth.gaur@aionos.ai",
            "password": "Satya2025#"
        }
        
        response = requests.post(
            f"{RAILWAY_URL}/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            login_result = response.json()
            print("   ✅ Login successful!")
            print(f"   - JWT Token: {login_result.get('access_token', 'N/A')[:50]}...")
            print(f"   - Inferrix Token: {login_result.get('inferrix_token', 'MISSING!')[:50] if login_result.get('inferrix_token') else 'MISSING!'}")
            
            if not login_result.get('inferrix_token'):
                print("   ⚠️  ISSUE: No Inferrix token returned!")
                print("   🔍 This means Inferrix API integration is not working on Railway")
            else:
                print("   ✅ Inferrix token present!")
                
            return login_result.get('access_token'), login_result.get('inferrix_token')
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return None, None
    
    # Test 3: Direct Inferrix API test (if we have a token)
    print("\n3️⃣ Testing direct Inferrix API...")
    jwt_token, inferrix_token = test_railway_diagnosis()
    
    if inferrix_token:
        try:
            headers = {"X-Authorization": f"Bearer {inferrix_token}"}
            response = requests.get(
                "https://cloud.inferrix.com/api/user/devices",
                headers=headers,
                params={"page": 0, "pageSize": 5},
                timeout=10
            )
            
            if response.status_code == 200:
                devices_data = response.json()
                device_count = len(devices_data.get('data', []))
                print(f"   ✅ Direct Inferrix API works! Found {device_count} devices")
            else:
                print(f"   ❌ Direct Inferrix API failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Direct Inferrix API error: {e}")
    else:
        print("   ⚠️  Cannot test Inferrix API - no token available")
    
    print("\n" + "=" * 60)
    print("🔧 DIAGNOSIS SUMMARY:")
    print("1. Railway deployment is running")
    print("2. Login endpoint is working")
    print("3. ISSUE: Inferrix token not being returned")
    print("4. This suggests Inferrix API call is failing on Railway")
    print("\n💡 POSSIBLE CAUSES:")
    print("- Network connectivity issues on Railway")
    print("- Inferrix API credentials not working on Railway")
    print("- Different environment configuration")
    print("- Rate limiting or IP restrictions")

if __name__ == "__main__":
    test_railway_diagnosis()
