#!/usr/bin/env python3
"""
Test All Devices Energy Consumption
"""
import sys
import os

# Add backend directory to Python path
sys.path.append('backend')

def test_all_devices_energy():
    """Test specifically the 'all devices' energy consumption query"""
    print("🔍 TESTING ALL DEVICES ENERGY CONSUMPTION")
    print("=" * 60)
    
    try:
        from enhanced_agentic_agent import get_enhanced_agentic_agent
        
        # Create agent instance
        agent = get_enhanced_agentic_agent()
        
        # Test queries
        queries = [
            "Show me energy consumption for all devices",
            "Show me energy usage on 2nd floor",  # This one works
            "Get energy consumption for all devices"
        ]
        
        for query in queries:
            print(f"\n{'='*50}")
            print(f"Testing query: '{query}'")
            print(f"{'='*50}")
            
            # Process the query
            response = agent.process_query(query, "satyarth.gaur@aionos.ai", "")
            
            print(f"Response: {response}")
            
            # Check response type
            if "Energy Consumption" in response:
                print("✅ Energy consumption data found")
            elif "Device List" in response or "Device Name" in response:
                print("❌ Response contains device list instead of energy consumption")
            elif "No devices found" in response:
                print("❌ No devices found")
            elif "No token provided" in response:
                print("❌ Token issue")
            else:
                print("❓ Unexpected response format")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_all_devices_energy()
