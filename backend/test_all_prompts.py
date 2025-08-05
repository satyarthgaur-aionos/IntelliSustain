#!/usr/bin/env python3
"""
Comprehensive test script for all 205 demo prompts with the agentic AI implementation
Covers all 6 BMS personas: Facility Manager, Energy Manager, Maintenance Technician, Security Officer, Operations Manager, Occupant/End User
"""

import os
import sys
import time
from dotenv import load_dotenv
import argparse
import requests
import json

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agentic_agent import agentic_agent

def load_prompts_from_file():
    """Load all prompts from demo_prompts.txt file"""
    prompts = []
    current_category = ""
    
    try:
        with open("../demo_prompts.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("##") and "**" in line:
                    current_category = line
                elif line and line[0].isdigit() and ". " in line:
                    # Extract prompt from numbered line
                    prompt = line.split(". ", 1)[1] if ". " in line else line
                    prompts.append({
                        "category": current_category,
                        "prompt": prompt,
                        "number": line.split(". ")[0] if ". " in line else "0"
                    })
    except FileNotFoundError:
        print("❌ demo_prompts.txt not found. Using built-in prompts.")
        return get_builtin_prompts()
    
    return prompts

def get_builtin_prompts():
    """Fallback prompts if file is not found"""
    return [
        # Facility Manager
        {"category": "🏢 FACILITY MANAGER", "prompt": "What is the current temperature and occupancy in zone 4?", "number": "1"},
        {"category": "🏢 FACILITY MANAGER", "prompt": "Show temperature for IAQ Sensor V2 - 300186", "number": "12"},
        
        # Energy Manager
        {"category": "⚡ ENERGY MANAGER", "prompt": "Turn off HVAC and dim lights in the east wing on Saturday and Sunday", "number": "17"},
        {"category": "⚡ ENERGY MANAGER", "prompt": "How much carbon emissions did we reduce this week?", "number": "23"},
        
        # Maintenance Technician
        {"category": "🔧 MAINTENANCE TECHNICIAN", "prompt": "Are any HVAC or lighting systems likely to fail in the next 7 days?", "number": "34"},
        {"category": "🔧 MAINTENANCE TECHNICIAN", "prompt": "Show all active alarms", "number": "40"},
        
        # Security Officer
        {"category": "🔒 SECURITY OFFICER", "prompt": "Monitor security systems for unauthorized access in the main entrance", "number": "65"},
        {"category": "🔒 SECURITY OFFICER", "prompt": "Grant access to the executive floor for user ID 12345", "number": "71"},
        
        # Operations Manager
        {"category": "📊 OPERATIONS MANAGER", "prompt": "Show me comprehensive operational analytics for this month", "number": "81"},
        {"category": "📊 OPERATIONS MANAGER", "prompt": "Compare our performance against hospitality industry benchmarks", "number": "83"},
        {"category": "📊 OPERATIONS MANAGER", "prompt": "List all assets in the system", "number": "101"},
        {"category": "📊 OPERATIONS MANAGER", "prompt": "Show all entity views", "number": "102"},
        {"category": "📊 OPERATIONS MANAGER", "prompt": "Show my notifications", "number": "106"},
        
        # Occupant/End User
        {"category": "👤 OCCUPANT/END USER", "prompt": "Lower the temperature by 2 degrees in Conference Room B for the next 3 hours", "number": "111"},
        {"category": "👤 OCCUPANT/END USER", "prompt": "Adjust temperature for my workspace", "number": "117"},
    ]

def test_prompts_by_category(prompts, test_mode="sample"):
    """Test prompts organized by category"""
    
    print("🧪 Testing All Demo Prompts with Agentic AI Implementation\n")
    print(f"Total prompts loaded: {len(prompts)}")
    print(f"Test mode: {test_mode}\n")
    
    # Group prompts by category
    categories = {}
    for prompt_data in prompts:
        category = prompt_data["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append(prompt_data)
    
    total_successful = 0
    total_failed = 0
    category_results = {}
    
    for category, category_prompts in categories.items():
        print(f"\n{'='*80}")
        print(f"📋 Testing Category: {category}")
        print(f"{'='*80}")
        
        # For sample mode, test only first 2 prompts per category
        if test_mode == "sample":
            test_prompts = category_prompts[:2]
        else:
            test_prompts = category_prompts
        
        category_successful = 0
        category_failed = 0
        
        for i, prompt_data in enumerate(test_prompts, 1):
            prompt = prompt_data["prompt"]
            number = prompt_data["number"]
            
            print(f"\nTest {number}: {prompt[:70]}{'...' if len(prompt) > 70 else ''}")
            
            try:
                start_time = time.time()
                result = agentic_agent.process_query(prompt, "TestUser")
                end_time = time.time()
                
                # Check if the response is valid
                if result and not result.startswith("❌ Error") and not result.startswith("❌ **Error"):
                    print(f"✅ SUCCESS ({end_time-start_time:.2f}s): {result[:100]}{'...' if len(result) > 100 else ''}")
                    category_successful += 1
                else:
                    print(f"❌ FAILED: {result[:200]}{'...' if len(result) > 200 else ''}")
                    category_failed += 1
                    
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
                category_failed += 1
            
            # Small delay to avoid overwhelming the API
            time.sleep(2.0)  # Increased from 0.5s to 2.0s to avoid rate limiting
        
        category_results[category] = {
            "successful": category_successful,
            "failed": category_failed,
            "total": len(test_prompts)
        }
        
        total_successful += category_successful
        total_failed += category_failed
        
        print(f"\n📊 Category Results: ✅ {category_successful} | ❌ {category_failed} | 📈 {(category_successful/len(test_prompts)*100):.1f}%")
    
    return total_successful, total_failed, category_results

def print_final_summary(total_successful, total_failed, category_results):
    """Print comprehensive test summary"""
    
    print(f"\n{'='*80}")
    print(f"📊 COMPREHENSIVE TEST RESULTS SUMMARY")
    print(f"{'='*80}")
    
    print(f"\n🎯 Overall Results:")
    print(f"✅ Total Successful: {total_successful}")
    print(f"❌ Total Failed: {total_failed}")
    print(f"📈 Overall Success Rate: {(total_successful/(total_successful+total_failed)*100):.1f}%")
    
    print(f"\n📋 Results by Category:")
    for category, results in category_results.items():
        success_rate = (results["successful"]/results["total"]*100) if results["total"] > 0 else 0
        status = "✅" if success_rate >= 90 else "⚠️" if success_rate >= 70 else "❌"
        print(f"{status} {category}: {results['successful']}/{results['total']} ({success_rate:.1f}%)")
    
    print(f"\n🎉 BMS Persona Coverage:")
    persona_categories = [
        "🏢 FACILITY MANAGER",
        "⚡ ENERGY MANAGER", 
        "🔧 MAINTENANCE TECHNICIAN",
        "🔒 SECURITY OFFICER",
        "📊 OPERATIONS MANAGER",
        "👤 OCCUPANT/END USER"
    ]
    
    for persona in persona_categories:
        if persona in category_results:
            results = category_results[persona]
            success_rate = (results["successful"]/results["total"]*100) if results["total"] > 0 else 0
            status = "✅ FULLY FUNCTIONAL" if success_rate >= 90 else "⚠️ NEEDS ATTENTION" if success_rate >= 70 else "❌ MAJOR ISSUES"
            print(f"   {persona}: {status} ({success_rate:.1f}%)")
    
    if total_failed == 0:
        print(f"\n🎉 PERFECT! All tested prompts are working with the agentic implementation!")
    elif total_failed <= 5:
        print(f"\n✅ EXCELLENT! Only {total_failed} prompts need minor attention.")
    elif total_failed <= 10:
        print(f"\n⚠️  GOOD! {total_failed} prompts need attention before demo.")
    else:
        print(f"\n❌ NEEDS WORK! {total_failed} prompts have issues that need to be resolved.")

def get_sample_prompts(prompts):
    """Get sample prompts (2 per category) for quick testing"""
    sample_prompts = []
    category_counts = {}
    
    for prompt in prompts:
        category = prompt.get('category', 'Unknown')
        if category not in category_counts:
            category_counts[category] = 0
        
        if category_counts[category] < 2:
            sample_prompts.append(prompt)
            category_counts[category] += 1
    
    return sample_prompts

def get_persona_prompts(prompts, persona):
    """Get prompts for a specific persona"""
    persona_mapping = {
        'facility': 'Facility Manager',
        'energy': 'Energy Manager', 
        'maintenance': 'Maintenance Technician',
        'security': 'Security Officer',
        'operations': 'Operations Manager',
        'occupant': 'Occupant/End User'
    }
    
    target_persona = persona_mapping.get(persona)
    if not target_persona:
        return []
    
    return [p for p in prompts if p.get('category') == target_persona]

def test_all_demo_prompts(mode):
    """Main test function"""
    print("🔍 Loading prompts from demo_prompts.txt...")
    prompts = load_prompts_from_file()
    
    if not prompts:
        print("❌ No prompts loaded. Check demo_prompts.txt file.")
        return
    
    print(f"📋 Loaded {len(prompts)} total prompts")
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Test all demo prompts")
    parser.add_argument('--mode', choices=['sample', 'full', 'persona', 'top10'], 
                       default='sample', help='Test mode: sample (2 per category), full (all prompts), persona (specific persona), top10 (most important)')
    parser.add_argument('--persona', choices=['facility', 'energy', 'maintenance', 'security', 'operations', 'occupant'],
                       help='Specific persona to test (use with --mode persona)')
    
    args = parser.parse_args()
    
    print(f"🚀 Starting {args.mode.upper()} test mode...")
    if args.mode == 'sample':
        test_prompts = get_sample_prompts(prompts)
    elif args.mode == 'full':
        test_prompts = prompts
    elif args.mode == 'persona':
        if not args.persona:
            print("❌ Error: --persona argument required when using --mode persona")
            sys.exit(1)
        test_prompts = get_persona_prompts(prompts, args.persona)
    elif args.mode == 'top10':
        # Add top 10 prompts
        top10_prompts = [
            "What is the current temperature and occupancy in zone 4?",
            "Show me the temperature and humidity in the east wing.",
            "Optimize energy usage for the building today.",
            "Show energy consumption trends for the last month.",
            "Notify me if any sensor detects abnormal readings or faults.",
            "Show all active alarms.",
            "Monitor security systems for unauthorized access in the main entrance.",
            "Show me comprehensive operational analytics for this month.",
            "Adjust the HVAC settings in my workspace for comfort.",
            "List all devices."
        ]
        # Convert to dicts as expected by test logic
        test_prompts = []
        for idx, prompt in enumerate(top10_prompts, 1):
            match = next((p for p in prompts if p.get("prompt", "").strip() == prompt.strip()), None)
            if match:
                test_prompts.append(match)
            else:
                test_prompts.append({"prompt": prompt, "category": "Top10", "number": idx})
    else:
        test_prompts = get_sample_prompts(prompts)

    # Test prompts by category
    total_successful, total_failed, category_results = test_prompts_by_category(test_prompts, args.mode)
    
    # Print final summary
    print_final_summary(total_successful, total_failed, category_results)
    
    return total_successful, total_failed

# Automated test script
if __name__ == "__main__":
    # List of prompts to test (add more as needed)
    prompts = [
        "What is the current temperature and occupancy in zone 4?",
        "Show me the temperature and humidity in the east wing.",
        "What's the environmental status in Conference Room B?",
        "Check temperature and occupancy in the main lobby.",
        "Monitor environmental conditions in the north wing.",
        "Show me real-time data for the west wing.",
        "What's the temperature in the 3rd floor?",
        "Check occupancy levels in Tower A.",
        "Show environmental data for the executive floor.",
        "Monitor conditions in the parking garage.",
        "What's the status in the server room?",
        "Show temperature for IAQ Sensor V2 - 300186.",
        "Check humidity for RH/T Sensor - 150002.",
        "Show telemetry for device 2F-Room33-Thermostat.",
        "What's the battery level of device 300186?",
        "Check device health for IAQ Sensor V2 - 300186.",
        # ... add more prompts as needed ...
    ]

    # Backend URL and JWT token (update as needed)
    BACKEND_URL = "http://localhost:8000/chat/enhanced"
    JWT = input("Paste your JWT token here: ")

    headers = {
        "Authorization": f"Bearer {JWT}",
        "Content-Type": "application/json"
    }

    results = []

    for i, prompt in enumerate(prompts, 1):
        data = {"query": prompt, "user": "admin@inferrix.com"}  # Use the correct keys
        try:
            resp = requests.post(BACKEND_URL, headers=headers, json=data, timeout=30)
            try:
                resp_json = resp.json()
            except Exception:
                resp_json = {"error": "Non-JSON response", "raw": resp.text}
            status = resp.status_code
            print(f"[{i}] {prompt}\nStatus: {status}\nResponse: {json.dumps(resp_json, indent=2)[:500]}\n{'-'*60}")
            results.append({"prompt": prompt, "status": status, "response": resp_json})
        except Exception as e:
            print(f"[{i}] {prompt}\nERROR: {e}\n{'-'*60}")
            results.append({"prompt": prompt, "status": "ERROR", "response": str(e)})

    # Optionally, save results to a file
    with open("test_prompt_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\nTest complete. Results saved to test_prompt_results.json.") 