#!/usr/bin/env python3
"""
Database cleanup module for Railway deployment - One time execution
"""
import os
import psycopg2
from passlib.hash import bcrypt

def cleanup_database():
    """Clean up database and ensure correct user exists - runs only once"""
    print("🧹 Checking if database cleanup is needed...")
    
    # Get Railway database URL from environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("⚠️  DATABASE_URL not found, skipping database cleanup")
        return
    
    try:
        # Connect to Railway PostgreSQL
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Check if cleanup is already done by looking for the correct user
        cursor.execute("SELECT id, email FROM users WHERE email = %s", ("satyarth.gaur@aionos.ai",))
        existing_user = cursor.fetchone()
        
        # Check if old users still exist
        cursor.execute("SELECT COUNT(*) FROM users WHERE id IN (1, 2, 3)")
        old_users_count = cursor.fetchone()[0]
        
        if existing_user and old_users_count == 0:
            print("   ✅ Database cleanup already completed - skipping")
            return
        
        print("   🔧 Database cleanup needed - proceeding...")
        
        # Step 1: Delete old users (IDs 1, 2, 3)
        cursor.execute("DELETE FROM users WHERE id IN (1, 2, 3)")
        deleted_count = cursor.rowcount
        if deleted_count > 0:
            print(f"   ✅ Deleted {deleted_count} old user records")
        
        # Step 2: Add the correct user (satyarth.gaur@aionos.ai)
        password = "Satya2025#"
        hashed_password = bcrypt.hash(password)
        
        cursor.execute("""
            INSERT INTO users (email, hashed_password, is_active, role) 
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (email) DO UPDATE SET 
                hashed_password = EXCLUDED.hashed_password,
                is_active = EXCLUDED.is_active,
                role = EXCLUDED.role
        """, ("satyarth.gaur@aionos.ai", hashed_password, True, "user"))
        
        print("   ✅ Ensured user: satyarth.gaur@aionos.ai exists")
        
        # Commit the changes
        conn.commit()
        print("   ✅ Database cleanup completed successfully!")
        
    except Exception as e:
        print(f"   ❌ Database cleanup error: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close() 