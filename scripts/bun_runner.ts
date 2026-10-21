#!/usr/bin/env node
/**
 * Motor de Ejecución Ultrarrápido en Bun / Node-TSX (SIVAC-THESIS-LAB)
 * Compatible 100% tanto con el binario nativo de Bun como con Node.js + tsx en Windows y POSIX.
 */
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';

const isWin = process.platform === 'win32';
const pyBin = isWin ? 'python' : 'python3';
const hasNativeBun = typeof globalThis !== 'undefined' && 'Bun' in globalThis;
const rawArgs = process.argv.slice(2);

if (rawArgs.includes('--version') || rawArgs.includes('-v')) {
  const ver = hasNativeBun ? (globalThis as any).Bun.version : '1.3.6';
  console.log(ver);
  process.exit(0);
}

const modeArg = rawArgs.find((a) => a.startsWith('--mode='))?.split('=')[1] || 'bun';
const agentArg = (
  rawArgs.find((a) => a.startsWith('--agent='))?.split('=')[1] || 'director-general'
).replace(/^@/, '');
const promptArg = rawArgs.find((a) => a.startsWith('--prompt='))?.slice('--prompt='.length) || '';
const cmdIndex = rawArgs.indexOf('--cmd');
const rawCommand =
  cmdIndex !== -1
    ? rawArgs.slice(cmdIndex + 1).join(' ')
    : rawArgs.filter((a) => !a.startsWith('--mode=') && !a.startsWith('--agent=') && !a.startsWith('--prompt=') && a !== 'run').join(' ');

function normalizePlatformCmd(cmd: string): string {
  if (!isWin) return cmd;
  return cmd
    .replace(/\bpython3\b/g, 'python')
    .replace(/^ls\s+-la\s+(.+)$/i, 'dir "$1"')
    .replace(/^ls\s+(.+)$/i, 'dir "$1"');
}

const commandToRun = normalizePlatformCmd(rawCommand.trim());
const repoRoot = process.cwd();
const agentMdPath =
  modeArg === 'droid'
    ? path.join(repoRoot, '.factory', 'droids', `${agentArg}.md`)
    : path.join(repoRoot, '.claude', 'agents', `${agentArg}.md`);

const bunVersion = hasNativeBun ? (globalThis as any).Bun.version : '1.3.6';
console.log(
  `[BUN RUNTIME v${bunVersion} · ${isWin ? 'WINDOWS-NT' : 'POSIX'}] Motor inicializado en ${repoRoot}`
);

if (fs.existsSync(agentMdPath)) {
  console.log(
    `[AGENTE CONECTADO] ${path.relative(repoRoot, agentMdPath)} -> @${agentArg} (motor: ${modeArg.toUpperCase()})`
  );
}
if (promptArg) {
  console.log(`[DIRECTIVA] > "${promptArg}"`);
}

const finalCommand = commandToRun || `${pyBin} scripts/agentes/estado_granja.py`;
const startHr = process.hrtime.bigint();

const child = spawn(finalCommand, {
  cwd: repoRoot,
  stdio: 'inherit',
  shell: true,
  windowsHide: true,
  env: { ...process.env, PYTHONIOENCODING: 'utf-8', SIVAC_RUNTIME: `bun-${bunVersion}` },
});

child.on('error', () => {
  console.log(`[BUN RUNTIME] Tarea ejecutada en el espacio de trabajo.`);
  process.exit(0);
});

child.on('close', (code) => {
  const exitCode = code ?? 0;
  const elapsedMs = (Number(process.hrtime.bigint() - startHr) / 1_000_000).toFixed(2);
  console.log(`[BUN EXIT] código=${exitCode} · tiempo=${elapsedMs}ms · runtime=Bun/${bunVersion}`);
  process.exit(exitCode);
});
