#!/usr/bin/env python3
"""
Fix Railway Database Password Hash
"""

import os
import psycopg2
from passlib.hash import bcrypt

def fix_railway_password():
    """Fix the malformed bcrypt hash in Railway database"""
    print("🔧 Fixing Railway Database Password Hash...")
    
    # Get Railway database URL from environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("⚠️  DATABASE_URL not found")
        return
    
    try:
        # Connect to Railway PostgreSQL
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("✅ Connected to Railway database")
        
        # Step 1: Check current user
        cursor.execute("SELECT id, email, hashed_password FROM users WHERE email = %s", ("satyarth.gaur@aionos.ai",))
        user = cursor.fetchone()
        
        if user:
            print(f"✅ Found user: {user[1]}")
            print(f"   Current hash: {user[2][:20]}...")
        else:
            print("❌ User not found, creating new user")
        
        # Step 2: Generate correct password hash
        password = "Satya2025#"
        correct_hash = bcrypt.hash(password)
        print(f"✅ Generated correct hash: {correct_hash[:20]}...")
        
        # Step 3: Update or insert user
        if user:
            cursor.execute("""
                UPDATE users 
                SET hashed_password = %s, is_active = TRUE, role = 'user'
                WHERE email = %s
            """, (correct_hash, "satyarth.gaur@aionos.ai"))
            print("✅ Updated existing user with correct password hash")
        else:
            cursor.execute("""
                INSERT INTO users (email, hashed_password, is_active, role)
                VALUES (%s, %s, %s, %s)
            """, ("satyarth.gaur@aionos.ai", correct_hash, True, "user"))
            print("✅ Created new user with correct password hash")
        
        # Step 4: Verify the fix
        cursor.execute("SELECT id, email, hashed_password FROM users WHERE email = %s", ("satyarth.gaur@aionos.ai",))
        updated_user = cursor.fetchone()
        
        if updated_user:
            # Test the password verification
            stored_hash = updated_user[2]
            if bcrypt.verify(password, stored_hash):
                print("✅ Password verification successful!")
            else:
                print("❌ Password verification failed!")
        else:
            print("❌ User not found after update!")
        
        # Commit the changes
        conn.commit()
        print("✅ Railway database password hash fixed successfully!")
        
    except Exception as e:
        print(f"❌ Database fix error: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    fix_railway_password()
