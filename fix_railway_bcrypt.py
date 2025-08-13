#!/usr/bin/env python3
"""
Fix for Railway bcrypt issue
"""
import requests
import json

def test_bcrypt_fix():
    """Test if bcrypt issue is causing the problem"""
    print("🔧 TESTING BCRYPT FIX")
    print("=" * 50)
    
    # Test credentials
    login_data = {
        "email": "satyarth.gaur@aionos.ai",
        "password": "Satya2025#"
    }
    
    print("Testing Railway login with bcrypt fix...")
    
    try:
        response = requests.post(
            "https://intellisustain-production.up.railway.app/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login successful!")
            print(f"JWT Token: {result.get('access_token', 'N/A')[:50]}...")
            print(f"Inferrix Token: {result.get('inferrix_token', 'N/A')[:50] if result.get('inferrix_token') else 'MISSING'}...")
        else:
            print("❌ Login failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_bcrypt_fix()
