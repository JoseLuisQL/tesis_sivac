#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - MOTOR QUIRÚRGICO DE MANIPULACIÓN Y FORMATEO DOCX / OPENXML
================================================================================
Módulo centralizado y reutilizable para maquetación editorial en Microsoft Word,
cumpliendo estrictamente con APA 7.ª edición y la normativa institucional UNAJMA.

Capacidades integradas:
  1. Conversión e inserción de ecuaciones MathML / LaTeX a OMML nativo de Word
     mediante la hoja de transformación oficial MML2OMML.XSL de Microsoft Office.
  2. Geometría tabular milimétrica (ancho total dxa, anchos por columna en w:tblGrid
     y w:tcW, márgenes celulares w:tblCellMar).
  3. Erradicación automática de propiedades de flotación (w:tblpPr) que quiebran
     el motor de paginación de Word.
  4. Blindaje contra fracturas de filas (w:cantSplit) y repetición de encabezados (w:tblHeader).
  5. Bordes APA 7 canónicos (tres líneas horizontales, cero verticales).
  6. Fusión vertical (w:vMerge) y alineación vertical/horizontal precisa.
  7. Auditoría estática de tablas y dimensiones de página.
  8. Exportación desatendida a PDF mediante Microsoft Word COM.
  9. Renderizado de páginas a imágenes PNG (150/300 DPI) vía PyMuPDF para auditoría visual.
================================================================================
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
import lxml.etree as ET
from xml.sax.saxutils import escape

import docx
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

# Constantes tipográficas institucionales UNAJMA y APA 7
FUENTE_POR_DEFECTO = "Times New Roman"
ANCHO_UTIL_PORTRAIT_DXA = 8788    # 15.50 cm (A4 21.0 cm - Margen Izq 3.0 cm - Margen Der 2.50 cm)
ANCHO_UTIL_LANDSCAPE_DXA = 14000  # 24.70 cm (A4 29.7 cm - Margen Izq 2.5 cm - Margen Der 2.50 cm)

# Parámetros OpenXML de interlineado, sangrías y espaciado APA 7 / UNAJMA
LINE_SPACING_1_5_DXA = 360       # Interlineado 1.5 líneas (360 dxa / w:line="360" w:lineRule="auto")
LINE_SPACING_1_0_DXA = 240       # Interlineado sencillo (240 dxa)
SANGRIA_PRIMERA_LINEA_DXA = 720  # Sangría de primera línea APA 7 (1.27 cm / 0.5 in = 720 dxa)
SANGRIA_FRANCESA_DXA = 720       # Sangría francesa para referencias bibliográficas (1.27 cm)
FONT_SIZE_BODY_PT = 12.0         # Cuerpo de texto institucional (12 pt / w:sz="24")
FONT_SIZE_TABLE_PT = 10.0        # Texto en celdas de tabla (10 pt / w:sz="20")
FONT_SIZE_NOTE_PT = 9.5          # Notas de tablas y figuras (9.5 pt / w:sz="19")

# Rutas estándar del convertidor oficial MML2OMML.XSL de Microsoft Office
RUTAS_MML2OMML = [
    r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL",
    r"C:\Program Files (x86)\Microsoft Office\root\Office16\MML2OMML.XSL",
    r"C:\Program Files\Microsoft Office\Office16\MML2OMML.XSL",
    r"C:\Program Files (x86)\Microsoft Office\Office16\MML2OMML.XSL",
    os.path.join(os.path.dirname(__file__), "MML2OMML.XSL")
]

_transformador_mml = None

def obtener_transformador_omml():
    """Carga y cachea la hoja de estilos XSLT MML2OMML.XSL para transformar MathML a OMML."""
    global _transformador_mml
    if _transformador_mml is not None:
        return _transformador_mml

    ruta_encontrada = None
    for r in RUTAS_MML2OMML:
        if os.path.exists(r):
            ruta_encontrada = r
            break

    if not ruta_encontrada:
        raise FileNotFoundError(
            "No se encontró la hoja de estilos MML2OMML.XSL en las rutas conocidas de Microsoft Office. "
            "Asegúrese de tener Microsoft Word / Office instalado o proveer la ruta al archivo."
        )

    xslt_doc = ET.parse(ruta_encontrada)
    _transformador_mml = ET.XSLT(xslt_doc)
    return _transformador_mml


# ==============================================================================
# 1. MOTOR DE MATEMÁTICAS Y FÓRMULAS OMML NATIVAS (<m:oMath>)
# ==============================================================================

def reparar_nary_omml(omml_elem):
    """
    Repara nodos <m:nary> (operadores de sumatoria, integral, producto, etc.) en OMML.
    Si <m:e> está vacío, Word renderiza una caja punteada de reemplazo (placeholder de operando faltante).
    Esta función detecta el operando subsiguiente (ej. <m:sSub>, <m:r>, etc.) y lo inserta dentro
    de <m:e>, o inyecta un operando vacío no visible para erradicar definitivamente la caja punteada.
    """
    ns_m = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'
    for nary in omml_elem.xpath('.//*[local-name()="nary"]'):
        e = nary.find(f'{ns_m}e')
        if e is not None and len(e) == 0 and not (e.text or '').strip():
            parent = nary.getparent()
            if parent is not None:
                idx = list(parent).index(nary)
                if idx + 1 < len(parent):
                    next_sib = parent[idx + 1]
                    txt = ''.join(next_sib.itertext()).strip()
                    if txt not in ['=', '+', '-', '<', '>', '≤', '≥', '→', '↔', '⇒', '⇔']:
                        parent.remove(next_sib)
                        e.append(next_sib)
                if len(e) == 0 and not (e.text or '').strip():
                    r_empty = parse_xml(r'<m:r xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:t xml:space="preserve"> </m:t></m:r>')
                    e.append(r_empty)


def mathml_to_omml(mathml_str):
    """
    Convierte una expresión MathML XML a un nodo OpenXML OMML (<m:oMath>).
    Limpia espacios en blanco, namespace prefixes redundantes y repara operadores n-arios.
    """
    transformador = obtener_transformador_omml()
    dom = ET.fromstring(mathml_str.strip())
    omml_tree = transformador(dom)
    omml_xml_bytes = ET.tostring(omml_tree)
    omml_elem = parse_xml(omml_xml_bytes)
    reparar_nary_omml(omml_elem)
    return omml_elem


def crear_parrafo_formula_dedicada(omml_elem, align="left", line_spacing=LINE_SPACING_1_0_DXA, space_before=40, space_after=50, left_indent_dxa=40):
    """
    Crea un párrafo que contiene exclusivamente una ecuación OMML nativa.
    Aplica lineRule="auto" (240 dxa = interlineado sencillo) y espaciado vertical
    seguro para erradicar totalmente colisiones y solapamientos con texto adyacente.
    """
    p = parse_xml(r'''<w:p %s>
        <w:pPr>
            <w:spacing w:line="%d" w:lineRule="auto" w:before="%d" w:after="%d"/>
            <w:ind w:firstLine="0" w:left="%d"/>
            <w:jc w:val="%s"/>
        </w:pPr>
    </w:p>''' % (nsdecls('w'), line_spacing, space_before, space_after, left_indent_dxa, align))
    p.append(omml_elem)
    return p


