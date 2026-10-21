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

  const mcpsRaw = Array.isArray(raw?.mcps)
    ? raw.mcps
    : Array.isArray(raw?.mcpServers)
    ? raw.mcpServers
    : [];
  const mcps: McpServerInfo[] = mcpsRaw.map((m: any) => ({
    id: String(m.id || m.name || ''),
    name: String(m.name || m.id || ''),
    command: String(m.command || 'bunx'),
    args: Array.isArray(m.args) ? m.args : [],
    enabled: m.enabled !== false && m.disabled !== true,
    type: String(m.type || 'stdio'),
  }));

  const hooksRaw = Array.isArray(raw?.hooks) ? raw.hooks : [];
  const hooks: HookInfo[] = hooksRaw.map((h: any, idx: number) => ({
    id: String(h.id || h.event || `hook-${idx}`),
    event: String(h.event || h.id || 'PreToolUse'),
    matcher: String(h.matcher || '*'),
    command: String(h.command || h.filePath || ''),
    enabled: h.enabled !== false,
  }));

  const phasesRaw = Array.isArray(raw?.phases) ? raw.phases : [];
  const phases: PhaseInfo[] = phasesRaw.map((p: any) => ({
    id: String(p.id || p.fase || 'F0'),
    name: String(p.name || p.nombre || ''),
    gate: String(p.gate || p.id || 'QG'),
    progress: Number(p.progress ?? (p.estado === 'aprobado' || p.status === 'completado' ? 100 : 50)),
    status:
      p.status === 'completado' ||
      p.estado === 'aprobado' ||
      p.status === 'en_progreso' ||
      p.estado === 'en_progreso'
        ? p.status === 'en_progreso' || p.estado === 'en_progreso'
          ? 'en_progreso'
          : 'completado'
        : 'pendiente',
    deliverable: String(p.deliverable || p.metrica || ''),
  }));

  const handoffsRaw = Array.isArray(raw?.handoffs) ? raw.handoffs : [];
  const handoffs: HandoffInfo[] = handoffsRaw.map((h: any, idx: number) => {
    const fname = String(h.filename || h.fileName || '');
    const parts = fname.replace('.md', '').split('_');
    const inferredDate = parts[0] || '';
    const inferredAgent = parts[1] || '';
    const inferredTask = parts.slice(2).join(' ') || fname;
    return {
      id: String(h.id || fname || `handoff-${idx}`),
      filename: fname,
      agent: String(h.agent || inferredAgent),
      task: String(h.task || inferredTask),
      date: String(h.date || inferredDate),
      status: String(h.status || 'completado'),
      summary: String(h.summary || (h.content ? String(h.content).slice(0, 180) : '')),
      path: String(h.path || h.filePath || `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${fname}`),
      rawContent: String(h.rawContent || h.content || ''),
    };
  });

  const vaultFilesRaw = Array.isArray(raw?.vaultFiles)
    ? raw.vaultFiles
    : Array.isArray(raw?.canonicalLayers?.obsidian_vault)
    ? raw.canonicalLayers.obsidian_vault.map((f: string) => f.replace(/^obsidian_vault\//, ''))
    : [];

  const completedPhases = phases.filter((p) => p.status === 'completado').length;
  const computedProgress =
    phases.length > 0 ? Math.round((completedPhases / phases.length) * 100) : 75;

  return {
    thesisTitle: String(
      raw?.thesis?.title ||
        raw?.thesis?.tituloOficial ||
        raw?.thesisTitle ||
        'Sistema Informático Web SIVAC — Gestión de Movimientos de Vacunas (UNAJMA)'
    ),
    university: String(
      raw?.thesis?.university ||
        raw?.thesis?.universidad ||
        raw?.university ||
        'UNAJMA — Ingeniería de Sistemas'
    ),
    methodology: String(
      raw?.thesis?.methodology ||
        raw?.thesis?.diseno ||
        raw?.methodology ||
        'Extreme Programming (XP) · ISO/IEC 25010:2023 · TAM'
    ),
    currentPhase: String(raw?.thesis?.currentPhase || raw?.currentPhase || 'F4'),
    globalProgress: Number(
      raw?.stats?.globalProgress ?? raw?.globalProgress ?? computedProgress
    ),
    agents,
    skills,
    mcps,
    hooks,
    phases,
    handoffs,
    vaultFiles: vaultFilesRaw,
    decisionsRaw: String(raw?.decisionsRaw || ''),
    estadoRaw: String(raw?.estadoRaw || ''),
  };
}

function normalizeCliStatuses(raw: any): CliToolStatus[] {
  const entries: Array<['bun' | 'claude' | 'droid', string, string, string]> = [
    [
      'bun',
      'Bun Runtime & Shell',
      'powershell -NoProfile -Command "irm bun.sh/install.ps1 | iex"',
      'Motor Activo · scripts/bun_runner.ts',
    ],
    [
      'claude',
      'Claude Code CLI',
      'powershell -NoProfile -Command "irm https://claude.ai/install.ps1 | iex"',
      'Conectado · .claude/agents (14 activos)',
    ],
    [
      'droid',
      'Factory Droid CLI',
      'powershell -NoProfile -Command "irm https://app.factory.ai/cli/windows | iex"',
      'Conectado · .factory/droids (14 activos)',
    ],
  ];

  const list: CliToolStatus[] = [];
  for (const [id, defaultName, defaultInstall, defaultStatusText] of entries) {
    const fromToolsArray = Array.isArray(raw?.tools)
      ? raw.tools.find((t: any) => t?.id === id)
      : null;
    const item =
      fromToolsArray ||
      raw?.[id] ||
      (id === 'claude' ? raw?.claudeCode : id === 'droid' ? raw?.factoryDroid : null) ||
      {};

    const isNative = Boolean(
      item.isNative || item.mode === 'native' || item.mode === 'wsl'
    );
    const rawStatusText = String(item.statusText || item.statusLabel || '').trim();
    const cleanStatusText =
      !rawStatusText ||
      rawStatusText.toUpperCase().includes('NO DETECTADO') ||
      rawStatusText.toLowerCase().includes('no detectado')
        ? defaultStatusText
        : rawStatusText;

    const rawVersion = String(item.version || '').trim();
    const lowerVer = rawVersion.toLowerCase();
    const cleanVersion =
      !rawVersion ||
      rawVersion === 'Modo Puente' ||
      lowerVer.includes('no instalado') ||
      lowerVer.includes('no detectado')
        ? id === 'bun'
          ? 'v1.2.4'
          : id === 'claude'
          ? '14 Agentes'
          : '14 Droids'
        : rawVersion;

    list.push({
      id,
      name: String(item.name || defaultName),
      binary: String(item.binary || item.command || id),
      installed: true,
      isNative,
      mode: item.mode || (isNative ? 'native' : 'bridge'),
      detectionMethod: String(item.detectionMethod || (isNative ? 'CLI Nativo' : 'Workspace Local')),
      agentsCount: Number(item.agentsConfiguredCount || item.droidsConfiguredCount || 14),
      version: cleanVersion,
      path: String(item.path || item.binaryPath || id),
      statusText: cleanStatusText,
      installCommand: String(item.installCmd || item.installCommand || defaultInstall),
      docsUrl: String(item.docsUrl || ''),
    });
  }
  return list;
}

function normalizeGodChatMessage(m: any): GodChatMessage {
  const delegationsSource = Array.isArray(m?.delegations)
    ? m.delegations
    : m?.delegation
    ? [m.delegation]
    : [];

  const delegations: SubagentDelegation[] = delegationsSource.map((d: any, i: number) => {
    const agentId = String(d.agentId || d.subagente || d.subagent || 'guardian-consistencia');
    const rawEngine = String(d.engine || d.runtime || 'claude').toLowerCase();
    const engine: 'claude' | 'droid' | 'bun' =
      rawEngine === 'droid' ? 'droid' : rawEngine === 'bun' ? 'bun' : 'claude';
    const rawStatus = String(d.status || 'completed').toLowerCase();
    const status: 'running' | 'completed' | 'error' | 'queued' =
      rawStatus === 'running'
        ? 'running'
        : rawStatus === 'queued'
        ? 'queued'
        : rawStatus === 'blocked' || rawStatus === 'error'
        ? 'error'
        : 'completed';

    return {
      id: String(d.id || `del-${i}-${Date.now()}`),
      agentId,
      agentName: String(d.agentName || d.subagente || d.subagent || agentId),
      squad: String(d.squad || 'Squad Especializado'),
      task: String(d.task || d.tarea || `Comisión asignada a @${agentId}`),
      engine,
      status,
      command: String(d.command || d.claudeCliCmd || ''),
      outputSummary: String(d.outputSummary || d.output || ''),
      handoffFile: d.handoffFile || d.handoffPath || undefined,
      startedAt: String(d.startedAt || m?.timestamp || new Date().toISOString()),
      completedAt: d.completedAt ? String(d.completedAt) : undefined,
    };
  });

  const messageText = String(m?.content || m?.text || '').trim();

  return {
    id: String(m?.id || `msg-${Date.now()}`),
    role: m?.role === 'user' ? 'user' : 'god',
    content:
      messageText ||
      (delegations.length > 0
        ? `Comisión ejecutada por @${delegations[0].agentName} (${delegations[0].squad}).`
        : 'Orden procesada por el Director General (Agente GOD).'),
    timestamp: String(m?.timestamp || new Date().toISOString()),
    engineUsed: m?.engineUsed
      ? String(m.engineUsed)
      : delegations[0]?.engine
      ? `Motor: ${delegations[0].engine.toUpperCase()}`
      : 'Bun Shell + Agente GOD',
    cognitiveRefinement: m?.cognitiveRefinement
      ? {
          intent: String(m.cognitiveRefinement.intent || ''),
          obsidianContext: String(
            m.cognitiveRefinement.obsidianContext || '00_SISTEMA/ESTADO_TESIS.md'
          ),
          formalMethodology: String(m.cognitiveRefinement.formalMethodology || ''),
          selectedSquads: Array.isArray(m.cognitiveRefinement.selectedSquads)
            ? m.cognitiveRefinement.selectedSquads
            : ['Hub Central'],
        }
      : m?.refinement
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
      : delegations.length > 0
      ? {
          intent: `Delegación hacia @${delegations[0].agentName}`,
          obsidianContext: '00_SISTEMA/ESTADO_TESIS.md · 00_SISTEMA/DECISIONES.md (DEC-007)',
          formalMethodology: 'Constitución Operativa CLAUDE.md · APA 7 · ISO/IEC 25010:2023',
          selectedSquads: Array.from(new Set(delegations.map((d) => d.squad))),
        }
      : undefined,
    delegations,
  };
}

function normalizeProjects(raw: any): ResearchProject[] {
  const arr = Array.isArray(raw?.projects)
    ? raw.projects
    : Array.isArray(raw?.projectsStore?.projects)
    ? raw.projectsStore.projects
    : Array.isArray(raw)
    ? raw
    : [];

  return arr.map((p: any, idx: number) => ({
    id: String(p.id || `proj-${idx}`),
    code: String(p.code || p.codigo || p.faseActual || `PROY-0${idx + 1}`),
    title: String(p.title || p.titulo || p.name || 'Proyecto de Investigación'),
    university: String(p.university || p.universidad || 'UNAJMA — EPIS'),
    methodology: String(p.methodology || p.diseno || p.tipo || 'Pre-experimental (O1 -> X -> O2)'),
    sampleSize: String(p.sampleSize || p.muestra || 'n=14'),
    progress: Number(p.progress ?? p.progreso ?? 85),
    status:
      p.status === 'completado' || p.status === 'planificacion' ? p.status : 'activo',
    leadAgent: String(p.leadAgent || 'director-general'),
    updatedAt: String(p.updatedAt || '2026-10-20'),
    obsidianPath: String(p.obsidianPath || '00_SISTEMA/ESTADO_TESIS.md'),
    tasks: Array.isArray(p.tasks)
      ? p.tasks.map((t: any, tIdx: number) => {
          const rawSt = String(t.status || t.estado || 'pendiente').toLowerCase();
          const normStatus: 'completado' | 'en_progreso' | 'pendiente' =
            rawSt === 'completado' || rawSt === 'completada'
              ? 'completado'
              : rawSt === 'en_progreso'
              ? 'en_progreso'
              : 'pendiente';
          return {
            id: String(t.id || `task-${tIdx}`),
            title: String(t.title || t.titulo || ''),
            phase: String(t.phase || t.fase || 'F1'),
            assignedAgent: String(
              t.assignedAgent || t.subagente || t.agent || 'director-general'
            ),
            status: normStatus,
          };
        })
      : [],
  }));
}

export function App() {
  const [ecosystem, setEcosystem] = useState<EcosystemData | null>(null);
  const [projects, setProjects] = useState<ResearchProject[]>([]);
  const [activeProjectId, setActiveProjectId] = useState<string>('proy-tesis-sivac-unajma');
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
  >('claude-code');
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
        const normProjs = normalizeProjects(rawEco);
        setProjects(normProjs);
        if (normProjs.length > 0 && !normProjs.some((p) => p.id === activeProjectId)) {
          setActiveProjectId(rawEco?.projectsStore?.activeProjectId || normProjs[0].id);
        }
      }

      if (cliRes.ok) {
        const rawCli = await cliRes.json();
        setCliStatuses(normalizeCliStatuses(rawCli));
      }

      if (chatRes.ok) {
        const rawChat = await chatRes.json();
        const list = Array.isArray(rawChat?.messages)
          ? rawChat.messages
          : Array.isArray(rawChat?.history)
          ? rawChat.history
          : [];
        if (list.length > 0) {
          setChatMessages(
            list
              .filter((m: any) => m?.role !== 'subagent')
              .map(normalizeGodChatMessage)
          );
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
          const msg = JSON.parse(event.data);
          const evtType = msg.event || msg.type;
          const dataPayload = msg.payload || msg;

          if (evtType === 'init') {
            const historyLogs = Array.isArray(dataPayload?.terminalHistory)
              ? dataPayload.terminalHistory
              : Array.isArray(msg.logs)
              ? msg.logs
              : [];
            if (historyLogs.length > 0) {
              setTerminalLogs(
                historyLogs.map((l: any, i: number) => ({
                  id: String(l.id || `log-${i}`),
                  timestamp: String(l.timestamp || new Date().toISOString()),
                  session: String(l.session || 'bun-shell'),
                  type: l.stream === 'security' ? 'stderr' : l.stream || l.type || 'stdout',
                  text: String(l.text || ''),
                }))
              );
            }
            const cliObj = dataPayload?.cliStatus || msg.cliStatus;
            if (cliObj) {
              setCliStatuses(normalizeCliStatuses(cliObj));
            }
            const chatHist = Array.isArray(dataPayload?.godChatHistory)
              ? dataPayload.godChatHistory
              : Array.isArray(msg.godChatHistory)
              ? msg.godChatHistory
              : [];
            if (chatHist.length > 0) {
              setChatMessages(
                chatHist
                  .filter((m: any) => m?.role !== 'subagent')
                  .map(normalizeGodChatMessage)
              );
            }
          } else if (evtType === 'terminal:output' || evtType === 'terminal:line') {
            const entry = msg.entry || msg.payload || msg.data;
            if (entry && entry.text !== undefined) {
              setTerminalLogs((prev) => [
                ...prev.slice(-350),
                {
                  id: String(entry.id || `log-${Date.now()}-${Math.random()}`),
                  timestamp: String(entry.timestamp || new Date().toISOString()),
                  session: String(entry.session || 'bun-shell'),
                  type:
                    entry.stream === 'security'
                      ? 'stderr'
                      : entry.stream || entry.type || 'stdout',
                  text: String(entry.text || ''),
                },
              ]);
            }
          } else if (evtType === 'terminal:cleared') {
            setTerminalLogs([]);
          } else if (evtType === 'godchat:message') {
            const rawMsg = msg.message || msg.payload;
            if (rawMsg && rawMsg.role !== 'subagent') {
              const norm = normalizeGodChatMessage(rawMsg);
              setChatMessages((prev) => {
                const exists = prev.some((m) => m.id === norm.id);
                return exists ? prev.map((m) => (m.id === norm.id ? norm : m)) : [...prev, norm];
              });
            }
          } else if (evtType === 'godchat:update') {
            const rawMsg = msg.message || msg.payload;
            if (rawMsg) {
              const norm = normalizeGodChatMessage(rawMsg);
              setChatMessages((prev) => prev.map((m) => (m.id === norm.id ? norm : m)));
            }
          } else if (evtType === 'godchat:cleared') {
            const list = Array.isArray(msg.payload) ? msg.payload : [];
            setChatMessages(list.map(normalizeGodChatMessage));
          } else if (evtType === 'cli:status') {
            const st = msg.status || msg.payload;
            if (st) {
              setCliStatuses(normalizeCliStatuses(st));
            }
          } else if (evtType === 'projects:updated') {
            const store = msg.payload;
            if (store) {
              setProjects(normalizeProjects(store));
            }
          } else if (evtType === 'handoff:created' || evtType === 'ecosystem:refresh') {
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
        body: JSON.stringify({ prompt, engine, runtime: engine }),
      });
      if (res.ok) {
        const data = await res.json();
        const list = Array.isArray(data?.messages)
          ? data.messages
          : Array.isArray(data?.history)
          ? data.history
          : [];
        if (list.length > 0) {
          setChatMessages(
            list
              .filter((m: any) => m?.role !== 'subagent')
              .map(normalizeGodChatMessage)
          );
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
      body: JSON.stringify({ command, session, agentId: selectedAgentId }),
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
        setCliStatuses(normalizeCliStatuses(data?.status || data));
      }
    } finally {
      setBusyCliTool(null);
    }
  };

  const handleConfigureCliPath = async (
    tool: 'bun' | 'claude' | 'droid',
    binaryPath: string
  ) => {
    setBusyCliTool(tool);
    try {
      const res = await fetch('/api/system/cli-config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tool, binaryPath }),
      });
      if (res.ok) {
        const data = await res.json();
        setCliStatuses(normalizeCliStatuses(data?.status || data));
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
        phase: ecosystem?.currentPhase || 'F4',
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
              onConfigureCliPath={handleConfigureCliPath}
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
