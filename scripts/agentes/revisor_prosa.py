# -*- coding: utf-8 -*-
"""
Revisor automático de prosa científica académica en español conforme a Regla Canónica 03 — Squad E.
Detecta primera persona, frases de relleno, párrafos fuera de 4-8 oraciones, uso de '&' y conteo de 250 palabras en Resumen.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad
