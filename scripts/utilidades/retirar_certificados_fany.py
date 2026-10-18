#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - RETIRO DE LOS CERTIFICADOS FANY 2024 DEFECTUOSOS
================================================================================
Reubica, sin borrar, los seis certificados ANEXO_2_VALIDACION_FANY_{VD,VI}_
EXPERTO_{1,2,3}_VACIO.docx desde la raiz de salidas/documentos/anexos_fany/
hacia salidas/documentos/anexos_fany/_archivo_obsoleto/.

El retiro obedece al dictamen del guardian-consistencia del 2026-10-18: ambos
conjuntos de items son defectuosos y no deben imprimirse ni someterse a ningun
juez. La estructura definitiva aguarda decision del tesista; este script no
genera contenido nuevo.

Idempotente: si un archivo ya fue reubicado, no falla. Si existe una colision de
nombre en el destino, desambigua con sufijo _DUPLICADO_n en lugar de sobrescribir.

Uso:
    python scripts/utilidades/retirar_certificados_fany.py
    python scripts/utilidades/retirar_certificados_fany.py --simular
================================================================================
"""

import argparse
import shutil
import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
DIR_ORIGEN = RAIZ_PROYECTO / "salidas" / "documentos" / "anexos_fany"
DIR_DESTINO = DIR_ORIGEN / "_archivo_obsoleto"

VARIABLES = ("VD", "VI")
EXPERTOS = (1, 2, 3)


def nombre_certificado(variable, experto):
    return "ANEXO_2_VALIDACION_FANY_%s_EXPERTO_%d_VACIO.docx" % (variable, experto)


def destino_libre(destino):
    """Devuelve una ruta de destino que no sobrescriba un archivo existente."""
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
        description="Reubica los certificados Fany 2024 defectuosos al archivo obsoleto."
    )
    parser.add_argument(
        "--simular",
        action="store_true",
        help="Muestra las operaciones sin mover archivos.",
    )
    args = parser.parse_args()

    if not DIR_ORIGEN.is_dir():
        print("ERROR: no existe el directorio %s" % DIR_ORIGEN)
        return 1

    if not args.simular:
        DIR_DESTINO.mkdir(parents=True, exist_ok=True)

    movidos = 0
    ya_reubicados = 0
    ausentes = 0

    for variable in VARIABLES:
        for experto in EXPERTOS:
            nombre = nombre_certificado(variable, experto)
            origen = DIR_ORIGEN / nombre
            if origen.is_file():
                destino = destino_libre(DIR_DESTINO / nombre)
                if args.simular:
                    print("SIMULA: %s -> %s" % (origen.name, destino.name))
                else:
                    shutil.move(str(origen), str(destino))
                    print("MOVIDO: %s -> %s" % (origen.name, destino.name))
                movidos += 1
            elif (DIR_DESTINO / nombre).is_file():
                print("YA REUBICADO: %s" % nombre)
                ya_reubicados += 1
            else:
                print("AUSENTE: %s" % nombre)
                ausentes += 1

    print("")
    print("Resumen: movidos=%d, ya_reubicados=%d, ausentes=%d"
          % (movidos, ya_reubicados, ausentes))

    restantes = [
        p.name for p in DIR_ORIGEN.glob("ANEXO_2_*_VACIO.docx") if p.is_file()
    ]
    if restantes:
        print("ADVERTENCIA: persisten certificados en la raiz: %s" % ", ".join(restantes))
        return 1

    print("Raiz de anexos_fany sin certificados ANEXO_2_*_VACIO.docx.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
