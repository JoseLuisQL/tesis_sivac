# -*- coding: utf-8 -*-
"""
Constructor de los seis instrumentos simplificados SIVAC v04.

Compila las seis especificaciones Markdown cerradas de
``salidas/instrumentos/INSTRUMENTOS_SIVAC_SIMPLIFICADO_v04/_ESPECIFICACION``
a seis documentos DOCX de una sola página, sus PDF oficiales, un PNG de
control por página y el ``MANIFIESTO_v04.json``.

Geometría común
---------------
* A4 vertical 11906 x 16838 dxa. Márgenes: izquierdo 1701 dxa (3.0 cm);
  superior, derecho e inferior 1417 dxa (2.5 cm). Ancho útil 8788 dxa.
* Times New Roman. Cuerpo 10 pt; tablas 9.5 pt. Ninguna fuente menor a 9.5 pt.
* Interlineado exacto por nota de producción (11.5 pt en 00; 12 pt en 01,
  02, 03 y 04; 10.5 pt dentro de la tabla del certificado 05).
* Banda institucional común: una sola tabla sin bordes de una fila y tres
  celdas (2.4 cm + 10.7 cm + 2.4 cm = 15.5 cm), altura exacta 2.2 cm y
  logotipos de 1.9 cm alineados al centro vertical.
* Rejilla visible de 0.5 pt solo en las tablas de formulario. Cero sombreado.
* Cero OMML y cero fórmulas en celdas.

Las líneas de llenado se escriben como runs literales: el escritor no
interpreta secuencias de guiones bajos como cursiva ni las recorta.

Uso
---
    python scripts/compiladores/instrumentos_recoleccion_v04_builder.py
    python scripts/compiladores/instrumentos_recoleccion_v04_builder.py --solo 05
    python scripts/compiladores/instrumentos_recoleccion_v04_builder.py --sin-pdf
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Tuple

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Emu, Pt

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from scripts.utilidades import docx_quirurgico as dq  # noqa: E402

BASE = RAIZ / "salidas" / "instrumentos" / "INSTRUMENTOS_SIVAC_SIMPLIFICADO_v04"
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
NO_PUNTO = 2              # 1.0 pt

MARGEN_LR = 57            # 1 mm lateral
MARGEN_TB = 28            # 0.5 mm vertical
MARGEN_LR_CAB = 28        # 0.5 mm lateral en rótulos de columna
MARGEN_TB_05 = 0          # sin relleno vertical: el certificado agota la página

# Interlineado exacto por nota de producción (pt).
INTERLINEA = {
    "00": 11.5, "01": 12.0, "02": 12.0, "03": 12.0, "04": 12.0, "05": 12.0,
}
INTERLINEA_TABLA = 12.0
INTERLINEA_TABLA_05 = 10.5

ALINEACION = {
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
    "center": WD_ALIGN_PARAGRAPH.CENTER,
    "both": WD_ALIGN_PARAGRAPH.JUSTIFY,
}

_ESTADO: Dict[str, Any] = {"hdr": []}

_TOKEN = re.compile(r"(\*\*.+?\*\*)")


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
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), font)


def add_runs(parrafo, texto: str, size: int = SP, bold: bool = False,
             italic: bool = False) -> None:
    """Escribe texto con marcas ``**negrita**``.

    Las secuencias de guiones bajos son líneas de relleno: no se interpretan
    como énfasis y se conservan íntegras.
    """
    if texto is None:
        return
    for parte in _TOKEN.split(texto):
        if not parte:
            continue
        b = bold
        t = parte
        if parte.startswith("**") and parte.endswith("**") and len(parte) > 4:
            t, b = parte[2:-2], True
        # Caja de marcado: se compone con una fuente que sí tenga el glifo.
        for trozo in re.split(r"(☐)", t):
            if not trozo:
                continue
            run = parrafo.add_run(trozo)
            if trozo == "☐":
                _set_run(run, size, bold=b, italic=italic,
                         font="Segoe UI Symbol")
            else:
                _set_run(run, size, bold=b, italic=italic)


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


def titulo(doc, texto: str, size: int = 24, before: float = 0,
           after: float = 1, line: float = 13.5):
    return par(doc, texto, size=size, bold=True, before=before, after=after,
               line=line, keep=True, keep_lines=True)


def subtitulo(doc, texto: str, before: float = 0, after: float = 2,
              line: float = 12.0):
    return par(doc, texto, size=SP, bold=True, before=before, after=after,
               line=line, keep=True, keep_lines=True)


def h2(doc, texto: str, before: float = 3.0, after: float = 0.5,
       line: float = 12.0):
    return par(doc, texto, size=SP, bold=True, before=before, after=after,
               line=line, keep=True, keep_lines=True)


# ---------------------------------------------------------------------------
# Geometría de tablas
# ---------------------------------------------------------------------------

def _dxa(anchos_cm: Sequence[float], flexible: Optional[int] = None) -> list[int]:
    """Convierte cm a dxa y absorbe el redondeo en la columna flexible.

    No se recorta la última columna a ciegas: en las tablas con columnas
    repetidas (casillas de 0.65 cm) todas conservan el mismo ancho y el ajuste
    cae sobre la columna de texto.
    """
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
    tbl = tabla._tbl
    tblPr = tbl.tblPr
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


def _escribir_celda(celda, spec, size: int, bold_defecto: bool,
                    align_defecto: str, linea: float,
                    margen_lr: Optional[int] = None,
                    margen_tb: Optional[int] = None) -> None:
    texto = "" if spec is None else str(spec)
    p = _reiniciar_celda(celda)
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(linea)
    pf.left_indent = Cm(0)
    pf.first_line_indent = Cm(0)
    pf.alignment = ALINEACION[align_defecto]
    if texto:
        add_runs(p, texto, size=size, bold=bold_defecto)
    celda.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    if margen_lr is not None or margen_tb is not None:
        _fijar_margen_celda(celda,
                            MARGEN_LR if margen_lr is None else margen_lr,
                            MARGEN_TB if margen_tb is None else margen_tb)


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


def tabla(doc, filas: Sequence[Sequence[Any]], anchos_cm: Sequence[float],
          header_rows: int = 1, apa: bool = False, size: int = SP_TABLA,
          merges: Sequence[Tuple[int, int, int, int]] = (),
          align_defecto: str = "left", header_align: str = "center",
          margen_lr: int = MARGEN_LR, margen_tb: int = MARGEN_TB,
          margen_lr_cabecera: Optional[int] = None,
          alto_filas_cm: Optional[float] = None,
          flex_col: Optional[int] = None, linea: float = INTERLINEA_TABLA,
          negritas: Sequence[Tuple[int, int]] = (),
          sin_bordes: bool = False):
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
            _escribir_celda(
                t.cell(r, c), spec, size, bold,
                header_align if cabecera else align_defecto, linea,
            )
            if cabecera and margen_lr_cabecera is not None:
                _fijar_margen_celda(t.cell(r, c), margen_lr_cabecera, margen_tb)

    for i, fila in enumerate(t.rows):
        dq._preparar_tr(fila._tr, cant_split=True,
                        tbl_header=(i < header_rows))
        if alto_filas_cm is not None and i >= header_rows:
            fila.height = Cm(alto_filas_cm)
            fila.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST

    _geometria(t, anchos_dxa)
    dq.eliminar_flotacion_tabla(t)
    if sin_bordes:
        _sin_bordes(t)
    elif apa:
        dq.aplicar_bordes_apa7_tabla(t)
    else:
        dq.aplicar_bordes_campo(t, exterior_sz=4, interior_sz=4)
    return t


# ---------------------------------------------------------------------------
# Plantilla y encabezado común
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
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), "Times New Roman")
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
            for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
                fuentes.set(qn(attr), "Times New Roman")
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
    for lado, valor in (("top", "1417"), ("right", "1417"),
                        ("bottom", "1417"), ("left", "1701"),
                        ("header", "0"), ("footer", "0"), ("gutter", "0")):
        pgMar.set(qn(f"w:{lado}"), valor)
    for nodo in sectPr.findall(qn("w:docGrid")):
        sectPr.remove(nodo)
    configurar_estilos(doc)
    # El documento nace sin párrafos: la primera línea es el encabezado.
    for p in list(doc.paragraphs):
        p._element.getparent().remove(p._element)
    doc.core_properties.language = "es-PE"
    doc.core_properties.author = "SIVAC"
    _ESTADO["hdr"] = []
    return doc


def encabezado(doc) -> None:
    """Banda institucional única de tres celdas sin bordes.

    Delega la geometría en el motor canónico (``dq.banda_institucional``):
    logotipos de 1.9 cm con centro vertical compartido y bloque de texto
    central de tres líneas a 9.5 pt. Los formularios son de una página y no
    llevan rótulo de página.
    """
    dq.banda_institucional(doc, LOGO_UNAJMA, LOGO_EPIS)
    _ESTADO["hdr"].extend([SP_TABLA, SP_TABLA, SP_TABLA])


# ---------------------------------------------------------------------------
# Documentos
# ---------------------------------------------------------------------------

def doc_00(doc) -> None:
    li = INTERLINEA["00"]
    encabezado(doc)
    titulo(doc, "Guía de aplicación de los instrumentos", before=2, after=1,
           line=13.0)
    subtitulo(doc, "Gestión de movimientos mensuales de vacunas", after=2,
              line=li)
    par(doc, "Esta guía explica cómo se aplican los tres instrumentos. Las dos "
             "fichas las llena el investigador mediante observación directa. El "
             "cuestionario lo llena el trabajador sin escribir su nombre.",
        align="both", line=li)

    h2(doc, "1. Qué mide cada instrumento", line=li)
    par(doc, "La ficha de tiempos mide cuánto demora el trabajador en registrar "
             "un movimiento de vacunas y en emitir el comprobante de salida o "
             "vale. Se cronometran tres registros y tres vales por trabajador en "
             "cada momento.", align="both", line=li)
    par(doc, "La ficha documental mide cuántos documentos de movimiento están "
             "sin discrepancias y cuántos despachos coinciden con la cantidad "
             "programada. Se revisan los documentos y los despachos del periodo "
             "consignado en la ficha.", align="both", line=li)
    par(doc, "El cuestionario mide la opinión del trabajador sobre el proceso y "
             "sobre su utilidad. Tiene ocho preguntas con respuesta de 1 a 5 y "
             "no lleva nombre.", align="both", line=li)

    h2(doc, "2. Cuándo se aplica", line=li)
    tabla(doc, [
        ("Momento", "Qué se hace", "Quién lo llena"),
        ("Antes de SIVAC (pretest)",
         "Se aplican las dos fichas y el cuestionario sobre el proceso que el "
         "trabajador usa sin SIVAC.", "Investigador y trabajador"),
        ("Con SIVAC (postest)",
         "Se aplican los mismos tres instrumentos sobre el proceso con SIVAC, "
         "después del periodo de uso.", "Investigador y trabajador"),
        ("Cierre de cada momento",
         "Se cuentan documentos y despachos, y se calculan promedios y "
         "porcentajes.", "Investigador"),
    ], (3.0, 9.5, 3.0), apa=True, flex_col=1, linea=li,
        margen_lr_cabecera=MARGEN_LR_CAB, negritas=((1, 0), (2, 0), (3, 0)))
    par(doc, "La revisión documental abarca treinta días calendario en cada "
             "momento. El cuestionario se aplica al final de cada momento, una "
             "vez concluidas las mediciones.", align="both",
        line=li, before=2)

    h2(doc, "3. Cómo se mide el tiempo", line=li)
    par(doc, "Se usa un cronómetro. En el registro se mide desde que el "
             "trabajador recibe la orden o el lote y abre el registro hasta que "
             "cierra y firma el asiento. En el vale se mide desde que recibe la "
             "solicitud de despacho hasta que genera y confirma el vale.",
        align="both", line=li)
    par(doc, "Las horas se anotan en hh:mm:ss. La conversión a minutos es: horas "
             "por 60, más los minutos, más los segundos divididos entre 60. El "
             "resultado se anota con dos decimales. Se hacen tres mediciones por "
             "operación y se promedian. Un tiempo igual o menor que cero anula la "
             "medición y obliga a repetirla.", align="both", line=li)

    h2(doc, "4. Qué se cuenta como documento conforme", line=li)
    par(doc, "Un documento es conforme solo si cumple los ocho criterios: "
             "biológico, lote, vencimiento, cantidad, centro, responsable y "
             "firmas, saldo y correlatividad. Un solo criterio incumplido hace "
             "no conforme el documento.", align="both", line=li)

    h2(doc, "5. Qué se cuenta como despacho conforme", line=li)
    par(doc, "Un despacho es conforme solo si la cantidad entregada es igual a "
             "la programada y existe el documento que lo autoriza. Cualquier "
             "diferencia, por exceso o por defecto, lo hace no conforme.",
        align="both", line=li)

    h2(doc, "6. Cómo se calculan los dos porcentajes", line=li)
    par(doc, "El porcentaje de documentos sin discrepancias se calcula dividiendo "
             "el número de documentos conformes entre el número de documentos "
             "revisados y multiplicando el cociente por cien.", align="both",
        line=li)
    par(doc, "El porcentaje de despachos conformes se calcula dividiendo el "
             "número de despachos conformes entre el número de despachos "
             "revisados y multiplicando el cociente por cien.", align="both",
        line=li)
    par(doc, "Los documentos no se compensan entre sí ni los despachos se suman "
             "en dosis.", align="both", line=li)

    h2(doc, "7. Cómo se asigna el número de trabajador", line=li)
    par(doc, "Se numera a los trabajadores del 1 al 14 siguiendo el orden de la "
             "lista del personal de inmunizaciones. El mismo número se usa en el "
             "pretest y en el postest. En los formularios se escribe solo el "
             "número. La lista que vincula números y nombres se conserva separada "
             "de los formularios y se destruye al concluir el informe.",
        align="both", line=li)


def doc_01(doc) -> None:
    li = INTERLINEA["01"]
    encabezado(doc)
    titulo(doc, "Cuestionario de satisfacción del usuario", before=2, after=1,
           line=13.0)
    subtitulo(doc, "Gestión de movimientos mensuales de vacunas", after=3,
              line=li)

    tabla(doc, [
        ("Trabajador N.°", "____________________"),
        ("Momento", "☐ Antes de SIVAC        ☐ Con SIVAC"),
        ("Fecha", "____ / ____ / ________"),
    ], (3.5, 12.0), header_rows=0, flex_col=1, linea=li,
        margen_lr_cabecera=MARGEN_LR_CAB, negritas=((0, 0), (1, 0), (2, 0)))

    par(doc, "Marque con una X el número que mejor represente su opinión. No "
             "escriba su nombre.", align="both", line=li, before=4, after=2,
        keep=True)

    filas = [
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
    tabla(doc, filas, (0.8, 11.45, 0.65, 0.65, 0.65, 0.65, 0.65),
          header_rows=1, size=SP_TABLA, flex_col=1, linea=li,
          margen_lr_cabecera=MARGEN_LR_CAB,
          negritas=((r, 0) for r in range(1, 9)))

    par(doc, "**Escala:** 1 = Totalmente en desacuerdo; 2 = En desacuerdo; "
             "3 = Ni de acuerdo ni en desacuerdo; 4 = De acuerdo; 5 = Totalmente "
             "de acuerdo.", align="both", line=li, before=4, after=0)
    par(doc, "Sus respuestas son confidenciales y se usarán únicamente para esta "
             "investigación.", align="both", line=li, before=3)


def doc_02(doc) -> None:
    li = INTERLINEA["02"]
    encabezado(doc)
    titulo(doc, "Ficha de tiempos", before=2, after=1, line=13.0)
    subtitulo(doc, "Registro del movimiento y emisión del comprobante de salida "
                   "o vale", after=3, line=li)

    tabla(doc, [
        ("Trabajador N.°", "____________________"),
        ("Centro", "____________________"),
        ("Fecha", "____ / ____ / ________"),
        ("Momento", "☐ Antes de SIVAC        ☐ Con SIVAC"),
        ("Observador", "____________________"),
    ], (3.5, 12.0), header_rows=0, flex_col=1, linea=li,
        margen_lr_cabecera=MARGEN_LR_CAB,
        negritas=((r, 0) for r in range(5)))

    par(doc, "Use un cronómetro. Anote las horas en hh:mm:ss. Convierta a minutos "
             "así: horas por 60, más los minutos, más los segundos divididos "
             "entre 60; anote dos decimales. Si el tiempo resulta cero o "
             "negativo, la medición se anula y se repite. Si ocurre una "
             "interrupción externa, anótela en Observación y repita la medición. "
             "Mantenga operaciones de similar magnitud entre trabajadores.",
        align="both", line=li, before=4, after=1)

    for bloque, titulo_bloque, texto in (
        ("A", "Bloque A. Tiempo de registro del movimiento de vacunas (T_reg)",
         "Se mide desde que el trabajador recibe la orden o el lote y abre el "
         "registro hasta que cierra y firma el asiento o confirma el guardado. "
         "Registre tres operaciones distintas: un ingreso, una salida y una "
         "transferencia. Si el trabajador no realiza alguno de esos tipos "
         "durante la jornada, registre otra operación del mismo bloque y "
         "anótelo en Observación."),
        ("B", "Bloque B. Tiempo de emisión del comprobante de salida o vale "
              "(T_vale)",
         "Se mide desde que el trabajador recibe la solicitud de despacho hasta "
         "que genera y confirma el vale impreso o digital. Registre tres vales "
         "distintos: salida regular, reposición urgente y transferencia. Si el "
         "trabajador no realiza alguno de esos tipos durante la jornada, "
         "registre otra operación del mismo bloque y anótelo en Observación."),
    ):
        h2(doc, titulo_bloque, before=5, after=1, line=li)
        par(doc, texto, align="both", line=li, after=2, keep=True)
        tabla(doc, [
            ("N.°", "Registro observado", "Hora de inicio", "Hora de fin",
             "Tiempo (min)", "Observación"),
            ("1", "", "", "", "", ""),
            ("2", "", "", "", "", ""),
            ("3", "", "", "", "", ""),
        ], (0.8, 5.0, 2.4, 2.4, 2.4, 2.5), header_rows=1, flex_col=1,
            linea=li, margen_lr_cabecera=MARGEN_LR_CAB,
            alto_filas_cm=0.8, negritas=((1, 0), (2, 0), (3, 0)))

    par(doc, "**T_reg promedio = ________ min**", line=li, before=6)
    par(doc, "**T_vale promedio = ________ min**", line=li, before=4)


def doc_03(doc) -> None:
    li = INTERLINEA["03"]
    encabezado(doc)
    titulo(doc, "Ficha documental", before=1, after=1, line=12.5)
    subtitulo(doc, "Documentos sin discrepancias y despachos conformes",
              after=2, line=li)

    tabla(doc, [
        ("Trabajador N.°", "____________________"),
        ("Centro", "____________________"),
        ("Fecha", "____ / ____ / ________"),
        ("Momento", "☐ Antes de SIVAC        ☐ Con SIVAC"),
        ("Observador", "____________________"),
        ("Periodo revisado", "del ____ / ____ / ________ al ____ / ____ / "
                             "________"),
    ], (3.5, 12.0), header_rows=0, flex_col=1, linea=li,
        margen_lr_cabecera=MARGEN_LR_CAB,
        negritas=((r, 0) for r in range(6)))

    h2(doc, "Bloque A. Documentos sin discrepancias (RSD)", before=4, after=1,
       line=li)
    par(doc, "Biológico: nombre y presentación. Lote: número rotulado. "
             "Vencimiento: mes y año. Cantidad: dosis o frascos. Centro: código "
             "y nombre coinciden con el documento que autoriza. Responsable y "
             "firmas: de quien entrega y de quien recibe. Saldo: inicial más "
             "ingresos menos salidas. Correlatividad: fecha y hora.",
        align="both", line=li, after=1)
    par(doc, "Escriba Sí o No en cada casilla. Un solo No hace no conforme el "
             "documento.", align="both", line=li, after=0, keep=True)
    par(doc, "Revise los cinco primeros documentos del periodo, en orden de "
             "fecha; si hay menos de cinco, revise todos.", align="both",
        line=li, after=2, keep=True)

    filas_a = [("Criterio", "Doc. 1", "Doc. 2", "Doc. 3",
                "Doc. 4", "Doc. 5")]
    for criterio in ("Biológico", "Lote", "Vencimiento", "Cantidad", "Centro",
                     "Responsable y firmas", "Saldo", "Correlatividad",
                     "¿Conforme?"):
        filas_a.append((criterio, "", "", "", "", ""))
    tabla(doc, filas_a, (5.5, 2.0, 2.0, 2.0, 2.0, 2.0), header_rows=1,
          flex_col=0, linea=li, margen_lr_cabecera=MARGEN_LR_CAB,
          alto_filas_cm=0.52, negritas=((9, 0),))

    h2(doc, "Bloque B. Despachos: cantidad programada frente a entregada (CPE)",
       before=4, after=1, line=li)
    par(doc, "Diferencia = entregado − programado. Conforme solo si la "
             "diferencia es cero y existe el documento que autoriza.",
        align="both", line=li, after=2, keep=True)

    filas_b = [("N.°", "Fecha", "Establecimiento destino", "Programado",
                "Entregado", "Diferencia", "Documento que autoriza",
                "¿Conforme?")]
    for i in range(1, 11):
        filas_b.append((str(i), "", "", "", "", "", "", ""))
    tabla(doc, filas_b, (0.8, 1.7, 2.4, 1.9, 1.9, 2.1, 2.3, 2.4),
          header_rows=1, flex_col=6, linea=li,
          margen_lr_cabecera=8, alto_filas_cm=0.46,
          negritas=((r, 0) for r in range(1, 11)))

    par(doc, "**Documentos conformes ______ / Documentos revisados ______**",
        line=li, before=4)
    par(doc, "**Despachos conformes ______ / Despachos revisados ______**",
        line=li, before=3)


def doc_04(doc) -> None:
    li = INTERLINEA["04"]
    encabezado(doc)
    titulo(doc, "Consentimiento informado para participar en la investigación",
           size=SP, before=2, after=2, line=li)

    tabla(doc, [
        ("Título de la investigación",
         "Aplicación del sistema SIVAC para mejorar la gestión de movimientos "
         "mensuales de vacunas en el personal de inmunizaciones de la Dirección "
         "de Salud Apurímac II"),
        ("Escuela profesional",
         "Ingeniería de Sistemas, Universidad Nacional José María Arguedas"),
        ("Naturaleza del estudio",
         "Tesis para optar el título profesional de Ingeniero de Sistemas"),
        ("Investigador responsable", "______________________________"),
        ("Asesora", "______________________________"),
    ], (4.5, 11.0), header_rows=0, flex_col=1, linea=li,
        margen_lr_cabecera=MARGEN_LR_CAB, negritas=((r, 0) for r in range(5)))

    par(doc, "Estimado(a) participante:", before=4, after=1, line=li)

    bloques = (
        ("1. Propósito.", "Esta investigación evalúa si el sistema SIVAC mejora "
         "la gestión de los movimientos mensuales de vacunas en el personal de "
         "inmunizaciones de la Dirección de Salud Apurímac II."),
        ("2. Procedimiento.", "Se observará y cronometrará cómo registra un "
         "movimiento de vacunas y cómo emite el comprobante de salida o vale. Se "
         "revisarán los documentos de movimiento de un periodo de treinta días y "
         "se le aplicará un cuestionario de ocho preguntas. La actividad se "
         "realiza en dos momentos, antes y con SIVAC, y demanda entre treinta y "
         "cuarenta minutos por momento."),
        ("3. Riesgos.", "No implica riesgos distintos de sus actividades "
         "habituales. No se tomarán muestras biológicas ni datos clínicos."),
        ("4. Beneficios.", "Contribuirá a mejorar el registro y el control de "
         "vacunas. No hay pago ni compensación económica."),
        ("5. Confidencialidad.", "Los formularios se identifican solo con un "
         "número de trabajador, sin nombres. La lista que vincula números y "
         "nombres queda en poder del investigador, separada de los formularios, "
         "y se destruye al concluir el informe. Los datos se usan solo para esta "
         "tesis."),
        ("6. Voluntariedad.", "La participación es libre. Puede retirarse en "
         "cualquier momento, sin perjuicio."),
        ("7. Contacto.", "Para consultas, comuníquese con el investigador."),
    )
    for rotulo, cuerpo in bloques:
        par(doc, f"**{rotulo}** {cuerpo}", align="both", line=li, after=0)

    par(doc, "Correo electrónico: ______________________________   "
             "Teléfono: ______________________", line=li, before=2,
        after=1)

    par(doc, "**8. Declaración de consentimiento.** He leído y comprendido la "
             "información. Mis preguntas fueron respondidas. Acepto participar "
             "voluntariamente.", align="both", line=li, after=3, keep=True)

    tabla(doc, [
        ("Participante", "Investigador"),
        ("Nombre: ______________________________",
         "Nombre: ______________________________"),
        ("Firma: ______________________________",
         "Firma: ______________________________"),
        ("Fecha: ____ / ____ / ________", "Fecha: ____ / ____ / ________"),
    ], (7.75, 7.75), header_rows=1, flex_col=0, linea=li,
        alto_filas_cm=0.62)

    par(doc, "Este documento se emite por duplicado: una copia para el "
             "participante y otra para el investigador.", align="both", line=li,
        before=3)


CERT_ITEMS = (
    (1, "El tiempo que demora el trabajador en registrar un movimiento de "
        "vacunas, en minutos, permite valorar la oportunidad de procesamiento."),
    (2, "El tiempo que demora el trabajador en emitir el comprobante o vale, en "
        "minutos, permite valorar la oportunidad de procesamiento."),
    (3, "La reducción del tiempo de registro entre pretest y postest mejora la "
        "oportunidad de procesamiento."),
    (4, "La reducción del tiempo del vale entre pretest y postest mejora la "
        "oportunidad de procesamiento."),
    (5, "El porcentaje de documentos sin discrepancias permite valorar la "
        "consistencia documental."),
    (6, "El porcentaje de despachos conformes permite valorar la consistencia "
        "documental."),
    (7, "El aumento de documentos sin discrepancias entre pretest y postest "
        "mejora la consistencia documental."),
    (8, "El aumento de despachos conformes entre pretest y postest mejora la "
        "consistencia documental."),
    (9, "El procedimiento actual para asentar los movimientos diarios y cierres "
        "de mes es ágil y no demanda un esfuerzo mental o físico excesivo."),
    (10, "El flujo de trabajo requerido para emitir comprobantes de salida y "
         "vales de entrega es fluido y está libre de demoras o trabas "
         "burocráticas."),
    (11, "El método empleado me permite conciliar los saldos de inventario con "
         "las microredes generando tranquilidad y reduciendo el estrés laboral."),
    (12, "El tiempo que dedico al registro administrativo de vacunas es "
         "equilibrado y me deja disponibilidad para mis labores sanitarias y "
         "asistenciales."),
    (13, "El mecanismo de registro utilizado me permite disponer de información "
         "fidedigna y en tiempo real del stock de vacunas y jeringas."),
    (14, "El control de números de lote y fechas de vencimiento que brinda el "
         "proceso previene oportunamente mermas o pérdidas de biológicos."),
    (15, "La metodología de gestión facilita la detección inmediata y "
         "rectificación de cualquier descuadre de inventario físico versus "
         "registrado."),
    (16, "En general, considero que el procedimiento empleado es una herramienta "
         "altamente eficaz para garantizar el abastecimiento oportuno de "
         "vacunas."),
)


def doc_05(doc) -> None:
    encabezado(doc)
    titulo(doc, "Certificado de validación de contenido de la variable "
                "dependiente", before=0, after=0, line=12.5)
    par(doc, "Variable dependiente: Gestión de movimientos mensuales de "
             "vacunas.", before=0, after=0, line=12.0)
    par(doc, "Marque Sí o No en cada criterio. Puede añadir sugerencias en la "
             "última columna.", before=0, after=1, line=12.0, keep=True)

    filas: list[tuple] = [
        ("N.°", "DIMENSIONES / Ítems", "Pert.¹", "", "Relev.²", "", "Clar.³",
         "", "Sugerencias"),
        ("", "", "Sí", "No", "Sí", "No", "Sí", "No", ""),
        ("", "**Dimensión 1. Oportunidad de procesamiento (ítems 1 a 4)**",
         "**Sí**", "**No**", "**Sí**", "**No**", "**Sí**", "**No**", ""),
    ]
    dims = {1: "**Dimensión 1. Oportunidad de procesamiento (ítems 1 a 4)**",
            5: "**Dimensión 2. Consistencia documental (ítems 5 a 8)**",
            9: "**Dimensión 3. Satisfacción del usuario (ítems 9 a 16)**"}
    for numero, texto in CERT_ITEMS:
        if numero in dims and numero != 1:
            filas.append(("", dims[numero], "**Sí**", "**No**", "**Sí**",
                          "**No**", "**Sí**", "**No**", ""))
        filas.append((str(numero), texto, "", "", "", "", "", "", ""))

    tabla(doc, filas, (0.7, 8.9, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 2.0),
          header_rows=2, flex_col=1, size=SP_TABLA, linea=INTERLINEA_TABLA_05,
          merges=((0, 0, 1, 0), (0, 1, 1, 1), (0, 2, 0, 3), (0, 4, 0, 5),
                  (0, 6, 0, 7), (0, 8, 1, 8)),
          margen_lr=57, margen_tb=MARGEN_TB_05,
          margen_lr_cabecera=MARGEN_LR_CAB,
          negritas=((r, 0) for r in range(2, len(filas))
                    if filas[r][1].startswith("**")))

    par(doc, "**Observaciones (precisar si hay suficiencia):** "
             "______________________________________________", line=12.0,
        before=0)
    par(doc, "**Opinión de aplicabilidad:** ☐ Aplicable        ☐ Aplicable "
             "después de corregir        ☐ No aplicable", line=12.0, before=0)
    par(doc, "**Apellidos y nombres:** ______________________________        "
             "**DNI:** ____________________        **Especialidad:** "
             "______________________________", line=12.0, before=0)
    par(doc, "**Fecha:** ____ de ____________________ del 2026.        "
             "**Firma:** ______________________________", line=12.0, before=0)

    par(doc, "**Notas al pie**", before=0, after=0, line=9.5)
    par(doc, "1. **Pertinencia:** el ítem corresponde al concepto teórico "
             "formulado.", size=SP_TABLA, line=9.5, after=0)
    par(doc, "2. **Relevancia:** el ítem es apropiado para representar al "
             "componente o dimensión específica del constructo.",
        size=SP_TABLA, line=9.5, after=0)
    par(doc, "3. **Claridad:** el enunciado del ítem se entiende sin dificultad "
             "alguna; es conciso, exacto y directo.", size=SP_TABLA,
        line=9.5, after=0)


DOCUMENTOS = (
    ("00_GUIA_DE_APLICACION_v04", doc_00, "00"),
    ("01_CUESTIONARIO_SATISFACCION_v04", doc_01, "01"),
    ("02_FICHA_TIEMPOS_v04", doc_02, "02"),
    ("03_FICHA_DOCUMENTAL_v04", doc_03, "03"),
    ("04_CONSENTIMIENTO_INFORMADO_v04", doc_04, "04"),
    ("05_CERTIFICADO_VALIDACION_v04", doc_05, "05"),
)

ROTULOS_ABREVIADOS = {
    "03_FICHA_DOCUMENTAL_v04": {
        "Documento 1-5": "Doc. 1-5",
    },
    "05_CERTIFICADO_VALIDACION_v04": {
        "Pertinencia": "Pert.", "Relevancia": "Relev.", "Claridad": "Clar.",
    },
}


# ---------------------------------------------------------------------------
# Inspección, exportación y manifiesto
# ---------------------------------------------------------------------------

def sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as fh:
        for bloque in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def inspeccionar_docx(ruta: Path) -> Dict[str, Any]:
    import xml.etree.ElementTree as ET

    W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
    with zipfile.ZipFile(ruta) as zf:
        raiz = ET.fromstring(zf.read("word/document.xml"))

    tamanos = []
    for sz in raiz.iter(f"{{{W}}}sz"):
        try:
            tamanos.append(int(sz.get(f"{{{W}}}val")))
        except (TypeError, ValueError):
            continue
    omml = sum(1 for _ in raiz.iter(f"{{{M}}}oMath"))
    flotantes = sum(1 for _ in raiz.iter(f"{{{W}}}tblpPr"))
    cant_split = sum(1 for _ in raiz.iter(f"{{{W}}}cantSplit"))
    filas = sum(1 for _ in raiz.iter(f"{{{W}}}tr"))
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

    # Líneas de llenado: secuencias de cuatro o más guiones bajos.
    textos = []
    for t in raiz.iter(f"{{{W}}}t"):
        if t.text:
            textos.append(t.text)
    texto_total = "".join(textos)
    rellenos = re.findall(r"_{4,}", texto_total)

    return {
        "docx": str(ruta),
        "sha256": sha256(ruta),
        "bytes": ruta.stat().st_size,
        "fuente_minima_cuerpo_pt": min(tamanos) / 2 if tamanos else None,
        "fuente_minima_encabezado_pt": (min(_ESTADO["hdr"]) / 2
                                        if _ESTADO["hdr"] else None),
        "tamanos_pt": sorted({t / 2 for t in tamanos}),
        "omml": omml,
        "tablas_flotantes": flotantes,
        "tablas": len(anchos),
        "filas": filas,
        "filas_cant_split": cant_split,
        "ancho_maximo_tabla_dxa": max(anchos) if anchos else None,
        "anchos_tabla_dxa": anchos,
        "tablas_exceden_ancho_util": [a for a in anchos if a > ANCHO_DXA],
        "lineas_relleno_docx": len(rellenos),
        "guiones_bajos_docx": texto_total.count("_"),
    }


def _texto_pdf(ruta_pdf: Path) -> Tuple[str, int, float, float]:
    import pymupdf

    doc = pymupdf.open(str(ruta_pdf))
    partes = []
    for pagina in doc:
        partes.append(pagina.get_text("text"))
    total = doc.page_count
    ultima = doc[total - 1]
    bloques = [b for b in ultima.get_text("blocks")
               if b[4].strip() and b[1] < ultima.rect.height - 70.87]
    fondo = max((b[3] for b in bloques), default=0.0)
    alto = ultima.rect.height
    doc.close()
    return "\n".join(partes), total, fondo, alto


def _verificar_rotulos(texto_pdf: str) -> Dict[str, Any]:
    fragmentos = ("Duraci ón", "Paus a", "¿Vál ida?", "Programa do",
                  "Entreg ado", "Diferenc ia", "Pertinen cia", "Relevanc ia",
                  "Clarida d", "Observaci ón", "Document o")
    hallados = [f for f in fragmentos if f in texto_pdf]
    return {"fragmentos_rotulo_partido": hallados}


def exportar(ruta_docx: Path) -> Dict[str, Any]:
    ruta_pdf = ruta_docx.with_suffix(".pdf")
    return dq.exportar_docx_a_pdf(ruta_docx, ruta_pdf, actualizar_campos=False)


def renderizar(ruta_pdf: Path, paginas: int) -> list[str]:
    CONTROL.mkdir(parents=True, exist_ok=True)
    salida = dq.renderizar_paginas_pdf(
        ruta_pdf, list(range(1, paginas + 1)), dpi=150, salida_dir=CONTROL)
    return salida["renderizadas"]


def construir(nombre: str, funcion, clave: str) -> Path:
    doc = nueva_plantilla()
    doc.core_properties.title = nombre
    doc.core_properties.subject = "Instrumentos simplificados SIVAC v04"
    doc.core_properties.author = "SIVAC"
    funcion(doc)
    ruta = BASE / f"{nombre}.docx"
    doc.save(str(ruta))
    return ruta


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solo", help="Compila únicamente el prefijo indicado")
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
        "version": "v04",
        "generado": datetime.now().isoformat(timespec="seconds"),
        "especificaciones": str(ESPEC),
        "geometria": {
            "pagina_dxa": [11906, 16838],
            "margenes_dxa": {"izquierdo": 1701, "superior": 1417,
                             "derecho": 1417, "inferior": 1417},
            "ancho_util_dxa": ANCHO_DXA,
            "tipo_letra": "Times New Roman",
            "cuerpo_pt": 10.0,
            "tablas_pt": 9.5,
            "fuente_minima_admitida_pt": 9.5,
            "interlineado_exacto_pt": INTERLINEA,
            "interlineado_tabla_05_pt": INTERLINEA_TABLA_05,
        },
        "documentos": [],
        "advertencias": [],
    }
    if (BASE / "MANIFIESTO_v04.json").exists():
        previo = json.loads((BASE / "MANIFIESTO_v04.json").read_text(
            encoding="utf-8"))
        manifiesto["documentos"] = previo.get("documentos", [])

    por_nombre = {d["nombre"]: d for d in manifiesto["documentos"]}
    for nombre, funcion, clave in DOCUMENTOS:
        if args.solo and not nombre.startswith(args.solo):
            continue
        print(f"[docx] {nombre}", flush=True)
        ruta = construir(nombre, funcion, clave)
        registro = inspeccionar_docx(ruta)
        registro["nombre"] = nombre
        registro["rotulos_abreviados"] = ROTULOS_ABREVIADOS.get(nombre, {})
        if not args.sin_pdf:
            print(f"[pdf ] {nombre}", flush=True)
            datos = exportar(ruta)
            ruta_pdf = ruta.with_suffix(".pdf")
            texto, paginas, fondo, alto = _texto_pdf(ruta_pdf)
            registro.update({
                "pdf": str(ruta_pdf),
                "sha256_pdf": sha256(ruta_pdf),
                "bytes_pdf": ruta_pdf.stat().st_size,
                "paginas_docx": datos.get("paginas"),
                "paginas_pdf_medidas": paginas,
                "fondo_ultima_pagina_pt": round(fondo, 2),
                "alto_pagina_pt": round(alto, 2),
                "margen_inferior_pt": 70.87,
                "holgura_inferior_cm": round((alto - 70.87 - fondo) / 28.3465, 2),
                "guiones_bajos_pdf": texto.count("_"),
                "lineas_relleno_completas": texto.count("_") >=
                registro["guiones_bajos_docx"],
                **_verificar_rotulos(texto),
            })
            if paginas != 1:
                manifiesto["advertencias"].append(
                    f"{nombre}: {paginas} páginas (se exige 1).")
            if not args.sin_render:
                registro["png"] = renderizar(ruta_pdf, min(paginas, 2))
        por_nombre[nombre] = registro
        manifiesto["documentos"] = list(por_nombre.values())

    (BASE / "MANIFIESTO_v04.json").write_text(
        json.dumps(manifiesto, indent=2, ensure_ascii=False), encoding="utf-8")

    resumen = {
        d["nombre"]: {
            "paginas_docx": d.get("paginas_docx"),
            "paginas_pdf": d.get("paginas_pdf_medidas"),
            "holgura_cm": d.get("holgura_inferior_cm"),
            "min_cuerpo": d.get("fuente_minima_cuerpo_pt"),
            "min_hdr": d.get("fuente_minima_encabezado_pt"),
            "tablas": d.get("tablas"),
            "ancho_max": d.get("ancho_maximo_tabla_dxa"),
            "omml": d.get("omml"),
            "relleno_ok": d.get("lineas_relleno_completas"),
            "rotulos_partidos": d.get("fragmentos_rotulo_partido"),
        }
        for d in manifiesto["documentos"]
    }
    print(json.dumps(resumen, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
