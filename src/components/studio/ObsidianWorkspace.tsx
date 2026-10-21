import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  FolderKanban,
  FileText,
  Plus,
  CheckCircle2,
  Clock,
  Sparkles,
  Save,
  Eye,
  Edit3,
  Play,
} from 'lucide-react';
import type {
  ResearchProject,
  AgentInfo,
} from '../../types/studio';

interface ObsidianWorkspaceProps {
  projects: ResearchProject[];
  activeProjectId: string;
  onSelectProject: (id: string) => void;
  onCreateProject: (payload: {
    code: string;
    title: string;
    university: string;
    methodology: string;
    sampleSize: string;
  }) => Promise<void>;
  onAddTask: (
    projectId: string,
    payload: { title: string; phase: string; assignedAgent: string }
  ) => Promise<void>;
  onToggleTaskStatus: (
    projectId: string,
    taskId: string,
    nextStatus: 'completado' | 'en_progreso' | 'pendiente'
  ) => Promise<void>;
  vaultFiles: string[];
  selectedVaultPath: string;
  vaultFileContent: string;
  onSelectVaultFile: (path: string) => Promise<void>;
  onSaveVaultFile: (path: string, content: string) => Promise<void>;
  agents: AgentInfo[];
  onCommissionTaskToGod: (prompt: string) => Promise<void>;
}

