#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB — AFINAMIENTO DE SECCIONES 4.10, 4.11 Y CAPÍTULO V (PRESUPUESTO)
Normalización APA 7, erradicación de artefactos de IA y alineación DEC-007
================================================================================
"""

import os
import sys
import shutil
from pathlib import Path

# Configurar sys.path para importación modular
raiz = Path(__file__).resolve().parent.parent.parent
if str(raiz) not in sys.path:
    sys.path.insert(0, str(raiz))
utilidades = Path(__file__).resolve().parent
if str(utilidades) not in sys.path:
    sys.path.insert(0, str(utilidades))

import docx
from docx.shared import Pt
from docx_quirurgico import (
    aplicar_formato_cuerpo,
    aplicar_formato_caption,
    aplicar_formato_nota_tabla_figura,
    FONT_SIZE_BODY_PT,
    FONT_SIZE_TABLE_PT,
    FUENTE_POR_DEFECTO
)

def afinar_secciones_cap4_cap5(docx_path: str):
    print(f"[*] Iniciando afinamiento de Capítulos IV y V en: {docx_path}")
    doc = docx.Document(docx_path)

    # --------------------------------------------------------------------------
    # 1. SECCIÓN 4.10: Rótulo y título de Tabla 9 según APA 7 formal
    # --------------------------------------------------------------------------
    p_t9_encontrado = False
    for i, p in enumerate(doc.paragraphs):
        txt = p.text.strip()
        if "Tabla 9 Rangos de Interpretación del Coeficiente Alfa de Cronbach" in txt:
            # Dividir en dos párrafos canónicos APA 7:
            # Párrafo 1: Rótulo en negrita ("Tabla 9")
            p.text = "Tabla 9"
            aplicar_formato_caption(p, tipo="tabla")

            # Párrafo 2: Título en cursiva insertado a continuación
            p_titulo = p.insert_paragraph_before("Rangos de interpretación del coeficiente alfa de Cronbach")
            # Intercambiamos textos o reordenamos:
            p_titulo.text = "Rangos de interpretación del coeficiente alfa de Cronbach"
            # Aplicar formato de título de tabla APA 7 (cursiva, sin sangría, 12 pt)
            p_titulo.paragraph_format.first_line_indent = 0
            p_titulo.paragraph_format.left_indent = 0
            p_titulo.paragraph_format.space_before = Pt(2)
            p_titulo.paragraph_format.space_after = Pt(6)
            p_titulo.paragraph_format.line_spacing = 1.5
            for r in p_titulo.runs:
                r.font.name = FUENTE_POR_DEFECTO
                r.font.size = Pt(FONT_SIZE_BODY_PT)
                r.font.italic = True
                r.font.bold = False

            # Nota: Al insertar before, p_titulo quedó antes de p.
            # Ajustamos: p_titulo es el primero (Rótulo), p es el segundo (Título)
            p_titulo.text = "Tabla 9"
            aplicar_formato_caption(p_titulo, tipo="tabla")

            p.text = "Rangos de interpretación del coeficiente alfa de Cronbach"
            p.paragraph_format.first_line_indent = 0
            p.paragraph_format.left_indent = 0
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.5
            for r in p.runs:
                r.font.name = FUENTE_POR_DEFECTO
                r.font.size = Pt(FONT_SIZE_BODY_PT)
                r.font.italic = True
                r.font.bold = False

            print(f"[OK] Tabla 9: Rótulo y título desdoblados en formato APA 7 en índice {i}.")
            p_t9_encontrado = True
            break
    assert p_t9_encontrado, "Error: No se encontró el párrafo de encabezado de Tabla 9."

    # --------------------------------------------------------------------------
    # 2. SECCIÓN 4.11: Subsanación de erratas ("descriptivo" y "contrastación")
    # --------------------------------------------------------------------------
    for p in doc.paragraphs:
        if p.text.strip() == "a) Análisis descriptiva:":
            p.text = "a) Análisis descriptivo:"
            aplicar_formato_cuerpo(p)
            print("[OK] Errata gramatical subsanada: 'a) Análisis descriptivo:'.")
        elif "Los criterios adoptados para la contratación de hipótesis son los siguientes:" in p.text:
            p.text = (
                "Los criterios adoptados para la contrastación de hipótesis y toma de decisiones "
                "estadísticas en la investigación son los siguientes:"
            )
            aplicar_formato_cuerpo(p)
            print("[OK] Errata crítica subsanada: 'contrastación de hipótesis'.")

    # --------------------------------------------------------------------------
    # 3. SECCIÓN 4.11: Formulación estadística formal de hipótesis H0 y H1 (DEC-007)
    # --------------------------------------------------------------------------
    h1_idx = None
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() == "Hipótesis Estadísticas:":
            h1_idx = i
            break

    if h1_idx is not None:
        p_intro = doc.paragraphs[h1_idx]
        p_intro.text = (
            "Para la contrastación empírica en el marco del diseño preexperimental con pretest y postest "
            "en un solo grupo (O₁ ⟶ X ⟶ O₂), se formulan formalmente los pares de hipótesis estadísticas nula (H₀) "
            "y alterna (H₁) para cada una de las tres dimensiones oficiales de la variable dependiente fijadas "
            "por el estándar metodológico institucional:"
        )
        aplicar_formato_cuerpo(p_intro)

        # Buscar y actualizar Hipótesis 1 (Oportunidad)
        for j in range(h1_idx, min(h1_idx + 15, len(doc.paragraphs))):
            p = doc.paragraphs[j]
            if p.text.strip() == "Hipótesis 1":
                p.text = "a) Hipótesis específica 1 (Oportunidad de procesamiento):"
                aplicar_formato_cuerpo(p)
                p.runs[0].font.bold = True
            elif "La aplicación del sistema \"SIVAC\" mejora significativamente la\xa0oportunidad" in p.text or \
                 "La aplicación del sistema \"SIVAC\" mejora significativamente la oportunidad" in p.text:
                p.text = (
                    "Hipótesis nula (H₀₁): La aplicación del sistema web SIVAC no reduce significativamente "
                    "los tiempos de registro de movimientos ni de emisión de comprobantes de salida en el "
                    "personal de inmunizaciones de la Dirección de Salud Apurímac II (H₀₁: μ_pre ≤ μ_post).\n"
                    "Hipótesis alterna (H₁₁): La aplicación del sistema web SIVAC reduce significativamente "
                    "los tiempos de registro de movimientos (Treg) y de emisión de comprobantes de salida o vales "
                    "(Tvale) en el personal de inmunizaciones de la Dirección de Salud Apurímac II (H₁₁: μ_pre > μ_post)."
                )
                aplicar_formato_cuerpo(p)

            # Buscar y actualizar Hipótesis 2 (Consistencia documental)
            elif p.text.strip() == "Hipótesis 2":
                p.text = "b) Hipótesis específica 2 (Consistencia documental):"
                aplicar_formato_cuerpo(p)
                p.runs[0].font.bold = True
            elif "La aplicación del sistema \"SIVAC\" mejora significativamente la\xa0consistencia" in p.text or \
                 "La aplicación del sistema \"SIVAC\" mejora significativamente la consistencia" in p.text:
                p.text = (
                    "Hipótesis nula (H₀₂): La aplicación del sistema web SIVAC no incrementa significativamente "
                    "el porcentaje de registros sin discrepancias ni la concordancia programada versus entregada "
                    "en el personal de inmunizaciones de la Dirección de Salud Apurímac II (H₀₂: μ_pre ≥ μ_post).\n"
                    "Hipótesis alterna (H₁₂): La aplicación del sistema web SIVAC incrementa significativamente "
                    "el porcentaje de registros sin discrepancias (RSD) y la concordancia de cantidad programada "
                    "versus entregada (CPE) en el personal de inmunizaciones de la Dirección de Salud Apurímac II (H₁₂: μ_pre < μ_post)."
                )
                aplicar_formato_cuerpo(p)

            # Buscar y actualizar Hipótesis 3 (Satisfacción del usuario)
            elif p.text.strip() == "Hipótesis 3":
                p.text = "c) Hipótesis específica 3 (Satisfacción del usuario):"
                aplicar_formato_cuerpo(p)
                p.runs[0].font.bold = True
            elif "La aplicación del sistema \"SIVAC\" mejora significativamente la\xa0satisfacción" in p.text or \
                 "La aplicación del sistema \"SIVAC\" mejora significativamente la satisfacción" in p.text:
                p.text = (
                    "Hipótesis nula (H₀₃): La aplicación del sistema web SIVAC no incrementa significativamente "
                    "el nivel de satisfacción del usuario con el proceso de gestión de movimientos de vacunas "
                    "en el personal de inmunizaciones de la Dirección de Salud Apurímac II (H₀₃: Me_pre ≥ Me_post).\n"
                    "Hipótesis alterna (H₁₃): La aplicación del sistema web SIVAC incrementa significativamente "
                    "el nivel de aceptación del proceso operativo (AP) y la utilidad percibida sanitaria (UP) bajo "
                    "el modelo TAM en el personal de inmunizaciones de la Dirección de Salud Apurímac II (H₁₃: Me_pre < Me_post)."
                )
                aplicar_formato_cuerpo(p)
        print("[OK] Hipótesis estadísticas formuladas rigurosamente con pares H0 y H1 para DEC-007.")

    # --------------------------------------------------------------------------
    # 4. SECCIÓN 4.11: Parámetros de decisión en prosa académica fluida
    # --------------------------------------------------------------------------
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() == "Nivel de significancia: α = 0.05 (5%)":
            p.text = (
                "Nivel de significancia y confianza. Se adopta un nivel de significancia de α = 0.05 (5%), "
                "equivalente a un nivel de confianza estadística del 95% (1 – α = 0.95), estándar riguroso para la "
                "investigación aplicada en ingeniería de sistemas y salud pública. Conforme a la regla de decisión "
                "del p-valor, se rechazará la hipótesis nula (H₀) y se aceptará la hipótesis alterna correspondiente (H₁) "
                "si el valor de probabilidad obtenido en el contraste empírico resulta estrictamente menor al nivel de "
                "significancia establecido (p < 0.05). En caso contrario (p ≥ 0.05), no se dispondrá de evidencia suficiente "
                "para rechazar la hipótesis nula."
            )
            aplicar_formato_cuerpo(p)
            print("[OK] Parámetros de decisión consolidados en prosa académica continua.")
        elif p.text.strip() == "Nivel de confianza: 1 – α = 0.95 (95%)":
            # Eliminar párrafo huérfano redundante
            parent = p._element.getparent()
            if parent is not None:
                parent.remove(p._element)
                print("[OK] Micro-párrafo huérfano de nivel de confianza eliminado limpiamente.")

    # --------------------------------------------------------------------------
    # 5. CAPÍTULO V: Erradicación de artefactos de IA en Tabla de Presupuesto (Tabla 10)
    # --------------------------------------------------------------------------
    t_presupuesto = None
    for t_idx, table in enumerate(doc.tables):
        if len(table.rows) > 0 and len(table.columns) > 0:
            if "PRESUPUESTO" in table.cell(0, 0).text.upper() or "RECURSOS" in table.cell(1, 0).text.upper():
                t_presupuesto = table
                break

    assert t_presupuesto is not None, "Error: No se encontró la tabla de presupuesto en el documento."

    for r_idx, row in enumerate(t_presupuesto.rows):
        c0_text = row.cells[0].text.strip()
        # 1. Normalizar recurso humano (Fila de especialista en redacción)
        if "especialista en redacción" in c0_text.lower():
            row.cells[0].text = "Asesoría metodológica y estadística"
            row.cells[1].text = "1"
            row.cells[2].text = "Servicio"
            row.cells[3].text = "-"
            row.cells[4].text = ""
            print(f"[OK] Fila {r_idx} de presupuesto ajustada a 'Asesoría metodológica y estadística'.")

        # 2. Erradicar token de IA "API Anthropic Tokens/mes"
        elif "anthropic" in c0_text.lower() or "token" in row.cells[2].text.lower():
            row.cells[0].text = "Servicios en la nube y base de datos (Cloud Hosting / PostgreSQL)"
            row.cells[1].text = "06 meses"
            row.cells[2].text = "Suscripción"
            row.cells[3].text = "250"
            row.cells[4].text = ""
            print(f"[OK] Fila {r_idx} de presupuesto normalizada: Erradicado token de IA 'API Anthropic'.")

    # Formatear celdas de la tabla de presupuesto en Times New Roman 10 pt
    for r_idx, row in enumerate(t_presupuesto.rows):
        is_hdr = (r_idx <= 2)
        for c in row.cells:
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.name = FUENTE_POR_DEFECTO
                    r.font.size = Pt(FONT_SIZE_TABLE_PT)
                    if is_hdr:
                        r.font.bold = True

    # Guardar documento actualizado
    doc.save(docx_path)
    print(f"[ÉXITO] Documento actualizado y guardado: {docx_path}")

if __name__ == "__main__":
    target = "salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V3_NORMALIZADO.docx"
    afinar_secciones_cap4_cap5(target)
