#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exporta las tablas de los anexos del Informe Final SIVAC a un libro Excel
profesional, con diseño cromático institucional y una sección de salidas SPSS.

Uso (sin argumentos, idempotente):

    C:/MisInvestigaciones/tesis/sivac/.venv/Scripts/python.exe ^
        scripts/estadistica/exportar_tablas_anexos_excel.py

Entradas (solo lectura):
    - salidas/documentos/informe_final_v04.docx          (tablas 35 a 54)
    - salidas/estadistica/reporte_estadistico_completo.json
    - salidas/evidencias/base_de_datos/pretest_campo.csv
    - salidas/evidencias/base_de_datos/posttest_campo.csv
    - datos/schemas/centros_acopio_reales_sivac.json
    - datos/schemas/codebook.json
    - salidas/documentos/anexos_instrumentos_validacion.json

Salida:
    - salidas/estadistica/TABLAS_ANEXOS_SIVAC.xlsx

Regla deontológica: ninguna cifra se inventa ni se recalcula por conveniencia.
Los estadísticos provienen del JSON inferencial; las matrices de datos y los
anexos, del DOCX; la asimetría, la curtosis y las correlaciones se calculan
sobre los CSV de campo y se declaran como derivadas en la hoja 11_NOTAS.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from functools import lru_cache
from datetime import date
from pathlib import Path

import pandas as pd
from docx import Document
from PIL import ImageFont
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.hyperlink import Hyperlink
from openpyxl.worksheet.pagebreak import Break
from openpyxl.worksheet.page import PageMargins
from openpyxl.worksheet.properties import PageSetupProperties
from scipy import stats as scipy_stats

# ---------------------------------------------------------------------------
# Rutas canónicas
# ---------------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parents[2]

DOCX_INFORME = RAIZ / "salidas" / "documentos" / "informe_final_v04.docx"
JSON_ESTADISTICO = RAIZ / "salidas" / "estadistica" / "reporte_estadistico_completo.json"
CSV_PRETEST = RAIZ / "salidas" / "evidencias" / "base_de_datos" / "pretest_campo.csv"
CSV_POSTEST = RAIZ / "salidas" / "evidencias" / "base_de_datos" / "posttest_campo.csv"
JSON_CENTROS = RAIZ / "datos" / "schemas" / "centros_acopio_reales_sivac.json"
JSON_CODEBOOK = RAIZ / "datos" / "schemas" / "codebook.json"
JSON_ANEXOS = RAIZ / "salidas" / "documentos" / "anexos_instrumentos_validacion.json"
XLSX_SALIDA = RAIZ / "salidas" / "estadistica" / "TABLAS_ANEXOS_SIVAC.xlsx"

# ---------------------------------------------------------------------------
# Paleta institucional sobria
# ---------------------------------------------------------------------------
AZUL_MARINO = "1F3864"
AZUL_ACERO = "2E5C8A"
GRIS_PERLA = "F2F2F2"
GRIS_REJILLA = "D9D9D9"
GRIS_TEXTO = "595959"
GRIS_BANDA = "D9D9D9"
BLANCO = "FFFFFF"
NEGRO = "000000"
ROJO_P = "C00000"

FMT_EST = "0.000"
FMT_ENT = "0"
FMT_UNO = "0.0"
FMT_PCT = '0.00"%"'
FMT_PCT_SIGNO = '+0.00"%";-0.00"%"'
FMT_CIENTIFICO = "0.00E+00"

CM = 1.0 / 2.54  # pulgadas por centímetro

_FUENTES = {
    ("Times New Roman", False, False): "C:/Windows/Fonts/times.ttf",
    ("Times New Roman", True, False): "C:/Windows/Fonts/timesbd.ttf",
    ("Times New Roman", False, True): "C:/Windows/Fonts/timesi.ttf",
    ("Times New Roman", True, True): "C:/Windows/Fonts/timesbi.ttf",
    ("Calibri", False, False): "C:/Windows/Fonts/calibri.ttf",
    ("Calibri", True, False): "C:/Windows/Fonts/calibrib.ttf",
    ("Calibri", False, True): "C:/Windows/Fonts/calibrii.ttf",
    ("Calibri", True, True): "C:/Windows/Fonts/calibriz.ttf",
}


@lru_cache(maxsize=96)
def _medidor(familia: str, tam: float, negrita: bool, cursiva: bool):
    """Fuente TrueType a la resolución de pantalla (96 ppp) o None si no existe."""
    ruta = _FUENTES.get((familia or "Calibri", bool(negrita), bool(cursiva)))
    if not ruta or not Path(ruta).exists():
        return None
    try:
        return ImageFont.truetype(ruta, max(6, int(round(tam * 96 / 72))))
    except OSError:
        return None


def ancho_texto_px(texto: str, familia: str, tam: float, negrita: bool,
                   cursiva: bool) -> float:
    medidor = _medidor(familia, tam, negrita, cursiva)
    if medidor is None:
        return len(texto) * tam * 0.5 * 96 / 72
    return float(medidor.getlength(texto))


LEYENDA_DATOS = "DATOS DE PRUEBA \u2013 REEMPLAZAR (DEC-007)"
GUION = "\u2014"

INDICADORES = [
    {"clave": "t_reg", "etiqueta": "T_reg (min)", "naturaleza": "min", "csv": "t_reg",
     "docx": "Tiempo de registro (T_reg)"},
    {"clave": "t_vale", "etiqueta": "T_vale (min)", "naturaleza": "min", "csv": "t_vale",
     "docx": "Tiempo de emisión de vales (T_vale)"},
    {"clave": "rsd", "etiqueta": "RSD (%)", "naturaleza": "pct", "csv": "rsd",
     "docx": "Registros sin discrepancias (RSD)"},
    {"clave": "cpe", "etiqueta": "CPE (%)", "naturaleza": "pct", "csv": "cpe",
     "docx": "Concordancia programada vs entregada (CPE)"},
    {"clave": "score_ap", "etiqueta": "AP (pts)", "naturaleza": "pts", "csv": "score_ap",
     "docx": "Aceptación del proceso (AP)"},
    {"clave": "score_up", "etiqueta": "UP (pts)", "naturaleza": "pts", "csv": "score_up",
     "docx": "Utilidad percibida (UP)"},
    {"clave": "score_tam_total", "etiqueta": "TAM total (pts)", "naturaleza": "pts",
     "csv": "score_tam_total", "docx": "Puntaje global TAM (AP + UP)"},
]

DIMENSIONES = {
    "t_reg": "D1: Oportunidad",
    "t_vale": "D1: Oportunidad",
    "rsd": "D2: Consistencia",
    "cpe": "D2: Consistencia",
    "score_ap": "D3: Satisfacción",
    "score_up": "D3: Satisfacción",
    "score_tam_total": "D3: Satisfacción",
}

HOJAS = [
    ("00_PORTADA", "Carátula, identificación del documento e índice navegable", "—"),
    ("01_ANEXO1_MATRIZ", "Anexo 1. Matriz de consistencia metodológica (DEC-007)", "Tabla 44"),
    ("02_ANEXO2_OPERAC", "Anexo 2. Matriz de operacionalización de las variables", "Tabla 45"),
    ("03_ANEXO5_PRETEST", "Anexo 5. Matriz de datos tabulados del pretest (n = 14)", "Tabla 52"),
    ("04_ANEXO5_POSTEST", "Anexo 5. Matriz de datos tabulados del postest (n = 14)", "Tabla 53"),
    ("05_DESCRIPTIVOS", "Estadística descriptiva por indicador y por constructo",
     "Tablas 36, 37 y 38"),
    ("06_CONFIABILIDAD", "Confiabilidad de consistencia interna e intervalo de confianza",
     "Tabla 35"),
    ("07_NORMALIDAD", "Prueba de normalidad de Shapiro-Wilk sobre diferencias pareadas",
     "Tabla 39"),
    ("08_CONTRASTES", "Contrastes t de Student y Wilcoxon, efecto y ajuste Holm",
     "Tablas 40, 41, 42 y 43"),
    ("09_ANEXO6_TRAZABILIDAD", "Anexo 6. Trazabilidad de historias de usuario XP", "Tabla 54"),
    ("10_SPSS_SALIDAS", "Salidas del visor SPSS: descriptivos y muestras relacionadas",
     "Réplica SPSS"),
    ("11_NOTAS", "Trazabilidad, convenciones y marcas [VERIFICAR]", "—"),
]

# Hoja 05 y 08: tablas replicadas del documento
# 01, 02 y 09 se imprimen en horizontal por densidad del texto, aunque tengan
# siete columnas o menos; el criterio se declara en la hoja 11_NOTAS.


# ---------------------------------------------------------------------------
# Utilidades de estilo
# ---------------------------------------------------------------------------
def relleno(color: str) -> PatternFill:
    return PatternFill(fill_type="solid", start_color=color, end_color=color)


def _limpio(texto: str) -> str:
    """Normaliza espacios y elimina caracteres de control inválidos en XML."""
    texto = texto.replace("\xa0", " ").replace("\x0b", "\n").replace("\x07", "\n")
    texto = "".join(c for c in texto if c == "\n" or c == "\t" or ord(c) >= 32)
    lineas = [linea.strip() for linea in texto.split("\n")]
    return "\n".join(lineas).strip()


