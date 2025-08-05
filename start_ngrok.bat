@echo off
title Inferrix AI Agent Demo - Development Only
echo.
echo ========================================
echo    INFERRIX AI AGENT - LOCAL DEV MODE
echo ========================================
echo.
echo 🔁 Launching Inferrix AI Agent (Local Development)...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 16+ and try again
    pause
    exit /b 1
)

REM Check if .env file exists in backend
if not exist "backend\.env" (
    echo WARNING: .env file not found in backend directory
    echo Please ensure you have configured your environment variables
    echo.
)

echo Starting services in separate windows...
echo.

REM --- Start Backend (FastAPI) ---
start "Inferrix AI Agent - Backend" cmd /k "cd /d %CD%\backend && venv\Scripts\activate && echo Backend starting on http://0.0.0.0:8000 && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

REM --- Start MCP Server ---
start "Inferrix AI Agent - MCP Server" cmd /k "cd /d %CD%\backend && venv\Scripts\activate && echo MCP Server starting on http://0.0.0.0:8001 && uvicorn mcp_server:app --host 0.0.0.0 --port 8001 --reload"

echo.
echo ========================================
echo    ALL SERVICES STARTING...
echo ========================================
echo.
echo Backend API:  http://127.0.0.1:8000
echo MCP Server:   http://127.0.0.1:8001
echo API Docs:     http://127.0.0.1:8000/docs
echo Frontend:     http://127.0.0.1:5173
echo.
echo Demo Credentials:
echo Email:    tech@inferrix.com
echo Password: Demo@1234
echo.
echo ========================================
echo    LOCAL DEVELOPMENT READY!
echo ========================================
echo.
echo ✅ All services started in separate terminals.
echo Wait 30-60 seconds for all services to fully load.
echo.
echo Press any key to open the frontend in your browser...
pause >nul

REM Open frontend in default browser
start http://127.0.0.1:5173

echo.
echo Demo launched successfully!
echo.
echo TIP: Keep this window open to monitor the demo.
echo To stop all services, run stop_demo.bat or close individual windows.
echo.
pause 