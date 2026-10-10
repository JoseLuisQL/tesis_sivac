# MANUAL DE USO Y OPERACIÓN — SIVAC-THESIS-LAB
> **Guía Oficial para el Tesista: Operación de la Granja de Agentes de Investigación Científica**  
> **Escuela Profesional de Ingeniería de Sistemas — Universidad Nacional José María Arguedas (UNAJMA)**  
> **Tesista / Autor:** Bach. José Luis Quispe León  
> **Asesora:** Dra. Norma Lorena Catacora Flores  
> **Versión del Ecosistema:** v3.0 (Arquitectura Multiagente Dual) — Octubre 2026  

---

## 1. Introducción y Rol del Tesista

Bienvenido a **SIVAC-THESIS-LAB**, el entorno computacional de investigación científica diseñado para asistir en la redacción, validación psicométrica, análisis bioestadístico y maquetación de tu tesis de grado:

> **“APLICACIÓN DEL SISTEMA ‘SIVAC’ PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II”**

### 1.1. Principio Rector de Mando
- **Tú eres la máxima autoridad del proyecto (Investigador Principal).**
- La granja de agentes genera propuestas, compila borradores y realiza auditorías formales, pero **ningún avance o capítulo definitivo se da por concluido sin tu revisión y aprobación expresa**.
- Toda la arquitectura opera en torno al **Director General (`director-general`)**, quien es el único que interactúa contigo y el único facultado para delegar tareas a los 13 subagentes especialistas.

---

## 2. Topología del Sistema y Catálogo de Squads

El sistema utiliza una **Topología Hub-and-Spoke radial (Estrella Jerárquica)**:

```text
                  ┌────────────────────────────────────────┐
                  │             TESISTA HUMANO             │
                  │        (Bach. José Luis Quispe)        │
                  └───────────────────▲────────────────────┘
                                      │ Aprobación / Instrucción
                  ┌───────────────────▼────────────────────┐
                  │            DIRECTOR GENERAL            │
                  │              (Agente GOD)              │
                  └───────────────────┬────────────────────┘
                                      │ Delegación
     ┌────────────────┬───────────────┼───────────────┬────────────────┐
┌────▼────┐      ┌────▼────┐     ┌────▼────┐     ┌────▼────┐      ┌────▼────┐
│ SQUAD A │      │ SQUAD B │     │ SQUAD C │     │ SQUAD D │      │ SQUAD E │
│Evidencia│      │Metodol. │     │Ing. XP  │     │Bioestad.│      │Redacción│
└─────────┘      └─────────┘     └─────────┘     └─────────┘      └─────────┘
                                      │
                                 ┌────▼────┐
                                 │ SQUAD F │
                                 │Gobernan.│
                                 └─────────┘
```

### 2.1. Directorio de Squads y Especialistas
1. **Squad A (Evidencia y Bibliometría):**
   - `investigador-bibliografico`: Búsqueda sistemática, recuperación de literatura y Zotero.
   - `verificador-integridad`: Auditoría anti-alucinaciones y verificación 1:1 de citas APA 7.
2. **Squad B (Metodología y Psicometría):**
   - `guardian-consistencia`: Custodio estricto de las 3 dimensiones oficiales fijadas por DEC-007.
   - `especialista-instrumentos`: Diseño psicométrico y evaluación de juicio de expertos ($V$ de Aiken, $IVC$).
   - `especialista-forms`: Formatos de recolección y herramientas digitales.
3. **Squad C (Ingeniería de Software SIVAC):**
   - `ingeniero-sivac`: Inspección técnica del repositorio SIVAC (`syncova`) en **estricto modo de solo lectura**.
   - `documentador-xp`: Redactor de la metodología Extreme Programming (historias de usuario, diagramas e iteraciones).
4. **Squad D (Bioestadística e Inferencia):**
   - `analista-estadistico`: Pruebas de normalidad (Shapiro-Wilk) y contrastes de hipótesis pareadas (Wilcoxon, $n=14$).
5. **Squad E (Redacción y Maquetación Editorial):**
   - `analista-documental`: Inspección de estilos según modelos UNAJMA (`Fany 2024`, `Jhon 2026`).
   - `redactor-academico`: Prosa científica rigurosa y técnica en español.
   - `maquetador-docx`: Compilación de documentos Word (.docx) mediante OpenXML desvinculado, tablas APA 7 y figuras a 300 DPI.
6. **Squad F (Gobernanza y Evaluación Simulada):**
   - `curador-cerebro`: Mantenimiento y custodia del vault de Obsidian.
   - `jurado-revisor`: Simulador de tribunal de sustentación de la UNAJMA (rúbrica de 20 puntos).

