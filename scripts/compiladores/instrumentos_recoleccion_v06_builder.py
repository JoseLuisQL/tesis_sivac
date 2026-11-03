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

INTERLINEA = {"00": 11.5, "01": 12.0, "02": 12.0, "03": 12.0,
              "04": 12.0, "05": 10.5}

ALINEACION = {
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
    "center": WD_ALIGN_PARAGRAPH.CENTER,
    "both": WD_ALIGN_PARAGRAPH.JUSTIFY,
}

_TOKEN = re.compile(r"(\*\*.+?\*\*)")
_MARCA_CAJA = re.compile(r"(☐)")
_CODIGOS_PROHIBIDOS = ("AP-0", "UP-0", "REG-", "VALE-", "P-0", "C-0", "OP-")

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


def banda_cierre_documental(doc, linea: float = 12.0) -> None:
    """Cierre IV-V en una sola fila de dos columnas, sin líneas verticales."""
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
    fila.height = Cm(1.70)
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

    caja = izq.add_paragraph()
    pf = caja.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Cm(1.0)
    _borde_parrafo(caja, lados=("bottom",))

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
        pf.line_spacing = Cm(0.45)
        add_runs(p, etiqueta + " ", size=SP_TABLA, bold=True)
        add_runs(p, valor, size=SP_TABLA, bold=False)
        _borde_parrafo(p, lados=("bottom",))


# ---------------------------------------------------------------------------
# Documentos
# ---------------------------------------------------------------------------

def doc_00(doc) -> None:
    """Guía de aplicación: índice, secuencia de campo y reglas operativas."""
    li = INTERLINEA["00"]
    titulo(doc, "Guía de aplicación de los instrumentos", line=li)

    rotulo(doc, "Instrumentos", line=li, before=6)
    tabla_registro(doc, [
        ("Instrumento", "Qué mide", "Quién lo llena", "Cuándo"),
        ("01. Ficha de tiempos",
         "Tiempo de registro del movimiento y tiempo de emisión del "
         "comprobante o vale, en minutos",
         "Investigador, por observación directa", "Pretest y postest"),
        ("02. Ficha documental",
         "Porcentaje de documentos sin discrepancias y de despachos conformes",
         "Investigador, por revisión documental",
         "Pretest y postest, sobre treinta días por momento"),
        ("03. Cuestionario de satisfacción",
         "Aceptación del proceso y utilidad percibida, en escala de 1 a 5",
         "Trabajador, sin nombre", "Al final de cada momento"),
        ("04. Consentimiento informado",
         "Aceptación voluntaria de participar",
         "Trabajador e investigador", "Antes de la primera medición"),
        ("05. Certificado de validación",
         "Validez de contenido de los ítems",
         "Tres jueces expertos", "Antes del trabajo de campo"),
    ], (3.2, 5.8, 3.0, 3.5), header_rows=1, linea=li,
        align_defecto="left", flex_col=1, rejilla=False, apa=True)

    rotulo(doc, "Secuencia de aplicación en campo", line=li)
    tabla_registro(doc, [
        ("Paso", "Momento", "Documento", "Quién y copias"),
        ("1", "Validación previa, antes del trabajo de campo",
         "05. Certificado de validación",
         "Tres jueces; un ejemplar por juez"),
        ("2", "Antes de la primera medición",
         "04. Consentimiento informado",
         "Participante e investigador; dos ejemplares por participante"),
        ("3", "Pretest",
         "01. Ficha de tiempos, 02. Ficha documental y 03. Cuestionario, "
         "en ese orden",
         "Una hoja de cada instrumento por participante"),
        ("4", "Intervención", "Sistema SIVAC", "Sin formulario"),
        ("5", "Postest",
         "01, 02 y 03, en el mismo orden del pretest",
         "Una hoja de cada instrumento por participante"),
    ], (1.2, 2.9, 6.4, 5.0), header_rows=1, linea=li,
        align_defecto="left", flex_col=2, rejilla=False, apa=True)
    par(doc, "Se imprime una hoja de la ficha de tiempos, una de la ficha "
             "documental y una del cuestionario por participante y por "
             "momento. El consentimiento se imprime por duplicado una sola "
             "vez por participante. El certificado de validación es de un "
             "solo uso por evaluador: se firma antes del trabajo de campo y "
             "no se entrega a los participantes.", align="both", line=li,
        before=10, after=0)

    rotulo(doc, "Reglas operativas", line=li)
    tabla_registro(doc, [
        ("Regla", "Aplicación"),
        ("1. Cronometraje",
         "Cronómetro; horas en hh:mm:ss; minutos con dos decimales; tres "
         "mediciones por operación, promediadas fuera del formulario; un "
         "tiempo cero o negativo se anula y se repite."),
        ("2. Documento conforme",
         "Cumple los ocho criterios de la ficha documental; un solo criterio "
         "incumplido lo hace no conforme."),
        ("3. Despacho conforme",
         "La cantidad entregada iguala la programada y existe el documento "
         "que lo autoriza; cualquier diferencia lo hace no conforme."),
        ("4. Porcentajes",
         "Documentos conformes entre documentos revisados, por cien. "
         "Despachos conformes entre despachos revisados, por cien. No se "
         "compensan entre sí."),
        ("5. Numeración del trabajador",
         "Del 1 al 14 según la lista del personal de inmunizaciones; el mismo "
         "número en pretest y postest; la lista de nombres se guarda aparte y "
         "se destruye al concluir el informe."),
        ("6. Menos de cinco documentos",
         "Se revisan todos los disponibles y se anota el número real en la "
         "línea de conteo."),
        ("7. Operación no ocurrida",
         "Se registra otra operación del mismo bloque y se anota en "
         "Observación; no se deja la fila vacía."),
    ], (4.2, 11.3), header_rows=1, linea=li, align_defecto="left",
        flex_col=1, rejilla=False, apa=True)
    parrafo_final_compacto(doc)


