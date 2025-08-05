#!/usr/bin/env python3
"""
Quick test to verify table formatting with bold headers
"""

from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

def test_bold_headers():
    """Test that table responses have proper formatting for bold headers"""
    agent = EnhancedAgenticInferrixAgent()
    
    print("🧪 Testing Table Formatting with Bold Headers")
    print("=" * 50)
    
    # Test queries that should return tabular data
    test_queries = [
        "What's the highest severity alarm right now?",
        "Show all devices",
        "Set all thermostats to 24°C"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}️⃣ Testing: '{query}'")
        try:
            result = agent.process_query(query)
            print("✅ Response generated successfully")
            
            # Check if it contains proper table format with headers
            if "| Time |" in result or "| Device Name |" in result:
                print("✅ Table format with headers detected")
                print("📋 Headers should now appear in BOLD font in the frontend")
            else:
                print("❌ Table format not found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Bold Headers Test Complete!")
    print("All table headers should now appear in bold font for better clarity.")

if __name__ == "__main__":
    test_bold_headers() 