---

## 3. Cómo Interactuar con el Sistema (Claude Code vs. Factory Droid)

El ecosistema cuenta con soporte dual nativo. Puedes trabajar con la interfaz que prefieras:

### 3.1. Modo Claude Code CLI
En este entorno ejecutas tus instrucciones directamente en la consola de Claude Code.
- La sesión principal siempre asume el rol del **Director General**.
- El Director General invoca a los subagentes mediante la herramienta interna `Agent` con el parámetro `subagent_type: "<nombre-agente>"`.
- **Ejemplo de instrucción para el tesista:**
  > *"Director General, por favor comisiona al redactor-academico para que afine la discusión del Capítulo VI contrastando con las fuentes de Wasswa et al. y Chekol et al."*

### 3.2. Modo Factory Droid CLI
En este entorno ejecutas a través de Factory Droid (`droid`).
- La sesión principal asume el rol de orquestación.
- El Director General comisiona a los subagentes mediante la herramienta `Task` especificando el droid correspondiente (`subagent_type: "<nombre-agente>"`).
- **Ejemplo de instrucción para el tesista:**
  > *"Director General, solicita al guardian-consistencia que realice una auditoría metodológica de los indicadores de la Dimensión 2."*

### 3.3. Estructura de Comisión Estándar
Cuando solicites una tarea compleja, el Director General generará un contrato de comisión formal:
```text
TAREA: <Acción concreta>
FASE: <Fase del proyecto según ESTADO_TESIS.md>
SQUAD: <Squad asignado>
SUBAGENTE: <nombre-agente>
ENTRADAS: <Rutas exactas de insumos>
SALIDA ESPERADA: <Ruta y formato de archivo entregable>
RESTRICCIONES: <Reglas canónicas aplicables>
CRITERIO DE ÉXITO: <Condición de aceptación objetiva>
```

---

## 4. Sincronización Determinista del Ecosistema (`scripts/sync_factory.py`)

### 4.1. Regla Canónica de la Única Fuente de Verdad (SSOT)
- La carpeta **`.claude/`** es la **ÚNICA FUENTE DE VERDAD**.
- **JAMÁS debes editar manualmente los archivos en `.factory/`**, ya que son artefactos generados automáticamente y cualquier cambio se perdería en la siguiente sincronización.
- Cuando desees ajustar un agente, una regla o una skill, modifica el archivo correspondiente en `.claude/` y luego corre el sincronizador.

### 4.2. Comandos de Sincronización
Abre una terminal PowerShell en la raíz del proyecto (`C:\MisInvestigaciones\tesis\sivac`) y utiliza:

1. **Sincronizar cambios normales:**
   ```powershell
   python scripts/sync_factory.py
   ```
   *Analiza `.claude/`, traduce las herramientas a formato Droid, sincroniza las 21 skills, mapea los 5 servidores MCP y actualiza los hooks de seguridad.*

2. **Verificar integridad del sistema (Auditoría de 0 inconsistencias):**
   ```powershell
   python scripts/sync_factory.py --check
   ```
   *Comprueba que los 14 droids, 21 skills, 5 servidores MCP y los hooks estén 100% alineados y reporta el estado de salud del entorno.*

3. **Forzar sobrescritura completa:**
   ```powershell
   python scripts/sync_factory.py --force
   ```
   *Reescribe íntegramente todos los artefactos en `.factory/` a partir de `.claude/`.*

---

## 5. Consulta y Navegación del Cerebro Digital (Obsidian)

Toda la memoria viva, bitácoras y estado de avance se custodian en:  
`C:\MisInvestigaciones\obsidian_vault`

### 5.1. Archivos Clave para el Tesista
1. **`00_SISTEMA/ESTADO_TESIS.md`:**
   - **Es la única fuente de verdad sobre el avance real de la tesis.**
   - Contiene el semáforo de fases (F0 a F9), los acuerdos metodológicos y la relación de entregables oficiales.
2. **`08_SISTEMA_Y_AGENTES/bitacoras/<nombre-agente>.md`:**
   - Historial cronológico de intervenciones de cada uno de los especialistas.
   - Si deseas saber qué hizo un agente en una fecha determinada, consulta su bitácora.
3. **`08_SISTEMA_Y_AGENTES/handoffs/`:**
   - Notas de relevo oficiales emitidas al culminar cada tarea (`AAAA-MM-DD_<agente>_<tarea>.md`).
   - Contienen: productos generados, hallazgos clave, aspectos pendientes a verificar con el tesista y riesgos metodológicos.
