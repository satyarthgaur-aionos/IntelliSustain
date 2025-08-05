#!/usr/bin/env python3
"""
Test script to verify Hinglish (mixed Hindi-English) support in IntelliSustain
"""

import requests
import json
import time
from ai_magic_core import MultiLanguageSupport

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_USER = "demo_user"

def test_hinglish_detection():
    """Test Hinglish language detection"""
    print("🔍 Testing Hinglish Language Detection")
    print("=" * 50)
    
    test_queries = [
        # Pure English
        ("What is the temperature in room 201?", "en"),
        # Pure Hindi
        ("कमरा 201 में तापमान क्या है?", "hi"),
        # Hinglish - Hindi location + English words
        ("कमरा 201 में temperature क्या है?", "hi"),
        ("Room 201 में temperature check करो", "hi"),
        # Hinglish - English location + Hindi words
        ("North wing में तापमान क्या है?", "hi"),
        ("East wing में humidity check करो", "hi"),
        # Hinglish - Mixed structure
        ("मैं north wing में temperature देखना चाहता हूं", "hi"),
        ("Can you check तापमान in east wing?", "hi"),
        # More complex Hinglish
        ("Server room में temperature और humidity का status क्या है?", "hi"),
        ("Main lobby में occupancy check करो please", "hi"),
    ]
    
    passed = 0
    total = len(test_queries)
    
    for query, expected_lang in test_queries:
        detected = MultiLanguageSupport.detect_language(query)
        is_hinglish = MultiLanguageSupport.is_hinglish(query)
        components = MultiLanguageSupport.extract_hinglish_components(query)
        
        print(f"\n📝 Query: '{query}'")
        print(f"   Expected: {expected_lang}")
        print(f"   Detected: {detected}")
        print(f"   Is Hinglish: {is_hinglish}")
        print(f"   Components: {components}")
        
        if detected == expected_lang:
            print("   ✅ PASSED")
            passed += 1
        else:
            print("   ❌ FAILED")
    
    print(f"\n🎯 Language Detection Results: {passed}/{total} tests passed")
    return passed == total

def test_hinglish_query(query, expected_contains=None, expected_not_contains=None):
    """Test a single Hinglish query and verify the response"""
    print(f"\n🔍 Testing Hinglish Query: '{query}'")
    
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

def test_hinglish_queries():
    """Test various Hinglish queries"""
    print("\n🚀 Testing Hinglish Query Processing")
    print("=" * 50)
    
    tests = [
        # Test 1: Hindi location + English parameter
        {
            "query": "कमरा 201 में temperature क्या है?",
            "expected_contains": ["Temperature for device", "25."],
            "expected_not_contains": ["Please hold on", "fetching data"],
            "description": "Hindi location with English parameter"
        },
        
        # Test 2: English location + Hindi parameter
        {
            "query": "Room 201 में तापमान क्या है?",
            "expected_contains": ["Temperature for device", "25."],
            "expected_not_contains": ["Please hold on", "fetching data"],
            "description": "English location with Hindi parameter"
        },
        
        # Test 3: Mixed structure
        {
            "query": "North wing में temperature और humidity check करो",
            "expected_contains": ["Temperature for device", "Humidity for device"],
            "expected_not_contains": ["Please hold on", "fetching data"],
            "description": "Mixed structure with multiple parameters"
        },
        
        # Test 4: Hindi floor + English words
        {
            "query": "तीसरी मंजिल में temperature क्या है?",
            "expected_contains": ["Temperature for device"],
            "expected_not_contains": ["Please hold on", "fetching data"],
            "description": "Hindi floor with English words"
        },
        
        # Test 5: English floor + Hindi words
        {
            "query": "3rd floor में तापमान और आर्द्रता क्या है?",
            "expected_contains": ["Temperature for device"],
            "expected_not_contains": ["Please hold on", "fetching data"],
            "description": "English floor with Hindi words"
        },
        
        # Test 6: Complex Hinglish
        {
            "query": "Server room में temperature और humidity का status check करो please",
            "expected_contains": ["Temperature for device", "Humidity for device"],
            "expected_not_contains": ["Please hold on", "fetching data"],
            "description": "Complex Hinglish with multiple elements"
        },
        
        # Test 7: Hinglish with device names
        {
            "query": "IAQ Sensor V2 - 300186 का temperature क्या है?",
            "expected_contains": ["Temperature for device 300186"],
            "expected_not_contains": ["Please hold on", "fetching data"],
            "description": "Hinglish with device names"
        },
        
        # Test 8: Hinglish occupancy query
        {
            "query": "Main lobby में occupancy कितनी है?",
            "expected_contains": ["occupancy", "45"],
            "expected_not_contains": ["Please hold on", "fetching data"],
            "description": "Hinglish occupancy query"
        },
        
        # Test 9: Hinglish battery query
        {
            "query": "Device 300186 का battery level क्या है?",
            "expected_contains": ["Battery for device"],
            "expected_not_contains": ["Please hold on", "fetching data"],
            "description": "Hinglish battery query"
        },
        
        # Test 10: Hinglish with Hindi location mapping
        {
            "query": "पूर्वी विंग में temperature क्या है?",
            "expected_contains": ["Temperature for device"],
            "expected_not_contains": ["Please hold on", "fetching data"],
            "description": "Hinglish with Hindi location mapping"
        }
    ]
    
    passed = 0
    total = len(tests)
    
    for i, test in enumerate(tests, 1):
        print(f"\n📋 Test {i}/{total}: {test['description']}")
        if test_hinglish_query(
            test["query"], 
            test.get("expected_contains"), 
            test.get("expected_not_contains")
        ):
            passed += 1
    
    print(f"\n🎯 Hinglish Query Results: {passed}/{total} tests passed")
    return passed == total

def main():
    """Run all Hinglish tests"""
    print("🚀 Testing IntelliSustain Hinglish Support")
    print("=" * 60)
    
    # Test 1: Language detection
    detection_passed = test_hinglish_detection()
    
    # Test 2: Query processing
    query_passed = test_hinglish_queries()
    
    # Overall results
    print(f"\n🎯 Overall Results:")
    print(f"   Language Detection: {'✅ PASSED' if detection_passed else '❌ FAILED'}")
    print(f"   Query Processing: {'✅ PASSED' if query_passed else '❌ FAILED'}")
    
    if detection_passed and query_passed:
        print("\n🎉 All Hinglish tests passed! The system properly handles mixed Hindi-English queries.")
    else:
        print("\n⚠️ Some Hinglish tests failed. The system may need improvements for mixed language support.")
    
    return detection_passed and query_passed

if __name__ == "__main__":
    main() 