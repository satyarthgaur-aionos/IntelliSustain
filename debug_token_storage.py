#!/usr/bin/env python3
"""
Debug Token Storage
"""
import sys
import os

# Add backend directory to Python path
sys.path.append('backend')

def debug_token_storage():
    """Debug token storage in the agent"""
    print("🔍 DEBUGGING TOKEN STORAGE")
    print("=" * 60)
    
    try:
        from enhanced_agentic_agent import get_enhanced_agentic_agent
        
        # Create agent instance
        agent = get_enhanced_agentic_agent()
        
        # Check initial token state
        print(f"Initial token: {getattr(agent, '_api_token', 'NOT SET')}")
        
        # Test token setting
        test_token = "test_token_123"
        print(f"\nSetting token: {test_token}")
        agent.set_api_token(test_token)
        
        # Check if token was set
        print(f"Token after setting: {getattr(agent, '_api_token', 'NOT SET')}")
        
        # Test direct attribute access
        print(f"Direct attribute access: {agent._api_token}")
        
        # Test getattr
        print(f"getattr result: {getattr(agent, '_api_token', 'NOT SET')}")
        
        # Test hasattr
        print(f"hasattr _api_token: {hasattr(agent, '_api_token')}")
        
        # Test dir to see all attributes
        print(f"\nAll attributes containing 'token':")
        for attr in dir(agent):
            if 'token' in attr.lower():
                print(f"  {attr}: {getattr(agent, attr, 'NOT ACCESSIBLE')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_token_storage()
