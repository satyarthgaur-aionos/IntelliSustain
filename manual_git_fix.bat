@echo off
echo ========================================
echo   Manual Git Fix - Step by Step
echo ========================================
echo.

echo Step 1: Reset git and start fresh...
git reset --hard HEAD
git clean -fd

echo.
echo Step 2: Add all files explicitly...
git add backend/
git add frontend/
git add *.md
git add *.json
git add *.toml
git add *.bat
git add *.ps1
git add *.sh

echo.
echo Step 3: Check what's staged...
git status

echo.
echo Step 4: Commit changes...
git commit -m "Add complete source code for Railway deployment"

echo.
echo Step 5: Pull and merge remote changes...
git pull origin main --allow-unrelated-histories

echo.
echo Step 6: Push to GitHub...
git push origin main

echo.
echo ========================================
echo   ✅ Manual Fix Complete!
echo ========================================
echo.
echo Check GitHub now:
echo https://github.com/satyarthgaur-aionos/IntelliSustain
echo.
echo You should see backend/ and frontend/ folders.
echo.
pause 