#!/usr/bin/env python3
"""
Test script for the new agentic AI implementation
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agentic_agent import agentic_agent

def test_agentic_scenarios():
    """Test all the 6 key scenarios with the agentic implementation"""
    
    print("🧪 Testing Agentic AI Implementation\n")
    
    # Test Scenario 3: Predictive Maintenance
    print("3️⃣ Testing Predictive Maintenance:")
    test_input = "Are any HVAC or lighting systems likely to fail in the next 7 days?"
    result = agentic_agent.process_query(test_input, "TestUser")
    print(f"Input: {test_input}")
    print(f"Output: {result}\n")
    
    # Test Scenario 4: ESG Reporting
    print("4️⃣ Testing ESG Reporting:")
    test_input = "How much carbon emissions did we reduce this week? Are we on track for our Q3 target?"
    result = agentic_agent.process_query(test_input, "TestUser")
    print(f"Input: {test_input}")
    print(f"Output: {result}\n")
    
    # Test Scenario 5: Cleaning Optimization
    print("5️⃣ Testing Cleaning Optimization:")
    test_input = "What are the least used restrooms on the 3rd floor today?"
    result = agentic_agent.process_query(test_input, "TestUser")
    print(f"Input: {test_input}")
    print(f"Output: {result}\n")
    
    # Test Scenario 6: Root Cause Analysis
    print("6️⃣ Testing Root Cause Analysis:")
    test_input = "Why is the east wing warm and noisy today?"
    result = agentic_agent.process_query(test_input, "TestUser")
    print(f"Input: {test_input}")
    print(f"Output: {result}\n")
    
    # Test Scenario 1: Energy Optimization
    print("1️⃣ Testing Energy Optimization:")
    test_input = "Turn off HVAC and dim lights in the east wing on Saturday and Sunday. Send me a report Monday."
    result = agentic_agent.process_query(test_input, "TestUser")
    print(f"Input: {test_input}")
    print(f"Output: {result}\n")
    
    # Test Scenario 2: Comfort Adjustment
    print("2️⃣ Testing Comfort Adjustment:")
    test_input = "Lower the temperature by 2 degrees in Conference Room B for the next 3 hours."
    result = agentic_agent.process_query(test_input, "TestUser")
    print(f"Input: {test_input}")
    print(f"Output: {result}\n")
    
    print("✅ All agentic scenarios tested successfully!")

if __name__ == "__main__":
    test_agentic_scenarios() 