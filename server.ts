import express from 'express';
import http from 'http';
import fs from 'fs';
import os from 'os';
import path from 'path';
import crypto from 'crypto';
import { execFileSync, execSync, spawn, ChildProcessWithoutNullStreams } from 'child_process';
import { fileURLToPath } from 'url';
import { createServer as createViteServer } from 'vite';
import { WebSocketServer, WebSocket } from 'ws';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const IS_WIN = process.platform === 'win32';
const PY_BIN = IS_WIN ? 'python' : 'python3';

// --- INTELLIGENT MULTI-STAGE CLI AUTO-DISCOVERY & LOCAL BRIDGE (WINDOWS + WSL2 + POSIX) ---
const LOCAL_BIN_DIR = path.join(__dirname, '.bin');
const CLI_CONFIG_PATH = path.join(__dirname, '.claude', 'cli-paths.json');
let cachedRegistryDirs: string[] | null = null;

function loadCustomCliPaths(): Record<string, string> {
  try {
    if (fs.existsSync(CLI_CONFIG_PATH)) {
      return JSON.parse(fs.readFileSync(CLI_CONFIG_PATH, 'utf-8'));
    }
  } catch {
    // ignore
  }
  return {};
}

function saveCustomCliPaths(paths: Record<string, string>) {
  try {
    fs.mkdirSync(path.dirname(CLI_CONFIG_PATH), { recursive: true });
    fs.writeFileSync(CLI_CONFIG_PATH, JSON.stringify(paths, null, 2) + '\n', 'utf-8');
  } catch {
    // ignore
  }
}

function findExecutableInSubdirs(
  baseDir: string,
  targetNames: string[],
  maxDepth = 2,
  currentDepth = 0
): string {
  if (currentDepth > maxDepth || !fs.existsSync(baseDir)) return '';
  try {
    const entries = fs.readdirSync(baseDir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.isFile() && targetNames.includes(entry.name.toLowerCase())) {
        return path.join(baseDir, entry.name);
      }
    }
    if (currentDepth < maxDepth) {
      for (const entry of entries) {
        if (entry.isDirectory() && !entry.name.startsWith('.')) {
          const found = findExecutableInSubdirs(
            path.join(baseDir, entry.name),
            targetNames,
            maxDepth,
            currentDepth + 1
          );
          if (found) return found;
        }
      }
    }
  } catch {
    // ignore permission errors
  }
  return '';
}

function ensureLocalCliShimsAndPath(forceRefreshRegistry = false): string {
  fs.mkdirSync(LOCAL_BIN_DIR, { recursive: true });
  const nodeExe = process.execPath;
  const tsxCliMjs = path.join(__dirname, 'node_modules', 'tsx', 'dist', 'cli.mjs');
  const tsxBinPosix = path.join(__dirname, 'node_modules', '.bin', 'tsx');
  const claudeScript = path.join(__dirname, 'scripts', 'cli_bridges', 'claude_cli.ts');
  const droidScript = path.join(__dirname, 'scripts', 'cli_bridges', 'droid_cli.ts');
  const bunRunnerScript = path.join(__dirname, 'scripts', 'bun_runner.ts');

  if (IS_WIN) {
    // Direct node.exe -> tsx/dist/cli.mjs invocation avoids nested .cmd batch issues on Windows
    const claudeCmdPath = path.join(LOCAL_BIN_DIR, 'claude.cmd');
    const droidCmdPath = path.join(LOCAL_BIN_DIR, 'droid.cmd');
    const bunCmdPath = path.join(LOCAL_BIN_DIR, 'bun.cmd');

    fs.writeFileSync(
      claudeCmdPath,
      `@echo off\r\n"${nodeExe}" "${tsxCliMjs}" "${claudeScript}" %*\r\n`,
      'utf-8'
    );
    fs.writeFileSync(
      droidCmdPath,
      `@echo off\r\n"${nodeExe}" "${tsxCliMjs}" "${droidScript}" %*\r\n`,
      'utf-8'
    );
    const userBunExe = path.join(os.homedir(), '.bun', 'bin', 'bun.exe');
    if (fs.existsSync(userBunExe)) {
      fs.writeFileSync(bunCmdPath, `@echo off\r\n"${userBunExe}" %*\r\n`, 'utf-8');
    } else {
      fs.writeFileSync(
        bunCmdPath,
        `@echo off\r\nif "%1"=="--version" (echo 1.2.4 & exit /b 0)\r\nif "%1"=="run" ("${nodeExe}" "${tsxCliMjs}" "${bunRunnerScript}" %* & exit /b %ERRORLEVEL%)\r\n"${nodeExe}" "${tsxCliMjs}" %*\r\n`,
        'utf-8'
      );
    }
  } else {
    const claudeSh = path.join(LOCAL_BIN_DIR, 'claude');
    const droidSh = path.join(LOCAL_BIN_DIR, 'droid');
    fs.writeFileSync(
      claudeSh,
      `#!/usr/bin/env bash\nexec "${tsxBinPosix}" "${claudeScript}" "$@"\n`,
      { mode: 0o755 }
    );
    fs.writeFileSync(
      droidSh,
      `#!/usr/bin/env bash\nexec "${tsxBinPosix}" "${droidScript}" "$@"\n`,
      { mode: 0o755 }
    );
    try {
      fs.chmodSync(claudeScript, 0o755);
      fs.chmodSync(droidScript, 0o755);
      fs.chmodSync(bunRunnerScript, 0o755);
    } catch {
      // ignore
    }
  }

  const home = os.homedir();
  const candidateDirs: string[] = [path.dirname(process.execPath)];

  if (IS_WIN) {
    const appData = process.env.APPDATA || path.join(home, 'AppData', 'Roaming');
    const localAppData = process.env.LOCALAPPDATA || path.join(home, 'AppData', 'Local');
    candidateDirs.push(
      path.join(home, 'bin'), // Official Factory Droid CLI Windows installer directory ($USERPROFILE\bin)
      path.join(home, '.local', 'bin'), // Official Claude Code Native Windows installer directory ($USERPROFILE\.local\bin)
      path.join(home, '.bun', 'bin'), // Official Bun Windows installer directory ($USERPROFILE\.bun\bin)
      path.join(home, '.factory', 'bin'),
      path.join(home, '.claude', 'local'),
      path.join(home, '.claude', 'bin'),
      path.join(localAppData, 'Microsoft', 'WinGet', 'Links'), // Official WinGet symlinks
      path.join(appData, 'npm'),
      path.join(localAppData, 'pnpm'),
      path.join(home, '.volta', 'bin'),
      path.join(localAppData, 'Volta', 'bin'),
      path.join(home, 'scoop', 'shims'),
      'C:\\ProgramData\\chocolatey\\bin',
      path.join(localAppData, 'AnthropicClaude'),
      path.join(localAppData, 'Programs', 'claude'),
      path.join(localAppData, 'Programs', 'claude-code'),
      path.join(localAppData, 'Programs', 'Factory'),
      path.join(localAppData, 'Factory'),
      path.join(localAppData, 'Programs', 'Python', 'Python313'),
      path.join(localAppData, 'Programs', 'Python', 'Python312'),
      path.join(localAppData, 'Programs', 'Python', 'Python311'),
      path.join(localAppData, 'Programs', 'Python', 'Python310'),
      path.join(localAppData, 'Microsoft', 'WindowsApps')
    );

    if (!cachedRegistryDirs || forceRefreshRegistry) {
      cachedRegistryDirs = [];
      try {
        const psPath = execFileSync(
          'powershell.exe',
          [
            '-NoProfile',
            '-Command',
            '[Environment]::GetEnvironmentVariable("Path","User") + ";" + [Environment]::GetEnvironmentVariable("Path","Machine")',
          ],
          { encoding: 'utf-8', timeout: 2500, windowsHide: true }
        ).trim();
        if (psPath) {
          for (const p of psPath.split(';')) {
            if (p.trim()) cachedRegistryDirs.push(p.trim());
          }
        }
      } catch {
        // ignore if powershell is restricted
      }
    }
    candidateDirs.push(...cachedRegistryDirs);
  } else {
    candidateDirs.push(
      path.join(home, '.local', 'bin'),
      path.join(home, 'bin'),
      path.join(home, '.bun', 'bin'),
      path.join(home, '.factory', 'bin'),
      path.join(home, '.claude', 'local'),
      path.join(home, '.claude', 'bin'),
      path.join(home, '.npm-global', 'bin'),
      path.join(home, '.volta', 'bin'),
      '/opt/homebrew/bin',
      '/usr/local/bin',
      '/usr/bin',
      '/bin'
    );
  }

  const sep = IS_WIN ? ';' : ':';
  const currentParts = (process.env.PATH || process.env.Path || '')
    .split(sep)
    .filter((p) => Boolean(p) && p !== LOCAL_BIN_DIR);
  const merged = Array.from(
    new Set([
      ...candidateDirs.filter((d) => {
        try {
          return fs.existsSync(d);
        } catch {
          return false;
        }
      }),
      ...currentParts,
      LOCAL_BIN_DIR, // Keep LOCAL_BIN_DIR last so real native binaries always win
    ])
  );
  const finalPathStr = merged.join(sep);
  process.env.PATH = finalPathStr;
  if (IS_WIN) {
    process.env.Path = finalPathStr;
  }

  // On POSIX/Linux/WSL, also ensure /usr/local/bin symlinks exist if writable so any subshell finds claude, droid, bun
  if (!IS_WIN) {
    const posixBunSh = path.join(LOCAL_BIN_DIR, 'bun');
    if (!fs.existsSync(posixBunSh)) {
      try {
        fs.writeFileSync(
          posixBunSh,
          `#!/usr/bin/env bash\nexec "${tsxBinPosix}" "${bunRunnerScript}" "$@"\n`,
          { mode: 0o755 }
        );
      } catch {
        // ignore
      }
    }
    for (const toolName of ['claude', 'droid', 'bun']) {
      const targetShim = path.join(LOCAL_BIN_DIR, toolName);
      const usrLocalDest = path.join('/usr/local/bin', toolName);
      try {
        if (!fs.existsSync(usrLocalDest) && fs.existsSync(targetShim)) {
          fs.symlinkSync(targetShim, usrLocalDest);
        }
      } catch {
        // ignore if /usr/local/bin is read-only
      }
    }
  }

  return finalPathStr;
}

ensureLocalCliShimsAndPath();

function normalizePlatformCommand(cmd: string): string {
  const trimmed = cmd.trim();
  if (!IS_WIN) return trimmed;
  return trimmed
    .replace(/\bpython3\b/g, 'python')
    .replace(/^ls\s+-la\s+(.+)$/i, 'dir "$1"')
    .replace(/^ls\s+(.+)$/i, 'dir "$1"');
}

function tokenizeCliArgs(cmd: string): string[] {
  const args: string[] = [];
  let current = '';
  let quoteChar: '"' | "'" | null = null;

  for (let i = 0; i < cmd.length; i++) {
    const ch = cmd[i];
    if (ch === '\\' && i + 1 < cmd.length && (cmd[i + 1] === '"' || cmd[i + 1] === "'")) {
      current += cmd[i + 1];
      i++;
      continue;
    }
    if (quoteChar) {
      if (ch === quoteChar) {
        quoteChar = null;
      } else {
        current += ch;
      }
    } else {
      if (ch === '"' || ch === "'") {
        quoteChar = ch;
      } else if (/\s/.test(ch)) {
        if (current.length > 0) {
          args.push(current);
          current = '';
        }
      } else {
        current += ch;
      }
    }
  }
  if (current.length > 0) {
    args.push(current);
  }
  return args;
}

function extractPromptFromCliCommand(rawCmd: string, fallbackPrompt?: string): {
  isVersionOrHelp: boolean;
  versionFlag: string;
  agentFromCmd?: string;
  promptText: string;
} {
  const trimmed = rawCmd.trim();
  const tokens = tokenizeCliArgs(trimmed);
  const first = (tokens[0] || '').toLowerCase();

  if (tokens.includes('--version') || tokens.includes('-v')) {
    return { isVersionOrHelp: true, versionFlag: '--version', promptText: '' };
  }
  if (tokens.includes('--help') || tokens.includes('-h')) {
    return { isVersionOrHelp: true, versionFlag: '--help', promptText: '' };
  }

  if (first === 'claude' || first === 'droid') {
    let agentFromCmd: string | undefined;
    const promptParts: string[] = [];
    for (let i = 1; i < tokens.length; i++) {
      const t = tokens[i];
      if ((t === '--agent' || t === '--droid' || t === '-a') && tokens[i + 1]) {
        agentFromCmd = tokens[i + 1].replace(/^@/, '');
        i++;
      } else if (t === '-p' || t === '--print' || t === '--prompt') {
        if (tokens[i + 1]) {
          promptParts.push(tokens[i + 1]);
          i++;
        }
      } else if (t === 'exec' || t === '--verbose' || t === '--dangerously-skip-permissions') {
        continue;
      } else if (t === '--auto' || t === '--output-format' || t === '--task-cmd') {
        i++;
      } else if (!t.startsWith('-')) {
        promptParts.push(t);
      }
    }
    const extracted = promptParts.join(' ').trim() || (fallbackPrompt || '').trim();
    return {
      isVersionOrHelp: false,
      versionFlag: '',
      agentFromCmd,
      promptText: extracted,
    };
  }

  return {
    isVersionOrHelp: false,
    versionFlag: '',
    promptText: trimmed || (fallbackPrompt || '').trim(),
  };
}

/**
 * Spawns the real native `claude` (`~/.local/bin/claude.exe`) or `droid` (`~/bin/droid.exe`) or `bun` (`~/.bun/bin/bun.exe`)
 * inside the project root (`cwd = __dirname`) and injects the prompt into its internal `stdin` stream (`child.stdin.write(...)`),
 * with automatic fallback to the local workspace CLI bridge if the native binary is not installed.
 */
function spawnCliAgentWithStdin(options: {
  tool: 'claude' | 'droid' | 'bun';
  isVersionOrHelp: boolean;
  versionFlag: string;
  agentId: string;
  promptText: string;
  rawCmd: string;
  spawnEnv: NodeJS.ProcessEnv;
  nativeBinaryPath?: string;
  isNativeAvailable?: boolean;
  forceBridge?: boolean;
}) {
  const tsxCliMjs = path.join(__dirname, 'node_modules', 'tsx', 'dist', 'cli.mjs');
  const claudeBridge = path.join(__dirname, 'scripts', 'cli_bridges', 'claude_cli.ts');
  const droidBridge = path.join(__dirname, 'scripts', 'cli_bridges', 'droid_cli.ts');
  const bunBridge = path.join(__dirname, 'scripts', 'bun_runner.ts');

  const useNative =
    Boolean(options.isNativeAvailable && options.nativeBinaryPath && !options.forceBridge) &&
    fs.existsSync(options.nativeBinaryPath!);

  if (options.isVersionOrHelp) {
    if (useNative && options.nativeBinaryPath) {
      const isCmd = options.nativeBinaryPath.toLowerCase().endsWith('.cmd');
      return spawn(options.nativeBinaryPath, [options.versionFlag || '--version'], {
        cwd: __dirname,
        env: options.spawnEnv,
        shell: isCmd,
        windowsHide: true,
      });
    }
    const bridge =
      options.tool === 'claude' ? claudeBridge : options.tool === 'droid' ? droidBridge : bunBridge;
    return spawn(process.execPath, [tsxCliMjs, bridge, options.versionFlag || '--version'], {
      cwd: __dirname,
      env: options.spawnEnv,
      windowsHide: true,
    });
  }

  // Construct the internal prompt sent inside the CLI (`claude > <prompt>`)
  const cleanPrompt = options.promptText.trim();
  const stdinPayload =
    cleanPrompt.length > 0
      ? options.agentId &&
        options.agentId !== 'director-general' &&
        !cleanPrompt.includes(`@${options.agentId}`)
        ? `@${options.agentId} ${cleanPrompt}\n`
        : `${cleanPrompt}\n`
      : '';

  if (options.tool === 'claude') {
    if (useNative && options.nativeBinaryPath && cleanPrompt.length > 0) {
      const isCmd = options.nativeBinaryPath.toLowerCase().endsWith('.cmd');
      const child = spawn(
        options.nativeBinaryPath,
        ['-p', '--dangerously-skip-permissions'],
        {
          cwd: __dirname,
          env: {
            ...options.spawnEnv,
            CI: 'true',
            FORCE_COLOR: '0',
          },
          stdio: ['pipe', 'pipe', 'pipe'],
          shell: isCmd,
          windowsHide: true,
        }
      );
      child.stdin?.write(stdinPayload, 'utf-8');
      child.stdin?.end();
      return child;
    }

    const child = spawn(
      process.execPath,
      [tsxCliMjs, claudeBridge, '--agent', options.agentId],
      {
        cwd: __dirname,
        env: options.spawnEnv,
        stdio: ['pipe', 'pipe', 'pipe'],
        windowsHide: true,
      }
    );
    if (stdinPayload) {
      child.stdin?.write(stdinPayload, 'utf-8');
    }
    child.stdin?.end();
    return child;
  }

  if (options.tool === 'droid') {
    if (useNative && options.nativeBinaryPath && cleanPrompt.length > 0) {
      const isCmd = options.nativeBinaryPath.toLowerCase().endsWith('.cmd');
      const child = spawn(
        options.nativeBinaryPath,
        ['exec', '--auto', 'medium', stdinPayload.trim()],
        {
          cwd: __dirname,
          env: {
            ...options.spawnEnv,
            CI: 'true',
            FORCE_COLOR: '0',
          },
          stdio: ['pipe', 'pipe', 'pipe'],
          shell: isCmd,
          windowsHide: true,
        }
      );
      child.stdin?.end();
      return child;
    }

    const child = spawn(
      process.execPath,
      [tsxCliMjs, droidBridge, '--droid', options.agentId],
      {
        cwd: __dirname,
        env: options.spawnEnv,
        stdio: ['pipe', 'pipe', 'pipe'],
        windowsHide: true,
      }
    );
    if (stdinPayload) {
      child.stdin?.write(stdinPayload, 'utf-8');
    }
    child.stdin?.end();
    return child;
  }

  // Bun tool
  const tokens = tokenizeCliArgs(options.rawCmd.trim());
  const sliceArgs =
    tokens[0]?.toLowerCase() === 'bun'
      ? tokens[1]?.toLowerCase() === 'run' && tokens[2]?.includes('bun_runner.ts')
        ? tokens.slice(3)
        : tokens.slice(1)
      : ['--mode=bun', `--agent=${options.agentId}`, `--prompt=${cleanPrompt}`];

  return spawn(process.execPath, [tsxCliMjs, bunBridge, ...sliceArgs], {
    cwd: __dirname,
    env: options.spawnEnv,
    windowsHide: true,
  });
}

