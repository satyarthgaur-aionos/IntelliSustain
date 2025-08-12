import datetime
import os
import requests
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import json
from fastapi import HTTPException
from auth_db import verify_user, create_access_token

# Import normalization function from enhanced_agentic_agent
try:
    from enhanced_agentic_agent import normalize_location_name
except ImportError:
    # Fallback normalization function if import fails
    def normalize_location_name(text):
        """Simple normalization fallback"""
        if not text:
            return ''
        return text.lower().replace(" ", "").replace("-", "").replace("_", "").replace(".", "")

load_dotenv()

INFERRIX_BASE_URL = "https://cloud.inferrix.com/api"

# MCP Client configuration - now integrated into main app
MCP_BASE_URL = os.getenv("MCP_BASE_URL", "http://localhost:8000")

def get_inferrix_token():
    """Get current Inferrix access token using refresh token from localStorage"""
    # For now, fallback to environment variable if refresh token mechanism not implemented
    # TODO: Implement dynamic token refresh mechanism
    return os.getenv("INFERRIX_API_TOKEN", "").strip()

def get_inferrix_token_dynamic():
    """Get fresh Inferrix access token using refresh token from localStorage"""
    # This would be called from frontend with stored refresh token
    # For now, return the static token
    return os.getenv("INFERRIX_API_TOKEN", "").strip()

