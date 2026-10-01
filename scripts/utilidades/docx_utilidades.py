#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB — UTILIDADES Y ESTILOS OPENXML PARA PYTHON-DOCX
Normativa: APA 7.ª edición y Reglamento de Grados y Títulos UNAJMA
================================================================================
"""

import os
import re
import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def aplicar_margenes_unajma(seccion):
    """Aplica márgenes reglamentarios UNAJMA: Izq 3.0 cm, Der/Sup/Inf 2.54 cm."""
    seccion.page_width = Cm(21.0)
    seccion.page_height = Cm(29.7)
    seccion.left_margin = Cm(3.0)
    seccion.right_margin = Cm(2.54)
    seccion.top_margin = Cm(2.54)
    seccion.bottom_margin = Cm(2.54)
    seccion.header_distance = Cm(1.27)
    seccion.footer_distance = Cm(1.27)

def configurar_numeracion(seccion, tipo='lowerRoman', start_num=None, desvincular=False, omitir_primera=False):
    """Configura la numeración de página OpenXML en la esquina superior derecha."""
    header = seccion.header
    if desvincular:
        header.is_linked_to_previous = False
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.text = ""
    run = p.add_run()
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), 'PAGE')
    run._r.append(fld)

    sectPr = seccion._sectPr
    for child in sectPr.findall(qn('w:pgNumType')):
        sectPr.remove(child)

    pgNumType = OxmlElement('w:pgNumType')
    if tipo:
        pgNumType.set(qn('w:fmt'), tipo)
    if start_num is not None:
        pgNumType.set(qn('w:start'), str(start_num))
    sectPr.append(pgNumType)

    if omitir_primera:
        seccion.different_first_page_header_footer = True
        seccion.first_page_header.paragraphs[0].text = ""
    else:
        seccion.different_first_page_header_footer = False

def procesar_formato_texto(texto):
    """Procesa marcas simples de markdown como **negrita** y *cursiva*."""
    tokens = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*)', texto)
    res = []
    for t in tokens:
        if not t:
            continue
        if t.startswith('**') and t.endswith('**') and len(t) >= 4:
            res.append((t[2:-2], True, False))
        elif t.startswith('*') and t.endswith('*') and len(t) >= 2:
            res.append((t[1:-1], False, True))
        else:
            res.append((t, False, False))
    return res

def agregar_titulo_1(doc, texto, page_break=True):
    """Nivel 1: Centrado, Negrita, Mayúsculas, 14 pt, Times New Roman."""
    p = doc.add_paragraph()
    if page_break:
        p.paragraph_format.page_break_before = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(14)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.first_line_indent = Inches(0)
    run = p.add_run(texto.upper())
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True
    return p

def agregar_titulo_2(doc, texto):
    """Nivel 2: Alineado a la izquierda, Negrita, 12 pt, Times New Roman."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.first_line_indent = Inches(0)
    run = p.add_run(texto)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    return p

def agregar_titulo_3(doc, texto):
    """Nivel 3: Alineado a la izquierda, Negrita Cursiva, 12 pt, Times New Roman."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.first_line_indent = Inches(0)
    run = p.add_run(texto)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.italic = True
    return p

def agregar_parrafo(doc, texto, sangria=True, cursiva=False, negrita=False, interlineado=1.5, alineacion=WD_ALIGN_PARAGRAPH.JUSTIFY):
    """Párrafo estándar APA 7: Justificado, 12 pt, interlineado 1.5, sangría 1.27 cm (0.5 in)."""
    p = doc.add_paragraph()
    p.alignment = alineacion
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = interlineado
    p.paragraph_format.first_line_indent = Inches(0.5) if sangria else Inches(0)

    partes = procesar_formato_texto(texto)
    for r_texto, r_bold, r_italic in partes:
        run = p.add_run(r_texto)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = negrita or r_bold
        run.font.italic = cursiva or r_italic
    return p

def agregar_item_lista(doc, texto, simbolo="•", sangria_izq=0.5):
    """Elemento de lista con viñeta o número."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.left_indent = Inches(sangria_izq)
    p.paragraph_format.first_line_indent = Inches(-0.25)

    run_sym = p.add_run(f"{simbolo} ")
    run_sym.font.name = 'Times New Roman'
    run_sym.font.size = Pt(12)
    run_sym.font.bold = True

    partes = procesar_formato_texto(texto)
    for r_texto, r_bold, r_italic in partes:
        run = p.add_run(r_texto)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = r_bold
        run.font.italic = r_italic
    return p

