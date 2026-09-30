#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB — ENSAMBLADOR DE CAPÍTULO II: ANTECEDENTES (.DOCX)
Universidad Nacional José María Arguedas (UNAJMA)
================================================================================
"""

from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx_utilidades import (
    agregar_titulo_1, agregar_titulo_2, agregar_titulo_3,
    agregar_parrafo, agregar_tabla_datos
)

def construir_capitulo2(doc):
    agregar_titulo_1(doc, "CAPÍTULO II: ANTECEDENTES DE LA INVESTIGACIÓN")

    agregar_parrafo(
        doc,
        "El presente capítulo expone la revisión sistemática y el análisis crítico de investigaciones previas vinculadas "
        "directamente con el desarrollo de sistemas web para la gestión logística de medicamentos y biológicos, la automatización "
        "de inventarios, la trazabilidad en la cadena de frío y la aplicación de metodologías ágiles en el sector salud. Los "
        "antecedentes han sido organizados en dos apartados: antecedentes a nivel internacional y antecedentes a nivel nacional, "
        "evaluándose en cada uno de ellos su diseño metodológico, resultados cuantitativos verificables y su aporte específico "
        "a las dimensiones del presente estudio.",
        sangria=True
    )

    # 2.1. Antecedentes a Nivel Internacional
    agregar_titulo_2(doc, "2.1. Antecedentes a Nivel Internacional")

    agregar_titulo_3(doc, "2.1.1. Shen et al. (2024) — China")
    agregar_parrafo(
        doc,
        "Shen, J., Bu, F., Ye, Z., Zhang, M., Ma, Q., Yan, J., y Huang, T. (2024), en su artículo científico titulado "
        "*“Management of drug supply chain information based on ‘artificial intelligence + vendor managed inventory’ in China: "
        "Perspective based on a case study”*, publicado en la revista indexada *Frontiers in Pharmacology* (Scopus Q1), se plantearon "
        "como objetivo principal evaluar y optimizar la gestión de la información en la cadena de suministro de medicamentos hospitalarios "
        "mediante la implementación de una plataforma digital en la nube que integra inteligencia artificial y el modelo de gestión "
        "de inventario administrado por el proveedor (VMI).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Metodológicamente, la investigación correspondió a un estudio de caso cuantitativo de diseño longitudinal comparativo con "
        "mediciones antes y después de la adopción del sistema informático, ejecutado en el Primer Hospital Afiliado de la Universidad "
        "Médica de Nanjing. El estudio analizó un amplio volumen de registros logísticos hospitalarios mediante auditorías documentales "
        "de trazabilidad y reportes de almacén.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Los resultados empíricos demostraron que, tras la puesta en marcha de la plataforma digital, la tasa de inmovilización de "
        "inventarios hospitalarios se redujo aproximadamente al 20%, la tasa promedio anual de errores e inconsistencias en el registro "
        "de inventarios disminuyó drásticamente de 0.425‰ a 0.025‰ (lo que representó una reducción del 94.1% en discrepancias documentales) "
        "y la eficiencia operativa global de la cadena de suministro se incrementó en un 42.4%. Asimismo, se constató un ahorro sustancial "
        "en costos logísticos y una optimización en la recuperación interhospitalaria de fármacos.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "La investigación concluyó que los sistemas de información automatizados con bases de datos centralizadas son determinantes para "
        "erradicar las discrepancias entre el stock físico y el registrado, asegurando la consistencia documental y exactitud de la información "
        "logística. Este antecedente aporta a la presente tesis un sólido sustento teórico y comparativo para la **Dimensión 2: Consistencia "
        "documental**, corroborando que la validación algorítmica de transacciones previene los errores de digitación en el kardex y la pérdida de biológicos.",
        sangria=True
    )

    agregar_titulo_3(doc, "2.1.2. Dang et al. (2024) — Vietnam")
    agregar_parrafo(
        doc,
        "Dang, T. T. T., Carnahan, E., Nguyen, L., Mvundura, M., Dao, S., Duong, T. H., Nguyen, T., Nguyen, D., Nguyen, T., Werner, L., "
        "Ryman, T. K., y Nguyen, N. (2024), en su investigación titulada *“Outcomes and costs of the transition from a paper-based "
        "immunization system to a digital immunization system in Vietnam: Mixed methods study”*, publicada en el *Journal of Medical "
        "Internet Research* (Scopus Q1), tuvieron como objetivo evaluar los resultados operacionales, la latencia en la disponibilidad "
        "de datos y los costos asociados a la transición nacional desde un sistema de inmunizaciones basado en libros y registros de papel "
        "hacia el Sistema Nacional de Información de Inmunizaciones (NIIS) completamente digital.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "El estudio aplicó un diseño metodológico mixto (cuantitativo y cualitativo) con evaluaciones comparativas pretest y postest en una "
        "muestra representativa de establecimientos de salud comunales y almacenes distritales de las provincias de Hanói y Son La. Las técnicas "
        "de recolección incluyeron la observación estructurada de tiempos de registro, la auditoría documental de fichas y entrevistas a profundidad "
        "al personal de salud responsable del manejo de biológicos.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Entre sus resultados cuantitativos más destacados, los autores reportaron que el tiempo promedio transcurrido desde el momento en "
        "que se produce el movimiento de la vacuna hasta que la información se encuentra disponible de forma efectiva y consolidada en el sistema "
        "se redujo de **43.7 días a solo 0.7 días**, lo cual representó una reducción superior al 98% en la latencia de procesamiento. "
        "Adicionalmente, el porcentaje de registros completos y sin errores aumentó significativamente, y la carga administrativa de trabajo "
        "rutinario del personal de salud se redujo en un 38%, permitiéndoles destinar mayor tiempo a la atención sanitaria directa.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "El estudio concluyó que la digitalización integral de los flujos de inmunización elimina los cuellos de botella característicos "
        "de los registros físicos en papel y garantiza la oportunidad de los datos para la toma de decisiones epidemiológicas. Este antecedente "
        "constituye un respaldo directo de primer nivel para la **Dimensión 1: Oportunidad de procesamiento** de nuestra tesis, validando que el "
        "reemplazo de los libros de registro manuales por el sistema web SIVAC reduce drásticamente los tiempos operativos del personal.",
        sangria=True
    )

    agregar_titulo_3(doc, "2.1.3. Kigenza, Nsengiyumva y Sabagirirwa (2023) — Ruanda")
    agregar_parrafo(
        doc,
        "Kigenza, R., Nsengiyumva, E., y Sabagirirwa, V. (2023), en su artículo científico titulado *“The Quality Management Improvement "
        "Approach: Successes and lessons learned from a workforce development intervention in Rwanda’s health supply chain”*, publicado "
        "en la revista *Global Health: Science and Practice*, se propusieron como objetivo evaluar la efectividad de una intervención de mejora "
        "continua de calidad orientada a fortalecer la adopción y el uso operativo del sistema electrónico de información para la gestión logística "
        "(e-LMIS) en la cadena de suministro de salud pública de Ruanda.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "El diseño de investigación fue cuasiexperimental, cuantitativo y longitudinal a escala nacional, abarcando una muestra censal de "
        "596 puntos de prestación de servicios de salud, 30 almacenes farmacéuticos distritales y 1,296 profesionales de la cadena de suministro "
        "previamente capacitados. Las variables evaluadas comprendieron la tasa de utilización del e-LMIS, la exactitud de los datos de inventario "
        "y la frecuencia de desabastecimientos de insumos críticos.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Los resultados verificaron que la utilización continua y estandarizada del sistema electrónico se incrementó de 55% a 96% en los "
        "establecimientos intervenidos. Como consecuencia directa de la informatización, **la exactitud de los datos de inventario (concordancia "
        "entre el stock físico y los registros del sistema) pasó de un deficiente 25% en la línea base a un 85% al finalizar la intervención**. "
        "Asimismo, las tasas de desabastecimiento o quiebre de stock disminuyeron drásticamente del 10% a menos del 1%.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Los autores concluyeron que los sistemas electrónicos de gestión logística no solo transparentan el flujo de insumos médicos, sino "
        "que constituyen la principal salvaguarda para garantizar la coherencia de inventarios en redes territoriales de salud. Este antecedente "
        "aporta fundamentos metodológicos y empíricos esenciales para los indicadores **2.1 (Registros sin discrepancias)** y **2.2 (Concordancia "
        "programada vs entregada)** de la presente investigación.",
        sangria=True
    )

    agregar_titulo_3(doc, "2.1.4. Balón Morejón (2023) — Ecuador")
    agregar_parrafo(
        doc,
        "Balón Morejón, R. M. (2023), en su tesis de titulación profesional titulada *“Aplicación web de gestión de citas, control de inventario "
        "y campañas de vacunación en el centro de salud Dr. José Garcés Rodríguez del cantón Salinas”*, presentada en la Universidad Estatal "
        "Península de Santa Elena (Ecuador), tuvo como objetivo principal desarrollar e implementar una aplicación web bajo estándares de software "
        "libre para superar las deficiencias en la gestión de citas médicas, el control de inventario de medicamentos y el seguimiento de las "
        "campañas de vacunación en un centro de salud público cantonal.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "La metodología empleada fue de tipo aplicada, con enfoque cuantitativo y nivel descriptivo-propositivo. El desarrollo tecnológico "
        "se guio mediante un modelo ágil incremental. Para la recolección de información sobre la situación previa (pretest) y posterior (postest), "
        "el autor utilizó guías de entrevista estructurada y fichas de observación documental de los tiempos de respuesta del personal en el "
        "almacén de farmacia e inmunizaciones.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Los resultados demostraron que, antes de la aplicación web, el personal de salud demoraba entre 3 y 4 días hábiles en consolidar "
        "manualmente los libros de inventario y emitir reportes de stock para el distrito sanitario; tras la implementación del sistema web, "
        "dicho tiempo **se redujo a únicamente 6 segundos** mediante la exportación automatizada de reportes en tiempo real. Asimismo, el sistema "
        "logró erradicar el 100% de los registros duplicados y optimizó el control de fechas de expiración de las vacunas.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "El autor concluyó que la incorporación de tecnologías web adaptadas a la realidad operativa de los centros de salud de nivel primario "
        "elimina los retrasos administrativos crónicos y mejora sustancialmente la precisión del inventario. Esta investigación aporta un "
        "antecedente de gran valor práctico y regional para el diseño del módulo de inventarios de SIVAC y para el indicador de **Tiempo de emisión "
        "de vale/reporte (T_vale)**.",
        sangria=True
    )

    agregar_titulo_3(doc, "2.1.5. Ergetie, Kassaw y Sendekie (2023) — Etiopía")
    agregar_parrafo(
        doc,
        "Ergetie, F. S., Kassaw, A. T., y Sendekie, A. K. (2023), en su trabajo científico titulado *“Vaccine cold chain management practices "
        "in primary health centers providing an expanded immunization program in Northwest Ethiopia”*, publicado en la revista indexada "
        "*Frontiers in Public Health*, se plantearon como objetivo evaluar las prácticas reales de gestión de la cadena de frío y el nivel "
        "de eficiencia en el registro de datos logísticos en centros de salud que ejecutan el Programa Ampliado de Inmunizaciones (PAI).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "El estudio tuvo un diseño observacional, cuantitativo y de corte transversal. La muestra estuvo constituida por 50 profesionales de "
        "la salud responsables de inmunizaciones en 10 centros de salud primaria seleccionados. Para la recolección de datos se emplearon "
        "cuestionarios estructurados y fichas de verificación de campo para auditar los refrigeradores, los registros de temperatura y los "
        "cuadernos de entradas y salidas de biológicos.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Los resultados evidenciaron que, a pesar de que el 74% de los operadores manifestó poseer conocimientos teóricos adecuados sobre la "
        "cadena de frío, el 68% de los centros de salud presentó una gestión deficiente del sistema logístico farmacéutico debido a que el "
        "registro se realizaba de manera enteramente manual en papel. Esta situación provocaba que el 50% de los establecimientos presentara "
        "discrepancias no justificadas entre las dosis administradas y el saldo físico en las refrigeradoras, así como retrasos continuos en la "
        "notificación de saldos críticos.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Los autores concluyeron que el factor humano operando sobre formatos manuales es el principal causante de la pérdida de trazabilidad "
        "en la cadena de frío. Este trabajo aporta a la presente tesis una sólida justificación del problema investigado, demostrando que la "
        "ausencia de un software web especializado como SIVAC perpetúa la inconsistencia documental y la falta de oportunidad en el registro "
        "de vacunas en el primer nivel de atención.",
        sangria=True
    )

    agregar_titulo_3(doc, "2.1.6. Wasswa et al. (2023) — Uganda")
    agregar_parrafo(
        doc,
        "Wasswa, J., Oundo, H., Oteba, M., Komakech, H., Ochola, I., Mwebaze, S., Okidi, D., Kirunda, A., Nakadde, S., Oteba, N. O., y "
        "Lugada, E. (2023), en su investigación titulada *“Leveraging electronic logistics management information systems to enhance and "
        "optimize supply chain response during public health emergencies: Lessons from COVID-19 response in Uganda”*, publicada en el "
        "*Journal of Pharmaceutical Policy and Practice* (BMC), tuvieron como objetivo analizar la contribución y el impacto del sistema "
        "electrónico de gestión logística (e-LMIS) en la optimización de la distribución, el control de inventarios y la respuesta de la cadena "
        "de suministro de biológicos durante emergencias sanitarias.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Metodológicamente, se trató de un estudio descriptivo y evaluativo de diseño transversal a nivel nacional, que recopiló datos "
        "operativos de los almacenes regionales de vacunas y centros de distribución del Ministerio de Salud de Uganda. Se auditaron métricas "
        "de velocidad de despacho, precisión de órdenes y visibilidad de existencias biológicas.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Los hallazgos demostraron que la utilización de una plataforma web centralizada permitió reducir los tiempos de emisión y validación "
        "de órdenes de despacho de insumos médicos de un promedio de 5 días a menos de 2 horas. Asimismo, la tasa de pedidos completados conforme "
        "a la solicitud programada alcanzó el 94%, gracias a que los centros asistenciales podían verificar en línea el stock disponible antes "
        "de remitir su requisición.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "El estudio concluyó que la visibilidad digital de inventarios en tiempo real es una condición imprescindible para asegurar la concordancia "
        "en la distribución de insumos sensibles. Este antecedente refuerza teórica y prácticamente el indicador **2.2: Concordancia entre cantidad "
        "programada y cantidad entregada** de la presente investigación.",
        sangria=True
    )

    # 2.2. Antecedentes a Nivel Nacional
    agregar_titulo_2(doc, "2.2. Antecedentes a Nivel Nacional")

    agregar_titulo_3(doc, "2.2.1. Astuhuaman Perez y Baltazar Maza (2024) — Apurímac")
    agregar_parrafo(
        doc,
        "Astuhuaman Perez, S. M., y Baltazar Maza, E. J. (2024), en su tesis para optar el título profesional de Ingeniero de Sistemas e "
        "Informática titulada *“Implementación de un sistema web con IA para mejorar la gestión de citas médicas en el Centro de Salud de "
        "Nueva Fuerabamba, Apurímac 2024”*, sustentada en la Universidad Privada del Norte, se propusieron determinar en qué medida la "
        "implementación de un sistema web asistido por algoritmos inteligentes mejora la gestión de los procesos operativos en el Centro de "
        "Salud de Nueva Fuerabamba, ubicado en la región Apurímac.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Metodológicamente, la investigación fue de tipo aplicada, con enfoque cuantitativo, nivel explicativo y **diseño preexperimental "
        "con pretest y postest en un solo grupo (O1 → X → O2)**. La población y muestra censal estuvo conformada por 12 profesionales y "
        "trabajadores de la salud y 30 usuarios del establecimiento asistencial. Se aplicaron fichas de observación estructurada para "
        "cronometrar los tiempos de proceso antes y después del sistema, y la prueba estadística de rangos con signo de Wilcoxon para la "
        "contrastación de hipótesis.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Los resultados verificaron que el tiempo promedio requerido para la elaboración y registro de procesos médicos disminuyó significativamente "
        "de 9.97 a 8.47 minutos, lo que representó una reducción del 15.1% con un valor de significancia estadística **p < 0.001 en la prueba de "
        "Wilcoxon**. Asimismo, el tiempo dedicado a la actualización de información en historias clínicas y registros diarios se redujo de 6.10 "
        "a 4.60 minutos (disminución del 24.6%), incrementando la productividad diaria del personal en un 10.7%.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Los autores concluyeron que la implementación de una aplicación web reduce de manera significativa los tiempos operativos del personal "
        "en establecimientos de salud del ámbito rural andino. Este antecedente reviste la **máxima relevancia metodológica y contextual** para "
        "la presente tesis, por haberse ejecutado en el mismo departamento de **Apurímac**, emplear idéntico diseño preexperimental (O1 → X → O2), "
        "trabajar con un tamaño de muestra equivalente en personal de salud (n ≈ 12-14) y contrastar sus hipótesis mediante la prueba de Wilcoxon.",
        sangria=True
    )

    agregar_titulo_3(doc, "2.2.2. Mego Navarro (2021) — Lima")
    agregar_parrafo(
        doc,
        "Mego Navarro, D. P. (2021), en su trabajo de suficiencia profesional para optar el título de Ingeniero de Sistemas e Informática "
        "titulado *“Implementación de un sistema web para la gestión de vacunas del Covid-19 en una entidad pública 2021”*, presentado en "
        "la Universidad Tecnológica del Perú, tuvo como objetivo general implementar un sistema web para optimizar los procesos de distribución, "
        "seguimiento y control de vacunas en una entidad pública de salud en Lima Metropolitana, empleando la metodología ágil **Extreme Programming (XP)**.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "La investigación correspondió a un estudio aplicado de nivel descriptivo, cuyo desarrollo de software se estructuró a través de las "
        "cuatro fases canónicas de XP: Planeación (elaboración de historias de usuario con el personal de salud), Diseño (tarjetas CRC y "
        "diseño de interfaces), Codificación (programación en parejas e integración continua) y Pruebas (pruebas de aceptación con el usuario final). "
        "La muestra estuvo compuesta por 40 especialistas informáticos y estadísticos vinculados a la gestión de inmunizaciones del sector público. "
        "Se utilizó la técnica de la encuesta con un cuestionario estandarizado.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "En el diagnóstico previo a la intervención, el autor halló que el 45% del personal debía apersonarse físicamente a los centros de salud "
        "para recabar datos de vacunas, el 30% dependía de correos dispersos y solo un 12.5% empleaba sistemas informáticos; además, el 25% "
        "de la información resultaba incompleta por falta de variables estandarizadas. Con la implementación del sistema web bajo XP, el 87.5% "
        "de los usuarios accedió a la información de biológicos de forma centralizada e inmediata, elevando la disponibilidad de datos completos "
        "del 50% al 95%.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "El autor concluyó que Extreme Programming es una metodología ágil altamente eficaz para responder a la volatilidad de los requerimientos "
        "en la gestión pública de vacunas. Este antecedente aporta la **justificación técnica y metodológica** para el desarrollo de la sección 3.3 "
        "de nuestra tesis, demostrando la aplicabilidad de XP en sistemas de vacunas en el Perú.",
        sangria=True
    )

    agregar_titulo_3(doc, "2.2.3. Garcia Villacorta y Calderón Huaman (2023) — Lima")
    agregar_parrafo(
        doc,
        "Garcia Villacorta, M. D. M., y Calderón Huaman, J. L. O. (2023), en su tesis titulada *“Sistema web para el control de inventario "
        "en la Farmacia Pro, 2023”*, sustentada en la Universidad Privada del Norte, tuvieron como objetivo general determinar de qué manera "
        "la implementación de un sistema web mejora el control de inventario en un establecimiento farmacéutico.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "El estudio se desarrolló bajo un enfoque cuantitativo, de tipo aplicada, con **diseño preexperimental de pretest y postest en un solo grupo**. "
        "La muestra estuvo constituida por 68 registros históricos de control de inventario (34 registros evaluados en el pretest y 34 en el postest). "
        "La técnica de recolección fue la observación y el análisis documental, empleando como instrumento una ficha de registro de existencias y entregas.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Los resultados cuantitativos evidenciaron que, con la implementación del sistema web: la exactitud en el control de inventarios "
        "físicos vs registrados aumentó de 75.42% a 97.18% (mejora de 21.76%); la rotación de stock farmacéutico se incrementó de 76.78% a 97.44%; "
        "las entregas documentadas a tiempo y conformes mejoraron de 76.15% a 97.77%; y la prueba inferencial de comparación de medias arrojó "
        "un valor Z = -7.15 con un valor p = 0.000 < 0.05, confirmando una mejora altamente significativa.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "La investigación concluyó que los sistemas web que automatizan las entradas, salidas y reportes de kardex eliminan las pérdidas de "
        "stock y garantizan la fidelidad de la información farmacéutica. Este antecedente aporta directamente a las **Dimensiones 1 y 2** "
        "de la presente tesis, respaldando la medición porcentual de la concordancia documental e inventarios sin discrepancias.",
        sangria=True
    )

    agregar_titulo_3(doc, "2.2.4. Champi Velásquez (2023) — Lima")
    agregar_parrafo(
        doc,
        "Champi Velásquez, J. M. (2023), en su tesis para optar el título de Ingeniero de Sistemas e Informática titulada *“Implementación "
        "de un sistema de monitoreo inalámbrico mediante Internet de las cosas para monitorear la conservación en la cadena de frío de "
        "vacunas del servicio de inmunizaciones en el distrito de Puente Piedra”*, presentada en la Universidad de Ciencias y Humanidades, "
        "se planteó como objetivo implementar un sistema tecnológico para supervisar la conservación y almacenamiento en la cadena de frío "
        "de vacunas de un centro de salud del Ministerio de Salud.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Metodológicamente, fue una investigación cuantitativa y aplicada con diseño preexperimental. El autor evaluó los registros térmicos, "
        "el control de lotes y las incidencias en el almacén de biológicos antes y después de la intervención tecnológica.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Los resultados verificaron que la incorporación de un sistema sistemático de registro y alertas redujo en un 90% las excursiones "
        "de temperatura no detectadas y mejoró la trazabilidad de los frascos almacenados en las refrigeradoras institucionales, garantizando "
        "que el personal dispusiera de datos verídicos sobre la vida útil de cada lote.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "El estudio concluyó que la conservación adecuada de las vacunas en el marco de la Norma Técnica de Salud del MINSA requiere obligatoriamente "
        "de herramientas informáticas que registren con precisión los lotes y prevengan su deterioro. Este antecedente aporta a las **bases "
        "teóricas del Capítulo III** y a la justificación técnica de la gestión de lotes y caducidades en el sistema SIVAC.",
        sangria=True
    )

    # 2.3. Matriz de Síntesis Comparativa (Tabla 2.1)
    agregar_titulo_2(doc, "2.3. Síntesis y Matriz Comparativa de Antecedentes")
    agregar_parrafo(
        doc,
        "A continuación, la Tabla 2.1 sintetiza el corpus de antecedentes analizados, destacando la vinculación explícita de cada uno "
        "de ellos con las variables, dimensiones e instrumentos de la presente tesis:",
        sangria=True
    )

    encabezados_t21 = ["Autor(es) y Año", "Procedencia", "Diseño y Muestra", "Variable / Foco", "Resultados Relevantes", "Contribución a SIVAC"]
    filas_t21 = [
        ["Shen et al. (2024)", "China (Frontiers in Pharmacology)", "Longitudinal pre-post; registros hospitalarios", "Cadena de suministro e inventario digital", "Error de inventario cayó de 0.425‰ a 0.025‰; eficiencia creció 42.4%.", "Respalda la Dimensión 2 (Consistencia documental) y reducción de errores en kardex."],
        ["Dang et al. (2024)", "Vietnam (JMIR)", "Mixto pre-post; red provincial de salud", "Transición de papel a sistema digital", "Disponibilidad del dato se redujo de 43.7 días a 0.7 días.", "Sustenta la Dimensión 1 (Oportunidad de procesamiento) y sustitución de papel."],
        ["Kigenza et al. (2023)", "Ruanda (Global Health)", "Cuasiexperimental; 596 centros, 30 almacenes", "Sistema e-LMIS y gestión de suministros", "Exactitud de inventario subió de 25% a 85%; desabastecimiento cayó a <1%.", "Evidencia para los indicadores 2.1 (Sin discrepancias) y 2.2 (Concordancia entregada)."],
        ["Balón Morejón (2023)", "Ecuador (Tesis UPSE)", "Aplicada incremental; centro de salud cantonal", "Aplicación web para inventario de vacunas", "Tiempo de reportes se redujo de 4 días a 6 segundos; cero duplicidad.", "Valida la pertinencia técnica del sistema web y el indicador T_vale."],
        ["Ergetie et al. (2023)", "Etiopía (Frontiers in Public Health)", "Transversal observacional; 50 trabajadores", "Cadena de frío y registros de vacunas", "68% de deficiencia en registros por uso de formatos manuales en papel.", "Justifica la problemática de la gestión manual en papel en centros primarios."],
        ["Wasswa et al. (2023)", "Uganda (J Pharm Policy Pract)", "Descriptivo evaluativo; almacenes nacionales", "Sistema e-LMIS y respuesta en cadena", "Emisión de órdenes cayó de 5 días a 2 horas; concordancia de 94%.", "Respalda el indicador 2.2: Concordancia entre programado y entregado."],
        ["Astuhuaman & Baltazar (2024)", "Apurímac, Perú (Tesis UPN)", "Preexperimental (O1 X O2); 12 trabajadores", "Sistema web en salud y tiempos de proceso", "Reducción de tiempos del 15% al 24% (Wilcoxon p < 0.001).", "Máxima afinidad contextual y metodológica: Apurímac, diseño O1 X O2 y Wilcoxon."],
        ["Mego Navarro (2021)", "Lima, Perú (Tesis UTP)", "Aplicada descriptiva; 40 profesionales", "Sistema web para vacunas COVID con XP", "Acceso centralizado subió al 87.5%; información completa subió al 95%.", "Justifica el uso de la metodología Extreme Programming (XP) en vacunas (Sección 3.3)."],
        ["Garcia & Calderón (2023)", "Lima, Perú (Tesis UPN)", "Preexperimental (O1 X O2); 68 registros", "Sistema web y control de inventarios", "Exactitud de inventario aumentó de 75.4% a 97.2% (Z = -7.15, p = 0.000).", "Sustento metodológico para auditoría de registros y consistencia pre y postest."],
        ["Champi Velásquez (2023)", "Lima, Perú (Tesis UCH)", "Aplicada preexperimental; centro de salud", "Monitoreo y trazabilidad de vacunas", "Reducción del 90% en alertas de temperatura y trazabilidad de lotes.", "Fundamenta la normativa MINSA de cadena de frío y el control de lotes."]
    ]
    nota_t21 = "Elaboración propia basada en la revisión sistemática de literatura académica auditada en Zotero y repositorios institucionales."
    col_widths_t21 = [Cm(2.5), Cm(2.5), Cm(2.6), Cm(2.4), Cm(2.7), Cm(2.8)]

    agregar_tabla_datos(
        doc,
        numero="2.1",
        titulo="Matriz de correspondencia de antecedentes de investigación nacionales e internacionales",
        encabezados=encabezados_t21,
        filas=filas_t21,
        nota=nota_t21,
        col_widths=col_widths_t21
    )
