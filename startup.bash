# 🐍 Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate       # (or source venv/bin/activate on Mac/Linux)
pip install -r requirements.txt

# 🧠 Run MCP Server
uvicorn mcp_server:app --port 8001 --reload

# 🚀 Run FastAPI backend
uvicorn main:app --reload

# ⚛️ Frontend Setup
cd ../frontend
npm install
npm run dev