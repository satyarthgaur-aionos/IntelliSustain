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
        
        # FORCE CLEAN DATABASE - Delete all users and recreate
        try:
            from database import SessionLocal
            db = SessionLocal()
            
            # Step 1: Delete ALL users using raw SQL to ensure complete cleanup
            print("🧹 FORCE CLEANING DATABASE - Deleting all users...")
            db.execute("DELETE FROM users")
            db.commit()
            print("✅ All users deleted from database")
            
            # Step 2: Reset the sequence to start from 1
            try:
                db.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1")
                db.commit()
                print("✅ Reset user ID sequence")
            except Exception as e:
                print(f"⚠️  Could not reset sequence: {e}")
            
            # Step 3: Create ONLY the correct user with proper password hash
            print("👤 Creating correct user: satyarth.gaur@aionos.ai")
            
            # Generate password hash using bcrypt directly to ensure compatibility
            from passlib.hash import bcrypt
            password = "Satya2025#"
            hashed_password = bcrypt.hash(password)
            
            correct_user = User(
                email="satyarth.gaur@aionos.ai",
                hashed_password=hashed_password,
                is_active=True,
                role="user"
            )
            db.add(correct_user)
            db.commit()
            print("✅ Created user: satyarth.gaur@aionos.ai with correct password hash")
            
            # Verify the password hash works
            if bcrypt.verify(password, hashed_password):
                print("✅ Password hash verification successful!")
            else:
                print("❌ Password hash verification failed!")
            
            # Step 4: Verify database state
            users = db.query(User).all()
            print(f"✅ Database now contains {len(users)} user(s):")
            for user in users:
                print(f"   - ID: {user.id}, Email: {user.email}, Role: {user.role}")
            
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
        print("  Email: satyarth.gaur@aionos.ai")
        print("  Password: Satya2025#")
    else:
        print("\n⚠️  Setup completed with warnings")
        print("Application will run in demo mode")
    
    return success

if __name__ == "__main__":
    main() 