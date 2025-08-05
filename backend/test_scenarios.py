#!/usr/bin/env python3
"""
Test script for the new conversational AI scenarios
"""

from tools import (
    energy_optimization_node,
    comfort_adjustment_node,
    predictive_maintenance_node,
    esg_reporting_node,
    cleaning_optimization_node,
    root_cause_identification_node
)

def test_scenarios():
    """Test all the new conversational AI scenarios"""
    
    print("🧪 Testing Conversational AI Scenarios\n")
    
    # Test Scenario 1: Energy Optimization
    print("1️⃣ Testing Energy Optimization:")
    test_input = "Turn off HVAC and dim lights in the east wing on Saturday and Sunday. Send me a report Monday."
    result = energy_optimization_node({'input': test_input})
    print(f"Input: {test_input}")
    print(f"Output: {result}\n")
    
    # Test Scenario 2: Comfort Adjustment
    print("2️⃣ Testing Comfort Adjustment:")
    test_input = "Lower the temperature by 2 degrees in Conference Room B for the next 3 hours."
    result = comfort_adjustment_node({'input': test_input})
    print(f"Input: {test_input}")
    print(f"Output: {result}\n")
    
    # Test Scenario 3: Predictive Maintenance
    print("3️⃣ Testing Predictive Maintenance:")
    test_input = "Are any HVAC or lighting systems likely to fail in the next 7 days?"
    result = predictive_maintenance_node({'input': test_input})
    print(f"Input: {test_input}")
    print(f"Output: {result}\n")
    
    # Test Scenario 4: ESG Reporting
    print("4️⃣ Testing ESG Reporting:")
    test_input = "How much carbon emissions did we reduce this week? Are we on track for our Q3 target?"
    result = esg_reporting_node({'input': test_input})
    print(f"Input: {test_input}")
    print(f"Output: {result}\n")
    
    # Test Scenario 5: Cleaning Optimization
    print("5️⃣ Testing Cleaning Optimization:")
    test_input = "What are the least used restrooms on the 3rd floor today?"
    result = cleaning_optimization_node({'input': test_input})
    print(f"Input: {test_input}")
    print(f"Output: {result}\n")
    
    # Test Scenario 6: Root Cause Identification
    print("6️⃣ Testing Root Cause Identification:")
    test_input = "Why is the east wing warm and noisy today?"
    result = root_cause_identification_node({'input': test_input})
    print(f"Input: {test_input}")
    print(f"Output: {result}\n")
    
    print("✅ All scenarios tested successfully!")

if __name__ == "__main__":
    test_scenarios() 