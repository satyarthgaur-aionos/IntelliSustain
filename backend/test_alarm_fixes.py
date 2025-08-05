#!/usr/bin/env python3
"""
Test script to verify alarm and device list query fixes
"""

import requests
import json
import time

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_QUERIES = [
    "show list of all devices with status",
    "show me all major and minor alarms",
    "list all devices",
    "show all alarms",
    "show devices with status",
    "show major alarms",
    "show minor alarms"
]

def test_query(query, device=None):
    """Test a single query"""
    print(f"\n🧪 Testing: '{query}'")
    print("-" * 50)
    
    payload = {
        "query": query,
        "user": "test_user"
    }
    
    if device:
        payload["device"] = device
    
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"📝 Response: {result.get('response', 'No response')}")
            return True
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"❌ Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Backend server not running")
        return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Alarm and Device List Query Fixes")
    print("=" * 60)
    
    # Test if backend is running
    try:
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ Backend is running")
        else:
            print("⚠️ Backend responded but health check failed")
    except:
        print("❌ Backend is not running. Please start the backend server first.")
        print("   Run: python main.py")
        return
    
    # Test all queries
    success_count = 0
    total_count = len(TEST_QUERIES)
    
    for query in TEST_QUERIES:
        if test_query(query):
            success_count += 1
        time.sleep(1)  # Small delay between requests
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {success_count}/{total_count} queries successful")
    
    if success_count == total_count:
        print("🎉 All tests passed! The fixes are working correctly.")
    else:
        print("⚠️ Some tests failed. Check the responses above for details.")

if __name__ == "__main__":
    main() 