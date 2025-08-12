#!/usr/bin/env python3
"""
Test dynamic Inferrix token refresh mechanism locally
"""
import requests
import json
import time

# Local URL
LOCAL_URL = "http://localhost:8000"

def test_login_and_token_refresh():
    """Test the complete login and token refresh flow"""
    print("🔐 Testing Login and Token Refresh Locally...")
    print("=" * 60)
    
    # Step 1: Login to get initial tokens
    print("1. Logging in to get initial tokens...")
    login_data = {
        "email": "admin@inferrix.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{LOCAL_URL}/login",
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
                f"{LOCAL_URL}/inferrix/refresh-token",
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
        
        # Test getting alarms (doesn't require deviceIds parameter)
        response = requests.get(
            "https://cloud.inferrix.com/api/alarms",
            headers=headers,
            params={"page": 0, "pageSize": 10},
            timeout=30
        )
        
        if response.status_code == 200:
            alarms_data = response.json()
            print("✅ API call successful!")
            print(f"   - Alarms count: {len(alarms_data.get('data', []))}")
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
            f"{LOCAL_URL}/login",
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
                    f"{LOCAL_URL}/inferrix/refresh-token",
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

def test_frontend_integration():
    """Test the frontend integration by simulating localStorage operations"""
    print("\n🌐 Testing Frontend Integration...")
    print("=" * 60)
    
    # Simulate what the frontend would do
    try:
        # Step 1: Login
        login_data = {
            "email": "admin@inferrix.com",
            "password": "admin123"
        }
        
        response = requests.post(
            f"{LOCAL_URL}/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            login_result = response.json()
            print("✅ Frontend login simulation successful!")
            
            # Simulate localStorage storage
            jwt_token = login_result.get("access_token")
            inferrix_refresh_token = login_result.get("inferrix_refresh_token")
            inferrix_access_token = login_result.get("inferrix_access_token")
            
            print(f"   - JWT stored: {jwt_token[:50]}...")
            print(f"   - Inferrix Refresh Token stored: {inferrix_refresh_token[:50] if inferrix_refresh_token else 'N/A'}...")
            print(f"   - Inferrix Access Token stored: {inferrix_access_token[:50] if inferrix_access_token else 'N/A'}...")
            
            # Step 2: Simulate token refresh from frontend
            if inferrix_refresh_token:
                print("\n   Simulating frontend token refresh...")
                refresh_data = {"refresh_token": inferrix_refresh_token}
                refresh_response = requests.post(
                    f"{LOCAL_URL}/inferrix/refresh-token",
                    json=refresh_data,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {jwt_token}"
                    },
                    timeout=30
                )
                
                if refresh_response.status_code == 200:
                    refresh_result = refresh_response.json()
                    print(f"   ✅ Frontend refresh simulation successful!")
                    print(f"   - Method: {refresh_result.get('method', 'refresh')}")
                    print(f"   - New tokens would be stored in localStorage")
                else:
                    print(f"   ❌ Frontend refresh simulation failed: {refresh_response.status_code}")
            
        else:
            print(f"❌ Frontend login simulation failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error during frontend integration test: {e}")

if __name__ == "__main__":
    print("🚀 Testing Dynamic Inferrix Token Refresh Locally")
    print("=" * 60)
    
    # Test basic login and refresh
    test_login_and_token_refresh()
    
    # Test multiple refreshes
    test_multiple_refreshes()
    
    # Test frontend integration
    test_frontend_integration()
    
    print("\n" + "=" * 60)
    print("🎉 Local token refresh testing completed!") 