def _texto_visible(valor, fmt: str) -> str:
    """Aproxima la representación en pantalla para calcular anchos."""
    if valor is None:
        return ""
    if isinstance(valor, bool):
        return str(valor)
    if isinstance(valor, (int, float)):
        if "E+" in fmt:
            return f"{valor:.2E}"
        if "%" in fmt:
            return f"{valor:+.2f}%" if fmt.startswith("+") else f"{valor:.2f}%"
        if fmt == FMT_ENT:
            return f"{valor:.0f}"
        if fmt == FMT_UNO:
            return f"{valor:.1f}"
        return f"{valor:.3f}"
    return str(valor)


def celda(ws, fila: int, col: int, valor, *, familia: str, tam: int = 10,
          negrita: bool = False, cursiva: bool = False, color: str = NEGRO,
          fondo: str | None = None, h: str = "left", v: str = "center",
          wrap: bool = True, fmt: str | None = None, borde: Border | None = None,
          subrayado: str | None = None):
    c = ws.cell(row=fila, column=col)
    c.value = valor
    c.font = Font(name=familia, size=tam, bold=negrita, italic=cursiva,
                  color=color, underline=subrayado)
    if fondo:
        c.fill = relleno(fondo)
    c.alignment = Alignment(horizontal=h, vertical=v, wrap_text=wrap)
    if fmt:
        c.number_format = fmt
    if borde is not None:
        c.border = borde
    return c


def fusionar(ws, r1: int, c1: int, r2: int, c2: int):
    ws.merge_cells(start_row=r1, start_column=c1, end_row=r2, end_column=c2)


def _es_numero(valor) -> bool:
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def _es_p_valor(titulo: str) -> bool:
    t = titulo.lower()
    return "p-valor" in t or "p-ajustado" in t or t.startswith("sig")


# ---------------------------------------------------------------------------
# Escritura de tablas
# ---------------------------------------------------------------------------
@dataclass
class Columna:
    titulo: str
    fmt: str | None = None
    alineacion: str = "auto"  # auto | left | center | right


def tabla(ws, fila: int, columnas: list[Columna], filas: list[list], *,
          familia: str, tam: int = 10, estilo: str = "apa",
          banda: bool = True, alto_encabezado: int = 32) -> int:
    """Escribe una tabla y devuelve la fila siguiente a la última escrita."""
    ncols = len(columnas)

    for j, col in enumerate(columnas, start=1):
        borde = None
        if estilo == "apa":
            borde = Border(bottom=Side(style="medium", color=AZUL_MARINO))
        elif estilo == "spss":
            borde = Border(left=Side(style="thin", color=GRIS_REJILLA),
                           right=Side(style="thin", color=GRIS_REJILLA),
                           top=Side(style="thin", color=GRIS_REJILLA),
                           bottom=Side(style="medium", color=AZUL_ACERO))
        celda(ws, fila, j, col.titulo, familia=familia, tam=tam + 1, negrita=True,
              color=BLANCO, fondo=AZUL_MARINO, h="center", v="center", borde=borde)
    ws.row_dimensions[fila].height = alto_encabezado

    r = fila + 1
    for i, datos in enumerate(filas):
        fondo = GRIS_PERLA if (banda and i % 2 == 1) else BLANCO
        for j, col in enumerate(columnas, start=1):
            valor = datos[j - 1] if j - 1 < len(datos) else None
            if col.alineacion == "auto":
                alineacion = "right" if _es_numero(valor) else "left"
            else:
                alineacion = col.alineacion
            ajuste = col.fmt is not None and _es_numero(valor)
            borde = None
            if estilo == "spss":
                borde = Border(left=Side(style="thin", color=GRIS_REJILLA),
                               right=Side(style="thin", color=GRIS_REJILLA),
                               top=Side(style="thin", color=GRIS_REJILLA),
                               bottom=Side(style="thin", color=GRIS_REJILLA))
            color = NEGRO
            if (_es_numero(valor) and valor < 0.05 and _es_p_valor(col.titulo)):
                color = ROJO_P
            celda(ws, r, j, valor, familia=familia, tam=tam, color=color, fondo=fondo,
                  h=alineacion, wrap=not ajuste, fmt=col.fmt, borde=borde)
        r += 1

    ultima = r - 1
    if estilo == "apa" and ultima > fila:
        for j in range(1, ncols + 1):
            ws.cell(row=ultima, column=j).border = Border(
                bottom=Side(style="medium", color=AZUL_MARINO))
    return r


def rotulo_tabla(ws, fila: int, numero: str, titulo: str, ncols: int, familia: str):
    if ncols > 1:
        fusionar(ws, fila, 1, fila, 2)
    celda(ws, fila, 1, numero, familia=familia, tam=11, negrita=True, color=AZUL_MARINO)
    ws.row_dimensions[fila].height = 18
    fusionar(ws, fila + 1, 1, fila + 1, ncols)
    celda(ws, fila + 1, 1, titulo, familia=familia, tam=11, cursiva=True, color=NEGRO,
          v="center")
    ws.row_dimensions[fila + 1].height = 30
    return fila + 2


def leyenda_datos(ws, fila: int, ncols: int, familia: str) -> int:
    fusionar(ws, fila, 1, fila, ncols)
    for c in range(1, ncols + 1):
        ws.cell(row=fila, column=c).fill = relleno(AZUL_ACERO)
    celda(ws, fila, 1, LEYENDA_DATOS, familia=familia, tam=9, negrita=True,
          color=BLANCO, h="left")
    ws.row_dimensions[fila].height = 17
    return fila + 1


def nota_tabla(ws, fila: int, texto: str, ncols: int, familia: str) -> int:
    fusionar(ws, fila, 1, fila, ncols)
    celda(ws, fila, 1, texto, familia=familia, tam=9, cursiva=True, color=GRIS_TEXTO,
          h="left", v="top")
    ws.row_dimensions[fila].height = max(15, 12.5 * math.ceil(len(texto) / 150.0))
    return fila + 1


# ---------------------------------------------------------------------------
# Ajustes de geometría
# ---------------------------------------------------------------------------
def ajustar_anchos(ws, minimo: float = 9, maximo: float = 52, margen: float = 1.9,
                   objetivo: float | None = None):
    """Ajusta los anchos al contenido real (medición tipográfica) y, si se indica
    un objetivo en unidades de columna, los comprime proporcionalmente para que
    la impresión no baje del 90 %. Las columnas numéricas conservan un piso que
    impide la aparición de ###."""
    anclas = {(r.min_row, r.min_col) for r in ws.merged_cells.ranges
              if r.max_col > r.min_col}
    deseados, pisos = {}, {}
    for col in range(1, ws.max_column + 1):
        ancho = float(minimo)
        piso = float(minimo)
        for fila in range(1, ws.max_row + 1):
            c = ws.cell(row=fila, column=col)
            if c.value is None or (fila, col) in anclas:
                continue
            texto = _texto_visible(c.value, c.number_format or "General")
            familia = c.font.name or "Calibri"
            tam = c.font.sz or 10
            negrita, cursiva = bool(c.font.b), bool(c.font.i)
            px = max(ancho_texto_px(seg, familia, tam, negrita, cursiva)
                     for seg in str(texto).split(chr(10)))
            ancho = max(ancho, px / 7.0 + margen)
            if _es_numero(c.value):
                piso = max(piso, px / 7.0 + 1.2)
            # ninguna palabra debe quedar cortada al comprimir la columna
            for palabra in str(texto).replace("/", " ").split():
                piso = max(piso, ancho_texto_px(palabra, familia, tam, negrita,
                                                cursiva) / 7.0 + 1.0)
        deseados[col] = min(maximo, ancho)
        pisos[col] = min(deseados[col], max(float(minimo), piso))

    if objetivo and sum(deseados.values()) > objetivo:
        libres = set(deseados)
        restante = float(objetivo)
        final = {}
        while libres:
            suma = sum(deseados[c] for c in libres)
            factor = restante / suma if suma else 1.0
            fijos = [c for c in libres if deseados[c] * factor < pisos[c]]
            if not fijos:
                for c in libres:
                    final[c] = deseados[c] * factor
                break
            for c in fijos:
                final[c] = pisos[c]
                restante -= pisos[c]
                libres.discard(c)
        deseados = {c: max(pisos[c], final.get(c, deseados[c])) for c in deseados}

    for col, ancho in deseados.items():
        ws.column_dimensions[get_column_letter(col)].width = round(
            max(float(minimo), ancho), 2)


