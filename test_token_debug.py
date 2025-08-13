#!/usr/bin/env python3
"""
Test Token Debug
"""
import sys
import os

# Add backend directory to Python path
sys.path.append('backend')

def test_token_debug():
    """Test token handling in the enhanced agentic agent"""
    print("🔍 TESTING TOKEN HANDLING")
    print("=" * 60)
    
    try:
        from enhanced_agentic_agent import get_enhanced_agentic_agent
        
        # Create agent instance
        agent = get_enhanced_agentic_agent()
        
        # Test token setting
        test_token = "test_token_123"
        print(f"Setting token: {test_token}")
        agent.set_api_token(test_token)
        
        # Check if token was set
        print(f"Token stored: {getattr(agent, '_api_token', 'NOT SET')}")
        
        # Test API request
        print("\nTesting API request...")
        result = agent._make_api_request("user/devices?pageSize=1&page=0")
        print(f"API result: {result}")
        
        if "error" in result:
            print(f"❌ API call failed: {result.get('error', 'Unknown error')}")
        else:
            print("✅ API call successful")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_token_debug()
