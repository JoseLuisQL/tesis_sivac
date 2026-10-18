#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - ANEXO 2. INSTRUMENTO DE VALIDACION (MODELO FANY 2024)
================================================================================

################################################################################
#  ESTADO DEL GENERADOR - 2026-10-18
#
#  ALINEADO A DEC-019 Y DEC-020. Este generador emite UN UNICO modelo de
#  certificado de validez de contenido: el del Instrumento N.° 03, Modalidad A,
#  con los ocho reactivos AP-01 a AP-04 y UP-01 a UP-04 transcritos
#  literalmente del instrumento oficial, sin parafrasis.
#
#  DEC-019: la Modalidad A es la via oficial de contrastacion de la Hipotesis
#  Especifica 3, aplicable en pretest y postest. Comprende cuatro reactivos de
#  Aceptacion del proceso operativo (I3.1) y cuatro de Utilidad percibida
#  (I3.2), con baremo global de 8 a 40 y de subescala de 4 a 20. La Modalidad B
#  (PU-01 a PU-04 y PE-01 a PE-04) es un modulo anexo de postest, no baremado,
#  no aditivo y sin certificado propio.
#
#  DEC-020: los Instrumentos 01 y 02 no se someten a juicio de contenido. Su
#  validez se sustenta en el protocolo PMMV, en el coeficiente de correlacion
#  intraclase ICC(2,1) mayor o igual a 0.75 de la ficha cronometrica y en el
#  kappa de Cohen mayor o igual a 0.80 de la ficha de cotejo documental.
#
#  El formato vigente es el de DEC-015: criterios dicotomicos Si/No de
#  Pertinencia, Relevancia y Claridad. No se reporta ningun coeficiente como
#  resultado (DEC-014).
#
#  EJECUCION SEGURA: sin argumentos el generador NO escribe ningun archivo.
#  Solo el argumento explicito --generar produce el DOCX. El argumento
#  --verificar audita la estructura en memoria sin guardar nada.
################################################################################

Genera el certificado de validez de contenido en BLANCO para impresion y
llenado manuscrito por los jueces expertos de la EPIS-UNAJMA.

Modelo de referencia verificado contra el PDF escaneado:
  referencias/modelos_tesis/Fany_Tesis_Bachiller_2024.pdf (1).pdf
  Anexo 2. Instrumento de validacion, paginas impresas 62 a 65.

Estructura replicada del modelo:
  1. Titulo de seccion "Anexo 2. Instrumento de validacion".
  2. Rotulo "CERTIFICADO DE VALIDEZ DE CONTENIDO DEL INSTRUMENTO ...".
  3. Encabezado de dos filas: N | DIMENSIONES / items | Pertinencia(1) |
     Relevancia(2) | Claridad(3) | Sugerencias, con Si/No en la segunda fila.
  4. Dos filas de dimension con los rotulos I3.1 e I3.2 y la repeticion
     Si/No en las columnas de criterio.
  5. Ocho filas de item con el enunciado literal y seis celdas vacias.
  6. Bloque inferior: observaciones, opinion de aplicabilidad, identidad del
     juez en puntos suspensivos, especialidad, lugar y fecha, firma.
  7. Notas al pie de la hoja con los tres criterios y la nota de suficiencia.

Con las dos filas de encabezado, las dos filas de dimension y las ocho filas
de item, la tabla ocupa doce filas y el certificado cabe en una sola pagina A4.

RESTRICCIONES DE INTEGRIDAD DEL ENTREGABLE:
  - El documento sale integramente en blanco: sin nombres, DNI, CIP, marcas,
    calificaciones, sombreados, colores de relleno ni dictamenes (DEC-016).
  - La fecha se emite como linea en blanco con el ano 2026 fijo en texto.
  - Tipografia Times New Roman en todo el documento, sin fuente manuscrita.
  - Prohibido OMML dentro de celdas.

EXCEPCION DOCUMENTAL A APA 7: la tabla emplea rejilla completa en lugar de las
tres lineas horizontales, por tratarse de un formulario institucional de
captura manuscrita y no de un cuadro del cuerpo de la tesis.

Uso:
    python scripts/compiladores/generar_anexo2_validacion_fany.py --verificar
    python scripts/compiladores/generar_anexo2_validacion_fany.py --generar
