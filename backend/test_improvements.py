#!/usr/bin/env python3
"""
Test script to verify all improvements to the IntelliSustain system
"""

import requests
import json
import time

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_USER = "demo_user"

def test_query(query, expected_contains=None, expected_not_contains=None):
    """Test a single query and verify the response"""
    print(f"\n🔍 Testing: '{query}'")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"query": query, "user": TEST_USER},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            response_text = data.get('response', '')
            print(f"✅ Status: {response.status_code}")
            print(f"📝 Response: {response_text[:200]}...")
            
            # Check for placeholder responses
            placeholder_phrases = [
                "Please hold on", "fetching data", "assuming successful", 
                "executing API call", "gathering data", "retrieving data",
                "Please allow me", "hold on for a moment"
            ]
            
            has_placeholder = any(phrase.lower() in response_text.lower() for phrase in placeholder_phrases)
            if has_placeholder:
                print("❌ FAILED: Contains placeholder response")
                return False
            
            # Check for expected content
            if expected_contains:
                if not any(content.lower() in response_text.lower() for content in expected_contains):
                    print(f"❌ FAILED: Expected content not found: {expected_contains}")
                    return False
            
            # Check for unexpected content
            if expected_not_contains:
                if any(content.lower() in response_text.lower() for content in expected_not_contains):
                    print(f"❌ FAILED: Unexpected content found: {expected_not_contains}")
                    return False
            
            print("✅ PASSED")
            return True
            
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: Exception - {str(e)}")
        return False

def main():
    """Run all improvement tests"""
    print("🚀 Testing IntelliSustain Improvements")
    print("=" * 50)
    
    tests = [
        # Test 1: Eliminate placeholder responses
        {
            "query": "What's the environmental status in Conference Room B?",
            "expected_not_contains": ["Please hold on", "fetching data", "assuming successful"],
            "description": "Should not contain placeholder responses"
        },
        
        # Test 2: Better location handling for ambiguous locations
        {
            "query": "Show environmental data for the north wing",
            "expected_contains": ["North Wing includes", "sub-locations", "particular room"],
            "description": "Should provide sub-location guidance"
        },
        
        # Test 3: Available locations guidance
        {
            "query": "What's the temperature in unknown location?",
            "expected_contains": ["Available Locations", "Floors", "Wings", "Rooms"],
            "description": "Should show available locations when location not found"
        },
        
        # Test 4: Real data for mapped locations
        {
            "query": "What is the current temperature and occupancy in zone 4?",
            "expected_contains": ["Temperature for device", "25."],
            "expected_not_contains": ["Please hold on", "fetching data"],
            "description": "Should return real data for mapped locations"
        },
        
        # Test 5: Consistent formatting
        {
            "query": "Check occupancy levels in Tower A",
            "expected_contains": ["👥", "📊", "✅"],
            "description": "Should use consistent markdown formatting with emojis"
        },
        
        # Test 6: Hindi support
        {
            "query": "कमरा 201 में तापमान क्या है?",
            "expected_contains": ["Temperature for device"],
            "expected_not_contains": ["Please hold on", "fetching data"],
            "description": "Should handle Hindi queries correctly"
        },
        
        # Test 7: Device-specific queries
        {
            "query": "Show temperature for IAQ Sensor V2 - 300186",
            "expected_contains": ["Temperature for device 300186"],
            "expected_not_contains": ["Please hold on", "fetching data"],
            "description": "Should handle device-specific queries"
        },
        
        # Test 8: Error handling for unmapped locations
        {
            "query": "What's the temperature in non-existent room?",
            "expected_contains": ["not found", "Available Locations"],
            "description": "Should provide helpful error messages for unmapped locations"
        },
        
        # Test 9: Multi-device queries
        {
            "query": "Show temperature and humidity in the east wing",
            "expected_contains": ["Temperature for device", "Humidity for device"],
            "expected_not_contains": ["Please hold on", "fetching data"],
            "description": "Should handle multi-device queries"
        },
        
        # Test 10: Battery and device health
        {
            "query": "What's the battery level of device 300186?",
            "expected_contains": ["Battery for device"],
            "expected_not_contains": ["Please hold on", "fetching data"],
            "description": "Should handle battery queries"
        }
    ]
    
    passed = 0
    total = len(tests)
    
    for i, test in enumerate(tests, 1):
        print(f"\n📋 Test {i}/{total}: {test['description']}")
        if test_query(
            test["query"], 
            test.get("expected_contains"), 
            test.get("expected_not_contains")
        ):
            passed += 1
    
    print(f"\n🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All improvements are working correctly!")
    else:
        print("⚠️ Some improvements need attention")
    
    return passed == total

if __name__ == "__main__":
    main() 