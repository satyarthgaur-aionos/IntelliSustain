import os
import time
import sys
from collections import defaultdict
from typing import Optional

# Add backend directory to Python path
sys.path.append('backend')

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Try to import database components
try:
    from database import engine, Base
    from user_model import User
    from auth_db import get_password_hash, verify_user, create_access_token
    
    # Check if database engine is available
    if engine is None:
        print("❌ Database engine is not available - DATABASE_URL may be empty")
        DATABASE_AVAILABLE = False
    else:
        try:
            # Create database tables on startup
            try:
                Base.metadata.create_all(bind=engine)
                print("✅ Database tables created successfully")
            except Exception as e:
                print(f"⚠️  Warning: Could not create database tables: {e}")
            
            # Migrate existing table to add missing columns
            try:
                with engine.connect() as connection:
                    # Check if columns exist first using text() for raw SQL
                    from sqlalchemy import text
                    result = connection.execute(text("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'users' AND table_schema = 'public'
                    """))
                    existing_columns = [row[0] for row in result]
                    
                    print(f"Existing columns: {existing_columns}")
                    
                    # Add is_active column if it doesn't exist
                    if 'is_active' not in existing_columns:
                        connection.execute(text("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE"))
                        print("✅ Added is_active column")
                    
                    # Add role column if it doesn't exist
                    if 'role' not in existing_columns:
                        connection.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR DEFAULT 'user'"))
                        print("✅ Added role column")
                    
                    # Update existing users with default values
                    connection.execute(text("UPDATE users SET is_active = TRUE WHERE is_active IS NULL"))
                    connection.execute(text("UPDATE users SET role = 'admin' WHERE role IS NULL"))
                    print("✅ Updated existing users with default values")
                    
                    connection.commit()
            except Exception as e:
                print(f"⚠️  Warning: Could not migrate table: {e}")
            
            # Database setup is handled by startup.py script
            # This prevents duplicate user creation
            print("✅ Database setup completed successfully")
            
            DATABASE_AVAILABLE = True
        except Exception as e:
            print(f"⚠️  Warning: Could not setup database: {e}")
            DATABASE_AVAILABLE = False
        
except ImportError as e:
    print(f"⚠️  Warning: Database modules not available: {e}")
    DATABASE_AVAILABLE = False

# Try to import AI Magic Core and Enhanced Agentic Agent
try:
    from ai_magic_core import (
        conversation_memory, multi_device_processor, proactive_insights,
        nlp_processor, rich_response, multi_lang, smart_notifications, self_healing
    )
    from enhanced_agentic_agent import get_enhanced_agentic_agent
    print("✅ AI Magic Core and Enhanced Agentic Agent imported successfully")
    AI_MAGIC_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Warning: AI Magic Core not available: {e}")
    AI_MAGIC_AVAILABLE = False

app = FastAPI(title="Inferrix AI Agent API", version="1.0.0")

# Mount static files (built React app)
try:
    if os.path.exists("static"):
        app.mount("/static", StaticFiles(directory="static"), name="static")
        print("✅ Static files mounted successfully")
    else:
        print("⚠️  Warning: Static files not found. Frontend not built yet.")
        print("   The app will still work with API endpoints only.")
except Exception as e:
    print(f"⚠️  Warning: Could not mount static files: {e}")

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
    """Authenticate user and return JWT token with Inferrix token"""
    if DATABASE_AVAILABLE:
        try:
            print(f"[DEBUG] Login attempt for: {user.email}")
            db_user = verify_user(user.email, user.password)
            if not db_user:
                print(f"[DEBUG] User verification failed for: {user.email}")
                raise HTTPException(status_code=401, detail="Invalid credentials")
            token = create_access_token({"sub": user.email})
            print(f"[DEBUG] Login successful for: {user.email}")
            
            # Get Inferrix token for the user
            try:
                import requests
                
                # First, try to get Inferrix token using user's credentials
                inferrix_response = requests.post(
                    "https://cloud.inferrix.com/api/auth/login",
                    json={"email": user.email, "password": user.password},
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if inferrix_response.status_code == 200:
                    inferrix_data = inferrix_response.json()
                    print(f"[DEBUG] Inferrix response: {inferrix_data}")
                    
                    # Try different possible token field names
                    inferrix_token = None
                    possible_token_fields = ["token", "access_token", "accessToken", "jwt", "jwt_token"]
                    
                    for field in possible_token_fields:
                        if field in inferrix_data:
                            inferrix_token = inferrix_data[field]
                            print(f"[DEBUG] Found token in field '{field}'")
                            break
                    
                    # If no standard field found, look for the first long string that looks like a JWT
                    if not inferrix_token:
                        for key, value in inferrix_data.items():
                            if isinstance(value, str) and len(value) > 100 and value.count('.') == 2:
                                # This looks like a JWT token (3 parts separated by dots)
                                inferrix_token = value
                                print(f"[DEBUG] Found JWT token in field '{key}'")
                                break
                    
                    if inferrix_token:
                        print(f"[DEBUG] Inferrix token obtained for: {user.email}")
                        return {
                            "access_token": token, 
                            "token_type": "bearer",
                            "inferrix_token": inferrix_token
                        }
                    else:
                        print("Warning: No token found in Inferrix response")
                        print(f"[DEBUG] Available fields: {list(inferrix_data.keys())}")
                        return {"access_token": token, "token_type": "bearer"}
                else:
                    print(f"Warning: Inferrix login failed with status {inferrix_response.status_code}")
                    print(f"[DEBUG] Inferrix error response: {inferrix_response.text}")
                    print("Note: User can still login to the application, but Inferrix API access will be limited")
                    return {"access_token": token, "token_type": "bearer"}
                    
            except Exception as e:
                print(f"Warning: Error getting Inferrix token: {e}")
                print("Note: User can still login to the application, but Inferrix API access will be limited")
                return {"access_token": token, "token_type": "bearer"}
                
        except Exception as e:
            print(f"[DEBUG] Login error for {user.email}: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")
    else:
        # No database available - cannot authenticate
        raise HTTPException(status_code=503, detail="Database not available")

def get_current_user():
    """Get current user - requires database"""
    if DATABASE_AVAILABLE:
        try:
            from auth_db import get_current_user as db_get_current_user
            return db_get_current_user()
        except:
            raise HTTPException(status_code=401, detail="Authentication required")
    else:
        raise HTTPException(status_code=503, detail="Database not available")

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
        
        # Use enhanced agentic agent if available
        if AI_MAGIC_AVAILABLE and DATABASE_AVAILABLE:
            try:
                agent = get_enhanced_agentic_agent()
                response = agent.process_query(prompt.query, prompt.user, prompt.device or "")
                
                # Update conversation memory if available
                if conversation_memory:
                    conversation_memory.add_to_history(
                        prompt.user, 
                        prompt.query, 
                        response, 
                        prompt.device
                    )
                
                if not response:
                    response = "No data found or unable to answer your query."
                    
            except Exception as e:
                print(f"Enhanced agent error: {e}")
                response = "No data found or unable to answer your query."
        else:
            response = "No data found or unable to answer your query."
        
        print(f"[DEBUG] Final response: {response[:100]}...")
        
        return {
            "response": response, 
            "tool": "enhanced_agentic_agent" if AI_MAGIC_AVAILABLE and DATABASE_AVAILABLE else "demo_agent",
            "timestamp": time.time(),
            "features_available": {
                "ai_magic": AI_MAGIC_AVAILABLE,
                "database": DATABASE_AVAILABLE,
                "conversation_memory": conversation_memory is not None if AI_MAGIC_AVAILABLE else False,
                "multi_device": multi_device_processor is not None if AI_MAGIC_AVAILABLE else False,
                "proactive_insights": proactive_insights is not None if AI_MAGIC_AVAILABLE else False,
                "nlp_processor": nlp_processor is not None if AI_MAGIC_AVAILABLE else False,
                "rich_response": rich_response is not None if AI_MAGIC_AVAILABLE else False,
                "multi_lang": multi_lang is not None if AI_MAGIC_AVAILABLE else False,
                "smart_notifications": smart_notifications is not None if AI_MAGIC_AVAILABLE else False,
                "self_healing": self_healing is not None if AI_MAGIC_AVAILABLE else False
            }
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
        
        # Use enhanced agentic agent with AI magic features
        if AI_MAGIC_AVAILABLE and DATABASE_AVAILABLE:
            try:
                agent = get_enhanced_agentic_agent()
                response = agent.process_query(prompt.query, prompt.user, prompt.device or "")
                
                # Apply AI Magic Core features
                if conversation_memory:
                    conversation_memory.add_to_history(
                        prompt.user, 
                        prompt.query, 
                        response, 
                        prompt.device
                    )
                
                if not response:
                    response = "No data found or unable to answer your query."
                    
            except Exception as e:
                print(f"Enhanced agent error: {e}")
                response = "No data found or unable to answer your query."
        else:
            response = "No data found or unable to answer your query."
        
        print(f"[DEBUG] Enhanced chat - Final response: {response[:100]}...")
        
        return {
            "response": response, 
            "tool": "enhanced_agentic_agent" if AI_MAGIC_AVAILABLE and DATABASE_AVAILABLE else "demo_enhanced_agent",
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
            ],
            "features_available": {
                "ai_magic": AI_MAGIC_AVAILABLE,
                "database": DATABASE_AVAILABLE,
                "conversation_memory": conversation_memory is not None if AI_MAGIC_AVAILABLE else False,
                "multi_device": multi_device_processor is not None if AI_MAGIC_AVAILABLE else False,
                "proactive_insights": proactive_insights is not None if AI_MAGIC_AVAILABLE else False,
                "nlp_processor": nlp_processor is not None if AI_MAGIC_AVAILABLE else False,
                "rich_response": rich_response is not None if AI_MAGIC_AVAILABLE else False,
                "multi_lang": multi_lang is not None if AI_MAGIC_AVAILABLE else False,
                "smart_notifications": smart_notifications is not None if AI_MAGIC_AVAILABLE else False,
                "self_healing": self_healing is not None if AI_MAGIC_AVAILABLE else False
            }
        }
    except Exception as e:
        print(f"Enhanced chat error: {e}")
        return JSONResponse(
            content={"error": str(e), "code": "ENHANCED_CHAT_ERROR"}, 
            status_code=500
        )

@app.get("/inferrix/alarms")
def get_alarms(current_user=Depends(get_current_user), request: Request = None):
    """Get alarms from Inferrix API (MCP-compatible endpoint)"""
    try:
        # Get user's Inferrix token from request header
        inferrix_token = request.headers.get("X-Inferrix-Token")
        if not inferrix_token:
            raise HTTPException(status_code=401, detail="No token provided")
        
        import requests
        url = "https://cloud.inferrix.com/api/v2/alarms"
        params = {
            "pageSize": 1000,  # Increased to get all alarms
            "page": 0,
            "sortProperty": "createdTime",
            "sortOrder": "DESC",
            "statusList": "ACTIVE"  # Only ACTIVE alarms by default
        }
        headers = {"X-Authorization": f"Bearer {inferrix_token}", "Content-Type": "application/json"}
        
        # Check for history/past/last/week/month/day/old in query string
        include_cleared = False
        if request and request.query_params:
            q = request.query_params.get('q', '').lower()
            if any(word in q for word in ['history', 'past', 'last', 'week', 'month', 'day', 'old']):
                include_cleared = True
                params["statusList"] = "CLEARED,ACTIVE"
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        alarms_data = response.json()
        
        if not include_cleared and isinstance(alarms_data, dict) and 'data' in alarms_data:
            alarms_data['data'] = [a for a in alarms_data['data'] if not a.get('cleared', False)]
        
        return alarms_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch alarms: {str(e)}")

@app.get("/inferrix/devices")
def get_devices(current_user=Depends(get_current_user), request: Request = None):
    """Get devices from Inferrix API (MCP-compatible endpoint)"""
    try:
        # Get user's Inferrix token from request header
        inferrix_token = request.headers.get("X-Inferrix-Token")
        if not inferrix_token:
            raise HTTPException(status_code=401, detail="No token provided")
        
        import requests
        url = "https://cloud.inferrix.com/api/user/devices"
        params = {
            "pageSize": 100,
            "page": 0,
            "sortProperty": "createdTime",
            "sortOrder": "DESC",
            "includeCustomers": "true"
        }
        headers = {"X-Authorization": f"Bearer {inferrix_token}", "Content-Type": "application/json"}
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch devices: {str(e)}")

INFERRIX_BASE_URL = "https://cloud.inferrix.com/api"

# MCP configuration - now integrated into main app
MCP_BASE_URL = os.getenv("MCP_BASE_URL", "http://localhost:8000")

def inferrix_api_status():
    """Check if Inferrix API is reachable"""
    # Since we now use user tokens, we can't check API status without a token
    # This function is used for the /api endpoint which doesn't have user context
    return {"status": "Inferrix API requires user authentication", "note": "Use /inferrix/devices or /inferrix/alarms with user token"}

@app.get("/api")
def api_root():
    """API root endpoint"""
    status = inferrix_api_status()
    return {
        "message": "Inferrix AI Agent API",
        "status": status,
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "database_available": DATABASE_AVAILABLE,
        "ai_magic_available": AI_MAGIC_AVAILABLE
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    try:
        # Simple health check - just verify the app is running
        return {
            "status": "✅ FastAPI server is running", 
            "timestamp": time.time(),
            "version": "1.0.0",
            "database_available": DATABASE_AVAILABLE,
            "ai_magic_available": AI_MAGIC_AVAILABLE,
            "note": "Use /inferrix/devices or /inferrix/alarms with authentication for API testing"
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
        ],
        "features_available": {
            "ai_magic": AI_MAGIC_AVAILABLE,
            "database": DATABASE_AVAILABLE,
            "conversation_memory": conversation_memory is not None if AI_MAGIC_AVAILABLE else False,
            "multi_device": multi_device_processor is not None if AI_MAGIC_AVAILABLE else False,
            "proactive_insights": proactive_insights is not None if AI_MAGIC_AVAILABLE else False,
            "nlp_processor": nlp_processor is not None if AI_MAGIC_AVAILABLE else False,
            "rich_response": rich_response is not None if AI_MAGIC_AVAILABLE else False,
            "multi_lang": multi_lang is not None if AI_MAGIC_AVAILABLE else False,
            "smart_notifications": smart_notifications is not None if AI_MAGIC_AVAILABLE else False,
            "self_healing": self_healing is not None if AI_MAGIC_AVAILABLE else False
        }
    }

@app.get("/debug/devices")
def debug_devices(current_user=Depends(get_current_user), request: Request = None):
    """Debug endpoint to show available devices and their IDs"""
    try:
        # Get user's Inferrix token from request header
        inferrix_token = request.headers.get("X-Inferrix-Token")
        if not inferrix_token:
            raise HTTPException(status_code=401, detail="No token provided")
        
        import requests
        headers = {"X-Authorization": f"Bearer {inferrix_token}"}
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

# Handle all other routes for SPA (must be last)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Serve the React app for all other routes (SPA routing)"""
    try:
        return FileResponse("static/index.html")
    except Exception as e:
        return {"error": "Frontend not available"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

