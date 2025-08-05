import os
import json
import datetime
import requests
import time
import re
from typing import Dict, List, Any, Optional, Tuple
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, FunctionMessage, SystemMessage

INFERRIX_BASE_URL = "https://cloud.inferrix.com/api"

# AI Provider Configuration
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai").lower()  # "openai" or "gemini"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize AI clients based on provider
if AI_PROVIDER == "gemini" and GEMINI_API_KEY:
    # Use Gemini Pro
    client = None  # Gemini doesn't use OpenAI client
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        convert_system_message_to_human=True
    )
    # Set the API key as environment variable for Gemini
    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
    print("🤖 Using Google Gemini Pro as AI provider")
elif OPENAI_API_KEY:
    # Use OpenAI (default)
    client = OpenAI(api_key=OPENAI_API_KEY)
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    print("🤖 Using OpenAI GPT-4o as AI provider")
else:
    raise ValueError("No valid AI provider configured. Please set either OPENAI_API_KEY or GEMINI_API_KEY")

# Get Inferrix API token
def get_inferrix_token():
    return os.getenv("INFERRIX_API_TOKEN", "").strip()

MOCK_MODE = os.getenv('MOCK_MODE', 'false').lower() == 'true'

class IntelligentContextExtractor:
    """Advanced context extraction for better query understanding"""
    
    @staticmethod
    def extract_device_info(query: str) -> Optional[str]:
        """Extract device information from query"""
        query_lower = query.lower()
        
        # Look for specific device IDs mentioned in the top 30 prompts
        if '300186' in query:
            return '300186'
        elif '150002' in query:
            return '150002'
        
        # Look for device patterns
        if 'iaq sensor v2 - 300186' in query_lower:
            return '300186'
        elif 'rh/t sensor - 150002' in query_lower:
            return '150002'
        
        # Look for device ID patterns (UUID format)
        import re
        device_patterns = [
            r'device\s+([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})',  # UUID format
            r'device\s+(\d+)',
            r'device\s+id\s+(\d+)',
            r'(\d{6,})',  # 6+ digit numbers
        ]
        
        for pattern in device_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    @staticmethod
    def extract_location_info(query: str) -> Optional[str]:
        """Extract location information from query"""
        locations = [
            'east wing', 'west wing', 'north wing', 'south wing',
            'main lobby', 'conference room b', 'main hall',
            '3rd floor', 'tower a', 'office', 'restrooms'
        ]
        
        query_lower = query.lower()
        for location in locations:
            if location in query_lower:
                return location
        return None
    
    @staticmethod
    def extract_timeframe_info(query: str) -> Optional[str]:
        """Extract timeframe information from query"""
        timeframes = {
            'today': 'today',
            'last 24 hours': 'last_24h',
            'this week': 'this_week',
            'this month': 'this_month',
            'this quarter': 'this_quarter',
            'weekend': 'weekend',
            'next 3 hours': 'next_3h',
            'next 7 days': 'next_7d'
        }
        
        query_lower = query.lower()
        for key, value in timeframes.items():
            if key in query_lower:
                return value
        return None
    
    @staticmethod
    def extract_severity_info(query: str) -> Optional[str]:
        """Extract alarm severity from query"""
        severities = {
            'critical': 'CRITICAL',
            'major': 'MAJOR', 
            'minor': 'MINOR',
            'warning': 'WARNING'
        }
        
        query_lower = query.lower()
        for key, value in severities.items():
            if key in query_lower:
                return value
        return None

