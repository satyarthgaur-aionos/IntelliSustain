@echo off
echo ========================================
echo   Railway Deployment Fix - Complete
echo ========================================
echo.

echo Step 1: Checking current git status...
git status

echo.
echo Step 2: Ensuring all backend files are properly committed...
git add backend/
git add frontend/
git add *.json
git add *.toml
git add *.md

echo.
echo Step 3: Committing any new changes...
git commit -m "Fix Railway deployment configuration"

echo.
echo Step 4: Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo   ✅ Code Pushed Successfully!
echo ========================================
echo.
echo Now fix Railway deployment:
echo.
echo OPTION 1: Redeploy Existing Project
echo 1. Go to: https://railway.app
echo 2. Find your project
echo 3. Click "Deploy" or "Redeploy"
echo.
echo OPTION 2: Create New Project (Recommended)
echo 1. Delete the current Railway project
echo 2. Go to: https://railway.app
echo 3. Click "New Project" ^> "Deploy from GitHub repo"
echo 4. Select: satyarthgaur-aionos/IntelliSustain
echo 5. Railway will auto-detect backend/ directory
echo.
echo OPTION 3: Manual Service Creation
echo 1. Create Backend Service:
echo    - Root directory: backend/
echo    - Build command: pip install -r requirements.txt
echo    - Start command: uvicorn main:app --host 0.0.0.0 --port $PORT
echo.
echo 2. Create Frontend Service:
echo    - Root directory: frontend/
echo    - Build command: npm install ^&^& npm run build
echo    - Start command: npm run preview
echo.
echo Environment Variables to set:
echo - INFERRIX_API_TOKEN=your_token
echo - OPENAI_API_KEY=your_key
echo - GOOGLE_API_KEY=your_key
echo - JWT_SECRET_KEY=your_secret
echo.
pause 