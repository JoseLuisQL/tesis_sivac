# -*- coding: utf-8 -*-
"""Libro de captura del paquete v22: la digitación de las hojas de campo.

Las fichas impresas se llenan a mano y después se digitan. Este libro es el
paso intermedio: una hoja por instrumento, con las columnas del diccionario de
variables y una fila por cada registro que la campaña debe producir (168
réplicas, 1 120 asientos, 700 despachos, 224 reactivos). Las claves de
identificación vienen escritas —operador, centro, momento, tarea, número de
réplica o de asiento— para que el digitador solo transcriba lo que está en el
papel y ninguna fila se pierda ni se duplique; las columnas de medición quedan
vacías a propósito.

El libro no se llena solo ni sustituye a la ficha: si una fila prevista no
existe en el papel, se deja en blanco y se explica en la hoja de
observaciones de la sesión; el consolidado se calcula después desde estas
cuatro hojas, no desde valores tecleados a mano.

Uso
---
    python scripts/compiladores/libro_captura_v22.py
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = (RAIZ / "salidas" / "instrumentos" / "INSTRUMENTOS_DEFINITIVOS_v22"
           / "07_CAPTURA" / "LIBRO_DE_CAPTURA_v22.xlsx")

sys.path.insert(0, str(RAIZ / "scripts" / "estadistica"))
import generar_datos_sinteticos as G  # noqa: E402

FUENTE = "Calibri"
BORDE = Border(*[Side(style="thin", color="B0B0B0")] * 4)
CABECERA = PatternFill("solid", fgColor="1F3A5F")
BANDA = PatternFill("solid", fgColor="F2F5F8")
CLAVE = PatternFill("solid", fgColor="EDEDED")
MEDIDA = PatternFill("solid", fgColor="FFFDF0")

ANCHO_MAX = 46


def _hoja(libro: Workbook, titulo: str, columnas, filas, claves: int,
          nota: str, validaciones=(), congelar: str = "A3"):
    hoja = libro.create_sheet(titulo)
    hoja["A1"] = nota
    hoja["A1"].font = Font(name=FUENTE, size=10, italic=True, color="444444")
    hoja["A1"].alignment = Alignment(wrap_text=False, vertical="center")
    hoja.row_dimensions[1].height = 30
    hoja.merge_cells(start_row=1, start_column=1, end_row=1,
                     end_column=len(columnas))

    for j, (nombre, ancho, tipo) in enumerate(columnas, 1):
        celda = hoja.cell(row=2, column=j, value=nombre)
        celda.font = Font(name=FUENTE, size=9, bold=True, color="FFFFFF")
        celda.fill = CABECERA
        celda.alignment = Alignment(horizontal="center", vertical="center",
                                    wrap_text=True)
        celda.border = BORDE
        hoja.column_dimensions[get_column_letter(j)].width = ancho

    hoja.row_dimensions[2].height = 34

    for i, fila in enumerate(filas, 3):
        for j, valor in enumerate(fila, 1):
            celda = hoja.cell(row=i, column=j, value=valor)
            celda.font = Font(name=FUENTE, size=10)
            celda.border = BORDE
            celda.fill = CLAVE if j <= claves else MEDIDA
            celda.alignment = Alignment(
                horizontal="left" if j <= claves else "center",
                vertical="center")

    primera, ultima = 3, 2 + len(filas)
    indices = {nombre: j for j, (nombre, _a, _t) in enumerate(columnas, 1)}
    for nombre_columna, opciones in validaciones:
        columna = indices[nombre_columna]
        val = DataValidation(type="list", formula1='"' + ",".join(opciones)
                             + '"', allow_blank=True, showDropDown=False)
        val.error = "Valor fuera de la lista de la ficha."
        val.errorTitle = "Valor no admitido"
        hoja.add_data_validation(val)
        letra = get_column_letter(columna)
        val.add(f"{letra}{primera}:{letra}{ultima}")

    hoja.freeze_panes = congelar
    hoja.auto_filter.ref = (f"A2:{get_column_letter(len(columnas))}{ultima}")
    hoja.sheet_view.zoomScale = 100
    return hoja


def hoja_leeme(libro: Workbook, conteos) -> None:
    hoja = libro.create_sheet("00_LEEME", 0)
    hoja.column_dimensions["A"].width = 34
    hoja.column_dimensions["B"].width = 74

    hoja["A1"] = "Libro de captura del paquete de instrumentos v22"
    hoja["A1"].font = Font(name=FUENTE, size=15, bold=True, color="1F3A5F")

    filas = [
        ("Qué es", "El puente entre la ficha de papel y el consolidado. Una "
                   "hoja por instrumento; una fila por registro."),
        ("Qué viene escrito", "Las claves: operador, centro, momento, tarea, "
                              "réplica o número de asiento, y la columna de "
                              "hoja en la ficha documental. No se cambian."),
        ("Qué se digita", "Solo lo que está en el papel, en las columnas con "
                          "fondo crema. Se transcribe tal como se leyó; las "
                          "cifras no se recalculan al digitar."),
        ("Cuándo se digita", "El mismo día de la sesión, con las hojas a la "
                             "vista. Una sesión son seis hojas de instrumento "
                             "y 79 filas del libro."),
        ("Filas previstas", " | ".join(f"{n}: {c}" for n, c in conteos)),
        ("Si falta una fila", "Se deja en blanco, nunca se borra ni se "
                              "duplica, y se explica en la hoja de "
                              "observaciones de la sesión con la referencia "
                              "«02-A, asiento 34»."),
        ("Si una cifra no cuadra", "Se digita lo que dice el papel y se anota "
                                   "la discrepancia en observaciones. La hoja "
                                   "no se corrige en el libro."),
        ("Después", "El consolidado por operador y momento se calcula desde "
                    "estas cuatro hojas: promedios de las réplicas válidas, "
                    "RSD y CPE sobre los registros revisados, AP y UP por suma "
                    "de reactivos."),
        ("Advertencia", "El libro está vacío de mediciones a propósito. Las "
                        "claves reproducen el diseño censal (14 operadores por "
                        "2 momentos) y no contienen ningún valor observado."),
    ]
    fila = 3
    for etiqueta, texto in filas:
        hoja.cell(row=fila, column=1, value=etiqueta).font = Font(
            name=FUENTE, size=10, bold=True)
        celda = hoja.cell(row=fila, column=2, value=texto)
        celda.font = Font(name=FUENTE, size=10)
        celda.alignment = Alignment(wrap_text=True, vertical="top")
        hoja.row_dimensions[fila].height = 15 * (1 + len(texto) // 95)
        fila += 1

    fila += 1
    hoja.cell(row=fila, column=1, value="Hoja").font = Font(
        name=FUENTE, size=10, bold=True, color="FFFFFF")
    hoja.cell(row=fila, column=1).fill = CABECERA
    hoja.cell(row=fila, column=2, value="Registros").font = Font(
        name=FUENTE, size=10, bold=True, color="FFFFFF")
    hoja.cell(row=fila, column=2).fill = CABECERA
    for nombre, conteo in conteos:
        fila += 1
        hoja.cell(row=fila, column=1, value=nombre).font = Font(
            name=FUENTE, size=10)
        hoja.cell(row=fila, column=2, value=conteo).font = Font(
            name=FUENTE, size=10)


def construir() -> Path:
    libro = Workbook()
    libro.remove(libro.active)

    def f( fecha):
        return fecha.strftime("%d/%m/%Y")

    replicas = []
    asientos = []
    despachos = []
    reactivos = []
    for op, centro, _cod, obs, pre, post in G.PADRON:
        for momento, fecha in (("Pretest", pre), ("Postest", post)):
            for indicador, tareas in (("T_reg", G.TAREAS_REG),
                                      ("T_vale", G.TAREAS_VALE)):
                for replica, tarea, escenario in tareas:
                    replicas.append([op, centro, momento, f(fecha), obs,
                                     indicador, replica, tarea, escenario])
            for n in range(1, 41):
                asientos.append([op, centro, momento, f(fecha), obs,
                                 1 if n <= 20 else 2, n])
            for n in range(1, 26):
                despachos.append([op, centro, momento, f(fecha), n])
            for codigo in ("AP-01", "AP-02", "AP-03", "AP-04",
                           "UP-01", "UP-02", "UP-03", "UP-04"):
                reactivos.append([op, centro, momento, f(fecha), obs,
                                  codigo, codigo[:2]])

    assert len(replicas) == 168, len(replicas)
    assert len(asientos) == 1120, len(asientos)
    assert len(despachos) == 700, len(despachos)
    assert len(reactivos) == 224, len(reactivos)

    conteos = [("01_replicas", len(replicas)),
               ("02_asientos", len(asientos)),
               ("02_despachos", len(despachos)),
               ("03_reactivos", len(reactivos))]

    hoja_leeme(libro, conteos)

    _hoja(libro, "01_replicas", [
        ("sujeto_id", 11, "texto"), ("centro_acopio", 26, "texto"),
        ("momento", 11, "texto"), ("fecha_sesion", 13, "texto"),
        ("observador", 12, "texto"), ("indicador", 10, "texto"),
        ("replica", 9, "texto"), ("tarea", 6, "texto"),
        ("escenario", 36, "texto"),
        ("documento", 20, "texto"), ("lote", 16, "texto"),
        ("hora_inicio", 12, "texto"), ("hora_corte", 12, "texto"),
        ("duracion_s", 11, "entero"), ("duracion_min", 13, "decimal"),
        ("pausa_s", 9, "entero"), ("motivo_pausa", 13, "texto"),
        ("valida", 9, "texto"),
    ], [r + [""] * 9 for r in replicas], 9,
        "01_replicas · una fila por réplica cronometrada (ficha 01). Hora de "
        "inicio y de corte como HH:MM:SS; duracion_s = corte − inicio en "
        "segundos, descontada la pausa; duracion_min = duracion_s ÷ 60 con "
        "cuatro decimales.",
        validaciones=(("indicador", ["T_reg", "T_vale"]),
                      ("valida", ["Sí", "No"]),
                      ("motivo_pausa", ["P1", "P2", "P3", "P4"])),
        congelar="D3")

    _hoja(libro, "02_asientos", [
        ("sujeto_id", 11, "texto"), ("centro_acopio", 26, "texto"),
        ("momento", 11, "texto"), ("fecha_sesion", 13, "texto"),
        ("auditor", 10, "texto"), ("hoja", 7, "texto"),
        ("n", 7, "entero"), ("fecha", 12, "texto"), ("tipo", 8, "texto"),
        ("documento", 22, "texto"), ("biologico", 11, "texto"),
        ("lote", 16, "texto"), ("cantidad", 10, "entero"),
        ("c1", 6, "texto"), ("c2", 6, "texto"), ("c3", 6, "texto"),
        ("c4", 6, "texto"), ("c5", 6, "texto"), ("c6", 6, "texto"),
        ("c7", 6, "texto"), ("c8", 6, "texto"),
        ("conforme", 10, "texto"), ("motivo", 14, "texto"),
        ("observacion", ANCHO_MAX, "texto"),
    ], [a + [""] * 17 for a in asientos], 7,
        "02_asientos · una fila por asiento auditado (ficha 02, bloque A). "
        "Criterios c1 a c8 en S o N; conforme en Sí o No; motivo solo cuando "
        "el asiento no es conforme (M1 a M8, unidos con +).",
        validaciones=(("tipo", ["ING", "SAL", "TRA", "DEV", "AJU"]),
                      ("c1", ["S", "N"]), ("c2", ["S", "N"]),
                      ("c3", ["S", "N"]), ("c4", ["S", "N"]),
                      ("c5", ["S", "N"]), ("c6", ["S", "N"]),
                      ("c7", ["S", "N"]), ("c8", ["S", "N"]),
                      ("conforme", ["Sí", "No"])),
        congelar="H3")

    _hoja(libro, "02_despachos", [
        ("sujeto_id", 11, "texto"), ("centro_acopio", 26, "texto"),
        ("momento", 11, "texto"), ("fecha_sesion", 13, "texto"),
        ("n", 7, "entero"),
        ("fecha", 12, "texto"), ("biologico", 11, "texto"),
        ("programado", 12, "entero"), ("entregado", 11, "entero"),
        ("diferencia", 11, "entero"), ("documento", 24, "texto"),
        ("conforme", 10, "texto"), ("observacion", ANCHO_MAX, "texto"),
    ], [d + [""] * 8 for d in despachos], 5,
        "02_despachos · una fila por despacho conciliado (ficha 02, bloque B). "
        "Diferencia = entregado − programado, con signo; conforme solo si la "
        "diferencia es cero y el documento coincide.",
        validaciones=(("conforme", ["Sí", "No"]),),
        congelar="F3")

    _hoja(libro, "03_reactivos", [
        ("sujeto_id", 11, "texto"), ("centro_acopio", 26, "texto"),
        ("momento", 11, "texto"), ("fecha_sesion", 13, "texto"),
        ("encuestador", 13, "texto"), ("reactivo", 10, "texto"),
        ("dimension", 11, "texto"), ("valor", 8, "entero"),
        ("score_ap", 10, "entero"), ("score_up", 10, "entero"),
        ("score_total", 12, "entero"), ("nivel", 10, "texto"),
        ("observacion", ANCHO_MAX, "texto"),
    ], [r + [""] * 6 for r in reactivos], 7,
        "03_reactivos · una fila por reactivo respondido (ficha 03). Valor de "
        "1 a 5, una sola marca por reactivo. AP, UP, TAM y nivel se calculan "
        "al cierre de la sesión, no se digitan de la hoja.",
        validaciones=(("reactivo", ["AP-01", "AP-02", "AP-03", "AP-04",
                                    "UP-01", "UP-02", "UP-03", "UP-04"]),
                      ("valor", ["1", "2", "3", "4", "5"]),
                      ("nivel", ["Bajo", "Medio", "Alto"])),
        congelar="G3")

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    libro.properties.creator = "SIVAC-THESIS-LAB"
    libro.properties.title = "Libro de captura del paquete de instrumentos v22"
    libro.properties.created = dt.datetime(2026, 1, 1)
    libro.properties.modified = dt.datetime(2026, 1, 1)
    libro.save(DESTINO)
    return DESTINO


def main() -> None:
    destino = construir()
    print(f"Libro de captura escrito: {destino}")


if __name__ == "__main__":
    main()
