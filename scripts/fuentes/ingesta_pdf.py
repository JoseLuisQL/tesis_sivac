# -*- coding: utf-8 -*-
"""
Módulo de ingesta e indexación de fuentes PDF con mapeo de página física y etiqueta impresa.
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad
from scripts.fuentes import texto


def cargar_indice(ruta_pdf: Path) -> Dict[str, Any]:
    """Carga el índice JSON cacheado de un PDF desde el vault o devuelve estructura base."""
    nombre_idx = f"{texto.slug(Path(ruta_pdf).stem)}.idx.json"
    ruta_idx = rutas.INDICES_PDF / nombre_idx
    if ruta_idx.exists():
        return json.loads(ruta_idx.read_text(encoding="utf-8"))
    return {
        "archivo": str(ruta_pdf),
        "paginas": [],
    }
