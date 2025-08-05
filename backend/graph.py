from typing import TypedDict, Optional
#from langchain_core.messages import HumanMessage
#from langchain_core.runnables import RunnableLambda
#from langchain_core.runnables.graph import END, StateGraph
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnableBranch

from tools import (
    fetch_active_alarms,
    acknowledge_alarm,
    fetch_temperature,
    check_health,
    predict_overheat_risk,
    fetch_alarms_for_device_today,
    get_highest_severity,
    fetch_all_devices,
    fetch_device_telemetry,
    check_device_online,
    check_device_telemetry_health,
    get_top_alarm_types,
    summarize_alarms_last_24h,
    list_low_battery_devices,
    is_device_online,
    energy_optimization_node,
    comfort_adjustment_node,
    predictive_maintenance_node,
    esg_reporting_node,
    cleaning_optimization_node,
    root_cause_identification_node
)

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# LLM config
use_gemini = "GOOGLE_API_KEY" in os.environ and os.environ["GOOGLE_API_KEY"]
llm = (
    ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
    if use_gemini else
    ChatOpenAI(model="gpt-4o", temperature=0)
)

# Define graph state schema
class AgentState(TypedDict, total=False):
    input: str
    user: str
    result: str
    tool: str
    last_alarm_query: dict  # For context memory

# For dynamic state updates, we'll use regular dict operations

# Tool functions
# Add print statements and ensure only 'result' is returned

def alarms_node(state):
    print('ALARMS NODE called with:', state)
    out = fetch_active_alarms(state)
    print('ALARMS NODE returned:', out)
    return {**state, 'result': out, 'tool': 'alarms'}

def acknowledge_node(state):
    print('ACKNOWLEDGE NODE called with:', state)
    out = acknowledge_alarm(state)
    print('ACKNOWLEDGE NODE returned:', out)
    return {**state, 'result': out, 'tool': 'acknowledge'}

def temperature_node(state):
    print('TEMPERATURE NODE called with:', state)
    out = fetch_temperature(state)
    print('TEMPERATURE NODE returned:', out)
    return {**state, 'result': out, 'tool': 'temperature'}

def health_node(state):
    print('HEALTH NODE called with:', state)
    out = check_health(state)
    print('HEALTH NODE returned:', out)
    return {**state, 'result': out, 'tool': 'health'}

def predict_node(state):
    print('PREDICT NODE called with:', state)
    out = predict_overheat_risk(state)
    print('PREDICT NODE returned:', out)
    return {**state, 'result': out, 'tool': 'predict'}

def alarms_by_device_node(state):
    print('ALARMS_BY_DEVICE NODE called with:', state)
    out = fetch_alarms_for_device_today(state)
    print('ALARMS_BY_DEVICE NODE returned:', out)
    return {**state, 'result': out, 'tool': 'alarms_by_device'}

def severity_node(state):
    print('SEVERITY NODE called with:', state)
    out = get_highest_severity(state)
    print('SEVERITY NODE returned:', out)
    return {**state, 'result': out, 'tool': 'severity'}

def devices_node(state):
    print('DEVICES NODE called with:', state)
    out = fetch_all_devices(state)
    print('DEVICES NODE returned:', out)
    return {**state, 'result': out, 'tool': 'devices'}

def telemetry_node(state):
    print('TELEMETRY NODE called with:', state)
    out = fetch_device_telemetry(state)
    print('TELEMETRY NODE returned:', out)
    return {**state, 'result': out, 'tool': 'telemetry'}

def online_node(state):
    print('ONLINE NODE called with:', state)
    out = check_device_online(state)
    print('ONLINE NODE returned:', out)
    return {**state, 'result': out, 'tool': 'online'}

def telemetry_health_node(state):
    print('TELEMETRY_HEALTH NODE called with:', state)
    out = check_device_telemetry_health(state)
    print('TELEMETRY_HEALTH NODE returned:', out)
    return {**state, 'result': out, 'tool': 'telemetry_health'}

def alarm_types_node(state):
    print('ALARM_TYPES NODE called with:', state)
    out = get_top_alarm_types(state)
    print('ALARM_TYPES NODE returned:', out)
    return {**state, 'result': out, 'tool': 'alarm_types'}

def summarize_alarms_node(state):
    print('SUMMARIZE_ALARMS NODE called with:', state)
    out = summarize_alarms_last_24h(state)
    print('SUMMARIZE_ALARMS NODE returned:', out)
    return {**state, 'result': out, 'tool': 'summarize_alarms'}

def low_battery_node(state):
    print('LOW_BATTERY NODE called with:', state)
    out = list_low_battery_devices(state)
    print('LOW_BATTERY NODE returned:', out)
    return {**state, 'result': out, 'tool': 'low_battery'}

