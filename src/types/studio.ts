export interface AgentInfo {
  id: string;
  name: string;
  squad: string;
  role: string;
  model: string;
  description: string;
  tools: string[];
  skills: string[];
  filePath: string;
  readOnly?: boolean;
}

export interface SkillInfo {
  id: string;
  name: string;
  description: string;
  path: string;
  enabled?: boolean;
}

export interface McpServerInfo {
  id: string;
  name: string;
  command: string;
  args: string[];
  enabled: boolean;
  type: string;
}

export interface HookInfo {
  id: string;
  event: string;
  matcher: string;
  command: string;
  enabled: boolean;
}

export interface PhaseInfo {
  id: string;
  name: string;
  gate: string;
  progress: number;
  status: 'completado' | 'en_progreso' | 'pendiente';
  deliverable: string;
}

export interface HandoffInfo {
  id: string;
  filename: string;
  agent: string;
  task: string;
  date: string;
  status: string;
  summary: string;
  path: string;
  rawContent: string;
}

export interface TerminalLog {
  id: string;
  timestamp: string;
  session: string;
  type: 'command' | 'stdout' | 'stderr' | 'system';
  text: string;
}

export interface CliToolStatus {
  id: 'bun' | 'claude' | 'droid';
  name: string;
  binary: string;
  installed: boolean;
  isNative?: boolean;
  mode?: 'native' | 'wsl' | 'bridge';
  detectionMethod?: string;
  agentsCount?: number;
  version: string;
  path: string;
  statusText: string;
  installCommand: string;
  docsUrl: string;
}

export interface SubagentDelegation {
  id: string;
  agentId: string;
  agentName: string;
  squad: string;
  task: string;
  engine: 'claude' | 'droid' | 'bun';
  status: 'queued' | 'running' | 'completed' | 'error';
  command: string;
  outputSummary?: string;
  handoffFile?: string;
  startedAt: string;
  completedAt?: string;
}

export interface GodChatMessage {
  id: string;
  role: 'user' | 'god';
  content: string;
  timestamp: string;
  engineUsed?: string;
  cognitiveRefinement?: {
    intent: string;
    obsidianContext: string;
    formalMethodology: string;
    selectedSquads: string[];
  };
  delegations?: SubagentDelegation[];
}

export interface ResearchProjectTask {
  id: string;
  title: string;
  phase: string;
  assignedAgent: string;
  status: 'completado' | 'en_progreso' | 'pendiente';
}

export interface ResearchProject {
  id: string;
  code: string;
  title: string;
  university: string;
  methodology: string;
  sampleSize: string;
  progress: number;
  status: 'activo' | 'planificacion' | 'completado';
  leadAgent: string;
  updatedAt: string;
  obsidianPath: string;
  tasks: ResearchProjectTask[];
}

export interface EcosystemData {
  thesisTitle: string;
  university: string;
  methodology: string;
  currentPhase: string;
  globalProgress: number;
  agents: AgentInfo[];
  skills: SkillInfo[];
  mcps: McpServerInfo[];
  hooks: HookInfo[];
  phases: PhaseInfo[];
  handoffs: HandoffInfo[];
  vaultFiles: string[];
  decisionsRaw: string;
  estadoRaw: string;
}
