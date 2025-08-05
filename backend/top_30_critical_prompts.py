#!/usr/bin/env python3
"""
Top 30 Critical Prompts Test - Most Important for Network Support/SME
These are the prompts that will be used most frequently in production
"""

import os
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agentic_agent import agentic_agent

def test_top_30_critical_prompts():
    """Test the top 30 most critical prompts for network support/SME"""
    
    print("\nFetching real device IDs for testing:")
    agentic_agent.print_real_device_ids()
    
    # TOP 30 CRITICAL PROMPTS - Most used by network support/SME
    critical_prompts = [
        # 1-5: Device Management (Most Critical)
        "List all devices",
        "Show all device names", 
        "How many devices are online?",
        "Show device status for all devices",
        "List devices with low battery",
        
        # 6-10: Alarm Management (Critical for Support)
        "Show all active alarms",
        "Show all critical alarms", 
        "Show all major alarms",
        "Show all minor alarms",
        "How many alarms are currently active?",
        
        # 11-15: Device Telemetry (Essential for Troubleshooting)
        "Show temperature for IAQ Sensor V2 - 300186",
        "Show latest telemetry for RH/T Sensor - 150002",
        "Show humidity for RH/T Sensor - 150002",
        "Show battery level for device 300186",
        "Show occupancy data for device 150002",
        
        # 16-20: Device Health & Status (Support Essentials)
        "Check health of IAQ Sensor V2 - 300186",
        "Is IAQ Sensor V2 - 300186 sending telemetry?",
        "Check device status for all devices",
        "Show device health for RH/T Sensor - 150002",
        "Check if device 150002 is online",
        
        # 21-25: Alarm Actions (Support Operations)
        "Acknowledge alarm 300186",
        "Acknowledge the high temperature alarm for IAQ Sensor V2 - 300186",
        "Acknowledge the critical alarm for RH/T Sensor - 150002",
        "Show all unacknowledged alarms",
        "Show all alarms for today",
        
        # 26-30: System Overview (Management & Reporting)
        "List all assets in the system",
        "Show all entity views", 
        "Show my notifications",
        "What is the overall system status?",
        "Are all systems functioning properly?"
    ]
    
    print("🎯 TESTING TOP 30 CRITICAL PROMPTS FOR NETWORK SUPPORT/SME")
    print("=" * 80)
    print(f"Total prompts to test: {len(critical_prompts)}")
    print("These are the most important prompts for production use\n")
    
    successful = 0
    failed = 0
    results = []
    
    for i, prompt in enumerate(critical_prompts, 1):
        print(f"\n[{i:2d}/30] Testing: {prompt}")
        print("-" * 60)
        
        try:
            start_time = time.time()
            result = agentic_agent.process_query(prompt, "NetworkSupport")
            end_time = time.time()
            
            # Check if response is meaningful (not generic clarification)
            is_meaningful = (
                result and 
                not result.startswith("🤔 I'd be happy to help") and
                not result.startswith("❌ Error") and
                not result.startswith("❌ **Error") and
                len(result) > 20  # Not too short
            )
            
            if is_meaningful:
                print(f"✅ SUCCESS ({end_time-start_time:.2f}s)")
                print(f"Response: {result[:150]}{'...' if len(result) > 150 else ''}")
                successful += 1
                status = "✅ SUCCESS"
            else:
                print(f"❌ FAILED ({end_time-start_time:.2f}s)")
                print(f"Response: {result[:200]}{'...' if len(result) > 200 else ''}")
                failed += 1
                status = "❌ FAILED"
            
            results.append({
                "number": i,
                "prompt": prompt,
                "status": status,
                "response": result[:100] + "..." if len(result) > 100 else result,
                "time": end_time - start_time
            })
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            failed += 1
            results.append({
                "number": i,
                "prompt": prompt,
                "status": "❌ ERROR",
                "response": f"Exception: {str(e)}",
                "time": 0
            })
        
        # Small delay to avoid overwhelming the API
        time.sleep(1.0)
    
    # Print comprehensive results
    print(f"\n{'='*80}")
    print(f"📊 TOP 30 CRITICAL PROMPTS - FINAL RESULTS")
    print(f"{'='*80}")
    print(f"✅ Successful: {successful}/30 ({successful/30*100:.1f}%)")
    print(f"❌ Failed: {failed}/30 ({failed/30*100:.1f}%)")
    
    if successful >= 25:
        print(f"\n🎉 EXCELLENT! {successful}/30 prompts working - Ready for production!")
    elif successful >= 20:
        print(f"\n✅ GOOD! {successful}/30 prompts working - Minor issues to address")
    elif successful >= 15:
        print(f"\n⚠️  NEEDS WORK! {successful}/30 prompts working - Significant issues")
    else:
        print(f"\n❌ CRITICAL ISSUES! Only {successful}/30 prompts working")
    
    print(f"\n📋 DETAILED RESULTS:")
    print("-" * 80)
    for result in results:
        print(f"{result['number']:2d}. {result['status']} - {result['prompt']}")
        if result['status'] == "❌ FAILED" or result['status'] == "❌ ERROR":
            print(f"    Response: {result['response']}")
    
    return successful, failed, results

if __name__ == "__main__":
    test_top_30_critical_prompts() 