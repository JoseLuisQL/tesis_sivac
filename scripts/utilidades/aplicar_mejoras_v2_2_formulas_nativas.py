#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Actualizador Quirúrgico Limpio v2.2 de PROYECTO_TESIS.docx
Soporte Nativo de Fórmulas Matemáticas de Word (OpenXML OMML / MML2OMML.XSL),
erradicación total de fugas booleanas ("TrueFalse") y normalización editorial
estricta bajo norma APA 7.ª edición (UNAJMA).

Guarda exclusivamente en salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V2.docx
preservando la inmutabilidad de referencias/proyecto_base/.
"""

import sys
import docx
from docx.shared import Pt, Inches
from docx.table import _Cell
from docx.text.paragraph import Paragraph
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
import lxml.etree as ET

FUENTE = "Times New Roman"
XSLT_PATH = r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL"

# Inicializar transformador MathML -> OMML
xslt_doc = ET.parse(XSLT_PATH)
transform_mml = ET.XSLT(xslt_doc)

def mathml_to_omml(mml_str):
    """Transforma una cadena MathML en un elemento XML nativo de Word <m:oMath>."""
    dom = ET.fromstring(mml_str)
    omml = transform_mml(dom)
    return parse_xml(ET.tostring(omml))

# Catálogo canónico de fórmulas matemáticas en MathML
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
    </math>""",

    "aiken_v": """<math xmlns="http://www.w3.org/1998/Math/MathML">
      <mrow>
        <mi>V</mi><mo>=</mo>
        <mfrac><mi>S</mi><mrow><mi>n</mi><mo stretchy="false">(</mo><mi>c</mi><mo>−</mo><mn>1</mn><mo stretchy="false">)</mo></mrow></mfrac>
      </mrow>
    </math>""",

    "cronbach_alpha": """<math xmlns="http://www.w3.org/1998/Math/MathML">
      <mrow>
        <mi>α</mi><mo>=</mo>
        <mrow><mo>(</mo><mfrac><mi>k</mi><mrow><mi>k</mi><mo>−</mo><mn>1</mn></mrow></mfrac><mo>)</mo></mrow>
        <mrow><mo>[</mo><mrow><mn>1</mn><mo>−</mo><mfrac><mrow><mo>∑</mo><msubsup><mi>s</mi><mi>i</mi><mn>2</mn></msubsup></mrow><msubsup><mi>s</mi><mi>t</mi><mn>2</mn></msubsup></mfrac></mrow><mo>]</mo></mrow>
      </mrow>
    </math>""",

    "dif_pareadas": """<math xmlns="http://www.w3.org/1998/Math/MathML">
      <mrow>
        <msub><mi>D</mi><mi>i</mi></msub><mo>=</mo><msub><mi>O</mi><mrow><mn>2</mn><mi>i</mi></mrow></msub><mo>−</mo><msub><mi>O</mi><mrow><mn>1</mn><mi>i</mi></mrow></msub>
      </mrow>
    </math>"""
}

def set_tc_vmerge(tc, mode):
    tcPr = tc.get_or_add_tcPr()
    for vm in tcPr.findall(qn('w:vMerge')):
        tcPr.remove(vm)
    if mode == 'restart':
        tcPr.append(parse_xml(r'<w:vMerge %s w:val="restart"/>' % nsdecls('w')))
    elif mode == 'continue':
        tcPr.append(parse_xml(r'<w:vMerge %s/>' % nsdecls('w')))

def get_row_tcs(table, row_idx):
    return table.rows[row_idx]._tr.findall(qn('w:tc'))

def set_tc_content(tc, table, items, font_size=Pt(9.0), bold_first=False, align=WD_ALIGN_PARAGRAPH.LEFT):
    """
    Rellena una celda de tabla garantizando tipografía uniforme Times New Roman,
    soporte para elementos de fórmulas OMML nativas y erradicación estricta de booleanos.
    """
    cell = _Cell(tc, table)
    cell.text = ""
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    for idx, item in enumerate(items):
        p = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()
        p.alignment = align
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(1.5)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.first_line_indent = Inches(0)

        # Inserción directa si es un elemento OMML
        if hasattr(item, 'tag') and 'oMath' in item.tag:
            p._p.append(item)
            continue

        if isinstance(item, (list, tuple)):
            for seg in item:
                if isinstance(seg, tuple):
                    t_text = str(seg[0])
                    t_bold = bool(seg[1]) if len(seg) > 1 else False
                    t_italic = bool(seg[2]) if len(seg) > 2 else False
                    t_size = seg[3] if len(seg) > 3 else font_size
                elif isinstance(seg, bool):
                    # Prohibición cardinal: nunca serializar un booleano como texto
                    continue
                else:
                    t_text = str(seg)
                    t_bold = False
                    t_italic = False
                    t_size = font_size

                run = p.add_run(t_text)
                run.font.name = FUENTE
                run.font.size = t_size
                run.font.bold = t_bold
                run.font.italic = t_italic
        else:
            # Si el item es un booleano suelto, ignorarlo
            if isinstance(item, bool):
                continue
            run = p.add_run(str(item))
            run.font.name = FUENTE
            run.font.size = font_size
            if idx == 0 and bold_first:
                run.font.bold = True

