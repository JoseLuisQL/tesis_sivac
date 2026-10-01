#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Normalización de texto para localización exacta de citas.

Función central: convertir texto "sucio" de PDF (ligaduras, guiones de corte de
línea, comillas tipográficas, espacios raros) a una forma canónica comparable,
conservando un mapa de posiciones para poder volver al texto original.
"""

from __future__ import annotations

import re
import unicodedata

_LIGADURAS = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "st", "ﬆ": "st"}
_COMILLAS = {"“": '"', "”": '"', "„": '"', "«": '"', "»": '"', "‘": "'", "’": "'", "‚": "'", "´": "'", "`": "'"}
_GUIONES = {"‐": "-", "‑": "-", "‒": "-", "–": "-", "—": "-", "−": "-", "­": ""}

# Palabra cortada por fin de línea: "proce-\nso" -> "proceso"
_RE_CORTE = re.compile(r"(\w)[-­]\s*\n\s*(\w)")
_RE_ESPACIOS = re.compile(r"\s+")

RE_DOI = re.compile(r"\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+[A-Za-z0-9])", re.I)
RE_ANIO = re.compile(r"\b(19[5-9]\d|20[0-3]\d)\b")


def limpiar_pdf(texto: str) -> str:
    """Limpieza *conservadora* (mantiene mayúsculas y tildes) para mostrar/guardar."""
    if not texto:
        return ""
    for k, v in _LIGADURAS.items():
        texto = texto.replace(k, v)
    texto = _RE_CORTE.sub(r"\1\2", texto)
    texto = texto.replace(" ", " ").replace("​", "")
    texto = re.sub(r"[ \t]*\n[ \t]*", " ", texto)
    return _RE_ESPACIOS.sub(" ", texto).strip()


def canonico(texto: str, quitar_tildes: bool = True) -> str:
    """Forma canónica para comparar: minúsculas, sin tildes, sin signos ni dobles espacios."""
    t = limpiar_pdf(texto)
    for k, v in _COMILLAS.items():
        t = t.replace(k, v)
    for k, v in _GUIONES.items():
        t = t.replace(k, v)
    t = unicodedata.normalize("NFKC", t)
    if quitar_tildes:
        t = "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")
    t = t.lower()
    t = re.sub(r"[^\w\s%.,;:()\-/]", " ", t)  # conserva puntuación con valor citable
    return _RE_ESPACIOS.sub(" ", t).strip()


def tokens(texto: str) -> list[str]:
    return re.findall(r"[a-z0-9áéíóúñü]+", canonico(texto, quitar_tildes=False))


def extraer_doi(texto: str) -> str | None:
    m = RE_DOI.search(texto or "")
    if not m:
        return None
    return m.group(1).rstrip(".,;)")


def slug(texto: str, maximo: int = 60) -> str:
    t = canonico(texto)
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:maximo].strip("-") or "sin-titulo"
