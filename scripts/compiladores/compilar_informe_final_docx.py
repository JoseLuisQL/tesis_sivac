#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB — COMPILADOR MAESTRO DEL INFORME FINAL DE TESIS (.DOCX)
Universidad Nacional José María Arguedas (UNAJMA)
Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas

Compila la versión completa y definitiva de:
salidas/informe_final_v01.docx

Estructura Institucional UNAJMA (APA 7 Adaptado):
- Sección 1 (Preliminares): Romanos minúsculas (i, ii, iii...), desvinculada.
  * Portada Exterior Empastada (Anexo 17 con escudo UNAJMA)
  * Carátula Interior
  * Declaración Jurada (Anexo 32)
  * Dedicatoria y Agradecimientos
  * Resumen (250 palabras), Abstract y Chumasqa (Quechua Chanka)
  * Índices de Contenido, Tablas y Figuras
- Sección 2 (Cuerpo Principal y Anexos): Arábigos reiniciados en 1, desvinculada.
  * Introducción
  * Capítulo I: Problema de Investigación
  * Capítulo II: Antecedentes de la Investigación
  * Capítulo III: Marco Teórico y Desarrollo de la Solución (XP)
  * Capítulo IV: Metodología de la Investigación
  * Capítulo V: Resultados
  * Capítulo VI: Discusión de Resultados
  * Conclusiones (1:1)
  * Recomendaciones (1:1)
  * Referencias Bibliográficas (APA 7, sangría francesa, 33 fuentes auditadas)
  * Anexos (Anexos 1 al 8)
================================================================================
"""

import os
import sys
import docx
from docx.enum.section import WD_SECTION

# Configurar resolución de rutas y paquetes en sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
UTILIDADES_DIR = os.path.join(PROJECT_ROOT, "scripts", "utilidades")

for d in [SCRIPT_DIR, UTILIDADES_DIR, PROJECT_ROOT]:
    if d not in sys.path:
        sys.path.insert(0, d)

from docx_utilidades import (
    aplicar_margenes_unajma,
    configurar_numeracion
)

from secciones_preliminares import construir_seccion_preliminares
from capitulo1_builder import construir_introduccion, construir_capitulo1
from capitulo2_builder import construir_capitulo2
from capitulo3_builder import construir_capitulo3
from capitulo4_builder import construir_capitulo4
from capitulo5_builder import construir_capitulo5
from capitulo6_builder import construir_capitulo6_y_final

BASE_DIR = PROJECT_ROOT
SALIDA_DOCX = os.path.join(PROJECT_ROOT, "salidas", "documentos", "informe_final_v01.docx")

def compilar_informe_completo():
    print("=" * 80)
    print("SIVAC-THESIS-LAB: INICIANDO COMPILACIÓN MAESTRA DEL INFORME FINAL DE TESIS")
    print(f"Destino: {SALIDA_DOCX}")
    print("=" * 80)

    # 1. Crear documento en blanco
    doc = docx.Document()

    # --------------------------------------------------------------------------
    # SECCIÓN 1: PÁGINAS PRELIMINARES (Numeración romana minúscula)
    # --------------------------------------------------------------------------
    print("\n[+] Configurando Sección 1: Páginas Preliminares...")
    seccion_preliminares = doc.sections[0]
    aplicar_margenes_unajma(seccion_preliminares)
    configurar_numeracion(
        seccion_preliminares,
        tipo='lowerRoman',
        start_num=1,
        desvincular=False,
        omitir_primera=True
    )

    print("    -> Ensamblando Portada, Carátula, Declaración Jurada, Dedicatoria, Agradecimientos...")
    print("    -> Ensamblando Resumen, Abstract, Chumasqa e Índices Preliminares...")
    construir_seccion_preliminares(doc, BASE_DIR)
    print("    [OK] Sección 1 completada con éxito.")

    # --------------------------------------------------------------------------
    # SECCIÓN 2: CUERPO PRINCIPAL Y ANEXOS (Numeración arábiga reiniciada en 1)
    # --------------------------------------------------------------------------
    print("\n[+] Creando y desvinculando Sección 2: Cuerpo Principal...")
    seccion_cuerpo = doc.add_section(WD_SECTION.NEW_PAGE)
    aplicar_margenes_unajma(seccion_cuerpo)
    configurar_numeracion(
        seccion_cuerpo,
        tipo='decimal',
        start_num=1,
        desvincular=True,
        omitir_primera=False
    )

    print("    -> Ensamblando Introducción y Capítulo I: Problema de Investigación...")
    construir_introduccion(doc)
    construir_capitulo1(doc)

    print("    -> Ensamblando Capítulo II: Antecedentes de la Investigación...")
    construir_capitulo2(doc)

    print("    -> Ensamblando Capítulo III: Marco Teórico y Metodología XP...")
    construir_capitulo3(doc)

    print("    -> Ensamblando Capítulo IV: Metodología de la Investigación...")
    construir_capitulo4(doc)

    print("    -> Ensamblando Capítulo V: Resultados Estadísticos e Inferenciales...")
    construir_capitulo5(doc)

    print("    -> Ensamblando Capítulo VI: Discusión, Conclusiones, Recomendaciones, Referencias y Anexos...")
    construir_capitulo6_y_final(doc)

    # --------------------------------------------------------------------------
    # GUARDADO DEL DOCUMENTO FINAL
    # --------------------------------------------------------------------------
    os.makedirs(os.path.dirname(SALIDA_DOCX), exist_ok=True)
    print(f"\n[+] Guardando documento maestro en: {SALIDA_DOCX}")
    doc.save(SALIDA_DOCX)

    tamano_kb = os.path.getsize(SALIDA_DOCX) / 1024
    print("=" * 80)
    print(f"[*] COMPILACIÓN EXITOSA: {SALIDA_DOCX}")
    print(f"    - Tamaño generado: {tamano_kb:.2f} KB")
    print(f"    - Secciones OpenXML: {len(doc.sections)}")
    print(f"    - Párrafos totales: {len(doc.paragraphs)}")
    print(f"    - Tablas totales: {len(doc.tables)}")
    print("=" * 80)
    return True

if __name__ == "__main__":
    compilar_informe_completo()
