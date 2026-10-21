@echo off
chcp 65001 >nul
title SIVAC-THESIS-LAB — Agent Studio (Windows Local)
echo ============================================================================
echo   SIVAC-THESIS-LAB · Multi-Agent Studio (Auto-Discovery CLI Engine)
echo ============================================================================
echo.

REM 1. Liberar puerto 3000 si quedo un proceso anterior colgado en Windows
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3000" ^| findstr "LISTENING"') do (
    echo [AUTO-LIMPIEZA] Cerrando instancia previa en puerto 3000 ^(PID %%a^)...
    taskkill /F /PID %%a >nul 2>&1
)

REM 2. Inyectar rutas oficiales de Factory Droid (~\bin), Claude Code (~\.local\bin), Bun y WinGet
set "PATH=%USERPROFILE%\bin;%USERPROFILE%\.local\bin;%USERPROFILE%\.bun\bin;%LOCALAPPDATA%\Microsoft\WinGet\Links;%APPDATA%\npm;%USERPROFILE%\.factory\bin;%USERPROFILE%\.claude\local;%CD%\.bin;%PATH%"

if not exist "node_modules" (
    echo [1/2] Instalando dependencias del estudio...
    call npm install
)

echo [2/2] Auto-detectando motores IA ^(Bun, Claude Code CLI, Factory Droid CLI^) e iniciando en http://localhost:3000 ...
echo.
call npx tsx server.ts
pause
