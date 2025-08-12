#!/usr/bin/env python3
"""
Test all final demo prompts for production
"""
import requests
import json
import time

def test_final_demo_prompts():
    """Test all final demo prompts systematically"""
    print("🎯 Testing Final Demo Prompts for Production")
    print("=" * 60)
    
    # Step 1: Login to get tokens
    print("1. Logging in to get authentication tokens...")
    login_data = {
        "email": "satyarth.gaur@aionos.ai",
        "password": "Satya2025#"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            login_result = response.json()
            print("✅ Login successful!")
            
            jwt_token = login_result.get('access_token')
            inferrix_token = login_result.get('inferrix_token')
            
            if not inferrix_token:
                print("❌ No Inferrix token received")
                return
            
            print(f"   - JWT Token: {jwt_token[:50]}...")
            print(f"   - Inferrix Token: {inferrix_token[:50]}...")
            
            # Setup headers for all requests
            headers = {
                "Authorization": f"Bearer {jwt_token}",
                "X-Inferrix-Token": inferrix_token,
                "Content-Type": "application/json"
            }
            
            # Define all demo prompts organized by category
            demo_prompts = {
                "Alarm Management": [
                    "Show me the critical alarms for today",
                    "show me critical alarms for past",
                    "Show me alarms with high CO2 levels",
                    "What's the highest severity alarm right now",
                    "Show me minor alarms for the past 1 week",
                    "Show all alarms for RH/T Sensor - 150002",
                    "Building mein abhi kaunse alarms active hain",
                    "Sirf critical alarms dikhao",
                    "Saare alarms show"
                ],
                "System/Device Status": [
                    "Show me any system issues",
                    "Show me all the active devices",
                    "Show me battery status of all devices",
                    "List devices with low battery"
                ],
                "Temperature Control (2F-Room50-Thermostat)": [
                    "Give temperature of 2F-Room50-Thermostat",
                    "Show temperature in Second Floor Room 50",
                    "Set temperature in 2F-Room50-Thermostat to 24 degrees",
                    "Reduce the temperature of 2nd Floor Room 50 by 2 degrees",
                    "Increase the temperature of 2nd Floor Room 50 by 3 degrees",
                    "Room 50 2nd floor ka tapmaan kya hai",
                    "Room 50 2nd floor ka temperature kya hai",
                    "Room 50 2nd floor ka temperature 22 degree par set karo"
                ],
                "Humidity Check": [
                    "Check humidity for RH/T Sensor - 150002",
                    "Check humidity of second floor room number 50"
                ],
                "Fan Control": [
                    "Set fan speed to 0 in 2F-Room50-Thermostat",
                    "Increase the fan speed in second floor room no 50 to high speed",
                    "Second floor room 50 mein fan speed high karo"
                ],
                "Predictive Maintenance": [
                    "Predict HVAC failures for next 7 days",
                    "How to fix filter choke alarm",
                    "Predict device failures for tomorrow",
                    "Predict HVAC issues for next 30 days",
                    "Are any devices likely to fail in the next 7 days"
                ],
                "Energy Consumption": [
                    "Show me energy consumption for all devices",
                    "Get energy consumption for Room 50 2nd floor",
                    "Show me energy consumption data",
                    "Show me energy usage on 2nd floor"
                ]
            }
            
            # Test each category
            total_prompts = sum(len(prompts) for prompts in demo_prompts.values())
            current_prompt = 0
            
            results = {
                "successful": [],
                "failed": [],
                "summary": {}
            }
            
            for category, prompts in demo_prompts.items():
                print(f"\n{'='*20} {category} {'='*20}")
                category_success = 0
                category_total = len(prompts)
                
                for prompt in prompts:
                    current_prompt += 1
                    print(f"\n[{current_prompt}/{total_prompts}] Testing: {prompt}")
                    
                    try:
                        chat_data = {
                            "query": prompt,
                            "user": "satyarth.gaur@aionos.ai",
                            "device": None
                        }
                        
                        response = requests.post(
                            "http://localhost:8000/chat/enhanced",
                            json=chat_data,
                            headers=headers,
                            timeout=60
                        )
                        
                        if response.status_code == 200:
                            chat_result = response.json()
                            response_text = chat_result.get('response', '')
                            
                            # Check if response is meaningful
                            if response_text and not response_text.startswith("❌"):
                                print(f"   ✅ Success: {response_text[:100]}...")
                                results["successful"].append({
                                    "prompt": prompt,
                                    "category": category,
                                    "response": response_text[:200]
                                })
                                category_success += 1
                            else:
                                print(f"   ❌ Failed: {response_text}")
                                results["failed"].append({
                                    "prompt": prompt,
                                    "category": category,
                                    "error": response_text
                                })
                        else:
                            print(f"   ❌ HTTP Error: {response.status_code}")
                            print(f"   Error: {response.text}")
                            results["failed"].append({
                                "prompt": prompt,
                                "category": category,
                                "error": f"HTTP {response.status_code}: {response.text}"
                            })
                            
                    except Exception as e:
                        print(f"   ❌ Exception: {e}")
                        results["failed"].append({
                            "prompt": prompt,
                            "category": category,
                            "error": str(e)
                        })
                    
                    # Small delay between requests
                    time.sleep(1)
                
                # Category summary
                success_rate = (category_success / category_total) * 100
                print(f"\n📊 {category} Results: {category_success}/{category_total} ({success_rate:.1f}%)")
                results["summary"][category] = {
                    "success": category_success,
                    "total": category_total,
                    "success_rate": success_rate
                }
            
            # Final summary
            print(f"\n{'='*60}")
            print("🎯 FINAL DEMO PROMPTS TEST RESULTS")
            print("=" * 60)
            
            total_successful = len(results["successful"])
            total_failed = len(results["failed"])
            overall_success_rate = (total_successful / total_prompts) * 100
            
            print(f"📈 Overall Success Rate: {total_successful}/{total_prompts} ({overall_success_rate:.1f}%)")
            print(f"✅ Successful: {total_successful}")
            print(f"❌ Failed: {total_failed}")
            
            print(f"\n📊 Category Breakdown:")
            for category, stats in results["summary"].items():
                print(f"   {category}: {stats['success']}/{stats['total']} ({stats['success_rate']:.1f}%)")
            
            if results["failed"]:
                print(f"\n❌ Failed Prompts:")
                for failure in results["failed"][:5]:  # Show first 5 failures
                    print(f"   - {failure['prompt']}: {failure['error'][:100]}...")
                if len(results["failed"]) > 5:
                    print(f"   ... and {len(results['failed']) - 5} more")
            
            # Save detailed results
            with open("demo_prompts_test_results.json", "w") as f:
                json.dump(results, f, indent=2)
            print(f"\n💾 Detailed results saved to: demo_prompts_test_results.json")
            
            # Production readiness assessment
            print(f"\n🚀 PRODUCTION READINESS ASSESSMENT:")
            if overall_success_rate >= 90:
                print("   ✅ EXCELLENT - Ready for production demo!")
            elif overall_success_rate >= 80:
                print("   ⚠️  GOOD - Minor issues to address before demo")
            elif overall_success_rate >= 70:
                print("   ⚠️  FAIR - Several issues need fixing before demo")
            else:
                print("   ❌ POOR - Major issues need resolution before demo")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    test_final_demo_prompts() 