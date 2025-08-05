# 🚀 Quick Deployment Setup

## Immediate Solution for Team Sharing

Since you're short on time, here are the fastest options:

### Option 1: Railway (Recommended - 10 minutes)

1. **Push to GitHub** (if not done):
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy to Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects services

3. **Set Environment Variables** in Railway dashboard:
   ```
   INFERRIX_API_TOKEN=your_token
   OPENAI_API_KEY=your_key
   GOOGLE_API_KEY=your_key
   JWT_SECRET_KEY=your_secret
   ```

4. **Get URLs** and share frontend URL with team!

### Option 2: Render (Alternative - 10 minutes)

1. Go to [render.com](https://render.com)
2. Deploy backend as Web Service
3. Deploy frontend as Static Site
4. Set environment variables
5. Share URLs

### Option 3: Vercel + Railway (Hybrid - 15 minutes)

1. **Frontend on Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repo
   - Set root directory to `frontend/`
   - Vercel auto-detects React app

2. **Backend on Railway**:
   - Deploy backend to Railway
   - Update frontend API URL

## Environment Variables Needed

### Backend (Railway/Render):
```
INFERRIX_API_TOKEN=your_inferrix_token
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
JWT_SECRET_KEY=your_jwt_secret
```

### Frontend:
```
VITE_API_URL=https://your-backend-url.railway.app
```

## Quick Commands

```bash
# Check if git is ready
git status

# If not committed
git add .
git commit -m "Ready for deployment"
git push origin main

# Then deploy to Railway/Render/Vercel
```

## Expected URLs After Deployment

- **Railway**: `https://your-app.railway.app`
- **Render**: `https://your-app.onrender.com`
- **Vercel**: `https://your-app.vercel.app`

## Troubleshooting

1. **Build fails**: Check Railway/Render logs
2. **CORS errors**: Backend CORS allows all origins
3. **API not working**: Check environment variables
4. **Frontend not loading**: Check API URL configuration

## Cost

- **Railway**: Free tier ($5 credit)
- **Render**: Free tier ($5 credit)
- **Vercel**: Free tier (unlimited)

---

**Time to deploy**: 10-15 minutes
**Time to share**: Instant
**Cost**: Free 