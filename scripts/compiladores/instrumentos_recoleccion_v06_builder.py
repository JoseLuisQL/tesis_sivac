# -*- coding: utf-8 -*-
"""Constructor de los instrumentos definitivos SIVAC v06.

Compila el paquete editorial ``INSTRUMENTOS_DEFINITIVOS_v06`` a partir del
builder v05, sin tocar ni un archivo de la versión anterior. Los cambios
autorizados para v06 son tres:

1. Renumeración por orden metodológico (DEC-007): 01 ficha de tiempos,
   02 ficha documental, 03 cuestionario de satisfacción, 04 consentimiento
   informado, 05 certificado de validación y 00 guía de aplicación. El
   contenido, la redacción y los ítems de cada instrumento se conservan.
2. Erradicación de líneas verticales: ningún ``w:tblBorders`` lleva ``w:left``,
   ``w:right`` ni ``w:insideV``. Se conservan el borde superior, los separadores
   horizontales internos y el borde inferior; la fila de encabezado recibe un
   separador horizontal propio.
3. Comodidad de llenado: filas de captura de 1.0 cm como mínimo donde la
   geometría lo permite, leyenda compacta de cinco celdas en el cuestionario y
   reequilibrio de la mancha para cerrar entre 0.8 y 3.0 cm de holgura inferior.

Geometría común (idéntica a v05)
--------------------------------
* A4 vertical 11906 x 16838 dxa. Márgenes: izquierdo 1701 dxa (3.0 cm);
  superior 1701 dxa (3.0 cm); derecho e inferior 1417 dxa (2.5 cm). Ancho útil
  8788 dxa.
* Times New Roman 10 pt en el cuerpo y 9.5 pt en las tablas. Ninguna fuente
  por debajo de 9.5 pt.
* Banda institucional nativa en ``word/header1.xml``: 2.4 + 10.7 + 2.4 cm,
  altura de fila exacta 2.0 cm y logotipos de 1.6 cm.
* Cero OMML, cero tablas flotantes y cero códigos internos visibles.

Uso
---
    python scripts/compiladores/instrumentos_recoleccion_v06_builder.py
    python scripts/compiladores/instrumentos_recoleccion_v06_builder.py --solo 02
    python scripts/compiladores/instrumentos_recoleccion_v06_builder.py --sin-pdf
"""

from __future__ import annotations

import argparse
import hashlib
import os
import json
import re
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Sequence, Tuple

from docx import Document
from docx.enum.table import (WD_CELL_VERTICAL_ALIGNMENT,
                             WD_ROW_HEIGHT_RULE, WD_TABLE_ALIGNMENT)
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, Twips

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from scripts.utilidades import docx_quirurgico as dq  # noqa: E402

BASE = RAIZ / "salidas" / "instrumentos" / "INSTRUMENTOS_DEFINITIVOS_v06"
DIR_IMPRIMIBLES = BASE / "01_IMPRIMIBLES"
DIR_EDITABLES = BASE / "02_EDITABLES"
DIR_FUENTES = BASE / "03_FUENTES"
DIR_CONTROL = BASE / "04_CONTROL_VISUAL"
DIR_ANTES = DIR_CONTROL / "antes_v06"

BASE_V05 = RAIZ / "salidas" / "instrumentos" / "INSTRUMENTOS_DEFINITIVOS_v05"
CONTROL_V05 = BASE_V05 / "_control_visual"

ASSETS_V03 = (RAIZ / "salidas" / "instrumentos" /
              "INSTRUMENTOS_REDISENADOS_FANY_20261102_v03" / "_assets")
LOGO_UNAJMA = ASSETS_V03 / "LOGO-UNAJMA-recorte.png"
LOGO_EPIS = ASSETS_V03 / "LOGO-EPIS.jpg"

ANCHO_DXA = 8788          # 15.5 cm
DXA_CM = 567.0            # twips por centímetro
SP = 20                   # 10.0 pt en medios puntos
SP_TABLA = 19             # 9.5 pt en medios puntos
MARGEN_LR = 57            # 1 mm lateral
MARGEN_TB = 28            # 0.5 mm vertical
ESP_ANTES = 8.0           # aire anterior de rótulos
ESP_DESPUES = 3.0         # aire posterior de rótulos
BANDA_ALTO_CM = 2.0       # altura exacta de la banda del encabezado
LOGO_ALTO_CM = 1.6        # altura exacta de cada logotipo
BANDA_ANCHOS_CM = (2.4, 10.7, 2.4)

# Alturas de captura: mínimo cómodo para escritura manual.
ALTO_CAPTURA = 1.0
ALTO_CAPTURA_HOLGADO = 1.05

INTERLINEA = {"00": 11.0, "01": 12.0, "02": 12.0, "03": 12.0,
              "04": 12.0, "05": 10.5}

ALINEACION = {
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
    "center": WD_ALIGN_PARAGRAPH.CENTER,
    "both": WD_ALIGN_PARAGRAPH.JUSTIFY,
}

_TOKEN = re.compile(r"(\*\*.+?\*\*)")
_MARCA_CAJA = re.compile(r"(☐)")
_CODIGOS_PROHIBIDOS = ("AP-0", "UP-0", "REG-", "VALE-", "OP-")

_ESTADO: Dict[str, Any] = {"hdr": [], "capturas": [], "capturas_libres": []}


# ---------------------------------------------------------------------------
# Texto y párrafos
# ---------------------------------------------------------------------------

def _set_run(run, size: int, bold: bool = False, italic: bool = False,
             font: str = "Times New Roman") -> None:
    run.font.name = font
    run.font.size = Pt(size / 2)
    run.bold = bold
    run.italic = italic
    rpr = run._r.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for atributo in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(atributo), font)


def _desactivar_rejilla(parrafo) -> None:
    """Añade ``<w:snapToGrid w:val="0"/>`` al párrafo en el orden de CT_PPr."""
    pPr = parrafo._p.get_or_add_pPr()
    nodo = pPr.find(qn("w:snapToGrid"))
    if nodo is None:
        nodo = OxmlElement("w:snapToGrid")
        pPr.insert_element_before(
            nodo, "w:spacing", "w:ind", "w:contextualSpacing",
            "w:mirrorIndents", "w:suppressOverlap", "w:jc",
            "w:textDirection", "w:textAlignment", "w:textboxTightWrap",
            "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr",
            "w:sectPr", "w:pPrChange",
        )
    nodo.set(qn("w:val"), "0")


def add_runs(parrafo, texto: str, size: int = SP, bold: bool = False,
             italic: bool = False) -> None:
    """Escribe texto con marcas ``**negrita**`` y cajas de marcado.

    Las secuencias de guiones bajos son líneas de relleno: no se interpretan
    como énfasis y se conservan íntegras.
    """
    if not texto:
        return
    for parte in _TOKEN.split(texto):
        if not parte:
            continue
        negrita = bold
        limpio = parte
        if parte.startswith("**") and parte.endswith("**") and len(parte) > 4:
            limpio, negrita = parte[2:-2], True
        for trozo in _MARCA_CAJA.split(limpio):
            if not trozo:
                continue
            run = parrafo.add_run(trozo)
            if trozo == "☐":
                _set_run(run, size, bold=negrita, italic=italic,
                         font="Segoe UI Symbol")
            else:
                _set_run(run, size, bold=negrita, italic=italic)


