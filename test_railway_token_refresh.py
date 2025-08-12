#!/usr/bin/env python3
"""
Test dynamic Inferrix token refresh mechanism on Railway
"""
import requests
import json
import time

# Railway URL
RAILWAY_URL = "https://intellisustain-production.up.railway.app"

def test_login_and_token_refresh():
    """Test the complete login and token refresh flow"""
    print("🔐 Testing Login and Token Refresh on Railway...")
    print("=" * 60)
    
    # Step 1: Login to get initial tokens
    print("1. Logging in to get initial tokens...")
    login_data = {
        "email": "admin@inferrix.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{RAILWAY_URL}/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            login_result = response.json()
            print("✅ Login successful!")
            print(f"   - Local JWT: {login_result.get('access_token', 'N/A')[:50]}...")
            print(f"   - Inferrix Refresh Token: {login_result.get('inferrix_refresh_token', 'N/A')[:50]}...")
            print(f"   - Inferrix Access Token: {login_result.get('inferrix_access_token', 'N/A')[:50]}...")
            
            # Step 2: Test token refresh
            print("\n2. Testing token refresh...")
            refresh_data = {
                "refresh_token": login_result.get("inferrix_refresh_token")
            }
            
            refresh_response = requests.post(
                f"{RAILWAY_URL}/inferrix/refresh-token",
                json=refresh_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {login_result.get('access_token')}"
                },
                timeout=30
            )
            
            if refresh_response.status_code == 200:
                refresh_result = refresh_response.json()
                print("✅ Token refresh successful!")
                print(f"   - Method used: {refresh_result.get('method', 'refresh')}")
                print(f"   - New Access Token: {refresh_result.get('access_token', 'N/A')[:50]}...")
                print(f"   - New Refresh Token: {refresh_result.get('refresh_token', 'N/A')[:50]}...")
                
                # Step 3: Test that the new token works with an API call
                print("\n3. Testing API call with new token...")
                test_api_call(refresh_result.get('access_token'))
                
            else:
                print(f"❌ Token refresh failed: {refresh_response.status_code}")
                print(f"   Error: {refresh_response.text}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")

def test_api_call(access_token):
    """Test making an API call with the refreshed token"""
    try:
        headers = {
            "X-Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Test getting devices
        response = requests.get(
            "https://cloud.inferrix.com/api/devices",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            devices_data = response.json()
            print("✅ API call successful!")
            print(f"   - Devices count: {len(devices_data.get('data', []))}")
        else:
            print(f"❌ API call failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during API call: {e}")

def test_multiple_refreshes():
    """Test multiple token refreshes to ensure consistency"""
    print("\n🔄 Testing Multiple Token Refreshes...")
    print("=" * 60)
    
    # First login
    login_data = {
        "email": "admin@inferrix.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{RAILWAY_URL}/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            login_result = response.json()
            refresh_token = login_result.get("inferrix_refresh_token")
            jwt_token = login_result.get("access_token")
            
            # Test multiple refreshes
            for i in range(3):
                print(f"\nRefresh attempt {i + 1}:")
                
                refresh_data = {"refresh_token": refresh_token}
                refresh_response = requests.post(
                    f"{RAILWAY_URL}/inferrix/refresh-token",
                    json=refresh_data,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {jwt_token}"
                    },
                    timeout=30
                )
                
                if refresh_response.status_code == 200:
                    refresh_result = refresh_response.json()
                    print(f"   ✅ Success - Method: {refresh_result.get('method', 'refresh')}")
                    
                    # Update tokens for next iteration
                    refresh_token = refresh_result.get("refresh_token")
                    access_token = refresh_result.get("access_token")
                    
                    # Test API call with new token
                    test_api_call(access_token)
                    
                else:
                    print(f"   ❌ Failed: {refresh_response.status_code}")
                    break
                    
    except Exception as e:
        print(f"❌ Error during multiple refresh test: {e}")

if __name__ == "__main__":
    print("🚀 Testing Dynamic Inferrix Token Refresh on Railway")
    print("=" * 60)
    
    # Test basic login and refresh
    test_login_and_token_refresh()
    
    # Test multiple refreshes
    test_multiple_refreshes()
    
    print("\n" + "=" * 60)
    print("🎉 Token refresh testing completed!") 