def doc_01(doc) -> None:
    """Ficha de tiempos: Dimensión 1, oportunidad de procesamiento."""
    li = INTERLINEA["01"]
    titulo(doc, "Ficha de tiempos", line=li)

    ficha_tecnica_cuatro(doc, [
        ("Variable", "Gestión de movimientos mensuales de vacunas",
         "Dimensión", "Oportunidad de procesamiento"),
        ("Indicador", "Tiempo de registro (T_reg) y tiempo de emisión del "
                      "comprobante o vale (T_vale), en minutos", "", ""),
        ("Aplicación", "Pretest y postest; observación directa del "
                       "investigador", "", ""),
    ], linea=li, alturas_cm=(1.0, 1.0, 0.50),
        merges=((1, 1, 1, 3), (2, 1, 2, 3)))

    seccion_romana(doc, "I", "Datos generales", lambda: tabla_registro(doc, [
        ("N.° de trabajador", "", "Centro de salud", ""),
        ("Fecha", "____ / ____ / ________", "Momento",
         "☐ Antes de SIVAC      ☐ Con SIVAC"),
    ], (3.4, 3.4, 2.6, 6.1), header_rows=0, linea=li,
        align_defecto="left", flex_col=3,
        negritas=((0, 0), (0, 2), (1, 0), (1, 2)),
        alturas_cm=(ALTO_CAPTURA, ALTO_CAPTURA), regla_altura="atLeast",
        captura=True), linea=li, before=4, after=2)

    seccion_romana(doc, "II", "Instrucciones", lambda: instrucciones(doc, [
        "Use cronómetro y anote las horas en hh:mm:ss. Exprese el tiempo en "
        "minutos con dos decimales; si resulta cero o negativo, anule la "
        "medición y repítala. Ante una interrupción externa, anótela en "
        "Observación y repita la medición.",
    ], linea=li), linea=li, before=4, after=2)

    cabecera_bloques = ("N.°", "Registro observado", "Hora de inicio",
                        "Hora de fin", "Tiempo (min)", "Observación")
    filas_bloque = [cabecera_bloques] + [("1", "", "", "", "", ""),
                                         ("2", "", "", "", "", ""),
                                         ("3", "", "", "", "", "")]
    alturas_bloque = (0.52, ALTO_CAPTURA, ALTO_CAPTURA, ALTO_CAPTURA)

    def contenido_tiempos() -> None:
        par(doc, "Bloque A. Tiempo de registro del movimiento de vacunas: un "
                 "ingreso, una salida y una transferencia.", bold=True,
            line=li, before=6, after=3, keep=True, keep_lines=True)
        tabla_registro(doc, filas_bloque, (0.8, 5.0, 2.4, 2.4, 2.4, 2.5),
                       header_rows=1, linea=li, align_defecto="center",
                       flex_col=1, alturas_cm=alturas_bloque,
                       regla_altura="atLeast", captura=True)
        par(doc, "Bloque B. Tiempo de emisión del comprobante de salida o "
                 "vale: un vale regular, una reposición urgente y una "
                 "transferencia.", bold=True, line=li, before=6, after=3,
            keep=True, keep_lines=True)
        tabla_registro(doc, filas_bloque, (0.8, 5.0, 2.4, 2.4, 2.4, 2.5),
                       header_rows=1, linea=li, align_defecto="center",
                       flex_col=1, alturas_cm=alturas_bloque,
                       regla_altura="atLeast", captura=True)

    seccion_romana(doc, "III", "Contenido", contenido_tiempos, linea=li,
                   before=4, after=2)

    seccion_romana(doc, "IV", "Observaciones", lambda: tabla_registro(
        doc, [("",), ("",)], (15.5,), header_rows=0, linea=li,
        align_defecto="left", flex_col=0,
        alturas_cm=(ALTO_CAPTURA, ALTO_CAPTURA), regla_altura="atLeast",
        captura=True, margen_tb=MARGEN_TB), linea=li, before=4, after=2)

    seccion_romana(doc, "V", "Responsable", lambda: tabla_registro(doc, [
        ("Nombre del observador", "_" * 24, "Fecha", "____ / ____ / ________"),
        ("Firma", "_" * 46, "", ""),
    ], (4.0, 5.0, 1.6, 4.9), header_rows=0, linea=li,
        align_defecto="left", flex_col=1,
        negritas=((0, 0), (0, 2), (1, 0)),
        alturas_cm=(ALTO_CAPTURA, ALTO_CAPTURA), regla_altura="atLeast",
        captura=True, merges=((1, 1, 1, 3),)), linea=li, before=4, after=2)
    parrafo_final_compacto(doc)
