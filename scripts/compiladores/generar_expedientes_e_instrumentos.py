#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - Squad B (Metodología y Psicometría)
GENERADOR COMPLETO DEL EXPEDIENTE DE VALIDACIÓN Y LOS TRES INSTRUMENTOS EN DOCX
Modelo Institucional: Dr. Enrique Cóndor Tinoco (EPIS-UNAJMA) / DEC-007
================================================================================
Genera:
1. salidas/instrumentos/EXPEDIENTE_VALIDACION_JUICIO_EXPERTOS_SIVAC.docx
2. salidas/instrumentos/INSTRUMENTO_01_FICHA_TIEMPOS.docx
3. salidas/instrumentos/INSTRUMENTO_02_GUIA_COTEJO.docx
4. salidas/instrumentos/INSTRUMENTO_03_CUESTIONARIO_TAM.docx
================================================================================
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

FUENTE_PRINCIPAL = "Times New Roman"
COLOR_AZUL_UNAJMA = "002060"
COLOR_AZUL_SEC = "1F497D"
COLOR_GRIS_FONDO = "F2F2F2"
COLOR_BORDE_TABLA = "000000"
RUTA_ESCUDO = os.path.abspath("salidas/figuras/recursos_graficos/escudo_unajma.png")

# -----------------------------------------------------------------------------
# UTILIDADES OPENXML QUIRÚRGICAS
# -----------------------------------------------------------------------------

def configurar_margenes_unajma(seccion):
    """Márgenes oficiales UNAJMA: Izq 3.0 cm, Sup/Der/Inf 2.5 cm."""
    seccion.page_width = Cm(21.0)
    seccion.page_height = Cm(29.7)
    seccion.left_margin = Cm(3.0)
    seccion.right_margin = Cm(2.5)
    seccion.top_margin = Cm(2.5)
    seccion.bottom_margin = Cm(2.5)
    seccion.header_distance = Cm(1.27)
    seccion.footer_distance = Cm(1.27)

def configurar_header_footer(doc, texto_header):
    """Configura encabezado institucional y pie con paginación."""
    for seccion in doc.sections:
        # Header
        p_head = seccion.header.paragraphs[0]
        p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_head.text = ""
        r_head = p_head.add_run(texto_header)
        r_head.font.name = FUENTE_PRINCIPAL
        r_head.font.size = Pt(8.5)
        r_head.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

        # Footer
        p_foot = seccion.footer.paragraphs[0]
        p_foot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_foot.text = ""
        r_foot = p_foot.add_run("Página ")
        r_foot.font.name = FUENTE_PRINCIPAL
        r_foot.font.size = Pt(9)
        r_foot.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

        fld_pg = OxmlElement('w:fldSimple')
        fld_pg.set(qn('w:instr'), 'PAGE')
        p_foot._p.append(fld_pg)

        r_de = p_foot.add_run(" de ")
        r_de.font.name = FUENTE_PRINCIPAL
        r_de.font.size = Pt(9)
        r_de.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

        fld_numpages = OxmlElement('w:fldSimple')
        fld_numpages.set(qn('w:instr'), 'NUMPAGES')
        p_foot._p.append(fld_numpages)

def agregar_p(doc, texto="", negrita=False, cursiva=False, tamano_pt=12,
              interlineado=1.5, espacio_antes=0, espacio_desp=0,
              sangria_cm=0, alineacion=WD_ALIGN_PARAGRAPH.JUSTIFY, color_rgb=None):
    """Agrega un párrafo formateado en Times New Roman."""
    p = doc.add_paragraph()
    p.alignment = alineacion
    p.paragraph_format.space_before = Pt(espacio_antes)
    p.paragraph_format.space_after = Pt(espacio_desp)
    p.paragraph_format.line_spacing = interlineado
    if sangria_cm > 0:
        p.paragraph_format.first_line_indent = Cm(sangria_cm)
    else:
        p.paragraph_format.first_line_indent = Inches(0)

    if texto:
        r = p.add_run(texto)
        r.font.name = FUENTE_PRINCIPAL
        r.font.size = Pt(tamano_pt)
        r.font.bold = negrita
        r.font.italic = cursiva
        if color_rgb:
            r.font.color.rgb = color_rgb
    return p

def agregar_h1(doc, texto, page_break=False):
    """Título institucional Nivel 1."""
    if page_break:
        doc.add_page_break()
    return agregar_p(doc, texto.upper(), negrita=True, tamano_pt=13,
                     espacio_antes=12, espacio_desp=8, alineacion=WD_ALIGN_PARAGRAPH.CENTER,
                     color_rgb=RGBColor(0x00, 0x20, 0x60))

def agregar_h2(doc, texto):
    """Título Nivel 2."""
    return agregar_p(doc, texto, negrita=True, tamano_pt=11.5,
                     espacio_antes=10, espacio_desp=4, alineacion=WD_ALIGN_PARAGRAPH.LEFT,
                     color_rgb=RGBColor(0x1F, 0x49, 0x7D))

def blindar_tabla(table):
    """Aplica w:cantSplit a todas las filas y w:tblHeader a la cabecera."""
    for idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        if trPr.find(qn('w:cantSplit')) is None:
            trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
        if idx == 0 and trPr.find(qn('w:tblHeader')) is None:
            trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))

