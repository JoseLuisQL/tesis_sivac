# CATÁLOGO E INVESTIGACIÓN PROFUNDA DE SERVIDORES MCP (FASE C)
> **Proyecto:** SIVAC-THESIS-LAB — Granja de Agentes de Investigación Científica  
> **Fecha de Emisión:** 2026-10-09  
> **Plataformas Evaluadas:** Claude Code CLI (v2.1+) & Factory Droid CLI (v0.237+)  
> **Objetivo:** Auditoría exhaustiva de capacidades, seguridad, consumo y principio de mínimo privilegio.

---

## 1. Estado de Conexión y Diagnóstico de Servidores MCP

| Servidor MCP | Tipo / Transporte | Estado en Claude Code | Estado en Factory Droid | Autenticación / Coste | Observación Diagnóstica |
|---|---|---|---|---|---|
| **zotero** | `stdio` (`zotero-mcp.exe`) | **✔ Connected** | **✔ Connected** | Local SQLite (`ZOTERO_LOCAL=true`) / **Gratuito** | Acceso instantáneo a la biblioteca local (199 ítems) y colección SIVAC (`4XAQ6D3D`). |
| **ydc-server** | `http` (`https://api.you.com/mcp`) | **✔ Connected** | **✔ Connected** | Bearer API Key / Saldo: **$99.33 USD** (9933 céntimos) | Búsqueda científica y extracción de contenidos web académicos. |
| **firecrawl** | `http` (`https://mcp.firecrawl.dev/v2/mcp`) | **✔ Connected** | **✔ Connected** | Bearer API Key / Saldo: **21,019 créditos** | Web scraping, rastreo profundo y extracción limpia en Markdown de artículos. |
| **context7** | `http` (`https://mcp.context7.com/mcp`) | **✔ Connected** | No en `~/.factory/mcp.json` | API Key / Documentación de librerías | Usado por `ingeniero-sivac` y `documentador-xp` para consultar SDKs y librerías. |
| **playwright** | `stdio` (`npx @playwright/mcp`) | **✔ Connected** | **✔ Connected** | Local headless browser / **Gratuito** | Automatización web e inspección de interfaces E2E. |
| **chrome-devtools** | `stdio` (`npx chrome-devtools-mcp`) | No configurado | **✔ Connected** | Local Chrome CDP / **Gratuito** | Inspección DOM de bajo nivel, consola y métricas web. |
| *Latted* | `stdio` (`mcp-remote`) | **✘ Timed out** | No configurado | Remoto caído | Servidor obsoleto en Claude; genera ruido en arranque. |
| *open-design* | `stdio` (Daemon local) | **✘ Timed out** | No configurado | Local no iniciado | Servidor de diseño desconectado. |

---

## 2. Herramientas Reales Expuestas y Pruebas Inocuas Ejecutadas

### 2.1. Zotero MCP (`zotero-mcp.exe`)
- **Herramientas Clave Expuestas:**
  - `zotero_list_libraries`: Lista bibliotecas del usuario (Personal ID=1).
  - `zotero_get_collections`: Árbol jerárquico de colecciones con sus claves alfanuméricas de 8 caracteres.
  - `zotero_search_items`: Búsqueda por coincidencia de subcadena (`titleCreatorYear` o `everything`).
  - `zotero_get_item_metadata`, `zotero_get_item_fulltext`, `zotero_read_pdf_pages`.
  - `zotero_export_bibliography`: Generación de bibliografía en estilos estándar.
- **Prueba Inocua Ejecutada:**
  - `zotero_get_collections()` $\longrightarrow$ Identificó colección oficial `TESIS_SIVAC_BIBLIOGRAFIA_ZOTERO` (Key: `4XAQ6D3D`).
  - `zotero_search_items(collection_key="4XAQ6D3D", query="Beck")` $\longrightarrow$ Recuperó exitosamente `Beck, Kent (1999). Embracing change with extreme programming` (Item Key: `B9CZXTV4`).
- **Límites y Coste:** Local, sin cuotas de red ni coste por consulta.

### 2.2. You.com MCP (`ydc-server`)
- **Herramientas Clave Expuestas:**
  - `ydc-server___you-search`: Búsqueda web contextual con snippets de alta relevancia.
  - `ydc-server___you-contents`: Extracción del cuerpo textual de páginas web encontradas.
  - `ydc-server___you-balance`: Consulta del saldo remanente de la cuenta.
- **Prueba Inocua Ejecutada:**
  - `ydc-server___you-balance()` $\longrightarrow$ Saldo verificado: **9,933 céntimos** ($99.33 USD).
- **Límites y Coste:** Pago por uso sobre créditos prepagados. Muy eficiente para rastreo bibliográfico rápido.

### 2.3. Firecrawl MCP (`firecrawl`)
- **Herramientas Clave Expuestas:**
  - `firecrawl___firecrawl_scrape`: Conversión de cualquier URL científica o institucional a Markdown limpio.
  - `firecrawl___firecrawl_search`: Búsqueda web con extracción directa.
  - `firecrawl___firecrawl_crawl`: Rastreo estructurado de sitios completos.
  - `firecrawl___firecrawl_research_search_papers`: Búsqueda especializada de papers científicos.
  - `firecrawl___firecrawl_credit_usage`: Consulta de consumo y saldo de créditos.
- **Prueba Inocua Ejecutada:**
  - `firecrawl___firecrawl_credit_usage()` $\longrightarrow$ Saldo verificado: **21,019 créditos restantes** (Periodo: 2026-09-29 al 2026-10-29).
