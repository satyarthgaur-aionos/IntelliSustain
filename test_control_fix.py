#!/usr/bin/env python3
"""
Quick test to verify control command fixes
"""
import requests
import json

def test_control_fix():
    """Test the control command fixes"""
    print("🔧 Testing Control Command Fixes...")
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
            
            # Setup headers
            headers = {
                "Authorization": f"Bearer {jwt_token}",
                "X-Inferrix-Token": inferrix_token,
                "Content-Type": "application/json"
            }
            
            # Test control commands that were failing
            test_prompts = [
                "Set temperature in 2F-Room50-Thermostat to 24 degrees",
                "Set fan speed to 0 in 2F-Room50-Thermostat",
                "Increase the fan speed in second floor room no 50 to high speed"
            ]
            
            for i, prompt in enumerate(test_prompts, 1):
                print(f"\n{i}. Testing: {prompt}")
                
                try:
                    chat_data = {
                        "query": prompt,
                        "user": "satyarth.gaur@aionos.ai",
                        "device": None
                    }
                    
                    response = requests.post(
                        "http://localhost:8000/chat/enhanced",
                        json=chat_data,
                        headers=headers,
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        chat_result = response.json()
                        response_text = chat_result.get('response', '')
                        
                        if response_text and not response_text.startswith("❌"):
                            print(f"   ✅ Success: {response_text[:100]}...")
                        else:
                            print(f"   ❌ Failed: {response_text}")
                    else:
                        print(f"   ❌ HTTP Error: {response.status_code}")
                        print(f"   Error: {response.text}")
                        
                except Exception as e:
                    print(f"   ❌ Exception: {e}")
                    
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    test_control_fix() 