def doc_02(doc) -> None:
    """Ficha documental: Dimensión 2, consistencia documental."""
    li = INTERLINEA["02"]
    lt = 10.5                     # interlineado exacto de las tablas compactas
    mt = MARGEN_TB
    titulo(doc, "Ficha documental", line=li)

    def ficha() -> None:
        rotulo(doc, "Ficha técnica", line=lt, before=2.0)
        tabla_registro(doc, [
            ("Variable", "Gestión de movimientos mensuales de vacunas",
             "Dimensión", "Consistencia documental"),
            ("Indicador", "Registros sin discrepancias (RSD) y concordancia "
                          "entre lo programado y lo entregado (CPE), en "
                          "porcentaje", "", ""),
            ("Aplicación", "Pretest y postest; revisión documental por el "
                           "investigador", "", ""),
        ], (3.6, 4.4, 3.0, 4.5), header_rows=0, linea=lt,
            align_defecto="left", flex_col=3,
            negritas=((0, 0), (0, 2), (1, 0), (2, 0)),
            alturas_cm=(0.72, 0.90, 0.45), regla_altura="atLeast",
            merges=((1, 1, 1, 3), (2, 1, 2, 3)), margen_tb=mt)

    ficha()

    seccion_romana(doc, "I", "Datos generales", lambda: tabla_registro(doc, [
        ("N.° de trabajador", "", "Centro de salud", ""),
        ("Fecha", "____ / ____ / ________", "Momento",
         "☐ Antes de SIVAC\n☐ Con SIVAC"),
        ("Periodo revisado",
         "del ____ / ____ / ________ al ____ / ____ / ________", "", ""),
    ], (4.0, 3.75, 4.0, 3.75), header_rows=0, linea=lt,
        align_defecto="left", flex_col=3,
        negritas=((0, 0), (0, 2), (1, 0), (1, 2), (2, 0)),
        alturas_cm=(0.58, 0.92, 0.58), regla_altura="atLeast",
        captura=True, libre=True, merges=((2, 1, 2, 3),),
        margen_tb=mt), linea=li, before=3, after=2)

    seccion_romana(doc, "II", "Instrucciones", lambda: instrucciones(doc, [
        "Marque Sí o No en cada casilla; un solo No hace no conforme el "
        "documento. Revise los cinco primeros documentos del periodo, en "
        "orden de fecha.",
    ], linea=li), linea=li, before=3, after=2)

    criterios = [
        "Biológico (nombre y presentación)",
        "Lote (número rotulado)",
        "Vencimiento (mes y año)",
        "Cantidad (dosis o frascos)",
        "Centro (código y nombre)",
        "Responsable y firmas (entrega y recepción)",
        "Saldo (inicial, ingresos y salidas)",
        "Correlatividad (fecha y hora)",
        "¿Conforme?",
    ]
    filas_documentos = [("Criterio", "Documento\n1", "Documento\n2",
                         "Documento\n3", "Documento\n4", "Documento\n5")]
    filas_documentos += [(criterio, "", "", "", "", "") for criterio in criterios]
    alturas_documentos = [0.44] * len(filas_documentos)
    alturas_documentos[0] = 0.78      # cabecera en dos líneas
    alturas_documentos[1] = 0.44      # «Biológico (…)»: una línea con 5.8 cm
    alturas_documentos[6] = 0.80      # «Responsable y firmas (…)»

    filas_despachos = [("N.°", "Fecha", "Establecimiento\ndestino",
                        "Programado", "Entregado", "Diferencia",
                        "Documento que\nautoriza", "¿Conforme?")]
    filas_despachos += [(str(n), "", "", "", "", "", "", "")
                        for n in range(1, 11)]
    alturas_despachos = [0.80] + [0.44] * 10

    def contenido_documental() -> None:
        par(doc, "Bloque A. Documentos sin discrepancias: marque Sí o No por "
                 "criterio en cada documento.", bold=True,
            line=li, before=3, after=2, keep=True, keep_lines=True)
        tabla_registro(doc, filas_documentos,
                       (5.8, 1.94, 1.94, 1.94, 1.94, 1.94),
                       header_rows=1, linea=lt, align_defecto="center",
                       flex_col=0, negritas=((r, 0) for r in range(1, 10)),
                       alturas_cm=alturas_documentos, captura=True,
                       margen_tb=mt)
        par(doc, "Bloque B. Despachos: cantidad programada frente a entregada.",
            bold=True, line=li, before=3, after=2, keep=True,
            keep_lines=True)
        tabla_registro(doc, filas_despachos,
                       (0.8, 1.9, 2.6, 2.1, 1.8, 1.8, 2.5, 2.0),
                       header_rows=1, linea=lt, align_defecto="center",
                       flex_col=2, alturas_cm=alturas_despachos, captura=True,
                       margen_tb=mt)

    seccion_romana(doc, "III", "Contenido", contenido_documental, linea=li,
                   before=3, after=2)

    par(doc, "Documentos conformes ____ / revisados ____      Despachos "
             "conformes ____ / revisados ____", size=20, bold=True,
        line=li, before=3, after=0)

    banda_cierre_documental(doc, linea=li)
    parrafo_final_compacto(doc)