def par(doc, texto: str = "", size: int = SP, bold: bool = False,
        italic: bool = False, align: str = "left", before: float = 0,
        after: float = 0, line: float = 12.0, left: float = 0,
        first: float = 0, keep: bool = False, keep_lines: bool = False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = Pt(line)
    pf.alignment = ALINEACION[align]
    if left:
        pf.left_indent = Cm(left)
    if first:
        pf.first_line_indent = Cm(first)
    pf.keep_with_next = keep
    pf.keep_together = keep_lines
    pf.widow_control = True
    if texto:
        add_runs(p, texto, size=size, bold=bold, italic=italic)
    return p


def titulo(doc, texto: str, line: float = 13.5):
    return par(doc, texto, size=24, bold=True, before=0, after=0,
               line=line, keep=True, keep_lines=True)


def parrafo_final_compacto(doc) -> None:
    """Párrafo de cierre de 1 pt para que la última tabla no empuje una cara.

    Word exige un párrafo después de la última tabla; si se deja el implícito
    con el interlineado normal, ese párrafo vacío salta a una segunda página
    cuando la tabla cierra al ras del margen inferior.
    """
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(1)
    pf.widow_control = False
    r = p.add_run(" ")
    _set_run(r, SP_TABLA)


def rotulo(doc, texto: str, line: float = 12.0, before: float = ESP_ANTES,
           after: float = ESP_DESPUES):
    return par(doc, texto, size=SP, bold=True, before=before, after=after,
               line=line, keep=True, keep_lines=True)


def configurar_encabezado(doc) -> None:
    """Crea ``word/header1.xml`` con la banda institucional nativa.

    La banda vive en la parte de encabezado del paquete: tabla de tres celdas
    sin bordes, fila de 2.0 cm exactos y logotipos de 1.6 cm insertados como
    imágenes del encabezado. No se crea pie de página ni ``w:footerReference``.
    """
    sec = doc.sections[0]
    sec.header_distance = Cm(0.8)
    sec.top_margin = Cm(3.0)
    header = sec.header
    header.is_linked_to_previous = False

    for p in list(header.paragraphs):
        p._element.getparent().remove(p._element)

    t = header.add_table(rows=1, cols=3, width=Cm(15.5))
    t.style = None
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    dq._fijar_margenes_celda_tabla(t._tbl, 0, 0, 0, 0)
    _geometria(t, _dxa(BANDA_ANCHOS_CM))
    _sin_bordes(t)
    dq.eliminar_flotacion_tabla(t)

    fila = t.rows[0]
    dq._preparar_tr(fila._tr, cant_split=True, tbl_header=False)
    fila.height = Cm(BANDA_ALTO_CM)
    fila.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
    for celda in fila.cells:
        celda.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

    for indice in (0, 2):
        parrafo = t.cell(0, indice).paragraphs[0]
        for hijo in list(parrafo._element):
            if hijo.tag != qn("w:pPr"):
                parrafo._element.remove(hijo)
        pf = parrafo.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing = 1.0          # automático 240: no recorta la imagen
        _desactivar_rejilla(parrafo)
        parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        ruta = LOGO_UNAJMA if indice == 0 else LOGO_EPIS
        parrafo.add_run().add_picture(str(ruta), height=Cm(LOGO_ALTO_CM))

    lineas = (
        ("UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS", True),
        ("Facultad de Ingeniería", False),
        ("Escuela Profesional de Ingeniería de Sistemas", False),
    )
    celda_texto = t.cell(0, 1)
    for posicion, (texto, negrita) in enumerate(lineas):
        parrafo = (celda_texto.paragraphs[0] if posicion == 0
                   else celda_texto.add_paragraph())
        if posicion == 0:
            for hijo in list(parrafo._element):
                if hijo.tag != qn("w:pPr"):
                    parrafo._element.remove(hijo)
        pf = parrafo.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing = Pt(11.5)
        parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = parrafo.add_run(texto)
        _set_run(run, SP_TABLA, bold=negrita)
        _ESTADO["hdr"].append(SP_TABLA)

    cierre = header.add_paragraph()
    pf = cierre.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(1)
    pf.widow_control = False

    pgMar = sec._sectPr.find(qn("w:pgMar"))
    pgMar.set(qn("w:top"), "1701")
    pgMar.set(qn("w:header"), "454")
    pgMar.set(qn("w:footer"), "0")


# ---------------------------------------------------------------------------
# Plantilla
# ---------------------------------------------------------------------------

def configurar_estilos(doc) -> None:
    estilos = doc.styles
    normal = estilos["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(10)
    rpr = normal.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for atributo in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(atributo), "Times New Roman")
    pf = normal.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.0
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.widow_control = True

    raiz = estilos.element
    defaults = raiz.find(qn("w:docDefaults"))
    if defaults is not None:
        rpr_def = defaults.find(qn("w:rPrDefault") + "/" + qn("w:rPr"))
        if rpr_def is not None:
            fuentes = rpr_def.find(qn("w:rFonts"))
            if fuentes is None:
                fuentes = OxmlElement("w:rFonts")
                rpr_def.insert(0, fuentes)
            for atributo in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
                fuentes.set(qn(atributo), "Times New Roman")
            for etiqueta in ("w:sz", "w:szCs"):
                nodo = rpr_def.find(qn(etiqueta))
                if nodo is None:
                    nodo = OxmlElement(etiqueta)
                    rpr_def.append(nodo)
                nodo.set(qn("w:val"), str(SP))
            idioma = rpr_def.find(qn("w:lang"))
            if idioma is None:
                idioma = OxmlElement("w:lang")
                rpr_def.append(idioma)
            idioma.set(qn("w:val"), "es-PE")
            idioma.set(qn("w:eastAsia"), "es-PE")


def nueva_plantilla() -> Document:
    doc = Document()
    sec = doc.sections[0]
    sectPr = sec._sectPr
    pgSz = sectPr.find(qn("w:pgSz"))
    pgSz.set(qn("w:w"), "11906")
    pgSz.set(qn("w:h"), "16838")
    pgMar = sectPr.find(qn("w:pgMar"))
    for lado, valor in (("top", "1701"), ("right", "1417"),
                        ("bottom", "1417"), ("left", "1701"),
                        ("header", "454"), ("footer", "0"), ("gutter", "0")):
        pgMar.set(qn(f"w:{lado}"), valor)
    for nodo in sectPr.findall(qn("w:docGrid")):
        sectPr.remove(nodo)
    configurar_estilos(doc)
    _ESTADO["hdr"] = []
    _ESTADO["capturas"] = []
    _ESTADO["capturas_libres"] = []
    configurar_encabezado(doc)
    for p in list(doc.paragraphs):
        p._element.getparent().remove(p._element)
    doc.core_properties.language = "es-PE"
    doc.core_properties.author = "SIVAC"
    return doc


# ---------------------------------------------------------------------------
# Geometría de tablas
# ---------------------------------------------------------------------------

def _dxa(anchos_cm: Sequence[float], flexible: Optional[int] = None) -> list[int]:
    valores = [int(round(a * DXA_CM)) for a in anchos_cm]
    delta = ANCHO_DXA - sum(valores)
    if delta:
        if flexible is None:
            flexible = max(range(len(valores)), key=lambda i: valores[i])
        valores[flexible] += delta
    return valores


def _geometria(tabla, anchos_dxa: Sequence[int]) -> None:
    tbl = tabla._tbl
    tblPr = tbl.tblPr
    previo = tblPr.find(qn("w:tblW"))
    if previo is not None:
        tblPr.remove(previo)
    tblW = OxmlElement("w:tblW")
    tblW.set(qn("w:type"), "dxa")
    tblW.set(qn("w:w"), str(sum(anchos_dxa)))
    tblPr.insert_element_before(
        tblW, "w:jc", "w:tblCellSpacing", "w:tblInd", "w:tblBorders",
        "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook",
    )
    tabla.autofit = False
    grid = tbl.tblGrid
    for gc, ancho in zip(grid.gridCol_lst, anchos_dxa):
        gc.set(qn("w:w"), str(ancho))
    for tr in tbl.tr_lst:
        indice = 0
        for tc in tr.tc_lst:
            span = tc.grid_span or 1
            ancho = sum(anchos_dxa[indice:indice + span])
            tcPr = tc.get_or_add_tcPr()
            tcW = tcPr.get_or_add_tcW()
            tcW.set(qn("w:type"), "dxa")
            tcW.set(qn("w:w"), str(ancho))
            indice += span


def _sin_bordes(tabla) -> None:
    """Tabla sin ninguna línea: tampoco declara bordes verticales."""
    tblPr = tabla._tbl.tblPr
    previo = tblPr.find(qn("w:tblBorders"))
    if previo is not None:
        tblPr.remove(previo)
    bordes = OxmlElement("w:tblBorders")
    for borde in ("top", "bottom", "insideH"):
        el = OxmlElement(f"w:{borde}")
        el.set(qn("w:val"), "nil")
        el.set(qn("w:sz"), "0")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "auto")
        bordes.append(el)
    tblPr.insert_element_before(
        bordes, "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook",
        "w:tblCaption", "w:tblDescription",
    )


def _borde_celda(celda, lados: Sequence[str], sz: int) -> None:
    """Escribe ``w:tcBorders`` solo con los lados horizontales indicados."""
    tcPr = celda._tc.get_or_add_tcPr()
    previo = tcPr.find(qn("w:tcBorders"))
    if previo is not None:
        tcPr.remove(previo)
    bordes = OxmlElement("w:tcBorders")
    for lado in lados:
        el = OxmlElement(f"w:{lado}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(sz))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")
        bordes.append(el)
    tcPr.insert_element_before(
        bordes, "w:shd", "w:noWrap", "w:tcMar", "w:textDirection",
        "w:tcFitText", "w:vAlign", "w:hideMark", "w:headers", "w:cellIns",
        "w:cellDel", "w:cellMerge", "w:tcPrChange",
    )


def _bordes_horizontales(tabla, exterior: int = 8, interior: int = 4,
                         apa: bool = False, header_rows: int = 1) -> None:
    """Bordes horizontales exclusivos: superior, internos y superior.

    ``apa=True`` deja solo las tres líneas canónicas: borde superior, borde
    inferior del encabezado y borde inferior de la tabla. ``insideV``,
    ``w:left`` y ``w:right`` no se emiten nunca; la ausencia del elemento deja
    la tabla sin líneas verticales en Word.
    """
    tblPr = tabla._tbl.tblPr
    previo = tblPr.find(qn("w:tblBorders"))
    if previo is not None:
        tblPr.remove(previo)
    bordes = OxmlElement("w:tblBorders")
    lados = ("top", "bottom") if apa else ("top", "insideH", "bottom")
    for borde in lados:
        el = OxmlElement(f"w:{borde}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(exterior if borde != "insideH" else interior))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")
        bordes.append(el)
    tblPr.insert_element_before(
        bordes, "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook",
        "w:tblCaption", "w:tblDescription",
    )
    if header_rows and header_rows > 0:
        fila = tabla.rows[header_rows - 1]
        for celda in fila.cells:
            _borde_celda(celda, ("bottom",), 4 if apa else 8)


def _reiniciar_celda(celda):
    tc = celda._tc
    for p in tc.findall(qn("w:p"))[1:]:
        tc.remove(p)
    p = celda.paragraphs[0]
    for hijo in list(p._element):
        if hijo.tag != qn("w:pPr"):
            p._element.remove(hijo)
    return p


def _fijar_margen_celda(celda, margen_lr: int, margen_tb: int) -> None:
    tcPr = celda._tc.get_or_add_tcPr()
    previo = tcPr.find(qn("w:tcMar"))
    if previo is not None:
        tcPr.remove(previo)
    mar = OxmlElement("w:tcMar")
    for lado, valor in (("top", margen_tb), ("left", margen_lr),
                        ("bottom", margen_tb), ("right", margen_lr)):
        nodo = OxmlElement(f"w:{lado}")
        nodo.set(qn("w:w"), str(valor))
        nodo.set(qn("w:type"), "dxa")
        mar.append(nodo)
    tcPr.insert_element_before(
        mar, "w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark",
        "w:headers", "w:cellIns", "w:cellDel", "w:cellMerge", "w:tcPrChange",
    )


def _escribir_celda(celda, spec, size: int, bold: bool, align: str,
                    linea: float, margen_lr: int = MARGEN_LR,
                    margen_tb: int = MARGEN_TB) -> None:
    texto = "" if spec is None else str(spec)
    p = _reiniciar_celda(celda)
    for posicion, renglon in enumerate(texto.split("\n")):
        if posicion > 0:
            p = celda.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing = Pt(linea)
        pf.left_indent = Cm(0)
        pf.first_line_indent = Cm(0)
        pf.alignment = ALINEACION[align]
        if renglon:
            add_runs(p, renglon, size=size, bold=bold)
    celda.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    _fijar_margen_celda(celda, margen_lr, margen_tb)


def _borde_parrafo(parrafo, lados=("top", "bottom"),
                   sz: int = 4) -> None:
    """Dibuja bordes nativos horizontales alrededor de un párrafo vacío."""
    pPr = parrafo._p.get_or_add_pPr()
    previo = pPr.find(qn("w:pBdr"))
    if previo is not None:
        pPr.remove(previo)
    bordes = OxmlElement("w:pBdr")
    for lado in ("top", "bottom"):
        el = OxmlElement(f"w:{lado}")
        activo = lado in lados
        el.set(qn("w:val"), "single" if activo else "nil")
        el.set(qn("w:sz"), str(sz) if activo else "0")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "auto")
        bordes.append(el)
    pPr.insert_element_before(
        bordes, "w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku",
        "w:wordWrap", "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE",
        "w:autoSpaceDN", "w:bidi", "w:adjustRightInd", "w:snapToGrid",
        "w:spacing", "w:ind", "w:contextualSpacing", "w:mirrorIndents",
        "w:suppressOverlap", "w:jc", "w:textDirection", "w:textAlignment",
        "w:textboxTightWrap", "w:outlineLvl", "w:divId", "w:cnfStyle",
        "w:rPr", "w:sectPr", "w:pPrChange",
    )


def _registrar_capturas(alturas: Sequence[Optional[float]],
                        libre: bool = False) -> None:
    for altura in alturas:
        if altura is None:
            continue
        valor = round(float(altura), 2)
        _ESTADO["capturas"].append(valor)
        if libre:
            _ESTADO["capturas_libres"].append(valor)