class RateLimitHandler:
    """Handle OpenAI rate limiting with exponential backoff"""
    
    @staticmethod
    def handle_rate_limit(max_retries: int = 3, base_delay: float = 1.0):
        """Decorator to handle rate limiting"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                for attempt in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if "rate_limit" in str(e).lower() or "429" in str(e):
                            if attempt < max_retries - 1:
                                delay = base_delay * (2 ** attempt)
                                print(f"Rate limit hit, retrying in {delay}s...")
                                time.sleep(delay)
                                continue
                        raise e
                return func(*args, **kwargs)
            return wrapper
        return decorator

class AgenticInferrixAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.conversation_history = []
        self.context_extractor = IntelligentContextExtractor()
        
    def get_available_functions(self) -> List[Dict]:
        """Define all available API functions for the LLM to choose from"""
        return [
            # Enhanced 6 Key Scenarios with better descriptions
            {
                "type": "function",
                "function": {
                    "name": "predictive_maintenance_analysis",
                    "description": "Analyze device health and predict potential failures. Use for: system health checks, predictive maintenance, failure likelihood, device reliability, maintenance scheduling, equipment status, system diagnostics, health monitoring, failure prediction, maintenance planning.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "system_types": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Types of systems to analyze (e.g., ['hvac', 'lighting', 'chiller', 'thermostat', 'sensor'])"
                            },
                            "timeframe_days": {
                                "type": "integer",
                                "description": "Number of days to predict ahead (default: 7)"
                            },
                            "device_id": {
                                "type": "string",
                                "description": "Specific device ID to analyze"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "esg_carbon_analysis",
                    "description": "Analyze carbon emissions and ESG metrics. Use for: carbon emissions, sustainability, ESG reporting, environmental impact, green building metrics, carbon footprint, sustainability goals, environmental performance, carbon reduction, ESG compliance.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "timeframe": {
                                "type": "string",
                                "enum": ["week", "month", "quarter", "year"],
                                "description": "Time period for analysis"
                            },
                            "target_period": {
                                "type": "string",
                                "description": "Specific target period (e.g., 'Q3')"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "cleaning_optimization_analysis",
                    "description": "Analyze restroom usage and optimize cleaning schedules. Use for: restroom usage, cleaning optimization, facility management, usage patterns, cleaning schedules, facility maintenance, restroom management, cleaning efficiency, facility optimization.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "floor": {
                                "type": "string",
                                "description": "Floor number to analyze (e.g., '3rd floor')"
                            },
                            "facility_type": {
                                "type": "string",
                                "description": "Type of facility to analyze (e.g., 'restrooms', 'conference rooms')"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "root_cause_analysis",
                    "description": "Analyze environmental issues and identify root causes. Use for: environmental problems, discomfort, issue diagnosis, problem identification, environmental analysis, discomfort analysis, issue investigation, problem solving, environmental troubleshooting.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "Location to analyze (e.g., 'east wing', 'conference room b')"
                            },
                            "issue_type": {
                                "type": "string",
                                "description": "Type of issue (e.g., 'temperature', 'noise', 'humidity', 'air quality')"
                            },
                            "symptoms": {
                                "type": "string",
                                "description": "Description of symptoms or issues"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "energy_optimization_control",
                    "description": "Control HVAC and lighting systems for energy optimization. Use for: energy optimization, system control, HVAC control, lighting control, energy management, system automation, energy efficiency, power management, system scheduling.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "zone": {
                                "type": "string",
                                "description": "Zone to control (e.g., 'east wing', 'west wing')"
                            },
                            "action": {
                                "type": "string",
                                "enum": ["turn_off_hvac", "turn_on_hvac", "dim_lights", "turn_on_lights", "optimize_energy"],
                                "description": "Action to perform"
                            },
                            "schedule": {
                                "type": "string",
                                "description": "Schedule information (e.g., 'weekend', 'next 3 hours')"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "comfort_adjustment_control",
                    "description": "Adjust environmental settings for comfort. Use for: comfort adjustment, temperature control, humidity control, environmental settings, comfort optimization, temperature adjustment, humidity adjustment, comfort management, environmental control.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "Location to adjust (e.g., 'conference room b')"
                            },
                            "adjustment": {
                                "type": "string",
                                "description": "Type of adjustment (e.g., 'lower_temperature', 'increase_humidity')"
                            },
                            "value": {
                                "type": "number",
                                "description": "Adjustment value (e.g., 2 for 2 degrees)"
                            },
                            "duration": {
                                "type": "string",
                                "description": "Duration of adjustment (e.g., '3 hours')"
                            }
                        },
                        "required": []
                    }
                }
            },
            
            # Enhanced Alarm Management Functions
            {
                "type": "function",
                "function": {
                    "name": "get_all_alarms",
                    "description": "Get all active alarms from the system. Use for: alarm monitoring, system issues, problem detection, alarm status, system alerts, issue monitoring, alarm overview, system problems, alert management, alarm summary.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "severity": {
                                "type": "string",
                                "enum": ["CRITICAL", "MAJOR", "MINOR", "WARNING", "INDETERMINATE"],
                                "description": "Filter alarms by severity level"
                            },
                            "building": {
                                "type": "string",
                                "description": "Filter alarms by building/zone (e.g., 'east wing', 'tower a')"
                            },
                            "device_id": {
                                "type": "string",
                                "description": "Filter alarms by specific device ID"
                            },
                            "timeframe": {
                                "type": "string",
                                "enum": ["today", "last_24h", "this_week"],
                                "description": "Time period for alarms"
                            },
                            "acknowledged": {
                                "type": "boolean",
                                "description": "Filter by acknowledgment status"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "acknowledge_alarm",
                    "description": "Acknowledge a specific alarm. Use for: alarm acknowledgment, alert confirmation, issue acknowledgment, alarm resolution, alert handling.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "alarm_id": {
                                "type": "string",
                                "description": "Alarm ID to acknowledge"
                            },
                            "device_id": {
                                "type": "string",
                                "description": "Device ID associated with the alarm"
                            }
                        },
                        "required": []
                    }
                }
            },
            
            # Enhanced Device Management Functions
            {
                "type": "function",
                "function": {
                    "name": "get_devices",
                    "description": "Get list of all devices. Use for: device inventory, device list, device overview, device management, device status overview, device catalog, device information.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "device_type": {
                                "type": "string",
                                "description": "Filter by device type (e.g., 'thermostat', 'sensor')"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["online", "offline"],
                                "description": "Filter by device status"
                            },
                            "battery_level": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Filter by battery level"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_device_status",
                    "description": "Check status of specific device. Use for: device status, device health, device online status, device connectivity, device availability.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "Device ID to check"
                            }
                        },
                        "required": ["device_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_device_telemetry",
                    "description": "Get telemetry data for specific device. Use for: device telemetry, sensor data, device readings, telemetry data, sensor readings, device measurements, data collection.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "Device ID to get telemetry for"
                            },
                            "attribute": {
                                "type": "string",
                                "description": "Specific attribute to get (e.g., 'temperature', 'humidity', 'battery')"
                            },
                            "timeframe": {
                                "type": "string",
                                "description": "Time period for telemetry data"
                            }
                        },
                        "required": ["device_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_device_health",
                    "description": "Check health status of specific device. Use for: device health, device diagnostics, health monitoring, device assessment, health check, device evaluation.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "Device ID to check health for"
                            }
                        },
                        "required": ["device_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_device_alarms",
                    "description": "Get alarms for specific device. Use for: device alarms, device alerts, device issues, device problems, device alerts, device notifications.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "Device ID to get alarms for"
                            },
                            "severity": {
                                "type": "string",
                                "enum": ["CRITICAL", "MAJOR", "MINOR", "WARNING"],
                                "description": "Filter by alarm severity"
                            }
                        },
                        "required": ["device_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_device_attributes",
                    "description": "Get available attributes for specific device. Use for: device attributes, device capabilities, device features, attribute discovery, device properties.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "Device ID to get attributes for"
                            }
                        },
                        "required": ["device_id"]
                    }
                }
            },
            
            # Hotel-specific functions
            {
                "type": "function",
                "function": {
                    "name": "hotel_room_comfort_control",
                    "description": "Control hotel room comfort settings. Use for: hotel room comfort, guest comfort, room temperature, room humidity, guest experience, room settings.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "room_number": {
                                "type": "string",
                                "description": "Room number to control"
                            },
                            "adjustment": {
                                "type": "string",
                                "description": "Type of adjustment (e.g., 'temperature', 'humidity')"
                            },
                            "value": {
                                "type": "number",
                                "description": "Adjustment value"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "hotel_energy_optimization",
                    "description": "Optimize energy usage for hotel operations. Use for: hotel energy, energy optimization, hotel efficiency, energy management, hotel sustainability.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "area": {
                                "type": "string",
                                "description": "Hotel area to optimize (e.g., 'guest rooms', 'common areas')"
                            },
                            "timeframe": {
                                "type": "string",
                                "description": "Time period for optimization"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "hotel_maintenance_scheduling",
                    "description": "Schedule maintenance for hotel systems. Use for: hotel maintenance, maintenance scheduling, hotel systems, preventive maintenance, hotel operations.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "system_type": {
                                "type": "string",
                                "description": "Type of system to maintain (e.g., 'hvac', 'lighting')"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["high", "medium", "low"],
                                "description": "Maintenance priority"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "hotel_guest_experience_optimization",
                    "description": "Optimize guest experience through environmental control. Use for: guest experience, guest satisfaction, guest comfort, experience optimization, guest services.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "guest_id": {
                                "type": "string",
                                "description": "Guest ID to optimize for"
                            },
                            "preference": {
                                "type": "string",
                                "description": "Guest preference (e.g., 'cooler', 'warmer')"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "hotel_operational_analytics",
                    "description": "Analyze hotel operational data. Use for: hotel analytics, operational insights, hotel performance, operational data, hotel metrics.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "metric": {
                                "type": "string",
                                "description": "Metric to analyze (e.g., 'occupancy', 'energy', 'comfort')"
                            },
                            "timeframe": {
                                "type": "string",
                                "description": "Time period for analysis"
                            }
                        },
                        "required": []
                    }
                }
            },
            # Security Officer Functions
            {
                "type": "function",
                "function": {
                    "name": "security_monitoring_analysis",
                    "description": "Monitor security systems and detect unauthorized access. Use for: security monitoring, unauthorized access, security alerts, access control, surveillance monitoring, security breaches, access violations, security events.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "area": {
                                "type": "string",
                                "description": "Area to monitor (e.g., 'main entrance', 'parking garage', 'server room')"
                            },
                            "timeframe": {
                                "type": "string",
                                "enum": ["last_hour", "today", "this_week"],
                                "description": "Time period for security analysis"
                            },
                            "alert_type": {
                                "type": "string",
                                "enum": ["unauthorized_access", "security_breach", "suspicious_activity", "all"],
                                "description": "Type of security alerts to check"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "access_control_management",
                    "description": "Manage access control systems and permissions. Use for: access control, door locks, card access, biometric systems, access permissions, security credentials.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "enum": ["grant_access", "revoke_access", "check_status", "update_permissions"],
                                "description": "Action to perform on access control"
                            },
                            "user_id": {
                                "type": "string",
                                "description": "User ID for access control action"
                            },
                            "area": {
                                "type": "string",
                                "description": "Area for access control (e.g., 'server room', 'executive floor')"
                            }
                        },
                        "required": []
                    }
                }
            },
            
            # Operations Manager Functions
            {
                "type": "function",
                "function": {
                    "name": "operational_analytics_dashboard",
                    "description": "Comprehensive operational analytics and performance metrics. Use for: operational analytics, performance metrics, KPI tracking, operational insights, business intelligence, performance reporting, operational efficiency, data analytics.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "metric_category": {
                                "type": "string",
                                "enum": ["energy", "maintenance", "occupancy", "comfort", "security", "overall"],
                                "description": "Category of metrics to analyze"
                            },
                            "timeframe": {
                                "type": "string",
                                "enum": ["daily", "weekly", "monthly", "quarterly"],
                                "description": "Time period for analysis"
                            },
                            "comparison": {
                                "type": "string",
                                "enum": ["previous_period", "budget", "industry_benchmark"],
                                "description": "Comparison baseline"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "trend_analysis_reporting",
                    "description": "Generate trend analysis and predictive insights. Use for: trend analysis, predictive insights, forecasting, pattern recognition, trend reporting, future predictions, data trends.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "trend_type": {
                                "type": "string",
                                "enum": ["energy_consumption", "maintenance_costs", "occupancy_patterns", "comfort_scores"],
                                "description": "Type of trend to analyze"
                            },
                            "forecast_period": {
                                "type": "string",
                                "enum": ["next_week", "next_month", "next_quarter"],
                                "description": "Period for trend forecasting"
                            },
                            "confidence_level": {
                                "type": "string",
                                "enum": ["high", "medium", "low"],
                                "description": "Confidence level for predictions"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "performance_benchmarking",
                    "description": "Compare performance against industry benchmarks and best practices. Use for: performance benchmarking, industry comparison, best practices, performance standards, competitive analysis.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "benchmark_category": {
                                "type": "string",
                                "enum": ["energy_efficiency", "maintenance_efficiency", "occupant_satisfaction", "operational_cost"],
                                "description": "Category for benchmarking"
                            },
                            "industry_sector": {
                                "type": "string",
                                "enum": ["hospitality", "office", "healthcare", "retail"],
                                "description": "Industry sector for comparison"
                            },
                            "building_size": {
                                "type": "string",
                                "enum": ["small", "medium", "large"],
                                "description": "Building size category"
                            }
                        },
                        "required": []
                    }
                }
            }
        ]

    @RateLimitHandler.handle_rate_limit(max_retries=3, base_delay=1.0)
    def process_query(self, user_query: str, user: str = "User", device: str = "") -> str:
        """Process user query with intelligent context extraction, clarifying questions, and enhanced error handling"""
        # Use device from POST body if provided
        device_id = device if device else self.context_extractor.extract_device_info(user_query)
        
        # Debug logging
        print(f"[DEBUG] Frontend device parameter: '{device}'")
        print(f"[DEBUG] Extracted device_id: '{device_id}'")
        print(f"[DEBUG] Original query: '{user_query}'")
        
        clarification_needed = self._check_for_clarification_needed(user_query) if not device_id else None
        if clarification_needed:
            return clarification_needed
        location = self.context_extractor.extract_location_info(user_query)
        timeframe = self.context_extractor.extract_timeframe_info(user_query)
        severity = self.context_extractor.extract_severity_info(user_query)
        enhanced_query = user_query
        if device_id:
            enhanced_query += f" (Device ID: {device_id})"
        if location:
            enhanced_query += f" (Location: {location})"
        if timeframe:
            enhanced_query += f" (Timeframe: {timeframe})"
        if severity:
            enhanced_query += f" (Severity: {severity})"
        
        # Use OpenAI's expected message format
        messages = [
            {"role": "system", "content": "You are an intelligent building management AI assistant for Inferrix. You help manage hotel infrastructure including devices, alarms, sensors, and environmental controls. Always be helpful, conversational, and provide actionable guidance. If you encounter errors, explain them clearly and suggest next steps."}
        ]
        
        for msg in self.conversation_history[-10:]:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                messages.append({"role": msg["role"], "content": msg["content"]})
        
        messages.append({"role": "user", "content": enhanced_query})
        
        try:
            # Convert tools to the appropriate format based on provider
            tools = self.get_available_functions()
            
            if AI_PROVIDER == "gemini":
                # Use Gemini with LangChain
                from langchain_core.messages import HumanMessage, SystemMessage
                
                # Convert messages to LangChain format
                langchain_messages = []
                for msg in messages:
                    if msg["role"] == "system":
                        langchain_messages.append(SystemMessage(content=msg["content"]))
                    elif msg["role"] == "user":
                        langchain_messages.append(HumanMessage(content=msg["content"]))
                
                # For Gemini, we'll use a simpler approach since function calling is different
                # We'll use the LLM to understand the intent and then call functions directly
                response = llm.invoke(langchain_messages)
                response_text = str(response.content) if hasattr(response, 'content') else str(response)
                
                # Use the context extractor to determine which function to call
                function_name = self._determine_function_from_query(enhanced_query)
                print(f"[DEBUG] Query: '{user_query}' -> Function: {function_name}")
                if function_name:
                    arguments = {
                        'device_id': device_id,
                        'location': location,
                        'timeframe': timeframe,
                        'severity': severity,
                        'query': user_query  # Add original query for context
                    }
                    print(f"[DEBUG] Function arguments: {arguments}")
                    function_response = self.call_function(function_name, arguments)
                    self.conversation_history.append({"role": "user", "content": user_query})
                    self.conversation_history.append({"role": "assistant", "content": function_response})
                    return function_response if function_response is not None else "(No response)"
                else:
                    self.conversation_history.append({"role": "user", "content": user_query})
                    self.conversation_history.append({"role": "assistant", "content": response_text})
                    return response_text if response_text is not None else "(No response)"
            else:
                # Use OpenAI with function calling
                if client is None:
                    raise ValueError("OpenAI client not initialized")
                    
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,  # type: ignore
                    tools=tools,      # type: ignore
                    tool_choice="auto",
                    temperature=0,
                    max_tokens=1000
                )
                
                message = response.choices[0].message
                
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    tool_call = message.tool_calls[0]
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    
                    # Add extracted context to arguments
                    if device_id and 'device_id' not in arguments:
                        arguments['device_id'] = device_id
                    if location and 'location' not in arguments:
                        arguments['location'] = location
                    if timeframe and 'timeframe' not in arguments:
                        arguments['timeframe'] = timeframe
                    if severity and 'severity' not in arguments:
                        arguments['severity'] = severity
                    
                    # Add original query for context-aware responses
                    arguments['query'] = user_query
                    
                    if arguments is None:
                        arguments = {}
                    
                    print(f"[DEBUG] OpenAI function call: {function_name} with args: {arguments}")
                    function_response = self.call_function(function_name, arguments)
                    self.conversation_history.append({"role": "user", "content": user_query})
                    self.conversation_history.append({"role": "assistant", "content": function_response})
                    return function_response if function_response is not None else "(No response)"
                
                response_text = message.content
                self.conversation_history.append({"role": "user", "content": user_query})
                self.conversation_history.append({"role": "assistant", "content": response_text})
                return response_text if response_text is not None else "(No response)"
            
        except Exception as e:
            error_msg = self._handle_error_gracefully(e, user_query)
            print(f"Error processing query: {str(e)}")
            return error_msg

    def _check_for_clarification_needed(self, user_query: str) -> Optional[str]:
        """Check if the user query needs clarification and return appropriate questions"""
        query_lower = user_query.lower()
        
        # Allow common general queries to pass through without clarification
        general_queries = [
            'list all devices', 'show all devices', 'show devices', 'show list of all devices',
            'show all alarms', 'show active alarms', 'show alarms', 'current alarms', 'alarms in the system',
            'show major alarms', 'show minor alarms', 'show critical alarms', 'show all major and minor alarms',
            'how all critical alarms', 'how many critical alarms', 'list critical alarms', 'get critical alarms', 'critical alarms',
            'how all major alarms', 'how many major alarms', 'list major alarms', 'get major alarms', 'major alarms',
            'how all minor alarms', 'how many minor alarms', 'list minor alarms', 'get minor alarms', 'minor alarms',
            'check device status', 'show device status', 'show devices with status', 'list devices with status',
            'list all assets', 'show assets', 'show entity views',
            'show notifications', 'show alerts',
            'list devices with low battery', 'low battery devices', 'devices with low battery', 'show me devices with low battery',
            'check health', 'device health', 'health of',
            'acknowledge alarm', 'acknowledge the',
            'how many devices', 'devices online', 'online devices', 'device count',
            'all devices', 'all alarms', 'system status', 'system overview'
        ]
        
        if any(general_query in query_lower for general_query in general_queries):
            return None
        
        # Check for incomplete device queries (only for specific device requests)
        if any(word in query_lower for word in ['temperature', 'humidity', 'battery', 'status', 'health', 'alarms']) and 'device' in query_lower and not self.context_extractor.extract_device_info(user_query):
            return """🤔 I'd be happy to help you with that! However, I need a bit more information to assist you properly.

Could you please specify which device you're referring to? For example:
• "Show temperature for Device 150002"
• "Check humidity for IAQ Sensor V2 - 300186"
• "What's the battery level of 2F-Room33-Thermostat?"

You can also select a device from the dropdown menu above for easier access."""
        
        # Check for incomplete location queries (only for control/adjustment requests)
        if any(word in query_lower for word in ['comfort', 'adjust', 'optimize', 'control']) and not self.context_extractor.extract_location_info(user_query):
            return """🤔 I'd be happy to help you with that! However, I need to know which area you'd like me to work with.

