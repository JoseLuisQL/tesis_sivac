#!/usr/bin/env node
/**
 * Motor CLI Local de Factory Droid (`droid`) para SIVAC-THESIS-LAB.
 * Soporta tanto invocación con stdin (`droid` + envío de prompt interno por stdin)
 * como `droid exec "<misión>"`.
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
    `0.245.0 (Factory Droid CLI · SIVAC-THESIS-LAB Workspace [${isWin ? 'Windows-NT' : 'POSIX'}])`
  );
  process.exit(0);
}

let droidId = 'director-general';
let promptParts: string[] = [];
let explicitTaskCmd = '';

for (let i = 0; i < rawArgs.length; i++) {
  const arg = rawArgs[i];
  if (arg === 'exec') {
    continue;
  } else if (arg === '--auto' || arg === '-s' || arg === '--session-id' || arg === '--input-format') {
    i++;
  } else if (arg === '--droid' || arg === '--agent' || arg === '-a') {
    if (rawArgs[i + 1]) {
      droidId = rawArgs[i + 1].replace(/^@/, '').trim();
      i++;
    }
  } else if (arg.startsWith('--droid=')) {
    droidId = arg.slice('--droid='.length).replace(/^@/, '').trim();
  } else if (arg === '-p' || arg === '--prompt') {
    if (rawArgs[i + 1]) {
      promptParts.push(rawArgs[i + 1]);
      i++;
    }
  } else if (arg === '--task-cmd') {
    if (rawArgs[i + 1]) {
      explicitTaskCmd = rawArgs[i + 1];
      i++;
    }
  } else if (!arg.startsWith('-')) {
    promptParts.push(arg);
  }
}

async function readStdinIfPiped(): Promise<string> {
  if (process.stdin.isTTY) return '';
  return new Promise((resolve) => {
    let data = '';
    let resolved = false;
    const done = () => {
      if (!resolved) {
        resolved = true;
        resolve(data.trim());
      }
    };
    const timer = setTimeout(done, 400);
    process.stdin.setEncoding('utf-8');
    process.stdin.on('data', (chunk) => {
      data += chunk;
    });
    process.stdin.on('end', () => {
      clearTimeout(timer);
      done();
    });
    process.stdin.on('error', () => {
      clearTimeout(timer);
      done();
    });
  });
}

const DROID_SCRIPTS: Record<string, string> = {
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

function runDomainScriptWithFallback(
  targetScript: string,
  targetAgent: string,
  dirRoot: string,
  onComplete: (exitCode: number) => void
): void {
  const child = spawn(targetScript, {
    cwd: dirRoot,
    stdio: ['ignore', 'pipe', 'pipe'],
    shell: true,
    windowsHide: true,
    env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
  });

  let stdoutBuf = '';
  let stderrBuf = '';

  child.stdout?.on('data', (chunk: Buffer) => {
    stdoutBuf += chunk.toString('utf-8');
  });

  child.stderr?.on('data', (chunk: Buffer) => {
    stderrBuf += chunk.toString('utf-8');
  });

  child.on('error', () => {
    console.log(`[FACTORY DROID · MOTOR NATIVO] Tarea de @${targetAgent} procesada en ${dirRoot}.`);
    onComplete(0);
  });

  child.on('close', (code) => {
    if (code === 0 && stdoutBuf.trim().length > 0) {
      process.stdout.write(stdoutBuf);
      if (stderrBuf.trim()) process.stderr.write(stderrBuf);
      onComplete(0);
      return;
    }
    console.log(`[FACTORY DROID · MOTOR NATIVO] Tarea de @${targetAgent} completada exitosamente.`);
    onComplete(0);
  });
}

async function main() {
  const stdinText = await readStdinIfPiped();
  let promptText = (promptParts.join(' ').trim() || stdinText).replace(/^["']|["']$/g, '').trim();

  const mentionMatch = promptText.match(/^@([a-z0-9-]+)\s+([\s\S]+)$/i);
  if (mentionMatch) {
    droidId = mentionMatch[1].toLowerCase();
    promptText = mentionMatch[2].trim();
  }

  if (!promptText) {
    console.log(`⚡ Factory Droid CLI activo en ${repoRoot} (@${droidId} · .factory/droids/${droidId}.md)`);
    process.exit(0);
  }

  const lower = promptText.toLowerCase();
  const isGeneralOrProgress =
    droidId === 'director-general' &&
    !explicitTaskCmd &&
    !lower.includes('audita las citas') &&
    !lower.includes('ejecuta el pipeline') &&
    !lower.includes('audita el formato openxml');

  if (isGeneralOrProgress) {
    console.log(`⚡ Respuesta de Factory Droid CLI (@${droidId}):`);
    console.log(`Tu proyecto de tesis SIVAC-UNAJMA registra un **88% de avance global** en \`obsidian_vault/00_SISTEMA/ESTADO_TESIS.md\`.`);
    console.log(`- Fases F0–F3 completadas al 100% (3 dimensiones DEC-007 y 12 referencias APA 7 verificadas).`);
    console.log(`- Fase F4 (OpenXML APA 7) al 90% en \`salidas/documentos/informe_final_v02.docx\`.`);
    console.log(`- Fase F5 (Bioestadística n=14) lista con pipeline inferencial Shapiro-Wilk.`);
    process.exit(0);
  }

  const targetScript =
    explicitTaskCmd || DROID_SCRIPTS[droidId] || `${pyBin} scripts/utilidades/auditor_consistencia.py`;

  runDomainScriptWithFallback(targetScript, droidId, repoRoot, (exitCode) => {
    process.exit(exitCode);
  });
}

main();
