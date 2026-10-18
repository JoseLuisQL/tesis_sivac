---
name: protocolo-obsidian-handoff
description: Protocolo estricto para lectura, escritura y relevos (handoffs) en el vault de Obsidian de SIVAC-THESIS-LAB con arquitectura académica canónica.
---

# Protocolo de Trabajo en Obsidian y Relevos (Handoffs)

Este protocolo rige la interacción de todos los 14 agentes con el cerebro central del equipo (`C:\MisInvestigaciones\obsidian_vault`).

---

## 1. Arquitectura Canónica del Vault (10 Carpetas)
Todos los agentes deben ubicar sus lecturas y escrituras exclusivamente dentro de esta taxonomía:

```
obsidian_vault/
├── 00_SISTEMA/                     ← Gobernanza, semáforo, reglas y glosario
├── 01_MOCS/                        ← Mapas de Contenido y navegación de alto nivel
├── 02_PROYECTOS/                   ← Proyectos de investigación (02.1_TESIS_SIVAC)
├── 03_CONCEPTOS_ATOMICOS/          ← Red Zettelkasten permanente de notas atómicas
├── 04_LITERATURA_Y_FUENTES/        ← Catálogo Zotero, notas de fuentes, libros y PDFs
├── 05_MODELOS_Y_REFERENCIAS/       ← Tesis modelo UNAJMA y formatos de validación (vigente: Fany 2024)
├── 06_METODOLOGIA_E_INSTRUMENTOS/  ← Instrumentos SIVAC, juicio expertos y bancos de citas
├── 07_ESTADISTICA_Y_DATOS/         ← Scripts reproducibles, figuras APA 7 300 DPI y datos
├── 08_SISTEMA_Y_AGENTES/           ← Bitácoras y handoffs de los 14 agentes
├── 09_CANVAS_Y_DIAGRAMAS/          ← Tableros visuales y diagramas conceptuales
├── _adjuntos/                      ← Repositorio universal de imágenes y media
└── 99_INBOX/                       ← Bandeja de entrada para captura rápida
```

---

## 2. Reglas de Escritura en Notas de Obsidian
1. **Frontmatter YAML obligatorio:** Cada nota creada debe iniciar con metadatos:
   ```yaml
   ---
   tipo: [sistema | borrador | ficha | instrumento | codigo | resultado | reporte | moc]
   fase: [F0 | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9]
   agente: [nombre-del-agente]
   estado: [borrador | revisado | aprobado]
   fuentes: [@citekey1, @citekey2]
   fecha: AAAA-MM-DD
   ---
   ```
2. **Uso de enlaces internos:** Vincular conceptos, variables y fuentes mediante `[[Nombre_Nota]]`.
3. **Fichas bibliográficas:** Se ubican en `04_LITERATURA_Y_FUENTES/notas_fuentes_zotero/` con su identificador `@citekey`.
4. **Imágenes y Archivos Adjuntos:** Toda figura, captura de pantalla o gráfico generado debe guardarse en `_adjuntos/` o en `07_ESTADISTICA_Y_DATOS/figuras_apa7_300dpi/`.
5. **Preservación estricta:** Prohibido borrar notas o información histórica previa.

---

## 3. Protocolo de Relevo (Handoff) al finalizar una tarea
Al completar cualquier encargo formal del Director General, el subagente DEBE:
1. Crear una nota de relevo en `08_SISTEMA_Y_AGENTES/handoffs/AAAA-MM-DD_<agente>_<tarea>.md`.
2. Estructurar el relevo con el siguiente formato:
   ```markdown
   # RELEVO DE TAREA: <nombre de la tarea>
   - **Agente:** <nombre>
   - **Fecha:** <AAAA-MM-DD>
   - **Fase:** <Fx>
   - **Estado:** completado | parcial | bloqueado
   
   ## Productos Generados
   - `ruta/al/archivo1.md`
   
   ## Hallazgos Clave
   1. ...
   
   ## Asuntos Pendientes / [VERIFICAR]
   - ...
   
   ## Riesgos e Incoherencias Detectadas
   - ...
   
   ## Siguiente Acción Sugerida
   - ...
   ```
3. Anexar la entrada en su bitácora personal en `08_SISTEMA_Y_AGENTES/bitacoras/<agente>.md`.
