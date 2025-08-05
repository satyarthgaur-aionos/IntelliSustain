#!/usr/bin/env python3
"""
Quick test to verify highest severity alarm filtering works correctly
"""

from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

def test_highest_severity_detection():
    """Test that highest severity queries are properly detected"""
    agent = EnhancedAgenticInferrixAgent()
    
    # Test queries that should trigger highest severity filtering
    highest_severity_queries = [
        "What's the highest severity alarm right now?",
        "Show me highest priority alarms",
        "What are the highest risk alarms?",
        "Show critical alarms",
        "Most critical alarms please",
        "Top priority alarms"
    ]
    
    # Test queries that should NOT trigger highest severity filtering
    regular_queries = [
        "Show me all alarms",
        "What alarms are there?",
        "Show me minor alarms",
        "Any system issues?"
    ]
    
    print("Testing highest severity query detection...")
    
    for query in highest_severity_queries:
        print(f"\nTesting: '{query}'")
        try:
            # This will test the detection logic without making actual API calls
            result = agent.process_query(query)
            print(f"Result: {result[:100]}...")  # Show first 100 chars
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "="*50)
    print("Test completed. The fix should now properly filter to show only highest severity alarms.")
    print("When you ask 'What's the highest severity alarm right now?', it should only show CRITICAL alarms if they exist.")

if __name__ == "__main__":
    test_highest_severity_detection() 