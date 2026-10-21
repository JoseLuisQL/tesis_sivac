import React, { useMemo, useState } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  Handle,
  Position,
  BackgroundVariant,
  MarkerType,
  type Node,
  type Edge,
  type NodeProps,
} from '@xyflow/react';
import {
  Cpu,
  Play,
  CheckCircle2,
  Clock,
  FileText,
  Lock,
  GitBranch,
  Layers,
  Sparkles,
  ArrowUpRight,
} from 'lucide-react';
import type {
  AgentInfo,
  PhaseInfo,
  HandoffInfo,
  SubagentDelegation,
} from '../../types/studio';

interface HubNodeData extends Record<string, unknown> {
  agent: AgentInfo;
  activeDelegationsCount: number;
  isSelected: boolean;
  onSelect: (id: string) => void;
}

interface SubagentNodeData extends Record<string, unknown> {
  agent: AgentInfo;
  squadShort: string;
  squadColor: string;
  status: 'idle' | 'running' | 'completed';
  lastTask?: string;
  isSelected: boolean;
  onSelect: (id: string) => void;
  onCommission: (agent: AgentInfo) => void;
}

const HubAgentNode: React.FC<NodeProps<Node<HubNodeData>>> = ({ data }) => {
  return (
    <div
      onClick={() => data.onSelect(data.agent.id)}
      className={`w-[270px] rounded-xl bg-[#111520] border transition-all cursor-pointer p-4 shadow-2xl ${
        data.isSelected
          ? 'border-orange-500 ring-2 ring-orange-500/25'
          : 'border-orange-500/50 hover:border-orange-400'
      }`}
    >
      <Handle type="source" position={Position.Top} id="top" className="!bg-orange-500 !w-2.5 !h-2.5" />
      <Handle type="source" position={Position.Bottom} id="bottom" className="!bg-orange-500 !w-2.5 !h-2.5" />
      <Handle type="source" position={Position.Left} id="left" className="!bg-orange-500 !w-2.5 !h-2.5" />
      <Handle type="source" position={Position.Right} id="right" className="!bg-orange-500 !w-2.5 !h-2.5" />

      <div className="flex items-center justify-between text-[11px] text-orange-300 font-mono mb-1.5">
        <span>HUB CENTRAL · ORQUESTADOR</span>
        <span>{data.agent.model}</span>
      </div>

      <div className="text-sm font-bold text-white tracking-tight flex items-center gap-2">
        <Cpu className="w-4 h-4 text-orange-400 shrink-0" />
        <span className="truncate">{data.agent.name}</span>
      </div>

      <p className="mt-1.5 text-xs text-zinc-400 line-clamp-2 leading-relaxed">
        Director de Tesis Senior (Agente GOD). Refinamiento cognitivo, memoria viva en Obsidian y delegación radial.
      </p>

      <div className="mt-3 pt-2.5 border-t border-white/10 flex items-center justify-between text-[11px] font-mono text-zinc-300">
        <span>13 Subagentes A–F</span>
        <span className="text-orange-400 font-semibold">
          {data.activeDelegationsCount > 0
            ? `${data.activeDelegationsCount} en ejecución`
            : 'Listo para delegar'}
        </span>
      </div>
    </div>
  );
};

const SubagentNode: React.FC<NodeProps<Node<SubagentNodeData>>> = ({ data }) => {
  const { agent, squadShort, squadColor, status, isSelected, onSelect, onCommission } = data;

  return (
    <div
      onClick={() => onSelect(agent.id)}
      className={`w-[225px] rounded-xl bg-[#0e1118] border transition-all cursor-pointer p-3 ${
        isSelected
          ? 'border-orange-400 ring-1 ring-orange-400/30 bg-[#141824]'
          : status === 'running'
          ? 'border-amber-400/70 bg-[#151722]'
          : status === 'completed'
          ? 'border-emerald-500/50'
          : 'border-white/10 hover:border-white/25'
      }`}
    >
      <Handle type="target" position={Position.Top} id="t-top" className="!bg-zinc-500 !w-2 !h-2" />
      <Handle type="target" position={Position.Bottom} id="t-bottom" className="!bg-zinc-500 !w-2 !h-2" />
      <Handle type="target" position={Position.Left} id="t-left" className="!bg-zinc-500 !w-2 !h-2" />
      <Handle type="target" position={Position.Right} id="t-right" className="!bg-zinc-500 !w-2 !h-2" />

      <div className="flex items-center justify-between text-[11px] text-zinc-400 font-mono mb-1">
        <span style={{ color: squadColor }} className="font-semibold">
          {squadShort}
        </span>
        <span>
          {agent.model} · {status === 'running' ? 'Ejecutando' : status === 'completed' ? 'Completado' : 'Listo'}
        </span>
      </div>

      <div className="text-xs font-semibold text-zinc-100 flex items-center justify-between gap-1.5">
        <span className="truncate">{agent.name}</span>
        {agent.readOnly && (
          <span title="Solo Lectura">
            <Lock className="w-3 h-3 text-amber-400 shrink-0" />
          </span>
        )}
      </div>

      <p className="mt-1 text-[11px] text-zinc-400 line-clamp-2 leading-snug">
        {agent.role || agent.description}
      </p>

      <div className="mt-2.5 pt-2 border-t border-white/10 flex items-center justify-between gap-2">
        <span className="text-[10px] font-mono text-zinc-500 truncate">
          {agent.skills.length} skills · {agent.tools.length} tools
        </span>
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            onCommission(agent);
          }}
          className="px-2 py-1 rounded bg-white/[0.06] hover:bg-orange-500 hover:text-zinc-950 text-[11px] font-medium text-zinc-200 flex items-center gap-1 transition-colors whitespace-nowrap shrink-0"
        >
          <Play className="w-2.5 h-2.5 fill-current" />
          <span>Comisionar</span>
        </button>
      </div>
    </div>
  );
};

