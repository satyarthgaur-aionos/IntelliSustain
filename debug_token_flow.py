#!/usr/bin/env python3
"""
Debug token flow to identify where the token is getting lost
"""
import requests
import json

def debug_token_flow():
    """Debug the complete token flow"""
    print("🔍 Debugging Token Flow...")
    print("=" * 50)
    
    # Step 1: Login and get tokens
    print("1. Logging in to get tokens...")
    login_data = {
        "email": "satyarth.gaur@aionos.ai",
        "password": "Satya2025#"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            login_result = response.json()
            print("✅ Login successful!")
            
            jwt_token = login_result.get('access_token')
            inferrix_token = login_result.get('inferrix_token')
            
            print(f"   - JWT Token: {jwt_token[:50]}..." if jwt_token else "   - JWT Token: None")
            print(f"   - Inferrix Token: {inferrix_token[:50]}..." if inferrix_token else "   - Inferrix Token: None")
            
            if not inferrix_token:
                print("❌ No Inferrix token received from login!")
                return
            
            # Step 2: Test chat with explicit token logging
            print("\n2. Testing chat with token debugging...")
            headers = {
                "Authorization": f"Bearer {jwt_token}",
                "X-Inferrix-Token": inferrix_token,
                "Content-Type": "application/json"
            }
            
            print(f"   - Sending headers: {headers}")
            
            chat_data = {
                "query": "show me critical alarms for past",
                "user": "satyarth.gaur@aionos.ai",
                "device": None
            }
            
            print(f"   - Sending data: {chat_data}")
            
            response = requests.post(
                "http://localhost:8000/chat/enhanced",
                json=chat_data,
                headers=headers,
                timeout=30
            )
            
            print(f"   - Response status: {response.status_code}")
            print(f"   - Response headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                chat_result = response.json()
                print("✅ Chat request successful!")
                print(f"   - Response: {chat_result.get('response', 'N/A')[:200]}...")
            else:
                print(f"❌ Chat request failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    debug_token_flow() 