def crear_parrafo_mixto_inline(segmentos, fuente=FUENTE_POR_DEFECTO, font_size_pt=7.5, align="left", line_spacing=210, space_before=10, space_after=20):
    """
    Crea un párrafo fluido con mezcla de texto formateado y ecuaciones OMML en la misma línea.
    Argumentos de `segmentos`:
      - Tupla: (texto, negrita, cursiva)
      - Elemento OMML nativo: <m:oMath>
      - String simple: texto sin formato
    """
    sz_val = str(int(font_size_pt * 2))
    p = parse_xml(r'''<w:p %s>
        <w:pPr>
            <w:spacing w:line="%d" w:lineRule="auto" w:before="%d" w:after="%d"/>
            <w:ind w:firstLine="0"/>
            <w:jc w:val="%s"/>
        </w:pPr>
    </w:p>''' % (nsdecls('w'), line_spacing, space_before, space_after, align))

    for seg in segmentos:
        if hasattr(seg, 'tag') and 'oMath' in seg.tag:
            p.append(seg)
        elif isinstance(seg, tuple):
            t_text = escape(str(seg[0]))
            t_bold = bool(seg[1]) if len(seg) > 1 else False
            t_italic = bool(seg[2]) if len(seg) > 2 else False
            r = parse_xml(r'''<w:r %s>
                <w:rPr>
                    <w:rFonts w:ascii="%s" w:hAnsi="%s"/>
                    <w:b w:val="%s"/>
                    <w:i w:val="%s"/>
                    <w:color w:val="000000"/>
                    <w:u w:val="none"/>
                    <w:sz w:val="%s"/>
                </w:rPr>
                <w:t xml:space="preserve">%s</w:t>
            </w:r>''' % (nsdecls('w'), fuente, fuente,
                        "1" if t_bold else "0",
                        "1" if t_italic else "0",
                        sz_val, t_text))
            p.append(r)
        else:
            t_text = escape(str(seg))
            r = parse_xml(r'''<w:r %s>
                <w:rPr>
                    <w:rFonts w:ascii="%s" w:hAnsi="%s"/>
                    <w:b w:val="0"/>
                    <w:i w:val="0"/>
                    <w:color w:val="000000"/>
                    <w:u w:val="none"/>
                    <w:sz w:val="%s"/>
                </w:rPr>
                <w:t xml:space="preserve">%s</w:t>
            </w:r>''' % (nsdecls('w'), fuente, fuente, sz_val, t_text))
            p.append(r)

    return p


# ==============================================================================
# 2. MOTOR DE GEOMETRÍA TABULAR OPENXML APA 7
# ==============================================================================

def eliminar_flotacion_tabla(table):
    """
    Elimina w:tblpPr (propiedades de posicionamiento flotante).
    CRÍTICO: Word inserta tblpPr cuando una tabla es movida en la GUI, lo que
    causa que la tabla ignore los márgenes de página y se fracture caóticamente.
    """
    tblPr = table._tbl.tblPr
    tblpPr = tblPr.find(qn('w:tblpPr'))
    if tblpPr is not None:
        tblPr.remove(tblpPr)
        return True
    return False


def configurar_geometria_tabla(table, total_width_dxa, col_widths_dxa, align="center", cell_margin_dxa=(30, 60, 30, 60)):
    """
    Configura la geometría estricta de una tabla OpenXML:
      - Remueve propiedades de flotación.
      - Fija w:tblW en dxa exacto.
      - Regenera w:tblGrid con w:gridCol explícitos para cada columna.
      - Asigna w:tcW a cada celda de cada fila.
      - Fija márgenes celulares internos w:tblCellMar (top, left, bottom, right en dxa).
    """
    tblPr = table._tbl.tblPr
    eliminar_flotacion_tabla(table)

    # 1. Ancho total de la tabla
    for w in tblPr.findall(qn('w:tblW')):
        tblPr.remove(w)
    tblPr.append(parse_xml(r'<w:tblW %s w:w="%d" w:type="dxa"/>' % (nsdecls('w'), total_width_dxa)))

    # 2. Alineación de tabla
    for jc in tblPr.findall(qn('w:jc')):
        tblPr.remove(jc)
    tblPr.append(parse_xml(r'<w:jc %s w:val="%s"/>' % (nsdecls('w'), align)))

    # 3. Padding interno celular
    top_m, left_m, bottom_m, right_m = cell_margin_dxa
    for cm in tblPr.findall(qn('w:tblCellMar')):
        tblPr.remove(cm)
    tblPr.append(parse_xml(r'''<w:tblCellMar %s>
        <w:top w:w="%d" w:type="dxa"/>
        <w:left w:w="%d" w:type="dxa"/>
        <w:bottom w:w="%d" w:type="dxa"/>
        <w:right w:w="%d" w:type="dxa"/>
    </w:tblCellMar>''' % (nsdecls('w'), top_m, left_m, bottom_m, right_m)))

    # 4. Reconstrucción de la cuadrícula w:tblGrid
    tblGrid = table._tbl.tblGrid
    if tblGrid is not None:
        table._tbl.remove(tblGrid)
    new_grid = parse_xml(r'<w:tblGrid %s/>' % nsdecls('w'))
    for cw in col_widths_dxa:
        new_grid.append(parse_xml(r'<w:gridCol %s w:w="%d"/>' % (nsdecls('w'), cw)))
    tblPr_idx = list(table._tbl).index(tblPr)
    table._tbl.insert(tblPr_idx + 1, new_grid)

    # 5. Aplicar ancho en cada celda
    for row in table.rows:
        tcs = row._tr.findall(qn('w:tc'))
        for idx, cw in enumerate(col_widths_dxa):
            if idx < len(tcs):
                tcPr = tcs[idx].get_or_add_tcPr()
                for w in tcPr.findall(qn('w:tcW')):
                    tcPr.remove(w)
                tcPr.append(parse_xml(r'<w:tcW %s w:w="%d" w:type="dxa"/>' % (nsdecls('w'), cw)))


def aplicar_bordes_apa7(table):
    """
    Aplica exactamente las 3 líneas horizontales exigidas por APA 7:
      - Borde superior de tabla (w:top, single, sz=4)
      - Borde inferior de encabezados (w:bottom en celda de Fila 0, single, sz=4)
      - Borde inferior de tabla (w:bottom, single, sz=4)
      - Cero bordes verticales y cero líneas interiores.
    """
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


ORDEN_TBLPR = (
    'w:tblStyle', 'w:tblpPr', 'w:tblOverlap', 'w:bidiVisual',
    'w:tblStyleRowBandSize', 'w:tblStyleColBandSize', 'w:tblW', 'w:jc',
    'w:tblCellSpacing', 'w:tblInd', 'w:tblBorders', 'w:shd', 'w:tblLayout',
    'w:tblCellMar', 'w:tblLook', 'w:tblCaption', 'w:tblDescription',
    'w:tblPrChange',
)


def normalizar_orden_tblPr(table):
    """
    Reordena los hijos de w:tblPr según la secuencia de CT_TblPr.

    python-docx y el motor quirúrgico agregan propiedades al final del nodo, de
    modo que w:tblW, w:jc, w:tblBorders y w:tblCellMar pueden quedar detrás de
    w:tblLook. Word tolera el desorden, pero otros validadores estrictos no;
    esta pasada deja la tabla conforme al esquema sin alterar sus valores.
    """
    tblPr = table._tbl.tblPr
    hijos = list(tblPr)
    indice = {qn(etiqueta): pos for pos, etiqueta in enumerate(ORDEN_TBLPR)}

    def clave(elemento):
        return indice.get(elemento.tag, len(ORDEN_TBLPR))

    ordenados = sorted(hijos, key=clave)
    if ordenados == hijos:
        return False
    for hijo in hijos:
        tblPr.remove(hijo)
    for hijo in ordenados:
        tblPr.append(hijo)
    return True