def is_online_node(state):
    print('IS_ONLINE NODE called with:', state)
    out = is_device_online(state)
    print('IS_ONLINE NODE returned:', out)
    return {**state, 'result': out, 'tool': 'is_online'}

def llm_node(state):
    print('LLM NODE called with:', state)
    response = llm.invoke([HumanMessage(content=state.get("input", ""))]).content
    return {**state, "result": response, "tool": "llm"}

def fallback_node(state):
    """Graceful fallback when no tool matches"""
    print('FALLBACK NODE called with:', state)
    fallback_message = (
        "❌ I couldn't understand your request.\n\n"
        "**What you can do:**\n"
        "- Please rephrase your question with more details or specific terms.\n"
        "- Try asking about a specific device, location, or metric.\n"
        "- If you need help, here are some example queries you can try:\n"
        "  • 'Show temperature for Conference Room B'\n"
        "  • 'Check device health for IAQ Sensor V2 - 300186'\n"
        "  • 'Show all critical alarms'\n"
        "  • 'List devices with low battery'\n"
        "\nIf you continue to have trouble, please contact your system administrator or Inferrix support."
    )
    return {**state, "result": fallback_message, "tool": "fallback"}

def energy_opt_node(state):
    print('ENERGY_OPTIMIZATION NODE called with:', state)
    out = energy_optimization_node(state)
    print('ENERGY_OPTIMIZATION NODE returned:', out)
    return {**state, 'result': out, 'tool': 'energy_optimization'}

def comfort_adj_node(state):
    print('COMFORT_ADJUSTMENT NODE called with:', state)
    out = comfort_adjustment_node(state)
    print('COMFORT_ADJUSTMENT NODE returned:', out)
    return {**state, 'result': out, 'tool': 'comfort_adjustment'}

def predictive_maint_node(state):
    print('PREDICTIVE_MAINTENANCE NODE called with:', state)
    out = predictive_maintenance_node(state)
    print('PREDICTIVE_MAINTENANCE NODE returned:', out)
    return {**state, 'result': out, 'tool': 'predictive_maintenance'}

def esg_report_node(state):
    print('ESG_REPORTING NODE called with:', state)
    out = esg_reporting_node(state)
    print('ESG_REPORTING NODE returned:', out)
    return {**state, 'result': out, 'tool': 'esg_reporting'}

def cleaning_opt_node(state):
    print('CLEANING_OPTIMIZATION NODE called with:', state)
    out = cleaning_optimization_node(state)
    print('CLEANING_OPTIMIZATION NODE returned:', out)
    return {**state, 'result': out, 'tool': 'cleaning_optimization'}

def root_cause_node(state):
    print('ROOT_CAUSE_IDENTIFICATION NODE called with:', state)
    out = root_cause_identification_node(state)
    print('ROOT_CAUSE_IDENTIFICATION NODE returned:', out)
    return {**state, 'result': out, 'tool': 'root_cause_identification'}

tools = {
    "alarms": RunnableLambda(alarms_node),
    "acknowledge": RunnableLambda(acknowledge_node),
    "temperature": RunnableLambda(temperature_node),
    "health": RunnableLambda(health_node),
    "predict": RunnableLambda(predict_node),
    "alarms_by_device": RunnableLambda(alarms_by_device_node),
    "severity": RunnableLambda(severity_node),
    "devices": RunnableLambda(devices_node),
    "telemetry": RunnableLambda(telemetry_node),
    "online": RunnableLambda(online_node),
    "telemetry_health": RunnableLambda(telemetry_health_node),
    "alarm_types": RunnableLambda(alarm_types_node),
    "summarize_alarms": RunnableLambda(summarize_alarms_node),
    "low_battery": RunnableLambda(low_battery_node),
    "is_online": RunnableLambda(is_online_node),
    "fallback": RunnableLambda(fallback_node),
    "energy_optimization": RunnableLambda(energy_opt_node),
    "comfort_adjustment": RunnableLambda(comfort_adj_node),
    "predictive_maintenance": RunnableLambda(predictive_maint_node),
    "esg_reporting": RunnableLambda(esg_report_node),
    "cleaning_optimization": RunnableLambda(cleaning_opt_node),
    "root_cause_identification": RunnableLambda(root_cause_node),
}

# Tool router
# Add print to router

def extract_severity(query: str) -> Optional[str]:
    """Extract severity level from query"""
    query_lower = query.lower()
    if "critical" in query_lower:
        return "CRITICAL"
    if "major" in query_lower:
        return "MAJOR"
    if "minor" in query_lower:
        return "MINOR"
    if "warning" in query_lower:
        return "WARNING"
    if "indeterminate" in query_lower:
        return "INDETERMINATE"
    return None

