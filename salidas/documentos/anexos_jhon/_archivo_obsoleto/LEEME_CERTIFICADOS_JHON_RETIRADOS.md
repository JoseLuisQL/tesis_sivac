# CERTIFICADOS JHON RETIRADOS DE LA RUTA OFICIAL

**Retiro registrado:** 2026-10-18 | **Responsable:** `maquetador-docx` (Squad E) | **Fundamento:** DEC-015, DEC-016 y DEC-020

## 1. Contenido

Tres documentos retirados de la raíz de `salidas/documentos/anexos_jhon/` y conservados íntegros, sin edición: `ANEXO_6_VALIDACION_EXPERTO_1_JHON_ESPEJO_VACIO.docx`, `ANEXO_6_VALIDACION_EXPERTO_2_JHON_ESPEJO_VACIO.docx` y `ANEXO_6_VALIDACION_EXPERTO_3_JHON_ESPEJO_VACIO.docx`.

## 2. Motivo del retiro

El modelo Jhon 2026 fue sustituido como formato de validación por el modelo Fany 2024 mediante DEC-015. Su generador, `scripts/compiladores/generar_anexo6_validacion_experto_jhon.py`, está neutralizado con `raise SystemExit`. La matriz única de 1 a 5 no permite calificar por criterio ni reproduce los enunciados del instrumento.

## 3. Modelo vigente

El modelo vigente está en `salidas/documentos/anexos_fany/`, hoy vacío porque el certificado aún no se ha generado. El generador es `scripts/compiladores/generar_anexo2_validacion_fany.py` y solo escribe el DOCX con el argumento explícito `--generar`.

## 4. Consecuencia de DEC-020

Existe un único certificado de validez de contenido: el del Instrumento N.° 03 en su Modalidad A de 8 ítems, con criterios dicotómicos de Pertinencia, Relevancia y Claridad. El esquema de seis certificados con sufijo VD y VI no rige, y los Instrumentos N.° 01 y N.° 02 no se someten a juicio de contenido.

## 5. Instrucción operativa

Los tres archivos no deben imprimirse, circularse ni presentarse a ningún juez, con ningún propósito. Nada de esta carpeta debe devolverse a la raíz de `anexos_jhon/`.
