# -*- coding: utf-8 -*-
"""
Buscador y verificador 1:1 de citas exactas en fuentes PDF indexadas (Squad A).
Formatea citas en APA 7 en español ("et al." desde 3 autores, p. [VERIFICAR] si no hay etiqueta impresa).
"""
import sys
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad
from scripts.fuentes import texto


def formatear_cita_apa7(
    coincidencia: Dict,
    autores: List[str],
    anio: int,
    tipo: str = "parafrasis",
) -> str:
    if not autores:
        autor_str = "[VERIFICAR: autor]"
    elif len(autores) == 1:
        autor_str = autores[0]
    elif len(autores) == 2:
        autor_str = f"{autores[0]} y {autores[1]}"
    else:
        autor_str = f"{autores[0]} et al."

    if tipo == "parafrasis":
        return f"({autor_str}, {anio})"

    etiqueta = coincidencia.get("etiqueta_impresa")
    pag_fisica = coincidencia.get("pagina_fisica", "?")
    if etiqueta:
        return f"({autor_str}, {anio}, p. {etiqueta})"
    return f"({autor_str}, {anio}, p. [VERIFICAR: página impresa no determinada; pág. PDF {pag_fisica}])"
