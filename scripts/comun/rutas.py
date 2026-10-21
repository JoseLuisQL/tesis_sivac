# -*- coding: utf-8 -*-
"""
Módulo canónico de rutas y constantes institucionales de SIVAC-THESIS-LAB.
Alineado con CLAUDE.md, DEC-007, DEC-015, DEC-019, DEC-020 y DEC-027.
"""
import os
from pathlib import Path

RAIZ_REPO = Path(os.environ.get("SIVAC_ROOT", Path(__file__).resolve().parents[2]))

_vault_env = os.environ.get("SIVAC_VAULT", "")
if _vault_env and Path(_vault_env).exists():
    BOVEDA_OBSIDIAN = Path(_vault_env)
elif Path("C:/MisInvestigaciones/obsidian_vault").exists():
    BOVEDA_OBSIDIAN = Path("C:/MisInvestigaciones/obsidian_vault")
else:
    BOVEDA_OBSIDIAN = RAIZ_REPO / "obsidian_vault"

RUTA_SYNCOVA = Path("C:/Proyectos/syncova")

# Constantes Institucionales Oficiales (DEC-027 / DEC-007)
TITULO_OFICIAL = (
    "APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS "
    "MENSUALES DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN "
    "DE SALUD APURÍMAC II"
)
TESISTA = "Bach. José Luis Quispe León"
ASESORA = "Dra. Norma Lorena Catacora Flores"
UNIVERSIDAD = "Universidad Nacional José María Arguedas (UNAJMA)"
ESCUELA = "Escuela Profesional de Ingeniería de Sistemas"
N_CENSAL = 14
ZOTERO_COLECCION = "4XAQ6D3D"

DIMENSIONES_DEC007 = (
    "Oportunidad de procesamiento",
    "Consistencia documental",
    "Satisfacción del usuario",
)

INDICADORES_DEC007 = (
    "T_reg",
    "T_vale",
    "RSD",
    "CPE",
    "AP",
    "UP",
)

# Capas Canónicas del Repositorio
CAPA_CLAUDE = RAIZ_REPO / ".claude"
CAPA_REFERENCIAS = RAIZ_REPO / "referencias"
CAPA_DATOS = RAIZ_REPO / "datos"
CAPA_SCRIPTS = RAIZ_REPO / "scripts"
CAPA_SALIDAS = RAIZ_REPO / "salidas"

# Subdirectorios de Datos
DATOS_RAW = CAPA_DATOS / "raw"
DATOS_PROCESSED = CAPA_DATOS / "processed"
DATOS_PLANTILLAS = CAPA_DATOS / "plantillas"
DATOS_SCHEMAS = CAPA_DATOS / "schemas"

# Subdirectorios de Salidas
SALIDAS_DOCUMENTOS = CAPA_SALIDAS / "documentos"
SALIDAS_FIGURAS = CAPA_SALIDAS / "figuras"
SALIDAS_INSTRUMENTOS = CAPA_SALIDAS / "instrumentos"
SALIDAS_REPORTES_JURADO = CAPA_SALIDAS / "reportes_jurado"
SALIDAS_REPORTES_ESTADISTICOS = CAPA_SALIDAS / "reportes_estadisticos"
SALIDAS_ARCHIVO = CAPA_SALIDAS / "archivo"
FIGURAS_FUENTES = SALIDAS_FIGURAS / "fuentes"

# Rutas del Vault de Obsidian
INDICES_PDF = BOVEDA_OBSIDIAN / "04_LITERATURA_Y_FUENTES" / "indices_pdf"
PDFS_FUENTES = BOVEDA_OBSIDIAN / "04_LITERATURA_Y_FUENTES" / "pdfs_fuentes"
NOTAS_FUENTES = BOVEDA_OBSIDIAN / "04_LITERATURA_Y_FUENTES" / "notas_fuentes_zotero"
ESTADO_TESIS_MD = BOVEDA_OBSIDIAN / "00_SISTEMA" / "ESTADO_TESIS.md"
DECISIONES_MD = BOVEDA_OBSIDIAN / "00_SISTEMA" / "DECISIONES.md"
HANDOFFS_DIR = BOVEDA_OBSIDIAN / "08_SISTEMA_Y_AGENTES" / "handoffs"
BITACORAS_DIR = BOVEDA_OBSIDIAN / "08_SISTEMA_Y_AGENTES" / "bitacoras"
