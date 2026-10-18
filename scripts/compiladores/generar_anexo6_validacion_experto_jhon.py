#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - ANEXO 6 ESPEJO JHON 2026 (p.177) - NEUTRALIZADO 2026-10-18
================================================================================
El espejo Jhon 2026 quedó superado como modelo de validación por DEC-015, que
adopta el Anexo 2 de Fany 2024 (páginas 62 a 65) como formato oficial de
validación por juicio de expertos. Los tres formatos que este generador produjo
se conservan en salidas/documentos/anexos_jhon/ y NO deben imprimirse ni
entregarse a ningún juez.

Su ejecución ya no es válida por cinco motivos:

1. DEC-015 sustituyó el espejo Jhon 2026 por el modelo Fany 2024.
2. El documento imprimía una fecha fija ("19 de octubre de 2026") y texto en
   fuente manuscrita simulada (Segoe Script, tinta azul oscuro #1A3A8A),
   ambos prohibidos por DEC-016.
3. La matriz única de 1 a 5 no es ninguna de las estructuras adoptadas: no es la
   tabla dicotómica de Fany 2024 (Pertinencia / Relevancia / Claridad) ni la
   escala Likert del Instrumento 03, y mezcla las tres dimensiones DEC-007 en
   una sola hoja sin correspondencia con los tres instrumentos oficiales.
4. El modo por omisión generaba los documentos MARCADO_A_MANO, es decir, con
   marcas X y rúbrica prellenadas, contrarias a DEC-014 y DEC-016.
5. La opción --retiro-condor invocaba por subproceso a
   archivar_condor_dejar_solo_jhon.py, que hoy aborta con SystemExit; el
   resultado sería una llamada muerta dentro de un script que seguiría
   produciendo material derogado.

El cuerpo original se conserva abajo, sin efecto, solo como registro histórico.
"""

raise SystemExit(
    "Script neutralizado. Modelo vigente: Fany 2024, Anexo 2 (DEC-015). "
    "Generador vigente: scripts/compiladores/generar_anexo2_validacion_fany.py -> "
    "salidas/documentos/anexos_fany/_archivo_obsoleto/ (bloqueado, ver "
    "LEEME_CERTIFICADOS_RETIRADOS.md). Los tres DOCX de "
    "salidas/documentos/anexos_jhon/ estan derogados: no imprimir ni entregar."
)


# ---------------------------------------------------------------------------
# CUERPO ORIGINAL (2026-10-17), CONSERVADO SIN EFECTO COMO REGISTRO HISTORICO.
# Todo lo que sigue es inalcanzable: el raise SystemExit de arriba lo impide.
# ---------------------------------------------------------------------------
import os
import sys
from pathlib import Path
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

RUTA_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RUTA_SALIDA = os.path.join(RUTA_BASE, "salidas", "documentos", "anexos_jhon")

TITULO_TESIS = "APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II"
TESISTA = "Bach. José Luis Quispe León"
FECHA_DOC = "19 de octubre de 2026"

FUENTE = "Times New Roman"
FUENTE_MANUS = "Segoe Script"
COLOR_MANUS = "1A3A8A"
COLOR_AZUL_JHON = "1F3864"
COLOR_AZUL_CLARO = "2E75B6"

# 3 jueces espejo - cada uno 1 hoja (como Jhon Anexo 6)
JUECES_JHON = [
    {"n": 1, "apellidos": "MENDOZA QUISPE CARLOS ALBERTO", "grado": "MAGISTER", "profesion": "INGENIERO DE SISTEMAS", "corto": "M.Sc. Carlos Alberto Mendoza Quispe", "dni": "41234567", "cip": "CIP N.° 228451"},
    {"n": 2, "apellidos": "PALOMINO HUAMÁN RUTH ELENA", "grado": "MAGISTER", "profesion": "INGENIERA DE SISTEMAS", "corto": "M.Sc. Ruth Elena Palomino Huamán", "dni": "43876512", "cip": "CIP N.° 231874"},
    {"n": 3, "apellidos": "FERNÁNDEZ TORRES JORGE LUIS", "grado": "MAGISTER", "profesion": "INGENIERO DE SISTEMAS", "corto": "M.Sc. Jorge Luis Fernández Torres", "dni": "40567890", "cip": "CIP N.° 219063"},
]

# Matriz única espejo Jhon p.177 - 3 dimensiones DEC-007, 12 preguntas profesionales
# Sin códigos abreviados visibles, sin guion largo U+2014, ordenada normativamente 4+4+4
# Cada fila: (dimension, indicador_etiqueta, pregunta_profesional)
MATRIZ_VALIDACION = [
    # D1 - OPORTUNIDAD DE PROCESAMIENTO (4 preguntas)
    ("OPORTUNIDAD", "Tiempo de registro", "El instrumento permite medir con precisión el tiempo que el personal emplea en registrar un movimiento de vacuna en el kardex.", True),
    ("OPORTUNIDAD", "Tiempo de registro", "Los momentos de inicio y fin para la medición del tiempo de registro están definidos con claridad y sin ambigüedad.", True),
    ("OPORTUNIDAD", "Tiempo de emisión de vale", "El instrumento permite medir con precisión el tiempo que el personal emplea en emitir el comprobante de salida o vale.", True),
    ("OPORTUNIDAD", "Oportunidad global", "El conjunto de tareas propuesto representa fielmente las situaciones reales de registro y emisión de vales en la DISA Apurímac II.", True),
    # D2 - CONSISTENCIA DOCUMENTAL (4 preguntas)
    ("CONSISTENCIA", "Registros sin discrepancias", "El instrumento verifica con exhaustividad la ausencia de discrepancias entre el registro físico y el registro digital.", True),
    ("CONSISTENCIA", "Registros sin discrepancias", "La regla de verificación basada en ocho criterios simultáneos es clara, completa y aplicable en campo.", True),
    ("CONSISTENCIA", "Concordancia programada y entregada", "El instrumento permite contrastar con exactitud la cantidad programada frente a la cantidad efectivamente entregada.", True),
    ("CONSISTENCIA", "Trazabilidad documental", "El instrumento garantiza la trazabilidad entre el comprobante físico, la guía de remisión y la base de datos.", True),
    # D3 - SATISFACCIÓN DEL USUARIO (4 preguntas)
    ("SATISFACCIÓN", "Aceptación del proceso", "Los enunciados referidos a la aceptación del proceso son claros, comprensibles y pertinentes para el personal de inmunizaciones.", True),
    ("SATISFACCIÓN", "Aceptación del proceso", "Los enunciados permiten valorar si el flujo de trabajo reduce el esfuerzo y la incertidumbre del personal.", True),
    ("SATISFACCIÓN", "Utilidad percibida", "Los enunciados referidos a la utilidad percibida reflejan con fidelidad la utilidad real para la gestión de vacunas.", True),
    ("SATISFACCIÓN", "Satisfacción global", "El cuestionario en su conjunto permite valorar la satisfacción global del usuario con el proceso, con escala y baremo adecuados.", True),
]

def configurar_margenes(seccion):
    seccion.page_width = Cm(21.0)
    seccion.page_height = Cm(29.7)
    seccion.left_margin = Cm(3.0)
    seccion.right_margin = Cm(2.5)
    seccion.top_margin = Cm(2.5)
    seccion.bottom_margin = Cm(2.0)
    seccion.header_distance = Cm(1.27)
    seccion.footer_distance = Cm(1.27)

def blindar_tabla(table):
    for idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        if trPr.find(qn('w:cantSplit')) is None:
            trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
        if idx == 0 and trPr.find(qn('w:tblHeader')) is None:
            trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))

def aplicar_bordes_grid(table, color="808080", sz="4"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._tbl.tblPr
    for el in tblPr.findall(qn('w:tblpPr')):
        tblPr.remove(el)
    for el in tblPr.findall(qn('w:tblBorders')):
        tblPr.remove(el)
    xml = r'''<w:tblBorders %s>
        <w:top w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
        <w:left w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
        <w:bottom w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
        <w:right w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
        <w:insideH w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
        <w:insideV w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
    </w:tblBorders>''' % (nsdecls('w'), sz, color, sz, color, sz, color, sz, color, sz, color, sz, color)
    tblPr.append(parse_xml(xml))

def colorear_celda(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    for shd in tcPr.findall(qn('w:shd')):
        tcPr.remove(shd)
    tcPr.append(parse_xml(r'<w:shd %s w:fill="%s"/>' % (nsdecls('w'), hex_color)))

def set_texto_celda(cell, texto, negrita=False, cursiva=False, tamano=8.5, color=None, alineacion=None, fuente=None):
    p = cell.paragraphs[0]
    p.text = ""
    p.paragraph_format.space_before = Pt(1.5)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.line_spacing = 1.0
    if alineacion is not None:
        p.alignment = alineacion
    r = p.add_run(str(texto))
    r.font.name = fuente if fuente else FUENTE
    r.font.size = Pt(tamano)
    r.font.bold = negrita
    r.font.italic = cursiva
    if color:
        r.font.color.rgb = color
    return p

def set_celda_manuscrita(cell, texto, tamano=9.5):
    p = cell.paragraphs[0]
    p.text = ""
    p.paragraph_format.space_before = Pt(1.5)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.line_spacing = 1.0
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(str(texto))
    r.font.name = FUENTE_MANUS
    r.font.size = Pt(tamano)
    r.font.italic = True
    r.font.color.rgb = RGBColor(0x1A, 0x3A, 0x8A)
    # Forzar color y fuente via XML
    rPr = r._r.get_or_add_rPr()
    c = rPr.find(qn('w:color'))
    if c is None:
        c = OxmlElement('w:color'); rPr.append(c)
    c.set(qn('w:val'), COLOR_MANUS)
    rf = rPr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rPr.append(rf)
    rf.set(qn('w:ascii'), FUENTE_MANUS)
    rf.set(qn('w:hAnsi'), FUENTE_MANUS)
    rf.set(qn('w:cs'), FUENTE_MANUS)
    return p

def agregar_p(doc, texto="", negrita=False, cursiva=False, tamano=10, alineacion=WD_ALIGN_PARAGRAPH.JUSTIFY, color=None, espacio_antes=0, espacio_desp=2, sangria=0, fuente=None):
    p = doc.add_paragraph()
    p.alignment = alineacion
    p.paragraph_format.space_before = Pt(espacio_antes)
    p.paragraph_format.space_after = Pt(espacio_desp)
    p.paragraph_format.line_spacing = 1.5
    if sangria > 0:
        p.paragraph_format.first_line_indent = Cm(sangria)
    if texto:
        r = p.add_run(texto)
        r.font.name = fuente if fuente else FUENTE
        r.font.size = Pt(tamano)
        r.font.bold = negrita
        r.font.italic = cursiva
        if color:
            r.font.color.rgb = color
    return p

def generar_un_experto(juez, modo_vacio=False):
    os.makedirs(RUTA_SALIDA, exist_ok=True)
    sufijo = "VACIO" if modo_vacio else "MARCADO_A_MANO"
    nombre_archivo = f"ANEXO_6_VALIDACION_EXPERTO_{juez['n']}_JHON_ESPEJO_{sufijo}.docx"
    ruta = os.path.join(RUTA_SALIDA, nombre_archivo)
    modo_txt = "VACÍO (para entrega a juez)" if modo_vacio else "MARCADO"
    print(f"[*] Generando {nombre_archivo} - {juez['corto']} [{modo_txt}]")

    doc = docx.Document()
    configurar_margenes(doc.sections[0])

    # Footer con numeración
    sec = doc.sections[0]
    pf = sec.footer.paragraphs[0]
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = pf.add_run()
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), 'PAGE')
    pf._p.append(fld)
    pf.paragraph_format.space_before = Pt(0)
    pf.paragraph_format.space_after = Pt(0)

    # --- Título Anexo ---
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(f"Anexo 6: Validación de instrumentos por el experto {juez['n']}")
    r.font.name = FUENTE
    r.font.size = Pt(9)
    r.font.italic = True
    r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("VALIDEZ DE INSTRUMENTOS DE INVESTIGACIÓN")
    r.font.name = FUENTE
    r.font.size = Pt(11)
    r.bold = True

    # Respetado juez
    agregar_p(doc, f"Respetado juez:", tamano=9, espacio_desp=2)
    agregar_p(doc, f"Usted ha sido seleccionado para evaluar el instrumento de recolección de información, que es parte de la investigación titulada “{TITULO_TESIS}”. Su colaboración es fundamental para asegurar la validez del instrumento y la utilidad de los resultados. Agradece su valiosa colaboración:", tamano=9, espacio_desp=4, sangria=0)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(f"Bach. {TESISTA.replace('Bach. ', '')}")
    r.font.name = FUENTE
    r.font.size = Pt(9)
    r.italic = True

    # I. DATOS GENERALES - modo_vacio: líneas punteadas; modo marcado: tinta manuscrita
    agregar_p(doc, "I. DATOS GENERALES", negrita=True, tamano=10, espacio_antes=4, espacio_desp=4)

    t_datos = doc.add_table(rows=4, cols=2)
    aplicar_bordes_grid(t_datos, sz="6")
    blindar_tabla(t_datos)
    # Anchos
    for row in t_datos.rows:
        row.cells[0].width = Cm(6.5)
        row.cells[1].width = Cm(9.0)
    # Header
    set_texto_celda(t_datos.cell(0, 0), "APELLIDOS Y NOMBRES DEL EXPERTO", negrita=True, tamano=8.5, color=RGBColor(0xFF,0xFF,0xFF), alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    colorear_celda(t_datos.cell(0, 0), COLOR_AZUL_JHON)
    if modo_vacio:
        set_texto_celda(t_datos.cell(0, 1), "................................................................................", tamano=8, color=RGBColor(0xBF,0xBF,0xBF), alineacion=WD_ALIGN_PARAGRAPH.LEFT)
    else:
        set_celda_manuscrita(t_datos.cell(0, 1), juez["apellidos"], tamano=9)
    colorear_celda(t_datos.cell(0, 1), "FFFFFF")
    # Ajustar: primera fila es header con valor, no header tradicional - en Jhon la primera fila ya es dato
    # Rehacer: tabla Jhon tiene 3 filas con etiqueta azul a la izquierda y valor manuscrito a la derecha
    # Ya esta bien: col0 etiqueta azul, col1 valor manuscrito
    # Pero cel(0,0) debe ser etiqueta, cel(0,1) valor - recolorear
    # celda 0,0 ya azul, 0,1 blanco manuscrito

    # Fila 2: GRADO
    set_texto_celda(t_datos.cell(1, 0), "GRADO ACADÉMICO", negrita=True, tamano=8.5, color=RGBColor(0xFF,0xFF,0xFF), alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    colorear_celda(t_datos.cell(1, 0), COLOR_AZUL_JHON)
    if modo_vacio:
        set_texto_celda(t_datos.cell(1, 1), "................................................................................", tamano=8, color=RGBColor(0xBF,0xBF,0xBF))
    else:
        set_celda_manuscrita(t_datos.cell(1, 1), juez["grado"], tamano=9)

    # Fila 3: PROFESION
    set_texto_celda(t_datos.cell(2, 0), "PROFESIÓN", negrita=True, tamano=8.5, color=RGBColor(0xFF,0xFF,0xFF), alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    colorear_celda(t_datos.cell(2, 0), COLOR_AZUL_JHON)
    if modo_vacio:
        set_texto_celda(t_datos.cell(2, 1), "................................................................................", tamano=8, color=RGBColor(0xBF,0xBF,0xBF))
    else:
        set_celda_manuscrita(t_datos.cell(2, 1), juez["profesion"], tamano=9)

    # Fila 4: CIP/DNI (adicional SIVAC)
    set_texto_celda(t_datos.cell(3, 0), "DNI / CIP", negrita=True, tamano=8.5, color=RGBColor(0xFF,0xFF,0xFF), alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    colorear_celda(t_datos.cell(3, 0), COLOR_AZUL_JHON)
    if modo_vacio:
        set_texto_celda(t_datos.cell(3, 1), "................................................................................", tamano=8, color=RGBColor(0xBF,0xBF,0xBF))
    else:
        set_celda_manuscrita(t_datos.cell(3, 1), f"DNI {juez['dni']}  -  {juez['cip']}", tamano=9)

    # II. ASPECTOS DE VALIDACIÓN
    agregar_p(doc, "II. ASPECTOS DE VALIDACIÓN", negrita=True, tamano=10, espacio_antes=8, espacio_desp=2)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.left_indent = Cm(0.6)
    r = p.add_run("Instrucciones:")
    r.font.name = FUENTE; r.font.size = Pt(9); r.bold = True; r.italic = True

    bullets = [
        "Dimensión Oportunidad: Las respuestas deben consignarse en valores numéricos (minutos decimales, precisión 0.01).",
        "Dimensión Consistencia: Las respuestas corresponden a auditoría dicotómica (1 es Conforme, 0 es Discrepancia) y porcentajes de registros sin discrepancias y concordancia.",
        "Dimensión Satisfacción: Las respuestas posibles son: Nada satisfecho, Poco satisfecho, Neutral, Muy satisfecho, Totalmente satisfecho (Likert 1 a 5).",
        "Marque con una X cada ítem según la valoración correspondiente que le otorgue.",
    ]
    for b in bullets:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Cm(0.8)
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(b)
        r.font.name = FUENTE; r.font.size = Pt(8.5)

    # Escala
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("ESCALA:  MALO (1)  -  REGULAR (2)  -  BUENO (3)  -  EXCELENTE (4)  -  SOBRESALIENTE (5)")
    r.font.name = FUENTE; r.font.size = Pt(8.5); r.bold = True

    # TABLA MATRIZ ÚNICA 8 columnas
    n_filas = len(MATRIZ_VALIDACION) + 1
    t_matriz = doc.add_table(rows=n_filas, cols=8)
    aplicar_bordes_grid(t_matriz, sz="4")
    blindar_tabla(t_matriz)
    # Anchos: Dim 2.0, Indicador 3.2, Pregunta 6.0, 1-5 cada 0.85
    anchos = [Cm(2.0), Cm(3.2), Cm(6.0), Cm(0.85), Cm(0.85), Cm(0.85), Cm(0.85), Cm(0.85)]
    for row in t_matriz.rows:
        for idx, cell in enumerate(row.cells):
            cell.width = anchos[idx]

    # Header fila 0
    headers = ["Dimensiones", "Indicadores", "Preguntas\nVariable: Gestión de movimientos de vacunas (VD)", "1", "2", "3", "4", "5"]
    # Segunda línea del header de preguntas
    for c_idx, h in enumerate(headers):
        cell = t_matriz.cell(0, c_idx)
        colorear_celda(cell, COLOR_AZUL_JHON)
        # Para columna preguntas, texto con salto
        if c_idx == 2:
            p = cell.paragraphs[0]
            p.text = ""
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            r1 = p.add_run("Variable: Gestión de movimientos de vacunas")
            r1.font.name = FUENTE; r1.font.size = Pt(6.5); r1.bold = True; r1.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
            r1.font.italic = True
            # segunda linea ya en header
        else:
            aline = WD_ALIGN_PARAGRAPH.CENTER
            set_texto_celda(cell, h, negrita=True, tamano=7.5 if c_idx < 3 else 8, color=RGBColor(0xFF,0xFF,0xFF), alineacion=aline)
        # Ajustar pregunta header manualmente
    # Reescribir header de preguntas correctamente
    cell_preg = t_matriz.cell(0, 2)
    p = cell_preg.paragraphs[0]
    p.text = ""
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run("Variable: Gestión de movimientos\nde certificados y validación de\ncertificados de capacitación")
    # Para SIVAC, corregir a VD real
    p.text = ""
    r = p.add_run("Variable: Gestión de movimientos de vacunas\n(DISA Apurímac II - DEC-007)")
    r.font.name = FUENTE; r.font.size = Pt(6.5); r.bold = True; r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
    r.font.italic = False
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Corregir header 0,0 y 0,1 y 0,3-7 que fueron sobrescritos
    set_texto_celda(t_matriz.cell(0, 0), "Dimensiones", negrita=True, tamano=7.5, color=RGBColor(0xFF,0xFF,0xFF), alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    colorear_celda(t_matriz.cell(0, 0), COLOR_AZUL_JHON)
    set_texto_celda(t_matriz.cell(0, 1), "Indicadores", negrita=True, tamano=7.5, color=RGBColor(0xFF,0xFF,0xFF), alineacion=WD_ALIGN_PARAGRAPH.CENTER)
    colorear_celda(t_matriz.cell(0, 1), COLOR_AZUL_JHON)
    for ci in range(3, 8):
        set_texto_celda(t_matriz.cell(0, ci), str(ci-2), negrita=True, tamano=8, color=RGBColor(0xFF,0xFF,0xFF), alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        colorear_celda(t_matriz.cell(0, ci), COLOR_AZUL_JHON)
    # Valoración label arriba de 1-5
    # Agregar fila extra de Valoración no, Jhon tiene "Valoración" spanning 5 cols - simplificamos con header ya puesto

    # Filas de datos
    # Agrupar por dimension para merge vertical
    from collections import defaultdict
    dim_rows = defaultdict(list)
    for idx, fila in enumerate(MATRIZ_VALIDACION, start=1):
        dim_rows[fila[0]].append(idx)

    for r_idx, fila in enumerate(MATRIZ_VALIDACION, start=1):
        dim, indicador, pregunta, marcar5 = fila
        # Col 0 Dimensión - solo en primera fila de cada dimensión, resto fusionada visualmente (texto solo en primera)
        cell_dim = t_matriz.cell(r_idx, 0)
        # Determinar si es primera fila de la dimensión
        first_of_dim = dim_rows[dim][0] == r_idx
        if first_of_dim:
            # Nombre corto
            nombre_dim = {"OPORTUNIDAD": "OPORTUNIDAD", "CONSISTENCIA": "CONSISTENCIA", "SATISFACCIÓN": "SATISFACCIÓN"}[dim]
            set_texto_celda(cell_dim, nombre_dim, negrita=True, tamano=7, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
            # vertical merge simulado: colorear resto igual pero vacío se verá como bloque
        else:
            set_texto_celda(cell_dim, "", tamano=7)
        # Col 1 Indicador
        set_texto_celda(t_matriz.cell(r_idx, 1), indicador, tamano=6.5, alineacion=WD_ALIGN_PARAGRAPH.LEFT)
        # Col 2 Pregunta
        set_texto_celda(t_matriz.cell(r_idx, 2), pregunta, tamano=7, alineacion=WD_ALIGN_PARAGRAPH.LEFT)
        # Col 3-7 valoraciones - en modo_vacio quedan en blanco para marcar X a mano
        for c in range(3, 8):
            cell = t_matriz.cell(r_idx, c)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cell.paragraphs[0].paragraph_format.space_before = Pt(1)
            cell.paragraphs[0].paragraph_format.space_after = Pt(1)
            # fix: paragraph_format está en paragraph, no en cell
            if modo_vacio:
                p = cell.paragraphs[0]
                p.text = ""
                continue
            val = 5  # todas en SOBRESALIENTE como Jhon
            marca = "X" if c == 7 else ""  # col 7 = 5
            # Crear run manuscrito si X
            p = cell.paragraphs[0]
            p.text = ""
            if marca == "X":
                r = p.add_run("X")
                r.font.name = FUENTE_MANUS
                r.font.size = Pt(11)
                r.bold = True
                r.italic = True
                r.font.color.rgb = RGBColor(0x1A, 0x3A, 0x8A)
                rPr = r._r.get_or_add_rPr()
                col = rPr.find(qn('w:color'))
                if col is None:
                    col = OxmlElement('w:color'); rPr.append(col)
                col.set(qn('w:val'), COLOR_MANUS)
            else:
                r = p.add_run("")
                r.font.size = Pt(8)

    # Fusion real vertical para Dimensiones (opcional visual)
    # Aplicar merge via python-docx merge
    for dim, rows_list in dim_rows.items():
        if len(rows_list) > 1:
            start = rows_list[0]
            end = rows_list[-1]
            # merge cells vertically
            try:
                cell_start = t_matriz.cell(start, 0)
                cell_end = t_matriz.cell(end, 0)
                # python-docx merge via _tc
                cell_start.merge(cell_end)
                # re-centrar vertical
                cell_start.vertical_alignment = docx.enum.table.WD_ALIGN_VERTICAL.CENTER
            except Exception:
                pass

    # III. OBSERVACIONES - modo_vacio: solo líneas punteadas
    agregar_p(doc, "III. OBSERVACIONES", negrita=True, tamano=10, espacio_antes=8, espacio_desp=2)
    # Líneas punteadas
    for i in range(3):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        pf = p.paragraph_format
        pf.left_indent = Cm(0.5)
        if i == 0 and not modo_vacio:
            r = p.add_run("Aplicable sin observaciones. Instrumento con excelente validez de contenido - se recomienda su aplicación inmediata en campo (pretest O1 y postest O2).")
            r.font.name = FUENTE_MANUS; r.font.size = Pt(9); r.italic = True; r.font.color.rgb = RGBColor(0x1A,0x3A,0x8A)
        else:
            r = p.add_run("_________________________________________________________________________________")
            r.font.name = FUENTE; r.font.size = Pt(8); r.font.color.rgb = RGBColor(0xBF,0xBF,0xBF)

    # Fecha
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(f"Andahuaylas, {FECHA_DOC}")
    r.font.name = FUENTE; r.font.size = Pt(9)
    # Fecha manuscrita simulada
    # Agregar subrayado manuscrito para día
    # Mantener simple

    # FIRMA + Sello - modo_vacio: solo línea + rótulo FIRMA (juez firma a mano)
    # Espacio para firma manuscrita
    p_firma_manus = doc.add_paragraph()
    p_firma_manus.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_firma_manus.paragraph_format.space_before = Pt(10)
    p_firma_manus.paragraph_format.space_after = Pt(0)
    if not modo_vacio:
        r = p_firma_manus.add_run(juez["corto"].replace("M.Sc. ", ""))
        r.font.name = FUENTE_MANUS; r.font.size = Pt(14); r.italic = True; r.font.color.rgb = RGBColor(0x1A,0x3A,0x8A)
        r.bold = True
    else:
        # vacío: espacio en blanco para firma manuscrita real
        r = p_firma_manus.add_run("")
        r.font.size = Pt(14)

    p_linea = doc.add_paragraph()
    p_linea.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_linea.paragraph_format.space_before = Pt(0)
    p_linea.paragraph_format.space_after = Pt(1)
    r = p_linea.add_run("________________________________________")
    r.font.name = FUENTE; r.font.size = Pt(10)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run("FIRMA")
    r.font.name = FUENTE; r.font.size = Pt(8); r.bold = True

    if not modo_vacio:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(f"[Sello: {juez['cip']} - {juez['profesion']} - UNAJMA]")
        r.font.name = FUENTE; r.font.size = Pt(7); r.font.color.rgb = RGBColor(0x1A,0x3A,0x8A); r.bold = True
        # Nota SIMULADO ética - solo en modo marcado
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run("- DOCUMENTO SIMULADO CON FINES DEMOSTRATIVOS - Requiere firma autógrafa y sello del juez para validez oficial -")
        r.font.name = FUENTE; r.font.size = Pt(7); r.bold = True; r.italic = True; r.font.color.rgb = RGBColor(0xC0,0x00,0x00)

    # Número de página centrado (como 177 en Jhon)
    # Ya en footer, pero agregar también centrado arriba del footer
    doc.save(ruta)
    print(f"  [OK] {ruta} ({os.path.getsize(ruta):,} bytes)")
    return ruta

def main():
    global RUTA_SALIDA
    import argparse
    parser = argparse.ArgumentParser(description="Anexo 6 Jhon espejo - 3 expertos")
    parser.add_argument("--salida", default=RUTA_SALIDA)
    parser.add_argument("--vacio", action="store_true", help="Genera 3 VACÍOS sin X ni tinta manuscrita (para entrega real a jueces)")
    parser.add_argument("--retiro-condor", action="store_true", help="Mueve 9 formatos Dr. Cóndor a _archivo_condor_no_usar/")
    args = parser.parse_args()
    RUTA_SALIDA = args.salida
    print("="*72)
    if args.vacio:
        print("SIVAC - ANEXO 6 JHON ESPEJO - MODO VACÍO (para entrega real a jueces)")
    else:
        print("SIVAC - ANEXO 6 JHON ESPEJO (p.177) - 3 EXPERTOS, 1 HOJA C/U")
    print("="*72)
    for juez in JUECES_JHON:
        generar_un_experto(juez, modo_vacio=args.vacio)
    if args.retiro_condor:
        import subprocess
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "archivar_condor_dejar_solo_jhon.py")], check=False)
    print("="*72)
    total = len([f for f in os.listdir(RUTA_SALIDA) if f.endswith(".docx")])
    print(f"[RESUMEN] {total} DOCX en {RUTA_SALIDA}")
    print("="*72)

if __name__ == "__main__":
    main()
