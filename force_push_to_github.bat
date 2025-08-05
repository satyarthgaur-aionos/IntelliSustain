@echo off
echo ========================================
echo   Force Push to GitHub - Fix All Issues
echo ========================================
echo.

echo Step 1: Checking current git status...
git status

echo.
echo Step 2: Adding ALL files to git (including backend and frontend)...
git add -A

echo.
echo Step 3: Checking what files are staged...
git status --porcelain

echo.
echo Step 4: Committing all source code...
git commit -m "Add complete source code: backend, frontend, and deployment configs"

echo.
echo Step 5: Pulling remote changes first...
git pull origin main --allow-unrelated-histories

echo.
echo Step 6: Force pushing to GitHub...
git push -f origin main

echo.
echo ========================================
echo   ✅ Force Push Complete!
echo ========================================
echo.
echo Your complete source code has been pushed to:
echo https://github.com/satyarthgaur-aionos/IntelliSustain
echo.
echo Now check GitHub to verify you see:
echo - backend/ folder with Python files
echo - frontend/ folder with React files
echo.
echo Then redeploy on Railway:
echo 1. Go to your Railway project
echo 2. Click "Deploy" or "Redeploy"
echo 3. Railway should now detect the backend/ directory
echo.
pause 