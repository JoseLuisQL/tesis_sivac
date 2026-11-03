# -*- coding: utf-8 -*-
"""Constructor de los instrumentos definitivos SIVAC v05.

Compila las especificaciones Markdown cerradas de
``salidas/instrumentos/INSTRUMENTOS_DEFINITIVOS_v05/_ESPECIFICACION`` a
documentos DOCX de una sola página, sus PDF oficiales, un PNG de control por
página y el ``MANIFIESTO_v05.json``.

Geometría común
---------------
* A4 vertical 11906 x 16838 dxa. Márgenes: izquierdo 1701 dxa (3.0 cm);
  superior, derecho e inferior 1417 dxa (2.5 cm). Ancho útil 8788 dxa.
* Times New Roman 10 pt en el cuerpo y 9.5 pt en las tablas. Ninguna fuente
  por debajo de 9.5 pt; si un bloque no cabe se recorta contenido, nunca el
  tamaño de letra.
* Interlineado sencillo exacto: 12 pt en los formularios 00 a 03.
* Banda institucional única delegada en ``docx_quirurgico.banda_institucional``
  (2.4 + 10.7 + 2.4 cm = 15.5 cm; altura exacta 2.2 cm; logotipos de 1.9 cm).
* Rejilla visible de 0.5 pt solo en las tablas de los formularios 01 a 03. La
  guía 00 usa las tres líneas horizontales APA 7. Cero sombreado.
* Cero OMML y cero fórmulas dentro de celdas.

Uso
---
    python scripts/compiladores/instrumentos_recoleccion_v05_builder.py
    python scripts/compiladores/instrumentos_recoleccion_v05_builder.py --solo 02
    python scripts/compiladores/instrumentos_recoleccion_v05_builder.py --sin-pdf
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
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

BASE = RAIZ / "salidas" / "instrumentos" / "INSTRUMENTOS_DEFINITIVOS_v05"
ESPEC = BASE / "_ESPECIFICACION"
ASSETS_V03 = (RAIZ / "salidas" / "instrumentos" /
              "INSTRUMENTOS_REDISENADOS_FANY_20261102_v03" / "_assets")
LOGO_UNAJMA = ASSETS_V03 / "LOGO-UNAJMA-recorte.png"
LOGO_EPIS = ASSETS_V03 / "LOGO-EPIS.jpg"
CONTROL = BASE / "_control_visual"

ANCHO_DXA = 8788          # 15.5 cm
DXA_CM = 567.0            # twips por centímetro
SP = 20                   # 10.0 pt en medios puntos
SP_TABLA = 19             # 9.5 pt en medios puntos
MARGEN_LR = 57            # 1 mm lateral
MARGEN_TB = 28            # 0.5 mm vertical

# Ritmo vertical unificado PMI-05, sección 3. Todo espacio se expresa en
# puntos y se aplica por igual a los seis instrumentos.
ESP_TITULO_ANTES = 12.0
ESP_TITULO_DESPUES = 2.0
ESP_FICHA_ANTES = 8.0
ESP_FICHA_DESPUES = 2.0
ESP_ANTES = 12.0          # rótulo de sección romana
ESP_DESPUES = 4.0
ESP_BLOQUE_ANTES = 8.0    # rótulo de bloque (Bloque A / Bloque B)
ESP_BLOQUE_DESPUES = 4.0
ESP_PROSA_ANTES = 2.0
ESP_PROSA_DESPUES = 2.0
ESP_CONTEO_ANTES = 4.0
ESP_CONTEO_DESPUES = 8.0

ALTO_FILA_MARCA_CM = 0.6      # PMI-05, sección 6: marcado o llenado
ALTO_FILA_ESCRITURA_CM = 0.68  # PMI-05, sección 6: escritura manuscrita

BANDA_ALTO_CM = 2.0       # altura exacta de la banda del encabezado
LOGO_ALTO_CM = 1.6        # altura exacta de cada logotipo
BANDA_ANCHOS_CM = (2.4, 10.7, 2.4)

INTERLINEA = {"00": 12.0, "01": 12.0, "02": 12.0, "03": 12.0}

ALINEACION = {
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
    "center": WD_ALIGN_PARAGRAPH.CENTER,
    "both": WD_ALIGN_PARAGRAPH.JUSTIFY,
}

_TOKEN = re.compile(r"(\*\*.+?\*\*)")
_MARCA_CAJA = re.compile(r"(☐)")
_CODIGOS_PROHIBIDOS = ("AP-0", "UP-0", "REG-", "VALE-", "P-0", "C-0", "OP-")

_ESTADO: Dict[str, Any] = {"hdr": []}


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


def titulo(doc, texto: str, line: float = 17.0,
           before: float = ESP_TITULO_ANTES):
    """Título del documento: negrita 14 pt, 12 pt antes y 2 pt después."""
    return par(doc, texto, size=28, bold=True, before=before,
               after=ESP_TITULO_DESPUES, line=17.0, keep=True,
               keep_lines=True)


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
    """Rótulo de sección: negrita 10 pt, 12 pt antes y 4 pt después.

    El interlineado exacto nunca baja de 12 pt para no recortar el texto de
    10 pt. El espacio mínimo de 12 pt separa además cualquier rótulo del
    borde inferior de la tabla que lo precede.
    """
    return par(doc, texto, size=SP, bold=True, before=before, after=after,
               line=max(line, 12.0), keep=True, keep_lines=True)


def configurar_encabezado(doc) -> None:
    """Crea ``word/header1.xml`` con la banda institucional nativa.

    La banda deja de ser una tabla del cuerpo y pasa a la parte de encabezado
    del paquete: tabla de tres celdas sin bordes, fila de 2.0 cm exactos y
    logotipos de 1.6 cm insertados como imágenes del encabezado. No se crea
    pie de página ni ``w:footerReference``.
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
    tblPr = tabla._tbl.tblPr
    previo = tblPr.find(qn("w:tblBorders"))
    if previo is not None:
        tblPr.remove(previo)
    bordes = OxmlElement("w:tblBorders")
    for borde in ("top", "left", "bottom", "right", "insideH", "insideV"):
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


def _reiniciar_celda(celda):
    tc = celda._tc
    for p in tc.findall(qn("w:p"))[1:]:
        tc.remove(p)
    p = celda.paragraphs[0]
    for hijo in list(p._element):
        if hijo.tag != qn("w:pPr"):
            p._element.remove(hijo)
    return p


def _texto_vertical(celda) -> None:
    """Gira el contenido de una celda a lectura vertical nativa (btLr).

    OpenXML permite rotar el flujo del texto dentro de la celda sin recurrir a
    guiones blandos ni a abreviaturas. La cabecera del Bloque B de la ficha
    documental usa esta dirección para que los rótulos completos quepan en
    columnas estrechas conservando las diez columnas y los diez datos.
    """
    tcPr = celda._tc.get_or_add_tcPr()
    previo = tcPr.find(qn("w:textDirection"))
    if previo is not None:
        tcPr.remove(previo)
    direccion = OxmlElement("w:textDirection")
    direccion.set(qn("w:val"), "btLr")
    tcPr.insert_element_before(
        direccion, "w:tcFitText", "w:vAlign", "w:hideMark", "w:headers",
        "w:cellIns", "w:cellDel", "w:cellMerge", "w:tcPrChange",
    )
    celda.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


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


def _borde_parrafo(parrafo, lados=("top", "left", "bottom", "right"),
                   sz: int = 4) -> None:
    """Dibuja un borde nativo alrededor (o al pie) de un párrafo vacío."""
    pPr = parrafo._p.get_or_add_pPr()
    previo = pPr.find(qn("w:pBdr"))
    if previo is not None:
        pPr.remove(previo)
    bordes = OxmlElement("w:pBdr")
    for lado in ("top", "left", "bottom", "right"):
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


