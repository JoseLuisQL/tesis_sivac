import React, { useEffect } from 'react';
import { Command } from 'cmdk';
import {
  Cpu,
  Terminal as TerminalIcon,
  GitBranch,
  Server,
  FolderKanban,
  Play,
  Search,
  X,
} from 'lucide-react';
import type { AgentInfo, McpServerInfo, SkillInfo } from '../../types/studio';

interface CommandPaletteProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  agents: AgentInfo[];
  mcps: McpServerInfo[];
  skills: SkillInfo[];
  onSelectAgent: (id: string) => void;
  onSwitchWorkspace: (tab: 'chat' | 'topology' | 'capabilities' | 'projects') => void;
  onRunCommand: (cmd: string) => Promise<void>;
  onSendGodPrompt: (prompt: string) => Promise<void>;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({
  open,
  onOpenChange,
  agents,
  mcps,
  skills,
  onSelectAgent,
  onSwitchWorkspace,
  onRunCommand,
  onSendGodPrompt,
}) => {
  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        onOpenChange(!open);
      } else if (e.key === 'Escape' && open) {
        onOpenChange(false);
      }
    };
    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, [open, onOpenChange]);

  if (!open) return null;

  return (
    <div
      onClick={() => onOpenChange(false)}
      className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-start justify-center pt-20 p-4"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-2xl rounded-2xl bg-[#111520] border border-white/15 shadow-2xl overflow-hidden"
      >
        <Command className="w-full flex flex-col">
          <div className="flex items-center px-4 border-b border-white/10">
            <Search className="w-4 h-4 text-orange-400 mr-3 shrink-0" />
            <Command.Input
              autoFocus
              placeholder="Comando rápido (⌘K): buscar 14 agentes, ejecutar Bun CLI, cambiar vista o activar MCPs..."
              className="w-full h-12 bg-transparent text-sm text-zinc-100 placeholder:text-zinc-500 focus:outline-none"
            />
            <button
              type="button"
              onClick={() => onOpenChange(false)}
              className="p-1 text-zinc-500 hover:text-zinc-200"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <Command.List className="max-h-[400px] overflow-y-auto p-2 space-y-2 text-xs">
            <Command.Empty className="py-8 text-center text-zinc-500">
              No se encontraron comandos ni agentes para esa búsqueda.
            </Command.Empty>

            <Command.Group
              heading="Vistas del Estudio (Agno + Opcode + LangGraph)"
              className="text-[11px] font-mono text-zinc-500 px-2 py-1"
            >
              {[
                { id: 'chat' as const, label: 'Ir a Consola Chat Agente GOD', icon: Cpu },
                {
                  id: 'topology' as const,
                  label: 'Ir a Grafo Radial React Flow (14 Agentes + F0–F10)',
                  icon: GitBranch,
                },
                {
                  id: 'capabilities' as const,
                  label: 'Ir a Gestor Opcode: MCPs, 17 Skills y Hooks',
                  icon: Server,
                },
                {
                  id: 'projects' as const,
                  label: 'Ir a Proyectos de Investigación y Memoria Obsidian',
                  icon: FolderKanban,
                },
              ].map((item) => {
                const IconComp = item.icon;
                return (
                  <Command.Item
                    key={item.id}
                    value={item.label}
                    onSelect={() => {
                      onSwitchWorkspace(item.id);
                      onOpenChange(false);
                    }}
                    className="px-3 py-2 rounded-lg text-xs text-zinc-200 hover:bg-orange-500/15 hover:text-orange-300 aria-selected:bg-orange-500/15 aria-selected:text-orange-300 flex items-center gap-2.5 cursor-pointer"
                  >
                    <IconComp className="w-3.5 h-3.5 text-orange-400" />
                    <span>{item.label}</span>
                  </Command.Item>
                );
              })}
            </Command.Group>

            <Command.Group
              heading="Comisionar o Inspeccionar Agentes (14 Agentes A–F)"
              className="text-[11px] font-mono text-zinc-500 px-2 py-1"
            >
              {agents.map((ag) => (
                <Command.Item
                  key={ag.id}
                  value={`${ag.name} ${ag.squad} ${ag.role}`}
                  onSelect={() => {
                    onSelectAgent(ag.id);
                    onOpenChange(false);
                  }}
                  className="px-3 py-2 rounded-lg text-xs text-zinc-200 hover:bg-white/10 aria-selected:bg-white/10 flex items-center justify-between gap-2 cursor-pointer"
                >
                  <div className="flex items-center gap-2 min-w-0">
                    <Cpu className="w-3.5 h-3.5 text-orange-400 shrink-0" />
                    <span className="font-mono font-semibold text-white">{ag.name}</span>
                    <span className="text-zinc-500">·</span>
                    <span className="text-zinc-400 truncate">{ag.role}</span>
                  </div>
                  <span className="font-mono text-[10px] text-zinc-500 shrink-0">
                    {ag.squad.split('(')[0].trim()} · {ag.model}
                  </span>
                </Command.Item>
              ))}
            </Command.Group>

            <Command.Group
              heading="Comandos Directos en Terminal XTerm.js + Bun Shell"
              className="text-[11px] font-mono text-zinc-500 px-2 py-1"
            >
              {[
                { label: 'Verificar versión de Bun Runtime', cmd: 'bun --version' },
                { label: 'Verificar instalación de Claude Code CLI', cmd: 'claude --version' },
                { label: 'Verificar instalación de Factory Droid CLI', cmd: 'droid --version' },
                {
                  label: 'Listar contratos de subagentes (.claude/agents)',
                  cmd: 'ls -la .claude/agents',
                },
                {
                  label: 'Ejecutar orden de diagnóstico F1 con Agente GOD',
                  prompt:
                    'Ejecuta la auditoría de brechas F1 entre PROYECTO_TESIS.docx y los modelos UNAJMA.',
                },
              ].map((action) => (
                <Command.Item
                  key={action.label}
                  value={action.label}
                  onSelect={() => {
                    if (action.cmd) {
                      onRunCommand(action.cmd);
                    } else if (action.prompt) {
                      onSendGodPrompt(action.prompt);
                    }
                    onOpenChange(false);
                  }}
                  className="px-3 py-2 rounded-lg text-xs text-zinc-200 hover:bg-white/10 aria-selected:bg-white/10 flex items-center justify-between gap-2 cursor-pointer"
                >
                  <div className="flex items-center gap-2">
                    {action.cmd ? (
                      <TerminalIcon className="w-3.5 h-3.5 text-emerald-400" />
                    ) : (
                      <Play className="w-3.5 h-3.5 text-orange-400" />
                    )}
                    <span>{action.label}</span>
                  </div>
                  {action.cmd && (
                    <span className="font-mono text-[10px] text-zinc-500">$ {action.cmd}</span>
                  )}
                </Command.Item>
              ))}
            </Command.Group>

            <Command.Group
              heading={`Servidores MCP (${mcps.length}) y Skills (${skills.length})`}
              className="text-[11px] font-mono text-zinc-500 px-2 py-1"
            >
              {mcps.map((m) => (
                <Command.Item
                  key={m.id}
                  value={`mcp ${m.name} ${m.command}`}
                  onSelect={() => {
                    onSwitchWorkspace('capabilities');
                    onOpenChange(false);
                  }}
                  className="px-3 py-2 rounded-lg text-xs text-zinc-300 hover:bg-white/10 aria-selected:bg-white/10 flex items-center justify-between cursor-pointer"
                >
                  <span>MCP Server: {m.name}</span>
                  <span className="font-mono text-[10px] text-zinc-500">
                    {m.enabled ? 'Activo' : 'Inactivo'}
                  </span>
                </Command.Item>
              ))}
            </Command.Group>
          </Command.List>
        </Command>
      </div>
    </div>
  );
};
