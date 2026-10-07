# Reporte de Auditoria Editorial y Visual OpenXML
- **Documento DOCX:** `PROYECTO_TESIS_ACTUALIZADO_V3_NORMALIZADO.docx`
- **Documento PDF:** `PROYECTO_TESIS_ACTUALIZADO_V3_NORMALIZADO.pdf` (61 paginas)
- **Estado General:** `RECHAZADO`

## Resumen de Metricas Estructurales
| Metrica | Valor |
|---|---|
| Total Parrafos | 610 |
| Total Tablas | 12 |
| Total Celdas | 553 |
| Formulas OMML en Celdas | 30 |
| Listas Detectadas | 60 |
| Quiebres Manuales (w:br) | 1 |
| Defectos Criticos | 1 |
| Defectos Altos | 8 |
| Defectos Medios | 727 |
| Defectos Bajos | 0 |

## Hallazgos y Defectos Detectados
| # | Categoria | Severidad | Ubicacion | Codigo | Descripcion |
|---|---|---|---|---|---|
| 1 | SALTO_PAGINA | **ALTA** | Parrafo [64] | `FALTA_SALTO_PAGINA_OBLIGATORIO` | Seccion Preliminar "Lista de tablas..." no inicia en pagina nueva. |
| 2 | SALTO_PAGINA | **ALTA** | Parrafo [77] | `FALTA_SALTO_PAGINA_OBLIGATORIO` | Seccion Preliminar "Lista de figuras..." no inicia en pagina nueva. |
| 3 | RIO_TIPOGRAFICO | **CRITICA** | Parrafo [385], Fragmento 1 | `RIO_TIPOGRAFICO_BR_JUSTIFICADO` | Quiebre manual <w:br/> en parrafo justificado con linea corta (7 caracteres). |
| 4 | RENDER_VISUAL | **MEDIA** | Pagina PDF 1, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (61.4 pt < 75.0 pt). |
| 5 | RENDER_VISUAL | **MEDIA** | Pagina PDF 2, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 6 | RENDER_VISUAL | **MEDIA** | Pagina PDF 2, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 7 | RENDER_VISUAL | **MEDIA** | Pagina PDF 2, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 8 | RENDER_VISUAL | **MEDIA** | Pagina PDF 2, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 9 | RENDER_VISUAL | **MEDIA** | Pagina PDF 2, Bloque 35 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (589.8 pt > 535.0 pt). |
| 10 | RENDER_VISUAL | **MEDIA** | Pagina PDF 3, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 11 | RENDER_VISUAL | **MEDIA** | Pagina PDF 3, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 12 | RENDER_VISUAL | **MEDIA** | Pagina PDF 3, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 13 | RENDER_VISUAL | **MEDIA** | Pagina PDF 5, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 14 | RENDER_VISUAL | **MEDIA** | Pagina PDF 5, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 15 | RENDER_VISUAL | **MEDIA** | Pagina PDF 6, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 16 | RENDER_VISUAL | **MEDIA** | Pagina PDF 6, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 17 | RENDER_VISUAL | **MEDIA** | Pagina PDF 6, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 18 | RENDER_VISUAL | **MEDIA** | Pagina PDF 6, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 19 | RENDER_VISUAL | **MEDIA** | Pagina PDF 7, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 20 | RENDER_VISUAL | **MEDIA** | Pagina PDF 7, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 21 | RENDER_VISUAL | **MEDIA** | Pagina PDF 7, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 22 | RENDER_VISUAL | **MEDIA** | Pagina PDF 7, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 23 | RENDER_VISUAL | **MEDIA** | Pagina PDF 7, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 24 | RENDER_VISUAL | **MEDIA** | Pagina PDF 7, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 25 | RENDER_VISUAL | **MEDIA** | Pagina PDF 7, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 26 | RENDER_VISUAL | **MEDIA** | Pagina PDF 7, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 27 | RENDER_VISUAL | **MEDIA** | Pagina PDF 7, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 28 | RENDER_VISUAL | **MEDIA** | Pagina PDF 7, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 29 | RENDER_VISUAL | **MEDIA** | Pagina PDF 7, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 30 | RENDER_VISUAL | **MEDIA** | Pagina PDF 7, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 31 | RENDER_VISUAL | **MEDIA** | Pagina PDF 7, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 32 | RENDER_VISUAL | **ALTA** | Pagina PDF 8 | `PAGINA_HUERFANA_CASI_BLANCO` | Pagina 8 es casi blanca (densidad tinta: 0.00%, palabras: 0). |
| 33 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 34 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 35 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 36 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 37 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 38 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 39 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 40 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 41 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 42 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 43 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 44 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 45 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 46 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 47 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 48 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 49 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 50 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 51 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 52 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 53 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 54 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 30 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 55 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 32 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 56 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 33 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 57 | RENDER_VISUAL | **MEDIA** | Pagina PDF 9, Bloque 34 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 58 | RENDER_VISUAL | **MEDIA** | Pagina PDF 10, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 59 | RENDER_VISUAL | **MEDIA** | Pagina PDF 10, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 60 | RENDER_VISUAL | **MEDIA** | Pagina PDF 10, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 61 | RENDER_VISUAL | **MEDIA** | Pagina PDF 10, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 62 | RENDER_VISUAL | **MEDIA** | Pagina PDF 10, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 63 | RENDER_VISUAL | **MEDIA** | Pagina PDF 10, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 64 | RENDER_VISUAL | **MEDIA** | Pagina PDF 10, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 65 | RENDER_VISUAL | **MEDIA** | Pagina PDF 10, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 66 | RENDER_VISUAL | **MEDIA** | Pagina PDF 10, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 67 | RENDER_VISUAL | **MEDIA** | Pagina PDF 10, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 68 | RENDER_VISUAL | **MEDIA** | Pagina PDF 10, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 69 | RENDER_VISUAL | **MEDIA** | Pagina PDF 10, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 70 | RENDER_VISUAL | **MEDIA** | Pagina PDF 10, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 71 | RENDER_VISUAL | **MEDIA** | Pagina PDF 10, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 72 | RENDER_VISUAL | **MEDIA** | Pagina PDF 10, Bloque 32 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (590.3 pt > 535.0 pt). |
| 73 | RENDER_VISUAL | **MEDIA** | Pagina PDF 11, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 74 | RENDER_VISUAL | **MEDIA** | Pagina PDF 11, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 75 | RENDER_VISUAL | **MEDIA** | Pagina PDF 11, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 76 | RENDER_VISUAL | **MEDIA** | Pagina PDF 11, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 77 | RENDER_VISUAL | **MEDIA** | Pagina PDF 11, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 78 | RENDER_VISUAL | **MEDIA** | Pagina PDF 11, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 79 | RENDER_VISUAL | **MEDIA** | Pagina PDF 11, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 80 | RENDER_VISUAL | **MEDIA** | Pagina PDF 11, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 81 | RENDER_VISUAL | **MEDIA** | Pagina PDF 11, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 82 | RENDER_VISUAL | **MEDIA** | Pagina PDF 11, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 83 | RENDER_VISUAL | **MEDIA** | Pagina PDF 11, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 84 | RENDER_VISUAL | **MEDIA** | Pagina PDF 11, Bloque 30 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 85 | RENDER_VISUAL | **MEDIA** | Pagina PDF 11, Bloque 31 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 86 | RENDER_VISUAL | **MEDIA** | Pagina PDF 11, Bloque 32 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 87 | RENDER_VISUAL | **MEDIA** | Pagina PDF 11, Bloque 33 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (589.2 pt > 535.0 pt). |
| 88 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 89 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 90 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 91 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 92 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 93 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 94 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 95 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 96 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 97 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 98 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 99 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 100 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 101 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 102 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 103 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 104 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 105 | RENDER_VISUAL | **MEDIA** | Pagina PDF 12, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 106 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 107 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 108 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 109 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 110 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 111 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 112 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 113 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 114 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 115 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 116 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 117 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 118 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 119 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 120 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 121 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 122 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 123 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 124 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 125 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 126 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 127 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 128 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 30 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 129 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 32 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 130 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 33 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 131 | RENDER_VISUAL | **MEDIA** | Pagina PDF 13, Bloque 34 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (585.5 pt > 535.0 pt). |
| 132 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 133 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 134 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 135 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 136 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 137 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 138 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 139 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 140 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 141 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 142 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 143 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 144 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 145 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 146 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 147 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 148 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 149 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 150 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 151 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 152 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 153 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 154 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 155 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 31 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 156 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 32 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 157 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 33 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 158 | RENDER_VISUAL | **MEDIA** | Pagina PDF 14, Bloque 34 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 159 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 160 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 161 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 162 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 163 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 164 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 165 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 166 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 167 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 168 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 169 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 170 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 171 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 172 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 173 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 174 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 175 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 176 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 177 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 178 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 179 | RENDER_VISUAL | **MEDIA** | Pagina PDF 15, Bloque 30 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (591.2 pt > 535.0 pt). |
| 180 | RENDER_VISUAL | **MEDIA** | Pagina PDF 16, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 181 | RENDER_VISUAL | **MEDIA** | Pagina PDF 16, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 182 | RENDER_VISUAL | **MEDIA** | Pagina PDF 16, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 183 | RENDER_VISUAL | **MEDIA** | Pagina PDF 16, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 184 | RENDER_VISUAL | **MEDIA** | Pagina PDF 16, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 185 | RENDER_VISUAL | **MEDIA** | Pagina PDF 16, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 186 | RENDER_VISUAL | **MEDIA** | Pagina PDF 16, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 187 | RENDER_VISUAL | **MEDIA** | Pagina PDF 16, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 188 | RENDER_VISUAL | **MEDIA** | Pagina PDF 16, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 189 | RENDER_VISUAL | **MEDIA** | Pagina PDF 16, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 190 | RENDER_VISUAL | **MEDIA** | Pagina PDF 16, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 191 | RENDER_VISUAL | **MEDIA** | Pagina PDF 16, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 192 | RENDER_VISUAL | **MEDIA** | Pagina PDF 16, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 193 | RENDER_VISUAL | **MEDIA** | Pagina PDF 16, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 194 | RENDER_VISUAL | **MEDIA** | Pagina PDF 16, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 195 | RENDER_VISUAL | **MEDIA** | Pagina PDF 17, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 196 | RENDER_VISUAL | **MEDIA** | Pagina PDF 17, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 197 | RENDER_VISUAL | **MEDIA** | Pagina PDF 17, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 198 | RENDER_VISUAL | **MEDIA** | Pagina PDF 17, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 199 | RENDER_VISUAL | **MEDIA** | Pagina PDF 17, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 200 | RENDER_VISUAL | **MEDIA** | Pagina PDF 17, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 201 | RENDER_VISUAL | **MEDIA** | Pagina PDF 17, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 202 | RENDER_VISUAL | **MEDIA** | Pagina PDF 17, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 203 | RENDER_VISUAL | **MEDIA** | Pagina PDF 17, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 204 | RENDER_VISUAL | **MEDIA** | Pagina PDF 17, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 205 | RENDER_VISUAL | **MEDIA** | Pagina PDF 17, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 206 | RENDER_VISUAL | **MEDIA** | Pagina PDF 17, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 207 | RENDER_VISUAL | **MEDIA** | Pagina PDF 17, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 208 | RENDER_VISUAL | **MEDIA** | Pagina PDF 17, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 209 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 210 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 211 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 212 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 213 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 214 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 215 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 216 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 217 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 218 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 219 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 220 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 221 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 222 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 223 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 224 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 225 | RENDER_VISUAL | **MEDIA** | Pagina PDF 18, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 226 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 227 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 228 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 229 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 230 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 231 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 232 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 233 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 234 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 235 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 236 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 237 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 238 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 239 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 240 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 241 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 242 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 243 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 244 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 31 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 245 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 32 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 246 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 34 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 247 | RENDER_VISUAL | **MEDIA** | Pagina PDF 19, Bloque 35 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 248 | RENDER_VISUAL | **MEDIA** | Pagina PDF 20, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 249 | RENDER_VISUAL | **MEDIA** | Pagina PDF 20, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 250 | RENDER_VISUAL | **MEDIA** | Pagina PDF 20, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 251 | RENDER_VISUAL | **MEDIA** | Pagina PDF 20, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 252 | RENDER_VISUAL | **MEDIA** | Pagina PDF 20, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 253 | RENDER_VISUAL | **MEDIA** | Pagina PDF 20, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 254 | RENDER_VISUAL | **MEDIA** | Pagina PDF 20, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 255 | RENDER_VISUAL | **MEDIA** | Pagina PDF 20, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 256 | RENDER_VISUAL | **MEDIA** | Pagina PDF 20, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 257 | RENDER_VISUAL | **MEDIA** | Pagina PDF 20, Bloque 30 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 258 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 259 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 260 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 261 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 262 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 263 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 264 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 265 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 266 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 267 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 268 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 269 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 270 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 271 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 272 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 273 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 274 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 275 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 276 | RENDER_VISUAL | **MEDIA** | Pagina PDF 21, Bloque 31 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 277 | RENDER_VISUAL | **MEDIA** | Pagina PDF 22, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 278 | RENDER_VISUAL | **MEDIA** | Pagina PDF 22, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 279 | RENDER_VISUAL | **MEDIA** | Pagina PDF 22, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 280 | RENDER_VISUAL | **MEDIA** | Pagina PDF 22, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 281 | RENDER_VISUAL | **MEDIA** | Pagina PDF 22, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 282 | RENDER_VISUAL | **MEDIA** | Pagina PDF 22, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 283 | RENDER_VISUAL | **MEDIA** | Pagina PDF 22, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 284 | RENDER_VISUAL | **MEDIA** | Pagina PDF 22, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 285 | RENDER_VISUAL | **MEDIA** | Pagina PDF 22, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 286 | RENDER_VISUAL | **MEDIA** | Pagina PDF 22, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 287 | RENDER_VISUAL | **MEDIA** | Pagina PDF 22, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 288 | RENDER_VISUAL | **MEDIA** | Pagina PDF 22, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 289 | RENDER_VISUAL | **MEDIA** | Pagina PDF 22, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 290 | RENDER_VISUAL | **MEDIA** | Pagina PDF 23, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 291 | RENDER_VISUAL | **MEDIA** | Pagina PDF 23, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 292 | RENDER_VISUAL | **MEDIA** | Pagina PDF 23, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 293 | RENDER_VISUAL | **MEDIA** | Pagina PDF 23, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 294 | RENDER_VISUAL | **MEDIA** | Pagina PDF 23, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 295 | RENDER_VISUAL | **MEDIA** | Pagina PDF 23, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 296 | RENDER_VISUAL | **MEDIA** | Pagina PDF 23, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 297 | RENDER_VISUAL | **MEDIA** | Pagina PDF 23, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 298 | RENDER_VISUAL | **MEDIA** | Pagina PDF 23, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 299 | RENDER_VISUAL | **MEDIA** | Pagina PDF 23, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 300 | RENDER_VISUAL | **MEDIA** | Pagina PDF 23, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 301 | RENDER_VISUAL | **MEDIA** | Pagina PDF 23, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 302 | RENDER_VISUAL | **MEDIA** | Pagina PDF 23, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 303 | RENDER_VISUAL | **MEDIA** | Pagina PDF 24, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 304 | RENDER_VISUAL | **MEDIA** | Pagina PDF 24, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 305 | RENDER_VISUAL | **MEDIA** | Pagina PDF 24, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 306 | RENDER_VISUAL | **MEDIA** | Pagina PDF 24, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 307 | RENDER_VISUAL | **MEDIA** | Pagina PDF 24, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 308 | RENDER_VISUAL | **MEDIA** | Pagina PDF 24, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 309 | RENDER_VISUAL | **MEDIA** | Pagina PDF 24, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 310 | RENDER_VISUAL | **MEDIA** | Pagina PDF 24, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 311 | RENDER_VISUAL | **MEDIA** | Pagina PDF 24, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 312 | RENDER_VISUAL | **MEDIA** | Pagina PDF 24, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 313 | RENDER_VISUAL | **MEDIA** | Pagina PDF 24, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 314 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 315 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 316 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 317 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 318 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 319 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 320 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 321 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 322 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 323 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 324 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 325 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 326 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 327 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 328 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 329 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 330 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 331 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 332 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 333 | RENDER_VISUAL | **MEDIA** | Pagina PDF 25, Bloque 31 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 334 | RENDER_VISUAL | **MEDIA** | Pagina PDF 26, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 335 | RENDER_VISUAL | **MEDIA** | Pagina PDF 26, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 336 | RENDER_VISUAL | **MEDIA** | Pagina PDF 26, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 337 | RENDER_VISUAL | **MEDIA** | Pagina PDF 26, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 338 | RENDER_VISUAL | **MEDIA** | Pagina PDF 26, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 339 | RENDER_VISUAL | **MEDIA** | Pagina PDF 26, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 340 | RENDER_VISUAL | **MEDIA** | Pagina PDF 26, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 341 | RENDER_VISUAL | **MEDIA** | Pagina PDF 26, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 342 | RENDER_VISUAL | **MEDIA** | Pagina PDF 26, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 343 | RENDER_VISUAL | **MEDIA** | Pagina PDF 26, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 344 | RENDER_VISUAL | **MEDIA** | Pagina PDF 26, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 345 | RENDER_VISUAL | **MEDIA** | Pagina PDF 26, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 346 | RENDER_VISUAL | **MEDIA** | Pagina PDF 26, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 347 | RENDER_VISUAL | **MEDIA** | Pagina PDF 27, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 348 | RENDER_VISUAL | **MEDIA** | Pagina PDF 27, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 349 | RENDER_VISUAL | **MEDIA** | Pagina PDF 27, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 350 | RENDER_VISUAL | **MEDIA** | Pagina PDF 27, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 351 | RENDER_VISUAL | **MEDIA** | Pagina PDF 27, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 352 | RENDER_VISUAL | **MEDIA** | Pagina PDF 27, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 353 | RENDER_VISUAL | **MEDIA** | Pagina PDF 27, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 354 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 355 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 356 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 357 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 358 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 359 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 360 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 361 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 362 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 363 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 364 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 365 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 31 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 366 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 32 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 367 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 35 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 368 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 36 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 369 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 37 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 370 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 39 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 371 | RENDER_VISUAL | **MEDIA** | Pagina PDF 28, Bloque 40 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 372 | RENDER_VISUAL | **MEDIA** | Pagina PDF 29, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 373 | RENDER_VISUAL | **MEDIA** | Pagina PDF 29, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 374 | RENDER_VISUAL | **MEDIA** | Pagina PDF 29, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 375 | RENDER_VISUAL | **MEDIA** | Pagina PDF 29, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 376 | RENDER_VISUAL | **MEDIA** | Pagina PDF 29, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 377 | RENDER_VISUAL | **MEDIA** | Pagina PDF 29, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 378 | RENDER_VISUAL | **MEDIA** | Pagina PDF 29, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 379 | RENDER_VISUAL | **MEDIA** | Pagina PDF 29, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 380 | RENDER_VISUAL | **MEDIA** | Pagina PDF 29, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 381 | RENDER_VISUAL | **MEDIA** | Pagina PDF 29, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 382 | RENDER_VISUAL | **MEDIA** | Pagina PDF 29, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 383 | RENDER_VISUAL | **MEDIA** | Pagina PDF 29, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 384 | RENDER_VISUAL | **MEDIA** | Pagina PDF 29, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 385 | RENDER_VISUAL | **MEDIA** | Pagina PDF 29, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 386 | RENDER_VISUAL | **MEDIA** | Pagina PDF 29, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 387 | RENDER_VISUAL | **MEDIA** | Pagina PDF 29, Bloque 30 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 388 | RENDER_VISUAL | **MEDIA** | Pagina PDF 30, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 389 | RENDER_VISUAL | **MEDIA** | Pagina PDF 30, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 390 | RENDER_VISUAL | **MEDIA** | Pagina PDF 30, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 391 | RENDER_VISUAL | **MEDIA** | Pagina PDF 30, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 392 | RENDER_VISUAL | **MEDIA** | Pagina PDF 30, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 393 | RENDER_VISUAL | **MEDIA** | Pagina PDF 30, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 394 | RENDER_VISUAL | **MEDIA** | Pagina PDF 30, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 395 | RENDER_VISUAL | **MEDIA** | Pagina PDF 30, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 396 | RENDER_VISUAL | **MEDIA** | Pagina PDF 30, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 397 | RENDER_VISUAL | **MEDIA** | Pagina PDF 30, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 398 | RENDER_VISUAL | **MEDIA** | Pagina PDF 30, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 399 | RENDER_VISUAL | **MEDIA** | Pagina PDF 30, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 400 | RENDER_VISUAL | **MEDIA** | Pagina PDF 30, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 401 | RENDER_VISUAL | **MEDIA** | Pagina PDF 31, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 402 | RENDER_VISUAL | **MEDIA** | Pagina PDF 31, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 403 | RENDER_VISUAL | **MEDIA** | Pagina PDF 31, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 404 | RENDER_VISUAL | **MEDIA** | Pagina PDF 31, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 405 | RENDER_VISUAL | **MEDIA** | Pagina PDF 31, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 406 | RENDER_VISUAL | **MEDIA** | Pagina PDF 31, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 407 | RENDER_VISUAL | **MEDIA** | Pagina PDF 31, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 408 | RENDER_VISUAL | **MEDIA** | Pagina PDF 31, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 409 | RENDER_VISUAL | **MEDIA** | Pagina PDF 31, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 410 | RENDER_VISUAL | **MEDIA** | Pagina PDF 31, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 411 | RENDER_VISUAL | **MEDIA** | Pagina PDF 31, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 412 | RENDER_VISUAL | **MEDIA** | Pagina PDF 31, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 413 | RENDER_VISUAL | **MEDIA** | Pagina PDF 31, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 414 | RENDER_VISUAL | **MEDIA** | Pagina PDF 31, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 415 | RENDER_VISUAL | **MEDIA** | Pagina PDF 31, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 416 | RENDER_VISUAL | **MEDIA** | Pagina PDF 32, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 417 | RENDER_VISUAL | **MEDIA** | Pagina PDF 32, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 418 | RENDER_VISUAL | **MEDIA** | Pagina PDF 32, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 419 | RENDER_VISUAL | **MEDIA** | Pagina PDF 32, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 420 | RENDER_VISUAL | **MEDIA** | Pagina PDF 33, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 421 | RENDER_VISUAL | **MEDIA** | Pagina PDF 33, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 422 | RENDER_VISUAL | **MEDIA** | Pagina PDF 33, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 423 | RENDER_VISUAL | **MEDIA** | Pagina PDF 33, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 424 | RENDER_VISUAL | **MEDIA** | Pagina PDF 33, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 425 | RENDER_VISUAL | **MEDIA** | Pagina PDF 33, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 426 | RENDER_VISUAL | **MEDIA** | Pagina PDF 33, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 427 | RENDER_VISUAL | **MEDIA** | Pagina PDF 33, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 428 | RENDER_VISUAL | **MEDIA** | Pagina PDF 33, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 429 | RENDER_VISUAL | **MEDIA** | Pagina PDF 33, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 430 | RENDER_VISUAL | **MEDIA** | Pagina PDF 33, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 431 | RENDER_VISUAL | **MEDIA** | Pagina PDF 33, Bloque 31 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (591.1 pt > 535.0 pt). |
| 432 | RENDER_VISUAL | **MEDIA** | Pagina PDF 33, Bloque 32 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (590.8 pt > 535.0 pt). |
| 433 | RENDER_VISUAL | **MEDIA** | Pagina PDF 33, Bloque 33 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (591.2 pt > 535.0 pt). |
| 434 | RENDER_VISUAL | **MEDIA** | Pagina PDF 34, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 435 | RENDER_VISUAL | **MEDIA** | Pagina PDF 34, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 436 | RENDER_VISUAL | **MEDIA** | Pagina PDF 34, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 437 | RENDER_VISUAL | **MEDIA** | Pagina PDF 34, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 438 | RENDER_VISUAL | **MEDIA** | Pagina PDF 34, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 439 | RENDER_VISUAL | **MEDIA** | Pagina PDF 34, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 440 | RENDER_VISUAL | **MEDIA** | Pagina PDF 34, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 441 | RENDER_VISUAL | **MEDIA** | Pagina PDF 34, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 442 | RENDER_VISUAL | **MEDIA** | Pagina PDF 34, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 443 | RENDER_VISUAL | **MEDIA** | Pagina PDF 35, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 444 | RENDER_VISUAL | **MEDIA** | Pagina PDF 35, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 445 | RENDER_VISUAL | **MEDIA** | Pagina PDF 35, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (66.4 pt < 75.0 pt). |
| 446 | RENDER_VISUAL | **MEDIA** | Pagina PDF 35, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (67.7 pt < 75.0 pt). |
| 447 | RENDER_VISUAL | **MEDIA** | Pagina PDF 35, Bloque 65 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 448 | RENDER_VISUAL | **ALTA** | Pagina PDF 35 | `COLISION_BLOQUES_VISUALES` | Colision y solapamiento visual directo detectado entre bloques de texto en PDF. |
| 449 | RENDER_VISUAL | **ALTA** | Pagina PDF 36 | `PAGINA_HUERFANA_CASI_BLANCO` | Pagina 36 es casi blanca (densidad tinta: 0.00%, palabras: 0). |
| 450 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 451 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 452 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 453 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 454 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 455 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 456 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 457 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 458 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 459 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 460 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 461 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 462 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 463 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 464 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 465 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 466 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 467 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 468 | RENDER_VISUAL | **MEDIA** | Pagina PDF 37, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 469 | RENDER_VISUAL | **MEDIA** | Pagina PDF 38, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 470 | RENDER_VISUAL | **MEDIA** | Pagina PDF 38, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 471 | RENDER_VISUAL | **MEDIA** | Pagina PDF 38, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 472 | RENDER_VISUAL | **MEDIA** | Pagina PDF 38, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 473 | RENDER_VISUAL | **MEDIA** | Pagina PDF 38, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 474 | RENDER_VISUAL | **MEDIA** | Pagina PDF 38, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 475 | RENDER_VISUAL | **MEDIA** | Pagina PDF 38, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 476 | RENDER_VISUAL | **MEDIA** | Pagina PDF 38, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 477 | RENDER_VISUAL | **MEDIA** | Pagina PDF 38, Bloque 30 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 478 | RENDER_VISUAL | **MEDIA** | Pagina PDF 38, Bloque 32 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 479 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 480 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 481 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 482 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 483 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 484 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 485 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 486 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 487 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 488 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 489 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 490 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 491 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 492 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 493 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 494 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 495 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 496 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 497 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 498 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 499 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 500 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 30 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 501 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 31 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 502 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 32 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 503 | RENDER_VISUAL | **MEDIA** | Pagina PDF 39, Bloque 33 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 504 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 505 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 506 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 507 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 508 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 509 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 510 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 511 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 512 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 513 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 514 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 31 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 515 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 32 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 516 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 33 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 517 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 34 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 518 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 35 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 519 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 36 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 520 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 37 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 521 | RENDER_VISUAL | **MEDIA** | Pagina PDF 40, Bloque 38 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 522 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 523 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 524 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 525 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 526 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 527 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 528 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 529 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 530 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 531 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 532 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 533 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 534 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 535 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 536 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 537 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 538 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 539 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 540 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 541 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 542 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 543 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 544 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 30 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 545 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 31 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 546 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 32 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 547 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 33 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 548 | RENDER_VISUAL | **MEDIA** | Pagina PDF 41, Bloque 34 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 549 | RENDER_VISUAL | **MEDIA** | Pagina PDF 42, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 550 | RENDER_VISUAL | **MEDIA** | Pagina PDF 42, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 551 | RENDER_VISUAL | **MEDIA** | Pagina PDF 42, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 552 | RENDER_VISUAL | **MEDIA** | Pagina PDF 42, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 553 | RENDER_VISUAL | **MEDIA** | Pagina PDF 43, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 554 | RENDER_VISUAL | **MEDIA** | Pagina PDF 43, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 555 | RENDER_VISUAL | **MEDIA** | Pagina PDF 43, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 556 | RENDER_VISUAL | **MEDIA** | Pagina PDF 43, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 557 | RENDER_VISUAL | **MEDIA** | Pagina PDF 43, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 558 | RENDER_VISUAL | **MEDIA** | Pagina PDF 43, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 559 | RENDER_VISUAL | **MEDIA** | Pagina PDF 43, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 560 | RENDER_VISUAL | **MEDIA** | Pagina PDF 44, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 561 | RENDER_VISUAL | **MEDIA** | Pagina PDF 44, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 562 | RENDER_VISUAL | **MEDIA** | Pagina PDF 44, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 563 | RENDER_VISUAL | **MEDIA** | Pagina PDF 44, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 564 | RENDER_VISUAL | **MEDIA** | Pagina PDF 44, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 565 | RENDER_VISUAL | **MEDIA** | Pagina PDF 45, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 566 | RENDER_VISUAL | **MEDIA** | Pagina PDF 45, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 567 | RENDER_VISUAL | **MEDIA** | Pagina PDF 45, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (66.4 pt < 75.0 pt). |
| 568 | RENDER_VISUAL | **MEDIA** | Pagina PDF 45, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (66.4 pt < 75.0 pt). |
| 569 | RENDER_VISUAL | **MEDIA** | Pagina PDF 45, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (66.4 pt < 75.0 pt). |
| 570 | RENDER_VISUAL | **MEDIA** | Pagina PDF 45, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 571 | RENDER_VISUAL | **MEDIA** | Pagina PDF 45, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 572 | RENDER_VISUAL | **MEDIA** | Pagina PDF 45, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 573 | RENDER_VISUAL | **MEDIA** | Pagina PDF 45, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 574 | RENDER_VISUAL | **MEDIA** | Pagina PDF 45, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 575 | RENDER_VISUAL | **MEDIA** | Pagina PDF 45, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 576 | RENDER_VISUAL | **MEDIA** | Pagina PDF 45, Bloque 30 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (591.0 pt > 535.0 pt). |
| 577 | RENDER_VISUAL | **ALTA** | Pagina PDF 45 | `COLISION_BLOQUES_VISUALES` | Colision y solapamiento visual directo detectado entre bloques de texto en PDF. |
| 578 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 579 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 580 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 581 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 582 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 583 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 584 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 585 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 586 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 587 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 588 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 589 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 590 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 591 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 592 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 30 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 593 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 31 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 594 | RENDER_VISUAL | **MEDIA** | Pagina PDF 46, Bloque 32 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 595 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 596 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 597 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 598 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 599 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 600 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 601 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 602 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 603 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 604 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 605 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 606 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 607 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 608 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 609 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 610 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 611 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 31 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 612 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 32 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 613 | RENDER_VISUAL | **MEDIA** | Pagina PDF 47, Bloque 33 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 614 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 615 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 616 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 617 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 618 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 619 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 620 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 621 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 622 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 623 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 624 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.2 pt < 75.0 pt). |
| 625 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 626 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 627 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 628 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 629 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 630 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 631 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 30 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 632 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 31 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 633 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 32 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 634 | RENDER_VISUAL | **MEDIA** | Pagina PDF 48, Bloque 33 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 635 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 636 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 637 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 638 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 639 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 640 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 13 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 641 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 642 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 643 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 644 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 645 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 646 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 647 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 648 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 649 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 650 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 651 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 27 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 652 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 653 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 30 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 654 | RENDER_VISUAL | **MEDIA** | Pagina PDF 49, Bloque 32 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 655 | RENDER_VISUAL | **MEDIA** | Pagina PDF 50, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 656 | RENDER_VISUAL | **MEDIA** | Pagina PDF 50, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 657 | RENDER_VISUAL | **MEDIA** | Pagina PDF 50, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 658 | RENDER_VISUAL | **MEDIA** | Pagina PDF 50, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 659 | RENDER_VISUAL | **MEDIA** | Pagina PDF 50, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 660 | RENDER_VISUAL | **ALTA** | Pagina PDF 51 | `PAGINA_HUERFANA_CASI_BLANCO` | Pagina 51 es casi blanca (densidad tinta: 0.15%, palabras: 14). |
| 661 | RENDER_VISUAL | **MEDIA** | Pagina PDF 52, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (57.5 pt < 75.0 pt). |
| 662 | RENDER_VISUAL | **MEDIA** | Pagina PDF 52, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (63.7 pt < 75.0 pt). |
| 663 | RENDER_VISUAL | **MEDIA** | Pagina PDF 52, Bloque 10 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (609.9 pt > 535.0 pt). |
| 664 | RENDER_VISUAL | **MEDIA** | Pagina PDF 52, Bloque 11 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (620.1 pt > 535.0 pt). |
| 665 | RENDER_VISUAL | **MEDIA** | Pagina PDF 52, Bloque 46 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (579.7 pt > 535.0 pt). |
| 666 | RENDER_VISUAL | **MEDIA** | Pagina PDF 53, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 667 | RENDER_VISUAL | **MEDIA** | Pagina PDF 53, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.4 pt < 75.0 pt). |
| 668 | RENDER_VISUAL | **MEDIA** | Pagina PDF 53, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.4 pt < 75.0 pt). |
| 669 | RENDER_VISUAL | **MEDIA** | Pagina PDF 53, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.4 pt < 75.0 pt). |
| 670 | RENDER_VISUAL | **MEDIA** | Pagina PDF 53, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.4 pt < 75.0 pt). |
| 671 | RENDER_VISUAL | **MEDIA** | Pagina PDF 53, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.4 pt < 75.0 pt). |
| 672 | RENDER_VISUAL | **MEDIA** | Pagina PDF 53, Bloque 17 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.4 pt < 75.0 pt). |
| 673 | RENDER_VISUAL | **MEDIA** | Pagina PDF 53, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.4 pt < 75.0 pt). |
| 674 | RENDER_VISUAL | **MEDIA** | Pagina PDF 53, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.4 pt < 75.0 pt). |
| 675 | RENDER_VISUAL | **MEDIA** | Pagina PDF 53, Bloque 21 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.4 pt < 75.0 pt). |
| 676 | RENDER_VISUAL | **MEDIA** | Pagina PDF 53, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.4 pt < 75.0 pt). |
| 677 | RENDER_VISUAL | **MEDIA** | Pagina PDF 53, Bloque 30 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.4 pt < 75.0 pt). |
| 678 | RENDER_VISUAL | **MEDIA** | Pagina PDF 53, Bloque 31 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.4 pt < 75.0 pt). |
| 679 | RENDER_VISUAL | **MEDIA** | Pagina PDF 53, Bloque 32 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (68.4 pt < 75.0 pt). |
| 680 | RENDER_VISUAL | **MEDIA** | Pagina PDF 54, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 681 | RENDER_VISUAL | **MEDIA** | Pagina PDF 54, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 682 | RENDER_VISUAL | **MEDIA** | Pagina PDF 54, Bloque 11 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 683 | RENDER_VISUAL | **MEDIA** | Pagina PDF 54, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 684 | RENDER_VISUAL | **MEDIA** | Pagina PDF 54, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 685 | RENDER_VISUAL | **MEDIA** | Pagina PDF 54, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 686 | RENDER_VISUAL | **MEDIA** | Pagina PDF 54, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 687 | RENDER_VISUAL | **MEDIA** | Pagina PDF 54, Bloque 28 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 688 | RENDER_VISUAL | **MEDIA** | Pagina PDF 55, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 689 | RENDER_VISUAL | **MEDIA** | Pagina PDF 55, Bloque 8 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 690 | RENDER_VISUAL | **MEDIA** | Pagina PDF 55, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 691 | RENDER_VISUAL | **MEDIA** | Pagina PDF 55, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 692 | RENDER_VISUAL | **MEDIA** | Pagina PDF 55, Bloque 19 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 693 | RENDER_VISUAL | **MEDIA** | Pagina PDF 55, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 694 | RENDER_VISUAL | **MEDIA** | Pagina PDF 55, Bloque 26 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 695 | RENDER_VISUAL | **MEDIA** | Pagina PDF 55, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 696 | RENDER_VISUAL | **MEDIA** | Pagina PDF 56, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 697 | RENDER_VISUAL | **MEDIA** | Pagina PDF 56, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 698 | RENDER_VISUAL | **MEDIA** | Pagina PDF 56, Bloque 9 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 699 | RENDER_VISUAL | **MEDIA** | Pagina PDF 56, Bloque 16 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 700 | RENDER_VISUAL | **MEDIA** | Pagina PDF 56, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 701 | RENDER_VISUAL | **MEDIA** | Pagina PDF 56, Bloque 22 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 702 | RENDER_VISUAL | **MEDIA** | Pagina PDF 56, Bloque 25 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 703 | RENDER_VISUAL | **MEDIA** | Pagina PDF 56, Bloque 29 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 704 | RENDER_VISUAL | **MEDIA** | Pagina PDF 57, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 705 | RENDER_VISUAL | **MEDIA** | Pagina PDF 57, Bloque 7 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 706 | RENDER_VISUAL | **MEDIA** | Pagina PDF 57, Bloque 12 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 707 | RENDER_VISUAL | **MEDIA** | Pagina PDF 57, Bloque 15 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 708 | RENDER_VISUAL | **MEDIA** | Pagina PDF 57, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 709 | RENDER_VISUAL | **MEDIA** | Pagina PDF 57, Bloque 20 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 710 | RENDER_VISUAL | **MEDIA** | Pagina PDF 57, Bloque 23 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 711 | RENDER_VISUAL | **MEDIA** | Pagina PDF 57, Bloque 24 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 712 | RENDER_VISUAL | **MEDIA** | Pagina PDF 57, Bloque 30 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 713 | RENDER_VISUAL | **MEDIA** | Pagina PDF 58, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 714 | RENDER_VISUAL | **MEDIA** | Pagina PDF 58, Bloque 10 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 715 | RENDER_VISUAL | **MEDIA** | Pagina PDF 58, Bloque 14 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (64.1 pt < 75.0 pt). |
| 716 | RENDER_VISUAL | **ALTA** | Pagina PDF 59 | `PAGINA_HUERFANA_CASI_BLANCO` | Pagina 59 es casi blanca (densidad tinta: 0.03%, palabras: 1). |
| 717 | RENDER_VISUAL | **MEDIA** | Pagina PDF 60, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (57.5 pt < 75.0 pt). |
| 718 | RENDER_VISUAL | **MEDIA** | Pagina PDF 60, Bloque 5 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (66.8 pt < 75.0 pt). |
| 719 | RENDER_VISUAL | **MEDIA** | Pagina PDF 60, Bloque 5 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (619.9 pt > 535.0 pt). |
| 720 | RENDER_VISUAL | **MEDIA** | Pagina PDF 60, Bloque 6 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (60.0 pt < 75.0 pt). |
| 721 | RENDER_VISUAL | **MEDIA** | Pagina PDF 60, Bloque 14 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (557.5 pt > 535.0 pt). |
| 722 | RENDER_VISUAL | **MEDIA** | Pagina PDF 60, Bloque 15 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (622.2 pt > 535.0 pt). |
| 723 | RENDER_VISUAL | **MEDIA** | Pagina PDF 60, Bloque 16 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (615.5 pt > 535.0 pt). |
| 724 | RENDER_VISUAL | **MEDIA** | Pagina PDF 60, Bloque 17 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (623.5 pt > 535.0 pt). |
| 725 | RENDER_VISUAL | **MEDIA** | Pagina PDF 60, Bloque 18 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (60.0 pt < 75.0 pt). |
| 726 | RENDER_VISUAL | **MEDIA** | Pagina PDF 60, Bloque 24 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (553.2 pt > 535.0 pt). |
| 727 | RENDER_VISUAL | **MEDIA** | Pagina PDF 61, Bloque 4 | `DESBORDE_MARGEN_IZQUIERDO` | Contenido excede el margen izquierdo seguro (66.8 pt < 75.0 pt). |
| 728 | RENDER_VISUAL | **MEDIA** | Pagina PDF 61, Bloque 4 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (619.9 pt > 535.0 pt). |
| 729 | RENDER_VISUAL | **MEDIA** | Pagina PDF 61, Bloque 9 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (544.0 pt > 535.0 pt). |
| 730 | RENDER_VISUAL | **MEDIA** | Pagina PDF 61, Bloque 12 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (553.1 pt > 535.0 pt). |
| 731 | RENDER_VISUAL | **MEDIA** | Pagina PDF 61, Bloque 13 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (548.0 pt > 535.0 pt). |
| 732 | RENDER_VISUAL | **MEDIA** | Pagina PDF 61, Bloque 18 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (557.6 pt > 535.0 pt). |
| 733 | RENDER_VISUAL | **MEDIA** | Pagina PDF 61, Bloque 19 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (622.2 pt > 535.0 pt). |
| 734 | RENDER_VISUAL | **MEDIA** | Pagina PDF 61, Bloque 25 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (551.8 pt > 535.0 pt). |
| 735 | RENDER_VISUAL | **MEDIA** | Pagina PDF 61, Bloque 26 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (548.7 pt > 535.0 pt). |
| 736 | RENDER_VISUAL | **MEDIA** | Pagina PDF 61, Bloque 30 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (555.1 pt > 535.0 pt). |