================================================================================
"""

import argparse
import os
import re
import sys
from pathlib import Path

import docx
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ_PROYECTO / "scripts" / "utilidades"))

import docx_quirurgico as quirurgico  # noqa: E402

RUTA_SALIDA = RAIZ_PROYECTO / "salidas" / "documentos" / "anexos_fany"
NOMBRE_SALIDA = "ANEXO_2_VALIDACION_FANY_INST03_MODALIDAD_A_VACIO.docx"

FUENTE = "Times New Roman"
ANIO_CONSTANCIA = "2026"

# ------------------------------------------------------------------------------
# GEOMETRIA: A4 vertical con margenes de formulario (izq 2.0, der 1.5,
# sup 1.8, inf 1.5 cm). Ancho util real = 17.5 cm (9918 dxa); la tabla ocupa
# 9897 dxa para no rozar el margen derecho al imprimir.
# ------------------------------------------------------------------------------
ANCHO_UTIL_DXA = 9897
COL_WIDTHS_DXA = [
    820,   # N                        (1.45 cm)
    4200,  # DIMENSIONES / items      (7.41 cm)
    550,   # Pertinencia Si           (0.97 cm)
    550,   # Pertinencia No           (0.97 cm)
    550,   # Relevancia Si            (0.97 cm)
    550,   # Relevancia No            (0.97 cm)
    550,   # Claridad Si              (0.97 cm)
    550,   # Claridad No              (0.97 cm)
    1577,  # Sugerencias              (2.78 cm)
]  # suma = 9897 dxa = 17.46 cm, dentro del ancho util de 17.5 cm

COL_N = 0
COL_ITEM = 1
COLS_CRITERIO = (2, 3, 4, 5, 6, 7)
COL_SUGERENCIAS = 8
ETIQUETAS_CRITERIO = {2: "Si", 3: "No", 4: "Si", 5: "No", 6: "Si", 7: "No"}

TAM_TITULO = 9.5
TAM_CERTIFICADO = 9.0
TAM_REFERENCIA = 8.0
TAM_ENCABEZADO = 8.0
TAM_DIMENSION = 8.5
TAM_CODIGO = 8.5
TAM_ITEM = 9.0
TAM_BLOQUE = 9.0
TAM_NOTA = 7.5

FILAS_ESPERADAS = 12      # 2 de encabezado + 2 de dimension + 8 de item
COLUMNAS_ESPERADAS = 9

# ------------------------------------------------------------------------------
# MODELO UNICO: INSTRUMENTO N. 03, MODALIDAD A (DEC-019 Y DEC-020)
# Los ocho reactivos se transcriben literalmente de la seccion 3 del archivo
# salidas/instrumentos/INSTRUMENTO_03_CUESTIONARIO_SATISFACCION_TAM.md.
# ------------------------------------------------------------------------------
ITEMS_MODALIDAD_A = [
    (
        "I3.1 Aceptación del proceso operativo",
        [
            ("AP-01", "El procedimiento actual para asentar los movimientos diarios y cierres de mes es ágil y no demanda un esfuerzo mental o físico excesivo."),
            ("AP-02", "El flujo de trabajo requerido para emitir comprobantes de salida y vales de entrega es fluido y está libre de demoras o trabas burocráticas."),
            ("AP-03", "El método empleado me permite conciliar los saldos de inventario con las microredes generando tranquilidad y reduciendo el estrés laboral."),
            ("AP-04", "El tiempo que dedico al registro administrativo de vacunas es equilibrado y me deja disponibilidad para mis labores sanitarias y asistenciales."),
        ],
    ),
    (
        "I3.2 Utilidad percibida para la gestión sanitaria",
        [
            ("UP-01", "El mecanismo de registro utilizado me permite disponer de información fidedigna y en tiempo real del stock de vacunas y jeringas."),
            ("UP-02", "El control de números de lote y fechas de vencimiento que brinda el proceso previene oportunamente mermas o pérdidas de biológicos."),
            ("UP-03", "La metodología de gestión facilita la detección inmediata y rectificación de cualquier descuadre de inventario físico versus registrado."),
            ("UP-04", "En general, considero que el procedimiento empleado es una herramienta altamente eficaz para garantizar el abastecimiento oportuno de vacunas."),
        ],
    ),
]

CERTIFICADO = {
    "numero": "03",
    "titulo": ("CUESTIONARIO DE SATISFACCIÓN DEL USUARIO Y ACEPTACIÓN "
               "TECNOLÓGICA (MODELO TAM)"),
    "modalidad": "MODALIDAD A",
    "variable": "VARIABLE DEPENDIENTE",
    "nombre_variable": "GESTIÓN DE MOVIMIENTOS DE VACUNAS",
    "dimension": "Dimensión 3: Satisfacción del usuario",
    "indicadores": "Indicadores I3.1 Aceptación del proceso operativo e I3.2 Utilidad percibida",
    "dimensiones": ITEMS_MODALIDAD_A,
}

CODIGOS_ESPERADOS = [codigo for _, items in ITEMS_MODALIDAD_A for codigo, _ in items]


# ------------------------------------------------------------------------------
# UTILIDADES OPENXML DE CELDA Y PARRAFO
# ------------------------------------------------------------------------------


def _p_vacio(line=240, before=10, after=10):
    """Parrafo vacio con interlineado sencillo, sin sangria."""
    return parse_xml(
        r'<w:p %s><w:pPr><w:spacing w:line="%d" w:lineRule="auto" '
        r'w:before="%d" w:after="%d"/><w:ind w:firstLine="0"/></w:pPr></w:p>'
        % (nsdecls("w"), line, before, after)
    )


def fijar_contenido_celda(cell, elemento):
    """Reemplaza el contenido de una celda conservando unicamente su w:tcPr."""
    tc = cell._tc
    for hijo in list(tc):
        if hijo.tag != qn("w:tcPr"):
            tc.remove(hijo)
    tc.append(elemento)


def texto_celda(cell, texto, tamano=TAM_ITEM, negrita=False, cursiva=False,
                alineacion="center", before=10, after=10,
                margen_izq_dxa=0):
    """Escribe texto formateado en una celda mediante el motor quirurgico."""
    p = quirurgico.crear_parrafo_celda(
        texto,
        bold=negrita,
        italic=cursiva,
        fuente=FUENTE,
        font_size_pt=tamano,
        align=alineacion,
        line_spacing=quirurgico.LINE_SPACING_1_0_DXA,
        space_before=before,
        space_after=after,
    )
    if margen_izq_dxa:
        # Se modifica el w:ind existente para preservar el orden exigido por el
        # esquema CT_PPr (spacing, ind, jc); reinsertarlo al final invalidaria el XML.
        pPr = p.find(qn("w:pPr"))
        for ind in pPr.findall(qn("w:ind")):
            ind.set(qn("w:left"), str(margen_izq_dxa))
            ind.set(qn("w:firstLine"), "0")
    fijar_contenido_celda(cell, p)


def texto_celda_con_superindice(cell, base, superindice, tamano=TAM_ENCABEZADO):
    """Escribe en la celda un rotulo con su llamada de nota en superindice real."""
    p = parse_xml(
        r'<w:p %s><w:pPr><w:spacing w:line="240" w:lineRule="auto" '
        r'w:before="10" w:after="10"/><w:ind w:firstLine="0"/>'
        r'<w:jc w:val="center"/></w:pPr></w:p>' % nsdecls("w")
    )
    sz_val = str(int(tamano * 2))
    for contenido, es_super in ((base, False), (superindice, True)):
        r = parse_xml(
            r'<w:r %s><w:rPr>'
            r'<w:rFonts w:ascii="%s" w:hAnsi="%s" w:eastAsia="%s" w:cs="%s"/>'
            r'<w:b w:val="1"/><w:color w:val="000000"/>'
            r'<w:sz w:val="%s"/><w:szCs w:val="%s"/>'
            r'<w:vertAlign w:val="%s"/>'
            r'</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>'
            % (nsdecls("w"), FUENTE, FUENTE, FUENTE, FUENTE,
               sz_val, sz_val, "superscript" if es_super else "baseline",
               contenido)
        )
        p.append(r)
    fijar_contenido_celda(cell, p)


def agregar_parrafo(doc, texto="", tamano=TAM_BLOQUE, negrita=False,
                    cursiva=False, alineacion=WD_ALIGN_PARAGRAPH.LEFT,
                    before=0, after=0, sangria_izq_dxa=0):
    """Agrega un parrafo de cuerpo con tipografia Times New Roman."""
    p = doc.add_paragraph()
    p.alignment = alineacion
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.0
    if sangria_izq_dxa:
        p.paragraph_format.left_indent = Cm(sangria_izq_dxa / 567.0)
    if texto:
        r = p.add_run(texto)
        r.font.name = FUENTE
        r.font.size = Pt(tamano)
        r.font.bold = negrita
        r.font.italic = cursiva
        r._element.rPr.rFonts.set(qn("w:eastAsia"), FUENTE)
        r._element.rPr.rFonts.set(qn("w:cs"), FUENTE)
    return p


def agregar_parrafo_con_superindice(doc, numero, texto, tamano=TAM_NOTA,
                                    alineacion=WD_ALIGN_PARAGRAPH.JUSTIFY,
                                    before=0, after=0):
    """Parrafo de nota al pie con el digito del criterio en superindice.

    Si `numero` es una cadena no numerica (por ejemplo "Nota:"), el prefijo se
    escribe en cursiva y sin superindice, conforme al modelo institucional.
    """
    p = doc.add_paragraph()
    p.alignment = alineacion
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.left_indent = Cm(0.30)
    p.paragraph_format.first_line_indent = Cm(-0.30)

    es_numerico = isinstance(numero, int) or str(numero).strip().isdigit()

    r_sup = p.add_run(str(numero))
    r_sup.font.name = FUENTE
    r_sup.font.size = Pt(tamano)
    if es_numerico:
        r_sup.font.superscript = True
    else:
        r_sup.font.italic = True

    r_cuerpo = p.add_run(texto)
    r_cuerpo.font.name = FUENTE
    r_cuerpo.font.size = Pt(tamano)
    return p


def agregar_linea_escritura(doc, before=5, after=5):
    """Linea de escritura en blanco para el llenado manuscrito."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.0
    pPr = p._p.get_or_add_pPr()

    # w:pBdr se inserta antes del primer elemento que el esquema CT_PPr situa
    # despues de el; anexarlo al final invalidaria la secuencia del parrafo.
    borde = parse_xml(
        r'<w:pBdr %s><w:bottom w:val="single" w:sz="4" w:space="1" w:color="000000"/></w:pBdr>'
        % nsdecls("w")
    )
    sucesores = (
        "w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
        "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
        "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
        "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
        "w:textDirection", "w:textAlignment", "w:textboxTightWrap",
        "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr",
        "w:pPrChange",
    )
    insertado = False
    for etiqueta in sucesores:
        referencia = pPr.find(qn(etiqueta))
        if referencia is not None:
            referencia.addprevious(borde)
            insertado = True
            break
    if not insertado:
        pPr.append(borde)

    r = p.add_run(" ")
    r.font.name = FUENTE
    r.font.size = Pt(TAM_BLOQUE)
    return p


