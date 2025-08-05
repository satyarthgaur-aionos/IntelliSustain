import requests
import os

# Load from .env
MCP_BASE_URL = os.getenv("MCP_BASE_URL", "http://localhost:8001/api/inferrix")

def get_critical_alarms(building_name: str):
    """Fetch alarms and filter critical ones for a building"""
    res = requests.get(f"{MCP_BASE_URL}/user/devices")
    if res.status_code != 200:
        return "Error fetching device list"

    devices = res.json()
    matching = [d for d in devices if building_name.lower() in d.get("name", "").lower()]
    results = []

    for device in matching:
        device_id = device.get("id")
        alarms = requests.get(f"{MCP_BASE_URL}/devices/{device_id}/events").json()
        critical = [a for a in alarms if a.get("severity") == "CRITICAL"]
        results.extend(critical)

    if not results:
        return f"No critical alarms found in {building_name}"
    return f"Found {len(results)} critical alarms in {building_name}."

def acknowledge_alarm(alarm_id: str):
    """Acknowledge a specific alarm by ID"""
    res = requests.post(f"{MCP_BASE_URL}/alarms/{alarm_id}/ack")
    if res.status_code == 200:
        return f"✅ Alarm {alarm_id} acknowledged."
    else:
        return f"❌ Failed to acknowledge alarm {alarm_id}."

def get_temperature(entity_type: str, entity_id: str, key="temperature"):
    """Query telemetry temperature for a given device"""
    url = f"{MCP_BASE_URL}/plugins/telemetry/{entity_type}/{entity_id}/values/timeseries"
    res = requests.get(url, params={"keys": key})
    if res.status_code != 200:
        return "Failed to fetch telemetry."

    data = res.json().get(key, [])
    if not data:
        return "No temperature data found."
    latest = data[-1]
    return f"🌡️ Latest temperature: {latest.get('value')}°C at {latest.get('ts')}"

def get_device_publish_status(device_id: str):
    """Check if device is sending telemetry"""
    url = f"{MCP_BASE_URL}/devices/{device_id}/publishTelemetryCommands"
    res = requests.get(url)
    if res.status_code != 200:
        return "Failed to check telemetry status."
    status = res.json()
    return f"Device {device_id} publish status: {status}"