# Render Deployment Guide (Alternative to Railway)

## Quick Deployment to Render

If Railway doesn't work, Render is another excellent free option.

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Get $5 free credit monthly

### Step 2: Deploy Backend

1. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Set root directory to `backend/`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Environment Variables**
   ```
   INFERRIX_API_TOKEN=your_token
   OPENAI_API_KEY=your_key
   GOOGLE_API_KEY=your_key
   JWT_SECRET_KEY=your_secret
   ```

### Step 3: Deploy Frontend

1. **Create New Static Site**
   - Click "New +" → "Static Site"
   - Connect your GitHub repo
   - Set root directory to `frontend/`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`

2. **Environment Variables**
   ```
   VITE_API_URL=https://your-backend-service.onrender.com
   ```

### Step 4: Get URLs

- **Backend**: `https://your-backend-service.onrender.com`
- **Frontend**: `https://your-frontend-service.onrender.com`

### Step 5: Share with Team

Share the frontend URL with your team members!

## Render Benefits

✅ **Free Tier**: $5 monthly credit
✅ **Automatic HTTPS**: SSL included
✅ **Global CDN**: Fast worldwide
✅ **Easy Setup**: 5-minute deployment
✅ **Git Integration**: Auto-deploy on push
✅ **Custom Domains**: Add your domain later

## Alternative: Vercel + Railway

**Frontend on Vercel:**
1. Deploy frontend to Vercel (free)
2. Connect GitHub repo
3. Vercel auto-detects React app

**Backend on Railway:**
1. Deploy backend to Railway
2. Update frontend API URL

---

**Time**: 10 minutes
**Cost**: Free
**Sharing**: Instant URLs 