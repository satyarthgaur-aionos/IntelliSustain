#!/usr/bin/env python3
"""
Debug script to test alarm queries and check for truncation
"""

import os
os.environ["AI_PROVIDER"] = "openai"
os.environ["OPENAI_API_KEY"] = "test-key-for-testing"
os.environ["INFERRIX_API_TOKEN"] = "test-token-for-testing"

def test_alarm_queries():
    print("🔍 Testing alarm queries...")
    
    try:
        from enhanced_agentic_agent import get_enhanced_agentic_agent
        print("✅ Enhanced agent imported successfully")
        
        # Test alarm query
        query = "what are the current alarms in the system?"
        print(f"\nQuery: {query}")
        
        result = enhanced_agentic_agent.process_query(query, "TestUser")
        
        print(f"Response length: {len(result)}")
        print(f"Contains truncation: {'...and' in result or '... more' in result}")
        print(f"Response preview: {result[:300]}...")
        
        # Check if it's using the right function
        print(f"\nFunction determination test:")
        device_id = enhanced_agentic_agent.context_extractor.extract_device_info(query)
        complex_command = {"action": None}
        function_name = enhanced_agentic_agent._determine_enhanced_function(query, device_id or "", [], complex_command)
        print(f"  Function: {function_name}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_alarm_queries() 