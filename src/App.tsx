import React, { useEffect, useState, useMemo } from 'react';
import { Group, Panel, Separator } from 'react-resizable-panels';
import {
  FileCode2,
  X,
  RefreshCw,
} from 'lucide-react';
import type {
  AgentInfo,
  SkillInfo,
  McpServerInfo,
  HookInfo,
  PhaseInfo,
  HandoffInfo,
  TerminalLog,
  CliToolStatus,
  SubagentDelegation,
  GodChatMessage,
  ResearchProject,
  EcosystemData,
} from './types/studio';
import { AgnoSidebar } from './components/studio/AgnoSidebar';
import { AgnoChatArea } from './components/studio/AgnoChatArea';
import { AgentFlowCanvas } from './components/studio/AgentFlowCanvas';
import { OpcodeCapabilities } from './components/studio/OpcodeCapabilities';
import { ObsidianWorkspace } from './components/studio/ObsidianWorkspace';
import { XTermConsole } from './components/studio/XTermConsole';
import { AgentInspectorPanel } from './components/studio/AgentInspectorPanel';
import { CommandPalette } from './components/studio/CommandPalette';

// --- NORMALIZERS FOR BACKEND PAYLOADS ---
function normalizeEcosystem(raw: any): EcosystemData {
  const agentsRaw = Array.isArray(raw?.agents) ? raw.agents : [];
  const agents: AgentInfo[] = agentsRaw.map((a: any) => ({
    id: String(a.id || a.name || 'agent'),
    name: String(a.name || a.id || 'agent'),
    squad: String(a.squad || 'General'),
    role: String(a.role || a.description || ''),
    model: String(a.model || 'sonnet'),
    description: String(a.description || a.role || ''),
    tools: Array.isArray(a.tools) ? a.tools : [],
    skills: Array.isArray(a.skills) ? a.skills : [],
    filePath: String(a.filePath || `.claude/agents/${a.id || a.name}.md`),
    readOnly: Boolean(a.readOnly || a.id === 'ingeniero-sivac'),
  }));

  const skillsRaw = Array.isArray(raw?.skills) ? raw.skills : [];
  const skills: SkillInfo[] = skillsRaw.map((s: any) => ({
    id: String(s.id || s.name || ''),
    name: String(s.name || s.id || ''),
    description: String(s.description || ''),
    path: String(s.path || s.filePath || `.claude/skills/${s.id || s.name}/SKILL.md`),
    enabled: s.enabled !== false,
  }));

  const mcpsRaw = Array.isArray(raw?.mcps) ? raw.mcps : [];
  const mcps: McpServerInfo[] = mcpsRaw.map((m: any) => ({
    id: String(m.id || m.name || ''),
    name: String(m.name || m.id || ''),
    command: String(m.command || 'npx'),
    args: Array.isArray(m.args) ? m.args : [],
    enabled: Boolean(m.enabled),
    type: String(m.type || 'stdio'),
  }));

  const hooksRaw = Array.isArray(raw?.hooks) ? raw.hooks : [];
  const hooks: HookInfo[] = hooksRaw.map((h: any, idx: number) => ({
    id: String(h.id || h.event || `hook-${idx}`),
    event: String(h.event || h.id || 'PreToolUse'),
    matcher: String(h.matcher || '*'),
    command: String(h.command || ''),
    enabled: Boolean(h.enabled),
  }));

  const phasesRaw = Array.isArray(raw?.phases) ? raw.phases : [];
  const phases: PhaseInfo[] = phasesRaw.map((p: any) => ({
    id: String(p.id || 'F0'),
    name: String(p.name || ''),
    gate: String(p.gate || 'QG'),
    progress: Number(p.progress ?? 0),
    status:
      p.status === 'completado' || p.status === 'en_progreso' ? p.status : 'pendiente',
    deliverable: String(p.deliverable || ''),
  }));

  const handoffsRaw = Array.isArray(raw?.handoffs) ? raw.handoffs : [];
  const handoffs: HandoffInfo[] = handoffsRaw.map((h: any, idx: number) => ({
    id: String(h.id || h.filename || `handoff-${idx}`),
    filename: String(h.filename || ''),
    agent: String(h.agent || ''),
    task: String(h.task || h.filename || ''),
    date: String(h.date || ''),
    status: String(h.status || 'completado'),
    summary: String(h.summary || ''),
    path: String(h.path || `08_SISTEMA_Y_AGENTES/handoffs/${h.filename || ''}`),
    rawContent: String(h.rawContent || ''),
  }));

  const completedPhases = phases.filter((p) => p.status === 'completado').length;
  const computedProgress =
    phases.length > 0 ? Math.round((completedPhases / phases.length) * 100) : 15;

  return {
    thesisTitle: String(
      raw?.thesis?.title ||
        raw?.thesisTitle ||
        'Sistema Informático Web SIVAC y Gestión de Inventario en SYNCOVA S.A.C.'
    ),
    university: String(
      raw?.thesis?.university || raw?.university || 'UNAJMA — Ingeniería de Sistemas'
    ),
    methodology: String(
      raw?.thesis?.methodology ||
        raw?.methodology ||
        'Extreme Programming (XP) · ISO/IEC 25010 · TAM'
    ),
    currentPhase: String(raw?.thesis?.currentPhase || raw?.currentPhase || 'F1'),
    globalProgress: Number(
      raw?.stats?.globalProgress ?? raw?.globalProgress ?? computedProgress
    ),
    agents,
    skills,
    mcps,
    hooks,
    phases,
    handoffs,
    vaultFiles: Array.isArray(raw?.vaultFiles) ? raw.vaultFiles : [],
    decisionsRaw: String(raw?.decisionsRaw || ''),
    estadoRaw: String(raw?.estadoRaw || ''),
  };
}

