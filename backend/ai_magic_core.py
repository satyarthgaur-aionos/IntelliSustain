#!/usr/bin/env python3
"""
AI Magic Core - Enhanced conversational memory, context, and intelligent features
"""

import json
import time
import re
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from collections import defaultdict
import hashlib

class ConversationMemory:
    """Manages conversational context and user memory"""
    
    def __init__(self):
        self.user_sessions = {}  # user_id -> session_data
        self.session_timeout = 3600  # 1 hour
    
    def get_user_session(self, user_id: str) -> Dict:
        """Get or create user session"""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                'created_at': time.time(),
                'last_activity': time.time(),
                'context': {
                    'last_device': None,
                    'last_query_type': None,
                    'preferences': {},
                    'recent_devices': [],
                    'user_role': 'user'
                },
                'conversation_history': [],
                'notifications': []
            }
        else:
            # Update last activity
            self.user_sessions[user_id]['last_activity'] = time.time()
        
        return self.user_sessions[user_id]
    
    def update_context(self, user_id: str, **kwargs):
        """Update user context"""
        session = self.get_user_session(user_id)
        session['context'].update(kwargs)
    
    def add_to_history(self, user_id: str, query: str, response: str, device_id: Optional[str] = None):
        """Add conversation to history"""
        session = self.get_user_session(user_id)
        entry = {
            'timestamp': time.time(),
            'query': query,
            'response': response,
            'device_id': device_id or ""
        }
        session['conversation_history'].append(entry)
        
        # Keep only last 20 conversations
        if len(session['conversation_history']) > 20:
            session['conversation_history'] = session['conversation_history'][-20:]
    
    def get_recent_context(self, user_id: str, limit: int = 5) -> List[Dict]:
        """Get recent conversation context"""
        session = self.get_user_session(user_id)
        return session['conversation_history'][-limit:]
    
    def add_notification(self, user_id: str, notification: Dict):
        """Add notification for user"""
        session = self.get_user_session(user_id)
        session['notifications'].append({
            'timestamp': time.time(),
            **notification
        })
    
    def get_notifications(self, user_id: str) -> List[Dict]:
        """Get user notifications"""
        session = self.get_user_session(user_id)
        return session['notifications']

class MultiDeviceProcessor:
    """Handles multi-device operations and bulk queries"""
    
    @staticmethod
    def extract_devices_from_query(query: str, available_devices: List[Dict]) -> List[str]:
        """Extract multiple devices from a query"""
        devices = []
        query_lower = query.lower()
        
        # Look for location-based queries
        location_patterns = {
            'east wing': ['east', 'east wing'],
            'west wing': ['west', 'west wing'], 
            'north wing': ['north', 'north wing'],
            'south wing': ['south', 'south wing'],
            '2nd floor': ['2nd', 'second', 'floor 2'],
            '3rd floor': ['3rd', 'third', 'floor 3'],
            'all thermostats': ['thermostat', 'all thermostat'],
            'all sensors': ['sensor', 'all sensor'],
            'all hvac': ['hvac', 'all hvac']
        }
        
        for location, patterns in location_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                # Find devices matching this location/type
                for device in available_devices:
                    device_name = device.get('name', '').lower()
                    if any(pattern in device_name for pattern in patterns):
                        device_id = device.get('id', {})
                        if isinstance(device_id, dict):
                            device_id = device_id.get('id', '')
                        if device_id:
                            devices.append(device_id)
        
        # If no location found, look for "all" or "every" patterns
        if 'all' in query_lower or 'every' in query_lower:
            # Return all devices (limit to first 10 for performance)
            for device in available_devices[:10]:
                device_id = device.get('id', {})
                if isinstance(device_id, dict):
                    device_id = device_id.get('id', '')
                if device_id:
                    devices.append(device_id)
        
        return devices

