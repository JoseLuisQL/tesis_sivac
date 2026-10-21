# -*- coding: utf-8 -*-
"""
Utilidades de normalización textual, extracción de DOIs y tokenización para SIVAC-THESIS-LAB.
"""
import re
import unicodedata
from typing import List, Optional

REGEX_DOI = re.compile(r"\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)\b")


def limpiar_pdf(texto: str) -> str:
    """Une palabras cortadas por guion al final de línea y normaliza espacios de extracción PDF."""
    if not texto:
        return ""
    sin_guion = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", texto)
    sin_saltos = re.sub(r"\s+", " ", sin_guion)
    return sin_saltos.strip()


def canonico(texto: str) -> str:
    """Convierte texto a minúsculas sin tildes ni signos de puntuación redundantes."""
    if not texto:
        return ""
    nfd = unicodedata.normalize("NFD", limpiar_pdf(texto))
    sin_tildes = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", sin_tildes.lower()).strip()


def tokens(texto: str) -> List[str]:
    """Devuelve la lista de tokens alfanuméricos canónicos."""
    return re.findall(r"[a-z0-9]+", canonico(texto))


def extraer_doi(texto: str) -> Optional[str]:
    """Extrae y limpia un identificador DOI desde cualquier cadena o URL."""
    if not texto:
        return None
    limpio = texto.replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
    m = REGEX_DOI.search(limpio)
    if not m:
        return None
    return m.group(1).rstrip(".,;)")


def slug(texto: str, max_len: int = 60) -> str:
    """Genera un identificador seguro para nombres de archivo o carpetas."""
    base = re.sub(r"[^a-z0-9]+", "-", canonico(texto)).strip("-")
    return base[:max_len].strip("-") or "sin-titulo"
