#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - CUARENTENA DE LOS GENERADORES APOCRIFOS
================================================================================
Reubica, sin borrar, los tres generadores retirados de la ruta oficial hacia
salidas/archivo/_generadores_apocrifos_no_usar/:

  * scripts/compiladores/generar_expedientes_e_instrumentos.py
  * scripts/estadistica/generar_matriz_ivc_excel.py
  * scripts/compiladores/generar_formatos_validacion.py

Motivo: los dos primeros emitian coeficientes prefabricados para 32 items
(V = 0.98 y 0.97, IVC = 1.00, "APROBADO"), prohibidos por DEC-014; el tercero
reproducia el modelo Condor Tinoco de cinco criterios y escala de 1 a 4,
superado por DEC-015.

Idempotente: si un archivo ya fue reubicado, no falla. Ante colision de nombre
en el destino desambigua con sufijo _DUPLICADO_n en lugar de sobrescribir.

Este script solo mueve archivos; no genera contenido ni calcula coeficientes.

Uso:
    python scripts/utilidades/cuarentenar_generadores_apocrifos.py
    python scripts/utilidades/cuarentenar_generadores_apocrifos.py --simular
================================================================================
"""

import argparse
import shutil
import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
DIR_DESTINO = RAIZ_PROYECTO / "salidas" / "archivo" / "_generadores_apocrifos_no_usar"

RETIRADOS = (
    RAIZ_PROYECTO / "scripts" / "compiladores" / "generar_expedientes_e_instrumentos.py",
    RAIZ_PROYECTO / "scripts" / "estadistica" / "generar_matriz_ivc_excel.py",
    RAIZ_PROYECTO / "scripts" / "compiladores" / "generar_formatos_validacion.py",
)


def destino_libre(destino):
    """Devuelve una ruta que no sobrescriba un archivo existente."""
    if not destino.exists():
        return destino
    contador = 1
    while True:
        candidato = destino.with_name(
            "%s_DUPLICADO_%d%s" % (destino.stem, contador, destino.suffix)
        )
        if not candidato.exists():
            return candidato
        contador += 1


def main():
    parser = argparse.ArgumentParser(
        description="Reubica los generadores apocrifos al archivo de cuarentena."
    )
    parser.add_argument(
        "--simular",
        action="store_true",
        help="Muestra las operaciones sin mover archivos.",
    )
    args = parser.parse_args()

    if not args.simular:
        DIR_DESTINO.mkdir(parents=True, exist_ok=True)

    movidos = 0
    ya_reubicados = 0
    ausentes = 0

    for origen in RETIRADOS:
        destino = destino_libre(DIR_DESTINO / origen.name)
        if origen.is_file():
            if args.simular:
                print("SIMULA: %s -> %s" % (origen.name, destino.name))
            else:
                shutil.move(str(origen), str(destino))
                print("MOVIDO: %s -> %s" % (origen.name, destino.name))
            movidos += 1
        elif (DIR_DESTINO / origen.name).is_file() or destino.exists():
            print("YA REUBICADO: %s" % origen.name)
            ya_reubicados += 1
        else:
            print("AUSENTE: %s" % origen.name)
            ausentes += 1

    print("")
    print("Resumen: movidos=%d, ya_reubicados=%d, ausentes=%d"
          % (movidos, ya_reubicados, ausentes))

    restantes = [p.name for p in RETIRADOS if p.is_file()]
    if restantes:
        print("ADVERTENCIA: persisten generadores en la ruta oficial: %s"
              % ", ".join(restantes))
        return 1

    print("Ruta oficial sin generadores apocrifos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
