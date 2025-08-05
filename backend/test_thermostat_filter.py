#!/usr/bin/env python3
"""
Test Thermostat Filtering
Verify that "Show me all thermostats" works correctly
"""

import os
from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

# Set up environment
os.environ['MOCK_MODE'] = 'true'
os.environ['OPENAI_API_KEY'] = 'demo-key'

def test_thermostat_filter():
    """Test thermostat filtering"""
    print("🧪 TESTING THERMOSTAT FILTERING")
    print("="*50)
    
    agent = EnhancedAgenticInferrixAgent()
    
    # Test queries
    test_queries = [
        "Show me all thermostats",
        "What thermostats are available?",
        "List all thermostats",
        "Show me thermostats in the building"
    ]
    
    for query in test_queries:
        print(f"\n📝 Testing: '{query}'")
        try:
            response = agent.process_query(query, user="TestUser")
            print(f"✅ Response: {response[:200]}...")
            
            # Check if response mentions thermostats
            if 'thermostat' in response.lower():
                print("✅ Response contains thermostat information")
            else:
                print("⚠️  Response doesn't mention thermostats")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print(f"\n{'='*50}")
    print("🎯 TEST COMPLETE")

if __name__ == "__main__":
    test_thermostat_filter() 