#!/usr/bin/env python3
"""
Compare Local vs Railway Environment Variables
"""
import os
import requests
from dotenv import load_dotenv

# Load local environment variables
load_dotenv('backend/.env')

RAILWAY_URL = "https://intellisustain-production.up.railway.app"

def compare_environments():
    """Compare local vs Railway environment variables"""
    print("🔍 ENVIRONMENT VARIABLE COMPARISON")
    print("=" * 60)
    
    # Local environment variables
    print("📁 LOCAL ENVIRONMENT (.env file):")
    local_vars = {
        'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'DATABASE_URL': os.getenv('DATABASE_URL'),
        'INFERRIX_API_TOKEN': os.getenv('INFERRIX_API_TOKEN')
    }
    
    for key, value in local_vars.items():
        status = "✅" if value else "❌"
        preview = f"{value[:20]}..." if value and len(value) > 20 else value
        print(f"  {status} {key}: {preview}")
    
    print("\n🌐 RAILWAY ENVIRONMENT (from screenshot):")
    railway_vars = {
        'JWT_SECRET_KEY': 'ddOk7RPm2RgSxgAkfcgsmKNvWgYIyLf7V3vETiZ_K cE',
        'OPENAI_API_KEY': None,  # Missing
        'GEMINI_API_KEY': None,  # Missing
        'DATABASE_URL': '********',  # Present but masked
        'INFERRIX_API_TOKEN': None  # Removed
    }
    
    for key, value in railway_vars.items():
        status = "✅" if value else "❌"
        preview = f"{value[:20]}..." if value and len(value) > 20 else value
        print(f"  {status} {key}: {preview}")
    
    print("\n" + "=" * 60)
    print("🔍 ANALYSIS:")
    
    # Check what's missing on Railway
    missing_on_railway = []
    for key in ['OPENAI_API_KEY', 'GEMINI_API_KEY']:
        if local_vars.get(key) and not railway_vars.get(key):
            missing_on_railway.append(key)
    
    if missing_on_railway:
        print(f"❌ MISSING ON RAILWAY: {', '.join(missing_on_railway)}")
        print("💡 SOLUTION: Add these to Railway shared variables")
    else:
        print("✅ All required variables are present on Railway")
    
    # Test Railway authentication
    print("\n🧪 TESTING RAILWAY AUTHENTICATION:")
    try:
        login_data = {
            "email": "satyarth.gaur@aionos.ai",
            "password": "Satya2025#"
        }
        response = requests.post(f"{RAILWAY_URL}/login", json=login_data, timeout=10)
        
        if response.status_code == 200:
            login_response = response.json()
            print("✅ Login successful")
            print(f"  - JWT Token: {'✅' if 'access_token' in login_response else '❌'}")
            print(f"  - Inferrix Token: {'✅' if 'inferrix_token' in login_response else '❌'}")
            
            if 'access_token' in login_response:
                # Test chat endpoint
                headers = {"Authorization": f"Bearer {login_response['access_token']}"}
                chat_data = {"query": "Hello", "user": "satyarth.gaur@aionos.ai"}
                
                chat_response = requests.post(f"{RAILWAY_URL}/chat", json=chat_data, headers=headers, timeout=30)
                print(f"  - Chat endpoint: {'✅' if chat_response.status_code == 200 else '❌'} ({chat_response.status_code})")
                
                if chat_response.status_code != 200:
                    print(f"    Error: {chat_response.text}")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    compare_environments()
