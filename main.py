import dotenv
import requests
import os
import time
import sys
from collections import defaultdict
from typing import Optional
dotenv.load_dotenv()

# Add backend directory to Python path
sys.path.append('backend')

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from enhanced_agentic_agent import get_enhanced_agentic_agent
from auth_db import get_current_user

# Import database components
from database import engine, Base
from user_model import User

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inferrix AI Agent API", version="1.0.0")

# Mount static files (built React app)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")

# Rate limiting
request_counts = defaultdict(list)
RATE_LIMIT_WINDOW = 60  # 1 minute
RATE_LIMIT_MAX_REQUESTS = 30  # 30 requests per minute

def check_rate_limit(client_ip: str):
    """Simple rate limiting based on IP address"""
    now = time.time()
    # Remove old requests outside the window
    request_counts[client_ip] = [req_time for req_time in request_counts[client_ip] 
                                if now - req_time < RATE_LIMIT_WINDOW]
    
    if len(request_counts[client_ip]) >= RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")
    
    request_counts[client_ip].append(now)

# Exception logging middleware for debugging
import traceback
@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        # Rate limiting
        client_ip = request.client.host if request.client else "unknown"
        check_rate_limit(client_ip)
        
        return await call_next(request)
    except HTTPException:
        # Re-raise HTTP exceptions (including rate limit)
        raise
    except Exception as e:
        print("Exception caught in middleware:")
        traceback.print_exc()
        raise e

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Models ===
class User(BaseModel):
    email: str
    password: str

class Prompt(BaseModel):
    query: str
    user: str  # Remove default, require explicit user
    device: Optional[str] = None  # Optional device field

# === Global Error Handler ===
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the error here if needed
    print(f"Global exception handler: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred. Please try again later.", "code": "INTERNAL_ERROR"}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "code": f"HTTP_{exc.status_code}"}
    )

# === Frontend Routes ===
@app.get("/")
async def serve_frontend():
    """Serve the React frontend"""
    try:
        return FileResponse("static/index.html")
    except Exception as e:
        # Fallback to API info if frontend not built
        return {
            "message": "Inferrix AI Agent Backend is Running",
            "frontend": "Not built or not found",
            "api_docs": "/docs",
            "health": "/health"
        }

