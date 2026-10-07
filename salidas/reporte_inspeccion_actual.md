# Reporte de Auditoria Editorial y Visual OpenXML
- **Documento DOCX:** `PROYECTO_TESIS_ACTUALIZADO_V3_NORMALIZADO.docx`
- **Documento PDF:** `PROYECTO_TESIS_ACTUALIZADO_V3_NORMALIZADO.pdf` (62 paginas)
- **Estado General:** `RECHAZADO`

## Resumen de Metricas Estructurales
| Metrica | Valor |
|---|---|
| Total Parrafos | 610 |
| Total Tablas | 12 |
| Total Celdas | 553 |
| Formulas OMML en Celdas | 15 |
| Listas Detectadas | 60 |
| Quiebres Manuales (w:br) | 1 |
| Defectos Criticos | 0 |
| Defectos Altos | 6 |
| Defectos Medios | 2 |
| Defectos Bajos | 0 |

## Hallazgos y Defectos Detectados
| # | Categoria | Severidad | Ubicacion | Codigo | Descripcion |
|---|---|---|---|---|---|
| 1 | RENDER_VISUAL | **ALTA** | Pagina PDF 7 | `PAGINA_HUERFANA_CASI_BLANCO` | Pagina 7 es casi blanca (densidad tinta: 0.00%, palabras: 0). |
| 2 | RENDER_VISUAL | **ALTA** | Pagina PDF 36 | `COLISION_BLOQUES_VISUALES` | Colision y solapamiento visual directo detectado entre bloques de texto en PDF. |
| 3 | RENDER_VISUAL | **ALTA** | Pagina PDF 37 | `PAGINA_HUERFANA_CASI_BLANCO` | Pagina 37 es casi blanca (densidad tinta: 0.00%, palabras: 0). |
| 4 | RENDER_VISUAL | **ALTA** | Pagina PDF 46 | `COLISION_BLOQUES_VISUALES` | Colision y solapamiento visual directo detectado entre bloques de texto en PDF. |
| 5 | RENDER_VISUAL | **ALTA** | Pagina PDF 52 | `PAGINA_HUERFANA_CASI_BLANCO` | Pagina 52 es casi blanca (densidad tinta: 0.21%, palabras: 14). |
| 6 | RENDER_VISUAL | **MEDIA** | Pagina PDF 54, Bloque 16 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (549.9 pt > 543.0 pt). |
| 7 | RENDER_VISUAL | **MEDIA** | Pagina PDF 54, Bloque 17 | `DESBORDE_MARGEN_DERECHO` | Contenido excede el margen derecho seguro (549.9 pt > 543.0 pt). |
| 8 | RENDER_VISUAL | **ALTA** | Pagina PDF 60 | `PAGINA_HUERFANA_CASI_BLANCO` | Pagina 60 es casi blanca (densidad tinta: 0.04%, palabras: 1). |

### Acciones de Mitigacion Recomendadas
- **[1] PAGINA_HUERFANA_CASI_BLANCO (Pagina PDF 7):** Revisar saltos de pagina redundantes o tablas desbordadas que empujan saltos en blanco.
- **[2] COLISION_BLOQUES_VISUALES (Pagina PDF 36):** Verificar tablas flotantes o saltos de linea negativos en el documento DOCX.
- **[3] PAGINA_HUERFANA_CASI_BLANCO (Pagina PDF 37):** Revisar saltos de pagina redundantes o tablas desbordadas que empujan saltos en blanco.
- **[4] COLISION_BLOQUES_VISUALES (Pagina PDF 46):** Verificar tablas flotantes o saltos de linea negativos en el documento DOCX.
- **[5] PAGINA_HUERFANA_CASI_BLANCO (Pagina PDF 52):** Revisar saltos de pagina redundantes o tablas desbordadas que empujan saltos en blanco.
- **[6] DESBORDE_MARGEN_DERECHO (Pagina PDF 54, Bloque 16):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[7] DESBORDE_MARGEN_DERECHO (Pagina PDF 54, Bloque 17):** Verificar ancho de tablas o formulas largas sin quiebre.
- **[8] PAGINA_HUERFANA_CASI_BLANCO (Pagina PDF 60):** Revisar saltos de pagina redundantes o tablas desbordadas que empujan saltos en blanco.