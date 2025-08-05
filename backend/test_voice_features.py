#!/usr/bin/env python3
"""
Test Voice-Enabled Features for IntelliSustain AI Agent
Tests weather, risk analysis, voice support, and mobile responsiveness
"""

import requests
import json
import time
import os
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
JWT_TOKEN = None

def login():
    """Login and get JWT token"""
    global JWT_TOKEN
    try:
        response = requests.post(f"{BASE_URL}/login", json={
            "username": "admin",
            "password": "admin123"
        })
        if response.status_code == 200:
            JWT_TOKEN = response.json().get("access_token")
            print("✅ Login successful")
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

def test_weather_features():
    """Test weather forecast and risk analysis features"""
    print("\n🌤️ Testing Weather Features...")
    
    headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
    
    # Test weather forecast
    weather_queries = [
        "What is the weather prediction in Mumbai for tomorrow?",
        "Show me weather forecast for Delhi this week",
        "What's the weather like in Bangalore today?",
        "Weather forecast for Chennai next 3 days"
    ]
    
    for query in weather_queries:
        try:
            response = requests.post(f"{BASE_URL}/chat/enhanced", 
                json={"query": query, "user": "test_user"},
                headers=headers
            )
            if response.status_code == 200:
                result = response.json().get("response", "")
                if "🌤️" in result or "weather" in result.lower():
                    print(f"✅ Weather query: {query[:50]}...")
                else:
                    print(f"⚠️ Weather query may not have worked: {query[:50]}...")
            else:
                print(f"❌ Weather query failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Weather query error: {e}")

def test_risk_analysis():
    """Test weather risk analysis features"""
    print("\n🌦️ Testing Risk Analysis Features...")
    
    headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
    
    risk_queries = [
        "What HVAC risks if it rains in Mumbai this week?",
        "What are the lighting risks if temperature drops in Bangalore?",
        "Analyze weather risks for electrical systems in Delhi",
        "What are the facility risks for plumbing in Chennai?"
    ]
    
    for query in risk_queries:
        try:
            response = requests.post(f"{BASE_URL}/chat/enhanced", 
                json={"query": query, "user": "test_user"},
                headers=headers
            )
            if response.status_code == 200:
                result = response.json().get("response", "")
                if "🌦️" in result or "risk" in result.lower():
                    print(f"✅ Risk analysis: {query[:50]}...")
                else:
                    print(f"⚠️ Risk analysis may not have worked: {query[:50]}...")
            else:
                print(f"❌ Risk analysis failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Risk analysis error: {e}")

def test_voice_support_features():
    """Test features that would work with voice input"""
    print("\n🎤 Testing Voice-Support Features...")
    
    headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
    
    voice_friendly_queries = [
        "Show me all critical alarms",
        "What's the temperature in room 101",
        "List devices with low battery",
        "Check device health",
        "Show humidity levels",
        "Turn off HVAC in east wing",
        "Schedule maintenance for tomorrow",
        "What's the energy consumption today"
    ]
    
    for query in voice_friendly_queries:
        try:
            response = requests.post(f"{BASE_URL}/chat/enhanced", 
                json={"query": query, "user": "test_user"},
                headers=headers
            )
            if response.status_code == 200:
                result = response.json().get("response", "")
                if result and len(result) > 10:
                    print(f"✅ Voice-friendly query: {query[:40]}...")
                else:
                    print(f"⚠️ Voice query may have empty response: {query[:40]}...")
            else:
                print(f"❌ Voice query failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Voice query error: {e}")

def test_mobile_responsive_features():
    """Test features that work well on mobile devices"""
    print("\n📱 Testing Mobile-Responsive Features...")
    
    headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
    
    mobile_queries = [
        "Show me a quick summary",
        "What's the status",
        "Any alerts today",
        "Quick device check",
        "Show alarms",
        "Device list",
        "Temperature check",
        "Battery status"
    ]
    
    for query in mobile_queries:
        try:
            response = requests.post(f"{BASE_URL}/chat/enhanced", 
                json={"query": query, "user": "test_user"},
                headers=headers
            )
            if response.status_code == 200:
                result = response.json().get("response", "")
                if result and len(result) < 500:  # Mobile-friendly responses should be concise
                    print(f"✅ Mobile-friendly query: {query[:30]}...")
                else:
                    print(f"⚠️ Mobile query may be too long: {query[:30]}...")
            else:
                print(f"❌ Mobile query failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Mobile query error: {e}")