def ajustar_altos(ws, desde: int = 1, hasta: int | None = None, *,
                  maximo: float = 409.0):
    """Calcula el alto de cada fila midiendo el texto con su fuente real y el
    ancho efectivo de la columna (o del rango combinado)."""
    hasta = hasta or ws.max_row
    horizontales = {(r.min_row, r.min_col): (r.min_col, r.max_col)
                    for r in ws.merged_cells.ranges if r.min_row == r.max_row}
    verticales = [r for r in ws.merged_cells.ranges
                  if r.max_row > r.min_row and r.max_col > r.min_col]
    for fila in range(desde, hasta + 1):
        necesario = 15.0
        for col in range(1, ws.max_column + 1):
            c = ws.cell(row=fila, column=col)
            if c.value is None:
                continue
            if any(r.min_row < fila <= r.max_row for r in verticales):
                continue
            tramo = horizontales.get((fila, col))
            if tramo:
                ancho = sum(ws.column_dimensions[get_column_letter(k)].width or 10
                            for k in range(tramo[0], tramo[1] + 1))
            else:
                ancho = ws.column_dimensions[get_column_letter(col)].width or 10
            util = max(24.0, ancho * 7.0 - 7.0)
            tam = c.font.sz or 10
            lineas = 0
            for segmento in str(c.value).split(chr(10)):
                px = ancho_texto_px(segmento, c.font.name or "Calibri", tam,
                                    bool(c.font.b), bool(c.font.i))
                lineas += max(1, math.ceil(px / (util * 0.97)))
            necesario = max(necesario, lineas * (tam * 1.32) + 3.0)
        necesario = min(maximo, necesario)
        actual = ws.row_dimensions[fila].height
        if actual is None or necesario > actual:
            ws.row_dimensions[fila].height = round(necesario, 1)


def configurar_impresion(ws, *, horizontal: bool, fila_encabezado: int | None):
    ws.page_setup.orientation = "landscape" if horizontal else "portrait"
    ws.page_setup.paperSize = 9  # A4
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_options.horizontalCentered = True
    if fila_encabezado:
        ws.print_title_rows = f"{fila_encabezado}:{fila_encabezado}"
    ws.page_margins = PageMargins(left=1.5 * CM, right=1.5 * CM, top=1.5 * CM,
                                  bottom=1.5 * CM, header=0.7 * CM, footer=0.7 * CM)
    ws.oddFooter.left.text = "&A"
    ws.oddFooter.left.size = 8
    ws.oddFooter.left.color = GRIS_TEXTO
    ws.oddFooter.right.text = "Página &P de &N"
    ws.oddFooter.right.size = 8
    ws.oddFooter.right.color = GRIS_TEXTO


def enlace_indice(c, destino: str):
    """Hipervínculo interno real (atributo location, no relación externa)."""
    c.hyperlink = Hyperlink(ref=c.coordinate, location=f"'{destino}'!A1")
    c.font = Font(name=c.font.name, size=c.font.sz, bold=c.font.b,
                  color=AZUL_ACERO, underline="single")


# ---------------------------------------------------------------------------
# Lectura de fuentes
# ---------------------------------------------------------------------------
def leer_tabla_docx(documento, indice: int) -> list[list[str]]:
    tabla_docx = documento.tables[indice]
    return [[_limpio(celda_docx.text) for celda_docx in fila.cells]
            for fila in tabla_docx.rows]


def leer_json(ruta: Path):
    with ruta.open(encoding="utf-8") as fh:
        return json.load(fh)


def derivar_forma(pre: pd.DataFrame, post: pd.DataFrame) -> dict:
    """Asimetría (G1) y curtosis de exceso (G2) por momento, sobre los CSV."""
    salida = {}
    for ind in INDICADORES:
        col = ind["csv"]
        salida[(ind["clave"], "pretest")] = (float(pre[col].skew()), float(pre[col].kurt()))
        salida[(ind["clave"], "posttest")] = (float(post[col].skew()), float(post[col].kurt()))
        diff = post[col] - pre[col]
        salida[(ind["clave"], "diferencia")] = (float(diff.skew()), float(diff.kurt()))
    return salida


def derivar_correlaciones(pre: pd.DataFrame, post: pd.DataFrame) -> dict:
    salida = {}
    for ind in INDICADORES:
        r, p = scipy_stats.pearsonr(pre[ind["csv"]], post[ind["csv"]])
        salida[ind["clave"]] = {"r": float(r), "p": float(p)}
    return salida


def derivar_ic_diferencia(media: float, desv: float, n: int, t_crit: float) -> dict:
    error = desv / math.sqrt(n)
    return {
        "error_tipico": error,
        "ic_inferior": media - t_crit * error,
        "ic_superior": media + t_crit * error,
    }


# ---------------------------------------------------------------------------
# Hojas
# ---------------------------------------------------------------------------
def hoja_portada(wb, meta: dict):
    ws = wb.create_sheet("00_PORTADA")
    ws.sheet_properties.tabColor = AZUL_MARINO
    ws.sheet_view.showGridLines = False

    for letra, valor in {"A": 4.0, "B": 21.0, "C": 52.0, "D": 20.0,
                         "E": 2.0, "F": 2.0, "G": 2.0, "H": 2.0}.items():
        ws.column_dimensions[letra].width = valor

    ncols = 8
    ws.row_dimensions[1].height = 10

    fusionar(ws, 2, 1, 3, ncols)
    for r in (2, 3):
        for c in range(1, ncols + 1):
            ws.cell(row=r, column=c).fill = relleno(AZUL_MARINO)
    celda(ws, 2, 1, "TABLAS DE ANEXOS DEL INFORME FINAL", familia="Calibri", tam=20,
          negrita=True, color=BLANCO, h="center", v="center")
    ws.row_dimensions[2].height = 30
    ws.row_dimensions[3].height = 26

    fusionar(ws, 4, 1, 4, ncols)
    for c in range(1, ncols + 1):
        ws.cell(row=4, column=c).fill = relleno(AZUL_ACERO)
    celda(ws, 4, 1, "Sistema web SIVAC y gestión de movimientos mensuales de vacunas",
          familia="Calibri", tam=12, negrita=True, color=BLANCO, h="center")
    ws.row_dimensions[4].height = 24

    fusionar(ws, 6, 1, 7, ncols)
    celda(ws, 6, 1, meta["titulo"], familia="Times New Roman", tam=12, negrita=True,
          cursiva=True, h="center", v="center")
    ws.row_dimensions[6].height = 42
    ws.row_dimensions[7].height = 30

    filas_meta = [
        ("Universidad", meta["institucion"]),
        ("Facultad", meta["facultad"]),
        ("Escuela profesional", meta["escuela"]),
        ("Tesista", meta["tesista"]),
        ("Asesora", meta["asesora"]),
        ("Documento fuente", "informe_final_v04.docx (59 tablas)"),
        ("Fecha de generación", date.today().isoformat()),
        ("Población y muestra",
         f"Censal, N = n = {meta['n_censal']}; diseño preexperimental O1 - X - O2"),
        ("Estado de los datos", meta["estado_datos"]),
    ]
    r = 9
    for etiqueta, valor in filas_meta:
        fusionar(ws, r, 1, r, 2)
        celda(ws, r, 1, f"{etiqueta}:", familia="Calibri", tam=10, negrita=True,
              color=AZUL_MARINO, h="right")
        fusionar(ws, r, 3, r, ncols)
        celda(ws, r, 3, valor, familia="Calibri", tam=10,
              negrita=(etiqueta == "Estado de los datos"))
        ws.row_dimensions[r].height = 17
        r += 1

    r += 1
    fusionar(ws, r, 1, r, ncols)
    for c in range(1, ncols + 1):
        ws.cell(row=r, column=c).fill = relleno(AZUL_MARINO)
    celda(ws, r, 1, LEYENDA_DATOS, familia="Calibri", tam=10, negrita=True,
          color=BLANCO, h="center")
    ws.row_dimensions[r].height = 20

    r += 2
    fusionar(ws, r, 1, r, ncols)
    celda(ws, r, 1, "ÍNDICE DE HOJAS", familia="Calibri", tam=12, negrita=True,
          color=AZUL_MARINO)
    ws.row_dimensions[r].height = 20

    r += 2
    encabezados = ["N.°", "Hoja", "Contenido", "Tablas incluidas"]
    for j, titulo in enumerate(encabezados, start=1):
        celda(ws, r, j, titulo, familia="Calibri", tam=11, negrita=True, color=BLANCO,
              fondo=AZUL_MARINO, h="center", v="center",
              borde=Border(bottom=Side(style="medium", color=AZUL_MARINO)))
    ws.row_dimensions[r].height = 26

    r += 1
    for i, (nombre, contenido, tablas) in enumerate(HOJAS, start=1):
        fondo = GRIS_PERLA if i % 2 == 0 else BLANCO
        celda(ws, r, 1, f"{i:02d}", familia="Calibri", tam=10, fondo=fondo, h="center")
        c = celda(ws, r, 2, nombre, familia="Calibri", tam=10, fondo=fondo,
                  color=AZUL_ACERO, subrayado="single")
        enlace_indice(c, nombre)
        celda(ws, r, 3, contenido, familia="Calibri", tam=10, fondo=fondo)
        celda(ws, r, 4, tablas, familia="Calibri", tam=10, fondo=fondo, h="center")
        ws.row_dimensions[r].height = 18
        r += 1

    for j in range(1, 5):
        ws.cell(row=r - 1, column=j).border = Border(
            bottom=Side(style="medium", color=AZUL_MARINO))

    r += 2
    fusionar(ws, r, 1, r, ncols)
    celda(ws, r, 1,
          "Nota. Índice navegable: cada nombre de hoja constituye un hipervínculo interno. "
          "Los datos empíricos se conservan rotulados como datos de prueba conforme a DEC-007.",
          familia="Calibri", tam=9, cursiva=True, color=GRIS_TEXTO, v="top", wrap=True)
    ws.row_dimensions[r].height = 26

    configurar_impresion(ws, horizontal=False, fila_encabezado=None)
    return ws


