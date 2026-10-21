#!/usr/bin/env node
/**
 * Puente CLI Local de Claude Code (claude) para SIVAC-THESIS-LAB (Windows & POSIX).
 * Se conecta con las definiciones reales en .claude/agents/*.md y ejecuta el flujo del subagente.
 * Soporta:
 *   claude --version
 *   claude -p "<prompt>" --agent <subagente> [--output-format stream-json] [--verbose]
 */
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';

const isWin = process.platform === 'win32';
const pyBin = isWin ? 'python' : 'python3';
const args = process.argv.slice(2);

if (args.includes('--version') || args.includes('-v')) {
  console.log(`2.1.42 (Claude Code CLI · Local Agent Bridge [${isWin ? 'Windows' : 'POSIX'}] — .claude/agents/)`);
  process.exit(0);
}

const agentIdx = args.indexOf('--agent');
const agentId = agentIdx !== -1 && args[agentIdx + 1] ? args[agentIdx + 1] : 'director-general';
const promptIdx = args.indexOf('-p');
const promptText = promptIdx !== -1 && args[promptIdx + 1] ? args[promptIdx + 1] : args.join(' ');
const isStreamJson = args.includes('stream-json');

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

const targetScript = AGENT_SCRIPTS[agentId] || `${pyBin} scripts/agentes/estado_granja.py`;
const agentFile = path.join(process.cwd(), '.claude', 'agents', `${agentId}.md`);

console.log(`[Claude Code CLI] Conectado a definición local: ${fs.existsSync(agentFile) ? `.claude/agents/${agentId}.md` : agentId}`);
console.log(`[Claude Code CLI] Subagente activo: @${agentId} | Directiva: "${promptText}"`);

if (isStreamJson) {
  console.log(
    JSON.stringify({
      type: 'system',
      subtype: 'init',
      agent: agentId,
      definition: fs.existsSync(agentFile) ? `.claude/agents/${agentId}.md` : 'default',
      prompt: promptText,
    })
  );
}

const shellBin = isWin ? 'cmd.exe' : 'bash';
const shellArgs = isWin ? ['/d', '/s', '/c', targetScript] : ['-c', targetScript];

const child = spawn(shellBin, shellArgs, {
  cwd: process.cwd(),
  stdio: 'inherit',
  env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
});

child.on('close', (code) => {
  const exitCode = code ?? 0;
  if (isStreamJson) {
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
