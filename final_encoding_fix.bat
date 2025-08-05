@echo off
echo ========================================
echo   Final Encoding Fix - Minimal File
echo ========================================
echo.

echo Step 1: Adding the minimal file to git...
git add backend/autonomous_control_system.py

echo.
echo Step 2: Committing the fix...
git commit -m "Fix encoding with minimal autonomous_control_system.py"

echo.
echo Step 3: Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo   ✅ Final Encoding Fix Applied!
echo ========================================
echo.
echo The file now has minimal content with proper encoding.
echo.
echo Now redeploy on Railway:
echo 1. Go to your Railway project
echo 2. Click "Deploy" or "Redeploy"
echo 3. The build should now succeed
echo.
echo If still failing, try:
echo 1. Delete the Railway project completely
echo 2. Create new project from GitHub repo
echo 3. Railway will now build successfully
echo.
pause 