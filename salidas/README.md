# CAPA 4: Entregables y Artefactos Generados (`salidas/`)

Estructura canónica de entregables conforme a `CLAUDE.md` y las decisiones metodológicas vigentes (**DEC-007**, **DEC-014**, **DEC-015**, **DEC-016**, **DEC-019**, **DEC-020**):

- `salidas/documentos/`: Informes finales versionados (`informe_final_v01.docx`, `informe_final_v02.docx`, ...) compilados con cirugía OpenXML nativa (`scripts/utilidades/docx_quirurgico.py`), y `anexos_fany/` para el certificado de validación Fany 2024 en blanco.
- `salidas/figuras/`: Gráficos y diagramas oficiales exportados a **300 DPI** reales en formato PNG con metadatos DPI verificados.
- `salidas/instrumentos/`: Fichas de recolección (Instrumentos 01 y 02 bajo PMMV) y Cuestionario TAM (Instrumento 03, Modalidad A de 8 reactivos y Modalidad B anexa), más el Certificado Único Fany 2024 en blanco.
- `salidas/reportes_estadisticos/`: Reportes reproducibles generados por `scripts/estadistica/pipeline_inferencial.py` únicamente cuando `datos/raw/MANIFEST.json` está sellado con datos reales.
- `salidas/reportes_jurado/`: Dictámenes y revisiones simuladas en escala vigesimal (0–20) emitidas por `jurado-revisor` (UNAJMA).
- `salidas/archivo/`: Resguardo histórico y cuarentena de versiones previas (`_material_apocrifo_no_usar/`).
