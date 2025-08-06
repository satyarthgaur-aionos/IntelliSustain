#!/usr/bin/env python3
"""
Force recreate tech user in Railway database
"""

import requests
import json

def force_recreate_tech_user():
    """Force recreate tech user by triggering a database update"""
    print("🔧 Force Recreating Tech User")
    print("=" * 40)
    
    # Railway URL
    base_url = "https://intellisustain-production.up.railway.app"
    
    # First, let's trigger a health check to see if we can restart the app
    try:
        print("🔄 Triggering health check to restart app...")
        health_response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Health status: {health_response.status_code}")
        
        if health_response.status_code == 200:
            print("✅ App is running")
            
            # Try to access the API info to trigger any startup logic
            print("🔄 Triggering API info to run startup logic...")
            api_response = requests.get(f"{base_url}/api", timeout=10)
            print(f"API status: {api_response.status_code}")
            
            if api_response.status_code == 200:
                print("✅ API is accessible")
                
                # Now test the tech user login again
                print("\n🧪 Testing tech user login...")
                login_data = {
                    "email": "tech@intellisustain.com",
                    "password": "Demo@1234"
                }
                
                login_response = requests.post(
                    f"{base_url}/login",
                    json=login_data,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                print(f"Login status: {login_response.status_code}")
                
                if login_response.status_code == 200:
                    print("✅ Tech user login successful!")
                    response_data = login_response.json()
                    print(f"Token: {response_data.get('access_token', 'No token')[:20]}...")
                else:
                    print("❌ Tech user login still failing")
                    try:
                        error_data = login_response.json()
                        print(f"Error: {error_data.get('detail', 'Unknown error')}")
                    except:
                        print(f"Error: {login_response.text}")
            else:
                print("❌ API not accessible")
        else:
            print("❌ App not running")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n🚀 Next Steps:")
    print("1. Check Railway logs for any errors")
    print("2. Manually trigger a redeploy in Railway")
    print("3. Check if DATABASE_URL is correctly set")
    print("4. Verify the tech user exists in the database")

if __name__ == "__main__":
    force_recreate_tech_user() 