def banda_cierre_documental(doc, linea: float = 12.0) -> None:
    """Cierre IV-V en una sola fila de dos columnas, sin partir ni huérfanos."""
    t = doc.add_table(rows=1, cols=2)
    t.style = None
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    dq._fijar_margenes_celda_tabla(t._tbl, MARGEN_LR, MARGEN_LR,
                                   MARGEN_TB, MARGEN_TB)
    _geometria(t, _dxa((8.2, 7.3), 1))
    dq.eliminar_flotacion_tabla(t)
    dq.aplicar_bordes_campo(t, exterior_sz=4, interior_sz=4)

    fila = t.rows[0]
    fila.height = Twips(1000)
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
    pf.line_spacing = Cm(1.1)
    _borde_parrafo(caja)

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
# Bloques compartidos
# ---------------------------------------------------------------------------

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
                   margen_lr: int = MARGEN_LR, margen_tb: int = MARGEN_TB,
                   merges: Sequence[Tuple[int, int, int, int]] = (),
                   vertical_cols: Sequence[int] = ()):
    """Tabla de registro con geometría exacta y protección de filas.

    ``rejilla`` dibuja la cuadrícula de 0.5 pt de los formularios; ``apa``
    aplica las tres líneas horizontales de la guía. ``alto_filas_cm`` fija una
    altura mínima de escritura y ``alto_exacto_cm`` una altura exacta para
    filas de captura vacías. ``alturas_cm`` prevalece sobre ambos y permite
    fijar una altura exacta distinta por fila; ``None`` deja la fila con el
    alto automático que exija su contenido. ``vertical_cols`` gira la cabecera
    de las columnas indicadas a lectura vertical nativa (btLr).
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

    for r in range(header_rows):
        for c in vertical_cols:
            _texto_vertical(t.cell(r, c))

    for i, fila in enumerate(t.rows):
        dq._preparar_tr(fila._tr, cant_split=True,
                        tbl_header=(i < header_rows))
        if alturas_cm is not None and i < len(alturas_cm) \
                and alturas_cm[i] is not None:
            fila.height = Cm(alturas_cm[i])
            fila.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
        elif i >= header_rows:
            if alto_exacto_cm is not None:
                fila.height = Cm(alto_exacto_cm)
                fila.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
            elif alto_filas_cm is not None:
                fila.height = Cm(alto_filas_cm)
                fila.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST

    _geometria(t, anchos_dxa)
    dq.eliminar_flotacion_tabla(t)
    if rejilla:
        dq.aplicar_bordes_campo(t, exterior_sz=4, interior_sz=4)
    elif apa:
        dq.aplicar_bordes_apa7_tabla(t)
    else:
        _sin_bordes(t)
    return t


def ficha_tecnica(doc, filas: Sequence[Tuple[str, str]],
                  linea: float = 12.0, con_cabecera: bool = False,
                  alturas_cm: Optional[Sequence[Optional[float]]] = None,
                  margen_tb: int = MARGEN_TB,
                  before: float = ESP_FICHA_ANTES) -> None:
    """Encabezado «Ficha técnica» y tabla Campo/Valor de 3.5 + 12.0 cm.

    Formato único PMI-05, sección 4: dos columnas y las cuatro filas
    Variable, Dimensión, Indicador y Aplicación. ``con_cabecera`` añade la
    fila «Campo | Valor»; la usan 01, 02, 03 y 05.
    """
    rotulo(doc, "Ficha técnica", line=linea, before=before,
           after=ESP_FICHA_DESPUES)
    cuerpo = ([("Campo", "Valor")] + list(filas) if con_cabecera
              else list(filas))
    inicio_datos = 1 if con_cabecera else 0
    if alturas_cm is None:
        alturas_cm = [None] * len(filas)
    alturas = ([ALTO_FILA_MARCA_CM] + list(alturas_cm) if con_cabecera
               else list(alturas_cm))
    tabla_registro(doc, cuerpo, (3.5, 12.0),
                   header_rows=1 if con_cabecera else 0,
                   linea=linea, align_defecto="left", flex_col=1,
                   negritas=tuple((i, 0)
                                  for i in range(inicio_datos, len(cuerpo))),
                   alturas_cm=alturas,
                   alto_filas_cm=ALTO_FILA_MARCA_CM, margen_tb=margen_tb)


def datos_generales(doc, pares: Sequence[Tuple[str, str]],
                    linea: float = 12.0,
                    alto_filas_cm: float = ALTO_FILA_MARCA_CM,
                    con_cabecera: bool = False,
                    alturas_cm: Optional[Sequence[Optional[float]]] = None,
                    margen_tb: int = MARGEN_TB) -> None:
    """Tabla Campo/Registro de 4.0 + 11.5 cm con filas de 0.6 cm.

    ``con_cabecera`` añade la fila «Campo | Registro»; la usan 01, 02, 03
    y 04.
    """
    cuerpo = ([("Campo", "Registro")] + list(pares) if con_cabecera
              else list(pares))
    inicio_datos = 1 if con_cabecera else 0
    if alturas_cm is None:
        alturas_cm = [None] * len(pares)
    alturas = ([ALTO_FILA_MARCA_CM] + list(alturas_cm) if con_cabecera
               else list(alturas_cm))
    tabla_registro(doc, cuerpo, (4.0, 11.5),
                   header_rows=1 if con_cabecera else 0,
                   linea=linea, align_defecto="left", flex_col=1,
                   alto_filas_cm=alto_filas_cm, alturas_cm=alturas,
                   negritas=tuple((i, 0)
                                  for i in range(inicio_datos, len(cuerpo))),
                   margen_tb=margen_tb)


def instrucciones(doc, lineas: Sequence[str], linea: float = 12.0,
                  after: float = ESP_PROSA_DESPUES,
                  before: float = ESP_PROSA_ANTES) -> None:
    """Párrafos de instrucciones justificados, sin sangría, con 2/2 pt."""
    for texto in lineas:
        par(doc, texto, align="both", line=max(linea, 12.0),
            before=before, after=after)


def caja_observaciones(doc, alto_cm: float = 2.0) -> None:
    """Recuadro vacío de 15.5 cm con borde visible y alto exacto PMI-05."""
    caja = doc.add_table(rows=1, cols=1)
    caja.style = None
    caja.alignment = WD_TABLE_ALIGNMENT.LEFT
    caja.autofit = False
    dq._fijar_margenes_celda_tabla(caja._tbl, MARGEN_LR, MARGEN_LR,
                                   MARGEN_TB, MARGEN_TB)
    _geometria(caja, _dxa((15.5,), 0))
    dq.eliminar_flotacion_tabla(caja)
    dq.aplicar_bordes_campo(caja, exterior_sz=4, interior_sz=4)
    fila = caja.rows[0]
    fila.height = Cm(alto_cm)
    fila.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
    dq._preparar_tr(fila._tr, cant_split=True, tbl_header=False)
    celda = caja.cell(0, 0)
    celda.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
    _fijar_margen_celda(celda, MARGEN_LR, MARGEN_TB)
    p = _reiniciar_celda(celda)
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(9.5)


def seccion_romana(doc, numero: str, titulo_seccion: str,
                   cuerpo: Callable[[], None], linea: float = 12.0,
                   before: float = ESP_ANTES,
                   after: float = ESP_DESPUES) -> None:
    """Rótulo «I. Título» y ejecución del bloque de contenido que le sigue."""
    rotulo(doc, f"{numero}. {titulo_seccion}", line=linea, before=before,
           after=after)
    cuerpo()


# ---------------------------------------------------------------------------
# Documentos
# ---------------------------------------------------------------------------

def doc_00(doc) -> None:
    li = INTERLINEA["00"]
    titulo(doc, "Guía de aplicación de los instrumentos", line=li)

    rotulo(doc, "Instrumentos", line=li, before=ESP_ANTES,
           after=ESP_DESPUES)
    tabla_registro(doc, [
        ("Instrumento", "Qué mide", "Quién lo llena", "Cuándo"),
        ("Ficha de tiempos",
         "Tiempos de registro y de emisión del comprobante o vale, en "
         "minutos, medidos sobre la salida regular de vacunas",
         "Investigador, por observación directa", "Pretest y postest"),
        ("Ficha documental",
         "Porcentaje de documentos sin discrepancias (seis criterios) y de "
         "despachos conformes, sobre cinco documentos y cinco despachos por "
         "momento",
         "Investigador, por revisión documental",
         "Pretest y postest, sobre treinta días por momento"),
        ("Cuestionario de satisfacción",
         "Aceptación del proceso y utilidad percibida, en escala de 1 a 5",
         "Trabajador, sin nombre", "Al final de cada momento"),
        ("Consentimiento informado",
         "Aceptación voluntaria de participar",
         "Trabajador e investigador", "Antes de la primera medición"),
        ("Certificado de validación",
         "Validez de contenido de los catorce ítems",
         "Tres jueces expertos", "Antes del trabajo de campo"),
    ], (3.2, 5.8, 3.0, 3.5), header_rows=1, linea=li,
        align_defecto="left", flex_col=1, rejilla=False, apa=True)

    rotulo(doc, "Reglas operativas", line=li)
    tabla_registro(doc, [
        ("Regla", "Aplicación"),
        ("1. Operación estándar",
         "Se cronometra únicamente la salida regular de vacunas. El inicio "
         "se marca cuando el trabajador dispone del documento fuente completo "
         "y comienza el registro; el corte de registro, cuando el movimiento "
         "queda registrado y guardado; el fin, cuando el comprobante o vale "
         "está emitido y disponible. T_reg va del inicio al corte de "
         "registro. T_vale va del corte de registro a la emisión del vale, de "
         "modo que no incluye T_reg y la suma no se consigna como indicador. "
         "El valor del trabajador es la mediana de sus tres mediciones "
         "válidas, calculada fuera del formulario."),
        ("2. Cronometraje",
         "Cronómetro; horas en hh:mm:ss; minutos con dos decimales; tres "
         "mediciones válidas por trabajador y momento; si una se invalida, "
         "se repite; un tiempo cero o negativo se anula y se repite."),
        ("3. Documento conforme",
         "Cumple los seis criterios de la ficha documental, de modo que todos "
         "los campos aplicables coinciden con el documento fuente; un solo "
         "criterio incumplido lo hace no conforme. La cantidad se compara en "
         "la misma unidad consignada en el documento fuente."),
        ("4. Despacho conforme",
         "La cantidad entregada coincide con la programada en la misma "
         "unidad; si hay diferencia, solo es conforme si existe documento de "
         "ajuste, devolución, modificación o autorización formal con fecha e "
         "identificación verificable."),
        ("5. Porcentajes",
         "Documentos conformes entre documentos revisados, por cien. "
         "Despachos conformes entre despachos revisados, por cien. No se "
         "compensan entre sí."),
        ("6. Numeración del trabajador",
         "Del 1 al 14 según la lista del personal de inmunizaciones; el mismo "
         "número en pretest y postest; la lista de nombres se guarda aparte y "
         "se destruye al concluir el informe."),
        ("7. Menos de cinco documentos",
         "Se revisan todos los disponibles y se anota el número real en la "
         "línea de conteo."),
        ("8. Operación no ocurrida",
         "Se registra la siguiente salida regular del mismo trabajador dentro "
         "del periodo y se anota en Observación; no se deja la fila vacía ni "
         "se fabrica la medición."),
    ], (4.2, 11.3), header_rows=1, linea=li, align_defecto="left",
        flex_col=1, rejilla=False, apa=True)
    parrafo_final_compacto(doc)


def doc_01(doc) -> None:
    li = INTERLINEA["01"]
    titulo(doc, "Cuestionario de satisfacción del usuario", line=li)

    ficha_tecnica(doc, [
        ("Variable", "Gestión de movimientos mensuales de vacunas"),
        ("Dimensión", "Satisfacción del usuario"),
        ("Indicador", "Aceptación del proceso (AP) y utilidad percibida (UP), "
                      "en escala ordinal de 1 a 5"),
        ("Aplicación", "Pretest y postest; cuestionario autoadministrado"),
    ], linea=li, con_cabecera=True)

    seccion_romana(doc, "I", "Datos generales", lambda: datos_generales(doc, [
        ("N.° de trabajador", ""),
        ("Centro de salud", ""),
        ("Fecha", "____ / ____ / ________"),
        ("Momento", "☐ Antes de SIVAC\n☐ Con SIVAC"),
    ], linea=li, con_cabecera=True,
        alturas_cm=(None, None, None, 0.95)), linea=li)

    seccion_romana(doc, "II", "Instrucciones", lambda: instrucciones(doc, [
        "Marque una sola alternativa por afirmación, considerando su "
        "experiencia durante los últimos 30 días de gestión de movimientos "
        "mensuales de vacunas. No escriba su nombre; sus respuestas son "
        "confidenciales.",
        "1 = Totalmente en desacuerdo; 2 = En desacuerdo; 3 = Ni de acuerdo "
        "ni en desacuerdo; 4 = De acuerdo; 5 = Totalmente de acuerdo.",
    ], linea=li), linea=li)

    reactivos = [
        ("N.°", "Afirmación", "1", "2", "3", "4", "5"),
        ("1", "El procedimiento utilizado para registrar movimientos de "
              "vacunas es fácil de realizar.", "", "", "", "", ""),
        ("2", "El procedimiento utilizado permite registrar los movimientos "
              "de vacunas en un tiempo razonable.", "", "", "", "", ""),
        ("3", "El procedimiento utilizado facilita la emisión de comprobantes "
              "o vales de salida.", "", "", "", "", ""),
        ("4", "El procedimiento utilizado permite consultar la información de "
              "movimientos de vacunas cuando se necesita.", "", "", "", "", ""),
        ("5", "El procedimiento utilizado facilita el control de lotes y "
              "fechas de vencimiento de las vacunas.", "", "", "", "", ""),
        ("6", "En general, estoy satisfecho con el procedimiento utilizado "
              "para gestionar los movimientos mensuales de vacunas.",
         "", "", "", "", ""),
    ]
    seccion_romana(doc, "III", "Contenido", lambda: tabla_registro(
        doc, reactivos, (0.8, 11.45, 0.65, 0.65, 0.65, 0.65, 0.65),
        header_rows=1, linea=li, align_defecto="left", flex_col=1,
        align_cols=("center", "left", "center", "center", "center",
                    "center", "center"),
        negritas=((r, 0) for r in range(1, 7)),
        alturas_cm=(ALTO_FILA_MARCA_CM,) + (None,) * 6,
        alto_filas_cm=ALTO_FILA_MARCA_CM), linea=li)

    par(doc, "Gracias por su participación.", align="left", line=li,
        before=ESP_ANTES, after=0)
    parrafo_final_compacto(doc)


def doc_02(doc) -> None:
    li = INTERLINEA["02"]
    # Excepción autorizada para 02: título 4 pt antes, rótulos romanos 5/2 y
    # prosa de instrucciones 0/0. La sección II se compone en dos párrafos y
    # la regla de T_reg y T_vale queda en su cuerpo; III no lleva nota. Con la
    # caja de IV a 1.2 cm, IV y V cierran en la misma página.
    lb = 5.0
    ab = 2.0
    titulo(doc, "Ficha de tiempos", line=li, before=4.0)

    ficha_tecnica(doc, [
        ("Variable", "Gestión de movimientos mensuales de vacunas"),
        ("Dimensión", "Oportunidad de procesamiento"),
        ("Indicador", "Tiempo de registro (T_reg) y tiempo de emisión del "
                      "comprobante o vale (T_vale), en minutos"),
        ("Aplicación", "Pretest y postest; observación directa del "
                       "investigador"),
    ], linea=li, con_cabecera=True,
        alturas_cm=(ALTO_FILA_MARCA_CM, ALTO_FILA_MARCA_CM, None,
                    ALTO_FILA_MARCA_CM))

    seccion_romana(doc, "I", "Datos generales", lambda: datos_generales(doc, [
        ("N.° de trabajador", ""),
        ("Centro de salud", ""),
        ("Fecha", "____ / ____ / ________"),
        ("Momento", "☐ Antes de SIVAC　　☐ Con SIVAC"),
    ], linea=li, con_cabecera=True,
        alturas_cm=(ALTO_FILA_MARCA_CM, ALTO_FILA_MARCA_CM,
                    ALTO_FILA_MARCA_CM, ALTO_FILA_MARCA_CM)),
        linea=li, before=lb, after=ab)

    seccion_romana(doc, "II", "Instrucciones", lambda: instrucciones(doc, [
        "Use cronómetro y anote las horas en hh:mm:ss; exprese los minutos "
        "con dos decimales y anule y repita la medición cuyo tiempo resulte "
        "cero o negativo. Se cronometra una sola operación estándar, la "
        "salida regular de vacunas: el inicio se marca cuando el trabajador "
        "dispone del documento fuente completo y comienza el registro; el "
        "corte de registro, cuando el movimiento queda registrado y guardado; "
        "el fin, cuando el comprobante o vale está emitido y disponible. "
        "T_reg va del inicio al corte de registro; T_vale va del corte de "
        "registro a la emisión del vale, de modo que no incluye T_reg y la "
        "suma no se consigna como indicador.",
        "Se excluyen las interrupciones externas: llamadas telefónicas, "
        "atención a usuarios no relacionada con la operación, fallas de "
        "energía e interrupciones o esperas de terceros. Se incluyen búsqueda "
        "de información, digitación, revisión, corrección de errores propios "
        "y generación del comprobante. Registre tres mediciones válidas por "
        "momento por trabajador, repita la medición invalidada y tome la "
        "mediana de las tres como valor del trabajador, calculada fuera del "
        "formulario.",
    ], linea=li, before=0.0, after=0.0), linea=li, before=lb, after=ab)

    filas_medicion = [
        ("N.°", "Fecha", "Hora de inicio", "Hora de fin de registro",
         "T_reg (min)", "Hora de emisión del vale", "T_vale (min)",
         "Interrupción externa", "¿Medición válida?"),
        ("1", "", "", "", "", "", "", "", ""),
        ("2", "", "", "", "", "", "", "", ""),
        ("3", "", "", "", "", "", "", "", ""),
    ]

    def contenido_tiempos() -> None:
        par(doc, "**Salida regular de vacunas: tres mediciones válidas por "
                 "trabajador.**", line=li, before=ESP_BLOQUE_ANTES,
            after=ESP_BLOQUE_DESPUES, keep=True, keep_lines=True)
        tabla_registro(
            doc, filas_medicion,
            (0.8, 1.6, 1.7, 1.9, 1.5, 1.9, 1.5, 2.8, 1.8),
            header_rows=1, linea=li, align_defecto="center", flex_col=1,
            align_cols=("center", "center", "center", "center", "center",
                        "center", "center", "left", "center"),
            alturas_cm=(None, ALTO_FILA_MARCA_CM, ALTO_FILA_MARCA_CM,
                        ALTO_FILA_MARCA_CM))

    seccion_romana(doc, "III", "Contenido", contenido_tiempos, linea=li,
                   before=lb, after=ab)

    # La regla de T_reg y T_vale quedó integrada en el cuerpo de II; por eso
    # III no lleva nota. La caja de IV se reduce al mínimo autorizado de
    # 1.2 cm para dejar la holgura inferior de PMI-05 §9 y mantener IV y V en
    # la misma página.
    seccion_romana(doc, "IV", "Observaciones",
                   lambda: caja_observaciones(doc, 1.2), linea=li,
                   before=lb, after=ab)

    seccion_romana(doc, "V", "Responsable", lambda: tabla_registro(doc, [
        ("Nombre del observador", ""),
        ("Firma", ""),
        ("Fecha", "____ / ____ / ____"),
    ], (4.0, 11.5), header_rows=0, linea=li, align_defecto="left",
        flex_col=1, negritas=((0, 0), (1, 0), (2, 0)),
        alturas_cm=(0.55, 0.55, 0.55)), linea=li, before=lb, after=ab)
    parrafo_final_compacto(doc)


def doc_03(doc) -> None:
    """Ficha documental con la forma única PMI-05.

    Dos tablas de captura con filas de 0.6 cm, ficha técnica de dos columnas
    y cierre IV-V unificado. El Bloque B fluye entre la página 1 y la 2 con la
    cabecera repetida y sin partir filas, para que ninguna página quede con
    más de 3 cm de blanco al pie. Como PMI-05 prohíbe reducir la tipografía o
    eliminar filas, el instrumento ocupa dos páginas.
    """
    li = INTERLINEA["03"]
    lt = 10.5                     # interlineado exacto de tablas
    titulo(doc, "Ficha documental", line=li, before=6.0)

    ficha_tecnica(doc, [
        ("Variable", "Gestión de movimientos mensuales de vacunas"),
        ("Dimensión", "Consistencia documental"),
        ("Indicador", "Registros sin discrepancias (RSD) y concordancia entre "
                      "lo programado y lo entregado (CPE), en porcentaje"),
        ("Aplicación", "Pretest y postest; revisión documental por el "
                       "investigador"),
    ], linea=lt, con_cabecera=True, before=4.0)

    seccion_romana(doc, "I", "Datos generales",
                   lambda: datos_generales(doc, [
                       ("N.° de trabajador", ""),
                       ("Centro de salud", ""),
                       ("Fecha", "____ / ____ / ________"),
                       ("Momento", "☐ Antes de SIVAC　　☐ Con SIVAC"),
                       ("Periodo revisado",
                        "del ____ / ____ / ________ al ____ / ____ / ________"),
                   ], linea=lt, con_cabecera=True,
                       alturas_cm=(None, None, None, ALTO_FILA_MARCA_CM,
                                   None)), linea=li, before=10.0)

    seccion_romana(doc, "II", "Instrucciones", lambda: instrucciones(doc, [
        "Marque Sí o No en cada criterio. El documento es conforme solo si "
        "todos los campos aplicables coinciden con el documento fuente; la "
        "cantidad se compara en la misma unidad consignada en el documento "
        "fuente.",
        "Seleccione cinco documentos de movimiento elegibles distribuidos "
        "durante todo el periodo: uno del inicio, uno del primer tercio, uno "
        "de la mitad, uno del último tercio y uno del final. Un documento es "
        "elegible si corresponde a un movimiento del trabajador evaluado, "
        "tiene fecha dentro del periodo, permite identificar el movimiento de "
        "vacunas, cuenta con documento fuente de contraste y contiene "
        "información suficiente para verificar los seis criterios.",
        "En el Bloque B, un despacho es conforme cuando la cantidad entregada "
        "coincide con la programada en la misma unidad; si hay diferencia, "
        "solo es conforme si existe documento de ajuste, devolución, "
        "modificación o autorización formal con fecha e identificación "
        "verificable.",
    ], linea=li), linea=li, before=10.0)

    criterios = [
        "Biológico (nombre y presentación)",
        "Lote (número rotulado)",
        "Vencimiento (mes y año)",
        "Cantidad (según la unidad registrada)",
        "Establecimiento (código y nombre)",
        "Responsable y firmas (entrega y recepción)",
        "Unidad registrada (apoyo, no puntúa)",
        "¿Conforme?",
    ]
    filas_documentos = [("Criterio\n(Sí o No)", "Documento\n1",
                         "Documento\n2", "Documento\n3", "Documento\n4",
                         "Documento\n5")]
    filas_documentos += [(criterio, "", "", "", "", "") for criterio in criterios]
    alturas_documentos = [ALTO_FILA_MARCA_CM] * len(filas_documentos)
    alturas_documentos[0] = 0.75      # cabecera en dos líneas
    alturas_documentos[6] = 0.75      # «Responsable y firmas (…)»: dos líneas
    alturas_documentos[7] = ALTO_FILA_MARCA_CM  # «Unidad registrada (…)»: una

    # Cabecera vertical nativa (btLr) en las ocho columnas descriptivas del
    # Bloque B. Conserva las diez columnas y los diez datos, mantiene 9.5 pt y
    # permite que «Establecimiento», «Programado», «Entregado», «Diferencia»
    # y «¿Conforme?» se lean completos, sin guiones blandos ni abreviaturas.
    filas_despachos = [("N.°", "Fecha", "Establecimiento\ndestino",
                        "Programado", "Entregado",
                        "Diferencia", "Documento que\nautoriza",
                        "¿Ajuste\nautorizado?", "Código\ndel ajuste",
                        "¿Conforme?")]
    filas_despachos += [(str(n), "", "", "", "", "", "", "", "", "")
                        for n in range(1, 6)]
    alturas_despachos = [2.9] + [ALTO_FILA_MARCA_CM] * 5

    def contenido_documental() -> None:
        par(doc, "Bloque A. Documentos sin discrepancias: marque Sí o No por "
                 "criterio en cada documento.", bold=True,
            line=li, before=ESP_BLOQUE_ANTES, after=ESP_BLOQUE_DESPUES,
            keep=True, keep_lines=True)
        tabla_registro(doc, filas_documentos,
                       (5.8, 1.94, 1.94, 1.94, 1.94, 1.94),
                       header_rows=1, linea=lt, align_defecto="center",
                       flex_col=0, negritas=((r, 0) for r in range(1, 9)),
                       alturas_cm=alturas_documentos)
        # Conteo del Bloque A inmediatamente bajo su propia tabla.
        par(doc, "**Documentos conformes** ____ de ____ revisados",
            size=SP, line=11.0, before=2.0, after=4.0)
        par(doc, "Bloque B. Despachos: cantidad programada frente a "
                 "entregada; cinco despachos por momento.", bold=True,
            line=li, before=ESP_BLOQUE_ANTES, after=ESP_BLOQUE_DESPUES,
            keep=True, keep_lines=True)
        # El Bloque B fluye desde la página 1: la tabla se parte entre filas,
        # nunca dentro de una fila (cantSplit) y repite la cabecera (tblHeader).
        tabla_registro(doc, filas_despachos,
                       (0.7, 1.4, 2.1, 1.5, 1.5, 1.4, 1.9, 1.7, 1.6, 1.7),
                       header_rows=1, linea=lt, align_defecto="center",
                       flex_col=2, alturas_cm=alturas_despachos,
                       vertical_cols=tuple(range(2, 10)))
        # Conteo del Bloque B inmediatamente bajo su propia tabla.
        par(doc, "**Despachos conformes** ____ de ____ revisados",
            size=SP, line=12.0, before=ESP_CONTEO_ANTES,
            after=ESP_CONTEO_DESPUES)

    seccion_romana(doc, "III", "Contenido", contenido_documental, linea=li,
                   before=10.0)

    seccion_romana(doc, "IV", "Observaciones",
                   lambda: caja_observaciones(doc, 4.0), linea=li)

    seccion_romana(doc, "V", "Responsable", lambda: tabla_registro(doc, [
        ("Nombre del observador", ""),
        ("Firma", ""),
        ("Fecha", "____ / ____ / ____"),
    ], (4.0, 11.5), header_rows=0, linea=li, align_defecto="left",
        flex_col=1, negritas=((0, 0), (1, 0), (2, 0)),
        alturas_cm=(0.6, 0.6, 0.6)), linea=li)

    parrafo_final_compacto(doc)


def doc_04(doc) -> None:
    li = 12.0
    titulo(doc, "Consentimiento informado para participar en la investigación",
           line=li)

    seccion_romana(doc, "I", "Datos generales del participante",
                   lambda: datos_generales(doc, [
                       ("N.° de trabajador", ""),
                       ("Centro de salud", ""),
                       ("Fecha", "____ / ____ / ________"),
                   ], linea=li, con_cabecera=True), linea=li)

    bloques = [
        ("1. Propósito.", "Esta investigación evalúa si el sistema SIVAC "
         "mejora la gestión de los movimientos mensuales de vacunas en el "
         "personal de inmunizaciones de la Dirección de Salud Apurímac II."),
        ("2. Procedimiento.", "Se observará y cronometrará cómo registra un "
         "movimiento de vacunas y cómo emite el comprobante de salida o vale. "
         "Se revisarán los documentos de movimiento de un periodo de treinta "
         "días y se le aplicará un cuestionario de seis preguntas. La "
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
        par(doc, "Estimado(a) participante:", line=li, align="both",
            before=ESP_PROSA_ANTES, after=ESP_PROSA_DESPUES)
        for lead, texto in bloques:
            par(doc, f"**{lead}** {texto}", line=li, align="both",
                before=ESP_PROSA_ANTES, after=ESP_PROSA_DESPUES)
            if lead.startswith("7."):
                par(doc, "Correo electrónico: ______________________    "
                         "Teléfono: ______________________", line=li,
                    before=ESP_PROSA_ANTES, after=ESP_PROSA_DESPUES)

    seccion_romana(doc, "II", "Información al participante", informacion,
                   linea=li)

    seccion_romana(doc, "III", "Firmas", lambda: tabla_registro(doc, [
        ("Participante", "Investigador"),
        ("Nombre: ______________________________",
         "Nombre: ______________________________"),
        ("Firma: ______________________________",
         "Firma: ______________________________"),
        ("Fecha: ____ / ____ / ________",
         "Fecha: ____ / ____ / ________"),
    ], (7.75, 7.75), header_rows=1, linea=li, align_defecto="left",
        flex_col=0, alturas_cm=(0.9, 0.9, 0.9, 0.9)), linea=li)

    par(doc, "Este documento se emite por duplicado: una copia para el "
             "participante y otra para el investigador.", line=li,
        before=ESP_ANTES, after=0)
    parrafo_final_compacto(doc)


def doc_05(doc) -> None:
    """Certificado de validación de contenido en dos páginas exactas.

    Matriz dicotómica de catorce ítems con Pertinencia, Relevancia y
    Claridad subdivididas en Sí y No, conforme al modelo vigente por DEC-015
    y a la estructura consolidada por DEC-024. Página 1: título, ficha
    técnica, datos del juez, instrucciones y encabezado de la matriz.
    Página 2: matriz continuada, notas, observaciones y firma. La rejilla es
    visible porque el documento es un formulario institucional firmable y no
    una tabla de resultados APA 7.
    """
    lt = 10.5          # interlineado exacto de la matriz
    li = 13.0          # cuerpo restante del certificado

    titulo(doc, "Certificado de validación de contenido")

    ficha_tecnica(doc, [
        ("Variable", "Gestión de movimientos mensuales de vacunas"),
        ("Dimensión", "Todas"),
        ("Indicador", "Los seis indicadores de la variable dependiente"),
        ("Aplicación", "Juicio de expertos, tres jueces"),
    ], linea=12.0, con_cabecera=True)

    seccion_romana(doc, "I", "Datos del juez validador",
                   lambda: datos_generales(doc, [
                       ("Apellidos y nombres", ""),
                       ("DNI", ""),
                       ("Especialidad", ""),
                       ("Institución", ""),
                       ("Fecha", "____ de ____________________ de 2026"),
                   ], linea=12.0, con_cabecera=True), linea=li)

    seccion_romana(doc, "II", "Instrucciones", lambda: instrucciones(doc, [
        "Marque Sí o No en cada criterio y por cada ítem. Use la columna "
        "Sugerencias para indicar mejoras. Las definiciones de los criterios "
        "figuran al pie de la tabla.",
    ], linea=li), linea=li)

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
        "El procedimiento utilizado para registrar movimientos de vacunas es "
        "fácil de realizar.",
        "El procedimiento utilizado permite registrar los movimientos de "
        "vacunas en un tiempo razonable.",
        "El procedimiento utilizado facilita la emisión de comprobantes o "
        "vales de salida.",
        "El procedimiento utilizado permite consultar la información de "
        "movimientos de vacunas cuando se necesita.",
        "El procedimiento utilizado facilita el control de lotes y fechas de "
        "vencimiento de las vacunas.",
        "En general, estoy satisfecho con el procedimiento utilizado para "
        "gestionar los movimientos mensuales de vacunas.",
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
                                "(ítems 9 a 14)**", "", "", "", "", "", "",
                             ""))
    negritas_matriz.append((12, 0))
    merges_matriz = [
        (0, 0, 1, 0), (0, 1, 1, 1),
        (0, 2, 0, 3), (0, 4, 0, 5), (0, 6, 0, 7), (0, 8, 1, 8),
        (2, 0, 2, 8), (7, 0, 7, 8), (12, 0, 12, 8),
    ]

    def matriz() -> None:
        t = tabla_registro(
            doc, filas_matriz,
            (0.7, 6.95, 0.975, 0.975, 0.975, 0.975, 0.975, 0.975, 2.0),
            header_rows=2, linea=lt, align_defecto="left",
            align_cols=("center", "left", "center", "center", "center",
                        "center", "center", "center", "center"),
            negritas=negritas_matriz, flex_col=1,
            margen_lr=MARGEN_LR, margen_tb=MARGEN_TB,
            merges=merges_matriz,
            alturas_cm=(ALTO_FILA_MARCA_CM, ALTO_FILA_MARCA_CM)
            + (None,) * (len(filas_matriz) - 2),
            alto_filas_cm=ALTO_FILA_MARCA_CM)
        # Cada rótulo de dimensión viaja con el primer ítem que introduce:
        # ninguna dimensión queda sola al pie de una página.
        for indice in (2, 7, 12):
            for celda in t.rows[indice].cells:
                for p in celda.paragraphs:
                    p.paragraph_format.keep_with_next = True

    seccion_romana(doc, "III", "Matriz de ítems", matriz, linea=li)

    par(doc, "**Notas al pie**", line=12.0, before=ESP_ANTES,
        after=ESP_BLOQUE_DESPUES)
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
                       # La línea de guiones no invade el renglón siguiente:
                       # el párrafo reserva 12 pt de aire posterior.
                       par(doc, "**Observaciones (precisar si hay "
                                "suficiencia):** " + "_" * 30,
                           line=13.0, after=12),
                       par(doc, "**Opinión de aplicabilidad:**", line=13.0,
                           before=6, after=5),
                       # Tres renglones independientes y sangrados: cada
                       # casilla conserva su enunciado (unión con espacio
                       # duro) y queda con espacio suficiente para marcarla.
                       par(doc, "☐  Aplicable", size=SP_TABLA,
                           line=li, after=7, left=0.9),
                       par(doc, "☐  Aplicable después de corregir",
                           size=SP_TABLA, line=li, after=7, left=0.9),
                       par(doc, "☐  No aplicable", size=SP_TABLA,
                           line=li, after=0, left=0.9),
                   ), linea=li)

    def firma() -> None:
        # Área libre de firma por encima de la rúbrica: 2.98 cm reales para la
        # firma manuscrita y el sello del juez. Sin recuadro, sin rejilla y
        # sin sombreado. El DNI no se repite aquí porque ya se captura en la
        # sección I.
        par(doc, "", line=84.5, after=0)
        rubrica = par(doc, "", line=1.0, after=0, align="center")
        rubrica.paragraph_format.left_indent = Cm(4.075)
        rubrica.paragraph_format.right_indent = Cm(4.075)
        _borde_parrafo(rubrica, lados=("bottom",), sz=6)
        par(doc, "Firma y sello del juez validador", size=SP_TABLA,
            align="center", line=11.5, before=3, after=0)

    # 12 pt separan la última línea de la sección IV del rótulo V; el área
    # libre de firma de 2.98 cm se reserva con el espaciador de la sección.
    seccion_romana(doc, "V", "Firma", firma, linea=li)
    parrafo_final_compacto(doc)


DOCUMENTOS = (
    ("00_GUIA_DE_APLICACION_v05", doc_00, "00"),
    ("01_CUESTIONARIO_SATISFACCION_v05", doc_01, "01"),
    ("02_FICHA_TIEMPOS_v05", doc_02, "02"),
    ("03_FICHA_DOCUMENTAL_v05", doc_03, "03"),
    ("04_CONSENTIMIENTO_INFORMADO_v05", doc_04, "04"),
    ("05_CERTIFICADO_VALIDACION_v05", doc_05, "05"),
)


# ---------------------------------------------------------------------------
# Inspección, exportación y manifiesto
# ---------------------------------------------------------------------------

def sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as fh:
        for bloque in iter(lambda: fh.read(65536), b""):
            h.update(bloque)
    return h.hexdigest()


def inspeccionar_docx(ruta: Path) -> Dict[str, Any]:
    W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
    WP = ("http://schemas.openxmlformats.org/drawingml/2006/"
          "wordprocessingDrawing")
    with zipfile.ZipFile(ruta) as z:
        nombres = z.namelist()
        raiz = ET.fromstring(z.read("word/document.xml"))
        partes_encabezado = sorted(n for n in nombres
                                   if re.fullmatch(r"word/header\d+\.xml", n))
        encabezado = (ET.fromstring(z.read("word/header1.xml"))
                      if "word/header1.xml" in nombres else None)

    tamanos = []
    tamanos_tabla = []
    textos = []
    for tc in raiz.iter(f"{{{W}}}tc"):
        for nodo in tc.iter(f"{{{W}}}sz"):
            try:
                tamanos_tabla.append(int(nodo.get(f"{{{W}}}val")))
            except (TypeError, ValueError):
                pass
    for nodo in raiz.iter(f"{{{W}}}sz"):
        try:
            tamanos.append(int(nodo.get(f"{{{W}}}val")))
        except (TypeError, ValueError):
            pass
    for t in raiz.iter(f"{{{W}}}t"):
        if t.text:
            textos.append(t.text)
    texto_total = "".join(textos)

    omml = sum(1 for _ in raiz.iter(f"{{{M}}}oMath"))
    omml_celdas = sum(1 for tc in raiz.iter(f"{{{W}}}tc")
                      for _ in tc.iter(f"{{{M}}}oMath"))
    flotantes = sum(1 for _ in raiz.iter(f"{{{W}}}tblpPr"))
    anchos = []
    for tbl in raiz.iter(f"{{{W}}}tbl"):
        grid = tbl.find(f"{{{W}}}tblGrid")
        if grid is None:
            continue
        suma = 0
        for gc in grid.findall(f"{{{W}}}gridCol"):
            try:
                suma += int(gc.get(f"{{{W}}}w"))
            except (TypeError, ValueError):
                pass
        anchos.append(suma)

    sectPr = raiz.find(f".//{{{W}}}sectPr")
    pgMar = sectPr.find(f"{{{W}}}pgMar") if sectPr is not None else None
    referencias_encabezado = sum(
        1 for _ in raiz.iter(f"{{{W}}}headerReference"))
    referencias_pie = sum(1 for _ in raiz.iter(f"{{{W}}}footerReference"))
    dibujos_cuerpo = sum(1 for _ in raiz.iter(f"{{{W}}}drawing"))

    tamanos_encabezado = []
    dibujos_encabezado = 0
    tablas_encabezado = 0
    ancho_encabezado = None
    alto_fila_encabezado = None
    alturas_logo_cm = []
    if encabezado is not None:
        for nodo in encabezado.iter(f"{{{W}}}sz"):
            try:
                tamanos_encabezado.append(int(nodo.get(f"{{{W}}}val")))
            except (TypeError, ValueError):
                pass
        dibujos_encabezado = sum(
            1 for _ in encabezado.iter(f"{{{W}}}drawing"))
        tablas_encabezado = sum(1 for _ in encabezado.iter(f"{{{W}}}tbl"))
        grid = encabezado.find(f".//{{{W}}}tblGrid")
        if grid is not None:
            ancho_encabezado = sum(
                int(gc.get(f"{{{W}}}w"))
                for gc in grid.findall(f"{{{W}}}gridCol")
                if gc.get(f"{{{W}}}w"))
        trHeight = encabezado.find(f".//{{{W}}}trHeight")
        if trHeight is not None:
            alto_fila_encabezado = {
                "val": int(trHeight.get(f"{{{W}}}val")),
                "hRule": trHeight.get(f"{{{W}}}hRule"),
            }
        for extent in encabezado.iter(f"{{{WP}}}extent"):
            cy = extent.get("cy")
            if cy:
                alturas_logo_cm.append(round(int(cy) / 360000, 2))

    codigos = {codigo: texto_total.count(codigo)
               for codigo in _CODIGOS_PROHIBIDOS}
    return {
        "docx": str(ruta),
        "sha256": sha256(ruta),
        "bytes": ruta.stat().st_size,
        "fuente_minima_global_pt": min(tamanos) / 2 if tamanos else None,
        "fuente_minima_tablas_pt": (min(tamanos_tabla) / 2
                                    if tamanos_tabla else None),
        "fuente_minima_encabezado_pt": (min(tamanos_encabezado) / 2
                                        if tamanos_encabezado else None),
        "tablas": len(anchos),
        "ancho_maximo_tabla_dxa": max(anchos) if anchos else None,
        "tablas_flotantes": flotantes,
        "omml": omml,
        "omml_en_celdas": omml_celdas,
        "codigos_internos": codigos,
        "codigos_internos_total": sum(codigos.values()),
        "partes_encabezado": partes_encabezado,
        "header1_xml": "word/header1.xml" in nombres,
        "referencias_encabezado": referencias_encabezado,
        "referencias_pie": referencias_pie,
        "dibujos_cuerpo": dibujos_cuerpo,
        "dibujos_encabezado": dibujos_encabezado,
        "tablas_encabezado": tablas_encabezado,
        "ancho_encabezado_dxa": ancho_encabezado,
        "alto_fila_encabezado": alto_fila_encabezado,
        "alturas_logo_cm": alturas_logo_cm,
        "pg_mar_top_dxa": (int(pgMar.get(f"{{{W}}}top"))
                           if pgMar is not None else None),
        "pg_mar_header_dxa": (int(pgMar.get(f"{{{W}}}header"))
                              if pgMar is not None else None),
    }


def exportar(ruta_docx: Path) -> Dict[str, Any]:
    ruta_pdf = ruta_docx.with_suffix(".pdf")
    return dq.exportar_docx_a_pdf(ruta_docx, ruta_pdf, actualizar_campos=False)


def informacion_pdf(ruta_pdf: Path) -> Dict[str, Any]:
    import pymupdf

    doc = pymupdf.open(str(ruta_pdf))
    paginas = doc.page_count
    texto = "\n".join(p.get_text("text") for p in doc)
    fondos: list[float] = []
    holguras: list[float] = []
    for pagina in doc:
        limite = pagina.rect.height - 70.87       # margen inferior 2.5 cm
        visibles = [b[3] for b in pagina.get_text("blocks")
                    if b[4].strip() and b[1] < limite]
        # Los bordes de tablas y recuadros también cuentan como tinta: una
        # caja vacía al pie reduce la holgura real aunque no tenga texto.
        for dibujo in pagina.get_drawings():
            rect = dibujo.get("rect")
            if rect is not None and rect.y0 < limite:
                visibles.append(min(rect.y1, limite))
        fondo = max(visibles, default=0.0)
        fondos.append(round(fondo, 2))
        holguras.append(round((limite - fondo) / 28.3465, 2))
    ultima = doc[paginas - 1]
    alto = ultima.rect.height
    doc.close()
    codigos = {codigo: texto.count(codigo) for codigo in _CODIGOS_PROHIBIDOS}
    return {
        "paginas_pdf": paginas,
        "texto": texto,
        "fondo_ultima_pagina_pt": fondos[-1] if fondos else 0.0,
        "alto_pagina_pt": round(alto, 2),
        "holgura_inferior_cm": holguras[-1] if holguras else 0.0,
        "holgura_inferior_por_pagina_cm": holguras,
        "fondo_por_pagina_pt": fondos,
        "codigos_internos_pdf": codigos,
        "codigos_internos_pdf_total": sum(codigos.values()),
        "escala_totalmente_en_desacuerdo": texto.count("Totalmente en desacuerdo"),
    }


def renderizar(ruta_pdf: Path, paginas: int) -> list[str]:
    CONTROL.mkdir(parents=True, exist_ok=True)
    salida = dq.renderizar_paginas_pdf(
        ruta_pdf, list(range(1, paginas + 1)), dpi=150, salida_dir=CONTROL)
    return salida["renderizadas"]


def construir(nombre: str, funcion) -> Path:
    doc = nueva_plantilla()
    doc.core_properties.title = nombre
    doc.core_properties.subject = "Instrumentos definitivos SIVAC v05"
    doc.core_properties.author = "SIVAC"
    funcion(doc)
    ruta = BASE / f"{nombre}.docx"
    doc.save(str(ruta))
    return ruta


def _advertencia_maquetacion(nombre: str,
                             registro: Dict[str, Any]) -> Optional[str]:
    """Advertencias editoriales verificadas que acompañan al manifiesto."""
    if registro.get("paginas_pdf_medidas") != 2:
        return None
    holguras = registro.get("holgura_inferior_por_pagina_cm") or []
    p1 = holguras[0] if len(holguras) > 0 else 0.0
    p2 = holguras[1] if len(holguras) > 1 else 0.0
    if nombre.startswith("03"):
        return ("dos páginas. La página 1 cierra en "
                f"{p1:.2f} cm con la fila «¿Conforme?» y el conteo del "
                f"Bloque A; la página 2 inicia con el Bloque B (holgura "
                f"{p2:.2f} cm) y contiene IV. Observaciones (4.0 cm) y V. "
                "Responsable. La cabecera del Bloque B usa textDirection "
                "btLr nativo en 8 celdas, sin guiones blandos; se conservan "
                "10 columnas y 5 despachos. Para mantener el conteo del "
                "Bloque A en la página 1 se ajustó el ritmo: título 6 pt "
                "antes, ficha 4 pt antes, rótulos I-III 10 pt antes y "
                "conteo 2/11/4.")
    if nombre.startswith("05"):
        return ("la página 1 cierra en "
                f"{p1:.3f} cm (mínimo PMI-05 §9: 0.4 cm) tras el ítem 7; "
                "la página 2 repite la cabecera de la matriz y contiene el "
                "ítem 8, la Dimensión 3, los ítems 9 a 14, las notas, las "
                "observaciones y la firma. Se conservan los catorce ítems y "
                "las tres dimensiones.")
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solo",
                        help="Compila solo los prefijos indicados (coma)")
    parser.add_argument("--sin-pdf", action="store_true",
                        help="Construye solo los DOCX")
    parser.add_argument("--sin-render", action="store_true",
                        help="No renderiza PNG de control")
    args = parser.parse_args()

    BASE.mkdir(parents=True, exist_ok=True)
    for ruta in (LOGO_UNAJMA, LOGO_EPIS):
        if not ruta.exists():
            raise FileNotFoundError(f"Logotipo ausente: {ruta}")

    manifiesto: Dict[str, Any] = {
        "version": "v05",
        "estado_compilacion": "definitivo",
        "generado": datetime.now().isoformat(timespec="seconds"),
        "especificaciones": str(ESPEC),
        "geometria": {
            "pagina_dxa": [11906, 16838],
            "margenes_dxa": {"izquierdo": 1701, "superior": 1701,
                             "derecho": 1417, "inferior": 1417},
            "distancia_encabezado_dxa": 454,
            "ancho_util_dxa": ANCHO_DXA,
            "alto_util_cm": 24.2,
            "banda_ubicacion": "encabezado nativo word/header1.xml",
            "banda_cm": list(BANDA_ANCHOS_CM),
            "banda_alto_cm": BANDA_ALTO_CM,
            "logo_alto_cm": LOGO_ALTO_CM,
            "espaciado": {
                "rotulos_antes_pt": ESP_ANTES,
                "rotulos_despues_pt": ESP_DESPUES,
                "titulo_primer_elemento_pt": 6.0,
                "tabla_rotulo_pt": ESP_ANTES,
                "margen_celda_vertical_mm": 0.5,
            },
            "tipo_letra": "Times New Roman",
            "cuerpo_pt": 10.0,
            "tablas_pt": 9.5,
            "fuente_minima_admitida_pt": 9.5,
            "interlineado_exacto_pt": INTERLINEA,
        },
        "documentos": [],
        "advertencias": [],
    }

    prefijos = ([p.strip() for p in args.solo.split(",") if p.strip()]
                if args.solo else [])

    for nombre, funcion, clave in DOCUMENTOS:
        if prefijos and not any(nombre.startswith(p) for p in prefijos):
            continue
        print(f"[docx] {nombre}", flush=True)
        ruta = construir(nombre, funcion)
        registro = inspeccionar_docx(ruta)
        registro["nombre"] = nombre
        if not args.sin_pdf:
            print(f"[pdf ] {nombre}", flush=True)
            datos = exportar(ruta)
            ruta_pdf = ruta.with_suffix(".pdf")
            info = informacion_pdf(ruta_pdf)
            registro.update({
                "pdf": str(ruta_pdf),
                "sha256_pdf": sha256(ruta_pdf),
                "bytes_pdf": ruta_pdf.stat().st_size,
                "paginas_docx": datos.get("paginas"),
                "paginas_pdf_medidas": info["paginas_pdf"],
                "fondo_ultima_pagina_pt": info["fondo_ultima_pagina_pt"],
                "alto_pagina_pt": info["alto_pagina_pt"],
                "margen_inferior_pt": 70.87,
                "holgura_inferior_cm": info["holgura_inferior_cm"],
                "holgura_inferior_por_pagina_cm": info[
                    "holgura_inferior_por_pagina_cm"],
                "fondo_por_pagina_pt": info["fondo_por_pagina_pt"],
                "codigos_internos_pdf": info["codigos_internos_pdf"],
                "codigos_internos_pdf_total": info["codigos_internos_pdf_total"],
                "escala_totalmente_en_desacuerdo": info[
                    "escala_totalmente_en_desacuerdo"],
            })
            if info["paginas_pdf"] > 2:
                manifiesto["advertencias"].append(
                    f"{nombre}: {info['paginas_pdf']} páginas (máximo 2).")
            if not args.sin_render:
                registro["png"] = renderizar(ruta_pdf, info["paginas_pdf"])
        advertencia = _advertencia_maquetacion(nombre, registro)
        if advertencia:
            manifiesto["advertencias"].append(f"{nombre}: {advertencia}")
        manifiesto["documentos"].append(registro)

    ruta_manifiesto = BASE / "MANIFIESTO_v05.json"
    if args.solo and ruta_manifiesto.exists():
        # ``--solo`` recompila un documento: la entrada nueva sustituye solo
        # la suya y las otras cinco se conservan con sus huellas intactas.
        previo = json.loads(ruta_manifiesto.read_text(encoding="utf-8"))
        por_nombre = {d.get("nombre"): d
                      for d in previo.get("documentos", [])}
        recompilados = {registro["nombre"]
                        for registro in manifiesto["documentos"]}
        for registro in manifiesto["documentos"]:
            por_nombre[registro["nombre"]] = registro
        orden = [nombre for nombre, _, _ in DOCUMENTOS]
        manifiesto["documentos"] = [por_nombre[clave] for clave in orden
                                    if clave in por_nombre]
        ajenas = [a for a in previo.get("advertencias", [])
                  if not any(a.startswith(f"{n}:") for n in recompilados)]
        manifiesto["advertencias"] = ajenas + manifiesto["advertencias"]

    ruta_manifiesto.write_text(
        json.dumps(manifiesto, indent=2, ensure_ascii=False), encoding="utf-8")

    resumen = {
        d["nombre"]: {
            "paginas_pdf": d.get("paginas_pdf_medidas"),
            "min_global": d.get("fuente_minima_global_pt"),
            "min_tablas": d.get("fuente_minima_tablas_pt"),
            "tablas": d.get("tablas"),
            "ancho_max": d.get("ancho_maximo_tabla_dxa"),
            "omml": d.get("omml"),
            "omml_celdas": d.get("omml_en_celdas"),
            "codigos": d.get("codigos_internos_total"),
            "codigos_pdf": d.get("codigos_internos_pdf_total"),
            "holgura_cm": d.get("holgura_inferior_cm"),
            "holguras_cm": d.get("holgura_inferior_por_pagina_cm"),
            "header1": d.get("header1_xml"),
            "header_ref": d.get("referencias_encabezado"),
            "footer_ref": d.get("referencias_pie"),
            "drawings": d.get("dibujos_cuerpo"),
            "drawings_hdr": d.get("dibujos_encabezado"),
            "pg_top": d.get("pg_mar_top_dxa"),
            "pg_header": d.get("pg_mar_header_dxa"),
            "min_hdr": d.get("fuente_minima_encabezado_pt"),
            "logo_cm": d.get("alturas_logo_cm"),
            "fila_hdr": d.get("alto_fila_encabezado"),
        }
        for d in manifiesto["documentos"]
    }
    print(json.dumps(resumen, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