def doc_03(doc) -> None:
    """Cuestionario de satisfacción: Dimensión 3, satisfacción del usuario."""
    li = INTERLINEA["03"]
    titulo(doc, "Cuestionario de satisfacción del usuario", line=li)

    ficha_tecnica(doc, [
        ("Variable", "Gestión de movimientos mensuales de vacunas"),
        ("Dimensión", "Satisfacción del usuario"),
        ("Indicador", "Aceptación del proceso (AP) y utilidad percibida (UP), "
                      "en escala ordinal de 1 a 5"),
        ("Aplicación", "Pretest y postest; cuestionario autoadministrado"),
    ], linea=li)

    seccion_romana(doc, "I", "Datos generales", lambda: datos_generales(doc, [
        ("N.° de trabajador", ""),
        ("Momento", "☐ Antes de SIVAC        ☐ Con SIVAC"),
        ("Fecha", "____ / ____ / ________"),
        ("Centro de salud", ""),
    ], linea=li), linea=li, before=6)

    def instrucciones_y_escala() -> None:
        par(doc, "Marque con una X un solo número por afirmación. No escriba "
                 "su nombre; sus respuestas son confidenciales.", align="both",
            line=li, before=0, after=4)
        leyenda_escala(doc, linea=li)

    seccion_romana(doc, "II", "Instrucciones", instrucciones_y_escala,
                   linea=li, before=6)

    reactivos = [
        ("N.°", "Afirmación", "1", "2", "3", "4", "5"),
        ("1", "El procedimiento actual para asentar los movimientos diarios y "
              "cierres de mes es ágil y no demanda un esfuerzo mental o físico "
              "excesivo.", "", "", "", "", ""),
        ("2", "El flujo de trabajo requerido para emitir comprobantes de salida "
              "y vales de entrega es fluido y está libre de demoras o trabas "
              "burocráticas.", "", "", "", "", ""),
        ("3", "El método empleado me permite conciliar los saldos de inventario "
              "con las microredes generando tranquilidad y reduciendo el estrés "
              "laboral.", "", "", "", "", ""),
        ("4", "El tiempo que dedico al registro administrativo de vacunas es "
              "equilibrado y me deja disponibilidad para mis labores sanitarias "
              "y asistenciales.", "", "", "", "", ""),
        ("5", "El mecanismo de registro utilizado me permite disponer de "
              "información fidedigna y en tiempo real del stock de vacunas y "
              "jeringas.", "", "", "", "", ""),
        ("6", "El control de números de lote y fechas de vencimiento que brinda "
              "el proceso previene oportunamente mermas o pérdidas de "
              "biológicos.", "", "", "", "", ""),
        ("7", "La metodología de gestión facilita la detección inmediata y "
              "rectificación de cualquier descuadre de inventario físico versus "
              "registrado.", "", "", "", "", ""),
        ("8", "En general, considero que el procedimiento empleado es una "
              "herramienta altamente eficaz para garantizar el abastecimiento "
              "oportuno de vacunas.", "", "", "", "", ""),
    ]
    seccion_romana(doc, "III", "Contenido", lambda: tabla_registro(
        doc, reactivos, (0.8, 11.45, 0.65, 0.65, 0.65, 0.65, 0.65),
        header_rows=1, linea=li, align_defecto="left", flex_col=1,
        negritas=((r, 0) for r in range(1, 9)),
        alto_filas_cm=ALTO_CAPTURA_HOLGADO, regla_altura="atLeast",
        captura=True, libre=True), linea=li, before=6)

    par(doc, "Gracias por su participación.", align="left", line=li,
        before=8, after=0)
    parrafo_final_compacto(doc)


