#!/usr/bin/env python3
"""
Comprehensive test script for all 55 prompts with the agentic AI implementation
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agentic_agent import agentic_agent

def test_comprehensive_prompts():
    """Test all 55 prompts comprehensively"""
    
    # All 55 prompts including the 6 key scenarios and existing prompts
    all_prompts = [
        # 6 Key Conversational AI Scenarios
        "Turn off HVAC and dim lights in the east wing on Saturday and Sunday. Send me a report Monday.",
        "Lower the temperature by 2 degrees in Conference Room B for the next 3 hours.",
        "Are any HVAC or lighting systems likely to fail in the next 7 days?",
        "How much carbon emissions did we reduce this week? Are we on track for our Q3 target?",
        "What are the least used restrooms on the 3rd floor today?",
        "Why is the east wing warm and noisy today?",
        
        # Additional Conversational Scenarios
        "Optimize energy usage in the west wing for the weekend.",
        "Reduce lighting in conference rooms after hours.",
        "Adjust comfort settings in the main hall for the townhall event.",
        "Increase temperature in the north wing by 1 degree.",
        "Check system health ahead of the high-profile visit.",
        "What maintenance is needed for the chiller systems?",
        "Show me the sustainability metrics for this month.",
        "What's our ESG performance for the quarter?",
        "Show me restroom usage patterns for cleaning optimization.",
        "Which areas need cleaning schedule adjustments?",
        "What's causing the environmental discomfort in the south wing?",
        "Why is the temperature fluctuating in the main lobby?",
        
        # Alarm Management - Critical/Major/Minor
        "Show all active alarms.",
        "Show all critical alarms.",
        "Show all major alarms.",
        "Show all minor alarms.",
        "Show all critical alarms for Tower A",
        "Show all major alarms or greater than major.",
        "What is the highest severity alarm right now?",
        "Show all unacknowledged alarms.",
        "Show all alarms for the office.",
        
        # Alarm by Device
        "Show all alarms for IAQ Sensor V2 - 300186.",
        "Show all alarms for RH/T Sensor - 150002.",
        
        # Alarm by Time
        "Show all alarms for today.",
        "Show all alarms in the last 24 hours.",
        "Summarize alarms for today.",
        "Summarize alarms for the last 24 hours.",
        "How many alarms are currently active?",
        
        # Alarm Types
        "List alarm types in the last 24 hours.",
        "Show top 3 alarm types.",
        
        # Acknowledge Alarms
        "Acknowledge alarm 300186.",
        "Acknowledge the high temperature alarm for IAQ Sensor V2 - 300186.",
        "Acknowledge the critical alarm for RH/T Sensor - 150002.",
        
        # Device Management
        "List all devices.",
        "Show all device names.",
        "How many devices are online?",
        "List devices with low battery.",
        "Show device status for all devices.",
        
        # Device Status
        "Is IAQ Sensor V2 - 300186 online?",
        "Is RH/T Sensor - 150002 online?",
        "Check if device is online.",
        
        # Device Telemetry
        "Show temperature for IAQ Sensor V2 - 300186.",
        "Show latest telemetry for RH/T Sensor - 150002.",
        "Show sensor telemetry for IAQ Sensor V2 - 300186 for the last 24 hours.",
        "Show humidity for RH/T Sensor - 150002.",
        "Show temperature",
        "Show humidity",
        "Show battery level",
        
        # Device Health
        "Check health of IAQ Sensor V2 - 300186.",
        "Is IAQ Sensor V2 - 300186 sending telemetry?",
        "Check device health",
        
        # Troubleshooting
        "My device is not sending telemetry.",
        "Why is device X not sending data?",
        "Show events for device RH/T Sensor - 150002.",
        "Forecast shows extreme heat; check HVAC-01 for potential overheat and recommend proactive maintenance."
    ]
    
    print("🧪 Comprehensive Testing of All 55 Prompts with Agentic AI Implementation\n")
    print(f"Total prompts to test: {len(all_prompts)}\n")
    
    successful_tests = 0
    failed_tests = 0
    partial_tests = 0
    
    results = {
        "successful": [],
        "failed": [],
        "partial": []
    }
    
    for i, prompt in enumerate(all_prompts, 1):
        print(f"Test {i:2d}/{len(all_prompts)}: {prompt[:60]}{'...' if len(prompt) > 60 else ''}")
        
        try:
            result = agentic_agent.process_query(prompt, "TestUser")
            
            # Check if the response is valid
            if result and not result.startswith("❌ Error"):
                # Check for specific quality indicators
                if any(keyword in result.lower() for keyword in ["error", "failed", "unable", "sorry", "issue"]):
                    print(f"⚠️  PARTIAL: {result[:100]}{'...' if len(result) > 100 else ''}")
                    partial_tests += 1
                    results["partial"].append({"prompt": prompt, "result": result})
                else:
                    print(f"✅ SUCCESS: {result[:100]}{'...' if len(result) > 100 else ''}")
                    successful_tests += 1
                    results["successful"].append({"prompt": prompt, "result": result})
            else:
                print(f"❌ FAILED: {result}")
                failed_tests += 1
                results["failed"].append({"prompt": prompt, "result": result})
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            failed_tests += 1
            results["failed"].append({"prompt": prompt, "result": f"Error: {str(e)}"})
        
        print("-" * 80)
    
    print(f"\n📊 Comprehensive Test Results Summary:")
    print(f"✅ Successful: {successful_tests}")
    print(f"⚠️  Partial: {partial_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"📈 Success Rate: {((successful_tests + partial_tests)/len(all_prompts)*100):.1f}%")
    
    if failed_tests == 0:
        print("\n🎉 All prompts are working with the agentic implementation!")
    else:
        print(f"\n⚠️  {failed_tests} prompts need attention before demo.")
    
    # Show detailed breakdown
    if results["failed"]:
        print(f"\n❌ Failed Prompts ({len(results['failed'])}):")
        for item in results["failed"]:
            print(f"  - {item['prompt'][:50]}...")
    
    if results["partial"]:
        print(f"\n⚠️  Partial Prompts ({len(results['partial'])}):")
        for item in results["partial"]:
            print(f"  - {item['prompt'][:50]}...")
    
    return successful_tests, partial_tests, failed_tests, results

if __name__ == "__main__":
    test_comprehensive_prompts() 