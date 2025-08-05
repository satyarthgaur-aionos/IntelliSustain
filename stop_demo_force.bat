@echo off
title Force Stopping Inferrix AI Agent Demo
echo.
echo ========================================
echo    FORCE STOPPING ALL SERVICES
echo ========================================
echo.

echo 🔴 FORCE STOPPING ALL DEMO SERVICES...

REM Kill ALL cmd windows that might be running our services
echo Force killing all command windows...
taskkill /f /im cmd.exe >nul 2>&1

REM Kill specific processes by name
echo Force killing uvicorn processes...
taskkill /f /im uvicorn.exe >nul 2>&1

echo Force killing node processes...
taskkill /f /im node.exe >nul 2>&1

echo Force killing python processes...
taskkill /f /im python.exe >nul 2>&1

REM Kill by port (force method)
echo Force killing processes on demo ports...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    echo Force killing PID %%a (port 8000)
    taskkill /f /pid %%a >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8001') do (
    echo Force killing PID %%a (port 8001)
    taskkill /f /pid %%a >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173') do (
    echo Force killing PID %%a (port 5173)
    taskkill /f /pid %%a >nul 2>&1
)

REM Wait longer for processes to terminate
echo Waiting for processes to terminate...
timeout /t 3 >nul

REM Final check - kill any remaining processes on our ports
echo Final cleanup...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8001') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173') do taskkill /f /pid %%a >nul 2>&1

echo.
echo ========================================
echo    FORCE STOP COMPLETE
echo ========================================
echo.
echo ⚠️  WARNING: This force stop killed ALL command windows
echo    and related processes. You may need to restart your terminal.
echo.
echo ✅ All demo services forcefully stopped
echo.
pause 