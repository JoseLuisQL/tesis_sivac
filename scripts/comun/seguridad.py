#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Guardas de seguridad para scripts (defensa en profundidad).

El hook PreToolUse protege las herramientas del agente; estas guardas protegen
además la ejecución de los propios scripts: ningún script puede escribir en
rutas inmutables, aunque se invoque directamente desde una terminal.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from . import rutas

# Rutas donde NUNCA se escribe (ni se mueve ni se borra).
_PROTEGIDAS = (
    rutas.SYNCOVA,
    rutas.MODELOS_TESIS,
    rutas.MODELOS_VALIDACION,
    rutas.PROYECTO_BASE,
)


class EscrituraProhibida(PermissionError):
    """Intento de escribir en una ruta inmutable del proyecto."""


def _resolver(ruta: str | Path) -> Path:
    return Path(ruta).expanduser().resolve(strict=False)


def _es_subruta(hijo: Path, padre: Path) -> bool:
    try:
        hijo.relative_to(padre.resolve(strict=False))
        return True
    except ValueError:
        return False


def asegurar_escritura_permitida(ruta: str | Path) -> Path:
    """Devuelve la ruta resuelta o lanza EscrituraProhibida si es inmutable."""
    destino = _resolver(ruta)
    for protegida in _PROTEGIDAS:
        if _es_subruta(destino, protegida):
            raise EscrituraProhibida(
                f"Escritura denegada en ruta inmutable: {destino} "
                f"(protegida: {protegida}). Ver .claude/rules/01_seguridad.md"
            )
    return destino


def asegurar_no_sobrescribe(origen: str | Path, destino: str | Path) -> Path:
    """Impide que una operación 'guardar como' pise el archivo de origen."""
    o, d = _resolver(origen), _resolver(destino)
    if o == d:
        raise EscrituraProhibida(
            "El destino coincide con el original; se exige una copia versionada "
            f"(p. ej. informe_final_v02.docx): {d}"
        )
    return asegurar_escritura_permitida(d)


def sha256_archivo(ruta: str | Path, bloque: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for chunk in iter(lambda: f.read(bloque), b""):
            h.update(chunk)
    return h.hexdigest()


def configurar_utf8() -> None:
    """Evita UnicodeEncodeError en consolas Windows (cp1252)."""
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
