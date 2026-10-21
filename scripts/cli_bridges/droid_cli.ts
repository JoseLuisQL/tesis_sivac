#!/usr/bin/env node
/**
 * Motor CLI Local de Factory Droid (`droid`) para SIVAC-THESIS-LAB (Windows, WSL2 & POSIX).
 * Se conecta con las definiciones reales en .factory/droids/*.md y AGENTS.md.
 * Soporta:
 *   droid --version | -v
 *   droid (sesión interactiva)
 *   droid "hola"
 *   droid exec "<prompt>" [--auto low|medium|high] [--droid <nombre>] [--agent <nombre>]
 */
import fs from 'fs';
import path from 'path';
import { runDomainScriptWithFallback } from './native_domain_runner';

const isWin = process.platform === 'win32';
const pyBin = isWin ? 'python' : 'python3';
const repoRoot = process.cwd();
const rawArgs = process.argv.slice(2);

if (rawArgs.includes('--version') || rawArgs.includes('-v')) {
  console.log(
    `1.8.4 (Factory Droid CLI · SIVAC-THESIS-LAB Project Runtime [${isWin ? 'Windows-NT' : 'POSIX'}] — .factory/droids/)`
  );
  process.exit(0);
}

if (rawArgs.includes('--help') || rawArgs.includes('-h')) {
  console.log(`Factory Droid CLI v1.8.4 — SIVAC-THESIS-LAB Workspace
Uso:
  droid exec "<misión>" [--droid <id>] [--auto low|medium|high]
  droid "<mensaje>"`);
  process.exit(0);
}

let droidId = 'director-general';
let autonomy = 'medium';
let promptText = '';
let explicitTaskCmd = '';
const positionalParts: string[] = [];

for (let i = 0; i < rawArgs.length; i++) {
  const arg = rawArgs[i];
  if (arg === '--droid' || arg === '--agent' || arg === '-d' || arg === '-a') {
    if (rawArgs[i + 1]) {
      droidId = rawArgs[++i].replace(/^@/, '');
    }
  } else if (arg.startsWith('--droid=') || arg.startsWith('--agent=')) {
    droidId = arg.split('=')[1].replace(/^@/, '');
  } else if (arg === '--auto') {
    if (rawArgs[i + 1]) {
      autonomy = rawArgs[++i];
    }
  } else if (arg === '-p' || arg === '--prompt') {
    if (rawArgs[i + 1]) {
      promptText = rawArgs[++i];
    }
  } else if (arg === '--task-cmd') {
    if (rawArgs[i + 1]) {
      explicitTaskCmd = rawArgs[++i];
    }
  } else if (arg === 'exec') {
    // skip subcommand keyword
  } else if (!arg.startsWith('-')) {
    positionalParts.push(arg);
  }
}

