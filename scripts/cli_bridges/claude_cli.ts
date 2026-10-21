#!/usr/local/bin/bun
/**
 * Puente CLI de Claude Code (claude) impulsado por Bun para SIVAC-THESIS-LAB.
 * Soporta:
 *   claude --version
 *   claude -p "<prompt>" --agent <subagente> [--output-format stream-json] [--verbose]
 */
import fs from 'fs';
import path from 'path';

const args = Bun.argv.slice(2);
if (args.includes('--version') || args.includes('-v')) {
  console.log('2.1.42 (Claude Code CLI · Bun Native Bridge — SIVAC-THESIS-LAB)');
  process.exit(0);
}

const agentIdx = args.indexOf('--agent');
const agentId = agentIdx !== -1 && args[agentIdx + 1] ? args[agentIdx + 1] : 'director-general';
const promptIdx = args.indexOf('-p');
const promptText = promptIdx !== -1 && args[promptIdx + 1] ? args[promptIdx + 1] : args.join(' ');
const isStreamJson = args.includes('stream-json');

const AGENT_SCRIPTS: Record<string, string> = {
  'director-general': 'python3 scripts/agentes/estado_granja.py',
  'investigador-bibliografico': 'python3 scripts/fuentes/buscador_citas.py',
  'verificador-integridad': 'python3 scripts/agentes/verificador_integridad.py',
  'guardian-consistencia': 'python3 scripts/agentes/guardian_consistencia.py',
  'especialista-instrumentos': 'python3 scripts/compiladores/generar_anexo2_validacion_fany.py',
  'especialista-forms': 'python3 scripts/agentes/validez_contenido.py',
  'ingeniero-sivac': 'python3 scripts/agentes/inventario_syncova.py',
  'documentador-xp': 'python3 scripts/agentes/inventario_syncova.py',
  'analista-estadistico': 'python3 scripts/estadistica/pipeline_inferencial.py --json',
  'analista-documental': 'python3 scripts/agentes/analista_documental.py',
  'redactor-academico': 'python3 scripts/agentes/revisor_prosa.py',
  'maquetador-docx': 'python3 scripts/utilidades/auditor_docx_apa7.py auditar salidas/documentos/informe_final_v02.docx',
  'curador-cerebro': 'python3 scripts/agentes/curador_cerebro.py',
  'jurado-revisor': 'python3 scripts/utilidades/auditor_docx_apa7.py auditar salidas/documentos/informe_final_v02.docx --md',
};

const targetScript = AGENT_SCRIPTS[agentId] || 'python3 scripts/agentes/estado_granja.py';
const agentFile = path.join(process.cwd(), '.claude', 'agents', `${agentId}.md`);

if (isStreamJson) {
  console.log(
    JSON.stringify({
      type: 'system',
      subtype: 'init',
      runtime: `bun-${Bun.version}`,
      agent: agentId,
      definition: fs.existsSync(agentFile) ? `.claude/agents/${agentId}.md` : 'default',
      prompt: promptText,
    })
  );
} else {
  console.log(`[Claude Code CLI · Bun v${Bun.version}] Invocando subagente @${agentId} (.claude/agents/${agentId}.md)`);
  console.log(`[Claude Code CLI] Orden recibida: "${promptText}"`);
}

const proc = Bun.spawn(['bash', '-c', targetScript], {
  cwd: process.cwd(),
  stdout: 'inherit',
  stderr: 'inherit',
  env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
});

const code = await proc.exited;
if (isStreamJson) {
  console.log(JSON.stringify({ type: 'result', subtype: code === 0 ? 'success' : 'blocked', agent: agentId, exitCode: code }));
}
process.exit(code);