function normalizeCliStatuses(raw: any): CliToolStatus[] {
  if (Array.isArray(raw?.tools)) return raw.tools;
  const list: CliToolStatus[] = [];
  const entries: Array<['bun' | 'claude' | 'droid', string, string]> = [
    ['bun', 'Bun Runtime & Shell', 'curl -fsSL https://bun.sh/install | bash'],
    ['claude', 'Claude Code CLI', 'bun add -g @anthropic-ai/claude-code'],
    ['droid', 'Factory Droid CLI', 'curl -fsSL https://app.factory.ai/cli | sh'],
  ];
  for (const [id, defaultName, defaultInstall] of entries) {
    const item = raw?.[id];
    if (item && typeof item === 'object') {
      list.push({
        id,
        name: String(item.name || defaultName),
        binary: String(item.binary || id),
        installed: Boolean(item.installed),
        version: String(item.version || (item.installed ? 'instalado' : 'Modo Puente')),
        path: String(item.path || ''),
        statusText: String(
          item.mode === 'native' || item.installed
            ? 'Binario Nativo Detectado'
            : 'Bridge Local Activo'
        ),
        installCommand: String(item.installCmd || item.installCommand || defaultInstall),
        docsUrl: String(item.docsUrl || ''),
      });
    }
  }
  return list;
}

function normalizeGodChatMessage(m: any): GodChatMessage {
  const delegationsRaw = Array.isArray(m?.delegations) ? m.delegations : [];
  const delegations: SubagentDelegation[] = delegationsRaw.map((d: any, i: number) => ({
    id: String(d.id || `del-${i}`),
    agentId: String(d.subagent || d.agentId || 'investigador-bibliografico'),
    agentName: String(d.subagent || d.agentName || 'investigador-bibliografico'),
    squad: String(d.squad || 'Squad'),
    task: String(d.task || ''),
    engine: d.engine === 'droid' || d.engine === 'bun' ? d.engine : 'claude',
    status:
      d.status === 'running' ||
      d.status === 'completed' ||
      d.status === 'error' ||
      d.status === 'queued'
        ? d.status
        : 'completed',
    command: String(d.command || ''),
    outputSummary: String(d.outputSummary || d.output || ''),
    handoffFile: d.handoffPath || d.handoffFile || undefined,
    startedAt: String(d.startedAt || m?.timestamp || new Date().toISOString()),
    completedAt: d.completedAt ? String(d.completedAt) : undefined,
  }));

  return {
    id: String(m?.id || `msg-${Date.now()}`),
    role: m?.role === 'user' ? 'user' : 'god',
    content: String(m?.content || ''),
    timestamp: String(m?.timestamp || new Date().toISOString()),
    engineUsed: m?.engineUsed ? String(m.engineUsed) : 'Bun Shell + Agente GOD',
    cognitiveRefinement: m?.refinement
      ? {
          intent: String(m.refinement.detectedIntent || m.refinement.intent || ''),
          obsidianContext: Array.isArray(m.refinement.obsidianContextChecked)
            ? m.refinement.obsidianContextChecked.join(' · ')
            : String(m.refinement.obsidianContext || '00_SISTEMA/ESTADO_TESIS.md'),
          formalMethodology: String(
            m.refinement.methodologicalFraming || m.refinement.formalMethodology || ''
          ),
          selectedSquads:
            delegations.length > 0
              ? Array.from(new Set(delegations.map((d) => d.squad)))
              : ['Hub Central'],
        }
      : m?.cognitiveRefinement,
    delegations,
  };
}

