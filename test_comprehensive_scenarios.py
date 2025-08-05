#!/usr/bin/env python3
"""
Comprehensive Test Suite for Enhanced BMS AI Agent
Tests all alarm functionality, fault reasoning, and system monitoring capabilities
"""

import sys
import os
import json
import time
from datetime import datetime

# Add backend to path and import
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Import the agent class
from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

# Initialize the agent instance
enhanced_agentic_agent = EnhancedAgenticInferrixAgent()

def run_test(test_name, query, expected_keywords=None, expected_contains=None):
    """Run a single test and validate results"""
    print(f"\n{'='*60}")
    print(f"🧪 TEST: {test_name}")
    print(f"📝 QUERY: {query}")
    print(f"{'='*60}")
    
    try:
        start_time = time.time()
        response = enhanced_agentic_agent.process_query(query)
        end_time = time.time()
        
        print(f"⏱️  Response Time: {end_time - start_time:.2f} seconds")
        print(f"📄 RESPONSE:")
        print(response)
        
        # Validation
        success = True
        if expected_keywords:
            missing_keywords = []
            for keyword in expected_keywords:
                if keyword.lower() not in response.lower():
                    missing_keywords.append(keyword)
            if missing_keywords:
                print(f"❌ MISSING KEYWORDS: {missing_keywords}")
                success = False
            else:
                print(f"✅ ALL KEYWORDS FOUND: {expected_keywords}")
        
        if expected_contains:
            if expected_contains.lower() not in response.lower():
                print(f"❌ MISSING CONTENT: {expected_contains}")
                success = False
            else:
                print(f"✅ CONTENT FOUND: {expected_contains}")
        
        if success:
            print("🎉 TEST PASSED!")
        else:
            print("💥 TEST FAILED!")
        
        return success
        
    except Exception as e:
        print(f"💥 TEST ERROR: {str(e)}")
        return False

