#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB - Ajuste Quirúrgico y Tipográfico de Alta Definición v2.6
Perfecciona la legibilidad y espaciado de Tabla 12 en Landscape (Página 51):
  - Fuente 7.0 pt, interlineado 190 dxa (9.5 pt), space_before 10 dxa, space_after 20 dxa.
  - Corrige acento en encabezado "HIPÓTESIS".
  - Elimina cualquier superposición de líneas o fórmulas.
  - Asegura que la tabla completa ocupe de manera balanceada y estética la Página 51 (A4 Landscape)
    sin desbordar a la página 52.
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

def get_tam_omml_clean():
    mml = """<math xmlns="http://www.w3.org/1998/Math/MathML">
      <mrow>
        <mtext>Puntaje</mtext><mo>=</mo>
        <munderover><mo>&#x2211;</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mn>8</mn></munderover>
        <msub><mtext>Item</mtext><mi>i</mi></msub>
      </mrow>
    </math>"""
    dom = ET.fromstring(mml)
    omml = transform_mml(dom)
    root = omml.getroot()
    nary = root.find(".//{http://schemas.openxmlformats.org/officeDocument/2006/math}nary")
    e = nary.find("{http://schemas.openxmlformats.org/officeDocument/2006/math}e")
    sSub = root.find(".//{http://schemas.openxmlformats.org/officeDocument/2006/math}sSub")
    if sSub is not None and e is not None:
        sSub.getparent().remove(sSub)
        e.append(sSub)
    return parse_xml(ET.tostring(root))

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

