#!/usr/bin/env bun
/**
 * Motor de Ejecución Ultrarrápido en Bun (SIVAC-THESIS-LAB)
 * Compatible 100% con Windows (cmd.exe / PowerShell / python) y Linux/macOS (bash / python3).
 * Ejecuta subagentes de Claude Code (.claude/agents/*.md), Factory Droid (.factory/droids/*.md)
 * y comandos del ecosistema utilizando el runtime nativo de Bun (Bun.spawn).
 */
import fs from 'fs';
import path from 'path';

const isWin = process.platform === 'win32';
const args = Bun.argv.slice(2);
const modeArg = args.find((a) => a.startsWith('--mode='))?.split('=')[1] || 'bun';
const agentArg = args.find((a) => a.startsWith('--agent='))?.split('=')[1] || 'director-general';
const cmdIndex = args.indexOf('--cmd');
const rawCommand = cmdIndex !== -1 ? args.slice(cmdIndex + 1).join(' ') : args.join(' ');

function normalizePlatformCmd(cmd: string): string {
  if (!isWin) return cmd;
  return cmd
    .replace(/\bpython3\b/g, 'python')
    .replace(/^ls\s+-la\s+(.+)$/i, 'dir "$1"')
    .replace(/^ls\s+(.+)$/i, 'dir "$1"');
}

const commandToRun = normalizePlatformCmd(rawCommand);
const repoRoot = process.cwd();
const agentMdPath =
  modeArg === 'droid'
    ? path.join(repoRoot, '.factory', 'droids', `${agentArg}.md`)
    : path.join(repoRoot, '.claude', 'agents', `${agentArg}.md`);

const bunVersion = Bun.version;
console.log(`[BUN RUNTIME v${bunVersion} · ${isWin ? 'WINDOWS-NT' : 'POSIX'}] Motor Bun inicializado en ${repoRoot}`);

if (fs.existsSync(agentMdPath)) {
  console.log(`[AGENTE CONECTADO] ${path.relative(repoRoot, agentMdPath)} -> @${agentArg} (motor: ${modeArg.toUpperCase()})`);
}

if (!commandToRun.trim()) {
  console.log(`[BUN RUNTIME] Listo. Ningún subcomando especificado.`);
  process.exit(0);
}

const startNs = Bun.nanoseconds();
const spawnCmd = isWin
  ? ['cmd.exe', '/d', '/s', '/c', commandToRun]
  : ['bash', '-c', commandToRun];

const proc = Bun.spawn(spawnCmd, {
  cwd: repoRoot,
  stdout: 'inherit',
  stderr: 'inherit',
  env: { ...process.env, PYTHONIOENCODING: 'utf-8', SIVAC_RUNTIME: `bun-${bunVersion}` },
});

const exitCode = await proc.exited;
const elapsedMs = ((Bun.nanoseconds() - startNs) / 1_000_000).toFixed(2);
console.log(`[BUN EXIT] código=${exitCode} · tiempo=${elapsedMs}ms · runtime=Bun/${bunVersion}`);
process.exit(exitCode);