# ------------------------------------------------------------------------------
# CONSTRUCCION DEL CERTIFICADO
# ------------------------------------------------------------------------------


def configurar_pagina(seccion, doc=None):
    """A4 vertical con margenes de formulario institucional."""
    seccion.page_width = Cm(21.0)
    seccion.page_height = Cm(29.7)
    seccion.left_margin = Cm(2.0)
    seccion.right_margin = Cm(1.5)
    seccion.top_margin = Cm(1.8)
    seccion.bottom_margin = Cm(1.5)
    seccion.header_distance = Cm(1.0)
    seccion.footer_distance = Cm(0.9)

    if doc is not None:
        # La totalidad del documento, incluidos los parrafos sin texto, declara
        # Times New Roman para no heredar la fuente por defecto de la plantilla.
        estilo = doc.styles["Normal"]
        estilo.font.name = FUENTE
        estilo.font.size = Pt(TAM_BLOQUE)
        rPr = estilo.element.get_or_add_rPr()
        rFonts = rPr.find(qn("w:rFonts"))
        if rFonts is None:
            rFonts = parse_xml(r'<w:rFonts %s/>' % nsdecls("w"))
            rPr.insert(0, rFonts)
        for atributo in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
            rFonts.set(qn(atributo), FUENTE)


def normalizar_celdas_sin_parrafo(tabla):
    """
    Garantiza que cada w:tc contenga al menos un w:p.

    Las fusiones de python-docx vacian por completo las celdas absorbidas; el
    esquema OpenXML exige un parrafo minimo por celda y Word rechaza el archivo
    cuando falta. Esta pasada reinyecta un parrafo vacio donde sea necesario.
    """
    reinyectados = 0
    for tr in tabla._tbl.findall(qn("w:tr")):
        for tc in tr.findall(qn("w:tc")):
            if tc.find(qn("w:p")) is None:
                tc.append(_p_vacio())
                reinyectados += 1
    return reinyectados


