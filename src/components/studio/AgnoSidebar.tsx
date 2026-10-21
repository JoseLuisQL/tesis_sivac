import React, { useState } from 'react';
import {
  Cpu,
  CheckCircle2,
  AlertCircle,
  RefreshCw,
  Download,
  Lock,
  Search,
  ChevronDown,
  ChevronRight,
  FolderKanban,
  Terminal as TerminalIcon,
} from 'lucide-react';
import type {
  AgentInfo,
  CliToolStatus,
  ResearchProject,
} from '../../types/studio';

interface AgnoSidebarProps {
  agents: AgentInfo[];
  selectedAgentId: string;
  onSelectAgent: (id: string) => void;
  cliStatuses: CliToolStatus[];
  onRefreshCli: () => Promise<void>;
  onCliAction: (tool: 'bun' | 'claude' | 'droid', action: 'verify' | 'install') => Promise<void>;
  projects: ResearchProject[];
  activeProjectId: string;
  onSelectProject: (id: string) => void;
  busyCliTool: string | null;
}

export const AgnoSidebar: React.FC<AgnoSidebarProps> = ({
  agents,
  selectedAgentId,
  onSelectAgent,
  cliStatuses,
  onRefreshCli,
  onCliAction,
  projects,
  activeProjectId,
  onSelectProject,
  busyCliTool,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [collapsedSquads, setCollapsedSquads] = useState<Record<string, boolean>>({});
  const [refreshingCli, setRefreshingCli] = useState(false);

  const handleRefresh = async () => {
    setRefreshingCli(true);
    try {
      await onRefreshCli();
    } finally {
      setRefreshingCli(false);
    }
  };

  const toggleSquad = (squad: string) => {
    setCollapsedSquads((prev) => ({ ...prev, [squad]: !prev[squad] }));
  };

  const filteredAgents = agents.filter((a) => {
    const q = searchQuery.toLowerCase().trim();
    if (!q) return true;
    return (
      a.name.toLowerCase().includes(q) ||
      a.squad.toLowerCase().includes(q) ||
      a.role.toLowerCase().includes(q)
    );
  });

  const groupedSquads = React.useMemo(() => {
    const map = new Map<string, AgentInfo[]>();
    filteredAgents.forEach((agent) => {
      const key = agent.squad || 'General';
      if (!map.has(key)) map.set(key, []);
      map.get(key)!.push(agent);
    });
    return Array.from(map.entries());
  }, [filteredAgents]);

  return (
    <aside className="h-full flex flex-col bg-[#0d1017] border-r border-white/10 select-none overflow-hidden">
      {/* 1. Active Research Project Selector (Agno EntitySelector style) */}
      <div className="p-3.5 border-b border-white/10 space-y-2 shrink-0">
        <div className="flex items-center justify-between text-[11px] font-mono text-zinc-400">
          <span className="flex items-center gap-1.5">
            <FolderKanban className="w-3.5 h-3.5 text-orange-400" />
            <span>PROYECTO ACTIVO</span>
          </span>
          <span>{projects.length} en vault</span>
        </div>

        <select
          value={activeProjectId}
          onChange={(e) => onSelectProject(e.target.value)}
          className="w-full h-9 px-2.5 rounded-lg bg-[#141824] border border-white/10 text-xs font-medium text-zinc-100 focus:outline-none focus:border-orange-500"
        >
          {projects.map((p) => (
            <option key={p.id} value={p.id} className="bg-[#141824] text-zinc-100">
              {p.code} · {p.title}
            </option>
          ))}
        </select>
      </div>

      {/* 2. Live CLI & Runtime Detector (Opcode Binary Dialog + Agno Endpoint Card) */}
      <div className="p-3.5 border-b border-white/10 space-y-2.5 shrink-0">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-mono text-zinc-400 flex items-center gap-1.5">
            <TerminalIcon className="w-3.5 h-3.5 text-orange-400" />
            <span>MOTORES LOCALES CLI</span>
          </span>
          <button
            type="button"
            onClick={handleRefresh}
            className="p-1 rounded hover:bg-white/10 text-zinc-400 hover:text-zinc-100 transition-colors"
            title="Re-escanear binarios locales (Bun, Claude Code, Factory Droid)"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${refreshingCli ? 'animate-spin text-orange-400' : ''}`} />
          </button>
        </div>

        <div className="space-y-1.5">
          {cliStatuses.map((tool) => {
            const isBusy = busyCliTool === tool.id;
            return (
              <div
                key={tool.id}
                className="p-2.5 rounded-lg bg-[#121622] border border-white/10 space-y-1.5"
              >
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-1.5 min-w-0">
                    {tool.installed ? (
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                    ) : (
                      <AlertCircle className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                    )}
                    <span className="text-xs font-semibold text-zinc-100 truncate">
                      {tool.name}
                    </span>
                  </div>
                  <span className="text-[11px] font-mono tabular-nums text-zinc-400 shrink-0">
                    {tool.installed ? tool.version : 'Modo Puente'}
                  </span>
                </div>

                <div className="flex items-center justify-between gap-2 pt-0.5">
                  <span className="text-[10px] font-mono text-zinc-500 truncate">
                    {tool.installed ? tool.path || tool.binary : tool.statusText}
                  </span>

                  <div className="flex items-center gap-1 shrink-0">
                    <button
                      type="button"
                      disabled={isBusy}
                      onClick={() => onCliAction(tool.id, 'verify')}
                      className="px-2 py-0.5 rounded bg-white/[0.06] hover:bg-white/[0.12] text-[10px] font-mono text-zinc-300 transition-colors whitespace-nowrap shrink-0"
                    >
                      Verificar
                    </button>
                    {!tool.installed && (
                      <button
                        type="button"
                        disabled={isBusy}
                        onClick={() => onCliAction(tool.id, 'install')}
                        className="px-2 py-0.5 rounded bg-orange-500/20 hover:bg-orange-500 text-orange-300 hover:text-zinc-950 text-[10px] font-mono font-semibold flex items-center gap-1 transition-colors whitespace-nowrap shrink-0"
                      >
                        <Download className="w-2.5 h-2.5" />
                        <span>Instalar</span>
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 3. Multi-Agent Squad Roster (14 Agents) */}
      <div className="p-3 border-b border-white/10 shrink-0">
        <div className="relative">
          <Search className="w-3.5 h-3.5 text-zinc-500 absolute left-2.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Filtrar 14 agentes o squads..."
            className="w-full h-8 pl-8 pr-2.5 rounded-lg bg-[#141824] border border-white/10 text-xs text-zinc-100 placeholder:text-zinc-500 focus:outline-none focus:border-orange-500"
          />
        </div>
      </div>

      <div className="flex-1 min-h-0 overflow-y-auto p-2.5 space-y-3">
        {groupedSquads.map(([squadName, squadAgents]) => {
          const isCollapsed = !!collapsedSquads[squadName];
          return (
            <div key={squadName} className="space-y-1">
              <button
                type="button"
                onClick={() => toggleSquad(squadName)}
                className="w-full px-2 py-1 flex items-center justify-between text-[11px] font-mono text-zinc-400 hover:text-zinc-200 transition-colors"
              >
                <span className="truncate font-semibold">{squadName}</span>
                <span className="flex items-center gap-1 shrink-0">
                  <span>({squadAgents.length})</span>
                  {isCollapsed ? (
                    <ChevronRight className="w-3 h-3" />
                  ) : (
                    <ChevronDown className="w-3 h-3" />
                  )}
                </span>
              </button>

              {!isCollapsed && (
                <div className="space-y-1">
                  {squadAgents.map((agent) => {
                    const isSelected = selectedAgentId === agent.id;
                    const isGod = agent.id === 'director-general';
                    return (
                      <button
                        key={agent.id}
                        type="button"
                        onClick={() => onSelectAgent(agent.id)}
                        className={`w-full px-2.5 py-2 rounded-lg text-left transition-colors flex items-start justify-between gap-2 ${
                          isSelected
                            ? 'bg-orange-500/15 border border-orange-500/40 text-white'
                            : 'hover:bg-white/[0.04] border border-transparent text-zinc-300'
                        }`}
                      >
                        <div className="min-w-0">
                          <div className="flex items-center gap-1.5">
                            <Cpu
                              className={`w-3.5 h-3.5 shrink-0 ${
                                isGod
                                  ? 'text-orange-400'
                                  : isSelected
                                  ? 'text-orange-300'
                                  : 'text-zinc-500'
                              }`}
                            />
                            <span className="text-xs font-semibold truncate">{agent.name}</span>
                            {agent.readOnly && (
                              <Lock className="w-3 h-3 text-amber-400 shrink-0" />
                            )}
                          </div>
                          <p className="text-[11px] text-zinc-500 truncate pl-5 mt-0.5">
                            {agent.role || agent.description}
                          </p>
                        </div>

                        <span className="text-[10px] font-mono text-zinc-400 shrink-0">
                          {agent.model}
                        </span>
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </aside>
  );
};
