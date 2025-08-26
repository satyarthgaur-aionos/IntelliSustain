# 🎯 System Prompt Usage in Our Agentic AI - Client Guide

## 🤖 **How We Use System Prompts for Input & Output Formatting**

Our IntelliSustain AI Agent uses **advanced system prompts** to intelligently format both user inputs and API outputs, creating a seamless, context-aware experience.

---

## 🧠 **System Prompt Architecture**

### **📋 Multi-Layer System Prompt Design**

```
┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEM PROMPT LAYERS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🎯 LAYER 1: CORE IDENTITY & ROLE                              │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ "You are IntelliSustain, an AI agent for BMS..."           │ │
│  │ • Defines agent personality and capabilities               │ │
│  │ • Sets operational boundaries and constraints              │ │
│  │ • Establishes safety protocols                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  🔧 LAYER 2: TOOL & API INTEGRATION                            │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ • API-driven only responses                                │ │
│  │ • Function calling instructions                            │ │
│  │ • Error handling protocols                                 │ │
│  │ • Data validation rules                                    │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  📊 LAYER 3: OUTPUT FORMATTING                                 │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ • Markdown formatting with emojis                          │ │
│  │ • Consistent response structures                           │ │
│  │ • Device ID inclusion rules                               │ │
│  │ • Actionable guidance format                              │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  🎤 LAYER 4: INPUT PROCESSING                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ • Natural language understanding                           │ │
│  │ • Context extraction and validation                       │ │
│  │ • Ambiguity resolution                                     │ │
│  │ • Parameter extraction                                     │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 **Input Formatting via System Prompts**

### **1. 🎯 Natural Language Understanding**

```python
# System prompt for input processing
system_prompt = (
    "You are IntelliSustain, an AI agent for the IntelliSustain Smart Building Management System (BMS)..."
    "\n\nCore Responsibilities:\n"
    "- Understand and Respond to Queries: Accurately interpret user queries about building conditions"
    "- Execute Actuator Commands: Precisely execute user commands to adjust building parameters"
    "- Handle Ambiguity and Clarify: If a request is ambiguous, ask clarifying questions"
    "- Error Handling: If an API call fails, inform the user and suggest alternatives"
)
```

**What This Does:**
- ✅ **Interprets vague queries** like "Room 50 2nd floor ka temperature kya hai?"
- ✅ **Extracts parameters** (device, location, timeframe, severity)
- ✅ **Resolves ambiguity** by asking clarifying questions
- ✅ **Validates inputs** before API calls

### **2. 🎤 Context-Aware Input Processing**

```python
# Context-aware prompt building
context_prompt = ""
if recent_context:
    context_prompt = "\n\nRecent conversation context:\n"
    for ctx in recent_context:
        context_prompt += f"User: {ctx['query']}\nAssistant: {ctx['response'][:100]}...\n"
if device_id:
    context_prompt += f"\nCurrent device context: {device_id}"

full_prompt = f"{context_prompt}\n\nUser query: {query}\n\nProvide a helpful, informative response based on the context and query."
```

**What This Does:**
- ✅ **Remembers previous conversations** for context
- ✅ **Maintains device focus** across interactions
- ✅ **Resolves pronouns** like "it", "that device", "the room"
- ✅ **Builds on previous queries** for follow-up questions

### **3. 🔍 Parameter Extraction**

```python
# LLM-based parameter extraction
def extract_alarm_filters(input_text):
    prompt = f"""
    Extract the following from the user query (if present):
    - device name
    - date (as YYYY-MM-DD or relative like 'today', 'yesterday')
    - severity (CRITICAL, MAJOR, MINOR, WARNING, INDETERMINATE)
    Return as JSON: {{'device': ..., 'date': ..., 'severity': ...}}
    Query: {input_text}
    """
    response = llm.invoke([HumanMessage(content=prompt)]).content
    return json.loads(response)
```

**What This Does:**
- ✅ **Extracts structured data** from natural language
- ✅ **Normalizes dates** (today, yesterday, specific dates)
- ✅ **Standardizes severity levels** (critical, major, minor)
- ✅ **Identifies device names** from various formats

---

## 📊 **Output Formatting via System Prompts**

### **1. 🎨 Consistent Response Formatting**

```python
# System prompt for output formatting
system_prompt += (
    "\n\nResponse Format:\n"
    "- Use consistent markdown formatting with emojis for better readability\n"
    "- Provide clear, actionable information or specific error messages\n"
    "- Include device IDs and actual values when reporting data\n"
    "- Suggest alternatives when requests cannot be fulfilled\n"
)
```

**What This Does:**
- ✅ **Standardizes responses** across all interactions
- ✅ **Uses emojis** for visual clarity (🚨 alarms, 🌡️ temperature, ⚡ energy)
- ✅ **Includes device IDs** for traceability
- ✅ **Provides actionable guidance** instead of raw data

### **2. 📋 Structured Data Presentation**

```python
# Example: Formatted alarm response
def _format_enhanced_alarm_summary(self, alarms_data, query):
    # System prompt ensures consistent formatting
    summary = f"🚨 **Alarm Summary**\n\n"
    for alarm in alarms_data:
        summary += f"• **{alarm['severity']}**: {alarm['type']} - {alarm['location']}\n"
        summary += f"  📅 {alarm['timestamp']} | 🔧 {alarm['device_id']}\n\n"
    return summary
