#!/usr/bin/env python3
"""
Test script for new features: Assets, Entity Views, and Notifications
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agentic_agent import agentic_agent

def test_new_features():
    """Test the new assets, entity views, and notifications features"""
    
    print("🧪 Testing New Features: Assets, Entity Views, and Notifications\n")
    
    # Test prompts for new features
    test_prompts = [
        "List all assets in the system",
        "Show all entity views", 
        "Show my notifications",
        "Display asset information",
        "Show entity view details",
        "List all alerts"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"Test {i}: {prompt}")
        try:
            result = agentic_agent.process_query(prompt, "TestUser")
            print(f"✅ Result: {result[:200]}{'...' if len(result) > 200 else ''}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        print("-" * 80)
    
    print("\n🎉 New Features Testing Complete!")

if __name__ == "__main__":
    test_new_features() 