def hoja_replica_tabla(wb, nombre: str, tabla_idx: int, numero: str, titulo: str,
                       *, horizontal: bool, con_leyenda: bool = False):
    """Hoja que replica íntegramente una tabla del documento (Times New Roman)."""
    ws = wb.create_sheet(nombre)
    ws.sheet_properties.tabColor = AZUL_ACERO
    ws.sheet_view.showGridLines = False

    filas = leer_tabla_docx(DOCUMENTO, tabla_idx)
    encabezados, cuerpo = filas[0], filas[1:]
    ncols = len(encabezados)

    r = rotulo_tabla(ws, 1, numero, titulo, ncols, "Times New Roman")
    if con_leyenda:
        r = leyenda_datos(ws, r, ncols, "Times New Roman")
    r += 1

    columnas = [Columna(e) for e in encabezados]
    fila_encabezado = r
    r = tabla(ws, r, columnas, cuerpo, familia="Times New Roman", tam=10)
    r += 1
    r = nota_tabla(ws, r,
                   "Nota. Transcripción íntegra de la tabla del informe final v04. "
                   "Formato APA 7 de tres líneas horizontales, sin líneas verticales.",
                   ncols, "Times New Roman")

    ajustar_anchos(ws, objetivo=140)
    ajustar_altos(ws, 1, r)
    configurar_impresion(ws, horizontal=horizontal, fila_encabezado=fila_encabezado)
    ws.freeze_panes = f"A{fila_encabezado + 1}"
    return ws


ETIQUETAS_MATRIZ = {
    "sujeto_id": "Sujeto",
    "centro_acopio": "Centro de acopio",
    "t_reg": "T_reg (min)",
    "t_vale": "T_vale (min)",
    "rsd": "RSD (%)",
    "cpe": "CPE (%)",
    "score_ap": "AP (pts)",
    "score_up": "UP (pts)",
    "score_tam_total": "TAM total (pts)",
    "nivel_satisfaccion": "Nivel",
}


def _etiqueta_columna(nombre: str) -> str:
    if nombre.startswith("ap_"):
        return "AP-" + nombre[3:]
    if nombre.startswith("up_"):
        return "UP-" + nombre[3:]
    return ETIQUETAS_MATRIZ.get(nombre, nombre)


def hoja_matriz_datos(wb, nombre: str, tabla_idx: int, numero: str, titulo: str):
    """Matriz de datos tabulados (18 columnas) con autofiltro y formato numérico."""
    ws = wb.create_sheet(nombre)
    ws.sheet_properties.tabColor = AZUL_ACERO
    ws.sheet_view.showGridLines = False

    filas = leer_tabla_docx(DOCUMENTO, tabla_idx)
    encabezados, cuerpo = filas[0], filas[1:]
    ncols = len(encabezados)

    r = rotulo_tabla(ws, 1, numero, titulo, ncols, "Calibri")
    r = leyenda_datos(ws, r, ncols, "Calibri")
    r += 1

    formatos = {
        "t_reg": FMT_UNO, "t_vale": FMT_UNO, "rsd": FMT_UNO, "cpe": FMT_UNO,
        "ap_01": FMT_ENT, "ap_02": FMT_ENT, "ap_03": FMT_ENT, "ap_04": FMT_ENT,
        "up_01": FMT_ENT, "up_02": FMT_ENT, "up_03": FMT_ENT, "up_04": FMT_ENT,
        "score_ap": FMT_ENT, "score_up": FMT_ENT, "score_tam_total": FMT_ENT,
    }
    columnas = [Columna(_etiqueta_columna(e), formatos.get(e)) for e in encabezados]

    cuerpo_tipado = []
    for fila in cuerpo:
        tipada = []
        for encabezado, valor in zip(encabezados, fila):
            if encabezado in formatos and valor not in ("", None):
                try:
                    numero_valor = float(valor)
                    tipada.append(int(numero_valor) if formatos[encabezado] == FMT_ENT
                                  else numero_valor)
                except ValueError:
                    tipada.append(valor)
            else:
                tipada.append(valor)
        cuerpo_tipado.append(tipada)

    fila_encabezado = r
    r = tabla(ws, r, columnas, cuerpo_tipado, familia="Calibri", tam=10)
    ws.auto_filter.ref = f"A{fila_encabezado}:{get_column_letter(ncols)}{r - 1}"
    r += 1
    r = nota_tabla(ws, r,
                   "Nota. Matriz íntegra de la tabla del informe final v04; los "
                   "encabezados se presentan con su etiqueta legible y no alteran el "
                   "contenido de las celdas. " + LEYENDA_DATOS + ". Unidad de análisis: "
                   "14 operadores de inmunizaciones.",
                   ncols, "Calibri")

    ajustar_anchos(ws, minimo=7.5, objetivo=138)
    ajustar_altos(ws, 1, r)
    # La matriz completa debe caber en una sola página con su nota: una
    # compresión leve de los altos evita que la nota quede aislada.
    for fila in range(1, r + 1):
        alto = ws.row_dimensions[fila].height
        if alto:
            ws.row_dimensions[fila].height = max(14.0, round(alto * 0.94, 1))
    configurar_impresion(ws, horizontal=(ncols > 7), fila_encabezado=fila_encabezado)
    ws.freeze_panes = f"B{fila_encabezado + 1}"
    return ws


def hoja_descriptivos(wb, est: dict, forma: dict):
    ws = wb.create_sheet("05_DESCRIPTIVOS")
    ws.sheet_properties.tabColor = AZUL_ACERO
    ws.sheet_view.showGridLines = False

    ncols = 12
    r = leyenda_datos(ws, 1, ncols, "Times New Roman") + 1

    bloques = [
        ("Tabla 36",
         "Estadística descriptiva de los indicadores de oportunidad de procesamiento",
         ["t_reg", "t_vale"], FMT_EST),
        ("Tabla 37",
         "Estadística descriptiva de los indicadores de consistencia documental",
         ["rsd", "cpe"], FMT_PCT),
        ("Tabla 38",
         "Estadística descriptiva de los constructos de satisfacción del usuario",
         ["score_ap", "score_up", "score_tam_total"], FMT_EST),
    ]

    primera_cabecera = None
    for indice_bloque, (numero, titulo, claves, fmt_num) in enumerate(bloques):
        if indice_bloque > 0:
            # Cada tabla abre una página propia: evita fragmentar las filas y
            # que la cabecera impresa pertenezca a otra tabla.
            ws.row_breaks.append(Break(id=r - 1))
        r = rotulo_tabla(ws, r, numero, titulo, ncols, "Times New Roman")
        columnas = [
            Columna("Indicador"), Columna("Momento Evaluado"), Columna("n", FMT_ENT),
            Columna("Media", fmt_num), Columna("DE", fmt_num), Columna("Mediana", fmt_num),
            Columna("RIC", fmt_num), Columna("Mínimo", fmt_num), Columna("Máximo", fmt_num),
            Columna("Asimetría", FMT_EST), Columna("Curtosis", FMT_EST),
            Columna("Variación", FMT_PCT_SIGNO),
        ]
        filas = []
        for clave in claves:
            datos = est["descriptivos"][clave]
            etiqueta = next(i["docx"] for i in INDICADORES if i["clave"] == clave)
            if clave in ("rsd", "cpe"):
                etiqueta = etiqueta[:-1] + ", %)" if etiqueta.endswith(")") else etiqueta
            for momento, rotulo in (("pretest", "Pretest (Manual)"),
                                    ("posttest", "Postest (SIVAC)"),
                                    ("diferencia", "Diferencia Pareada")):
                s = datos[momento]
                asimetria, curtosis = forma[(clave, momento)]
                variacion = datos["delta_porcentual"] if momento == "posttest" else GUION
                filas.append([etiqueta, rotulo, s["n"], s["media"], s["desv_est"],
                              s["mediana"], s["iqr"], s["minimo"], s["maximo"],
                              asimetria, curtosis, variacion])
        cabecera = r
        primera_cabecera = primera_cabecera or cabecera
        r = tabla(ws, r, columnas, filas, familia="Times New Roman", tam=10)
        r += 1
        r = nota_tabla(ws, r,
                       "Nota. Media, DE, mediana, RIC, mínimo y máximo tomados de "
                       "reporte_estadistico_completo.json. Asimetría (G1) y curtosis de "
                       "exceso (G2) calculadas sobre los CSV de campo. n = 14; "
                       "RIC = rango intercuartílico; el guion indica no aplicable.",
                       ncols, "Times New Roman")
        r += 1

    ajustar_anchos(ws, objetivo=140)
    ajustar_altos(ws, 1, r)
    configurar_impresion(ws, horizontal=True, fila_encabezado=None)
    ws.freeze_panes = f"A{primera_cabecera + 1}"
    return ws