def doc_04(doc) -> None:
    """Consentimiento informado: documento ético transversal."""
    li = INTERLINEA["04"]
    titulo(doc, "Consentimiento informado para participar en la investigación",
           line=li)

    seccion_romana(doc, "I", "Datos generales del participante",
                   lambda: datos_generales(doc, [
                       ("N.° de trabajador", ""),
                       ("Centro de salud", ""),
                       ("Fecha", "____ / ____ / ________"),
                   ], linea=li), linea=li, before=6)

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
        ("7. Contacto.", "Para consultas, comuníquese con el investigador."),
        ("8. Declaración de consentimiento.", "He leído y comprendido la "
         "información. Mis preguntas fueron respondidas. Acepto participar "
         "voluntariamente."),
    ]

    def informacion() -> None:
        par(doc, "Estimado(a) participante:", line=li, after=0)
        for lead, texto in bloques:
            par(doc, f"**{lead}** {texto}", line=li, before=8, after=0)
            if lead.startswith("7."):
                par(doc, "Correo electrónico: ______________________    "
                         "Teléfono: ______________________", line=li, after=0)

    seccion_romana(doc, "II", "Información al participante", informacion,
                   linea=li, before=8)

    seccion_romana(doc, "III", "Firmas", lambda: tabla_registro(doc, [
        ("Participante", "Investigador"),
        ("Nombre: ______________________________",
         "Nombre: ______________________________"),
        ("Firma: ______________________________",
         "Firma: ______________________________"),
        ("Fecha: ____ / ____ / ________",
         "Fecha: ____ / ____ / ________"),
    ], (7.75, 7.75), header_rows=1, linea=li, align_defecto="left",
        flex_col=0, alturas_cm=(0.60, 1.15, 1.35, 1.00),
        regla_altura="atLeast", captura=True, libre=True), linea=li,
        before=8)

    par(doc, "Este documento se emite por duplicado: una copia para el "
             "participante y otra para el investigador.", line=li, before=8,
        after=0)
    parrafo_final_compacto(doc)