def fijar_disposicion_fija(tabla):
    """Fija w:tblLayout en modo fixed para que Word respete los anchos en dxa.

    Sin esta declaracion Word puede reajustar las columnas al contenido y
    desbordar la tabla fuera del ancho util. El elemento se inserta antes de
    w:tblCellMar y w:tblLook, conforme al orden exigido por CT_TblPr.
    """
    tblPr = tabla._tbl.tblPr
    for previo in tblPr.findall(qn("w:tblLayout")):
        tblPr.remove(previo)
    layout = parse_xml(
        r'<w:tblLayout %s w:type="fixed"/>' % nsdecls("w"))
    for etiqueta in ("w:tblCellMar", "w:tblLook", "w:tblCaption",
                     "w:tblDescription"):
        referencia = tblPr.find(qn(etiqueta))
        if referencia is not None:
            referencia.addprevious(layout)
            return
    tblPr.append(layout)


def construir_tabla_certificado(doc, dimensiones):
    """
    Construye la tabla de validacion con la estructura Fany 2024:
    dos filas de encabezado, una fila por dimension y una fila por item.
    """
    total_items = sum(len(items) for _, items in dimensiones)
    n_filas = 2 + len(dimensiones) + total_items
    if n_filas != FILAS_ESPERADAS or total_items != 8:
        raise ValueError(
            "La estructura del certificado debe tener %d filas y 8 items; "
            "se obtuvieron %d filas y %d items."
            % (FILAS_ESPERADAS, n_filas, total_items)
        )

    tabla = doc.add_table(rows=n_filas, cols=COLUMNAS_ESPERADAS)
    quirurgico.configurar_geometria_tabla(
        tabla, ANCHO_UTIL_DXA, COL_WIDTHS_DXA,
        align="center", cell_margin_dxa=(20, 50, 20, 50),
    )
    quirurgico.aplicar_bordes_rejilla(tabla, color="808080", sz="4")
    fijar_disposicion_fija(tabla)

    # --- Fusiones previas al rotulado del encabezado ---
    # Verticales: N, DIMENSIONES / items y Sugerencias ocupan las dos filas.
    for c in (COL_N, COL_ITEM, COL_SUGERENCIAS):
        celda = tabla.cell(0, c).merge(tabla.cell(1, c))
        celda.width = Cm(COL_WIDTHS_DXA[c] / 567.0)
    # Horizontales: cada criterio abarca sus columnas Si y No en la fila 1.
    for c in (2, 4, 6):
        celda = tabla.cell(0, c).merge(tabla.cell(0, c + 1))
        celda.width = Cm((COL_WIDTHS_DXA[c] + COL_WIDTHS_DXA[c + 1]) / 567.0)

    # --- Encabezado: fila 1 ---
    texto_celda(tabla.cell(0, COL_N), "N°", tamano=TAM_ENCABEZADO, negrita=True)
    texto_celda(tabla.cell(0, COL_ITEM), "DIMENSIONES / ítems",
                tamano=TAM_ENCABEZADO, negrita=True)
    texto_celda_con_superindice(tabla.cell(0, 2), "Pertinencia", "1")
    texto_celda_con_superindice(tabla.cell(0, 4), "Relevancia", "2")
    texto_celda_con_superindice(tabla.cell(0, 6), "Claridad", "3")
    texto_celda(tabla.cell(0, COL_SUGERENCIAS), "Sugerencias",
                tamano=TAM_ENCABEZADO, negrita=True)

    # --- Encabezado: fila 2 (Si / No) ---
    for c, etiqueta in ETIQUETAS_CRITERIO.items():
        texto_celda(tabla.cell(1, c), etiqueta, tamano=TAM_ENCABEZADO,
                    negrita=True)

    # --- Filas de dimension e items ---
    fila = 2
    for etiqueta_dim, items in dimensiones:
        celda_dim = tabla.cell(fila, COL_N).merge(tabla.cell(fila, COL_ITEM))
        celda_dim.width = Cm((COL_WIDTHS_DXA[COL_N] + COL_WIDTHS_DXA[COL_ITEM]) / 567.0)
        texto_celda(celda_dim, etiqueta_dim, tamano=TAM_DIMENSION, negrita=True,
                    alineacion="left", before=15, after=15, margen_izq_dxa=50)
        for c, etiqueta in ETIQUETAS_CRITERIO.items():
            texto_celda(tabla.cell(fila, c), etiqueta, tamano=TAM_ENCABEZADO,
                        negrita=True)
        fijar_contenido_celda(tabla.cell(fila, COL_SUGERENCIAS), _p_vacio())
        fila += 1

        for codigo, enunciado in items:
            texto_celda(tabla.cell(fila, COL_N), codigo, tamano=TAM_CODIGO,
                        alineacion="center")
            texto_celda(tabla.cell(fila, COL_ITEM), enunciado, tamano=TAM_ITEM,
                        alineacion="both", before=10, after=10,
                        margen_izq_dxa=50)
            for c in COLS_CRITERIO:
                fijar_contenido_celda(tabla.cell(fila, c), _p_vacio())
            fijar_contenido_celda(tabla.cell(fila, COL_SUGERENCIAS), _p_vacio())
            fila += 1

    # --- Alineacion vertical y blindaje de filas ---
    normalizar_celdas_sin_parrafo(tabla)

    for row in tabla.rows:
        for cell in row.cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    quirurgico.blindar_filas_tabla(
        tabla, cant_split=True, repetir_encabezado=True, filas_encabezado=2
    )
    quirurgico.normalizar_orden_tblPr(tabla)
    return tabla


