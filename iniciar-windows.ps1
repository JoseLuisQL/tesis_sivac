# ============================================================================
# SIVAC-THESIS-LAB · Lanzador Oficial para Windows PowerShell
# ============================================================================
$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  SIVAC-THESIS-LAB · Multi-Agent Studio (Auto-Discovery CLI Engine)" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

# 1. Liberar puerto 3000 si existe un proceso anterior ocupándolo
try {
    $staleProcs = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($pidToKill in $staleProcs) {
        if ($pidToKill -and $pidToKill -gt 0) {
            Write-Host "[AUTO-LIMPIEZA] Liberando puerto 3000 ocupado por PID $pidToKill..." -ForegroundColor Yellow
            Stop-Process -Id $pidToKill -Force -ErrorAction SilentlyContinue
        }
    }
} catch {}

# 2. Recargar PATH en vivo desde el Registro de Windows + rutas oficiales de Anthropic, Factory AI y Bun
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$machinePath = [Environment]::GetEnvironmentVariable("Path", "Machine")
$extraPaths = @(
    "$env:USERPROFILE\bin",
    "$env:USERPROFILE\.local\bin",
    "$env:USERPROFILE\.bun\bin",
    "$env:LOCALAPPDATA\Microsoft\WinGet\Links",
    "$env:APPDATA\npm",
    "$env:USERPROFILE\.factory\bin",
    "$env:USERPROFILE\.claude\local",
    "$PSScriptRoot\.bin"
) -join ";"

$env:PATH = "$extraPaths;$userPath;$machinePath"

if (-not (Test-Path "node_modules")) {
    Write-Host "[1/2] Instalando dependencias con npm install..." -ForegroundColor Yellow
    npm install
}

Write-Host "[2/2] Verificando motores IA locales..." -ForegroundColor Green
foreach ($cmd in @("bun", "claude", "droid", "python")) {
    $found = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($found) {
        Write-Host "  [OK] $cmd -> $($found.Source)" -ForegroundColor Green
    } else {
        Write-Host "  [PUENTE WORKSPACE] $cmd -> Enlazado automaticamente a .claude/agents y .factory/droids" -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Host "Abriendo SIVAC Agent Studio en http://localhost:3000 ..." -ForegroundColor Green
npx tsx server.ts
