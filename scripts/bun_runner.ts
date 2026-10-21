#!/usr/local/bin/bun
/**
 * Motor de Ejecución Ultrarrápido en Bun (SIVAC-THESIS-LAB)
 * Ejecuta subagentes de Claude Code (.claude/agents/*.md), Factory Droid (.factory/droids/*.md)
 * y comandos del ecosistema utilizando el runtime nativo de Bun (Bun.spawn).
 */
import fs from 'fs';
import path from 'path';

const args = Bun.argv.slice(2);
const modeArg = args.find((a) => a.startsWith('--mode='))?.split('=')[1] || 'bun';
const agentArg = args.find((a) => a.startsWith('--agent='))?.split('=')[1] || 'director-general';
const cmdIndex = args.indexOf('--cmd');
const commandToRun = cmdIndex !== -1 ? args.slice(cmdIndex + 1).join(' ') : args.join(' ');

const repoRoot = process.cwd();
const agentMdPath =
  modeArg === 'droid'
    ? path.join(repoRoot, '.factory', 'droids', `${agentArg}.md`)
    : path.join(repoRoot, '.claude', 'agents', `${agentArg}.md`);

const bunVersion = Bun.version;
console.log(`[BUN RUNTIME v${bunVersion}] Motor Bun inicializado en ${repoRoot}`);

if (fs.existsSync(agentMdPath)) {
  console.log(`[AGENTE CARGADO] ${path.relative(repoRoot, agentMdPath)} -> @${agentArg} (modo: ${modeArg.toUpperCase()})`);
}

if (!commandToRun.trim()) {
  console.log(`[BUN RUNTIME] Listo. Ningún subcomando especificado.`);
  process.exit(0);
}

const startNs = Bun.nanoseconds();
const proc = Bun.spawn(['bash', '-c', commandToRun], {
  cwd: repoRoot,
  stdout: 'inherit',
  stderr: 'inherit',
  env: { ...process.env, PYTHONIOENCODING: 'utf-8', SIVAC_RUNTIME: `bun-${bunVersion}` },
});

const exitCode = await proc.exited;
const elapsedMs = ((Bun.nanoseconds() - startNs) / 1_000_000).toFixed(2);
console.log(`[BUN EXIT] código=${exitCode} · tiempo=${elapsedMs}ms · runtime=Bun/${bunVersion}`);
process.exit(exitCode);
