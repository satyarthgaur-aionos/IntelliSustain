# HVAC Fault Knowledge Base (parsed from UNIT FAULT POSSIBLITIES.xlsx images)

FAULT_KNOWLEDGE = [
    # Treated Fresh Air Unit (TFA Unit)
    {"equipment": "TFA", "fault": "Fan Failure", "parameter": "Supply fan not running", "possibility": "Power Supply Issue / Unit in Manual Mode/ Damper Status Not received/ Unit Offline", "suggestion": "Power Supply Issue / Unit in Manual Mode/ Damper Status Not received/ Unit Offline."},
    {"equipment": "TFA", "fault": "Fan Failure", "parameter": "Motor overload trip", "possibility": "VFD fault", "suggestion": "Check for Overload Current / Voltage."},
    {"equipment": "TFA", "fault": "Fan Failure", "parameter": "Uncommanded fan stop", "possibility": "Actuator failure", "suggestion": "Check Power Supply / Unit Offline."},
    {"equipment": "TFA", "fault": "Damper Fault", "parameter": "Outdoor/return air damper stuck (not modulating as commanded)", "possibility": "Feedback mismatch with command signal", "suggestion": "Actuator Stuck/ Not properly installed/ Power Supply Issue/Actuator Fault."},
    {"equipment": "TFA", "fault": "Filter Choke Alarm", "parameter": "High differential pressure across filter", "possibility": "Clogged filters requiring cleaning or replacement", "suggestion": "Clogged filters/pressure indication/cleaning or replacement."},
    {"equipment": "TFA", "fault": "Cooling Coil Fault", "parameter": "Valve actuator fault for chilled water coils", "possibility": "Low or no temperature change across coil", "suggestion": "Power Supply Issue / Faulty Sensor / Unit Offline."},
    {"equipment": "TFA", "fault": "High/Low Supply Air Temperature", "parameter": "Deviates beyond configured setpoints", "possibility": "Faulty actuator/ leak or room conditions deviation", "suggestion": "Check actuator leak or room conditions deviation."},
    {"equipment": "TFA", "fault": "CO2 High Alarm", "parameter": "CO2 High", "possibility": "Indicates poor ventilation or over-occupancy", "suggestion": "Check ventilation or occupancy."},
    {"equipment": "TFA", "fault": "Phase Loss / Power Failure", "parameter": "Power supply interruption to the TFA unit", "possibility": "Check Power Supply", "suggestion": "Check Power Supply."},
    {"equipment": "TFA", "fault": "BMS Communication Failure", "parameter": "Loss of communication with the TFA Controller", "possibility": "Power supply interruption to the TFA Controller", "suggestion": "Check Power Supply."},
    {"equipment": "TFA", "fault": "BMS Communication Failure", "parameter": "Data not updating in BMS", "possibility": "Network Issue/ System Offline", "suggestion": "Check Network strength."},
    # Air Cooled Water Chillers
    {"equipment": "Chiller", "fault": "Compressor Fault", "parameter": "High discharge temperature", "possibility": "Overload/overcurrent trip", "suggestion": "Alarms will be generated on the Chiller Controller."},
    {"equipment": "Chiller", "fault": "Compressor Fault", "parameter": "Short cycling (frequent start-stop)", "possibility": "Locked rotor or no-start condition", "suggestion": "Alarms will be generated on the Chiller Controller."},
    {"equipment": "Chiller", "fault": "Condenser Fan Fault", "parameter": "Fan not running when commanded", "possibility": "High condensing pressure due to fan failure", "suggestion": "Alarms will be generated on the Chiller Controller."},
    {"equipment": "Chiller", "fault": "Refrigerant Circuit Fault", "parameter": "Low refrigerant pressure alarm", "possibility": "Low suction temperature", "suggestion": "Alarms will be generated on the Chiller Controller."},
    {"equipment": "Chiller", "fault": "Pump Related Faults", "parameter": "Low differential pressure", "possibility": "Refrigeration leak detected (if sensors available)", "suggestion": "Alarms will be generated on the Chiller Controller."},
    {"equipment": "Chiller", "fault": "High Chilled Water Supply", "parameter": "Indicates poor cooling performance or system overshoot", "possibility": "System overshoot", "suggestion": "Indicates poor cooling performance or system overshoot."},
    {"equipment": "Chiller", "fault": "Chiller Not Available / Off", "parameter": "Due to local control, BMS disable signal, or fault lockout", "possibility": "Indicates command/logic interlock or improper capacity control", "suggestion": "Check local/remote status and capacity control."},
    {"equipment": "Chiller", "fault": "Main Power Supply Failure", "parameter": "Total power loss to the chiller", "possibility": "Power loss", "suggestion": "Total power loss to the chiller."},
    # Pumps
    {"equipment": "Pump", "fault": "On/Off Command", "parameter": "Command Not Working", "possibility": "Unit in manual mode/connection issue/system offline", "suggestion": "Unit in Manual Mode / Unit Offline / Power Supply Issue."},
    {"equipment": "Pump", "fault": "Trip Status", "parameter": "Pump fault", "possibility": "Check for the alarm.", "suggestion": "Check for the alarm."},
    {"equipment": "Pump", "fault": "Phase Loss / Power Failure", "parameter": "Power supply interruption to the Pump unit", "possibility": "Check Power Supply", "suggestion": "Check Power Supply."},
    {"equipment": "Pump", "fault": "BMS Communication Failure", "parameter": "Data not updating in BMS", "possibility": "Network Issue/ System Offline", "suggestion": "Check Network strength."},
    # AQI Sensors
    {"equipment": "AQI Sensor", "fault": "AQI", "parameter": "Range Between 0-50", "possibility": "Good", "suggestion": "Minimal impact."},
    {"equipment": "AQI Sensor", "fault": "AQI", "parameter": "Range Between 51-100", "possibility": "Satisfactory/Minor Breathing Discomfort For Sensitive People", "suggestion": "Good / Minimal impact."},
    {"equipment": "AQI Sensor", "fault": "CO2", "parameter": "Range Between 400-800", "possibility": "Acceptable conditions with normal level of CO2", "suggestion": "Acceptable conditions."},
    {"equipment": "AQI Sensor", "fault": "pm 10", "parameter": "Range Between 0-50", "possibility": "Good / Minimal impact", "suggestion": "Good / Minimal impact."},
    {"equipment": "AQI Sensor", "fault": "Battery Failure", "parameter": "Battery Reading < 2.7", "possibility": "Battery Burned Out", "suggestion": "Check / Replace Battery."},
]

def get_fault_suggestion(fault, parameter=None):
    """
    Lookup suggestion(s) for a given fault (and optional parameter).
    Returns a list of dicts with all matches.
    """
    results = []
    for entry in FAULT_KNOWLEDGE:
        if entry["fault"].lower() == fault.lower() and (parameter is None or parameter.lower() in entry["parameter"].lower()):
            results.append(entry)
    return results 