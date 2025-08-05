# Energy Consumption Guide for Inferrix AI Agent

## Overview
This guide explains how to find energy consumption for any location or device using the available APIs in the Inferrix system.

## Available APIs for Energy Consumption

### 1. TELEMETRY API ENDPOINTS
- **Base URL**: `https://cloud.inferrix.com/api`
- **Endpoint**: `/plugins/telemetry/DEVICE/{device_id}/values/timeseries`
- **Method**: GET
- **Parameters**: 
  - `keys` (comma-separated list of telemetry keys)
  - `startTs` (start timestamp)
  - `endTs` (end timestamp)
  - `limit` (number of records to return)

### 2. DEVICE DISCOVERY API
- **Endpoint**: `/deviceInfos/all`
- **Method**: GET
- **Parameters**: 
  - `pageSize` (number of devices per page)
  - `page` (page number)
  - `sortProperty` (sort by property)
  - `sortOrder` (ASC/DESC)

### 3. TELEMETRY KEYS API
- **Endpoint**: `/plugins/telemetry/DEVICE/{device_id}/keys/timeseries`
- **Method**: GET
- **Purpose**: Discover available telemetry keys for a device

## Energy-Related Telemetry Keys

### Common Energy Keys
- `energy_consumption` - Total energy consumption
- `power_consumption` - Current power consumption
- `electricity_usage` - Electricity usage
- `kwh` - Kilowatt-hours
- `voltage` - Voltage readings
- `current` - Current readings
- `power_factor` - Power factor
- `energy_efficiency` - Energy efficiency metrics

### HVAC Energy Keys
- `hvac_energy` - HVAC energy consumption
- `cooling_energy` - Cooling system energy
- `heating_energy` - Heating system energy
- `fan_energy` - Fan energy consumption

### Lighting Energy Keys
- `lighting_energy` - Lighting energy consumption
- `led_energy` - LED energy usage
- `lighting_power` - Lighting power consumption

## How to Find Energy Consumption

### Step 1: Discover Available Devices
```python
# Get all devices
devices_response = requests.get(
    "https://cloud.inferrix.com/api/deviceInfos/all",
    headers={"Authorization": f"Bearer {token}"}
)
devices = devices_response.json()
```

### Step 2: Find Devices by Location
```python
# Filter devices by location
location_devices = []
for device in devices:
    if "Room 50" in device.get('name', '') or "2nd floor" in device.get('name', ''):
        location_devices.append(device)
```

### Step 3: Get Available Telemetry Keys
```python
# Get available telemetry keys for a device
device_id = "4505c680-4c26-11f0-816d-85352a7c91ff"
keys_response = requests.get(
    f"https://cloud.inferrix.com/api/plugins/telemetry/DEVICE/{device_id}/keys/timeseries",
    headers={"Authorization": f"Bearer {token}"}
)
available_keys = keys_response.json()
```

### Step 4: Get Energy Consumption Data
```python
# Get energy consumption data
energy_response = requests.get(
    f"https://cloud.inferrix.com/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries",
    params={
        "keys": "energy_consumption,power_consumption,kwh",
        "startTs": start_timestamp,
        "endTs": end_timestamp,
        "limit": 100
    },
    headers={"Authorization": f"Bearer {token}"}
)
energy_data = energy_response.json()
```

## Example Queries for Energy Consumption

### 1. Get Energy Consumption for a Specific Device
```python
def get_device_energy_consumption(device_id, start_time=None, end_time=None):
    """
    Get energy consumption for a specific device
    """
    params = {
        "keys": "energy_consumption,power_consumption,kwh,voltage,current"
    }
    
    if start_time:
        params["startTs"] = start_time
    if end_time:
        params["endTs"] = end_time
    
    response = requests.get(
        f"https://cloud.inferrix.com/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries",
        params=params,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    return response.json()
```

### 2. Get Energy Consumption for a Location
```python
def get_location_energy_consumption(location_name):
    """
    Get energy consumption for all devices in a location
    """
    # First, find all devices in the location
    devices = get_devices_by_location(location_name)
    
    total_energy = 0
    energy_data = {}
    
    for device in devices:
        device_id = device.get('id', {}).get('id') if isinstance(device.get('id'), dict) else device.get('id')
        
        # Get energy consumption for this device
        device_energy = get_device_energy_consumption(device_id)
        
        if device_energy:
            energy_data[device.get('name')] = device_energy
            # Sum up total energy if available
            for reading in device_energy:
                if 'energy_consumption' in reading:
                    total_energy += float(reading['energy_consumption'])
    
    return {
        'location': location_name,
        'total_energy': total_energy,
        'device_energy': energy_data
    }
```

