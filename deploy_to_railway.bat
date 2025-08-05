@echo off
echo ========================================
echo   Railway Deployment Helper Script
echo ========================================
echo.

echo Step 1: Checking if git is initialized...
if not exist ".git" (
    echo ❌ Git repository not found!
    echo Please run: git init
    echo Then: git add . && git commit -m "Initial commit"
    pause
    exit /b 1
)

echo ✅ Git repository found
echo.

echo Step 2: Checking if code is committed...
git status --porcelain
if %errorlevel% neq 0 (
    echo ❌ Please commit your changes first:
    echo git add .
    echo git commit -m "Ready for Railway deployment"
    pause
    exit /b 1
)

echo ✅ Code is committed
echo.

echo Step 3: Pushing to GitHub...
echo Please ensure your code is pushed to GitHub:
echo git push origin main
echo.

echo Step 4: Deploy to Railway
echo.
echo 📋 Next Steps:
echo 1. Go to https://railway.app
echo 2. Click "New Project"
echo 3. Select "Deploy from GitHub repo"
echo 4. Choose your repository
echo 5. Railway will automatically detect and deploy your services
echo.

echo 📝 Environment Variables to set in Railway:
echo.
echo Backend Service:
echo - INFERRIX_API_TOKEN=your_token
echo - OPENAI_API_KEY=your_key
echo - GOOGLE_API_KEY=your_key
echo - JWT_SECRET_KEY=your_secret
echo.
echo Frontend Service:
echo - VITE_API_URL=https://your-backend-url.railway.app
echo.

echo 🚀 After deployment, share the frontend URL with your team!
echo.

pause 