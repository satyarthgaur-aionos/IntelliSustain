#!/usr/bin/env python3
"""
Test New Password Verification
This script tests the new password hash from the database.
"""

import sys
sys.path.append('backend')

from database import SessionLocal
from user_model import User
from auth_db import verify_password

def test_new_password():
    """Test the new password hash from database"""
    
    try:
        db = SessionLocal()
        
        # Get the tech user with updated hash
        tech_user = db.query(User).filter(User.email == "tech@intellisustain.com").first()
        
        if tech_user:
            print(f"🔍 Testing new password hash for {tech_user.email}...")
            print(f"New hash: {tech_user.hashed_password[:20]}...")
            
            # Test the password
            password = "Demo@1234"
            is_valid = verify_password(password, tech_user.hashed_password)
            
            print(f"✅ Password verification result: {is_valid}")
            
            if is_valid:
                print("🎉 Password verification works!")
                print("Now try logging in with: tech@intellisustain.com / Demo@1234")
            else:
                print("❌ Password verification still failed!")
                
        else:
            print("❌ User not found!")
            
        db.close()
        
    except Exception as e:
        print(f"❌ Error during password verification: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_new_password() 