def select_tool(state: AgentState):
    """Improved router with context and better alarm/telemetry distinction"""
    print('ROUTER called with:', state)
    query = (state.get("input") or "").lower()
    severity = extract_severity(query)

    # New conversational AI scenarios - check these first
    # Energy optimization
    if any(word in query for word in ["turn off hvac", "dim lights", "energy optimization", "weekend schedule", "energy savings"]):
        return "energy_optimization"
    
    # Comfort adjustment
    if any(word in query for word in ["lower temperature", "comfort", "conference room", "townhall", "environmental control"]):
        return "comfort_adjustment"
    
    # Predictive maintenance
    if any(word in query for word in ["likely to fail", "predictive maintenance", "system health", "maintenance schedule", "compressor strain"]):
        return "predictive_maintenance"
    
    # ESG reporting
    if any(word in query for word in ["carbon emissions", "co2", "esg", "sustainability", "green building", "q3 target"]):
        return "esg_reporting"
    
    # Cleaning optimization
    if any(word in query for word in ["least used restrooms", "cleaning schedule", "restroom usage", "cleaning routes"]):
        return "cleaning_optimization"
    
    # Root cause identification
    if any(word in query for word in ["why is", "warm and noisy", "environmental discomfort", "root cause", "chiller underperformance"]):
        return "root_cause_identification"

    # Contextual follow-up: 'give the details', 'show more', etc.
    if any(phrase in query for phrase in ["give the details", "show more", "details please", "expand", "more info"]):
        if state.get("last_alarm_query"):
            return "alarms_by_device"  # Use last context
        else:
            return "alarms"

    # Device + alarm queries (e.g., 'show all alarms for device X', 'alarms in Tower A')
    if ("alarm" in query or "alarms" in query or "alert" in query or "alerts" in query) and (
        "device" in query or "sensor" in query or "tower" in query or "room" in query or any(name in query for name in ["iaq", "rh/t", "hvac", "thermostat", "controller", "pir"])):
        return "alarms_by_device"

    # General alarm queries
    if any(word in query for word in ["alarm", "alarms", "alert", "alerts", "issue", "problem"]):
        return "alarms"

    # Telemetry/sensor data queries (must mention telemetry/temperature/humidity etc.)
    if any(word in query for word in ["telemetry", "sensor", "humidity", "occupancy", "motion", "reading", "readings", "sensor data", "measurements"]):
        return "telemetry"
    if any(word in query for word in ["temperature", "temp", "thermal", "heat", "cooling"]):
        return "temperature"

    # Battery-related queries
    if any(word in query for word in ["low battery", "battery low", "devices with low battery", "battery status", "low power"]):
        return "low_battery"
    # Device-related queries
    if any(word in query for word in ["device", "devices", "list devices", "show devices", "all devices"]):
        return "devices"
    # Alarm type analysis
    if any(word in query for word in ["alarm types", "top 3 alarm types", "most common alarms", "alarm categories"]):
        return "alarm_types"
    # Alarm summaries
    if any(word in query for word in ["summarize alarms", "summary of alarms", "alarms in last 24 hours", "alarm summary", "recent alarms"]):
        return "summarize_alarms"
    # Online status queries
    if any(word in query for word in ["is online", "online status", "is device online", "device status", "connection status"]):
        return "is_online"
    # Telemetry health queries
    if any(word in query for word in ["not sending telemetry", "disconnected", "telemetry health", "data transmission", "sensor data"]):
        return "telemetry_health"
    # Health check queries
    if any(word in query for word in ["health", "health check", "device health", "system health", "status check"]):
        return "health"
    # Prediction queries
    if any(word in query for word in ["predict", "prediction", "overheat", "risk", "forecast", "future"]):
        return "predict"
    # Acknowledge queries
    if any(word in query for word in ["acknowledge", "ack", "resolve", "clear alarm", "mark as resolved"]):
        return "acknowledge"
    # Severity queries
    if any(word in query for word in ["highest severity", "most severe", "worst alarm", "critical level"]):
        return "severity"
    # Fallback
    return "fallback"

# Build the graph
workflow = StateGraph(AgentState)

# Add router node first
workflow.add_node("router", RunnableLambda(lambda state: state))

# Add all nodes
for tool_name, tool_func in tools.items():
    workflow.add_node(tool_name, tool_func)

# Add router
workflow.add_conditional_edges(
    "router",
    select_tool,
    {tool_name: tool_name for tool_name in tools.keys()}
)

# Set entry point
workflow.set_entry_point("router")

# Set exit point - all tools terminate the graph
for tool_name in tools.keys():
    workflow.add_edge(tool_name, END)

# Compile the graph
agent_graph = workflow.compile()
