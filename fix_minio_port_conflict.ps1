# Fix MinIO Port Conflict
# Kill the Python process that's interfering with port 9000

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Fixing MinIO Port Conflict" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

Write-Host "`nProblem: A Python process is interfering with MinIO on port 9000" -ForegroundColor Yellow

# Kill the Python process on port 9000
Write-Host "`n[1] Stopping Python process on port 9000..." -ForegroundColor Yellow
try {
    Stop-Process -Id 21448 -Force -ErrorAction SilentlyContinue
    Write-Host "    [OK] Stopped Python process" -ForegroundColor Green
} catch {
    Write-Host "    [INFO] Process may have already stopped" -ForegroundColor Gray
}

Start-Sleep -Seconds 2

# Verify port 9000 is clear
Write-Host "`n[2] Verifying port 9000..." -ForegroundColor Yellow
$connections = Get-NetTCPConnection -LocalPort 9000 -ErrorAction SilentlyContinue
if ($connections) {
    Write-Host "    Processes on port 9000:" -ForegroundColor Gray
    foreach ($conn in $connections) {
        $proc = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
        if ($proc) {
            Write-Host "      - $($proc.ProcessName) (PID: $($proc.Id))" -ForegroundColor Gray
        }
    }
} else {
    Write-Host "    [OK] Port 9000 is clear" -ForegroundColor Green
}

# Now try the mc alias command
Write-Host "`n[3] Testing mc alias command..." -ForegroundColor Yellow
Write-Host "    Waiting 3 seconds for MinIO to stabilize..." -ForegroundColor Gray
Start-Sleep -Seconds 3

try {
    $result = mc alias set myminio http://127.0.0.1:9000 minioadmin minioadmin 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    [SUCCESS] mc alias set successfully!" -ForegroundColor Green
    } else {
        Write-Host "    [ERROR] mc alias command failed" -ForegroundColor Red
        Write-Host "    $result" -ForegroundColor Red
    }
} catch {
    Write-Host "    [ERROR] $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "NEXT STEPS" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "`nIf the alias command still fails, try:" -ForegroundColor White
Write-Host "1. Use 'localhost' instead:" -ForegroundColor Gray
Write-Host "   mc alias set myminio http://localhost:9000 minioadmin minioadmin" -ForegroundColor Gray
Write-Host "`n2. Or access MinIO Console directly:" -ForegroundColor Gray
Write-Host "   http://127.0.0.1:9001" -ForegroundColor Gray
Write-Host "`n3. Or use PySpark directly (no mc needed):" -ForegroundColor Gray
Write-Host "   Your PySpark code already has the correct S3A configuration!" -ForegroundColor Gray
Write-Host "============================================================" -ForegroundColor Cyan
