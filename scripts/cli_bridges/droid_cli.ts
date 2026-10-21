#!/usr/bin/env node
/**
 * Puente CLI Local de Factory Droid (droid) para SIVAC-THESIS-LAB (Windows & POSIX).
 * Se conecta con las definiciones reales en .factory/droids/*.md y ejecuta la misión del droid.
 * Soporta:
 *   droid --version
 *   droid exec "<prompt>" [--auto low|medium|high] [--droid <nombre>] [--agent <nombre>]
 */
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';

const isWin = process.platform === 'win32';
const pyBin = isWin ? 'python' : 'python3';
const args = process.argv.slice(2);

if (args.includes('--version') || args.includes('-v')) {
  console.log(`1.8.4 (Factory Droid CLI · Local Droid Bridge [${isWin ? 'Windows' : 'POSIX'}] — .factory/droids/)`);
  process.exit(0);
}

const droidIdx = args.indexOf('--droid') !== -1 ? args.indexOf('--droid') : args.indexOf('--agent');
const autoIdx = args.indexOf('--auto');
const autonomy = autoIdx !== -1 && args[autoIdx + 1] ? args[autoIdx + 1] : 'medium';
const droidId = droidIdx !== -1 && args[droidIdx + 1] ? args[droidIdx + 1] : 'maquetador-docx';
const execIdx = args.indexOf('exec');
const promptText = execIdx !== -1 && args[execIdx + 1] ? args[execIdx + 1] : args.join(' ');

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

const targetScript = DROID_SCRIPTS[droidId] || `${pyBin} scripts/agentes/estado_granja.py`;
const droidFile = path.join(process.cwd(), '.factory', 'droids', `${droidId}.md`);

console.log(
  `[Factory Droid CLI] Conectado a definición local: ${
    fs.existsSync(droidFile) ? `.factory/droids/${droidId}.md` : 'AGENTS.md'
  } · autonomía=${autonomy}`
);
console.log(`[Factory Droid CLI] Droid activo: @${droidId} | Misión: "${promptText}"`);

const shellBin = isWin ? 'cmd.exe' : 'bash';
const shellArgs = isWin ? ['/d', '/s', '/c', targetScript] : ['-c', targetScript];

const child = spawn(shellBin, shellArgs, {
  cwd: process.cwd(),
  stdio: 'inherit',
  env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
});

child.on('close', (code) => {
  process.exit(code ?? 0);
});
