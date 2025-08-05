<<<<<<< HEAD
# 🚦 Inferrix AI Agent Demo

A **production-ready, enterprise-grade AI Agent** that integrates with the Inferrix IoT platform to provide intelligent monitoring, alarm management, and device health insights through natural language conversations.

## 🌟 Key Features

### 🤖 **Intelligent AI Agent**
- **Natural Language Processing**: Chat with the AI using plain English
- **Multi-Tool Routing**: Automatically selects the right tool based on your query
- **Context-Aware Responses**: Understands device names, severity levels, and time ranges
- **Graceful Fallbacks**: Helpful suggestions when queries aren't understood
- **15+ specialized tools for Inferrix operations**:

### 🔐 **Enterprise Security**
- **JWT Authentication**: Secure token-based authentication
- **Rate Limiting**: Protection against API abuse (30 requests/minute)
- **CORS Protection**: Configurable cross-origin resource sharing
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **No hardcoded data - all from live Inferrix API**:

### 📊 **Real-Time Data Integration**
- **Live Inferrix API**: All data comes directly from Inferrix, no hardcoded values
- **Dynamic Device Discovery**: Device dropdown populated from live API
- **Real-Time Alarms**: Active alarm monitoring and management
- **Telemetry Data**: Temperature, humidity, battery, occupancy, and motion sensors

### 🎨 **Modern UI/UX**
- **Professional Design**: Clean, modern interface following enterprise standards
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Interactive Elements**: Clickable prompt suggestions, loading states, error banners
- **Accessibility**: ARIA labels, keyboard navigation, screen reader support

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **LangChain**: AI/LLM orchestration framework
- **LangGraph**: Stateful AI agent workflows
- **PostgreSQL**: Reliable database for user management
- **JWT**: Secure authentication tokens

### Frontend
- **React 18**: Modern JavaScript framework
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API communication
- **Vite**: Fast build tool and dev server

### AI/LLM
- **OpenAI GPT-4o**: Primary LLM for natural language understanding
- **Google Gemini Pro**: Fallback LLM option
- **Custom Tool Integration**: 15+ specialized tools for Inferrix operations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Inferrix API access

### 1. Clone and Setup
```bash
git clone <repository-url>
cd Inferrix_AI_Agent_Demo_Complete_Final
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration
Create `.env` file in the backend directory:
```env
INFERRIX_API_TOKEN=your_inferrix_api_token_here
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here  # Optional
DATABASE_URL=postgresql://user:password@localhost/inferrix_agent
JWT_SECRET_KEY=your_jwt_secret_key_here
```

### 4. Database Setup
```bash
# Start PostgreSQL and create database
createdb inferrix_agent

