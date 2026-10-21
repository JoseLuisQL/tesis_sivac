# SIVAC-THESIS-LAB — Minimalist Agent Farm OS, Chat con Agente GOD, Motor Bun & Detector de CLIs

Evolución del centro de mando multi-agente hacia una interfaz **minimalista, ordenada y autoexplicativa**, presidida por un **Panel de Chat conversacional con el Agente GOD (`director-general`)** que delega automáticamente en los 13 subagentes especialistas, ejecuta procesos ultrarrápidos mediante **Bun Runtime (`bun`)**, enlaza directamente con tus instalaciones de **Claude Code CLI (`claude`)** y **Factory Droid CLI (`droid`)**, e incorpora un **Visor de Detección de Sistemas en Vivo** para verificar si los agentes están instalados y listos.

## User Review & Critical Decisions

> [!IMPORTANT]
> Se han consolidado las cuatro decisiones confirmadas e integradas con la investigación profunda sobre los protocolos de ejecución de **Bun**, **Claude Code CLI** y **Factory Droid CLI**:

- **Decisión Confirmada 1 — Panel de Chat Directo con el Agente GOD (`director-general`) + Delegación Automática**: El usuario conversa en lenguaje natural con el Agente GOD como en un chat moderno. El Agente GOD aplica internamente el *Loop de Refinamiento Cognitivo 3.0*, selecciona automáticamente al subagente especialista idóneo de los Squads A–F, muestra una tarjeta limpia de delegación en vivo dentro del mismo hilo de chat, ejecuta la tarea y devuelve el resultado junto con el informe `handoff` depositado en Obsidian.
- **Decisión Confirmada 2 — Motor de Ejecución con Bun (`bun`) + Puente Nativo a `claude` y `droid`**: El backend incorpora soporte nativo para **Bun** (`bun --version`, `bun run`, `bunx` y ejecución de shells vía Bun cuando está disponible, con aprovisionamiento de Bun en un clic) y conecta con los protocolos reales de línea de comandos:
  - **Claude Code CLI**: `claude -p "<comisión>" --agent <subagente> --output-format stream-json --verbose`
  - **Factory Droid CLI**: `droid exec "<comisión>" --auto medium` (leyendo `.factory/droids/<subagente>.md` y `AGENTS.md`)
  - **Ejecutor Científico SIVAC**: Ejecución mediante Bun/Python3 de los 26 scripts verificados del repositorio cuando se trabaja en entorno contenerizado o sin clave externa.
- **Decisión Confirmada 3 — Visor de Detección en Vivo (`Bun`, `Claude Code`, `Factory Droid`, `Python 3`, `Git`) + Instalador 1-Clic**: Un panel y barra de diagnóstico en tiempo real que escanea el `PATH` del sistema, muestra claramente si cada motor está **Instalado / No Instalado**, su versión exacta, ruta del binario (`which`), estado de configuración (`.claude/agents/`, `.factory/droids/`, `.mcp.json`) y botones de **Instalar / Reparar en 1 Clic** desde la propia terminal integrada.
- **Decisión Confirmada 4 — Rediseño Minimalista Paso a Paso para Cualquier Usuario**: Se eliminan las pantallas saturadas de paneles simultáneos. La interfaz se organiza en **5 vistas limpias y respirables**, encabezadas por el **Chat con el Director General (Agente GOD)** con sugerencias guiadas en lenguaje cotidiano, de modo que cualquier investigador o revisor pueda operar el sistema sin conocimientos técnicos previos.

---

## 1. Overview & Core Concept

