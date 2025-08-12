#!/usr/bin/env python3
"""
Simple chat test to verify the complete flow
"""
import requests
import json

def test_simple_chat():
    """Test the complete login and chat flow"""
    print("🧪 Testing Simple Chat Flow...")
    print("=" * 50)
    
    # Step 1: Login
    print("1. Logging in...")
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
            
            if not inferrix_token:
                print("❌ No Inferrix token received")
                return
            
            # Step 2: Test a simple chat query
            print("\n2. Testing simple chat query...")
            headers = {
                "Authorization": f"Bearer {jwt_token}",
                "X-Inferrix-Token": inferrix_token,
                "Content-Type": "application/json"
            }
            
            # Test with a simple query that should work
            chat_data = {
                "query": "Hello, how are you?",
                "user": "satyarth.gaur@aionos.ai",
                "device": None
            }
            
            response = requests.post(
                "http://localhost:8000/chat",
                json=chat_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                chat_result = response.json()
                print("✅ Chat request successful!")
                print(f"   - Response: {chat_result.get('response', 'N/A')[:200]}...")
                print(f"   - Tool used: {chat_result.get('tool', 'N/A')}")
            else:
                print(f"❌ Chat request failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    test_simple_chat() 