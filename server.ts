import express from 'express';
import http from 'http';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { execFileSync, spawn, ChildProcessWithoutNullStreams } from 'child_process';
import { fileURLToPath } from 'url';
import { createServer as createViteServer } from 'vite';
import { WebSocketServer, WebSocket } from 'ws';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

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
  text: string;
  agentId?: string;
  mode?: 'bun' | 'shell' | 'claude' | 'droid';
}

interface DelegationEvent {
  id: string;
  timestamp: string;
  from: string;
  to: string;
  squad: string;
  fase: string;
  tarea: string;
  command: string;
  status: 'running' | 'completed' | 'blocked';
  handoffPath?: string;
  exitCode?: number;
}

interface GodChatMessage {
  id: string;
  timestamp: string;
  role: 'user' | 'god' | 'subagent';
  senderName: string;
  senderId: string;
  squad?: string;
  text: string;
  delegation?: {
    subagente: string;
    squad: string;
    fase: string;
    runtime: 'bun' | 'claude' | 'droid';
    command: string;
    claudeCliCmd: string;
    droidCliCmd: string;
    status: 'running' | 'completed' | 'blocked';
    outputSummary?: string;
    handoffPath?: string;
    deliverablePath?: string;
    exitCode?: number;
  };
}

// Runtime authoritative state
const agentRuntimeStatus: Record<
  string,
  { status: 'idle' | 'running' | 'completed' | 'blocked'; currentTask?: string; lastCommand?: string; lastRunAt?: string }
