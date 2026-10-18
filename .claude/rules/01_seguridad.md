---
description: Reglas de seguridad absolutas e innegociables para SIVAC-THESIS-LAB
---

# REGLA CANÓNICA 01: SEGURIDAD Y PROTECCIÓN DE ACTIVOS

## 1. Código Fuente SIVAC (`C:\Proyectos\syncova`)
- **Modo Estricto de SOLO LECTURA:** El directorio del software SIVAC es intocable.
- Queda terminantemente prohibido crear, modificar, mover o borrar cualquier archivo dentro de `C:\Proyectos\syncova`.
- Cualquier intento es interceptado y bloqueado con código 1 por el hook `PreToolUse` en `.claude/hooks/pretooluse_blocker.cjs`.
- El agente `ingeniero-sivac` tiene permisos de herramientas restringidos por mínimo privilegio (`Read`, `Grep`, `Glob`).

## 2. Inmutabilidad de Documentos e Insumos Originales
- Los archivos originales de referencia jamás se sobrescriben ni modifican:
  - `PROYECTO_TESIS.docx` (Documento base aprobado).
  - `referencias/modelos_tesis/` (o `ejemplos_tesis/`: Tesis modelo UNAJMA Fany 2024 y Jhon 2026).
  - `referencias/modelos_validacion/` (o `ejemplo_validacion/`: formatos históricos de validación; el modelo vigente por DEC-015 es el Anexo 2 de Fany 2024).
- Toda edición o compilación se realiza sobre copias de trabajo versionadas en `salidas/documentos/` (`informe_final_v01.docx`, `informe_final_v02.docx`, etc.).

## 3. Integridad Empírica (Cero Simulación de Datos de Campo)
- Queda **estrictamente prohibido inventar, simular o extrapolar datos numéricos empíricos** de pretest, postest o encuestas.
- Sin datos reales entregados directamente por el tesista en `datos/raw/`, el análisis inferencial permanece en estado `BLOQUEADO: esperando datos de campo`.

## 4. Preservación del Cerebro Obsidian (`C:\MisInvestigaciones\obsidian_vault`)
- El vault es un archivo histórico vivo con investigaciones y notas atómicas previas.
- **Principio de no destrucción:** No se borra ni destruye ninguna nota existente.
- Toda nota nueva debe incluir YAML frontmatter válido con `tipo`, `fase`, `agente`, `estado`, `fecha_actualizacion`.

## 5. Protección de Credenciales y Secretos
- Ninguna API key o token se guarda en archivos versionados por Git.
- Se gestionan en `.claude/settings.local.json` (listado en `.gitignore`).
