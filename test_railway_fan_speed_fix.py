#!/usr/bin/env python3
"""
Test fan speed fix on Railway
"""

import requests
import json
import time

def test_railway_fan_speed_fix():
    """Test fan speed fix on Railway"""
    print("🧪 Testing Fan Speed Fix on Railway")
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
    
    # Test the specific failing patterns
    test_prompts = [
        "Set fan speed to 0 in 2F-Room50-Thermostat",
        "set fan to lowest speed for 2nd floor room 50",
        "Set fan speed in 2F-Room50-Thermostat to 0",
        "set fan to medium speed for 2F-Room50-Thermostat",
        "Set fan speed to 2 in 2F-Room50-Thermostat"
    ]
    
    successful_tests = 0
    failed_tests = 0
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🧪 Test {i}: '{prompt}'")
        print("-" * 40)
        
        try:
            chat_data = {
                "query": prompt,
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
                print(f"📋 Response: {response_text}")
                
                # Check if response contains °C (which it shouldn't for fan speed)
                if '°C' in response_text and 'fan' in response_text.lower():
                    print("⚠️  WARNING: Response contains °C for fan speed!")
                    failed_tests += 1
                else:
                    successful_tests += 1
                    
            else:
                print(f"❌ Failed! Status: {chat_response.status_code}")
                try:
                    error_data = chat_response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Error: {chat_response.text}")
                failed_tests += 1
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            failed_tests += 1
        
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print(f"\n📊 Test Summary:")
    print("=" * 50)
    print(f"✅ Successful tests: {successful_tests}")
    print(f"❌ Failed tests: {failed_tests}")
    total_tests = successful_tests + failed_tests
    if total_tests > 0:
        success_rate = (successful_tests/total_tests)*100
        print(f"📈 Success rate: {success_rate:.1f}%")

if __name__ == "__main__":
    test_railway_fan_speed_fix() 