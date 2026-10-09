#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB - Actualizador Quirúrgico Limpio v2.1 de PROYECTO_TESIS.docx
Elimina absolutamente todos los tokens artificiales (cero DEC-007, cero [C1]-[C8])
y sustituye la redacción robótica/defensiva por prosa académica formal, sobria y humana
para la Universidad Nacional José María Arguedas (UNAJMA).

Guarda exclusivamente en salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V2.docx
preservando la inmutabilidad de referencias/proyecto_base/.
"""

import sys
import docx
from docx.shared import Pt, Inches
from docx.table import _Cell
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

FUENTE = "Times New Roman"

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

def set_tc_content(tc, table, lines, font_size=Pt(9.5), bold_first=False, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell = _Cell(tc, table)
    cell.text = ""
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    for idx, item in enumerate(lines):
        p = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()
        p.alignment = align
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(1.5)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.first_line_indent = Inches(0)

        if isinstance(item, (list, tuple)):
            for seg in item:
                if isinstance(seg, tuple) and len(seg) >= 3:
                    t_text, t_bold, t_italic = seg[0], seg[1], seg[2]
                elif isinstance(seg, tuple) and len(seg) == 2:
                    t_text, t_bold, t_italic = seg[0], seg[1], False
                else:
                    t_text, t_bold, t_italic = str(seg), False, False
                run = p.add_run(t_text)
                run.font.name = FUENTE
                run.font.size = font_size
                run.font.bold = t_bold
                run.font.italic = t_italic
        else:
            run = p.add_run(str(item))
            run.font.name = FUENTE
            run.font.size = font_size
            if idx == 0 and bold_first:
                run.font.bold = True

def aplicar_bordes_apa7(table):
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

def actualizar_parrafo(p, runs_data, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=Pt(6), line_spacing=1.5, indent=Inches(0.5)):
    p.text = ""
    p.alignment = align
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = space_after
    p.paragraph_format.first_line_indent = indent

    for item in runs_data:
        if isinstance(item, tuple):
            text = item[0]
            bold = item[1] if len(item) > 1 else False
            italic = item[2] if len(item) > 2 else False
            size = item[3] if len(item) > 3 else Pt(12)
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

def procesar_actualizacion():
    doc_path = "salidas/archivo/PROYECTO_TESIS_ORIGINAL_BACKUP.docx"
    print(f"Cargando documento base de respaldo: {doc_path}...")
    doc = docx.Document(doc_path)

    # =========================================================================
    # PARTE 1: PÁRRAFOS 376 A 386 (SECCIÓN 3.3 OPERACIONALIZACIÓN DE VARIABLES)
    # =========================================================================
    print("Actualizando Párrafos 376 a 386 (Sección 3.3 con redacción sobria y humana)...")

    # P376: Título 3.3
    actualizar_parrafo(doc.paragraphs[376], [("3.3 Operacionalización de variables", True, False)],
                       align=WD_ALIGN_PARAGRAPH.LEFT, indent=Inches(0), space_after=Pt(6))

    # P377: Introducción
    actualizar_parrafo(doc.paragraphs[377], [
        ("En la presente investigación se han identificado y definido dos variables de estudio:", False, False)
    ])

    # P378: Variable independiente
    actualizar_parrafo(doc.paragraphs[378], [("Variable independiente:", True, False)],
                       align=WD_ALIGN_PARAGRAPH.LEFT, indent=Inches(0), space_after=Pt(2))

    # P379: Sistema "SIVAC"
    actualizar_parrafo(doc.paragraphs[379], [
        ("Sistema web \"SIVAC\". ", True, False),
        ("Definida conceptualmente como una aplicación informática basada en arquitectura web para el registro, control, seguimiento y trazabilidad de los movimientos de biológicos en la red de frío de la Dirección de Salud Apurímac II (Sommerville, 2016; Pressman y Maxim, 2021). Operacionalmente, constituye la solución tecnológica implementada para sistematizar la gestión operativa de vacunas, evaluada a través de sus componentes de registro de movimientos, emisión de comprobantes y control de existencias frente al procedimiento tradicional previo.", False, False)
    ], indent=Inches(0.5))

    # P380: Vacío
    doc.paragraphs[380].text = ""

    # P381: Variable dependiente
    actualizar_parrafo(doc.paragraphs[381], [("Variable dependiente:", True, False)],
                       align=WD_ALIGN_PARAGRAPH.LEFT, indent=Inches(0), space_after=Pt(2))

    # P382: Gestión de movimientos de vacunas
    actualizar_parrafo(doc.paragraphs[382], [
        ("Gestión de movimientos de vacunas. ", True, False),
        ("Definida conceptualmente como el conjunto estructurado de procedimientos técnicos y administrativos orientados a registrar, controlar, reportar y verificar las entradas, salidas, saldos y distribución de vacunas e insumos, asegurando la trazabilidad de los biológicos y la disponibilidad de información oportuna (Ministerio de Salud, 2022). Operacionalmente, se evalúa mediante tres dimensiones: oportunidad de procesamiento (tiempos de registro y de emisión de vales), consistencia documental (registros sin discrepancias y concordancia de cantidades) y satisfacción del usuario (aceptación del proceso y utilidad percibida según el modelo de aceptación tecnológica).", False, False)
    ], indent=Inches(0.5))

    # P383: Vacío
    doc.paragraphs[383].text = ""

    # P384: Introducción a Tabla 5
    actualizar_parrafo(doc.paragraphs[384], [
        ("En la Tabla 5 se detalla la matriz de operacionalización de las variables consideradas en la presente investigación.", False, False)
    ], indent=Inches(0.5))

    # P385: Título Tabla 5
    actualizar_parrafo(doc.paragraphs[385], [
        ("Tabla 5\n", True, False, Pt(10)),
        ("Operacionalización de variables", False, True, Pt(10))
    ], align=WD_ALIGN_PARAGRAPH.LEFT, indent=Inches(0), space_after=Pt(4), line_spacing=1.0)

    # P386: Nota Tabla 5
    actualizar_parrafo(doc.paragraphs[386], [
        ("Nota. ", True, False, Pt(10)),
        ("Definiciones adaptadas de Sommerville (2016), Davis (1989) y Ministerio de Salud (2022). Escala de Likert: 1 = Muy en desacuerdo, 2 = En desacuerdo, 3 = Ni de acuerdo ni en desacuerdo, 4 = De acuerdo, 5 = Muy de acuerdo.", False, False, Pt(10))
    ], align=WD_ALIGN_PARAGRAPH.LEFT, indent=Inches(0), space_after=Pt(12), line_spacing=1.5)

    # =========================================================================
    # PARTE 2: TABLA 5 (OPERACIONALIZACIÓN DE VARIABLES - ÍNDICE 4)
    # =========================================================================
    print("Reestructurando Tabla 5 (Operacionalización de Variables limpia con APA 7)...")
    t5 = doc.tables[4]

    # Eliminar filas excedentes (reducir a 8 filas: 1 cabecera + 1 VI + 6 VD)
    while len(t5.rows) > 8:
        tr = t5.rows[-1]._tr
        t5._tbl.remove(tr)

    # Fila 0: Encabezados
    headers_t5 = ["Variable", "Definición conceptual", "Dimensiones", "Indicadores", "Escala / Unidad de medida"]
    tcs_0 = get_row_tcs(t5, 0)
    for c_idx, h_text in enumerate(headers_t5):
        set_tc_content(tcs_0[c_idx], t5, [([h_text, True, False])],
                       font_size=Pt(9.5), align=WD_ALIGN_PARAGRAPH.CENTER)

    # Fila 1: Variable Independiente
    tcs_1 = get_row_tcs(t5, 1)
    set_tc_vmerge(tcs_1[0], 'restart')
    set_tc_content(tcs_1[0], t5, [
        ([("Variable Independiente:", True, False)]),
        ("Sistema web SIVAC")
    ], font_size=Pt(9.0))

    set_tc_vmerge(tcs_1[1], 'restart')
    set_tc_content(tcs_1[1], t5, [
        ("Aplicación informática basada en plataforma web orientada al registro, control y seguimiento de las operaciones de ingreso, almacenamiento y distribución de vacunas en la Dirección de Salud Apurímac II.")
    ], font_size=Pt(8.5))

    set_tc_vmerge(tcs_1[2], 'restart')
    set_tc_content(tcs_1[2], t5, [
        ([("Implementación del sistema", True, False)])
    ], font_size=Pt(9.0))

    set_tc_vmerge(tcs_1[3], 'restart')
    set_tc_content(tcs_1[3], t5, [
        ("Adopción y uso del sistema web en la gestión de vacunas.")
    ], font_size=Pt(8.5))

    set_tc_vmerge(tcs_1[4], 'restart')
    set_tc_content(tcs_1[4], t5, [
        ([("Dicotómica nominal", True, False)]),
        ("0 = Sin sistema (Pretest)"),
        ("1 = Con sistema (Postest)")
    ], font_size=Pt(8.5))

    # Filas 2 a 7: Variable Dependiente
    vd_text = [
        ([("Variable Dependiente:", True, False)]),
        ("Gestión de movimientos de vacunas")
    ]
    def_vd = [
        ("Conjunto de procedimientos técnicos y administrativos orientados a programar, registrar, despachar y controlar el flujo de productos biológicos e insumos en la red de frío de la Dirección de Salud Apurímac II.")
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
    set_tc_content(tcs_2[2], t5, [([("Oportunidad de procesamiento", True, False)])], font_size=Pt(9.0))
    set_tc_vmerge(tcs_3[2], 'continue')

    set_tc_content(tcs_2[3], t5, [
        ([("Tiempo de registro de movimiento de vacunas", True, False)]),
        ("Duración en minutos desde el inicio hasta la culminación del registro.")
    ], font_size=Pt(8.5))
    set_tc_content(tcs_2[4], t5, [
        ([("Minutos (min)", True, False)]),
        ("Razón / Continua"),
        ("Ficha cronométrica")
    ], font_size=Pt(8.5))

    set_tc_content(tcs_3[3], t5, [
        ([("Tiempo de emisión de comprobante de salida / vale", True, False)]),
        ("Duración en minutos para la generación y emisión del vale de entrega.")
    ], font_size=Pt(8.5))
    set_tc_content(tcs_3[4], t5, [
        ([("Minutos (min)", True, False)]),
        ("Razón / Continua"),
        ("Ficha cronométrica")
    ], font_size=Pt(8.5))

    # Dimensión 2: Consistencia documental (Filas 4 y 5)
    tcs_4 = get_row_tcs(t5, 4)
    tcs_5 = get_row_tcs(t5, 5)
    set_tc_vmerge(tcs_4[2], 'restart')
    set_tc_content(tcs_4[2], t5, [([("Consistencia documental", True, False)])], font_size=Pt(9.0))
    set_tc_vmerge(tcs_5[2], 'continue')

    set_tc_content(tcs_4[3], t5, [
        ([("Porcentaje de registros sin discrepancias", True, False)]),
        ("Proporción de transacciones sin inconsistencias de lote, cantidad, fecha o destino.")
    ], font_size=Pt(8.5))
    set_tc_content(tcs_4[4], t5, [
        ([("Porcentaje (%)", True, False)]),
        ("Razón / Proporción"),
        ("Ficha de cotejo")
    ], font_size=Pt(8.5))

    set_tc_content(tcs_5[3], t5, [
        ([("Concordancia entre cantidad programada y entregada", True, False)]),
        ("Nivel de coincidencia entre las dosis requeridas y las efectivamente despachadas.")
    ], font_size=Pt(8.5))
    set_tc_content(tcs_5[4], t5, [
        ([("Porcentaje (%)", True, False)]),
        ("Razón / Proporción"),
        ("Ficha de cotejo")
    ], font_size=Pt(8.5))

    # Dimensión 3: Satisfacción del usuario (Filas 6 y 7)
    tcs_6 = get_row_tcs(t5, 6)
    tcs_7 = get_row_tcs(t5, 7)
    set_tc_vmerge(tcs_6[2], 'restart')
    set_tc_content(tcs_6[2], t5, [([("Satisfacción del usuario", True, False)])], font_size=Pt(9.0))
    set_tc_vmerge(tcs_7[2], 'continue')

    set_tc_content(tcs_6[3], t5, [
        ([("Aceptación del proceso", True, False)]),
        ("Grado de conformidad del personal con el flujo operativo de trabajo.")
    ], font_size=Pt(8.5))
    set_tc_content(tcs_6[4], t5, [
        ([("Escala de Likert (1 a 5)", True, False)]),
        ("Ordinal"),
        ("Cuestionario TAM")
    ], font_size=Pt(8.5))

    set_tc_content(tcs_7[3], t5, [
        ([("Utilidad percibida", True, False)]),
        ("Percepción del usuario sobre el beneficio del sistema en sus labores.")
    ], font_size=Pt(8.5))
    set_tc_content(tcs_7[4], t5, [
        ([("Escala de Likert (1 a 5)", True, False)]),
        ("Ordinal"),
        ("Cuestionario TAM")
    ], font_size=Pt(8.5))

    aplicar_bordes_apa7(t5)

    # =========================================================================
    # PARTE 3: TABLA 8 (INSTRUMENTOS DE RECOLECCIÓN DE DATOS - ÍNDICE 7)
    # =========================================================================
    print("Reestructurando Tabla 8 (Instrumentos con redacción sobria y sin [C1]-[C8])...")
    t8 = doc.tables[7]
    tcs_8_0 = get_row_tcs(t8, 0)
    set_tc_content(tcs_8_0[0], t8, [([("Instrumento", True, False)])], font_size=Pt(9.5), align=WD_ALIGN_PARAGRAPH.CENTER)
    set_tc_content(tcs_8_0[1], t8, [([("Descripción y estructura operativa", True, False)])], font_size=Pt(9.5), align=WD_ALIGN_PARAGRAPH.CENTER)
    set_tc_content(tcs_8_0[2], t8, [([("Dimensión evaluada", True, False)])], font_size=Pt(9.5), align=WD_ALIGN_PARAGRAPH.CENTER)

    # Instrumento 1
    tcs_8_1 = get_row_tcs(t8, 1)
    set_tc_content(tcs_8_1[0], t8, [
        ([("Instrumento N° 01:", True, False)]),
        ("Ficha de observación de tiempos cronometrados")
    ], font_size=Pt(9.0))
    set_tc_content(tcs_8_1[1], t8, [
        ("Registro estructurado para el cronometraje de tareas operativas en minutos. Permite registrar la hora de inicio, hora de término y duración neta para el registro de movimientos y la emisión de vales de salida de vacunas, registrando operador y centro de acopio.")
    ], font_size=Pt(8.5))
    set_tc_content(tcs_8_1[2], t8, [
        ([("Oportunidad de procesamiento", True, False)]),
        ("(Tiempos de registro y de emisión de vales)")
    ], font_size=Pt(8.5))

    # Instrumento 2
    tcs_8_2 = get_row_tcs(t8, 2)
    set_tc_content(tcs_8_2[0], t8, [
        ([("Instrumento N° 02:", True, False)]),
        ("Ficha de cotejo documental de consistencia")
    ], font_size=Pt(9.0))
    set_tc_content(tcs_8_2[1], t8, [
        ("Instrumento de auditoría documental para verificar la conformidad de los registros respecto a criterios de exactitud: tipo de movimiento, denominación de la vacuna, número de lote, cantidad, fecha, destino, responsable y documento de sustento. Asimismo, evalúa la correspondencia entre cantidades programadas y entregadas.")
    ], font_size=Pt(8.5))
    set_tc_content(tcs_8_2[2], t8, [
        ([("Consistencia documental", True, False)]),
        ("(Registros conformes y concordancia de cantidades)")
    ], font_size=Pt(8.5))

    # Instrumento 3
    tcs_8_3 = get_row_tcs(t8, 3)
    set_tc_content(tcs_8_3[0], t8, [
        ([("Instrumento N° 03:", True, False)]),
        ("Cuestionario de satisfacción del usuario (TAM)")
    ], font_size=Pt(9.0))
    set_tc_content(tcs_8_3[1], t8, [
        ("Cuestionario estructurado bajo escala de Likert de 5 niveles (1: Muy en desacuerdo a 5: Muy de acuerdo), fundamentado en el Modelo de Aceptación Tecnológica de Davis (1989). Consta de 8 reactivos distribuidos en dos subescalas: Aceptación del proceso (4 reactivos) y Utilidad percibida (4 reactivos).")
    ], font_size=Pt(8.5))
    set_tc_content(tcs_8_3[2], t8, [
        ([("Satisfacción del usuario", True, False)]),
        ("(Aceptación y utilidad percibida)")
    ], font_size=Pt(8.5))

    aplicar_bordes_apa7(t8)

    # =========================================================================
    # PARTE 4: PÁRRAFOS 478, 490, 498 Y 500 (CAPÍTULO IV METODOLOGÍA)
    # =========================================================================
    print("Actualizando Párrafos 478, 490, 498 y 500 (Metodología limpia)...")

    # P478: Nota Tabla 8
    actualizar_parrafo(doc.paragraphs[478], [
        ("Nota. ", True, False, Pt(10)),
        ("Los tres instrumentos han sido diseñados para responder a las dimensiones de oportunidad de procesamiento, consistencia documental y satisfacción del usuario. Serán sometidos a validación por juicio de expertos mediante el coeficiente V de Aiken e índice de validez de contenido previo a su aplicación en campo.", False, False, Pt(10))
    ], align=WD_ALIGN_PARAGRAPH.LEFT, indent=Inches(0), space_after=Pt(12), line_spacing=1.5)

    # P490: Consistencia documental sin [C1]-[C8]
    actualizar_parrafo(doc.paragraphs[490], [
        ("La consistencia documental se evaluará mediante la Ficha de Cotejo Documental N° 02 sobre muestras de transacciones de kardex y comprobantes oficiales de salida. Para el indicador de registros sin discrepancias, se verificará la conformidad de cada transacción evaluando los siguientes aspectos: tipo de movimiento registrado, denominación del producto biológico según esquema oficial, número de lote, cantidad de dosis coincidente con el documento de entrega, fecha cronológicamente consistente, establecimiento de destino individualizado, personal responsable identificado y documento de sustento asociado. Un registro se considera conforme cuando satisface la totalidad de estos aspectos, y no conforme cuando presenta al menos una inconsistencia o dato faltante. Asimismo, para el indicador de concordancia entre cantidad programada y entregada, se cotejará el volumen de dosis despachadas en los vales de salida frente a los requerimientos mensuales programados.", False, False)
    ], indent=Inches(0.5))

    # P498: Validez de expertos sin mención informal a Cóndor Tinoco
    actualizar_parrafo(doc.paragraphs[498], [
        ("Los instrumentos serán validados mediante juicio de expertos con un panel integrado por tres docentes especialistas de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Nacional José María Arguedas, empleando los formatos estandarizados institucionales de evaluación. Se calificarán los criterios de pertinencia, relevancia y claridad para cada ítem, cuantificando la validez de contenido mediante el coeficiente V de Aiken (esperándose valores V ≥ 0.80 con significancia p < 0.05) y el índice de validez de contenido (IVC ≥ 0.80 según Tristán-López, 2008).", False, False)
    ], indent=Inches(0.5))

    # P500: Confiabilidad
    actualizar_parrafo(doc.paragraphs[500], [
        ("Para el Cuestionario de Satisfacción del Usuario (Instrumento N° 03), se calculará el coeficiente Alfa de Cronbach para determinar la consistencia interna de los 8 reactivos de escala Likert, estableciéndose como umbral de confiabilidad admisible un valor α ≥ 0.80. Para las fichas de observación cronométrica y de cotejo documental, la confiabilidad se asegurará mediante la estandarización del protocolo de medición y la verificación de concordancia inter-observador.", False, False)
    ], indent=Inches(0.5))

    # =========================================================================
    # PARTE 5: TABLA 12 (ANEXO 1: MATRIZ DE CONSISTENCIA - ÍNDICE 11)
    # =========================================================================
    print("Reestructurando Tabla 12 (Matriz de Consistencia limpia con APA 7)...")
    t12 = doc.tables[11]

    # Encabezados
    headers_t12 = ["VARIABLES", "PROBLEMAS", "OBJETIVOS", "HIPÓTESIS", "DIMENSIONES", "INDICADORES Y ESCALAS", "METODOLOGÍA"]
    tcs_12_0 = get_row_tcs(t12, 0)
    for c_idx, h_text in enumerate(headers_t12):
        set_tc_content(tcs_12_0[c_idx], t12, [([h_text, True, False])],
                       font_size=Pt(9.0), align=WD_ALIGN_PARAGRAPH.CENTER)

    # Fila 1: Variable Independiente
    tcs_12_1 = get_row_tcs(t12, 1)
    set_tc_content(tcs_12_1[0], t12, [
        ([("VARIABLE INDEPENDIENTE:", True, False)]),
        ("Sistema web SIVAC")
    ], font_size=Pt(8.5))

    set_tc_content(tcs_12_1[1], t12, [
        ([("Problema General:", True, False)]),
        ("¿En qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025?")
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_1[2], t12, [
        ([("Objetivo General:", True, False)]),
        ("Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025.")
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_1[3], t12, [
        ([("Hipótesis General:", True, False)]),
        ("La aplicación del sistema \"SIVAC\" mejora significativamente la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025.")
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_1[4], t12, [
        ([("Implementación del sistema", True, False)])
    ], font_size=Pt(8.5))

    set_tc_content(tcs_12_1[5], t12, [
        ([("Condición operativa:", True, False)]),
        ("• Sin sistema SIVAC (Pretest)"),
        ("• Con sistema SIVAC (Postest)"),
        ("Escala: Dicotómica nominal")
    ], font_size=Pt(8.0))

    # Metodología unificada para Fila 1 a 4
    metodologia_lineas = [
        ([("Tipo:", True, False), (" Aplicada")]),
        ([("Enfoque:", True, False), (" Cuantitativo")]),
        ([("Nivel:", True, False), (" Explicativo")]),
        ([("Diseño:", True, False), (" Preexperimental con pretest y postest en un solo grupo (O₁ ⟶ X ⟶ O₂)")]),
        ([("Población y muestra:", True, False), (" Censal (N = n = 14 trabajadores de inmunizaciones)")]),
        ([("Técnicas:", True, False), (" Observación, análisis documental y encuesta")]),
        ([("Instrumentos:", True, False), (" Fichas cronométricas, de cotejo y cuestionario TAM")]),
        ([("Análisis de datos:", True, False), (" Shapiro-Wilk, Wilcoxon pareado y t de Student")])
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
        ([("VARIABLE DEPENDIENTE:", True, False)]),
        ("Gestión de movimientos de vacunas")
    ], font_size=Pt(8.5))
    set_tc_vmerge(tcs_12_3[0], 'continue')
    set_tc_vmerge(tcs_12_4[0], 'continue')

    # Fila 2: Dimensión 1 Oportunidad
    set_tc_content(tcs_12_2[1], t12, [
        ([("Problema Específico 1:", True, False)]),
        ("¿En qué medida la aplicación del sistema \"SIVAC\" mejora la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?")
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_2[2], t12, [
        ([("Objetivo Específico 1:", True, False)]),
        ("Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.")
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_2[3], t12, [
        ([("Hipótesis Específica 1:", True, False)]),
        ("La aplicación del sistema \"SIVAC\" mejora significativamente la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.")
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_2[4], t12, [
        ([("Oportunidad de procesamiento", True, False)])
    ], font_size=Pt(8.5))

    set_tc_content(tcs_12_2[5], t12, [
        ("• Tiempo de registro de movimientos (min)."),
        ("• Tiempo de emisión de vales (min)."),
        ("Escala: Razón / Continua."),
        ("Instrumento: Ficha cronométrica.")
    ], font_size=Pt(8.0))

    # Fila 3: Dimensión 2 Consistencia
    set_tc_content(tcs_12_3[1], t12, [
        ([("Problema Específico 2:", True, False)]),
        ("¿En qué medida la aplicación del sistema \"SIVAC\" mejora la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?")
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_3[2], t12, [
        ([("Objetivo Específico 2:", True, False)]),
        ("Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.")
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_3[3], t12, [
        ([("Hipótesis Específica 2:", True, False)]),
        ("La aplicación del sistema \"SIVAC\" mejora significativamente la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.")
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_3[4], t12, [
        ([("Consistencia documental", True, False)])
    ], font_size=Pt(8.5))

    set_tc_content(tcs_12_3[5], t12, [
        ("• Porcentaje de registros sin discrepancias (%)."),
        ("• Concordancia entre cantidad programada y entregada (%)."),
        ("Escala: Razón / Proporción."),
        ("Instrumento: Ficha de cotejo.")
    ], font_size=Pt(8.0))

    # Fila 4: Dimensión 3 Satisfacción
    set_tc_content(tcs_12_4[1], t12, [
        ([("Problema Específico 3:", True, False)]),
        ("¿En qué medida la aplicación del sistema \"SIVAC\" mejora la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?")
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_4[2], t12, [
        ([("Objetivo Específico 3:", True, False)]),
        ("Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.")
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_4[3], t12, [
        ([("Hipótesis Específica 3:", True, False)]),
        ("La aplicación del sistema \"SIVAC\" mejora significativamente la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.")
    ], font_size=Pt(8.0))

    set_tc_content(tcs_12_4[4], t12, [
        ([("Satisfacción del usuario", True, False)])
    ], font_size=Pt(8.5))

    set_tc_content(tcs_12_4[5], t12, [
        ("• Aceptación del proceso."),
        ("• Utilidad percibida."),
        ("Escala: Ordinal (Likert 1-5)."),
        ("Instrumento: Cuestionario TAM.")
    ], font_size=Pt(8.0))

    aplicar_bordes_apa7(t12)

    # Guardar en copia versionada en salidas/documentos/
    out_v2 = "salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V2.docx"
    print(f"Guardando documento versionado en: {out_v2}...")
    doc.save(out_v2)

    print("\n¡ACTUALIZACIÓN QUIRÚRGICA LIMPIA v2.1 COMPLETADA CON ÉXITO EN SALIDAS/DOCUMENTOS/!")

if __name__ == '__main__':
    procesar_actualizacion()
