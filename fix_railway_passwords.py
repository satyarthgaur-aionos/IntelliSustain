#!/usr/bin/env python3
"""
Fix Railway passwords - re-hash with exact bcrypt version
"""

import bcrypt
import os

def hash_password(password: str) -> str:
    """Hash password with bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def main():
    print("🔧 Fixing Railway Passwords")
    print("=" * 40)
    
    # Test passwords
    passwords = {
        "admin@inferrix.com": "admin123",
        "demo@inferrix.com": "demo123", 
        "tech@intellisustain.com": "Demo@1234"
    }
    
    print("\n📝 Generating new password hashes:")
    print("-" * 40)
    
    for email, password in passwords.items():
        # Generate new hash
        new_hash = hash_password(password)
        
        # Verify it works
        is_valid = verify_password(password, new_hash)
        
        print(f"\n👤 {email}")
        print(f"   Password: {password}")
        print(f"   New Hash: {new_hash}")
        print(f"   Verification: {'✅ Valid' if is_valid else '❌ Invalid'}")
        
        # Also test with the old hash from Railway
        if email == "tech@intellisustain.com":
            old_hash = "$2b$12$YU4exsnOVpF.9qldXfDhl.n5e22PhRKLGkh9ilbMCFanPoZyToDny"
            old_valid = verify_password(password, old_hash)
            print(f"   Old Hash Test: {'✅ Valid' if old_valid else '❌ Invalid'}")
    
    print("\n🚀 Next Steps:")
    print("1. Update the password hashes in Railway database")
    print("2. Or update main.py to use these new hashes")
    print("3. Test login with the credentials")

if __name__ == "__main__":
    main() 