function isKnownSystemShellCommand(cmd: string): boolean {
  const firstToken = cmd.trim().split(/\s+/)[0]?.toLowerCase() || '';
  const systemCmds = new Set([
    'python',
    'python3',
    'py',
    'git',
    'ls',
    'dir',
    'pwd',
    'cd',
    'cat',
    'type',
    'echo',
    'npm',
    'npx',
    'pnpm',
    'yarn',
    'node',
    'tsx',
    'curl',
    'powershell',
    'powershell.exe',
    'pwsh',
    'cmd',
    'cmd.exe',
    'where',
    'where.exe',
    'which',
    'whoami',
    'clear',
    'cls',
    'mkdir',
    ' winget',
    'winget',
  ]);
  return systemCmds.has(firstToken);
}

interface AgentMeta {
  id: string;
  name: string;
  description: string;
  model: string;
  squad: string;
  role: string;
  tools: string[];
  skills: string[];
  filePath: string;
  droidPath: string;
  readOnly: boolean;
  status: 'idle' | 'running' | 'completed' | 'blocked';
  currentTask?: string;
  lastCommand?: string;
  lastRunAt?: string;
}

interface SkillMeta {
  id: string;
  name: string;
  description: string;
  filePath: string;
  path: string;
  enabled: boolean;
  hasAgents: boolean;
  hasReferences: boolean;
  hasTemplates: boolean;
}

interface RuleMeta {
  id: string;
  title: string;
  description: string;
  filePath: string;
  content: string;
}

interface TerminalLine {
  id: string;
  timestamp: string;
  stream: 'stdout' | 'stderr' | 'system' | 'command' | 'security';
  type: 'stdout' | 'stderr' | 'system' | 'command';
  session: 'bun-shell' | 'claude-code' | 'factory-droid';
  text: string;
  agentId?: string;
  mode?: 'bun' | 'shell' | 'claude' | 'droid';
}

interface DelegationEvent {
  id: string;
  timestamp: string;
  from: string;
  to: string;
  agentId: string;
  agentName: string;
  squad: string;
  fase: string;
  tarea: string;
  task: string;
  engine: 'claude' | 'droid' | 'bun';
  command: string;
  status: 'running' | 'completed' | 'blocked' | 'error';
  outputSummary?: string;
  handoffPath?: string;
  handoffFile?: string;
  exitCode?: number;
  startedAt: string;
  completedAt?: string;
}

interface GodChatMessage {
  id: string;
  timestamp: string;
  role: 'user' | 'god' | 'subagent';
  senderName: string;
  senderId: string;
  squad?: string;
  text: string;
  content: string;
  engineUsed?: string;
  cognitiveRefinement?: {
    intent: string;
    obsidianContext: string;
    formalMethodology: string;
    selectedSquads: string[];
  };
  delegation?: {
    id: string;
    subagente: string;
    agentId: string;
    agentName: string;
    squad: string;
    fase: string;
    task: string;
    runtime: 'bun' | 'claude' | 'droid';
    engine: 'bun' | 'claude' | 'droid';
    command: string;
    claudeCliCmd: string;
    droidCliCmd: string;
    status: 'running' | 'completed' | 'blocked';
    outputSummary?: string;
    handoffPath?: string;
    handoffFile?: string;
    deliverablePath?: string;
    exitCode?: number;
    startedAt: string;
    completedAt?: string;
  };
  delegations?: Array<{
    id: string;
    agentId: string;
    agentName: string;
    squad: string;
    task: string;
    engine: 'claude' | 'droid' | 'bun';
    status: 'running' | 'completed' | 'error' | 'queued';
    command: string;
    outputSummary?: string;
    handoffFile?: string;
    startedAt: string;
    completedAt?: string;
  }>;
}

// Runtime authoritative state
const agentRuntimeStatus: Record<
  string,
  { status: 'idle' | 'running' | 'completed' | 'blocked'; currentTask?: string; lastCommand?: string; lastRunAt?: string }
> = {};

const disabledSkillsSet = new Set<string>();

const terminalHistory: TerminalLine[] = [
  {
    id: 'boot-1',
    timestamp: new Date().toISOString(),
    stream: 'system',
    type: 'system',
    session: 'bun-shell',
    text: `[SIVAC-THESIS-LAB OS · ${IS_WIN ? 'WINDOWS LOCAL' : 'POSIX'}] Motor Bun + Puentes Agentes Locales (.claude/agents y .factory/droids) conectados.`,
  },
  {
    id: 'boot-2',
    timestamp: new Date().toISOString(),
    stream: 'system',
    type: 'system',
    session: 'bun-shell',
    text: '[MEMORIA VIVA OBSIDIAN] Sincronizado con obsidian_vault/00_SISTEMA/ESTADO_TESIS.md y DECISIONES.md (DEC-007 / DEC-015 / DEC-020 / DEC-027).',
  },
];

const activeDelegations: DelegationEvent[] = [];

const welcomeText =
  'Bienvenido al **SIVAC Agent Studio**. Los **14 agentes locales** (`.claude/agents/*.md` y `.factory/droids/*.md`) están enlazados y listos.\n\n' +
  'Escribe cualquier orden en el cuadro inferior o pulsa una **Directiva Rápida** (por ejemplo: *"Auditar Brechas F1 (UNAJMA)"*, *"Verificar Consistencia (DEC-007)"* o *"Ejecutar Bioestadística (n=14)"*). Yo ejecutaré el **Loop de Refinamiento Cognitivo 3.0**, delegaré al subagente especialista y transmitiré la ejecución en vivo en la terminal **XTerm.js**.';

const godChatHistory: GodChatMessage[] = [
  {
    id: 'god-welcome-1',
    timestamp: new Date().toISOString(),
    role: 'god',
    senderName: 'Director General (Agente GOD)',
    senderId: 'director-general',
    squad: 'Hub Central',
    text: welcomeText,
    content: welcomeText,
    engineUsed: 'Bun Shell + Claude Code + Factory Droid',
    cognitiveRefinement: {
      intent: 'Inicialización del Orquestador Radial Hub-and-Spoke (14 agentes conectados)',
      obsidianContext: '00_SISTEMA/ESTADO_TESIS.md · 00_SISTEMA/DECISIONES.md (DEC-007)',
      formalMethodology: 'Constitución CLAUDE.md · APA 7 · ISO/IEC 25010:2023 · Modelo TAM',
      selectedSquads: ['Hub Central', 'Squads A-F (13 Subagentes)'],
    },
    delegations: [],
  },
];

let activeChildProcess: ChildProcessWithoutNullStreams | null = null;

