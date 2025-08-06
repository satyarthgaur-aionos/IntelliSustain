#!/usr/bin/env python3
"""
Startup script for Railway deployment
Handles database setup and user migration
"""

import os
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.append('backend')

def setup_database():
    """Setup database tables and migrate users"""
    print("🚀 Starting Railway deployment setup...")
    
    try:
        # Import database components
        from database import engine, Base
        from user_model import User
        from auth_db import get_password_hash
        
        print("✅ Database modules imported successfully")
        
        # Create tables
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Database tables created successfully")
        except Exception as e:
            print(f"⚠️  Warning: Could not create database tables: {e}")
            return False
        
        # Create admin user
        try:
            from database import SessionLocal
            db = SessionLocal()
            
            # Check if admin user already exists
            admin_user = db.query(User).filter(User.email == "admin@inferrix.com").first()
            
            if not admin_user:
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
            else:
                print("✅ Admin user already exists")
            
            # Create demo user
            demo_user = db.query(User).filter(User.email == "demo@inferrix.com").first()
            
            if not demo_user:
                # Create demo user
                demo_user = User(
                    email="demo@inferrix.com",
                    hashed_password=get_password_hash("demo123"),
                    is_active=True,
                    role="user"
                )
                db.add(demo_user)
                db.commit()
                print("✅ Demo user created successfully!")
            else:
                print("✅ Demo user already exists")
            
            # Migrate existing users
            users_to_create = [
                {
                    "email": "tech@intellisustain.com",
                    "hashed_password": "$2b$12$YU4exsnOVpF.9qldXfDhl.n5e22PhRKLGkh9ilbMCFanPoZyToDny",
                    "is_active": True,
                    "role": "admin"
                }
            ]
            
            for user_data in users_to_create:
                existing_user = db.query(User).filter(User.email == user_data["email"]).first()
                if not existing_user:
                    user = User(
                        email=user_data["email"],
                        hashed_password=user_data["hashed_password"],
                        is_active=user_data["is_active"],
                        role=user_data["role"]
                    )
                    db.add(user)
                    print(f"✅ Migrated user: {user_data['email']}")
                else:
                    print(f"✅ User {user_data['email']} already exists")
            
            db.commit()
            db.close()
            
            print("🎉 Database setup completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error during user creation: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Error importing database modules: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during database setup: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Railway Database Setup")
    print("=" * 40)
    
    # Check if DATABASE_URL is set
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        print("Please ensure Railway PostgreSQL is configured")
        return False
    
    print(f"✅ Database URL configured: {database_url[:20]}...")
    
    # Wait a bit for database to be ready
    print("⏳ Waiting for database to be ready...")
    time.sleep(5)
    
    # Setup database
    success = setup_database()
    
    if success:
        print("\n🎉 Setup complete!")
        print("You can now log in with:")
        print("  Admin: admin@inferrix.com / admin123")
        print("  Demo:  demo@inferrix.com / demo123")
        print("  Tech:  tech@intellisustain.com / Demo@1234")
    else:
        print("\n⚠️  Setup completed with warnings")
        print("Application will run in demo mode")
    
    return success

if __name__ == "__main__":
    main() 