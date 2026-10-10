#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - UTILIDADES Y ESTILOS OPENXML PARA PYTHON-DOCX
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
    """Procesa marcas simples de markdown como ***negrita cursiva***, **negrita** y *cursiva*."""
    tokens = re.split(r'(\*\*\*[^*]+\*\*\*|\*\*[^*]+\*\*|\*[^*]+\*)', str(texto))
    res = []
    for t in tokens:
        if not t:
            continue
        if t.startswith('***') and t.endswith('***') and len(t) >= 6:
            res.append((t[3:-3], True, True))
        elif t.startswith('**') and t.endswith('**') and len(t) >= 4:
            res.append((t[2:-2], True, False))
        elif t.startswith('*') and t.endswith('*') and len(t) >= 2:
            res.append((t[1:-1], False, True))
        else:
            res.append((t, False, False))
    return res

def agregar_titulo_1(doc, texto, page_break=True, incluir_en_toc=True):
    """Nivel 1: Centrado, Negrita, Mayúsculas, 14 pt, Times New Roman."""
    p = doc.add_paragraph()
    if page_break:
        p.paragraph_format.page_break_before = True
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(14)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.first_line_indent = Inches(0)
    if incluir_en_toc:
        pPr = p._p.get_or_add_pPr()
        pPr.append(parse_xml(r'<w:outlineLvl %s w:val="0"/>' % nsdecls('w')))
    run = p.add_run(texto.upper())
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True
    return p

def agregar_titulo_2(doc, texto, incluir_en_toc=True):
    """Nivel 2: Alineado a la izquierda, Negrita, 12 pt, Times New Roman."""
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.first_line_indent = Inches(0)
    if incluir_en_toc:
        pPr = p._p.get_or_add_pPr()
        pPr.append(parse_xml(r'<w:outlineLvl %s w:val="1"/>' % nsdecls('w')))
    run = p.add_run(texto)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    return p

def agregar_titulo_3(doc, texto, incluir_en_toc=True):
    """Nivel 3: Alineado a la izquierda, Negrita Cursiva, 12 pt, Times New Roman."""
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.first_line_indent = Inches(0)
    if incluir_en_toc:
        pPr = p._p.get_or_add_pPr()
        pPr.append(parse_xml(r'<w:outlineLvl %s w:val="2"/>' % nsdecls('w')))
    run = p.add_run(texto)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.italic = True
    return p

def agregar_titulo_4(doc, texto):
    """Nivel 4: Alineado a la izquierda, Negrita Cursiva, 12 pt, Times New Roman."""
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
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

