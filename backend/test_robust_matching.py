#!/usr/bin/env python3
"""
Test script for robust substring normalization matching
"""

from dotenv import load_dotenv
load_dotenv()

from enhanced_agentic_agent import normalize_location_name, EnhancedAgenticInferrixAgent
import re

def extract_device_phrase(query):
    """Extract the likely device/location phrase from a user query using regex and heuristics."""
    # Try to extract after 'in', 'at', 'for', 'of', 'on', etc.
    match = re.search(r'\b(?:in|at|for|of|on)\b\s+([\w\s\-\.]+)', query, re.IGNORECASE)
    if match:
        phrase = match.group(1).strip()
        # Remove trailing question/command words
        phrase = re.sub(r'\b(temperature|thermostat|sensor|controller|ac|hvac|fcu|tag|please|now|today|status|reading|value|data|show|display|is|are|was|were|be|get|set|to|by|with|from|and|or|the|a|an|of|for|on|in|at|no|number|room|floor|mansion|building|block|tower|wing|zone|area|section|unit|suite|flat|apartment|office|lobby|hall|corridor|passage|stairs|lift|elevator|basement|ground|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|manzil|मंजिल|कमरा|संख्या|का|में|की|के|पर|है|का|का|का|का)\b', '', phrase, flags=re.IGNORECASE)
        return phrase.strip()
    # Fallback: try to extract a room/floor pattern
    match = re.search(r'(\d+[a-z]?f?[-_\s]*room\s*\d+)', query, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Fallback: return the whole query
    return query.strip()

def test_normalization():
    print("=== Testing Normalization Function ===")
    test_cases = [
        "Show temperature in Second Floor Room No. 50",
        "2F-Room50-Thermostat",
        "Second Floor Room 50",
        "2nd Floor Room No. 50",
        "Room 50 on Second Floor",
        "दूसरी मंजिल कमरा 50",
        "2F Room 50",
        "Room50 2F",
        "2froom50",
        "2f-room50",
        "2f_room50",
        "2f.room50",
        "Show temperature at 2F-Room50-Thermostat",
        "Temperature for 2F Room 50",
        "Thermostat in Room 50, Second Floor",
        "कमरा ५० दूसरी मंजिल",
        "2F Room 50 Thermostat",
        "2F-Room50",
        "2F Room 50 AC",
        "2F Room 50 FCU",
        "2F Room 50 Tag",
        "2F Room 50 Sensor",
        "2F Room 50 Controller",
        "2F Room 50 Lighting",
        "2F Room 50",
        "Room 50",
        "Second Floor",
        "2F",
        "50"
    ]
    for test_case in test_cases:
        normalized = normalize_location_name(test_case)
        print(f"Input: '{test_case}'\nNormalized: '{normalized}'\n{'-'*50}")

def test_device_matching():
    print("\n=== Testing Device Matching ===")
    agent = EnhancedAgenticInferrixAgent()
    test_queries = [
        "Show temperature in Second Floor Room No. 50",
        "What's the temperature in 2F Room 50?",
        "Room 50 on Second Floor temperature",
        "2F-Room50-Thermostat",
        "2froom50",
        "Second Floor Room 50 thermostat",
        "Show temperature at 2F-Room50-Thermostat",
        "Temperature for 2F Room 50",
        "Thermostat in Room 50, Second Floor",
        "कमरा ५० दूसरी मंजिल",
        "2F Room 50 Thermostat",
        "2F-Room50",
        "2F Room 50 AC",
        "2F Room 50 FCU",
        "2F Room 50 Tag",
        "2F Room 50 Sensor",
        "2F Room 50 Controller",
        "2F Room 50 Lighting",
        "2F Room 50",
        "Room 50",
        "Second Floor",
        "2F",
        "50"
    ]
    for query in test_queries:
        print(f"\nTesting query: '{query}'")
        device_phrase = extract_device_phrase(query)
        print(f"Extracted device phrase: '{device_phrase}'")
        device_id = agent._map_device_name_to_id(device_phrase)
        print(f"Mapped device ID: {device_id}")
        if device_id:
            print("✅ SUCCESS: Device found!")
        else:
            print("❌ FAILED: No device found")

if __name__ == "__main__":
    test_normalization()
    test_device_matching() 