### Acciones de Mitigacion Recomendadas
- **[1] FALTA_SALTO_PAGINA_OBLIGATORIO (Parrafo [64]):** Inyectar <w:pageBreakBefore/> en w:pPr del parrafo o preceder con salto de pagina formal.
- **[2] FALTA_SALTO_PAGINA_OBLIGATORIO (Parrafo [77]):** Inyectar <w:pageBreakBefore/> en w:pPr del parrafo o preceder con salto de pagina formal.
- **[3] RIO_TIPOGRAFICO_BR_JUSTIFICADO (Parrafo [385], Fragmento 1):** Reemplazar <w:br/> por salto de parrafo formal (<w:p>) o eliminar el quiebre manual.
- **[4] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 1, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[5] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 2, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[6] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 2, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[7] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 2, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[8] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 2, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[9] DESBORDE_MARGEN_DERECHO (Pagina PDF 2, Bloque 35):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[10] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 3, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[11] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 3, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[12] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 3, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[13] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 5, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[14] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 5, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[15] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 6, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[16] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 6, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[17] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 6, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[18] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 6, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[19] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 7, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[20] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 7, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[21] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 7, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[22] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 7, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[23] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 7, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[24] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 7, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[25] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 7, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[26] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 7, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[27] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 7, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[28] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 7, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[29] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 7, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[30] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 7, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[31] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 7, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[32] PAGINA_HUERFANA_CASI_BLANCO (Pagina PDF 8):** Revisar saltos de pagina redundantes o tablas desbordadas que empujan saltos en blanco.
- **[33] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[34] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[35] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[36] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[37] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[38] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[39] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[40] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[41] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[42] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[43] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[44] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[45] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[46] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[47] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[48] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[49] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[50] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[51] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[52] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[53] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[54] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 30):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[55] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 32):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[56] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 33):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[57] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 9, Bloque 34):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[58] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 10, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[59] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 10, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[60] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 10, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[61] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 10, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[62] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 10, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[63] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 10, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[64] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 10, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[65] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 10, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[66] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 10, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[67] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 10, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[68] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 10, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[69] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 10, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[70] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 10, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[71] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 10, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[72] DESBORDE_MARGEN_DERECHO (Pagina PDF 10, Bloque 32):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[73] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 11, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[74] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 11, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[75] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 11, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[76] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 11, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[77] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 11, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[78] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 11, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[79] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 11, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[80] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 11, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[81] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 11, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[82] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 11, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[83] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 11, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[84] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 11, Bloque 30):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[85] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 11, Bloque 31):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[86] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 11, Bloque 32):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[87] DESBORDE_MARGEN_DERECHO (Pagina PDF 11, Bloque 33):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[88] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[89] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[90] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[91] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[92] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[93] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[94] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[95] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[96] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[97] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[98] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[99] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[100] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[101] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[102] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[103] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[104] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[105] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 12, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[106] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[107] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[108] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[109] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[110] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[111] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[112] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[113] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[114] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[115] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[116] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[117] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[118] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[119] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[120] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[121] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[122] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[123] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[124] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[125] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[126] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[127] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[128] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 30):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[129] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 32):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[130] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 13, Bloque 33):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[131] DESBORDE_MARGEN_DERECHO (Pagina PDF 13, Bloque 34):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[132] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[133] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[134] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[135] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[136] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[137] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[138] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[139] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[140] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[141] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[142] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[143] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[144] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[145] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[146] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[147] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[148] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[149] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[150] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[151] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[152] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[153] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[154] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[155] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 31):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[156] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 32):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[157] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 33):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[158] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 14, Bloque 34):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[159] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[160] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[161] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[162] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[163] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[164] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[165] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[166] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[167] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[168] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[169] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[170] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[171] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[172] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[173] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[174] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[175] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[176] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[177] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[178] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 15, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[179] DESBORDE_MARGEN_DERECHO (Pagina PDF 15, Bloque 30):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[180] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 16, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[181] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 16, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[182] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 16, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[183] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 16, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[184] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 16, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[185] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 16, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[186] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 16, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[187] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 16, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[188] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 16, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[189] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 16, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[190] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 16, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[191] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 16, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[192] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 16, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[193] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 16, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[194] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 16, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[195] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 17, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[196] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 17, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[197] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 17, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[198] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 17, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[199] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 17, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[200] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 17, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[201] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 17, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[202] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 17, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[203] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 17, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[204] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 17, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[205] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 17, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[206] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 17, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[207] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 17, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[208] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 17, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[209] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[210] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[211] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[212] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[213] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[214] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[215] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[216] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[217] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[218] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[219] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[220] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[221] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[222] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[223] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[224] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[225] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 18, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[226] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[227] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[228] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[229] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[230] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[231] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[232] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[233] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[234] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[235] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[236] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[237] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[238] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[239] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[240] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[241] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[242] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[243] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[244] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 31):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[245] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 32):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[246] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 34):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[247] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 19, Bloque 35):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[248] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 20, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[249] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 20, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[250] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 20, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[251] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 20, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[252] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 20, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[253] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 20, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[254] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 20, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[255] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 20, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[256] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 20, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[257] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 20, Bloque 30):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[258] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[259] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[260] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[261] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[262] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[263] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[264] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[265] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[266] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[267] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[268] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[269] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[270] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[271] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[272] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[273] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[274] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[275] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[276] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 21, Bloque 31):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[277] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 22, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[278] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 22, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[279] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 22, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[280] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 22, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[281] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 22, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[282] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 22, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[283] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 22, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[284] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 22, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[285] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 22, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[286] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 22, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[287] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 22, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[288] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 22, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[289] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 22, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[290] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 23, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[291] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 23, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[292] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 23, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[293] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 23, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[294] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 23, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[295] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 23, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[296] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 23, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[297] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 23, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[298] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 23, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[299] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 23, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[300] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 23, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[301] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 23, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[302] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 23, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[303] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 24, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[304] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 24, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[305] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 24, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[306] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 24, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[307] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 24, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[308] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 24, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[309] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 24, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[310] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 24, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[311] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 24, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[312] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 24, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[313] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 24, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[314] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[315] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[316] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[317] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[318] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[319] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[320] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[321] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[322] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[323] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[324] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[325] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[326] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[327] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[328] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[329] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[330] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[331] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[332] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[333] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 25, Bloque 31):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[334] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 26, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[335] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 26, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[336] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 26, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[337] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 26, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[338] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 26, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[339] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 26, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[340] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 26, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[341] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 26, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[342] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 26, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[343] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 26, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[344] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 26, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[345] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 26, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[346] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 26, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[347] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 27, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[348] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 27, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[349] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 27, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[350] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 27, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[351] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 27, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[352] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 27, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[353] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 27, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[354] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[355] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[356] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[357] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[358] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[359] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[360] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[361] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[362] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[363] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[364] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[365] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 31):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[366] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 32):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[367] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 35):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[368] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 36):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[369] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 37):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[370] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 39):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[371] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 28, Bloque 40):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[372] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 29, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[373] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 29, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[374] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 29, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[375] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 29, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[376] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 29, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[377] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 29, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[378] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 29, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[379] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 29, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[380] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 29, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[381] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 29, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[382] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 29, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[383] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 29, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[384] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 29, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[385] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 29, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[386] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 29, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[387] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 29, Bloque 30):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[388] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 30, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[389] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 30, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[390] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 30, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[391] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 30, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[392] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 30, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[393] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 30, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[394] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 30, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[395] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 30, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[396] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 30, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[397] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 30, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[398] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 30, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[399] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 30, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[400] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 30, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[401] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 31, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[402] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 31, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[403] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 31, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[404] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 31, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[405] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 31, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[406] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 31, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[407] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 31, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[408] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 31, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[409] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 31, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[410] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 31, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[411] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 31, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[412] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 31, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[413] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 31, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[414] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 31, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[415] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 31, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[416] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 32, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[417] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 32, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[418] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 32, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[419] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 32, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[420] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 33, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[421] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 33, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[422] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 33, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[423] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 33, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[424] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 33, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[425] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 33, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[426] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 33, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[427] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 33, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[428] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 33, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[429] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 33, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[430] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 33, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[431] DESBORDE_MARGEN_DERECHO (Pagina PDF 33, Bloque 31):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[432] DESBORDE_MARGEN_DERECHO (Pagina PDF 33, Bloque 32):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[433] DESBORDE_MARGEN_DERECHO (Pagina PDF 33, Bloque 33):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[434] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 34, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[435] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 34, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[436] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 34, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[437] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 34, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[438] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 34, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[439] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 34, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[440] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 34, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[441] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 34, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[442] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 34, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[443] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 35, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[444] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 35, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[445] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 35, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[446] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 35, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[447] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 35, Bloque 65):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[448] COLISION_BLOQUES_VISUALES (Pagina PDF 35):** Verificar tablas flotantes o saltos de linea negativos en el documento DOCX.
- **[449] PAGINA_HUERFANA_CASI_BLANCO (Pagina PDF 36):** Revisar saltos de pagina redundantes o tablas desbordadas que empujan saltos en blanco.
- **[450] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[451] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[452] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[453] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[454] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[455] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[456] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[457] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[458] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[459] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[460] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[461] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[462] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[463] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[464] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[465] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[466] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[467] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[468] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 37, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[469] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 38, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[470] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 38, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[471] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 38, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[472] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 38, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[473] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 38, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[474] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 38, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[475] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 38, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[476] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 38, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[477] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 38, Bloque 30):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[478] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 38, Bloque 32):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[479] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[480] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[481] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[482] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[483] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[484] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[485] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[486] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[487] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[488] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[489] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[490] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[491] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[492] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[493] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[494] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[495] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[496] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[497] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[498] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[499] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[500] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 30):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[501] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 31):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[502] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 32):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[503] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 39, Bloque 33):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[504] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[505] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[506] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[507] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[508] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[509] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[510] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[511] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[512] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[513] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[514] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 31):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[515] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 32):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[516] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 33):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[517] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 34):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[518] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 35):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[519] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 36):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[520] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 37):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[521] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 40, Bloque 38):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[522] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[523] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[524] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[525] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[526] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[527] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[528] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[529] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[530] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[531] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[532] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[533] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[534] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[535] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[536] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[537] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[538] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[539] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[540] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[541] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[542] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[543] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[544] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 30):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[545] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 31):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[546] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 32):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[547] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 33):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[548] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 41, Bloque 34):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[549] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 42, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[550] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 42, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[551] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 42, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[552] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 42, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[553] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 43, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[554] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 43, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[555] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 43, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[556] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 43, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[557] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 43, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[558] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 43, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[559] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 43, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[560] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 44, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[561] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 44, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[562] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 44, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[563] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 44, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[564] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 44, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[565] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 45, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[566] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 45, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[567] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 45, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[568] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 45, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[569] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 45, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[570] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 45, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[571] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 45, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[572] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 45, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[573] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 45, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[574] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 45, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[575] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 45, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[576] DESBORDE_MARGEN_DERECHO (Pagina PDF 45, Bloque 30):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[577] COLISION_BLOQUES_VISUALES (Pagina PDF 45):** Verificar tablas flotantes o saltos de linea negativos en el documento DOCX.
- **[578] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[579] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[580] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[581] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[582] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[583] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[584] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[585] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[586] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[587] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[588] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[589] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[590] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[591] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[592] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 30):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[593] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 31):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[594] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 46, Bloque 32):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[595] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[596] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[597] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[598] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[599] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[600] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[601] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[602] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[603] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[604] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[605] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[606] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[607] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[608] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[609] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[610] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[611] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 31):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[612] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 32):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[613] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 47, Bloque 33):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[614] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[615] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[616] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[617] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[618] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[619] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[620] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[621] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[622] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[623] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[624] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[625] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[626] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[627] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[628] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[629] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[630] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[631] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 30):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[632] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 31):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[633] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 32):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[634] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 48, Bloque 33):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[635] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[636] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[637] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[638] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[639] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[640] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 13):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[641] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[642] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[643] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[644] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[645] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[646] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[647] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[648] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[649] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[650] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[651] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 27):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[652] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[653] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 30):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[654] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 49, Bloque 32):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[655] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 50, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[656] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 50, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[657] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 50, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[658] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 50, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[659] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 50, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[660] PAGINA_HUERFANA_CASI_BLANCO (Pagina PDF 51):** Revisar saltos de pagina redundantes o tablas desbordadas que empujan saltos en blanco.
- **[661] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 52, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[662] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 52, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[663] DESBORDE_MARGEN_DERECHO (Pagina PDF 52, Bloque 10):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[664] DESBORDE_MARGEN_DERECHO (Pagina PDF 52, Bloque 11):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[665] DESBORDE_MARGEN_DERECHO (Pagina PDF 52, Bloque 46):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[666] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 53, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[667] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 53, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[668] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 53, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[669] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 53, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[670] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 53, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[671] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 53, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[672] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 53, Bloque 17):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[673] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 53, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[674] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 53, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[675] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 53, Bloque 21):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[676] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 53, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[677] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 53, Bloque 30):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[678] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 53, Bloque 31):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[679] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 53, Bloque 32):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[680] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 54, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[681] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 54, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[682] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 54, Bloque 11):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[683] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 54, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[684] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 54, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[685] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 54, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[686] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 54, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[687] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 54, Bloque 28):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[688] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 55, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[689] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 55, Bloque 8):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[690] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 55, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[691] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 55, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[692] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 55, Bloque 19):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[693] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 55, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[694] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 55, Bloque 26):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[695] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 55, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[696] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 56, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[697] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 56, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[698] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 56, Bloque 9):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[699] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 56, Bloque 16):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[700] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 56, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[701] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 56, Bloque 22):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[702] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 56, Bloque 25):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[703] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 56, Bloque 29):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[704] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 57, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[705] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 57, Bloque 7):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[706] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 57, Bloque 12):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[707] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 57, Bloque 15):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[708] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 57, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[709] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 57, Bloque 20):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[710] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 57, Bloque 23):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[711] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 57, Bloque 24):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[712] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 57, Bloque 30):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[713] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 58, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[714] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 58, Bloque 10):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[715] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 58, Bloque 14):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[716] PAGINA_HUERFANA_CASI_BLANCO (Pagina PDF 59):** Revisar saltos de pagina redundantes o tablas desbordadas que empujan saltos en blanco.
- **[717] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 60, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[718] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 60, Bloque 5):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[719] DESBORDE_MARGEN_DERECHO (Pagina PDF 60, Bloque 5):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[720] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 60, Bloque 6):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[721] DESBORDE_MARGEN_DERECHO (Pagina PDF 60, Bloque 14):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[722] DESBORDE_MARGEN_DERECHO (Pagina PDF 60, Bloque 15):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[723] DESBORDE_MARGEN_DERECHO (Pagina PDF 60, Bloque 16):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[724] DESBORDE_MARGEN_DERECHO (Pagina PDF 60, Bloque 17):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[725] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 60, Bloque 18):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[726] DESBORDE_MARGEN_DERECHO (Pagina PDF 60, Bloque 24):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[727] DESBORDE_MARGEN_IZQUIERDO (Pagina PDF 61, Bloque 4):** Verificar sangrias negativas de parrafos o celdas de tablas desalineadas.
- **[728] DESBORDE_MARGEN_DERECHO (Pagina PDF 61, Bloque 4):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[729] DESBORDE_MARGEN_DERECHO (Pagina PDF 61, Bloque 9):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[730] DESBORDE_MARGEN_DERECHO (Pagina PDF 61, Bloque 12):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[731] DESBORDE_MARGEN_DERECHO (Pagina PDF 61, Bloque 13):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[732] DESBORDE_MARGEN_DERECHO (Pagina PDF 61, Bloque 18):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[733] DESBORDE_MARGEN_DERECHO (Pagina PDF 61, Bloque 19):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[734] DESBORDE_MARGEN_DERECHO (Pagina PDF 61, Bloque 25):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[735] DESBORDE_MARGEN_DERECHO (Pagina PDF 61, Bloque 26):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[736] DESBORDE_MARGEN_DERECHO (Pagina PDF 61, Bloque 30):** Verificar ancho de tablas o formulas largas sin quiebre.