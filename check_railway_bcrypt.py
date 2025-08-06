#!/usr/bin/env python3
"""
Check Railway bcrypt version and generate correct hash
"""

import bcrypt
import sys

def check_bcrypt_version():
    """Check bcrypt version and capabilities"""
    print("🔍 Checking bcrypt version and capabilities")
    print("=" * 50)
    
    # Check bcrypt version
    try:
        import bcrypt
        print(f"✅ bcrypt version: {bcrypt.__version__}")
    except AttributeError:
        print("⚠️  bcrypt version not available")
    
    # Test password hashing
    password = "Demo@1234"
    
    print(f"\n📝 Testing password: {password}")
    print("-" * 30)
    
    # Generate new hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    hash_str = hashed.decode('utf-8')
    
    print(f"New hash: {hash_str}")
    
    # Test verification
    is_valid = bcrypt.checkpw(password.encode('utf-8'), hashed)
    print(f"Verification: {'✅ Valid' if is_valid else '❌ Invalid'}")
    
    # Test with the old Railway hash
    old_hash = "$2b$12$YU4exsnOVpF.9qldXfDhl.n5e22PhRKLGkh9ilbMCFanPoZyToDny"
    old_valid = bcrypt.checkpw(password.encode('utf-8'), old_hash.encode('utf-8'))
    print(f"Old Railway hash test: {'✅ Valid' if old_valid else '❌ Invalid'}")
    
    # Test with our new hash from fix_railway_passwords.py
    new_hash = "$2b$12$8p.bMoNeHn.zfSQxyoRCA.LALbtH9I8hlYlZOdbdFruPwheY7a2sS"
    new_valid = bcrypt.checkpw(password.encode('utf-8'), new_hash.encode('utf-8'))
    print(f"New hash test: {'✅ Valid' if new_valid else '❌ Invalid'}")
    
    print(f"\n🚀 Recommendation:")
    if old_valid:
        print("✅ Use the old Railway hash - it works!")
        print(f"   Hash: {old_hash}")
    elif new_valid:
        print("✅ Use the new hash - it works!")
        print(f"   Hash: {new_hash}")
    else:
        print("❌ Neither hash works - need to generate new one")
        print(f"   New hash: {hash_str}")

if __name__ == "__main__":
    check_bcrypt_version() 