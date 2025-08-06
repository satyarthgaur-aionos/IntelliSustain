#!/usr/bin/env python3
"""
Railway Deployment Status Checker
This script helps monitor the deployment status and provides guidance.
"""

import os
import sys
import time
from datetime import datetime

def print_status(message, status_type="INFO"):
    """Print a formatted status message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    colors = {
        "INFO": "\033[94m",    # Blue
        "SUCCESS": "\033[92m", # Green
        "WARNING": "\033[93m", # Yellow
        "ERROR": "\033[91m",   # Red
        "RESET": "\033[0m"     # Reset
    }
    
    print(f"{colors.get(status_type, colors['INFO'])}[{timestamp}] {status_type}: {message}{colors['RESET']}")

def check_railway_deployment():
    """Check Railway deployment status and provide guidance"""
    
    print_status("🚀 Railway Deployment Status Check", "INFO")
    print_status("=" * 50, "INFO")
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print_status("❌ main.py not found in current directory", "ERROR")
        print_status("Please run this script from the project root directory", "WARNING")
        return
    
    # Check key files
    key_files = [
        "main.py",
        "requirements.txt", 
        "Procfile",
        "runtime.txt",
        "static/index.html"
    ]
    
    print_status("📁 Checking key deployment files:", "INFO")
    for file in key_files:
        if os.path.exists(file):
            print_status(f"✅ {file} - Found", "SUCCESS")
        else:
            print_status(f"❌ {file} - Missing", "ERROR")
    
    print_status("=" * 50, "INFO")
    print_status("🔧 Deployment Configuration:", "INFO")
    
    # Check main.py configuration
    try:
        with open("main.py", "r") as f:
            content = f.read()
            if "sys.path.append('backend')" in content:
                print_status("✅ Python path configured correctly", "SUCCESS")
            else:
                print_status("⚠️  Python path configuration may be missing", "WARNING")
                
            if "StaticFiles" in content:
                print_status("✅ Static files mounting configured", "SUCCESS")
            else:
                print_status("⚠️  Static files mounting may be missing", "WARNING")
    except Exception as e:
        print_status(f"❌ Error reading main.py: {e}", "ERROR")
    
    # Check requirements.txt
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
            required_packages = ["fastapi", "uvicorn", "sqlalchemy", "psycopg2-binary"]
            for package in required_packages:
                if package in content:
                    print_status(f"✅ {package} - Included", "SUCCESS")
                else:
                    print_status(f"⚠️  {package} - May be missing", "WARNING")
    except Exception as e:
        print_status(f"❌ Error reading requirements.txt: {e}", "ERROR")
    
    print_status("=" * 50, "INFO")
    print_status("🌐 Railway Deployment Steps:", "INFO")
    print_status("1. ✅ Code pushed to GitHub", "SUCCESS")
    print_status("2. ✅ Railway connected to GitHub repository", "SUCCESS")
    print_status("3. 🔄 Railway should auto-deploy (check Railway dashboard)", "INFO")
    print_status("4. ⏳ Wait for build to complete (usually 2-5 minutes)", "INFO")
    print_status("5. 🔍 Check Railway logs for any errors", "INFO")
    
    print_status("=" * 50, "INFO")
    print_status("🔍 Troubleshooting Tips:", "INFO")
    print_status("• If deployment fails, check Railway logs", "INFO")
    print_status("• Ensure all environment variables are set in Railway", "INFO")
    print_status("• Verify DATABASE_URL is correctly configured", "INFO")
    print_status("• Check that static files are properly built", "INFO")
    
    print_status("=" * 50, "INFO")
    print_status("📱 Next Steps:", "INFO")
    print_status("1. Go to Railway dashboard", "INFO")
    print_status("2. Check if deployment is in progress", "INFO")
    print_status("3. Wait for build to complete", "INFO")
    print_status("4. Test the deployed URL", "INFO")
    print_status("5. Try logging in with: tech@intellisustain.com / Demo@1234", "INFO")

if __name__ == "__main__":
    check_railway_deployment() 