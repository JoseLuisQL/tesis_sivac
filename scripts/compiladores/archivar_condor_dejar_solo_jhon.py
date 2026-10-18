#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHIVADO Y NEUTRALIZADO: 2026-10-18

Este script quedo sin efecto el 2026-10-18.

El modelo Jhon 2026 fue sustituido como formato de validacion por el modelo
Fany 2024 mediante DEC-015. Los tres espejos
ANEXO_6_VALIDACION_EXPERTO_{1,2,3}_JHON_ESPEJO_VACIO.docx ya fueron archivados
el 2026-10-18 en salidas/documentos/anexos_jhon/_archivo_obsoleto/, junto con
la nota LEEME_CERTIFICADOS_JHON_RETIRADOS.md, que documenta el retiro.

El expediente oficial vigente es el certificado unico del Instrumento N.° 03,
Modalidad A, en salidas/documentos/anexos_fany/, conforme a DEC-015, DEC-019
y DEC-020. Lo emite scripts/compiladores/generar_anexo2_validacion_fany.py con
el argumento explicito --generar.

El procedimiento que este script ejecutaba ya se realizo: los formatos
Dr. Condor estan en salidas/instrumentos/formatos_validacion/
_archivo_condor_no_usar/ y el material SIMULADO_DEMO esta en cuarentena en
salidas/archivo/_material_apocrifo_no_usar/SIMULADO_DEMO_JHON/. No queda nada
por mover.

Este archivo se conserva unicamente como registro del procedimiento de archivo
ya ejecutado y no debe volver a ejecutarse. El bloque de entrada imprime el
aviso y termina con codigo distinto de cero, sin escribir ningun archivo.
"""

import sys


def _operativo_original_deshabilitado():
    """Cuerpo original del operativo de archivado (2026-10-17). Sin invocar."""
    import os
    import shutil
    from pathlib import Path

    RUTA_BASE = Path(r"C:\MisInvestigaciones\tesis\sivac")
    DIR_FORMATOS = RUTA_BASE / "salidas" / "instrumentos" / "formatos_validacion"
    DIR_ARCHIVO = DIR_FORMATOS / "_archivo_condor_no_usar"
    DIR_ARCHIVO.mkdir(parents=True, exist_ok=True)

    movidos = []
    for f in DIR_FORMATOS.glob("FORMATO_VALIDACION_*.docx"):
        dst = DIR_ARCHIVO / f.name
        shutil.move(str(f), str(dst))
        movidos.append(f.name)
        print(f" [ARCHIVADO] {f.name} -> _archivo_condor_no_usar/")
    for f in DIR_FORMATOS.glob("FORMATO_VALIDACION_*.pdf"):
        dst = DIR_ARCHIVO / f.name
        shutil.move(str(f), str(dst))
        movidos.append(f.name)
        print(f" [ARCHIVADO] {f.name} -> _archivo_condor_no_usar/")

    DIR_JHON = RUTA_BASE / "salidas" / "documentos" / "anexos_jhon"
    DIR_DEMO = DIR_JHON / "SIMULADO_DEMO"
    if DIR_JHON.exists():
        DIR_DEMO.mkdir(parents=True, exist_ok=True)
        for f in DIR_JHON.glob("*MARCADO_A_MANO.docx"):
            dst = DIR_DEMO / f.name
            shutil.move(str(f), str(dst))
            print(f" [DEMO] {f.name} -> anexos_jhon/SIMULADO_DEMO/")
        for f in DIR_JHON.glob("*MARCADO_A_MANO.pdf"):
            dst = DIR_DEMO / f.name
            shutil.move(str(f), str(dst))
            print(f" [DEMO] {f.name} -> anexos_jhon/SIMULADO_DEMO/")

    readme = DIR_ARCHIVO / "LEEME_ARCHIVO_CONDOR.md"
    readme.write_text(
        "# Archivo Condor. No usar para sustentacion\n\n"
        "Los formatos Dr. Condor (Tabla 8 columnas, escala 1-4) se archivan aqui "
        "por instruccion del tesista (2026-10-17).\n\n"
        "**Certificados Jhon retirados:** los tres espejos "
        "`ANEXO_6_VALIDACION_EXPERTO_*_JHON_ESPEJO_VACIO.docx` ya no son "
        "expediente oficial. Se conservan en "
        "`salidas/documentos/anexos_jhon/_archivo_obsoleto/`, con la nota "
        "`LEEME_CERTIFICADOS_JHON_RETIRADOS.md` que documenta el retiro "
        "(DEC-015).\n\n"
        "**Expediente oficial vigente:** certificado unico del Instrumento "
        "N.° 03, Modalidad A, en `salidas/documentos/anexos_fany/`, modelo "
        "Fany 2024, conforme a DEC-015 y DEC-020.\n\n"
        "No eliminar este respaldo.\n",
        encoding="utf-8",
    )
    print(
        f"\n[OK] {len(movidos)} formatos Condor archivados. "
        "Los espejos Jhon estan retirados en anexos_jhon/_archivo_obsoleto/ "
        "(DEC-015). Expediente oficial vigente: certificado unico del "
        "Instrumento N.° 03, Modalidad A, en salidas/documentos/anexos_fany/ "
        "(DEC-015 y DEC-020)."
    )

    print("\n--- Queda en formatos_validacion/ ---")
    for f in DIR_FORMATOS.iterdir():
        print(" ", f.name)
    print("\n--- Queda en anexos_jhon/ ---")
    if DIR_JHON.exists():
        for f in sorted(DIR_JHON.iterdir()):
            print(" ", f.name, "(dir)" if f.is_dir() else "")


def imprimir_uso_retirado():
    """Explica por que el script no se ejecuta. No escribe ningun archivo."""
    print("=" * 78)
    print("SIVAC - ARCHIVO DE LOS ESPEJOS JHON: PROCEDIMIENTO RETIRADO")
    print("=" * 78)
    print("Este script quedo sin efecto el 2026-10-18.")
    print()
    print("DEC-015 sustituyo el modelo Jhon 2026 por el modelo Fany 2024 como")
    print("formato oficial de validacion por juicio de expertos.")
    print()
    print("El archivado de los tres espejos JHON ya se ejecuto el 2026-10-18:")
    print("  salidas/documentos/anexos_jhon/_archivo_obsoleto/")
    print("  salidas/documentos/anexos_jhon/_archivo_obsoleto/"
          "LEEME_CERTIFICADOS_JHON_RETIRADOS.md")
    print()
    print("Expediente oficial vigente (DEC-015 y DEC-020): certificado unico del")
    print("Instrumento N.° 03, Modalidad A, en salidas/documentos/anexos_fany/.")
    print("Generador: scripts/compiladores/generar_anexo2_validacion_fany.py --generar")
    print()
    print("Este script no escribe ningun archivo. Consulte la nota de retiro")
    print("antes de cualquier operacion sobre anexos_jhon/.")
    print("=" * 78)


def main():
    """Guarda de ejecucion: bloquea el script y termina con codigo 1."""
    imprimir_uso_retirado()
    sys.exit(1)


if __name__ == "__main__":
    main()
