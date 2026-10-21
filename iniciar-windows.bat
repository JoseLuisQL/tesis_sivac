@echo off
chcp 65001 >nul
title SIVAC-THESIS-LAB — Agent Studio (Windows Local)
echo ============================================================================
echo   SIVAC-THESIS-LAB · Multi-Agent Studio (Agno + Opcode + React Flow + XTerm)
echo ============================================================================
echo.

REM 1. Agregar rutas comunes de Bun, Claude Code, Factory Droid y npm en Windows al PATH
set "PATH=%USERPROFILE%\.bun\bin;%APPDATA%\npm;%USERPROFILE%\.local\bin;%USERPROFILE%\.factory\bin;%USERPROFILE%\.claude\local;%USERPROFILE%\.claude\bin;%CD%\.bin;%PATH%"

if not exist "node_modules" (
  echo [1/2] Instalando dependencias del entorno...
  call npm install
)

echo [2/2] Iniciando servidor full-stack y conectando con los 14 agentes locales en http://localhost:3000 ...
start "" http://localhost:3000
call npx tsx server.ts
pause