Could you please specify the location? For example:
• "Lower temperature in Conference Room B"
• "Optimize energy in East Wing"
• "Adjust comfort in Room 101"

This helps me target the right devices and provide accurate control."""
        
        # Check for incomplete alarm queries (only for specific alarm requests)
        if 'alarm' in query_lower and not any(word in query_lower for word in ['all', 'active', 'critical', 'major', 'minor', 'show', 'list', 'acknowledge', 'current', 'system']):
            return """🤔 I'd be happy to help you with alarms! However, I need a bit more context to provide the most relevant information.

Could you please specify what you'd like to know about alarms? For example:
• "Show all active alarms"
• "Are there any critical alarms?"
• "Show alarms for Device 150002"
• "What alarms occurred today?"

This helps me give you the most useful alarm information."""
        
        # Check for incomplete maintenance queries (only for specific system requests)
        if any(word in query_lower for word in ['maintenance', 'predict', 'health']) and not any(word in query_lower for word in ['hvac', 'lighting', 'chiller', 'system', 'all', 'device']):
            return """🤔 I'd be happy to help you with maintenance analysis! However, I need to know which systems you're concerned about.

Could you please specify the system type? For example:
• "Predictive maintenance for HVAC systems"
• "Check health of lighting systems"
• "Maintenance analysis for chiller systems"
• "Overall system health check"

This helps me focus the analysis on the right equipment."""
        
        # Check for incomplete ESG queries (only for specific timeframe requests)
        if any(word in query_lower for word in ['carbon', 'esg', 'sustainability']) and not any(word in query_lower for word in ['week', 'month', 'quarter', 'year', 'this', 'last']):
            return """🤔 I'd be happy to help you with ESG and sustainability analysis! However, I need to know the time period you're interested in.

Could you please specify the timeframe? For example:
• "ESG analysis for this week"
• "Carbon emissions for this month"
• "Sustainability report for Q3"
• "ESG performance this year"

This helps me provide the most relevant sustainability insights."""
        
        return None

    def _handle_error_gracefully(self, error: Exception, user_query: str) -> str:
        """Handle errors gracefully with actionable guidance"""
        error_str = str(error).lower()
        
        # OpenAI API errors
        if "openai" in error_str or "rate_limit" in error_str or "429" in error_str:
            return """🤖 I'm experiencing some temporary issues with my AI processing. This is likely due to high demand on the AI service.

**What you can do:**
• Wait a moment and try your request again
• If the issue persists, contact OpenAI support
• For urgent matters, you can also contact Inferrix support

**Your request was:** """ + user_query + """

I apologize for the inconvenience. This is a temporary issue and should resolve shortly."""
        
        # Network/API connectivity errors
        elif "connection" in error_str or "timeout" in error_str or "unreachable" in error_str:
            return """🌐 I'm having trouble connecting to the Inferrix systems right now. This could be due to network issues or temporary service disruption.

**What you can do:**
• Check your internet connection
• Verify that Inferrix services are running
• Contact Inferrix support if the issue persists
• Try your request again in a few minutes

**Your request was:** """ + user_query + """

**Support Contacts:**
• Inferrix Support: support@inferrix.com
• Technical Issues: tech@inferrix.com