4. **`06_METODOLOGIA_E_INSTRUMENTOS/`:**
   - Dictámenes metodológicos, matrices de consistencia y protocolos de evaluación.
5. **`04_LITERATURA_Y_FUENTES/`:**
   - Catálogo maestro de fuentes bibliográficas con citekeys de Zotero y enlaces a los 27 PDFs primarios.

### 5.2. Cómo Explorar el Vault
- Abre la aplicación **Obsidian** y apunta el espacio de trabajo a la carpeta `C:\MisInvestigaciones\obsidian_vault`.
- Abre el archivo `HOME.md` en el panel principal para navegar interactivamente a través de los MOCs (Maps of Content).

---

## 6. Pipeline de Compilación de Documentos Word (.docx)

Los documentos finales se construyen mediante generadores de OpenXML desvinculado de alta precisión alojados en `scripts/compiladores/`.

### 6.1. Compilación del Informe Final de Tesis
Para generar el documento maestro completo del informe final:
```powershell
python scripts/compiladores/compilar_informe_final_docx.py
```
- **Salida generada:** `salidas/documentos/informe_final_v01.docx`.
- **Características del documento:**
  - Paginación romana en preliminares (`i, ii, iii...`) con carátula desvinculada.
  - Paginación arábiga reiniciada en `1` desde la `INTRODUCCIÓN`.
  - 18 tablas nativas APA 7 de tres líneas horizontales.
  - 19 figuras oficiales a 300 DPI con leyendas académicas.
  - 12 ecuaciones matemáticas nativas OMML (centradas y numeradas).
  - Cero ocurrencias del carácter de guion largo (`U+2014`).
  - Índices nativos de contenido, tablas y figuras mediante instrucciones de campo OpenXML (`TOC`).

### 6.2. Compilación del Expediente de Validación de Instrumentos
Para generar los instrumentos oficiales y el expediente de juicio de expertos:
```powershell
python scripts/compiladores/generar_expedientes_e_instrumentos.py
```
- **Salidas generadas en `salidas/instrumentos/`:**
  - `INSTRUMENTO_01_FICHA_TIEMPOS.docx` (Medición de $T_{reg}$ y $T_{vale}$).
  - `INSTRUMENTO_02_GUIA_COTEJO.docx` (Auditoría de $RSD$ con 8 criterios y $CPE$).
  - `INSTRUMENTO_03_CUESTIONARIO_TAM.docx` (Medición de satisfacción $AP$ y $UP$).
  - `EXPEDIENTE_VALIDACION_JUICIO_EXPERTOS_SIVAC.docx` (Expediente oficial para los jueces de la EPIS-UNAJMA).

---

## 7. Protocolos de Seguridad y Buenas Prácticas

Para salvaguardar la integridad de la investigación, ten en cuenta las siguientes directrices:

1. **Protección del Sistema SIVAC (`C:\Proyectos\syncova`):**
   - El código fuente de la aplicación web en producción es estrictamente intocable por los agentes de tesis.
   - El hook `PreToolUse` bloquea en tiempo real cualquier intento de escritura o borrado sobre este directorio.
2. **Inmutabilidad de Insumos Base (`referencias/`):**
   - Las tesis modelo institucionales (`Fany 2024`, `Jhon 2026`) y el archivo base original (`PROYECTO_TESIS.docx`) no deben editarse. Toda modificación se efectúa en `salidas/`.
3. **Cero Invención Empírica:**
   - La fase de resultados inferenciales (Capítulo V) permanecerá bloqueada hasta que realices la recolección física en campo y entregues los datos empíricos reales en `datos/raw/`.
4. **Respaldos en Git:**
   - Tras concluir sesiones de trabajo significativas, realiza commits en los repositorios locales:
     ```powershell
     git -C C:\MisInvestigaciones\tesis\sivac add .
     git -C C:\MisInvestigaciones\tesis\sivac commit -m "feat(avance): descripcion del avance"
     ```

---

## 8. Resumen de Flujo de Trabajo Típico para el Tesista

```text
1. Abrir terminal en C:\MisInvestigaciones\tesis\sivac.
2. Iniciar sesión en Claude Code o Factory Droid.
3. Consultar ESTADO_TESIS.md para verificar la fase activa.
4. Dar instrucción clara al Director General (quien delegará al subagente experto).
5. Revisar los productos generados en salidas/ o notas en obsidian_vault/.
6. Si estás conforme con el entregable, brindar tu aprobación expresa para avanzar.
```
