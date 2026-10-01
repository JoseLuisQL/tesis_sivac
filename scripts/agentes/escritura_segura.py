#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Escritor de salidas con guardas de seguridad.

Único punto de escritura del módulo de inventario de syncova: el script
`inventario_syncova.py` no contiene ninguna operación de escritura propia, de
modo que su solo-lectura sobre el repositorio inspeccionado es auditable.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad  # noqa: E402

# Vetos propios del módulo, adicionales a los de seguridad.py (que no cubre la raíz de
# referencias/ ni datos/raw/): referencias inmutables y datos de campo.
_VETADAS = (rutas.REFERENCIAS, rutas.DATOS_RAW, rutas.SYNCOVA)
_NOMBRES_VETADOS = {"proyecto_tesis.docx"}


def _bajo(ruta: Path, base: Path) -> bool:
    try:
        ruta.relative_to(Path(base).resolve(strict=False))
        return True
    except ValueError:
        return False


def _zonas_permitidas() -> tuple[Path, ...]:
    """Lista BLANCA de carpetas donde este módulo puede escribir: salidas/ y el temporal del SO.

    Se evalúa en cada llamada (no al importar) para respetar SIVAC_ROOT y pruebas.
    Cualquier otra ruta —vault de Obsidian, CLAUDE.md, .claude/, scripts/, datos/— se rechaza.
    """
    return (Path(rutas.SALIDAS).resolve(strict=False), Path(tempfile.gettempdir()).resolve(strict=False))


def validar_destino(destino: str | Path) -> Path:
    """Valida un destino de escritura: aplica seguridad.py, los vetos y la lista blanca del módulo."""
    ruta = seguridad.asegurar_escritura_permitida(destino)
    for veto in _VETADAS:
        if _bajo(ruta, veto):
            raise seguridad.EscrituraProhibida(
                f"Escritura denegada (referencias/, datos/raw/ y syncova son intocables): {ruta}"
            )
    if ruta.name.lower() in _NOMBRES_VETADOS:
        raise seguridad.EscrituraProhibida(f"Escritura denegada sobre el documento base: {ruta}")
    if not any(_bajo(ruta, zona) for zona in _zonas_permitidas()):
        raise seguridad.EscrituraProhibida(
            f"Escritura denegada: solo se admite salidas/ (o el directorio temporal). Destino: {ruta}"
        )
    return ruta


def escribir_salida(destino: str | Path, contenido: str, *, no_escribir_en: str | Path | None = None,
                    sobrescribir: bool = False) -> Path:
    """Escribe `contenido` en `destino` tras validar que la ruta sea permitida.

    `no_escribir_en` es el repositorio inspeccionado: nunca se escribe dentro de él.
    Un archivo existente NO se pisa salvo `sobrescribir=True` (lanza FileExistsError).
    """
    ruta = validar_destino(destino)
    if no_escribir_en is not None:
        base = Path(no_escribir_en).expanduser().resolve(strict=False)
        try:
            ruta.relative_to(base)
        except ValueError:
            pass
        else:
            raise seguridad.EscrituraProhibida(
                f"El destino está dentro del repositorio inspeccionado (solo lectura): {ruta}"
            )
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w" if sobrescribir else "x", encoding="utf-8", newline="\n") as f:
        f.write(contenido)
    return ruta