class ProactiveInsights:
    """Provides proactive recommendations and insights"""
    
    @staticmethod
    def analyze_device_health(device_data: Dict) -> Dict:
        """Analyze device health and provide insights"""
        insights = {
            'status': 'healthy',
            'recommendations': [],
            'warnings': []
        }
        
        # Check battery level
        battery = device_data.get('battery_level')
        if battery is not None:
            # Battery threshold: For most IoT devices, low battery is typically < 3.0V
            # Normal range: 3.0V - 4.2V for Li-ion batteries
            if battery < 3.0:
                insights['status'] = 'warning'
                insights['warnings'].append(f"Battery level is low ({battery:.2f}V)")
                insights['recommendations'].append("Consider replacing battery soon")
            elif battery < 3.5:
                insights['recommendations'].append(f"Monitor battery level ({battery:.2f}V)")
        
        # Check last seen
        last_seen = device_data.get('lastSeen')
        if last_seen:
            try:
                last_seen_time = datetime.fromisoformat(last_seen.replace('Z', '+00:00'))
                time_diff = datetime.now(last_seen_time.tzinfo) - last_seen_time
                if time_diff > timedelta(hours=24):
                    insights['status'] = 'warning'
                    insights['warnings'].append(f"Device hasn't reported in {time_diff.days} days")
                    insights['recommendations'].append("Check device connectivity")
            except:
                pass
        
        return insights
    
    @staticmethod
    def detect_anomalies(telemetry_data: Dict, device_id: str) -> List[Dict]:
        """Detect anomalies in telemetry data"""
        anomalies = []
        
        # Simple anomaly detection for temperature
        if 'temperature' in telemetry_data:
            temp_values = []
            for entry in telemetry_data['temperature'][:10]:  # Last 10 readings
                if isinstance(entry, dict) and 'value' in entry:
                    try:
                        temp_values.append(float(entry['value']))
                    except:
                        pass
            
            if len(temp_values) >= 3:
                avg_temp = sum(temp_values) / len(temp_values)
                for temp in temp_values:
                    if abs(temp - avg_temp) > 5:  # 5 degree deviation
                        anomalies.append({
                            'type': 'temperature_anomaly',
                            'device_id': device_id,
                            'value': temp,
                            'expected_range': f"{avg_temp-2:.1f}°C - {avg_temp+2:.1f}°C",
                            'severity': 'medium'
                        })
        
        return anomalies

class NaturalLanguageProcessor:
    """Enhanced natural language processing for complex commands"""
    
    @staticmethod
    def parse_complex_command(query: str) -> Dict:
        """Parse complex natural language commands"""
        parsed = {
            'action': None,
            'devices': [],
            'parameters': {},
            'schedule': None,
            'conditions': []
        }
        
        query_lower = query.lower()
        
        # Parse actions
        if any(word in query_lower for word in ['turn off', 'shut down', 'disable']):
            parsed['action'] = 'turn_off'
        elif any(word in query_lower for word in ['turn on', 'enable', 'activate']):
            parsed['action'] = 'turn_on'
        elif any(word in query_lower for word in ['adjust', 'set', 'change']):
            parsed['action'] = 'adjust'
        elif any(word in query_lower for word in ['schedule', 'plan']):
            parsed['action'] = 'schedule'
        
        # Parse time conditions
        time_patterns = {
            'after 8pm': '20:00',
            'before 6am': '06:00',
            'weekends': 'weekend',
            'weekdays': 'weekday',
            'every monday': 'monday',
            'daily': 'daily'
        }
        
        for pattern, time_value in time_patterns.items():
            if pattern in query_lower:
                parsed['schedule'] = time_value
        
        # Parse parameters (temperature, brightness, etc.)
        temp_match = re.search(r'(\d+)\s*degrees?', query_lower)
        if temp_match:
            parsed['parameters']['temperature'] = int(temp_match.group(1))
        
        return parsed

