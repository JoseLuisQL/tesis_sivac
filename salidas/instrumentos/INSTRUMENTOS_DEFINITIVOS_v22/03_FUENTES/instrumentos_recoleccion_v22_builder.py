# -*- coding: utf-8 -*-
"""Paquete de instrumentos v22: hojas de campo capaces de recibir el registro
real de SIVAC.

La v21 imprimía las hojas del anexo de la tesis, pero no todos los campos que
la base de datos exige: no había columna de pausa ni de motivo, el documento y
el lote compartían una sola celda, el asiento no declaraba su tipo, y ni la
ficha documental ni el cuestionario tenían dónde anotar la observación de cada
fila. Llenar la v21 a mano obliga a inventar la pausa (y con ella T_reg), a
perder el lote o a no poder derivar el motivo M1-M8.

Esta versión conserva la maqueta aprobada (rótulo del anexo, objetivo con
sangría, bloque de identificación, rejilla, nota al pie; Times New Roman 12 pt,
A4 3/2,5/2,5/2,5 cm) y añade exactamente los campos que el diccionario de
variables de `datos/recolectados/README.md` y los CSV de
`datos/prueba_sintetica/` registran por fila:

* Instrumento 01 — pausa en segundos, motivo P1-P4, documento y lote
  separados, columna de validez y leyenda de motivos. La duración neta es
  hora de corte − hora de inicio − pausa, que es la regla con la que el
  conjunto cuadra en las 168 réplicas.
* Instrumento 02 — tipo de asiento (ING/SAL/TRA/DEV/AJU) y observación por
  asiento; nota que fija cómo se deriva el motivo M1-M8 de los criterios
  marcados N.
* Instrumento 03 — encuestador y recuadro de observaciones.

El módulo es autónomo: no depende del motor v14, que ya no está en el
repositorio y dejaba la compilación rota.

Uso
---
    python scripts/compiladores/instrumentos_recoleccion_v22_builder.py
    python scripts/compiladores/instrumentos_recoleccion_v22_builder.py --solo 03 04
    python scripts/compiladores/instrumentos_recoleccion_v22_builder.py --sin-pdf
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import fitz
from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

RAIZ = Path(__file__).resolve().parents[2]
VERSION = "v22"
BASE = RAIZ / "salidas" / "instrumentos" / ("INSTRUMENTOS_DEFINITIVOS_" + VERSION)
DIR_PDF = BASE / "01_IMPRIMIBLES"
DIR_DOCX = BASE / "02_EDITABLES"
DIR_FUENTES = BASE / "03_FUENTES"
DIR_CONTROL = BASE / "04_CONTROL_VISUAL"

FUENTE = "Times New Roman"
CUERPO = 12.0
REJILLA = 9.0
NOTA = 8.5
ANCHO = 15.5                 # cm útiles (21 - 3,0 - 2,5)
ANCHO_DXA = 8788
SELLO = "D:20260101000000Z"
MARCA_ZIP = (1980, 1, 1, 0, 0, 0)

MOMENTO = "[  ] Antes        [  ] Con el SIVAC"


# ---------------------------------------------------------------------------
# Documento y párrafos
# ---------------------------------------------------------------------------

def nueva_pagina() -> Document:
    doc = Document()
    seccion = doc.sections[0]
    seccion.page_width = Cm(21.0)
    seccion.page_height = Cm(29.7)
    seccion.top_margin = Cm(2.5)
    seccion.bottom_margin = Cm(2.5)
    seccion.left_margin = Cm(3.0)
    seccion.right_margin = Cm(2.5)
    seccion.header_distance = Cm(1.25)
    seccion.footer_distance = Cm(1.25)

    normal = doc.styles["Normal"]
    normal.font.name = FUENTE
    normal.font.size = Pt(CUERPO)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FUENTE)
    pf = normal.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.5

    pie = seccion.footer.paragraphs[0]
    pie.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = pie.add_run()
    run.font.name = FUENTE
    run.font.size = Pt(10)
    for tipo, texto in (("begin", None), (None, " PAGE "), ("end", None)):
        if tipo:
            fld = OxmlElement("w:fldChar")
            fld.set(qn("w:fldCharType"), tipo)
            run._r.append(fld)
        else:
            instr = OxmlElement("w:instrText")
            instr.set(qn("xml:space"), "preserve")
            instr.text = texto
            run._r.append(instr)
    return doc


def cerrar(doc: Document) -> None:
    """Last empty paragraph is unnecessary: the table already closes the page."""
    cuerpo = doc.element.body
    hijos = list(cuerpo.iterchildren())
    if len(hijos) > 1 and hijos[-2].tag == qn("w:p") and not hijos[-2].text:
        previo = hijos[-2]
        if not "".join(t.text or "" for t in previo.iter(qn("w:t"))).strip():
            cuerpo.remove(previo)


def _run(par, texto: str, size: float = CUERPO, bold: bool = False,
         italic: bool = False) -> None:
    run = par.add_run(texto)
    run.font.name = FUENTE
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run._element.rPr.rFonts.set(qn("w:eastAsia"), FUENTE)
    run._element.rPr.rFonts.set(qn("w:cs"), FUENTE)


def par(doc: Document, texto: str = "", size: float = CUERPO,
        bold: bool = False, italic: bool = False, sangria: bool = True,
        antes: float = 0, despues: float = 0, alineacion: str = "justify",
        interlinea: float = 1.5) -> Any:
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = {"justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
                    "left": WD_ALIGN_PARAGRAPH.LEFT,
                    "center": WD_ALIGN_PARAGRAPH.CENTER,
                    "right": WD_ALIGN_PARAGRAPH.RIGHT}[alineacion]
    pf.first_line_indent = Cm(1.25) if sangria else Cm(0)
    pf.space_before = Pt(antes)
    pf.space_after = Pt(despues)
    pf.line_spacing = interlinea
    if texto:
        _run(p, texto, size=size, bold=bold, italic=italic)
    return p


def rotulo(doc: Document, fijo: str, resto: str, nueva_hoja: bool = False
           ) -> None:
    p = doc.add_paragraph()
    pf = p.paragraph_format
    if nueva_hoja:
        pf.page_break_before = True
    pf.space_before = Pt(0)
    pf.space_after = Pt(8)
    pf.line_spacing = 1.15
    pf.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    _run(p, fijo + " " + resto, size=CUERPO, bold=True)


def objetivo(doc: Document, texto: str, despues: float = 12) -> None:
    par(doc, texto, size=CUERPO, sangria=True, despues=despues,
        alineacion="justify", interlinea=1.5)


def hueco(doc: Document, puntos: float = 10) -> None:
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.0
    run = p.add_run("")
    run.font.name = FUENTE
    run.font.size = Pt(puntos)


def nota(doc: Document, texto: str, antes: float = 6,
         size: float = NOTA) -> None:
    par(doc, "Nota. " + texto, size=size, sangria=False, antes=antes,
        alineacion="justify", interlinea=1.0)


# ---------------------------------------------------------------------------
# Rejilla
# ---------------------------------------------------------------------------

def _borde(tabla, exterior: int = 6, interior: int = 4) -> None:
    tblPr = tabla._tbl.tblPr
    previo = tblPr.find(qn("w:tblBorders"))
    if previo is not None:
        tblPr.remove(previo)
    bordes = OxmlElement("w:tblBorders")
    for lado, sz in (("top", exterior), ("left", exterior),
                     ("bottom", exterior), ("right", exterior),
                     ("insideH", interior), ("insideV", interior)):
        el = OxmlElement("w:" + lado)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(sz))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")
        bordes.append(el)
    tblPr.append(bordes)


def _margenes(tabla, lr: int, tb: int) -> None:
    tblPr = tabla._tbl.tblPr
    previo = tblPr.find(qn("w:tblCellMar"))
    if previo is not None:
        tblPr.remove(previo)
    mar = OxmlElement("w:tblCellMar")
    for lado, valor in (("top", tb), ("left", lr), ("bottom", tb),
                        ("right", lr)):
        el = OxmlElement("w:" + lado)
        el.set(qn("w:w"), str(valor))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblPr.append(mar)


def _geometria(tabla, anchos: Sequence[float]) -> None:
    dxa = [int(round(a * 567)) for a in anchos]
    delta = ANCHO_DXA - sum(dxa)
    dxa[-1] += delta
    tabla.autofit = False
    tblPr = tabla._tbl.tblPr
    for etiqueta in ("w:tblW", "w:tblLayout"):
        previo = tblPr.find(qn(etiqueta))
        if previo is not None:
            tblPr.remove(previo)
    ancho = OxmlElement("w:tblW")
    ancho.set(qn("w:w"), str(ANCHO_DXA))
    ancho.set(qn("w:type"), "dxa")
    tblPr.append(ancho)
    fijo = OxmlElement("w:tblLayout")
    fijo.set(qn("w:type"), "fixed")
    tblPr.append(fijo)
    for col, valor in zip(tabla._tbl.tblGrid.findall(qn("w:gridCol")), dxa):
        col.set(qn("w:w"), str(valor))
    for fila in tabla.rows:
        for celda, valor in zip(fila.cells, dxa):
            celda.width = Pt(valor / 20)


def _celda(celda, texto: str, size: float, bold: bool, alineacion: str,
           negativo: bool = False) -> None:
    celda.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    # Una celda fusionada arrastra el párrafo vacío de cada celda original y el
    # texto queda pegado al borde superior. Se conserva solo el primero.
    parrafos = celda.paragraphs
    for sobrante in parrafos[1:]:
        sobrante._element.getparent().remove(sobrante._element)
    p = parrafos[0]
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.0
    pf.first_line_indent = Cm(0)
    p.alignment = {"left": WD_ALIGN_PARAGRAPH.LEFT,
                   "center": WD_ALIGN_PARAGRAPH.CENTER,
                   "justify": WD_ALIGN_PARAGRAPH.JUSTIFY}[alineacion]
    partes = str(texto).split("\n")
    for i, parte in enumerate(partes):
        run = p.add_run(parte)
        run.font.name = FUENTE
        run.font.size = Pt(size)
        run.bold = bold
        run._element.rPr.rFonts.set(qn("w:eastAsia"), FUENTE)
        if i < len(partes) - 1:
            run.add_break()


def tabla(doc: Document, filas: Sequence[Sequence[Any]],
          anchos: Sequence[float],
          alturas: Optional[Sequence[Optional[float]]] = None,
          negritas: Sequence[int] = (), izq: Sequence[int] = (),
          verticales: Sequence[Tuple[int, int, int]] = (),
          size: float = REJILLA, margenes: Tuple[int, int] = (70, 16),
          centrada: bool = False) -> Any:
    """Rejilla de captura.

    Cada fila es una secuencia de celdas; una celda es un texto, o una tupla
    ``(texto, columnas_que_ocupa, negrita)`` para encabezados de banda.
    ``verticales`` fusiona filas: ``(desde, hasta, columna)``.
    """
    columnas = len(anchos)
    t = doc.add_table(rows=len(filas), cols=columnas)
    t.alignment = 1 if centrada else 0
    _geometria(t, anchos)
    _borde(t)
    _margenes(t, margenes[0], margenes[1])

    for i, fila in enumerate(filas):
        if alturas and i < len(alturas) and alturas[i]:
            t.rows[i].height = Cm(alturas[i])
            t.rows[i]._tr.get_or_add_trPr()

        col = 0
        for spec in fila:
            if isinstance(spec, tuple):
                texto, span = spec[0], spec[1]
                bold = spec[2] if len(spec) > 2 else False
            else:
                texto, span, bold = spec, 1, i in negritas
            if col >= columnas:
                break
            span = max(1, min(span, columnas - col))
            celda = t.cell(i, col)
            if span > 1:
                celda = celda.merge(t.cell(i, col + span - 1))
            alineacion = "left" if (col in izq or span > 1) else "center"
            if i in negritas and col not in izq and span == 1:
                alineacion = "center"
            _celda(celda, texto, size, bold, alineacion)
            col += span

    for desde, hasta, col in verticales:
        a = t.cell(desde, col)
        b = t.cell(hasta, col)
        fusion = a.merge(b)
        _celda(fusion, "", size, False, "center")

    return t


def identificacion(doc: Document, filas: Sequence[Sequence[Any]],
                   anchos: Sequence[float], altura: float = 0.72) -> Any:
    return tabla(doc, filas, anchos, alturas=[altura] * len(filas),
                 negritas=tuple(range(len(filas))), izq=(1, 3), size=9.0,
                 margenes=(90, 30))


# ---------------------------------------------------------------------------
# Anexo 4.1 — Instrumento N.° 01: tiempos
# ---------------------------------------------------------------------------

ANCHOS_REG = [0.75, 3.20, 2.40, 1.85, 1.28, 1.28, 1.02, 1.15, 1.42, 1.15]

CAB_REG = ["N.°", "Escenario y tarea observada", "Documento N.°", "Lote",
           "Hora de\ninicio", "Hora de\ncorte", "Pausa\n(s)", "Motivo",
           "T_reg\n(min)", "Válida\n(S/N)"]

# El vale no tiene lote: la columna del número ocupa las dos del registro y
# así las seis columnas restantes quedan alineadas en ambas bandas.
CAB_VALE = ["N.°", "Escenario y tarea observada", ("Vale PECOSA N.°", 2),
            "Hora de\nsolicitud", "Hora de\nemisión", "Pausa\n(s)", "Motivo",
            "T_vale\n(min)", "Válida\n(S/N)"]

TAREAS_REG = [
    "REG-01. Ingreso de lote al almacén (T1)",
    "REG-02. Salida o transferencia a la red (T2)",
    "REG-03. Redistribución a la red (T3)",
]
TAREAS_VALE = [
    "VALE-01. Vale simple para puesto de salud (T4)",
    "VALE-02. Vale regular para centro de salud (T5)",
    "VALE-03. Vale de reposición o contingencia (T6)",
]

LEYENDA_PAUSA = ("Motivos de pausa: P1 atención en ventanilla · P2 llamada del "
                 "establecimiento · P3 corte breve de energía · P4 "
                 "verificación de existencias.")

NOTA_TIEMPOS = (
    "Elaboración propia. T_reg = hora de corte − hora de inicio − pausa; "
    "T_vale = hora de emisión − hora de solicitud − pausa. La pausa se anota "
    "en segundos y se descuenta del intervalo, de modo que hora de corte − "
    "hora de inicio = duración neta + pausa. " + LEYENDA_PAUSA + " Una réplica "
    "es válida cuando la operación se completó sin interrupción distinta de "
    "las pausas anotadas; si no lo es, se marca N, se explica en "
    "observaciones y se repite la medición hasta completar tres réplicas "
    "válidas por indicador. El documento es el número del ingreso, salida, "
    "transferencia o ajuste; el lote es el código del biológico."
)


def pagina_tiempos(doc: Document) -> None:
    rotulo(doc, "Anexo 4.1.",
           "Instrumento N.° 01: ficha de registro de tiempos operativos")
    objetivo(doc,
             "El objetivo es medir el tiempo de registro de un movimiento de "
             "vacunas y el de emisión del vale de salida, antes y con el "
             "SIVAC. La ficha registra seis operaciones: tres de registro y "
             "tres de emisión del vale.", despues=10)

    identificacion(doc, [
        ["Operador (TRAB)", "", "Centro de acopio", ""],
        ["Fecha", "", "Momento", MOMENTO],
        ["Observador", "", "Periodo auditado", "del ____ al ____"],
    ], [3.0, 4.3, 3.0, 5.2], altura=0.54)

    hueco(doc, 8)
    filas: List[List[Any]] = [
        [("REGISTRO DEL MOVIMIENTO DE VACUNAS (T_reg)", 10, True)],
        CAB_REG,
    ]
    for n, tarea in enumerate(TAREAS_REG, 1):
        filas.append([str(n), tarea, "", "", "", "", "", "", "", ""])
    filas += [
        [("EMISIÓN DEL VALE DE SALIDA (T_vale)", 10, True)],
        CAB_VALE,
    ]
    for n, tarea in enumerate(TAREAS_VALE, 1):
        filas.append([str(n), tarea, ("", 2), "", "", "", "", "", ""])

    tabla(doc, filas, ANCHOS_REG,
          alturas=[0.42, 0.88] + [1.16] * 3 + [0.42, 0.88] + [1.16] * 3,
          negritas=(0, 1, 5, 6), izq=(1, 2), size=8.0,
          margenes=(55, 12))

    hueco(doc, 8)
    tabla(doc, [
        [("RESUMEN DEL OPERADOR", 3, True)],
        ["T_reg promedio (min)", "T_vale promedio (min)",
         "Réplicas válidas (de 6)"],
        ["", "", ""],
    ], [5.1667] * 3, [0.42, 0.80, 0.94], negritas=(0, 1))

    hueco(doc, 8)
    tabla(doc, [
        [("OBSERVACIONES", 1, True)],
        [""], [""],
    ], [ANCHO], [0.36, 0.90, 0.90], negritas=(0,))

    hueco(doc, 6)
    _firma(doc, "Firma del observador")

    nota(doc, NOTA_TIEMPOS, antes=5)


# ---------------------------------------------------------------------------
# Anexo 4.2 — Instrumento N.° 02: auditoría documental
# ---------------------------------------------------------------------------

CRITERIOS: Tuple[str, ...] = (
    "Biológico", "Lote", "Vencimiento", "Cantidad", "Origen y destino",
    "Responsable", "Saldo", "Correlatividad",
)

MOTIVOS_M: Tuple[str, ...] = (
    "M1 biológico", "M2 lote", "M3 vencimiento", "M4 cantidad física",
    "M5 origen y destino", "M6 responsable y firma", "M7 saldo aritmético",
    "M8 correlatividad",
)

# N.° · Fecha · Tipo · Documento · Biológico · Lote · Cant. · 8 criterios ·
# Conf. · Motivo · Observación. La v22 reunía motivo y observación en una sola
# celda de 2,38 cm: ni «M2+M8» ni la frase del auditor cabían en un renglón y
# la hoja resultaba ilegible escrita a mano. Se separan las dos columnas y se
# recortan las de marca —que solo llevan S o N— para que la observación
# disponga de 3,00 cm, ancho de dos renglones manuscritos.
ANCHOS_A = ([0.46, 0.96, 0.72, 1.64, 1.22, 1.16, 0.72] + [0.42] * 8
            + [1.20, 0.96, 2.70])
ANCHO_A_MOT = len(ANCHOS_A) - 2        # 15
ANCHO_A_ULT = len(ANCHOS_A) - 1        # 16

TIPOS = "ING ingreso · SAL salida · TRA transferencia · DEV devolución · AJU ajuste"


def _ident_documental(doc: Document, hoja: str) -> None:
    identificacion(doc, [
        ["Operador (TRAB)", "", "Centro de acopio", ""],
        ["Periodo auditado", "del ____ al ____", "Momento", MOMENTO],
        ["Hoja", hoja, "Auditor", ""],
    ], [3.0, 4.3, 3.0, 5.2], altura=0.54)


def _encabezado_asientos() -> List[List[Any]]:
    return [
        [("BLOQUE A. ASIENTOS DEL KARDEX", len(ANCHOS_A), True)],
        [("N.°", 1), ("DATOS DEL ASIENTO", 6),
         ("CRITERIOS DE CONFORMIDAD", 8), ("Conf.", 1),
         ("Motivo", 1), ("Observación", 1)],
        ["", "Fecha", "Tipo", "Documento", "Biológico", "Lote", "Cant."] +
        [str(n) for n in range(1, 9)] + ["", "", ""],
    ]


def _tabla_asientos(doc: Document, desde: int, hasta: int,
                    alto: float = 0.62) -> None:
    filas = _encabezado_asientos()
    for n in range(desde, hasta + 1):
        filas.append([str(n)] + [""] * (len(ANCHOS_A) - 1))
    tabla(doc, filas, ANCHOS_A,
          alturas=[0.40, 0.48, 0.46] + [alto] * (hasta - desde + 1),
          negritas=(0, 1, 2), izq=(3, 4, 5),
          verticales=((1, 2, 0), (1, 2, ANCHO_A_MOT),
                      (1, 2, ANCHO_A_ULT)),
          size=7.0, margenes=(28, 6))


def _resumen(doc: Document, etiqueta: str, alto: float = 0.74) -> None:
    """Cierre del bloque A en un solo renglón escribible: revisados, conformes
    y RSD. La v22 gastaba dos renglones y empujaba la tabla fuera de la hoja."""
    tabla(doc, [
        [(etiqueta, 1, False), "", ("Asientos conformes", 1, True), "",
         ("RSD (%)", 1, True), ""],
    ], [3.90, 1.30, 3.30, 1.30, 2.10, 1.30], [alto],
       negritas=(), izq=(0, 2, 4), size=8.0, margenes=(60, 24))


def _observaciones(doc: Document, filas: int = 2, alto: float = 0.60) -> None:
    tabla(doc, [[("OBSERVACIONES", 1, True)]] + [[""] for _ in range(filas)],
          [ANCHO], [0.34] + [alto] * filas, negritas=(0,), size=8.5)


def _firma(doc: Document, etiqueta: str, alto: float = 0.62) -> None:
    """Línea de suscripción: la ficha impresa debe poder acreditar quién midió."""
    tabla(doc, [[etiqueta, ""]], [4.6, 10.9], [alto],
          negritas=(0,), izq=(0, 1), size=8.5, margenes=(60, 10))


NOTA_ASIENTOS = (
    "Fuente: NTS N.° 196-MINSA/DGIESP-2022 y elaboración propia. Tipo: "
    + TIPOS + ". Los números 1 a 8 de la rejilla son los criterios y el "
    "motivo: 1 biológico, 2 lote, 3 vencimiento, 4 cantidad física, 5 origen "
    "y destino, 6 responsable y firma, 7 saldo aritmético, 8 correlatividad. "
    "El asiento es conforme solo si los ocho están en S; en «Motivo» se "
    "anotan los criterios marcados N y en «Observación», la frase del "
    "auditor. RSD = conformes ÷ revisados × 100."
)


def pagina_documental_a(doc: Document) -> None:
    rotulo(doc, "Anexo 4.2.",
           "Instrumento N.° 02: ficha de auditoría del kardex")
    objetivo(doc,
             "El objetivo es verificar que cada asiento del kardex coincida "
             "con el documento que lo sustenta.", despues=8)
    _ident_documental(doc, "1 de 2 (bloque A)")

    hueco(doc, 3)
    _tabla_asientos(doc, 1, 20)

    hueco(doc, 3)
    _resumen(doc, "Asientos revisados (hoja 1)")

    hueco(doc, 3)
    _observaciones(doc, 1, 0.44)

    hueco(doc, 3)
    _firma(doc, "Firma del auditor", 0.56)

    nota(doc, NOTA_ASIENTOS, antes=5, size=7.6)


def pagina_documental_b(doc: Document) -> None:
    rotulo(doc, "Anexo 4.2.",
           "Instrumento N.° 02: ficha de auditoría del kardex "
           "(continuación)", nueva_hoja=True)
    objetivo(doc,
             "El objetivo es completar la auditoría del kardex del mismo "
             "operador y momento (asientos 21 a 40).", despues=8)
    _ident_documental(doc, "2 de 2 (bloque A)")

    hueco(doc, 3)
    _tabla_asientos(doc, 21, 40)

    hueco(doc, 3)
    _resumen(doc, "Asientos revisados (total)")

    hueco(doc, 3)
    _observaciones(doc, 1, 0.44)

    hueco(doc, 3)
    _firma(doc, "Firma del auditor", 0.56)

    nota(doc, NOTA_ASIENTOS + " Las dos hojas se archivan juntas: la suma de "
              "asientos revisados de ambas debe ser cuarenta.", antes=5,
         size=7.6)


def pagina_documental_c(doc: Document) -> None:
    rotulo(doc, "Anexo 4.2.",
           "Instrumento N.° 02: conciliación de despachos", nueva_hoja=True)
    objetivo(doc,
             "El objetivo es comparar la cantidad programada con la entregada "
             "en cada despacho del operador y momento auditados. La ficha "
             "concilia veinticinco despachos.", despues=10)
    _ident_documental(doc, "1 de 1 (bloque B)")

    hueco(doc, 8)
    anchos = [0.78, 1.42, 1.20, 1.66, 1.56, 1.52, 2.36, 0.95, 4.05]
    filas: List[List[Any]] = [
        [("BLOQUE B. DESPACHOS CONCILIADOS", 9, True)],
        ["N.°", "Fecha", "Biológico", "Programado", "Entregado", "Diferencia",
         "Documento", "Conf.", "Obs."],
    ]
    for n in range(1, 26):
        filas.append([str(n)] + [""] * 8)
    # Sin fusión vertical en la columna N.°: el encabezado ocupa una fila y la
    # numeración empieza en 1. Fusionar (1, 2, 0) borraba el despacho 1 y la
    # hoja quedaba con 24 renglones útiles cuando la nota pide 25.
    tabla(doc, filas, anchos, alturas=[0.36, 0.52] + [0.48] * 25,
          negritas=(0, 1), izq=(6, 8),
          size=7.5, margenes=(32, 3))

    hueco(doc, 6)
    tabla(doc, [
        ["Despachos evaluados", "Despachos conformes", "CPE (%)"],
        ["", "", ""],
    ], [5.1667] * 3, [0.42, 0.58], negritas=(0,), size=8.5)

    hueco(doc, 6)
    _observaciones(doc, 1, 0.58)

    hueco(doc, 6)
    _firma(doc, "Firma del auditor")

    nota(doc, "Elaboración propia. El despacho es conforme cuando la cantidad "
              "entregada iguala la programada y el documento coincide con el "
              "registro; una diferencia se anota, no se corrige en la hoja. "
              "Diferencia = entregado − programado: negativa, faltante; "
              "positiva, exceso. "
              "CPE = despachos conformes ÷ despachos evaluados × 100.",
         antes=6)


# ---------------------------------------------------------------------------
# Anexo 4.3 — Instrumento N.° 03: cuestionario
# ---------------------------------------------------------------------------

REACTIVOS_AP: Tuple[Tuple[str, str], ...] = (
    ("AP-01", "El procedimiento de registro de movimientos de vacunas resulta "
              "ágil y sin demoras innecesarias."),
    ("AP-02", "La emisión de comprobantes y vales de salida se realiza con "
              "facilidad y claridad en los pasos requeridos."),
    ("AP-03", "El flujo operativo para conciliar saldos mensuales reduce la "
              "fatiga y el esfuerzo administrativo."),
    ("AP-04", "Considero que la modalidad de trabajo empleada es cómoda, "
              "ordenada y eficiente para mis labores."),
)

REACTIVOS_UP: Tuple[Tuple[str, str], ...] = (
    ("UP-01", "La plataforma o método de trabajo mejora mi productividad y "
              "desempeño en el control de vacunas."),
    ("UP-02", "El sistema proporciona información precisa y oportuna para la "
              "toma de decisiones en inmunizaciones."),
    ("UP-03", "La aplicación de reglas automáticas de control (como FEFO) "
              "evita errores y vencimiento de biológicos."),
    ("UP-04", "En términos generales, considero sumamente útil la herramienta "
              "para la gestión institucional en la DISA."),
)

D1 = "Dimensión 1: Aceptación del proceso (AP)"
D2 = "Dimensión 2: Utilidad percibida (UP)"


def _escala_likert(doc: Document) -> None:
    filas = [
        [("ESCALA DE MEDICIÓN LIKERT", 5, True)],
        [("Nomenclatura", 5, True)],
        ["Muy en\ndesacuerdo", "En\ndesacuerdo", "Indiferente", "De acuerdo",
         "Totalmente\nde acuerdo"],
        [("Valoración", 5, True)],
        ["1", "2", "3", "4", "5"],
    ]
    tabla(doc, filas, [3.1] * 5, alturas=[0.46, 0.34, 0.90, 0.34, 0.42],
          size=REJILLA, negritas=(0, 1, 3, 4), margenes=(80, 10),
          centrada=True)
    par(doc, "Nota. Elaboración propia.", size=NOTA, sangria=False,
        antes=4, despues=8, alineacion="left", interlinea=1.0)


def pagina_cuestionario(doc: Document) -> None:
    rotulo(doc, "Anexo 4.3.",
           "Instrumento N.° 03: cuestionario de satisfacción del usuario")
    objetivo(doc,
             "El objetivo es conocer la aceptación del proceso y la utilidad "
             "percibida del sistema SIVAC en el personal de inmunizaciones. "
             "Son ocho preguntas de respuesta anónima.", despues=10)

    identificacion(doc, [
        ["Operador (TRAB)", "", "Centro de acopio", ""],
        ["Fecha", "", "Momento", MOMENTO],
        ["Encuestador", ("", 3)],
    ], [3.0, 4.3, 3.0, 5.2], altura=0.54)
    hueco(doc, 10)

    _escala_likert(doc)

    anchos = [1.05, 1.35, 8.00, 1.02, 1.02, 1.02, 1.02, 1.02]
    filas: List[List[Any]] = [
        [("VARIABLE DEPENDIENTE: GESTIÓN DE MOVIMIENTOS MENSUALES DE VACUNAS",
          8, True)],
        [("N.°", 1), ("Código", 1), ("Reactivo", 1),
         ("Escala de medición (1 a 5)", 5)],
        ["", "", "", "1", "2", "3", "4", "5"],
    ]
    alturas: List[Optional[float]] = [0.52, 0.44, 0.34]
    negritas = [0, 1, 2]

    filas.append([(D1, 8, True)])
    alturas.append(0.40)
    negritas.append(len(filas) - 1)
    n = 0
    for codigo, texto in REACTIVOS_AP:
        n += 1
        filas.append([str(n), codigo, texto, "", "", "", "", ""])
        alturas.append(1.14)
    for codigo, texto in REACTIVOS_UP:
        n += 1
        if n == 5:
            filas.append([(D2, 8, True)])
            alturas.append(0.40)
            negritas.append(len(filas) - 1)
        filas.append([str(n), codigo, texto, "", "", "", "", ""])
        alturas.append(1.14)

    alturas = [a if a != 1.14 else 0.92 for a in alturas]
    tabla(doc, filas, anchos, alturas=alturas, size=REJILLA,
          negritas=tuple(negritas), izq=(2,),
          verticales=((1, 2, 0), (1, 2, 1)), margenes=(65, 12))

    hueco(doc, 8)
    tabla(doc, [
        [("PUNTAJE (se completa al final; no lo llena el encuestado)", 4,
          True)],
        ["AP (4 a 20)", "UP (4 a 20)", "TAM (8 a 40)", "Nivel"],
        ["", "", "", ""],
    ], [3.10, 3.10, 3.60, 5.70], [0.32, 0.54, 0.62], negritas=(0, 1),
       size=8.0)

    hueco(doc, 8)
    _observaciones(doc, 1, 0.62)

    hueco(doc, 8)
    _firma(doc, "Firma del encuestador")

    nota(doc, "Elaboración propia, sobre el modelo de aceptación tecnológica "
              "de Davis (1989). Cada dimensión suma cuatro ítems (4 a 20 "
              "puntos) y el total es la suma de las dos (8 a 40 puntos). "
              "Marque una sola opción por ítem. Baremo del TAM: Bajo 8 a 18, "
              "Medio 19 a 29, Alto 30 a 40.", antes=6)



# ---------------------------------------------------------------------------
# Hoja de observaciones de la sesión (registro complementario)
# ---------------------------------------------------------------------------

ANCHOS_OBS = [0.70, 1.95, 2.55, 1.60, 1.45, 1.12, 1.12, 0.95, 0.95, 1.35,
              1.06]


def pagina_observaciones(doc: Document) -> None:
    rotulo(doc, "Hoja de observaciones.",
           "Registro complementario de la sesión de campo")
    objetivo(doc,
             "La hoja recoge lo que no tiene columna en las otras tres fichas: "
             "la réplica que reemplaza a una inválida, los totales reales "
             "cuando el kardex o los despachos del periodo no alcanzan la "
             "meta, y las incidencias de la sesión. Se llena durante la "
             "observación, no después, y cada anotación remite a la hoja y a "
             "la casilla que corrige o completa.", despues=8)

    identificacion(doc, [
        ["Operador (TRAB)", "", "Centro de acopio", ""],
        ["Fecha", "", "Momento", MOMENTO],
        ["Observador", "", "Periodo auditado", "del ____ al ____"],
    ], [3.0, 4.3, 3.0, 5.2], altura=0.54)

    hueco(doc, 8)
    filas: List[List[Any]] = [
        [("RÉPLICAS DE REEMPLAZO (Instrumento 01)", len(ANCHOS_OBS), True)],
        ["N.°", "Reemplaza a", "Escenario y tarea observada", "Documento N.°",
         "Lote", "Hora de\ninicio", "Hora de\ncorte", "Pausa\n(s)", "Motivo",
         "Duración\n(min)", "Válida\n(S/N)"],
    ]
    for n in range(1, 5):
        filas.append([str(n)] + [""] * (len(ANCHOS_OBS) - 1))
    tabla(doc, filas, ANCHOS_OBS, alturas=[0.40, 0.66] + [0.92] * 4,
          negritas=(0, 1), izq=(2, 3),
          verticales=((1, 1, 0),), size=7.6, margenes=(40, 8))

    nota(doc, "Se usa solo cuando una réplica del Instrumento 01 quedó marcada "
              "N. En «Reemplaza a» se anota la tarea y el número de la réplica "
              "sustituida (por ejemplo REG-02, réplica 3). La duración se "
              "calcula con la misma regla de la ficha: hora de corte − hora de "
              "inicio − pausa, en minutos con cuatro decimales. Si la réplica "
              "de reemplazo se mide en una visita posterior, se anota la fecha "
              "en la primera línea de anotaciones.", antes=5, size=7.6)

    hueco(doc, 8)
    filas = [[("ANOTACIONES DE LA SESIÓN", 3, True)],
             [("N.°", 1), ("Hoja y casilla", 1), ("Anotación", 1)]]
    for n in range(1, 11):
        filas.append([str(n), "", ""])
    tabla(doc, filas, [0.90, 4.10, 10.50], alturas=[0.38, 0.42] + [0.66] * 10,
          negritas=(0, 1), izq=(1, 2),
          verticales=((1, 1, 0),), size=7.6, margenes=(50, 10))

    nota(doc, "Cada anotación debe poder leerse junto a la hoja que completa: "
              "«02-A, asiento 34, motivo: M7 y M8» o «02-B, total real de "
              "despachos del periodo: 19». Las cifras que la hoja declara "
              "—totales reales, réplicas de reemplazo, sesiones no aplicables—"
              " son las que usa la digitación; no se corrigen en la ficha.",
         antes=5, size=7.6)

    hueco(doc, 8)
    _firma(doc, "Firma del observador")


# ---------------------------------------------------------------------------
# Documentos y exportación
# ---------------------------------------------------------------------------

def doc_tiempos() -> Document:
    doc = nueva_pagina()
    pagina_tiempos(doc)
    cerrar(doc)
    return doc


def doc_documental() -> Document:
    doc = nueva_pagina()
    pagina_documental_a(doc)
    pagina_documental_b(doc)
    pagina_documental_c(doc)
    cerrar(doc)
    return doc


def doc_observaciones() -> Document:
    doc = nueva_pagina()
    pagina_observaciones(doc)
    cerrar(doc)
    return doc


def doc_cuestionario() -> Document:
    doc = nueva_pagina()
    pagina_cuestionario(doc)
    cerrar(doc)
    return doc


CARTA = RAIZ / "CARTA-DE-AUTORIZACION.pdf"

LEEME = """# Instrumentos de recolección de datos (v22)