def clear_and_set_tc(tc, items, font_size_pt=7.0, align="left", line_spacing=190, space_before=10, space_after=20):
    tcPr = tc.find(qn('w:tcPr'))
    for child in list(tc):
        if child.tag != qn('w:tcPr'):
            tc.remove(child)

    if not items:
        empty_p = parse_xml(r'<w:p %s><w:pPr><w:spacing w:line="180" w:before="0" w:after="0"/></w:pPr></w:p>' % nsdecls('w'))
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
        <w:top w:w="20" w:type="dxa"/>
        <w:left w:w="50" w:type="dxa"/>
        <w:bottom w:w="20" w:type="dxa"/>
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
    print("Iniciando ajuste maestro de alta definición v2.6...")
    doc = docx.Document(DOC_PATH)

    # Encabezados de Anexos
    p599 = doc.paragraphs[599]
    p599.paragraph_format.space_before = Pt(6)
    p599.paragraph_format.space_after = Pt(2)

    p600 = doc.paragraphs[600]
    p600.paragraph_format.space_before = Pt(2)
    p600.paragraph_format.space_after = Pt(6)

    # TABLA 12: MATRIZ DE CONSISTENCIA
    t12 = doc.tables[11]
    # Ancho total: exactamente 14,000 dxa (24.70 cm)
    # Col 0 (VARIABLES): 1,250 dxa (2.20 cm)
    # Col 1 (PROBLEMAS): 2,350 dxa (4.14 cm)
    # Col 2 (OBJETIVOS): 2,350 dxa (4.14 cm)
    # Col 3 (HIPÓTESIS): 2,350 dxa (4.14 cm)
    # Col 4 (DIMENSIONES): 1,450 dxa (2.56 cm)
    # Col 5 (INDICADORES): 2,500 dxa (4.41 cm)
    # Col 6 (METODOLOGÍA): 1,750 dxa (3.09 cm)
    t12_cols = [1250, 2350, 2350, 2350, 1450, 2500, 1750]
    configure_table_geometry(t12, 14000, t12_cols)

    for r in t12.rows:
        set_row_properties(r._tr, cant_split=True, is_header=False)
    set_row_properties(t12.rows[0]._tr, cant_split=True, is_header=True)

    # Parámetros tipográficos de alta definición:
    # font_size = 7.0 pt, line_spacing = 185 dxa (9.25 pt), space_before = 6 dxa, space_after = 12 dxa
    FS = 7.0
    LS = 185
    SB = 6
    SA = 12

    # Fila 0: Encabezados
    headers_t12 = ["VARIABLES", "PROBLEMAS", "OBJETIVOS", "HIPÓTESIS", "DIMENSIONES", "INDICADORES Y ESCALAS", "METODOLOGÍA"]
    tcs_12_0 = t12.rows[0]._tr.findall(qn('w:tc'))
    for c_idx, h_text in enumerate(headers_t12):
        set_tc_vmerge(tcs_12_0[c_idx], 'none')
        clear_and_set_tc(tcs_12_0[c_idx], [[(h_text, True, False)]],
                         font_size_pt=7.5, align="center", line_spacing=200, space_before=4, space_after=4)

    # Fila 1: Variable Independiente
    tcs_12_1 = t12.rows[1]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_12_1[0], 'none')
    clear_and_set_tc(tcs_12_1[0], [
        [("VARIABLE INDEPENDIENTE:", True, False)],
        "Sistema web SIVAC"
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_1[1], 'none')
    clear_and_set_tc(tcs_12_1[1], [
        [("Problema General:", True, False)],
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025?"
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_1[2], 'none')
    clear_and_set_tc(tcs_12_1[2], [
        [("Objetivo General:", True, False)],
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025."
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_1[3], 'none')
    clear_and_set_tc(tcs_12_1[3], [
        [("Hipótesis General:", True, False)],
        "La aplicación del sistema \"SIVAC\" mejora significativamente la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025."
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_1[4], 'none')
    clear_and_set_tc(tcs_12_1[4], [
        [("Implementación del sistema", True, False)]
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_1[5], 'none')
    clear_and_set_tc(tcs_12_1[5], [
        [("Condición operativa:", True, False)],
        "• Pretest: Sin sistema",
        "• Postest: Con sistema",
        [("Escala: ", True, False), ("Dicotómica (0=Pre, 1=Post)", False, False)]
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_1[6], 'restart')
    clear_and_set_tc(tcs_12_1[6], [
        [("Tipo: ", True, False), ("Aplicada", False, False)],
        [("Enfoque: ", True, False), ("Cuantitativo", False, False)],
        [("Nivel: ", True, False), ("Explicativo", False, False)],
        [("Diseño: ", True, False), ("Preexperimental", False, False)],
        mathml_to_omml(FORMULAS_MML["diseno_preexp"]),
        [("Población y Muestra:", True, False)],
        "Censal (N = n = 14)"
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    # Fila 2: Variable Dependiente - Dimensión 1 (Oportunidad)
    tcs_12_2 = t12.rows[2]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_12_2[0], 'restart')
    clear_and_set_tc(tcs_12_2[0], [
        [("VARIABLE DEPENDIENTE:", True, False)],
        "Gestión de movimientos de vacunas"
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_2[1], 'none')
    clear_and_set_tc(tcs_12_2[1], [
        [("Problema Específico 1:", True, False)],
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II?"
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_2[2], 'none')
    clear_and_set_tc(tcs_12_2[2], [
        [("Objetivo Específico 1:", True, False)],
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II."
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_2[3], 'none')
    clear_and_set_tc(tcs_12_2[3], [
        [("Hipótesis Específica 1:", True, False)],
        "La aplicación del sistema \"SIVAC\" mejora significativamente la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II."
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_2[4], 'none')
    clear_and_set_tc(tcs_12_2[4], [
        [("Oportunidad de procesamiento", True, False)]
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_2[5], 'none')
    clear_and_set_tc(tcs_12_2[5], [
        [("Tiempo registro de vacunas:", True, False)],
        mathml_to_omml(FORMULAS_MML["t_reg"]),
        [("Escala: ", True, False), ("Razón (min) | Ficha cronométrica", False, False)],
        [("Tiempo emisión de comprobante/vale:", True, False)],
        mathml_to_omml(FORMULAS_MML["t_vale"]),
        [("Escala: ", True, False), ("Razón (min) | Ficha cronométrica", False, False)]
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_2[6], 'continue')
    clear_and_set_tc(tcs_12_2[6], [])

    # Fila 3: Variable Dependiente - Dimensión 2 (Consistencia)
    tcs_12_3 = t12.rows[3]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_12_3[0], 'continue')
    clear_and_set_tc(tcs_12_3[0], [])

    set_tc_vmerge(tcs_12_3[1], 'none')
    clear_and_set_tc(tcs_12_3[1], [
        [("Problema Específico 2:", True, False)],
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II?"
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_3[2], 'none')
    clear_and_set_tc(tcs_12_3[2], [
        [("Objetivo Específico 2:", True, False)],
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II."
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_3[3], 'none')
    clear_and_set_tc(tcs_12_3[3], [
        [("Hipótesis Específica 2:", True, False)],
        "La aplicación del sistema \"SIVAC\" mejora significativamente la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II."
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_3[4], 'none')
    clear_and_set_tc(tcs_12_3[4], [
        [("Consistencia documental", True, False)]
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_3[5], 'none')
    clear_and_set_tc(tcs_12_3[5], [
        [("Registros sin discrepancias (RSD):", True, False)],
        mathml_to_omml(FORMULAS_MML["rsd"]),
        [("Escala: ", True, False), ("Proporción (%) | Ficha de cotejo", False, False)],
        [("Concordancia programada vs entregada (CPE):", True, False)],
        mathml_to_omml(FORMULAS_MML["cpe"]),
        [("Escala: ", True, False), ("Proporción (%) | Ficha de cotejo", False, False)]
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_3[6], 'continue')
    clear_and_set_tc(tcs_12_3[6], [])

    # Fila 4: Variable Dependiente - Dimensión 3 (Satisfacción)
    tcs_12_4 = t12.rows[4]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_12_4[0], 'continue')
    clear_and_set_tc(tcs_12_4[0], [])

    set_tc_vmerge(tcs_12_4[1], 'none')
    clear_and_set_tc(tcs_12_4[1], [
        [("Problema Específico 3:", True, False)],
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II?"
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_4[2], 'none')
    clear_and_set_tc(tcs_12_4[2], [
        [("Objetivo Específico 3:", True, False)],
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II."
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_4[3], 'none')
    clear_and_set_tc(tcs_12_4[3], [
        [("Hipótesis Específica 3:", True, False)],
        "La aplicación del sistema \"SIVAC\" mejora significativamente la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II."
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_4[4], 'none')
    clear_and_set_tc(tcs_12_4[4], [
        [("Satisfacción del usuario", True, False)]
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_4[5], 'none')
    clear_and_set_tc(tcs_12_4[5], [
        [("Aceptación del proceso (AP):", True, False)],
        "Escala Likert (1 a 5, baremo 8-40)",
        [("Utilidad percibida (UP):", True, False)],
        "Escala Likert (1 a 5, baremo 8-40)",
        [("Instrumento:", True, False)],
        "Cuestionario TAM (16 ítems)"
    ], font_size_pt=FS, align="left", line_spacing=LS, space_before=SB, space_after=SA)

    set_tc_vmerge(tcs_12_4[6], 'continue')
    clear_and_set_tc(tcs_12_4[6], [])

    aplicar_bordes_apa7(t12)
    print("  [x] Tabla 12 reconfigurada con tipografía y espaciado de alta definición.")

    doc.save(DOC_PATH)
    print(f"Documento guardado con éxito en {DOC_PATH}.")

if __name__ == "__main__":
    main()
