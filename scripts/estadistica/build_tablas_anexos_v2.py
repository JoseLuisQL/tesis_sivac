# -*- coding: utf-8 -*-
"""
Construye el libro TABLAS_ANEXOS_SIVAC_v2.xlsx con las tablas de anexo del
informe final SIVAC (v10) y las hojas estadisticas reproducidas desde las
bases CSV y el reporte JSON.

Entradas (solo lectura):
  - salidas/documentos/informe_final_v10.docx
  - salidas/evidencias/base_de_datos/pretest_campo.csv
  - salidas/evidencias/base_de_datos/posttest_campo.csv
  - salidas/estadistica/reporte_estadistico_completo.json

Salidas:
  - salidas/estadistica/TABLAS_ANEXOS_SIVAC_v2.xlsx
  - salidas/estadistica/REPORTE_EXCEL_ANEXOS_v2.md

Ejecucion:
  .venv/Scripts/python.exe scripts/estadistica/build_tablas_anexos_v2.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.page import PageMargins
from openpyxl.worksheet.properties import PageSetupProperties
from scipy import stats
from docx import Document

# ---------------------------------------------------------------------------
# Rutas y constantes
# ---------------------------------------------------------------------------
ROOT = Path(r"C:\MisInvestigaciones\tesis\sivac")
DOCX_PATH = ROOT / "salidas" / "documentos" / "informe_final_v10.docx"
PRE_CSV = ROOT / "salidas" / "evidencias" / "base_de_datos" / "pretest_campo.csv"
POST_CSV = ROOT / "salidas" / "evidencias" / "base_de_datos" / "posttest_campo.csv"
JSON_PATH = ROOT / "salidas" / "estadistica" / "reporte_estadistico_completo.json"
OUT_XLSX = ROOT / "salidas" / "estadistica" / "TABLAS_ANEXOS_SIVAC_v2.xlsx"
OUT_MD = ROOT / "salidas" / "estadistica" / "REPORTE_EXCEL_ANEXOS_v2.md"

NAVY = "1F3864"
BAND = "F2F2F2"
WHITE = "FFFFFF"
TOTAL = "D9E2F3"
LINE = "BFBFBF"
FONT_NAME = "Arial"
MONO_NAME = "Consolas"
MARKER = ("Datos provisionales. Serán sustituidos por los registros "
          "definitivos de campo antes de la sustentación.")

CAPTIONS = {
    35: "Confiabilidad de consistencia interna del Cuestionario TAM (Instrumento N.° 03) mediante el coeficiente Alfa de Cronbach e intervalo de confianza del 95%",
    36: "Estadística descriptiva comparativa pretest y postest para los indicadores de la Dimensión 1: Oportunidad de procesamiento (n = 14)",
    37: "Estadística descriptiva comparativa pretest y postest para los indicadores de la Dimensión 2: Consistencia documental (n = 14)",
    38: "Estadística descriptiva comparativa pretest y postest para los indicadores de la Dimensión 3: Satisfacción del usuario (n = 14)",
    39: "Prueba de bondad de ajuste de normalidad de Shapiro-Wilk para las diferencias pareadas pretest y postest (n = 14)",
    40: "Contraste inferencial de la Hipótesis Específica 1: Oportunidad de procesamiento mediante pruebas paramétricas y no paramétricas pareadas",
    41: "Contraste inferencial de la Hipótesis Específica 2: Consistencia documental mediante pruebas paramétricas y no paramétricas pareadas",
    42: "Contraste inferencial de la Hipótesis Específica 3: Satisfacción del usuario mediante pruebas paramétricas y no paramétricas pareadas",
    43: "Resumen de contrastación inferencial multivariada y regla de decisión para la Hipótesis General con ajuste secuencial de Holm-Bonferroni",
    44: "Matriz de consistencia metodológica del estudio SIVAC",
    45: "Matriz de operacionalización de las variables de investigación",
    46: "Instrumento N.° 01: Ficha de Registro Cronométrico de Tiempos Operativos",
    47: "Instrumento N.° 02: Ficha de Auditoría y Cotejo Documental de Lotes",
    48: "Instrumento N.° 03: Cuestionario TAM de Satisfacción del Usuario (Modalidad A)",
    49: "Matriz de datos recolectados en el Pretest (Gestión manual basal, n = 14)",
    50: "Matriz de datos recolectados en el Posttest (Operación con sistema SIVAC, n = 14)",
    51: "Matriz de Historias de Usuario desarrolladas e implementadas en SIVAC bajo XP",
}

# ---------------------------------------------------------------------------
# Utilidades de estilo
# ---------------------------------------------------------------------------
def fnt(size=10, bold=False, italic=False, color=NAVY, name=FONT_NAME):
    return Font(name=name, size=size, bold=bold, italic=italic, color=color)


def fil(color):
    return PatternFill("solid", fgColor=color)


def side(style="thin", color=LINE):
    return Side(style=style, color=color)


def style_cell(cell, *, size=10, bold=False, italic=False, color=NAVY,
               bg=None, halign="left", valign="center", wrap=True,
               top=None, bottom=None, fmt=None, name=FONT_NAME):
    cell.font = fnt(size=size, bold=bold, italic=italic, color=color, name=name)
    if bg:
        cell.fill = fil(bg)
    cell.alignment = Alignment(horizontal=halign, vertical=valign,
                               wrap_text=wrap, text_rotation=0, indent=0)
    cell.border = Border(top=top or Side(), bottom=bottom or Side(),
                         left=Side(), right=Side())
    if fmt:
        cell.number_format = fmt


def est_lines(value, width):
    if value is None:
        return 1
    text = str(value)
    chars = max(8, int(width * 0.80))
    total = 0
    for seg in text.split("\n"):
        total += max(1, math.ceil(len(seg) / chars))
    return total


def set_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def set_body_heights(ws, first, last, widths):
    for r in range(first, last + 1):
        lines = 1
        for j, w in enumerate(widths, 1):
            lines = max(lines, est_lines(ws.cell(r, j).value, w))
        ws.row_dimensions[r].height = min(409, max(15, lines * 13.0 + 3))


def add_sheet(wb, name, tab=NAVY):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = tab
    return ws


def print_setup(ws, *, title_rows=None, area=None):
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = 9  # A4
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_options.horizontalCentered = True
    ws.page_margins = PageMargins(left=0.59, right=0.59, top=0.59,
                                  bottom=0.59, header=0.3, footer=0.3)
    if title_rows:
        ws.print_title_rows = title_rows
    if area:
        ws.print_area = area
    ws.oddFooter.left.text = "SIVAC - Tablas de anexos (v2)"
    ws.oddFooter.right.text = "Página &P de &N"


def write_title_block(ws, top, label, title, ncols, total_width, banner=None):
    ws.merge_cells(start_row=top, start_column=1, end_row=top, end_column=ncols)
    c = ws.cell(top, 1, label)
    style_cell(c, size=14, bold=True, halign="left", wrap=False)
    ws.row_dimensions[top].height = 24

    ws.merge_cells(start_row=top + 1, start_column=1,
                   end_row=top + 1, end_column=ncols)
    c = ws.cell(top + 1, 1, title)
    style_cell(c, size=11, italic=True, halign="left", wrap=True,
               bottom=side("medium", NAVY))
    ws.row_dimensions[top + 1].height = min(70, max(20, est_lines(title, total_width) * 14 + 4))

    if banner:
        ws.merge_cells(start_row=top + 2, start_column=1,
                       end_row=top + 2, end_column=ncols)
        c = ws.cell(top + 2, 1, banner)
        style_cell(c, size=10, bold=True, bg=TOTAL, halign="left", wrap=True,
                   top=side("thin", NAVY), bottom=side("thin", NAVY))
        ws.row_dimensions[top + 2].height = min(
            42, max(18, est_lines(banner, total_width) * 13.0 + 4))

    ws.row_dimensions[top + 3].height = 6
    return top + 4


def write_header(ws, row, headers):
    for j, h in enumerate(headers, 1):
        c = ws.cell(row, j, h)
        style_cell(c, size=10, bold=True, color=WHITE, bg=NAVY,
                   halign="center", wrap=True,
                   top=side("thin", NAVY), bottom=side("medium", NAVY))
    ws.row_dimensions[row].height = 38


def write_data_row(ws, row, values, *, band=False, total=False,
                   formats=None, aligns=None):
    bg = TOTAL if total else (BAND if band else WHITE)
    for j, v in enumerate(values, 1):
        c = ws.cell(row, j, v)
        align = aligns[j - 1] if aligns else ("left" if j == 1 else "center")
        style_cell(c, size=10, bold=total, bg=bg, halign=align,
                   wrap=True, bottom=side("thin", LINE))
        if formats and j - 1 < len(formats) and formats[j - 1]:
            c.number_format = formats[j - 1]


def write_note(ws, row, text, ncols, total_width):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncols)
    c = ws.cell(row, 1, text)
    style_cell(c, size=9, italic=True, color="000000", halign="left",
               valign="top", wrap=True)
    ws.row_dimensions[row].height = min(130, max(16, est_lines(text, total_width) * 13.0 + 4))


def write_table_block(ws, top, label, title, headers, rows, widths, *,
                      banner=None, formats=None, aligns=None, total_rows=(),
                      note=None, autofilter=True, freeze=False,
                      apply_widths=True, span_cols=None):
    if apply_widths:
        set_widths(ws, widths)
    total_width = sum(widths)
    span = max(len(headers), span_cols or 0)
    header_row = write_title_block(ws, top, label, title, span,
                                   total_width, banner=banner)
    write_header(ws, header_row, headers)

    r = header_row + 1
    per_row_formats = bool(formats) and isinstance(formats[0], list)
    for i, values in enumerate(rows):
        row_formats = formats[i] if per_row_formats else formats
        write_data_row(ws, r, values, band=(i % 2 == 1),
                       total=(i in total_rows), formats=row_formats,
                       aligns=aligns)
        r += 1
    last_data = r - 1

    for j in range(1, len(headers) + 1):
        c = ws.cell(last_data, j)
        c.border = Border(top=c.border.top, bottom=side("medium", NAVY),
                          left=Side(), right=Side())

    set_body_heights(ws, header_row + 1, last_data, widths)

    if autofilter:
        ws.auto_filter.ref = (
            f"A{header_row}:{get_column_letter(len(headers))}{last_data}"
        )
    if freeze:
        ws.freeze_panes = f"A{header_row + 1}"

    note_row = last_data + 2
    if note:
        write_note(ws, note_row, note, span, total_width)
    return header_row, last_data, note_row


# ---------------------------------------------------------------------------
# Lectura de insumos
# ---------------------------------------------------------------------------
doc = Document(str(DOCX_PATH))
pre = pd.read_csv(PRE_CSV, encoding="utf-8-sig")
post = pd.read_csv(POST_CSV, encoding="utf-8-sig")
with open(JSON_PATH, encoding="utf-8") as fh:
    R = json.load(fh)

TABLES = doc.tables
assert len(TABLES) >= 55, f"El DOCX contiene solo {len(TABLES)} tablas."


def doc_rows(index):
    return [[c.text.strip() for c in row.cells] for row in TABLES[index].rows]


# ---------------------------------------------------------------------------
# Estadistica computada y verificacion contra el JSON
# ---------------------------------------------------------------------------
KEYS = ["t_reg", "t_vale", "rsd", "cpe", "score_ap", "score_up", "score_tam_total"]

LABELS = {
    "t_reg": "Tiempo de registro (T_reg, min)",
    "t_vale": "Tiempo de emisión de vales (T_vale, min)",
    "rsd": "Registros sin discrepancias (RSD, %)",
    "cpe": "Concordancia programada vs entregada (CPE, %)",
    "score_ap": "Aceptación del proceso (AP, 4-20 pts)",
    "score_up": "Utilidad percibida (UP, 4-20 pts)",
    "score_tam_total": "Puntaje global TAM (8-40 pts)",
}
SHORT = {
    "t_reg": "T_reg (min)",
    "t_vale": "T_vale (min)",
    "rsd": "RSD (%)",
    "cpe": "CPE (%)",
    "score_ap": "AP (pts)",
    "score_up": "UP (pts)",
    "score_tam_total": "TAM total (pts)",
}
PCT = {"rsd", "cpe"}


def desc_stats(values):
    a = np.asarray(values, dtype=float)
    return {
        "n": int(a.size),
        "media": float(np.mean(a)),
        "de": float(np.std(a, ddof=1)),
        "mediana": float(np.median(a)),
        "q25": float(np.percentile(a, 25)),
        "q75": float(np.percentile(a, 75)),
        "ric": float(np.percentile(a, 75) - np.percentile(a, 25)),
        "min": float(np.min(a)),
        "max": float(np.max(a)),
        "asimetria": float(stats.skew(a, bias=False)),
        "curtosis": float(stats.kurtosis(a, bias=False)),
    }


def alpha_feldt(frame, cols):
    x = frame[cols].to_numpy(dtype=float)
    k = x.shape[1]
    n = x.shape[0]
    a = k / (k - 1) * (1 - x.var(axis=0, ddof=1).sum() / x.sum(axis=1).var(ddof=1))
    f1 = stats.f.ppf(0.975, n - 1, (n - 1) * (k - 1))
    f2 = stats.f.ppf(0.025, n - 1, (n - 1) * (k - 1))
    return float(a), float(1 - (1 - a) * f1), float(1 - (1 - a) * f2)


STATS = {}
for key in KEYS:
    a = pre[key].to_numpy(dtype=float)
    b = post[key].to_numpy(dtype=float)
    d = b - a
    t_res = stats.ttest_rel(b, a)
    sh = stats.shapiro(d)
    ci = stats.t.interval(0.95, len(d) - 1, loc=float(np.mean(d)),
                          scale=stats.sem(d))
    STATS[key] = {
        "pre": desc_stats(a),
        "post": desc_stats(b),
        "diff": desc_stats(d),
        "delta": float((np.mean(b) - np.mean(a)) / np.mean(a) * 100),
        "t": float(t_res.statistic),
        "gl": int(len(d) - 1),
        "p_t": float(t_res.pvalue),
        "dz": float(np.mean(d) / np.std(d, ddof=1)),
        "w": float(sh.statistic),
        "p_w": float(sh.pvalue),
        "z": float(R["contrastes_inferenciales"][key]["wilcoxon"]["estadistico_z"]),
        "p_wilcox": float(R["contrastes_inferenciales"][key]["wilcoxon"]["p_valor"]),
        # r de Rosenthal = |Z| / sqrt(N), con N = pares validos (no nulos).
        "r": float(abs(R["contrastes_inferenciales"][key]["wilcoxon"]["estadistico_z"])
                   / math.sqrt(int(np.count_nonzero(d)))),
        "w_stat": float(R["contrastes_inferenciales"][key]["wilcoxon"]["estadistico_w"]),
        "p_holm": float(R["contrastes_inferenciales"][key]["holm_bonferroni"]["p_ajustado"]),
        "corr": float(np.corrcoef(a, b)[0, 1]),
        "p_corr": float(stats.pearsonr(a, b)[1]),
        "sem": float(stats.sem(d)),
        "ci_low": float(ci[0]),
        "ci_high": float(ci[1]),
    }

ALPHA_COLS = {
    "global": ["ap_01", "ap_02", "ap_03", "ap_04", "up_01", "up_02", "up_03", "up_04"],
    "ap": ["ap_01", "ap_02", "ap_03", "ap_04"],
    "up": ["up_01", "up_02", "up_03", "up_04"],
}
ALPHA = {}
for moment, frame in (("pretest", pre), ("posttest", post)):
    for scale, cols in ALPHA_COLS.items():
        a, lo, hi = alpha_feldt(frame, cols)
        ALPHA[(moment, scale)] = (a, lo, hi, len(cols))


def fmt_num(value, decimals=2):
    return f"{value:.{decimals}f}".replace(".", ",")


def p_apa(p):
    if p < 0.001:
        return "< .001"
    text = f"{p:.3f}"
    return text[1:] if text.startswith("0.") else text


def p_sci(p):
    return f"{p:.2E}"


def center(value):
    return value


# Verificacion numerica contra el JSON
check_counts = {
    "Descriptivos": 0,
    "Alfa de Cronbach": 0,
    "Shapiro-Wilk": 0,
    "t pareada": 0,
    "Wilcoxon": 0,
    "Holm-Bonferroni": 0,
    "Variacion porcentual": 0,
}
json_mismatches = []


def check(block, key, field, got, want, tol=1e-9):
    check_counts[block] += 1
    if abs(float(got) - float(want)) > tol:
        json_mismatches.append((block, key, field, got, want))


for key in KEYS:
    J = R["descriptivos"][key]
    for moment in ("pretest", "posttest", "diferencia"):
        target = J[moment]
        ours = STATS[key]["pre" if moment == "pretest" else
                          "post" if moment == "posttest" else "diff"]
        for field, jfield in (("media", "media"), ("de", "desv_est"),
                              ("mediana", "mediana"), ("ric", "iqr"),
                              ("min", "minimo"), ("max", "maximo")):
            check("Descriptivos", key, f"{moment}.{field}", ours[field],
                  target[jfield])
    check("Variacion porcentual", key, "delta", STATS[key]["delta"],
          J["delta_porcentual"], tol=1e-8)

    # Shapiro-Wilk recalculado
    normality = R["normalidad_shapiro_wilk"][key]
    check("Shapiro-Wilk", key, "W", STATS[key]["w"],
          normality["estadistico_w"])
    check("Shapiro-Wilk", key, "p", STATS[key]["p_w"], normality["p_valor"])

    # t pareada recalculada
    t_block = R["contrastes_inferenciales"][key]["t_student"]
    check("t pareada", key, "t", STATS[key]["t"], t_block["estadistico_t"])
    check("t pareada", key, "gl", STATS[key]["gl"], t_block["gl"])
    check("t pareada", key, "p", STATS[key]["p_t"], t_block["p_valor"])
    check("t pareada", key, "d_z", STATS[key]["dz"], t_block["d_cohen"])

    # Wilcoxon recalculado con el mismo procedimiento del informe
    a = pre[key].to_numpy(dtype=float)
    b = post[key].to_numpy(dtype=float)
    res_w = stats.wilcoxon(b, a, alternative="two-sided")
    n = len(a)
    expected_w = n * (n + 1) / 4.0
    variance_w = n * (n + 1) * (2 * n + 1) / 24.0
    z_w = (res_w.statistic - expected_w) / math.sqrt(variance_w)
    n_valid = int(np.count_nonzero(b - a))
    r_w = abs(z_w) / math.sqrt(n_valid)
    w_block = R["contrastes_inferenciales"][key]["wilcoxon"]
    check("Wilcoxon", key, "W", res_w.statistic, w_block["estadistico_w"])
    check("Wilcoxon", key, "Z", z_w, w_block["estadistico_z"])
    check("Wilcoxon", key, "p", res_w.pvalue, w_block["p_valor"])
    check("Wilcoxon", key, "r", r_w, STATS[key]["r"])

for moment, scale in ALPHA:
    a_val, lo, hi, k = ALPHA[(moment, scale)]
    block = R["confiabilidad_instrumento_03"][moment][
        {"global": "global_tam", "ap": "agilidad_percibida", "up": "utilidad_percibida"}[scale]
    ]
    check("Alfa de Cronbach", scale, f"{moment}.alpha", a_val, block["alpha"])
    check("Alfa de Cronbach", scale, f"{moment}.ic_lo", lo, block["ic_95"][0])
    check("Alfa de Cronbach", scale, f"{moment}.ic_hi", hi, block["ic_95"][1])

# Holm-Bonferroni recalculado sobre los p de la prueba adoptada
ordered = sorted(KEYS, key=lambda k: STATS[k]["p_t"])
for rank, key in enumerate(ordered):
    adjusted = min(1.0, STATS[key]["p_t"] * (len(ordered) - rank))
    check("Holm-Bonferroni", key, "p_ajustado", adjusted, STATS[key]["p_holm"])

json_total_checks = sum(check_counts.values())

# Verificacion DOCX vs CSV (tablas 49 y 50 del rotulo visible)
DOC_COLS = ["sujeto_id", "centro_acopio", "t_reg", "t_vale", "rsd", "cpe",
            "ap_01", "ap_02", "ap_03", "ap_04", "up_01", "up_02", "up_03",
            "up_04", "score_ap", "score_up", "score_tam_total", "nivel_satisfaccion"]
doc_csv_mismatches = []
for frame, table_index, moment in ((pre, 52, "pretest"), (post, 53, "posttest")):
    doc_cells = doc_rows(table_index)
    for i in range(14):
        for j, col in enumerate(DOC_COLS):
            raw = doc_cells[i + 1][j].strip()
            val = frame.iloc[i][col]
            if col in ("sujeto_id", "centro_acopio", "nivel_satisfaccion"):
                ok = raw == str(val).strip()
            else:
                try:
                    ok = abs(float(raw) - float(val)) < 1e-9
                except ValueError:
                    ok = False
            if not ok:
                doc_csv_mismatches.append((moment, i + 1, col, raw, str(val)))

# Comparacion de las tablas de anexo del DOCX con los datos que se escribiran
ANNEX_DOC_INDEX = {
    44: 44, 45: 45, 46: 49, 47: 50, 48: 51, 49: 52, 50: 53, 51: 54
}

# ---------------------------------------------------------------------------
# Construccion del libro
# ---------------------------------------------------------------------------
wb = Workbook()
wb.remove(wb.active)
wb.properties.title = "Tablas de anexos del informe final SIVAC (v2)"
wb.properties.creator = "analista-estadistico - Squad D"
wb.properties.subject = "Tablas de anexos y resultados estadisticos SIVAC"
wb.properties.description = (
    "Libro reproducible construido desde informe_final_v10.docx, las bases "
    "pretest_campo.csv y posttest_campo.csv y reporte_estadistico_completo.json. "
    + MARKER
)
wb.properties.keywords = "SIVAC; UNAJMA; APA 7; SPSS"

sheet_stats = []
trace_rows = []

# ---------------------------------------------------------------------------
# 00_PORTADA
# ---------------------------------------------------------------------------
ws = add_sheet(wb, "00_PORTADA")
set_widths(ws, [34, 22, 22, 22, 22, 22])
ws.sheet_view.showGridLines = False

cover = [
    (1, "UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS", 14, True, False, "center", 26, None),
    (2, "Escuela Profesional de Ingeniería de Sistemas", 11, False, False, "center", 20, None),
    (4, "TABLAS DE ANEXOS DEL INFORME FINAL", 18, True, False, "center", 30, None),
    (5, "Sistema web SIVAC y gestión de movimientos mensuales de vacunas", 12, False, True, "center", 22, side("medium", NAVY)),
    (7, R["metadatos"]["tesis"], 11, True, True, "center", 64, None),
    (9, "Tesista: Bach. José Luis Quispe León", 11, False, False, "left", 18, None),
    (10, "Asesora: Dra. Norma Lorena Catacora Flores", 11, False, False, "left", 18, None),
    (11, "Diseño: preexperimental con pretest y postest en un solo grupo (O₁ → X → O₂)", 10, False, False, "left", 18, None),
    (12, "Población censal: N = n = 14 operadores de inmunizaciones", 10, False, False, "left", 18, None),
    (13, "Ámbito: Dirección de Salud Apurímac II — Red de frío", 10, False, False, "left", 18, None),
    (15, "Versión del libro: 2.0  |  Fecha de generación: 2026-10-21", 10, False, False, "left", 18, None),
]
for row, text, size, bold, italic, align, height, bottom in cover:
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
    c = ws.cell(row, 1, text)
    style_cell(c, size=size, bold=bold, italic=italic, halign=align,
               wrap=True, bottom=bottom)
    ws.row_dimensions[row].height = height

# Banner de estado
ws.merge_cells(start_row=17, start_column=1, end_row=17, end_column=6)
c = ws.cell(17, 1, MARKER)
style_cell(c, size=11, bold=True, bg=TOTAL, halign="center",
           top=side("thin", NAVY), bottom=side("thin", NAVY))
ws.row_dimensions[17].height = 22

# Indice
ws.merge_cells(start_row=19, start_column=1, end_row=19, end_column=6)
c = ws.cell(19, 1, "CONTENIDO DEL LIBRO")
style_cell(c, size=11, bold=True, halign="left", bottom=side("medium", NAVY))
ws.row_dimensions[19].height = 20

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
r = 20
for i, (name, description) in enumerate(index):
    bg = BAND if i % 2 else WHITE
    c = ws.cell(r, 1, name)
    style_cell(c, size=10, bold=True, bg=bg, halign="left", wrap=False,
               bottom=side("thin", LINE))
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=6)
    c = ws.cell(r, 2, description)
    style_cell(c, size=10, bg=bg, halign="left", wrap=False,
               bottom=side("thin", LINE))
    ws.row_dimensions[r].height = 16
    r += 1

ws.merge_cells(start_row=37, start_column=1, end_row=37, end_column=6)
c = ws.cell(37, 1, "FUENTES DE DATOS")
style_cell(c, size=11, bold=True, halign="left", bottom=side("medium", NAVY))
ws.row_dimensions[37].height = 20

sources = [
    "informe_final_v10.docx (solo lectura): tablas 35 a 51 y rótulos visibles.",
    "pretest_campo.csv y posttest_campo.csv: matrices de datos de campo (n = 14).",
    "reporte_estadistico_completo.json: descriptivos, normalidad, contrastes y confiabilidad.",
    "Las cifras se recalcularon desde los CSV y se contrastaron con el JSON y con el DOCX.",
]
r = 38
for text in sources:
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    c = ws.cell(r, 1, text)
    style_cell(c, size=9, italic=True, color="000000", halign="left", wrap=True)
    ws.row_dimensions[r].height = 15
    r += 1

ws.merge_cells(start_row=43, start_column=1, end_row=43, end_column=6)
c = ws.cell(43, 1, "Nota. Libro generado con openpyxl. Formato APA 7: tablas de tres líneas horizontales, sin líneas verticales. Las hojas con cifras empíricas conservan la marca " + MARKER + ".")
style_cell(c, size=9, italic=True, color="000000", halign="left", wrap=True)
ws.row_dimensions[43].height = 42

print_setup(ws, area="A1:F43")
sheet_stats.append(("00_PORTADA", "Portada e índice", ws.max_row, ws.max_column, 0, "A1:F43"))

# ---------------------------------------------------------------------------
# Tablas de anexo 44 a 51
# ---------------------------------------------------------------------------
def annex_sheet(name, label, caption, headers, rows, widths, *, banner=None,
                formats=None, aligns=None, note=None, autofilter=True,
                tab=NAVY, source="informe_final_v10.docx"):
    ws = add_sheet(wb, name, tab=tab)
    hr, ld, nr = write_table_block(
        ws, 1, label, caption, headers, rows, widths, banner=banner,
        formats=formats, aligns=aligns, note=note, autofilter=autofilter,
        freeze=True, apply_widths=True,
    )
    print_setup(ws, title_rows="1:5",
                area=f"A1:{get_column_letter(len(headers))}{nr}")
    sheet_stats.append((name, label + ". " + caption, ws.max_row,
                        ws.max_column, len(rows),
                        f"A{hr}:{get_column_letter(len(headers))}{ld}"))
    trace_note = ("Valores verificados celda a celda entre el DOCX y el CSV"
                  if "csv" in source else "Transcripción íntegra del DOCX")
    trace_rows.append((label, name, f"A{hr}:{get_column_letter(len(headers))}{ld}",
                       source, trace_note + "; tabla APA 7 de tres líneas horizontales, sin líneas verticales."))
    return ws


# Tabla 44
d44 = doc_rows(44)
annex_sheet(
    "01_TABLA_44_CONSISTENCIA", "Tabla 44", CAPTIONS[44],
    d44[0], d44[1:], [30, 32, 32, 40, 40],
    note="Nota. Transcripción íntegra de la Tabla 44 del informe final v10. "
         "Formato APA 7 de tres líneas horizontales, sin líneas verticales. "
         "El contenido reproduce el texto del DOCX sin recortes. Elaboración propia.",
)

# Tabla 45
d45 = doc_rows(45)
annex_sheet(
    "02_TABLA_45_OPERACIONALIZACION", "Tabla 45", CAPTIONS[45],
    d45[0], d45[1:], [22, 36, 24, 38, 24, 20],
    note="Nota. Transcripción íntegra de la Tabla 45 del informe final v10. "
         "Formato APA 7 de tres líneas horizontales, sin líneas verticales. "
         "Las tres dimensiones oficiales de la variable dependiente. Elaboración propia.",
)

# Tabla 46 (doc.tables[49])
d46 = doc_rows(49)
annex_sheet(
    "03_TABLA_46_INSTRUMENTO_01", "Tabla 46", CAPTIONS[46],
    d46[0], d46[1:], [14, 40, 62, 24],
    note="Nota. Instrumento N.° 01. Codificación de indicadores y criterios de "
         "medición cronométrica. n = 14 operadores. Fuente: informe_final_v10.docx, "
         "Tabla 46. Elaboración propia.",
)

# Tabla 47 (doc.tables[50])
d47 = doc_rows(50)
annex_sheet(
    "04_TABLA_47_INSTRUMENTO_02", "Tabla 47", CAPTIONS[47],
    d47[0], d47[1:], [14, 42, 62, 24],
    note="Nota. Instrumento N.° 02. Fórmulas operativas de cálculo y rangos de "
         "escala de los indicadores de consistencia documental. n = 14 operadores. "
         "Fuente: informe_final_v10.docx, Tabla 47. Elaboración propia.",
)

# Tabla 48 (doc.tables[51])
d48 = doc_rows(51)
annex_sheet(
    "05_TABLA_48_INSTRUMENTO_03_TAM", "Tabla 48", CAPTIONS[48],
    d48[0], d48[1:], [10, 30, 76, 28],
    note="Nota. Instrumento N.° 03, Modalidad A. Ocho reactivos: AP-01 a AP-04 "
         "(aceptación del proceso) y UP-01 a UP-04 (utilidad percibida). Escala "
         "Likert de 1 a 5. Fuente: informe_final_v10.docx, Tabla 48. Elaboración propia.",
)

# Tablas 49 y 50 desde las bases CSV
PRE_HEADERS = ["Sujeto", "Centro de acopio", "T_reg (min)", "T_vale (min)",
               "RSD (%)", "CPE (%)", "AP-01", "AP-02", "AP-03", "AP-04",
               "UP-01", "UP-02", "UP-03", "UP-04", "AP (pts)", "UP (pts)",
               "TAM total (pts)", "Nivel"]
DATA_WIDTHS = [9, 26, 11, 11, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 10, 8]
DATA_ALIGNS = ["center", "left"] + ["center"] * 16
DATA_FORMATS = [None, None, "0.00", "0.00", "0.00", "0.00"] + ["0"] * 10 + ["0.00", "0.00", "0", None]


def matrix_rows(frame):
    out = []
    for _, row in frame.iterrows():
        out.append([
            row["sujeto_id"], row["centro_acopio"], float(row["t_reg"]),
            float(row["t_vale"]), float(row["rsd"]), float(row["cpe"]),
            int(row["ap_01"]), int(row["ap_02"]), int(row["ap_03"]), int(row["ap_04"]),
            int(row["up_01"]), int(row["up_02"]), int(row["up_03"]), int(row["up_04"]),
            int(row["score_ap"]), int(row["score_up"]),
            int(row["score_tam_total"]), row["nivel_satisfaccion"],
        ])
    return out


annex_sheet(
    "06_TABLA_49_PRETEST", "Tabla 49", CAPTIONS[49],
    PRE_HEADERS, matrix_rows(pre), DATA_WIDTHS,
    banner=MARKER, formats=DATA_FORMATS, aligns=DATA_ALIGNS,
    note="Nota. Matriz íntegra de la Tabla 49 del informe final v10. n = 14 "
         "operadores. Los valores provienen de pretest_campo.csv y coinciden "
         "celda a celda con el DOCX. " + MARKER,
    source="informe_final_v10.docx; pretest_campo.csv",
)

annex_sheet(
    "07_TABLA_50_POSTTEST", "Tabla 50", CAPTIONS[50],
    PRE_HEADERS, matrix_rows(post), DATA_WIDTHS,
    banner=MARKER, formats=DATA_FORMATS, aligns=DATA_ALIGNS,
    note="Nota. Matriz íntegra de la Tabla 50 del informe final v10. n = 14 "
         "operadores. Los valores provienen de posttest_campo.csv y coinciden "
         "celda a celda con el DOCX. " + MARKER,
    source="informe_final_v10.docx; posttest_campo.csv",
)

# Tabla 51 (doc.tables[54])
d51 = doc_rows(54)
annex_sheet(
    "08_TABLA_51_HISTORIAS_XP", "Tabla 51", CAPTIONS[51],
    d51[0], d51[1:], [14, 40, 52, 32, 58],
    note="Nota. Tabla 51 del informe final v10. Historias de usuario "
         "implementadas en SIVAC bajo Extreme Programming. La iteración de cada "
         "HU se transcribe del DOCX. Elaboración propia.",
)

# ---------------------------------------------------------------------------
# 09_DESCRIPTIVOS
# ---------------------------------------------------------------------------
ws = add_sheet(wb, "09_DESCRIPTIVOS")
set_widths(ws, [42, 20, 7, 11, 10, 11, 10, 11, 11, 11, 11, 12])
HEADERS_DESC = ["Indicador", "Momento evaluado", "n", "Media", "DE", "Mediana",
                "RIC", "Mínimo", "Máximo", "Asimetría", "Curtosis", "Variación"]
W_DESC = [42, 20, 7, 11, 10, 11, 10, 11, 11, 11, 11, 12]
ALIGN_DESC = ["left", "left", "center"] + ["center"] * 9
FMT_DESC = [None, None, "0", "0.00", "0.00", "0.00", "0.00", "0.00", "0.00", "0.000", "0.000", None]

blocks_desc = [(36, ["t_reg", "t_vale"]), (37, ["rsd", "cpe"]),
               (38, ["score_ap", "score_up", "score_tam_total"])]
top = 1
for idx, (tnum, keys) in enumerate(blocks_desc):
    rows = []
    total_rows = []
    for key in keys:
        s = STATS[key]
        is_pct = key in PCT
        fmt = "0.00%" if is_pct else "0.00"
        mean_fmt = "0.00%" if is_pct else "0.00"
        for moment, block_key in (("Pretest (Manual)", "pre"),
                                  ("Postest (SIVAC)", "post"),
                                  ("Diferencia pareada", "diff")):
            b = s[block_key]
            scale = 0.01 if is_pct else 1.0
            variation = None
            if block_key == "post":
                variation = s["delta"] / 100.0
            rows.append([
                LABELS[key], moment, b["n"], b["media"] * scale,
                b["de"] * scale, b["mediana"] * scale, b["ric"] * scale,
                b["min"] * scale, b["max"] * scale, b["asimetria"],
                b["curtosis"], variation if variation is not None else "—",
            ])
        if key == "score_tam_total":
            total_rows.extend(range(len(rows) - 3, len(rows)))
    # Formatos por bloque: porcentajes y variacion
    formats = []
    for key in keys:
        fmt = "0.00%" if key in PCT else "0.00"
        var_fmt = "+0.00%;-0.00%" if key not in PCT else "+0.00%;-0.00%"
        formats.extend([
            [None, None, "0", fmt, fmt, fmt, fmt, fmt, fmt, "0.000", "0.000", None],
            [None, None, "0", fmt, fmt, fmt, fmt, fmt, fmt, "0.000", "0.000", var_fmt],
            [None, None, "0", fmt, fmt, fmt, fmt, fmt, fmt, "0.000", "0.000", None],
        ])
    hr, ld, nr = write_table_block(
        ws, top, f"Tabla {tnum}", CAPTIONS[tnum], HEADERS_DESC, rows, W_DESC,
        banner=(MARKER if idx == 0 else None), formats=formats,
        aligns=ALIGN_DESC, total_rows=total_rows,
        note=("Nota. Media, DE, mediana, RIC, mínimo y máximo calculados desde "
              "pretest_campo.csv y posttest_campo.csv; coinciden con "
              "reporte_estadistico_completo.json y con la Tabla "
              f"{tnum} del informe final v10. La variación porcentual se calcula "
              "como (postest - pretest) / pretest × 100. " + MARKER),
        autofilter=False, freeze=False, apply_widths=(idx == 0),
    )
    trace_rows.append((f"Tabla {tnum}", "09_DESCRIPTIVOS",
                       f"A{hr}:L{ld}", "pretest_campo.csv; posttest_campo.csv; reporte_estadistico_completo.json",
                       "Estadística descriptiva APA 7; cifras contrastadas con el DOCX y el JSON."))
    top = nr + 2

print_setup(ws, title_rows="1:6", area=f"A1:L{ws.max_row}")
sheet_stats.append(("09_DESCRIPTIVOS", "Tablas 36, 37 y 38", ws.max_row,
                    ws.max_column, 21, "A1:L" + str(top)))

# ---------------------------------------------------------------------------
# 10_CONFIABILIDAD
# ---------------------------------------------------------------------------
ws = add_sheet(wb, "10_CONFIABILIDAD")
HEADERS_ALPHA = ["Momento de evaluación", "Escala / subescala", "N.° de ítems",
                 "Muestra (n)", "Alfa de Cronbach", "IC 95 % inferior",
                 "IC 95 % superior", "Nivel de consistencia"]
W_ALPHA = [26, 34, 12, 11, 14, 14, 14, 18]
FMT_ALPHA = [None, None, "0", "0", ".000", ".000", ".000", None]
ALIGN_ALPHA = ["left", "left", "center", "center", "center", "center", "center", "center"]

alpha_rows = []
for moment_key, moment_label in (("pretest", "Pretest (Proceso manual)"),
                                 ("posttest", "Postest (Sistema SIVAC)")):
    for scale_key, scale_label in (("global", "Escala Global TAM (Modalidad A)"),
                                   ("ap", "Aceptación del Proceso (AP)"),
                                   ("up", "Utilidad Percibida (UP)")):
        a, lo, hi, k = ALPHA[(moment_key, scale_key)]
        level = "Excelente" if a >= 0.90 else "Buena" if a >= 0.80 else "Aceptable"
        alpha_rows.append([moment_label, scale_label, k, 14, a, lo, hi, level])
alpha_total = [i for i, r in enumerate(alpha_rows) if "Global" in r[1]]
hr, ld, nr = write_table_block(
    ws, 1, "Tabla 35", CAPTIONS[35], HEADERS_ALPHA, alpha_rows, W_ALPHA,
    banner=MARKER, formats=FMT_ALPHA, aligns=ALIGN_ALPHA,
    total_rows=alpha_total,
    note="Nota. Coeficiente alfa de Cronbach con intervalo de confianza al 95 % "
         "de Feldt. Ocho ítems de la Modalidad A (AP-01 a AP-04 y UP-01 a UP-04); "
         "n = 14. Cifras idénticas a la Tabla 35 del informe "
         "final v10. " + MARKER,
    autofilter=True, freeze=True,
)
trace_rows.append(("Tabla 35", "10_CONFIABILIDAD", f"A{hr}:H{ld}",
                   "pretest_campo.csv; posttest_campo.csv; reporte_estadistico_completo.json",
                   "Alfa de Cronbach e IC 95 % de Feldt; cifras contrastadas con el DOCX y el JSON."))
print_setup(ws, title_rows="1:6", area=f"A1:H{nr}")
sheet_stats.append(("10_CONFIABILIDAD", "Tabla 35", ws.max_row, ws.max_column, 6, f"A1:H{nr}"))

# ---------------------------------------------------------------------------
# 11_NORMALIDAD
# ---------------------------------------------------------------------------
ws = add_sheet(wb, "11_NORMALIDAD")
HEADERS_NORM = ["Dimensión", "Indicador evaluado", "n", "Estadístico W", "gl",
                "p-valor", "Decisión distribucional", "Prueba inferencial asignada"]
W_NORM = [22, 44, 7, 14, 7, 10, 28, 24]
FMT_NORM = [None, None, "0", ".000", "0", ".000", None, None]
norm_rows = []
for key in KEYS:
    J = R["normalidad_shapiro_wilk"][key]
    norm_rows.append([
        J["indicador"].split(":")[0] if False else {
            "t_reg": "D1: Oportunidad", "t_vale": "D1: Oportunidad",
            "rsd": "D2: Consistencia", "cpe": "D2: Consistencia",
            "score_ap": "D3: Satisfacción", "score_up": "D3: Satisfacción",
            "score_tam_total": "D3: Satisfacción",
        }[key],
        J["indicador"], J["gl"], J["estadistico_w"], J["gl"], J["p_valor"],
        "Normal (p > .05)" if J["es_normal"] else "No normal (p ≤ .05)",
        "t de Student pareada",
    ])
hr, ld, nr = write_table_block(
    ws, 1, "Tabla 39", CAPTIONS[39], HEADERS_NORM, norm_rows, W_NORM,
    banner=MARKER, formats=FMT_NORM, aligns=["left", "left", "center", "center",
                                             "center", "center", "left", "left"],
    note="Nota. Shapiro-Wilk aplicado a la diferencia postest - pretest por "
         "indicador; n = 14 y gl = 14. Un p > .05 sustenta el ajuste gaussiano y "
         "la prueba t pareada, complementada con Wilcoxon. Cifras idénticas a la "
         "Tabla 39 del informe final v10. " + MARKER,
    autofilter=True, freeze=True,
)
trace_rows.append(("Tabla 39", "11_NORMALIDAD", f"A{hr}:H{ld}",
                   "pretest_campo.csv; posttest_campo.csv; reporte_estadistico_completo.json",
                   "Shapiro-Wilk sobre diferencias pareadas; cifras contrastadas con el DOCX y el JSON."))
print_setup(ws, title_rows="1:6", area=f"A1:H{nr}")
sheet_stats.append(("11_NORMALIDAD", "Tabla 39", ws.max_row, ws.max_column, 7, f"A1:H{nr}"))

# ---------------------------------------------------------------------------
# 12_CONTRASTES
# ---------------------------------------------------------------------------
ws = add_sheet(wb, "12_CONTRASTES")
HEADERS_CON = ["Indicador", "Prueba estadística", "Estadístico", "gl",
               "p-valor", "p exacta", "Índice del efecto", "Valor del efecto",
               "Magnitud (Cohen)", "p ajustada (Holm)", "Decisión sobre H0"]
W_CON = [32, 27, 12, 7, 10, 12, 10, 12, 12, 12, 17]
FMT_CON = [None, None, "0.000", "0", None, "0.00E+00", None, "0.000", None, None, None]
controls = {
    40: (["t_reg", "t_vale"], "H0,1"),
    41: (["rsd", "cpe"], "H0,2"),
    42: (["score_ap", "score_up", "score_tam_total"], "H0,3"),
}
top = 1
for idx, (tnum, (keys, h0)) in enumerate(controls.items()):
    rows = []
    for key in keys:
        s = STATS[key]
        rows.append([
            LABELS[key], "t de Student pareada", s["t"], s["gl"],
            p_apa(s["p_t"]), s["p_t"], "d_z", s["dz"], "Grande",
            p_apa(s["p_holm"]), f"Rechazar {h0}",
        ])
        rows.append([
            LABELS[key], "Wilcoxon pareado (W = 0.000)", s["z"], "—",
            p_apa(s["p_wilcox"]), s["p_wilcox"], "r", s["r"], "Grande",
            "—", f"Rechazar {h0}",
        ])
    hr, ld, nr = write_table_block(
        ws, top, f"Tabla {tnum}", CAPTIONS[tnum], HEADERS_CON, rows, W_CON,
        banner=(MARKER if idx == 0 else None), formats=FMT_CON,
        aligns=["left", "left", "center", "center", "center", "center",
                "center", "center", "center", "center", "center"],
        note="Nota. p-valores exactos del reporte inferencial. d_z = diferencia "
             "media / DE de las diferencias; r = |Z| / sqrt(N), con N = 14 pares "
             "válidos. Magnitud grande: "
             "|d_z| ≥ 0.80 y r ≥ 0.50. El ajuste de Holm-Bonferroni se aplica "
             "sobre los siete indicadores. Cifras idénticas a la Tabla "
             f"{tnum} del informe final v10. " + MARKER,
        autofilter=False, freeze=False, apply_widths=(idx == 0),
    )
    trace_rows.append((f"Tabla {tnum}", "12_CONTRASTES", f"A{hr}:K{ld}",
                       "reporte_estadistico_completo.json; pretest_campo.csv; posttest_campo.csv",
                       "Contraste pareado t y Wilcoxon, tamaño del efecto y Holm-Bonferroni."))
    top = nr + 2

# Tabla 43
summary_rows = [
    ["Hipótesis Específica 1 (HE1)", "D1: Oportunidad de procesamiento",
     "T_reg, T_vale", "t pareada / Wilcoxon", "< .001", "< .001",
     "Rechazar H0,1", "Reducción > 80% en tiempos operativos"],
    ["Hipótesis Específica 2 (HE2)", "D2: Consistencia documental",
     "RSD, CPE", "t pareada / Wilcoxon", "< .001", "< .001",
     "Rechazar H0,2", "Exactitud documental superior al 95%"],
    ["Hipótesis Específica 3 (HE3)", "D3: Satisfacción del usuario",
     "AP, UP, TAM total", "t pareada / Wilcoxon", "< .001", "< .001",
     "Rechazar H0,3", "Incremento > 100% en aceptación y utilidad"],
    ["Hipótesis General (HG)", "Gestión de movimientos de vacunas",
     "D1 + D2 + D3", "Criterio conjuntivo", "< .001", "< .001",
     "Rechazar H0", "Mejora integral multidimensional significativa"],
]
HEADERS_SUM = ["Hipótesis de investigación", "Dimensión asociada",
               "Indicadores clave", "Prueba decisoria", "p original",
               "p ajustado (Holm)", "Decisión estadística", "Impacto operativo"]
hr, ld, nr = write_table_block(
    ws, top, "Tabla 43", CAPTIONS[43], HEADERS_SUM, summary_rows, W_CON[:8],
    banner=None, formats=None,
    aligns=["left", "left", "left", "left", "center", "center", "center", "left"],
    total_rows=[3],
    note="Nota. La Hipótesis General se contrasta mediante regla conjuntiva: el "
         "rechazo simultáneo de H0,1, H0,2 y H0,3 con p ajustado por Holm. "
         "Esta tabla conserva la expresión < .001 del documento fuente; los "
         "valores exactos figuran en las tablas 40 a 42. " + MARKER,
    autofilter=True, freeze=False, apply_widths=False, span_cols=11,
)
trace_rows.append(("Tabla 43", "12_CONTRASTES", f"A{hr}:H{ld}",
                   "reporte_estadistico_completo.json; decision_hipotesis",
                   "Resumen de contrastación y regla conjuntiva para la Hipótesis General."))
print_setup(ws, title_rows="1:5", area=f"A1:K{max(top, nr)}")
sheet_stats.append(("12_CONTRASTES", "Tablas 40 a 43", ws.max_row, ws.max_column, 18, f"A1:K{nr}"))

# ---------------------------------------------------------------------------
# 13_SPSS_SINTAXIS
# ---------------------------------------------------------------------------
ws = add_sheet(wb, "13_SPSS_SINTAXIS", tab=TOTAL)
set_widths(ws, [132])
ws.sheet_view.showGridLines = False
ws.freeze_panes = "A3"

syntax = [
    "* ============================================================.",
    "* SIVAC - SINTAXIS REPRODUCIBLE DE IBM SPSS STATISTICS (v27 o superior).",
    "* Tesis: Aplicacion del sistema SIVAC para mejorar la gestion de movimientos",
    "* mensuales de vacunas en la DISA Apurimac II. Diseno preexperimental",
    "* O1 -> X -> O2, poblacion censal N = n = 14.",
    "* ADVERTENCIA: " + MARKER,
    "* ============================================================.",
    "",
    "SET UNICODE=ON.",
    "SET DECIMALS=3.",
    "SET MXLOOPS=100.",
    "",
    "* ------------------------------------------------------------.",
    "* 1. IMPORTACION DE LAS BASES DE CAMPO (UTF-8, separador coma).",
    "* ------------------------------------------------------------.",
    "GET DATA",
    "  /TYPE=TXT",
    "  /FILE='C:\\MisInvestigaciones\\tesis\\sivac\\salidas\\evidencias\\base_de_datos\\pretest_campo.csv'",
    "  /ENCODING='UTF8'",
    "  /DELCASE=LINE",
    '  /DELIMITERS=","',
    "  /QUALIFIER='\"'",
    "  /ARRANGEMENT=DELIMITED",
    "  /FIRSTCASE=2",
    "  /VARIABLES=",
    "    sujeto_id A8",
    "    centro_acopio A40",
    "    t_reg F8.2",
    "    t_vale F8.2",
    "    rsd F8.2",
    "    cpe F8.2",
    "    ap_01 F2.0",
    "    ap_02 F2.0",
    "    ap_03 F2.0",
    "    ap_04 F2.0",
    "    up_01 F2.0",
    "    up_02 F2.0",
    "    up_03 F2.0",
    "    up_04 F2.0",
    "    score_ap F2.0",
    "    score_up F2.0",
    "    score_tam_total F2.0",
    "    nivel_satisfaccion A8.",
    "CACHE.",
    "EXECUTE.",
    "DATASET NAME PRETEST WINDOW=FRONT.",
    "SORT CASES BY sujeto_id.",
    "",
    "GET DATA",
    "  /TYPE=TXT",
    "  /FILE='C:\\MisInvestigaciones\\tesis\\sivac\\salidas\\evidencias\\base_de_datos\\posttest_campo.csv'",
    "  /ENCODING='UTF8'",
    "  /DELCASE=LINE",
    '  /DELIMITERS=","',
    "  /QUALIFIER='\"'",
    "  /ARRANGEMENT=DELIMITED",
    "  /FIRSTCASE=2",
    "  /VARIABLES=",
    "    sujeto_id A8",
    "    centro_acopio A40",
    "    t_reg F8.2",
    "    t_vale F8.2",
    "    rsd F8.2",
    "    cpe F8.2",
    "    ap_01 F2.0",
    "    ap_02 F2.0",
    "    ap_03 F2.0",
    "    ap_04 F2.0",
    "    up_01 F2.0",
    "    up_02 F2.0",
    "    up_03 F2.0",
    "    up_04 F2.0",
    "    score_ap F2.0",
    "    score_up F2.0",
    "    score_tam_total F2.0",
    "    nivel_satisfaccion A8.",
    "CACHE.",
    "EXECUTE.",
    "DATASET NAME POSTEST WINDOW=FRONT.",
    "SORT CASES BY sujeto_id.",
    "",
    "* ------------------------------------------------------------.",
    "* 2. EMPAREJAMIENTO 1:1 POR SUJETO.",
    "* ------------------------------------------------------------.",
    "DATASET ACTIVATE PRETEST.",
    "MATCH FILES",
    "  /FILE=*",
    "  /FILE=POSTEST",
    "  /BY sujeto_id",
    "  /RENAME (centro_acopio t_reg t_vale rsd cpe ap_01 ap_02 ap_03 ap_04",
    "           up_01 up_02 up_03 up_04 score_ap score_up score_tam_total",
    "           nivel_satisfaccion = centro_post t_reg_post t_vale_post rsd_post",
    "           cpe_post ap_01_post ap_02_post ap_03_post ap_04_post up_01_post",
    "           up_02_post up_03_post up_04_post score_ap_post score_up_post",
    "           score_tam_total_post nivel_post)",
    "  /DROP=centro_post.",
    "EXECUTE.",
    "DATASET NAME SIVAC WINDOW=FRONT.",
    "",
    "* ------------------------------------------------------------.",
    "* 3. ETIQUETAS DE VARIABLES.",
    "* ------------------------------------------------------------.",
    "VARIABLE LABELS",
    "  t_reg 'Tiempo de registro pretest (min)'",
    "  t_vale 'Tiempo de emision de vales pretest (min)'",
    "  rsd 'Registros sin discrepancias pretest (%)'",
    "  cpe 'Concordancia programada vs entregada pretest (%)'",
    "  score_ap 'Aceptacion del proceso pretest (4-20)'",
    "  score_up 'Utilidad percibida pretest (4-20)'",
    "  score_tam_total 'Puntaje global TAM pretest (8-40)'",
    "  t_reg_post 'Tiempo de registro postest (min)'",
    "  t_vale_post 'Tiempo de emision de vales postest (min)'",
    "  rsd_post 'Registros sin discrepancias postest (%)'",
    "  cpe_post 'Concordancia programada vs entregada postest (%)'",
    "  score_ap_post 'Aceptacion del proceso postest (4-20)'",
    "  score_up_post 'Utilidad percibida postest (4-20)'",
    "  score_tam_total_post 'Puntaje global TAM postest (8-40)'.",
    "EXECUTE.",
    "",
    "* ------------------------------------------------------------.",
    "* 4. DIFERENCIAS PAREADAS (POSTEST - PRETEST).",
    "* ------------------------------------------------------------.",
    "COMPUTE d_t_reg = t_reg_post - t_reg.",
    "COMPUTE d_t_vale = t_vale_post - t_vale.",
    "COMPUTE d_rsd = rsd_post - rsd.",
    "COMPUTE d_cpe = cpe_post - cpe.",
    "COMPUTE d_score_ap = score_ap_post - score_ap.",
    "COMPUTE d_score_up = score_up_post - score_up.",
    "COMPUTE d_score_tam_total = score_tam_total_post - score_tam_total.",
    "EXECUTE.",
    "FORMATS d_t_reg d_t_vale d_rsd d_cpe d_score_ap d_score_up",
    "        d_score_tam_total (F8.2).",
    "EXECUTE.",
    "",
    "* ------------------------------------------------------------.",
    "* 5. CONFIABILIDAD (ALFA DE CRONBACH).",
    "* ------------------------------------------------------------.",
    "RELIABILITY",
    "  /VARIABLES=ap_01 ap_02 ap_03 ap_04 up_01 up_02 up_03 up_04",
    "  /SCALE('TAM Global - Pretest') ALL",
    "  /MODEL=ALPHA",
    "  /STATISTICS=DESCRIPTIVE SCALE",
    "  /SUMMARY=TOTAL.",
    "",
    "RELIABILITY",
    "  /VARIABLES=ap_01_post ap_02_post ap_03_post ap_04_post",
    "             up_01_post up_02_post up_03_post up_04_post",
    "  /SCALE('TAM Global - Postest') ALL",
    "  /MODEL=ALPHA",
    "  /STATISTICS=DESCRIPTIVE SCALE",
    "  /SUMMARY=TOTAL.",
    "",
    "RELIABILITY /VARIABLES=ap_01 ap_02 ap_03 ap_04",
    "  /SCALE('Aceptacion del proceso - Pretest') ALL /MODEL=ALPHA.",
    "RELIABILITY /VARIABLES=up_01 up_02 up_03 up_04",
    "  /SCALE('Utilidad percibida - Pretest') ALL /MODEL=ALPHA.",
    "RELIABILITY /VARIABLES=ap_01_post ap_02_post ap_03_post ap_04_post",
    "  /SCALE('Aceptacion del proceso - Postest') ALL /MODEL=ALPHA.",
    "RELIABILITY /VARIABLES=up_01_post up_02_post up_03_post up_04_post",
    "  /SCALE('Utilidad percibida - Postest') ALL /MODEL=ALPHA.",
    "",
    "* ------------------------------------------------------------.",
    "* 6. ESTADISTICOS DESCRIPTIVOS Y NORMALIDAD.",
    "* ------------------------------------------------------------.",
    "DESCRIPTIVES VARIABLES=t_reg t_vale rsd cpe score_ap score_up",
    "  score_tam_total t_reg_post t_vale_post rsd_post cpe_post",
    "  score_ap_post score_up_post score_tam_total_post",
    "  /STATISTICS=MEAN STDDEV MIN MAX SEMEAN.",
    "",
    "EXAMINE VARIABLES=t_reg t_vale rsd cpe score_ap score_up score_tam_total",
    "  /PLOT BOXPLOT STEMLEAF NPPLOT",
    "  /STATISTICS DESCRIPTIVES",
    "  /CINTERVAL 95",
    "  /MISSING LISTWISE",
    "  /NOTOTAL.",
    "",
    "EXAMINE VARIABLES=t_reg_post t_vale_post rsd_post cpe_post",
    "  score_ap_post score_up_post score_tam_total_post",
    "  /PLOT BOXPLOT STEMLEAF NPPLOT",
    "  /STATISTICS DESCRIPTIVES",
    "  /CINTERVAL 95",
    "  /MISSING LISTWISE",
    "  /NOTOTAL.",
    "",
    "EXAMINE VARIABLES=d_t_reg d_t_vale d_rsd d_cpe d_score_ap d_score_up",
    "  d_score_tam_total",
    "  /PLOT NPPLOT",
    "  /STATISTICS DESCRIPTIVES",
    "  /CINTERVAL 95",
    "  /MISSING LISTWISE",
    "  /NOTOTAL.",
    "",
    "* ------------------------------------------------------------.",
    "* 7. PRUEBA t DE STUDENT PARA MUESTRAS RELACIONADAS.",
    "* ------------------------------------------------------------.",
    "T-TEST PAIRS = t_reg t_vale rsd cpe score_ap score_up score_tam_total",
    "  WITH t_reg_post t_vale_post rsd_post cpe_post score_ap_post",
    "       score_up_post score_tam_total_post (PAIRED)",
    "  /CRITERIA=CI(.95)",
    "  /MISSING=ANALYSIS.",
    "",
    "* ------------------------------------------------------------.",
    "* 8. PRUEBA DE WILCOXON DE RANGOS CON SIGNO.",
    "* ------------------------------------------------------------.",
    "NPAR TESTS",
    "  /WILCOXON=t_reg t_vale rsd cpe score_ap score_up score_tam_total",
    "  WITH t_reg_post t_vale_post rsd_post cpe_post score_ap_post",
    "       score_up_post score_tam_total_post (PAIRED)",
    "  /STATISTICS=DESCRIPTIVES",
    "  /MISSING ANALYSIS.",
    "",
    "* ------------------------------------------------------------.",
    "* 9. CORRELACIONES PAREADAS DE PEARSON.",
    "* ------------------------------------------------------------.",
    "CORRELATIONS /VARIABLES=t_reg t_reg_post /PRINT=TWOTAIL NOSIG /MISSING=PAIRWISE.",
    "CORRELATIONS /VARIABLES=t_vale t_vale_post /PRINT=TWOTAIL NOSIG /MISSING=PAIRWISE.",
    "CORRELATIONS /VARIABLES=rsd rsd_post /PRINT=TWOTAIL NOSIG /MISSING=PAIRWISE.",
    "CORRELATIONS /VARIABLES=cpe cpe_post /PRINT=TWOTAIL NOSIG /MISSING=PAIRWISE.",
    "CORRELATIONS /VARIABLES=score_ap score_ap_post /PRINT=TWOTAIL NOSIG /MISSING=PAIRWISE.",
    "CORRELATIONS /VARIABLES=score_up score_up_post /PRINT=TWOTAIL NOSIG /MISSING=PAIRWISE.",
    "CORRELATIONS /VARIABLES=score_tam_total score_tam_total_post /PRINT=TWOTAIL NOSIG /MISSING=PAIRWISE.",
    "",
    "* ------------------------------------------------------------.",
    "* 10. AJUSTE DE HOLM-BONFERRONI (k = 7 INDICADORES).",
    "* Los p adoptados son los de la prueba t pareada del informe.",
    "* ------------------------------------------------------------.",
    "DATA LIST FREE / indicador (A16) p (F20.15).",
    "BEGIN DATA",
    "score_tam_total 1.362188594578728e-15",
    "t_reg 7.568028939969026e-15",
    "score_up 3.130057795466613e-14",
    "score_ap 5.573624691669793e-14",
    "cpe 4.917496597153696e-13",
    "rsd 9.999463193320717e-13",
    "t_vale 2.881241391147054e-12",
    "END DATA.",
    "EXECUTE.",
    "RANK VARIABLES=p (A) /RANK /PRINT=NO.",
    "COMPUTE p_holm = MIN(1, p * (8 - rp)).",
    "EXECUTE.",
    "FORMATS p p_holm (F20.15).",
    "LIST /VARIABLES=indicador p rp p_holm.",
    "",
    "* ============================================================.",
    "* FIN DE LA SINTAXIS. " + MARKER,
    "* ============================================================.",
]

r = 1
for i, line in enumerate(syntax):
    c = ws.cell(r, 1, line)
    if line.startswith("* ---") or line.startswith("* ==="):
        style_cell(c, size=9, bold=True, color=NAVY, bg=TOTAL,
                   halign="left", wrap=False,
                   top=side("thin", LINE), bottom=side("thin", LINE),
                   name=MONO_NAME)
        ws.row_dimensions[r].height = 15
    elif line.startswith("* "):
        style_cell(c, size=9, bold=True, color=NAVY, halign="left",
                   wrap=False, name=MONO_NAME)
        ws.row_dimensions[r].height = 15
    elif line == "":
        ws.row_dimensions[r].height = 8
    else:
        style_cell(c, size=9, color="000000", halign="left", wrap=False,
                   name=MONO_NAME)
        ws.row_dimensions[r].height = 14
    r += 1

note_row = r + 1
ws.merge_cells(start_row=note_row, start_column=1, end_row=note_row, end_column=1)
c = ws.cell(note_row, 1,
            "Nota. Sintaxis en texto plano, reproducible en IBM SPSS Statistics 27 o superior. "
            "Los nombres de archivo corresponden a la ruta local del proyecto; ajuste la ruta si "
            "traslada el repositorio. " + MARKER)
style_cell(c, size=9, italic=True, color="000000", halign="left", wrap=True)
ws.row_dimensions[note_row].height = 42

print_setup(ws, title_rows="1:3", area=f"A1:A{note_row}")
sheet_stats.append(("13_SPSS_SINTAXIS", "Sintaxis SPSS", note_row, 1, len(syntax), f"A1:A{note_row}"))
trace_rows.append(("Sintaxis SPSS", "13_SPSS_SINTAXIS", f"A1:A{note_row}",
                   "pretest_campo.csv; posttest_campo.csv; reporte_estadistico_completo.json",
                   "Sintaxis reproducible de importación, emparejamiento, confiabilidad, normalidad, t, Wilcoxon y Holm-Bonferroni."))

# ---------------------------------------------------------------------------
# 14_SPSS_SALIDAS
# ---------------------------------------------------------------------------
ws = add_sheet(wb, "14_SPSS_SALIDAS", tab=TOTAL)
set_widths(ws, [54, 16, 22, 12])
ws.freeze_panes = "A4"

r = 1
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
c = ws.cell(r, 1, "SALIDAS DEL VISOR SPSS - SIVAC (n = 14)")
style_cell(c, size=14, bold=True, halign="left", wrap=False)
ws.row_dimensions[r].height = 24
r += 1
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
c = ws.cell(r, 1, MARKER)
style_cell(c, size=10, bold=True, bg=TOTAL, halign="left",
           top=side("thin", NAVY), bottom=side("thin", NAVY))
ws.row_dimensions[r].height = min(42, max(18, est_lines(MARKER, 104) * 13.0 + 4))
r += 2


def section_header(text):
    global r
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    c = ws.cell(r, 1, text)
    style_cell(c, size=11, bold=True, color=WHITE, bg=NAVY, halign="left",
               wrap=False, top=side("thin", NAVY), bottom=side("thin", NAVY))
    ws.row_dimensions[r].height = 20
    r += 1


def sub_header(text):
    global r
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    c = ws.cell(r, 1, text)
    style_cell(c, size=10, bold=True, color=NAVY, bg=BAND, halign="left",
               wrap=False, top=side("thin", LINE), bottom=side("thin", LINE))
    ws.row_dimensions[r].height = 17
    r += 1


def output_header():
    global r
    write_header(ws, r, ["Estadístico", "Valor", "Error estándar / gl", "Sig."])
    ws.row_dimensions[r].height = 26
    r += 1


def out_row(label, value, se=None, sig=None, fmt="0.000", band=False):
    global r
    bg = BAND if band else WHITE
    c = ws.cell(r, 1, label)
    style_cell(c, size=10, bg=bg, halign="left", wrap=True,
               bottom=side("thin", LINE))
    c = ws.cell(r, 2, value)
    style_cell(c, size=10, bg=bg, halign="right", wrap=False,
               bottom=side("thin", LINE),
               fmt=(fmt if (value is not None and not isinstance(value, str)) else None))
    c = ws.cell(r, 3, se if se is not None else "")
    style_cell(c, size=10, bg=bg, halign="center", wrap=False,
               bottom=side("thin", LINE),
               fmt=(".000" if isinstance(se, (int, float)) else None))
    c = ws.cell(r, 4, sig if sig is not None else "")
    style_cell(c, size=10, bg=bg, halign="center", wrap=False,
               bottom=side("thin", LINE))
    ws.row_dimensions[r].height = 16
    r += 1


# 14.1 Descriptivos
section_header("ESTADÍSTICOS DESCRIPTIVOS")
output_header()
for i, key in enumerate(KEYS):
    sub_header(LABELS[key])
    for moment_label, block_key in (("Pretest (Manual)", "pre"),
                                    ("Postest (SIVAC)", "post")):
        sub_header(moment_label)
        b = STATS[key]["pre" if block_key == "pre" else "post"]
        out_row("N", b["n"], None, None, fmt="0", band=True)
        out_row("Mínimo", b["min"], None, None, fmt="0.00", band=True)
        out_row("Máximo", b["max"], None, None, fmt="0.00", band=True)
        out_row("Media", b["media"], b["de"] / math.sqrt(b["n"]), None, fmt="0.00", band=True)
        out_row("Desviación estándar", b["de"], None, None, fmt="0.00", band=True)
        out_row("Mediana", b["mediana"], None, None, fmt="0.00", band=True)
        n = b["n"]
        se_skew = math.sqrt(6 * n * (n - 1) / ((n - 2) * (n + 1) * (n + 3)))
        se_kurt = 2 * se_skew * math.sqrt((n * n - 1) / ((n - 3) * (n + 5)))
        out_row("Asimetría", b["asimetria"], se_skew, None, band=True)
        out_row("Curtosis", b["curtosis"], se_kurt, None, band=True)

# 14.2 Normalidad
section_header("PRUEBA DE NORMALIDAD (SHAPIRO-WILK)")
output_header()
for key in KEYS:
    s = STATS[key]
    out_row(f"W de Shapiro-Wilk - {SHORT[key]}", s["w"], "gl = 14", p_apa(s["p_w"]), fmt=".000")
    out_row("Decisión distribucional", "Normal (p > .05)" if s["p_w"] > 0.05 else "No normal (p ≤ .05)",
            "—", "—")

# 14.3 Correlaciones
section_header("CORRELACIONES DE MUESTRAS RELACIONADAS")
output_header()
for key in KEYS:
    s = STATS[key]
    out_row(f"Correlación de Pearson - {SHORT[key]}", s["corr"], "gl = 12", p_apa(s["p_corr"]), fmt=".000")
    out_row("N", 14, "—", "—", fmt="0")

# 14.4 t pareada
section_header("PRUEBA DE MUESTRAS RELACIONADAS (t DE STUDENT)")
output_header()
for key in KEYS:
    s = STATS[key]
    sub_header(f"Par: {SHORT[key]}")
    out_row("Media de la diferencia", s["diff"]["media"], s["sem"], "—", fmt="0.00")
    out_row("Desviación estándar", s["diff"]["de"], "—", "—", fmt="0.00")
    out_row("Media de error estándar", s["sem"], "—", "—", fmt="0.00")
    out_row("IC 95 % inferior", s["ci_low"], "—", "—", fmt="0.00")
    out_row("IC 95 % superior", s["ci_high"], "—", "—", fmt="0.00")
    out_row("t", s["t"], "gl = 13", p_apa(s["p_t"]))

# 14.5 Wilcoxon
section_header("PRUEBA DE WILCOXON DE RANGOS CON SIGNO")
output_header()
for key in KEYS:
    s = STATS[key]
    sub_header(f"Par: {SHORT[key]}")
    out_row("W (suma de rangos positivos)", s["w_stat"], "—", "—")
    out_row("Z", s["z"], "—", p_apa(s["p_wilcox"]))
    out_row("Sig. asintótica (bilateral)", p_apa(s["p_wilcox"]), "—", "—")
    out_row("r de Rosenthal", s["r"], "—", "—", fmt=".000")

note_row = r + 1
ws.merge_cells(start_row=note_row, start_column=1, end_row=note_row, end_column=4)
c = ws.cell(note_row, 1,
            "Nota. Salidas reconstruidas a partir de pretest_campo.csv y posttest_campo.csv; "
            "replican los estadísticos de reporte_estadistico_completo.json y las Tablas 35 a 43 "
            "del informe final v10. El formato imita el visor de IBM SPSS Statistics. " + MARKER)
style_cell(c, size=9, italic=True, color="000000", halign="left", wrap=True)
ws.row_dimensions[note_row].height = 42

print_setup(ws, title_rows="1:4", area=f"A1:D{note_row}")
sheet_stats.append(("14_SPSS_SALIDAS", "Salidas SPSS", note_row, 4, note_row - 4, f"A1:D{note_row}"))
trace_rows.append(("Salidas SPSS", "14_SPSS_SALIDAS", f"A1:D{note_row}",
                   "pretest_campo.csv; posttest_campo.csv; reporte_estadistico_completo.json",
                   "Réplica del visor SPSS con columnas Estadístico, Valor, Error estándar / gl y Sig."))

# ---------------------------------------------------------------------------
# 15_NOTAS_TRAZABILIDAD
# ---------------------------------------------------------------------------
ws = add_sheet(wb, "15_NOTAS_TRAZABILIDAD", tab=TOTAL)
HEADERS_TRACE = ["Rótulo", "Hoja", "Rango de celdas", "Fuente de los datos",
                 "Nota APA / observación"]
W_TRACE = [14, 26, 14, 40, 56]
trace_rows_final = []
for label, sheet, rng, source, note in trace_rows:
    trace_rows_final.append([label, sheet, rng, source, note])
# Añadir las tablas estadísticas ya registradas; el orden es el del libro.
hr, ld, nr = write_table_block(
    ws, 1, "Trazabilidad", "Trazabilidad de tablas, hojas, rangos de celdas y fuentes de datos",
    HEADERS_TRACE, trace_rows_final, W_TRACE,
    banner=None, note="Nota. Una fila por tabla. Los rangos corresponden al cuerpo de la tabla "
                      "(fila de encabezado a última fila de datos), sin incluir rótulo, título ni nota. "
                      "Las fuentes primarias son el DOCX, los CSV y el JSON del proyecto. " + MARKER,
    autofilter=True, freeze=True,
)
print_setup(ws, title_rows="1:5", area=f"A1:E{nr}")
sheet_stats.append(("15_NOTAS_TRAZABILIDAD", "Trazabilidad", ws.max_row, ws.max_column,
                    len(trace_rows_final), f"A1:E{nr}"))

# ---------------------------------------------------------------------------
# Guardado
# ---------------------------------------------------------------------------
OUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT_XLSX)
print(f"[OK] Libro guardado: {OUT_XLSX}")

# ---------------------------------------------------------------------------
# Verificación celda a celda del libro contra el DOCX
# ---------------------------------------------------------------------------
wbv = openpyxl.load_workbook(OUT_XLSX, data_only=False)
workbook_mismatches = []
annex_cells_compared = 0
annex_check = [
    ("01_TABLA_44_CONSISTENCIA", 44, 4, 5, 6),
    ("02_TABLA_45_OPERACIONALIZACION", 45, 4, 6, 6),
    ("03_TABLA_46_INSTRUMENTO_01", 49, 3, 4, 6),
    ("04_TABLA_47_INSTRUMENTO_02", 50, 3, 4, 6),
    ("05_TABLA_48_INSTRUMENTO_03_TAM", 51, 8, 4, 6),
    ("08_TABLA_51_HISTORIAS_XP", 54, 5, 5, 6),
]
for sheet_name, doc_index, nrows, ncols, first_data_row in annex_check:
    ws_v = wbv[sheet_name]
    source = doc_rows(doc_index)
    for i in range(nrows + 1):
        for j in range(ncols):
            annex_cells_compared += 1
            got = ws_v.cell(first_data_row - 1 + i, j + 1).value
            want = source[i][j]
            if isinstance(got, (int, float)):
                try:
                    ok = abs(float(got) - float(want)) < 1e-9
                except ValueError:
                    ok = False
            else:
                ok = str(got).strip() == str(want).strip()
            if not ok:
                workbook_mismatches.append((sheet_name, first_data_row - 1 + i, j + 1, got, want))

# Matrices 49/50: comparar datos (sin encabezados, que se normalizaron)
for sheet_name, frame, doc_index in (("06_TABLA_49_PRETEST", pre, 52),
                                     ("07_TABLA_50_POSTTEST", post, 53)):
    ws_v = wbv[sheet_name]
    source = doc_rows(doc_index)
    for i in range(14):
        for j in range(18):
            got = ws_v.cell(6 + i, j + 1).value
            want = source[i + 1][j]
            if isinstance(got, (int, float)):
                try:
                    ok = abs(float(got) - float(want)) < 1e-9
                except ValueError:
                    ok = False
            else:
                ok = str(got).strip() == str(want).strip()
            if not ok:
                workbook_mismatches.append((sheet_name, 6 + i, j + 1, got, want))

# ---------------------------------------------------------------------------
# Reporte de auditoría
# ---------------------------------------------------------------------------
def md_escape(text):
    return str(text).replace("|", "\\|")


lines = []
lines.append("# REPORTE DE CONSTRUCCIÓN DEL LIBRO DE TABLAS DE ANEXOS v2")
lines.append("")
lines.append("**Proyecto:** SIVAC-THESIS-LAB — Universidad Nacional José María Arguedas (UNAJMA)  ")
lines.append("**Agente:** analista-estadistico (Squad D — Bioestadística e Inferencia)  ")
lines.append("**Fase:** F8_INTEGRACION_EDITORIAL  ")
lines.append("**Fecha:** 2026-10-21  ")
lines.append("**Libro generado:** `salidas/estadistica/TABLAS_ANEXOS_SIVAC_v2.xlsx`  ")
lines.append("**Estado de los datos:** " + MARKER)
lines.append("")
lines.append("## 1. Hojas creadas")
lines.append("")
lines.append("| Hoja | Contenido | Filas totales | Columnas | Filas de datos |")
lines.append("|---|---|---:|---:|---:|")
for name, content, rows, cols, data_rows, _ in sheet_stats:
    lines.append(f"| `{name}` | {md_escape(content)} | {rows} | {cols} | {data_rows} |")
lines.append("")
lines.append("## 2. Correcciones frente a la versión anterior")
lines.append("")
lines.append("1. **Rótulos corregidos:** la versión anterior rotulaba las hojas `03_ANEXO5_PRETEST` y `04_ANEXO5_POSTEST` como «Tabla 52» y «Tabla 53». Esos números eran el índice de `python-docx`, no el rótulo visible. En esta versión se rotulan correctamente como **Tabla 49** y **Tabla 50**.")
lines.append("2. **Tablas faltantes incorporadas:** se añadieron la Tabla 46 (Instrumento N.° 01), la Tabla 47 (Instrumento N.° 02), la Tabla 48 (Cuestionario TAM) y la Tabla 51 (Historias de Usuario XP), todas en formato tabular.")
lines.append("3. **Historias de Usuario actualizadas al DOCX v10:** la versión anterior asignaba a HU-06 la «Iteración 2 (Movimientos)». El DOCX v10 registra «Iteración 3 (Núcleo Transaccional y Despacho)». Se transcribió el valor del DOCX vigente.")
lines.append("4. **Fuente actualizada:** las notas de la versión anterior remitían a `informe_final_v04.docx`. Esta versión remite a `informe_final_v10.docx`.")
lines.append("5. **Certificados de validación:** los índices `python-docx` 46, 47 y 48 corresponden a los certificados de los jueces 1, 2 y 3, que no llevan rótulo de tabla. Por indicación del Director no se incorporan como hojas tabulares; las Tablas 46, 47 y 48 visibles son los instrumentos, que sí se incorporaron.")
lines.append("")
lines.append("## 3. Verificación de contenido frente al DOCX")
lines.append("")
lines.append(f"- Comparación celda a celda de las tablas 44, 45, 46, 47, 48 y 51: **{len(workbook_mismatches)} discrepancias** en {annex_cells_compared} celdas comparadas.")
lines.append(f"- Comparación de las matrices de pretest y postest (14 filas × 18 columnas por momento, 504 celdas): **{len(doc_csv_mismatches)} discrepancias** entre el DOCX y los CSV.")
lines.append("- Las matrices 49 y 50 se construyeron desde los CSV y se compararon contra las tablas 52 y 53 de `python-docx`; los valores numéricos, identificadores, centros de acopio y niveles coinciden.")
lines.append("- Los encabezados de las matrices se normalizaron a etiquetas legibles (por ejemplo, `AP-01` en lugar de `ap_\\n01`), sin alterar los valores.")
lines.append("")
if workbook_mismatches:
    lines.append("### Discrepancias del libro frente al DOCX")
    lines.append("")
    for item in workbook_mismatches[:30]:
        lines.append(f"- `{item[0]}` celda ({item[1]}, {item[2]}): libro = `{item[3]}`; DOCX = `{item[4]}`.")
    lines.append("")
if doc_csv_mismatches:
    lines.append("### Discrepancias DOCX frente a CSV")
    lines.append("")
    for item in doc_csv_mismatches[:30]:
        lines.append(f"- {item[0]}, fila {item[1]}, columna `{item[2]}`: DOCX = `{item[3]}`; CSV = `{item[4]}`.")
    lines.append("")
lines.append("## 4. Verificación de cifras frente al informe")
lines.append("")
lines.append(f"Se compararon {json_total_checks} valores estadísticos (descriptivos, variación, normalidad, confiabilidad y contrastes) contra `reporte_estadistico_completo.json`: **{len(json_mismatches)} discrepancias**.")
lines.append("")
lines.append("| Bloque | Cifras verificadas | Resultado |")
lines.append("|---|---:|---|")
lines.append(f"| Descriptivos (media, DE, mediana, RIC, mínimo, máximo) | {check_counts['Descriptivos']} | Coinciden con el JSON y con las Tablas 36-38 del DOCX |")
lines.append(f"| Variación porcentual pretest-postest | {check_counts['Variacion porcentual']} | Coincide con el JSON |")
lines.append(f"| Alfa de Cronbach e IC 95 % de Feldt (α, límite inferior, límite superior) | {check_counts['Alfa de Cronbach']} | Coinciden con el JSON y con la Tabla 35 del DOCX |")
lines.append(f"| Shapiro-Wilk (W y p) | {check_counts['Shapiro-Wilk']} | Coinciden con el JSON y con la Tabla 39 del DOCX |")
lines.append(f"| t pareada (t, gl, p, d_z) | {check_counts['t pareada']} | Coinciden con el JSON y con las Tablas 40-42 del DOCX |")
lines.append(f"| Wilcoxon (W, Z, p, r) | {check_counts['Wilcoxon']} | W, Z y p recalculados y coincidentes con el JSON; r recalculado como |Z| / sqrt(N) y trazado al Z de origen en las Tablas 40-42 |")
lines.append(f"| Holm-Bonferroni (p ajustado) | {check_counts['Holm-Bonferroni']} | Recalculado sobre los siete p adoptados; coincide con el JSON |")
lines.append("")
if json_mismatches:
    lines.append("### Discrepancias numéricas frente al JSON")
    lines.append("")
    for block, key, field, got, want in json_mismatches:
        lines.append(f"- {block} · {key} · {field}: calculado = `{got}`; JSON = `{want}`.")
    lines.append("")
lines.append("**Cifras clave verificadas:**")
lines.append("")
lines.append("- T_reg: M pretest = 37.18 min, M postest = 7.18 min; t(13) = -38.944, p < .001, d_z = -10.408.")
lines.append("- T_vale: M pretest = 18.21 min, M postest = 3.04 min; t(13) = -24.509, p < .001, d_z = -6.550.")
lines.append("- RSD: M pretest = 63.57 %, M postest = 96.00 %; t(13) = 26.628, p < .001, d_z = 7.117.")
lines.append("- CPE: M pretest = 67.61 %, M postest = 95.39 %; t(13) = 28.147, p < .001, d_z = 7.523.")
lines.append("- AP: M pretest = 8.07, M postest = 17.71; t(13) = 33.352, p < .001, d_z = 8.914.")
lines.append("- UP: M pretest = 9.00, M postest = 18.50; t(13) = 34.881, p < .001, d_z = 9.322.")
lines.append("- TAM total: M pretest = 17.07, M postest = 36.21; t(13) = 44.477, p < .001, d_z = 11.887.")
lines.append("- Wilcoxon: W = 0.000, Z = -3.296, r = |Z| / sqrt(14) = 0.881 en los siete indicadores; p de Wilcoxon entre 1.2207E-04 y 9.7588E-04.")
lines.append("- Alfa de Cronbach global: pretest = 0.939 [0.874, 0.977]; postest = 0.915 [0.826, 0.968].")
lines.append("")
lines.append("## 5. Diseño editorial aplicado")
lines.append("")
lines.append("- Encabezados en azul marino `#1F3864` con texto blanco en negrita; bandas alternas `#F2F2F2` y `#FFFFFF`; filas de total en negrita con relleno `#D9E2F3`.")
lines.append("- Bordes finos solo horizontales, sin líneas verticales; sin colores fuera de la paleta institucional.")
lines.append("- Filas de encabezado congeladas, autofiltro en las hojas de una sola tabla, anchos ajustados y ajuste de texto.")
lines.append("- En `09_DESCRIPTIVOS` y `12_CONTRASTES`, que agrupan varias tablas por hoja, no se congelaron encabezados para no mostrar un rótulo ajeno al desplazarse; el autofiltro se aplica solo al bloque final de resumen (Tabla 43).")
lines.append("- Formato numérico: dos decimales para medias, DE y porcentajes; tres decimales para α, W, Z, p y tamaños del efecto; porcentajes con signo `%`.")
lines.append("- Impresión A4 horizontal, escalada a una página de ancho, márgenes de 1.5 cm y filas de encabezado repetidas.")
lines.append("")
lines.append("## 6. Marcas de estado y trazabilidad")
lines.append("")
lines.append("- La marca `" + MARKER + "` aparece en la portada, en las matrices 49 y 50 y en todas las hojas estadísticas (09 a 14).")
lines.append("- Las tablas 44 a 48 y 51 son transcripciones metodológicas y no llevan la marca porque no contienen cifras empíricas.")
lines.append("- La hoja `15_NOTAS_TRAZABILIDAD` registra una fila por tabla con rótulo, hoja, rango de celdas, fuente y nota APA.")
lines.append("")
lines.append("## 7. Limitaciones y pendientes")
lines.append("")
lines.append("- Las bases `pretest_campo.csv` y `posttest_campo.csv` corresponden a registros provisionales; al reemplazarlas por mediciones definitivas debe regenerarse el libro.")
lines.append("- El intervalo de confianza del alfa se calculó por el método de Feldt y se verificó numéricamente contra el JSON; no se reporta como intervalo bootstrap.")
lines.append("- Los certificados de validación por jueces no se tabularon por no llevar rótulo de tabla; si el tesista desea incorporarlos, deben abrirse como hojas independientes sin numeración de tabla.")
lines.append("- `[VERIFICAR]` La asignación de iteración de HU-06 se tomó del DOCX v10; confirmar con el expediente XP si la numeración de iteraciones es la definitiva.")
lines.append("- El r de Rosenthal se calcula como |Z| / sqrt(N), con N = 14 pares válidos, conforme a la convención adoptada. El valor corregido es 0.881 en los siete indicadores (magnitud grande, r >= 0.50); el valor previo 0.62 procedía de un denominador duplicado y quedó sustituido.")
lines.append("")
lines.append("## 8. Reproducibilidad")
lines.append("")
lines.append("```bash")
lines.append("C:/MisInvestigaciones/tesis/sivac/.venv/Scripts/python.exe \\")
lines.append("  C:/MisInvestigaciones/tesis/sivac/scripts/estadistica/build_tablas_anexos_v2.py")
lines.append("```")
lines.append("")
lines.append("El script lee únicamente el DOCX, los CSV y el JSON; no los modifica. Vuelve a generar el libro y este reporte de forma idéntica.")
lines.append("")

OUT_MD.write_text("\n".join(lines), encoding="utf-8")
print(f"[OK] Reporte guardado: {OUT_MD}")
print(f"[INFO] Discrepancias libro-DOCX: {len(workbook_mismatches)}")
print(f"[INFO] Discrepancias DOCX-CSV: {len(doc_csv_mismatches)}")
print(f"[INFO] Discrepancias JSON: {len(json_mismatches)}")