def construir_bloque_inferior(doc):
    """Observaciones, opinion de aplicabilidad, identidad del juez y firma."""
    agregar_parrafo(doc, "Observaciones (precisar si hay suficiencia):",
                    tamano=TAM_BLOQUE, negrita=True, before=4, after=1)
    agregar_linea_escritura(doc, before=6, after=5)

    agregar_parrafo(
        doc,
        "Opinión de aplicabilidad:      Aplicable [   ]      "
        "Aplicable después de corregir [   ]      No aplicable [   ]",
        tamano=TAM_BLOQUE, before=3, after=3,
    )

    agregar_parrafo(
        doc,
        "Apellidos y nombres del juez validador: "
        "............................................................................"
        "        DNI: ..........................",
        tamano=TAM_BLOQUE, before=2, after=2,
    )

    agregar_parrafo(
        doc,
        "Especialidad del validador: "
        "............................................................................"
        "................................",
        tamano=TAM_BLOQUE, before=2, after=2,
    )

    agregar_parrafo(
        doc,
        "Andahuaylas, ......... de ........................................ de " + ANIO_CONSTANCIA,
        tamano=TAM_BLOQUE, before=4, after=5,
    )

    agregar_parrafo(doc, "______________________________",
                    tamano=TAM_BLOQUE, alineacion=WD_ALIGN_PARAGRAPH.CENTER,
                    before=8, after=0)
    agregar_parrafo(doc, "Firma del experto informante",
                    tamano=TAM_BLOQUE, alineacion=WD_ALIGN_PARAGRAPH.CENTER,
                    before=1, after=0)


def construir_notas_al_pie(doc):
    """Notas de los tres criterios y nota de suficiencia, en cuerpo menor."""
    agregar_parrafo(doc, "", tamano=4, before=0, after=1)
    agregar_parrafo_con_superindice(
        doc, 1, "Pertinencia: El ítem corresponde al concepto teórico formulado.")
    agregar_parrafo_con_superindice(
        doc, 2,
        "Relevancia: El ítem es apropiado para representar al componente o "
        "dimensión específica del constructo.")
    agregar_parrafo_con_superindice(
        doc, 3,
        "Claridad: Se entiende sin dificultad alguna el enunciado del ítem, "
        "es conciso, exacto y directo.")
    agregar_parrafo_con_superindice(
        doc, "Nota:",
        " Suficiencia, se dice suficiencia cuando los ítems planteados son "
        "suficientes para medir la dimensión", before=1, after=0)


