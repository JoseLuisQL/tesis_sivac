---
name: protocolo-obsidian-handoff
description: Protocolo estricto para lectura, escritura y relevos (handoffs) en el vault de Obsidian de SIVAC-THESIS-LAB.
---

# Protocolo de Trabajo en Obsidian y Relevos (Handoffs)

Este protocolo rige la interacción de todos los agentes con el cerebro del equipo (`C:\MisInvestigaciones\obsidian_vault`).

## 1. Reglas de Escritura en Notas de Obsidian
1. **Frontmatter YAML obligatorio:** Cada nota creada debe iniciar con metadatos:
   ```yaml
   ---
   tipo: [sistema | borrador | ficha | instrumento | codigo | resultado | reporte]
   fase: [F0 | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9]
   agente: [nombre-del-agente]
   estado: [borrador | revisado | aprobado]
   fuentes: [@citekey1, @citekey2]
   fecha: AAAA-MM-DD
   ---
   ```
2. **Uso de enlaces internos:** Vincular conceptos, variables y fuentes mediante `[[Nombre_Nota]]`.
3. **Fichas bibliográficas:** Deben ubicarse en `04_LITERATURA/fichas/` y nombrarse `@citekey.md`.
4. **No destrucción:** No borrar ni sobrescribir notas existentes sin autorización expresa.

## 2. Protocolo de Relevo (Handoff) al finalizar una tarea
Al completar cualquier encargo, el subagente DEBE:
1. Crear una nota de relevo en `07_AGENTES/handoffs/AAAA-MM-DD_<agente>_<tarea>.md`.
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
3. Anexar la entrada en su bitácora personal en `07_AGENTES/bitacoras/<agente>.md`.