def aplicar_bordes_apa7(table):
    """
    Aplica las tres líneas horizontales canónicas de APA 7:
    borde superior de tabla, borde inferior de encabezados y borde inferior de última fila.
    Cero bordes verticales y cero líneas interiores.
    """
    tblPr = table._tbl.tblPr
    for b in tblPr.findall(qn('w:tblBorders')):
        tblPr.remove(b)
    bordes_xml = parse_xml(r'''
        <w:tblBorders %s>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>
            <w:insideH w:val="none"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''' % nsdecls('w'))
    tblPr.append(bordes_xml)

    rows = table._tbl.findall(qn('w:tr'))
    for r_idx, tr in enumerate(rows):
        trPr = tr.get_or_add_trPr()
        for b in trPr.findall(qn('w:tcBorders')):
            trPr.remove(b)
        for tc in tr.findall(qn('w:tc')):
            tcPr = tc.get_or_add_tcPr()
            for b in tcPr.findall(qn('w:tcBorders')):
                tcPr.remove(b)
            if r_idx == 0:
                tc_border = parse_xml(r'''
                    <w:tcBorders %s>
                        <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>
                        <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>
                        <w:left w:val="none"/>
                        <w:right w:val="none"/>
                    </w:tcBorders>
                ''' % nsdecls('w'))
                tcPr.append(tc_border)
            elif r_idx == len(rows) - 1:
                tc_border = parse_xml(r'''
                    <w:tcBorders %s>
                        <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>
                        <w:top w:val="none"/>
                        <w:left w:val="none"/>
                        <w:right w:val="none"/>
                    </w:tcBorders>
                ''' % nsdecls('w'))
                tcPr.append(tc_border)
            else:
                tc_border = parse_xml(r'''
                    <w:tcBorders %s>
                        <w:top w:val="none"/>
                        <w:bottom w:val="none"/>
                        <w:left w:val="none"/>
                        <w:right w:val="none"/>
                    </w:tcBorders>
                ''' % nsdecls('w'))
                tcPr.append(tc_border)

def actualizar_parrafo(p, runs_data, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=Pt(0), space_after=Pt(6), line_spacing=1.5, indent=Inches(0.5)):
    """Actualiza el texto y formato de un párrafo con Times New Roman estricto."""
    p.text = ""
    p.alignment = align
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = space_before
    p.paragraph_format.space_after = space_after
    p.paragraph_format.first_line_indent = indent

    for item in runs_data:
        if isinstance(item, tuple):
            text = item[0]
            bold = item[1] if len(item) > 1 else False
            italic = item[2] if len(item) > 2 else False
            size = item[3] if len(item) > 3 else Pt(12)
        elif isinstance(item, bool):
            continue
        else:
            text = str(item)
            bold = False
            italic = False
            size = Pt(12)

        run = p.add_run(text)
        run.font.name = FUENTE
        run.font.size = size
        run.font.bold = bold
        run.font.italic = italic

def insertar_parrafo_ecuacion_despues(p_base, doc, mml_key):
    """
    Inserta un nuevo párrafo de ecuación centrada nativa de Word inmediatamente después de p_base.
    """
    new_xml = parse_xml(f"<w:p {nsdecls('w')}/>")
    p_base._p.addnext(new_xml)
    p_eq = Paragraph(new_xml, doc)
    p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_eq.paragraph_format.space_before = Pt(6)
    p_eq.paragraph_format.space_after = Pt(6)
    p_eq.paragraph_format.line_spacing = 1.15
    p_eq.paragraph_format.first_line_indent = Inches(0)

    omml_elem = mathml_to_omml(FORMULAS_MML[mml_key])
    p_eq._p.append(omml_elem)
    return p_eq

def insertar_parrafo_texto_despues(p_base, doc, runs_data, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=Pt(0), space_after=Pt(6), line_spacing=1.5, indent=Inches(0.5)):
    """
    Inserta un nuevo párrafo de texto inmediatamente después de p_base.
    """
    new_xml = parse_xml(f"<w:p {nsdecls('w')}/>")
    p_base._p.addnext(new_xml)
    p_nuevo = Paragraph(new_xml, doc)
    actualizar_parrafo(p_nuevo, runs_data, align=align, space_before=space_before, space_after=space_after, line_spacing=line_spacing, indent=indent)
    return p_nuevo