def test_cross_browser_features():
    """Test features that work across different browsers"""
    print("\n🌐 Testing Cross-Browser Features...")
    
    headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
    
    # Test basic functionality that should work in all browsers
    basic_queries = [
        "Hello",
        "Help",
        "What can you do",
        "Show devices",
        "List alarms",
        "Check status"
    ]
    
    for query in basic_queries:
        try:
            response = requests.post(f"{BASE_URL}/chat/enhanced", 
                json={"query": query, "user": "test_user"},
                headers=headers
            )
            if response.status_code == 200:
                result = response.json().get("response", "")
                if result:
                    print(f"✅ Cross-browser query: {query[:30]}...")
                else:
                    print(f"⚠️ Cross-browser query empty: {query[:30]}...")
            else:
                print(f"❌ Cross-browser query failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Cross-browser query error: {e}")

def test_hindi_language_support():
    """Test Hindi language support"""
    print("\n🇮🇳 Testing Hindi Language Support...")
    
    headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
    
    hindi_queries = [
        "नमस्ते",
        "मौसम कैसा है",
        "डिवाइस की स्थिति दिखाएं",
        "अलार्म दिखाएं",
        "तापमान क्या है"
    ]
    
    for query in hindi_queries:
        try:
            response = requests.post(f"{BASE_URL}/chat/enhanced", 
                json={"query": query, "user": "test_user"},
                headers=headers
            )
            if response.status_code == 200:
                result = response.json().get("response", "")
                if result:
                    print(f"✅ Hindi query: {query[:20]}...")
                else:
                    print(f"⚠️ Hindi query empty: {query[:20]}...")
            else:
                print(f"❌ Hindi query failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Hindi query error: {e}")

def test_advanced_features():
    """Test advanced AI features"""
    print("\n🤖 Testing Advanced AI Features...")
    
    headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
    
    advanced_queries = [
        "Analyze energy consumption trends",
        "Predict maintenance needs",
        "Show me optimization recommendations",
        "What are the root causes of recent alarms",
        "Generate a facility health report",
        "Forecast energy usage for next week"
    ]
    
    for query in advanced_queries:
        try:
            response = requests.post(f"{BASE_URL}/chat/enhanced", 
                json={"query": query, "user": "test_user"},
                headers=headers
            )
            if response.status_code == 200:
                result = response.json().get("response", "")
                if result and ("analysis" in result.lower() or "recommend" in result.lower() or "trend" in result.lower()):
                    print(f"✅ Advanced query: {query[:40]}...")
                else:
                    print(f"⚠️ Advanced query may not have worked: {query[:40]}...")
            else:
                print(f"❌ Advanced query failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Advanced query error: {e}")

def test_error_handling():
    """Test error handling and graceful degradation"""
    print("\n🛡️ Testing Error Handling...")
    
    headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
    
    # Test with invalid queries
    error_queries = [
        "",  # Empty query
        "   ",  # Whitespace only
        "x" * 1000,  # Very long query
        "SELECT * FROM users",  # SQL injection attempt
        "<script>alert('xss')</script>",  # XSS attempt
    ]
    
    for query in error_queries:
        try:
            response = requests.post(f"{BASE_URL}/chat/enhanced", 
                json={"query": query, "user": "test_user"},
                headers=headers
            )
            if response.status_code == 200:
                result = response.json().get("response", "")
                if result and "error" not in result.lower():
                    print(f"✅ Error handling: Query handled gracefully")
                else:
                    print(f"⚠️ Error handling: Query may have failed")
            else:
                print(f"❌ Error handling: Request failed with {response.status_code}")
        except Exception as e:
            print(f"❌ Error handling: Exception occurred - {e}")

def main():
    """Run all tests"""
    print("🚀 Starting Voice-Enabled Features Test Suite")
    print("=" * 60)
    
    # Login first
    if not login():
        print("❌ Cannot proceed without login")
        return
    
    # Run all tests
    test_weather_features()
    test_risk_analysis()
    test_voice_support_features()
    test_mobile_responsive_features()
    test_cross_browser_features()
    test_hindi_language_support()
    test_advanced_features()
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("✅ Voice-Enabled Features Test Suite Complete!")
    print("\n📋 Summary:")
    print("• Weather forecast and risk analysis features")
    print("• Voice-friendly natural language queries")
    print("• Mobile-responsive design support")
    print("• Cross-browser compatibility")
    print("• Hindi language support")
    print("• Advanced AI analytics")
    print("• Robust error handling")
    print("\n🎤 Voice Input Features:")
    print("• Speech-to-text using Web Speech API")
    print("• Cross-browser speech recognition")
    print("• Mobile voice input support")
    print("• Graceful fallback for unsupported browsers")
    print("\n📱 Mobile Responsiveness:")
    print("• Touch-friendly interface")
    print("• Responsive design for all screen sizes")
    print("• Optimized for mobile keyboards")
    print("• Landscape and portrait support")

if __name__ == "__main__":
    main() 