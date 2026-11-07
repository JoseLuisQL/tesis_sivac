# Histórico de tablas de anexos (libros v2 a v5)

Resguardo de la cadena anterior de libros de tablas de anexos, retirada de
`salidas/estadistica/` el 2026-11-07 para que esa carpeta contenga solo el
entregable vigente.

## Qué queda en `salidas/estadistica/`

| Archivo | Origen |
| :--- | :--- |
| `TABLAS_ANEXOS_SIVAC.xlsx` | Libro vigente. Lo genera `scripts/estadistica/exportar_tablas_anexos_excel.py` desde el `informe_final_vNN.docx` de mayor versión, el reporte estadístico y los CSV de campo. |
| `paridad_TABLAS_ANEXOS_SIVAC.json` | Control de paridad de esa misma generación. |
| `reporte_estadistico_completo.json` | Reporte inferencial fuente de las cifras. |
| `AUDITORIA_DATOS.md` / `.json` | Auditoría integral; el bloque K verifica el libro contra el reporte, los CSV y el informe. |

## Qué se guarda aquí

- `TABLAS_ANEXOS_SIVAC_v2.xlsx` a `_v5.xlsx`: libros anteriores, atados a
  `informe_final_v10` y a los informes v16-v19, con 17 hojas y numeración de
  tablas que ya no corresponde al informe vigente.
- `paridad_TABLAS_ANEXOS_SIVAC_v4.json` y `_v5.json`: sus reportes de paridad.
- `REPORTE_EXCEL_ANEXOS_v2.md`: memoria de construcción del libro v2.
- `_dump_*.json`, `_v2_dump.txt`, `_v3_preview.pdf`, `_val_*.pdf` y
  `_validacion_tablas_anexos.pdf`: volcados y previsualizaciones de validación
  usados durante el diseño editorial de esos libros.

## Regla

Nada de esta carpeta se usa para armar el informe. Si hace falta una cifra,
sale del libro vigente, del reporte estadístico o de los CSV de campo; el
bloque K de `verificar_conjunto_datos.py` comprueba esa correspondencia.

Los scripts `build_tablas_anexos_v2.py` y `build_tablas_anexos_v3.py` siguen en
`scripts/estadistica/` como registro histórico y escriben por omisión en esta
carpeta, de modo que reejecutarlos no repone copias junto al libro vigente.
