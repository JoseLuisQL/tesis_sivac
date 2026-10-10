#!/usr/bin/env node
/**
 * Hook PreToolUse de Seguridad SIVAC-THESIS-LAB
 * Bloquea estrictamente cualquier intento de escritura o modificación sobre:
 * 1. C:\Proyectos\syncova (Código fuente - SOLO LECTURA)
 * 2. C:\MisInvestigaciones\tesis\sivac\referencias / ejemplos_tesis (Modelos originales)
 * 3. C:\MisInvestigaciones\tesis\sivac\ejemplo_validacion (Formatos originales)
 * 4. C:\MisInvestigaciones\tesis\sivac\PROYECTO_TESIS.docx (Documento original inmutable)
 */

const fs = require('fs');

function readStdin() {
  try {
    return fs.readFileSync(0, 'utf-8');
  } catch (err) {
    return '';
  }
}

const rawInput = readStdin();
if (!rawInput.trim()) {
  process.exit(0);
}

let eventData = {};
try {
  eventData = JSON.parse(rawInput);
} catch (e) {
  // Si no es JSON válido, permitir
  process.exit(0);
}

const tool = eventData.tool_name || eventData.tool || '';
const toolInput = eventData.tool_input || eventData.input || {};

const FORBIDDEN_PATHS = [
  'syncova',
  'ejemplos_tesis',
  'ejemplo_validacion',
  'proyecto_tesis.docx',
  'referencias/modelos_tesis',
  'referencias/modelos_validacion',
  'referencias/proyecto_base'
];

function isForbiddenTarget(filePath) {
  if (!filePath || typeof filePath !== 'string') return false;
  const normalized = filePath.toLowerCase().replace(/\\/g, '/');
  return FORBIDDEN_PATHS.some(target => normalized.includes(target));
}

// 1. Verificar herramientas de escritura directa
if (tool === 'Write' || tool === 'Edit' || tool === 'Create') {
  const targetPath = toolInput.file_path || toolInput.path || '';
  if (isForbiddenTarget(targetPath)) {
    console.error(`[SEGURIDAD BLOQUEADA] Error: Intento de escritura/edición denegado en ruta protegida de solo lectura: "${targetPath}". (Regla 3.2 SIVAC-THESIS-LAB).`);
    process.exit(2);
  }
}

// 2. Verificar herramientas de ejecución de terminal
if (tool === 'PowerShell' || tool === 'Bash' || tool === 'Execute') {
  const cmd = (toolInput.command || '').toLowerCase();
  const writePatterns = [
    'rm ', 'del ', 'remove-item', 'set-content', 'out-file', 'add-content',
    'echo ', 'git checkout', 'git reset', 'git clean', '>', '>>', 'move-item', 'ren '
  ];

  const hasWriteAction = writePatterns.some(p => cmd.includes(p));
  const hasForbiddenTarget = FORBIDDEN_PATHS.some(t => cmd.includes(t));

  if (hasWriteAction && hasForbiddenTarget) {
    console.error(`[SEGURIDAD BLOQUEADA] Error: Comando bloqueado por intentar modificar rutas de solo lectura protegidas (syncova, modelos o proyecto original).`);
    process.exit(2);
  }
}

process.exit(0);
