@echo off
REM === Activate virtual environment ===
call backend\venv\Scripts\activate.bat

REM === Kill previous servers (if needed manually) ===
REM taskkill /F /IM uvicorn.exe >nul 2>&1

REM === Start FastAPI backend ===
echo Starting FastAPI (main.py) on port 8000...
start "FastAPI" cmd /k "uvicorn main:app --port 8000 --reload"

REM === Start MCP Server ===
echo Starting MCP Server on port 8001...
start "MCP Server" cmd /k "uvicorn mcp_server:app --port 8001 --reload"

REM === Done ===
echo.
echo ✅ Both FastAPI and MCP Server launched in new terminals.
echo Make sure your .env is set correctly.