def construir_documento():
    """Construye en memoria el certificado unico y devuelve el documento."""
    doc = docx.Document()
    configurar_pagina(doc.sections[0], doc=doc)

    # 1. Titulo de seccion
    agregar_parrafo(doc, "Anexo 2. Instrumento de validación",
                    tamano=TAM_TITULO, negrita=True, before=0, after=4)

    # 2. Rotulo del certificado
    rotulo = (
        "CERTIFICADO DE VALIDEZ DE CONTENIDO DEL INSTRUMENTO N.° %s: "
        "%s. %s" % (CERTIFICADO["numero"], CERTIFICADO["titulo"],
                    CERTIFICADO["modalidad"])
    )
    agregar_parrafo(doc, rotulo, tamano=TAM_CERTIFICADO, negrita=True,
                    alineacion=WD_ALIGN_PARAGRAPH.CENTER, before=0, after=2)

    # 3. Referencia de la variable y de la dimension evaluada
    referencia = "%s: %s. %s. %s." % (
        CERTIFICADO["variable"], CERTIFICADO["nombre_variable"],
        CERTIFICADO["dimension"], CERTIFICADO["indicadores"])
    agregar_parrafo(doc, referencia, tamano=TAM_REFERENCIA,
                    alineacion=WD_ALIGN_PARAGRAPH.CENTER, before=0, after=5)

    # 4. Tabla de validacion
    construir_tabla_certificado(doc, CERTIFICADO["dimensiones"])

    # 5. Bloque inferior
    construir_bloque_inferior(doc)

    # 6. Notas al pie de la hoja
    construir_notas_al_pie(doc)

    return doc


def generar_certificado():
    """Genera el unico certificado DOCX en blanco y devuelve su ruta."""
    doc = construir_documento()
    ruta_salida = RUTA_SALIDA / NOMBRE_SALIDA
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(ruta_salida))
    return ruta_salida


def ejecutar_generacion():
    """Genera el certificado e informa el resultado."""
    print("=" * 78)
    print("SIVAC - ANEXO 2 MODELO FANY 2024")
    print("CERTIFICADO UNICO: INSTRUMENTO N.° 03 - MODALIDAD A (DEC-019, DEC-020)")
    print("=" * 78)
    ruta = generar_certificado()
    print("[OK] %s (%s bytes)" % (ruta.name, "{:,}".format(os.path.getsize(ruta))))
    print("     Items: AP-01 a AP-04 e UP-01 a UP-04 (8 en total).")
    print("     Estado: en blanco, listo para impresion y llenado manuscrito.")
    print("=" * 78)
    return 0


# ------------------------------------------------------------------------------
# VERIFICACION PROGRAMATICA DEL ENTREGABLE
# ------------------------------------------------------------------------------

PATRONES_PROHIBIDOS = [
    ("CIP", "registro de colegiatura"),
    ("DICTAMEN", "dictamen emitido"),
    ("APROBADO", "veredicto emitido"),
    ("Segoe Script", "fuente manuscrita simulada"),
    ("1A3A8A", "color de tinta manuscrita simulada"),
]


def _texto_de_tc(tc):
    """Extrae el texto de un elemento w:tc sin depender de los proxies de python-docx."""
    return "".join(t.text or "" for t in tc.iter(qn("w:t"))).strip()


def _runs_de_tc(tc):
    """Devuelve los elementos w:r contenidos en un w:tc."""
    return tc.findall(".//" + qn("w:r"))


def _normalizar(texto):
    """Colapsa espacios para comparar transcripciones literales."""
    return re.sub(r"\s+", " ", texto or "").strip()