class RichResponseGenerator:
    """Generates rich, actionable responses"""
    
    @staticmethod
    def format_device_summary(devices: List[Dict]) -> str:
        """Format a rich device summary"""
        if not devices:
            return "No devices found."
        
        summary = f"📱 **{len(devices)} Devices Found:**\n\n"
        
        # Group by type
        by_type = defaultdict(list)
        for device in devices:
            device_type = device.get('type', 'Unknown')
            by_type[device_type].append(device)
        
        for device_type, device_list in by_type.items():
            summary += f"**{device_type} ({len(device_list)}):**\n"
            for device in device_list[:5]:  # Show first 5 of each type
                name = device.get('name', 'Unknown')
                status = device.get('status', 'unknown')
                status_emoji = "🟢" if status == 'online' else "🔴"
                summary += f"  {status_emoji} {name}\n"
            if len(device_list) > 5:
                summary += f"  ... and {len(device_list)-5} more\n"
            summary += "\n"
        
        return summary
    
    @staticmethod
    def format_alarm_summary(alarms: List[Dict]) -> str:
        """Format a rich alarm summary"""
        if not alarms:
            return "✅ No active alarms found."
        
        summary = f"🚨 **{len(alarms)} Active Alarms:**\n\n"
        
        # Group by severity
        by_severity = defaultdict(list)
        for alarm in alarms:
            severity = alarm.get('severity', 'UNKNOWN')
            by_severity[severity].append(alarm)
        
        for severity, alarm_list in by_severity.items():
            emoji = "🔴" if severity == "CRITICAL" else "🟡" if severity == "MAJOR" else "🟢"
            summary += f"{emoji} **{severity} ({len(alarm_list)}):**\n"
            for alarm in alarm_list[:3]:  # Show first 3 of each severity
                device = alarm.get('originatorName', 'Unknown Device')
                alarm_type = alarm.get('type', 'Unknown')
                summary += f"  • {device}: {alarm_type}\n"
            if len(alarm_list) > 3:
                summary += f"  ... and {len(alarm_list)-3} more\n"
            summary += "\n"
        
        return summary

class MultiLanguageSupport:
    """Multi-language support using LLM translation"""
    
    SUPPORTED_LANGUAGES = ['en', 'hi', 'es', 'fr', 'de', 'zh']
    
    @staticmethod
    def detect_language(query: str) -> str:
        """Enhanced language detection with Hinglish support"""
        # Count Hindi and English characters
        hindi_chars = len(re.findall(r'[अ-ह]', query))
        english_chars = len(re.findall(r'[a-zA-Z]', query))
        total_chars = len(re.sub(r'[^a-zA-Zअ-ह]', '', query))  # Only count letters
        
        if total_chars == 0:
            return 'en'  # Default to English if no letters found
        
        # Calculate percentage of Hindi characters
        hindi_percentage = hindi_chars / total_chars if total_chars > 0 else 0
        
        # Enhanced detection logic
        if hindi_percentage >= 0.3:  # If 30% or more characters are Hindi
            return 'hi'  # Treat as Hindi/Hinglish
        elif re.search(r'[ñáéíóúü]', query):  # Spanish
            return 'es'
        elif re.search(r'[àâäéèêëïîôöùûüÿç]', query):  # French
            return 'fr'
        elif re.search(r'[äöüß]', query):  # German
            return 'de'
        elif re.search(r'[一-龯]', query):  # Chinese
            return 'zh'
        else:
            return 'en'
    
    @staticmethod
    def is_hinglish(query: str) -> bool:
        """Check if query is Hinglish (mixed Hindi-English)"""
        hindi_chars = len(re.findall(r'[अ-ह]', query))
        english_chars = len(re.findall(r'[a-zA-Z]', query))
        total_chars = len(re.sub(r'[^a-zA-Zअ-ह]', '', query))
        
        if total_chars == 0:
            return False
        
        hindi_percentage = hindi_chars / total_chars
        # Consider Hinglish if both Hindi and English are present
        return 0.1 <= hindi_percentage <= 0.9 and hindi_chars > 0 and english_chars > 0
    
    @staticmethod
    def extract_hinglish_components(query: str) -> Dict[str, Union[list, bool]]:
        """Extract Hindi and English components from Hinglish query"""
        # Split by spaces and categorize words
        words = query.split()
        hindi_words = []
        english_words = []
        
        for word in words:
            # Clean word (remove punctuation)
            clean_word = re.sub(r'[^\wअ-ह]', '', word)
            if re.search(r'[अ-ह]', clean_word):
                hindi_words.append(clean_word)
            elif re.search(r'[a-zA-Z]', clean_word):
                english_words.append(clean_word)
        
        return {
            'hindi_words': hindi_words,
            'english_words': english_words,
            'mixed': len(hindi_words) > 0 and len(english_words) > 0
        }
    
    @staticmethod
    def translate_response(response: str, target_language: str, llm_client) -> str:
        """Translate response to target language"""
        if target_language == 'en':
            return response
        
        try:
            # Use LLM for translation
            prompt = f"Translate this response to {target_language}. Keep the emojis and formatting:\n\n{response}"
            translated = llm_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            return translated.choices[0].message.content
        except:
            return response  # Fallback to original if translation fails

