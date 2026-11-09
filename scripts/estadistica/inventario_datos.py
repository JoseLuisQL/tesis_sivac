# -*- coding: utf-8 -*-
"""Inventario verificable de la capa `datos/`.

Recorre `datos/` y deja en `datos/INVENTARIO.json` la ficha de cada archivo
(bytes, SHA-256 y, para los CSV, filas y columnas). El inventario es la
referencia que usa `verificar_conjunto_datos.py` para comprobar que ningún
archivo queda fuera del mapa documentado en `datos/README.md` y que las
dimensiones declaradas corresponden a los archivos reales.

No modifica ningún dato: solo lee y escribe el inventario.

Uso:
    python scripts/estadistica/inventario_datos.py [--verificar]

`--verificar` compara sin escribir y devuelve código 1 si el inventario está
desactualizado.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / "datos"
INVENTARIO = DATOS / "INVENTARIO.json"

# Archivos que documentan la capa y no se inventarían como datos.
EXCLUIDOS = {"README.md", "INVENTARIO.json"}

CAPAS = {
    "plantillas": "Formatos vacíos para la recolección en campo",
    "processed": "Matrices tabuladas limpias (destino tras el control de calidad)",
    "prueba_sintetica": "Conjunto de prueba reproducible (semilla x)",
    "raw": "Datos de campo brutos e inmutables",
    "recolectados": "Conjunto consolidado que consume el pipeline estadístico",
    "schemas": "Catálogos y diccionario de variables",
}


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def dimensiones(ruta: Path) -> dict | None:
    if ruta.suffix.lower() != ".csv":
        return None
    with ruta.open(encoding="utf-8", newline="") as f:
        filas = list(csv.reader(f))
    if not filas:
        return {"filas": 0, "columnas": 0}
    return {"filas": len(filas) - 1, "columnas": len(filas[0])}


def ficha(ruta: Path) -> dict:
    datos = {
        "bytes": ruta.stat().st_size,
        "sha256": sha256(ruta),
    }
    dims = dimensiones(ruta)
    if dims is not None:
        datos.update(dims)
    return datos


def construir() -> dict:
    capas: dict[str, dict] = {}
    for capa in sorted(CAPAS):
        carpeta = DATOS / capa
        if not carpeta.is_dir():
            continue
        archivos = {}
        for ruta in sorted(carpeta.iterdir()):
            if not ruta.is_file() or ruta.name in EXCLUIDOS:
                continue
            if ruta.name.startswith(".") or ruta.suffix == ".pyc":
                continue
            archivos[ruta.name] = ficha(ruta)
        capas[capa] = {"descripcion": CAPAS[capa], "archivos": archivos}

    sueltos = sorted(
        ruta.name for ruta in DATOS.iterdir()
        if ruta.is_file() and ruta.name not in EXCLUIDOS
        and not ruta.name.startswith(".")
    )
    return {
        "generado_por": "scripts/estadistica/inventario_datos.py",
        "capa": "datos/",
        "regla": "sin MANIFEST.json firmado en datos/raw/ el pipeline "
                 "inferencial permanece bloqueado (Regla Canónica 01)",
        "capas": capas,
        "archivos_sueltos_en_la_raiz": sueltos,
        "totales": {
            "capas": len(capas),
            "archivos": sum(len(c["archivos"]) for c in capas.values()),
            "csv": sum(1 for c in capas.values() for a in c["archivos"].values()
                       if "filas" in a),
        },
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--verificar", action="store_true",
                   help="no escribe: comprueba que el inventario esté al día")
    args = p.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    actual = construir()
    texto = json.dumps(actual, ensure_ascii=False, indent=2) + "\n"

    if args.verificar:
        if not INVENTARIO.exists():
            print("[DESACTUALIZADO] falta datos/INVENTARIO.json")
            return 1
        if INVENTARIO.read_text(encoding="utf-8") != texto:
            print("[DESACTUALIZADO] datos/INVENTARIO.json no coincide con los archivos")
            return 1
        print(f"[OK] Inventario al día: {actual['totales']['archivos']} archivos "
              f"en {actual['totales']['capas']} capas")
        return 0

    INVENTARIO.write_text(texto, encoding="utf-8")
    for capa, contenido in actual["capas"].items():
        print(f"{capa}/ ({len(contenido['archivos'])} archivos)")
        for nombre, meta in contenido["archivos"].items():
            dims = (f"  {meta['filas']} × {meta['columnas']}"
                    if "filas" in meta else "")
            print(f"  {nombre}{dims}")
    print(f"\nInventario escrito: {INVENTARIO.relative_to(RAIZ)} "
          f"({actual['totales']['archivos']} archivos)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
