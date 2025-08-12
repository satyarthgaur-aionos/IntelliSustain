#!/usr/bin/env python3
"""
Simple test for Railway fan speed
"""

import requests
import json

def test_simple_fan_speed():
    """Test simple fan speed on Railway"""
    print("🧪 Testing Simple Fan Speed on Railway")
    print("=" * 50)
    
    # Railway URL
    base_url = "https://intellisustain-production.up.railway.app"
    
    # Test credentials
    login_data = {
        "email": "admin@inferrix.com",
        "password": "admin123"
    }
    
    # First, get authentication token
    try:
        print("🔐 Getting authentication token...")
        login_response = requests.post(
            f"{base_url}/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get('access_token')
            print("✅ Authentication successful!")
        else:
            print("❌ Authentication failed")
            return
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return
    
    # Headers for authenticated requests
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # Test the working pattern first
    test_query = "Set fan speed in 2F-Room50-Thermostat to 0"
    
    print(f"\n🧪 Testing: '{test_query}'")
    print("-" * 40)
    
    try:
        # Test chat endpoint
        chat_data = {
            "query": test_query,
            "user": "admin@inferrix.com",
            "device": None
        }
        
        chat_response = requests.post(
            f"{base_url}/chat",
            json=chat_data,
            headers=headers,
            timeout=45
        )
        
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            response_text = response_data.get('response', '')
            tool_used = response_data.get('tool', 'unknown')
            
            print(f"✅ Success! Tool: {tool_used}")
            print(f"📋 Full Response:")
            print(response_text)
            
        else:
            print(f"❌ Failed! Status: {chat_response.status_code}")
            try:
                error_data = chat_response.json()
                print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   Error: {chat_response.text}")
                
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_simple_fan_speed() 