def tabla_registro(doc, filas: Sequence[Sequence[Any]],
                   anchos_cm: Sequence[float], header_rows: int = 1,
                   size: int = SP_TABLA, linea: float = 12.0,
                   align_defecto: str = "left", header_align: str = "center",
                   align_cols: Optional[Sequence[str]] = None,
                   negritas: Sequence[Tuple[int, int]] = (),
                   rejilla: bool = True, apa: bool = False,
                   flex_col: Optional[int] = None,
                   alto_filas_cm: Optional[float] = None,
                   alto_exacto_cm: Optional[float] = None,
                   alturas_cm: Optional[Sequence[Optional[float]]] = None,
                   regla_altura: str = "exact",
                   captura: bool = False, libre: bool = False,
                   captura_filas: Optional[Sequence[int]] = None,
                   margen_lr: int = MARGEN_LR, margen_tb: int = MARGEN_TB,
                   merges: Sequence[Tuple[int, int, int, int]] = ()):
    """Tabla de registro con geometría exacta y protección de filas.

    ``rejilla`` dibuja los separadores horizontales de los formularios (sin
    líneas verticales); ``apa`` aplica las tres líneas horizontales de la guía.
    ``alto_filas_cm`` fija una altura mínima de escritura y ``alto_exacto_cm``
    una altura exacta para filas de captura vacías. ``captura=True`` registra
    la altura mínima efectiva de las filas de llenado para el manifiesto.
    """
    nfilas = len(filas)
    ncols = len(anchos_cm)
    anchos_dxa = _dxa(anchos_cm, flex_col)

    t = doc.add_table(rows=nfilas, cols=ncols)
    t.style = None
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    dq._fijar_margenes_celda_tabla(t._tbl, margen_lr, margen_lr,
                                   margen_tb, margen_tb)

    cubiertas = set()
    for r1, c1, r2, c2 in merges:
        if (r1, c1) == (r2, c2):
            continue
        t.cell(r1, c1).merge(t.cell(r2, c2))
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                if (r, c) != (r1, c1):
                    cubiertas.add((r, c))

    negras = set(negritas)
    for r, fila in enumerate(filas):
        for c in range(ncols):
            if (r, c) in cubiertas:
                continue
            spec = fila[c] if c < len(fila) else ""
            cabecera = r < header_rows
            bold = True if cabecera else ((r, c) in negras)
            alineacion = header_align if cabecera else (
                align_cols[c] if align_cols is not None else align_defecto)
            _escribir_celda(t.cell(r, c), spec, size, bold,
                            alineacion, linea, margen_lr, margen_tb)

    for i, fila in enumerate(t.rows):
        dq._preparar_tr(fila._tr, cant_split=True,
                        tbl_header=(i < header_rows))
        altura = None
        if alturas_cm is not None and i < len(alturas_cm) \
                and alturas_cm[i] is not None:
            altura = alturas_cm[i]
        elif i >= header_rows:
            if alto_exacto_cm is not None:
                altura = alto_exacto_cm
            elif alto_filas_cm is not None:
                altura = alto_filas_cm
        if altura is not None:
            fila.height = Cm(altura)
            regla = (WD_ROW_HEIGHT_RULE.AT_LEAST
                     if (regla_altura == "atLeast" or
                         (alturas_cm is not None and i >= header_rows and
                          alto_exacto_cm is None and alto_filas_cm is None and
                          regla_altura != "exact"))
                     else WD_ROW_HEIGHT_RULE.EXACTLY)
            fila.height_rule = regla
            if captura and i >= header_rows and (
                    captura_filas is None or i in captura_filas):
                _registrar_capturas([altura], libre=libre)

    _geometria(t, anchos_dxa)
    dq.eliminar_flotacion_tabla(t)
    if apa:
        _bordes_horizontales(t, exterior=8, interior=4, apa=True,
                             header_rows=header_rows)
    elif rejilla:
        _bordes_horizontales(t, exterior=8, interior=4, apa=False,
                             header_rows=header_rows)
    else:
        _sin_bordes(t)
    return t


def ficha_tecnica(doc, filas: Sequence[Tuple[str, str]],
                  linea: float = 12.0, con_cabecera: bool = True,
                  alturas_cm: Optional[Sequence[Optional[float]]] = None,
                  margen_tb: int = MARGEN_TB,
                  before: float = 6.0) -> None:
    """Encabezado «Ficha técnica» y tabla Campo/Valor de 3.5 + 12.0 cm."""
    rotulo(doc, "Ficha técnica", line=linea, before=before)
    if con_cabecera:
        cuerpo = [("Campo", "Valor")] + list(filas)
        cabecera = 1
        negritas = ()
    else:
        cuerpo = list(filas)
        cabecera = 0
        negritas = tuple((i, 0) for i in range(len(cuerpo)))
    tabla_registro(doc, cuerpo, (3.5, 12.0), header_rows=cabecera,
                   linea=linea, align_defecto="left", flex_col=1,
                   negritas=negritas, alturas_cm=alturas_cm,
                   regla_altura="atLeast", margen_tb=margen_tb)


def ficha_tecnica_cuatro(doc, filas: Sequence[Sequence[str]],
                         linea: float = 12.0,
                         alturas_cm: Optional[Sequence[Optional[float]]] = None,
                         merges: Sequence[Tuple[int, int, int, int]] = (),
                         margen_tb: int = MARGEN_TB,
                         before: float = 6.0) -> None:
    """Ficha técnica compacta de cuatro columnas, sin fila de encabezado."""
    rotulo(doc, "Ficha técnica", line=linea, before=before)
    negritas = tuple((r, c) for r in range(len(filas)) for c in (0, 2)
                     if c < len(filas[r]) and filas[r][c])
    tabla_registro(doc, filas, (3.6, 4.4, 3.0, 4.5), header_rows=0,
                   linea=linea, align_defecto="left", flex_col=3,
                   negritas=negritas, merges=merges,
                   alturas_cm=alturas_cm, regla_altura="atLeast",
                   margen_tb=margen_tb)


def datos_generales(doc, pares: Sequence[Tuple[str, str]],
                    linea: float = 12.0,
                    alto_filas_cm: float = ALTO_CAPTURA,
                    con_cabecera: bool = True,
                    alturas_cm: Optional[Sequence[Optional[float]]] = None,
                    margen_tb: int = MARGEN_TB) -> None:
    """Tabla Campo/Registro de 4.0 + 11.5 cm con filas de captura."""
    if con_cabecera:
        cuerpo = [("Campo", "Registro")] + list(pares)
        cabecera = 1
        negritas = ()
    else:
        cuerpo = list(pares)
        cabecera = 0
        negritas = tuple((i, 0) for i in range(len(cuerpo)))
    tabla_registro(doc, cuerpo, (4.0, 11.5), header_rows=cabecera,
                   linea=linea, align_defecto="left", flex_col=1,
                   alto_filas_cm=alto_filas_cm, alturas_cm=alturas_cm,
                   regla_altura="atLeast", captura=True, libre=True,
                   negritas=negritas, margen_tb=margen_tb)


def instrucciones(doc, lineas: Sequence[str], linea: float = 12.0,
                  after: float = 1.0) -> None:
    """Párrafos de instrucciones justificados, sin sangría."""
    for texto in lineas:
        par(doc, texto, align="both", line=linea, before=0, after=after)


def seccion_romana(doc, numero: str, titulo_seccion: str,
                   cuerpo: Callable[[], None], linea: float = 12.0,
                   before: float = ESP_ANTES,
                   after: float = ESP_DESPUES) -> None:
    """Rótulo «I. Título» y ejecución del bloque de contenido que le sigue."""
    rotulo(doc, f"{numero}. {titulo_seccion}", line=linea, before=before,
           after=after)
    cuerpo()


def leyenda_escala(doc, linea: float = 12.0) -> None:
    """Banda horizontal de cinco celdas con la escala Likert completa."""
    fila = (("**1** Totalmente en desacuerdo", "**2** En desacuerdo",
             "**3** Ni de acuerdo ni en desacuerdo", "**4** De acuerdo",
             "**5** Totalmente de acuerdo"),)
    tabla_registro(doc, fila, (3.1, 3.1, 3.1, 3.1, 3.1), header_rows=0,
                   linea=10.5, align_defecto="center", flex_col=2,
                   regla_altura="atLeast", alto_filas_cm=1.00,
                   apa=True, margen_tb=MARGEN_TB)


def banda_cierre_documental(doc, linea: float = 12.0,
                             antes: float = 10.0) -> None:
    """Cierre IV-V en una sola fila de dos columnas, sin líneas verticales."""
    par(doc, "", size=2, line=max(antes, 2.0), before=0, after=0)
    t = doc.add_table(rows=1, cols=2)
    t.style = None
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    dq._fijar_margenes_celda_tabla(t._tbl, MARGEN_LR, MARGEN_LR,
                                   MARGEN_TB, MARGEN_TB)
    _geometria(t, _dxa((8.2, 7.3), 1))
    dq.eliminar_flotacion_tabla(t)
    _bordes_horizontales(t, exterior=8, interior=4, apa=False, header_rows=0)

    fila = t.rows[0]
    fila.height = Cm(2.25)
    fila.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
    dq._preparar_tr(fila._tr, cant_split=True, tbl_header=False)

    izq, der = t.cell(0, 0), t.cell(0, 1)
    for celda in (izq, der):
        celda.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
        _fijar_margen_celda(celda, MARGEN_LR, MARGEN_TB)

    p = _reiniciar_celda(izq)
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(min(linea, 9.5))
    add_runs(p, "IV. Observaciones", size=SP_TABLA, bold=True)

    p = _reiniciar_celda(der)
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(min(linea, 9.5))
    add_runs(p, "V. Responsable", size=SP_TABLA, bold=True)

    for etiqueta, valor in (
            ("Nombre del observador:", "_" * 16),
            ("Firma:", "_" * 32),
            ("Fecha:", "____ / ____ / ________")):
        p = der.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing = Cm(0.52)
        add_runs(p, etiqueta + " ", size=SP_TABLA, bold=True)
        add_runs(p, valor, size=SP_TABLA, bold=False)
        _borde_parrafo(p, lados=("bottom",))


# ---------------------------------------------------------------------------
# Documentos
# ---------------------------------------------------------------------------

def linea_identificacion(doc, texto: str, linea: float = 10.5,
                         salto_pagina: bool = False) -> None:
    """Línea de identificación del instrumento, impresa bajo el título."""
    p = par(doc, texto, size=SP_TABLA, line=linea, before=0, after=0,
            italic=False)
    if salto_pagina:
        p.paragraph_format.page_break_before = True


def doc_00(doc) -> None:
    """Guía de aplicación: instrumentos, instantes y reglas operativas."""
    li = INTERLINEA["00"]
    titulo(doc, "Guía de aplicación de los instrumentos", line=li)
    linea_identificacion(doc, "Instrumento 00 · Guía de aplicación · "
                              "Versión v06 · Ejemplar del investigador", li)

    rotulo(doc, "Instrumentos", line=li, before=5)
    tabla_registro(doc, [
        ("Instrumento", "Qué mide", "Quién lo llena", "Cuándo"),
        ("01. Ficha de tiempos",
         "T_reg y T_vale, en minutos",
         "Investigador, por observación directa", "Pretest y postest"),
        ("02. Ficha documental",
         "RSD y CPE, en porcentaje",
         "Investigador, por revisión documental", "Pretest y postest"),
        ("03. Cuestionario",
         "AP y UP, escala de 1 a 5",
         "Trabajador, sin nombre", "Al final de cada momento"),
        ("04. Consentimiento",
         "Aceptación voluntaria", "Trabajador e investigador",
         "Antes de la primera medición"),
        ("05. Certificado",
         "Validez de contenido", "Tres jueces expertos",
         "Antes del trabajo de campo"),
    ], (3.1, 4.0, 4.6, 3.8), header_rows=1, linea=li,
        align_defecto="left", flex_col=1, rejilla=False, apa=True)

    rotulo(doc, "Los cuatro instantes y las dos fórmulas", line=li)
    tabla_registro(doc, [
        ("Instante", "Definición"),
        ("Inicio", "El trabajador dispone del documento fuente completo y "
                   "comienza el registro del movimiento."),
        ("Corte de registro", "El movimiento queda registrado y guardado."),
        ("Solicitud de despacho", "El establecimiento destino presenta la "
                                  "solicitud del vale."),
        ("Emisión", "El comprobante o vale está emitido y disponible."),
        ("Fórmulas", "**T_reg = corte de registro − inicio.**  "
                     "**T_vale = emisión − solicitud de despacho.** Son las "
                     "únicas definiciones; no se usa ninguna otra."),
    ], (3.1, 12.4), header_rows=1, linea=li, align_defecto="left",
        flex_col=1, rejilla=False, apa=True)

    rotulo(doc, "Reglas operativas", line=li)
    tabla_registro(doc, [
        ("Regla", "Aplicación"),
        ("1. Réplicas",
         "Tres mediciones válidas por indicador y momento. El valor del "
         "trabajador es la mediana de las tres, calculada fuera del "
         "formulario. Horas en hh:mm:ss; minutos con dos decimales."),
        ("2. Interrupción externa",
         "Se anota en la columna correspondiente y la réplica se repite; no "
         "se descuenta del tiempo."),
        ("3. Documento conforme",
         "Cumple los ocho criterios de la ficha 02. Un solo No anula el "
         "documento."),
        ("4. Despacho conforme",
         "La cantidad entregada iguala la programada en la misma unidad. "
         "Toda diferencia se anota como observación y no altera la "
         "conformidad."),
        ("5. Hoja de continuación",
         "Si hay más asientos que filas, se usa la hoja siguiente con la "
         "numeración corrida y «Hoja __ de __»."),
        ("6. Doble codificación",
         "Un segundo observador, ciego, codifica el 20 % de la muestra: ocho "
         "documentos y cinco despachos por trabajador. Se anota su nombre en "
         "la ficha y se calcula kappa de Cohen."),
        ("7. Trabajador ausente",
         "Si no está en el postest, se conserva en el padrón, se registra «No "
         "aplica — ausente» y el caso se excluye por pares. No se imputa."),
        ("8. Dos centros",
         "Un trabajador que cubre dos centros recibe un solo código; el "
         "centro se anota por observación y se reporta el principal."),
        ("9. Operación no ocurrida",
         "Se registra la siguiente operación del mismo bloque y se anota; no "
         "se deja la fila vacía ni se inventa el dato."),
        ("10. Numeración",
         "TRAB-01 a TRAB-14, igual en pretest y postest. La lista de nombres "
         "se guarda aparte y se destruye al cerrar el estudio."),
        ("11. Porcentajes",
         "Conformes entre revisados, por cien, en cada indicador. No se "
         "compensan entre sí."),
    ], (3.6, 11.9), header_rows=1, linea=li, align_defecto="left",
        flex_col=1, rejilla=False, apa=True)

    par(doc, "Se imprime una hoja de 01, 02 y 03 por trabajador y momento, "
             "más las de continuación. El consentimiento va por duplicado.",
        align="both", size=SP_TABLA, line=li, before=8, after=0)
    parrafo_final_compacto(doc)


