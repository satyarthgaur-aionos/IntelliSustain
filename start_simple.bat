@echo off
setlocal

REM Get the directory of this script
set SCRIPT_DIR=%~dp0

echo 🔁 Launching Inferrix AI Agent Demo...

REM Check if services are already running
netstat -an | findstr :8000 >nul
if not errorlevel 1 (
    echo WARNING: Port 8000 is already in use. Backend may already be running.
)

netstat -an | findstr :5173 >nul
if not errorlevel 1 (
    echo WARNING: Port 5173 is already in use. Frontend may already be running.
)

echo.
echo Starting services...

REM Start Backend
if exist "%SCRIPT_DIR%backend\venv" (
    start "Backend" cmd /k "cd /d %SCRIPT_DIR%backend && venv\Scripts\activate && echo Backend starting on http://localhost:8000 && uvicorn main:app --port 8000 --reload"
) else (
    echo ERROR: Virtual environment not found. Run start_demo.bat first.
    pause
    exit /b 1
)

REM Start MCP Server
start "MCP Server" cmd /k "cd /d %SCRIPT_DIR%backend && venv\Scripts\activate && echo MCP Server starting on http://localhost:8001 && uvicorn mcp_server:app --port 8001 --reload"

REM Start Frontend
if exist "%SCRIPT_DIR%frontend\node_modules" (
    start "Frontend" cmd /k "cd /d %SCRIPT_DIR%frontend && echo Frontend starting on http://localhost:5173 && npm run dev"
) else (
    echo ERROR: Node modules not found. Run start_demo.bat first.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    SERVICES STARTING...
echo ========================================
echo Backend:  http://localhost:8000
echo MCP Server: http://localhost:8001
echo Frontend: http://localhost:5173
echo.
echo Login: tech@inferrix.com / password123
echo.
echo ✅ All services started in separate terminals.
echo Opening browser in 3 seconds...
timeout /t 3 >nul
start http://localhost:5173

echo Demo started! Check the service windows for any errors.
pause 