def test_alarm_functionality():
    """Test comprehensive alarm functionality"""
    print("\n" + "🚨" * 20 + " ALARM FUNCTIONALITY TESTS " + "🚨" * 20)
    
    tests = [
        # Basic Alarm Queries
        {
            "name": "Show Active Alarms",
            "query": "show me active alarms",
            "expected_keywords": ["alarms", "active", "found"]
        },
        {
            "name": "Show Critical Alarms",
            "query": "show me critical alarms",
            "expected_keywords": ["critical", "alarms"]
        },
        
        # Historical Alarm Queries
        {
            "name": "Historical Alarms - Last Week",
            "query": "show me history of alarms from last 1 week",
            "expected_keywords": ["historical", "alarms", "week"]
        },
        {
            "name": "Historical Alarms - Last Month",
            "query": "show me alarms from last 1 month",
            "expected_keywords": ["historical", "alarms", "month"]
        },
        {
            "name": "Data Disconnection History",
            "query": "show me history of data disconnections",
            "expected_keywords": ["historical", "data disconnections", "communication"]
        },
        {
            "name": "Connection Failures",
            "query": "show me connection failures",
            "expected_keywords": ["connection", "failures", "communication"]
        },
        
        # Air Quality Alarms
        {
            "name": "Air Quality Alarms",
            "query": "show me alarms related to air quality",
            "expected_keywords": ["air quality", "aqi", "alarms"]
        },
        {
            "name": "Bad Air Quality Areas",
            "query": "show me areas with bad air quality",
            "expected_keywords": ["air quality", "bad", "areas"]
        },
        {
            "name": "What is Air Quality",
            "query": "what is air quality",
            "expected_keywords": ["air quality", "aqi", "pm"]
        },
        
        # CO2 Alarms - Case Insensitive Testing
        {
            "name": "CO2 Alarms - Uppercase",
            "query": "show me CO2 alarms",
            "expected_keywords": ["co2", "alarms", "carbon dioxide"]
        },
        {
            "name": "CO2 Alarms - Lowercase",
            "query": "show me co2 alarms",
            "expected_keywords": ["co2", "alarms", "carbon dioxide"]
        },
        {
            "name": "CO2 Alarms - Mixed Case",
            "query": "show me Co2 alarms",
            "expected_keywords": ["co2", "alarms", "carbon dioxide"]
        },
        {
            "name": "CO2 High Alarms",
            "query": "show me CO2 high alarms",
            "expected_keywords": ["co2", "high", "poor ventilation", "over-occupancy"]
        },
        {
            "name": "Areas with High CO2",
            "query": "show me areas with high CO2 levels",
            "expected_keywords": ["co2", "high", "poor ventilation", "over-occupancy"]
        },
        {
            "name": "Carbon Dioxide Alarms",
            "query": "show me carbon dioxide alarms",
            "expected_keywords": ["carbon dioxide", "co2", "alarms"]
        },
        
        # Battery Alarms
        {
            "name": "Battery Status All Devices",
            "query": "show me battery status of all devices",
            "expected_keywords": ["battery", "devices", "status"]
        },
        {
            "name": "Low Battery Devices",
            "query": "show me any devices with low battery",
            "expected_keywords": ["battery", "low", "devices"]
        },
        {
            "name": "Battery Alarms",
            "query": "show me alarms with low battery",
            "expected_keywords": ["battery", "alarms", "low"]
        },
        
        # System Communication
        {
            "name": "System Communication Alarms",
            "query": "show me alarms related to system communication",
            "expected_keywords": ["communication", "system", "alarms"]
        },
        {
            "name": "System Connection Status",
            "query": "give me the system connection status",
            "expected_keywords": ["connection", "status", "system"]
        },
        {
            "name": "Connection Health",
            "query": "show health of the connections",
            "expected_keywords": ["health", "connections", "system"]
        },
        
        # Pump Status
        {
            "name": "Pump Status",
            "query": "show me status of pumps",
            "expected_keywords": ["pump", "status", "pumps"]
        },
        
        # Filter Alarms
        {
            "name": "Filter Choke Alarms",
            "query": "show me filter choke alarms",
            "expected_keywords": ["filter", "choke", "alarms"]
        },
        
        # Chiller/HVAC Alarms
        {
            "name": "Chiller Alarms",
            "query": "show me alarms related to chiller or hvac",
            "expected_keywords": ["chiller", "hvac", "alarms"]
        },
        {
            "name": "Chilled Water Temperature",
            "query": "show me high chilled water supply temperature alarms",
            "expected_keywords": ["chilled water", "temperature", "cooling performance"]
        },
        {
            "name": "Low Chilled Water Temperature",
            "query": "show me low chilled water supply temperature alarms",
            "expected_keywords": ["chilled water", "temperature", "freezing"]
        },
        
        # Advanced Equipment Alarms
        {
            "name": "Compressor Faults",
            "query": "show me compressor faults",
            "expected_keywords": ["compressor", "faults", "discharge temperature"]
        },
        {
            "name": "Refrigerant Circuit Alarms",
            "query": "show me refrigerant circuit alarms",
            "expected_keywords": ["refrigerant", "circuit", "pressure"]
        },
        {
            "name": "Temperature Sensor Faults",
            "query": "show me temperature sensor faults",
            "expected_keywords": ["temperature", "sensor", "faults"]
        },
        {
            "name": "Safety Interlock Alarms",
            "query": "show me safety interlock alarms",
            "expected_keywords": ["safety", "interlock", "emergency"]
        },
        {
            "name": "Fire Alarm Interlock",
            "query": "show me fire alarm interlock alarms",
            "expected_keywords": ["fire", "alarm", "interlock"]
        },
        {
            "name": "Emergency Stop Alarms",
            "query": "show me emergency stop alarms",
            "expected_keywords": ["emergency", "stop", "safety"]
        },
        
        # Vibration and Advanced Monitoring
        {
            "name": "Vibration Alarms",
            "query": "show me vibration alarms",
            "expected_keywords": ["vibration", "mechanical", "wear"]
        },
        {
            "name": "Oil Pressure Alarms",
            "query": "show me oil pressure alarms",
            "expected_keywords": ["oil", "pressure", "lubrication"]
        },
        {
            "name": "Expansion Valve Alarms",
            "query": "show me expansion valve alarms",
            "expected_keywords": ["expansion", "valve", "eev", "txv"]
        },
        
        # Environmental Alarms
        {
            "name": "Supply Air Temperature",
            "query": "show me supply air temperature alarms",
            "expected_keywords": ["supply air", "temperature", "coil control"]
        },
        {
            "name": "Return Air Temperature",
            "query": "show me return air temperature alarms",
            "expected_keywords": ["return air", "temperature", "ductwork"]
        },
        {
            "name": "Humidity Alarms",
            "query": "show me humidity alarms",
            "expected_keywords": ["humidity", "rh", "mold", "comfort"]
        },
        {
            "name": "Airflow Failure",
            "query": "show me airflow failure alarms",
            "expected_keywords": ["airflow", "failure", "fan", "belt"]
        },
        
        # PM Alarms
        {
            "name": "PM10 Alarms",
            "query": "show me PM10 alarms",
            "expected_keywords": ["pm10", "particulate", "breathing"]
        },
        {
            "name": "PM2.5 Alarms",
            "query": "show me PM2.5 alarms",
            "expected_keywords": ["pm2.5", "particulate", "breathing"]
        },
        
        # Communication and Power
        {
            "name": "Phase Loss Alarms",
            "query": "show me phase loss alarms",
            "expected_keywords": ["phase", "loss", "power", "electrical"]
        },
        {
            "name": "Power Failure Alarms",
            "query": "show me power failure alarms",
            "expected_keywords": ["power", "failure", "electrical"]
        },
        {
            "name": "BMS Communication Failure",
            "query": "show me BMS communication failure alarms",
            "expected_keywords": ["bms", "communication", "network"]
        },
        
        # Advanced Chiller Alarms
        {
            "name": "Condenser Pressure Alarms",
            "query": "show me condenser pressure alarms",
            "expected_keywords": ["condenser", "pressure", "heat rejection"]
        },
        {
            "name": "Evaporator Pressure Alarms",
            "query": "show me evaporator pressure alarms",
            "expected_keywords": ["evaporator", "pressure", "refrigerant"]
        },
        {
            "name": "Freeze Protection Alarms",
            "query": "show me freeze protection alarms",
            "expected_keywords": ["freeze", "protection", "ice formation"]
        },
        {
            "name": "Flow Switch Trip Alarms",
            "query": "show me flow switch trip alarms",
            "expected_keywords": ["flow", "switch", "trip", "evaporator"]
        },
        
        # Operational Alarms
        {
            "name": "Unscheduled Operation",
            "query": "show me unscheduled operation alarms",
            "expected_keywords": ["unscheduled", "operation", "schedule"]
        },
        {
            "name": "Access Panel Open",
            "query": "show me access panel open alarms",
            "expected_keywords": ["access", "panel", "security", "unauthorized"]
        },
        {
            "name": "Differential Pressure Sensor Faults",
            "query": "show me differential pressure sensor faults",
            "expected_keywords": ["differential", "pressure", "sensor", "dp"]
        },
        {
            "name": "Low Water Flow Alarms",
            "query": "show me low water flow alarms",
            "expected_keywords": ["water", "flow", "valve", "pump"]
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if run_test(test["name"], test["query"], test.get("expected_keywords")):
            passed += 1
        else:
            failed += 1
    
    return passed, failed

def test_fault_reasoning():
    """Test detailed fault reasoning functionality"""
    print("\n" + "🔍" * 20 + " FAULT REASONING TESTS " + "🔍" * 20)
    
    # Test specific alarm types to verify reasoning
    tests = [
        {
            "name": "CO2 High Alarm Reasoning",
            "query": "what causes CO2 high alarm",
            "expected_contains": "poor ventilation or over-occupancy"
        },
        {
            "name": "Filter Choke Alarm Reasoning",
            "query": "what causes filter choke alarm",
            "expected_contains": "high differential pressure across filter"
        },
        {
            "name": "Fan Failure Reasoning",
            "query": "what causes fan failure alarm",
            "expected_contains": "supply fan not running"
        },
        {
            "name": "Battery Alarm Reasoning",
            "query": "what causes battery alarm",
            "expected_contains": "battery levels dropping"
        },
        {
            "name": "Communication Failure Reasoning",
            "query": "what causes BMS communication failure",
            "expected_contains": "network issue"
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if run_test(test["name"], test["query"], expected_contains=test["expected_contains"]):
            passed += 1
        else:
            failed += 1
    
    return passed, failed

def test_comprehensive_scenarios():
    """Test complex real-world scenarios"""
    print("\n" + "🌍" * 20 + " COMPREHENSIVE SCENARIOS " + "🌍" * 20)
    
    tests = [
        {
            "name": "Hotel Banquet Hall CO2 Issue",
            "query": "banquet hall has high CO2 level due to poor ventilation or over-occupancy",
            "expected_keywords": ["co2", "banquet", "ventilation", "occupancy"]
        },
        {
            "name": "Office Building Air Quality",
            "query": "show me air quality alarms in office building",
            "expected_keywords": ["air quality", "office", "alarms"]
        },
        {
            "name": "Mall HVAC System Issues",
            "query": "mall has chiller issues and pump problems",
            "expected_keywords": ["chiller", "pump", "mall"]
        },
        {
            "name": "Data Center Communication",
            "query": "data center has communication failures and battery issues",
            "expected_keywords": ["communication", "battery", "data center"]
        },
        {
            "name": "Hospital Air Quality Monitoring",
            "query": "hospital needs air quality monitoring for PM2.5 and CO2",
            "expected_keywords": ["hospital", "pm2.5", "co2", "air quality"]
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if run_test(test["name"], test["query"], test.get("expected_keywords")):
            passed += 1
        else:
            failed += 1
    
    return passed, failed

def main():
    """Run comprehensive test suite"""
    print("🚀 COMPREHENSIVE BMS AI AGENT TEST SUITE")
    print("=" * 60)
    print(f"📅 Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    total_passed = 0
    total_failed = 0
    
    # Test 1: Alarm Functionality
    passed, failed = test_alarm_functionality()
    total_passed += passed
    total_failed += failed
    
    # Test 2: Fault Reasoning
    passed, failed = test_fault_reasoning()
    total_passed += passed
    total_failed += failed
    
    # Test 3: Comprehensive Scenarios
    passed, failed = test_comprehensive_scenarios()
    total_passed += passed
    total_failed += failed
    
    # Final Results
    print("\n" + "🏁" * 20 + " FINAL TEST RESULTS " + "🏁" * 20)
    print(f"✅ PASSED: {total_passed}")
    print(f"❌ FAILED: {total_failed}")
    print(f"📊 TOTAL: {total_passed + total_failed}")
    
    if total_failed == 0:
        print("🎉 ALL TESTS PASSED! BMS AI Agent is working perfectly!")
    else:
        print(f"⚠️  {total_failed} tests failed. Please review the results above.")
    
    print(f"📅 Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    main() 