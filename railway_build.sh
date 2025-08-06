#!/bin/bash
set -e

echo "🚀 Railway Build Script for Inferrix AI Agent"
echo "=============================================="

# Check if we're in Railway environment
if [ -n "$RAILWAY_ENVIRONMENT" ]; then
    echo "✅ Running in Railway environment: $RAILWAY_ENVIRONMENT"
else
    echo "⚠️  Not running in Railway environment"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check if Node.js is available for frontend build
if command -v node &> /dev/null && command -v npm &> /dev/null; then
    echo "✅ Node.js and npm found, building frontend..."
    
    # Install frontend dependencies
    cd frontend
    npm install --production=false
    
    # Build frontend
    npm run build
    
    # Copy built files to static directory
    cd ..
    if [ -d "frontend/dist" ]; then
        mkdir -p static
        cp -r frontend/dist/* static/
        echo "✅ Frontend built and copied to static directory"
        echo "📄 Static files created in static/ directory"
    else
        echo "⚠️  Frontend build failed, continuing with backend only"
    fi
else
    echo "⚠️  Node.js not available, skipping frontend build"
    echo "   The app will work with API endpoints only"
fi

echo "🎉 Railway build completed successfully!"
echo "✅ Backend ready"
echo "✅ Frontend ready (if built)"
echo "✅ Ready to start FastAPI server" 