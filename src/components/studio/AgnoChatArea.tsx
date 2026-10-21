import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  Send,
  Sparkles,
  Brain,
  Cpu,
  Terminal as TerminalIcon,
  CheckCircle2,
  Loader2,
  Trash2,
  FileText,
  ChevronRight,
  ChevronDown,
  Zap,
  Play,
  Bot,
  User,
  ArrowUpRight,
} from 'lucide-react';
import type {
  GodChatMessage,
  SubagentDelegation,
  AgentInfo,
  CliToolStatus,
} from '../../types/studio';

type ThinkingMode = 'auto' | 'think' | 'think_hard' | 'ultrathink';

interface ThinkingConfig {
  id: ThinkingMode;
  label: string;
  description: string;
  suffix: string;
}

const THINKING_MODES: ThinkingConfig[] = [
  {
    id: 'auto',
    label: 'Auto',
    description: 'Refinamiento cognitivo estándar',
    suffix: '',
  },
  {
    id: 'think',
    label: 'Think',
    description: 'Análisis metodológico paso a paso',
    suffix: ' [MODO: THINK - Analiza metodológicamente paso a paso]',
  },
  {
    id: 'think_hard',
    label: 'Think Hard',
    description: 'Cruce profundo con DEC-007 y ESTADO_TESIS.md',
    suffix: ' [MODO: THINK HARD - Cruza exhaustivamente con DEC-007 y ESTADO_TESIS.md]',
  },
  {
    id: 'ultrathink',
    label: 'Ultrathink',
    description: 'Rigor máximo APA 7 + ISO/IEC 25010 + TAM + Estadística',
    suffix: ' [MODO: ULTRATHINK - Máximo rigor doctoral APA 7, ISO/IEC 25010 y TAM]',
  },
];

const QUICK_DIRECTIVES = [
  {
    label: 'Auditar Brechas F1 (UNAJMA)',
    prompt:
      'Ejecuta la auditoría de brechas estructurales entre PROYECTO_TESIS.docx y los modelos oficiales UNAJMA en la Fase F1.',
  },
  {
    label: 'Verificar Consistencia (DEC-007)',
    prompt:
      'Verifica la matriz de consistencia isomórfica con las 3 dimensiones de DEC-007 (Calidad Técnica ISO 25010, Aceptación TAM e Impacto Operativo).',
  },
  {
    label: 'Ejecutar Bioestadística (n=14)',
    prompt:
      'Ejecuta el pipeline bioestadístico reproducible en scripts/estadistica/pipeline.py para n=14 colaboradores (Shapiro-Wilk, t-Student y Wilcoxon).',
  },
  {
    label: 'Documentar Ingeniería XP SIVAC',
    prompt:
      'Audita en modo solo lectura la arquitectura del sistema SIVAC (syncova) y redacta la sección 3.3 con artefactos XP e historias de usuario.',
  },
  {
    label: 'Simular Jurado Revisor (20 pts)',
    prompt:
      'Convoca al jurado-revisor para evaluar el estado actual del informe final bajo la rúbrica vigesimal UNAJMA (20 puntos).',
  },
];

interface AgnoChatAreaProps {
  messages: GodChatMessage[];
  agents: AgentInfo[];
  cliStatuses: CliToolStatus[];
  preferredEngine: 'auto' | 'claude' | 'droid' | 'bun';
  onChangeEngine: (engine: 'auto' | 'claude' | 'droid' | 'bun') => void;
  onSendMessage: (prompt: string, engine: 'auto' | 'claude' | 'droid' | 'bun') => Promise<void>;
  onClearChat: () => Promise<void>;
  onSelectAgent: (agentId: string) => void;
  onOpenVaultFile: (path: string) => void;
  onRunInTerminal: (cmd: string) => Promise<void>;
  isSending: boolean;
}

