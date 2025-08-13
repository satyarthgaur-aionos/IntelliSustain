#!/usr/bin/env python3
"""
Debug Railway vs Local behavior to identify the 401 error issue
"""
import requests
import json
import time

def test_local_vs_railway():
    """Compare local and Railway behavior"""
    print("🔍 DEBUGGING RAILWAY VS LOCAL BEHAVIOR")
    print("=" * 60)
    
    # Test credentials
    login_data = {
        "email": "satyarth.gaur@aionos.ai",
        "password": "Satya2025#"
    }
    
    # Test 1: Local behavior
    print("1️⃣ Testing LOCAL behavior...")
    try:
        local_response = requests.post(
            "http://localhost:8000/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if local_response.status_code == 200:
            local_result = local_response.json()
            print("   ✅ Local login successful!")
            print(f"   - JWT Token: {local_result.get('access_token', 'N/A')[:50]}...")
            print(f"   - Inferrix Token: {local_result.get('inferrix_token', 'N/A')[:50] if local_result.get('inferrix_token') else 'MISSING'}...")
            
            # Test local Inferrix API call
            if local_result.get('inferrix_token'):
                print("   🔍 Testing local Inferrix API call...")
                local_headers = {
                    "Authorization": f"Bearer {local_result.get('access_token')}",
                    "X-Inferrix-Token": local_result.get('inferrix_token'),
                    "Content-Type": "application/json"
                }
                
                local_api_response = requests.get(
                    "http://localhost:8000/inferrix/devices",
                    headers=local_headers,
                    timeout=30
                )
                print(f"   - Local API Status: {local_api_response.status_code}")
                if local_api_response.status_code == 200:
                    print("   ✅ Local API call successful!")
                else:
                    print(f"   ❌ Local API call failed: {local_api_response.text}")
        else:
            print(f"   ❌ Local login failed: {local_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Local test error: {e}")
    
    print("\n" + "=" * 60)
    
    # Test 2: Railway behavior
    print("2️⃣ Testing RAILWAY behavior...")
    try:
        railway_response = requests.post(
            "https://intellisustain-production.up.railway.app/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if railway_response.status_code == 200:
            railway_result = railway_response.json()
            print("   ✅ Railway login successful!")
            print(f"   - JWT Token: {railway_result.get('access_token', 'N/A')[:50]}...")
            print(f"   - Inferrix Token: {railway_result.get('inferrix_token', 'N/A')[:50] if railway_result.get('inferrix_token') else 'MISSING'}...")
            
            # Test Railway Inferrix API call
            if railway_result.get('inferrix_token'):
                print("   🔍 Testing Railway Inferrix API call...")
                railway_headers = {
                    "Authorization": f"Bearer {railway_result.get('access_token')}",
                    "X-Inferrix-Token": railway_result.get('inferrix_token'),
                    "Content-Type": "application/json"
                }
                
                railway_api_response = requests.get(
                    "https://intellisustain-production.up.railway.app/inferrix/devices",
                    headers=railway_headers,
                    timeout=30
                )
                print(f"   - Railway API Status: {railway_api_response.status_code}")
                if railway_api_response.status_code == 200:
                    print("   ✅ Railway API call successful!")
                else:
                    print(f"   ❌ Railway API call failed: {railway_api_response.text}")
        else:
            print(f"   ❌ Railway login failed: {railway_response.status_code}")
            print(f"   - Error: {railway_response.text}")
            
    except Exception as e:
        print(f"   ❌ Railway test error: {e}")
    
    print("\n" + "=" * 60)
    
    # Test 3: Direct Inferrix API call comparison
    print("3️⃣ Testing DIRECT Inferrix API calls...")
    
    # Get tokens first
    local_token = None
    railway_token = None
    
    try:
        local_login = requests.post("http://localhost:8000/login", json=login_data, timeout=30)
        if local_login.status_code == 200:
            local_token = local_login.json().get('inferrix_token')
    except:
        pass
    
    try:
        railway_login = requests.post("https://intellisustain-production.up.railway.app/login", json=login_data, timeout=30)
        if railway_login.status_code == 200:
            railway_token = railway_login.json().get('inferrix_token')
    except:
        pass
    
    if local_token:
        print("   🔍 Testing direct Inferrix API from LOCAL...")
        try:
            direct_local = requests.get(
                "https://cloud.inferrix.com/api/user/devices",
                headers={"X-Authorization": f"Bearer {local_token}"},
                params={"page": 0, "pageSize": 10},
                timeout=30
            )
            print(f"   - Direct Local Status: {direct_local.status_code}")
            if direct_local.status_code == 200:
                print("   ✅ Direct Local API call successful!")
            else:
                print(f"   ❌ Direct Local API call failed: {direct_local.text}")
        except Exception as e:
            print(f"   ❌ Direct Local API error: {e}")
    
    if railway_token:
        print("   🔍 Testing direct Inferrix API from RAILWAY...")
        try:
            direct_railway = requests.get(
                "https://cloud.inferrix.com/api/user/devices",
                headers={"X-Authorization": f"Bearer {railway_token}"},
                params={"page": 0, "pageSize": 10},
                timeout=30
            )
            print(f"   - Direct Railway Status: {direct_railway.status_code}")
            if direct_railway.status_code == 200:
                print("   ✅ Direct Railway API call successful!")
            else:
                print(f"   ❌ Direct Railway API call failed: {direct_railway.text}")
        except Exception as e:
            print(f"   ❌ Direct Railway API error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 ANALYSIS COMPLETE")

if __name__ == "__main__":
    test_local_vs_railway()
