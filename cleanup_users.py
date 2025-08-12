#!/usr/bin/env python3
"""
Clean up users table - remove invalid users and keep only the valid one
"""
import sys
import os
sys.path.append('backend')

from backend.database import SessionLocal
from backend.user_model import User

def cleanup_users():
    """Remove invalid users from the database"""
    print("🧹 Cleaning up users table...")
    
    db = SessionLocal()
    try:
        # Get all users
        all_users = db.query(User).all()
        print(f"Found {len(all_users)} users in database:")
        
        for user in all_users:
            print(f"   - ID: {user.id}, Email: {user.email}, Active: {user.is_active}")
        
        # Remove users with IDs 1, 2, and 3 (the invalid ones)
        users_to_delete = db.query(User).filter(User.id.in_([1, 2, 3])).all()
        
        if users_to_delete:
            print(f"\n🗑️  Deleting {len(users_to_delete)} invalid users...")
            for user in users_to_delete:
                print(f"   - Deleting: {user.email} (ID: {user.id})")
                db.delete(user)
            
            db.commit()
            print("✅ Invalid users deleted successfully!")
        else:
            print("✅ No invalid users found to delete")
        
        # Verify the cleanup
        remaining_users = db.query(User).all()
        print(f"\n📋 Remaining users ({len(remaining_users)}):")
        for user in remaining_users:
            print(f"   - ID: {user.id}, Email: {user.email}, Active: {user.is_active}")
            
        if len(remaining_users) == 1 and remaining_users[0].email == "satyarth.gaur@aionos.ai":
            print("\n✅ Cleanup successful! Only the valid user remains.")
        else:
            print("\n⚠️  Unexpected users found after cleanup.")
            
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_users() 