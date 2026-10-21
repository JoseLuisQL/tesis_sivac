import React, { useState } from 'react';
import {
  Server,
  Wrench,
  ShieldCheck,
  Search,
  FileCode2,
  Play,
  CheckCircle2,
  XCircle,
} from 'lucide-react';
import type {
  McpServerInfo,
  SkillInfo,
  HookInfo,
} from '../../types/studio';

interface OpcodeCapabilitiesProps {
  mcps: McpServerInfo[];
  skills: SkillInfo[];
  hooks: HookInfo[];
  onToggleMcp: (id: string, enabled: boolean) => Promise<void>;
  onToggleSkill: (id: string, enabled: boolean) => Promise<void>;
  onToggleHook: (id: string, enabled: boolean) => Promise<void>;
  onOpenFile: (path: string) => void;
  onRunInTerminal: (cmd: string) => Promise<void>;
}

export const OpcodeCapabilities: React.FC<OpcodeCapabilitiesProps> = ({
  mcps,
  skills,
  hooks,
  onToggleMcp,
  onToggleSkill,
  onToggleHook,
  onOpenFile,
  onRunInTerminal,
}) => {
  const [activeTab, setActiveTab] = useState<'mcps' | 'skills' | 'hooks'>('mcps');
  const [search, setSearch] = useState('');

  const filteredSkills = skills.filter(
    (s) =>
      !search.trim() ||
      s.name.toLowerCase().includes(search.toLowerCase()) ||
      s.description.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="h-full flex flex-col bg-[#0b0d12]">
      {/* Top Sub-bar (winfunc/opcode MCPManager & HooksEditor header) */}
      <div className="h-11 px-5 border-b border-white/10 flex items-center justify-between gap-4 bg-[#0f1219] shrink-0">
        <div className="flex items-center gap-1 bg-black/40 p-1 rounded-lg border border-white/10">
          <button
            type="button"
            onClick={() => setActiveTab('mcps')}
            className={`px-3 py-1 rounded-md text-xs font-medium flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0 ${
              activeTab === 'mcps'
                ? 'bg-orange-500 text-zinc-950 font-semibold'
                : 'text-zinc-400 hover:text-zinc-100'
            }`}
          >
            <Server className="w-3.5 h-3.5" />
            <span>Servidores MCP ({mcps.length})</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('skills')}
            className={`px-3 py-1 rounded-md text-xs font-medium flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0 ${
              activeTab === 'skills'
                ? 'bg-orange-500 text-zinc-950 font-semibold'
                : 'text-zinc-400 hover:text-zinc-100'
            }`}
          >
            <Wrench className="w-3.5 h-3.5" />
            <span>Skills Científicas ({skills.length})</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('hooks')}
            className={`px-3 py-1 rounded-md text-xs font-medium flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0 ${
              activeTab === 'hooks'
                ? 'bg-orange-500 text-zinc-950 font-semibold'
                : 'text-zinc-400 hover:text-zinc-100'
            }`}
          >
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Hooks y Seguridad ({hooks.length})</span>
          </button>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => onOpenFile('.mcp.json')}
            className="px-2.5 py-1 rounded bg-white/[0.05] hover:bg-white/[0.1] border border-white/10 text-xs font-mono text-zinc-300 flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0"
          >
            <FileCode2 className="w-3.5 h-3.5 text-orange-400" />
            <span>.mcp.json</span>
          </button>
          <button
            type="button"
            onClick={() => onOpenFile('.claude/settings.json')}
            className="px-2.5 py-1 rounded bg-white/[0.05] hover:bg-white/[0.1] border border-white/10 text-xs font-mono text-zinc-300 flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0"
          >
            <FileCode2 className="w-3.5 h-3.5 text-orange-400" />
            <span>.claude/settings.json</span>
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 min-h-0 overflow-y-auto p-6">
        <div className="max-w-5xl mx-auto space-y-6">
          {activeTab === 'mcps' && (
            <div className="space-y-4">
              <div>
                <h2 className="text-base font-semibold text-zinc-100">
                  01. Servidores Model Context Protocol (.mcp.json y .factory/config.json)
                </h2>
                <p className="text-xs text-zinc-400 mt-0.5">
                  Activa o desactiva servidores MCP en tiempo real para Claude Code y Factory Droid.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {mcps.map((mcp) => (
                  <div
                    key={mcp.id}
                    className="p-4 rounded-xl bg-[#0f1219] border border-white/10 flex flex-col justify-between gap-3"
                  >
                    <div className="space-y-2">
                      <div className="flex items-center justify-between gap-2">
                        <div className="flex items-center gap-2">
                          <Server className="w-4 h-4 text-orange-400" />
                          <span className="text-sm font-semibold text-zinc-100 font-mono">
                            {mcp.name}
                          </span>
                        </div>

                        <button
                          type="button"
                          onClick={() => onToggleMcp(mcp.id, !mcp.enabled)}
                          className={`px-3 py-1 rounded-md text-xs font-mono font-semibold flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0 ${
                            mcp.enabled
                              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                              : 'bg-zinc-800 text-zinc-400 border border-white/10'
                          }`}
                        >
                          {mcp.enabled ? (
                            <>
                              <CheckCircle2 className="w-3.5 h-3.5" />
                              <span>Activo</span>
                            </>
                          ) : (
                            <>
                              <XCircle className="w-3.5 h-3.5" />
                              <span>Inactivo</span>
                            </>
                          )}
                        </button>
                      </div>

                      <div className="px-3 py-2 rounded-lg bg-black/40 border border-white/5 font-mono text-xs text-zinc-300 overflow-x-auto whitespace-nowrap">
                        $ {mcp.command} {(mcp.args || []).join(' ')}
                      </div>
                    </div>

                    <div className="flex items-center justify-between text-[11px] font-mono text-zinc-400 pt-2 border-t border-white/5">
                      <span>Transporte: {mcp.type || 'stdio'}</span>
                      <button
                        type="button"
                        onClick={() =>
                          onRunInTerminal(`echo "Verificando MCP ${mcp.name}: ${mcp.command}"`)
                        }
                        className="text-orange-400 hover:text-orange-300 flex items-center gap-1"
                      >
                        <Play className="w-3 h-3 fill-current" />
                        <span>Probar en Terminal</span>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'skills' && (
            <div className="space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                  <h2 className="text-base font-semibold text-zinc-100">
                    02. Catálogo de 17 Skills Especializadas (.claude/skills/)
                  </h2>
                  <p className="text-xs text-zinc-400 mt-0.5">
                    Capacidades modulares asignadas a los 14 agentes del ecosistema SIVAC-THESIS-LAB.
                  </p>
                </div>

                <div className="relative w-72">
                  <Search className="w-3.5 h-3.5 text-zinc-500 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    placeholder="Buscar skill (ej. apa7, docx, estadistica)..."
                    className="w-full h-8 pl-8 pr-3 rounded-lg bg-[#141824] border border-white/10 text-xs text-zinc-100 placeholder:text-zinc-500 focus:outline-none focus:border-orange-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                {filteredSkills.map((skill) => {
                  const isEnabled = skill.enabled !== false;
                  return (
                    <div
                      key={skill.id}
                      className="p-4 rounded-xl bg-[#0f1219] border border-white/10 flex flex-col justify-between gap-3"
                    >
                      <div>
                        <div className="flex items-center justify-between gap-2 mb-1.5">
                          <span className="text-sm font-semibold text-zinc-100 font-mono truncate">
                            {skill.name}
                          </span>
                          <button
                            type="button"
                            onClick={() => onToggleSkill(skill.id, !isEnabled)}
                            className={`px-2.5 py-0.5 rounded text-[11px] font-mono font-semibold transition-colors whitespace-nowrap shrink-0 ${
                              isEnabled
                                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                                : 'bg-zinc-800 text-zinc-400 border border-white/10'
                            }`}
                          >
                            {isEnabled ? 'Habilitada' : 'Deshabilitada'}
                          </button>
                        </div>
                        <p className="text-xs text-zinc-400 line-clamp-2 leading-relaxed">
                          {skill.description}
                        </p>
                      </div>

                      <div className="flex items-center justify-between pt-2 border-t border-white/5 text-[11px] font-mono text-zinc-500">
                        <span className="truncate">{skill.path}</span>
                        <button
                          type="button"
                          onClick={() => onOpenFile(skill.path)}
                          className="text-orange-400 hover:text-orange-300 flex items-center gap-1 shrink-0"
                        >
                          <FileCode2 className="w-3 h-3" />
                          <span>Inspeccionar SKILL.md</span>
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {activeTab === 'hooks' && (
            <div className="space-y-4">
              <div>
                <h2 className="text-base font-semibold text-zinc-100">
                  03. Hooks Canónicos de Gobernanza (.claude/settings.json)
                </h2>
                <p className="text-xs text-zinc-400 mt-0.5">
                  Salvaguardas automáticas de solo-lectura en syncova, validación de citas y sincronización con Obsidian.
                </p>
              </div>

              <div className="space-y-3">
                {hooks.map((hook) => (
                  <div
                    key={hook.id}
                    className="p-4 rounded-xl bg-[#0f1219] border border-white/10 flex items-center justify-between gap-4"
                  >
                    <div className="space-y-1 min-w-0 flex-1">
                      <div className="flex items-center gap-2 text-xs font-mono">
                        <span className="font-semibold text-orange-400">{hook.event}</span>
                        <span className="text-zinc-600">·</span>
                        <span className="text-zinc-300">Matcher: {hook.matcher}</span>
                      </div>
                      <div className="px-3 py-1.5 rounded bg-black/40 border border-white/5 font-mono text-xs text-zinc-300 truncate">
                        {hook.command}
                      </div>
                    </div>

                    <button
                      type="button"
                      onClick={() => onToggleHook(hook.id, !hook.enabled)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-colors whitespace-nowrap shrink-0 ${
                        hook.enabled
                          ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                          : 'bg-zinc-800 text-zinc-400 border border-white/10'
                      }`}
                    >
                      {hook.enabled ? 'Hook Activo' : 'Desactivado'}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