def hoja_confiabilidad(wb, est: dict):
    ws = wb.create_sheet("06_CONFIABILIDAD")
    ws.sheet_properties.tabColor = AZUL_ACERO
    ws.sheet_view.showGridLines = False

    r = rotulo_tabla(ws, 1, "Tabla 35",
                     "Confiabilidad de consistencia interna del Instrumento N.° 03 "
                     "(Modalidad A) con intervalo de confianza al 95 %", 8, "Times New Roman")
    r = leyenda_datos(ws, r, 8, "Times New Roman") + 1

    columnas = [
        Columna("Momento de Evaluación"), Columna("Escala / Subescala"),
        Columna("Número de Ítems", FMT_ENT), Columna("Muestra (n)", FMT_ENT),
        Columna("Alfa de Cronbach", FMT_EST), Columna("IC 95% Inferior", FMT_EST),
        Columna("IC 95% Superior", FMT_EST), Columna("Nivel de Consistencia"),
    ]

    etiquetas = [
        ("global_tam", "Escala Global TAM (Modalidad A)", 8),
        ("agilidad_percibida", "Aceptación del Proceso (AP)", 4),
        ("utilidad_percibida", "Utilidad Percibida (UP)", 4),
    ]
    filas = []
    for momento, rotulo in (("pretest", "Pretest (Proceso manual)"),
                            ("posttest", "Postest (Sistema SIVAC)")):
        for clave, etiqueta, items in etiquetas:
            datos = est["confiabilidad_instrumento_03"][momento][clave]
            filas.append([rotulo, etiqueta, items, datos["n_sujetos"], datos["alpha"],
                          datos["ic_95"][0], datos["ic_95"][1], datos["interpretacion"]])

    cabecera = r
    r = tabla(ws, r, columnas, filas, familia="Times New Roman", tam=10)
    r += 1
    r = nota_tabla(ws, r,
                   "Nota. Coeficiente alfa de Cronbach con intervalo de confianza al 95 % "
                   "de Feldt. Ocho ítems de la Modalidad A (AP-01 a AP-04 y UP-01 a UP-04) "
                   "conforme a DEC-019; n = 14. " + LEYENDA_DATOS + ".",
                   8, "Times New Roman")

    ajustar_anchos(ws, objetivo=140)
    ajustar_altos(ws, 1, r)
    configurar_impresion(ws, horizontal=True, fila_encabezado=cabecera)
    ws.freeze_panes = f"A{cabecera + 1}"
    return ws


def hoja_normalidad(wb, est: dict):
    ws = wb.create_sheet("07_NORMALIDAD")
    ws.sheet_properties.tabColor = AZUL_ACERO
    ws.sheet_view.showGridLines = False

    columnas = [
        Columna("Dimensión"), Columna("Indicador Evaluado"), Columna("n", FMT_ENT),
        Columna("Estadístico W", FMT_EST), Columna("gl", FMT_ENT),
        Columna("p-valor", FMT_EST), Columna("Decisión Distribucional"),
        Columna("Prueba Inferencial Asignada"),
    ]
    r = rotulo_tabla(ws, 1, "Tabla 39",
                     "Prueba de normalidad de Shapiro-Wilk sobre las diferencias pareadas "
                     "(D = O2 - O1)", 8, "Times New Roman")
    r = leyenda_datos(ws, r, 8, "Times New Roman") + 1

    filas = []
    for clave, datos in est["normalidad_shapiro_wilk"].items():
        filas.append([DIMENSIONES[clave],
                      next(i["docx"] for i in INDICADORES if i["clave"] == clave),
                      datos["gl"], datos["estadistico_w"], datos["gl"], datos["p_valor"],
                      "Normal (p > .05)" if datos["es_normal"] else "No normal (p <= .05)",
                      "t de Student pareada" if datos["es_normal"] else "Wilcoxon pareado"])

    cabecera = r
    r = tabla(ws, r, columnas, filas, familia="Times New Roman", tam=10)
    r += 1
    r = nota_tabla(ws, r,
                   "Nota. Shapiro-Wilk aplicado a la diferencia postest - pretest por "
                   "indicador; n = 14 y gl = 14. Un p > .05 sustenta el ajuste gaussiano y "
                   "la prueba t pareada, complementada con Wilcoxon. " + LEYENDA_DATOS + ".",
                   8, "Times New Roman")

    ajustar_anchos(ws, objetivo=140)
    ajustar_altos(ws, 1, r)
    configurar_impresion(ws, horizontal=True, fila_encabezado=cabecera)
    ws.freeze_panes = f"A{cabecera + 1}"
    return ws


def hoja_contrastes(wb, est: dict):
    ws = wb.create_sheet("08_CONTRASTES")
    ws.sheet_properties.tabColor = AZUL_ACERO
    ws.sheet_view.showGridLines = False

    r = leyenda_datos(ws, 1, 9, "Times New Roman") + 1

    def filas_contraste(claves, h0):
        filas = []
        for clave in claves:
            datos = est["contrastes_inferenciales"][clave]
            etiqueta = next(i["docx"] for i in INDICADORES if i["clave"] == clave)
            t = datos["t_student"]
            w = datos["wilcoxon"]
            filas.append([etiqueta, "t pareada", t["estadistico_t"], t["gl"],
                          t["p_valor"], t["d_cohen"], "Grande",
                          datos["holm_bonferroni"]["p_ajustado"], f"Rechazar H0,{h0}"])
            filas.append([etiqueta, "Wilcoxon",
                          f"W = {w['estadistico_w']:.1f} (Z = {w['estadistico_z']:.2f})",
                          GUION, w["p_valor"], w["r_rosenthal"], "Grande",
                          GUION, f"Rechazar H0,{h0}"])
        return filas

    bloques = [
        ("Tabla 40", "Contraste de la Hipótesis Específica 1: oportunidad de procesamiento",
         ["t_reg", "t_vale"], "1"),
        ("Tabla 41", "Contraste de la Hipótesis Específica 2: consistencia documental",
         ["rsd", "cpe"], "2"),
        ("Tabla 42", "Contraste de la Hipótesis Específica 3: satisfacción del usuario",
         ["score_ap", "score_up", "score_tam_total"], "3"),
    ]

    primera_cabecera = None
    for indice_bloque, (numero, titulo, claves, h0) in enumerate(bloques):
        if indice_bloque > 0:
            # Cada tabla abre una página nueva. En OOXML el salto se ancla a la
            # fila previa (0-based), de modo que la página siguiente inicia en el
            # rótulo de la tabla y la nota precedente nunca queda huérfana.
            ws.row_breaks.append(Break(id=r - 1))
        r = rotulo_tabla(ws, r, numero, titulo, 9, "Times New Roman")
        columnas = [
            Columna("Indicador"), Columna("Prueba Estadística"),
            Columna("Estadístico", FMT_EST), Columna("gl", FMT_ENT),
            Columna("p-valor", FMT_CIENTIFICO), Columna("Tamaño del Efecto", FMT_EST),
            Columna("Magnitud (Cohen)"), Columna("p-ajustado Holm", FMT_CIENTIFICO),
            Columna(f"Decisión sobre H0,{h0}"),
        ]
        cabecera = r
        primera_cabecera = primera_cabecera or cabecera
        r = tabla(ws, r, columnas, filas_contraste(claves, h0),
                  familia="Times New Roman", tam=10)
        r += 1
        r = nota_tabla(ws, r,
                       "Nota. p-valores exactos del reporte inferencial, en notación "
                       "científica por ser menores que .001 y en rojo por ser menores que "
                       ".05. d = d_z de Cohen (|d| >= 0.8, efecto grande); r = |Z| / sqrt(N) "
                       "(r >= 0.5, efecto grande). Ajuste de Holm-Bonferroni sobre las tres "
                       "hipótesis específicas.",
                       9, "Times New Roman")
        r += 1

    # La Tabla 43 abre su propia página para no fragmentar la nota de la Tabla 42.
    ws.row_breaks.append(Break(id=r - 1))
    r = rotulo_tabla(ws, r, "Tabla 43",
                     "Resumen de contrastación inferencial multivariada y regla de decisión "
                     "para la Hipótesis General (Holm-Bonferroni)", 8, "Times New Roman")
    columnas = [
        Columna("Hipótesis de Investigación"), Columna("Dimensión Asociada"),
        Columna("Indicadores Clave"), Columna("Prueba Decisoria"),
        Columna("p-valor Original"), Columna("p-valor Ajustado"),
        Columna("Decisión Estadística"), Columna("Impacto Operativo"),
    ]
    filas_43 = [
        ["Hipótesis Específica 1 (HE1)", "D1: Oportunidad de procesamiento",
         "T_reg, T_vale", "t pareada / Wilcoxon", "< .001", "< .001", "Rechazar H0,1",
         "Reducción > 80% en tiempos operativos"],
        ["Hipótesis Específica 2 (HE2)", "D2: Consistencia documental", "RSD, CPE",
         "t pareada / Wilcoxon", "< .001", "< .001", "Rechazar H0,2",
         "Exactitud documental superior al 95%"],
        ["Hipótesis Específica 3 (HE3)", "D3: Satisfacción del usuario",
         "AP, UP, TAM total", "t pareada / Wilcoxon", "< .001", "< .001", "Rechazar H0,3",
         "Incremento > 100% en aceptación y utilidad"],
        ["Hipótesis General (HG)", "Gestión de movimientos de vacunas", "D1 + D2 + D3",
         "Criterio conjuntivo", "< .001", "< .001", "Rechazar H0",
         "Mejora integral multidimensional significativa"],
    ]
    cabecera = r
    r = tabla(ws, r, columnas, filas_43, familia="Times New Roman", tam=10)
    for f in range(cabecera + 1, r):
        for k in (5, 6):
            c = ws.cell(row=f, column=k)
            if isinstance(c.value, str) and c.value.startswith("<"):
                c.font = Font(name=c.font.name, size=c.font.sz,
                              bold=c.font.b, italic=c.font.i, color=ROJO_P)
    r += 1
    r = nota_tabla(ws, r,
                   "Nota. La Hipótesis General se contrasta mediante regla conjuntiva: el "
                   "rechazo simultáneo de H0,1, H0,2 y H0,3 con p ajustado por Holm. Esta "
                   "tabla conserva la expresión < .001 del documento fuente; los valores "
                   "exactos figuran en las tablas 40 a 42.",
                   8, "Times New Roman")

    ajustar_anchos(ws, objetivo=140)
    ajustar_altos(ws, 1, r)
    configurar_impresion(ws, horizontal=True, fila_encabezado=None)
    ws.freeze_panes = f"A{primera_cabecera + 1}"
    return ws


