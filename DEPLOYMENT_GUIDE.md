# 🚀 Quick Deployment Guide

## Option 1: Railway (Recommended - 5 minutes)

**Railway is the fastest and most reliable option for your demo.**

### Steps:
1. **Sign up at [railway.app](https://railway.app)** (free tier available)
2. **Connect your GitHub repository**
3. **Deploy automatically** - Railway will detect your setup and deploy all 3 services
4. **Set environment variables:**
   - `INFERRIX_API_TOKEN` (your API token)
   - `JWT_SECRET_KEY` (auto-generated)

### Benefits:
- ✅ **Free tier** with generous limits
- ✅ **Automatic HTTPS** 
- ✅ **Custom domains** available
- ✅ **Zero configuration** needed
- ✅ **Real-time logs** and monitoring

---

## Option 2: Render (Alternative - 10 minutes)

### Steps:
1. **Sign up at [render.com](https://render.com)** (free tier available)
2. **Connect your GitHub repository**
3. **Deploy using the `render.yaml` configuration**
4. **Set environment variables** in the dashboard

### Benefits:
- ✅ **Free tier** available
- ✅ **Automatic HTTPS**
- ✅ **Custom domains**
- ✅ **Good performance**

---

## Option 3: Quick Local Tunnel (Immediate - 2 minutes)

**For immediate sharing without deployment:**

### Steps:
1. **Install Node.js** if not already installed
2. **Run the quick deployment script:**
   ```bash
   python quick_deploy.py
   ```
3. **Share the generated URLs** with your team

### Benefits:
- ✅ **Instant sharing** (no deployment needed)
- ✅ **Works immediately**
- ⚠️ **URLs change on restart**
- ⚠️ **Requires your computer to stay on**

---

## Option 4: Manual Local Tunnel (If script doesn't work)

### Steps:
1. **Install localtunnel:**
   ```bash
   npm install -g localtunnel
   ```

2. **Start your services:**
   ```bash
   # Terminal 1 - Backend
   cd backend && python main.py
   
   # Terminal 2 - MCP Server  
   cd backend && python mcp_server.py
   
   # Terminal 3 - Frontend
   cd frontend && npm run dev
   ```

3. **Create tunnels:**
   ```bash
   # Terminal 4 - Backend tunnel
   lt --port 8000 --subdomain inferrix-api
   
   # Terminal 5 - MCP tunnel
   lt --port 8001 --subdomain inferrix-mcp
   
   # Terminal 6 - Frontend tunnel
   lt --port 5173 --subdomain inferrix-app
   ```

4. **Share the URLs** that appear in each terminal

---

## Environment Variables Required

Make sure to set these in your deployment platform:

```bash
INFERRIX_API_TOKEN=your_inferrix_api_token_here
JWT_SECRET_KEY=any_random_string_for_jwt_signing
```

---

## Troubleshooting

### Common Issues:

1. **Port already in use:**
   ```bash
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   
   # Mac/Linux
   lsof -ti:8000 | xargs kill -9
   ```

2. **Node.js not found:**
   - Download from [nodejs.org](https://nodejs.org/)

3. **Python not found:**
   - Install Python 3.8+ from [python.org](https://python.org/)

4. **localtunnel not working:**
   - Try using ngrok instead: `npm install -g ngrok`
   - Or use Railway/Render deployment

---

## Recommendation

**For your demo, I recommend:**

1. **Immediate:** Use Option 3 (Quick Local Tunnel) for instant sharing
2. **Long-term:** Deploy to Railway for permanent URLs

**Railway is the best choice because:**
- ✅ **Zero configuration** needed
- ✅ **Automatic deployment** from GitHub
- ✅ **Free tier** is generous
- ✅ **Custom domains** available
- ✅ **Real-time monitoring**

---

## Quick Start Commands

```bash
# Option 1: Railway (recommended)
# Just push to GitHub and connect to Railway

# Option 2: Quick local tunnel
python quick_deploy.py

# Option 3: Manual tunnel
cd backend && python main.py &
cd backend && python mcp_server.py &
cd frontend && npm run dev &
lt --port 8000 --subdomain inferrix-api &
lt --port 8001 --subdomain inferrix-mcp &
lt --port 5173 --subdomain inferrix-app
```

**Your demo will be ready in under 5 minutes! 🎉** 