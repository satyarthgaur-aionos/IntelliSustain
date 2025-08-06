#!/usr/bin/env python3
"""
Migrate users from local database to Railway PostgreSQL
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.append('backend')

from database import SessionLocal
from user_model import User

def migrate_users():
    """Migrate users to Railway database"""
    print("🔄 Migrating users to Railway database...")
    
    # Check if DATABASE_URL is set
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        print("Please ensure Railway PostgreSQL is configured")
        return
    
    print(f"✅ Database URL configured: {database_url[:20]}...")
    
    db = SessionLocal()
    try:
        # Check if users already exist
        existing_users = db.query(User).all()
        if existing_users:
            print(f"⚠️  Found {len(existing_users)} existing users in Railway database")
            print("Skipping migration to avoid duplicates")
            for user in existing_users:
                print(f"  - {user.email}")
            return
        
        # Create the same users as in your local database
        users_to_create = [
            {
                "email": "tech@intellisustain.com",
                "hashed_password": "$2b$12$YU4exsnOVpF.9qldXfDhl.n5e22PhRKLGkh9ilbMCFanPoZyToDny",
                "is_active": True,
                "role": "admin"
            },
            {
                "email": "admin@inferrix.com", 
                "hashed_password": "$2b$12$UWokWYsDsmUloq8c8ip6WOKYTV7dfjYkThYICA8QXICeblwllJe90",
                "is_active": True,
                "role": "admin"
            }
        ]
        
        print("📝 Creating users in Railway database...")
        
        for user_data in users_to_create:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if existing_user:
                print(f"⚠️  User {user_data['email']} already exists, skipping")
                continue
            
            # Create user
            user = User(
                email=user_data["email"],
                hashed_password=user_data["hashed_password"],
                is_active=user_data["is_active"],
                role=user_data["role"]
            )
            
            db.add(user)
            print(f"✅ Created user: {user_data['email']}")
        
        db.commit()
        print("🎉 User migration completed successfully!")
        
        # Show all users
        all_users = db.query(User).all()
        print(f"\n📊 Total users in Railway database: {len(all_users)}")
        for user in all_users:
            print(f"  - {user.email} ({user.role})")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def main():
    """Main migration function"""
    print("🚀 Railway User Migration")
    print("=" * 40)
    
    migrate_users()
    
    print("\n🎉 Migration complete!")
    print("You can now log in with:")
    print("  - tech@intellisustain.com (existing password)")
    print("  - admin@inferrix.com (existing password)")

if __name__ == "__main__":
    main() 