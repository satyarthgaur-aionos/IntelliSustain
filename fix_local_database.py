#!/usr/bin/env python3
"""
Fix Local Database Script
This script will fix the local database by recreating the users table with the correct schema.
"""

import os
import sys
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker

# Add backend directory to Python path
sys.path.append('backend')

def fix_local_database():
    """Fix the local database by recreating the users table"""
    
    try:
        from database import engine, Base
        from user_model import User
        from auth_db import get_password_hash
        
        print("🔧 Fixing local database...")
        
        # Drop the existing users table
        with engine.connect() as connection:
            print("🗑️  Dropping existing users table...")
            connection.execute(text("DROP TABLE IF EXISTS users CASCADE"))
            connection.commit()
            print("✅ Users table dropped")
        
        # Create the table with the correct schema
        print("🏗️  Creating users table with correct schema...")
        Base.metadata.create_all(bind=engine)
        print("✅ Users table created with correct schema")
        
        # Create the users
        from database import SessionLocal
        db = SessionLocal()
        
        # Create admin user
        admin_user = User(
            email="admin@inferrix.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            role="admin"
        )
        db.add(admin_user)
        print("✅ Admin user created")
        
        # Create demo user
        demo_user = User(
            email="demo@inferrix.com",
            hashed_password=get_password_hash("demo123"),
            is_active=True,
            role="user"
        )
        db.add(demo_user)
        print("✅ Demo user created")
        
        # Create tech user with existing password hash
        tech_user = User(
            email="tech@intellisustain.com",
            hashed_password="$2b$12$YU4exsnOVpF.9qldXfDhl.n5e22PhRKLGkh9ilbMCFanPoZyToDny",
            is_active=True,
            role="admin"
        )
        db.add(tech_user)
        print("✅ Tech user created")
        
        db.commit()
        db.close()
        
        print("🎉 Database fix completed successfully!")
        print("\n📋 Available users:")
        print("• tech@intellisustain.com / Demo@1234")
        print("• admin@inferrix.com / admin123")
        print("• demo@inferrix.com / demo123")
        
    except Exception as e:
        print(f"❌ Error fixing database: {e}")
        print("Please make sure your PostgreSQL server is running and accessible.")

if __name__ == "__main__":
    fix_local_database() 