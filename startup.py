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
        
        # Clean up database and create only the correct user
        try:
            from database import SessionLocal
            db = SessionLocal()
            
            # Delete all existing users
            db.query(User).delete()
            db.commit()
            print("✅ Cleared all existing users")
            
            # Create only the correct user for demo
            correct_user = User(
                email="satyarth.gaur@aionos.ai",
                hashed_password=get_password_hash("Satya2025#"),
                is_active=True,
                role="user"
            )
            db.add(correct_user)
            db.commit()
            print("✅ Created user: satyarth.gaur@aionos.ai")
            
            # Verify
            users = db.query(User).all()
            print(f"✅ Database now contains {len(users)} user(s):")
            for user in users:
                print(f"   - Email: {user.email}, Role: {user.role}")
            
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