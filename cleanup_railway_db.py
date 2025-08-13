#!/usr/bin/env python3
"""
Clean up Railway PostgreSQL database and add correct user
"""
import os
import psycopg2
from passlib.hash import bcrypt

def cleanup_railway_database():
    """Clean up Railway database and add correct user"""
    print("🧹 Cleaning up Railway PostgreSQL Database...")
    print("=" * 50)
    
    # Get Railway database URL from environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not found")
        print("Please set DATABASE_URL in Railway environment variables")
        return
    
    try:
        # Connect to Railway PostgreSQL
        print("1. Connecting to Railway PostgreSQL...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        print("✅ Connected to Railway PostgreSQL")
        
        # Step 1: Check current users
        print("\n2. Checking current users in Railway database...")
        cursor.execute("SELECT id, email, is_active, role FROM users ORDER BY id")
        current_users = cursor.fetchall()
        
        print(f"   Current users in Railway database:")
        for user in current_users:
            print(f"   - ID: {user[0]}, Email: {user[1]}, Active: {user[2]}, Role: {user[3]}")
        
        # Step 2: Delete old users (IDs 1, 2, 3)
        print("\n3. Deleting old users (IDs 1, 2, 3)...")
        cursor.execute("DELETE FROM users WHERE id IN (1, 2, 3)")
        deleted_count = cursor.rowcount
        print(f"   ✅ Deleted {deleted_count} old user records")
        
        # Step 3: Add the correct user (satyarth.gaur@aionos.ai)
        print("\n4. Adding correct user (satyarth.gaur@aionos.ai)...")
        
        # Hash the password
        password = "Satya2025#"
        hashed_password = bcrypt.hash(password)
        
        # Insert the user
        cursor.execute("""
            INSERT INTO users (email, hashed_password, is_active, role) 
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (email) DO UPDATE SET 
                hashed_password = EXCLUDED.hashed_password,
                is_active = EXCLUDED.is_active,
                role = EXCLUDED.role
        """, ("satyarth.gaur@aionos.ai", hashed_password, True, "user"))
        
        print("   ✅ Added/Updated user: satyarth.gaur@aionos.ai")
        
        # Step 4: Verify the changes
        print("\n5. Verifying database state...")
        cursor.execute("SELECT id, email, is_active, role FROM users ORDER BY id")
        final_users = cursor.fetchall()
        
        print(f"   Final users in Railway database:")
        for user in final_users:
            print(f"   - ID: {user[0]}, Email: {user[1]}, Active: {user[2]}, Role: {user[3]}")
        
        # Commit the changes
        conn.commit()
        print("\n✅ Railway database cleanup completed successfully!")
        
        # Step 5: Test the user credentials
        print("\n6. Testing user credentials...")
        cursor.execute("SELECT hashed_password FROM users WHERE email = %s", ("satyarth.gaur@aionos.ai",))
        result = cursor.fetchone()
        
        if result:
            stored_hash = result[0]
            if bcrypt.verify(password, stored_hash):
                print("   ✅ Password verification successful!")
            else:
                print("   ❌ Password verification failed!")
        else:
            print("   ❌ User not found!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("\n🔗 Database connection closed")

if __name__ == "__main__":
    cleanup_railway_database() 