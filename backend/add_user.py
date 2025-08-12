#!/usr/bin/env python3
"""
Add the Inferrix user to the PostgreSQL database
"""
import sys
import os
sys.path.append('.')

from database import SessionLocal, engine
from user_model import User, Base
from auth_db import get_password_hash

def add_inferrix_user():
    """Add the Inferrix user to the database"""
    print("🔐 Adding Inferrix user to database...")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == "satyarth.gaur@aionos.ai").first()
        
        if existing_user:
            print("✅ User already exists in database")
            return existing_user
        
        # Create new user
        hashed_password = get_password_hash("Satya2025#")
        new_user = User(
            email="satyarth.gaur@aionos.ai",
            hashed_password=hashed_password,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print("✅ User added successfully!")
        print(f"   - Email: {new_user.email}")
        print(f"   - Active: {new_user.is_active}")
        
        return new_user
        
    except Exception as e:
        print(f"❌ Error adding user: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    add_inferrix_user() 