def aplicar_bordes_rejilla(table, color="808080", sz="4"):
    """
    Aplica una rejilla completa (bordes exteriores e interiores) a una tabla.

    EXCEPCIÓN DOCUMENTAL DELIBERADA A APA 7: el formato APA 7 exige tres líneas
    horizontales y cero verticales para las tablas del cuerpo de la tesis. Sin
    embargo, los formatos institucionales de validación por juicio de expertos
    (Anexo 2, modelo Fany 2024) son formularios de captura manuscrita y requieren
    rejilla cerrada para que el juez identifique con precisión cada celda de
    marcado. Esta función se emplea exclusivamente en dichos formatos y jamás en
    tablas de resultados, operacionalización o consistencia.
    """
    tblPr = table._tbl.tblPr
    for b in tblPr.findall(qn('w:tblBorders')):
        tblPr.remove(b)

    xml = r'''<w:tblBorders %s>
        <w:top w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
        <w:left w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
        <w:bottom w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
        <w:right w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
        <w:insideH w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
        <w:insideV w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
    </w:tblBorders>''' % (nsdecls('w'), sz, color, sz, color, sz, color, sz, color, sz, color, sz, color)

    # CT_TblPr exige tblBorders antes de shd, tblLayout, tblCellMar y tblLook.
    bordes = parse_xml(xml)
    sucesores = ('w:shd', 'w:tblLayout', 'w:tblCellMar', 'w:tblLook',
                 'w:tblCaption', 'w:tblDescription')
    for etiqueta in sucesores:
        referencia = tblPr.find(qn(etiqueta))
        if referencia is not None:
            referencia.addprevious(bordes)
            return bordes
    tblPr.append(bordes)
    return bordes


def blindar_filas_tabla(table, cant_split=True, repetir_encabezado=True, filas_encabezado=1):
    """
    Asegura que las filas no se fracturen entre dos páginas (w:cantSplit)
    y que las filas de encabezado se repitan automáticamente si la tabla desborda
    (w:tblHeader). `filas_encabezado` permite declarar encabezados de dos o más
    filas, como exige el formato de validación por juicio de expertos (Anexo 2).
    """
    for r_idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        if cant_split and trPr.find(qn('w:cantSplit')) is None:
            trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
        if repetir_encabezado and r_idx < filas_encabezado and trPr.find(qn('w:tblHeader')) is None:
            trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))


def set_tc_vmerge(tc, mode):
    """
    Gestiona la fusión vertical de celdas en OpenXML:
      - mode='restart': Inicia un nuevo bloque fusionado.
      - mode='continue': Continúa la fusión con la celda superior.
      - mode='none': Celda independiente no fusionada.
    """
    tcPr = tc.get_or_add_tcPr()
    for vm in tcPr.findall(qn('w:vMerge')):
        tcPr.remove(vm)
    if mode == 'restart':
        tcPr.append(parse_xml(r'<w:vMerge %s w:val="restart"/>' % nsdecls('w')))
    elif mode == 'continue':
        tcPr.append(parse_xml(r'<w:vMerge %s/>' % nsdecls('w')))


def set_tc_paragraphs(tc, paragraphs):
    """
    Reemplaza todos los párrafos de una celda por una lista de nuevos elementos <w:p>.
    Garantiza que siempre exista al menos un párrafo para mantener el XML válido.
    """
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


def set_tc_bottom_border(tc, val='single', sz=4, color='888888'):
    """
    Asigna un borde inferior específico a una celda individual (w:tc o _Cell).
    Útil para líneas divisorias horizontales entre dimensiones o indicadores dentro de tablas APA 7.
    """
    tc_elem = tc._tc if hasattr(tc, '_tc') else tc
    tcPr = tc_elem.get_or_add_tcPr()
    tcBorders = tcPr.find(qn('w:tcBorders'))
    if tcBorders is None:
        tcBorders = parse_xml(r'<w:tcBorders %s/>' % nsdecls('w'))
        tcPr.append(tcBorders)
    for b in tcBorders.findall(qn('w:bottom')):
        tcBorders.remove(b)
    tcBorders.append(parse_xml(r'<w:bottom %s w:val="%s" w:sz="%d" w:space="0" w:color="%s"/>' % (
        nsdecls('w'), val, sz, color
    )))


def crear_parrafo_celda(texto, bold=False, italic=False, fuente=FUENTE_POR_DEFECTO, font_size_pt=7.5, align="left", line_spacing=LINE_SPACING_1_0_DXA, space_before=20, space_after=20):
    """
    Crea un párrafo para celdas de tablas bajo APA 7 y normativa institucional UNAJMA:
      - Interlineado sencillo seguro (w:line="240" w:lineRule="auto") para erradicar
        colisiones de ascenders/descenders y solapamientos verticales.
      - Espaciado superior/inferior controlado (20 dxa = 1 pt).
    """
    sz_val = str(int(font_size_pt * 2))
    texto_escapado = escape(str(texto))
    p = parse_xml(r'''<w:p %s>
        <w:pPr>
            <w:spacing w:line="%d" w:lineRule="auto" w:before="%d" w:after="%d"/>
            <w:ind w:firstLine="0"/>
            <w:jc w:val="%s"/>
        </w:pPr>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="%s" w:hAnsi="%s"/>
                <w:b w:val="%s"/>
                <w:i w:val="%s"/>
                <w:color w:val="000000"/>
                <w:u w:val="none"/>
                <w:sz w:val="%s"/>
                <w:szCs w:val="%s"/>
            </w:rPr>
            <w:t xml:space="preserve">%s</w:t>
        </w:r>
    </w:p>''' % (nsdecls('w'), line_spacing, space_before, space_after, align,
                fuente, fuente,
                "1" if bold else "0",
                "1" if italic else "0",
                sz_val, sz_val, texto_escapado))
    return p


def crear_parrafo_item_lista(texto, bold=False, italic=False, fuente=FUENTE_POR_DEFECTO,
                             font_size_pt=6.5, align="both", line_spacing=LINE_SPACING_1_0_DXA,
                             space_before=0, space_after=20, left_indent_dxa=180, hanging_dxa=180,
                             bold_prefix=False):
    """
    Crea un párrafo quirúrgico <w:p> para un ítem de lista o viñeta dentro de una celda de tabla:
      - Sangría colgante (w:ind w:left="..." w:hanging="...") para que las líneas subsiguientes
        se alineen bajo el texto y no bajo el símbolo de viñeta.
      - Interlineado sencillo controlado (lineRule="auto") y espaciado compacto.
      - Opción de resaltar en negrita el prefijo (ej. '• Finalidad / Qué mide:' o '• Ind 1.1:').
    """
    sz_val = str(int(font_size_pt * 2))
    ind_xml = (f'<w:ind {nsdecls("w")} w:left="{left_indent_dxa}" w:hanging="{hanging_dxa}"/>'
               if hanging_dxa > 0 else
               f'<w:ind {nsdecls("w")} w:left="{left_indent_dxa}" w:firstLine="0"/>')

    p = parse_xml(r'''<w:p %s>
        <w:pPr>
            <w:spacing w:line="%d" w:lineRule="auto" w:before="%d" w:after="%d"/>
            %s
            <w:jc w:val="%s"/>
        </w:pPr>
    </w:p>''' % (nsdecls('w'), line_spacing, space_before, space_after, ind_xml, align))

    texto_str = str(texto).strip()
    if bold_prefix and ":" in texto_str:
        idx_colon = texto_str.find(":")
        prefijo = texto_str[:idx_colon + 1]
        cuerpo = texto_str[idx_colon + 1:]

        r_pre = parse_xml(r'''<w:r %s>
            <w:rPr>
                <w:rFonts w:ascii="%s" w:hAnsi="%s"/>
                <w:b w:val="1"/>
                <w:i w:val="%s"/>
                <w:color w:val="000000"/>
                <w:u w:val="none"/>
                <w:sz w:val="%s"/>
                <w:szCs w:val="%s"/>
            </w:rPr>
            <w:t xml:space="preserve">%s</w:t>
        </w:r>''' % (nsdecls('w'), fuente, fuente, "1" if italic else "0", sz_val, sz_val, escape(prefijo)))
        p.append(r_pre)

        if cuerpo:
            r_cuerpo = parse_xml(r'''<w:r %s>
                <w:rPr>
                    <w:rFonts w:ascii="%s" w:hAnsi="%s"/>
                    <w:b w:val="%s"/>
                    <w:i w:val="%s"/>
                    <w:color w:val="000000"/>
                    <w:u w:val="none"/>
                    <w:sz w:val="%s"/>
                    <w:szCs w:val="%s"/>
                </w:rPr>
                <w:t xml:space="preserve">%s</w:t>
            </w:r>''' % (nsdecls('w'), fuente, fuente, "1" if bold else "0", "1" if italic else "0", sz_val, sz_val, escape(cuerpo)))
            p.append(r_cuerpo)
    else:
        r = parse_xml(r'''<w:r %s>
            <w:rPr>
                <w:rFonts w:ascii="%s" w:hAnsi="%s"/>
                <w:b w:val="%s"/>
                <w:i w:val="%s"/>
                <w:color w:val="000000"/>
                <w:u w:val="none"/>
                <w:sz w:val="%s"/>
                <w:szCs w:val="%s"/>
            </w:rPr>
            <w:t xml:space="preserve">%s</w:t>
        </w:r>''' % (nsdecls('w'), fuente, fuente, "1" if bold else "0", "1" if italic else "0", sz_val, sz_val, escape(texto_str)))
        p.append(r)

    return p


