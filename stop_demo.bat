@echo off
title Force Stopping Inferrix AI Agent Demo
echo.
echo ========================================
echo    FORCE STOPPING ALL DEMO WINDOWS
echo ========================================
echo.

echo Killing FastAPI (uvicorn) servers...
taskkill /f /im uvicorn.exe >nul 2>&1

echo Killing Node.js (Vite/React) servers...
taskkill /f /im node.exe >nul 2>&1

timeout /t 2 >nul

echo Closing any remaining demo windows by title...
taskkill /f /fi "WINDOWTITLE eq Inferrix AI Agent - Backend*" >nul 2>&1
taskkill /f /fi "WINDOWTITLE eq Inferrix AI Agent - MCP Server*" >nul 2>&1
taskkill /f /fi "WINDOWTITLE eq Inferrix AI Agent - Frontend*" >nul 2>&1

echo Force closing all command prompt windows...
taskkill /f /im cmd.exe >nul 2>&1

echo.
echo ========================================
echo    ALL DEMO WINDOWS AND SERVERS CLOSED
echo ========================================
echo.
pause 