### 3. Get Historical Energy Consumption
```python
def get_historical_energy_consumption(device_id, days=30):
    """
    Get historical energy consumption for the last N days
    """
    end_time = int(time.time() * 1000)  # Current time in milliseconds
    start_time = end_time - (days * 24 * 60 * 60 * 1000)  # N days ago
    
    return get_device_energy_consumption(device_id, start_time, end_time)
```

## Energy Consumption Analysis

### 1. Real-time Energy Monitoring
- Monitor current power consumption
- Track energy efficiency
- Detect energy anomalies

### 2. Historical Energy Analysis
- Analyze energy consumption trends
- Identify peak usage periods
- Calculate energy costs

### 3. Energy Optimization
- Identify energy-intensive devices
- Optimize HVAC settings
- Implement energy-saving measures

## Example Usage Scenarios

### Scenario 1: Room Energy Consumption
```python
# Get energy consumption for Room 50
room_energy = get_location_energy_consumption("Room 50 2nd floor")
print(f"Total energy consumption for Room 50: {room_energy['total_energy']} kWh")
```

### Scenario 2: Device-Specific Energy
```python
# Get energy consumption for a specific thermostat
thermostat_energy = get_device_energy_consumption("4505c680-4c26-11f0-816d-85352a7c91ff")
print(f"Thermostat energy consumption: {thermostat_energy}")
```

### Scenario 3: Historical Analysis
```python
# Get last 7 days of energy consumption
weekly_energy = get_historical_energy_consumption("4505c680-4c26-11f0-816d-85352a7c91ff", 7)
print(f"Weekly energy consumption: {weekly_energy}")
```

## Energy Consumption Metrics

### Key Metrics to Track
1. **Total Energy Consumption** (kWh)
2. **Peak Power Demand** (kW)
3. **Energy Efficiency Ratio**
4. **Cost per kWh**
5. **Energy Usage Patterns**

### Energy Efficiency Indicators
- **Power Factor**: Should be close to 1.0
- **Energy Intensity**: kWh per square foot
- **Peak Demand**: Maximum power usage
- **Load Factor**: Average load vs peak load

## Integration with AI Agent

The Inferrix AI Agent can be enhanced to:
1. **Automatically detect energy anomalies**
2. **Provide energy consumption reports**
3. **Suggest energy optimization strategies**
4. **Monitor energy efficiency trends**
5. **Alert on high energy consumption**

## API Response Format

### Telemetry Data Response
```json
{
  "deviceId": "4505c680-4c26-11f0-816d-85352a7c91ff",
  "values": [
    {
      "ts": 1754282872000,
      "value": "25.5",
      "key": "energy_consumption"
    },
    {
      "ts": 1754282872000,
      "value": "2.1",
      "key": "power_consumption"
    }
  ]
}
```

### Device Information Response
```json
{
  "id": {
    "id": "4505c680-4c26-11f0-816d-85352a7c91ff",
    "entityType": "DEVICE"
  },
  "name": "2F-Room50-Thermostat",
  "type": "Thermostat",
  "location": "Second Floor Room No. 50"
}
```

## Best Practices

1. **Regular Monitoring**: Check energy consumption daily/weekly
2. **Historical Analysis**: Compare current vs historical data
3. **Anomaly Detection**: Set up alerts for unusual energy usage
4. **Optimization**: Use data to optimize energy efficiency
5. **Reporting**: Generate regular energy consumption reports

## Troubleshooting

### Common Issues
1. **No Energy Data**: Check if energy telemetry keys are available
2. **Authentication Errors**: Verify API token is valid
3. **Device Not Found**: Ensure device ID is correct
4. **No Historical Data**: Check date range parameters

### Debugging Steps
1. Verify device exists using device discovery API
2. Check available telemetry keys for the device
3. Test with a known working device ID
4. Verify API token permissions

This guide provides a comprehensive approach to finding and analyzing energy consumption data using the available Inferrix APIs. 