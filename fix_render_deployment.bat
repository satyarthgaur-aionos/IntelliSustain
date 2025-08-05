@echo off
echo ========================================
echo   Fix Render Deployment Issues
echo ========================================
echo.

echo Step 1: Adding the updated requirements.txt...
git add backend/requirements.txt

echo.
echo Step 2: Committing the fix...
git commit -m "Fix Render deployment: update requirements.txt for compatibility"

echo.
echo Step 3: Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo   ✅ Render Deployment Fix Applied!
echo ========================================
echo.
echo The requirements.txt has been updated for better Render compatibility.
echo.
echo Now redeploy on Render:
echo 1. Go to your Render dashboard
echo 2. Click "Manual Deploy" on your backend service
echo 3. The build should now succeed
echo.
echo If still failing:
echo 1. Delete the Render service
echo 2. Create new Web Service
echo 3. Connect to GitHub repo again
echo 4. Build should succeed with updated requirements
echo.
pause 