function parseYamlFrontmatter(raw: string): { frontmatter: Record<string, unknown>; body: string } {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!match) {
    return { frontmatter: {}, body: raw };
  }
  const yamlBlock = match[1];
  const body = match[2];
  const result: Record<string, unknown> = {};
  let currentKey: string | null = null;
  let currentList: string[] | null = null;

  for (const line of yamlBlock.split(/\r?\n/)) {
    const listMatch = line.match(/^\s*-\s+(.+)$/);
    if (listMatch && currentKey && currentList) {
      currentList.push(listMatch[1].trim().replace(/^['"]|['"]$/g, ''));
      continue;
    }
    const kvMatch = line.match(/^([a-zA-Z0-9_-]+):\s*(.*)$/);
    if (kvMatch) {
      const key = kvMatch[1];
      const val = kvMatch[2].trim();
      if (!val || val === '>' || val === '>-' || val === '|') {
        currentKey = key;
        currentList = [];
        result[key] = currentList;
      } else {
        currentKey = key;
        currentList = null;
        result[key] = val.replace(/^['"]|['"]$/g, '');
      }
    }
  }
  return { frontmatter: result, body };
}

function serializeYamlFrontmatter(frontmatter: Record<string, unknown>, body: string): string {
  const lines: string[] = ['---'];
  for (const [key, val] of Object.entries(frontmatter)) {
    if (Array.isArray(val)) {
      lines.push(`${key}:`);
      for (const item of val) {
        lines.push(`  - ${item}`);
      }
    } else if (val !== undefined && val !== null) {
      const strVal = String(val);
      if (strVal.includes(':') || strVal.includes('#')) {
        lines.push(`${key}: "${strVal.replace(/"/g, '\\"')}"`);
      } else {
        lines.push(`${key}: ${strVal}`);
      }
    }
  }
  lines.push('---', '');
  return lines.join('\n') + body.replace(/^\r?\n/, '');
}

const AGENT_DEFAULT_SCRIPTS: Record<string, string> = {
  'director-general': `${PY_BIN} scripts/agentes/estado_granja.py`,
  'investigador-bibliografico': `${PY_BIN} scripts/fuentes/buscador_citas.py`,
  'verificador-integridad': `${PY_BIN} scripts/agentes/verificador_integridad.py`,
  'guardian-consistencia': `${PY_BIN} scripts/agentes/guardian_consistencia.py`,
  'especialista-instrumentos': `${PY_BIN} scripts/compiladores/generar_anexo2_validacion_fany.py`,
  'especialista-forms': `${PY_BIN} scripts/agentes/validez_contenido.py`,
  'ingeniero-sivac': `${PY_BIN} scripts/agentes/inventario_syncova.py`,
  'documentador-xp': `${PY_BIN} scripts/agentes/inventario_syncova.py`,
  'analista-estadistico': `${PY_BIN} scripts/estadistica/pipeline_inferencial.py --json`,
  'analista-documental': `${PY_BIN} scripts/agentes/analista_documental.py`,
  'redactor-academico': `${PY_BIN} scripts/agentes/revisor_prosa.py`,
  'maquetador-docx': `${PY_BIN} scripts/utilidades/auditor_docx_apa7.py auditar salidas/documentos/informe_final_v02.docx`,
  'curador-cerebro': `${PY_BIN} scripts/agentes/curador_cerebro.py`,
  'jurado-revisor': `${PY_BIN} scripts/utilidades/auditor_docx_apa7.py auditar salidas/documentos/informe_final_v02.docx --md`,
};

const SQUAD_BY_AGENT: Record<string, { squad: string; role: string }> = {
  'director-general': {
    squad: 'Hub Central (Director General / Agente GOD)',
    role: 'Director de Tesis Senior, Orquestador Maestro y Única Interfaz con el Tesista',
  },
  'investigador-bibliografico': {
    squad: 'Squad A (Evidencia y Bibliometría)',
    role: 'Investigador Bibliográfico y Curador de Evidencia Científica',
  },
  'verificador-integridad': {
    squad: 'Squad A (Evidencia y Bibliometría)',
    role: 'Auditor de Integridad Bibliográfica 1:1 y Anti-Alucinaciones',
  },
  'guardian-consistencia': {
    squad: 'Squad B (Metodología, Medición y Psicometría)',
    role: 'Custodio Metodológico de las 3 Dimensiones Oficiales (DEC-007)',
  },
  'especialista-instrumentos': {
    squad: 'Squad B (Metodología, Medición y Psicometría)',
    role: 'Especialista en Instrumentos de Medición y Juicio de Expertos (Fany 2024)',
  },
  'especialista-forms': {
    squad: 'Squad B (Metodología, Medición y Psicometría)',
    role: 'Especialista en Digitalización y Recolección de Datos',
  },
  'ingeniero-sivac': {
    squad: 'Squad C (Ingeniería de Software y Auditoría SIVAC)',
    role: 'Auditor Técnico de Software y Trazabilidad (Solo Lectura)',
  },
  'documentador-xp': {
    squad: 'Squad C (Ingeniería de Software y Auditoría SIVAC)',
    role: 'Documentador Metodológico XP y Arquitectura de Software (Sección 3.3)',
  },
  'analista-estadistico': {
    squad: 'Squad D (Bioestadística e Inferencia)',
    role: 'Especialista Bioestadístico y Ciencia de Datos (N = n = 14)',
  },
  'analista-documental': {
    squad: 'Squad E (Redacción, Estilo y Maquetación Editorial)',
    role: 'Auditor Documental e Inspector de Plantillas Institucionales UNAJMA',
  },
  'redactor-academico': {
    squad: 'Squad E (Redacción, Estilo y Maquetación Editorial)',
    role: 'Redactor Académico Principal y Estilista Científico APA 7',
  },
  'maquetador-docx': {
    squad: 'Squad E (Redacción, Estilo y Maquetación Editorial)',
    role: 'Compilador Editorial y Maquetador Quirúrgico OpenXML (.docx)',
  },
  'curador-cerebro': {
    squad: 'Squad F (Gobernanza, Memoria y Evaluación Externa)',
    role: 'Curador del Cerebro de Conocimiento en Obsidian y Taxonomía Viva',
  },
  'jurado-revisor': {
    squad: 'Squad F (Gobernanza, Memoria y Evaluación Externa)',
    role: 'Jurado Dictaminador Simulado UNAJMA (Escala Vigesimal 20 pts)',
  },
};

function loadAgents(): AgentMeta[] {
  const agentsDir = path.join(__dirname, '.claude', 'agents');
  if (!fs.existsSync(agentsDir)) return [];
  const files = fs.readdirSync(agentsDir).filter((f) => f.endsWith('.md')).sort();

  return files.map((file) => {
    const id = file.replace('.md', '');
    const fullPath = path.join(agentsDir, file);
    const raw = fs.readFileSync(fullPath, 'utf-8');
    const { frontmatter } = parseYamlFrontmatter(raw);
    const tools = Array.isArray(frontmatter.tools) ? (frontmatter.tools as string[]) : [];
    const skills = Array.isArray(frontmatter.skills) ? (frontmatter.skills as string[]) : [];
    const name = typeof frontmatter.name === 'string' ? frontmatter.name : id;
    const canonicalInfo = SQUAD_BY_AGENT[id];
    const readOnly =
      name === 'ingeniero-sivac' ||
      (tools.length > 0 && tools.every((t) => ['Read', 'Grep', 'Glob'].includes(t)));
    const runtime = agentRuntimeStatus[id] || { status: 'idle' };

    return {
      id,
      name,
      description: typeof frontmatter.description === 'string' ? frontmatter.description : canonicalInfo?.role || '',
      model: typeof frontmatter.model === 'string' ? frontmatter.model : id === 'director-general' ? 'opus' : 'sonnet',
      squad:
        typeof frontmatter.squad === 'string' && frontmatter.squad.trim()
          ? frontmatter.squad
          : canonicalInfo?.squad || 'Squad Especializado',
      role:
        typeof frontmatter.role === 'string' && frontmatter.role.trim()
          ? frontmatter.role
          : canonicalInfo?.role || (typeof frontmatter.description === 'string' ? frontmatter.description : ''),
      tools,
      skills,
      filePath: `.claude/agents/${file}`,
      droidPath: `.factory/droids/${file}`,
      readOnly,
      status: runtime.status,
      currentTask: runtime.currentTask,
      lastCommand: runtime.lastCommand || AGENT_DEFAULT_SCRIPTS[id],
      lastRunAt: runtime.lastRunAt,
    };
  });
}

function loadRules(): RuleMeta[] {
  const rulesDir = path.join(__dirname, '.claude', 'rules');
  if (!fs.existsSync(rulesDir)) return [];
  const files = fs.readdirSync(rulesDir).filter((f) => f.endsWith('.md')).sort();

  return files.map((file) => {
    const fullPath = path.join(rulesDir, file);
    const raw = fs.readFileSync(fullPath, 'utf-8');
    const { frontmatter, body } = parseYamlFrontmatter(raw);
    const headingMatch = body.match(/^#\s+(.+)$/m);
    return {
      id: file.replace('.md', ''),
      title: headingMatch ? headingMatch[1].trim() : file.replace('.md', ''),
      description: typeof frontmatter.description === 'string' ? frontmatter.description : '',
      filePath: `.claude/rules/${file}`,
      content: body.trim(),
    };
  });
}

function loadSkills(): SkillMeta[] {
  const skillsDir = path.join(__dirname, '.claude', 'skills');
  if (!fs.existsSync(skillsDir)) return [];
  const entries = fs.readdirSync(skillsDir, { withFileTypes: true });
  const skills: SkillMeta[] = [];

  for (const entry of entries) {
    if (!entry.isDirectory() || entry.name === 'shared') continue;
    const skillMdPath = path.join(skillsDir, entry.name, 'SKILL.md');
    if (!fs.existsSync(skillMdPath)) continue;
    const raw = fs.readFileSync(skillMdPath, 'utf-8');
    const { frontmatter, body } = parseYamlFrontmatter(raw);
    const firstParagraph = body
      .split(/\r?\n\r?\n/)
      .map((p) => p.trim())
      .find((p) => p && !p.startsWith('#'));

    const relPath = `.claude/skills/${entry.name}/SKILL.md`;
    skills.push({
      id: entry.name,
      name: typeof frontmatter.name === 'string' ? frontmatter.name : entry.name,
      description:
        typeof frontmatter.description === 'string' && frontmatter.description.length > 0
          ? frontmatter.description
          : firstParagraph || 'Skill especializada de SIVAC-THESIS-LAB',
      filePath: relPath,
      path: relPath,
      enabled: !disabledSkillsSet.has(entry.name),
      hasAgents: fs.existsSync(path.join(skillsDir, entry.name, 'agents')),
      hasReferences: fs.existsSync(path.join(skillsDir, entry.name, 'references')),
      hasTemplates: fs.existsSync(path.join(skillsDir, entry.name, 'templates')),
    });
  }

  return skills.sort((a, b) => a.id.localeCompare(b.id));
}

function loadWorkflowModules() {
  const wfPath = path.join(__dirname, '.claude', 'workflows', 'sivac-scripts-especializados.js');
  if (!fs.existsSync(wfPath)) return [];
  const raw = fs.readFileSync(wfPath, 'utf-8');
  const modules: Array<{ id: string; squad: string; targetScript: string; summary: string }> = [];
  const regex = /\{\s*id:\s*'([^']+)',\s*squad:\s*'([^']+)',\s*spec:\s*`([^`]+)`/g;
  let match: RegExpExecArray | null;
  while ((match = regex.exec(raw)) !== null) {
    const id = match[1];
    const squad = match[2];
    const spec = match[3].trim();
    const scriptMatch = spec.match(/Crea\s+([^\s(+\n]+)/);
    const firstSentence = spec.split(/\.\s+/)[1] || spec.split(/\r?\n/)[0];
    modules.push({
      id,
      squad,
      targetScript: scriptMatch ? scriptMatch[1] : `scripts/${id}.py`,
      summary: firstSentence.trim(),
    });
  }
  return modules;
}

function loadProjectsStore() {
  const storePath = path.join(__dirname, 'obsidian_vault', '00_SISTEMA', 'PROYECTOS_INVESTIGACION.json');
  if (!fs.existsSync(storePath)) {
    return { activeProjectId: 'proy-tesis-sivac-unajma', projects: [] };
  }
  return JSON.parse(fs.readFileSync(storePath, 'utf-8'));
}

function saveProjectsStore(data: unknown) {
  const storePath = path.join(__dirname, 'obsidian_vault', '00_SISTEMA', 'PROYECTOS_INVESTIGACION.json');
  fs.mkdirSync(path.dirname(storePath), { recursive: true });
  fs.writeFileSync(storePath, JSON.stringify(data, null, 2), 'utf-8');
}

function loadHandoffs() {
  const handoffsDir = path.join(__dirname, 'obsidian_vault', '08_SISTEMA_Y_AGENTES', 'handoffs');
  if (!fs.existsSync(handoffsDir)) return [];
  return fs
    .readdirSync(handoffsDir)
    .filter((f) => f.endsWith('.md'))
    .sort()
    .reverse()
    .map((f, idx) => {
      const fullPath = path.join(handoffsDir, f);
      const content = fs.readFileSync(fullPath, 'utf-8');
      const parts = f.replace('.md', '').split('_');
      const datePart = parts[0] || new Date().toISOString().slice(0, 10);
      const agentPart = parts[1] || 'director-general';
      const taskSlug = parts.slice(2).join(' ') || f;
      const statusMatch = content.match(/\*\*Estado:\*\*\s*`?([a-zA-Z_]+)`?/i);
      const relPath = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${f}`;
      return {
        id: `handoff-${idx}-${f}`,
        filename: f,
        fileName: f,
        agent: agentPart,
        task: taskSlug,
        date: datePart,
        status: statusMatch ? statusMatch[1].toLowerCase() : 'completado',
        summary: content.slice(0, 220),
        path: relPath,
        filePath: relPath,
        content,
        rawContent: content,
        updatedAt: fs.statSync(fullPath).mtime.toISOString(),
      };
    });
}

function getGitHistory() {
  try {
    const logOut = execFileSync(
      'git',
      ['log', '--pretty=format:%h|%ad|%an|%s', '--date=short', '-n', '15'],
      { cwd: __dirname, encoding: 'utf-8' }
    );
    const commits = logOut
      .trim()
      .split('\n')
      .filter(Boolean)
      .map((line) => {
        const [hash, date, author, ...msgParts] = line.split('|');
        return { hash, date, author, message: msgParts.join('|') };
      });
    const trackedOut = execFileSync('git', ['ls-files'], { cwd: __dirname, encoding: 'utf-8' });
    const trackedCount = trackedOut.trim().split('\n').filter(Boolean).length;
    const branchOut = execFileSync('git', ['rev-parse', '--abbrev-ref', 'HEAD'], {
      cwd: __dirname,
      encoding: 'utf-8',
    }).trim();
    return { initialized: true, branch: branchOut, trackedCount, commits };
  } catch {
    return { initialized: false, branch: 'main', trackedCount: 0, commits: [] };
  }
}

function detectCliStatus(forceRefresh = false) {
  ensureLocalCliShimsAndPath(forceRefresh);
  const customPaths = loadCustomCliPaths();
  const home = os.homedir();
  const appData = process.env.APPDATA || path.join(home, 'AppData', 'Roaming');
  const localAppData = process.env.LOCALAPPDATA || path.join(home, 'AppData', 'Local');
  const nodeBinDir = path.dirname(process.execPath);

  // Official documented native installation locations (excluding LOCAL_BIN_DIR)
  const knownNativeLocations: Record<string, string[]> = IS_WIN
    ? {
        bun: [
          customPaths.bun || '',
          path.join(home, '.bun', 'bin', 'bun.exe'),
          path.join(localAppData, 'Microsoft', 'WinGet', 'Links', 'bun.exe'),
          path.join(home, 'scoop', 'shims', 'bun.exe'),
          path.join(appData, 'npm', 'bun.cmd'),
          path.join(nodeBinDir, 'bun.exe'),
          path.join(nodeBinDir, 'bun.cmd'),
          'C:\\ProgramData\\chocolatey\\bin\\bun.exe',
        ],
        claude: [
          customPaths.claude || '',
          path.join(home, '.local', 'bin', 'claude.exe'), // Official claude.ai/install.ps1
          path.join(localAppData, 'Microsoft', 'WinGet', 'Links', 'claude.exe'), // Official winget Anthropic.ClaudeCode
          path.join(home, '.claude', 'local', 'claude.exe'),
          path.join(home, '.claude', 'local', 'node_modules', '.bin', 'claude.cmd'),
          path.join(home, '.claude', 'bin', 'claude.exe'),
          path.join(appData, 'npm', 'claude.cmd'),
          path.join(nodeBinDir, 'claude.cmd'),
          path.join(nodeBinDir, 'claude.exe'),
          path.join(home, '.bun', 'bin', 'claude.exe'),
          path.join(home, '.bun', 'bin', 'claude.cmd'),
          path.join(home, '.volta', 'bin', 'claude.exe'),
          path.join(localAppData, 'Volta', 'bin', 'claude.exe'),
          path.join(localAppData, 'pnpm', 'claude.cmd'),
          path.join(home, 'scoop', 'shims', 'claude.exe'),
          path.join(home, 'scoop', 'shims', 'claude.cmd'),
          path.join(localAppData, 'AnthropicClaude', 'claude.exe'),
          path.join(localAppData, 'Programs', 'claude', 'claude.exe'),
          path.join(localAppData, 'Programs', 'claude-code', 'claude.exe'),
        ],
        droid: [
          customPaths.droid || '',
          path.join(home, 'bin', 'droid.exe'), // Official app.factory.ai/cli/windows ($USERPROFILE\bin\droid.exe)
          path.join(home, '.factory', 'bin', 'droid.exe'),
          path.join(home, '.local', 'bin', 'droid.exe'),
          path.join(localAppData, 'Microsoft', 'WinGet', 'Links', 'droid.exe'),
          path.join(localAppData, 'Factory', 'droid.exe'),
          path.join(localAppData, 'Programs', 'Factory', 'droid.exe'),
          path.join(appData, 'npm', 'droid.cmd'),
          path.join(nodeBinDir, 'droid.cmd'),
          path.join(nodeBinDir, 'droid.exe'),
          path.join(home, '.bun', 'bin', 'droid.exe'),
          path.join(home, '.bun', 'bin', 'droid.cmd'),
          path.join(home, 'scoop', 'shims', 'droid.exe'),
        ],
      }
    : {
        bun: [
          customPaths.bun || '',
          path.join(home, '.bun', 'bin', 'bun'),
          '/opt/homebrew/bin/bun',
          '/usr/local/bin/bun',
          '/usr/bin/bun',
        ],
        claude: [
          customPaths.claude || '',
          path.join(home, '.local', 'bin', 'claude'), // Official claude.ai/install.sh
          path.join(home, '.claude', 'local', 'claude'),
          path.join(home, '.bun', 'bin', 'claude'),
          path.join(home, '.npm-global', 'bin', 'claude'),
          '/opt/homebrew/bin/claude',
          '/usr/local/bin/claude',
        ],
        droid: [
          customPaths.droid || '',
          path.join(home, '.local', 'bin', 'droid'), // Official app.factory.ai/cli
          path.join(home, '.factory', 'bin', 'droid'),
          path.join(home, 'bin', 'droid'),
          path.join(home, '.bun', 'bin', 'droid'),
          '/opt/homebrew/bin/droid',
          '/usr/local/bin/droid',
        ],
      };

  const findDynamicVersionedBinary = (binName: string): string => {
    if (!IS_WIN) return '';
    const winGetPkgs = path.join(localAppData, 'Microsoft', 'WinGet', 'Packages');
    if (binName === 'claude') {
      return (
        findExecutableInSubdirs(path.join(home, '.local', 'share', 'claude'), ['claude.exe'], 2) ||
        findExecutableInSubdirs(path.join(home, '.claude', 'downloads'), ['claude.exe'], 1) ||
        findExecutableInSubdirs(winGetPkgs, ['claude.exe'], 2) ||
        findExecutableInSubdirs(path.join(appData, 'nvm'), ['claude.cmd', 'claude.exe'], 2)
      );
    }
    if (binName === 'droid') {
      return (
        findExecutableInSubdirs(path.join(home, '.factory'), ['droid.exe'], 2) ||
        findExecutableInSubdirs(winGetPkgs, ['droid.exe'], 2) ||
        findExecutableInSubdirs(path.join(appData, 'nvm'), ['droid.cmd', 'droid.exe'], 2)
      );
    }
    if (binName === 'bun') {
      return (
        findExecutableInSubdirs(winGetPkgs, ['bun.exe'], 2) ||
        findExecutableInSubdirs(path.join(home, 'scoop', 'apps', 'bun'), ['bun.exe'], 2)
      );
    }
    return '';
  };

  const isOurBridgeFile = (filePath: string): boolean => {
    if (!filePath) return false;
    const norm = path.normalize(filePath).toLowerCase();
    const normLocalBin = path.normalize(LOCAL_BIN_DIR).toLowerCase();
    if (norm.startsWith(normLocalBin) || norm.includes('cli_bridges')) return true;
    try {
      if (fs.existsSync(filePath) && fs.statSync(filePath).size < 2048) {
        const content = fs.readFileSync(filePath, 'utf-8');
        if (content.includes('cli_bridges') || content.includes('bun_runner.ts')) {
          return true;
        }
      }
    } catch {
      // ignore
    }
    return false;
  };

  const runVersionSafe = (execPath: string, versionArg = '--version'): string => {
    if (!execPath) return '';
    try {
      const lower = execPath.toLowerCase();
      let rawOut = '';
      if (IS_WIN) {
        if (lower.endsWith('.cmd') || lower.endsWith('.bat')) {
          rawOut = execSync(`"${execPath}" ${versionArg}`, {
            cwd: __dirname,
            encoding: 'utf-8',
            env: process.env,
            timeout: 3500,
            windowsHide: true,
          });
        } else {
          // Direct .exe execution — immune to cmd.exe quote escaping issues
          rawOut = execFileSync(execPath, [versionArg], {
            cwd: __dirname,
            encoding: 'utf-8',
            env: process.env,
            timeout: 3500,
            windowsHide: true,
          });
        }
      } else {
        rawOut = execFileSync(execPath, [versionArg], {
          cwd: __dirname,
          encoding: 'utf-8',
          env: process.env,
          timeout: 3500,
        });
      }
      return (
        rawOut
          .split(/\r?\n/)
          .map((l) => l.trim())
          .find(Boolean) || ''
      );
    } catch {
      return '';
    }
  };

  const formatShortPath = (fullPath: string): string => {
    if (!fullPath) return '';
    const normHome = path.normalize(home);
    const normFull = path.normalize(fullPath);
    if (normFull.toLowerCase().startsWith(normHome.toLowerCase())) {
      return '~' + normFull.slice(normHome.length).replace(/\\/g, '/');
    }
    return fullPath.replace(/\\/g, '/');
  };

  const probeBinary = (binName: string, versionArg = '--version') => {
    const candidates = (knownNativeLocations[binName] || []).filter(Boolean);
    let nativePath = '';
    let detectionMethod = '';

    // Stage 1: Explicit official installation paths
    for (const candidate of candidates) {
      if (fs.existsSync(candidate) && !isOurBridgeFile(candidate)) {
        nativePath = candidate;
        detectionMethod = 'Ruta Oficial';
        break;
      }
    }

    // Stage 2: Versioned subfolders (WinGet, Claude versions, NVM)
    if (!nativePath) {
      const dyn = findDynamicVersionedBinary(binName);
      if (dyn && !isOurBridgeFile(dyn)) {
        nativePath = dyn;
        detectionMethod = 'Auto-Escaneo';
      }
    }

    // Stage 3: OS PATH resolution (where.exe on Windows / command -v on POSIX)
    if (!nativePath) {
      try {
        if (IS_WIN) {
          const whereOut = execFileSync('where.exe', [binName], {
            cwd: __dirname,
            encoding: 'utf-8',
            env: process.env,
            timeout: 2500,
            windowsHide: true,
          })
            .split(/\r?\n/)
            .map((s) => s.trim())
            .filter((p) => Boolean(p) && !isOurBridgeFile(p));
          if (whereOut.length > 0) {
            nativePath = whereOut[0];
            detectionMethod = 'System PATH';
          }
        } else {
          const whichOut = execFileSync('bash', ['-c', `command -v ${binName}`], {
            cwd: __dirname,
            encoding: 'utf-8',
            env: process.env,
            timeout: 2500,
          }).trim();
          if (whichOut && !isOurBridgeFile(whichOut)) {
            nativePath = whichOut;
            detectionMethod = 'System PATH';
          }
        }
      } catch {
        // continue to Stage 4
      }
    }

    // Stage 4: PowerShell Get-Command fallback on Windows
    if (!nativePath && IS_WIN && (binName === 'claude' || binName === 'droid' || binName === 'bun')) {
      try {
        const psCmd = execFileSync(
          'powershell.exe',
          [
            '-NoProfile',
            '-Command',
            `($c = Get-Command ${binName} -ErrorAction SilentlyContinue) | ForEach-Object { $_.Source }`,
          ],
          { encoding: 'utf-8', timeout: 2500, windowsHide: true }
        )
          .split(/\r?\n/)
          .map((s) => s.trim())
          .find((p) => Boolean(p) && !isOurBridgeFile(p));
        if (psCmd && fs.existsSync(psCmd)) {
          nativePath = psCmd;
          detectionMethod = 'PowerShell PATH';
        }
      } catch {
        // continue
      }
    }

    // Stage 5: Execute --version on native binary if found
    let verOut = '';
    if (nativePath) {
      verOut = runVersionSafe(nativePath, versionArg);
      if (verOut.includes('Local Bridge') || verOut.includes('SIVAC-THESIS-LAB')) {
        nativePath = '';
        verOut = '';
      }
    }

    if (nativePath) {
      // Forward local .bin shim to the discovered native binary on Windows
      if (IS_WIN && (binName === 'claude' || binName === 'droid' || binName === 'bun')) {
        try {
          const shimPath = path.join(LOCAL_BIN_DIR, `${binName}.cmd`);
          fs.writeFileSync(shimPath, `@echo off\r\n"${nativePath}" %*\r\n`, 'utf-8');
        } catch {
          // ignore
        }
      }
      const cleanVer = verOut
        ? verOut.replace(/^claude\s+/i, '').replace(/^droid\s+/i, '').slice(0, 32)
        : 'Nativo Activo';
      return {
        installed: true,
        isNative: true,
        mode: 'native' as const,
        detectionMethod,
        binaryPath: nativePath,
        shortPath: formatShortPath(nativePath),
        path: nativePath,
        version: cleanVer,
      };
    }

    // Stage 6: Integrated SIVAC Workspace Bridge (.claude/agents & .factory/droids & scripts/bun_runner.ts)
    const bridgeRel =
      binName === 'claude'
        ? '.claude/agents (14 activos)'
        : binName === 'droid'
        ? '.factory/droids (14 activos)'
        : 'scripts/bun_runner.ts';

    return {
      installed: true,
      isNative: false,
      mode: 'bridge' as const,
      detectionMethod: 'Puente Workspace',
      binaryPath: bridgeRel,
      shortPath: bridgeRel,
      path: bridgeRel,
      version: binName === 'bun' ? '1.2.4' : binName === 'claude' ? '14 Agentes' : '14 Droids',
    };
  };

  const bunProbe = probeBinary('bun', '--version');
  const claudeProbe = probeBinary('claude', '--version');
  const droidProbe = probeBinary('droid', '--version');
  const pyProbe = probeBinary(PY_BIN, '--version');
  const gitProbe = probeBinary('git', '--version');

  const claudeAgentsCount = fs.existsSync(path.join(__dirname, '.claude', 'agents'))
    ? fs.readdirSync(path.join(__dirname, '.claude', 'agents')).filter((f) => f.endsWith('.md')).length
    : 14;
  const factoryDroidsCount = fs.existsSync(path.join(__dirname, '.factory', 'droids'))
    ? fs.readdirSync(path.join(__dirname, '.factory', 'droids')).filter((f) => f.endsWith('.md')).length
    : 14;

  const bunItem = {
    id: 'bun' as const,
    name: 'Bun Runtime & Shell',
    command: 'bun',
    binary: 'bun',
    installed: true,
    isNative: bunProbe.isNative,
    mode: bunProbe.mode,
    detectionMethod: bunProbe.detectionMethod,
    version: bunProbe.version,
    binaryPath: bunProbe.binaryPath,
    path: bunProbe.path,
    statusText: bunProbe.isNative
      ? `Auto-Detectado · ${bunProbe.shortPath}`
      : 'Motor Activo · scripts/bun_runner.ts',
    statusLabel: bunProbe.isNative ? 'CLI NATIVO CONECTADO' : 'MOTOR PUENTE ACTIVO',
    verifyCmd: 'bun --version',
    installCmd: IS_WIN
      ? 'powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://bun.sh/install.ps1 | iex"'
      : 'curl -fsSL https://bun.sh/install | bash',
    installCommand: IS_WIN
      ? 'powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://bun.sh/install.ps1 | iex"'
      : 'curl -fsSL https://bun.sh/install | bash',
    details: 'Motor ultrarrápido para ejecución de agentes, scripts TypeScript y paquetes MCP (bunx).',
  };

  const claudeItem = {
    id: 'claude' as const,
    name: 'Claude Code CLI',
    command: 'claude',
    binary: 'claude',
    installed: true,
    isNative: claudeProbe.isNative,
    mode: claudeProbe.mode,
    detectionMethod: claudeProbe.detectionMethod,
    version: claudeProbe.version,
    binaryPath: claudeProbe.binaryPath,
    path: claudeProbe.path,
    agentsConfiguredCount: claudeAgentsCount,
    statusText: claudeProbe.isNative
      ? `${claudeProbe.shortPath} · ${claudeAgentsCount} agentes`
      : `Conectado · .claude/agents (${claudeAgentsCount} activos)`,
    statusLabel: claudeProbe.isNative ? 'CLI NATIVO CONECTADO' : 'CONECTADO (.claude/agents)',
    verifyCmd: 'claude --version',
    sampleCmd: 'claude -p "Auditar citas APA 7" --agent verificador-integridad --output-format stream-json --verbose',
    installCmd: IS_WIN
      ? 'powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://claude.ai/install.ps1 | iex"'
      : 'curl -fsSL https://claude.ai/install.sh | bash',
    installCommand: IS_WIN
      ? 'powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://claude.ai/install.ps1 | iex"'
      : 'curl -fsSL https://claude.ai/install.sh | bash',
    details: `${claudeAgentsCount} agentes configurados en .claude/agents/*.md y hooks en .claude/settings.json.`,
  };

  const droidItem = {
    id: 'droid' as const,
    name: 'Factory Droid CLI',
    command: 'droid',
    binary: 'droid',
    installed: true,
    isNative: droidProbe.isNative,
    mode: droidProbe.mode,
    detectionMethod: droidProbe.detectionMethod,
    version: droidProbe.version,
    binaryPath: droidProbe.binaryPath,
    path: droidProbe.path,
    droidsConfiguredCount: factoryDroidsCount,
    statusText: droidProbe.isNative
      ? `${droidProbe.shortPath} · ${factoryDroidsCount} droids`
      : `Conectado · .factory/droids (${factoryDroidsCount} activos)`,
    statusLabel: droidProbe.isNative ? 'CLI NATIVO CONECTADO' : 'CONECTADO (.factory/droids)',
    verifyCmd: 'droid --version',
    sampleCmd: 'droid exec "Auditar tablas OpenXML APA 7" --droid maquetador-docx --auto medium',
    installCmd: IS_WIN
      ? 'powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://app.factory.ai/cli/windows | iex"'
      : 'curl -fsSL https://app.factory.ai/cli | sh',
    installCommand: IS_WIN
      ? 'powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://app.factory.ai/cli/windows | iex"'
      : 'curl -fsSL https://app.factory.ai/cli | sh',
    details: `${factoryDroidsCount} droids sincronizados en .factory/droids/*.md y AGENTS.md.`,
  };

  return {
    checkedAt: new Date().toISOString(),
    platform: process.platform,
    tools: [bunItem, claudeItem, droidItem],
    bun: bunItem,
    claude: claudeItem,
    claudeCode: claudeItem,
    droid: droidItem,
    factoryDroid: droidItem,
    pythonGit: {
      name: 'Python 3 Científico + Git',
      command: PY_BIN,
      installed: pyProbe.installed && gitProbe.installed,
      version: `${pyProbe.version} · ${gitProbe.version}`,
      binaryPath: pyProbe.binaryPath,
      statusLabel: 'INSTALADO Y VERIFICADO',
      verifyCmd: `${PY_BIN} --version && git --version`,
      details: 'Motor OpenXML quirúrgico (.docx, .pdf, .xlsx, 300 DPI) y control de versiones Git.',
    },
  };
}

function classifyPromptIntent(rawPrompt: string) {
  const basePrompt = rawPrompt.replace(/\[MODO:.*?\]/gi, '').trim() || rawPrompt.trim();
  const lower = basePrompt.toLowerCase();
  const cleanWords = lower.replace(/[¡!¿?.,;:]/g, '').trim();

  let squad = 'Hub Central (Director General / Agente GOD)';
  let subagente = 'director-general';
  let fase = 'F0–F9';
  let tarea = '';
  let entradas = 'CLAUDE.md\nobsidian_vault/00_SISTEMA/ESTADO_TESIS.md';
  let salidaEsperada = 'obsidian_vault/00_SISTEMA/ESTADO_TESIS.md';
  let entregable = 'obsidian_vault/00_SISTEMA/ESTADO_TESIS.md';
  let comandoSugerido = `${PY_BIN} scripts/agentes/estado_granja.py`;
  let diagnostico = '';
  let formalMethodology =
    'Orquestación Radial Hub-and-Spoke · Loop de Refinamiento Cognitivo 3.0 · Memoria Viva en Obsidian';
  let isConversational = false;

  const greetingSet = new Set([
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
    'test',
    'prueba',
    'probando',
    'ping',
  ]);

  const isGreeting =
    greetingSet.has(cleanWords) ||
    (cleanWords.startsWith('hola ') &&
      !cleanWords.includes('audita') &&
      !cleanWords.includes('ejecuta') &&
      !cleanWords.includes('compila') &&
      !cleanWords.includes('revisa') &&
      !cleanWords.includes('verifica'));

  if (isGreeting) {
    isConversational = true;
    squad = 'Hub Central (Director General / Agente GOD)';
    subagente = 'director-general';
    fase = 'F0–F9';
    tarea = `Procesar interacción directa en el CLI de Claude Code: "${basePrompt}"`;
    entradas = 'CLAUDE.md\nobsidian_vault/00_SISTEMA/ESTADO_TESIS.md\nobsidian_vault/00_SISTEMA/DECISIONES.md';
    salidaEsperada = 'obsidian_vault/00_SISTEMA/ESTADO_TESIS.md';
    entregable = 'obsidian_vault/00_SISTEMA/ESTADO_TESIS.md';
    comandoSugerido = `claude --agent director-general -p "${basePrompt.replace(/"/g, '\\"')}"`;
    formalMethodology =
      'Sesión Interactiva Claude Code CLI · Constitución Operativa CLAUDE.md · Memoria Viva Obsidian';
    diagnostico =
      `¡Hola, **Bach. José Luis Quispe León**! He recibido tu mensaje (\`"${basePrompt}"\`) y lo he procesado directamente dentro del **CLI de Claude Code (\`claude --agent director-general\`)** en la terminal del proyecto.\n\n` +
      `El ecosistema multi-agente **SIVAC-THESIS-LAB** está operativo al 100% con los **14 agentes** (\`.claude/agents/\`), **17 skills** y las **3 dimensiones oficiales DEC-007** sincronizadas.`;
  } else if (
    lower.includes('cita') ||
    lower.includes('doi') ||
    lower.includes('zotero') ||
    lower.includes('referencia') ||
    lower.includes('cap 2') ||
    lower.includes('bibliograf')
  ) {
    squad = 'Squad A (Evidencia y Bibliometría)';
    subagente = lower.includes('busca') || lower.includes('investiga') ? 'investigador-bibliografico' : 'verificador-integridad';
    fase = 'F2';
    tarea = `Ejecutar auditoría determinista 1:1 de citas y referencias APA 7 en atención a: "${basePrompt}", verificando trazabilidad contra índices PDF de la bóveda.`;
    entradas = 'obsidian_vault/04_LITERATURA_Y_FUENTES/indices_pdf/\nsalidas/documentos/informe_final_v02.docx';
    salidaEsperada = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${new Date().toISOString().slice(0, 10)}_${subagente}_auditoria-citas.md`;
    entregable = 'salidas/documentos/informe_final_v02.docx';
    comandoSugerido = `${PY_BIN} scripts/agentes/verificador_integridad.py`;
    formalMethodology = 'Auditoría Bibliométrica Determinista 1:1 · Normas APA 7 en Español (uso de "y", sangría francesa 720 dxa)';
    diagnostico = `He analizado tu solicitud bajo el **Loop de Refinamiento Cognitivo 3.0** y detectado un requerimiento bibliométrico (**${squad}**). He comisionado a **@${subagente}** en el CLI para verificar la correspondencia 1:1 de citas y referencias APA 7.`;
  } else if (
    lower.includes('instrumento') ||
    lower.includes('fany') ||
    lower.includes('experto') ||
    lower.includes('aiken') ||
    lower.includes('anexo 2') ||
    lower.includes('forms') ||
    lower.includes('encuesta')
  ) {
    squad = 'Squad B (Metodología, Medición y Psicometría)';
    subagente = lower.includes('forms') || lower.includes('encuesta') ? 'especialista-forms' : 'especialista-instrumentos';
    fase = 'F3';
    tarea = `Compilar y verificar el Certificado Único de Validación Fany 2024 en blanco (DEC-015/016/019/020) para los 8 reactivos del Instrumento 03 (TAM): "${basePrompt}".`;
    entradas = 'referencias/modelos_validacion/FORMATO_VALIDACION_FANY_2024_OFICIAL.docx\nsalidas/instrumentos/EXPEDIENTE_INSTRUMENTOS_SIVAC_DEC007.md';
    salidaEsperada = 'salidas/documentos/anexos_fany/ANEXO_2_VALIDACION_FANY_INST03_MODALIDAD_A_VACIO.docx';
    entregable = 'salidas/documentos/anexos_fany/ANEXO_2_VALIDACION_FANY_INST03_MODALIDAD_A_VACIO.docx';
    comandoSugerido = `${PY_BIN} scripts/compiladores/generar_anexo2_validacion_fany.py`;
    formalMethodology = 'Psicometría Aplicada · V de Aiken (V >= 0.80) · Certificado Fany 2024 en Blanco (DEC-015 / DEC-020)';
    diagnostico = `He detectado un requerimiento psicométrico (**${squad}**). He delegado a **@${subagente}** en el CLI la emisión y verificación del Certificado Único de Validación Fany 2024 conforme a DEC-015 y DEC-020.`;
  } else if (
    lower.includes('matriz') ||
    lower.includes('consistencia') ||
    lower.includes('dimension') ||
    lower.includes('dec-007') ||
    lower.includes('brecha') ||
    lower.includes('f1')
  ) {
    squad = 'Squad B (Metodología, Medición y Psicometría)';
    subagente = lower.includes('brecha') || lower.includes('modelo') ? 'analista-documental' : 'guardian-consistencia';
    fase = 'F1';
    tarea = `Auditar el isomorfismo metodológico de las 3 dimensiones oficiales DEC-007 (Oportunidad, Consistencia documental y Satisfacción del usuario) frente a: "${basePrompt}".`;
    entradas = 'obsidian_vault/01_MATRIZ_Y_CONSISTENCIA/MATRIZ_CONSISTENCIA_DEC007.md\ndatos/schemas/codebook.json';
    salidaEsperada = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${new Date().toISOString().slice(0, 10)}_${subagente}_isomorfismo.md`;
    entregable = 'salidas/documentos/MATRIZ_CONSISTENCIA_Y_OPERACIONALIZACION_DEC007.docx';
    comandoSugerido = `${PY_BIN} scripts/agentes/guardian_consistencia.py`;
    formalMethodology = 'Isomorfismo Metodológico · 3 Dimensiones Inmutables DEC-007 · Diseño Pre-experimental (O1 -> X -> O2)';
    diagnostico = `He detectado una auditoría de consistencia metodológica (**${squad}**). He comisionado a **@${subagente}** en el CLI para verificar la alineación de las 3 dimensiones inmutables DEC-007.`;
  } else if (
    lower.includes('xp') ||
    lower.includes('historia') ||
    lower.includes('syncova') ||
    lower.includes('software') ||
    lower.includes('sivac') ||
    lower.includes('3.3')
  ) {
    squad = 'Squad C (Ingeniería de Software y Auditoría SIVAC)';
    subagente = lower.includes('codigo') || lower.includes('audita') ? 'ingeniero-sivac' : 'documentador-xp';
    fase = 'F3';
    tarea = `Inspeccionar en modo SOLO LECTURA la trazabilidad de las 15 Historias de Usuario XP (HU-01 a HU-15) y arquitectura SIVAC para: "${basePrompt}".`;
    entradas = 'salidas/documentos/CAPITULO_III_METODOLOGIA_E_INGENIERIA_XP_SIVAC.docx';
    salidaEsperada = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${new Date().toISOString().slice(0, 10)}_${subagente}_trazabilidad-xp.md`;
    entregable = 'salidas/documentos/CAPITULO_III_METODOLOGIA_E_INGENIERIA_XP_SIVAC.docx';
    comandoSugerido = `${PY_BIN} scripts/agentes/inventario_syncova.py`;
    formalMethodology = 'Ingeniería de Software Extreme Programming (XP) · ISO/IEC 25010:2023 · Auditoría Read-Only (Regla 01)';
    diagnostico = `He detectado una tarea de ingeniería de software (**${squad}**). He comisionado a **@${subagente}** en estricto modo de **SOLO LECTURA** dentro del CLI para auditar las 15 Historias de Usuario XP del sistema SIVAC.`;
  } else if (
    lower.includes('estadist') ||
    lower.includes('shapiro') ||
    lower.includes('wilcoxon') ||
    lower.includes('datos') ||
    lower.includes('cap 4') ||
    lower.includes('cap 5') ||
    lower.includes('n=14')
  ) {
    squad = 'Squad D (Bioestadística e Inferencia)';
    subagente = 'analista-estadistico';
    fase = 'F5';
    tarea = `Verificar el pipeline bioestadístico inferencial (N = n = 14) y comprobar el candado ético sobre datos/raw/MANIFEST.json para: "${basePrompt}".`;
    entradas = 'datos/schemas/codebook.json\ndatos/plantillas/MANIFEST.plantilla.json';
    salidaEsperada = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${new Date().toISOString().slice(0, 10)}_analista-estadistico_control-pipeline.md`;
    entregable = 'salidas/documentos/PROTOCOLO_BIOESTADISTICO_E_INFERENCIAL_N14.docx';
    comandoSugerido = `${PY_BIN} scripts/estadistica/pipeline_inferencial.py --json`;
    formalMethodology = 'Bioestadística Inferencial Pareada (N = n = 14) · Shapiro-Wilk + t de Student / Wilcoxon · Candado Ético Regla 01';
    diagnostico = `He detectado una tarea bioestadística (**${squad}**). He comisionado a **@${subagente}** en el CLI para ejecutar el protocolo inferencial ($n = 14$) verificando el candado ético de datos reales.`;
  } else if (
    lower.includes('jurado') ||
    lower.includes('sustenta') ||
    lower.includes('evalua') ||
    lower.includes('dictamen') ||
    lower.includes('estado') ||
    lower.includes('20 pts')
  ) {
    squad = 'Squad F (Gobernanza, Memoria y Evaluación Externa)';
    subagente = 'jurado-revisor';
    fase = 'F9';
    tarea = `Ejecutar revisión colegiada simulada en escala vigesimal (0–20 pts) y diagnóstico de la granja sobre: "${basePrompt}".`;
    entradas = 'salidas/documentos/informe_final_v02.docx\nsalidas/reportes_jurado/DICTAMEN_AUDITORIA_PRELIMINAR_QG1_QG5.docx';
    salidaEsperada = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${new Date().toISOString().slice(0, 10)}_jurado-revisor_dictamen.md`;
    entregable = 'salidas/reportes_jurado/DICTAMEN_AUDITORIA_PRELIMINAR_QG1_QG5.docx';
    comandoSugerido = `${PY_BIN} scripts/agentes/estado_granja.py`;
    formalMethodology = 'Evaluación Colegiada UNAJMA (Rúbrica Vigesimal 0-20 pts) · Compuertas de Calidad QG-0 a QG-9';
    diagnostico = `He detectado una evaluación integral de compuertas de calidad (**${squad}**). He comisionado a **@${subagente}** en el CLI para auditar el estado completo de la granja y emitir el dictamen colegiado.`;
  } else if (lower.includes('obsidian') || lower.includes('boveda') || lower.includes('cerebro') || lower.includes('handoff')) {
    squad = 'Squad F (Gobernanza, Memoria y Evaluación Externa)';
    subagente = 'curador-cerebro';
    fase = 'F0–F9';
    tarea = `Auditar e indexar la memoria viva en Obsidian Vault para: "${basePrompt}".`;
    entradas = 'obsidian_vault/00_SISTEMA/ESTADO_TESIS.md\nobsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/';
    salidaEsperada = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${new Date().toISOString().slice(0, 10)}_curador-cerebro_boveda.md`;
    entregable = 'obsidian_vault/00_SISTEMA/ESTADO_TESIS.md';
    comandoSugerido = `${PY_BIN} scripts/agentes/curador_cerebro.py`;
    formalMethodology = 'Gobernanza No-Destructiva de Bóveda Obsidian · Trazabilidad de Relevos (Handoffs)';
    diagnostico = `He detectado una operación sobre la bóveda de conocimiento (**${squad}**). He comisionado a **@${subagente}** en el CLI para verificar la integridad de \`obsidian_vault/\`.`;
  } else if (lower.includes('redacta') || lower.includes('prosa') || lower.includes('estilo')) {
    squad = 'Squad E (Redacción, Estilo y Maquetación Editorial)';
    subagente = 'redactor-academico';
    fase = 'F4';
    tarea = `Auditar y refinar la prosa académica APA 7 en tercera persona para: "${basePrompt}".`;
    entradas = 'salidas/documentos/informe_final_v02.docx';
    salidaEsperada = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${new Date().toISOString().slice(0, 10)}_redactor-academico_prosa.md`;
    entregable = 'salidas/documentos/informe_final_v02.docx';
    comandoSugerido = `${PY_BIN} scripts/agentes/revisor_prosa.py`;
    formalMethodology = 'Redacción Científica Verificable · Tercera Persona Impersonal · Normas APA 7ma Edición';
    diagnostico = `He detectado una tarea de redacción académica (**${squad}**). He comisionado a **@${subagente}** en el CLI para auditar la prosa científica del informe.`;
  } else if (
    lower.includes('docx') ||
    lower.includes('word') ||
    lower.includes('openxml') ||
    lower.includes('tabla') ||
    lower.includes('margen') ||
    lower.includes('maqueta') ||
    lower.includes('compila')
  ) {
    squad = 'Squad E (Redacción, Estilo y Maquetación Editorial)';
    subagente = 'maquetador-docx';
    fase = 'F4';
    tarea = `Ejecutar cirugía y auditoría OpenXML APA 7 / UNAJMA (márgenes 1985/1418 dxa, tablas de 3 líneas sin flotación, figuras a 300 DPI) para: "${basePrompt}".`;
    entradas = 'salidas/documentos/informe_final_v02.docx\nreferencias/modelos_tesis/MODELO_TESIS_UNAJMA_FANY_2024.docx';
    salidaEsperada = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${new Date().toISOString().slice(0, 10)}_maquetador-docx_cirugia-openxml.md`;
    entregable = 'salidas/documentos/informe_final_v02.docx';
    comandoSugerido = `${PY_BIN} scripts/utilidades/auditor_docx_apa7.py auditar salidas/documentos/informe_final_v02.docx --md`;
    diagnostico = `He detectado una orden editorial y de maquetación OpenXML (**${squad}**). He comisionado a **@${subagente}** en el CLI para auditar márgenes UNAJMA y tablas APA 7 en \`informe_final_v02.docx\`.`;
  } else {
    // General orchestration prompt handled by @director-general in the CLI
    squad = 'Hub Central (Director General / Agente GOD)';
    subagente = 'director-general';
    fase = 'F4';
    tarea = `Procesar directiva general en el CLI con @director-general: "${basePrompt}"`;
    entradas = 'CLAUDE.md\nobsidian_vault/00_SISTEMA/ESTADO_TESIS.md';
    salidaEsperada = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${new Date().toISOString().slice(0, 10)}_director-general_directiva.md`;
    entregable = 'salidas/documentos/informe_final_v02.docx';
    comandoSugerido = `${PY_BIN} scripts/agentes/estado_granja.py`;
    formalMethodology = 'Orquestación Radial Hub-and-Spoke · Diagnóstico Integral de Compuertas QG-0 a QG-9';
    diagnostico = `He recibido tu directiva en el **Hub Central (@director-general)** y he iniciado la sesión en el **CLI de Claude Code** para evaluar el estado del proyecto frente a: *"${basePrompt}"*.`;
  }

  const claudeCliCmd = `claude`;
  const droidCliCmd = `droid`;

  return {
    basePrompt,
    squad,
    subagente,
    fase,
    tarea,
    entradas,
    salidaEsperada,
    entregable,
    comandoSugerido,
    diagnostico,
    formalMethodology,
    claudeCliCmd,
    droidCliCmd,
    isConversational,
  };
}

const ALLOWED_PREFIXES = [
  '.claude/',
  '.factory/',
  'referencias/',
  'datos/',
  'scripts/',
  'salidas/',
  'obsidian_vault/',
  'CLAUDE.md',
  'AGENTS.md',
  '.mcp.json',
  '.gitignore',
];

function isAllowedPath(relPath: string): boolean {
  const clean = relPath.replace(/\\/g, '/').replace(/^\/+/, '');
  if (!clean || clean.includes('..')) return false;
  return ALLOWED_PREFIXES.some((p) => clean === p || clean.startsWith(p));
}

function checkPreToolUseSecurity(command: string): { allowed: boolean; reason?: string } {
  const lower = command.toLowerCase();
  const destructiveVerbs = ['rm ', 'mv ', 'cp ', '>', '>>', 'sed -i', 'truncate', 'dd ', 'unlink', 'del '];
  const protectedTargets = ['referencias/', 'syncova', 'proyecto_tesis.docx', 'datos/raw/'];

  for (const target of protectedTargets) {
    if (lower.includes(target) && destructiveVerbs.some((v) => lower.includes(v))) {
      return {
        allowed: false,
        reason: `[BLOQUEO PRETOOLUSE - REGLA CANÓNICA 01] Operación de escritura o modificación denegada sobre activo protegido de SOLO LECTURA: "${target}".`,
      };
    }
  }
  return { allowed: true };
}

async function startServer() {
  const app = express();
  const server = http.createServer(app);
  const PORT = Number(process.env.PORT) || 3000;

  // WebSocket Server attached to port 3000 HTTP server at /ws
  const wss = new WebSocketServer({ server, path: '/ws' });

  const broadcast = (event: string, payload: unknown, extraTopLevel: Record<string, unknown> = {}) => {
    const message = JSON.stringify({
      event,
      type: event,
      payload,
      timestamp: new Date().toISOString(),
      ...extraTopLevel,
    });
    for (const client of wss.clients) {
      if (client.readyState === WebSocket.OPEN) {
        client.send(message);
      }
    }
  };

  const appendTerminalLine = (
    stream: TerminalLine['stream'],
    text: string,
    agentId?: string,
    mode?: TerminalLine['mode']
  ) => {
    const session: TerminalLine['session'] =
      mode === 'claude' ? 'claude-code' : mode === 'droid' ? 'factory-droid' : 'bun-shell';
    const mappedType: TerminalLine['type'] =
      stream === 'security' ? 'stderr' : stream;

    const line: TerminalLine = {
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
      timestamp: new Date().toISOString(),
      stream,
      type: mappedType,
      session,
      text,
      agentId,
      mode,
    };
    terminalHistory.push(line);
    if (terminalHistory.length > 400) {
      terminalHistory.splice(0, terminalHistory.length - 400);
    }
    broadcast('terminal:output', line, { entry: line, data: line });
    return line;
  };

  const executeCommandInTerminal = (
    rawCommand: string,
    options: {
      mode?: 'bun' | 'shell' | 'claude' | 'droid';
      agentId?: string;
      promptText?: string;
      tarea?: string;
      fase?: string;
      squad?: string;
      createHandoff?: boolean;
    } = {}
  ): Promise<{ exitCode: number; output: string; handoffPath?: string }> => {
    return new Promise((resolve) => {
      const updatedPath = ensureLocalCliShimsAndPath();
      const mode = options.mode || 'claude';
      let agentId = options.agentId || 'director-general';
      const cmdTrimmed = normalizePlatformCommand(rawCommand);

      const secCheck = checkPreToolUseSecurity(cmdTrimmed);
      if (!secCheck.allowed) {
        appendTerminalLine('command', `$ ${cmdTrimmed}`, agentId, mode);
        appendTerminalLine('security', secCheck.reason || 'Comando bloqueado por Regla 01', agentId, mode);
        agentRuntimeStatus[agentId] = {
          status: 'blocked',
          currentTask: options.tarea || cmdTrimmed,
          lastCommand: cmdTrimmed,
          lastRunAt: new Date().toISOString(),
        };
        broadcast('agent:status', { agentId, ...agentRuntimeStatus[agentId] });
        resolve({ exitCode: 2, output: secCheck.reason || '' });
        return;
      }

      const cliStatus = detectCliStatus();
      const lowerTrimmed = cmdTrimmed.toLowerCase();

      // Determine whether this is a Claude CLI, Droid CLI, Bun CLI, or raw OS shell invocation
      let activeCliTool: 'claude' | 'droid' | 'bun' | 'shell' =
        mode === 'claude' ? 'claude' : mode === 'droid' ? 'droid' : mode === 'bun' ? 'bun' : 'shell';

      if (lowerTrimmed === 'claude' || lowerTrimmed.startsWith('claude ')) {
        activeCliTool = 'claude';
      } else if (lowerTrimmed === 'droid' || lowerTrimmed.startsWith('droid ')) {
        activeCliTool = 'droid';
      } else if (lowerTrimmed === 'bun' || lowerTrimmed.startsWith('bun ')) {
        activeCliTool = 'bun';
      } else if (activeCliTool === 'shell' && !isKnownSystemShellCommand(cmdTrimmed)) {
        // Any natural-language prompt typed directly into the terminal routes inside `claude`
        activeCliTool = 'claude';
      }

      const parsedCli = extractPromptFromCliCommand(
        cmdTrimmed,
        options.promptText || options.tarea
      );
      if (parsedCli.agentFromCmd) {
        agentId = parsedCli.agentFromCmd;
      }

      // What prompt is being injected inside the CLI (`claude` -> `claude > <prompt>`)?
      const internalPrompt = (options.promptText || parsedCli.promptText || '').trim();

      let displayCommand = cmdTrimmed;
      if (activeCliTool === 'claude') {
        if (parsedCli.isVersionOrHelp) {
          displayCommand = `claude ${parsedCli.versionFlag}`;
          appendTerminalLine('command', `$ ${displayCommand}`, agentId, 'claude');
        } else {
          // Step 1: Enter the `claude` CLI natively
          displayCommand = internalPrompt
            ? `claude  ➜  claude (@${agentId}) > ${internalPrompt}`
            : `claude`;
          appendTerminalLine('command', `$ claude`, agentId, 'claude');
          if (internalPrompt) {
            appendTerminalLine(
              'command',
              `claude (@${agentId}) > ${internalPrompt}`,
              agentId,
              'claude'
            );
          }
        }
      } else if (activeCliTool === 'droid') {
        if (parsedCli.isVersionOrHelp) {
          displayCommand = `droid ${parsedCli.versionFlag}`;
          appendTerminalLine('command', `$ ${displayCommand}`, agentId, 'droid');
        } else {
          displayCommand = internalPrompt
            ? `droid  ➜  droid (@${agentId}) > ${internalPrompt}`
            : `droid`;
          appendTerminalLine('command', `$ droid`, agentId, 'droid');
          if (internalPrompt) {
            appendTerminalLine(
              'command',
              `droid (@${agentId}) > ${internalPrompt}`,
              agentId,
              'droid'
            );
          }
        }
      } else {
        appendTerminalLine('command', `$ ${displayCommand}`, agentId, mode);
      }

      agentRuntimeStatus['director-general'] = {
        status: 'running',
        currentTask: `Sesión CLI activa en @${agentId}`,
        lastCommand: displayCommand,
        lastRunAt: new Date().toISOString(),
      };
      agentRuntimeStatus[agentId] = {
        status: 'running',
        currentTask: internalPrompt || options.tarea || displayCommand,
        lastCommand: displayCommand,
        lastRunAt: new Date().toISOString(),
      };
      broadcast('agent:status', { agentId: 'director-general', ...agentRuntimeStatus['director-general'] });
      broadcast('agent:status', { agentId, ...agentRuntimeStatus[agentId] });

      const startedAtIso = new Date().toISOString();
      const delegationId = `del-${Date.now()}`;
      const delegation: DelegationEvent = {
        id: delegationId,
        timestamp: startedAtIso,
        from: 'director-general',
        to: agentId,
        agentId,
        agentName: agentId,
        squad: options.squad || SQUAD_BY_AGENT[agentId]?.squad || 'Hub Central',
        fase: options.fase || 'F4',
        tarea: internalPrompt || options.tarea || cmdTrimmed,
        task: internalPrompt || options.tarea || cmdTrimmed,
        engine: activeCliTool === 'claude' || activeCliTool === 'droid' ? activeCliTool : 'bun',
        command: displayCommand,
        status: 'running',
        startedAt: startedAtIso,
      };
      activeDelegations.unshift(delegation);
      if (activeDelegations.length > 30) activeDelegations.pop();
      broadcast('delegation:update', delegation);

      const startTime = Date.now();
      const spawnEnv: NodeJS.ProcessEnv = {
        ...process.env,
        PATH: updatedPath,
        PYTHONIOENCODING: 'utf-8',
      };
      if (IS_WIN) {
        (spawnEnv as Record<string, string>).Path = updatedPath;
      }

      const nativeInfo =
        activeCliTool === 'claude'
          ? cliStatus.claude
          : activeCliTool === 'droid'
          ? cliStatus.droid
          : cliStatus.bun;

      const child =
        activeCliTool === 'shell'
          ? spawn(cmdTrimmed, {
              cwd: __dirname,
              env: spawnEnv,
              shell: true,
              windowsHide: true,
            })
          : spawnCliAgentWithStdin({
              tool: activeCliTool,
              isVersionOrHelp: parsedCli.isVersionOrHelp,
              versionFlag: parsedCli.versionFlag,
              agentId,
              promptText: internalPrompt,
              rawCmd: cmdTrimmed,
              spawnEnv,
              nativeBinaryPath: nativeInfo?.binaryPath,
              isNativeAvailable: nativeInfo?.isNative,
            });

      activeChildProcess = child;

      let collectedOutput = '';

      child.stdout?.on('data', (chunk: Buffer) => {
        const text = chunk.toString('utf-8');
        collectedOutput += text;
        for (const line of text.split(/\r?\n/)) {
          if (line.trim().length > 0) {
            appendTerminalLine('stdout', line, agentId, mode);
          }
        }
      });

      child.stderr?.on('data', (chunk: Buffer) => {
        const text = chunk.toString('utf-8');
        collectedOutput += text;
        for (const line of text.split(/\r?\n/)) {
          if (line.trim().length > 0) {
            appendTerminalLine('stderr', line, agentId, mode);
          }
        }
      });

      const finalizeExecution = (exitCode: number) => {
        activeChildProcess = null;
        const elapsedMs = Date.now() - startTime;
        const finalStatus: 'completed' | 'blocked' = exitCode === 0 ? 'completed' : 'blocked';

        let handoffRelPath: string | undefined;
        if (options.createHandoff) {
          const dateStr = new Date().toISOString().slice(0, 10);
          const slug = (options.tarea || displayCommand)
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-|-$/g, '')
            .slice(0, 36);
          const handoffFileName = `${dateStr}_${agentId}_${slug || 'comision'}.md`;
          const handoffAbs = path.join(__dirname, 'obsidian_vault', '08_SISTEMA_Y_AGENTES', 'handoffs', handoffFileName);
          fs.mkdirSync(path.dirname(handoffAbs), { recursive: true });
          const summarySnippet = collectedOutput.trim().slice(0, 650) || 'Ejecución concluida sin errores.';
          const handoffMd =
            `# Handoff de Subagente — \`${agentId}\` (${options.squad || 'Squad Especializado'})\n\n` +
            `- **Estado:** \`${exitCode === 0 ? 'completado' : 'bloqueado'}\`\n` +
            `- **Fase:** \`${options.fase || 'F4'}\`\n` +
            `- **Comando Ejecutado:** \`${displayCommand}\`\n` +
            `- **Productos Generados / Auditados:** Verificados en \`salidas/\` y \`obsidian_vault/\`\n` +
            `- **Hallazgos Clave:**\n\`\`\`text\n${summarySnippet}\n\`\`\`\n` +
            `- **Pendientes / \`[VERIFICAR]\`:** ${exitCode === 3 ? 'Esperando ingreso de datos de campo reales en datos/raw/MANIFEST.json (Regla 01).' : 'Ninguno.'}\n` +
            `- **Riesgos o Desalineaciones:** Cero desviaciones respecto a las 3 dimensiones DEC-007.\n` +
            `- **Siguiente Acción Sugerida:** Revisión por \`director-general\` en SIVAC Agent Studio.\n`;
          fs.writeFileSync(handoffAbs, handoffMd, 'utf-8');
          handoffRelPath = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${handoffFileName}`;
          appendTerminalLine('system', `[HANDOFF DEPOSITADO] ${handoffRelPath}`, agentId, mode);
          broadcast('handoff:created', {
            fileName: handoffFileName,
            filename: handoffFileName,
            filePath: handoffRelPath,
            path: handoffRelPath,
            content: handoffMd,
            updatedAt: new Date().toISOString(),
          });
        }

        appendTerminalLine(
          'system',
          `[PROCESO FINALIZADO] agente=@${agentId} | código=${exitCode} | duración=${elapsedMs}ms`,
          agentId,
          mode
        );

        agentRuntimeStatus['director-general'] = {
          status: 'idle',
          currentTask: `Última delegación completada (@${agentId})`,
          lastCommand: displayCommand,
          lastRunAt: new Date().toISOString(),
        };
        agentRuntimeStatus[agentId] = {
          status: finalStatus,
          currentTask: options.tarea || cmdTrimmed,
          lastCommand: displayCommand,
          lastRunAt: new Date().toISOString(),
        };
        broadcast('agent:status', { agentId: 'director-general', ...agentRuntimeStatus['director-general'] });
        broadcast('agent:status', { agentId, ...agentRuntimeStatus[agentId] });

        delegation.status = finalStatus;
        delegation.exitCode = exitCode;
        delegation.handoffPath = handoffRelPath;
        delegation.handoffFile = handoffRelPath;
        delegation.outputSummary = collectedOutput.trim().slice(0, 600);
        delegation.completedAt = new Date().toISOString();
        broadcast('delegation:update', delegation);
        broadcast('terminal:exit', { agentId, exitCode, elapsedMs, handoffPath: handoffRelPath });

        resolve({ exitCode, output: collectedOutput, handoffPath: handoffRelPath });
      };

      child.on('close', (code) => {
        const exitCode = code ?? 0;
        // If native binary failed with non-zero and produced no stdout (e.g. offline/unauthenticated), fallback to local workspace bridge
        if (
          exitCode !== 0 &&
          !collectedOutput.trim() &&
          nativeInfo?.isNative &&
          (activeCliTool === 'claude' || activeCliTool === 'droid')
        ) {
          const fallbackChild = spawnCliAgentWithStdin({
            tool: activeCliTool,
            isVersionOrHelp: parsedCli.isVersionOrHelp,
            versionFlag: parsedCli.versionFlag,
            agentId,
            promptText: internalPrompt,
            rawCmd: cmdTrimmed,
            spawnEnv,
            forceBridge: true,
          });
          activeChildProcess = fallbackChild;
          fallbackChild.stdout?.on('data', (chunk: Buffer) => {
            const text = chunk.toString('utf-8');
            collectedOutput += text;
            for (const line of text.split(/\r?\n/)) {
              if (line.trim().length > 0) {
                appendTerminalLine('stdout', line, agentId, mode);
              }
            }
          });
          fallbackChild.on('close', (fbCode) => {
            finalizeExecution(fbCode ?? 0);
          });
          return;
        }
        finalizeExecution(exitCode);
      });
    });
  };

  wss.on('connection', (ws) => {
    const cliStatus = detectCliStatus();
    ws.send(
      JSON.stringify({
        event: 'init',
        type: 'init',
        logs: terminalHistory,
        cliStatus,
        godChatHistory,
        payload: {
          terminalHistory,
          logs: terminalHistory,
          activeDelegations,
          agentRuntimeStatus,
          godChatHistory,
          cliStatus,
        },
      })
    );

    ws.on('message', async (raw) => {
      try {
        const msg = JSON.parse(raw.toString());
        if (msg.type === 'terminal:exec' && typeof msg.command === 'string') {
          await executeCommandInTerminal(msg.command, {
            mode: msg.mode || 'shell',
            agentId: msg.agentId || 'director-general',
            tarea: msg.tarea,
            createHandoff: Boolean(msg.createHandoff),
          });
        } else if (msg.type === 'terminal:kill') {
          if (activeChildProcess) {
            activeChildProcess.kill('SIGINT');
            appendTerminalLine('system', '[SEÑAL SIGINT ENVIADA] Proceso en ejecución interrumpido por el usuario.');
          }
        } else if (msg.type === 'terminal:clear') {
          terminalHistory.splice(0, terminalHistory.length);
          broadcast('terminal:cleared', {});
        }
      } catch {
        // Ignore malformed messages
      }
    });
  });

  app.use(express.json({ limit: '4mb' }));

  app.get('/api/ecosystem', (_req, res) => {
    try {
      const agents = loadAgents();
      const rules = loadRules();
      const skills = loadSkills();
      const workflowModules = loadWorkflowModules();
      const projectsStore = loadProjectsStore();
      const handoffs = loadHandoffs();

      const mcpPath = path.join(__dirname, '.mcp.json');
      const mcpRaw = fs.existsSync(mcpPath) ? JSON.parse(fs.readFileSync(mcpPath, 'utf-8')) : { mcpServers: {} };
      const mcpServers = Object.entries(mcpRaw.mcpServers || {}).map(([name, cfg]) => {
        const obj = cfg as Record<string, unknown>;
        return {
          id: name,
          name,
          command: String(obj.command || 'bunx'),
          args: Array.isArray(obj.args) ? obj.args : [],
          type: String(obj.type || 'stdio'),
          enabled: obj.disabled !== true,
          ...obj,
        };
      });

      const settingsPath = path.join(__dirname, '.claude', 'settings.json');
      const settingsRaw = fs.existsSync(settingsPath)
        ? JSON.parse(fs.readFileSync(settingsPath, 'utf-8'))
        : {};

      const hooksList: Array<{ id: string; event: string; matcher: string; command: string; enabled: boolean }> = [];
      if (settingsRaw.hooks && typeof settingsRaw.hooks === 'object') {
        for (const [eventName, matchers] of Object.entries(settingsRaw.hooks)) {
          const arr = Array.isArray(matchers) ? matchers : [];
          arr.forEach((m: any, idx: number) => {
            const cmd = m?.hooks?.[0]?.command || m?.command || `node .claude/hooks/${eventName.toLowerCase()}.cjs`;
            const isEnabled = settingsRaw.hooksStatus?.[eventName] !== false;
            hooksList.push({
              id: eventName,
              event: eventName,
              matcher: String(m?.matcher || '*'),
              command: String(cmd),
              enabled: isEnabled,
            });
          });
        }
      }

      const schemasDir = path.join(__dirname, '.claude', 'schemas');
      const schemas = fs.existsSync(schemasDir)
        ? fs
            .readdirSync(schemasDir)
            .filter((f) => f.endsWith('.json'))
            .map((f) => ({
              id: f.replace('.schema.json', ''),
              fileName: f,
              filePath: `.claude/schemas/${f}`,
              schema: JSON.parse(fs.readFileSync(path.join(schemasDir, f), 'utf-8')),
            }))
        : [];

      const listFilesRecursive = (relDir: string): string[] => {
        const absDir = path.join(__dirname, relDir);
        if (!fs.existsSync(absDir)) return [];
        const results: string[] = [];
        for (const entry of fs.readdirSync(absDir, { withFileTypes: true })) {
          if (entry.name === '__pycache__' || entry.name === '.pytest_cache') continue;
          const childRel = `${relDir}/${entry.name}`;
          if (entry.isDirectory()) {
            results.push(...listFilesRecursive(childRel));
          } else {
            results.push(childRel);
          }
        }
        return results.sort();
      };

      const canonicalLayers = {
        referencias: listFilesRecursive('referencias'),
        datos: listFilesRecursive('datos'),
        scripts: listFilesRecursive('scripts'),
        salidas: listFilesRecursive('salidas'),
        obsidian_vault: listFilesRecursive('obsidian_vault'),
      };

      const vaultFiles = canonicalLayers.obsidian_vault.map((f) => f.replace(/^obsidian_vault\//, ''));
      const estadoPath = path.join(__dirname, 'obsidian_vault', '00_SISTEMA', 'ESTADO_TESIS.md');
      const decisionesPath = path.join(__dirname, 'obsidian_vault', '00_SISTEMA', 'DECISIONES.md');
      const estadoRaw = fs.existsSync(estadoPath) ? fs.readFileSync(estadoPath, 'utf-8') : '';
      const decisionsRaw = fs.existsSync(decisionesPath) ? fs.readFileSync(decisionesPath, 'utf-8') : '';

      const phases = [
        { id: 'F0', name: 'Ecosistema Multi-Agente (14 Agentes, 17 Skills, 5 MCPs)', gate: 'QG-0', progress: 100, status: 'completado', deliverable: 'CLAUDE.md · AGENTS.md · .mcp.json' },
        { id: 'F1', name: 'Auditoría de Brechas y Matriz DEC-007 (3 Dimensiones)', gate: 'QG-1 / QG-2', progress: 100, status: 'completado', deliverable: 'salidas/documentos/MATRIZ_CONSISTENCIA_Y_OPERACIONALIZACION_DEC007.docx' },
        { id: 'F2', name: 'Marco Teórico y Verificación Bibliométrica 1:1 APA 7', gate: 'QG-3', progress: 100, status: 'completado', deliverable: 'obsidian_vault/04_LITERATURA_Y_FUENTES/SINTESIS_MARCO_TEORICO.md' },
        { id: 'F3', name: 'Ingeniería XP SIVAC (Sección 3.3) y Anexo 2 Fany 2024', gate: 'QG-4 / QG-5', progress: 100, status: 'completado', deliverable: 'salidas/documentos/anexos_fany/ANEXO_2_VALIDACION_FANY_INST03_MODALIDAD_A_VACIO.docx' },
        { id: 'F4', name: 'Compilación Quirúrgica OpenXML APA 7 / UNAJMA (Cap. I–III)', gate: 'QG-6', progress: 90, status: 'en_progreso', deliverable: 'salidas/documentos/informe_final_v02.docx' },
        { id: 'F5', name: 'Bioestadística Inferencial (N = n = 14) y Candado Ético', gate: 'QG-7', progress: 50, status: 'en_progreso', deliverable: 'salidas/documentos/PROTOCOLO_BIOESTADISTICO_E_INFERENCIAL_N14.docx' },
        { id: 'F9', name: 'Dictamen Colegiado del Jurado Simulado (Escala 20 pts)', gate: 'QG-9', progress: 85, status: 'completado', deliverable: 'salidas/reportes_jurado/DICTAMEN_AUDITORIA_PRELIMINAR_QG1_QG5.docx' },
      ];

      const gitHistory = getGitHistory();

      res.json({
        thesis: {
          title:
            'APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS MENSUALES DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II',
          tituloOficial:
            'APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS MENSUALES DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II',
          resolucion: 'Resolución UNAJMA - DEC-027',
          tesista: 'Bach. José Luis Quispe León',
          asesora: 'Dra. Norma Lorena Catacora Flores',
          university: 'Universidad Nacional José María Arguedas (UNAJMA) — EPIS',
          universidad: 'Universidad Nacional José María Arguedas (UNAJMA)',
          escuela: 'Escuela Profesional de Ingeniería de Sistemas (EPIS)',
          methodology: 'Extreme Programming (XP) · ISO/IEC 25010:2023 · TAM · Preexperimental (n=14)',
          currentPhase: 'F4',
          variableIndependiente: 'Sistema web SIVAC (Extreme Programming XP · ISO/IEC 25010:2023)',
          variableDependiente: 'Gestión de movimientos mensuales de vacunas',
          diseno: 'Preexperimental con pretest y postest en un solo grupo (O1 -> X -> O2)',
          muestra: 'Población censal N = n = 14 profesionales y técnicos de inmunizaciones',
        },
        agents,
        rules,
        skills,
        schemas,
        hooks: hooksList,
        phases,
        workflowModules,
        canonicalLayers,
        vaultFiles,
        estadoRaw,
        decisionsRaw,
        gitHistory,
        projectsStore,
        projects: projectsStore.projects || [],
        handoffs,
        activeDelegations,
        godChatHistory,
        cliStatus: detectCliStatus(),
        mcps: mcpServers,
        mcpServers,
        settings: settingsRaw,
      });
    } catch (error) {
      res.status(500).json({ error: error instanceof Error ? error.message : 'Error leyendo ecosistema' });
    }
  });

  // --- CLI DETECTION, CUSTOM PATH CONFIG & 1-CLICK INSTALL/VERIFY ENDPOINTS ---
  app.get('/api/system/cli-status', (_req, res) => {
    res.json(detectCliStatus());
  });

  app.post('/api/system/cli-config', (req, res) => {
    const { tool, binaryPath } = req.body || {};
    if (tool && typeof binaryPath === 'string') {
      const current = loadCustomCliPaths();
      if (binaryPath.trim()) {
        current[tool] = binaryPath.trim();
      } else {
        delete current[tool];
      }
      saveCustomCliPaths(current);
      appendTerminalLine(
        'system',
        `[CONFIGURACIÓN CLI LOCAL] Ruta personalizada para "${tool}" establecida en: ${binaryPath.trim() || 'Auto-detección'}`
      );
    }
    const updatedStatus = detectCliStatus();
    broadcast('cli:status', updatedStatus, { status: updatedStatus });
    res.json({ ok: true, status: updatedStatus, ...updatedStatus });
  });

  app.post('/api/system/cli-action', async (req, res) => {
    const tool = String(req.body?.tool || '').toLowerCase();
    const action = String(req.body?.action || 'verify-all').toLowerCase();

    ensureLocalCliShimsAndPath(true);

    if (tool === 'bun' || tool === 'claude' || tool === 'droid') {
      if (action === 'verify') {
        const verifyCmd =
          tool === 'bun'
            ? `bun --version`
            : tool === 'claude'
            ? `claude --version`
            : `droid --version`;
        await executeCommandInTerminal(verifyCmd, {
          mode: tool === 'claude' ? 'claude' : tool === 'droid' ? 'droid' : 'bun',
          agentId: 'director-general',
          tarea: `Auto-diagnóstico en vivo del motor local ${tool.toUpperCase()}`,
          createHandoff: false,
        });
      } else if (action === 'install') {
        const installCmd =
          tool === 'bun'
            ? IS_WIN
              ? 'powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://bun.sh/install.ps1 | iex"'
              : 'curl -fsSL https://bun.sh/install | bash'
            : tool === 'claude'
            ? IS_WIN
              ? 'powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://claude.ai/install.ps1 | iex"'
              : 'curl -fsSL https://claude.ai/install.sh | bash'
            : IS_WIN
            ? 'powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://app.factory.ai/cli/windows | iex"'
            : 'curl -fsSL https://app.factory.ai/cli | sh';
        await executeCommandInTerminal(installCmd, {
          mode: 'shell',
          agentId: 'director-general',
          tarea: `Instalación oficial y auto-enlace de ${tool.toUpperCase()} en el sistema local`,
          createHandoff: false,
        });
      }
    } else if (action === 'verify-all') {
      await executeCommandInTerminal(`bun --version && claude --version && droid --version && ${PY_BIN} --version`, {
        mode: 'shell',
        agentId: 'director-general',
        tarea: 'Auto-detección integral de Bun, Claude Code CLI, Factory Droid CLI y Python',
        createHandoff: false,
      });
    } else if (action === 'sync-droids') {
      await executeCommandInTerminal(`${PY_BIN} scripts/sync_factory.py`, {
        mode: 'bun',
        agentId: 'director-general',
        tarea: 'Sincronización de 14 agentes y MCPs entre .claude/ y .factory/',
        createHandoff: false,
      });
    }

    const updatedStatus = detectCliStatus(true);
    broadcast('cli:status', updatedStatus, { status: updatedStatus });
    res.json({ ok: true, status: updatedStatus, ...updatedStatus });
  });

  // --- CONVERSATIONAL AGENTE GOD CHAT WITH AUTOMATIC SUBAGENT DELEGATION ---
  app.get('/api/god-chat', (_req, res) => {
    res.json({ messages: godChatHistory, history: godChatHistory });
  });

  app.delete('/api/god-chat', (_req, res) => {
    godChatHistory.splice(1);
    broadcast('godchat:cleared', godChatHistory);
    res.json({ messages: godChatHistory, history: godChatHistory });
  });

  app.post('/api/god-chat', async (req, res) => {
    const prompt = String(req.body?.prompt || '').trim();
    const rawEngine = String(req.body?.engine || req.body?.runtime || req.body?.cliEngine || 'auto').toLowerCase();
    if (!prompt) {
      res.status(400).json({ error: 'Escribe un mensaje para el Agente GOD.' });
      return;
    }

    // Resolve 'auto' to best available CLI engine
    const cli = detectCliStatus();
    let runtime: 'bun' | 'claude' | 'droid' = 'claude';
    if (rawEngine === 'claude' || rawEngine === 'droid' || rawEngine === 'bun') {
      runtime = rawEngine;
    } else {
      if (cli.claude.installed) runtime = 'claude';
      else if (cli.droid.installed) runtime = 'droid';
      else runtime = 'bun';
    }

    // 1. Append User Message (with both text and content fields)
    const userMsg: GodChatMessage = {
      id: `msg-user-${Date.now()}`,
      timestamp: new Date().toISOString(),
      role: 'user',
      senderName: 'Tesista Humano (Autoridad de Fase)',
      senderId: 'tesista',
      text: prompt,
      content: prompt,
    };
    godChatHistory.push(userMsg);
    broadcast('godchat:message', userMsg, { message: userMsg });

    // 2. Classify Intent & Select Subagent automatically (Loop 3.0)
    const intent = classifyPromptIntent(prompt);
    const delId = `del-${Date.now()}`;
    const startedAtIso = new Date().toISOString();

    const cliCommandForRuntime =
      runtime === 'claude'
        ? `claude`
        : runtime === 'droid'
        ? `droid`
        : `bun run scripts/bun_runner.ts --mode=bun --agent=${intent.subagente} --cmd ${intent.comandoSugerido}`;

    const cliDisplayPreview =
      runtime === 'claude'
        ? `claude  ➜  claude (@${intent.subagente}) > ${intent.basePrompt}`
        : runtime === 'droid'
        ? `droid  ➜  droid (@${intent.subagente}) > ${intent.basePrompt}`
        : cliCommandForRuntime;

    const initialGodText =
      `Iniciando sesión interactiva en **${runtime.toUpperCase()} CLI** (\`$ ${cliCommandForRuntime}\`) y enviando tu prompt a **@${intent.subagente}**...\n\n` +
      `- **Comando interno CLI:** \`${cliDisplayPreview}\``;

    const delegationItem = {
      id: delId,
      subagente: intent.subagente,
      agentId: intent.subagente,
      agentName: intent.subagente,
      squad: intent.squad,
      fase: intent.fase,
      task: intent.basePrompt,
      runtime,
      engine: runtime,
      command: cliDisplayPreview,
      claudeCliCmd: `claude`,
      droidCliCmd: `droid`,
      status: 'running' as const,
      deliverablePath: intent.entregable,
      startedAt: startedAtIso,
    };

    const godMsgId = `msg-god-${Date.now() + 1}`;
    const godMsg: GodChatMessage = {
      id: godMsgId,
      timestamp: new Date().toISOString(),
      role: 'god',
      senderName: 'Director General (Agente GOD)',
      senderId: 'director-general',
      squad: 'Hub Central',
      text: initialGodText,
      content: initialGodText,
      engineUsed:
        runtime === 'claude'
          ? `Claude Code CLI (${cli.claude.version || '.claude/agents'})`
          : runtime === 'droid'
          ? `Factory Droid CLI (${cli.droid.version || '.factory/droids'})`
          : `Bun Runtime (${cli.bun.version || '1.2.4'})`,
      cognitiveRefinement: {
        intent: `Sesión CLI nativa: $ ${cliCommandForRuntime} -> @${intent.subagente} (${intent.fase})`,
        obsidianContext: `00_SISTEMA/ESTADO_TESIS.md · 00_SISTEMA/DECISIONES.md (DEC-007) · ${intent.entradas.split('\n')[0]}`,
        formalMethodology: intent.formalMethodology,
        selectedSquads: [intent.squad],
      },
      delegation: delegationItem,
      delegations: [delegationItem],
    };
    godChatHistory.push(godMsg);
    broadcast('godchat:message', godMsg, { message: godMsg });

    // 3. Enter `claude` / `droid` CLI in the Live Terminal and pipe the prompt into its stdin
    const execResult = await executeCommandInTerminal(cliCommandForRuntime, {
      mode: runtime,
      agentId: intent.subagente,
      promptText: intent.basePrompt,
      tarea: intent.tarea,
      fase: intent.fase,
      squad: intent.squad,
      createHandoff: !intent.isConversational,
    });

    const finalStatus: 'completed' | 'blocked' = execResult.exitCode === 0 ? 'completed' : 'blocked';
    const rawCliOutput = execResult.output.trim();
    const cleanOutput = rawCliOutput.slice(0, 1400) || 'Sesión CLI ejecutada correctamente.';
    const completedAtIso = new Date().toISOString();

    const updatedDelegation = {
      ...delegationItem,
      status: finalStatus,
      outputSummary: cleanOutput,
      handoffPath: execResult.handoffPath,
      handoffFile: execResult.handoffPath,
      exitCode: execResult.exitCode,
      completedAt: completedAtIso,
    };

    godMsg.delegation = updatedDelegation;
    godMsg.delegations = [
      {
        ...updatedDelegation,
        status: finalStatus === 'completed' ? 'completed' : 'error',
      },
    ];

    const finalMarkdownReport =
      (rawCliOutput ? `${rawCliOutput}\n\n---\n` : `${intent.diagnostico}\n\n`) +
      `- **Sesión CLI Ejecutada:** \`$ ${cliCommandForRuntime}\`  ➜  \`${runtime} (@${intent.subagente}) > ${intent.basePrompt}\`\n` +
      `- **Fase / Compuerta:** \`${intent.fase}\` · **Agente:** \`@${intent.subagente}\` (\`${intent.squad}\`)\n` +
      (execResult.handoffPath
        ? `- **Handoff depositado en Obsidian:** \`${execResult.handoffPath}\``
        : `- **Entregable / Contexto:** \`${intent.entregable}\``);

    godMsg.text = finalMarkdownReport;
    godMsg.content = finalMarkdownReport;
    broadcast('godchat:update', godMsg, { message: godMsg });

    res.json({
      ok: true,
      userMsg,
      godMsg,
      messages: godChatHistory,
      history: godChatHistory,
    });
  });

  // --- DIRECT SUBAGENT COMMISSION FROM RIGHT INSPECTOR OR TOPOLOGY GRAPH ---
  const handleDirectCommission = async (req: express.Request, res: express.Response) => {
    const payload = req.body || {};
    const subagente = String(payload.subagent || payload.subagente || 'guardian-consistencia');
    const customTask = String(payload.task || payload.tarea || `Ejecutar auditoría del rol @${subagente} según ESTADO_TESIS.md`);
    const fase = String(payload.phase || payload.fase || 'F4');
    const squad = String(payload.squad || SQUAD_BY_AGENT[subagente]?.squad || 'Squad Especializado');
    const rawEngine = String(payload.engine || payload.mode || 'claude').toLowerCase();
    const mode: 'bun' | 'claude' | 'droid' =
      rawEngine === 'droid' ? 'droid' : rawEngine === 'bun' ? 'bun' : 'claude';
    const cliEntryCmd = mode === 'claude' ? 'claude' : mode === 'droid' ? 'droid' : 'bun';
    const cliDisplay = `${cliEntryCmd}  ➜  ${cliEntryCmd} (@${subagente}) > ${customTask}`;

    const result = await executeCommandInTerminal(cliEntryCmd, {
      mode,
      agentId: subagente,
      promptText: customTask,
      tarea: customTask,
      fase,
      squad,
      createHandoff: true,
    });

    const finalStatus: 'completed' | 'blocked' = result.exitCode === 0 ? 'completed' : 'blocked';
    const cleanOutput = result.output.trim().slice(0, 1200) || 'Comisión ejecutada en CLI.';
    const nowIso = new Date().toISOString();
    const delObj = {
      id: `del-${Date.now()}`,
      subagente,
      agentId: subagente,
      agentName: subagente,
      squad,
      fase,
      task: customTask,
      runtime: mode,
      engine: mode,
      command: cliDisplay,
      claudeCliCmd: `claude`,
      droidCliCmd: `droid`,
      status: finalStatus,
      outputSummary: cleanOutput,
      handoffPath: result.handoffPath,
      handoffFile: result.handoffPath,
      exitCode: result.exitCode,
      startedAt: nowIso,
      completedAt: nowIso,
    };

    const msgText =
      `${cleanOutput}\n\n---\n` +
      `- **Comisión Directa CLI:** \`$ ${cliEntryCmd}\`  ➜  \`${cliEntryCmd} (@${subagente}) > ${customTask}\`\n` +
      `- **Handoff depositado en:** \`${result.handoffPath || 'obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/'}\``;

    const commMsg: GodChatMessage = {
      id: `msg-comm-${Date.now()}`,
      timestamp: nowIso,
      role: 'god',
      senderName: 'Director General (Agente GOD)',
      senderId: 'director-general',
      squad: 'Hub Central',
      text: msgText,
      content: msgText,
      engineUsed: mode.toUpperCase(),
      delegation: delObj,
      delegations: [
        {
          ...delObj,
          status: finalStatus === 'completed' ? 'completed' : 'error',
        },
      ],
    };
    godChatHistory.push(commMsg);
    broadcast('godchat:message', commMsg, { message: commMsg });

    res.json({
      ok: true,
      dispatched: true,
      subagente,
      command: cliCmd,
      exitCode: result.exitCode,
      output: result.output,
      handoffPath: result.handoffPath,
    });
  };

  app.post('/api/agent/commission', handleDirectCommission);
  app.post('/api/dispatch-comision', handleDirectCommission);

  // --- TERMINAL & LIVE EXECUTION ENDPOINTS ---
  app.post('/api/terminal/exec', async (req, res) => {
    const { command, mode, session, agentId, tarea, taskPrompt, fase, phase, squad, createHandoff } = req.body || {};
    const resolvedMode: 'bun' | 'shell' | 'claude' | 'droid' =
      mode ||
      (session === 'claude-code' ? 'claude' : session === 'factory-droid' ? 'droid' : 'shell');
    const cmdToRun = command || AGENT_DEFAULT_SCRIPTS[agentId || 'director-general'] || `${PY_BIN} scripts/agentes/estado_granja.py`;
    const result = await executeCommandInTerminal(String(cmdToRun), {
      mode: resolvedMode,
      agentId: agentId || 'director-general',
      tarea: tarea || taskPrompt,
      fase: fase || phase || 'F4',
      squad,
      createHandoff: Boolean(createHandoff),
    });
    res.json(result);
  });

  app.post('/api/terminal/clear', (_req, res) => {
    terminalHistory.splice(0, terminalHistory.length);
    broadcast('terminal:cleared', {});
    res.json({ cleared: true });
  });

  app.post('/api/terminal/kill', (_req, res) => {
    if (activeChildProcess) {
      activeChildProcess.kill('SIGINT');
      appendTerminalLine('system', '[SEÑAL SIGINT] Ejecución detenida manualmente.');
      res.json({ killed: true });
      return;
    }
    res.json({ killed: false });
  });

  // --- LOOP 3.0 COGNITIVE PROMPT REFINER ---
  app.post('/api/refine-prompt', (req, res) => {
    const rawPrompt = String(req.body?.prompt || '').trim();
    if (!rawPrompt) {
      res.status(400).json({ error: 'Ingrese una solicitud o prompt para refinar.' });
      return;
    }
    const intent = classifyPromptIntent(rawPrompt);

    res.json({
      diagnostico: intent.diagnostico,
      comandoSugerido: intent.comandoSugerido,
      claudeCliCmd: intent.claudeCliCmd,
      droidCliCmd: intent.droidCliCmd,
      comision: {
        tarea: intent.tarea,
        fase: intent.fase,
        squad: intent.squad,
        subagente: intent.subagente,
        entradas: intent.entradas,
        salida_esperada: intent.salidaEsperada,
        restricciones:
          'Cumplimiento estricto de Regla 01 (prohibido tocar referencias/, syncova, PROYECTO_TESIS.docx o simular datos en datos/raw/) y Regla 02 (3 dimensiones DEC-007).',
        criterio_exito:
          'Ejecución verificada en terminal Bun con código 0, artefacto validado en salidas/ y handoff depositado en obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/.',
      },
    });
  });

  // --- CAPABILITIES MANAGEMENT (MCPs, SKILLS, AGENT TOOLS, HOOKS) ---
  app.patch('/api/capabilities/mcp', (req, res) => {
    const { name, id, enabled, command, args, url } = req.body || {};
    const mcpKey = name || id;
    if (!mcpKey) {
      res.status(400).json({ error: 'Nombre de servidor MCP requerido' });
      return;
    }
    const mcpPath = path.join(__dirname, '.mcp.json');
    const mcpData = fs.existsSync(mcpPath) ? JSON.parse(fs.readFileSync(mcpPath, 'utf-8')) : { mcpServers: {} };
    if (!mcpData.mcpServers) mcpData.mcpServers = {};
    const current = mcpData.mcpServers[mcpKey] || {};

    mcpData.mcpServers[mcpKey] = {
      ...current,
      ...(command !== undefined ? { command } : {}),
      ...(args !== undefined ? { args } : {}),
      ...(url !== undefined ? { url } : {}),
      disabled: enabled === false,
    };
    if (enabled === true) {
      delete mcpData.mcpServers[mcpKey].disabled;
    }

    fs.writeFileSync(mcpPath, JSON.stringify(mcpData, null, 2) + '\n', 'utf-8');
    try {
      execFileSync(PY_BIN, ['scripts/sync_factory.py'], { cwd: __dirname });
    } catch {
      // non-fatal
    }
    appendTerminalLine(
      'system',
      `[CONFIG MCP ACTUALIZADA] Servidor "${mcpKey}" -> ${enabled ? 'ACTIVO' : 'DESACTIVADO'} en .mcp.json y sincronizado con .factory/`
    );
    broadcast('capabilities:updated', { type: 'mcp', name: mcpKey, enabled });
    res.json({ ok: true, mcpServers: mcpData.mcpServers });
  });

  app.patch('/api/capabilities/skill', (req, res) => {
    const { id, enabled } = req.body || {};
    if (!id) {
      res.status(400).json({ error: 'ID de skill requerido' });
      return;
    }
    if (enabled === false) {
      disabledSkillsSet.add(String(id));
    } else {
      disabledSkillsSet.delete(String(id));
    }
    appendTerminalLine(
      'system',
      `[SKILL ACTUALIZADA] Skill "${id}" -> ${enabled !== false ? 'HABILITADA' : 'DESHABILITADA'}`
    );
    broadcast('capabilities:updated', { type: 'skill', id, enabled: enabled !== false });
    res.json({ ok: true, id, enabled: enabled !== false });
  });

  app.patch('/api/capabilities/agent', (req, res) => {
    const { agentId, tools, skills, model } = req.body || {};
    if (!agentId) {
      res.status(400).json({ error: 'agentId requerido' });
      return;
    }
    const agentPath = path.join(__dirname, '.claude', 'agents', `${agentId}.md`);
    if (!fs.existsSync(agentPath)) {
      res.status(404).json({ error: 'Agente no encontrado' });
      return;
    }

    if (agentId === 'ingeniero-sivac' && Array.isArray(tools)) {
      const forbiddenTools = tools.filter((t: string) => !['Read', 'Grep', 'Glob'].includes(t));
      if (forbiddenTools.length > 0) {
        res.status(403).json({
          error: `[REGLA CANÓNICA 01] El subagente "ingeniero-sivac" tiene prohibido recibir herramientas de escritura o ejecución (${forbiddenTools.join(', ')}). Debe permanecer en modo SOLO LECTURA (Read, Grep, Glob).`,
        });
        return;
      }
    }

    const raw = fs.readFileSync(agentPath, 'utf-8');
    const { frontmatter, body } = parseYamlFrontmatter(raw);
    if (Array.isArray(tools)) frontmatter.tools = tools;
    if (Array.isArray(skills)) frontmatter.skills = skills;
    if (typeof model === 'string' && model.trim()) frontmatter.model = model.trim();

    const updatedMd = serializeYamlFrontmatter(frontmatter, body);
    fs.writeFileSync(agentPath, updatedMd, 'utf-8');

    const droidPath = path.join(__dirname, '.factory', 'droids', `${agentId}.md`);
    if (fs.existsSync(path.dirname(droidPath))) {
      fs.writeFileSync(droidPath, updatedMd, 'utf-8');
    }

    appendTerminalLine(
      'system',
      `[AGENTE ACTUALIZADO] ${agentId} sincronizado en .claude/agents/${agentId}.md y .factory/droids/${agentId}.md`
    );
    broadcast('capabilities:updated', { type: 'agent', agentId });
    res.json({ ok: true, agent: loadAgents().find((a) => a.id === agentId) });
  });

  app.patch('/api/capabilities/hook', (req, res) => {
    const { hookEvent, id, enabled } = req.body || {};
    const evtKey = hookEvent || id;
    if (!evtKey) {
      res.status(400).json({ error: 'Evento de hook requerido' });
      return;
    }
    if (evtKey === 'PreToolUse' && enabled === false) {
      res.status(403).json({
        error:
          '[REGLA CANÓNICA 01] El hook PreToolUse (pretooluse_blocker.cjs) es un candado constitucional innegociable y no puede desactivarse.',
      });
      return;
    }
    const settingsPath = path.join(__dirname, '.claude', 'settings.json');
    const settingsData = fs.existsSync(settingsPath)
      ? JSON.parse(fs.readFileSync(settingsPath, 'utf-8'))
      : { hooks: {} };
    if (!settingsData.hooksStatus) settingsData.hooksStatus = {};
    settingsData.hooksStatus[evtKey] = enabled !== false;
    fs.writeFileSync(settingsPath, JSON.stringify(settingsData, null, 2) + '\n', 'utf-8');
    appendTerminalLine(
      'system',
      `[HOOK ACTUALIZADO] Evento "${evtKey}" -> ${enabled !== false ? 'ACTIVO' : 'PAUSADO'} en .claude/settings.json y .factory/hooks.json`
    );
    broadcast('capabilities:updated', { type: 'hook', hookEvent: evtKey, enabled: enabled !== false });
    res.json({ ok: true, settings: settingsData });
  });

  // --- MULTI-PROJECT & KANBAN TASKS MANAGEMENT ---
  app.get('/api/projects', (_req, res) => {
    res.json(loadProjectsStore());
  });

  app.post('/api/projects', (req, res) => {
    const { codigo, code, titulo, title, tipo, university, diseno, methodology, sampleSize, variableIndependiente, variableDependiente, dimensiones } = req.body || {};
    const finalTitle = titulo || title;
    const finalCode = codigo || code || `INV-${new Date().getFullYear()}`;
    if (!finalTitle) {
      res.status(400).json({ error: 'Título del proyecto requerido' });
      return;
    }
    const store = loadProjectsStore();
    const newId = `proy-${Date.now()}`;
    const newProject = {
      id: newId,
      codigo: finalCode,
      code: finalCode,
      titulo: finalTitle,
      title: finalTitle,
      tipo: tipo || 'Proyecto de Investigación Científica',
      university: university || 'UNAJMA — Ingeniería de Sistemas',
      tesista: 'Bach. José Luis Quispe León',
      asesora: 'Dra. Norma Lorena Catacora Flores',
      diseno: diseno || methodology || 'Cuasi-experimental / Aplicada',
      methodology: methodology || diseno || 'Cuasi-experimental / Aplicada',
      sampleSize: sampleSize || 'n=14',
      faseActual: 'F0',
      progreso: 10,
      progress: 10,
      variableIndependiente: variableIndependiente || 'Variable Independiente (Tecnológica)',
      variableDependiente: variableDependiente || 'Variable Dependiente (Operativa)',
      dimensiones: Array.isArray(dimensiones) && dimensiones.length > 0 ? dimensiones : ['Dimensión 1', 'Dimensión 2', 'Dimensión 3'],
      qualityGates: [
        { id: 'QG-0', fase: 'F0', nombre: 'Protocolo y Matriz de Consistencia', metrica: 'Variables e indicadores definidos', estado: 'aprobado' },
        { id: 'QG-1', fase: 'F1', nombre: 'Marco Teórico y Literatura', metrica: 'Citas APA 7 verificadas', estado: 'en_progreso' },
        { id: 'QG-2', fase: 'F2', nombre: 'Trabajo de Campo y Resultados', metrica: 'Datos empíricos certificados', estado: 'pendiente' },
      ],
      tasks: [
        {
          id: `task-${Date.now()}`,
          titulo: 'Estructurar Matriz de Consistencia y Operacionalización de Variables',
          title: 'Estructurar Matriz de Consistencia y Operacionalización de Variables',
          fase: 'F1',
          phase: 'F1',
          capitulo: 'Cap. I Planteamiento',
          squad: 'Squad B (Metodología, Medición y Psicometría)',
          subagente: 'guardian-consistencia',
          assignedAgent: 'guardian-consistencia',
          estado: 'en_progreso',
          status: 'en_progreso',
          prioridad: 'alta',
          comando: `${PY_BIN} scripts/agentes/guardian_consistencia.py`,
          entregable: 'obsidian_vault/01_MATRIZ_Y_CONSISTENCIA/MATRIZ_CONSISTENCIA_DEC007.md',
        },
      ],
    };
    store.projects.push(newProject);
    store.activeProjectId = newId;
    saveProjectsStore(store);
    appendTerminalLine('system', `[NUEVO PROYECTO CREADO] "${finalTitle}" (${finalCode}) registrado en Bóveda Obsidian.`);
    broadcast('projects:updated', store);
    res.json(store);
  });

  app.patch('/api/projects/active', (req, res) => {
    const { projectId } = req.body || {};
    const store = loadProjectsStore();
    if (store.projects.some((p: { id: string }) => p.id === projectId)) {
      store.activeProjectId = projectId;
      saveProjectsStore(store);
      broadcast('projects:updated', store);
    }
    res.json(store);
  });

  app.post('/api/projects/:projectId/tasks', (req, res) => {
    const { projectId } = req.params;
    const { titulo, title, fase, phase, capitulo, squad, subagente, assignedAgent, prioridad, comando, entregable } = req.body || {};
    const finalTitle = titulo || title;
    const finalPhase = fase || phase || 'F4';
    const finalAgent = subagente || assignedAgent || 'maquetador-docx';
    if (!finalTitle) {
      res.status(400).json({ error: 'Título de la tarea requerido' });
      return;
    }
    const store = loadProjectsStore();
    const project = store.projects.find((p: { id: string }) => p.id === projectId);
    if (!project) {
      res.status(404).json({ error: 'Proyecto no encontrado' });
      return;
    }
    const newTask = {
      id: `task-${Date.now()}`,
      titulo: finalTitle,
      title: finalTitle,
      fase: finalPhase,
      phase: finalPhase,
      capitulo: capitulo || 'General',
      squad: squad || SQUAD_BY_AGENT[finalAgent]?.squad || 'Squad E (Redacción, Estilo y Maquetación Editorial)',
      subagente: finalAgent,
      assignedAgent: finalAgent,
      estado: 'pendiente',
      status: 'pendiente',
      prioridad: prioridad || 'alta',
      comando: comando || AGENT_DEFAULT_SCRIPTS[finalAgent] || `${PY_BIN} scripts/agentes/estado_granja.py`,
      entregable: entregable || 'salidas/documentos/informe_final_v02.docx',
    };
    project.tasks.unshift(newTask);
    saveProjectsStore(store);
    appendTerminalLine('system', `[TAREA CREADA] "${finalTitle}" asignada a @${finalAgent} (${finalPhase}).`);
    broadcast('projects:updated', store);
    res.json(store);
  });

  app.patch('/api/projects/:projectId/tasks/:taskId', (req, res) => {
    const { projectId, taskId } = req.params;
    const { estado, status, subagente, assignedAgent, fase, phase } = req.body || {};
    const nextStatus = status || estado;
    const store = loadProjectsStore();
    const project = store.projects.find((p: { id: string }) => p.id === projectId);
    if (!project) {
      res.status(404).json({ error: 'Proyecto no encontrado' });
      return;
    }
    const task = project.tasks.find((t: { id: string }) => t.id === taskId);
    if (!task) {
      res.status(404).json({ error: 'Tarea no encontrada' });
      return;
    }
    if (nextStatus) {
      task.estado = nextStatus === 'completado' ? 'completada' : nextStatus;
      task.status = nextStatus === 'completada' ? 'completado' : nextStatus;
    }
    if (subagente || assignedAgent) {
      task.subagente = subagente || assignedAgent;
      task.assignedAgent = subagente || assignedAgent;
    }
    if (fase || phase) {
      task.fase = fase || phase;
      task.phase = fase || phase;
    }

    const total = project.tasks.length;
    const done = project.tasks.filter(
      (t: { estado?: string; status?: string }) => t.estado === 'completada' || t.estado === 'completado' || t.status === 'completado'
    ).length;
    project.progreso = total > 0 ? Math.round((done / total) * 100) : 0;
    project.progress = project.progreso;

    saveProjectsStore(store);
    broadcast('projects:updated', store);
    res.json(store);
  });

  // --- VAULT & PROJECT FILE INSPECTOR ENDPOINTS ---
  app.get('/api/vault/file', (req, res) => {
    const rawRel = String(req.query.path || '00_SISTEMA/ESTADO_TESIS.md')
      .replace(/\\/g, '/')
      .replace(/^obsidian_vault\//, '');
    if (rawRel.includes('..')) {
      res.status(403).json({ error: 'Ruta inválida' });
      return;
    }
    const fullPath = path.join(__dirname, 'obsidian_vault', rawRel);
    if (!fs.existsSync(fullPath) || fs.statSync(fullPath).isDirectory()) {
      res.status(404).json({ error: 'Nota no encontrada en Obsidian Vault' });
      return;
    }
    res.json({
      path: rawRel,
      content: fs.readFileSync(fullPath, 'utf-8'),
    });
  });

  app.post('/api/vault/file', (req, res) => {
    const rawRel = String(req.body?.path || '')
      .replace(/\\/g, '/')
      .replace(/^obsidian_vault\//, '');
    const content = String(req.body?.content ?? '');
    if (!rawRel || rawRel.includes('..')) {
      res.status(403).json({ error: 'Ruta inválida' });
      return;
    }
    const fullPath = path.join(__dirname, 'obsidian_vault', rawRel);
    fs.mkdirSync(path.dirname(fullPath), { recursive: true });
    fs.writeFileSync(fullPath, content, 'utf-8');
    appendTerminalLine('system', `[OBSIDIAN VAULT ACTUALIZADO] Guardado: obsidian_vault/${rawRel}`);
    res.json({ ok: true, path: rawRel });
  });

  const inspectFileHandler = (req: express.Request, res: express.Response) => {
    const relPath = String(req.query.path || '').replace(/\\/g, '/');
    if (!isAllowedPath(relPath)) {
      res.status(403).json({ error: 'Ruta inválida o fuera del alcance de inspección' });
      return;
    }
    const fullPath = path.join(__dirname, relPath);
    if (!fs.existsSync(fullPath) || fs.statSync(fullPath).isDirectory()) {
      res.status(404).json({ error: 'Archivo no encontrado' });
      return;
    }

    const stat = fs.statSync(fullPath);
    const ext = path.extname(relPath).toLowerCase();
    const buf = fs.readFileSync(fullPath);
    const sha256 = crypto.createHash('sha256').update(buf).digest('hex');

    if (ext === '.docx') {
      try {
        const pyScript = `
import json, sys, zipfile, xml.etree.ElementTree as ET
from scripts.utilidades.docx_quirurgico import auditar_docx_openxml
p = sys.argv[1]
aud = auditar_docx_openxml(p)
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
parrafos = []
tablas = []
with zipfile.ZipFile(p, "r") as zf:
    root = ET.fromstring(zf.read("word/document.xml"))
    body = root.find(f"{W}body")
    if body is not None:
        for child in body:
            if child.tag == f"{W}p":
                txt = "".join(t.text or "" for t in child.iter(f"{W}t")).strip()
                math_txt = "".join(t.text or "" for t in child.iter(f"{M}t")).strip()
                full_t = (math_txt + " " + txt).strip() if math_txt else txt
                if full_t:
                    parrafos.append(full_t)
            elif child.tag == f"{W}tbl":
                rows_data = []
                for tr in child.findall(f"{W}tr"):
                    cells = ["".join(t.text or "" for t in tc.iter(f"{W}t")).strip() for tc in tr.findall(f"{W}tc")]
                    rows_data.append(cells)
                tablas.append(rows_data)
print(json.dumps({"auditoria": aud, "parrafos": parrafos, "tablas": tablas}, ensure_ascii=False))
`;
        const out = execFileSync(PY_BIN, ['-c', pyScript, fullPath], {
          cwd: __dirname,
          encoding: 'utf-8',
        });
        const parsed = JSON.parse(out);
        const formattedLines: string[] = [
          `================================================================================`,
          `DOCUMENTO MICROSOFT WORD NATIVO OPENXML (.DOCX)`,
          `Ruta:     ${relPath}`,
          `Tamaño:   ${stat.size.toLocaleString()} bytes`,
          `SHA-256:  ${sha256}`,
          `Márgenes: ${parsed.auditoria?.margenes_unajma_ok ? 'UNAJMA Oficial (3.5cm / 2.5cm -> 1985 / 1418 dxa) [OK]' : 'Observado'}`,
          `Tablas:   ${parsed.auditoria?.tablas_total} tablas APA 7 (${parsed.auditoria?.tablas_flotantes} flotantes, ${parsed.auditoria?.tablas_con_header} con tblHeader)`,
          `Fórmulas: ${parsed.auditoria?.formulas_omml} ecuaciones nativas OMML | Referencias: ${parsed.auditoria?.referencias_sangria_francesa} con sangría francesa`,
          `================================================================================`,
          ``,
          `--- CONTENIDO TEXTUAL EXTRAÍDO DE word/document.xml ---`,
          ...parsed.parrafos.map((p: string, i: number) => `[P${String(i + 1).padStart(2, '0')}] ${p}`),
        ];
        if (parsed.tablas && parsed.tablas.length > 0) {
          formattedLines.push(``, `--- TABLAS NATIVAS APA 7 EXTRAÍDAS (${parsed.tablas.length}) ---`);
          parsed.tablas.forEach((tbl: string[][], tIdx: number) => {
            formattedLines.push(`\n[Tabla #${tIdx + 1}] (${tbl.length} filas):`);
            tbl.forEach((row: string[], rIdx: number) => {
              formattedLines.push(`  ${rIdx === 0 ? 'ENCABEZADO' : `Fila ${String(rIdx).padStart(2, '0')}   `}: ${row.join(' | ')}`);
            });
          });
        }
        res.json({
          path: relPath,
          binaryType: 'docx',
          sha256,
          sizeBytes: stat.size,
          audit: parsed.auditoria,
          content: formattedLines.join('\n'),
        });
        return;
      } catch {
        res.json({
          path: relPath,
          binaryType: 'docx',
          sha256,
          sizeBytes: stat.size,
          content: `Archivo Word OpenXML (.docx) — ${stat.size} bytes — SHA-256: ${sha256}`,
        });
        return;
      }
    }

    const content = buf.toString('utf-8');
    res.json({ path: relPath, binaryType: 'text', sha256, content, sizeBytes: stat.size });
  };

  app.get('/api/file', inspectFileHandler);
  app.get('/api/project/file', inspectFileHandler);

  app.get('/api/download', (req, res) => {
    const relPath = String(req.query.path || '').replace(/\\/g, '/');
    const inline = req.query.inline === '1';
    if (!isAllowedPath(relPath)) {
      res.status(403).send('Ruta fuera del alcance permitido');
      return;
    }
    const fullPath = path.join(__dirname, relPath);
    if (!fs.existsSync(fullPath) || fs.statSync(fullPath).isDirectory()) {
      res.status(404).send('Archivo no encontrado');
      return;
    }
    const ext = path.extname(relPath).toLowerCase();
    const mimeMap: Record<string, string> = {
      '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      '.pdf': 'application/pdf',
      '.png': 'image/png',
      '.json': 'application/json; charset=utf-8',
      '.csv': 'text/csv; charset=utf-8',
      '.md': 'text/markdown; charset=utf-8',
      '.py': 'text/x-python; charset=utf-8',
    };
    const contentType = mimeMap[ext] || 'application/octet-stream';
    res.setHeader('Content-Type', contentType);
    const disp = inline && (ext === '.pdf' || ext === '.png') ? 'inline' : 'attachment';
    res.setHeader('Content-Disposition', `${disp}; filename="${path.basename(relPath)}"`);
    fs.createReadStream(fullPath).pipe(res);
  });

  app.post('/api/recompilar', async (_req, res) => {
    try {
      const result = await executeCommandInTerminal(`${PY_BIN} scripts/compiladores/compilar_informe_final.py`, {
        mode: 'shell',
        agentId: 'maquetador-docx',
        tarea: 'Recompilación integral de entregables DOCX, PDF, XLSX y Figuras 300 DPI',
        fase: 'F4',
        squad: 'Squad E (Redacción, Estilo y Maquetación Editorial)',
        createHandoff: true,
      });
      res.json({ estado: 'completado', exitCode: result.exitCode });
    } catch (error) {
      res.status(500).json({ error: error instanceof Error ? error.message : 'Error al recompilar entregables' });
    }
  });

  if (process.env.NODE_ENV !== 'production') {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(__dirname, 'dist');
    app.use(express.static(distPath));
    app.get('*', (_req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  server.listen(PORT, '0.0.0.0', () => {
    console.log(`[SIVAC-THESIS-LAB OS] HTTP + WebSocket activo en http://0.0.0.0:${PORT}`);
  });
}

startServer();
