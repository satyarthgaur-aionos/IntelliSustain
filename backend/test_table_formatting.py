#!/usr/bin/env python3
"""
Test script to verify table formatting works correctly for all response types
"""

from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

def test_table_formatting():
    """Test that all table responses are properly formatted"""
    agent = EnhancedAgenticInferrixAgent()
    
    print("🧪 Testing Table Formatting for All Response Types")
    print("=" * 60)
    
    # Test 1: Highest severity alarms (should show only CRITICAL)
    print("\n1️⃣ Testing Highest Severity Alarms:")
    print("Query: 'What's the highest severity alarm right now?'")
    try:
        result = agent.process_query("What's the highest severity alarm right now?")
        print("✅ Response generated successfully")
        print("📋 Response preview:")
        print(result[:200] + "..." if len(result) > 200 else result)
        
        # Check if it contains proper table format
        if "| Time |" in result and "| --- |" in result:
            print("✅ Table format detected correctly")
        else:
            print("❌ Table format not found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Device list
    print("\n2️⃣ Testing Device List:")
    print("Query: 'Show all devices'")
    try:
        result = agent.process_query("Show all devices")
        print("✅ Response generated successfully")
        print("📋 Response preview:")
        print(result[:200] + "..." if len(result) > 200 else result)
        
        # Check if it contains proper table format
        if "| Device Name |" in result and "| --- |" in result:
            print("✅ Table format detected correctly")
        else:
            print("❌ Table format not found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Bulk actions
    print("\n3️⃣ Testing Bulk Actions:")
    print("Query: 'Set all thermostats to 24°C'")
    try:
        result = agent.process_query("Set all thermostats to 24°C")
        print("✅ Response generated successfully")
        print("📋 Response preview:")
        print(result[:200] + "..." if len(result) > 200 else result)
        
        # Check if it contains proper table format
        if "| Device Name |" in result and "| --- |" in result:
            print("✅ Table format detected correctly")
        else:
            print("❌ Table format not found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Single device response
    print("\n4️⃣ Testing Single Device Response:")
    print("Query: 'Show temperature for RH/T Sensor - 150002'")
    try:
        result = agent.process_query("Show temperature for RH/T Sensor - 150002")
        print("✅ Response generated successfully")
        print("📋 Response preview:")
        print(result[:200] + "..." if len(result) > 200 else result)
        
        # Check if it contains proper table format
        if "| Device Name |" in result and "| --- |" in result:
            print("✅ Table format detected correctly")
        else:
            print("❌ Table format not found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Table Formatting Test Complete!")
    print("All responses with multiple records should now display in proper table format")
    print("with borders, styling, and vertical scrollbars for large tables.")

if __name__ == "__main__":
    test_table_formatting() 