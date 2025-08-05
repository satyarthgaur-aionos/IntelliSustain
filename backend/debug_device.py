#!/usr/bin/env python3
"""
Debug script to test device diagnosis and understand HTTP errors
"""

import os
os.environ["AI_PROVIDER"] = "openai"
os.environ["OPENAI_API_KEY"] = "test-key-for-testing"
os.environ["INFERRIX_API_TOKEN"] = "test-token-for-testing"

def test_device_diagnosis():
    print("🔍 Testing device diagnosis...")
    
    try:
        from enhanced_agentic_agent import enhanced_agentic_agent
        print("✅ Enhanced agent imported successfully")
        
        # Test device mapping
        device_id = "300186"
        print(f"\nTesting device mapping for: {device_id}")
        
        # Test the mapping function directly
        mapped_id = enhanced_agentic_agent._map_device_name_to_id(device_id)
        print(f"Mapped ID: {mapped_id}")
        
        # Test API request directly
        if mapped_id:
            print(f"\nTesting API request for mapped ID: {mapped_id}")
            try:
                device_data = enhanced_agentic_agent._make_api_request(f"deviceInfos/{mapped_id}")
                print(f"API Response: {device_data}")
            except Exception as e:
                print(f"API Error: {str(e)}")
        
        # Test the full diagnosis
        print(f"\nTesting full diagnosis query...")
        result = enhanced_agentic_agent.process_query(f"Diagnose device {device_id}", "TestUser", device_id)
        print(f"Diagnosis Result: {result[:300]}...")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_device_diagnosis() 