#!/usr/bin/env python3
"""
Verification script to test corrected API endpoints
"""

import requests
import json
import time
import os

# Test configuration
BASE_URL = "http://localhost:8000"
INFERRIX_API_TOKEN = os.getenv("INFERRIX_API_TOKEN", "").strip()

def test_inferrix_endpoint(endpoint, description):
    """Test a direct Inferrix API endpoint"""
    print(f"\n🧪 Testing: {description}")
    print(f"📍 Endpoint: {endpoint}")
    print("-" * 60)
    
    headers = {
        "Authorization": f"Bearer {INFERRIX_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        url = f"https://cloud.inferrix.com/api/{endpoint}"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"📊 Response: {len(str(data))} characters")
            if 'data' in data:
                print(f"📈 Data count: {len(data['data'])} items")
            return True
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_backend_endpoint(endpoint, description):
    """Test a backend endpoint"""
    print(f"\n🧪 Testing: {description}")
    print(f"📍 Endpoint: {endpoint}")
    print("-" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"📊 Response: {len(str(data))} characters")
            return True
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    """Main verification function"""
    print("🔍 API Endpoint Verification")
    print("=" * 60)
    
    if not INFERRIX_API_TOKEN:
        print("❌ INFERRIX_API_TOKEN not set. Please set the environment variable.")
        return
    
    # Test core endpoints that were fixed
    endpoints_to_test = [
        # Device endpoints
        ("user/devices?pageSize=10&page=0", "Device List Endpoint"),
        ("user/devices?pageSize=5&page=0", "Device List with Sorting"),
        
        # Alarm endpoints
        ("alarms?pageSize=10&page=0", "Alarm List Endpoint"),
        ("alarms?searchStatus=MAJOR&pageSize=5&page=0", "Major Alarms Endpoint"),
        
        # Asset endpoints
        ("assetInfos/all?pageSize=10&page=0", "Asset List Endpoint"),
        
        # Entity view endpoints
        ("entityViewInfos/all?pageSize=10&page=0", "Entity View List Endpoint"),
        
        # Notification endpoints
        ("notification/requests?pageSize=10&page=0", "Notification Requests Endpoint"),
    ]
    
    # Test backend endpoints
    backend_endpoints = [
        ("/inferrix/devices", "Backend Device Endpoint"),
        ("/health", "Backend Health Check"),
        ("/", "Backend Root Endpoint"),
    ]
    
    print("\n🚀 Testing Direct Inferrix API Endpoints")
    print("=" * 60)
    
    success_count = 0
    total_count = len(endpoints_to_test)
    
    for endpoint, description in endpoints_to_test:
        if test_inferrix_endpoint(endpoint, description):
            success_count += 1
        time.sleep(1)  # Small delay between requests
    
    print(f"\n📊 Direct API Results: {success_count}/{total_count} successful")
    
    print("\n🚀 Testing Backend Endpoints")
    print("=" * 60)
    
    backend_success = 0
    backend_total = len(backend_endpoints)
    
    for endpoint, description in backend_endpoints:
        if test_backend_endpoint(endpoint, description):
            backend_success += 1
        time.sleep(1)
    
    print(f"\n📊 Backend Results: {backend_success}/{backend_total} successful")
    
    print("\n" + "=" * 60)
    print(f"🎯 Overall Results:")
    print(f"   Direct API: {success_count}/{total_count}")
    print(f"   Backend: {backend_success}/{backend_total}")
    print(f"   Total: {success_count + backend_success}/{total_count + backend_total}")
    
    if success_count + backend_success == total_count + backend_total:
        print("🎉 All endpoints are working correctly!")
    else:
        print("⚠️ Some endpoints need attention. Check the errors above.")

if __name__ == "__main__":
    main() 