@echo off
echo Launching all Cloudflare tunnels...

start "Vite Frontend" cmd /k "C:\cloudflared\cloudflared.exe tunnel --url http://127.0.0.1:5173"
start "Backend API" cmd /k "C:\cloudflared\cloudflared.exe tunnel --url http://127.0.0.1:8000"
start "MCP Server" cmd /k "C:\cloudflared\cloudflared.exe tunnel --url http://127.0.0.1:8001"

echo ✅ All tunnels launched in new windows.
echo 🔗 Copy the URLs from the cloudflared console outputs.
pause