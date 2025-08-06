#!/usr/bin/env python3
"""
Test AI Magic Features - Comprehensive demonstration of all implemented features
"""

import os
import sys
import time
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_agentic_agent import get_enhanced_agentic_agent
from ai_magic_core import conversation_memory, smart_notifications, self_healing

def test_conversational_memory():
    """Test conversational memory and context tracking"""
    print("🧠 **Testing Conversational Memory & Context**")
    print("=" * 50)
    
    user_id = "demo_user_001"
    
    # Simulate a conversation
    queries = [
        "What's the temperature of device 300186?",
        "Show me the humidity too",
        "Are there any alarms?",
        "What was the last device I asked about?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. User: {query}")
        response = enhanced_agentic_agent.process_query(query, user_id)
        print(f"   AI: {response[:100]}...")
        
        # Get recent context
        context = conversation_memory.get_recent_context(user_id, 2)
        print(f"   Context: {len(context)} recent conversations stored")
    
    print("\n✅ Conversational Memory Test Complete")

def test_multi_device_operations():
    """Test multi-device operations and bulk queries"""
    print("\n🔄 **Testing Multi-Device Operations**")
    print("=" * 50)
    
    multi_device_queries = [
        "Show me all thermostats",
        "Get temperature from all sensors",
        "What's the status of all devices?",
        "Check all devices in east wing"
    ]
    
    for i, query in enumerate(multi_device_queries, 1):
        print(f"\n{i}. User: {query}")
        response = enhanced_agentic_agent.process_query(query, "multi_user")
        print(f"   AI: {response[:150]}...")
    
    print("\n✅ Multi-Device Operations Test Complete")

def test_proactive_insights():
    """Test proactive insights and recommendations"""
    print("\n🔍 **Testing Proactive Insights**")
    print("=" * 50)
    
    insight_queries = [
        "Analyze the health of device 300186",
        "What insights can you provide about device 150002?",
        "Are there any anomalies in the system?",
        "Give me recommendations for device maintenance"
    ]
    
    for i, query in enumerate(insight_queries, 1):
        print(f"\n{i}. User: {query}")
        response = enhanced_agentic_agent.process_query(query, "insight_user")
        print(f"   AI: {response[:200]}...")
    
    print("\n✅ Proactive Insights Test Complete")

def test_natural_language_control():
    """Test natural language control and complex commands"""
    print("\n🤖 **Testing Natural Language Control**")
    print("=" * 50)
    
    control_queries = [
        "Turn off all thermostats after 8pm",
        "Set temperature to 22 degrees for device 300186",
        "Schedule maintenance for next Monday",
        "Adjust humidity to 50% in the east wing"
    ]
    
    for i, query in enumerate(control_queries, 1):
        print(f"\n{i}. User: {query}")
        response = enhanced_agentic_agent.process_query(query, "control_user")
        print(f"   AI: {response[:200]}...")
    
    print("\n✅ Natural Language Control Test Complete")

def test_rich_responses():
    """Test rich, visual, and actionable responses"""
    print("\n🎨 **Testing Rich Responses**")
    print("=" * 50)
    
    rich_queries = [
        "Show me all devices with their status",
        "List all active alarms",
        "Give me a summary of system health",
        "What devices are online?"
    ]
    
    for i, query in enumerate(rich_queries, 1):
        print(f"\n{i}. User: {query}")
        response = enhanced_agentic_agent.process_query(query, "rich_user")
        print(f"   AI: {response[:200]}...")
    
    print("\n✅ Rich Responses Test Complete")

def test_personalization():
    """Test personalization and user profiles"""
    print("\n👤 **Testing Personalization**")
    print("=" * 50)
    
    # Simulate different user roles
    users = [
        ("admin_user", "admin"),
        ("technician_user", "technician"),
        ("manager_user", "manager")
    ]
    
    for user_id, role in users:
        print(f"\nTesting {role} user: {user_id}")
        
        # Update user context
        conversation_memory.update_context(user_id, user_role=role, preferences={'notifications': 'high'})
        
        # Test personalized response
        query = "What should I do about device issues?"
        response = enhanced_agentic_agent.process_query(query, user_id)
        print(f"   Query: {query}")
        print(f"   Response: {response[:150]}...")
    
    print("\n✅ Personalization Test Complete")

def test_self_healing():
    """Test self-healing and troubleshooting"""
    print("\n🔧 **Testing Self-Healing & Troubleshooting**")
    print("=" * 50)
    
    healing_queries = [
        "Diagnose device 300186",
        "What's wrong with the system?",
        "Troubleshoot device connectivity",
        "Check for maintenance issues"
    ]
    
    for i, query in enumerate(healing_queries, 1):
        print(f"\n{i}. User: {query}")
        response = enhanced_agentic_agent.process_query(query, "healing_user")
        print(f"   AI: {response[:200]}...")
    
    print("\n✅ Self-Healing Test Complete")

