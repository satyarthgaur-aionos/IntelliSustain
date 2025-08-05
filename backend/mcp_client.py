import requests
import os

MCP_BASE_URL = os.getenv("MCP_BASE_URL", "http://localhost:8001/api/inferrix")
AUTH_TOKEN = os.getenv("INFERRIX_AUTH_TOKEN")
HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}"}

def get_devices():
    url = f"{MCP_BASE_URL}/user/devices"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_device_telemetry(entity_type, entity_id, keys):
    url = f"{MCP_BASE_URL}/plugins/telemetry/{entity_type}/{entity_id}/values/timeseries"
    params = {"keys": keys}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

def ack_alarm(alarm_id):
    url = f"{MCP_BASE_URL}/alarms/{alarm_id}/ack"
    response = requests.post(url, headers=HEADERS)
    return response.json()

def get_highest_alarm_severity():
    url = f"{MCP_BASE_URL}/alarms/highestSeverity"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_alarm_types():
    url = f"{MCP_BASE_URL}/alarms/types"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_device_events(device_id):
    url = f"{MCP_BASE_URL}/devices/{device_id}/events"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_publish_telemetry(device_id):
    url = f"{MCP_BASE_URL}/devices/{device_id}/publishTelemetryCommands"
    response = requests.get(url, headers=HEADERS)
    return response.json()