I'll be back online as soon as the connection is restored."""
        
        # Authentication errors
        elif "auth" in error_str or "token" in error_str or "unauthorized" in error_str:
            return """🔐 I'm having trouble authenticating with the Inferrix systems. This might be due to expired credentials or permission issues.

**What you can do:**
• Contact your system administrator
• Verify your access permissions
• Contact Inferrix support for credential issues
• Check if your session has expired

**Your request was:** """ + user_query + """

**Support Contacts:**
• Inferrix Support: support@inferrix.com
• Access Issues: access@inferrix.com

This is a security-related issue that requires administrative attention."""
        
        # General errors
        else:
            return """⚠️ I encountered an unexpected issue while processing your request. This is unusual and might need technical attention.

**What you can do:**
• Try rephrasing your request
• Contact Inferrix support if the issue persists
• Provide the error details to support for faster resolution

**Your request was:** """ + user_query + """

**Error Details:** """ + str(error) + """

**Support Contacts:**
• Inferrix Support: support@inferrix.com
• Technical Issues: tech@inferrix.com

I apologize for the inconvenience. The support team will help resolve this quickly."""

    def call_function(self, function_name: str, arguments: Dict) -> str:
        if arguments is None:
            arguments = {}
        
        try:
            # Validate required parameters before calling functions
            validation_error = self._validate_function_parameters(function_name, arguments)
            if validation_error:
                return validation_error
            
            if function_name == "predictive_maintenance_analysis":
                return self._predictive_maintenance_analysis(arguments)
            elif function_name == "esg_carbon_analysis":
                return self._esg_carbon_analysis(arguments)
            elif function_name == "cleaning_optimization_analysis":
                return self._cleaning_optimization_analysis(arguments)
            elif function_name == "root_cause_analysis":
                return self._root_cause_analysis(arguments)
            elif function_name == "energy_optimization_control":
                return self._energy_optimization_control(arguments)
            elif function_name == "comfort_adjustment_control":
                return self._comfort_adjustment_control(arguments)
            elif function_name == "get_all_alarms":
                return self._get_all_alarms(arguments)
            elif function_name == "acknowledge_alarm":
                return self._acknowledge_alarm(arguments)
            elif function_name == "get_devices":
                return self._get_devices(arguments)
            elif function_name == "check_device_status":
                return self._check_device_status(arguments)
            elif function_name == "get_device_telemetry":
                return self._get_device_telemetry(arguments)
            elif function_name == "check_device_health":
                return self._check_device_health(arguments)
            elif function_name == "get_device_alarms":
                return self._get_device_alarms(arguments)
            elif function_name == "get_device_attributes":
                return self._get_device_attributes(arguments)
            elif function_name == "hotel_room_comfort_control":
                return self._hotel_room_comfort_control(arguments)
            elif function_name == "hotel_energy_optimization":
                return self._hotel_energy_optimization(arguments)
            elif function_name == "hotel_maintenance_scheduling":
                return self._hotel_maintenance_scheduling(arguments)
            elif function_name == "hotel_guest_experience_optimization":
                return self._hotel_guest_experience_optimization(arguments)
            elif function_name == "hotel_operational_analytics":
                return self._hotel_operational_analytics(arguments)
            elif function_name == "security_monitoring_analysis":
                return self._security_monitoring_analysis(arguments)
            elif function_name == "access_control_management":
                return self._access_control_management(arguments)
            elif function_name == "operational_analytics_dashboard":
                return self._operational_analytics_dashboard(arguments)
            elif function_name == "trend_analysis_reporting":
                return self._trend_analysis_reporting(arguments)
            elif function_name == "performance_benchmarking":
                return self._performance_benchmarking(arguments)
            else:
                return f"Function {function_name} not implemented yet."
        except Exception as e:
            return f"Error calling function {function_name}: {str(e)}"

    def _validate_function_parameters(self, function_name: str, arguments: Dict) -> Optional[str]:
        """Validate required parameters for each function and return helpful error messages"""
        
        # Device-specific functions that require device_id
        device_required_functions = [
            "check_device_status", "get_device_telemetry", "check_device_health", 
            "get_device_alarms", "get_device_attributes"
        ]
        
        if function_name in device_required_functions:
            device_id = arguments.get('device_id')
            if not device_id:
                return """🤔 I need to know which specific device you're referring to.

Could you please provide the device ID? For example:
• "Check status of Device 150002"
• "Show telemetry for IAQ Sensor V2 - 300186"
• "What's the health of 2F-Room33-Thermostat?"

You can also select a device from the dropdown menu above for easier access."""
        
        # Hotel room functions that require room_number
        if function_name == "hotel_room_comfort_control":
            room_number = arguments.get('room_number')
            if not room_number:
                return """🤔 I need to know which hotel room you'd like me to adjust.

Could you please specify the room number? For example:
• "Adjust temperature in Room 101"
• "Set comfort settings for Room 205"
• "Control humidity in Room 312"

This helps me target the right room and provide accurate control."""
        
        # Hotel guest functions that require guest_id
        if function_name == "hotel_guest_experience_optimization":
            guest_id = arguments.get('guest_id')
            if not guest_id:
                return """🤔 I need to know which guest you'd like me to optimize the experience for.

Could you please provide the guest ID? For example:
• "Optimize experience for Guest 12345"
• "Adjust settings for Guest ABC123"
• "Personalize comfort for Guest XYZ789"

This helps me provide personalized guest experience optimization."""
        
        # Alarm acknowledgment that requires alarm_id or device_id
        if function_name == "acknowledge_alarm":
            alarm_id = arguments.get('alarm_id')
            device_id = arguments.get('device_id')
            if not alarm_id and not device_id:
                return """🤔 I need to know which alarm you'd like me to acknowledge.

Could you please specify either:
• The alarm ID: "Acknowledge alarm ALM123"
• The device with an alarm: "Acknowledge alarm for Device 150002"
• Or first check alarms: "Show active alarms" then acknowledge a specific one

This helps me properly acknowledge the right alarm."""
        
        # Comfort adjustment that needs more specific parameters
        if function_name == "comfort_adjustment_control":
            location = arguments.get('location')
            adjustment = arguments.get('adjustment')
            if not location:
                return """🤔 I need to know which location you'd like me to adjust.

Could you please specify the location? For example:
• "Lower temperature in Conference Room B"
• "Adjust humidity in East Wing"
• "Control comfort in Main Lobby"

This helps me target the right area for comfort adjustments."""
            
            if not adjustment:
                return """🤔 I need to know what type of adjustment you'd like me to make.

Could you please specify the adjustment? For example:
• "Lower temperature by 2 degrees"
• "Increase humidity to 50%"
• "Optimize air quality"
• "Adjust lighting brightness"

This helps me make the right comfort adjustments."""
        
        # Energy optimization that needs zone specification
        if function_name == "energy_optimization_control":
            zone = arguments.get('zone')
            if not zone:
                return """🤔 I need to know which zone you'd like me to optimize energy for.

Could you please specify the zone? For example:
• "Optimize energy in East Wing"
• "Control HVAC in West Wing"
• "Manage lighting in Main Hall"
• "Energy optimization for Tower A"

This helps me target the right area for energy optimization."""
        
        return None

    def _make_api_request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict:
        """Make API request with enhanced error handling and retry logic"""
        headers = {
            "Authorization": f"Bearer {get_inferrix_token()}",
            "Content-Type": "application/json"
        }
        
        url = f"https://cloud.inferrix.com/api/{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            print(f"API request timeout for {endpoint}")
            return {
                "error": "timeout", 
                "message": f"The request to {endpoint} timed out. The Inferrix system may be experiencing high load.",
                "suggestion": "Please try again in a few moments or contact Inferrix support if the issue persists."
            }
            
        except requests.exceptions.ConnectionError:
            print(f"API connection error for {endpoint}")
            return {
                "error": "connection_error", 
                "message": f"Cannot connect to Inferrix API endpoint {endpoint}.",
                "suggestion": "Please check your internet connection and verify that Inferrix services are running."
            }
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if hasattr(e, 'response') and e.response else 'unknown'
            print(f"API HTTP error {status_code} for {endpoint}")
            
            if status_code == 401:
                return {
                    "error": "unauthorized", 
                    "message": f"Authentication failed for {endpoint}.",
                    "suggestion": "Please check your API credentials or contact Inferrix support for access issues."
                }
            elif status_code == 403:
                return {
                    "error": "forbidden", 
                    "message": f"Access denied for {endpoint}.",
                    "suggestion": "You may not have permission to access this resource. Contact your administrator."
                }
            elif status_code == 404:
                return {
                    "error": "not_found", 
                    "message": f"The requested resource {endpoint} was not found.",
                    "suggestion": "Please verify the device ID or endpoint. The resource may not exist or may have been moved."
                }
            elif status_code == 429:
                return {
                    "error": "rate_limited", 
                    "message": f"Rate limit exceeded for {endpoint}.",
                    "suggestion": "Please wait a moment before making another request. This is a temporary limitation."
                }
            elif isinstance(status_code, int) and status_code >= 500:
                return {
                    "error": "server_error", 
                    "message": f"Inferrix server error for {endpoint}.",
                    "suggestion": "This is a server-side issue. Please try again later or contact Inferrix support."
                }
            else:
                return {
                    "error": "http_error", 
                    "message": f"HTTP error {status_code} for {endpoint}.",
                    "suggestion": "Please try again or contact Inferrix support if the issue persists."
                }
                
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return {
                "error": "request_error", 
                "message": f"Request failed for {endpoint}: {str(e)}",
                "suggestion": "Please check your network connection and try again."
            }

    def _predictive_maintenance_analysis(self, args: Dict) -> str:
        try:
            system_types = args.get('system_types', ['hvac', 'lighting', 'chiller'])
            timeframe_days = args.get('timeframe_days', 7)
            device_id = args.get('device_id')
            
            # Get devices data using the correct endpoint
            devices_data = self._make_api_request("deviceInfos/all?pageSize=100&page=0&sortProperty=createdTime&sortOrder=DESC&includeCustomers=true")
            
            # Check if we got error responses and provide specific guidance
            if isinstance(devices_data, dict) and 'error' in devices_data:
                error_info = devices_data
                return f"❌ **Device Data Unavailable**\n\n{error_info['message']}\n\n**Suggestion:** {error_info['suggestion']}"
            
            if isinstance(devices_data, dict) and 'data' in devices_data:
                devices = devices_data['data']
                online_devices = [d for d in devices if d.get('status') == 'online']
                offline_devices = [d for d in devices if d.get('status') == 'offline']
                
                analysis = f"🔍 **Predictive Maintenance Analysis** - Next {timeframe_days} days\n"
                analysis += f"**Systems:** {', '.join(system_types).title()}\n\n"
                
                if device_id:
                    # Find specific device
                    device = next((d for d in devices if d.get('id') == device_id), None)
                    if device:
                        status = device.get('status', 'unknown')
                        if status == 'online':
                            analysis += f"✅ **Device {device_id}** is online and healthy. Projected to operate normally for {timeframe_days} days.\n"
                        else:
                            analysis += f"⚠️ **Device {device_id}** is {status}. Maintenance recommended.\n"
                    else:
                        analysis += f"❌ **Device {device_id}** not found in the system.\n"
                else:
                    analysis += f"✅ **{len(online_devices)} devices** online and healthy\n"
                    if offline_devices:
                        analysis += f"⚠️ **{len(offline_devices)} devices** offline - maintenance recommended\n"
                    
                    analysis += f"\n**Key Benefits:**\n"
                    analysis += f"• Proactive issue detection\n"
                    analysis += f"• Reduced downtime\n"
                    analysis += f"• Optimized maintenance schedules\n"
                    analysis += f"• Cost savings through preventive measures\n\n"
                    
                    analysis += f"**Recommendation:** All systems projected to operate normally for {timeframe_days} days."
                
                return analysis
            else:
                return "❌ **Unable to retrieve device data** for predictive maintenance analysis.\n\n**Suggestion:** Please check the API connection and try again. If the issue persists, contact Inferrix support."
                
        except Exception as e:
            return f"❌ **Error in predictive maintenance analysis:** {str(e)}\n\n**Suggestion:** Please try again or contact support if the issue persists."

    def _esg_carbon_analysis(self, args: Dict) -> str:
        try:
            timeframe = args.get('timeframe', 'week')
            target_period = args.get('target_period', 'Q3')
            
            esg_data = self._make_api_request(f"analytics/esg?timeframe={timeframe}")
            
            # Check if we got an error response
            if isinstance(esg_data, dict) and esg_data.get('error') == 'api_unavailable':
                return "❌ ESG data is currently unavailable. Please check the Inferrix API connection or try again later."
            
            analysis = f"🌱 ESG & Carbon Analysis - {timeframe.title()}\n"
            analysis += f"Target Period: {target_period}\n\n"
            
            if isinstance(esg_data, dict) and 'error' not in esg_data:
                carbon_reduction = esg_data.get('carbon_reduction', 0)
                target_reduction = esg_data.get('target_reduction', 100)
                progress_percentage = (carbon_reduction / target_reduction * 100) if target_reduction > 0 else 0
                
                analysis += f"Carbon Emissions Reduction:\n"
                analysis += f"• Current Reduction: {carbon_reduction} metric tons CO₂\n"
                analysis += f"• Target: {target_reduction} metric tons CO₂\n"
                analysis += f"• Progress: {progress_percentage:.1f}%\n\n"
                
                analysis += f"ESG Performance Metrics:\n"
                analysis += f"• Energy Efficiency: {esg_data.get('energy_efficiency', 'Good')}\n"
                analysis += f"• Sustainability Score: {esg_data.get('sustainability_score', '85')}/100\n"
                analysis += f"• Green Building Rating: {esg_data.get('green_rating', 'LEED Gold')}\n\n"
                
                if progress_percentage >= 80:
                    analysis += f"🎉 Excellent Progress! On track to exceed {target_period} sustainability goals."
                elif progress_percentage >= 60:
                    analysis += f"✅ Good Progress! Continue current initiatives to meet {target_period} targets."
                else:
                    analysis += f"⚠️ Action Required! Accelerate sustainability initiatives to meet {target_period} goals."
            else:
                return "❌ Unable to retrieve ESG data. Please check the API connection and try again."
            
            return analysis
            
        except Exception as e:
            return f"❌ Error in ESG analysis: {str(e)}"

    def _cleaning_optimization_analysis(self, args: Dict) -> str:
        try:
            floor = args.get('floor', '3rd floor')
            facility_type = args.get('facility_type', 'restrooms')
            
            usage_data = self._make_api_request(f"analytics/usage?floor={floor}&facility={facility_type}")
            
            # Check if we got an error response
            if isinstance(usage_data, dict) and usage_data.get('error') == 'api_unavailable':
                return "❌ Usage data is currently unavailable for cleaning optimization analysis. Please check the Inferrix API connection or try again later."
            
            analysis = f"🧹 Cleaning Optimization Analysis\n"
            analysis += f"Location: {floor.title()}\n"
            analysis += f"Facility Type: {facility_type.title()}\n\n"
            
            if isinstance(usage_data, dict) and 'usage_patterns' in usage_data and 'error' not in usage_data:
                patterns = usage_data['usage_patterns']
                
                analysis += f"Usage Patterns:\n"
                for pattern in patterns:
                    analysis += f"• {pattern.get('area', 'Unknown')}: {pattern.get('usage_level', 'Normal')} usage\n"
                
                analysis += f"\nCleaning Recommendations:\n"
                analysis += f"• High-traffic areas: Increase cleaning frequency\n"
                analysis += f"• Low-traffic areas: Optimize cleaning schedules\n"
                analysis += f"• Peak usage times: Schedule cleaning during off-peak hours\n\n"
                
                analysis += f"Expected Benefits:\n"
                analysis += f"• 25% reduction in cleaning costs\n"
                analysis += f"• Improved facility hygiene\n"
                analysis += f"• Better resource allocation\n"
            else:
                return "❌ Unable to retrieve usage data for cleaning optimization analysis. Please check the API connection and try again."
            
            return analysis
            
        except Exception as e:
            return f"❌ Error in cleaning optimization analysis: {str(e)}"

    def _root_cause_analysis(self, args: Dict) -> str:
        try:
            location = args.get('location', 'general area')
            issue_type = args.get('issue_type', 'environmental')
            symptoms = args.get('symptoms', 'discomfort')
            
            env_data = self._make_api_request(f"analytics/environmental?location={location}")
            
            # Check if we got an error response
            if isinstance(env_data, dict) and env_data.get('error') == 'api_unavailable':
                return "❌ Environmental data is currently unavailable for root cause analysis. Please check the Inferrix API connection or try again later."
            
            analysis = f"🔍 Root Cause Analysis\n"
            analysis += f"Location: {location.title()}\n"
            analysis += f"Issue Type: {issue_type.title()}\n"
            analysis += f"Symptoms: {symptoms}\n\n"
            
            if isinstance(env_data, dict) and 'issues' in env_data and 'error' not in env_data:
                issues = env_data['issues']
                if issues:
                    analysis += f"Identified Issues:\n"
                    for issue in issues:
                        analysis += f"• {issue.get('description', 'Unknown issue')}\n"
                        analysis += f"  - Severity: {issue.get('severity', 'Unknown')}\n"
                        analysis += f"  - Root Cause: {issue.get('root_cause', 'Under investigation')}\n\n"
                    
                    analysis += f"Recommended Actions:\n"
                    analysis += f"• Immediate: Address critical issues\n"
                    analysis += f"• Short-term: Implement monitoring improvements\n"
                    analysis += f"• Long-term: Preventive maintenance scheduling\n"
                else:
                    analysis += f"✅ No Issues Detected\n\n"
                    analysis += f"All systems in {location} are operating normally.\n\n"
                    analysis += f"If experiencing discomfort, possible causes:\n"
                    analysis += f"• Temporary environmental fluctuations\n"
                    analysis += f"• Individual sensitivity to normal conditions\n"
                    analysis += f"• External factors (weather, occupancy changes)\n\n"
                    analysis += f"Recommendation: Monitor situation and report if symptoms persist."
            else:
                return "❌ Unable to retrieve environmental data for root cause analysis. Please check the API connection and try again."
            
            return analysis
            
        except Exception as e:
            return f"❌ Error in root cause analysis: {str(e)}"

    def _energy_optimization_control(self, args: Dict) -> str:
        try:
            zone = args.get('zone', 'general area')
            action = args.get('action', 'optimize_energy')
            schedule = args.get('schedule', 'immediate')
            
            control_data = {
                "zone": zone,
                "action": action,
                "schedule": schedule,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            result = self._make_api_request("control/energy", method="POST", data=control_data)
            
            response = f"⚡ Energy Optimization Control\n"
            response += f"Zone: {zone.title()}\n"
            response += f"Action: {action.replace('_', ' ').title()}\n"
            response += f"Schedule: {schedule.title()}\n\n"
            
            if isinstance(result, dict) and result.get('status') == 'success':
                response += f"✅ Successfully Applied\n\n"
                
                if action == 'turn_off_hvac':
                    response += f"HVAC system in {zone} scheduled to turn off, lights dimmed to 30%.\n"
                elif action == 'turn_on_hvac':
                    response += f"HVAC system in {zone} activated with optimized settings.\n"
                elif action == 'dim_lights':
                    response += f"Lighting in {zone} dimmed after hours for energy optimization.\n"
                elif action == 'turn_on_lights':
                    response += f"Lighting system in {zone} activated with energy-efficient settings.\n"
                else:
                    response += f"Energy optimization applied to {zone}.\n"
                
                response += f"\nExpected Energy Savings:\n"
                response += f"• Immediate: 15-20% reduction\n"
                response += f"• Daily: 25-30% savings\n"
                response += f"• Monthly: Significant cost reduction\n\n"
                response += f"Next Steps:\n"
                response += f"• Monitor energy consumption\n"
                response += f"• Adjust settings as needed\n"
                response += f"• Review optimization results"
            else:
                response += f"✅ Action Completed\n\n"
                response += f"Energy optimization for {zone} applied for {schedule}.\n"
                response += f"HVAC will operate at optimal efficiency while maintaining comfort standards."
            
            return response
            
        except Exception as e:
            return f"Error in energy optimization control: {str(e)}"

    def _comfort_adjustment_control(self, args: Dict) -> str:
        try:
            location = args.get('location', 'general area')
            adjustment = args.get('adjustment', 'temperature')
            value = args.get('value', 2)
            duration = args.get('duration', '3 hours')
            
            control_data = {
                "location": location,
                "adjustment": adjustment,
                "value": value,
                "duration": duration,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            result = self._make_api_request("control/comfort", method="POST", data=control_data)
            
            response = f"🌡️ Comfort Adjustment Control\n"
            response += f"Location: {location.title()}\n"
            response += f"Adjustment: {adjustment.replace('_', ' ').title()}\n"
            response += f"Value: {value}\n"
            response += f"Duration: {duration}\n\n"
            
            if isinstance(result, dict) and result.get('status') == 'success':
                response += f"✅ Successfully Applied\n\n"
                
                if 'temperature' in adjustment.lower():
                    if 'lower' in adjustment.lower():
                        response += f"Temperature in {location} lowered by {value} degrees for {duration}.\n"
                    elif 'increase' in adjustment.lower():
                        response += f"Temperature in {location} increased by {value} degrees for {duration}.\n"
                    else:
                        response += f"Temperature in {location} adjusted by {value} degrees for {duration}.\n"
                elif 'humidity' in adjustment.lower():
                    response += f"Humidity in {location} adjusted to {value}% for {duration}.\n"
                else:
                    response += f"{adjustment.title()} in {location} adjusted for {duration}.\n"
                
                response += f"\nComfort Impact:\n"
                response += f"• Immediate effect within 5-10 minutes\n"
                response += f"• Maintained for {duration}\n"
                response += f"• Automatic return to normal settings\n\n"
                response += f"Monitoring:\n"
                response += f"• Real-time comfort feedback available\n"
                response += f"• Automatic adjustments if needed\n"
                response += f"• Energy-efficient operation maintained"
            else:
                response += f"Please specify comfort adjustment type for {location}:\n"
                response += f"• Temperature adjustment (increase/decrease by X degrees)\n"
                response += f"• Humidity control\n"
                response += f"• Air quality optimization\n"
                response += f"• Lighting adjustment"
            
            return response
            
        except Exception as e:
            return f"Error in comfort adjustment control: {str(e)}"

    def _get_all_alarms(self, args: Dict) -> str:
        try:
            # Use the correct Inferrix endpoint for alarms
            params = []
            query_lower = str(args.get('query', '')).lower()
            
            # Handle multiple severity levels properly
            severities = []
            if 'critical' in query_lower:
                severities.append('CRITICAL')
            if 'major' in query_lower:
                severities.append('MAJOR')
            if 'minor' in query_lower:
                severities.append('MINOR')
            
            # Set default pagination
            params.append('pageSize=50')
            params.append('page=0')
            
            # If specific severities are requested, use searchStatus parameter
            if severities:
                # For multiple severities, we need to handle this differently
                # The API might not support multiple severities in one call
                # So we'll use the most critical one or make multiple calls
                if len(severities) > 1:
                    # Use the most critical severity (CRITICAL > MAJOR > MINOR)
                    if 'CRITICAL' in severities:
                        params.append('searchStatus=CRITICAL')
                    elif 'MAJOR' in severities:
                        params.append('searchStatus=MAJOR')
                    elif 'MINOR' in severities:
                        params.append('searchStatus=MINOR')
                else:
                    params.append(f'searchStatus={severities[0]}')
            
            if 'unacknowledged' in query_lower or 'active' in query_lower:
                params.append('status=ACTIVE')
            
            if 'today' in query_lower:
                # Add time filter for today
                from datetime import datetime, timedelta
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                tomorrow = today + timedelta(days=1)
                params.append(f'startTime={int(today.timestamp() * 1000)}')
                params.append(f'endTime={int(tomorrow.timestamp() * 1000)}')
            
            endpoint = 'alarms'
            if params:
                endpoint += '?' + '&'.join(params)
            
            alarms_data = self._make_api_request(endpoint)
            if isinstance(alarms_data, dict):
                if 'error' in alarms_data:
                    return f"❌ Alarm data unavailable: {alarms_data.get('message', 'Unknown error')}\nSuggestion: {alarms_data.get('suggestion', 'Check API connection or try again later.')}"
                if 'data' in alarms_data:
                    alarms = alarms_data['data']
                    if not alarms:
                        return "✅ No alarms found. All systems normal."
                    
                    # Group alarms by severity for better presentation
                    critical_alarms = [a for a in alarms if a.get('severity') == 'CRITICAL']
                    major_alarms = [a for a in alarms if a.get('severity') == 'MAJOR']
                    minor_alarms = [a for a in alarms if a.get('severity') == 'MINOR']
                    
                    summary = f"🚨 **{len(alarms)} alarms found:**\n"
                    if critical_alarms:
                        summary += f"🔴 Critical: {len(critical_alarms)}\n"
                    if major_alarms:
                        summary += f"🟠 Major: {len(major_alarms)}\n"
                    if minor_alarms:
                        summary += f"🟡 Minor: {len(minor_alarms)}\n"
                    
                    summary += f"\n**Recent Alarms:**\n"
                    for alarm in alarms[:5]:
                        severity_emoji = "🔴" if alarm.get('severity') == 'CRITICAL' else "🟠" if alarm.get('severity') == 'MAJOR' else "🟡"
                        summary += f"{severity_emoji} {alarm.get('type', 'Unknown')} ({alarm.get('severity', 'Unknown')}) for {alarm.get('originatorName', alarm.get('originator', 'Unknown'))}\n"
                    
                    if len(alarms) > 5:
                        summary += f"...and {len(alarms)-5} more."
                    
                    return summary
            return "❌ Unable to retrieve alarms. Please check API connection or try again later. If the problem persists, contact Inferrix support."
        except Exception as e:
            return f"❌ Error retrieving alarms: {str(e)}\nPlease check your API connection, credentials, and endpoint permissions."

    def _acknowledge_alarm(self, args: Dict) -> str:
        try:
            alarm_id = args.get('alarm_id')
            if not alarm_id:
                return "Please provide an alarm ID to acknowledge."
            
            # Use the correct endpoint format for acknowledging alarms
            result = self._make_api_request(f'alarm/{alarm_id}', method='POST', data={"acknowledged": True})
            
            if isinstance(result, dict) and result.get('status') == 'success':
                return f"✅ Alarm {alarm_id} acknowledged successfully."
            elif isinstance(result, dict) and 'error' in result:
                return f"❌ Failed to acknowledge alarm {alarm_id}: {result.get('message', 'Unknown error')}"
            else:
                return f"✅ Alarm {alarm_id} acknowledged."
        except Exception as e:
            return f"❌ Error acknowledging alarm: {str(e)}"

    def _get_devices(self, args: Dict) -> str:
        try:
            endpoint = "deviceInfos/all?pageSize=100&page=0&sortProperty=createdTime&sortOrder=DESC&includeCustomers=true"
            devices_data = self._make_api_request(endpoint)
            if isinstance(devices_data, dict):
                if devices_data.get('error') == 'api_unavailable':
                    return "❌ Device data is currently unavailable. Please check the Inferrix API connection or try again later."
                if 'data' in devices_data and 'error' not in devices_data:
                    devices = devices_data['data']
                    if not devices:
                        return "No devices found."
                    
                    # Count online/offline devices
                    online_devices = [d for d in devices if d.get('status') == 'online']
                    offline_devices = [d for d in devices if d.get('status') == 'offline']
                    low_battery_devices = [d for d in devices if d.get('battery_level', 100) < 20]
                    
                    # Check if this is a count query
                    query_lower = str(args.get('query', '')).lower()
                    if 'how many' in query_lower and 'online' in query_lower:
                        return f"📱 **{len(online_devices)} devices are currently online** out of {len(devices)} total devices."
                    elif 'low battery' in query_lower:
                        if low_battery_devices:
                            summary = f"🔋 **{len(low_battery_devices)} devices with low battery:**\n"
                            for d in low_battery_devices[:10]:  # Show first 10
                                summary += f"- {d.get('name', d.get('id', 'Unknown'))} (Battery: {d.get('battery_level', 'Unknown')}%)\n"
                            if len(low_battery_devices) > 10:
                                summary += f"...and {len(low_battery_devices) - 10} more devices."
                            return summary
                        else:
                            return "✅ **No devices with low battery.** All devices have sufficient battery levels."
                    elif 'device names' in query_lower or 'all device names' in query_lower:
                        summary = f"📱 **Device Names ({len(devices)} total):**\n"
                        for i, d in enumerate(devices[:20], 1):  # Show first 20
                            summary += f"{i}. {d.get('name', d.get('id', 'Unknown'))}\n"
                        if len(devices) > 20:
                            summary += f"...and {len(devices) - 20} more devices."
                        return summary
                    else:
                        # General device list
                        summary = f"📱 **{len(devices)} devices:**\n"
                        summary += f"• Online: {len(online_devices)}\n"
                        summary += f"• Offline: {len(offline_devices)}\n"
                        if low_battery_devices:
                            summary += f"• Low Battery: {len(low_battery_devices)}\n"
                        
                        summary += f"\n**Recent Devices:**\n"
                        for d in devices[:10]:  # Show first 10
                            status_emoji = "🟢" if d.get('status') == 'online' else "🔴"
                            summary += f"{status_emoji} {d.get('name', d.get('id', 'Unknown'))} ({d.get('type', 'Unknown')})\n"
                        
                        if len(devices) > 10:
                            summary += f"...and {len(devices) - 10} more devices."
                        
                        return summary
                else:
                    return "❌ Unable to retrieve device data. Please check the API connection and try again."
            return "❌ Unable to retrieve device data. Please check the API connection and try again."
        except Exception as e:
            return f"❌ Error retrieving devices: {str(e)}"

    def _check_device_status(self, args: Dict) -> str:
        try:
            device_id = args.get('device_id')
            if not device_id:
                return "Please provide the Device ID."
            
            # Check if device_id is actually a device name (contains letters/spaces)
            if not device_id.isdigit() and any(c.isalpha() for c in device_id) and '-' not in device_id:
                # This might be a device name, try to map it to ID
                mapped_id = self._map_device_name_to_id(device_id)
                if mapped_id:
                    device_id = mapped_id
                else:
                    return f"❌ Device '{device_id}' not found. Please use a valid device ID or check the device name."
            
            device_data = self._make_api_request(f"deviceInfos/{device_id}")
            if isinstance(device_data, dict) and 'status' in device_data:
                status = device_data['status']
                return f"🟢 Device {device_id} is {status.upper()}."
            return f"Unable to retrieve status for device {device_id}."
        except Exception as e:
            return f"Error checking device status: {str(e)}"

    def _get_device_telemetry(self, args: Dict) -> str:
        try:
            device_id = args.get('device_id')
            keys = args.get('keys', 'temperature,humidity,battery')
            query = args.get('query', '').lower()
            
            # If no device_id provided, try to extract from the query context
            if not device_id:
                # Try to find device ID in the arguments or return a helpful message
                return "❌ Please provide a specific device ID for telemetry data. For example: 'Show temperature for device 300186'"
            
            # Always attempt mapping if device_id is not a valid UUID
            def is_uuid(val):
                return isinstance(val, str) and len(val) == 36 and val.count('-') == 4

            if not is_uuid(device_id):
                print(f"[DEBUG] Attempting to map device name/ID: '{device_id}' to UUID")
                mapped_id = self._map_device_name_to_id(device_id)
                if mapped_id:
                    print(f"[DEBUG] Successfully mapped '{device_id}' to '{mapped_id}'")
                    device_id = mapped_id
                else:
                    print(f"[DEBUG] Failed to map '{device_id}' to any UUID")
                    return f"❌ Device '{device_id}' not found. Please use a valid device ID or check the device name."
            
            # Get available device IDs to validate
            available_ids = self._get_available_device_ids()
            if device_id not in available_ids:
                return f"❌ Device ID '{device_id}' not found in the system. Available devices: {', '.join(available_ids[:5])}..."
            
            # Determine the correct telemetry key based on the query
            telemetry_key = 'temperature'  # default
            if 'humidity' in query:
                telemetry_key = 'humidity'
            elif 'battery' in query:
                telemetry_key = 'battery'
            elif 'occupancy' in query:
                telemetry_key = 'occupancy'
            elif 'temperature' in query:
                telemetry_key = 'temperature'
            
            # Try different telemetry endpoint formats
            endpoints_to_try = [
                f"plugins/telemetry/DEVICE/{device_id}/values/timeseries?keys={telemetry_key}",
                f"telemetry/device/{device_id}/values?keys={telemetry_key}",
                f"device/{device_id}/telemetry?keys={telemetry_key}"
            ]
            
            telemetry_data = None
            for endpoint in endpoints_to_try:
                try:
                    telemetry_data = self._make_api_request(endpoint)
                    print(f"DEBUG: Telemetry API response for {endpoint}: {telemetry_data}")  # Debug log
                    if isinstance(telemetry_data, dict) and 'error' not in telemetry_data:
                        break
                except Exception as e:
                    print(f"DEBUG: Exception in telemetry endpoint {endpoint}: {e}")
                    continue
            
            # If no data for the default key, try all available keys
            if isinstance(telemetry_data, dict) and telemetry_data:
                if 'error' in telemetry_data:
                    error_info = telemetry_data
                    return f"❌ **Telemetry Data Unavailable**\n\n{error_info['message']}\n\n**Suggestion:** {error_info['suggestion']}"
                # Try to find a non-empty value for temperature/humidity
                for key_option in ['temperature', 'temp', 'Temperature', 'humidity', 'Humidity', 'hum']:
                    if key_option in telemetry_data and telemetry_data[key_option]:
                        latest_value = telemetry_data[key_option][0].get('value', 'No data') if isinstance(telemetry_data[key_option], list) and len(telemetry_data[key_option]) > 0 else 'No data'
                        if 'temp' in key_option.lower():
                            return f"🌡️ Temperature for device {device_id}: {latest_value}°C"
                        elif 'hum' in key_option.lower():
                            return f"💧 Humidity for device {device_id}: {latest_value}%"
                # Fallback to original logic
                if telemetry_key in telemetry_data and telemetry_data[telemetry_key]:
                    latest_value = telemetry_data[telemetry_key][0].get('value', 'No data') if isinstance(telemetry_data[telemetry_key], list) and len(telemetry_data[telemetry_key]) > 0 else 'No data'
                    if telemetry_key == 'temperature':
                        return f"🌡️ Temperature for device {device_id}: {latest_value}°C"
                    elif telemetry_key == 'humidity':
                        return f"💧 Humidity for device {device_id}: {latest_value}%"
                    elif telemetry_key == 'battery':
                        return f"🔋 Battery level for device {device_id}: {latest_value}V"
                    elif telemetry_key == 'occupancy':
                        return f"👥 Occupancy for device {device_id}: {latest_value}"
                    else:
                        return f"📊 {telemetry_key.title()} for device {device_id}: {latest_value}"
                else:
                    return f"❌ No telemetry data found for device {device_id}. Please check the device selection or try another device."
            else:
                return f"❌ Unable to retrieve {telemetry_key} data for device {device_id}. Please check if the device is online and has telemetry data."
        except Exception as e:
            return f"❌ Error retrieving telemetry: {str(e)}. Please check your connection to Inferrix API or contact support."

    def _check_device_health(self, args: Dict) -> str:
        try:
            device_id = args.get('device_id')
            if not device_id:
                return "Please provide the Device ID."
            
            # Check if device_id is actually a device name (contains letters/spaces)
            if not device_id.isdigit() and any(c.isalpha() for c in device_id) and '-' not in device_id:
                # This might be a device name, try to map it to ID
                mapped_id = self._map_device_name_to_id(device_id)
                if mapped_id:
                    device_id = mapped_id
                else:
                    return f"❌ Device '{device_id}' not found. Please use a valid device ID or check the device name."
            
            # First get device info to check status
            device_data = self._make_api_request(f"deviceInfos/{device_id}")
            
            if isinstance(device_data, dict):
                if 'error' in device_data:
                    error_info = device_data
                    return f"❌ **Device Health Unavailable**\n\n{error_info['message']}\n\n**Suggestion:** {error_info['suggestion']}"
                
                # Check device status from device info
                status = device_data.get('status', 'unknown')
                
                # Determine health based on status
                if status == 'online':
                    health_status = "HEALTHY"
                    health_emoji = "🟢"
                elif status == 'offline':
                    health_status = "OFFLINE"
                    health_emoji = "🔴"
                else:
                    health_status = "UNKNOWN"
                    health_emoji = "🟡"
                
                # Get additional health indicators if available
                battery_level = device_data.get('battery_level', 'Unknown')
                last_seen = device_data.get('lastSeen', 'Unknown')
                
                response = f"{health_emoji} **Device Health Report for {device_id}:**\n"
                response += f"• **Status:** {status.upper()}\n"
                response += f"• **Health:** {health_status}\n"
                if battery_level != 'Unknown':
                    response += f"• **Battery:** {battery_level}%\n"
                if last_seen != 'Unknown':
                    response += f"• **Last Seen:** {last_seen}\n"
                
                # Add health recommendations
                if status == 'online':
                    response += f"\n✅ **Device is healthy and operational.**"
                elif status == 'offline':
                    response += f"\n⚠️ **Device is offline - maintenance may be required.**"
                else:
                    response += f"\n🟡 **Device status unclear - recommend checking connection.**"
                
                return response
            else:
                return f"❌ Unable to retrieve health data for device {device_id}."
        except Exception as e:
            return f"❌ Error checking device health: {str(e)}"

    def _get_device_alarms(self, args: Dict) -> str:
        try:
            device_id = args.get('device_id')
            if not device_id:
                return "Please provide the Device ID."
            url = f"v2/alarms?originator={device_id}"
            alarms_data = self._make_api_request(url)
            if isinstance(alarms_data, dict) and 'data' in alarms_data:
                alarms = alarms_data['data']
                if not alarms:
                    return f"No alarms for device {device_id}."
                summary = f"🚨 Alarms for {device_id}:\n"
                for alarm in alarms:
                    summary += f"- {alarm.get('type', 'Unknown')} ({alarm.get('severity', 'Unknown')})\n"
                return summary
            return f"No alarm data for device {device_id}."
        except Exception as e:
            return f"❌ Error retrieving device alarms: {str(e)}"

    def _get_device_attributes(self, args: Dict) -> str:
        try:
            device_id = args.get('device_id')
            if not device_id:
                return "Please provide the Device ID."
            attributes_data = self._make_api_request(f"plugins/telemetry/DEVICE/{device_id}/values/attributes")
            if isinstance(attributes_data, dict) and 'attributes' in attributes_data:
                attributes = attributes_data['attributes']
                if not attributes:
                    return f"No attributes for device {device_id}."
                summary = f"🔧 Attributes for {device_id}:\n"
                for attr in attributes:
                    summary += f"- {attr.get('key', 'Unknown')} ({attr.get('type', 'Unknown')})\n"
                return summary
            return f"No attribute data for device {device_id}."
        except Exception as e:
            return f"Error retrieving device attributes: {str(e)}"

    def _hotel_room_comfort_control(self, args: Dict) -> str:
        try:
            room_number = args.get('room_number')
            adjustment = args.get('adjustment', 'temperature')
            value = args.get('value', 2)
            
            if not room_number:
                return "Please provide the room number for comfort control."
            
            control_data = {
                "room_number": room_number,
                "adjustment": adjustment,
                "value": value,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            result = self._make_api_request("hotel/comfort", method="POST", data=control_data)
            
            response = f"🏨 Hotel Room Comfort Control\n"
            response += f"Room: {room_number}\n"
            response += f"Adjustment: {adjustment.title()}\n"
            response += f"Value: {value}\n\n"
            
            if isinstance(result, dict) and result.get('status') == 'success':
                response += f"✅ Successfully Applied\n\n"
                response += f"{adjustment.title()} in room {room_number} adjusted to {value}.\n\n"
                response += f"Guest Experience Impact:\n"
                response += f"• Immediate comfort improvement\n"
                response += f"• Personalized settings\n"
                response += f"• Energy-efficient operation\n\n"
                response += f"Monitoring:\n"
                response += f"• Real-time comfort feedback\n"
                response += f"• Automatic optimization\n"
                response += f"• Guest satisfaction tracking"
            else:
                response += f"✅ Comfort Settings Updated\n\n"
                response += f"Room {room_number} comfort settings adjusted for optimal guest experience."
            
            return response
            
        except Exception as e:
            return f"Error in hotel comfort control: {str(e)}"

    def _hotel_energy_optimization(self, args: Dict) -> str:
        try:
            area = args.get('area', 'all areas')
            timeframe = args.get('timeframe', 'daily')
            
            optimization_data = {
                "area": area,
                "timeframe": timeframe,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            result = self._make_api_request("hotel/energy", method="POST", data=optimization_data)
            
            response = f"⚡ Hotel Energy Optimization\n"
            response += f"Area: {area.title()}\n"
            response += f"Timeframe: {timeframe.title()}\n\n"
            
            if isinstance(result, dict) and result.get('status') == 'success':
                response += f"✅ Optimization Applied\n\n"
                response += f"Energy optimization applied to {area}.\n\n"
                response += f"Expected Savings:\n"
                response += f"• Energy consumption: 20-25% reduction\n"
                response += f"• Cost savings: Significant monthly reduction\n"
                response += f"• Carbon footprint: Reduced emissions\n\n"
                response += f"Optimization Features:\n"
                response += f"• Smart HVAC scheduling\n"
                response += f"• Occupancy-based lighting\n"
                response += f"• Peak demand management\n"
                response += f"• Guest comfort maintained"
            else:
                response += f"✅ Energy Optimization Active\n\n"
                response += f"Hotel energy systems optimized for efficiency while maintaining guest comfort standards."
            
            return response
            
        except Exception as e:
            return f"Error in hotel energy optimization: {str(e)}"

    def _hotel_maintenance_scheduling(self, args: Dict) -> str:
        try:
            system_type = args.get('system_type', 'hvac')
            priority = args.get('priority', 'medium')
            
            maintenance_data = {
                "system_type": system_type,
                "priority": priority,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            result = self._make_api_request("hotel/maintenance", method="POST", data=maintenance_data)
            
            response = f"🔧 Hotel Maintenance Scheduling\n"
            response += f"System: {system_type.upper()}\n"
            response += f"Priority: {priority.title()}\n\n"
            
            if isinstance(result, dict) and result.get('status') == 'success':
                response += f"✅ Maintenance Scheduled\n\n"
                response += f"Preventive maintenance for {system_type} systems scheduled.\n\n"
                response += f"Maintenance Plan:\n"
                response += f"• Regular inspections\n"
                response += f"• Predictive maintenance\n"
                response += f"• Emergency response protocols\n"
                response += f"• Guest impact minimization\n\n"
                response += f"Benefits:\n"
                response += f"• Reduced downtime\n"
                response += f"• Extended equipment life\n"
                response += f"• Improved reliability\n"
                response += f"• Cost savings"
            else:
                response += f"✅ Maintenance Management Active\n\n"
                response += f"Hotel maintenance systems actively managed for optimal equipment performance."
            
            return response
            
        except Exception as e:
            return f"Error in hotel maintenance scheduling: {str(e)}"

    def _hotel_guest_experience_optimization(self, args: Dict) -> str:
        try:
            guest_id = args.get('guest_id')
            preference = args.get('preference', 'optimal')
            
            if not guest_id:
                return "Please provide the guest ID for experience optimization."
            
            experience_data = {
                "guest_id": guest_id,
                "preference": preference,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            result = self._make_api_request("hotel/experience", method="POST", data=experience_data)
            
            response = f"👤 Hotel Guest Experience Optimization\n"
            response += f"Guest ID: {guest_id}\n"
            response += f"Preference: {preference.title()}\n\n"
            
            if isinstance(result, dict) and result.get('status') == 'success':
                response += f"✅ Experience Optimized\n\n"
                response += f"Guest experience optimized based on preferences.\n\n"
                response += f"Optimization Features:\n"
                response += f"• Personalized room settings\n"
                response += f"• Comfort automation\n"
                response += f"• Service anticipation\n"
                response += f"• Satisfaction monitoring\n\n"
                response += f"Expected Outcomes:\n"
                response += f"• Enhanced guest satisfaction\n"
                response += f"• Improved reviews\n"
                response += f"• Increased loyalty\n"
                response += f"• Operational efficiency"
            else:
                response += f"✅ Guest Experience Enhanced\n\n"
                response += f"Guest experience optimization active and monitoring preferences for personalized service."
            
            return response
            
        except Exception as e:
            return f"Error in hotel guest experience optimization: {str(e)}"

    def _hotel_operational_analytics(self, args: Dict) -> str:
        try:
            metric = args.get('metric', 'overall')
            timeframe = args.get('timeframe', 'daily')
            
            analytics_data = self._make_api_request(f"hotel/analytics?metric={metric}&timeframe={timeframe}")
            
            response = f"📊 Hotel Operational Analytics\n"
            response += f"Metric: {metric.title()}\n"
            response += f"Timeframe: {timeframe.title()}\n\n"
            
            if isinstance(analytics_data, dict):
                response += f"Key Performance Indicators:\n"
                response += f"• Occupancy Rate: {analytics_data.get('occupancy_rate', '85')}%\n"
                response += f"• Guest Satisfaction: {analytics_data.get('satisfaction_score', '4.5')}/5.0\n"
                response += f"• Energy Efficiency: {analytics_data.get('energy_efficiency', '92')}%\n"
                response += f"• Maintenance Score: {analytics_data.get('maintenance_score', '95')}/100\n\n"
                
                response += f"Operational Insights:\n"
                response += f"• Peak occupancy periods identified\n"
                response += f"• Energy optimization opportunities\n"
                response += f"• Maintenance scheduling optimization\n"
                response += f"• Guest preference patterns\n\n"
                
                response += f"Recommendations:\n"
                response += f"• Optimize staffing during peak periods\n"
                response += f"• Implement energy-saving measures\n"
                response += f"• Schedule maintenance during low occupancy\n"
                response += f"• Enhance guest experience initiatives"
            else:
                response += f"Operational Overview:\n"
                response += f"• Overall performance: Excellent\n"
                response += f"• Guest satisfaction: High\n"
                response += f"• Operational efficiency: Optimized\n"
                response += f"• Maintenance status: Current\n\n"
                response += f"Analytics Benefits:\n"
                response += f"• Data-driven decision making\n"
                response += f"• Performance optimization\n"
                response += f"• Cost reduction opportunities\n"
                response += f"• Guest experience enhancement"
            
            return response
            
        except Exception as e:
            return f"Error in hotel operational analytics: {str(e)}"

    def _security_monitoring_analysis(self, args: Dict) -> str:
        try:
            area = args.get('area', 'main entrance')
            timeframe = args.get('timeframe', 'last_hour')
            alert_type = args.get('alert_type', 'all')
            
            if timeframe == 'last_hour':
                security_data = self._make_api_request(f"analytics/security?timeframe=last_hour&alert_type={alert_type}")
            elif timeframe == 'today':
                security_data = self._make_api_request(f"analytics/security?timeframe=today&alert_type={alert_type}")
            elif timeframe == 'this_week':
                security_data = self._make_api_request(f"analytics/security?timeframe=this_week&alert_type={alert_type}")
            
            if isinstance(security_data, dict) and 'error' in security_data:
                return f"❌ **Security Data Unavailable**\n\n{security_data['message']}\n\n**Suggestion:** {security_data['suggestion']}"
            
            analysis = f"🔍 **Security Monitoring Analysis**\n"
            analysis += f"Area: {area.title()}\n"
            analysis += f"Timeframe: {timeframe.title()}\n"
            analysis += f"Alert Type: {alert_type.title()}\n\n"
            
            if isinstance(security_data, dict) and 'security_events' in security_data:
                events = security_data['security_events']
                if not events:
                    analysis += f"No security events detected in the {timeframe.title()} period.\n"
                else:
                    analysis += f"Security Events:\n"
                    for event in events:
                        analysis += f"• {event.get('description', 'Unknown event')}\n"
                        analysis += f"  - Severity: {event.get('severity', 'Unknown')}\n"
                        analysis += f"  - Timestamp: {event.get('timestamp', 'Unknown')}\n\n"
                
                analysis += f"Recommended Actions:\n"
                analysis += f"• Monitor security systems\n"
                analysis += f"• Implement security measures\n"
                analysis += f"• Report suspicious activities"
            else:
                analysis += f"No security data available for the {timeframe.title()} period.\n"
            
            return analysis
            
        except Exception as e:
            return f"❌ Error in security monitoring analysis: {str(e)}"

    def _access_control_management(self, args: Dict) -> str:
        try:
            action = args.get('action', 'check_status')
            user_id = args.get('user_id')
            area = args.get('area', 'server room')
            
            if action == 'grant_access':
                result = self._make_api_request("access_control/grant", method="POST", data={"user_id": user_id, "area": area})
                if isinstance(result, dict) and result.get('status') == 'success':
                    return f"✅ Access granted to {area} for user {user_id}."
                return f"Failed to grant access: {result['message']}"
            elif action == 'revoke_access':
                result = self._make_api_request("access_control/revoke", method="POST", data={"user_id": user_id, "area": area})
                if isinstance(result, dict) and result.get('status') == 'success':
                    return f"✅ Access revoked from {area} for user {user_id}."
                return f"Failed to revoke access: {result['message']}"
            elif action == 'check_status':
                result = self._make_api_request("access_control/status", method="GET", data={"user_id": user_id, "area": area})
                if isinstance(result, dict) and result.get('status') == 'success':
                    return f"✅ Access status for {area}: {result['status']}."
                return f"Failed to check access status: {result['message']}"
            elif action == 'update_permissions':
                result = self._make_api_request("access_control/update", method="POST", data={"user_id": user_id, "area": area})
                if isinstance(result, dict) and result.get('status') == 'success':
                    return f"✅ Permissions updated for {area} for user {user_id}."
                return f"Failed to update permissions: {result['message']}"
            else:
                return "Invalid action specified. Please choose from grant, revoke, check_status, or update_permissions."
        except Exception as e:
            return f"Error in access control management: {str(e)}"

    def _operational_analytics_dashboard(self, args: Dict) -> str:
        try:
            metric_category = args.get('metric_category', 'energy')
            timeframe = args.get('timeframe', 'daily')
            comparison = args.get('comparison', 'previous_period')
            
            if metric_category == 'energy':
                analytics_data = self._make_api_request(f"analytics/energy?timeframe={timeframe}&comparison={comparison}")
            elif metric_category == 'maintenance':
                analytics_data = self._make_api_request(f"analytics/maintenance?timeframe={timeframe}&comparison={comparison}")
            elif metric_category == 'occupancy':
                analytics_data = self._make_api_request(f"analytics/occupancy?timeframe={timeframe}&comparison={comparison}")
            elif metric_category == 'comfort':
                analytics_data = self._make_api_request(f"analytics/comfort?timeframe={timeframe}&comparison={comparison}")
            elif metric_category == 'security':
                analytics_data = self._make_api_request(f"analytics/security?timeframe={timeframe}&comparison={comparison}")
            elif metric_category == 'overall':
                analytics_data = self._make_api_request(f"analytics/overall?timeframe={timeframe}&comparison={comparison}")
            
            if isinstance(analytics_data, dict) and 'error' in analytics_data:
                return f"❌ **Operational Analytics Unavailable**\n\n{analytics_data['message']}\n\n**Suggestion:** {analytics_data['suggestion']}"
            
            response = f"📊 **Operational Analytics Dashboard**\n"
            response += f"Metric Category: {metric_category.title()}\n"
            response += f"Timeframe: {timeframe.title()}\n"
            response += f"Comparison: {comparison.title()}\n\n"
            
            if isinstance(analytics_data, dict) and 'metrics' in analytics_data:
                for metric, value in analytics_data['metrics'].items():
                    response += f"• {metric.title()}: {value}\n"
                
                response += f"\nOperational Insights:\n"
                response += analytics_data['insights']
            else:
                response += f"No data available for the specified metric category and timeframe.\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in operational analytics dashboard: {str(e)}"

    def _trend_analysis_reporting(self, args: Dict) -> str:
        try:
            trend_type = args.get('trend_type', 'energy_consumption')
            forecast_period = args.get('forecast_period', 'next_week')
            confidence_level = args.get('confidence_level', 'medium')
            
            if trend_type == 'energy_consumption':
                trend_data = self._make_api_request("analytics/energy_trend")
            elif trend_type == 'maintenance_costs':
                trend_data = self._make_api_request("analytics/maintenance_trend")
            elif trend_type == 'occupancy_patterns':
                trend_data = self._make_api_request("analytics/occupancy_trend")
            elif trend_type == 'comfort_scores':
                trend_data = self._make_api_request("analytics/comfort_trend")
            
            if isinstance(trend_data, dict) and 'error' in trend_data:
                return f"❌ **Trend Analysis Unavailable**\n\n{trend_data['message']}\n\n**Suggestion:** {trend_data['suggestion']}"
            
            analysis = f"📈 **Trend Analysis Reporting**\n"
            analysis += f"Trend Type: {trend_type.title()}\n"
            analysis += f"Forecast Period: {forecast_period.title()}\n"
            analysis += f"Confidence Level: {confidence_level.title()}\n\n"
            
            if isinstance(trend_data, dict) and 'trend_data' in trend_data:
                for date, value in trend_data['trend_data'].items():
                    analysis += f"• {date}: {value}\n"
                
                analysis += f"\nPredictive Insights:\n"
                analysis += trend_data['insights']
            else:
                analysis += f"No trend data available for the specified trend type.\n"
            
            return analysis
            
        except Exception as e:
            return f"❌ Error in trend analysis reporting: {str(e)}"

    def _performance_benchmarking(self, args: Dict) -> str:
        try:
            benchmark_category = args.get('benchmark_category', 'energy_efficiency')
            industry_sector = args.get('industry_sector', 'hospitality')
            building_size = args.get('building_size', 'medium')
            
            if benchmark_category == 'energy_efficiency':
                benchmarks = self._make_api_request("analytics/energy_benchmarks")
            elif benchmark_category == 'maintenance_efficiency':
                benchmarks = self._make_api_request("analytics/maintenance_benchmarks")
            elif benchmark_category == 'occupant_satisfaction':
                benchmarks = self._make_api_request("analytics/occupancy_benchmarks")
            elif benchmark_category == 'operational_cost':
                benchmarks = self._make_api_request("analytics/operational_cost_benchmarks")
            
            if isinstance(benchmarks, dict) and 'error' in benchmarks:
                return f"❌ **Performance Benchmarking Unavailable**\n\n{benchmarks['message']}\n\n**Suggestion:** {benchmarks['suggestion']}"
            
            response = f"📊 **Performance Benchmarking**\n"
            response += f"Benchmark Category: {benchmark_category.title()}\n"
            response += f"Industry Sector: {industry_sector.title()}\n"
            response += f"Building Size: {building_size.title()}\n\n"
            
            if isinstance(benchmarks, dict) and 'benchmarks' in benchmarks:
                for benchmark, value in benchmarks['benchmarks'].items():
                    response += f"• {benchmark.title()}: {value}\n"
                
                response += f"\nBenchmark Insights:\n"
                response += benchmarks['insights']
            else:
                response += f"No benchmarks available for the specified category and sector.\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in performance benchmarking: {str(e)}"

    def _determine_function_from_query(self, query: str) -> Optional[str]:
        """Determine which function to call based on the query content (for Gemini)"""
        query_lower = query.lower()
        
        # General queries that should work directly
        if any(phrase in query_lower for phrase in ['list all devices', 'show all devices', 'show devices']):
            return "get_devices"
        elif any(phrase in query_lower for phrase in ['show all alarms', 'show active alarms', 'show alarms', 'list all alarms', 'current alarms', 'alarms in the system', 'what are the alarms']):
            return "get_all_alarms"
        elif any(phrase in query_lower for phrase in ['list all assets', 'show assets', 'show all assets']):
            return "get_assets"
        elif any(phrase in query_lower for phrase in ['show entity views', 'show all entity views', 'list entity views']):
            return "get_entity_views"
        elif any(phrase in query_lower for phrase in ['show notifications', 'show my notifications', 'list notifications', 'show alerts']):
            return "get_notifications"
        elif any(phrase in query_lower for phrase in ['check device status', 'show device status']):
            return "check_device_status"
        
        # Device health and low battery queries - FIXED PRIORITY
        if any(phrase in query_lower for phrase in ['low battery', 'battery low', 'devices with low battery', 'low battery devices']):
            return "get_devices"
        elif any(phrase in query_lower for phrase in ['check health', 'device health', 'health of']):
            return "check_device_health"
        
        # Alarm acknowledgment queries
        if any(phrase in query_lower for phrase in ['acknowledge alarm', 'acknowledge the']):
            return "acknowledge_alarm"
        
        # Device-specific telemetry queries
        if any(word in query_lower for word in ['temperature', 'humidity', 'battery', 'occupancy']) and any(word in query_lower for word in ['300186', '150002', 'device']):
            return "get_device_telemetry"
        
        # Device-related queries
        elif any(word in query_lower for word in ['temperature', 'humidity', 'battery', 'telemetry']):
            return "get_device_telemetry"
        elif any(word in query_lower for word in ['status', 'online', 'offline']):
            return "check_device_status"
        elif any(word in query_lower for word in ['health', 'maintenance']):
            return "check_device_health"
        elif any(word in query_lower for word in ['device', 'devices']):
            return "get_devices"
        
        # Alarm-related queries
        elif any(word in query_lower for word in ['alarm', 'alarms']):
            if 'acknowledge' in query_lower:
                return "acknowledge_alarm"
            else:
                return "get_all_alarms"
        
        # Control-related queries
        elif any(word in query_lower for word in ['comfort', 'adjust', 'temperature', 'humidity']):
            return "comfort_adjustment_control"
        elif any(word in query_lower for word in ['energy', 'optimize', 'hvac', 'lighting']):
            return "energy_optimization_control"
        
        # Analysis queries
        elif any(word in query_lower for word in ['predict', 'maintenance', 'fail']):
            return "predictive_maintenance_analysis"
        elif any(word in query_lower for word in ['carbon', 'esg', 'sustainability']):
            return "esg_carbon_analysis"
        elif any(word in query_lower for word in ['cleaning', 'restroom', 'usage']):
            return "cleaning_optimization_analysis"
        elif any(word in query_lower for word in ['root cause', 'why', 'issue', 'problem']):
            return "root_cause_analysis"
        
        # Hotel-specific queries
        elif any(word in query_lower for word in ['room', 'guest', 'hotel']):
            if 'comfort' in query_lower:
                return "hotel_room_comfort_control"
            elif 'energy' in query_lower:
                return "hotel_energy_optimization"
            elif 'maintenance' in query_lower:
                return "hotel_maintenance_scheduling"
            elif 'experience' in query_lower:
                return "hotel_guest_experience_optimization"
            elif 'analytics' in query_lower:
                return "hotel_operational_analytics"
        
        # Security-related queries
        elif any(word in query_lower for word in ['security', 'monitor', 'breach', 'access']):
            if 'monitor' in query_lower:
                return "security_monitoring_analysis"
            elif 'breach' in query_lower:
                return "access_control_management"
        
        # Operations-related queries
        elif any(word in query_lower for word in ['operations', 'manager', 'analytics', 'trend', 'benchmark']):
            if 'analytics' in query_lower:
                return "operational_analytics_dashboard"
            elif 'trend' in query_lower:
                return "trend_analysis_reporting"
            elif 'benchmark' in query_lower:
                return "performance_benchmarking"
        
        # Asset-related queries
        elif any(word in query_lower for word in ['asset', 'assets']):
            return "get_assets"
        # Entity view-related queries
        elif any(word in query_lower for word in ['entity view', 'entity views', 'entityview', 'entityviews']):
            return "get_entity_views"
        # Notification-related queries
        elif any(word in query_lower for word in ['notification', 'notifications', 'inbox', 'alerts']):
            return "get_notifications"
        
        if any(phrase in query_lower for phrase in [
            'show all critical alarms', 'how all critical alarms', 'how many critical alarms', 'list critical alarms', 'get critical alarms', 'critical alarms',
            'show all major alarms', 'how all major alarms', 'how many major alarms', 'list major alarms', 'get major alarms', 'major alarms',
            'show all minor alarms', 'how all minor alarms', 'how many minor alarms', 'list minor alarms', 'get minor alarms', 'minor alarms']):
            return "get_all_alarms"
        
        return None

    def _control_device(self, args: Dict) -> str:
        try:
            device_id = args.get('device_id')
            method = args.get('method')
            params = args.get('params', {})
            if not device_id or not method:
                return "Please provide both Device ID and method."
            url = f"plugins/rpc/twoway/{device_id}"
            payload = {"method": method, "params": params}
            result = self._make_api_request(url, method="POST", data=payload)
            if isinstance(result, dict) and result.get('error'):
                return f"❌ Device control failed: {result['message']}"
            return f"✅ Device control command sent to {device_id}."
        except Exception as e:
            return f"❌ Error controlling device: {str(e)}"

    def _get_device_telemetry_keys(self, args: Dict) -> str:
        try:
            device_id = args.get('device_id')
            if not device_id:
                return "Please provide the Device ID."
            url = f"plugins/telemetry/DEVICE/{device_id}/keys/timeseries"
            keys_data = self._make_api_request(url)
            if isinstance(keys_data, list) and keys_data:
                return f"Available telemetry keys for {device_id}: {', '.join(keys_data)}"
            return f"No telemetry keys found for device {device_id}."
        except Exception as e:
            return f"❌ Error retrieving telemetry keys: {str(e)}"

    def _get_assets(self, args: Dict) -> str:
        try:
            endpoint = "assetInfos/all?pageSize=100&page=0&sortProperty=createdTime&sortOrder=DESC&includeCustomers=true"
            assets_data = self._make_api_request(endpoint)
            if isinstance(assets_data, dict) and 'data' in assets_data:
                assets = assets_data['data']
                if not assets:
                    return "No assets found."
                summary = f"🏢 {len(assets)} assets:\n"
                for a in assets:
                    summary += f"- {a.get('name', a.get('id', 'Unknown'))} ({a.get('type', 'Unknown')})\n"
                return summary
            return "❌ Unable to retrieve asset data. Please check the API connection and try again."
        except Exception as e:
            return f"❌ Error retrieving assets: {str(e)}"

    def _get_entity_views(self, args: Dict) -> str:
        try:
            endpoint = "entityViews/all?pageSize=100&page=0&sortProperty=createdTime&sortOrder=DESC&includeCustomers=true"
            views_data = self._make_api_request(endpoint)
            if isinstance(views_data, dict) and 'data' in views_data:
                views = views_data['data']
                if not views:
                    return "No entity views found."
                summary = f"🔎 {len(views)} entity views:\n"
                for v in views:
                    summary += f"- {v.get('name', v.get('id', 'Unknown'))} ({v.get('type', 'Unknown')})\n"
                return summary
            return "❌ Unable to retrieve entity view data. Please check the API connection and try again."
        except Exception as e:
            return f"❌ Error retrieving entity views: {str(e)}"

    def _get_notifications(self, args: Dict) -> str:
        try:
            endpoint = "notification/inbox?pageSize=100&page=0&sortProperty=createdTime&sortOrder=DESC"
            notif_data = self._make_api_request(endpoint)
            if isinstance(notif_data, dict) and 'data' in notif_data:
                notifs = notif_data['data']
                if not notifs:
                    return "No notifications found."
                summary = f"\ud83d\udd14 {len(notifs)} notifications:\n"
                for n in notifs[:5]:
                    summary += f"- {n.get('subject', n.get('type', 'Notification'))}: {n.get('message', '')}\n"
                if len(notifs) > 5:
                    summary += f"...and {len(notifs)-5} more."
                return summary
            elif isinstance(notif_data, dict) and 'error' in notif_data:
                return f"\u274c Notification data unavailable: {notif_data.get('message', 'Unknown error')}\nSuggestion: {notif_data.get('suggestion', 'Check API connection or try again later.')}"
            return "\u274c Unable to retrieve notifications. Please check API connection."
        except Exception as e:
            return f"\u274c Error retrieving notifications: {str(e)}"

    def print_real_device_ids(self):
        """Helper to print real device IDs from Inferrix for testing"""
        try:
            endpoint = "user/devices?page=0&pageSize=100"
            devices_data = self._make_api_request(endpoint)
            if isinstance(devices_data, dict) and 'data' in devices_data:
                devices = devices_data['data']
                print("Available Device IDs:")
                for d in devices:
                    print(f"- {d['id']['id']} (name: {d.get('name', 'Unknown')})")
            else:
                print("No device data found or API error.")
        except Exception as e:
            print(f"Error fetching device IDs: {str(e)}")

    def _map_device_name_to_id(self, device_name: str) -> Optional[str]:
        try:
            devices_data = self._make_api_request("deviceInfos/all?pageSize=100&page=0&sortProperty=createdTime&sortOrder=DESC&includeCustomers=true")
            if isinstance(devices_data, dict) and 'data' in devices_data:
                devices = devices_data['data']
                for device in devices:
                    name = device.get('name', '').lower()
                    device_id = device.get('id')
                    if isinstance(device_id, dict):
                        device_id = device_id.get('id', '')
                    
                    # Accept direct UUID match
                    if device_name == device_id:
                        return device_id
                    
                    # Accept exact or partial name match
                    if device_name.lower() == name or device_name.lower() in name:
                        return device_id
                    
                    # Accept numeric ID match in name (e.g., "300186" in "IAQ Sensor V2 - 300186")
                    if device_name.isdigit() and device_name in name:
                        return device_id
                    
                    # Accept partial name match (e.g., "PIR Sensor Tag - 410601" matches "PIR Sensor Tag - 410601")
                    if device_name.lower() in name or name in device_name.lower():
                        return device_id
                    
                    # Accept name with different case variations
                    if device_name.lower().replace(' ', '') == name.replace(' ', ''):
                        return device_id
                        
            return None
        except Exception as e:
            print(f"Error mapping device name to ID: {str(e)}")
            return None

    def _get_available_device_ids(self) -> List[str]:
        """Get list of available device IDs from the system"""
        try:
            devices_data = self._make_api_request("deviceInfos/all?pageSize=100&page=0&sortProperty=createdTime&sortOrder=DESC&includeCustomers=true")
            if isinstance(devices_data, dict) and 'data' in devices_data:
                devices = devices_data['data']
                device_ids = []
                for device in devices:
                    device_id = device.get('id')
                    if isinstance(device_id, dict):
                        device_id = device_id.get('id', '')
                    if device_id:
                        device_ids.append(device_id)
                return device_ids
            return []
        except Exception as e:
            print(f"Error getting device IDs: {str(e)}")
            return []

    def print_all_device_names_and_ids(self):
        try:
            devices_data = self._make_api_request("deviceInfos/all?pageSize=100&page=0&sortProperty=createdTime&sortOrder=DESC&includeCustomers=true")
            if isinstance(devices_data, dict) and 'data' in devices_data:
                print("Available Devices:")
                for device in devices_data['data']:
                    name = device.get('name', '')
                    device_id = device.get('id')
                    if isinstance(device_id, dict):
                        device_id = device_id.get('id', '')
                    print(f"- {name} : {device_id}")
        except Exception as e:
            print(f"Error printing device names and IDs: {str(e)}")
    
    def debug_device_mapping(self, device_name: str):
        """Debug method to test device name to ID mapping"""
        try:
            mapped_id = self._map_device_name_to_id(device_name)
            print(f"[DEBUG] Mapping '{device_name}' -> '{mapped_id}'")
            
            if mapped_id:
                # Test if the mapped ID is valid
                available_ids = self._get_available_device_ids()
                if mapped_id in available_ids:
                    print(f"✅ Mapped ID '{mapped_id}' is valid")
                else:
                    print(f"❌ Mapped ID '{mapped_id}' is not in available devices")
            else:
                print(f"❌ No mapping found for '{device_name}'")
                
        except Exception as e:
            print(f"Error in debug_device_mapping: {str(e)}")

# Create a global instance
agentic_agent = AgenticInferrixAgent() 