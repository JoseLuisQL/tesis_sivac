import React, { useState } from 'react';
import {
  Cpu,
  Play,
  FileCode2,
  Lock,
  Terminal as TerminalIcon,
  Wrench,
  Copy,
  Check,
  FileText,
  X,
} from 'lucide-react';
import type { AgentInfo, HandoffInfo } from '../../types/studio';

interface AgentInspectorPanelProps {
  agent: AgentInfo | null;
  handoffs: HandoffInfo[];
  onCommissionAgent: (
    agent: AgentInfo,
    customTask: string,
    engine: 'claude' | 'droid' | 'bun'
  ) => Promise<void>;
  onOpenFile: (path: string) => void;
  onRunInTerminal: (cmd: string) => Promise<void>;
  onClose?: () => void;
}

export const AgentInspectorPanel: React.FC<AgentInspectorPanelProps> = ({
  agent,
  handoffs,
  onCommissionAgent,
  onOpenFile,
  onRunInTerminal,
  onClose,
}) => {
  const [taskInput, setTaskInput] = useState('');
  const [engine, setEngine] = useState<'claude' | 'droid' | 'bun'>('claude');
  const [copiedCmd, setCopiedCmd] = useState(false);
  const [isDispatching, setIsDispatching] = useState(false);

  if (!agent) {
    return (
      <aside className="h-full bg-[#0d1017] border-l border-white/10 p-5 flex items-center justify-center text-xs text-zinc-500">
        Selecciona un agente en la barra lateral o en el grafo radial para inspeccionarlo.
      </aside>
    );
  }

  const agentHandoffs = handoffs.filter((h) => h.agent === agent.id);
  const defaultTask =
    taskInput.trim() ||
    `Ejecutar auditoría y entregable correspondiente al rol ${agent.role} según ESTADO_TESIS.md`;

  const cliCommandPreview =
    engine === 'claude'
      ? `claude --agent ${agent.id} -p "${defaultTask.replace(/"/g, '\\"')}"`
      : engine === 'droid'
      ? `droid exec --agent ${agent.id} "${defaultTask.replace(/"/g, '\\"')}"`
      : `bun run --cwd . scripts/agent-runner.ts --agent=${agent.id}`;

  const handleCopy = () => {
    navigator.clipboard.writeText(cliCommandPreview);
    setCopiedCmd(true);
    setTimeout(() => setCopiedCmd(false), 1600);
  };

  const handleCommissionSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isDispatching) return;
    setIsDispatching(true);
    try {
      await onCommissionAgent(agent, defaultTask, engine);
      setTaskInput('');
    } finally {
      setIsDispatching(false);
    }
  };

  return (
    <aside className="h-full flex flex-col bg-[#0d1017] border-l border-white/10 overflow-hidden select-none">
      {/* Inspector Header */}
      <div className="p-4 border-b border-white/10 flex items-start justify-between gap-2 bg-[#0f1219] shrink-0">
        <div className="min-w-0">
          <div className="flex items-center gap-1.5 text-[11px] font-mono text-orange-400">
            <span>{agent.squad}</span>
            <span>·</span>
            <span>Modelo: {agent.model}</span>
          </div>
          <h3 className="text-sm font-bold text-white flex items-center gap-1.5 mt-1 truncate">
            <Cpu className="w-4 h-4 text-orange-400 shrink-0" />
            <span className="truncate">{agent.name}</span>
            {agent.readOnly && <Lock className="w-3.5 h-3.5 text-amber-400 shrink-0" />}
          </h3>
          <p className="text-xs text-zinc-400 mt-1 leading-snug">{agent.role}</p>
        </div>

        {onClose && (
          <button
            type="button"
            onClick={onClose}
            className="p-1 rounded hover:bg-white/10 text-zinc-400 hover:text-zinc-100"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Scrollable Inspector Body */}
      <div className="flex-1 min-h-0 overflow-y-auto p-4 space-y-5">
        {/* Direct Commission Form (Opcode AgentExecution style) */}
        <form
          onSubmit={handleCommissionSubmit}
          className="p-3.5 rounded-xl bg-[#121622] border border-white/10 space-y-3"
        >
          <div className="flex items-center justify-between text-xs">
            <span className="font-semibold text-zinc-100">Comisionar Subagente</span>
            <div className="flex items-center gap-1 bg-black/40 p-0.5 rounded border border-white/10 font-mono text-[10px]">
              {(['claude', 'droid', 'bun'] as const).map((eng) => (
                <button
                  key={eng}
                  type="button"
                  onClick={() => setEngine(eng)}
                  className={`px-2 py-0.5 rounded transition-colors ${
                    engine === eng
                      ? 'bg-orange-500 text-zinc-950 font-semibold'
                      : 'text-zinc-400 hover:text-zinc-200'
                  }`}
                >
                  {eng}
                </button>
              ))}
            </div>
          </div>

          <textarea
            rows={3}
            value={taskInput}
            onChange={(e) => setTaskInput(e.target.value)}
            placeholder={`Tarea específica para ${agent.name} (o deja en blanco para usar su directiva canónica)...`}
            className="w-full p-2.5 rounded-lg bg-[#0b0d12] border border-white/10 text-xs text-zinc-100 placeholder:text-zinc-500 focus:outline-none focus:border-orange-500 resize-none"
          />

          {/* Command Preview */}
          <div className="p-2 rounded-lg bg-black/50 border border-white/5 flex items-center justify-between gap-2">
            <code className="text-[10px] font-mono text-zinc-400 truncate">
              $ {cliCommandPreview}
            </code>
            <button
              type="button"
              onClick={handleCopy}
              className="p-1 text-zinc-400 hover:text-white shrink-0"
              title="Copiar comando CLI"
            >
              {copiedCmd ? (
                <Check className="w-3.5 h-3.5 text-emerald-400" />
              ) : (
                <Copy className="w-3.5 h-3.5" />
              )}
            </button>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="submit"
              disabled={isDispatching}
              className="flex-1 py-2 px-3 rounded-lg bg-orange-500 hover:bg-orange-400 disabled:opacity-50 text-xs font-semibold text-zinc-950 flex items-center justify-center gap-1.5 transition-colors whitespace-nowrap shrink-0"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>{isDispatching ? 'Ejecutando...' : 'Despachar Comisión'}</span>
            </button>
            <button
              type="button"
              onClick={() => onRunInTerminal(cliCommandPreview)}
              className="py-2 px-2.5 rounded-lg bg-white/[0.06] hover:bg-white/[0.12] text-xs font-mono text-zinc-200 flex items-center gap-1 transition-colors whitespace-nowrap shrink-0"
              title="Ejecutar directamente en XTerm.js"
            >
              <TerminalIcon className="w-3.5 h-3.5 text-orange-400" />
              <span>CLI</span>
            </button>
          </div>
        </form>

        {/* Agent Definition File */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-[11px] font-mono text-zinc-400">
            <span>CONTRATO DE AGENTE</span>
            <button
              type="button"
              onClick={() => onOpenFile(agent.filePath)}
              className="text-orange-400 hover:text-orange-300 flex items-center gap-1"
            >
              <FileCode2 className="w-3 h-3" />
              <span>Ver .md</span>
            </button>
          </div>
          <div className="p-3 rounded-xl bg-[#111520] border border-white/10 text-xs text-zinc-300 leading-relaxed">
            {agent.description}
          </div>
        </div>

        {/* Assigned Skills */}
        <div className="space-y-2">
          <div className="text-[11px] font-mono text-zinc-400 flex items-center gap-1.5">
            <Wrench className="w-3.5 h-3.5 text-orange-400" />
            <span>SKILLS ASIGNADAS ({agent.skills.length})</span>
          </div>
          <div className="space-y-1.5">
            {agent.skills.map((sk) => (
              <button
                key={sk}
                type="button"
                onClick={() => onOpenFile(`.claude/skills/${sk}/SKILL.md`)}
                className="w-full px-3 py-1.5 rounded-lg bg-[#111520] hover:bg-white/[0.06] border border-white/10 text-left text-xs font-mono text-zinc-200 flex items-center justify-between transition-colors"
              >
                <span className="truncate">{sk}</span>
                <span className="text-[10px] text-orange-400">SKILL.md →</span>
              </button>
            ))}
          </div>
        </div>

        {/* Assigned Tools */}
        <div className="space-y-2">
          <div className="text-[11px] font-mono text-zinc-400">
            HERRAMIENTAS PERMITIDAS ({agent.tools.length})
          </div>
          <div className="p-3 rounded-xl bg-[#111520] border border-white/10 text-xs font-mono text-zinc-300">
            {agent.tools.join(' · ')}
          </div>
        </div>

        {/* Agent Handoffs History */}
        <div className="space-y-2">
          <div className="text-[11px] font-mono text-zinc-400">
            HANDOFFS EN OBSIDIAN ({agentHandoffs.length})
          </div>
          {agentHandoffs.length === 0 ? (
            <div className="p-3 rounded-xl bg-[#111520] border border-white/10 text-xs text-zinc-500">
              Sin relevos registrados aún para este agente.
            </div>
          ) : (
            <div className="space-y-2">
              {agentHandoffs.map((h) => (
                <button
                  key={h.id}
                  type="button"
                  onClick={() => onOpenFile(h.path)}
                  className="w-full p-3 rounded-xl bg-[#111520] hover:border-orange-500/50 border border-white/10 text-left space-y-1 transition-colors"
                >
                  <div className="flex items-center justify-between text-[11px] font-mono text-zinc-400">
                    <span>{h.date}</span>
                    <span className="text-emerald-400">{h.status}</span>
                  </div>
                  <div className="text-xs font-semibold text-zinc-200 flex items-center gap-1.5">
                    <FileText className="w-3.5 h-3.5 text-orange-400 shrink-0" />
                    <span className="truncate">{h.task}</span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </aside>
  );
};
