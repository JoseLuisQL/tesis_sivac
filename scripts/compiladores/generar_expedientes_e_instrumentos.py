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
# PADRÓN DE EXPERTOS EVALUADORES
#
# Vaciado por mandato de DEC-014 y DEC-016. Este padrón atribuía nombres, DNI y
# CIP a tres jueces que no evaluaron los instrumentos, y los formatos de
# validación vigentes deben entregarse íntegramente en blanco, sin identidad de
# evaluador ni número de colegiatura. La constante se conserva como lista vacía
# para no romper la cadena de importación del módulo.
# -----------------------------------------------------------------------------
EXPERTOS = []

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
    # ---------------------------------------------------------------------
    # BLOQUEADO POR DEC-014 (2026-10-18)
    #
    # Este expediente contenia constancias, dictamenes y coeficientes (V de
    # Aiken, IVC, intervalos de confianza) atribuidos a tres jueces que no
    # evaluaron los instrumentos. La Regla Canonica 01, seccion 3, prohibe
    # inventar o simular datos empiricos, y la demostracion aritmetica de
    # DEC-014 prueba que V = 0.987 es inalcanzable con 32 items x 3 jueces x
    # 4 categorias.
    #
    # El material se conserva en cuarentena en:
    #   salidas/archivo/_material_apocrifo_no_usar/
    #
    # Los formatos vigentes son los certificados en blanco del modelo Fany
    # 2024 generados por generar_anexo2_validacion_fany.py.
    #
    # Para reactivar esta funcion seria necesario un nuevo pronunciamiento del
    # tesista y de la asesora que sustituya a DEC-014.
    # ---------------------------------------------------------------------
    raise RuntimeError(
        "Generacion bloqueada por DEC-014: el expediente de validacion contenia "
        "coeficientes psicometricos y constancias atribuidas a jueces que no "
        "evaluaron los instrumentos, sin respaldo empirico. DEC-016 exige ademas "
        "que los formatos de validacion se entreguen integramente en blanco, sin "
        "nombres, DNI, CIP, sellos ni veredictos. Usar "
        "scripts/compiladores/generar_anexo2_validacion_fany.py en su lugar."
    )


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
        ("Momento de Medición:", "[  ] PRETEST (O1: Kardex manual físico, libros de registro y hojas Excel dispersas)\n[  ] POSTEST (O2: Sistema web SIVAC y su base de datos relacional)"),
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
        ("PROMEDIO", "TIEMPO PROMEDIO DE REGISTRO (T_reg) POR OPERADOR", "-", "-", "-", "________"),
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
        ("Momento de Auditoría:", "[  ] PRETEST (O1: Kardex físico, cuadernos manuales y actas manuscritas)\n[  ] POSTEST (O2: Registros en la base de datos relacional del sistema SIVAC y vales electrónicos PDF)"),
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
    agregar_p(doc, "Fórmulas oficiales: RSD (%) = (Registros Conformes / Total Auditados) * 100  |  CPE (%) = (Entregas Concordantes / Total de Entregas Evaluadas) * 100", cursiva=True, tamano_pt=9.0)

    t_aud = doc.add_table(rows=7, cols=7)
    aplicar_bordes_cuadricula(t_aud)
    formatear_celdas_tabla(t_aud, [1.2, 3.2, 2.3, 2.3, 2.4, 2.1, 2.0])

    h_aud = ["N°", "N° Vale / PECOSA", "Cant. Prog.", "Cant. Entr.", "Concordancia (1/0)", "8 Criterios", "RSD (1/0)"]
    for c_i, h in enumerate(h_aud):
        c = t_aud.cell(0, c_i)
        colorear_celda(c, COLOR_AZUL_UNAJMA)
        set_texto_celda(c, h, negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=RGBColor(0xFF, 0xFF, 0xFF))

    for r_i in range(1, 6):
        set_texto_celda(t_aud.cell(r_i, 0), str(r_i), tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_i, 1), f"VALE-2025-00{r_i}", tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_i, 2), "_____ dosis", tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_i, 3), "_____ dosis", tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_i, 4), "[  ] 1   [  ] 0", tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_i, 5), "[  ] Conforme", tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        set_texto_celda(t_aud.cell(r_i, 6), "[  ]", tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)

    # Fila de totales
    set_texto_celda(t_aud.cell(6, 0), "RESUMEN", negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    set_texto_celda(t_aud.cell(6, 1), "TOTALES AUDITADOS", negrita=True, tamano_pt=8.0)
    set_texto_celda(t_aud.cell(6, 2), "N_prog = ___", negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    set_texto_celda(t_aud.cell(6, 3), "N_entr = ___", negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    set_texto_celda(t_aud.cell(6, 4), "N_conc = ___\nCPE = ___%", negrita=True, tamano_pt=8.0, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
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

    # 1. Compilación de los instrumentos DOCX
    # El expediente de validacion queda excluido por DEC-014; los tres
    # instrumentos de recoleccion de datos no estan afectados y se generan.
    try:
        ruta_exp = generar_expediente_completo()
    except RuntimeError as exc:
        print(f"[BLOQUEADO por DEC-014] {exc}")
        ruta_exp = None

    ruta_i1 = generar_instrumento_1()
    ruta_i2 = generar_instrumento_2()
    ruta_i3 = generar_instrumento_3()

    print("\n" + "-" * 80)
    print("[*] Iniciando exportación desatendida a PDF mediante Microsoft Word COM...")
    print("-" * 80)

    # 2. Exportación a PDF de alta resolución
    archivos_docx = [d for d in (ruta_exp, ruta_i1, ruta_i2, ruta_i3) if d]
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
    print(f"[RESUMEN] Documentos DOCX generados: {len(archivos_docx)}  |  Archivos PDF exportados: {len(archivos_pdf)}")
    if ruta_exp is None:
        print("[BLOQUEADO por DEC-014] El expediente de validación por juicio de expertos no se generó. "
              "El certificado vigente se produce con scripts/compiladores/generar_anexo2_validacion_fany.py.")
    print("=" * 80)

if __name__ == "__main__":
    main()