def doc_05(doc) -> None:
    """Certificado de validación de contenido: documento transversal previo."""
    li = INTERLINEA["05"]
    lt = 10.5          # matriz: interlineado exacto de la especificación
    titulo(doc, "Certificado de validación de contenido", line=10.0)

    ficha_tecnica(doc, [
        ("Variable", "Gestión de movimientos mensuales de vacunas"),
        ("Dimensión", "Todas"),
        ("Indicador", "Los seis indicadores de la variable dependiente"),
        ("Aplicación", "Juicio de expertos, tres jueces"),
    ], linea=10.0, con_cabecera=False, alturas_cm=(0.50,) * 4)

    seccion_romana(doc, "I", "Datos del juez validador",
                   lambda: tabla_registro(doc, [
                       ("Apellidos y nombres: ______________________________",
                        "DNI: ____________________"),
                       ("Especialidad: ______________________________",
                        "Institución: ______________________________"),
                       ("Fecha: ____ de ____________________ de 2026", ""),
                   ], (7.75, 7.75), header_rows=0, linea=10.0,
                       align_defecto="left", flex_col=0,
                       alturas_cm=(0.55, 0.55, 0.55), regla_altura="atLeast",
                       captura=True, libre=True), linea=10.0)

    seccion_romana(doc, "II", "Instrucciones", lambda: instrucciones(doc, [
        "Marque Sí o No en cada criterio y por cada ítem. Use la columna "
        "Sugerencias para indicar mejoras. Las definiciones de los criterios "
        "figuran al pie de la tabla.",
    ], linea=li), linea=10.0)

    items = [
        "El tiempo que demora el trabajador en registrar un movimiento de "
        "vacunas, en minutos, permite valorar la oportunidad de procesamiento.",
        "El tiempo que demora el trabajador en emitir el comprobante o vale, "
        "en minutos, permite valorar la oportunidad de procesamiento.",
        "La reducción del tiempo de registro entre pretest y postest mejora "
        "la oportunidad de procesamiento.",
        "La reducción del tiempo del vale entre pretest y postest mejora la "
        "oportunidad de procesamiento.",
        "El porcentaje de documentos sin discrepancias permite valorar la "
        "consistencia documental.",
        "El porcentaje de despachos conformes permite valorar la "
        "consistencia documental.",
        "El aumento de documentos sin discrepancias entre pretest y postest "
        "mejora la consistencia documental.",
        "El aumento de despachos conformes entre pretest y postest mejora la "
        "consistencia documental.",
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
        "El mecanismo de registro utilizado me permite disponer de "
        "información fidedigna y en tiempo real del stock de vacunas y "
        "jeringas.",
        "El control de números de lote y fechas de vencimiento que brinda el "
        "proceso previene oportunamente mermas o pérdidas de biológicos.",
        "La metodología de gestión facilita la detección inmediata y "
        "rectificación de cualquier descuadre de inventario físico versus "
        "registrado.",
        "En general, considero que el procedimiento empleado es una "
        "herramienta altamente eficaz para garantizar el abastecimiento "
        "oportuno de vacunas.",
    ]

    filas_matriz = [
        ("N.°", "DIMENSIONES / Ítems", "Pertinencia", "", "Relevancia",
         "", "Claridad", "", "Sugerencias"),
        ("", "", "Sí", "No", "Sí", "No", "Sí", "No", ""),
        ("**Dimensión 1. Oportunidad de procesamiento (ítems 1 a 4)**",
         "", "", "", "", "", "", "", ""),
    ]
    negritas_matriz = [(2, 0)]
    for numero, texto in enumerate(items, start=1):
        filas_matriz.append((str(numero), texto, "", "", "", "", "", "", ""))
    filas_matriz.insert(7, ("**Dimensión 2. Consistencia documental "
                               "(ítems 5 a 8)**", "", "", "", "", "", "",
                             ""))
    negritas_matriz.append((7, 0))
    filas_matriz.insert(12, ("**Dimensión 3. Satisfacción del usuario "
                                "(ítems 9 a 16)**", "", "", "", "", "", "",
                             ""))
    negritas_matriz.append((12, 0))
    merges_matriz = [
        (0, 2, 0, 3), (0, 4, 0, 5), (0, 6, 0, 7),
        (2, 0, 2, 8), (7, 0, 7, 8), (12, 0, 12, 8),
    ]

    def matriz() -> None:
        tabla_registro(
            doc, filas_matriz,
            (0.7, 6.95, 0.975, 0.975, 0.975, 0.975, 0.975, 0.975, 2.0),
            header_rows=2, linea=lt, align_defecto="left",
            align_cols=("center", "left", "center", "center", "center",
                        "center", "center", "center", "center"),
            negritas=negritas_matriz, flex_col=1,
            margen_lr=MARGEN_LR, margen_tb=MARGEN_TB,
            merges=merges_matriz)

    seccion_romana(doc, "III", "Matriz de ítems", matriz, linea=10.0)

    par(doc, "**Notas al pie**", line=9.5, before=8, after=3)
    notas = [
        "1. **Pertinencia:** el ítem corresponde al concepto teórico formulado.",
        "2. **Relevancia:** el ítem es apropiado para representar al componente "
        "o dimensión específica del constructo.",
        "3. **Claridad:** el enunciado se entiende sin dificultad alguna; es "
        "conciso, exacto y directo.",
    ]
    for nota in notas:
        par(doc, nota, size=SP_TABLA, line=9.5, before=0, after=0)

    seccion_romana(doc, "IV", "Observaciones y opinión de aplicabilidad",
                   lambda: (
                       par(doc, "**Observaciones (precisar si hay "
                                "suficiencia):** ______________________________",
                           line=10.0, after=0),
                       par(doc, "**Opinión de aplicabilidad:** ☐ Aplicable   "
                                "☐ Aplicable después de corregir   "
                                "☐ No aplicable", size=SP_TABLA, line=10.0,
                           after=0),
                   ), linea=10.0)

    seccion_romana(doc, "V", "Firma", lambda: tabla_registro(
        doc, [("Firma del juez validador", "", "Fecha", "")], (5.0, 5.5, 1.5, 3.5),
        header_rows=0, linea=li, align_defecto="left", flex_col=1,
        negritas=((0, 0), (0, 2)),
        alturas_cm=(1.40,), regla_altura="atLeast", captura=True,
        libre=True), linea=10.0)
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
                      capturas_libres: Sequence[float]) -> Dict[str, Any]:
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
    codigos = {token: textos.count(token) for token in _CODIGOS_PROHIBIDOS}
    codigos = {k: v for k, v in codigos.items() if v}

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
        "codigos_internos": codigos,
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
        "secciones": ["Instrumentos", "Secuencia de aplicación en campo",
                      "Reglas operativas"],
        "tablas": ["Instrumentos: 3.2, 5.8, 3.0 y 3.5 cm",
                   "Secuencia de aplicación: 1.2, 2.9, 6.4 y 5.0 cm",
                   "Reglas operativas: 4.2 y 11.3 cm"],
        "cambios": [
            "Se añade la tabla «Secuencia de aplicación en campo» con los "
            "cinco pasos reales: certificado antes del campo, consentimiento "
            "antes de la primera medición, pretest 01, 02 y 03, intervención "
            "SIVAC y postest en el mismo orden.",
            "Se explicita qué se imprime por participante y qué documento es "
            "de un solo uso por evaluador.",
        ],
    },
    "01": {
        "titulo": "Ficha de tiempos",
        "que_mide": "Oportunidad de procesamiento: tiempo de registro "
                    "(T_reg) y tiempo de emisión del comprobante o vale "
                    "(T_vale), en minutos.",
        "secciones": ["Ficha técnica", "I. Datos generales",
                      "II. Instrucciones", "III. Contenido",
                      "IV. Observaciones", "V. Responsable"],
        "tablas": ["Ficha técnica: 3.6, 4.4, 3.0 y 4.5 cm",
                   "Datos generales: 3.4, 3.4, 2.6 y 6.1 cm",
                   "Bloques A y B: 0.8, 5.0, 2.4, 2.4, 2.4 y 2.5 cm",
                   "Observaciones: 15.5 cm",
                   "Responsable: 4.0, 5.0, 1.6 y 4.9 cm"],
        "cambios": [
            "Las seis filas de medición suben de 0.68 cm a 1.0 cm.",
            "Las dos filas de observaciones y las filas de datos generales "
            "suben a 1.0 cm.",
            "La ficha técnica pasa a cuatro columnas con la fila del "
            "indicador y la de aplicación en 1.0 cm.",
        ],
    },
    "02": {
        "titulo": "Ficha documental",
        "que_mide": "Consistencia documental: registros sin discrepancias "
                    "(RSD) y concordancia entre lo programado y lo entregado "
                    "(CPE), en porcentaje.",
        "secciones": ["Ficha técnica", "I. Datos generales",
                      "II. Instrucciones", "III. Contenido",
                      "IV. Observaciones", "V. Responsable"],
        "tablas": ["Ficha técnica: 3.6, 4.4, 3.0 y 4.5 cm",
                   "Datos generales: 4.0, 3.75, 4.0 y 3.75 cm",
                   "Bloque A: 5.8 cm y cinco columnas de 1.94 cm",
                   "Bloque B: 0.8, 1.9, 2.6, 2.1, 1.8, 1.8, 2.5 y 2.0 cm",
                   "Cierre IV-V: 8.2 y 7.3 cm"],
        "cambios": [
            "El bloque A conserva los nueve criterios y los cinco documentos; "
            "el bloque B conserva los diez despachos.",
            "Se recupera holgura con separaciones de 4 pt para que el cierre "
            "no quede al ras del margen inferior.",
            "La columna de documento mide 1.94 cm en lugar de 1.10 cm, para "
            "que «Documento 1» a «Documento 5» se lean completos.",
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
                   "Reactivos: 0.8, 11.45 y cinco columnas de 0.65 cm"],
        "cambios": [
            "La explicación corrida de la escala se sustituye por una banda "
            "horizontal de cinco celdas, una por valor, con su rótulo.",
            "Las ocho filas de respuesta suben a 1.15 cm y las cuatro filas "
            "de datos generales a 1.0 cm.",
            "Los ocho enunciados, su orden y la escala 1 a 5 se conservan "
            "literalmente.",
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
            "Las tres filas de datos generales y las tres filas de firmas "
            "suben a 1.0 cm como mínimo, con la fila de firma en 1.35 cm.",
            "Los ocho bloques de información se conservan textualmente, con "
            "aire de 8 pt entre ellos.",
        ],
    },
    "05": {
        "titulo": "Certificado de validación de contenido",
        "que_mide": "No mide: acredita la validez de contenido de los ítems "
                    "por juicio de tres expertos, antes del trabajo de campo.",
        "secciones": ["Ficha técnica", "I. Datos del juez validador",
                      "II. Instrucciones", "III. Matriz de ítems",
                      "IV. Observaciones y opinión de aplicabilidad",
                      "V. Firma"],
        "tablas": ["Ficha técnica: 3.5 y 12.0 cm",
                   "Datos del juez: 7.75 y 7.75 cm",
                   "Matriz: 0.7, 6.95, seis columnas de 0.975, 2.0 cm",
                   "Firma: 5.0, 5.5, 1.5 y 3.5 cm"],
        "cambios": [
            "Los 16 ítems, las tres dimensiones y los tres criterios de "
            "juicio se conservan; la matriz ocupa dos páginas.",
            "Las filas de datos del juez y de firma ganan altura de escritura.",
        ],
    },
}


