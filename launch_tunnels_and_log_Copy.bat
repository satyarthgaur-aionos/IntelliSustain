@echo off
echo Launching all tunnels...

setlocal

:: Output file
set LOGFILE=tunnel-urls.txt
echo [Tunnel URLs - %DATE% %TIME%] > %LOGFILE%
echo ---------------------------------------- >> %LOGFILE%

:: Launch Vite Tunnel and capture URL
echo Starting Vite frontend tunnel...
for /f "tokens=*" %%i in ('C:\cloudflared\cloudflared.exe tunnel --url http://127.0.0.1:5173 2^>nul ^| findstr /i "https://"') do (
    echo Frontend (Vite): %%i >> %LOGFILE%
    echo Vite frontend available at: %%i
)

:: Launch FastAPI Tunnel and capture URL
echo Starting FastAPI backend tunnel...
for /f "tokens=*" %%i in ('C:\cloudflared\cloudflared.exe tunnel --url http://127.0.0.1:8000 2^>nul ^| findstr /i "https://"') do (
    echo Backend (FastAPI): %%i >> %LOGFILE%
    echo FastAPI backend available at: %%i
)

:: Launch MCP Tunnel and capture URL
echo Starting MCP tunnel...
for /f "tokens=*" %%i in ('C:\cloudflared\cloudflared.exe tunnel --url http://127.0.0.1:8001 2^>nul ^| findstr /i "https://"') do (
    echo MCP Server: %%i >> %LOGFILE%
    echo MCP server available at: %%i
)

echo ---------------------------------------- >> %LOGFILE%
echo Done! Tunnel URLs saved to: %LOGFILE%
echo All tunnels launched!
pause
