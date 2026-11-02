# -*- coding: utf-8 -*-
"""
Construye el libro de tablas de anexos SIVAC desde la v2 y lo versiona.

La ruta es parametrizable: el mismo script produce la v3 (por defecto) o la v4
con --salida. No recalcula ni reescribe cifras: toma la base, aplica el diseno
editorial y actualiza exclusivamente:

  1. La fuente documental (cualquier informe_final_vNN -> fuente vigente).
  2. La erradicacion de la referencia a la libreria interna de generacion.
  3. El doble punto y los avisos duplicados de datos provisionales.
  4. El rediseno editorial: portada, banda de control, cabeceras, bandas
     alternas, bordes APA 7 de tres lineas e impresion horizontal.
  5. Opcionalmente la Tabla 51 desde el DOCX (--actualizar-hu) y una hoja
     breve de validez reportada con formulas V/IVC (--hoja-validez).

Ningun valor numerico cambia. La paridad se verifica dos veces (contra la base
y contra el libro de referencia) y se reporta en JSON junto al SHA-256 real de
la fuente y de la salida.

Entradas (solo lectura):
  - salidas/estadistica/TABLAS_ANEXOS_SIVAC_v2.xlsx
  - salidas/documentos/informe_final_vNN.docx

Salidas:
  - --salida (por defecto TABLAS_ANEXOS_SIVAC_v3.xlsx)
  - paridad_<salida>.json

Ejemplos:
  .venv/Scripts/python.exe scripts/estadistica/build_tablas_anexos_v3.py \\
      --dry-run --fuente-docx informe_final_v16.docx \\
      --salida TABLAS_ANEXOS_SIVAC_v4.xlsx

  .venv/Scripts/python.exe scripts/estadistica/build_tablas_anexos_v3.py \\
      --fuente-docx informe_final_v17.docx \\
      --salida TABLAS_ANEXOS_SIVAC_v4.xlsx --actualizar-hu \\
      --hoja-validez --recalcular
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import math
import os
import re
from copy import copy
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.page import PageMargins
from openpyxl.worksheet.pagebreak import Break
from openpyxl.worksheet.properties import PageSetupProperties

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Rutas y constantes editoriales
# ---------------------------------------------------------------------------
ROOT = Path(r"C:\MisInvestigaciones\tesis\sivac")
DEFAULT_BASE = ROOT / "salidas" / "estadistica" / "TABLAS_ANEXOS_SIVAC_v2.xlsx"
DEFAULT_OUT = ROOT / "salidas" / "estadistica" / "TABLAS_ANEXOS_SIVAC_v3.xlsx"
DEFAULT_SOURCE = ROOT / "salidas" / "documentos" / "informe_final_v16.docx"
DEFAULT_REF = ROOT / "salidas" / "estadistica" / "TABLAS_ANEXOS_SIVAC_v3.xlsx"


def _resolve(value: str, base_dir: Path) -> Path:
    p = Path(value)
    return p if p.is_absolute() else base_dir / p


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Construye el libro de tablas de anexos SIVAC desde una base "
                    "y un DOCX fuente, con paridad numerica verificada.")
    parser.add_argument("--fuente-docx", default=str(DEFAULT_SOURCE),
                        help="DOCX fuente (ruta absoluta o nombre en salidas/documentos).")
    parser.add_argument("--base-xlsx", default=str(DEFAULT_BASE),
                        help="Libro base (por defecto la v2).")
    parser.add_argument("--salida", default=str(DEFAULT_OUT),
                        help="Libro de salida (por defecto la v3; para la v4 use "
                             "TABLAS_ANEXOS_SIVAC_v4.xlsx).")
    parser.add_argument("--referencia-paridad", default=str(DEFAULT_REF),
                        help="Libro de referencia para la paridad numerica (por "
                             "defecto la v3). Use 'ninguna' para omitir.")
    parser.add_argument("--reporte-paridad", default=None,
                        help="Ruta del JSON de paridad; por defecto "
                             "paridad_<salida>.json junto al libro.")
    parser.add_argument("--fecha", default=None,
                        help="Fecha de generacion AAAA-MM-DD (por defecto hoy).")
    parser.add_argument("--hoja-validez", action="store_true",
                        help="Anade 16_VALIDEZ_REPORTADA con formulas V/IVC.")
    parser.add_argument("--actualizar-hu", action="store_true",
                        help="Sincroniza la Tabla 51 desde el DOCX fuente (usar con la v17).")
    parser.add_argument("--correcciones-veracidad", default=None,
                        help="JSON del lote de veracidad para sincronizar rotulos y "
                             "notas de las Tablas 49 y 50 (caso datos de prueba).")
    parser.add_argument("--recalcular", action="store_true",
                        help="Recalcula la cache de formulas con una instancia aislada de Excel.")
    parser.add_argument("--force", action="store_true",
                        help="Sobrescribe la salida si ya existe.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Valida rutas, fuente y Tabla 51 sin escribir el libro.")
    return parser.parse_args(argv)


ARGS = parse_args()
IN_XLSX = _resolve(ARGS.base_xlsx, ROOT / "salidas" / "estadistica")
OUT_XLSX = _resolve(ARGS.salida, ROOT / "salidas" / "estadistica")
SOURCE_DOCX_PATH = _resolve(ARGS.fuente_docx, ROOT / "salidas" / "documentos")
TMP_XLSX = OUT_XLSX.with_suffix(".tmp.xlsx")

SOURCE_DOCX = SOURCE_DOCX_PATH.name
SOURCE_DOCX_STEM = SOURCE_DOCX_PATH.stem.replace("_", " ")
SOURCE_DOCX_BASE = SOURCE_DOCX_PATH.stem

FECHA_GENERACION = ARGS.fecha or datetime.date.today().isoformat()
_m = re.search(r"_v(\d+)$", OUT_XLSX.stem)
BOOK_VERSION_NUM = _m.group(1) if _m else "3"
BOOK_VERSION_DOTTED = f"{BOOK_VERSION_NUM}.0"
_ms = re.search(r"_v(\d+)$", SOURCE_DOCX_PATH.stem)
SOURCE_DOC_VERSION_NUM = _ms.group(1) if _ms else None

if ARGS.referencia_paridad and ARGS.referencia_paridad.lower() != "ninguna":
    REF_XLSX = _resolve(ARGS.referencia_paridad, ROOT / "salidas" / "estadistica")
else:
    REF_XLSX = None

if ARGS.hoja_validez and not ARGS.recalcular:
    raise SystemExit(
        "[ERROR] --hoja-validez requiere --recalcular: no se escriben formulas "
        "sin cache verificada.")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def contar_formulas(wb) -> int:
    return sum(1 for ws in wb.worksheets for row in ws.iter_rows()
               for cell in row if isinstance(cell.value, str)
               and cell.value.startswith("="))

NAVY = "1F3864"
BAND = "F2F5FA"          # bandas alternas de lectura
WHITE = "FFFFFF"
SOFT = "D9E2F3"          # subcabeceras y filas de total
RULE = "BFBFBF"          # lineas horizontales finas
INK = "1F2937"           # texto de cuerpo
MUTED = "4B5563"         # notas
FONT = "Arial"
MONO = "Consolas"

MARKER = ("Datos de prueba. Serán sustituidos por los registros "
          "definitivos de campo antes de la sustentación.")
LEGACY_MARKER = ("Datos provisionales. Serán sustituidos por los registros "
                 "definitivos de campo antes de la sustentación.")
RAYA_LARGA = chr(0x2014)

TAB_TABLE = "FF" + NAVY
TAB_SPSS = "FF" + SOFT

# ---------------------------------------------------------------------------
# Utilidades de estilo
# ---------------------------------------------------------------------------
def font(size=10, bold=False, italic=False, color=INK, name=FONT):
    return Font(name=name, size=size, bold=bold, italic=italic, color=color)


def fill(color):
    return PatternFill("solid", fgColor="FF" + color)


def side(style="thin", color=RULE):
    return Side(style=style, color="FF" + color)


def border(top=None, bottom=None):
    return Border(top=top or Side(), bottom=bottom or Side(),
                  left=Side(), right=Side())


def align(halign="left", valign="center", wrap=True):
    return Alignment(horizontal=halign, vertical=valign, wrap_text=wrap,
                     text_rotation=0, indent=0)


def paint(ws, r1, c1, r2, c2, *, f=None, bg=None, al=None, bd=None):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            cell = ws.cell(r, c)
            if f is not None:
                cell.font = f
            if bg is not None:
                cell.fill = bg
            if al is not None:
                cell.alignment = al
            if bd is not None:
                cell.border = bd


def est_lines(text, width, factor=0.80):
    if text is None:
        return 1
    chars = max(8, int(width * factor))
    total = 0
    for seg in str(text).split("\n"):
        total += max(1, math.ceil(len(seg) / chars))
    return total


AUTO_ROWS: dict[str, set[int]] = {}


def set_height(ws, row, height, manual=False):
    """Fija una altura de respaldo. Las filas de datos se registran como
    automaticas: al final se les retira el atributo customHeight del XML para
    que Excel pueda recalcularlas. Las filas combinadas conservan la altura
    manual porque Excel no autoajusta celdas combinadas."""
    rd = ws.row_dimensions[row]
    rd.height = min(409, max(8, height))
    if not manual:
        AUTO_ROWS.setdefault(ws.title, set()).add(row)


def auto_height(ws, row, widths, *, size=10, factor=0.80, minimum=16):
    lines = 1
    for j, w in enumerate(widths, 1):
        lines = max(lines, est_lines(ws.cell(row, j).value, w, factor))
    set_height(ws, row, lines * (size * 1.30) + 2, manual=False)


def head_style(ws, row, ncols, *, height=36):
    paint(ws, row, 1, row, ncols,
          f=font(10, bold=True, color=WHITE),
          bg=fill(NAVY),
          al=align("center", "center", True),
          bd=border(top=side("medium", NAVY), bottom=side("medium", NAVY)))
    set_height(ws, row, height, manual=False)


def data_style(ws, row, ncols, *, band=False, total=False, closing=False):
    bg = fill(SOFT) if total else (fill(BAND) if band else fill(WHITE))
    bd = border(bottom=side("medium", NAVY) if closing else side("thin", RULE))
    for c in range(1, ncols + 1):
        cell = ws.cell(row, c)
        horizontal = cell.alignment.horizontal or ("left" if c == 1 else "center")
        cell.font = font(10, bold=total, color=NAVY if total else INK)
        cell.fill = bg
        cell.alignment = align(horizontal, "center", True)
        cell.border = bd


def note_style(ws, row, width, *, size=9):
    paint(ws, row, 1, row, 1,
          f=font(size, italic=True, color=MUTED),
          al=align("left", "top", True),
          bd=Border())
    text = ws.cell(row, 1).value
    set_height(ws, row, est_lines(text, width, 0.92) * (size * 1.36) + 4,
               manual=True)


def label_style(ws, row, ncols, *, top_rule=False):
    paint(ws, row, 1, row, ncols,
          f=font(14, bold=True, color=NAVY),
          al=align("left", "center", False),
          bd=border(top=side("thin", NAVY) if top_rule else None))
    set_height(ws, row, 25, manual=False)


def title_style(ws, row, ncols, width):
    paint(ws, row, 1, row, ncols,
          f=font(11, italic=True, color=NAVY),
          al=align("left", "center", True),
          bd=Border())
    text = ws.cell(row, 1).value
    set_height(ws, row, est_lines(text, width, 0.88) * 14.5 + 4, manual=True)


def banner_style(ws, row, ncols, width):
    paint(ws, row, 1, row, ncols,
          f=font(10, bold=True, color=NAVY),
          bg=fill(SOFT),
          al=align("left", "center", True),
          bd=border(top=side("thin", NAVY), bottom=side("thin", NAVY)))
    text = ws.cell(row, 1).value
    set_height(ws, row, est_lines(text, width, 0.90) * 13.5 + 5, manual=True)


def set_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def print_setup(ws, *, area, title_rows=None, landscape=True, fit_width=1,
                fit_height=0):
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws.page_setup.paperSize = 9  # A4
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    ws.page_setup.fitToWidth = fit_width
    ws.page_setup.fitToHeight = fit_height
    ws.print_options.horizontalCentered = True
    ws.page_margins = PageMargins(left=0.5, right=0.5, top=0.55,
                                  bottom=0.55, header=0.3, footer=0.3)
    ws.print_area = area
    # La asignacion None del setter de openpyxl no borra las filas repetidas
    # heredadas del libro base; se limpia el atributo interno para que la hoja
    # no arrastre el encabezado de otra tabla al imprimir.
    if title_rows:
        ws.print_title_rows = title_rows
    else:
        ws._print_rows = None
    ws._print_cols = None
    ws.oddFooter.left.text = f"SIVAC · Tablas de anexos (v{BOOK_VERSION_NUM})"
    # Solo el numero de pagina: el campo &N acumula páginas de hojas con
    # distinto escalado y producia totales discrepantes (33 y 34) en el mismo
    # trabajo de impresion.
    ws.oddFooter.right.text = "Página &P"


def clear_heights(ws):
    for key in list(ws.row_dimensions.keys()):
        del ws.row_dimensions[key]


# ---------------------------------------------------------------------------
# Sincronizacion opcional de la Tabla 51 y hoja de validez reportada
# ---------------------------------------------------------------------------
def leer_tabla_51_docx(docx_path: Path) -> list[list[str]]:
    """Extrae la Tabla 51 (Codigo HU / Iteracion XP) del DOCX fuente.

    No escribe nada: solo lee la tabla para sincronizar la hoja 08 cuando la
    v17 este disponible. No imputa filas ni puntajes.
    """
    try:
        from docx import Document
    except ImportError as exc:
        raise SystemExit(
            "[ERROR] python-docx no esta disponible para --actualizar-hu."
        ) from exc
    doc = Document(str(docx_path))
    target = None
    for tbl in doc.tables:
        if not tbl.rows:
            continue
        first = " ".join(c.text.strip() for c in tbl.rows[0].cells)
        if "Código HU" in first and "Iteración XP" in first:
            target = tbl
            break
    if target is None:
        raise SystemExit(
            "[ERROR] No se encontro la Tabla 51 (Codigo HU / Iteracion XP) "
            "en el DOCX fuente.")
    rows: list[list[str]] = []
    for row in target.rows[1:]:
        values, seen = [], set()
        for cell in row.cells:
            key = id(cell._tc)
            if key in seen:
                continue
            seen.add(key)
            values.append(" ".join(cell.text.split()))
        if any(values):
            rows.append(values[:5])
    return rows


def sincronizar_tabla_51(ws, rows: list[list[str]]) -> dict:
    """Sobrescribe las filas de la Tabla 51 conservando estilos y nota.

    Si el numero de filas del DOCX difiere del de la hoja, inserta o elimina
    las filas necesarias antes de la nota y reajusta el filtro y el area de
    impresion. No inventa filas: solo transcribe las del DOCX.
    """
    header = note = None
    for r in range(1, ws.max_row + 1):
        value = ws.cell(r, 1).value
        if not isinstance(value, str):
            continue
        if value.strip().lower() == "código hu":
            header = r
        if header is not None and value.strip().lower().startswith("nota."):
            note = r
            break
    if header is None or note is None:
        raise SystemExit(
            "[ERROR] No se reconocio la cabecera o la nota de la hoja "
            "08_TABLA_51_HISTORIAS_XP.")
    actuales = [r for r in range(header + 1, note)
                if any(ws.cell(r, c).value not in (None, "")
                       for c in range(1, 6))]
    delta = len(rows) - len(actuales)
    if delta != 0:
        # Ajusta la hoja al numero de filas del DOCX sin tocar el resto del
        # libro. La nota se desplaza con la tabla y se vuelve a combinar.
        nota_merge = None
        for rng in list(ws.merged_cells.ranges):
            if rng.min_row >= note:
                if rng.min_row == note and rng.max_row == note:
                    nota_merge = (rng.min_col, rng.max_col)
                ws.unmerge_cells(str(rng))
        if delta > 0:
            ws.insert_rows(note, delta)
        else:
            ws.delete_rows(note + delta, -delta)
        note += delta
        if nota_merge:
            ws.merge_cells(start_row=note, start_column=nota_merge[0],
                           end_row=note, end_column=nota_merge[1])
    actuales = list(range(header + 1, header + 1 + len(rows)))
    AUTO_ROWS.pop(ws.title, None)
    for i, values in enumerate(rows):
        r = actuales[i]
        for c in range(1, 6):
            ws.cell(r, c).value = values[c - 1] if c - 1 < len(values) else None
        data_style(ws, r, 5, band=(i % 2 == 1), total=False,
                   closing=(i == len(rows) - 1))
        auto_height(ws, r, [14, 42, 52, 32, 60])
    nota = ws.cell(note, 1).value or ""
    ws.cell(note, 1).value = re.sub(
        r"informe final v\d+", SOURCE_DOCX_STEM, nota, flags=re.IGNORECASE)
    note_style(ws, note, 200)
    ws.auto_filter.ref = f"A5:E{header + len(rows)}"
    ws.print_area = f"A1:E{note}"
    return {"filas_docx": len(rows), "filas_hoja": len(actuales),
            "cabecera": header, "nota": note,
            "filas_ajustadas": delta}


VERACITY_TABLES = {
    "06_TABLA_49_PRETEST": "Tabla 49",
    "07_TABLA_50_POSTTEST": "Tabla 50",
}


def sincronizar_rotulos_veracidad(wb, ruta_json: Path) -> dict:
    """Sincroniza rotulo y nota de las Tablas 49 y 50 con el lote de veracidad.

    Solo admite el caso declarado de datos de prueba: exige que el rotulo
    vigente coincida con el ancla del lote, que el texto nuevo no acredite
    mediciones de campo y que los nombres de los centros de acopio no cambien.
    No toca cifras, columnas ni ninguna otra hoja.
    """
    crudo = ruta_json.read_bytes()
    data = json.loads(crudo.decode("utf-8"))
    por_hoja = {}
    for item in data.get("sustituciones", []):
        ubicacion = item.get("ubicacion", "")
        for hoja, tabla in VERACITY_TABLES.items():
            if f"rotulo de la {tabla}" in ubicacion:
                por_hoja.setdefault(hoja, {})["rotulo"] = item
            elif f"nota de la {tabla}" in ubicacion:
                por_hoja.setdefault(hoja, {})["nota"] = item
    faltan = [h for h in VERACITY_TABLES if len(por_hoja.get(h, {})) != 2]
    if faltan:
        raise SystemExit(
            "[ERROR] El lote de veracidad no contiene rotulo y nota para: "
            + ", ".join(faltan))

    detalle = {}
    for hoja in VERACITY_TABLES:
        ws = wb[hoja]
        fila_titulo = next(
            (r for r in range(1, ws.max_row + 1)
             if isinstance(ws.cell(r, 1).value, str)
             and ws.cell(r, 1).value.strip().lower().startswith("matriz de datos")),
            None)
        fila_nota = next(
            (r for r in range(1, ws.max_row + 1)
             if isinstance(ws.cell(r, 1).value, str)
             and ws.cell(r, 1).value.strip().lower().startswith("nota.")),
            None)
        if fila_titulo is None or fila_nota is None:
            raise SystemExit(
                f"[ERROR] No se reconocio el rotulo o la nota de {hoja}.")
        rotulo = por_hoja[hoja]["rotulo"]
        nota = por_hoja[hoja]["nota"]
        vigente = ws.cell(fila_titulo, 1).value
        # La hoja 07 rotulaba "Posttest"; el DOCX y el lote usan "Postest".
        # Se admite esa variante ortografica y se registra el rotulo previo.
        normalizar = lambda t: re.sub(  # noqa: E731
            r"\s+", " ", str(t).replace("Posttest", "Postest")).strip()
        if normalizar(vigente) != normalizar(rotulo["ancla_original"]):
            raise SystemExit(
                f"[ERROR] El rotulo vigente de {hoja} no coincide con el ancla "
                f"del lote de veracidad: {vigente!r}")
        for texto, etiqueta in ((rotulo["texto_nuevo"], "rotulo"),
                                (nota["texto_nuevo"], "nota")):
            bajo = texto.lower()
            for prohibido in ("acreditado", "datos recolectados"):
                if prohibido in bajo:
                    raise SystemExit(
                        f"[ERROR] El {etiqueta} nuevo de {hoja} conserva "
                        f"{prohibido!r}; se detiene la sincronizacion.")
            if ("mediciones finales" in bajo
                    and "no constituyen mediciones finales" not in bajo):
                raise SystemExit(
                    f"[ERROR] El {etiqueta} nuevo de {hoja} afirma mediciones "
                    "finales; se detiene la sincronizacion.")
        nota_baja = nota["texto_nuevo"].lower()
        if not all(clave in nota_baja for clave in
                   ("no constituyen", "mediciones", "de campo")):
            raise SystemExit(
                f"[ERROR] La nota nueva de {hoja} no declara que los valores "
                "no constituyen mediciones de campo.")
        centros_antes = [ws.cell(r, 2).value for r in range(fila_titulo + 3,
                                                           fila_nota)]
        ws.cell(fila_titulo, 1).value = rotulo["texto_nuevo"]
        ws.cell(fila_nota, 1).value = nota["texto_nuevo"]
        note_style(ws, fila_nota, 200)
        centros_despues = [ws.cell(r, 2).value for r in range(fila_titulo + 3,
                                                             fila_nota)]
        if centros_antes != centros_despues:
            raise SystemExit(
                f"[ERROR] La sincronizacion altero los centros de acopio de {hoja}.")
        detalle[hoja] = {
            "rotulo": rotulo["texto_nuevo"],
            "rotulo_previo": vigente,
            "nota": nota["texto_nuevo"],
            "centros_preservados": sum(
                1 for r in range(fila_titulo + 4, fila_nota)
                if str(ws.cell(r, 1).value or "").startswith("TRAB-")),
        }
    return {"json": str(ruta_json),
            "sha256": hashlib.sha256(crudo).hexdigest(),
            "caso": "DATOS DE PRUEBA",
            "hojas": detalle}


def agregar_hoja_validez(wb, source_docx: str, source_sha: str) -> None:
    """Hoja breve de validez reportada, sin matriz fingida por juez.

    Usa formulas para V e IVC. La V no imputa n: bajo unanimidad en el maximo,
    S = n(c-1), n se cancela y V = (c-l)/(c-l); solo se calcula si c = 4 y
    l = 1. El IVC (S-CVI/Ave) es el promedio entre componentes de la proporcion
    de valoraciones favorables de cada componente, no el promedio de la V
    ordinal; en el caso declarado de unanimidad maxima cada proporcion es n/n
    y el promedio es 1. La hoja no toca ninguna columna estadistica existente.
    """
    name = "16_VALIDEZ_REPORTADA"
    if name in wb.sheetnames:
        del wb[name]
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = TAB_TABLE
    set_widths(ws, [34, 18, 70])

    def section(row: int, text: str) -> None:
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=3)
        c = ws.cell(row, 1, text)
        c.font = font(10, bold=True, color=WHITE)
        c.fill = fill(NAVY)
        c.alignment = align("left", "center", False)
        c.border = Border()
        ws.row_dimensions[row].height = 20

    def merged(row: int, text: str, *, size=9, bold=False, italic=False,
               height=None) -> None:
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=3)
        c = ws.cell(row, 1, text)
        c.font = font(size, bold=bold, italic=italic, color=INK)
        c.alignment = align("left", "top", True)
        c.border = Border()
        set_height(ws, row, height or (est_lines(text, 122, 0.95) * 13 + 4),
                   manual=True)

    ws.merge_cells("A1:C1")
    c = ws.cell(1, 1, "VALIDEZ DE CONTENIDO REPORTADA (NO CERTIFICADA)")
    c.font = Font(name=FONT, size=14, bold=True, color=NAVY)
    c.alignment = align("center", "center", True)
    c.border = border(bottom=side("medium", NAVY))
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:C2")
    c = ws.cell(2, 1, "Matriz de validación de contenido del expediente v09 · "
                      "escala ordinal 1-4 · doce componentes y tres criterios")
    c.font = font(10, italic=True, color=NAVY)
    c.alignment = align("center", "center", True)
    c.border = Border()
    ws.row_dimensions[2].height = 18

    merged(3, f"Fuente documental del libro: {source_docx} · SHA-256 {source_sha}",
           size=8, italic=True, height=26)

    section(5, "PARÁMETROS Y RESULTADO PUNTUAL CONDICIONAL")
    # Cabecera de la tabla de parametros (fila 6)
    for col, text in ((1, "Parámetro"), (2, "Valor"), (3, "Fundamento")):
        c = ws.cell(6, col, text)
        c.font = font(9.5, bold=True, color=WHITE)
        c.fill = fill(NAVY)
        c.alignment = align("center", "center", True)
        c.border = border(top=side("thin", NAVY), bottom=side("medium", NAVY))
    ws.row_dimensions[6].height = 20

    params = [
        ("c (categorías de la escala)", 4,
         "Escala ordinal 1-4 del expediente v09."),
        ("l (calificación mínima)", 1, "1 = No cumple; 4 = Cumple plenamente."),
        ("Unanimidad en el máximo", "Sí",
         "Declaración del tesista: todos los jueces asignaron 4 en todo."),
        ("n (jueces)", "No especificado",
         "El diseño prevé tres jueces; la declaración no confirma el número."),
        ("V de Aiken (puntual)",
         '=IF(AND(B9="Sí",B7=4,B8=1),(B7-B8)/(B7-B8),"No calculable")',
         "Solo se calcula con c = 4 y l = 1. Con unanimidad, S = n(c-1); n se "
         "cancela y V = (c-l)/(c-l) = 1.000."),
        ("IVC (S-CVI/Ave)",
         '=IF(AND(B9="Sí",B7=4,B8=1,B11=1),1,"No calculable")',
         "Caso de unanimidad máxima reportada: cada I-CVI es la proporción de "
         "valoraciones favorables del componente (n/n = 1) y el S-CVI/Ave es "
         "el promedio entre componentes. No es una identidad IVC = V."),
        ("IC de Aiken", "No calculado",
         "Requiere n confirmado y el método de Penfield y Giacobbi (2004); no se imputa n = 3."),
    ]
    for i, (label, value, basis) in enumerate(params):
        r = 7 + i
        ws.cell(r, 1, label).font = font(9.5, bold=True, color=NAVY)
        ws.cell(r, 2, value).font = font(9.5, color=INK)
        ws.cell(r, 3, basis).font = font(9, color=MUTED)
        for col in range(1, 4):
            cell = ws.cell(r, col)
            cell.fill = fill(BAND) if i % 2 else fill(WHITE)
            cell.alignment = align("left" if col != 2 else "center", "center", True)
            cell.border = border(
                bottom=side("medium", NAVY) if i == len(params) - 1 else side("thin", RULE))
        ws.cell(r, 2).number_format = "0.000"
        set_height(ws, r, max(26, est_lines(basis, 70, 0.80) * 12 + 8),
                   manual=True)
    ws.row_dimensions[14].height = 8

    section(15, "CONDICIONES DEL CÁLCULO CONDICIONAL")
    condiciones = [
        "1. El instrumento aplicado fue la matriz del expediente v09, con 12 componentes y tres criterios.",
        "2. La escala experta fue la ordinal 1-4 (1 = No cumple; 4 = Cumple plenamente).",
        "3. Todos los jueces que respondieron asignaron 4 en todas las celdas ítem × criterio.",
        "4. El tesista ratifica que «4 en todo» cubre la totalidad de componentes, criterios y jueces.",
    ]
    for i, text in enumerate(condiciones):
        merged(16 + i, text)
    ws.row_dimensions[20].height = 8

    merged(21, "Resultados calculados a partir de calificaciones comunicadas "
               "por el tesista. Pendientes de cotejo con las fichas originales.",
           size=8, italic=True, height=26)

    ws.freeze_panes = "A7"
    print_setup(ws, area="A1:C21", title_rows=None)


# ---------------------------------------------------------------------------
# Validacion del entorno, huella de la fuente y modo de simulacion
# ---------------------------------------------------------------------------
if not IN_XLSX.exists():
    raise SystemExit(f"[ERROR] No existe el libro base: {IN_XLSX}")
if not SOURCE_DOCX_PATH.exists():
    raise SystemExit(f"[ERROR] No existe el DOCX fuente: {SOURCE_DOCX_PATH}")
if OUT_XLSX == IN_XLSX:
    raise SystemExit("[ERROR] La salida no puede ser el mismo archivo que la base.")
if REF_XLSX is not None and REF_XLSX == OUT_XLSX:
    raise SystemExit("[ERROR] La referencia de paridad no puede ser la salida.")
if REF_XLSX is not None and not REF_XLSX.exists():
    raise SystemExit(f"[ERROR] No existe la referencia de paridad: {REF_XLSX}")
try:
    datetime.date.fromisoformat(FECHA_GENERACION)
except ValueError:
    raise SystemExit(f"[ERROR] Fecha invalida (AAAA-MM-DD): {FECHA_GENERACION}")

SOURCE_SHA256 = sha256_file(SOURCE_DOCX_PATH)
SOURCE_SIZE = SOURCE_DOCX_PATH.stat().st_size
BASE_SHA256 = sha256_file(IN_XLSX)
REF_SHA256 = sha256_file(REF_XLSX) if REF_XLSX is not None else None


def excel_disponible() -> tuple[bool, str]:
    """Comprueba que Excel pueda abrirse en una instancia aislada."""
    try:
        import pythoncom
        import win32com.client as win32
    except ImportError as exc:
        return False, f"pywin32 no disponible: {exc}"
    pythoncom.CoInitialize()
    app = None
    try:
        app = win32.DispatchEx("Excel.Application")
        app.Visible = False
        app.DisplayAlerts = False
        return True, "Excel COM disponible"
    except Exception as exc:
        return False, str(exc)
    finally:
        if app is not None:
            try:
                app.Quit()
            except Exception:
                pass
        pythoncom.CoUninitialize()


def recalcular_con_excel(path: Path) -> dict:
    """Recalcula la cache de formulas con una instancia aislada de Excel.

    Excel COM es la unica alternativa disponible: openpyxl escribe formulas sin
    valor cacheado y LibreOffice no esta instalado. La instancia se crea con
    DispatchEx para no interferir con ninguna sesion abierta del usuario.
    """
    try:
        import pythoncom
        import win32com.client as win32
    except ImportError as exc:
        return {"estado": "fallido", "motor": "Excel COM",
                "motivo": f"pywin32 no disponible: {exc}"}
    pythoncom.CoInitialize()
    app = None
    libro = None
    try:
        app = win32.DispatchEx("Excel.Application")
        app.Visible = False
        app.DisplayAlerts = False
        app.AskToUpdateLinks = False
        libro = app.Workbooks.Open(str(path), UpdateLinks=0, ReadOnly=False)
        app.CalculateFullRebuild()
        libro.Save()
        paginas = {}
        for hoja in libro.Worksheets:
            try:
                paginas[str(hoja.Name)] = int(hoja.PageSetup.Pages.Count)
            except Exception:
                paginas[str(hoja.Name)] = None
        version = str(getattr(app, "Version", "") or "").strip()
        total = sum(v for v in paginas.values() if isinstance(v, int))
        return {"estado": "recalculado",
                "motor": f"Excel COM {version}".strip(),
                "paginas_impresion": paginas,
                "paginas_totales": total}
    except Exception as exc:
        return {"estado": "fallido", "motor": "Excel COM", "motivo": str(exc)}
    finally:
        if libro is not None:
            try:
                libro.Close(SaveChanges=False)
            except Exception:
                pass
        if app is not None:
            try:
                app.Quit()
            except Exception:
                pass
        pythoncom.CoUninitialize()


if ARGS.dry_run:
    print("=" * 78)
    print("MODO SIMULACION (--dry-run): no se escribe ningun archivo")
    print("=" * 78)
    print(f"Base               : {IN_XLSX}")
    print(f"  SHA-256 base     : {BASE_SHA256}")
    print(f"Fuente DOCX        : {SOURCE_DOCX_PATH}")
    print(f"  Bytes            : {SOURCE_SIZE:,}")
    print(f"  SHA-256 fuente   : {SOURCE_SHA256}")
    print(f"Salida             : {OUT_XLSX} (version {BOOK_VERSION_DOTTED})")
    print(f"  Ya existe        : {'si' if OUT_XLSX.exists() else 'no'}")
    print(f"Referencia paridad : {REF_XLSX if REF_XLSX else 'ninguna'}")
    if REF_SHA256:
        print(f"  SHA-256 ref.     : {REF_SHA256}")
    print(f"Fecha              : {FECHA_GENERACION}")
    print(f"Hoja de validez    : {'si' if ARGS.hoja_validez else 'no'}")
    print(f"Actualizar Tabla 51: {'si' if ARGS.actualizar_hu else 'no'}")
    print(f"Recalcular cache   : {'si' if ARGS.recalcular else 'no'}")
    if ARGS.hoja_validez:
        ok, motivo = excel_disponible()
        print(f"Preflight Excel    : {'OK' if ok else 'NO DISPONIBLE'} ({motivo})")
    if ARGS.actualizar_hu:
        filas = leer_tabla_51_docx(SOURCE_DOCX_PATH)
        print(f"Tabla 51 en fuente : {len(filas)} filas")
        for fila in filas:
            print("  " + " | ".join(fila))
    print("=" * 78)
    raise SystemExit(0)

if OUT_XLSX.exists() and not ARGS.force:
    raise SystemExit(
        f"[ERROR] La salida ya existe: {OUT_XLSX}\n"
        "         Use --force para reemplazarla o indique otra ruta con --salida.")

if ARGS.hoja_validez:
    ok, motivo = excel_disponible()
    if not ok:
        raise SystemExit(
            "[ERROR] --hoja-validez requiere Excel COM para cachear las formulas: "
            f"{motivo}.\n         Sin cache verificada no se escribe la hoja.")

wb = openpyxl.load_workbook(IN_XLSX)

# Captura de paridad numerica ANTES de cualquier cambio.
numeric_before = {}
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, (int, float)) and not isinstance(cell.value, bool):
                numeric_before[(ws.title, cell.coordinate)] = cell.value

# ---------------------------------------------------------------------------
# 1. Portada institucional redisenada
# ---------------------------------------------------------------------------
del wb["00_PORTADA"]
ws = wb.create_sheet("00_PORTADA", 0)
ws.sheet_view.showGridLines = False
ws.sheet_properties.tabColor = TAB_TABLE
set_widths(ws, [28, 16, 26, 18, 18, 18])
TOTAL_W = 124

# Banda institucional (tres niveles)
for row, text, size, bold, italic, height in (
    (1, "UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS", 16, True, False, 32),
    (2, "Escuela Profesional de Ingeniería de Sistemas", 11, False, False, 20),
    (3, "TABLAS DE ANEXOS DEL INFORME FINAL", 18, True, False, 38),
):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
    c = ws.cell(row, 1, text)
    c.font = Font(name=FONT, size=size, bold=bold, italic=italic, color="FFFFFFFF")
    c.fill = fill(NAVY)
    c.alignment = align("center", "center", True)
    c.border = Border()
    ws.row_dimensions[row].height = height

ws.row_dimensions[4].height = 10

ws.merge_cells(start_row=5, start_column=1, end_row=5, end_column=6)
c = ws.cell(5, 1, "Sistema web SIVAC y gestión de movimientos mensuales de vacunas")
c.font = font(12, italic=True, color=NAVY)
c.alignment = align("center", "center", True)
c.border = border(bottom=side("medium", NAVY))
ws.row_dimensions[5].height = 24

ws.row_dimensions[6].height = 8

ws.merge_cells(start_row=7, start_column=1, end_row=7, end_column=6)
c = ws.cell(7, 1, "APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE "
                  "MOVIMIENTOS MENSUALES DE VACUNAS EN EL PERSONAL DE "
                  "INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II")
c.font = font(11, bold=True, italic=True, color=NAVY)
c.alignment = align("center", "center", True)
c.border = Border()
ws.row_dimensions[7].height = 58

ws.row_dimensions[8].height = 8

meta = [
    "Tesista: Bach. José Luis Quispe León",
    "Asesora: Dra. Norma Lorena Catacora Flores",
    "Diseño: preexperimental con pretest y postest en un solo grupo (O₁ → X → O₂)",
    "Población censal: N = n = 14 operadores de inmunizaciones",
    "Ámbito: Dirección de Salud Apurímac II, Red de frío",
]
for i, text in enumerate(meta):
    r = 9 + i
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    c = ws.cell(r, 1, text)
    c.font = font(10, color=INK)
    c.alignment = align("left", "center", True)
    c.border = Border()
    ws.row_dimensions[r].height = 17

for r in (14, 15, 16):
    ws.row_dimensions[r].height = 6

# Aviso unico de datos provisionales, preservado en A17
ws.merge_cells(start_row=17, start_column=1, end_row=17, end_column=6)
c = ws.cell(17, 1, MARKER)
c.font = font(10, bold=True, color=NAVY)
c.fill = fill(SOFT)
c.alignment = align("center", "center", True)
c.border = border(top=side("thin", NAVY), bottom=side("thin", NAVY))
ws.row_dimensions[17].height = 26

ws.row_dimensions[18].height = 8


def cover_section(row, text):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
    c = ws.cell(row, 1, text)
    c.font = font(11, bold=True, color=WHITE)
    c.fill = fill(NAVY)
    c.alignment = align("left", "center", False)
    c.border = Border()
    ws.row_dimensions[row].height = 22


def cover_pair(row, label, value, band=False, closing=False):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)
    ws.merge_cells(start_row=row, start_column=3, end_row=row, end_column=6)
    bg = fill(BAND) if band else fill(WHITE)
    bd = border(bottom=side("medium", NAVY) if closing else side("thin", RULE))
    c = ws.cell(row, 1, label)
    c.font = font(10, bold=True, color=NAVY)
    c.fill = bg
    c.alignment = align("left", "center", True)
    c.border = bd
    c = ws.cell(row, 3, value)
    c.font = font(10, color=INK)
    c.fill = bg
    c.alignment = align("left", "center", True)
    c.border = bd
    ws.row_dimensions[row].height = 20


cover_section(19, "CONTROL DE VERSIÓN")
ws.merge_cells(start_row=20, start_column=1, end_row=20, end_column=2)
ws.merge_cells(start_row=20, start_column=3, end_row=20, end_column=6)
for col, text in ((1, "Campo"), (3, "Valor")):
    c = ws.cell(20, col, text)
    c.font = font(10, bold=True, color=WHITE)
    c.fill = fill(NAVY)
    c.alignment = align("left", "center", True)
    c.border = border(top=side("thin", NAVY), bottom=side("medium", NAVY))
ws.row_dimensions[20].height = 22

cover_pair(21, "Versión del libro", BOOK_VERSION_DOTTED, band=False)
cover_pair(22, "Fecha de generación", FECHA_GENERACION, band=True)
cover_pair(23, "Fuente documental", f"{SOURCE_DOCX} · SHA-256 {SOURCE_SHA256[:16]}…",
           band=False)
cover_pair(24, "Estado de los datos", "De prueba", band=True)
cover_pair(25, "Estándar de composición",
           "APA 7: tres líneas horizontales, sin líneas verticales", band=False,
           closing=True)

ws.row_dimensions[26].height = 12

cover_section(27, "CONTENIDO DEL LIBRO")
ws.merge_cells(start_row=28, start_column=1, end_row=28, end_column=2)
ws.merge_cells(start_row=28, start_column=3, end_row=28, end_column=6)
for col, text in ((1, "Hoja"), (3, "Contenido")):
    c = ws.cell(28, col, text)
    c.font = font(10, bold=True, color=WHITE)
    c.fill = fill(NAVY)
    c.alignment = align("left", "center", True)
    c.border = border(top=side("thin", NAVY), bottom=side("medium", NAVY))
ws.row_dimensions[28].height = 21

index = [
    ("00_PORTADA", "Portada institucional, control de versión y fuentes."),
    ("01_TABLA_44_CONSISTENCIA", "Tabla 44. Matriz de consistencia metodológica."),
    ("02_TABLA_45_OPERACIONALIZACION", "Tabla 45. Matriz de operacionalización de variables."),
    ("03_TABLA_46_INSTRUMENTO_01", "Tabla 46. Ficha de registro cronométrico de tiempos."),
    ("04_TABLA_47_INSTRUMENTO_02", "Tabla 47. Ficha de auditoría y cotejo documental."),
    ("05_TABLA_48_INSTRUMENTO_03_TAM", "Tabla 48. Cuestionario TAM (Modalidad A)."),
    ("06_TABLA_49_PRETEST", "Tabla 49. Matriz de datos del pretest (n = 14)."),
    ("07_TABLA_50_POSTTEST", "Tabla 50. Matriz de datos del posttest (n = 14)."),
    ("08_TABLA_51_HISTORIAS_XP", "Tabla 51. Historias de usuario bajo Extreme Programming."),
    ("09_DESCRIPTIVOS", "Tablas 36, 37 y 38. Estadística descriptiva comparativa."),
    ("10_CONFIABILIDAD", "Tabla 35. Alfa de Cronbach e IC 95 % de Feldt."),
    ("11_NORMALIDAD", "Tabla 39. Shapiro-Wilk sobre diferencias pareadas."),
    ("12_CONTRASTES", "Tablas 40 a 43. Contrastes y ajuste de Holm-Bonferroni."),
    ("13_SPSS_SINTAXIS", "Sintaxis reproducible de IBM SPSS Statistics."),
    ("14_SPSS_SALIDAS", "Réplica del visor SPSS en formato de tabla."),
    ("15_NOTAS_TRAZABILIDAD", "Trazabilidad, rangos de celdas y notas APA."),
]
if ARGS.hoja_validez:
    index.append(
        ("16_VALIDEZ_REPORTADA",
         "Validez de contenido reportada. Cálculo condicional, no certificado."))
for i, (name, desc) in enumerate(index):
    r = 29 + i
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
    ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=6)
    bg = fill(BAND) if i % 2 else fill(WHITE)
    bd = border(bottom=side("thin", RULE))
    c = ws.cell(r, 1, name)
    c.font = font(9.5, bold=True, color=NAVY)
    c.fill = bg
    c.alignment = align("left", "center", False)
    c.border = bd
    c = ws.cell(r, 3, desc)
    c.font = font(9.5, color=INK)
    c.fill = bg
    c.alignment = align("left", "center", False)
    c.border = bd
    ws.row_dimensions[r].height = 17

last_index_row = 29 + len(index) - 1
ws.row_dimensions[last_index_row + 1].height = 12

fuentes_row = last_index_row + 2
cover_section(fuentes_row, "FUENTES DE DATOS")
sources = [
    f"{SOURCE_DOCX} (solo lectura): tablas 35 a 51 y rótulos visibles. "
    f"SHA-256 {SOURCE_SHA256}.",
    "pretest_campo.csv y posttest_campo.csv: matrices de datos (n = 14).",
    "reporte_estadistico_completo.json: descriptivos, normalidad, contrastes y confiabilidad.",
    "Las cifras se recalcularon desde los CSV y se contrastaron con el JSON y con el DOCX.",
]
for i, text in enumerate(sources):
    r = fuentes_row + 1 + i
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    c = ws.cell(r, 1, text)
    c.font = font(9, color=MUTED)
    c.alignment = align("left", "center", True)
    c.border = Border()
    set_height(ws, r, est_lines(text, 116, 0.85) * 12 + 5, manual=True)

spacer_row = fuentes_row + len(sources) + 1
ws.row_dimensions[spacer_row].height = 10

note_row = spacer_row + 1
ws.merge_cells(start_row=note_row, start_column=1, end_row=note_row, end_column=6)
c = ws.cell(note_row, 1,
            "Nota. Composición editorial conforme al estándar APA 7: tablas de tres "
            "líneas horizontales, sin líneas verticales, encabezado azul institucional "
            "y bandas alternas de lectura. La precisión decimal de cada tabla se "
            "declara en su propia nota.")
c.font = font(9, italic=True, color=MUTED)
c.alignment = align("left", "top", True)
c.border = Border()
set_height(ws, note_row, 44, manual=True)

# En celdas combinadas, Excel solo dibuja el borde de la celda superior
# izquierda; para que las lineas recorran todo el ancho combinado se replican
# los bordes en cada celda del rango.
for rng in list(ws.merged_cells.ranges):
    tl = ws.cell(rng.min_row, rng.min_col)
    bd = copy(tl.border)
    if any(getattr(s, "style", None)
           for s in (bd.left, bd.right, bd.top, bd.bottom)):
        paint(ws, rng.min_row, rng.min_col, rng.max_row, rng.max_col, bd=bd)

# La portada institucional ocupa la primera pagina impresa y el indice la
# segunda. Sin este corte, el encabezado del indice queda al pie de la pagina 1
# y sus filas se separan del titulo en la pagina siguiente.
ws.row_breaks.append(Break(id=26))

print_setup(ws, area=f"A1:F{note_row}", title_rows=None)

# ---------------------------------------------------------------------------
# 2. Actualizacion de textos: fuente documental, avisos y doble punto
# ---------------------------------------------------------------------------
REPLACEMENTS = (
    (re.compile(r"informe_final_v\d+\.docx", re.IGNORECASE), SOURCE_DOCX),
    (re.compile(r"informe[ _]final[ _]v\d+\.docx", re.IGNORECASE), SOURCE_DOCX),
    (re.compile(r"informe[ _]final[ _]v\d+", re.IGNORECASE), SOURCE_DOCX_STEM),
)

# Detecta cualquier referencia a una version distinta de la fuente vigente.
STALE_SOURCE = re.compile(r"informe[ _]final[ _]v(\d+)", re.IGNORECASE)


def clean_text(value: str) -> str:
    out = value.replace(LEGACY_MARKER, MARKER)
    for pattern, new in REPLACEMENTS:
        out = pattern.sub(new, out)
    return out


NOTE_ROWS = {
    "01_TABLA_44_CONSISTENCIA": [11],
    "02_TABLA_45_OPERACIONALIZACION": [11],
    "03_TABLA_46_INSTRUMENTO_01": [10],
    "04_TABLA_47_INSTRUMENTO_02": [10],
    "05_TABLA_48_INSTRUMENTO_03_TAM": [15],
    "06_TABLA_49_PRETEST": [21],
    "07_TABLA_50_POSTTEST": [21],
    "08_TABLA_51_HISTORIAS_XP": [12],
    "09_DESCRIPTIVOS": [13, 27, 44],
    "10_CONFIABILIDAD": [13],
    "11_NORMALIDAD": [14],
    "12_CONTRASTES": [11, 23, 37, 49],
    "14_SPSS_SALIDAS": [260],
    "15_NOTAS_TRAZABILIDAD": [26],
}

for ws in wb.worksheets:
    if ws.title == "00_PORTADA":
        continue

    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, str):
                cell.value = clean_text(cell.value)

    # El aviso de datos provisionales se conserva una sola vez por hoja:
    # en la banda superior de las hojas con cifras empiricas. Se retira de las notas.
    for r in NOTE_ROWS.get(ws.title, []):
        cell = ws.cell(r, 1)
        if isinstance(cell.value, str):
            text = cell.value.replace(" " + MARKER, "").replace(MARKER, "")
            cell.value = text.rstrip()

# Sintaxis SPSS: conservar el aviso del encabezado y retirarlo del cierre.
if "13_SPSS_SINTAXIS" in wb.sheetnames:
    ws = wb["13_SPSS_SINTAXIS"]
    for r in range(1, ws.max_row + 1):
        cell = ws.cell(r, 1)
        if isinstance(cell.value, str) and MARKER in cell.value:
            if not cell.value.lstrip().upper().startswith("* ADVERTENCIA"):
                cell.value = cell.value.replace(" " + MARKER, "").replace(MARKER, "").rstrip()

# ---------------------------------------------------------------------------
# 3. Rediseno de hojas tabulares
# ---------------------------------------------------------------------------
SPECS = {
    "01_TABLA_44_CONSISTENCIA": dict(
        widths=[28, 34, 34, 44, 44], labels=[1], titles=[2], banner=[3],
        headers=[5], data=[(6, 9, 5)], notes=[11], totals=[], freeze="A6",
        print_titles="1:5"),
    "02_TABLA_45_OPERACIONALIZACION": dict(
        widths=[22, 38, 26, 42, 26, 20], labels=[1], titles=[2], banner=[3],
        headers=[5], data=[(6, 9, 6)], notes=[11], totals=[], freeze="A6",
        print_titles="1:5"),
    "03_TABLA_46_INSTRUMENTO_01": dict(
        widths=[14, 40, 64, 24], labels=[1], titles=[2], banner=[3],
        headers=[5], data=[(6, 8, 4)], notes=[10], totals=[], freeze="A6",
        print_titles="1:5"),
    "04_TABLA_47_INSTRUMENTO_02": dict(
        widths=[14, 42, 64, 24], labels=[1], titles=[2], banner=[3],
        headers=[5], data=[(6, 8, 4)], notes=[10], totals=[], freeze="A6",
        print_titles="1:5"),
    "05_TABLA_48_INSTRUMENTO_03_TAM": dict(
        widths=[12, 30, 80, 30], labels=[1], titles=[2], banner=[3],
        headers=[5], data=[(6, 13, 4)], notes=[15], totals=[], freeze="A6",
        print_titles="1:5"),
    "06_TABLA_49_PRETEST": dict(
        widths=[9, 28, 11, 11, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 10, 8],
        labels=[1], titles=[2], banner=[3], headers=[5],
        data=[(6, 19, 18)], notes=[21], totals=[], freeze="A6",
        print_titles="1:5"),
    "07_TABLA_50_POSTTEST": dict(
        widths=[9, 28, 11, 11, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 10, 8],
        labels=[1], titles=[2], banner=[3], headers=[5],
        data=[(6, 19, 18)], notes=[21], totals=[], freeze="A6",
        print_titles="1:5"),
    "08_TABLA_51_HISTORIAS_XP": dict(
        widths=[14, 42, 52, 32, 60], labels=[1], titles=[2], banner=[3],
        headers=[5], data=[(6, 10, 5)], notes=[12], totals=[], freeze="A6",
        print_titles="1:5"),
    "09_DESCRIPTIVOS": dict(
        widths=[42, 20, 7, 11, 10, 11, 10, 11, 11, 11, 11, 12],
        labels=[1, 15, 29], titles=[2, 16, 30], banner=[3],
        headers=[5, 19, 33],
        data=[(6, 11, 12), (20, 25, 12), (34, 42, 12)],
        notes=[13, 27, 44], totals=[40, 41, 42], freeze="A6",
        print_titles=None),
    "10_CONFIABILIDAD": dict(
        widths=[28, 36, 12, 11, 14, 14, 14, 20], labels=[1], titles=[2],
        banner=[3], headers=[5], data=[(6, 11, 8)], notes=[13],
        totals=[6, 9], freeze="A6", print_titles="1:5"),
    "11_NORMALIDAD": dict(
        widths=[22, 46, 7, 14, 7, 10, 28, 26], labels=[1], titles=[2],
        banner=[3], headers=[5], data=[(6, 12, 8)], notes=[14],
        totals=[], freeze="A6", print_titles="1:5"),
    "12_CONTRASTES": dict(
        widths=[30, 27, 14, 12, 10, 12, 11, 19, 12, 12, 18],
        labels=[1, 13, 25, 39], titles=[2, 14, 26, 40], banner=[3],
        headers=[5, 17, 29, 43],
        data=[(6, 9, 11), (18, 21, 11), (30, 35, 11), (44, 47, 8)],
        notes=[11, 23, 37, 49], totals=[47], freeze="A6", print_titles=None),
    "15_NOTAS_TRAZABILIDAD": dict(
        widths=[14, 34, 14, 44, 66], labels=[1], titles=[2], banner=[],
        headers=[5], data=[(6, 24, 5)], notes=[26], totals=[], freeze="A6",
        print_titles="1:5"),
}

for name, spec in SPECS.items():
    ws = wb[name]
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = TAB_TABLE
    clear_heights(ws)
    set_widths(ws, spec["widths"])
    total_width = sum(spec["widths"])

    for i, r in enumerate(spec["labels"]):
        label_style(ws, r, len(spec["widths"]), top_rule=(i > 0))
    for r in spec["titles"]:
        title_style(ws, r, len(spec["widths"]), total_width)
    for r in spec["banner"]:
        banner_style(ws, r, len(spec["widths"]), total_width)
    for r in spec["headers"]:
        ncols = ws.max_column
        head_style(ws, r, ncols)
    for first, last, ncols in spec["data"]:
        for r in range(first, last + 1):
            data_style(ws, r, ncols,
                       band=((r - first) % 2 == 1),
                       total=(r in spec["totals"]),
                       closing=(r == last))
            auto_height(ws, r, spec["widths"][:ncols])
    for r in spec["notes"]:
        note_style(ws, r, total_width)
    for r in range(1, ws.max_row + 1):
        if ws.row_dimensions[r].height is None:
            ws.row_dimensions[r].height = 8

    ws.freeze_panes = spec["freeze"]
    print_setup(ws, area=f"A1:{get_column_letter(len(spec['widths']))}{ws.max_row}",
                title_rows=spec["print_titles"])

# La fila 7 de la matriz de operacionalizacion contiene la definicion mas larga
# del indicador T_vale; se fija en 70 pt (68 pt requeridos por el modelo de
# lineas) porque la celda D7 esta combinada y Excel no autoajusta combinadas.
ws = wb["02_TABLA_45_OPERACIONALIZACION"]
AUTO_ROWS.get(ws.title, set()).discard(7)
ws.row_dimensions[7].height = 70

# La Tabla 43 (sintesis multivariada) se imprime completa en una pagina: sin
# este corte, el titulo y la cabecera quedaban al pie de la pagina anterior y
# las filas de contraste aparecian sin rotulo en la siguiente.
wb["12_CONTRASTES"].row_breaks.append(Break(id=38))

# Matrices: los totales enteros deben presentarse sin decimales.
for name in ("06_TABLA_49_PRETEST", "07_TABLA_50_POSTTEST"):
    ws = wb[name]
    for r in range(6, 20):
        for c in (3, 4, 5, 6):
            ws.cell(r, c).number_format = "0.00"
        for c in range(7, 17):
            ws.cell(r, c).number_format = "0"
        ws.cell(r, 17).number_format = "0"  # TAM total (entero)
        ws.cell(r, 18).number_format = "General"  # Nivel (texto)

# ---------------------------------------------------------------------------
# 4. Hojas SPSS
# ---------------------------------------------------------------------------
# 13_SPSS_SINTAXIS
ws = wb["13_SPSS_SINTAXIS"]
ws.sheet_view.showGridLines = False
ws.sheet_properties.tabColor = TAB_SPSS
ws.column_dimensions["A"].width = 132
for r in range(1, ws.max_row + 1):
    cell = ws.cell(r, 1)
    text = cell.value if isinstance(cell.value, str) else ""
    if text.startswith("* ---") or text.startswith("* ==="):
        cell.font = font(9, bold=True, color=NAVY, name=MONO)
        cell.fill = fill(SOFT)
        cell.alignment = align("left", "center", False)
        cell.border = border(top=side("thin", RULE), bottom=side("thin", RULE))
        ws.row_dimensions[r].height = 15
    elif text.startswith("* "):
        cell.font = font(9, bold=True, color=NAVY, name=MONO)
        cell.alignment = align("left", "center", False)
        cell.border = Border()
        ws.row_dimensions[r].height = 15
    elif text == "":
        ws.row_dimensions[r].height = 8
    else:
        cell.font = font(9, color=INK, name=MONO)
        cell.alignment = align("left", "center", False)
        cell.border = Border()
        ws.row_dimensions[r].height = 14
AUTO_ROWS.setdefault(ws.title, set()).update(range(1, 248))
note_style(ws, 248, 132)
ws.freeze_panes = "A8"
# El listado de sintaxis es continuo: repetir el bloque de comentarios inicial
# en cada pagina robaba cinco lineas utiles y cortaba las sentencias.
print_setup(ws, area=f"A1:A{ws.max_row}", title_rows=None)

# 14_SPSS_SALIDAS
ws = wb["14_SPSS_SALIDAS"]
ws.sheet_view.showGridLines = False
ws.sheet_properties.tabColor = TAB_SPSS
set_widths(ws, [58, 18, 24, 12])
clear_heights(ws)

# Titulo y aviso. En celdas combinadas el borde inferior solo se dibuja si se
# aplica a todas las celdas del rango, no unicamente a la celda superior izquierda.
ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=4)
c = ws.cell(1, 1, "RESULTADOS CON PRESENTACIÓN TIPO SPSS - SIVAC (n = 14)")
c.font = font(14, bold=True, color=NAVY)
c.alignment = align("left", "center", False)
paint(ws, 1, 1, 1, 4, bd=border(bottom=side("medium", NAVY)))
c.border = border(bottom=side("medium", NAVY))
ws.row_dimensions[1].height = 28

ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=4)
c = ws.cell(2, 1, "Cálculos elaborados con Python; presentación tipo SPSS; "
                  "datos de prueba.")
c.font = font(10, bold=True, color=NAVY)
c.fill = fill(SOFT)
c.alignment = align("left", "center", True)
paint(ws, 2, 1, 2, 4, bg=fill(SOFT),
      bd=border(top=side("thin", NAVY), bottom=side("thin", NAVY)))
c.border = border(top=side("thin", NAVY), bottom=side("thin", NAVY))
ws.row_dimensions[2].height = 26

data_toggle = 0
for r in range(3, ws.max_row + 1):
    a = ws.cell(r, 1).value
    b = ws.cell(r, 2).value
    merged_full = any(m.min_row == r and m.max_row == r and
                      m.min_col == 1 and m.max_col == 4
                      for m in ws.merged_cells.ranges)
    is_section = (isinstance(a, str) and a.isupper() and merged_full)
    is_header = (a == "Estadístico" and b == "Valor")
    is_sub = merged_full and not is_section and a not in (None, "") and not is_header

    if r == 260:  # nota final
        note_style(ws, r, 112)
        continue
    if is_section:
        paint(ws, r, 1, r, 4, f=font(10, bold=True, color=WHITE), bg=fill(NAVY),
              al=align("left", "center", False),
              bd=border(top=side("thin", NAVY), bottom=side("thin", NAVY)))
        ws.row_dimensions[r].height = 22
        data_toggle = 0
    elif is_header:
        head_style(ws, r, 4, height=26)
        data_toggle = 0
    elif is_sub:
        paint(ws, r, 1, r, 4, f=font(9.5, bold=True, color=NAVY), bg=fill(SOFT),
              al=align("left", "center", True),
              bd=border(bottom=side("thin", RULE)))
        ws.row_dimensions[r].height = 19
        data_toggle = 0
    elif a is not None:
        for cidx in range(1, 5):
            cell = ws.cell(r, cidx)
            horizontal = cell.alignment.horizontal or ("left" if cidx == 1 else "center")
            cell.font = font(9.5, color=INK)
            cell.fill = fill(BAND if data_toggle % 2 else WHITE)
            cell.alignment = align(horizontal, "center", True)
            cell.border = border(bottom=side("thin", RULE))
        ws.row_dimensions[r].height = 16
        AUTO_ROWS.setdefault(ws.title, set()).add(r)
        data_toggle += 1
    else:
        ws.row_dimensions[r].height = 8
        AUTO_ROWS.setdefault(ws.title, set()).add(r)

ws.freeze_panes = "A6"
# Solo se repiten el titulo y el aviso (filas 1-3). Las filas 4-5 contienen la
# primera seccion y su cabecera: repetirlas rotulaba como "Estadisticos
# descriptivos" las paginas de correlaciones, t de Student y Wilcoxon.
print_setup(ws, area=f"A1:D{ws.max_row}", title_rows="1:3")

# 15_NOTAS_TRAZABILIDAD ya fue tratada por SPECS; refuerzo de ancho de notas.
wb["15_NOTAS_TRAZABILIDAD"].column_dimensions["E"].width = 66

# ---------------------------------------------------------------------------
# 4-d. Sincronizacion opcional de rotulos y notas de las Tablas 49 y 50
# ---------------------------------------------------------------------------
veracidad = None
if ARGS.correcciones_veracidad:
    veracidad = sincronizar_rotulos_veracidad(
        wb, _resolve(ARGS.correcciones_veracidad, ROOT))
    print("Rotulos y notas de Tablas 49 y 50 sincronizados con el lote de "
          "veracidad: " + ", ".join(veracidad["hojas"]))

# ---------------------------------------------------------------------------
# 4-ter. Barrido de la raya larga (U+2014) en todo el libro
# ---------------------------------------------------------------------------
GUION_NOTA = "Guion: valor no consignado o no aplicable en la fuente."
barrido_u2014 = {"celdas_corregidas": 0, "incisos_puntuados": 0,
                 "por_hoja": {}, "notas_ampliadas": []}

for ws in wb.worksheets:
    tocadas = 0
    for row in ws.iter_rows():
        for cell in row:
            if not isinstance(cell.value, str) or RAYA_LARGA not in cell.value:
                continue
            if cell.value.strip() == RAYA_LARGA:
                cell.value = "-"
            else:
                cell.value = (cell.value.replace(f" {RAYA_LARGA} ", ", ")
                              .replace(f"{RAYA_LARGA} ", ", ")
                              .replace(f" {RAYA_LARGA}", ",")
                              .replace(RAYA_LARGA, ","))
                barrido_u2014["incisos_puntuados"] += 1
            tocadas += 1
    if not tocadas:
        continue
    barrido_u2014["por_hoja"][ws.title] = tocadas
    barrido_u2014["celdas_corregidas"] += tocadas
    for r in NOTE_ROWS.get(ws.title, []):
        nota = ws.cell(r, 1).value
        if isinstance(nota, str) and nota.startswith("Nota."):
            if GUION_NOTA not in nota:
                ws.cell(r, 1).value = nota.rstrip() + " " + GUION_NOTA
                ancho = (sum(SPECS[ws.title]["widths"]) if ws.title in SPECS
                         else sum((ws.column_dimensions[get_column_letter(i)].width
                                   or 8.43)
                                  for i in range(1, ws.max_column + 1)))
                note_style(ws, r, int(ancho))
                barrido_u2014["notas_ampliadas"].append((ws.title, r))
            break

# ---------------------------------------------------------------------------
# 4-bis. Sincronizacion opcional de la Tabla 51 y hoja de validez reportada
# ---------------------------------------------------------------------------
tabla_51 = None
if ARGS.actualizar_hu:
    filas_hu = leer_tabla_51_docx(SOURCE_DOCX_PATH)
    tabla_51 = sincronizar_tabla_51(wb["08_TABLA_51_HISTORIAS_XP"], filas_hu)
    print(f"Tabla 51 sincronizada desde {SOURCE_DOCX}: "
          f"{tabla_51['filas_docx']} filas.")

if ARGS.hoja_validez:
    agregar_hoja_validez(wb, SOURCE_DOCX, SOURCE_SHA256)

# ---------------------------------------------------------------------------
# 5. Propiedades del libro y guardado con metadatos limpios
# ---------------------------------------------------------------------------
wb.properties.title = (
    f"Tablas de anexos del informe final SIVAC (v{BOOK_VERSION_NUM})")
wb.properties.creator = "analista-estadistico - Squad D"
wb.properties.lastModifiedBy = "analista-estadistico - Squad D"
wb.properties.subject = "Tablas de anexos y resultados estadisticos SIVAC"
wb.properties.description = (
    f"Libro reproducible de tablas de anexos del informe final SIVAC. "
    f"Version {BOOK_VERSION_DOTTED}, generada el {FECHA_GENERACION}. "
    f"Fuente documental: {SOURCE_DOCX} (SHA-256 {SOURCE_SHA256}). "
    f"Bases: pretest_campo.csv y posttest_campo.csv. "
    f"Reporte: reporte_estadistico_completo.json. {MARKER}"
)
wb.properties.keywords = "SIVAC; UNAJMA; APA 7; SPSS"

OUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
wb.save(TMP_XLSX)

# openpyxl escribe su nombre en docProps/app.xml. Se sustituye por metadatos
# neutros para erradicar toda mencion a la herramienta interna de generacion.
CLEAN_APP = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/'
    'extended-properties" xmlns:vt="http://schemas.openxmlformats.org/'
    'officeDocument/2006/docPropsVTypes">'
    '<Application>Microsoft Excel</Application>'
    '<AppVersion>16.0300</AppVersion>'
    '<DocSecurity>0</DocSecurity>'
    '<ScaleCrop>false</ScaleCrop>'
    '<Company>Universidad Nacional Jose Maria Arguedas</Company>'
    '<LinksUpToDate>false</LinksUpToDate>'
    '<SharedDoc>false</SharedDoc>'
    '<HyperlinksChanged>false</HyperlinksChanged>'
    '</Properties>'
)

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"

with zipfile.ZipFile(TMP_XLSX, "r") as zin:
    workbook_xml = ET.fromstring(zin.read("xl/workbook.xml"))
    rels_xml = ET.fromstring(zin.read("xl/_rels/workbook.xml.rels"))
    rid_target = {rel.get("Id"): rel.get("Target") for rel in rels_xml}

    title_to_path = {}
    sheets_el = workbook_xml.find(f"{{{NS_MAIN}}}sheets")
    if sheets_el is not None:
        for sh in sheets_el:
            name = sh.get("name")
            rid = sh.get(f"{{{NS_REL}}}id")
            target = (rid_target.get(rid, "") or "").lstrip("/")
            if target:
                path = target if target.startswith("xl/") else "xl/" + target
                title_to_path[name] = path

    auto_paths = {title_to_path[t]: rows for t, rows in AUTO_ROWS.items()
                  if t in title_to_path}

    def strip_custom_height(xml_text: str, rows: set[int]) -> str:
        """Deja las filas de contenido en altura automatica real.

        No basta con retirar customHeight: mientras subsista ht, Excel conserva
        esa altura como propia y no la recalcula. Se retiran ambos atributos
        para que el ajuste de texto se resuelva al abrir el libro y ninguna
        edicion posterior quede recortada por una altura fija heredada.
        """
        def repl(match):
            tag = match.group(0)
            r_match = re.search(r'\br="(\d+)"', tag)
            if r_match and int(r_match.group(1)) in rows:
                tag = re.sub(r'\s+(?:ht|customHeight)="[^"]*"', "", tag)
            return tag
        return re.sub(r"<row\b[^>]*>", repl, xml_text)

    with zipfile.ZipFile(OUT_XLSX, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "docProps/app.xml":
                data = CLEAN_APP.encode("utf-8")
            elif item.filename in auto_paths:
                xml_text = data.decode("utf-8")
                data = strip_custom_height(xml_text, auto_paths[item.filename]).encode("utf-8")
            zout.writestr(item, data)

TMP_XLSX.unlink(missing_ok=True)

# ---------------------------------------------------------------------------
# 6. Verificaciones de aceptacion
# ---------------------------------------------------------------------------
wbv = openpyxl.load_workbook(OUT_XLSX)

VALIDITY_SHEET = "16_VALIDEZ_REPORTADA"
SPSS_TITLE = "RESULTADOS CON PRESENTACIÓN TIPO SPSS - SIVAC (n = 14)"
SPSS_SOURCE = ("Cálculos elaborados con Python; presentación tipo SPSS; "
               "datos de prueba.")
rotulo_spss = None
if "14_SPSS_SALIDAS" in wbv.sheetnames:
    _ws14 = wbv["14_SPSS_SALIDAS"]
    rotulo_spss = {
        "titulo": _ws14.cell(1, 1).value,
        "fuente": _ws14.cell(2, 1).value,
        "titulo_ok": _ws14.cell(1, 1).value == SPSS_TITLE,
        "fuente_ok": _ws14.cell(2, 1).value == SPSS_SOURCE,
    }
    if not (rotulo_spss["titulo_ok"] and rotulo_spss["fuente_ok"]):
        OUT_XLSX.unlink(missing_ok=True)
        raise SystemExit(
            "[ERROR] El rotulo de 14_SPSS_SALIDAS no declara la presentacion "
            "tipo SPSS con calculos en Python. Se elimino la salida.")

# 6.1 Paridad numerica exacta contra la base
numeric_after = {}
for ws in wbv.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, (int, float)) and not isinstance(cell.value, bool):
                numeric_after[(ws.title, cell.coordinate)] = cell.value

mismatches = []
for key, before in numeric_before.items():
    after = numeric_after.get(key, "__MISSING__")
    if after == "__MISSING__" or float(after) != float(before):
        mismatches.append((key, before, after))

extra = [k for k in numeric_after if k not in numeric_before]
extra_estadisticas = [k for k in extra if k[0] != VALIDITY_SHEET]
extra_validez = [k for k in extra if k[0] == VALIDITY_SHEET]

# 6.2 Paridad numerica contra el libro de referencia (v3 por defecto)
ref_mismatches, ref_extra, ref_extra_validez = [], [], []
if REF_XLSX is not None:
    wbr = openpyxl.load_workbook(REF_XLSX)
    numeric_ref = {}
    for ws in wbr.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, (int, float)) and not isinstance(cell.value, bool):
                    numeric_ref[(ws.title, cell.coordinate)] = cell.value
    for key, value in numeric_ref.items():
        after = numeric_after.get(key, "__MISSING__")
        if after == "__MISSING__" or float(after) != float(value):
            ref_mismatches.append((key, value, after))
    ref_new = [k for k in numeric_after if k not in numeric_ref]
    ref_extra = [k for k in ref_new if k[0] != VALIDITY_SHEET]
    ref_extra_validez = [k for k in ref_new if k[0] == VALIDITY_SHEET]

paridad_exacta = not mismatches and not extra_estadisticas and not ref_mismatches and not ref_extra

# 6.3 Texto: herramienta interna, fuente obsoleta, doble punto, avisos
text_hits = {"openpyxl": [], "fuente_obsoleta": [], "doble_punto": [],
             "etiquetas_internas": [], "raya_larga": []}
marker_count = {}
for ws in wbv.worksheets:
    count = 0
    for row in ws.iter_rows():
        for cell in row:
            if not isinstance(cell.value, str):
                continue
            text = cell.value
            if "openpyxl" in text.lower():
                text_hits["openpyxl"].append((ws.title, cell.coordinate, text[:80]))
            stale = STALE_SOURCE.search(text)
            if (stale and SOURCE_DOC_VERSION_NUM
                    and stale.group(1) != SOURCE_DOC_VERSION_NUM):
                text_hits["fuente_obsoleta"].append(
                    (ws.title, cell.coordinate, text[:80]))
            if ".." in text:
                text_hits["doble_punto"].append((ws.title, cell.coordinate, text[:80]))
            if re.search(r"\bQG-?\d+\b", text) or re.search(r"\bDEC-\d+\b", text):
                text_hits["etiquetas_internas"].append(
                    (ws.title, cell.coordinate, text[:80]))
            if RAYA_LARGA in text:
                text_hits["raya_larga"].append(
                    (ws.title, cell.coordinate, text[:80]))
            count += text.count(MARKER)
    marker_count[ws.title] = count

# 6.4 Recalculo real de la cache si el libro contiene formulas
formulas_escritas = contar_formulas(wbv)
recalc = {"formulas": formulas_escritas, "estado": "no aplica"}
if formulas_escritas:
    if not ARGS.recalcular:
        OUT_XLSX.unlink(missing_ok=True)
        raise SystemExit(
            "[ERROR] El libro contiene formulas y no se solicito --recalcular. "
            "Se elimino la salida para no entregar caches vacias.")
    recalc = recalcular_con_excel(OUT_XLSX)
    recalc["formulas"] = formulas_escritas
    if recalc["estado"] != "recalculado":
        OUT_XLSX.unlink(missing_ok=True)
        raise SystemExit(
            f"[ERROR] No se pudo recalcular la cache: {recalc.get('motivo')}. "
            "Se elimino la salida.")
    wbc = openpyxl.load_workbook(OUT_XLSX, data_only=True)
    if VALIDITY_SHEET in wbc.sheetnames:
        hoja = wbc[VALIDITY_SHEET]
        cache = {c: hoja[c].value for c in ("B11", "B12")}
        cache_ok = all(isinstance(v, (int, float)) and abs(float(v) - 1.0) < 1e-9
                       for v in cache.values())
        recalc["valores_cache"] = {
            k: (float(v) if isinstance(v, (int, float)) else v)
            for k, v in cache.items()}
        recalc["cache_verificada"] = cache_ok
        if not cache_ok:
            OUT_XLSX.unlink(missing_ok=True)
            raise SystemExit(
                "[ERROR] La cache recalculada no devuelve 1.000 en B11/B12. "
                "Se elimino la salida.")
    errores_formula = []
    for hoja_c in wbc.worksheets:
        for row in hoja_c.iter_rows():
            for cell in row:
                valor = cell.value
                if isinstance(valor, str) and valor.startswith("#"):
                    errores_formula.append(
                        (hoja_c.title, cell.coordinate, valor))
    recalc["errores_formula"] = len(errores_formula)
    recalc["error_summary"] = [list(e) for e in errores_formula[:20]]
    if errores_formula:
        OUT_XLSX.unlink(missing_ok=True)
        raise SystemExit(
            f"[ERROR] El recalculado dejo {len(errores_formula)} celdas con "
            "error de formula. Se elimino la salida.")

# 6.5 Integridad de los insumos y huella de la salida
sha = sha256_file(OUT_XLSX)
size = OUT_XLSX.stat().st_size
base_intacta = sha256_file(IN_XLSX) == BASE_SHA256
ref_intacta = (sha256_file(REF_XLSX) == REF_SHA256) if REF_XLSX is not None else None

# 6.6 Reporte de paridad en JSON
paridad = {
    "metadata": {
        "generado": datetime.datetime.now().isoformat(timespec="seconds"),
        "fecha_declarada": FECHA_GENERACION,
        "version_libro": BOOK_VERSION_DOTTED,
        "script": "scripts/estadistica/build_tablas_anexos_v3.py",
        "interprete": f"Python {sys.version.split()[0]}",
        "argumentos": {
            "--fuente-docx": ARGS.fuente_docx,
            "--base-xlsx": ARGS.base_xlsx,
            "--salida": ARGS.salida,
            "--referencia-paridad": ARGS.referencia_paridad,
            "--actualizar-hu": ARGS.actualizar_hu,
            "--correcciones-veracidad": ARGS.correcciones_veracidad,
            "--hoja-validez": ARGS.hoja_validez,
            "--recalcular": ARGS.recalcular,
        },
    },
    "fuente_docx": {
        "nombre": SOURCE_DOCX,
        "ruta": str(SOURCE_DOCX_PATH),
        "bytes": SOURCE_SIZE,
        "sha256": SOURCE_SHA256,
    },
    "base_xlsx": {"ruta": str(IN_XLSX), "sha256": BASE_SHA256},
    "salida_xlsx": {
        "ruta": str(OUT_XLSX),
        "sha256": sha,
        "bytes": size,
        "hojas": wbv.sheetnames,
    },
    "referencia_paridad": (
        {"ruta": str(REF_XLSX), "sha256": REF_SHA256} if REF_XLSX else None),
    "paridad_numerica": {
        "contra_base": {
            "celdas_comparadas": len(numeric_before),
            "discrepancias": [list(map(str, m)) for m in mismatches],
            "celdas_nuevas_estadisticas": [list(k) for k in extra_estadisticas],
            "celdas_nuevas_hoja_validez": [list(k) for k in extra_validez],
        },
        "contra_referencia": {
            "celdas_comparadas": len(numeric_ref) if REF_XLSX else 0,
            "discrepancias": [list(map(str, m)) for m in ref_mismatches],
            "celdas_nuevas_estadisticas": [list(k) for k in ref_extra],
            "celdas_nuevas_hoja_validez": [list(k) for k in ref_extra_validez],
        },
        "resultado": "EXACTA" if paridad_exacta else "FALLA",
    },
    "tabla_51": tabla_51,
    "hoja_validez": (
        {
            "hoja": VALIDITY_SHEET,
            "formulas": ["B11", "B12"],
            "imputa_n": False,
            "matriz_por_juez": False,
            "escala": "matriz VD de 12 componentes, ordinal 1-4",
            "no_es": "cuestionario TAM de 8 reactivos, Likert 1-5",
            "leyenda": (
                "Resultados calculados a partir de calificaciones comunicadas "
                "por el tesista. Pendientes de cotejo con las fichas originales."),
        } if ARGS.hoja_validez else None),
    "recalculo": recalc,
    "texto": {
        "menciones_openpyxl": len(text_hits["openpyxl"]),
        "fuente_obsoleta": [list(t) for t in text_hits["fuente_obsoleta"]],
        "dobles_puntos": len(text_hits["doble_punto"]),
        "etiquetas_internas": [list(t) for t in text_hits["etiquetas_internas"]],
        "raya_larga_restante": [list(t) for t in text_hits["raya_larga"]],
        "avisos_por_hoja": {k: v for k, v in marker_count.items() if v},
        "aviso_de_datos": MARKER,
    },
    "barrido_u2014": barrido_u2014,
    "rotulo_spss_salidas": rotulo_spss,
    "veracidad_rotulos": veracidad,
    "portada": {
        "paginas": 2,
        "motivo": ("Portada institucional y trazabilidad de la fuente; "
                   "salto de pagina intencional en la fila 26."),
    },
    "verificacion_de_ejecucion": {
        "codigo_salida": 0,
        "base_intacta": base_intacta,
        "referencia_intacta": ref_intacta,
        "hoja_de_validez_escrita": ARGS.hoja_validez,
        "tabla_51_sincronizada": tabla_51 is not None,
        "rotulos_veracidad_sincronizados": veracidad is not None,
        "rotulo_spss_salidas_ok": bool(rotulo_spss and rotulo_spss["titulo_ok"]
                                       and rotulo_spss["fuente_ok"]),
        "errores_formula": recalc.get("errores_formula", 0),
        "paginas_impresion_totales": recalc.get("paginas_totales"),
        "raya_larga_restante": len(text_hits["raya_larga"]),
    },
}
paridad_path = (
    _resolve(ARGS.reporte_paridad, ROOT / "salidas" / "estadistica")
    if ARGS.reporte_paridad
    else OUT_XLSX.with_name(f"paridad_{OUT_XLSX.stem}.json"))
paridad_path.parent.mkdir(parents=True, exist_ok=True)
paridad_path.write_text(json.dumps(paridad, ensure_ascii=False, indent=2),
                        encoding="utf-8")

print("=" * 78)
print(OUT_XLSX.name)
print("=" * 78)
print(f"Archivo            : {OUT_XLSX}")
print(f"Tamano             : {size:,} bytes")
print(f"SHA-256            : {sha}")
print(f"Fuente DOCX        : {SOURCE_DOCX}")
print(f"SHA-256 fuente     : {SOURCE_SHA256}")
print(f"Hojas              : {len(wbv.sheetnames)}")
print(f"Celdas numericas   : {len(numeric_before)} comparadas; "
      f"{len(mismatches)} discrepancias; {len(extra_estadisticas)} celdas nuevas")
if extra_validez:
    print(f"  Hoja de validez  : {len(extra_validez)} celdas numericas nuevas "
          "(fuera de las columnas estadisticas)")
print(f"Paridad referencia : {len(ref_mismatches)} discrepancias; "
      f"{len(ref_extra)} celdas nuevas"
      if REF_XLSX else "Paridad referencia : omitida")
print(f"Coincidencia       : {'EXACTA' if paridad_exacta else 'FALLA'}")
print(f"Menciones openpyxl : {len(text_hits['openpyxl'])}")
print(f"Fuente obsoleta    : {len(text_hits['fuente_obsoleta'])}")
print(f"Dobles puntos      : {len(text_hits['doble_punto'])}")
print(f"Etiquetas internas : {len(text_hits['etiquetas_internas'])}")
print(f"Raya U+2014        : {len(text_hits['raya_larga'])}")
print(f"Rotulo SPSS        : "
      f"{'OK' if rotulo_spss and rotulo_spss['titulo_ok'] and rotulo_spss['fuente_ok'] else 'FALLA'}")
print(f"Barrido U+2014     : {barrido_u2014['celdas_corregidas']} celdas; "
      f"{barrido_u2014['incisos_puntuados']} incisos; "
      f"notas ampliadas {len(barrido_u2014['notas_ampliadas'])}")
print(f"Recalculo          : {recalc['estado']} "
      f"({recalc.get('motor', 'sin formulas')})")
if "cache_verificada" in recalc:
    print(f"Cache B11/B12      : {recalc['valores_cache']} "
          f"({'OK' if recalc['cache_verificada'] else 'FALLA'})")
    print(f"Errores de formula : {recalc.get('errores_formula', 0)}")
    print(f"Paginas impresion  : {recalc.get('paginas_totales', 'n/d')}")
print(f"Reporte de paridad : {paridad_path}")
print("Avisos por hoja    : " + ", ".join(
    f"{k}={v}" for k, v in marker_count.items() if v))
for label in ("openpyxl", "fuente_obsoleta", "doble_punto",
              "etiquetas_internas", "raya_larga"):
    for item in text_hits[label][:10]:
        print(f"  [{label}] {item}")
for item in mismatches[:20]:
    print(f"  [num base] {item}")
for item in ref_mismatches[:20]:
    print(f"  [num ref] {item}")
print("=" * 78)