# === API Endpoints ===
@app.post("/login")
def login(user: User):
    """Authenticate user and return JWT token"""
    from auth_db import verify_user, create_access_token
    db_user = verify_user(user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/chat")
def chat(prompt: Prompt, current_user=Depends(get_current_user)):
    """Process chat query through AI agent using agentic approach"""
    try:
        if not prompt.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Debug logging for POST body
        print(f"[DEBUG] POST body received:")
        print(f"  - query: '{prompt.query}'")
        print(f"  - user: '{prompt.user}'")
        print(f"  - device: '{prompt.device}'")
        
        # Use the enhanced agentic agent
        # Pass device information if available
        if prompt.device:
            # If device is selected, modify the query to include device context
            device_context = f" (Device ID: {prompt.device})"
            enhanced_query = prompt.query + device_context
            print(f"[DEBUG] Enhanced query with device: '{enhanced_query}'")
            agent = get_enhanced_agentic_agent()
            response = agent.process_query(enhanced_query, prompt.user, prompt.device)
        else:
            print(f"[DEBUG] No device selected, using original query")
            agent = get_enhanced_agentic_agent()
            response = agent.process_query(prompt.query, prompt.user)
        
        # Always return a string
        if not response:
            response = "No data found or unable to answer your query."
        
        print(f"[DEBUG] Final response: {response[:100]}...")
        
        return {
            "response": response, 
            "tool": "enhanced_agentic_agent",  # Indicate this is using the enhanced agentic approach
            "timestamp": time.time()
        }
    except Exception as e:
        print(f"Chat error: {e}")
        return JSONResponse(
            content={"error": str(e), "code": "CHAT_ERROR"}, 
            status_code=500
        )

@app.post("/chat/enhanced")
def enhanced_chat(prompt: Prompt, current_user=Depends(get_current_user)):
    """Process chat query through enhanced AI agent with AI magic features"""
    try:
        if not prompt.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Debug logging for POST body
        print(f"[DEBUG] Enhanced chat - POST body received:")
        print(f"  - query: '{prompt.query}'")
        print(f"  - user: '{prompt.user}'")
        print(f"  - device: '{prompt.device}'")
        
        # Use the enhanced agentic agent with AI magic features
        agent = get_enhanced_agentic_agent()
        response = agent.process_query(prompt.query, prompt.user, prompt.device or "")
        
        # Always return a string
        if not response:
            response = "No data found or unable to answer your query."
        
        print(f"[DEBUG] Enhanced chat - Final response: {response[:100]}...")
        
        return {
            "response": response, 
            "tool": "enhanced_agentic_agent",  # Indicate this is using the enhanced agentic approach
            "timestamp": time.time(),
            "features": [
                "conversational_memory",
                "multi_device_operations", 
                "proactive_insights",
                "natural_language_control",
                "rich_responses",
                "personalization",
                "self_healing",
                "smart_notifications",
                "multi_language_support"
            ]
        }
    except Exception as e:
        print(f"Enhanced chat error: {e}")
        return JSONResponse(
            content={"error": str(e), "code": "ENHANCED_CHAT_ERROR"}, 
            status_code=500
        )

@app.get("/inferrix/alarms")
def get_alarms(current_user=Depends(get_current_user)):
    """Get alarms from Inferrix API"""
    try:
        jwt_token = os.getenv("INFERRIX_API_TOKEN")
        if not jwt_token:
            raise HTTPException(status_code=500, detail="Inferrix API token not configured")
        
        headers = {"X-Authorization": f"Bearer {jwt_token}"}
        response = requests.get(
            "https://cloud.inferrix.com/api/alarms",
            headers=headers,
            params={"page": 0, "pageSize": 100}
        )
        response.raise_for_status()
        
        return {"data": response.json().get("data", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch alarms: {str(e)}")

@app.get("/inferrix/devices")
def get_devices(current_user=Depends(get_current_user)):
    """Get devices from Inferrix API"""
    try:
        jwt_token = os.getenv("INFERRIX_API_TOKEN")
        if not jwt_token:
            raise HTTPException(status_code=500, detail="Inferrix API token not configured")
        
        headers = {"X-Authorization": f"Bearer {jwt_token}"}
        response = requests.get(
            "https://cloud.inferrix.com/api/user/devices",
            headers=headers,
            params={"page": 0, "pageSize": 100}
        )
        response.raise_for_status()
        
        return {"devices": response.json().get("data", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch devices: {str(e)}")

INFERRIX_BASE_URL = "https://cloud.inferrix.com/api"
INFERRIX_API_TOKEN = os.getenv("INFERRIX_API_TOKEN", "").strip()

def inferrix_api_status():
    """Check if Inferrix API is reachable"""
    url = f"{INFERRIX_BASE_URL}/alarms"
    headers = {
        "X-Authorization": f"Bearer {INFERRIX_API_TOKEN}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json().get("data", [])
        return {"status": "Inferrix API reachable", "alarms_count": len(data)}
    except Exception as e:
        return {"status": "Inferrix API unreachable", "error": str(e)}

@app.get("/api")
def api_root():
    """API root endpoint"""
    status = inferrix_api_status()
    return {
        "message": "Inferrix AI Agent API",
        "status": status,
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    try:
        # Simple health check - just verify the app is running
        return {
            "status": "✅ FastAPI server is running", 
            "timestamp": time.time(),
            "version": "1.0.0"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={
                "status": "❌ Server error", 
                "error": str(e),
                "timestamp": time.time()
            }
        )

@app.get("/api/info")
def api_info():
    """Dynamic API information endpoint"""
    return {
        "name": "Inferrix AI Agent",
        "version": "2.0.0",
        "description": "Intelligent building management AI agent with agentic capabilities",
        "capabilities": [
            "Predictive Maintenance Analysis",
            "ESG Carbon Analysis", 
            "Cleaning Optimization",
            "Root Cause Analysis",
            "Energy Optimization Control",
            "Comfort Adjustment Control",
            "Device Management",
            "Alarm Management",
            "Telemetry Analysis"
        ],
        "supported_queries": [
            "Are any HVAC or lighting systems likely to fail in the next 7 days?",
            "How much carbon emissions did we reduce this week? Are we on track for our Q3 target?",
            "What are the least used restrooms on the 3rd floor today?",
            "Why is the east wing warm and noisy today?",
            "Turn off HVAC and dim lights in the east wing on Saturday and Sunday",
            "Lower the temperature by 2 degrees in Conference Room B for the next 3 hours"
        ]
    }

@app.get("/debug/devices")
def debug_devices(current_user=Depends(get_current_user)):
    """Debug endpoint to show available devices and their IDs"""
    try:
        jwt_token = os.getenv("INFERRIX_API_TOKEN")
        if not jwt_token:
            raise HTTPException(status_code=500, detail="Inferrix API token not configured")
        
        headers = {"X-Authorization": f"Bearer {jwt_token}"}
        response = requests.get(
            "https://cloud.inferrix.com/api/user/devices",
            headers=headers,
            params={"page": 0, "pageSize": 50}
        )
        response.raise_for_status()
        
        devices = response.json().get("data", [])
        device_info = []
        
        for device in devices:
            device_id = device.get('id', {})
            if isinstance(device_id, dict):
                device_id = device_id.get('id', 'Unknown')
            
            device_info.append({
                "name": device.get('name', 'Unknown'),
                "id": device_id,
                "type": device.get('type', 'Unknown'),
                "status": device.get('status', 'Unknown')
            })
        
        return {
            "total_devices": len(device_info),
            "devices": device_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch devices: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

