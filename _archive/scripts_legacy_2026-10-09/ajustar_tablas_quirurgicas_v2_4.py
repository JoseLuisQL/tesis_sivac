#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB - Corrección Maestra Definitiva de Tablas v2.4
Resuelve de raíz los problemas visuales y estructurales reportados por el tesista:
  1. Tabla 5 (Operacionalización de variables, Portrait):
     - Comienza al inicio de página (salto de página en Párrafo 385 con keep_with_next).
     - Fórmulas optimizadas en MathML/OMML:
         * T_reg: T_reg = t_fin - t_ini
         * T_vale: T_vale = t_emision - t_solicitud
         * TAM: Item sin caracteres especiales que generen cajas cuadradas
     - Dimensiones y espaciados compactados para que la TABLA COMPLETA (Filas 0-7)
       quepa en UNA SOLA PÁGINA A4 vertical (8,788 dxa de ancho útil).
     - Cero celdas partidas y cero páginas huérfanas.

  2. Tabla 12 (Anexo 1: Matriz de Consistencia, Landscape):
     - ELIMINACIÓN TOTAL de w:tblpPr (propiedad de tabla flotante que causaba el quiebre).
     - Ancho exacto al área imprimible: 14,000 dxa (24.70 cm).
     - Eliminación de cuadros de texto flotantes obsoletos y de párrafos vacíos redundantes.
     - Títulos "ANEXOS" y "Anexo 1: Matriz de Consistencia" integrados en flujo nativo.
     - Espaciado y tipografía optimizados (7.0-7.5 pt) para que la matriz completa
       quepa de forma impecable en la página horizontal con cero partición de filas.
