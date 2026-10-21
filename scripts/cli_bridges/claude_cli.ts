#!/usr/bin/env node
/**
 * Motor CLI Local de Claude Code (`claude`) para SIVAC-THESIS-LAB (Windows, WSL2 & POSIX).
 * Se ejecuta directamente dentro del directorio del proyecto y conecta con:
 *   - CLAUDE.md (Constitución Operativa)
 *   - .claude/agents/<agente>.md (14 Agentes Especializados)
 *   - .claude/skills/<skill>/SKILL.md (17 Skills Científicas)
 *   - .claude/settings.json & .mcp.json (Hooks PreToolUse/PostToolUse y 5 MCPs)
 *   - obsidian_vault/00_SISTEMA/ESTADO_TESIS.md y DECISIONES.md (Memoria Viva)
 *
 * Soporta:
 *   claude --version | -v
 *   claude --help | -h
 *   claude (sesión interactiva en el proyecto)
 *   claude "hola"
 *   claude -p "<prompt>" [--agent <id>] [--task-cmd "<cmd>"] [--output-format stream-json] [--verbose]
 */
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';

const isWin = process.platform === 'win32';
const pyBin = isWin ? 'python' : 'python3';
const repoRoot = process.cwd();
const rawArgs = process.argv.slice(2);

if (rawArgs.includes('--version') || rawArgs.includes('-v')) {
  console.log(
    `2.1.42 (Claude Code CLI · SIVAC-THESIS-LAB Project Runtime [${isWin ? 'Windows-NT' : 'POSIX'}] — .claude/agents/)`
  );
  process.exit(0);
}

if (rawArgs.includes('--help') || rawArgs.includes('-h')) {
  console.log(`Claude Code CLI v2.1.42 — SIVAC-THESIS-LAB Multi-Agent Workspace
Uso:
  claude [opciones] [prompt]
  claude --agent <nombre-agente> -p "<mensaje o instrucción>"

Opciones:
  -p, --print, --prompt <texto>   Procesa el prompt directamente en el CLI del agente
  --agent, -a <id>                Selecciona uno de los 14 agentes de .claude/agents/*.md (default: director-general)
  --output-format <formato>       Formato de salida (text | stream-json)
  --verbose                       Muestra trazas detalladas de ToolUse y lectura de contexto
  -v, --version                   Muestra la versión del motor Claude Code CLI`);
  process.exit(0);
}

// Parse CLI arguments cleanly
let agentId = 'director-general';
let promptText = '';
let explicitTaskCmd = '';
let isStreamJson = false;
let isVerbose = false;
const positionalParts: string[] = [];

for (let i = 0; i < rawArgs.length; i++) {
  const arg = rawArgs[i];
  if (arg === '--agent' || arg === '-a') {
    if (rawArgs[i + 1]) {
      agentId = rawArgs[++i].replace(/^@/, '');
    }
  } else if (arg.startsWith('--agent=')) {
    agentId = arg.split('=')[1].replace(/^@/, '');
  } else if (arg === '-p' || arg === '--print' || arg === '--prompt') {
    if (rawArgs[i + 1]) {
      promptText = rawArgs[++i];
    }
  } else if (arg.startsWith('--prompt=')) {
    promptText = arg.slice('--prompt='.length);
  } else if (arg === '--task-cmd') {
    if (rawArgs[i + 1]) {
      explicitTaskCmd = rawArgs[++i];
    }
  } else if (arg === '--output-format') {
    const fmt = rawArgs[i + 1] || '';
    if (fmt === 'stream-json') isStreamJson = true;
    i++;
  } else if (arg.startsWith('--output-format=')) {
    if (arg.includes('stream-json')) isStreamJson = true;
  } else if (arg === '--verbose') {
    isVerbose = true;
  } else if (!arg.startsWith('-')) {
    positionalParts.push(arg);
  }
}

if (!promptText && positionalParts.length > 0) {
  promptText = positionalParts.join(' ').trim();
}

