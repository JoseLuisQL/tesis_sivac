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
- Numeración global continua de tablas: Tablas 13, 14, 15, 16 y 17
- Cero invención de datos de campo: marcadores formales [Pendiente]
- Cero signos '$', cero fórmulas crudas y cero jerga interna
================================================================================
"""

import os
import sys
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utilidades')))

from docx_utilidades import (
    agregar_titulo_1, agregar_titulo_2, agregar_titulo_3, agregar_titulo_4,
    agregar_parrafo, agregar_item_lista, agregar_tabla_datos
)


SUJETOS_CENTROS_UNIFICADOS = [
    ("S-01", "Almacén Especializado DISA Apurímac II - Sede Central"),
    ("S-02", "Almacén Especializado DISA Apurímac II - Sede Central"),
    ("S-03", "Almacén Especializado DISA Apurímac II - Sede Central"),
    ("S-04", "Almacén Especializado DISA Apurímac II - Sede Central"),
    ("S-05", "Centro de Acopio Andahuaylas"),
    ("S-06", "Centro de Acopio Andahuaylas"),
    ("S-07", "Centro de Acopio Talavera"),
    ("S-08", "Centro de Acopio Talavera"),
    ("S-09", "Centro de Acopio San Jerónimo"),
    ("S-10", "Centro de Acopio San Jerónimo"),
    ("S-11", "Centro de Acopio Santa María de Chicmo"),
    ("S-12", "Centro de Acopio Huancarama"),
    ("S-13", "Centro de Acopio Chincheros"),
    ("S-14", "Centro de Acopio Uripa/Ocobamba")
]


def construir_capitulo5(doc):
    agregar_titulo_1(doc, "CAPÍTULO V: RESULTADOS")

    # ==========================================================================
    # 5.1. Análisis descriptivo
    # ==========================================================================
    agregar_titulo_2(doc, "5.1. Análisis descriptivo")

    # --------------------------------------------------------------------------
    # 5.1.1. Dimensión 1: Oportunidad de procesamiento
    # --------------------------------------------------------------------------
    agregar_titulo_3(doc, "5.1.1. Dimensión 1: Oportunidad de procesamiento")
    agregar_parrafo(
        doc,
        "El análisis descriptivo de la primera dimensión evaluó el comportamiento temporal de las operaciones "
        "logísticas en los ocho centros de acopio de la Dirección de Salud Apurímac II a través de dos indicadores "
        "cuantitativos expresados en minutos: el tiempo de registro de movimiento de vacunas y el tiempo de emisión "
        "de comprobante de salida o vale. Las mediciones se efectuaron mediante observación directa cronometrada con "
        "el Instrumento N.° 01 sobre los catorce operadores que conformaron la población censal, contrastando el "
        "desempeño del procedimiento manual tradicional en el pre-test frente al flujo automatizado con el sistema "
        "web SIVAC en el post-test. En la Tabla 13 se presenta la distribución individual por sujeto y centro de "
        "acopio, junto con los estadísticos de tendencia central y dispersión.",
        sangria=True
    )

    headers_t13 = [
        "Sujeto",
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
        ["**Media**", "**Promedio aritmético censal (n = 14)**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**DE**", "**Desviación estándar muestral**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Mediana**", "**Percentil 50 de la distribución**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Mínimo**", "**Valor mínimo observado**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Máximo**", "**Valor máximo observado**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"]
    ])

    agregar_tabla_datos(
        doc,
        numero="13",
        titulo="Comparación descriptiva de los tiempos de registro y emisión de vales de salida entre el pre-test y post-test",
        encabezados=headers_t13,
        filas=filas_t13,
        nota="Tiempos medidos en minutos mediante el Instrumento N.° 01 sobre la población censal de 14 operadores distribuidos en los 8 centros de acopio de la DISA Apurímac II. Valores con marcador [Pendiente] reservados para el vaciado del levantamiento de campo.",
        col_widths=[Inches(0.65), Inches(2.05), Inches(0.85), Inches(0.85), Inches(0.85), Inches(0.85)],
        font_size_pt=8.5
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
        "de conformidad (nombre del biológico, número de lote, fecha de vencimiento, cantidad física, procedencia o "
        "destino, identificación del operador, saldo aritmético de kardex y correlatividad temporal). Los resultados "
        "descriptivos se consolidan en la Tabla 14.",
        sangria=True
    )

    headers_t14 = [
        "Sujeto",
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
        ["**Media**", "**Promedio aritmético censal (n = 14)**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**DE**", "**Desviación estándar muestral**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Mediana**", "**Percentil 50 de la distribución**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Mínimo**", "**Valor mínimo observado**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Máximo**", "**Valor máximo observado**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"]
    ])

    agregar_tabla_datos(
        doc,
        numero="14",
        titulo="Comparación descriptiva del porcentaje de registros sin discrepancias y concordancia de cantidades entre el pre-test y post-test",
        encabezados=headers_t14,
        filas=filas_t14,
        nota="Proporciones obtenidas mediante auditoría documental con el Instrumento N.° 02 en los 8 centros de acopio de la DISA Apurímac II (n = 14). Valores con marcador [Pendiente] reservados para el vaciado del levantamiento de campo.",
        col_widths=[Inches(0.65), Inches(2.05), Inches(0.85), Inches(0.85), Inches(0.85), Inches(0.85)],
        font_size_pt=8.5
    )

    agregar_parrafo(
        doc,
        "Los valores consolidados en la Tabla 14 reflejan el impacto de las reglas de integridad referencial, el "
        "bloqueo preventivo de despachos con existencias insuficientes y el ordenamiento automático por fecha de "
        "expiración implementados en la base de datos relacional del sistema web SIVAC para erradicar los errores "
        "de arrastre aritmético y transcripción manual.",
        sangria=True
    )

    # --------------------------------------------------------------------------
    # 5.1.3. Dimensión 3: Satisfacción del usuario
    # --------------------------------------------------------------------------
    agregar_titulo_3(doc, "5.1.3. Dimensión 3: Satisfacción del usuario")
    agregar_parrafo(
        doc,
        "El análisis descriptivo de la tercera dimensión examinó la percepción de los catorce operadores de la cadena "
        "de inmunizaciones respecto a la gestión logística mediante dos indicadores sustentados en el Modelo de "
        "Aceptación Tecnológica (Davis, 1989): la aceptación del proceso y la utilidad percibida. La medición se "
        "realizó a través del Instrumento N.° 03, integrado por dieciséis reactivos calificados en escala ordinal "
        "Likert de cinco niveles (desde 1 = Totalmente en desacuerdo hasta 5 = Totalmente de acuerdo). En la Tabla 15 "
        "se exponen los puntajes promediados e índices sumativos registrados en el pre-test y post-test.",
        sangria=True
    )

    headers_t15 = [
        "Sujeto",
        "Centro de Acopio",
        "Aceptación del Proceso Pre-test (1-5)",
        "Aceptación del Proceso Post-test (1-5)",
        "Utilidad Percibida Pre-test (1-5)",
        "Utilidad Percibida Post-test (1-5)"
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
        ["**Media**", "**Promedio aritmético censal (n = 14)**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**DE**", "**Desviación estándar muestral**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Mediana**", "**Percentil 50 de la distribución**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Mínimo**", "**Valor mínimo observado**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"],
        ["**Máximo**", "**Valor máximo observado**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**", "**[Pendiente]**"]
    ])

    agregar_tabla_datos(
        doc,
        numero="15",
        titulo="Comparación descriptiva de la aceptación del proceso y utilidad percibida entre el pre-test y post-test",
        encabezados=headers_t15,
        filas=filas_t15,
        nota="Puntuaciones obtenidas mediante el Instrumento N.° 03 (Cuestionario TAM en escala Likert de 1 a 5) sobre la población censal de la DISA Apurímac II (n = 14). Valores con marcador [Pendiente] reservados para el vaciado del levantamiento de campo.",
        col_widths=[Inches(0.65), Inches(2.05), Inches(0.85), Inches(0.85), Inches(0.85), Inches(0.85)],
        font_size_pt=8.5
    )

    agregar_parrafo(
        doc,
        "La comparación presentada en la Tabla 15 permite evaluar la evolución de la conformidad del personal técnico "
        "y administrativo frente a la facilidad de aprendizaje, la fluidez del despacho de vacunas y la eficacia del "
        "control de lotes alcanzado con la plataforma web frente al procedimiento manual previo.",
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
        "(post-test menos pre-test) de cada uno de los seis indicadores evaluados. Se establecieron las siguientes "
        "hipótesis estadísticas para la verificación del supuesto de normalidad a un nivel de significancia de 0.05:",
        sangria=True
    )
    agregar_item_lista(
        doc,
        "**Hipótesis nula de normalidad (H0):** Las diferencias pareadas entre el post-test y el pre-test de los "
        "indicadores siguen una distribución normal (valor de significancia mayor a 0.05).",
        simbolo="•"
    )
    agregar_item_lista(
        doc,
        "**Hipótesis alterna de normalidad (H1):** Las diferencias pareadas entre el post-test y el pre-test de los "
        "indicadores no siguen una distribución normal (valor de significancia menor o igual a 0.05).",
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
            "14",
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
        nota="Prueba de Shapiro-Wilk evaluada con nivel de significancia de 0.05 sobre las diferencias pareadas (n = 14). Si el p-valor supera 0.05 se emplea la prueba t de Student para muestras relacionadas; en caso contrario se aplica la prueba de rangos con signo de Wilcoxon.",
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
        "la investigación, adoptando un nivel de significancia nominal de 0.05 (nivel de confianza del 95%).",
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
        "La regla de decisión estadística estableció rechazar la hipótesis nula y aceptar la hipótesis alterna del "
        "investigador si el valor de probabilidad asociado al estadístico de contraste para muestras relacionadas "
        "(estadístico Z de rangos con signo de Wilcoxon o estadístico t de Student pareado) resultaba inferior al "
        "umbral crítico de 0.05.",
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
        "El contraste inferencial evaluó si las mediciones del post-test en los indicadores de tiempo de registro y "
        "tiempo de emisión de vale presentaron una disminución estadísticamente significativa respecto a las "
        "mediciones del pre-test bajo el criterio de significancia menor a 0.05.",
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
        "La prueba de hipótesis verificó si las proporciones auditadas en el post-test superaron significativamente "
        "los niveles de exactitud documental registrados durante la gestión manual en el pre-test.",
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
        "El contraste estadístico determinó si las puntuaciones psicométricas obtenidas con el cuestionario TAM tras "
        "la implementación del sistema web SIVAC evidenciaron un incremento significativo (significancia menor a 0.05) "
        "frente a la línea base del pre-test. En la Tabla 17 se presenta el consolidado general de las pruebas "
        "inferenciales y de magnitud del efecto para las cuatro hipótesis del estudio.",
        sangria=True
    )

    headers_t17 = [
        "Hipótesis Contrastada",
        "Indicadores Evaluados",
        "Estadístico de Contraste (Z / t)",
        "Significancia Bilateral (p-valor)",
        "Tamaño del Efecto (r)",
        "Decisión Estadística (alfa = 0.05)"
    ]
    filas_t17 = [
        [
            "Hipótesis General:\nGestión de movimientos de vacunas",
            "Desempeño integral en las tres dimensiones evaluadas",
            "[Pendiente]",
            "[Pendiente]",
            "[Pendiente]",
            "[Pendiente]"
        ],
        [
            "Hipótesis Específica 1:\nOportunidad de procesamiento",
            "Tiempo de registro de movimiento de vacunas\n\nTiempo de emisión de comprobante de salida o vale",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]"
        ],
        [
            "Hipótesis Específica 2:\nConsistencia documental",
            "Porcentaje de registros sin discrepancias\n\nConcordancia de cantidad programada versus entregada",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]"
        ],
        [
            "Hipótesis Específica 3:\nSatisfacción del usuario",
            "Aceptación del proceso\n\nUtilidad percibida",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]",
            "[Pendiente]\n\n[Pendiente]"
        ]
    ]

    agregar_tabla_datos(
        doc,
        numero="17",
        titulo="Consolidado de la contrastación inferencial de las hipótesis general y específicas mediante pruebas para muestras relacionadas",
        encabezados=headers_t17,
        filas=filas_t17,
        nota="Contrastes inferenciales pre-test versus post-test evaluados en la población censal de la DISA Apurímac II (n = 14) a un nivel de significancia de 0.05. Valores con marcador [Pendiente] reservados para la ejecución del script bioestadístico con datos reales de campo.",
        col_widths=[Inches(1.23), Inches(1.53), Inches(0.83), Inches(0.83), Inches(0.74), Inches(0.94)],
        font_size_pt=8.5
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
