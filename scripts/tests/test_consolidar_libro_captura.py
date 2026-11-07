# -*- coding: utf-8 -*-
"""Prueba de ida y vuelta del libro de captura v22.

Toma el libro vacío del paquete, lo llena con el conjunto sintético —una fila
por registro, tal como lo haría un digitador—, lo consolida y compara el
resultado con los CSV de campo publicados. Si la cadena ficha → libro →
consolidado está bien construida, ambos archivos deben ser idénticos byte a
byte.

Se puede ejecutar con pytest o directamente:

    python scripts/tests/test_consolidar_libro_captura.py
"""
from __future__ import annotations

import csv
import shutil
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts" / "estadistica"))

import consolidar_libro_captura as C  # noqa: E402

SINT = RAIZ / "datos" / "prueba_sintetica"
RECO = RAIZ / "datos" / "recolectados"

# hoja del libro -> (archivo sintético, columnas renombradas, columnas a llenar)
MAPA = {
    "01_replicas": ("instrumento01_replicas.csv", {"fecha": "fecha_sesion"},
                    ["documento", "lote", "hora_inicio", "hora_corte",
                     "duracion_s", "duracion_min", "pausa_s", "motivo_pausa",
                     "valida"],
                    ["sujeto_id", "momento", "indicador", "replica"]),
    "02_asientos": ("instrumento02_asientos.csv", {},
                    ["fecha", "tipo", "documento", "biologico", "lote",
                     "cantidad", "c1", "c2", "c3", "c4", "c5", "c6", "c7",
                     "c8", "conforme", "motivo", "observacion"],
                    ["sujeto_id", "momento", "n"]),
    "02_despachos": ("instrumento02_despachos.csv", {},
                     ["fecha", "biologico", "programado", "entregado",
                      "diferencia", "documento", "conforme", "observacion"],
                     ["sujeto_id", "momento", "n"]),
    "03_reactivos": ("instrumento03_reactivos.csv",
                     {"fecha": "fecha_sesion"}, ["valor", "observacion"],
                     ["sujeto_id", "momento", "reactivo"]),
}

NUMERICAS = {"duracion_s", "duracion_min", "pausa_s", "cantidad", "programado",
             "entregado", "diferencia", "valor"}
VACIAS = {"", None}


def _csv(nombre: str) -> list[dict]:
    with (SINT / nombre).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _numero(texto: str):
    try:
        return int(texto) if str(texto).lstrip("-").isdigit() else float(texto)
    except ValueError:
        return texto


def llenar_libro(destino: Path) -> Path:
    """Copia el libro del paquete y digita el conjunto sintético en él."""
    from openpyxl import load_workbook

    shutil.copy(C.LIBRO, destino)
    libro = load_workbook(destino)

    for hoja, (archivo, renombres, columnas, clave) in MAPA.items():
        registros = _csv(archivo)
        sheet = libro[hoja]
        cabecera = [c.value for c in sheet[2]]
        indice = {}
        for fila in sheet.iter_rows(min_row=3, max_col=len(cabecera)):
            celdas = {cabecera[j]: fila[j] for j in range(len(cabecera))}
            if celdas["sujeto_id"].value is None:
                continue
            llave = tuple(str(celdas[c].value) for c in clave)
            indice[llave] = celdas
        for registro in registros:
            celdas = indice[tuple(registro[c] for c in clave)]
            for columna in columnas:
                valor = registro.get(renombres.get(columna, columna), "")
                if valor in VACIAS:
                    continue
                celdas[columna].value = (_numero(valor) if columna in NUMERICAS
                                         else valor)

    libro.save(destino)
    return destino


def test_ida_y_vuelta():
    with tempfile.TemporaryDirectory() as carpeta:
        libro = llenar_libro(Path(carpeta) / "LIBRO_LLENO.xlsx")
        resultado = C.consolidar(libro)
        assert not any(resultado["pendientes"].values()), "quedaron sesiones incompletas"
        assert not resultado["avisos"], resultado["avisos"]

        for momento, nombre in (("Pretest", "pretest_campo"),
                                ("Postest", "posttest_campo")):
            filas = [f for f in resultado["filas"] if f["_momento"] == momento]
            generado = Path(carpeta) / f"{nombre}.csv"
            with generado.open("w", encoding="utf-8", newline="") as f:
                import csv as _csv_mod
                escritor = _csv_mod.DictWriter(f, fieldnames=C.COLUMNAS,
                                               lineterminator="\n")
                escritor.writeheader()
                for fila in filas:
                    escritor.writerow({c: fila[c] for c in C.COLUMNAS})
            assert generado.read_bytes() == (RECO / f"{nombre}.csv").read_bytes(), (
                f"{nombre} no reproduce el CSV publicado")


if __name__ == "__main__":
    test_ida_y_vuelta()
    print("OK: libro lleno -> consolidado idéntico a los CSV publicados")