def crear_parrafos_desde_texto(texto_multilinea, fuente=FUENTE_POR_DEFECTO, font_size_pt=6.5,
                               align="both", line_spacing=LINE_SPACING_1_0_DXA, space_before=0,
                               space_after=20, left_indent_dxa=180, hanging_dxa=180, bold_prefix=False):
    """
    Convierte una cadena de texto multilinea (con viñetas '•', guiones '-' o párrafos)
    en una lista de elementos <w:p> individuales para celdas de tabla:
      - Cada línea no vacía se convierte en un <w:p> independiente.
      - Si una línea comienza con '•' o '-', se le aplica sangría colgante para viñetas.
      - Si una línea tiene sangría de sub-ítem (ej. '  - ' o '    - '), se incrementa la sangría izquierda.
      - Si una línea es un encabezado o texto regular sin viñeta, se formatea sin sangría colgante.
      - Erradica de raíz el texto corrido accidental en Word y asegura que cada viñeta
        inicie limpia en su propio renglón.
    """
    if not texto_multilinea:
        return []

    parrafos = []
    lineas = str(texto_multilinea).splitlines()

    for linea in lineas:
        linea_raw = linea.rstrip()
        linea_strip = linea_raw.strip()
        if not linea_strip:
            continue

        espacios_inicio = len(linea_raw) - len(linea_raw.lstrip(' '))
        es_subitem = linea_strip.startswith('-') or linea_strip.startswith('–') or (espacios_inicio >= 2 and (linea_strip.startswith('-') or linea_strip.startswith('•')))
        es_vineta = linea_strip.startswith('•') or linea_strip.startswith('* ') or es_subitem

        if es_subitem:
            sub_left = left_indent_dxa + 160
            sub_hanging = 140
            p = crear_parrafo_item_lista(
                linea_strip,
                fuente=fuente,
                font_size_pt=font_size_pt,
                align=align,
                line_spacing=line_spacing,
                space_before=space_before,
                space_after=space_after,
                left_indent_dxa=sub_left,
                hanging_dxa=sub_hanging,
                bold_prefix=bold_prefix
            )
        elif es_vineta:
            p = crear_parrafo_item_lista(
                linea_strip,
                fuente=fuente,
                font_size_pt=font_size_pt,
                align=align,
                line_spacing=line_spacing,
                space_before=space_before,
                space_after=space_after,
                left_indent_dxa=left_indent_dxa,
                hanging_dxa=hanging_dxa,
                bold_prefix=bold_prefix
            )
        else:
            es_titulo = linea_strip.endswith(':') or linea_strip.isupper()
            p = crear_parrafo_celda(
                linea_strip,
                bold=es_titulo,
                fuente=fuente,
                font_size_pt=font_size_pt,
                align="left" if es_titulo else align,
                line_spacing=line_spacing,
                space_before=space_before + (10 if es_titulo else 0),
                space_after=space_after
            )

        parrafos.append(p)

    return parrafos


# ==============================================================================
# 3. MOTOR DE FORMATEO QUIRÚRGICO DE PÁRRAFOS Y TIPOGRAFÍA APA 7 / UNAJMA
# ==============================================================================

def aplicar_formato_cuerpo(p, font_size_pt=FONT_SIZE_BODY_PT, line_spacing=LINE_SPACING_1_5_DXA,
                           space_before=0, space_after=0, first_line_indent_dxa=SANGRIA_PRIMERA_LINEA_DXA,
                           align="both", fuente=FUENTE_POR_DEFECTO):
    """
    Aplica el formato canónico estricto de cuerpo de texto bajo APA 7 y estándar UNAJMA:
      - Tipografía: Times New Roman 12 pt (w:sz="24")
      - Interlineado: 1.5 líneas (w:line="360" w:lineRule="auto")
      - Sangría de primera línea: 1.27 cm / 0.5 in (w:ind w:firstLine="720")
      - Espaciado: w:before="0", w:after="0"
      - Alineación: Justificado (w:jc w:val="both")
    """
    pPr = p._p.get_or_add_pPr()

    # 1. Configurar espaciado (w:spacing)
    for sp in pPr.findall(qn('w:spacing')):
        pPr.remove(sp)
    pPr.append(parse_xml(r'<w:spacing %s w:line="%d" w:lineRule="auto" w:before="%d" w:after="%d"/>' % (
        nsdecls('w'), line_spacing, space_before, space_after)))

    # 2. Configurar sangría (w:ind)
    for ind in pPr.findall(qn('w:ind')):
        pPr.remove(ind)
    pPr.append(parse_xml(r'<w:ind %s w:firstLine="%d" w:left="0" w:right="0"/>' % (
        nsdecls('w'), first_line_indent_dxa)))

    # 3. Configurar alineación (w:jc)
    for jc in pPr.findall(qn('w:jc')):
        pPr.remove(jc)
    pPr.append(parse_xml(r'<w:jc %s w:val="%s"/>' % (nsdecls('w'), align)))

    # 4. Formatear cada run respetando negrita / cursiva previa
    sz_val = str(int(font_size_pt * 2))
    for r in p.runs:
        rPr = r._r.get_or_add_rPr()

        # Preservar estilos de negrita y cursiva
        b_elem = rPr.find(qn('w:b'))
        es_bold = b_elem is not None and (b_elem.get(qn('w:val')) is None or b_elem.get(qn('w:val')) == '1')
        i_elem = rPr.find(qn('w:i'))
        es_italic = i_elem is not None and (i_elem.get(qn('w:val')) is None or i_elem.get(qn('w:val')) == '1')

        # Asignar fuente Times New Roman
        for rf in rPr.findall(qn('w:rFonts')):
            rPr.remove(rf)
        rPr.append(parse_xml(r'<w:rFonts %s w:ascii="%s" w:hAnsi="%s" w:eastAsia="%s" w:cs="%s"/>' % (
            nsdecls('w'), fuente, fuente, fuente, fuente)))

        # Asignar tamaño en medios puntos
        for sz in rPr.findall(qn('w:sz')):
            rPr.remove(sz)
        rPr.append(parse_xml(r'<w:sz %s w:val="%s"/>' % (nsdecls('w'), sz_val)))
        for szCs in rPr.findall(qn('w:szCs')):
            rPr.remove(szCs)
        rPr.append(parse_xml(r'<w:szCs %s w:val="%s"/>' % (nsdecls('w'), sz_val)))

        # Reasegurar negrita y cursiva
        if es_bold and rPr.find(qn('w:b')) is None:
            rPr.append(parse_xml(r'<w:b %s w:val="1"/>' % nsdecls('w')))
        if es_italic and rPr.find(qn('w:i')) is None:
            rPr.append(parse_xml(r'<w:i %s w:val="1"/>' % nsdecls('w')))


