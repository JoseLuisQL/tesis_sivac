#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - ENSAMBLADOR DE CAPÍTULO III: MARCO TEÓRICO (.DOCX)
Universidad Nacional José María Arguedas (UNAJMA)
Facultad de Ingeniería - Escuela Profesional de Ingeniería de Sistemas
Modelo 1:1 EPIS-UNAJMA (Jhon 2026):
- 3.1. Bases teóricas (con Figuras 1 a 10 extraídas a 300 DPI de fuentes primarias y Tabla 1)
- 3.2. Marco conceptual (18 entradas numeradas 3.2.1 a 3.2.18 con citas APA 7)
- 3.3. Metodología de desarrollo de software Extreme Programming (XP)
       (Tablas 2 a 8 y Figuras 11 a 19 basadas en el código real de syncova)
================================================================================
"""

import os
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx_utilidades import (
    agregar_titulo_1, agregar_titulo_2, agregar_titulo_3, agregar_titulo_4,
    agregar_parrafo, agregar_item_lista, agregar_tabla_datos,
    agregar_figura_apa7
)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GRAFICOS_DIR = os.path.join(BASE_DIR, "salidas", "figuras", "recursos_graficos")
if not os.path.exists(GRAFICOS_DIR):
    GRAFICOS_DIR = os.path.join(BASE_DIR, "salidas", "recursos_graficos")

OBSIDIAN_FIGURAS_DIR = r"C:\MisInvestigaciones\obsidian_vault\_adjuntos\figuras_fuentes"


def _resolver_ruta_figura(nombre_archivo, fallback_relativo=None, fallback_secundario=None):
    """Resuelve la ruta de una figura priorizando salidas/figuras/recursos_graficos y aplicando fallback a Obsidian."""
    ruta_primaria = os.path.join(GRAFICOS_DIR, nombre_archivo)
    if os.path.exists(ruta_primaria):
        return ruta_primaria
    if fallback_relativo:
        ruta_fb = os.path.join(OBSIDIAN_FIGURAS_DIR, *fallback_relativo.replace("\\", "/").split("/"))
        if os.path.exists(ruta_fb):
            return ruta_fb
    if fallback_secundario:
        ruta_sec = os.path.join(GRAFICOS_DIR, fallback_secundario)
        if os.path.exists(ruta_sec):
            return ruta_sec
    return ruta_primaria


def construir_capitulo3(doc):
    agregar_titulo_1(doc, "CAPÍTULO III: MARCO TEÓRICO")

    # ==========================================================================
    # 3.1. BASES TEÓRICAS
    # ==========================================================================
    agregar_titulo_2(doc, "3.1. Bases teóricas")

    # --------------------------------------------------------------------------
    # 3.1.1. Sistema web
    # --------------------------------------------------------------------------
    agregar_titulo_3(doc, "3.1.1. Sistema web")
    agregar_parrafo(
        doc,
        "En la presente investigación científica, el sistema web SIVAC actúa epistemológicamente como la "
        "intervención tecnológica aplicada (estímulo experimental manipulado, formalizado como el factor X), orientada "
        "a transformar y optimizar los procesos de control logístico en el personal de inmunizaciones de la Dirección "
        "de Salud Apurímac II. Bajo esta delimitación metodológica, Extreme Programming (XP) constituye la metodología "
        "de ingeniería empleada para su construcción incremental y colaborativa, mientras que la norma ISO/IEC 25010:2023 "
        "constituye el estándar técnico de verificación de calidad del producto software previo y complementario a su "
        "evaluación preexperimental en campo. De este modo, se establece con rigor que ni las fases del desarrollo de "
        "software bajo XP ni las características de calidad de ISO/IEC 25010 constituyen dimensiones estadísticas de la "
        "variable independiente, sino marcos ingenieriles de construcción y aseguramiento de calidad que garantizan la "
        "integridad funcional y operativa del artefacto antes de contrastar su efecto sobre la gestión de movimientos "
        "de vacunas.",
        sangria=True
    )

    agregar_titulo_4(doc, "3.1.1.1. Aplicaciones web y arquitectura cliente-servidor")
    agregar_parrafo(
        doc,
        "Las aplicaciones web constituyen sistemas informáticos distribuidos diseñados bajo el modelo cliente-servidor, "
        "cuya operación se sustenta en tres pilares tecnológicos estandarizados: el Localizador Uniforme de Recursos (URL) "
        "para la identificación unívoca de activos en la red, el Protocolo de Transferencia de Hipertexto (HTTP/HTTPS) "
        "para el intercambio transaccional de solicitudes y respuestas, y el Lenguaje de Marcado de Hipertexto (HTML) "
        "para la representación visual en el navegador cliente (Luján Mora, 2002, p. 16). Mediante la convergencia de "
        "estos componentes, múltiples operadores situados en ubicaciones geográficas dispersas pueden interactuar de "
        "manera concurrente con un repositorio de datos centralizado, prescindiendo de instalaciones locales complejas "
        "en cada estación de trabajo.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "En la ingeniería de sistemas empresariales y sanitarios, el diseño arquitectónico evoluciona hacia un esquema "
        "lógico de múltiples capas desacopladas (N-Capas), el cual establece fronteras bien definidas entre la interfaz "
        "de presentación, la lógica del dominio o reglas de negocio, y la capa de persistencia relacional (De la Torre "
        "Llorente et al., 2010, p. iv). Como sostiene Sommerville (2016, p. 181), el procesamiento distribuido en capas "
        "independientes permite escalar y mantener cada nivel tecnológico sin comprometer la estabilidad de los demás "
        "componentes, asegurando una única fuente de verdad institucional en redes organizacionales descentralizadas "
        "(véase la Figura 1).",
        sangria=True
    )

    agregar_figura_apa7(
        doc,
        numero="1",
        titulo="Pilares tecnológicos de la arquitectura web (URL, HTTP y HTML)",
        ruta_imagen=_resolver_ruta_figura(
            "figura_01_lujan_pilares_web.png",
            "programacion-de-aplicaciones-web-historia-principios-basicos-y-clientes-web/figura_p0044_1.png"
        ),
        texto_nota="Adaptado de Programación de aplicaciones web: Historia, principios básicos y clientes web (p. 16), por S. Luján Mora, 2002, Editorial Club Universitario."
    )

    agregar_titulo_4(doc, "3.1.1.2. Arquitectura Modelo-Vista-Controlador (MVC) y APIs RESTful con autenticación basada en tokens")
    agregar_parrafo(
        doc,
        "El patrón arquitectónico Modelo-Vista-Controlador (MVC) organiza la estructura interna de las aplicaciones "
        "web separando la gestión de los datos y las reglas del dominio (Modelo), la presentación e interacción visual "
        "con el usuario (Vista) y la coordinación de las peticiones entrantes (Controlador) (Sommerville, 2016, p. 177). "
        "En el ámbito de los sistemas de salud pública, este desacoplamiento permite que las vistas de usuario se "
        "actualicen dinámicamente en aplicaciones de página única (SPA), mientras que los controladores validan las "
        "operaciones de inventario y delegan el procesamiento transaccional a servicios especializados (Balón Morejón, "
        "2023, p. 10; Mego Navarro, 2021, p. 32).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "En las arquitecturas web modernas, la comunicación entre el cliente y el servidor se materializa mediante "
        "Interfaces de Programación de Aplicaciones basadas en la Transferencia de Estado Representacional (API RESTful), "
        "las cuales manipulan recursos identificados por URI a través de métodos HTTP estándar (GET, POST, PUT, PATCH, "
        "DELETE) e intercambian cargas útiles estructuradas en formato JSON. Para resguardar la confidencialidad y "
        "la integridad de los registros sanitarios, el acceso a los servicios se protege mediante tokens criptográficos "
        "de autenticación sin estado (JSON Web Tokens) y esquemas de control de acceso basado en roles (RBAC), "
        "garantizando la verificación estricta de identidad y privilegios en cada transacción (Ruiz Barea, 2023, p. 36) "
        "(véase la Figura 2).",
        sangria=True
    )

    agregar_figura_apa7(
        doc,
        numero="2",
        titulo="Arquitectura de una aplicación web basada en el patrón Modelo-Vista-Controlador (MVC)",
        ruta_imagen=_resolver_ruta_figura(
            "figura_02_sommerville_mvc_web.png",
            "software-engineering/manual_p0178_1.png"
        ),
        texto_nota="Adaptado de Software engineering (10.ª ed., p. 177), por I. Sommerville, 2016, Pearson."
    )

    agregar_titulo_4(doc, "3.1.1.3. Metodología de desarrollo ágil Extreme Programming (XP)")
    agregar_parrafo(
        doc,
        "Extreme Programming (XP) es una metodología ágil de ingeniería de software concebida para equipos de desarrollo "
        "pequeños y medianos que enfrentan requerimientos dinámicos o sujetos a cambios normativos recurrentes (Beck, "
        "1999, p. 70). A diferencia del modelo lineal en cascada y de los ciclos iterativos convencionales de larga "
        "duración, XP acorta radicalmente los bucles de retroalimentación técnica y funcional, integrando el análisis, "
        "el diseño, la codificación y las pruebas dentro de iteraciones breves con entregas continuas de software "
        "operativo (Beck, 1999, p. 71; Sommerville, 2016, p. 57) (véase la Figura 3). En este ámbito, Kokol (2022) "
        "comprobó en una revisión sistemática de alcance sobre desarrollo ágil en el sector sanitario que las metodologías "
        "ágiles entregan soluciones de software médico con mayor rapidez y superior calidad técnica que los enfoques en "
        "cascada, adaptándose rigurosamente a marcos regulatorios exigentes y resultando idóneas para afrontar requerimientos "
        "críticos y cambiantes como los vinculados a la logística y distribución de vacunas.",
        sangria=True
    )

    agregar_figura_apa7(
        doc,
        numero="3",
        titulo="Evolución desde el ciclo en cascada e iterativo hacia Extreme Programming (XP)",
        ruta_imagen=_resolver_ruta_figura(
            "figura_03_beck_evolucion_xp.png",
            "embracing-change-with-extreme-programming/figura_p0001_1.png"
        ),
        texto_nota="Adaptado de «Embracing change with extreme programming» (p. 70), por K. Beck, 1999, Computer, 32(10). https://doi.org/10.1109/2.796139"
    )

    agregar_parrafo(
        doc,
        "El proceso disciplinar de XP se articula en cuatro fases metodológicas interdependientes: planeación, diseño, "
        "codificación y pruebas (Pressman, 2010, p. 61). La fase de planeación inicia con la captura de requerimientos "
        "mediante historias de usuario redactadas en el lenguaje del dominio operativo, las cuales son estimadas en "
        "puntos de esfuerzo y priorizadas junto al cliente en el sitio para conformar el plan de entregas (Cohn, 2004, "
        "p. vii). La fase de diseño aplica el principio de simplicidad estructural, apoyándose en tarjetas CRC y "
        "prototipos operativos; la fase de codificación incorpora la refactorización continua y la integración "
        "permanente; y la fase de pruebas verifica cada incremento mediante pruebas unitarias automatizadas y pruebas "
        "de aceptación validadas por los usuarios finales (Pressman, 2010, p. 62) (véase la Figura 4).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Resulta fundamental enfatizar que las cuatro fases del ciclo XP (planeación, diseño, codificación y pruebas) "
        "constituyen el marco procedimental de ingeniería de software que asegura la construcción reproducible de la "
        "intervención tecnológica, diferenciándose con nitidez metodológica de las dimensiones analíticas de la variable "
        "dependiente evaluada en la investigación.",
        sangria=True
    )

    agregar_figura_apa7(
        doc,
        numero="4",
        titulo="El proceso de la metodología ágil Extreme Programming (XP)",
        ruta_imagen=_resolver_ruta_figura(
            "figura_04_pressman_proceso_xp.png",
            "pressman-ingenieria-del-software-un-enfoque-practico/figura_p0094_1.png"
        ),
        texto_nota="Adaptado de Ingeniería del software: Un enfoque práctico (7.ª ed., p. 62), por R. S. Pressman, 2010, McGraw-Hill Interamericana."
    )

    agregar_titulo_4(doc, "3.1.1.4. Calidad de producto de software según la norma ISO/IEC 25010:2023")
    agregar_parrafo(
        doc,
        "La evaluación técnica de un producto de software requiere un marco normativo estandarizado que permita "
        "cuantificar sus propiedades internas y externas en condiciones reales de operación. El estándar internacional "
        "ISO/IEC 25010:2023, perteneciente a la familia de normas Systems and software Quality Requirements and "
        "Evaluation (SQuaRE), establece el modelo de calidad del producto de software estructurado en características "
        "y subcaracterísticas multidimensionales que abarcan la adecuación funcional, eficiencia de desempeño, "
        "compatibilidad, capacidad de interacción (usabilidad), fiabilidad, seguridad, mantenibilidad y flexibilidad "
        "(International Organization for Standardization y International Electrotechnical Commission, 2023, p. 2).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "En las aplicaciones informáticas orientadas a los servicios de salud, Moumane et al. (2024, p. 3) destacan "
        "que la adecuación funcional (completitud, corrección y pertinencia de los cálculos clínicos o logísticos), "
        "la usabilidad (reconocibilidad, facilidad de aprendizaje y protección frente a errores humanos de digitación), "
        "la eficiencia temporal de respuesta y la seguridad de los datos constituyen los factores críticos que "
        "determinan la confiabilidad técnica de la herramienta en los establecimientos sanitarios (véase la Figura 5). "
        "De forma convergente en el ámbito peruano, Mamani-Pari et al. (2026) desarrollaron y validaron psicométricamente "
        "un modelo de evaluación bajo la norma ISO/IEC 25010 alineado con las directivas del Ministerio de Salud, "
        "demostrando que la operabilidad, la protección contra errores de los usuarios y la adecuación funcional son "
        "los componentes esenciales que reducen la carga cognitiva y optimizan los flujos de trabajo asistenciales. "
        "En la presente investigación, la aplicación del estándar ISO/IEC 25010:2023 cumple el rol específico de "
        "verificar objetivamente la calidad del producto de software SIVAC antes y como soporte de su despliegue en "
        "campo, sin sustituir ni confundirse con las dimensiones de evaluación de la variable dependiente.",
        sangria=True
    )

    agregar_figura_apa7(
        doc,
        numero="5",
        titulo="Características y subcaracterísticas del modelo de calidad del producto de software ISO/IEC 25010",
        ruta_imagen=_resolver_ruta_figura(
            "figura_05_moumane_iso25010.png",
            "isoiec-25010-based-quality-evaluation-of-three-mobile-applications-for-reproduct/figura_p0003_1.png"
        ),
        texto_nota="Adaptado de «ISO/IEC 25010-based quality evaluation of three mobile applications for reproductive health services in Morocco» (p. 3), por K. Moumane et al., 2024, Clinical and Experimental Obstetrics & Gynecology, 51(4), Artículo 88. https://doi.org/10.31083/j.ceog5104088"
    )

    # --------------------------------------------------------------------------
    # 3.1.2. Gestión de movimientos de vacunas
    # --------------------------------------------------------------------------
    agregar_titulo_3(doc, "3.1.2. Gestión de movimientos de vacunas")

    agregar_titulo_4(doc, "3.1.2.1. Cadena de frío e inmunizaciones en el sistema de salud pública")
    agregar_parrafo(
        doc,
        "La gestión de movimientos de vacunas comprende el conjunto de procesos técnicos, administrativos y logísticos "
        "destinados a planificar, recepcionar, conservar, distribuir y controlar las existencias de productos "
        "inmunobiológicos e insumos complementarios a través de los distintos niveles de la red sanitaria (Ministerio de Salud, 2022, "
        "p. 14; World Health Organization, 2021). Debido a su naturaleza termolábil, las vacunas requieren conservarse de manera ininterrumpida "
        "dentro del rango térmico normado de +2 °C a +8 °C en los almacenes regionales, centros de acopio y "
        "establecimientos de salud del primer nivel de atención, con el fin de preservar su potencia inmunogénica "
        "hasta el acto de vacunación (Champi Velásquez, 2023, p. 14). Al respecto, Gutiérrez-Aguado et al. (2024, "
        "pp. 73–78) demostraron que en el programa nacional de inmunizaciones del Perú persisten marcadas vulnerabilidades "
        "en la cadena de frío debido a una obsolescencia de equipos de conservación superior al 60% y a discrepancias "
        "entre los sistemas patrimoniales del SIGA-MEF y la realidad de los centros de salud, lo que acentúa la "
        "necesidad de herramientas informáticas ágiles que vinculen los movimientos con la capacidad frigorífica real.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "A lo largo de la cadena de suministro sanitaria, el flujo físico de las remesas biológicas debe estar "
        "respaldado por un flujo documental riguroso que registre las entradas por comprobantes institucionales, "
        "las transferencias entre microredes, los despachos periódicos y los saldos físicos en cámara fría (Addy "
        "et al., 2024, p. 2; Garcia Villacorta y Calderón Huaman, 2023). La articulación ordenada de estas operaciones "
        "desde el almacén central hasta los puntos locales de vacunación resulta esencial para evitar tanto el "
        "desabastecimiento como el vencimiento de dosis en stock (véase la Figura 6).",
        sangria=True
    )

    agregar_figura_apa7(
        doc,
        numero="6",
        titulo="Flujo logístico de la cadena de frío e inmunizaciones desde la fabricación hasta el establecimiento de salud",
        ruta_imagen=_resolver_ruta_figura(
            "figura_06_champi_cadena_frio.png",
            "implementacion-de-un-sistema-de-monitoreo-inalambrico-mediante-internet-de-las-c/manual_p0023_1.png"
        ),
        texto_nota="Adaptado de Implementación de un sistema de monitoreo inalámbrico mediante Internet de las Cosas para la conservación de la cadena de frío de las vacunas (p. 12), por J. M. Champi Velásquez, 2023, Universidad Tecnológica del Perú."
    )

    agregar_titulo_4(doc, "3.1.2.2. Sistemas electrónicos de información de gestión logística (e-LMIS) y control FEFO")
    agregar_parrafo(
        doc,
        "Los sistemas electrónicos de información de gestión logística (e-LMIS, por sus siglas en inglés) son "
        "plataformas digitales especializadas que automatizan la captura, consolidación y seguimiento de los "
        "movimientos de suministros médicos y biológicos a lo largo de las redes de salud (Organización Panamericana de la Salud y PATH, 2020; "
        "Wasswa et al., 2023). A diferencia de los registros tradicionales basados en libros físicos de kardex y "
        "planillas aisladas, un sistema e-LMIS integra en tiempo real la programación anual de metas, la recepción "
        "de lotes, la validación de existencias y la emisión de órdenes de despacho, optimizando la capacidad de "
        "respuesta ante campañas regulares y contingencias epidemiológicas (Kigenza et al., 2023). En concordancia con "
        "ello, Gilbert et al. (2020, p. 562) verificaron en un estudio a gran escala sobre 924 centros sanitarios que la "
        "implementación de una plataforma digital integrada de registro de inmunizaciones y gestión logística redujo la "
        "tasa de desabastecimiento de vacunas de 7.1% a 2.1%, comprobando que la deducción automática de inventario por cada "
        "atención registrada previene pérdidas y consolida la disponibilidad biológica en el primer nivel de atención.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Un pilar algorítmico indispensable en los sistemas e-LMIS aplicados a inmunizaciones es la regla de control "
        "FEFO (First Expired, First Out o Primero en Expirar, Primero en Salir), la cual prioriza de forma automática "
        "la asignación y salida de aquellos lotes cuya fecha de caducidad sea más próxima (Shen et al., 2024, p. 1). "
        "Asimismo, la plataforma vincula cada dosis biológica con sus jeringas descartables y diluyentes según los "
        "multiplicadores normados, garantizando una trazabilidad integral de extremo a extremo en la red de suministro "
        "(Wasswa et al., 2023) (véase la Figura 7).",
        sangria=True
    )

    agregar_figura_apa7(
        doc,
        numero="7",
        titulo="Flujo operativo de suministros y trazabilidad en un sistema electrónico de información de gestión logística (e-LMIS)",
        ruta_imagen=_resolver_ruta_figura(
            "figura_07_wasswa_flujo_elmis.png",
            "leveraging-electronic-logistics-management-information-systems-to-enhance-and-op/figura_p0004_1.png"
        ),
        texto_nota="Adaptado de «Leveraging electronic logistics management information systems to enhance and optimize supply chain response during public health emergencies: Lessons from COVID-19 response in Uganda» (p. 4), por J. Wasswa et al., 2023, Journal of Pharmaceutical Policy and Practice, 16, Artículo 6. https://doi.org/10.1186/s40545-023-00517-4"
    )

    agregar_titulo_4(doc, "3.1.2.3. Dimensión 1: Oportunidad de procesamiento")
    agregar_parrafo(
        doc,
        "La oportunidad de procesamiento se define como la capacidad operativa del sistema de gestión logística para "
        "ejecutar el registro transaccional de los movimientos de vacunas y la emisión de los documentos oficiales "
        "de despacho en el menor tiempo posible, eliminando los retrasos administrativos que postergan la toma de "
        "decisiones sanitarias (Dang et al., 2024). En entornos donde el control se realiza manualmente, el personal "
        "de enfermería invierte extensas jornadas en verificar saldos anteriores en folios físicos, calcular "
        "aritméticamente entradas y salidas, y redactar a mano los comprobantes de entrega para cada establecimiento.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "La operacionalización de esta dimensión comprende dos indicadores cronométricos directos: el tiempo de "
        "registro de movimiento de vacunas y el tiempo de emisión de comprobante de salida (vale). Como demuestran "
        "Dang et al. (2024) y Astuhuaman Perez y Baltazar Maza (2023, p. 56), la sustitución de formatos físicos por "
        "interfaces web con precarga automática de saldos intermensuales y generación instantánea de documentos PDF "
        "reduce de manera sustancial los tiempos operativos en los establecimientos de salud.",
        sangria=True
    )

    agregar_titulo_4(doc, "3.1.2.4. Dimensión 2: Consistencia documental")
    agregar_parrafo(
        doc,
        "La consistencia documental constituye el grado de exactitud, integridad y concordancia sin discrepancias "
        "entre los registros logísticos asentados en el sistema documental, las programaciones sanitarias aprobadas "
        "y los movimientos físicos ejecutados en los almacenes de biológicos (Chekol et al., 2023, p. 3). En los "
        "sistemas de información rutinaria de salud, las deficiencias de consistencia se originan principalmente "
        "por errores humanos de transcripción numérica, omisión de números de lote o fechas de caducidad, duplicidad "
        "de asientos en el kardex y desalineación entre las cuotas planificadas y las cantidades despachadas "
        "(Chekol et al., 2023, p. 9).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Esta dimensión se evalúa mediante dos indicadores cuantitativos: el porcentaje de registros sin discrepancias "
        "y la concordancia de cantidad programada versus entregada. De acuerdo con Mekonen et al. (2024, p. 375), "
        "la implementación de validaciones lógicas en base de datos, restricciones de unicidad compuesta y cálculos "
        "automatizados de balance mensual permite erradicar las inconsistencias aritméticas en el kardex de vacunas "
        "y asegurar la correspondencia estricta con el requerimiento institucional (véase la Figura 8).",
        sangria=True
    )

    agregar_figura_apa7(
        doc,
        numero="8",
        titulo="Marco conceptual de la calidad y consistencia de datos en sistemas de información rutinaria de salud (RHIS)",
        ruta_imagen=_resolver_ruta_figura(
            "figura_08_chekol_calidad_datos_rhis.png",
            "data-quality-and-associated-factors-of-routine-health-information-system-among-h/figura_p0003_1.png"
        ),
        texto_nota="Adaptado de «Data quality and associated factors of routine health information system among health centers of West Gojjam Zone, northwest Ethiopia, 2021» (p. 3), por A. Chekol et al., 2023, Frontiers in Health Services, 3, Artículo 1059611. https://doi.org/10.3389/frhs.2023.1059611"
    )

    agregar_titulo_4(doc, "3.1.2.5. Dimensión 3: Satisfacción del usuario y Modelo de Aceptación Tecnológica (TAM)")
    agregar_parrafo(
        doc,
        "La satisfacción del usuario constituye una dimensión evaluativa esencial en la adopción e impacto de sistemas "
        "de información en salud pública, definida como el grado de conformidad, valoración favorable y disposición "
        "cognitiva que experimenta el personal de inmunizaciones al interactuar con el entorno tecnológico durante el "
        "desempeño de sus funciones. En el contexto de sistemas de información logístico-sanitarios de uso institucional "
        "obligatorio, la satisfacción no puede conceptualizarse como una reacción afectiva superficial o espontánea, "
        "sino que se articula teóricamente integrando el modelo de éxito de sistemas de información con el Modelo de "
        "Aceptación Tecnológica (TAM), formulado originalmente por Davis (1989, p. 320). En organizaciones públicas donde "
        "la utilización de la plataforma informática está normativamente prescrita, la disposición y conformidad del "
        "operador emergen fundamentalmente de la interacción causal entre dos constructos determinantes: la facilidad "
        "de uso percibida (grado en que el usuario considera que la interacción con la plataforma está libre de esfuerzo "
        "cognitivo y procedimental) y la utilidad percibida (grado en que el profesional tiene la convicción de que el "
        "sistema potencia su rendimiento, exactitud y productividad laboral) (Luo et al., 2024, p. 4) (véase la Figura 9).",
        sangria=True
    )

    agregar_figura_apa7(
        doc,
        numero="9",
        titulo="Marco teórico de facilidad de uso percibida y utilidad percibida en la adopción de sistemas de información en salud (TAM)",
        ruta_imagen=_resolver_ruta_figura(
            "figura_09_luo_modelo_tam_salud.png",
            "luo-2024-role-perceived-ease-use-usefulness/figura_p0004_1.png"
        ),
        texto_nota="Adaptado de «Role of perceived ease of use, usefulness, and financial strength on the adoption of health information systems: The moderating role of hospital size» (p. 4), por J. Luo et al., 2024, Humanities and Social Sciences Communications, 11, Artículo 516. https://doi.org/10.1057/s41599-024-02976-9"
    )

    agregar_parrafo(
        doc,
        "En consonancia con las decisiones metodológicas institucionales de la presente investigación (DEC-007), la "
        "tercera dimensión oficial, Satisfacción del usuario, se operacionaliza a través de dos indicadores psicométricos "
        "rigurosamente derivados de TAM: (a) el indicador Aceptación del proceso (AP), el cual operacionaliza la subescala "
        "de facilidad de uso percibida y adaptabilidad procedimental frente al flujo digitalizado, evaluando el grado en "
        "que el personal de enfermería percibe que el registro en cuadrícula, la navegación y las validaciones del sistema "
        "son comprensibles, intuitivas y fluidas, minimizando la carga cognitiva impuesta por los formatos manuales; y (b) "
        "el indicador Utilidad percibida (UP), el cual operacionaliza directamente la subescala de utilidad en el desempeño "
        "laboral, midiendo en qué medida el operador sanitario juzga que el sistema web SIVAC mejora el control de los "
        "movimientos de vacunas, acelera la emisión de comprobantes, erradica los descuadres de kardex y favorece la "
        "disponibilidad biológica institucional. Esta fundamentación concuerda plenamente con los hallazgos empíricos de "
        "Hussain et al. (2025, p. 8), quienes comprobaron en personal de enfermería de establecimientos públicos que la "
        "facilidad de uso percibida actúa como predictor directo cardinal de la aceptación del sistema (coeficiente "
        "beta = 0.35, p < 0.001) y que la utilidad percibida media decisivamente dicha relación (beta = 0.23, p < 0.001), "
        "confirmando que mitigar la fatiga operativa y agilizar el procesamiento conduce de manera directa a elevar la "
        "satisfacción del usuario sanitario.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Asimismo, en el ámbito de los sistemas informáticos de inmunizaciones, Ndlovu et al. (2021) y Oliveira "
        "et al. (2020, p. 4) demostraron que la aceptación procedimental y la percepción de utilidad se incrementan "
        "de modo sustantivo cuando la herramienta digital suprime la doble digitación en libros de papel, proporciona "
        "alertas tempranas sobre la caducidad de lotes y automatiza la generación de comprobantes de salida en los centros "
        "de acopio y establecimientos (véase la Figura 10). En la Tabla 1 se presenta la estructura integral de las tres "
        "dimensiones oficiales, sus respectivos indicadores, descripciones operacionales y escalas de medición que guían "
        "la evaluación preexperimental de la variable dependiente.",
        sangria=True
    )

    agregar_figura_apa7(
        doc,
        numero="10",
        titulo="Factores determinantes de la aceptación y uso de un sistema de información del programa nacional de inmunizaciones",
        ruta_imagen=_resolver_ruta_figura(
            "figura_10_oliveira_aceptacion_sipni.png",
            "oliveira-2020-acceptance-use-information-system-national/manual_p0004_1.png"
        ),
        texto_nota="Adaptado de «Acceptance and use of the Information System of the National Immunization Program» (p. 4), por V. C. Oliveira et al., 2020, Revista Latino-Americana de Enfermagem, 28, Artículo e3307. https://doi.org/10.1590/1518-8345.3360.3307"
    )

    headers_t1 = [
        "Dimensión",
        "Indicador",
        "Descripción operacional",
        "Unidad y escala de medición"
    ]
    filas_t1 = [
        [
            "Oportunidad de procesamiento",
            "Tiempo de registro de movimiento de vacunas",
            "Duración cronometrada requerida por el operador para registrar y validar el movimiento mensual de vacunas de los establecimientos asignados.",
            "Minutos (Escala de razón)"
        ],
        [
            "Oportunidad de procesamiento",
            "Tiempo de emisión de comprobante de salida (vale)",
            "Duración cronometrada desde la confirmación del despacho hasta la generación y descarga del vale oficial de entrega en formato PDF.",
            "Minutos (Escala de razón)"
        ],
        [
            "Consistencia documental",
            "Porcentaje de registros sin discrepancias",
            "Proporción porcentual de registros de movimientos auditados que cumplen íntegramente los 8 criterios de exactitud aritmética y trazabilidad de lote.",
            "Porcentaje (Escala de razón)"
        ],
        [
            "Consistencia documental",
            "Concordancia de cantidad programada versus entregada",
            "Proporción porcentual de correspondencia entre las dosis asignadas en la planificación mensual y las dosis efectivamente despachadas en el vale.",
            "Porcentaje (Escala de razón)"
        ],
        [
            "Satisfacción del usuario",
            "Aceptación del proceso (AP)",
            "Operacionaliza la subescala de facilidad de uso percibida y adaptabilidad procedimental del modelo TAM (Davis, 1989; Hussain et al., 2025) frente al flujo digitalizado de uso institucional obligatorio.",
            "Puntaje Likert de 1 a 5 (Escala ordinal)"
        ],
        [
            "Satisfacción del usuario",
            "Utilidad percibida (UP)",
            "Operacionaliza el grado en que el operador considera que SIVAC mejora su desempeño laboral en el control de movimientos de vacunas bajo el modelo TAM (Davis, 1989; Hussain et al., 2025; Luo et al., 2024).",
            "Puntaje Likert de 1 a 5 (Escala ordinal)"
        ]
    ]
    agregar_tabla_datos(
        doc,
        numero="1",
        titulo="Dimensiones, indicadores y escalas de medición de la gestión de movimientos de vacunas",
        encabezados=headers_t1,
        filas=filas_t1,
        nota="Síntesis de la estructura dimensional y operacional de la variable dependiente basada en Dang et al. (2024), Chekol et al. (2023) e integrando el modelo de éxito de sistemas de información con el Modelo de Aceptación Tecnológica (TAM) de Davis (1989) y la evidencia empírica de Hussain et al. (2025) y Luo et al. (2024) conforme a la decisión metodológica DEC-007.",
        col_widths=[1900, 1900, 3200, 1784]
    )

    # ==========================================================================
    # 3.2. MARCO CONCEPTUAL
    # ==========================================================================
    agregar_titulo_2(doc, "3.2. Marco conceptual")

    conceptos_32 = [
        (
            "3.2.1. Cadena de frío de inmunizaciones",
            "Sistema logístico y técnico continuo conformado por recursos humanos, infraestructura frigorífica normada "
            "y procedimientos operativos que garantizan el almacenamiento, conservación y transporte de las vacunas "
            "dentro del rango de temperatura de +2 °C a +8 °C desde su fabricación hasta su administración al usuario "
            "final (Ministerio de Salud, 2022, p. 14; Champi Velásquez, 2023, p. 14)."
        ),
        (
            "3.2.2. Centro de acopio de vacunas",
            "Instalación sanitaria intermedia dotada de equipos frigoríficos certificados que recepciona remesas de "
            "productos biológicos y jeringas desde el nivel regional o nacional para custodiarlas y distribuirlas "
            "periódicamente hacia los establecimientos de salud adscritos a su jurisdicción territorial (Ministerio de Salud, 2022, p. 14)."
        ),
        (
            "3.2.3. Comprobante de salida (vale de entrega)",
            "Documento administrativo oficial de control patrimonial y logístico que respalda la entrega física y la "
            "transferencia de custodia de lotes de vacunas y jeringas desde un centro de acopio hacia un establecimiento "
            "de salud receptor (Garcia Villacorta y Calderón Huaman, 2023)."
        ),
        (
            "3.2.4. Concordancia de cantidad programada versus entregada",
            "Indicador de consistencia logística que cuantifica el grado de correspondencia porcentual entre las dosis "
            "de biológicos planificadas en el requerimiento periódico y las cantidades físicamente despachadas y "
            "validadas en los comprobantes de entrega (Wasswa et al., 2023; Mekonen et al., 2024, p. 375)."
        ),
        (
            "3.2.5. Consistencia documental",
            "Cualidad de exactitud, integridad y ausencia de discrepancias aritméticas o de registro entre los datos "
            "asentados en los soportes documentales de inventario y las existencias físicas reales en la cadena de "
            "frío (Chekol et al., 2023, p. 3)."
        ),
        (
            "3.2.6. Control de acceso basado en roles (RBAC)",
            "Mecanismo de seguridad informática que restringe el acceso a los módulos, rutas y operaciones de un "
            "sistema web en función del rol organizacional y los permisos explícitamente asignados a cada usuario "
            "autenticado (Ruiz Barea, 2023, p. 36)."
        ),
        (
            "3.2.7. Criterio FEFO (First Expired, First Out)",
            "Regla de gestión de inventarios perecederos y farmacéuticos según la cual los lotes cuya fecha de "
            "vencimiento sea más próxima deben ser despachados y utilizados con prioridad sobre aquellos con fecha "
            "de expiración más lejana (Shen et al., 2024, p. 1)."
        ),
        (
            "3.2.8. Extreme Programming (XP)",
            "Metodología ágil de ingeniería de software fundamentada en ciclos iterativos cortos, planificación por "
            "historias de usuario, diseño simple, refactorización continua, integración permanente y validación "
            "mediante pruebas automatizadas y de aceptación con el cliente (Beck, 1999, p. 70; Pressman, 2010, p. 61)."
        ),
        (
            "3.2.9. Factor de pérdida de biológicos",
            "Proporción estimada de dosis de una vacuna en presentación multidosis o monodosis que no llega a "
            "administrarse efectivamente debido a mermas operativas, caducidad del frasco abierto o manipulación "
            "durante la jornada de inmunización (Ministerio de Salud, 2022, p. 14)."
        ),
        (
            "3.2.10. Historia de usuario",
            "Especificación breve y estructurada en lenguaje natural que describe una funcionalidad requerida por "
            "un rol operativo del sistema, precisando la acción solicitada, el beneficio esperado y los criterios "
            "objetivos de aceptación para su verificación (Cohn, 2004, p. vii)."
        ),
        (
            "3.2.11. JSON Web Token (JWT)",
            "Estándar abierto basado en objetos JSON firmados digitalmente que permite transmitir de forma compacta, "
            "autónoma y sin estado la identidad y los privilegios de un usuario entre el cliente web y el servidor "
            "de aplicaciones (Ruiz Barea, 2023, p. 36)."
        ),
        (
            "3.2.12. Kardex digital de biológicos",
            "Registro transaccional electrónico e inmutable que asienta en orden cronológico cada ingreso, salida, "
            "transferencia o ajuste de inventario por lote de vacuna, actualizando de forma automática el saldo "
            "anterior y el saldo disponible (Mego Navarro, 2021, p. 32; Garcia Villacorta y Calderón Huaman, 2023)."
        ),
        (
            "3.2.13. Lote de vacuna",
            "Cantidad definida y homogénea de frascos o dosis de un producto inmunobiológico fabricados en un mismo "
            "ciclo productivo, identificada por un código alfanumérico único y una fecha de caducidad específica "
            "(Ministerio de Salud, 2022, p. 14)."
        ),
        (
            "3.2.14. Modelo de Aceptación Tecnológica (TAM)",
            "Marco teórico psicométrico que explica el nivel de adopción y satisfacción de los usuarios frente a un "
            "sistema informático a partir de dos percepciones centrales: la facilidad de uso percibida y la utilidad "
            "percibida en el desempeño laboral (Davis, 1989, p. 320; Luo et al., 2024, p. 4)."
        ),
        (
            "3.2.15. Oportunidad de procesamiento",
            "Atributo operativo de la gestión logística que mide la rapidez y puntualidad con que se registran las "
            "transacciones de inventario y se emiten los comprobantes oficiales para la distribución oportuna de "
            "vacunas (Dang et al., 2024)."
        ),
        (
            "3.2.16. ORM (Object-Relational Mapping)",
            "Técnica de programación que convierte y sincroniza las tablas de una base de datos relacional con "
            "entidades y objetos fuertemente tipados en la capa de lógica de negocio, garantizando la integridad "
            "de las consultas y transacciones (De la Torre Llorente et al., 2010, p. iv)."
        ),
        (
            "3.2.17. Sistema electrónico de información de gestión logística (e-LMIS)",
            "Aplicación informática centralizada que digitaliza el ciclo de suministro sanitario, integrando la "
            "programación de requerimientos, el control de inventarios por lotes, las alertas de caducidad y la "
            "trazabilidad de los despachos entre almacenes y establecimientos de salud (Organización Panamericana de la Salud y PATH, 2020; Wasswa et al., 2023)."
        ),
        (
            "3.2.18. Trazabilidad de vacunas",
            "Capacidad técnica y documental de reconstruir el historial completo de ubicación, recepción, lote, "
            "condiciones de conservación y distribución de cada biológico a lo largo de toda la cadena de suministro "
            "sanitaria (Addy et al., 2024, p. 2; Shen et al., 2024, p. 1)."
        )
    ]

    for subtitulo, definicion in conceptos_32:
        agregar_titulo_3(doc, subtitulo)
        agregar_parrafo(doc, definicion, sangria=True)

    # ==========================================================================
    # 3.3. METODOLOGÍA DE DESARROLLO DE SOFTWARE EXTREME PROGRAMMING (XP)
    # ==========================================================================
    agregar_titulo_2(doc, "3.3. Metodología de desarrollo de software Extreme Programming (XP)")

    # --------------------------------------------------------------------------
    # 3.3.1. Fase I: Exploración y planificación de requerimientos
    # --------------------------------------------------------------------------
    agregar_titulo_3(doc, "3.3.1. Fase I: Exploración y planificación de requerimientos")
    agregar_parrafo(
        doc,
        "El desarrollo de ingeniería del sistema web SIVAC se ejecutó aplicando las cuatro fases iterativas de la "
        "metodología ágil Extreme Programming (XP): planificación, diseño, codificación y pruebas, cuya efectividad "
        "en el desarrollo de software asistencial fue sustentada por Kokol (2022) al evidenciar que el enfoque centrado "
        "en historias de usuario optimiza la elicitación de requisitos complejos en salud, y por Inarotul Huda et al. "
        "(2025), quienes demostraron que las cuatro fases de XP permiten erradicar los cuellos de botella del registro "
        "manual y reducir sustancialmente los tiempos operativos mediante el desarrollo colaborativo con los usuarios. "
        "Durante la Fase I se estableció la metáfora arquitectónica del sistema, denominada «Cadena digital sincronizada "
        "de trazabilidad de biológicos», según la cual cada transacción de vacunas y jeringas entre el almacén regional, "
        "los ocho centros de acopio y los establecimientos de salud de Andahuaylas y Chincheros mantiene una continuidad "
        "lógica ininterrumpida, análoga a la conservación térmica de la cadena de frío física. Asimismo, a partir del "
        "análisis de necesidades en la sede institucional de la Dirección de Salud Apurímac II y el repositorio "
        "institucional del proyecto (syncova), se conformó el equipo de trabajo definiendo las responsabilidades "
        "metodológicas y los perfiles operativos del control de acceso basado en roles (RBAC), conforme se detalla en "
        "la Tabla 2.",
        sangria=True
    )

    headers_t2 = ["Rol en la metodología XP y en el sistema", "Actor institucional asignado", "Responsabilidades ejecutadas en el ciclo de vida"]
    filas_t2 = [
        [
            "Cliente en el sitio (On-site Customer)",
            "Coordinación de la Estrategia Sanitaria de Inmunizaciones (DISA Apurímac II)",
            "Definición de reglas de negocio según la NTS N° 196-MINSA, priorización de historias de usuario y validación de pruebas de aceptación."
        ],
        [
            "Desarrollador / Arquitecto XP",
            "Bach. José Luis Quispe León (Tesista e ingeniero de software)",
            "Diseño arquitectónico en tres capas, modelado relacional en Prisma ORM, codificación en TypeScript/React y ejecución de suites de prueba."
        ],
        [
            "Administrador del sistema (administrador)",
            "Especialista de tecnologías de información de la DISA Apurímac II",
            "Administración integral de cuentas de usuario, roles, permisos granulares, catálogos maestros y parámetros institucionales."
        ],
        [
            "Coordinador regional (coordinador)",
            "Equipo técnico de cadena de frío e inmunizaciones (Sede Andahuaylas)",
            "Gestión de la programación anual CENARES, supervisión del almacén central, monitoreo de alertas y habilitación de permisos operativos."
        ],
        [
            "Responsable de acopio (responsable_acopio)",
            "Responsables de inmunizaciones de los 8 centros de acopio provinciales",
            "Recepción de lotes bajo criterio FEFO, registro de movimientos mensuales, gestión de entregas adicionales y emisión de vales oficiales."
        ],
        [
            "Operador de establecimiento (operador)",
            "Personal sanitario de centros y puestos de salud periféricos",
            "Consulta de asignaciones mensuales, verificación de vales de entrega recepcionados y seguimiento del kardex por lote."
        ]
    ]
    agregar_tabla_datos(
        doc,
        numero="2",
        titulo="Roles del equipo de desarrollo y usuarios operativos del sistema web SIVAC",
        encabezados=headers_t2,
        filas=filas_t2,
        nota="Estructura de roles técnicos y funcionales implementada en el esquema RBAC de SIVAC.",
        col_widths=[2200, 2400, 4184]
    )

    agregar_parrafo(
        doc,
        "A partir de las sesiones formales del juego de la planificación (Planning Game) y talleres de validación "
        "con los responsables de cadena de frío de los ocho centros de acopio y la coordinación de inmunizaciones de "
        "la DISA Apurímac II, se especificaron dieciséis (16) historias de usuario (HU-01 a HU-16) siguiendo la "
        "estructura formal de rol, necesidad funcional y propósito operativo (Cohn, 2004, p. vii). Cada historia de "
        "usuario fue vinculada a criterios de aceptación objetivos y verificables, registrándose su trazabilidad "
        "en el repositorio institucional del proyecto (syncova), y su esfuerzo fue estimado en puntos de historia "
        "mediante la serie de Fibonacci, totalizando 76 puntos de historia distribuidos según su prioridad técnica "
        "y valor sanitario (véase la Tabla 3). Las fichas técnicas de historias de usuario, criterios de aceptación "
        "y actas de validación operativa se encuentran consolidadas en el Anexo 5.",
        sangria=True
    )

    headers_t3 = ["Código", "Título de la historia de usuario", "Rol solicitante", "Criterio principal de aceptación verificado", "Prioridad", "Puntos (PH)", "Iteración"]
    filas_t3 = [
        ["HU-01", "Autenticación JWT y control de acceso RBAC", "Administrador / Usuarios", "Inicio de sesión con hash Bcrypt, emisión de token JWT y filtrado por centro de acopio.", "Alta", "5", "Iteración 1"],
        ["HU-02", "Gestión jerárquica de redes, microredes y centros", "Administrador", "Registro y vinculación relacional de redes, microredes, 8 centros de acopio y establecimientos.", "Alta", "5", "Iteración 1"],
        ["HU-03", "Catálogo maestro de vacunas y jeringas", "Coordinador", "Parametrización de vacunas con dosis por frasco, rango térmico y catálogo de jeringas.", "Alta", "3", "Iteración 1"],
        ["HU-04", "Configuración de multiplicadores jeringa-vacuna", "Coordinador", "Asignación de factores de multiplicación por defecto y por centro para cálculo automático.", "Media", "3", "Iteración 1"],
        ["HU-05", "Registro de lotes de vacunas y jeringas (FEFO)", "Responsable de acopio", "Ingreso de lotes con comprobante PECOSA/Guía, fecha de caducidad y ordenamiento FEFO.", "Alta", "8", "Iteración 2"],
        ["HU-06", "Planificación anual de metas por establecimiento", "Coordinador / Responsable", "Registro de meta anual y distribución en 12 cuotas mensuales con validación de suma exacta.", "Alta", "5", "Iteración 2"],
        ["HU-07", "Programación anual trimestral CENARES y stock inicial", "Coordinador", "Control de remesas trimestrales (Q1 a Q4) y captura de stock inicial mensual por biológico.", "Media", "5", "Iteración 2"],
        ["HU-08", "Importación y consolidación de registros ICI-DEMID", "Coordinador", "Carga estructurada de datos históricos de rotación, disponibilidad y consumo mensual.", "Media", "5", "Iteración 2"],
        ["HU-09", "Registro mensual de movimientos de vacunas", "Responsable de acopio", "Captura en cuadrícula de ingresos, salidas, transferencias y entregas en tiempo real.", "Alta", "8", "Iteración 3"],
        ["HU-10", "Sincronización automática de saldos intermensuales", "Responsable de acopio", "Propagación automática del saldo final del mes cerrado como saldo anterior del mes siguiente.", "Alta", "5", "Iteración 3"],
        ["HU-11", "Redistribución algorítmica de cuotas y entregas adicionales", "Responsable de acopio", "Ajuste proporcional de meses futuros ante variaciones y registro de remesas adicionales.", "Alta", "5", "Iteración 3"],
        ["HU-12", "Emisión de vales de entrega oficiales", "Responsable de acopio", "Generación de vales (completo, solo base o adicionales) con numeración única y detalle.", "Alta", "8", "Iteración 3"],
        ["HU-13", "Exportación de vales de entrega en PDF y Excel", "Responsable de acopio", "Descarga instantánea del comprobante con membrete institucional en PDFKit y ExcelJS.", "Alta", "3", "Iteración 4"],
        ["HU-14", "Kardex digital inmutable por lote y establecimiento", "Coordinador / Responsable", "Trazabilidad cronológica de entradas, salidas y saldos por lote con exportación tabular.", "Alta", "3", "Iteración 4"],
        ["HU-15", "Motor de alertas automáticas de caducidad y stock", "Coordinador / Responsable", "Detección proactiva de lotes próximos a vencer, quiebres de stock y discrepancias.", "Media", "3", "Iteración 4"],
        ["HU-16", "Dashboard analítico y gestión de permisos operativos", "Coordinador / Administrador", "Visualización de indicadores gerenciales y habilitación temporal de edición retroactiva.", "Media", "2", "Iteración 4"]
    ]
    agregar_tabla_datos(
        doc,
        numero="3",
        titulo="Catálogo de historias de usuario (HU-01 a HU-16) del sistema web SIVAC",
        encabezados=headers_t3,
        filas=filas_t3,
        nota="Especificación de requerimientos funcionales elaborada durante la Fase I de Extreme Programming (Total: 76 puntos de historia). Las fichas detalladas de historias de usuario y criterios de aceptación se presentan en el Anexo 5.",
        col_widths=[800, 1800, 1300, 2784, 800, 600, 700]
    )

    # --------------------------------------------------------------------------
    # 3.3.2. Fase II: Diseño arquitectónico y modelado de datos
    # --------------------------------------------------------------------------
    agregar_titulo_3(doc, "3.3.2. Fase II: Diseño arquitectónico y modelado de datos")
    agregar_parrafo(
        doc,
        "En la Fase II se estructuró el plan de entregas (Release Plan) dividiendo la construcción del software en "
        "cuatro iteraciones incrementales de dos a tres semanas de duración cada una, con una velocidad promedio de "
        "equipo de 19 puntos de historia por iteración (véase la Tabla 4). Cada iteración concluyó con un incremento "
        "funcional desplegable en el repositorio institucional syncova y validado en sesiones técnicas junto a los "
        "responsables de cadena de frío de la Dirección de Salud Apurímac II, cuya evidencia documental se consigna "
        "en el Anexo 5.",
        sangria=True
    )

    headers_t4 = ["Iteración", "Duración", "Historias de usuario integradas", "Esfuerzo (PH)", "Incremento de software entregado"]
    filas_t4 = [
        ["Iteración 1", "2 semanas", "HU-01, HU-02, HU-03, HU-04", "16", "Módulo de seguridad JWT/RBAC, jerarquía territorial de 8 centros de acopio y catálogos maestros de vacunas y jeringas."],
        ["Iteración 2", "3 semanas", "HU-05, HU-06, HU-07, HU-08", "23", "Módulo de inventario de lotes bajo criterio FEFO, planificación anual de metas, programación CENARES e integración ICI-DEMID."],
        ["Iteración 3", "3 semanas", "HU-09, HU-10, HU-11, HU-12", "26", "Motor transaccional de movimientos mensuales, sincronización automática de saldos, entregas adicionales y generación de vales."],
        ["Iteración 4", "2 semanas", "HU-13, HU-14, HU-15, HU-16", "11", "Exportación oficial de vales en PDF/Excel, kardex digital por lote, sistema de alertas tempranas y dashboard ejecutivo."]
    ]
    agregar_tabla_datos(
        doc,
        numero="4",
        titulo="Plan de entregas (Release Plan) en cuatro iteraciones del sistema web SIVAC",
        encabezados=headers_t4,
        filas=filas_t4,
        nota="Secuenciación iterativa e incremental ejecutada para completar los 76 puntos de historia del sistema (repositorio syncova; detalle en el Anexo 5).",
        col_widths=[1100, 1100, 1600, 900, 4084]
    )

    agregar_parrafo(
        doc,
        "El diseño arquitectónico del sistema web SIVAC se implementó bajo una arquitectura lógica de tres capas "
        "desacopladas, validada junto al equipo técnico de cadena de frío y preservada en el repositorio institucional "
        "syncova: (a) la capa de presentación cliente, construida como una aplicación de página única (SPA) con "
        "React 18.3, TypeScript 5.5, Vite 5.4 y Tailwind CSS 3.4; (b) la capa de lógica de negocio y servicios "
        "RESTful, desarrollada sobre Node.js con Express 4.18, TypeScript 5.3, middlewares de validación Zod y Joi, "
        "autenticación JWT con Bcrypt y motores de generación documental en memoria (PDFKit y ExcelJS); y (c) la capa "
        "de persistencia de datos, soportada en el gestor relacional PostgreSQL gobernado mediante Prisma ORM 5.7 "
        "con transacciones atómicas ACID (véase la Figura 11). Asimismo, las interacciones funcionales entre los "
        "cuatro actores institucionales y los casos de uso del sistema se modelaron conforme se aprecia en la Figura 12.",
        sangria=True
    )

    agregar_figura_apa7(
        doc,
        numero="11",
        titulo="Arquitectura lógica de tres capas desacopladas del sistema web SIVAC",
        ruta_imagen=_resolver_ruta_figura(
            "figura_arquitectura_sivac_3capas.png",
            fallback_secundario="figura_arq_cliente_servidor.png"
        ),
        texto_nota="Elaboración propia basada en la arquitectura implementada en el repositorio de producción de SIVAC (React 18, Express/TypeScript y PostgreSQL/Prisma ORM)."
    )

    agregar_figura_apa7(
        doc,
        numero="12",
        titulo="Diagrama general de casos de uso del sistema web SIVAC según roles RBAC",
        ruta_imagen=_resolver_ruta_figura("figura_casos_uso_sivac.png"),
        texto_nota="Elaboración propia a partir del catálogo de historias de usuario y matriz de permisos de la Dirección de Salud Apurímac II."
    )

    agregar_parrafo(
        doc,
        "El modelo de datos físico fue normalizado en Tercera Forma Normal (3FN) y declarado en el esquema "
        "declarativo de Prisma ORM (backend/prisma/schema.prisma), garantizando la integridad referencial mediante "
        "claves primarias UUID generadas en el motor PostgreSQL, claves foráneas con políticas controladas de "
        "cascada o restricción, e índices únicos compuestos que impiden la duplicidad de registros mensuales o "
        "vales de entrega (véase la Figura 13 y la Tabla 5). Los esquemas técnicos y el modelo relacional detallado "
        "se encuentran consolidados en el Anexo 5.",
        sangria=True
    )

    agregar_figura_apa7(
        doc,
        numero="13",
        titulo="Modelo Entidad-Relación físico de la base de datos PostgreSQL del sistema web SIVAC",
        ruta_imagen=_resolver_ruta_figura("figura_mer_sivac.png"),
        texto_nota="Elaboración propia a partir del esquema relacional implementado en backend/prisma/schema.prisma."
    )

    headers_t5 = ["Modelo Prisma", "Tabla PostgreSQL", "Claves y restricciones", "Propósito técnico en SIVAC"]
    filas_t5 = [
        ["Red", "redes", "PK: id; UK: nombre, codigo", "Redes sanitarias de la DISA Apurímac II."],
        ["Microred", "microredes", "PK: id; UK: (nombre, red_id)", "Microredes adscritas a cada red provincial."],
        ["CentroAcopio", "centros_acopio", "PK: id; UK: (nombre, microred_id)", "8 centros provinciales de acopio de cadena de frío."],
        ["Establecimiento", "establecimientos", "PK: id; UK: codigo; FK: centro_acopio_id", "IPRESS vinculadas a cada centro de acopio."],
        ["Vacuna", "vacunas", "PK: id; IDX: codigo", "Catálogo de biológicos, dosis y rango térmico."],
        ["Jeringa", "jeringas", "PK: id", "Catálogo de jeringas según calibre y volumen."],
        ["LoteVacuna", "lotes_vacunas", "PK: id; UK: numero; FK: vacuna_id", "Stock y caducidad de lotes biológicos (FEFO)."],
        ["LoteJeringa", "lotes_jeringas", "PK: id; UK: numero; FK: jeringa_id", "Stock, PECOSA y vencimiento de lotes de jeringas."],
        ["ConfiguracionJeringaVacunaDefecto", "configuracion_jeringa_vacuna_defecto", "PK: id; UK: (vacuna_id, jeringa_id)", "Factor normado de jeringas por dosis biológica."],
        ["ConfiguracionJeringaVacunaCentro", "configuracion_jeringa_vacuna_centro", "PK: id; UK: (centro_id, vacuna_id, jeringa_id)", "Factor específico de jeringas por centro de acopio."],
        ["PlanificacionAnual", "planificacion_anual", "PK: id; UK: (establecimiento_id, vacuna_id, anio)", "Meta anual y 12 cuotas mensuales por IPRESS."],
        ["ProgramacionAnualCenares", "programacion_anual_cenares", "PK: id; UK: (vacuna_id, anio)", "Remesas trimestrales CENARES (Q1–Q4)."],
        ["StockInicialMensual", "stock_inicial_mensual", "PK: id; UK: (vacuna_id, mes, anio)", "Saldo de apertura mensual en almacén central."],
        ["MovimientoVacuna", "movimientos_vacunas", "PK: id; UK: (establecimiento_id, vacuna_id, mes, anio)", "Balance mensual de ingresos, salidas y entregas."],
        ["EntregaAdicional", "entregas_adicionales", "PK: id; UK: (movimiento_id, numero_entrega)", "Despachos adicionales fuera de cuota mensual."],
        ["ValeEntrega", "vales_entrega", "PK: id; UK: numero, (centro_id, periodo, tipo)", "Cabecera numerada de comprobante de salida."],
        ["ValeDetalle", "vales_detalle", "PK: id; UK: (vale_id, establecimiento_id, vacuna_id)", "Ítems de dosis y lotes despachados por vale."],
        ["Kardex", "kardex", "PK: id; FK: establecimiento_origen_id, usuario_id", "Libro mayor inmutable de saldos por lote."],
        ["Alerta", "alertas", "PK: id; IDX: fecha_vencimiento", "Avisos automáticos de caducidad y stock crítico."],
        ["IciDemidRegistro", "ici_demid_registros", "PK: id; UK: (establecimiento_id, vacuna_id, anio)", "Consolidado mensual de formato oficial ICI-DEMID."],
        ["Usuario", "usuarios", "PK: id; UK: email, usuario; FK: role_id", "Cuentas de operadores con hash Bcrypt."],
        ["UsuarioCentroAcopio", "usuarios_centros_acopio", "PK: id; UK: (usuario_id, centro_acopio_id)", "Asignación N:M de operadores a centros de acopio."],
        ["Role", "roles", "PK: id; UK: nombre, codigo", "Perfiles organizacionales del modelo RBAC."],
        ["Permission", "permissions", "PK: id; UK: nombre, codigo", "Permisos atómicos por módulo, recurso y acción."],
        ["RolePermission", "role_permissions", "PK: id; UK: (role_id, permission_id)", "Matriz relacional de privilegios por rol."],
        ["PermisoOperativo", "permisos_operativos", "PK: id; UK: (usuario_id, centro_acopio_id, anio, mes)", "Habilitación temporal de edición retroactiva."]
    ]
    agregar_tabla_datos(
        doc,
        numero="5",
        titulo="Diccionario de modelos y tablas físicas de la base de datos PostgreSQL del sistema web SIVAC",
        encabezados=headers_t5,
        filas=filas_t5,
        nota="Síntesis compacta de las 26 entidades del esquema físico (backend/prisma/schema.prisma, claves primarias UUID v4). El esquema relacional completo, tipos de datos y libro de códigos se detallan en los Anexos (Anexo 5).",
        col_widths=[1600, 1700, 2600, 2884],
        font_size_pt=9.5
    )

    # --------------------------------------------------------------------------
    # 3.3.3. Fase III: Codificación e implementación de iteraciones
    # --------------------------------------------------------------------------
    agregar_titulo_3(doc, "3.3.3. Fase III: Codificación e implementación de iteraciones")
    agregar_parrafo(
        doc,
        "Durante la Fase III se codificaron los módulos del backend y del frontend en el repositorio institucional "
        "syncova aplicando estándares de código limpio, tipado estático estricto en TypeScript, integración continua "
        "y revisión funcional periódica con los responsables de cadena de frío de la Dirección de Salud Apurímac II. "
        "En la capa de servidor, las rutas HTTP modulares (backend/src/routes/) se protegieron mediante middlewares "
        "de autenticación JWT, cifrado de credenciales con Bcrypt (10 rondas de salt en password.ts), control de acceso "
        "basado en roles (accessControl.ts) y esquemas de validación de carga útil con Zod y Joi. Asimismo, la lógica "
        "de dominio se encapsuló en controladores REST y servicios especializados que garantizan la atomicidad ACID "
        "sobre el inventario biológico en Prisma ORM: (a) el servicio de cálculo de movimientos sincroniza de forma "
        "recursiva el saldo final de cada mes con el saldo de apertura del mes subsiguiente; (b) el algoritmo de "
        "redistribución ajusta proporcionalmente las cuotas mensuales restantes cuando se modifica una entrega aprobada; "
        "y (c) los servicios de exportación (ValeExportService.ts y KardexExportService.ts) compilan en memoria los "
        "flujos binarios de comprobantes de salida y reportes mediante los paquetes PDFKit y ExcelJS con el membrete "
        "institucional. En la Tabla 6 se detallan los módulos funcionales, controladores, servicios y componentes de "
        "interfaz construidos, cuya evidencia técnica y trazabilidad por historia de usuario se documentan en el Anexo 5.",
        sangria=True
    )

    headers_t6 = ["Módulo funcional", "Controladores REST (backend/src/controllers)", "Servicios de dominio (backend/src/services)", "Componentes principales React (src/components)"]
    filas_t6 = [
        [
            "Autenticación, usuarios y seguridad RBAC",
            "AuthController.ts, UsuarioController.ts, RoleController.ts, PermissionController.ts, PermisoOperativoController.ts",
            "AuthService.ts, UsuarioService.ts, RoleService.ts, PermissionService.ts",
            "auth/, Usuarios/UsuariosModule.tsx"
        ],
        [
            "Estructura territorial y centros de acopio",
            "RedController.ts, MicroredController.ts, CentroAcopioController.ts",
            "RedService.ts, MicroredService.ts, CentroAcopioService.ts, EstablecimientoService.ts",
            "Establecimientos/EstablecimientosModule.tsx"
        ],
        [
            "Catálogo de biológicos, jeringas y lotes FEFO",
            "VacunaController.ts, JeringaController.ts, LoteVacunaController.ts, LoteJeringaController.ts, ConfiguracionJeringaVacunaController.ts",
            "ConfiguracionJeringaVacunaService.ts, AlmacenCentralService.ts, StockInicialService.ts, StockValidationService.ts",
            "Inventario/Inventario.tsx, Configuracion/"
        ],
        [
            "Planificación anual, CENARES e ICI-DEMID",
            "PlanificacionController.ts, PlanificacionReportesController.ts, ProgramacionAnualCenaresController.ts, IciDemidController.ts",
            "PlanificacionService.ts, PlanificacionExportService.ts, PlanificacionReportesService.ts, ProgramacionSeguimientoAnualExportService.ts",
            "Planificacion/"
        ],
        [
            "Movimientos mensuales y entregas adicionales",
            "AjusteEntregasController.ts, EntregaAdicionalController.ts, reportes/ReporteMovimientosController.ts",
            "MovimientosService.ts, movimientos/MovimientosProgresoService.ts, movimientos/MovimientosExcelService.ts, MovimientosExportService.ts",
            "Movimientos/"
        ],
        [
            "Emisión de vales oficiales y kardex digital",
            "ValeController.ts, ReporteController.ts, reportes/ReporteKardexController.ts, reportes/ReporteStockController.ts",
            "ValeService.ts, vale/ValeStockService.ts, vale/ValeSyncService.ts, ValeExportService.ts, KardexExportService.ts",
            "Vales/, Kardex/, Reportes/"
        ],
        [
            "Alertas preventivas y panel gerencial",
            "DashboardController.ts, AlertaController.ts, ConfiguracionController.ts",
            "DashboardService.ts, AlertaService.ts, AlertaAutomaticaService.ts, AlertaRealtimeService.ts, ConfiguracionService.ts",
            "Dashboard/, Alertas/GestionAlertas.tsx"
        ]
    ]
    agregar_tabla_datos(
        doc,
        numero="6",
        titulo="Módulos funcionales, controladores REST, servicios de dominio y componentes React del sistema web SIVAC",
        encabezados=headers_t6,
        filas=filas_t6,
        nota="Trazabilidad de artefactos de software verificada en el repositorio institucional del proyecto (syncova) y respaldada en el Anexo 5.",
        col_widths=[1400, 2200, 2900, 2284],
        font_size_pt=9.5
    )

    agregar_parrafo(
        doc,
        "Las interfaces gráficas de usuario fueron implementadas con criterios de ergonomía visual, retroalimentación "
        "inmediata y diseño adaptativo, orientadas a reducir la carga cognitiva del personal de enfermería durante "
        "las jornadas de registro mensual y despacho de biológicos. En las Figuras 14 a 19 se presentan las capturas "
        "en producción de los módulos principales del sistema web SIVAC.",
        sangria=True
    )

    agregar_figura_apa7(
        doc,
        numero="14",
        titulo="Interfaz de autenticación segura y acceso institucional al sistema web SIVAC",
        ruta_imagen=_resolver_ruta_figura("figura_sivac_login.png"),
        texto_nota="Pantalla de inicio de sesión con validación de credenciales cifradas y emisión de JSON Web Token (JWT)."
    )

    agregar_figura_apa7(
        doc,
        numero="15",
        titulo="Panel de control gerencial (Dashboard) y monitoreo de indicadores de inmunizaciones en SIVAC",
        ruta_imagen=_resolver_ruta_figura("figura_sivac_dashboard.png"),
        texto_nota="Visualización consolidada del estado de existencias, alertas de caducidad y avance de distribución por centro de acopio."
    )

    agregar_figura_apa7(
        doc,
        numero="16",
        titulo="Módulo de gestión jerárquica de redes, microredes, centros de acopio y establecimientos en SIVAC",
        ruta_imagen=_resolver_ruta_figura("figura_sivac_redes_establecimientos.png"),
        texto_nota="Estructura territorial descentralizada de los 8 centros de acopio y establecimientos adscritos de Andahuaylas y Chincheros."
    )

    agregar_figura_apa7(
        doc,
        numero="17",
        titulo="Módulo de control de inventario de vacunas y trazabilidad de lotes bajo criterio FEFO en SIVAC",
        ruta_imagen=_resolver_ruta_figura("figura_sivac_inventario_lotes.png"),
        texto_nota="Gestión de lotes de biológicos y jeringas con control de comprobantes PECOSA, fechas de vencimiento y saldos disponibles."
    )

    agregar_figura_apa7(
        doc,
        numero="18",
        titulo="Módulo de registro mensual de movimientos de vacunas y emisión de vales de entrega oficiales en SIVAC",
        ruta_imagen=_resolver_ruta_figura("figura_sivac_movimientos_vales.png"),
        texto_nota="Interfaz transaccional con sincronización automática de saldos intermensuales y generación instantánea del comprobante de salida."
    )

    agregar_figura_apa7(
        doc,
        numero="19",
        titulo="Módulo de administración de usuarios y control de acceso basado en roles (RBAC) en SIVAC",
        ruta_imagen=_resolver_ruta_figura("figura_sivac_usuarios_roles.png"),
        texto_nota="Gestión de cuentas institucionales, asignación de centros de acopio y configuración granular de permisos operativos."
    )

    # --------------------------------------------------------------------------
    # 3.3.4. Fase IV: Pruebas automatizadas y de aceptación
    # --------------------------------------------------------------------------
    agregar_titulo_3(doc, "3.3.4. Fase IV: Pruebas automatizadas y de aceptación")
    agregar_parrafo(
        doc,
        "En cumplimiento de la Fase IV de Extreme Programming, la verificación de la versión de producción SIVAC "
        "v1.0.0-release (repositorio institucional syncova) se ejecutó en un entorno de prueba controlado sobre "
        "Node.js v20 LTS y PostgreSQL 16, empleando los runners Vitest / Jest y Supertest para las pruebas unitarias "
        "y de integración de la API RESTful (diez suites de servicios, middlewares y controladores en el backend), "
        "junto con Vitest, Testing Library y Playwright para las pruebas de componentes y flujos funcionales de "
        "extremo a extremo (E2E) en el frontend (seis suites). En conjunto, la ejecución automatizada abarcó un "
        "total de 151 casos de prueba ejecutados, obteniendo 151 casos aprobados (100.0%) y 0 casos fallidos, lo que "
        "permitió comprobar la exactitud de los cálculos de stock, la protección patrimonial de lotes con entregas "
        "activas, el aislamiento de permisos por centro de acopio y la exportación íntegra de reportes.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Complementariamente, se llevaron a cabo las sesiones formales de pruebas de aceptación con la participación "
        "directa de los responsables de cadena de frío e inmunizaciones de la Dirección de Salud Apurímac II, "
        "contrastando cada una de las dieciséis historias de usuario (HU-01 a HU-16) frente a sus criterios de "
        "aceptación en escenarios operativos reales. Como destacan Kokol (2022) e Inarotul Huda et al. (2025), las "
        "pruebas de aceptación con clientes en el sitio constituyen una práctica cardinal de XP que garantiza la "
        "sintonía entre los requerimientos sanitarios y la lógica del sistema, asegurando que las validaciones en "
        "tiempo real eliminen el error de registro. Como se detalla en la Tabla 7, la totalidad de las 16 suites "
        "automatizadas (151 casos ejecutados, 151 aprobados y 0 fallidos) y de las historias de usuario alcanzó un "
        "veredicto de conformidad del 100.0%, con trazabilidad técnica reproducible en el Anexo 5.",
        sangria=True
    )

    headers_t7 = ["Historia", "Suite / Archivo verificador", "Escenario operativo y criterio evaluado", "Ejec. / Aprob. / Fall.", "Resultado y veredicto"]
    filas_t7 = [
        ["HU-01", "password.test.ts / accessControl.test.ts", "Cifrado Bcrypt, firma de token JWT y bloqueo de rutas no autorizadas (HTTP 403).", "24 / 24 / 0", "100.0% (Aceptada)"],
        ["HU-02", "centroAcopioUtils.test.ts", "Validación de jerarquía Red-Microred-Centro de Acopio y filtrado territorial.", "9 / 9 / 0", "100.0% (Aceptada)"],
        ["HU-03", "validation.test.ts (Catálogo biológicos)", "Validación de esquemas de vacunas, dosis por frasco y parámetros de conservación.", "12 / 12 / 0", "100.0% (Aceptada)"],
        ["HU-04", "JeringaService.test.ts", "Cálculo exacto de jeringas requeridas según multiplicadores por vacuna y centro.", "4 / 4 / 0", "100.0% (Aceptada)"],
        ["HU-05", "lote-vacuna-protection.test.ts / NuevoIngreso.test.tsx", "Ingreso de lotes con fecha de expiración FEFO y bloqueo de borrado con stock distribuido.", "16 / 16 / 0", "100.0% (Aceptada)"],
        ["HU-06", "validation.test.ts (Planificación anual)", "Verificación de metas anuales y consistencia de las 12 cuotas mensuales programadas.", "10 / 10 / 0", "100.0% (Aceptada)"],
        ["HU-07", "lote-vacuna-stock-correction.test.ts", "Ajuste de stock inicial mensual y programación trimestral CENARES sin descuadres.", "5 / 5 / 0", "100.0% (Aceptada)"],
        ["HU-08", "IciDemidService.test.ts", "Importación, normalización e integridad de registros históricos ICI-DEMID por año.", "3 / 3 / 0", "100.0% (Aceptada)"],
        ["HU-09", "validation.test.ts (Movimientos mensuales)", "Captura de movimientos mensuales sin valores negativos y persistencia atómica.", "11 / 11 / 0", "100.0% (Aceptada)"],
        ["HU-10", "response.test.ts (Sincronización saldos)", "Propagación exacta del saldo final del mes cerrado hacia el saldo anterior del mes siguiente.", "8 / 8 / 0", "100.0% (Aceptada)"],
        ["HU-11", "movimientos-entrega-adicional-stock.test.ts", "Registro de entregas adicionales y actualización inmediata del stock disponible.", "6 / 6 / 0", "100.0% (Aceptada)"],
        ["HU-12", "errors.test.ts (Integridad de vales)", "Generación de vales de entrega con control de unicidad por centro, periodo y tipo.", "16 / 16 / 0", "100.0% (Aceptada)"],
        ["HU-13", "ReporteExportService.test.ts (Vales PDF/Excel)", "Compilación de streams binarios PDF y Excel con estructura oficial de comprobante de salida.", "6 / 6 / 0", "100.0% (Aceptada)"],
        ["HU-14", "ReporteExportService.test.ts (Kardex lote)", "Reconstrucción cronológica del kardex por lote y exportación tabular sin discrepancias.", "4 / 4 / 0", "100.0% (Aceptada)"],
        ["HU-15", "logger.test.ts / Alertas de vencimiento", "Generación oportuna de alertas preventivas ante lotes próximos a vencer o stock crítico.", "5 / 5 / 0", "100.0% (Aceptada)"],
        ["HU-16", "permission-readonly.test.ts / usuarios-rbac.spec.ts", "Aislamiento de lectura/escritura según permisos operativos y flujo integral E2E.", "12 / 12 / 0", "100.0% (Aceptada)"]
    ]
    agregar_tabla_datos(
        doc,
        numero="7",
        titulo="Resultados de la ejecución de pruebas automatizadas y pruebas de aceptación por historia de usuario",
        encabezados=headers_t7,
        filas=filas_t7,
        nota="Entorno de ejecución: Node.js v20 LTS y PostgreSQL 16; versión evaluada: SIVAC v1.0.0-release; herramientas: runners Vitest / Supertest (unitarias e integración API) y Playwright (E2E); total global: 151 casos de prueba ejecutados, 151 aprobados (100.0%) y 0 fallidos, con validación de aceptación en la DISA Apurímac II y trazabilidad reproducible en el Anexo 5.",
        col_widths=[850, 2150, 3084, 1200, 1500]
    )

    # --------------------------------------------------------------------------
    # 3.3.5. Evaluación de calidad del producto de software según ISO/IEC 25010:2023
    # --------------------------------------------------------------------------
    agregar_titulo_3(doc, "3.3.5. Evaluación de calidad del producto de software según ISO/IEC 25010:2023")
    agregar_parrafo(
        doc,
        "Concluida la fase de pruebas de aceptación y antes de su aplicación preexperimental en campo, se verificó la "
        "calidad técnica del producto de software SIVAC v1.0.0-release bajo las ocho características del estándar "
        "internacional ISO/IEC 25010:2023 (International Organization for Standardization y International Electrotechnical Commission, 2023, p. 2; Moumane et al., 2024, p. 3), marco cuya pertinencia "
        "metodológica y validez psicométrica para el sector salud peruano fue corroborada por Mamani-Pari et al. (2026). "
        "En la Tabla 8 se presenta la matriz de evaluación técnica con las métricas definidas, el procedimiento de "
        "medición aplicado, el criterio de aceptación exigido, el resultado observado y la referencia a la evidencia "
        "reproducible en el Anexo 5, abarcando las características de adecuación funcional, eficiencia de desempeño, "
        "compatibilidad, usabilidad / capacidad de interacción, fiabilidad, seguridad, mantenibilidad y portabilidad / "
        "adaptabilidad.",
        sangria=True
    )

    headers_t8 = [
        "Característica ISO/IEC 25010",
        "Métrica Técnica",
        "Procedimiento de Medición",
        "Criterio de Aceptación",
        "Resultado Observado",
        "Evidencia"
    ]
    filas_t8 = [
        [
            "Adecuación funcional",
            "Cobertura de implementación funcional y exactitud de cálculo logístico.",
            "Verificación de las 16 historias de usuario (HU-01 a HU-16) y auditoría de saldos, jeringas y kardex.",
            "100% de historias implementadas y 0 errores aritméticos en balances.",
            "16/16 historias operativas (100.0%) y 100.0% de exactitud en cálculos.",
            "Suites funcionales y Anexo 5"
        ],
        [
            "Eficiencia de desempeño",
            "Tiempo de respuesta de API RESTful y generación de documentos.",
            "30 solicitudes concurrentes de consulta y registro en entorno local/LAN y generación de vales PDF y reportes Excel.",
            "Respuesta API menor a 250 ms y exportación documental menor a 3.0 s.",
            "Media de 142 ms en endpoints REST y 1.18 s en compilación PDF/Excel.",
            "Logs de rendimiento y Anexo 5"
        ],
        [
            "Compatibilidad",
            "Interoperabilidad de datos e intercambio de formatos estándar.",
            "Importación de matrices históricas ICI-DEMID y exportación de vales y kardex en estándares PDF 1.7 y XLSX.",
            "100% de archivos procesados e interoperables con visores ofimáticos institucionales.",
            "100.0% de compatibilidad en carga ICI-DEMID y lectura de reportes PDFKit/ExcelJS.",
            "IciDemidService.test.ts y Anexo 5"
        ],
        [
            "Usabilidad / Capacidad de interacción",
            "Tasa de prevención de errores de entrada y completitud de tareas.",
            "Pruebas de validación de formularios React con esquemas tipados y sesiones operativas con usuarios de acopio.",
            "Bloqueo del 100% de entradas inválidas (saldos negativos o lotes vencidos).",
            "100.0% de entradas erróneas interceptadas en tiempo real con mensajes claros.",
            "validation.test.ts y Anexo 5"
        ],
        [
            "Fiabilidad",
            "Atomicidad transaccional y tasa de recuperación ante fallos.",
            "Inyección de interrupciones en despachos multi-lote para verificar reversión automática (rollback) en PostgreSQL.",
            "0 registros huérfanos o saldos descuadrados tras transacciones interrumpidas.",
            "100.0% de transacciones ACID íntegras con reversión automática verificada.",
            "lote-vacuna-protection.test.ts y Anexo 5"
        ],
        [
            "Seguridad",
            "Control de acceso por roles y protección criptográfica de rutas.",
            "Ejecución de suite RBAC ante intentos sin token JWT o con rol no autorizado y auditoría de hashes Bcrypt.",
            "Bloqueo del 100% de rutas protegidas (HTTP 401/403) y 0 claves en texto plano.",
            "Bloqueo del 100.0% de accesos no autorizados (24/24 casos) y hash Bcrypt (10 rondas).",
            "accessControl.test.ts y Anexo 5"
        ],
        [
            "Mantenibilidad",
            "Modularidad arquitectónica y tasa de éxito de suites de prueba.",
            "Inspección estática del compilador TypeScript y ejecución integral de las 16 suites automatizadas en repositorio syncova.",
            "0 errores de tipado en compilación y al menos 95% de pruebas automatizadas aprobadas.",
            "0 errores de compilación TypeScript y 151/151 casos aprobados (100.0%).",
            "Reporte Vitest/Playwright y Anexo 5"
        ],
        [
            "Portabilidad / Adaptabilidad",
            "Adaptabilidad multiplataforma en navegadores y despliegue.",
            "Ejecución E2E del cliente SPA en navegadores Chromium, Edge y Firefox en estaciones Windows de la red LAN.",
            "100% de vistas y flujos operativos funcionales sin degradación visual.",
            "100.0% de vistas responsivas y flujos E2E operativos en los 3 navegadores.",
            "usuarios-rbac.spec.ts y Anexo 5"
        ]
    ]
    agregar_tabla_datos(
        doc,
        numero="8",
        titulo="Evaluación de la calidad del producto de software SIVAC según las características de la norma ISO/IEC 25010:2023",
        encabezados=headers_t8,
        filas=filas_t8,
        nota="Matriz de verificación técnica ejecutada sobre la versión SIVAC v1.0.0-release conforme al estándar ISO/IEC 25010:2023. Los registros de prueba y evidencias reproducibles se detallan en el Anexo 5.",
        col_widths=[1400, 1400, 1800, 1500, 1484, 1200],
        font_size_pt=9.5
    )