- **Qué Hace**: Permite que cualquier persona dirija un laboratorio de investigación de 14 agentes simplemente conversando en un chat limpio con el **Director General (`director-general`)**. Cuando el usuario pide una tarea (por ejemplo, *"Revisa las citas del capítulo 2"*, *"Genera el formato de validación de expertos"* o *"Actualiza el avance de mi proyecto"*), el Agente GOD razona, delega automáticamente en el subagente correspondiente, ejecuta la acción usando **Bun**, **Claude Code** o **Factory Droid** en la terminal integrada y presenta el resultado de forma clara y ordenada.
- **Investigación Técnica Aplicada (`Bun` + `Claude Code` + `Factory Droid`)**:
  - **Bun Runtime (`bun`)**: Proporciona arranque instantáneo de procesos (~4x más rápido que Node tradicional), ejecución de scripts TypeScript/JavaScript sin transpilación previa (`bun run`) y gestión de paquetes MCP con `bunx`.
  - **Claude Code Headless & Subagents**: Utiliza las banderas oficiales `-p` (modo programático), `--agent <nombre>` (invocación directa de subagentes en `.claude/agents/*.md`) y `--output-format stream-json` para transmitir eventos estructurados en tiempo real hacia la UI.
  - **Factory Droid CLI (`droid`)**: Utiliza `droid exec "<prompt>" --auto medium` y sincroniza automáticamente `.factory/droids/*.md`, `.factory/hooks.json` y `AGENTS.md`.
- **Valor Principal**: Combina la potencia de una granja multi-agente real en terminal con la simplicidad visual de un asistente conversacional minimalista y un diagnóstico transparente del entorno local.

---

## 2. User Experience & Visual Design

### Flujos de Usuario Principales (Simples y Guiados)
1. **Vista 1 (Principal): Chat con el Agente GOD & Orquestación Automática**:
   - Al entrar, el usuario ve una interfaz limpia dividida en dos zonas claras:
     - **Columna Principal (Chat con el Agente GOD)**: Un área conversacional clara con botones de inicio rápido en lenguaje sencillo (*"Verificar citas APA 7"*, *"Generar certificado de validación Fany 2024"*, *"Auditar formato Word UNAJMA"*, *"Ver estado de mi tesis"*). Al enviar un mensaje, el Agente GOD responde explicando qué hará, muestra una tarjeta visual de **Delegación en Curso** (`Director General ➔ subagente`), ejecuta el proceso en tiempo real y entrega el resumen junto con el botón para abrir o descargar el documento generado.
     - **Columna Lateral Compacta (Mapa Radial Simplificado + Estado en Vivo)**: Muestra qué agente está activo en ese instante en la estrella radial y el estado de conexión de **Bun**, **Claude Code** y **Factory Droid**.
2. **Vista 2: Detector de Agentes Locales (`Claude Code`, `Factory Droid`, `Bun`) & Terminal Bun**:
   - **Tarjetas de Diagnóstico de Instalación**: Cuatro tarjetas minimalistas que indican en tiempo real:
     - `Bun Runtime (bun)`: Estado (`Instalado` / `No detectado`), versión, ruta del binario y botón **"Instalar / Verificar Bun en Terminal"**.
     - `Claude Code CLI (claude)`: Estado (`Instalado` / `Puente Local Listo`), versión, cantidad de agentes detectados (`14 en .claude/agents/`) y comando de instalación/enlace (`bunx @anthropic-ai/claude-code` / `npm i -g @anthropic-ai/claude-code`).
     - `Factory Droid CLI (droid)`: Estado (`Instalado` / `Puente Local Listo`), versión, cantidad de droids sincronizados (`14 en .factory/droids/`) y botón de sincronización e instalación (`curl -fsSL https://app.factory.ai/cli | sh`).
     - `Motor Científico Python 3 + Git`: Estado verificado de los 26 scripts y repositorio Git.
   - **Consola Bun WebSocket**: Terminal limpia donde se ven los comandos ejecutados por `bun`, `claude`, `droid` o el usuario, con selector de motor de ejecución.
3. **Vista 3: Mis Proyectos de Investigación y Avances (Kanban Simple)**:
   - Selector claro de proyecto (*Tesis SIVAC UNAJMA*, *Artículo Científico Scopus* o botón **"Crear Nuevo Proyecto"**) con barra de progreso general, lista clara de tareas por etapas (`Por hacer`, `En curso`, `En revisión`, `Completado`) y un botón **"Pedir al Agente GOD que ejecute esta tarea"** en cada tarjeta.
4. **Vista 4: Interruptores de MCPs, Skills y Herramientas**:
   - Lista ordenada con interruptores simples (`Activado` / `Desactivado`) para conectar o desconectar servidores MCP (`.mcp.json`), herramientas y las 17 skills de los agentes sin configuraciones confusas.
