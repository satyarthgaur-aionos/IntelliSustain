# Cloudflare Tunnel Setup Guide for Inferrix AI Agent Demo

## Overview
This guide helps you set up Cloudflare Tunnel to share your local development environment with your team members.

## Prerequisites
1. Cloudflare account with a domain
2. Windows machine with PowerShell
3. All three services running locally (Vite, FastAPI, MCP)

## Step 1: Install Cloudflare Tunnel

### Option A: Using winget (Recommended)
```powershell
winget install Cloudflare.cloudflared
```

### Option B: Manual Installation
1. Go to https://github.com/cloudflare/cloudflared/releases
2. Download `cloudflared-windows-amd64.exe`
3. Rename to `cloudflared.exe` and add to your PATH

## Step 2: Authenticate with Cloudflare

```bash
cloudflared tunnel login
```

This will:
- Open your browser
- Ask you to authorize cloudflared
- Download a certificate file

## Step 3: Create Tunnel

```bash
cloudflared tunnel create inferrix-ai-demo
```

This creates a tunnel and saves credentials to `~/.cloudflared/`.

## Step 4: Configure Your Domain

1. Go to your Cloudflare dashboard
2. Add your domain if not already added
3. Create DNS records for each service:

```
Type: CNAME
Name: inferrix-frontend
Target: [your-tunnel-id].cfargotunnel.com
Proxy: Enabled

Type: CNAME  
Name: inferrix-api
Target: [your-tunnel-id].cfargotunnel.com
Proxy: Enabled

Type: CNAME
Name: inferrix-mcp
Target: [your-tunnel-id].cfargotunnel.com
Proxy: Enabled
```

## Step 5: Update Configuration

1. Replace `your-domain.com` in `cloudflare-tunnels.yml` with your actual domain
2. Update `frontend/src/config/api.js` with your domain URLs

## Step 6: Start Services

### Option A: Use the batch script
```bash
start_with_cloudflare.bat
```

### Option B: Manual startup
1. Start FastAPI: `cd backend && python main.py`
2. Start MCP: `cd backend && python mcp_server.py`  
3. Start Vite: `cd frontend && npm run dev`
4. Start Tunnel: `cloudflared tunnel --config cloudflare-tunnels.yml run`

## Step 7: Share with Team

Your team can now access:
- **Frontend**: https://inferrix-frontend.your-domain.com
- **API**: https://inferrix-api.your-domain.com
- **MCP**: https://inferrix-mcp.your-domain.com

## Troubleshooting

### Common Issues:

1. **"Connection refused"**
   - Ensure all local services are running
   - Check firewall settings
   - Verify ports are correct

2. **"Hostname not found"**
   - Check DNS records in Cloudflare
   - Ensure tunnel is running
   - Verify domain configuration

3. **CORS errors**
   - Backend is already configured with `allowedHosts: 'all'`
   - Check if API URLs are correct in frontend

### Debug Commands:

```bash
# Check tunnel status
cloudflared tunnel list

# View tunnel logs
cloudflared tunnel logs inferrix-ai-demo

# Test tunnel connection
cloudflared tunnel info inferrix-ai-demo
```

## Security Notes

1. **Temporary Solution**: This is for development/testing only
2. **Production**: Use proper deployment (Railway, AWS, etc.)
3. **Access Control**: Consider adding authentication to your tunnel
4. **Monitoring**: Monitor tunnel usage in Cloudflare dashboard

## Next Steps

When ready for production:
1. Deploy to Railway/AWS
2. Set up proper domain and SSL
3. Configure production environment variables
4. Set up monitoring and logging 