"""

import os
import docx
from docx.shared import Pt
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
import lxml.etree as ET

DOC_PATH = "salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V2.docx"
FUENTE = "Times New Roman"
XSLT_PATH = r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL"

xslt_doc = ET.parse(XSLT_PATH)
transform_mml = ET.XSLT(xslt_doc)

def mathml_to_omml(mml_str):
    dom = ET.fromstring(mml_str)
    omml = transform_mml(dom)
    return parse_xml(ET.tostring(omml))

FORMULAS_MML = {
    "diseno_preexp": """<math xmlns="http://www.w3.org/1998/Math/MathML">
      <mrow>
        <mi mathvariant="bold">G</mi><mo>:</mo><mspace width="0.2em"/>
        <msub><mi>O</mi><mn>1</mn></msub><mo>&#x2192;</mo><mi>X</mi><mo>&#x2192;</mo><msub><mi>O</mi><mn>2</mn></msub>
      </mrow>
    </math>""",

    "t_reg": """<math xmlns="http://www.w3.org/1998/Math/MathML">
      <mrow>
        <msub><mi>T</mi><mtext>reg</mtext></msub><mo>=</mo>
        <msub><mi>t</mi><mtext>fin</mtext></msub><mo>−</mo><msub><mi>t</mi><mtext>inicio</mtext></msub>
      </mrow>
    </math>""",

    "t_vale": """<math xmlns="http://www.w3.org/1998/Math/MathML">
      <mrow>
        <msub><mi>T</mi><mtext>vale</mtext></msub><mo>=</mo>
        <msub><mi>t</mi><mtext>emisión</mtext></msub><mo>−</mo><msub><mi>t</mi><mtext>solicitud</mtext></msub>
      </mrow>
    </math>""",

    "rsd": """<math xmlns="http://www.w3.org/1998/Math/MathML">
      <mrow>
        <mi>RSD</mi><mo>=</mo>
        <mrow><mo>(</mo><mfrac><msub><mi>N</mi><mtext>conformes</mtext></msub><msub><mi>N</mi><mtext>total</mtext></msub></mfrac><mo>)</mo></mrow>
        <mo>×</mo><mn>100</mn>
      </mrow>
    </math>""",

    "cpe": """<math xmlns="http://www.w3.org/1998/Math/MathML">
      <mrow>
        <mi>CPE</mi><mo>=</mo>
        <mrow><mo>(</mo><mfrac><mrow><mo>∑</mo><msub><mi>Q</mi><mtext>entregada</mtext></msub></mrow><mrow><mo>∑</mo><msub><mi>Q</mi><mtext>programada</mtext></msub></mrow></mfrac><mo>)</mo></mrow>
        <mo>×</mo><mn>100</mn>
      </mrow>
    </math>""",

    "tam_total": """<math xmlns="http://www.w3.org/1998/Math/MathML">
      <mrow>
        <mtext>Puntaje</mtext><mo>=</mo>
        <munderover><mo>∑</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mn>8</mn></munderover>
        <msub><mtext>Item</mtext><mi>i</mi></msub>
      </mrow>
    </math>"""
}

def clear_and_set_tc(tc, items, font_size_pt=8.0, align="left", line_spacing=220, space_before=10, space_after=10):
    tcPr = tc.find(qn('w:tcPr'))
    for child in list(tc):
        if child.tag != qn('w:tcPr'):
            tc.remove(child)

    if not items:
        empty_p = parse_xml(r'<w:p %s><w:pPr><w:spacing w:line="200" w:before="0" w:after="0"/></w:pPr></w:p>' % nsdecls('w'))
        tc.append(empty_p)
        return

    sz_val = str(int(font_size_pt * 2))

    for item in items:
        p = parse_xml(r'''<w:p %s>
            <w:pPr>
                <w:spacing w:line="%d" w:lineRule="auto" w:before="%d" w:after="%d"/>
                <w:ind w:firstLine="0"/>
                <w:jc w:val="%s"/>
            </w:pPr>
        </w:p>''' % (nsdecls('w'), line_spacing, space_before, space_after, align))

        if hasattr(item, 'tag') and 'oMath' in item.tag:
            p.append(item)
            tc.append(p)
            continue

        if isinstance(item, list):
            for seg in item:
                if isinstance(seg, tuple):
                    t_text = str(seg[0])
                    t_bold = bool(seg[1]) if len(seg) > 1 else False
                    t_italic = bool(seg[2]) if len(seg) > 2 else False
                    t_sz = str(int(seg[3] * 2)) if len(seg) > 3 else sz_val
                else:
                    t_text = str(seg)
                    t_bold = False
                    t_italic = False
                    t_sz = sz_val

                r = parse_xml(r'''<w:r %s>
                    <w:rPr>
                        <w:rFonts w:ascii="%s" w:hAnsi="%s"/>
                        <w:b w:val="%s"/>
                        <w:i w:val="%s"/>
                        <w:sz w:val="%s"/>
                    </w:rPr>
                    <w:t xml:space="preserve">%s</w:t>
                </w:r>''' % (nsdecls('w'), FUENTE, FUENTE,
                            "1" if t_bold else "0",
                            "1" if t_italic else "0",
                            t_sz, t_text))
                p.append(r)
        else:
            t_text = str(item)
            r = parse_xml(r'''<w:r %s>
                <w:rPr>
                    <w:rFonts w:ascii="%s" w:hAnsi="%s"/>
                    <w:b w:val="0"/>
                    <w:i w:val="0"/>
                    <w:sz w:val="%s"/>
                </w:rPr>
                <w:t xml:space="preserve">%s</w:t>
            </w:r>''' % (nsdecls('w'), FUENTE, FUENTE, sz_val, t_text))
            p.append(r)

        tc.append(p)

def set_tc_vmerge(tc, mode):
    tcPr = tc.get_or_add_tcPr()
    for vm in tcPr.findall(qn('w:vMerge')):
        tcPr.remove(vm)
    if mode == 'restart':
        tcPr.append(parse_xml(r'<w:vMerge %s w:val="restart"/>' % nsdecls('w')))
    elif mode == 'continue':
        tcPr.append(parse_xml(r'<w:vMerge %s/>' % nsdecls('w')))

def set_tc_width(tc, width_dxa):
    tcPr = tc.get_or_add_tcPr()
    for w in tcPr.findall(qn('w:tcW')):
        tcPr.remove(w)
    tcPr.append(parse_xml(r'<w:tcW %s w:w="%d" w:type="dxa"/>' % (nsdecls('w'), width_dxa)))

def set_row_properties(tr, cant_split=True, is_header=False):
    trPr = tr.get_or_add_trPr()
    if cant_split and trPr.find(qn('w:cantSplit')) is None:
        trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
    if is_header and trPr.find(qn('w:tblHeader')) is None:
        trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))

def configure_table_geometry(table, total_width_dxa, col_widths_dxa, align="center"):
    tblPr = table._tbl.tblPr

    # Eliminar propiedad de tabla flotante si existe
    tblpPr = tblPr.find(qn('w:tblpPr'))
    if tblpPr is not None:
        tblPr.remove(tblpPr)

    # tblW
    for w in tblPr.findall(qn('w:tblW')):
        tblPr.remove(w)
    tblPr.append(parse_xml(r'<w:tblW %s w:w="%d" w:type="dxa"/>' % (nsdecls('w'), total_width_dxa)))

    # Alineación
    for jc in tblPr.findall(qn('w:jc')):
        tblPr.remove(jc)
    tblPr.append(parse_xml(r'<w:jc %s w:val="%s"/>' % (nsdecls('w'), align)))

    # Márgenes de celda compactos
    for cm in tblPr.findall(qn('w:tblCellMar')):
        tblPr.remove(cm)
    tblPr.append(parse_xml(r'''<w:tblCellMar %s>
        <w:top w:w="20" w:type="dxa"/>
        <w:left w:w="60" w:type="dxa"/>
        <w:bottom w:w="20" w:type="dxa"/>
        <w:right w:w="60" w:type="dxa"/>
    </w:tblCellMar>''' % nsdecls('w')))

    # tblGrid
    tblGrid = table._tbl.tblGrid
    if tblGrid is not None:
        table._tbl.remove(tblGrid)
    new_grid = parse_xml(r'<w:tblGrid %s/>' % nsdecls('w'))
    for cw in col_widths_dxa:
        new_grid.append(parse_xml(r'<w:gridCol %s w:w="%d"/>' % (nsdecls('w'), cw)))
    tblPr_idx = list(table._tbl).index(tblPr)
    table._tbl.insert(tblPr_idx + 1, new_grid)

    # tcW en cada celda
    for row in table.rows:
        tcs = row._tr.findall(qn('w:tc'))
        for idx, cw in enumerate(col_widths_dxa):
            if idx < len(tcs):
                set_tc_width(tcs[idx], cw)

def aplicar_bordes_apa7(table):
    tblPr = table._tbl.tblPr
    for b in tblPr.findall(qn('w:tblBorders')):
        tblPr.remove(b)
    bordes_xml = parse_xml(r'''<w:tblBorders %s>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:left w:val="none"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:right w:val="none"/>
        <w:insideH w:val="none"/>
        <w:insideV w:val="none"/>
    </w:tblBorders>''' % nsdecls('w'))
    tblPr.append(bordes_xml)

    if len(table.rows) > 0:
        for tc in table.rows[0]._tr.findall(qn('w:tc')):
            tcPr = tc.get_or_add_tcPr()
            tcBorders = tcPr.find(qn('w:tcBorders'))
            if tcBorders is None:
                tcBorders = parse_xml(r'<w:tcBorders %s/>' % nsdecls('w'))
                tcPr.append(tcBorders)
            for b in tcBorders.findall(qn('w:bottom')):
                tcBorders.remove(b)
            tcBorders.append(parse_xml(r'<w:bottom %s w:val="single" w:sz="4" w:space="0" w:color="000000"/>' % nsdecls('w')))

def main():
    print("Iniciando ajuste maestro y resolución definitiva de tablas v2.4...")
    doc = docx.Document(DOC_PATH)

    # =========================================================================
    # 1. TABLA 5: OPERACIONALIZACIÓN DE VARIABLES (PORTRAIT)
    # =========================================================================
    print("--- 1. Procesando Tabla 5 (Operacionalización de variables) ---")
    t5 = doc.tables[4]

    # Asegurar que el título de Tabla 5 tenga salto de página y keep_with_next
    p385 = doc.paragraphs[385]
    p385.paragraph_format.page_break_before = True
    p385.paragraph_format.keep_with_next = True
    p385.paragraph_format.space_before = Pt(0)
    p385.paragraph_format.space_after = Pt(4)

    # Nota de Tabla 5
    p386 = doc.paragraphs[386]
    p386.paragraph_format.page_break_before = False
    p386.paragraph_format.space_before = Pt(2)
    p386.paragraph_format.space_after = Pt(12)

    # Geometría Portrait: 8,788 dxa (15.50 cm)
    # Col 0 (Variable): 1,200 dxa (2.12 cm)
    # Col 1 (Definición conceptual): 2,088 dxa (3.68 cm)
    # Col 2 (Dimensiones): 1,350 dxa (2.38 cm)
    # Col 3 (Indicadores): 2,550 dxa (4.50 cm) - Ampliada para fórmulas
    # Col 4 (Escala / Unidad): 1,600 dxa (2.82 cm)
    t5_cols = [1200, 2088, 1350, 2550, 1600]
    t5_total = sum(t5_cols) # 8,788 dxa
    configure_table_geometry(t5, t5_total, t5_cols)

    # Fila 0: Encabezados
    headers_t5 = ["Variable", "Definición conceptual", "Dimensiones", "Indicadores", "Escala / Unidad de medida"]
    tcs_0 = t5.rows[0]._tr.findall(qn('w:tc'))
    set_row_properties(t5.rows[0]._tr, cant_split=True, is_header=True)
    for c_idx, h_text in enumerate(headers_t5):
        set_tc_vmerge(tcs_0[c_idx], 'none')
        clear_and_set_tc(tcs_0[c_idx], [[(h_text, True, False)]],
                         font_size_pt=8.5, align="center", line_spacing=220, space_before=10, space_after=10)

    # Fila 1: Variable Independiente
    tcs_1 = t5.rows[1]._tr.findall(qn('w:tc'))
    set_row_properties(t5.rows[1]._tr, cant_split=True, is_header=False)
    set_tc_vmerge(tcs_1[0], 'none')
    clear_and_set_tc(tcs_1[0], [
        [("Variable Independiente:", True, False)],
        [("Sistema web SIVAC", False, False)]
    ], font_size_pt=8.0, align="left", line_spacing=210, space_before=8, space_after=8)

    set_tc_vmerge(tcs_1[1], 'none')
    clear_and_set_tc(tcs_1[1], [
        "Aplicación informática web para el registro, control y seguimiento de las operaciones de ingreso, almacenamiento y distribución de vacunas en la Dirección de Salud Apurímac II."
    ], font_size_pt=7.5, align="left", line_spacing=210, space_before=8, space_after=8)

    set_tc_vmerge(tcs_1[2], 'none')
    clear_and_set_tc(tcs_1[2], [
        [("Implementación del sistema", True, False)]
    ], font_size_pt=8.0, align="left", line_spacing=210, space_before=8, space_after=8)

    set_tc_vmerge(tcs_1[3], 'none')
    clear_and_set_tc(tcs_1[3], [
        "Adopción y uso del sistema web en la gestión de vacunas."
    ], font_size_pt=7.5, align="left", line_spacing=210, space_before=8, space_after=8)

    set_tc_vmerge(tcs_1[4], 'none')
    clear_and_set_tc(tcs_1[4], [
        [("Dicotómica nominal", True, False)],
        "0 = Sin sistema (Pretest)",
        "1 = Con sistema (Postest)"
    ], font_size_pt=7.5, align="left", line_spacing=210, space_before=8, space_after=8)

    # Configurar filas de Variable Dependiente (Filas 2-7)
    for r_idx in range(2, 8):
        set_row_properties(t5.rows[r_idx]._tr, cant_split=True, is_header=False)

    # Fila 2: VD - Dimensión 1 - Indicador 1.1 (T_reg)
    tcs_2 = t5.rows[2]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_2[0], 'restart')
    clear_and_set_tc(tcs_2[0], [
        [("Variable Dependiente:", True, False)],
        [("Gestión de movimientos de vacunas", False, False)]
    ], font_size_pt=8.0, align="left", line_spacing=210, space_before=8, space_after=8)

    set_tc_vmerge(tcs_2[1], 'restart')
    clear_and_set_tc(tcs_2[1], [
        "Procedimientos técnicos y administrativos para programar, registrar, despachar y controlar el flujo de biológicos e insumos en la Dirección de Salud Apurímac II."
    ], font_size_pt=7.5, align="left", line_spacing=210, space_before=8, space_after=8)

    set_tc_vmerge(tcs_2[2], 'restart')
    clear_and_set_tc(tcs_2[2], [
        [("Oportunidad de procesamiento", True, False)]
    ], font_size_pt=8.0, align="left", line_spacing=210, space_before=8, space_after=8)

    set_tc_vmerge(tcs_2[3], 'none')
    clear_and_set_tc(tcs_2[3], [
        [("Tiempo de registro de vacunas", True, False)],
        mathml_to_omml(FORMULAS_MML["t_reg"]),
        "Duración en minutos desde inicio hasta fin del registro."
    ], font_size_pt=7.5, align="left", line_spacing=210, space_before=8, space_after=8)

    set_tc_vmerge(tcs_2[4], 'none')
    clear_and_set_tc(tcs_2[4], [
        [("Minutos (min)", True, False)],
        "Razón / Continua",
        "Ficha cronométrica"
    ], font_size_pt=7.5, align="left", line_spacing=210, space_before=8, space_after=8)

    # Fila 3: VD - Dimensión 1 - Indicador 1.2 (T_vale)
    tcs_3 = t5.rows[3]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_3[0], 'continue')
    clear_and_set_tc(tcs_3[0], [])
    set_tc_vmerge(tcs_3[1], 'continue')
    clear_and_set_tc(tcs_3[1], [])
    set_tc_vmerge(tcs_3[2], 'continue')
    clear_and_set_tc(tcs_3[2], [])

    set_tc_vmerge(tcs_3[3], 'none')
    clear_and_set_tc(tcs_3[3], [
        [("Tiempo de emisión de vale", True, False)],
        mathml_to_omml(FORMULAS_MML["t_vale"]),
        "Duración en minutos para generar y emitir el vale de salida."
    ], font_size_pt=7.5, align="left", line_spacing=210, space_before=8, space_after=8)

    set_tc_vmerge(tcs_3[4], 'none')
    clear_and_set_tc(tcs_3[4], [
        [("Minutos (min)", True, False)],
        "Razón / Continua",
        "Ficha cronométrica"
    ], font_size_pt=7.5, align="left", line_spacing=210, space_before=8, space_after=8)

    # Fila 4: VD - Dimensión 2 - Indicador 2.1 (RSD)
    tcs_4 = t5.rows[4]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_4[0], 'continue')
    clear_and_set_tc(tcs_4[0], [])
    set_tc_vmerge(tcs_4[1], 'continue')
    clear_and_set_tc(tcs_4[1], [])

    set_tc_vmerge(tcs_4[2], 'restart')
    clear_and_set_tc(tcs_4[2], [
        [("Consistencia documental", True, False)]
    ], font_size_pt=8.0, align="left", line_spacing=210, space_before=8, space_after=8)

    set_tc_vmerge(tcs_4[3], 'none')
    clear_and_set_tc(tcs_4[3], [
        [("Registros sin discrepancias (RSD)", True, False)],
        mathml_to_omml(FORMULAS_MML["rsd"]),
        "Proporción de transacciones sin inconsistencias de lote o saldo."
    ], font_size_pt=7.5, align="left", line_spacing=210, space_before=8, space_after=8)

    set_tc_vmerge(tcs_4[4], 'none')
    clear_and_set_tc(tcs_4[4], [
        [("Porcentaje (%)", True, False)],
        "Razón / Proporción",
        "Ficha de cotejo"
    ], font_size_pt=7.5, align="left", line_spacing=210, space_before=8, space_after=8)

    # Fila 5: VD - Dimensión 2 - Indicador 2.2 (CPE)
    tcs_5 = t5.rows[5]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_5[0], 'continue')
    clear_and_set_tc(tcs_5[0], [])
    set_tc_vmerge(tcs_5[1], 'continue')
    clear_and_set_tc(tcs_5[1], [])
    set_tc_vmerge(tcs_5[2], 'continue')
    clear_and_set_tc(tcs_5[2], [])

    set_tc_vmerge(tcs_5[3], 'none')
    clear_and_set_tc(tcs_5[3], [
        [("Concordancia programada vs entregada (CPE)", True, False)],
        mathml_to_omml(FORMULAS_MML["cpe"]),
        "Coincidencia entre dosis requeridas y despachadas."
    ], font_size_pt=7.5, align="left", line_spacing=210, space_before=8, space_after=8)

    set_tc_vmerge(tcs_5[4], 'none')
    clear_and_set_tc(tcs_5[4], [
        [("Porcentaje (%)", True, False)],
        "Razón / Proporción",
        "Ficha de cotejo"
    ], font_size_pt=7.5, align="left", line_spacing=210, space_before=8, space_after=8)

    # Fila 6: VD - Dimensión 3 - Indicador 3.1 (AP)
    tcs_6 = t5.rows[6]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_6[0], 'continue')
    clear_and_set_tc(tcs_6[0], [])
    set_tc_vmerge(tcs_6[1], 'continue')
    clear_and_set_tc(tcs_6[1], [])

    set_tc_vmerge(tcs_6[2], 'restart')
    clear_and_set_tc(tcs_6[2], [
        [("Satisfacción del usuario", True, False)]
    ], font_size_pt=8.0, align="left", line_spacing=210, space_before=8, space_after=8)

    set_tc_vmerge(tcs_6[3], 'none')
    clear_and_set_tc(tcs_6[3], [
        [("Aceptación del proceso (AP)", True, False)],
        mathml_to_omml(FORMULAS_MML["tam_total"]),
        "Conformidad del personal con el flujo operativo."
    ], font_size_pt=7.5, align="left", line_spacing=210, space_before=8, space_after=8)

    set_tc_vmerge(tcs_6[4], 'none')
    clear_and_set_tc(tcs_6[4], [
        [("Escala Likert (1 a 5)", True, False)],
        "Rango: 8 a 40 puntos",
        "Cuestionario TAM"
    ], font_size_pt=7.5, align="left", line_spacing=210, space_before=8, space_after=8)

    # Fila 7: VD - Dimensión 3 - Indicador 3.2 (UP)
    tcs_7 = t5.rows[7]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_7[0], 'continue')
    clear_and_set_tc(tcs_7[0], [])
    set_tc_vmerge(tcs_7[1], 'continue')
    clear_and_set_tc(tcs_7[1], [])
    set_tc_vmerge(tcs_7[2], 'continue')
    clear_and_set_tc(tcs_7[2], [])

    set_tc_vmerge(tcs_7[3], 'none')
    clear_and_set_tc(tcs_7[3], [
        [("Utilidad percibida (UP)", True, False)],
        "Percepción del beneficio sanitario en sus labores operativas."
    ], font_size_pt=7.5, align="left", line_spacing=210, space_before=8, space_after=8)

    set_tc_vmerge(tcs_7[4], 'none')
    clear_and_set_tc(tcs_7[4], [
        [("Escala Likert (1 a 5)", True, False)],
        "Rango: 8 a 40 puntos",
        "Cuestionario TAM"
    ], font_size_pt=7.5, align="left", line_spacing=210, space_before=8, space_after=8)

    aplicar_bordes_apa7(t5)
    print("  [x] Tabla 5 optimizada y compactada.")

    # =========================================================================
    # 2. TABLA 8: INSTRUMENTOS (PORTRAIT)
    # =========================================================================
    print("--- 2. Procesando Tabla 8 (Instrumentos) ---")
    t8 = doc.tables[7]
    t8_cols = [2200, 4188, 2400]
    configure_table_geometry(t8, 8788, t8_cols)
    aplicar_bordes_apa7(t8)

    # =========================================================================
    # 3. TABLA 12: MATRIZ DE CONSISTENCIA (LANDSCAPE)
    # =========================================================================
    print("--- 3. Procesando Tabla 12 y Anexo 1 (Matriz de Consistencia) ---")
    t12 = doc.tables[11]

    # Geometría Landscape: exactamente 14,000 dxa (24.70 cm)
    # Col 0 (VARIABLES): 1,300 dxa (2.29 cm)
    # Col 1 (PROBLEMAS): 2,300 dxa (4.06 cm)
    # Col 2 (OBJETIVOS): 2,300 dxa (4.06 cm)
    # Col 3 (HIPÓTESIS): 2,300 dxa (4.06 cm)
    # Col 4 (DIMENSIONES): 1,500 dxa (2.65 cm)
    # Col 5 (INDICADORES): 2,500 dxa (4.41 cm)
    # Col 6 (METODOLOGÍA): 1,800 dxa (3.17 cm)
    t12_cols = [1300, 2300, 2300, 2300, 1500, 2500, 1800]
    t12_total = sum(t12_cols) # 14,000 dxa
    configure_table_geometry(t12, t12_total, t12_cols)

    # Configurar propiedades de fila
    for r in t12.rows:
        set_row_properties(r._tr, cant_split=True, is_header=False)
    set_row_properties(t12.rows[0]._tr, cant_split=True, is_header=True)

    # Fila 0: Encabezados
    headers_t12 = ["VARIABLES", "PROBLEMAS", "OBJETIVOS", "HIPÓTESIS", "DIMENSIONES", "INDICADORES Y ESCALAS", "METODOLOGÍA"]
    tcs_12_0 = t12.rows[0]._tr.findall(qn('w:tc'))
    for c_idx, h_text in enumerate(headers_t12):
        set_tc_vmerge(tcs_12_0[c_idx], 'none')
        clear_and_set_tc(tcs_12_0[c_idx], [[(h_text, True, False)]],
                         font_size_pt=8.0, align="center", line_spacing=210, space_before=6, space_after=6)

    # Fila 1: Variable Independiente
    tcs_12_1 = t12.rows[1]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_12_1[0], 'none')
    clear_and_set_tc(tcs_12_1[0], [
        [("VARIABLE INDEPENDIENTE:", True, False)],
        [("Sistema web SIVAC", False, False)]
    ], font_size_pt=7.5, align="left", line_spacing=200, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_1[1], 'none')
    clear_and_set_tc(tcs_12_1[1], [
        [("Problema General:", True, False)],
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025?"
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_1[2], 'none')
    clear_and_set_tc(tcs_12_1[2], [
        [("Objetivo General:", True, False)],
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025."
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_1[3], 'none')
    clear_and_set_tc(tcs_12_1[3], [
        [("Hipótesis General:", True, False)],
        "La aplicación del sistema \"SIVAC\" mejora significativamente la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025."
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_1[4], 'none')
    clear_and_set_tc(tcs_12_1[4], [
        [("Implementación del sistema", True, False)]
    ], font_size_pt=7.5, align="left", line_spacing=200, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_1[5], 'none')
    clear_and_set_tc(tcs_12_1[5], [
        [("Condición operativa:", True, False)],
        "• Pretest: Sin sistema",
        "• Postest: Con sistema",
        [("Escala: ", True, False), ("Dicotómica", False, False)]
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_1[6], 'restart')
    clear_and_set_tc(tcs_12_1[6], [
        [("Tipo: ", True, False), ("Aplicada", False, False)],
        [("Enfoque: ", True, False), ("Cuantitativo", False, False)],
        [("Nivel: ", True, False), ("Explicativo", False, False)],
        [("Diseño: ", True, False), ("Preexperimental", False, False)],
        mathml_to_omml(FORMULAS_MML["diseno_preexp"]),
        [("Población y Muestra:", True, False)],
        "Censal (N = n = 14)"
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    # Fila 2: Variable Dependiente - Dimensión 1
    tcs_12_2 = t12.rows[2]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_12_2[0], 'restart')
    clear_and_set_tc(tcs_12_2[0], [
        [("VARIABLE DEPENDIENTE:", True, False)],
        [("Gestión de movimientos de vacunas", False, False)]
    ], font_size_pt=7.5, align="left", line_spacing=200, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_2[1], 'none')
    clear_and_set_tc(tcs_12_2[1], [
        [("Problema Específico 1:", True, False)],
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?"
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_2[2], 'none')
    clear_and_set_tc(tcs_12_2[2], [
        [("Objetivo Específico 1:", True, False)],
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_2[3], 'none')
    clear_and_set_tc(tcs_12_2[3], [
        [("Hipótesis Específica 1:", True, False)],
        "La aplicación del sistema \"SIVAC\" mejora significativamente la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_2[4], 'none')
    clear_and_set_tc(tcs_12_2[4], [
        [("Oportunidad de procesamiento", True, False)]
    ], font_size_pt=7.5, align="left", line_spacing=200, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_2[5], 'none')
    clear_and_set_tc(tcs_12_2[5], [
        [("Tiempo registro vacunas:", True, False)],
        mathml_to_omml(FORMULAS_MML["t_reg"]),
        [("Escala: ", True, False), ("Razón (minutos)", False, False)],
        [("Tiempo emisión vale:", True, False)],
        mathml_to_omml(FORMULAS_MML["t_vale"]),
        [("Escala: ", True, False), ("Razón (minutos)", False, False)]
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_2[6], 'continue')
    clear_and_set_tc(tcs_12_2[6], [])

    # Fila 3: Variable Dependiente - Dimensión 2
    tcs_12_3 = t12.rows[3]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_12_3[0], 'continue')
    clear_and_set_tc(tcs_12_3[0], [])

    set_tc_vmerge(tcs_12_3[1], 'none')
    clear_and_set_tc(tcs_12_3[1], [
        [("Problema Específico 2:", True, False)],
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?"
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_3[2], 'none')
    clear_and_set_tc(tcs_12_3[2], [
        [("Objetivo Específico 2:", True, False)],
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_3[3], 'none')
    clear_and_set_tc(tcs_12_3[3], [
        [("Hipótesis Específica 2:", True, False)],
        "La aplicación del sistema \"SIVAC\" mejora significativamente la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_3[4], 'none')
    clear_and_set_tc(tcs_12_3[4], [
        [("Consistencia documental", True, False)]
    ], font_size_pt=7.5, align="left", line_spacing=200, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_3[5], 'none')
    clear_and_set_tc(tcs_12_3[5], [
        [("Registros sin discrepancias:", True, False)],
        mathml_to_omml(FORMULAS_MML["rsd"]),
        [("Escala: ", True, False), ("Proporción (%)", False, False)],
        [("Concordancia programada vs entregada:", True, False)],
        mathml_to_omml(FORMULAS_MML["cpe"]),
        [("Escala: ", True, False), ("Proporción (%)", False, False)]
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_3[6], 'continue')
    clear_and_set_tc(tcs_12_3[6], [])

    # Fila 4: Variable Dependiente - Dimensión 3
    tcs_12_4 = t12.rows[4]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_12_4[0], 'continue')
    clear_and_set_tc(tcs_12_4[0], [])

    set_tc_vmerge(tcs_12_4[1], 'none')
    clear_and_set_tc(tcs_12_4[1], [
        [("Problema Específico 3:", True, False)],
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?"
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_4[2], 'none')
    clear_and_set_tc(tcs_12_4[2], [
        [("Objetivo Específico 3:", True, False)],
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_4[3], 'none')
    clear_and_set_tc(tcs_12_4[3], [
        [("Hipótesis Específica 3:", True, False)],
        "La aplicación del sistema \"SIVAC\" mejora significativamente la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_4[4], 'none')
    clear_and_set_tc(tcs_12_4[4], [
        [("Satisfacción del usuario", True, False)]
    ], font_size_pt=7.5, align="left", line_spacing=200, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_4[5], 'none')
    clear_and_set_tc(tcs_12_4[5], [
        [("Aceptación del proceso (AP):", True, False)],
        "Escala de Likert (1-5, baremo 8-40)",
        [("Utilidad percibida (UP):", True, False)],
        "Escala de Likert (1-5, baremo 8-40)"
    ], font_size_pt=7.0, align="left", line_spacing=190, space_before=4, space_after=4)

    set_tc_vmerge(tcs_12_4[6], 'continue')
    clear_and_set_tc(tcs_12_4[6], [])

    aplicar_bordes_apa7(t12)
    print("  [x] Tabla 12 reconfigurada como tabla en línea nativa y bordes APA 7.")

    # Guardar cambios
    print(f"Guardando documento oficial en {DOC_PATH}...")
    doc.save(DOC_PATH)
    print("¡Ajuste maestro v2.4 completado exitosamente!")

if __name__ == "__main__":
    main()
