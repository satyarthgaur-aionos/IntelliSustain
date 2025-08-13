#!/usr/bin/env python3
"""
Debug JWT Token Validation Issues
"""
import requests
import json
import os
from dotenv import load_dotenv

# Load local environment variables
load_dotenv('backend/.env')

RAILWAY_URL = "https://intellisustain-production.up.railway.app"

def debug_jwt_validation():
    """Debug JWT token validation issues"""
    print("🔍 DEBUGGING JWT TOKEN VALIDATION")
    print("=" * 60)
    
    # Test 1: Login and get token
    print("1️⃣ Login and get JWT token...")
    try:
        login_data = {
            "email": "satyarth.gaur@aionos.ai",
            "password": "Satya2025#"
        }
        response = requests.post(f"{RAILWAY_URL}/login", json=login_data, timeout=10)
        
        if response.status_code == 200:
            login_response = response.json()
            print("✅ Login successful")
            
            if 'access_token' in login_response:
                token = login_response['access_token']
                print(f"   - Token length: {len(token)}")
                print(f"   - Token preview: {token[:50]}...")
                
                # Test 2: Try to decode the token manually
                print("\n2️⃣ Testing JWT token structure...")
                try:
                    import jwt
                    from jose import jwt as jose_jwt
                    
                    # Try to decode without verification first
                    decoded = jwt.decode(token, options={"verify_signature": False})
                    print(f"   ✅ Token can be decoded (without verification)")
                    print(f"   - Payload: {decoded}")
                    
                    # Check if we have the right secret key
                    local_secret = os.getenv('JWT_SECRET_KEY')
                    print(f"   - Local JWT_SECRET_KEY: {local_secret[:20] if local_secret else 'None'}...")
                    
                    # Try to verify with local secret
                    try:
                        verified = jwt.decode(token, local_secret, algorithms=["HS256"])
                        print(f"   ✅ Token verified with local secret")
                    except Exception as e:
                        print(f"   ❌ Token verification failed with local secret: {e}")
                        
                except Exception as e:
                    print(f"   ❌ Token decode error: {e}")
                
                # Test 3: Try different authentication methods
                print("\n3️⃣ Testing different authentication methods...")
                
                # Method 1: Standard Bearer token
                headers1 = {"Authorization": f"Bearer {token}"}
                chat_data = {
                    "query": "Hello",
                    "user": "satyarth.gaur@aionos.ai"
                }
                
                print("   Trying standard Bearer token...")
                response = requests.post(f"{RAILWAY_URL}/chat", json=chat_data, headers=headers1, timeout=30)
                print(f"   - Status: {response.status_code}")
                if response.status_code != 200:
                    print(f"   - Error: {response.text}")
                
                # Method 2: Different header format
                headers2 = {"Authorization": f"bearer {token}"}
                print("   Trying lowercase bearer...")
                response = requests.post(f"{RAILWAY_URL}/chat", json=chat_data, headers=headers2, timeout=30)
                print(f"   - Status: {response.status_code}")
                
                # Method 3: Check what the actual error is
                if response.status_code == 401:
                    print("   - Getting detailed error...")
                    try:
                        error_data = response.json()
                        print(f"   - Error details: {error_data}")
                    except:
                        print(f"   - Raw error: {response.text}")
                
            else:
                print("❌ No access_token in login response")
                print(f"   - Response keys: {list(login_response.keys())}")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Test error: {e}")
    
    print("\n" + "=" * 60)
    print("📋 ANALYSIS:")
    print("The issue appears to be with JWT token validation")
    print("Possible causes:")
    print("1. JWT_SECRET_KEY mismatch between token creation and validation")
    print("2. Token format issue")
    print("3. Database connection issue during user lookup")

if __name__ == "__main__":
    debug_jwt_validation()
