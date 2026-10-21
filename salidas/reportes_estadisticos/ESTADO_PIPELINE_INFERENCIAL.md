# ESTADO DEL PIPELINE ESTADÍSTICO INFERENCIAL (`salidas/reportes_estadisticos/`)

- **Estado Actual:** `BLOQUEADO: esperando datos de campo` (Código de salida `3`).
- **Fundamento Normativo:** Regla Canónica 01 (`01_seguridad.md`) y especificación de `scripts/estadistica/manifest_datos.py` / `scripts/estadistica/pipeline_inferencial.py`.
- **Requisito de Desbloqueo:** El pipeline estadístico solo ejecuta cálculos descriptivos, prueba de normalidad de Shapiro-Wilk sobre diferencias pareadas ($\Delta_i = X_{\text{post}} - X_{\text{pre}}$) y contrastes inferenciales ($t$ de Student pareada o Rangos con Signo de Wilcoxon con $N = n = 14$) cuando existen en `datos/raw/`:
  1. `pretest_sivac.csv` y `postest_sivac.csv` con suma SHA-256 verificada y 14 sujetos (`TRAB-01` a `TRAB-14`).
  2. `datos/raw/MANIFEST.json` firmado por el tesista con la declaración literal: *"Declaro que estos datos provienen de mediciones reales de campo y no han sido simulados."*
