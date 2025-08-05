@echo off
echo 🔁 Launching Inferrix AI Agent Fullstack Demo...

REM --- Start Backend (FastAPI) ---
start cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --port 8000 --reload"

REM --- Start MCP Server ---
start cmd /k "cd backend && venv\Scripts\activate && uvicorn mcp_server:app --port 8001 --reload"

REM --- Start Frontend (React) ---
start cmd /k "cd frontend && npm run dev"

echo ✅ All services started in separate terminals.
pause