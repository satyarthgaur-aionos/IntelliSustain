@echo off
echo ========================================
echo   Fix Render Compatibility - Stable Versions
echo ========================================
echo.

echo Step 1: Adding the updated requirements.txt and runtime.txt...
git add backend/requirements.txt
git add backend/runtime.txt

echo.
echo Step 2: Committing the compatibility fixes...
git commit -m "Fix Render compatibility: use stable package versions without Rust dependencies"

echo.
echo Step 3: Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo   ✅ Render Compatibility Fix Applied!
echo ========================================
echo.
echo Updated to stable versions:
echo - Python 3.9.18
echo - pydantic 1.10.8 (no Rust dependencies)
echo - fastapi 0.95.2
echo - uvicorn 0.22.0
echo.
echo Now redeploy on Render:
echo 1. Go to your Render dashboard
echo 2. Click "Manual Deploy" on your backend service
echo 3. The build should now succeed without Rust errors
echo.
echo If still failing:
echo 1. Delete the Render service
echo 2. Create new Web Service
echo 3. Connect to GitHub repo again
echo 4. Build should succeed with stable versions
echo.
pause 