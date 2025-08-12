#!/usr/bin/env python3
"""
Test simple token approach - using only the "token" value from Inferrix login
"""
import requests
import json

def test_simple_token_approach():
    """Test the simplified token approach"""
    print("🔐 Testing Simple Token Approach...")
    print("=" * 60)
    
    # Step 1: Login to get the token
    print("1. Logging in to get Inferrix token...")
    login_data = {
        "email": "admin@inferrix.com",
        "password": "admin123"
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
            print(f"   - Local JWT: {login_result.get('access_token', 'N/A')[:50]}...")
            print(f"   - Inferrix Token: {login_result.get('inferrix_token', 'N/A')[:50]}...")
            
            # Step 2: Test API call with the token
            if login_result.get('inferrix_token'):
                print("\n2. Testing API call with Inferrix token...")
                test_api_call(login_result.get('inferrix_token'))
            else:
                print("❌ No Inferrix token received")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")

def test_api_call(token):
    """Test making an API call with the token"""
    try:
        headers = {
            "X-Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Test getting alarms
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

def test_ai_agent_token():
    """Test that the AI agent can get a fresh token"""
    print("\n🤖 Testing AI Agent Token Function...")
    print("=" * 60)
    
    try:
        # Import the AI agent's token function
        import sys
        sys.path.append('backend')
        from enhanced_agentic_agent import get_inferrix_token
        
        token = get_inferrix_token()
        if token:
            print("✅ AI agent token function working!")
            print(f"   - Token obtained: {token[:50]}...")
            
            # Test API call with AI agent token
            print("\n   Testing API call with AI agent token...")
            test_api_call(token)
        else:
            print("❌ AI agent token function failed")
            
    except Exception as e:
        print(f"❌ Error testing AI agent token: {e}")

if __name__ == "__main__":
    print("🚀 Testing Simple Token Approach")
    print("=" * 60)
    
    # Test the simple approach
    test_simple_token_approach()
    
    # Test AI agent token function
    test_ai_agent_token()
    
    print("\n" + "=" * 60)
    print("🎉 Simple token approach testing completed!") 