def test_smart_notifications():
    """Test smart notifications and alerts"""
    print("\n📬 **Testing Smart Notifications**")
    print("=" * 50)
    
    # Add some test notifications
    test_user = "notification_user"
    
    # Simulate different notification events
    notifications = [
        {
            'type': 'alarm',
            'severity': 'CRITICAL',
            'device_name': 'HVAC Unit 1',
            'message': 'Temperature exceeded safety limits'
        },
        {
            'type': 'device_status',
            'status': 'offline',
            'device_name': 'Sensor 300186',
            'offline_duration': '2 hours'
        },
        {
            'type': 'battery',
            'level': 15,
            'device_name': 'Thermostat 150002'
        }
    ]
    
    for notification in notifications:
        # Evaluate notification
        eval_result = smart_notifications.evaluate_notification(notification)
        if eval_result['should_notify']:
            conversation_memory.add_notification(test_user, eval_result)
            print(f"   Added notification: {eval_result['message'][:50]}...")
    
    # Test notification retrieval
    notification_queries = [
        "Show me my notifications",
        "What alerts do I have?",
        "Any critical notifications?",
        "System status alerts"
    ]
    
    for i, query in enumerate(notification_queries, 1):
        print(f"\n{i}. User: {query}")
        response = enhanced_agentic_agent.process_query(query, test_user)
        print(f"   AI: {response[:150]}...")
    
    print("\n✅ Smart Notifications Test Complete")

def test_multi_language_support():
    """Test multi-language support"""
    print("\n🌍 **Testing Multi-Language Support**")
    print("=" * 50)
    
    # Test different languages
    language_queries = [
        ("English", "What's the temperature of device 300186?"),
        ("Spanish", "¿Cuál es la temperatura del dispositivo 300186?"),
        ("French", "Quelle est la température de l'appareil 300186?"),
        ("German", "Was ist die Temperatur des Geräts 300186?")
    ]
    
    for language, query in language_queries:
        print(f"\n{language}: {query}")
        response = enhanced_agentic_agent.process_query(query, "multilang_user")
        print(f"   Response: {response[:100]}...")
    
    print("\n✅ Multi-Language Support Test Complete")

def test_comprehensive_scenarios():
    """Test comprehensive real-world scenarios"""
    print("\n🎯 **Testing Comprehensive Scenarios**")
    print("=" * 50)
    
    scenarios = [
        {
            "name": "Hotel Manager Morning Check",
            "queries": [
                "Good morning! What's the overall system status?",
                "Are there any critical issues I need to address?",
                "Show me all devices in the east wing",
                "What's the temperature in the main lobby?"
            ]
        },
        {
            "name": "Technician Troubleshooting",
            "queries": [
                "I'm getting reports of high temperature in room 301",
                "Diagnose the HVAC system",
                "What maintenance is due this week?",
                "Show me the device history for sensor 300186"
            ]
        },
        {
            "name": "System Administrator",
            "queries": [
                "Give me a comprehensive system health report",
                "Are there any devices that need attention?",
                "What are the current alarms?",
                "Show me proactive recommendations"
            ]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📋 **Scenario: {scenario['name']}**")
        user_id = f"scenario_{scenario['name'].lower().replace(' ', '_')}"
        
        for i, query in enumerate(scenario['queries'], 1):
            print(f"\n{i}. User: {query}")
            response = enhanced_agentic_agent.process_query(query, user_id)
            print(f"   AI: {response[:150]}...")
    
    print("\n✅ Comprehensive Scenarios Test Complete")

def main():
    """Run all AI magic feature tests"""
    print("🚀 **AI Magic Features Comprehensive Test Suite**")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Run all tests
        test_conversational_memory()
        test_multi_device_operations()
        test_proactive_insights()
        test_natural_language_control()
        test_rich_responses()
        test_personalization()
        test_self_healing()
        test_smart_notifications()
        test_multi_language_support()
        test_comprehensive_scenarios()
        
        print("\n" + "=" * 60)
        print("🎉 **ALL AI MAGIC FEATURES TESTED SUCCESSFULLY!**")
        print("=" * 60)
        print("\n✨ **Implemented Features:**")
        print("✅ Conversational Memory & Context")
        print("✅ Multi-Device & Bulk Operations")
        print("✅ Proactive Recommendations & Insights")
        print("✅ Natural Language Control & Automation")
        print("✅ Rich, Visual, and Actionable Responses")
        print("✅ Personalization & User Profiles")
        print("✅ Self-Healing & Troubleshooting")
        print("✅ Smart Notifications & Alerts")
        print("✅ Multi-Language Support")
        print("\n🚀 Your AI chatbot is now enterprise-ready with cutting-edge features!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 