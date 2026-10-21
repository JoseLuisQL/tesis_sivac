# ============================================================================
# SIVAC-THESIS-LAB · Lanzador Oficial para Windows PowerShell
# ============================================================================
$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  SIVAC-THESIS-LAB · Multi-Agent Studio (Agno + Opcode + React Flow + XTerm)" -ForegroundColor White
Write-Host "============================================================================" -ForegroundColor Cyan

# 1. Recargar PATH de Usuario y Sistema en Windows sin necesidad de reiniciar la consola
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$machinePath = [Environment]::GetEnvironmentVariable("Path", "Machine")
$extraPaths = @(
    "$env:USERPROFILE\.bun\bin",
    "$env:APPDATA\npm",
    "$env:USERPROFILE\.local\bin",
    "$env:USERPROFILE\.factory\bin",
    "$env:USERPROFILE\.claude\local",
    "$env:USERPROFILE\.claude\bin",
    "$PSScriptRoot\.bin"
) -join ";"
$env:PATH = "$extraPaths;$userPath;$machinePath"

# 2. Instalar node_modules si aún no existen
if (-not (Test-Path "$PSScriptRoot\node_modules")) {
    Write-Host "[1/2] Instalando paquetes del estudio multi-agente..." -ForegroundColor Yellow
    npm install
}

Write-Host "[2/2] Levantando SIVAC Agent Studio en http://localhost:3000 ..." -ForegroundColor Green
Start-Process "http://localhost:3000"
npx tsx server.ts
