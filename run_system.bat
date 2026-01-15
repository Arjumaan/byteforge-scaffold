@echo off
title ByteForge - System Launcher
echo ========================================================
echo   STARTING BYTEFORGE SECURITY FRAMEWORK
echo ========================================================
echo.

:: Add Go bin to path for this session
set "PATH=%PATH%;%USERPROFILE%\go\bin"

echo [1/2] Starting Backend (FastAPI)...
start "ByteForge Backend" cmd /k "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo [2/2] Starting Frontend (Vite)...
start "ByteForge Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo [!] Services started in new windows.
echo [!] Backend: http://localhost:8000/docs
echo [!] Frontend: http://localhost:5173
echo.
echo Press any key to shutdown both services...
pause >nul

taskkill /FI "WINDOWTITLE eq ByteForge Backend" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq ByteForge Frontend" /T /F >nul 2>&1
echo [!] Services stopped.