class SmartNotifications:
    """Smart notification system with intelligent filtering and prioritization"""
    
    def __init__(self):
        self.notification_rules = {
            'critical_alarm': {
                'priority': 'high',
                'channels': ['immediate', 'email', 'sms'],
                'conditions': ['severity == CRITICAL']
            },
            'device_offline': {
                'priority': 'medium',
                'channels': ['immediate', 'email'],
                'conditions': ['status == offline', 'last_seen > 24h']
            },
            'battery_low': {
                'priority': 'low',
                'channels': ['email'],
                'conditions': ['battery_level < 3.0V']
            },
            'anomaly_detected': {
                'priority': 'medium',
                'channels': ['immediate', 'email'],
                'conditions': ['anomaly_score > threshold']
            }
        }
    
    def evaluate_notification(self, event_data: Dict) -> Dict:
        """Evaluate if an event should trigger a notification"""
        notification = {
            'should_notify': False,
            'priority': 'low',
            'channels': [],
            'message': '',
            'action_required': False
        }
        
        # Check for critical alarms
        if event_data.get('type') == 'alarm' and event_data.get('severity') == 'CRITICAL':
            notification.update({
                'should_notify': True,
                'priority': 'high',
                'channels': ['immediate', 'email', 'sms'],
                'message': f"🚨 CRITICAL ALARM: {event_data.get('device_name', 'Unknown Device')} - {event_data.get('message', 'Critical issue detected')}",
                'action_required': True
            })
        
        # Check for device offline
        elif event_data.get('type') == 'device_status' and event_data.get('status') == 'offline':
            notification.update({
                'should_notify': True,
                'priority': 'medium',
                'channels': ['immediate', 'email'],
                'message': f"📱 Device Offline: {event_data.get('device_name', 'Unknown Device')} has been offline for {event_data.get('offline_duration', 'unknown')}",
                'action_required': True
            })
        
        # Check for battery low
        elif event_data.get('type') == 'battery' and event_data.get('level', 4.2) < 3.0:
            notification.update({
                'should_notify': True,
                'priority': 'low',
                'channels': ['email'],
                'message': f"🔋 Low Battery: {event_data.get('device_name', 'Unknown Device')} battery at {event_data.get('level'):.2f}V",
                'action_required': False
            })
        
        return notification
    
    def format_notification_message(self, notification: Dict, user_context: Dict) -> str:
        """Format notification message based on user preferences"""
        message = notification['message']
        
        # Add personalized context
        if user_context.get('role') == 'admin':
            message += "\n\n🔧 Admin Actions Available:"
            message += "\n• Acknowledge alarm"
            message += "\n• View device details"
            message += "\n• Check system health"
        elif user_context.get('role') == 'technician':
            message += "\n\n🛠️ Technician Actions Available:"
            message += "\n• View troubleshooting guide"
            message += "\n• Check maintenance schedule"
            message += "\n• Request parts"
        
        return message