5. **Vista 5: Mis Documentos (`.docx`, `.pdf`, `.xlsx`, `300 DPI`)**:
   - Galería limpia de entregables con vista previa inmediata y botón **"Descargar Archivo"** en un clic.

### Identidad Visual Minimalista
- **Dirección Estética**: *Calm Minimalist Research Workspace* — inspirado en la claridad de Linear, Notion y Claude Desktop. Mucho espacio en blanco (`#F8FAFC` y `#FFFFFF`), bordes finos de `1px solid #E2E8F0`, tipografía legible y cero saturación de cajas anidadas.
- **Paleta de Colores (`60-30-10`)**:
  - **60% Lienzo Neutro Luminoso**: `#F8FAFC` (`slate-50`) y `#FFFFFF` (`white`) para lectura descansada.
  - **30% Estructura y Tipografía**: `#0F172A` (`slate-900`) para títulos y `#475569` (`slate-600`) para explicaciones claras; `#0B0F19` (`slate-950`) reservado exclusivamente para la consola de terminal y el lienzo radial.
  - **10% Acento Funcional**: Azul institucional `#1E3A8A` (`blue-900`) para acciones del Agente GOD, Esmeralda `#047857` (`emerald-700`) para estados verificados/instalados y Ámbar `#B45309` (`amber-700`) cuando un CLI local requiere instalación o puente.
- **Tipografía**:
  - `Plus Jakarta Sans` (`400`, `600`, `700`) para toda la conversación, guías paso a paso y navegación.
  - `JetBrains Mono` (`tabular-nums`) para comandos de Bun/Claude/Droid, versiones de binarios y métricas.

---

## 3. Key Product Decisions & Trade-Offs

- **Decisión 1: Orquestación Conversacional Centrada en el Agente GOD (`director-general`)**
  - *Enfoque Elegido*: En lugar de obligar al usuario a rellenar formularios complejos de 8 campos para cada orden, el usuario escribe en un **Chat directo con el Agente GOD**. El servidor procesa el mensaje, construye automáticamente el contrato `comision.schema.json`, identifica el subagente de los Squads A–F, ejecuta la herramienta mediante **Bun / Claude / Droid** y transmite el progreso paso a paso en el chat y en la terminal.
  - *Por Qué*: Hace que el sistema sea inmediatamente intuitivo para cualquier persona sin perder ni un ápice del rigor metodológico (DEC-007, APA 7, Regla 01).
- **Decisión 2: Integración Real del Runtime `Bun` y Escáner de Binarios en Tiempo Real**
  - *Enfoque Elegido*: El servidor verifica e instala/habilita **Bun** (`~/.bun/bin/bun` o `/usr/local/bin/bun`) para ejecutar scripts y comandos con el motor de Bun (`bun --version`, `bun run`, `bunx`), y expone un endpoint `/api/system/cli-status` que inspecciona en tiempo real los binarios `bun`, `claude`, `droid`, `python3` y `git` en el sistema operativo.
  - *Por Qué*: Garantiza velocidad superior en la ejecución de comandos en terminal y ofrece transparencia total sobre qué motores están instalados en el entorno y cómo invocarlos en local o en contenedor.

---

## 4. Technical Architecture & Data Strategy *(Technical Reference)*

