# -*- coding: utf-8 -*-
"""Exporta el libro de campo en Excel (PRETEST / POSTTEST / DICCIONARIO / CONTROL).

El libro se construye **desde los CSV canónicos** de `datos/recolectados/`, no
desde valores escritos a mano: si el CSV cambia, el libro cambia. Las hojas de
datos reproducen exactamente las filas y el orden de columnas del CSV, de modo
que cualquier lector pueda contrastar libro y archivo plano fila por fila.

Uso:
    python scripts/estadistica/exportar_libro_campo.py [ruta_destino.xlsx]

Sin argumento escribe `datos/recolectados/datos_recolectados_pre_post.xlsx`.
"""
from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

RAIZ = Path(__file__).resolve().parents[2]
RECO = RAIZ / "datos" / "recolectados"

DICCIONARIO = [
    ("sujeto_id", "Texto", "TRAB-01 … TRAB-14", "Control censal",
     "Identificador anónimo del operador"),
    ("centro_acopio", "Texto", "13 centros de acopio", "Geográfico",
     "Centro de acopio o establecimiento de salud"),
    ("t_reg", "Decimal", "minutos", "D1. Oportunidad",
     "I1.1 Tiempo de registro de movimientos"),
    ("t_vale", "Decimal", "minutos", "D1. Oportunidad",
     "I1.2 Tiempo de emisión del vale"),
    ("rsd", "Decimal", "0 – 100 %", "D2. Consistencia documental",
     "I2.1 Registros sin discrepancias"),
    ("cpe", "Decimal", "0 – 100 %", "D2. Consistencia documental",
     "I2.2 Concordancia programada vs. entregada"),
    ("ap_01 … ap_04", "Entero", "1 – 5 (Likert)", "D3. Satisfacción",
     "Reactivos de aceptación del proceso (TAM)"),
    ("up_01 … up_04", "Entero", "1 – 5 (Likert)", "D3. Satisfacción",
     "Reactivos de utilidad percibida (TAM)"),
    ("score_ap", "Entero", "4 – 20 puntos", "D3. Satisfacción",
     "Suma de ap_01 … ap_04"),
    ("score_up", "Entero", "4 – 20 puntos", "D3. Satisfacción",
     "Suma de up_01 … up_04"),
    ("score_tam_total", "Entero", "8 – 40 puntos", "D3. Satisfacción",
     "score_ap + score_up"),
    ("nivel_satisfaccion", "Texto", "Bajo / Medio / Alto", "Baremo",
     "Bajo 8–18; Medio 19–29; Alto 30–40"),
]

NEGRITA = Font(bold=True, color="FFFFFF")
CABECERA_FILL = PatternFill("solid", fgColor="1F3864")
TITULO = Font(bold=True, size=12)
BORDE = Border(bottom=Side(style="thin", color="BFBFBF"))
CENTRO = Alignment(horizontal="center", vertical="center", wrap_text=True)


def leer(nombre: str) -> tuple[list[str], list[list[str]]]:
    with (RECO / nombre).open(encoding="utf-8", newline="") as fh:
        filas = list(csv.reader(fh))
    return filas[0], filas[1:]


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def hoja_datos(wb: Workbook, nombre: str, archivo: str) -> None:
    cabecera, filas = leer(archivo)
    ws = wb.create_sheet(nombre)
    ws.append(cabecera)
    for fila in filas:
        # Los números se escriben como números: el libro debe poder recalcularse.
        valores = []
        for valor in fila:
            try:
                if valor != "" and "." in valor:
                    valores.append(float(valor))
                elif valor.isdigit():
                    valores.append(int(valor))
                else:
                    valores.append(valor)
            except ValueError:
                valores.append(valor)
        ws.append(valores)
    for celda in ws[1]:
        celda.font = NEGRITA
        celda.fill = CABECERA_FILL
        celda.alignment = CENTRO
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = ws.dimensions
    for idx, titulo in enumerate(cabecera, start=1):
        ancho = max(len(titulo) + 2, 12)
        ws.column_dimensions[get_column_letter(idx)].width = ancho
    ws.row_dimensions[1].height = 32


