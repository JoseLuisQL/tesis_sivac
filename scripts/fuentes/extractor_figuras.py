# -*- coding: utf-8 -*-
"""
Extractor trazable de figuras y tablas desde fuentes PDF a 300 DPI exactos con sidecar JSON (Squad A/E).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad

DPI_OFICIAL = 300
ZOOM_300_DPI = 300.0 / 72.0