def auditar_documento(doc):
    """Audita el certificado a nivel de elementos OpenXML."""
    hallazgos = {
        "items_detectados": 0,
        "codigos": [],
        "dimensiones_detectadas": [],
        "enunciados": {},
        "celdas_criterio_con_texto": [],
        "celdas_criterio_con_digito": [],
        "sugerencias_con_texto": [],
        "marcas_x": 0,
        "patrones_prohibidos": [],
        "sombreados": 0,
        "colores_no_negros": set(),
        "omml_en_tablas": 0,
        "fuentes": set(),
        "tablas": len(doc.tables),
        "filas": 0,
        "columnas": 0,
        "filas_con_cantsplit": 0,
        "filas_con_tblheader": 0,
        "fecha_en_blanco": False,
    }

    texto_total = []
    for p in doc.paragraphs:
        texto_total.append(p.text)
        for r in p.runs:
            if r.font.name:
                hallazgos["fuentes"].add(r.font.name)
            if r.font.color and r.font.color.rgb:
                hallazgos["colores_no_negros"].add(str(r.font.color.rgb))

    for tabla in doc.tables:
        filas_xml = tabla._tbl.findall(qn("w:tr"))
        hallazgos["filas"] = max(hallazgos["filas"], len(filas_xml))
        tblGrid = tabla._tbl.find(qn("w:tblGrid"))
        if tblGrid is not None:
            n_cols = len(tblGrid.findall(qn("w:gridCol")))
            hallazgos["columnas"] = max(hallazgos["columnas"], n_cols)
        hallazgos["omml_en_tablas"] += len(
            tabla._tbl.xpath('.//*[local-name()="oMath"]'))

        for tr in filas_xml:
            trPr = tr.find(qn("w:trPr"))
            if trPr is not None:
                if trPr.find(qn("w:cantSplit")) is not None:
                    hallazgos["filas_con_cantsplit"] += 1
                if trPr.find(qn("w:tblHeader")) is not None:
                    hallazgos["filas_con_tblheader"] += 1

            tcs = tr.findall(qn("w:tc"))
            for tc in tcs:
                texto_total.append(_texto_de_tc(tc))
                for r in _runs_de_tc(tc):
                    rPr = r.find(qn("w:rPr"))
                    if rPr is None:
                        continue
                    rFonts = rPr.find(qn("w:rFonts"))
                    if rFonts is not None:
                        nombre = rFonts.get(qn("w:ascii"))
                        if nombre:
                            hallazgos["fuentes"].add(nombre)
                    color = rPr.find(qn("w:color"))
                    if color is not None:
                        val = color.get(qn("w:val"))
                        if val:
                            hallazgos["colores_no_negros"].add(val.upper())
                tcPr = tc.find(qn("w:tcPr"))
                if tcPr is not None:
                    for shd in tcPr.findall(qn("w:shd")):
                        relleno = shd.get(qn("w:fill"))
                        if relleno and relleno.lower() not in ("auto", "ffffff"):
                            hallazgos["sombreados"] += 1

            # Fila de item: nueve celdas y un codigo AP-nn o UP-nn en la columna N.
            if len(tcs) == COLUMNAS_ESPERADAS:
                etiqueta_n = _texto_de_tc(tcs[COL_N])
                if re.fullmatch(r"(AP|UP)-\d{2}", etiqueta_n):
                    hallazgos["items_detectados"] += 1
                    hallazgos["codigos"].append(etiqueta_n)
                    hallazgos["enunciados"][etiqueta_n] = _texto_de_tc(tcs[COL_ITEM])
                    for c in COLS_CRITERIO:
                        valor = _texto_de_tc(tcs[c])
                        if valor:
                            hallazgos["celdas_criterio_con_texto"].append(
                                (etiqueta_n, c, valor))
                        if any(ch in "0123456789" for ch in valor):
                            hallazgos["celdas_criterio_con_digito"].append(
                                (etiqueta_n, c, valor))
                    sugerencia = _texto_de_tc(tcs[COL_SUGERENCIAS])
                    if sugerencia:
                        hallazgos["sugerencias_con_texto"].append(
                            (etiqueta_n, sugerencia))

    texto_unido = "\n".join(texto_total)

    # Linea de fecha: espacio en blanco para el dia y el mes, año fijo en texto.
    hallazgos["fecha_en_blanco"] = bool(re.search(
        r"de\s+\.{4,}\s+de\s+" + ANIO_CONSTANCIA, texto_unido))

    # Rotulos de dimension presentes en el documento
    for etiqueta, _ in ITEMS_MODALIDAD_A:
        if etiqueta in texto_unido:
            hallazgos["dimensiones_detectadas"].append(etiqueta)

    for patron, motivo in PATRONES_PROHIBIDOS:
        if re.search(r"(?<![A-Za-zÁÉÍÓÚÑ])" + re.escape(patron) + r"(?![A-Za-zÁÉÍÓÚÑ])",
                     texto_unido):
            hallazgos["patrones_prohibidos"].append((patron, motivo))

    # Marcas X o aspa en cualquier parte del documento.
    for token in re.split(r"[\s|\[\]]+", texto_unido):
        if token.strip().upper() in ("X", "XX", "×"):
            hallazgos["marcas_x"] += 1

    hallazgos["patrones_prohibidos"] = sorted(set(hallazgos["patrones_prohibidos"]))
    return hallazgos