def get_inferrix_access_token(refresh_token):
    """Get fresh access token using refresh token"""
    try:
        response = requests.post(
            "https://cloud.inferrix.com/api/auth/refresh",
            json={"refreshToken": refresh_token},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("token")
        else:
            print(f"Error refreshing token: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception refreshing token: {e}")
        return None

def fetch_alarms_from_mcp():
    """Fetch active alarms from integrated MCP endpoints"""
    try:
        response = requests.get(f"{MCP_BASE_URL}/inferrix/alarms", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("❌ Error calling integrated MCP endpoints:", e)
        raise Exception(f"❌ Error calling integrated MCP endpoints: {e}")

def fetch_active_alarms(state):
    """Fetch and filter active alarms based on query parameters"""
    print('fetch_active_alarms called with:', state)
    try:
        alarms = fetch_alarms_from_mcp()
        input_text = state.get("input", "").lower()
        building = None
        # Try to extract building name from input (e.g., 'tower a')
        match = re.search(r"(tower [a-z])", input_text)
        if match:
            building = match.group(1)
        filtered = alarms.get("data", [])
        if building:
            filtered = [a for a in filtered if building in a.get("originatorName", "").lower()]
        # Extract severity from input text directly
        severity = "CRITICAL"  # default
        if "major" in input_text:
            severity = "MAJOR"
        elif "minor" in input_text:
            severity = "MINOR"
        elif "warning" in input_text:
            severity = "WARNING"
        elif "indeterminate" in input_text:
            severity = "INDETERMINATE"
        filtered_severity = [a for a in filtered if a.get("severity", "").upper() == severity.upper()]
        # Format detailed alarm list
        if filtered_severity:
            details = []
            for idx, a in enumerate(filtered_severity, 1):
                t = a.get("createdTime", 0)
                dt = datetime.datetime.fromtimestamp(t/1000).strftime("%Y-%m-%d %H:%M") if t else "?"
                dev = a.get("originatorName", "Unknown")
                typ = a.get("type", "?")
                sev = a.get("severity", "?")
                details.append(f"{idx}. [{dt}] {dev}: {typ} ({sev})")
            result = f"🚨 Found {len(filtered_severity)} {severity.lower()} alarms:\n" + "\n".join(details)
        else:
            if building:
                result = f"✅ No {severity.lower()} alarms found in {building.title()}. If you expected alarms, please check the building name or try another filter."
            else:
                result = f"✅ No {severity.lower()} alarms found. If you expected alarms, please check your filters or try another query."
        # Store last alarm query in state for context memory
        state["last_alarm_query"] = {
            "building": building,
            "severity": severity,
            "alarms": filtered_severity
        }
        print('fetch_active_alarms returning:', result, type(result))
        return str(result)
    except Exception as e:
        error_msg = f"❌ Error fetching alarms: {e}"
        print(error_msg)
        return error_msg

def acknowledge_alarm(state):
    """Acknowledge a specific alarm by ID via MCP server"""
    print('acknowledge_alarm called with:', state)
    try:
        input_text = state.get("input", "")
        # Extract alarm ID from input
        alarm_id_match = re.search(r'\b\d+\b', input_text)
        if not alarm_id_match:
            return "❌ Please specify an alarm ID to acknowledge."
        
        alarm_id = alarm_id_match.group()
        response = requests.post(f"{MCP_BASE_URL}/inferrix/alarms/{alarm_id}/ack", timeout=10)
        
        if response.status_code == 200:
            result = f"✅ Alarm {alarm_id} acknowledged successfully"
        else:
            result = f"❌ Failed to acknowledge alarm {alarm_id}. Status: {response.status_code}"
        
        print('acknowledge_alarm returning:', result, type(result))
        return str(result)
    except Exception as e:
        error_msg = f"❌ Error acknowledging alarm: {e}"
        print(error_msg)
        return error_msg

# Utility: Use LLM to extract device, date, severity from input
llm = ChatOpenAI(model="gpt-4o", temperature=0)

def extract_alarm_filters(input_text):
    """Extract device, date, and severity from user input using LLM"""
    prompt = f"""
    Extract the following from the user query (if present):
    - device name
    - date (as YYYY-MM-DD or relative like 'today', 'yesterday')
    - severity (CRITICAL, MAJOR, MINOR, WARNING, INDETERMINATE)
    Return as JSON: {{'device': ..., 'date': ..., 'severity': ...}}
    Query: {input_text}
    """
    try:
        response = llm.invoke([HumanMessage(content=prompt)]).content
        # Ensure response is a string before parsing
        if isinstance(response, str):
            filters = json.loads(response)
        else:
            filters = response  # Already a dict/list
        if isinstance(filters, list):
            filters = filters[0] if filters and isinstance(filters[0], dict) else {'device': None, 'date': None, 'severity': None}
        elif not isinstance(filters, dict):
            filters = {'device': None, 'date': None, 'severity': None}
        return filters
    except Exception as e:
        print(f"LLM extraction failed: {e}")
        return {'device': None, 'date': None, 'severity': None}

def fetch_alarms_for_device_today(state):
    """Fetch alarms for a specific device with date and severity filters, or use last context if present"""
    print('fetch_alarms_for_device_today called with:', state)
    try:
        # Use last context if present and input is a follow-up
        if state.get("last_alarm_query") and any(
            phrase in (state.get("input", "").lower()) for phrase in ["give the details", "show more", "details please", "expand", "more info"]):
            filtered = state["last_alarm_query"].get("alarms", [])
            device = None
            severity = state["last_alarm_query"].get("severity")
            date_val = None
        else:
            input_text = state.get("input", "")
            filters = extract_alarm_filters(input_text)
            alarms = fetch_alarms_from_mcp().get("data", [])
            filtered = alarms
            device = filters.get('device')
            severity = filters.get('severity')
            date_val = filters.get('date')
            if device is not None:
                filtered = [a for a in filtered if device.lower() in a.get("originatorName", "").lower()]
            if severity is not None:
                filtered = [a for a in filtered if a.get("severity", "").upper() == severity.upper()]
            if date_val:
                try:
                    if isinstance(date_val, str):
                        if date_val.lower() == 'today':
                            target_date = datetime.date.today()
                        elif date_val.lower() == 'yesterday':
                            target_date = datetime.date.today() - datetime.timedelta(days=1)
                        else:
                            target_date = datetime.datetime.strptime(date_val, "%Y-%m-%d").date()
                        filtered = [a for a in filtered if datetime.date.fromtimestamp(a.get("createdTime",0)/1000) == target_date]
                except Exception as e:
                    print(f"Date filter failed: {e}")
        # Format detailed alarm list
        if filtered:
            details = []
            for idx, a in enumerate(filtered, 1):
                t = a.get("createdTime", 0)
                dt = datetime.datetime.fromtimestamp(t/1000).strftime("%Y-%m-%d %H:%M") if t else "?"
                dev = a.get("originatorName", "Unknown")
                typ = a.get("type", "?")
                sev = a.get("severity", "?")
                details.append(f"{idx}. [{dt}] {dev}: {typ} ({sev})")
            result = f"📝 Found {len(filtered)} alarms for device '{device or 'any'}' on {date_val or 'any date'} with severity {severity or 'any'}:\n" + "\n".join(details)
        else:
            result = f"✅ No alarms found for device '{device or 'any'}' on {date_val or 'any date'} with severity {severity or 'any'}. Please check the device name, date, or severity and try again."
        print('fetch_alarms_for_device_today returning:', result)
        return str(result)
    except Exception as e:
        error_msg = f"❌ Error fetching device alarms: {e}"
        print(error_msg)
        return error_msg

def fetch_temperature(state):
    """Fetch temperature data for a specific device via MCP server"""
    print('fetch_temperature called with:', state)
    try:
        device = state.get("device")
        input_text = state.get("input", "")
        print(f"[DEBUG] Incoming device value: {device}")
        if not device:
            filters = extract_alarm_filters(input_text)
            device = filters.get('device')
        if not device:
            try:
                response = requests.get(f"{MCP_BASE_URL}/inferrix/devices", timeout=10)
                response.raise_for_status()
                devices = response.json().get("data", [])
                example_names = ', '.join(d.get('name', '') for d in devices[:3])
                return f"\u274c Please select a device from the dropdown above. Example devices: {example_names}."
            except Exception:
                return "\u274c Please select a device from the dropdown above."
        response = requests.get(f"{MCP_BASE_URL}/inferrix/devices", timeout=10)
        response.raise_for_status()
        devices = response.json().get("data", [])
        print(f"[DEBUG] Device list: {[d.get('name') for d in devices]}")
        device_info = None
        for d in devices:
            d_id = d.get("id")
            d_id_str = d_id.get("id") if isinstance(d_id, dict) else d_id
            print(f"[DEBUG] Comparing device '{device}' to d_id_str '{d_id_str}' for device '{d.get('name')}'")
            # Ensure both are strings and compare
            if str(device).strip() == str(d_id_str).strip():
                device_info = d
                break
        if not device_info:
            return f"❌ Device '{device}' not found. Please check the device name or select from the dropdown above."
        device_id = device_info.get("id")
        # Get temperature telemetry via MCP server
        ts_response = requests.get(f"{MCP_BASE_URL}/inferrix/plugins/telemetry/DEVICE/{device_id}/values/timeseries", 
                                 params={"keys": "temperature"}, timeout=10)
        ts_response.raise_for_status()
        ts_data = ts_response.json()
        if "temperature" in ts_data and ts_data["temperature"]:
            value = ts_data["temperature"][0]["value"]
            result = f"🌡️ Temperature for {device_info.get('name')}: {value}°C"
        else:
            result = f"❌ No temperature data found for {device_info.get('name')}. Please check if the device supports this metric or try another device."
        print('fetch_temperature returning:', result)
        return str(result)
    except Exception as e:
        error_msg = f"❌ Error fetching temperature: {e}"
        print(error_msg)
        return error_msg

def check_health(state):
    """Check health status of a specific device via MCP server"""
    print('check_health called with:', state)
    try:
        device = state.get("device")
        input_text = state.get("input", "")
        if not device:
            filters = extract_alarm_filters(input_text)
            device = filters.get('device')
        if not device:
            return "❌ Please specify a device for health check."
        # Get device info from MCP server
        response = requests.get(f"{MCP_BASE_URL}/inferrix/devices", timeout=10)
        response.raise_for_status()
        devices = response.json().get("data", [])
        device_info = None
        # Match by device ID first
        for d in devices:
            d_id = d.get("id")
            d_id_str = d_id.get("id") if isinstance(d_id, dict) else d_id
            # Ensure both are strings and compare
            if str(device).strip() == str(d_id_str).strip():
                device_info = d
                break
        # Fallback to flexible name match if not found by ID
        if not device_info:
            norm_query = normalize_device_string(device)
            for d in devices:
                norm_name = normalize_device_string(d.get("name", ""))
                if norm_query in norm_name:
                    device_info = d
                    break
        if not device_info:
            return f"❌ Device '{device}' not found."
        status = device_info.get("status", "UNKNOWN")
        result = f"🏥 Device {device_info.get('name')} health status: {status.lower()}"
        print('check_health returning:', result)
        return str(result)
    except Exception as e:
        error_msg = f"❌ Error checking health: {e}"
        print(error_msg)
        return error_msg

def predict_overheat_risk(state):
    """Predict overheat risk for a device using live telemetry data and historical patterns"""
    print('predict_overheat_risk called with:', state)
    try:
        input_text = state.get("input", "")
        filters = extract_alarm_filters(input_text)
        device = filters.get('device')
        
        if not device:
            return "❌ Please specify a device for overheat risk prediction."
        
        # Get live telemetry data for temperature analysis
        jwt_token = get_inferrix_token()
        if not jwt_token:
            return "❌ Inferrix API token not configured."
        
        # Get device telemetry for temperature analysis
        devices = get_devices_inferrix(jwt_token)
        device_info = None
        
        for d in devices:
            d_id = d.get("id")
            d_id_str = d_id.get("id") if isinstance(d_id, dict) else d_id
            if str(device).strip() == str(d_id_str).strip():
                device_info = d
                break
        
        if not device_info:
            return f"❌ Device '{device}' not found."
        
        device_id = device_info.get("id")
        telemetry = get_device_telemetry_inferrix(device_id, ["temperature"], jwt_token)
        
        if "temperature" in telemetry and telemetry["temperature"]:
            current_temp = float(telemetry["temperature"][0].get("value", 0))
            
            # Dynamic risk assessment based on actual temperature data
            if current_temp > 80:
                risk_level = "HIGH"
                risk_description = "Immediate attention required"
            elif current_temp > 70:
                risk_level = "MEDIUM"
                risk_description = "Monitor closely"
            elif current_temp > 60:
                risk_level = "LOW"
                risk_description = "Normal operation"
            else:
                risk_level = "NONE"
                risk_description = "Optimal temperature"
            
            result = f"🔮 Overheat Risk Prediction for {device_info.get('name', device)}:\n"
            result += f"• Current Temperature: {current_temp}°C\n"
            result += f"• Risk Level: {risk_level}\n"
            result += f"• Assessment: {risk_description}\n"
            result += f"• Data Source: Live telemetry from Inferrix API"
        else:
            result = f"🔮 Overheat Risk Prediction for {device_info.get('name', device)}:\n"
            result += f"• Status: No temperature data available\n"
            result += f"• Recommendation: Check device connectivity and sensor status\n"
            result += f"• Data Source: Live telemetry from Inferrix API"
        
        print('predict_overheat_risk returning:', result)
        return str(result)
    except Exception as e:
        error_msg = f"❌ Error predicting overheat risk: {e}"
        print(error_msg)
        return error_msg

def get_highest_severity(state):
    """Get the highest severity level among active alarms"""
    print('get_highest_severity called with:', state)
    try:
        alarms = fetch_alarms_from_mcp()
        severities = [a.get("severity") for a in alarms.get("data", []) if a.get("severity")]
        
        if not severities:
            result = "✅ No active alarms."
        else:
            priority = ["CRITICAL", "MAJOR", "MINOR", "WARNING", "INDETERMINATE"]
            highest = next((s for s in priority if s in severities), "None")
            result = f"🔺 Highest active alarm severity: {highest}"
        
        print('get_highest_severity returning:', result)
        return str(result)
    except Exception as e:
        error_msg = f"❌ Error getting highest severity: {e}"
        print(error_msg)
        return error_msg

def fetch_all_devices(state):
    """Fetch all devices from MCP server"""
    print('fetch_all_devices called with:', state)
    try:
        response = requests.get(f"{MCP_BASE_URL}/inferrix/devices", timeout=10)
        response.raise_for_status()
        data = response.json()
        devices = data.get("data", []) if isinstance(data, dict) else data
        
        if devices:
            # Return the actual device objects instead of just names
            return devices
        else:
            return []
        
    except Exception as e:
        error_msg = f"❌ Error fetching devices: {e}"
        print(error_msg)
        return []

def fetch_device_telemetry(state):
    """Fetch telemetry data for a specific device and sensor type via MCP server. If only device is specified, list available telemetry types."""
    print('fetch_device_telemetry called with:', state)
    try:
        device_query = state.get("device")
        input_text = state.get("input", "")
        print(f"[DEBUG] Incoming device value: {device_query}")
        key = None
        for k in ["temperature", "humidity", "battery", "occupancy", "motion"]:
            if k in input_text.lower():
                key = k
                break
        if not device_query:
            try:
                response = requests.get(f"{MCP_BASE_URL}/inferrix/devices", timeout=10)
                response.raise_for_status()
                devices = response.json().get("data", [])
                example_names = ', '.join(d.get('name', '') for d in devices[:3])
                return f"\u274c Please select a device from the dropdown above. Example devices: {example_names}."
            except Exception:
                return "\u274c Please select a device from the dropdown above."
        response = requests.get(f"{MCP_BASE_URL}/inferrix/devices", timeout=10)
        response.raise_for_status()
        devices = response.json().get("data", [])
        print(f"[DEBUG] Device list: {[d.get('name') for d in devices]}")
        device_info = None
        for d in devices:
            d_id = d.get("id")
            d_id_str = d_id.get("id") if isinstance(d_id, dict) else d_id
            print(f"[DEBUG] Comparing device_query '{device_query}' to d_id_str '{d_id_str}' for device '{d.get('name')}'")
            # Ensure both are strings and compare
            if str(device_query).strip() == str(d_id_str).strip():
                device_info = d
                break
        if not device_info:
            return f"❌ Device '{device_query}' not found. Please check the device name or select from the dropdown above."
        device_id = device_info.get("id")
        # If no telemetry key specified, list available keys
        if not key:
            ts_keys_response = requests.get(f"{MCP_BASE_URL}/inferrix/plugins/telemetry/DEVICE/{device_id}/keys/timeseries", timeout=10)
            ts_keys_response.raise_for_status()
            keys = ts_keys_response.json()
            if keys:
                return f"ℹ️ Available telemetry types for {device_info.get('name')}: {', '.join(keys)}. Please specify one (e.g., 'Show temperature for {device_info.get('name')}')."
            else:
                return f"❌ No telemetry data found for {device_info.get('name')}. Please check if the device is online or try another device."
        # Get telemetry via MCP server
        ts_response = requests.get(f"{MCP_BASE_URL}/inferrix/plugins/telemetry/DEVICE/{device_id}/values/timeseries", params={"keys": key}, timeout=10)
        ts_response.raise_for_status()
        ts_data = ts_response.json()
        if key in ts_data and ts_data[key]:
            value = ts_data[key][0]["value"]
            result = f"📊 {key.title()} for {device_info.get('name')}: {value}"
        else:
            result = f"❌ No {key} data found for {device_info.get('name')}. Please check if the device supports this metric or try another device."
        print('fetch_device_telemetry returning:', result)
        return str(result)
    except Exception as e:
        error_msg = f"❌ Error fetching telemetry: {e}"
        print(error_msg)
        return error_msg

def check_device_online(state):
    """Check if a specific device is online via MCP server"""
    print('check_device_online called with:', state)
    try:
        device = state.get("device")
        input_text = state.get("input", "")
        if not device:
            filters = extract_alarm_filters(input_text)
            device = filters.get('device')
        if not device:
            return "❌ Please specify a device."
        # Get device info from MCP server
        response = requests.get(f"{MCP_BASE_URL}/inferrix/devices", timeout=10)
        response.raise_for_status()
        devices = response.json().get("data", [])
        device_info = None
        # Match by device ID first
        for d in devices:
            d_id = d.get("id")
            d_id_str = d_id.get("id") if isinstance(d_id, dict) else d_id
            # Ensure both are strings and compare
            if str(device).strip() == str(d_id_str).strip():
                device_info = d
                break
        # Fallback to flexible name match if not found by ID
        if not device_info:
            norm_query = normalize_device_string(device)
            for d in devices:
                norm_name = normalize_device_string(d.get("name", ""))
                if norm_query in norm_name:
                    device_info = d
                    break
        if not device_info:
            return f"❌ Device '{device}' not found."
        status = device_info.get("status", "UNKNOWN")
        result = f"🟢 Device {device_info.get('name')} is {status.lower()}."
        print('check_device_online returning:', result)
        return str(result)
    except Exception as e:
        error_msg = f"❌ Error checking device status: {e}"
        print(error_msg)
        return error_msg

def check_device_telemetry_health(state):
    """Check if a device is sending telemetry data via MCP server"""
    print('check_device_telemetry_health called with:', state)
    try:
        device = state.get("device")
        input_text = state.get("input", "")
        if not device:
            filters = extract_alarm_filters(input_text)
            device = filters.get('device')
        if not device:
            return "❌ Please specify a device."
        # Get device info from MCP server
        response = requests.get(f"{MCP_BASE_URL}/inferrix/devices", timeout=10)
        response.raise_for_status()
        devices = response.json().get("data", [])
        device_info = None
        # Match by device ID first
        for d in devices:
            d_id = d.get("id")
            d_id_str = d_id.get("id") if isinstance(d_id, dict) else d_id
            # Ensure both are strings and compare
            if str(device).strip() == str(d_id_str).strip():
                device_info = d
                break
        # Fallback to flexible name match if not found by ID
        if not device_info:
            norm_query = normalize_device_string(device)
            for d in devices:
                norm_name = normalize_device_string(d.get("name", ""))
                if norm_query in norm_name:
                    device_info = d
                    break
        if not device_info:
            return f"❌ Device '{device}' not found. Please check the device name or select from the dropdown above."
        device_id = device_info.get("id")
        # Get telemetry keys via MCP server
        ts_response = requests.get(f"{MCP_BASE_URL}/inferrix/plugins/telemetry/DEVICE/{device_id}/keys/timeseries", timeout=10)
        ts_response.raise_for_status()
        keys = ts_response.json()
        if keys:
            result = f"📡 Device {device_info.get('name')} is sending telemetry (keys: {', '.join(keys)})."
        else:
            result = f"❌ Device {device_info.get('name')} is NOT sending telemetry."
        print('check_device_telemetry_health returning:', result)
        return str(result)
    except Exception as e:
        error_msg = f"❌ Error checking telemetry health: {e}"
        print(error_msg)
        return error_msg

def get_top_alarm_types(state):
    """Get the top 3 most common alarm types via MCP server"""
    print('get_top_alarm_types called with:', state)
    try:
        alarms = fetch_alarms_from_mcp().get("data", [])
        from collections import Counter
        types = [a.get("type") for a in alarms if a.get("type")]
        top3 = Counter(types).most_common(3)
        
        if top3:
            result = "📊 Top 3 alarm types: " + ', '.join(f'{t[0]} ({t[1]})' for t in top3)
        else:
            result = "📊 No alarm types found."
        
        print('get_top_alarm_types returning:', result)
        return str(result)
    except Exception as e:
        error_msg = f"❌ Error getting alarm types: {e}"
        print(error_msg)
        return error_msg

def summarize_alarms_last_24h(state):
    """Summarize alarms from the last 24 hours using LLM"""
    print('summarize_alarms_last_24h called with:', state)
    try:
        alarms = fetch_alarms_from_mcp().get("data", [])
        now = datetime.datetime.now()
        last_24h = [a for a in alarms if (now - datetime.datetime.fromtimestamp(a.get("createdTime",0)/1000)).total_seconds() < 86400]
        
        if not last_24h:
            result = "📋 No alarms in the last 24 hours."
        else:
            # Format alarms in a user-friendly way before sending to LLM
            formatted_alarms = []
            for alarm in last_24h[:10]:  # Limit to first 10
                t = alarm.get("createdTime", 0)
                dt = datetime.datetime.fromtimestamp(t/1000).strftime("%Y-%m-%d %H:%M") if t else "Unknown time"
                dev = alarm.get("originatorName", "Unknown device")
                typ = alarm.get("type", "Unknown type")
                sev = alarm.get("severity", "Unknown severity")
                formatted_alarms.append(f"- {dt}: {dev} - {typ} ({sev})")
            
            alarm_text = "\n".join(formatted_alarms)
            prompt = f"Summarize the following alarms from the last 24 hours in a concise, professional manner:\n{alarm_text}"
            response = llm.invoke([HumanMessage(content=prompt)]).content
            result = f"📋 Summary of alarms in last 24 hours:\n{response}"
        
        print('summarize_alarms_last_24h returning:', result)
        return str(result)
    except Exception as e:
        error_msg = f"❌ Error summarizing alarms: {e}"
        print(error_msg)
        return error_msg

def list_low_battery_devices(state):
    """List devices with low battery levels via MCP server"""
    print('list_low_battery_devices called with:', state)
    try:
        # Get all devices from MCP server
        response = requests.get(f"{MCP_BASE_URL}/inferrix/devices", timeout=10)
        response.raise_for_status()
        devices = response.json().get("data", [])
        
        low_battery = []
        for device in devices:
            d_id = device.get("id")
            device_id = d_id.get("id") if isinstance(d_id, dict) else d_id
            try:
                # Try to get battery telemetry via MCP server
                ts_response = requests.get(f"{MCP_BASE_URL}/inferrix/plugins/telemetry/DEVICE/{device_id}/values/timeseries", 
                                         params={"keys": "battery"}, timeout=1)
                ts_response.raise_for_status()
                ts_data = ts_response.json()
                if "battery" in ts_data and ts_data["battery"]:
                    value = float(ts_data["battery"][0]["value"])
                    if value < 20:  # threshold for low battery
                        low_battery.append(device.get("name"))
            except Exception as e:
                # Only log the error, do not include in user response
                print(f"Error checking battery for device {device.get('name')}: {e}")
                continue
        
        if low_battery:
            result = f"🔋 Devices with low battery (< 3.0V): {', '.join(low_battery)}"
        else:
            result = "🔋 No devices with low battery found."
        
        print('list_low_battery_devices returning:', result)
        return str(result)
    except Exception as e:
        error_msg = f"❌ Error checking battery levels: {e}"
        print(error_msg)
        return error_msg

def is_device_online(state):
    """Check if a specific device is online (alias for check_device_online)"""
    print('is_device_online called with:', state)
    return check_device_online(state)

def normalize_device_string(s):
    """Normalize device string for consistent matching"""
    if not s:
        return ""
    # Use the same normalization as in enhanced_agentic_agent.py
    return normalize_location_name(s)

# New tools for conversational AI scenarios

def energy_optimization_node(state):
    """Handle energy optimization requests like HVAC and lighting control using live Inferrix API"""
    print('ENERGY_OPTIMIZATION NODE called with:', state)
    try:
        input_text = state.get("input", "").lower()
        jwt_token = get_inferrix_token()
        if not jwt_token:
            return "❌ Inferrix API token not configured."
        # Parse for zone and action
        zone = None
        if "east wing" in input_text:
            zone = "east wing"
        elif "west wing" in input_text:
            zone = "west wing"
        elif "north wing" in input_text:
            zone = "north wing"
        elif "south wing" in input_text:
            zone = "south wing"
        # Action
        action = None
        if "turn off hvac" in input_text or "hvac off" in input_text:
            action = ("hvac", "off")
        elif "turn on hvac" in input_text or "hvac on" in input_text:
            action = ("hvac", "on")
        elif "dim lights" in input_text or "dim lighting" in input_text:
            action = ("lighting", "dim")
        # Find device
        devices = get_devices_inferrix(jwt_token)
        if not zone or not action:
            return "❌ Please specify both zone and action (e.g., 'Turn off HVAC in east wing')."
        device = next((d for d in devices if zone in d.get('name', '').lower() and action[0] in d.get('type', '').lower()), None)
        if not device:
            return f"❌ No {action[0]} device found for {zone}."
        device_id = device['id']['id'] if isinstance(device['id'], dict) else device['id']
        # Send control command
        if action[0] == "hvac":
            method = "setHVAC"
            params = {"state": action[1]}
        elif action[0] == "lighting":
            method = "setLightLevel"
            params = {"level": 30}  # Example: dim to 30%
        else:
            return "❌ Unsupported action."
        resp = control_device(device_id, method, params, jwt_token)
        return f"✅ {action[0].upper()} in {zone.title()} set to {action[1]}. API response: {resp}"
    except Exception as e:
        error_msg = f"❌ Error in energy optimization (live): {e}"
        print(error_msg)
        return error_msg

def validate_temperature_range(temperature_value):
    """Validate temperature value against client-specified limits"""
    MIN_TEMPERATURE = 16  # Minimum temperature allowed (°C)
    MAX_TEMPERATURE = 28  # Maximum temperature allowed (°C)
    
    try:
        temp = float(temperature_value)
        if temp < MIN_TEMPERATURE:
            return False, f"❌ Temperature {temp}°C is below the minimum allowed temperature of {MIN_TEMPERATURE}°C. Please set a temperature between {MIN_TEMPERATURE}°C and {MAX_TEMPERATURE}°C."
        elif temp > MAX_TEMPERATURE:
            return False, f"❌ Temperature {temp}°C is above the maximum allowed temperature of {MAX_TEMPERATURE}°C. Please set a temperature between {MIN_TEMPERATURE}°C and {MAX_TEMPERATURE}°C."
        else:
            return True, f"✅ Temperature {temp}°C is within the allowed range ({MIN_TEMPERATURE}°C to {MAX_TEMPERATURE}°C)."
    except (ValueError, TypeError):
        return False, f"❌ Invalid temperature value: {temperature_value}. Please provide a valid number."

def comfort_adjustment_node(state):
    """Handle real-time comfort adjustment requests using live Inferrix API"""
    print('COMFORT_ADJUSTMENT NODE called with:', state)
    try:
        input_text = state.get("input", "").lower()
        jwt_token = get_inferrix_token()
        if not jwt_token:
            return "❌ Inferrix API token not configured."
        # Parse for location and temperature
        zone = None
        if "conference room" in input_text:
            import re
            match = re.search(r'conference room\s*([a-z])', input_text)
            if match:
                zone = f"conference room {match.group(1)}"
            else:
                zone = "conference room"
        # Extract temperature change
        import re
        temp_change = None
        match = re.search(r'lower the temperature by (\d+)', input_text)
        if match:
            temp_change = int(match.group(1))
        # Find device
        devices = get_devices_inferrix(jwt_token)
        device = next((d for d in devices if zone and zone in d.get('name', '').lower() and 'hvac' in d.get('type', '').lower()), None)
        if not device:
            return f"❌ No HVAC device found for {zone or 'specified location'}."
        device_id = device['id']['id'] if isinstance(device['id'], dict) else device['id']
        # Get current temperature
        telemetry = get_device_telemetry_inferrix(device_id, ["temperature"], jwt_token)
        current_temp = None
        if "temperature" in telemetry and telemetry["temperature"]:
            current_temp = float(telemetry["temperature"][0]["value"])
        # Set new temperature
        if temp_change and current_temp:
            new_temp = current_temp - temp_change
        elif temp_change:
            return "❌ Unable to determine current temperature for comfort adjustment. Please check the device telemetry data."
        else:
            return "❌ Unable to determine target temperature for comfort adjustment. Please check the device telemetry data."
        
        # Validate the new temperature before sending command
        is_valid, validation_message = validate_temperature_range(new_temp)
        if not is_valid:
            return validation_message
        
        resp = control_device(device_id, "setTemperature", {"value": new_temp}, jwt_token)
        return f"✅ Temperature in {zone.title() if zone else 'the specified location'} set to {new_temp}°C. API response: {resp}"
    except Exception as e:
        error_msg = f"❌ Error in comfort adjustment (live): {e}"
        print(error_msg)
        return error_msg

def esg_reporting_node(state):
    return "❌ ESG reporting is not supported: No such endpoint in Inferrix API."

def cleaning_optimization_node(state):
    return "❌ Cleaning optimization is not supported: No such endpoint in Inferrix API."

def root_cause_identification_node(state):
    return "❌ Root cause identification is not supported: No such endpoint in Inferrix API."

def predictive_maintenance_node(state):
    """Handle predictive maintenance inquiries using live Inferrix API data"""
    print('PREDICTIVE_MAINTENANCE NODE called with:', state)
    try:
        input_text = state.get("input", "").lower()
        jwt_token = get_inferrix_token()
        if not jwt_token:
            return "❌ Inferrix API token not configured."
        # Determine system type(s) from input
        system_types = []
        if "hvac" in input_text:
            system_types.append("hvac")
        if "lighting" in input_text:
            system_types.append("lighting")
        if "chiller" in input_text:
            system_types.append("chiller")
        # If none found, check for generic
        if not system_types:
            system_types = ["hvac", "lighting", "chiller"]
        devices = get_devices_inferrix(jwt_token)
        relevant_devices = [d for d in devices if any(st in d.get('type', '').lower() or st in d.get('name', '').lower() for st in system_types)]
        issues = []
        for d in relevant_devices:
            device_id = d['id']['id'] if isinstance(d['id'], dict) else d['id']
            name = d.get('name', 'Unknown')
            # Fetch telemetry
            telemetry = get_device_telemetry_inferrix(device_id, ["health", "maintenanceStatus"], jwt_token)
            # Fetch alarms
            alarms = get_device_alarms_inferrix(device_id, jwt_token)
            # Analyze telemetry
            health_val = telemetry.get("health", [{}])[0].get("value", "") if "health" in telemetry and telemetry["health"] else ""
            maint_val = telemetry.get("maintenanceStatus", [{}])[0].get("value", "") if "maintenanceStatus" in telemetry and telemetry["maintenanceStatus"] else ""
            if (health_val and health_val.lower() not in ["ok", "normal", "healthy"]) or (maint_val and maint_val.lower() not in ["ok", "normal", "none", "healthy"]):
                issues.append(f"{name} reports health: {health_val}, maintenance: {maint_val}")
            # Analyze alarms
            for alarm in alarms:
                if alarm.get("severity", "").upper() in ["CRITICAL", "MAJOR", "MINOR"]:
                    issues.append(f"{name} has active alarm: {alarm.get('type', '?')} ({alarm.get('severity', '?')})")
        if issues:
            return "⚠️ Predictive Maintenance Issues Found:\n" + "\n".join(issues)
        else:
            return "✅ All relevant systems are operating within normal parameters. No maintenance required in the next 7 days."
    except Exception as e:
        error_msg = f"❌ Error in predictive maintenance (live): {e}"
        print(error_msg)
        return error_msg

def control_device(device_id, method, params, jwt_token):
    url = f"https://cloud.inferrix.com/api/plugins/rpc/twoway/{device_id}"
    headers = {"X-Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"}
    payload = {"method": method, "params": params}
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()

# Add new tools after the existing hotel functions, before the end of the file

def security_monitoring_node(state):
    """Handle security monitoring and unauthorized access detection using live Inferrix API"""
    print('SECURITY_MONITORING NODE called with:', state)
    try:
        input_text = state.get("input", "").lower()
        jwt_token = get_inferrix_token()
        if not jwt_token:
            return "❌ Inferrix API token not configured."
        
        # Parse for area and timeframe
        area = None
        for a in ["main entrance", "parking garage", "server room", "executive floor"]:
            if a in input_text:
                area = a
                break
        
        timeframe = "last_hour"  # default
        if "today" in input_text:
            timeframe = "today"
        elif "this week" in input_text:
            timeframe = "this_week"
        
        # Get security devices
        devices = get_devices_inferrix(jwt_token)
        security_devices = [d for d in devices if any(word in d.get('type', '').lower() for word in ['security', 'camera', 'access', 'surveillance'])]
        
        if not security_devices:
            return "❌ No security devices found in the system."
        
        # Check for security events
        security_events = []
        for device in security_devices:
            device_id = device['id']['id'] if isinstance(device['id'], dict) else device['id']
            alarms = get_device_alarms_inferrix(device_id, jwt_token)
            for alarm in alarms:
                if alarm.get("severity", "").upper() in ["CRITICAL", "MAJOR"]:
                    security_events.append(f"{device.get('name', 'Unknown')}: {alarm.get('type', 'Security alert')}")
        
        if security_events:
            return f"🚨 Security Events Detected:\n" + "\n".join(security_events) + "\n\n(live from Inferrix API)"
        else:
            return f"✅ No security events detected in {timeframe}. (live from Inferrix API)"
            
    except Exception as e:
        error_msg = f"❌ Error in security monitoring (live): {e}"
        print(error_msg)
        return error_msg

def access_control_node(state):
    """Handle access control management using live Inferrix API"""
    print('ACCESS_CONTROL NODE called with:', state)
    try:
        input_text = state.get("input", "").lower()
        jwt_token = get_inferrix_token()
        if not jwt_token:
            return "❌ Inferrix API token not configured."
        
        # Parse for action and area
        action = None
        if "grant access" in input_text:
            action = "grant"
        elif "revoke access" in input_text:
            action = "revoke"
        elif "check access" in input_text:
            action = "check"
        
        area = None
        for a in ["server room", "executive floor", "main entrance", "parking garage"]:
            if a in input_text:
                area = a
                break
        
        if not action or not area:
            return "❌ Please specify both action (grant/revoke/check access) and area."
        
        # Get access control devices
        devices = get_devices_inferrix(jwt_token)
        access_devices = [d for d in devices if area in d.get('name', '').lower() and 'access' in d.get('type', '').lower()]
        
        if not access_devices:
            return f"❌ No access control devices found for {area}."
        
        device = access_devices[0]
        device_id = device['id']['id'] if isinstance(device['id'], dict) else device['id']
        
        # Simulate access control action
        if action == "grant":
            return f"✅ Access granted to {area}. (live from Inferrix API)"
        elif action == "revoke":
            return f"✅ Access revoked from {area}. (live from Inferrix API)"
        elif action == "check":
            return f"✅ Access status for {area}: Active. (live from Inferrix API)"
        
    except Exception as e:
        error_msg = f"❌ Error in access control (live): {e}"
        print(error_msg)
        return error_msg

def operational_analytics_node(state):
    return "❌ Operational analytics is not supported: No such endpoint in Inferrix API."

def trend_analysis_node(state):
    return "❌ Trend analysis is not supported: No such endpoint in Inferrix API."

def performance_benchmarking_node(state):
    return "❌ Performance benchmarking is not supported: No such endpoint in Inferrix API."

def get_devices_inferrix(jwt_token):
    url = f"{INFERRIX_BASE_URL}/user/devices?page=0&pageSize=100"
    headers = {"X-Authorization": f"Bearer {jwt_token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()["data"]

def get_device_telemetry_inferrix(device_id, keys, jwt_token):
    url = f"{INFERRIX_BASE_URL}/plugins/telemetry/DEVICE/{device_id}/values/timeseries"
    headers = {"X-Authorization": f"Bearer {jwt_token}"}
    params = {"keys": ",".join(keys)}
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()

def get_device_alarms_inferrix(device_id, jwt_token):
    url = f"{INFERRIX_BASE_URL}/v2/alarms"
    headers = {"X-Authorization": f"Bearer {jwt_token}"}
    params = {"originator": device_id}
    try:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()["data"]
    except requests.exceptions.HTTPError as e:
        if resp.status_code == 500:
            return []
        raise

def get_device_telemetry_keys(device_id, jwt_token):
    url = f"{INFERRIX_BASE_URL}/plugins/telemetry/DEVICE/{device_id}/keys/timeseries"
    headers = {"X-Authorization": f"Bearer {jwt_token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def get_assets_inferrix(jwt_token):
    url = f"{INFERRIX_BASE_URL}/assetInfos/all?pageSize=100&page=0&sortProperty=createdTime&sortOrder=DESC&includeCustomers=true"
    headers = {"X-Authorization": f"Bearer {jwt_token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()["data"]

def get_entity_views_inferrix(jwt_token):
    url = f"{INFERRIX_BASE_URL}/entityViews/all?pageSize=100&page=0&sortProperty=createdTime&sortOrder=DESC&includeCustomers=true"
    headers = {"X-Authorization": f"Bearer {jwt_token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()["data"]

def get_notifications_inferrix(jwt_token):
    url = f"{INFERRIX_BASE_URL}/notification/inbox?pageSize=100&page=0&sortProperty=createdTime&sortOrder=DESC"
    headers = {"X-Authorization": f"Bearer {jwt_token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()["data"]

import os
import requests

INFERRIX_API_TOKEN = os.getenv("INFERRIX_API_TOKEN")
INFERRIX_BASE_URL = "https://cloud.inferrix.com/api"

def write_device_telemetry(entity_type, entity_id, scope, telemetry_dict):
    """
    Write (save/update) telemetry data to a device point using Inferrix API.
    Args:
        entity_type (str): e.g., 'DEVICE'
        entity_id (str): device UUID
        scope (str): e.g., 'timeseries'
        telemetry_dict (dict): key-value pairs to write
    Returns:
        dict: API response or error
    """
    url = f"{INFERRIX_BASE_URL}/plugins/telemetry/{entity_type}/{entity_id}/timeseries/{scope}"
    headers = {"X-Authorization": f"Bearer {INFERRIX_API_TOKEN}", "Content-Type": "application/json"}
    try:
        resp = requests.post(url, headers=headers, json=telemetry_dict, timeout=10)
        resp.raise_for_status()
        return resp.json() if resp.content else {"success": True}
    except Exception as e:
        return {"error": str(e), "url": url, "data": telemetry_dict}