def formatear_tabla_apa7(table, col_widths=None, font_size_pt=10):
    """Formatea una tabla según APA 7 (líneas horizontales canónicas, sin verticales, repetición de encabezado y cantSplit)."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._tbl.tblPr
    tblpPr = tblPr.find(qn('w:tblpPr'))
    if tblpPr is not None:
        tblPr.remove(tblpPr)
    for b in tblPr.findall(qn('w:tblBorders')):
        tblPr.remove(b)
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

    # Procesar y normalizar anchos de columnas (dxa) dentro del límite portrait (8788 dxa)
    if not col_widths or len(col_widths) == 0:
        n_cols = len(table.columns) if len(table.columns) > 0 else (len(table.rows[0].cells) if len(table.rows) > 0 else 1)
        w_col = 8784 // n_cols
        col_widths = [w_col] * n_cols
        col_widths[-1] += (8784 - sum(col_widths))

    widths_dxa = None
    if col_widths and len(col_widths) > 0:
        raw_dxa = []
        for cw in col_widths:
            val_int = int(cw)
            # Longitudes de python-docx vienen en EMU (1 dxa = 635 EMU)
            if val_int >= 12700:
                raw_dxa.append(int(round(val_int / 635.0)))
            else:
                raw_dxa.append(val_int)

        total_dxa = sum(raw_dxa)
        limite_portrait_dxa = 8788
        if total_dxa > limite_portrait_dxa:
            # Escalamiento proporcional al ancho útil de 8784 dxa (15.50 cm)
            factor = 8784.0 / total_dxa
            widths_dxa = [max(100, int(round(w * factor))) for w in raw_dxa]
            diferencia = 8784 - sum(widths_dxa)
            if widths_dxa:
                widths_dxa[-1] += diferencia
        else:
            widths_dxa = raw_dxa

        # Reconstruir w:tblGrid
        tblGrid = table._tbl.tblGrid
        if tblGrid is not None:
            table._tbl.remove(tblGrid)
        new_grid = parse_xml(r'<w:tblGrid %s/>' % nsdecls('w'))
        for cw in widths_dxa:
            new_grid.append(parse_xml(r'<w:gridCol %s w:w="%d"/>' % (nsdecls('w'), cw)))
        tblPr_idx = list(table._tbl).index(tblPr)
        table._tbl.insert(tblPr_idx + 1, new_grid)

        # Fijar w:tblW en dxa
        for w in tblPr.findall(qn('w:tblW')):
            tblPr.remove(w)
        tblPr.append(parse_xml(r'<w:tblW %s w:w="%d" w:type="dxa"/>' % (nsdecls('w'), sum(widths_dxa))))

        # Fijar w:tblLayout en fixed para que Word no recalcule gridCol por encima del límite portrait
        for tl in tblPr.findall(qn('w:tblLayout')):
            tblPr.remove(tl)
        tblPr.append(parse_xml(r'<w:tblLayout %s w:type="fixed"/>' % nsdecls('w')))

    if len(table.rows) > 0:
        header_tr = table.rows[0]._tr
        trPr = header_tr.get_or_add_trPr()
        if trPr.find(qn('w:tblHeader')) is None:
            trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            for b in tcPr.findall(qn('w:tcBorders')):
                tcPr.remove(b)
            tcBorders = parse_xml(
                r'<w:tcBorders %s>'
                r'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
                r'</w:tcBorders>' % nsdecls('w')
            )
            tcPr.append(tcBorders)

    for r_idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        if trPr.find(qn('w:cantSplit')) is None:
            trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))

        tcs = row._tr.findall(qn('w:tc'))
        if widths_dxa:
            for idx, cw in enumerate(widths_dxa):
                if idx < len(tcs):
                    tcPr = tcs[idx].get_or_add_tcPr()
                    for w in tcPr.findall(qn('w:tcW')):
                        tcPr.remove(w)
                    tcPr.append(parse_xml(r'<w:tcW %s w:w="%d" w:type="dxa"/>' % (nsdecls('w'), cw)))

        for c_idx, cell in enumerate(row.cells):
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.first_line_indent = Inches(0)
                if r_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(font_size_pt)
                    if r_idx == 0:
                        run.font.bold = True

def agregar_encabezado_tabla_apa7(doc, numero, titulo):
    """
    Rótulo APA 7 con campo nativo SEQ Tabla \* ARABIC para auto-detección en TOC de Ilustraciones.
    Párrafo con formato: 'Tabla ' + [SEQ Tabla \* ARABIC] + ' ' + [titulo].
    """
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Inches(0)

    # 1. Rótulo 'Tabla '
    run_lbl = p.add_run("Tabla ")
    run_lbl.font.name = 'Times New Roman'
    run_lbl.font.size = Pt(10)
    run_lbl.font.bold = True

    # 2. Campo complejo SEQ Tabla \* ARABIC con número en caché
    num_str = str(numero).lower().replace("tabla", "").strip() if "tabla" in str(numero).lower() else str(numero).strip()
    r_begin = parse_xml(r'<w:r %s><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>' % nsdecls('w'))
    p._p.append(r_begin)
    r_instr = parse_xml(r'<w:r %s><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:instrText xml:space="preserve"> SEQ Tabla \* ARABIC </w:instrText></w:r>' % nsdecls('w'))
    p._p.append(r_instr)
    r_sep = parse_xml(r'<w:r %s><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>' % nsdecls('w'))
    p._p.append(r_sep)
    r_val = parse_xml(r'<w:r %s><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/><w:noProof/></w:rPr><w:t>%s</w:t></w:r>' % (nsdecls('w'), num_str))
    p._p.append(r_val)
    r_end = parse_xml(r'<w:r %s><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>' % nsdecls('w'))
    p._p.append(r_end)

    # 3. Separador y título en cursiva
    run_sep = p.add_run(" ")
    run_sep.font.name = 'Times New Roman'
    run_sep.font.size = Pt(10)

    run_tit = p.add_run(titulo)
    run_tit.font.name = 'Times New Roman'
    run_tit.font.size = Pt(10)
    run_tit.font.italic = True
    return p

def agregar_nota_tabla_apa7(doc, texto_nota):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Inches(0)
    nota_limpia = str(texto_nota).strip()
    if nota_limpia.startswith("Nota."):
        nota_limpia = nota_limpia[5:].strip()
    elif nota_limpia.startswith("*Nota.*"):
        nota_limpia = nota_limpia[7:].strip()
    run_etiqueta = p.add_run("Nota. ")
    run_etiqueta.font.name = 'Times New Roman'
    run_etiqueta.font.size = Pt(9.5)
    run_etiqueta.font.italic = True
    for r_texto, r_bold, r_italic in procesar_formato_texto(nota_limpia):
        run_texto = p.add_run(r_texto)
        run_texto.font.name = 'Times New Roman'
        run_texto.font.size = Pt(9.5)
        run_texto.font.bold = r_bold
        run_texto.font.italic = r_italic

def agregar_tabla_datos(doc, numero, titulo, encabezados, filas, nota=None, col_widths=None, font_size_pt=10):
    agregar_encabezado_tabla_apa7(doc, numero, titulo)
    tbl = doc.add_table(rows=len(filas) + 1, cols=len(encabezados))
    for c_idx, h_text in enumerate(encabezados):
        cell = tbl.rows[0].cells[c_idx]
        cell.text = str(h_text)
    for r_idx, fila in enumerate(filas):
        for c_idx, val in enumerate(fila):
            cell = tbl.rows[r_idx + 1].cells[c_idx]
            p = cell.paragraphs[0]
            p.text = ""
            for r_texto, r_bold, r_italic in procesar_formato_texto(str(val)):
                run = p.add_run(r_texto)
                run.font.name = 'Times New Roman'
                run.font.size = Pt(font_size_pt)
                run.font.bold = r_bold
                run.font.italic = r_italic
    formatear_tabla_apa7(tbl, col_widths=col_widths, font_size_pt=font_size_pt)
    if nota:
        agregar_nota_tabla_apa7(doc, nota)
    return tbl

def agregar_figura_apa7(doc, numero, titulo, ruta_imagen, texto_nota, ancho_in=5.5, alto_max_in=5.2):
    """
    Inserta una figura APA 7 con campo nativo SEQ Figura \* ARABIC.
    """
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Inches(0)

    # 1. Rótulo 'Figura '
    run_lbl = p.add_run("Figura ")
    run_lbl.font.name = 'Times New Roman'
    run_lbl.font.size = Pt(10)
    run_lbl.font.bold = True

    # 2. Campo complejo SEQ Figura \* ARABIC con número en caché
    num_str = str(numero).lower().replace("figura", "").strip() if "figura" in str(numero).lower() else str(numero).strip()
    r_begin = parse_xml(r'<w:r %s><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>' % nsdecls('w'))
    p._p.append(r_begin)
    r_instr = parse_xml(r'<w:r %s><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:instrText xml:space="preserve"> SEQ Figura \* ARABIC </w:instrText></w:r>' % nsdecls('w'))
    p._p.append(r_instr)
    r_sep = parse_xml(r'<w:r %s><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>' % nsdecls('w'))
    p._p.append(r_sep)
    r_val = parse_xml(r'<w:r %s><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/><w:noProof/></w:rPr><w:t>%s</w:t></w:r>' % (nsdecls('w'), num_str))
    p._p.append(r_val)
    r_end = parse_xml(r'<w:r %s><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>' % nsdecls('w'))
    p._p.append(r_end)

    # 3. Separador y título en cursiva
    run_sep = p.add_run(" ")
    run_sep.font.name = 'Times New Roman'
    run_sep.font.size = Pt(10)

    run_tit = p.add_run(titulo)
    run_tit.font.name = 'Times New Roman'
    run_tit.font.size = Pt(10)
    run_tit.font.italic = True

    # 4. Imagen centrada
    p_img = doc.add_paragraph()
    p_img.paragraph_format.keep_with_next = True
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(4)
    p_img.paragraph_format.first_line_indent = Inches(0)
    if os.path.exists(ruta_imagen):
        ancho_final = min(float(ancho_in), 5.9)
        try:
            from PIL import Image
            with Image.open(ruta_imagen) as im:
                w_px, h_px = im.size
                if w_px > 0 and h_px > 0 and alto_max_in:
                    alto_estimado = ancho_final * (h_px / w_px)
                    if alto_estimado > alto_max_in:
                        ancho_final = alto_max_in * (w_px / h_px)
        except Exception:
            pass
        p_img.add_run().add_picture(ruta_imagen, width=Inches(ancho_final))
    else:
        run_alt = p_img.add_run(f"[RECURSO GRÁFICO OFICIAL: {os.path.basename(ruta_imagen)}]")
        run_alt.font.name = 'Times New Roman'
        run_alt.font.italic = True

    # 5. Nota de figura
    p_nota = doc.add_paragraph()
    p_nota.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_nota.paragraph_format.space_before = Pt(4)
    p_nota.paragraph_format.space_after = Pt(12)
    p_nota.paragraph_format.line_spacing = 1.0
    p_nota.paragraph_format.first_line_indent = Inches(0)
    nota_limpia = str(texto_nota).strip()
    if nota_limpia.startswith("Nota."):
        nota_limpia = nota_limpia[5:].strip()
    elif nota_limpia.startswith("*Nota.*"):
        nota_limpia = nota_limpia[7:].strip()
    run_n_lbl = p_nota.add_run("Nota. ")
    run_n_lbl.font.name = 'Times New Roman'
    run_n_lbl.font.size = Pt(9.5)
    run_n_lbl.font.italic = True
    for r_texto, r_bold, r_italic in procesar_formato_texto(nota_limpia):
        run_n_txt = p_nota.add_run(r_texto)
        run_n_txt.font.name = 'Times New Roman'
        run_n_txt.font.size = Pt(9.5)
        run_n_txt.font.bold = r_bold
        run_n_txt.font.italic = r_italic
    return p

def agregar_indice_contenido_nativo(doc):
    """
    Inserta un bloque <w:sdt> nativo de Word para Tabla de Contenido
    con instrucción de campo complejo: TOC \\o "1-3" \\h \\z \\u
    """
    p_temp = doc.add_paragraph()
    p_temp.paragraph_format.space_before = Pt(6)
    p_temp.paragraph_format.space_after = Pt(6)
    p_temp.paragraph_format.line_spacing = 1.15
    p_temp.paragraph_format.first_line_indent = Inches(0)

    sdt_xml = f"""<w:sdt {nsdecls('w')}>
      <w:sdtPr>
        <w:rPr>
          <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
          <w:sz w:val="24"/>
          <w:szCs w:val="24"/>
        </w:rPr>
        <w:docPartObj>
          <w:docPartGallery w:val="Table of Contents"/>
          <w:docPartUnique/>
        </w:docPartObj>
      </w:sdtPr>
      <w:sdtContent>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TDC1"/>
            <w:tabs>
              <w:tab w:val="right" w:leader="dot" w:pos="8921"/>
            </w:tabs>
            <w:spacing w:line="360" w:lineRule="auto" w:before="0" w:after="0"/>
            <w:ind w:firstLine="0" w:left="0" w:right="0"/>
          </w:pPr>
          <w:r><w:fldChar w:fldCharType="begin"/></w:r>
          <w:r><w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText></w:r>
          <w:r><w:fldChar w:fldCharType="separate"/></w:r>
          <w:r><w:fldChar w:fldCharType="end"/></w:r>
        </w:p>
      </w:sdtContent>
    </w:sdt>"""
    sdt_elem = parse_xml(sdt_xml)
    p_temp._p.addprevious(sdt_elem)
    doc._body._body.remove(p_temp._p)

def agregar_indice_tablas_nativo(doc):
    """
    Inserta el campo complejo nativo TOC \\h \\z \\c "Tabla" con tabulación derecha y puntos.
    """
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.first_line_indent = Inches(0)

    pPr = p._p.get_or_add_pPr()
    tabs_xml = parse_xml(r'<w:tabs %s><w:tab w:val="right" w:leader="dot" w:pos="8921"/></w:tabs>' % nsdecls('w'))
    pPr.append(tabs_xml)

    r_b = parse_xml(r'<w:r %s><w:fldChar w:fldCharType="begin"/></w:r>' % nsdecls('w'))
    r_i = parse_xml(r'<w:r %s><w:instrText xml:space="preserve"> TOC \h \z \c "Tabla" </w:instrText></w:r>' % nsdecls('w'))
    r_s = parse_xml(r'<w:r %s><w:fldChar w:fldCharType="separate"/></w:r>' % nsdecls('w'))
    r_e = parse_xml(r'<w:r %s><w:fldChar w:fldCharType="end"/></w:r>' % nsdecls('w'))
    p._p.append(r_b)
    p._p.append(r_i)
    p._p.append(r_s)
    p._p.append(r_e)
    return p

def agregar_indice_figuras_nativo(doc):
    """
    Inserta el campo complejo nativo TOC \\h \\z \\c "Figura" con tabulación derecha y puntos.
    """
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.first_line_indent = Inches(0)

    pPr = p._p.get_or_add_pPr()
    tabs_xml = parse_xml(r'<w:tabs %s><w:tab w:val="right" w:leader="dot" w:pos="8921"/></w:tabs>' % nsdecls('w'))
    pPr.append(tabs_xml)

    r_b = parse_xml(r'<w:r %s><w:fldChar w:fldCharType="begin"/></w:r>' % nsdecls('w'))
    r_i = parse_xml(r'<w:r %s><w:instrText xml:space="preserve"> TOC \h \z \c "Figura" </w:instrText></w:r>' % nsdecls('w'))
    r_s = parse_xml(r'<w:r %s><w:fldChar w:fldCharType="separate"/></w:r>' % nsdecls('w'))
    r_e = parse_xml(r'<w:r %s><w:fldChar w:fldCharType="end"/></w:r>' % nsdecls('w'))
    p._p.append(r_b)
    p._p.append(r_i)
    p._p.append(r_s)
    p._p.append(r_e)
    return p

def agregar_ecuacion_omml(doc, mathml_str, numero_eq=None):
    """Inserta un párrafo centrado con una ecuación OMML nativa de Word a partir de MathML."""
    from docx_quirurgico import mathml_to_omml
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.first_line_indent = Inches(0)
    omml_elem = mathml_to_omml(mathml_str)
    p._p.append(omml_elem)
    if numero_eq is not None:
        run_num = p.add_run(f"    ({numero_eq})")
        run_num.font.name = 'Times New Roman'
        run_num.font.size = Pt(12)
    return p

def habilitar_actualizacion_automatica_campos(doc):
    """Configura w:updateFields w:val='true' en word/settings.xml para que Word actualice campos al abrir."""
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls, qn
    settings_elm = doc.settings.element
    if settings_elm.find(qn('w:updateFields')) is None:
        settings_elm.append(parse_xml(r'<w:updateFields %s w:val="true"/>' % nsdecls('w')))

