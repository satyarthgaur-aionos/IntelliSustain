@echo off
echo 🚀 Inferrix AI Agent - Complete Deployment
echo ============================================

echo.
echo 📋 This script will:
echo   1. Build the React frontend
echo   2. Setup backend dependencies
echo   3. Create deployment files
echo   4. Prepare for Railway deployment
echo.

echo 🔍 Checking requirements...
python deploy_complete.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Deployment setup completed successfully!
    echo.
    echo 📋 Next steps:
    echo   1. Run: git add .
    echo   2. Run: git commit -m "Complete deployment setup"
    echo   3. Run: git push origin main
    echo   4. Deploy to Railway
    echo   5. Add environment variables in Railway dashboard
    echo.
    echo 🎉 Your app will be ready at the Railway URL!
) else (
    echo.
    echo ❌ Deployment setup failed!
    echo Please check the errors above and try again.
)

pause 