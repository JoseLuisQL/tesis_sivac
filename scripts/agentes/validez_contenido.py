# -*- coding: utf-8 -*-
"""
Validador psicométrico por juicio de expertos bajo modelo vigente Fany 2024 (DEC-015, DEC-020).
Calcula V de Aiken dicotómico (c = 2, V = S/n) con IC 95% de Penfield & Giacobbi (2004)
e IVC de Tristán-López (2008) sobre los 8 ítems de la Modalidad A del Instrumento N.° 03.
"""
import math
import sys
from pathlib import Path
from typing import Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad


def v_aiken_dicotomico(aciertos_si: int, n_jueces: int) -> float:
    """Con l = 0 y c = 2, V = S / (n * (c - 1)) se reduce a S / n."""
    if n_jueces <= 0:
        raise ValueError("El número de jueces debe ser mayor que cero.")
    return aciertos_si / float(n_jueces)


def ic95_penfield_giacobbi(v: float, n: int, z: float = 1.95996) -> Tuple[float, float]:
    """Intervalo de confianza asimétrico al 95% de Penfield & Giacobbi (2004) con k = c - 1 = 1."""
    z2 = z * z
    disc = max(0.0, z2 - 2.0 - (1.0 / n) + 4.0 * n * v * (1.0 - v))
    raiz = math.sqrt(disc)
    denom = 2.0 * (n + z2)
    lim_inf = max(0.0, (2.0 * n * v + z2 - 1.0 - z * raiz) / denom)
    lim_sup = min(1.0, (2.0 * n * v + z2 + 1.0 + z * raiz) / denom)
    return (round(lim_inf, 4), round(lim_sup, 4))
