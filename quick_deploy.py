#!/usr/bin/env python3
"""
Quick deployment script for sharing your application
Uses localtunnel for immediate sharing without complex setup
"""

import subprocess
import time
import os
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_port(port):
    """Check if a port is in use"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

def main():
    print("🚀 Quick Deployment Setup")
    print("=" * 50)
    
    # Check if Node.js is installed
    success, stdout, stderr = run_command("node --version")
    if not success:
        print("❌ Node.js not found. Please install Node.js first.")
        print("Download from: https://nodejs.org/")
        return
    
    # Check if Python is installed
    success, stdout, stderr = run_command("python --version")
    if not success:
        print("❌ Python not found. Please install Python first.")
        return
    
    # Install localtunnel globally
    print("📦 Installing localtunnel...")
    success, stdout, stderr = run_command("npm install -g localtunnel")
    if not success:
        print("❌ Failed to install localtunnel")
        print("Error:", stderr)
        return
    
    # Check if required ports are available
    ports = [8000, 8001, 5173]
    for port in ports:
        if check_port(port):
            print(f"⚠️  Port {port} is already in use. Please stop any services using this port.")
            return
    
    # Start the backend server
    print("🔧 Starting FastAPI backend...")
    backend_process = subprocess.Popen(
        ["python", "main.py"],
        cwd="backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start the MCP server
    print("🔧 Starting MCP server...")
    mcp_process = subprocess.Popen(
        ["python", "mcp_server.py"],
        cwd="backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait a moment for MCP to start
    time.sleep(3)
    
    # Start the frontend
    print("🔧 Starting Vite frontend...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd="frontend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for frontend to start
    time.sleep(5)
    
    print("🌐 Creating tunnels...")
    
    # Create tunnels for each service
    backend_tunnel = subprocess.Popen(
        ["lt", "--port", "8000", "--subdomain", "inferrix-api"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    mcp_tunnel = subprocess.Popen(
        ["lt", "--port", "8001", "--subdomain", "inferrix-mcp"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    frontend_tunnel = subprocess.Popen(
        ["lt", "--port", "5173", "--subdomain", "inferrix-app"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for tunnels to be created
    time.sleep(10)
    
    print("\n" + "=" * 50)
    print("🎉 Your application is now accessible!")
    print("=" * 50)
    print("📱 Share these URLs with your team:")
    print(f"Frontend: https://inferrix-app.loca.lt")
    print(f"Backend API: https://inferrix-api.loca.lt")
    print(f"MCP Server: https://inferrix-mcp.loca.lt")
    print("\n⚠️  Note: These URLs will change each time you restart the script")
    print("💡 For permanent URLs, use Railway or Render deployment")
    print("\nPress Ctrl+C to stop all services")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping all services...")
        backend_process.terminate()
        mcp_process.terminate()
        frontend_process.terminate()
        backend_tunnel.terminate()
        mcp_tunnel.terminate()
        frontend_tunnel.terminate()
        print("✅ All services stopped")

if __name__ == "__main__":
    main() 