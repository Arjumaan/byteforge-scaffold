@echo off
title ByteForge - Dependency Installer
echo ========================================================
echo   INSTALLING BYTEFORGE DEPENDENCIES
echo ========================================================
echo.

echo [1/3] Installing Backend Python Dependencies...
cd backend

:: Try basic python first (assuming user has correct version)
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [!] Error installing Python dependencies.
    echo [!] Ensure Python is installed and in PATH.
    pause
    exit /b
)

:: Install extra security packages explicitly if missing
python -m pip install passlib bcrypt cryptography
cd ..

echo.
echo [2/3] Installing Frontend Node Dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo.
    echo [!] Error installing Node dependencies.
    echo [!] Ensure Node.js is installed.
    pause
    exit /b
)
cd ..

echo.
echo [3/3] Installing Security Tools (Go & Nuclei, Katana)...
:: Check if Go is installed
go version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Go is NOT installed. Installing via Winget...
    winget install GoLang.Go --accept-source-agreements --accept-package-agreements
    if %errorlevel% neq 0 (
        echo [!] Failed to install Go. Please install manually from https://go.dev/dl/
    ) else (
        echo [!] Go installed. Refreshing environment variables...
        call RefreshEnv.cmd >nul 2>&1
    )
)

echo.
echo [*] Installing Nuclei, Katana, GoSpider...
set "GOPATH=%USERPROFILE%\go"
set "PATH=%PATH%;%GOPATH%\bin"

go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/jaeles-project/gospider@latest

echo.
echo ========================================================
echo   INSTALLATION COMPLETE
echo ========================================================
echo.
echo You can now run 'run_system.bat' to start the application.
pause