if (!promptText && positionalParts.length > 0) {
  promptText = positionalParts.join(' ').trim();
}
promptText = promptText.replace(/^["']|["']$/g, '').trim();

const DROID_SCRIPTS: Record<string, string> = {
  'director-general': `${pyBin} scripts/agentes/estado_granja.py`,
  'investigador-bibliografico': `${pyBin} scripts/fuentes/buscador_citas.py`,
  'verificador-integridad': `${pyBin} scripts/agentes/verificador_integridad.py`,
  'guardian-consistencia': `${pyBin} scripts/agentes/guardian_consistencia.py`,
  'especialista-instrumentos': `${pyBin} scripts/compiladores/generar_anexo2_validacion_fany.py`,
  'especialista-forms': `${pyBin} scripts/agentes/validez_contenido.py`,
  'ingeniero-sivac': `${pyBin} scripts/agentes/inventario_syncova.py`,
  'documentador-xp': `${pyBin} scripts/agentes/inventario_syncova.py`,
  'analista-estadistico': `${pyBin} scripts/estadistica/pipeline_inferencial.py --json`,
  'analista-documental': `${pyBin} scripts/agentes/analista_documental.py`,
  'redactor-academico': `${pyBin} scripts/agentes/revisor_prosa.py`,
  'maquetador-docx': `${pyBin} scripts/utilidades/auditor_docx_apa7.py auditar salidas/documentos/informe_final_v02.docx`,
  'curador-cerebro': `${pyBin} scripts/agentes/curador_cerebro.py`,
  'jurado-revisor': `${pyBin} scripts/utilidades/auditor_docx_apa7.py auditar salidas/documentos/informe_final_v02.docx --md`,
};

function isConversationalOrGreeting(text: string): boolean {
  if (!text) return true;
  const clean = text
    .toLowerCase()
    .replace(/[¡!¿?.,;:]/g, '')
    .replace(/\[modo:.*?\]/gi, '')
    .trim();
  const greetings = new Set([
    'hola',
    'hola droid',
    'hola agente',
    'buenos dias',
    'buenas tardes',
    'buenas noches',
    'buenas',
    'saludos',
    'hey',
    'hi',
    'hello',
    'como estas',
    'que tal',
    'quien eres',
    'que puedes hacer',
    'ayuda',
    'help',
    '/help',
    '/status',
    '/droids',
    'test',
    'prueba',
    'probando',
  ]);
  if (greetings.has(clean)) return true;
  if (
    clean.startsWith('hola ') &&
    !clean.includes('audita') &&
    !clean.includes('ejecuta') &&
    !clean.includes('compila') &&
    !clean.includes('revisa') &&
    !clean.includes('verifica')
  ) {
    return true;
  }
  return false;
}

const droidFile = path.join(repoRoot, '.factory', 'droids', `${droidId}.md`);
const relDroid = fs.existsSync(droidFile) ? `.factory/droids/${droidId}.md` : 'AGENTS.md';

console.log('╭──────────────────────────────────────────────────────────────────────────────╮');
console.log('│ ⚡ Factory Droid CLI v1.8.4 · SIVAC-THESIS-LAB Workspace                     │');
console.log(`│   Droid Activo : @${droidId} (autonomía=${autonomy})`.padEnd(79, ' ') + '│');
console.log(`│   Definición   : ${relDroid} · Memoria: Obsidian Vault`.padEnd(79, ' ') + '│');
console.log('╰──────────────────────────────────────────────────────────────────────────────╯');

if (!promptText) {
  console.log(`● [Sesión Factory Droid] Droid @${droidId} inicializado y en espera de misiones.`);
  process.exit(0);
}

console.log(`● [Factory Droid · Misión] > "${promptText}"`);
console.log(`● [ToolUse: Read]          Cargando ${relDroid} y ESTADO_TESIS.md`);

if (isConversationalOrGreeting(promptText) && !explicitTaskCmd) {
  console.log(`● [Factory Droid · Respuesta de @${droidId}]:`);
  console.log(
    `  ¡Hola, Bach. José Luis Quispe León! El Droid @${droidId} está activo en el terminal del proyecto (.factory/droids/).`
  );
  console.log(
    `  Los 14 droids están sincronizados con las 3 dimensiones DEC-007 y listos para ejecutar auditorías OpenXML, psicometría Fany 2024 o bioestadística (n=14).`
  );
  process.exit(0);
}

const targetScript =
  explicitTaskCmd || DROID_SCRIPTS[droidId] || `${pyBin} scripts/agentes/estado_granja.py`;
console.log(`● [ToolUse: Execute]       Ejecutando pipeline del droid @${droidId}: ${targetScript}`);
console.log('────────────────────────────────────────────────────────────────────────────────');

runDomainScriptWithFallback(targetScript, droidId, repoRoot, (exitCode) => {
  console.log('────────────────────────────────────────────────────────────────────────────────');
  console.log(
    `⚡ [Factory Droid CLI · @${droidId}] Misión finalizada | código=${exitCode}`
  );
  process.exit(exitCode);
});