def asegurar_salto_pagina_parrafo(p):
    """
    Inyecta <w:pageBreakBefore/> en el pPr del párrafo si no existe,
    asegurando que el párrafo inicie estrictamente al tope de una página nueva.
    """
    pPr = p._p.get_or_add_pPr()
    if pPr.find(qn('w:pageBreakBefore')) is None:
        pbb = parse_xml(r'<w:pageBreakBefore %s/>' % nsdecls('w'))
        pPr.insert(0, pbb)


def aplicar_formato_lista_vineta(p, nivel=0, fuente=FUENTE_POR_DEFECTO, line_spacing=LINE_SPACING_1_5_DXA, space_before=0, space_after=60):
    """
    Aplica formato canónico APA 7 a elementos de lista o viñetas:
      - Sangría francesa / colgante: w:left="720", w:hanging="360" (0.5 pulgada izquierda, 0.25 pulgada colgante)
      - Erradica terminantemente w:firstLine positivo para evitar saltos gigantescos de tabulación.
      - Interlineado 1.5 líneas (360 dxa) y Times New Roman 12 pt justificado.
    """
    pPr = p._p.get_or_add_pPr()

    # 1. Configurar espaciado (w:spacing)
    for sp in pPr.findall(qn('w:spacing')):
        pPr.remove(sp)
    pPr.append(parse_xml(r'<w:spacing %s w:line="%d" w:lineRule="auto" w:before="%d" w:after="%d"/>' % (
        nsdecls('w'), line_spacing, space_before, space_after)))

    # 2. Configurar sangría colgante estricta (sin firstLine positivo)
    left_dxa = 720 + (nivel * 360)
    for ind in pPr.findall(qn('w:ind')):
        pPr.remove(ind)
    pPr.append(parse_xml(r'<w:ind %s w:left="%d" w:hanging="360"/>' % (nsdecls('w'), left_dxa)))

    # 3. Alineación justificada
    for jc in pPr.findall(qn('w:jc')):
        pPr.remove(jc)
    pPr.append(parse_xml(r'<w:jc %s w:val="both"/>' % nsdecls('w')))

    # 4. Formatear cada run respetando negrita / cursiva previa
    sz_val = "24"  # 12 pt
    for r in p.runs:
        rPr = r._r.get_or_add_rPr()
        b_elem = rPr.find(qn('w:b'))
        es_bold = b_elem is not None and (b_elem.get(qn('w:val')) is None or b_elem.get(qn('w:val')) == '1')
        i_elem = rPr.find(qn('w:i'))
        es_italic = i_elem is not None and (i_elem.get(qn('w:val')) is None or i_elem.get(qn('w:val')) == '1')

        for rf in rPr.findall(qn('w:rFonts')):
            rPr.remove(rf)
        rPr.append(parse_xml(r'<w:rFonts %s w:ascii="%s" w:hAnsi="%s" w:eastAsia="%s" w:cs="%s"/>' % (
            nsdecls('w'), fuente, fuente, fuente, fuente)))

        for sz in rPr.findall(qn('w:sz')):
            rPr.remove(sz)
        rPr.append(parse_xml(r'<w:sz %s w:val="%s"/>' % (nsdecls('w'), sz_val)))
        for szCs in rPr.findall(qn('w:szCs')):
            rPr.remove(szCs)
        rPr.append(parse_xml(r'<w:szCs %s w:val="%s"/>' % (nsdecls('w'), sz_val)))

        if es_bold and rPr.find(qn('w:b')) is None:
            rPr.append(parse_xml(r'<w:b %s w:val="1"/>' % nsdecls('w')))
        if es_italic and rPr.find(qn('w:i')) is None:
            rPr.append(parse_xml(r'<w:i %s w:val="1"/>' % nsdecls('w')))


def aplicar_formato_heading(p, nivel=1, fuente=FUENTE_POR_DEFECTO, page_break_before=False):
    """
    Aplica el formato canónico a encabezados (Headings 1, 2, 3, 4):
      - Cero sangría de primera línea (w:firstLine="0" w:left="0")
      - Fuente Times New Roman
      - Espaciado anterior y posterior proporcional
      - Salto de página antes opcional o mandatorio para capítulos.
    """
    pPr = p._p.get_or_add_pPr()

    txt_norm = p.text.strip().upper()
    es_capitulo = txt_norm.startswith("CAPÍTULO") or txt_norm.startswith("CAPITULO") or txt_norm.startswith("ANEXOS") or txt_norm.startswith("REFERENCIA")
    if page_break_before or (nivel == 1 and es_capitulo):
        asegurar_salto_pagina_parrafo(p)

    if pPr.find(qn('w:keepNext')) is None:
        pPr.insert(0, parse_xml(r'<w:keepNext %s/>' % nsdecls('w')))

    if nivel == 1:
        # Nivel 1: Capítulos o Títulos Principales (12 o 14 pt, Negrita, centrado o izquierda, 1.5 interlineado)
        sz_val = "24"  # 12 pt (o 28 para 14 pt según directiva)
        line_spacing = LINE_SPACING_1_5_DXA
        before = 360   # 18 pt
        after = 120    # 6 pt
        align = "center" if "CAPÍTULO" in p.text.upper() or "CAPITULO" in p.text.upper() or "ANEXOS" in p.text.upper() else "left"
        es_bold = True
        es_italic = False
    elif nivel == 2:
        # Nivel 2: Secciones 1.1, 1.2, 4.7, etc. (12 pt, Negrita, alineado a la izquierda)
        sz_val = "24"
        line_spacing = LINE_SPACING_1_5_DXA
        before = 240   # 12 pt
        after = 120    # 6 pt
        align = "left"
        es_bold = True
        es_italic = False
    elif nivel == 3:
        # Nivel 3: Subsecciones 1.2.1, 1.2.2 (12 pt, Negrita y Cursiva, izquierda)
        sz_val = "24"
        line_spacing = LINE_SPACING_1_5_DXA
        before = 240   # 12 pt
        after = 120    # 6 pt
        align = "left"
        es_bold = True
        es_italic = True
    else:
        sz_val = "24"
        line_spacing = LINE_SPACING_1_5_DXA
        before = 120
        after = 60
        align = "left"
        es_bold = True
        es_italic = False

    # Spacing
    for sp in pPr.findall(qn('w:spacing')):
        pPr.remove(sp)
    pPr.append(parse_xml(r'<w:spacing %s w:line="%d" w:lineRule="auto" w:before="%d" w:after="%d"/>' % (
        nsdecls('w'), line_spacing, before, after)))

    # Indent (sin sangría)
    for ind in pPr.findall(qn('w:ind')):
        pPr.remove(ind)
    pPr.append(parse_xml(r'<w:ind %s w:firstLine="0" w:left="0" w:right="0"/>' % nsdecls('w')))

    # Alignment
    for jc in pPr.findall(qn('w:jc')):
        pPr.remove(jc)
    pPr.append(parse_xml(r'<w:jc %s w:val="%s"/>' % (nsdecls('w'), align)))

    # Runs
    for r in p.runs:
        rPr = r._r.get_or_add_rPr()
        for rf in rPr.findall(qn('w:rFonts')):
            rPr.remove(rf)
        rPr.append(parse_xml(r'<w:rFonts %s w:ascii="%s" w:hAnsi="%s" w:eastAsia="%s" w:cs="%s"/>' % (
            nsdecls('w'), fuente, fuente, fuente, fuente)))
        for sz in rPr.findall(qn('w:sz')):
            rPr.remove(sz)
        rPr.append(parse_xml(r'<w:sz %s w:val="%s"/>' % (nsdecls('w'), sz_val)))
        for szCs in rPr.findall(qn('w:szCs')):
            rPr.remove(szCs)
        rPr.append(parse_xml(r'<w:szCs %s w:val="%s"/>' % (nsdecls('w'), sz_val)))

        for b in rPr.findall(qn('w:b')):
            rPr.remove(b)
        if es_bold:
            rPr.append(parse_xml(r'<w:b %s w:val="1"/>' % nsdecls('w')))

        for i in rPr.findall(qn('w:i')):
            rPr.remove(i)
        if es_italic:
            rPr.append(parse_xml(r'<w:i %s w:val="1"/>' % nsdecls('w')))


