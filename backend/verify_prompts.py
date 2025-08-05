#!/usr/bin/env python3
"""
Verify All 23 Prompts
Simple verification that all prompts are properly structured
"""

from TOP_20_PRACTICAL_PROMPTS import PRACTICAL_PROMPTS

def verify_prompts():
    """Verify all prompts are properly structured"""
    print("🧪 VERIFYING ALL 23 PROMPTS")
    print("="*60)
    
    total_prompts = 0
    valid_prompts = 0
    issues = []
    
    for complexity, prompts in PRACTICAL_PROMPTS.items():
        print(f"\n📋 {complexity} PROMPTS ({len(prompts)} prompts)")
        print("-" * 40)
        
        for i, prompt_data in enumerate(prompts, 1):
            total_prompts += 1
            
            # Check required fields
            required_fields = ['prompt', 'scenario', 'use_case', 'expected_response', 'complexity', 'frequency']
            missing_fields = [field for field in required_fields if field not in prompt_data]
            
            if missing_fields:
                issues.append(f"Prompt {total_prompts} missing: {missing_fields}")
                print(f"   ❌ {i}. Missing fields: {missing_fields}")
            else:
                valid_prompts += 1
                prompt = prompt_data['prompt']
                scenario = prompt_data['scenario']
                print(f"   ✅ {i}. {scenario}")
                
                # Check prompt quality
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
    print("📊 VERIFICATION SUMMARY")
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
        print("🎉 ALL PROMPTS ARE PROPERLY STRUCTURED!")
        print("✅ Ready for demo!")
    else:
        print("⚠️  Some prompts need attention.")
    
    return success_rate == 100

def show_prompt_samples():
    """Show sample prompts from each category"""
    print(f"\n{'='*60}")
    print("📝 SAMPLE PROMPTS FROM EACH CATEGORY")
    print(f"{'='*60}")
    
    for complexity, prompts in PRACTICAL_PROMPTS.items():
        print(f"\n🎯 {complexity.upper()}:")
        for i, prompt_data in enumerate(prompts[:2], 1):  # Show first 2 from each category
            print(f"   {i}. {prompt_data['scenario']}")
            print(f"      Prompt: {prompt_data['prompt'][:80]}...")
            print()

if __name__ == "__main__":
    success = verify_prompts()
    show_prompt_samples()
    
    if success:
        print("🎉 VERIFICATION COMPLETE - ALL PROMPTS READY!")
    else:
        print("⚠️  VERIFICATION COMPLETE - SOME ISSUES FOUND") 