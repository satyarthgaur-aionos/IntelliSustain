#!/usr/bin/env python3
"""
Debug Login Script
This script will help debug the login process and check user credentials.
"""

import os
import sys

# Add backend directory to Python path
sys.path.append('backend')

def debug_login():
    """Debug the login process"""
    
    try:
        from database import SessionLocal
        from user_model import User
        from auth_db import verify_password, get_password_hash
        
        print("🔍 Debugging login process...")
        
        # Get database session
        db = SessionLocal()
        
        # Check if users exist
        users = db.query(User).all()
        print(f"📊 Found {len(users)} users in database:")
        
        for user in users:
            print(f"  • {user.email} (active: {user.is_active}, role: {user.role})")
        
        # Test the specific user
        tech_user = db.query(User).filter(User.email == "tech@intellisustain.com").first()
        
        if tech_user:
            print(f"\n✅ User found: {tech_user.email}")
            print(f"   Active: {tech_user.is_active}")
            print(f"   Role: {tech_user.role}")
            print(f"   Password hash: {tech_user.hashed_password[:20]}...")
            
            # Test password verification
            test_password = "Demo@1234"
            is_valid = verify_password(test_password, tech_user.hashed_password)
            print(f"   Password '{test_password}' valid: {is_valid}")
            
            # Test with different password
            test_password2 = "demo123"
            is_valid2 = verify_password(test_password2, tech_user.hashed_password)
            print(f"   Password '{test_password2}' valid: {is_valid2}")
            
            # Create a new hash for comparison
            new_hash = get_password_hash("Demo@1234")
            print(f"   New hash for 'Demo@1234': {new_hash[:20]}...")
            
        else:
            print("❌ User tech@intellisustain.com not found!")
            
            # Create the user with correct password
            print("🛠️  Creating user with correct password...")
            new_hash = get_password_hash("Demo@1234")
            tech_user = User(
                email="tech@intellisustain.com",
                hashed_password=new_hash,
                is_active=True,
                role="admin"
            )
            db.add(tech_user)
            db.commit()
            print("✅ User created with correct password hash")
        
        db.close()
        
        print("\n🔧 Next steps:")
        print("1. Try logging in with: tech@intellisustain.com / Demo@1234")
        print("2. If it still fails, check the browser console for errors")
        print("3. Check the backend logs for more details")
        
    except Exception as e:
        print(f"❌ Error debugging login: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_login() 