#!/usr/bin/env python3
"""
Script to fix the device mapping logic in agentic_agent.py
"""

def fix_device_mapping():
    """Fix the device mapping logic in _get_device_telemetry function"""
    
    # Read the original file
    with open('agentic_agent.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Old logic to replace
    old_logic = '''            # Check if device_id is actually a device name (contains letters/spaces)
            if not device_id.isdigit() and any(c.isalpha() for c in device_id) and '-' not in device_id:
                # This might be a device name, try to map it to ID
                mapped_id = self._map_device_name_to_id(device_id)
                if mapped_id:
                    device_id = mapped_id
                else:
                    return f"❌ Device '{device_id}' not found. Please use a valid device ID or check the device name."'''
    
    # New logic to insert
    new_logic = '''            # Always attempt mapping if device_id is not a valid UUID
            def is_uuid(val):
                return isinstance(val, str) and len(val) == 36 and val.count('-') == 4

            if not is_uuid(device_id):
                print(f"[DEBUG] Attempting to map device name/ID: '{device_id}' to UUID")
                mapped_id = self._map_device_name_to_id(device_id)
                if mapped_id:
                    print(f"[DEBUG] Successfully mapped '{device_id}' to '{mapped_id}'")
                    device_id = mapped_id
                else:
                    print(f"[DEBUG] Failed to map '{device_id}' to any UUID")
                    return f"❌ Device '{device_id}' not found. Please use a valid device ID or check the device name."'''
    
    # Replace the old logic with new logic
    if old_logic in content:
        new_content = content.replace(old_logic, new_logic)
        
        # Write the fixed content back to the file
        with open('agentic_agent.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Successfully fixed device mapping logic in agentic_agent.py")
        print("   - Old logic: Only mapped device names without hyphens")
        print("   - New logic: Always maps any non-UUID to UUID using robust mapping")
        return True
    else:
        print("❌ Could not find the old device mapping logic to replace")
        print("   The file may have already been fixed or the logic is different")
        return False

if __name__ == "__main__":
    print("🔧 Fixing device mapping logic in agentic_agent.py...")
    success = fix_device_mapping()
    if success:
        print("\n🎉 Device mapping fix applied successfully!")
        print("   You can now test with: python test_device_mapping.py")
    else:
        print("\n⚠️  Please check the file manually or contact support") 