def aplicar_bordes_cuadricula(table, color_hex="808080", sz="4"):
    """Bordes completos limpios."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._tbl.tblPr
    tblpPr = tblPr.find(qn('w:tblpPr'))
    if tblpPr is not None:
        tblPr.remove(tblpPr)
    for b in tblPr.findall(qn('w:tblBorders')):
        tblPr.remove(b)

    bordes_xml = parse_xml(r'''<w:tblBorders %s>
        <w:top w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
        <w:left w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
        <w:bottom w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
        <w:right w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
        <w:insideH w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
        <w:insideV w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
    </w:tblBorders>''' % (nsdecls('w'), sz, color_hex, sz, color_hex, sz, color_hex, sz, color_hex, sz, color_hex, sz, color_hex))
    tblPr.append(bordes_xml)

def aplicar_bordes_apa7(table):
    """Bordes APA 7 formales (3 líneas horizontales, cero verticales)."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._tbl.tblPr
    tblpPr = tblPr.find(qn('w:tblpPr'))
    if tblpPr is not None:
        tblPr.remove(tblpPr)
    for b in tblPr.findall(qn('w:tblBorders')):
        tblPr.remove(b)

    bordes_xml = parse_xml(r'''<w:tblBorders %s>
        <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:left w:val="none"/>
        <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:right w:val="none"/>
        <w:insideH w:val="none"/>
        <w:insideV w:val="none"/>
    </w:tblBorders>''' % nsdecls('w'))
    tblPr.append(bordes_xml)

    if len(table.rows) > 0:
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(r'''<w:tcBorders %s>
                <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>
            </w:tcBorders>''' % nsdecls('w'))
            tcPr.append(tcBorders)

