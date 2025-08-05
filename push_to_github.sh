#!/bin/bash

echo "========================================"
echo "  GitHub Push Script for IntelliSustain"
echo "========================================"
echo

echo "Step 1: Checking if git is initialized..."
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found!"
    echo "Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository found"
fi

echo
echo "Step 2: Adding remote origin..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/satyarthgaur-aionos/IntelliSustain.git
echo "✅ Remote origin set to: https://github.com/satyarthgaur-aionos/IntelliSustain.git"

echo
echo "Step 3: Adding all files to git..."
git add .

echo
echo "Step 4: Committing changes..."
git commit -m "Initial commit: Inferrix AI Agent Demo with Railway deployment setup"

echo
echo "Step 5: Pushing to GitHub..."
git branch -M main
git push -u origin main

echo
echo "========================================"
echo "  ✅ Push Complete!"
echo "========================================"
echo
echo "Your code has been pushed to:"
echo "https://github.com/satyarthgaur-aionos/IntelliSustain"
echo
echo "Next Steps:"
echo "1. Go to https://railway.app"
echo "2. Click 'New Project'"
echo "3. Select 'Deploy from GitHub repo'"
echo "4. Choose: satyarthgaur-aionos/IntelliSustain"
echo "5. Railway will auto-detect and deploy your services"
echo
echo "Environment Variables to set in Railway:"
echo "- INFERRIX_API_TOKEN=your_token"
echo "- OPENAI_API_KEY=your_key"
echo "- GOOGLE_API_KEY=your_key"
echo "- JWT_SECRET_KEY=your_secret"
echo

read -p "Press Enter to continue..." 