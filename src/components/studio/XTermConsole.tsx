import React, { useEffect, useRef, useState } from 'react';
import { Terminal } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';
import {
  Terminal as TerminalIcon,
  Play,
  Trash2,
  ChevronDown,
  ChevronUp,
  Cpu,
  Command,
} from 'lucide-react';
import type { TerminalLog, CliToolStatus } from '../../types/studio';

interface XTermConsoleProps {
  logs: TerminalLog[];
  activeSession: 'bun-shell' | 'claude-code' | 'factory-droid';
  onSelectSession: (session: 'bun-shell' | 'claude-code' | 'factory-droid') => void;
  onExecuteCommand: (command: string, session?: string) => Promise<void>;
  onClearTerminal: () => Promise<void>;
  isMinimized: boolean;
  onToggleMinimize: () => void;
  cliStatuses: CliToolStatus[];
}

export const XTermConsole: React.FC<XTermConsoleProps> = ({
  logs,
  activeSession,
  onSelectSession,
  onExecuteCommand,
  onClearTerminal,
  isMinimized,
  onToggleMinimize,
  cliStatuses,
}) => {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const termRef = useRef<Terminal | null>(null);
  const fitAddonRef = useRef<FitAddon | null>(null);
  const renderedCountRef = useRef<number>(0);
  const inputBufferRef = useRef<string>('');
  const [quickInput, setQuickInput] = useState('');
  const [isRunning, setIsRunning] = useState(false);

  const sessionRunnerRef = useRef(activeSession);
  const executeCallbackRef = useRef(onExecuteCommand);

  useEffect(() => {
    sessionRunnerRef.current = activeSession;
  }, [activeSession]);

  useEffect(() => {
    executeCallbackRef.current = onExecuteCommand;
  }, [onExecuteCommand]);

  useEffect(() => {
    if (!containerRef.current || termRef.current) return;

    const term = new Terminal({
      cursorBlink: true,
      cursorStyle: 'bar',
      fontFamily: "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
      fontSize: 12,
      lineHeight: 1.45,
      convertEol: true,
      scrollback: 3000,
      theme: {
        background: '#090b10',
        foreground: '#e4e4e7',
        cursor: '#f97316',
        selectionBackground: 'rgba(249, 115, 22, 0.28)',
        black: '#18181b',
        red: '#ef4444',
        green: '#22c55e',
        yellow: '#f59e0b',
        blue: '#3b82f6',
        magenta: '#a855f7',
        cyan: '#06b6d4',
        white: '#f4f4f5',
        brightBlack: '#71717a',
        brightRed: '#f87171',
        brightGreen: '#4ade80',
        brightYellow: '#fbbf24',
        brightBlue: '#60a5fa',
        brightMagenta: '#c084fc',
        brightCyan: '#22d3ee',
        brightWhite: '#ffffff',
      },
    });

    const fitAddon = new FitAddon();
    term.loadAddon(fitAddon);
    term.open(containerRef.current);

    setTimeout(() => {
      try {
        fitAddon.fit();
      } catch {
        // Ignore fit error when container is hidden
      }
    }, 60);

    term.writeln(
      '\x1b[38;5;208m╭──────────────────────────────────────────────────────────────────────────╮\x1b[0m'
    );
    term.writeln(
      '\x1b[38;5;208m│\x1b[0m \x1b[1;37mSIVAC-THESIS-LAB · XTerm.js + Bun Shell Runtime Bridge\x1b[0m                  \x1b[38;5;208m│\x1b[0m'
    );
    term.writeln(
      '\x1b[38;5;208m│\x1b[0m \x1b[90mEscribe cualquier comando directamente aquí o usa la barra inferior.\x1b[0m     \x1b[38;5;208m│\x1b[0m'
    );
    term.writeln(
      '\x1b[38;5;208m╰──────────────────────────────────────────────────────────────────────────╯\x1b[0m'
    );
    term.write('\r\n\x1b[1;33msivac@unajma\x1b[0m:\x1b[1;34m~\x1b[0m$ ');

    term.onData((data) => {
      const code = data.charCodeAt(0);
      if (code === 13) {
        // Enter
        const cmd = inputBufferRef.current.trim();
        term.write('\r\n');
        inputBufferRef.current = '';
        if (cmd) {
          executeCallbackRef.current(cmd, sessionRunnerRef.current);
        } else {
          term.write('\x1b[1;33msivac@unajma\x1b[0m:\x1b[1;34m~\x1b[0m$ ');
        }
      } else if (code === 127 || code === 8) {
        // Backspace
        if (inputBufferRef.current.length > 0) {
          inputBufferRef.current = inputBufferRef.current.slice(0, -1);
          term.write('\b \b');
        }
      } else if (code === 3) {
        // Ctrl+C
        inputBufferRef.current = '';
        term.write('^C\r\n\x1b[1;33msivac@unajma\x1b[0m:\x1b[1;34m~\x1b[0m$ ');
      } else if (code >= 32) {
        inputBufferRef.current += data;
        term.write(data);
      }
    });

    termRef.current = term;
    fitAddonRef.current = fitAddon;

    const resizeObserver = new ResizeObserver(() => {
      try {
        fitAddon.fit();
      } catch {
        // ignore
      }
    });
    resizeObserver.observe(containerRef.current);

    return () => {
      resizeObserver.disconnect();
      term.dispose();
      termRef.current = null;
      fitAddonRef.current = null;
    };
  }, []);

  // Re-fit when un-minimized
  useEffect(() => {
    if (!isMinimized && fitAddonRef.current) {
      setTimeout(() => {
        try {
          fitAddonRef.current?.fit();
        } catch {
          // ignore
        }
      }, 80);
    }
  }, [isMinimized]);

  // Stream new logs into XTerm
  useEffect(() => {
    const term = termRef.current;
    if (!term) return;

    if (logs.length === 0 && renderedCountRef.current > 0) {
      term.clear();
      renderedCountRef.current = 0;
      term.write('\x1b[1;33msivac@unajma\x1b[0m:\x1b[1;34m~\x1b[0m$ ');
      return;
    }

    const newLogs = logs.slice(renderedCountRef.current);
    if (newLogs.length === 0) return;

    newLogs.forEach((entry) => {
      const time = entry.timestamp
        ? new Date(entry.timestamp).toLocaleTimeString('es-PE', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
          })
        : '';
      const cleanLines = String(entry.text || '').split(/\r?\n/);
      cleanLines.forEach((line) => {
        if (!line.trim() && cleanLines.length > 1) return;
        if (entry.type === 'command') {
          term.writeln(`\r\x1b[90m[${time}]\x1b[0m \x1b[1;38;5;208m${line}\x1b[0m`);
        } else if (entry.type === 'stderr') {
          term.writeln(`\r\x1b[90m[${time}]\x1b[0m \x1b[31m${line}\x1b[0m`);
        } else if (entry.type === 'system') {
          term.writeln(`\r\x1b[90m[${time}]\x1b[0m \x1b[36m${line}\x1b[0m`);
        } else {
          term.writeln(`\r\x1b[37m${line}\x1b[0m`);
        }
      });
    });

    renderedCountRef.current = logs.length;
    term.write('\x1b[1;33msivac@unajma\x1b[0m:\x1b[1;34m~\x1b[0m$ ');
    term.scrollToBottom();
  }, [logs]);

  const handleQuickSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const cmd = quickInput.trim();
    if (!cmd || isRunning) return;
    setIsRunning(true);
    setQuickInput('');
    try {
      await onExecuteCommand(cmd, activeSession);
    } finally {
      setIsRunning(false);
    }
  };

  const bunStatus = cliStatuses.find((c) => c.id === 'bun');
  const claudeStatus = cliStatuses.find((c) => c.id === 'claude');
  const droidStatus = cliStatuses.find((c) => c.id === 'droid');

  return (
    <div className="h-full flex flex-col bg-[#090b10] border-t border-white/10 select-text">
      {/* Terminal Header Bar (OpenHands + Opcode style) */}
      <div className="h-9 px-3 flex items-center justify-between gap-2 bg-[#0f1219] border-b border-white/10 shrink-0">
        <div className="flex items-center gap-2 min-w-0 flex-1 overflow-hidden">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-zinc-200 whitespace-nowrap shrink-0">
            <TerminalIcon className="w-3.5 h-3.5 text-orange-400" />
            <span>Terminal XTerm.js</span>
          </div>

          <span className="text-zinc-700 shrink-0" aria-hidden="true">
            ·
          </span>

          {/* Interactive Session Tabs */}
          <div className="flex items-center gap-1 bg-black/40 p-0.5 rounded-md border border-white/10 shrink-0">
            <button
              type="button"
              onClick={() => onSelectSession('bun-shell')}
              className={`px-2 py-1 rounded text-[11px] font-mono transition-colors whitespace-nowrap shrink-0 ${
                activeSession === 'bun-shell'
                  ? 'bg-orange-500/20 text-orange-300 font-semibold'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              bun-shell {bunStatus?.installed ? `(${bunStatus.version})` : ''}
            </button>
            <button
              type="button"
              onClick={() => onSelectSession('claude-code')}
              className={`px-2 py-1 rounded text-[11px] font-mono transition-colors whitespace-nowrap shrink-0 ${
                activeSession === 'claude-code'
                  ? 'bg-orange-500/20 text-orange-300 font-semibold'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              claude-code {claudeStatus?.installed ? '· Activo' : '· Bridge'}
            </button>
            <button
              type="button"
              onClick={() => onSelectSession('factory-droid')}
              className={`px-2 py-1 rounded text-[11px] font-mono transition-colors whitespace-nowrap shrink-0 ${
                activeSession === 'factory-droid'
                  ? 'bg-orange-500/20 text-orange-300 font-semibold'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              factory-droid {droidStatus?.installed ? '· Activo' : '· Bridge'}
            </button>
          </div>

          {/* Quick Preset Commands */}
          <div className="hidden xl:flex items-center gap-1.5 ml-1 overflow-x-auto no-scrollbar min-w-0">
            {[
              { label: 'claude "hola"', cmd: 'claude "hola"' },
              { label: 'Avance Tesis', cmd: 'claude "como esta mi avance actual de mi tesis?"' },
              { label: 'claude --version', cmd: 'claude --version' },
              { label: 'droid --version', cmd: 'droid --version' },
              { label: 'bun --version', cmd: 'bun --version' },
            ].map((preset) => (
              <button
                key={preset.cmd}
                type="button"
                onClick={() => onExecuteCommand(preset.cmd, activeSession)}
                className="px-2 py-0.5 text-[11px] font-mono text-zinc-400 hover:text-zinc-100 bg-white/[0.03] hover:bg-white/[0.08] border border-white/10 rounded transition-colors whitespace-nowrap shrink-0"
              >
                {preset.label}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <button
            type="button"
            onClick={onClearTerminal}
            className="px-2 py-1 text-[11px] text-zinc-400 hover:text-zinc-200 flex items-center gap-1 rounded hover:bg-white/5 transition-colors whitespace-nowrap shrink-0"
            title="Limpiar salida de terminal"
          >
            <Trash2 className="w-3 h-3" />
            <span>Limpiar</span>
          </button>
          <button
            type="button"
            onClick={onToggleMinimize}
            className="px-2 py-1 text-[11px] text-zinc-400 hover:text-zinc-200 flex items-center gap-1 rounded hover:bg-white/5 transition-colors whitespace-nowrap shrink-0"
          >
            {isMinimized ? (
              <>
                <ChevronUp className="w-3.5 h-3.5" />
                <span>Expandir</span>
              </>
            ) : (
              <>
                <ChevronDown className="w-3.5 h-3.5" />
                <span>Minimizar</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* XTerm.js Canvas + Input Bar */}
      {!isMinimized && (
        <>
          <div className="flex-1 min-h-0 relative px-2 py-1 bg-[#090b10] overflow-hidden">
            <div ref={containerRef} className="w-full h-full" />
          </div>

          <form
            onSubmit={handleQuickSubmit}
            className="h-9 px-3 bg-[#0c0f17] border-t border-white/10 flex items-center gap-2 shrink-0"
          >
            <span className="text-[11px] font-mono text-orange-400 flex items-center gap-1 whitespace-nowrap shrink-0">
              <Command className="w-3 h-3" />
              <span>
                {activeSession === 'claude-code'
                  ? 'claude >'
                  : activeSession === 'factory-droid'
                  ? 'droid >'
                  : 'bun $'}
              </span>
            </span>
            <input
              type="text"
              value={quickInput}
              onChange={(e) => setQuickInput(e.target.value)}
              placeholder={
                activeSession === 'claude-code'
                  ? 'Escribe tu prompt para Claude Code CLI (ej. hola, como esta mi avance actual de mi tesis, audita citas APA 7)...'
                  : activeSession === 'factory-droid'
                  ? 'Escribe tu misión para Factory Droid CLI (ej. auditar consistencia, validar instrumentos)...'
                  : 'Escribe un comando shell (ej. bun --version, python --version)...'
              }
              className="flex-1 bg-transparent text-xs font-mono text-zinc-100 placeholder:text-zinc-600 focus:outline-none"
            />
            <button
              type="submit"
              disabled={!quickInput.trim() || isRunning}
              className="px-3 py-1 rounded bg-orange-500 hover:bg-orange-400 disabled:opacity-40 text-xs font-semibold text-zinc-950 flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0"
            >
              <Play className="w-3 h-3 fill-current" />
              <span>Ejecutar</span>
            </button>
          </form>
        </>
      )}
    </div>
  );
};
