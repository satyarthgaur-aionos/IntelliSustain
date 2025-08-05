#!/bin/bash

# 🌐 MCP Server
cd backend || exit

# 🛑 Stop any running FastAPI or MCP
fuser -k 8000/tcp 2>/dev/null
fuser -k 8001/tcp 2>/dev/null

# ✅ Activate virtualenv if available
if [ -d "venv" ]; then
  source venv/bin/activate
else
  echo "[!] venv not found. Please run 'python -m venv venv' and install requirements."
  exit 1
fi

# 🧠 Start FastAPI backend (LangGraph)
nohup uvicorn main:app --port 8000 --host 0.0.0.0 > backend.log 2>&1 &

# 🔄 Start MCP Server
nohup uvicorn mcp_server:app --port 8001 --host 0.0.0.0 > mcp.log 2>&1 &

# ✅ Info
sleep 2
echo "✅ FastAPI backend running at http://localhost:8000"
echo "✅ MCP server running at http://localhost:8001"
echo "📜 Logs: backend.log, mcp.log"

# 🛑 Reminder
# To stop: kill $(lsof -t -i:8000 -i:8001)