### Diagrama de Arquitectura Minimalista y Flujo del Chat GOD + Bun

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                 SIVAC-THESIS-LAB — INTERFAZ MINIMALISTA CENTRADA EN EL USUARIO           │
├──────────────────────┬───────────────────────────────────────────────────────────────────┤
│  NAVEGACIÓN LIMPIA   │  BARRA SUPERIOR: Proyecto Activo · Estado CLIs · Botón Terminal   │
│  (Sidebar 240px)     ├───────────────────────────────────────────────────────────────────┤
│                      │  [VISTA 1] CHAT CON EL AGENTE GOD (director-general)              │
│  1. Chat Agente GOD  │   ├─ Hilo Conversacional Claro + Botones de Órdenes Guiadas       │
│  2. Estado CLIs &    │   ├─ Tarjeta de Delegación Automática (GOD ➔ Subagente Squad A-F) │
│     Terminal Bun     │   └─ Mapa Radial Compacto en Vivo + Resultado y Handoff           │
│  3. Proyectos &      ├───────────────────────────────────────────────────────────────────┤
│     Avances (Kanban) │  [VISTA 2] DETECTOR DE CLIs (Bun · Claude Code · Droid) & CONSOLA │
│  4. MCPs, Skills &   │   ├─ Semáforo de Instalación Real (Versión, Ruta PATH, Config)    │
│     Herramientas     │   ├─ Acciones 1-Clic: Instalar Bun / Probar Claude / Sync Droid   │
│  5. Documentos DOCX  │   └─ Terminal Interactiva Bun Shell + Streaming WebSocket (/ws)   │
│     PDF & 300 DPI    ├───────────────────────────────────────────────────────────────────┤
│                      │  [VISTAS 3-5] KANBAN PROYECTOS · INTERRUPTORES MCP/SKILLS · DOCX  │
└──────────────────────┴─────────────────────────────────▲─────────────────────────────────┘
                                                         │ REST (/api/*) + WebSocket (/ws)
┌────────────────────────────────────────────────────────▼─────────────────────────────────┐
│                    SERVIDOR FULL-STACK + MOTOR BUN SHELL & PUENTE CLI                    │
├────────────────────────────┬───────────────────────────┬─────────────────────────────────┤
│  ORQUESTADOR DEL CHAT GOD  │  ESCÁNER & MOTOR BUN CLI  │  PUENTE CLAUDE CODE & DROID     │
│  • Analiza intención del   │  • Detecta binarios en    │  • Ejecuta `claude -p --agent`  │
│    usuario (Loop 3.0)      │    PATH (`bun`, `claude`, │    con `--output-format`        │
│  • Selecciona Subagente    │    `droid`, `python3`)    │  • Ejecuta `droid exec --auto`  │
│    (Squads A–F) y genera   │  • Ejecuta procesos con   │  • Sincroniza `.claude/`,       │
│    contrato + handoff real │    Bun Shell / child_proc │    `.factory/` y `.mcp.json`    │
└────────────────────────────┴───────────────────────────┴─────────────────────────────────┘
```

### Modelo de Datos para el Chat GOD y el Detector de CLIs
1. **Historial de Conversación y Delegación (`GodChatMessage`)**:
   - Cada mensaje en el chat contiene: `id`, `role` (`user` | `god` | `subagent`), `timestamp`, `text`, y un objeto opcional `delegation` con el subagente comisionado (`subagente`, `squad`, `fase`, `runtimeUsed`: `'bun'` | `'claude'` | `'droid'`, `command`, `cliCommandForLocal`, `status`, `outputSummary`, `handoffPath`, `deliverablePath`).
2. **Estado de Detección de Motores (`CliDetectionStatus`)**:
   - Devuelto por `GET /api/system/cli-status` y actualizado vía WebSocket:
     - `bun`: `{ installed: boolean, version: string, binaryPath: string, installCmd: string }`
     - `claudeCode`: `{ installed: boolean, version: string, binaryPath: string, agentsCount: number, headlessFlag: string, installCmd: string }`
     - `factoryDroid`: `{ installed: boolean, version: string, binaryPath: string, droidsCount: number, execFlag: string, installCmd: string }`
     - `python`: `{ installed: boolean, version: string, scriptsCount: number }`

### Mapeo Interactivo de Componentes y Manejadores de Estado
- **Chat con el Agente GOD (`POST /api/god-chat`)**:
  - Cuando el usuario envía una orden en lenguaje natural (o pulsa una sugerencia rápida), el Agente GOD responde inmediatamente en el chat explicando el diagnóstico metodológico, activa en vivo el nodo del subagente en el mapa radial, ejecuta la tarea a través del motor **Bun / Claude / Droid**, transmite el progreso por WebSocket y adjunta en la burbuja de respuesta tanto el resultado verificado como el comando exacto de Claude Code (`claude -p ... --agent ...`) y Factory Droid (`droid exec ...`) junto con el enlace directo al archivo o `handoff`.
- **Detector e Instalador de CLIs (`GET /api/system/cli-status` y `POST /api/system/install-cli`)**:
  - Permite verificar con un clic si `bun`, `claude` y `droid` están instalados en el entorno, instalar o actualizar `bun` en vivo, sincronizar `.factory/droids/` con `.claude/agents/` y probar la ejecución directa en la terminal.