def evaluar_hallazgos(h):
    """Convierte el diccionario de hallazgos en una lista de comprobaciones."""
    codigos_ok = h["codigos"] == CODIGOS_ESPERADOS
    transcripcion_ok = all(
        _normalizar(h["enunciados"].get(codigo, "")) == _normalizar(enunciado)
        for _, items in ITEMS_MODALIDAD_A
        for codigo, enunciado in items
    )
    return [
        ("Tabla unica con %d filas y %d columnas" % (FILAS_ESPERADAS, COLUMNAS_ESPERADAS),
         h["tablas"] == 1 and h["filas"] == FILAS_ESPERADAS
         and h["columnas"] == COLUMNAS_ESPERADAS,
         "%d tabla(s), %d filas, %d columnas" % (h["tablas"], h["filas"], h["columnas"])),
        ("Ocho items con codigos AP-01 a AP-04 e UP-01 a UP-04",
         h["items_detectados"] == 8 and codigos_ok,
         "%d items: %s" % (h["items_detectados"], ", ".join(h["codigos"]) or "ninguno")),
        ("Transcripcion literal de los ocho reactivos",
         transcripcion_ok,
         "coincide con el Instrumento N.° 03" if transcripcion_ok else "discrepancia detectada"),
        ("Dos encabezados de dimension I3.1 e I3.2",
         len(h["dimensiones_detectadas"]) == 2,
         "; ".join(h["dimensiones_detectadas"]) or "ninguno"),
        ("Celdas de criterio vacias, sin digitos",
         not h["celdas_criterio_con_texto"] and not h["celdas_criterio_con_digito"],
         "%d con texto, %d con digito" % (
             len(h["celdas_criterio_con_texto"]), len(h["celdas_criterio_con_digito"]))),
        ("Columna de sugerencias vacia",
         not h["sugerencias_con_texto"],
         "%d con texto" % len(h["sugerencias_con_texto"])),
        ("Sin marcas X ni aspas",
         h["marcas_x"] == 0,
         "%d marca(s)" % h["marcas_x"]),
        ("Sin patrones prohibidos",
         not h["patrones_prohibidos"],
         ", ".join(p for p, _ in h["patrones_prohibidos"]) or "ninguno"),
        ("Sin sombreados de relleno",
         h["sombreados"] == 0,
         "%d celda(s)" % h["sombreados"]),
        ("Sin colores de tinta distintos del negro",
         h["colores_no_negros"] <= {"000000"},
         ", ".join(sorted(h["colores_no_negros"])) or "sin declaracion"),
        ("Sin OMML dentro de tablas",
         h["omml_en_tablas"] == 0,
         "%d elemento(s)" % h["omml_en_tablas"]),
        ("Fuente Times New Roman exclusiva",
         h["fuentes"] <= {FUENTE},
         ", ".join(sorted(h["fuentes"])) or "sin declaracion"),
        ("Fecha en blanco con el año %s como texto fijo" % ANIO_CONSTANCIA,
         h["fecha_en_blanco"],
         "linea de fecha con el año fijo" if h["fecha_en_blanco"]
         else "no se detecto la linea de fecha esperada"),
        ("Filas no fragmentables y encabezado de dos filas repetido",
         h["filas_con_cantsplit"] == h["filas"] and h["filas_con_tblheader"] == 2,
         "cantSplit %d/%d, tblHeader %d" % (
             h["filas_con_cantsplit"], h["filas"], h["filas_con_tblheader"])),
    ]


def ejecutar_verificacion():
    """Audita la estructura del certificado en memoria, sin escribir DOCX."""
    print("=" * 78)
    print("VERIFICACION ESTRUCTURAL - CERTIFICADO UNICO DEL INSTRUMENTO N.° 03")
    print("Modalidad A: 8 items, 2 dimensiones, formato Fany 2024 (DEC-015)")
    print("=" * 78)

    doc = construir_documento()
    comprobaciones = evaluar_hallazgos(auditar_documento(doc))

    fallos = 0
    for nombre, ok, detalle in comprobaciones:
        print("  [%s] %s" % ("OK" if ok else "FALLA", nombre))
        print("         %s" % detalle)
        if not ok:
            fallos += 1

    ruta_existente = RUTA_SALIDA / NOMBRE_SALIDA
    print("-" * 78)
    if ruta_existente.exists():
        archivo = docx.Document(str(ruta_existente))
        comprobaciones_archivo = evaluar_hallazgos(auditar_documento(archivo))
        fallos_archivo = sum(1 for _, ok, _ in comprobaciones_archivo if not ok)
        print("  DOCX en disco: %s" % ruta_existente.name)
        print("  Comprobaciones no conformes sobre el archivo: %d" % fallos_archivo)
        fallos += fallos_archivo
    else:
        print("  DOCX en disco: no generado (esta verificacion no escribe archivos).")

    print("-" * 78)
    print("  Comprobaciones: %d | No conformes: %d" % (len(comprobaciones), fallos))
    print("  Estado: %s" % ("CONFORME" if fallos == 0 else "NO CONFORME"))
    print("=" * 78)
    return 0 if fallos == 0 else 1


def imprimir_uso():
    """Explica los modos de ejecucion sin escribir ningun archivo."""
    print("=" * 78)
    print("SIVAC - ANEXO 2 MODELO FANY 2024")
    print("Generador del certificado unico del Instrumento N.° 03, Modalidad A.")
    print("=" * 78)
    print("Uso:")
    print("  python scripts/compiladores/generar_anexo2_validacion_fany.py --verificar")
    print("      Audita la estructura del certificado en memoria sin escribir DOCX.")
    print("  python scripts/compiladores/generar_anexo2_validacion_fany.py --generar")
    print("      Genera el unico certificado en blanco en %s" % RUTA_SALIDA)
    print()
    print("Sin argumentos no se escribe ningun archivo. Los Instrumentos 01 y 02")
    print("no se someten a juicio de contenido (DEC-020).")
    print("=" * 78)


def main():
    parser = argparse.ArgumentParser(
        description="Genera el Anexo 2 de validacion por juicio de expertos, "
                    "modelo Fany 2024, en blanco.")
    grupo = parser.add_mutually_exclusive_group()
    grupo.add_argument("--generar", action="store_true",
                       help="Genera el certificado DOCX en blanco del Instrumento N.° 03")
    grupo.add_argument("--verificar", action="store_true",
                       help="Audita la estructura en memoria sin generar DOCX")
    args = parser.parse_args()

    if args.generar:
        sys.exit(ejecutar_generacion())
    if args.verificar:
        sys.exit(ejecutar_verificacion())

    imprimir_uso()
    sys.exit(0)


if __name__ == "__main__":
    main()
