Write-Host "Starting ByteForge Penetration Testing Framework..." -ForegroundColor Cyan

# Check for .env file
if (-not (Test-Path "backend\.env")) {
    Write-Host "WARNING: backend\.env not found! Please create it first." -ForegroundColor Yellow
    exit
}

# Start Backend in a new window
Write-Host "[+] Starting Backend (Port 8000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "cd backend; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

# Start Frontend in a new window
Write-Host "[+] Starting Frontend (Port 5173)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "cd frontend; npm run dev"

Write-Host "[OK] Systems initialization triggered." -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Gray
Write-Host "Backend Docs: http://localhost:8000/docs" -ForegroundColor Gray
