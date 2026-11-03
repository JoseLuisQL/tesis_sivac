# -*- coding: utf-8 -*-
"""
Constructor canónico del paquete de instrumentos de recolección SIVAC v03.

Compila las ocho especificaciones Markdown cerradas de
``salidas/instrumentos/INSTRUMENTOS_REDISENADOS_FANY_20261102_v03/_ESPECIFICACION``
a ocho documentos DOCX individuales, sus PDF oficiales y el maestro
``00_INSTRUMENTOS_RECOLECCION_SIVAC_v03.docx``.

Principios de maquetación
-------------------------
* A4 vertical (11906 x 16838 dxa). Márgenes: izquierdo 1701 dxa (3.0 cm);
  superior, derecho e inferior 1417 dxa (2.5 cm). Ancho útil 8788 dxa (15.5 cm).
* Times New Roman 10 pt en cuerpo y 9.5 pt en tablas y notas. Ninguna fuente
  por debajo de 9.5 pt.
* Encabezado institucional reutilizado de la referencia v02: dos logotipos
  simétricos (escudo UNAJMA y logotipo EPIS) y regla gris con paginación.
* Rejilla visible solo en los formularios (fichas, cuestionario, control y
  certificado). Protocolo y diccionario usan tablas APA 7 de tres líneas.
* Sin OMML en celdas. Toda la geometría, bordes y anchos se delegan en
  ``scripts/utilidades/docx_quirurgico.py``.

Uso
---
    python scripts/compiladores/instrumentos_recoleccion_v03_builder.py
    python scripts/compiladores/instrumentos_recoleccion_v03_builder.py --sin-pdf
    python scripts/compiladores/instrumentos_recoleccion_v03_builder.py --solo 01_FICHA_TIEMPOS_v03

No crea archivos temporales: el DOCX se construye en memoria a partir de una
copia de lectura de la referencia v02 y se escribe directamente en la carpeta
destino.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from docx import Document
from docx.enum.table import WD_ROW_HEIGHT_RULE, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from scripts.utilidades import docx_quirurgico as dq  # noqa: E402
from scripts.comun import seguridad  # noqa: E402

V02_DIR = RAIZ / "salidas" / "instrumentos" / "INSTRUMENTOS_REDISENADOS_FANY_20261022_v02"
V02_DOCX = V02_DIR / "00_INSTRUMENTOS_RECOLECCION_SIVAC.docx"
SALIDA = RAIZ / "salidas" / "instrumentos" / "INSTRUMENTOS_REDISENADOS_FANY_20261102_v03"

ANCHO_DXA = 8788          # 15.5 cm
DXA_CM = 567.0            # twips por centímetro
SP = 20                   # 10.0 pt en medios puntos
SP_TABLA = 19             # 9.5 pt en medios puntos

# Márgenes internos de celda: 1 mm lateral; 0.5 mm vertical para las tablas
# densas (la nota de producción fija 1 mm para el ajuste horizontal de las
# horas hh:mm:ss, que es donde el margen es determinante).
MARGEN_LR = 57            # 1 mm
MARGEN_TB = 28            # 0.5 mm


# ---------------------------------------------------------------------------
# Utilidades de bajo nivel
# ---------------------------------------------------------------------------

def _dxa(anchos_cm: Sequence[float]) -> List[int]:
    """Convierte anchos en cm a dxa y recorta solo si exceden 8788 dxa.

    No se rellena la última columna: las tablas cuyo ancho declarado suma
    menos que el área útil (por ejemplo, la página A de la ficha de
    auditoría, 15.46 cm) conservan la geometría exacta de la especificación.
    """
    valores = [int(round(a * DXA_CM)) for a in anchos_cm]
    delta = ANCHO_DXA - sum(valores)
    if delta < 0:
        valores[-1] += delta
    return valores


_TOKEN = re.compile(r"(\*\*.+?\*\*|\^\{[^}]*\}|_\{[^}]*\})")


def add_runs(parrafo, texto: str, size: int = SP, bold: bool = False,
             italic: bool = False) -> None:
    """Escribe texto con marcas ``**negrita**``, ``_{subíndice}`` y
    ``^{superíndice}``. Las secuencias de guiones bajos son líneas de
    relleno y nunca se interpretan como cursiva."""
    if texto is None:
        return
    for parte in _TOKEN.split(texto):
        if not parte:
            continue
        b, i = bold, italic
        va = None
        t = parte
        if parte.startswith("**") and parte.endswith("**") and len(parte) > 4:
            t, b = parte[2:-2], True
        elif parte.startswith("^{") and parte.endswith("}"):
            t, va = parte[2:-1], "superscript"
        elif parte.startswith("_{") and parte.endswith("}"):
            t, va = parte[2:-1], "subscript"
        run = parrafo.add_run(t)
        run.font.size = Pt(size / 2)
        run.bold = b
        run.italic = i
        if va == "superscript":
            run.font.superscript = True
        elif va == "subscript":
            run.font.subscript = True


def par(doc, texto: str = "", size: int = SP, bold: bool = False,
        italic: bool = False, align: str = "left", before: float = 0,
        after: float = 0, line: float = 1.0, left: float = 0,
        hanging: float = 0, first: float = 0, keep: bool = False,
        keep_lines: bool = False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    pf.alignment = {
        "left": WD_ALIGN_PARAGRAPH.LEFT,
        "right": WD_ALIGN_PARAGRAPH.RIGHT,
        "center": WD_ALIGN_PARAGRAPH.CENTER,
        "both": WD_ALIGN_PARAGRAPH.JUSTIFY,
    }[align]
    if left:
        pf.left_indent = Cm(left)
    if hanging:
        pf.first_line_indent = Cm(-hanging)
    elif first:
        pf.first_line_indent = Cm(first)
    pf.keep_with_next = keep
    pf.keep_together = keep_lines
    if texto:
        add_runs(p, texto, size=size, bold=bold, italic=italic)
    return p


def titulo(doc, texto: str, before: float = 0, after: float = 3):
    return par(doc, texto, size=24, bold=True, before=before, after=after,
               keep=True)


def titulo_salto(doc, texto: str, before: float = 0, after: float = 3):
    """Título que inicia página sin párrafo vacío de salto.

    Evita la página en blanco que produce un párrafo de salto cuando el
    contenido anterior llena exactamente el área imprimible.
    """
    p = titulo(doc, texto, before=before, after=after)
    p.paragraph_format.page_break_before = True
    return p


def subtitulo(doc, texto: str, before: float = 0, after: float = 2):
    return par(doc, texto, size=SP, bold=True, before=before, after=after,
               keep=True)


def h2(doc, texto: str, before: float = 7, after: float = 2):
    return par(doc, texto, size=SP, bold=True, before=before, after=after,
               keep=True, keep_lines=True)


def item(doc, marcador: str, texto: str, size: int = SP, left: float = 0.7,
         hanging: float = 0.55, before: float = 0, after: float = 1,
         line: float = 1.0):
    p = par(doc, "", size=size, before=before, after=after, line=line,
            left=left, hanging=hanging)
    p.paragraph_format.tab_stops.add_tab_stop(Cm(left))
    add_runs(p, f"{marcador}\t{texto}", size=size)
    return p


def salto_pagina(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run()
    br = OxmlElement("w:br")
    br.set(qn("w:type"), "page")
    run._r.append(br)
    return p


def linea_relleno(doc, texto: str = "", antes: float = 1.0, size: int = SP):
    """Línea de guiones para campos manuscritos, con espacio posterior medido."""
    return par(doc, texto, size=size, before=antes, after=0, line=1.4)


# ---------------------------------------------------------------------------
# Tablas nativas
# ---------------------------------------------------------------------------

def _valor_celda(spec) -> str:
    if isinstance(spec, dict):
        return spec.get("texto", spec.get("text", ""))
    return "" if spec is None else str(spec)


def _es_negrita(spec, por_defecto: bool) -> bool:
    if isinstance(spec, dict):
        return bool(spec.get("negrita", spec.get("bold", por_defecto)))
    return por_defecto


def _alineacion(spec, por_defecto: str) -> str:
    if isinstance(spec, dict):
        return spec.get("alineacion", spec.get("align", por_defecto))
    return por_defecto


def _reiniciar_celda(celda):
    tc = celda._tc
    parrafos = tc.findall(qn("w:p"))
    for p in parrafos[1:]:
        tc.remove(p)
    p = celda.paragraphs[0]
    for hijo in list(p._element):
        if hijo.tag != qn("w:pPr"):
            p._element.remove(hijo)
    return p


def _escribir_celda(celda, spec, size: int, bold_defecto: bool,
                    align_defecto: str, margen_lr: int, margen_tb: int,
                    linea: float = 1.0):
    texto = _valor_celda(spec)
    bold = _es_negrita(spec, bold_defecto)
    align = _alineacion(spec, align_defecto)
    valign = spec.get("valign", "center") if isinstance(spec, dict) else "center"
    size_cel = spec.get("size", size) if isinstance(spec, dict) else size

    p = _reiniciar_celda(celda)
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = linea
    pf.left_indent = Cm(0)
    pf.first_line_indent = Cm(0)
    pf.alignment = {
        "left": WD_ALIGN_PARAGRAPH.LEFT,
        "right": WD_ALIGN_PARAGRAPH.RIGHT,
        "center": WD_ALIGN_PARAGRAPH.CENTER,
        "both": WD_ALIGN_PARAGRAPH.JUSTIFY,
    }[align]
    if texto:
        add_runs(p, texto, size=size_cel, bold=bold)

    from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
    celda.vertical_alignment = {
        "top": WD_CELL_VERTICAL_ALIGNMENT.TOP,
        "center": WD_CELL_VERTICAL_ALIGNMENT.CENTER,
        "bottom": WD_CELL_VERTICAL_ALIGNMENT.BOTTOM,
    }[valign]


def _fijar_margen_celda(celda, margen_lr: int, margen_tb: int):
    """Fija w:tcMar en una celda respetando el orden del esquema CT_TcPr."""
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


def _geometria(tabla, anchos_dxa: Sequence[int]):
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

    # tcW por celda, respetando gridSpan de las celdas combinadas.
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


def tabla(doc, filas: Sequence[Sequence[Any]], anchos_cm: Sequence[float],
          header_rows: int = 1, apa: bool = False, size: int = SP_TABLA,
          merges: Sequence[Tuple[int, int, int, int]] = (),
          align_defecto: str = "left", header_align: str = "center",
          margen_lr: int = MARGEN_LR, margen_tb: int = MARGEN_TB,
          margen_lr_cabecera: Optional[int] = None,
          alto_filas_cm: Optional[float] = None,
          repetir_encabezado: bool = True, bold_defecto: bool = False,
          linea_celda: float = 1.0):
    """Crea una tabla nativa con geometría exacta y bordes reglamentarios.

    ``margen_lr_cabecera`` permite estrechar los márgenes laterales solo en la
    fila de rótulos: los rótulos de 9.5 pt necesitan ese margen adicional para
    no partirse, mientras las celdas de datos conservan el margen de 1 mm que
    exige la nota de producción.
    """
    nfilas = len(filas)
    ncols = len(anchos_cm)
    anchos_dxa = _dxa(anchos_cm)

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
        celda = t.cell(r1, c1)
        celda.merge(t.cell(r2, c2))
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                if (r, c) != (r1, c1):
                    cubiertas.add((r, c))

    for r, fila in enumerate(filas):
        for c in range(ncols):
            if (r, c) in cubiertas:
                continue
            spec = fila[c] if c < len(fila) else ""
            es_cabecera = r < header_rows
            celda = t.cell(r, c)
            _escribir_celda(
                celda, spec, size,
                bold_defecto=(True if es_cabecera else bold_defecto),
                align_defecto=(header_align if es_cabecera else align_defecto),
                margen_lr=margen_lr, margen_tb=margen_tb,
                linea=linea_celda,
            )
            if es_cabecera and margen_lr_cabecera is not None:
                _fijar_margen_celda(celda, margen_lr_cabecera, margen_tb)

    for i, fila in enumerate(t.rows):
        dq._preparar_tr(fila._tr, cant_split=True,
                        tbl_header=(repetir_encabezado and i < header_rows))
        if alto_filas_cm is not None and i >= header_rows:
            fila.height = Cm(alto_filas_cm)
            fila.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST

    _geometria(t, anchos_dxa)
    dq.eliminar_flotacion_tabla(t)
    if apa:
        dq.aplicar_bordes_apa7_tabla(t)
    else:
        dq.aplicar_bordes_campo(t, exterior_sz=8, interior_sz=4)
    return t


def nota(doc, texto: str, before: float = 2, after: float = 4):
    """Nota al pie de tabla o figura: 9.5 pt, sin sangría."""
    return par(doc, texto, size=SP_TABLA, before=before, after=after)


# ---------------------------------------------------------------------------
# Plantilla y estilos
# ---------------------------------------------------------------------------

def nueva_plantilla() -> Document:
    """Documento vacío con el encabezado, la sección y los logotipos de v02."""
    doc = Document(str(V02_DOCX))
    body = doc.element.body
    for hijo in list(body):
        if hijo.tag != qn("w:sectPr"):
            body.remove(hijo)

    seccion = doc.sections[0]
    sectPr = seccion._sectPr
    for etiqueta in ("w:docGrid",):
        for nodo in sectPr.findall(qn(etiqueta)):
            sectPr.remove(nodo)

    # El pie heredado de v02 conserva un rótulo del instrumento anterior: se
    # vacía. El encabezado se conserva íntegro (logotipos y paginación) y solo
    # se eleva su tipografía a 9.5 pt, porque v02 usaba 8.5 pt.
    for p in seccion.footer.paragraphs:
        for r in list(p.runs):
            r._r.getparent().remove(r._r)
    for tabla_pie in seccion.footer.tables:
        for fila in tabla_pie.rows:
            for celda in fila.cells:
                for p in celda.paragraphs:
                    for r in list(p.runs):
                        r._r.getparent().remove(r._r)
    # El paquete conserva encabezados de secciones eliminadas (header1 a
    # header3). Se elevan todos, no solo el de la sección activa, para que
    # ninguna parte del DOCX conserve 8.5 pt y el PDF no muestre fuentes
    # menores a 9.5 pt.
    for relacion in doc.part.rels.values():
        if not relacion.reltype.endswith("/header"):
            continue
        raiz_hdr = relacion.target_part.element
        for etiqueta in ("w:sz", "w:szCs"):
            for sz in raiz_hdr.iter(qn(etiqueta)):
                try:
                    if int(sz.get(qn("w:val"))) < 19:
                        sz.set(qn("w:val"), "19")
                except (TypeError, ValueError):
                    pass

    configurar_estilos(doc)
    return doc


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

    # docDefaults: evita que Word reintroduzca Calibri o 11 pt.
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
            tam = rpr_def.find(qn("w:sz"))
            if tam is None:
                tam = OxmlElement("w:sz")
                rpr_def.append(tam)
            tam.set(qn("w:val"), str(SP))
            tam_cs = rpr_def.find(qn("w:szCs"))
            if tam_cs is None:
                tam_cs = OxmlElement("w:szCs")
                rpr_def.append(tam_cs)
            tam_cs.set(qn("w:val"), str(SP))
            idioma = rpr_def.find(qn("w:lang"))
            if idioma is None:
                idioma = OxmlElement("w:lang")
                rpr_def.append(idioma)
            idioma.set(qn("w:val"), "es-PE")
            idioma.set(qn("w:eastAsia"), "es-PE")


# ---------------------------------------------------------------------------
# Documento 00. Protocolo de campo
# ---------------------------------------------------------------------------

def _texto_protocolo(doc) -> None:
    titulo(doc, "Protocolo de campo de los Instrumentos 1 y 2")
    subtitulo(doc, "Sistema SIVAC, versión v03", before=0, after=6)

    h2(doc, "1. Objetivo", before=2)
    par(doc, "Regula la aplicación de la Ficha de tiempos (Instrumento 1) y de "
             "la Ficha de auditoría documental (Instrumento 2), destinadas a "
             "medir la Variable Dependiente “Gestión de movimientos mensuales "
             "de vacunas” (DEC-027) en la DISA Apurímac II. El Instrumento 3 se "
             "rige por su propio instructivo.", align="both")

    h2(doc, "2. Diseño, población y códigos")
    par(doc, "Diseño preexperimental de un solo grupo, con pretest y postest "
             "(O1 → X → O2). Población censal: N = n = 14 trabajadores de "
             "inmunizaciones en 13 centros de acopio.", align="both")
    item(doc, "•", "Fases: “Antes de SIVAC (pretest)” y “Con SIVAC (postest)”, "
                   "con los mismos escenarios y la misma carga fija.")
    item(doc, "•", "Códigos: participantes P01 a P14; centros C01 a C13.")
    item(doc, "•", "La lista maestra que vincula códigos y nombres la custodia "
                   "el investigador, separada de las fichas.")

    h2(doc, "3. Dimensiones e indicadores")
    item(doc, "1.", "Oportunidad de procesamiento: T_reg (tiempo de registro "
                    "de movimientos) y T_vale (tiempo de emisión del vale), en "
                    "minutos decimales.")
    item(doc, "2.", "Consistencia documental: RSD (documentos sin discrepancias) "
                    "y CPE (despachos concordantes), en porcentaje.")
    item(doc, "3.", "Satisfacción del usuario: AP (aceptación del proceso) y UP "
                    "(utilidad percibida), en puntos.")
    par(doc, "Cada dimensión se mide con su propio instrumento y ningún "
             "indicador se sustituye ni se estima a partir de otro.",
        align="both", before=2)

    h2(doc, "4. Tareas cronometradas, carga fija y disparadores")
    par(doc, "Se cronometran seis tareas: tres de registro (REG-01, REG-02 y "
             "REG-03) y tres de emisión de vale (VALE-01, VALE-02 y VALE-03). "
             "Cada tarea se ejecuta una vez por fase y produce una observación "
             "destinada a su indicador.", align="both")
    filas = [
        ["Código", "Escenario", "Carga fija", "Inicio", "Fin"],
        ["REG-01", "Ingreso de lote", "1 biológico, 1 lote, 20 frascos",
         "Recibe el lote y abre el kardex o el formulario",
         "Cierra y firma el asiento, o confirma el guardado"],
        ["REG-02", "Salida o transferencia a microred",
         "3 biológicos, 3 lotes, 30 frascos (10 por biológico)",
         "Recibe la orden de salida y abre el registro",
         "Cierra y firma el asiento, o confirma el guardado"],
        ["REG-03", "Redistribución entre centros de acopio",
         "2 biológicos, 2 lotes, 20 frascos (10 por biológico)",
         "Recibe la orden de redistribución y abre el registro",
         "Cierra y firma el asiento, o confirma el guardado"],
        ["VALE-01", "Vale de salida regular", "3 biológicos, 30 frascos",
         "Recibe la solicitud de despacho",
         "Genera y confirma el vale impreso o digital"],
        ["VALE-02", "Vale de reposición urgente por contingencia de cadena de frío",
         "1 biológico, 10 frascos", "Recibe la solicitud urgente",
         "Genera y confirma el vale impreso o digital"],
        ["VALE-03", "Vale de transferencia entre centros de acopio",
         "2 biológicos, 20 frascos", "Recibe la solicitud de transferencia",
         "Genera y confirma el vale impreso o digital"],
    ]
    tabla(doc, filas, [1.7, 4.3, 3.5, 3.0, 3.0], apa=True)
    nota(doc, "La carga es fija. Si la carga real difiere en el número de "
              "biológicos, de lotes o de frascos, la tarea no es válida.")

    h2(doc, "5. Repeticiones de tareas no válidas")
    par(doc, "Una tarea se anula si no se completó, si la carga real no fue la "
             "fijada o si medió una interrupción no registrada. La repetición se "
             "asienta en el registro de repeticiones de la página 2 de la Ficha "
             "1, con el mismo código de escenario y el motivo.", align="both")
    par(doc, "De cada escenario se conserva el primer tiempo válido. Las "
             "repeticiones posteriores no se promedian, no se suman y no "
             "sustituyen a un tiempo ya válido.", align="both")

    h2(doc, "6. Duración, pausa y validez")
    item(doc, "•", "Duración: minutos decimales, calculada como fin menos inicio.")
    item(doc, "•", "Pausa: interrupción no atribuible al procedimiento (atención "
                   "a terceros, corte de energía o fuerza mayor). Se anota en "
                   "minutos y se resta.")
    item(doc, "•", "Tiempo válido: duración menos pausa, con dos cifras decimales.")
    item(doc, "•", "Una interrupción atribuible al procedimiento no se resta; si "
                   "impide completar la tarea, la anula.")
    item(doc, "•", "Una tarea con tiempo válido igual o menor que cero se anula "
                   "y se repite.")

    h2(doc, "7. Criterios de conformidad documental (RSD)")
    par(doc, "Un documento es conforme solo si los ocho criterios están en Sí.",
        align="both")
    criterios = [
        "Biológico: nombre y presentación coinciden con el producto físico y "
        "el documento de origen.",
        "Lote: el número asentado es idéntico al rotulado y al del documento "
        "de origen.",
        "Vencimiento: mes y año coinciden con el rotulado.",
        "Cantidad: dosis o frascos coinciden con el conteo físico.",
        "Centro: código y denominación del establecimiento coinciden con el "
        "documento que autoriza.",
        "Responsable: nombre, cargo y firma o sello de quien entrega y de quien "
        "recibe, legibles.",
        "Saldo: saldo final = saldo inicial + ingresos − salidas, sin diferencia.",
        "Correlatividad: fecha y hora del asiento son coherentes con el "
        "documento que autoriza y con el asiento previo.",
    ]
    for i, texto in enumerate(criterios, 1):
        item(doc, f"{i}.", texto)
    par(doc, "Un solo No hace no conforme el documento. El motivo se consigna "
             "como el primer criterio marcado No.", align="both", before=2)

    h2(doc, "8. Concordancia de despachos (CPE)")
    par(doc, "E es la cantidad entregada; P, la cantidad programada; "
             "D = E − P. El despacho es concordante solo si D = 0 y existe el "
             "documento que autoriza el despacho. Toda diferencia distinta de "
             "cero, por exceso o por defecto, es no concordante, y un despacho "
             "sin documento que autoriza también es no concordante aunque las "
             "cantidades coincidan. No existe diferencia autorizada ni "
             "compensación entre despachos. Si las unidades difieren, se "
             "convierten a dosis y se anota la equivalencia en Observación.",
        align="both")

    h2(doc, "9. Ventana documental y corpus")
    item(doc, "•", "La ventana documental es de 30 días calendario, común a "
                   "todas las fichas de auditoría de una misma fase.")
    item(doc, "•", "El corpus es de 40 a 60 entregas por ventana, distribuidas "
                   "entre los 14 participantes según los movimientos que cada "
                   "uno registró.")
    item(doc, "•", "La ficha de auditoría es por participante: el código P del "
                   "encabezado atribuye todas las filas de la hoja.")
    item(doc, "•", "La suma de las filas auditadas de los 14 participantes debe "
                   "situarse entre 40 y 60. El investigador verifica esta suma "
                   "antes de cerrar la fase.")
    item(doc, "•", "Si un participante no registró entregas en la ventana, su "
                   "CPE queda “no calculable” y no se imputa valor.")
    par(doc, "La página A audita los documentos que respaldan los movimientos "
             "de la misma ventana; la página B audita los despachos que "
             "integran el corpus.", align="both", before=2)

    h2(doc, "10. Fórmulas y unidades")
    formulas = [
        "T_reg = media aritmética de los tres tiempos válidos de REG-01, "
        "REG-02 y REG-03, en minutos decimales.",
        "T_vale = media aritmética de los tres tiempos válidos de VALE-01, "
        "VALE-02 y VALE-03, en minutos decimales.",
        "RSD = documentos conformes / documentos auditados × 100, en porcentaje.",
        "CPE = despachos concordantes / despachos auditados × 100, en porcentaje.",
        "AP = suma de AP-01 a AP-04, de 4 a 20 puntos.",
        "UP = suma de UP-01 a UP-04, de 4 a 20 puntos.",
    ]
    for texto in formulas:
        item(doc, "•", texto)
    par(doc, "Cada participante recibe un valor por indicador. No se agrega un "
             "valor por indicador a partir de participantes con datos faltantes.",
        align="both", before=2)

    h2(doc, "11. Reglas de incidencia")
    incidencias = [
        "Tarea no realizada: se anota “No realizada”, no se imputa tiempo y se "
        "reprograma. Si un escenario queda sin tiempo válido, el indicador se "
        "informa como sin dato.",
        "Documento faltante: si no se ubica el asiento, se anota “No ubicado” y "
        "no se cuenta como auditado; si falta un respaldo de un asiento "
        "existente, se marcan No los criterios que no puedan verificarse.",
        "Despacho sin documento que autoriza: se audita y es no concordante "
        "aunque las cantidades coincidan; se anota “sin documento”.",
        "Participante sin entregas en la ventana: CPE “no calculable”, sin "
        "imputación.",
        "Ningún campo se completa con valores supuestos, promedios ni copias.",
    ]
    for i, texto in enumerate(incidencias, 1):
        item(doc, f"{i}.", texto)

    h2(doc, "12. Orden de aplicación")
    orden = [
        "Consentimiento informado.",
        "Ficha de tiempos, durante la ejecución de las seis tareas.",
        "Ficha de auditoría, sobre la ventana documental de 30 días.",
        "Cuestionario de satisfacción, al cierre.",
    ]
    for i, texto in enumerate(orden, 1):
        item(doc, f"{i}.", texto)

    h2(doc, "13. Anonimato y uso académico")
    par(doc, "Las fichas no llevan nombres, documentos de identidad ni datos "
             "clínicos; solo emplean los códigos P y C. La lista maestra se "
             "guarda aparte y se destruye al terminar el informe. Los datos se "
             "usan solo para esta investigación.", align="both")


# ---------------------------------------------------------------------------
# Documento 01. Ficha de tiempos
# ---------------------------------------------------------------------------

ANCHOS_FICHA1 = [0.7, 4.6, 1.4, 1.4, 1.3, 1.1, 1.3, 1.2, 1.1, 1.4]

CABECERA_FICHA1 = [
    "N.°", "Escenario", "Inicio", "Fin", "Dur. (min)", "Pausa (min)",
    "Válido (min)", "¿Vál.?", "Carga", "Obs.",
]

ESCENARIOS_FICHA1 = [
    ("1", "REG-01. Ingreso de lote: 1 biológico, 1 lote, 20 frascos"),
    ("2", "REG-02. Salida o transferencia a microred: 3 biológicos, 3 lotes, "
          "30 frascos (10 por biológico)"),
    ("3", "REG-03. Redistribución entre centros de acopio: 2 biológicos, "
          "2 lotes, 20 frascos (10 por biológico)"),
    ("4", "VALE-01. Vale de salida regular: 3 biológicos, 30 frascos"),
    ("5", "VALE-02. Vale de reposición urgente por contingencia de cadena de "
          "frío: 1 biológico, 10 frascos"),
    ("6", "VALE-03. Vale de transferencia entre centros de acopio: 2 biológicos, "
          "20 frascos"),
]


def _tabla_identificacion_ficha1(doc):
    filas = [
        [{ "texto": "Fase", "negrita": True },
         "☐ Antes de SIVAC (pretest)      ☐ Con SIVAC (postest)"],
        [{"texto": "Participante", "negrita": True}, "P ____"],
        [{"texto": "Centro", "negrita": True}, "C ____"],
        [{"texto": "Fecha", "negrita": True}, "____ / ____ / ________"],
        [{"texto": "Observador", "negrita": True},
         "________________________________________________"],
        [{"texto": "Hora de inicio de sesión", "negrita": True},
         "____ : ____ : ____"],
        [{"texto": "Hora de fin de sesión", "negrita": True},
         "____ : ____ : ____"],
    ]
    tabla(doc, filas, [3.6, 11.9], header_rows=0, size=SP,
          margen_tb=8, alto_filas_cm=0.55)


def _tabla_registro_ficha1(doc, con_escenarios: bool = True):
    filas = [CABECERA_FICHA1]
    if con_escenarios:
        for num, escenario in ESCENARIOS_FICHA1:
            filas.append([num, escenario, "", "", "", "", "",
                          "☐ Sí ☐ No", "☐ Sí ☐ No", ""])
    else:
        for num in range(1, 7):
            filas.append([str(num), "", "", "", "", "", "",
                          "☐ Sí ☐ No", "☐ Sí ☐ No", ""])
    tabla(doc, filas, ANCHOS_FICHA1,
          align_defecto="center", header_align="center",
          margen_lr=MARGEN_LR, margen_tb=(18 if con_escenarios else 4),
          margen_lr_cabecera=28, linea_celda=0.9,
          alto_filas_cm=None if con_escenarios else 0.5)


def _texto_ficha_tiempos(doc) -> None:
    # ------------------------------- Página 1 -------------------------------
    titulo(doc, "Instrumento 1. Ficha de tiempos de los movimientos de vacunas")
    par(doc, "Dimensión 1. Oportunidad de procesamiento (T_reg, tiempo de "
             "registro, y T_vale, tiempo de emisión del vale).", size=SP,
        after=3)

    _tabla_identificacion_ficha1(doc)
    par(doc, "Centro: centro de acopio donde ocurre el movimiento observado. "
             "Participante: código P del trabajador observado. Cada fase se "
             "registra en una ficha distinta.", size=SP, before=2, after=3)

    h2(doc, "Instrucciones", before=3, after=1)
    item(doc, "1.", "Cronometre cada tarea desde su disparador de inicio hasta "
                    "su disparador de fin y anote las horas en hh:mm:ss.",
         size=SP_TABLA, after=0)
    item(doc, "2.", "Ejecute las seis tareas una sola vez: REG-01, REG-02 y "
                    "REG-03 para T_reg; VALE-01, VALE-02 y VALE-03 para "
                    "T_vale. No repita una tarea válida.", size=SP_TABLA,
         after=0)
    item(doc, "3.", "Verifique la carga antes de iniciar y marque Sí o No en "
                    "Carga verificada. La carga se verifica con el número de "
                    "biológicos y de frascos; solo en REG-01 a REG-03 se "
                    "verifica además el número de lotes. Si la carga real "
                    "difiere de la fija, la tarea es no válida.", size=SP_TABLA,
         after=0)
    item(doc, "4.", "Si hay pausa, anótela en minutos y réstela. Una "
                    "interrupción externa que no impide completar la tarea se "
                    "registra como pausa y se resta. Marque No en ¿Válida?, "
                    "explique el motivo en Observación y registre la repetición "
                    "en la página 2 solo si la tarea no se completa, si la carga "
                    "no es la fijada o si la interrupción impide terminarla.",
         size=SP_TABLA, after=2)

    _tabla_registro_ficha1(doc)
    nota(doc, "Duración (min) = fin − inicio. Tiempo válido (min) = duración − "
              "pausa. Use minutos decimales con dos cifras. Conversión: minutos "
              "= horas × 60 + minutos + segundos ÷ 60. Anote el resultado con "
              "dos decimales. La carga de cada escenario es fija y se verifica "
              "con Sí o No; no se transcriben biológicos ni lotes en esta "
              "tabla.", before=2, after=3)

    subtitulo(doc, "Observaciones (incidencias, tareas no válidas y motivos de "
                   "anulación)", after=1)
    for _ in range(3):
        par(doc, "__________________________________________________________"
                 "____________________", size=SP, after=0, line=1.15)
    par(doc, "Firma del observador: ______________   "
             "Nombre: ________________   "
             "Hora de cierre: ____ : ____", size=SP, before=3)

    # ------------------------------- Página 2 -------------------------------
    titulo_salto(doc, "Instrumento 1. Ficha de tiempos (continuación)", after=0)

    h2(doc, "Registro de repeticiones", before=0, after=1)
    par(doc, "Se completa solo con las tareas marcadas No en ¿Válida? de la "
             "página 1. Anote el mismo código de escenario y el motivo de la "
             "anulación. De cada escenario se conserva el primer tiempo válido; "
             "la repetición no se promedia con la observación original.",
        size=SP_TABLA, after=2, line=0.95)
    _tabla_registro_ficha1(doc, con_escenarios=False)

    h2(doc, "Escenarios, carga fija y disparadores", before=2, after=1)
    filas = [
        ["Código", "Escenario", "Carga fija", "Inicio", "Fin"],
        ["REG-01", "Ingreso de lote", "1 biológico, 1 lote, 20 frascos",
         "El participante recibe el lote y abre el kardex o el formulario de "
         "ingreso", "Cierra y firma el asiento, o confirma el guardado"],
        ["REG-02", "Salida o transferencia a microred",
         "3 biológicos, 3 lotes, 30 frascos (10 por biológico)",
         "Recibe la orden de salida y abre el registro",
         "Cierra y firma el asiento, o confirma el guardado"],
        ["REG-03", "Redistribución entre centros de acopio",
         "2 biológicos, 2 lotes, 20 frascos (10 por biológico)",
         "Recibe la orden de redistribución y abre el registro",
         "Cierra y firma el asiento, o confirma el guardado"],
        ["VALE-01", "Vale de salida regular", "3 biológicos, 30 frascos",
         "Recibe la solicitud de despacho",
         "Genera y confirma el vale impreso o digital"],
        ["VALE-02", "Vale de reposición urgente por contingencia de cadena de frío",
         "1 biológico, 10 frascos", "Recibe la solicitud urgente",
         "Genera y confirma el vale impreso o digital"],
        ["VALE-03", "Vale de transferencia entre centros de acopio",
         "2 biológicos, 20 frascos", "Recibe la solicitud de transferencia",
         "Genera y confirma el vale impreso o digital"],
    ]
    tabla(doc, filas, [1.6, 3.7, 3.3, 3.6, 3.3], margen_tb=2,
          margen_lr=28, linea_celda=0.9)

    h2(doc, "Campos", before=2, after=1)
    campos = [
        ("Inicio:", "hora del disparador de inicio, en hh:mm:ss."),
        ("Fin:", "hora del disparador de fin, en hh:mm:ss."),
        ("Duración:", "fin menos inicio, en minutos decimales con dos cifras. "
                      "Conversión: minutos = horas × 60 + minutos + segundos ÷ "
                      "60. Anote el resultado con dos decimales."),
        ("Pausa:", "minutos de interrupción no atribuible al procedimiento. "
                   "Se resta."),
        ("Tiempo válido:", "duración menos pausa, en minutos decimales con dos "
                           "cifras."),
        ("¿Válida?:", "Sí si la tarea se completó, la carga fue la fijada y el "
                      "tiempo válido es mayor que cero. No en caso contrario; un "
                      "tiempo válido igual o menor que cero anula la tarea."),
        ("Carga verificada:", "Sí si el número de biológicos y de frascos "
                              "coincide con la carga fija; en REG-01 a REG-03 se "
                              "verifica además el número de lotes. No en caso "
                              "contrario."),
        ("Observación:", "motivo de la anulación o incidencia ocurrida."),
    ]
    for etiqueta, texto in campos:
        item(doc, "•", f"**{etiqueta}** {texto}", size=SP_TABLA, after=0,
             line=1.0)

    h2(doc, "Pausa, validez y repetición", before=1, after=0)
    par(doc, "La pausa es una interrupción externa no atribuible al "
             "procedimiento: atención a una persona ajena, corte de energía, "
             "interrupción administrativa o fuerza mayor. Se anota en minutos y "
             "se resta. Una interrupción externa que no impide completar la "
             "tarea se registra como pausa y se resta; una interrupción "
             "atribuible al procedimiento no se resta.", size=SP_TABLA,
        align="both", after=1, line=1.0)
    par(doc, "La tarea se anula solo si no se completó, si la carga no fue la "
             "fijada o si la interrupción impide terminarla. Se repite en la "
             "misma sesión o en una visita de reemplazo y se asienta en el "
             "registro de repeticiones. Un tiempo válido igual o menor que cero "
             "anula la tarea y se repite. Si un escenario queda sin tiempo "
             "válido, el observador lo informa al investigador y no se imputa "
             "valor.", size=SP_TABLA, align="both", line=1.0)

    h2(doc, "Agregación", before=1, after=0)
    par(doc, "T_reg es la media aritmética de los tres tiempos válidos de "
             "REG-01, REG-02 y REG-03. T_vale es la media aritmética de los "
             "tres tiempos válidos de VALE-01, VALE-02 y VALE-03. De cada "
             "escenario se usa un solo tiempo: el primero válido.",
        size=SP_TABLA, align="both", line=1.0)


# ---------------------------------------------------------------------------
# Documento 02. Ficha de auditoría documental
# ---------------------------------------------------------------------------

ANCHOS_AUDITORIA_A = [5.5, 1.66, 1.66, 1.66, 1.66, 1.66, 1.66]
ANCHOS_AUDITORIA_B = [0.8, 1.7, 2.7, 1.4, 1.4, 1.4, 2.6, 1.4, 2.1]

CRITERIOS_RSD = [
    "Tipo de documento", "N.° o serie", "Fecha",
    "Biológico: nombre y presentación coinciden con el producto físico y el "
    "documento de origen",
    "Lote: el número asentado es idéntico al rotulado y al del documento de "
    "origen",
    "Vencimiento: mes y año coinciden con el rotulado",
    "Cantidad: dosis o frascos coinciden con el conteo físico",
    "Centro: código y denominación coinciden con el documento que autoriza",
    "Responsable: nombre, cargo y firma o sello de quien entrega y de quien "
    "recibe, legibles",
    "Saldo: el saldo final coincide con el saldo inicial más los ingresos "
    "menos las salidas, sin diferencia",
    "Correlatividad: fecha y hora son coherentes con el documento que autoriza "
    "y con el asiento previo",
    "¿Conforme?",
]


def _identificacion_auditoria(doc):
    filas = [
        [{"texto": "Fase", "negrita": True},
         "☐ Antes de SIVAC (pretest)      ☐ Con SIVAC (postest)",
         "", ""],
        [{"texto": "Participante", "negrita": True}, "P ____",
         {"texto": "Centro", "negrita": True}, "C ____"],
        [{"texto": "Fecha de auditoría", "negrita": True},
         "____ / ____ / ________", {"texto": "Hoja", "negrita": True},
         "N.° ____"],
        [{"texto": "Auditor", "negrita": True},
         "________________________________________________", "", ""],
        [{"texto": "Ventana auditada", "negrita": True},
         "desde ____ / ____ / ________ hasta ____ / ____ / ________", "", ""],
    ]
    merges = [(0, 1, 0, 3), (3, 1, 3, 3), (4, 1, 4, 3)]
    tabla(doc, filas, [3.3, 4.0, 3.4, 4.8], header_rows=0, size=SP,
          merges=merges, margen_tb=6, alto_filas_cm=0.48)


def _texto_ficha_auditoria(doc) -> None:
    # ------------------------------- Página A -------------------------------
    titulo(doc, "Instrumento 2. Ficha de auditoría documental")
    par(doc, "Dimensión 2. Consistencia documental (RSD y CPE)", size=SP,
        after=3)
    subtitulo(doc, "Página A. Documentos sin discrepancias (RSD)", after=3)

    _identificacion_auditoria(doc)
    par(doc, "Centro: centro de acopio donde se custodian los documentos "
             "auditados. Participante: código P del trabajador cuyos movimientos "
             "se auditan; este código atribuye todas las filas de la hoja. "
             "Ventana auditada: 30 días calendario, común a las fichas de la "
             "misma fase. Tipo de documento: kardex, vale de salida, PECOSA, "
             "acta de entrega y recepción u otro asiento de movimiento.",
        size=SP, before=3, after=4)

    h2(doc, "Instrucciones", before=2, after=1)
    item(doc, "1.", "Audite solo asientos de movimiento de vacunas (ingresos, "
                    "salidas y transferencias). No audite tarjetas de vacunación "
                    "ni documentos clínicos.", after=0)
    item(doc, "2.", "Una columna por documento. Escriba Sí o No en cada uno de "
                    "los ocho criterios. El documento es conforme solo si los "
                    "ocho criterios están en Sí.", after=0)
    item(doc, "3.", "Complete las tres filas de identificación de cada documento "
                    "antes de calificar los criterios.", after=0)
    item(doc, "4.", "Si hay más de seis documentos, abra otra hoja A y continúe "
                    "la numeración: la segunda hoja se rotula del 7 al 12, y así "
                    "sucesivamente.", after=2)

    par(doc, "**Instrucción visible en la matriz:** Escriba Sí o No. El "
             "documento es conforme solo si los ocho criterios están en Sí.",
        size=SP, after=1)

    filas = [["Criterio", "Doc. 1", "Doc. 2", "Doc. 3",
              "Doc. 4", "Doc. 5", "Doc. 6"]]
    for criterio in CRITERIOS_RSD:
        filas.append([criterio, "", "", "", "", "", ""])
    tabla(doc, filas, ANCHOS_AUDITORIA_A, header_align="center",
          align_defecto="left", margen_tb=6, margen_lr_cabecera=28)

    nota(doc, "Un solo No hace no conforme el documento. El motivo se anota "
              "como el primer criterio marcado No.", before=2, after=2)

    tabla(doc, [["Documentos auditados", "Documentos conformes", "RSD (%)"],
                ["____", "____", "____"]],
          [5.7, 5.4, 4.4], header_align="center", align_defecto="center",
          margen_tb=8, size=SP)
    par(doc, "Documentos no ubicados (no se cuentan como auditados): ____. "
             "Otras incidencias: ____________________________________________."
        , size=SP, before=2, after=1)
    par(doc, "El auditor solo cuenta. El porcentaje final lo calcula el "
             "investigador.", size=SP)

    # ------------------------------- Página B -------------------------------
    titulo_salto(doc, "Instrumento 2. Ficha de auditoría documental "
                      "(continuación)", after=2)
    subtitulo(doc, "Página B. Despachos y concordancia programada frente a "
                   "entregada (CPE)", after=3)

    _identificacion_auditoria(doc)

    h2(doc, "Instrucciones", before=2, after=1)
    item(doc, "1.", "Una fila por despacho. El código P del encabezado atribuye "
                    "todas las filas de la hoja.", size=SP_TABLA, after=0)
    item(doc, "2.", "Anote P y E en la misma unidad del documento que autoriza "
                    "(dosis o frascos). Si difieren, convierta a dosis y anote "
                    "la equivalencia en Observación.", size=SP_TABLA, after=0)
    item(doc, "3.", "D = E − P. El despacho es concordante solo si D = 0 y "
                    "existe el documento que autoriza. Toda diferencia distinta "
                    "de cero, por exceso o por defecto, es no concordante; un "
                    "despacho sin documento que autoriza es no concordante "
                    "aunque las cantidades coincidan. No existe diferencia "
                    "autorizada ni compensación entre despachos.", size=SP_TABLA,
         after=0)
    item(doc, "4.", "Si hay más de quince despachos, abra otra hoja B y continúe "
                    "la numeración.", size=SP_TABLA, after=0)
    item(doc, "5.", "La suma de las filas auditadas de los 14 participantes debe "
                    "situarse entre 40 y 60 por ventana; el investigador "
                    "verifica esa suma antes de cerrar la fase.", size=SP_TABLA,
         after=0)

    h2(doc, "Definiciones", before=1, after=1)
    definiciones = [
        ("Fecha:", "fecha del despacho."),
        ("Establecimiento destino:", "código y denominación del establecimiento "
                                     "que recibe el despacho."),
        ("P:", "cantidad programada en la orden oficial."),
        ("E:", "cantidad física entregada."),
        ("D:", "diferencia E − P."),
        ("Documento que autoriza:", "tipo y número de la orden, solicitud o "
                                    "vale que respalda el despacho. Si no "
                                    "existe, anote “sin documento”."),
        ("¿Concordante?:", "Sí solo si D = 0 y existe el documento que autoriza; "
                           "No en cualquier otro caso."),
        ("Observación:", "motivo de no concordancia, equivalencia de unidades o "
                         "incidencia."),
    ]
    for etiqueta, texto in definiciones:
        item(doc, "•", f"**{etiqueta}** {texto}", size=SP_TABLA, after=0)

    filas = [["N.°", "Fecha", "Establecimiento destino",
              "Cant. prog. (P)", "Cant. entr. (E)",
              "Dif. (E − P)", "Documento que autoriza", "¿Conc.?",
              "Observación"]]
    for num in range(1, 16):
        filas.append([str(num), "", "", "", "", "", "",
                      "☐Sí☐No", ""])
    tabla(doc, filas, ANCHOS_AUDITORIA_B, header_align="center",
          align_defecto="center", margen_tb=4, margen_lr=28,
          margen_lr_cabecera=28, alto_filas_cm=0.42, size=SP_TABLA)

    tabla(doc, [["Despachos auditados", "Despachos concordantes", "CPE (%)"],
                ["____", "____", "____"]],
          [5.7, 5.4, 4.4], header_align="center", align_defecto="center",
          margen_tb=8, size=SP)
    par(doc, "Si el participante no registró entregas en la ventana, anote "
             "“no calculable” en CPE y no impute valor.", size=SP, before=2,
        after=1)
    par(doc, "El auditor solo cuenta. El porcentaje final lo calcula el "
             "investigador.", size=SP, after=2)
    par(doc, "Firma del auditor: ______________   "
             "Nombre: ________________   "
             "Fecha: ____ / ____ / ________", size=SP, before=2)


# ---------------------------------------------------------------------------
# Documento 03. Cuestionario AP/UP
# ---------------------------------------------------------------------------

ITEMS_AP_UP = [
    ("AP", "Aceptación del proceso (AP)", [
        ("AP-01", "El procedimiento actual para asentar los movimientos diarios "
                  "y cierres de mes es ágil y no demanda un esfuerzo mental o "
                  "físico excesivo."),
        ("AP-02", "El flujo de trabajo requerido para emitir comprobantes de "
                  "salida y vales de entrega es fluido y está libre de demoras "
                  "o trabas burocráticas."),
        ("AP-03", "El método empleado me permite conciliar los saldos de "
                  "inventario con las microredes generando tranquilidad y "
                  "reduciendo el estrés laboral."),
        ("AP-04", "El tiempo que dedico al registro administrativo de vacunas es "
                  "equilibrado y me deja disponibilidad para mis labores "
                  "sanitarias y asistenciales."),
    ]),
    ("UP", "Utilidad percibida (UP)", [
        ("UP-01", "El mecanismo de registro utilizado me permite disponer de "
                  "información fidedigna y en tiempo real del stock de vacunas "
                  "y jeringas."),
        ("UP-02", "El control de números de lote y fechas de vencimiento que "
                  "brinda el proceso previene oportunamente mermas o pérdidas "
                  "de biológicos."),
        ("UP-03", "La metodología de gestión facilita la detección inmediata y "
                  "rectificación de cualquier descuadre de inventario físico "
                  "versus registrado."),
        ("UP-04", "En general, considero que el procedimiento empleado es una "
                  "herramienta altamente eficaz para garantizar el abastecimiento "
                  "oportuno de vacunas."),
    ]),
]


def _texto_cuestionario(doc) -> None:
    titulo(doc, "Instrumento 3. Cuestionario de satisfacción del usuario")
    par(doc, "Dimensión 3. Satisfacción del usuario. Indicadores: AP (Aceptación "
             "del proceso) y UP (Utilidad percibida).", size=SP, after=4)

    tabla(doc, [
        [{"texto": "Fase", "negrita": True},
         "☐ Antes de SIVAC (pretest)      ☐ Con SIVAC (postest)"],
        [{"texto": "Participante", "negrita": True}, "P ____"],
        [{"texto": "Centro", "negrita": True}, "C ____"],
        [{"texto": "Fecha", "negrita": True}, "____ / ____ / ________"],
    ], [3.4, 12.1], header_rows=0, size=SP, margen_tb=18)

    subtitulo(doc, "Instrucción de fase", before=5, after=1)
    par(doc, "Responda pensando en el proceso de registro que utiliza "
             "actualmente. En el pretest, ese proceso es el que usa antes de la "
             "implementación de SIVAC; en el postest, es el que usa con SIVAC.",
        size=SP, after=3)

    subtitulo(doc, "Instrucción de respuesta", before=2, after=1)
    par(doc, "Marque un solo número por ítem. 1 = Totalmente en desacuerdo; "
             "2 = En desacuerdo; 3 = Ni de acuerdo ni en desacuerdo; 4 = De "
             "acuerdo; 5 = Totalmente de acuerdo.", size=SP, after=3)

    filas = [["N.°", "Ítem", "1", "2", "3", "4", "5"]]
    for _, rotulo, items in ITEMS_AP_UP:
        filas.append(["", f"**{rotulo}**", "", "", "", "", ""])
        for codigo, enunciado in items:
            filas.append([codigo, enunciado, "", "", "", "", ""])
    tabla(doc, filas, [1.2, 10.1, 0.84, 0.84, 0.84, 0.84, 0.84],
          header_align="center", align_defecto="left", margen_tb=18,
          size=SP_TABLA)

    par(doc, "Gracias por su participación. Sus respuestas son confidenciales y "
             "se utilizarán únicamente para esta investigación.", size=SP,
        before=5, after=4)
    subtitulo(doc, "Observaciones del participante", after=2)
    for _ in range(3):
        par(doc, "__________________________________________________________"
                 "____________________", size=SP, line=1.4)


# ---------------------------------------------------------------------------
# Documento 04. Consentimiento informado
# ---------------------------------------------------------------------------

def _texto_consentimiento(doc) -> None:
    L = 1.5
    titulo(doc, "Consentimiento informado para participar en la investigación")
    tabla(doc, [
        [{"texto": "Título de la investigación", "negrita": True},
         "Aplicación del sistema “SIVAC” para mejorar la gestión de movimientos "
         "mensuales de vacunas en el personal de inmunizaciones de la Dirección "
         "de Salud Apurímac II"],
        [{"texto": "Tesista", "negrita": True}, "Bach. José Luis Quispe León"],
        [{"texto": "Asesora", "negrita": True},
         "Dra. Norma Lorena Catacora Flores"],
        [{"texto": "Escuela profesional", "negrita": True},
         "Ingeniería de Sistemas, Universidad Nacional José María Arguedas"],
    ], [4.6, 10.9], header_rows=0, size=SP, margen_tb=18)

    par(doc, "Estimado(a) participante:", size=SP, before=5, after=1, line=L)

    bloques = [
        ("1. Propósito.", "Evaluar el efecto del sistema SIVAC en la gestión de "
                          "los movimientos mensuales de vacunas en el personal "
                          "de inmunizaciones de la Dirección de Salud Apurímac "
                          "II."),
        ("2. Procedimiento.", "Se le observará en seis tareas cronometradas, se "
                              "revisarán los documentos de movimiento y se le "
                              "aplicará un cuestionario de ocho ítems. Dos "
                              "momentos, antes y con SIVAC; aproximadamente 30 a "
                              "40 minutos por momento."),
        ("3. Riesgos.", "No implica riesgos distintos de sus actividades "
                        "habituales. No se tomarán muestras biológicas ni datos "
                        "clínicos."),
        ("4. Beneficios.", "Contribuirá a mejorar el registro y control de "
                           "vacunas. No hay pago ni compensación económica."),
        ("5. Confidencialidad.", "Los formularios usan los códigos P01 a P14 y "
                                 "C01 a C13, sin nombres. La lista que vincula "
                                 "códigos y nombres queda en poder del "
                                 "investigador. Los datos se usan solo para esta "
                                 "tesis y se destruyen al concluir el informe."),
        ("6. Voluntariedad.", "La participación es libre. Puede retirarse en "
                              "cualquier momento, sin perjuicio."),
        ("7. Contacto.", "Para consultas, comuníquese con el investigador."),
    ]
    for etiqueta, texto in bloques:
        par(doc, f"**{etiqueta}** {texto}", size=SP, align="both", after=0,
            line=L)

    par(doc, "Correo electrónico: ____________________________________",
        size=SP, before=1, line=L)
    par(doc, "Teléfono: ____________________________________", size=SP,
        after=2, line=L)

    par(doc, "**8. Declaración de consentimiento.** He leído y comprendido la "
             "información. Mis preguntas fueron respondidas. Acepto participar "
             "voluntariamente.", size=SP, align="both", before=2, after=4,
        line=L)

    tabla(doc, [
        [{"texto": "Participante", "negrita": True, "alineacion": "center"},
         {"texto": "Investigador", "negrita": True, "alineacion": "center"}],
        ["Nombre: ____________________________________",
         "Nombre: José Luis Quispe León"],
        ["Firma: ____________________________________",
         "Firma: ____________________________________"],
        ["Fecha: ____ / ____ / ________", "Fecha: ____ / ____ / ________"],
    ], [7.75, 7.75], header_align="center", align_defecto="left",
        margen_tb=22, size=SP)

    par(doc, "Este documento se emite por duplicado: una copia para el "
             "participante y otra para el investigador.", size=SP, before=6,
        line=L)


# ---------------------------------------------------------------------------
# Documento 05. Hoja de control de aplicación
# ---------------------------------------------------------------------------

ANCHOS_CONTROL = [0.9, 1.0, 1.6, 1.2, 1.2, 2.3, 2.4, 1.4, 3.5]
CABECERA_CONTROL = [
    "P", "Centro", "Fecha", "REG (0 a 3)", "VALE (0 a 3)",
    "Documentos (auditados / conformes)",
    "Despachos (auditados / concordantes)", "AP/UP (Sí / No)", "Observaciones",
]


def _tabla_control(doc):
    filas = [CABECERA_CONTROL]
    for i in range(1, 15):
        filas.append([f"P{i:02d}", "", "", "", "", "", "", "", ""])
    tabla(doc, filas, ANCHOS_CONTROL, header_align="center",
          align_defecto="center", margen_tb=16, size=SP_TABLA)


def _texto_control(doc) -> None:
    titulo(doc, "Hoja de control de aplicación")
    par(doc, "Documento interno del investigador. No se entrega al participante "
             "ni se archiva con las fichas anónimas.", size=SP, after=4)

    h2(doc, "Instrucciones", before=3)
    instrucciones = [
        "Complete una tabla por fase: pretest (antes de SIVAC) y postest (con "
        "SIVAC).",
        "Anote 3/3 en REG cuando REG-01, REG-02 y REG-03 tengan tiempo válido, "
        "y 3/3 en VALE cuando VALE-01, VALE-02 y VALE-03 lo tengan. Si falta "
        "alguna tarea, anote el número efectivo (0/3, 1/3 o 2/3).",
        "Anote en cada celda el par auditados / conformes (o auditados / "
        "concordantes); el numerador alimenta RSD o CPE y el denominador debe "
        "ser mayor que cero.",
        "El corpus de 40 a 60 de DEC-021 corresponde a las entregas o despachos "
        "que alimentan la CPE; no se aplica a los documentos de la RSD.",
        "No impute valores, promedios ni datos supuestos. Deje la celda en "
        "blanco cuando el dato no se haya obtenido.",
        "Si un participante no tiene entregas en la ventana auditada, escriba "
        "“no calculable” en la celda del par de despachos. Si no tiene "
        "documentos de movimiento, escriba “no calculable” en la celda del par "
        "de documentos. Al transcribir a la base de datos, “no calculable” se "
        "registra como celda vacía, conforme al diccionario de datos.",
        "Marque AP/UP con Sí cuando el cuestionario de ocho ítems esté completo "
        "y con No cuando no lo esté.",
        "Registre en Observaciones toda incidencia: tarea no realizada, "
        "documento no ubicado, despacho sin documento que autoriza, retiro del "
        "participante o repetición de una medición.",
        "No anote nombres ni documentos de identidad. Use solo los códigos P01 "
        "a P14 y C01 a C13.",
    ]
    for i, texto in enumerate(instrucciones, 1):
        item(doc, f"{i}.", texto, after=0)

    h2(doc, "Pretest. Antes de SIVAC (O1)", before=6)
    _tabla_control(doc)

    salto_pagina(doc)
    h2(doc, "Postest. Con SIVAC (O2)", before=0)
    _tabla_control(doc)

    h2(doc, "Resumen de la aplicación", before=10)
    tabla(doc, [
        ["Indicador", "Pretest", "Postest", "Verificación"],
        ["Total de participantes", "", "", "14"],
        ["Total de documentos auditados (sin mínimo ni máximo fijado)", "",
         "", "Sin mínimo ni máximo fijado"],
        ["Total de despachos auditados", "", "", "Entre 40 y 60"],
        ["Incidencias", "", "", "Número y motivo"],
    ], [5.9, 3.2, 3.2, 3.2], header_align="center",
        align_defecto="left", margen_tb=18, size=SP)

    par(doc, "El corpus de 40 a 60 de DEC-021 corresponde a las entregas o "
             "despachos de la CPE; no se aplica a los documentos de la RSD.",
        size=SP, before=5)


# ---------------------------------------------------------------------------
# Certificado de validación de la variable dependiente
# ---------------------------------------------------------------------------

CERT_ITEMS: List[Tuple[str, str]] = [
    ("D1", "Dimensión 1. Oportunidad de procesamiento (ítems 1 a 4)"),
    ("1", "El tiempo de registro de los movimientos mensuales de vacunas "
          "(T_reg), expresado en minutos, corresponde a la oportunidad de "
          "procesamiento."),
    ("2", "El tiempo de emisión del comprobante de salida o vale (T_vale), "
          "expresado en minutos, corresponde a la oportunidad de procesamiento."),
    ("3", "La reducción de T_reg y de T_vale entre el pretest y el postest "
          "expresa una mejora de la oportunidad de procesamiento."),
    ("4", "La oportunidad de procesamiento se valora con los tiempos que "
          "registra el personal de inmunizaciones en sus movimientos mensuales "
          "de vacunas."),
    ("D2", "Dimensión 2. Consistencia documental (ítems 5 a 8)"),
    ("5", "El porcentaje de registros sin discrepancias (RSD) corresponde a la "
          "consistencia documental de los movimientos mensuales de vacunas."),
    ("6", "La concordancia entre la cantidad programada y la cantidad entregada "
          "(CPE) corresponde a la consistencia documental."),
    ("7", "El aumento de RSD y de CPE entre el pretest y el postest expresa una "
          "mejora de la consistencia documental."),
    ("8", "La consistencia documental se valora con los registros y documentos "
          "de movimiento de vacunas del personal de inmunizaciones."),
    ("D3", "Dimensión 3. Satisfacción del usuario (ítems 9 a 16)"),
    ("9", "El procedimiento actual para asentar los movimientos diarios y "
          "cierres de mes es ágil y no demanda un esfuerzo mental o físico "
          "excesivo."),
    ("10", "El flujo de trabajo requerido para emitir comprobantes de salida y "
           "vales de entrega es fluido y está libre de demoras o trabas "
           "burocráticas."),
    ("11", "El método empleado me permite conciliar los saldos de inventario con "
           "las microredes generando tranquilidad y reduciendo el estrés "
           "laboral."),
    ("12", "El tiempo que dedico al registro administrativo de vacunas es "
           "equilibrado y me deja disponibilidad para mis labores sanitarias y "
           "asistenciales."),
    ("13", "El mecanismo de registro utilizado me permite disponer de "
           "información fidedigna y en tiempo real del stock de vacunas y "
           "jeringas."),
    ("14", "El control de números de lote y fechas de vencimiento que brinda el "
           "proceso previene oportunamente mermas o pérdidas de biológicos."),
    ("15", "La metodología de gestión facilita la detección inmediata y "
           "rectificación de cualquier descuadre de inventario físico versus "
           "registrado."),
    ("16", "En general, considero que el procedimiento empleado es una "
           "herramienta altamente eficaz para garantizar el abastecimiento "
           "oportuno de vacunas."),
]


def _texto_certificado(doc) -> None:
    titulo(doc, "Certificado de validación de contenido de la variable "
                "dependiente")
    par(doc, "Variable dependiente: Gestión de movimientos mensuales de vacunas.",
        size=SP, after=3)
    par(doc, "Marque Sí o No en cada criterio. Puede añadir sugerencias en la "
             "última columna. El certificado es anónimo hasta el cierre.",
        size=SP, after=4)

    filas = [
        ["N.°", "DIMENSIONES / Ítems", "Pertinencia^{1}", "", "Relevancia^{2}",
         "", "Claridad^{3}", "", "Sugerencias"],
        ["", "", "Sí", "No", "Sí", "No", "Sí", "No", ""],
    ]
    for codigo, texto in CERT_ITEMS:
        if codigo.startswith("D"):
            filas.append(["", f"**{texto}**", "", "", "", "", "", "", ""])
        else:
            filas.append([codigo, texto, "", "", "", "", "", "", ""])

    merges = [
        (0, 0, 1, 0), (0, 1, 1, 1),
        (0, 2, 0, 3), (0, 4, 0, 5), (0, 6, 0, 7),
        (0, 8, 1, 8),
    ]
    tabla(doc, filas, [0.8, 6.0, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 3.3],
          header_rows=2, header_align="center", align_defecto="left",
          merges=merges, margen_tb=16, size=SP_TABLA)

    par(doc, "**Observaciones (precisar si hay suficiencia):**", size=SP,
        before=6, after=2)
    for _ in range(2):
        par(doc, "__________________________________________________________"
                 "____________________", size=SP, line=1.4)
    par(doc, "**Opinión de aplicabilidad:** ☐ Aplicable      "
             "☐ Aplicable después de corregir      "
             "☐ No aplicable", size=SP, before=5, after=3)
    par(doc, "**Apellidos y nombres del juez validador:** "
             "______________________________________________", size=SP, after=3)
    par(doc, "**DNI:** ____________________      **Especialidad del "
             "validador:** ______________________________", size=SP, after=3)
    par(doc, "**Fecha:** ____ de ____________________ del ________.      "
             "**Firma:** ______________________________", size=SP, after=6)

    subtitulo(doc, "Notas al pie", after=1)
    item(doc, "1.", "**Pertinencia:** el ítem corresponde al concepto teórico "
                    "formulado.", size=SP_TABLA, after=0)
    item(doc, "2.", "**Relevancia:** el ítem es apropiado para representar al "
                    "componente o dimensión específica del constructo.",
         size=SP_TABLA, after=0)
    item(doc, "3.", "**Claridad:** el enunciado del ítem se entiende sin "
                    "dificultad alguna; es conciso, exacto y directo.",
         size=SP_TABLA, after=0)


# ---------------------------------------------------------------------------
# Diccionario de datos
# ---------------------------------------------------------------------------

DICT_VARIABLES = [
    ("id_participante", "Código del participante", "Texto", "Código",
     "P01 a P14", "Hoja de control de aplicación",
     "Identifica al trabajador sin revelar su nombre."),
    ("centro", "Código del centro de acopio", "Texto", "Código", "C01 a C13",
     "Hoja de control de aplicación",
     "Identifica el centro donde se aplica el instrumento."),
    ("fase", "Momento de aplicación", "Entero", "Código",
     "1 = pretest; 2 = postest", "Hoja de control de aplicación",
     "Permite separar las dos mediciones del mismo participante."),
    ("fecha", "Fecha de aplicación", "Fecha", "AAAA-MM-DD",
     "Fecha calendario válida; vacía si no se aplicó", "Ficha 1 y Ficha 2",
     "No se completa si la medición no se realizó."),
    ("reg_01", "Tiempo de registro de REG-01", "Decimal", "Minutos",
     "Mayor o igual que 0; vacía si no se realizó", "Ficha 1 (tiempos)",
     "Tiempo válido de la tarea REG-01, ingreso de lote."),
    ("reg_02", "Tiempo de registro de REG-02", "Decimal", "Minutos",
     "Mayor o igual que 0; vacía si no se realizó", "Ficha 1 (tiempos)",
     "Tiempo válido de la tarea REG-02, salida o transferencia a microred."),
    ("reg_03", "Tiempo de registro de REG-03", "Decimal", "Minutos",
     "Mayor o igual que 0; vacía si no se realizó", "Ficha 1 (tiempos)",
     "Tiempo válido de la tarea REG-03, redistribución entre centros de acopio."),
    ("vale_01", "Tiempo de emisión de VALE-01", "Decimal", "Minutos",
     "Mayor o igual que 0; vacía si no se realizó", "Ficha 1 (tiempos)",
     "Tiempo válido de la tarea VALE-01, vale de salida regular."),
    ("vale_02", "Tiempo de emisión de VALE-02", "Decimal", "Minutos",
     "Mayor o igual que 0; vacía si no se realizó", "Ficha 1 (tiempos)",
     "Tiempo válido de la tarea VALE-02, reposición urgente por contingencia."),
    ("vale_03", "Tiempo de emisión de VALE-03", "Decimal", "Minutos",
     "Mayor o igual que 0; vacía si no se realizó", "Ficha 1 (tiempos)",
     "Tiempo válido de la tarea VALE-03, transferencia entre centros de acopio."),
    ("t_reg", "Tiempo medio de registro", "Decimal", "Minutos",
     "Mayor o igual que 0; vacía si falta alguna observación", "Derivada",
     "Requiere reg_01, reg_02 y reg_03."),
    ("t_vale", "Tiempo medio de emisión del vale", "Decimal", "Minutos",
     "Mayor o igual que 0; vacía si falta alguna observación", "Derivada",
     "Requiere vale_01, vale_02 y vale_03."),
    ("doc_auditados", "Documentos auditados", "Entero", "Conteo",
     "Mayor o igual que 0; vacía si no se auditó", "Ficha 2 (auditoría)",
     "No incluye documentos no ubicados."),
    ("doc_conformes", "Documentos conformes", "Entero", "Conteo",
     "De 0 a doc_auditados; vacía si no se auditó", "Ficha 2 (auditoría)",
     "Solo cuenta documentos con los ocho criterios en Sí."),
    ("rsd", "Registros sin discrepancias", "Decimal", "Porcentaje",
     "De 0 a 100; vacía si doc_auditados es 0", "Derivada",
     "Se informa como porcentaje."),
    ("desp_auditados", "Despachos auditados", "Entero", "Conteo",
     "Mayor o igual que 0; vacía si no se auditó", "Ficha 2 (auditoría)",
     "Incluye los despachos sin documento que autoriza, que se registran como "
     "no concordantes."),
    ("desp_concordantes", "Despachos concordantes", "Entero", "Conteo",
     "De 0 a desp_auditados; vacía si no se auditó", "Ficha 2 (auditoría)",
     "Solo cuenta despachos con diferencia igual a cero y documento que "
     "autoriza."),
    ("cpe", "Concordancia programada frente a entregada", "Decimal",
     "Porcentaje", "De 0 a 100; vacía si desp_auditados es 0", "Derivada",
     "Se informa como porcentaje."),
    ("ap_01", "Aceptación del proceso, reactivo 1", "Entero", "Likert 1 a 5",
     "1, 2, 3, 4 o 5; vacía si no se respondió", "Instrumento 3",
     "Enunciado literal AP-01 de DEC-019."),
    ("ap_02", "Aceptación del proceso, reactivo 2", "Entero", "Likert 1 a 5",
     "1, 2, 3, 4 o 5; vacía si no se respondió", "Instrumento 3",
     "Enunciado literal AP-02 de DEC-019."),
    ("ap_03", "Aceptación del proceso, reactivo 3", "Entero", "Likert 1 a 5",
     "1, 2, 3, 4 o 5; vacía si no se respondió", "Instrumento 3",
     "Enunciado literal AP-03 de DEC-019."),
    ("ap_04", "Aceptación del proceso, reactivo 4", "Entero", "Likert 1 a 5",
     "1, 2, 3, 4 o 5; vacía si no se respondió", "Instrumento 3",
     "Enunciado literal AP-04 de DEC-019."),
    ("up_01", "Utilidad percibida, reactivo 1", "Entero", "Likert 1 a 5",
     "1, 2, 3, 4 o 5; vacía si no se respondió", "Instrumento 3",
     "Enunciado literal UP-01 de DEC-019."),
    ("up_02", "Utilidad percibida, reactivo 2", "Entero", "Likert 1 a 5",
     "1, 2, 3, 4 o 5; vacía si no se respondió", "Instrumento 3",
     "Enunciado literal UP-02 de DEC-019."),
    ("up_03", "Utilidad percibida, reactivo 3", "Entero", "Likert 1 a 5",
     "1, 2, 3, 4 o 5; vacía si no se respondió", "Instrumento 3",
     "Enunciado literal UP-03 de DEC-019."),
    ("up_04", "Utilidad percibida, reactivo 4", "Entero", "Likert 1 a 5",
     "1, 2, 3, 4 o 5; vacía si no se respondió", "Instrumento 3",
     "Enunciado literal UP-04 de DEC-019."),
    ("ap", "Puntaje de aceptación del proceso", "Entero", "Puntos",
     "De 4 a 20; vacía si falta algún reactivo AP", "Derivada",
     "Suma de los cuatro reactivos AP."),
    ("up", "Puntaje de utilidad percibida", "Entero", "Puntos",
     "De 4 a 20; vacía si falta algún reactivo UP", "Derivada",
     "Suma de los cuatro reactivos UP."),
    ("observaciones", "Observaciones de la aplicación", "Texto", "Texto libre",
     "Texto; vacía si no hay incidencia", "Hoja de control de aplicación",
     "Registra incidencias, repeticiones y motivos de anulación."),
]


def _texto_diccionario(doc) -> None:
    titulo(doc, "Diccionario de datos de los instrumentos SIVAC")

    h2(doc, "1. Alcance", before=3)
    par(doc, "Este diccionario define la estructura tabular con la que se "
             "registran las respuestas de los tres instrumentos de recolección: "
             "la Ficha de tiempos, la Ficha de auditoría documental y el "
             "Cuestionario de satisfacción. Su finalidad es asegurar que la "
             "captura, la validación y el análisis posterior utilicen los mismos "
             "nombres, tipos y reglas de ausencia. El diccionario no contiene "
             "datos: todas las celdas de captura se emiten vacías.",
        align="both")

    h2(doc, "2. Reglas de codificación")
    reglas = [
        "Una celda vacía significa que el dato no se realizó o no es aplicable. "
        "No se usan 0 ni 99 como códigos de ausencia.",
        "No se imputan valores, promedios, valores de la fase opuesta ni datos "
        "supuestos.",
        "RSD y CPE solo se calculan cuando el denominador correspondiente es "
        "mayor que cero.",
        "AP y UP solo se calculan cuando los cuatro reactivos de la subescala "
        "están completos.",
        "El valor 0 solo se admite cuando la medición efectiva sea cero; el "
        "valor 99 no se admite en ninguna variable.",
        "Las fechas se registran en formato AAAA-MM-DD y los minutos en "
        "decimales con dos cifras.",
    ]
    for i, texto in enumerate(reglas, 1):
        item(doc, f"{i}.", texto)

    h2(doc, "3. Variables", before=7)
    filas = [["Variable", "Etiqueta", "Tipo", "Unidad o escala",
              "Valores admitidos", "Fuente", "Observaciones"]]
    for fila in DICT_VARIABLES:
        filas.append(list(fila))
    tabla(doc, filas, [2.3, 2.4, 1.1, 1.7, 3.0, 2.5, 2.5], apa=True,
          align_defecto="left", margen_tb=14)

    h2(doc, "4. Fórmulas", before=8)
    par(doc, "Las fórmulas se expresan con texto y no con objetos OMML. Se "
             "ubican fuera de la tabla para no alterar su estructura.",
        align="both", after=2)
    formulas = [
        "T_reg = (reg_01 + reg_02 + reg_03) / 3.",
        "T_vale = (vale_01 + vale_02 + vale_03) / 3.",
        "RSD = doc_conformes / doc_auditados × 100.",
        "CPE = desp_concordantes / desp_auditados × 100.",
        "AP = ap_01 + ap_02 + ap_03 + ap_04.",
        "UP = up_01 + up_02 + up_03 + up_04.",
    ]
    for texto in formulas:
        item(doc, "•", texto)

    h2(doc, "5. Control de calidad")
    controles = [
        "Que las tres observaciones de cada indicador existan cuando se reporte "
        "T_reg o T_vale; si falta una, el promedio no se calcula.",
        "Que el denominador de RSD y de CPE sea mayor que cero antes de "
        "calcular el porcentaje.",
        "Que los valores Likert de ap_01 a ap_04 y de up_01 a up_04 estén entre "
        "1 y 5.",
        "Que no haya celdas con 0 o 99 usadas como código de ausencia.",
        "Que doc_conformes no exceda doc_auditados y que desp_concordantes no "
        "exceda desp_auditados.",
        "Que id_participante pertenezca al rango P01 a P14 y centro al rango "
        "C01 a C13.",
        "Que cada participante tenga como máximo un registro por fase.",
    ]
    for i, texto in enumerate(controles, 1):
        item(doc, f"{i}.", texto)


# ---------------------------------------------------------------------------
# Ensamblado y exportación
# ---------------------------------------------------------------------------

DOCUMENTOS = [
    ("00_PROTOCOLO_DE_CAMPO_v03", _texto_protocolo,
     "Protocolo de campo de los Instrumentos 1 y 2"),
    ("01_FICHA_TIEMPOS_v03", _texto_ficha_tiempos,
     "Instrumento 1. Ficha de tiempos"),
    ("02_FICHA_AUDITORIA_v03", _texto_ficha_auditoria,
     "Instrumento 2. Ficha de auditoría documental"),
    ("03_CUESTIONARIO_AP_UP_v03", _texto_cuestionario,
     "Instrumento 3. Cuestionario de satisfacción del usuario"),
    ("04_CONSENTIMIENTO_INFORMADO_v03", _texto_consentimiento,
     "Consentimiento informado"),
    ("05_CONTROL_DE_APLICACION_v03", _texto_control,
     "Hoja de control de aplicación"),
    ("CERTIFICADO_VALIDACION_VD_v03", _texto_certificado,
     "Certificado de validación de contenido de la VD"),
    ("DICCIONARIO_DE_DATOS_v03", _texto_diccionario,
     "Diccionario de datos de los instrumentos SIVAC"),
]
MAESTRO = "00_INSTRUMENTOS_RECOLECCION_SIVAC_v03"


def _preparar_directorio() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    assets = SALIDA / "_assets"
    assets.mkdir(exist_ok=True)
    with zipfile.ZipFile(V02_DOCX) as zf:
        (assets / "LOGO-UNAJMA-recorte.png").write_bytes(
            zf.read("word/media/image1.png"))
        (assets / "LOGO-EPIS.jpg").write_bytes(zf.read("word/media/image2.jpg"))


def construir_individual(nombre: str, funcion, titulo_doc: str) -> Path:
    doc = nueva_plantilla()
    doc.core_properties.title = titulo_doc
    doc.core_properties.subject = "Instrumentos de recolección SIVAC v03"
    doc.core_properties.author = "SIVAC"
    funcion(doc)
    ruta = SALIDA / f"{nombre}.docx"
    if ruta.exists():
        raise FileExistsError(f"La versión ya existe y no se sobrescribe: {ruta}")
    doc.save(str(ruta))
    return ruta


def construir_maestro() -> Path:
    doc = nueva_plantilla()
    doc.core_properties.title = "Instrumentos de recolección SIVAC v03"
    doc.core_properties.subject = "Paquete completo de instrumentos"
    doc.core_properties.author = "SIVAC"
    for indice, (_, funcion, _) in enumerate(DOCUMENTOS):
        if indice:
            salto_pagina(doc)
        funcion(doc)
    ruta = SALIDA / f"{MAESTRO}.docx"
    if ruta.exists():
        raise FileExistsError(f"La versión ya existe y no se sobrescribe: {ruta}")
    doc.save(str(ruta))
    return ruta


def sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as fh:
        for bloque in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def inspeccionar_docx(ruta: Path) -> Dict[str, Any]:
    """Control de calidad OpenXML: fuentes, OMML, anchos y flotación."""
    import xml.etree.ElementTree as ET

    W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
    with zipfile.ZipFile(ruta) as zf:
        xml = zf.read("word/document.xml")
        encabezados = [n for n in zf.namelist()
                       if re.match(r"word/header\d+\.xml$", n)]
        xml_hdr = [zf.read(n) for n in encabezados]
    raiz = ET.fromstring(xml)

    tamanos = []
    for sz in raiz.iter(f"{{{W}}}sz"):
        try:
            tamanos.append(int(sz.get(f"{{{W}}}val")))
        except (TypeError, ValueError):
            continue
    tamanos_hdr = []
    for bloque in xml_hdr:
        try:
            raiz_h = ET.fromstring(bloque)
        except ET.ParseError:
            continue
        for sz in raiz_h.iter(f"{{{W}}}sz"):
            try:
                tamanos_hdr.append(int(sz.get(f"{{{W}}}val")))
            except (TypeError, ValueError):
                continue

    omml = sum(1 for _ in raiz.iter(f"{{{M}}}oMath"))
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

    return {
        "docx": str(ruta),
        "sha256": sha256(ruta),
        "bytes": ruta.stat().st_size,
        "fuente_minima_cuerpo_pt": min(tamanos) / 2 if tamanos else None,
        "fuente_minima_encabezado_pt": min(tamanos_hdr) / 2 if tamanos_hdr else None,
        "tamanos_pt": sorted({t / 2 for t in tamanos}),
        "omml": omml,
        "tablas_flotantes": flotantes,
        "tablas": len(anchos),
        "ancho_maximo_tabla_dxa": max(anchos) if anchos else None,
        "tablas_exceden_ancho_util": [a for a in anchos if a > ANCHO_DXA],
    }


def exportar(ruta_docx: Path) -> Dict[str, Any]:
    ruta_pdf = ruta_docx.with_suffix(".pdf")
    resultado = dq.exportar_docx_a_pdf(ruta_docx, ruta_pdf, actualizar_campos=True)
    return resultado


def renderizar(pdf: Path, paginas: Optional[Sequence[int]] = None) -> List[str]:
    import pymupdf

    documento = pymupdf.open(str(pdf))
    total = documento.page_count
    documento.close()
    if paginas is None:
        paginas = list(range(1, total + 1))
    destino = SALIDA / "_control_visual" / pdf.stem
    salida = dq.renderizar_paginas_pdf(pdf, paginas, dpi=120, salida_dir=destino)
    return salida["renderizadas"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sin-pdf", action="store_true",
                        help="Construye solo los DOCX")
    parser.add_argument("--solo", help="Compila únicamente el documento indicado")
    parser.add_argument("--maestro-solo", action="store_true",
                        help="Construye únicamente el maestro")
    args = parser.parse_args()

    _preparar_directorio()
    manifiesto: Dict[str, Any] = {
        "version": "v03",
        "generado": datetime.now().isoformat(timespec="seconds"),
        "especificaciones": str(SALIDA / "_ESPECIFICACION"),
        "referencia_geometria": str(V02_DOCX),
        "documentos": [],
        "advertencias": [],
    }

    pendientes = [d for d in DOCUMENTOS if not args.solo or d[0] == args.solo]
    if args.maestro_solo:
        pendientes = []

    for nombre, funcion, titulo_doc in pendientes:
        print(f"[docx] {nombre}", flush=True)
        ruta = construir_individual(nombre, funcion, titulo_doc)
        registro = inspeccionar_docx(ruta)
        registro["nombre"] = nombre
        if not args.sin_pdf:
            print(f"[pdf ] {nombre}", flush=True)
            pdf = exportar(ruta)
            registro["pdf"] = str(ruta.with_suffix(".pdf"))
            registro["sha256_pdf"] = sha256(ruta.with_suffix(".pdf"))
            registro["paginas"] = pdf["paginas"]
            registro["paginas_pdf_medidas"] = pdf.get("paginas")
        manifiesto["documentos"].append(registro)

    if not args.solo or args.maestro_solo:
        print(f"[docx] {MAESTRO}", flush=True)
        ruta = construir_maestro()
        registro = inspeccionar_docx(ruta)
        registro["nombre"] = MAESTRO
        if not args.sin_pdf:
            print(f"[pdf ] {MAESTRO}", flush=True)
            pdf = exportar(ruta)
            registro["pdf"] = str(ruta.with_suffix(".pdf"))
            registro["sha256_pdf"] = sha256(ruta.with_suffix(".pdf"))
            registro["paginas"] = pdf["paginas"]
        manifiesto["documentos"].append(registro)

    ruta_manifiesto = SALIDA / "MANIFIESTO_v03.json"
    if ruta_manifiesto.exists():
        previo = json.loads(ruta_manifiesto.read_text(encoding="utf-8"))
        # Conserva registros ya emitidos y actualiza los recompilados.
        por_nombre = {d["nombre"]: d for d in previo.get("documentos", [])}
        for d in manifiesto["documentos"]:
            por_nombre[d["nombre"]] = d
        manifiesto["documentos"] = list(por_nombre.values())
        manifiesto["advertencias"] = previo.get("advertencias", [])
    ruta_manifiesto.write_text(
        json.dumps(manifiesto, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(
        {d["nombre"]: d.get("paginas") for d in manifiesto["documentos"]},
        indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