export const AgnoChatArea: React.FC<AgnoChatAreaProps> = ({
  messages,
  cliStatuses,
  preferredEngine,
  onChangeEngine,
  onSendMessage,
  onClearChat,
  onSelectAgent,
  onOpenVaultFile,
  onRunInTerminal,
  isSending,
}) => {
  const [input, setInput] = useState('');
  const [thinkingMode, setThinkingMode] = useState<ThinkingMode>('auto');
  const [expandedReasonings, setExpandedReasonings] = useState<Record<string, boolean>>({});
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isSending]);

  const toggleReasoning = (msgId: string) => {
    setExpandedReasonings((prev) => ({
      ...prev,
      [msgId]: prev[msgId] === undefined ? false : !prev[msgId],
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || isSending) return;
    const modeObj = THINKING_MODES.find((m) => m.id === thinkingMode);
    const finalPrompt = modeObj?.suffix ? `${trimmed}${modeObj.suffix}` : trimmed;
    setInput('');
    await onSendMessage(finalPrompt, preferredEngine);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const bunCli = cliStatuses.find((c) => c.id === 'bun');
  const claudeCli = cliStatuses.find((c) => c.id === 'claude');
  const droidCli = cliStatuses.find((c) => c.id === 'droid');

  return (
    <div className="h-full flex flex-col bg-[#0b0d12]">
      {/* Top Context Subheader (agno-agi/agent-ui + Opcode style) */}
      <div className="h-11 px-5 border-b border-white/10 flex items-center justify-between gap-4 bg-[#0f1219] shrink-0">
        <div className="flex items-center gap-2.5 text-xs text-zinc-300 min-w-0">
          <Bot className="w-4 h-4 text-orange-400 shrink-0" />
          <span className="font-semibold text-white whitespace-nowrap">
            Agente GOD (director-general)
          </span>
          <span className="text-zinc-600" aria-hidden="true">
            ·
          </span>
          <span className="text-zinc-400 truncate">
            Orquestador Radial Hub-and-Spoke · Loop Cognitivo 3.0 + Delegación Automática
          </span>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <div className="hidden sm:flex items-center gap-2 text-[11px] font-mono text-zinc-400">
            <span>Bun: {bunCli?.installed ? bunCli.version : 'Activo'}</span>
            <span aria-hidden="true">·</span>
            <span>Claude: {claudeCli?.installed ? 'CLI Local' : 'Bridge'}</span>
            <span aria-hidden="true">·</span>
            <span>Droid: {droidCli?.installed ? 'CLI Local' : 'Bridge'}</span>
          </div>

          <button
            type="button"
            onClick={onClearChat}
            className="px-2.5 py-1 rounded-md bg-white/[0.04] hover:bg-white/[0.09] border border-white/10 text-xs text-zinc-300 flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0"
            title="Reiniciar sesión de conversación con el Agente GOD"
          >
            <Trash2 className="w-3.5 h-3.5 text-zinc-400" />
            <span>Limpiar sesión</span>
          </button>
        </div>
      </div>

      {/* Messages Stream (agno-agi/agent-ui MessageArea pattern) */}
      <div className="flex-1 min-h-0 overflow-y-auto px-6 py-6">
        <div className="max-w-4xl mx-auto space-y-6">
          {messages.map((msg) => {
            const isUser = msg.role === 'user';
            const isReasoningOpen =
              expandedReasonings[msg.id] !== undefined ? expandedReasonings[msg.id] : true;

            if (isUser) {
              return (
                <div key={msg.id} className="flex items-start gap-4 justify-end">
                  <div className="max-w-2xl rounded-2xl bg-[#181c28] border border-white/10 px-4 py-3 text-sm text-zinc-100 leading-relaxed">
                    <div className="flex items-center justify-between gap-4 text-[11px] font-mono text-zinc-400 mb-1">
                      <span>Tesista Humano (Autoridad de Fase)</span>
                      <span>
                        {msg.timestamp
                          ? new Date(msg.timestamp).toLocaleTimeString('es-PE', {
                              hour: '2-digit',
                              minute: '2-digit',
                            })
                          : ''}
                      </span>
                    </div>
                    <p className="whitespace-pre-wrap">{msg.content}</p>
                  </div>
                  <div className="w-8 h-8 rounded-lg bg-zinc-800 border border-white/10 flex items-center justify-center shrink-0">
                    <User className="w-4 h-4 text-zinc-300" />
                  </div>
                </div>
              );
            }

            return (
              <div key={msg.id} className="flex items-start gap-4">
                <div className="w-8 h-8 rounded-lg bg-orange-500/15 border border-orange-500/40 flex items-center justify-center shrink-0 mt-0.5">
                  <Cpu className="w-4 h-4 text-orange-400" />
                </div>

                <div className="flex-1 min-w-0 space-y-3">
                  {/* Header Metadata (Zero-Pill clean inline text) */}
                  <div className="flex items-center gap-2 text-xs text-zinc-400 font-mono">
                    <span className="font-semibold text-zinc-100">director-general</span>
                    <span aria-hidden="true">·</span>
                    <span>Hub Central (opus)</span>
                    {msg.engineUsed && (
                      <>
                        <span aria-hidden="true">·</span>
                        <span className="text-orange-400">Motor: {msg.engineUsed}</span>
                      </>
                    )}
                    <span aria-hidden="true">·</span>
                    <span>
                      {msg.timestamp
                        ? new Date(msg.timestamp).toLocaleTimeString('es-PE', {
                            hour: '2-digit',
                            minute: '2-digit',
                          })
                        : ''}
                    </span>
                  </div>

                  {/* Agno-style Reasoning Steps Accordion (Loop de Refinamiento Cognitivo 3.0) */}
                  {msg.cognitiveRefinement && (
                    <div className="rounded-xl bg-[#0f1219] border border-white/10 overflow-hidden">
                      <button
                        type="button"
                        onClick={() => toggleReasoning(msg.id)}
                        className="w-full px-3.5 py-2 flex items-center justify-between text-xs text-zinc-300 hover:bg-white/[0.03] transition-colors"
                      >
                        <div className="flex items-center gap-2 font-mono">
                          <Brain className="w-3.5 h-3.5 text-orange-400" />
                          <span className="font-semibold text-zinc-200">
                            Reasoning · Loop de Refinamiento Cognitivo (Protocolo 3.0)
                          </span>
                          <span className="text-zinc-500">·</span>
                          <span className="text-zinc-400">
                            {msg.cognitiveRefinement.selectedSquads.join(', ')}
                          </span>
                        </div>
                        {isReasoningOpen ? (
                          <ChevronDown className="w-3.5 h-3.5 text-zinc-400" />
                        ) : (
                          <ChevronRight className="w-3.5 h-3.5 text-zinc-400" />
                        )}
                      </button>

                      {isReasoningOpen && (
                        <div className="px-3.5 pb-3 pt-1 border-t border-white/5 space-y-2 text-xs">
                          <div className="flex items-start gap-2.5">
                            <span className="font-mono text-[10px] text-orange-400 bg-orange-500/10 px-1.5 py-0.5 rounded shrink-0 mt-0.5">
                              STEP 1
                            </span>
                            <div className="text-zinc-300">
                              <span className="text-zinc-400 font-medium">Intención Científica: </span>
                              {msg.cognitiveRefinement.intent}
                            </div>
                          </div>
                          <div className="flex items-start gap-2.5">
                            <span className="font-mono text-[10px] text-orange-400 bg-orange-500/10 px-1.5 py-0.5 rounded shrink-0 mt-0.5">
                              STEP 2
                            </span>
                            <div className="text-zinc-300">
                              <span className="text-zinc-400 font-medium">Memoria Viva Obsidian: </span>
                              {msg.cognitiveRefinement.obsidianContext}
                            </div>
                          </div>
                          <div className="flex items-start gap-2.5">
                            <span className="font-mono text-[10px] text-orange-400 bg-orange-500/10 px-1.5 py-0.5 rounded shrink-0 mt-0.5">
                              STEP 3
                            </span>
                            <div className="text-zinc-300">
                              <span className="text-zinc-400 font-medium">Rigor Metodológico: </span>
                              {msg.cognitiveRefinement.formalMethodology}
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Agno-style Tool Calls / Radial Subagent Delegations */}
                  {msg.delegations && msg.delegations.length > 0 && (
                    <div className="space-y-2">
                      <div className="text-[11px] font-mono text-zinc-400 flex items-center gap-1.5">
                        <Zap className="w-3.5 h-3.5 text-orange-400" />
                        <span>
                          Comisiones Radiales Despachadas ({msg.delegations.length} subagentes)
                        </span>
                      </div>
                      <div className="grid grid-cols-1 gap-2.5">
                        {msg.delegations.map((del: SubagentDelegation) => (
                          <div
                            key={del.id}
                            className="p-3 rounded-xl bg-[#10141f] border border-white/10 space-y-2"
                          >
                            <div className="flex items-center justify-between gap-2">
                              <div className="flex items-center gap-2 text-xs min-w-0">
                                {del.status === 'running' || del.status === 'queued' ? (
                                  <Loader2 className="w-3.5 h-3.5 text-amber-400 animate-spin shrink-0" />
                                ) : (
                                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                                )}
                                <button
                                  type="button"
                                  onClick={() => onSelectAgent(del.agentId)}
                                  className="font-mono font-semibold text-zinc-100 hover:text-orange-400 transition-colors truncate"
                                >
                                  {del.agentName}
                                </button>
                                <span className="text-zinc-600">·</span>
                                <span className="text-zinc-400 font-mono text-[11px] truncate">
                                  {del.squad}
                                </span>
                                <span className="text-zinc-600">·</span>
                                <span className="text-orange-300 font-mono text-[11px]">
                                  {del.engine}
                                </span>
                              </div>

                              <div className="flex items-center gap-1.5 shrink-0">
                                {del.handoffFile && (
                                  <button
                                    type="button"
                                    onClick={() => onOpenVaultFile(del.handoffFile!)}
                                    className="px-2 py-1 rounded bg-white/[0.06] hover:bg-white/[0.12] text-[11px] font-mono text-emerald-300 flex items-center gap-1 transition-colors whitespace-nowrap shrink-0"
                                  >
                                    <FileText className="w-3 h-3" />
                                    <span>Ver Handoff</span>
                                    <ArrowUpRight className="w-3 h-3" />
                                  </button>
                                )}
                                <button
                                  type="button"
                                  onClick={() => onRunInTerminal(del.command)}
                                  className="px-2 py-1 rounded bg-white/[0.06] hover:bg-orange-500 hover:text-zinc-950 text-[11px] font-mono text-zinc-300 flex items-center gap-1 transition-colors whitespace-nowrap shrink-0"
                                  title="Re-ejecutar comando en la terminal XTerm.js"
                                >
                                  <TerminalIcon className="w-3 h-3" />
                                  <span>Terminal</span>
                                </button>
                              </div>
                            </div>

                            <div className="text-xs text-zinc-300">{del.task}</div>

                            <div className="px-2.5 py-1.5 rounded bg-black/50 border border-white/5 font-mono text-[11px] text-zinc-400 overflow-x-auto whitespace-nowrap">
                              $ {del.command}
                            </div>

                            {del.outputSummary && (
                              <div className="text-xs text-zinc-300 bg-white/[0.02] p-2.5 rounded-lg border border-white/5 font-mono whitespace-pre-wrap leading-relaxed">
                                {del.outputSummary}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Main Markdown Response (react-markdown + remark-gfm) */}
                  <div className="rounded-2xl bg-[#111520] border border-white/10 px-5 py-4 text-sm text-zinc-200 leading-relaxed space-y-3">
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      components={{
                        h1: ({ children }) => (
                          <h1 className="text-base font-bold text-white mt-2 mb-1">{children}</h1>
                        ),
                        h2: ({ children }) => (
                          <h2 className="text-sm font-bold text-white mt-2 mb-1">{children}</h2>
                        ),
                        h3: ({ children }) => (
                          <h3 className="text-xs font-bold text-orange-300 mt-2 mb-1">
                            {children}
                          </h3>
                        ),
                        p: ({ children }) => (
                          <p className="text-sm text-zinc-200 leading-relaxed mb-2 last:mb-0">
                            {children}
                          </p>
                        ),
                        ul: ({ children }) => (
                          <ul className="list-disc pl-5 space-y-1 text-sm text-zinc-300 my-2">
                            {children}
                          </ul>
                        ),
                        ol: ({ children }) => (
                          <ol className="list-decimal pl-5 space-y-1 text-sm text-zinc-300 my-2">
                            {children}
                          </ol>
                        ),
                        code: ({ children }) => (
                          <code className="px-1.5 py-0.5 rounded bg-black/50 border border-white/10 font-mono text-xs text-orange-300">
                            {children}
                          </code>
                        ),
                        table: ({ children }) => (
                          <div className="overflow-x-auto my-2 border border-white/10 rounded-lg">
                            <table className="w-full text-left border-collapse text-xs">
                              {children}
                            </table>
                          </div>
                        ),
                        th: ({ children }) => (
                          <th className="py-2 px-3 bg-black/40 border-b border-white/10 font-mono text-zinc-300">
                            {children}
                          </th>
                        ),
                        td: ({ children }) => (
                          <td className="py-2 px-3 border-b border-white/5 text-zinc-300">
                            {children}
                          </td>
                        ),
                      }}
                    >
                      {msg.content}
                    </ReactMarkdown>
                  </div>
                </div>
              </div>
            );
          })}

          {isSending && (
            <div className="flex items-center gap-3 text-xs font-mono text-orange-400 pl-12">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>
                Agente GOD ejecutando Loop de Refinamiento Cognitivo 3.0 y delegando en subagentes...
              </span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Opcode-style Floating Prompt Input Bar */}
      <div className="px-6 pb-4 pt-2 bg-[#0b0d12] border-t border-white/10 shrink-0">
        <div className="max-w-4xl mx-auto space-y-2.5">
          {/* Quick Directives Strip */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
            <span className="text-[11px] font-mono text-zinc-500 whitespace-nowrap shrink-0 mr-1">
              Directivas:
            </span>
            {QUICK_DIRECTIVES.map((dir) => (
              <button
                key={dir.label}
                type="button"
                onClick={() => onSendMessage(dir.prompt, preferredEngine)}
                disabled={isSending}
                className="px-2.5 py-1 rounded-lg bg-[#121622] hover:bg-orange-500/15 border border-white/10 hover:border-orange-500/40 text-xs text-zinc-300 hover:text-orange-200 flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0"
              >
                <Play className="w-2.5 h-2.5 text-orange-400 fill-current" />
                <span>{dir.label}</span>
              </button>
            ))}
          </div>

          {/* Prompt Box */}
          <form
            onSubmit={handleSubmit}
            className="rounded-xl bg-[#111520] border border-white/15 focus-within:border-orange-500/70 transition-colors overflow-hidden shadow-lg"
          >
            <textarea
              rows={2}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Escribe una orden para el Agente GOD (ej. 'Avanza el capítulo de resultados bioestadísticos n=14 y valida DEC-007')..."
              className="w-full px-4 pt-3 pb-2 bg-transparent text-sm text-zinc-100 placeholder:text-zinc-500 focus:outline-none resize-none"
            />

            {/* Bottom Controls inside Prompt Box (winfunc/opcode FloatingPromptInput style) */}
            <div className="px-3 py-2 bg-[#0d1018] border-t border-white/10 flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center gap-2 flex-wrap">
                {/* Thinking Mode Selector */}
                <div className="flex items-center gap-1 bg-black/40 p-0.5 rounded-lg border border-white/10">
                  {THINKING_MODES.map((m) => (
                    <button
                      key={m.id}
                      type="button"
                      onClick={() => setThinkingMode(m.id)}
                      title={m.description}
                      className={`px-2 py-1 rounded-md text-[11px] font-mono flex items-center gap-1 transition-colors whitespace-nowrap shrink-0 ${
                        thinkingMode === m.id
                          ? 'bg-orange-500/20 text-orange-300 font-semibold'
                          : 'text-zinc-400 hover:text-zinc-200'
                      }`}
                    >
                      <Sparkles className="w-3 h-3" />
                      <span>{m.label}</span>
                    </button>
                  ))}
                </div>

                {/* CLI Engine Selector */}
                <div className="flex items-center gap-1 bg-black/40 p-0.5 rounded-lg border border-white/10">
                  {(
                    [
                      { id: 'auto', label: 'Motor: Auto' },
                      { id: 'claude', label: 'Claude Code' },
                      { id: 'droid', label: 'Factory Droid' },
                      { id: 'bun', label: 'Bun Shell' },
                    ] as const
                  ).map((eng) => (
                    <button
                      key={eng.id}
                      type="button"
                      onClick={() => onChangeEngine(eng.id)}
                      className={`px-2 py-1 rounded-md text-[11px] font-mono transition-colors whitespace-nowrap shrink-0 ${
                        preferredEngine === eng.id
                          ? 'bg-white/15 text-white font-semibold'
                          : 'text-zinc-400 hover:text-zinc-200'
                      }`}
                    >
                      {eng.label}
                    </button>
                  ))}
                </div>
              </div>

              <button
                type="submit"
                disabled={!input.trim() || isSending}
                className="px-4 py-1.5 rounded-lg bg-orange-500 hover:bg-orange-400 disabled:opacity-40 text-xs font-semibold text-zinc-950 flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Enviar Orden al Agente GOD</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};
