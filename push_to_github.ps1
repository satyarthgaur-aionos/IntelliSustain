Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GitHub Push Script for IntelliSustain" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Checking if git is initialized..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    Write-Host "❌ Git repository not found!" -ForegroundColor Red
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository found" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 2: Adding remote origin..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin https://github.com/satyarthgaur-aionos/IntelliSustain.git
Write-Host "✅ Remote origin set to: https://github.com/satyarthgaur-aionos/IntelliSustain.git" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Adding all files to git..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "Step 4: Committing changes..." -ForegroundColor Yellow
git commit -m "Initial commit: Inferrix AI Agent Demo with Railway deployment setup"

Write-Host ""
Write-Host "Step 5: Pushing to GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✅ Push Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your code has been pushed to:" -ForegroundColor White
Write-Host "https://github.com/satyarthgaur-aionos/IntelliSustain" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Go to https://railway.app" -ForegroundColor White
Write-Host "2. Click 'New Project'" -ForegroundColor White
Write-Host "3. Select 'Deploy from GitHub repo'" -ForegroundColor White
Write-Host "4. Choose: satyarthgaur-aionos/IntelliSustain" -ForegroundColor White
Write-Host "5. Railway will auto-detect and deploy your services" -ForegroundColor White
Write-Host ""
Write-Host "Environment Variables to set in Railway:" -ForegroundColor Yellow
Write-Host "- INFERRIX_API_TOKEN=your_token" -ForegroundColor White
Write-Host "- OPENAI_API_KEY=your_key" -ForegroundColor White
Write-Host "- GOOGLE_API_KEY=your_key" -ForegroundColor White
Write-Host "- JWT_SECRET_KEY=your_secret" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to continue..." 