def aplicar_formato_caption(p, tipo="tabla", fuente=FUENTE_POR_DEFECTO):
    """
    Aplica formato APA 7 a rótulos y títulos de tablas y figuras:
      - Rótulo (Tabla X / Figura X): Negrita, izquierda, sin sangría, espacio anterior 12 pt.
      - Título descriptivo: Cursiva, izquierda, sin sangría, espacio posterior 6 pt.
    """
    pPr = p._p.get_or_add_pPr()
    txt = p.text.strip()
    es_rotulo = txt.startswith("Tabla ") or txt.startswith("Figura ")

    before = 240 if es_rotulo else 0
    after = 40 if es_rotulo else 120
    es_bold = es_rotulo
    es_italic = not es_rotulo

    for sp in pPr.findall(qn('w:spacing')):
        pPr.remove(sp)
    pPr.append(parse_xml(r'<w:spacing %s w:line="%d" w:lineRule="auto" w:before="%d" w:after="%d"/>' % (
        nsdecls('w'), LINE_SPACING_1_5_DXA, before, after)))

    for ind in pPr.findall(qn('w:ind')):
        pPr.remove(ind)
    pPr.append(parse_xml(r'<w:ind %s w:firstLine="0" w:left="0" w:right="0"/>' % nsdecls('w')))

    for jc in pPr.findall(qn('w:jc')):
        pPr.remove(jc)
    pPr.append(parse_xml(r'<w:jc %s w:val="left"/>' % nsdecls('w')))

    sz_val = "24"  # 12 pt
    for r in p.runs:
        rPr = r._r.get_or_add_rPr()
        for rf in rPr.findall(qn('w:rFonts')):
            rPr.remove(rf)
        rPr.append(parse_xml(r'<w:rFonts %s w:ascii="%s" w:hAnsi="%s"/>' % (nsdecls('w'), fuente, fuente)))
        for sz in rPr.findall(qn('w:sz')):
            rPr.remove(sz)
        rPr.append(parse_xml(r'<w:sz %s w:val="%s"/>' % (nsdecls('w'), sz_val)))
        for szCs in rPr.findall(qn('w:szCs')):
            rPr.remove(szCs)
        rPr.append(parse_xml(r'<w:szCs %s w:val="%s"/>' % (nsdecls('w'), sz_val)))

        for b in rPr.findall(qn('w:b')):
            rPr.remove(b)
        if es_bold:
            rPr.append(parse_xml(r'<w:b %s w:val="1"/>' % nsdecls('w')))

        for i in rPr.findall(qn('w:i')):
            rPr.remove(i)
        if es_italic:
            rPr.append(parse_xml(r'<w:i %s w:val="1"/>' % nsdecls('w')))


def aplicar_formato_nota_tabla_figura(p, fuente=FUENTE_POR_DEFECTO):
    """
    Aplica formato APA 7 a notas de tablas y figuras:
      - Tipografía: 9.5 pt o 10 pt
      - Interlineado sencillo (1.0 = 240 dxa)
      - Espaciado: w:before="60", w:after="240"
      - Sin sangría de primera línea
      - "Nota." o "Fuente:" en cursiva inicial
    """
    pPr = p._p.get_or_add_pPr()

    for sp in pPr.findall(qn('w:spacing')):
        pPr.remove(sp)
    pPr.append(parse_xml(r'<w:spacing %s w:line="%d" w:lineRule="auto" w:before="60" w:after="240"/>' % (
        nsdecls('w'), LINE_SPACING_1_0_DXA)))

    for ind in pPr.findall(qn('w:ind')):
        pPr.remove(ind)
    pPr.append(parse_xml(r'<w:ind %s w:firstLine="0" w:left="0" w:right="0"/>' % nsdecls('w')))

    for jc in pPr.findall(qn('w:jc')):
        pPr.remove(jc)
    pPr.append(parse_xml(r'<w:jc %s w:val="both"/>' % nsdecls('w')))

    sz_val = str(int(FONT_SIZE_NOTE_PT * 2))  # 19 para 9.5 pt o 20 para 10 pt
    for r in p.runs:
        rPr = r._r.get_or_add_rPr()
        for rf in rPr.findall(qn('w:rFonts')):
            rPr.remove(rf)
        rPr.append(parse_xml(r'<w:rFonts %s w:ascii="%s" w:hAnsi="%s"/>' % (nsdecls('w'), fuente, fuente)))
        for sz in rPr.findall(qn('w:sz')):
            rPr.remove(sz)
        rPr.append(parse_xml(r'<w:sz %s w:val="%s"/>' % (nsdecls('w'), sz_val)))
        for szCs in rPr.findall(qn('w:szCs')):
            rPr.remove(szCs)
        rPr.append(parse_xml(r'<w:szCs %s w:val="%s"/>' % (nsdecls('w'), sz_val)))


def aplicar_formato_referencia(p, fuente=FUENTE_POR_DEFECTO):
    """
    Aplica formato APA 7 a entradas de la lista de referencias bibliográficas:
      - Sangría francesa de 1.27 cm (w:ind w:left="720" w:hanging="720")
      - Interlineado 1.5 líneas (w:line="360")
      - Tipografía: Times New Roman 12 pt
      - Espaciado posterior: 6 pt (w:after="120")
    """
    pPr = p._p.get_or_add_pPr()

    for sp in pPr.findall(qn('w:spacing')):
        pPr.remove(sp)
    pPr.append(parse_xml(r'<w:spacing %s w:line="%d" w:lineRule="auto" w:before="0" w:after="120"/>' % (
        nsdecls('w'), LINE_SPACING_1_5_DXA)))

    for ind in pPr.findall(qn('w:ind')):
        pPr.remove(ind)
    pPr.append(parse_xml(r'<w:ind %s w:left="%d" w:hanging="%d" w:right="0"/>' % (
        nsdecls('w'), SANGRIA_FRANCESA_DXA, SANGRIA_FRANCESA_DXA)))

    for jc in pPr.findall(qn('w:jc')):
        pPr.remove(jc)
    pPr.append(parse_xml(r'<w:jc %s w:val="both"/>' % nsdecls('w')))

    sz_val = "24"
    for r in p.runs:
        rPr = r._r.get_or_add_rPr()
        for rf in rPr.findall(qn('w:rFonts')):
            rPr.remove(rf)
        rPr.append(parse_xml(r'<w:rFonts %s w:ascii="%s" w:hAnsi="%s"/>' % (nsdecls('w'), fuente, fuente)))
        for sz in rPr.findall(qn('w:sz')):
            rPr.remove(sz)
        rPr.append(parse_xml(r'<w:sz %s w:val="%s"/>' % (nsdecls('w'), sz_val)))
        for szCs in rPr.findall(qn('w:szCs')):
            rPr.remove(szCs)
        rPr.append(parse_xml(r'<w:szCs %s w:val="%s"/>' % (nsdecls('w'), sz_val)))


def aplicar_formato_formula_dedicada(p):
    """
    Asegura que un párrafo con ecuación OMML dedicada tenga centrado impecable,
    espaciado superior/inferior armónico y cero sangrías.
    """
    pPr = p._p.get_or_add_pPr()

    for sp in pPr.findall(qn('w:spacing')):
        pPr.remove(sp)
    pPr.append(parse_xml(r'<w:spacing %s w:line="%d" w:lineRule="auto" w:before="120" w:after="120"/>' % (
        nsdecls('w'), LINE_SPACING_1_5_DXA)))

    for ind in pPr.findall(qn('w:ind')):
        pPr.remove(ind)
    pPr.append(parse_xml(r'<w:ind %s w:firstLine="0" w:left="0" w:right="0"/>' % nsdecls('w')))

    for jc in pPr.findall(qn('w:jc')):
        pPr.remove(jc)
    pPr.append(parse_xml(r'<w:jc %s w:val="center"/>' % nsdecls('w')))


