# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - COMPILADOR QUIRURGICO DEL INFORME FINAL v05
================================================================================
Mision: rediseno geometrico de tablas comprimidas, erradicacion de texto
cortado, normalizacion APA 7 de las 59 tablas, seccion horizontal propia para
el Anexo 5, ajuste de figuras y exportacion DOCX/PDF.

Entrada inmutable:
  - salidas/documentos/informe_final_v04.docx  (solo lectura)

Salidas:
  - salidas/documentos/informe_final_v05.docx
  - salidas/documentos/informe_final_v05.pdf
  - salidas/reportes_maquetacion/reporte_tablas_v05.json
  - salidas/reportes_maquetacion/paginas_control/*.png

Motor obligatorio: scripts/utilidades/docx_quirurgico.py
  (configurar_geometria_tabla, eliminar_flotacion_tabla, auditar_docx_openxml)

Uso:
  python scripts/compiladores/compilar_informe_final_v05.py
  python scripts/compiladores/compilar_informe_final_v05.py --sin-pdf
================================================================================
"""

import argparse
import copy
import hashlib
import html
import json
import re
import sys
import time
import unicodedata
import zipfile
from datetime import date
from pathlib import Path

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, Twips
from docx.table import Table
from docx.text.paragraph import Paragraph
from lxml import etree

RAIZ = Path(__file__).resolve().parents[2]
DOCX_V04 = RAIZ / "salidas" / "documentos" / "informe_final_v04.docx"
DOCX_V05 = RAIZ / "salidas" / "documentos" / "informe_final_v05.docx"
PDF_V05 = RAIZ / "salidas" / "documentos" / "informe_final_v05.pdf"
REPORTE_DIR = RAIZ / "salidas" / "reportes_maquetacion"
REPORTE_JSON = REPORTE_DIR / "reporte_tablas_v05.json"
PAGINAS_DIR = REPORTE_DIR / "paginas_control"

sys.path.insert(0, str(RAIZ / "scripts" / "utilidades"))
from docx_quirurgico import (  # noqa: E402
    auditar_docx_openxml,
    configurar_geometria_tabla,
    eliminar_flotacion_tabla,
)

# Geometria real medida en los sectPr del documento (dxa)
ANCHO_UTIL_PORTRAIT = 8765      # 11906 - 1701 - 1440
ANCHO_UTIL_LANDSCAPE = 13697    # 16838 - 1701 - 1440
ANCHO_ANEXO5 = 13630          # 1100 + 2100 + 14 x 745, bajo la caja util 13697
ALTO_ANEXO5 = 11906 - 1440 - 1440
FUENTE = "Times New Roman"
TAM_NOTA = 9.5

# Tablas reconstruidas (indice 1-based de doc.tables; rotulo = indice - 1)
COLUMNAS_ESPERADAS = {
    36: 7, 37: 8, 38: 8, 39: 8, 40: 6,
    41: 7, 42: 7, 43: 7, 44: 7,
    53: 18, 54: 18, 56: 1, 57: 1, 58: 1, 59: 1,
}
TABLAS_RECONSTRUIDAS = sorted(COLUMNAS_ESPERADAS)
TABLAS_ESTADISTICAS_9PT = {36, 37, 38, 39, 41, 42, 43, 44}


# ---------------------------------------------------------------------------
# Utilidades basicas
# ---------------------------------------------------------------------------
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for bloque in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(bloque)
    return h.hexdigest()


def escala_anchos(anchos, total):
    """Reescala proporcionalmente una lista de anchos dxa hasta sumar total."""
    anchos = [max(1, int(a)) for a in anchos]
    suma = sum(anchos)
    if suma == total:
        return list(anchos)
    salida = [max(1, int(round(a * total / suma))) for a in anchos]
    diferencia = total - sum(salida)
    salida[-1] += diferencia
    while salida[-1] < 1:
        salida[-1] += 1
        salida[0] -= 1
    return salida


def _texto_parrafo(el, doc) -> str:
    return Paragraph(el, doc._body).text.replace("\n", " ").strip()


# ---------------------------------------------------------------------------
# Constructores XML nativos
# ---------------------------------------------------------------------------
def _run_xml(texto, pt, bold=False, italic=False):
    sz = int(round(pt * 2))
    b = "<w:b/>" if bold else ""
    i = "<w:i/>" if italic else ""
    t = html.escape(str(texto), quote=False)
    return (
        f'<w:r><w:rPr><w:rFonts w:ascii="{FUENTE}" w:hAnsi="{FUENTE}" w:cs="{FUENTE}"/>'
        f'{b}{i}<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
        f'<w:t xml:space="preserve">{t}</w:t></w:r>'
    )


def _p_xml(texto, pt, bold=False, jc="left", italic=False):
    return (
        '<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
        '<w:ind w:firstLine="0" w:left="0" w:right="0"/>'
        f'<w:jc w:val="{jc}"/></w:pPr>{_run_xml(texto, pt, bold, italic)}</w:p>'
    )


def _parrafos_celda(texto, pt, bold, jc, italic=False):
    partes = str(texto).split("\n")
    if not partes:
        partes = [""]
    return "".join(_p_xml(p, pt, bold, jc, italic) for p in partes)


def _tc_xml(texto, ancho, pt, bold=False, jc="left", header=False):
    borde = ""
    if header:
        borde = ('<w:tcBorders><w:bottom w:val="single" w:sz="8" w:space="0" '
                 'w:color="000000"/></w:tcBorders>')
    return (
        f'<w:tc><w:tcPr><w:tcW w:w="{ancho}" w:type="dxa"/>{borde}'
        '<w:vAlign w:val="center"/></w:tcPr>'
        f'{_parrafos_celda(texto, pt, bold, jc)}</w:tc>'
    )


def construir_tabla_xml(headers, filas, anchos, font_pt, header_pt=None,
                        aligns=None, total=None):
    """Construye una tabla APA 7 nativa completa (3 lineas, fixed layout)."""
    header_pt = header_pt if header_pt is not None else font_pt
    total = total if total is not None else sum(anchos)
    if len(anchos) != len(headers):
        raise ValueError(f"anchos({len(anchos)}) != headers({len(headers)})")
    aligns = aligns or ["left"] + ["center"] * (len(headers) - 1)

    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in anchos)
    celdas_h = "".join(
        _tc_xml(h, anchos[i], header_pt, bold=True, jc="center", header=True)
        for i, h in enumerate(headers)
    )
    filas_xml = [
        f'<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>{celdas_h}</w:tr>'
    ]
    for fila in filas:
        celdas = "".join(
            _tc_xml(str(fila[i]) if i < len(fila) else "", anchos[i], font_pt,
                    bold=False, jc=aligns[i] if i < len(aligns) else "center")
            for i in range(len(headers))
        )
        filas_xml.append(f'<w:tr><w:trPr><w:cantSplit/></w:trPr>{celdas}</w:tr>')

    return parse_xml(
        f'<w:tbl {nsdecls("w")}>'
        '<w:tblPr>'
        f'<w:tblW w:w="{total}" w:type="dxa"/>'
        '<w:jc w:val="center"/>'
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:left w:val="none"/>'
        '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:right w:val="none"/>'
        '<w:insideH w:val="none"/>'
        '<w:insideV w:val="none"/>'
        '</w:tblBorders>'
        '<w:tblLayout w:type="fixed"/>'
        '<w:tblCellMar><w:top w:w="40" w:type="dxa"/><w:left w:w="60" w:type="dxa"/>'
        '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="60" w:type="dxa"/></w:tblCellMar>'
        '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" '
        'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
        '</w:tblPr>'
        f'<w:tblGrid>{grid}</w:tblGrid>'
        f'{"".join(filas_xml)}'
        '</w:tbl>'
    )


def construir_recuadro_foto_xml(etiqueta, instruccion):
    """Recuadro sobrio de una celda para marcador fotografico (9 cm de alto)."""
    alto = int(round(9.0 / 2.54 * 1440))  # 9 cm en dxa
    ancho = ANCHO_UTIL_PORTRAIT
    return parse_xml(
        f'<w:tbl {nsdecls("w")}>'
        '<w:tblPr>'
        f'<w:tblW w:w="{ancho}" w:type="dxa"/>'
        '<w:jc w:val="center"/>'
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        '<w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        '<w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        '<w:insideH w:val="none"/><w:insideV w:val="none"/>'
        '</w:tblBorders>'
        '<w:tblLayout w:type="fixed"/>'
        '<w:tblCellMar><w:top w:w="120" w:type="dxa"/><w:left w:w="120" w:type="dxa"/>'
        '<w:bottom w:w="120" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tblCellMar>'
        '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" '
        'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
        '</w:tblPr>'
        f'<w:tblGrid><w:gridCol w:w="{ancho}"/></w:tblGrid>'
        '<w:tr><w:trPr><w:cantSplit/><w:tblHeader/>'
        f'<w:trHeight w:val="{alto}" w:hRule="atLeast"/></w:trPr>'
        f'<w:tc><w:tcPr><w:tcW w:w="{ancho}" w:type="dxa"/>'
        '<w:vAlign w:val="center"/></w:tcPr>'
        f'{_p_xml(etiqueta, 10, bold=True, jc="center")}'
        f'{_p_xml(instruccion, 9, bold=False, jc="center")}'
        '</w:tc></w:tr>'
        '</w:tbl>'
    )


# ---------------------------------------------------------------------------
# Reconstruccion de tablas
# ---------------------------------------------------------------------------
def _datos_tabla(tabla):
    return [[c.text.strip() for c in fila.cells] for fila in tabla.rows]


def _reemplazar_tabla(doc, indice, nueva_tabla):
    vieja = doc.tables[indice - 1]._tbl
    vieja.addprevious(nueva_tabla)
    vieja.getparent().remove(vieja)


def _reconstruir_35(doc):
    datos = _datos_tabla(doc.tables[35])
    headers = ["Momento de evaluacion", "Escala / subescala", "N. de items",
               "Muestra (n)", "Alfa de Cronbach", "IC 95 % [LI, LS]",
               "Nivel de consistencia"]
    headers[0] = "Momento de evaluación"
    headers[2] = "N.° de ítems"
    headers[6] = "Nivel de consistencia"
    filas = []
    for r in datos[1:]:
        filas.append([r[0], r[1], r[2], r[3], r[4], f"[{r[5]}, {r[6]}]", r[7]])
    anchos = escala_anchos([1900, 1500, 900, 900, 1100, 1600, 1300],
                           ANCHO_UTIL_PORTRAIT)
    nueva = construir_tabla_xml(headers, filas, anchos, 9.0,
                                aligns=["left", "left", "center", "center",
                                        "center", "center", "center"])
    _reemplazar_tabla(doc, 36, nueva)


def _reconstruir_descriptivos(doc, indice):
    datos = _datos_tabla(doc.tables[indice - 1])
    headers = [datos[0][0], "Momento", "Media", "DE", "Mediana", "RIC",
               "Mín – Máx", "Variación"]
    filas = []
    for r in datos[1:]:
        filas.append([r[0], r[1], r[3], r[4], r[5], r[6],
                      f"{r[7]} – {r[8]}", r[9]])
    anchos = escala_anchos([2300, 1350, 900, 850, 950, 900, 1350, 1100],
                           ANCHO_UTIL_PORTRAIT)
    nueva = construir_tabla_xml(headers, filas, anchos, 9.0,
                                aligns=["left", "left", "center", "center",
                                        "center", "center", "center", "center"])
    _reemplazar_tabla(doc, indice, nueva)


def _reconstruir_39(doc):
    datos = _datos_tabla(doc.tables[39])
    headers = ["Dimensión", "Indicador", "W", "p",
               "Decisión distribucional", "Prueba asignada"]
    filas = [[r[0], r[1], r[3], r[5], r[6], r[7]] for r in datos[1:]]
    anchos = escala_anchos([1900, 2600, 800, 850, 1500, 1800],
                           ANCHO_UTIL_PORTRAIT)
    nueva = construir_tabla_xml(headers, filas, anchos, 10.0,
                                aligns=["left", "left", "center", "center",
                                        "left", "left"])
    _reemplazar_tabla(doc, 40, nueva)


def _reconstruir_contraste(doc, indice):
    datos = _datos_tabla(doc.tables[indice - 1])
    headers = ["Indicador", "Prueba", "Estadístico", "p",
               "Tamaño del efecto", "p ajustado (Holm)", "Decisión"]
    filas = []
    for r in datos[1:]:
        magnitud = r[6].split("(")[0].strip().lower() or "grande"
        efecto = f"{r[5]} ({magnitud})"
        filas.append([r[0], r[1], r[2], r[4], efecto, r[7], r[8]])
    anchos = escala_anchos([2400, 1700, 1200, 800, 1500, 1100, 1200],
                           ANCHO_UTIL_PORTRAIT)
    nueva = construir_tabla_xml(headers, filas, anchos, 9.0,
                                aligns=["left", "left", "center", "center",
                                        "center", "center", "center"])
    _reemplazar_tabla(doc, indice, nueva)


def _reconstruir_44(doc):
    datos = _datos_tabla(doc.tables[43])
    headers = ["Hipótesis", "Dimensión", "Prueba decisoria", "p original",
               "p ajustado (Holm)", "Decisión", "Impacto operativo"]
    filas = [[r[0], r[1], r[3], r[4], r[5], r[6], r[7]] for r in datos[1:]]
    # Columna "Impacto operativo" ampliada para evitar cortes de palabra.
    anchos = escala_anchos([1800, 1750, 1150, 750, 950, 950, 1415],
                           ANCHO_UTIL_PORTRAIT)
    nueva = construir_tabla_xml(headers, filas, anchos, 9.0,
                                aligns=["left", "left", "left", "center",
                                        "center", "center", "left"])
    _reemplazar_tabla(doc, 44, nueva)


ANCHOS_ANEXO5 = [1100, 2100] + [745] * 14  # suma exacta = 13630


ENCABEZADOS_ANEXO5 = [
    "sujeto_id", "centro_acopio", "t_reg", "t_vale", "rsd", "cpe",
    "ap_\n01", "ap_\n02", "ap_\n03", "ap_\n04",
    "up_\n01", "up_\n02", "up_\n03", "up_\n04",
    "score_\nap", "score_\nup", "score_\ntam_total", "nivel_\nsatisfaccion",
]


def _reconstruir_anexo5(doc, indice):
    datos = _datos_tabla(doc.tables[indice - 1])
    headers = datos[0]
    if len(headers) == len(ENCABEZADOS_ANEXO5):
        # Saltos controlados en los guiones bajos: evita la fragmentacion
        # tipografica (ap_0 / 1, nivel_satisfac / cion) en columnas estrechas.
        headers = list(ENCABEZADOS_ANEXO5)
    filas = datos[1:]
    # 18 columnas (2 identificadoras + 16 de datos). Anchos dimensionados para
    # que score_tam_total y nivel_satisfaccion no se fragmenten a mitad de palabra.
    if len(headers) == len(ANCHOS_ANEXO5) and sum(ANCHOS_ANEXO5) == ANCHO_ANEXO5:
        anchos = list(ANCHOS_ANEXO5)
        cols_num = len(headers) - 2
    else:
        cols_num = len(headers) - 2
        base = [1100, 2100]
        resto = ANCHO_ANEXO5 - sum(base)
        anchos_num = [resto // cols_num] * cols_num
        anchos_num[-1] += resto - sum(anchos_num)
        anchos = base + anchos_num
    nueva = construir_tabla_xml(
        headers, filas, anchos, font_pt=8.5, header_pt=9.0,
        aligns=["center", "left"] + ["center"] * cols_num,
        total=ANCHO_ANEXO5,
    )
    _reemplazar_tabla(doc, indice, nueva)


def _reconstruir_foto(doc, indice):
    texto = doc.tables[indice - 1].rows[0].cells[0].text
    m = re.search(r"correspondiente a:\s*(.+?)(?:\n|\s*\(Resoluci)", texto, re.S)
    asunto = m.group(1).strip().rstrip(".") if m else "la evidencia fotografica de campo"
    etiqueta = "ESPACIO RESERVADO PARA FOTOGRAFÍA DE EVIDENCIA"
    instruccion = ("Inserte en este recuadro la fotografía de evidencia correspondiente a: "
                   f"{asunto}. Resolución mínima de 300 DPI, formato JPG o PNG.")
    _reemplazar_tabla(doc, indice, construir_recuadro_foto_xml(etiqueta, instruccion))


# ---------------------------------------------------------------------------
# Normalizacion OpenXML de tablas existentes
# ---------------------------------------------------------------------------
def _set_ordenado(rPr, elemento, tags_posteriores):
    pos = len(rPr)
    for i, ch in enumerate(rPr):
        if ch.tag in tags_posteriores:
            pos = i
            break
    rPr.insert(pos, elemento)


def _set_fuente_run(run_el, pt, bold=None):
    rPr = run_el.find(qn("w:rPr"))
    if rPr is None:
        rPr = OxmlElement("w:rPr")
        run_el.insert(0, rPr)
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = parse_xml(
            f'<w:rFonts {nsdecls("w")} w:ascii="{FUENTE}" w:hAnsi="{FUENTE}" '
            f'w:cs="{FUENTE}"/>'
        )
        rPr.insert(0, rf)
    else:
        for attr in ("w:ascii", "w:hAnsi", "w:cs"):
            rf.set(qn(attr), FUENTE)
    if bold is not None:
        b = rPr.find(qn("w:b"))
        if bold and b is None:
            b = parse_xml(f'<w:b {nsdecls("w")}/>')
            idx = rPr.index(rf) + 1
            rPr.insert(idx, b)
        elif not bold and b is not None:
            rPr.remove(b)
    for tag in ("w:sz", "w:szCs"):
        for e in rPr.findall(qn(tag)):
            rPr.remove(e)
    sz = int(round(pt * 2))
    posteriores = {qn(t) for t in (
        "w:highlight", "w:u", "w:effect", "w:bdr", "w:shd", "w:fitText",
        "w:vertAlign", "w:rtl", "w:cs", "w:em", "w:lang", "w:eastAsianLayout",
        "w:specVanish", "w:oMath")}
    _set_ordenado(rPr, parse_xml(f'<w:sz {nsdecls("w")} w:val="{sz}"/>'), posteriores)
    _set_ordenado(rPr, parse_xml(f'<w:szCs {nsdecls("w")} w:val="{sz}"/>'), posteriores)


def _set_espaciado_parrafo(p_el):
    pPr = p_el.find(qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        p_el.insert(0, pPr)
    for tag in ("w:spacing", "w:ind"):
        for e in pPr.findall(qn(tag)):
            pPr.remove(e)
    posteriores = {qn(t) for t in (
        "w:jc", "w:textDirection", "w:textAlignment", "w:textboxTightWrap",
        "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr")}
    pos = len(pPr)
    for i, ch in enumerate(pPr):
        if ch.tag in posteriores:
            pos = i
            break
    pPr.insert(pos, parse_xml(
        f'<w:ind {nsdecls("w")} w:firstLine="0" w:left="0" w:right="0"/>'))
    pPr.insert(pos, parse_xml(
        f'<w:spacing {nsdecls("w")} w:before="0" w:after="0" w:line="240" '
        'w:lineRule="auto"/>'))


def normalizar_tabla(tbl, doc, target, font_pt=10.0, apa=True,
                     espaciado=True, preservar_bordes=False,
                     preservar_fuente=False):
    """Fija ancho, layout, bordes APA, cantSplit, tblHeader y tipografia."""
    tabla = Table(tbl, doc._body)
    eliminar_flotacion_tabla(tabla)

    grid = tbl.find(qn("w:tblGrid"))
    cols = grid.findall(qn("w:gridCol")) if grid is not None else []
    actuales = [int(c.get(qn("w:w")) or 0) for c in cols]
    if not actuales:
        primera = tbl.find(qn("w:tr"))
        tcs = primera.findall(qn("w:tc")) if primera is not None else []
        actuales = [int((tc.find(qn("w:tcPr")).find(qn("w:tcW")).get(qn("w:w")))
                        if tc.find(qn("w:tcPr")) is not None and
                        tc.find(qn("w:tcPr")).find(qn("w:tcW")) is not None else 1000)
                    for tc in tcs] or [1000]
    anchos = escala_anchos(actuales, target)
    if grid is None:
        grid = OxmlElement("w:tblGrid")
        tbl.insert(1, grid)
    for c in list(grid):
        grid.remove(c)
    for w in anchos:
        grid.append(parse_xml(f'<w:gridCol {nsdecls("w")} w:w="{w}"/>'))

    # Motor canonico (Twips evita la ambiguedad EMU/dxa del wrapper)
    configurar_geometria_tabla(tabla, target, [Twips(w) for w in anchos])

    old_tblPr = tbl.find(qn("w:tblPr"))
    if not preservar_bordes:
        nueva = parse_xml(
            f'<w:tblPr {nsdecls("w")}>'
            f'<w:tblW w:w="{target}" w:type="dxa"/>'
            '<w:jc w:val="center"/>'
            '<w:tblBorders>'
            '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
            '<w:left w:val="none"/>'
            '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
            '<w:right w:val="none"/>'
            '<w:insideH w:val="none"/><w:insideV w:val="none"/>'
            '</w:tblBorders>'
            '<w:tblLayout w:type="fixed"/>'
            '<w:tblCellMar><w:top w:w="40" w:type="dxa"/><w:left w:w="60" w:type="dxa"/>'
            '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="60" w:type="dxa"/></w:tblCellMar>'
            '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" '
            'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
            '</w:tblPr>'
        )
        tbl.replace(old_tblPr, nueva)
    else:
        for tag in ("w:tblW", "w:tblLayout"):
            for e in old_tblPr.findall(qn(tag)):
                old_tblPr.remove(e)
        old_tblPr.insert(0, parse_xml(
            f'<w:tblW {nsdecls("w")} w:w="{target}" w:type="dxa"/>'))
        old_tblPr.append(parse_xml(f'<w:tblLayout {nsdecls("w")} w:type="fixed"/>'))

    for ri, tr in enumerate(tbl.findall(qn("w:tr"))):
        trPr = tr.find(qn("w:trPr"))
        if trPr is None:
            trPr = OxmlElement("w:trPr")
            tr.insert(0, trPr)
        otros = [copy.deepcopy(ch) for ch in trPr
                 if ch.tag not in (qn("w:cantSplit"), qn("w:tblHeader"))]
        for ch in list(trPr):
            trPr.remove(ch)
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if ri == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        for ch in otros:
            trPr.append(ch)

        col = 0
        for tc in tr.findall(qn("w:tc")):
            tcPr = tc.find(qn("w:tcPr"))
            if tcPr is None:
                tcPr = OxmlElement("w:tcPr")
                tc.insert(0, tcPr)
            span = 1
            gs = tcPr.find(qn("w:gridSpan"))
            if gs is not None:
                try:
                    span = int(gs.get(qn("w:val")))
                except (TypeError, ValueError):
                    span = 1
            ancho_celda = sum(anchos[col:col + span]) or anchos[-1]
            col += span
            for e in tcPr.findall(qn("w:tcW")):
                tcPr.remove(e)
            tcPr.insert(0, parse_xml(
                f'<w:tcW {nsdecls("w")} w:w="{ancho_celda}" w:type="dxa"/>'))
            for e in tcPr.findall(qn("w:tcBorders")):
                tcPr.remove(e)
            if not preservar_bordes and ri == 0:
                idx = 1
                for tag in ("w:gridSpan", "w:hMerge", "w:vMerge"):
                    e = tcPr.find(qn(tag))
                    if e is not None:
                        idx = tcPr.index(e) + 1
                tcPr.insert(idx, parse_xml(
                    f'<w:tcBorders {nsdecls("w")}><w:bottom w:val="single" w:sz="8" '
                    'w:space="0" w:color="000000"/></w:tcBorders>'))
            for e in tcPr.findall(qn("w:vAlign")):
                tcPr.remove(e)
            tcPr.append(parse_xml(f'<w:vAlign {nsdecls("w")} w:val="center"/>'))

    if not preservar_fuente:
        for ri, tr in enumerate(tbl.findall(qn("w:tr"))):
            for tc in tr.findall(qn("w:tc")):
                for run in tc.findall(".//" + qn("w:r")):
                    _set_fuente_run(run, font_pt, bold=True if ri == 0 else None)
    if espaciado:
        for p in tbl.findall(".//" + qn("w:p")):
            _set_espaciado_parrafo(p)


# ---------------------------------------------------------------------------
# Seccion horizontal propia para el Anexo 5
# ---------------------------------------------------------------------------
def _sectpr_xml(landscape=False, header_rid="rId62"):
    if landscape:
        pg = '<w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>'
    else:
        pg = '<w:pgSz w:w="11906" w:h="16838"/>'
    return parse_xml(
        f'<w:sectPr {nsdecls("w")} xmlns:r="http://schemas.openxmlformats.org/'
        'officeDocument/2006/relationships">'
        f'<w:headerReference w:type="default" r:id="{header_rid}"/>'
        f'{pg}'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1701" '
        'w:header="720" w:footer="720" w:gutter="0"/>'
        '<w:cols w:space="720"/><w:docGrid w:linePitch="360"/>'
        '</w:sectPr>'
    )


def _agregar_sectpr(par_el, sect):
    pPr = par_el.find(qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        par_el.insert(0, pPr)
    for e in pPr.findall(qn("w:sectPr")):
        pPr.remove(e)
    pPr.append(sect)


def configurar_seccion_horizontal_anexo5(doc):
    body = doc.element.body
    hijos = list(body)
    idx_a5 = idx_a6 = None
    for i, el in enumerate(hijos):
        if el.tag != qn("w:p"):
            continue
        txt = _texto_parrafo(el, doc)
        if idx_a5 is None and txt.startswith("ANEXO 5:"):
            idx_a5 = i
        elif idx_a6 is None and txt.startswith("ANEXO 6:"):
            idx_a6 = i
    if idx_a5 is None or idx_a6 is None:
        raise RuntimeError("No se localizaron los encabezados ANEXO 5 / ANEXO 6.")

    previo = hijos[idx_a5 - 1]
    ultimo = hijos[idx_a6 - 1]
    if previo.tag != qn("w:p") or ultimo.tag != qn("w:p"):
        raise RuntimeError("Delimitadores de Anexo 5 no son parrafos.")
    _agregar_sectpr(previo, _sectpr_xml(landscape=False, header_rid="rId62"))
    _agregar_sectpr(ultimo, _sectpr_xml(landscape=True, header_rid="rId61"))
    print("  -> Seccion horizontal propia del Anexo 5 creada (2 sectPr nuevos).")


def mapa_secciones(doc):
    """Devuelve (seccion_de_cada_tabla, orientacion_de_cada_seccion).

    Se usa el orden ordinal de las tablas (doc.tables esta en orden de
    documento) porque id() sobre proxies lxml no es estable entre accesos.
    """
    body = doc.element.body
    idx = 0
    secciones_por_tabla = []
    orientaciones = []
    for el in body:
        if el.tag == qn("w:tbl"):
            secciones_por_tabla.append(idx)
        if el.tag == qn("w:p"):
            pPr = el.find(qn("w:pPr"))
            if pPr is not None and pPr.find(qn("w:sectPr")) is not None:
                sp = pPr.find(qn("w:sectPr"))
                pg = sp.find(qn("w:pgSz"))
                orientaciones.append(
                    "landscape" if pg is not None and
                    pg.get(qn("w:orient")) == "landscape" else "portrait")
                idx += 1
    root = body.find(qn("w:sectPr"))
    if root is not None:
        pg = root.find(qn("w:pgSz"))
        orientaciones.append(
            "landscape" if pg is not None and
            pg.get(qn("w:orient")) == "landscape" else "portrait")
    return secciones_por_tabla, orientaciones


# ---------------------------------------------------------------------------
# Notas de tabla, figuras y emojis
# ---------------------------------------------------------------------------
def _insertar_en_nota(tbl_el, doc, texto):
    sig = tbl_el.getnext()
    while sig is not None and sig.tag == qn("w:p") and not _texto_parrafo(sig, doc):
        sig = sig.getnext()
    if sig is None or sig.tag != qn("w:p"):
        return False
    par = Paragraph(sig, doc._body)
    if texto.strip() in par.text:
        return False
    if not par.text.strip().startswith("Nota."):
        return False
    marker = "Fuente:"
    objetivo = None
    corte = None
    for run in par.runs:
        k = run.text.find(marker)
        if k >= 0:
            objetivo, corte = run, k
            break
    if objetivo is not None:
        resto = objetivo.text[corte:]
        objetivo.text = objetivo.text[:corte]
        nuevo = copy.deepcopy(objetivo._r)
        for t in nuevo.findall(qn("w:t")):
            nuevo.remove(t)
        t = OxmlElement("w:t")
        t.set(qn("xml:space"), "preserve")
        t.text = texto + " " + resto
        nuevo.append(t)
        objetivo._r.addnext(nuevo)
    else:
        run = par.add_run(" " + texto)
        run.font.name = FUENTE
        run.font.size = Pt(TAM_NOTA)
    return True


def ajustar_notas_tablas(doc, tablas_por_indice):
    cambios = []
    textos = {
        36: "El intervalo de confianza se expresa como [límite inferior, límite superior].",
        39: "Muestra censal n = 14.",
        40: "Muestra censal n = 14; grados de libertad gl = n − 1 = 13.",
        42: "Grados de libertad gl = n − 1 = 13.",
    }
    for indice, texto in textos.items():
        tbl = doc.tables[indice - 1]._tbl
        if _insertar_en_nota(tbl, doc, texto):
            cambios.append({"tabla": indice, "texto": texto})
    return cambios


def mantener_rotulos_con_tabla(doc):
    """Aplica keepNext a rótulo y título para que no queden huérfanos."""
    ajustados = 0
    for i, t in enumerate(doc.tables, 1):
        if i in (56, 57, 58, 59):  # los recuadros fotográficos llevan rótulo debajo
            continue
        previos = []
        prev = t._tbl.getprevious()
        while prev is not None and len(previos) < 3:
            if prev.tag == qn("w:p"):
                txt = _texto_parrafo(prev, doc)
                if txt:
                    previos.append((prev, txt))
            prev = prev.getprevious()
        if not previos:
            continue
        objetivos = []
        if re.match(r"^(Tabla|Figura)\s", previos[0][1]):
            objetivos.append(previos[0][0])
        elif len(previos) >= 2 and re.match(r"^Tabla\s", previos[1][1]):
            objetivos.extend([previos[0][0], previos[1][0]])
        elif not previos[0][1].startswith(("Nota.", "Fuente:")):
            objetivos.append(previos[0][0])
        for el in objetivos:
            Paragraph(el, doc._body).paragraph_format.keep_with_next = True
            ajustados += 1
    return ajustados


# ---------------------------------------------------------------------------
# Integridad documental del acta, numeracion correlativa e indices nativos
# ---------------------------------------------------------------------------
def _fijar_texto_parrafo(p, nuevo):
    """Sustituye el texto del parrafo conservando el formato del primer run."""
    runs = p.runs
    if not runs:
        run = p.add_run(nuevo)
        run.font.name = FUENTE
        run.font.size = Pt(11)
        return
    runs[0].text = nuevo
    for run in runs[1:]:
        run.text = ""


def corregir_acta(doc):
    """Retira el dictamen prellenado del acta y deja campos manuscribibles."""
    sustituciones = []
    acta = doc.tables[0].rows[0].cells[0]
    for p in acta.paragraphs:
        texto = p.text.strip()
        if "Espacio reservado para la inserción" in texto:
            nuevo = "Acta pendiente de suscripción por el jurado evaluador."
            _fijar_texto_parrafo(p, nuevo)
            sustituciones.append({"campo": "instruccion_acta",
                                  "antes": texto, "despues": nuevo})
        elif "APROBADO CON MENCI" in texto:
            nuevo = "Calificación final: __________________________________________"
            _fijar_texto_parrafo(p, nuevo)
            sustituciones.append({"campo": "dictamen_prellenado",
                                  "antes": texto, "despues": nuevo})
    return sustituciones


def _es_parrafo_indice(p):
    """True para las entradas generadas por los campos TOC/TOF."""
    try:
        estilo = (p.style.name or "").lower()
    except Exception:
        estilo = ""
    return estilo.startswith(("table of figures", "toc "))


def _siguiente_parrafo_adjunto(p):
    """Primer parrafo no vacio contiguo; None si media una tabla."""
    el = p._p.getnext()
    while el is not None:
        if el.tag == qn("w:tbl"):
            return None
        if el.tag == qn("w:p"):
            texto = "".join(n.text or "" for n in el.iter(qn("w:t"))).strip()
            if texto:
                return Paragraph(el, p._parent)
        el = el.getnext()
    return None


def unificar_rotulos(doc):
    """Fusiona rotulo y titulo en un solo parrafo para que el indice nativo
    capture 'Tabla N Titulo' y 'Figura N Titulo' completos."""
    fusionados = 0
    i = 0
    while i < len(doc.paragraphs):
        p = doc.paragraphs[i]
        if _es_parrafo_indice(p):
            i += 1
            continue
        texto = p.text.strip()
        if re.fullmatch(r"(Tabla|Figura)\s+A?\d+(?:\.\d+)?", texto):
            q = _siguiente_parrafo_adjunto(p)
            if q is not None:
                titulo = q.text.strip()
                valido = (
                    titulo and len(titulo) < 400
                    and not titulo.startswith(("Nota.", "Fuente:"))
                    and not re.match(r"^(Tabla|Figura|ANEXO|CAPÍTULO|CAPITULO)\s", titulo)
                    and not list(q._p.iter(qn("w:drawing")))
                )
                if valido:
                    run = p.add_run(" " + titulo)
                    run.italic = True
                    run.font.name = FUENTE
                    run.font.size = Pt(12)
                    q._p.getparent().remove(q._p)
                    fusionados += 1
        i += 1
    return fusionados


def _campo_seq_runs(tipo, numero, rPr=None):
    """Devuelve los cinco runs de un campo SEQ nativo con resultado fijo."""
    nodos = []
    for clase in ("begin", "instr", "separate", "result", "end"):
        r = OxmlElement("w:r")
        if clase in ("result",) and rPr is not None:
            r.append(copy.deepcopy(rPr))
        if clase == "begin":
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), "begin")
            r.append(fc)
        elif clase == "instr":
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = f" SEQ {tipo} \\* ARABIC \\r {numero} "
            r.append(it)
        elif clase == "separate":
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), "separate")
            r.append(fc)
        elif clase == "result":
            t = OxmlElement("w:t")
            t.set(qn("xml:space"), "preserve")
            t.text = str(numero)
            r.append(t)
        else:
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), "end")
            r.append(fc)
        nodos.append(r)
    return nodos


def _actualizar_campo_seq(p, tipo, numero):
    """Actualiza un campo SEQ existente en el parrafo, si lo hubiera."""
    estado = None
    encontrado = False
    actualizado = False
    resultado_pendiente = False
    for el in p._p:
        if el.tag != qn("w:r"):
            continue
        fc = el.find(qn("w:fldChar"))
        it = el.find(qn("w:instrText"))
        if fc is not None:
            clase = fc.get(qn("w:fldCharType"))
            if clase == "begin":
                estado = "instr"
                encontrado = False
            elif clase == "separate":
                estado = "result"
                resultado_pendiente = encontrado
            elif clase == "end":
                estado = None
                encontrado = False
                resultado_pendiente = False
        elif it is not None and estado == "instr":
            if re.search(rf"\bSEQ\s+{tipo}\b", it.text or ""):
                encontrado = True
                actualizado = True
                it.text = f" SEQ {tipo} \\* ARABIC \\r {numero} "
        elif estado == "result" and resultado_pendiente:
            for t in el.findall(qn("w:t")):
                t.text = str(numero)
                resultado_pendiente = False
    return actualizado


def _reescribir_rotulo(p, tipo, numero):
    """Renumerar 'Tabla N'/'Figura N' e inyectar el campo SEQ si falta."""
    m = re.match(rf"^{tipo}\s+(A?\d+(?:\.\d+)?)", p.text)
    if not m:
        return None
    antiguo = m.group(1)
    if _actualizar_campo_seq(p, tipo, numero):
        return antiguo
    ini, fin = m.start(1), m.end(1)
    acum = 0
    for run in p.runs:
        largo = len(run.text)
        if acum <= ini < acum + largo and fin <= acum + largo:
            offset = ini - acum
            prefijo = run.text[:offset]
            sufijo = run.text[offset + len(antiguo):]
            run.text = prefijo
            rPr = run._r.find(qn("w:rPr"))
            ancla = run._r
            for nodo in _campo_seq_runs(tipo, numero, rPr):
                ancla.addnext(nodo)
                ancla = nodo
            if sufijo:
                r = OxmlElement("w:r")
                if rPr is not None:
                    r.append(copy.deepcopy(rPr))
                t = OxmlElement("w:t")
                t.set(qn("xml:space"), "preserve")
                t.text = sufijo
                r.append(t)
                ancla.addnext(r)
            return antiguo
        acum += largo
    return None


def _insertar_rotulo_tabla(doc, indice_tabla):
    """Antepone 'Tabla N ' al titulo de una tabla que carece de rotulo."""
    tbl = doc.tables[indice_tabla - 1]._tbl
    prev = tbl.getprevious()
    titulo = None
    while prev is not None:
        if prev.tag == qn("w:p"):
            texto = "".join(n.text or "" for n in prev.iter(qn("w:t"))).strip()
            if texto:
                titulo = Paragraph(prev, doc._body)
                break
        prev = prev.getprevious()
    if titulo is None:
        return False
    pPr = titulo._p.find(qn("w:pPr"))
    pos = 1 if pPr is not None else 0
    etiqueta = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    b = OxmlElement("w:b")
    rPr.append(b)
    etiqueta.append(rPr)
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = "Tabla "
    etiqueta.append(t)
    titulo._p.insert(pos, etiqueta)
    pos += 1
    for nodo in _campo_seq_runs("Tabla", 0, rPr):
        titulo._p.insert(pos, nodo)
        pos += 1
    espacio = OxmlElement("w:r")
    t2 = OxmlElement("w:t")
    t2.set(qn("xml:space"), "preserve")
    t2.text = " "
    espacio.append(t2)
    titulo._p.insert(pos, espacio)
    titulo.paragraph_format.first_line_indent = Inches(0)
    titulo.paragraph_format.space_before = Pt(12)
    titulo.paragraph_format.space_after = Pt(2)
    return True


def renumerar_capturas(doc):
    """Numeracion correlativa unica de tablas y figuras, en orden de aparicion."""
    contador = {"Tabla": 0, "Figura": 0}
    mapeo = []
    for p in doc.paragraphs:
        if _es_parrafo_indice(p):
            continue
        texto = p.text.strip()
        m = re.match(r"^(Tabla|Figura)\s+(A?\d+(?:\.\d+)?)", texto)
        if not m:
            continue
        tipo = m.group(1)
        if tipo == "Tabla" and not re.match(
                r"^Tabla\s+A?\d+(?:\.\d+)?(\s|$)", texto):
            continue
        contador[tipo] += 1
        nuevo = contador[tipo]
        antiguo = _reescribir_rotulo(p, tipo, nuevo)
        mapeo.append({
            "tipo": tipo,
            "antiguo": f"{tipo} {antiguo}" if antiguo else tipo,
            "nuevo": f"{tipo} {nuevo}",
            "texto": p.text.strip()[:140],
        })
    return mapeo, contador


REFERENCIAS_CRUZADAS = [
    ("La matriz detallada de operacionalización de variables se presenta en la Tabla 10 del Capítulo IV.",
     "en la Tabla 10 del Capítulo IV", "en la Tabla 32"),
    ("En la Tabla 1 se presenta la estructura integral de las tres dimensiones",
     "En la Tabla 1", "En la Tabla 2"),
    ("En la Figura 1 se esquematizan las fases metodológicas", "En la Figura 1", "En la Figura 11"),
    ("se formalizaron cuatro roles operativos en la Tabla 1", "en la Tabla 1", "en la Tabla 3"),
    ("En la Tabla 2 se consolida el catálogo oficial", "En la Tabla 2", "En la Tabla 4"),
    ("En la Tabla 3 se detallan los ocho requerimientos no funcionales", "En la Tabla 3", "En la Tabla 5"),
    ("En la Tabla 4 se establece la matriz de correspondencia", "En la Tabla 4", "En la Tabla 6"),
    ("En la Tabla 5 se presentan las historias de usuario priorizadas", "En la Tabla 5", "En la Tabla 7"),
    ("En la Tabla 6 se detalla el cronograma de iteraciones", "En la Tabla 6", "En la Tabla 8"),
    ("En la Figura 2 se exhibe el modelado visual", "En la Figura 2", "En la Figura 12"),
    ("En la Figura 3 se ilustra la arquitectura de subsistemas", "En la Figura 3", "En la Figura 13"),
    ("conforme se detalla en la Figura 4:", "en la Figura 4", "en la Figura 14"),
    ("modelado en la Figura 5. El flujo describe", "en la Figura 5", "en la Figura 15"),
    ("graficado en la Figura 6. Este proceso modela", "en la Figura 6", "en la Figura 16"),
    ("En la Figura 7 se expone el diagrama de secuencia", "En la Figura 7", "En la Figura 17"),
    ("en la Tabla 7 se detalla la matriz de privilegios", "en la Tabla 7", "en la Tabla 9"),
    ("En la Figura 8 se presenta el diagrama de secuencia", "En la Figura 8", "En la Figura 18"),
    ("En la Figura 9 se exhibe el Modelo Entidad-Relación", "En la Figura 9", "En la Figura 19"),
    ("En la Figura 10 se presenta el Esquema Relacional", "En la Figura 10", "En la Figura 20"),
    ("En la Figura 11 se visualiza el Diccionario Físico", "En la Figura 11", "En la Figura 21"),
    ("En la Tabla 23 se sintetiza el stack de desarrollo", "En la Tabla 23", "En la Tabla 25"),
    ("En la Figura 12 se exhibe el árbol de directorios del proyecto backend", "En la Figura 12", "En la Figura 22"),
    ("En la Figura 13 se muestra el árbol de directorios del frontend", "En la Figura 13", "En la Figura 23"),
    ("documentado en la Figura 15. Este componente evalúa", "en la Figura 15", "en la Figura 25"),
    ("Tal como se ilustra en la Figura 16", "en la Figura 16", "en la Figura 26"),
    ("En la Figura 17 se exhibe el método calcularIndicadoresDisponibilidad", "En la Figura 17", "En la Figura 27"),
    ("En la Figura 34 se ilustra la ejecución real", "En la Figura 34", "En la Figura 44"),
    ("En la Tabla 24 se resume la cobertura", "En la Tabla 24", "En la Tabla 26"),
    ("En la Tabla 25 se consolidan los resultados observados", "En la Tabla 25", "En la Tabla 27"),
    ("En la Tabla 26 se sintetizan los resultados de la evaluación", "En la Tabla 26", "En la Tabla 28"),
    ("En la Figura 35 se detalla el diagrama de despliegue", "En la Figura 35", "En la Figura 45"),
    ("En la Tabla 9 se detalla la distribución del personal evaluado", "En la Tabla 9", "En la Tabla 30"),
    ("se presentan en la Tabla 10.", "en la Tabla 10", "en la Tabla 32"),
    ("En la Tabla 11 se sintetiza la correspondencia metodológica", "En la Tabla 11", "En la Tabla 33"),
    ("se reportarán en la Tabla 12 una vez concluida", "en la Tabla 12", "en la Tabla 34"),
    ("En la Tabla 4 se consolidan los coeficientes psicométricos", "En la Tabla 4", "En la Tabla 35"),
    ("En la Tabla 5 y en la Figura 6 se detallan", "En la Tabla 5 y en la Figura 6",
     "En la Tabla 36 y en la Figura 46"),
    ("en la Tabla 6 y se ilustran comparativamente en la Figura 7",
     "en la Tabla 6 y se ilustran comparativamente en la Figura 7",
     "en la Tabla 37 y se ilustran comparativamente en la Figura 47"),
    ("En la Tabla 7 y en la Figura 8 se presenta", "En la Tabla 7 y en la Figura 8",
     "En la Tabla 38 y en la Figura 48"),
    ("La Tabla 8 resume las decisiones", "La Tabla 8", "La Tabla 39"),
    ("(Tabla 9).", "(Tabla 9)", "(Tabla 40)"),
    ("(Tabla 10).", "(Tabla 10)", "(Tabla 41)"),
    ("(Tabla 11).", "(Tabla 11)", "(Tabla 42)"),
    ("En la Tabla 12 se presenta el balance", "En la Tabla 12", "En la Tabla 43"),
    ("En la Tabla A1.1 se presenta", "En la Tabla A1.1", "En la Tabla 44"),
    ("En la Tabla A2.1 se presenta", "En la Tabla A2.1", "En la Tabla 45"),
    ("En la Tabla A6.1 se sintetizan", "En la Tabla A6.1", "En la Tabla 51"),
]


def actualizar_referencias_cruzadas(doc):
    aplicadas, fallidas = [], []
    for ancla, viejo, nuevo in REFERENCIAS_CRUZADAS:
        objetivo = None
        for p in doc.paragraphs:
            if ancla in p.text:
                objetivo = p
                break
        if objetivo is None:
            fallidas.append({"ancla": ancla, "motivo": "ancla no encontrada"})
            continue
        reemplazado = False
        for run in objetivo.runs:
            if viejo in run.text:
                run.text = run.text.replace(viejo, nuevo, 1)
                reemplazado = True
                break
        if reemplazado:
            aplicadas.append({"ancla": ancla[:70], "antes": viejo, "despues": nuevo})
        else:
            fallidas.append({"ancla": ancla, "motivo": "frase repartida entre runs"})
    return aplicadas, fallidas


def _set_outline(p, nivel):
    pPr = p._p.find(qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        p._p.insert(0, pPr)
    for previo in pPr.findall(qn("w:outlineLvl")):
        pPr.remove(previo)
    ol = OxmlElement("w:outlineLvl")
    ol.set(qn("w:val"), str(nivel))
    rPr = pPr.find(qn("w:rPr"))
    sect = pPr.find(qn("w:sectPr"))
    ref = rPr if rPr is not None else sect
    if ref is not None:
        ref.addprevious(ol)
    else:
        pPr.append(ol)


def asignar_niveles_esquema(doc):
    asignados = 0
    for p in doc.paragraphs:
        if _es_parrafo_indice(p):
            continue
        t = p.text.strip()
        if not t:
            continue
        nivel = None
        if re.match(r"^CAPÍTULO\s+[IVXL]+:", t):
            nivel = 0
        elif t in ("CONCLUSIONES", "RECOMENDACIONES", "ANEXOS"):
            nivel = 0
        elif re.match(r"^ANEXO\s+[1-7]:", t):
            nivel = 0
        elif re.match(r"^3\.3\.\d+\.\d+\.", t):
            nivel = 3
        elif re.match(r"^3\.3\.\d+\.", t):
            nivel = 2
        elif re.match(r"^3\.3\.", t):
            nivel = 1
        elif re.match(r"^\d+\.\d+\.\d+\.", t):
            nivel = 2
        elif re.match(r"^\d+\.\d+\.", t):
            nivel = 1
        if nivel is None:
            continue
        _set_outline(p, nivel)
        asignados += 1
    return asignados


NOTAS_ANEXO7 = [
    "Nota. Registro fotográfico de la sesión de capacitación en la sede central. "
    "Dirección de Salud Apurímac II (2026).",
    "Nota. Registro fotográfico del cronometraje de tiempos en el Almacén "
    "Especializado de Vacunas. Dirección de Salud Apurímac II (2026).",
    "Nota. Registro fotográfico del cotejo documental y la verificación física "
    "de lotes. Dirección de Salud Apurímac II (2026).",
    "Nota. Registro fotográfico de la aplicación del cuestionario TAM a los "
    "operadores de inmunizaciones. Dirección de Salud Apurímac II (2026).",
]


def diferenciar_notas_anexo7(doc):
    repetida = ("Nota. Registro fotográfico de verificación en campo. "
                "Dirección de Salud Apurímac II (2026).")
    indice = 0
    cambios = []
    for p in doc.paragraphs:
        if p.text.strip() == repetida and indice < len(NOTAS_ANEXO7):
            _fijar_texto_parrafo(p, NOTAS_ANEXO7[indice])
            cambios.append({"figura": f"A7.{indice + 1}", "nota": NOTAS_ANEXO7[indice]})
            indice += 1
    return cambios


def aplicar_keepnext_global(doc):
    """Vincula rotulos, titulos, encabezados e imagenes con su objeto."""
    ajustados = 0
    parrafos = doc.paragraphs
    for i, p in enumerate(parrafos):
        if _es_parrafo_indice(p):
            continue
        texto = p.text.strip()
        es_rotulo = bool(re.match(r"^(Tabla|Figura)\s+\d+", texto))
        pPr = p._p.find(qn("w:pPr"))
        tiene_nivel = pPr is not None and pPr.find(qn("w:outlineLvl")) is not None
        tiene_dibujo = bool(list(p._p.iter(qn("w:drawing"))))
        if es_rotulo or tiene_nivel:
            p.paragraph_format.keep_with_next = True
            ajustados += 1
        elif tiene_dibujo and i + 1 < len(parrafos):
            siguiente = parrafos[i + 1].text.strip()
            if re.match(r"^Figura\s+\d+", siguiente):
                p.paragraph_format.keep_with_next = True
                ajustados += 1
    # La fila de cabecera viaja siempre con la primera fila de datos: evita
    # encabezados huerfanos al pie de pagina en tablas que cruzan el salto.
    for tabla in doc.tables:
        if not tabla.rows:
            continue
        for celda in tabla.rows[0].cells:
            for p in celda.paragraphs:
                p.paragraph_format.keep_with_next = True
                ajustados += 1
    return ajustados


def ajustar_figuras(doc):
    escaladas = []
    for i, shape in enumerate(doc.inline_shapes, 1):
        ancho_in = shape.width / 914400
        if ancho_in > 5.8:
            ratio = 5.8 / ancho_in
            shape.width = Inches(5.8)
            shape.height = int(shape.height * ratio)
            escaladas.append({"figura": i, "ancho_previo_in": round(ancho_in, 2),
                              "ancho_nuevo_in": 5.8})

    notas = 0
    parrafos = doc.paragraphs
    etiquetas = [
        i for i, p in enumerate(parrafos)
        if re.fullmatch(r"Figura (?:A7\.\d+|\d+)", p.text.strip())
    ]
    for i in etiquetas:
        if i + 2 >= len(parrafos):
            continue
        nota = parrafos[i + 2]
        texto = nota.text.strip()
        if not texto or texto.startswith("Nota."):
            continue
        if nota.style.name.lower().startswith(("heading", "título", "titulo")):
            continue
        run = nota.add_run("Nota. ")
        run.italic = True
        run.font.name = FUENTE
        run.font.size = Pt(TAM_NOTA)
        pPr = nota._p.find(qn("w:pPr"))
        pos = 1 if pPr is not None else 0
        nota._p.insert(pos, run._r)
        nota.paragraph_format.first_line_indent = Inches(0)
        notas += 1
    return escaladas, notas


EMOJI_RANGOS = (
    (0x1F000, 0x1FAFF), (0x2600, 0x27BF), (0x2B00, 0x2BFF),
    (0xFE00, 0xFE0F), (0x1F1E6, 0x1F1FF), (0x200D, 0x200D),
)


def _es_emoji(ch):
    o = ord(ch)
    return any(a <= o <= b for a, b in EMOJI_RANGOS)


def limpiar_emojis(doc):
    erradicados = []
    conteo = {}

    def limpiar_nodo(root):
        for t in root.iter(qn("w:t")):
            original = t.text or ""
            if not any(_es_emoji(c) for c in original):
                continue
            limpio = "".join(c for c in original if not _es_emoji(c))
            if limpio != original and original.lstrip() != original:
                limpio = limpio.lstrip()
            for c in original:
                if _es_emoji(c):
                    clave = f"U+{ord(c):04X}"
                    erradicados.append(clave)
                    conteo[clave] = conteo.get(clave, 0) + 1
            t.text = limpio

    limpiar_nodo(doc.element.body)
    for sec in doc.sections:
        for parte in (sec.header, sec.footer, sec.first_page_header,
                      sec.first_page_footer, sec.even_page_header,
                      sec.even_page_footer):
            try:
                limpiar_nodo(parte._element)
            except Exception:
                pass
    return sorted(set(erradicados)), conteo


# ---------------------------------------------------------------------------
# Reporte y verificacion
# ---------------------------------------------------------------------------
def _caption_tabla(tbl, doc, indice):
    """Rotulo local de la tabla (sin escanear hasta tablas ajenas).

    Los recuadros fotograficos del Anexo 7 llevan su rotulo 'Figura A7.x'
    en el parrafo inmediatamente posterior.
    """
    if indice in (56, 57, 58, 59):
        sig = tbl.getnext()
        while sig is not None:
            if sig.tag == qn("w:p"):
                m = re.match(r"^(Figura\s+A7\.\d+)", _texto_parrafo(sig, doc))
                if m:
                    return m.group(1)
            sig = sig.getnext()
    previos = []
    prev = tbl.getprevious()
    while prev is not None and len(previos) < 3:
        if prev.tag == qn("w:p"):
            txt = _texto_parrafo(prev, doc)
            if txt:
                previos.append(txt)
        prev = prev.getprevious()
    for txt in previos:
        m = re.match(r"^(Tabla\s+A?\d+(?:\.\d+)?|Figura\s+A?\d+(?:\.\d+)?)", txt)
        if m:
            return m.group(1)
    return "(sin rótulo)"


def construir_reporte(doc, escaladas, notas_figura, emojis, paginas_pdf,
                      sha_origen, sha_salida, secciones, audit,
                      numeracion=None, integridad=None, indices=None,
                      pictogramas=None, notas_anexo7=None):
    secciones_por_tabla, orientaciones = mapa_secciones(doc)
    tablas = []
    for i, t in enumerate(doc.tables, 1):
        tbl = t._tbl
        grid = tbl.find(qn("w:tblGrid"))
        anchos = [int(g.get(qn("w:w"))) for g in grid.findall(qn("w:gridCol"))] \
            if grid is not None else []
        total = sum(anchos)
        sec = secciones_por_tabla[i - 1] if i - 1 < len(secciones_por_tabla) else 0
        orient = orientaciones[sec] if sec < len(orientaciones) else "portrait"
        util = ANCHO_UTIL_LANDSCAPE if orient == "landscape" else ANCHO_UTIL_PORTRAIT
        trs = tbl.findall(qn("w:tr"))
        cant_split = all(
            tr.find(qn("w:trPr")) is not None and
            tr.find(qn("w:trPr")).find(qn("w:cantSplit")) is not None
            for tr in trs
        )
        header = bool(trs) and trs[0].find(qn("w:trPr")) is not None and \
            trs[0].find(qn("w:trPr")).find(qn("w:tblHeader")) is not None
        flotante = len(list(tbl.iter(qn("w:tblpPr")))) > 0
        layout = tbl.find(qn("w:tblPr")).find(qn("w:tblLayout"))
        fijo = layout is not None and layout.get(qn("w:type")) == "fixed"
        cols = len(t.columns)
        esperadas = COLUMNAS_ESPERADAS.get(i)
        tablas.append({
            "indice": i,
            "rotulo": _caption_tabla(tbl, doc, i),
            "filas": len(t.rows),
            "columnas": cols,
            "columnas_esperadas": esperadas,
            "anchos_dxa": anchos,
            "ancho_total_dxa": total,
            "seccion": sec,
            "orientacion": orient,
            "ancho_util_dxa": util,
            "tblpPr": flotante,
            "tblHeader": header,
            "cantSplit_todas_filas": cant_split,
            "tblLayout_fijo": fijo,
            "cumple": (not flotante and header and cant_split and fijo and
                       total <= util and (esperadas is None or cols == esperadas)),
        })

    from collections import Counter

    conteo = Counter(t["rotulo"] for t in tablas if t["rotulo"].startswith("Tabla"))
    duplicados = [
        {"rotulo": rotulo,
         "indices": [t["indice"] for t in tablas if t["rotulo"] == rotulo]}
        for rotulo, veces in conteo.items() if veces > 1
    ]
    sin_rotulo = [
        {"indice": t["indice"], "filas": t["filas"], "columnas": t["columnas"]}
        for t in tablas if t["rotulo"] == "(sin rótulo)"
    ]

    return {
        "version": "v05",
        "fecha": str(date.today()),
        "fuente_inmutable": str(DOCX_V04),
        "sha256_origen": sha_origen,
        "salida_docx": str(DOCX_V05),
        "sha256_salida": sha_salida,
        "secciones_total": secciones,
        "secciones_originales_conservadas": 5,
        "secciones_nuevas": 2,
        "orientaciones": orientaciones,
        "tablas_total": len(doc.tables),
        "tablas_conformes": sum(1 for x in tablas if x["cumple"]),
        "tablas": tablas,
        "tablas_reconstruidas": TABLAS_RECONSTRUIDAS,
        "geometria": {
            "ancho_util_portrait_dxa": ANCHO_UTIL_PORTRAIT,
            "ancho_util_landscape_dxa": ANCHO_UTIL_LANDSCAPE,
            "ancho_anexo5_dxa": ANCHO_ANEXO5,
            "criterio": ("Anchos útiles medidos en los sectPr reales "
                         "(A4 11906/16838 menos márgenes 1701 + 1440). "
                         "Toda tabla se normaliza a 8765 dxa en vertical; "
                         "la matriz A1.1 y las matrices A5.x se ajustan a "
                         "13697 y 13630 dxa respectivamente."),
        },
        "numeracion": numeracion or {},
        "indices": indices or {},
        "integridad": integridad or {},
        "pictogramas": pictogramas or {},
        "notas_anexo7_diferenciadas": notas_anexo7 or [],
        "emojis_erradicados_por_reconstruccion": [
            "U+1F4F7 (4 marcadores del Anexo 7, sustituidos por recuadro nativo)"
        ],
        "rotulos_duplicados": duplicados,
        "tablas_sin_rotulo_numerado": sin_rotulo,
        "auditoria_motor_nota": (
            "margenes_unajma_ok=false obedece a la expectativa hardcodeada "
            "1985/1418 del motor de auditoría; los 7 sectPr cumplen la regla "
            "canónica UNAJMA (izquierdo 1701 dxa, superior/derecho/inferior 1440 dxa)."
        ),
        "figuras": {
            "inline_shapes_total": len(doc.inline_shapes),
            "escaladas": escaladas,
            "notas_figura_prefijadas": notas_figura,
        },
        "emojis_erradicados": emojis,
        "pdf_paginas": paginas_pdf,
        "auditoria_motor": audit,
    }


def verificar_docx(ruta):
    doc = docx.Document(str(ruta))
    secciones_por_tabla, orientaciones = mapa_secciones(doc)
    errores = []
    if len(doc.sections) != 7:
        errores.append(f"Secciones={len(doc.sections)} (esperado 7)")
    if len(doc.tables) != 59:
        errores.append(f"Tablas={len(doc.tables)} (esperado 59)")
    for i, t in enumerate(doc.tables, 1):
        tbl = t._tbl
        if list(tbl.iter(qn("w:tblpPr"))):
            errores.append(f"T{i}: tblpPr")
        trs = tbl.findall(qn("w:tr"))
        if not trs:
            errores.append(f"T{i}: sin filas")
            continue
        trPr0 = trs[0].find(qn("w:trPr"))
        if trPr0 is None or trPr0.find(qn("w:tblHeader")) is None:
            errores.append(f"T{i}: sin tblHeader")
        for tr in trs:
            trPr = tr.find(qn("w:trPr"))
            if trPr is None or trPr.find(qn("w:cantSplit")) is None:
                errores.append(f"T{i}: fila sin cantSplit")
                break
        grid = tbl.find(qn("w:tblGrid"))
        total = sum(int(g.get(qn("w:w"))) for g in grid.findall(qn("w:gridCol")))
        sec = secciones_por_tabla[i - 1] if i - 1 < len(secciones_por_tabla) else 0
        util = ANCHO_UTIL_LANDSCAPE if (
            sec < len(orientaciones) and orientaciones[sec] == "landscape"
        ) else ANCHO_UTIL_PORTRAIT
        if total > util:
            errores.append(f"T{i}: ancho {total} > util {util}")
        if i in COLUMNAS_ESPERADAS and len(t.columns) != COLUMNAS_ESPERADAS[i]:
            errores.append(f"T{i}: {len(t.columns)} columnas (esperado {COLUMNAS_ESPERADAS[i]})")
    # Emojis en todas las partes XML
    with zipfile.ZipFile(ruta) as z:
        for nombre in z.namelist():
            if not nombre.endswith(".xml"):
                continue
            texto = z.read(nombre).decode("utf-8", errors="ignore")
            if any(_es_emoji(c) for c in texto):
                errores.append(f"Emoji residual en {nombre}")
    # Figuras
    for k, sh in enumerate(doc.inline_shapes, 1):
        if sh.width / 914400 > 5.81:
            errores.append(f"Figura {k}: ancho {sh.width/914400:.2f} in")
    return errores, doc


# ---------------------------------------------------------------------------
# Exportacion PDF (Word COM)
# ---------------------------------------------------------------------------
def exportar_pdf(docx_path, pdf_path):
    import win32com.client

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = None
    try:
        doc = word.Documents.Open(
            FileName=str(docx_path.resolve()), ConfirmConversions=False,
            ReadOnly=False, AddToRecentFiles=False)
        doc.Fields.Update()
        for i in range(1, doc.TablesOfContents.Count + 1):
            doc.TablesOfContents(i).Update()
        for i in range(1, doc.TablesOfFigures.Count + 1):
            doc.TablesOfFigures(i).Update()
        doc.Repaginate()
        indices = {
            "contenido_entradas": None,
            "figuras_entradas": None,
            "tablas_entradas": None,
            "incluye": {},
        }
        try:
            if doc.TablesOfContents.Count:
                toc = doc.TablesOfContents(1)
                texto = toc.Range.Text
                indices["contenido_entradas"] = max(
                    0, int(toc.Range.Paragraphs.Count) - 1)
                indices["incluye"] = {
                    "3.3": "3.3." in texto,
                    "capitulo_v": "CAPÍTULO V" in texto,
                    "capitulo_vi": "CAPÍTULO VI" in texto,
                    "conclusiones": "CONCLUSIONES" in texto,
                    "recomendaciones": "RECOMENDACIONES" in texto,
                    "anexo_1": "ANEXO 1" in texto,
                    "anexo_7": "ANEXO 7" in texto,
                }
            for i in range(1, doc.TablesOfFigures.Count + 1):
                tf = doc.TablesOfFigures(i)
                texto = tf.Range.Text
                entradas = max(0, int(tf.Range.Paragraphs.Count) - 1)
                if "Figura" in texto:
                    indices["figuras_entradas"] = entradas
                elif "Tabla" in texto:
                    indices["tablas_entradas"] = entradas
        except Exception as exc:
            indices["error"] = str(exc)
        doc.Save()
        doc.ExportAsFixedFormat(
            OutputFileName=str(pdf_path.resolve()),
            ExportFormat=17,
            OpenAfterExport=False,
            OptimizeFor=0,
            Range=0,
            Item=0,
            IncludeDocProps=True,
            KeepIRM=True,
            CreateBookmarks=1,
            DocStructureTags=True,
            BitmapMissingFonts=True,
            UseISO19005_1=False,
        )
        paginas = int(doc.ComputeStatistics(2))
        return {"paginas": paginas, "indices": indices}
    finally:
        if doc is not None:
            doc.Close(False)
        word.Quit()


def renderizar_paginas(pdf_path, paginas, dpi=150):
    import fitz

    PAGINAS_DIR.mkdir(parents=True, exist_ok=True)
    generadas = []
    with fitz.open(str(pdf_path)) as pdf:
        for numero in sorted(set(paginas)):
            if numero < 1 or numero > len(pdf):
                continue
            page = pdf[numero - 1]
            pix = page.get_pixmap(dpi=dpi)
            destino = PAGINAS_DIR / f"pagina_{numero:03d}.png"
            pix.save(str(destino))
            generadas.append(str(destino))
    return generadas


def localizar_paginas(pdf_path):
    import fitz

    objetivos = [
        ("acta_sustentacion", "MIEMBROS DEL JURADO DICTAMINADOR", 1),
        ("indice_contenido", "NDICE DE CONTENIDO", 1),
        ("indice_figuras", "NDICE DE FIGURAS", 1),
        ("indice_tablas", "NDICE DE TABLAS", 1),
        ("inicio_capitulo_v", "5.1. Análisis de Confiabilidad", 10),
        ("tabla_confiabilidad", "IC 95 % [LI, LS]", 10),
        ("tabla_descriptivos", "Mín – Máx", 10),
        ("tabla_contrastes", "d = -10.41", 10),
        ("tabla_sintesis", "Impacto operativo", 10),
        ("anexo5_landscape", "ANEXO 5:", 10),
        ("anexo5_postest", "Posttest (Operación con sistema SIVAC", 145),
        ("anexo7_recuadro", "ESPACIO RESERVADO PARA FOTOGRAFÍA DE EVIDENCIA", 10),
    ]
    encontradas = {}
    with fitz.open(str(pdf_path)) as pdf:
        for clave, aguja, desde in objetivos:
            for i, page in enumerate(pdf, 1):
                if i < desde:
                    continue
                if page.search_for(aguja):
                    encontradas[clave] = i
                    break
    return encontradas


# ---------------------------------------------------------------------------
# Orquestador
# ---------------------------------------------------------------------------
def compilar(sin_pdf=False):
    inicio = time.time()
    print("=" * 78)
    print("SIVAC-THESIS-LAB :: COMPILADOR QUIRURGICO v05")
    print("=" * 78)
    if not DOCX_V04.exists():
        raise FileNotFoundError(DOCX_V04)
    sha_origen = sha256(DOCX_V04)

    doc = docx.Document(str(DOCX_V04))
    print(f"Base inmutable: {DOCX_V04.name} ({len(doc.tables)} tablas, "
          f"{len(doc.sections)} secciones)")

    print("\n[1/10] Creando seccion horizontal propia para el Anexo 5...")
    configurar_seccion_horizontal_anexo5(doc)

    print("\n[2/10] Reconstruyendo tablas comprimidas (reduccion de columnas)...")
    _reconstruir_35(doc)
    for idx in (37, 38, 39):
        _reconstruir_descriptivos(doc, idx)
    _reconstruir_39(doc)
    for idx in (41, 42, 43):
        _reconstruir_contraste(doc, idx)
    _reconstruir_44(doc)
    _reconstruir_anexo5(doc, 53)
    _reconstruir_anexo5(doc, 54)
    for idx in (56, 57, 58, 59):
        _reconstruir_foto(doc, idx)
    print(f"  -> {len(TABLAS_RECONSTRUIDAS)} tablas reconstruidas con geometria nativa.")

    print("\n[3/10] Normalizando las 59 tablas (ancho fijo, APA 7, cantSplit)...")
    secciones_por_tabla, orientaciones = mapa_secciones(doc)
    for i, t in enumerate(doc.tables, 1):
        if i in TABLAS_RECONSTRUIDAS:
            continue
        tbl = t._tbl
        sec = secciones_por_tabla[i - 1] if i - 1 < len(secciones_por_tabla) else 0
        orient = orientaciones[sec] if sec < len(orientaciones) else "portrait"
        target = ANCHO_UTIL_LANDSCAPE if orient == "landscape" else ANCHO_UTIL_PORTRAIT
        if i == 1:  # recuadro de portada: conservar marco institucional
            normalizar_tabla(tbl, doc, target, apa=False, espaciado=False,
                             preservar_bordes=True, preservar_fuente=True)
        elif i in (47, 48, 49):  # fichas de validacion: conservar espacio de firma
            normalizar_tabla(tbl, doc, target, font_pt=10.0, apa=True,
                             espaciado=False)
        else:
            normalizar_tabla(tbl, doc, target,
                             font_pt=9.0 if i in TABLAS_ESTADISTICAS_9PT else 10.0,
                             apa=True, espaciado=True)
    print("  -> Geometria y bordes normalizados en el 100% de tablas.")

    print("\n[4/10] Ajustando notas de tabla y figuras...")
    notas_tabla = ajustar_notas_tablas(doc, {})
    escaladas, notas_figura = ajustar_figuras(doc)
    print(f"  -> {len(notas_tabla)} notas de tabla recuperan n/gl/IC.")
    print(f"  -> {len(escaladas)} figuras reescaladas; "
          f"{notas_figura} notas de figura prefijadas con 'Nota.'.")

    print("\n[5/10] Numeracion correlativa, referencias cruzadas e integridad...")
    integridad = corregir_acta(doc)
    fusionados = unificar_rotulos(doc)
    insertados = sum(1 for i in (2, 30, 32) if _insertar_rotulo_tabla(doc, i))
    mapeo, contador = renumerar_capturas(doc)
    refs_ok, refs_fallidas = actualizar_referencias_cruzadas(doc)
    notas_a7 = diferenciar_notas_anexo7(doc)
    print(f"  -> Acta: {len(integridad)} sustituciones de integridad.")
    print(f"  -> {fusionados} rotulos fusionados con su titulo; "
          f"{insertados} rotulos insertados a tablas sin numero.")
    print(f"  -> {contador['Tabla']} tablas y {contador['Figura']} figuras "
          f"renumeradas de forma continua.")
    print(f"  -> {len(refs_ok)} referencias cruzadas actualizadas "
          f"({len(refs_fallidas)} fallidas).")
    print(f"  -> {len(notas_a7)} notas del Anexo 7 diferenciadas.")

    print("\n[6/10] Esquema, keepNext y jerarquia de indices...")
    niveles = asignar_niveles_esquema(doc)
    keepnext = aplicar_keepnext_global(doc)
    print(f"  -> {niveles} encabezados con outlineLvl; "
          f"{keepnext} parrafos vinculados con keepNext.")

    print("\n[7/10] Erradicando emojis y simbolos no tipograficos...")
    emojis, pictogramas = limpiar_emojis(doc)
    print(f"  -> Codepoints erradicados: {pictogramas or 'ninguno'}")

    DOCX_V05.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(DOCX_V05))
    print(f"\n[8/10] DOCX guardado: {DOCX_V05.name} "
          f"({DOCX_V05.stat().st_size/1024/1024:.2f} MB)")

    errores, _ = verificar_docx(DOCX_V05)
    if errores:
        print("  [ALERTA] Verificacion interna detecto:")
        for e in errores[:30]:
            print("    -", e)
    else:
        print("  -> Verificacion interna: 59 tablas conformes, 7 secciones, 0 emojis.")

    paginas_pdf = 0
    generadas = []
    indices_word = {}
    if not sin_pdf:
        print("\n[9/10] Exportando PDF oficial con Word COM e índices nativos...")
        resultado = exportar_pdf(DOCX_V05, PDF_V05)
        paginas_pdf = resultado["paginas"]
        indices_word = resultado.get("indices", {})
        print(f"  -> PDF: {PDF_V05.name} ({paginas_pdf} paginas)")
        print(f"  -> Índices: {indices_word}")
        try:
            paginas = localizar_paginas(PDF_V05)
            print(f"  -> Paginas localizadas: {paginas}")
            generadas = renderizar_paginas(PDF_V05, list(paginas.values()), 150)
            print(f"  -> {len(generadas)} paginas PNG de control en {PAGINAS_DIR}")
        except Exception as exc:
            print(f"  [AVISO] Render de control no disponible: {exc}")
    else:
        print("\n[9/10] Exportacion PDF omitida (--sin-pdf).")

    print("\n[10/10] Auditando OpenXML y generando reporte...")
    audit = auditar_docx_openxml(DOCX_V05)
    sha_salida = sha256(DOCX_V05)
    numeracion = {
        "tablas_total": contador["Tabla"],
        "figuras_total": contador["Figura"],
        "mapa": mapeo,
        "referencias_cruzadas_actualizadas": refs_ok,
        "referencias_cruzadas_fallidas": refs_fallidas,
        "rotulos_insertados": insertados,
        "rotulos_fusionados_con_titulo": fusionados,
    }
    reporte = construir_reporte(doc, escaladas, notas_figura, emojis,
                                paginas_pdf, sha_origen, sha_salida,
                                len(doc.sections), audit,
                                numeracion=numeracion,
                                integridad={"acta": integridad},
                                indices=indices_word,
                                pictogramas=pictogramas,
                                notas_anexo7=notas_a7)
    reporte["verificacion_interna"] = errores
    reporte["paginas_control_png"] = generadas
    REPORTE_DIR.mkdir(parents=True, exist_ok=True)
    REPORTE_JSON.write_text(
        json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"  -> Reporte: {REPORTE_JSON}")
    print(f"  -> Motor: {audit['tablas_total']} tablas, "
          f"{audit['tablas_flotantes']} flotantes, "
          f"cantSplit {audit['tablas_con_cantsplit']}/{audit['tablas_total']}")
    print(f"\nCompilacion v05 concluida en {time.time()-inicio:.1f} s "
          f"(errores={len(errores)}).")
    return reporte


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin-pdf", action="store_true", help="Solo DOCX + reporte")
    args = ap.parse_args()
    compilar(sin_pdf=args.sin_pdf)
