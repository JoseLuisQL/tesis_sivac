#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - AFINAMIENTO DE SECCIONES CRÍTICAS (CAPÍTULOS I Y II)
Alineación estricta con DEC-007 y estándar institucional UNAJMA
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
    aplicar_formato_nota_tabla_figura,
    FONT_SIZE_TABLE_PT
)

def afinar_documento(docx_path: str):
    # 0. Backup de seguridad
    backup_path = docx_path.replace('.docx', '_PRE_AFINAMIENTO.docx')
    shutil.copy2(docx_path, backup_path)
    print(f"[OK] Backup creado en: {backup_path}")

    doc = docx.Document(docx_path)

    # 1. Párrafo 87 (Justificación)
    p87_encontrado = False
    for i, p in enumerate(doc.paragraphs):
        if "Bajo esta perspectiva, la investigación tendrá un aporte organizacional" in p.text:
            p.text = (
                "Bajo esta perspectiva, la investigación tendrá un aporte organizacional y metodológico porque "
                "contribuirá a ordenar los flujos de control de inventario y distribución que actualmente dependen "
                "de procedimientos manuales o registros dispersos. En lugar de asumir reducciones temporales subjetivas "
                "o no parametrizadas, el estudio evaluará la oportunidad de procesamiento mediante indicadores métricos "
                "directamente observables y reproducibles. Específicamente, se cuantificarán el tiempo de registro de "
                "movimientos (Treg) y el tiempo de emisión de comprobantes de salida o vales (Tvale), comparados antes "
                "y después de la implementación de la solución tecnológica. De este modo, la investigación aportará "
                "datos empíricos objetivos sobre la reducción de la latencia en las operaciones de abastecimiento biológico."
            )
            aplicar_formato_cuerpo(p)
            print(f"[OK] Párrafo 87 (Justificación) actualizado en índice {i}.")
            p87_encontrado = True
            break
    assert p87_encontrado, "Error: No se encontró el párrafo 87 de Justificación."

    # 2. Sección 1.5 Delimitación
    h_idx = None
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip().startswith("1.5 Delimitación"):
            h_idx = i
            break
    assert h_idx is not None, "Error: No se encontró el encabezado 1.5 Delimitación."
    print(f"[OK] Encabezado 1.5 Delimitación localizado en índice {h_idx}.")

    p92 = doc.paragraphs[h_idx + 1]
    p93 = doc.paragraphs[h_idx + 2]
    p94 = doc.paragraphs[h_idx + 3]

    assert "CAPÍTULO II" in p94.text, f"Error: P94 no corresponde a Capítulo II (texto actual: '{p94.text}')"

    # Reemplazo de P92 (Introducción metodológica de delimitación)
    p92.text = (
        "La presente investigación se circunscribe metodológicamente a través de cuatro ejes canónicos "
        "del estándar institucional, asegurando la validez interna del diseño experimental y delimitando "
        "con precisión el alcance de los hallazgos."
    )
    aplicar_formato_cuerpo(p92)

    # Reemplazo de P93 (Delimitación espacial)
    p93.text = (
        "Delimitación espacial. El estudio se circunscribe al ámbito institucional y geográfico de la "
        "Dirección de Salud Apurímac II, ubicada en la provincia de Andahuaylas, departamento de Apurímac. "
        "De manera específica, las mediciones e intervenciones se focalizan en la Oficina de la Estrategia "
        "Sanitaria de Inmunizaciones y en la red de sus 11 centros de acopio zonales de biológicos. Dichos "
        "establecimientos albergan la infraestructura de cadena de frío responsable de la custodia, conservación "
        "y distribución de los biológicos hacia los establecimientos de salud del primer y segundo nivel de "
        "atención de la provincia."
    )
    aplicar_formato_cuerpo(p93)

    # Inserción de Delimitación temporal antes de P94
    p_temporal = p94.insert_paragraph_before(
        "Delimitación temporal. El horizonte cronológico de la investigación comprende el periodo entre "
        "los años 2024 y 2025. Este intervalo abarca la fase de diagnóstico basal y levantamiento de mediciones "
        "en la condición pretest, ejecutada durante el último trimestre del año 2024 bajo la modalidad tradicional "
        "de registros manuales y hojas de cálculo aisladas. Asimismo, comprende el posterior despliegue operativo "
        "e inducción técnica en el uso del sistema web SIVAC, culminando con la fase de evaluación experimental "
        "postest concluida en el año 2025."
    )
    aplicar_formato_cuerpo(p_temporal)

    # Inserción de Delimitación poblacional antes de P94
    p_poblacional = p94.insert_paragraph_before(
        "Delimitación poblacional. La unidad de análisis humano se delimita a una población censal finita "
        "integrada por la totalidad del personal involucrado en la cadena operativa de inmunizaciones de la "
        "institución (N = n = 14). Esta cobertura censal está conformada por tres profesionales del equipo "
        "técnico de la Estrategia Sanitaria de Inmunizaciones, encargados de la coordinación y supervisión "
        "central, y 11 servidores designados como responsables directos del manejo de cadena de frío y centros "
        "de acopio provinciales. Dada la magnitud acotada del universo, se analizó al censo completo sin "
        "recurrir a muestreo probabilístico, eliminando el error muestral."
    )
    aplicar_formato_cuerpo(p_poblacional)

    # Inserción de Delimitación temática antes de P94
    p_tematica = p94.insert_paragraph_before(
        "Delimitación temática. La investigación se encuadra disciplinariamente en el área de la Ingeniería "
        "de Sistemas aplicada a la logística sanitaria. En el plano temático, el estudio analiza la influencia "
        "del sistema web SIVAC sobre la gestión de movimientos de vacunas. Dicha solución tecnológica se "
        "desarrolló mediante la metodología ágil Extreme Programming y se evaluó bajo el estándar ISO/IEC 25010:2023. "
        "La variable dependiente se restringe rigurosamente a tres dimensiones canónicas. La primera corresponde "
        "a la oportunidad de procesamiento, evaluada a través del tiempo de registro de movimientos (Treg) "
        "y el tiempo de emisión de comprobantes de salida o vales (Tvale). Asimismo, se analiza la consistencia "
        "documental, calculada mediante los registros sin discrepancias (RSD) y la concordancia programada "
        "versus entregada (CPE). Finalmente, la satisfacción del usuario se determina con base en la aceptación "
        "del proceso operativo (AP) y la utilidad percibida sanitaria (UP) bajo el Modelo de Aceptación Tecnológica."
    )
    aplicar_formato_cuerpo(p_tematica)
    print("[OK] Sección 1.5 Delimitación reestructurada formalmente con los 4 ejes canónicos UNAJMA.")

    # 3. Párrafo 202 y P200 (2.2.20 Oportunidad de procesamiento)
    p200_act = False
    p202_act = False
    for p in doc.paragraphs:
        if "Este resultado sustenta la pertinencia de medir tiempos de registro y reporte." in p.text:
            p.text = (
                "Duong et al. (2021) reportaron que 725 de 767 usuarios finales indicaron que el sistema NIIS "
                "les ayudaba a gestionar y reportar datos de inmunización y a ahorrar tiempo. Este resultado "
                "sustenta la pertinencia de evaluar cronométricamente los tiempos dedicados al registro de biológicos "
                "y a la emisión de comprobantes de movimiento."
            )
            aplicar_formato_cuerpo(p)
            p200_act = True
        elif "El tiempo de registro y el tiempo de reporte son expresiones concretas" in p.text:
            p.text = (
                "El tiempo de registro de movimientos y el tiempo de emisión de comprobantes de salida o vales "
                "constituyen las expresiones operativas de la oportunidad de procesamiento. Estos indicadores "
                "cuantifican el intervalo cronometrado que demanda la gestión operativa desde la captura inicial "
                "de los datos de los biológicos hasta la formalización del balance en kardex y la expedición del "
                "documento oficial de entrega. Al parametrizar ambos momentos críticos, la dimensión permite "
                "evaluar con exactitud la reducción de la latencia temporal atribuible a la automatización del flujo "
                "de trabajo. De esta manera, se descartan aproximaciones subjetivas y se garantiza un contraste "
                "empírico reproducible entre las condiciones de pretest y postest."
            )
            aplicar_formato_cuerpo(p)
            p202_act = True

    assert p202_act, "Error: No se encontró el párrafo 202 de Oportunidad de procesamiento."
    print(f"[OK] Párrafo 202 (Oportunidad de procesamiento) armonizado con DEC-007 (P200 complementario: {p200_act}).")

    # 4. Tabla 3 (Indicadores de la satisfacción del usuario)
    t3 = doc.tables[2]
    # Configurar fila 1
    t3.cell(1, 0).text = "Satisfacción del usuario"
    t3.cell(1, 1).text = "Aceptación del proceso operativo (AP)"
    t3.cell(1, 2).text = "Escala Likert (1-5; 4 ítems, 4 a 20 pts)"

    # Configurar fila 2
    t3.cell(2, 0).text = "Satisfacción del usuario"
    t3.cell(2, 1).text = "Utilidad percibida sanitaria (UP)"
    t3.cell(2, 2).text = "Escala Likert (1-5; 4 ítems, 4 a 20 pts)"

    # Estilizar runs de celdas
    for r_i, row in enumerate(t3.rows):
        is_hdr = (r_i == 0)
        for c_i, cell in enumerate(row.cells):
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(FONT_SIZE_TABLE_PT)
                    if is_hdr:
                        r.font.bold = True

    # Actualizar nota de Tabla 3
    t3_nota_act = False
    for p in doc.paragraphs:
        if p.text.strip().startswith("Nota.") and "dimensión satisfacción del usuario" in p.text:
            p.text = (
                "Nota. Adaptado de la matriz de operacionalización de variables de la investigación, "
                "fundamentado en el Technology Acceptance Model (TAM; Davis, 1989; Ndlovu et al., 2021) "
                "y el estándar internacional ISO/IEC 25010:2023. Cada indicador se evalúa mediante cuatro "
                "reactivos tipo Likert de 5 puntos (1 = Totalmente en desacuerdo a 5 = Totalmente de acuerdo), "
                "generando una puntuación acumulada de 4 a 20 puntos por indicador y una escala global "
                "de 8 a 40 puntos para la dimensión."
            )
            aplicar_formato_nota_tabla_figura(p)
            t3_nota_act = True
            break
    assert t3_nota_act, "Error: No se encontró la nota de Tabla 3."
    print("[OK] Tabla 3 y nota formal actualizadas conforme a DEC-007.")

    # 5. Eliminación del párrafo residual huérfano con solo un punto (".") en sección 2.2.23 (antes de 2.2.24)
    puntos_removidos = 0
    for p in list(doc.paragraphs):
        if p.text.strip() == ".":
            parent = p._element.getparent()
            if parent is not None:
                parent.remove(p._element)
                puntos_removidos += 1
    print(f"[OK] Párrafo residual huérfano con punto ('.') eliminado limpiamente ({puntos_removidos} nodo/s removido/s).")

    # Guardar documento
    doc.save(docx_path)
    print(f"[ÉXITO] Documento actualizado y guardado: {docx_path}")

if __name__ == "__main__":
    target = "salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V3_NORMALIZADO.docx"
    afinar_documento(target)
