#!/usr/bin/env python3
"""
Test BMS-specific chat queries
"""
import requests
import json

def test_bms_chat():
    """Test BMS-specific chat queries"""
    print("🏢 Testing BMS Chat Queries...")
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
            
            # Step 2: Test BMS queries
            print("\n2. Testing BMS queries...")
            headers = {
                "Authorization": f"Bearer {jwt_token}",
                "X-Inferrix-Token": inferrix_token,
                "Content-Type": "application/json"
            }
            
            # Test queries that should work
            test_queries = [
                "Show me all devices in the system",
                "What is the current temperature?",
                "List all alarms",
                "Show device status"
            ]
            
            for i, query in enumerate(test_queries, 1):
                print(f"\n   Query {i}: {query}")
                chat_data = {
                    "query": query,
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
                    response_text = chat_result.get('response', 'N/A')
                    print(f"   ✅ Response: {response_text[:100]}...")
                else:
                    print(f"   ❌ Failed: {response.status_code}")
                    print(f"      Error: {response.text}")
                    
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    test_bms_chat() 