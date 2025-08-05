#!/usr/bin/env python3
"""
Test script to analyze how various prompts will be processed by the enhanced agentic agent
"""

def test_prompt_analysis():
    """Analyze how different prompts will be processed"""
    
    # Test prompts from user
    test_prompts = [
        "Set the fan speed status to 0 for 2nd floor Room 34",
        "Show temperature in Second Floor Room No. 50",
        "Give temperature of third floor Room50",
        "Temperature in 2F Room 43",
        "Temperature in 3F Room 50",
        "Give temperature of third floor Room50",
        "Show temperature in 3F Room49",
        "Temperature in 3F Room51",
        "Temperature in 2F Room50",
        "Show temperature in Second Floor Room No. 50",
        "Give temperature of 2F-Room50-Thermostat",
        "Show humidity in Room 33",
        "Show battery for all thermostats",
        "Show temperature in InferrixGreenTech office",
        "Turn off fan in Room 201",
        "Set temperature in room 201 to 26 degrees",
        "Set the temperature in Banquet Hall 1 to 24"
    ]
    
    print("🔍 **PROMPT ANALYSIS REPORT**\n")
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"{i}. **Prompt:** {prompt}")
        
        # Analyze function determination
        function = analyze_function_determination(prompt)
        print(f"   **Function:** {function}")
        
        # Analyze device mapping
        device_info = analyze_device_mapping(prompt)
        print(f"   **Device:** {device_info}")
        
        # Analyze telemetry key
        telemetry_key = analyze_telemetry_key(prompt)
        print(f"   **Telemetry Key:** {telemetry_key}")
        
        # Expected behavior
        behavior = predict_behavior(prompt, function, device_info, telemetry_key)
        print(f"   **Expected Behavior:** {behavior}")
        print()

def analyze_function_determination(query):
    """Analyze which function would be called for a query"""
    query_lower = query.lower()
    
    # Check for specific function triggers
    if any(word in query_lower for word in ['fan speed', 'set', 'turn off', 'turn on']):
        return "Control command (setFanSpeed, etc.)"
    elif any(word in query_lower for word in ['temperature', 'humidity', 'battery', 'telemetry', 'heartbeat']):
        return "get_device_telemetry"
    elif any(word in query_lower for word in ['all', 'every', 'multiple']):
        return "get_multi_device_telemetry"
    elif any(word in query_lower for word in ['thermostat', 'thermostats']):
        return "get_devices"
    else:
        return "General query or LLM fallback"

def analyze_device_mapping(query):
    """Analyze device mapping for a query"""
    query_lower = query.lower()
    
    # Extract location patterns
    import re
    
    # Pattern 1: "2nd floor Room 34" -> "2F-Room34-Thermostat"
    match1 = re.search(r'(\d+)(?:nd|rd|th|st)\s+floor\s+room\s+(\d+)', query_lower)
    if match1:
        floor = match1.group(1)
        room = match1.group(2)
        return f"Will map to: {floor}F-Room{room}-Thermostat"
    
    # Pattern 2: "Second Floor Room No. 50" -> "2F-Room50-Thermostat"
    match2 = re.search(r'second\s+floor\s+room\s+no\.?\s*(\d+)', query_lower)
    if match2:
        room = match2.group(1)
        return f"Will map to: 2F-Room{room}-Thermostat"
    
    # Pattern 3: "third floor Room50" -> "3F-Room50-Thermostat"
    match3 = re.search(r'third\s+floor\s+room(\d+)', query_lower)
    if match3:
        room = match3.group(1)
        return f"Will map to: 3F-Room{room}-Thermostat"
    
    # Pattern 4: "2F Room 43" -> "2F-Room43-Thermostat"
    match4 = re.search(r'(\d+)f\s+room\s+(\d+)', query_lower)
    if match4:
        floor = match4.group(1)
        room = match4.group(2)
        return f"Will map to: {floor}F-Room{room}-Thermostat"
    
    # Pattern 5: "Room 33" -> "2F-Room33-Thermostat" (assumes 2F if not specified)
    match5 = re.search(r'room\s+(\d+)', query_lower)
    if match5 and 'floor' not in query_lower and not re.search(r'\d+f', query_lower):
        room = match5.group(1)
        return f"Will map to: 2F-Room{room}-Thermostat (assumed 2F)"
    
    # Pattern 6: "2F-Room50-Thermostat" -> direct match
    if '2f-room50-thermostat' in query_lower:
        return "Direct device name match"
    
    # Pattern 7: "InferrixGreenTech office" -> location-based search
    if 'inferrixgreentech' in query_lower or 'office' in query_lower:
        return "Location-based device search"
    
    # Pattern 8: "Banquet Hall 1" -> location-based search
    if 'banquet' in query_lower:
        return "Location-based device search"
    
    return "No clear device pattern detected"

def analyze_telemetry_key(query):
    """Analyze which telemetry key would be requested"""
    query_lower = query.lower()
    
    if 'temperature' in query_lower or 'temp' in query_lower:
        return "temperature"
    elif 'humidity' in query_lower:
        return "humidity"
    elif 'battery' in query_lower:
        return "battery"
    elif 'heartbeat' in query_lower:
        return "heartbeat"
    elif 'fan speed' in query_lower:
        return "setFanSpeed (control)"
    else:
        return "temperature (default)"

def predict_behavior(prompt, function, device_info, telemetry_key):
    """Predict the expected behavior for a prompt"""
    
    if "Control command" in function:
        if "setFanSpeed" in telemetry_key:
            return "Will attempt to set fan speed to 0 for the specified device"
        elif "temperature" in telemetry_key:
            return "Will attempt to set temperature to specified value"
    
    if "get_device_telemetry" in function:
        if "No clear device pattern" in device_info:
            return "Will show available devices and suggest alternatives"
        elif "Room50" in device_info or "Room51" in device_info:
            return "Will show error: Room not found, suggest available rooms on that floor"
        else:
            return f"Will fetch {telemetry_key} data for the specified device"
    
    if "get_multi_device_telemetry" in function:
        return f"Will fetch {telemetry_key} data for all thermostats"
    
    if "get_devices" in function:
        return "Will show list of all available devices"
    
    return "Will use LLM to generate response or show error message"

if __name__ == "__main__":
    test_prompt_analysis() 