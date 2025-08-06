#!/bin/bash
# Railway deployment script
# Builds frontend and starts FastAPI server

echo "🚀 Starting Railway deployment..."

# Install frontend dependencies and build
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
echo "🔨 Building React app..."
npm run build
cd ..

# Create static directory if it doesn't exist
mkdir -p static

# Copy built frontend to static directory
echo "📁 Copying built frontend to static directory..."
cp -r frontend/dist/* static/

# Setup database and create users
echo "🗄️ Setting up database..."
python setup_admin.py

# Migrate existing users
echo "🔄 Migrating users..."
python migrate_users.py

# Start FastAPI server
echo "🚀 Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port $PORT 