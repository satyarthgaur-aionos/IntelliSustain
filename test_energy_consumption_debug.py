#!/usr/bin/env python3
"""
Test Energy Consumption Debug
"""
import sys
import os

# Add backend directory to Python path
sys.path.append('backend')

def test_energy_consumption_debug():
    """Test energy consumption with token handling"""
    print("🔍 TESTING ENERGY CONSUMPTION WITH TOKEN")
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
        
        # Test energy consumption query
        query = "Show me energy consumption for all devices"
        user = "satyarth.gaur@aionos.ai"
        
        print(f"\nTesting query: '{query}'")
        print(f"User: {user}")
        
        # Process the query
        response = agent.process_query(query, user, "", test_token)
        
        print(f"\nResponse: {response}")
        
        # Check if response contains energy consumption data
        if "Energy Consumption" in response:
            print("✅ Energy consumption data found in response")
        elif "No token provided" in response:
            print("❌ Token not being passed correctly to API calls")
        elif "Device List" in response or "Device Name" in response:
            print("❌ Response contains device list instead of energy consumption")
        else:
            print("❓ Unexpected response format")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_energy_consumption_debug()
