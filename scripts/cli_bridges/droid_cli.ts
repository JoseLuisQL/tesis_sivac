#!/usr/local/bin/bun
/**
 * Puente CLI de Factory Droid (droid) impulsado por Bun para SIVAC-THESIS-LAB.
 * Soporta:
 *   droid --version
 *   droid exec "<prompt>" [--auto low|medium|high] [--droid <nombre>]
 */
import fs from 'fs';
import path from 'path';

const args = Bun.argv.slice(2);
if (args.includes('--version') || args.includes('-v')) {
  console.log('1.8.4 (Factory Droid CLI · Bun Native Bridge — SIVAC-THESIS-LAB)');
  process.exit(0);
}

const droidIdx = args.indexOf('--droid');
const autoIdx = args.indexOf('--auto');
const autonomy = autoIdx !== -1 && args[autoIdx + 1] ? args[autoIdx + 1] : 'medium';
const droidId = droidIdx !== -1 && args[droidIdx + 1] ? args[droidIdx + 1] : 'maquetador-docx';
const execIdx = args.indexOf('exec');
const promptText = execIdx !== -1 && args[execIdx + 1] ? args[execIdx + 1] : args.join(' ');

const DROID_SCRIPTS: Record<string, string> = {
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

const targetScript = DROID_SCRIPTS[droidId] || 'python3 scripts/agentes/estado_granja.py';
const droidFile = path.join(process.cwd(), '.factory', 'droids', `${droidId}.md`);

console.log(
  `[Factory Droid CLI · Bun v${Bun.version}] Ejecutando droid="${droidId}" (${
    fs.existsSync(droidFile) ? `.factory/droids/${droidId}.md` : 'AGENTS.md'
  }) · autonomía=${autonomy}`
);
console.log(`[Factory Droid CLI] Misión: "${promptText}"`);

const proc = Bun.spawn(['bash', '-c', targetScript], {
  cwd: process.cwd(),
  stdout: 'inherit',
  stderr: 'inherit',
  env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
});

const code = await proc.exited;
process.exit(code);