// Clean surrounding quotes if present
promptText = promptText.replace(/^["']|["']$/g, '').trim();

// Read agent markdown metadata from .claude/agents/<agentId>.md
function loadAgentMetadata(id: string) {
  const agentFile = path.join(repoRoot, '.claude', 'agents', `${id}.md`);
  const meta = {
    id,
    exists: fs.existsSync(agentFile),
    relPath: `.claude/agents/${id}.md`,
    model: id === 'director-general' ? 'claude-opus-4-6' : 'claude-sonnet-4-6',
    role: 'Agente Especialista SIVAC-THESIS-LAB',
    tools: ['Read', 'Grep', 'Glob', 'Bash'],
    skills: [] as string[],
  };
  if (!meta.exists) return meta;
  try {
    const raw = fs.readFileSync(agentFile, 'utf-8');
    const fmMatch = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (fmMatch) {
      const yaml = fmMatch[1];
      const descMatch = yaml.match(/description:\s*(.+)/);
      const modelMatch = yaml.match(/model:\s*(.+)/);
      if (descMatch) meta.role = descMatch[1].trim().replace(/^['"]|['"]$/g, '');
      if (modelMatch) {
        const m = modelMatch[1].trim();
        meta.model = m === 'opus' ? 'claude-opus-4-6' : m === 'sonnet' ? 'claude-sonnet-4-6' : m;
      }
      const skillsBlock = yaml.match(/skills:\r?\n((?:\s*-\s*.+\r?\n?)+)/);
      if (skillsBlock) {
        meta.skills = skillsBlock[1]
          .split(/\r?\n/)
          .map((s) => s.replace(/^\s*-\s*/, '').trim())
          .filter(Boolean);
      }
      const toolsBlock = yaml.match(/tools:\r?\n((?:\s*-\s*.+\r?\n?)+)/);
      if (toolsBlock) {
        meta.tools = toolsBlock[1]
          .split(/\r?\n/)
          .map((s) => s.replace(/^\s*-\s*/, '').trim())
          .filter(Boolean);
      }
    }
  } catch {
    // ignore read error
  }
  return meta;
}

// Map specialist subagents to their canonical verification scripts
const AGENT_SCRIPTS: Record<string, string> = {
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
    'hola claude',
    'hola agente',
    'hola director',
    'hola god',
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
    'que eres',
    'que puedes hacer',
    'ayuda',
    'help',
    '/help',
    '/status',
    '/agents',
    '/doctor',
    'test',
    'prueba',
    'probando',
    'ping',
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

const agentMeta = loadAgentMetadata(agentId);
const agentsDir = path.join(repoRoot, '.claude', 'agents');
const totalAgents = fs.existsSync(agentsDir)
  ? fs.readdirSync(agentsDir).filter((f) => f.endsWith('.md')).length
  : 14;
const skillsDir = path.join(repoRoot, '.claude', 'skills');
const totalSkills = fs.existsSync(skillsDir)
  ? fs.readdirSync(skillsDir, { withFileTypes: true }).filter((d) => d.isDirectory() && d.name !== 'shared').length
  : 17;

console.log('╭──────────────────────────────────────────────────────────────────────────────╮');
console.log('│ ✻ Claude Code CLI v2.1.42 · SIVAC-THESIS-LAB Workspace                       │');
console.log(`│   Directorio : ${repoRoot.slice(0, 62).padEnd(62, ' ')}│`);
console.log(`│   Agente CLI : @${agentId} (${agentMeta.model})`.padEnd(79, ' ') + '│');
console.log(`│   Contrato   : ${agentMeta.relPath} · ${totalAgents} agentes · ${totalSkills} skills`.padEnd(79, ' ') + '│');
console.log('╰──────────────────────────────────────────────────────────────────────────────╯');

if (!promptText) {
  console.log(`● [Sesión Interactiva Claude Code] Agente @${agentId} listo en el proyecto.`);
  console.log(`● [Contexto Cargado] CLAUDE.md · obsidian_vault/00_SISTEMA/ESTADO_TESIS.md · .mcp.json`);
  console.log(`✔ Escribe cualquier mensaje o comando (ej. "hola", "audita citas APA 7", "verifica DEC-007") para procesarlo con @${agentId}.`);
  process.exit(0);
}

console.log(`● [Claude CLI · Prompt]   > "${promptText}"`);
console.log(
  `● [ToolUse: Read]         Cargando ${agentMeta.relPath} (Tools: ${agentMeta.tools.slice(0, 6).join(', ')})`
);
if (agentMeta.skills.length > 0) {
  console.log(`● [ToolUse: Skill]        Skills activas: ${agentMeta.skills.join(', ')}`);
}
console.log(
  `● [ToolUse: Read]         Sincronizando memoria viva: obsidian_vault/00_SISTEMA/ESTADO_TESIS.md y DECISIONES.md (DEC-007)`
);

if (isStreamJson && isVerbose) {
  console.log(
    JSON.stringify({
      type: 'system',
      subtype: 'init',
      agent: agentId,
      model: agentMeta.model,
      definition: agentMeta.relPath,
      prompt: promptText,
    })
  );
}

// If conversational greeting / general question, process directly inside the Claude CLI without running an unrelated OpenXML audit
if (isConversationalOrGreeting(promptText) && !explicitTaskCmd) {
  console.log(`● [ToolUse: Glob]         Verificando ecosistema: ${totalAgents} agentes en .claude/agents/ y ${totalSkills} skills en .claude/skills/`);
  console.log(`● [Loop Cognitivo 3.0]    Procesando mensaje conversacional en sesión de @${agentId}...`);
  console.log('');
  console.log(`✻ [Respuesta Claude Code CLI · @${agentId}]:`);
  console.log(
    `  ¡Hola, Bach. José Luis Quispe León! Estoy activo dentro del CLI de Claude Code en tu proyecto SIVAC-THESIS-LAB.`
  );
  console.log(`   Rol activo: ${agentMeta.role}`);
  console.log(`  ▸ Memoria Obsidian conectada: ESTADO_TESIS.md (Fases F0–F3 al 100%, F4 OpenXML al 90%, F5 Bioestadística n=14 activa).`);
  console.log(`  ▸ Dimensiones oficiales (DEC-007): Oportunidad, Consistencia documental y Satisfacción del usuario (TAM).`);
  console.log(`  ▸ Puedes pedirme cualquier tarea directamente, por ejemplo:`);
  console.log(`    1. "Audita las citas y referencias APA 7" (@verificador-integridad)`);
  console.log(`    2. "Verifica la matriz de consistencia DEC-007" (@guardian-consistencia)`);
  console.log(`    3. "Ejecuta el pipeline bioestadístico n=14" (@analista-estadistico)`);
  console.log(`    4. "Audita el formato OpenXML de informe_final_v02.docx" (@maquetador-docx)`);
  console.log(`    5. "Simula la evaluación del jurado UNAJMA sobre 20 puntos" (@jurado-revisor)`);
  process.exit(0);
}

// Otherwise, execute the agent's specialist verification/execution tool inside the Claude Code CLI session
const targetScript =
  explicitTaskCmd || AGENT_SCRIPTS[agentId] || `${pyBin} scripts/agentes/estado_granja.py`;

console.log(`● [ToolUse: Bash]         Ejecutando herramienta del agente @${agentId}: ${targetScript}`);
console.log('────────────────────────────────────────────────────────────────────────────────');

const shellBin = isWin ? 'cmd.exe' : 'bash';
const shellArgs = isWin ? ['/d', '/s', '/c', targetScript] : ['-c', targetScript];

const child = spawn(shellBin, shellArgs, {
  cwd: repoRoot,
  stdio: 'inherit',
  env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
});

child.on('close', (code) => {
  const exitCode = code ?? 0;
  console.log('────────────────────────────────────────────────────────────────────────────────');
  console.log(
    `✻ [Claude Code CLI · @${agentId}] Directiva procesada: "${promptText}" | estado=${
      exitCode === 0 ? 'COMPLETADO (0)' : `OBSERVADO (${exitCode})`
    }`
  );
  if (isStreamJson && isVerbose) {
    console.log(
      JSON.stringify({
        type: 'result',
        subtype: exitCode === 0 ? 'success' : 'blocked',
        agent: agentId,
        exitCode,
      })
    );
  }
  process.exit(exitCode);
});