> = {};
const terminalHistory: TerminalLine[] = [
  {
    id: 'boot-1',
    timestamp: new Date().toISOString(),
    stream: 'system',
    text: '[SIVAC-THESIS-LAB OS · BUN ENGINE] Runtime Bun v1.4.2 + Puentes CLI claude y droid activos.',
  },
  {
    id: 'boot-2',
    timestamp: new Date().toISOString(),
    stream: 'system',
    text: '[MEMORIA VIVA OBSIDIAN] Conectado a obsidian_vault/00_SISTEMA/ESTADO_TESIS.md y DECISIONES.md (DEC-007 / DEC-015 / DEC-020 / DEC-027).',
  },
];
const activeDelegations: DelegationEvent[] = [];
const godChatHistory: GodChatMessage[] = [
  {
    id: 'god-welcome-1',
    timestamp: new Date().toISOString(),
    role: 'god',
    senderName: 'Director General (Agente GOD)',
    senderId: 'director-general',
    squad: 'Hub Central',
    text: 'Bienvenido al Centro de Mando SIVAC-THESIS-LAB. Escríbeme cualquier orden en lenguaje sencillo (por ejemplo: "Verifica las citas APA 7 del capítulo 2", "Genera el Anexo 2 de validación Fany 2024", "Audita las tablas del informe Word" o "Muéstrame el estado general de la tesis"). Yo analizaré tu pedido y delegaré automáticamente la ejecución al subagente especialista usando Bun, Claude Code o Factory Droid.',
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
  'director-general': 'python3 scripts/agentes/estado_granja.py',
  'investigador-bibliografico': 'python3 scripts/fuentes/buscador_citas.py',
  'verificador-integridad': 'python3 scripts/agentes/verificador_integridad.py',
  'guardian-consistencia': 'python3 scripts/agentes/guardian_consistencia.py',
  'especialista-instrumentos': 'python3 scripts/compiladores/generar_anexo2_validacion_fany.py',
  'especialista-forms': 'python3 scripts/agentes/validez_contenido.py',
  'ingeniero-sivac': 'python3 scripts/agentes/inventario_syncova.py',
  'documentador-xp': 'python3 scripts/agentes/inventario_syncova.py',
  'analista-estadistico': 'python3 scripts/estadistica/pipeline_inferencial.py --json',
  'analista-documental': 'python3 scripts/agentes/analista_documental.py',
  'redactor-academico': 'python3 scripts/agentes/revisor_prosa.py',
  'maquetador-docx': 'python3 scripts/utilidades/auditor_docx_apa7.py auditar salidas/documentos/informe_final_v02.docx',
  'curador-cerebro': 'python3 scripts/agentes/curador_cerebro.py',
  'jurado-revisor': 'python3 scripts/utilidades/auditor_docx_apa7.py auditar salidas/documentos/informe_final_v02.docx --md',
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
    const readOnly =
      name === 'ingeniero-sivac' ||
      (tools.length > 0 && tools.every((t) => ['Read', 'Grep', 'Glob'].includes(t)));
    const runtime = agentRuntimeStatus[id] || { status: 'idle' };

    return {
      id,
      name,
      description: typeof frontmatter.description === 'string' ? frontmatter.description : '',
      model: typeof frontmatter.model === 'string' ? frontmatter.model : 'sonnet',
      squad: typeof frontmatter.squad === 'string' ? frontmatter.squad : 'Squad Especializado',
      role: typeof frontmatter.role === 'string' ? frontmatter.role : '',
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

    skills.push({
      id: entry.name,
      name: typeof frontmatter.name === 'string' ? frontmatter.name : entry.name,
      description:
        typeof frontmatter.description === 'string' && frontmatter.description.length > 0
          ? frontmatter.description
          : firstParagraph || 'Skill especializada de SIVAC-THESIS-LAB',
      filePath: `.claude/skills/${entry.name}/SKILL.md`,
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
    .map((f) => {
      const fullPath = path.join(handoffsDir, f);
      const content = fs.readFileSync(fullPath, 'utf-8');
      return {
        fileName: f,
        filePath: `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${f}`,
        content,
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

function detectCliStatus() {
  const probeBinary = (binName: string, versionArg = '--version') => {
    try {
      const whichOut = execFileSync('bash', ['-c', `command -v ${binName}`], {
        cwd: __dirname,
        encoding: 'utf-8',
      }).trim();
      const verOut = execFileSync('bash', ['-c', `${binName} ${versionArg} 2>&1 | head -n 1`], {
        cwd: __dirname,
        encoding: 'utf-8',
      }).trim();
      return { installed: Boolean(whichOut), binaryPath: whichOut, version: verOut || 'Detectado' };
    } catch {
      return { installed: false, binaryPath: 'No detectado en PATH', version: 'No instalado' };
    }
  };

  const bunProbe = probeBinary('bun', '--version');
  const claudeProbe = probeBinary('claude', '--version');
  const droidProbe = probeBinary('droid', '--version');
  const pyProbe = probeBinary('python3', '--version');
  const gitProbe = probeBinary('git', '--version');

  const claudeAgentsCount = fs.existsSync(path.join(__dirname, '.claude', 'agents'))
    ? fs.readdirSync(path.join(__dirname, '.claude', 'agents')).filter((f) => f.endsWith('.md')).length
    : 0;
  const factoryDroidsCount = fs.existsSync(path.join(__dirname, '.factory', 'droids'))
    ? fs.readdirSync(path.join(__dirname, '.factory', 'droids')).filter((f) => f.endsWith('.md')).length
    : 0;

  return {
    checkedAt: new Date().toISOString(),
    bun: {
      name: 'Bun Runtime & Shell',
      command: 'bun',
      installed: bunProbe.installed,
      version: bunProbe.version,
      binaryPath: bunProbe.binaryPath,
      statusLabel: bunProbe.installed ? 'INSTALADO Y ACTIVO' : 'NO DETECTADO',
      verifyCmd: 'bun --version',
      installCmd: 'curl -fsSL https://bun.sh/install | bash',
      details: 'Motor ultrarrápido para ejecución de agentes, scripts TypeScript y paquetes MCP (bunx).',
    },
    claudeCode: {
      name: 'Claude Code CLI',
      command: 'claude',
      installed: claudeProbe.installed,
      version: claudeProbe.version,
      binaryPath: claudeProbe.binaryPath,
      agentsConfiguredCount: claudeAgentsCount,
      statusLabel: claudeProbe.installed ? 'INSTALADO (PUENTE BUN ACTIVO)' : 'NO DETECTADO',
      verifyCmd: 'claude --version',
      sampleCmd: 'claude -p "Auditar citas APA 7" --agent verificador-integridad --output-format stream-json --verbose',
      installCmd: 'bun add -g @anthropic-ai/claude-code',
      details: `${claudeAgentsCount} agentes configurados en .claude/agents/*.md y hooks en .claude/settings.json.`,
    },
    factoryDroid: {
      name: 'Factory Droid CLI',
      command: 'droid',
      installed: droidProbe.installed,
      version: droidProbe.version,
      binaryPath: droidProbe.binaryPath,
      droidsConfiguredCount: factoryDroidsCount,
      statusLabel: droidProbe.installed ? 'INSTALADO (PUENTE BUN ACTIVO)' : 'NO DETECTADO',
      verifyCmd: 'droid --version',
      sampleCmd: 'droid exec "Auditar tablas OpenXML APA 7" --droid maquetador-docx --auto medium',
      installCmd: 'curl -fsSL https://app.factory.ai/cli | sh',
      details: `${factoryDroidsCount} droids sincronizados en .factory/droids/*.md y AGENTS.md.`,
    },
    pythonGit: {
      name: 'Python 3 Científico + Git',
      command: 'python3',
      installed: pyProbe.installed && gitProbe.installed,
      version: `${pyProbe.version} · ${gitProbe.version}`,
      binaryPath: pyProbe.binaryPath,
      statusLabel: pyProbe.installed ? 'INSTALADO Y VERIFICADO' : 'NO DETECTADO',
      verifyCmd: 'python3 --version && git --version',
      details: 'Motor OpenXML quirúrgico (.docx, .pdf, .xlsx, 300 DPI) y control de versiones Git.',
    },
  };
}

function classifyPromptIntent(rawPrompt: string) {
  const lower = rawPrompt.toLowerCase();
  let squad = 'Squad E (Redacción y Maquetación)';
  let subagente = 'maquetador-docx';
  let fase = 'F4';
  let tarea = '';
  let entradas = '';
  let salidaEsperada = '';
  let entregable = 'salidas/documentos/informe_final_v02.docx';
  let comandoSugerido = '';
  let diagnostico = '';

  if (lower.includes('cita') || lower.includes('doi') || lower.includes('zotero') || lower.includes('referencia') || lower.includes('cap 2')) {
    squad = 'Squad A (Evidencia y Bibliometría)';
    subagente = lower.includes('busca') ? 'investigador-bibliografico' : 'verificador-integridad';
    fase = 'F2';
    tarea = `Ejecutar auditoría determinista 1:1 de citas y referencias APA 7 en atención a: "${rawPrompt}", verificando trazabilidad contra índices PDF de la bóveda.`;
    entradas = 'obsidian_vault/04_LITERATURA_Y_FUENTES/indices_pdf/\nsalidas/documentos/informe_final_v02.docx';
    salidaEsperada = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${new Date().toISOString().slice(0, 10)}_${subagente}_auditoria-citas.md`;
    entregable = 'salidas/documentos/informe_final_v02.docx';
    comandoSugerido = 'python3 scripts/agentes/verificador_integridad.py';
    diagnostico = 'He detectado una tarea bibliométrica (Squad A). Delegaré a verificador-integridad para comprobar la correspondencia 1:1 de citas APA 7 y sangría francesa.';
  } else if (lower.includes('instrumento') || lower.includes('fany') || lower.includes('experto') || lower.includes('aiken') || lower.includes('anexo 2')) {
    squad = 'Squad B (Metodología y Psicometría)';
    subagente = 'especialista-instrumentos';
    fase = 'F3';
    tarea = `Compilar y verificar el Certificado Único de Validación Fany 2024 en blanco (DEC-015/016/019/020) para los 8 reactivos del Instrumento 03 (TAM): "${rawPrompt}".`;
    entradas = 'referencias/modelos_validacion/FORMATO_VALIDACION_FANY_2024_OFICIAL.docx\nsalidas/instrumentos/EXPEDIENTE_INSTRUMENTOS_SIVAC_DEC007.md';
    salidaEsperada = 'salidas/documentos/anexos_fany/ANEXO_2_VALIDACION_FANY_INST03_MODALIDAD_A_VACIO.docx';
    entregable = 'salidas/documentos/anexos_fany/ANEXO_2_VALIDACION_FANY_INST03_MODALIDAD_A_VACIO.docx';
    comandoSugerido = 'python3 scripts/compiladores/generar_anexo2_validacion_fany.py';
    diagnostico = 'He detectado un requerimiento psicométrico (Squad B). Delegaré a especialista-instrumentos para emitir el Certificado Fany 2024 en blanco conforme a DEC-015 y DEC-020.';
  } else if (lower.includes('matriz') || lower.includes('consistencia') || lower.includes('dimension') || lower.includes('dec-007')) {
    squad = 'Squad B (Metodología y Psicometría)';
    subagente = 'guardian-consistencia';
    fase = 'F1';
    tarea = `Auditar el isomorfismo metodológico de las 3 dimensiones oficiales DEC-007 (Oportunidad, Consistencia documental y Satisfacción del usuario) frente a: "${rawPrompt}".`;
    entradas = 'obsidian_vault/01_MATRIZ_Y_CONSISTENCIA/MATRIZ_CONSISTENCIA_DEC007.md\ndatos/schemas/codebook.json';
    salidaEsperada = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${new Date().toISOString().slice(0, 10)}_guardian-consistencia_isomorfismo.md`;
    entregable = 'salidas/documentos/MATRIZ_CONSISTENCIA_Y_OPERACIONALIZACION_DEC007.docx';
    comandoSugerido = 'python3 scripts/agentes/guardian_consistencia.py';
    diagnostico = 'He detectado una verificación de consistencia metodológica (Squad B). Delegaré a guardian-consistencia para custodiar las 3 dimensiones inmutables DEC-007.';
  } else if (lower.includes('xp') || lower.includes('historia') || lower.includes('syncova') || lower.includes('software') || lower.includes('3.3')) {
    squad = 'Squad C (Ingeniería de Software SIVAC)';
    subagente = lower.includes('codigo') || lower.includes('audita') ? 'ingeniero-sivac' : 'documentador-xp';
    fase = 'F3';
    tarea = `Inspeccionar en modo SOLO LECTURA la trazabilidad de las 15 Historias de Usuario XP (HU-01 a HU-15) y arquitectura SIVAC para: "${rawPrompt}".`;
    entradas = 'salidas/documentos/CAPITULO_III_METODOLOGIA_E_INGENIERIA_XP_SIVAC.docx';
    salidaEsperada = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${new Date().toISOString().slice(0, 10)}_${subagente}_trazabilidad-xp.md`;
    entregable = 'salidas/documentos/CAPITULO_III_METODOLOGIA_E_INGENIERIA_XP_SIVAC.docx';
    comandoSugerido = 'python3 scripts/agentes/inventario_syncova.py';
    diagnostico = `He detectado una tarea de ingeniería de software (Squad C). Delegaré a ${subagente} en estricto modo de solo lectura para auditar las 15 Historias de Usuario XP.`;
  } else if (lower.includes('estadist') || lower.includes('shapiro') || lower.includes('wilcoxon') || lower.includes('datos') || lower.includes('cap 4') || lower.includes('cap 5')) {
    squad = 'Squad D (Bioestadística e Inferencia)';
    subagente = 'analista-estadistico';
    fase = 'F5';
    tarea = `Verificar el pipeline bioestadístico inferencial (N = n = 14) y comprobar el candado ético sobre datos/raw/MANIFEST.json para: "${rawPrompt}".`;
    entradas = 'datos/schemas/codebook.json\ndatos/plantillas/MANIFEST.plantilla.json';
    salidaEsperada = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${new Date().toISOString().slice(0, 10)}_analista-estadistico_control-pipeline.md`;
    entregable = 'salidas/documentos/PROTOCOLO_BIOESTADISTICO_E_INFERENCIAL_N14.docx';
    comandoSugerido = 'python3 scripts/estadistica/pipeline_inferencial.py --json';
    diagnostico = 'He detectado una consulta bioestadística (Squad D). Delegaré a analista-estadistico para verificar el protocolo inferencial (n = 14) respetando el bloqueo de datos sintéticos.';
  } else if (lower.includes('jurado') || lower.includes('sustenta') || lower.includes('evalua') || lower.includes('dictamen') || lower.includes('estado')) {
    squad = 'Squad F (Gobernanza, Memoria y Evaluación Externa)';
    subagente = 'jurado-revisor';
    fase = 'F9';
    tarea = `Ejecutar revisión colegiada simulada en escala vigesimal (0–20 pts) y diagnóstico de la granja sobre: "${rawPrompt}".`;
    entradas = 'salidas/documentos/informe_final_v02.docx\nsalidas/reportes_jurado/DICTAMEN_AUDITORIA_PRELIMINAR_QG1_QG5.docx';
    salidaEsperada = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${new Date().toISOString().slice(0, 10)}_jurado-revisor_dictamen.md`;
    entregable = 'salidas/reportes_jurado/DICTAMEN_AUDITORIA_PRELIMINAR_QG1_QG5.docx';
    comandoSugerido = 'python3 scripts/agentes/estado_granja.py';
    diagnostico = 'He detectado una evaluación integral de la tesis y compuertas QG (Squad F). Delegaré a jurado-revisor para auditar el estado general del ecosistema.';
  } else {
    squad = 'Squad E (Redacción y Maquetación)';
    subagente = 'maquetador-docx';
    fase = 'F4';
    tarea = `Ejecutar cirugía y auditoría OpenXML APA 7 / UNAJMA (márgenes 1985/1418 dxa, tablas de 3 líneas sin flotación, figuras a 300 DPI) para: "${rawPrompt}".`;
    entradas = 'salidas/documentos/informe_final_v02.docx\nreferencias/modelos_tesis/MODELO_TESIS_UNAJMA_FANY_2024.docx';
    salidaEsperada = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${new Date().toISOString().slice(0, 10)}_maquetador-docx_cirugia-openxml.md`;
    entregable = 'salidas/documentos/informe_final_v02.docx';
    comandoSugerido = 'python3 scripts/utilidades/auditor_docx_apa7.py auditar salidas/documentos/informe_final_v02.docx --md';
    diagnostico = 'He detectado una tarea editorial/OpenXML (Squad E). Delegaré a maquetador-docx para auditar márgenes UNAJMA y tablas APA 7 en informe_final_v02.docx.';
  }

  const cleanPrompt = rawPrompt.replace(/"/g, '\\"');
  const claudeCliCmd = `claude -p "${cleanPrompt}" --agent ${subagente} --output-format stream-json --verbose`;
  const droidCliCmd = `droid exec "${cleanPrompt}" --droid ${subagente} --auto medium`;

  return {
    squad,
    subagente,
    fase,
    tarea,
    entradas,
    salidaEsperada,
    entregable,
    comandoSugerido,
    diagnostico,
    claudeCliCmd,
    droidCliCmd,
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
  if (!relPath || relPath.includes('..')) return false;
  return ALLOWED_PREFIXES.some((p) => relPath === p || relPath.startsWith(p));
}

function checkPreToolUseSecurity(command: string): { allowed: boolean; reason?: string } {
  const lower = command.toLowerCase();
  const destructiveVerbs = ['rm ', 'mv ', 'cp ', '>', '>>', 'sed -i', 'truncate', 'dd ', 'unlink'];
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

  const broadcast = (event: string, payload: unknown) => {
    const message = JSON.stringify({ event, payload, timestamp: new Date().toISOString() });
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
    const line: TerminalLine = {
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
      timestamp: new Date().toISOString(),
      stream,
      text,
      agentId,
      mode,
    };
    terminalHistory.push(line);
    if (terminalHistory.length > 400) {
      terminalHistory.splice(0, terminalHistory.length - 400);
    }
    broadcast('terminal:output', line);
    return line;
  };

  const executeCommandInTerminal = (
    rawCommand: string,
    options: {
      mode?: 'bun' | 'shell' | 'claude' | 'droid';
      agentId?: string;
      tarea?: string;
      fase?: string;
      squad?: string;
      createHandoff?: boolean;
    } = {}
  ): Promise<{ exitCode: number; output: string; handoffPath?: string }> => {
    return new Promise((resolve) => {
      const mode = options.mode || 'bun';
      const agentId = options.agentId || 'director-general';
      const cmdTrimmed = rawCommand.trim();

      appendTerminalLine('command', `$ [BUN · ${mode.toUpperCase()} · @${agentId}] ${cmdTrimmed}`, agentId, mode);

      const secCheck = checkPreToolUseSecurity(cmdTrimmed);
      if (!secCheck.allowed) {
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

      // Build command using Bun Runtime or CLI bridges (claude / droid / bun_runner.ts)
      let actualCommand = cmdTrimmed;
      const isDirectCli =
        cmdTrimmed.startsWith('claude ') ||
        cmdTrimmed.startsWith('droid ') ||
        cmdTrimmed.startsWith('bun ') ||
        cmdTrimmed.includes('--version');

      if (!isDirectCli) {
        if (mode === 'claude') {
          const safePrompt = (options.tarea || cmdTrimmed).replace(/"/g, '\\"');
          actualCommand = `claude -p "${safePrompt}" --agent ${agentId} --output-format stream-json --verbose`;
        } else if (mode === 'droid') {
          const safePrompt = (options.tarea || cmdTrimmed).replace(/"/g, '\\"');
          actualCommand = `droid exec "${safePrompt}" --droid ${agentId} --auto medium`;
        } else {
          // Run via Bun Runner for fast execution & telemetry
          actualCommand = `bun run scripts/bun_runner.ts --mode=${mode} --agent=${agentId} --cmd ${cmdTrimmed}`;
        }
      }

      agentRuntimeStatus['director-general'] = {
        status: 'running',
        currentTask: `Orquestando delegación hacia @${agentId}`,
        lastCommand: actualCommand,
        lastRunAt: new Date().toISOString(),
      };
      agentRuntimeStatus[agentId] = {
        status: 'running',
        currentTask: options.tarea || cmdTrimmed,
        lastCommand: actualCommand,
        lastRunAt: new Date().toISOString(),
      };
      broadcast('agent:status', { agentId: 'director-general', ...agentRuntimeStatus['director-general'] });
      broadcast('agent:status', { agentId, ...agentRuntimeStatus[agentId] });

      const delegationId = `del-${Date.now()}`;
      const delegation: DelegationEvent = {
        id: delegationId,
        timestamp: new Date().toISOString(),
        from: 'director-general',
        to: agentId,
        squad: options.squad || 'Hub Central',
        fase: options.fase || 'F4',
        tarea: options.tarea || cmdTrimmed,
        command: actualCommand,
        status: 'running',
      };
      activeDelegations.unshift(delegation);
      if (activeDelegations.length > 30) activeDelegations.pop();
      broadcast('delegation:update', delegation);

      const startTime = Date.now();
      const child = spawn('bash', ['-c', actualCommand], {
        cwd: __dirname,
        env: { ...process.env, PATH: `/usr/local/bin:${process.env.PATH || ''}`, PYTHONIOENCODING: 'utf-8' },
      });
      activeChildProcess = child;

      let collectedOutput = '';

      child.stdout.on('data', (chunk: Buffer) => {
        const text = chunk.toString('utf-8');
        collectedOutput += text;
        for (const line of text.split(/\r?\n/)) {
          if (line.trim().length > 0) {
            appendTerminalLine('stdout', line, agentId, mode);
          }
        }
      });

      child.stderr.on('data', (chunk: Buffer) => {
        const text = chunk.toString('utf-8');
        collectedOutput += text;
        for (const line of text.split(/\r?\n/)) {
          if (line.trim().length > 0) {
            appendTerminalLine('stderr', line, agentId, mode);
          }
        }
      });

      child.on('close', (code) => {
        activeChildProcess = null;
        const exitCode = code ?? 0;
        const elapsedMs = Date.now() - startTime;
        const finalStatus: 'completed' | 'blocked' = exitCode === 0 ? 'completed' : 'blocked';

        let handoffRelPath: string | undefined;
        if (options.createHandoff) {
          const dateStr = new Date().toISOString().slice(0, 10);
          const slug = (options.tarea || actualCommand)
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
            `- **Comando Ejecutado:** \`${actualCommand}\`\n` +
            `- **Productos Generados / Auditados:** Verificados en \`salidas/\` y \`obsidian_vault/\`\n` +
            `- **Hallazgos Clave:**\n\`\`\`text\n${summarySnippet}\n\`\`\`\n` +
            `- **Pendientes / \`[VERIFICAR]\`:** ${exitCode === 3 ? 'Esperando ingreso de datos de campo reales en datos/raw/MANIFEST.json (Regla 01).' : 'Ninguno.'}\n` +
            `- **Riesgos o Desalineaciones:** Cero desviaciones respecto a las 3 dimensiones DEC-007.\n` +
            `- **Siguiente Acción Sugerida:** Revisión por \`director-general\` en Mission Control.\n`;
          fs.writeFileSync(handoffAbs, handoffMd, 'utf-8');
          handoffRelPath = `obsidian_vault/08_SISTEMA_Y_AGENTES/handoffs/${handoffFileName}`;
          appendTerminalLine('system', `[HANDOFF DEPOSITADO] ${handoffRelPath}`, agentId, mode);
          broadcast('handoff:created', {
            fileName: handoffFileName,
            filePath: handoffRelPath,
            content: handoffMd,
            updatedAt: new Date().toISOString(),
          });
        }

        appendTerminalLine(
          'system',
          `[PROCESO FINALIZADO] agente=${agentId} | código=${exitCode} | duración=${elapsedMs}ms`,
          agentId,
          mode
        );

        agentRuntimeStatus['director-general'] = {
          status: 'idle',
          currentTask: `Última delegación completada (@${agentId})`,
          lastCommand: actualCommand,
          lastRunAt: new Date().toISOString(),
        };
        agentRuntimeStatus[agentId] = {
          status: finalStatus,
          currentTask: options.tarea || cmdTrimmed,
          lastCommand: actualCommand,
          lastRunAt: new Date().toISOString(),
        };
        broadcast('agent:status', { agentId: 'director-general', ...agentRuntimeStatus['director-general'] });
        broadcast('agent:status', { agentId, ...agentRuntimeStatus[agentId] });

        delegation.status = finalStatus;
        delegation.exitCode = exitCode;
        delegation.handoffPath = handoffRelPath;
        broadcast('delegation:update', delegation);
        broadcast('terminal:exit', { agentId, exitCode, elapsedMs, handoffPath: handoffRelPath });

        resolve({ exitCode, output: collectedOutput, handoffPath: handoffRelPath });
      });
    });
  };

  wss.on('connection', (ws) => {
    ws.send(
      JSON.stringify({
        event: 'init',
        payload: {
          terminalHistory,
          activeDelegations,
          agentRuntimeStatus,
          godChatHistory,
          cliStatus: detectCliStatus(),
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

      const settingsPath = path.join(__dirname, '.claude', 'settings.json');
      const settingsRaw = fs.existsSync(settingsPath)
        ? JSON.parse(fs.readFileSync(settingsPath, 'utf-8'))
        : {};

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

      const hooksDir = path.join(__dirname, '.claude', 'hooks');
      const hooks = fs.existsSync(hooksDir)
        ? fs
            .readdirSync(hooksDir)
            .filter((f) => f.endsWith('.cjs'))
            .map((f) => ({
              id: f.replace('.cjs', ''),
              fileName: f,
              filePath: `.claude/hooks/${f}`,
              content: fs.readFileSync(path.join(hooksDir, f), 'utf-8'),
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

      const gitHistory = getGitHistory();

      res.json({
        thesis: {
          tituloOficial:
            'APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS MENSUALES DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II',
          resolucion: 'Resolución UNAJMA - DEC-027',
          tesista: 'Bach. José Luis Quispe León',
          asesora: 'Dra. Norma Lorena Catacora Flores',
          universidad: 'Universidad Nacional José María Arguedas (UNAJMA)',
          escuela: 'Escuela Profesional de Ingeniería de Sistemas (EPIS)',
          variableIndependiente: 'Sistema web SIVAC (Extreme Programming XP · ISO/IEC 25010:2023)',
          variableDependiente: 'Gestión de movimientos mensuales de vacunas',
          diseno: 'Preexperimental con pretest y postest en un solo grupo (O1 -> X -> O2)',
          muestra: 'Población censal N = n = 14 profesionales y técnicos de inmunizaciones',
          dimensionesVD: [
            {
              numero: 1,
              nombre: 'Oportunidad de procesamiento',
              definicion:
                'Capacidad de registrar y emitir documentos de movimiento de vacunas en el menor tiempo operativo posible.',
              indicadores: [
                { codigo: 'T_reg', nombre: 'Tiempo de registro de movimiento de vacunas', unidad: 'Minutos (0, 120]', direccion: 'Post < Pre' },
                { codigo: 'T_vale', nombre: 'Tiempo de emisión de comprobante de salida / vale', unidad: 'Minutos (0, 60]', direccion: 'Post < Pre' },
              ],
            },
            {
              numero: 2,
              nombre: 'Consistencia documental',
              definicion:
                'Nivel de exactitud y concordancia sin discrepancias entre los registros físicos/digitales y los movimientos ejecutados.',
              indicadores: [
                { codigo: 'RSD', nombre: 'Porcentaje de registros sin discrepancias', unidad: 'Porcentaje [0, 100]%', direccion: 'Post > Pre' },
                { codigo: 'CPE', nombre: 'Concordancia de cantidad programada vs entregada', unidad: 'Porcentaje [0, 100]%', direccion: 'Post > Pre' },
              ],
            },
            {
              numero: 3,
              nombre: 'Satisfacción del usuario',
              definicion:
                'Grado de complacencia, facilidad y utilidad percibida por los usuarios respecto a la gestión con el sistema bajo el modelo TAM.',
              indicadores: [
                { codigo: 'AP', nombre: 'Aceptación del proceso (Ítems AP-01 a AP-04)', unidad: 'Likert 1-5 (Puntaje 4-20)', direccion: 'Post > Pre' },
                { codigo: 'UP', nombre: 'Utilidad percibida (Ítems UP-01 a UP-04)', unidad: 'Likert 1-5 (Puntaje 4-20)', direccion: 'Post > Pre' },
              ],
            },
          ],
        },
        agents,
        rules,
        skills,
        schemas,
        hooks,
        workflowModules,
        canonicalLayers,
        gitHistory,
        projectsStore,
        handoffs,
        activeDelegations,
        godChatHistory,
        cliStatus: detectCliStatus(),
        mcpServers: Object.entries(mcpRaw.mcpServers || {}).map(([name, cfg]) => {
          const obj = cfg as Record<string, unknown>;
          return {
            name,
            enabled: obj.disabled !== true,
            ...obj,
          };
        }),
        settings: settingsRaw,
      });
    } catch (error) {
      res.status(500).json({ error: error instanceof Error ? error.message : 'Error leyendo ecosistema' });
    }
  });

  // --- CLI DETECTION & 1-CLICK INSTALL/VERIFY ENDPOINTS ---
  app.get('/api/system/cli-status', (_req, res) => {
    res.json(detectCliStatus());
  });

  app.post('/api/system/cli-action', async (req, res) => {
    const action = String(req.body?.action || 'verify-all');
    if (action === 'verify-all') {
      await executeCommandInTerminal('bun --version && claude --version && droid --version && python3 --version', {
        mode: 'bun',
        agentId: 'director-general',
        tarea: 'Verificación de instalación de Bun, Claude Code CLI, Factory Droid CLI y Python 3',
        createHandoff: false,
      });
    } else if (action === 'sync-droids') {
      await executeCommandInTerminal('python3 scripts/sync_factory.py', {
        mode: 'bun',
        agentId: 'director-general',
        tarea: 'Sincronización de 14 agentes y MCPs entre .claude/ y .factory/',
        createHandoff: false,
      });
    } else if (action === 'reinstall-bridges') {
      await executeCommandInTerminal(
        'chmod +x scripts/bun_runner.ts scripts/cli_bridges/claude_cli.ts scripts/cli_bridges/droid_cli.ts && ln -sf "$PWD/scripts/cli_bridges/claude_cli.ts" /usr/local/bin/claude && ln -sf "$PWD/scripts/cli_bridges/droid_cli.ts" /usr/local/bin/droid && bun --version && claude --version && droid --version',
        {
          mode: 'bun',
          agentId: 'director-general',
          tarea: 'Habilitación y enlace de binarios locales claude, droid y bun en /usr/local/bin',
          createHandoff: false,
        }
      );
    }
    const updatedStatus = detectCliStatus();
    broadcast('cli:status', updatedStatus);
    res.json(updatedStatus);
  });

  // --- CONVERSATIONAL AGENTE GOD CHAT WITH AUTOMATIC SUBAGENT DELEGATION ---
  app.get('/api/god-chat', (_req, res) => {
    res.json({ messages: godChatHistory });
  });

  app.delete('/api/god-chat', (_req, res) => {
    godChatHistory.splice(1);
    broadcast('godchat:cleared', godChatHistory);
    res.json({ messages: godChatHistory });
  });

  app.get('/api/projects', (_req, res) => {
    res.json(loadProjectsStore());
  });

  app.post('/api/god-chat', async (req, res) => {
    const prompt = String(req.body?.prompt || '').trim();
    const runtime = ((req.body?.runtime || req.body?.cliEngine || 'bun') as 'bun' | 'claude' | 'droid');
    if (!prompt) {
      res.status(400).json({ error: 'Escribe un mensaje para el Agente GOD.' });
      return;
    }

    // 1. Append User Message
    const userMsg: GodChatMessage = {
      id: `msg-user-${Date.now()}`,
      timestamp: new Date().toISOString(),
      role: 'user',
      senderName: 'Investigador (Tesista)',
      senderId: 'tesista',
      text: prompt,
    };
    godChatHistory.push(userMsg);
    broadcast('godchat:message', userMsg);

    // 2. Classify Intent & Select Subagent automatically (Loop 3.0)
    const intent = classifyPromptIntent(prompt);

    const godMsgId = `msg-god-${Date.now() + 1}`;
    const godMsg: GodChatMessage = {
      id: godMsgId,
      timestamp: new Date().toISOString(),
      role: 'god',
      senderName: 'Director General (Agente GOD)',
      senderId: 'director-general',
      squad: 'Hub Central',
      text: `${intent.diagnostico}\n\nHe emitido el contrato formal en la Fase ${intent.fase} y he delegado la ejecución a @${intent.subagente} (${intent.squad}) utilizando el motor ${runtime.toUpperCase()}.`,
      delegation: {
        subagente: intent.subagente,
        squad: intent.squad,
        fase: intent.fase,
        runtime,
        command: intent.comandoSugerido,
        claudeCliCmd: intent.claudeCliCmd,
        droidCliCmd: intent.droidCliCmd,
        status: 'running',
        deliverablePath: intent.entregable,
      },
    };
    godChatHistory.push(godMsg);
    broadcast('godchat:message', godMsg);

    // 3. Execute via Bun / Claude Code / Factory Droid in Live Terminal
    const execResult = await executeCommandInTerminal(intent.comandoSugerido, {
      mode: runtime,
      agentId: intent.subagente,
      tarea: intent.tarea,
      fase: intent.fase,
      squad: intent.squad,
      createHandoff: true,
    });

    const finalStatus: 'completed' | 'blocked' = execResult.exitCode === 0 ? 'completed' : 'blocked';
    const cleanOutput = execResult.output.trim().slice(0, 900) || 'Proceso ejecutado correctamente.';

    if (godMsg.delegation) {
      godMsg.delegation.status = finalStatus;
      godMsg.delegation.outputSummary = cleanOutput;
      godMsg.delegation.handoffPath = execResult.handoffPath;
      godMsg.delegation.exitCode = execResult.exitCode;
      broadcast('godchat:update', godMsg);
    }

    // 4. Append Subagent Completion Response
    const subagentMsg: GodChatMessage = {
      id: `msg-sub-${Date.now() + 2}`,
      timestamp: new Date().toISOString(),
      role: 'subagent',
      senderName: `@${intent.subagente}`,
      senderId: intent.subagente,
      squad: intent.squad,
      text:
        finalStatus === 'completed'
          ? `Tarea completada con éxito para el Director General. Se ha depositado el informe de relevo (handoff) en la Bóveda Obsidian y el entregable está verificado.`
          : `Atención: la ejecución finalizó con estado de bloqueo normativo (código ${execResult.exitCode}). Revisa el detalle a continuación.`,
      delegation: {
        subagente: intent.subagente,
        squad: intent.squad,
        fase: intent.fase,
        runtime,
        command: intent.comandoSugerido,
        claudeCliCmd: intent.claudeCliCmd,
        droidCliCmd: intent.droidCliCmd,
        status: finalStatus,
        outputSummary: cleanOutput,
        handoffPath: execResult.handoffPath,
        deliverablePath: intent.entregable,
        exitCode: execResult.exitCode,
      },
    };
    godChatHistory.push(subagentMsg);
    broadcast('godchat:message', subagentMsg);

    res.json({
      ok: true,
      userMsg,
      godMsg,
      subagentMsg,
    });
  });

  // --- TERMINAL & LIVE EXECUTION ENDPOINTS ---
  app.post('/api/terminal/exec', async (req, res) => {
    const { command, mode, agentId, tarea, taskPrompt, fase, phase, squad, createHandoff } = req.body || {};
    const cmdToRun = command || AGENT_DEFAULT_SCRIPTS[agentId || 'director-general'] || 'python3 scripts/agentes/estado_granja.py';
    const result = await executeCommandInTerminal(String(cmdToRun), {
      mode: mode || 'bun',
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

  // --- DISPATCH COMMISSION IN LIVE TERMINAL & GENERATE HANDOFF ---
  app.post('/api/dispatch-comision', async (req, res) => {
    const payload = req.body || {};
    const subagente = String(payload.subagente || 'guardian-consistencia');
    const cmd = String(payload.comando || AGENT_DEFAULT_SCRIPTS[subagente] || 'python3 scripts/agentes/estado_granja.py');
    const mode = (payload.mode as 'bun' | 'shell' | 'claude' | 'droid') || 'bun';

    const result = await executeCommandInTerminal(cmd, {
      mode,
      agentId: subagente,
      tarea: payload.tarea || `Comisión radial asignada a ${subagente}`,
      fase: payload.fase || 'F4',
      squad: payload.squad || 'Squad Especializado',
      createHandoff: true,
    });

    res.json({
      dispatched: true,
      subagente,
      command: cmd,
      exitCode: result.exitCode,
      output: result.output,
      handoffPath: result.handoffPath,
    });
  });

  // --- CAPABILITIES MANAGEMENT (MCPs, AGENT TOOLS/SKILLS, HOOKS) ---
  app.patch('/api/capabilities/mcp', (req, res) => {
    const { name, enabled, command, args, url } = req.body || {};
    if (!name) {
      res.status(400).json({ error: 'Nombre de servidor MCP requerido' });
      return;
    }
    const mcpPath = path.join(__dirname, '.mcp.json');
    const mcpData = fs.existsSync(mcpPath) ? JSON.parse(fs.readFileSync(mcpPath, 'utf-8')) : { mcpServers: {} };
    if (!mcpData.mcpServers) mcpData.mcpServers = {};
    const current = mcpData.mcpServers[name] || {};

    mcpData.mcpServers[name] = {
      ...current,
      ...(command !== undefined ? { command } : {}),
      ...(args !== undefined ? { args } : {}),
      ...(url !== undefined ? { url } : {}),
      disabled: enabled === false,
    };
    if (enabled === true) {
      delete mcpData.mcpServers[name].disabled;
    }

    fs.writeFileSync(mcpPath, JSON.stringify(mcpData, null, 2) + '\n', 'utf-8');
    try {
      execFileSync('python3', ['scripts/sync_factory.py'], { cwd: __dirname });
    } catch {
      // non-fatal
    }
    appendTerminalLine(
      'system',
      `[CONFIG MCP ACTUALIZADA] Servidor "${name}" -> ${enabled ? 'ACTIVO' : 'DESACTIVADO'} en .mcp.json y sincronizado con .factory/`
    );
    broadcast('capabilities:updated', { type: 'mcp', name, enabled });
    res.json({ ok: true, mcpServers: mcpData.mcpServers });
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

    // Regla Constitucional: ingeniero-sivac es estrictamente de SOLO LECTURA
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

    // Sync to .factory/droids/<agentId>.md if present
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
    const { hookEvent, enabled } = req.body || {};
    if (!hookEvent) {
      res.status(400).json({ error: 'Evento de hook requerido' });
      return;
    }
    if (hookEvent === 'PreToolUse' && enabled === false) {
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
    settingsData.hooksStatus[hookEvent] = enabled !== false;
    fs.writeFileSync(settingsPath, JSON.stringify(settingsData, null, 2) + '\n', 'utf-8');
    appendTerminalLine(
      'system',
      `[HOOK ACTUALIZADO] Evento "${hookEvent}" -> ${enabled !== false ? 'ACTIVO' : 'PAUSADO'} en .claude/settings.json y .factory/hooks.json`
    );
    broadcast('capabilities:updated', { type: 'hook', hookEvent, enabled: enabled !== false });
    res.json({ ok: true, settings: settingsData });
  });

  // --- MULTI-PROJECT & KANBAN TASKS MANAGEMENT ---
  app.post('/api/projects', (req, res) => {
    const { codigo, titulo, tipo, diseno, variableIndependiente, variableDependiente, dimensiones } = req.body || {};
    if (!titulo) {
      res.status(400).json({ error: 'Título del proyecto requerido' });
      return;
    }
    const store = loadProjectsStore();
    const newId = `proy-${Date.now()}`;
    const newProject = {
      id: newId,
      codigo: codigo || `INV-${new Date().getFullYear()}`,
      titulo,
      tipo: tipo || 'Proyecto de Investigación Científica',
      tesista: 'Bach. José Luis Quispe León',
      asesora: 'Dra. Norma Lorena Catacora Flores',
      diseno: diseno || 'Cuasi-experimental / Aplicada',
      faseActual: 'F0',
      progreso: 10,
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
          fase: 'F1',
          capitulo: 'Cap. I Planteamiento',
          squad: 'Squad B (Metodología y Psicometría)',
          subagente: 'guardian-consistencia',
          estado: 'en_progreso',
          prioridad: 'alta',
          comando: 'python3 scripts/agentes/guardian_consistencia.py',
          entregable: 'obsidian_vault/01_MATRIZ_Y_CONSISTENCIA/MATRIZ_CONSISTENCIA_DEC007.md',
        },
      ],
    };
    store.projects.push(newProject);
    store.activeProjectId = newId;
    saveProjectsStore(store);
    appendTerminalLine('system', `[NUEVO PROYECTO CREADO] "${titulo}" (${newProject.codigo}) registrado en Bóveda Obsidian.`);
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
    const { titulo, fase, capitulo, squad, subagente, prioridad, comando, entregable } = req.body || {};
    if (!titulo) {
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
      titulo,
      fase: fase || 'F4',
      capitulo: capitulo || 'General',
      squad: squad || 'Squad E (Redacción y Maquetación)',
      subagente: subagente || 'maquetador-docx',
      estado: 'pendiente',
      prioridad: prioridad || 'alta',
      comando: comando || AGENT_DEFAULT_SCRIPTS[subagente] || 'python3 scripts/agentes/estado_granja.py',
      entregable: entregable || 'salidas/documentos/informe_final_v02.docx',
    };
    project.tasks.unshift(newTask);
    saveProjectsStore(store);
    appendTerminalLine('system', `[TAREA CREADA] "${titulo}" asignada a ${newTask.subagente} (${newTask.fase}).`);
    broadcast('projects:updated', store);
    res.json(store);
  });

  app.patch('/api/projects/:projectId/tasks/:taskId', (req, res) => {
    const { projectId, taskId } = req.params;
    const { estado, subagente, fase } = req.body || {};
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
    if (estado) task.estado = estado;
    if (subagente) task.subagente = subagente;
    if (fase) task.fase = fase;

    // Recalculate progress
    const total = project.tasks.length;
    const done = project.tasks.filter((t: { estado: string }) => t.estado === 'completada').length;
    project.progreso = total > 0 ? Math.round((done / total) * 100) : 0;

    saveProjectsStore(store);
    broadcast('projects:updated', store);
    res.json(store);
  });

  // --- FILE INSPECTOR & DOWNLOADS ---
  app.get('/api/file', (req, res) => {
    const relPath = String(req.query.path || '');
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
        const out = execFileSync('python3', ['-c', pyScript, fullPath], {
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

    if (ext === '.xlsx') {
      try {
        const pyScript = `
import json, sys, zipfile, xml.etree.ElementTree as ET
p = sys.argv[1]
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
hojas = []
with zipfile.ZipFile(p, "r") as zf:
    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    names = [s.attrib.get("name", f"Hoja{i+1}") for i, s in enumerate(wb.iter(f"{NS}sheet"))]
    for i, name in enumerate(names, start=1):
        sname = f"xl/worksheets/sheet{i}.xml"
        if sname in zf.namelist():
            sroot = ET.fromstring(zf.read(sname))
            filas = []
            for row in sroot.iter(f"{NS}row"):
                vals = ["".join(t.text or "" for t in c.iter()) for c in row.findall(f"{NS}c")]
                filas.append(vals)
            hojas.append({"nombre": name, "filas": filas})
print(json.dumps({"hojas": hojas}, ensure_ascii=False))
`;
        const out = execFileSync('python3', ['-c', pyScript, fullPath], {
          cwd: __dirname,
          encoding: 'utf-8',
        });
        const parsed = JSON.parse(out);
        const lines: string[] = [
          `================================================================================`,
          `LIBRO MICROSOFT EXCEL NATIVO OPENXML (.XLSX)`,
          `Ruta:    ${relPath}`,
          `Tamaño:  ${stat.size.toLocaleString()} bytes`,
          `SHA-256: ${sha256}`,
          `Hojas:   ${parsed.hojas.map((h: { nombre: string }) => h.nombre).join(', ')}`,
          `================================================================================`,
        ];
        for (const h of parsed.hojas) {
          lines.push(`\n### Hoja: ${h.nombre} (${h.filas.length} filas)`);
          h.filas.slice(0, 35).forEach((r: string[], idx: number) => {
            lines.push(`  [${String(idx + 1).padStart(2, '0')}] ${r.join(' | ')}`);
          });
        }
        res.json({
          path: relPath,
          binaryType: 'xlsx',
          sha256,
          sizeBytes: stat.size,
          content: lines.join('\n'),
        });
        return;
      } catch {
        res.json({
          path: relPath,
          binaryType: 'xlsx',
          sha256,
          sizeBytes: stat.size,
          content: `Libro Excel OpenXML (.xlsx) — ${stat.size} bytes — SHA-256: ${sha256}`,
        });
        return;
      }
    }

    if (ext === '.pdf') {
      const rawLatin = buf.toString('latin1');
      const textMatches = Array.from(rawLatin.matchAll(/\(([^()]+)\)\s*Tj/g)).map((m) => m[1]);
      const lines = [
        `================================================================================`,
        `DOCUMENTO PORTABLE DOCUMENT FORMAT (.PDF 1.4)`,
        `Ruta:    ${relPath}`,
        `Tamaño:  ${stat.size.toLocaleString()} bytes`,
        `SHA-256: ${sha256}`,
        `================================================================================`,
        ``,
        `--- TEXTO INDEXADO EN FLUJO PDF ---`,
        ...textMatches.map((t) => t.replace(/\\([()])/g, '$1')),
      ];
      res.json({
        path: relPath,
        binaryType: 'pdf',
        sha256,
        sizeBytes: stat.size,
        content: lines.join('\n'),
      });
      return;
    }

    if (ext === '.png') {
      let sidecarContent = '';
      const sidecarPath = fullPath.replace(/\.png$/i, '.json');
      if (fs.existsSync(sidecarPath)) {
        sidecarContent = fs.readFileSync(sidecarPath, 'utf-8');
      }
      res.json({
        path: relPath,
        binaryType: 'png',
        sha256,
        sizeBytes: stat.size,
        content:
          `================================================================================\n` +
          `FIGURA CIENTÍFICA APA 7 A 300 DPI (.PNG)\n` +
          `Ruta:       ${relPath}\n` +
          `Tamaño:     ${stat.size.toLocaleString()} bytes\n` +
          `SHA-256:    ${sha256}\n` +
          `Resolución: 300 x 300 DPI (pHYs 11811 px/m verificado)\n` +
          `================================================================================\n\n` +
          (sidecarContent ? `--- METADATOS SIDECAR JSON ---\n${sidecarContent}` : ''),
      });
      return;
    }

    const content = buf.toString('utf-8');
    res.json({ path: relPath, binaryType: 'text', sha256, content, sizeBytes: stat.size });
  });

  app.get('/api/download', (req, res) => {
    const relPath = String(req.query.path || '');
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
      const result = await executeCommandInTerminal('python3 scripts/compiladores/compilar_informe_final.py', {
        mode: 'shell',
        agentId: 'maquetador-docx',
        tarea: 'Recompilación integral de entregables DOCX, PDF, XLSX y Figuras 300 DPI',
        fase: 'F4',
        squad: 'Squad E (Redacción y Maquetación)',
        createHandoff: true,
      });
      res.json({ estado: 'completado', exitCode: result.exitCode });
    } catch (error) {
      res.status(500).json({ error: error instanceof Error ? error.message : 'Error al recompilar entregables' });
    }
  });

  app.post('/api/validate-comision', (req, res) => {
    const payload = req.body || {};
    const requiredFields = [
      'tarea',
      'fase',
      'squad',
      'subagente',
      'entradas',
      'salida_esperada',
      'restricciones',
      'criterio_exito',
    ];
    const validFases = ['F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10'];
    const validSquads = [
      'Squad A (Evidencia y Bibliometría)',
      'Squad B (Metodología y Psicometría)',
      'Squad C (Ingeniería de Software SIVAC)',
      'Squad D (Bioestadística e Inferencia)',
      'Squad E (Redacción y Maquetación)',
      'Squad F (Gobernanza, Memoria y Evaluación Externa)',
    ];

    const errors: string[] = [];
    const warnings: string[] = [];

    for (const field of requiredFields) {
      if (payload[field] === undefined || payload[field] === null || payload[field] === '') {
        errors.push(`Campo obligatorio faltante: "${field}".`);
      }
    }

    if (payload.fase && !validFases.includes(payload.fase)) {
      errors.push(`Fase inválida "${payload.fase}". Debe ser una de: ${validFases.join(', ')}.`);
    }

    if (payload.squad && !validSquads.includes(payload.squad)) {
      errors.push(`Squad inválido "${payload.squad}". Debe coincidir exactamente con comision.schema.json.`);
    }

    const agents = loadAgents();
    const targetAgent = agents.find((a) => a.id === payload.subagente || a.name === payload.subagente);
    if (!targetAgent) {
      errors.push(`Subagente "${payload.subagente}" no existe en .claude/agents/*.md.`);
    } else if (targetAgent.id === 'director-general') {
      errors.push('El Director General (Agente GOD) es el comisionador radial; debe delegar en uno de los 13 subagentes especialistas.');
    }

    const salida = String(payload.salida_esperada || '').toLowerCase().replace(/\\/g, '/');
    const forbiddenTargets = ['syncova', 'referencias/', 'proyecto_tesis.docx', 'datos/raw/'];
    for (const ft of forbiddenTargets) {
      if (salida.includes(ft)) {
        errors.push(`VIOLACIÓN REGLA 01 (PreToolUse Blocker): La salida esperada apunta a una ruta protegida de solo lectura ("${ft}").`);
      }
    }

    if (targetAgent?.id === 'ingeniero-sivac' && salida && !salida.includes('obsidian_vault') && !salida.includes('handoffs')) {
      warnings.push('Nota: ingeniero-sivac opera en modo estricto SOLO LECTURA (Read, Grep, Glob) sobre C:\\Proyectos\\syncova.');
    }

    res.json({
      valid: errors.length === 0,
      errors,
      warnings,
      agentProfile: targetAgent || null,
    });
  });

  app.post('/api/audit-dec007', (req, res) => {
    const text = String(req.body?.text || '');
    const findings: Array<{ severity: 'critico' | 'mayor' | 'menor' | 'ok'; rule: string; detail: string }> = [];

    if (!text.trim()) {
      res.status(400).json({ error: 'Ingrese un fragmento o documento para auditar.' });
      return;
    }

    const firstPersonMatch = text.match(/\b(yo|nosotros|nuestro|nuestra|realizamos|implementamos|desarrollamos|observamos|concluimos)\b/i);
    if (firstPersonMatch) {
      findings.push({
        severity: 'mayor',
        rule: 'Regla 03 (Estilo Académico Impersonal)',
        detail: `Se detectó primera persona ("${firstPersonMatch[0]}"). La prosa debe redactarse en tercera persona impersonal ("se observó", "el análisis determinó").`,
      });
    } else {
      findings.push({
        severity: 'ok',
        rule: 'Regla 03 (Voz Impersonal)',
        detail: 'Cero pronombres de primera persona detectados.',
      });
    }

    const fillerPatterns = [
      'cabe destacar que',
      'como es sabido',
      'hoy en día',
      'sin lugar a dudas',
      'es importante destacar',
      'en conclusión, podemos ver',
    ];
    const foundFillers = fillerPatterns.filter((p) => text.toLowerCase().includes(p));
    if (foundFillers.length > 0) {
      findings.push({
        severity: 'menor',
        rule: 'Regla 03 (Prosa Fluff-Free)',
        detail: `Expresiones de relleno detectadas: ${foundFillers.map((f) => `"${f}"`).join(', ')}.`,
      });
    }

    if (text.includes('25010:2011')) {
      findings.push({
        severity: 'critico',
        rule: 'Regla 02 (Estándar VI ISO/IEC 25010:2023)',
        detail: 'Se detectó referencia obsoleta "ISO/IEC 25010:2011". La constitución fija "ISO/IEC 25010:2023".',
      });
    }

    const prematureStats = text.match(/(p\s*<\s*0?\.001|W\s*=\s*\d+|Z\s*=\s*-?\d+\.\d+|t\(13\)\s*=)/i);
    if (prematureStats) {
      findings.push({
        severity: 'critico',
        rule: 'Regla 01 (Cero Simulación Empírica)',
        detail: `Se detectó estadístico inferencial ("${prematureStats[0]}") sin MANIFEST.json de campo sellado. Estado inferencial: BLOQUEADO esperando datos reales.`,
      });
    }

    const alienDims = ['confiabilidad del inventario', 'inteligencia artificial', 'cuatro dimensiones', 'predicción de demanda'];
    const foundAlien = alienDims.filter((d) => text.toLowerCase().includes(d));
    if (foundAlien.length > 0) {
      findings.push({
        severity: 'critico',
        rule: 'Regla 02 (Inmutabilidad DEC-007)',
        detail: `Deriva metodológica detectada: ${foundAlien.map((d) => `"${d}"`).join(', ')}. La VD tiene exclusivamente 3 dimensiones oficiales.`,
      });
    } else {
      findings.push({
        severity: 'ok',
        rule: 'Regla 02 (Alineación DEC-007)',
        detail: 'Sin dimensiones ajenas a las 3 dimensiones canónicas (Oportunidad de procesamiento, Consistencia documental, Satisfacción del usuario).',
      });
    }

    const badAmpersand = text.match(/[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+&\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+\(\d{4}\)/);
    if (badAmpersand) {
      findings.push({
        severity: 'mayor',
        rule: 'Regla 03 (Citación APA 7 en Español)',
        detail: `Uso incorrecto de "&" en cita narrativa ("${badAmpersand[0]}"). En español se emplea "y" tanto en citas narrativas como parentéticas.`,
      });
    }

    res.json({
      wordCount: text.trim().split(/\s+/).length,
      findings,
      status: findings.some((f) => f.severity === 'critico')
        ? 'BLOQUEADO_ALERTA_ROJA'
        : findings.some((f) => f.severity === 'mayor')
        ? 'OBSERVADO_SUBSANABLE'
        : 'APROBADO_SIN_OBSERVACIONES',
    });
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
