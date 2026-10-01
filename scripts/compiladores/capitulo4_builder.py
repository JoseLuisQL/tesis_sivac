#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB — ENSAMBLADOR DE CAPÍTULO IV: METODOLOGÍA (.DOCX)
Universidad Nacional José María Arguedas (UNAJMA)
Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas
================================================================================
"""

import os
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx_utilidades import (
    agregar_titulo_1, agregar_titulo_2, agregar_titulo_3,
    agregar_parrafo, agregar_item_lista, agregar_tabla_datos
)

def construir_capitulo4(doc):
    agregar_titulo_1(doc, "CAPÍTULO IV: METODOLOGÍA DE LA INVESTIGACIÓN")

    agregar_parrafo(
        doc,
        "El presente capítulo describe la metodología científica rigurosa adoptada para contrastar la hipótesis de "
        "investigación y determinar la influencia del sistema web SIVAC sobre la gestión de movimientos de vacunas. Se detallan "
        "el enfoque, tipo, nivel y diseño metodológico; la formulación canónica de hipótesis; la matriz de operacionalización de "
        "variables; la caracterización de la población censal; las técnicas e instrumentos de recolección de datos con sus respectivas "
        "evidencias de validez y confiabilidad; el procedimiento de trabajo de campo; el plan de análisis estadístico inferencial; "
        "y las consideraciones éticas institucionales observadas.",
        sangria=True
    )

    # 4.1. Enfoque, Tipo y Nivel de Investigación
    agregar_titulo_2(doc, "4.1. Enfoque, Tipo y Nivel de Investigación")
    agregar_parrafo(
        doc,
        "**Enfoque de Investigación:** La investigación se enmarca en el **enfoque cuantitativo** (Hernández Sampieri et al., 2014), "
        "toda vez que utiliza la recolección sistemática de datos numéricos y métricas operacionales objetivas (minutos cronometrados de registro, "
        "minutos de emisión de comprobantes, porcentajes de concordancia aritmética y puntajes en escalas psicométricas) para probar hipótesis "
        "previamente establecidas mediante medición numérica y análisis estadístico inferencial estandarizado.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Tipo de Investigación:** Por su finalidad, corresponde a una investigación **aplicada y tecnológica**. Es aplicada porque busca "
        "resolver una problemática concreta e inmediata en la administración sanitaria de la DISA Apurímac II; y es tecnológica porque involucra "
        "la concepción, diseño e implementación de un artefacto de software funcional (Sistema web SIVAC) estructurado según estándares de "
        "ingeniería de software (ISO/IEC 25010:2023) y metodologías ágiles de desarrollo (Extreme Programming).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Nivel de Investigación:** La investigación alcanza el nivel **explicativo causal**, puesto que no se limita a describir las deficiencias "
        "del estado actual ni a establecer meras correlaciones estadísticas, sino que tiene como propósito fundamental demostrar la relación de "
        "causa-efecto existente entre la manipulación deliberada de la Variable Independiente (implantación de SIVAC) y las transformaciones "
        "observadas en la Variable Dependiente (gestión de movimientos de vacunas en sus tres dimensiones).",
        sangria=True
    )

    # 4.2. Diseño Metodológico
    agregar_titulo_2(doc, "4.2. Diseño Metodológico")
    agregar_parrafo(
        doc,
        "La investigación adopta un diseño **preexperimental con pretest y postest en un solo grupo** ($O_1 \\longrightarrow X \\longrightarrow O_2$), "
        "conformado por la totalidad de la población censal de usuarios responsables de la gestión de biológicos en la red de frío de la DISA Apurímac II "
        "(Hernández Sampieri et al., 2014). El esquema metodológico formal se representa de la siguiente manera:",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "$$G: O_1 \\longrightarrow X \\longrightarrow O_2$$",
        sangria=False,
        cursiva=False,
        negrita=True,
        alineacion=WD_ALIGN_PARAGRAPH.CENTER
    )
    agregar_parrafo(
        doc,
        "Donde:\n"
        "• **$G$:** Grupo censal único conformado por los 14 trabajadores de inmunizaciones de los 11 centros de acopio provinciales.\n"
        "• **$O_1$:** Medición basal preliminar (*Pretest*), efectuada sobre los procesos manuales y hojas de cálculo tradicionales.\n"
        "• **$X$:** Estímulo o tratamiento experimental, constituido por la implantación, puesta en producción y uso operativo del sistema web SIVAC.\n"
        "• **$O_2$:** Medición final posterior (*Postest*), realizada tras la operatividad del sistema SIVAC bajo idénticas condiciones y métricas.",
        sangria=True
    )

    # 4.3. Hipótesis de Investigación
    agregar_titulo_2(doc, "4.3. Hipótesis de Investigación")
    agregar_parrafo(
        doc,
        "En concordancia biunívoca 1:1 con los problemas y objetivos de la investigación y en cumplimiento de la directriz metodológica "
        "**DEC-007**, se formularon las siguientes hipótesis:",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Hipótesis General (HG):**\n"
        "La implementación del sistema web SIVAC influye significativamente en la gestión de movimientos de vacunas en el personal "
        "de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Hipótesis Específica 1 (HE1):**\n"
        "La implementación del sistema web SIVAC influye significativamente en la oportunidad de procesamiento de la gestión de movimientos "
        "de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Hipótesis Específica 2 (HE2):**\n"
        "La implementación del sistema web SIVAC influye significativamente en la consistencia documental de la gestión de movimientos "
        "de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Hipótesis Específica 3 (HE3):**\n"
        "La implementación del sistema web SIVAC influye significativamente en la satisfacción del usuario en el personal de inmunizaciones "
        "de la Dirección de Salud Apurímac II, Andahuaylas 2025.",
        sangria=True
    )

    # 4.4. Operacionalización de Variables
    agregar_titulo_2(doc, "4.4. Operacionalización de Variables")
    agregar_parrafo(
        doc,
        "La operacionalización descompone analíticamente las variables en dimensiones, indicadores, fórmulas de cálculo, escalas de medición "
        "e instrumentos de recojo de datos, garantizando la trazabilidad científica de cada medición:",
        sangria=True
    )

    headers_op = ["Variable", "Dimensiones", "Indicadores", "Fórmula / Métrica", "Escala", "Instrumento"]
    filas_op = [
        ["Variable Independiente (VI):\nSistema web SIVAC\n(Extreme Programming / ISO 25010)",
         "D1: Adecuación Funcional\n(ISO/IEC 25010:2023)",
         "Ind 1.1: Completitud funcional\nInd 1.2: Exactitud de resultados",
         "$(HU_{validadas} / HU_{totales}) \\times 100$\n% Errores aritméticos en saldos",
         "Razón\nRazón",
         "Ficha de aceptación de software (XP / ISO 25010)"],
        ["",
         "D2: Usabilidad\n(ISO/IEC 25010:2023)",
         "Ind 2.1: Facilidad de aprendizaje\nInd 2.2: Claridad de interfaz",
         "Minutos de inducción requeridos\nEvaluación de interfaz (1-5)",
         "Razón\nOrdinal",
         "Guía de usabilidad de software"],
        ["Variable Dependiente (VD):\nGestión de movimientos de vacunas\n(NTS N° 196-MINSA / DEC-007)",
         "D1: Oportunidad de procesamiento",
         "Ind 1.1: Tiempo de registro mensual ($T_{reg}$)\nInd 1.2: Tiempo de emisión de vale ($T_{vale}$)",
         "Minutos cronometrados en registro\nMinutos cronometrados en emisión",
         "Razón (min)\nRazón (min)",
         "Ficha de observación y cronometraje temporal"],
        ["",
         "D2: Consistencia documental",
         "Ind 2.1: % Registros sin discrepancias ($RSD$)\nInd 2.2: % Concordancia programada ($CPE$)",
         "$(Lotes_{sin\\_disc} / 20) \\times 100$\n$(Cant_{entregada} / Cant_{prog}) \\times 100$",
         "Razón (%)\nRazón (%)",
         "Ficha de cotejo y verificación de inventario"],
        ["",
         "D3: Satisfacción del usuario\n(Modelo TAM - Davis, 1989)",
         "Ind 3.1: Aceptación del proceso ($AP$)\nInd 3.2: Utilidad percibida ($UP$)",
         "Sumatoria ítems 1 a 5 (5-25 pts)\nSumatoria ítems 6 a 10 (5-25 pts)",
         "Ordinal / Intervalo\n(Baremo 10-50 pts)",
         "Cuestionario psicométrico TAM (Escala Likert 1-5)"]
    ]
    agregar_tabla_datos(
        doc,
        numero=4.1,
        titulo="Matriz de operacionalización de variables de investigación (DEC-007)",
        encabezados=headers_op,
        filas=filas_op,
        nota="Elaboración propia basada en ISO/IEC (25010:2023), NTS N° 196-MINSA (2022) y Davis (1989)."
    )

    # 4.5. Población y Muestra
    agregar_titulo_2(doc, "4.5. Población y Muestra")
    agregar_parrafo(
        doc,
        "**Población:** La población objetivo estuvo constituida por la totalidad del personal de salud directamente responsable de "
        "la recepción, custodia de cadena de frío, registro en kardex, distribución y reporte de vacunas en la Dirección de Salud Apurímac II, "
        "abarcando las provincias de Andahuaylas y Chincheros, correspondiente a catorce (14) profesionales y técnicos sanitarios.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Muestra y Tipo de Muestreo:** Dado que el tamaño de la población es reducido, finito y plenamente accesible ($N = 14 \\le 50$), "
        "se aplicó un **muestreo no probabilístico de tipo censal**, en el cual la muestra coincide exactamente con la totalidad del universo "
        "poblacional ($N = n = 14$). Los catorce trabajadores censados desempeñan sus labores operativas en los once (11) centros de acopio zonales "
        "de la red de frío institucional:",
        sangria=True
    )
    headers_pob = ["N°", "Código Sujeto", "Centro de Acopio de Red de Frío", "Ámbito Provincial", "Responsabilidad Principal"]
    filas_pob = [
        ["1", "TRAB-01", "Centro de Acopio Central DISA (Sede)", "Andahuaylas", "Coordinación regional y recepción de remesas"],
        ["2", "TRAB-02", "Centro de Acopio Central DISA (Sede)", "Andahuaylas", "Gestión de almacén de biológicos y pecosas"],
        ["3", "TRAB-03", "Centro de Acopio Andahuaylas", "Andahuaylas", "Custodia y distribución microred Andahuaylas"],
        ["4", "TRAB-04", "Centro de Acopio Andahuaylas", "Andahuaylas", "Control de kardex y despacho a puestos de salud"],
        ["5", "TRAB-05", "Centro de Acopio San Jerónimo", "Andahuaylas", "Custodia y despacho microred San Jerónimo"],
        ["6", "TRAB-06", "Centro de Acopio Talavera", "Andahuaylas", "Custodia y despacho microred Talavera"],
        ["7", "TRAB-07", "Centro de Acopio Santa María de Chicmo", "Andahuaylas", "Custodia y despacho microred Chicmo"],
        ["8", "TRAB-08", "Centro de Acopio Huancabamba", "Andahuaylas", "Custodia y despacho microred Huancabamba"],
        ["9", "TRAB-09", "Centro de Acopio Pampachiri", "Andahuaylas", "Custodia y despacho microred Pampachiri"],
        ["10", "TRAB-10", "Centro de Acopio Huancarama", "Andahuaylas", "Custodia y despacho microred Huancarama"],
        ["11", "TRAB-11", "Centro de Acopio Chincheros", "Chincheros", "Coordinación provincial y custodia Chincheros"],
        ["12", "TRAB-12", "Centro de Acopio Chincheros", "Chincheros", "Kardex y distribución a centros periféricos"],
        ["13", "TRAB-13", "Centro de Acopio Uripa", "Chincheros", "Custodia y despacho microred Uripa"],
        ["14", "TRAB-14", "Centro de Acopio Ocobamba", "Chincheros", "Custodia y despacho microred Ocobamba"]
    ]
    agregar_tabla_datos(
        doc,
        numero=4.2,
        titulo="Distribución de la población censal de trabajadores de inmunizaciones según centro de acopio",
        encabezados=headers_pob,
        filas=filas_pob,
        nota="Población censal oficial ($N = n = 14$). Fuente: Coordinación de Inmunizaciones de la DISA Apurímac II."
    )
    agregar_parrafo(
        doc,
        "**Criterios de Inclusión:** Personal nombrado o contratado (CAS/terceros) con funciones oficiales de manejo de cadena de frío y kardex "
        "de biológicos con una antigüedad mayor a tres meses en el centro de acopio, y que otorgó su consentimiento informado voluntario.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Criterios de Exclusión:** Personal con licencias médicas prolongadas, personal rotativo sin permanencia operativa o que desempeñe "
        "exclusivamente labores de digitación asistencial no vinculada al control de existencias de vacunas.",
        sangria=True
    )

    # 4.6. Técnicas e Instrumentos de Recolección de Datos
    agregar_titulo_2(doc, "4.6. Técnicas e Instrumentos de Recolección de Datos")
    agregar_parrafo(
        doc,
        "Para recolectar la información empírica de manera objetiva, sistemática y auditable, se seleccionaron tres técnicas complementarias:",
        sangria=True
    )
    agregar_item_lista(doc, "**Técnica de Observación Sistemática y Ficha de Cronometraje Temporal:** Empleada para cuantificar la dimensión *Oportunidad de Procesamiento*. Se utilizó un cronómetro digital estandarizado para medir con precisión de décimas de minuto el tiempo requerido para efectuar el balance mensual de movimientos de 10 establecimientos adscritos ($T_{reg}$) y el tiempo demandado para la generación y emisión física de un vale oficial de distribución ($T_{vale}$).", sangria_izq=0.5)
    agregar_item_lista(doc, "**Técnica de Análisis Documental y Ficha de Cotejo de Inventario:** Utilizada para evaluar la *Consistencia Documental*. Se contrastó una muestra de auditoría física de 20 lotes por centro de acopio frente a los saldos asentados en kardex para calcular el porcentaje de registros sin discrepancias ($RSD$), y se verificaron las actas de recepción de remesas institucionales para determinar la concordancia programada vs entregada ($CPE$).", sangria_izq=0.5)
    agregar_item_lista(doc, "**Técnica de Encuesta y Cuestionario Psicométrico TAM:** Empleada para medir la dimensión *Satisfacción del Usuario*. Se aplicó un instrumento de diez (10) reactivos formulados en escala Likert de 5 puntos (1: Totalmente en desacuerdo, 5: Totalmente de acuerdo), estructurado en dos subdimensiones: Aceptación del Proceso ($AP$, ítems 1 al 5) y Utilidad Percibida ($UP$, ítems 6 al 10), con un baremo global de 10 a 50 puntos (Bajo: 10-22, Medio: 23-36, Alto: 37-50).", sangria_izq=0.5)

    agregar_titulo_3(doc, "4.6.1. Validez de los Instrumentos por Juicio de Expertos")
    agregar_parrafo(
        doc,
        "La validez de contenido de los instrumentos fue dictaminada formalmente mediante **juicio de expertos**, participando tres (3) jueces "
        "especialistas con grado de Magíster y Doctor en Ingeniería de Sistemas y Salud Pública. Los jueces evaluaron la claridad, pertinencia "
        "y relevancia de cada reactivo utilizando el coeficiente de **V de Aiken** (Tristán, 2008). Todos los ítems alcanzaron coeficientes "
        "comprendidos entre **0.87 y 1.00**, superando con holgura el punto de corte crítico institucional ($V > 0.80$, $p < .05$), lo que confirmó "
        "su validez de contenido.",
        sangria=True
    )

    agregar_titulo_3(doc, "4.6.2. Confiabilidad Psicométrica del Instrumento TAM")
    agregar_parrafo(
        doc,
        "La consistencia interna del cuestionario TAM fue evaluada mediante el coeficiente **Alfa de Cronbach** en ambas etapas experimentales. "
        "En la fase pretest, el instrumento arrojó un coeficiente $\\alpha = 0.5851$, coherente con la dispersión y heterogeneidad de percepciones "
        "asociadas al uso de hojas de cálculo disímiles y registros en papel. En la fase postest, tras la implantación de SIVAC, se registró un "
        "coeficiente global de $\\alpha = 0.3863$, con promedios por ítem marcadamente concentrados en el límite superior (medias entre 4.43 y 4.71 "
        "sobre 5.0) y desviaciones estándar mínimas ($SD \\approx 0.47$ a $0.52$). Este fenómeno psicométrico de compresión de varianza "
        "(*efecto techo* o *ceiling effect*) refleja un consenso y homogeneidad unánime en la satisfacción del personal.",
        sangria=True
    )

    # 4.7. Procedimiento de Recolección de Datos
    agregar_titulo_2(doc, "4.7. Procedimiento de Recolección de Datos")
    agregar_parrafo(
        doc,
        "La ejecución del trabajo de campo se desarrolló de manera secuencial a través de tres etapas operativas:",
        sangria=True
    )
    agregar_item_lista(doc, "**Etapa 1: Diagnóstico de Línea Base (Pretest):** Coordinación con la Dirección Ejecutiva de Salud Individual y la Estrategia de Inmunizaciones de la DISA Apurímac II. Aplicación de las fichas de observación temporal, auditoría física de saldos y aplicación del cuestionario TAM en los 11 centros de acopio sobre el método tradicional de trabajo manual y en Excel.", sangria_izq=0.5)
    agregar_item_lista(doc, "**Etapa 2: Implantación y Puesta en Producción de SIVAC:** Despliegue de la plataforma web en infraestructura de servidores seguros, parametrización de catálogos normados de vacunas según la NTS N° 196-MINSA, capacitación presencial y virtual a los 14 operadores en sus puestos de trabajo, y periodo de acompañamiento técnico de cuatro semanas de operación continua.", sangria_izq=0.5)
    agregar_item_lista(doc, "**Etapa 3: Evaluación de Salida (Postest):** Medición final utilizando exactamente los mismos instrumentos, cronómetros y criterios de auditoría de inventario, consolidando las matrices empíricas de salida para su análisis estadístico.", sangria_izq=0.5)

    # 4.8. Plan de Procesamiento y Análisis de Datos
    agregar_titulo_2(doc, "4.8. Plan de Procesamiento y Análisis de Datos")
    agregar_parrafo(
        doc,
        "El análisis cuantitativo de los datos empíricos se diseñó bajo un estricto protocolo de reproducibilidad computacional implementado "
        "en lenguaje Python mediante el script científico `analisis_estadistico_sivac.py`, estructurado en las siguientes fases analíticas:",
        sangria=True
    )
    agregar_item_lista(doc, "**Control de Calidad de Datos:** Auditoría de integridad estructural, cálculo de códigos hash criptográficos SHA-256 para prevenir alteraciones y verificación de rangos matemáticos en las matrices de pretest y postest.", sangria_izq=0.5)
    agregar_item_lista(doc, "**Análisis Descriptivo:** Cálculo de medidas de tendencia central (media aritmética, mediana) y de dispersión (desviación estándar, rangos intercuartílicos), acompañadas de representaciones gráficas de barras comparativas a 300 DPI.", sangria_izq=0.5)
    agregar_item_lista(doc, "**Evaluación de Normalidad (Shapiro-Wilk):** Aplicación de la prueba de bondad de ajuste de Shapiro-Wilk sobre la serie de diferencias pareadas ($D_i = \\text{Post}_i - \\text{Pre}_i$) de cada indicador para determinar la parametricidad de los datos bajo un nivel de significancia $\\alpha = 0.05$.", sangria_izq=0.5)
    agregar_item_lista(doc, "**Contraste de Hipótesis Inferencial Principal (Wilcoxon):** Aplicación de la prueba no paramétrica de rangos con signo de Wilcoxon para muestras relacionadas ($n = 14$), calculando el estadístico $W$, el valor $Z$ tipificado, el $p$-valor unilateral y el tamaño del efecto $r$ de Rosenthal ($r = |Z| / \\sqrt{2n}$), interpretado según los estándares de Cohen (1988).", sangria_izq=0.5)
    agregar_item_lista(doc, "**Contraste Paramétrico de Verificación (t de Student pareada):** Ejecución complementaria de la prueba $t$ de Student para muestras emparejadas ($gl = 13$) y estimación del tamaño del efecto mediante la $d$ de Cohen para corroborar la robustez de los hallazgos.", sangria_izq=0.5)

    # 4.9. Consideraciones Éticas
    agregar_titulo_2(doc, "4.9. Consideraciones Éticas")
    agregar_parrafo(
        doc,
        "La investigación se rigió estrictamente por el Código de Ética de la Investigación de la UNAJMA y las directrices internacionales "
        "de la Declaración de Helsinki. Se garantizó el principio de **autonomía** mediante la suscripción del consentimiento informado por parte "
        "de cada participante; la **confidencialidad y protección de la privacidad**, anonimizando las identidades de los evaluados mediante códigos "
        "alfanuméricos (`TRAB-01` a `TRAB-14`); la **no maleficencia**, asegurando que las evaluaciones no interfirieran con el normal abastecimiento "
        "de vacunas a la población infantil; y la **integridad científica y transparencia de datos**, certificando la autenticidad e inalterabilidad "
        "de los registros de campo.",
        sangria=True
    )
