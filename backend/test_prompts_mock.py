#!/usr/bin/env python3
"""
Test Prompts with Mock Data
Verify that all 23 prompts work properly without API dependencies
"""

import os
import sys

# Set up mock environment
os.environ['MOCK_MODE'] = 'true'
os.environ['OPENAI_API_KEY'] = 'demo-key'

from TOP_20_PRACTICAL_PROMPTS import PRACTICAL_PROMPTS

def test_prompts_structure():
    """Test that all prompts are properly structured"""
    print("🧪 TESTING ALL 23 PROMPTS STRUCTURE")
    print("="*60)
    
    total_prompts = 0
    valid_prompts = 0
    issues = []
    
    for complexity, prompts in PRACTICAL_PROMPTS.items():
        print(f"\n📋 Testing {complexity} prompts ({len(prompts)} prompts)")
        print("-" * 40)
        
        for i, prompt_data in enumerate(prompts, 1):
            total_prompts += 1
            
            # Check required fields
            required_fields = ['prompt', 'scenario', 'use_case', 'expected_response', 'complexity', 'frequency']
            missing_fields = [field for field in required_fields if field not in prompt_data]
            
            if missing_fields:
                issues.append(f"Prompt {total_prompts} missing fields: {missing_fields}")
                print(f"   ❌ Prompt {i}: Missing fields {missing_fields}")
            else:
                valid_prompts += 1
                print(f"   ✅ Prompt {i}: {prompt_data['scenario']}")
                
                # Check prompt quality
                prompt = prompt_data['prompt']
                if len(prompt) < 10:
                    issues.append(f"Prompt {total_prompts} too short")
                elif len(prompt) > 500:
                    issues.append(f"Prompt {total_prompts} too long")
                
                # Check expected response quality
                expected = prompt_data['expected_response']
                if len(expected) < 50:
                    issues.append(f"Prompt {total_prompts} expected response too short")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 STRUCTURE TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Prompts: {total_prompts}")
    print(f"Valid Prompts: {valid_prompts}")
    print(f"Issues Found: {len(issues)}")
    
    if issues:
        print(f"\n⚠️  Issues Found:")
        for issue in issues:
            print(f"   • {issue}")
    
    success_rate = (valid_prompts / total_prompts) * 100
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("🎉 All prompts are properly structured!")
    else:
        print("⚠️  Some prompts need attention.")
    
    return success_rate == 100

def test_prompt_content():
    """Test that prompts have good content"""
    print(f"\n{'='*60}")
    print("📝 CONTENT QUALITY TEST")
    print(f"{'='*60}")
    
    good_prompts = 0
    total_prompts = 0
    
    for complexity, prompts in PRACTICAL_PROMPTS.items():
        for prompt_data in prompts:
            total_prompts += 1
            prompt = prompt_data['prompt']
            scenario = prompt_data['scenario']
            
            # Check for good content indicators
            good_indicators = [
                'device', 'temperature', 'alarm', 'hvac', 'energy', 'maintenance',
                'schedule', 'optimize', 'analyze', 'predict', 'automate', 'integrate'
            ]
            
            good_count = sum(1 for indicator in good_indicators if indicator.lower() in prompt.lower())
            
            if good_count >= 2:  # At least 2 good indicators
                good_prompts += 1
                print(f"   ✅ {scenario}: Good content ({good_count} indicators)")
            else:
                print(f"   ⚠️  {scenario}: Could be improved ({good_count} indicators)")
    
    quality_rate = (good_prompts / total_prompts) * 100
    print(f"\nContent Quality: {quality_rate:.1f}% ({good_prompts}/{total_prompts})")
    
    return quality_rate >= 80

def test_device_references():
    """Test that device references are consistent"""
    print(f"\n{'='*60}")
    print("📱 DEVICE REFERENCE TEST")
    print(f"{'='*60}")
    
    device_refs = []
    
    for complexity, prompts in PRACTICAL_PROMPTS.items():
        for prompt_data in prompts:
            prompt = prompt_data['prompt']
            
            # Extract device references
            if '300186' in prompt:
                device_refs.append('300186')
            if '150002' in prompt:
                device_refs.append('150002')
    
    print(f"Device 300186 referenced: {'300186' in device_refs}")
    print(f"Device 150002 referenced: {'150002' in device_refs}")
    
    if '300186' in device_refs and '150002' in device_refs:
        print("✅ Device references are consistent")
        return True
    else:
        print("⚠️  Some device references missing")
        return False

def main():
    """Run all tests"""
    print("🧪 COMPREHENSIVE PROMPT TESTING")
    print("Testing all 23 prompts for structure, content, and consistency")
    print("="*80)
    
    # Run tests
    structure_ok = test_prompts_structure()
    content_ok = test_prompt_content()
    devices_ok = test_device_references()
    
    # Final summary
    print(f"\n{'='*80}")
    print("🎯 FINAL TEST SUMMARY")
    print(f"{'='*80}")
    
    tests_passed = sum([structure_ok, content_ok, devices_ok])
    total_tests = 3
    
    print(f"Structure Test: {'✅ PASS' if structure_ok else '❌ FAIL'}")
    print(f"Content Test: {'✅ PASS' if content_ok else '❌ FAIL'}")
    print(f"Device Test: {'✅ PASS' if devices_ok else '❌ FAIL'}")
    print(f"Overall: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! Prompts are ready for demo!")
        return True
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 