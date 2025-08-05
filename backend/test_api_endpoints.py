#!/usr/bin/env python3
"""
Test script for new API endpoints: Assets, Entity Views, and Notifications
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools import get_assets_inferrix, get_entity_views_inferrix, get_notifications_inferrix

def test_api_endpoints():
    """Test the new API endpoints directly"""
    
    print("🧪 Testing New API Endpoints\n")
    
    token = os.getenv('JWT_TOKEN')
    if not token:
        print("❌ No JWT token found in environment variables")
        return
    
    try:
        print("Testing Assets API...")
        assets = get_assets_inferrix(token)
        print(f"✅ Assets API: {len(assets)} assets found")
        
        print("\nTesting Entity Views API...")
        entity_views = get_entity_views_inferrix(token)
        print(f"✅ Entity Views API: {len(entity_views)} entity views found")
        
        print("\nTesting Notifications API...")
        notifications = get_notifications_inferrix(token)
        print(f"✅ Notifications API: {len(notifications)} notifications found")
        
        print("\n🎉 All API endpoints are working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing API endpoints: {str(e)}")

if __name__ == "__main__":
    test_api_endpoints() 