def agregar_referencia_apa7(doc, texto):
    """Referencia APA 7 con sangría francesa de 1.27 cm (0.5 in)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.5)

    partes = procesar_formato_texto(texto)
    for r_texto, r_bold, r_italic in partes:
        run = p.add_run(r_texto)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = r_bold
        run.font.italic = r_italic
    return p

def formatear_tabla_apa7(table, col_widths=None):
    """Formatea una tabla según APA 7 (líneas horizontales canónicas, sin verticales, repetición de encabezado)."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        r'<w:tblBorders %s>'
        r'  <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        r'  <w:left w:val="none"/>'
        r'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        r'  <w:right w:val="none"/>'
        r'  <w:insideH w:val="none"/>'
        r'  <w:insideV w:val="none"/>'
        r'</w:tblBorders>' % nsdecls('w')
    )
    tblPr.append(tblBorders)

    if len(table.rows) > 0:
        header_tr = table.rows[0]._tr
        trPr = header_tr.get_or_add_trPr()
        trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                r'<w:tcBorders %s>'
                r'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
                r'</w:tcBorders>' % nsdecls('w')
            )
            tcPr.append(tcBorders)

    for r_idx, row in enumerate(table.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if col_widths and c_idx < len(col_widths):
                cell.width = col_widths[c_idx]
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.first_line_indent = Inches(0)
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(10)
                    if r_idx == 0:
                        run.font.bold = True

def agregar_encabezado_tabla_apa7(doc, numero, titulo):
    p_num = doc.add_paragraph()
    p_num.paragraph_format.space_before = Pt(12)
    p_num.paragraph_format.space_after = Pt(2)
    p_num.paragraph_format.line_spacing = 1.0
    p_num.paragraph_format.first_line_indent = Inches(0)
    run_num = p_num.add_run(f"Tabla {numero}")
    run_num.font.name = 'Times New Roman'
    run_num.font.size = Pt(10)
    run_num.font.bold = True

    p_tit = doc.add_paragraph()
    p_tit.paragraph_format.space_before = Pt(0)
    p_tit.paragraph_format.space_after = Pt(4)
    p_tit.paragraph_format.line_spacing = 1.0
    p_tit.paragraph_format.first_line_indent = Inches(0)
    run_tit = p_tit.add_run(titulo)
    run_tit.font.name = 'Times New Roman'
    run_tit.font.size = Pt(10)
    run_tit.font.italic = True

def agregar_nota_tabla_apa7(doc, texto_nota):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Inches(0)
    run_etiqueta = p.add_run("Nota. ")
    run_etiqueta.font.name = 'Times New Roman'
    run_etiqueta.font.size = Pt(9)
    run_etiqueta.font.italic = True
    run_texto = p.add_run(texto_nota)
    run_texto.font.name = 'Times New Roman'
    run_texto.font.size = Pt(9)

def agregar_tabla_datos(doc, numero, titulo, encabezados, filas, nota=None, col_widths=None):
    agregar_encabezado_tabla_apa7(doc, numero, titulo)
    tbl = doc.add_table(rows=len(filas) + 1, cols=len(encabezados))
    for c_idx, h_text in enumerate(encabezados):
        cell = tbl.rows[0].cells[c_idx]
        cell.text = h_text
    for r_idx, fila in enumerate(filas):
        for c_idx, val in enumerate(fila):
            cell = tbl.rows[r_idx + 1].cells[c_idx]
            cell.text = str(val)
    formatear_tabla_apa7(tbl, col_widths=col_widths)
    if nota:
        agregar_nota_tabla_apa7(doc, nota)

def agregar_figura_apa7(doc, numero, titulo, ruta_imagen, texto_nota, ancho_in=5.8):
    p_num = doc.add_paragraph()
    p_num.paragraph_format.space_before = Pt(12)
    p_num.paragraph_format.space_after = Pt(2)
    p_num.paragraph_format.line_spacing = 1.0
    p_num.paragraph_format.first_line_indent = Inches(0)
    run_num = p_num.add_run(f"Figura {numero}")
    run_num.font.name = 'Times New Roman'
    run_num.font.size = Pt(10)
    run_num.font.bold = True

    p_tit = doc.add_paragraph()
    p_tit.paragraph_format.space_before = Pt(0)
    p_tit.paragraph_format.space_after = Pt(6)
    p_tit.paragraph_format.line_spacing = 1.0
    p_tit.paragraph_format.first_line_indent = Inches(0)
    run_tit = p_tit.add_run(titulo)
    run_tit.font.name = 'Times New Roman'
    run_tit.font.size = Pt(10)
    run_tit.font.italic = True

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(4)
    p_img.paragraph_format.first_line_indent = Inches(0)
    if os.path.exists(ruta_imagen):
        p_img.add_run().add_picture(ruta_imagen, width=Inches(ancho_in))
    else:
        run_alt = p_img.add_run(f"[RECURSO GRÁFICO OFICIAL: {os.path.basename(ruta_imagen)}]")
        run_alt.font.name = 'Times New Roman'
        run_alt.font.italic = True

    p_nota = doc.add_paragraph()
    p_nota.paragraph_format.space_before = Pt(4)
    p_nota.paragraph_format.space_after = Pt(12)
    p_nota.paragraph_format.line_spacing = 1.0
    p_nota.paragraph_format.first_line_indent = Inches(0)
    run_n_lbl = p_nota.add_run("Nota. ")
    run_n_lbl.font.name = 'Times New Roman'
    run_n_lbl.font.size = Pt(9)
    run_n_lbl.font.italic = True
    run_n_txt = p_nota.add_run(texto_nota)
    run_n_txt.font.name = 'Times New Roman'
    run_n_txt.font.size = Pt(9)
