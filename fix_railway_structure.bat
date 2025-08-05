@echo off
echo ========================================
echo   Fix Railway Structure - Complete Fix
echo ========================================
echo.

echo Step 1: Delete current Railway project...
echo Please go to https://railway.app and delete the current project
echo Then come back and press any key to continue...
pause

echo.
echo Step 2: Creating proper Railway structure...
echo Creating main.py in root directory for Railway detection...

copy backend\main.py main.py
copy backend\requirements.txt requirements.txt
copy backend\Procfile Procfile

echo.
echo Step 3: Adding all files to git...
git add main.py
git add requirements.txt
git add Procfile
git add backend/
git add frontend/

echo.
echo Step 4: Committing changes...
git commit -m "Fix Railway structure: move main.py to root for auto-detection"

echo.
echo Step 5: Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo   ✅ Railway Structure Fixed!
echo ========================================
echo.
echo Now create new Railway project:
echo 1. Go to: https://railway.app
echo 2. Click "New Project" ^> "Deploy from GitHub repo"
echo 3. Select: satyarthgaur-aionos/IntelliSustain
echo 4. Railway will now detect Python app in root directory
echo.
echo Environment Variables to add:
echo - INFERRIX_API_TOKEN=your_token
echo - OPENAI_API_KEY=your_key
echo - GOOGLE_API_KEY=your_key
echo - JWT_SECRET_KEY=your_secret
echo.
pause 