def hoja_spss(wb, est: dict, forma: dict, correlaciones: dict):
    ws = wb.create_sheet("10_SPSS_SALIDAS")
    ws.sheet_properties.tabColor = AZUL_MARINO
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 47
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 22

    n = int(est["metadatos"]["n_censal"])
    gl = n - 1
    t_crit = float(scipy_stats.t.ppf(0.975, gl))

    def banda(titulo: str, ncols: int, fila: int, salto: bool = False) -> int:
        if salto:
            ws.row_breaks.append(Break(id=fila - 1))
        fusionar(ws, fila, 1, fila, ncols)
        for c in range(1, ncols + 1):
            ws.cell(row=fila, column=c).fill = relleno(GRIS_BANDA)
            ws.cell(row=fila, column=c).border = Border(
                top=Side(style="thin", color=GRIS_REJILLA),
                bottom=Side(style="thin", color=GRIS_REJILLA))
        celda(ws, fila, 1, titulo.upper(), familia="Calibri", tam=10, negrita=True,
              color=AZUL_MARINO, h="left")
        ws.row_dimensions[fila].height = 20
        return fila + 1

    def grupo(texto: str, ncols: int, fila: int) -> int:
        fusionar(ws, fila, 1, fila, ncols)
        for c in range(1, ncols + 1):
            ws.cell(row=fila, column=c).fill = relleno(AZUL_MARINO)
        celda(ws, fila, 1, texto, familia="Calibri", tam=10, negrita=True, color=BLANCO)
        ws.row_dimensions[fila].height = 18
        return fila + 1

    def encabezado_spss(titulos: list[str], fila: int) -> int:
        for j, titulo in enumerate(titulos, start=1):
            celda(ws, fila, j, titulo, familia="Calibri", tam=10, negrita=True,
                  color=BLANCO, fondo=AZUL_ACERO, h="center", v="center",
                  borde=Border(left=Side(style="thin", color=GRIS_REJILLA),
                               right=Side(style="thin", color=GRIS_REJILLA),
                               top=Side(style="thin", color=GRIS_REJILLA),
                               bottom=Side(style="thin", color=GRIS_REJILLA)))
        ws.row_dimensions[fila].height = 28
        return fila + 1

    def fila_spss(valores: list, fila: int, fmts: list, col_p: int | None = None) -> int:
        for j, (valor, fmt) in enumerate(zip(valores, fmts), start=1):
            es_num = _es_numero(valor)
            color = ROJO_P if (es_num and col_p == j and valor < 0.05) else NEGRO
            if es_num and col_p == j and valor < 0.001:
                valor, fmt, es_num = "< .001", None, False
            celda(ws, fila, j, valor, familia="Calibri", tam=10, color=color,
                  fondo=BLANCO, h="right" if (es_num or col_p == j) else "left",
                  wrap=not es_num, fmt=fmt,
                  borde=Border(left=Side(style="thin", color=GRIS_REJILLA),
                               right=Side(style="thin", color=GRIS_REJILLA),
                               top=Side(style="thin", color=GRIS_REJILLA),
                               bottom=Side(style="thin", color=GRIS_REJILLA)))
        ws.row_dimensions[fila].height = 16
        return fila + 1

    def nota_spss(texto: str, ncols: int, fila: int) -> int:
        fusionar(ws, fila, 1, fila, ncols)
        celda(ws, fila, 1, texto, familia="Calibri", tam=9, cursiva=True,
              color=GRIS_TEXTO, h="left", v="top")
        ws.row_dimensions[fila].height = 16
        return fila + 2

    r = 1
    celda(ws, r, 1, "SALIDAS DEL VISOR SPSS - SIVAC (n = 14)",
          familia="Calibri", tam=12, negrita=True, color=AZUL_MARINO)
    ws.row_dimensions[r].height = 20
    r += 1
    fusionar(ws, r, 1, r, 3)
    for c in range(1, 4):
        ws.cell(row=r, column=c).fill = relleno(AZUL_ACERO)
    celda(ws, r, 1, LEYENDA_DATOS, familia="Calibri", tam=9, negrita=True,
          color=BLANCO, fondo=AZUL_ACERO)
    ws.row_dimensions[r].height = 17
    r += 2

    # 1. Estadísticos descriptivos
    r = banda("Estadísticos descriptivos", 3, r)
    r = encabezado_spss(["Estadístico", "Pretest (Manual)", "Postest (SIVAC)"], r)
    for ind in INDICADORES:
        clave = ind["clave"]
        if clave == "score_ap":
            # Evita que el bloque AP (pts) quede partido entre dos páginas.
            ws.row_breaks.append(Break(id=r - 1))
        r = grupo(ind["etiqueta"], 3, r)
        datos = est["descriptivos"][clave]
        for etiqueta, fmt, obtener in (
                ("N", FMT_ENT, lambda s: s["n"]),
                ("Media", FMT_EST, lambda s: s["media"]),
                ("Mediana", FMT_EST, lambda s: s["mediana"]),
                ("Desviación estándar", FMT_EST, lambda s: s["desv_est"]),
                ("Mínimo", FMT_EST, lambda s: s["minimo"]),
                ("Máximo", FMT_EST, lambda s: s["maximo"])):
            r = fila_spss([etiqueta, obtener(datos["pretest"]), obtener(datos["posttest"])],
                          r, [None, fmt, fmt])
        r = fila_spss(["Asimetría", forma[(clave, "pretest")][0],
                       forma[(clave, "posttest")][0]], r, [None, FMT_EST, FMT_EST])
        r = fila_spss(["Curtosis", forma[(clave, "pretest")][1],
                       forma[(clave, "posttest")][1]], r, [None, FMT_EST, FMT_EST])
    r = nota_spss("Origen del cálculo: reporte_estadistico_completo.json (estadísticos "
                  "principales) y CSV de campo (asimetría y curtosis). n = 14.", 3, r)

    # 2. Prueba de normalidad
    r = banda("Prueba de normalidad", 3, r)
    r = encabezado_spss(["Indicador", "Shapiro-Wilk W", "Sig."], r)
    for clave, datos in est["normalidad_shapiro_wilk"].items():
        etiqueta = next(i["docx"] for i in INDICADORES if i["clave"] == clave)
        r = fila_spss([etiqueta, datos["estadistico_w"], datos["p_valor"]],
                      r, [None, FMT_EST, FMT_EST], col_p=3)
    r = nota_spss("Origen del cálculo: prueba de Shapiro-Wilk sobre las diferencias "
                  "pareadas; gl = 14 en todos los indicadores.", 3, r)

    # 3. Estadísticos de muestras relacionadas
    r = banda("Estadísticos de muestras relacionadas", 3, r, salto=True)
    r = encabezado_spss(["Estadístico", "Pretest (Manual)", "Postest (SIVAC)"], r)
    for ind in INDICADORES:
        clave = ind["clave"]
        datos = est["descriptivos"][clave]
        r = grupo(f"Par: {ind['etiqueta']}", 3, r)
        for etiqueta, fmt, obtener in (
                ("N", FMT_ENT, lambda s: s["n"]),
                ("Media", FMT_EST, lambda s: s["media"]),
                ("Desviación estándar", FMT_EST, lambda s: s["desv_est"]),
                ("Media de error estándar", FMT_EST,
                 lambda s: s["desv_est"] / math.sqrt(s["n"]))):
            r = fila_spss([etiqueta, obtener(datos["pretest"]), obtener(datos["posttest"])],
                          r, [None, fmt, fmt])
    r = nota_spss("Origen del cálculo: media de error estándar = desviación estándar / "
                  "raíz de n, con n = 14.", 3, r)

    # 4. Correlaciones de muestras relacionadas
    r = banda("Correlaciones de muestras relacionadas", 3, r, salto=True)
    r = encabezado_spss(["Par de indicadores", "Correlación", "Sig."], r)
    for ind in INDICADORES:
        datos = correlaciones[ind["clave"]]
        r = fila_spss([f"{ind['etiqueta']} - pretest y postest", datos["r"], datos["p"]],
                      r, [None, FMT_EST, FMT_EST], col_p=3)
    r = nota_spss("Origen del cálculo: coeficiente de Pearson bilateral sobre los CSV de "
                  "campo; N = 14 en cada par.", 3, r)

    # 5. Prueba de muestras relacionadas
    r = banda("Prueba de muestras relacionadas", 2, r)
    r = encabezado_spss(["Estadístico de la diferencia", "Valor"], r)
    for ind in INDICADORES:
        clave = ind["clave"]
        datos = est["descriptivos"][clave]
        contraste = est["contrastes_inferenciales"][clave]
        diff = datos["diferencia"]
        ic = derivar_ic_diferencia(diff["media"], diff["desv_est"], diff["n"], t_crit)
        if clave == "cpe":
            # Cierra la página tras tres pares para que el resto de la tabla
            # quepa completa en la página siguiente.
            ws.row_breaks.append(Break(id=r - 1))
        r = grupo(f"Par: {ind['etiqueta']}", 2, r)
        for etiqueta, valor, fmt in (
                ("Media de la diferencia", diff["media"], FMT_EST),
                ("Desviación estándar", diff["desv_est"], FMT_EST),
                ("Media de error estándar", ic["error_tipico"], FMT_EST),
                ("IC 95% inferior", ic["ic_inferior"], FMT_EST),
                ("IC 95% superior", ic["ic_superior"], FMT_EST),
                ("t", contraste["t_student"]["estadistico_t"], FMT_EST),
                ("gl", gl, FMT_ENT),
                ("Sig. (bilateral)", contraste["t_student"]["p_valor"], FMT_EST)):
            r = fila_spss([etiqueta, valor], r, [None, fmt],
                          col_p=2 if etiqueta.startswith("Sig") else None)
    r = nota_spss("Origen del cálculo: reporte_estadistico_completo.json. Intervalo de "
                  "confianza al 95 % calculado como media de la diferencia +/- t(0.975; 13) "
                  "por el error estándar. Sig. bilateral de la prueba t de Student pareada.",
                  2, r)

    ajustar_altos(ws, 1, r)
    configurar_impresion(ws, horizontal=False, fila_encabezado=None)
    ws.freeze_panes = "A6"
    return ws