def doc_01(doc) -> None:
    """Ficha de tiempos: Dimensión 1, oportunidad de procesamiento."""
    li = INTERLINEA["01"]
    titulo(doc, "Ficha de tiempos", line=li)
    linea_identificacion(doc, "Instrumento 01 · Ficha de tiempos · "
                              "Versión v06 · Hoja 1 de 1", li)

    seccion_romana(doc, "I", "Datos generales", lambda: tabla_registro(doc, [
        ("N.° de trabajador", "", "Centro de salud", ""),
        ("Fecha", "____ / ____ / ________", "Momento",
         "☐ Antes de SIVAC      ☐ Con SIVAC"),
    ], (3.3, 3.5, 2.5, 6.2), header_rows=0, linea=li,
        align_defecto="left", flex_col=3,
        negritas=((0, 0), (0, 2), (1, 0), (1, 2)),
        alturas_cm=(ALTO_CAPTURA, ALTO_CAPTURA), regla_altura="atLeast",
        captura=True), linea=li, before=5, after=2)

    seccion_romana(doc, "II", "Instrucciones", lambda: instrucciones(doc, [
        "T_reg = hora de corte de registro − hora de inicio. T_vale = hora de "
        "emisión − hora de solicitud de despacho. No hay otra definición.",
        "Anote tres mediciones válidas por indicador. El valor del trabajador "
        "es la mediana de las tres y se calcula fuera de este formulario. Si "
        "hay interrupción externa (llamada, atención a usuarios no "
        "relacionada, falla de energía, espera de terceros), anótela y repita "
        "la medición: no se descuenta del tiempo.",
    ], linea=li), linea=li, before=5, after=2)

    cab_a = ("N.°", "Escenario", "Inicio", "Corte de registro",
             "T_reg (min)", "Interrupción externa")
    filas_a = [cab_a,
               ("1", "Registro de ingreso", "", "", "", ""),
               ("2", "Registro de salida", "", "", "", ""),
               ("3", "Registro de transferencia", "", "", "", "")]
    cab_b = ("N.°", "Escenario", "Solicitud de despacho", "Emisión",
             "T_vale (min)", "Interrupción externa")
    filas_b = [cab_b,
               ("1", "Vale regular", "", "", "", ""),
               ("2", "Vale por reposición", "", "", "", ""),
               ("3", "Vale de transferencia", "", "", "", "")]
    anchos = (0.8, 3.9, 2.5, 2.8, 2.5, 3.0)

    def contenido_tiempos() -> None:
        par(doc, "**Bloque A. T_reg** — tiempo de registro del movimiento: un "
                 "ingreso, una salida y una transferencia.", line=li,
            before=4, after=2, keep=True, keep_lines=True)
        tabla_registro(doc, filas_a, anchos, header_rows=1, linea=li,
                       align_defecto="center", flex_col=1,
                       alturas_cm=(0.85, 1.0, 1.0, 1.0),
                       regla_altura="atLeast", captura=True)
        par(doc, "**Bloque B. T_vale** — tiempo de emisión del comprobante o "
                 "vale: uno regular, una reposición urgente y una "
                 "transferencia.", line=li, before=8, after=2, keep=True,
            keep_lines=True)
        tabla_registro(doc, filas_b, anchos, header_rows=1, linea=li,
                       align_defecto="center", flex_col=1,
                       alturas_cm=(0.85, 1.0, 1.0, 1.0),
                       regla_altura="atLeast", captura=True)

    seccion_romana(doc, "III", "Contenido", contenido_tiempos, linea=li,
                   before=5, after=2)

    seccion_romana(doc, "IV", "Observaciones", lambda: tabla_registro(
        doc, [("",), ("",)], (15.5,), header_rows=0, linea=li,
        align_defecto="left", flex_col=0,
        alturas_cm=(1.0, 1.0), regla_altura="atLeast",
        captura=True, margen_tb=MARGEN_TB), linea=li, before=5, after=2)

    seccion_romana(doc, "V", "Responsable", lambda: tabla_registro(doc, [
        ("Nombre del observador", "_" * 22, "Fecha", "____ / ____ / ________"),
        ("Firma", "_" * 44, "", ""),
    ], (4.1, 4.9, 1.6, 4.9), header_rows=0, linea=li,
        align_defecto="left", flex_col=1,
        negritas=((0, 0), (0, 2), (1, 0)),
        alturas_cm=(1.0, 1.0), regla_altura="atLeast",
        captura=True, merges=((1, 1, 1, 3),)), linea=li, before=5, after=2)
    parrafo_final_compacto(doc)


def doc_02(doc) -> None:
    """Ficha documental: Dimensión 2, consistencia documental."""
    li = INTERLINEA["02"]
    lt = 10.5                     # interlineado exacto de las tablas compactas
    mt = MARGEN_TB
    titulo(doc, "Ficha documental", line=li)
    linea_identificacion(doc, "Instrumento 02 · Ficha documental · "
                              "Versión v06 · Hoja ____ de ____", li)

    seccion_romana(doc, "I", "Datos generales", lambda: (
        tabla_registro(doc, [
            ("N.° de trabajador", "", "Centro de salud", ""),
            ("Fecha", "____/____/______", "Momento",
             "☐ Antes del SIVAC   ☐ Con SIVAC"),
        ], (3.9, 3.4, 2.9, 5.3), header_rows=0, linea=lt,
            align_defecto="left", flex_col=3,
            negritas=((0, 0), (0, 2), (1, 0), (1, 2)),
            alturas_cm=(0.6, 0.6), regla_altura="atLeast",
            captura=True, libre=True, margen_tb=mt),
        par(doc, "Periodo revisado: del ____ / ____ / ________ al "
                 "____ / ____ / ________", size=SP_TABLA, line=lt,
            before=3, after=0),
    ), linea=li, before=4, after=2)

    seccion_romana(doc, "II", "Instrucciones", lambda: par(
        doc, "Un renglón por asiento; marque Sí o No en los ocho criterios: "
             "1 biológico (nombre y presentación); 2 lote; 3 vencimiento (mes "
             "y año); 4 cantidad; 5 establecimiento; 6 responsable y firmas; "
             "7 saldo aritmético (inicial + ingresos − salidas); 8 "
             "correlatividad temporal con los asientos contiguos. **Un solo No "
             "anula el documento.** El Bloque B (hoja 2) registra los "
             "despachos: es conforme solo si lo entregado iguala lo programado "
             "en la misma unidad; toda diferencia es una observación.",
        align="both",
        size=SP_TABLA, line=lt, before=2, after=0), linea=li, before=4,
        after=2)

    cab_a = ("N.°", "Fecha", "Tipo de doc.", "N.° de doc.", "Lote",
             "1", "2", "3", "4", "5", "6", "7", "8", "Conf.")
    filas_a = [cab_a] + [(str(n), "", "", "", "", "", "", "", "", "", "",
                          "", "", "") for n in range(1, 41)]

    cab_b = ("N.°", "Fecha", "Establecimiento destino", "Biológico",
             "Prog.", "Entr.", "Dif.", "Observación", "Conforme")
    filas_b = [cab_b] + [(str(n), "", "", "", "", "", "", "", "")
                         for n in range(1, 26)]

    def bloque_a() -> None:
        par(doc, "**III. Bloque A. Documentos auditados (40 por hoja).**",
            size=SP_TABLA, line=lt, before=2, after=2, keep=True,
            keep_lines=True)
        tabla_registro(doc, filas_a,
                       (0.8, 1.7, 1.85, 1.95, 1.7, 0.75, 0.75, 0.75, 0.75,
                        0.75, 0.75, 0.75, 0.75, 1.3),
                       header_rows=1, linea=10.0, align_defecto="center",
                       flex_col=2,
                       alturas_cm=[0.70] + [0.42] * 40,
                       regla_altura="atLeast", captura=True, margen_tb=14)

    bloque_a()

    linea_identificacion(doc, "Instrumento 02 · Ficha documental · "
                              "Versión v06 · Hoja ____ de ____", li,
                         salto_pagina=True)
    par(doc, "N.°: ______   Centro: __________   Momento: ☐ Antes de SIVAC "
             "☐ Con SIVAC   Fecha: __/__/____", size=SP_TABLA, line=lt,
        before=4, after=0)

    def bloque_b() -> None:
        par(doc, "**III (continuación). Bloque B. Despachos auditados (25 "
                 "por hoja).** Prog. = cantidad programada; Entr. = cantidad "
                 "entregada; Dif. = entregado − programado, en la misma unidad "
                 "(dosis o frascos). El documento de ajuste se anota como "
                 "observación.", size=SP_TABLA, line=lt, before=6,
            after=2, keep=True, keep_lines=True)
        tabla_registro(doc, filas_b,
                       (0.8, 1.6, 2.7, 1.9, 1.1, 1.1, 1.1, 3.2, 2.0),
                       header_rows=1, linea=lt, align_defecto="center",
                       flex_col=2,
                       alturas_cm=[0.8] + [0.62] * 25,
                       captura=True, margen_tb=mt)

    bloque_b()

    par(doc, "Documentos conformes ______ / revisados ______      Despachos "
             "conformes ______ / revisados ______", size=SP_TABLA, bold=True,
        line=lt, before=10, after=0)
    par(doc, "Si el número de asientos supera las filas de la hoja, continúe "
             "en la hoja siguiente con la numeración corrida y anote «Hoja __ "
             "de __» en ambas. El segundo observador firma la doble "
             "codificación en la hoja de continuación.", size=SP_TABLA, line=lt,
        before=6, after=0)

    banda_cierre_documental(doc, linea=li, antes=15.0)
    parrafo_final_compacto(doc)


