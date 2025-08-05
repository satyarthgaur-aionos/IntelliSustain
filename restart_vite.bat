@echo off
echo Stopping all Vite processes...
taskkill /f /im node.exe 2>nul
taskkill /f /im npm.exe 2>nul

echo Waiting 3 seconds...
timeout /t 3 /nobreak > nul

echo Starting Vite with new configuration...
cd frontend
npm run dev

echo Vite restarted with new configuration!
pause 