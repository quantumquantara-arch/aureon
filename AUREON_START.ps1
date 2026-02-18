# AUREON Startup Script for PowerShell
# Usage: Right-click > Run with PowerShell
# Or: powershell -ExecutionPolicy Bypass -File AUREON_START.ps1

$ErrorActionPreference = "Continue"
Set-Location "C:\AUREON_AUTONOMOUS"

Write-Host "==============================" -ForegroundColor Cyan
Write-Host "  AUREON STARTUP" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""

# Set UTF-8 output to prevent encoding crashes
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python not found!" -ForegroundColor Red
    pause
    exit 1
}

# Start AUREON
Write-Host ""
Write-Host "Starting AUREON autonomous..." -ForegroundColor Green
python aureon_autonomous.py

# If it exits, pause so you can see errors
Write-Host ""
Write-Host "AUREON exited. Press any key to close." -ForegroundColor Yellow
pause