- **Límites y Coste:** 21k créditos disponibles. Ideal para papers que no tienen descarga directa vía API.

### 2.4. Playwright & Chrome DevTools MCP
- **Herramientas Clave Expuestas:**
  - Navegación, toma de capturas de pantalla, inspección de consola de JavaScript y evaluación de selectores DOM.
- **Uso en la Tesis:** Inspección visual de la interfaz del sistema SIVAC (`syncova`) para documentar la sección 3.3 de Extreme Programming y verificar los flujos de PECOSA, vales y kardex en navegador real.

---

## 3. Clasificación Funcional de MCPs

```
├── 1. Bibliografía y Literatura Científica (Núcleo Epistemológico)
│   ├── zotero (Fuente de verdad primaria de citas, metadatos y PDFs)
│   ├── ydc-server (Descubrimiento y búsqueda de literatura académica reciente)
│   └── firecrawl (Extracción de papers y páginas técnicas a Markdown)
│
├── 2. Auditoría de Código y Arquitectura de Software
│   └── context7 (Documentación oficial de frameworks, Prisma, PostgreSQL y React)
│
├── 3. Pruebas de Interfaz y Evidencia Visual del Software
│   ├── playwright (Automatización E2E y capturas del sistema SIVAC)
│   └── chrome-devtools (Inspección técnica de rendimiento y errores en consola)
│
└── 4. Memoria y Sistema de Archivos
    └── Sistema de Archivos Nativo (Obsidian Vault, DOCX, scripts en .venv)
```

---

## 4. Detección de Brechas (Gaps) y Redundancias

1. **Redundancia:** `playwright` y `chrome-devtools` se solapan en inspección de páginas web. Playwright es superior para flujos automatizados de usuario en formularios de SIVAC, mientras que Chrome DevTools es más directo para inspección de red. Mantener ambos pero asignar preferentemente Playwright a los agentes de interfaz.
2. **Brecha Crítica (Verificación DOI):** Actualmente la verificación de DOIs contra Crossref se realiza mediante el script `verificador_integridad.py` utilizando la librería Python `habanero` / peticiones HTTPS directas. No existe un MCP dedicado a Crossref/OpenAlex. Dado que el script local en Python funciona de manera determinista y sin consumir tokens de LLM, **se recomienda conservar la verificación de DOI en el script Python** en lugar de saturar el contexto con herramientas MCP adicionales.
3. **Servidores Caídos en Claude:** `Latted` y `open-design` deben eliminarse de `.claude/` para acelerar el tiempo de inicio de Claude Code y eliminar los tiempos muertos de 30 segundos (`timed out`).

---

## 5. Matriz Maestra: Agente $\times$ MCP $\times$ Herramientas (Mínimo Privilegio)

| Agente | MCP Autorizados | Herramientas MCP Específicas Permitidas | Justificación de Restricción |
|---|---|---|---|
| **director-general** | `zotero`, `ydc-server`, `firecrawl` | Consultas de lectura, balance, búsqueda bibliográfica | Visión global y verificación general de insumos. |
| **investigador-bibliografico** | `zotero`, `ydc-server`, `firecrawl` | `zotero_search_*`, `zotero_get_*`, `you-search`, `firecrawl_scrape`, `firecrawl_research_*` | Búsqueda exhaustiva y descarga de literatura académica. |
| **verificador-integridad** | `zotero` | `zotero_search_items`, `zotero_get_item_metadata` | Solo cotejo 1:1 de metadatos existentes. No realiza búsquedas web abiertas. |
| **guardian-consistencia** | *Ninguno (Filesystem)* | *Solo herramientas de lectura de archivos locales* | Su labor es de consistencia lógica entre capítulos y matrices. |
| **especialista-instrumentos** | *Ninguno (Filesystem)* | *Solo herramientas de archivos locales* | Diseña formatos en Word y hojas de cálculo. |
| **especialista-forms** | `playwright` | Navegación e interacción básica para validar formularios | Inspección de formularios digitales generados. |
| **ingeniero-sivac** | `context7` | Búsqueda de documentación de arquitectura y APIs | Auditoría técnica de código en modo SOLO LECTURA. |
| **documentador-xp** | `context7`, `playwright` | Documentación técnica y capturas de pantalla de SIVAC | Redacción de la sección 3.3 con evidencia visual del software. |
| **analista-estadistico** | *Ninguno (Filesystem / Python)* | *Scripts deterministas de scipy, pingouin, statsmodels* | El cálculo bioestadístico debe ser 100% determinista vía script, sin intermediación de LLM. |
| **analista-documental** | *Ninguno (Filesystem)* | *Inspección OpenXML / PDF local* | Auditoría estructural de modelos UNAJMA. |
| **redactor-academico** | `zotero` | `zotero_get_item_metadata` (solo lectura de fuentes aprobadas) | Redacta con citas reales; no añade nuevas fuentes sin pasar por el investigador. |
| **maquetador-docx** | *Ninguno (Filesystem / Word COM)* | *python-docx y win32com* | Compilación OpenXML nativa sin dependencias de red. |
| **curador-cerebro** | *Ninguno (Filesystem)* | *Gestión de Markdown en Obsidian Vault* | Preservación de la taxonomía y memoria viva. |
| **jurado-revisor** | *Ninguno (Filesystem)* | *Lectura de entregables y rúbricas locales* | Evaluación colegiada independiente sin sesgo externo. |
