@echo off
echo ========================================
echo   Deploy to Render - Alternative Solution
echo ========================================
echo.

echo Step 1: Ensure code is pushed to GitHub...
git add -A
git commit -m "Prepare for Render deployment"
git push origin main

echo.
echo ========================================
echo   ✅ Code Ready for Render!
echo ========================================
echo.
echo Now deploy to Render:
echo.
echo STEP 1: Backend Deployment
echo 1. Go to: https://render.com
echo 2. Click "New +" ^> "Web Service"
echo 3. Connect to GitHub repo: satyarthgaur-aionos/IntelliSustain
echo 4. Set Root Directory: backend/
echo 5. Build Command: pip install -r requirements.txt
echo 6. Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
echo 7. Add Environment Variables:
echo    - INFERRIX_API_TOKEN=your_token
echo    - OPENAI_API_KEY=your_key
echo    - GOOGLE_API_KEY=your_key
echo    - JWT_SECRET_KEY=your_secret
echo.
echo STEP 2: Frontend Deployment
echo 1. Click "New +" ^> "Static Site"
echo 2. Connect to same GitHub repo
echo 3. Set Root Directory: frontend/
echo 4. Build Command: npm install ^&^& npm run build
echo 5. Publish Directory: dist
echo 6. Add Environment Variable:
echo    - VITE_API_URL=https://your-backend-service.onrender.com
echo.
echo Expected URLs:
echo - Backend: https://your-backend-service.onrender.com
echo - Frontend: https://your-frontend-service.onrender.com
echo.
pause 