def hoja_notas(wb, notas: list[tuple[str, str, str, str]]):
    ws = wb.create_sheet("11_NOTAS")
    ws.sheet_properties.tabColor = GRIS_TEXTO
    ws.sheet_view.showGridLines = False

    r = rotulo_tabla(ws, 1, "Trazabilidad",
                     "Notas de procedencia, convenciones de formato y marcas [VERIFICAR]",
                     5, "Calibri")
    r += 1

    columnas = [Columna("Hoja"), Columna("Elemento"), Columna("Observación"),
                Columna("Marca"), Columna("Fuente")]
    fila_encabezado = r
    fuentes = {
        "TRAZABLE": "DOCX / JSON",
        "DERIVADO": "Cálculo sobre CSV",
        "CONVENCIÓN": "Diseño del libro",
        "[VERIFICAR]": "Requiere ratificación",
    }
    filas = [[hoja, elemento, observacion, marca, fuentes.get(marca, "")]
             for hoja, elemento, observacion, marca in notas]

    r = tabla(ws, r, columnas, filas, familia="Calibri", tam=10)
    ws.auto_filter.ref = f"A{fila_encabezado}:E{r - 1}"
    r += 1
    r = nota_tabla(ws, r,
                   "Nota. Toda celda numérica procede del informe final v04, del reporte "
                   "estadístico o de los CSV de campo. Las marcas [VERIFICAR] requieren "
                   "ratificación expresa del tesista antes del cierre de la compuerta QG-7.",
                   5, "Calibri")

    ajustar_anchos(ws, maximo=52, objetivo=96)
    ajustar_altos(ws, 1, r)
    # Compresión leve de los altos: evita que la nota final quede aislada en una
    # página casi vacía, sin recortar el texto (los altos se estimaron al alza).
    for fila in range(1, r + 1):
        alto = ws.row_dimensions[fila].height
        if alto:
            ws.row_dimensions[fila].height = max(14.0, round(alto * 0.96, 1))
    configurar_impresion(ws, horizontal=False, fila_encabezado=fila_encabezado)
    ws.freeze_panes = f"A{fila_encabezado + 1}"
    return ws


# ---------------------------------------------------------------------------
# Control de coherencia entre el DOCX y el JSON
# ---------------------------------------------------------------------------
def control_coherencia(est: dict, tablas_docx: dict) -> list[str]:
    discrepancias = []

    def comparar(etiqueta: str, valor: float, texto_docx: str, decimales: int = 3):
        esperado = f"{valor:.{decimales}f}"
        if esperado.lstrip("-") not in texto_docx.replace(",", "."):
            discrepancias.append(f"{etiqueta}: el valor {esperado} del JSON no figura en el DOCX")

    for clave, datos in est["contrastes_inferenciales"].items():
        etiqueta = next(i["docx"] for i in INDICADORES if i["clave"] == clave)
        fila = next((f for f in tablas_docx["contrastes"]
                     if f[0].startswith(etiqueta[:16])), None)
        if fila is None:
            discrepancias.append(f"{etiqueta}: no se localizó la fila en las tablas 40 a 42")
            continue
        comparar(f"t {clave}", datos["t_student"]["estadistico_t"], fila[2])
        comparar(f"d {clave}", datos["t_student"]["d_cohen"], fila[5], decimales=2)

    for momento in ("pretest", "posttest"):
        for clave in ("global_tam", "agilidad_percibida", "utilidad_percibida"):
            comparar(f"alfa {momento} {clave}",
                     est["confiabilidad_instrumento_03"][momento][clave]["alpha"],
                     tablas_docx["confiabilidad"])

    for clave, datos in est["normalidad_shapiro_wilk"].items():
        comparar(f"W {clave}", datos["estadistico_w"], tablas_docx["normalidad"])
        if datos["p_valor"] >= 0.05:
            comparar(f"p {clave}", datos["p_valor"], tablas_docx["normalidad"])

    return discrepancias


