#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Ajuste Quirúrgico y Corrección Estructural de Tablas v2.3
Resuelve de forma definitiva los problemas de desajuste visual, saltos de página
inadecuados, celdas partidas y desbordamiento de márgenes en:
  - Tabla 5 (Operacionalización de variables)
  - Tabla 8 (Instrumentos de recolección de datos)
  - Tabla 12 (Anexo 1: Matriz de Consistencia)

Principios aplicados:
  1. Geometría exacta de página (8,788 dxa útil Portrait, 14,000 dxa útil Landscape).
  2. <w:cantSplit/> en todas las filas para impedir fractura intra-celular de párrafos y fórmulas.
  3. <w:tblHeader/> en la fila 0 de todas las tablas para repetición obligatoria de encabezados.
  4. Salto de página antes de Tabla 5 para inicio limpio en página dedicada.
  5. Ampliación sustancial de las columnas de Indicadores (2,400 dxa en T5, 2,500 dxa en T12)
     para albergar ecuaciones nativas OMML sin quiebres de línea artificiales.
  6. Erradicación total de textos residuales/duplicados mediante limpieza de bajo nivel OpenXML.
  7. Reemplazo del cuadro de texto flotante de Anexos por flujo de párrafos nativos de Word.
"""

import sys
import docx
from docx.shared import Pt, Inches
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
import lxml.etree as ET

DOC_PATH = "salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V2.docx"
FUENTE = "Times New Roman"
XSLT_PATH = r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL"

# Inicializar transformador MathML -> OMML nativo de Word
xslt_doc = ET.parse(XSLT_PATH)
transform_mml = ET.XSLT(xslt_doc)

def mathml_to_omml(mml_str):
    """Convierte cadena MathML a nodo OpenXML <m:oMath> nativo."""
    dom = ET.fromstring(mml_str)
    omml = transform_mml(dom)
    return parse_xml(ET.tostring(omml))

# Catálogo canónico de fórmulas matemáticas
FORMULAS_MML = {
    "diseno_preexp": """<math xmlns="http://www.w3.org/1998/Math/MathML">
      <mrow>
        <mi mathvariant="bold">G</mi><mo>:</mo><mspace width="0.3em"/>
        <msub><mi>O</mi><mn>1</mn></msub><mo>&#x2192;</mo><mi>X</mi><mo>&#x2192;</mo><msub><mi>O</mi><mn>2</mn></msub>
      </mrow>
    </math>""",

    "t_reg": """<math xmlns="http://www.w3.org/1998/Math/MathML">
      <mrow>
        <msub><mi>T</mi><mtext>reg</mtext></msub><mo>=</mo>
        <msub><mi>t</mi><mtext>fin_registro</mtext></msub><mo>−</mo><msub><mi>t</mi><mtext>inicio_registro</mtext></msub>
      </mrow>
    </math>""",

    "t_vale": """<math xmlns="http://www.w3.org/1998/Math/MathML">
      <mrow>
        <msub><mi>T</mi><mtext>vale</mtext></msub><mo>=</mo>
        <msub><mi>t</mi><mtext>emisión</mtext></msub><mo>−</mo><msub><mi>t</mi><mtext>inicio_solicitud</mtext></msub>
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
        <mtext>Puntaje Total</mtext><mo>=</mo>
        <munderover><mo>∑</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mn>8</mn></munderover>
        <msub><mtext>Ítem</mtext><mi>i</mi></msub>
      </mrow>
    </math>"""
}

def clear_and_set_tc(tc, items, font_size_pt=8.5, align="left", line_spacing=252, space_before=20, space_after=20):
    """
    Limpia de forma exhaustiva una celda tc y añade nuevos párrafos en OpenXML puro,
    garantizando cero textos duplicados, soporte para <m:oMath> y formato uniforme.
    """
    # Preservar tcPr si existe
    tcPr = tc.find(qn('w:tcPr'))
    for child in list(tc):
        if child.tag != qn('w:tcPr'):
            tc.remove(child)

    if not items:
        # Párrafo mínimo requerido por ECMA-376
        empty_p = parse_xml(r'<w:p %s><w:pPr><w:spacing w:line="240" w:before="0" w:after="0"/></w:pPr></w:p>' % nsdecls('w'))
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

    # 1. tblW
    for w in tblPr.findall(qn('w:tblW')):
        tblPr.remove(w)
    tblPr.append(parse_xml(r'<w:tblW %s w:w="%d" w:type="dxa"/>' % (nsdecls('w'), total_width_dxa)))

    # 2. Alineación de tabla
    for jc in tblPr.findall(qn('w:jc')):
        tblPr.remove(jc)
    tblPr.append(parse_xml(r'<w:jc %s w:val="%s"/>' % (nsdecls('w'), align)))

    # 3. Márgenes internos de celda compactos
    for cm in tblPr.findall(qn('w:tblCellMar')):
        tblPr.remove(cm)
    tblPr.append(parse_xml(r'''<w:tblCellMar %s>
        <w:top w:w="30" w:type="dxa"/>
        <w:left w:w="70" w:type="dxa"/>
        <w:bottom w:w="30" w:type="dxa"/>
        <w:right w:w="70" w:type="dxa"/>
    </w:tblCellMar>''' % nsdecls('w')))

    # 4. tblGrid
    tblGrid = table._tbl.tblGrid
    if tblGrid is not None:
        table._tbl.remove(tblGrid)
    new_grid = parse_xml(r'<w:tblGrid %s/>' % nsdecls('w'))
    for cw in col_widths_dxa:
        new_grid.append(parse_xml(r'<w:gridCol %s w:w="%d"/>' % (nsdecls('w'), cw)))
    # Insertar tblGrid después de tblPr
    tblPr_idx = list(table._tbl).index(tblPr)
    table._tbl.insert(tblPr_idx + 1, new_grid)

    # 5. Aplicar tcW en cada celda
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

    # Borde inferior del encabezado (Fila 0)
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
    print("Iniciando ajuste estructural y corrección de tablas v2.3...")
    doc = docx.Document(DOC_PATH)

    # =========================================================================
    # 1. TABLA 5: OPERACIONALIZACIÓN DE VARIABLES
    # =========================================================================
    print("--- Procesando Tabla 5 ---")
    t5 = doc.tables[4]

    # Forzar salto de página en el párrafo del título de Tabla 5
    # Buscar el párrafo que contiene "Tabla 5"
    p_t5_title = None
    for p in doc.paragraphs:
        if "Tabla 5" in p.text and "Operacionalización" in p.text:
            p_t5_title = p
            break

    if p_t5_title is not None:
        p_t5_title.paragraph_format.page_break_before = True
        print("  [x] Salto de página antes de Tabla 5 configurado.")

    # Geometría Portrait: 8,788 dxa (15.50 cm)
    # Col 0 (Variable): 1,200 dxa (2.12 cm)
    # Col 1 (Definición conceptual): 2,088 dxa (3.68 cm)
    # Col 2 (Dimensiones): 1,400 dxa (2.47 cm)
    # Col 3 (Indicadores): 2,400 dxa (4.23 cm) - Ampliada para fórmulas OMML
    # Col 4 (Escala / Unidad): 1,700 dxa (3.00 cm)
    t5_cols = [1200, 2088, 1400, 2400, 1700]
    t5_total = sum(t5_cols) # 8788 dxa
    configure_table_geometry(t5, t5_total, t5_cols)

    # Ajustar número de filas a 8
    while len(t5.rows) > 8:
        tr = t5.rows[-1]._tr
        t5._tbl.remove(tr)

    # Fila 0: Encabezados
    headers_t5 = ["Variable", "Definición conceptual", "Dimensiones", "Indicadores", "Escala / Unidad de medida"]
    tcs_0 = t5.rows[0]._tr.findall(qn('w:tc'))
    set_row_properties(t5.rows[0]._tr, cant_split=True, is_header=True)
    for c_idx, h_text in enumerate(headers_t5):
        set_tc_vmerge(tcs_0[c_idx], 'none')
        clear_and_set_tc(tcs_0[c_idx], [[(h_text, True, False)]],
                         font_size_pt=9.0, align="center", line_spacing=240, space_before=20, space_after=20)

    # Fila 1: Variable Independiente
    tcs_1 = t5.rows[1]._tr.findall(qn('w:tc'))
    set_row_properties(t5.rows[1]._tr, cant_split=True, is_header=False)
    set_tc_vmerge(tcs_1[0], 'none')
    clear_and_set_tc(tcs_1[0], [
        [("Variable Independiente:", True, False)],
        [("Sistema web SIVAC", False, False)]
    ], font_size_pt=8.5, align="left")

    set_tc_vmerge(tcs_1[1], 'none')
    clear_and_set_tc(tcs_1[1], [
        "Aplicación informática basada en plataforma web orientada al registro, control y seguimiento de las operaciones de ingreso, almacenamiento y distribución de vacunas en la Dirección de Salud Apurímac II."
    ], font_size_pt=8.0, align="left")

    set_tc_vmerge(tcs_1[2], 'none')
    clear_and_set_tc(tcs_1[2], [
        [("Implementación del sistema", True, False)]
    ], font_size_pt=8.5, align="left")

    set_tc_vmerge(tcs_1[3], 'none')
    clear_and_set_tc(tcs_1[3], [
        "Adopción y uso del sistema web en la gestión de vacunas."
    ], font_size_pt=8.0, align="left")

    set_tc_vmerge(tcs_1[4], 'none')
    clear_and_set_tc(tcs_1[4], [
        [("Dicotómica nominal", True, False)],
        "0 = Sin sistema (Pretest)",
        "1 = Con sistema (Postest)"
    ], font_size_pt=8.0, align="left")

    # Filas 2 a 7: Variable Dependiente
    # Configurar propiedades de fila (cantSplit en todas)
    for r_idx in range(2, 8):
        set_row_properties(t5.rows[r_idx]._tr, cant_split=True, is_header=False)

    # Fila 2: VD - Dimensión 1 (Oportunidad) - Indicador 1.1 (T_reg)
    tcs_2 = t5.rows[2]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_2[0], 'restart')
    clear_and_set_tc(tcs_2[0], [
        [("Variable Dependiente:", True, False)],
        [("Gestión de movimientos de vacunas", False, False)]
    ], font_size_pt=8.5, align="left")

    set_tc_vmerge(tcs_2[1], 'restart')
    clear_and_set_tc(tcs_2[1], [
        "Conjunto de procedimientos técnicos y administrativos orientados a programar, registrar, despachar y controlar el flujo de productos biológicos e insumos en la red de frío de la Dirección de Salud Apurímac II."
    ], font_size_pt=8.0, align="left")

    set_tc_vmerge(tcs_2[2], 'restart')
    clear_and_set_tc(tcs_2[2], [
        [("Oportunidad de procesamiento", True, False)]
    ], font_size_pt=8.5, align="left")

    set_tc_vmerge(tcs_2[3], 'none')
    clear_and_set_tc(tcs_2[3], [
        [("Tiempo de registro de movimiento de vacunas", True, False)],
        mathml_to_omml(FORMULAS_MML["t_reg"]),
        "Duración en minutos desde el inicio hasta la culminación del registro."
    ], font_size_pt=8.0, align="left")

    set_tc_vmerge(tcs_2[4], 'none')
    clear_and_set_tc(tcs_2[4], [
        [("Minutos decimales (min)", True, False)],
        "Escala: Razón / Continua",
        "Instrumento: Ficha cronométrica"
    ], font_size_pt=8.0, align="left")

    # Fila 3: VD - Dimensión 1 (Oportunidad) - Indicador 1.2 (T_vale)
    tcs_3 = t5.rows[3]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_3[0], 'continue')
    clear_and_set_tc(tcs_3[0], [])
    set_tc_vmerge(tcs_3[1], 'continue')
    clear_and_set_tc(tcs_3[1], [])
    set_tc_vmerge(tcs_3[2], 'continue')
    clear_and_set_tc(tcs_3[2], [])

    set_tc_vmerge(tcs_3[3], 'none')
    clear_and_set_tc(tcs_3[3], [
        [("Tiempo de emisión de comprobante de salida / vale", True, False)],
        mathml_to_omml(FORMULAS_MML["t_vale"]),
        "Duración en minutos para la generación y emisión del vale de entrega."
    ], font_size_pt=8.0, align="left")

    set_tc_vmerge(tcs_3[4], 'none')
    clear_and_set_tc(tcs_3[4], [
        [("Minutos decimales (min)", True, False)],
        "Escala: Razón / Continua",
        "Instrumento: Ficha cronométrica"
    ], font_size_pt=8.0, align="left")

    # Fila 4: VD - Dimensión 2 (Consistencia documental) - Indicador 2.1 (RSD)
    tcs_4 = t5.rows[4]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_4[0], 'continue')
    clear_and_set_tc(tcs_4[0], [])
    set_tc_vmerge(tcs_4[1], 'continue')
    clear_and_set_tc(tcs_4[1], [])

    set_tc_vmerge(tcs_4[2], 'restart')
    clear_and_set_tc(tcs_4[2], [
        [("Consistencia documental", True, False)]
    ], font_size_pt=8.5, align="left")

    set_tc_vmerge(tcs_4[3], 'none')
    clear_and_set_tc(tcs_4[3], [
        [("Porcentaje de registros sin discrepancias", True, False)],
        mathml_to_omml(FORMULAS_MML["rsd"]),
        "Proporción de transacciones sin inconsistencias de lote, cantidad, fecha o destino."
    ], font_size_pt=8.0, align="left")

    set_tc_vmerge(tcs_4[4], 'none')
    clear_and_set_tc(tcs_4[4], [
        [("Porcentaje (%)", True, False)],
        "Escala: Razón / Proporción",
        "Instrumento: Ficha de cotejo"
    ], font_size_pt=8.0, align="left")

    # Fila 5: VD - Dimensión 2 (Consistencia documental) - Indicador 2.2 (CPE)
    tcs_5 = t5.rows[5]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_5[0], 'continue')
    clear_and_set_tc(tcs_5[0], [])
    set_tc_vmerge(tcs_5[1], 'continue')
    clear_and_set_tc(tcs_5[1], [])
    set_tc_vmerge(tcs_5[2], 'continue')
    clear_and_set_tc(tcs_5[2], [])

    set_tc_vmerge(tcs_5[3], 'none')
    clear_and_set_tc(tcs_5[3], [
        [("Concordancia entre cantidad programada y entregada", True, False)],
        mathml_to_omml(FORMULAS_MML["cpe"]),
        "Nivel de coincidencia entre las dosis requeridas y las efectivamente despachadas."
    ], font_size_pt=8.0, align="left")

    set_tc_vmerge(tcs_5[4], 'none')
    clear_and_set_tc(tcs_5[4], [
        [("Porcentaje (%)", True, False)],
        "Escala: Razón / Proporción",
        "Instrumento: Ficha de cotejo"
    ], font_size_pt=8.0, align="left")

    # Fila 6: VD - Dimensión 3 (Satisfacción del usuario) - Indicador 3.1 (AP)
    tcs_6 = t5.rows[6]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_6[0], 'continue')
    clear_and_set_tc(tcs_6[0], [])
    set_tc_vmerge(tcs_6[1], 'continue')
    clear_and_set_tc(tcs_6[1], [])

    set_tc_vmerge(tcs_6[2], 'restart')
    clear_and_set_tc(tcs_6[2], [
        [("Satisfacción del usuario", True, False)]
    ], font_size_pt=8.5, align="left")

    set_tc_vmerge(tcs_6[3], 'none')
    clear_and_set_tc(tcs_6[3], [
        [("Aceptación del proceso (AP)", True, False)],
        mathml_to_omml(FORMULAS_MML["tam_total"]),
        "Grado de conformidad del personal con el flujo operativo de trabajo."
    ], font_size_pt=8.0, align="left")

    set_tc_vmerge(tcs_6[4], 'none')
    clear_and_set_tc(tcs_6[4], [
        [("Escala de Likert (1 a 5)", True, False)],
        "Rango total: 8 a 40 puntos",
        "Instrumento: Cuestionario TAM"
    ], font_size_pt=8.0, align="left")

    # Fila 7: VD - Dimensión 3 (Satisfacción del usuario) - Indicador 3.2 (UP)
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
        "Percepción del usuario sobre el beneficio del sistema en sus labores sanitarias."
    ], font_size_pt=8.0, align="left")

    set_tc_vmerge(tcs_7[4], 'none')
    clear_and_set_tc(tcs_7[4], [
        [("Escala de Likert (1 a 5)", True, False)],
        "Rango total: 8 a 40 puntos",
        "Instrumento: Cuestionario TAM"
    ], font_size_pt=8.0, align="left")

    aplicar_bordes_apa7(t5)
    print("  [x] Tabla 5 saneada, alineada a 8,788 dxa y formateada bajo APA 7.")

    # =========================================================================
    # 2. TABLA 8: INSTRUMENTOS DE RECOLECCIÓN DE DATOS
    # =========================================================================
    print("--- Procesando Tabla 8 ---")
    t8 = doc.tables[7]
    t8_cols = [2200, 4188, 2400] # 8788 dxa
    configure_table_geometry(t8, 8788, t8_cols)

    set_row_properties(t8.rows[0]._tr, cant_split=True, is_header=True)
    tcs_8_0 = t8.rows[0]._tr.findall(qn('w:tc'))
    headers_t8 = ["Instrumento", "Descripción y estructura operativa", "Dimensión evaluada"]
    for c_idx, h_text in enumerate(headers_t8):
        set_tc_vmerge(tcs_8_0[c_idx], 'none')
        clear_and_set_tc(tcs_8_0[c_idx], [[(h_text, True, False)]],
                         font_size_pt=9.0, align="center")

    inst_data = [
        (
            [("Instrumento N° 01:", True, False), ("\nFicha de observación de tiempos cronometrados", False, False)],
            "Registro estructurado para el cronometraje de tareas operativas: registro de movimientos de vacunas (Treg) y emisión de comprobantes de salida o vales (Tvale), medido en minutos decimales.",
            [("Oportunidad de procesamiento", True, False), ("\n(Tiempos de registro y de emisión de vales)", False, False)]
        ),
        (
            [("Instrumento N° 02:", True, False), ("\nFicha de cotejo documental de consistencia", False, False)],
            "Instrumento de auditoría documental para verificar la conformidad de registros de movimiento (RSD) bajo 8 criterios técnicos obligatorios y la concordancia de cantidades programadas vs entregadas (CPE).",
            [("Consistencia documental", True, False), ("\n(Registros conformes y concordancia de cantidades)", False, False)]
        ),
        (
            [("Instrumento N° 03:", True, False), ("\nCuestionario de satisfacción del usuario (TAM)", False, False)],
            "Cuestionario estructurado bajo escala de Likert de 5 niveles (8 ítems) que evalúa las subescalas de Aceptación del Proceso (AP) y Utilidad Percibida (UP), con baremo de 8 a 40 puntos.",
            [("Satisfacción del usuario", True, False), ("\n(Aceptación y utilidad percibida)", False, False)]
        )
    ]

    for r_idx, (col0, col1, col2) in enumerate(inst_data, start=1):
        set_row_properties(t8.rows[r_idx]._tr, cant_split=True, is_header=False)
        tcs_r = t8.rows[r_idx]._tr.findall(qn('w:tc'))
        set_tc_vmerge(tcs_r[0], 'none')
        clear_and_set_tc(tcs_r[0], [col0], font_size_pt=8.5, align="left")
        set_tc_vmerge(tcs_r[1], 'none')
        clear_and_set_tc(tcs_r[1], [col1], font_size_pt=8.0, align="left")
        set_tc_vmerge(tcs_r[2], 'none')
        clear_and_set_tc(tcs_r[2], [col2], font_size_pt=8.5, align="left")

    aplicar_bordes_apa7(t8)
    print("  [x] Tabla 8 saneada y alineada a 8,788 dxa.")

    # =========================================================================
    # 3. TABLA 12: MATRIZ DE CONSISTENCIA (ANEXO 1)
    # =========================================================================
    print("--- Procesando Tabla 12 y Anexo 1 ---")
    t12 = doc.tables[11]

    # Limpieza del cuadro de texto flotante arcaico en el anexo
    # Buscar el párrafo que contiene el cuadro de texto flotante "ANEXOS"
    p_drawing_anexos = None
    for p in doc.paragraphs:
        if len(p._p.findall(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing")) > 0:
            # Comprobar si tiene el texto ANEXOS
            p_xml = ET.tostring(p._p, encoding="utf-8").decode("utf-8")
            if "ANEXOS" in p_xml or "Matriz de Consistencia" in p_xml:
                p_drawing_anexos = p
                break

    # Insertar párrafos limpios de títulos antes de la Tabla 12
    t12_elem = t12._tbl
    parent_body = t12_elem.getparent()
    t12_idx = list(parent_body).index(t12_elem)

    # Crear párrafo Título ANEXOS
    p_anexos_title = parse_xml(r'''<w:p %s>
        <w:pPr>
            <w:pStyle w:val="Ttulo1"/>
            <w:spacing w:before="240" w:after="120"/>
            <w:jc w:val="center"/>
        </w:pPr>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="%s" w:hAnsi="%s"/>
                <w:b w:val="1"/>
                <w:sz w:val="28"/>
            </w:rPr>
            <w:t>ANEXOS</w:t>
        </w:r>
    </w:p>''' % (nsdecls('w'), FUENTE, FUENTE))

    # Crear párrafo Subtítulo Anexo 1: Matriz de Consistencia
    p_anexo1_title = parse_xml(r'''<w:p %s>
        <w:pPr>
            <w:spacing w:before="60" w:after="180"/>
            <w:jc w:val="center"/>
        </w:pPr>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="%s" w:hAnsi="%s"/>
                <w:b w:val="1"/>
                <w:i w:val="1"/>
                <w:sz w:val="24"/>
            </w:rPr>
            <w:t>Anexo 1: Matriz de Consistencia</w:t>
        </w:r>
    </w:p>''' % (nsdecls('w'), FUENTE, FUENTE))

    parent_body.insert(t12_idx, p_anexos_title)
    parent_body.insert(t12_idx + 1, p_anexo1_title)
    print("  [x] Párrafos limpios de títulos de Anexo 1 insertados antes de Tabla 12.")

    # Eliminar el párrafo con cuadro de texto flotante obsoleto
    if p_drawing_anexos is not None:
        p_drawing_elem = p_drawing_anexos._p
        if p_drawing_elem.getparent() is not None:
            p_drawing_elem.getparent().remove(p_drawing_elem)
            print("  [x] Cuadro de texto flotante obsoleto eliminado con éxito.")

    # Geometría Landscape: exactamente 14,000 dxa (24.70 cm)
    # Col 0 (VARIABLES): 1,300 dxa (2.29 cm)
    # Col 1 (PROBLEMAS): 2,250 dxa (3.97 cm)
    # Col 2 (OBJETIVOS): 2,250 dxa (3.97 cm)
    # Col 3 (HIPÓTESIS): 2,250 dxa (3.97 cm)
    # Col 4 (DIMENSIONES): 1,550 dxa (2.73 cm)
    # Col 5 (INDICADORES Y ESCALAS): 2,500 dxa (4.41 cm) - Ampliada para fórmulas
    # Col 6 (METODOLOGÍA): 1,900 dxa (3.35 cm)
    t12_cols = [1300, 2250, 2250, 2250, 1550, 2500, 1900]
    t12_total = sum(t12_cols) # 14000 dxa
    configure_table_geometry(t12, t12_total, t12_cols)

    # Configurar cantSplit y tblHeader en filas de Tabla 12
    for r in t12.rows:
        set_row_properties(r._tr, cant_split=True, is_header=False)
    set_row_properties(t12.rows[0]._tr, cant_split=True, is_header=True)

    # Fila 0: Encabezados de Tabla 12
    headers_t12 = ["VARIABLES", "PROBLEMAS", "OBJETIVOS", "HIPÓTESIS", "DIMENSIONES", "INDICADORES Y ESCALAS", "METODOLOGÍA"]
    tcs_12_0 = t12.rows[0]._tr.findall(qn('w:tc'))
    for c_idx, h_text in enumerate(headers_t12):
        set_tc_vmerge(tcs_12_0[c_idx], 'none')
        clear_and_set_tc(tcs_12_0[c_idx], [[(h_text, True, False)]],
                         font_size_pt=8.5, align="center", line_spacing=240, space_before=20, space_after=20)

    # Fila 1: Variable Independiente
    tcs_12_1 = t12.rows[1]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_12_1[0], 'none')
    clear_and_set_tc(tcs_12_1[0], [
        [("VARIABLE INDEPENDIENTE:", True, False)],
        [("Sistema web SIVAC", False, False)]
    ], font_size_pt=8.0, align="left")

    set_tc_vmerge(tcs_12_1[1], 'none')
    clear_and_set_tc(tcs_12_1[1], [
        [("Problema General:", True, False)],
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025?"
    ], font_size_pt=7.5, align="left")

    set_tc_vmerge(tcs_12_1[2], 'none')
    clear_and_set_tc(tcs_12_1[2], [
        [("Objetivo General:", True, False)],
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025."
    ], font_size_pt=7.5, align="left")

    set_tc_vmerge(tcs_12_1[3], 'none')
    clear_and_set_tc(tcs_12_1[3], [
        [("Hipótesis General:", True, False)],
        "La aplicación del sistema \"SIVAC\" mejora significativamente la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025."
    ], font_size_pt=7.5, align="left")

    set_tc_vmerge(tcs_12_1[4], 'none')
    clear_and_set_tc(tcs_12_1[4], [
        [("Implementación del sistema", True, False)]
    ], font_size_pt=8.0, align="left")

    set_tc_vmerge(tcs_12_1[5], 'none')
    clear_and_set_tc(tcs_12_1[5], [
        [("Condición operativa:", True, False)],
        "• Sin sistema SIVAC (Pretest)",
        "• Con sistema SIVAC (Postest)",
        [("Escala:", True, False), (" Dicotómica", False, False)]
    ], font_size_pt=7.5, align="left")

    set_tc_vmerge(tcs_12_1[6], 'restart')
    clear_and_set_tc(tcs_12_1[6], [
        [("Tipo: ", True, False), ("Aplicada", False, False)],
        [("Enfoque: ", True, False), ("Cuantitativo", False, False)],
        [("Nivel: ", True, False), ("Explicativo", False, False)],
        [("Diseño: ", True, False), ("Preexperimental", False, False)],
        mathml_to_omml(FORMULAS_MML["diseno_preexp"]),
        [("Población y Muestra:", True, False)],
        "Censal (N = n = 14 usuarios)"
    ], font_size_pt=7.5, align="left")

    # Fila 2: Variable Dependiente - Dimensión 1 (Oportunidad de procesamiento)
    tcs_12_2 = t12.rows[2]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_12_2[0], 'restart')
    clear_and_set_tc(tcs_12_2[0], [
        [("VARIABLE DEPENDIENTE:", True, False)],
        [("Gestión de movimientos de vacunas", False, False)]
    ], font_size_pt=8.0, align="left")

    set_tc_vmerge(tcs_12_2[1], 'none')
    clear_and_set_tc(tcs_12_2[1], [
        [("Problema Específico 1:", True, False)],
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?"
    ], font_size_pt=7.5, align="left")

    set_tc_vmerge(tcs_12_2[2], 'none')
    clear_and_set_tc(tcs_12_2[2], [
        [("Objetivo Específico 1:", True, False)],
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size_pt=7.5, align="left")

    set_tc_vmerge(tcs_12_2[3], 'none')
    clear_and_set_tc(tcs_12_2[3], [
        [("Hipótesis Específica 1:", True, False)],
        "La aplicación del sistema \"SIVAC\" mejora significativamente la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size_pt=7.5, align="left")

    set_tc_vmerge(tcs_12_2[4], 'none')
    clear_and_set_tc(tcs_12_2[4], [
        [("Oportunidad de procesamiento", True, False)]
    ], font_size_pt=8.0, align="left")

    set_tc_vmerge(tcs_12_2[5], 'none')
    clear_and_set_tc(tcs_12_2[5], [
        [("Tiempo de registro de movimientos:", True, False)],
        mathml_to_omml(FORMULAS_MML["t_reg"]),
        [("Escala: ", True, False), ("Razón (minutos)", False, False)],
        [("Tiempo de emisión de comprobante de salida / vale:", True, False)],
        mathml_to_omml(FORMULAS_MML["t_vale"]),
        [("Escala: ", True, False), ("Razón (minutos)", False, False)]
    ], font_size_pt=7.5, align="left")

    set_tc_vmerge(tcs_12_2[6], 'continue')
    clear_and_set_tc(tcs_12_2[6], [])

    # Fila 3: Variable Dependiente - Dimensión 2 (Consistencia documental)
    tcs_12_3 = t12.rows[3]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_12_3[0], 'continue')
    clear_and_set_tc(tcs_12_3[0], [])

    set_tc_vmerge(tcs_12_3[1], 'none')
    clear_and_set_tc(tcs_12_3[1], [
        [("Problema Específico 2:", True, False)],
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?"
    ], font_size_pt=7.5, align="left")

    set_tc_vmerge(tcs_12_3[2], 'none')
    clear_and_set_tc(tcs_12_3[2], [
        [("Objetivo Específico 2:", True, False)],
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size_pt=7.5, align="left")

    set_tc_vmerge(tcs_12_3[3], 'none')
    clear_and_set_tc(tcs_12_3[3], [
        [("Hipótesis Específica 2:", True, False)],
        "La aplicación del sistema \"SIVAC\" mejora significativamente la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size_pt=7.5, align="left")

    set_tc_vmerge(tcs_12_3[4], 'none')
    clear_and_set_tc(tcs_12_3[4], [
        [("Consistencia documental", True, False)]
    ], font_size_pt=8.0, align="left")

    set_tc_vmerge(tcs_12_3[5], 'none')
    clear_and_set_tc(tcs_12_3[5], [
        [("Registros sin discrepancias:", True, False)],
        mathml_to_omml(FORMULAS_MML["rsd"]),
        [("Escala: ", True, False), ("Razón / Proporción (%)", False, False)],
        [("Concordancia programada vs entregada:", True, False)],
        mathml_to_omml(FORMULAS_MML["cpe"]),
        [("Escala: ", True, False), ("Razón / Proporción (%)", False, False)]
    ], font_size_pt=7.5, align="left")

    set_tc_vmerge(tcs_12_3[6], 'continue')
    clear_and_set_tc(tcs_12_3[6], [])

    # Fila 4: Variable Dependiente - Dimensión 3 (Satisfacción del usuario)
    tcs_12_4 = t12.rows[4]._tr.findall(qn('w:tc'))
    set_tc_vmerge(tcs_12_4[0], 'continue')
    clear_and_set_tc(tcs_12_4[0], [])

    set_tc_vmerge(tcs_12_4[1], 'none')
    clear_and_set_tc(tcs_12_4[1], [
        [("Problema Específico 3:", True, False)],
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?"
    ], font_size_pt=7.5, align="left")

    set_tc_vmerge(tcs_12_4[2], 'none')
    clear_and_set_tc(tcs_12_4[2], [
        [("Objetivo Específico 3:", True, False)],
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size_pt=7.5, align="left")

    set_tc_vmerge(tcs_12_4[3], 'none')
    clear_and_set_tc(tcs_12_4[3], [
        [("Hipótesis Específica 3:", True, False)],
        "La aplicación del sistema \"SIVAC\" mejora significativamente la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size_pt=7.5, align="left")

    set_tc_vmerge(tcs_12_4[4], 'none')
    clear_and_set_tc(tcs_12_4[4], [
        [("Satisfacción del usuario", True, False)]
    ], font_size_pt=8.0, align="left")

    set_tc_vmerge(tcs_12_4[5], 'none')
    clear_and_set_tc(tcs_12_4[5], [
        [("Aceptación del proceso operativo (AP):", True, False)],
        "Escala de Likert (1 a 5, baremo 8-40)",
        [("Utilidad percibida sanitaria (UP):", True, False)],
        "Escala de Likert (1 a 5, baremo 8-40)"
    ], font_size_pt=7.5, align="left")

    set_tc_vmerge(tcs_12_4[6], 'continue')
    clear_and_set_tc(tcs_12_4[6], [])

    aplicar_bordes_apa7(t12)
    print("  [x] Tabla 12 saneada, ajustada exactamente a 14,000 dxa y formateada bajo APA 7.")

    # Guardar documento actualizado
    print(f"Guardando documento oficial en {DOC_PATH}...")
    doc.save(DOC_PATH)
    print("¡Proceso completado exitosamente con cero errores!")

if __name__ == "__main__":
    main()
