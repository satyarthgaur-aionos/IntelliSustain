#!/usr/bin/env python3
"""
Complete deployment script for Inferrix AI Agent
Handles frontend build and backend setup
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if all required tools are available"""
    print("🔍 Checking deployment requirements...")
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False
    
    # Check npm
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm: {result.stdout.strip()}")
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False
    
    # Check Python
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Python: {result.stdout.strip()}")
        else:
            print("❌ Python not found")
            return False
    except FileNotFoundError:
        print("❌ Python not found")
        return False
    
    return True

def build_frontend():
    """Build the React frontend"""
    print("\n🚀 Building React Frontend...")
    print("=" * 50)
    
    if not os.path.exists("frontend"):
        print("❌ Frontend directory not found!")
        return False
    
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
            
            # List static files
            static_files = list(Path("static").rglob("*"))
            print(f"📄 Static files created: {len(static_files)} files")
            
        else:
            print("❌ dist directory not found after build!")
            return False
        
        print("🎉 Frontend build completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during build: {e}")
        return False

def setup_backend():
    """Setup backend dependencies and database"""
    print("\n🔧 Setting up Backend...")
    print("=" * 50)
    
    try:
        # Install Python dependencies
        print("📦 Installing Python dependencies...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Failed to install Python dependencies: {result.stderr}")
            return False
        
        print("✅ Python dependencies installed successfully")
        
        # Run database migration if needed
        print("🗄️  Setting up database...")
        if os.path.exists("migrate_table.py"):
            result = subprocess.run([sys.executable, "migrate_table.py"], 
                                 capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Database migration completed")
            else:
                print(f"⚠️  Database migration warning: {result.stderr}")
        
        print("✅ Backend setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during backend setup: {e}")
        return False

def create_deployment_files():
    """Create necessary deployment files"""
    print("\n📝 Creating deployment files...")
    print("=" * 50)
    
    # Create Procfile if it doesn't exist
    if not os.path.exists("Procfile"):
        with open("Procfile", "w") as f:
            f.write("web: uvicorn main:app --host 0.0.0.0 --port $PORT\n")
        print("✅ Procfile created")
    
    # Create runtime.txt if it doesn't exist
    if not os.path.exists("runtime.txt"):
        with open("runtime.txt", "w") as f:
            f.write("python-3.10.12\n")
        print("✅ runtime.txt created")
    
    # Create .gitignore if it doesn't exist
    if not os.path.exists(".gitignore"):
        with open(".gitignore", "w") as f:
            f.write("""# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
dist/
build/
static/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
""")
        print("✅ .gitignore created")
    
    print("✅ Deployment files created")

def main():
    """Main deployment function"""
    print("🚀 Inferrix AI Agent - Complete Deployment")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Deployment requirements not met!")
        print("Please install Node.js, npm, and Python")
        return False
    
    # Create deployment files
    create_deployment_files()
    
    # Build frontend
    if not build_frontend():
        print("\n❌ Frontend build failed!")
        return False
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed!")
        return False
    
    print("\n🎉 Complete deployment setup finished!")
    print("=" * 60)
    print("✅ Frontend built and ready")
    print("✅ Backend dependencies installed")
    print("✅ Database migration ready")
    print("✅ Static files in 'static' directory")
    print("✅ Ready for Railway deployment!")
    
    print("\n📋 Next steps:")
    print("1. Commit and push to GitHub")
    print("2. Deploy to Railway")
    print("3. Add environment variables in Railway dashboard")
    print("4. Your app will be available at the Railway URL")
    
    return True

if __name__ == "__main__":
    main() 