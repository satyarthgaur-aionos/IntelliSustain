def classify_intent(prompt: str) -> str:
    prompt = prompt.lower()

    if "devices" in prompt:
        return "get_devices"
    elif any(x in prompt for x in ["temperature", "humidity", "co2", "occupancy"]):
        return "get_environment"
    elif "acknowledge" in prompt and "alarm" in prompt:
        return "acknowledge_alarm"
    elif "highest severity" in prompt:
        return "get_alarm_severity"
    elif "alarm types" in prompt:
        return "get_alarm_types"
    elif any(x in prompt for x in ["disconnected", "not sending", "stopped"]):
        return "get_device_health"
    elif any(x in prompt for x in ["overheat", "energy usage"]):
        return "predictive_alert"
    elif "who am i" in prompt or "identity" in prompt:
        return "whoami"
    else:
        return "get_devices"