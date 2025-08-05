@echo off
echo ========================================
echo   Fix Encoding Issues and Deploy
echo ========================================
echo.

echo Step 1: Adding all files with encoding fixes...
git add -A

echo.
echo Step 2: Committing encoding fixes...
git commit -m "Fix UTF-8 encoding issues in Python files"

echo.
echo Step 3: Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo   ✅ Encoding Issues Fixed!
echo ========================================
echo.
echo The encoding problems have been resolved.
echo.
echo Now redeploy on Railway:
echo 1. Go to your Railway project
echo 2. Click "Deploy" or "Redeploy"
echo 3. The build should now succeed
echo.
echo If still failing:
echo 1. Delete the current Railway project
echo 2. Create new project from GitHub repo
echo 3. Railway will now build successfully
echo.
pause 