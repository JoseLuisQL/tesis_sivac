---
name: tablas-quirurgicas-docx-apa7
description: Generación quirúrgica y automatizada de tablas nativas en Microsoft Word (.docx) bajo normas APA 7.ª edición con python-docx y OpenXML para SIVAC-THESIS-LAB.
---

# TABLAS QUIRÚRGICAS EN WORD (.DOCX) — NORMA APA 7.ª EDICIÓN

> **Propósito:** Esta habilidad proporciona el motor Python oficial (`scripts/utilidades/docx_quirurgico.py`) y las directivas de bajo nivel OpenXML (`oxml`) necesarias para construir, auditar y blindar tablas académicas nativas en Word que cumplan al 100% con los estándares de APA 7 y el formato oficial de la UNAJMA, integrando fórmulas matemáticas nativas OMML y auditoría visual desatendida.

---

## 1. Reglas Estructurales Innegociables de Tablas APA 7

1. **Líneas Horizontales Obligatorias (Exactamente Tres):**
   - Borde superior de la tabla (arriba de los encabezados): 1/2 pt a 1 pt (`w:top`, sz="4" a "8").
   - Borde inferior de los encabezados (separando cabecera de datos): 1/2 pt a 1 pt (`w:bottom` en celdas de Fila 0).
   - Borde inferior de la tabla (después de la última fila de datos): 1/2 pt a 1 pt (`w:bottom`, sz="4" a "8").
2. **Prohibición Total de Líneas Verticales:**
   - Queda terminantemente prohibido el uso de bordes verticales exteriores (`left`, `right`) o interiores (`insideV`).
3. **Erradicación de Flotación (`<w:tblpPr>`):**
   - Las tablas **JAMÁS** deben ser flotantes. Si contienen `<w:tblpPr>`, Word rompe el flujo del documento, fractura filas caóticamente y superpone texto.
4. **Repetición de Cabeceras (`<w:tblHeader>`):**
   - La fila de encabezados debe repetirse automáticamente si la tabla se fragmenta en varias páginas.
5. **Protección contra División de Filas (`<w:cantSplit>`):**
   - Ninguna fila de datos debe partirse entre dos páginas; la fila debe mantenerse íntegra en la página actual o saltar completa a la siguiente.
6. **Límites de Ancho Imprimible en dxa (UNAJMA):**
   - **Página Vertical (Portrait):** Margen izquierdo 3.0 cm, derecho 2.5 cm $\to$ **Máximo 8,788 dxa (15.50 cm)**.
   - **Página Horizontal (Landscape):** Márgenes laterales 2.5 cm $\to$ **Máximo 14,000 dxa (24.70 cm)**.

---

## 2. Motor Quirúrgico Central: `scripts/utilidades/docx_quirurgico.py`

En lugar de reescribir scripts ad-hoc para cada tabla, todos los agentes deben importar y utilizar las utilidades probadas:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import docx
from scripts.utilidades.docx_quirurgico import (
    configurar_geometria_tabla,
    aplicar_bordes_apa7,
    blindar_filas_tabla,
    eliminar_flotacion_tabla,
    mathml_to_omml,
    crear_parrafo_formula_dedicada,
    crear_parrafo_mixto_inline,
    crear_parrafo_celda,
    set_tc_paragraphs,
    set_tc_vmerge,
    exportar_docx_a_pdf,
    renderizar_paginas_pdf
)
```

---

## 3. Patrones de Construcción y Modificación Quirúrgica

### A. Configurar Geometría Exacta y Bordes APA 7
```python
# Definir anchos por columna en dxa sumando exactamente el ancho útil
# Ejemplo para Landscape (Total: 14,000 dxa):
col_widths = [1200, 2250, 2250, 2250, 1350, 3100, 1600]
configurar_geometria_tabla(table, total_width_dxa=14000, col_widths_dxa=col_widths, align="center")
aplicar_bordes_apa7(table)
blindar_filas_tabla(table, cant_split=True, repetir_encabezado=True)
```

### B. Inserción de Fórmulas Matemáticas Nativas OMML (`<m:oMath>`)
```python
# MathML bien formado (sin cajas punteadas ni <m:e/> huérfanos)
mml_tiempo = """<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mrow>
    <msub><mi>T</mi><mtext>reg</mtext></msub><mo>=</mo>
    <msub><mi>t</mi><mtext>fin</mtext></msub><mo>−</mo><msub><mi>t</mi><mtext>inicio</mtext></msub>
  </mrow>
</math>"""

omml_elem = mathml_to_omml(mml_tiempo)

# Opción 1: Párrafo de fórmula dedicada centrada o indentada
p_form = crear_parrafo_formula_dedicada(omml_elem, align="left", line_spacing=200, space_before=2, space_after=4)

# Opción 2: Párrafo mixto con texto y fórmula en la misma línea
p_mixto = crear_parrafo_mixto_inline([
    ("Tiempo de registro: ", True, False), # Negrita
    omml_elem,
    (" (minutos)", False, False)
], font_size_pt=7.5, line_spacing=200)

# Asignar a la celda
set_tc_paragraphs(celda._tc, [p_mixto])
```

### C. Fusión Vertical de Celdas (`w:vMerge`)
```python
# En la primera fila del bloque fusionado:
set_tc_vmerge(celda_fila_1._tc, 'restart')

# En las siguientes filas que continúan la fusión:
set_tc_vmerge(celda_fila_2._tc, 'continue')
set_tc_paragraphs(celda_fila_2._tc, [])  # Celda vacía sin contenido redundante
```

---

## 4. Herramientas de Línea de Comandos (CLI) para Agentes

Cualquier agente puede verificar y auditar el estado editorial ejecutando:

1. **Auditar geometría y anomalías en tablas:**
   ```bash
   python scripts/utilidades/docx_quirurgico.py auditar salidas/documentos/informe_final_v01.docx
   ```
   *(Alerta instantáneamente si existen tablas con `w:tblpPr`, filas sin `w:cantSplit` o anchos desbordados).*

2. **Blindar todas las tablas de un documento automáticamente:**
   ```bash
   python scripts/utilidades/docx_quirurgico.py blindar-todas salidas/documentos/informe_final_v01.docx
   ```

3. **Exportar a PDF oficial mediante Microsoft Word COM:**
   ```bash
   python scripts/utilidades/docx_quirurgico.py exportar-pdf salidas/documentos/informe_final_v01.docx
   ```

4. **Renderizar páginas clave a imágenes PNG para auditoría visual:**
   ```bash
   python scripts/utilidades/docx_quirurgico.py renderizar-paginas salidas/documentos/informe_final_v01.pdf --paginas 32,51 --dpi 150
   ```
