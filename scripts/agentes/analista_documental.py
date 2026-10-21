# -*- coding: utf-8 -*-
"""
Analista documental estructural en modo solo lectura para .docx, .pdf y .xlsx (Modelos UNAJMA) — Squad E.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad
