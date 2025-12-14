# MinIO Restart Script
# This script will stop any running MinIO instances and start a fresh one

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "MinIO Restart Script" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Step 1: Stop existing MinIO processes
Write-Host "`n[1] Stopping existing MinIO processes..." -ForegroundColor Yellow
try {
    $minioProcesses = Get-Process -Name "minio" -ErrorAction SilentlyContinue
    if ($minioProcesses) {
        $minioProcesses | Stop-Process -Force
        Write-Host "    [OK] Stopped MinIO process(es)" -ForegroundColor Green
        Start-Sleep -Seconds 2
    } else {
        Write-Host "    [INFO] No MinIO processes running" -ForegroundColor Gray
    }
} catch {
    Write-Host "    [ERROR] Failed to stop MinIO: $_" -ForegroundColor Red
}

# Step 2: Create data directory
Write-Host "`n[2] Setting up MinIO data directory..." -ForegroundColor Yellow
$dataDir = "C:\minio-data"
try {
    if (-not (Test-Path $dataDir)) {
        New-Item -ItemType Directory -Force -Path $dataDir | Out-Null
        Write-Host "    [OK] Created directory: $dataDir" -ForegroundColor Green
    } else {
        Write-Host "    [OK] Directory exists: $dataDir" -ForegroundColor Green
    }
} catch {
    Write-Host "    [ERROR] Failed to create directory: $_" -ForegroundColor Red
    exit 1
}

# Step 3: Clear proxy settings
Write-Host "`n[3] Clearing proxy settings..." -ForegroundColor Yellow
$env:HTTP_PROXY = ""
$env:HTTPS_PROXY = ""
$env:NO_PROXY = "localhost,127.0.0.1"
Write-Host "    [OK] Proxy settings cleared" -ForegroundColor Green

# Step 4: Start MinIO
Write-Host "`n[4] Starting MinIO server..." -ForegroundColor Yellow
Write-Host "    Data directory: $dataDir" -ForegroundColor Gray
Write-Host "    API Port: 9000" -ForegroundColor Gray
Write-Host "    Console Port: 9001" -ForegroundColor Gray
Write-Host ""
Write-Host "    MinIO will start in a new window..." -ForegroundColor Cyan
Write-Host "    Keep that window open while using MinIO!" -ForegroundColor Cyan
Write-Host ""

try {
    # Start MinIO in a new window
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "minio server $dataDir --console-address :9001"
    
    Write-Host "    [OK] MinIO server started" -ForegroundColor Green
    Write-Host ""
    Write-Host "    Waiting 5 seconds for MinIO to initialize..." -ForegroundColor Gray
    Start-Sleep -Seconds 5
    
} catch {
    Write-Host "    [ERROR] Failed to start MinIO: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "    Make sure MinIO is installed. Check with: minio --version" -ForegroundColor Yellow
    exit 1
}

# Step 5: Test connection
Write-Host "`n[5] Testing MinIO connection..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:9000/minio/health/live" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "    [OK] MinIO is responding!" -ForegroundColor Green
} catch {
    Write-Host "    [WARNING] MinIO might still be starting up..." -ForegroundColor Yellow
    Write-Host "    Wait a few more seconds and try the mc alias command" -ForegroundColor Yellow
}

# Step 6: Instructions
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "NEXT STEPS" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Set up MinIO alias:" -ForegroundColor White
Write-Host "   mc alias set myminio http://127.0.0.1:9000 minioadmin minioadmin" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Test the connection:" -ForegroundColor White
Write-Host "   mc admin info myminio" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Access MinIO Console in browser:" -ForegroundColor White
Write-Host "   http://127.0.0.1:9001" -ForegroundColor Gray
Write-Host "   Username: minioadmin" -ForegroundColor Gray
Write-Host "   Password: minioadmin" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