const nodeTypes = {
  hubNode: HubAgentNode,
  subagentNode: SubagentNode,
};

interface AgentFlowCanvasProps {
  agents: AgentInfo[];
  phases: PhaseInfo[];
  handoffs: HandoffInfo[];
  delegations: SubagentDelegation[];
  selectedAgentId: string;
  onSelectAgent: (id: string) => void;
  onCommissionAgent: (agent: AgentInfo, customTask?: string) => void;
  onOpenVaultFile: (path: string) => void;
}

const SQUAD_COLORS: Record<string, string> = {
  'Squad A': '#38bdf8',
  'Squad B': '#a78bfa',
  'Squad C': '#34d399',
  'Squad D': '#fbbf24',
  'Squad E': '#f472b6',
  'Squad F': '#fb923c',
};

export const AgentFlowCanvas: React.FC<AgentFlowCanvasProps> = ({
  agents,
  phases,
  handoffs,
  delegations,
  selectedAgentId,
  onSelectAgent,
  onCommissionAgent,
  onOpenVaultFile,
}) => {
  const [subTab, setSubTab] = useState<'graph' | 'phases'>('graph');
  const [squadFilter, setSquadFilter] = useState<string>('ALL');

  const hubAgent = useMemo(
    () =>
      agents.find((a) => a.id === 'director-general') || {
        id: 'director-general',
        name: 'director-general',
        squad: 'Hub Central',
        role: 'Director de Tesis Senior / Agente GOD',
        model: 'opus',
        description: 'Orquestador Maestro de la Constitución',
        tools: ['Read', 'Write', 'Edit', 'Bash', 'Agent', 'Skill'],
        skills: ['academic-pipeline', 'protocolo-obsidian-handoff', 'matriz-consistencia'],
        filePath: '.claude/agents/director-general.md',
      },
    [agents]
  );

  const subagents = useMemo(
    () =>
      agents
        .filter((a) => a.id !== 'director-general')
        .filter((a) => (squadFilter === 'ALL' ? true : a.squad.startsWith(squadFilter))),
    [agents, squadFilter]
  );

  const activeDelegationsCount = useMemo(
    () => delegations.filter((d) => d.status === 'running' || d.status === 'queued').length,
    [delegations]
  );

  // Build React Flow nodes & edges in a clean radial elliptical topology
  const { nodes, edges } = useMemo(() => {
    const centerX = 560;
    const centerY = 340;
    const radiusX = 450;
    const radiusY = 275;

    const flowNodes: Node[] = [
      {
        id: hubAgent.id,
        type: 'hubNode',
        position: { x: centerX - 135, y: centerY - 80 },
        data: {
          agent: hubAgent,
          activeDelegationsCount,
          isSelected: selectedAgentId === hubAgent.id,
          onSelect: onSelectAgent,
        },
      },
    ];

    const flowEdges: Edge[] = [];
    const total = subagents.length || 1;

    subagents.forEach((agent, index) => {
      const angle = (2 * Math.PI * index) / total - Math.PI / 2;
      const x = Math.round(centerX + radiusX * Math.cos(angle) - 112);
      const y = Math.round(centerY + radiusY * Math.sin(angle) - 64);

      const squadKey =
        Object.keys(SQUAD_COLORS).find((k) => agent.squad.startsWith(k)) || 'Squad A';
      const color = SQUAD_COLORS[squadKey] || '#f97316';

      const agentDelegation = delegations.find((d) => d.agentId === agent.id);
      const hasHandoff = handoffs.some((h) => h.agent === agent.id);
      const status: 'idle' | 'running' | 'completed' =
        agentDelegation?.status === 'running' || agentDelegation?.status === 'queued'
          ? 'running'
          : agentDelegation?.status === 'completed' || hasHandoff
          ? 'completed'
          : 'idle';

      // Choose handles based on angle quadrant
      let sourceHandle = 'top';
      let targetHandle = 't-bottom';
      const deg = ((angle * 180) / Math.PI + 360) % 360;
      if (deg >= 315 || deg < 45) {
        sourceHandle = 'right';
        targetHandle = 't-left';
      } else if (deg >= 45 && deg < 135) {
        sourceHandle = 'bottom';
        targetHandle = 't-top';
      } else if (deg >= 135 && deg < 225) {
        sourceHandle = 'left';
        targetHandle = 't-right';
      } else {
        sourceHandle = 'top';
        targetHandle = 't-bottom';
      }

      flowNodes.push({
        id: agent.id,
        type: 'subagentNode',
        position: { x, y },
        data: {
          agent,
          squadShort: squadKey,
          squadColor: color,
          status,
          lastTask: agentDelegation?.task,
          isSelected: selectedAgentId === agent.id,
          onSelect: onSelectAgent,
          onCommission: (ag: AgentInfo) => onCommissionAgent(ag),
        },
      });

      const isEdgeActive = status === 'running' || selectedAgentId === agent.id;

      flowEdges.push({
        id: `edge-${hubAgent.id}-${agent.id}`,
        source: hubAgent.id,
        target: agent.id,
        sourceHandle,
        targetHandle,
        animated: isEdgeActive,
        style: {
          stroke: isEdgeActive ? '#f97316' : color,
          strokeWidth: isEdgeActive ? 2.2 : 1.2,
          opacity: isEdgeActive ? 0.95 : 0.45,
        },
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: isEdgeActive ? '#f97316' : color,
        },
      });
    });

    return { nodes: flowNodes, edges: flowEdges };
  }, [hubAgent, subagents, delegations, handoffs, selectedAgentId, activeDelegationsCount, onSelectAgent, onCommissionAgent]);

  return (
    <div className="h-full flex flex-col bg-[#0b0d12]">
      {/* Sub-toolbar for Mission Control */}
      <div className="h-11 px-4 border-b border-white/10 flex items-center justify-between gap-4 bg-[#0f1219] shrink-0">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1 bg-black/40 p-1 rounded-lg border border-white/10">
            <button
              type="button"
              onClick={() => setSubTab('graph')}
              className={`px-3 py-1 rounded-md text-xs font-medium flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0 ${
                subTab === 'graph'
                  ? 'bg-orange-500 text-zinc-950 font-semibold'
                  : 'text-zinc-400 hover:text-zinc-100'
              }`}
            >
              <GitBranch className="w-3.5 h-3.5" />
              <span>Grafo Radial React Flow (14 Agentes)</span>
            </button>
            <button
              type="button"
              onClick={() => setSubTab('phases')}
              className={`px-3 py-1 rounded-md text-xs font-medium flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0 ${
                subTab === 'phases'
                  ? 'bg-orange-500 text-zinc-950 font-semibold'
                  : 'text-zinc-400 hover:text-zinc-100'
              }`}
            >
              <Layers className="w-3.5 h-3.5" />
              <span>Fases F0–F10 · Quality Gates · Handoffs ({handoffs.length})</span>
            </button>
          </div>
        </div>

        {subTab === 'graph' && (
          <div className="flex items-center gap-1 overflow-x-auto">
            {['ALL', 'Squad A', 'Squad B', 'Squad C', 'Squad D', 'Squad E', 'Squad F'].map(
              (sq) => (
                <button
                  key={sq}
                  type="button"
                  onClick={() => setSquadFilter(sq)}
                  className={`px-2.5 py-1 rounded text-xs font-mono transition-colors whitespace-nowrap shrink-0 ${
                    squadFilter === sq
                      ? 'bg-white/15 text-white font-semibold'
                      : 'text-zinc-400 hover:text-zinc-200 hover:bg-white/5'
                  }`}
                >
                  {sq === 'ALL' ? 'Todos (14)' : sq}
                </button>
              )
            )}
          </div>
        )}
      </div>

      {/* Main Content Area */}
      {subTab === 'graph' ? (
        <div className="flex-1 min-h-0 relative">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            nodeTypes={nodeTypes}
            fitView
            fitViewOptions={{ padding: 0.16 }}
            minZoom={0.35}
            maxZoom={1.6}
            proOptions={{ hideAttribution: true }}
          >
            <Background
              variant={BackgroundVariant.Dots}
              gap={22}
              size={1.2}
              color="rgba(255, 255, 255, 0.1)"
            />
            <Controls position="bottom-left" />
            <MiniMap
              position="bottom-right"
              nodeColor={(n) =>
                n.type === 'hubNode' ? '#f97316' : (n.data?.squadColor as string) || '#52525b'
              }
              maskColor="rgba(9, 11, 16, 0.75)"
            />
          </ReactFlow>

          {/* Floating Legend Overlay */}
          <div className="absolute top-3 left-3 bg-[#0f1219]/90 backdrop-blur-md border border-white/10 rounded-lg px-3 py-2 pointer-events-none">
            <div className="text-xs font-semibold text-zinc-200">
              01. Topología Radial Hub-and-Spoke (@xyflow/react)
            </div>
            <div className="text-[11px] text-zinc-400 mt-0.5">
              Arrastra el lienzo, haz zoom o selecciona cualquier nodo para inspeccionar o comisionar tareas reales.
            </div>
          </div>
        </div>
      ) : (
        <div className="flex-1 min-h-0 overflow-y-auto p-6 space-y-8">
          {/* Phases F0-F10 Table */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-base font-semibold text-zinc-100">
                  01. Pipeline Metodológico F0–F10 y Compuertas de Calidad (QG-0 a QG-9)
                </h2>
                <p className="text-xs text-zinc-400 mt-0.5">
                  Sincronizado en vivo con obsidian_vault/00_SISTEMA/ESTADO_TESIS.md
                </p>
              </div>
              <button
                type="button"
                onClick={() => onOpenVaultFile('00_SISTEMA/ESTADO_TESIS.md')}
                className="px-3 py-1.5 rounded-lg bg-white/[0.06] hover:bg-white/[0.12] text-xs font-medium text-zinc-200 flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0"
              >
                <FileText className="w-3.5 h-3.5 text-orange-400" />
                <span>Abrir ESTADO_TESIS.md</span>
                <ArrowUpRight className="w-3.5 h-3.5" />
              </button>
            </div>

            <div className="border border-white/10 rounded-xl overflow-hidden bg-[#0f1219]">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-white/10 text-[11px] font-mono text-zinc-400 bg-black/20">
                    <th className="py-2.5 px-4">Fase</th>
                    <th className="py-2.5 px-4">Nombre de Etapa</th>
                    <th className="py-2.5 px-4">Quality Gate</th>
                    <th className="py-2.5 px-4">Entregable Canónico</th>
                    <th className="py-2.5 px-4 text-right">Avance</th>
                    <th className="py-2.5 px-4 text-right">Estado</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5 text-xs">
                  {phases.map((phase) => (
                    <tr key={phase.id} className="hover:bg-white/[0.02] transition-colors">
                      <td className="py-2.5 px-4 font-mono font-semibold text-orange-400">
                        {phase.id}
                      </td>
                      <td className="py-2.5 px-4 font-medium text-zinc-200">{phase.name}</td>
                      <td className="py-2.5 px-4 font-mono text-zinc-400">{phase.gate}</td>
                      <td className="py-2.5 px-4 text-zinc-400">{phase.deliverable}</td>
                      <td className="py-2.5 px-4 text-right font-mono tabular-nums text-zinc-200">
                        {phase.progress}%
                      </td>
                      <td className="py-2.5 px-4 text-right font-mono">
                        {phase.status === 'completado' ? (
                          <span className="text-emerald-400 inline-flex items-center gap-1 justify-end">
                            <CheckCircle2 className="w-3.5 h-3.5" />
                            <span>Completado</span>
                          </span>
                        ) : phase.status === 'en_progreso' ? (
                          <span className="text-amber-400 inline-flex items-center gap-1 justify-end">
                            <Sparkles className="w-3.5 h-3.5" />
                            <span>En curso</span>
                          </span>
                        ) : (
                          <span className="text-zinc-500 inline-flex items-center gap-1 justify-end">
                            <Clock className="w-3.5 h-3.5" />
                            <span>Pendiente</span>
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Handoffs Registry */}
          <div>
            <div className="mb-4">
              <h2 className="text-base font-semibold text-zinc-100">
                02. Relevos y Contratos de Handoff en Obsidian (08_SISTEMA_Y_AGENTES/handoffs)
              </h2>
              <p className="text-xs text-zinc-400 mt-0.5">
                Reportes depositados por los subagentes al concluir cada comisión radial
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {handoffs.map((h) => (
                <div
                  key={h.id}
                  onClick={() => onOpenVaultFile(h.path)}
                  className="p-4 rounded-xl bg-[#0f1219] border border-white/10 hover:border-orange-500/50 transition-colors cursor-pointer"
                >
                  <div className="flex items-center justify-between text-xs text-zinc-400 font-mono mb-1.5">
                    <span>
                      {h.agent} · {h.date}
                    </span>
                    <span className="text-emerald-400">{h.status}</span>
                  </div>
                  <div className="text-sm font-semibold text-zinc-100 mb-1">{h.task}</div>
                  <p className="text-xs text-zinc-400 line-clamp-2 leading-relaxed">
                    {h.summary}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
