# -*- coding: utf-8 -*-
"""
Motor centralizado de Cirugía OpenXML Nativa para Microsoft Word (.docx), PDF 1.4, XLSX y PNG 300 DPI
bajo normas APA 7 y UNAJMA.
Referencia oficial: .claude/skills/tablas-quirurgicas-docx-apa7/SKILL.md
"""
import argparse
import hashlib
import html
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile
import zlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"


def eliminar_flotacion_tabla(table) -> bool:
    """Elimina el nodo <w:tblpPr> si existe para impedir tablas flotantes."""
    tblPr = getattr(getattr(table, "_tbl", None), "tblPr", None)
    if tblPr is None:
        return False
    removido = False
    for child in list(tblPr):
        if child.tag.endswith("tblpPr"):
            tblPr.remove(child)
            removido = True
    return removido


def configurar_geometria_tabla(
    table,
    total_width_dxa: int = 8788,
    col_widths_dxa: Optional[Sequence[int]] = None,
    align: str = "center",
) -> None:
    """Configura el ancho exacto en dxa y elimina cualquier flotación w:tblpPr."""
    eliminar_flotacion_tabla(table)
    if col_widths_dxa and hasattr(table, "rows"):
        for row in table.rows:
            for idx, cell in enumerate(row.cells):
                if idx < len(col_widths_dxa):
                    cell.width = col_widths_dxa[idx]


def aplicar_bordes_rejilla(tabla, sz: int = 4) -> None:
    """Aplica rejilla visible completa (seis bordes) a una tabla nativa de campo.

    Excepción declarada al bordado APA 7 de tres líneas horizontales: las decisiones
    DEC-025 y DEC-026 exigen rejilla visible en los instrumentos de campo, porque las
    casillas que se llenan a mano se pierden al imprimir cuando la tabla solo lleva
    bordes horizontales. Se aplica a los formularios de campo y a las guías de llenado;
    las tablas narrativas del informe conservan las tres líneas horizontales.

    ``sz`` se expresa en octavos de punto (4 = 0.5 pt). Mantiene el orden de hijos de
    CT_TblPr, no inserta flotación y no altera filas, celdas ni anchos.
    """
    from docx.oxml import OxmlElement

    tbl = getattr(tabla, "_tbl", tabla)
    tblPr = tbl.tblPr
    if tblPr is None:
        return
    existente = tblPr.find(_qn("w:tblBorders"))
    if existente is not None:
        tblPr.remove(existente)
    bordes = OxmlElement("w:tblBorders")
    for borde in ("top", "left", "bottom", "right", "insideH", "insideV"):
        elemento = OxmlElement(f"w:{borde}")
        elemento.set(_qn("w:val"), "single")
        elemento.set(_qn("w:sz"), str(int(sz)))
        elemento.set(_qn("w:space"), "0")
        elemento.set(_qn("w:color"), "000000")
        bordes.append(elemento)
    posteriores = ("w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook", "w:tblCaption", "w:tblDescription")
    referencia = None
    for etiqueta in posteriores:
        hallado = tblPr.find(_qn(etiqueta))
        if hallado is not None:
            referencia = hallado
            break
    if referencia is not None:
        referencia.addprevious(bordes)
    else:
        tblPr.append(bordes)


def aplicar_bordes_campo(tabla, exterior_sz: int = 8,
                         interior_sz: int = 4) -> None:
    """Rejilla de campo con exterior 1 pt e interior 0.5 pt.

    Conserva la excepción declarada de rejilla visible para los formularios de
    campo y evita el peso visual uniforme de 1 pt en todas las líneas. No
    inserta flotación ni altera anchos, filas o celdas.
    """
    from docx.oxml import OxmlElement

    tbl = getattr(tabla, "_tbl", tabla)
    tblPr = tbl.tblPr
    if tblPr is None:
        return
    existente = tblPr.find(_qn("w:tblBorders"))
    if existente is not None:
        tblPr.remove(existente)
    bordes = OxmlElement("w:tblBorders")
    for borde in ("top", "left", "bottom", "right", "insideH", "insideV"):
        elemento = OxmlElement(f"w:{borde}")
        elemento.set(_qn("w:val"), "single")
        elemento.set(_qn("w:sz"),
                     str(int(exterior_sz if borde in
                             ("top", "left", "bottom", "right") else interior_sz)))
        elemento.set(_qn("w:space"), "0")
        elemento.set(_qn("w:color"), "000000")
        bordes.append(elemento)
    posteriores = ("w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook",
                   "w:tblCaption", "w:tblDescription")
    referencia = None
    for etiqueta in posteriores:
        hallado = tblPr.find(_qn(etiqueta))
        if hallado is not None:
            referencia = hallado
            break
    if referencia is not None:
        referencia.addprevious(bordes)
    else:
        tblPr.append(bordes)


def banda_institucional(
    documento,
    ruta_logo_izq: Union[str, Path],
    ruta_logo_der: Union[str, Path],
    ancho_total_cm: float = 15.5,
):
    """Compone la banda institucional superior como una sola tabla de tres celdas.

    Geometría OpenXML
    -----------------
    El ancho total por omisión es de 15.5 cm (8788 dxa a razón de 567 dxa por
    centímetro) y se reparte en tres columnas: 2.4 cm (1361 dxa) para el
    logotipo izquierdo, 10.7 cm (6066 dxa) para el bloque de texto y 2.4 cm
    (1361 dxa) para el logotipo derecho. La fila única lleva altura fija exacta
    de 2.2 cm (``<w:trHeight w:val="1247" w:hRule="exact"/>``) y las tres celdas
    se alinean al centro con ``<w:vAlign w:val="center"/>``. Ninguna celda lleva
    bordes ni sombreado.

    Ambos logotipos se insertan con la misma altura final de 1.9 cm; el ancho se
    deduce de la relación de aspecto nativa del archivo, de modo que la imagen no
    se deforma. El bloque central escribe tres líneas centradas de 9.5 pt. La
    tabla se ancla al inicio del cuerpo, no lleva ``<w:tblHeader/>`` y, por ser
    contenido del cuerpo, no se repite en las páginas siguientes.

    Devuelve la tabla nativa creada (``docx.table.Table``).
    """
    from docx.enum.table import (WD_CELL_VERTICAL_ALIGNMENT,
                                 WD_ROW_HEIGHT_RULE, WD_TABLE_ALIGNMENT)
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt

    ruta_izq = Path(ruta_logo_izq)
    ruta_der = Path(ruta_logo_der)
    for ruta in (ruta_izq, ruta_der):
        if not ruta.exists():
            raise FileNotFoundError(f"Logotipo ausente: {ruta}")

    dxa_cm = 567.0
    total_dxa = int(round(float(ancho_total_cm) * dxa_cm))
    ancho_logo_dxa = int(round(2.4 * dxa_cm))
    ancho_texto_dxa = total_dxa - 2 * ancho_logo_dxa
    if ancho_texto_dxa <= 0:
        raise ValueError("El ancho total no admite dos celdas de 2.4 cm.")
    anchos = [ancho_logo_dxa, ancho_texto_dxa, ancho_logo_dxa]

    tabla = documento.add_table(rows=1, cols=3)
    tabla.style = None
    tabla.alignment = WD_TABLE_ALIGNMENT.LEFT
    tabla.autofit = False
    _fijar_margenes_celda_tabla(tabla._tbl, 0, 0, 0, 0)

    tbl = tabla._tbl
    tblPr = tbl.tblPr

    # Ancho total explícito en dxa.
    previo = tblPr.find(qn("w:tblW"))
    if previo is not None:
        tblPr.remove(previo)
    tblW = OxmlElement("w:tblW")
    tblW.set(qn("w:type"), "dxa")
    tblW.set(qn("w:w"), str(sum(anchos)))
    tblPr.insert_element_before(
        tblW, "w:jc", "w:tblCellSpacing", "w:tblInd", "w:tblBorders",
        "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook",
    )

    # Rejilla y anchos de celda idénticos a la rejilla.
    for gc, ancho in zip(tbl.tblGrid.gridCol_lst, anchos):
        gc.set(qn("w:w"), str(ancho))
    for indice, ancho in enumerate(anchos):
        tcPr = tabla.rows[0].cells[indice]._tc.get_or_add_tcPr()
        tcW = tcPr.get_or_add_tcW()
        tcW.set(qn("w:type"), "dxa")
        tcW.set(qn("w:w"), str(ancho))

    # Bordes nulos en la tabla y en cada celda; sin sombreado.
    previo = tblPr.find(qn("w:tblBorders"))
    if previo is not None:
        tblPr.remove(previo)
    bordes_tabla = OxmlElement("w:tblBorders")
    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        nodo = OxmlElement(f"w:{lado}")
        nodo.set(qn("w:val"), "nil")
        nodo.set(qn("w:sz"), "0")
        nodo.set(qn("w:space"), "0")
        nodo.set(qn("w:color"), "auto")
        bordes_tabla.append(nodo)
    tblPr.insert_element_before(
        bordes_tabla, "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook",
        "w:tblCaption", "w:tblDescription",
    )
    sombra_tabla = tblPr.find(qn("w:shd"))
    if sombra_tabla is not None:
        tblPr.remove(sombra_tabla)

    for celda in tabla.rows[0].cells:
        tcPr = celda._tc.get_or_add_tcPr()
        previo = tcPr.find(qn("w:tcBorders"))
        if previo is not None:
            tcPr.remove(previo)
        bordes_celda = OxmlElement("w:tcBorders")
        for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
            nodo = OxmlElement(f"w:{lado}")
            nodo.set(qn("w:val"), "nil")
            nodo.set(qn("w:sz"), "0")
            nodo.set(qn("w:space"), "0")
            nodo.set(qn("w:color"), "auto")
            bordes_celda.append(nodo)
        tcPr.insert_element_before(
            bordes_celda, "w:shd", "w:noWrap", "w:tcMar", "w:textDirection",
            "w:tcFitText", "w:vAlign", "w:hideMark", "w:headers",
            "w:cellIns", "w:cellDel", "w:cellMerge", "w:tcPrChange",
        )
        sombra_celda = tcPr.find(qn("w:shd"))
        if sombra_celda is not None:
            tcPr.remove(sombra_celda)
        celda.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

    # Logotipos: misma altura de 1.9 cm; ancho por relación de aspecto nativa.
    for indice, ruta in ((0, ruta_izq), (2, ruta_der)):
        parrafo = tabla.rows[0].cells[indice].paragraphs[0]
        for hijo in list(parrafo._element):
            if hijo.tag != qn("w:pPr"):
                parrafo._element.remove(hijo)
        pf = parrafo.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing = 1.0
        parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        parrafo.add_run().add_picture(str(ruta), height=Cm(1.9))

    # Bloque de texto institucional centrado, tres líneas de 9.5 pt.
    lineas = (
        ("UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS", True),
        ("Facultad de Ingeniería", False),
        ("Escuela Profesional de Ingeniería de Sistemas", False),
    )
    celda_texto = tabla.rows[0].cells[1]
    for posicion, (texto, negrita) in enumerate(lineas):
        parrafo = celda_texto.paragraphs[0] if posicion == 0 else \
            celda_texto.add_paragraph()
        if posicion == 0:
            for hijo in list(parrafo._element):
                if hijo.tag != qn("w:pPr"):
                    parrafo._element.remove(hijo)
        pf = parrafo.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing = 1.0
        parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = parrafo.add_run(texto)
        run.bold = negrita
        run.font.size = Pt(9.5)
        rPr = run._r.get_or_add_rPr()
        rFonts = rPr.find(qn("w:rFonts"))
        if rFonts is None:
            rFonts = OxmlElement("w:rFonts")
            rPr.insert(0, rFonts)
        for atributo in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rFonts.set(qn(atributo), "Times New Roman")

    # Altura exacta de fila y ausencia de repetición de encabezado.
    fila = tabla.rows[0]
    fila.height = Cm(2.2)
    fila.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
    _preparar_tr(fila._tr, cant_split=True, tbl_header=False)
    eliminar_flotacion_tabla(tabla)

    # Anclaje al inicio del cuerpo.
    cuerpo = documento.element.body
    cuerpo.remove(tbl)
    cuerpo.insert(0, tbl)
    return tabla


def _qn(tag: str):
    from docx.oxml.ns import qn

    return qn(tag)


_ALINEACIONES = ("left", "center", "right", "both", "justify")


def _fijar_alineacion_celda(tc, alineacion: str) -> None:
    """Fija <w:jc> en todos los párrafos de la celda respetando el orden de CT_PPr."""
    from docx.oxml import OxmlElement

    if alineacion not in _ALINEACIONES:
        raise ValueError(f"Alineación no válida: {alineacion}")
    for p in tc.findall(_qn("w:p")):
        pPr = p.find(_qn("w:pPr"))
        if pPr is None:
            from docx.oxml import OxmlElement as _OE

            pPr = _OE("w:pPr")
            p.insert(0, pPr)
        jc = pPr.find(_qn("w:jc"))
        if jc is None:
            jc = OxmlElement("w:jc")
            pPr.append(jc)
        jc.set(_qn("w:val"), "both" if alineacion == "justify" else alineacion)


def _fijar_texto_celda(tc, texto: str, alineacion: Optional[str] = None) -> None:
    """Reescribe el texto de una celda conservando el <w:rPr> del primer run."""
    from docx.oxml import OxmlElement

    p = tc.find(_qn("w:p"))
    if p is None:
        p = OxmlElement("w:p")
        tc.append(p)
    runs = p.findall(_qn("w:r"))
    for extra in p.findall(_qn("w:r"))[1:]:
        p.remove(extra)
    if runs:
        run = runs[0]
        for t in run.findall(_qn("w:t"))[1:]:
            run.remove(t)
        t = run.find(_qn("w:t"))
        if t is None:
            t = OxmlElement("w:t")
            run.append(t)
    else:
        run = OxmlElement("w:r")
        t = OxmlElement("w:t")
        run.append(t)
        p.append(run)
    t.text = texto
    if texto != texto.strip() or "  " in texto:
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    if alineacion:
        _fijar_alineacion_celda(tc, alineacion)


def _preparar_tr(tr, cant_split: bool = True, tbl_header: bool = False) -> None:
    """Garantiza <w:cantSplit/> y <w:tblHeader/> en el orden correcto de <w:trPr>."""
    from docx.oxml import OxmlElement

    trPr = tr.find(_qn("w:trPr"))
    if trPr is None:
        trPr = OxmlElement("w:trPr")
        tr.insert(0, trPr)
    cs = trPr.find(_qn("w:cantSplit"))
    if cant_split and cs is None:
        cs = OxmlElement("w:cantSplit")
        trPr.insert(0, cs)
    elif not cant_split and cs is not None:
        trPr.remove(cs)
    th = trPr.find(_qn("w:tblHeader"))
    if tbl_header and th is None:
        th = OxmlElement("w:tblHeader")
        cs_node = trPr.find(_qn("w:cantSplit"))
        trPr.insert(trPr.index(cs_node) + 1 if cs_node is not None else 0, th)
    elif not tbl_header and th is not None:
        trPr.remove(th)


_ORDEN_CELLMAR = ("w:top", "w:left", "w:bottom", "w:right")
_ORDEN_TBLPR_ANTES_CELLMAR = (
    "w:tblLayout",
    "w:shd",
    "w:tblBorders",
    "w:tblInd",
    "w:tblCellSpacing",
    "w:jc",
    "w:tblW",
    "w:tblStyle",
)


def _fijar_margenes_celda_tabla(
    tbl,
    izquierdo_dxa: int = 57,
    derecho_dxa: int = 57,
    superior_dxa: Optional[int] = None,
    inferior_dxa: Optional[int] = None,
) -> None:
    """Fija los márgenes de celda de toda la tabla mediante <w:tblCellMar>.

    Los márgenes superior e inferior solo se modifican cuando se especifican,
    de modo que las llamadas laterales previas conservan su comportamiento.
    """
    from docx.oxml import OxmlElement

    pr = tbl.find(_qn("w:tblPr"))
    if pr is None:
        pr = OxmlElement("w:tblPr")
        tbl.insert(0, pr)
    mar = pr.find(_qn("w:tblCellMar"))
    if mar is None:
        mar = OxmlElement("w:tblCellMar")
        ancla = None
        for etiqueta in _ORDEN_TBLPR_ANTES_CELLMAR:
            ancla = pr.find(_qn(etiqueta))
            if ancla is not None:
                break
        if ancla is not None:
            ancla.addnext(mar)
        else:
            pr.append(mar)
    ajustes = [
        ("w:left", izquierdo_dxa),
        ("w:right", derecho_dxa),
    ]
    if superior_dxa is not None:
        ajustes.append(("w:top", superior_dxa))
    if inferior_dxa is not None:
        ajustes.append(("w:bottom", inferior_dxa))
    for etiqueta, valor in ajustes:
        nodo = mar.find(_qn(etiqueta))
        if nodo is None:
            nodo = OxmlElement(etiqueta)
            orden = _ORDEN_CELLMAR.index(etiqueta)
            insertado = False
            for hijo in list(mar):
                nombre = "w:" + hijo.tag.split("}")[1]
                if nombre in _ORDEN_CELLMAR and _ORDEN_CELLMAR.index(nombre) > orden:
                    hijo.addprevious(nodo)
                    insertado = True
                    break
            if not insertado:
                mar.append(nodo)
        nodo.set(_qn("w:w"), str(int(valor)))
        nodo.set(_qn("w:type"), "dxa")


def _fijar_tamano_run(run, medios_puntos: int) -> bool:
    """Fija <w:sz>/<w:szCs> de un run respetando el orden de CT_RPr. Devuelve si cambió."""
    tamano = int(medios_puntos)
    rPr = run.find(_qn("w:rPr"))
    if rPr is None:
        from docx.oxml import OxmlElement

        rPr = OxmlElement("w:rPr")
        run.insert(0, rPr)
    cambio = False
    for etiqueta in ("w:sz", "w:szCs"):
        nodo = rPr.find(_qn(etiqueta))
        if nodo is None:
            _rpr_propiedad(rPr, etiqueta.split(":")[1], True)
            nodo = rPr.find(_qn(etiqueta))
        if nodo.get(_qn("w:val")) != str(tamano):
            nodo.set(_qn("w:val"), str(tamano))
            cambio = True
    return cambio


def _ancho_texto_dxa(
    texto: str,
    tamano_pt: float,
    archivo_fuente: Optional[str] = None,
    negrita: bool = False,
) -> Optional[float]:
    """Mide el ancho de avance de un texto en dxa con las métricas reales de la fuente."""
    import os

    try:
        from PIL import ImageFont
    except ImportError:  # pragma: no cover - Pillow es dependencia del proyecto
        return None
    if archivo_fuente is None:
        archivo_fuente = "timesbd.ttf" if negrita else "times.ttf"
    ruta = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / archivo_fuente
    if not ruta.exists():
        return None
    fuente = ImageFont.truetype(str(ruta), 1000)
    return float(fuente.getlength(texto)) / 1000.0 * float(tamano_pt) * 20.0


def _fijar_margenes_celda(tc, izquierdo_dxa: int, derecho_dxa: int) -> None:
    """Fija <w:tcMar> laterales de una celda respetando el orden de CT_TcPr."""
    from docx.oxml import OxmlElement

    orden = ("w:top", "w:left", "w:bottom", "w:right")
    tcPr = tc.find(_qn("w:tcPr"))
    if tcPr is None:
        tcPr = OxmlElement("w:tcPr")
        tc.insert(0, tcPr)
    mar = tcPr.find(_qn("w:tcMar"))
    if mar is None:
        mar = OxmlElement("w:tcMar")
        posteriores = ("w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark")
        ancla = None
        for hijo in list(tcPr):
            if "w:" + hijo.tag.split("}")[1] in posteriores:
                ancla = hijo
                break
        if ancla is not None:
            ancla.addprevious(mar)
        else:
            tcPr.append(mar)
    for etiqueta, valor in (("w:left", izquierdo_dxa), ("w:right", derecho_dxa)):
        nodo = mar.find(_qn(etiqueta))
        if nodo is None:
            nodo = OxmlElement(etiqueta)
            posicion = orden.index(etiqueta)
            insertado = False
            for hijo in list(mar):
                nombre = "w:" + hijo.tag.split("}")[1]
                if nombre in orden and orden.index(nombre) > posicion:
                    hijo.addprevious(nodo)
                    insertado = True
                    break
            if not insertado:
                mar.append(nodo)
        nodo.set(_qn("w:w"), str(int(valor)))
        nodo.set(_qn("w:type"), "dxa")


def _margenes_actuales(tbl):
    """Devuelve los márgenes laterales efectivos máximos de la tabla (dxa)."""
    izquierdo = derecho = None
    tblPr = tbl.find(_qn("w:tblPr"))
    mar = tblPr.find(_qn("w:tblCellMar")) if tblPr is not None else None
    if mar is not None:
        for etiqueta in ("w:left", "w:right"):
            nodo = mar.find(_qn(etiqueta))
            if nodo is not None and nodo.get(_qn("w:w")):
                if etiqueta == "w:left":
                    izquierdo = int(nodo.get(_qn("w:w")))
                else:
                    derecho = int(nodo.get(_qn("w:w")))
    izquierdo = izquierdo if izquierdo is not None else 108
    derecho = derecho if derecho is not None else 108
    for tr in tbl.findall(_qn("w:tr")):
        for tc in tr.findall(_qn("w:tc")):
            tcPr = tc.find(_qn("w:tcPr"))
            if tcPr is None:
                continue
            tcMar = tcPr.find(_qn("w:tcMar"))
            if tcMar is None:
                continue
            for etiqueta in ("w:left", "w:right"):
                nodo = tcMar.find(_qn(etiqueta))
                if nodo is not None and nodo.get(_qn("w:w")):
                    valor = int(nodo.get(_qn("w:w")))
                    if etiqueta == "w:left":
                        izquierdo = max(izquierdo, valor)
                    else:
                        derecho = max(derecho, valor)
    return izquierdo, derecho


def _tamano_parrafo(parrafo) -> float:
    for run in parrafo.iter(_qn("w:r")):
        rPr = run.find(_qn("w:rPr"))
        if rPr is not None:
            sz = rPr.find(_qn("w:sz"))
            if sz is not None and sz.get(_qn("w:val")):
                return int(sz.get(_qn("w:val"))) / 2.0
    return 11.0


def _parrafo_negrita(parrafo) -> bool:
    """Indica si el texto del párrafo se imprime en negrita (métrica distinta a redonda)."""
    for run in parrafo.iter(_qn("w:r")):
        if not "".join(t.text or "" for t in run.iter(_qn("w:t"))).strip():
            continue
        rPr = run.find(_qn("w:rPr"))
        if rPr is None:
            return False
        b = rPr.find(_qn("w:b"))
        if b is None:
            return False
        if b.get(_qn("w:val")) in ("0", "false", "off"):
            return False
        return True
    return False


_PATRON_RANGO = re.compile(
    r"[+\-−]?\s*\d+(?:[.,]\d+)?\s*[–—−-]\s*[+\-−]?\s*\d+(?:[.,]\d+)?"
)


def _segmentos_indivisibles(texto: str) -> List[str]:
    """Divide un token en los segmentos donde Word puede cortar (guion).

    Los rangos «N – M» (guion medio, raya o guion simple) se conservan como una
    unidad indivisible: no se permite el corte dentro del rango. El resto de
    palabras se sigue partiendo tras el guion simple, como antes.
    """
    segmentos: List[str] = []
    ultimo = 0
    for rango in _PATRON_RANGO.finditer(texto):
        for palabra in texto[ultimo : rango.start()].split():
            for parte in re.split(r"(?<=-)", palabra):
                if parte:
                    segmentos.append(parte)
        segmentos.append(rango.group(0))
        ultimo = rango.end()
    for palabra in texto[ultimo:].split():
        for parte in re.split(r"(?<=-)", palabra):
            if parte:
                segmentos.append(parte)
    return segmentos


def _tokens_columna(trs, columna: int, tamano_pt: Optional[float], centrada: bool):
    """Tokens indivisibles medidos con el tamaño y el peso reales de cada run."""
    tokens = []
    for posicion, tr in enumerate(trs):
        celdas = tr.findall(_qn("w:tc"))
        if columna >= len(celdas):
            continue
        for parrafo in celdas[columna].iter(_qn("w:p")):
            tamano_parrafo = _tamano_parrafo(parrafo)
            for run in parrafo.iter(_qn("w:r")):
                texto = "".join(t.text or "" for t in run.iter(_qn("w:t")))
                if not texto.strip():
                    continue
                rPr = run.find(_qn("w:rPr"))
                tamano = tamano_parrafo
                negrita = False
                if rPr is not None:
                    sz = rPr.find(_qn("w:sz"))
                    if sz is not None and sz.get(_qn("w:val")):
                        try:
                            tamano = int(sz.get(_qn("w:val"))) / 2.0
                        except ValueError:
                            tamano = tamano_parrafo
                    b = rPr.find(_qn("w:b"))
                    negrita = b is not None and b.get(_qn("w:val")) not in ("0", "false", "off")
                if tamano_pt is not None and (posicion == 0 or centrada) and tamano is None:
                    tamano = tamano_pt
                for segmento in _segmentos_indivisibles(texto):
                    tokens.append((segmento, tamano if tamano else 10.0, negrita))
    return tokens


def _medir_columnas(trs, grid, margenes_dxa: int, tamano_pt: float, columnas_centradas):
    """Ancho mínimo requerido por columna y verificación del token más largo."""
    mediciones = []
    for columna, ancho in enumerate(grid):
        centrada = columna in columnas_centradas
        tokens = _tokens_columna(trs, columna, tamano_pt, centrada)
        medidas = [(t, tam, _ancho_texto_dxa(t, tam, negrita=n)) for t, tam, n in tokens]
        medidas = [m for m in medidas if m[2] is not None]
        util = ancho - 2 * margenes_dxa
        if medidas:
            token, tam, ancho_glifo = max(medidas, key=lambda m: m[2])
        else:
            token, tam, ancho_glifo = "", None, 0.0
        mediciones.append(
            {
                "columna": columna,
                "ancho_dxa": ancho,
                "ancho_util_dxa": util,
                "token_mas_largo": token,
                "tamano_token_pt": tam,
                "ancho_token_dxa": round(ancho_glifo, 1),
                "requerido_dxa": int(round(ancho_glifo)) + 2 * margenes_dxa + 8,
                "cabe": ancho_glifo <= util,
            }
        )
    return mediciones


def _rebalancear_columnas(tbl, grid, mediciones, relleno_dxa: int = 8):
    """Redistribuye anchos conservando el total: cubre déficits con excedentes."""
    requeridos = [max(m["requerido_dxa"] + max(0, relleno_dxa - 8), 240) for m in mediciones]
    total = sum(grid)
    if sum(requeridos) > total:
        return {"aplicado": False, "motivo": "Los requerimientos exceden el ancho total de la tabla", "anchos_nuevos": grid}
    deficits = [max(0, requeridos[i] - grid[i]) for i in range(len(grid))]
    if not any(deficits):
        return {"aplicado": False, "motivo": "Ninguna columna requiere ensanche", "anchos_nuevos": grid}
    excedentes = [max(0, grid[i] - requeridos[i]) for i in range(len(grid))]
    nuevos = list(grid)
    pendiente = sum(deficits)
    tomado = [0] * len(grid)
    for i in sorted(range(len(grid)), key=lambda j: (-excedentes[j], j)):
        if pendiente <= 0:
            break
        tomar = min(excedentes[i], pendiente)
        nuevos[i] -= tomar
        tomado[i] = tomar
        pendiente -= tomar
    if pendiente > 0:
        return {"aplicado": False, "motivo": "No hay excedente suficiente para cubrir los déficits", "anchos_nuevos": grid}
    for i in range(len(grid)):
        nuevos[i] += deficits[i]
    if sum(nuevos) != total:  # ajuste de redondeo
        nuevos[-1] += total - sum(nuevos)

    for col, ancho in zip(tbl.find(_qn("w:tblGrid")).findall(_qn("w:gridCol")), nuevos):
        col.set(_qn("w:w"), str(ancho))
    for tr in tbl.findall(_qn("w:tr")):
        for columna, tc in enumerate(tr.findall(_qn("w:tc"))):
            if columna >= len(nuevos):
                continue
            tcPr = tc.find(_qn("w:tcPr"))
            if tcPr is None:
                continue
            tcW = tcPr.find(_qn("w:tcW"))
            if tcW is None:
                continue
            tcW.set(_qn("w:w"), str(nuevos[columna]))
            tcW.set(_qn("w:type"), "dxa")
    return {
        "aplicado": True,
        "anchos_anteriores": grid,
        "anchos_nuevos": nuevos,
        "ensanchadas": [i for i in range(len(grid)) if deficits[i] > 0],
        "donantes": [i for i in range(len(grid)) if tomado[i] > 0],
    }


def ajustar_matriz_anexo(
    documento,
    indices_tabla: Sequence[int],
    margenes_dxa: int = 57,
    tamano_pt: float = 8.0,
    columnas_centradas: Optional[Sequence[int]] = None,
    aplicar_margenes: bool = True,
    rebalancear: bool = True,
) -> Dict[str, Any]:
    """
    Ajusta las matrices de datos de anexos (18 columnas) por geometría y no por texto:
    márgenes laterales de celda, 8 pt en cabecera y celdas numéricas, encabezado
    repetido, filas no fragmentables y columnas de ítems/puntajes centradas.
    Si un token indivisible excede el ancho útil, redistribuye los anchos columnales
    conservando el ancho total de la tabla. ``aplicar_margenes=False`` conserva los
    márgenes vigentes y deja el desborde exclusivamente al rebalanceo.

    Devuelve, por tabla, el ancho de columna, el ancho útil y la verificación del
    glifo más largo contra ese ancho útil.
    """
    acciones: List[Dict[str, Any]] = []
    detalle_tablas: List[Dict[str, Any]] = []
    tablas = documento.tables
    for indice in indices_tabla:
        if not 0 <= indice < len(tablas):
            raise IndexError(f"Índice de tabla {indice} fuera de rango (0..{len(tablas) - 1})")
        table = tablas[indice]
        tbl = table._tbl
        trs = tbl.findall(_qn("w:tr"))
        grid = [int(g.get(_qn("w:w"))) for g in tbl.find(_qn("w:tblGrid")).findall(_qn("w:gridCol"))]
        columnas = list(columnas_centradas) if columnas_centradas is not None else list(range(2, len(grid)))

        if aplicar_margenes:
            _fijar_margenes_celda_tabla(tbl, margenes_dxa, margenes_dxa)
        for posicion, tr in enumerate(trs):
            _preparar_tr(tr, cant_split=True, tbl_header=(posicion == 0))
            for columna, tc in enumerate(tr.findall(_qn("w:tc"))):
                if aplicar_margenes:
                    _fijar_margenes_celda(tc, margenes_dxa, margenes_dxa)
                if columna in columnas:
                    _fijar_alineacion_celda(tc, "center")
                if posicion == 0 or columna in columnas:
                    for run in tc.iter(_qn("w:r")):
                        if not "".join(t.text or "" for t in run.iter(_qn("w:t"))).strip():
                            continue
                        _fijar_tamano_run(run, int(round(tamano_pt * 2)))

        margen_izq, margen_der = _margenes_actuales(tbl)
        margenes_medicion = max(margen_izq, margen_der)
        medicion = _medir_columnas(trs, grid, margenes_medicion, tamano_pt, columnas)
        rebalanceo = (
            _rebalancear_columnas(tbl, grid, medicion, relleno_dxa=90)
            if rebalancear
            else {"aplicado": False, "motivo": "Rebalanceo desactivado por parametro", "anchos_nuevos": grid}
        )
        if rebalanceo["aplicado"]:
            grid = rebalanceo["anchos_nuevos"]
            medicion = _medir_columnas(trs, grid, margenes_medicion, tamano_pt, columnas)

        columnas_desbordadas = [m["columna"] for m in medicion if not m["cabe"]]
        detalle_tablas.append(
            {
                "indice_tabla": indice,
                "columnas": len(grid),
                "filas": len(trs),
                "ancho_tabla_dxa": sum(grid),
                "margenes_laterales_dxa": margenes_medicion,
                "via_geometria": "margenes+rebalanceo" if (aplicar_margenes and rebalancear) else ("margenes" if aplicar_margenes else "rebalanceo"),
                "tamano_pt": tamano_pt,
                "columnas_centradas": len(columnas),
                "rebalanceo": rebalanceo,
                "verificacion_glifos": medicion,
                "columnas_desbordadas": columnas_desbordadas,
                "cabe_sin_desborde": not columnas_desbordadas,
            }
        )
        acciones.append(
            {
                "categoria": "matriz_anexo_geometria",
                "tabla": indice,
                "estado": "corregido" if not columnas_desbordadas else "parcial",
                "detalle": (
                    (
                        f"margenes laterales de celda fijados en {margenes_dxa} dxa; "
                        if aplicar_margenes
                        else f"margenes laterales vigentes conservados ({margenes_medicion} dxa); "
                    )
                    + f"cabecera y celdas numericas a {tamano_pt} pt; {len(columnas)} columnas "
                    f"centradas; tblHeader y cantSplit; rebalanceo="
                    f"{'si' if rebalanceo['aplicado'] else 'no'}; via={detalle_tablas[-1]['via_geometria']}"
                ),
            }
        )
    return {"acciones": acciones, "tablas": detalle_tablas}


def normalizar_tamano_minimo_tabla(
    documento,
    indices_tabla: Sequence[int],
    minimo_pt: float = 10.0,
) -> Dict[str, Any]:
    """Eleva a un mínimo tipográfico el tamaño de todos los runs de una tabla."""
    minimo = int(round(minimo_pt * 2))
    acciones: List[Dict[str, Any]] = []
    for indice in indices_tabla:
        tabla = documento.tables[indice]
        ajustados = 0
        for run in tabla._tbl.iter(_qn("w:r")):
            if not "".join(t.text or "" for t in run.iter(_qn("w:t"))).strip():
                continue
            rPr = run.find(_qn("w:rPr"))
            if rPr is None:
                from docx.oxml import OxmlElement

                rPr = OxmlElement("w:rPr")
                run.insert(0, rPr)
            cambiado = False
            for etiqueta in ("w:sz", "w:szCs"):
                sz = rPr.find(_qn(etiqueta))
                if sz is None:
                    from docx.oxml import OxmlElement

                    sz = OxmlElement(etiqueta)
                    rPr.insert_element_before(
                        sz,
                        "w:u",
                        "w:effect",
                        "w:bdr",
                        "w:shd",
                        "w:fitText",
                        "w:vertAlign",
                        "w:rtl",
                        "w:cs",
                        "w:em",
                        "w:lang",
                        "w:eastAsianLayout",
                        "w:specVanish",
                        "w:oMath",
                    )
                    sz.set(_qn("w:val"), str(minimo))
                    cambiado = True
                else:
                    try:
                        if int(sz.get(_qn("w:val"))) < minimo:
                            sz.set(_qn("w:val"), str(minimo))
                            cambiado = True
                    except (TypeError, ValueError):
                        sz.set(_qn("w:val"), str(minimo))
                        cambiado = True
            if cambiado:
                ajustados += 1
        acciones.append({"tabla": indice, "runs_ajustados": ajustados, "minimo_pt": minimo_pt})
    return {"acciones": acciones}


def rebalancear_tabla(
    documento,
    indices_tabla: Sequence[int],
    relleno_dxa: int = 8,
) -> Dict[str, Any]:
    """
    Rebalanceo geométrico genérico: mide el token indivisible más largo de cada
    columna con el tamaño tipográfico real y redistribuye anchos conservando el
    ancho total de la tabla. No altera texto, márgenes ni tamaños de fuente.
    """
    acciones: List[Dict[str, Any]] = []
    detalle_tablas: List[Dict[str, Any]] = []
    tablas = documento.tables
    for indice in indices_tabla:
        if not 0 <= indice < len(tablas):
            raise IndexError(f"Índice de tabla {indice} fuera de rango (0..{len(tablas) - 1})")
        tbl = tablas[indice]._tbl
        trs = tbl.findall(_qn("w:tr"))
        grid = [int(g.get(_qn("w:w"))) for g in tbl.find(_qn("w:tblGrid")).findall(_qn("w:gridCol"))]
        margen_izq, margen_der = _margenes_actuales(tbl)
        margenes = max(margen_izq, margen_der)
        antes = _medir_columnas(trs, grid, margenes, None, ())
        rebalanceo = _rebalancear_columnas(tbl, grid, antes, relleno_dxa=relleno_dxa)
        if rebalanceo["aplicado"]:
            grid = rebalanceo["anchos_nuevos"]
        despues = _medir_columnas(trs, grid, margenes, None, ())
        desbordadas = [m["columna"] for m in despues if not m["cabe"]]
        detalle_tablas.append(
            {
                "indice_tabla": indice,
                "columnas": len(grid),
                "filas": len(trs),
                "ancho_tabla_dxa": sum(grid),
                "margenes_laterales_dxa": margenes,
                "via_geometria": "rebalanceo",
                "rebalanceo": rebalanceo,
                "verificacion_glifos": despues,
                "columnas_desbordadas": desbordadas,
                "cabe_sin_desborde": not desbordadas,
            }
        )
        acciones.append(
            {
                "categoria": "tabla_rebalanceo",
                "tabla": indice,
                "estado": "corregido" if not desbordadas else "parcial",
                "detalle": (
                    f"rebalanceo={'si' if rebalanceo['aplicado'] else 'no'}; "
                    f"anchos {rebalanceo.get('anchos_anteriores', grid)} -> {grid}"
                ),
            }
        )
    return {"acciones": acciones, "tablas": detalle_tablas}


def actualizar_nota_tabla(table, texto: str, tamano_pt: float = 9.5) -> bool:
    """
    Actualiza la nota inmediatamente posterior a la tabla conservando el prefijo
    «Nota.» en cursiva (TNR 9.5-10 pt, interlineado sencillo).
    """
    from docx.oxml import OxmlElement

    tbl = table._tbl
    hermana = tbl.getnext()
    if hermana is None or not hermana.tag.endswith("}p"):
        return False
    texto_actual = "".join(t.text or "" for t in hermana.iter(_qn("w:t")))
    if not texto_actual.lstrip().startswith("Nota."):
        return False

    runs = hermana.findall(_qn("w:r"))
    if not runs:
        return False
    prefijo = runs[0]
    for extra in runs[1:]:
        hermana.remove(extra)
    cuerpo = OxmlElement("w:r")
    rPr_ref = prefijo.find(_qn("w:rPr"))
    if rPr_ref is not None:
        from copy import deepcopy

        cuerpo.append(deepcopy(rPr_ref))
        i = cuerpo.find(_qn("w:rPr")).find(_qn("w:i"))
        if i is not None:
            cuerpo.find(_qn("w:rPr")).remove(i)
    t = OxmlElement("w:t")
    t.text = texto
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    cuerpo.append(t)
    hermana.append(cuerpo)

    pPr = hermana.find(_qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        hermana.insert(0, pPr)
    sp = pPr.find(_qn("w:spacing"))
    if sp is None:
        sp = OxmlElement("w:spacing")
        pPr.insert(0, sp)
    sp.set(_qn("w:line"), "240")
    sp.set(_qn("w:lineRule"), "auto")
    return True


_ORDEN_RPR = (
    "rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike", "dstrike",
    "outline", "shadow", "emboss", "imprint", "noProof", "snapToGrid", "vanish", "webHidden",
    "color", "spacing", "w", "kern", "position", "sz", "szCs", "highlight", "u", "effect",
    "bdr", "shd", "fitText", "vertAlign", "rtl", "cs", "em", "lang", "eastAsianLayout",
    "specVanish", "oMath",
)


def _rpr_propiedad(rPr, etiqueta: str, activa: bool = True):
    """Activa o elimina una propiedad de <w:rPr> respetando el orden del esquema CT_RPr."""
    from docx.oxml import OxmlElement

    actual = rPr.find(_qn(f"w:{etiqueta}"))
    if not activa:
        if actual is not None:
            rPr.remove(actual)
        return None
    if actual is not None:
        return actual
    nuevo = OxmlElement(f"w:{etiqueta}")
    if etiqueta not in _ORDEN_RPR:
        rPr.append(nuevo)
        return nuevo
    limite = _ORDEN_RPR.index(etiqueta)
    for hijo in rPr:
        nombre = hijo.tag.split("}")[-1]
        if nombre in _ORDEN_RPR and _ORDEN_RPR.index(nombre) > limite:
            hijo.addprevious(nuevo)
            return nuevo
    rPr.append(nuevo)
    return nuevo


def _texto_parrafo(p) -> str:
    """Texto de un <w:p> uniendo solo los <w:t> (evita la triple lectura de python-docx)."""
    return "".join(t.text or "" for t in p.iter(_qn("w:t")))


def _parrafo_con_imagen(p) -> bool:
    return p is not None and p.tag == _qn("w:p") and p.find(".//" + _qn("w:drawing")) is not None


def _es_rotulo(p) -> bool:
    import re as _re

    if p is None or p.tag != _qn("w:p"):
        return False
    pPr = p.find(_qn("w:pPr"))
    if pPr is not None:
        if pPr.find(_qn("w:outlineLvl")) is not None:
            return False
        pStyle = pPr.find(_qn("w:pStyle"))
        if pStyle is not None and pStyle.get(_qn("w:val")) == "Tabladeilustraciones":
            return False
    return bool(_re.match(r"^(Figura|Tabla)\s+\d+", _texto_parrafo(p).strip()))


def reordenar_figuras_apa7(documento, desde: int = 11, hasta: int = 48) -> List[Dict[str, Any]]:
    """
    Coloca la imagen entre el rótulo y la nota (orden APA 7) en las figuras indicadas.
    Mueve el párrafo con el <w:drawing> sin duplicarlo ni eliminarlo.
    """
    import re as _re

    cuerpo = documento.element.body
    acciones: List[Dict[str, Any]] = []
    for indice, elemento in enumerate(list(cuerpo)):
        if not _es_rotulo(elemento):
            continue
        coincidencia = _re.match(r"^Figura\s+(\d+)", _texto_parrafo(elemento).strip())
        if not coincidencia:
            continue
        numero = int(coincidencia.group(1))
        if not desde <= numero <= hasta:
            continue
        previo = elemento.getprevious()
        if not _parrafo_con_imagen(previo):
            continue
        elemento.addnext(previo)
        acciones.append(
            {
                "categoria": "orden_figura_rotulo",
                "parrafo": indice,
                "figura": numero,
                "estado": "corregido",
                "detalle": "imagen movida delante del rótulo al espacio entre rótulo y nota",
            }
        )
    return acciones


def normalizar_rotulos_ilustracion(
    documento,
    estilo: str = "Rotulodeilustracion",
    figuras_excluidas: Sequence[int] = (49, 50, 51, 52),
) -> List[Dict[str, Any]]:
    """
    Aplica el estilo institucional de rótulo y fija la etiqueta y el número en negrita
    y el título descriptivo en cursiva, sin sangría.
    """
    import re as _re

    from docx.enum.style import WD_STYLE_TYPE
    from docx.oxml import OxmlElement

    estilos = documento.styles
    existentes = {s.name: s for s in estilos}
    if "Rotulo de ilustracion" in existentes:
        estilo_objeto = existentes["Rotulo de ilustracion"]
    else:
        estilo_objeto = estilos.add_style("Rotulo de ilustracion", WD_STYLE_TYPE.PARAGRAPH)
        estilo_objeto.base_style = estilos["Normal"]
        estilo_objeto.quick_style = True
        pPr = estilo_objeto.element.get_or_add_pPr()
        keep = OxmlElement("w:keepNext")
        pPr.append(keep)
        ind = OxmlElement("w:ind")
        ind.set(_qn("w:firstLine"), "0")
        ind.set(_qn("w:left"), "0")
        pPr.append(ind)
        rPr = estilo_objeto.element.get_or_add_rPr()
        fuentes = OxmlElement("w:rFonts")
        for atributo in ("w:ascii", "w:hAnsi", "w:cs"):
            fuentes.set(_qn(atributo), "Times New Roman")
        rPr.append(fuentes)

    acciones: List[Dict[str, Any]] = []
    for indice, elemento in enumerate(list(documento.element.body)):
        if not _es_rotulo(elemento):
            continue
        texto = _texto_parrafo(elemento).strip()
        coincidencia = _re.match(r"^(Figura|Tabla)\s+(\d+)", texto)
        if not coincidencia:
            continue
        tipo, numero = coincidencia.group(1), int(coincidencia.group(2))
        if tipo == "Figura" and numero in set(figuras_excluidas):
            continue

        runs = elemento.findall(_qn("w:r"))
        fin_campo = None
        for pos, run in enumerate(runs):
            fld = run.find(_qn("w:fldChar"))
            if fld is not None and fld.get(_qn("w:fldCharType")) == "end":
                fin_campo = pos
        if fin_campo is None:
            continue
        etiqueta, numero_run, titulo = runs[0], runs[fin_campo - 1], runs[fin_campo + 1:]
        cambios = []

        for run in (etiqueta, numero_run):
            rPr = run.find(_qn("w:rPr"))
            if rPr is None:
                rPr = OxmlElement("w:rPr")
                run.insert(0, rPr)
            if rPr.find(_qn("w:b")) is None:
                _rpr_propiedad(rPr, "b", True)
                cambios.append("negrita")
        for run in titulo:
            if not _texto_parrafo(run).strip() and run.find(_qn("w:t")) is None:
                continue
            rPr = run.find(_qn("w:rPr"))
            if rPr is None:
                rPr = OxmlElement("w:rPr")
                run.insert(0, rPr)
            if rPr.find(_qn("w:i")) is None:
                _rpr_propiedad(rPr, "i", True)
                cambios.append("cursiva")
            if rPr.find(_qn("w:b")) is not None:
                _rpr_propiedad(rPr, "b", False)
                cambios.append("negrita_retirada_titulo")

        parrafo = None
        for p in documento.paragraphs:
            if p._p is elemento:
                parrafo = p
                break
        if parrafo is not None:
            parrafo.style = estilo_objeto
            cambios.append("estilo")

        acciones.append(
            {
                "categoria": "rotulo_formato",
                "parrafo": indice,
                "rotulo": f"{tipo} {numero}",
                "estado": "corregido" if cambios else "sin_cambios",
                "detalle": ", ".join(dict.fromkeys(cambios)),
            }
        )
    return acciones


def insertar_prefijo_notas(documento) -> List[Dict[str, Any]]:
    """
    Antepone «Nota.» en cursiva a las notas de tabla que carecen del prefijo,
    conservando su tamaño (9.5-10 pt) e interlineado sencillo.
    """
    from docx.oxml import OxmlElement

    cuerpo = documento.element.body
    acciones: List[Dict[str, Any]] = []
    indice_tabla = 0
    for elemento in list(cuerpo):
        if elemento.tag != _qn("w:tbl"):
            continue
        indice_tabla += 1
        siguiente = elemento.getnext()
        if siguiente is None or siguiente.tag != _qn("w:p"):
            continue
        texto = _texto_parrafo(siguiente).strip()
        if not texto or texto.startswith("Nota."):
            continue
        tamanos = set()
        for run in siguiente.iter(_qn("w:r")):
            rPr = run.find(_qn("w:rPr"))
            if rPr is not None and rPr.find(_qn("w:sz")) is not None:
                tamanos.add(rPr.find(_qn("w:sz")).get(_qn("w:val")))
        pPr = siguiente.find(_qn("w:pPr"))
        linea = None
        if pPr is not None and pPr.find(_qn("w:spacing")) is not None:
            linea = pPr.find(_qn("w:spacing")).get(_qn("w:line"))
        if not tamanos or not tamanos <= {"19", "20"} or linea != "240":
            continue
        if texto.startswith(("Figura", "Tabla")):
            continue

        prefijo = OxmlElement("w:r")
        rPr = OxmlElement("w:rPr")
        fuentes = OxmlElement("w:rFonts")
        for atributo in ("w:ascii", "w:hAnsi", "w:cs"):
            fuentes.set(_qn(atributo), "Times New Roman")
        rPr.append(fuentes)
        rPr.append(OxmlElement("w:i"))
        sz = OxmlElement("w:sz")
        sz.set(_qn("w:val"), sorted(tamanos)[0])
        rPr.append(sz)
        szcs = OxmlElement("w:szCs")
        szcs.set(_qn("w:val"), sorted(tamanos)[0])
        rPr.append(szcs)
        prefijo.append(rPr)
        t = OxmlElement("w:t")
        t.text = "Nota. "
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        prefijo.append(t)
        if pPr is not None:
            pPr.addnext(prefijo)
        else:
            siguiente.insert(0, prefijo)
        acciones.append(
            {
                "categoria": "nota_sin_prefijo",
                "tabla": indice_tabla,
                "parrafo": list(cuerpo).index(siguiente),
                "estado": "corregido",
                "detalle": "prefijo Nota. en cursiva insertado; texto original intacto",
            }
        )
    return acciones


def _normalizar_referencia(texto: str) -> str:
    """Minúsculas, sin acentos ni puntuación, para comparar y ordenar referencias."""
    import re as _re
    import unicodedata

    descompuesto = unicodedata.normalize("NFKD", texto)
    sin_acentos = "".join(c for c in descompuesto if not unicodedata.combining(c))
    return _re.sub(r"[^a-z0-9]+", " ", sin_acentos.lower()).strip()


def _clave_referencia(texto: str) -> str:
    """Clave autor-año para detectar duplicados bibliográficos."""
    import re as _re

    coincidencia = _re.match(r"^(.{1,90}?)\s*\((\d{4})[a-z]?\)", texto)
    if coincidencia:
        return _normalizar_referencia(coincidencia.group(1)) + "|" + coincidencia.group(2)
    return _normalizar_referencia(texto)[:60]


def _parrafos_referencia(documento):
    """Párrafos de la lista final: sangría francesa de 720 dxa."""
    from docx.text.paragraph import Paragraph

    salida = []
    for p in documento.paragraphs:
        pPr = p._p.find(_qn("w:pPr"))
        ind = pPr.find(_qn("w:ind")) if pPr is not None else None
        if ind is not None and ind.get(_qn("w:hanging")) == "720":
            salida.append(p)
    return salida


def _crear_parrafo_referencia(texto: str):
    """Crea <w:p> con sangría francesa 720/720, interlineado 360, TNR 12 pt y justificado."""
    from docx.oxml import OxmlElement

    p = OxmlElement("w:p")
    pPr = OxmlElement("w:pPr")
    sp = OxmlElement("w:spacing")
    sp.set(_qn("w:before"), "0")
    sp.set(_qn("w:after"), "120")
    sp.set(_qn("w:line"), "360")
    sp.set(_qn("w:lineRule"), "auto")
    pPr.append(sp)
    ind = OxmlElement("w:ind")
    ind.set(_qn("w:left"), "720")
    ind.set(_qn("w:hanging"), "720")
    pPr.append(ind)
    jc = OxmlElement("w:jc")
    jc.set(_qn("w:val"), "both")
    pPr.append(jc)
    p.append(pPr)

    run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    fuentes = OxmlElement("w:rFonts")
    for atributo in ("w:ascii", "w:hAnsi", "w:cs"):
        fuentes.set(_qn(atributo), "Times New Roman")
    rPr.append(fuentes)
    sz = OxmlElement("w:sz")
    sz.set(_qn("w:val"), "24")
    rPr.append(sz)
    szcs = OxmlElement("w:szCs")
    szcs.set(_qn("w:val"), "24")
    rPr.append(szcs)
    run.append(rPr)
    t = OxmlElement("w:t")
    t.text = texto
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    run.append(t)
    p.append(run)
    return p


def _agregar_hipervinculo_referencia(documento, parrafo, url: str) -> None:
    """Añade al final de una referencia un hipervínculo externo nativo, sin tocar el texto previo."""
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    from docx.oxml import OxmlElement

    rid = documento.part.relate_to(url, RT.HYPERLINK, is_external=True)
    enlace = OxmlElement("w:hyperlink")
    enlace.set(_qn("r:id"), rid)
    run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    fuentes = OxmlElement("w:rFonts")
    for atributo in ("w:ascii", "w:hAnsi", "w:cs"):
        fuentes.set(_qn(atributo), "Times New Roman")
    rPr.append(fuentes)
    color = OxmlElement("w:color")
    color.set(_qn("w:val"), "0563C1")
    rPr.append(color)
    u = OxmlElement("w:u")
    u.set(_qn("w:val"), "single")
    rPr.append(u)
    sz = OxmlElement("w:sz")
    sz.set(_qn("w:val"), "24")
    rPr.append(sz)
    szcs = OxmlElement("w:szCs")
    szcs.set(_qn("w:val"), "24")
    rPr.append(szcs)
    run.append(rPr)
    t = OxmlElement("w:t")
    t.text = url
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    run.append(t)
    enlace.append(run)
    parrafo._p.append(enlace)


def insertar_referencias(documento, inserciones: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Inserta referencias completas en la lista final, inmediatamente después de su
    ancla alfabética. Se ejecuta al final de la pasada para no desplazar índices.
    No reescribe ninguna referencia existente.
    """
    from docx.text.paragraph import Paragraph

    acciones: List[Dict[str, Any]] = []
    referencias = _parrafos_referencia(documento)
    claves = {_clave_referencia(p.text.strip()): p.text.strip()[:60] for p in referencias}
    orden_inicial = [_normalizar_referencia(p.text) for p in referencias]
    inversiones_iniciales = [
        (i, orden_inicial[i][:40], orden_inicial[i + 1][:40])
        for i in range(len(orden_inicial) - 1)
        if orden_inicial[i] > orden_inicial[i + 1]
    ]

    parrafos = list(documento.paragraphs)
    anterior = None
    for orden, insercion in enumerate(inserciones, 1):
        texto = insercion["texto"].strip()
        clave = _clave_referencia(texto)
        duplicada = clave in claves
        if insercion.get("encadenada") and anterior is not None:
            ancla = anterior
            criterio = "despues_de_insercion_previa"
        else:
            indice = insercion.get("ancla_indice")
            prefijo = _normalizar_referencia(insercion.get("ancla_texto", ""))
            candidato = parrafos[indice] if isinstance(indice, int) and 0 <= indice < len(parrafos) else None
            if candidato is not None and not _normalizar_referencia(candidato.text).startswith(prefijo):
                candidato = None
            if candidato is None and prefijo:
                candidato = next(
                    (p for p in parrafos if _normalizar_referencia(p.text).startswith(prefijo)),
                    None,
                )
            if candidato is None:
                raise ValueError(f"No se encontro el ancla de la referencia {orden}: {insercion.get('ancla_texto')}")
            ancla = candidato
            criterio = "ancla_alfabetica"

        url = insercion.get("url")
        if url and texto.endswith(url):
            nuevo = _crear_parrafo_referencia(texto[: -len(url)])
        else:
            nuevo = _crear_parrafo_referencia(texto)
        ancla._p.addnext(nuevo)
        anterior = Paragraph(nuevo, ancla._parent)
        if url and texto.endswith(url):
            _agregar_hipervinculo_referencia(documento, anterior, url)
        claves[clave] = texto[:60]
        acciones.append(
            {
                "categoria": "referencia_insertada",
                "orden": orden,
                "ancla": insercion.get("ancla_texto", ""),
                "criterio": criterio,
                "referencia": texto[:90],
                "clave": clave,
                "duplicada": duplicada,
                "estado": "insertada",
            }
        )

    finales = _parrafos_referencia(documento)
    orden_final = [_normalizar_referencia(p.text) for p in finales]
    inversiones_finales = [
        (i, finales[i].text[:45], finales[i + 1].text[:45])
        for i in range(len(finales) - 1)
        if orden_final[i] > orden_final[i + 1]
    ]
    claves_finales = [_clave_referencia(p.text.strip()) for p in finales]
    duplicadas = sorted({c for c in claves_finales if claves_finales.count(c) > 1})
    return {
        "acciones": acciones,
        "entradas_antes": len(referencias),
        "entradas_despues": len(finales),
        "inversiones_antes": inversiones_iniciales,
        "inversiones_despues": inversiones_finales,
        "orden_alfabetico_conservado": not inversiones_finales,
        "claves_duplicadas": duplicadas,
    }


def _reemplazar_texto_parrafo(p, viejo: str, nuevo: str, maximo: Optional[int] = 1) -> int:
    """
    Sustituye un texto dentro de un párrafo conservando el formato de los runs.
    Devuelve el número de sustituciones efectivas.
    """
    if not viejo or viejo == nuevo:
        return 0
    elemento = getattr(p, "_p", p)
    limite = maximo if maximo else 10 ** 6
    aplicadas = 0
    while aplicadas < limite:
        nodos = [t for t in elemento.iter(_qn("w:t"))]
        if not nodos:
            return aplicadas
        offsets = []
        acumulado = 0
        for nodo in nodos:
            texto_nodo = nodo.text or ""
            offsets.append((acumulado, acumulado + len(texto_nodo)))
            acumulado += len(texto_nodo)
        texto = "".join(nodo.text or "" for nodo in nodos)
        posicion = texto.find(viejo)
        if posicion < 0:
            return aplicadas
        fin = posicion + len(viejo)
        afectados = [
            i for i, (inicio, termino) in enumerate(offsets)
            if max(inicio, posicion) < min(termino, fin)
        ]
        if not afectados:
            return aplicadas
        primero, ultimo = afectados[0], afectados[-1]
        prefijo = (nodos[primero].text or "")[: posicion - offsets[primero][0]]
        if primero == ultimo:
            sufijo = (nodos[primero].text or "")[fin - offsets[primero][0]:]
            nodos[primero].text = prefijo + nuevo + sufijo
        else:
            nodos[primero].text = prefijo + nuevo
            for indice in afectados[1:-1]:
                nodos[indice].text = ""
            nodos[ultimo].text = (nodos[ultimo].text or "")[fin - offsets[ultimo][0]:]
        for nodo in nodos:
            if nodo.text and (nodo.text != nodo.text.strip() or "  " in nodo.text):
                nodo.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        aplicadas += 1
    return aplicadas


def _texto_normalizado(texto: str) -> str:
    import re as _re

    return _re.sub(r"\s+", " ", texto).strip()


def _reemplazar_flexible(p, viejo: str, nuevo: str, maximo: Optional[int] = 1) -> int:
    """
    Sustituye un texto aunque el ancla use espacios donde el párrafo tiene saltos de
    línea. Si el reemplazo literal falla, aplica solo los tramos que difieren,
    conservando los saltos y el formato del resto del párrafo.
    """
    aplicadas = _reemplazar_texto_parrafo(p, viejo, nuevo, maximo)
    if aplicadas or not viejo or not nuevo:
        return aplicadas
    import difflib

    comparador = difflib.SequenceMatcher(None, viejo, nuevo, autojunk=False)
    tramos = []
    actual = None
    for etiqueta, i1, i2, j1, j2 in comparador.get_opcodes():
        if etiqueta == "equal":
            if actual is not None and (i2 - i1) < 5:
                continue
            if actual is not None:
                tramos.append(actual)
                actual = None
            continue
        if actual is None:
            actual = [i1, i2, j1, j2]
        else:
            actual[1], actual[3] = i2, j2
    if actual is not None:
        tramos.append(actual)

    texto = p.text
    total = 0
    for i1, i2, j1, j2 in tramos:
        viejo_tramo, nuevo_tramo = viejo[i1:i2], nuevo[j1:j2]
        if not viejo_tramo or texto.count(viejo_tramo) != 1:
            return total
        if _reemplazar_texto_parrafo(p, viejo_tramo, nuevo_tramo, 1) != 1:
            return total
        total += 1
    return total


def _fijar_texto_run(r_el, texto: str) -> None:
    """Deja un único w:t con el texto indicado dentro del run, conservando su formato."""
    from docx.oxml import OxmlElement

    nodos = list(r_el.iter(_qn("w:t")))
    if not nodos:
        nodo = OxmlElement("w:t")
        r_el.append(nodo)
        nodos = [nodo]
    nodos[0].text = texto
    if texto != texto.strip():
        nodos[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    else:
        nodos[0].attrib.pop("{http://www.w3.org/XML/1998/namespace}space", None)
    for extra in nodos[1:]:
        extra.getparent().remove(extra)


def _run_a_cursiva(r_el) -> None:
    """Inserta <w:i/> y <w:iCs/> en el rPr del run respetando el orden del esquema."""
    from docx.oxml import OxmlElement

    rpr = r_el.find(_qn("w:rPr"))
    if rpr is None:
        rpr = OxmlElement("w:rPr")
        r_el.insert(0, rpr)
    if rpr.find(_qn("w:i")) is not None:
        return
    previos = {_qn(t) for t in ("w:rStyle", "w:rFonts", "w:b", "w:bCs")}
    posicion = 0
    for indice, hijo in enumerate(list(rpr)):
        if hijo.tag in previos:
            posicion = indice + 1
    rpr.insert(posicion, OxmlElement("w:iCs"))
    rpr.insert(posicion, OxmlElement("w:i"))


def aplicar_alineaciones(documento, lotes) -> Dict[str, Any]:
    """
    Fija la alineación nativa de párrafos concretos. APA 7 pide alineación izquierda
    con margen derecho irregular en las referencias, porque el justificado estira las
    líneas que preceden a una URL larga. No altera el texto ni provoca reflujo.
    """
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    mapa = {
        "left": WD_ALIGN_PARAGRAPH.LEFT,
        "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
        "center": WD_ALIGN_PARAGRAPH.CENTER,
        "right": WD_ALIGN_PARAGRAPH.RIGHT,
    }
    acciones: List[Dict[str, Any]] = []
    aplicadas = 0
    fallidas = 0
    for nombre, datos in lotes:
        for orden in datos.get("alineaciones", []):
            indice = orden.get("indice_docx")
            clave = str(orden.get("valor", "left")).strip().lower()
            estado = "fallida"
            detalle = "índice inválido"
            if isinstance(indice, int) and 0 <= indice < len(documento.paragraphs):
                if clave not in mapa:
                    detalle = f"alineación no reconocida: {clave}"
                else:
                    parrafo = documento.paragraphs[indice]
                    anterior = parrafo.alignment
                    parrafo.alignment = mapa[clave]
                    estado = "aplicada"
                    detalle = f"{anterior} -> {clave}"
            if estado == "aplicada":
                aplicadas += 1
            else:
                fallidas += 1
            acciones.append(
                {
                    "lote": nombre,
                    "indice_docx": indice,
                    "ubicacion": orden.get("ubicacion", ""),
                    "alineacion": clave,
                    "estado": estado,
                    "detalle": detalle,
                }
            )
    return {"alineaciones_aplicadas": aplicadas, "alineaciones_fallidas": fallidas, "acciones": acciones}


def aplicar_cursivas(documento, lotes) -> Dict[str, Any]:
    """
    Aplica cursiva nativa a un fragmento exacto de un párrafo, dividiendo el run en
    tres tramos con idéntico formato. No altera el texto del párrafo.
    """
    from copy import deepcopy

    acciones: List[Dict[str, Any]] = []
    aplicadas = 0
    fallidas = 0
    for nombre, datos in lotes:
        for orden in datos.get("cursivas", []):
            indice = orden.get("indice_docx")
            texto = orden.get("texto", "")
            estado = "fallida"
            detalle = "índice o texto inválido"
            if isinstance(indice, int) and 0 <= indice < len(documento.paragraphs) and texto:
                parrafo = documento.paragraphs[indice]
                candidato = None
                for run in parrafo.runs:
                    if run.text.count(texto) == 1:
                        candidato = run
                        break
                if candidato is None:
                    detalle = "fragmento no hallado o ambiguo en el párrafo"
                else:
                    run_el = candidato._r
                    antes, _, despues = candidato.text.partition(texto)
                    padre = run_el.getparent()
                    posicion = list(padre).index(run_el)
                    nuevos = []
                    if antes:
                        tramo = deepcopy(run_el)
                        _fijar_texto_run(tramo, antes)
                        nuevos.append(tramo)
                    tramo = deepcopy(run_el)
                    _fijar_texto_run(tramo, texto)
                    _run_a_cursiva(tramo)
                    nuevos.append(tramo)
                    if despues:
                        tramo = deepcopy(run_el)
                        _fijar_texto_run(tramo, despues)
                        nuevos.append(tramo)
                    padre.remove(run_el)
                    for desplazamiento, elemento in enumerate(nuevos):
                        padre.insert(posicion + desplazamiento, elemento)
                    estado = "aplicada"
                    detalle = f"{len(nuevos)} runs nativos"
            if estado == "aplicada":
                aplicadas += 1
            else:
                fallidas += 1
            acciones.append(
                {
                    "lote": nombre,
                    "indice_docx": indice,
                    "ubicacion": orden.get("ubicacion", ""),
                    "texto": texto,
                    "estado": estado,
                    "detalle": detalle,
                }
            )
    return {"cursivas_aplicadas": aplicadas, "cursivas_fallidas": fallidas, "acciones": acciones}


def _buscar_unico(documento, viejo: str):
    """Devuelve el párrafo único que contiene el ancla, o None si hay cero o varias."""
    objetivo = _texto_normalizado(viejo)
    candidatos = [p for p in documento.paragraphs if objetivo in _texto_normalizado(p.text)]
    return candidatos[0] if len(candidatos) == 1 else None


_ESPACIOS_COLA = " \t "


def sanear_espacios_finales(documento) -> Dict[str, Any]:
    """
    Recorta los espacios y tabuladores residuales de la cola del texto de cada
    párrafo del cuerpo. Actúa sobre el último run con texto y sobre los runs
    posteriores que solo contengan espacios, sin eliminar runs ni alterar el
    formato. Los párrafos cuyo texto íntegro sea espacio en blanco no se tocan.
    """
    acciones: List[Dict[str, Any]] = []
    for indice, parrafo in enumerate(documento.paragraphs):
        elemento = getattr(parrafo, "_p", parrafo)
        runs = [r for r in elemento.findall(_qn("w:r")) if r.find(_qn("w:t")) is not None]
        if not runs:
            continue
        texto_parrafo = "".join(
            t.text or "" for r in runs for t in r.findall(_qn("w:t"))
        )
        if not texto_parrafo or not texto_parrafo.strip():
            continue

        ultimo_con_texto = None
        for run in runs:
            if any((t.text or "").strip(_ESPACIOS_COLA) for t in run.findall(_qn("w:t"))):
                ultimo_con_texto = run
        if ultimo_con_texto is None:
            continue

        recortado = 0
        nodos = ultimo_con_texto.findall(_qn("w:t"))
        for nodo in reversed(nodos):
            actual = nodo.text or ""
            limpio = actual.rstrip(_ESPACIOS_COLA)
            if limpio != actual:
                recortado += len(actual) - len(limpio)
                nodo.text = limpio
                nodo.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            if limpio:
                break

        posteriores = runs[runs.index(ultimo_con_texto) + 1:]
        for run in posteriores:
            for nodo in run.findall(_qn("w:t")):
                actual = nodo.text or ""
                if actual and not actual.strip(_ESPACIOS_COLA):
                    recortado += len(actual)
                    nodo.text = ""
                    nodo.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")

        if recortado:
            acciones.append(
                {
                    "categoria": "saneamiento_espacios_finales",
                    "parrafo": indice,
                    "caracteres_recortados": recortado,
                    "estado": "corregido",
                }
            )
    return {
        "acciones": acciones,
        "parrafos_saneados": len(acciones),
        "indices": [a["parrafo"] for a in acciones],
        "caracteres_recortados": sum(a["caracteres_recortados"] for a in acciones),
    }


def aplicar_ordenes_edicion(
    ruta_origen: Union[str, Path],
    lotes: Sequence[Tuple[str, Dict[str, Any]]],
    ruta_destino: Optional[Union[str, Path]] = None,
    solo_verificar: bool = False,
    tablas_matriz: Sequence[int] = (),
    margenes_matriz_dxa: int = 57,
    tamano_matriz_pt: float = 8.0,
    via_matriz: str = "rebalanceo",
    tablas_rebalanceo: Sequence[int] = (),
    sanear_espacios: bool = False,
) -> Dict[str, Any]:
    """
    Aplica lotes de órdenes de sustitución sobre un DOCX sin insertar ni eliminar
    párrafos. Cada orden se direcciona por índice base 0 de párrafo o de tabla
    (fila y columna base 1, con encabezado incluido). En modo ``solo_verificar``
    no escribe archivo alguno y reporta qué órdenes se aplicarían.

    ``via_matriz`` elige una sola vía geométrica para las matrices de anexos:
    ``margenes`` (tcMar), ``rebalanceo`` (anchos columnares) o ``ambas``.
    ``tablas_rebalanceo`` rebalancea tablas adicionales conservando su ancho total.
    """
    import re as _re

    import docx

    if via_matriz not in ("margenes", "rebalanceo", "ambas"):
        raise ValueError("via_matriz debe ser 'margenes', 'rebalanceo' o 'ambas'")

    origen = Path(ruta_origen)
    documento = docx.Document(str(origen))
    acciones: List[Dict[str, Any]] = []
    resumen_lotes: List[Dict[str, Any]] = []

    matrices: Dict[str, Any] = {"acciones": [], "tablas": []}
    if tablas_matriz and not solo_verificar:
        matrices = ajustar_matriz_anexo(
            documento,
            tablas_matriz,
            margenes_dxa=margenes_matriz_dxa,
            tamano_pt=tamano_matriz_pt,
            aplicar_margenes=via_matriz in ("margenes", "ambas"),
            rebalancear=via_matriz in ("rebalanceo", "ambas"),
        )
        acciones += matrices["acciones"]

    rebalanceos: Dict[str, Any] = {"acciones": [], "tablas": []}
    if tablas_rebalanceo and not solo_verificar:
        rebalanceos = rebalancear_tabla(documento, tablas_rebalanceo)
        acciones += rebalanceos["acciones"]

    for nombre, datos in lotes:
        ordenes = datos.get("sustituciones", datos if isinstance(datos, list) else [])
        aplicadas = 0
        fallidas = 0
        detalles = []
        for orden in ordenes:
            viejo = orden.get("ancla_original", "")
            nuevo = orden.get("texto_nuevo", "")
            ocurrencias = orden.get("ocurrencias") or 1
            ubicacion = orden.get("ubicacion") or ""
            indice = orden.get("indice_docx")
            modo = "indice"
            aplicadas_orden = 0

            coincidencia_tabla = _re.match(r"TABLA\s+(\d+),\s*fila\s+(\d+),\s*columna\s+(\d+)", ubicacion)
            if coincidencia_tabla:
                numero_tabla = int(coincidencia_tabla.group(1))
                fila, columna = int(coincidencia_tabla.group(2)), int(coincidencia_tabla.group(3))
                objetivo = _texto_normalizado(viejo)
                candidatas = []
                if 0 <= numero_tabla < len(documento.tables):
                    candidatas.append(documento.tables[numero_tabla])
                if isinstance(indice, int) and 0 <= indice < len(documento.tables):
                    if not candidatas or documento.tables[indice] is not candidatas[0]:
                        candidatas.append(documento.tables[indice])
                celda = None
                for tabla in candidatas:
                    if fila - 1 >= len(tabla.rows):
                        continue
                    fila_celdas = tabla.rows[fila - 1].cells
                    if columna - 1 < len(fila_celdas):
                        posible = fila_celdas[columna - 1]
                        if objetivo in _texto_normalizado(posible.text):
                            celda = posible
                            break
                    encontradas = [c for c in fila_celdas if objetivo in _texto_normalizado(c.text)]
                    if len(encontradas) == 1:
                        celda = encontradas[0]
                        modo = "celda_reubicada"
                        break
                if celda is None and objetivo:
                    ubicaciones = []
                    for tabla in documento.tables:
                        for row in tabla.rows:
                            for c in row.cells:
                                if objetivo in _texto_normalizado(c.text):
                                    ubicaciones.append(c)
                    if len(ubicaciones) == 1:
                        celda = ubicaciones[0]
                        modo = "celda_reubicada"
                if celda is not None:
                    for parrafo in celda.paragraphs:
                        if _texto_normalizado(viejo) in _texto_normalizado(parrafo.text):
                            aplicadas_orden += _reemplazar_flexible(parrafo, viejo, nuevo, ocurrencias)
                if aplicadas_orden == 0:
                    modo = "fallida"
            else:
                if isinstance(indice, int) and 0 <= indice < len(documento.paragraphs):
                    parrafo = documento.paragraphs[indice]
                    if _texto_normalizado(viejo) in _texto_normalizado(parrafo.text):
                        aplicadas_orden = _reemplazar_flexible(parrafo, viejo, nuevo, ocurrencias)
                if aplicadas_orden == 0:
                    unico = _buscar_unico(documento, viejo) if viejo else None
                    if unico is not None:
                        aplicadas_orden = _reemplazar_flexible(unico, viejo, nuevo, ocurrencias)
                        modo = "busqueda_unica"
                    else:
                        modo = "fallida"

            if aplicadas_orden:
                aplicadas += 1
            else:
                fallidas += 1
            detalles.append(
                {
                    "indice_docx": indice,
                    "ubicacion": ubicacion or None,
                    "ancla": viejo[:80],
                    "sustituciones": aplicadas_orden,
                    "modo": modo,
                    "estado": "aplicada" if aplicadas_orden else "fallida",
                }
            )
        acciones.extend(
            {
                "categoria": "orden_edicion",
                "lote": nombre,
                "indice_docx": d["indice_docx"],
                "ubicacion": d["ubicacion"],
                "estado": d["estado"],
                "detalle": f"{d['sustituciones']} sustitucion(es); modo {d['modo']}",
            }
            for d in detalles
        )
        resumen_lotes.append(
            {
                "lote": nombre,
                "total": len(ordenes),
                "aplicadas": aplicadas,
                "fallidas": fallidas,
                "detalles": detalles,
            }
        )

    saneamiento: Dict[str, Any] = {"acciones": [], "parrafos_saneados": 0, "indices": [], "caracteres_recortados": 0}
    if sanear_espacios:
        saneamiento = sanear_espacios_finales(documento)
        acciones += saneamiento["acciones"]

    destino = None
    sha_destino = None
    if not solo_verificar:
        if ruta_destino is None:
            raise ValueError("Se requiere ruta_destino cuando solo_verificar es False")
        destino = Path(ruta_destino)
        seguridad.asegurar_no_sobrescribe(origen, destino)
        seguridad.asegurar_escritura_permitida(destino)
        documento.save(str(destino))
        sha_destino = seguridad.sha256_archivo(destino)

    verificacion = docx.Document(str(destino)) if destino is not None else documento
    return {
        "origen": str(origen),
        "destino": str(destino) if destino else None,
        "solo_verificar": solo_verificar,
        "sha256_origen": seguridad.sha256_archivo(origen),
        "sha256_destino": sha_destino,
        "parrafos": len(verificacion.paragraphs),
        "tablas": len(verificacion.tables),
        "total_ordenes": sum(r["total"] for r in resumen_lotes),
        "total_aplicadas": sum(r["aplicadas"] for r in resumen_lotes),
        "total_fallidas": sum(r["fallidas"] for r in resumen_lotes),
        "lotes": resumen_lotes,
        "matrices_anexo": matrices["tablas"],
        "tablas_rebalanceadas": rebalanceos["tablas"],
        "saneamiento_espacios": saneamiento,
        "acciones": acciones,
    }


def detectar_duplicados_editoriales(documento, ventana: int = 60) -> Dict[str, Any]:
    """
    Verificación previa/posterior de las categorías 2 y 3 de la auditoría:
    bloque duplicado por doble orilla literal y encabezados consecutivos repetidos.
    """
    cuerpo = documento.element.body
    con_cola = []
    consecutivos = []
    anterior = None
    for indice, elemento in enumerate(list(cuerpo)):
        if elemento.tag != _qn("w:p"):
            anterior = None
            continue
        texto = _texto_parrafo(elemento).strip()
        if len(texto) >= 2 * ventana and texto[:ventana] == texto[-ventana:]:
            con_cola.append({"parrafo": indice, "orilla": texto[:ventana]})
        pPr = elemento.find(_qn("w:pPr"))
        nivel = pPr.find(_qn("w:outlineLvl")) if pPr is not None else None
        if nivel is not None and texto:
            if anterior is not None and anterior[1] == texto:
                consecutivos.append({"parrafo": indice, "texto": texto[:80]})
            anterior = (indice, texto)
        else:
            anterior = None
    return {"bloques_duplicados": con_cola, "encabezados_consecutivos_repetidos": consecutivos}


def contadores_estructurales(documento) -> Dict[str, int]:
    """Cuenta las categorías auditadas para el antes/después del reporte."""
    import re as _re

    cuerpo = documento.element.body
    imagen_antes = 0
    sin_estilo = 0
    total_rotulos = 0
    for elemento in list(cuerpo):
        if not _es_rotulo(elemento):
            continue
        total_rotulos += 1
        pPr = elemento.find(_qn("w:pPr"))
        if pPr is None or pPr.find(_qn("w:pStyle")) is None:
            sin_estilo += 1
        if _re.match(r"^Figura\s+(1[1-9]|[2-4]\d)\b", _texto_parrafo(elemento).strip()):
            if _parrafo_con_imagen(elemento.getprevious()):
                imagen_antes += 1
    notas_sin_prefijo = 0
    for elemento in list(cuerpo):
        if elemento.tag != _qn("w:tbl"):
            continue
        siguiente = elemento.getnext()
        if siguiente is None or siguiente.tag != _qn("w:p"):
            continue
        texto = _texto_parrafo(siguiente).strip()
        if not texto or texto.startswith(("Nota.", "Figura", "Tabla")):
            continue
        tamanos = set()
        for run in siguiente.iter(_qn("w:r")):
            rPr = run.find(_qn("w:rPr"))
            if rPr is not None and rPr.find(_qn("w:sz")) is not None:
                tamanos.add(rPr.find(_qn("w:sz")).get(_qn("w:val")))
        pPr = siguiente.find(_qn("w:pPr"))
        linea = None
        if pPr is not None and pPr.find(_qn("w:spacing")) is not None:
            linea = pPr.find(_qn("w:spacing")).get(_qn("w:line"))
        if tamanos and tamanos <= {"19", "20"} and linea == "240":
            notas_sin_prefijo += 1
    return {
        "rotulos_total": total_rotulos,
        "rotulos_sin_estilo": sin_estilo,
        "figuras_imagen_antes_del_rotulo": imagen_antes,
        "notas_sin_prefijo": notas_sin_prefijo,
    }


def corregir_estructura_editorial(
    ruta_origen: Union[str, Path],
    ruta_destino: Union[str, Path],
    figuras_desde: int = 11,
    figuras_hasta: int = 48,
    figuras_excluidas: Sequence[int] = (49, 50, 51, 52),
    tablas_matriz: Sequence[int] = (),
    margenes_matriz_dxa: int = 57,
    tamano_matriz_pt: float = 8.0,
    referencias: Sequence[Dict[str, Any]] = (),
    sanear_espacios: bool = False,
) -> Dict[str, Any]:
    """
    Pasada única y trazable de corrección estructural APA 7 sobre un informe:
    orden figura/rótulo, formato y estilo de rótulos, prefijo de notas de tabla,
    ajuste geométrico de las matrices de datos de anexos y, opcionalmente,
    recorte de espacios residuales de cola.
    No crea texto, no altera tablas de datos ni referencias.
    """
    import docx

    origen = Path(ruta_origen)
    destino = Path(ruta_destino)
    seguridad.asegurar_no_sobrescribe(origen, destino)
    seguridad.asegurar_escritura_permitida(destino)

    documento = docx.Document(str(origen))
    antes = contadores_estructurales(documento)
    duplicados_antes = detectar_duplicados_editoriales(documento)

    acciones = []
    acciones += reordenar_figuras_apa7(documento, figuras_desde, figuras_hasta)
    acciones += normalizar_rotulos_ilustracion(documento, figuras_excluidas=figuras_excluidas)
    acciones += insertar_prefijo_notas(documento)
    matrices: Dict[str, Any] = {"acciones": [], "tablas": []}
    if tablas_matriz:
        matrices = ajustar_matriz_anexo(
            documento,
            tablas_matriz,
            margenes_dxa=margenes_matriz_dxa,
            tamano_pt=tamano_matriz_pt,
        )
        acciones += matrices["acciones"]
    resultado_referencias: Dict[str, Any] = {}
    if referencias:
        resultado_referencias = insertar_referencias(documento, referencias)
        acciones += resultado_referencias["acciones"]
    saneamiento: Dict[str, Any] = {"acciones": [], "parrafos_saneados": 0, "indices": [], "caracteres_recortados": 0}
    if sanear_espacios:
        saneamiento = sanear_espacios_finales(documento)
        acciones += saneamiento["acciones"]

    destino.parent.mkdir(parents=True, exist_ok=True)
    documento.save(str(destino))

    verificacion = docx.Document(str(destino))
    despues = contadores_estructurales(verificacion)
    duplicados_despues = detectar_duplicados_editoriales(verificacion)
    return {
        "origen": str(origen),
        "destino": str(destino),
        "sha256_origen": seguridad.sha256_archivo(origen),
        "sha256_destino": seguridad.sha256_archivo(destino),
        "parrafos_antes": len(docx.Document(str(origen)).paragraphs),
        "parrafos_despues": len(verificacion.paragraphs),
        "tablas_antes": len(docx.Document(str(origen)).tables),
        "tablas_despues": len(verificacion.tables),
        "antes": antes,
        "despues": despues,
        "duplicados_antes": duplicados_antes,
        "duplicados_despues": duplicados_despues,
        "matrices_anexo": matrices["tablas"],
        "referencias": resultado_referencias,
        "saneamiento_espacios": saneamiento,
        "acciones": acciones,
    }


def reconstruir_tabla_filas(
    ruta_origen: Union[str, Path],
    ruta_destino: Union[str, Path],
    indice_tabla: int,
    filas: Sequence[Any],
    alineaciones: Optional[Sequence[str]] = None,
    fila_total: Optional[Any] = None,
    columnas: Optional[Sequence[str]] = None,
    nota: Optional[str] = None,
    porcentaje_compacto: bool = False,
) -> Dict[str, Any]:
    """
    Reconstruye las filas de datos de una tabla nativa clonando la geometría y el formato
    de una fila de datos existente (w:tblGrid, w:tcPr, fuente, w:cantSplit).

    Conserva la fila 0 de encabezado (con w:tblHeader y las tres líneas APA 7) y la fila
    final de Total, que solo se reescribe si se entrega ``fila_total``.

    ``filas`` admite listas de celdas o diccionarios (claves en ``columnas``). Devuelve el
    detalle fila por fila para el reporte de auditoría.
    """
    from copy import deepcopy

    import docx

    origen = Path(ruta_origen)
    destino = Path(ruta_destino)
    seguridad.asegurar_no_sobrescribe(origen, destino)
    seguridad.asegurar_escritura_permitida(destino)

    sha_origen = seguridad.sha256_archivo(origen)
    documento = docx.Document(str(origen))
    tablas_antes = len(documento.tables)
    parrafos_antes = len(documento.paragraphs)
    if not 0 <= indice_tabla < tablas_antes:
        raise IndexError(f"Índice de tabla {indice_tabla} fuera de rango (0..{tablas_antes - 1})")

    table = documento.tables[indice_tabla]
    tbl = table._tbl
    grid = [int(g.get(_qn("w:w"))) for g in tbl.tblGrid.gridCol_lst]
    ancho = sum(grid)

    trs = tbl.tr_lst
    if len(trs) < 2:
        raise ValueError("La tabla no tiene filas de datos que clonar")
    filas_antes = len(trs)
    plantilla = deepcopy(trs[1])
    tr_total = trs[-1] if fila_total is not None else None
    for tr in trs[1:-1] if fila_total is not None else trs[1:]:
        tbl.remove(tr)

    if columnas is None and filas and isinstance(filas[0], dict):
        columnas = list(filas[0].keys())
    alineaciones = list(alineaciones or ["left"] * len(grid))
    if len(alineaciones) < len(grid):
        alineaciones += ["left"] * (len(grid) - len(alineaciones))

    def _valores(fila: Any) -> List[str]:
        if isinstance(fila, dict):
            if columnas is None:
                raise ValueError("Se requiere 'columnas' para filas en formato diccionario")
            valores = [str(fila.get(c, "")) for c in columnas]
        else:
            valores = [str(v) for v in fila]
        if porcentaje_compacto:
            import re as _re

            valores = [_re.sub(r"(\d)\s+%", r"\1%", v) for v in valores]
        return valores

    detalle: List[Dict[str, Any]] = []
    for k, fila in enumerate(filas, start=1):
        nuevo = deepcopy(plantilla)
        _preparar_tr(nuevo, cant_split=True, tbl_header=False)
        valores = _valores(fila)
        celdas = nuevo.findall(_qn("w:tc"))
        if len(valores) != len(celdas):
            raise ValueError(f"La fila {k} tiene {len(valores)} valores y la tabla {len(celdas)} columnas")
        for j, tc in enumerate(celdas):
            _fijar_texto_celda(tc, valores[j], alineaciones[j])
            tcW = tc.find(_qn("w:tcPr")).find(_qn("w:tcW"))
            if tcW is not None:
                tcW.set(_qn("w:w"), str(grid[j]))
                tcW.set(_qn("w:type"), "dxa")
        if tr_total is not None:
            tr_total.addprevious(nuevo)
        else:
            tbl.append(nuevo)
        detalle.append({"indice": k, "origen": "plantilla_fila_1", "celdas": valores})

    if fila_total is not None and tr_total is not None:
        _preparar_tr(tr_total, cant_split=True, tbl_header=False)
        valores = _valores(fila_total)
        celdas = tr_total.findall(_qn("w:tc"))
        if len(valores) != len(celdas):
            raise ValueError("La fila Total no coincide en columnas con la tabla")
        for j, tc in enumerate(celdas):
            _fijar_texto_celda(tc, valores[j], alineaciones[j])
            tcW = tc.find(_qn("w:tcPr")).find(_qn("w:tcW"))
            if tcW is not None:
                tcW.set(_qn("w:w"), str(grid[j]))
        detalle.append({"indice": len(filas) + 1, "origen": "fila_total_conservada", "celdas": valores})

    nota_actualizada = actualizar_nota_tabla(table, nota) if nota else False
    destino.parent.mkdir(parents=True, exist_ok=True)
    documento.save(str(destino))

    verificacion = docx.Document(str(destino))
    tabla_final = verificacion.tables[indice_tabla]
    trs_final = tabla_final._tbl.tr_lst
    return {
        "tabla_indice": indice_tabla,
        "filas_antes": filas_antes,
        "filas_despues": len(trs_final),
        "encabezado_conservado": trs_final[0].find(_qn("w:trPr")).find(_qn("w:tblHeader")) is not None,
        "total_al_final": "".join(t.text or "" for t in trs_final[-1].iter(_qn("w:t"))).strip().startswith("Total"),
        "cant_split": sum(1 for tr in trs_final if tr.find(_qn("w:trPr")) is not None and tr.find(_qn("w:trPr")).find(_qn("w:cantSplit")) is not None),
        "tabla_flotante": tabla_final._tbl.tblPr.find(_qn("w:tblpPr")) is not None,
        "grid": grid,
        "ancho_total_dxa": ancho,
        "parrafos_antes": parrafos_antes,
        "parrafos_despues": len(verificacion.paragraphs),
        "tablas_antes": tablas_antes,
        "tablas_despues": len(verificacion.tables),
        "nota_actualizada": nota_actualizada,
        "sha256_origen": sha_origen,
        "sha256_destino": seguridad.sha256_archivo(destino),
        "destino": str(destino),
        "detalle_filas": detalle,
    }


def construir_docx_openxml(
    ruta_destino: Union[str, Path],
    titulo_documento: str,
    bloques: Sequence[Dict[str, Any]],
    permitir_referencias_bootstrap: bool = False,
) -> Path:
    """
    Construye un archivo Microsoft Word (.docx) 100% nativo OpenXML (sin dependencias externas)
    cumpliendo estrictamente los estándares UNAJMA y APA 7:
    - Papel A4: w=11906 dxa, h=16838 dxa
    - Márgenes UNAJMA: Superior=1985 dxa (3.5 cm), Izquierdo=1985 dxa (3.5 cm),
      Inferior=1418 dxa (2.5 cm), Derecho=1418 dxa (2.5 cm)
    - Tipografía: Times New Roman 12 pt (cuerpo) y 10 pt (tablas/notas)
    - Tablas APA 7 de 3 líneas horizontales, w:tblHeader, w:cantSplit, cero w:tblpPr
    - Referencias con sangría francesa de 1.27 cm (w:left="720" w:hanging="720")
    """
    p_dest = Path(ruta_destino)
    if not permitir_referencias_bootstrap:
        seguridad.asegurar_escritura_permitida(p_dest)
    p_dest.parent.mkdir(parents=True, exist_ok=True)

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>"""

    rels_root = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>"""

    doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>"""

    styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="es-PE"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="160" w:line="480" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:keepNext/>
      <w:spacing w:before="240" w:after="120" w:line="480" w:lineRule="auto"/>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="28"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:keepNext/>
      <w:spacing w:before="200" w:after="100" w:line="480" w:lineRule="auto"/>
      <w:jc w:val="left"/>
    </w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ReferenciaAPA7">
    <w:name w:val="Referencia APA 7"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="0" w:after="120" w:line="480" w:lineRule="auto"/>
      <w:ind w:left="720" w:hanging="720"/>
      <w:jc w:val="both"/>
    </w:pPr>
  </w:style>
</w:styles>"""

    settings_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:zoom w:percent="100"/>
  <w:defaultTabStop w:val="720"/>
  <w:characterSpacingControl w:val="doNotCompress"/>
</w:settings>"""

    core_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:dcterms="http://purl.org/dc/terms/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{html.escape(titulo_documento)}</dc:title>
  <dc:creator>{html.escape(rutas.TESISTA)}</dc:creator>
  <cp:lastModifiedBy>SIVAC-THESIS-LAB (maquetador-docx)</cp:lastModifiedBy>
  <dc:description>Documento generado con cirugía OpenXML nativa bajo normas APA 7 y Reglamento UNAJMA</dc:description>
</cp:coreProperties>"""

    body_parts: List[str] = []

    for b in bloques:
        tipo = b.get("tipo", "parrafo")
        if tipo == "titulo_portada":
            lineas = b.get("lineas", [])
            for lin in lineas:
                txt = html.escape(str(lin.get("texto", "")))
                bold = "<w:b/>" if lin.get("negrita", True) else ""
                sz = int(lin.get("pt", 14)) * 2
                body_parts.append(
                    f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="80" w:line="360" w:lineRule="auto"/></w:pPr>'
                    f'<w:r><w:rPr>{bold}<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr><w:t xml:space="preserve">{txt}</w:t></w:r></w:p>'
                )
        elif tipo == "h1":
            txt = html.escape(str(b.get("texto", "")))
            body_parts.append(
                f'<w:p><w:pPr><w:pStyle w:val="Heading1"/><w:jc w:val="center"/></w:pPr>'
                f'<w:r><w:rPr><w:b/><w:sz w:val="28"/></w:rPr><w:t xml:space="preserve">{txt}</w:t></w:r></w:p>'
            )
        elif tipo == "h2":
            txt = html.escape(str(b.get("texto", "")))
            body_parts.append(
                f'<w:p><w:pPr><w:pStyle w:val="Heading2"/><w:jc w:val="left"/></w:pPr>'
                f'<w:r><w:rPr><w:b/><w:sz w:val="24"/></w:rPr><w:t xml:space="preserve">{txt}</w:t></w:r></w:p>'
            )
        elif tipo == "h3":
            txt = html.escape(str(b.get("texto", "")))
            body_parts.append(
                f'<w:p><w:pPr><w:keepNext/><w:jc w:val="left"/></w:pPr>'
                f'<w:r><w:rPr><w:b/><w:i/><w:sz w:val="24"/></w:rPr><w:t xml:space="preserve">{txt}</w:t></w:r></w:p>'
            )
        elif tipo == "parrafo":
            txt = html.escape(str(b.get("texto", "")))
            align = b.get("alineacion", "both")
            sangria = '<w:ind w:firstLine="720"/>' if b.get("sangria_primera_linea", True) else ""
            bold = "<w:b/>" if b.get("negrita", False) else ""
            italic = "<w:i/>" if b.get("cursiva", False) else ""
            body_parts.append(
                f'<w:p><w:pPr><w:jc w:val="{align}"/><w:spacing w:after="160" w:line="480" w:lineRule="auto"/>{sangria}</w:pPr>'
                f'<w:r><w:rPr>{bold}{italic}<w:sz w:val="24"/></w:rPr><w:t xml:space="preserve">{txt}</w:t></w:r></w:p>'
            )
        elif tipo == "formula_omml":
            etiqueta = html.escape(str(b.get("etiqueta", "")))
            expresion = html.escape(str(b.get("expresion", "")))
            body_parts.append(
                f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="120"/></w:pPr>'
                f'<m:oMathPara xmlns:m="{M_NS}"><m:oMath><m:r><m:t>{expresion}</m:t></m:r></m:oMath></m:oMathPara>'
                f'<w:r><w:rPr><w:sz w:val="22"/></w:rPr><w:t xml:space="preserve">   {etiqueta}</w:t></w:r></w:p>'
            )
        elif tipo == "referencia":
            txt = html.escape(str(b.get("texto", "")))
            body_parts.append(
                f'<w:p><w:pPr><w:pStyle w:val="ReferenciaAPA7"/><w:ind w:left="720" w:hanging="720"/><w:jc w:val="both"/></w:pPr>'
                f'<w:r><w:rPr><w:sz w:val="24"/></w:rPr><w:t xml:space="preserve">{txt}</w:t></w:r></w:p>'
            )
        elif tipo == "tabla_apa7":
            numero = html.escape(str(b.get("numero", "Tabla 1")))
            titulo = html.escape(str(b.get("titulo", "")))
            encabezados = b.get("encabezados", [])
            filas = b.get("filas", [])
            nota = html.escape(str(b.get("nota", "Elaboración propia.")))
            total_w = int(b.get("ancho_total_dxa", 8503))
            num_cols = max(1, len(encabezados))
            col_w = total_w // num_cols

            # Prefijo APA 7: Tabla N en negrita + Título en cursiva con keepNext
            body_parts.append(
                f'<w:p><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="40" w:line="240" w:lineRule="auto"/></w:pPr>'
                f'<w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{numero}</w:t></w:r></w:p>'
            )
            body_parts.append(
                f'<w:p><w:pPr><w:keepNext/><w:spacing w:before="0" w:after="100" w:line="240" w:lineRule="auto"/></w:pPr>'
                f'<w:r><w:rPr><w:i/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{titulo}</w:t></w:r></w:p>'
            )

            grid_cols = "".join(f'<w:gridCol w:w="{col_w}"/>' for _ in range(num_cols))
            # Fila de encabezado con borde inferior single sz=4, tblHeader y cantSplit
            header_cells = []
            for h_txt in encabezados:
                h_esc = html.escape(str(h_txt))
                header_cells.append(
                    f'<w:tc><w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/>'
                    f'<w:tcBorders><w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/></w:tcBorders>'
                    f'<w:vAlign w:val="center"/></w:tcPr>'
                    f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="40" w:after="40" w:line="240" w:lineRule="auto"/></w:pPr>'
                    f'<w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{h_esc}</w:t></w:r></w:p></w:tc>'
                )
            rows_xml = [
                f'<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>{"".join(header_cells)}</w:tr>'
            ]

            for fila in filas:
                row_cells = []
                for idx_c, c_txt in enumerate(fila):
                    c_esc = html.escape(str(c_txt))
                    jc_val = "left" if idx_c <= 1 else "center"
                    row_cells.append(
                        f'<w:tc><w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
                        f'<w:p><w:pPr><w:jc w:val="{jc_val}"/><w:spacing w:before="30" w:after="30" w:line="240" w:lineRule="auto"/></w:pPr>'
                        f'<w:r><w:rPr><w:sz w:val="19"/></w:rPr><w:t xml:space="preserve">{c_esc}</w:t></w:r></w:p></w:tc>'
                    )
                rows_xml.append(f'<w:tr><w:trPr><w:cantSplit/></w:trPr>{"".join(row_cells)}</w:tr>')

            tabla_xml = (
                f'<w:tbl>'
                f'<w:tblPr>'
                f'<w:tblW w:w="{total_w}" w:type="dxa"/>'
                f'<w:jc w:val="center"/>'
                f'<w:tblBorders>'
                f'<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
                f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
                f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'</w:tblBorders>'
                f'<w:tblCellMar>'
                f'<w:top w:w="60" w:type="dxa"/><w:left w:w="90" w:type="dxa"/>'
                f'<w:bottom w:w="60" w:type="dxa"/><w:right w:w="90" w:type="dxa"/>'
                f'</w:tblCellMar>'
                f'</w:tblPr>'
                f'<w:tblGrid>{grid_cols}</w:tblGrid>'
                f'{"".join(rows_xml)}'
                f'</w:tbl>'
            )
            body_parts.append(tabla_xml)
            body_parts.append(
                f'<w:p><w:pPr><w:spacing w:before="60" w:after="180" w:line="240" w:lineRule="auto"/></w:pPr>'
                f'<w:r><w:rPr><w:i/><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">Nota. </w:t></w:r>'
                f'<w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">{nota}</w:t></w:r></w:p>'
            )

    sect_pr = (
        '<w:sectPr>'
        '<w:pgSz w:w="11906" w:h="16838" w:orient="portrait"/>'
        '<w:pgMar w:top="1985" w:right="1418" w:bottom="1418" w:left="1985" w:header="709" w:footer="709" w:gutter="0"/>'
        '<w:pgNumType w:fmt="decimal" w:start="1"/>'
        '</w:sectPr>'
    )

    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:document xmlns:w="{W_NS}" xmlns:m="{M_NS}">'
        f'<w:body>{"".join(body_parts)}{sect_pr}</w:body>'
        '</w:document>'
    )

    with zipfile.ZipFile(p_dest, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels_root)
        zf.writestr("word/_rels/document.xml.rels", doc_rels)
        zf.writestr("word/styles.xml", styles_xml)
        zf.writestr("word/settings.xml", settings_xml)
        zf.writestr("docProps/core.xml", core_xml)
        zf.writestr("word/document.xml", document_xml)

    return p_dest


def auditar_docx_openxml(ruta_docx: Union[str, Path]) -> Dict[str, Any]:
    """Audita un archivo .docx inspeccionando directamente su árbol OpenXML."""
    p = Path(ruta_docx)
    if not p.exists():
        return {"archivo": str(p), "existe": False, "cumple_apa7": False, "hallazgos": ["Archivo no encontrado"]}

    hallazgos: List[str] = []
    tablas_total = 0
    tablas_flotantes = 0
    tablas_con_header = 0
    tablas_con_cantsplit = 0
    referencias_sangria_francesa = 0
    formulas_omml = 0
    margenes_unajma_ok = False

    try:
        with zipfile.ZipFile(p, "r") as zf:
            xml_bytes = zf.read("word/document.xml")
        root = ET.fromstring(xml_bytes)

        for sect in root.iter(f"{{{W_NS}}}pgMar"):
            top = sect.attrib.get(f"{{{W_NS}}}top")
            left = sect.attrib.get(f"{{{W_NS}}}left")
            bottom = sect.attrib.get(f"{{{W_NS}}}bottom")
            right = sect.attrib.get(f"{{{W_NS}}}right")

            def _dxa_cercano(valor, esperado: int, tolerancia: int = 1) -> bool:
                try:
                    return abs(int(valor) - esperado) <= tolerancia
                except (TypeError, ValueError):
                    return False

            # Regla 03 UNAJMA: izquierdo 3.0 cm (1701 dxa), derecho, superior e
            # inferior 2.5 cm (1417 dxa). Se admite ±1 dxa por redondeo twips.
            if (
                _dxa_cercano(top, 1417)
                and _dxa_cercano(left, 1701)
                and _dxa_cercano(bottom, 1417)
                and _dxa_cercano(right, 1417)
            ):
                margenes_unajma_ok = True
            else:
                hallazgos.append(f"Márgenes fuera de norma UNAJMA: top={top}, left={left}, bottom={bottom}, right={right}")

        for tbl in root.iter(f"{{{W_NS}}}tbl"):
            tablas_total += 1
            if list(tbl.iter(f"{{{W_NS}}}tblpPr")):
                tablas_flotantes += 1
                hallazgos.append(f"Tabla #{tablas_total} contiene posicionamiento flotante <w:tblpPr> prohibido.")
            if list(tbl.iter(f"{{{W_NS}}}tblHeader")):
                tablas_con_header += 1
            if list(tbl.iter(f"{{{W_NS}}}cantSplit")):
                tablas_con_cantsplit += 1

        for ind in root.iter(f"{{{W_NS}}}ind"):
            if ind.attrib.get(f"{{{W_NS}}}hanging") == "720":
                referencias_sangria_francesa += 1

        for _ in root.iter(f"{{{M_NS}}}oMath"):
            formulas_omml += 1

    except Exception as exc:
        hallazgos.append(f"Error al inspeccionar OpenXML: {exc}")

    return {
        "archivo": str(p),
        "existe": True,
        "sha256": seguridad.sha256_archivo(p),
        "bytes": p.stat().st_size,
        "margenes_unajma_ok": margenes_unajma_ok,
        "tablas_total": tablas_total,
        "tablas_flotantes": tablas_flotantes,
        "tablas_con_header": tablas_con_header,
        "tablas_con_cantsplit": tablas_con_cantsplit,
        "referencias_sangria_francesa": referencias_sangria_francesa,
        "formulas_omml": formulas_omml,
        "cumple_apa7": len(hallazgos) == 0 and margenes_unajma_ok and tablas_flotantes == 0,
        "hallazgos": hallazgos,
    }


def _pdf_escape(texto: str) -> str:
    """Convierte texto UTF-8 a codificación PDF WinAnsi (Latin-1) escapando paréntesis."""
    reemplazos = {
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "—": "-",
        "–": "-",
        "•": "*",
        "≥": ">=",
        "≤": "<=",
        "≠": "!=",
        "±": "+/-",
        "×": "x",
        "⟶": "->",
        "→": "->",
    }
    for k, v in reemplazos.items():
        texto = texto.replace(k, v)
    b = texto.encode("latin-1", errors="replace").decode("latin-1")
    return b.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def construir_pdf_nativo(
    ruta_destino: Union[str, Path],
    titulo: str,
    paginas_lineas: Sequence[Sequence[str]],
    permitir_referencias_bootstrap: bool = False,
) -> Path:
    """
    Construye un documento PDF 1.4 multipágina válido con tipografía Times-Roman y Helvetica-Bold,
    encabezado institucional UNAJMA y numeración de páginas.
    """
    p_dest = Path(ruta_destino)
    if not permitir_referencias_bootstrap:
        seguridad.asegurar_escritura_permitida(p_dest)
    p_dest.parent.mkdir(parents=True, exist_ok=True)

    num_pages = max(1, len(paginas_lineas))
    # Objetos PDF:
    # 1: Catalog
    # 2: Pages
    # 3: Font F1 (Times-Roman)
    # 4: Font F2 (Times-Bold)
    # 5 + 2*i: Page i
    # 6 + 2*i: Content stream i
    objects: List[bytes] = []

    page_ids = [5 + 2 * i for i in range(num_pages)]
    kids_str = " ".join(f"{pid} 0 R" for pid in page_ids)

    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(f"<< /Type /Pages /Kids [{kids_str}] /Count {num_pages} >>".encode("ascii"))
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman /Encoding /WinAnsiEncoding >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold /Encoding /WinAnsiEncoding >>")

    for i, lineas in enumerate(paginas_lineas):
        page_id = 5 + 2 * i
        content_id = 6 + 2 * i
        stream_cmds = [
            "BT",
            "/F2 9 Tf",
            "85 795 Td",
            f"({_pdf_escape('UNIVERSIDAD NACIONAL JOSE MARIA ARGUEDAS (UNAJMA) - EPIS | SIVAC-THESIS-LAB')}) Tj",
            "ET",
            "0.7 w 85 788 m 525 788 l S",
        ]
        y = 762
        for idx_l, raw_line in enumerate(lineas):
            if y < 65:
                break
            es_encabezado = (
                idx_l == 0
                or raw_line.startswith("CAPÍTULO")
                or raw_line.startswith("CAPITULO")
                or raw_line.startswith("ANEXO")
                or raw_line.startswith("TABLA")
                or raw_line.startswith("Tabla ")
                or raw_line.startswith("CERTIFICADO")
                or raw_line.startswith("INSTRUMENTO")
                or raw_line.startswith("PROYECTO")
                or raw_line.startswith("1.")
                or raw_line.startswith("2.")
                or raw_line.startswith("3.")
                or raw_line.startswith("4.")
                or raw_line.startswith("5.")
                or raw_line.startswith("6.")
            )
            font_tag = "/F2" if es_encabezado else "/F1"
            font_sz = 11 if es_encabezado else 10
            # Ajuste de línea a 86 caracteres
            texto_linea = str(raw_line)
            fragmentos = [texto_linea[j : j + 88] for j in range(0, max(1, len(texto_linea)), 88)]
            for frag in fragmentos:
                if y < 65:
                    break
                stream_cmds.append(f"BT {font_tag} {font_sz} Tf 85 {y} Td ({_pdf_escape(frag)}) Tj ET")
                y -= 14

        # Pie de página
        stream_cmds.append("0.5 w 85 52 m 525 52 l S")
        stream_cmds.append(
            f"BT /F1 9 Tf 85 38 Td ({_pdf_escape(titulo[:65])} — Pagina {i + 1} de {num_pages}) Tj ET"
        )

        stream_data = "\n".join(stream_cmds).encode("latin-1", errors="replace")
        page_obj = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
            f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> "
            f"/Contents {content_id} 0 R >>"
        ).encode("ascii")
        content_obj = (
            f"<< /Length {len(stream_data)} >>\nstream\n".encode("ascii")
            + stream_data
            + b"\nendstream"
        )
        objects.append(page_obj)
        objects.append(content_obj)

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets: List[int] = []
    for idx, obj_bytes in enumerate(objects, start=1):
        offsets.append(len(out))
        out.extend(f"{idx} 0 obj\n".encode("ascii"))
        out.extend(obj_bytes)
        out.extend(b"\nendobj\n")

    xref_pos = len(out)
    out.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    out.extend(b"0000000000 65535 f \n")
    for off in offsets:
        out.extend(f"{off:010d} 00000 n \n".encode("ascii"))
    out.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("ascii")
    )
    p_dest.write_bytes(bytes(out))
    return p_dest


def construir_xlsx_openxml(
    ruta_destino: Union[str, Path],
    hojas: Sequence[Tuple[str, Sequence[Sequence[Any]]]],
) -> Path:
    """Construye un libro Microsoft Excel (.xlsx) OpenXML nativo con múltiples hojas."""
    p_dest = Path(ruta_destino)
    seguridad.asegurar_escritura_permitida(p_dest)
    p_dest.parent.mkdir(parents=True, exist_ok=True)

    overrides = "".join(
        f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for i in range(1, len(hojas) + 1)
    )
    content_types = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  {overrides}
</Types>"""

    rels_root = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

    sheets_tag = "".join(
        f'<sheet name="{html.escape(nombre[:31])}" sheetId="{i}" r:id="rId{i}"/>'
        for i, (nombre, _) in enumerate(hojas, start=1)
    )
    workbook_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>{sheets_tag}</sheets>
</workbook>"""

    wb_rels_tag = "".join(
        f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
        for i in range(1, len(hojas) + 1)
    )
    workbook_rels = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {wb_rels_tag}
</Relationships>"""

    with zipfile.ZipFile(p_dest, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels_root)
        zf.writestr("xl/workbook.xml", workbook_xml)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)

        for idx_s, (_, filas) in enumerate(hojas, start=1):
            rows_xml = []
            for r_idx, fila in enumerate(filas, start=1):
                cells_xml = []
                for c_idx, val in enumerate(fila):
                    col_letter = chr(65 + (c_idx % 26))
                    ref = f"{col_letter}{r_idx}"
                    if isinstance(val, (int, float)):
                        cells_xml.append(f'<c r="{ref}"><v>{val}</v></c>')
                    else:
                        txt = html.escape(str(val))
                        cells_xml.append(f'<c r="{ref}" t="inlineStr"><is><t>{txt}</t></is></c>')
                rows_xml.append(f'<row r="{r_idx}">{"".join(cells_xml)}</row>')
            sheet_xml = (
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                f'<sheetData>{"".join(rows_xml)}</sheetData>'
                '</worksheet>'
            )
            zf.writestr(f"xl/worksheets/sheet{idx_s}.xml", sheet_xml)

    return p_dest


def construir_png_300dpi(
    ruta_destino: Union[str, Path],
    ancho: int = 1200,
    alto: int = 750,
    color_acento: Tuple[int, int, int] = (30, 58, 138),
) -> Path:
    """
    Construye un archivo PNG de alta resolución con metadato físico exacto pHYs de 300 DPI
    (11811 píxeles por metro en X e Y) y diagramación limpia de cajas arquitectónicas/estadísticas.
    """
    p_dest = Path(ruta_destino)
    seguridad.asegurar_escritura_permitida(p_dest)
    p_dest.parent.mkdir(parents=True, exist_ok=True)

    def _chunk(chunk_type: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)

    # Fondo blanco #FFFFFF con marco gris #D3D3D3, franja superior en color_acento y bloques de diagrama
    r_ac, g_ac, b_ac = color_acento
    raw_rows = bytearray()

    for y in range(alto):
        raw_rows.append(0)  # Filter type 0 (None)
        if y < 4 or y >= alto - 4:
            # Borde exterior gris #D3D3D3 (regla de extraccion-figuras-pdf-docx)
            row_bytes = bytes([211, 211, 211]) * ancho
        elif 20 <= y < 76:
            # Encabezado del diagrama
            row_bytes = bytes([211, 211, 211]) * 24 + bytes([r_ac, g_ac, b_ac]) * (ancho - 48) + bytes([211, 211, 211]) * 24
        elif y in (140, 320, 360, 540, 580, 700):
            # Líneas horizontales de los módulos del diagrama
            row_bytes = bytes([255, 255, 255]) * 60 + bytes([r_ac, g_ac, b_ac]) * (ancho - 120) + bytes([255, 255, 255]) * 60
        elif (140 < y < 320) or (360 < y < 540) or (580 < y < 700):
            # Tres tarjetas modulares en paralelo
            bloque_w = (ancho - 180) // 3
            fila = bytearray(bytes([211, 211, 211]) * 4 + bytes([255, 255, 255]) * 56)
            for b_idx in range(3):
                fill_c = (241, 245, 249) if b_idx % 2 == 0 else (238, 242, 255)
                fila.extend(bytes([r_ac, g_ac, b_ac]) * 3)
                fila.extend(bytes(fill_c) * (bloque_w - 6))
                fila.extend(bytes([r_ac, g_ac, b_ac]) * 3)
                if b_idx < 2:
                    fila.extend(bytes([255, 255, 255]) * 30)
            restante = ancho - (len(fila) // 3) - 4
            if restante > 0:
                fila.extend(bytes([255, 255, 255]) * restante)
            fila.extend(bytes([211, 211, 211]) * 4)
            row_bytes = bytes(fila[: ancho * 3])
        else:
            row_bytes = bytes([211, 211, 211]) * 4 + bytes([255, 255, 255]) * (ancho - 8) + bytes([211, 211, 211]) * 4
        raw_rows.extend(row_bytes)

    ihdr = struct.pack(">IIBBBBB", ancho, alto, 8, 2, 0, 0, 0)
    # 300 DPI = 300 / 0.0254 = 11811 píxeles por metro (unit specifier = 1)
    phys = struct.pack(">IIB", 11811, 11811, 1)
    idat = zlib.compress(bytes(raw_rows), level=6)

    png_bytes = (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", ihdr)
        + _chunk(b"pHYs", phys)
        + _chunk(b"IDAT", idat)
        + _chunk(b"IEND", b"")
    )
    p_dest.write_bytes(png_bytes)
    return p_dest


# =============================================================================
# EXTENSION v17 — operaciones nativas adicionales (exclusivamente aditivas)
# Ninguna funcion existente cambia de firma ni de comportamiento. Cada funcion
# nueva se expone por un subcomando nuevo o por un parametro opcional.
# =============================================================================


def _runs_en_parrafo(p) -> List[Any]:
    """Todos los <w:r> del párrafo en orden de lectura, incluidos los de w:hyperlink."""
    return [r for r in p.iter(_qn("w:r"))]


def _texto_run(r) -> str:
    return "".join(t.text or "" for t in r.findall(_qn("w:t")))


def _dividir_run(r, cortes) -> Optional[List[Tuple[Any, int, int]]]:
    """Divide un run de texto plano en segmentos y devuelve [(run, inicio, fin)]."""
    from copy import deepcopy

    from docx.oxml import OxmlElement

    hijos = [c for c in r if c.tag not in (_qn("w:rPr"), _qn("w:lastRenderedPageBreak"))]
    if any(c.tag != _qn("w:t") for c in hijos):
        return None
    texto = _texto_run(r)
    puntos = sorted({int(c) for c in cortes if 0 < int(c) < len(texto)})
    if not puntos:
        return [(r, 0, len(texto))]
    padre = r.getparent()
    segmentos: List[Tuple[Any, int, int]] = []
    inicio = 0
    for corte in puntos + [len(texto)]:
        nuevo = deepcopy(r)
        for t in nuevo.findall(_qn("w:t")):
            nuevo.remove(t)
        for marca in nuevo.findall(_qn("w:lastRenderedPageBreak")):
            nuevo.remove(marca)
        t = OxmlElement("w:t")
        t.text = texto[inicio:corte]
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        nuevo.append(t)
        r.addprevious(nuevo)
        segmentos.append((nuevo, inicio, corte))
        inicio = corte
    padre.remove(r)
    return segmentos


def aplicar_cursivas_por_tramos(documento, especificacion: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aplica cursiva APA 7 a tramos exactos (títulos de obra, nombre y volumen de
    revista) dividiendo los runs en las fronteras del tramo. No cursiva la
    entrada completa ni toca autores, año o DOI.
    """
    from docx.oxml import OxmlElement

    acciones: List[Dict[str, Any]] = []
    fallos: List[Dict[str, Any]] = []
    for item in especificacion:
        indice = int(item["indice_docx"])
        tramos = [t for t in item.get("tramos", []) if t]
        if not 0 <= indice < len(documento.paragraphs):
            fallos.append({"indice_docx": indice, "motivo": "índice fuera de rango"})
            continue
        p = documento.paragraphs[indice]
        texto = _texto_parrafo(p._p)
        rangos: List[Tuple[int, int]] = []
        error = None
        for tramo in tramos:
            pos = texto.find(tramo)
            if pos < 0:
                error = f"tramo no encontrado: {tramo[:60]}"
                break
            if texto.find(tramo, pos + 1) >= 0:
                error = f"tramo ambiguo: {tramo[:60]}"
                break
            rangos.append((pos, pos + len(tramo)))
        if error:
            fallos.append({"indice_docx": indice, "motivo": error})
            continue
        info: List[Tuple[Any, int, int]] = []
        desplazamiento = 0
        for r in _runs_en_parrafo(p._p):
            t = _texto_run(r)
            info.append((r, desplazamiento, desplazamiento + len(t)))
            desplazamiento += len(t)
        cortes = set()
        for a, b in rangos:
            cortes.update((a, b))
        segmentos: List[Tuple[Any, int, int]] = []
        for r, a, b in info:
            if b <= a:
                segmentos.append((r, a, b))
                continue
            divididos = _dividir_run(r, [c for c in cortes if a < c < b])
            if divididos is None:
                error = "run con contenido no textual"
                break
            segmentos.extend(divididos)
        if error:
            fallos.append({"indice_docx": indice, "motivo": error})
            continue
        marcados = 0
        for r, a, b in segmentos:
            if not any(ia <= a and b <= ib for ia, ib in rangos):
                continue
            rPr = r.find(_qn("w:rPr"))
            if rPr is None:
                rPr = OxmlElement("w:rPr")
                r.insert(0, rPr)
            _rpr_propiedad(rPr, "i", True)
            _rpr_propiedad(rPr, "iCs", True)
            marcados += 1
        acciones.append({"indice_docx": indice, "tramos": len(rangos), "runs_marcados": marcados})
    return {
        "acciones": acciones,
        "fallos": fallos,
        "parrafos_ok": len(acciones),
        "parrafos_fallidos": len(fallos),
    }


def _insertar_keep_next(p) -> bool:
    from docx.oxml import OxmlElement

    pPr = p.find(_qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        p.insert(0, pPr)
    if pPr.find(_qn("w:keepNext")) is not None:
        return False
    kn = OxmlElement("w:keepNext")
    pStyle = pPr.find(_qn("w:pStyle"))
    if pStyle is not None:
        pStyle.addnext(kn)
    else:
        pPr.insert(0, kn)
    return True


def aplicar_keep_next(
    documento,
    indices: Sequence[int] = (),
    incluir_rotulos: bool = True,
    incluir_formulas: bool = True,
) -> Dict[str, Any]:
    """Inyecta w:keepNext para evitar rótulos y ecuaciones huérfanas."""
    objetivos = {int(i) for i in indices}
    if incluir_rotulos:
        objetivos.update(
            i
            for i, p in enumerate(documento.paragraphs)
            if p.style is not None and p.style.name == "Rotulo de ilustracion"
        )
    if incluir_formulas:
        objetivos.update(
            i
            for i, p in enumerate(documento.paragraphs)
            if any(str(e.tag).endswith(("}oMath", "}oMathPara")) for e in p._p.iter())
        )
    modificados = []
    for i in sorted(objetivos):
        if 0 <= i < len(documento.paragraphs) and _insertar_keep_next(documento.paragraphs[i]._p):
            modificados.append(i)
    return {"candidatos": len(objetivos), "modificados": len(modificados), "indices": modificados}


def ajustar_margenes_celda(
    documento,
    indice_tabla: int,
    izquierdo_dxa: int = 28,
    derecho_dxa: int = 28,
    superior_dxa: Optional[int] = None,
    inferior_dxa: Optional[int] = None,
) -> Dict[str, Any]:
    """Fija los márgenes de todas las celdas de una tabla.

    Los márgenes superior e inferior se conservan si no se especifican.
    """
    tabla = documento.tables[indice_tabla]
    _fijar_margenes_celda_tabla(
        tabla._tbl,
        izquierdo_dxa=izquierdo_dxa,
        derecho_dxa=derecho_dxa,
        superior_dxa=superior_dxa,
        inferior_dxa=inferior_dxa,
    )
    return {
        "tabla": indice_tabla,
        "izquierdo_dxa": izquierdo_dxa,
        "derecho_dxa": derecho_dxa,
        "superior_dxa": superior_dxa,
        "inferior_dxa": inferior_dxa,
        "filas": len(tabla.rows),
    }


def retirar_encabezado_repetido(tabla) -> bool:
    """Retira w:tblHeader de la fila 0 conservando w:cantSplit y los bordes."""
    trPr = tabla.rows[0]._tr.find(_qn("w:trPr"))
    if trPr is None:
        return False
    th = trPr.find(_qn("w:tblHeader"))
    if th is None:
        return False
    trPr.remove(th)
    return True


def normalizar_jerarquia_encabezados(
    documento,
    quitar_cursiva_nivel2: bool = True,
    nivel3_estilo: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Retira la cursiva accidental de los encabezados de nivel 2 (w:outlineLvl=2)
    y, opcionalmente, asigna un estilo a los de nivel 3. Por defecto no se asigna
    estilo porque 'Heading 3' arrastra color azul ajeno a la norma UNAJMA.
    """
    nivel2: List[int] = []
    nivel3: List[int] = []
    for i, p in enumerate(documento.paragraphs):
        pPr = p._p.find(_qn("w:pPr"))
        if pPr is None:
            continue
        ol = pPr.find(_qn("w:outlineLvl"))
        if ol is None:
            continue
        valor = ol.get(_qn("w:val"))
        if valor == "2":
            nivel2.append(i)
        elif valor == "3":
            nivel3.append(i)
    quitados = 0
    if quitar_cursiva_nivel2:
        for i in nivel2:
            for r in _runs_en_parrafo(documento.paragraphs[i]._p):
                rPr = r.find(_qn("w:rPr"))
                if rPr is not None and rPr.find(_qn("w:i")) is not None:
                    _rpr_propiedad(rPr, "i", False)
                    _rpr_propiedad(rPr, "iCs", False)
                    quitados += 1
    estilizados = 0
    if nivel3_estilo:
        for i in nivel3:
            p = documento.paragraphs[i]
            if p.style is None or p.style.name != nivel3_estilo:
                p.style = documento.styles[nivel3_estilo]
                estilizados += 1
    return {
        "nivel2": len(nivel2),
        "nivel3": len(nivel3),
        "cursivas_retiradas": quitados,
        "nivel3_estilizados": estilizados,
        "indices_nivel3": nivel3,
    }


def ajustar_estilo_indice(
    documento,
    nombre_estilo: str = "table of figures",
    line: int = 240,
) -> Dict[str, Any]:
    """Fija el interlineado del estilo del índice de figuras sin tocar fuente ni tamaño."""
    from docx.oxml import OxmlElement

    estilo = documento.styles[nombre_estilo]
    pPr = estilo.element.find(_qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        estilo.element.append(pPr)
    spacing = pPr.find(_qn("w:spacing"))
    if spacing is None:
        spacing = OxmlElement("w:spacing")
        pPr.append(spacing)
    anterior = spacing.get(_qn("w:line"))
    spacing.set(_qn("w:line"), str(line))
    spacing.set(_qn("w:lineRule"), "auto")
    return {"estilo": nombre_estilo, "line_anterior": anterior, "line_nuevo": line}


def reemplazar_en_hipervinculos(
    documento,
    indice: int,
    viejo: str,
    nuevo: str,
    ocurrencias: int = 1,
) -> Dict[str, Any]:
    """Sustituye texto dentro de w:hyperlink (entradas de índice con runs=0)."""
    p = documento.paragraphs[indice]._p
    aplicadas = 0
    for t in p.iter(_qn("w:t")):
        if not t.text or viejo not in t.text:
            continue
        t.text = t.text.replace(viejo, nuevo, ocurrencias)
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        aplicadas += 1
        if aplicadas >= ocurrencias:
            break
    return {"indice_docx": indice, "aplicadas": aplicadas, "estado": "aplicada" if aplicadas else "fallida"}


def anexar_filas_tabla(
    documento,
    indice_tabla: int,
    filas: Sequence[Sequence[str]],
) -> Dict[str, Any]:
    """Añade filas nativas clonando la última fila de datos (conserva tcPr, fuente y cantSplit)."""
    from copy import deepcopy

    tabla = documento.tables[indice_tabla]
    modelo = tabla.rows[-1]._tr
    creadas: List[List[str]] = []
    for valores in filas:
        nuevo = deepcopy(modelo)
        trPr = nuevo.find(_qn("w:trPr"))
        if trPr is not None:
            th = trPr.find(_qn("w:tblHeader"))
            if th is not None:
                trPr.remove(th)
        _preparar_tr(nuevo, cant_split=True, tbl_header=False)
        celdas = nuevo.findall(_qn("w:tc"))
        for tc, valor in zip(celdas, valores):
            _fijar_texto_celda(tc, str(valor))
        modelo.addnext(nuevo)
        modelo = nuevo
        creadas.append([str(v) for v in valores])
    return {"tabla": indice_tabla, "filas_agregadas": len(creadas), "filas": creadas}


def insertar_prefijo_notas_especificas(documento, indices: Sequence[int]) -> List[Dict[str, Any]]:
    """Antepone «Nota.» en cursiva a las notas indicadas que carezcan del prefijo."""
    from docx.oxml import OxmlElement

    acciones: List[Dict[str, Any]] = []
    for indice in indices:
        if not 0 <= indice < len(documento.paragraphs):
            acciones.append({"parrafo": indice, "estado": "fuera_de_rango"})
            continue
        p = documento.paragraphs[indice]._p
        texto = _texto_parrafo(p).strip()
        if not texto or texto.startswith("Nota."):
            acciones.append({"parrafo": indice, "estado": "sin_cambio"})
            continue
        tamanos = set()
        for run in p.iter(_qn("w:r")):
            rPr = run.find(_qn("w:rPr"))
            if rPr is not None and rPr.find(_qn("w:sz")) is not None:
                tamanos.add(rPr.find(_qn("w:sz")).get(_qn("w:val")))
        tamano = sorted(tamanos)[0] if tamanos else "19"
        prefijo = OxmlElement("w:r")
        rPr = OxmlElement("w:rPr")
        fuentes = OxmlElement("w:rFonts")
        for atributo in ("w:ascii", "w:hAnsi", "w:cs"):
            fuentes.set(_qn(atributo), "Times New Roman")
        rPr.append(fuentes)
        rPr.append(OxmlElement("w:i"))
        sz = OxmlElement("w:sz")
        sz.set(_qn("w:val"), tamano)
        rPr.append(sz)
        szcs = OxmlElement("w:szCs")
        szcs.set(_qn("w:val"), tamano)
        rPr.append(szcs)
        prefijo.append(rPr)
        t = OxmlElement("w:t")
        t.text = "Nota. "
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        prefijo.append(t)
        pPr = p.find(_qn("w:pPr"))
        if pPr is not None:
            pPr.addnext(prefijo)
        else:
            p.insert(0, prefijo)
        acciones.append({"parrafo": indice, "estado": "corregido", "detalle": "prefijo Nota. insertado"})
    return acciones


def blindar_todas_las_tablas(documento) -> Dict[str, Any]:
    """Erradica w:tblpPr y garantiza cantSplit, tblHeader y tres líneas APA 7."""
    from docx.oxml import OxmlElement

    acciones: List[Dict[str, Any]] = []
    for i, tabla in enumerate(documento.tables):
        flotante = eliminar_flotacion_tabla(tabla)
        for j, fila in enumerate(tabla.rows):
            _preparar_tr(fila._tr, cant_split=True, tbl_header=(j == 0))
        tblPr = tabla._tbl.tblPr
        anterior = tblPr.find(_qn("w:tblBorders"))
        if anterior is not None:
            tblPr.remove(anterior)
        bordes = OxmlElement("w:tblBorders")
        for borde in ("top", "left", "bottom", "right", "insideH", "insideV"):
            el = OxmlElement(f"w:{borde}")
            if borde in ("top", "bottom"):
                el.set(_qn("w:val"), "single")
                el.set(_qn("w:sz"), "8")
                el.set(_qn("w:space"), "0")
                el.set(_qn("w:color"), "000000")
            else:
                el.set(_qn("w:val"), "none")
                el.set(_qn("w:sz"), "0")
                el.set(_qn("w:space"), "0")
                el.set(_qn("w:color"), "auto")
            bordes.append(el)
        tblPr.insert_element_before(
            bordes,
            "w:shd",
            "w:tblLayout",
            "w:tblCellMar",
            "w:tblLook",
            "w:tblCaption",
            "w:tblDescription",
        )
        for tc in tabla.rows[0]._tr.findall(_qn("w:tc")):
            tcPr = tc.find(_qn("w:tcPr"))
            if tcPr is None:
                tcPr = OxmlElement("w:tcPr")
                tc.insert(0, tcPr)
            previos = tcPr.find(_qn("w:tcBorders"))
            if previos is not None:
                tcPr.remove(previos)
            borde_celda = OxmlElement("w:tcBorders")
            abajo = OxmlElement("w:bottom")
            abajo.set(_qn("w:val"), "single")
            abajo.set(_qn("w:sz"), "4")
            abajo.set(_qn("w:space"), "0")
            abajo.set(_qn("w:color"), "000000")
            borde_celda.append(abajo)
            tcPr.insert_element_before(
                borde_celda,
                "w:shd",
                "w:noWrap",
                "w:tcMar",
                "w:textDirection",
                "w:tcFitText",
                "w:vAlign",
                "w:hideMark",
            )
        acciones.append({"tabla": i, "flotacion_retirada": bool(flotante), "filas": len(tabla.rows)})
    return {"tablas": len(acciones), "acciones": acciones}


def actualizar_campos_docx(ruta_origen: Union[str, Path], ruta_salida: Union[str, Path],
                           solo: Optional[Sequence[str]] = None,
                           excepto_instr: Optional[Sequence[str]] = None) -> Dict[str, Any]:
    """Actualiza índices y campos nativos en una copia NUEVA; nunca guarda sobre el origen.

    ``solo`` permite actualizar únicamente ciertos tipos de campo (por ejemplo
    ``("PAGEREF", "SEQ")``) para no regenerar índices cuyo texto se compone a mano
    con el título completo del rótulo. ``excepto_instr`` excluye campos cuyo código
    contenga alguno de los fragmentos indicados, de modo que el índice general de
    contenidos se puede regenerar sin tocar los índices de figuras y tablas.
    """
    import win32com.client

    tipos = {
        "REF": 3,
        "SEQ": 12,
        "TOC": 13,
        "PAGEREF": 37,
    }
    filtro = {tipos[t.strip().upper()] for t in solo if t.strip().upper() in tipos} if solo else None
    origen = Path(ruta_origen).resolve()
    salida = Path(ruta_salida).resolve()
    seguridad.asegurar_no_sobrescribe(origen, salida)
    seguridad.asegurar_escritura_permitida(salida)
    if Path(str(salida).replace(salida.name, "~$" + salida.name)).exists():
        raise PermissionError(f"[SEGURIDAD BLOQUEADA] Existe un archivo de bloqueo para '{salida}'.")
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = None
    paginas = None
    actualizados = 0
    omitidos = 0
    try:
        doc = word.Documents.Open(str(origen), ReadOnly=False, AddToRecentFiles=False)
        # Los índices de figuras y tablas pueden ser campos TOC fuera de
        # TablesOfContents; se actualizan explícitamente y se repagina hasta
        # estabilizar los folios.
        if filtro is None:
            for _ in range(3):
                doc.Fields.Update()
                for i in range(1, doc.TablesOfContents.Count + 1):
                    doc.TablesOfContents(i).Update()
                for i in range(1, doc.Fields.Count + 1):
                    campo = doc.Fields(i)
                    if campo.Type == 13:  # wdFieldTOC
                        campo.Update()
                doc.Repaginate()
        else:
            # Actualización ordenada por dependencia: primero los campos que no
            # alteran la paginación (REF, SEQ), después el índice general —cuya
            # regeneración sí desplaza páginas— y al final las referencias de
            # página, ya con la paginación estabilizada. Se reenumera la colección
            # en cada fase porque la actualización de un índice recrea su contenido.
            def _actualizar_tipos(tipos: set) -> tuple:
                aplicados = 0
                descartados = 0
                total = doc.Fields.Count
                for indice in range(1, total + 1):
                    try:
                        campo = doc.Fields(indice)
                        tipo_campo = campo.Type
                        if tipo_campo not in tipos:
                            continue
                        if excepto_instr:
                            try:
                                codigo = campo.Code.Text
                            except Exception:  # noqa: BLE001
                                codigo = ""
                            if any(fragmento in codigo for fragmento in excepto_instr):
                                descartados += 1
                                continue
                        campo.Update()
                        aplicados += 1
                    except Exception:  # noqa: BLE001
                        continue
                return aplicados, descartados

            def _actualizar_indice_general() -> tuple:
                """Regenera el índice de contenidos a partir de los encabezados.

                ``Field.Update`` sobre un campo TOC informa éxito pero no reconstruye
                las entradas; la regeneración real la ejecuta el objeto
                ``TablesOfContents``. Los índices de ilustraciones (``TOC \\c``) no
                figuran en esa colección y quedan intactos, de modo que sus entradas
                —compuestas con el título completo del rótulo— no se sobrescriben.
                """
                aplicados = 0
                descartados = 0
                total = doc.TablesOfContents.Count
                for indice in range(1, total + 1):
                    try:
                        indice_toc = doc.TablesOfContents(indice)
                        if excepto_instr:
                            try:
                                codigo = indice_toc.Range.Fields(1).Code.Text
                            except Exception:  # noqa: BLE001
                                codigo = ""
                            if any(fragmento in codigo for fragmento in excepto_instr):
                                descartados += 1
                                continue
                        indice_toc.Update()
                        aplicados += 1
                    except Exception:  # noqa: BLE001
                        continue
                return aplicados, descartados

            n_ref, o_ref = _actualizar_tipos({3, 12})
            n_toc, o_toc = _actualizar_indice_general()
            if n_toc:
                doc.Repaginate()
            n_pag, o_pag = _actualizar_tipos({37})
            doc.Repaginate()
            actualizados = n_ref + n_toc + n_pag
            omitidos = o_ref + o_toc + o_pag
        paginas = int(doc.ComputeStatistics(2))
        doc.SaveAs2(str(salida), FileFormat=16, AddToRecentFiles=False)
    finally:
        if doc is not None:
            doc.Close(SaveChanges=0)
        word.Quit()
    return {
        "origen": str(origen),
        "salida": str(salida),
        "sha256_origen": seguridad.sha256_archivo(origen),
        "sha256_salida": seguridad.sha256_archivo(salida),
        "paginas": paginas,
        "campos_actualizados": actualizados,
        "campos_omitidos": omitidos,
        "filtro": list(solo) if solo else "todos",
        "excepto_instr": list(excepto_instr) if excepto_instr else None,
    }


def _medir_pdf_imagenes(ruta_pdf: Union[str, Path]) -> Dict[str, Any]:
    """Mide páginas, rectángulo y resolución efectiva de las imágenes incrustadas del PDF."""
    import statistics

    import pymupdf

    pdf = pymupdf.open(str(ruta_pdf))
    try:
        resoluciones: List[float] = []
        for pagina in pdf:
            for imagen in pagina.get_images(full=True):
                xref = imagen[0]
                info = pdf.extract_image(xref)
                ancho_px = int(info.get("width") or 0)
                if not ancho_px:
                    continue
                for rect in pagina.get_image_rects(xref):
                    if rect.width:
                        resoluciones.append(ancho_px / (rect.width / 72.0))
        return {
            "paginas": pdf.page_count,
            "rect_primera": [round(pdf[0].rect.width, 2), round(pdf[0].rect.height, 2)],
            "imagenes": len(resoluciones),
            "dpi_min": round(min(resoluciones), 1) if resoluciones else None,
            "dpi_mediana": round(statistics.median(resoluciones), 1) if resoluciones else None,
            "dpi_max": round(max(resoluciones), 1) if resoluciones else None,
        }
    finally:
        pdf.close()


def exportar_docx_a_pdf(
    ruta_docx: Union[str, Path],
    ruta_pdf: Optional[Union[str, Path]] = None,
    actualizar_campos: bool = False,
    calidad_imagen: bool = True,
) -> Dict[str, Any]:
    """
    Exporta a PDF con Word COM. Con ``calidad_imagen`` intenta primero
    ExportAsFixedFormat2(..., OptimizeForImageQuality=True) para conservar la
    resolución original; si Word no lo admite, cae a ExportAsFixedFormat sin
    alterar el comportamiento anterior.
    """
    import win32com.client

    docx = Path(ruta_docx).resolve()
    pdf = Path(ruta_pdf).resolve() if ruta_pdf else docx.with_suffix(".pdf")
    seguridad.asegurar_escritura_permitida(pdf)
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = None
    paginas = None
    metodo = None
    calidad_aplicada = False
    try:
        doc = word.Documents.Open(str(docx), ReadOnly=True, AddToRecentFiles=False)
        if actualizar_campos:
            doc.Fields.Update()
            for i in range(1, doc.TablesOfContents.Count + 1):
                doc.TablesOfContents(i).Update()
        if calidad_imagen:
            try:
                doc.ExportAsFixedFormat2(
                    OutputFileName=str(pdf),
                    ExportFormat=17,
                    OpenAfterExport=False,
                    OptimizeFor=0,
                    Range=0,
                    Item=0,
                    IncludeDocProps=True,
                    KeepIRM=True,
                    CreateBookmarks=0,
                    DocStructureTags=True,
                    BitmapMissingFonts=True,
                    UseISO19005_1=False,
                    OptimizeForImageQuality=True,
                )
                metodo = "ExportAsFixedFormat2"
                calidad_aplicada = True
            except Exception:
                if pdf.exists():
                    pdf.unlink()
                doc.ExportAsFixedFormat(
                    OutputFileName=str(pdf),
                    ExportFormat=17,
                    OpenAfterExport=False,
                    OptimizeFor=0,
                    Range=0,
                    Item=0,
                    IncludeDocProps=True,
                    KeepIRM=True,
                    CreateBookmarks=0,
                    DocStructureTags=True,
                    BitmapMissingFonts=True,
                    UseISO19005_1=False,
                )
                metodo = "ExportAsFixedFormat"
                calidad_aplicada = False
        else:
            doc.ExportAsFixedFormat(
                OutputFileName=str(pdf),
                ExportFormat=17,
                OpenAfterExport=False,
                OptimizeFor=0,
                Range=0,
                Item=0,
                IncludeDocProps=True,
                KeepIRM=True,
                CreateBookmarks=0,
                DocStructureTags=True,
                BitmapMissingFonts=True,
                UseISO19005_1=False,
            )
            metodo = "ExportAsFixedFormat"
        paginas = int(doc.ComputeStatistics(2))
    finally:
        if doc is not None:
            doc.Close(SaveChanges=0)
        word.Quit()
    medicion = _medir_pdf_imagenes(pdf) if pdf.exists() else {}
    return {
        "docx": str(docx),
        "pdf": str(pdf),
        "metodo_exportacion": metodo,
        "optimize_for_image_quality": calidad_aplicada,
        "paginas": paginas,
        "medicion_pdf": medicion,
        "sha256_docx": seguridad.sha256_archivo(docx),
        "sha256_pdf": seguridad.sha256_archivo(pdf) if pdf.exists() else None,
    }


def _hash_perceptual(blob: bytes) -> Tuple[int, Tuple[int, int]]:
    """Calcula un aHash de 64 bits y las dimensiones en píxeles de una imagen."""
    import io

    from PIL import Image

    with Image.open(io.BytesIO(blob)) as imagen:
        ancho, alto = imagen.size
        gris = imagen.convert("L").resize((8, 8), Image.Resampling.LANCZOS)
        pixeles = list(gris.getdata())
    promedio = sum(pixeles) / len(pixeles)
    bits = 0
    for pixel in pixeles:
        bits = (bits << 1) | (1 if pixel >= promedio else 0)
    return bits, (ancho, alto)


def _distancia_hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def _mae_visual(a: bytes, b: bytes, lado: int = 32) -> float:
    """Error absoluto medio entre dos imágenes reducidas al mismo tamaño (solo comparación)."""
    import io

    from PIL import Image

    with Image.open(io.BytesIO(a)) as ia, Image.open(io.BytesIO(b)) as ib:
        ga = list(ia.convert("L").resize((lado, lado), Image.Resampling.BILINEAR).getdata())
        gb = list(ib.convert("L").resize((lado, lado), Image.Resampling.BILINEAR).getdata())
    return sum(abs(x - y) for x, y in zip(ga, gb)) / float(lado * lado)


def _aspecto_compatible(ratio_a: float, ratio_b: float, tolerancia: float = 0.05) -> bool:
    """Comprueba proporciones compatibles con tolerancia relativa."""
    if not ratio_a or not ratio_b:
        return False
    return abs(ratio_a - ratio_b) / max(ratio_a, ratio_b) <= tolerancia


def _podar_imagenes_no_dibujadas(pdf) -> int:
    """
    Elimina de los recursos de página las copias internas de imagen que
    `replace_image` deja sin dibujar. No altera el contenido visible: solo
    quita entradas cuyo nombre no aparece en ningún operador `Do`.
    """
    quitados = 0
    for pagina in pdf:
        try:
            contenido = pagina.read_contents().decode("latin-1")
        except (RuntimeError, ValueError):
            continue
        usados = set(re.findall(r"/([A-Za-z0-9]+)\s+Do", contenido))
        tipo, valor = pdf.xref_get_key(pagina.xref, "Resources/XObject")
        if tipo != "dict":
            continue
        for nombre in re.findall(r"/([A-Za-z0-9]+)\s+\d+ 0 R", valor):
            if nombre.startswith("fzImg") and nombre not in usados:
                pdf.xref_set_key(pagina.xref, "Resources/XObject/" + nombre, "null")
                quitados += 1
    return quitados


def reparar_imagenes_pdf(
    ruta_docx: Union[str, Path],
    ruta_pdf: Union[str, Path],
    ruta_salida: Union[str, Path],
    umbral_hamming: int = 10,
) -> Dict[str, Any]:
    """
    Repara la resolución de las imágenes del PDF reemplazando cada objeto de
    imagen por el blob original del DOCX, sin rasterizar páginas ni tocar texto.
    """
    import docx
    import pymupdf

    docx_path = Path(ruta_docx).resolve()
    pdf_origen = Path(ruta_pdf).resolve()
    pdf_salida = Path(ruta_salida).resolve()
    seguridad.asegurar_escritura_permitida(pdf_salida)
    if pdf_origen != pdf_salida:
        seguridad.asegurar_no_sobrescribe(pdf_origen, pdf_salida)

    documento = docx.Document(str(docx_path))
    candidatos: List[Dict[str, Any]] = []
    for el in documento.element.body.iter():
        if el.tag != _qn("a:blip"):
            continue
        rid = el.get(_qn("r:embed"))
        if not rid:
            continue
        parte = documento.part.related_parts[rid]
        blob = parte.blob
        bits, (ancho, alto) = _hash_perceptual(blob)
        candidatos.append(
            {
                "orden": len(candidatos),
                "blob": blob,
                "hash": bits,
                "ancho": ancho,
                "alto": alto,
                "ratio": ancho / alto if alto else 0.0,
                "sha256": hashlib.sha256(blob).hexdigest(),
            }
        )

    pdf = pymupdf.open(str(pdf_origen))
    textos_antes = [pagina.get_text("text") for pagina in pdf]
    geometria_antes = [(round(p.rect.width, 2), round(p.rect.height, 2)) for p in pdf]
    ocurrencias: List[Dict[str, Any]] = []
    for numero, pagina in enumerate(pdf, start=1):
        for imagen in pagina.get_images(full=True):
            xref = imagen[0]
            for rect in pagina.get_image_rects(xref):
                ocurrencias.append({"pagina": numero, "xref": xref, "rect": tuple(rect)})

    usados: set = set()
    asignaciones: List[Dict[str, Any]] = []
    for ocurrencia in ocurrencias:
        ref = pdf.extract_image(ocurrencia["xref"])
        bits_ref, (ancho_ref, alto_ref) = _hash_perceptual(ref["image"])
        ancho_rect = ocurrencia["rect"][2] - ocurrencia["rect"][0]
        alto_rect = ocurrencia["rect"][3] - ocurrencia["rect"][1]
        ratio_rect = ancho_rect / alto_rect if alto_rect else 0.0
        evaluados: List[Dict[str, Any]] = []
        for candidato in candidatos:
            if candidato["orden"] in usados:
                continue
            if not _aspecto_compatible(candidato["ratio"], ratio_rect):
                continue
            evaluados.append(
                {
                    "candidato": candidato,
                    "hamming": _distancia_hamming(candidato["hash"], bits_ref),
                    "mae": _mae_visual(candidato["blob"], ref["image"]),
                }
            )
        # El MAE distingue capturas de interfaz casi idénticas donde el aHash empata;
        # el hamming actúa como filtro de plausibilidad y desempate secundario.
        evaluados.sort(key=lambda e: (e["mae"], e["hamming"], e["candidato"]["orden"]))
        elegido = None
        ambiguo = None
        if not evaluados:
            ambiguo = "sin candidato con proporción compatible"
        else:
            mejor = evaluados[0]
            segundo = evaluados[1] if len(evaluados) > 1 else None
            if mejor["hamming"] > umbral_hamming:
                ambiguo = f"hamming mínimo {mejor['hamming']} > {umbral_hamming}"
            elif mejor["mae"] > 3.0:
                ambiguo = f"MAE mínimo {mejor['mae']:.2f} > 3.0"
            elif segundo is not None:
                margen_h = segundo["hamming"] - mejor["hamming"]
                margen_mae = segundo["mae"] - mejor["mae"]
                if margen_h < 2 and margen_mae < 1.5:
                    ambiguo = (
                        f"empate visual (hamming {mejor['hamming']} vs {segundo['hamming']}; "
                        f"MAE {mejor['mae']:.2f} vs {segundo['mae']:.2f})"
                    )
            if ambiguo is None:
                elegido = mejor
        if elegido is None:
            asignaciones.append(
                {
                    "pagina": ocurrencia["pagina"],
                    "xref": ocurrencia["xref"],
                    "asignada": False,
                    "motivo": ambiguo,
                    "candidatos_compatibles": len(evaluados),
                }
            )
            continue
        candidato = elegido["candidato"]
        usados.add(candidato["orden"])
        asignaciones.append(
            {
                "pagina": ocurrencia["pagina"],
                "xref": ocurrencia["xref"],
                "orden_docx": candidato["orden"],
                "hamming": elegido["hamming"],
                "mae": round(elegido["mae"], 2),
                "ancho_px": candidato["ancho"],
                "alto_px": candidato["alto"],
                "rect": [round(v, 2) for v in ocurrencia["rect"]],
                "dpi_previo": round(ancho_ref / (ancho_rect / 72.0), 1) if ancho_rect else None,
                "asignada": True,
            }
        )
        if ancho_rect and alto_rect:
            pdf[ocurrencia["pagina"] - 1].replace_image(ocurrencia["xref"], stream=candidato["blob"])

    imagenes_podadas = _podar_imagenes_no_dibujadas(pdf)
    destino_temporal = pdf_salida.with_name(pdf_salida.stem + "_tmp.pdf")
    pdf.save(str(destino_temporal), garbage=4, deflate=True)
    pdf.close()
    if destino_temporal != pdf_salida:
        if pdf_salida.exists():
            pdf_salida.unlink()
        destino_temporal.replace(pdf_salida)

    nuevo = pymupdf.open(str(pdf_salida))
    textos_despues = [pagina.get_text("text") for pagina in nuevo]
    geometria_despues = [(round(p.rect.width, 2), round(p.rect.height, 2)) for p in nuevo]
    actuales_por_pagina: Dict[int, List[Tuple[int, Tuple[float, float, float, float]]]] = {}
    for numero, pagina in enumerate(nuevo, start=1):
        lista = []
        for imagen in pagina.get_images(full=True):
            try:
                for rect in pagina.get_image_rects(imagen[0]):
                    lista.append((imagen[0], tuple(rect)))
            except (ValueError, RuntimeError):
                continue
        actuales_por_pagina[numero] = lista
    resoluciones: List[Dict[str, Any]] = []
    for asignacion in asignaciones:
        if not asignacion.get("asignada"):
            continue
        rect_objetivo = asignacion["rect"]
        elegido = None
        for xref, rect in actuales_por_pagina.get(asignacion["pagina"], []):
            distancia = sum(abs(rect[i] - rect_objetivo[i]) for i in range(4))
            if distancia <= 2.0:
                elegido = (xref, rect)
                break
        if elegido is None:
            continue
        xref, rect = elegido
        ancho_px = int(nuevo.extract_image(xref)["width"])
        if rect[2]:
            resoluciones.append(
                {
                    "pagina": asignacion["pagina"],
                    "xref": xref,
                    "dpi": round(ancho_px / ((rect[2] - rect[0]) / 72.0), 1),
                    "rect_igual": True,
                }
            )
    dpi_valores = [r["dpi"] for r in resoluciones]
    nuevo.close()
    return {
        "docx": str(docx_path),
        "pdf_origen": str(pdf_origen),
        "pdf_salida": str(pdf_salida),
        "candidatos_docx": len(candidatos),
        "ocurrencias_pdf": len(ocurrencias),
        "asignadas": sum(1 for a in asignaciones if a.get("asignada")),
        "sin_asignar": [a for a in asignaciones if not a.get("asignada")],
        "texto_identico": textos_antes == textos_despues,
        "geometria_identica": geometria_antes == geometria_despues,
        "paginas": len(textos_despues),
        "dpi_min": min(dpi_valores) if dpi_valores else None,
        "dpi_mediana": sorted(dpi_valores)[len(dpi_valores) // 2] if dpi_valores else None,
        "dpi_max": max(dpi_valores) if dpi_valores else None,
        "rects_identicos": all(r["rect_igual"] for r in resoluciones),
        "imagenes_duplicadas_podadas": imagenes_podadas,
        "asignaciones": asignaciones,
        "resoluciones": resoluciones,
        "sha256_pdf": seguridad.sha256_archivo(pdf_salida),
    }


def renderizar_paginas_pdf(
    ruta_pdf: Union[str, Path],
    paginas: Sequence[int],
    dpi: int = 150,
    salida_dir: Optional[Union[str, Path]] = None,
) -> Dict[str, Any]:
    """Renderiza páginas seleccionadas de un PDF a PNG para auditoría visual."""
    import pymupdf

    pdf = Path(ruta_pdf).resolve()
    documento = pymupdf.open(str(pdf))
    destino = Path(salida_dir) if salida_dir else pdf.parent
    destino.mkdir(parents=True, exist_ok=True)
    generadas: List[str] = []
    try:
        for numero in paginas:
            if not 1 <= int(numero) <= documento.page_count:
                continue
            pagina = documento[int(numero) - 1]
            pix = pagina.get_pixmap(dpi=dpi)
            ruta = destino / f"{pdf.stem}_p{int(numero):03d}.png"
            pix.save(str(ruta))
            generadas.append(str(ruta))
        total = documento.page_count
    finally:
        documento.close()
    return {"pdf": str(pdf), "paginas_totales": total, "dpi": dpi, "renderizadas": generadas}


def sustituir_imagen_figura(
    documento,
    indice_parrafo: int,
    ruta_imagen: Union[str, Path],
    ancho_cm: float,
    alto_cm: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Sustituye el binario de una figura por su fuente nativa, sin remuestreo, y
    ajusta el tamaño de despliegue conservando la proporción de píxeles.
    """
    import io

    from PIL import Image

    ruta = Path(ruta_imagen)
    datos = ruta.read_bytes()
    with Image.open(io.BytesIO(datos)) as imagen:
        pixeles = imagen.size
        formato = (imagen.format or "").upper()
    if formato in ("JPEG", "JPG"):
        with Image.open(io.BytesIO(datos)) as imagen:
            buffer = io.BytesIO()
            imagen.save(buffer, format="PNG", optimize=False)
            datos = buffer.getvalue()
        formato = "PNG"
    p = documento.paragraphs[indice_parrafo]._p
    espacios = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
    rId = None
    for blip in p.iter():
        if blip.tag.endswith("}blip") and blip.get(espacios):
            rId = blip.get(espacios)
            break
    if rId is None:
        raise ValueError(f"El párrafo {indice_parrafo} no contiene una imagen incrustada")
    parte = documento.part.related_parts[rId]
    anterior = len(parte.blob)
    parte._blob = datos
    if hasattr(parte, "_image"):
        parte._image = None
    proporcion = pixeles[1] / pixeles[0] if pixeles[0] else 1.0
    alto = float(alto_cm) if alto_cm is not None else ancho_cm * proporcion
    cx = int(round(ancho_cm * 360000))
    cy = int(round(alto * 360000))
    ajustados = 0
    for el in p.iter():
        if el.tag.split("}")[-1] in ("extent", "ext") and "cx" in el.attrib and "cy" in el.attrib:
            el.set("cx", str(cx))
            el.set("cy", str(cy))
            ajustados += 1
    return {
        "parrafo": indice_parrafo,
        "rId": rId,
        "archivo": str(ruta),
        "pixeles": list(pixeles),
        "ancho_cm": round(ancho_cm, 2),
        "alto_cm": round(alto, 2),
        "dpi_efectivo": round(pixeles[0] / (ancho_cm / 2.54), 1),
        "bytes_anteriores": anterior,
        "bytes_nuevos": len(datos),
        "formatos_ajustados": ajustados,
    }


def editar_formula_fraccion(
    documento,
    indice_parrafo: int,
    numerador: Sequence[str],
    denominador: Sequence[str],
    ocurrencia: int = 0,
) -> Dict[str, Any]:
    """
    Reescribe el numerador y el denominador de la primera fracción OMML
    (<m:f>) de un párrafo, conservando <m:fPr> y la tipografía Cambria Math.
    No altera la numeración de la ecuación ni inserta texto fuera de la
    fórmula. Cada elemento de las secuencias se convierte en un <m:r> propio.
    """
    from docx.oxml import OxmlElement

    if not 0 <= indice_parrafo < len(documento.paragraphs):
        raise IndexError(f"Índice de párrafo {indice_parrafo} fuera de rango")
    parrafo = documento.paragraphs[indice_parrafo]
    formulas = [e for e in parrafo._p.iter() if e.tag == f"{{{M_NS}}}oMath"]
    if ocurrencia >= len(formulas):
        return {
            "parrafo": indice_parrafo,
            "aplicado": False,
            "motivo": f"El párrafo contiene {len(formulas)} fórmulas; no existe la ocurrencia {ocurrencia}",
        }
    fraccion = formulas[ocurrencia].find(f"{{{M_NS}}}f")
    if fraccion is None:
        return {
            "parrafo": indice_parrafo,
            "aplicado": False,
            "motivo": "La fórmula no contiene una fracción <m:f>",
        }

    def _rellenar(hijo, piezas: Sequence[str]) -> int:
        for nodo in list(hijo):
            hijo.remove(nodo)
        for pieza in piezas:
            run = OxmlElement("m:r")
            rpr = OxmlElement("w:rPr")
            fuentes = OxmlElement("w:rFonts")
            fuentes.set(_qn("w:ascii"), "Cambria Math")
            fuentes.set(_qn("w:hAnsi"), "Cambria Math")
            rpr.append(fuentes)
            run.append(rpr)
            texto = OxmlElement("m:t")
            texto.text = str(pieza)
            run.append(texto)
            hijo.append(run)
        return len(piezas)

    num = fraccion.find(f"{{{M_NS}}}num")
    den = fraccion.find(f"{{{M_NS}}}den")
    if num is None or den is None:
        return {
            "parrafo": indice_parrafo,
            "aplicado": False,
            "motivo": "La fracción carece de <m:num> o <m:den>",
        }
    piezas_num = _rellenar(num, numerador)
    piezas_den = _rellenar(den, denominador)
    return {
        "parrafo": indice_parrafo,
        "aplicado": True,
        "numerador": " ".join(str(p) for p in numerador),
        "denominador": " ".join(str(p) for p in denominador),
        "runs_numerador": piezas_num,
        "runs_denominador": piezas_den,
    }


def redimensionar_figura(
    documento,
    indice_parrafo: int,
    ancho_cm: float,
) -> Dict[str, Any]:
    """Ajusta el ancho de una figura nativa conservando su proporción y su blob."""
    from docx.shared import Cm

    p = documento.paragraphs[indice_parrafo]._p
    ext = p.find(".//" + _qn("wp:extent"))
    if ext is None:
        return {"indice_parrafo": indice_parrafo, "aplicado": False, "motivo": "sin wp:extent"}
    cx, cy = int(ext.get("cx")), int(ext.get("cy"))
    nuevo_cx = int(Cm(ancho_cm))
    nuevo_cy = int(round(cy * nuevo_cx / cx)) if cx else cy
    ext.set("cx", str(nuevo_cx))
    ext.set("cy", str(nuevo_cy))
    for a_ext in p.iter(_qn("a:ext")):
        a_ext.set("cx", str(nuevo_cx))
        a_ext.set("cy", str(nuevo_cy))
    ancho_px = None
    blip = p.find(".//" + _qn("a:blip"))
    if blip is not None:
        rid = blip.get(_qn("r:embed"))
        if rid:
            try:
                import io

                from PIL import Image

                with Image.open(io.BytesIO(documento.part.related_parts[rid].blob)) as imagen:
                    ancho_px = imagen.size[0]
            except Exception:
                ancho_px = None
    dpi = round(ancho_px / (nuevo_cx / 914400), 2) if ancho_px else None
    return {
        "indice_parrafo": indice_parrafo,
        "aplicado": True,
        "ancho_anterior_cm": round(cx / 360000, 3),
        "alto_anterior_cm": round(cy / 360000, 3),
        "ancho_nuevo_cm": round(nuevo_cx / 360000, 3),
        "alto_nuevo_cm": round(nuevo_cy / 360000, 3),
        "ancho_px": ancho_px,
        "dpi": dpi,
    }


def erradicar_raya_global(documento, reemplazo: str = "No aplica") -> Dict[str, Any]:
    """Elimina U+2014 de todo texto imprimible, sin tocar U+2013 ni U+2212."""
    raya = "—"
    reemplazos = 0
    celdas = 0
    nodos = list(documento.element.body.iter(_qn("w:t")))
    for seccion in documento.sections:
        for contenedor in (
            seccion.header,
            seccion.footer,
            seccion.first_page_header,
            seccion.first_page_footer,
            seccion.even_page_header,
            seccion.even_page_footer,
        ):
            try:
                nodos.extend(contenedor._element.iter(_qn("w:t")))
            except Exception:
                continue
    for t in nodos:
        if not t.text or raya not in t.text:
            continue
        if t.text.strip() == raya:
            t.text = reemplazo
            celdas += 1
        else:
            t.text = t.text.replace(raya, ",")
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        reemplazos += 1
    restantes = sum(
        1
        for t in documento.element.body.iter(_qn("w:t"))
        if t.text and raya in t.text
    )
    return {"nodos_reemplazados": reemplazos, "celdas_placeholder": celdas, "rayas_restantes_cuerpo": restantes}


def normalizar_margenes_secciones(
    documento,
    izquierdo_cm: float = 3.0,
    derecho_cm: float = 2.5,
    superior_cm: float = 2.5,
    inferior_cm: float = 2.5,
) -> Dict[str, Any]:
    """
    Fija los márgenes de todas las secciones a la especificación UNAJMA
    (izquierdo 3.0 cm; derecho, superior e inferior 2.5 cm), conservando
    orientación, tamaño de página, gutter y distancias de encabezado/pie.
    Devuelve los valores reales antes y después y el ancho útil resultante.
    """
    from docx.shared import Cm

    objetivo = {
        "izquierdo_emu": int(Cm(izquierdo_cm)),
        "derecho_emu": int(Cm(derecho_cm)),
        "superior_emu": int(Cm(superior_cm)),
        "inferior_emu": int(Cm(inferior_cm)),
    }
    detalle: List[Dict[str, Any]] = []
    for indice, seccion in enumerate(documento.sections):
        antes = {
            "izquierdo_emu": int(seccion.left_margin or 0),
            "derecho_emu": int(seccion.right_margin or 0),
            "superior_emu": int(seccion.top_margin or 0),
            "inferior_emu": int(seccion.bottom_margin or 0),
        }
        seccion.left_margin = Cm(izquierdo_cm)
        seccion.right_margin = Cm(derecho_cm)
        seccion.top_margin = Cm(superior_cm)
        seccion.bottom_margin = Cm(inferior_cm)
        despues = {
            "izquierdo_emu": int(seccion.left_margin),
            "derecho_emu": int(seccion.right_margin),
            "superior_emu": int(seccion.top_margin),
            "inferior_emu": int(seccion.bottom_margin),
        }
        ancho_util_emu = int(seccion.page_width) - despues["izquierdo_emu"] - despues["derecho_emu"]
        detalle.append(
            {
                "seccion": indice,
                "orientacion": str(seccion.orientation),
                "ancho_pagina_emu": int(seccion.page_width),
                "alto_pagina_emu": int(seccion.page_height),
                "antes_emu": antes,
                "despues_emu": despues,
                "ancho_util_emu": ancho_util_emu,
                "ancho_util_dxa": int(round(ancho_util_emu / 635)),
                "cambio": antes != despues,
            }
        )
    return {
        "objetivo_cm": {
            "izquierdo": izquierdo_cm,
            "derecho": derecho_cm,
            "superior": superior_cm,
            "inferior": inferior_cm,
        },
        "secciones": detalle,
        "secciones_ajustadas": sum(1 for d in detalle if d["cambio"]),
    }


def aplicar_salto_pagina_previo(documento, prefijos: Sequence[str]) -> Dict[str, Any]:
    """
    Activa <w:pageBreakBefore/> en los párrafos cuyo texto comienza con alguno
    de los prefijos dados, sin insertar párrafos ni alterar el contenido. Se usa
    para que cada formato de evaluación del Anexo 3 inicie en página propia.
    """
    acciones: List[Dict[str, Any]] = []
    for indice, parrafo in enumerate(documento.paragraphs):
        texto = parrafo.text.strip()
        if not any(texto.startswith(prefijo) for prefijo in prefijos):
            continue
        if parrafo.paragraph_format.page_break_before:
            acciones.append({"parrafo": indice, "aplicado": False, "motivo": "ya tenia pageBreakBefore"})
            continue
        parrafo.paragraph_format.page_break_before = True
        acciones.append({"parrafo": indice, "aplicado": True, "texto": texto[:90]})
    return {"acciones": acciones, "aplicados": sum(1 for a in acciones if a["aplicado"])}


def _texto_tc(tc) -> str:
    """Extrae el texto de una celda conservando los saltos de párrafo."""
    parrafos = []
    for p in tc.findall(_qn("w:p")):
        parrafos.append("".join(t.text or "" for t in p.iter(_qn("w:t"))))
    return "\n".join(parrafos).strip()


def _ancho_util_tabla_dxa(tabla) -> Tuple[int, bool]:
    """Calcula el ancho útil (dxa) de la sección que contiene la tabla."""
    el = tabla._tbl
    nxt = el
    sect = None
    while nxt is not None:
        if nxt.tag == _qn("w:sectPr"):
            sect = nxt
            break
        hallado = nxt.find(".//" + _qn("w:sectPr"))
        if hallado is not None:
            sect = hallado
            break
        nxt = nxt.getnext()
    if sect is None:
        return 8788, False
    pg = sect.find(_qn("w:pgSz"))
    mar = sect.find(_qn("w:pgMar"))
    if pg is None or mar is None:
        return 8788, False
    ancho = int(pg.get(_qn("w:w")))
    alto = int(pg.get(_qn("w:h")))
    izquierdo = int(mar.get(_qn("w:left")))
    derecho = int(mar.get(_qn("w:right")))
    return ancho - izquierdo - derecho, ancho > alto


def _limpiar_tc(tc) -> None:
    """Elimina párrafos y contenido de una celda conservando su tcPr."""
    for hijo in list(tc):
        if hijo.tag != _qn("w:tcPr"):
            tc.remove(hijo)


def _celda_texto_nuevo(tc, texto: str, negrita: bool = False, tamano_medios: int = 20) -> None:
    """Escribe texto nuevo en una celda con tipografía Times New Roman."""
    from docx.oxml import OxmlElement

    _limpiar_tc(tc)
    p = OxmlElement("w:p")
    pPr = OxmlElement("w:pPr")
    jc = OxmlElement("w:jc")
    jc.set(_qn("w:val"), "left")
    pPr.append(jc)
    p.append(pPr)
    r = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    fuentes = OxmlElement("w:rFonts")
    for attr in ("w:ascii", "w:hAnsi", "w:cs"):
        fuentes.set(_qn(attr), "Times New Roman")
    rPr.append(fuentes)
    if negrita:
        b = OxmlElement("w:b")
        b.set(_qn("w:val"), "1")
        rPr.append(b)
    for etiqueta in ("w:sz", "w:szCs"):
        sz = OxmlElement(etiqueta)
        sz.set(_qn("w:val"), str(tamano_medios))
        rPr.append(sz)
    r.append(rPr)
    t = OxmlElement("w:t")
    t.text = texto
    if texto != texto.strip() or "  " in texto:
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    r.append(t)
    p.append(r)
    tc.append(p)


def _copiar_parrafos_celda(origen_tc, destino_tc) -> int:
    """Copia los párrafos de una celda origen a una celda destino (deepcopy)."""
    import copy

    _limpiar_tc(destino_tc)
    copiados = 0
    for p in origen_tc.findall(_qn("w:p")):
        nuevo = copy.deepcopy(p)
        pPr = nuevo.find(_qn("w:pPr"))
        if pPr is not None:
            tabs = pPr.find(_qn("w:tabs"))
            if tabs is not None:
                pPr.remove(tabs)
            frame = pPr.find(_qn("w:framePr"))
            if frame is not None:
                pPr.remove(frame)
        for marca in list(nuevo.iter(_qn("w:lastRenderedPageBreak"))):
            marca.getparent().remove(marca)
        pPr = nuevo.find(_qn("w:pPr"))
        if pPr is None:
            from docx.oxml import OxmlElement

            pPr = OxmlElement("w:pPr")
            nuevo.insert(0, pPr)
        jc = pPr.find(_qn("w:jc"))
        if jc is None:
            from docx.oxml import OxmlElement

            jc = OxmlElement("w:jc")
            pPr.insert_element_before(
                jc,
                "w:textDirection",
                "w:textAlignment",
                "w:textboxTightWrap",
                "w:outlineLvl",
                "w:divId",
                "w:cnfStyle",
                "w:rPr",
                "w:sectPr",
                "w:pPrChange",
            )
        jc.set(_qn("w:val"), "left")
        for run in nuevo.iter(_qn("w:r")):
            rPr = run.find(_qn("w:rPr"))
            if rPr is None:
                from docx.oxml import OxmlElement

                rPr = OxmlElement("w:rPr")
                run.insert(0, rPr)
            for etiqueta in ("w:sz", "w:szCs"):
                sz = rPr.find(_qn(etiqueta))
                if sz is None:
                    from docx.oxml import OxmlElement

                    sz = OxmlElement(etiqueta)
                    rPr.insert_element_before(
                        sz,
                        "w:u",
                        "w:effect",
                        "w:bdr",
                        "w:shd",
                        "w:fitText",
                        "w:vertAlign",
                        "w:rtl",
                        "w:cs",
                        "w:em",
                        "w:lang",
                        "w:eastAsianLayout",
                        "w:specVanish",
                        "w:oMath",
                    )
                    sz.set(_qn("w:val"), "20")
                else:
                    try:
                        if int(sz.get(_qn("w:val"))) < 20:
                            sz.set(_qn("w:val"), "20")
                    except (TypeError, ValueError):
                        sz.set(_qn("w:val"), "20")
        destino_tc.append(nuevo)
        copiados += 1
    if not destino_tc.findall(_qn("w:p")):
        from docx.oxml import OxmlElement

        destino_tc.append(OxmlElement("w:p"))
    return copiados


def _fijar_ancho_grid(tabla, anchos: Sequence[int]) -> None:
    """Fija <w:tblW> y <w:tblGrid> en dxa para una tabla nativa."""
    tbl = tabla._tbl
    tblPr = tbl.tblPr
    tblW = tblPr.find(_qn("w:tblW"))
    if tblW is None:
        from docx.oxml import OxmlElement

        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    tblW.set(_qn("w:type"), "dxa")
    tblW.set(_qn("w:w"), str(sum(anchos)))
    layout = tblPr.find(_qn("w:tblLayout"))
    if layout is None:
        from docx.oxml import OxmlElement

        layout = OxmlElement("w:tblLayout")
        tblPr.append(layout)
    layout.set(_qn("w:type"), "fixed")
    grid = tbl.find(_qn("w:tblGrid"))
    if grid is not None:
        for col, ancho in zip(grid.findall(_qn("w:gridCol")), anchos):
            col.set(_qn("w:w"), str(int(ancho)))


def reorganizar_tabla_bloques(
    documento,
    indice: int,
    etiqueta_campo: str = "Campo",
    etiqueta_valor: str = "Contenido",
    ancho_etiqueta_dxa: Optional[int] = None,
    filas_extra: Optional[Sequence[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    """
    Reorganiza una tabla nativa en dos columnas Campo/Contenido, una fila por
    cada celda fuente, conservando textualmente todo el contenido y su formato.
    """
    from docx.oxml import OxmlElement

    tabla = documento.tables[indice]
    trs = tabla._tbl.findall(_qn("w:tr"))
    if len(trs) < 2:
        return {"tabla": indice, "reorganizada": False, "motivo": "sin filas de datos"}
    encabezados = [_texto_tc(tc) or f"Campo {j + 1}" for j, tc in enumerate(trs[0].findall(_qn("w:tc")))]
    ancho_util, horizontal = _ancho_util_tabla_dxa(tabla)
    if ancho_etiqueta_dxa is None:
        ancho_etiqueta_dxa = 3200 if horizontal else 2500
    ancho_etiqueta_dxa = min(int(ancho_etiqueta_dxa), ancho_util - 1200)
    ancho_valor = ancho_util - ancho_etiqueta_dxa
    textos_origen: List[str] = []
    celdas_nuevas: List[Tuple[str, Any]] = []
    for tr in trs[1:]:
        for j, tc in enumerate(tr.findall(_qn("w:tc"))):
            etiqueta = encabezados[j] if j < len(encabezados) else f"Campo {j + 1}"
            celdas_nuevas.append((etiqueta, tc))
            textos_origen.append(_texto_tc(tc))

    nueva = documento.add_table(rows=1, cols=2)
    tabla._tbl.addprevious(nueva._tbl)
    filas_nuevas = nueva._tbl.findall(_qn("w:tr"))
    tc_izq, tc_der = filas_nuevas[0].findall(_qn("w:tc"))
    _celda_texto_nuevo(tc_izq, etiqueta_campo, negrita=True)
    _celda_texto_nuevo(tc_der, etiqueta_valor, negrita=True)

    for etiqueta, tc_origen in celdas_nuevas:
        fila = nueva.add_row()
        tcs = fila._tr.findall(_qn("w:tc"))
        _celda_texto_nuevo(tcs[0], etiqueta, negrita=True)
        _copiar_parrafos_celda(tc_origen, tcs[1])

    extras = 0
    for extra in filas_extra or []:
        for etiqueta in encabezados:
            fila = nueva.add_row()
            tcs = fila._tr.findall(_qn("w:tc"))
            _celda_texto_nuevo(tcs[0], etiqueta, negrita=True)
            _celda_texto_nuevo(tcs[1], str(extra.get(etiqueta, "")))
            extras += 1

    anchos = [ancho_etiqueta_dxa, ancho_valor]
    _fijar_ancho_grid(nueva, anchos)
    configurar_geometria_tabla(nueva, ancho_util, anchos)
    for j, fila in enumerate(nueva.rows):
        _preparar_tr(fila._tr, cant_split=True, tbl_header=(j == 0))
    _fijar_margenes_celda_tabla(nueva._tbl, 28, 28)
    tabla._tbl.getparent().remove(tabla._tbl)

    textos_nuevos = [
        _texto_tc(tc)
        for tr in nueva._tbl.findall(_qn("w:tr"))[1:]
        for tc in tr.findall(_qn("w:tc"))[1::2]
    ][: len(textos_origen)]
    return {
        "tabla_original": indice,
        "reorganizada": True,
        "filas": len(nueva.rows),
        "columnas": 2,
        "ancho_util_dxa": ancho_util,
        "ancho_etiqueta_dxa": ancho_etiqueta_dxa,
        "ancho_valor_dxa": ancho_valor,
        "orientacion": "horizontal" if horizontal else "vertical",
        "celdas_origen": len(textos_origen),
        "filas_extra": extras,
        "texto_conservado": textos_origen == textos_nuevos,
    }


def reemplazar_parrafos_completos(documento, reemplazos: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Reemplaza el texto íntegro de párrafos concretos conservando su pPr."""
    from docx.oxml import OxmlElement

    acciones: List[Dict[str, Any]] = []
    for item in reemplazos:
        indice = int(item["indice"])
        texto = str(item["texto"])
        p = documento.paragraphs[indice]._p
        pPr = p.find(_qn("w:pPr"))
        rPr = None
        primer_run = p.find(_qn("w:r"))
        if primer_run is not None:
            rPr = primer_run.find(_qn("w:rPr"))
        anterior = "".join(t.text or "" for t in p.iter(_qn("w:t")))
        for hijo in list(p):
            if hijo is pPr:
                continue
            p.remove(hijo)
        r = OxmlElement("w:r")
        if rPr is not None:
            import copy

            r.append(copy.deepcopy(rPr))
        t = OxmlElement("w:t")
        t.text = texto
        if texto != texto.strip() or "  " in texto:
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        r.append(t)
        if pPr is not None:
            pPr.addnext(r)
        else:
            p.insert(0, r)
        acciones.append({"indice": indice, "caracteres_previos": len(anterior), "caracteres_nuevos": len(texto)})
    return {"reemplazados": len(acciones), "acciones": acciones}


def eliminar_filas_tabla(documento, especificaciones: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Elimina filas nativas concretas de una tabla, de mayor a menor índice."""
    acciones: List[Dict[str, Any]] = []
    for item in especificaciones:
        tabla = documento.tables[int(item["tabla"])]
        eliminadas = []
        for indice in sorted({int(i) for i in item["filas"]}, reverse=True):
            trs = tabla._tbl.findall(_qn("w:tr"))
            if 0 <= indice < len(trs):
                trs[indice].getparent().remove(trs[indice])
                eliminadas.append(indice)
        acciones.append({"tabla": int(item["tabla"]), "filas_eliminadas": sorted(eliminadas)})
    return {"acciones": acciones}


def escribir_celdas_parrafos(documento, especificaciones: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Reescribe una celda con varios párrafos nativos (Firma/Sello/DNI)."""
    from docx.oxml import OxmlElement

    acciones: List[Dict[str, Any]] = []
    for item in especificaciones:
        tabla = documento.tables[int(item["tabla"])]
        tc = tabla.rows[int(item["fila"])].cells[int(item["columna"])]._tc
        _limpiar_tc(tc)
        for texto in item["parrafos"]:
            p = OxmlElement("w:p")
            r = OxmlElement("w:r")
            t = OxmlElement("w:t")
            t.text = str(texto)
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            r.append(t)
            p.append(r)
            tc.append(p)
        if not tc.findall(_qn("w:p")):
            tc.append(OxmlElement("w:p"))
        acciones.append(
            {
                "tabla": int(item["tabla"]),
                "fila": int(item["fila"]),
                "columna": int(item["columna"]),
                "parrafos": len(item["parrafos"]),
            }
        )
    return {"celdas": len(acciones), "acciones": acciones}


def escribir_celdas_texto(documento, especificaciones: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Reescribe el texto de celdas concretas conservando el rPr del primer run."""
    acciones: List[Dict[str, Any]] = []
    for item in especificaciones:
        tabla = documento.tables[int(item["tabla"])]
        tc = tabla.rows[int(item["fila"])].cells[int(item["columna"])]._tc
        antes = _texto_tc(tc)
        _fijar_texto_celda(tc, str(item["texto"]))
        acciones.append({"tabla": int(item["tabla"]), "fila": int(item["fila"]), "columna": int(item["columna"]), "antes": antes[:80]})
    return {"celdas": len(acciones), "acciones": acciones}


def aplicar_keep_next_ultima_fila(documento, indices: Sequence[int]) -> Dict[str, Any]:
    """Fija <w:keepNext/> solo en los párrafos de la última fila de cada tabla."""
    from docx.oxml import OxmlElement

    acciones: List[Dict[str, Any]] = []
    for indice in indices:
        tabla = documento.tables[int(indice)]
        trs = tabla._tbl.findall(_qn("w:tr"))
        if not trs:
            acciones.append({"tabla": int(indice), "aplicados": 0, "motivo": "tabla sin filas"})
            continue
        aplicados = 0
        for p in trs[-1].iter(_qn("w:p")):
            pPr = p.find(_qn("w:pPr"))
            if pPr is None:
                pPr = OxmlElement("w:pPr")
                p.insert(0, pPr)
            if pPr.find(_qn("w:keepNext")) is None:
                keep = OxmlElement("w:keepNext")
                pPr.insert_element_before(
                    keep,
                    "w:pageBreakBefore",
                    "w:framePr",
                    "w:widowControl",
                    "w:numPr",
                    "w:suppressLineNumbers",
                    "w:pBdr",
                    "w:shd",
                    "w:tabs",
                    "w:suppressAutoHyphens",
                    "w:kinsoku",
                    "w:wordWrap",
                    "w:overflowPunct",
                    "w:topLinePunct",
                    "w:autoSpaceDE",
                    "w:autoSpaceDN",
                    "w:bidi",
                    "w:adjustRightInd",
                    "w:snapToGrid",
                    "w:spacing",
                    "w:ind",
                    "w:contextualSpacing",
                    "w:mirrorIndents",
                    "w:suppressOverlap",
                    "w:jc",
                    "w:textDirection",
                    "w:textAlignment",
                    "w:textboxTightWrap",
                    "w:outlineLvl",
                    "w:divId",
                    "w:cnfStyle",
                    "w:rPr",
                    "w:sectPr",
                    "w:pPrChange",
                )
                aplicados += 1
        acciones.append({"tabla": int(indice), "aplicados": aplicados, "filas": len(trs)})
    return {"tablas": len(indices), "acciones": acciones}


# =============================================================================
# OPERACIONES DECLARADAS COMO CAPACIDADES FALTANTES (plan v21)
# =============================================================================
_ORDEN_TCW_SUCESORES = (
    "w:gridSpan",
    "w:hMerge",
    "w:vMerge",
    "w:tcBorders",
    "w:shd",
    "w:noWrap",
    "w:tcMar",
    "w:textDirection",
    "w:tcFitText",
    "w:vAlign",
    "w:hideMark",
    "w:headers",
    "w:cellIns",
    "w:cellDel",
    "w:cellMerge",
    "w:tcPrChange",
)
_ORDEN_VALIGN_SUCESORES = (
    "w:hideMark",
    "w:headers",
    "w:cellIns",
    "w:cellDel",
    "w:cellMerge",
    "w:tcPrChange",
)
_ORDEN_TABS_SUCESORES = (
    "w:suppressAutoHyphens",
    "w:kinsoku",
    "w:wordWrap",
    "w:overflowPunct",
    "w:topLinePunct",
    "w:autoSpaceDE",
    "w:autoSpaceDN",
    "w:bidi",
    "w:adjustRightInd",
    "w:snapToGrid",
    "w:spacing",
    "w:ind",
    "w:contextualSpacing",
    "w:mirrorIndents",
    "w:suppressOverlap",
    "w:jc",
    "w:textDirection",
    "w:textAlignment",
    "w:textboxTightWrap",
    "w:outlineLvl",
    "w:divId",
    "w:cnfStyle",
    "w:rPr",
    "w:sectPr",
    "w:pPrChange",
)
_PATRON_NUMERICO = re.compile(r"^[+\-−]?\s*\d[\d\s.,]*\s*%?$")
_PATRON_SUBINDICE = re.compile(
    r"(?<![A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ])"
    r"([A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)_"
    r"([A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ]+(?:[,_][A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ]+)*)"
)
# Marcador de lista al inicio de párrafo: número, letra, romano, viñeta o guion.
_PATRON_MARCADOR_LISTA = re.compile(
    r"^([  ]{0,8})(\d{1,3}[.)]|[IVXLC]{1,5}[.)]|[A-Za-z][.)]|[•▪◦‣·]|[-–—])([ \t ]+)"
)
_PATRON_ROTULO_LETRA = re.compile(r"^[A-Z][.)]$")
_ORDEN_IND_SUCESORES = (
    "w:contextualSpacing",
    "w:mirrorIndents",
    "w:suppressOverlap",
    "w:jc",
    "w:textDirection",
    "w:textAlignment",
    "w:textboxTightWrap",
    "w:outlineLvl",
    "w:divId",
    "w:cnfStyle",
    "w:rPr",
    "w:sectPr",
    "w:pPrChange",
)


def _anchos_grid_tabla(tabla) -> List[int]:
    """Devuelve los anchos declarados en <w:tblGrid>."""
    grid = tabla._tbl.find(_qn("w:tblGrid"))
    if grid is None:
        return []
    return [int(col.get(_qn("w:w")) or 0) for col in grid.findall(_qn("w:gridCol"))]


def _margenes_tabla(tabla) -> Dict[str, int]:
    """Lee los márgenes laterales y verticales declarados en <w:tblCellMar>."""
    valores = {"left": 108, "right": 108, "top": 0, "bottom": 0}
    mar = tabla._tbl.tblPr.find(_qn("w:tblCellMar")) if tabla._tbl.tblPr is not None else None
    if mar is None:
        return valores
    for lado in ("left", "right", "top", "bottom"):
        nodo = mar.find(_qn(f"w:{lado}"))
        if nodo is not None and nodo.get(_qn("w:w")) is not None:
            valores[lado] = int(nodo.get(_qn("w:w")))
    return valores


def _alto_estimado_tabla(tabla) -> Dict[str, Any]:
    """Estima el alto de una tabla midiendo el texto real de cada celda.

    Es un estimador interno y relativo: sirve para comparar antes/después con el
    mismo criterio, no para predecir la paginación exacta de Word.
    """
    import math

    anchos = _anchos_grid_tabla(tabla)
    margenes = _margenes_tabla(tabla)
    total = 0.0
    filas: List[float] = []
    for tr in tabla._tbl.findall(_qn("w:tr")):
        tcs = tr.findall(_qn("w:tc"))
        alto_fila = 0.0
        for j, tc in enumerate(tcs):
            ancho = anchos[j] if j < len(anchos) else (sum(anchos) // max(1, len(tcs)))
            disponible = max(1, ancho - margenes["left"] - margenes["right"])
            lineas = 0
            for p in tc.iter(_qn("w:p")):
                texto = "".join(t.text or "" for t in p.iter(_qn("w:t")))
                if not texto.strip():
                    lineas += 1
                    continue
                ancho_pt = _ancho_texto_dxa(texto, 10.0)
                if ancho_pt is None:
                    ancho_pt = len(texto) * 5.0 * 20.0
                lineas += max(1, math.ceil(ancho_pt / disponible))
            alto_celda = lineas * 11.5 + (margenes["top"] + margenes["bottom"]) / 20.0
            alto_fila = max(alto_fila, alto_celda)
        total += alto_fila
        filas.append(round(alto_fila, 1))
    return {
        "alto_estimado_pt": round(total, 1),
        "filas_pt": filas,
        "metodo": "ancho medido con metricas Times New Roman a 10 pt; 11,5 pt por linea",
    }


def aplicar_geometria_proporcional(
    documento,
    indice_tabla: int,
    anchos_dxa: Sequence[int],
    margen_dxa: int = 60,
    solo_verificar: bool = False,
) -> Dict[str, Any]:
    """Fija tblLayout fijo, tblW, gridCol y tcW coherentes y proporcionales.

    Los anchos se reciben ya calculados por el plan; la operación garantiza que
    la suma declarada coincida con la suma real de columnas y que ninguna quede
    por debajo del margen de celda indicado.
    """
    from docx.oxml import OxmlElement

    indice = int(indice_tabla)
    if indice < 0 or indice >= len(documento.tables):
        return {"tabla": indice, "estado": "fallida", "motivo": "índice de tabla fuera de rango"}
    tabla = documento.tables[indice]
    actuales = _anchos_grid_tabla(tabla)
    nuevos = [int(a) for a in anchos_dxa]
    if len(nuevos) != len(actuales):
        return {
            "tabla": indice,
            "estado": "fallida",
            "motivo": f"se esperaban {len(actuales)} anchos y se recibieron {len(nuevos)}",
        }
    if any(a <= 2 * int(margen_dxa) for a in nuevos):
        return {
            "tabla": indice,
            "estado": "fallida",
            "motivo": "algún ancho no deja espacio útil tras descontar el margen de celda",
        }
    horizontal = sum(actuales) > 8788
    limite = 14000 if horizontal else 8788
    if sum(nuevos) > limite:
        return {
            "tabla": indice,
            "estado": "fallida",
            "motivo": f"la suma {sum(nuevos)} dxa excede el límite institucional {limite} dxa",
        }

    resultado = {
        "tabla": indice,
        "estado": "aplicable" if solo_verificar else "aplicada",
        "anchos_antes": actuales,
        "anchos_despues": nuevos,
        "suma_dxa": sum(nuevos),
        "margen_dxa": int(margen_dxa),
        "orientacion": "horizontal" if horizontal else "vertical",
    }
    if solo_verificar:
        return resultado

    tbl = tabla._tbl
    tblPr = tbl.tblPr
    tblW = tblPr.find(_qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.insert_element_before(
            tblW,
            "w:jc",
            "w:tblCellSpacing",
            "w:tblInd",
            "w:tblBorders",
            "w:shd",
            "w:tblLayout",
            "w:tblCellMar",
            "w:tblLook",
            "w:tblCaption",
            "w:tblDescription",
            "w:tblPrChange",
        )
    tblW.set(_qn("w:type"), "dxa")
    tblW.set(_qn("w:w"), str(sum(nuevos)))

    layout = tblPr.find(_qn("w:tblLayout"))
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tblPr.insert_element_before(
            layout,
            "w:tblCellMar",
            "w:tblLook",
            "w:tblCaption",
            "w:tblDescription",
            "w:tblPrChange",
        )
    layout.set(_qn("w:type"), "fixed")

    grid = tbl.find(_qn("w:tblGrid"))
    if grid is not None:
        for col, ancho in zip(grid.findall(_qn("w:gridCol")), nuevos):
            col.set(_qn("w:w"), str(ancho))

    corregidas = 0
    for tr in tbl.findall(_qn("w:tr")):
        columna = 0
        for tc in tr.findall(_qn("w:tc")):
            tcPr = tc.find(_qn("w:tcPr"))
            if tcPr is None:
                tcPr = OxmlElement("w:tcPr")
                tc.insert(0, tcPr)
            span = tcPr.find(_qn("w:gridSpan"))
            span_val = int(span.get(_qn("w:val")) or 1) if span is not None else 1
            ancho = sum(nuevos[columna : columna + span_val])
            tcW = tcPr.find(_qn("w:tcW"))
            if tcW is None:
                tcW = OxmlElement("w:tcW")
                tcPr.insert_element_before(tcW, *_ORDEN_TCW_SUCESORES)
            tcW.set(_qn("w:type"), "dxa")
            tcW.set(_qn("w:w"), str(ancho))
            corregidas += 1
            columna += max(1, span_val)
    resultado["celdas_tcw"] = corregidas
    return resultado


def aplicar_valign(
    documento,
    indice_tabla: int,
    valor: str = "top",
    excepto_encabezado: bool = True,
    solo_verificar: bool = False,
) -> Dict[str, Any]:
    """Fija <w:vAlign> en las celdas de una tabla (por defecto, top)."""
    from docx.oxml import OxmlElement

    if valor not in ("top", "center", "bottom"):
        return {"tabla": int(indice_tabla), "estado": "fallida", "motivo": f"valor no válido: {valor}"}
    indice = int(indice_tabla)
    if indice < 0 or indice >= len(documento.tables):
        return {"tabla": indice, "estado": "fallida", "motivo": "índice de tabla fuera de rango"}
    tabla = documento.tables[indice]
    tcs = []
    for posicion, tr in enumerate(tabla._tbl.findall(_qn("w:tr"))):
        if posicion == 0 and excepto_encabezado:
            continue
        tcs.extend(tr.findall(_qn("w:tc")))
    if not tcs:
        return {"tabla": indice, "estado": "omitida", "motivo": "tabla sin celdas de cuerpo"}

    resultado = {
        "tabla": indice,
        "estado": "aplicable" if solo_verificar else "aplicada",
        "valor": valor,
        "excepto_encabezado": bool(excepto_encabezado),
        "celdas": len(tcs),
    }
    if solo_verificar:
        return resultado

    modificadas = 0
    for tc in tcs:
        tcPr = tc.find(_qn("w:tcPr"))
        if tcPr is None:
            tcPr = OxmlElement("w:tcPr")
            tc.insert(0, tcPr)
        vAlign = tcPr.find(_qn("w:vAlign"))
        if vAlign is None:
            vAlign = OxmlElement("w:vAlign")
            tcPr.insert_element_before(vAlign, *_ORDEN_VALIGN_SUCESORES)
        if vAlign.get(_qn("w:val")) != valor:
            vAlign.set(_qn("w:val"), valor)
        modificadas += 1
    resultado["celdas_modificadas"] = modificadas
    return resultado


def _fijar_tabulador_decimal(p, posicion_dxa: int) -> bool:
    """Inyecta un tabulador decimal nativo en el párrafo y alinea a la izquierda."""
    from docx.oxml import OxmlElement

    pPr = p.find(_qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        p.insert(0, pPr)
    tabs = pPr.find(_qn("w:tabs"))
    if tabs is None:
        tabs = OxmlElement("w:tabs")
        pPr.insert_element_before(tabs, *_ORDEN_TABS_SUCESORES)
    tab = None
    for candidato in tabs.findall(_qn("w:tab")):
        if candidato.get(_qn("w:val")) == "decimal":
            tab = candidato
            break
    if tab is None:
        tab = OxmlElement("w:tab")
        tab.set(_qn("w:val"), "decimal")
        tabs.append(tab)
    tab.set(_qn("w:pos"), str(int(posicion_dxa)))
    jc = pPr.find(_qn("w:jc"))
    if jc is None:
        jc = OxmlElement("w:jc")
        pPr.insert_element_before(
            jc,
            "w:textDirection",
            "w:textAlignment",
            "w:textboxTightWrap",
            "w:outlineLvl",
            "w:divId",
            "w:cnfStyle",
            "w:rPr",
            "w:sectPr",
            "w:pPrChange",
        )
    jc.set(_qn("w:val"), "left")
    return True


def _insertar_tabulador_inicial(p) -> bool:
    """Inserta un run con <w:tab/> al inicio del párrafo si aún no lo tiene."""
    from docx.oxml import OxmlElement

    primer_run = None
    for hijo in p:
        if hijo.tag == _qn("w:r"):
            primer_run = hijo
            break
    if primer_run is not None:
        if primer_run.find(_qn("w:tab")) is not None:
            return False
    run = OxmlElement("w:r")
    # El run del tabulador no imprime glifo: se fija a 1 pt para que la línea
    # técnica del tabulador no incremente el alto de la fila ni desplace el valor.
    rPr = OxmlElement("w:rPr")
    for etiqueta in ("w:sz", "w:szCs"):
        nodo = OxmlElement(etiqueta)
        nodo.set(_qn("w:val"), "2")
        rPr.append(nodo)
    run.append(rPr)
    run.append(OxmlElement("w:tab"))
    if primer_run is not None:
        primer_run.addprevious(run)
    else:
        p.append(run)
    return True


def _colocar_numero_en_tabulador_decimal(p, posicion_dxa: int) -> bool:
    """Alinea el número completo con una parada de tabulador decimal nativa.

    El tabulador se inserta al inicio del párrafo y el número entero queda
    después de él, de modo que Word alinea el separador decimal en la parada y
    distribuye la parte entera a la izquierda y la cola decimal a la derecha.
    No debe insertarse un tabulador entre la parte entera y la cola: Word solo
    desplaza el texto posterior al tabulador, lo que produciría un hueco visible
    del tipo «38 .5».
    """
    if not _insertar_tabulador_inicial(p):
        _quitar_tabulador_decimal(p)
        if not _insertar_tabulador_inicial(p):
            return False
    _fijar_tabulador_decimal(p, int(posicion_dxa))
    _fijar_justificacion_parrafo(p, "left")
    return True


def _quitar_tabulador_decimal(p) -> bool:
    """Retira el tabulador decimal y el run de tabulación inicial de un párrafo.

    Se usa cuando una columna no admite tabulación decimal y debe degradarse a
    alineación derecha: dejar el tabulador produciría el mismo corte del número.
    """
    retirado = False
    pPr = p.find(_qn("w:pPr"))
    if pPr is not None:
        tabs = pPr.find(_qn("w:tabs"))
        if tabs is not None:
            for tab in list(tabs.findall(_qn("w:tab"))):
                if tab.get(_qn("w:val")) == "decimal":
                    tabs.remove(tab)
                    retirado = True
            if not tabs.findall(_qn("w:tab")):
                pPr.remove(tabs)
    for r in list(p.findall(_qn("w:r"))):
        if r.find(_qn("w:t")) is not None:
            break
        if r.find(_qn("w:tab")) is not None:
            p.remove(r)
            retirado = True
        else:
            break
    return retirado


def _fijar_justificacion_parrafo(p, valor: str) -> None:
    """Fija <w:jc> del párrafo conservando el orden de hijos del esquema."""
    from docx.oxml import OxmlElement

    pPr = p.find(_qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        p.insert(0, pPr)
    jc = pPr.find(_qn("w:jc"))
    if jc is None:
        jc = OxmlElement("w:jc")
        pPr.insert_element_before(
            jc,
            "w:textDirection",
            "w:textAlignment",
            "w:textboxTightWrap",
            "w:outlineLvl",
            "w:divId",
            "w:cnfStyle",
            "w:rPr",
            "w:sectPr",
            "w:pPrChange",
        )
    jc.set(_qn("w:val"), valor)


def _reserva_tabulador_dxa(tamano_pt: float = 10.0) -> float:
    """Holgura que Word exige tras la cola decimal para no partir el número.

    La comprobación empírica con ExportAsFixedFormat2 muestra que un tabulador
    decimal cuyo número termina a menos de medio em del borde útil se parte en
    dos líneas («0.» / «939»). Se reserva 0,6 em, nunca menos de 6 pt (120 dxa).
    """
    return max(120.0, 0.6 * float(tamano_pt) * 20.0)


def aplicar_alineacion_decimal(
    documento,
    indice_tabla: int,
    columnas: Sequence[int],
    modo: str = "tab_decimal",
    solo_verificar: bool = False,
) -> Dict[str, Any]:
    """Alinea columnas numéricas con tabulador decimal nativo (no a la derecha).

    El tabulador se coloca de modo que la cola decimal (desde el separador hasta
    el final, incluido el sufijo «%») termine antes del borde derecho útil,
    dejando la holgura que Word exige para no partir el número («0.» / «939»):
    0,6 em, nunca menos de 6 pt. Antes de fijar el tabulador se comprueba, como
    aserción previa obligatoria, que la parte entera más la cola decimal más esa
    holgura caben en el ancho útil de la celda; si no caben, la columna se
    degrada a alineación derecha, se retira el tabulador decimal con su run y se
    registra la degradación. También se degrada cuando los valores usan punto
    como separador decimal: en un documento en español Word no reconoce esa
    parada y parte el número igualmente. Las celdas sin valor numérico no se tocan.
    """
    if modo not in ("tab_decimal", "derecha"):
        return {"tabla": int(indice_tabla), "estado": "fallida", "motivo": f"modo no válido: {modo}"}
    indice = int(indice_tabla)
    if indice < 0 or indice >= len(documento.tables):
        return {"tabla": indice, "estado": "fallida", "motivo": "índice de tabla fuera de rango"}
    tabla = documento.tables[indice]
    anchos = _anchos_grid_tabla(tabla)
    margenes = _margenes_tabla(tabla)
    trs = tabla._tbl.findall(_qn("w:tr"))
    sufijo_pt = (_ancho_texto_dxa("%", 10.0) or 150.0) / 20.0
    reserva_dxa = _reserva_tabulador_dxa(10.0)

    detalle: List[Dict[str, Any]] = []
    total_alineadas = 0
    total_omitidas = 0
    total_degradadas = 0
    columnas_degradadas: List[int] = []
    for columna in [int(c) for c in columnas]:
        if columna < 0 or columna >= len(anchos):
            detalle.append({"columna": columna, "estado": "fallida", "motivo": "columna fuera del grid"})
            continue
        disponible_dxa = max(1, anchos[columna] - margenes["left"] - margenes["right"])
        posicion_porcentaje_pt = max(1.0, disponible_dxa / 20.0 - sufijo_pt - 1.0)
        celdas_columna: List[Tuple[Any, str]] = []
        for tr in trs[1:]:
            tcs = tr.findall(_qn("w:tc"))
            if columna >= len(tcs):
                continue
            tc = tcs[columna]
            for p in tc.iter(_qn("w:p")):
                texto = "".join(t.text or "" for t in p.iter(_qn("w:t"))).strip()
                if _PATRON_NUMERICO.match(texto):
                    celdas_columna.append((p, texto))
        numericas = len(celdas_columna)
        if numericas == 0:
            total_omitidas += 1
            detalle.append(
                {
                    "columna": columna,
                    "estado": "omitida",
                    "motivo": "sin valores numéricos en la columna",
                    "ancho_util_pt": round(disponible_dxa / 20.0, 1),
                }
            )
            continue
        cola_dxa = 0.0
        entero_dxa = 0.0
        tiene_decimal = False
        for _, texto in celdas_columna:
            limpio = re.sub(r"\s+", "", texto)
            separador = re.search(r"[.,]", limpio)
            if separador:
                tiene_decimal = True
                cola = limpio[separador.start() :]
                entero = limpio[: separador.start()]
            else:
                cola = ""
                entero = limpio
            cola_dxa = max(cola_dxa, _ancho_texto_dxa(cola, 10.0) or 0.0)
            entero_dxa = max(entero_dxa, _ancho_texto_dxa(entero, 10.0) or 0.0)
        # Un tabulador decimal solo lo reconoce Word si el valor emplea el
        # separador decimal de la configuración regional del documento (coma en
        # español). Comprobación empírica con ExportAsFixedFormat2 y sonda COM:
        # con valores «0.939» la parada decimal se ignora (el tabulador salta a la
        # parada por omisión de 36 pt y el número se parte en «0.» / «939»),
        # mientras que la misma parada como tabulador izquierdo sí se respeta.
        # Por eso, si la columna usa punto como separador, se degrada a derecha.
        usa_punto = any(
            (re.search(r"[.,]", re.sub(r"\s+", "", texto)) or [None])[0] == "."
            for _, texto in celdas_columna
        )
        # Aserción previa obligatoria: entero + cola + holgura debe caber en el ancho útil.
        cabe_decimal = entero_dxa + cola_dxa + reserva_dxa <= disponible_dxa
        if modo == "tab_decimal" and usa_punto:
            modo_columna = "derecha"
            motivo_columna = (
                "la columna usa punto como separador decimal y el documento está en "
                "español: Word ignora la parada decimal y partiría el número; "
                "se aplicó alineación derecha"
            )
        elif modo == "tab_decimal" and not tiene_decimal:
            # Columna de enteros: la alineación derecha es equivalente y evita
            # un tabulador decimal sin separador que descuadraría la columna.
            modo_columna = "derecha"
            motivo_columna = "columna de enteros: se aplicó alineación derecha"
        elif modo == "tab_decimal" and cabe_decimal:
            modo_columna = "tab_decimal"
            motivo_columna = ""
        else:
            modo_columna = "derecha"
            motivo_columna = (
                "parte entera + cola decimal + holgura (0,6 em) exceden el ancho útil: "
                "se aplicó alineación derecha"
            )
        posicion_dxa = max(entero_dxa, disponible_dxa - cola_dxa - reserva_dxa)
        posicion_pt = max(0.0, posicion_dxa / 20.0)
        for p, _ in celdas_columna:
            if solo_verificar:
                continue
            if modo_columna == "tab_decimal":
                _colocar_numero_en_tabulador_decimal(p, int(round(posicion_pt * 20)))
            else:
                _quitar_tabulador_decimal(p)
                _fijar_justificacion_parrafo(p, "right")
        total_alineadas += numericas
        if modo_columna == "derecha" and modo == "tab_decimal" and tiene_decimal:
            total_degradadas += 1
            columnas_degradadas.append(columna)
            detalle.append(
                {
                    "columna": columna,
                    "estado": "degradada",
                    "motivo": motivo_columna,
                    "valores_numericos": numericas,
                    "celdas_alineadas": numericas,
                    "ancho_util_pt": round(disponible_dxa / 20.0, 1),
                    "ancho_util_dxa": round(disponible_dxa, 1),
                    "parte_entera_dxa": round(entero_dxa, 1),
                    "cola_decimal_dxa": round(cola_dxa, 1),
                    "reserva_dxa": round(reserva_dxa, 1),
                }
            )
            continue
        detalle.append(
            {
                "columna": columna,
                "estado": "aplicable" if solo_verificar else "aplicada",
                "alineacion": "tab_decimal" if modo_columna == "tab_decimal" else "derecha",
                "valores_numericos": numericas,
                "celdas_alineadas": numericas,
                "posicion_tabulador_pt": round(posicion_pt, 1),
                "posicion_tabulador_porcentaje_pt": round(posicion_porcentaje_pt, 1),
                "ancho_util_pt": round(disponible_dxa / 20.0, 1),
                "ancho_util_dxa": round(disponible_dxa, 1),
                "cola_decimal_dxa": round(cola_dxa, 1),
                "parte_entera_dxa": round(entero_dxa, 1),
                "reserva_dxa": round(reserva_dxa, 1),
            }
        )

    # Verificación posterior celda por celda: ningún tabulador puede quedar fuera del ancho útil.
    verificacion = {"columnas_revisadas": 0, "columnas_fuera_de_ancho": 0, "detalle": []}
    if not solo_verificar:
        for fila in detalle:
            if fila.get("estado") != "aplicada":
                continue
            if fila.get("alineacion") != "tab_decimal":
                continue
            columna = int(fila["columna"])
            disponible_dxa = float(fila["ancho_util_dxa"])
            revisadas = 0
            fuera = 0
            for tr in trs[1:]:
                tcs = tr.findall(_qn("w:tc"))
                if columna >= len(tcs):
                    continue
                for p in tcs[columna].iter(_qn("w:p")):
                    texto = "".join(t.text or "" for t in p.iter(_qn("w:t"))).strip()
                    if not _PATRON_NUMERICO.match(texto):
                        continue
                    revisadas += 1
                    pPr = p.find(_qn("w:pPr"))
                    tabs = pPr.find(_qn("w:tabs")) if pPr is not None else None
                    posiciones = [
                        int(t.get(_qn("w:pos")) or 0)
                        for t in (tabs.findall(_qn("w:tab")) if tabs is not None else [])
                        if t.get(_qn("w:val")) == "decimal"
                    ]
                    if not posiciones:
                        fuera += 1
                        continue
                    limpio = re.sub(r"\s+", "", texto)
                    separador = re.search(r"[.,]", limpio)
                    if separador:
                        cola = limpio[separador.start() :]
                        exceso = posiciones[0] + (_ancho_texto_dxa(cola, 10.0) or 0.0) + reserva_dxa
                    else:
                        # Entero: la cifra completa queda a la izquierda de la parada.
                        exceso = posiciones[0]
                    if exceso > disponible_dxa + 1:
                        fuera += 1
            verificacion["columnas_revisadas"] += 1
            if fuera:
                verificacion["columnas_fuera_de_ancho"] += 1
                verificacion["detalle"].append(
                    {"columna": columna, "celdas_revisadas": revisadas, "celdas_fuera_de_ancho": fuera}
                )

    return {
        "tabla": indice,
        "modo": modo,
        "estado": "aplicable" if solo_verificar else "aplicada",
        "columnas": [int(c) for c in columnas],
        "celdas_alineadas": total_alineadas,
        "columnas_omitidas": total_omitidas,
        "columnas_degradadas": total_degradadas,
        "columnas_degradadas_lista": columnas_degradadas,
        "reserva_dxa": round(reserva_dxa, 1),
        "verificacion": verificacion,
        "detalle": detalle,
    }


def _texto_con_tabuladores(p) -> str:
    """Reconstruye el texto del párrafo representando tabuladores y saltos.

    A diferencia de concatenar solo ``w:t``, permite detectar si el marcador ya
    está separado por un tabulador nativo, condición que hace idempotente la
    normalización de listas.
    """
    piezas: List[str] = []
    for run in p.iter(_qn("w:r")):
        for nodo in run.iter():
            if nodo.tag == _qn("w:t"):
                piezas.append(nodo.text or "")
            elif nodo.tag == _qn("w:tab"):
                piezas.append("\t")
            elif nodo.tag in (_qn("w:br"), _qn("w:cr")):
                piezas.append("\n")
    return "".join(piezas)


def _nodos_texto_directos(p):
    """Devuelve los nodos ``w:t`` de runs simples del párrafo.

    Retorna ``None`` cuando algún run contiene elementos distintos de ``rPr`` y
    ``w:t`` (hipervínculos, campos, tabuladores, saltos): en ese caso la cirugía
    se aborta en lugar de reconstruir el párrafo y perder formato.
    """
    nodos: List[List[Any]] = []
    tolerados = {
        _qn("w:lastRenderedPageBreak"),
        _qn("w:softHyphen"),
        _qn("w:noBreakHyphen"),
    }
    for r in p.findall(_qn("w:r")):
        for hijo in r:
            if hijo.tag not in (_qn("w:rPr"), _qn("w:t")) and hijo.tag not in tolerados:
                return None
        t = r.find(_qn("w:t"))
        if t is None:
            continue
        nodos.append([r, t, t.text or ""])
    return nodos


def _fijar_sangria(
    p,
    izquierda_dxa: int,
    colgante_dxa: Optional[int] = None,
    primera_linea_dxa: Optional[int] = None,
) -> None:
    """Fija ``w:ind`` con sangría izquierda, colgante o de primera línea exactas."""
    from docx.oxml import OxmlElement

    pPr = p.find(_qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        p.insert(0, pPr)
    ind = pPr.find(_qn("w:ind"))
    if ind is None:
        ind = OxmlElement("w:ind")
        pPr.insert_element_before(ind, *_ORDEN_IND_SUCESORES)
    for clave in (
        "left",
        "leftChars",
        "start",
        "startChars",
        "hanging",
        "hangingChars",
        "firstLine",
        "firstLineChars",
        "right",
        "rightChars",
        "end",
        "endChars",
    ):
        ind.attrib.pop(_qn(f"w:{clave}"), None)
    if izquierda_dxa:
        ind.set(_qn("w:left"), str(int(izquierda_dxa)))
    if colgante_dxa:
        ind.set(_qn("w:hanging"), str(int(colgante_dxa)))
    if primera_linea_dxa:
        ind.set(_qn("w:firstLine"), str(int(primera_linea_dxa)))
    if not ind.attrib:
        pPr.remove(ind)


def _fijar_tabulador_izquierda(p, posicion_dxa: int) -> None:
    """Garantiza una parada de tabulador izquierda en la posición indicada."""
    from docx.oxml import OxmlElement

    pPr = p.find(_qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        p.insert(0, pPr)
    tabs = pPr.find(_qn("w:tabs"))
    if tabs is None:
        tabs = OxmlElement("w:tabs")
        pPr.insert_element_before(tabs, *_ORDEN_TABS_SUCESORES)
    posicion = str(int(posicion_dxa))
    for tab in tabs.findall(_qn("w:tab")):
        if tab.get(_qn("w:val")) in (None, "left") and tab.get(_qn("w:pos")) == posicion:
            return
    tab = OxmlElement("w:tab")
    tab.set(_qn("w:val"), "left")
    tab.set(_qn("w:pos"), posicion)
    tabs.append(tab)
    # El esquema exige paradas ordenadas por posición.
    for hijo in sorted(tabs.findall(_qn("w:tab")), key=lambda x: int(x.get(_qn("w:pos")) or 0)):
        tabs.remove(hijo)
        tabs.append(hijo)


def _insertar_tab_marcador(p, nodos, lead_end: int, marker_end: int, space_end: int) -> bool:
    """Sustituye los espacios tras el marcador por un ``<w:tab/>`` nativo.

    Conserva en su lugar el texto del marcador, elimina los espacios iniciales
    manuales y los que separaban el marcador del contenido, e inserta el
    tabulador exactamente en el límite del marcador. Divide el run cuando el
    marcador y el contenido comparten nodo, copiando ``w:rPr`` para no perder
    negritas, subíndices ni tamaño.
    """
    import copy

    from docx.oxml import OxmlElement

    tramos: List[Tuple[Any, Any, str, int]] = []
    pos = 0
    for r, t, txt in nodos:
        tramos.append((r, t, txt, pos))
        pos += len(txt)
    if not (0 <= lead_end <= marker_end <= space_end <= pos):
        return False

    for r, t, txt, inicio in tramos:
        conservado = "".join(
            ch
            for k, ch in enumerate(txt)
            if (lead_end <= inicio + k < marker_end) or (inicio + k >= space_end)
        )
        if conservado != txt:
            t.text = conservado
            if conservado != conservado.strip():
                t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")

    objetivo = None
    for tramo in tramos:
        r, t, txt, inicio = tramo
        if inicio < marker_end <= inicio + len(txt):
            objetivo = tramo
            break
    if objetivo is None:
        return False
    r, t, txt, inicio = objetivo
    rPr = r.find(_qn("w:rPr"))
    corte = marker_end - inicio
    prefijo = "".join(ch for k, ch in enumerate(txt[:corte]) if inicio + k >= lead_end)
    cola = "".join(ch for k, ch in enumerate(txt) if k >= corte and inicio + k >= space_end)
    t.text = prefijo
    if prefijo != prefijo.strip():
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")

    run_tab = OxmlElement("w:r")
    if rPr is not None:
        run_tab.append(copy.deepcopy(rPr))
    run_tab.append(OxmlElement("w:tab"))
    r.addnext(run_tab)
    if cola:
        run_cola = OxmlElement("w:r")
        if rPr is not None:
            run_cola.append(copy.deepcopy(rPr))
        nodo = OxmlElement("w:t")
        nodo.text = cola
        if cola != cola.strip():
            nodo.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        run_cola.append(nodo)
        run_tab.addnext(run_cola)

    for r0, t0, _ in nodos:
        if (t0.text or "") != "":
            continue
        if any(c.tag not in (_qn("w:rPr"), _qn("w:t")) for c in r0):
            continue
        padre = r0.getparent()
        if padre is not None:
            padre.remove(r0)
    return True


def _quitar_espacios_iniciales(p, nodos) -> int:
    """Elimina los espacios manuales con que arranca un párrafo narrativo."""
    retirados = 0
    for r, t, txt in nodos:
        if not txt:
            continue
        if not txt.startswith("  "):
            break
        limpio = txt.lstrip(" ")
        retirados += len(txt) - len(limpio)
        t.text = limpio
        if limpio != limpio.strip():
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        if limpio:
            break
    return retirados


def _clasificar_marcador(texto: str):
    """Clasifica un párrafo con marcador como ``item``, ``rotulo`` o ``None``."""
    m = _PATRON_MARCADOR_LISTA.match(texto)
    if m is None:
        return None
    marcador = m.group(2)
    resto = texto[m.end() :]
    es_rotulo = (
        bool(_PATRON_ROTULO_LETRA.match(marcador))
        and resto.strip().endswith(":")
        and "\t" not in m.group(3)
    )
    return m, ("rotulo" if es_rotulo else "item")


def _verificar_listas_normalizadas(
    documento, sangria_dxa: int, colgante_dxa: int
) -> Dict[str, Any]:
    """Comprueba en el documento resultante que listas y rótulos quedaron nativos."""
    resumen = {
        "items": 0,
        "items_justificados": 0,
        "items_sin_tab": 0,
        "items_sin_colgante": 0,
        "items_con_salto": 0,
        "rotulos": 0,
        "rotulos_justificados": 0,
        "prosa_justificada": 0,
        "prosa_con_sangria_manual": 0,
    }
    for par in documento.paragraphs:
        p = par._p
        texto = _texto_con_tabuladores(p)
        clasificado = _clasificar_marcador(texto)
        pPr = p.find(_qn("w:pPr"))
        jc = pPr.find(_qn("w:jc")) if pPr is not None else None
        valor_jc = jc.get(_qn("w:val")) if jc is not None else None
        if clasificado is None:
            if valor_jc != "both":
                continue
            resumen["prosa_justificada"] += 1
            nodos = _nodos_texto_directos(p)
            if nodos:
                crudo = "".join(x[2] for x in nodos)
                if crudo.startswith("  "):
                    resumen["prosa_con_sangria_manual"] += 1
            continue
        m, clase = clasificado
        if clase == "rotulo":
            resumen["rotulos"] += 1
            if valor_jc == "both":
                resumen["rotulos_justificados"] += 1
            continue
        resumen["items"] += 1
        if valor_jc == "both":
            resumen["items_justificados"] += 1
        if "\t" not in m.group(3):
            resumen["items_sin_tab"] += 1
        ind = pPr.find(_qn("w:ind")) if pPr is not None else None
        if (
            ind is None
            or ind.get(_qn("w:left")) != str(int(sangria_dxa))
            or ind.get(_qn("w:hanging")) != str(int(colgante_dxa))
        ):
            resumen["items_sin_colgante"] += 1
        if p.find(".//" + _qn("w:br")) is not None:
            resumen["items_con_salto"] += 1
    return resumen


def normalizar_listas_rotulos(
    documento,
    solo_verificar: bool = False,
    sangria_dxa: int = 720,
    colgante_dxa: int = 360,
    limpiar_espacios_prosa: bool = True,
) -> Dict[str, Any]:
    """Normaliza listas numeradas, viñetas y rótulos A/B/C con recursos nativos.

    Cada ítem conserva su marcador y pasa a ``jc=left`` con sangría francesa
    nativa (``left=720``, ``hanging=360``) y una parada de tabulador izquierda
    en 720 dxa; los espacios manuales que separaban marcador y contenido se
    sustituyen por ``<w:tab/>``. Los rótulos de una sola letra terminados en dos
    puntos (``A.``, ``B.``, ``C.``) son encabezados sin contenido en el mismo
    párrafo: se alinean a la izquierda y se anulan sus sangrías, sin tabulador
    porque no hay texto que alinear. La prosa narrativa conserva justificado e
    interlineado; solo se le retiran los espacios iniciales manuales.

    La operación es idempotente: un marcador ya separado por tabulador se
    reconoce como normalizado y no se vuelve a tocar. Los párrafos con runs
    complejos (campos, hipervínculos, tabuladores previos) se omiten y se
    reportan en ``fallidos`` en lugar de reconstruirse.
    """
    detalle: List[Dict[str, Any]] = []
    fallidos: List[Dict[str, Any]] = []
    items = 0
    rotulos = 0
    prosa = 0
    ya_normalizados = 0
    omitidos = 0
    for indice, par in enumerate(documento.paragraphs):
        p = par._p
        texto = _texto_con_tabuladores(p)
        clasificado = _clasificar_marcador(texto)
        if clasificado is None:
            if not limpiar_espacios_prosa:
                continue
            if "\t" in texto or "\n" in texto:
                continue
            pPr = p.find(_qn("w:pPr"))
            jc = pPr.find(_qn("w:jc")) if pPr is not None else None
            valor_jc = jc.get(_qn("w:val")) if jc is not None else None
            if valor_jc not in ("both", "left"):
                continue
            nodos = _nodos_texto_directos(p)
            if nodos is None:
                continue
            if not "".join(x[2] for x in nodos).startswith("  "):
                continue
            if solo_verificar:
                prosa += 1
                detalle.append({"parrafo": indice, "clase": "prosa", "accion": "espacios_iniciales"})
                continue
            retirados = _quitar_espacios_iniciales(p, nodos)
            if retirados:
                prosa += 1
                detalle.append(
                    {
                        "parrafo": indice,
                        "clase": "prosa",
                        "accion": "espacios_iniciales",
                        "caracteres_retirados": retirados,
                    }
                )
            continue
        m, clase = clasificado
        marcador = m.group(2)
        if "\t" in m.group(3):
            ya_normalizados += 1
            detalle.append({"parrafo": indice, "clase": "ya_normalizado", "marcador": marcador})
            continue
        nodos = _nodos_texto_directos(p)
        if nodos is None:
            omitidos += 1
            fallidos.append(
                {
                    "parrafo": indice,
                    "motivo": "run con contenido no textual (campo, hipervínculo o tabulador)",
                    "texto": texto[:80],
                }
            )
            continue
        if "".join(x[2] for x in nodos) != texto:
            omitidos += 1
            fallidos.append(
                {
                    "parrafo": indice,
                    "motivo": "el texto directo no coincide con el texto con tabuladores",
                    "texto": texto[:80],
                }
            )
            continue
        if solo_verificar:
            if clase == "rotulo":
                rotulos += 1
                accion = {"jc": "left", "ind": {"left": 0, "firstLine": 0}}
            else:
                items += 1
                accion = {
                    "jc": "left",
                    "ind": {"left": int(sangria_dxa), "hanging": int(colgante_dxa)},
                    "tabulador_dxa": int(sangria_dxa),
                }
            detalle.append({"parrafo": indice, "clase": clase, "marcador": marcador, **accion})
            continue
        if clase == "rotulo":
            _fijar_sangria(p, 0, None, None)
            _fijar_justificacion_parrafo(p, "left")
            rotulos += 1
            detalle.append({"parrafo": indice, "clase": "rotulo", "marcador": marcador})
            continue
        if not _insertar_tab_marcador(p, nodos, m.start(2), m.end(2), m.end()):
            omitidos += 1
            fallidos.append({"parrafo": indice, "motivo": "no se pudo insertar el tabulador del marcador"})
            continue
        _fijar_sangria(p, sangria_dxa, colgante_dxa, None)
        _fijar_tabulador_izquierda(p, sangria_dxa)
        _fijar_justificacion_parrafo(p, "left")
        items += 1
        detalle.append(
            {
                "parrafo": indice,
                "clase": "item",
                "marcador": marcador,
                "jc": "left",
                "ind": {"left": int(sangria_dxa), "hanging": int(colgante_dxa)},
                "tabulador_dxa": int(sangria_dxa),
            }
        )

    resultado = {
        "estado": "aplicable" if solo_verificar else "aplicada",
        "sangria_dxa": int(sangria_dxa),
        "colgante_dxa": int(colgante_dxa),
        "items": items,
        "rotulos": rotulos,
        "prosa_limpiada": prosa,
        "ya_normalizados": ya_normalizados,
        "omitidos": omitidos,
        "fallidos": fallidos,
        "detalle": detalle,
    }
    if not solo_verificar:
        resultado["verificacion"] = _verificar_listas_normalizadas(documento, sangria_dxa, colgante_dxa)
    return resultado


def _convertir_subindices_run(r, permitidos, excluir) -> Tuple[int, int]:
    """Convierte la notación con guion bajo de un run en subíndices nativos."""
    import copy

    from docx.oxml import OxmlElement

    tnodes = r.findall(_qn("w:t"))
    if not tnodes:
        return 0, 0
    texto = "".join(t.text or "" for t in tnodes)
    coincidencias = [
        m
        for m in _PATRON_SUBINDICE.finditer(texto)
        if m.group(1) in permitidos and m.group(0) not in excluir
    ]
    if not coincidencias:
        return 0, 0

    # Un único nodo w:t por run: se consolidan los fragmentos sin alterar texto.
    if len(tnodes) > 1:
        tnodes[0].text = texto
        for sobrante in tnodes[1:]:
            sobrante.getparent().remove(sobrante)

    piezas: List[Tuple[str, bool]] = []
    posicion = 0
    guiones = 0
    for m in coincidencias:
        guion = m.start(2) - 1
        piezas.append((texto[posicion:guion], False))
        sufijo = m.group(2)
        guiones += 1 + sufijo.count("_")
        piezas.append((texto[guion + 1 : m.end()].replace("_", ""), True))
        posicion = m.end()
    piezas.append((texto[posicion:], False))

    rPr = r.find(_qn("w:rPr"))
    referencia = r
    primera = True
    for contenido, subindice in piezas:
        if primera:
            destino = r
            primera = False
        else:
            destino = OxmlElement("w:r")
            if rPr is not None:
                destino.append(copy.deepcopy(rPr))
            referencia.addnext(destino)
            referencia = destino
        t = destino.find(_qn("w:t"))
        if t is None:
            t = OxmlElement("w:t")
            destino.append(t)
        t.text = contenido
        if contenido != contenido.strip() or "  " in contenido:
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        destino_rPr = destino.find(_qn("w:rPr"))
        if subindice:
            if destino_rPr is None:
                destino_rPr = OxmlElement("w:rPr")
                destino.insert(0, destino_rPr)
            nodo = _rpr_propiedad(destino_rPr, "vertAlign", True)
            nodo.set(_qn("w:val"), "subscript")
        elif destino_rPr is not None:
            _rpr_propiedad(destino_rPr, "vertAlign", False)
    return len(coincidencias), guiones


def _contar_subindices_run(r, permitidos, excluir) -> Tuple[int, int]:
    """Cuenta conversiones y guiones bajos sin modificar el documento."""
    tnodes = r.findall(_qn("w:t"))
    if not tnodes:
        return 0, 0
    texto = "".join(t.text or "" for t in tnodes)
    coincidencias = [
        m
        for m in _PATRON_SUBINDICE.finditer(texto)
        if m.group(1) in permitidos and m.group(0) not in excluir
    ]
    return len(coincidencias), sum(1 + m.group(2).count("_") for m in coincidencias)


def convertir_notacion_subindices(
    documento,
    terminos: Any,
    ambito: str = "cuerpo",
    solo_verificar: bool = False,
) -> Dict[str, Any]:
    """Sustituye «nombre_sufijo» por subíndice nativo sin perder caracteres.

    «terminos» puede ser la lista del inventario de cuerpo, un diccionario con
    las claves ``cuerpo``/``celdas``/``identificadores`` o una lista de celdas.
    El guion bajo desaparece y el sufijo pasa a ``w:vertAlign=subscript``; el
    resto del texto visible se conserva intacto.
    """
    if ambito not in ("cuerpo", "celdas", "ambos"):
        return {"estado": "fallida", "motivo": f"ámbito no válido: {ambito}"}

    cuerpo: List[Dict[str, Any]] = []
    celdas: List[Dict[str, Any]] = []
    excluir: List[str] = []
    if isinstance(terminos, dict):
        cuerpo = list(terminos.get("cuerpo", []))
        celdas = list(terminos.get("celdas", []))
        excluir = list(terminos.get("identificadores", []) or terminos.get("excluir", []))
    else:
        if ambito == "celdas":
            celdas = list(terminos)
        else:
            cuerpo = list(terminos)

    aplicadas: List[Dict[str, Any]] = []
    fallidas: List[Dict[str, Any]] = []
    total_ocurrencias = 0
    total_guiones = 0
    parrafos_tocados = 0
    celdas_tocadas = 0

    def _procesar(p) -> Tuple[int, int]:
        ocurrencias = 0
        guiones = 0
        for r in p.findall(_qn("w:r")):
            if solo_verificar:
                o, g = _contar_subindices_run(r, permitidos, excluir)
            else:
                o, g = _convertir_subindices_run(r, permitidos, excluir)
            ocurrencias += o
            guiones += g
        return ocurrencias, guiones

    if ambito in ("cuerpo", "ambos"):
        for item in cuerpo:
            indice = int(item["indice"])
            permitidos = {t.split("_")[0] for t in item.get("terminos", [])}
            if not permitidos:
                continue
            if indice < 0 or indice >= len(documento.paragraphs):
                fallidas.append(
                    {"ambito": "cuerpo", "indice": indice, "motivo": "índice de párrafo fuera de rango"}
                )
                continue
            ocurrencias, guiones = _procesar(documento.paragraphs[indice]._p)
            if ocurrencias:
                parrafos_tocados += 1
                total_ocurrencias += ocurrencias
                total_guiones += guiones
                aplicadas.append(
                    {
                        "ambito": "cuerpo",
                        "indice": indice,
                        "ocurrencias": ocurrencias,
                        "guiones_bajos_retirados": guiones,
                        "estado": "aplicable" if solo_verificar else "aplicada",
                    }
                )
            else:
                fallidas.append(
                    {"ambito": "cuerpo", "indice": indice, "motivo": "sin coincidencias para los términos declarados"}
                )

    if ambito in ("celdas", "ambos"):
        for item in celdas:
            tabla = int(item["tabla"])
            fila = int(item["fila"])
            columna = int(item["col"])
            permitidos = {t.split("_")[0] for t in item.get("terminos", [])}
            if not permitidos:
                continue
            try:
                tc = documento.tables[tabla].cell(fila, columna)._tc
            except (IndexError, ValueError):
                fallidas.append(
                    {
                        "ambito": "celdas",
                        "tabla": tabla,
                        "fila": fila,
                        "columna": columna,
                        "motivo": "celda fuera de rango",
                    }
                )
                continue
            ocurrencias = 0
            guiones = 0
            for p in tc.iter(_qn("w:p")):
                o, g = _procesar(p)
                ocurrencias += o
                guiones += g
            if ocurrencias:
                celdas_tocadas += 1
                total_ocurrencias += ocurrencias
                total_guiones += guiones
                aplicadas.append(
                    {
                        "ambito": "celdas",
                        "tabla": tabla,
                        "fila": fila,
                        "columna": columna,
                        "ocurrencias": ocurrencias,
                        "guiones_bajos_retirados": guiones,
                        "estado": "aplicable" if solo_verificar else "aplicada",
                    }
                )
            else:
                fallidas.append(
                    {
                        "ambito": "celdas",
                        "tabla": tabla,
                        "fila": fila,
                        "columna": columna,
                        "motivo": "sin coincidencias para los términos declarados",
                    }
                )

    return {
        "estado": "aplicable" if solo_verificar else "aplicada",
        "ambito": ambito,
        "aplicadas": aplicadas,
        "fallidas": fallidas,
        "parrafos_con_subindices": parrafos_tocados,
        "celdas_con_subindices": celdas_tocadas,
        "ocurrencias": total_ocurrencias,
        "guiones_bajos_retirados": total_guiones,
    }


def aplicar_keep_junta(
    documento,
    indices: Sequence[int],
    solo_verificar: bool = False,
) -> Dict[str, Any]:
    """Inyecta <w:keepNext/> en todas las filas de una tabla menos la última."""
    aplicadas: List[Dict[str, Any]] = []
    fallidas: List[Dict[str, Any]] = []
    for indice in [int(i) for i in indices]:
        if indice < 0 or indice >= len(documento.tables):
            fallidas.append({"tabla": indice, "motivo": "índice de tabla fuera de rango"})
            continue
        tabla = documento.tables[indice]
        trs = tabla._tbl.findall(_qn("w:tr"))
        if len(trs) < 2:
            fallidas.append({"tabla": indice, "motivo": "la tabla no tiene filas de cuerpo"})
            continue
        marcados = 0
        for tr in trs[:-1]:
            for p in tr.iter(_qn("w:p")):
                if solo_verificar:
                    pPr = p.find(_qn("w:pPr"))
                    if pPr is None or pPr.find(_qn("w:keepNext")) is None:
                        marcados += 1
                elif _insertar_keep_next(p):
                    marcados += 1
        aplicadas.append(
            {
                "tabla": indice,
                "filas": len(trs),
                "parrafos_marcados": marcados,
                "estado": "aplicable" if solo_verificar else "aplicada",
            }
        )
    return {
        "estado": "aplicable" if solo_verificar else "aplicada",
        "aplicadas": aplicadas,
        "fallidas": fallidas,
    }


def aplicar_keep_cabecera(documento, solo_verificar: bool = False) -> Dict[str, Any]:
    """Evita encabezados huérfanos: une la fila de cabecera con la primera fila
    de cuerpo y el rótulo con su título y su nota.

    Las tablas largas pueden repartirse entre páginas —la cabecera se repite por
    ``w:tblHeader``—, pero ninguna debe quedar con la sola cabecera al pie de una
    página ni con el rótulo separado del objeto. La unión se expresa con
    ``<w:keepNext/>`` nativo, sin mover ni alterar contenido.
    """
    tablas_marcadas = 0
    filas_marcadas = 0
    rotulos_marcados = 0
    for tabla in documento.tables:
        trs = tabla._tbl.findall(_qn("w:tr"))
        if not trs:
            continue
        marcadas = 0
        for parrafo in trs[0].iter(_qn("w:p")):
            if solo_verificar:
                pPr = parrafo.find(_qn("w:pPr"))
                if pPr is None or pPr.find(_qn("w:keepNext")) is None:
                    marcadas += 1
            elif _insertar_keep_next(parrafo):
                marcadas += 1
        if marcadas:
            tablas_marcadas += 1
            filas_marcadas += marcadas
    parrafos = documento.paragraphs
    for indice, parrafo in enumerate(parrafos):
        if not re.match(r"^(Tabla|Figura)\s+\d+$", parrafo.text.strip()):
            continue
        objetivos = [parrafo]
        if indice + 1 < len(parrafos):
            objetivos.append(parrafos[indice + 1])
        if indice + 2 < len(parrafos) and re.match(
            r"^(Nota|Fuente)\b", parrafos[indice + 2].text.strip()
        ):
            objetivos.append(parrafos[indice + 2])
        marcadas = 0
        for objetivo in objetivos:
            if solo_verificar:
                pPr = objetivo._p.find(_qn("w:pPr"))
                if pPr is None or pPr.find(_qn("w:keepNext")) is None:
                    marcadas += 1
            elif _insertar_keep_next(objetivo._p):
                marcadas += 1
        if marcadas:
            rotulos_marcados += 1
    return {
        "estado": "aplicable" if solo_verificar else "aplicada",
        "tablas_con_cabecera_marcada": tablas_marcadas,
        "parrafos_cabecera_marcados": filas_marcadas,
        "rotulos_marcados": rotulos_marcados,
    }


def ensanchar_rango_tabla(
    documento,
    indice_tabla: int,
    columna_objetivo: int,
    ancho_objetivo_dxa: int,
    donantes: Dict[int, int],
    margen_dxa: int = 60,
    solo_verificar: bool = False,
) -> Dict[str, Any]:
    """Ensancha una columna de rango financiando el ancho con columnas donantes."""
    indice = int(indice_tabla)
    tabla = documento.tables[indice]
    actuales = _anchos_grid_tabla(tabla)
    nuevos = list(actuales)
    objetivo = int(columna_objetivo)
    nuevos[objetivo] = int(ancho_objetivo_dxa)
    for columna, monto in donantes.items():
        columna = int(columna)
        nuevos[columna] = nuevos[columna] - int(monto)
        if nuevos[columna] <= 2 * int(margen_dxa):
            return {
                "tabla": indice,
                "estado": "fallida",
                "motivo": f"la columna donante {columna} quedaría sin espacio útil",
            }
    if sum(nuevos) != sum(actuales):
        return {
            "tabla": indice,
            "estado": "fallida",
            "motivo": f"el ensanche altera la suma de la tabla ({sum(actuales)} -> {sum(nuevos)} dxa)",
        }
    resultado = aplicar_geometria_proporcional(
        documento, indice, nuevos, margen_dxa=margen_dxa, solo_verificar=solo_verificar
    )
    resultado["operacion"] = "ensanche_rango"
    resultado["columna_objetivo"] = objetivo
    resultado["ancho_objetivo_dxa"] = int(ancho_objetivo_dxa)
    resultado["donantes"] = {str(k): int(v) for k, v in donantes.items()}
    return resultado


def reparar_tcw_tabla(
    documento,
    indice_tabla: int,
    solo_verificar: bool = False,
) -> Dict[str, Any]:
    """Restaura la coherencia entre <w:tcW> y <w:tblGrid> en toda la tabla."""
    from docx.oxml import OxmlElement

    indice = int(indice_tabla)
    if indice < 0 or indice >= len(documento.tables):
        return {"tabla": indice, "estado": "fallida", "motivo": "índice de tabla fuera de rango"}
    tabla = documento.tables[indice]
    anchos = _anchos_grid_tabla(tabla)
    corregidas = 0
    revisadas = 0
    for tr in tabla._tbl.findall(_qn("w:tr")):
        tcs = tr.findall(_qn("w:tc"))
        if len(tcs) != len(anchos):
            continue
        for tc, ancho in zip(tcs, anchos):
            revisadas += 1
            tcPr = tc.find(_qn("w:tcPr"))
            if tcPr is None:
                tcPr = OxmlElement("w:tcPr")
                tc.insert(0, tcPr)
            tcW = tcPr.find(_qn("w:tcW"))
            if tcW is None:
                tcW = OxmlElement("w:tcW")
                tcPr.insert_element_before(tcW, *_ORDEN_TCW_SUCESORES)
            if tcW.get(_qn("w:w")) != str(ancho) or tcW.get(_qn("w:type")) != "dxa":
                if not solo_verificar:
                    tcW.set(_qn("w:type"), "dxa")
                    tcW.set(_qn("w:w"), str(ancho))
                corregidas += 1
    return {
        "tabla": indice,
        "estado": "aplicable" if solo_verificar else "aplicada",
        "celdas_revisadas": revisadas,
        "celdas_corregidas": corregidas,
        "grid_dxa": anchos,
    }


def dividir_parrafo_por_saltos(
    documento,
    indice: int,
    alineacion_lista: str = "left",
) -> Dict[str, Any]:
    """
    Convierte los saltos manuales <w:br/> de un párrafo en párrafos nativos
    independientes, sin alterar el texto. El primer párrafo conserva su pPr;
    los ítems de lista se alinean a la izquierda y sin sangría de primera línea.
    """
    import copy

    from docx.oxml import OxmlElement

    if alineacion_lista not in _ALINEACIONES:
        raise ValueError(f"Alineación no válida: {alineacion_lista}")

    p = documento.paragraphs[int(indice)]._p
    pPr = p.find(_qn("w:pPr"))
    saltos = [
        br
        for br in p.iter(_qn("w:br"))
        if br.get(_qn("w:type")) in (None, "", "textWrapping")
    ]
    if not saltos:
        return {"indice": int(indice), "parrafos": 1, "dividido": False, "textos": []}

    segmentos: List[List[Any]] = [[]]
    for hijo in list(p):
        if hijo is pPr:
            continue
        if hijo.tag == _qn("w:r"):
            rPr = hijo.find(_qn("w:rPr"))
            run_actual = None
            for parte in list(hijo):
                if parte is rPr:
                    continue
                if parte.tag == _qn("w:br") and parte.get(_qn("w:type")) in (None, "", "textWrapping"):
                    segmentos.append([])
                    run_actual = None
                    continue
                if run_actual is None:
                    run_actual = OxmlElement("w:r")
                    if rPr is not None:
                        run_actual.append(copy.deepcopy(rPr))
                    segmentos[-1].append(run_actual)
                run_actual.append(copy.deepcopy(parte))
        else:
            segmentos[-1].append(copy.deepcopy(hijo))

    textos = []
    for segmento in segmentos:
        textos.append(
            "".join(
                t.text or ""
                for elemento in segmento
                for t in elemento.iter(_qn("w:t"))
            )
        )
    while len(segmentos) > 1 and not textos[-1].strip():
        segmentos.pop()
        textos.pop()

    referencia = p
    creados = 0
    for posicion, segmento in enumerate(segmentos):
        nuevo = OxmlElement("w:p")
        if pPr is not None:
            nuevo_pPr = copy.deepcopy(pPr)
        else:
            nuevo_pPr = OxmlElement("w:pPr")
        if posicion > 0:
            ind = nuevo_pPr.find(_qn("w:ind"))
            if ind is None:
                ind = OxmlElement("w:ind")
                nuevo_pPr.insert_element_before(
                    ind,
                    "w:contextualSpacing",
                    "w:mirrorIndents",
                    "w:suppressOverlap",
                    "w:jc",
                    "w:textDirection",
                    "w:textAlignment",
                    "w:textboxTightWrap",
                    "w:outlineLvl",
                    "w:divId",
                    "w:cnfStyle",
                    "w:rPr",
                    "w:sectPr",
                    "w:pPrChange",
                )
            ind.set(_qn("w:firstLine"), "0")
            ind.set(_qn("w:left"), "0")
            jc = nuevo_pPr.find(_qn("w:jc"))
            if jc is None:
                jc = OxmlElement("w:jc")
                nuevo_pPr.insert_element_before(
                    jc,
                    "w:textDirection",
                    "w:textAlignment",
                    "w:textboxTightWrap",
                    "w:outlineLvl",
                    "w:divId",
                    "w:cnfStyle",
                    "w:rPr",
                    "w:sectPr",
                    "w:pPrChange",
                )
            jc.set(_qn("w:val"), alineacion_lista)
        nuevo.append(nuevo_pPr)
        for elemento in segmento:
            nuevo.append(elemento)
        referencia.addnext(nuevo)
        referencia = nuevo
        creados += 1
    p.getparent().remove(p)
    return {
        "indice": int(indice),
        "dividido": True,
        "parrafos": creados,
        "textos": [t[:120] for t in textos],
    }


def convertir_urls_a_hipervinculos(
    documento,
    desde: str = "REFERENCIAS BIBLIOGRÁFICAS",
    hasta: str = "ANEXOS",
) -> Dict[str, Any]:
    """
    Convierte los DOI/URL en texto plano de la sección de referencias en
    hipervínculos nativos <w:hyperlink> con relación externa, sin cambiar el
    texto visible ni agregar fuentes.
    """
    import copy

    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    from docx.oxml import OxmlElement

    parrafos = documento.paragraphs
    inicio = None
    fin = None
    for i, parrafo in enumerate(parrafos):
        texto = parrafo.text.strip()
        if inicio is None and texto == desde:
            inicio = i
        elif inicio is not None and texto == hasta:
            fin = i
            break
    if inicio is None:
        raise ValueError(f"No se encontró el encabezado «{desde}»")
    fin = fin if fin is not None else len(parrafos)

    patron = re.compile(r"https?://[^\s]+")
    acciones: List[Dict[str, Any]] = []
    for i in range(inicio + 1, fin):
        parrafo = parrafos[i]
        pe = parrafo._p
        for coincidencia in list(patron.finditer(parrafo.text)):
            url = coincidencia.group(0).rstrip(".,;:)")
            objetivo = None
            for run in pe.findall(_qn("w:r")):
                texto_run = "".join(t.text or "" for t in run.iter(_qn("w:t")))
                if url in texto_run:
                    objetivo = run
                    break
            if objetivo is None:
                continue
            texto_run = "".join(t.text or "" for t in objetivo.iter(_qn("w:t")))
            antes, despues = texto_run.split(url, 1)
            rPr = objetivo.find(_qn("w:rPr"))
            r_id = parrafo.part.relate_to(url, RT.HYPERLINK, is_external=True)
            hipervinculo = OxmlElement("w:hyperlink")
            hipervinculo.set(_qn("r:id"), r_id)
            hipervinculo.set(_qn("w:history"), "1")
            run_hiper = OxmlElement("w:r")
            if rPr is not None:
                run_hiper.append(copy.deepcopy(rPr))
            run_hiper_rPr = run_hiper.find(_qn("w:rPr"))
            if run_hiper_rPr is None:
                run_hiper_rPr = OxmlElement("w:rPr")
                run_hiper.insert(0, run_hiper_rPr)
            color = run_hiper_rPr.find(_qn("w:color"))
            if color is None:
                color = OxmlElement("w:color")
                run_hiper_rPr.insert_element_before(
                    color,
                    "w:spacing",
                    "w:w",
                    "w:kern",
                    "w:position",
                    "w:sz",
                    "w:szCs",
                    "w:highlight",
                    "w:u",
                    "w:effect",
                    "w:bdr",
                    "w:shd",
                    "w:fitText",
                    "w:vertAlign",
                    "w:rtl",
                    "w:cs",
                    "w:em",
                    "w:lang",
                    "w:eastAsianLayout",
                    "w:specVanish",
                    "w:oMath",
                )
            color.set(_qn("w:val"), "0563C1")
            subrayado = run_hiper_rPr.find(_qn("w:u"))
            if subrayado is None:
                subrayado = OxmlElement("w:u")
                run_hiper_rPr.insert_element_before(
                    subrayado,
                    "w:effect",
                    "w:bdr",
                    "w:shd",
                    "w:fitText",
                    "w:vertAlign",
                    "w:rtl",
                    "w:cs",
                    "w:em",
                    "w:lang",
                    "w:eastAsianLayout",
                    "w:specVanish",
                    "w:oMath",
                )
            subrayado.set(_qn("w:val"), "single")
            t = OxmlElement("w:t")
            t.text = url
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            run_hiper.append(t)
            hipervinculo.append(run_hiper)

            reemplazos = []
            if antes:
                run_antes = OxmlElement("w:r")
                if rPr is not None:
                    run_antes.append(copy.deepcopy(rPr))
                t_antes = OxmlElement("w:t")
                t_antes.text = antes
                t_antes.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                run_antes.append(t_antes)
                reemplazos.append(run_antes)
            reemplazos.append(hipervinculo)
            if despues:
                run_despues = OxmlElement("w:r")
                if rPr is not None:
                    run_despues.append(copy.deepcopy(rPr))
                t_despues = OxmlElement("w:t")
                t_despues.text = despues
                t_despues.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                run_despues.append(t_despues)
                reemplazos.append(run_despues)
            for nuevo in reemplazos:
                objetivo.addprevious(nuevo)
            pe.remove(objetivo)
            acciones.append({"parrafo": i, "url": url, "r_id": r_id})

    relaciones = sum(
        1
        for rel in documento.part.rels.values()
        if rel.reltype.endswith("/hyperlink") and rel.is_external
    )
    return {"hipervinculos": len(acciones), "relaciones_externas": relaciones, "acciones": acciones}


def escribir_leyenda_celda(documento, especificaciones: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Deja una celda con un único párrafo y una única leyenda, conservando el rPr
    del primer run y el pPr original. Elimina párrafos e instrucciones previas.
    """
    from docx.oxml import OxmlElement

    acciones: List[Dict[str, Any]] = []
    for item in especificaciones:
        tabla = documento.tables[int(item["tabla"])]
        tc = tabla.rows[int(item["fila"])].cells[int(item["columna"])]._tc
        parrafos = tc.findall(_qn("w:p"))
        primero = parrafos[0] if parrafos else None
        if primero is None:
            primero = OxmlElement("w:p")
            tc.append(primero)
        for extra in parrafos[1:]:
            tc.remove(extra)
        rPr = None
        for run in primero.findall(_qn("w:r")):
            rPr = run.find(_qn("w:rPr"))
            break
        for hijo in list(primero):
            if hijo.tag == _qn("w:pPr"):
                continue
            primero.remove(hijo)
        run = OxmlElement("w:r")
        if rPr is not None:
            import copy

            run.append(copy.deepcopy(rPr))
        t = OxmlElement("w:t")
        t.text = str(item["texto"])
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        run.append(t)
        primero.append(run)
        acciones.append(
            {
                "tabla": int(item["tabla"]),
                "fila": int(item["fila"]),
                "columna": int(item["columna"]),
                "texto": str(item["texto"]),
            }
        )
    return {"celdas": len(acciones), "acciones": acciones}


def sincronizar_entradas_indice(documento, reemplazos: Sequence[Dict[str, str]]) -> Dict[str, Any]:
    """
    Sincroniza el texto visible de las entradas de índices nativos (TOC \\c)
    cuando Word no regenera su resultado cacheado. Solo modifica nodos <w:t>
    de párrafos que contienen PAGEREF: conserva hipervínculos, campos y folios.
    """
    acciones: List[Dict[str, Any]] = []
    for i, parrafo in enumerate(documento.paragraphs):
        if not any("PAGEREF" in (x.text or "") for x in parrafo._p.iter(_qn("w:instrText"))):
            continue
        for run in parrafo._p.findall(".//" + _qn("w:r")):
            t = run.find(_qn("w:t"))
            if t is None or not t.text:
                continue
            for item in reemplazos:
                viejo = item["viejo"]
                nuevo = item["nuevo"]
                if viejo in t.text:
                    t.text = t.text.replace(viejo, nuevo, 1)
                    acciones.append({"parrafo": i, "viejo": viejo[:80], "nuevo": nuevo[:80]})
    return {"entradas_actualizadas": len(acciones), "acciones": acciones}


def _estilo_por_id(documento, style_id: str):
    for estilo in documento.styles:
        if (estilo.style_id or "") == style_id:
            return estilo
    raise KeyError(f"No existe el estilo con styleId '{style_id}'")


def _vaciar_parrafo(parrafo) -> None:
    """Retira todo el contenido visible del párrafo conservando su w:pPr."""
    pPr = parrafo._p.find(_qn("w:pPr"))
    for hijo in list(parrafo._p):
        if hijo is not pPr:
            parrafo._p.remove(hijo)


def _insertar_campo_pagina(parrafo, tamano_pt: float = 11.0) -> None:
    """Inyecta un campo PAGE nativo, centrado, con tipografía explícita."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.shared import Pt

    parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER

    def _run():
        run = parrafo.add_run()
        run.font.name = "Times New Roman"
        run.font.size = Pt(tamano_pt)
        rPr = run._r.find(_qn("w:rPr"))
        if rPr is not None:
            rFonts = rPr.find(_qn("w:rFonts"))
            if rFonts is None:
                rFonts = OxmlElement("w:rFonts")
                rPr.insert(0, rFonts)
            rFonts.set(_qn("w:cs"), "Times New Roman")
        return run

    inicio = _run()
    fld = OxmlElement("w:fldChar")
    fld.set(_qn("w:fldCharType"), "begin")
    inicio._r.append(fld)
    instruccion = _run()
    texto = OxmlElement("w:instrText")
    texto.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    texto.text = " PAGE "
    instruccion._r.append(texto)
    separador = _run()
    fld = OxmlElement("w:fldChar")
    fld.set(_qn("w:fldCharType"), "separate")
    separador._r.append(fld)
    resultado = _run()
    t = OxmlElement("w:t")
    t.text = "1"
    resultado._r.append(t)
    cierre = _run()
    fld = OxmlElement("w:fldChar")
    fld.set(_qn("w:fldCharType"), "end")
    cierre._r.append(fld)


def negrita_numeral_rotulos(documento) -> Dict[str, Any]:
    """
    Fija en negrita exclusivamente el campo SEQ (valor y código) de los rótulos
    Tabla/Figura del cuerpo. No toca el título descriptivo, los índices ni el
    texto que sigue al campo.
    """
    rotulos = 0
    runs_modificados = 0
    detalles = []
    for indice, parrafo in enumerate(documento.paragraphs):
        if "SEQ" not in parrafo._p.xml:
            continue
        dentro = False
        modificados = 0
        for run in parrafo.runs:
            fld = run._r.find(_qn("w:fldChar"))
            if fld is not None:
                tipo = fld.get(_qn("w:fldCharType"))
                if tipo == "begin":
                    dentro = True
                if dentro and run.font.bold is not True:
                    run.font.bold = True
                    modificados += 1
                if tipo == "end":
                    dentro = False
                continue
            if dentro and run.font.bold is not True:
                run.font.bold = True
                modificados += 1
        if modificados:
            rotulos += 1
            runs_modificados += modificados
            detalles.append({"indice_docx": indice, "rotulo": parrafo.text[:70], "runs": modificados})
    return {"rotulos_verificados": 103, "rotulos_ajustados": rotulos, "runs_modificados": runs_modificados, "detalles": detalles}


def aplicar_ajustes_formato_v20(documento, plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extensión aditiva de formato editorial v20. No sustituye texto, no toca
    imágenes ni ecuaciones y no reescribe tablas: solo normaliza fuentes de
    estilos, sangrías/alineaciones narrativas, espaciados de celdas, bordes de
    formularios, orden de rótulos fotográficos y paginación preliminar.

    Todas las operaciones son idempotentes y se reportan por separado para que
    la compuerta de conservación compare texto, tablas y OMML antes/después.
    """
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt
    from docx.text.paragraph import Paragraph

    acciones: List[Dict[str, Any]] = []

    # 1. Fuentes y tamaños de estilos institucionales (folios e índices).
    estilos = []
    for item in plan.get("estilos_fuente", []):
        estilo = _estilo_por_id(documento, item["style_id"])
        fuente = item.get("font", "Times New Roman")
        estilo.font.name = fuente
        rPr = estilo.element.find(_qn("w:rPr"))
        if rPr is not None:
            rFonts = rPr.find(_qn("w:rFonts"))
            if rFonts is None:
                from docx.oxml import OxmlElement

                rFonts = OxmlElement("w:rFonts")
                rPr.insert(0, rFonts)
            for atributo in ("asciiTheme", "hAnsiTheme", "cstheme"):
                if rFonts.get(_qn(f"w:{atributo}")) is not None:
                    del rFonts.attrib[_qn(f"w:{atributo}")]
            rFonts.set(_qn("w:cs"), fuente)
        if item.get("sz"):
            estilo.font.size = Pt(float(item["sz"]) / 2.0)
        estilos.append(
            {
                "style_id": item["style_id"],
                "fuente": fuente,
                "sz_medios_puntos": item.get("sz"),
            }
        )

    # 2. Nivel 3 real por w:outlineLvl: negrita + cursiva, sin tocar el texto.
    nivel3 = []
    if plan.get("nivel3_negrita_cursiva"):
        for i, parrafo in enumerate(documento.paragraphs):
            pPr = parrafo._p.find(_qn("w:pPr"))
            outline = pPr.find(_qn("w:outlineLvl")) if pPr is not None else None
            if outline is None or outline.get(_qn("w:val")) != "3":
                continue
            for run in parrafo.runs:
                run.bold = True
                run.italic = True
            nivel3.append(i)

    # 3. Alineación de notas y espaciado del bloque de advertencia.
    alineados = []
    for item in plan.get("parrafos_alineacion", []):
        valor = str(item.get("jc", "left")).lower()
        destino = {
            "left": WD_ALIGN_PARAGRAPH.LEFT,
            "center": WD_ALIGN_PARAGRAPH.CENTER,
            "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
        }[valor]
        for indice in item.get("indices", []):
            parrafo = documento.paragraphs[int(indice)]
            parrafo.alignment = destino
            alineados.append(int(indice))

    espaciados = []
    for item in plan.get("parrafos_espaciado", []):
        parrafo = documento.paragraphs[int(item["indice"])]
        if item.get("line"):
            parrafo.paragraph_format.line_spacing = float(item["line"]) / 240.0
        if item.get("first_line") is not None:
            parrafo.paragraph_format.first_line_indent = Cm(float(item["first_line"]) / 567.0)
        espaciados.append(int(item["indice"]))

    # 4. Celdas: espaciado heredado y runs de firma sin tipografía explícita.
    celdas_espaciadas = 0
    for indice in plan.get("celdas_espaciado", {}).get("tablas", []):
        tabla = documento.tables[int(indice)]
        for fila in tabla.rows:
            for celda in fila.cells:
                for parrafo in celda.paragraphs:
                    pPr = parrafo._p.find(_qn("w:pPr"))
                    spacing = pPr.find(_qn("w:spacing")) if pPr is not None else None
                    if spacing is not None and spacing.get(_qn("w:after")) is not None:
                        continue
                    parrafo.paragraph_format.space_after = Pt(0)
                    parrafo.paragraph_format.line_spacing = 1.0
                    celdas_espaciadas += 1

    firmas = 0
    for item in plan.get("runs_firma", []):
        for indice in item.get("tablas", []):
            tabla = documento.tables[int(indice)]
            fila = tabla.rows[int(item.get("fila", 1)) - 1]
            for celda in fila.cells:
                for parrafo in celda.paragraphs:
                    for run in parrafo.runs:
                        if not run.text.strip():
                            continue
                        run.font.name = item.get("font", "Times New Roman")
                        run.font.size = Pt(float(item.get("sz", 20)) / 2.0)
                        firmas += 1

    # 5. Rejilla declarada (DEC-025) solo en formularios y marcos de campo.
    def _sin_bordes_celda(tabla):
        quitados = 0
        for tc in tabla._tbl.iter(_qn("w:tc")):
            tcPr = tc.find(_qn("w:tcPr"))
            if tcPr is None:
                continue
            for bordes in tcPr.findall(_qn("w:tcBorders")):
                tcPr.remove(bordes)
                quitados += 1
        return quitados

    rejillas = []
    for item in plan.get("rejilla_formularios", []):
        sz = int(item.get("sz", 4))
        for indice in item.get("tablas", []):
            tabla = documento.tables[int(indice)]
            quitados = _sin_bordes_celda(tabla)
            aplicar_bordes_rejilla(tabla, sz=sz)
            verticales = False
            if item.get("verticales_por_celda"):
                from docx.oxml import OxmlElement

                tblPr = tabla._tbl.tblPr
                bordes = tblPr.find(_qn("w:tblBorders"))
                if bordes is not None:
                    inside = bordes.find(_qn("w:insideV"))
                    if inside is not None:
                        inside.set(_qn("w:val"), "nil")
                for tc in tabla._tbl.iter(_qn("w:tc")):
                    tcPr = tc.find(_qn("w:tcPr"))
                    if tcPr is None:
                        tcPr = OxmlElement("w:tcPr")
                        tc.insert(0, tcPr)
                    tcBorders = tcPr.find(_qn("w:tcBorders"))
                    if tcBorders is None:
                        tcBorders = OxmlElement("w:tcBorders")
                        tcPr.append(tcBorders)
                    for lado in ("left", "right"):
                        borde = tcBorders.find(_qn(f"w:{lado}"))
                        if borde is None:
                            borde = OxmlElement(f"w:{lado}")
                            tcBorders.append(borde)
                        borde.set(_qn("w:val"), "single")
                        borde.set(_qn("w:sz"), str(sz))
                        borde.set(_qn("w:space"), "0")
                        borde.set(_qn("w:color"), "000000")
                verticales = True
            rejillas.append(
                {
                    "tabla": int(indice),
                    "sz": sz,
                    "tcBorders_retirados": quitados,
                    "verticales_por_celda": verticales,
                }
            )

    marcos = []
    for item in plan.get("marcos_fotografia", []):
        sz = int(item.get("sz", 4))
        for indice in item.get("tablas", []):
            tabla = documento.tables[int(indice)]
            quitados = _sin_bordes_celda(tabla)
            aplicar_bordes_rejilla(tabla, sz=sz)
            movido = False
            if item.get("mover_rotulo"):
                tbl = tabla._tbl
                siguiente = tbl.getnext()
                if (
                    siguiente is not None
                    and siguiente.tag == _qn("w:p")
                    and "".join(n.text or "" for n in siguiente.iter(_qn("w:t"))).strip().startswith("Figura")
                ):
                    tbl.addprevious(siguiente)
                    caption = Paragraph(siguiente, documento._body)
                    caption.paragraph_format.keep_with_next = True
                    movido = True
            marcos.append(
                {
                    "tabla": int(indice),
                    "sz": sz,
                    "tcBorders_retirados": quitados,
                    "rotulo_movido_antes": movido,
                }
            )

    # 6. Folio romano centrado en pie para preliminares, sin contaminar el cuerpo.
    folio = {}
    if plan.get("folio_preliminar"):
        especificacion = plan["folio_preliminar"]
        indice = int(especificacion.get("seccion", 1))
        seccion = documento.sections[indice]
        if especificacion.get("encabezado_limpiar", True):
            _vaciar_parrafo(seccion.header.paragraphs[0])
        pie = seccion.footer
        pie.is_linked_to_previous = False
        for extra in list(pie.paragraphs[1:]):
            extra._p.getparent().remove(extra._p)
        _vaciar_parrafo(pie.paragraphs[0])
        _insertar_campo_pagina(pie.paragraphs[0], float(especificacion.get("tamano_pt", 11.0)))
        siguiente = int(especificacion.get("desvincular_pie_seccion", indice + 1))
        if siguiente < len(documento.sections):
            pie_siguiente = documento.sections[siguiente].footer
            pie_siguiente.is_linked_to_previous = False
            for parrafo in pie_siguiente.paragraphs:
                _vaciar_parrafo(parrafo)
            for extra in list(pie_siguiente.paragraphs[1:]):
                extra._p.getparent().remove(extra._p)
        folio = {
            "seccion": indice,
            "campo_pagina_en_pie": True,
            "encabezado_vaciado": True,
            "pie_seccion_siguiente_vacio": True,
            "formato_conservado": "lowerRoman start=2",
        }

    return {
        "estilos": estilos,
        "nivel3_negrita_cursiva": nivel3,
        "parrafos_alineados": alineados,
        "parrafos_espaciados": espaciados,
        "celdas_espaciadas": celdas_espaciadas,
        "runs_firma_normalizados": firmas,
        "rejillas": rejillas,
        "marcos_fotografia": marcos,
        "folio_preliminar": folio,
    }


def cirugia_extension(
    ruta_origen: Union[str, Path],
    ruta_destino: Union[str, Path],
    plan: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Aplica en una sola sesión las operaciones nativas del plan v17, en orden
    determinista y sin tocar el archivo de origen.
    """
    import docx

    origen = Path(ruta_origen)
    documento = docx.Document(str(origen))
    operaciones: List[Dict[str, Any]] = []
    indices_alto = [1, 8, 32, 33, 34, 35]
    alto_antes = {
        indice: _alto_estimado_tabla(documento.tables[indice])
        for indice in indices_alto
        if indice < len(documento.tables)
    }

    for item in plan.get("hipervinculos", []):
        operaciones.append(
            {
                "tipo": "hipervinculo",
                **reemplazar_en_hipervinculos(
                    documento,
                    int(item["indice_docx"]),
                    item["ancla_original"],
                    item["texto_nuevo"],
                    int(item.get("ocurrencias", 1)),
                ),
            }
        )

    if plan.get("hipervinculos_nativos"):
        operaciones.append(
            {
                "tipo": "hipervinculos_nativos",
                **convertir_urls_a_hipervinculos(
                    documento,
                    plan["hipervinculos_nativos"].get("desde", "REFERENCIAS BIBLIOGRÁFICAS"),
                    plan["hipervinculos_nativos"].get("hasta", "ANEXOS"),
                ),
            }
        )

    if plan.get("erradicar_raya"):
        operaciones.append(
            {
                "tipo": "erradicar_raya",
                **erradicar_raya_global(documento, str(plan["erradicar_raya"])),
            }
        )

    if plan.get("parrafos_reemplazo"):
        operaciones.append(
            {
                "tipo": "parrafos_reemplazo",
                **reemplazar_parrafos_completos(documento, plan["parrafos_reemplazo"]),
            }
        )

    if plan.get("referencias"):
        operaciones.append(
            {
                "tipo": "referencias",
                **insertar_referencias(documento, plan["referencias"]),
            }
        )

    for item in plan.get("formulas", []):
        operaciones.append(
            {
                "tipo": "formula_fraccion",
                **editar_formula_fraccion(
                    documento,
                    int(item["indice_parrafo"]),
                    item["numerador"],
                    item["denominador"],
                    int(item.get("ocurrencia", 0)),
                ),
            }
        )

    if plan.get("imagenes"):
        for item in plan["imagenes"]:
            operaciones.append(
                {
                    "tipo": "imagen",
                    **sustituir_imagen_figura(
                        documento,
                        int(item["indice_docx"]),
                        item["ruta"],
                        float(item["ancho_cm"]),
                        float(item["alto_cm"]) if item.get("alto_cm") else None,
                    ),
                }
            )

    if plan.get("redimensiones_figura"):
        for item in plan["redimensiones_figura"]:
            operaciones.append(
                {
                    "tipo": "redimension_figura",
                    **redimensionar_figura(
                        documento,
                        int(item["indice_parrafo"]),
                        float(item["ancho_cm"]),
                    ),
                }
            )

    if plan.get("cursivas"):
        especificacion = plan["cursivas"]
        if isinstance(especificacion, dict) and especificacion.get("especificacion_ruta"):
            especificacion = json.loads(
                Path(especificacion["especificacion_ruta"]).read_text(encoding="utf-8")
            )
            especificacion = especificacion.get("referencias", especificacion)
        operaciones.append({"tipo": "cursivas", **aplicar_cursivas_por_tramos(documento, especificacion)})

    if plan.get("jerarquia"):
        operaciones.append(
            {
                "tipo": "jerarquia",
                **normalizar_jerarquia_encabezados(
                    documento,
                    quitar_cursiva_nivel2=bool(plan["jerarquia"].get("quitar_cursiva_nivel2", True)),
                    nivel3_estilo=plan["jerarquia"].get("nivel3_estilo"),
                ),
            }
        )

    if plan.get("keep_next"):
        operaciones.append(
            {
                "tipo": "keep_next",
                **aplicar_keep_next(
                    documento,
                    indices=plan["keep_next"].get("indices", ()),
                    incluir_rotulos=bool(plan["keep_next"].get("incluir_rotulos", True)),
                    incluir_formulas=bool(plan["keep_next"].get("incluir_formulas", True)),
                ),
            }
        )

    if plan.get("subindices"):
        especificacion = plan["subindices"]
        ambito = especificacion.get("ambito", "ambos") if isinstance(especificacion, dict) else "cuerpo"
        operaciones.append(
            {
                "tipo": "subindices",
                **convertir_notacion_subindices(documento, especificacion, ambito=ambito),
            }
        )

    if plan.get("keep_next_ultima_fila"):
        especificacion = plan["keep_next_ultima_fila"]
        indices_ultima = especificacion.get("tablas", especificacion) if isinstance(especificacion, dict) else especificacion
        operaciones.append(
            {
                "tipo": "keep_next_ultima_fila",
                **aplicar_keep_next_ultima_fila(documento, [int(i) for i in indices_ultima]),
            }
        )

    if plan.get("notas"):
        operaciones.append(
            {
                "tipo": "notas",
                "acciones": insertar_prefijo_notas_especificas(documento, plan["notas"].get("indices", [])),
            }
        )

    if plan.get("listas"):
        especificacion = plan["listas"]
        if not isinstance(especificacion, dict):
            especificacion = {}
        operaciones.append(
            {
                "tipo": "normalizar_listas",
                **normalizar_listas_rotulos(
                    documento,
                    sangria_dxa=int(especificacion.get("sangria_dxa", 720)),
                    colgante_dxa=int(especificacion.get("colgante_dxa", 360)),
                    limpiar_espacios_prosa=bool(
                        especificacion.get("limpiar_espacios_prosa", True)
                    ),
                ),
            }
        )

    tablas = plan.get("tablas", {})
    for item in tablas.get("anexar_filas", []):
        operaciones.append(
            {
                "tipo": "anexar_filas",
                **anexar_filas_tabla(documento, int(item["tabla"]), item["filas"]),
            }
        )
    if tablas.get("eliminar_filas"):
        operaciones.append(
            {
                "tipo": "eliminar_filas",
                **eliminar_filas_tabla(documento, tablas["eliminar_filas"]),
            }
        )
    if tablas.get("celdas_texto"):
        operaciones.append(
            {
                "tipo": "celdas_texto",
                **escribir_celdas_texto(documento, tablas["celdas_texto"]),
            }
        )
    if tablas.get("celdas_leyenda"):
        operaciones.append(
            {
                "tipo": "celdas_leyenda",
                **escribir_leyenda_celda(documento, tablas["celdas_leyenda"]),
            }
        )
    if tablas.get("celdas_parrafos"):
        operaciones.append(
            {
                "tipo": "celdas_parrafos",
                **escribir_celdas_parrafos(documento, tablas["celdas_parrafos"]),
            }
        )
    for item in tablas.get("margenes_celda", []):
        operaciones.append(
            {
                "tipo": "margenes_celda",
                **ajustar_margenes_celda(
                    documento,
                    int(item["tabla"]),
                    int(item.get("izquierdo_dxa", 28)),
                    int(item.get("derecho_dxa", 28)),
                    int(item["superior_dxa"]) if item.get("superior_dxa") is not None else None,
                    int(item["inferior_dxa"]) if item.get("inferior_dxa") is not None else None,
                ),
            }
        )
    for item in tablas.get("geometria_proporcional", []):
        operaciones.append(
            {
                "tipo": "geometria_proporcional",
                **aplicar_geometria_proporcional(
                    documento,
                    int(item["tabla"]),
                    [int(a) for a in item["anchos_dxa"]],
                    int(item.get("margen_dxa", 60)),
                ),
            }
        )
    for item in tablas.get("ensanchar_rango", []):
        operaciones.append(
            {
                "tipo": "ensanche_rango",
                **ensanchar_rango_tabla(
                    documento,
                    int(item["tabla"]),
                    int(item["columna_objetivo"]),
                    int(item["ancho_objetivo_dxa"]),
                    {int(k): int(v) for k, v in item.get("donantes", {}).items()},
                    int(item.get("margen_dxa", 60)),
                ),
            }
        )
    for indice in tablas.get("reparar_tcw", []):
        operaciones.append(
            {
                "tipo": "reparar_tcw",
                **reparar_tcw_tabla(documento, int(indice)),
            }
        )
    for item in tablas.get("valign", []):
        operaciones.append(
            {
                "tipo": "valign",
                **aplicar_valign(
                    documento,
                    int(item["tabla"]),
                    str(item.get("valor", "top")),
                    bool(item.get("excepto_encabezado", True)),
                ),
            }
        )
    for item in tablas.get("alineacion_decimal", []):
        operaciones.append(
            {
                "tipo": "alineacion_decimal",
                **aplicar_alineacion_decimal(
                    documento,
                    int(item["tabla"]),
                    [int(c) for c in item["columnas"]],
                    str(item.get("modo", "tab_decimal")),
                ),
            }
        )
    if tablas.get("normalizar_tamano"):
        operaciones.append(
            {
                "tipo": "normalizar_tamano",
                **normalizar_tamano_minimo_tabla(
                    documento,
                    [int(item["tabla"]) for item in tablas["normalizar_tamano"]],
                    float(tablas["normalizar_tamano"][0].get("minimo_pt", 10.0)) if tablas["normalizar_tamano"] else 10.0,
                ),
            }
        )
    if tablas.get("rebalanceo"):
        rebalanceo = rebalancear_tabla(documento, [int(i) for i in tablas["rebalanceo"]])
        operaciones.append({"tipo": "rebalanceo", **rebalanceo})
    for indice in tablas.get("quitar_tblheader", []):
        operaciones.append(
            {
                "tipo": "quitar_tblheader",
                "tabla": int(indice),
                "retirado": retirar_encabezado_repetido(documento.tables[int(indice)]),
            }
        )
    for item in sorted(tablas.get("reorganizar_bloques", []), key=lambda x: int(x["tabla"]), reverse=True):
        operaciones.append(
            {
                "tipo": "reorganizar_bloques",
                **reorganizar_tabla_bloques(
                    documento,
                    int(item["tabla"]),
                    item.get("etiqueta_campo", "Campo"),
                    item.get("etiqueta_valor", "Contenido"),
                    int(item["ancho_etiqueta_dxa"]) if item.get("ancho_etiqueta_dxa") else None,
                    item.get("filas_extra"),
                ),
            }
        )

    if plan.get("estilo_indice"):
        operaciones.append(
            {
                "tipo": "estilo_indice",
                **ajustar_estilo_indice(
                    documento,
                    plan["estilo_indice"].get("nombre", "table of figures"),
                    int(plan["estilo_indice"].get("line", 240)),
                ),
            }
        )

    if plan.get("saltos_pagina"):
        operaciones.append(
            {
                "tipo": "saltos_pagina",
                **aplicar_salto_pagina_previo(documento, plan["saltos_pagina"].get("prefijos", [])),
            }
        )

    if plan.get("margenes_seccion"):
        valores = plan["margenes_seccion"]
        operaciones.append(
            {
                "tipo": "margenes_seccion",
                **normalizar_margenes_secciones(
                    documento,
                    float(valores.get("izquierdo_cm", 3.0)),
                    float(valores.get("derecho_cm", 2.5)),
                    float(valores.get("superior_cm", 2.5)),
                    float(valores.get("inferior_cm", 2.5)),
                ),
            }
        )

    if plan.get("sincronizar_indices"):
        operaciones.append(
            {
                "tipo": "sincronizar_indices",
                **sincronizar_entradas_indice(documento, plan["sincronizar_indices"]),
            }
        )

    if plan.get("dividir_parrafos"):
        for item in plan["dividir_parrafos"]:
            operaciones.append(
                {
                    "tipo": "dividir_parrafo",
                    **dividir_parrafo_por_saltos(
                        documento,
                        int(item["indice"]),
                        item.get("alineacion_lista", "left"),
                    ),
                }
            )

    if plan.get("ajustes_formato"):
        operaciones.append(
            {
                "tipo": "ajustes_formato",
                **aplicar_ajustes_formato_v20(documento, plan["ajustes_formato"]),
            }
        )

    if plan.get("negrilla_rotulos"):
        operaciones.append({"tipo": "negrilla_rotulos", **negrita_numeral_rotulos(documento)})

    destino = Path(ruta_destino)
    seguridad.asegurar_no_sobrescribe(origen, destino)
    seguridad.asegurar_escritura_permitida(destino)
    documento.save(str(destino))

    verificacion = docx.Document(str(destino))
    formulas = sum(
        1
        for p in verificacion.paragraphs
        if any(str(e.tag).endswith(("}oMath", "}oMathPara")) for e in p._p.iter())
    )
    tablas_verificadas = []
    for indice in [int(i) for i in tablas.get("rebalanceo", [])] + [
        int(item["tabla"]) for item in tablas.get("anexar_filas", [])
    ]:
        tabla = verificacion.tables[indice]
        tablas_verificadas.append(
            {
                "tabla": indice,
                "filas": len(tabla.rows),
                "columnas": len(tabla.columns),
                "cantSplit": all(
                    fila._tr.find(_qn("w:trPr")) is not None
                    and fila._tr.find(_qn("w:trPr")).find(_qn("w:cantSplit")) is not None
                    for fila in tabla.rows
                ),
            }
        )
    alto_despues = {
        indice: _alto_estimado_tabla(verificacion.tables[indice])
        for indice in indices_alto
        if indice < len(verificacion.tables)
    }
    alto_tablas = [
        {
            "tabla": indice,
            "alto_antes_pt": alto_antes[indice]["alto_estimado_pt"],
            "alto_despues_pt": alto_despues[indice]["alto_estimado_pt"],
            "delta_pt": round(
                alto_despues[indice]["alto_estimado_pt"] - alto_antes[indice]["alto_estimado_pt"], 1
            ),
        }
        for indice in indices_alto
        if indice in alto_antes and indice in alto_despues
    ]
    clases = {
        "margenes_celda": len(tablas.get("margenes_celda", [])),
        "geometria_proporcional": len(tablas.get("geometria_proporcional", [])),
        "ensanche_rango": len(tablas.get("ensanchar_rango", [])),
        "reparar_tcw": len(tablas.get("reparar_tcw", [])),
        "valign": len(tablas.get("valign", [])),
        "alineacion_decimal": len(tablas.get("alineacion_decimal", [])),
    }
    tablas_distintas = set()
    for clave in ("margenes_celda", "geometria_proporcional", "valign", "alineacion_decimal"):
        for item in tablas.get(clave, []):
            tablas_distintas.add(int(item["tabla"]))
    tablas_distintas.update(int(i) for i in tablas.get("reparar_tcw", []))
    tablas_distintas.update(int(item["tabla"]) for item in tablas.get("ensanchar_rango", []))
    fallidas = [op for op in operaciones if op.get("estado") == "fallida"]
    aplicadas = [op for op in operaciones if op.get("estado") != "fallida"]
    return {
        "origen": str(origen),
        "destino": str(destino),
        "sha256_origen": seguridad.sha256_archivo(origen),
        "sha256_destino": seguridad.sha256_archivo(destino),
        "parrafos": len(verificacion.paragraphs),
        "tablas": len(verificacion.tables),
        "formulas_omml": formulas,
        "operaciones": operaciones,
        "aplicadas": aplicadas,
        "fallidas": fallidas,
        "tablas_afectadas_por_clase": clases,
        "tablas_distintas_afectadas": sorted(tablas_distintas),
        "alto_tablas": alto_tablas,
        "tablas_verificadas": tablas_verificadas,
    }


# ===========================================================================
# CIRUGÍA ESTRUCTURAL: traslado nativo de bloques, injerto de tablas de otra
# fuente, normalización de rótulos en dos párrafos y renumeración continua.
# Todas las operaciones trabajan sobre el árbol OpenXML del documento y nunca
# reconstruyen texto degradado ni pierden campos, marcadores o relaciones.
# ===========================================================================

R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def _resolver_referencias(valor: Any, base_dir: Path) -> Any:
    """Resuelve nodos {"$ref": "archivo.json#/ruta/pointer"} contra el directorio del plan."""
    if isinstance(valor, dict):
        if set(valor.keys()) == {"$ref"}:
            destino = str(valor["$ref"])
            archivo, _, puntero = destino.partition("#")
            ruta = Path(archivo)
            if not ruta.is_absolute():
                ruta = (base_dir / ruta).resolve()
            datos = json.loads(ruta.read_text(encoding="utf-8"))
            actual = datos
            for tramo in [t for t in puntero.split("/") if t]:
                tramo = tramo.replace("~1", "/").replace("~0", "~")
                actual = actual[int(tramo)] if isinstance(actual, list) else actual[tramo]
            return _resolver_referencias(actual, base_dir)
        return {clave: _resolver_referencias(v, base_dir) for clave, v in valor.items()}
    if isinstance(valor, list):
        return [_resolver_referencias(v, base_dir) for v in valor]
    return valor


def _hijos_cuerpo(documento) -> List[Any]:
    return list(documento.element.body.iterchildren())


def _texto_elemento(el) -> str:
    if el is None:
        return ""
    return "".join(t.text or "" for t in el.iter(_qn("w:t")))


def _localizar_elemento(documento, ancla: str, modo: str = "prefijo",
                        ocurrencia: int = 1, desde=None, hasta=None) -> Any:
    """Ubica un elemento del cuerpo por su texto. modo: prefijo | contiene | exacto."""
    if not ancla:
        raise ValueError("Ancla vacía en el plan estructural")
    hijos = _hijos_cuerpo(documento)
    activo = desde is None
    vistos = 0
    for el in hijos:
        if not activo:
            if el is desde:
                activo = True
            continue
        if hasta is not None and el is hasta:
            break
        if el.tag not in (_qn("w:p"), _qn("w:tbl")):
            continue
        if el.tag == _qn("w:p"):
            estilo = el.find(_qn("w:pPr") + "/" + _qn("w:pStyle"))
            if estilo is not None and estilo.get(_qn("w:val")) in (
                    "Tabladeilustraciones", "Tabladecontenido", "TOC1", "TOC2", "TOC3"):
                continue
        texto = _texto_elemento(el).strip()
        if modo == "exacto":
            coincide = texto == ancla
        elif modo == "contiene":
            coincide = ancla in texto
        else:
            coincide = texto.startswith(ancla)
        if coincide:
            vistos += 1
            if vistos == ocurrencia:
                return el
    raise LookupError(f"No se localizó el ancla ({modo}): {ancla[:90]!r}")


def _rango_entre(documento, desde_ancla: str, hasta_ancla: str,
                 modo_desde: str = "prefijo", modo_hasta: str = "prefijo",
                 hasta_inclusive: bool = True) -> List[Any]:
    inicio = _localizar_elemento(documento, desde_ancla, modo_desde)
    hijos = _hijos_cuerpo(documento)
    i = hijos.index(inicio)
    fin = _localizar_elemento(documento, hasta_ancla, modo_hasta, desde=inicio)
    j = hijos.index(fin)
    if j < i:
        raise ValueError("El ancla final precede a la inicial en el rango pedido")
    return hijos[i: j + 1 if hasta_inclusive else j]


def _reemplazar_patron_parrafo(p, patron, funcion, maximo: Optional[int] = None) -> int:
    """Sustituye un patrón regex sobre el texto concatenado del párrafo conservando runs."""
    limite = maximo if maximo else 10 ** 6
    aplicadas = 0
    regex = re.compile(patron)
    desde = 0
    while aplicadas < limite:
        nodos = list(p.iter(_qn("w:t")))
        if not nodos:
            return aplicadas
        offsets, acumulado = [], 0
        for nodo in nodos:
            texto_nodo = nodo.text or ""
            offsets.append((acumulado, acumulado + len(texto_nodo)))
            acumulado += len(texto_nodo)
        texto = "".join(nodo.text or "" for nodo in nodos)
        coincidencia = regex.search(texto, desde)
        if not coincidencia:
            return aplicadas
        nuevo = funcion(coincidencia)
        if nuevo is None:
            return aplicadas
        if nuevo == coincidencia.group(0):
            # Coincidencia sin cambio: se avanza para no reencontrarla indefinidamente.
            desde = coincidencia.end()
            if desde >= len(texto):
                return aplicadas
            continue
        posicion, fin = coincidencia.start(), coincidencia.end()
        afectados = [k for k, (ini, ter) in enumerate(offsets)
                     if max(ini, posicion) < min(ter, fin)]
        if not afectados:
            return aplicadas
        primero, ultimo = afectados[0], afectados[-1]
        prefijo = (nodos[primero].text or "")[: posicion - offsets[primero][0]]
        sufijo = (nodos[ultimo].text or "")[fin - offsets[ultimo][0]:]
        nodos[primero].text = prefijo + nuevo
        for k in afectados[1:-1]:
            nodos[k].text = ""
        if ultimo != primero:
            nodos[ultimo].text = sufijo
        else:
            nodos[primero].text = prefijo + nuevo + sufijo
        for nodo in nodos:
            if nodo.text and (nodo.text != nodo.text.strip()):
                nodo.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        aplicadas += 1
        desde = 0
    return aplicadas


def _primer_rpr(p):
    for run in p.iter(_qn("w:r")):
        rpr = run.find(_qn("w:rPr"))
        if rpr is not None:
            return rpr
    return None


def _nuevo_run(rpr, texto: str, negrita: bool = False, cursiva: bool = False) -> Any:
    from docx.oxml import OxmlElement

    run = OxmlElement("w:r")
    rpr_nuevo = OxmlElement("w:rPr")
    if rpr is not None:
        import copy as _copy

        for hijo in _copy.deepcopy(rpr):
            if hijo.tag in (_qn("w:b"), _qn("w:i")):
                continue
            rpr_nuevo.append(hijo)
    if negrita:
        _rpr_propiedad(rpr_nuevo, "b", True)
    if cursiva:
        _rpr_propiedad(rpr_nuevo, "i", True)
    if rpr_nuevo.find(_qn("w:rFonts")) is None:
        fuentes = OxmlElement("w:rFonts")
        for atributo in ("w:ascii", "w:hAnsi", "w:cs"):
            fuentes.set(_qn(atributo), "Times New Roman")
        rpr_nuevo.insert(0, fuentes)
    if len(rpr_nuevo):
        run.append(rpr_nuevo)
    nodo = OxmlElement("w:t")
    nodo.text = texto
    nodo.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    run.append(nodo)
    return run


def _op_reemplazo_fragmento(documento, esp: Dict[str, Any]) -> Dict[str, Any]:
    ancla = esp["ancla"]
    parrafos = [el for el in _hijos_cuerpo(documento) if el.tag == _qn("w:p")]
    objetivo = _localizar_elemento(documento, ancla, esp.get("modo", "prefijo"))
    if "documento" in esp:
        # Restringe la búsqueda al bloque del resumen o del abstract.
        inicio = _localizar_elemento(documento, esp["documento"], "prefijo")
        hijos = _hijos_cuerpo(documento)
        objetivo = None
        for el in hijos[hijos.index(inicio):]:
            if el.tag == _qn("w:p") and ancla in _texto_elemento(el):
                objetivo = el
                break
        if objetivo is None:
            raise LookupError(f"Fragmento no hallado en {esp['documento']}: {ancla[:70]!r}")
    aplicar = 0
    for sustitucion in esp.get("sustituciones", []):
        aplicar += _reemplazar_flexible(objetivo, sustitucion["buscar"], sustitucion["reemplazar"])
    if not aplicar:
        raise LookupError(f"No se aplicó el fragmento: {ancla[:90]!r}")
    del parrafos
    return {"tipo": "reemplazo_fragmento", "ancla": ancla[:90], "sustituciones": aplicar}


def _op_reemplazo_parrafo(documento, esp: Dict[str, Any]) -> Dict[str, Any]:
    objetivo = _localizar_elemento(documento, esp["ancla"], esp.get("modo", "prefijo"))
    texto = esp["texto"]
    for sustitucion in esp.get("sustituciones", []):
        texto = texto.replace(sustitucion["buscar"], sustitucion["reemplazar"])
    rpr = _primer_rpr(objetivo)
    for run in list(objetivo.iter(_qn("w:r"))):
        objetivo.remove(run)
    objetivo.append(_nuevo_run(rpr, texto))
    return {"tipo": "reemplazo_parrafo", "ancla": esp["ancla"][:90],
            "caracteres": len(texto)}


def _op_renombrar_parrafo(documento, esp: Dict[str, Any]) -> Dict[str, Any]:
    """Cambia solo el encabezado numérico de un rótulo, conservando el resto del texto."""
    objetivo = _localizar_elemento(documento, esp["ancla"], esp.get("modo", "prefijo"))
    cambios = 0
    for viejo, nuevo in esp.get("cambios", {}).items():
        cambios += _reemplazar_texto_parrafo(objetivo, viejo, nuevo)
    if not cambios:
        raise LookupError(f"Renombrado sin efecto en: {esp['ancla'][:80]!r}")
    return {"tipo": "renombrar_parrafo", "ancla": esp["ancla"][:90], "cambios": cambios}


def _op_eliminar_rango(documento, esp: Dict[str, Any]) -> Dict[str, Any]:
    bloque = _rango_entre(documento, esp["desde"], esp["hasta"],
                          esp.get("modo_desde", "prefijo"), esp.get("modo_hasta", "prefijo"))
    cuerpo = documento.element.body
    for el in bloque:
        if el.tag == _qn("w:sectPr"):
            raise RuntimeError("El rango contiene un w:sectPr: se aborta para no perder secciones")
        cuerpo.remove(el)
    return {"tipo": "eliminar_rango", "desde": esp["desde"][:70],
            "hasta": esp["hasta"][:70], "elementos": len(bloque)}


def _op_trasladar_rango(documento, esp: Dict[str, Any]) -> Dict[str, Any]:
    inicio = _localizar_elemento(documento, esp["desde"], esp.get("modo_desde", "prefijo"))
    destino = _localizar_elemento(documento, esp["destino_despues_de"],
                                  esp.get("modo_destino", "prefijo"))
    bloque = _rango_entre(documento, esp["desde"], esp["hasta"],
                          esp.get("modo_desde", "prefijo"), esp.get("modo_hasta", "prefijo"))
    if any(el is destino for el in bloque):
        raise RuntimeError("El destino del traslado está dentro del bloque que se mueve")
    cuerpo = documento.element.body
    for el in bloque:
        if el.tag == _qn("w:sectPr"):
            raise RuntimeError("El rango contiene un w:sectPr: se aborta para no perder secciones")
        cuerpo.remove(el)
    ancla = destino
    for el in bloque:
        ancla.addnext(el)
        ancla = el
    del inicio
    return {"tipo": "trasladar_rango", "desde": esp["desde"][:70],
            "hasta": esp["hasta"][:70], "elementos": len(bloque),
            "destino": esp["destino_despues_de"][:70]}


def _op_trasladar_tabla(documento, esp: Dict[str, Any]) -> Dict[str, Any]:
    """Traslada una tabla nativa completa (``w:tbl``) a otra posición del cuerpo.

    ``trasladar_rango`` opera sobre párrafos, de modo que una tabla intercalada
    queda atrás y se separa de su rótulo. Esta operación mueve el objeto tabular
    con sus propiedades, filas, relaciones y estilos, sin reconstruirlo.
    """
    hijos = _hijos_cuerpo(documento)
    tablas = [el for el in hijos if el.tag == _qn("w:tbl")]
    if esp.get("contiene"):
        candidatas = [el for el in tablas if esp["contiene"] in _texto_elemento(el)]
        if len(candidatas) != 1:
            raise LookupError(
                f"'contiene' debe identificar una sola tabla; encontradas {len(candidatas)}"
            )
        tabla = candidatas[0]
    elif esp.get("indice_tabla") is not None:
        indice = int(esp["indice_tabla"])
        if indice < 0 or indice >= len(tablas):
            raise IndexError(f"índice de tabla fuera de rango: {indice}")
        tabla = tablas[indice]
    else:
        raise ValueError("trasladar_tabla requiere 'contiene' o 'indice_tabla'")
    modo = esp.get("modo", "prefijo")
    if esp.get("antes_de"):
        destino = _localizar_elemento(documento, esp["antes_de"], modo)
        if destino is tabla:
            raise RuntimeError("La tabla ya ocupa la posición indicada por el ancla")
        destino.addprevious(tabla)
        ubicacion = f"antes de {esp['antes_de'][:60]}"
    else:
        destino = _localizar_elemento(documento, esp["despues_de"], modo)
        if destino is tabla:
            raise RuntimeError("La tabla ya ocupa la posición indicada por el ancla")
        destino.addnext(tabla)
        ubicacion = f"después de {esp['despues_de'][:60]}"
    return {"tipo": "trasladar_tabla", "filas": len(tabla.findall(_qn("w:tr"))),
            "destino": ubicacion}


def _op_insertar_parrafos(documento, esp: Dict[str, Any]) -> Dict[str, Any]:
    from docx.oxml import OxmlElement

    ancla = _localizar_elemento(documento, esp["despues_de"], esp.get("modo", "prefijo"))
    modelo = esp.get("modelo_ancla")
    modelo_el = _localizar_elemento(documento, modelo, "prefijo") if modelo else None
    rpr_modelo = _primer_rpr(modelo_el) if modelo_el is not None else None
    ppr_modelo = modelo_el.find(_qn("w:pPr")) if modelo_el is not None else None
    insertados = []
    for especificacion in esp["parrafos"]:
        estilo = especificacion.get("estilo", "cuerpo")
        texto = especificacion["texto"]
        for sustitucion in esp.get("sustituciones", []):
            texto = texto.replace(sustitucion["buscar"], sustitucion["reemplazar"])
        for sustitucion in especificacion.get("sustituciones", []):
            texto = texto.replace(sustitucion["buscar"], sustitucion["reemplazar"])
        p = OxmlElement("w:p")
        if ppr_modelo is not None:
            import copy as _copy

            p.append(_copy.deepcopy(ppr_modelo))
        ppr = p.find(_qn("w:pPr"))
        if ppr is None:
            ppr = OxmlElement("w:pPr")
            p.insert(0, ppr)
        # Ajustes de estilo institucional por clase de párrafo.
        for hijo in list(ppr):
            if hijo.tag in (_qn("w:keepNext"), _qn("w:pageBreakBefore"), _qn("w:outlineLvl"),
                            _qn("w:ind"), _qn("w:jc"), _qn("w:spacing")):
                ppr.remove(hijo)
        espaciado = OxmlElement("w:spacing")
        sangria = OxmlElement("w:ind")
        sangria.set(_qn("w:left"), "0")
        justificacion = OxmlElement("w:jc")
        nivel_pendiente = None
        if estilo == "heading1":
            espaciado.set(_qn("w:before"), "240")
            espaciado.set(_qn("w:after"), "120")
            espaciado.set(_qn("w:line"), "360")
            espaciado.set(_qn("w:lineRule"), "auto")
            sangria.set(_qn("w:firstLine"), "0")
            justificacion.set(_qn("w:val"), "left")
            nivel = OxmlElement("w:outlineLvl")
            nivel.set(_qn("w:val"), "0")
            nivel_pendiente = nivel
        elif estilo == "heading2":
            espaciado.set(_qn("w:before"), "240")
            espaciado.set(_qn("w:after"), "120")
            espaciado.set(_qn("w:line"), "360")
            espaciado.set(_qn("w:lineRule"), "auto")
            sangria.set(_qn("w:firstLine"), "0")
            justificacion.set(_qn("w:val"), "left")
            nivel = OxmlElement("w:outlineLvl")
            nivel.set(_qn("w:val"), "1")
            nivel_pendiente = nivel
        elif estilo == "heading3":
            espaciado.set(_qn("w:before"), "240")
            espaciado.set(_qn("w:after"), "120")
            espaciado.set(_qn("w:line"), "360")
            espaciado.set(_qn("w:lineRule"), "auto")
            sangria.set(_qn("w:firstLine"), "0")
            justificacion.set(_qn("w:val"), "left")
            nivel = OxmlElement("w:outlineLvl")
            nivel.set(_qn("w:val"), "2")
            nivel_pendiente = nivel
        elif estilo == "rotulo":
            espaciado.set(_qn("w:before"), "240")
            espaciado.set(_qn("w:after"), "0")
            espaciado.set(_qn("w:line"), "360")
            espaciado.set(_qn("w:lineRule"), "auto")
            sangria.set(_qn("w:firstLine"), "0")
            justificacion.set(_qn("w:val"), "left")
            ppr.append(OxmlElement("w:keepNext"))
        elif estilo == "titulo_rotulo":
            espaciado.set(_qn("w:before"), "0")
            espaciado.set(_qn("w:after"), "40")
            espaciado.set(_qn("w:line"), "360")
            espaciado.set(_qn("w:lineRule"), "auto")
            sangria.set(_qn("w:firstLine"), "0")
            justificacion.set(_qn("w:val"), "left")
            ppr.append(OxmlElement("w:keepNext"))
        elif estilo == "nota":
            espaciado.set(_qn("w:before"), "40")
            espaciado.set(_qn("w:after"), "240")
            espaciado.set(_qn("w:line"), "240")
            espaciado.set(_qn("w:lineRule"), "auto")
            sangria.set(_qn("w:firstLine"), "0")
            justificacion.set(_qn("w:val"), "both")
        else:  # cuerpo
            espaciado.set(_qn("w:before"), "0")
            espaciado.set(_qn("w:after"), "0")
            espaciado.set(_qn("w:line"), "360")
            espaciado.set(_qn("w:lineRule"), "auto")
            sangria.set(_qn("w:firstLine"), "720")
            justificacion.set(_qn("w:val"), "both")
        if especificacion.get("salto_pagina"):
            ppr.append(OxmlElement("w:pageBreakBefore"))
        ppr.append(espaciado)
        ppr.append(sangria)
        ppr.append(justificacion)
        if nivel_pendiente is not None:
            ppr.append(nivel_pendiente)
        negrita = estilo in ("heading1", "heading2", "rotulo")
        cursiva = estilo == "titulo_rotulo"
        tamano = 19 if estilo == "nota" else 24
        rpr = None
        if rpr_modelo is not None:
            import copy as _copy

            rpr = _copy.deepcopy(rpr_modelo)
            for hijo in list(rpr):
                if hijo.tag in (_qn("w:b"), _qn("w:i"), _qn("w:sz"), _qn("w:szCs")):
                    rpr.remove(hijo)
        run = _nuevo_run(rpr, texto, negrita=negrita, cursiva=cursiva)
        rpr_run = run.find(_qn("w:rPr"))
        if rpr_run is None:
            rpr_run = OxmlElement("w:rPr")
            run.insert(0, rpr_run)
        for etiqueta in ("sz", "szCs"):
            nodo = OxmlElement(f"w:{etiqueta}")
            nodo.set(_qn("w:val"), str(tamano))
            rpr_run.append(nodo)
        p.append(run)
        ancla.addnext(p)
        ancla = p
        insertados.append(estilo)
    return {"tipo": "insertar_parrafos", "despues_de": esp["despues_de"][:70],
            "parrafos": len(insertados), "estilos": insertados}


def _mapa_relaciones(origen_part, destino_part, elemento) -> int:
    """Revincula imágenes y enlaces externos del XML copiado a la parte destino."""
    remapeadas = 0
    for nodo in elemento.iter():
        for atributo, valor in list(nodo.attrib.items()):
            if not atributo.startswith("{" + R_NS + "}"):
                continue
            try:
                rel = origen_part.rels[valor]
            except KeyError:
                continue
            if rel.is_external:
                nuevo = destino_part.relate_to(rel.target_ref, rel.reltype, is_external=True)
            else:
                nuevo = destino_part.relate_to(rel.target_part, rel.reltype)
            nodo.set(atributo, nuevo)
            remapeadas += 1
    return remapeadas


def _asegurar_estilos(documento, origen_documento, elemento) -> List[str]:
    """Copia las definiciones de estilo referidas por el injerto que falten en el destino."""
    import copy as _copy

    destino_part = documento.part
    origen_part = origen_documento.part
    destino_ids = {s.get(_qn("w:styleId")) for s in destino_part.styles.element.findall(_qn("w:style"))}
    origen_estilos = {s.get(_qn("w:styleId")): s for s in origen_part.styles.element.findall(_qn("w:style"))}
    pendientes = set()
    for etiqueta in ("w:pStyle", "w:rStyle", "w:tblStyle"):
        for nodo in elemento.iter(_qn(etiqueta)):
            valor = nodo.get(_qn("w:val"))
            if valor:
                pendientes.add(valor)
    copiados = []
    while pendientes:
        style_id = pendientes.pop()
        if not style_id or style_id in destino_ids:
            continue
        definicion = origen_estilos.get(style_id)
        if definicion is None:
            continue
        copia = _copy.deepcopy(definicion)
        destino_part.styles.element.append(copia)
        destino_ids.add(style_id)
        copiados.append(style_id)
        for etiqueta in ("w:basedOn", "w:next", "w:link"):
            for nodo in copia.iter(_qn(etiqueta)):
                pendientes.add(nodo.get(_qn("w:val")))
    return copiados


def _escalar_tabla(tabla, maximo_dxa: int = 8765) -> Dict[str, Any]:
    grid = tabla.find(_qn("w:tblGrid"))
    anchos = []
    if grid is not None:
        for col in grid.findall(_qn("w:gridCol")):
            anchos.append(int(col.get(_qn("w:w")) or 0))
    if not anchos:
        return {"escalada": False, "motivo": "tabla sin w:gridCol"}
    total = sum(anchos)
    if total <= maximo_dxa:
        return {"escalada": False, "ancho_original_dxa": total}
    factor = maximo_dxa / float(total)
    nuevos = [max(240, int(round(a * factor))) for a in anchos]
    for col, nuevo in zip(grid.findall(_qn("w:gridCol")), nuevos):
        col.set(_qn("w:w"), str(nuevo))
    for fila in tabla.findall(_qn("w:tr")):
        for celda, nuevo in zip(fila.findall(_qn("w:tc")), nuevos):
            tcw = celda.find(_qn("w:tcW"))
            if tcw is None:
                tcw = _etiqueta_hija(celda, "w:tcW")
            tcw.set(_qn("w:w"), str(nuevo))
            tcw.set(_qn("w:type"), "dxa")
    tblw = tabla.find(_qn("w:tblPr") + "/" + _qn("w:tblW"))
    if tblw is not None:
        tblw.set(_qn("w:w"), str(sum(nuevos)))
        tblw.set(_qn("w:type"), "dxa")
    return {"escalada": True, "ancho_original_dxa": total, "ancho_final_dxa": sum(nuevos),
            "factor": round(factor, 4)}


def _etiqueta_hija(padre, etiqueta: str):
    from docx.oxml import OxmlElement

    nodo = padre.find(_qn(etiqueta))
    if nodo is not None:
        return nodo
    return _insertar_hijo_ordenado(padre, OxmlElement(etiqueta))


def _insertar_hijo_ordenado(padre, nodo):
    orden = ["w:tcW", "w:gridSpan", "w:hMerge", "w:vMerge", "w:tcBorders", "w:shd", "w:noWrap",
             "w:tcMar", "w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark"]
    nombre = nodo.tag.split("}")[1]
    posicion = orden.index("w:" + nombre) if ("w:" + nombre) in orden else len(orden)
    for indice, hijo in enumerate(list(padre)):
        clave = "w:" + hijo.tag.split("}")[1]
        if clave in orden and orden.index(clave) > posicion:
            padre.insert(indice, nodo)
            return nodo
    padre.append(nodo)
    return nodo


def _nuevo_rotulo_numero(documento, etiqueta: str, numero: int, titulo: str,
                        nota: Optional[str] = None, lead_in: Optional[str] = None,
                        marcador: Optional[str] = None) -> List[Any]:
    """Construye rótulo (con campo SEQ y marcador) y título cursiva en párrafos separados."""
    from docx.oxml import OxmlElement

    elementos = []
    if lead_in:
        p = OxmlElement("w:p")
        ppr = OxmlElement("w:pPr")
        espaciado = OxmlElement("w:spacing")
        espaciado.set(_qn("w:before"), "0")
        espaciado.set(_qn("w:after"), "0")
        espaciado.set(_qn("w:line"), "360")
        espaciado.set(_qn("w:lineRule"), "auto")
        sangria = OxmlElement("w:ind")
        sangria.set(_qn("w:firstLine"), "720")
        sangria.set(_qn("w:left"), "0")
        jc = OxmlElement("w:jc")
        jc.set(_qn("w:val"), "both")
        ppr.append(espaciado)
        ppr.append(sangria)
        ppr.append(jc)
        p.append(ppr)
        p.append(_nuevo_run(None, lead_in))
        elementos.append(p)

    # Párrafo del rótulo: "Tabla N" en negrita con campo SEQ y marcador.
    p = OxmlElement("w:p")
    ppr = OxmlElement("w:pPr")
    estilo = OxmlElement("w:pStyle")
    estilo.set(_qn("w:val"), "Rotulodeilustracion")
    ppr.append(estilo)
    ppr.append(OxmlElement("w:keepNext"))
    espaciado = OxmlElement("w:spacing")
    espaciado.set(_qn("w:before"), "240")
    espaciado.set(_qn("w:after"), "0")
    espaciado.set(_qn("w:line"), "360")
    espaciado.set(_qn("w:lineRule"), "auto")
    ppr.append(espaciado)
    sangria = OxmlElement("w:ind")
    sangria.set(_qn("w:firstLine"), "0")
    sangria.set(_qn("w:left"), "0")
    ppr.append(sangria)
    jc = OxmlElement("w:jc")
    jc.set(_qn("w:val"), "left")
    ppr.append(jc)
    p.append(ppr)
    nombre = marcador or f"_Toc9{abs(hash((etiqueta, numero, titulo))) % 900000 + 100000}"
    inicio = OxmlElement("w:bookmarkStart")
    inicio.set(_qn("w:id"), str(abs(hash(nombre)) % 9000 + 1000))
    inicio.set(_qn("w:name"), nombre)
    p.append(inicio)
    p.append(_nuevo_run(None, f"{etiqueta} ", negrita=True))
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    _rpr_propiedad(rpr, "b", True)
    run.append(rpr)
    campo = OxmlElement("w:fldChar")
    campo.set(_qn("w:fldCharType"), "begin")
    run.append(campo)
    p.append(run)
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    _rpr_propiedad(rpr, "b", True)
    run.append(rpr)
    instr = OxmlElement("w:instrText")
    instr.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    instr.text = f" SEQ {etiqueta} \\* ARABIC \\r {numero} "
    run.append(instr)
    p.append(run)
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    _rpr_propiedad(rpr, "b", True)
    run.append(rpr)
    separador = OxmlElement("w:fldChar")
    separador.set(_qn("w:fldCharType"), "separate")
    run.append(separador)
    p.append(run)
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    _rpr_propiedad(rpr, "b", True)
    rpr.append(OxmlElement("w:noProof"))
    run.append(rpr)
    numero_nodo = OxmlElement("w:t")
    numero_nodo.text = str(numero)
    run.append(numero_nodo)
    p.append(run)
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    _rpr_propiedad(rpr, "b", True)
    run.append(rpr)
    cierre = OxmlElement("w:fldChar")
    cierre.set(_qn("w:fldCharType"), "end")
    run.append(cierre)
    p.append(run)
    elementos.append(p)

    # Título descriptivo en cursiva, en párrafo propio, con cierre del marcador.
    p = OxmlElement("w:p")
    ppr = OxmlElement("w:pPr")
    estilo = OxmlElement("w:pStyle")
    estilo.set(_qn("w:val"), "Rotulodeilustracion")
    ppr.append(estilo)
    ppr.append(OxmlElement("w:keepNext"))
    espaciado = OxmlElement("w:spacing")
    espaciado.set(_qn("w:before"), "0")
    espaciado.set(_qn("w:after"), "40")
    espaciado.set(_qn("w:line"), "360")
    espaciado.set(_qn("w:lineRule"), "auto")
    ppr.append(espaciado)
    sangria = OxmlElement("w:ind")
    sangria.set(_qn("w:firstLine"), "0")
    sangria.set(_qn("w:left"), "0")
    ppr.append(sangria)
    jc = OxmlElement("w:jc")
    jc.set(_qn("w:val"), "left")
    ppr.append(jc)
    p.append(ppr)
    p.append(_nuevo_run(None, titulo, cursiva=True))
    fin = OxmlElement("w:bookmarkEnd")
    fin.set(_qn("w:id"), inicio.get(_qn("w:id")))
    p.append(fin)
    elementos.append(p)

    if nota:
        p = OxmlElement("w:p")
        ppr = OxmlElement("w:pPr")
        espaciado = OxmlElement("w:spacing")
        espaciado.set(_qn("w:before"), "40")
        espaciado.set(_qn("w:after"), "240")
        espaciado.set(_qn("w:line"), "240")
        espaciado.set(_qn("w:lineRule"), "auto")
        sangria = OxmlElement("w:ind")
        sangria.set(_qn("w:firstLine"), "0")
        sangria.set(_qn("w:left"), "0")
        jc = OxmlElement("w:jc")
        jc.set(_qn("w:val"), "both")
        ppr.append(espaciado)
        ppr.append(sangria)
        ppr.append(jc)
        p.append(ppr)
        run = _nuevo_run(None, nota)
        rpr = run.find(_qn("w:rPr"))
        if rpr is None:
            rpr = OxmlElement("w:rPr")
            run.insert(0, rpr)
        tamano = OxmlElement("w:sz")
        tamano.set(_qn("w:val"), "19")
        rpr.append(tamano)
        p.append(run)
        elementos.append(p)
    return elementos


def aplicar_bordes_apa7_tabla(tabla) -> None:
    """Fija las tres líneas horizontales APA 7 sobre una tabla nativa (CT_Tbl o Table).

    Se aplica de forma selectiva a las tablas injertadas y no al documento completo,
    porque los formularios de campo conservan por decisión expresa su rejilla visible.
    """
    from docx.oxml import OxmlElement

    tbl = getattr(tabla, "_tbl", tabla)
    tblPr = tbl.tblPr
    if tblPr is None:
        return
    previos = tblPr.find(_qn("w:tblBorders"))
    if previos is not None:
        tblPr.remove(previos)
    bordes = OxmlElement("w:tblBorders")
    for borde in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{borde}")
        if borde in ("top", "bottom"):
            el.set(_qn("w:val"), "single")
            el.set(_qn("w:sz"), "8")
            el.set(_qn("w:space"), "0")
            el.set(_qn("w:color"), "000000")
        else:
            el.set(_qn("w:val"), "none")
            el.set(_qn("w:sz"), "0")
            el.set(_qn("w:space"), "0")
            el.set(_qn("w:color"), "auto")
        bordes.append(el)
    tblPr.insert_element_before(
        bordes,
        "w:shd",
        "w:tblLayout",
        "w:tblCellMar",
        "w:tblLook",
        "w:tblCaption",
        "w:tblDescription",
    )
    filas = tbl.findall(_qn("w:tr"))
    if not filas:
        return
    for tc in filas[0].findall(_qn("w:tc")):
        tcPr = tc.find(_qn("w:tcPr"))
        if tcPr is None:
            tcPr = OxmlElement("w:tcPr")
            tc.insert(0, tcPr)
        previos_celda = tcPr.find(_qn("w:tcBorders"))
        if previos_celda is not None:
            tcPr.remove(previos_celda)
        borde_celda = OxmlElement("w:tcBorders")
        abajo = OxmlElement("w:bottom")
        abajo.set(_qn("w:val"), "single")
        abajo.set(_qn("w:sz"), "4")
        abajo.set(_qn("w:space"), "0")
        abajo.set(_qn("w:color"), "000000")
        borde_celda.append(abajo)
        tcPr.insert_element_before(
            borde_celda,
            "w:shd",
            "w:noWrap",
            "w:tcMar",
            "w:textDirection",
            "w:tcFitText",
            "w:vAlign",
            "w:hideMark",
        )


def _normalizar_runs_tabla(tabla, tamano: int = 20) -> int:
    """Fija Times New Roman y el tamaño de celda (medios puntos) en todos los runs."""
    cambios = 0
    for run in tabla.iter(_qn("w:r")):
        rpr = run.find(_qn("w:rPr"))
        if rpr is None:
            from docx.oxml import OxmlElement

            rpr = OxmlElement("w:rPr")
            run.insert(0, rpr)
        fuentes = _rpr_propiedad(rpr, "rFonts", True)
        for atributo in ("ascii", "hAnsi", "cs"):
            fuentes.set(_qn(f"w:{atributo}"), "Times New Roman")
        for etiqueta in ("sz", "szCs"):
            nodo = _rpr_propiedad(rpr, etiqueta, True)
            nodo.set(_qn("w:val"), str(tamano))
        cambios += 1
    return cambios


def _op_injertar_tabla(documento, esp: Dict[str, Any]) -> Dict[str, Any]:
    import copy as _copy
    import docx as _docx

    origen = _docx.Document(str(esp["archivo"]))
    indice = int(esp["indice_tabla"])
    tabla_origen = origen.tables[indice]._tbl
    copia = _copy.deepcopy(tabla_origen)
    remapeadas = _mapa_relaciones(origen.part, documento.part, copia)
    estilos = _asegurar_estilos(documento, origen, copia)
    geometria = _escalar_tabla(copia, int(esp.get("ancho_max_dxa", 8765)))
    if esp.get("bordes_apa7", True):
        aplicar_bordes_apa7_tabla(copia)
    runs_normalizados = _normalizar_runs_tabla(copia, int(esp.get("tamano_celda", 20)))
    filas = copia.findall(_qn("w:tr"))
    for posicion, fila in enumerate(filas):
        _preparar_tr(fila, cant_split=True, tbl_header=(posicion == 0))
    ancla = _localizar_elemento(documento, esp["despues_de"], esp.get("modo", "prefijo")) \
        if esp.get("despues_de") else None
    if ancla is None:
        ancla = _localizar_elemento(documento, esp["antes_de"], esp.get("modo", "prefijo"))
    insertar_antes = ancla is not None and esp.get("despues_de") is None
    previos = _nuevo_rotulo_numero(
        documento,
        esp.get("rotulo", "Tabla"),
        int(esp.get("numero", 900)),
        esp["titulo"],
        nota=esp.get("nota"),
        lead_in=esp.get("lead_in"),
    )
    secuencia = previos + [copia]
    if insertar_antes:
        for el in secuencia:
            ancla.addprevious(el)
    else:
        for el in secuencia:
            ancla.addnext(el)
            ancla = el
    return {"tipo": "injertar_tabla", "archivo": str(esp["archivo"]), "indice": indice,
            "filas": len(filas), "relaciones": remapeadas, "estilos": estilos,
            "geometria": geometria, "runs_normalizados": runs_normalizados,
            "titulo": esp["titulo"][:80]}


def _op_eliminar_tabla_con_rotulo(documento, esp: Dict[str, Any]) -> Dict[str, Any]:
    rotulo = _localizar_elemento(documento, esp["rotulo"], esp.get("modo", "prefijo"))
    hijos = _hijos_cuerpo(documento)
    indice = hijos.index(rotulo)
    for posicion in range(indice, min(indice + 6, len(hijos))):
        if hijos[posicion].tag == _qn("w:tbl"):
            objetivo = hijos[posicion]
            break
    else:
        raise LookupError("No se halló la tabla asociada al rótulo indicado")
    cuerpo = documento.element.body
    retirados = []
    for el in (rotulo, objetivo):
        cuerpo.remove(el)
        retirados.append(el.tag.split("}")[1])
    if esp.get("retirar_nota"):
        siguiente = objetivo.getnext()
        if siguiente is not None and siguiente.tag == _qn("w:p") and \
                _texto_elemento(siguiente).strip().startswith(("Nota.", "Nota ", "Fuente")):
            cuerpo.remove(siguiente)
            retirados.append("nota")
    return {"tipo": "eliminar_tabla_con_rotulo", "rotulo": esp["rotulo"][:80],
            "retirados": retirados}


def _dividir_rotulo(p) -> Optional[Dict[str, str]]:
    """Separa el rótulo (negrita, con SEQ) del título (cursiva) en dos párrafos nativos."""
    import copy as _copy
    from docx.oxml import OxmlElement

    runs = p.findall(_qn("w:r"))
    fin_campo = None
    for posicion, run in enumerate(runs):
        fld = run.find(_qn("w:fldChar"))
        if fld is not None and fld.get(_qn("w:fldCharType")) == "end":
            fin_campo = posicion
    if fin_campo is None:
        return None
    posteriores = runs[fin_campo + 1:]
    titulo_runs = []
    for run in posteriores:
        texto = _texto_parrafo(run)
        if not titulo_runs:
            if not texto.strip():
                continue
            run_t = run.find(_qn("w:t"))
            if run_t is not None:
                run_t.text = (run_t.text or "").lstrip()
            titulo_runs.append(run)
        else:
            titulo_runs.append(run)
    if not titulo_runs:
        return None
    texto_titulo = "".join(_texto_parrafo(r) for r in titulo_runs).strip()
    if not texto_titulo:
        return None

    # Párrafo del título: mismo estilo, sin sangría, keepNext con el objeto.
    nuevo = OxmlElement("w:p")
    ppr = p.find(_qn("w:pPr"))
    if ppr is not None:
        nuevo.append(_copy.deepcopy(ppr))
    ppr_nuevo = nuevo.find(_qn("w:pPr"))
    if ppr_nuevo is not None:
        for etiqueta in ("w:ind", "w:spacing"):
            for hijo in ppr_nuevo.findall(_qn(etiqueta)):
                ppr_nuevo.remove(hijo)
        espaciado = OxmlElement("w:spacing")
        espaciado.set(_qn("w:before"), "0")
        espaciado.set(_qn("w:after"), "120")
        espaciado.set(_qn("w:line"), "360")
        espaciado.set(_qn("w:lineRule"), "auto")
        sangria = OxmlElement("w:ind")
        sangria.set(_qn("w:firstLine"), "0")
        sangria.set(_qn("w:left"), "0")
        ppr_nuevo.append(espaciado)
        ppr_nuevo.append(sangria)
        if ppr_nuevo.find(_qn("w:keepNext")) is None:
            ppr_nuevo.insert(0, OxmlElement("w:keepNext"))

    # El cierre del marcador acompaña al título para que la referencia abarque ambos.
    cierres = [h for h in p.iter(_qn("w:bookmarkEnd"))]
    for run in titulo_runs:
        p.remove(run)
        for hijo in list(run):
            if hijo.tag == _qn("w:rPr"):
                if hijo.find(_qn("w:i")) is None:
                    _rpr_propiedad(hijo, "i", True)
                if hijo.find(_qn("w:b")) is not None:
                    _rpr_propiedad(hijo, "b", False)
        nuevo.append(run)
    for cierre in cierres:
        p.remove(cierre)
        nuevo.append(cierre)

    # El rótulo queda sin espacio final y con el número en negrita.
    for run in runs[: fin_campo + 1]:
        rpr = run.find(_qn("w:rPr"))
        if rpr is not None and rpr.find(_qn("w:b")) is None:
            _rpr_propiedad(rpr, "b", True)
    for nodo in reversed([t for t in p.iter(_qn("w:t")) if (t.text or "").strip()]):
        nodo.text = (nodo.text or "").rstrip()
        break
    etiqueta = _texto_parrafo(p).strip()
    etiqueta = re.sub(r"\s+", " ", etiqueta)
    p.addnext(nuevo)
    return {"rotulo": etiqueta, "titulo": texto_titulo}


def _es_rotulo_con_secuencia(el) -> bool:
    if el.tag != _qn("w:p"):
        return False
    texto = _texto_elemento(el).strip()
    if not re.match(r"^(Tabla|Figura)\s+\d+", texto):
        return False
    return any("SEQ" in (t.text or "") for t in el.iter(_qn("w:instrText")))


def normalizar_rotulos_dos_parrafos(documento) -> Dict[str, Any]:
    """Rótulo en negrita y título en cursiva en párrafos separados, con campos intactos."""
    divididos, sin_titulo = [], []
    for el in _hijos_cuerpo(documento):
        if not _es_rotulo_con_secuencia(el):
            continue
        resultado = _dividir_rotulo(el)
        if resultado is None:
            sin_titulo.append(_texto_elemento(el).strip()[:80])
            continue
        divididos.append(resultado)
    return {"rotulos_divididos": len(divididos), "sin_titulo": sin_titulo,
            "detalle": [d["rotulo"] for d in divididos]}


def _marcador_y_numero(el) -> Tuple[Optional[str], int]:
    nombre = None
    for inicio in el.iter(_qn("w:bookmarkStart")):
        valor = inicio.get(_qn("w:name"))
        if valor:
            nombre = valor
            break
    texto = _texto_elemento(el).strip()
    coincidencia = re.match(r"^(Tabla|Figura)\s+(\d+)", texto)
    numero = int(coincidencia.group(2)) if coincidencia else 0
    return nombre, numero


def _titulo_de_rotulo(el) -> str:
    siguiente = el.getnext()
    if siguiente is not None and siguiente.tag == _qn("w:p"):
        texto = _texto_elemento(siguiente).strip()
        if texto and not re.match(r"^(Nota\.|Fuente:|Tabla\s|Figura\s)", texto):
            return texto
    return ""


def renumerar_etiquetas(documento, llamadas: bool = True,
                        etiquetas: Sequence[str] = ("Tabla", "Figura")) -> Dict[str, Any]:
    """Renumera de forma continua rótulos, cachés de SEQ y llamadas del cuerpo."""
    hijos = _hijos_cuerpo(documento)
    rotulos = {etiqueta: [] for etiqueta in etiquetas}
    for el in hijos:
        if not _es_rotulo_con_secuencia(el):
            continue
        texto = _texto_elemento(el).strip()
        coincidencia = re.match(r"^(Tabla|Figura)\s+\d+", texto)
        if coincidencia and coincidencia.group(1) in rotulos:
            rotulos[coincidencia.group(1)].append(el)

    mapas: Dict[str, Dict[int, int]] = {}
    cambios_rotulo = 0
    cambios_codigo = 0
    for etiqueta, elementos in rotulos.items():
        mapa: Dict[int, int] = {}
        for posicion, el in enumerate(elementos, start=1):
            _, viejo = _marcador_y_numero(el)
            if viejo and viejo not in mapa:
                mapa[viejo] = posicion
            # Sincroniza el código del campo: SEQ ... \* ARABIC \r <número>.
            for instr in el.iter(_qn("w:instrText")):
                codigo = instr.text or ""
                if "SEQ" not in codigo:
                    continue
                nuevo_codigo = re.sub(r"\\r\s+\d+", f"\\\\r {posicion}", codigo, count=1)
                if nuevo_codigo != codigo:
                    instr.text = nuevo_codigo
                    cambios_codigo += 1
            # Reescribe la caché del número dentro del campo SEQ.
            dentro = False
            for run in el.findall(_qn("w:r")):
                fld = run.find(_qn("w:fldChar"))
                if fld is not None:
                    tipo = fld.get(_qn("w:fldCharType"))
                    if tipo == "separate":
                        dentro = True
                    elif tipo == "end":
                        dentro = False
                elif dentro:
                    for nodo in run.iter(_qn("w:t")):
                        if nodo.text and nodo.text.strip() == str(viejo):
                            nodo.text = str(posicion)
                            cambios_rotulo += 1
        mapas[etiqueta] = mapa

    cambios_llamadas = 0
    if llamadas:
        patron = re.compile(r"\b(Tabla|Figura)\s+(\d+)\b")
        marcados = []
        for el in hijos:
            if el.tag != _qn("w:p"):
                continue
            estilo = el.find(_qn("w:pPr") + "/" + _qn("w:pStyle"))
            if estilo is not None and estilo.get(_qn("w:val")) == "Tabladeilustraciones":
                continue
            if _es_rotulo_con_secuencia(el):
                continue

            def _sustituir(m, mapas=mapas):
                etiqueta, numero = m.group(1), int(m.group(2))
                mapa = mapas.get(etiqueta, {})
                if numero in mapa and mapa[numero] != numero:
                    # Separador temporal (U+200B) para que la cascada de renumeración
                    # no vuelva a interpretar el número recién escrito.
                    return f"{etiqueta}​{mapa[numero]}"
                return m.group(0)

            aplicadas = _reemplazar_patron_parrafo(el, patron, _sustituir)
            if aplicadas:
                cambios_llamadas += aplicadas
                marcados.append(el)
        for el in marcados:
            _reemplazar_texto_parrafo(el, "​", " ", maximo=None)
    return {"tablas_numeradas": len(rotulos.get("Tabla", [])),
            "figuras_numeradas": len(rotulos.get("Figura", [])),
            "caches_reescritas": cambios_rotulo,
            "codigos_reescritos": cambios_codigo,
            "llamadas_reescritas": cambios_llamadas,
            "mapas": {k: {str(a): b for a, b in v.items()} for k, v in mapas.items()}}


def _parrafo_inicio_indice(documento, etiqueta: str):
    for el in _hijos_cuerpo(documento):
        if el.tag != _qn("w:p"):
            continue
        for instr in el.iter(_qn("w:instrText")):
            if "TOC" in (instr.text or "") and f'\\c "{etiqueta}"' in (instr.text or ""):
                return el
    return None


def _parrafo_fin_indice(documento, inicio):
    el = inicio.getnext()
    while el is not None:
        if el.tag == _qn("w:p"):
            tiene_instr = any(True for _ in el.iter(_qn("w:instrText")))
            texto = _texto_elemento(el).strip()
            if not tiene_instr and not texto and any(
                    (f.get(_qn("w:fldCharType")) == "end") for f in el.iter(_qn("w:fldChar"))):
                return el
        el = el.getnext()
    return None


def recomponer_indices_ilustraciones(documento) -> Dict[str, Any]:
    """Reconstruye los índices de figuras y tablas leyendo el título completo del rótulo."""
    resultado = {}
    for etiqueta in ("Figura", "Tabla"):
        inicio = _parrafo_inicio_indice(documento, etiqueta)
        if inicio is None:
            resultado[etiqueta] = {"estado": "sin_campo_toc"}
            continue
        fin = _parrafo_fin_indice(documento, inicio)
        if fin is None:
            resultado[etiqueta] = {"estado": "sin_cierre_de_campo"}
            continue
        if inicio.getnext() is None:
            resultado[etiqueta] = {"estado": "sin_plantilla"}
            continue
        # El primer párrafo del índice contiene el inicio del campo TOC y, además,
        # la primera entrada. Se clona como plantilla y se limpia su contenido de
        # entrada para que la reconstrucción no duplique el primer registro.
        import copy as _copy

        plantilla = _copy.deepcopy(inicio)
        _limpiar_entrada_de_inicio(inicio)
        # Retira las entradas actuales manteniendo el inicio y el cierre del campo.
        el = inicio.getnext()
        while el is not None and el is not fin:
            siguiente = el.getnext()
            documento.element.body.remove(el)
            el = siguiente
        rotulos = [x for x in _hijos_cuerpo(documento) if _es_rotulo_con_secuencia(x)]
        rotulos = [x for x in rotulos if _texto_elemento(x).strip().startswith(etiqueta + " ")]
        entradas = 0
        for el in rotulos:
            marcador, numero = _marcador_y_numero(el)
            if not marcador:
                continue
            titulo = _titulo_de_rotulo(el)
            nueva = _copiar_entrada_indice(plantilla, etiqueta, numero, titulo, marcador)
            fin.addprevious(nueva)
            entradas += 1
        resultado[etiqueta] = {"estado": "recompuesto", "entradas": entradas}
    return resultado


def _limpiar_entrada_de_inicio(inicio) -> None:
    """Deja en el párrafo inicial del índice solo el inicio y el separador del campo TOC."""
    conservar_hasta = -1
    hijos = list(inicio)
    for posicion, hijo in enumerate(hijos):
        if hijo.find(_qn("w:fldChar")) is not None and \
                hijo.find(_qn("w:fldChar")).get(_qn("w:fldCharType")) == "separate":
            conservar_hasta = posicion
            break
    for posicion, hijo in enumerate(hijos):
        if hijo.tag == _qn("w:pPr"):
            continue
        if posicion > conservar_hasta:
            inicio.remove(hijo)


def _copiar_entrada_indice(plantilla, etiqueta: str, numero: int, titulo: str, marcador: str):
    import copy as _copy

    nueva = _copy.deepcopy(plantilla)
    # La plantilla proviene del párrafo que abre el campo TOC y contiene, además, la
    # primera entrada. Se conserva solo el hipervínculo de la entrada (con su tabulador
    # y su PAGEREF interno) para no reabrir el índice en cada párrafo.
    for hijo in list(nueva):
        if hijo.tag not in (_qn("w:pPr"), _qn("w:hyperlink")):
            nueva.remove(hijo)
    if next(nueva.iter(_qn("w:hyperlink")), None) is None:
        return nueva
    for hiper in nueva.iter(_qn("w:hyperlink")):
        hiper.set(_qn("w:anchor"), marcador)
    runs = [r for r in nueva.iter(_qn("w:r"))]
    # Runs con texto escribible: se excluyen los que portan campos, tabuladores o dibujos.
    candidatos = []
    for run in runs:
        if (run.find(_qn("w:fldChar")) is not None
                or run.find(_qn("w:instrText")) is not None
                or run.find(_qn("w:tab")) is not None
                or run.find(_qn("w:drawing")) is not None):
            continue
        if run.find(_qn("w:t")) is None:
            continue
        candidatos.append(run)
    etiqueta_run = None
    for run in candidatos:
        rpr = run.find(_qn("w:rPr"))
        if rpr is not None and rpr.find(_qn("w:b")) is not None:
            etiqueta_run = run
            break
    if etiqueta_run is None and candidatos:
        etiqueta_run = candidatos[0]
    titulo_run = None
    for run in candidatos:
        if run is etiqueta_run:
            continue
        rpr = run.find(_qn("w:rPr"))
        if rpr is not None and rpr.find(_qn("w:i")) is not None:
            titulo_run = run
            break
    if titulo_run is None:
        for run in candidatos:
            if run is not etiqueta_run:
                titulo_run = run
                break
    espacio = "{http://www.w3.org/XML/1998/namespace}space"
    if etiqueta_run is not None:
        nodo = etiqueta_run.find(_qn("w:t"))
        nodo.text = f"{etiqueta} {numero}"
        nodo.set(espacio, "preserve")
    if titulo_run is not None:
        nodo = titulo_run.find(_qn("w:t"))
        nodo.text = f" {titulo}"
        nodo.set(espacio, "preserve")
    # Se vacían los runs restantes para no arrastrar fragmentos del título anterior
    # ni el número de página cacheado de la entrada que sirvió de plantilla.
    for run in candidatos:
        if run is etiqueta_run or run is titulo_run:
            continue
        for nodo in run.iter(_qn("w:t")):
            nodo.text = ""
    # Destino del PAGEREF y caché de página vacía hasta la actualización de campos.
    for instr in nueva.iter(_qn("w:instrText")):
        instr.text = f" PAGEREF {marcador} \\h "
    pila: List[Dict[str, Any]] = []
    for run in nueva.iter(_qn("w:r")):
        fld = run.find(_qn("w:fldChar"))
        if fld is not None:
            tipo = fld.get(_qn("w:fldCharType"))
            if tipo == "begin":
                pila.append({"instr": "", "resultado": False})
            elif tipo == "separate":
                if pila:
                    pila[-1]["resultado"] = True
            elif tipo == "end":
                if pila:
                    pila.pop()
            continue
        instr = run.find(_qn("w:instrText"))
        if instr is not None:
            if pila:
                pila[-1]["instr"] += instr.text or ""
            continue
        # Solo se vacía el número de página: la etiqueta y el título son texto visible.
        if pila and pila[-1]["resultado"] and "PAGEREF" in pila[-1]["instr"]:
            for nodo in run.iter(_qn("w:t")):
                nodo.text = ""
    return nueva


def unificar_marcadores(documento) -> Dict[str, Any]:
    """Garantiza identificadores y nombres de marcador únicos tras injertar contenido.

    Los rótulos creados por cirugía derivan el identificador del nombre del marcador; si
    coincide con uno preexistente, Word rechaza la actualización de campos. Se reasignan
    los identificadores duplicados conservando la pareja w:bookmarkStart / w:bookmarkEnd.
    """
    cuerpo = documento.element.body
    inicios = list(cuerpo.iter(_qn("w:bookmarkStart")))
    maximo = 0
    for nodo in inicios:
        try:
            maximo = max(maximo, int(nodo.get(_qn("w:id")) or 0))
        except (TypeError, ValueError):
            pass
    vistos_id = set()
    vistos_nombre = set()
    ids_reescritos = 0
    nombres_reescritos = 0
    for nodo in inicios:
        ident = nodo.get(_qn("w:id"))
        nombre = nodo.get(_qn("w:name")) or ""
        if ident in vistos_id:
            maximo += 1
            for fin in cuerpo.iter(_qn("w:bookmarkEnd")):
                if fin.get(_qn("w:id")) == ident:
                    fin.set(_qn("w:id"), str(maximo))
                    break
            nodo.set(_qn("w:id"), str(maximo))
            ident = str(maximo)
            ids_reescritos += 1
        vistos_id.add(ident)
        if nombre in vistos_nombre:
            maximo += 1
            nuevo = f"{nombre}_{maximo}"
            nodo.set(_qn("w:name"), nuevo)
            nombre = nuevo
            nombres_reescritos += 1
        vistos_nombre.add(nombre)
    return {"ids_reescritos": ids_reescritos, "nombres_reescritos": nombres_reescritos,
            "marcadores": len(inicios)}


def cirugia_estructural(ruta_origen: Union[str, Path], ruta_salida: Union[str, Path],
                        plan: Dict[str, Any]) -> Dict[str, Any]:
    """Aplica un plan de cirugía estructural sobre una copia versionada del documento."""
    import docx as _docx

    origen = Path(ruta_origen).resolve()
    salida = Path(ruta_salida).resolve()
    base_dir = Path(plan.get("_base_dir", origen.parent))
    plan = _resolver_referencias({k: v for k, v in plan.items() if not k.startswith("_")}, base_dir)
    documento = _docx.Document(str(origen))
    reporte: List[Dict[str, Any]] = []
    fallidas: List[Dict[str, Any]] = []
    for operacion in plan.get("operaciones", []):
        tipo = operacion.get("tipo")
        try:
            if tipo == "reemplazo_fragmento":
                detalle = _op_reemplazo_fragmento(documento, operacion)
            elif tipo == "reemplazo_parrafo":
                detalle = _op_reemplazo_parrafo(documento, operacion)
            elif tipo == "renombrar_parrafo":
                detalle = _op_renombrar_parrafo(documento, operacion)
            elif tipo == "eliminar_rango":
                detalle = _op_eliminar_rango(documento, operacion)
            elif tipo == "trasladar_rango":
                detalle = _op_trasladar_rango(documento, operacion)
            elif tipo == "trasladar_tabla":
                detalle = _op_trasladar_tabla(documento, operacion)
            elif tipo == "insertar_parrafos":
                detalle = _op_insertar_parrafos(documento, operacion)
            elif tipo == "injertar_tabla":
                detalle = _op_injertar_tabla(documento, operacion)
            elif tipo == "eliminar_tabla_con_rotulo":
                detalle = _op_eliminar_tabla_con_rotulo(documento, operacion)
            elif tipo == "normalizar_rotulos":
                detalle = normalizar_rotulos_dos_parrafos(documento)
                detalle["tipo"] = "normalizar_rotulos"
            elif tipo == "renumerar":
                detalle = renumerar_etiquetas(documento, bool(operacion.get("llamadas", True)),
                                              tuple(operacion.get("etiquetas", ("Tabla", "Figura"))))
                detalle["tipo"] = "renumerar"
            elif tipo == "recomponer_indices":
                detalle = recomponer_indices_ilustraciones(documento)
                detalle["tipo"] = "recomponer_indices"
            elif tipo == "verificar":
                detalle = _verificacion_estructural(documento)
                detalle["tipo"] = "verificar"
            else:
                raise ValueError(f"Operación desconocida: {tipo}")
            detalle["id"] = operacion.get("id")
            reporte.append(detalle)
        except Exception as exc:  # noqa: BLE001
            fallidas.append({"id": operacion.get("id"), "tipo": tipo, "error": str(exc)})
            if plan.get("detener_en_error", True):
                raise
    seguridad.asegurar_no_sobrescribe(origen, salida)
    seguridad.asegurar_escritura_permitida(salida)
    marcadores = unificar_marcadores(documento)
    documento.save(str(salida))
    return {
        "origen": str(origen),
        "salida": str(salida),
        "sha256_origen": seguridad.sha256_archivo(origen),
        "sha256_salida": seguridad.sha256_archivo(salida),
        "operaciones": len(plan.get("operaciones", [])),
        "aplicadas": len(reporte),
        "fallidas": fallidas,
        "marcadores_unificados": marcadores,
        "detalle": reporte,
        "estructura_final": _verificacion_estructural(documento),
    }


def _verificacion_estructural(documento) -> Dict[str, Any]:
    hijos = _hijos_cuerpo(documento)
    tablas = sum(1 for el in hijos if el.tag == _qn("w:tbl"))
    rotulos_tabla = rotulos_figura = 0
    for el in hijos:
        if _es_rotulo_con_secuencia(el):
            texto = _texto_elemento(el).strip()
            if texto.startswith("Tabla "):
                rotulos_tabla += 1
            elif texto.startswith("Figura "):
                rotulos_figura += 1
    secciones = sum(1 for el in hijos if el.tag == _qn("w:sectPr"))
    secciones += sum(1 for el in hijos if el.tag == _qn("w:p")
                     and el.find(_qn("w:pPr") + "/" + _qn("w:sectPr")) is not None)
    return {
        "parrafos": sum(1 for el in hijos if el.tag == _qn("w:p")),
        "tablas": tablas,
        "rotulos_tabla": rotulos_tabla,
        "rotulos_figura": rotulos_figura,
        "omml": sum(1 for _ in documento.element.body.iter(_qn("m:oMath"))),
        "secciones": secciones,
        "hipervinculos": sum(1 for _ in documento.element.body.iter(_qn("w:hyperlink"))),
        "marcadores": sum(1 for _ in documento.element.body.iter(_qn("w:bookmarkStart"))),
        "campos": sum(1 for _ in documento.element.body.iter(_qn("w:instrText"))),
    }


def main() -> int:
    seguridad.configurar_utf8()
    parser = argparse.ArgumentParser(description="Motor quirúrgico OpenXML para tablas y documentos APA 7 (UNAJMA)")
    parser.add_argument(
        "comando",
        choices=[
            "auditar",
            "blindar-todas",
            "exportar-pdf",
            "renderizar-paginas",
            "reconstruir-tabla",
            "corregir-estructura",
            "aplicar-ordenes",
            "aplicar-cursiva",
            "cirugia-extension",
            "cirugia-estructural",
            "actualizar-campos",
            "reparar-imagenes-pdf",
            "tablas.geometria_proporcional",
            "tablas.valign",
            "tablas.alineacion_decimal",
            "runs.subindices",
            "tablas.keep_junta",
            "tablas.keep_cabecera",
            "parrafos.normalizar_listas",
        ],
        nargs="?",
        default="auditar",
    )
    parser.add_argument("ruta_docx", nargs="?", help="Ruta al archivo .docx o .pdf a inspeccionar")
    parser.add_argument("--paginas", default="1", help="Páginas a renderizar")
    parser.add_argument("--todas", action="store_true", help="Renderiza todas las páginas del PDF")
    parser.add_argument("--pdf", help="PDF de origen para reparar imágenes")
    parser.add_argument("--dpi", type=int, default=300, help="Resolución DPI")
    parser.add_argument("--json", action="store_true", help="Salida en formato JSON")
    parser.add_argument("--salida", help="DOCX de destino (comando reconstruir-tabla)")
    parser.add_argument("--tabla", type=int, default=None, help="Índice base 0 de la tabla a reconstruir")
    parser.add_argument("--filas", help="Archivo JSON con las filas de datos")
    parser.add_argument("--clave", help="Clave del objeto JSON que contiene la lista de filas")
    parser.add_argument("--ultima-fila-es-total", action="store_true", help="El último elemento de la lista es la fila Total")
    parser.add_argument("--columnas", help="Claves de columna separadas por coma")
    parser.add_argument("--alineaciones", default="left,left,center,center", help="Alineación por columna")
    parser.add_argument("--nota", help="Texto de la nota posterior a la tabla")
    parser.add_argument("--porcentaje-compacto", action="store_true", help="Elimina el espacio antes del signo %% (estilo 14.29%%)")
    parser.add_argument("--reporte", help="Archivo JSON donde escribir el detalle de la reconstrucción")
    parser.add_argument("--figuras-desde", type=int, default=11, help="Primera figura a reordenar")
    parser.add_argument("--figuras-hasta", type=int, default=48, help="Última figura a reordenar")
    parser.add_argument("--figuras-excluidas", default="49,50,51,52", help="Figuras que se dejan intactas")
    parser.add_argument("--tablas-matriz", default="", help="Índices base 0 de las matrices de anexo a ajustar (ej. 52,53)")
    parser.add_argument("--margenes-matriz", type=int, default=57, help="Márgenes laterales de celda en dxa para las matrices")
    parser.add_argument("--tamano-matriz", type=float, default=8.0, help="Tamaño en pt para cabecera y celdas numéricas de las matrices")
    parser.add_argument("--via-matriz", choices=["margenes", "rebalanceo", "ambas"], default="rebalanceo", help="Única vía geométrica para las matrices de anexo")
    parser.add_argument("--tablas-rebalanceo", default="", help="Índices base 0 de tablas adicionales a rebalancear conservando su ancho total")
    parser.add_argument("--referencias", help="Archivo JSON con las referencias a insertar (se aplican al final)")
    parser.add_argument("--lotes", help="Rutas de los JSON de órdenes separadas por coma, en el orden de aplicación")
    parser.add_argument("--solo-verificar", action="store_true", help="No escribe archivo: solo comprueba qué órdenes se aplicarían")
    parser.add_argument("--sanear-espacios", action="store_true", help="Recorta espacios y tabuladores residuales al final de cada párrafo antes de guardar")
    parser.add_argument("--solo-campos", help="Tipos de campo a actualizar con actualizar-campos (ej. PAGEREF,SEQ)")
    parser.add_argument("--excepto-campos", help="Campos a excluir al actualizar: 'ilustraciones' excluye los TOC \\c de figuras y tablas")
    parser.add_argument("--plan", help="Archivo JSON con el plan de la extensión quirúrgica")
    parser.add_argument("--salida-dir", help="Directorio de destino de las páginas PNG renderizadas")
    parser.add_argument("--anchos", help="Anchos de columna en dxa separados por coma (tablas.geometria_proporcional)")
    parser.add_argument("--margen-dxa", type=int, default=60, help="Margen de celda en dxa para el reparto proporcional")
    parser.add_argument("--valor", default="top", choices=["top", "center", "bottom"], help="Valor de w:vAlign (tablas.valign)")
    parser.add_argument("--modo", default="tab_decimal", choices=["tab_decimal", "derecha"], help="Modo de alineación decimal")
    parser.add_argument("--terminos", help="JSON con el inventario de notación (runs.subindices)")
    parser.add_argument("--ambito", default="ambos", choices=["cuerpo", "celdas", "ambos"], help="Ámbito de runs.subindices")
    parser.add_argument("--indices", help="Índices de tabla separados por coma (tablas.keep_junta)")
    parser.add_argument("--sangria-dxa", type=int, default=720, help="Sangría izquierda de ítems de lista en dxa (parrafos.normalizar_listas)")
    parser.add_argument("--colgante-dxa", type=int, default=360, help="Sangría francesa de ítems de lista en dxa (parrafos.normalizar_listas)")
    args = parser.parse_args()

    if args.comando == "aplicar-cursiva":
        if not (args.ruta_docx and args.lotes):
            parser.error("aplicar-cursiva requiere <docx> y --lotes")
        if not args.solo_verificar and not args.salida:
            parser.error("aplicar-cursiva requiere --salida cuando no se usa --solo-verificar")
        import docx as _docx

        documento = _docx.Document(str(Path(args.ruta_docx)))
        lotes_cursiva = []
        for ruta_lote in [r.strip() for r in args.lotes.split(",") if r.strip()]:
            datos = json.loads(Path(ruta_lote).read_text(encoding="utf-8"))
            lotes_cursiva.append((Path(ruta_lote).stem, datos))
        reporte = aplicar_cursivas(documento, lotes_cursiva)
        reporte.update(aplicar_alineaciones(documento, lotes_cursiva))
        reporte["sha256_origen"] = seguridad.sha256_archivo(Path(args.ruta_docx))
        reporte["solo_verificar"] = bool(args.solo_verificar)
        if not args.solo_verificar:
            seguridad.asegurar_no_sobrescribe(Path(args.ruta_docx), Path(args.salida))
            seguridad.asegurar_escritura_permitida(Path(args.salida))
            documento.save(str(Path(args.salida)))
            reporte["sha256_destino"] = seguridad.sha256_archivo(Path(args.salida))
            reporte["salida"] = str(Path(args.salida))
        if args.reporte:
            Path(args.reporte).parent.mkdir(parents=True, exist_ok=True)
            Path(args.reporte).write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(reporte, indent=2, ensure_ascii=False))
        return 0

    if args.comando == "cirugia-extension":
        if not (args.ruta_docx and args.salida and args.plan):
            parser.error("cirugia-extension requiere <docx>, --plan y --salida")
        plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
        reporte = cirugia_extension(Path(args.ruta_docx), Path(args.salida), plan)
        if args.reporte:
            Path(args.reporte).parent.mkdir(parents=True, exist_ok=True)
            Path(args.reporte).write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
        resumen = {k: v for k, v in reporte.items() if k != "operaciones"}
        resumen["operaciones"] = len(reporte["operaciones"])
        print(json.dumps(resumen, indent=2, ensure_ascii=False))
        return 0

    if args.comando == "cirugia-estructural":
        if not (args.ruta_docx and args.salida and args.plan):
            parser.error("cirugia-estructural requiere <docx>, --plan y --salida")
        plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
        plan["_base_dir"] = str(Path(args.plan).resolve().parent)
        reporte = cirugia_estructural(Path(args.ruta_docx), Path(args.salida), plan)
        if args.reporte:
            Path(args.reporte).parent.mkdir(parents=True, exist_ok=True)
            Path(args.reporte).write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
        resumen = {k: v for k, v in reporte.items() if k != "detalle"}
        resumen["detalle"] = [
            {k: v for k, v in d.items() if k in ("id", "tipo", "elementos", "parrafos", "entradas",
                                                "tablas_numeradas", "figuras_numeradas",
                                                "caches_reescritas", "llamadas_reescritas",
                                                "rotulos_divididos", "filas", "titulo", "cambios")}
            for d in reporte["detalle"]
        ]
        print(json.dumps(resumen, indent=2, ensure_ascii=False))
        return 0

    if args.comando == "actualizar-campos":
        if not (args.ruta_docx and args.salida):
            parser.error("actualizar-campos requiere <docx> y --salida")
        fragmentos = None
        if args.excepto_campos:
            fragmentos = []
            for token in args.excepto_campos.split(","):
                token = token.strip()
                if token.lower() == "ilustraciones":
                    fragmentos += ['\\c "Tabla"', '\\c "Figura"']
                elif token:
                    fragmentos.append(token)
        reporte = actualizar_campos_docx(Path(args.ruta_docx), Path(args.salida),
                                         solo=(args.solo_campos.split(",") if args.solo_campos else None),
                                         excepto_instr=fragmentos)
        if args.reporte:
            Path(args.reporte).parent.mkdir(parents=True, exist_ok=True)
            Path(args.reporte).write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(reporte, indent=2, ensure_ascii=False))
        return 0

    if args.comando == "blindar-todas":
        if not (args.ruta_docx and args.salida):
            parser.error("blindar-todas requiere <docx> y --salida")
        import docx as _docx

        documento = _docx.Document(str(Path(args.ruta_docx)))
        reporte = blindar_todas_las_tablas(documento)
        seguridad.asegurar_no_sobrescribe(Path(args.ruta_docx), Path(args.salida))
        seguridad.asegurar_escritura_permitida(Path(args.salida))
        documento.save(str(Path(args.salida)))
        reporte["destino"] = str(Path(args.salida))
        reporte["sha256_destino"] = seguridad.sha256_archivo(Path(args.salida))
        if args.reporte:
            Path(args.reporte).parent.mkdir(parents=True, exist_ok=True)
            Path(args.reporte).write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps({"tablas": reporte["tablas"], "destino": reporte["destino"]}, indent=2, ensure_ascii=False))
        return 0

    if args.comando == "exportar-pdf":
        if not args.ruta_docx:
            parser.error("exportar-pdf requiere <docx>")
        reporte = exportar_docx_a_pdf(Path(args.ruta_docx), args.salida)
        if args.reporte:
            Path(args.reporte).parent.mkdir(parents=True, exist_ok=True)
            Path(args.reporte).write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(reporte, indent=2, ensure_ascii=False))
        return 0

    if args.comando == "renderizar-paginas":
        if not args.ruta_docx:
            parser.error("renderizar-paginas requiere <pdf>")
        if args.todas:
            import pymupdf

            with pymupdf.open(args.ruta_docx) as _pdf:
                paginas = list(range(1, _pdf.page_count + 1))
        else:
            paginas = [int(p) for p in args.paginas.split(",") if p.strip()]
        reporte = renderizar_paginas_pdf(Path(args.ruta_docx), paginas, args.dpi, args.salida_dir)
        if args.reporte:
            Path(args.reporte).parent.mkdir(parents=True, exist_ok=True)
            Path(args.reporte).write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(reporte, indent=2, ensure_ascii=False))
        return 0

    if args.comando == "reparar-imagenes-pdf":
        if not (args.ruta_docx and args.pdf and args.salida):
            parser.error("reparar-imagenes-pdf requiere <docx>, --pdf y --salida")
        reporte = reparar_imagenes_pdf(Path(args.ruta_docx), Path(args.pdf), Path(args.salida))
        if args.reporte:
            Path(args.reporte).parent.mkdir(parents=True, exist_ok=True)
            Path(args.reporte).write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps({k: v for k, v in reporte.items() if k not in ("asignaciones", "resoluciones")}, indent=2, ensure_ascii=False))
        return 0

    if args.comando in (
        "tablas.geometria_proporcional",
        "tablas.valign",
        "tablas.alineacion_decimal",
        "runs.subindices",
        "tablas.keep_junta",
        "tablas.keep_cabecera",
        "parrafos.normalizar_listas",
    ):
        if not args.ruta_docx:
            parser.error(f"{args.comando} requiere <docx>")
        if not args.solo_verificar and not args.salida:
            parser.error(f"{args.comando} requiere --salida cuando no se usa --solo-verificar")
        import docx as _docx

        origen = Path(args.ruta_docx)
        documento = _docx.Document(str(origen))
        aplicadas: List[Dict[str, Any]] = []
        fallidas: List[Dict[str, Any]] = []

        if args.comando == "tablas.geometria_proporcional":
            if args.tabla is None or not args.anchos:
                parser.error("tablas.geometria_proporcional requiere --tabla y --anchos")
            resultado = aplicar_geometria_proporcional(
                documento,
                args.tabla,
                [int(a) for a in args.anchos.split(",") if a.strip()],
                args.margen_dxa,
                solo_verificar=args.solo_verificar,
            )
            (fallidas if resultado.get("estado") == "fallida" else aplicadas).append(resultado)
        elif args.comando == "tablas.valign":
            if args.tabla is None:
                parser.error("tablas.valign requiere --tabla")
            resultado = aplicar_valign(
                documento,
                args.tabla,
                args.valor,
                solo_verificar=args.solo_verificar,
            )
            (fallidas if resultado.get("estado") == "fallida" else aplicadas).append(resultado)
        elif args.comando == "tablas.alineacion_decimal":
            if args.tabla is None or not args.columnas:
                parser.error("tablas.alineacion_decimal requiere --tabla y --columnas")
            resultado = aplicar_alineacion_decimal(
                documento,
                args.tabla,
                [int(c) for c in args.columnas.split(",") if c.strip()],
                args.modo,
                solo_verificar=args.solo_verificar,
            )
            (fallidas if resultado.get("estado") == "fallida" else aplicadas).append(resultado)
        elif args.comando == "runs.subindices":
            if not args.terminos:
                parser.error("runs.subindices requiere --terminos")
            inventario = json.loads(Path(args.terminos).read_text(encoding="utf-8"))
            resultado = convertir_notacion_subindices(
                documento,
                inventario,
                ambito=args.ambito,
                solo_verificar=args.solo_verificar,
            )
            aplicadas.extend(resultado.get("aplicadas", []))
            fallidas.extend(resultado.get("fallidas", []))
        elif args.comando == "parrafos.normalizar_listas":
            resultado = normalizar_listas_rotulos(
                documento,
                solo_verificar=args.solo_verificar,
                sangria_dxa=args.sangria_dxa,
                colgante_dxa=args.colgante_dxa,
            )
            (fallidas if resultado.get("estado") == "fallida" else aplicadas).append(resultado)
        elif args.comando == "tablas.keep_cabecera":
            resultado = aplicar_keep_cabecera(documento, solo_verificar=args.solo_verificar)
            (fallidas if resultado.get("estado") == "fallida" else aplicadas).append(resultado)
        else:
            if not args.indices:
                parser.error("tablas.keep_junta requiere --indices")
            resultado = aplicar_keep_junta(
                documento,
                [int(i) for i in args.indices.split(",") if i.strip()],
                solo_verificar=args.solo_verificar,
            )
            aplicadas.extend(resultado.get("aplicadas", []))
            fallidas.extend(resultado.get("fallidas", []))

        reporte = {
            "comando": args.comando,
            "solo_verificar": bool(args.solo_verificar),
            "sha256_origen": seguridad.sha256_archivo(origen),
            "aplicadas": aplicadas,
            "fallidas": fallidas,
        }
        if args.comando == "runs.subindices":
            reporte["ocurrencias"] = resultado.get("ocurrencias", 0)
            reporte["guiones_bajos_retirados"] = resultado.get("guiones_bajos_retirados", 0)
            reporte["parrafos_con_subindices"] = resultado.get("parrafos_con_subindices", 0)
            reporte["celdas_con_subindices"] = resultado.get("celdas_con_subindices", 0)
        if not args.solo_verificar:
            destino = Path(args.salida)
            seguridad.asegurar_no_sobrescribe(origen, destino)
            seguridad.asegurar_escritura_permitida(destino)
            documento.save(str(destino))
            reporte["sha256_destino"] = seguridad.sha256_archivo(destino)
            reporte["salida"] = str(destino)
        if args.reporte:
            Path(args.reporte).parent.mkdir(parents=True, exist_ok=True)
            Path(args.reporte).write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(reporte, indent=2, ensure_ascii=False))
        return 0 if not fallidas else 1

    if args.comando == "aplicar-ordenes":
        if not (args.ruta_docx and args.lotes):
            parser.error("aplicar-ordenes requiere <docx> y --lotes")
        if not args.solo_verificar and not args.salida:
            parser.error("aplicar-ordenes requiere --salida cuando no se usa --solo-verificar")
        lotes = []
        for ruta_lote in [r.strip() for r in args.lotes.split(",") if r.strip()]:
            datos = json.loads(Path(ruta_lote).read_text(encoding="utf-8"))
            lotes.append((Path(ruta_lote).stem, datos))
        reporte = aplicar_ordenes_edicion(
            Path(args.ruta_docx),
            lotes,
            Path(args.salida) if args.salida else None,
            solo_verificar=args.solo_verificar,
            tablas_matriz=[int(x) for x in args.tablas_matriz.split(",") if x.strip()],
            margenes_matriz_dxa=args.margenes_matriz,
            tamano_matriz_pt=args.tamano_matriz,
            via_matriz=args.via_matriz,
            tablas_rebalanceo=[int(x) for x in args.tablas_rebalanceo.split(",") if x.strip()],
            sanear_espacios=args.sanear_espacios,
        )
        if args.reporte:
            Path(args.reporte).parent.mkdir(parents=True, exist_ok=True)
            Path(args.reporte).write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
        resumen = {
            "solo_verificar": reporte["solo_verificar"],
            "sha256_origen": reporte["sha256_origen"],
            "sha256_destino": reporte["sha256_destino"],
            "parrafos": reporte["parrafos"],
            "tablas": reporte["tablas"],
            "total_ordenes": reporte["total_ordenes"],
            "total_aplicadas": reporte["total_aplicadas"],
            "total_fallidas": reporte["total_fallidas"],
            "saneamiento_espacios": {
                "parrafos_saneados": reporte["saneamiento_espacios"]["parrafos_saneados"],
                "caracteres_recortados": reporte["saneamiento_espacios"]["caracteres_recortados"],
            },
            "lotes": [
                {k: v for k, v in lote.items() if k != "detalles"} for lote in reporte["lotes"]
            ],
        }
        print(json.dumps(resumen, indent=2, ensure_ascii=False))
        return 0

    if args.comando == "corregir-estructura":
        if not (args.ruta_docx and args.salida):
            parser.error("corregir-estructura requiere <docx> y --salida")
        reporte = corregir_estructura_editorial(
            Path(args.ruta_docx),
            Path(args.salida),
            figuras_desde=args.figuras_desde,
            figuras_hasta=args.figuras_hasta,
            figuras_excluidas=[int(x) for x in args.figuras_excluidas.split(",") if x.strip()],
            tablas_matriz=[int(x) for x in args.tablas_matriz.split(",") if x.strip()],
            margenes_matriz_dxa=args.margenes_matriz,
            tamano_matriz_pt=args.tamano_matriz,
            referencias=(
                json.loads(Path(args.referencias).read_text(encoding="utf-8"))
                if args.referencias
                else ()
            ),
            sanear_espacios=args.sanear_espacios,
        )
        if args.reporte:
            Path(args.reporte).parent.mkdir(parents=True, exist_ok=True)
            Path(args.reporte).write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps({k: v for k, v in reporte.items() if k != "acciones"}, indent=2, ensure_ascii=False))
        print(json.dumps({"acciones": len(reporte["acciones"])}, ensure_ascii=False))
        return 0

    if args.comando == "reconstruir-tabla":
        if not (args.ruta_docx and args.salida and args.tabla is not None and args.filas):
            parser.error("reconstruir-tabla requiere <docx>, --salida, --tabla y --filas")
        datos = json.loads(Path(args.filas).read_text(encoding="utf-8"))
        if args.clave:
            datos = datos[args.clave]
        filas = list(datos)
        fila_total = None
        if args.ultima_fila_es_total:
            fila_total = filas.pop()
        reporte = reconstruir_tabla_filas(
            Path(args.ruta_docx),
            Path(args.salida),
            args.tabla,
            filas,
            alineaciones=[a.strip() for a in args.alineaciones.split(",") if a.strip()],
            fila_total=fila_total,
            columnas=[c.strip() for c in args.columnas.split(",")] if args.columnas else None,
            nota=args.nota,
            porcentaje_compacto=args.porcentaje_compacto,
        )
        if args.reporte:
            Path(args.reporte).parent.mkdir(parents=True, exist_ok=True)
            Path(args.reporte).write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(reporte, indent=2, ensure_ascii=False))
        return 0

    if not args.ruta_docx:
        print(json.dumps({"estado": "listo", "motor": "docx_quirurgico.py", "regla": "APA 7 / UNAJMA"}, ensure_ascii=False))
        return 0

    reporte = auditar_docx_openxml(args.ruta_docx)
    print(json.dumps(reporte, indent=2, ensure_ascii=False))
    return 0 if reporte.get("cumple_apa7", False) else 1


if __name__ == "__main__":
    sys.exit(main())
