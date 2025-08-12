#!/usr/bin/env python3
"""
Check if the user exists in the database
"""
from database import SessionLocal
from user_model import User
from auth_db import verify_password

def check_user():
    """Check if the user exists in the database"""
    print("🔍 Checking user in database...")
    
    db = SessionLocal()
    try:
        # Check if user exists
        user = db.query(User).filter(User.email == "satyarth.gaur@aionos.ai").first()
        
        if user:
            print("✅ User found in database!")
            print(f"   - Email: {user.email}")
            print(f"   - Active: {user.is_active}")
            print(f"   - Hashed password: {user.hashed_password[:50]}...")
            
            # Test password verification
            is_valid = verify_password("Satya2025#", user.hashed_password)
            print(f"   - Password verification: {'✅ Valid' if is_valid else '❌ Invalid'}")
            
            return user
        else:
            print("❌ User not found in database")
            return None
            
    except Exception as e:
        print(f"❌ Error checking user: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    check_user() 