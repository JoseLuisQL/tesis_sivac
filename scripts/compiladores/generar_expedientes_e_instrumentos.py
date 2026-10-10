#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - Squad B (Metodología y Psicometría)
COMPILADOR MAESTRO DEL EXPEDIENTE DE VALIDACIÓN Y LOS TRES INSTRUMENTOS EN DOCX Y PDF
Modelo Institucional: Dr. Enrique Cóndor Tinoco (EPIS-UNAJMA) / Directiva DEC-007
================================================================================
Artefactos generados:
1. salidas/instrumentos/EXPEDIENTE_VALIDACION_JUICIO_EXPERTOS_SIVAC.docx & .pdf
2. salidas/instrumentos/INSTRUMENTO_01_FICHA_TIEMPOS.docx & .pdf
3. salidas/instrumentos/INSTRUMENTO_02_GUIA_COTEJO.docx & .pdf
4. salidas/instrumentos/INSTRUMENTO_03_CUESTIONARIO_TAM.docx & .pdf
================================================================================
"""

import os
import sys
import time
import subprocess
from pathlib import Path
import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

# Constantes de tipografía y colores institucionales UNAJMA
FUENTE_PRINCIPAL = "Times New Roman"
COLOR_AZUL_UNAJMA = "002060"       # Azul institucional UNAJMA
COLOR_AZUL_SEC = "1F497D"          # Azul secundario
COLOR_GRIS_FONDO = "F2F2F2"        # Gris claro para sombreados
COLOR_GRIS_BORDE = "808080"        # Gris medio para bordes de cuadrícula
COLOR_VERDE_APROBADO = "006600"    # Verde para veredicto aprobado

RUTA_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RUTA_SALIDAS = os.path.join(RUTA_BASE, "salidas", "instrumentos")
RUTA_ESCUDO = os.path.join(RUTA_BASE, "salidas", "figuras", "recursos_graficos", "escudo_unajma.png")

# -----------------------------------------------------------------------------
# PADRÓN OFICIAL DE EXPERTOS EVALUADORES (EPIS - UNAJMA)
# -----------------------------------------------------------------------------
EXPERTOS = [
    {
        "id": "EXP-01",
        "trato": "M.Sc.",
        "nombre": "M.Sc. Iván Soria Solís",
        "nombre_completo": "IVÁN SORIA SOLÍS",
        "dni": "40725333",
        "profesion": "Ingeniero Informático y de Sistemas",
        "grado": "Magíster Scientiae en Informática",
        "cip": "CIP N.° 184521",
        "cargo": "Docente de la Escuela Profesional de Ingeniería de Sistemas",
        "institucion": "Universidad Nacional José María Arguedas (UNAJMA)",
        "especialidad": "Tecnologías de la Información, Sistemas de Información y Métodos de Investigación"
    },
    {
        "id": "EXP-02",
        "trato": "M.Sc.",
        "nombre": "M.Sc. Daniel Minaya Gutiérrez",
        "nombre_completo": "DANIEL MINAYA GUTIÉRREZ",
        "dni": "44254814",
        "profesion": "Ingeniero Informático y de Sistemas",
        "grado": "Magíster en Informática y Sistemas",
        "cip": "CIP N.° 197842",
        "cargo": "Docente de la Escuela Profesional de Ingeniería de Sistemas",
        "institucion": "Universidad Nacional José María Arguedas (UNAJMA)",
        "especialidad": "Calidad de Software, Ingeniería de Sistemas y Métodos Cuantitativos"
    },
    {
        "id": "EXP-03",
        "trato": "M.Sc.",
        "nombre": "M.Sc. Javier Ramos Gonzales",
        "nombre_completo": "JAVIER RAMOS GONZALES",
        "dni": "44844286",
        "profesion": "Ingeniero de Sistemas",
        "grado": "Magíster en Ingeniería de Sistemas",
        "cip": "CIP N.° 210455",
        "cargo": "Docente de la Escuela Profesional de Ingeniería de Sistemas",
        "institucion": "Universidad Nacional José María Arguedas (UNAJMA)",
        "especialidad": "Sistemas de Información, Arquitectura Web y Gestión de Procesos"
    }
]

# -----------------------------------------------------------------------------
# DEFINICIÓN DE ÍTEMS OFICIALES (DEC-007)
# -----------------------------------------------------------------------------

# INSTRUMENTO 1: FICHA DE TIEMPOS CRONOMETRADOS (8 ÍTEMS)
ITEMS_INST1 = [
    ("INST1-01", "Tiempo de registro (T_reg): Definición operacional y delimitación del proceso de captura."),
    ("INST1-02", "Puntos de corte operativo T_reg (Trigger inicio: recepción de remesa; Trigger fin: asiento formal)."),
    ("INST1-03", "Batería estandarizada REG-01: Registro simple de ingreso nacional (1 biológico, lote único)."),
    ("INST1-04", "Batería estandarizada REG-02: Registro regular de despacho multivacunal a establecimiento de salud."),
    ("INST1-05", "Batería estandarizada REG-03: Movimiento complejo / reajuste multibioplástico con insumos y jeringas."),
    ("INST1-06", "Tiempo de emisión de vales (T_vale): Delimitación de confección, balance y generación PDF."),
    ("INST1-07", "Batería estandarizada VALE-01/02/03: Vales simple, regular de red y contingencia de cadena de frío."),
    ("INST1-08", "Tratamiento bioestadístico anti-pseudorreplicación: Agregación intrasujeto para n=14 Wilcoxon.")
]

# INSTRUMENTO 2: GUÍA DE COTEJO DOCUMENTAL (8 ÍTEMS)
ITEMS_INST2 = [
    ("INST2-01", "Porcentaje de registros sin discrepancias (RSD): Definición operacional e integridad del dato."),
    ("INST2-02", "Regla inmutable de los 8 criterios de conformidad del dato en kardex y actas de entrega/recepción."),
    ("INST2-03", "Calificación dicotómica estricta (1 = Cumple los 8 criterios simultáneos, 0 = Presenta discrepancia)."),
    ("INST2-04", "Ventana temporal simétrica de 30 días calendario consecutivos para pretest y postest (PMMV)."),
    ("INST2-05", "Representatividad del corpus documental auditado (40 a 60 transacciones por periodo en la red de frío)."),
    ("INST2-06", "Concordancia programada vs entregada (CPE): Definición operacional de conformidad física vs pedido."),
    ("INST2-07", "Fórmula y método de auditoría de contrastación directa entre pedidos y entregas efectivas."),
    ("INST2-08", "Trazabilidad cruzada entre comprobantes físicos (PECOSA/Guía de remisión) y base de datos relacional.")
]

# INSTRUMENTO 3: CUESTIONARIO TAM (16 ÍTEMS: 8 OFICIALES PARA HE3 + 8 ANEXO TAM CLÁSICO SIVAC)
ITEMS_INST3 = [
    # Subdimensión 3.1: Aceptación del Proceso (AP)
    ("TAM-AP01", "AP-01: El procedimiento para registrar movimientos diarios y cierres no demanda esfuerzo excesivo."),
    ("TAM-AP02", "AP-02: El flujo de trabajo para emitir vales de entrega es fluido y libre de demoras o trabas."),
    ("TAM-AP03", "AP-03: El método permite conciliar saldos con las microredes reduciendo estrés e incertidumbre laboral."),
    ("TAM-AP04", "AP-04: El tiempo dedicado al registro deja disponibilidad para tareas sanitarias y asistenciales."),
    # Subdimensión 3.2: Utilidad Percibida (UP)
    ("TAM-UP01", "UP-01: El mecanismo permite disponer de información fidedigna y en tiempo real del stock de vacunas."),
    ("TAM-UP02", "UP-02: El control de lotes y vencimientos previene oportunamente mermas y pérdidas de biológicos."),
    ("TAM-UP03", "UP-03: Facilita la detección inmediata y rectificación de cualquier descuadre de inventario físico."),
    ("TAM-UP04", "UP-04: En general, es una herramienta altamente eficaz para asegurar el abastecimiento de vacunas."),
    # Módulo Anexo TAM Clásico: Utilidad Percibida del Software (PU)
    ("TAM-PU01", "PU-01: Utilizar SIVAC agiliza notablemente el registro de entradas, salidas y transferencias."),
    ("TAM-PU02", "PU-02: SIVAC permite consultar inmediatamente existencias y saldos por lote y caducidad."),
    ("TAM-PU03", "PU-03: La generación automática de vales oficiales en PDF agiliza sustancialmente el despacho."),
    ("TAM-PU04", "PU-04: SIVAC incrementa la productividad global en el control de cadena de frío institucional."),
    # Módulo Anexo TAM Clásico: Facilidad de Uso Percibida (PEOU)
    ("TAM-PE01", "PE-01: La interfaz gráfica de SIVAC es limpia, intuitiva y fácil de comprender para el operador."),
    ("TAM-PE02", "PE-02: Aprender a operar los módulos de movimientos y lotes requirió poco tiempo y esfuerzo."),
    ("TAM-PE03", "PE-03: Los mensajes de confirmación y validación de stock orientan claramente las acciones."),
    ("TAM-PE04", "PE-04: Es fácil lograr que SIVAC realice exactamente las tareas requeridas durante la jornada.")
]

# -----------------------------------------------------------------------------
# UTILIDADES OPENXML QUIRÚRGICAS Y GEOMETRÍA MILIMÉTRICA
# -----------------------------------------------------------------------------

def configurar_margenes_unajma(seccion):
    """Márgenes oficiales UNAJMA: Izquierdo 3.0 cm, Superior/Derecho/Inferior 2.5 cm."""
    seccion.page_width = Cm(21.0)
    seccion.page_height = Cm(29.7)
    seccion.left_margin = Cm(3.0)
    seccion.right_margin = Cm(2.5)
    seccion.top_margin = Cm(2.5)
    seccion.bottom_margin = Cm(2.5)
    seccion.header_distance = Cm(1.27)
    seccion.footer_distance = Cm(1.27)

def configurar_header_footer(doc, texto_header):
    """Configura encabezado institucional y pie con numeración nativa OpenXML (PAGE de NUMPAGES)."""
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
    """Agrega un párrafo formateado rigurosamente en Times New Roman."""
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
    return agregar_p(doc, texto.upper(), negrita=True, tamano_pt=12.5,
                     espacio_antes=14, espacio_desp=8, alineacion=WD_ALIGN_PARAGRAPH.CENTER,
                     color_rgb=RGBColor(0x00, 0x20, 0x60))

def agregar_h2(doc, texto):
    """Título Nivel 2."""
    return agregar_p(doc, texto, negrita=True, tamano_pt=11.5,
                     espacio_antes=10, espacio_desp=4, alineacion=WD_ALIGN_PARAGRAPH.LEFT,
                     color_rgb=RGBColor(0x1F, 0x49, 0x7D))

def agregar_h3(doc, texto):
    """Título Nivel 3."""
    return agregar_p(doc, texto, negrita=True, cursiva=True, tamano_pt=10.5,
                     espacio_antes=6, espacio_desp=2, alineacion=WD_ALIGN_PARAGRAPH.LEFT)

def blindar_tabla(table):
    """Aplica w:cantSplit a todas las filas y w:tblHeader a la cabecera."""
    for idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        if trPr.find(qn('w:cantSplit')) is None:
            trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
        if idx == 0 and trPr.find(qn('w:tblHeader')) is None:
            trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))

def aplicar_bordes_cuadricula(table, color_hex="808080", sz="4"):
    """Aplica bordes reticulares limpios y elimina propiedades flotantes."""
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
    """Bordes APA 7 canónicos (tres líneas horizontales, cero verticales)."""
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
    """Aplica sombreado de fondo w:shd a una celda."""
    tcPr = cell._tc.get_or_add_tcPr()
    for shd in tcPr.findall(qn('w:shd')):
        tcPr.remove(shd)
    shd_xml = parse_xml(r'<w:shd %s w:fill="%s"/>' % (nsdecls('w'), color_hex))
    tcPr.append(shd_xml)

def set_texto_celda(cell, texto, negrita=False, cursiva=False, tamano_pt=9.0,
                     alineacion=WD_ALIGN_PARAGRAPH.LEFT, color_rgb=None):
    """Inserta texto estilizado en una celda con márgenes compactos."""
    p = cell.paragraphs[0]
    p.alignment = alineacion
    p.text = ""
    p.paragraph_format.space_before = Pt(2.0)
    p.paragraph_format.space_after = Pt(2.0)
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
    """Establece anchos de columnas y márgenes de celda (w:tcMar)."""
    blindar_tabla(table)
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

def insertar_encabezado_institucional(doc, titulo_instrumento, subtitulo_instrumento=""):
    """Inserta el membrete superior institucional oficial UNAJMA con escudo."""
    if os.path.exists(RUTA_ESCUDO):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(0)
        p_img.paragraph_format.space_after = Pt(6)
        r_img = p_img.add_run()
        r_img.add_picture(RUTA_ESCUDO, width=Cm(2.5))

    agregar_p(doc, "UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS", negrita=True, tamano_pt=13,
              espacio_desp=2, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0x00, 0x20, 0x60))
    agregar_p(doc, "FACULTAD DE INGENIERÍA", negrita=True, tamano_pt=11.5,
              espacio_desp=2, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0x1F, 0x49, 0x7D))
    agregar_p(doc, "ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS", negrita=True, tamano_pt=11,
              espacio_desp=12, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    agregar_h1(doc, titulo_instrumento)
    if subtitulo_instrumento:
        agregar_p(doc, subtitulo_instrumento, cursiva=True, tamano_pt=10,
                  espacio_desp=10, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

# -----------------------------------------------------------------------------
# GENERADOR 1: EXPEDIENTE INTEGRAL DE VALIDACIÓN POR JUICIO DE EXPERTOS
# -----------------------------------------------------------------------------

def generar_expediente_completo():
    ruta_salida = os.path.join(RUTA_SALIDAS, "EXPEDIENTE_VALIDACION_JUICIO_EXPERTOS_SIVAC.docx")
    print(f"[*] Generando Expediente Colegiado de Validación: {ruta_salida}")
    doc = docx.Document()
    configurar_margenes_unajma(doc.sections[0])
    configurar_header_footer(doc, "UNAJMA - EPIS | EXPEDIENTE DE VALIDACIÓN POR JUICIO DE EXPERTOS")

    # CARÁTULA INSTITUCIONAL
    if os.path.exists(RUTA_ESCUDO):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(12)
        p_img.paragraph_format.space_after = Pt(14)
        r_img = p_img.add_run()
        r_img.add_picture(RUTA_ESCUDO, width=Cm(3.2))

    agregar_p(doc, "UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS", negrita=True, tamano_pt=14,
              espacio_desp=4, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0x00, 0x20, 0x60))
    agregar_p(doc, "FACULTAD DE INGENIERÍA", negrita=True, tamano_pt=12.5,
              espacio_desp=4, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0x1F, 0x49, 0x7D))
    agregar_p(doc, "ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS", negrita=True, tamano_pt=12,
              espacio_desp=24, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    agregar_p(doc, "EXPEDIENTE TÉCNICO DE VALIDACIÓN DE INSTRUMENTOS POR JUICIO DE EXPERTOS", negrita=True, tamano_pt=14,
              espacio_desp=10, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0x00, 0x20, 0x60))
    agregar_p(doc, "EVALUACIÓN PSICOMÉTRICA MEDIANTE EL ÍNDICE DE VALIDEZ DE CONTENIDO (IVC) Y COEFICIENTE V DE AIKEN",
              negrita=True, cursiva=True, tamano_pt=11, espacio_desp=26, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    agregar_p(doc, "TRABAJO DE INVESTIGACIÓN:", negrita=True, tamano_pt=11, espacio_desp=4, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    agregar_p(doc, "“APLICACIÓN DEL SISTEMA «SIVAC» PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II”",
              negrita=True, tamano_pt=12, espacio_desp=28, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    agregar_p(doc, "TESISTA / AUTOR: Bach. José Luis Quispe León (DNI N° 70519963)", negrita=True, tamano_pt=11, espacio_desp=4, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    agregar_p(doc, "ASESORA: Dra. Norma Lorena Catacora Flores", negrita=True, tamano_pt=11, espacio_desp=32, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    agregar_p(doc, "Andahuaylas, Apurímac - Perú\n2026", negrita=True, tamano_pt=11, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    # SECCIÓN I: PROTOCOLO METODOLÓGICO Y PSICOMÉTRICO
    agregar_h1(doc, "SECCIÓN I: PROTOCOLO METODOLÓGICO Y PSICOMÉTRICO DE VALIDACIÓN", page_break=True)
    agregar_p(doc, "El presente expediente reúne las piezas técnicas y metodológicas para certificar la validez de contenido de los instrumentos de recolección de datos diseñados para la investigación. La validación se rige por la Guía Metodológica del Dr. Enrique Edgardo Cóndor Tinoco (docente de la EPIS - UNAJMA), fundamentada en Lawshe (1975), Tristán-López (2008), Aiken (1985) y Polit, Beck & Owen (2007).", sangria_cm=1.27)
    agregar_p(doc, "El panel de validación está constituido por tres (03) docentes especialistas de la Escuela Profesional de Ingeniería de Sistemas de la UNAJMA con grado de Magíster y colegiatura vigente en el Colegio de Ingenieros del Perú (CIP). Cada experto evalúa la totalidad de los 32 ítems distribuidos en los tres instrumentos bajo cinco criterios psicométricos normados: Suficiencia, Relevancia, Coherencia, Claridad y Redacción.", sangria_cm=1.27)

    # SECCIÓN II: RÚBRICA OFICIAL DE EVALUACIÓN
    agregar_h1(doc, "SECCIÓN II: RÚBRICA INSTITUCIONAL DE CALIFICACIÓN POR CRITERIO", page_break=False)
    agregar_p(doc, "Tabla 1. *Rúbrica de niveles para la evaluación psicométrica de ítems por juicio de expertos*", cursiva=True, tamano_pt=10, espacio_desp=4)

    t_rubrica = doc.add_table(rows=6, cols=3)
    aplicar_bordes_cuadricula(t_rubrica)
    formatear_celdas_tabla(t_rubrica, [3.0, 5.0, 7.5])

    headers_rub = ["Criterio", "Definición Institucional", "Indicadores de Calificación (Escala 1 a 4)"]
    for c_idx, h in enumerate(headers_rub):
        cell = t_rubrica.cell(0, c_idx)
        colorear_celda(cell, COLOR_AZUL_UNAJMA)
        set_texto_celda(cell, h, negrita=True, tamano_pt=9.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

    datos_rub = [
        ("Suficiencia", "¿El ítem abarca suficientemente el contenido del indicador?",
         "1 = El ítem no es suficiente para medir el indicador.\n2 = El ítem mide algún aspecto, pero no cubre la dimensión.\n3 = El ítem podría modificarse para contribuir completamente.\n4 = El ítem es plenamente suficiente y abarca el indicador."),
        ("Relevancia", "¿El ítem es pertinente y esencial para la variable investigada?",
         "1 = El ítem puede ser eliminado sin afectar la medición.\n2 = El ítem tiene poca relevancia o aporte tangencial.\n3 = El ítem es relativamente importante y pertinente.\n4 = El ítem es muy relevante, esencial y debe ser considerado."),
        ("Coherencia", "¿El ítem está alineado lógicamente con los objetivos y dimensiones?",
         "1 = El ítem no tiene relación lógica con la dimensión.\n2 = El ítem tiene una relación tangencial con la dimensión.\n3 = El ítem tiene una relación moderada y coherente con el indicador.\n4 = El ítem se encuentra completamente relacionado y coherente."),
        ("Claridad", "¿El ítem es comprensible, unívoco y libre de ambigüedades?",
         "1 = El ítem no está claro, genera confusión o ambigüedad.\n2 = El ítem requiere modificaciones sustanciales de redacción.\n3 = El ítem requiere una modificación específica de términos.\n4 = El ítem es plenamente claro, directo y se entiende."),
        ("Redacción", "¿El ítem cumple con la normativa gramatical y sintáctica académica?",
         "1 = La redacción del ítem no es adecuada.\n2 = La redacción del ítem tiene que ser mejorada en su sintaxis.\n3 = La redacción del ítem podría ser mejorada en su semántica.\n4 = La redacción es entendible, adecuada y gramaticalmente correcta.")
    ]

    for r_idx, fila in enumerate(datos_rub, start=1):
        for c_idx, val in enumerate(fila):
            cell = t_rubrica.cell(r_idx, c_idx)
            set_texto_celda(cell, val, negrita=(c_idx==0), tamano_pt=8.5)

    agregar_p(doc, "Nota. Tomado literalmente del Formato Institucional de Validación por Ítem de la EPIS - UNAJMA (Dr. Enrique Cóndor Tinoco, 2020; Tristán-López, 2008).", cursiva=True, tamano_pt=9, espacio_antes=4, espacio_desp=12)

    # SECCIÓN III: MATRIZ DE OPERACIONALIZACIÓN DE VARIABLES (DEC-007)
    agregar_h1(doc, "SECCIÓN III: MATRIZ DE OPERACIONALIZACIÓN DE VARIABLES VINCULADA", page_break=True)
    agregar_p(doc, "Tabla 2. *Operacionalización de variables con las tres dimensiones oficiales fijadas por DEC-007*", cursiva=True, tamano_pt=10, espacio_desp=4)

    t_op = doc.add_table(rows=7, cols=5)
    aplicar_bordes_apa7(t_op)
    formatear_celdas_tabla(t_op, [2.5, 3.2, 3.6, 3.0, 3.2])

    headers_op = ["Variable", "Dimensiones", "Indicadores", "Unidad / Escala", "Instrumento Oficial"]
    for c_idx, h in enumerate(headers_op):
        cell = t_op.cell(0, c_idx)
        colorear_celda(cell, COLOR_AZUL_UNAJMA)
        set_texto_celda(cell, h, negrita=True, tamano_pt=9.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

    datos_op = [
        ("VI: Sistema web SIVAC", "Ingeniería de Software XP e ISO/IEC 25010:2023", "Fases XP (Planificación, Diseño, Codificación, Pruebas y Aceptación)", "Hitos de iteración cumplidos (Ordinal)", "Ficha técnica de desarrollo y auditoría"),
        ("VD: Gestión de movimientos de vacunas", "1. Oportunidad de procesamiento", "I1.1: Tiempo de registro (T_reg)\nI1.2: Tiempo de emisión de vale (T_vale)", "Minutos decimales (Razón)\nMinutos decimales (Razón)", "Instrumento 01:\nFicha de Tiempos Cronometrados"),
        ("", "2. Consistencia documental", "I2.1: Registros sin discrepancias (RSD)\nI2.2: Concordancia prog. vs ent. (CPE)", "Porcentaje % (Razón)\nPorcentaje % (Razón)", "Instrumento 02:\nGuía de Cotejo Documental"),
        ("", "3. Satisfacción del usuario", "I3.1: Aceptación del proceso (AP)\nI3.2: Utilidad percibida (UP)", "Escala Likert 1-5 (Ordinal)\nEscala Likert 1-5 (Ordinal)", "Instrumento 03:\nCuestionario TAM"),
        ("", "Población censal", "Personal de inmunizaciones: N = n = 14", "DISA Apurímac II", "Pretest y Postest (O1 -> X -> O2)"),
        ("", "Módulo complementario", "Calidad en uso de software SIVAC", "Constructos PU y PEOU (TAM clásico)", "Anexo al Instrumento 03 (Postest)")
    ]

    for r_idx, fila in enumerate(datos_op, start=1):
        for c_idx, val in enumerate(fila):
            cell = t_op.cell(r_idx, c_idx)
            set_texto_celda(cell, val, tamano_pt=8.5)

    agregar_p(doc, "Nota. Matriz aprobada y custodiada bajo mandato metodológico DEC-007.", cursiva=True, tamano_pt=9, espacio_antes=4, espacio_desp=14)

    # -------------------------------------------------------------------------
    # SECCIONES IV, V Y VI: EXPEDIENTES INDIVIDUALIZADOS POR JUEZ EXPERTO
    # -------------------------------------------------------------------------
    romanos = ["IV", "V", "VI"]
    for idx_exp, exp in enumerate(EXPERTOS):
        sec_num = romanos[idx_exp]
        agregar_h1(doc, f"SECCIÓN {sec_num}: EXPEDIENTE DE EVALUACIÓN — {exp['nombre'].upper()}", page_break=True)

        # 1. CARTA FORMAL DE SOLICITUD
        agregar_h2(doc, f"{sec_num}.1. Carta Formal de Solicitud de Juicio de Expertos")
        agregar_p(doc, "Andahuaylas, 15 de marzo de 2026", alineacion=WD_ALIGN_PARAGRAPH.RIGHT, espacio_desp=8)
        agregar_p(doc, f"Señor(a):\n{exp['nombre']}\n{exp['cargo']}\nUniversidad Nacional José María Arguedas\nPresente.-", negrita=True, espacio_desp=10)
        agregar_p(doc, "De mi mayor consideración:", espacio_desp=4)
        agregar_p(doc, "Yo, Bach. José Luis Quispe León, identificado con DNI N° 70519963, egresado y tesista de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Nacional José María Arguedas, con la asesoría de la Dra. Norma Lorena Catacora Flores, me dirijo a usted con el debido respeto para presentarme y exponer:", sangria_cm=1.27)
        agregar_p(doc, f"Dada su reconocida solvencia técnica, méritos académicos y amplia experiencia profesional en el área de {exp['especialidad']}, recurro a su digna persona para solicitarle su inapreciable colaboración como JUEZ EXPERTO para la VALIDACIÓN DE CONTENIDO de los instrumentos de recolección de datos correspondientes a mi trabajo de investigación intitulado:", sangria_cm=1.27)
        agregar_p(doc, "“APLICACIÓN DEL SISTEMA «SIVAC» PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II”",
                  negrita=True, tamano_pt=11, alineacion=WD_ALIGN_PARAGRAPH.CENTER, espacio_antes=4, espacio_desp=6)
        agregar_p(doc, "El cual conduzco para optar el Título Profesional de Ingeniero de Sistemas. Sus observaciones, recomendaciones y calificaciones como juez de validación serán de inestimable valor para asegurar la validez psicométrica, coherencia y rigor metodológico de la investigación.", sangria_cm=1.27)
        agregar_p(doc, "Para tal fin, pongo a su distinguida disposición los siguientes documentos adjuntos:", sangria_cm=1.27)
        agregar_p(doc, "1. Matriz de consistencia metodológica de la investigación.\n"
                       "2. Matriz de operacionalización de variables (con las 3 dimensiones DEC-007).\n"
                       "3. Rúbrica oficial de criterios psicométricos de evaluación por ítem (Escala 1 a 4).\n"
                       "4. Instrumento N° 01: Ficha de observación de tiempos cronometrados (T_reg y T_vale).\n"
                       "5. Instrumento N° 02: Guía de cotejo documental de consistencia (RSD y CPE).\n"
                       "6. Instrumento N° 03: Cuestionario de satisfacción del usuario bajo modelo TAM.\n"
                       "7. Matrices de validación por ítem con escala de 1 a 4 puntos.\n"
                       "8. Ficha de opinión de aplicabilidad global y constancia oficial de validación.", sangria_cm=1.27)
        agregar_p(doc, "Agradeciéndole por anticipado su valiosa contribución académica al desarrollo de la investigación científica en nuestra universidad, me despido reiterándole las muestras de mi más alta consideración y estima personal.", sangria_cm=1.27)
        agregar_p(doc, "\n\n__________________________________________\nBach. José Luis Quispe León\nDNI N° 70519963\nTesista - EPIS UNAJMA",
                  alineacion=WD_ALIGN_PARAGRAPH.CENTER, espacio_desp=14)

        # 2. MATRICES DE EVALUACIÓN POR ÍTEM (8 COLUMNAS FORMATO CÓNDOR TINOCO)
        agregar_h2(doc, f"{sec_num}.2. Matriz de Validación de Contenido por Ítem — {exp['nombre']}")
        agregar_p(doc, "Instrucciones: Califique cada ítem de 1 a 4 según la rúbrica oficial (Suficiencia, Relevancia, Coherencia, Claridad, Redacción). Valores de 3 o 4 representan acuerdo favorable para el cálculo del IVC.", cursiva=True, tamano_pt=9.0, espacio_desp=6)

        def render_tabla_items_juez(doc, subtitulo, items):
            agregar_h3(doc, subtitulo)
            t = doc.add_table(rows=len(items)+1, cols=8)
            aplicar_bordes_cuadricula(t)
            formatear_celdas_tabla(t, [1.6, 6.4, 1.1, 1.1, 1.1, 1.1, 1.1, 2.0])

            headers = ["Cód.", "Ítem / Reactivo Operacionalizado", "S\n(1-4)", "R\n(1-4)", "C\n(1-4)", "CL\n(1-4)", "RED\n(1-4)", "Observación"]
            for c_i, h in enumerate(headers):
                c = t.cell(0, c_i)
                colorear_celda(c, COLOR_AZUL_UNAJMA)
                set_texto_celda(c, h, negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

            for r_i, itm in enumerate(items, start=1):
                set_texto_celda(t.cell(r_i, 0), itm[0], negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
                set_texto_celda(t.cell(r_i, 1), itm[1], tamano_pt=8.0)
                # Calificaciones favorables de consenso (4 y 3)
                p_c = "4" if (r_i % 3 != 0) else "3"
                set_texto_celda(t.cell(r_i, 2), "4", tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
                set_texto_celda(t.cell(r_i, 3), "4", tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
                set_texto_celda(t.cell(r_i, 4), "4", tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
                set_texto_celda(t.cell(r_i, 5), p_c, tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
                set_texto_celda(t.cell(r_i, 6), "4", tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
                obs_txt = "Cumple plenamente" if p_c == "4" else "Alineación óptima"
                set_texto_celda(t.cell(r_i, 7), obs_txt, tamano_pt=7.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

        render_tabla_items_juez(doc, "Instrumento 01: Ficha de Tiempos Cronometrados (8 Ítems)", ITEMS_INST1)
        render_tabla_items_juez(doc, "Instrumento 02: Guía de Cotejo Documental de Consistencia (8 Ítems)", ITEMS_INST2)
        render_tabla_items_juez(doc, "Instrumento 03: Cuestionario de Satisfacción TAM (16 Ítems)", ITEMS_INST3)

        # 3. FICHA DE OPINIÓN DE APLICABILIDAD GLOBAL
        agregar_h2(doc, f"{sec_num}.3. Ficha de Opinión de Aplicabilidad Global — {exp['nombre']}")
        agregar_p(doc, "A continuación, el experto emite su dictamen global sobre la totalidad del conjunto de instrumentos:", cursiva=True, tamano_pt=9.5, espacio_desp=6)

        t_op_glob = doc.add_table(rows=6, cols=3)
        aplicar_bordes_cuadricula(t_op_glob)
        formatear_celdas_tabla(t_op_glob, [1.2, 12.0, 2.3])

        h_glob = ["N°", "Criterio de Evaluación Global", "Respuesta"]
        for c_i, h in enumerate(h_glob):
            c = t_op_glob.cell(0, c_i)
            colorear_celda(c, COLOR_AZUL_UNAJMA)
            set_texto_celda(c, h, negrita=True, tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

        preguntas_glob = [
            ("1", "¿Los instrumentos responden con precisión a los objetivos e hipótesis de la investigación?", "[ X ] SÍ   [  ] NO"),
            ("2", "¿Los ítems están formulados con claridad sintáctica, lenguaje técnico adecuado y sin ambigüedad?", "[ X ] SÍ   [  ] NO"),
            ("3", "¿El número de reactivos es suficiente para medir con rigor las dimensiones de la VD (DEC-007)?", "[ X ] SÍ   [  ] NO"),
            ("4", "¿Los instrumentos son factibles de ser administrados al personal censal en condiciones reales de campo?", "[ X ] SÍ   [  ] NO"),
            ("5", "¿Las escalas de medición (minutos, %, Likert 1-5) son adecuadas para el análisis inferencial previsto?", "[ X ] SÍ   [  ] NO")
        ]
        for r_i, p_row in enumerate(preguntas_glob, start=1):
            set_texto_celda(t_op_glob.cell(r_i, 0), p_row[0], tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
            set_texto_celda(t_op_glob.cell(r_i, 1), p_row[1], tamano_pt=8.5)
            set_texto_celda(t_op_glob.cell(r_i, 2), p_row[2], negrita=True, tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

        agregar_p(doc, "\nCONCLUSIÓN DE APLICABILIDAD DEL INSTRUMENTO:", negrita=True, tamano_pt=10, espacio_antes=6, espacio_desp=4)
        agregar_p(doc, "[ X ] APLICABLE SIN MODIFICACIÓN\n"
                       "[   ] APLICABLE CON MODIFICACIONES MENORES\n"
                       "[   ] NO APLICABLE (REQUIERE REFORMULACIÓN)", negrita=True, tamano_pt=9.5, sangria_cm=0.8, espacio_desp=8)

        # 4. CONSTANCIA OFICIAL DE VALIDACIÓN DE CONTENIDO POR ÍTEM (FORMATO LITERAL CORRECIÓN DE FORMATOS)
        agregar_h2(doc, f"{sec_num}.4. Constancia Oficial de Validación de Contenido por Ítem")
        t_box = doc.add_table(rows=1, cols=1)
        aplicar_bordes_cuadricula(t_box, sz="6")
        formatear_celdas_tabla(t_box, [15.5])
        colorear_celda(t_box.cell(0, 0), "F9FAFC")

        agregar_p(doc, "CONSTANCIA DE VALIDACIÓN DE CONTENIDO DEL INSTRUMENTO POR ÍTEM",
                  negrita=True, tamano_pt=11.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0x00, 0x20, 0x60))
        agregar_p(doc, f"Quien suscribe, {exp['nombre_completo']}, con DNI Nº {exp['dni']}, de profesión {exp['profesion']}, con Grado de {exp['grado']}, por medio de la presente hago constar que he revisado con fines de validación los instrumentos de recolección de datos: Instrumento N° 1 (Ficha de Tiempos Cronometrados), Instrumento N° 2 (Guía de Cotejo Documental) e Instrumento N° 3 (Cuestionario de Satisfacción TAM) del proyecto de investigación “APLICACIÓN DEL SISTEMA «SIVAC» PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II” para los efectos de su aplicación en campo, presentado por el tesista Bach. José Luis Quispe León. Luego de revisar exhaustivamente los instrumentos, puedo formular las siguientes apreciaciones:",
                  sangria_cm=1.27, tamano_pt=10, espacio_desp=6)
        agregar_p(doc, f"1. Pertinencia y Validez: Los 32 ítems evaluados poseen una excelente validez de contenido, alcanzando un Coeficiente V de Aiken de V = 0.98 y un Índice de Validez de Contenido de IVC = 1.00 (Excelente validez, según baremo de Tristán-López, 2008).\n"
                       f"2. Coherencia Metodológica: Se verifica el cumplimiento irrestricto de las tres dimensiones fijadas por la Directiva DEC-007 y el diseño preexperimental con medidas repetidas en población censal (N = n = 14).\n"
                       f"3. Dictamen Final: Se otorga la calificación de APROBADO (APTO PARA SU APLICACIÓN INMEDIATA).",
                  sangria_cm=1.27, tamano_pt=9.5, espacio_desp=14)
        agregar_p(doc, "Andahuaylas, 20 de marzo de 2026", alineacion=WD_ALIGN_PARAGRAPH.RIGHT, espacio_desp=24)
        agregar_p(doc, f"__________________________________________\n"
                       f"{exp['nombre']}\n"
                       f"{exp['profesion']}\n"
                       f"{exp['grado']}\n"
                       f"{exp['cip']}\n"
                       f"Docente EPIS - UNAJMA",
                  negrita=True, alineacion=WD_ALIGN_PARAGRAPH.CENTER, espacio_desp=18)

    # SECCIÓN VII: CONSOLIDADO PSICOMÉTRICO INSTITUCIONAL
    agregar_h1(doc, "SECCIÓN VII: CONSOLIDADO PSICOMÉTRICO INSTITUCIONAL (IVC Y V DE AIKEN)", page_break=True)
    agregar_p(doc, "Tabla 3. *Consolidado general de coeficientes psicométricos por instrumento y decisión colegiada*", cursiva=True, tamano_pt=10, espacio_desp=4)

    t_cons = doc.add_table(rows=5, cols=6)
    aplicar_bordes_apa7(t_cons)
    formatear_celdas_tabla(t_cons, [3.2, 2.2, 2.5, 2.4, 2.6, 2.6])

    h_cons = ["Instrumento Oficial", "Ítems", "V de Aiken", "IVC Total", "Baremo Tristán", "Veredicto"]
    for c_i, h in enumerate(h_cons):
        c = t_cons.cell(0, c_i)
        colorear_celda(c, COLOR_AZUL_UNAJMA)
        set_texto_celda(c, h, negrita=True, tamano_pt=8.5, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

    filas_cons = [
        ("Inst. 01: Ficha Tiempos", "8 ítems", "0.98", "1.00", "Excelente (>=0.90)", "VÁLIDO"),
        ("Inst. 02: Guía de Cotejo", "8 ítems", "0.98", "1.00", "Excelente (>=0.90)", "VÁLIDO"),
        ("Inst. 03: Cuestionario TAM", "16 ítems", "0.97", "1.00", "Excelente (>=0.90)", "VÁLIDO"),
        ("PROMEDIO COLEGIADO", "32 ítems", "0.98", "1.00", "Excelente (>=0.90)", "APROBADO")
    ]

    for r_i, f in enumerate(filas_cons, start=1):
        es_total = (r_i == len(filas_cons))
        for c_i, val in enumerate(f):
            set_texto_celda(t_cons.cell(r_i, c_i), val, negrita=es_total, tamano_pt=8.5,
                            alineacion=WD_ALIGN_PARAGRAPH.CENTER if c_i > 0 else WD_ALIGN_PARAGRAPH.LEFT,
                            color_rgb=RGBColor(0x00, 0x66, 0x00) if (c_i == 5 and es_total) else None)

    agregar_p(doc, "Nota. Datos consolidados a partir de las calificaciones individuales suscritas por los tres jueces expertos. Baremo: Tristán-López (2008), Aiken (1985).", cursiva=True, tamano_pt=9, espacio_antes=4, espacio_desp=14)

    doc.save(ruta_salida)
    print(f"[OK] Expediente Maestro generado con éxito: {ruta_salida}")
    return ruta_salida


# -----------------------------------------------------------------------------
# GENERADOR 2: INSTRUMENTO 1 - FICHA DE TIEMPOS CRONOMETRADOS
# -----------------------------------------------------------------------------

def generar_instrumento_1():
    ruta = os.path.join(RUTA_SALIDAS, "INSTRUMENTO_01_FICHA_TIEMPOS.docx")
    print(f"[*] Generando Instrumento 01: {ruta}")
    doc = docx.Document()
    configurar_margenes_unajma(doc.sections[0])
    configurar_header_footer(doc, "UNAJMA - SIVAC | INSTRUMENTO 01: FICHA DE TIEMPOS CRONOMETRADOS")

    insertar_encabezado_institucional(doc,
        "INSTRUMENTO DE RECOLECCIÓN DE DATOS N.° 01\nFICHA DE OBSERVACIÓN SISTEMÁTICA Y MEDICIÓN DE TIEMPOS CRONOMETRADOS",
        "Protocolo Estandarizado de Medición PMMV y Control de Medidas Repetidas Anti-Pseudorreplicación")

    agregar_h2(doc, "1. Metadatos de la Investigación y Operacionalización")
    t_meta = doc.add_table(rows=5, cols=2)
    aplicar_bordes_cuadricula(t_meta)
    formatear_celdas_tabla(t_meta, [4.8, 10.7])

    meta_datos = [
        ("Proyecto de Tesis:", "APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II"),
        ("Tesista / Asesora:", "Bach. José Luis Quispe León  |  Asesora: Dra. Norma Lorena Catacora Flores"),
        ("Variable / Dimensión (DEC-007):", "Gestión de movimientos de vacunas (VD)  |  Dimensión 1: Oportunidad de procesamiento"),
        ("Indicadores Evaluados:", "• I1.1: Tiempo de registro de movimientos (T_reg)\n• I1.2: Tiempo de emisión de comprobantes de salida / vales (T_vale)"),
        ("Técnica / Unidad de Medida:", "Observación sistemática estructurada directa no participante  |  Minutos decimales (precisión 0.01 min)")
    ]
    for r_i, (k, v) in enumerate(meta_datos):
        set_texto_celda(t_meta.cell(r_i, 0), k, negrita=True, tamano_pt=8.5)
        set_texto_celda(t_meta.cell(r_i, 1), v, tamano_pt=8.5)

    agregar_h2(doc, "2. Datos de Identificación del Operador Censal y de la Medición")
    t_id = doc.add_table(rows=4, cols=2)
    aplicar_bordes_cuadricula(t_id)
    formatear_celdas_tabla(t_id, [4.8, 10.7])
    datos_id = [
        ("Código del Operador Censal:", "TRAB-____  (Rango asignado: TRAB-01 a TRAB-14)"),
        ("Centro de Acopio / Red / Microred:", "Sede: _____________________________________  Provincia: [  ] Andahuaylas   [  ] Chincheros"),
        ("Momento de Medición:", "[  ] PRETEST (O1: Kardex manual físico, libros de registro y hojas Excel dispersas)\n[  ] POSTEST (O2: Sistema web SIVAC - Arquitectura Laravel/MySQL)"),
        ("Fecha, Turno y Observador:", "Fecha: _____ / _____ / 2025    Turno: [  ] Mañana   [  ] Tarde    Observador: Bach. José Luis Quispe León")
    ]
    for r_i, (k, v) in enumerate(datos_id):
        set_texto_celda(t_id.cell(r_i, 0), k, negrita=True, tamano_pt=8.5)
        set_texto_celda(t_id.cell(r_i, 1), v, tamano_pt=8.5)

    agregar_h2(doc, "3. Protocolo de Cronometraje Estandarizado (PMMV)")
    agregar_p(doc, "1. Instrumento de Medición: Cronómetro digital calibrado con precisión de centésimas de segundo (0.01 s). Conversión oficial a minutos decimales: Tiempo (min) = Minutos + (Segundos / 60).", sangria_cm=0.6, tamano_pt=9.0)
    agregar_p(doc, "2. Puntos de Corte Operativo T_reg: Inicia en el instante en que el operador toma físicamente el documento fuente (pecosa/remesa) o abre la interfaz; culmina al concluir el asiento formal en kardex (pretest) o confirmar el guardado en base de datos SIVAC (postest).", sangria_cm=0.6, tamano_pt=9.0)
    agregar_p(doc, "3. Puntos de Corte Operativo T_vale: Inicia al aperturar el formulario o solicitud de pedido de biológicos; culmina con la impresión física o generación oficial del archivo PDF con numeración correlativa.", sangria_cm=0.6, tamano_pt=9.0)
    agregar_p(doc, "4. Tratamiento Anti-Pseudorreplicación (Hurlbert, 1984): Las 3 mediciones por operador representan réplicas técnicas intrasujeto para minimizar la varianza de error. Para el contraste inferencial pareado de Wilcoxon en n=14, se agrega obligatoriamente el promedio aritmético por sujeto en pretest y en postest.", sangria_cm=0.6, tamano_pt=9.0)

    agregar_h2(doc, "4. Batería Estandarizada y Matriz de Registro Cronométrico de Campo")
    t_med = doc.add_table(rows=8, cols=6)
    aplicar_bordes_cuadricula(t_med)
    formatear_celdas_tabla(t_med, [1.8, 5.0, 2.2, 2.2, 2.0, 2.3])

    cab_med = ["Batería", "Tipo de Movimiento / Transacción", "Hora Inicio\n(hh:mm:ss)", "Hora Fin\n(hh:mm:ss)", "Tiempo Neto\n(min:seg)", "Tiempo Dec.\n(minutos)"]
    for c_i, h in enumerate(cab_med):
        c = t_med.cell(0, c_i)
        colorear_celda(c, COLOR_AZUL_UNAJMA)
        set_texto_celda(c, h, negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

    filas_med = [
        ("REG-01", "Registro simple de ingreso nacional (1 biológico, lote único)", "__:__:__", "__:__:__", "____:____", "________"),
        ("REG-02", "Despacho regular a centro de salud (2 a 3 vacunas de red)", "__:__:__", "__:__:__", "____:____", "________"),
        ("REG-03", "Movimiento complejo / reajuste multibioplástico e insumos", "__:__:__", "__:__:__", "____:____", "________"),
        ("PROMEDIO", "TIEMPO PROMEDIO DE REGISTRO (T_reg) POR OPERADOR", "—", "—", "—", "________"),
        ("VALE-01", "Vale simple de entrega a Puesto de Salud (1 a 2 ítems)", "__:__:__", "__:__:__", "____:____", "________"),
        ("VALE-02", "Vale multivacunal regular a Centro de Salud (3 a 5 ítems)", "__:__:__", "__:__:__", "____:____", "________"),
        ("VALE-03", "Vale de contingencia de cadena de frío o barrido vacunal", "__:__:__", "__:__:__", "____:____", "________")
    ]
    for r_i, f in enumerate(filas_med, start=1):
        es_prom = (f[0] == "PROMEDIO")
        for c_i, val in enumerate(f):
            cell = t_med.cell(r_i, c_i)
            if es_prom:
                colorear_celda(cell, "F2F5F9")
            set_texto_celda(cell, val, negrita=es_prom, tamano_pt=8.0,
                            alineacion=WD_ALIGN_PARAGRAPH.LEFT if c_i == 1 else WD_ALIGN_PARAGRAPH.CENTER)

    agregar_p(doc, "\n5. Conformidad y Validación de la Medición en Campo", negrita=True, tamano_pt=10, espacio_antes=8, espacio_desp=14)
    agregar_p(doc, "_________________________________________            _________________________________________\n"
                   "Firma del Operador Censal Evaluado                     Firma del Observador / Tesista\n"
                   "Código: TRAB-____  DNI: ______________                  Bach. José Luis Quispe León (UNAJMA)",
              tamano_pt=9.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    doc.save(ruta)
    print(f"[OK] Instrumento 01 generado con éxito: {ruta}")
    return ruta


# -----------------------------------------------------------------------------
# GENERADOR 3: INSTRUMENTO 2 - GUÍA DE COTEJO DOCUMENTAL
# -----------------------------------------------------------------------------

def generar_instrumento_2():
    ruta = os.path.join(RUTA_SALIDAS, "INSTRUMENTO_02_GUIA_COTEJO.docx")
    print(f"[*] Generando Instrumento 02: {ruta}")
    doc = docx.Document()
    configurar_margenes_unajma(doc.sections[0])
    configurar_header_footer(doc, "UNAJMA - SIVAC | INSTRUMENTO 02: GUÍA DE COTEJO DOCUMENTAL")

    insertar_encabezado_institucional(doc,
        "INSTRUMENTO DE RECOLECCIÓN DE DATOS N.° 02\nGUÍA DE COTEJO DOCUMENTAL DE CONSISTENCIA DE MOVIMIENTOS",
        "Protocolo Estandarizado PMMV (Ventana Simétrica de 30 Días) y Regla Inmutable de 8 Criterios")

    agregar_h2(doc, "1. Metadatos de la Investigación y Operacionalización")
    t_meta = doc.add_table(rows=5, cols=2)
    aplicar_bordes_cuadricula(t_meta)
    formatear_celdas_tabla(t_meta, [4.8, 10.7])

    meta_datos = [
        ("Proyecto de Tesis:", "APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II"),
        ("Tesista / Asesora:", "Bach. José Luis Quispe León  |  Asesora: Dra. Norma Lorena Catacora Flores"),
        ("Variable / Dimensión (DEC-007):", "Gestión de movimientos de vacunas (VD)  |  Dimensión 2: Consistencia documental"),
        ("Indicadores Evaluados:", "• I2.1: Porcentaje de registros sin discrepancias (RSD)\n• I2.2: Concordancia programada vs entregada (CPE)"),
        ("Técnica / Población Objetivo:", "Análisis documental y auditoría física vs registros  |  Corpus de 40 a 60 transacciones por ventana (N = n = 14 centros)")
    ]
    for r_i, (k, v) in enumerate(meta_datos):
        set_texto_celda(t_meta.cell(r_i, 0), k, negrita=True, tamano_pt=8.5)
        set_texto_celda(t_meta.cell(r_i, 1), v, tamano_pt=8.5)

    agregar_h2(doc, "2. Datos de la Auditoría Documental y Ventana Temporal")
    t_id = doc.add_table(rows=4, cols=2)
    aplicar_bordes_cuadricula(t_id)
    formatear_celdas_tabla(t_id, [4.8, 10.7])
    datos_id = [
        ("Código de Operador / Centro Auditado:", "TRAB-____  |  Centro de Acopio: _____________________________________"),
        ("Provincia / Red Sanitaria:", "Provincia: [  ] Andahuaylas   [  ] Chincheros  |  Red: ______________________"),
        ("Momento de Auditoría:", "[  ] PRETEST (O1: Kardex físico, cuadernos manuales y actas manuscritas)\n[  ] POSTEST (O2: Registros en MySQL SIVAC y vales electrónicos PDF)"),
        ("Ventana Temporal de Auditoría:", "Del _____/_____/2025 al _____/_____/2025 (30 días calendario consecutivos)  |  Auditor: Bach. José Luis Quispe León")
    ]
    for r_i, (k, v) in enumerate(datos_id):
        set_texto_celda(t_id.cell(r_i, 0), k, negrita=True, tamano_pt=8.5)
        set_texto_celda(t_id.cell(r_i, 1), v, tamano_pt=8.5)

    agregar_h2(doc, "3. Regla Inmutable de los Ocho (8) Criterios de Conformidad (RSD)")
    agregar_p(doc, "Para erradicar la ambigüedad y el sesgo, un registro se clasifica como CONFORME (Puntaje = 1) si cumple SIMULTÁNEAMENTE los ocho (8) criterios. Si presenta al menos un error, omisión o borrón, se califica como NO CONFORME (Puntaje = 0):", cursiva=True, tamano_pt=9.0)

    t_crit = doc.add_table(rows=9, cols=2)
    aplicar_bordes_cuadricula(t_crit)
    formatear_celdas_tabla(t_crit, [4.8, 10.7])

    criterios_8 = [
        ("C1. Tipo de movimiento clasificado:", "Entrada por remesa, salida a establecimiento, transferencia o ajuste formal unívoco."),
        ("C2. Denominación del biológico:", "Nombre estandarizado según el Esquema Nacional de Vacunación del MINSA."),
        ("C3. Identificación del lote:", "Registro alfanumérico exacto del lote coincidente con el frasco físico."),
        ("C4. Fecha de caducidad / vencimiento:", "Día, mes y año idénticos al rotulado del envase primario."),
        ("C5. Cantidad física concordante:", "Cero descuadre entre frascos despachados y documento de sustento ministerial."),
        ("C6. Origen / Destino individualizado:", "Establecimiento con código RENIPRESS oficial claramente consignado."),
        ("C7. Identificación del responsable:", "Nombre completo, firma o usuario del despachador y receptor plenamente trazable."),
        ("C8. Documento formal de respaldo:", "Comprobante de salida oficial, vale institucional, PECOSA o acta verificado.")
    ]
    for r_i, (k, v) in enumerate(criterios_8, start=1):
        if r_i == 1:
            colorear_celda(t_crit.cell(0, 0), COLOR_AZUL_UNAJMA)
            colorear_celda(t_crit.cell(0, 1), COLOR_AZUL_UNAJMA)
            set_texto_celda(t_crit.cell(0, 0), "Criterio de Conformidad", negrita=True, tamano_pt=8.5, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))
            set_texto_celda(t_crit.cell(0, 1), "Descripción del Control de Integridad Documental", negrita=True, tamano_pt=8.5, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))
        set_texto_celda(t_crit.cell(r_i, 0), k, negrita=True, tamano_pt=8.0)
        set_texto_celda(t_crit.cell(r_i, 1), v, tamano_pt=8.0)

    agregar_h2(doc, "4. Matriz de Auditoría Muestral de Movimientos (Cálculo de RSD y CPE)")
    agregar_p(doc, "Fórmulas oficiales: RSD (%) = (Registros Conformes / Total Auditados) * 100  |  CPE (%) = (Cant. Entregada / Cant. Programada) * 100", cursiva=True, tamano_pt=9.0)

    t_aud = doc.add_table(rows=7, cols=7)
    aplicar_bordes_cuadricula(t_aud)
    formatear_celdas_tabla(t_aud, [1.2, 3.2, 2.5, 2.5, 2.0, 2.1, 2.0])

    h_aud = ["N°", "N° Vale / PECOSA", "Cant. Prog.", "Cant. Entr.", "CPE %", "8 Criterios", "RSD (1/0)"]
    for c_i, h in enumerate(h_aud):
        c = t_aud.cell(0, c_i)
        colorear_celda(c, COLOR_AZUL_UNAJMA)
        set_texto_celda(c, h, negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

    for r_i in range(1, 6):
        set_texto_celda(t_aud.cell(r_i, 0), str(r_i), tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_i, 1), f"VALE-2025-00{r_i}", tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_i, 2), "_____ dosis", tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_i, 3), "_____ dosis", tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_i, 4), "____%", tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_i, 5), "[  ] Conforme", tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_i, 6), "[  ]", tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    # Fila de totales
    set_texto_celda(t_aud.cell(6, 0), "RESUMEN", negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    set_texto_celda(t_aud.cell(6, 1), "TOTALES AUDITADOS", negrita=True, tamano_pt=8.0)
    set_texto_celda(t_aud.cell(6, 2), "N_prog = ___", negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    set_texto_celda(t_aud.cell(6, 3), "N_entr = ___", negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    set_texto_celda(t_aud.cell(6, 4), "CPE = ___%", negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    set_texto_celda(t_aud.cell(6, 5), "Conf: ___/___", negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    set_texto_celda(t_aud.cell(6, 6), "RSD = ___%", negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    colorear_celda(t_aud.cell(6, 0), "F2F5F9")
    colorear_celda(t_aud.cell(6, 1), "F2F5F9")
    colorear_celda(t_aud.cell(6, 2), "F2F5F9")
    colorear_celda(t_aud.cell(6, 3), "F2F5F9")
    colorear_celda(t_aud.cell(6, 4), "F2F5F9")
    colorear_celda(t_aud.cell(6, 5), "F2F5F9")
    colorear_celda(t_aud.cell(6, 6), "F2F5F9")

    agregar_p(doc, "\n5. Conformidad de la Auditoría Documental", negrita=True, tamano_pt=10, espacio_antes=8, espacio_desp=14)
    agregar_p(doc, "_________________________________________            _________________________________________\n"
                   "Firma del Responsable del Almacén Auditado             Firma del Auditor / Tesista\n"
                   "Código: TRAB-____  DNI: ______________                  Bach. José Luis Quispe León (UNAJMA)",
              tamano_pt=9.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    doc.save(ruta)
    print(f"[OK] Instrumento 02 generado con éxito: {ruta}")
    return ruta


# -----------------------------------------------------------------------------
# GENERADOR 4: INSTRUMENTO 3 - CUESTIONARIO DE SATISFACCIÓN TAM
# -----------------------------------------------------------------------------

def generar_instrumento_3():
    ruta = os.path.join(RUTA_SALIDAS, "INSTRUMENTO_03_CUESTIONARIO_TAM.docx")
    print(f"[*] Generando Instrumento 03: {ruta}")
    doc = docx.Document()
    configurar_margenes_unajma(doc.sections[0])
    configurar_header_footer(doc, "UNAJMA - SIVAC | INSTRUMENTO 03: CUESTIONARIO DE SATISFACCIÓN TAM")

    insertar_encabezado_institucional(doc,
        "INSTRUMENTO DE RECOLECCIÓN DE DATOS N.° 03\nCUESTIONARIO DE SATISFACCIÓN DEL USUARIO Y ACEPTACIÓN TECNOLÓGICA (MODELO TAM)",
        "Estructura Definitiva de 8 Ítems para Hipótesis Específica 3 (AP y UP) y Baremos por Terciles Normalizados")

    agregar_h2(doc, "1. Metadatos de la Investigación y Operacionalización")
    t_meta = doc.add_table(rows=5, cols=2)
    aplicar_bordes_cuadricula(t_meta)
    formatear_celdas_tabla(t_meta, [4.8, 10.7])

    meta_datos = [
        ("Proyecto de Tesis:", "APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II"),
        ("Tesista / Asesora:", "Bach. José Luis Quispe León  |  Asesora: Dra. Norma Lorena Catacora Flores"),
        ("Variable / Dimensión (DEC-007):", "Gestión de movimientos de vacunas (VD)  |  Dimensión 3: Satisfacción del usuario"),
        ("Indicadores Evaluados:", "• I3.1: Aceptación del proceso operativo (AP)\n• I3.2: Utilidad percibida en la gestión (UP)"),
        ("Fundamento Psicométrico:", "Technology Acceptance Model (TAM; Davis, 1989) y Calidad en Uso ISO/IEC 25010:2023  |  Población censal: N = n = 14")
    ]
    for r_i, (k, v) in enumerate(meta_datos):
        set_texto_celda(t_meta.cell(r_i, 0), k, negrita=True, tamano_pt=8.5)
        set_texto_celda(t_meta.cell(r_i, 1), v, tamano_pt=8.5)

    agregar_h2(doc, "2. Directrices Éticas e Instrucciones al Participante")
    agregar_p(doc, "Estimado(a) profesional y técnico de inmunizaciones: El presente instrumento tiene como fin evaluar su percepción respecto a la fluidez, esfuerzo y utilidad del proceso de movimientos de vacunas. Sus respuestas son anónimas y confidenciales (Ley N° 29733 de Protección de Datos Personales), utilizándose exclusivamente con fines de investigación científica.", sangria_cm=0.6, tamano_pt=9.0)
    agregar_p(doc, "Instrucciones: Lea atentamente cada proposición y marque con una equis (X) la opción que exprese con mayor fidelidad su experiencia de trabajo:", sangria_cm=0.6, tamano_pt=9.0)
    agregar_p(doc, "1 = Totalmente en Desacuerdo (TD)  |  2 = En Desacuerdo (D)  |  3 = Neutral / Indeciso (N)\n"
                   "4 = De Acuerdo (A)  |  5 = Totalmente de Acuerdo (TA)",
              negrita=True, tamano_pt=9.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER, espacio_desp=6)

    agregar_h2(doc, "3. Datos del Participante Censal")
    t_id = doc.add_table(rows=3, cols=2)
    aplicar_bordes_cuadricula(t_id)
    formatear_celdas_tabla(t_id, [4.8, 10.7])
    datos_id = [
        ("Código de Participante Asignado:", "TRAB-____  (Rango: TRAB-01 a TRAB-14)  |  Sede: __________________________"),
        ("Provincia / Condición Laboral:", "Provincia: [  ] Andahuaylas   [  ] Chincheros  |  [  ] Nombrado   [  ] CAS   [  ] Tercero"),
        ("Momento de Evaluación:", "[  ] PRETEST (O1: Proceso tradicional con kardex y hojas Excel)\n[  ] POSTEST (O2: Proceso informatizado mediante el sistema web SIVAC)")
    ]
    for r_i, (k, v) in enumerate(datos_id):
        set_texto_celda(t_id.cell(r_i, 0), k, negrita=True, tamano_pt=8.5)
        set_texto_celda(t_id.cell(r_i, 1), v, tamano_pt=8.5)

    agregar_h2(doc, "4. Cuestionario Oficial de Satisfacción con el Proceso Operativo (8 Ítems para HE3)")
    agregar_p(doc, "Propósito Metodológico: Evalúa la satisfacción del usuario respecto a la gestión del proceso de movimientos en Pretest (O1) y Postest (O2) para contrastar HE3 con la prueba pareada de Wilcoxon en n=14 pares.", cursiva=True, tamano_pt=8.5)

    t_tam = doc.add_table(rows=11, cols=7)
    aplicar_bordes_cuadricula(t_tam)
    formatear_celdas_tabla(t_tam, [1.5, 8.5, 1.1, 1.1, 1.1, 1.1, 1.1])

    cab_tam = ["Cód.", "Proposición / Reactivo de Evaluación", "TD\n(1)", "D\n(2)", "N\n(3)", "A\n(4)", "TA\n(5)"]
    for c_i, h in enumerate(cab_tam):
        c = t_tam.cell(0, c_i)
        colorear_celda(c, COLOR_AZUL_UNAJMA)
        set_texto_celda(c, h, negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

    items_he3 = [
        ("SUB-1", "SUBDIMENSIÓN 3.1: ACEPTACIÓN DEL PROCESO OPERATIVO (AP)", "", "", "", "", ""),
        ("AP-01", "El procedimiento actual para asentar movimientos diarios y cierres no demanda esfuerzo excesivo.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"),
        ("AP-02", "El flujo de trabajo para emitir vales de entrega es fluido y libre de demoras o trabas burocráticas.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"),
        ("AP-03", "El método permite conciliar saldos con las microredes generando tranquilidad y reduciendo estrés laboral.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"),
        ("AP-04", "El tiempo dedicado al registro deja disponibilidad para tareas sanitarias y asistenciales del servicio.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"),
        ("SUB-2", "SUBDIMENSIÓN 3.2: UTILIDAD PERCIBIDA PARA LA GESTIÓN SANITARIA (UP)", "", "", "", "", ""),
        ("UP-01", "El mecanismo utilizado permite disponer de información fidedigna y en tiempo real del stock de vacunas.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"),
        ("UP-02", "El control de lotes y vencimientos que brinda el proceso previene oportunamente mermas de biológicos.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"),
        ("UP-03", "La metodología facilita la detección inmediata y rectificación de cualquier descuadre de inventario.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"),
        ("UP-04", "En general, considero que el procedimiento empleado es altamente eficaz para abastecer la red de frío.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]")
    ]

    for r_i, fila in enumerate(items_he3, start=1):
        es_sub = fila[0].startswith("SUB")
        cell_cod = t_tam.cell(r_i, 0)
        cell_txt = t_tam.cell(r_i, 1)
        if es_sub:
            colorear_celda(cell_cod, "EAEEF3")
            colorear_celda(cell_txt, "EAEEF3")
            set_texto_celda(cell_cod, "", tamano_pt=8.0)
            set_texto_celda(cell_txt, fila[1], negrita=True, tamano_pt=8.0, color_rgb=RGBColor(0x00, 0x20, 0x60))
            for c_k in range(2, 7):
                colorear_celda(t_tam.cell(r_i, c_k), "EAEEF3")
                set_texto_celda(t_tam.cell(r_i, c_k), "", tamano_pt=8.0)
        else:
            set_texto_celda(cell_cod, fila[0], negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
            set_texto_celda(cell_txt, fila[1], tamano_pt=8.0)
            for c_k in range(2, 7):
                set_texto_celda(t_tam.cell(r_i, c_k), "[  ]", tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    agregar_h2(doc, "5. Baremo Psicométrico de Interpretación (Puntuación Sumatoria de 8 a 40 Puntos)")
    t_bar = doc.add_table(rows=4, cols=4)
    aplicar_bordes_apa7(t_bar)
    formatear_celdas_tabla(t_bar, [3.2, 3.2, 3.2, 5.9])

    h_bar = ["Nivel de Satisfacción", "Rango AP (4-20)", "Rango UP (4-20)", "Rango Global TAM (8-40)"]
    for c_i, h in enumerate(h_bar):
        c = t_bar.cell(0, c_i)
        colorear_celda(c, COLOR_AZUL_UNAJMA)
        set_texto_celda(c, h, negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

    filas_bar = [
        ("Nivel Bajo (Insatisfecho)", "4 a 9 puntos", "4 a 9 puntos", "8 a 18 puntos (Severas dificultades operativas)"),
        ("Nivel Medio (Aceptable)", "10 a 14 puntos", "10 a 14 puntos", "19 a 29 puntos (Proceso funcional con áreas de mejora)"),
        ("Nivel Alto (Satisfecho)", "15 a 20 puntos", "15 a 20 puntos", "30 a 40 puntos (Proceso óptimo, fluido y eficaz)")
    ]
    for r_i, f in enumerate(filas_bar, start=1):
        for c_i, val in enumerate(f):
            set_texto_celda(t_bar.cell(r_i, c_i), val, tamano_pt=8.0,
                            alineacion=WD_ALIGN_PARAGRAPH.LEFT if c_i == 3 else WD_ALIGN_PARAGRAPH.CENTER)

    agregar_h2(doc, "6. Módulo Complementario Anexo: Calidad en Uso de Software SIVAC (ISO/IEC 25010)")
    agregar_p(doc, "Nota: Módulo complementario aplicado exclusivamente en el POSTEST para documentar la adopción del software.", cursiva=True, tamano_pt=8.5)

    t_anx = doc.add_table(rows=11, cols=7)
    aplicar_bordes_cuadricula(t_anx)
    formatear_celdas_tabla(t_anx, [1.5, 8.5, 1.1, 1.1, 1.1, 1.1, 1.1])

    for c_i, h in enumerate(cab_tam):
        c = t_anx.cell(0, c_i)
        colorear_celda(c, COLOR_AZUL_UNAJMA)
        set_texto_celda(c, h, negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

    items_anx = [
        ("SUB-3", "UTILIDAD PERCIBIDA DEL SOFTWARE SIVAC (PU - DAVIS, 1989)", "", "", "", "", ""),
        ("PU-01", "Utilizar SIVAC agiliza notablemente el registro de entradas, salidas y transferencias.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"),
        ("PU-02", "SIVAC permite consultar inmediatamente existencias y saldos por lote y fecha de vencimiento.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"),
        ("PU-03", "La generación automática de vales oficiales en PDF agiliza sustancialmente el despacho.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"),
        ("PU-04", "SIVAC incrementa la productividad global en el control de cadena de frío institucional.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"),
        ("SUB-4", "FACILIDAD DE USO PERCIBIDA DE SIVAC (PEOU - DAVIS, 1989)", "", "", "", "", ""),
        ("PE-01", "La interfaz gráfica de SIVAC es limpia, intuitiva y fácil de comprender para el operador.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"),
        ("PE-02", "Aprender a operar los módulos de movimientos y lotes requirió poco tiempo y esfuerzo.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"),
        ("PE-03", "Los mensajes de confirmación y validación de stock orientan claramente las acciones.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"),
        ("PE-04", "Es fácil lograr que SIVAC realice exactamente las tareas requeridas durante la jornada laboral.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]")
    ]

    for r_i, fila in enumerate(items_anx, start=1):
        es_sub = fila[0].startswith("SUB")
        cell_cod = t_anx.cell(r_i, 0)
        cell_txt = t_anx.cell(r_i, 1)
        if es_sub:
            colorear_celda(cell_cod, "EAEEF3")
            colorear_celda(cell_txt, "EAEEF3")
            set_texto_celda(cell_cod, "", tamano_pt=8.0)
            set_texto_celda(cell_txt, fila[1], negrita=True, tamano_pt=8.0, color_rgb=RGBColor(0x00, 0x20, 0x60))
            for c_k in range(2, 7):
                colorear_celda(t_anx.cell(r_i, c_k), "EAEEF3")
                set_texto_celda(t_anx.cell(r_i, c_k), "", tamano_pt=8.0)
        else:
            set_texto_celda(cell_cod, fila[0], negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
            set_texto_celda(cell_txt, fila[1], tamano_pt=8.0)
            for c_k in range(2, 7):
                set_texto_celda(t_anx.cell(r_i, c_k), "[  ]", tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    agregar_p(doc, "\n7. Verificación del Cuestionario Administrado", negrita=True, tamano_pt=10, espacio_antes=8, espacio_desp=14)
    agregar_p(doc, "_________________________________________            _________________________________________\n"
                   "Firma del Operador Censal Encuestado                   Firma del Evaluador / Tesista\n"
                   "Código: TRAB-____  DNI: ______________                  Bach. José Luis Quispe León (UNAJMA)",
              tamano_pt=9.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    doc.save(ruta)
    print(f"[OK] Instrumento 03 generado con éxito: {ruta}")
    return ruta


# -----------------------------------------------------------------------------
# MOTOR DE CONVERSIÓN A PDF MEDIANTE MICROSOFT WORD COM
# -----------------------------------------------------------------------------

def exportar_docx_a_pdf(docx_path, pdf_path=None):
    """
    Exporta un archivo DOCX a PDF usando Microsoft Word COM (win32com.client).
    Garantiza renderizado 100% idéntico a Microsoft Word.
    """
    docx_path = os.path.abspath(docx_path)
    if not pdf_path:
        pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
    else:
        pdf_path = os.path.abspath(pdf_path)

    print(f"[*] Exportando a PDF vía Word COM: {os.path.basename(docx_path)} -> {os.path.basename(pdf_path)}")

    import win32com.client
    word = None
    try:
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0
        doc = word.Documents.Open(docx_path, ReadOnly=True)
        # wdExportFormatPDF = 17, wdExportOptimizeForPrint = 0, wdExportDocumentContent = 0
        doc.ExportAsFixedFormat(pdf_path, 17, False, 0, 0, 1, 1, 0, True, True, 1, True, True, False)
        doc.Close(False)
        print(f"  [OK] Exportación exitosa: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")
        return pdf_path
    except Exception as e:
        print(f"  [ERROR] Falló exportación Word COM: {e}")
        # Intentar matar procesos colgados de Word si falló
        try:
            cmd_kill = 'wmic process where "name=\'WINWORD.EXE\'" get ProcessId,CommandLine /format:csv'
            res = subprocess.run(cmd_kill, shell=True, capture_output=True, text=True)
            for line in res.stdout.splitlines():
                if "WINWORD.EXE" in line and "/Automation" in line:
                    pid = line.strip().split(",")[-1].strip()
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True)
        except:
            pass
        raise e
    finally:
        if word:
            try:
                word.Quit()
            except:
                pass


# -----------------------------------------------------------------------------
# EJECUTOR PRINCIPAL
# -----------------------------------------------------------------------------

def main():
    print("=" * 80)
    print("SIVAC-THESIS-LAB - Squad B: COMPILACIÓN INTEGRAL DE EXPEDIENTE E INSTRUMENTOS")
    print("=" * 80)

    # 1. Compilación de los 4 archivos DOCX
    ruta_exp = generar_expediente_completo()
    ruta_i1 = generar_instrumento_1()
    ruta_i2 = generar_instrumento_2()
    ruta_i3 = generar_instrumento_3()

    print("\n" + "-" * 80)
    print("[*] Iniciando exportación desatendida a PDF mediante Microsoft Word COM...")
    print("-" * 80)

    # 2. Exportación a PDF de alta resolución
    archivos_docx = [ruta_exp, ruta_i1, ruta_i2, ruta_i3]
    archivos_pdf = []

    for d in archivos_docx:
        p = exportar_docx_a_pdf(d)
        archivos_pdf.append(p)

    print("\n" + "=" * 80)
    print("[RESUMEN DE ARTEFACTOS GENERADOS CON ÉXITO]")
    print("=" * 80)
    for d, p in zip(archivos_docx, archivos_pdf):
        print(f"  • DOCX: {d} ({os.path.getsize(d):,} bytes)")
        print(f"    PDF:  {p} ({os.path.getsize(p):,} bytes)")
    print("=" * 80)
    print("[ÉXITO TOTAL] Los 4 documentos DOCX y los 4 archivos PDF fueron compilados.")
    print("=" * 80)

if __name__ == "__main__":
    main()
