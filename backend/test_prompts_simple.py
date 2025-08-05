#!/usr/bin/env python3
"""
Simple Test for All 23 Prompts
Quick verification that prompts work without errors
"""

import os
import time
from enhanced_agentic_agent import EnhancedAgenticInferrixAgent
from TOP_20_PRACTICAL_PROMPTS import PRACTICAL_PROMPTS

# Set mock mode for testing
os.environ['MOCK_MODE'] = 'true'

def test_prompts():
    """Test all 23 prompts"""
    print("🧪 TESTING ALL 23 PROMPTS")
    print("="*60)
    
    agent = EnhancedAgenticInferrixAgent()
    results = []
    prompt_count = 0
    
    for complexity, prompts in PRACTICAL_PROMPTS.items():
        print(f"\n📋 Testing {complexity} prompts ({len(prompts)} prompts)")
        print("-" * 40)
        
        for prompt_data in prompts:
            prompt_count += 1
            prompt = prompt_data['prompt']
            scenario = prompt_data['scenario']
            
            print(f"\n{prompt_count}. {scenario}")
            print(f"   Prompt: {prompt[:80]}...")
            
            try:
                start_time = time.time()
                response = agent.process_query(prompt, user="TestUser")
                end_time = time.time()
                
                response_time = end_time - start_time
                
                # Check for common issues
                issues = []
                response_lower = response.lower()
                
                if any(error in response_lower for error in ['error', 'failed', 'exception', 'invalid']):
                    issues.append("Contains error")
                    
                if 'please provide' in response_lower or 'could you specify' in response_lower:
                    issues.append("Asks for clarification")
                    
                if len(response.strip()) < 50:
                    issues.append("Response too short")
                
                status = "✅ PASS" if not issues else "⚠️  ISSUES"
                
                print(f"   Status: {status}")
                print(f"   Time: {response_time:.2f}s")
                print(f"   Response: {response[:100]}...")
                
                if issues:
                    print(f"   Issues: {', '.join(issues)}")
                
                results.append({
                    'number': prompt_count,
                    'scenario': scenario,
                    'status': 'PASS' if not issues else 'ISSUES',
                    'issues': issues,
                    'response_time': response_time
                })
                
            except Exception as e:
                print(f"   Status: ❌ ERROR")
                print(f"   Error: {str(e)}")
                results.append({
                    'number': prompt_count,
                    'scenario': scenario,
                    'status': 'ERROR',
                    'issues': [f"Exception: {str(e)}"],
                    'response_time': 0
                })
            
            time.sleep(0.2)  # Small delay
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    total = len(results)
    passed = len([r for r in results if r['status'] == 'PASS'])
    issues = len([r for r in results if r['status'] == 'ISSUES'])
    errors = len([r for r in results if r['status'] == 'ERROR'])
    
    print(f"Total Prompts: {total}")
    print(f"✅ Passed: {passed}")
    print(f"⚠️  Issues: {issues}")
    print(f"❌ Errors: {errors}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if issues > 0:
        print(f"\n⚠️  Prompts with Issues:")
        for r in results:
            if r['status'] == 'ISSUES':
                print(f"   #{r['number']}: {r['scenario']} - {', '.join(r['issues'])}")
    
    if errors > 0:
        print(f"\n❌ Prompts with Errors:")
        for r in results:
            if r['status'] == 'ERROR':
                print(f"   #{r['number']}: {r['scenario']} - {', '.join(r['issues'])}")
    
    if passed == total:
        print(f"\n🎉 ALL PROMPTS WORKING! Ready for demo!")
    elif passed >= total * 0.9:
        print(f"\n✅ Most prompts working. Minor issues can be addressed.")
    else:
        print(f"\n⚠️  Several prompts need attention before demo.")

if __name__ == "__main__":
    test_prompts() 