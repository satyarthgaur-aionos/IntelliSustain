#!/usr/bin/env python3
"""
Test Railway fix with corrected email parameter
"""
import requests
import json

def test_railway_fix():
    """Test the Railway fix with corrected email parameter"""
    print("🔧 TESTING RAILWAY FIX - CORRECTED EMAIL PARAMETER")
    print("=" * 60)
    
    # Test credentials
    login_data = {
        "email": "satyarth.gaur@aionos.ai",
        "password": "Satya2025#"
    }
    
    print("Testing Railway login with corrected email parameter...")
    
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
                print("🔧 The email parameter fix worked!")
            else:
                print("❌ Still missing Inferrix token - check Railway logs")
        else:
            print(f"❌ Login failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_railway_fix()
