#!/usr/bin/env python3
"""
Railway Variables Checker
This script helps verify that Railway environment variables are set correctly.
"""

import os

def check_railway_variables():
    """Check Railway environment variables"""
    
    print("🔍 Checking Railway Environment Variables...")
    print("=" * 50)
    
    # Check critical variables
    critical_vars = [
        "DATABASE_URL",
        "INFERRIX_API_TOKEN", 
        "OPENAI_API_KEY",
        "GOOGLE_API_KEY",
        "JWT_SECRET_KEY"
    ]
    
    for var in critical_vars:
        value = os.getenv(var)
        if value:
            # Show first 20 characters for security
            display_value = value[:20] + "..." if len(value) > 20 else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NOT SET")
    
    print("=" * 50)
    
    # Check for any DATABASE related variables
    db_vars = [k for k in os.environ.keys() if 'DATABASE' in k.upper() or 'DB' in k.upper()]
    if db_vars:
        print(f"📊 Found database-related variables: {db_vars}")
    else:
        print("⚠️  No database-related variables found")
    
    print("=" * 50)
    print("🔧 Next Steps:")
    print("1. If DATABASE_URL is not set, add it to Railway variables")
    print("2. Make sure to use: ${{ Postgres.DATABASE_URL }}")
    print("3. Check that the PostgreSQL service is connected")

if __name__ == "__main__":
    check_railway_variables() 