def doc_03(doc) -> None:
    """Cuestionario de satisfacción: Dimensión 3, satisfacción del usuario."""
    li = INTERLINEA["03"]
    titulo(doc, "Cuestionario de satisfacción del usuario", line=li)
    linea_identificacion(doc, "Instrumento 03 · Cuestionario de satisfacción · "
                              "Versión v06 · Hoja 1 de 1", li)

    ficha_tecnica(doc, [
        ("Variable", "Gestión de movimientos mensuales de vacunas"),
        ("Dimensión", "Satisfacción del usuario"),
        ("Indicador", "Aceptación del proceso (AP) y utilidad percibida (UP), "
                      "en escala ordinal de 1 a 5"),
        ("Aplicación", "Pretest y postest; cuestionario autoadministrado"),
    ], linea=li, alturas_cm=(0.52,) * 4)

    seccion_romana(doc, "I", "Datos generales", lambda: datos_generales(doc, [
        ("N.° de trabajador", ""),
        ("Centro de salud", ""),
        ("Fecha", "____ / ____ / ________"),
        ("Momento", "☐ Antes de SIVAC        ☐ Con SIVAC"),
    ], linea=li, alto_filas_cm=0.85), linea=li, before=5)

    def instrucciones_y_escala() -> None:
        par(doc, "Marque con una X un solo número por afirmación. No escriba "
                 "su nombre; sus respuestas son confidenciales.", align="both",
            line=li, before=0, after=4)
        leyenda_escala(doc, linea=li)

    seccion_romana(doc, "II", "Instrucciones", instrucciones_y_escala,
                   linea=li, before=5)

    cabecera = ("N.°", "Afirmación", "1", "2", "3", "4", "5")
    banda_ap = ("", "**Aceptación del proceso (AP)**", "", "", "", "", "")
    banda_up = ("", "**Utilidad percibida (UP)**", "", "", "", "", "")
    items_ap = [
        "El procedimiento actual para asentar los movimientos diarios y "
        "cierres de mes es ágil y no demanda un esfuerzo mental o físico "
        "excesivo.",
        "El flujo de trabajo requerido para emitir comprobantes de salida y "
        "vales de entrega es fluido y está libre de demoras o trabas "
        "burocráticas.",
        "El método empleado me permite conciliar los saldos de inventario con "
        "las microredes generando tranquilidad y reduciendo el estrés laboral.",
        "El tiempo que dedico al registro administrativo de vacunas es "
        "equilibrado y me deja disponibilidad para mis labores sanitarias y "
        "asistenciales.",
    ]
    items_up = [
        "El mecanismo de registro que utilizo me permite disponer de "
        "información fidedigna del stock de vacunas y jeringas cuando la "
        "necesito.",
        "El control de números de lote y fechas de vencimiento que brinda el "
        "proceso previene oportunamente mermas o pérdidas de biológicos.",
        "La metodología de gestión facilita la detección inmediata y "
        "rectificación de cualquier descuadre de inventario físico versus "
        "registrado.",
        "El procedimiento que utilizo me permite atender a tiempo los "
        "requerimientos de vacunas de los establecimientos de mi "
        "jurisdicción.",
    ]
    filas = [cabecera, banda_ap]
    filas += [(str(n), texto, "", "", "", "", "")
              for n, texto in enumerate(items_ap, start=1)]
    filas.append(banda_up)
    filas += [(str(n), texto, "", "", "", "", "")
              for n, texto in enumerate(items_up, start=5)]

    seccion_romana(doc, "III", "Contenido", lambda: tabla_registro(
        doc, filas, (0.9, 11.2, 0.68, 0.68, 0.68, 0.68, 0.68),
        header_rows=1, linea=li, align_defecto="left", flex_col=1,
        negritas=((1, 1), (6, 1)),
        alturas_cm=[0.55, 0.62] + [1.0] * 4 + [0.62] + [1.0] * 4,
        regla_altura="atLeast", captura=True, libre=True), linea=li, before=5)

    par(doc, "Total AP: ____ / 20      Total UP: ____ / 20      Total: ____ "
             "/ 40", size=SP_TABLA, line=li, before=6, after=0)
    par(doc, "Gracias por su participación.", line=li, before=6, after=0)
    parrafo_final_compacto(doc)


def doc_04(doc) -> None:
    """Consentimiento informado: documento ético transversal."""
    li = INTERLINEA["04"]
    titulo(doc, "Consentimiento informado para participar en la investigación",
           line=li)
    linea_identificacion(doc, "Instrumento 04 · Consentimiento informado · "
                              "Versión v06 · Hoja 1 de 1", li)

    seccion_romana(doc, "I", "Datos generales del participante",
                   lambda: datos_generales(doc, [
                       ("N.° de trabajador", ""),
                       ("Centro de salud", ""),
                       ("Fecha", "____ / ____ / ________"),
                       ("Momento", "Antes de la primera medición"),
                   ], linea=li, alto_filas_cm=0.7), linea=li, before=4)

    bloques = [
        ("1. Propósito.", "Esta investigación evalúa si el sistema SIVAC "
         "mejora la gestión de los movimientos mensuales de vacunas en el "
         "personal de inmunizaciones de la Dirección de Salud Apurímac II."),
        ("2. Procedimiento.", "Se observará y cronometrará cómo registra un "
         "movimiento de vacunas y cómo emite el comprobante de salida o vale. "
         "Se revisarán los documentos de movimiento de un periodo de treinta "
         "días y se le aplicará un cuestionario de ocho preguntas. La "
         "actividad se realiza en dos momentos, antes y con SIVAC, y demanda "
         "entre treinta y cuarenta minutos por momento."),
        ("3. Riesgos.", "No implica riesgos distintos de sus actividades "
         "habituales. No se tomarán muestras biológicas ni datos clínicos."),
        ("4. Beneficios.", "Contribuirá a mejorar el registro y el control de "
         "vacunas. No hay pago ni compensación económica."),
        ("5. Confidencialidad.", "Los formularios se identifican solo con un "
         "número de trabajador, sin nombres. La lista que vincula números y "
         "nombres queda en poder del investigador, separada de los "
         "formularios, y se destruye al concluir el informe. Los datos se usan "
         "solo para esta tesis."),
        ("6. Voluntariedad.", "La participación es libre. Puede retirarse en "
         "cualquier momento, sin perjuicio."),
        ("7. Aprobación y contacto.", "El estudio cuenta con la aprobación del "
         "Comité de Ética en Investigación de la Universidad Nacional José "
         "María Arguedas, o con su constancia de exención (N.° ____________). "
         "Investigador: Bach. "
         "José Luis Quispe León, Escuela Profesional de Ingeniería de "
         "Sistemas, UNAJMA, Andahuaylas. Correo: jquispe.leon20@gmail.com. "
         "Teléfono: ____________."),
        ("8. Declaración de consentimiento.", "He leído y comprendido la "
         "información. Mis preguntas fueron respondidas. Acepto participar "
         "voluntariamente."),
    ]

    def informacion() -> None:
        par(doc, "Estimado(a) participante:", line=li, after=0)
        for lead, texto in bloques:
            par(doc, f"**{lead}** {texto}", line=li, before=6, after=0,
                align="both")

    seccion_romana(doc, "II", "Información al participante", informacion,
                   linea=li, before=5)

    seccion_romana(doc, "III", "Firmas", lambda: tabla_registro(doc, [
        ("Participante", "Investigador"),
        ("Nombre: ______________________________",
         "Nombre: ______________________________"),
        ("DNI: ______________",
         "DNI: ______________"),
        ("Firma: ______________________________",
         "Firma: ______________________________"),
        ("Fecha: ____ / ____ / ________",
         "Fecha: ____ / ____ / ________"),
        ("Testigo (si el participante no puede firmar): nombre, DNI y firma. "
         "Si no puede firmar, impresión de huella digital del dedo índice "
         "derecho.", ""),
    ], (7.75, 7.75), header_rows=1, linea=li, align_defecto="left",
        flex_col=0, alturas_cm=(0.55, 0.95, 0.75, 1.15, 0.75, 0.85),
        regla_altura="atLeast", captura=True, libre=True,
        merges=((5, 0, 5, 1),)), linea=li, before=5)

    par(doc, "Este documento se emite por duplicado: una copia para el "
             "participante y otra para el investigador.", size=SP_TABLA,
        line=li, before=6, after=0)
    parrafo_final_compacto(doc)


def doc_05(doc) -> None:
    """Certificado de validación de contenido: documento transversal previo."""
    li = INTERLINEA["05"]
    lt = 10.5          # matriz: interlineado exacto de la especificación
    titulo(doc, "Certificado de validación de contenido", line=10.0)
    linea_identificacion(doc, "Instrumento 05 · Certificado de validación · "
                              "Versión v06 · Hoja ____ de ____", lt)

    ficha_tecnica(doc, [
        ("Variable", "Gestión de movimientos mensuales de vacunas"),
        ("Dimensión", "Todas"),
        ("Indicador", "Los seis indicadores de la variable dependiente"),
        ("Aplicación", "Juicio de expertos, tres jueces"),
    ], linea=lt, con_cabecera=False, alturas_cm=(0.48,) * 4)

    seccion_romana(doc, "I", "Datos del juez validador",
                   lambda: tabla_registro(doc, [
                       ("Apellidos y nombres: ______________________________",
                        "DNI: ____________________"),
                       ("Especialidad: ______________________________",
                        "Institución: ______________________________"),
                       ("Cargo: ______________________________",
                        "CIP: ____________________"),
                       ("Fecha: ____ de ____________________ de ________",
                        ""),
                   ], (7.75, 7.75), header_rows=0, linea=lt,
                       align_defecto="left", flex_col=1,
                       alturas_cm=(0.6, 0.6, 0.6, 0.6), regla_altura="atLeast",
                       captura=True, libre=True, merges=((3, 0, 3, 1),)),
                   linea=li, before=4)

    seccion_romana(doc, "II", "Instrucciones", lambda: instrucciones(doc, [
        "Marque Sí o No en cada criterio y por cada ítem; use Sugerencias para "
        "indicar mejoras. No hay respuestas correctas: se valora el "
        "instrumento, no los resultados del estudio. Pert. = pertinencia; "
        "Relev. = relevancia; Clar. = claridad.",
        "Pertinencia: el ítem corresponde al concepto formulado. Relevancia: "
        "el ítem representa el componente o dimensión. Claridad: el enunciado "
        "se entiende sin dificultad, es conciso, exacto y directo.",
    ], linea=lt), linea=li, before=4)

    def tabla_items(etiqueta: str, filas: Sequence[Sequence[str]]) -> None:
        rotulo(doc, etiqueta, line=lt, before=6, after=2)
        cuerpo = [("N.°", "Ítem", "Pert.", "", "Relev.", "",
                   "Clar.", "", "Sugerencias"),
                  ("", "", "Sí", "No", "Sí", "No", "Sí", "No", "")]
        cuerpo += list(filas)
        tabla_registro(doc, cuerpo,
                       (1.2, 7.2, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 2.5),
                       header_rows=2, linea=lt, align_defecto="left",
                       align_cols=("center", "left", "center", "center",
                                   "center", "center", "center", "center",
                                   "left"),
                       flex_col=1, margen_tb=MARGEN_TB,
                       alturas_cm=[0.55, 0.45] + [0.85] * len(filas),
                       regla_altura="atLeast",
                       merges=((0, 2, 0, 3), (0, 4, 0, 5), (0, 6, 0, 7)))

    items_t = [
        ("T-01", "Los campos de la ficha permiten anotar la hora de inicio y "
                 "la de corte del registro, de modo que T_reg = corte − "
                 "inicio, en minutos."),
        ("T-02", "Los campos permiten anotar la hora de solicitud de despacho "
                 "y la de emisión, de modo que T_vale = emisión − solicitud, "
                 "en minutos."),
        ("T-03", "Las tres réplicas por indicador y la regla de la mediana "
                 "bastan para obtener un valor por trabajador y momento."),
        ("T-04", "La hoja identifica instrumento, versión, trabajador, centro, "
                 "fecha y momento, y permite repetir la medición ante una "
                 "interrupción externa."),
    ]
    items_d = [
        ("D-01", "El criterio 1 comprueba el biológico: nombre y "
                 "presentación."),
        ("D-02", "El criterio 2 comprueba el número de lote."),
        ("D-03", "El criterio 3 comprueba el vencimiento, mes y año."),
        ("D-04", "El criterio 4 comprueba la cantidad de dosis o frascos."),
        ("D-05", "El criterio 5 comprueba el establecimiento de origen o "
                 "destino."),
        ("D-06", "El criterio 6 comprueba el responsable y las firmas de "
                 "entrega y recepción."),
        ("D-07", "El criterio 7 comprueba el saldo aritmético: inicial más "
                 "ingresos menos salidas."),
        ("D-08", "El criterio 8 comprueba la correlatividad temporal entre "
                 "asientos contiguos."),
        ("D-09", "La regla conjuntiva es explícita: un solo No anula el "
                 "documento, y la columna Conforme no se marca por impresión "
                 "global."),
        ("D-10", "El bloque B compara cantidad programada y entregada en la "
                 "misma unidad, y trata toda diferencia como observación, no "
                 "como criterio de conformidad."),
    ]
    items_c = [
        ("AP-01", "El procedimiento actual para asentar los movimientos "
                  "diarios y cierres de mes es ágil y no demanda un esfuerzo "
                  "mental o físico excesivo."),
        ("AP-02", "El flujo de trabajo requerido para emitir comprobantes de "
                  "salida y vales de entrega es fluido y está libre de demoras "
                  "o trabas burocráticas."),
        ("AP-03", "El método empleado me permite conciliar los saldos de "
                  "inventario con las microredes generando tranquilidad y "
                  "reduciendo el estrés laboral."),
        ("AP-04", "El tiempo que dedico al registro administrativo de vacunas "
                  "es equilibrado y me deja disponibilidad para mis labores "
                  "sanitarias y asistenciales."),
        ("UP-01", "El mecanismo de registro que utilizo me permite disponer "
                  "de información fidedigna del stock de vacunas y jeringas "
                  "cuando la necesito."),
        ("UP-02", "El control de números de lote y fechas de vencimiento que "
                  "brinda el proceso previene oportunamente mermas o pérdidas "
                  "de biológicos."),
        ("UP-03", "La metodología de gestión facilita la detección inmediata y "
                  "rectificación de cualquier descuadre de inventario físico "
                  "versus registrado."),
        ("UP-04", "El procedimiento que utilizo me permite atender a tiempo "
                  "los requerimientos de vacunas de los establecimientos de "
                  "mi jurisdicción."),
    ]

    tabla_items("(a) Ficha de tiempos — Instrumento 01", items_t)
    tabla_items("(b) Ficha documental — Instrumento 02", items_d)
    tabla_items("(c) Cuestionario de satisfacción — Instrumento 03", items_c)

    seccion_romana(doc, "III", "Observaciones y opinión de aplicabilidad",
                   lambda: (
                       par(doc, "**Observaciones (precisar si hay "
                                "suficiencia):** ______________________________",
                           line=lt, before=2, after=4),
                       par(doc, "**Opinión de aplicabilidad:** ☐ Aplicable   "
                                "☐ Aplicable después de corregir   "
                                "☐ No aplicable", size=SP_TABLA, line=lt,
                           after=2),
                   ), linea=li, before=6)

    seccion_romana(doc, "IV", "Firma", lambda: tabla_registro(
        doc, [("Firma del juez validador", "", "DNI / CIP", ""),
              ("", "", "Fecha", "__ / __ / ____")],
        (4.3, 5.6, 2.0, 3.6), header_rows=0, linea=li, align_defecto="left",
        flex_col=1, negritas=((0, 0), (0, 2), (1, 2)),
        alturas_cm=(1.5, 0.6), regla_altura="atLeast", captura=True,
        libre=True), linea=li, before=4)
    parrafo_final_compacto(doc)
