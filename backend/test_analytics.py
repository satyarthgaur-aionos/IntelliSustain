#!/usr/bin/env python3
"""
Test script for advanced analytics functionality
"""

import os
import sys
import time

# Set up environment variables for testing
os.environ["AI_PROVIDER"] = "openai"
os.environ["OPENAI_API_KEY"] = "test-key-for-testing"  # This will be overridden if real key exists
os.environ["INFERRIX_API_TOKEN"] = "test-token-for-testing"  # This will be overridden if real token exists

# Try to get real credentials if available (with proper encoding)
if os.path.exists(".env"):
    try:
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
    except Exception as e:
        print(f"Note: Could not read .env file: {e}")

def test_analytics_functionality():
    """Test the analytics functionality with mock data"""
    print("🧪 Testing Advanced Analytics Functionality")
    print("=" * 50)
    
    try:
        # Import after setting environment variables
        from enhanced_agentic_agent import get_enhanced_agentic_agent
        print("✅ Enhanced agentic agent imported successfully")
        
        # Test the context extractor
        print("\n🔍 Testing Context Extractor:")
        extractor = enhanced_agentic_agent.context_extractor
        
        # Test timeframe extraction
        timeframe = extractor.extract_timeframe_info("Show me trends for the last 24 hours")
        print(f"  Timeframe extraction: {timeframe}")
        
        # Test location extraction  
        location = extractor.extract_location_info("What's happening in the east wing?")
        print(f"  Location extraction: {location}")
        
        # Test device extraction
        device = extractor.extract_device_info("Show me data for device 300186")
        print(f"  Device extraction: {device}")
        
        # Test function determination
        print("\n🔍 Testing Function Determination:")
        
        test_queries = [
            "Show me energy usage trends for the last 24 hours",
            "What is the root cause of high temperature?",
            "Give me optimization recommendations",
            "What are the occupancy trends?",
            "Show me alarm trends"
        ]
        
        for query in test_queries:
            device_id = extractor.extract_device_info(query)
            timeframe = extractor.extract_timeframe_info(query)
            location = extractor.extract_location_info(query)
            
            # Mock complex command parsing
            complex_command = {"action": None}
            
            function_name = enhanced_agentic_agent._determine_enhanced_function(
                query, device_id or "", [], complex_command
            )
            
            print(f"  Query: '{query}'")
            print(f"    -> Function: {function_name}")
            print(f"    -> Device: {device_id}")
            print(f"    -> Timeframe: {timeframe}")
            print(f"    -> Location: {location}")
            print()
        
        # Test analytics method directly
        print("🔍 Testing Analytics Method:")
        
        analytics_tests = [
            {
                "name": "Energy Trends",
                "args": {
                    "query": "Show me energy usage trends for the last 24 hours",
                    "device_id": "",
                    "type": ""
                }
            },
            {
                "name": "Root Cause Analysis", 
                "args": {
                    "query": "What is the root cause of high temperature?",
                    "device_id": "300186",
                    "type": ""
                }
            },
            {
                "name": "Optimization Recommendations",
                "args": {
                    "query": "Give me optimization recommendations for energy savings",
                    "device_id": "",
                    "type": ""
                }
            }
        ]
        
        for test in analytics_tests:
            print(f"\n  Testing: {test['name']}")
            try:
                result = enhanced_agentic_agent._get_advanced_analytics(test['args'])
                print(f"    Result: {result[:100]}...")
                print(f"    Length: {len(result)} characters")
                print(f"    Contains analytics: {'✅' if any(x in result.lower() for x in ['trend', 'analysis', 'recommendation', 'forecast', 'root cause']) else '❌'}")
            except Exception as e:
                print(f"    Error: {str(e)}")
        
        print("\n✅ Analytics functionality testing completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        print("This is expected if API keys are not configured for real testing")

if __name__ == "__main__":
    test_analytics_functionality() 