export const ObsidianWorkspace: React.FC<ObsidianWorkspaceProps> = ({
  projects,
  activeProjectId,
  onSelectProject,
  onCreateProject,
  onAddTask,
  onToggleTaskStatus,
  vaultFiles,
  selectedVaultPath,
  vaultFileContent,
  onSelectVaultFile,
  onSaveVaultFile,
  agents,
  onCommissionTaskToGod,
}) => {
  const [subView, setSubView] = useState<'projects' | 'vault'>('projects');
  const [showNewProjectModal, setShowNewProjectModal] = useState(false);
  const [newProjCode, setNewProjCode] = useState('');
  const [newProjTitle, setNewProjTitle] = useState('');
  const [newProjUni, setNewProjUni] = useState('UNAJMA — Ingeniería de Sistemas');
  const [newProjMethod, setNewProjMethod] = useState('Cuasi-experimental / Pre-experimental');
  const [newProjSample, setNewProjSample] = useState('n=14');

  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskPhase, setNewTaskPhase] = useState('F2');
  const [newTaskAgent, setNewTaskAgent] = useState('guardian-consistencia');

  const [isEditingVault, setIsEditingVault] = useState(false);
  const [draftContent, setDraftContent] = useState(vaultFileContent);
  const [isSavingVault, setIsSavingVault] = useState(false);

  React.useEffect(() => {
    setDraftContent(vaultFileContent);
  }, [vaultFileContent, selectedVaultPath]);

  const activeProject =
    projects.find((p) => p.id === activeProjectId) || projects[0] || null;

  const handleCreateProjectSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newProjCode.trim() || !newProjTitle.trim()) return;
    await onCreateProject({
      code: newProjCode.trim(),
      title: newProjTitle.trim(),
      university: newProjUni.trim(),
      methodology: newProjMethod.trim(),
      sampleSize: newProjSample.trim(),
    });
    setNewProjCode('');
    setNewProjTitle('');
    setShowNewProjectModal(false);
  };

  const handleAddTaskSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeProject || !newTaskTitle.trim()) return;
    await onAddTask(activeProject.id, {
      title: newTaskTitle.trim(),
      phase: newTaskPhase,
      assignedAgent: newTaskAgent,
    });
    setNewTaskTitle('');
  };

  const handleSaveVault = async () => {
    if (!selectedVaultPath) return;
    setIsSavingVault(true);
    try {
      await onSaveVaultFile(selectedVaultPath, draftContent);
      setIsEditingVault(false);
    } finally {
      setIsSavingVault(false);
    }
  };

  return (
    <div className="h-full flex flex-col bg-[#0b0d12]">
      {/* Top Sub-bar */}
      <div className="h-11 px-5 border-b border-white/10 flex items-center justify-between gap-4 bg-[#0f1219] shrink-0">
        <div className="flex items-center gap-1 bg-black/40 p-1 rounded-lg border border-white/10">
          <button
            type="button"
            onClick={() => setSubView('projects')}
            className={`px-3 py-1 rounded-md text-xs font-medium flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0 ${
              subView === 'projects'
                ? 'bg-orange-500 text-zinc-950 font-semibold'
                : 'text-zinc-400 hover:text-zinc-100'
            }`}
          >
            <FolderKanban className="w-3.5 h-3.5" />
            <span>Proyectos e Hitos de Investigación ({projects.length})</span>
          </button>
          <button
            type="button"
            onClick={() => setSubView('vault')}
            className={`px-3 py-1 rounded-md text-xs font-medium flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0 ${
              subView === 'vault'
                ? 'bg-orange-500 text-zinc-950 font-semibold'
                : 'text-zinc-400 hover:text-zinc-100'
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Memoria Viva Obsidian Vault ({vaultFiles.length} notas)</span>
          </button>
        </div>

        {subView === 'projects' && (
          <button
            type="button"
            onClick={() => setShowNewProjectModal(true)}
            className="px-3 py-1.5 rounded-lg bg-orange-500 hover:bg-orange-400 text-xs font-semibold text-zinc-950 flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Nuevo Proyecto de Investigación</span>
          </button>
        )}
      </div>

      {/* Main Content */}
      {subView === 'projects' ? (
        <div className="flex-1 min-h-0 overflow-y-auto p-6">
          <div className="max-w-5xl mx-auto space-y-6">
            {/* Project Cards Strip */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {projects.map((proj) => {
                const isSelected = activeProject?.id === proj.id;
                return (
                  <div
                    key={proj.id}
                    onClick={() => onSelectProject(proj.id)}
                    className={`p-4 rounded-xl border transition-all cursor-pointer ${
                      isSelected
                        ? 'bg-[#131826] border-orange-500/60'
                        : 'bg-[#0f1219] border-white/10 hover:border-white/25'
                    }`}
                  >
                    <div className="flex items-center justify-between text-xs font-mono text-zinc-400 mb-1.5">
                      <span className="text-orange-400 font-semibold">{proj.code}</span>
                      <span>
                        {proj.university} · {proj.sampleSize}
                      </span>
                    </div>
                    <h3 className="text-sm font-semibold text-zinc-100 leading-snug mb-2">
                      {proj.title}
                    </h3>
                    <div className="text-xs text-zinc-400 mb-3">{proj.methodology}</div>

                    <div className="space-y-1.5">
                      <div className="flex items-center justify-between text-[11px] font-mono text-zinc-300">
                        <span>Avance Global</span>
                        <span className="tabular-nums font-semibold text-orange-400">
                          {proj.progress}%
                        </span>
                      </div>
                      <div className="w-full h-1.5 rounded-full bg-black/50 overflow-hidden">
                        <div
                          className="h-full bg-orange-500 transition-all"
                          style={{ width: `${proj.progress}%` }}
                        />
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Active Project Tasks Table + New Task Form */}
            {activeProject && (
              <div className="space-y-4">
                <div className="flex flex-wrap items-center justify-between gap-4">
                  <div>
                    <h2 className="text-base font-semibold text-zinc-100">
                      01. Plan de Tareas y Comisiones — {activeProject.code}
                    </h2>
                    <p className="text-xs text-zinc-400 mt-0.5">
                      Haz clic en el estado de cualquier tarea para actualizar su progreso o despáchala al Agente GOD.
                    </p>
                  </div>
                </div>

                {/* Add Task Bar */}
                <form
                  onSubmit={handleAddTaskSubmit}
                  className="p-3 rounded-xl bg-[#0f1219] border border-white/10 flex flex-wrap items-center gap-2.5"
                >
                  <input
                    type="text"
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                    placeholder="Nueva tarea científica o técnica (ej. Validar normalidad Shapiro-Wilk de dimensión TAM)..."
                    className="flex-1 min-w-[240px] h-9 px-3 rounded-lg bg-[#141824] border border-white/10 text-xs text-zinc-100 placeholder:text-zinc-500 focus:outline-none focus:border-orange-500"
                  />
                  <select
                    value={newTaskPhase}
                    onChange={(e) => setNewTaskPhase(e.target.value)}
                    className="h-9 px-2.5 rounded-lg bg-[#141824] border border-white/10 text-xs font-mono text-zinc-200"
                  >
                    {['F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10'].map(
                      (f) => (
                        <option key={f} value={f}>
                          Fase {f}
                        </option>
                      )
                    )}
                  </select>
                  <select
                    value={newTaskAgent}
                    onChange={(e) => setNewTaskAgent(e.target.value)}
                    className="h-9 px-2.5 rounded-lg bg-[#141824] border border-white/10 text-xs font-mono text-zinc-200"
                  >
                    {agents.map((a) => (
                      <option key={a.id} value={a.id}>
                        {a.name} ({a.squad.split(' ')[0]} {a.squad.split(' ')[1] || ''})
                      </option>
                    ))}
                  </select>
                  <button
                    type="submit"
                    className="h-9 px-3.5 rounded-lg bg-orange-500 hover:bg-orange-400 text-xs font-semibold text-zinc-950 flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0"
                  >
                    <Plus className="w-3.5 h-3.5" />
                    <span>Agregar Tarea</span>
                  </button>
                </form>

                {/* Tasks Table */}
                <div className="border border-white/10 rounded-xl overflow-hidden bg-[#0f1219]">
                  <table className="w-full text-left border-collapse">
                    <thead>
                      <tr className="border-b border-white/10 text-[11px] font-mono text-zinc-400 bg-black/20">
                        <th className="py-2.5 px-4">Fase</th>
                        <th className="py-2.5 px-4">Tarea / Entregable</th>
                        <th className="py-2.5 px-4">Subagente Asignado</th>
                        <th className="py-2.5 px-4">Estado</th>
                        <th className="py-2.5 px-4 text-right">Acción Directa</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5 text-xs">
                      {activeProject.tasks.map((task) => {
                        const nextStatus =
                          task.status === 'pendiente'
                            ? 'en_progreso'
                            : task.status === 'en_progreso'
                            ? 'completado'
                            : 'pendiente';
                        return (
                          <tr key={task.id} className="hover:bg-white/[0.02]">
                            <td className="py-2.5 px-4 font-mono font-semibold text-orange-400">
                              {task.phase}
                            </td>
                            <td className="py-2.5 px-4 font-medium text-zinc-200">{task.title}</td>
                            <td className="py-2.5 px-4 font-mono text-zinc-400">
                              {task.assignedAgent}
                            </td>
                            <td className="py-2.5 px-4">
                              <button
                                type="button"
                                onClick={() =>
                                  onToggleTaskStatus(activeProject.id, task.id, nextStatus)
                                }
                                className="inline-flex items-center gap-1.5 font-mono text-xs hover:underline"
                              >
                                {task.status === 'completado' ? (
                                  <span className="text-emerald-400 flex items-center gap-1">
                                    <CheckCircle2 className="w-3.5 h-3.5" />
                                    <span>Completado</span>
                                  </span>
                                ) : task.status === 'en_progreso' ? (
                                  <span className="text-amber-400 flex items-center gap-1">
                                    <Sparkles className="w-3.5 h-3.5" />
                                    <span>En curso</span>
                                  </span>
                                ) : (
                                  <span className="text-zinc-400 flex items-center gap-1">
                                    <Clock className="w-3.5 h-3.5" />
                                    <span>Pendiente</span>
                                  </span>
                                )}
                              </button>
                            </td>
                            <td className="py-2.5 px-4 text-right">
                              <button
                                type="button"
                                onClick={() =>
                                  onCommissionTaskToGod(
                                    `Comisiona al subagente ${task.assignedAgent} (${task.phase}) para ejecutar la tarea del proyecto ${activeProject.code}: "${task.title}"`
                                  )
                                }
                                className="px-2.5 py-1 rounded bg-white/[0.06] hover:bg-orange-500 hover:text-zinc-950 text-[11px] font-mono text-zinc-200 inline-flex items-center gap-1 transition-colors whitespace-nowrap shrink-0"
                              >
                                <Play className="w-2.5 h-2.5 fill-current" />
                                <span>Delegar con GOD</span>
                              </button>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        </div>
      ) : (
        /* Obsidian Vault Split Reader & Editor */
        <div className="flex-1 min-h-0 grid grid-cols-12 overflow-hidden">
          <div className="col-span-4 border-r border-white/10 bg-[#0d1017] overflow-y-auto p-3 space-y-1">
            <div className="px-2 py-1.5 text-[11px] font-mono text-zinc-400">
              ARCHIVOS EN OBSIDIAN_VAULT ({vaultFiles.length})
            </div>
            {vaultFiles.map((file) => {
              const isSelected = selectedVaultPath === file;
              return (
                <button
                  key={file}
                  type="button"
                  onClick={() => onSelectVaultFile(file)}
                  className={`w-full px-2.5 py-2 rounded-lg text-left text-xs font-mono flex items-center gap-2 transition-colors ${
                    isSelected
                      ? 'bg-orange-500/15 text-orange-300 border border-orange-500/40'
                      : 'text-zinc-400 hover:bg-white/5 hover:text-zinc-200'
                  }`}
                >
                  <FileText className="w-3.5 h-3.5 shrink-0" />
                  <span className="truncate">{file}</span>
                </button>
              );
            })}
          </div>

          <div className="col-span-8 flex flex-col min-h-0 bg-[#0b0d12]">
            <div className="h-10 px-4 border-b border-white/10 flex items-center justify-between bg-[#0f1219] shrink-0">
              <span className="text-xs font-mono text-zinc-300 truncate">
                obsidian_vault/{selectedVaultPath}
              </span>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setIsEditingVault(!isEditingVault)}
                  className="px-2.5 py-1 rounded bg-white/[0.06] hover:bg-white/[0.12] text-xs text-zinc-200 flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0"
                >
                  {isEditingVault ? (
                    <>
                      <Eye className="w-3.5 h-3.5 text-orange-400" />
                      <span>Vista Previa</span>
                    </>
                  ) : (
                    <>
                      <Edit3 className="w-3.5 h-3.5 text-orange-400" />
                      <span>Editar Nota</span>
                    </>
                  )}
                </button>
                {isEditingVault && (
                  <button
                    type="button"
                    disabled={isSavingVault}
                    onClick={handleSaveVault}
                    className="px-3 py-1 rounded bg-orange-500 hover:bg-orange-400 text-xs font-semibold text-zinc-950 flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0"
                  >
                    <Save className="w-3.5 h-3.5" />
                    <span>Guardar en Vault</span>
                  </button>
                )}
              </div>
            </div>

            <div className="flex-1 min-h-0 overflow-y-auto p-6">
              {isEditingVault ? (
                <textarea
                  value={draftContent}
                  onChange={(e) => setDraftContent(e.target.value)}
                  className="w-full h-full min-h-[420px] p-4 rounded-xl bg-[#0f1219] border border-white/10 font-mono text-xs text-zinc-100 focus:outline-none focus:border-orange-500 resize-none leading-relaxed"
                />
              ) : (
                <div className="max-w-3xl mx-auto prose prose-invert text-sm text-zinc-200 space-y-3 leading-relaxed">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{vaultFileContent}</ReactMarkdown>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* New Project Modal */}
      {showNewProjectModal && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
          <form
            onSubmit={handleCreateProjectSubmit}
            className="w-full max-w-lg rounded-2xl bg-[#111520] border border-white/15 p-6 space-y-4 shadow-2xl"
          >
            <h3 className="text-base font-bold text-white">
              Registrar Nuevo Proyecto de Investigación en Obsidian
            </h3>
            <div className="space-y-3 text-xs">
              <div>
                <label className="block text-zinc-400 mb-1">Código del Proyecto</label>
                <input
                  type="text"
                  required
                  value={newProjCode}
                  onChange={(e) => setNewProjCode(e.target.value)}
                  placeholder="Ej. TESIS-IA-2026"
                  className="w-full h-9 px-3 rounded-lg bg-[#0b0d12] border border-white/10 text-zinc-100"
                />
              </div>
              <div>
                <label className="block text-zinc-400 mb-1">Título Completo de la Investigación</label>
                <input
                  type="text"
                  required
                  value={newProjTitle}
                  onChange={(e) => setNewProjTitle(e.target.value)}
                  placeholder="Ej. Sistema multi-agente para automatización de diagnóstico..."
                  className="w-full h-9 px-3 rounded-lg bg-[#0b0d12] border border-white/10 text-zinc-100"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-zinc-400 mb-1">Universidad / Escuela</label>
                  <input
                    type="text"
                    value={newProjUni}
                    onChange={(e) => setNewProjUni(e.target.value)}
                    className="w-full h-9 px-3 rounded-lg bg-[#0b0d12] border border-white/10 text-zinc-100"
                  />
                </div>
                <div>
                  <label className="block text-zinc-400 mb-1">Muestra (n)</label>
                  <input
                    type="text"
                    value={newProjSample}
                    onChange={(e) => setNewProjSample(e.target.value)}
                    className="w-full h-9 px-3 rounded-lg bg-[#0b0d12] border border-white/10 text-zinc-100"
                  />
                </div>
              </div>
              <div>
                <label className="block text-zinc-400 mb-1">Diseño y Marco Metodológico</label>
                <input
                  type="text"
                  value={newProjMethod}
                  onChange={(e) => setNewProjMethod(e.target.value)}
                  className="w-full h-9 px-3 rounded-lg bg-[#0b0d12] border border-white/10 text-zinc-100"
                />
              </div>
            </div>
            <div className="flex items-center justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={() => setShowNewProjectModal(false)}
                className="px-3.5 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-xs text-zinc-300"
              >
                Cancelar
              </button>
              <button
                type="submit"
                className="px-4 py-1.5 rounded-lg bg-orange-500 hover:bg-orange-400 text-xs font-semibold text-zinc-950"
              >
                Crear Proyecto
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};