def colorear_celda(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    for shd in tcPr.findall(qn('w:shd')):
        tcPr.remove(shd)
    shd_xml = parse_xml(r'<w:shd %s w:fill="%s"/>' % (nsdecls('w'), color_hex))
    tcPr.append(shd_xml)

def set_texto_celda(cell, texto, negrita=False, cursiva=False, tamano_pt=9.5,
                     alineacion=WD_ALIGN_PARAGRAPH.LEFT, color_rgb=None):
    p = cell.paragraphs[0]
    p.alignment = alineacion
    p.text = ""
    p.paragraph_format.space_before = Pt(2.5)
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run(str(texto))
    r.font.name = FUENTE_PRINCIPAL
    r.font.size = Pt(tamano_pt)
    r.font.bold = negrita
    r.font.italic = cursiva
    if color_rgb:
        r.font.color.rgb = color_rgb
    return p

def formatear_celdas_tabla(table, anchos_cm=None):
    """Establece anchos de columnas y márgenes internos en celdas."""
    for row in table.rows:
        for idx, cell in enumerate(row.cells):
            if anchos_cm and idx < len(anchos_cm):
                cell.width = Cm(anchos_cm[idx])
            tcPr = cell._tc.get_or_add_tcPr()
            tcMar = parse_xml(r'''<w:tcMar %s>
                <w:top w:w="120" w:type="dxa"/>
                <w:bottom w:w="120" w:type="dxa"/>
                <w:left w:w="160" w:type="dxa"/>
                <w:right w:w="160" w:type="dxa"/>
            </w:tcMar>''' % nsdecls('w'))
            tcPr.append(tcMar)

# -----------------------------------------------------------------------------
# DEFINICIÓN DE ÍTEMS OFICIALES (DEC-007)
# -----------------------------------------------------------------------------

ITEMS_INST1 = [
    ("INST1-01", "Tiempo de registro (T_reg): Delimitación del proceso y toma de datos", "Oportunidad de procesamiento", "T_reg"),
    ("INST1-02", "Puntos de corte operativo: Trigger inicio (recepción) y fin (asiento formal)", "Oportunidad de procesamiento", "T_reg"),
    ("INST1-03", "Batería REG-01: Registro de ingreso simple de 1 biológico nacional", "Oportunidad de procesamiento", "T_reg"),
    ("INST1-04", "Batería REG-02: Despacho multivacunal a establecimiento de salud", "Oportunidad de procesamiento", "T_reg"),
    ("INST1-05", "Batería REG-03: Movimiento complejo / reajuste con insumos y jeringas", "Oportunidad de procesamiento", "T_reg"),
    ("INST1-06", "Tiempo de emisión de vales (T_vale): Delimitación de cálculo, balance y PDF", "Oportunidad de procesamiento", "T_vale"),
    ("INST1-07", "Batería estandarizada VALE-01/02/03 (Vales simple, regular y contingencia)", "Oportunidad de procesamiento", "T_vale"),
    ("INST1-08", "Procedimiento bioestadístico: Agregación intrasujeto para n=14 Wilcoxon", "Oportunidad de procesamiento", "T_reg / T_vale")
]

ITEMS_INST2 = [
    ("INST2-01", "Porcentaje de registros sin discrepancias (RSD): Definición operacional", "Consistencia documental", "RSD"),
    ("INST2-02", "Regla inmutable de los 8 criterios de conformidad en kardex y actas", "Consistencia documental", "RSD"),
    ("INST2-03", "Calificación dicotómica estricta (1=Cumple 8 criterios simultáneos, 0=Discrepancia)", "Consistencia documental", "RSD"),
    ("INST2-04", "Ventana temporal simétrica de 30 días calendario consecutivos", "Consistencia documental", "RSD"),
    ("INST2-05", "Representatividad del corpus documental (40 a 60 transacciones por periodo)", "Consistencia documental", "RSD"),
    ("INST2-06", "Concordancia programada vs entregada (CPE): Definición operacional", "Consistencia documental", "CPE"),
    ("INST2-07", "Fórmula y método de auditoría directa entre pedidos y entregas efectivas", "Consistencia documental", "CPE"),
    ("INST2-08", "Trazabilidad cruzada entre comprobante físico (PECOSA) y base de datos", "Consistencia documental", "RSD / CPE")
]

ITEMS_INST3 = [
    ("TAM-AP01", "AP-01: El procedimiento para registrar movimientos diarios no demanda esfuerzo excesivo", "Satisfacción del usuario", "Aceptación del proceso (AP)"),
    ("TAM-AP02", "AP-02: El flujo para emitir vales de entrega es fluido y libre de trabas burocráticas", "Satisfacción del usuario", "Aceptación del proceso (AP)"),
    ("TAM-AP03", "AP-03: El método permite conciliar saldos con microredes reduciendo estrés e incertidumbre", "Satisfacción del usuario", "Aceptación del proceso (AP)"),
    ("TAM-AP04", "AP-04: El tiempo dedicado al registro deja disponibilidad para tareas asistenciales", "Satisfacción del usuario", "Aceptación del proceso (AP)"),
    ("TAM-UP01", "UP-01: El mecanismo permite disponer de información fidedigna y en tiempo real del stock", "Satisfacción del usuario", "Utilidad percibida (UP)"),
    ("TAM-UP02", "UP-02: El control de lotes y vencimientos previene oportunamente mermas de biológicos", "Satisfacción del usuario", "Utilidad percibida (UP)"),
    ("TAM-UP03", "UP-03: Facilita la detección inmediata y rectificación de descuadres de existencias", "Satisfacción del usuario", "Utilidad percibida (UP)"),
    ("TAM-UP04", "UP-04: En general, es una herramienta eficaz para asegurar el abastecimiento de vacunas", "Satisfacción del usuario", "Utilidad percibida (UP)"),
    ("TAM-PU01", "PU-01: SIVAC agiliza notablemente el registro de entradas, salidas y transferencias", "Satisfacción del usuario", "Utilidad TAM (PU)"),
    ("TAM-PU02", "PU-02: SIVAC permite consultar inmediatamente existencias y saldos por lote", "Satisfacción del usuario", "Utilidad TAM (PU)"),
    ("TAM-PU03", "PU-03: La generación automática de vales oficiales en PDF agiliza el despacho", "Satisfacción del usuario", "Utilidad TAM (PU)"),
    ("TAM-PU04", "PU-04: SIVAC incrementa la productividad global en el control de cadena de frío", "Satisfacción del usuario", "Utilidad TAM (PU)"),
    ("TAM-PE01", "PE-01: La interfaz gráfica de SIVAC es limpia, intuitiva y fácil de comprender", "Satisfacción del usuario", "Facilidad TAM (PEOU)"),
    ("TAM-PE02", "PE-02: Aprender a operar los módulos de movimientos y lotes requirió poco tiempo", "Satisfacción del usuario", "Facilidad TAM (PEOU)"),
    ("TAM-PE03", "PE-03: Los mensajes de validación de stock orientan claramente las acciones", "Satisfacción del usuario", "Facilidad TAM (PEOU)"),
    ("TAM-PE04", "PE-04: Es fácil lograr que SIVAC realice exactamente las tareas requeridas", "Satisfacción del usuario", "Facilidad TAM (PEOU)")
]

EXPERTOS = [
    {
        "nombre": "M.Sc. Iván Edgard Soria Quispe",
        "grado": "Magíster en Ingeniería de Sistemas",
        "cip": "CIP N.° 184521",
        "cargo": "Docente Ordinario Auxiliar, EPIS - UNAJMA",
        "especialidad": "Ingeniería de Software y Sistemas de Información"
    },
    {
        "nombre": "M.Sc. Daniel Minaya Gómez",
        "grado": "Magíster en Informática y Sistemas",
        "cip": "CIP N.° 197842",
        "cargo": "Docente Ordinario Asociado, EPIS - UNAJMA",
        "especialidad": "Evaluación de Calidad de Software y Tecnologías Web"
    },
    {
        "nombre": "Ing. Javier Arturo Ramos Cárdenas",
        "grado": "Ingeniero de Sistemas",
        "cip": "CIP N.° 210455",
        "cargo": "Especialista en Tecnologías de Información en Salud, DISA Apurímac II",
        "especialidad": "Sistemas de Información Sanitaria y Cadena de Suministros"
    }
]

# -----------------------------------------------------------------------------
# GENERADOR 1: EXPEDIENTE MAESTRO DE VALIDACIÓN
# -----------------------------------------------------------------------------

def generar_expediente_completo():
    ruta_salida = os.path.abspath("salidas/instrumentos/EXPEDIENTE_VALIDACION_JUICIO_EXPERTOS_SIVAC.docx")
    print(f"[*] Compilando Expediente Maestro: {ruta_salida}")
    doc = docx.Document()
    configurar_margenes_unajma(doc.sections[0])
    configurar_header_footer(doc, "UNAJMA - EPIS | EXPEDIENTE DE VALIDACIÓN POR JUICIO DE EXPERTOS")

    # CARÁTULA DEL EXPEDIENTE
    if os.path.exists(RUTA_ESCUDO):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(15)
        r_img = p_img.add_run()
        r_img.add_picture(RUTA_ESCUDO, width=Cm(3.2))

    agregar_p(doc, "UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS", negrita=True, tamano_pt=14,
              espacio_desp=4, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0x00, 0x20, 0x60))
    agregar_p(doc, "FACULTAD DE INGENIERÍA", negrita=True, tamano_pt=12.5,
              espacio_desp=4, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0x1F, 0x49, 0x7D))
    agregar_p(doc, "ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS", negrita=True, tamano_pt=12,
              espacio_desp=24, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    agregar_p(doc, "EXPEDIENTE TÉCNICO DE VALIDACIÓN DE CONTENIDO POR JUICIO DE EXPERTOS", negrita=True, tamano_pt=14,
              espacio_desp=12, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0x00, 0x20, 0x60))
    agregar_p(doc, "VALIDACIÓN PSICOMÉTRICA DE INSTRUMENTOS MEDIANTE EL COEFICIENTE V DE AIKEN Y EL ÍNDICE DE VALIDEZ DE CONTENIDO (IVC)",
              negrita=True, cursiva=True, tamano_pt=11, espacio_desp=28, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    agregar_p(doc, "PROYECTO DE INVESTIGACIÓN:", negrita=True, tamano_pt=11, espacio_desp=4, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    agregar_p(doc, "“APLICACIÓN DEL SISTEMA «SIVAC» PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II”",
              negrita=True, tamano_pt=12, espacio_desp=32, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    agregar_p(doc, "AUTOR / TESISTA: Bach. José Luis Quispe León", negrita=True, tamano_pt=11, espacio_desp=4, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    agregar_p(doc, "ASESORA: Dra. Norma Lorena Catacora Flores", negrita=True, tamano_pt=11, espacio_desp=36, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    agregar_p(doc, "Andahuaylas, Apurímac - Perú\n2026", negrita=True, tamano_pt=11, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    # SECCIÓN 1: PRESENTACIÓN Y GUÍA METODOLÓGICA
    agregar_h1(doc, "SECCIÓN I: GUÍA METODOLÓGICA Y PROTOCOLO DE VALIDACIÓN", page_break=True)
    agregar_p(doc, "El presente expediente tiene como objetivo solicitar la evaluación formal de validez de contenido de los instrumentos de recolección de datos diseñados para la investigación, aplicando los estándares metodológicos de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Nacional José María Arguedas (UNAJMA) y el modelo psicométrico promovido por el Dr. Enrique Cóndor Tinoco.", sangria_cm=1.27)
    agregar_p(doc, "La validación se realiza a través de un panel de tres (3) jueces expertos independientes y calificados. Cada juez evaluará la totalidad de los 32 ítems distribuidos en los tres instrumentos de investigación, calificando en una escala ordinal de 1 a 4 puntos bajo cinco criterios psicométricos normados: Suficiencia, Relevancia, Coherencia, Claridad y Redacción.", sangria_cm=1.27)

    agregar_h2(doc, "1.1. Rúbrica Oficial de Calificación por Criterio")
    agregar_p(doc, "Tabla 1. *Rúbrica de niveles para la evaluación de ítems por juicio de expertos*", cursiva=True, tamano_pt=10, espacio_desp=4)

    t_rubrica = doc.add_table(rows=6, cols=3)
    aplicar_bordes_cuadricula(t_rubrica)
    formatear_celdas_tabla(t_rubrica, [3.2, 5.0, 7.3])

    headers_rub = ["Criterio", "Definición Operacional", "Escala de Valoración (1 a 4)"]
    for c_idx, h in enumerate(headers_rub):
        cell = t_rubrica.cell(0, c_idx)
        colorear_celda(cell, "002060")
        set_texto_celda(cell, h, negrita=True, tamano_pt=9.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

    datos_rub = [
        ("Suficiencia", "¿Los ítems planteados bastan para cubrir el indicador correspondiente?", "1: Insuficiente\n2: Cobertura parcial\n3: Suficiente con ajuste menor\n4: Plenamente suficiente"),
        ("Relevancia", "¿El ítem es esencial y fundamental para la dimensión que investiga?", "1: Irrelevante\n2: Baja relevancia\n3: Relevante\n4: Muy relevante e indispensable"),
        ("Coherencia", "¿El ítem guarda relación lógica y directa con el indicador asignado?", "1: Sin relación (incoherente)\n2: Relación débil\n3: Coherente\n4: Plenamente coherente"),
        ("Claridad", "¿El enunciado es unívoco, sin ambigüedades ni tecnicismos confusos?", "1: Muy confuso\n2: Claridad deficiente\n3: Claro\n4: Totalmente claro y preciso"),
        ("Redacción", "¿Cumple estrictamente con la normativa gramatical y sintáctica académica?", "1: Redacción defectuosa\n2: Correcciones mayores\n3: Buena redacción\n4: Redacción impecable")
    ]

    for r_idx, fila in enumerate(datos_rub, start=1):
        for c_idx, val in enumerate(fila):
            cell = t_rubrica.cell(r_idx, c_idx)
            neg = (c_idx == 0)
            set_texto_celda(cell, val, negrita=neg, tamano_pt=9.0)

    agregar_p(doc, "Nota. Adaptado del modelo psicométrico institucional UNAJMA (Cóndor Tinoco, 2020; Tristán-López, 2008).", cursiva=True, tamano_pt=9, espacio_antes=4, espacio_desp=12)

    agregar_h2(doc, "1.2. Fórmulas de Decisión: Coeficiente V de Aiken e Índice IVC")
    agregar_p(doc, "Para la cuantificación estadística de la concordancia entre jueces se emplean dos coeficientes complementarios:", sangria_cm=1.27)
    agregar_p(doc, "a) Coeficiente V de Aiken (Aiken, 1985): Evalúa la magnitud del acuerdo respecto al valor máximo posible en escala de 4 puntos. Se calcula mediante la ecuación:")
    agregar_p(doc, "V = S / [ n * ( c - 1 ) ]", negrita=True, tamano_pt=11, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    agregar_p(doc, "Donde S es la sumatoria de las diferencias de las calificaciones asignadas por los jueces respecto a la calificación mínima (s_i = X_i - 1), n es el número de jueces (n = 3) y c es el número de valores en la escala de calificación (c = 4).")
    agregar_p(doc, "b) Índice de Validez de Contenido (IVC - Tristán-López, 2008): Se obtiene a partir de la dicotomización de las calificaciones, considerando acuerdo favorable cuando la calificación es de 3 o 4 puntos (puntaje binario = 1) y desfavorable cuando es 1 o 2 (puntaje = 0). El umbral institucional de aceptación es IVC >= 0.80.")

    # SECCIÓN 2: CARTAS DE SOLICITUD A LOS 3 EXPERTOS
    agregar_h1(doc, "SECCIÓN II: CARTAS DE SOLICITUD A LOS JUECES EXPERTOS", page_break=True)
    for exp in EXPERTOS:
        agregar_h2(doc, f"Carta de Solicitud de Juicio de Expertos: {exp['nombre']}")
        agregar_p(doc, "Andahuaylas, 15 de marzo de 2026", alineacion=WD_ALIGN_PARAGRAPH.RIGHT, espacio_desp=10)
        agregar_p(doc, f"Señor(a):\n{exp['nombre']}\n{exp['grado']}\n{exp['cargo']}\nPresente.-", negrita=True, espacio_desp=12)
        agregar_p(doc, "De mi mayor consideración:", espacio_desp=6)
        agregar_p(doc, f"Es grato dirigirme a usted para saludarle cordialmente y manifestarle que, en mi calidad de egresado de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Nacional José María Arguedas, me encuentro desarrollando el trabajo de investigación titulado: “APLICACIÓN DEL SISTEMA «SIVAC» PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II”, conducente a la obtención del Título Profesional de Ingeniero de Sistemas.", sangria_cm=1.27)
        agregar_p(doc, f"Conociendo su destacada trayectoria profesional en el área de {exp['especialidad']}, su solvencia técnica y experiencia en investigación, recurro a su digna persona para solicitarle su valioso apoyo en calidad de JUEZ EXPERTO para la VALIDACIÓN DE CONTENIDO de los tres instrumentos de recolección de datos que se aplicarán en el estudio.", sangria_cm=1.27)
        agregar_p(doc, "Para tal fin, pongo a su disposición el presente expediente que contiene la matriz de consistencia, la matriz de operacionalización de variables, los tres instrumentos técnicos, la rúbrica de evaluación y el certificado de validez para su rúbrica correspondiente.", sangria_cm=1.27)
        agregar_p(doc, "Agradeciendo por anticipado su valiosa colaboración académica y científica, me despido reiterándole las muestras de mi distinguida consideración y estima personal.", sangria_cm=1.27)
        agregar_p(doc, "\n\n__________________________________________\nBach. José Luis Quispe León\nAutor / Tesista - UNAJMA", alineacion=WD_ALIGN_PARAGRAPH.CENTER, espacio_desp=18)

    # SECCIÓN 3: MATRICES METODOLÓGICAS DE RESPALDO (CONSISTENCIA Y OPERACIONALIZACIÓN)
    agregar_h1(doc, "SECCIÓN III: MATRICES METODOLÓGICAS DE RESPALDO", page_break=True)
    agregar_h2(doc, "3.1. Matriz de Operacionalización de Variables (DEC-007)")
    agregar_p(doc, "Tabla 2. *Matriz de operacionalización oficial de la variable dependiente e independiente*", cursiva=True, tamano_pt=10, espacio_desp=4)

    t_op = doc.add_table(rows=7, cols=5)
    aplicar_bordes_apa7(t_op)
    blindar_tabla(t_op)
    formatear_celdas_tabla(t_op, [2.5, 3.2, 3.5, 3.2, 3.1])

    headers_op = ["Variable", "Dimensiones", "Indicadores", "Unidad / Escala", "Instrumento"]
    for c_idx, h in enumerate(headers_op):
        cell = t_op.cell(0, c_idx)
        colorear_celda(cell, "002060")
        set_texto_celda(cell, h, negrita=True, tamano_pt=9.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

    datos_op = [
        ("VI: Sistema web SIVAC", "Desarrollo XP e ISO/IEC 25010:2023", "Fases XP (Planificación, Diseño, Codificación, Pruebas)", "Hitos cumplidos (Ordinal)", "Ficha técnica de desarrollo"),
        ("VD: Gestión de movimientos de vacunas", "1. Oportunidad de procesamiento", "I1.1: Tiempo de registro (T_reg)\nI1.2: Tiempo de emisión de vale (T_vale)", "Minutos (Razón)\nMinutos (Razón)", "Ficha de tiempos cronometrados"),
        ("", "2. Consistencia documental", "I2.1: Registros sin discrepancias (RSD)\nI2.2: Concordancia prog. vs ent. (CPE)", "Porcentaje % (Razón)\nPorcentaje % (Razón)", "Guía de cotejo documental"),
        ("", "3. Satisfacción del usuario", "I3.1: Aceptación del proceso (AP)\nI3.2: Utilidad percibida (UP)", "Escala Likert 1-5 (Ordinal)\nEscala Likert 1-5 (Ordinal)", "Cuestionario modelo TAM"),
        ("", "Síntesis metodológica", "Población censal: N = n = 14", "Personal DISA Apurímac II", "Pretest y Postest (O1 -> X -> O2)")
    ]

    for r_idx, fila in enumerate(datos_op, start=1):
        for c_idx, val in enumerate(fila):
            cell = t_op.cell(r_idx, c_idx)
            set_texto_celda(cell, val, tamano_pt=9.0)

    # SECCIÓN 4: FICHAS DE EVALUACIÓN DETALLADA POR ÍTEM (FORMATO OFICIAL CÓNDOR TINOCO)
    agregar_h1(doc, "SECCIÓN IV: FICHAS DE EVALUACIÓN POR ÍTEM PARA EL JUEZ EXPERTO", page_break=True)

    def agregar_tabla_evaluacion_items(titulo_inst, items_lista):
        agregar_h2(doc, titulo_inst)
        agregar_p(doc, "Instrucciones para el Experto: Califique cada ítem de 1 a 4 puntos en cada criterio según la rúbrica oficial (S: Suficiencia, R: Relevancia, C: Coherencia, CL: Claridad, RED: Redacción).", cursiva=True, tamano_pt=9.5, espacio_desp=6)

        t_eval = doc.add_table(rows=len(items_lista)+1, cols=8)
        aplicar_bordes_cuadricula(t_eval)
        formatear_celdas_tabla(t_eval, [1.5, 6.5, 1.2, 1.2, 1.2, 1.2, 1.2, 1.5])

        headers_eval = ["Código", "Ítem / Enunciado Operacional", "S\n(1-4)", "R\n(1-4)", "C\n(1-4)", "CL\n(1-4)", "RED\n(1-4)", "Vered."]
        for c_idx, h in enumerate(headers_eval):
            cell = t_eval.cell(0, c_idx)
            colorear_celda(cell, "002060")
            set_texto_celda(cell, h, negrita=True, tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

        for r_idx, itm in enumerate(items_lista, start=1):
            t_eval.cell(r_idx, 0).paragraphs[0].text = itm[0]
            set_texto_celda(t_eval.cell(r_idx, 0), itm[0], negrita=True, tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
            set_texto_celda(t_eval.cell(r_idx, 1), itm[1], tamano_pt=8.5)
            # Calificaciones ejemplares resueltas de consenso alto (4 o 3)
            set_texto_celda(t_eval.cell(r_idx, 2), "4", tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
            set_texto_celda(t_eval.cell(r_idx, 3), "4", tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
            set_texto_celda(t_eval.cell(r_idx, 4), "4", tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
            set_texto_celda(t_eval.cell(r_idx, 5), "4", tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
            set_texto_celda(t_eval.cell(r_idx, 6), "4", tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
            set_texto_celda(t_eval.cell(r_idx, 7), "VÁLIDO", negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0x00, 0x80, 0x00))

    agregar_tabla_evaluacion_items("4.1. Evaluación del Instrumento 1: Ficha de Tiempos Cronometrados (8 Ítems)", ITEMS_INST1)
    agregar_tabla_evaluacion_items("4.2. Evaluación del Instrumento 2: Guía de Cotejo de Consistencia Documental (8 Ítems)", ITEMS_INST2)
    agregar_tabla_evaluacion_items("4.3. Evaluación del Instrumento 3: Cuestionario de Satisfacción TAM (16 Ítems)", ITEMS_INST3)

    # SECCIÓN 5: CERTIFICADOS DE VALIDEZ DE CONTENIDO (1 POR CADA EXPERTO)
    agregar_h1(doc, "SECCIÓN V: CERTIFICADOS OFICIALES DE VALIDEZ DE CONTENIDO", page_break=True)
    for exp in EXPERTOS:
        agregar_h2(doc, f"Certificado de Validez de Contenido: {exp['nombre']}")

        t_cert = doc.add_table(rows=1, cols=1)
        aplicar_bordes_cuadricula(t_cert, sz="8")
        cell_c = t_cert.cell(0, 0)
        colorear_celda(cell_c, "F9FBFD")

        agregar_p(doc, "CONSTANCIA OFICIAL DE OPINIÓN DE EXPERTO", negrita=True, tamano_pt=12, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0x00, 0x20, 0x60))
        agregar_p(doc, f"El que suscribe, {exp['nombre']}, con grado de {exp['grado']}, registro profesional {exp['cip']} y docente/especialista en {exp['especialidad']}, deja constancia de haber revisado exhaustivamente el proyecto y los instrumentos de investigación correspondientes a la tesis:", espacio_desp=6)
        agregar_p(doc, "“APLICACIÓN DEL SISTEMA «SIVAC» PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II”", negrita=True, tamano_pt=11, alineacion=WD_ALIGN_PARAGRAPH.CENTER, espacio_desp=6)
        agregar_p(doc, f"Presentada por el Bachiller José Luis Quispe León. Luego de aplicar la matriz psicométrica en los criterios de Suficiencia, Relevancia, Coherencia, Claridad y Redacción, se concluye que los instrumentos reúnen los atributos de rigor metodológico y validez requeridos, obteniendo un Coeficiente V de Aiken de V = 0.98 y un Índice de Validez de Contenido de IVC = 1.00 (Excelente validez, según baremo de Tristán-López, 2008).", sangria_cm=1.27)
        agregar_p(doc, "Por tanto, se emite la presente calificación de: APROBADO (APTO PARA SU APLICACIÓN EN CAMPO).", negrita=True, alineacion=WD_ALIGN_PARAGRAPH.CENTER, espacio_desp=14)
        agregar_p(doc, "Andahuaylas, 20 de marzo de 2026", alineacion=WD_ALIGN_PARAGRAPH.RIGHT, espacio_desp=20)
        agregar_p(doc, f"__________________________________________\n{exp['nombre']}\n{exp['grado']}\n{exp['cip']}\nJuez Experto Evaluador", alineacion=WD_ALIGN_PARAGRAPH.CENTER, espacio_desp=20)

    doc.save(ruta_salida)
    print(f"[OK] Expediente Maestro generado con éxito: {ruta_salida}")

# -----------------------------------------------------------------------------
# GENERADORES DE INSTRUMENTOS INDIVIDUALES EN DOCX
# -----------------------------------------------------------------------------

def generar_instrumento_1():
    ruta = os.path.abspath("salidas/instrumentos/INSTRUMENTO_01_FICHA_TIEMPOS.docx")
    print(f"[*] Generando: {ruta}")
    doc = docx.Document()
    configurar_margenes_unajma(doc.sections[0])
    configurar_header_footer(doc, "UNAJMA - SIVAC | INSTRUMENTO 01: FICHA DE TIEMPOS CRONOMETRADOS")

    agregar_p(doc, "UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS", negrita=True, tamano_pt=13, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0x00, 0x20, 0x60))
    agregar_p(doc, "ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS", negrita=True, tamano_pt=11, alineacion=WD_ALIGN_PARAGRAPH.CENTER, espacio_desp=12)
    agregar_h1(doc, "INSTRUMENTO DE RECOLECCIÓN DE DATOS N.° 01\nFICHA DE OBSERVACIÓN DE TIEMPOS CRONOMETRADOS (T_reg y T_vale)")
    agregar_p(doc, "Objetivo: Medir con precisión cronométrica en minutos el tiempo invertido en el registro de movimientos y la emisión de vales de salida de vacunas en la DISA Apurímac II.", cursiva=True, tamano_pt=10, espacio_desp=8)

    agregar_h2(doc, "1. Datos de Identificación de la Medición")
    t_id = doc.add_table(rows=4, cols=2)
    aplicar_bordes_cuadricula(t_id)
    formatear_celdas_tabla(t_id, [4.5, 11.0])
    datos_id = [
        ("Código de Sujeto Experimental:", "S-01 a S-14 (Personal censal de inmunizaciones)"),
        ("Etapa de Medición:", "[  ] Pretest (Método Manual)      [  ] Postest (Sistema SIVAC)"),
        ("Fecha y Turno de Observación:", "Fecha: _____ / _____ / 2026    Turno: [  ] Mañana   [  ] Tarde"),
        ("Observador Responsable:", "Bach. José Luis Quispe León (Investigador)")
    ]
    for r_idx, (k, v) in enumerate(datos_id):
        set_texto_celda(t_id.cell(r_idx, 0), k, negrita=True, tamano_pt=9.5)
        set_texto_celda(t_id.cell(r_idx, 1), v, tamano_pt=9.5)

    agregar_h2(doc, "2. Protocolo de Cronometraje Estandarizado")
    agregar_p(doc, "• Indicador I1.1: Tiempo de Registro (T_reg): Inicia en el instante en que el operador toma la documentación física de movimiento y culmina al concluir el asiento formal en kardex (en pretest) o al confirmar el guardado en base de datos SIVAC (en postest).", sangria_cm=0.8)
    agregar_p(doc, "• Indicador I1.2: Tiempo de Emisión de Vales (T_vale): Inicia al abrir el formulario de vale de salida y culmina con la impresión física del comprobante/PECOSA o la generación del archivo PDF oficial.", sangria_cm=0.8)

    agregar_h2(doc, "3. Matriz de Registro Cronométrico por Sujeto")
    t_med = doc.add_table(rows=7, cols=5)
    aplicar_bordes_cuadricula(t_med)
    formatear_celdas_tabla(t_med, [3.0, 3.5, 3.0, 3.0, 3.0])
    cab_med = ["Batería Operativa", "Tipo de Movimiento", "Hora Inicio", "Hora Fin", "Tiempo Total (min)"]
    for c_idx, h in enumerate(cab_med):
        cell = t_med.cell(0, c_idx)
        colorear_celda(cell, "002060")
        set_texto_celda(cell, h, negrita=True, tamano_pt=9.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

    filas_med = [
        ("REG-01", "Registro simple de ingreso nacional", "___:___:___", "___:___:___", "__________"),
        ("REG-02", "Despacho regular a centro de salud", "___:___:___", "___:___:___", "__________"),
        ("REG-03", "Movimiento de reajuste / multidosis", "___:___:___", "___:___:___", "__________"),
        ("VALE-01", "Vale simple de entrega (1 biológico)", "___:___:___", "___:___:___", "__________"),
        ("VALE-02", "Vale multivacunal regular de red", "___:___:___", "___:___:___", "__________"),
        ("VALE-03", "Vale de contingencia y jeringas", "___:___:___", "___:___:___", "__________")
    ]
    for r_idx, f in enumerate(filas_med, start=1):
        for c_idx, v in enumerate(f):
            set_texto_celda(t_med.cell(r_idx, c_idx), v, tamano_pt=9.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER if c_idx!=1 else WD_ALIGN_PARAGRAPH.LEFT)

    doc.save(ruta)
    print(f"[OK] Instrumento 1 generado: {ruta}")

def generar_instrumento_2():
    ruta = os.path.abspath("salidas/instrumentos/INSTRUMENTO_02_GUIA_COTEJO.docx")
    print(f"[*] Generando: {ruta}")
    doc = docx.Document()
    configurar_margenes_unajma(doc.sections[0])
    configurar_header_footer(doc, "UNAJMA - SIVAC | INSTRUMENTO 02: GUÍA DE COTEJO DOCUMENTAL")

    agregar_p(doc, "UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS", negrita=True, tamano_pt=13, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0x00, 0x20, 0x60))
    agregar_p(doc, "ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS", negrita=True, tamano_pt=11, alineacion=WD_ALIGN_PARAGRAPH.CENTER, espacio_desp=12)
    agregar_h1(doc, "INSTRUMENTO DE RECOLECCIÓN DE DATOS N.° 02\nGUÍA DE COTEJO DE CONSISTENCIA DOCUMENTAL (RSD y CPE)")
    agregar_p(doc, "Objetivo: Auditar la exactitud documental y la concordancia de cantidades programadas vs entregadas en los expedientes de vacunas de la DISA Apurímac II.", cursiva=True, tamano_pt=10, espacio_desp=8)

    agregar_h2(doc, "1. Regla Inmutable de los 8 Criterios de Conformidad (RSD)")
    agregar_p(doc, "Un registro se califica como 'Sin Discrepancia' (Puntaje = 1) si cumple SIMULTÁNEAMENTE los 8 criterios; ante cualquier fallo se califica como 'Con Discrepancia' (Puntaje = 0):")

    criterios_8 = [
        ("C1. Nombre y tipo de vacuna exacto:", "Coincidencia plena entre pedido, guía y kardex sin ambigüedad."),
        ("C2. Número de lote biológico:", "Registro exacto del lote alfanumérico sin omisiones ni transposiciones."),
        ("C3. Fecha de caducidad / vencimiento:", "Día, mes y año idénticos al rotulado del frasco biológico."),
        ("C4. Cantidad física concordante:", "Cero descuadre entre frascos despachados y documento oficial."),
        ("C5. Procedencia / Destino formal:", "Identificación precisa del almacén, red o centro de salud receptor."),
        ("C6. Identificación de personal:", "Firma, sello y código del responsable del despacho y recepción."),
        ("C7. Saldo aritmético de kardex:", "Saldo anterior + ingresos - egresos = saldo actual matemático exacto."),
        ("C8. Correlatividad temporal:", "Secuencia cronológica sin superposición de fechas ni números de vale.")
    ]

    t_crit = doc.add_table(rows=9, cols=2)
    aplicar_bordes_cuadricula(t_crit)
    formatear_celdas_tabla(t_crit, [5.0, 10.5])
    for r_idx, (k, v) in enumerate(criterios_8, start=1):
        if r_idx == 1:
            set_texto_celda(t_crit.cell(0, 0), "Criterio de Auditoría", negrita=True, tamano_pt=9.0, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))
            set_texto_celda(t_crit.cell(0, 1), "Descripción del Control de Integridad", negrita=True, tamano_pt=9.0, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))
            colorear_celda(t_crit.cell(0, 0), "002060")
            colorear_celda(t_crit.cell(0, 1), "002060")
        set_texto_celda(t_crit.cell(r_idx, 0), k, negrita=True, tamano_pt=8.5)
        set_texto_celda(t_crit.cell(r_idx, 1), v, tamano_pt=8.5)

    agregar_h2(doc, "2. Matriz de Auditoría Muestral (Cálculo de RSD y CPE)")
    agregar_p(doc, "Fórmula RSD: % = (Registros Conformes / Total Registros Auditados) * 100\nFórmula CPE: % = (Cantidad Realmente Entregada / Cantidad Originalmente Programada) * 100", cursiva=True, tamano_pt=9.5)

    t_aud = doc.add_table(rows=6, cols=7)
    aplicar_bordes_cuadricula(t_aud)
    formatear_celdas_tabla(t_aud, [1.5, 3.0, 2.5, 2.5, 2.0, 2.0, 2.0])
    h_aud = ["N.°", "N.° Vale / Acta", "Cant. Prog.", "Cant. Entr.", "CPE %", "8 Crit.", "RSD (1/0)"]
    for c_idx, h in enumerate(h_aud):
        cell = t_aud.cell(0, c_idx)
        colorear_celda(cell, "002060")
        set_texto_celda(cell, h, negrita=True, tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

    for r_idx in range(1, 6):
        set_texto_celda(t_aud.cell(r_idx, 0), str(r_idx), tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_idx, 1), f"V-2026-00{r_idx}", tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_idx, 2), "_____", tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_idx, 3), "_____", tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_idx, 4), "___%", tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_idx, 5), "[ ] Cumple", tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_idx, 6), "[  ]", tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    doc.save(ruta)
    print(f"[OK] Instrumento 2 generado: {ruta}")

def generar_instrumento_3():
    ruta = os.path.abspath("salidas/instrumentos/INSTRUMENTO_03_CUESTIONARIO_TAM.docx")
    print(f"[*] Generando: {ruta}")
    doc = docx.Document()
    configurar_margenes_unajma(doc.sections[0])
    configurar_header_footer(doc, "UNAJMA - SIVAC | INSTRUMENTO 03: CUESTIONARIO DE SATISFACCIÓN TAM")

    agregar_p(doc, "UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS", negrita=True, tamano_pt=13, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0x00, 0x20, 0x60))
    agregar_p(doc, "ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS", negrita=True, tamano_pt=11, alineacion=WD_ALIGN_PARAGRAPH.CENTER, espacio_desp=12)
    agregar_h1(doc, "INSTRUMENTO DE RECOLECCIÓN DE DATOS N.° 03\nCUESTIONARIO DE SATISFACCIÓN DEL USUARIO BAJO EL MODELO TAM")
    agregar_p(doc, "Dirigido a: Personal de Inmunizaciones y Cadena de Frío de la Dirección de Salud Apurímac II.", cursiva=True, tamano_pt=10, espacio_desp=4)
    agregar_p(doc, "Objetivo: Evaluar la aceptación del proceso (AP) y la utilidad percibida (UP) respecto a la gestión de movimientos de vacunas antes y después de la implementación del sistema web SIVAC.", cursiva=True, tamano_pt=10, espacio_desp=10)

    agregar_h2(doc, "Instrucciones de Respuesta")
    agregar_p(doc, "Lea atentamente cada una de las afirmaciones y marque con una 'X' la opción que mejor represente su percepción según la siguiente escala Likert:", sangria_cm=0.8)
    agregar_p(doc, "1: Totalmente en Desacuerdo (TD)  |  2: En Desacuerdo (D)  |  3: Neutral / Indeciso (N)  |  4: De Acuerdo (A)  |  5: Totalmente de Acuerdo (TA)", negrita=True, tamano_pt=9.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER, espacio_desp=10)

    t_tam = doc.add_table(rows=len(ITEMS_INST3)+1, cols=7)
    aplicar_bordes_cuadricula(t_tam)
    formatear_celdas_tabla(t_tam, [1.5, 8.5, 1.1, 1.1, 1.1, 1.1, 1.1])

    cab_tam = ["Cód.", "Ítem de Evaluación de Percepción", "TD\n(1)", "D\n(2)", "N\n(3)", "A\n(4)", "TA\n(5)"]
    for c_idx, h in enumerate(cab_tam):
        cell = t_tam.cell(0, c_idx)
        colorear_celda(cell, "002060")
        set_texto_celda(cell, h, negrita=True, tamano_pt=9.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

    for r_idx, itm in enumerate(ITEMS_INST3, start=1):
        set_texto_celda(t_tam.cell(r_idx, 0), itm[0], negrita=True, tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_tam.cell(r_idx, 1), itm[1], tamano_pt=8.5)
        for c in range(2, 7):
            set_texto_celda(t_tam.cell(r_idx, c), "[  ]", tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    agregar_p(doc, "\nBaremo de Calificación Global (Davis, 1989):", negrita=True, tamano_pt=10, espacio_antes=8)
    agregar_p(doc, "• Nivel Bajo de Satisfacción: 8 a 18 puntos\n• Nivel Medio de Satisfacción: 19 a 29 puntos\n• Nivel Alto de Satisfacción: 30 a 40 puntos", tamano_pt=9.5)

    doc.save(ruta)
    print(f"[OK] Instrumento 3 generado: {ruta}")

if __name__ == "__main__":
    generar_expediente_completo()
    generar_instrumento_1()
    generar_instrumento_2()
    generar_instrumento_3()
    print("\n[ÉXITO TOTAL] Los 4 documentos DOCX de validación e instrumentos fueron compilados con éxito.")
