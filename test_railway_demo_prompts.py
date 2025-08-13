#!/usr/bin/env python3
"""
Test Final Demo Prompts on Railway Deployment
"""
import requests
import json
import time
from datetime import datetime

# Railway deployment URL
RAILWAY_URL = "https://intellisustain-production.up.railway.app"

def test_railway_demo_prompts():
    """Test all demo prompts on Railway deployment"""
    print("🚀 TESTING RAILWAY DEPLOYMENT - FINAL DEMO PROMPTS")
    print("=" * 80)
    print(f"📍 Testing URL: {RAILWAY_URL}")
    print(f"⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Step 1: Login to get tokens
    print("\n1️⃣ Logging in to get authentication tokens...")
    login_data = {
        "email": "satyarth.gaur@aionos.ai",
        "password": "Satya2025#"
    }
    
    try:
        response = requests.post(
            f"{RAILWAY_URL}/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            login_result = response.json()
            jwt_token = login_result.get('access_token')
            inferrix_token = login_result.get('inferrix_token')
            
            if jwt_token and inferrix_token:
                print("✅ Login successful!")
                print(f"   - JWT Token: {jwt_token[:50]}...")
                print(f"   - Inferrix Token: {inferrix_token[:50]}...")
            else:
                print("❌ Login successful but missing tokens")
                return
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Headers for all requests
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "X-Inferrix-Token": inferrix_token,
        "Content-Type": "application/json"
    }
    
    # Test prompts (same as local test)
    test_prompts = [
        # Alarm Management
        "Show me the critical alarms for today",
        "show me critical alarms for past",
        "Show me alarms with high CO2 levels",
        "What's the highest severity alarm right now",
        "Show me minor alarms for the past 1 week",
        "Show all alarms for RH/T Sensor - 150002",
        "Building mein abhi kaunse alarms active hain",
        "Sirf critical alarms dikhao",
        "Saare alarms show",
        
        # System/Device Status
        "Show me any system issues",
        "Show me all the active devices",
        "Show me battery status of all devices",
        "List devices with low battery",
        
        # Temperature Control
        "Give temperature of 2F-Room50-Thermostat",
        "Show temperature in Second Floor Room 50",
        "Set temperature in 2F-Room50-Thermostat to 24 degrees",
        "Reduce the temperature of 2nd Floor Room 50 by 2 degrees",
        "Increase the temperature of 2nd Floor Room 50 by 3 degrees",
        "Room 50 2nd floor ka tapmaan kya hai",
        "Room 50 2nd floor ka temperature kya hai",
        "Room 50 2nd floor ka temperature 22 degree par set karo",
        
        # Humidity Check
        "Check humidity for RH/T Sensor - 150002",
        "Check humidity of second floor room number 50",
        
        # Fan Control
        "Set fan speed to 0 in 2F-Room50-Thermostat",
        "Increase the fan speed in second floor room no 50 to high speed",
        "Second floor room 50 mein fan speed high karo",
        
        # Predictive Maintenance
        "Predict HVAC failures for next 7 days",
        "How to fix filter choke alarm",
        "Predict device failures for tomorrow",
        "Predict HVAC issues for next 30 days",
        "Are any devices likely to fail in the next 7 days",
        
        # Energy Consumption
        "Show me energy consumption for all devices",
        "Get energy consumption for Room 50 2nd floor",
        "Show me energy consumption data",
        "Show me energy usage on 2nd floor"
    ]
    
    # Categories for organization
    categories = {
        "Alarm Management": list(range(0, 9)),
        "System/Device Status": list(range(9, 13)),
        "Temperature Control": list(range(13, 21)),
        "Humidity Check": list(range(21, 23)),
        "Fan Control": list(range(23, 26)),
        "Predictive Maintenance": list(range(26, 31)),
        "Energy Consumption": list(range(31, 35))
    }
    
    results = []
    successful = 0
    failed = 0
    
    # Test each prompt
    for i, prompt in enumerate(test_prompts):
        print(f"\n[{i+1}/{len(test_prompts)}] Testing: {prompt}")
        
        try:
            response = requests.post(
                f"{RAILWAY_URL}/chat/enhanced",
                json={
                    "query": prompt,
                    "user": "satyarth.gaur@aionos.ai",
                    "device": None
                },
                headers=headers,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', '')
                
                if ai_response and not ai_response.startswith('❌'):
                    print(f"   ✅ Success: {ai_response[:100]}...")
                    results.append({"prompt": prompt, "status": "success", "response": ai_response})
                    successful += 1
                else:
                    print(f"   ❌ Failed: {ai_response}")
                    results.append({"prompt": prompt, "status": "failed", "response": ai_response})
                    failed += 1
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                print(f"   Error: {response.text}")
                results.append({"prompt": prompt, "status": "failed", "response": f"HTTP {response.status_code}"})
                failed += 1
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            results.append({"prompt": prompt, "status": "failed", "response": str(e)})
            failed += 1
        
        # Small delay between requests
        time.sleep(1)
    
    # Calculate category results
    category_results = {}
    for category, indices in categories.items():
        category_success = sum(1 for i in indices if results[i]["status"] == "success")
        category_total = len(indices)
        category_results[category] = {
            "success": category_success,
            "total": category_total,
            "percentage": (category_success / category_total * 100) if category_total > 0 else 0
        }
    
    # Print final results
    print("\n" + "=" * 80)
    print("🎯 RAILWAY DEMO PROMPTS TEST RESULTS")
    print("=" * 80)
    print(f"📈 Overall Success Rate: {successful}/{len(test_prompts)} ({successful/len(test_prompts)*100:.1f}%)")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    
    print(f"\n📊 Category Breakdown:")
    for category, stats in category_results.items():
        print(f"   {category}: {stats['success']}/{stats['total']} ({stats['percentage']:.1f}%)")
    
    if failed > 0:
        print(f"\n❌ Failed Prompts:")
        for result in results:
            if result["status"] == "failed":
                print(f"   - {result['prompt']}: {result['response'][:100]}...")
    
    # Save detailed results
    output_file = "railway_demo_prompts_test_results.json"
    with open(output_file, 'w') as f:
        json.dump({
            "test_time": datetime.now().isoformat(),
            "railway_url": RAILWAY_URL,
            "overall_results": {
                "successful": successful,
                "failed": failed,
                "total": len(test_prompts),
                "success_rate": successful/len(test_prompts)*100
            },
            "category_results": category_results,
            "detailed_results": results
        }, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    
    # Production readiness assessment
    success_rate = successful/len(test_prompts)*100
    if success_rate >= 95:
        assessment = "✅ EXCELLENT - Ready for production demo!"
    elif success_rate >= 90:
        assessment = "✅ GOOD - Minor issues, ready for demo"
    elif success_rate >= 80:
        assessment = "⚠️ ACCEPTABLE - Some issues, needs attention"
    else:
        assessment = "❌ NEEDS WORK - Significant issues found"
    
    print(f"\n🚀 PRODUCTION READINESS ASSESSMENT:")
    print(f"   {assessment}")

if __name__ == "__main__":
    test_railway_demo_prompts()