| Archivo | Contenido | Hojas |
| --- | --- | --- |
| 01_CARTA_AUTORIZACION | Carta de autorización institucional firmada y sellada | 2 |
| 03_INSTRUMENTO_01_TIEMPOS | Ficha de registro de tiempos: pausa, motivo, documento y lote separados, validez | 1 |
| 04_INSTRUMENTO_02_DOCUMENTAL | Auditoría del kardex (2 hojas, 20 asientos cada una, con tipo y observación) y conciliación de 25 despachos | 3 |
| 05_INSTRUMENTO_03_CUESTIONARIO | Cuestionario de aceptación y utilidad percibida, 8 reactivos Likert, con encuestador y observaciones | 1 |
| 06_HOJA_DE_OBSERVACIONES | Réplicas de reemplazo y anotaciones de la sesión | 1 |
| 00_PAQUETE_COMPLETO | Los cinco documentos en orden de uso | 8 |

Fuera de `01_IMPRIMIBLES`:

| Carpeta | Contenido |
| --- | --- |
| 02_EDITABLES | Los cuatro documentos en DOCX, para corregir la maqueta |
| 03_FUENTES | El compilador que genera el paquete |
| 04_CONTROL_VISUAL | Una imagen por página, para revisar la maqueta sin abrir el PDF |
| 05_GUIA | Guía de llenado y control de la sesión (9 páginas) |
| 07_CAPTURA | LIBRO_DE_CAPTURA_v22.xlsx: una fila por registro previsto, claves escritas y mediciones en blanco |

