# 🚨 Railway Deployment Fix

## Problem
Railway is only finding `README.md` and failing to detect your backend code.

## Solution

### Step 1: Fix Repository Structure
Run the fix script:
```bash
fix_railway_deployment.bat
```

This will:
- Add all backend/ and frontend/ files to git
- Push complete source code to GitHub
- Ensure Railway can detect your Python backend

### Step 2: Redeploy on Railway

**Option A: Redeploy Existing Project**
1. Go to your Railway project
2. Click "Deploy" or "Redeploy"
3. Railway should now detect the backend/ directory

**Option B: Create New Project (Recommended)**
1. Delete the current Railway project
2. Go to [railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select: `satyarthgaur-aionos/IntelliSustain`
5. Railway will now detect the proper structure

### Step 3: Configure Service Settings

When creating the new project, Railway should detect:
- **Backend Service**: `backend/` directory with Python files
- **Frontend Service**: `frontend/` directory with React files

### Step 4: Set Environment Variables

In Railway dashboard, add:
```
INFERRIX_API_TOKEN=your_token
OPENAI_API_KEY=your_key
GOOGLE_API_KEY=your_key
JWT_SECRET_KEY=your_secret
```

## Expected Structure After Fix

Your GitHub repo should contain:
```
IntelliSustain/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── railway.json
│   ├── Procfile
│   └── nixpacks.toml
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   └── src/
├── railway.toml
└── README.md
```

## Troubleshooting

### If Still Failing:
1. **Check GitHub**: Ensure all files are pushed to [https://github.com/satyarthgaur-aionos/IntelliSustain](https://github.com/satyarthgaur-aionos/IntelliSustain)
2. **Verify Structure**: Backend/ and frontend/ folders should be visible
3. **Manual Deploy**: Try deploying backend and frontend as separate services

### Alternative: Manual Service Creation
1. Create **Backend Service**:
   - Root directory: `backend/`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. Create **Frontend Service**:
   - Root directory: `frontend/`
   - Build command: `npm install && npm run build`
   - Start command: `npm run preview`

## Quick Commands

```bash
# Fix and push all code
fix_railway_deployment.bat

# Check what's in your repo
git ls-files

# Verify backend files are included
git ls-files | grep backend/
```

---

**Time to fix**: 5 minutes
**Expected result**: Railway detects backend/ directory and deploys successfully 