function normalizeProjects(raw: any): ResearchProject[] {
  const arr = Array.isArray(raw?.projects)
    ? raw.projects
    : Array.isArray(raw)
    ? raw
    : [];
  return arr.map((p: any, idx: number) => ({
    id: String(p.id || `proj-${idx}`),
    code: String(p.code || p.currentPhase || `PROY-0${idx + 1}`),
    title: String(p.title || p.name || 'Proyecto de Investigación'),
    university: String(p.university || 'UNAJMA'),
    methodology: String(p.methodology || p.design || 'Cuasi-experimental'),
    sampleSize: String(p.sampleSize || p.population || 'n=14'),
    progress: Number(p.progress ?? 15),
    status:
      p.status === 'completado' || p.status === 'planificacion' ? p.status : 'activo',
    leadAgent: String(p.leadAgent || 'director-general'),
    updatedAt: String(p.updatedAt || '2026-10-20'),
    obsidianPath: String(p.obsidianPath || '00_SISTEMA/ESTADO_TESIS.md'),
    tasks: Array.isArray(p.tasks)
      ? p.tasks.map((t: any, tIdx: number) => ({
          id: String(t.id || `task-${tIdx}`),
          title: String(t.title || ''),
          phase: String(t.phase || 'F1'),
          assignedAgent: String(t.assignedAgent || t.agent || 'director-general'),
          status:
            t.status === 'completado' || t.status === 'en_progreso'
              ? t.status
              : 'pendiente',
        }))
      : [],
  }));
}

