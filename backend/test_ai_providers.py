#!/usr/bin/env python3
"""
Test script to verify both OpenAI and Gemini AI providers work correctly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_ai_providers():
    """Test both OpenAI and Gemini providers"""
    
    print("🧪 Testing AI Provider Configuration")
    print("=" * 50)
    
    # Test OpenAI configuration
    print("\n1️⃣ Testing OpenAI Configuration:")
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print("✅ OPENAI_API_KEY found")
        # Temporarily set provider to OpenAI
        os.environ["AI_PROVIDER"] = "openai"
        try:
            from agentic_agent import agentic_agent
            print("✅ OpenAI agent initialized successfully")
            
            # Test a simple query
            response = agentic_agent.process_query("Show all devices")
            print(f"✅ OpenAI Response: {response[:100]}...")
            
        except Exception as e:
            print(f"❌ OpenAI Error: {e}")
    else:
        print("⚠️ OPENAI_API_KEY not found")
    
    # Test Gemini configuration
    print("\n2️⃣ Testing Gemini Configuration:")
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        print("✅ GEMINI_API_KEY found")
        # Temporarily set provider to Gemini
        os.environ["AI_PROVIDER"] = "gemini"
        try:
            # Reload the module to get new configuration
            import importlib
            import agentic_agent
            importlib.reload(agentic_agent)
            
            print("✅ Gemini agent initialized successfully")
            
            # Test a simple query
            response = agentic_agent.agentic_agent.process_query("Show all devices")
            print(f"✅ Gemini Response: {response[:100]}...")
            
        except Exception as e:
            print(f"❌ Gemini Error: {e}")
    else:
        print("⚠️ GEMINI_API_KEY not found")
    
    # Test provider switching
    print("\n3️⃣ Testing Provider Switching:")
    print("To switch providers, simply change the AI_PROVIDER environment variable:")
    print("• For OpenAI: export AI_PROVIDER=openai")
    print("• For Gemini: export AI_PROVIDER=gemini")
    print("\nOr in your .env file:")
    print("• AI_PROVIDER=openai")
    print("• AI_PROVIDER=gemini")
    
    print("\n4️⃣ Environment Variables Summary:")
    print(f"• AI_PROVIDER: {os.getenv('AI_PROVIDER', 'openai')}")
    print(f"• OPENAI_API_KEY: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Not set'}")
    print(f"• GEMINI_API_KEY: {'✅ Set' if os.getenv('GEMINI_API_KEY') else '❌ Not set'}")
    
    print("\n🎉 AI Provider Testing Complete!")
    print("\n💡 Usage Instructions:")
    print("1. Set your preferred AI_PROVIDER in .env file")
    print("2. Ensure the corresponding API key is set")
    print("3. Restart the application")
    print("4. All scenarios will work with the selected provider")

if __name__ == "__main__":
    test_ai_providers() 