# ---------------------------------------------------------------------------
# Inspección
# ---------------------------------------------------------------------------

NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS_M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
NS_PIC = "http://schemas.openxmlformats.org/drawingml/2006/picture"
NS_WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"

PT_CM = 28.3465           # puntos por centímetro
MARGEN_INFERIOR_PT = 70.87  # 2.5 cm


def exportar_pdf(docx: Path, pdf: Path) -> Dict[str, Any]:
    """Exporta a PDF con Word; si no hay Word, con LibreOffice.

    La exportación con Word COM solo existe en Windows. En cualquier otro
    sistema se usa ``soffice --headless``, que respeta la geometría del DOCX
    y sustituye Times New Roman por Liberation Serif, de métricas idénticas.
    """
    try:
        resultado = dq.exportar_docx_a_pdf(docx, pdf)
        normalizar_pdf(pdf, pdf)
        return resultado
    except Exception as error:            # sin Word COM en este sistema
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory() as temporal:
            subprocess.run(["soffice", "--headless", "--norestore",
                            "--convert-to", "pdf", "--outdir", temporal,
                            str(docx)], check=True, capture_output=True,
                           timeout=300)
            generado = Path(temporal) / (docx.stem + ".pdf")
            normalizar_pdf(generado, pdf)
        return {"motor": "libreoffice", "detalle": type(error).__name__}


def normalizar_pdf(origen: Path, destino: Path,
                   sello: str = "D:20260101000000Z") -> None:
    """Fija la fecha del PDF y reescribe el archivo sin basura variable.

    LibreOffice sella la hora de conversión y el identificador del documento,
    de modo que dos compilaciones idénticas daban PDF distintos. Con la fecha
    fija y ``garbage=4`` el archivo depende solo del contenido.
    """
    import fitz
    documento = fitz.open(origen)
    metadatos = documento.metadata or {}
    metadatos["creationDate"] = sello
    metadatos["modDate"] = ""
    documento.set_metadata(metadatos)
    documento.save(destino, garbage=4, deflate=True, no_new_id=True)
    documento.close()
    # PyMuPDF vuelve a sortear el /ID del trailer en cada guardado; se
    # reemplaza por uno derivado del contenido. El reemplazo conserva la
    # longitud, así que los desplazamientos de la tabla xref no cambian.
    crudo = destino.read_bytes()
    patron = re.compile(rb"/ID\[<[0-9A-Fa-f]{32}><[0-9A-Fa-f]{32}>\]")
    fijo = (hashlib.sha256(patron.sub(b"", crudo)).hexdigest().upper()
            [:32].encode())
    destino.write_bytes(patron.sub(b"/ID[<" + fijo + b"><" + fijo + b">]",
                                   crudo))


def sello_compilacion() -> str:
    """Hora de compilación determinista.

    Respeta ``SOURCE_DATE_EPOCH`` (convención de compilación reproducible);
    sin esa variable usa el instante cero del día de la versión. Así el
    manifiesto sale idéntico en cada corrida.
    """
    segundos = os.environ.get("SOURCE_DATE_EPOCH")
    if segundos and segundos.isdigit():
        return datetime.utcfromtimestamp(int(segundos)).isoformat(
            timespec="seconds")
    return "2026-11-03T00:00:00"


def fijar_marcas_zip(ruta: Path, marca: Tuple[int, int, int, int, int, int]
                     = (1980, 1, 1, 0, 0, 0)) -> None:
    """Reescribe el DOCX con fechas de entrada fijas.

    python-docx sella cada entrada del ZIP con la hora de compilación; eso
    hace que el archivo cambie en cada corrida aunque el contenido sea el
    mismo. Con marcas fijas el paquete es reproducible byte a byte.
    """
    with zipfile.ZipFile(ruta) as original:
        entradas = [(i.filename, original.read(i.filename))
                    for i in original.infolist()]
    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as destino:
        for nombre, datos in entradas:
            info = zipfile.ZipInfo(nombre, date_time=marca)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            destino.writestr(info, datos)


def sha256(ruta: Path) -> str:
    digest = hashlib.sha256()
    with open(ruta, "rb") as manejador:
        for bloque in iter(lambda: manejador.read(1 << 20), b""):
            digest.update(bloque)
    return digest.hexdigest()


def _fuentes(raiz_xml) -> list[int]:
    valores = []
    for nodo in raiz_xml.iter(f"{{{NS_W}}}sz"):
        valor = nodo.get(f"{{{NS_W}}}val")
        if valor and valor.isdigit():
            valores.append(int(valor))
    return valores


def inspeccionar_docx(ruta: Path, capturas: Sequence[float],
                      capturas_libres: Sequence[float],
                      codigos: Sequence[str] = _CODIGOS_PROHIBIDOS
                      ) -> Dict[str, Any]:
    """Audita el paquete DOCX: bordes, fuentes, OMML, códigos y encabezado."""
    with zipfile.ZipFile(ruta) as paquete:
        nombres = paquete.namelist()
        xml_doc = paquete.read("word/document.xml").decode("utf-8")
        encabezados = sorted(n for n in nombres
                             if re.fullmatch(r"word/header\d+\.xml", n))
        xml_hdr = (paquete.read(encabezados[0]).decode("utf-8")
                   if encabezados else "")

    raiz = ET.fromstring(xml_doc.encode("utf-8"))
    raiz_hdr = ET.fromstring(xml_hdr.encode("utf-8")) if xml_hdr else None

    tablas = list(raiz.iter(f"{{{NS_W}}}tbl"))
    flotantes = sum(1 for _ in raiz.iter(f"{{{NS_W}}}tblpPr"))

    verticales_tblborders = 0
    for bordes in raiz.iter(f"{{{NS_W}}}tblBorders"):
        for hijo in bordes:
            nombre = hijo.tag.split("}")[-1]
            if nombre in ("left", "right", "insideV"):
                verticales_tblborders += 1
    inside_v = xml_doc.count("<w:insideV")
    verticales_celdas = sum(
        1 for bordes in raiz.iter(f"{{{NS_W}}}tcBorders")
        for hijo in bordes if hijo.tag.split("}")[-1] in ("left", "right"))

    fuentes = _fuentes(raiz)
    fuentes_tablas = [v for tabla in tablas for v in _fuentes(tabla)]
    fuentes_hdr = _fuentes(raiz_hdr) if raiz_hdr is not None else []
    omml = sum(1 for _ in raiz.iter(f"{{{NS_M}}}oMath"))
    imagenes_cuerpo = sum(1 for _ in raiz.iter(f"{{{NS_W}}}drawing"))

    textos = "".join(nodo.text or "" for nodo in raiz.iter(f"{{{NS_W}}}t"))
    hallados = {token: textos.count(token) for token in codigos}
    hallados = {k: v for k, v in hallados.items() if v}

    logotipos = (sum(1 for _ in raiz_hdr.iter(f"{{{NS_PIC}}}pic"))
                 if raiz_hdr is not None else 0)
    alturas_logo = []
    if raiz_hdr is not None:
        for extent in raiz_hdr.iter(f"{{{NS_WP}}}extent"):
            alto = extent.get("cy")
            if alto and alto.isdigit():
                alturas_logo.append(round(int(alto) / 360000.0, 3))

    return {
        "sha256": sha256(ruta),
        "bytes": ruta.stat().st_size,
        "tablas": len(tablas),
        "tablas_flotantes": flotantes,
        "bordes_verticales": verticales_tblborders + verticales_celdas + inside_v,
        "insideV": inside_v,
        "verticales_en_tblBorders": verticales_tblborders,
        "omml": omml,
        "fuente_minima_pt": round(min(fuentes) / 2.0, 1) if fuentes else None,
        "fuente_minima_tablas_pt": (round(min(fuentes_tablas) / 2.0, 1)
                                    if fuentes_tablas else None),
        "fuente_minima_encabezado_pt": (round(min(fuentes_hdr) / 2.0, 1)
                                        if fuentes_hdr else None),
        "logotipos_encabezado": logotipos,
        "altura_logotipo_cm": alturas_logo,
        "header_references": xml_doc.count("<w:headerReference"),
        "imagenes_en_cuerpo": imagenes_cuerpo,
        "codigos_internos": hallados,
        "altura_minima_fila_cm": (min(capturas) if capturas else None),
        "altura_minima_captura_libre_cm": (min(capturas_libres)
                                           if capturas_libres else None),
    }


