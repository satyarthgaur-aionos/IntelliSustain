@echo off
echo ========================================
echo   Fix Git Conflict - Force Push Solution
echo ========================================
echo.

echo Step 1: Pulling remote changes first...
git pull origin main --allow-unrelated-histories

echo.
echo Step 2: Adding all files including the new structure...
git add -A

echo.
echo Step 3: Committing the Railway structure fix...
git commit -m "Fix Railway structure: add main.py to root directory"

echo.
echo Step 4: Force pushing to GitHub...
git push -f origin main

echo.
echo ========================================
echo   ✅ Git Conflict Fixed!
echo ========================================
echo.
echo Your code has been pushed to GitHub with the Railway structure fix.
echo.
echo Now create new Railway project:
echo 1. Go to: https://railway.app
echo 2. Click "New Project" ^> "Deploy from GitHub repo"
echo 3. Select: satyarthgaur-aionos/IntelliSustain
echo 4. Railway will now detect Python app in root directory
echo.
echo Environment Variables to add:
echo - INFERRIX_API_TOKEN=your_token
echo - OPENAI_API_KEY=your_key
echo - GOOGLE_API_KEY=your_key
echo - JWT_SECRET_KEY=your_secret
echo.
pause 