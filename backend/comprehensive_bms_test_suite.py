#!/usr/bin/env python3
"""
Comprehensive BMS Test Suite for IntelliSustain
Tests all 200-400 possible scenarios across the entire BMS scope
"""

import requests
import json
import time
import datetime
from typing import Dict, List, Any, Optional
import sys
import os

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_USER = "tech@intellisustain.com"
TEST_PASSWORD = "admin@123"

class ComprehensiveBMSTestSuite:
    def __init__(self):
        self.session = requests.Session()
        self.jwt_token = None
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "total": 0,
            "details": []
        }
        
    def login(self):
        """Login and get JWT token"""
        try:
            response = self.session.post(f"{BASE_URL}/login", json={
                "email": TEST_USER,
                "password": TEST_PASSWORD
            })
            if response.status_code == 200:
                self.jwt_token = response.json().get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.jwt_token}"})
                print("✅ Login successful")
                return True
            else:
                print(f"❌ Login failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False

    def test_scenario(self, category: str, scenario: str, query: str, expected_patterns: Optional[List[str]] = None, expected_errors: Optional[List[str]] = None):
        """Test a single scenario"""
        self.test_results["total"] += 1
        
        try:
            response = self.session.post(f"{BASE_URL}/chat/enhanced", json={
                "query": query,
                "user": TEST_USER,
                "device": None
            })
            
            if response.status_code == 200:
                result = response.json().get("response", "")
                
                # Check for expected patterns
                if expected_patterns:
                    pattern_found = any(pattern.lower() in result.lower() for pattern in expected_patterns)
                    if pattern_found:
                        self.test_results["passed"] += 1
                        print(f"✅ {category} - {scenario}")
                        return True
                    else:
                        self.test_results["failed"] += 1
                        print(f"❌ {category} - {scenario} (Pattern not found)")
                        return False
                
                # Check for expected errors
                elif expected_errors:
                    error_found = any(error.lower() in result.lower() for error in expected_errors)
                    if error_found:
                        self.test_results["passed"] += 1
                        print(f"✅ {category} - {scenario}")
                        return True
                    else:
                        self.test_results["failed"] += 1
                        print(f"❌ {category} - {scenario} (Expected error not found)")
                        return False
                
                # Default success check
                else:
                    if result and len(result) > 10:
                        self.test_results["passed"] += 1
                        print(f"✅ {category} - {scenario}")
                        return True
                    else:
                        self.test_results["failed"] += 1
                        print(f"❌ {category} - {scenario} (Empty response)")
                        return False
                        
            else:
                self.test_results["failed"] += 1
                print(f"❌ {category} - {scenario} (HTTP {response.status_code})")
                return False
                
        except Exception as e:
            self.test_results["failed"] += 1
            print(f"❌ {category} - {scenario} (Exception: {e})")
            return False

    def run_device_management_tests(self):
        """Test device management scenarios"""
        print("\n🔧 DEVICE MANAGEMENT TESTS")
        print("=" * 50)
        
        # Device listing and status
        self.test_scenario("Device Management", "List all devices", "Show all devices", ["devices", "online", "offline"])
        self.test_scenario("Device Management", "Count devices", "How many devices are online?", ["online", "devices"])
        self.test_scenario("Device Management", "Device status", "Show device status", ["status", "online", "offline"])
        self.test_scenario("Device Management", "Low battery devices", "List devices with low battery", ["battery", "low"])
        self.test_scenario("Device Management", "Device types", "Show all device types", ["type", "sensor", "thermostat"])
        
        # Device-specific queries
        self.test_scenario("Device Management", "Specific device info", "Show information for device 300186", ["300186", "device"])
        self.test_scenario("Device Management", "Device health", "Check health of device 300186", ["health", "300186"])
        self.test_scenario("Device Management", "Device attributes", "Show attributes for device 150002", ["attributes", "150002"])
        self.test_scenario("Device Management", "Device telemetry keys", "What telemetry does device 300186 support?", ["telemetry", "keys"])
        
        # Invalid device scenarios
        self.test_scenario("Device Management", "Invalid device ID", "Show temperature for device INVALID123", ["not found", "invalid"], ["not found", "invalid"])
        self.test_scenario("Device Management", "Non-existent device", "Check status of device 999999", ["not found", "999999"], ["not found", "999999"])

    def run_telemetry_tests(self):
        """Test telemetry data scenarios"""
        print("\n📊 TELEMETRY TESTS")
        print("=" * 50)
        
        # Temperature queries
        self.test_scenario("Telemetry", "Temperature query", "Show temperature for device 300186", ["temperature", "°C"])
        self.test_scenario("Telemetry", "Temperature with location", "What's the temperature in Conference Room B?", ["temperature", "conference"])
        self.test_scenario("Telemetry", "Temperature comparison", "Compare temperature between devices", ["temperature", "compare"])
        
        # Humidity queries
        self.test_scenario("Telemetry", "Humidity query", "Show humidity for device 150002", ["humidity", "%"])
        self.test_scenario("Telemetry", "Humidity with location", "What's the humidity in Room 101?", ["humidity", "room"])
        
        # Battery queries
        self.test_scenario("Telemetry", "Battery level", "Show battery level for device 300186", ["battery", "level"])
        self.test_scenario("Telemetry", "Low battery alert", "Which devices have low battery?", ["battery", "low"])
        
        # Occupancy queries
        self.test_scenario("Telemetry", "Occupancy data", "Show occupancy for device 300186", ["occupancy", "people"])
        self.test_scenario("Telemetry", "Occupancy by location", "How many people are in Tower A?", ["occupancy", "tower"])
        
        # Invalid telemetry scenarios
        self.test_scenario("Telemetry", "Invalid metric", "Show pressure for device 300186", ["does not report", "pressure"], ["does not report", "pressure"])
        self.test_scenario("Telemetry", "No telemetry data", "Show temperature for device 999999", ["not found", "telemetry"], ["not found", "telemetry"])

    def run_alarm_management_tests(self):
        """Test alarm management scenarios"""
        print("\n🚨 ALARM MANAGEMENT TESTS")
        print("=" * 50)
        
        # Alarm listing
        self.test_scenario("Alarms", "All alarms", "Show all alarms", ["alarms", "critical", "major"])
        self.test_scenario("Alarms", "Critical alarms", "Show critical alarms", ["critical", "alarms"])
        self.test_scenario("Alarms", "Major alarms", "Show major alarms", ["major", "alarms"])
        self.test_scenario("Alarms", "Minor alarms", "Show minor alarms", ["minor", "alarms"])
        
        # Alarm filtering
        self.test_scenario("Alarms", "Alarms by device", "Show alarms for device 300186", ["alarms", "300186"])
        self.test_scenario("Alarms", "Alarms by location", "Show alarms in Tower A", ["alarms", "tower"])
        self.test_scenario("Alarms", "Today's alarms", "Show alarms for today", ["alarms", "today"])
        self.test_scenario("Alarms", "Recent alarms", "Show recent alarms", ["alarms", "recent"])
        
        # Alarm acknowledgment
        self.test_scenario("Alarms", "Acknowledge alarm", "Acknowledge alarm for device 300186", ["acknowledge", "alarm"])
        self.test_scenario("Alarms", "Acknowledge specific alarm", "Acknowledge alarm ALM123", ["acknowledge", "ALM123"])
        
        # Alarm statistics
        self.test_scenario("Alarms", "Alarm count", "How many alarms are active?", ["alarms", "count"])
        self.test_scenario("Alarms", "Alarm summary", "Summarize all alarms", ["alarms", "summary"])
        self.test_scenario("Alarms", "Top alarm types", "Show top 3 alarm types", ["alarm", "types"])

    def run_hotel_operations_tests(self):
        """Test hotel-specific scenarios"""
        print("\n🏨 HOTEL OPERATIONS TESTS")
        print("=" * 50)
        
        # Room comfort control
        self.test_scenario("Hotel", "Room temperature", "Increase temperature by 2 degrees in room 101", ["room", "temperature", "101"])
        self.test_scenario("Hotel", "Room comfort", "Set comfort settings for room 205", ["room", "comfort", "205"])
        self.test_scenario("Hotel", "Room humidity", "Control humidity in room 312", ["room", "humidity", "312"])
        
        # Guest experience
        self.test_scenario("Hotel", "Guest optimization", "Optimize experience for guest 12345", ["guest", "optimization"])
        self.test_scenario("Hotel", "Guest comfort", "Personalize comfort for guest ABC123", ["guest", "comfort"])
        
        # Energy optimization
        self.test_scenario("Hotel", "Energy optimization", "Optimize energy usage in guest rooms", ["energy", "optimization", "rooms"])
        self.test_scenario("Hotel", "Low occupancy energy", "Optimize energy during low occupancy", ["energy", "occupancy"])
        
        # Maintenance scheduling
        self.test_scenario("Hotel", "Elevator maintenance", "Schedule preventive maintenance for elevator equipment", ["maintenance", "elevator"])
        self.test_scenario("Hotel", "HVAC maintenance", "Schedule HVAC maintenance for floor 3", ["maintenance", "hvac"])
        
        # Operational analytics
        self.test_scenario("Hotel", "Energy consumption", "Analyze energy consumption patterns for the last month", ["energy", "consumption", "patterns"])
        self.test_scenario("Hotel", "Occupancy analytics", "Show occupancy analytics for all floors", ["occupancy", "analytics"])

    def run_energy_optimization_tests(self):
        """Test energy optimization scenarios"""
        print("\n⚡ ENERGY OPTIMIZATION TESTS")
        print("=" * 50)
        
        # HVAC optimization
        self.test_scenario("Energy", "HVAC optimization", "Optimize HVAC in East Wing", ["hvac", "optimization", "east"])
        self.test_scenario("Energy", "Temperature optimization", "Lower temperature by 2 degrees in Conference Room B", ["temperature", "conference", "room"])
        self.test_scenario("Energy", "Fan speed control", "Set fan speed to medium in Server Room A", ["fan", "speed", "server"])
        
        # Lighting optimization
        self.test_scenario("Energy", "Lighting control", "Turn off HVAC and dim lights in the east wing", ["lighting", "dim", "east"])
        self.test_scenario("Energy", "Occupancy lighting", "Optimize lighting based on occupancy", ["lighting", "occupancy"])
        
        # Energy analysis
        self.test_scenario("Energy", "Energy consumption", "Show energy consumption for this week", ["energy", "consumption", "week"])
        self.test_scenario("Energy", "Peak demand", "Analyze peak energy demand", ["peak", "demand", "energy"])
        self.test_scenario("Energy", "Energy savings", "Calculate energy savings from optimization", ["energy", "savings"])

    def run_predictive_maintenance_tests(self):
        """Test predictive maintenance scenarios"""
        print("\n🔧 PREDICTIVE MAINTENANCE TESTS")
        print("=" * 50)
        
        # System health checks
        self.test_scenario("Maintenance", "HVAC health", "Are any HVAC systems likely to fail?", ["hvac", "fail", "maintenance"])
        self.test_scenario("Maintenance", "Lighting health", "Check health of lighting systems", ["lighting", "health", "systems"])
        self.test_scenario("Maintenance", "Chiller health", "Predictive maintenance for chiller systems", ["chiller", "maintenance"])
        self.test_scenario("Maintenance", "Overall health", "Overall system health check", ["system", "health", "check"])
        
        # Maintenance scheduling
        self.test_scenario("Maintenance", "Maintenance schedule", "Schedule maintenance for next week", ["maintenance", "schedule", "week"])
        self.test_scenario("Maintenance", "Preventive maintenance", "Schedule preventive maintenance", ["preventive", "maintenance"])
        
        # Failure prediction
        self.test_scenario("Maintenance", "Failure prediction", "Which systems are likely to fail in the next 7 days?", ["fail", "systems", "days"])
        self.test_scenario("Maintenance", "Equipment health", "Check equipment health status", ["equipment", "health", "status"])

    def run_esg_sustainability_tests(self):
        """Test ESG and sustainability scenarios"""
        print("\n🌱 ESG & SUSTAINABILITY TESTS")
        print("=" * 50)
        
        # Carbon emissions
        self.test_scenario("ESG", "Carbon emissions", "How much carbon emissions did we reduce this week?", ["carbon", "emissions", "reduce"])
        self.test_scenario("ESG", "ESG analysis", "ESG analysis for this week", ["esg", "analysis", "week"])
        self.test_scenario("ESG", "Carbon target", "Are we on track for our Q3 carbon target?", ["carbon", "target", "q3"])
        
        # Sustainability reporting
        self.test_scenario("ESG", "Sustainability report", "Generate sustainability report for this month", ["sustainability", "report", "month"])
        self.test_scenario("ESG", "ESG performance", "Show ESG performance metrics", ["esg", "performance", "metrics"])
        
        # Energy efficiency
        self.test_scenario("ESG", "Energy efficiency", "Calculate energy efficiency improvements", ["energy", "efficiency", "improvements"])
        self.test_scenario("ESG", "Green building", "Show green building compliance status", ["green", "building", "compliance"])

    def run_security_monitoring_tests(self):
        """Test security monitoring scenarios"""
        print("\n🔒 SECURITY MONITORING TESTS")
        print("=" * 50)
        
        # Access control
        self.test_scenario("Security", "Access control", "Show access control status", ["access", "control", "status"])
        self.test_scenario("Security", "Security monitoring", "Security monitoring analysis", ["security", "monitoring", "analysis"])
        self.test_scenario("Security", "Access logs", "Show recent access logs", ["access", "logs", "recent"])
        
        # Security alerts
        self.test_scenario("Security", "Security alerts", "Show security alerts", ["security", "alerts"])
        self.test_scenario("Security", "Unauthorized access", "Check for unauthorized access attempts", ["unauthorized", "access", "attempts"])

    def run_cleaning_optimization_tests(self):
        """Test cleaning optimization scenarios"""
        print("\n🧹 CLEANING OPTIMIZATION TESTS")
        print("=" * 50)
        
        # Restroom usage
        self.test_scenario("Cleaning", "Restroom usage", "What are the least used restrooms on the 3rd floor today?", ["restrooms", "least", "used"])
        self.test_scenario("Cleaning", "Cleaning schedule", "Optimize cleaning schedule based on usage", ["cleaning", "schedule", "usage"])
        self.test_scenario("Cleaning", "High traffic areas", "Identify high traffic areas for cleaning", ["high", "traffic", "cleaning"])

    def run_root_cause_analysis_tests(self):
        """Test root cause analysis scenarios"""
        print("\n🔍 ROOT CAUSE ANALYSIS TESTS")
        print("=" * 50)
        
        # Problem diagnosis
        self.test_scenario("Analysis", "Warm and noisy", "Why is the east wing warm and noisy today?", ["east", "wing", "warm", "noisy"])
        self.test_scenario("Analysis", "Temperature issues", "Root cause analysis for temperature problems", ["root", "cause", "temperature"])
        self.test_scenario("Analysis", "System issues", "Analyze system performance issues", ["system", "performance", "issues"])

    def run_weather_risk_tests(self):
        """Test weather and risk analysis scenarios"""
        print("\n🌤️ WEATHER & RISK ANALYSIS TESTS")
        print("=" * 50)
        
        # Weather forecasts
        self.test_scenario("Weather", "Mumbai weather", "What is the weather prediction in Mumbai for tomorrow?", ["mumbai", "weather", "tomorrow"])
        self.test_scenario("Weather", "Delhi forecast", "Show me weather forecast for Delhi this week", ["delhi", "weather", "week"])
        
        # Risk analysis
        self.test_scenario("Weather", "HVAC rain risk", "What HVAC risks if it rains in Mumbai this week?", ["hvac", "risks", "rain", "mumbai"])
        self.test_scenario("Weather", "Lighting temperature risk", "What are the lighting risks if temperature drops in Bangalore?", ["lighting", "risks", "temperature", "bangalore"])

    def run_advanced_analytics_tests(self):
        """Test advanced analytics scenarios"""
        print("\n📈 ADVANCED ANALYTICS TESTS")
        print("=" * 50)
        
        # Trend analysis
        self.test_scenario("Analytics", "Temperature trends", "Show temperature trends for the last month", ["temperature", "trends", "month"])
        self.test_scenario("Analytics", "Energy trends", "Analyze energy consumption trends", ["energy", "trends", "consumption"])
        
        # Performance benchmarking
        self.test_scenario("Analytics", "Performance benchmark", "Performance benchmarking report", ["performance", "benchmark", "report"])
        self.test_scenario("Analytics", "Operational analytics", "Operational analytics dashboard", ["operational", "analytics", "dashboard"])
        
        # Smart notifications
        self.test_scenario("Analytics", "Smart notifications", "Show smart notifications", ["smart", "notifications"])
        self.test_scenario("Analytics", "Proactive insights", "Generate proactive insights", ["proactive", "insights"])

    def run_error_handling_tests(self):
        """Test error handling and edge cases"""
        print("\n⚠️ ERROR HANDLING TESTS")
        print("=" * 50)
        
        # Invalid inputs
        self.test_scenario("Error Handling", "Empty query", "", ["error", "empty"], ["error", "empty"])
        self.test_scenario("Error Handling", "Invalid location", "Show temperature in InvalidLocation123", ["not found", "location"], ["not found", "location"])
        self.test_scenario("Error Handling", "Invalid device", "Check status of device INVALID", ["not found", "device"], ["not found", "device"])
        self.test_scenario("Error Handling", "Invalid metric", "Show pressure for device 300186", ["does not report", "pressure"], ["does not report", "pressure"])
        
        # Ambiguous queries
        self.test_scenario("Error Handling", "Ambiguous location", "Show temperature in north wing", ["ambiguous", "location"], ["ambiguous", "location"])
        self.test_scenario("Error Handling", "Missing device", "Show temperature", ["specify", "device"], ["specify", "device"])

    def run_multi_language_tests(self):
        """Test multi-language support"""
        print("\n🌐 MULTI-LANGUAGE TESTS")
        print("=" * 50)
        
        # Hindi queries
        self.test_scenario("Multi-Language", "Hindi temperature", "कमरा 201 में तापमान क्या है?", ["temperature", "room"])
        self.test_scenario("Multi-Language", "Hindi humidity", "कमरा 201 में humidity क्या है?", ["humidity", "room"])
        
        # Hinglish queries
        self.test_scenario("Multi-Language", "Hinglish temperature", "कमरा 201 में temperature क्या है?", ["temperature", "room"])
        self.test_scenario("Multi-Language", "Hinglish device", "Device 300186 का status क्या है?", ["status", "device"])

    def run_complex_scenario_tests(self):
        """Test complex multi-step scenarios"""
        print("\n🔄 COMPLEX SCENARIO TESTS")
        print("=" * 50)
        
        # Multi-device queries
        self.test_scenario("Complex", "Multi-device temperature", "Show temperature for all devices in Tower A", ["temperature", "tower", "devices"])
        self.test_scenario("Complex", "Multi-metric analysis", "Compare temperature and humidity across all floors", ["temperature", "humidity", "floors"])
        
        # Time-based queries
        self.test_scenario("Complex", "Time-based energy", "Show energy consumption for the last 24 hours", ["energy", "consumption", "hours"])
        self.test_scenario("Complex", "Historical trends", "Show temperature trends for the past week", ["temperature", "trends", "week"])
        
        # Conditional scenarios
        self.test_scenario("Complex", "Conditional optimization", "If occupancy is low, optimize energy usage", ["occupancy", "energy", "optimization"])
        self.test_scenario("Complex", "Weather-based control", "Adjust HVAC based on weather forecast", ["hvac", "weather", "forecast"])

    def run_all_tests(self):
        """Run all test categories"""
        print("🚀 STARTING COMPREHENSIVE BMS TEST SUITE")
        print("=" * 60)
        
        if not self.login():
            print("❌ Cannot proceed without login")
            return
        
        # Run all test categories
        self.run_device_management_tests()
        self.run_telemetry_tests()
        self.run_alarm_management_tests()
        self.run_hotel_operations_tests()
        self.run_energy_optimization_tests()
        self.run_predictive_maintenance_tests()
        self.run_esg_sustainability_tests()
        self.run_security_monitoring_tests()
        self.run_cleaning_optimization_tests()
        self.run_root_cause_analysis_tests()
        self.run_weather_risk_tests()
        self.run_advanced_analytics_tests()
        self.run_error_handling_tests()
        self.run_multi_language_tests()
        self.run_complex_scenario_tests()
        
        # Print final results
        self.print_results()

    def print_results(self):
        """Print comprehensive test results"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE BMS TEST RESULTS")
        print("=" * 60)
        
        total = self.test_results["total"]
        passed = self.test_results["passed"]
        failed = self.test_results["failed"]
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📊 Total: {total}")
        print(f"🎯 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT! System is ready for live demo!")
        elif success_rate >= 80:
            print("👍 GOOD! Minor issues to address before demo")
        elif success_rate >= 70:
            print("⚠️ FAIR! Several issues need attention")
        else:
            print("🚨 POOR! Major issues need immediate attention")
        
        print("\n📋 Test Categories Covered:")
        categories = [
            "Device Management", "Telemetry", "Alarm Management", 
            "Hotel Operations", "Energy Optimization", "Predictive Maintenance",
            "ESG & Sustainability", "Security Monitoring", "Cleaning Optimization",
            "Root Cause Analysis", "Weather & Risk Analysis", "Advanced Analytics",
            "Error Handling", "Multi-Language Support", "Complex Scenarios"
        ]
        
        for category in categories:
            print(f"  • {category}")
        
        print(f"\n⏱️ Total Test Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)

if __name__ == "__main__":
    test_suite = ComprehensiveBMSTestSuite()
    test_suite.run_all_tests() 