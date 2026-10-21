# -*- coding: utf-8 -*-
"""
Control de calidad de 4 niveles para ingesta de datos de campo (N = n = 14) — Squad B.
Nivel 1: Estructura (14 filas TRAB-01..TRAB-14, cero faltantes)
Nivel 2: Rangos (t_reg (0,120], t_vale (0,60], rsd/cpe [0,100], Likert 1-5 enteros)
Nivel 3: Consistencia (score_ap, score_up, score_tam_total y baremo 8-18 Bajo, 19-29 Medio, 30-40 Alto)
Nivel 4: Trazabilidad SHA-256
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad
