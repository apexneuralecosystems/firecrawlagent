# Restart all app processes (backend + frontend).
# Run this whenever you change backend code or requirements.
#
# Usage:
#   .\scripts\restart-all.ps1
#   .\scripts\restart-all.ps1 -InstallBackendDeps   # also: pip install -r backend/requirements.txt

param(
    [switch]$InstallBackendDeps
)

$ErrorActionPreference = "Stop"
$root = (Get-Item (Join-Path $PSScriptRoot "..")).FullName

function Get-PidsOnPort($port) {
    $out = netstat -ano 2>$null
    $pids = @()
    foreach ($line in ($out | Select-String "LISTENING" | Select-String ":$port ")) {
        $parts = $line.Line -split '\s+', -1
        $pid = $parts[-1]
        if ($pid -match '^\d+$') { $pids += [int]$pid }
    }
    $pids | Select-Object -Unique
}

function Stop-Port($port, $name) {
    $pids = Get-PidsOnPort $port
    foreach ($p in $pids) {
        Write-Host "Stopping $name (port $port, PID $p)..."
        taskkill /PID $p /F 2>$null
    }
    if (-not $pids.Count) { Write-Host "No process on port $port." }
}

Write-Host "Stopping existing backend and frontend..."
Stop-Port 8000 "backend"
Stop-Port 3000 "frontend"
Start-Sleep -Seconds 2

if ($InstallBackendDeps) {
    Write-Host "Installing backend requirements..."
    Push-Location (Join-Path $root "backend")
    pip install -r requirements.txt
    Pop-Location
}

Write-Host "Starting backend in new window (http://localhost:8000)..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\backend'; python -m uvicorn main:app --host 0.0.0.0 --port 8000"
Start-Sleep -Seconds 2

Write-Host "Starting frontend in new window (http://localhost:3000)..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\frontend'; npm run dev"

Write-Host ""
Write-Host "Done. Backend and frontend are running in separate windows."
Write-Host "  Backend:  http://localhost:8000"
Write-Host "  Frontend: http://localhost:3000"