El libro de captura no se consolida a mano: `scripts/estadistica/
consolidar_libro_captura.py` lee sus cuatro hojas, recalcula la aritmética de
cada ficha y escribe `datos/recolectados/pretest_campo.csv` y
`posttest_campo.csv`. Sin `--escribir` solo audita y enumera lo que falta; con
`--escribir` exige las veintiocho sesiones completas.

La v21 no admitía el registro real: no tenía pausa ni motivo, unía documento y
lote en una celda, no declaraba el tipo de asiento, no tenía columna de validez
y no dejaba anotar la observación de cada fila. La v22 conserva la maqueta
aprobada (Times New Roman 12 pt, A4, márgenes 3 / 2,5 / 2,5 / 2,5 cm) y añade
esos campos.

Los conteos coinciden con la tesis y con la base de datos: seis operaciones
cronometradas (tres de registro y tres de emisión del vale), cuarenta asientos
de kardex por operador y momento (veinte por hoja), veinticinco despachos,
ocho criterios de conformidad y ocho reactivos AP/UP.

El paquete no incluye consentimiento informado: el permiso formal es la Carta
de Autorización, que la tesis reproduce en el Anexo 8.
"""


DOCUMENTOS: Dict[str, Tuple[str, Any]] = {
    "01_CARTA_AUTORIZACION": (
        "Carta de autorización institucional", CARTA),
    "03_INSTRUMENTO_01_TIEMPOS": (
        "Anexo 4.1. Ficha de registro de tiempos", doc_tiempos),
    "04_INSTRUMENTO_02_DOCUMENTAL": (
        "Anexo 4.2. Ficha de auditoría documental", doc_documental),
    "05_INSTRUMENTO_03_CUESTIONARIO": (
        "Anexo 4.3. Cuestionario de satisfacción del usuario",
        doc_cuestionario),
    "06_HOJA_DE_OBSERVACIONES": (
        "Hoja de observaciones de la sesión", doc_observaciones),
}

PAGINAS_ESPERADAS = {
    "01_CARTA_AUTORIZACION": 2,
    "03_INSTRUMENTO_01_TIEMPOS": 1,
    "04_INSTRUMENTO_02_DOCUMENTAL": 3,
    "05_INSTRUMENTO_03_CUESTIONARIO": 1,
    "06_HOJA_DE_OBSERVACIONES": 1,
}

ORDEN_PAQUETE = ("01_CARTA_AUTORIZACION",
                 "03_INSTRUMENTO_01_TIEMPOS",
                 "04_INSTRUMENTO_02_DOCUMENTAL",
                 "05_INSTRUMENTO_03_CUESTIONARIO",
                 "06_HOJA_DE_OBSERVACIONES")


def exportar_pdf(docx: Path, pdf: Path) -> None:
    with tempfile.TemporaryDirectory() as temporal:
        subprocess.run(["soffice", "--headless", "--norestore",
                        "--convert-to", "pdf", "--outdir", temporal,
                        str(docx)], check=True, capture_output=True,
                       timeout=300)
        normalizar_pdf(Path(temporal) / (docx.stem + ".pdf"), pdf)


def normalizar_pdf(origen: Path, destino: Path) -> None:
    documento = fitz.open(origen)
    metadatos = documento.metadata or {}
    metadatos["creationDate"] = SELLO
    metadatos["modDate"] = ""
    documento.set_metadata(metadatos)
    documento.save(destino, garbage=4, deflate=True, no_new_id=True)
    documento.close()
    crudo = destino.read_bytes()
    patron = re.compile(rb"/ID\[<[0-9A-Fa-f]{32}><[0-9A-Fa-f]{32}>\]")
    fijo = hashlib.sha256(patron.sub(b"", crudo)).hexdigest().upper()[:32]
    destino.write_bytes(
        patron.sub(b"/ID[<" + fijo.encode() + b"><" + fijo.encode() + b">]",
                   crudo))


def fijar_marcas_zip(ruta: Path) -> None:
    with zipfile.ZipFile(ruta) as original:
        entradas = [(i.filename, original.read(i.filename))
                    for i in original.infolist()]
    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as destino:
        for nombre, datos in entradas:
            info = zipfile.ZipInfo(nombre, date_time=MARCA_ZIP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            destino.writestr(info, datos)


def sha256(ruta: Path) -> str:
    digest = hashlib.sha256()
    with open(ruta, "rb") as manejador:
        for bloque in iter(lambda: manejador.read(1 << 20), b""):
            digest.update(bloque)
    return digest.hexdigest()


def sello_compilacion() -> str:
    segundos = os.environ.get("SOURCE_DATE_EPOCH")
    if segundos and segundos.isdigit():
        from datetime import datetime, timezone
        return datetime.fromtimestamp(int(segundos), timezone.utc).isoformat(
            timespec="seconds")
    return "2026-11-07T00:00:00"


def control_visual(pdf: Path, destino: Path, dpi: int = 110) -> None:
    documento = fitz.open(pdf)
    for i, pagina in enumerate(documento, 1):
        imagen = destino / f"{pdf.stem}-{i}.png"
        pagina.get_pixmap(dpi=dpi).save(imagen)
    documento.close()


def compilar(solo: Optional[Sequence[str]] = None, con_pdf: bool = True
             ) -> Dict[str, Any]:
    for directorio in (DIR_PDF, DIR_DOCX, DIR_FUENTES, DIR_CONTROL):
        directorio.mkdir(parents=True, exist_ok=True)
    for previo in DIR_CONTROL.glob("*.png"):
        previo.unlink()

    manifiesto: Dict[str, Any] = {
        "version": VERSION,
        "fecha": sello_compilacion(),
        "tipografia": FUENTE,
        "geometria": "A4 21 x 29,7 cm; margenes 3,0 / 2,5 / 2,5 / 2,5 cm; "
                     "ancho util 15,5 cm",
        "documentos": {},
    }
    for nombre, (descripcion, constructor) in DOCUMENTOS.items():
        if solo and not any(nombre.startswith(s) for s in solo):
            continue
        if isinstance(constructor, Path):
            pdf = DIR_PDF / f"{nombre}_{VERSION}.pdf"
            normalizar_pdf(constructor, pdf)
            paginas = fitz.open(pdf).page_count
            esperadas = PAGINAS_ESPERADAS[nombre]
            if paginas != esperadas:
                raise SystemExit(
                    f"{nombre}: {paginas} páginas, se esperaban {esperadas}")
            manifiesto["documentos"][nombre] = {
                "descripcion": descripcion,
                "pdf": str(pdf.relative_to(RAIZ)),
                "paginas": paginas,
                "sha256_pdf": sha256(pdf),
                "origen": str(constructor.relative_to(RAIZ)),
            }
            control_visual(pdf, DIR_CONTROL)
            print(f"{nombre}: {paginas} p.")
            continue
        docx = DIR_DOCX / f"{nombre}_{VERSION}.docx"
        constructor().save(docx)
        fijar_marcas_zip(docx)
        entrada: Dict[str, Any] = {
            "descripcion": descripcion,
            "docx": str(docx.relative_to(RAIZ)),
            "sha256_docx": sha256(docx),
        }
        if con_pdf:
            pdf = DIR_PDF / f"{nombre}_{VERSION}.pdf"
            exportar_pdf(docx, pdf)
            paginas = fitz.open(pdf).page_count
            esperadas = PAGINAS_ESPERADAS[nombre]
            if paginas != esperadas:
                raise SystemExit(
                    f"{nombre}: {paginas} páginas, se esperaban {esperadas}")
            entrada.update({"pdf": str(pdf.relative_to(RAIZ)),
                            "paginas": paginas, "sha256_pdf": sha256(pdf)})
            control_visual(pdf, DIR_CONTROL)
        manifiesto["documentos"][nombre] = entrada
        print(f"{nombre}: {entrada.get('paginas', '-')} p.")

    completo_ok = con_pdf and all(n in manifiesto["documentos"]
                                  for n in ORDEN_PAQUETE)
    if completo_ok:
        completo = fitz.open()
        for nombre in ORDEN_PAQUETE:
            completo.insert_pdf(fitz.open(RAIZ /
                                          manifiesto["documentos"][nombre]["pdf"]))
        destino = DIR_PDF / f"00_PAQUETE_COMPLETO_{VERSION}.pdf"
        with tempfile.TemporaryDirectory() as temporal:
            crudo = Path(temporal) / "paquete.pdf"
            metadatos = completo.metadata or {}
            metadatos["creationDate"] = SELLO
            metadatos["modDate"] = ""
            completo.set_metadata(metadatos)
            completo.save(crudo, garbage=4, deflate=True)
            completo.close()
            normalizar_pdf(crudo, destino)
        manifiesto["paquete_completo"] = {
            "pdf": str(destino.relative_to(RAIZ)),
            "paginas": fitz.open(destino).page_count,
            "sha256_pdf": sha256(destino)}
        print(f"00_PAQUETE_COMPLETO: "
              f"{manifiesto['paquete_completo']['paginas']} p.")

    shutil.copy2(Path(__file__), DIR_FUENTES / Path(__file__).name)
    (BASE / "LEEME.md").write_text(LEEME, encoding="utf-8")
    (BASE / f"MANIFIESTO_{VERSION}.json").write_text(
        json.dumps(manifiesto, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifiesto


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solo", nargs="*")
    parser.add_argument("--sin-pdf", action="store_true")
    args = parser.parse_args()
    compilar(args.solo, con_pdf=not args.sin_pdf)


if __name__ == "__main__":
    main()