def escribir_especificaciones(registro: Dict[str, Dict[str, Any]]) -> list[str]:
    """Genera las seis fichas de especificación v06 con las medidas reales."""
    generadas = []
    for clave, _funcion, _orden in DOCUMENTOS:
        codigo = clave[:2]
        meta = META[codigo]
        datos = registro[clave]
        lineas = [
            "---",
            "tipo: instrumento",
            "fase: F8",
            "agente: maquetador-docx",
            "estado: borrador",
            "fecha: 2026-11-02",
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
        lineas += [f"{i}. {seccion}"
                   for i, seccion in enumerate(meta["secciones"], start=1)]
        lineas += ["", "## Geometría de las tablas", ""]
        lineas += [f"- {tabla}" for tabla in meta["tablas"]]
        lineas += ["", "## Cambios autorizados respecto de v05", ""]
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
        datos = registro[clave]
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
        "**Fecha de compilación:** 2026-11-02. **Estado:** borrador para "
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
        capturas = list(_ESTADO["capturas"])
        libres = list(_ESTADO["capturas_libres"])
        datos = inspeccionar_docx(docx, capturas, libres)
        datos["docx"] = str(docx)
        datos["capturas_registradas"] = len(capturas)
        datos["alturas_captura_cm"] = sorted(set(capturas))

        pdf = DIR_IMPRIMIBLES / f"{nombre}.pdf"
        datos["pdf"] = str(pdf)
        if not sin_pdf:
            dq.exportar_docx_a_pdf(docx, pdf)
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
        "fecha": "2026-11-02",
        "generado": datetime.now().isoformat(timespec="seconds"),
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
