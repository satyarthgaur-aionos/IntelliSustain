#!/usr/bin/env python3
"""
Debug Energy Consumption Issue
"""
import sys
import os

# Add backend directory to Python path
sys.path.append('backend')

def debug_energy_consumption():
    """Debug the energy consumption issue"""
    print("🔍 DEBUGGING ENERGY CONSUMPTION ISSUE")
    print("=" * 60)
    
    try:
        from enhanced_agentic_agent import get_enhanced_agentic_agent
        
        # Create agent instance
        agent = get_enhanced_agentic_agent()
        
        # Test query
        query = "Show me energy consumption for all devices"
        user = "satyarth.gaur@aionos.ai"
        
        print(f"Testing query: '{query}'")
        print(f"User: {user}")
        
        # Process the query
        response = agent.process_query(query, user, "")
        
        print(f"\nResponse: {response}")
        
        # Check if response contains energy consumption data
        if "Energy Consumption" in response:
            print("✅ Energy consumption data found in response")
        elif "Device List" in response or "Device Name" in response:
            print("❌ Response contains device list instead of energy consumption")
        else:
            print("❓ Unexpected response format")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_energy_consumption()