# Initialize database (if needed)
python init_db.py
```

### 5. Frontend Setup
```bash
cd frontend
npm install
```

### 6. Start the Application
```bash
# Terminal 1: Start backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend
cd frontend
npm run dev
```

### 7. Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🎯 Demo Script

### Login
1. Use credentials: `tech@inferrix.com` / `password123`
2. Observe JWT token generation and secure session

### Core Capabilities Demo

#### 1. **Alarm Management**
```
"Show all critical alarms"
"Show me alarms for Tower A"
"List devices with low battery"
"Show top 3 alarm types"
```

#### 2. **Device Monitoring**
```
"Check if device HVAC-01 is online"
"Show temperature for IAQ Sensor V2"
"Get humidity readings for RH/T Sensor"
"Check device health status"
```

#### 3. **Advanced Queries**
```
"Summarize alarms from the last 24 hours"
"Acknowledge alarm 12345"
"What's the highest severity alarm?"
"Show telemetry health for all devices"
```

#### 4. **Error Handling Demo**
- Try invalid device names
- Test with expired JWT tokens
- Observe graceful error messages

### UI/UX Features to Highlight
- **Dynamic Device Dropdown**: Shows real devices from Inferrix API
- **Prompt Suggestions**: Clickable quick-start queries
- **Loading States**: Professional spinners and progress indicators
- **Error Banners**: Clear, actionable error messages
- **Responsive Design**: Test on different screen sizes

## 🔧 API Endpoints

### Authentication
- `POST /login` - Authenticate user and get JWT token

### Chat & AI
- `POST /chat` - Process natural language queries through AI agent
- `GET /api/info` - Get API capabilities and endpoints

### Inferrix Integration
- `GET /inferrix/alarms` - Get active alarms
- `GET /inferrix/devices` - Get all devices
- `GET /health` - Check Inferrix API connectivity

## 🧠 AI Agent Tools

The agent has 15+ specialized tools:

1. **Alarm Tools**
   - `alarms` - Fetch active alarms
   - `alarms_by_device` - Device-specific alarms
   - `acknowledge` - Acknowledge alarms
   - `alarm_types` - Top alarm categories

2. **Device Tools**
   - `devices` - List all devices
   - `health` - Device health checks
   - `online` - Online status
   - `telemetry_health` - Data transmission status

3. **Telemetry Tools**
   - `temperature` - Temperature readings
   - `telemetry` - Sensor data (humidity, battery, etc.)

4. **Analytics Tools**
   - `severity` - Highest alarm severity
   - `summarize_alarms` - 24h alarm summary
   - `low_battery` - Battery status
   - `predict` - Overheat risk prediction

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend│    │  Inferrix API   │
│                 │    │                 │    │                 │
│ • Chat UI       │◄──►│ • JWT Auth      │◄──►│ • Alarms        │
│ • Device Select │    │ • Rate Limiting │    │ • Devices       │
│ • Error Handling│    │ • AI Agent      │    │ • Telemetry     │
│ • Responsive    │    │ • Tool Routing  │    │ • Health Data   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   PostgreSQL    │
                       │                 │
                       │ • User Accounts │
                       │ • Session Data  │
                       └─────────────────┘
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based sessions
- **Rate Limiting**: 30 requests per minute per IP
- **Input Validation**: All inputs validated and sanitized
- **Error Handling**: No sensitive data in error messages
- **CORS Protection**: Configurable cross-origin policies

## 📱 Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers

## 🚨 Production Deployment

### Environment Variables
```env
# Required
INFERRIX_API_TOKEN=your_token
OPENAI_API_KEY=your_key
DATABASE_URL=postgresql://user:pass@host/db
JWT_SECRET_KEY=your_secret

# Optional
GOOGLE_API_KEY=your_key
CORS_ORIGINS=https://yourdomain.com
RATE_LIMIT_REQUESTS=30
RATE_LIMIT_WINDOW=60
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🐛 Troubleshooting

### Common Issues

1. **JWT Token Expired**
   - Solution: Re-login or refresh token
   - UI automatically handles this

2. **Inferrix API Unreachable**
   - Check API token validity
   - Verify network connectivity
   - Check Inferrix service status

3. **Rate Limit Exceeded**
   - Wait 1 minute before retrying
   - Reduce request frequency

4. **Device Not Found**
   - Verify device name spelling
   - Check if device exists in Inferrix
   - Use device dropdown for exact names

### Debug Mode
```bash
# Enable debug logging
export DEBUG=1
uvicorn main:app --reload --log-level debug
```

## 📈 Performance

- **Response Time**: < 2 seconds for most queries
- **Concurrent Users**: 100+ with rate limiting
- **API Calls**: Optimized with caching and timeouts
- **Memory Usage**: < 512MB for typical usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is proprietary software for Inferrix AI Agent demonstration purposes.

---

## 🎉 Demo Success Checklist

Before your demo, ensure:

- [ ] All services are running (backend, frontend, database)
- [ ] Inferrix API is accessible
- [ ] Test login with demo credentials
- [ ] Try all major query types
- [ ] Test error scenarios
- [ ] Verify responsive design on different screens
- [ ] Have backup demo data ready
- [ ] Prepare demo script and key talking points

**Good luck with your demo! 🚀**
=======
# IntelliSustain
>>>>>>> 721329a9d4c3567832b01e7a028223bc0c84bddd
