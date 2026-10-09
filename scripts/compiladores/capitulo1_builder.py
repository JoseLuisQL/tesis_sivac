#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - ENSAMBLADOR DE INTRODUCCIÓN Y CAPÍTULO I (.DOCX)
Universidad Nacional José María Arguedas (UNAJMA)
Estructura Oficial de Informe Final de Tesis EPIS-UNAJMA
================================================================================
"""

from docx_utilidades import (
    agregar_titulo_1, agregar_titulo_2, agregar_titulo_3,
    agregar_parrafo, agregar_item_lista
)


def construir_introduccion(doc):
    agregar_titulo_1(doc, "INTRODUCCIÓN", page_break=False)

    agregar_parrafo(
        doc,
        "El propósito de esta investigación fue determinar la influencia del sistema web SIVAC "
        "en la mejora de la gestión de movimientos de vacunas en el personal de inmunizaciones "
        "de la Dirección de Salud Apurímac II. La trazabilidad logística de los productos "
        "biológicos constituye un componente crítico para la salud pública, dado que las vacunas "
        "son insumos termolábiles sujetos a estrictos parámetros de conservación térmica entre "
        "+2 °C y +8 °C y a un control administrativo riguroso desde su recepción en los almacenes "
        "centrales hasta su despacho final hacia los establecimientos de salud ejecutores. La "
        "sincronización precisa entre el flujo físico de los lotes biológicos y el respaldo "
        "documental de cada ingreso, transferencia y salida resulta indispensable para prevenir "
        "quiebres de stock, evitar vencimientos por rotación inadecuada y asegurar la cobertura "
        "oportuna del Esquema Nacional de Vacunación.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Previo a la intervención tecnológica ejecutada en el presente estudio, la administración "
        "de movimientos de vacunas en la Dirección de Salud Apurímac II, cuya jurisdicción comprende "
        "las provincias de Andahuaylas y Chincheros a través de ocho centros de "
        "acopio zonales, operaba mediante procedimientos manuales basados en libros físicos de kardex, "
        "formatos impresos de requisición y hojas de cálculo aisladas sin conexión en red. Esta "
        "dependencia del soporte en papel ocasionaba tiempos prolongados en el asentamiento de "
        "transacciones y en la emisión de comprobantes oficiales de salida, frecuentes discrepancias "
        "aritméticas y de codificación entre los saldos registrados y las existencias físicas en "
        "refrigeración, así como una pronunciada sobrecarga operativa e insatisfacción en los "
        "trabajadores responsables de la cadena de frío.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Para resolver dicha problemática operativa, se desarrolló e implementó el sistema web SIVAC "
        "aplicando las cuatro fases iterativas de la metodología ágil Extreme Programming: "
        "planificación, diseño, codificación y pruebas, bajo los estándares de calidad de producto "
        "de software de la norma internacional ISO/IEC 25010:2023. La arquitectura cliente-servidor "
        "desacoplada del sistema automatizó la gestión de movimientos de vacunas articulando tres "
        "dimensiones fundamentales: la oportunidad de procesamiento, medida a través del tiempo de "
        "registro de movimientos y del tiempo de emisión de comprobantes de salida; la consistencia "
        "documental, evaluada mediante el porcentaje de registros sin discrepancias y la concordancia "
        "entre la cantidad programada y la cantidad entregada; y la satisfacción del usuario, "
        "analizada a partir de la aceptación del proceso y la utilidad percibida según el Modelo "
        "de Aceptación Tecnológica.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Metodológicamente, la investigación se ejecutó bajo el enfoque cuantitativo, de tipo "
        "aplicada y nivel explicativo, empleando un diseño preexperimental con pre-test y post-test "
        "en un solo grupo. Se trabajó con una población censal conformada por la totalidad de los "
        "14 operadores de la cadena de inmunizaciones de la Dirección de Salud Apurímac II, "
        "integrada por cuatro especialistas de la sede administrativa central y diez responsables "
        "de los centros de acopio periféricos. Para la recolección de datos empíricos se aplicaron "
        "tres instrumentos: una ficha de observación de tiempos cronometrados, una guía de cotejo "
        "documental de kardex y vales, y un cuestionario psicométrico en escala Likert, los cuales "
        "fueron validados mediante juicio de expertos con el Índice de Validez de Contenido y el "
        "coeficiente V de Aiken, contemplando la prueba de Shapiro-Wilk para el análisis de "
        "normalidad y la prueba de rangos con signo de Wilcoxon para la contrastación de hipótesis.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Finalmente, el estudio consolidó un aporte práctico, metodológico e institucional directo "
        "para la salud pública en el departamento de Apurímac al transformar un proceso logístico "
        "históricamente manual en un flujo digital auditable, centralizado y en tiempo real. En el "
        "plano práctico e institucional, la puesta en producción del sistema web SIVAC dotó a la "
        "Dirección de Salud Apurímac II de una plataforma propia que optimizó el control de lotes "
        "bajo el principio de primero en expirar, primero en salir y transparentó la distribución "
        "interinstitucional de biológicos hacia las microredes de salud; asimismo, en el plano "
        "metodológico, estableció una estructura de medición e instrumentación replicable para "
        "evaluar el impacto de sistemas de información logística sanitaria en redes de salud de "
        "alta dispersión geográfica.",
        sangria=True
    )


def construir_capitulo1(doc):
    agregar_titulo_1(doc, "CAPÍTULO I: PROBLEMA DE INVESTIGACIÓN")

    # 1.1. Descripción de la realidad problemática
    agregar_titulo_2(doc, "1.1. Descripción de la realidad problemática")

    agregar_parrafo(
        doc,
        "A escala global, el fortalecimiento de la cadena de suministro de productos biológicos "
        "representa un imperativo estratégico para garantizar la eficacia de los programas de "
        "inmunización y reducir la morbimortalidad por enfermedades prevenibles por vacunación "
        "(World Health Organization [WHO], 2021). Las vacunas constituyen preparados biológicos "
        "termolábiles cuya potencia inmunogénica depende tanto de la preservación ininterrumpida "
        "de la cadena de frío entre +2 °C y +8 °C como de la exactitud y velocidad del flujo de "
        "información logística que respalda su recepción, almacenamiento, distribución y despacho "
        "(Organización Panamericana de la Salud [OPS] y PATH, 2020; Brooks et al., 2024). Sin "
        "embargo, en numerosos sistemas de salud de ingresos bajos y medianos persiste el uso de "
        "formatos manuales en soporte de papel y hojas de cálculo desconectadas, lo cual fragmenta "
        "la trazabilidad de los lotes, retrasa la consolidación de saldos y dificulta la toma de "
        "decisiones oportunas ante emergencias sanitarias (OPS y PATH, 2020).",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Diversas investigaciones internacionales evidenciaron las limitaciones críticas asociadas "
        "a la gestión manual y deficitaria de registros en los almacenes de salud pública. En un "
        "estudio sobre sistemas de información sanitaria rutinaria en centros de salud de Etiopía, "
        "Chekol et al. (2023, p. 9) determinaron que el nivel general de calidad y concordancia "
        "documental de los datos apenas alcanzó el 74%, identificando la complejidad de los "
        "formatos impresos y la ausencia de validación automatizada como los factores determinantes "
        "del error administrativo. De manera convergente, Mekonen et al. (2024, p. 375) evaluaron "
        "el desempeño del sistema de información de gestión logística de vacunas en establecimientos "
        "públicos de la región de Amhara y comprobaron que la escasez de herramientas digitales "
        "estandarizadas restringió la exactitud de los reportes de existencias biológicas y elevó "
        "la carga operativa del personal sanitario. En la misma línea, Ergetie et al. (2023, p. 7) "
        "constataron que las deficiencias en el registro sistemático de movimientos e inventarios "
        "en la cadena de frío primaria limitaron la disponibilidad verificable de vacunas esenciales.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "En contrapartida, la literatura científica internacional demostró que la adopción de "
        "plataformas digitales y sistemas web especializados revierte de forma sustancial estas "
        "deficiencias operativas y documentales. Shen et al. (2024, p. 1), al evaluar la "
        "implementación de un sistema digital de gestión de cadena de suministro hospitalaria en "
        "China, verificaron que la tasa de roturas de stock se redujo de 0.425% a 0.277% y que la "
        "eficiencia operativa global se incrementó de manera significativa gracias al control "
        "automatizado de inventarios. Asimismo, Dang et al. (2024), en un estudio longitudinal sobre "
        "la transición del registro en papel hacia un sistema nacional de inmunización digital en "
        "Vietnam, comprobaron que el tiempo transcurrido hasta la disponibilidad efectiva del dato "
        "disminuyó de 43.7 a 0.7 días (reducción del 98%) y que la carga administrativa del "
        "personal se redujo en un 38%. Resultados equivalentes fueron reportados por Kigenza et al. "
        "(2023) en Ruanda y por Wasswa et al. (2023) en Uganda, quienes demostraron que la "
        "operación de sistemas electrónicos de gestión logística incrementó la exactitud de los "
        "inventarios del 25% al 85% y aseguró una disponibilidad promedio del 90% en hospitales "
        "regionales de referencia, mientras que en el contexto sudamericano Balón Morejón "
        "(2023, p. xii) acreditó que una aplicación web de inventario vacunal en Ecuador redujo "
        "la emisión de reportes de varios días a segundos.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "En el ámbito nacional peruano, la gestión técnica y administrativa de los productos "
        "biológicos se rige por la Norma Técnica de Salud NTS N° 196-MINSA/DGIESP-2022, aprobada "
        "mediante Resolución Ministerial N° 884-2022/MINSA, la cual establece la obligatoriedad "
        "de mantener actualizado el control de stock por tipo de vacuna, número de lote y fecha "
        "de expiración mediante el registro en kardex y la emisión de comprobantes oficiales de "
        "salida en todas las dependencias de salud (Ministerio de Salud [MINSA], 2022). Pese a "
        "las exigencias de dicho marco regulatorio (MINSA, 2022), en los niveles regionales y "
        "locales del país subsiste una marcada brecha tecnológica en el control logístico interno "
        "de los almacenes de inmunizaciones. Al respecto, Mego Navarro (2021, p. 32) identificó "
        "en una entidad pública de salud que el 45% de los operadores aún recababa información "
        "de vacunas desplazándose físicamente a los centros de salud y que el 25% de los reportes "
        "presentaba datos incompletos por carecer de un sistema web centralizado.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "De igual modo, Champi Velásquez (2023, p. 14) advirtió que en los servicios públicos de "
        "inmunizaciones del país la supervisión manual de la cadena de frío y del inventario de "
        "biológicos expone los lotes a riesgos de deterioro y pérdida de trazabilidad por demoras "
        "en la detección de incidencias y en la actualización de registros físicos. A su vez, "
        "Alvarez Ticllasuca et al. (2023, p. 72) demostraron en establecimientos de salud de la "
        "región central del Perú que la incorporación de sistemas de información automatizados "
        "elevó la eficacia del control de inmunizaciones del 25.9% al 77.8%, confirmando la "
        "necesidad de sustituir los registros tradicionales en papel. En concordancia con ello, "
        "Garcia Villacorta y Calderón Huaman (2023) evidenciaron que la ausencia de una plataforma "
        "web de inventarios genera desfases críticos entre el stock físico y el contable, y que "
        "su implementación permite elevar la exactitud del control de existencias de 75.42% a "
        "97.18%, optimizando la concordancia de las entregas programadas.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "En el contexto local de la Dirección de Salud Apurímac II (DISA Apurímac II), con sede "
        "institucional en la ciudad de Andahuaylas, la Estrategia Sanitaria Nacional de "
        "Inmunizaciones administra el abastecimiento y la distribución de vacunas hacia ocho "
        "centros de acopio y cabeceras de microred desplegados en las provincias de Andahuaylas "
        "y Chincheros. Este flujo operativo recayó sobre una dotación censal de 14 trabajadores "
        "(cuatro profesionales en la sede administrativa central y diez responsables de cadena de "
        "frío en los centros de acopio periféricos), quienes ejecutaban de manera manual el "
        "asentamiento de ingresos, transferencias, saldos de kardex y vales de despacho. En primer "
        "término, esta modalidad tradicional afectó severamente la oportunidad de procesamiento, "
        "dado que la transcripción manual en cuadernos físicos y hojas de cálculo locales demandaba "
        "tiempos excesivos tanto para registrar cada movimiento de lote como para verificar y "
        "emitir los comprobantes oficiales de salida hacia las microredes.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "En segundo término, se verificaron deficiencias recurrentes en la consistencia documental, "
        "expresadas en errores de transcripción de códigos alfanuméricos de lote, omisión de fechas "
        "de caducidad, discrepancias entre los saldos asentados en los libros de kardex y las "
        "existencias reales en los equipos frigoríficos, así como discordancias entre las "
        "cantidades programadas por las microredes y las dosis efectivamente entregadas. En tercer "
        "término, la duplicidad de tareas mecánicas de conciliación mensual y la incertidumbre "
        "frente a las auditorías sanitarias deterioraron la satisfacción del usuario en los 14 "
        "operadores institucionales, generando agotamiento administrativo y baja aceptación del "
        "proceso manual. Frente a esta realidad problemática, se desarrolló e implementó el "
        "sistema web SIVAC bajo la metodología ágil Extreme Programming y el estándar ISO/IEC "
        "25010:2023, con el fin de automatizar y centralizar la gestión de movimientos de vacunas "
        "en la Dirección de Salud Apurímac II.",
        sangria=True
    )

    # 1.2. Formulación del problema
    agregar_titulo_2(doc, "1.2. Formulación del problema")

    agregar_titulo_3(doc, "1.2.1. Problema general")
    agregar_parrafo(
        doc,
        "¿En qué medida la aplicación del sistema “SIVAC” mejora la gestión de movimientos de "
        "vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?",
        sangria=True
    )

    agregar_titulo_3(doc, "1.2.2. Problemas específicos")
    problemas_esp = [
        "¿En qué medida la aplicación del sistema “SIVAC” mejora la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?",
        "¿En qué medida la aplicación del sistema “SIVAC” mejora la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?",
        "¿En qué medida la aplicación del sistema “SIVAC” mejora la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?"
    ]
    for pe in problemas_esp:
        agregar_item_lista(doc, pe, simbolo="•")

    # 1.3. Justificación de la investigación
    agregar_titulo_2(doc, "1.3. Justificación de la investigación")

    agregar_titulo_3(doc, "1.3.1. Justificación teórica")
    agregar_parrafo(
        doc,
        "El presente estudio se justificó teóricamente porque articuló los principios de la "
        "ingeniería de software ágil, la calidad de producto informático y la psicometría de "
        "adopción tecnológica aplicados a la logística sanitaria de inmunizaciones. En el ámbito "
        "del desarrollo de software, la investigación corroboró la eficacia de la metodología "
        "Extreme Programming formulada por Beck (1999, p. 71) para construir sistemas transaccionales "
        "mediante entregas incrementales y retroalimentación continua en entornos públicos con "
        "reglas operativas estrictas. Asimismo, el estudio aplicó el modelo de calidad de producto "
        "establecido por la International Organization for Standardization e International "
        "Electrotechnical Commission [ISO/IEC] (2023, p. 2) a través de la norma ISO/IEC 25010:2023, "
        "sustentando cómo la adecuación funcional, la eficiencia de desempeño y la capacidad de "
        "interacción inciden en la oportunidad de procesamiento y en la consistencia documental "
        "de los inventarios biológicos. De igual forma, validó empíricamente los constructos de "
        "utilidad percibida y facilidad de uso percibida del Modelo de Aceptación Tecnológica "
        "propuesto por Davis (1989, p. 320) para explicar la satisfacción del personal sanitario.",
        sangria=True
    )

    agregar_titulo_3(doc, "1.3.2. Justificación práctica")
    agregar_parrafo(
        doc,
        "En el plano práctico, la investigación se justificó al resolver de manera directa las "
        "deficiencias operativas del registro manual de biológicos en la Dirección de Salud "
        "Apurímac II mediante la puesta en operación del sistema web SIVAC. La herramienta "
        "implementada permitió a los 14 operadores de la estrategia sanitaria y de los ocho "
        "centros de acopio automatizar el asentamiento de entradas, salidas y transferencias, "
        "actualizar en tiempo real los saldos del kardex digital por lote y fecha de caducidad, "
        "y generar comprobantes oficiales de salida en lapsos mínimos. Con ello se eliminaron las "
        "discrepancias aritméticas en las conciliaciones mensuales y se redujo sustancialmente la "
        "carga administrativa del personal de cadena de frío.",
        sangria=True
    )

    agregar_titulo_3(doc, "1.3.3. Justificación metodológica")
    agregar_parrafo(
        doc,
        "Desde la perspectiva metodológica, el estudio se justificó porque estructuró y ejecutó "
        "un diseño preexperimental con pre-test y post-test en un solo grupo bajo los lineamientos "
        "del enfoque cuantitativo de Hernández-Sampieri et al. (2014, p. 141), adaptado a una "
        "población censal de 14 operadores especializados. Asimismo, la investigación diseñó y "
        "sometió a validación rigurosa por juicio de expertos tres instrumentos de medición "
        "específicos para evaluar el flujo de vacunas (una ficha de observación de tiempos "
        "cronometrados, una guía de cotejo de ocho criterios normativos de integridad documental "
        "y un cuestionario psicométrico de satisfacción), cuya validez de contenido se determinó "
        "mediante el modelo modificado por Tristán-López (2008, p. 38) y el coeficiente V de Aiken, "
        "constituyendo un referente metodológico verificable para futuras investigaciones en "
        "informática biomédica y gestión pública.",
        sangria=True
    )

    agregar_titulo_3(doc, "1.3.4. Justificación social")
    agregar_parrafo(
        doc,
        "En el ámbito social, la investigación se justificó por su contribución directa a la "
        "protección de la salud colectiva en las provincias de Andahuaylas y Chincheros. Al "
        "garantizar la oportunidad en el despacho de biológicos y la exactitud documental de los "
        "lotes distribuidos desde la sede central de la Dirección de Salud Apurímac II hacia los "
        "ocho centros de acopio y establecimientos periféricos, el estudio coadyuvó a asegurar "
        "la disponibilidad oportuna y la conservación íntegra de las vacunas destinadas a niños "
        "menores de cinco años, gestantes, adultos mayores y poblaciones vulnerables de las "
        "comunidades rurales andinas, reduciendo el riesgo de desabastecimiento y de pérdida de "
        "dosis por caducidad.",
        sangria=True
    )

    agregar_titulo_3(doc, "1.3.5. Justificación tecnológica")
    agregar_parrafo(
        doc,
        "Tecnológicamente, el estudio se justificó al modernizar la infraestructura informática "
        "del área de inmunizaciones de la Dirección de Salud Apurímac II mediante una arquitectura "
        "web cliente-servidor desacoplada, construida con tecnologías modernas de código abierto, "
        "servicios de interfaz de programación de aplicaciones bajo estilo REST, persistencia "
        "relacional transaccional y autenticación segura basada en tokens criptográficos y control "
        "de acceso por roles. Esta solución reemplazó el uso de archivos locales aislados por "
        "una plataforma centralizada accesible desde cualquier centro de acopio autorizado, "
        "implementando algoritmos de priorización de lotes próximos a vencer y validaciones "
        "automáticas de integridad referencial.",
        sangria=True
    )

    # 1.4. Objetivos de la investigación
    agregar_titulo_2(doc, "1.4. Objetivos de la investigación")

    agregar_titulo_3(doc, "1.4.1. Objetivo general")
    agregar_parrafo(
        doc,
        "Determinar en qué medida la aplicación del sistema “SIVAC” mejora la gestión de "
        "movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud "
        "Apurímac II.",
        sangria=True
    )

    agregar_titulo_3(doc, "1.4.2. Objetivos específicos")
    objetivos_esp = [
        "Determinar en qué medida la aplicación del sistema “SIVAC” mejora la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.",
        "Determinar en qué medida la aplicación del sistema “SIVAC” mejora la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.",
        "Determinar en qué medida la aplicación del sistema “SIVAC” mejora la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II."
    ]
    for oe in objetivos_esp:
        agregar_item_lista(doc, oe, simbolo="•")

    # 1.5. Limitaciones de la investigación
    agregar_titulo_2(doc, "1.5. Limitaciones de la investigación")
    agregar_parrafo(
        doc,
        "Durante el desarrollo y ejecución del estudio en la Dirección de Salud Apurímac II se "
        "identificaron limitaciones de índole geográfica, tecnológica, operativa y muestral que "
        "fueron controladas dentro del alcance metodológico de la investigación. En primer lugar, "
        "la dispersión geográfica de los ocho centros de acopio en las provincias de Andahuaylas "
        "y Chincheros conllevó fluctuaciones temporales en el ancho de banda de internet en "
        "establecimientos periféricos; esta condición se superó optimizando la ligereza de las "
        "peticiones de datos del sistema web SIVAC y el manejo transaccional en el navegador. "
        "En segundo lugar, se presentó una resistencia inicial al cambio por parte de operadores "
        "habituados al llenado manual de libros físicos de kardex, la cual fue mitigada mediante "
        "jornadas presenciales de capacitación práctica y el diseño de interfaces intuitivas con "
        "validación preventiva de errores conforme al estándar ISO/IEC 25010:2023.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "En tercer lugar, en cuanto al alcance funcional y temático, la investigación se "
        "circunscribió exclusivamente a la gestión logística de movimientos de vacunas en sus "
        "tres dimensiones de estudio: oportunidad de procesamiento, consistencia documental y "
        "satisfacción del usuario, sin abarcar el registro nominal clínico de pacientes vacunados "
        "ni la gestión presupuestal financiera, los cuales corresponden a plataformas nacionales "
        "externas. Finalmente, dado que el universo institucional del personal responsable de "
        "inmunizaciones y cadena de frío de la Dirección de Salud Apurímac II estuvo constituido "
        "de forma íntegra por 14 servidores públicos, el tamaño de la población censal determinó "
        "la evaluación previa de los supuestos distribucionales mediante la prueba de Shapiro-Wilk "
        "para muestras pequeñas y la aplicación de la prueba no paramétrica de rangos con signo "
        "de Wilcoxon para garantizar el rigor inferencial de los resultados.",
        sangria=True
    )
