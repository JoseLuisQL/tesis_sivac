#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - ENSAMBLADOR DE CAPÍTULO V: RESULTADOS (.DOCX)
Universidad Nacional José María Arguedas (UNAJMA)
Facultad de Ingeniería - Escuela Profesional de Ingeniería de Sistemas

Alineación 1:1 con el Informe Final EPIS-UNAJMA (Modelo Jhon 2026, pp. 99–111):
- Inicio directo en 5.1. Análisis descriptivo (cero párrafo introductorio meta-explicativo)
- Subsecciones 5.1.1, 5.1.2, 5.1.3 y 5.2 (5.2.1 y 5.2.2 con 5.2.2.1 a 5.2.2.4)
- Numeración global continua de tablas: Tablas 13, 14, 15, 16 y 17 (SEQ Tabla)
- Cuadro complementario de unidades de observación y agregación sin campo SEQ Tabla
- Cero invención de datos de campo: marcadores formales [Pendiente]
- Cero signos de dólar, cero fórmulas crudas y cero guion largo
================================================================================
"""

import os
import sys
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utilidades')))

from docx_utilidades import (
    agregar_titulo_1, agregar_titulo_2, agregar_titulo_3, agregar_titulo_4,
    agregar_parrafo, agregar_item_lista, agregar_tabla_datos,
    formatear_tabla_apa7, procesar_formato_texto
)
from docx_quirurgico import configurar_geometria_tabla


SUJETOS_CENTROS_UNIFICADOS = [
    ("OP-01", "Almacén Especializado DISA Apurímac II - Sede Central"),
    ("OP-02", "Almacén Especializado DISA Apurímac II - Sede Central"),
    ("OP-03", "Almacén Especializado DISA Apurímac II - Sede Central"),
    ("OP-04", "Almacén Especializado DISA Apurímac II - Sede Central"),
    ("OP-05", "Centro de Acopio Andahuaylas"),
    ("OP-06", "Centro de Acopio Andahuaylas"),
    ("OP-07", "Centro de Acopio Talavera"),
    ("OP-08", "Centro de Acopio Talavera"),
    ("OP-09", "Centro de Acopio San Jerónimo"),
    ("OP-10", "Centro de Acopio San Jerónimo"),
    ("OP-11", "Centro de Acopio Santa María de Chicmo"),
    ("OP-12", "Centro de Acopio Huancarama"),
    ("OP-13", "Centro de Acopio Chincheros"),
    ("OP-14", "Centro de Acopio Uripa/Ocobamba")
]


def agregar_cuadro_complementario(doc, titulo_texto, encabezados, filas, nota_texto=None, col_widths=None, font_size_pt=9.0):
    """Inserta un cuadro complementario formateado en APA 7 sin campo SEQ Tabla."""
    p_tit = doc.add_paragraph()
    p_tit.paragraph_format.keep_with_next = True
    p_tit.paragraph_format.space_before = Pt(12)
    p_tit.paragraph_format.space_after = Pt(4)
    p_tit.paragraph_format.line_spacing = 1.0
    p_tit.paragraph_format.first_line_indent = Inches(0)

    partes_tit = procesar_formato_texto(titulo_texto)
    for r_texto, r_bold, r_italic in partes_tit:
        run_t = p_tit.add_run(r_texto)
        run_t.font.name = 'Times New Roman'
        run_t.font.size = Pt(10)
        run_t.font.bold = True or r_bold
        run_t.font.italic = r_italic

    tbl = doc.add_table(rows=len(filas) + 1, cols=len(encabezados))
    for c_idx, h_text in enumerate(encabezados):
        cell = tbl.rows[0].cells[c_idx]
        p = cell.paragraphs[0]
        p.text = ""
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r_texto, r_bold, r_italic in procesar_formato_texto(h_text):
            r = p.add_run(r_texto)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(font_size_pt)
            r.font.bold = True
            r.font.italic = r_italic

    for r_idx, fila in enumerate(filas):
        for c_idx, val in enumerate(fila):
            cell = tbl.rows[r_idx + 1].cells[c_idx]
            p = cell.paragraphs[0]
            p.text = ""
            for r_texto, r_bold, r_italic in procesar_formato_texto(val):
                r = p.add_run(r_texto)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(font_size_pt)
                r.font.bold = r_bold
                r.font.italic = r_italic

    formatear_tabla_apa7(tbl, col_widths=col_widths, font_size_pt=font_size_pt)

    if nota_texto:
        p_not = doc.add_paragraph()
        p_not.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_not.paragraph_format.space_before = Pt(4)
        p_not.paragraph_format.space_after = Pt(12)
        p_not.paragraph_format.line_spacing = 1.0
        p_not.paragraph_format.first_line_indent = Inches(0)
        run_lbl = p_not.add_run("Nota. ")
        run_lbl.font.name = 'Times New Roman'
        run_lbl.font.size = Pt(9.5)
        run_lbl.font.italic = True
        for r_texto, r_bold, r_italic in procesar_formato_texto(nota_texto):
            r = p_not.add_run(r_texto)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            r.font.bold = r_bold
            r.font.italic = r_italic


def construir_capitulo5(doc):
    agregar_titulo_1(doc, "CAPÍTULO V: RESULTADOS")

    # ==========================================================================
    # 5.1. Análisis descriptivo
    # ==========================================================================
    agregar_titulo_2(doc, "5.1. Análisis descriptivo")
    agregar_parrafo(
        doc,
        "El análisis descriptivo tuvo como propósito caracterizar el comportamiento empírico de las tres dimensiones "
        "oficiales de la gestión de movimientos de vacunas (oportunidad de procesamiento, consistencia documental y "
        "satisfacción del usuario) en las condiciones basales del pre-test bajo gestión manual frente a las condiciones "
        "del post-test bajo la operación del sistema web SIVAC. Conforme a las pautas metodológicas fijadas en el Capítulo IV, "
        "las unidades primarias observadas en campo fueron agregadas por operador para estructurar pares válidos (O₁ᵢ, O₂ᵢ) "
        "sobre la población censal de 14 trabajadores de la Dirección de Salud Apurímac II. En el cuadro siguiente se "
        "especifica por cada uno de los seis indicadores la unidad observada, el número de operaciones o expedientes en "
        "pre-test y post-test, el n efectivo de operadores pareados y la regla de agregación pareada.",
        sangria=True
    )

    headers_descriptivo_resumen = [
        "Dimensión e Indicador",
        "Unidad Observada",
        "Operaciones / Expedientes (Pre-test / Post-test)",
        "n Efectivo (Operadores Pareados)",
        "Regla de Agregación Pareada"
    ]
    filas_descriptivo_resumen = [
        [
            "Dimensión 1:\nTiempo de registro (T_reg)",
            "Operaciones individuales de registro de lote",
            "[Pendiente] / [Pendiente]",
            "N = 14 (operadores censales)",
            "Promedio aritmético en minutos de las k operaciones del operador i en cada periodo."
        ],
        [
            "Dimensión 1:\nTiempo de emisión de vale (T_vale)",
            "Confección y emisión de comprobantes de salida",
            "[Pendiente] / [Pendiente]",
            "n válido ([Pendiente])",
            "Promedio aritmético en minutos de los m vales emitidos por el operador i en cada periodo."
        ],
        [
            "Dimensión 2:\nRegistros sin discrepancias (RSD)",
            "Asientos y expedientes de kardex auditados",
            "[Pendiente] / [Pendiente]",
            "N = 14 (operadores censales)",
            "Porcentaje de registros conformes (8 criterios normativos) sobre el total auditado al operador i."
        ],
        [
            "Dimensión 2:\nConcordancia programada vs. entregada (CPE)",
            "Despachos de vacunas auditados y conciliados",
            "[Pendiente] / [Pendiente]",
            "N = 14 (operadores censales)",
            "Porcentaje de despachos concordantes (Q_entregada = Q_programada) sobre el total del operador i."
        ],
        [
            "Dimensión 3:\nAceptación del proceso (AP)",
            "Cuestionarios psicométricos, reactivos AP-01 a AP-04 (Modalidad A)",
            "[Pendiente] / [Pendiente]",
            "N = 14 (operadores censales)",
            "Puntaje sumativo directo obtenido por el operador i en la subescala de aceptación del proceso operativo (4–20 puntos)."
        ],
        [
            "Dimensión 3:\nUtilidad percibida (UP)",
            "Cuestionarios psicométricos, reactivos UP-01 a UP-04 (Modalidad A)",
            "[Pendiente] / [Pendiente]",
            "N = 14 (operadores censales)",
            "Puntaje sumativo directo obtenido por el operador i en la subescala de utilidad percibida para la gestión (4–20 puntos)."
        ]
    ]
    agregar_cuadro_complementario(
        doc,
        titulo_texto="Estructura de unidad observada, operaciones auditadas, n efectivo y regla de agregación pareada por indicador",
        encabezados=headers_descriptivo_resumen,
        filas=filas_descriptivo_resumen,
        nota_texto="Síntesis de la recolección en campo en ventanas simétricas de 30 días calendario en el pre-test y post-test. Los valores [Pendiente] se integran a partir del levantamiento de datos empíricos de campo.",
        col_widths=[Inches(1.30), Inches(1.15), Inches(1.00), Inches(0.95), Inches(1.70)],
        font_size_pt=10
    )

    agregar_parrafo(
        doc,
        "La presentación de los resultados descriptivos se complementa, una vez ingresados los datos de campo reales, "
        "con la incorporación de gráficos estadísticos pre-test vs. post-test de alta resolución (300 DPI): (a) diagramas "
        "de cajas pareados (boxplots) para los indicadores de tiempos de registro y emisión de vales; (b) gráficos de barras "
        "para los indicadores porcentuales de consistencia documental; y (c) gráficos de barras agrupadas para los "
        "indicadores de aceptación del proceso y utilidad percibida de la Modalidad A del Instrumento N.° 03.",
        sangria=True
    )

    # --------------------------------------------------------------------------
    # 5.1.1. Dimensión 1: Oportunidad de procesamiento
    # --------------------------------------------------------------------------
    agregar_titulo_3(doc, "5.1.1. Dimensión 1: Oportunidad de procesamiento")
    agregar_parrafo(
        doc,
        "El análisis descriptivo de la primera dimensión evaluó el comportamiento temporal de las operaciones "
        "logísticas en los ocho centros de acopio de la Dirección de Salud Apurímac II a través de dos indicadores "
        "cuantitativos expresados en minutos: el tiempo de registro de movimiento de vacunas y el tiempo de emisión "
        "de comprobante de salida o vale pecosa. Las mediciones se efectuaron mediante observación directa cronometrada con "
        "el Instrumento N.° 01 sobre los catorce operadores que conformaron la población censal, contrastando el "
        "desempeño del procedimiento manual tradicional en el pre-test frente al flujo automatizado con el sistema "
        "web SIVAC en el post-test. En la Tabla 13 se presenta la distribución individual por operador y centro de "
        "acopio, junto con los estadísticos de tendencia central y dispersión.",
        sangria=True
    )

    headers_t13 = [
        "Operador",
        "Centro de Acopio",
        "Tiempo de Registro Pre-test (min)",
        "Tiempo de Registro Post-test (min)",
        "Tiempo de Emisión de Vale Pre-test (min)",
        "Tiempo de Emisión de Vale Post-test (min)"
    ]
    filas_t13 = []
    for cod_sujeto, nom_centro in SUJETOS_CENTROS_UNIFICADOS:
        filas_t13.append([
            cod_sujeto,
            nom_centro,
            "[Pendiente]",
            "[Pendiente]",
            "[Pendiente]",
            "[Pendiente]"
        ])
    filas_t13.extend([
        ["**Media**", "**Promedio aritmético censal**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**DE**", "**Desviación estándar muestral**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Mediana**", "**Percentil 50 de la distribución**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Mínimo**", "**Valor mínimo observado**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Máximo**", "**Valor máximo observado**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**n efectivo**", "**n efectivo (operadores pareados)**", "**14**", "**14**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Unidades primarias**", "**Unidades primarias auditadas (operaciones/registros)**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"]
    ])

    agregar_tabla_datos(
        doc,
        numero="13",
        titulo="Comparación descriptiva de los tiempos de registro y emisión de vales de salida entre el pre-test y post-test",
        encabezados=headers_t13,
        filas=filas_t13,
        nota="Tiempos medidos en minutos mediante el Instrumento N.° 01 sobre la población censal de 14 operadores de la DISA Apurímac II. El n efectivo en emisión de vales se delimita a los operadores con despachos en ambas ventanas. Valores [Pendiente] reservados para el vaciado de datos reales de campo.",
        col_widths=[Inches(0.75), Inches(1.35), Inches(1.00), Inches(1.00), Inches(1.00), Inches(1.00)],
        font_size_pt=10
    )

    agregar_parrafo(
        doc,
        "La estructura tabulada en la Tabla 13 permite cuantificar la reducción absoluta y relativa de los tiempos "
        "operativos tras la sustitución del llenado manuscrito de libros de kardex y talonarios físicos por el "
        "registro transaccional con validación automática de lotes y generación inmediata de comprobantes en formato "
        "electrónico dentro del sistema web SIVAC.",
        sangria=True
    )

    # --------------------------------------------------------------------------
    # 5.1.2. Dimensión 2: Consistencia documental
    # --------------------------------------------------------------------------
    agregar_titulo_3(doc, "5.1.2. Dimensión 2: Consistencia documental")
    agregar_parrafo(
        doc,
        "La segunda dimensión analizó el grado de exactitud contable y trazabilidad de los expedientes de "
        "inmunizaciones mediante dos indicadores expresados en escala porcentual: el porcentaje de registros sin "
        "discrepancias y la concordancia de cantidad programada versus entregada. Los datos fueron recabados aplicando "
        "el Instrumento N.° 02 (Guía de cotejo de consistencia documental) sobre ventanas simétricas de treinta días "
        "calendario en el pre-test y post-test, verificando el cumplimiento simultáneo de los ocho criterios normativos "
        "de conformidad de la NTS N.° 196-MINSA/DGIESP-2022 (nombre del biológico, número de lote, fecha de vencimiento, "
        "cantidad física, procedencia o destino, identificación del operador, saldo aritmético de kardex y correlatividad "
        "temporal). Los resultados descriptivos se consolidan en la Tabla 14.",
        sangria=True
    )

    headers_t14 = [
        "Operador",
        "Centro de Acopio",
        "Registros sin Discrepancias Pre-test (%)",
        "Registros sin Discrepancias Post-test (%)",
        "Concordancia de Cantidades Pre-test (%)",
        "Concordancia de Cantidades Post-test (%)"
    ]
    filas_t14 = []
    for cod_sujeto, nom_centro in SUJETOS_CENTROS_UNIFICADOS:
        filas_t14.append([
            cod_sujeto,
            nom_centro,
            "[Pendiente]",
            "[Pendiente]",
            "[Pendiente]",
            "[Pendiente]"
        ])
    filas_t14.extend([
        ["**Media**", "**Promedio aritmético censal**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**DE**", "**Desviación estándar muestral**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Mediana**", "**Percentil 50 de la distribución**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Mínimo**", "**Valor mínimo observado**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Máximo**", "**Valor máximo observado**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**n efectivo**", "**n efectivo (operadores pareados)**", "**14**", "**14**", "**14**", "**14**"],
        ["**Unidades primarias**", "**Unidades primarias auditadas (operaciones/registros)**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"]
    ])

    agregar_tabla_datos(
        doc,
        numero="14",
        titulo="Comparación descriptiva del porcentaje de registros sin discrepancias y concordancia de cantidades entre el pre-test y post-test",
        encabezados=headers_t14,
        filas=filas_t14,
        nota="Proporciones obtenidas mediante auditoría documental con el Instrumento N.° 02 en los 8 centros de acopio de la DISA Apurímac II (n = 14). Los valores [Pendiente] se completan con los datos auditados en campo.",
        col_widths=[Inches(0.75), Inches(1.35), Inches(1.00), Inches(1.00), Inches(1.00), Inches(1.00)],
        font_size_pt=10
    )

    agregar_parrafo(
        doc,
        "Los valores consolidados en la Tabla 14 reflejan el impacto de las reglas de integridad referencial, el "
        "bloqueo preventivo de despachos con existencias insuficientes y el ordenamiento automático por fecha de "
        "expiración bajo la regla FEFO implementados en la base de datos relacional del sistema web SIVAC para erradicar "
        "los errores de arrastre aritmético y discrepancia de inventario.",
        sangria=True
    )

    # --------------------------------------------------------------------------
    # 5.1.3. Dimensión 3: Satisfacción del usuario
    # --------------------------------------------------------------------------
    agregar_titulo_3(doc, "5.1.3. Dimensión 3: Satisfacción del usuario")
    agregar_parrafo(
        doc,
        "El análisis descriptivo de la tercera dimensión examinó la percepción de los catorce operadores de la cadena "
        "de inmunizaciones respecto a la gestión logística mediante dos indicadores de la Modalidad A del Instrumento "
        "N.° 03, sustentados en el Modelo de Aceptación Tecnológica (Davis, 1989): la aceptación del proceso operativo "
        "(reactivos AP-01 a AP-04) y la utilidad percibida para la gestión (reactivos UP-01 a UP-04). La medición se "
        "realizó en escala ordinal Likert de cinco niveles, estructurando puntajes sumativos por indicador (rango de 4 a "
        "20 puntos) y un puntaje global de dimensión sobre los 8 ítems de la Modalidad A (rango de 8 a 40 puntos). En la "
        "Tabla 15 se exponen los puntajes sumativos registrados en el pre-test y post-test.",
        sangria=True
    )

    headers_t15 = [
        "Operador",
        "Centro de Acopio",
        "Aceptación del Proceso Pre-test (4-20)",
        "Aceptación del Proceso Post-test (4-20)",
        "Utilidad Percibida Pre-test (4-20)",
        "Utilidad Percibida Post-test (4-20)"
    ]
    filas_t15 = []
    for cod_sujeto, nom_centro in SUJETOS_CENTROS_UNIFICADOS:
        filas_t15.append([
            cod_sujeto,
            nom_centro,
            "[Pendiente]",
            "[Pendiente]",
            "[Pendiente]",
            "[Pendiente]"
        ])
    filas_t15.extend([
        ["**Media**", "**Promedio aritmético censal**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**DE**", "**Desviación estándar muestral**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Mediana**", "**Percentil 50 de la distribución**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Mínimo**", "**Valor mínimo observado**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Máximo**", "**Valor máximo observado**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**n efectivo**", "**n efectivo (operadores pareados)**", "**14**", "**14**", "**14**", "**14**"],
        ["**Unidades primarias**", "**Unidades primarias auditadas (operaciones/registros)**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"]
    ])

    agregar_tabla_datos(
        doc,
        numero="15",
        titulo="Comparación descriptiva de la aceptación del proceso y utilidad percibida entre el pre-test y post-test",
        encabezados=headers_t15,
        filas=filas_t15,
        nota="Puntuaciones sumativas directas obtenidas mediante la Modalidad A del Instrumento N.° 03, compuesta por 8 ítems (AP-01 a AP-04 y UP-01 a UP-04), sobre la población censal de la DISA Apurímac II (n = 14). Consistencia interna por indicador y del global de la Modalidad A: Alfa de Cronbach de Aceptación del proceso (α_AP = [Pendiente]), de Utilidad percibida (α_UP = [Pendiente]) y del conjunto de los 8 ítems de la Modalidad A (α_MA = [Pendiente]). La Modalidad B del instrumento no forma parte de esta tabla. Valores [Pendiente] reservados para el vaciado de datos de campo.",
        col_widths=[Inches(0.75), Inches(1.35), Inches(1.00), Inches(1.00), Inches(1.00), Inches(1.00)],
        font_size_pt=10
    )

    agregar_parrafo(
        doc,
        "La comparación presentada en la Tabla 15 permite evaluar la evolución de la conformidad del personal técnico "
        "y administrativo frente a la fluidez del flujo de trabajo, la adaptabilidad procedimental y la eficacia del "
        "control de biológicos alcanzada con la plataforma web frente a la carga cognitiva del procedimiento manual previo.",
        sangria=True
    )

    # ==========================================================================
    # 5.2. Análisis inferencial
    # ==========================================================================
    agregar_titulo_2(doc, "5.2. Análisis inferencial")

    # --------------------------------------------------------------------------
    # 5.2.1. Prueba de normalidad
    # --------------------------------------------------------------------------
    agregar_titulo_3(doc, "5.2.1. Prueba de normalidad")
    agregar_parrafo(
        doc,
        "Con el propósito de seleccionar el estadístico idóneo para la contrastación de las hipótesis y considerando "
        "que el tamaño de la población censal fue de catorce operadores (n = 14, inferior a cincuenta unidades de "
        "análisis), se aplicó la prueba de bondad de ajuste de Shapiro-Wilk sobre las diferencias intrasujeto "
        "(post-test menos pre-test, di = O2i - O1i) de cada uno de los seis indicadores evaluados. Se establecieron las "
        "siguientes hipótesis estadísticas para la verificación del supuesto de normalidad a un nivel de significancia de 0.05:",
        sangria=True
    )
    agregar_item_lista(
        doc,
        "**Hipótesis nula de normalidad (H0):** Las diferencias pareadas entre el post-test y el pre-test siguen una "
        "distribución normal (valor de probabilidad p > 0.05).",
        simbolo="•"
    )
    agregar_item_lista(
        doc,
        "**Hipótesis alterna de normalidad (H1):** Las diferencias pareadas entre el post-test y el pre-test no siguen una "
        "distribución normal (valor de probabilidad p <= 0.05).",
        simbolo="•"
    )

    headers_t16 = [
        "Dimensión",
        "Indicador Evaluado",
        "Estadístico Shapiro-Wilk (W)",
        "Grados de Libertad (gl)",
        "Significancia (p-valor)",
        "Prueba Inferencial Seleccionada"
    ]
    filas_t16 = [
        [
            "1. Oportunidad de procesamiento",
            "Tiempo de registro de movimiento de vacunas",
            "[Pendiente]",
            "14",
            "[Pendiente]",
            "Wilcoxon pareado / t de Student"
        ],
        [
            "1. Oportunidad de procesamiento",
            "Tiempo de emisión de comprobante de salida o vale",
            "[Pendiente]",
            "[Pendiente]",
            "[Pendiente]",
            "Wilcoxon pareado / t de Student"
        ],
        [
            "2. Consistencia documental",
            "Porcentaje de registros sin discrepancias",
            "[Pendiente]",
            "14",
            "[Pendiente]",
            "Wilcoxon pareado / t de Student"
        ],
        [
            "2. Consistencia documental",
            "Concordancia de cantidad programada versus entregada",
            "[Pendiente]",
            "14",
            "[Pendiente]",
            "Wilcoxon pareado / t de Student"
        ],
        [
            "3. Satisfacción del usuario",
            "Aceptación del proceso",
            "[Pendiente]",
            "14",
            "[Pendiente]",
            "Wilcoxon pareado / t de Student"
        ],
        [
            "3. Satisfacción del usuario",
            "Utilidad percibida",
            "[Pendiente]",
            "14",
            "[Pendiente]",
            "Wilcoxon pareado / t de Student"
        ]
    ]

    agregar_tabla_datos(
        doc,
        numero="16",
        titulo="Resultados de la prueba de normalidad de Shapiro-Wilk para los indicadores de la gestión de movimientos de vacunas",
        encabezados=headers_t16,
        filas=filas_t16,
        nota="Prueba de Shapiro-Wilk evaluada con nivel de significancia de 0.05 sobre las diferencias pareadas intrasujeto. Si el p-valor supera 0.05 se emplea la prueba t de Student pareada; en caso contrario se aplica la prueba de rangos con signo de Wilcoxon.",
        col_widths=[Inches(1.23), Inches(1.53), Inches(0.88), Inches(0.64), Inches(0.79), Inches(1.03)],
        font_size_pt=9.0
    )

    # --------------------------------------------------------------------------
    # 5.2.2. Contrastación de hipótesis
    # --------------------------------------------------------------------------
    agregar_titulo_3(doc, "5.2.2. Contrastación de hipótesis")
    agregar_parrafo(
        doc,
        "Una vez verificado el comportamiento distribucional de las diferencias pareadas, se procedió a la "
        "contrastación estadística formal de la hipótesis general y de las tres hipótesis específicas formuladas en "
        "la investigación, adoptando un nivel de significancia bilateral nominal de 0.05 (confianza del 95%) y aplicando "
        "la corrección secuencial de Holm-Bonferroni para controlar la tasa de error familiar tipo I por múltiples comparaciones.",
        sangria=True
    )

    # 5.2.2.1. Contrastación de la hipótesis general
    agregar_titulo_4(doc, "5.2.2.1. Contrastación de la hipótesis general")
    agregar_item_lista(
        doc,
        "**Hipótesis nula (H0):** La aplicación del sistema web SIVAC no mejora significativamente la gestión de "
        "movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.",
        simbolo="•"
    )
    agregar_item_lista(
        doc,
        "**Hipótesis alterna (H1):** La aplicación del sistema web SIVAC mejora significativamente la gestión de "
        "movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.",
        simbolo="•"
    )
    agregar_parrafo(
        doc,
        "La contrastación de la Hipótesis General abordó la gestión de movimientos de vacunas como un constructo "
        "multidimensional integral. Debido a que las tres dimensiones componentes fueron medidas en escalas heterogéneas "
        "(minutos cronometrados en oportunidad, porcentajes en consistencia documental y puntajes ordinales en satisfacción), "
        "la decisión estadística formal no se sustentó en un promedio simple ni en un p-valor artificialmente unificado, "
        "sino en una regla de decisión conjuntiva multivariada: la hipótesis nula general (H0) se rechaza si y solo si se "
        "rechazan simultáneamente las hipótesis nulas de las tres hipótesis específicas (HE1, HE2 y HE3) a un nivel de "
        "significancia bilateral ajustado de p < 0.05 en sus respectivos indicadores mediante Wilcoxon o t de Student.",
        sangria=True
    )

    # 5.2.2.2. Contrastación de la hipótesis específica 1: Oportunidad de procesamiento
    agregar_titulo_4(doc, "5.2.2.2. Contrastación de la hipótesis específica 1: Oportunidad de procesamiento")
    agregar_item_lista(
        doc,
        "**Hipótesis nula (H0,1):** La aplicación del sistema web SIVAC no mejora significativamente la oportunidad "
        "de procesamiento en los movimientos de vacunas del personal de inmunizaciones de la Dirección de Salud "
        "Apurímac II.",
        simbolo="•"
    )
    agregar_item_lista(
        doc,
        "**Hipótesis alterna (H1,1):** La aplicación del sistema web SIVAC mejora significativamente la oportunidad "
        "de procesamiento en los movimientos de vacunas del personal de inmunizaciones de la Dirección de Salud "
        "Apurímac II, reduciendo los tiempos de registro y de emisión de comprobantes de salida.",
        simbolo="•"
    )
    agregar_parrafo(
        doc,
        "El contraste inferencial evaluó si las mediciones pareadas del post-test en los indicadores de tiempo de registro "
        "(T_reg) y tiempo de emisión de vale (T_vale) presentaron una disminución estadísticamente significativa respecto a "
        "la línea base del pre-test bajo significancia bilateral p < 0.05 con ajuste de Holm-Bonferroni.",
        sangria=True
    )

    # 5.2.2.3. Contrastación de la hipótesis específica 2: Consistencia documental
    agregar_titulo_4(doc, "5.2.2.3. Contrastación de la hipótesis específica 2: Consistencia documental")
    agregar_item_lista(
        doc,
        "**Hipótesis nula (H0,2):** La aplicación del sistema web SIVAC no mejora significativamente la consistencia "
        "documental de los registros de movimientos de vacunas en el personal de inmunizaciones de la Dirección de "
        "Salud Apurímac II.",
        simbolo="•"
    )
    agregar_item_lista(
        doc,
        "**Hipótesis alterna (H1,2):** La aplicación del sistema web SIVAC mejora significativamente la consistencia "
        "documental de los registros de movimientos de vacunas en el personal de inmunizaciones de la Dirección de "
        "Salud Apurímac II, incrementando el porcentaje de registros sin discrepancias y la concordancia de "
        "cantidades programadas versus entregadas.",
        simbolo="•"
    )
    agregar_parrafo(
        doc,
        "La prueba de hipótesis verificó si las proporciones auditadas en el post-test en registros sin discrepancias (RSD) "
        "y concordancia programada versus entregada (CPE) superaron significativamente los niveles basales de la gestión "
        "manual tradicional en el pre-test.",
        sangria=True
    )

    # 5.2.2.4. Contrastación de la hipótesis específica 3: Satisfacción del usuario
    agregar_titulo_4(doc, "5.2.2.4. Contrastación de la hipótesis específica 3: Satisfacción del usuario")
    agregar_item_lista(
        doc,
        "**Hipótesis nula (H0,3):** La aplicación del sistema web SIVAC no mejora significativamente la satisfacción "
        "del usuario respecto a la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección "
        "de Salud Apurímac II.",
        simbolo="•"
    )
    agregar_item_lista(
        doc,
        "**Hipótesis alterna (H1,3):** La aplicación del sistema web SIVAC mejora significativamente la satisfacción "
        "del usuario respecto a la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección "
        "de Salud Apurímac II, elevando la aceptación del proceso y la utilidad percibida.",
        simbolo="•"
    )
    agregar_parrafo(
        doc,
        "El contraste estadístico determinó si las puntuaciones psicométricas pareadas obtenidas con la Modalidad A del "
        "Instrumento N.° 03 en los indicadores de aceptación del proceso (AP) y utilidad percibida (UP) evidenciaron un incremento significativo "
        "en el post-test. En la Tabla 17 se presenta el consolidado de la contrastación inferencial: para la Hipótesis General "
        "(HG) se establece la integración inferencial conjunta de H1, H2 y H3 bajo evaluación multidimensional, mientras que "
        "para cada uno de los seis indicadores de H1, H2 y H3 se reporta explícitamente el n válido, el estadístico de prueba "
        "(W / Z o t), el p-valor bilateral (ajustado por Holm-Bonferroni), el tamaño del efecto (r = |Z|/√N_válidos o d de Cohen) "
        "y la decisión estadística.",
        sangria=True
    )

    headers_t17 = [
        "Hipótesis Contrastada",
        "Prueba / Indicadores Evaluados",
        "n Válido",
        "Estadístico (W / Z o t)",
        "p-valor Bilateral (Holm-Bonferroni)",
        "Tamaño del Efecto (r o d)",
        "Decisión Estadística (α = 0.05)"
    ]
    filas_t17 = [
        [
            "Hipótesis General (HG):\nGestión de movimientos de vacunas",
            "Integración inferencial conjunta de H1, H2 y H3 (Evaluación multidimensional)",
            "14",
            "Criterio conjuntivo",
            "p_adj < 0.05 simultáneo",
            "Multidimensional",
            "[Pendiente]"
        ],
        [
            "Hipótesis Específica 1 (H1):\nOportunidad de procesamiento",
            "Tiempo de registro de vacunas (T_reg)\n\nTiempo de emisión de vales (T_vale)",
            "14\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]"
        ],
        [
            "Hipótesis Específica 2 (H2):\nConsistencia documental",
            "Registros sin discrepancias (RSD)\n\nConcordancia programada vs. entregada (CPE)",
            "14\n\n14",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]"
        ],
        [
            "Hipótesis Específica 3 (H3):\nSatisfacción del usuario",
            "Aceptación del proceso (AP)\n\nUtilidad percibida (UP)",
            "14\n\n14",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]"
        ]
    ]

    tbl_t17 = agregar_tabla_datos(
        doc,
        numero="17",
        titulo="Consolidado de la contrastación inferencial de las hipótesis general y específicas mediante pruebas para muestras relacionadas",
        encabezados=headers_t17,
        filas=filas_t17,
        nota="Contrastes inferenciales pre-test versus post-test evaluados en la población censal de la DISA Apurímac II a un nivel de significancia bilateral de 0.05. Para cada uno de los 6 indicadores de H1, H2 y H3 se reporta el n válido, el estadístico (W / Z o t), el p-valor bilateral (ajustado por Holm-Bonferroni), el tamaño del efecto (r = |Z|/√N_válidos según Rosenthal, 1991, o d de Cohen) y la decisión estadística ([Pendiente]).",
        col_widths=[1340, 1593, 939, 1095, 1105, 1617, 1095],
        font_size_pt=10
    )
    # Las siete columnas contienen palabras no fragmentables de hasta 1,424 dxa
    # ("Multidimensional"). Los 8,784 dxa útiles solo se cubren reduciendo los márgenes
    # celulares a 50 dxa por lado mediante el helper canónico, sin alterar la fuente de 10 pt.
    configurar_geometria_tabla(
        tbl_t17, total_width_dxa=8784,
        col_widths_dxa=[1340, 1593, 939, 1095, 1105, 1617, 1095],
        align="center", cell_margin_dxa=(30, 50, 30, 50)
    )


if __name__ == "__main__":
    import docx
    from docx_utilidades import aplicar_margenes_unajma
    d = docx.Document()
    aplicar_margenes_unajma(d.sections[0])
    construir_capitulo5(d)
    os.makedirs("salidas/documentos", exist_ok=True)
    d.save("salidas/documentos/test_cap5.docx")
    print("Capítulo V compilado exitosamente.")
