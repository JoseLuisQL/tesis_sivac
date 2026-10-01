#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Rutas canónicas compartidas por todos los scripts.

Única fuente de verdad para ubicaciones del workspace y del vault de Obsidian.
Cada ruta puede sobrescribirse con variables de entorno (útil en pruebas):

    SIVAC_ROOT, SIVAC_VAULT, SIVAC_SYNCOVA
"""

from __future__ import annotations

import os
from pathlib import Path

# scripts/comun/rutas.py -> raíz del workspace = dos niveles arriba de scripts/
RAIZ = Path(os.environ.get("SIVAC_ROOT", Path(__file__).resolve().parents[2]))
VAULT = Path(os.environ.get("SIVAC_VAULT", r"C:\MisInvestigaciones\obsidian_vault"))
SYNCOVA = Path(os.environ.get("SIVAC_SYNCOVA", r"C:\Proyectos\syncova"))

# --- Capa 1: insumos inmutables -------------------------------------------
REFERENCIAS = RAIZ / "referencias"
MODELOS_TESIS = REFERENCIAS / "modelos_tesis"
MODELOS_VALIDACION = REFERENCIAS / "modelos_validacion"
PROYECTO_BASE = REFERENCIAS / "proyecto_base"

# --- Capa 2: datos ----------------------------------------------------------
DATOS = RAIZ / "datos"
DATOS_RAW = DATOS / "raw"
DATOS_PROCESSED = DATOS / "processed"
DATOS_PLANTILLAS = DATOS / "plantillas"
DATOS_SCHEMAS = DATOS / "schemas"

# --- Capa 4: salidas --------------------------------------------------------
SALIDAS = RAIZ / "salidas"
SALIDAS_DOCUMENTOS = SALIDAS / "documentos"
SALIDAS_FIGURAS = SALIDAS / "figuras"

# --- Esquemas JSON de gobernanza -------------------------------------------
SCHEMAS_CLAUDE = RAIZ / ".claude" / "schemas"

# --- Vault de Obsidian (cerebro) -------------------------------------------
LITERATURA = VAULT / "04_LITERATURA_Y_FUENTES"
PDFS_FUENTES = LITERATURA / "PDFs_articulos" / "PDFs_SIVAC"
NOTAS_FUENTES = LITERATURA / "notas_fuentes_zotero"
INDICES_PDF = LITERATURA / "indices_pdf"
FIGURAS_FUENTES = VAULT / "_adjuntos" / "figuras_fuentes"
HANDOFFS = VAULT / "08_SISTEMA_Y_AGENTES" / "handoffs"
BITACORAS = VAULT / "08_SISTEMA_Y_AGENTES" / "bitacoras"
ESTADO_TESIS = VAULT / "00_SISTEMA" / "ESTADO_TESIS.md"

# --- Constantes metodológicas (DEC-007) ------------------------------------
ZOTERO_COLECCION = "4XAQ6D3D"
N_CENSAL = 14
TITULO_OFICIAL = (
    "APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE "
    "VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II"
)
TESISTA = "Bach. José Luis Quispe León"
ASESORA = "Dra. Norma Lorena Catacora Flores"
DIMENSIONES_VD = (
    "Oportunidad de procesamiento",
    "Consistencia documental",
    "Satisfacción del usuario",
)
INDICADORES = ("T_reg", "T_vale", "RSD", "CPE", "AP", "UP")
