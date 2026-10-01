# CUARENTENA — SCRIPTS CON DATOS NO EMPÍRICOS (NO EJECUTAR PARA LA TESIS)

Fecha de aislamiento: 2026-09-30

| Script | Problema |
|---|---|
| `crear_datos_campo.py` | Escribe a mano arreglos pretest/postest y genera `bd_sivac_*.csv`. No son datos de campo. |
| `generar_figuras_oficiales_apa7.py` | Define en el código los mismos arreglos "conforme a los descriptivos verificados en Fase 7". |

Pendiente de revisión (NO movidos para no romper el compilador, pero contaminados):
- `scripts/compiladores/capitulo5_builder.py` y `capitulo6_builder.py` contienen cifras de resultados escritas en el texto.

Regla vigente: `.claude/rules/01_seguridad.md` §3 — cero simulación de datos empíricos.
Sin `datos/raw/MANIFEST.json` firmado por el tesista, todo análisis inferencial permanece BLOQUEADO.
