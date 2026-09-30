---
name: tablas-quirurgicas-docx-apa7
description: Generación quirúrgica y automatizada de tablas nativas en Microsoft Word (.docx) bajo normas APA 7.ª edición con python-docx y OpenXML para SIVAC-THESIS-LAB.
---

# TABLAS QUIRÚRGICAS EN WORD (.DOCX) — NORMA APA 7.ª EDICIÓN

> **Propósito:** Esta habilidad proporciona el código Python (`python-docx`) y las estructuras de bajo nivel OpenXML (`oxml`) necesarias para construir tablas académicas nativas en Word que cumplan al 100% con los estándares de APA 7 y el formato oficial de la UNAJMA.

---

## 1. Reglas Estructurales de Tablas en APA 7

1. **Líneas Horizontales Obligatorias (Exactamente Tres):**
   - Borde superior de la tabla (arriba de los encabezados): 1/2 pt a 1 pt.
   - Borde inferior de los encabezados (separando cabecera de datos): 1/2 pt a 1 pt.
   - Borde inferior de la tabla (después de la última fila de datos): 1/2 pt a 1 pt.
2. **Prohibición de Líneas Verticales:**
   - Queda terminantemente prohibido el uso de bordes verticales exteriores (`left`, `right`) o interiores (`insideV`).
3. **Repetición de Cabeceras (`w:tblHeader`):**
   - La fila de encabezados debe repetirse automáticamente si la tabla se fragmenta en dos páginas.
4. **Protección contra División de Filas (`w:cantSplit`):**
   - Ninguna fila de datos debe partirse entre dos páginas; la fila debe mantenerse íntegra en la página superior o saltar completa a la siguiente.
5. **Tipografía y Jerarquía:**
   - **Número de Tabla:** Párrafo propio en negrita, sin punto final (ej. `Tabla 1`).
   - **Título de la Tabla:** Siguiente párrafo en cursiva, interlineado 1.5, con mayúscula inicial (ej. *Estadísticos descriptivos del tiempo de registro en pretest y postest*).
   - **Cuerpo de la Tabla:** Times New Roman 10 pt (o 11 pt), interlineado sencillo (1.0) o 1.15, alineación a la izquierda para texto descriptivo y centrada o a la derecha para cifras numéricas.
   - **Nota de la Tabla:** Párrafo inferior con la palabra `*Nota.*` en cursiva seguida de texto normal en 10 pt.

---

## 2. Implementación Quirúrgica con `python-docx` y OpenXML

```python
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def aplicar_estilo_apa7_tabla(table):
    """
    Aplica los bordes canónicos de APA 7: solo 3 líneas horizontales,
    sin líneas verticales, cantSplit en todas las filas y tblHeader en la primera.
    """
    # 1. Alineación centrada de la tabla en la página
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # 2. Configurar bordes OpenXML (3 líneas horizontales)
    tblPr = table._tbl.tblPr
    # Eliminar cualquier configuración previa de bordes
    for child in list(tblPr):
        if child.tag.endswith('tblBorders'):
            tblPr.remove(child)
            
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="8" w:space="0" w:color="auto"/>'
        f'  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="auto"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="none"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)
    
    # 3. Procesar fila de encabezados (Fila 0)
    header_tr = table.rows[0]._tr.get_or_add_trPr()
    header_tr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    header_tr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    
    # Borde inferior del encabezado
    for cell in table.rows[0].cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="auto"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(tcBorders)
        
    # 4. Procesar filas de datos (cantSplit en todas)
    for row in table.rows[1:]:
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
    # 5. Margen interno de celdas (padding)
    tblCellMar = parse_xml(
        f'<w:tblCellMar {nsdecls("w")}>'
        f'  <w:top w:w="120" w:type="dxa"/>'
        f'  <w:bottom w:w="120" w:type="dxa"/>'
        f'  <w:left w:w="160" w:type="dxa"/>'
        f'  <w:right w:w="160" w:type="dxa"/>'
        f'</w:tblCellMar>'
    )
    tblPr.append(tblCellMar)

def insertar_tabla_apa7(doc, numero, titulo, encabezados, datos, anchos, nota=None):
    """
    Inserta una tabla completa en formato APA 7 con número, título y nota.
    """
    # 1. Párrafo de Número de Tabla
    p_num = doc.add_paragraph()
    p_num.paragraph_format.space_before = Pt(12)
    p_num.paragraph_format.space_after = Pt(2)
    p_num.paragraph_format.line_spacing = 1.15
    run_num = p_num.add_run(f"Tabla {numero}")
    run_num.font.name = "Times New Roman"
    run_num.font.size = Pt(12)
    run_num.font.bold = True
    
    # 2. Párrafo de Título de Tabla
    p_tit = doc.add_paragraph()
    p_tit.paragraph_format.space_before = Pt(0)
    p_tit.paragraph_format.space_after = Pt(6)
    p_tit.paragraph_format.line_spacing = 1.15
    run_tit = p_tit.add_run(titulo)
    run_tit.font.name = "Times New Roman"
    run_tit.font.size = Pt(12)
    run_tit.font.italic = True
    
    # 3. Crear Tabla
    table = doc.add_table(rows=len(datos) + 1, cols=len(encabezados))
    aplicar_estilo_apa7_tabla(table)
    
    # 4. Rellenar Encabezados
    for col_idx, enc in enumerate(encabezados):
        cell = table.cell(0, col_idx)
        cell.width = Inches(anchos[col_idx])
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(enc)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)
        run.font.bold = True
        
    # 5. Rellenar Datos
    for row_idx, fila in enumerate(datos):
        for col_idx, val in enumerate(fila):
            cell = table.cell(row_idx + 1, col_idx)
            cell.width = Inches(anchos[col_idx])
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            # Alinear texto a la izquierda, números al centro o derecha
            if col_idx == 0 and not str(val).replace('.', '').isdigit():
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(str(val))
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
            
    # 6. Párrafo de Nota de Tabla
    if nota:
        p_nota = doc.add_paragraph()
        p_nota.paragraph_format.space_before = Pt(4)
        p_nota.paragraph_format.space_after = Pt(12)
        p_nota.paragraph_format.line_spacing = 1.0
        run_etiqueta = p_nota.add_run("Nota. ")
        run_etiqueta.font.name = "Times New Roman"
        run_etiqueta.font.size = Pt(10)
        run_etiqueta.font.italic = True
        run_cuerpo = p_nota.add_run(nota)
        run_cuerpo.font.name = "Times New Roman"
        run_cuerpo.font.size = Pt(10)
```