def inspeccionar_pdf(ruta_pdf: Path) -> Dict[str, Any]:
    """Cuenta páginas y mide la holgura inferior real de cada una."""
    import pymupdf

    documento = pymupdf.open(str(ruta_pdf))
    holguras = []
    try:
        for pagina in documento:
            fondos = [b[3] for b in pagina.get_text("blocks") if b[4].strip()]
            for trazo in pagina.get_drawings():
                caja = trazo.get("rect")
                if caja is not None:
                    fondos.append(caja.y1)
            if not fondos:
                holguras.append(round(24.2, 2))
                continue
            fondo = max(fondos)
            holgura = (pagina.rect.height - MARGEN_INFERIOR_PT - fondo) / PT_CM
            holguras.append(round(holgura, 2))
        paginas = documento.page_count
    finally:
        documento.close()
    return {
        "sha256": sha256(ruta_pdf),
        "paginas": paginas,
        "holguras_por_pagina_cm": holguras,
        "holgura_inferior_cm": holguras[-1] if holguras else None,
    }


# ---------------------------------------------------------------------------
# Documentación del paquete
# ---------------------------------------------------------------------------

META = {
    "00": {
        "titulo": "Guía de aplicación de los instrumentos",
        "que_mide": "No mide: ordena la aplicación de los cinco instrumentos "
                    "y fija las reglas operativas del trabajo de campo.",
        "secciones": ["Instrumentos", "Los cuatro instantes y las dos "
                      "fórmulas", "Reglas operativas"],
        "tablas": ["Instrumentos: 3.1, 4.0, 4.6 y 3.8 cm",
                   "Instantes y fórmulas: 3.1 y 12.4 cm",
                   "Reglas operativas: 3.6 y 11.9 cm"],
        "cambios": [
            "Una sola definición por indicador: T_reg = corte de registro − "
            "inicio; T_vale = emisión − solicitud de despacho.",
            "Once reglas operativas: réplicas y mediana, interrupción externa, "
            "documento conforme (ocho criterios), despacho conforme (igualdad "
            "exacta), hoja de continuación, doble codificación del 20 %, "
            "trabajador ausente, dos centros, operación no ocurrida, "
            "numeración y cálculo de porcentajes.",
        ],
    },
    "01": {
        "titulo": "Ficha de tiempos",
        "que_mide": "Oportunidad de procesamiento: tiempo de registro "
                    "(T_reg) y tiempo de emisión del comprobante o vale "
                    "(T_vale), en minutos.",
        "secciones": ["I. Datos generales", "II. Instrucciones",
                      "III. Contenido", "IV. Observaciones",
                      "V. Responsable"],
        "tablas": ["Datos generales: 3.3, 3.5, 2.5 y 6.2 cm",
                   "Bloques A y B: 0.8, 3.9, 2.5, 2.8, 2.5 y 3.0 cm",
                   "Observaciones: 15.5 cm",
                   "Responsable: 4.1, 4.9, 1.6 y 4.9 cm"],
        "cambios": [
            "El bloque A admite tres réplicas de T_reg y el bloque B tres de "
            "T_vale; la fila identifica el escenario (ingreso, salida, "
            "transferencia; vale regular, reposición, transferencia).",
            "Se añade la columna «Solicitud de despacho», de modo que T_vale = "
            "emisión − solicitud, como en la Ecuación 2.",
            "Se elimina la ficha técnica: sus datos ya están en la guía y en "
            "las instrucciones, y no se llenan en campo.",
            "Cada fila de medición mide 1.0 cm y la hoja cabe en una página.",
        ],
    },
    "02": {
        "titulo": "Ficha documental",
        "que_mide": "Consistencia documental: registros sin discrepancias "
                    "(RSD) y concordancia entre lo programado y lo entregado "
                    "(CPE), en porcentaje.",
        "secciones": ["I. Datos generales", "II. Instrucciones",
                      "III. Bloque A. Documentos auditados (40 por hoja)",
                      "III (continuación). Bloque B. Despachos auditados "
                      "(25 por hoja)", "IV. Observaciones", "V. Responsable"],
        "tablas": ["Datos generales: 3.9, 3.4, 2.9 y 5.3 cm",
                   "Bloque A: 0.8, 1.7, 1.85, 1.95, 1.7, ocho columnas de "
                   "0.75 y 1.3 cm",
                   "Bloque B: 0.8, 1.6, 2.7, 1.9, 1.1, 1.1, 1.1, 3.2 y 2.0 cm",
                   "Cierre IV-V: 8.2 y 7.3 cm"],
        "cambios": [
            "El bloque A pasa a 40 asientos por hoja, con ocho criterios "
            "dicotómicos y una columna Conforme; el bloque B, a 25 despachos. "
            "Ambos con «Hoja __ de __» y numeración corrida.",
            "Cada asiento se identifica con fecha, tipo de documento, número "
            "y lote, de modo que el Sí/No se puede reconstruir.",
            "La regla es conjuntiva y explícita: un solo No anula el "
            "documento.",
            "En el bloque B la conformidad es la igualdad exacta entre "
            "programado y entregado; el documento de ajuste se anota como "
            "observación y no altera la conformidad.",
        ],
    },
    "03": {
        "titulo": "Cuestionario de satisfacción del usuario",
        "que_mide": "Satisfacción del usuario: aceptación del proceso (AP) y "
                    "utilidad percibida (UP), en escala ordinal de 1 a 5.",
        "secciones": ["Ficha técnica", "I. Datos generales",
                      "II. Instrucciones", "III. Contenido"],
        "tablas": ["Ficha técnica: 3.5 y 12.0 cm",
                   "Datos generales: 4.0 y 11.5 cm",
                   "Leyenda de escala: cinco celdas de 3.1 cm",
                   "Reactivos: 0.9, 11.2 y cinco columnas de 0.68 cm"],
        "cambios": [
            "Se restituyen los ocho reactivos: AP-01 a AP-04 y UP-01 a UP-04, "
            "con la escala única de 1 a 5 y los rangos 4–20, 4–20 y 8–40.",
            "Seis enunciados se transcriben literales del expediente DEC-007 "
            "(AP-01 a AP-04, UP-02 y UP-03), que es la redacción que "
            "acompaña a las columnas ap_01…ap_04 y up_01…up_04.",
            "Se reformulan dos enunciados, con decisión anotada: UP-01 "
            "sustituye «en tiempo real» por «cuando la necesito», para que "
            "pueda responderse en el pretest manual; UP-04 deja de ser un "
            "juicio global de eficacia y pasa a una consecuencia concreta, "
            "de modo que ningún ítem de satisfacción global se sume dentro de "
            "UP. El puntaje y el alfa no cambian: dependen de los valores, "
            "no de la redacción.",
            "La separación AP/UP se imprime como banda de subescala; los "
            "códigos de reactivo quedan en la ficha de especificación y el "
            "trabajador solo ve el número de orden.",
        ],
    },
    "04": {
        "titulo": "Consentimiento informado",
        "que_mide": "No mide: acredita la aceptación voluntaria de participar, "
                    "antes de la primera medición.",
        "secciones": ["I. Datos generales del participante",
                      "II. Información al participante", "III. Firmas"],
        "tablas": ["Datos generales: 4.0 y 11.5 cm",
                   "Firmas: dos columnas de 7.75 cm"],
        "cambios": [
            "Se añade la aprobación por comité de ética (o su constancia de "
            "exención) con su número.",
            "Se añade el contacto real del investigador: correo y teléfono.",
            "Se añade la opción de testigo o huella digital para quien no "
            "puede firmar.",
        ],
    },
    "05": {
        "titulo": "Certificado de validación de contenido",
        "que_mide": "No mide: acredita la validez de contenido de los ítems "
                    "por juicio de tres expertos, antes del trabajo de campo.",
        "secciones": ["Ficha técnica", "I. Datos del juez validador",
                      "II. Instrucciones",
                      "III. Matriz de ítems: (a) ficha de tiempos, (b) ficha "
                      "documental, (c) cuestionario",
                      "IV. Observaciones y opinión de aplicabilidad",
                      "V. Firma"],
        "tablas": ["Ficha técnica: 3.5 y 12.0 cm",
                   "Datos del juez: 7.75 y 7.75 cm",
                   "Matriz: 1.2, 7.2, seis columnas de 0.75 y 2.5 cm",
                   "Firma: 4.3, 5.6, 2.0 y 3.6 cm"],
        "cambios": [
            "El certificado queda en blanco: sin nombres, sin V de Aiken y sin "
            "dictamen pre-marcado.",
            "Se estructura en tres secciones, una por instrumento, con los "
            "códigos visibles para el juez: T-01 a T-04, D-01 a D-10 y AP-01 a "
            "UP-04.",
            "Se retiran las hipótesis de cambio: el juez valora instrumentos, "
            "no resultados esperados.",
        ],
    },
}


def escribir_especificaciones(registro: Dict[str, Dict[str, Any]]) -> list[str]:
    """Genera las seis fichas de especificación v06 con las medidas reales."""
    generadas = []
    for clave, _funcion, _orden in DOCUMENTOS:
        codigo = clave[:2]
        meta = META[codigo]
        datos = registro.get(clave)
        if datos is None:
            continue
        lineas = [
            "---",
            "tipo: instrumento",
            "fase: F8",
            "agente: maquetador-docx",
            "estado: borrador",
            "fecha: 2026-11-03",
            "---",
            "",
            "| [Logotipo UNAJMA] | **UNIVERSIDAD NACIONAL JOSÉ MARÍA "
            "ARGUEDAS**<br>Facultad de Ingeniería<br>Escuela Profesional de "
            "Ingeniería de Sistemas | [Logotipo EPIS] |",
            "|---|---|---|",
            "",
            f"# {meta['titulo']}",
            "",
            f"**Archivo:** `{clave}.docx`. **Orden de aplicación:** "
            f"{codigo}. **Páginas:** {datos.get('paginas')}.",
            "",
            "## Función en el trabajo de campo",
            "",
            meta["que_mide"],
            "",
            "## Estructura",
            "",
        ]
        lineas += [f"- {seccion}" for seccion in meta["secciones"]]
        lineas += ["", "## Geometría de las tablas", ""]
        lineas += [f"- {tabla}" for tabla in meta["tablas"]]
        lineas += ["", "## Cambios respecto de v05", ""]
        lineas += [f"- {cambio}" for cambio in meta["cambios"]]
        lineas += [
            "",
            "## Producción",
            "",
            "A4 vertical; margen izquierdo 3.0 cm; superior 3.0 cm; derecho e "
            "inferior 2.5 cm; ancho útil 15.5 cm; distancia del encabezado "
            "0.8 cm. Banda institucional de tres celdas de 2.4, 10.7 y 2.4 cm "
            "en `word/header1.xml`, con altura de fila exacta de 2.0 cm, ambos "
            "logotipos a 1.6 cm y `vAlign` centrado; el cuerpo no contiene "
            "imágenes. Times New Roman 10 pt en el cuerpo y 9.5 pt en las "
            "tablas; ninguna fuente por debajo de 9.5 pt. Bordes: solo líneas "
            "horizontales nativas; ningún `w:tblBorders` lleva `w:left`, "
            "`w:right` ni `w:insideV`. Todas las filas con `cantSplit`; la "
            "fila de encabezado con `tblHeader`. Cero OMML, cero tablas "
            "flotantes y cero códigos internos visibles.",
            "",
            "## Control medido",
            "",
            f"- Bordes verticales: {datos.get('bordes_verticales')}.",
            f"- Tablas flotantes: {datos.get('tablas_flotantes')}.",
            f"- OMML: {datos.get('omml')}.",
            f"- Fuente mínima: {datos.get('fuente_minima_pt')} pt; en "
            f"tablas: {datos.get('fuente_minima_tablas_pt')} pt.",
            f"- Altura mínima de fila de captura: "
            f"{datos.get('altura_minima_fila_cm')} cm.",
            f"- Holgura inferior: "
            f"{datos.get('holgura_inferior_cm')} cm.",
            f"- SHA-256 del DOCX: `{datos.get('sha256')}`.",
            "",
            "## Límites que el maquetador no debe cruzar",
            "",
            "No se altera ni se reordena el contenido de los ítems, los "
            "criterios de conformidad ni las escalas. No se añaden ni se "
            "quitan filas, columnas o documentos. No se escribe ningún código "
            "interno en el formulario. No se colocan fórmulas ni objetos "
            "matemáticos en las celdas. No se rellena ninguna casilla.",
            "",
            "Esta nota no se imprime.",
            "",
        ]
        destino = DIR_FUENTES / f"{clave}.md"
        destino.write_text("\n".join(lineas), encoding="utf-8")
        generadas.append(str(destino))
    return generadas


