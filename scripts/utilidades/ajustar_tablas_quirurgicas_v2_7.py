#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Ajuste Quirúrgico y Tipográfico Maestro Definitivo v2.7
Logra la maquetación perfecta de Tabla 12 en Landscape (Página 51):
  - Fórmulas inline integradas con texto en un mismo párrafo para máxima compacidad y legibilidad.
  - Tipografía Times New Roman 7.2 pt, interlineado natural y amplio (200 dxa = 10 pt).
  - Cero líneas superpuestas, cero cajas de caracteres extraños.
  - La Matriz de Consistencia completa (Filas 0-4) cabe en UNA SOLA PÁGINA (Página 51).
  - Encabezados claros: "HIPÓTESIS" con tilde.
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
    </math>"""
}

def create_p_inline(segments, font_size_pt=7.2, align="left", line_spacing=200, space_before=10, space_after=20):
    """
    Crea un párrafo en el que los segmentos pueden ser:
      - Tupla: (texto, negrita, cursiva)
      - Elemento OMML de fórmula (<m:oMath>)
    Permite combinar texto y fórmula en una sola línea fluida.
    """
    sz_val = str(int(font_size_pt * 2))
    p = parse_xml(r'''<w:p %s>
        <w:pPr>
            <w:spacing w:line="%d" w:lineRule="auto" w:before="%d" w:after="%d"/>
            <w:ind w:firstLine="0"/>
            <w:jc w:val="%s"/>
        </w:pPr>
    </w:p>''' % (nsdecls('w'), line_spacing, space_before, space_after, align))

    for seg in segments:
        if hasattr(seg, 'tag') and 'oMath' in seg.tag:
            p.append(seg)
        elif isinstance(seg, tuple):
            t_text = str(seg[0])
            t_bold = bool(seg[1]) if len(seg) > 1 else False
            t_italic = bool(seg[2]) if len(seg) > 2 else False
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
                        sz_val, t_text))
            p.append(r)
        else:
            t_text = str(seg)
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

    return p

def set_tc_paragraphs(tc, paragraphs):
    tcPr = tc.find(qn('w:tcPr'))
    for child in list(tc):
        if child.tag != qn('w:tcPr'):
            tc.remove(child)

    if not paragraphs:
        empty_p = parse_xml(r'<w:p %s><w:pPr><w:spacing w:line="180" w:before="0" w:after="0"/></w:pPr></w:p>' % nsdecls('w'))
        tc.append(empty_p)
        return

    for p in paragraphs:
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

    tblpPr = tblPr.find(qn('w:tblpPr'))
    if tblpPr is not None:
        tblPr.remove(tblpPr)

    for w in tblPr.findall(qn('w:tblW')):
        tblPr.remove(w)
    tblPr.append(parse_xml(r'<w:tblW %s w:w="%d" w:type="dxa"/>' % (nsdecls('w'), total_width_dxa)))

    for jc in tblPr.findall(qn('w:jc')):
        tblPr.remove(jc)
    tblPr.append(parse_xml(r'<w:jc %s w:val="%s"/>' % (nsdecls('w'), align)))

    for cm in tblPr.findall(qn('w:tblCellMar')):
        tblPr.remove(cm)
    tblPr.append(parse_xml(r'''<w:tblCellMar %s>
        <w:top w:w="30" w:type="dxa"/>
        <w:left w:w="50" w:type="dxa"/>
        <w:bottom w:w="30" w:type="dxa"/>
        <w:right w:w="50" w:type="dxa"/>
    </w:tblCellMar>''' % nsdecls('w')))

    tblGrid = table._tbl.tblGrid
    if tblGrid is not None:
        table._tbl.remove(tblGrid)
    new_grid = parse_xml(r'<w:tblGrid %s/>' % nsdecls('w'))
    for cw in col_widths_dxa:
        new_grid.append(parse_xml(r'<w:gridCol %s w:w="%d"/>' % (nsdecls('w'), cw)))
    tblPr_idx = list(table._tbl).index(tblPr)
    table._tbl.insert(tblPr_idx + 1, new_grid)

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
    print("Iniciando ajuste maestro de alta definición v2.7...")
    doc = docx.Document(DOC_PATH)

    # 1. Encabezados de Anexos
    p599 = doc.paragraphs[599]
    p599.paragraph_format.space_before = Pt(4)
    p599.paragraph_format.space_after = Pt(2)

    p600 = doc.paragraphs[600]
    p600.paragraph_format.space_before = Pt(2)
    p600.paragraph_format.space_after = Pt(4)

    # 2. TABLA 12: MATRIZ DE CONSISTENCIA
    t12 = doc.tables[11]
    # Ancho total: exactamente 14,000 dxa (24.70 cm)
    # Col 0 (VARIABLES): 1,250 dxa
    # Col 1 (PROBLEMAS): 2,350 dxa
    # Col 2 (OBJETIVOS): 2,350 dxa
    # Col 3 (HIPÓTESIS): 2,350 dxa
    # Col 4 (DIMENSIONES): 1,400 dxa
    # Col 5 (INDICADORES): 2,550 dxa
    # Col 6 (METODOLOGÍA): 1,750 dxa
    t12_cols = [1250, 2350, 2350, 2350, 1400, 2550, 1750]
    configure_table_geometry(t12, 14000, t12_cols)

    for r in t12.rows:
        set_row_properties(r._tr, cant_split=True, is_header=False)
    set_row_properties(t12.rows[0]._tr, cant_split=True, is_header=True)

    FS = 7.2
    LS = 200
    SB = 10
    SA = 20

    # Fila 0: Encabezados
    headers_t12 = ["VARIABLES", "PROBLEMAS", "OBJETIVOS", "HIPÓTESIS", "DIMENSIONES", "INDICADORES Y ESCALAS", "METODOLOGÍA"]
    tcs_12_0 = t12.rows[0]._tr.findall(qn('w:tc'))
    for c_idx, h_text in enumerate(headers_t12):
        set_tc_vmerge(tcs_12_0[c_idx], 'none')
        p = create_p_inline([(h_text, True, False)], font_size_pt=7.5, align="center", line_spacing=210, space_before=4, space_after=4)
        set_tc_paragraphs(tcs_12_0[c_idx], [p])

    # Fila 1: Variable Independiente
    tcs_12_1 = t12.rows[1]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_12_1[0], 'none')
    p_vi = [
        create_p_inline([("VARIABLE INDEPENDIENTE:", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=0),
        create_p_inline(["Sistema web SIVAC"], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_1[0], p_vi)

    set_tc_vmerge(tcs_12_1[1], 'none')
    p_pg = [
        create_p_inline([("Problema General:", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=0),
        create_p_inline(["¿En qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025?"], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_1[1], p_pg)

    set_tc_vmerge(tcs_12_1[2], 'none')
    p_og = [
        create_p_inline([("Objetivo General:", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=0),
        create_p_inline(["Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025."], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_1[2], p_og)

    set_tc_vmerge(tcs_12_1[3], 'none')
    p_hg = [
        create_p_inline([("Hipótesis General:", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=0),
        create_p_inline(["La aplicación del sistema \"SIVAC\" mejora significativamente la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025."], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_1[3], p_hg)

    set_tc_vmerge(tcs_12_1[4], 'none')
    p_dim_vi = [
        create_p_inline([("Implementación del sistema", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_1[4], p_dim_vi)

    set_tc_vmerge(tcs_12_1[5], 'none')
    p_ind_vi = [
        create_p_inline([("Condición operativa:", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=0),
        create_p_inline(["• Pretest: Sin sistema"], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=0),
        create_p_inline(["• Postest: Con sistema"], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=0),
        create_p_inline([("Escala: ", True, False), ("Dicotómica (0=Pre, 1=Post)", False, False)], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_1[5], p_ind_vi)

    set_tc_vmerge(tcs_12_1[6], 'restart')
    p_metod = [
        create_p_inline([("Tipo: ", True, False), ("Aplicada | ", False, False), ("Enfoque: ", True, False), ("Cuantitativo", False, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=0),
        create_p_inline([("Nivel: ", True, False), ("Explicativo | ", False, False), ("Diseño: ", True, False), ("Preexperimental", False, False)], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=0),
        create_p_inline([mathml_to_omml(FORMULAS_MML["diseno_preexp"])], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=0),
        create_p_inline([("Población y Muestra: ", True, False), ("Censal (N = n = 14)", False, False)], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_1[6], p_metod)

    # Fila 2: Variable Dependiente - Dimensión 1 (Oportunidad)
    tcs_12_2 = t12.rows[2]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_12_2[0], 'restart')
    p_vd = [
        create_p_inline([("VARIABLE DEPENDIENTE:", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=0),
        create_p_inline(["Gestión de movimientos de vacunas"], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_2[0], p_vd)

    set_tc_vmerge(tcs_12_2[1], 'none')
    p_pe1 = [
        create_p_inline([("Problema Específico 1:", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=0),
        create_p_inline(["¿En qué medida la aplicación del sistema \"SIVAC\" mejora la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II?"], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_2[1], p_pe1)

    set_tc_vmerge(tcs_12_2[2], 'none')
    p_oe1 = [
        create_p_inline([("Objetivo Específico 1:", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=0),
        create_p_inline(["Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II."], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_2[2], p_oe1)

    set_tc_vmerge(tcs_12_2[3], 'none')
    p_he1 = [
        create_p_inline([("Hipótesis Específica 1:", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=0),
        create_p_inline(["La aplicación del sistema \"SIVAC\" mejora significativamente la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II."], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_2[3], p_he1)

    set_tc_vmerge(tcs_12_2[4], 'none')
    p_dim_d1 = [
        create_p_inline([("Oportunidad de procesamiento", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_2[4], p_dim_d1)

    set_tc_vmerge(tcs_12_2[5], 'none')
    p_ind_d1 = [
        create_p_inline([
            ("Tiempo registro vacunas: ", True, False),
            mathml_to_omml(FORMULAS_MML["t_reg"]),
            (" (min) | Ficha cronométrica", False, False)
        ], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=6),
        create_p_inline([
            ("Tiempo emisión de vale: ", True, False),
            mathml_to_omml(FORMULAS_MML["t_vale"]),
            (" (min) | Ficha cronométrica", False, False)
        ], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_2[5], p_ind_d1)

    set_tc_vmerge(tcs_12_2[6], 'continue')
    set_tc_paragraphs(tcs_12_2[6], [])

    # Fila 3: Variable Dependiente - Dimensión 2 (Consistencia)
    tcs_12_3 = t12.rows[3]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_12_3[0], 'continue')
    set_tc_paragraphs(tcs_12_3[0], [])

    set_tc_vmerge(tcs_12_3[1], 'none')
    p_pe2 = [
        create_p_inline([("Problema Específico 2:", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=0),
        create_p_inline(["¿En qué medida la aplicación del sistema \"SIVAC\" mejora la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II?"], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_3[1], p_pe2)

    set_tc_vmerge(tcs_12_3[2], 'none')
    p_oe2 = [
        create_p_inline([("Objetivo Específico 2:", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=0),
        create_p_inline(["Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II."], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_3[2], p_oe2)

    set_tc_vmerge(tcs_12_3[3], 'none')
    p_he2 = [
        create_p_inline([("Hipótesis Específica 2:", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=0),
        create_p_inline(["La aplicación del sistema \"SIVAC\" mejora significativamente la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II."], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_3[3], p_he2)

    set_tc_vmerge(tcs_12_3[4], 'none')
    p_dim_d2 = [
        create_p_inline([("Consistencia documental", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_3[4], p_dim_d2)

    set_tc_vmerge(tcs_12_3[5], 'none')
    p_ind_d2 = [
        create_p_inline([
            ("Registros sin discrepancias: ", True, False),
            mathml_to_omml(FORMULAS_MML["rsd"]),
            (" | Ficha cotejo", False, False)
        ], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=6),
        create_p_inline([
            ("Concordancia programada/entregada: ", True, False),
            mathml_to_omml(FORMULAS_MML["cpe"]),
            (" | Ficha cotejo", False, False)
        ], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_3[5], p_ind_d2)

    set_tc_vmerge(tcs_12_3[6], 'continue')
    set_tc_paragraphs(tcs_12_3[6], [])

    # Fila 4: Variable Dependiente - Dimensión 3 (Satisfacción)
    tcs_12_4 = t12.rows[4]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_12_4[0], 'continue')
    set_tc_paragraphs(tcs_12_4[0], [])

    set_tc_vmerge(tcs_12_4[1], 'none')
    p_pe3 = [
        create_p_inline([("Problema Específico 3:", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=0),
        create_p_inline(["¿En qué medida la aplicación del sistema \"SIVAC\" mejora la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II?"], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_4[1], p_pe3)

    set_tc_vmerge(tcs_12_4[2], 'none')
    p_oe3 = [
        create_p_inline([("Objetivo Específico 3:", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=0),
        create_p_inline(["Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II."], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_4[2], p_oe3)

    set_tc_vmerge(tcs_12_4[3], 'none')
    p_he3 = [
        create_p_inline([("Hipótesis Específica 3:", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=0),
        create_p_inline(["La aplicación del sistema \"SIVAC\" mejora significativamente la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II."], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_4[3], p_he3)

    set_tc_vmerge(tcs_12_4[4], 'none')
    p_dim_d3 = [
        create_p_inline([("Satisfacción del usuario", True, False)], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_4[4], p_dim_d3)

    set_tc_vmerge(tcs_12_4[5], 'none')
    p_ind_d3 = [
        create_p_inline([
            ("Aceptación del proceso (AP): ", True, False),
            ("Escala Likert 1-5 (baremo 8-40)", False, False)
        ], font_size_pt=FS, line_spacing=LS, space_before=SB, space_after=4),
        create_p_inline([
            ("Utilidad percibida (UP): ", True, False),
            ("Escala Likert 1-5 (baremo 8-40)", False, False)
        ], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=4),
        create_p_inline([
            ("Instrumento: ", True, False),
            ("Cuestionario TAM (16 ítems)", False, False)
        ], font_size_pt=FS, line_spacing=LS, space_before=0, space_after=SA)
    ]
    set_tc_paragraphs(tcs_12_4[5], p_ind_d3)

    set_tc_vmerge(tcs_12_4[6], 'continue')
    set_tc_paragraphs(tcs_12_4[6], [])

    aplicar_bordes_apa7(t12)
    print("  [x] Tabla 12 reconfigurada con fórmulas inline perfectamente integradas.")

    doc.save(DOC_PATH)
    print(f"Documento guardado con éxito en {DOC_PATH}.")

if __name__ == "__main__":
    main()