def hoja_diccionario(wb: Workbook) -> None:
    ws = wb.create_sheet("DICCIONARIO")
    ws.append(["Columna", "Tipo", "Rango / unidad", "Dimensión (DEC-007)",
               "Indicador"])
    for fila in DICCIONARIO:
        ws.append(list(fila))
    for celda in ws[1]:
        celda.font = NEGRITA
        celda.fill = CABECERA_FILL
        celda.alignment = CENTRO
    for idx, ancho in enumerate((20, 10, 26, 30, 46), start=1):
        ws.column_dimensions[get_column_letter(idx)].width = ancho
    ws.freeze_panes = "A2"


def hoja_control(wb: Workbook) -> None:
    ws = wb.create_sheet("CONTROL")
    # Sin marca de tiempo: el libro debe ser idéntico byte a byte entre
    # ejecuciones para poder compararlo en el control de versiones.
    ws.append(["Archivo", "Filas", "Bytes", "SHA-256"])
    for celda in ws[1]:
        celda.font = NEGRITA
        celda.fill = CABECERA_FILL
    for nombre in ("pretest_campo.csv", "posttest_campo.csv"):
        ruta = RECO / nombre
        _, filas = leer(nombre)
        ws.append([nombre, len(filas), ruta.stat().st_size, sha256(ruta)])
    for celda in ws["D"][1:]:
        celda.border = BORDE
    for idx, ancho in enumerate((28, 8, 12, 70), start=1):
        ws.column_dimensions[get_column_letter(idx)].width = ancho
    ws.append([])
    ws.append(["Estado", "DATOS DE PRUEBA — REEMPLAZAR (DEC-007)"])
    ws["B" + str(ws.max_row)].font = Font(bold=True, color="C00000")


def _fijar_fechas(destino: Path) -> None:
    """Reescribe el zip interno con fecha fija.

    openpyxl sella la hora de guardado en cada entrada del zip, de modo que dos
    ejecuciones idénticas producían archivos con distinto SHA-256 y el libro
    aparecía como modificado en el control de versiones sin haber cambiado
    ningún dato. Con la fecha fija, el archivo es reproducible byte a byte.
    """
    import re
    import zipfile

    fijo = b"2026-01-01T00:00:00Z"
    with zipfile.ZipFile(destino) as original:
        entradas = [(info.filename, original.read(info.filename))
                    for info in original.infolist()]
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as salida:
        for nombre, datos in entradas:
            if nombre == "docProps/core.xml":
                # openpyxl reescribe `modified` con la hora de guardado.
                datos = re.sub(
                    rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                    rb"\1" + fijo + rb"\2", datos)
            info = zipfile.ZipInfo(nombre, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            salida.writestr(info, datos)


def exportar(destino: Path) -> Path:
    wb = Workbook()
    wb.remove(wb.active)
    hoja_datos(wb, "PRETEST", "pretest_campo.csv")
    hoja_datos(wb, "POSTTEST", "posttest_campo.csv")
    hoja_diccionario(wb)
    hoja_control(wb)
    wb.properties.title = "Datos recolectados pretest-postest SIVAC"
    wb.properties.creator = "SIVAC-THESIS-LAB"
    # Metadatos con fecha fija: openpyxl sella la hora en docProps/core.xml y
    # el archivo cambiaría en cada ejecución sin que cambien los datos.
    from datetime import datetime as _dt
    wb.properties.created = _dt(2026, 1, 1)
    wb.properties.modified = _dt(2026, 1, 1)
    destino.parent.mkdir(parents=True, exist_ok=True)
    wb.save(destino)
    _fijar_fechas(destino)
    return destino


def main(argv: list[str]) -> int:
    destino = (Path(argv[1]) if len(argv) > 1
               else RECO / "datos_recolectados_pre_post.xlsx")
    print(f"Libro de campo escrito: {exportar(destino)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