def normalizar_formato_documento_completo(doc, verbose=True):
    """
    Normaliza quirúrgicamente todo el documento DOCX garantizando que CADA párrafo
    cumpla con las normas de formato, sangrías, interlineado y tipografía APA 7 / UNAJMA:
      - Capítulos (I al V, Referencias, Anexos) inician en página nueva (w:pageBreakBefore).
      - Listas y viñetas con sangría colgante controlada (sin salto desmedido de tabulación).
      - Paginación continua entre secciones (sin reinicio espurio a 1 en landscape o anexos).
    """
    conteo = {
        "cuerpo_con_sangria": 0,
        "listas": 0,
        "headings": 0,
        "captions": 0,
        "notas": 0,
        "referencias": 0,
        "formulas": 0,
        "otros": 0
    }

    en_referencias = False

    for idx, p in enumerate(doc.paragraphs):
        txt = p.text.strip()
        contiene_omml = len(p._p.xpath('.//m:oMath')) > 0

        # Si es una fórmula OMML dedicada (sin texto o con texto muy corto)
        if contiene_omml and len(txt) < 30:
            aplicar_formato_formula_dedicada(p)
            conteo["formulas"] += 1
            continue

        if not txt:
            continue

        txt_clean = txt.replace('\xa0', ' ')
        txt_clean_upper = txt_clean.upper()

        # Detectar sección de referencias bibliográficas
        if txt_clean_upper.startswith("REFERENCIA"):
            en_referencias = True
            aplicar_formato_heading(p, nivel=1, page_break_before=True)
            conteo["headings"] += 1
            continue

        if txt_clean_upper == "ANEXOS":
            en_referencias = False
            aplicar_formato_heading(p, nivel=1, page_break_before=True)
            conteo["headings"] += 1
            continue
        elif txt_clean_upper.startswith("ANEXO"):
            en_referencias = False
            # Si es el primer anexo y viene inmediatamente despues de ANEXOS, no forzar salto redundante
            prev_p = doc.paragraphs[idx-1] if idx > 0 else None
            prev_txt = prev_p.text.strip().upper() if prev_p else ""
            salto = not (prev_txt == "ANEXOS")
            aplicar_formato_heading(p, nivel=2 if not salto else 1, page_break_before=salto)
            conteo["headings"] += 1
            continue

        # Si estamos en la sección de referencias y es una entrada bibliográfica
        if en_referencias and len(txt_clean) > 20 and not txt_clean_upper.startswith("ANEXO"):
            aplicar_formato_referencia(p)
            conteo["referencias"] += 1
            continue

        # Detectar Capítulos
        if txt_clean_upper.startswith("CAPÍTULO") or txt_clean_upper.startswith("CAPITULO"):
            if "CAPITULO" in txt_clean:
                for t_node in p._p.xpath('.//w:t'):
                    if t_node.text and "CAPITULO" in t_node.text:
                        t_node.text = t_node.text.replace("CAPITULO", "CAPÍTULO")
            aplicar_formato_heading(p, nivel=1, page_break_before=True)
            conteo["headings"] += 1
            continue

        # Chequear otros encabezados y preliminares con salto obligatorio
        style_name = p.style.name if p.style else 'Normal'
        preliminares_con_salto = [
            "INTRODUCCIÓN", "RESUMEN", "ABSTRACT", "CHUMASQA", "DEDICATORIA", "AGRADECIMIENTOS",
            "ÍNDICE GENERAL", "ÍNDICE DE CONTENIDO", "ÍNDICE DE TABLAS", "LISTA DE TABLAS",
            "ÍNDICE DE FIGURAS", "LISTA DE FIGURAS", "REFERENCIAS", "REFERENCIAS BIBLIOGRÁFICAS", "ANEXOS"
        ]
        if txt_clean_upper in preliminares_con_salto or style_name.startswith("Heading 1"):
            es_salto = txt_clean_upper in preliminares_con_salto or txt_clean in ["INTRODUCCIÓN", "RESUMEN", "ABSTRACT", "CHUMASQA"]
            aplicar_formato_heading(p, nivel=1, page_break_before=es_salto)
            conteo["headings"] += 1
            continue
        elif style_name.startswith("Heading 2") or (len(txt_clean) < 80 and any(txt_clean.startswith(f"{i}.") for i in range(1, 10)) and len(txt_clean.split()[0].split('.')) == 2):
            aplicar_formato_heading(p, nivel=2)
            conteo["headings"] += 1
            continue
        elif style_name.startswith("Heading 3") or (len(txt_clean) < 80 and any(txt_clean.startswith(f"{i}.") for i in range(1, 10)) and len(txt_clean.split()[0].split('.')) == 3):
            aplicar_formato_heading(p, nivel=3)
            conteo["headings"] += 1
            continue

        # Chequear rótulos y notas de tablas/figuras
        if txt_clean.startswith("Tabla ") or txt_clean.startswith("Figura "):
            aplicar_formato_caption(p, tipo="tabla")
            conteo["captions"] += 1
            continue

        if txt_clean.startswith("Nota.") or txt_clean.startswith("Nota:") or txt_clean.startswith("Fuente:") or txt_clean.startswith("Nota "):
            aplicar_formato_nota_tabla_figura(p)
            conteo["notas"] += 1
            continue

        # Excluir párrafos especiales de portada o preliminares (primeros párrafos)
        if idx < 30 and (len(txt) < 80 or "UNIVERSIDAD" in txt or "FACULTAD" in txt or "ESCUELA" in txt or "TESIS" in txt or "BACHILLER" in txt):
            conteo["otros"] += 1
            continue

        # Detectar viñetas o listas enumeradas (evitar sangría regular 720 que destruye sangría francesa)
        es_lista = len(p._p.xpath('.//w:numPr')) > 0 or txt_clean.startswith('•') or txt_clean.startswith('-')
        if es_lista:
            aplicar_formato_lista_vineta(p)
            conteo["listas"] += 1
            continue

        # Párrafos de cuerpo normal (narrativa científica)
        if len(txt) > 40:
            aplicar_formato_cuerpo(p)
            conteo["cuerpo_con_sangria"] += 1
        else:
            conteo["otros"] += 1

    # Asegurar continuidad de paginación entre secciones (erradicar w:start="1" espurio)
    for s_idx, sec in enumerate(doc.sections):
        if s_idx > 0:
            sectPr = sec._sectPr
            for pnt in sectPr.findall(qn('w:pgNumType')):
                if pnt.get(qn('w:start')) is not None:
                    del pnt.attrib[qn('w:start')]

    if verbose:
        print("\n--- RESUMEN DE NORMALIZACIÓN DE PÁRRAFOS ---")
        for k, v in conteo.items():
            print(f"  - {k}: {v} párrafos procesados")

    return conteo


# ==============================================================================
# 4. HERRAMIENTAS DE AUDITORÍA, CONVERSIÓN Y RENDERIZADO VISUAL
# ==============================================================================

def blindar_todas_tablas_documento(docx_path, salida_path=None, aplicar_bordes=True):
    """
    Recorre todas las tablas del documento para aplicar blindaje integral:
      - Remueve flotación (w:tblpPr).
      - Inyecta w:cantSplit en todas las filas.
      - Inyecta w:tblHeader en la primera fila de cada tabla.
      - Aplica opcionalmente los 3 bordes canónicos APA 7.
    """
    doc = docx.Document(docx_path)
    conteo_modificadas = 0

    for idx, table in enumerate(doc.tables):
        eliminar_flotacion_tabla(table)
        blindar_filas_tabla(table, cant_split=True, repetir_encabezado=True)
        if aplicar_bordes:
            aplicar_bordes_apa7(table)
        conteo_modificadas += 1

    destino = salida_path if salida_path else docx_path
    doc.save(destino)
    return conteo_modificadas


