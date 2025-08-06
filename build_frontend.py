#!/usr/bin/env python3
"""
Build script for React frontend
"""

import os
import subprocess
import sys
import shutil

def build_frontend():
    """Build the React frontend for production"""
    print("🚀 Building React Frontend...")
    print("=" * 50)
    
    # Check if frontend directory exists
    if not os.path.exists("frontend"):
        print("❌ Frontend directory not found!")
        return False
    
    # Check if package.json exists
    if not os.path.exists("frontend/package.json"):
        print("❌ package.json not found in frontend directory!")
        return False
    
    try:
        # Install dependencies
        print("📦 Installing frontend dependencies...")
        result = subprocess.run(
            ["npm", "install"],
            cwd="frontend",
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
        
        print("✅ Dependencies installed successfully")
        
        # Build the frontend
        print("🔨 Building React app...")
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd="frontend",
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ Build failed: {result.stderr}")
            return False
        
        print("✅ React app built successfully")
        
        # Copy built files to static directory
        print("📁 Copying built files to static directory...")
        
        # Create static directory if it doesn't exist
        if not os.path.exists("static"):
            os.makedirs("static")
        
        # Copy dist contents to static
        if os.path.exists("frontend/dist"):
            # Remove existing static contents
            if os.path.exists("static"):
                shutil.rmtree("static")
            
            # Copy dist to static
            shutil.copytree("frontend/dist", "static")
            print("✅ Built files copied to static directory")
        else:
            print("❌ dist directory not found after build!")
            return False
        
        print("🎉 Frontend build completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during build: {e}")
        return False

def main():
    """Main build function"""
    print("🚀 Inferrix Frontend Build Script")
    print("=" * 50)
    
    # Check if Node.js is available
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Node.js not found! Please install Node.js first.")
            return False
        print(f"✅ Node.js version: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Node.js not found! Please install Node.js first.")
        return False
    
    # Check if npm is available
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ npm not found! Please install npm first.")
            return False
        print(f"✅ npm version: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ npm not found! Please install npm first.")
        return False
    
    # Build the frontend
    success = build_frontend()
    
    if success:
        print("\n🎉 Build completed successfully!")
        print("Static files are ready in the 'static' directory")
        print("The FastAPI server will serve these files automatically")
    else:
        print("\n❌ Build failed!")
    
    return success

if __name__ == "__main__":
    main() 