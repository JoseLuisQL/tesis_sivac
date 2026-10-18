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
        "El propósito de esta investigación fue determinar en qué medida la aplicación del sistema web SIVAC "
        "mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud "
        "Apurímac II, evaluando los cambios observados antes y después de la intervención tecnológica. La "
        "trazabilidad logística de los productos biológicos constituye un componente crítico para la salud "
        "pública, dado que las vacunas son insumos termolábiles sujetos a estrictos parámetros de conservación "
        "térmica entre +2 °C y +8 °C y a un control administrativo riguroso desde su recepción en los almacenes "
        "centrales hasta su despacho final hacia los establecimientos de salud ejecutores. La sincronización "
        "precisa entre el flujo físico de los lotes biológicos y el respaldo documental de cada ingreso, "
        "transferencia y salida resulta indispensable para prevenir quiebres de stock, evitar vencimientos por "
        "rotación inadecuada y asegurar la cobertura oportuna del Esquema Nacional de Vacunación.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Previo a la intervención tecnológica ejecutada en el presente estudio, la administración de movimientos "
        "de vacunas en la Dirección de Salud Apurímac II (en adelante, DISA Apurímac II), cuya jurisdicción "
        "comprende las provincias de Andahuaylas y Chincheros a través de ocho centros de acopio (el almacén "
        "especializado de la sede central y los centros de acopio vinculados a las redes y microredes de salud), "
        "operaba mediante procedimientos manuales basados en libros físicos de kardex, formatos impresos de "
        "requisición y hojas de cálculo aisladas sin conexión en red. Esta dependencia del soporte en papel "
        "ocasionaba tiempos prolongados en el asentamiento de transacciones y en la emisión de vales de salida "
        "(equivalentes institucionalmente a comprobantes de salida o entrega), frecuentes discrepancias "
        "aritméticas y de codificación entre los saldos registrados y las existencias físicas en refrigeración, "
        "así como una pronunciada sobrecarga operativa e insatisfacción en los trabajadores responsables de la "
        "cadena de frío.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Para atender dicha problemática operativa, se desarrolló e implementó el sistema web SIVAC aplicando las "
        "cuatro fases iterativas de la metodología ágil Extreme Programming: planificación, diseño, codificación "
        "y pruebas, verificando sus atributos de calidad técnica bajo la norma internacional ISO/IEC 25010:2023. "
        "La arquitectura cliente-servidor desacoplada del sistema se diseñó para sistematizar la gestión de "
        "movimientos de vacunas articulando tres dimensiones fundamentales: la oportunidad de procesamiento, "
        "medida a través del tiempo de registro de movimientos y del tiempo de emisión de vales de salida; la "
        "consistencia documental, evaluada mediante el porcentaje de registros sin discrepancias y la concordancia "
        "entre la cantidad programada y la cantidad entregada; y la satisfacción del usuario, analizada a partir "
        "de la aceptación del proceso y la utilidad percibida según el Modelo de Aceptación Tecnológica.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Metodológicamente, la investigación se estructuró bajo el enfoque cuantitativo, de tipo aplicada y nivel "
        "explicativo, empleando un diseño preexperimental con pre-test y post-test en un solo grupo (GE: O₁ – X – O₂). "
        "Se trabajó con una población censal conformada por la totalidad de los 14 operadores de la cadena de "
        "inmunizaciones de la DISA Apurímac II (N = n = 14), integrada por cuatro especialistas de la sede "
        "administrativa central y diez responsables de los centros de acopio periféricos. Para la recolección de "
        "datos empíricos se diseñaron tres instrumentos: una ficha de observación de tiempos cronometrados, una "
        "guía de cotejo documental de kardex y vales de salida, y un cuestionario psicométrico en escala Likert, "
        "los cuales serán sometidos a validación de contenido por juicio de tres expertos de la EPIS-UNAJMA "
        "conforme al procedimiento descrito en el Capítulo IV, contemplando la prueba de Shapiro-Wilk para el "
        "análisis de normalidad y la prueba de rangos con signo de Wilcoxon (α = 0.05) para la contrastación de "
        "hipótesis.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Finalmente, el estudio configuró un aporte práctico, metodológico e institucional directo para la gestión "
        "sanitaria en el departamento de Apurímac al estructurar la transición de un proceso logístico "
        "históricamente manual hacia un flujo digital auditable y centralizado. La implementación del sistema web "
        "SIVAC tuvo como propósito proporcionar a la Dirección de Salud Apurímac II (en adelante, DISA Apurímac II) "
        "una plataforma tecnológica propia para centralizar el control de lotes, automatizar el kardex y fortalecer "
        "la trazabilidad documental de los movimientos de vacunas hacia las redes y microredes de salud; asimismo, "
        "en el plano metodológico, estableció una estructura de medición e instrumentación replicable para evaluar "
        "intervenciones de sistemas de información logística sanitaria en redes de salud de alta dispersión "
        "geográfica.",
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
        "decisiones oportunas ante emergencias sanitarias (Organización Panamericana de la Salud y PATH, 2020).",
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
        "plataformas digitales y sistemas web especializados atenúa de forma sustancial estas "
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
        "biológicos se rige por la Norma Técnica de Salud NTS N.° 196-MINSA/DGIESP-2022, aprobada "
        "mediante Resolución Ministerial N.° 884-2022/MINSA, la cual establece la obligatoriedad "
        "de mantener actualizado el control de stock por tipo de vacuna, número de lote y fecha "
        "de expiración mediante el registro en kardex y la emisión de vales de salida (equivalentes "
        "institucionalmente a comprobantes de salida o entrega) en todas las dependencias de salud "
        "(Ministerio de Salud, 2022). Pese a las exigencias de dicho marco regulatorio "
        "(Ministerio de Salud, 2022), en los niveles regionales y locales del país subsiste una marcada brecha "
        "tecnológica y de infraestructura en el control logístico de los almacenes de inmunizaciones. "
        "Esta problemática fue constatada por Gutiérrez-Aguado et al. (2024, pp. 73–78) en su "
        "evaluación nacional de la cadena de frío del MINSA, donde determinaron que apenas el 38.2% "
        "de los equipos de refrigeración contaba con una antigüedad menor a diez años (registrando "
        "un 61.8% de obsolescencia que superó el 80% en las regiones del interior del país) y "
        "evidenciaron profundos desfases entre los inventarios patrimoniales oficiales del módulo "
        "SIGA-MEF y las existencias reales reportadas en los almacenes locales, lo cual compromete "
        "la planificación de suministros y eleva el riesgo de pérdida biológica por falta de "
        "herramientas digitales ágiles. Al respecto, Mego Navarro (2021, p. 32) identificó en una "
        "entidad pública de salud que el 45% de los operadores aún recababa información de vacunas "
        "desplazándose físicamente a los centros de salud y que el 25% de los reportes presentaba "
        "datos incompletos por carecer de un sistema web centralizado.",
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
        "En el contexto local de la Dirección de Salud Apurímac II (en adelante, DISA Apurímac II), "
        "con sede institucional en la ciudad de Andahuaylas, la Estrategia Sanitaria Nacional de "
        "Inmunizaciones administra el abastecimiento y la distribución de vacunas hacia ocho "
        "centros de acopio, los cuales comprenden el almacén especializado de la sede central y los "
        "centros de acopio vinculados a las redes y microredes de salud de las provincias de "
        "Andahuaylas y Chincheros. Este flujo operativo recae sobre una dotación censal de 14 "
        "trabajadores (cuatro profesionales en la sede administrativa central y diez responsables "
        "de cadena de frío en los centros de acopio periféricos), quienes ejecutaban de manera "
        "manual el asentamiento de ingresos, transferencias, saldos de kardex y vales de salida. "
        "En primer término, esta modalidad tradicional afectó la oportunidad de procesamiento, "
        "dado que la transcripción manual en cuadernos físicos y hojas de cálculo locales demandaba "
        "tiempos prolongados tanto para registrar cada movimiento de lote como para verificar y "
        "emitir los vales de salida hacia las microredes.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "En el diagnóstico documental preliminar efectuado en la cadena de frío de la DISA Apurímac II "
        "durante la línea base pre-intervención, la inspección de los libros de kardex manuscrito y "
        "talonarios de vales de salida correspondientes al periodo basal [Pendiente de consignar volumen "
        "exacto de registros basales] evidenció demoras operativas recurrentes en la transcripción manual "
        "y en la conciliación mensual de saldos, así como observaciones de completitud documental que "
        "sustentaron la necesidad de implementar una solución digital centralizada.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "En segundo término, se identificaron deficiencias recurrentes en la consistencia documental, "
        "expresadas en errores de transcripción de códigos alfanuméricos de lote, omisión de fechas "
        "de caducidad, discrepancias entre los saldos asentados en los libros de kardex y las "
        "existencias reales en los equipos frigoríficos, así como discordancias entre las "
        "cantidades programadas por las microredes y las dosis efectivamente entregadas en los vales "
        "de salida. En tercer término, la duplicidad de tareas mecánicas de conciliación mensual y la "
        "incertidumbre frente a las auditorías sanitarias afectaron la satisfacción del usuario en los "
        "14 operadores institucionales, generando sobrecarga administrativa y baja aceptación del "
        "proceso manual. Frente a esta realidad problemática, se desarrolló e implementó el "
        "sistema web SIVAC bajo la metodología ágil Extreme Programming y el estándar ISO/IEC "
        "25010:2023, con el propósito de reducir las discrepancias documentales, disminuir la "
        "probabilidad de errores de transcripción e incorporar controles preventivos frente a "
        "inconsistencias en la gestión de movimientos de vacunas en la DISA Apurímac II.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Para efectos de esta investigación, la variable dependiente gestión de movimientos de vacunas "
        "comprende exclusivamente el registro, validación, trazabilidad documental y emisión de vales de "
        "salida vinculados a los ingresos, salidas, transferencias y saldos de biológicos en los ocho "
        "centros de acopio de la DISA Apurímac II. La conservación termodinámica de los equipos "
        "frigoríficos, el acto clínico de vacunación nominal de pacientes y la ejecución presupuestal no "
        "forman parte de la variable evaluada.",
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
        "ingeniería de software ágil, la calidad de producto informático y la evaluación de "
        "aceptación tecnológica aplicados a la logística sanitaria de inmunizaciones. En el ámbito "
        "del desarrollo de software, la investigación empleó la metodología Extreme Programming "
        "formulada por Beck (1999, p. 71) como marco de ingeniería de software para construir "
        "sistemas transaccionales mediante entregas incrementales y retroalimentación continua en "
        "entornos públicos con reglas operativas estrictas. Asimismo, el estudio aplicó el modelo "
        "de calidad de producto establecido por la International Organization for Standardization e "
        "International Electrotechnical Commission [ISO/IEC] (2023, p. 2) a través de la norma "
        "ISO/IEC 25010:2023, sustentando cómo la adecuación funcional, la eficiencia de desempeño "
        "y la capacidad de interacción se vinculan con la oportunidad de procesamiento y la "
        "consistencia documental de los inventarios biológicos. De igual forma, el estudio empleó "
        "el Modelo de Aceptación Tecnológica (TAM) propuesto por Davis (1989, p. 320), articulado "
        "con la literatura de éxito de sistemas de información, como referente evaluativo de la "
        "percepción del usuario a través de la utilidad percibida y la facilidad de uso percibida "
        "en el personal sanitario, sin pretender validar el modelo TAM como teoría general.",
        sangria=True
    )

    agregar_titulo_3(doc, "1.3.2. Justificación práctica")
    agregar_parrafo(
        doc,
        "En el plano práctico, la investigación se justificó al abordar de manera directa las "
        "deficiencias operativas del registro manual de biológicos en la DISA Apurímac II mediante "
        "el desarrollo y despliegue del sistema web SIVAC. La herramienta implementada proporcionó "
        "a los 14 operadores de la estrategia sanitaria y de los ocho centros de acopio módulos "
        "para sistematizar el asentamiento de entradas, salidas y transferencias, actualizar en "
        "tiempo real los saldos del kardex digital por lote y fecha de caducidad, y generar vales "
        "de salida estandarizados. Con ello se buscó reducir las discrepancias aritméticas en las "
        "conciliaciones mensuales y disminuir la carga administrativa asociada al registro manual.",
        sangria=True
    )

    agregar_titulo_3(doc, "1.3.3. Justificación metodológica")
    agregar_parrafo(
        doc,
        "Desde la perspectiva metodológica, el estudio se justificó porque estructuró un diseño "
        "preexperimental con pre-test y post-test en un solo grupo (GE: O₁ – X – O₂) bajo los "
        "lineamientos del enfoque cuantitativo de Hernández-Sampieri et al. (2014, p. 141), "
        "adaptado a una población censal de 14 operadores especializados (N = n = 14). Asimismo, la "
        "investigación diseñó tres instrumentos de medición específicos para evaluar el flujo de "
        "movimientos de vacunas (una ficha de observación de tiempos cronometrados, una guía de "
        "cotejo de ocho criterios normativos de integridad documental y un cuestionario psicométrico "
        "de satisfacción), estableciendo una distinción rigurosa entre: (a) la validez de contenido, "
        "cuya estimación se realizará mediante juicio de tres expertos aplicando el modelo modificado "
        "por Tristán-López (2008, p. 38), del que se derivan el coeficiente V de Aiken y el Índice de "
        "Validez de Contenido (IVC), a los que esa fuente no asocia un umbral de aceptación de 0.80. "
        "Este estudio adopta de manera expresa el valor de 0.80 como criterio propio de aceptación "
        "para ambos coeficientes; (b) la confiabilidad por consistencia interna, estimada mediante el coeficiente "
        "Alfa de Cronbach por subescala para el cuestionario psicométrico TAM; y (c) la objetividad "
        "procedimental y concordancia interevaluador, garantizadas mediante un protocolo "
        "estandarizado de observación con disparadores unívocos y el coeficiente Kappa de Cohen "
        "para las fichas de tiempos y la guía de cotejo documental.",
        sangria=True
    )

    agregar_titulo_3(doc, "1.3.4. Justificación social")
    agregar_parrafo(
        doc,
        "En el ámbito social, la investigación se justificó por su contribución a la gestión "
        "oportuna del suministro de inmunizaciones en beneficio de la salud colectiva en las "
        "provincias de Andahuaylas y Chincheros. Al fortalecer el control en el despacho de "
        "biológicos y la trazabilidad documental de los lotes distribuidos desde el almacén "
        "especializado de la sede central de la DISA Apurímac II hacia los centros de acopio de "
        "las redes y microredes de salud, el estudio coadyuvó a respaldar la disponibilidad "
        "oportuna de las vacunas destinadas a niños menores de cinco años, gestantes, adultos "
        "mayores y poblaciones vulnerables de las comunidades rurales andinas, disminuyendo el "
        "riesgo de desabastecimiento y de pérdida de dosis por caducidad.",
        sangria=True
    )

    agregar_titulo_3(doc, "1.3.5. Justificación tecnológica")
    agregar_parrafo(
        doc,
        "Tecnológicamente, el estudio se justificó al modernizar la infraestructura informática "
        "del área de inmunizaciones de la DISA Apurímac II mediante una arquitectura web "
        "cliente-servidor desacoplada, construida con tecnologías de código abierto, servicios de "
        "interfaz de programación de aplicaciones bajo estilo REST, persistencia relacional "
        "transaccional y autenticación segura basada en tokens criptográficos y control de acceso "
        "por roles. Esta solución permitió sustituir el uso de archivos locales aislados por una "
        "plataforma centralizada accesible desde los ocho centros de acopio autorizados, "
        "incorporando controles preventivos frente a inconsistencias y reglas de priorización de "
        "lotes próximos a vencer.",
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

    # 1.5. Hipótesis de la investigación
    agregar_titulo_2(doc, "1.5. Hipótesis de la investigación")

    agregar_titulo_3(doc, "1.5.1. Hipótesis general")
    agregar_parrafo(
        doc,
        "La aplicación del sistema web SIVAC mejora significativamente la gestión de movimientos de "
        "vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, evidenciada "
        "de manera integrada a través de la reducción de los tiempos de procesamiento, el incremento "
        "de la consistencia documental y el incremento de la satisfacción y aceptación del sistema "
        "por el usuario.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "En atención a que la variable dependiente se encuentra conformada por indicadores medidos en "
        "escalas heterogéneas (minutos cronometrados, porcentajes de conformidad documental y puntajes "
        "ordinales en escala Likert), la contrastación empírica de la hipótesis general se determina "
        "mediante la integración inferencial conjunta de las tres hipótesis específicas (H1, H2 y H3) "
        "bajo una regla de decisión conjuntiva con nivel de significancia α = 0.05 y corrección de "
        "Holm-Bonferroni, sin aplicar un p-valor paramétrico único sobre métricas inconmensurables.",
        sangria=True
    )

    agregar_titulo_3(doc, "1.5.2. Hipótesis específicas")
    hipotesis_esp = [
        "**H1:** La aplicación del sistema web SIVAC mejora significativamente la oportunidad de procesamiento en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, evidenciada en la reducción del tiempo de registro de movimientos y del tiempo de emisión de vales de salida.",
        "**H2:** La aplicación del sistema web SIVAC mejora significativamente la consistencia documental en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, evidenciada en el incremento del porcentaje de registros sin discrepancias y de la concordancia entre la cantidad programada y la cantidad entregada.",
        "**H3:** La aplicación del sistema web SIVAC mejora significativamente la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, evidenciada en el incremento de la aceptación del proceso y de la utilidad percibida."
    ]
    for he in hipotesis_esp:
        agregar_item_lista(doc, he, simbolo="•")

    # 1.6. Variables de la investigación
    agregar_titulo_2(doc, "1.6. Variables de la investigación")

    agregar_titulo_3(doc, "1.6.1. Variable independiente: Sistema web SIVAC")
    agregar_parrafo(
        doc,
        "El sistema web SIVAC constituye la intervención tecnológica experimental administrada sobre "
        "el flujo logístico de inmunizaciones de la DISA Apurímac II, evaluada operacionalmente como "
        "una condición dicotómica pre-intervención (gestión manual en libros físicos de kardex y "
        "talonarios impresos) frente a post-intervención (gestión digitalizada mediante la plataforma "
        "web SIVAC construida bajo la metodología Extreme Programming y verificada con la norma "
        "ISO/IEC 25010:2023).",
        sangria=True
    )

    agregar_titulo_3(doc, "1.6.2. Variable dependiente: Gestión de movimientos de vacunas")
    agregar_parrafo(
        doc,
        "La gestión de movimientos de vacunas comprende el proceso técnico-administrativo de "
        "registro, validación, trazabilidad en kardex y emisión de vales de salida de los productos "
        "biológicos en los centros de acopio de la DISA Apurímac II. Se estructura en tres "
        "dimensiones oficiales: (1) oportunidad de procesamiento, evaluada mediante el tiempo de "
        "registro de movimientos y el tiempo de emisión de vales de salida; (2) consistencia "
        "documental, medida a través del porcentaje de registros sin discrepancias y la concordancia "
        "entre cantidad programada y cantidad entregada; y (3) satisfacción del usuario, medida "
        "mediante la aceptación del proceso y la utilidad percibida bajo el Modelo de Aceptación "
        "Tecnológica (TAM). La matriz detallada de operacionalización de variables se presenta en "
        "la Tabla 10 del Capítulo IV.",
        sangria=True
    )

    # 1.7. Delimitación de la investigación
    agregar_titulo_2(doc, "1.7. Delimitación de la investigación")
    agregar_parrafo(
        doc,
        "La investigación se circunscribió espacialmente a la jurisdicción sanitaria de la DISA "
        "Apurímac II, abarcando sus ocho centros de acopio: el almacén especializado de la sede "
        "central en Andahuaylas y los centros de acopio vinculados a las redes y microredes de "
        "salud de las provincias de Andahuaylas y Chincheros. Temporalmente, el estudio se ejecutó "
        "durante el periodo 2025–2026, estructurando ventanas simétricas de observación basal "
        "(pre-test) y post-intervención (post-test) de 30 días calendario cada una. Social y "
        "poblacionalmente, se delimitó a la totalidad censal de los 14 operadores responsables "
        "de la cadena de frío e inmunizaciones de dicha entidad (N = n = 14).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "En cuanto a la delimitación temática y a las limitaciones operativas controladas durante "
        "el estudio, la investigación se enfocó exclusivamente en la gestión logística y documental "
        "de movimientos de vacunas en sus tres dimensiones oficiales (oportunidad de procesamiento, "
        "consistencia documental y satisfacción del usuario), sin abarcar la termodinámica física de "
        "los equipos frigoríficos, el acto clínico de vacunación nominal de pacientes ni la ejecución "
        "presupuestal financiera. Asimismo, las fluctuaciones de conectividad en centros periféricos "
        "y la curva inicial de adaptación del personal fueron mitigadas mediante la ligereza "
        "transaccional de la arquitectura web, jornadas presenciales de capacitación práctica y un "
        "periodo de estabilización operativa previo a la medición post-test; finalmente, dado el "
        "tamaño de la población censal (N = n = 14), se estableció la verificación distribucional "
        "con la prueba de Shapiro-Wilk y el contraste no paramétrico de rangos con signo de Wilcoxon "
        "para respaldar el rigor inferencial del estudio.",
        sangria=True
    )
