# -*- coding: utf-8 -*-
"""
Descargador y verificador de fuentes bibliográficas por DOI vía Crossref y OpenAlex (Squad A).
Genera ficha en Obsidian y payload para registro en Zotero (colección 4XAQ6D3D).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad
from scripts.fuentes import texto
