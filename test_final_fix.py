#!/usr/bin/env python3
"""
Test the final fix with correct parameters
"""
import requests
import json

def test_final_fix():
    """Test the final fix with correct username parameter"""
    print("🔧 TESTING FINAL FIX - CORRECT USERNAME PARAMETER")
    print("=" * 60)
    
    # Test credentials
    login_data = {
        "email": "satyarth.gaur@aionos.ai",
        "password": "Satya2025#"
    }
    
    print("Testing Railway login with correct username parameter...")
    
    try:
        response = requests.post(
            "https://intellisustain-production.up.railway.app/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login successful!")
            print(f"JWT Token: {result.get('access_token', 'N/A')[:50]}...")
            print(f"Inferrix Token: {result.get('inferrix_token', 'N/A')[:50] if result.get('inferrix_token') else 'MISSING'}...")
            
            if result.get('inferrix_token'):
                print("🎉 SUCCESS: Railway now gets Inferrix token!")
                print("🔧 The username parameter fix worked!")
                
                # Test chat with the token
                print("\n2️⃣ Testing chat with token...")
                headers = {
                    "Authorization": f"Bearer {result.get('access_token')}",
                    "X-Inferrix-Token": result.get('inferrix_token'),
                    "Content-Type": "application/json"
                }
                
                chat_data = {
                    "query": "List devices with low battery",
                    "user": "satyarth.gaur@aionos.ai",
                    "device": None
                }
                
                chat_response = requests.post(
                    "https://intellisustain-production.up.railway.app/chat/enhanced",
                    json=chat_data,
                    headers=headers,
                    timeout=30
                )
                
                if chat_response.status_code == 200:
                    chat_result = chat_response.json()
                    print("✅ Chat successful!")
                    print(f"Response: {chat_result.get('response', 'No response')[:200]}...")
                else:
                    print(f"❌ Chat failed: {chat_response.text}")
            else:
                print("❌ Still missing Inferrix token - check Railway logs")
        else:
            print(f"❌ Login failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_final_fix()
