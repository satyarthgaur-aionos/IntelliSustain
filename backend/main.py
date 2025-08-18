import dotenv
import requests
import os
import time
from collections import defaultdict
from typing import Optional
dotenv.load_dotenv()

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from enhanced_agentic_agent import get_enhanced_agentic_agent
from auth_db import get_current_user

# Import database cleanup for one-time execution
from database_cleanup import cleanup_database

app = FastAPI(title="Inferrix AI Agent API", version="1.0.0")

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
    allow_origins=["*","https://d4c12a824b71.ngrok-free.app"],  # In production, restrict to your frontend domain
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

# === Endpoints ===
@app.post("/login")
def login(user: User):
    """Authenticate user and return JWT token + Inferrix token"""
    from auth_db import verify_user, create_access_token
    
    # First authenticate with local database
    db_user = verify_user(user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create local JWT token
    token = create_access_token({"sub": user.email})
    
    # Now authenticate with Inferrix API using the same credentials
    try:
        inferrix_login_data = {
            "username": user.email,  # Use username as per Postman working example
            "password": user.password  # Use the same password from local login
        }
        
        # Add more detailed headers and debugging
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "IntelliSustain-AI-Agent/2.0.0",
            "Accept": "application/json",
            "Connection": "keep-alive"
        }
        
        # Add Railway-specific headers if needed
        if os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("PORT") == "8080":
            headers["X-Platform"] = "Railway"
            headers["X-Environment"] = "production"
            print(f"[DEBUG] Detected Railway environment")
        
        print(f"[DEBUG] Calling Inferrix API with headers: {headers}")
        print(f"[DEBUG] Inferrix login data: {inferrix_login_data}")
        
        # Add retry logic for Railway
        max_retries = 3 if (os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("PORT") == "8080") else 1
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                print(f"[DEBUG] Attempt {retry_count + 1} of {max_retries} for Inferrix API call")
                inferrix_response = requests.post(
                    "https://cloud.inferrix.com/api/auth/login",
                    json=inferrix_login_data,
                    headers=headers,
                    timeout=30
                )
                break  # Success, exit retry loop
            except Exception as e:
                retry_count += 1
                print(f"[DEBUG] Attempt {retry_count} failed: {e}")
                if retry_count >= max_retries:
                    print(f"[DEBUG] All {max_retries} attempts failed")
                    raise e
                time.sleep(1)  # Wait before retry
        
        print(f"[DEBUG] Inferrix response status: {inferrix_response.status_code}")
        print(f"[DEBUG] Inferrix response headers: {dict(inferrix_response.headers)}")
        print(f"[DEBUG] Inferrix response text: {inferrix_response.text}")
        
        if inferrix_response.status_code == 200:
            inferrix_data = inferrix_response.json()
            inferrix_token = inferrix_data.get("token")  # Get "token" field as per Postman response
            
            if inferrix_token:
                print(f"[DEBUG] Successfully got Inferrix token: {inferrix_token[:50]}...")
                return {
                    "access_token": token, 
                    "token_type": "bearer",
                    "inferrix_token": inferrix_token  # Return as "inferrix_token" for frontend
                }
            else:
                print(f"[DEBUG] Warning: No token in Inferrix response. Full response: {inferrix_data}")
                return {"access_token": token, "token_type": "bearer"}
        else:
            print(f"[DEBUG] Warning: Inferrix login failed with status {inferrix_response.status_code}")
            print(f"[DEBUG] Error response: {inferrix_response.text}")
            return {"access_token": token, "token_type": "bearer"}
            
    except Exception as e:
        print(f"Warning: Error getting Inferrix refresh token: {e}")
        return {"access_token": token, "token_type": "bearer"}

@app.post("/chat")
def chat(prompt: Prompt, request: Request, current_user=Depends(get_current_user)):
    """Process chat query through AI agent using agentic approach"""
    try:
        if not prompt.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Minimal logging for POST body
        print(f"[DEBUG] Chat request from user: {prompt.user}")
        
        # Get the Inferrix token from the request headers
        inferrix_token = None
        auth_header = request.headers.get("X-Inferrix-Token")
        if auth_header:
            inferrix_token = auth_header
        
        # Use the enhanced agentic agent
        # Pass device information if available
        if prompt.device:
            # If device is selected, modify the query to include device context
            device_context = f" (Device ID: {prompt.device})"
            enhanced_query = prompt.query + device_context
            agent = get_enhanced_agentic_agent()
            response = agent.process_query(enhanced_query, prompt.user, prompt.device, inferrix_token)
        else:
            agent = get_enhanced_agentic_agent()
            response = agent.process_query(prompt.query, prompt.user, "", inferrix_token)
        
        # Always return a string
        if not response:
            response = "No data found or unable to answer your query."
        
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

