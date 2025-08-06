#!/usr/bin/env python3
"""
Setup script to create initial admin user for Railway deployment
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
from auth_db import get_password_hash

def create_admin_user():
    """Create admin user if it doesn't exist"""
    print("🔧 Setting up admin user...")
    
    db = SessionLocal()
    try:
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.email == "admin@inferrix.com").first()
        
        if admin_user:
            print("✅ Admin user already exists")
            return
        
        # Create admin user
        admin_user = User(
            email="admin@inferrix.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            role="admin"
        )
        
        db.add(admin_user)
        db.commit()
        
        print("✅ Admin user created successfully!")
        print("📧 Email: admin@inferrix.com")
        print("🔑 Password: admin123")
        print("⚠️  Remember to change password in production!")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

def create_test_user():
    """Create a test user for demo purposes"""
    print("🔧 Setting up test user...")
    
    db = SessionLocal()
    try:
        # Check if test user already exists
        test_user = db.query(User).filter(User.email == "demo@inferrix.com").first()
        
        if test_user:
            print("✅ Test user already exists")
            return
        
        # Create test user
        test_user = User(
            email="demo@inferrix.com",
            hashed_password=get_password_hash("demo123"),
            is_active=True,
            role="user"
        )
        
        db.add(test_user)
        db.commit()
        
        print("✅ Test user created successfully!")
        print("📧 Email: demo@inferrix.com")
        print("🔑 Password: demo123")
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main setup function"""
    print("🚀 Railway Database Setup")
    print("=" * 40)
    
    # Check if DATABASE_URL is set
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        print("Please ensure Railway PostgreSQL is configured")
        return
    
    print(f"✅ Database URL configured: {database_url[:20]}...")
    
    # Create users
    create_admin_user()
    create_test_user()
    
    print("\n🎉 Setup complete!")
    print("You can now log in with:")
    print("  Admin: admin@inferrix.com / admin123")
    print("  Demo:  demo@inferrix.com / demo123")

if __name__ == "__main__":
    main() 