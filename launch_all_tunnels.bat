@echo off
set LOGFILE=tunnel-urls.txt

:: Clear previous log
echo [Tunnel URLs - %DATE% %TIME%] > %LOGFILE%
echo -------------------------------------------- >> %LOGFILE%

:: Launch each tunnel in a new CMD window
start "Vite UI Tunnel" cmd /k "cloudflared tunnel --url http://127.0.0.1:5173"
start "FastAPI Backend Tunnel" cmd /k "cloudflared tunnel --url http://127.0.0.1:8000"
start "MCP Server Tunnel" cmd /k "cloudflared tunnel --url http://127.0.0.1:8001"

echo Tunnels are launching... check %LOGFILE% for public URLs.
pause