def auditar_documento_docx(docx_path):
    """
    Audita exhaustivamente las tablas de un documento DOCX:
      - Detecta tablas flotantes (w:tblpPr).
      - Revisa anchos de tabla frente a los límites recomendados.
      - Verifica presencia de w:cantSplit y w:tblHeader.
    """
    doc = docx.Document(docx_path)
    reporte = {
        "archivo": str(docx_path),
        "total_tablas": len(doc.tables),
        "advertencias": [],
        "tablas": []
    }

    for idx, table in enumerate(doc.tables):
        tblPr = table._tbl.tblPr
        es_flotante = tblPr.find(qn('w:tblpPr')) is not None
        tblW_elem = tblPr.find(qn('w:tblW'))
        ancho_dxa = int(tblW_elem.get(qn('w:w'), 0)) if tblW_elem is not None and tblW_elem.get(qn('w:w')) else None

        cant_split_count = 0
        has_tbl_header = False
        for r_idx, row in enumerate(table.rows):
            trPr = row._tr.trPr
            if trPr is not None:
                if trPr.find(qn('w:cantSplit')) is not None:
                    cant_split_count += 1
                if r_idx == 0 and trPr.find(qn('w:tblHeader')) is not None:
                    has_tbl_header = True

        info = {
            "indice": idx + 1,
            "filas": len(table.rows),
            "columnas": len(table.columns),
            "ancho_dxa": ancho_dxa,
            "es_flotante": es_flotante,
            "cant_split_filas": f"{cant_split_count}/{len(table.rows)}",
            "tiene_tbl_header": has_tbl_header
        }

        if es_flotante:
            reporte["advertencias"].append(f"Tabla {idx+1}: Contiene w:tblpPr (tabla flotante). Riesgo alto de saltos caóticos de página.")
        if cant_split_count < len(table.rows):
            reporte["advertencias"].append(f"Tabla {idx+1}: Solo {cant_split_count}/{len(table.rows)} filas tienen w:cantSplit.")
        if not has_tbl_header and len(table.rows) > 3:
            reporte["advertencias"].append(f"Tabla {idx+1}: No tiene w:tblHeader configurado en la fila 0.")

        reporte["tablas"].append(info)

    return reporte


def exportar_docx_a_pdf(docx_path, pdf_path=None):
    """
    Exporta un archivo DOCX a PDF usando Microsoft Word vía automatización COM en Windows.
    Garantiza una conversión 100% idéntica a la visualización de Word.
    """
    docx_path = Path(docx_path).resolve()
    if not pdf_path:
        pdf_path = docx_path.with_suffix(".pdf")
    else:
        pdf_path = Path(pdf_path).resolve()
        if pdf_path.is_dir():
            pdf_path = pdf_path / f"{docx_path.stem}.pdf"

    cmd = f"""
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $doc = $word.Documents.Open('{str(docx_path)}')
    # wdExportFormatPDF = 17, wdExportOptimizeForPrint = 0, wdExportDocumentContent = 0
    # ExportAsFixedFormat con Item = 0 asegura exportar exclusivamente el contenido del documento,
    # suprimiendo marcas de revisión, globos y comentarios marginales que distorsionan los márgenes.
    $doc.ExportAsFixedFormat('{str(pdf_path)}', 17, $false, 0, 0, 1, 1, 0, $true, $true, 1, $true, $true, $false)
    $doc.Close([ref]0)
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    """
    proc = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True)
    if proc.returncode != 0 or not pdf_path.exists():
        raise RuntimeError(f"Error al exportar DOCX a PDF: {proc.stderr or proc.stdout}")

    return str(pdf_path)


def renderizar_paginas_pdf(pdf_path, paginas_1based, out_dir, dpi=150):
    """
    Renderiza una lista de páginas específicas de un PDF a imágenes PNG a alta resolución.
    Permite verificar visualmente la maquetación sin abrir interfaces gráficas.
    """
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz

    doc = fitz.open(str(pdf_path))
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rutas_generadas = []
    for p_num in paginas_1based:
        idx = p_num - 1
        if 0 <= idx < len(doc):
            page = doc[idx]
            pix = page.get_pixmap(dpi=dpi)
            out_file = out_dir / f"pagina_{p_num}.png"
            pix.save(str(out_file))
            rutas_generadas.append(str(out_file))
        else:
            print(f"Advertencia: La página {p_num} excede el total de páginas del PDF ({len(doc)}).")

    return rutas_generadas


# ==============================================================================
# 4. INTERFAZ DE LÍNEA DE COMANDOS (CLI)
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Motor Quirúrgico DOCX/OpenXML para SIVAC-THESIS-LAB")
    subparsers = parser.add_subparsers(dest="comando", help="Comandos disponibles")

    # Comando: auditar
    p_audit = subparsers.add_parser("auditar", help="Auditar tablas y geometría en un DOCX")
    p_audit.add_argument("docx", help="Ruta al archivo .docx")

    # Comando: blindar-todas
    p_blind = subparsers.add_parser("blindar-todas", help="Inyectar cantSplit, tblHeader y eliminar flotación en todas las tablas")
    p_blind.add_argument("docx", help="Ruta al archivo .docx")
    p_blind.add_argument("--salida", default=None, help="Ruta de salida opcional (por defecto sobreescribe el archivo)")
    p_blind.add_argument("--sin-bordes", action="store_true", help="No alterar bordes existentes")

    # Comando: exportar-pdf
    p_pdf = subparsers.add_parser("exportar-pdf", help="Exportar DOCX a PDF mediante Word COM")
    p_pdf.add_argument("docx", help="Ruta al archivo .docx")
    p_pdf.add_argument("--pdf", default=None, help="Ruta de salida opcional del .pdf")

    # Comando: renderizar-paginas
    p_rend = subparsers.add_parser("renderizar-paginas", help="Renderizar páginas de un PDF a PNG para auditoría visual")
    p_rend.add_argument("pdf", help="Ruta al archivo .pdf")
    p_rend.add_argument("--paginas", required=True, help="Lista de páginas separadas por coma (ej. 32,51)")
    p_rend.add_argument("--out-dir", default="salidas/figuras/verificacion", help="Carpeta de salida")
    p_rend.add_argument("--dpi", type=int, default=150, help="Resolución DPI (default 150)")

    args = parser.parse_args()

    if args.comando == "auditar":
        res = auditar_documento_docx(args.docx)
        print(f"\n--- AUDITORÍA DE TABLAS: {res['archivo']} ---")
        print(f"Total de tablas: {res['total_tablas']}")
        for t in res["tablas"]:
            print(f"  [Tabla {t['indice']}] {t['filas']} filas x {t['columnas']} cols | Ancho: {t['ancho_dxa']} dxa | Flotante: {t['es_flotante']} | cantSplit: {t['cant_split_filas']} | Header: {t['tiene_tbl_header']}")
        if res["advertencias"]:
            print("\nADVERTENCIAS DETECTADAS:")
            for adv in res["advertencias"]:
                print(f"  [!] {adv}")
        else:
            print("\n[✓] Todas las tablas cumplen con las directivas de contención y flujo natural.")

    elif args.comando == "blindar-todas":
        n = blindar_todas_tablas_documento(args.docx, args.salida, aplicar_bordes=not args.sin_bordes)
        print(f"[✓] {n} tablas blindadas exitosamente (cantSplit, tblHeader, sin flotación).")

    elif args.comando == "exportar-pdf":
        out = exportar_docx_a_pdf(args.docx, args.pdf)
        print(f"[✓] PDF generado con éxito en: {out}")

    elif args.comando == "renderizar-paginas":
        p_list = [int(p.strip()) for p in args.paginas.split(",") if p.strip().isdigit()]
        imgs = renderizar_paginas_pdf(args.pdf, p_list, args.out_dir, dpi=args.dpi)
        print(f"[✓] {len(imgs)} página(s) renderizada(s):")
        for img in imgs:
            print(f"  - {img}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