```

**What This Does:**
- ✅ **Transforms raw API data** into readable formats
- ✅ **Highlights important information** (severity, timestamps)
- ✅ **Groups related data** logically
- ✅ **Provides visual hierarchy** with markdown

### **3. 🎯 Actionable Response Generation**

```python
# System prompt for actionable responses
system_prompt += (
    "\n\nInteraction Flow:\n"
    "1. Receive user input and parse the query/command\n"
    "2. Identify intent (query or command)\n"
    "3. Extract and validate all necessary parameters\n"
    "4. If parameters are missing, prompt the user for clarification\n"
    "5. Formulate and execute the appropriate Inferrix API call\n"
    "6. Process the API response and provide clear, user-friendly response\n"
)
```

**What This Does:**
- ✅ **Guides response structure** for different query types
- ✅ **Ensures parameter validation** before API calls
- ✅ **Provides clear error messages** when things go wrong
- ✅ **Suggests next steps** for incomplete requests

---

## 🚀 **Real Examples of System Prompt Usage**

### **Example 1: Input Processing**

**User Input:** "Room 50 2nd floor ka temperature kya hai?"

**System Prompt Processing:**
```python
# 1. Extract location and parameter
extracted_params = {
    'device': 'Room 50 2nd floor',
    'parameter': 'temperature',
    'language': 'hinglish'
}

# 2. Validate and normalize
normalized_device = "2F-Room50-Thermostat"
normalized_query = "temperature"

# 3. Build API call
api_endpoint = f"devices/{normalized_device}/telemetry"
```

**Result:** Clean, structured API call with validated parameters

### **Example 2: Output Formatting**

**Raw API Response:**
```json
{
  "device_id": "2F-Room50-Thermostat",
  "temperature": 23.5,
  "humidity": 45.2,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**System Prompt Formatted Output:**
```
🌡️ **Temperature Reading - Room 50 (2nd Floor)**

**Current Conditions:**
• Temperature: **23.5°C** 
• Humidity: **45.2%**
• Device: 2F-Room50-Thermostat
• Last Updated: 10:30 AM

✅ **Status**: Normal operating range
```

### **Example 3: Error Handling**

**API Error:** `{"error": "Device not found", "code": 404}`

**System Prompt Formatted Error:**
```
❌ **Device Not Found**

**Issue**: Room 50 2nd floor thermostat is not available in the system.

**Possible Solutions:**
• Check if the device name is correct
• Verify the device is online and connected
• Try: "Show me all available thermostats"

**Available Similar Devices:**
• 2F-Room33-Thermostat
• 2F-Room34-Thermostat
• 2F-Room35-Thermostat
```

---

## 📊 **System Prompt Benefits**

### **✅ Input Processing Benefits**

| **Feature** | **Traditional Approach** | **Our System Prompt Approach** |
|-------------|-------------------------|--------------------------------|
| **Language Support** | English only | English + Hinglish + Mixed |
| **Parameter Extraction** | Manual regex | AI-powered extraction |
| **Context Handling** | None | Full conversation memory |
| **Ambiguity Resolution** | Error messages | Clarifying questions |
| **Validation** | Basic | Comprehensive |

### **✅ Output Formatting Benefits**

| **Feature** | **Raw API Response** | **System Prompt Formatted** |
|-------------|---------------------|----------------------------|
| **Readability** | JSON/XML | Human-friendly markdown |
| **Visual Appeal** | Plain text | Emojis and formatting |
| **Actionability** | Data only | Clear next steps |
| **Consistency** | Varies by API | Standardized format |
| **Error Handling** | Technical errors | User-friendly guidance |

---

## 🎯 **Key Advantages for Clients**

### **1. 🧠 Intelligent Input Processing**
- **Natural Language Understanding**: Handles conversational queries
- **Context Awareness**: Remembers previous interactions
- **Multi-language Support**: English + Hinglish seamlessly
- **Parameter Validation**: Ensures data quality before API calls

### **2. 📊 Professional Output Formatting**
- **Consistent Branding**: Standardized response format
- **Visual Clarity**: Emojis and markdown for better UX
- **Actionable Information**: Clear next steps and guidance
- **Error Recovery**: Helpful suggestions when things go wrong

### **3. 🔧 Technical Excellence**
- **API Integration**: Seamless connection to Inferrix API
- **Error Handling**: Graceful degradation and recovery
- **Performance**: Optimized for real-time responses
- **Scalability**: Handles multiple concurrent users

### **4. 💼 Business Value**
- **User Experience**: Professional, intuitive interface
- **Operational Efficiency**: Faster query resolution
- **Data Quality**: Validated inputs and structured outputs
- **Maintenance**: Easy to update and extend

---

## 🎤 **Client Presentation Points**

### **"How do you handle user input formatting?"**
*"We use advanced system prompts that intelligently process natural language, extract parameters, validate inputs, and maintain conversation context. This ensures accurate API calls and excellent user experience."*

### **"How do you format API responses?"**
*"Our system prompts transform raw API data into professional, actionable responses with consistent formatting, visual clarity, and helpful guidance for users."*

### **"What makes your approach different?"**
*"Unlike traditional chatbots that just pass through data, our system prompts create intelligent, context-aware interactions that feel natural and provide real business value."*

---

## 🎯 **Conclusion**

**Our system prompts are the intelligence layer that transforms raw API interactions into a sophisticated, user-friendly Agentic AI experience. They handle both input processing and output formatting to create seamless, professional interactions that drive real business value.**

**This is not just API integration - it's intelligent conversation management!** 🤖✨
