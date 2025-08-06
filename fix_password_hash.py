#!/usr/bin/env python3
"""
Fix Password Hash
This script updates the password hash to work with the current bcrypt version.
"""

import sys
sys.path.append('backend')

from database import SessionLocal
from user_model import User
from auth_db import get_password_hash

def fix_password_hash():
    """Update the password hash for the tech user"""
    
    try:
        db = SessionLocal()
        
        # Get the tech user
        tech_user = db.query(User).filter(User.email == "tech@intellisustain.com").first()
        
        if tech_user:
            print(f"🔧 Updating password hash for {tech_user.email}...")
            
            # Create new hash with current bcrypt version
            new_hash = get_password_hash("Demo@1234")
            print(f"New hash: {new_hash[:20]}...")
            
            # Update the user's password hash
            tech_user.hashed_password = new_hash
            db.commit()
            
            print("✅ Password hash updated successfully!")
            print("Now try logging in with: tech@intellisustain.com / Demo@1234")
            
        else:
            print("❌ User not found!")
            
        db.close()
        
    except Exception as e:
        print(f"❌ Error updating password hash: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_password_hash() 