export function App() {
  const [ecosystem, setEcosystem] = useState<EcosystemData | null>(null);
  const [projects, setProjects] = useState<ResearchProject[]>([]);
  const [activeProjectId, setActiveProjectId] = useState<string>('sivac-2026');
  const [cliStatuses, setCliStatuses] = useState<CliToolStatus[]>([]);
  const [chatMessages, setChatMessages] = useState<GodChatMessage[]>([]);
  const [terminalLogs, setTerminalLogs] = useState<TerminalLog[]>([]);

  const [activeWorkspace, setActiveWorkspace] = useState<
    'chat' | 'topology' | 'capabilities' | 'projects'
  >('chat');
  const [selectedAgentId, setSelectedAgentId] = useState<string>('director-general');
  const [preferredEngine, setPreferredEngine] = useState<'auto' | 'claude' | 'droid' | 'bun'>(
    'auto'
  );
  const [activeTerminalSession, setActiveTerminalSession] = useState<
    'bun-shell' | 'claude-code' | 'factory-droid'
  >('bun-shell');
  const [isTerminalMinimized, setIsTerminalMinimized] = useState<boolean>(false);
  const [commandPaletteOpen, setCommandPaletteOpen] = useState<boolean>(false);

  const [selectedVaultPath, setSelectedVaultPath] = useState<string>(
    '00_SISTEMA/ESTADO_TESIS.md'
  );
  const [vaultFileContent, setVaultFileContent] = useState<string>('');
  const [modalFilePath, setModalFilePath] = useState<string | null>(null);
  const [modalFileContent, setModalFileContent] = useState<string>('');

  const [isSendingChat, setIsSendingChat] = useState<boolean>(false);
  const [busyCliTool, setBusyCliTool] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchAllData = async () => {
    try {
      const [ecoRes, cliRes, chatRes] = await Promise.all([
        fetch('/api/ecosystem'),
        fetch('/api/system/cli-status'),
        fetch('/api/god-chat'),
      ]);

      if (ecoRes.ok) {
        const rawEco = await ecoRes.json();
        const normEco = normalizeEcosystem(rawEco);
        setEcosystem(normEco);
        if (normEco.estadoRaw && !vaultFileContent) {
          setVaultFileContent(normEco.estadoRaw);
        }
        if (rawEco.projects) {
          const normProjs = normalizeProjects(rawEco.projects);
          setProjects(normProjs);
          if (normProjs.length > 0 && !normProjs.some((p) => p.id === activeProjectId)) {
            setActiveProjectId(normProjs[0].id);
          }
        }
      }

      if (cliRes.ok) {
        const rawCli = await cliRes.json();
        setCliStatuses(normalizeCliStatuses(rawCli));
      }

      if (chatRes.ok) {
        const rawChat = await chatRes.json();
        if (Array.isArray(rawChat?.messages)) {
          setChatMessages(rawChat.messages.map(normalizeGodChatMessage));
        }
      }
    } catch (err) {
      console.error('Error loading studio data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllData();

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    let ws: WebSocket | null = null;

    try {
      ws = new WebSocket(wsUrl);
      ws.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          if (payload.type === 'init') {
            if (Array.isArray(payload.logs)) {
              setTerminalLogs(
                payload.logs.map((l: any, i: number) => ({
                  id: String(l.id || `log-${i}`),
                  timestamp: String(l.timestamp || new Date().toISOString()),
                  session: String(l.session || 'bun-shell'),
                  type: l.stream || l.type || 'stdout',
                  text: String(l.text || ''),
                }))
              );
            }
            if (payload.cliStatus) {
              setCliStatuses(normalizeCliStatuses(payload.cliStatus));
            }
            if (Array.isArray(payload.godChatHistory)) {
              setChatMessages(payload.godChatHistory.map(normalizeGodChatMessage));
            }
          } else if (payload.type === 'terminal:output' || payload.type === 'terminal:line') {
            const entry = payload.entry || payload.data;
            if (entry) {
              setTerminalLogs((prev) => [
                ...prev.slice(-350),
                {
                  id: String(entry.id || `log-${Date.now()}-${Math.random()}`),
                  timestamp: String(entry.timestamp || new Date().toISOString()),
                  session: String(entry.session || 'bun-shell'),
                  type: entry.stream || entry.type || 'stdout',
                  text: String(entry.text || ''),
                },
              ]);
            }
          } else if (payload.type === 'terminal:cleared') {
            setTerminalLogs([]);
          } else if (payload.type === 'godchat:message' && payload.message) {
            const norm = normalizeGodChatMessage(payload.message);
            setChatMessages((prev) => {
              const exists = prev.some((m) => m.id === norm.id);
              return exists ? prev.map((m) => (m.id === norm.id ? norm : m)) : [...prev, norm];
            });
          } else if (payload.type === 'godchat:update' && payload.message) {
            const norm = normalizeGodChatMessage(payload.message);
            setChatMessages((prev) => prev.map((m) => (m.id === norm.id ? norm : m)));
          } else if (payload.type === 'cli:status' && payload.status) {
            setCliStatuses(normalizeCliStatuses(payload.status));
          } else if (payload.type === 'ecosystem:refresh') {
            fetchAllData();
          }
        } catch {
          // ignore malformed ws message
        }
      };
    } catch {
      // ignore ws connection error
    }

    return () => {
      if (ws) ws.close();
    };
  }, []);

  const selectedAgent = useMemo(() => {
    if (!ecosystem) return null;
    return (
      ecosystem.agents.find((a) => a.id === selectedAgentId) ||
      ecosystem.agents[0] ||
      null
    );
  }, [ecosystem, selectedAgentId]);

  const allDelegations = useMemo(() => {
    const list: SubagentDelegation[] = [];
    chatMessages.forEach((m) => {
      if (m.delegations) list.push(...m.delegations);
    });
    return list;
  }, [chatMessages]);

  // --- HANDLERS ---
  const handleSendGodMessage = async (
    prompt: string,
    engine: 'auto' | 'claude' | 'droid' | 'bun' = preferredEngine
  ) => {
    setIsSendingChat(true);
    try {
      const res = await fetch('/api/god-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, engine }),
      });
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data?.history)) {
          setChatMessages(data.history.map(normalizeGodChatMessage));
        }
        await fetchAllData();
      }
    } finally {
      setIsSendingChat(false);
    }
  };

  const handleClearGodChat = async () => {
    const res = await fetch('/api/god-chat', { method: 'DELETE' });
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data?.messages)) {
        setChatMessages(data.messages.map(normalizeGodChatMessage));
      }
    }
  };

  const handleExecuteTerminalCommand = async (
    command: string,
    session: string = activeTerminalSession
  ) => {
    if (isTerminalMinimized) setIsTerminalMinimized(false);
    await fetch('/api/terminal/exec', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command, session }),
    });
  };

  const handleClearTerminal = async () => {
    await fetch('/api/terminal/clear', { method: 'POST' });
    setTerminalLogs([]);
  };

  const handleRefreshCli = async () => {
    const res = await fetch('/api/system/cli-status');
    if (res.ok) {
      const raw = await res.json();
      setCliStatuses(normalizeCliStatuses(raw));
    }
  };

  const handleCliAction = async (
    tool: 'bun' | 'claude' | 'droid',
    action: 'verify' | 'install'
  ) => {
    setBusyCliTool(tool);
    if (isTerminalMinimized) setIsTerminalMinimized(false);
    try {
      const res = await fetch('/api/system/cli-action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tool, action }),
      });
      if (res.ok) {
        const data = await res.json();
        if (data?.status) {
          setCliStatuses(normalizeCliStatuses(data.status));
        } else {
          await handleRefreshCli();
        }
      }
    } finally {
      setBusyCliTool(null);
    }
  };

  const handleCommissionAgent = async (
    agent: AgentInfo,
    customTask?: string,
    engine: 'claude' | 'droid' | 'bun' = 'claude'
  ) => {
    const taskText =
      customTask ||
      `Ejecutar auditoría y entregable canónico del rol ${agent.role} (${agent.squad}) según ESTADO_TESIS.md`;
    if (isTerminalMinimized) setIsTerminalMinimized(false);
    await fetch('/api/agent/commission', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        subagent: agent.id,
        squad: agent.squad,
        phase: ecosystem?.currentPhase || 'F1',
        task: taskText,
        engine,
        inputs: 'obsidian_vault/00_SISTEMA/ESTADO_TESIS.md',
        expectedOutput: `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${new Date()
          .toISOString()
          .slice(0, 10)}_${agent.id}.md`,
      }),
    });
    await fetchAllData();
  };

  const handleToggleMcp = async (id: string, enabled: boolean) => {
    await fetch('/api/capabilities/mcp', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: id, id, enabled }),
    });
    await fetchAllData();
  };

  const handleToggleSkill = async (id: string, enabled: boolean) => {
    await fetch('/api/capabilities/skill', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, enabled }),
    });
    await fetchAllData();
  };

  const handleToggleHook = async (id: string, enabled: boolean) => {
    await fetch('/api/capabilities/hook', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ hookEvent: id, id, enabled }),
    });
    await fetchAllData();
  };

  const handleSelectVaultFile = async (filePath: string) => {
    const clean = filePath.replace(/^obsidian_vault\//, '');
    setSelectedVaultPath(clean);
    const res = await fetch(`/api/vault/file?path=${encodeURIComponent(clean)}`);
    if (res.ok) {
      const data = await res.json();
      setVaultFileContent(String(data?.content || ''));
    }
  };

  const handleSaveVaultFile = async (filePath: string, content: string) => {
    const clean = filePath.replace(/^obsidian_vault\//, '');
    await fetch('/api/vault/file', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: clean, content }),
    });
    setVaultFileContent(content);
    await fetchAllData();
  };

  const handleOpenInspectFile = async (filePath: string) => {
    if (
      filePath.startsWith('00_') ||
      filePath.startsWith('01_') ||
      filePath.startsWith('08_') ||
      filePath.startsWith('obsidian_vault/')
    ) {
      const clean = filePath.replace(/^obsidian_vault\//, '');
      await handleSelectVaultFile(clean);
      setActiveWorkspace('projects');
      return;
    }

    const res = await fetch(`/api/project/file?path=${encodeURIComponent(filePath)}`);
    if (res.ok) {
      const data = await res.json();
      setModalFilePath(filePath);
      setModalFileContent(String(data?.content || ''));
    }
  };

  const handleCreateProject = async (payload: {
    code: string;
    title: string;
    university: string;
    methodology: string;
    sampleSize: string;
  }) => {
    const res = await fetch('/api/projects', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (res.ok) {
      await fetchAllData();
    }
  };

  const handleAddTask = async (
    projectId: string,
    payload: { title: string; phase: string; assignedAgent: string }
  ) => {
    const res = await fetch(`/api/projects/${encodeURIComponent(projectId)}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (res.ok) {
      await fetchAllData();
    }
  };

  const handleToggleTaskStatus = async (
    projectId: string,
    taskId: string,
    nextStatus: 'completado' | 'en_progreso' | 'pendiente'
  ) => {
    const res = await fetch(
      `/api/projects/${encodeURIComponent(projectId)}/tasks/${encodeURIComponent(taskId)}`,
      {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: nextStatus }),
      }
    );
    if (res.ok) {
      await fetchAllData();
    }
  };

  if (loading && !ecosystem) {
    return (
      <div className="h-screen w-screen bg-[#0b0d12] text-zinc-100 flex items-center justify-center">
        <div className="flex items-center gap-3 text-sm font-mono text-zinc-300">
          <RefreshCw className="w-4 h-4 text-orange-400 animate-spin" />
          <span>Cargando SIVAC Agent Studio...</span>
        </div>
      </div>
    );
  }

  const agents = ecosystem?.agents || [];
  const skills = ecosystem?.skills || [];
  const mcps = ecosystem?.mcps || [];
  const hooks = ecosystem?.hooks || [];
  const phases = ecosystem?.phases || [];
  const handoffs = ecosystem?.handoffs || [];
  const vaultFiles = ecosystem?.vaultFiles || [];

  return (
    <div className="h-screen w-screen flex flex-col bg-[#0b0d12] text-zinc-100 overflow-hidden">
      {/* Strict 3-Zone Top Bar Contract */}
      <header className="h-12 flex items-center justify-between gap-8 px-5 bg-[#0d1017] border-b border-white/10 shrink-0">
        {/* Zone 1: Single text element wordmark */}
        <a
          href="#studio"
          onClick={(e) => {
            e.preventDefault();
            setActiveWorkspace('chat');
          }}
          className="text-base font-bold tracking-tight text-white whitespace-nowrap shrink-0"
        >
          SIVAC Agent Studio
        </a>

        {/* Zone 2: 4 concise single-line text navigation links */}
        <nav className="flex items-center gap-6 text-xs font-medium text-zinc-400">
          <a
            href="#chat"
            onClick={(e) => {
              e.preventDefault();
              setActiveWorkspace('chat');
            }}
            className={`hover:text-white transition-colors whitespace-nowrap shrink-0 py-1 ${
              activeWorkspace === 'chat'
                ? 'text-white border-b-2 border-orange-500 font-semibold'
                : ''
            }`}
          >
            Chat GOD
          </a>
          <a
            href="#topology"
            onClick={(e) => {
              e.preventDefault();
              setActiveWorkspace('topology');
            }}
            className={`hover:text-white transition-colors whitespace-nowrap shrink-0 py-1 ${
              activeWorkspace === 'topology'
                ? 'text-white border-b-2 border-orange-500 font-semibold'
                : ''
            }`}
          >
            Topología Radial
          </a>
          <a
            href="#capabilities"
            onClick={(e) => {
              e.preventDefault();
              setActiveWorkspace('capabilities');
            }}
            className={`hover:text-white transition-colors whitespace-nowrap shrink-0 py-1 ${
              activeWorkspace === 'capabilities'
                ? 'text-white border-b-2 border-orange-500 font-semibold'
                : ''
            }`}
          >
            MCPs y Skills
          </a>
          <a
            href="#projects"
            onClick={(e) => {
              e.preventDefault();
              setActiveWorkspace('projects');
            }}
            className={`hover:text-white transition-colors whitespace-nowrap shrink-0 py-1 ${
              activeWorkspace === 'projects'
                ? 'text-white border-b-2 border-orange-500 font-semibold'
                : ''
            }`}
          >
            Proyectos y Vault
          </a>
        </nav>

        {/* Zone 3: 1 primary action button */}
        <div className="flex items-center gap-3 shrink-0">
          <button
            type="button"
            onClick={() => setCommandPaletteOpen(true)}
            className="px-3.5 py-1.5 text-xs font-semibold text-zinc-950 bg-orange-500 hover:bg-orange-400 rounded-lg transition-colors whitespace-nowrap shrink-0"
          >
            Comandos ⌘K
          </button>
        </div>
      </header>

      {/* Main Resizable Split-Pane Workbench (react-resizable-panels) */}
      <div className="flex-1 min-h-0 overflow-hidden">
        <Group orientation="horizontal" className="h-full w-full">
          {/* Left Panel: Agno + Opcode Sidebar */}
          <Panel defaultSize="21%" minSize="16%" maxSize="32%">
            <AgnoSidebar
              agents={agents}
              selectedAgentId={selectedAgentId}
              onSelectAgent={(id) => setSelectedAgentId(id)}
              cliStatuses={cliStatuses}
              onRefreshCli={handleRefreshCli}
              onCliAction={handleCliAction}
              projects={projects}
              activeProjectId={activeProjectId}
              onSelectProject={setActiveProjectId}
              busyCliTool={busyCliTool}
            />
          </Panel>

          <Separator className="w-1 bg-white/10 hover:bg-orange-500/60 transition-colors cursor-col-resize" />

          {/* Center Panel: Main Workspace + Bottom XTerm.js Terminal Dock */}
          <Panel defaultSize="57%" minSize="38%">
            <Group orientation="vertical" className="h-full w-full">
              {/* Top Workspace Viewport */}
              <Panel defaultSize={isTerminalMinimized ? '94%' : '66%'} minSize="30%">
                <div className="h-full w-full overflow-hidden">
                  {activeWorkspace === 'chat' && (
                    <AgnoChatArea
                      messages={chatMessages}
                      agents={agents}
                      cliStatuses={cliStatuses}
                      preferredEngine={preferredEngine}
                      onChangeEngine={setPreferredEngine}
                      onSendMessage={handleSendGodMessage}
                      onClearChat={handleClearGodChat}
                      onSelectAgent={(id) => setSelectedAgentId(id)}
                      onOpenVaultFile={handleOpenInspectFile}
                      onRunInTerminal={(cmd) => handleExecuteTerminalCommand(cmd)}
                      isSending={isSendingChat}
                    />
                  )}

                  {activeWorkspace === 'topology' && (
                    <AgentFlowCanvas
                      agents={agents}
                      phases={phases}
                      handoffs={handoffs}
                      delegations={allDelegations}
                      selectedAgentId={selectedAgentId}
                      onSelectAgent={(id) => setSelectedAgentId(id)}
                      onCommissionAgent={(ag, customTask) =>
                        handleCommissionAgent(ag, customTask)
                      }
                      onOpenVaultFile={handleOpenInspectFile}
                    />
                  )}

                  {activeWorkspace === 'capabilities' && (
                    <OpcodeCapabilities
                      mcps={mcps}
                      skills={skills}
                      hooks={hooks}
                      onToggleMcp={handleToggleMcp}
                      onToggleSkill={handleToggleSkill}
                      onToggleHook={handleToggleHook}
                      onOpenFile={handleOpenInspectFile}
                      onRunInTerminal={(cmd) => handleExecuteTerminalCommand(cmd)}
                    />
                  )}

                  {activeWorkspace === 'projects' && (
                    <ObsidianWorkspace
                      projects={projects}
                      activeProjectId={activeProjectId}
                      onSelectProject={setActiveProjectId}
                      onCreateProject={handleCreateProject}
                      onAddTask={handleAddTask}
                      onToggleTaskStatus={handleToggleTaskStatus}
                      vaultFiles={vaultFiles}
                      selectedVaultPath={selectedVaultPath}
                      vaultFileContent={vaultFileContent}
                      onSelectVaultFile={handleSelectVaultFile}
                      onSaveVaultFile={handleSaveVaultFile}
                      agents={agents}
                      onCommissionTaskToGod={(prompt) => {
                        setActiveWorkspace('chat');
                        return handleSendGodMessage(prompt, preferredEngine);
                      }}
                    />
                  )}
                </div>
              </Panel>

              <Separator className="h-1 bg-white/10 hover:bg-orange-500/60 transition-colors cursor-row-resize" />

              {/* Bottom Dock: Real XTerm.js + Bun Shell Terminal */}
              <Panel
                defaultSize={isTerminalMinimized ? '6%' : '34%'}
                minSize="6%"
                maxSize="65%"
              >
                <XTermConsole
                  logs={terminalLogs}
                  activeSession={activeTerminalSession}
                  onSelectSession={setActiveTerminalSession}
                  onExecuteCommand={handleExecuteTerminalCommand}
                  onClearTerminal={handleClearTerminal}
                  isMinimized={isTerminalMinimized}
                  onToggleMinimize={() => setIsTerminalMinimized(!isTerminalMinimized)}
                  cliStatuses={cliStatuses}
                />
              </Panel>
            </Group>
          </Panel>

          <Separator className="w-1 bg-white/10 hover:bg-orange-500/60 transition-colors cursor-col-resize" />

          {/* Right Panel: Contextual Agent Inspector & Handoff Dispatcher */}
          <Panel defaultSize="22%" minSize="18%" maxSize="34%">
            <AgentInspectorPanel
              agent={selectedAgent}
              handoffs={handoffs}
              onCommissionAgent={(ag, task, eng) => handleCommissionAgent(ag, task, eng)}
              onOpenFile={handleOpenInspectFile}
              onRunInTerminal={(cmd) => handleExecuteTerminalCommand(cmd)}
            />
          </Panel>
        </Group>
      </div>

      {/* Command Palette (cmdk ⌘K) */}
      <CommandPalette
        open={commandPaletteOpen}
        onOpenChange={setCommandPaletteOpen}
        agents={agents}
        mcps={mcps}
        skills={skills}
        onSelectAgent={(id) => setSelectedAgentId(id)}
        onSwitchWorkspace={(tab) => setActiveWorkspace(tab)}
        onRunCommand={(cmd) => handleExecuteTerminalCommand(cmd)}
        onSendGodPrompt={(prompt) => {
          setActiveWorkspace('chat');
          return handleSendGodMessage(prompt, preferredEngine);
        }}
      />

      {/* File Source Modal Viewer (.claude/agents/*.md, .mcp.json, SKILL.md) */}
      {modalFilePath && (
        <div
          onClick={() => setModalFilePath(null)}
          className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-6"
        >
          <div
            onClick={(e) => e.stopPropagation()}
            className="w-full max-w-4xl max-h-[82vh] rounded-2xl bg-[#111520] border border-white/15 flex flex-col overflow-hidden shadow-2xl"
          >
            <div className="h-11 px-4 border-b border-white/10 flex items-center justify-between bg-[#0f1219] shrink-0">
              <div className="flex items-center gap-2 text-xs font-mono text-zinc-200">
                <FileCode2 className="w-4 h-4 text-orange-400" />
                <span>{modalFilePath}</span>
              </div>
              <button
                type="button"
                onClick={() => setModalFilePath(null)}
                className="p-1 text-zinc-400 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <pre className="flex-1 overflow-auto p-5 text-xs font-mono text-zinc-200 leading-relaxed whitespace-pre-wrap">
              {modalFileContent}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