def procesar_actualizacion_v2_2():
    doc_path = "salidas/archivo/PROYECTO_TESIS_ORIGINAL_BACKUP.docx"
    print(f"Cargando documento base de respaldo: {doc_path}...")
    doc = docx.Document(doc_path)

    # =========================================================================
    # PARTE 1: PÁRRAFOS 376 A 386 (SECCIÓN 3.3 OPERACIONALIZACIÓN DE VARIABLES)
    # =========================================================================
    print("Actualizando Párrafos 376 a 386 (Sección 3.3)...")

    actualizar_parrafo(doc.paragraphs[376], [("3.3 Operacionalización de variables", True, False)],
                       align=WD_ALIGN_PARAGRAPH.LEFT, indent=Inches(0), space_after=Pt(6))

    actualizar_parrafo(doc.paragraphs[377], [
        ("En la presente investigación se han identificado y definido dos variables de estudio:", False, False)
    ])

    actualizar_parrafo(doc.paragraphs[378], [("Variable independiente:", True, False)],
                       align=WD_ALIGN_PARAGRAPH.LEFT, indent=Inches(0), space_after=Pt(2))

    actualizar_parrafo(doc.paragraphs[379], [
        ("Sistema web \"SIVAC\". ", True, False),
        ("Definida conceptualmente como una aplicación informática basada en arquitectura web para el registro, control, seguimiento y trazabilidad de los movimientos de biológicos en la red de frío de la Dirección de Salud Apurímac II (Sommerville, 2016; Pressman y Maxim, 2021). Operacionalmente, constituye la solución tecnológica implementada para sistematizar la gestión operativa de vacunas, evaluada a través de sus componentes de registro de movimientos, emisión de comprobantes y control de existencias frente al procedimiento tradicional previo.", False, False)
    ], indent=Inches(0.5))

    doc.paragraphs[380].text = ""

    actualizar_parrafo(doc.paragraphs[381], [("Variable dependiente:", True, False)],
                       align=WD_ALIGN_PARAGRAPH.LEFT, indent=Inches(0), space_after=Pt(2))

    actualizar_parrafo(doc.paragraphs[382], [
        ("Gestión de movimientos de vacunas. ", True, False),
        ("Definida conceptualmente como el conjunto estructurado de procedimientos técnicos y administrativos orientados a registrar, controlar, reportar y verificar las entradas, salidas, saldos y distribución de vacunas e insumos, asegurando la trazabilidad de los biológicos y la disponibilidad de información oportuna (Ministerio de Salud, 2022). Operacionalmente, se evalúa mediante tres dimensiones: oportunidad de procesamiento (tiempos de registro y de emisión de vales), consistencia documental (registros sin discrepancias y concordancia de cantidades) y satisfacción del usuario (aceptación del proceso y utilidad percibida según el modelo de aceptación tecnológica).", False, False)
    ], indent=Inches(0.5))

    doc.paragraphs[383].text = ""

    actualizar_parrafo(doc.paragraphs[384], [
        ("En la Tabla 5 se detalla la matriz de operacionalización de las variables consideradas en la presente investigación.", False, False)
    ], indent=Inches(0.5))

    actualizar_parrafo(doc.paragraphs[385], [
        ("Tabla 5\n", True, False, Pt(10)),
        ("Operacionalización de variables", False, True, Pt(10))
    ], align=WD_ALIGN_PARAGRAPH.LEFT, indent=Inches(0), space_after=Pt(4), line_spacing=1.0)

    actualizar_parrafo(doc.paragraphs[386], [
        ("Nota. ", True, False, Pt(10)),
        ("Definiciones adaptadas de Sommerville (2016), Davis (1989) y Ministerio de Salud (2022). Escala de Likert: 1 = Muy en desacuerdo, 2 = En desacuerdo, 3 = Ni de acuerdo ni en desacuerdo, 4 = De acuerdo, 5 = Muy de acuerdo.", False, False, Pt(10))
    ], align=WD_ALIGN_PARAGRAPH.LEFT, indent=Inches(0), space_after=Pt(12), line_spacing=1.5)

    # =========================================================================
    # PARTE 2: TABLA 5 (OPERACIONALIZACIÓN DE VARIABLES - ÍNDICE 4) CON FÓRMULAS NATIVAS
    # =========================================================================
    print("Reestructurando Tabla 5 con fórmulas nativas de Word OMML y APA 7...")
    t5 = doc.tables[4]

    while len(t5.rows) > 8:
        tr = t5.rows[-1]._tr
        t5._tbl.remove(tr)

    # Fila 0: Encabezados LIMPIOS (CERO TrueFalse)
    headers_t5 = ["Variable", "Definición conceptual", "Dimensiones", "Indicadores", "Escala / Unidad de medida"]
    tcs_0 = get_row_tcs(t5, 0)
    for c_idx, h_text in enumerate(headers_t5):
        set_tc_content(tcs_0[c_idx], t5, [(h_text, True, False)],
                       font_size=Pt(9.5), align=WD_ALIGN_PARAGRAPH.CENTER)

    # Fila 1: Variable Independiente
    tcs_1 = get_row_tcs(t5, 1)
    set_tc_vmerge(tcs_1[0], 'restart')
    set_tc_content(tcs_1[0], t5, [
        [("Variable Independiente:", True, False)],
        "Sistema web SIVAC"
    ], font_size=Pt(9.0))

    set_tc_vmerge(tcs_1[1], 'restart')
    set_tc_content(tcs_1[1], t5, [
        "Aplicación informática basada en plataforma web orientada al registro, control y seguimiento de las operaciones de ingreso, almacenamiento y distribución de vacunas en la Dirección de Salud Apurímac II."
    ], font_size=Pt(8.5))

    set_tc_vmerge(tcs_1[2], 'restart')
    set_tc_content(tcs_1[2], t5, [
        [("Implementación del sistema", True, False)]
    ], font_size=Pt(9.0))

    set_tc_vmerge(tcs_1[3], 'restart')
    set_tc_content(tcs_1[3], t5, [
        "Adopción y uso del sistema web en la gestión de vacunas."
    ], font_size=Pt(8.5))

    set_tc_vmerge(tcs_1[4], 'restart')
    set_tc_content(tcs_1[4], t5, [
        [("Dicotómica nominal", True, False)],
        "0 = Sin sistema (Pretest)",
        "1 = Con sistema (Postest)"
    ], font_size=Pt(8.5))

    # Filas 2 a 7: Variable Dependiente
    vd_text = [
        [("Variable Dependiente:", True, False)],
        "Gestión de movimientos de vacunas"
    ]
    def_vd = [
        "Conjunto de procedimientos técnicos y administrativos orientados a programar, registrar, despachar y controlar el flujo de productos biológicos e insumos en la red de frío de la Dirección de Salud Apurímac II."
    ]

    for r in range(2, 8):
        tcs_r = get_row_tcs(t5, r)
        set_tc_vmerge(tcs_r[0], 'restart' if r == 2 else 'continue')
        if r == 2:
            set_tc_content(tcs_r[0], t5, vd_text, font_size=Pt(9.0))

        set_tc_vmerge(tcs_r[1], 'restart' if r == 2 else 'continue')
        if r == 2:
            set_tc_content(tcs_r[1], t5, def_vd, font_size=Pt(8.5))

    # Dimensión 1: Oportunidad de procesamiento (Filas 2 y 3)
    tcs_2 = get_row_tcs(t5, 2)
    tcs_3 = get_row_tcs(t5, 3)
    set_tc_vmerge(tcs_2[2], 'restart')
    set_tc_content(tcs_2[2], t5, [[("Oportunidad de procesamiento", True, False)]], font_size=Pt(9.0))
    set_tc_vmerge(tcs_3[2], 'continue')

    # Ind 1.1 con ecuación OMML nativa
    omml_treg = mathml_to_omml(FORMULAS_MML["t_reg"])
    set_tc_content(tcs_2[3], t5, [
        [("Tiempo de registro de movimiento de vacunas", True, False)],
        omml_treg,
        "Duración en minutos desde el inicio hasta la culminación del registro."
    ], font_size=Pt(8.5))
    set_tc_content(tcs_2[4], t5, [
        [("Minutos decimales (min)", True, False)],
        "Escala: Razón / Continua",
        "Instrumento: Ficha cronométrica"
    ], font_size=Pt(8.5))

    # Ind 1.2 con ecuación OMML nativa
    omml_tvale = mathml_to_omml(FORMULAS_MML["t_vale"])
    set_tc_content(tcs_3[3], t5, [
        [("Tiempo de emisión de comprobante de salida / vale", True, False)],
        omml_tvale,
        "Duración en minutos para la generación y emisión del vale de entrega."
    ], font_size=Pt(8.5))
    set_tc_content(tcs_3[4], t5, [
        [("Minutos decimales (min)", True, False)],
        "Escala: Razón / Continua",
        "Instrumento: Ficha cronométrica"
    ], font_size=Pt(8.5))

    # Dimensión 2: Consistencia documental (Filas 4 y 5)
    tcs_4 = get_row_tcs(t5, 4)
    tcs_5 = get_row_tcs(t5, 5)
    set_tc_vmerge(tcs_4[2], 'restart')
    set_tc_content(tcs_4[2], t5, [[("Consistencia documental", True, False)]], font_size=Pt(9.0))
    set_tc_vmerge(tcs_5[2], 'continue')

    # Ind 2.1 con ecuación OMML nativa
    omml_rsd = mathml_to_omml(FORMULAS_MML["rsd"])
    set_tc_content(tcs_4[3], t5, [
        [("Porcentaje de registros sin discrepancias", True, False)],
        omml_rsd,
        "Proporción de transacciones sin inconsistencias de lote, cantidad, fecha o destino."
    ], font_size=Pt(8.5))
    set_tc_content(tcs_4[4], t5, [
        [("Porcentaje (%)", True, False)],
        "Escala: Razón / Proporción",
        "Instrumento: Ficha de cotejo"
    ], font_size=Pt(8.5))

    # Ind 2.2 con ecuación OMML nativa
    omml_cpe = mathml_to_omml(FORMULAS_MML["cpe"])
    set_tc_content(tcs_5[3], t5, [
        [("Concordancia entre cantidad programada y entregada", True, False)],
        omml_cpe,
        "Nivel de coincidencia entre las dosis requeridas y las efectivamente despachadas."
    ], font_size=Pt(8.5))
    set_tc_content(tcs_5[4], t5, [
        [("Porcentaje (%)", True, False)],
        "Escala: Razón / Proporción",
        "Instrumento: Ficha de cotejo"
    ], font_size=Pt(8.5))

    # Dimensión 3: Satisfacción del usuario (Filas 6 y 7)
    tcs_6 = get_row_tcs(t5, 6)
    tcs_7 = get_row_tcs(t5, 7)
    set_tc_vmerge(tcs_6[2], 'restart')
    set_tc_content(tcs_6[2], t5, [[("Satisfacción del usuario", True, False)]], font_size=Pt(9.0))
    set_tc_vmerge(tcs_7[2], 'continue')

    # Ind 3.1 con fórmula TAM
    omml_tam = mathml_to_omml(FORMULAS_MML["tam_total"])
    set_tc_content(tcs_6[3], t5, [
        [("Aceptación del proceso", True, False)],
        omml_tam,
        "Grado de conformidad del personal con el flujo operativo de trabajo."
    ], font_size=Pt(8.5))
    set_tc_content(tcs_6[4], t5, [
        [("Escala de Likert (1 a 5)", True, False)],
        "Rango total: 8 a 40 puntos",
        "Instrumento: Cuestionario TAM"
    ], font_size=Pt(8.5))

    set_tc_content(tcs_7[3], t5, [
        [("Utilidad percibida", True, False)],
        "Percepción del usuario sobre el beneficio del sistema en sus labores."
    ], font_size=Pt(8.5))
    set_tc_content(tcs_7[4], t5, [
        [("Escala de Likert (1 a 5)", True, False)],
        "Rango total: 8 a 40 puntos",
        "Instrumento: Cuestionario TAM"
    ], font_size=Pt(8.5))

    aplicar_bordes_apa7(t5)

    # =========================================================================
    # PARTE 3: TABLA 8 (INSTRUMENTOS DE RECOLECCIÓN DE DATOS - ÍNDICE 7)
    # =========================================================================
    print("Reestructurando Tabla 8 con APA 7...")
    t8 = doc.tables[7]
    tcs_8_0 = get_row_tcs(t8, 0)
    set_tc_content(tcs_8_0[0], t8, [("Instrumento", True, False)], font_size=Pt(9.5), align=WD_ALIGN_PARAGRAPH.CENTER)
    set_tc_content(tcs_8_0[1], t8, [("Descripción y estructura operativa", True, False)], font_size=Pt(9.5), align=WD_ALIGN_PARAGRAPH.CENTER)
    set_tc_content(tcs_8_0[2], t8, [("Dimensión evaluada", True, False)], font_size=Pt(9.5), align=WD_ALIGN_PARAGRAPH.CENTER)

    # Instrumento 1
    tcs_8_1 = get_row_tcs(t8, 1)
    set_tc_content(tcs_8_1[0], t8, [
        [("Instrumento N° 01:", True, False)],
        "Ficha de observación de tiempos cronometrados"
    ], font_size=Pt(9.0))
    set_tc_content(tcs_8_1[1], t8, [
        "Registro estructurado para el cronometraje de tareas operativas en minutos. Permite registrar la hora de inicio, hora de término y duración neta para el registro de movimientos y la emisión de vales de salida de vacunas, registrando operador y centro de acopio."
    ], font_size=Pt(8.5))
    set_tc_content(tcs_8_1[2], t8, [
        [("Oportunidad de procesamiento", True, False)],
        "(Tiempos de registro y de emisión de vales)"
    ], font_size=Pt(8.5))

    # Instrumento 2
    tcs_8_2 = get_row_tcs(t8, 2)
    set_tc_content(tcs_8_2[0], t8, [
        [("Instrumento N° 02:", True, False)],
        "Ficha de cotejo documental de consistencia"
    ], font_size=Pt(9.0))
    set_tc_content(tcs_8_2[1], t8, [
        "Instrumento de auditoría documental para verificar la conformidad de los registros respecto a criterios de exactitud: tipo de movimiento, denominación de la vacuna, número de lote, cantidad, fecha, destino, responsable y documento de sustento. Asimismo, evalúa la correspondencia entre cantidades programadas y entregadas."
    ], font_size=Pt(8.5))
    set_tc_content(tcs_8_2[2], t8, [
        [("Consistencia documental", True, False)],
        "(Registros conformes y concordancia de cantidades)"
    ], font_size=Pt(8.5))

    # Instrumento 3
    tcs_8_3 = get_row_tcs(t8, 3)
    set_tc_content(tcs_8_3[0], t8, [
        [("Instrumento N° 03:", True, False)],
        "Cuestionario de satisfacción del usuario (TAM)"
    ], font_size=Pt(9.0))
    set_tc_content(tcs_8_3[1], t8, [
        "Cuestionario estructurado bajo escala de Likert de 5 niveles (1: Muy en desacuerdo a 5: Muy de acuerdo), fundamentado en el Modelo de Aceptación Tecnológica de Davis (1989). Consta de 8 reactivos distribuidos en dos subescalas: Aceptación del proceso (4 reactivos) y Utilidad percibida (4 reactivos)."
    ], font_size=Pt(8.5))
    set_tc_content(tcs_8_3[2], t8, [
        [("Satisfacción del usuario", True, False)],
        "(Aceptación y utilidad percibida)"
    ], font_size=Pt(8.5))

    aplicar_bordes_apa7(t8)

    # =========================================================================
    # PARTE 4: INSERCIÓN DE ECUACIONES NATIVAS EN EL CUERPO DE METODOLOGÍA
    # =========================================================================
    print("Insertando ecuaciones nativas OMML en el cuerpo capitular...")

    # 4.1 Esquema del diseño preexperimental (P413)
    # Reemplazar texto simple 'G: O₁ — X — O₂' por ecuación OMML centrada
    p413 = doc.paragraphs[413]
    actualizar_parrafo(p413, [], align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(6), space_after=Pt(6), line_spacing=1.15, indent=Inches(0))
    p413._p.append(mathml_to_omml(FORMULAS_MML["diseno_preexp"]))

    # 4.2 Nota de Tabla 8 (P478)
    actualizar_parrafo(doc.paragraphs[478], [
        ("Nota. ", True, False, Pt(10)),
        ("Los tres instrumentos han sido diseñados para responder a las dimensiones de oportunidad de procesamiento, consistencia documental y satisfacción del usuario. Serán sometidos a validación por juicio de expertos mediante el coeficiente V de Aiken e índice de validez de contenido previo a su aplicación en campo.", False, False, Pt(10))
    ], align=WD_ALIGN_PARAGRAPH.LEFT, indent=Inches(0), space_after=Pt(12), line_spacing=1.5)

    # 4.3 Medición del tiempo de registro (P486)
    p486 = doc.paragraphs[486]
    actualizar_parrafo(p486, [
        ("El tiempo de registro de movimiento se cuantifica en minutos decimales desde el inicio de la captura o digitación de los datos hasta la culminación formal y balance de la transacción en el kardex institucional, expresándose mediante la siguiente relación:", False, False)
    ])
    p_eq_treg = insertar_parrafo_ecuacion_despues(p486, doc, "t_reg")
    p_txt_treg_post = insertar_parrafo_texto_despues(p_eq_treg, doc, [
        ("En caso de procesarse varios registros continuos en una misma jornada, se calculará el tiempo medio dividiendo la duración total acumulada entre el número de movimientos formalizados.", False, False)
    ])

    # 4.4 Medición del tiempo de emisión de vale (desplazado por inserciones previas)
    def find_para_index(texto_clave):
        for idx, p in enumerate(doc.paragraphs):
            if texto_clave in p.text:
                return idx
        return -1

    p_vale_idx = find_para_index("Medición del tiempo de emisión de vale de entrega")
    p_vale_desc = doc.paragraphs[p_vale_idx + 1]
    actualizar_parrafo(p_vale_desc, [
        ("El tiempo de emisión de comprobante de salida o vale se cuantifica en minutos decimales desde la recepción del requerimiento hasta la formalización, visualización y exportación del vale oficial de salida en formato digital o impreso, calculándose de acuerdo con:", False, False)
    ])
    p_eq_tvale = insertar_parrafo_ecuacion_despues(p_vale_desc, doc, "t_vale")

    # 4.5 Consistencia documental
    p_consist_idx = find_para_index("Medición de la consistencia documental")
    p_consist_desc = doc.paragraphs[p_consist_idx + 1]
    actualizar_parrafo(p_consist_desc, [
        ("La consistencia documental se evaluará mediante la Ficha de Cotejo Documental N° 02 sobre muestras de transacciones de kardex y vales oficiales de salida. Para el indicador de porcentaje de registros sin discrepancias (RSD), se verificará la conformidad de cada transacción evaluando los ocho aspectos técnicos obligatorios: tipo de movimiento, denominación normalizada de la vacuna, número de lote, cantidad de dosis, fecha completa, establecimiento de destino, responsable identificado y documento de respaldo. Un registro se clasifica como conforme si satisface la totalidad de dichos criterios, calculándose el indicador mediante la siguiente fórmula:", False, False)
    ])
    p_eq_rsd = insertar_parrafo_ecuacion_despues(p_consist_desc, doc, "rsd")
    p_txt_cpe_intro = insertar_parrafo_texto_despues(p_eq_rsd, doc, [
        ("Asimismo, para el indicador de concordancia entre cantidad programada y entregada (CPE), se cotejará el volumen de dosis despachadas en los vales de salida frente a los requerimientos mensuales programados por las microredes, según la siguiente expresión:", False, False)
    ])
    p_eq_cpe = insertar_parrafo_ecuacion_despues(p_txt_cpe_intro, doc, "cpe")

    # 4.6 Validez del instrumento
    p_validez_idx = find_para_index("Validez del instrumento:")
    p_validez_desc = doc.paragraphs[p_validez_idx + 1]
    actualizar_parrafo(p_validez_desc, [
        ("Los instrumentos serán validados mediante juicio de expertos con un panel integrado por tres docentes especialistas de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Nacional José María Arguedas, evaluando pertinencia, relevancia y claridad para cada ítem. La cuantificación de la validez de contenido se realizará mediante el coeficiente V de Aiken, cuya expresión matemática corresponde a:", False, False)
    ])
    p_eq_aiken = insertar_parrafo_ecuacion_despues(p_validez_desc, doc, "aiken_v")
    p_txt_aiken_post = insertar_parrafo_texto_despues(p_eq_aiken, doc, [
        ("donde S representa la sumatoria de las diferencias entre la calificación asignada por cada juez y la calificación mínima posible de la escala, n es el número de jueces expertos (n = 3), y c es el número de valores de la escala de evaluación. Se considerarán válidos aquellos ítems con valores V ≥ 0.80 y significancia estadística p < 0.05, complementándose con el índice de validez de contenido (IVC ≥ 0.80 según Tristán-López, 2008).", False, False)
    ])

    # 4.7 Confiabilidad del instrumento
    p_confiab_idx = find_para_index("Confiabilidad del instrumento:")
    p_confiab_desc = doc.paragraphs[p_confiab_idx + 1]
    actualizar_parrafo(p_confiab_desc, [
        ("Para el Cuestionario de Satisfacción del Usuario (Instrumento N° 03), se calculará el coeficiente Alfa de Cronbach para determinar la consistencia interna de los 8 reactivos de escala Likert, estableciéndose como umbral de confiabilidad admisible un valor α ≥ 0.80, calculado mediante la fórmula:", False, False)
    ])
    p_eq_cronbach = insertar_parrafo_ecuacion_despues(p_confiab_desc, doc, "cronbach_alpha")
    p_txt_cronbach_post = insertar_parrafo_texto_despues(p_eq_cronbach, doc, [
        ("donde k representa el número de reactivos analizados (k = 8), s_i² corresponde a la varianza de cada ítem individual y s_t² representa la varianza total de las puntuaciones de la escala. Para las fichas cronométricas y de cotejo documental, la confiabilidad se asegurará mediante la estandarización estricta del protocolo de observación y la verificación de concordancia inter-observador.", False, False)
    ])

    # 4.8 Análisis inferencial
    p_inferencial_idx = find_para_index("b) Análisis inferencial:")
    p_inferencial_desc = doc.paragraphs[p_inferencial_idx + 1]
    actualizar_parrafo(p_inferencial_desc, [
        ("Se aplicará la prueba de Shapiro-Wilk como revisión preliminar de normalidad de las diferencias pareadas entre pretest y postest debido a que la población censal es reducida (n = 14 ≤ 50), donde las diferencias individuales se definen como:", False, False)
    ])
    p_eq_dif = insertar_parrafo_ecuacion_despues(p_inferencial_desc, doc, "dif_pareadas")
    p_txt_dif_post = insertar_parrafo_texto_despues(p_eq_dif, doc, [
        ("En caso de corroborarse la distribución normal de las diferencias (p > 0.05), se aplicará la prueba paramétrica t de Student para muestras relacionadas; de no cumplirse dicho supuesto (p ≤ 0.05), se empleará la prueba no paramétrica de rangos con signo de Wilcoxon, fijándose un nivel de significancia de α = 0.05 y un nivel de confianza del 95%.", False, False)
    ])

    # =========================================================================
    # PARTE 5: TABLA 12 (ANEXO 1: MATRIZ DE CONSISTENCIA - ÍNDICE 11)
    # =========================================================================
    print("Reestructurando Tabla 12 (Matriz de Consistencia con fórmulas OMML nativas)...")
    t12 = doc.tables[11]

    # Encabezados LIMPIOS (CERO TrueFalse)
    headers_t12 = ["VARIABLES", "PROBLEMAS", "OBJETIVOS", "HIPÓTESIS", "DIMENSIONES", "INDICADORES Y ESCALAS", "METODOLOGÍA"]
    tcs_12_0 = get_row_tcs(t12, 0)
    for c_idx, h_text in enumerate(headers_t12):
        set_tc_content(tcs_12_0[c_idx], t12, [(h_text, True, False)],
                       font_size=Pt(9.0), align=WD_ALIGN_PARAGRAPH.CENTER)

    # Fila 1: Variable Independiente
    tcs_12_1 = get_row_tcs(t12, 1)
    set_tc_content(tcs_12_1[0], t12, [
        [("VARIABLE INDEPENDIENTE:", True, False)],
        "Sistema web SIVAC"
    ], font_size=Pt(8.5))

    set_tc_content(tcs_12_1[1], t12, [
        [("Problema General:", True, False)],
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025?"
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_1[2], t12, [
        [("Objetivo General:", True, False)],
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025."
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_1[3], t12, [
        [("Hipótesis General:", True, False)],
        "La aplicación del sistema \"SIVAC\" mejora significativamente la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025."
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_1[4], t12, [
        [("Implementación del sistema", True, False)]
    ], font_size=Pt(8.5))

    set_tc_content(tcs_12_1[5], t12, [
        [("Condición operativa:", True, False)],
        "• Sin sistema SIVAC (Pretest)",
        "• Con sistema SIVAC (Postest)",
        "Escala: Dicotómica nominal"
    ], font_size=Pt(8.0))

    # Metodología unificada para Filas 1 a 4 con ecuación OMML del diseño
    omml_diseno_t12 = mathml_to_omml(FORMULAS_MML["diseno_preexp"])
    metodologia_lineas = [
        [("Tipo:", True, False), (" Aplicada")],
        [("Enfoque:", True, False), (" Cuantitativo")],
        [("Nivel:", True, False), (" Explicativo")],
        [("Diseño preexperimental:", True, False)],
        omml_diseno_t12,
        [("Población censal:", True, False), (" N = n = 14 trabajadores")],
        [("Técnicas:", True, False), (" Observación, análisis documental y encuesta")],
        [("Instrumentos:", True, False), (" Fichas cronométricas, de cotejo y cuestionario TAM")],
        [("Análisis estadístico:", True, False), (" Shapiro-Wilk, Wilcoxon pareado y t de Student")]
    ]

    set_tc_vmerge(tcs_12_1[6], 'restart')
    set_tc_content(tcs_12_1[6], t12, metodologia_lineas, font_size=Pt(7.5))
    for r in range(2, 5):
        tcs_r = get_row_tcs(t12, r)
        set_tc_vmerge(tcs_r[6], 'continue')

    # Filas 2 a 4: Variable Dependiente
    tcs_12_2 = get_row_tcs(t12, 2)
    tcs_12_3 = get_row_tcs(t12, 3)
    tcs_12_4 = get_row_tcs(t12, 4)

    set_tc_vmerge(tcs_12_2[0], 'restart')
    set_tc_content(tcs_12_2[0], t12, [
        [("VARIABLE DEPENDIENTE:", True, False)],
        "Gestión de movimientos de vacunas"
    ], font_size=Pt(8.5))
    set_tc_vmerge(tcs_12_3[0], 'continue')
    set_tc_vmerge(tcs_12_4[0], 'continue')

    # Fila 2: Dimensión 1 Oportunidad
    set_tc_content(tcs_12_2[1], t12, [
        [("Problema Específico 1:", True, False)],
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?"
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_2[2], t12, [
        [("Objetivo Específico 1:", True, False)],
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_2[3], t12, [
        [("Hipótesis Específica 1:", True, False)],
        "La aplicación del sistema \"SIVAC\" mejora significativamente la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_2[4], t12, [
        [("Oportunidad de procesamiento", True, False)]
    ], font_size=Pt(8.5))

    omml_treg_t12 = mathml_to_omml(FORMULAS_MML["t_reg"])
    omml_tvale_t12 = mathml_to_omml(FORMULAS_MML["t_vale"])
    set_tc_content(tcs_12_2[5], t12, [
        [("Tiempo de registro de movimientos:", True, False)],
        omml_treg_t12,
        [("Tiempo de emisión de vales:", True, False)],
        omml_tvale_t12,
        "Escala: Razón / Continua (minutos).",
        "Instrumento: Ficha cronométrica."
    ], font_size=Pt(8.0))

    # Fila 3: Dimensión 2 Consistencia
    set_tc_content(tcs_12_3[1], t12, [
        [("Problema Específico 2:", True, False)],
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?"
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_3[2], t12, [
        [("Objetivo Específico 2:", True, False)],
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_3[3], t12, [
        [("Hipótesis Específica 2:", True, False)],
        "La aplicación del sistema \"SIVAC\" mejora significativamente la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_3[4], t12, [
        [("Consistencia documental", True, False)]
    ], font_size=Pt(8.5))

    omml_rsd_t12 = mathml_to_omml(FORMULAS_MML["rsd"])
    omml_cpe_t12 = mathml_to_omml(FORMULAS_MML["cpe"])
    set_tc_content(tcs_12_3[5], t12, [
        [("Registros sin discrepancias:", True, False)],
        omml_rsd_t12,
        [("Concordancia programada vs entregada:", True, False)],
        omml_cpe_t12,
        "Escala: Razón / Proporción (%).",
        "Instrumento: Ficha de cotejo documental."
    ], font_size=Pt(8.0))

    # Fila 4: Dimensión 3 Satisfacción
    set_tc_content(tcs_12_4[1], t12, [
        [("Problema Específico 3:", True, False)],
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?"
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_4[2], t12, [
        [("Objetivo Específico 3:", True, False)],
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_4[3], t12, [
        [("Hipótesis Específica 3:", True, False)],
        "La aplicación del sistema \"SIVAC\" mejora significativamente la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_4[4], t12, [
        [("Satisfacción del usuario", True, False)]
    ], font_size=Pt(8.5))

    omml_tam_t12 = mathml_to_omml(FORMULAS_MML["tam_total"])
    set_tc_content(tcs_12_4[5], t12, [
        [("Aceptación del proceso operativo (AP)", True, False)],
        [("Utilidad percibida sanitaria (UP)", True, False)],
        omml_tam_t12,
        "Escala: Ordinal (Likert 1 a 5, Baremo 8-40).",
        "Instrumento: Cuestionario TAM."
    ], font_size=Pt(8.0))

    aplicar_bordes_apa7(t12)

    # =========================================================================
    # PARTE 6: GUARDADO Y CONTROL DE CALIDAD FINAL
    # =========================================================================
    out_v2 = "salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V2.docx"
    print(f"\nGuardando documento con fórmulas nativas en: {out_v2}...")
    doc.save(out_v2)
    print("¡PROCESAMIENTO QUIRÚRGICO v2.2 COMPLETADO EXITOSAMENTE!")

if __name__ == '__main__':
    procesar_actualizacion_v2_2()
