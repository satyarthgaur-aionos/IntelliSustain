from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()

INFERRIX_API_TOKEN = os.getenv("INFERRIX_API_TOKEN")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","https://d4c12a824b71.ngrok-free.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "MCP Server for Inferrix is running"}

@app.get("/inferrix/alarms")
def get_alarms(request: Request):
    url = "https://cloud.inferrix.com/api/v2/alarms"
    params = {
        "pageSize": 1000,  # Increased to get all alarms
        "page": 0,
        "sortProperty": "createdTime",
        "sortOrder": "DESC",
        "statusList": "ACTIVE"  # Only ACTIVE alarms by default
    }
    headers = {"X-Authorization": f"Bearer {INFERRIX_API_TOKEN}", "Content-Type": "application/json"}
    try:
        # Check for history/past/last/week/month/day/old in query string
        include_cleared = False
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
    except requests.RequestException as e:
        print("❌ Error calling Inferrix API:", e)
        raise HTTPException(status_code=500, detail="Inferrix API call failed")

@app.get("/inferrix/devices")
def get_devices():
    url = "https://cloud.inferrix.com/api/user/devices"
    params = {
        "pageSize": 100,
        "page": 0,
        "sortProperty": "createdTime",
        "sortOrder": "DESC",
        "includeCustomers": "true"
    }
    headers = {"X-Authorization": f"Bearer {INFERRIX_API_TOKEN}", "Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("❌ Error calling Inferrix API (devices):", e)
        raise HTTPException(status_code=500, detail="Inferrix API call failed (devices)")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting MCP Server on http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
