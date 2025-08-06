#!/usr/bin/env python3
"""
Migration script to add missing columns to users table
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.append('backend')

def migrate_users_table():
    """Add missing columns to users table"""
    print("🔄 Migrating users table...")
    
    try:
        from database import engine, SessionLocal
        
        # Create a database session
        db = SessionLocal()
        
        # Add missing columns using raw SQL
        with engine.connect() as connection:
            # Check if columns exist first
            result = connection.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND table_schema = 'public'
            """)
            existing_columns = [row[0] for row in result]
            
            print(f"Existing columns: {existing_columns}")
            
            # Add is_active column if it doesn't exist
            if 'is_active' not in existing_columns:
                connection.execute("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE")
                print("✅ Added is_active column")
            
            # Add role column if it doesn't exist
            if 'role' not in existing_columns:
                connection.execute("ALTER TABLE users ADD COLUMN role VARCHAR DEFAULT 'user'")
                print("✅ Added role column")
            
            # Update existing users with default values
            connection.execute("UPDATE users SET is_active = TRUE WHERE is_active IS NULL")
            connection.execute("UPDATE users SET role = 'admin' WHERE role IS NULL")
            print("✅ Updated existing users with default values")
            
            connection.commit()
        
        db.close()
        print("🎉 Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False

def main():
    """Main migration function"""
    print("🚀 Users Table Migration")
    print("=" * 40)
    
    # Check if DATABASE_URL is set
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        return False
    
    print(f"✅ Database URL configured: {database_url[:20]}...")
    
    # Run migration
    success = migrate_users_table()
    
    if success:
        print("\n🎉 Migration complete!")
        print("Users table now has all required columns:")
        print("  - id (Primary Key)")
        print("  - email (Unique)")
        print("  - hashed_password")
        print("  - is_active (Boolean, default TRUE)")
        print("  - role (String, default 'user')")
    else:
        print("\n❌ Migration failed!")
    
    return success

if __name__ == "__main__":
    main() 