class SelfHealing:
    """Self-healing capabilities for automatic problem resolution"""
    
    def __init__(self):
        self.healing_strategies = {
            'device_offline': [
                'check_network_connectivity',
                'restart_device',
                'check_power_supply',
                'escalate_to_technician'
            ],
            'high_temperature': [
                'adjust_hvac_settings',
                'check_ventilation',
                'verify_sensor_accuracy',
                'schedule_maintenance'
            ],
            'communication_error': [
                'retry_connection',
                'check_api_endpoints',
                'verify_authentication',
                'restart_service'
            ],
            'data_anomaly': [
                'validate_sensor_data',
                'check_calibration',
                'compare_with_historical',
                'flag_for_review'
            ]
        }
    
    def diagnose_issue(self, device_data: Dict, telemetry_data: Dict) -> Dict:
        """Diagnose issues and suggest healing strategies"""
        diagnosis = {
            'issues_found': [],
            'healing_actions': [],
            'confidence': 0.0,
            'requires_human_intervention': False
        }
        
        # Check device connectivity
        if device_data.get('status') == 'offline':
            diagnosis['issues_found'].append({
                'type': 'device_offline',
                'severity': 'high',
                'description': 'Device is not responding'
            })
            diagnosis['healing_actions'].extend(self.healing_strategies['device_offline'])
            diagnosis['confidence'] += 0.8
        
        # Check temperature anomalies
        if 'temperature' in telemetry_data:
            temp_values = []
            for entry in telemetry_data['temperature'][:5]:
                if isinstance(entry, dict) and 'value' in entry:
                    try:
                        temp_values.append(float(entry['value']))
                    except:
                        pass
            
            if temp_values:
                avg_temp = sum(temp_values) / len(temp_values)
                if avg_temp > 30:  # High temperature threshold
                    diagnosis['issues_found'].append({
                        'type': 'high_temperature',
                        'severity': 'medium',
                        'description': f'Average temperature is {avg_temp:.1f}°C'
                    })
                    diagnosis['healing_actions'].extend(self.healing_strategies['high_temperature'])
                    diagnosis['confidence'] += 0.6
        
        # Determine if human intervention is needed
        if diagnosis['confidence'] > 0.7 and any(issue['severity'] == 'high' for issue in diagnosis['issues_found']):
            diagnosis['requires_human_intervention'] = True
        
        return diagnosis
    
    def generate_healing_plan(self, diagnosis: Dict) -> str:
        """Generate a human-readable healing plan"""
        if not diagnosis['issues_found']:
            return "✅ No issues detected. Device is operating normally."
        
        plan = f"🔧 **Self-Healing Diagnosis Report:**\n\n"
        plan += f"**Issues Found:** {len(diagnosis['issues_found'])}\n"
        plan += f"**Confidence:** {diagnosis['confidence']:.1%}\n"
        plan += f"**Human Intervention Required:** {'Yes' if diagnosis['requires_human_intervention'] else 'No'}\n\n"
        
        for issue in diagnosis['issues_found']:
            severity_emoji = "🔴" if issue['severity'] == 'high' else "🟡" if issue['severity'] == 'medium' else "🟢"
            plan += f"{severity_emoji} **{issue['type'].replace('_', ' ').title()}** ({issue['severity']})\n"
            plan += f"   {issue['description']}\n\n"
        
        if diagnosis['healing_actions']:
            plan += "**Recommended Actions:**\n"
            for i, action in enumerate(diagnosis['healing_actions'][:5], 1):  # Limit to 5 actions
                plan += f"{i}. {action.replace('_', ' ').title()}\n"
        
        if diagnosis['requires_human_intervention']:
            plan += "\n⚠️ **Human intervention recommended for critical issues.**"
        
        return plan

# Global instances
conversation_memory = ConversationMemory()
multi_device_processor = MultiDeviceProcessor()
proactive_insights = ProactiveInsights()
nlp_processor = NaturalLanguageProcessor()
rich_response = RichResponseGenerator()
multi_lang = MultiLanguageSupport()
smart_notifications = SmartNotifications()
self_healing = SelfHealing() 