def escribir_guia_lectura(registro: Dict[str, Dict[str, Any]]) -> Path:
    """Índice del paquete: qué contiene y qué se imprime en campo."""
    filas = []
    for clave, _funcion, _orden in DOCUMENTOS:
        meta = META[clave[:2]]
        datos = registro.get(clave)
        if datos is None:
            continue
        filas.append(
            f"| {clave[:2]} | {meta['titulo']} | "
            f"`01_IMPRIMIBLES/{clave}.pdf` | `02_EDITABLES/{clave}.docx` | "
            f"{datos.get('paginas')} |")
    lineas = [
        "# Paquete de instrumentos definitivos v06",
        "",
        "**Tesis:** Aplicación del sistema SIVAC para mejorar la gestión de "
        "movimientos mensuales de vacunas en el personal de inmunizaciones de "
        "la Dirección de Salud Apurímac II.",
        "",
        "**Fecha de compilación:** 2026-11-03. **Estado:** borrador para "
        "revisión del tesista; no sustituye la aprobación del tesista.",
        "",
        "## Contenido del paquete",
        "",
        "| Carpeta | Contenido |",
        "|---|---|",
        "| `01_IMPRIMIBLES` | Los seis documentos en PDF, listos para "
        "impresión en A4. |",
        "| `02_EDITABLES` | Los seis documentos en DOCX, con estilos nativos "
        "y geometría OpenXML. |",
        "| `03_FUENTES` | Las seis fichas de especificación y el manifiesto "
        "técnico con las huellas SHA-256. |",
        "| `04_CONTROL_VISUAL` | Una imagen PNG por página generada y, en "
        "`antes_v06`, las páginas de la versión anterior para comparar. |",
        "",
        "## Índice de documentos",
        "",
        "| Orden | Documento | Imprimible | Editable | Páginas |",
        "|---|---|---|---|---|",
    ]
    lineas += filas
    lineas += [
        "",
        "## Secuencia de aplicación en campo",
        "",
        "1. **Antes del trabajo de campo:** los tres jueces firman el "
        "certificado de validación (05). Un ejemplar por juez; no se entrega "
        "a los participantes.",
        "2. **Antes de la primera medición:** cada participante firma el "
        "consentimiento informado (04) por duplicado.",
        "3. **Pretest:** se aplican la ficha de tiempos (01), la ficha "
        "documental (02) y el cuestionario (03), en ese orden.",
        "4. **Intervención:** operación del sistema SIVAC. No se usa ningún "
        "formulario.",
        "5. **Postest:** se aplican 01, 02 y 03 en el mismo orden del "
        "pretest.",
        "",
        "## Qué se imprime",
        "",
        "| Documento | Copias |",
        "|---|---|",
        "| 01. Ficha de tiempos | Una hoja por participante y por momento "
        "(pretest y postest). |",
        "| 02. Ficha documental | Una hoja por participante y por momento, "
        "sobre los documentos del periodo revisado. |",
        "| 03. Cuestionario | Una hoja por participante y por momento. |",
        "| 04. Consentimiento | Dos ejemplares por participante, firmados una "
        "sola vez antes de la primera medición. |",
        "| 05. Certificado | Un ejemplar por juez validador, de un solo uso, "
        "firmado antes del trabajo de campo. |",
        "| 00. Guía | Un ejemplar para el investigador. |",
        "",
        "## Reglas de impresión",
        "",
        "A4 vertical, sin escala. Márgenes: izquierdo 3.0 cm, superior "
        "3.0 cm, derecho e inferior 2.5 cm. Times New Roman 10 pt en el "
        "cuerpo y 9.5 pt en las tablas. Las tablas usan solo líneas "
        "horizontales; no llevan líneas verticales. No se imprime ninguna "
        "nota de producción.",
        "",
        "## Reproducibilidad",
        "",
        "El paquete se regenera con:",
        "",
        "```",
        "python scripts/compiladores/instrumentos_recoleccion_v06_builder.py",
        "python scripts/compiladores/concordancia_v06_builder.py",
        "python scripts/compiladores/verificar_instrumentos_v06.py",
        "```",
        "",
        "Dos corridas seguidas producen archivos idénticos byte a byte: el "
        "DOCX se reescribe con fechas de entrada fijas en el ZIP, el PDF se "
        "normaliza (fecha fija e identificador derivado del contenido) y el "
        "manifiesto usa `SOURCE_DATE_EPOCH` o, en su defecto, el instante "
        "cero de la fecha de la versión.",
        "",
    ]
    destino = BASE / "00_LEEME_v06.md"
    destino.write_text("\n".join(lineas), encoding="utf-8")
    return destino


# ---------------------------------------------------------------------------
# Compilación
# ---------------------------------------------------------------------------

DOCUMENTOS: Tuple[Tuple[str, Callable[[Any], None], str], ...] = (
    ("00_GUIA_DE_APLICACION_v06", doc_00, "00"),
    ("01_FICHA_TIEMPOS_v06", doc_01, "01"),
    ("02_FICHA_DOCUMENTAL_v06", doc_02, "02"),
    ("03_CUESTIONARIO_SATISFACCION_v06", doc_03, "03"),
    ("04_CONSENTIMIENTO_INFORMADO_v06", doc_04, "04"),
    ("05_CERTIFICADO_VALIDACION_v06", doc_05, "05"),
)


def preparar_carpetas() -> None:
    for carpeta in (BASE, DIR_IMPRIMIBLES, DIR_EDITABLES, DIR_FUENTES,
                    DIR_CONTROL, DIR_ANTES):
        carpeta.mkdir(parents=True, exist_ok=True)
    if CONTROL_V05.is_dir():
        for png in sorted(CONTROL_V05.glob("*.png")):
            destino = DIR_ANTES / png.name
            if not destino.exists():
                shutil.copy2(png, destino)


def construir(solo: Optional[Sequence[str]] = None, sin_pdf: bool = False,
              sin_render: bool = False, dpi: int = 150) -> Dict[str, Any]:
    preparar_carpetas()
    registro: Dict[str, Dict[str, Any]] = {}

    for nombre, funcion, orden in DOCUMENTOS:
        if solo and orden not in solo:
            continue
        docx = DIR_EDITABLES / f"{nombre}.docx"
        doc = nueva_plantilla()
        funcion(doc)
        doc.save(str(docx))
        fijar_marcas_zip(docx)
        capturas = list(_ESTADO["capturas"])
        libres = list(_ESTADO["capturas_libres"])
        permitidos = (("AP-", "UP-") if orden == "05" else ())
        vigilados = tuple(c for c in _CODIGOS_PROHIBIDOS
                          if not any(c.startswith(p) for p in permitidos))
        datos = inspeccionar_docx(docx, capturas, libres, vigilados)
        datos["docx"] = str(docx)
        datos["capturas_registradas"] = len(capturas)
        datos["alturas_captura_cm"] = sorted(set(capturas))

        pdf = DIR_IMPRIMIBLES / f"{nombre}.pdf"
        datos["pdf"] = str(pdf)
        for obsoleto in DIR_CONTROL.glob(f"{nombre}_p*.png"):
            obsoleto.unlink()
        if not sin_pdf:
            datos["exportacion"] = exportar_pdf(docx, pdf)
            datos.update(inspeccionar_pdf(pdf))
            if not sin_render:
                paginas = list(range(1, datos["paginas"] + 1))
                render = dq.renderizar_paginas_pdf(
                    pdf, paginas, dpi=dpi, salida_dir=DIR_CONTROL)
                datos["png"] = render["renderizadas"]

        registro[nombre] = datos
        print(f"[v06] {nombre}: {datos['tablas']} tablas, "
              f"{datos.get('paginas', '?')} pág., "
              f"{datos['bordes_verticales']} bordes verticales, "
              f"{datos['fuente_minima_pt']} pt mínimo")

    manifiesto = {
        "version": "v06",
        "fecha": "2026-11-03",
        "generado": sello_compilacion(),
        "builder": str(Path(__file__).resolve()),
        "base_v05": str(BASE_V05),
        "paquete": str(BASE),
        "geometria": {
            "pagina": "A4 vertical 11906 x 16838 dxa",
            "margenes_cm": {"izquierdo": 3.0, "superior": 3.0,
                            "derecho": 2.5, "inferior": 2.5},
            "ancho_util_dxa": ANCHO_DXA,
            "alto_util_cm": 24.2,
            "cuerpo_pt": SP / 2,
            "tablas_pt": SP_TABLA / 2,
            "encabezado": "word/header1.xml, banda 2.4 + 10.7 + 2.4 cm, "
                          "fila 2.0 cm, logotipos 1.6 cm",
        },
        "documentos": registro,
        "resumen": {
            "documentos": len(registro),
            "bordes_verticales": sum(d["bordes_verticales"]
                                     for d in registro.values()),
            "insideV": sum(d["insideV"] for d in registro.values()),
            "tablas_flotantes": sum(d["tablas_flotantes"]
                                    for d in registro.values()),
            "omml": sum(d["omml"] for d in registro.values()),
            "fuente_minima_pt": min(d["fuente_minima_pt"]
                                    for d in registro.values()),
            "codigos_internos": sum(sum(d["codigos_internos"].values())
                                    for d in registro.values()),
            "logotipos_encabezado": sorted({d["logotipos_encabezado"]
                                            for d in registro.values()}),
        },
    }

    if not sin_pdf:
        manifiesto["especificaciones"] = escribir_especificaciones(registro)
        manifiesto["leeme"] = str(escribir_guia_lectura(registro))

    destino = DIR_FUENTES / "MANIFIESTO_v06.json"
    destino.write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2),
                       encoding="utf-8")
    print(f"[v06] manifiesto: {destino}")
    return manifiesto


def main(argv: Optional[Sequence[str]] = None) -> int:
    analizador = argparse.ArgumentParser(
        description="Compila el paquete de instrumentos definitivos v06.")
    analizador.add_argument("--solo", default=None,
                            help="códigos separados por coma: 00,01,02")
    analizador.add_argument("--sin-pdf", action="store_true",
                            help="genera solo los DOCX y el manifiesto")
    analizador.add_argument("--sin-render", action="store_true",
                            help="exporta el PDF sin renderizar las páginas")
    analizador.add_argument("--dpi", type=int, default=150)
    argumentos = analizador.parse_args(argv)
    solo = (None if not argumentos.solo
            else [c.strip() for c in argumentos.solo.split(",") if c.strip()])
    manifiesto = construir(solo=solo, sin_pdf=argumentos.sin_pdf,
                           sin_render=argumentos.sin_render,
                           dpi=argumentos.dpi)
    resumen = manifiesto["resumen"]
    print(f"[v06] documentos={resumen['documentos']} "
          f"bordes_verticales={resumen['bordes_verticales']} "
          f"omml={resumen['omml']} "
          f"fuente_minima={resumen['fuente_minima_pt']} pt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
