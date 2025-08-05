@echo off
echo ========================================
echo   Fix Railway Deployment
echo ========================================
echo.

echo Step 1: Checking current git status...
git status

echo.
echo Step 2: Adding all files including backend and frontend...
git add backend/
git add frontend/
git add *.md
git add *.json
git add *.toml
git add *.bat
git add *.ps1
git add *.sh

echo.
echo Step 3: Checking what files are staged...
git status --porcelain

echo.
echo Step 4: Committing all source code...
git commit -m "Add complete source code: backend, frontend, and deployment configs"

echo.
echo Step 5: Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo   ✅ Fixed Deployment Structure
echo ========================================
echo.
echo Your complete source code has been pushed to:
echo https://github.com/satyarthgaur-aionos/IntelliSustain
echo.
echo Now redeploy on Railway:
echo 1. Go to your Railway project
echo 2. Click "Deploy" or "Redeploy"
echo 3. Railway should now detect the backend/ directory
echo.
echo If still failing, try:
echo 1. Delete the Railway project
echo 2. Create new project
echo 3. Select your GitHub repo again
echo.
pause 