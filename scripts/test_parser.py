#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba del motor de parseo de markdown a DOCX para capítulos de tesis SIVAC.
"""

import os
import re
import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def parsear_lineas_tabla(lineas):
    """Convierte líneas de tabla markdown en una matriz de celdas de texto."""
    filas = []
    for l in lineas:
        l = l.strip()
        if not l.startswith('|'):
            continue
        # Descartar fila separadora |---|---|
        if re.match(r'^\|[\s\-:|]+\|$', l):
            continue
        # Partir celdas
        partes = [c.strip() for c in l.split('|')[1:-1]]
        filas.append(partes)
    return filas

print("[*] Test parser listo.")
