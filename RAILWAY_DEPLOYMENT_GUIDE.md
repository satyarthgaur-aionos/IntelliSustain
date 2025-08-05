# Railway Deployment Guide for Inferrix AI Agent

## Quick Deployment to Railway

This guide will help you deploy your Inferrix AI Agent application to Railway in under 10 minutes.

### Prerequisites
1. GitHub account
2. Railway account (free at railway.app)
3. Your code pushed to GitHub

### Step 1: Prepare Your Repository

1. **Push your code to GitHub** (if not already done)
2. **Ensure all files are committed**

### Step 2: Deploy to Railway

#### Option A: Deploy All Services Together (Recommended)

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will automatically detect the services

#### Option B: Deploy Services Separately

**Backend Service:**
1. Create new project in Railway
2. Connect to your GitHub repo
3. Set root directory to `backend/`
4. Railway will use the `railway.json` and `Procfile` automatically

**Frontend Service:**
1. Create another project in Railway
2. Connect to same GitHub repo
3. Set root directory to `frontend/`
4. Railway will build and serve the React app

### Step 3: Configure Environment Variables

In Railway dashboard, add these environment variables:

```
# Backend Environment Variables
INFERRIX_API_TOKEN=your_inferrix_token
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
JWT_SECRET_KEY=your_jwt_secret
DATABASE_URL=your_database_url

# Frontend Environment Variables
VITE_API_URL=https://your-backend-service.railway.app
```

### Step 4: Get Your URLs

After deployment, Railway will provide:
- **Backend URL**: `https://your-backend-service.railway.app`
- **Frontend URL**: `https://your-frontend-service.railway.app`

### Step 5: Update Frontend Configuration

Update `frontend/src/config/api.js` with your Railway backend URL:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://your-backend-service.railway.app';

export const API_ENDPOINTS = {
    LOGIN: `${API_BASE_URL}/login`,
    CHAT: `${API_BASE_URL}/chat`,
    ENHANCED_CHAT: `${API_BASE_URL}/chat/enhanced`,
    ALARMS: `${API_BASE_URL}/inferrix/alarms`,
    DEVICES: `${API_BASE_URL}/inferrix/devices`,
    HEALTH: `${API_BASE_URL}/health`,
};
```

### Step 6: Share with Your Team

Share the frontend URL with your team members:
```
https://your-frontend-service.railway.app
```

## Troubleshooting

### Common Issues:

1. **Build Failures**: Check Railway logs for missing dependencies
2. **CORS Errors**: Backend CORS is configured to allow all origins
3. **API Connection**: Ensure environment variables are set correctly
4. **Port Issues**: Railway automatically handles port assignment

### Quick Fixes:

1. **Restart Service**: Use Railway dashboard to restart services
2. **Check Logs**: View real-time logs in Railway dashboard
3. **Redeploy**: Trigger a new deployment from Railway dashboard

## Cost

Railway offers:
- **Free Tier**: $5 credit monthly (sufficient for demo)
- **Pay-as-you-go**: Only pay for actual usage
- **Auto-scaling**: Handles traffic automatically

## Benefits of Railway

✅ **Instant Deployment**: Deploy in minutes
✅ **Automatic HTTPS**: SSL certificates included
✅ **Global CDN**: Fast loading worldwide
✅ **Auto-scaling**: Handles traffic spikes
✅ **Easy sharing**: Direct URLs for team access
✅ **Real-time logs**: Debug issues quickly
✅ **Environment variables**: Secure configuration
✅ **Git integration**: Automatic deployments

## Alternative: Vercel (Frontend Only)

If you prefer Vercel for frontend:

1. Deploy frontend to Vercel
2. Deploy backend to Railway
3. Update frontend API URL to point to Railway backend

## Support

- Railway Documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Railway Status: https://status.railway.app

---

**Estimated Time**: 10-15 minutes
**Cost**: Free tier available
**Sharing**: Instant URL sharing with team 