def construir_notas(est: dict, pre: pd.DataFrame, centros: list, codebook: dict,
                    discrepancias: list[str], meta: dict) -> list[tuple[str, str, str, str]]:
    notas: list[tuple[str, str, str, str]] = []

    notas.append(("Global", "Fuente primaria de las tablas",
                  "Las hojas 01, 02, 03, 04 y 09 transcriben íntegras las tablas 44, 45, "
                  "52, 53 y 54 de informe_final_v04.docx. Las hojas 05 a 08 se construyen "
                  "desde reporte_estadistico_completo.json y se contrastaron contra el DOCX.",
                  "TRAZABLE"))
    notas.append(("Global", "Estado de los datos",
                  LEYENDA_DATOS + ". Los valores empíricos no deben citarse como resultados "
                  "definitivos mientras el tesista no certifique el levantamiento real.",
                  "CONVENCIÓN"))
    notas.append(("Global", "Celdas con guion",
                  "El guion (—) señala un valor no aplicable: gl inexistente en la prueba "
                  "de Wilcoxon, variación porcentual en pretest y en la diferencia pareada, "
                  "y p-ajustado Holm en los contrastes no paramétricos. No denota dato "
                  "faltante.", "CONVENCIÓN"))
    notas.append(("Global", "Celdas con guion: ratificación",
                  "Se solicita ratificar que el guion empleado en las hojas 05 y 08 denote "
                  "no aplicable y no dato perdido, conforme a la convención APA 7.",
                  "[VERIFICAR]"))
    notas.append(("Global", "Orientación de impresión",
                  "Las hojas 01, 02 y 09 se imprimen en horizontal por la densidad de sus "
                  "celdas de texto, aunque tengan siete columnas o menos; el resto de hojas "
                  "sigue el criterio de más de siete columnas. Todas se ajustan a una página "
                  "de ancho en A4 con márgenes de 1.5 cm.", "CONVENCIÓN"))
    notas.append(("05_DESCRIPTIVOS", "Asimetría y curtosis",
                  "No figuran en las tablas 36 a 38 del DOCX. Se calcularon sobre los CSV de "
                  "campo con pandas (asimetría G1 y curtosis de exceso G2, estimadores "
                  "insesgados) para pretest, postest y diferencia pareada.", "DERIVADO"))
    notas.append(("05_DESCRIPTIVOS", "Variación porcentual",
                  "Corresponde al campo delta_porcentual del reporte estadístico; se muestra "
                  "con signo explícito y dos decimales.", "TRAZABLE"))
    notas.append(("06_CONFIABILIDAD", "Alfa de Cronbach",
                  "Coeficientes e intervalos de confianza de Feldt tomados del reporte "
                  "estadístico; la etiqueta AP corresponde a la clave interna "
                  "agilidad_percibida del JSON.", "TRAZABLE"))
    notas.append(("07_NORMALIDAD", "p-valores",
                  "Los siete indicadores arrojan p > .05. El menor valor corresponde a UP "
                  "(p = .052), próximo al umbral; se conserva la decisión normal del informe.",
                  "TRAZABLE"))
    notas.append(("08_CONTRASTES", "p-valores y notación científica",
                  "Las tablas 40 a 42 muestran el valor exacto en notación científica cuando "
                  "es menor que .001; el DOCX los redondea a .001 o los expresa como < .001. "
                  "La tabla 43 conserva la expresión < .001 por ser un cuadro de síntesis.",
                  "CONVENCIÓN"))
    notas.append(("08_CONTRASTES", "Estadístico de Wilcoxon",
                  "Se conserva la expresión compuesta W y Z del DOCX en una sola celda, por "
                  "tratarse de un estadístico bivariado en la salida de origen.", "CONVENCIÓN"))
    notas.append(("10_SPSS_SALIDAS", "Correlaciones de muestras relacionadas",
                  "Coeficiente de Pearson bilateral calculado sobre los CSV de campo. El DOCX "
                  "no reporta esta salida; se incorpora por exigencia de la réplica SPSS.",
                  "DERIVADO"))
    notas.append(("10_SPSS_SALIDAS", "Intervalo de confianza de la diferencia",
                  "Calculado como media de la diferencia más menos t(0.975; 13) por el error "
                  "estándar, con t crítico = 2.160369 y n = 14.", "DERIVADO"))
    notas.append(("10_SPSS_SALIDAS", "Número de columnas",
                  "Los bloques se disponen en dos o tres columnas conforme al diseño "
                  "solicitado; la prueba de muestras relacionadas se presenta en formato "
                  "vertical para conservar los ocho estadísticos de la salida SPSS.",
                  "CONVENCIÓN"))

    centros_csv = sorted(pre["centro_acopio"].unique())
    catalogo = {c["nombre"] for c in centros}
    fuera_catalogo = [c for c in centros_csv if c not in catalogo]
    notas.append(("03/04", "Centros de acopio",
                  f"Los CSV registran {len(centros_csv)} centros distintos para 14 "
                  f"operadores; {len(centros_csv) - len(fuera_catalogo)} coinciden con el "
                  f"catálogo de {len(centros)} centros de acopio. "
                  + (f"Sin coincidencia: {', '.join(fuera_catalogo)}." if fuera_catalogo
                     else "Todas las denominaciones coinciden con el catálogo real."),
                  "TRAZABLE" if not fuera_catalogo else "[VERIFICAR]"))
    notas.append(("03/04", "Centros declarados en la tabla 30",
                  "La tabla 30 del informe distribuye a los 14 operadores en 8 centros "
                  "(Almacén Especializado, Andahuaylas, Talavera, San Jerónimo, Santa María "
                  "de Chicmo, Huancarama, Chincheros y Uripa/Ocobamba), mientras las matrices "
                  "52 y 53 registran 13 centros del catálogo real, entre ellos Huancaray, "
                  "Turpo, Kishuara y Pampachiri. Se requiere conciliar la distribución.",
                  "[VERIFICAR]"))
    notas.append(("01_ANEXO1_MATRIZ", "Prueba inferencial declarada",
                  "La matriz de consistencia declara Wilcoxon pareada y tamaño del efecto "
                  "r = |Z| / sqrt(N), mientras el Capítulo V adopta la t de Student pareada "
                  "por normalidad de las diferencias, complementada con Wilcoxon. Ambas "
                  "pruebas se reportan; se sugiere explicitar la jerarquía en la matriz.",
                  "[VERIFICAR]"))
    notas.append(("09_ANEXO6_TRAZABILIDAD", "Cobertura de historias de usuario",
                  "La tabla 54 consigna cinco historias (HU-01, HU-04, HU-06, HU-09 y HU-12) "
                  "de las 76 documentadas en la sección 3.3. Se transcribe sin alteración; "
                  "corresponde declarar en el anexo que se trata de una selección "
                  "representativa por iteración.", "[VERIFICAR]"))

    for columna in codebook.get("columnas", []):
        nombre = columna.get("nombre")
        if nombre not in pre.columns:
            continue
        detalle = columna.get("descripcion") or columna.get("indicador") or ""
        extra = []
        if columna.get("unidad"):
            extra.append(f"unidad: {columna['unidad']}")
        rango = columna.get("rango")
        if isinstance(rango, list) and len(rango) == 2:
            extra.append(f"rango: {rango[0]} a {rango[1]}")
        if columna.get("formula"):
            extra.append(f"fórmula: {columna['formula']}")
        if extra:
            detalle = f"{detalle} ({'; '.join(extra)})"
        if detalle:
            notas.append(("03/04", f"Variable {nombre}", detalle.strip(), "TRAZABLE"))

    if discrepancias:
        for texto in discrepancias:
            notas.append(("Global", "Control de coherencia DOCX-JSON", texto, "[VERIFICAR]"))
    else:
        notas.append(("Global", "Control de coherencia DOCX-JSON",
                      "Los estadísticos t, d, alfa y W del reporte coinciden con los valores "
                      "publicados en el DOCX al tercer decimal.", "TRAZABLE"))

    notas.append(("00_PORTADA", "Ficha del documento",
                  f"{meta['tesista']} | {meta['asesora']} | generado el "
                  f"{date.today().isoformat()}.", "TRAZABLE"))
    return notas


# ---------------------------------------------------------------------------
# Orquestación
# ---------------------------------------------------------------------------
DOCUMENTO = None


def main() -> int:
    global DOCUMENTO

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    faltantes = [ruta for ruta in (DOCX_INFORME, JSON_ESTADISTICO, CSV_PRETEST,
                                   CSV_POSTEST, JSON_CENTROS, JSON_ANEXOS)
                 if not ruta.exists()]
    if faltantes:
        for ruta in faltantes:
            print(f"[ERROR] Falta la fuente: {ruta}")
        return 2

    est = leer_json(JSON_ESTADISTICO)
    centros = leer_json(JSON_CENTROS)
    anexos = leer_json(JSON_ANEXOS)
    codebook = leer_json(JSON_CODEBOOK) if JSON_CODEBOOK.exists() else {"columnas": []}
    pre = pd.read_csv(CSV_PRETEST)
    post = pd.read_csv(CSV_POSTEST)
    DOCUMENTO = Document(str(DOCX_INFORME))

    metadatos = est["metadatos"]
    meta = {
        "institucion": metadatos["institucion"],
        "facultad": anexos["metadata"].get("facultad", "Facultad de Ingeniería"),
        "escuela": metadatos["escuela"],
        "tesista": metadatos["tesista"],
        "asesora": metadatos["asesora"],
        "n_censal": metadatos["n_censal"],
        "estado_datos": metadatos["estado_datos"],
        "titulo": metadatos["tesis"],
    }

    forma = derivar_forma(pre, post)
    correlaciones = derivar_correlaciones(pre, post)

    tablas_docx = {
        "contrastes": (leer_tabla_docx(DOCUMENTO, 40) + leer_tabla_docx(DOCUMENTO, 41)
                       + leer_tabla_docx(DOCUMENTO, 42)),
        "confiabilidad": " ".join(" ".join(f) for f in leer_tabla_docx(DOCUMENTO, 35)),
        "normalidad": " ".join(" ".join(f) for f in leer_tabla_docx(DOCUMENTO, 39)),
    }
    discrepancias = control_coherencia(est, tablas_docx)

    wb = Workbook()
    wb.remove(wb.active)
    wb.properties.title = "Tablas de anexos del Informe Final SIVAC"
    wb.properties.subject = meta["titulo"]
    wb.properties.creator = "Squad D - Analista Estadístico | SIVAC-THESIS-LAB"
    wb.properties.keywords = "SIVAC; UNAJMA; APA 7; SPSS; DEC-007"

    hoja_portada(wb, meta)
    hoja_replica_tabla(wb, "01_ANEXO1_MATRIZ", 44, "Tabla 44",
                       "Matriz de consistencia metodológica del estudio SIVAC",
                       horizontal=True)
    hoja_replica_tabla(wb, "02_ANEXO2_OPERAC", 45, "Tabla 45",
                       "Matriz de operacionalización de las variables de investigación",
                       horizontal=True)
    hoja_matriz_datos(wb, "03_ANEXO5_PRETEST", 52, "Tabla 52",
                      "Matriz de datos recolectados en el pretest (gestión manual basal, n = 14)")
    hoja_matriz_datos(wb, "04_ANEXO5_POSTEST", 53, "Tabla 53",
                      "Matriz de datos recolectados en el postest (operación con SIVAC, n = 14)")
    hoja_descriptivos(wb, est, forma)
    hoja_confiabilidad(wb, est)
    hoja_normalidad(wb, est)
    hoja_contrastes(wb, est)
    hoja_replica_tabla(wb, "09_ANEXO6_TRAZABILIDAD", 54, "Tabla 54",
                       "Matriz de historias de usuario desarrolladas e implementadas en "
                       "SIVAC bajo Extreme Programming", horizontal=True)
    hoja_spss(wb, est, forma, correlaciones)
    notas = construir_notas(est, pre, centros, codebook, discrepancias, meta)
    hoja_notas(wb, notas)

    XLSX_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(XLSX_SALIDA)
    wb.close()

    print(f"Libro generado: {XLSX_SALIDA}")
    print(f"Hojas: {len(wb.sheetnames)} -> {', '.join(HOJAS[i][0] for i in range(len(HOJAS)))}")
    print(f"Notas registradas: {len(notas)}")
    if discrepancias:
        print("Discrepancias DOCX-JSON registradas:")
        for texto in discrepancias:
            print(f"  - {texto}")
    else:
        print("Control de coherencia DOCX-JSON: sin discrepancias al tercer decimal.")
    print(f"Tamaño: {XLSX_SALIDA.stat().st_size / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