# Removed complex refresh token endpoint - using simple token approach

@app.post("/chat/enhanced")
def enhanced_chat(prompt: Prompt, request: Request, current_user=Depends(get_current_user)):
    """Process chat query through enhanced AI agent with AI magic features"""
    try:
        if not prompt.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Minimal logging for enhanced chat
        print(f"[DEBUG] Enhanced chat request from user: {prompt.user}")
        
        # Get the Inferrix token from the request headers
        inferrix_token = None
        auth_header = request.headers.get("X-Inferrix-Token")
        if auth_header:
            inferrix_token = auth_header
        else:
            print("[DEBUG] Enhanced chat - No X-Inferrix-Token header found")
        
        # Use the enhanced agentic agent with AI magic features
        agent = get_enhanced_agentic_agent()
        # Set the API token on the agent
        agent._api_token = inferrix_token
        response = agent.process_query(prompt.query, prompt.user, prompt.device or "", inferrix_token)
        
        # Always return a string
        if not response:
            response = "No data found or unable to answer your query."
        
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
def get_alarms(request: Request, current_user=Depends(get_current_user)):
    """Get alarms from Inferrix API"""
    try:
        # Get the Inferrix token from the request headers
        inferrix_token = request.headers.get("X-Inferrix-Token")
        if not inferrix_token:
            raise HTTPException(status_code=401, detail="Inferrix API token required. Please log in again.")
        
        headers = {"X-Authorization": f"Bearer {inferrix_token}"}
        response = requests.get(
            "https://cloud.inferrix.com/api/v2/alarms",
            headers=headers,
            params={"pageSize": 100, "page": 0, "sortProperty": "createdTime", "sortOrder": "DESC", "statusList": "ACTIVE"}
        )
        response.raise_for_status()
        
        return {"data": response.json().get("data", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inferrix API call failed: {str(e)}")

@app.get("/inferrix/devices")
def get_devices(request: Request, current_user=Depends(get_current_user)):
    """Get devices from Inferrix API"""
    try:
        # Get the Inferrix token from the request headers
        inferrix_token = request.headers.get("X-Inferrix-Token")
        if not inferrix_token:
            raise HTTPException(status_code=401, detail="Inferrix API token required. Please log in again.")
        
        headers = {"X-Authorization": f"Bearer {inferrix_token}"}
        response = requests.get(
            "https://cloud.inferrix.com/api/user/devices",
            headers=headers,
            params={"page": 0, "pageSize": 100}
        )
        response.raise_for_status()
        
        return {"devices": response.json().get("data", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inferrix API call failed: {str(e)}")

INFERRIX_BASE_URL = "https://cloud.inferrix.com/api"

def inferrix_api_status():
    """Check if Inferrix API is reachable"""
    # Since we now use user-specific tokens, we can't check API status without a token
    return {"status": "Inferrix API requires user authentication", "note": "Use /inferrix/devices or /inferrix/alarms with user token"}

@app.get("/")
def root():
    """Root endpoint with API status"""
    status = inferrix_api_status()
    if status.get("status") == "Inferrix API reachable":
        return {
            "message": "Inferrix AI Agent Backend is Running",
            "status": status,
            "version": "1.0.0"
        }
    # If unreachable, show a friendly HTML message
    return HTMLResponse(
        f"""
        <html>
        <head><title>Inferrix AI Agent Backend</title></head>
        <body style='font-family:sans-serif; background:#f8fafc; color:#222; text-align:center; padding-top:60px;'>
            <h1>ðŸš¦ Inferrix AI Agent Backend is Running</h1>
            <p style='color:#e53e3e; font-size:1.2em;'>
                <b>Warning:</b> Inferrix API is currently <b>unreachable</b>.<br/>
                Please check your API token, network, or Inferrix service status.<br/>
                <span style='font-size:0.9em; color:#666;'>({status.get('error','')})</span>
            </p>
            <hr style='margin:2em 0;'/>
            <p style='color:#555;'>
                The backend server is <b>up</b> and ready to serve requests.<br/>
                <span style='font-size:0.9em;'>If you are an admin, check the backend logs for more details.</span>
            </p>
        </body>
        </html>
        """,
        status_code=200
    )

@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "✅ FastAPI server is running",
        "timestamp": time.time(),
        "version": "1.0.0",
        "database_available": True,
        "ai_magic_available": True,
        "note": "Use /inferrix/devices or /inferrix/alarms with authentication for API testing"
    }

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
    
    # Run database cleanup once on startup
    cleanup_database()
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

# Force redeploy - Railway fix v2
# FORCE RAILWAY REDEPLOYMENT - 2025-08-18 19:45:00 - AI agent token fix deployed


