#!/usr/bin/env python3
"""
Test Password Verification
This script tests if the password verification works with the existing hash.
"""

import sys
sys.path.append('backend')

from auth_db import verify_password

def test_password():
    """Test password verification"""
    
    # The hash from the database
    stored_hash = "$2b$12$YU4exsnOVpF.9qldXfDhl.n5e22PhRKLGkh9ilbMCFanPoZyToDny"
    
    # Test the password
    password = "Demo@1234"
    
    print(f"🔍 Testing password verification...")
    print(f"Password: {password}")
    print(f"Stored hash: {stored_hash[:20]}...")
    
    try:
        is_valid = verify_password(password, stored_hash)
        print(f"✅ Password verification result: {is_valid}")
        
        if is_valid:
            print("🎉 Password verification works!")
        else:
            print("❌ Password verification failed!")
            
    except Exception as e:
        print(f"❌ Error during password verification: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_password() 