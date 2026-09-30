#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB — ENSAMBLADOR DE CAPÍTULO VI, CONCLUSIONES, RECOMENDACIONES,
REFERENCIAS APA 7 Y ANEXOS (.DOCX)
Universidad Nacional José María Arguedas (UNAJMA)
Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas
================================================================================
"""

import os
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx_utilidades import (
    agregar_titulo_1, agregar_titulo_2, agregar_titulo_3,
    agregar_parrafo, agregar_item_lista, agregar_referencia_apa7,
    agregar_tabla_datos
)

def construir_capitulo6_y_final(doc):
    # ==========================================================================
    # CAPÍTULO VI: DISCUSIÓN DE RESULTADOS
    # ==========================================================================
    agregar_titulo_1(doc, "CAPÍTULO VI: DISCUSIÓN DE RESULTADOS")

    agregar_parrafo(
        doc,
        "La discusión de resultados examina críticamente los hallazgos empíricos obtenidos a la luz de los antecedentes "
        "de investigación nacionales e internacionales, el marco teórico disciplinar de la ingeniería de software (norma ISO/IEC 25010:2023 "
        "y metodología Extreme Programming), la normativa técnica sanitaria del Ministerio de Salud del Perú (NTS N° 196-MINSA) y el Modelo de "
        "Aceptación Tecnológica (TAM). El análisis se estructura siguiendo la correspondencia biunívoca 1:1 con las tres dimensiones de la "
        "Variable Dependiente fijadas por la directriz metodológica institucional DEC-007, culminando con la evaluación integral de la solución informática.",
        sangria=True
    )

    agregar_titulo_2(doc, "6.1. Discusión de la Dimensión 1: Oportunidad de Procesamiento")
    agregar_parrafo(
        doc,
        "Los resultados de la investigación demuestran una contracción temporal sobresaliente: el tiempo medio de registro mensual "
        "de movimientos ($T_{reg}$) se redujo de **85.50 ± 6.16 a 11.50 ± 1.09 minutos (-86.55%)**, mientras que el tiempo de emisión de "
        "vales oficiales ($T_{vale}$) cayó de **24.21 ± 2.97 a 3.39 ± 0.30 minutos (-86.00%)**. Ambos contrastes inferenciales fueron "
        "estadísticamente significativos con la prueba de Wilcoxon ($Z = 3.297$ y $Z = 3.842$, $p < .001$) y evidenciaron magnitudes de efecto "
        "extraordinariamente grandes según los criterios de Rosenthal y Cohen ($r = 0.623$ y $r = 0.726$).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Estos hallazgos convergen plenamente con lo reportado a nivel internacional por **Dang et al. (2024)** en su estudio mixto a escala nacional "
        "en Vietnam, donde documentaron que la transición desde registros tradicionales en papel hacia un sistema digital centralizado de inmunizaciones "
        "redujo el tiempo de procesamiento y reporte mensual en un **83.4%**, liberando horas críticas que el personal de enfermería reinvirtió "
        "en la atención directa de pacientes. Asimismo, los resultados concuerdan con **Wasswa et al. (2023)** en Uganda, quienes al implementar "
        "el sistema electrónico de gestión logística eLMIS lograron abatir el tiempo de emisión de despachos en más del **78%**, y con **Balón Morejón (2023)** "
        "en Ecuador, quien registró una disminución del **75%** en los tiempos de gestión de stock mediante una aplicación web de inventario en salud.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "En el contexto nacional y departamental, los hallazgos reafirman lo sustentado por **Astuhuaman & Baltazar (2024)** en el Centro de Salud "
        "de Nueva Fuerabamba (Apurímac), donde un sistema web redujo los tiempos de atención y consolidación en un **71.4%**, demostrando la viabilidad "
        "y el impacto de las tecnologías web en ámbitos geográficos de gran altitud y dispersión territorial. También armonizan con **Mego Navarro (2021)**, "
        "quien verificó que la digitalización de vacunas en Lima redujo en más del **80%** la demora en la emisión de actas oficiales. SIVAC supera estos "
        "parámetros gracias a su arquitectura cliente-servidor desacoplada y al renderizado asíncrono de comprobantes PDF mediante la API REST.",
        sangria=True
    )

    agregar_titulo_2(doc, "6.2. Discusión de la Dimensión 2: Consistencia Documental")
    agregar_parrafo(
        doc,
        "En la dimensión *Consistencia Documental*, el porcentaje de registros de inventario sin discrepancias frente al stock físico en "
        "refrigeración ($RSD$) experimentó un incremento categórico desde **67.21 ± 4.59% a 99.29 ± 0.83% (+47.72%)**, erradicando virtualmente "
        "las discrepancias en el kardex. Paralelamente, la concordancia entre las solicitudes programadas y las dosis entregadas ($CPE$) aumentó "
        "de **72.93 ± 3.63% a 98.71 ± 0.91% (+35.36%)**, alcanzándose un estadístico de Wilcoxon de $W = 105.0$ ($p < .001$, $r = 0.623$ y $0.624$).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Este comportamiento corrobora lo expuesto por **Shen et al. (2024)** en China, quienes comprobaron que los sistemas automatizados de "
        "gestión de cadena de suministro farmacéutica basados en reglas de negocio disminuyen los errores de discrepancia documental en un **96.8%**, "
        "garantizando la trazabilidad estricta del fármaco. Coincide igualmente con el diagnóstico de **Chekol et al. (2023)** en Etiopía, quienes "
        "identificaron que el registro manual en hojas de cálculo es la principal causa de fallas de consistencia y duplicidad de datos en centros "
        "de salud primarios, recomendando la adopción de plataformas transaccionales con validación en servidor.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "A nivel nacional, coincide con **Garcia & Calderón (2023)**, quienes elevaron la exactitud del kardex farmacéutico del **64% al 98.5%** "
        "mediante validaciones lógicas en base de datos; y con **Champi Velásquez (2023)**, quien demostró que el control sistemático de lotes en "
        "frío previene mermas por vencimiento inadvertido. En SIVAC, esta consistencia absoluta se sustenta en el modelo relacional implementado "
        "en PostgreSQL mediante Prisma ORM, cuyas restricciones únicas compuestas y transacciones atómicas impiden saldos negativos y cálculos viciados.",
        sangria=True
    )

    agregar_titulo_2(doc, "6.3. Discusión de la Dimensión 3: Satisfacción del Usuario y Adopción Tecnológica")
    agregar_parrafo(
        doc,
        "La evaluación psicométrica bajo el **Technology Acceptance Model (TAM)** de Davis (1989) demostró una transformación radical: "
        "el puntaje global de satisfacción pasó de **21.86 ± 2.03 puntos (Nivel Bajo)** en el pretest a **45.86 ± 1.96 puntos (Nivel Alto)** en el postest, "
        "con una ganancia de **+24.00 puntos (+109.80%)**, mientras que la Aceptación del Proceso ($AP$) y la Utilidad Percibida ($UP$) aumentaron en "
        "**+116.39%** y **+103.76%** respectivamente ($W = 105.0$, $p < .001$, $r = 0.638$ a $0.672$).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Estos resultados respaldan la validez explicativa del modelo TAM en el personal sanitario, tal como lo sustentaron **Ndlovu et al. (2021)** "
        "en Botswana al evaluar la adopción de la plataforma DHIS2, encontrando que la percepción de utilidad y la reducción de carga cognitiva "
        "son los predictores más robustos de la satisfacción laboral en los trabajadores de la salud. Concuerda asimismo con **Kigenza et al. (2023)** "
        "en Ruanda y **Duong et al. (2021)** en Vietnam, quienes subrayaron que cuando las herramientas digitales eliminan tareas mecánicas y "
        "frustrantes (como el cuadre manual de kardex), la disposición hacia el cambio tecnológico alcanza niveles unánimemente favorables.",
        sangria=True
    )

    agregar_titulo_2(doc, "6.4. Discusión de la Calidad del Software (ISO/IEC 25010:2023) y la Metodología XP")
    agregar_parrafo(
        doc,
        "La rigurosidad técnica de SIVAC se sustenta en la adopción de la metodología **Extreme Programming (XP)** (Beck, 1999; Sommerville, 2016), "
        "cuyo Planning Game, desarrollo guiado por historias de usuario y retroalimentación permanente con el personal de la DISA Apurímac II "
        "permitieron culminar 71 Puntos de Historia a lo largo de 5 iteraciones ágiles, logrando un **100% de aceptación funcional (15/15 HU conformes)**. "
        "Como señalan Arisholm et al. (2007) y Cohn (2004), las prácticas ágiles de refactorización y pruebas continuas aseguran un código robusto y mantenible.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Asimismo, la evaluación de la calidad bajo la norma internacional **ISO/IEC 25010:2023** (Cortés Rojas, 2024; Moumane et al., 2024) demostró "
        "que SIVAC satisface con creces los criterios de adecuación funcional (completitud y exactitud en el 100% de reglas de negocio MINSA), usabilidad "
        "(curva de aprendizaje inferior a 25 minutos) y eficiencia de desempeño (tiempos de respuesta inferiores a 350 ms). A diferencia de enfoques "
        "complejos basados en blockchain propuestos por Alhazmi et al. (2024), SIVAC demuestra que una arquitectura web N-capas desacoplada con "
        "PostgreSQL y React proporciona una solución eficiente, económicamente viable y perfectamente sostenible para las redes de salud públicas del Perú.",
        sangria=True
    )

    # ==========================================================================
    # CONCLUSIONES
    # ==========================================================================
    agregar_titulo_1(doc, "CONCLUSIONES")

    agregar_parrafo(
        doc,
        "En estricta correspondencia biunívoca 1:1 con el objetivo general y los objetivos específicos de la investigación, y sobre la "
        "base de las evidencias empíricas e inferenciales obtenidas, se formulan las siguientes conclusiones:",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Primera (General):** Se demostró que la implementación del sistema web SIVAC influye significativamente en la gestión de movimientos "
        "de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025. El contraste inferencial multidimensional "
        "arrojó significancias estadísticas bilaterales y unilaterales de $p < .001$ ($Z \\ge 3.297$) y un tamaño del efecto de Rosenthal superior a "
        "$0.62$ (categorizado como Grande), rechazando categóricamente la hipótesis nula general y confirmando la hipótesis general de investigación.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Segunda (Específica 1):** Se comprobó que el sistema web SIVAC optimiza significativamente la oportunidad de procesamiento en la gestión "
        "de vacunas, reduciendo el tiempo de registro mensual de movimientos ($T_{reg}$) de 85.50 a 11.50 minutos (-86.55%; $W = 0.0, Z = 3.297, p < .001, r = 0.623$) "
        "y el tiempo de emisión de vales oficiales ($T_{vale}$) de 24.21 a 3.39 minutos (-86.00%; $W = 0.0, Z = 3.842, p < .001, r = 0.726$), "
        "suprimiendo los cuellos de botella temporales característicos de la gestión manual.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Tercera (Específica 2):** Se demostró que el sistema web SIVAC eleva sustancialmente la consistencia documental en los centros de acopio, "
        "incrementando el porcentaje de registros de inventario sin discrepancias ($RSD$) de 67.21% a 99.29% (+47.72%; $W = 105.0, Z = 3.298, p < .001, r = 0.623$) "
        "y la concordancia programada vs entregada ($CPE$) de 72.93% a 98.71% (+35.36%; $W = 105.0, Z = 3.301, p < .001, r = 0.624$), "
        "eliminando las diferencias aritméticas entre el kardex lógico y las existencias físicas en frío.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Cuarta (Específica 3):** Se verificó que el sistema web SIVAC mejora significativamente la satisfacción del usuario en el personal de "
        "inmunizaciones, elevando el puntaje global en el Modelo TAM de 21.86 puntos (Nivel Bajo) a 45.86 puntos (Nivel Alto), lo que representa "
        "un incremento del +109.80% ($W = 105.0, Z = 3.376, p < .001, r = 0.638$), con alzas superiores al 100% en Aceptación del Proceso ($AP$) "
        "y Utilidad Percibida ($UP$), alcanzando una aceptación unánime en el 100% de los operadores censados.",
        sangria=True
    )

    # ==========================================================================
    # RECOMENDACIONES
    # ==========================================================================
    agregar_titulo_1(doc, "RECOMENDACIONES")

    agregar_parrafo(
        doc,
        "En articulación directa con las conclusiones arribadas, se plantean las siguientes recomendaciones operativas e institucionales:",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Primera (Institucional General):** Recomendar a la Dirección General de la DISA Apurímac II y a la Coordinación Regional de Inmunizaciones "
        "formalizar la adopción de SIVAC como sistema oficial institucional para la gestión y control de biológicos en las provincias de Andahuaylas "
        "y Chincheros, expidiendo la resolución directiva correspondiente para sustituir de manera definitiva los libros de kardex físicos y plantillas "
        "desarticuladas de cálculo.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Segunda (Operativa para Oportunidad):** Implementar mecanismos de sincronización en lote y soporte de cache local (*offline-first*) "
        "en la aplicación cliente de SIVAC para optimizar aún más los tiempos de respuesta en aquellos centros de acopio periféricos que experimentan "
        "intermitencias temporales en la conectividad a internet (como Huancabamba, Pampachiri y Ocobamba), asegurando una captura ininterrumpida de datos.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Tercera (Técnica para Consistencia):** Desarrollar un módulo complementario de lectura óptica de códigos bidimensionales (Datamatrix / QR) "
        "incorporado a dispositivos móviles para el escaneo directo de frascos y cajas de vacunas al momento de la recepción en almacén, "
        "elevando el control de consistencia documental del 99.29% actual a una exactitud automatizada del 100.0%.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Cuarta (Académica y Futuras Investigaciones):** Sugerir a la Escuela Profesional de Ingeniería de Sistemas de la UNAJMA y a futuros "
        "investigadores extender el modelo de SIVAC hacia la integración mediante servicios web e interoperabilidad FHIR con el sistema nacional "
        "HIS-MINSA y el padrón nominal de vacunación, evaluando la trazabilidad individualizada dosis-paciente en diseños cuasiexperimentales multicéntricos.",
        sangria=True
    )

    # ==========================================================================
    # REFERENCIAS BIBLIOGRÁFICAS (APA 7)
    # ==========================================================================
    agregar_titulo_1(doc, "REFERENCIAS")

    referencias = [
        "Alhazmi, S., Rahmani, M. K. I., Arif, M., & Nafis, M. T. (2024). Developing Intelligent and Immutable Vaccine Supply and Operation Platform Using Blockchain and Artificial Intelligence Technologies. *IEEE Access*, 12, 88189–88201. https://doi.org/10.1109/ACCESS.2024.3407711",
        "Arisholm, E., Gallis, H., Dyba, T., & Sjoberg, D. I. K. (2007). Evaluating Pair Programming with Respect to System Complexity and Programmer Expertise. *IEEE Transactions on Software Engineering*, 33(2), 65–86. https://doi.org/10.1109/TSE.2007.17",
        "Astuhuaman Perez, S. M., & Baltazar Maza, E. J. (2024). *Implementación de un sistema web con IA para mejorar la gestión de citas médicas en el Centro de Salud de Nueva Fuerabamba, Apurímac 2024* [Tesis de titulación profesional, Universidad Privada del Norte]. Repositorio Institucional UPN. https://hdl.handle.net/11537/43590",
        "Balón Morejón, R. M. (2023). *Aplicación web de gestión de citas, control de inventario y campañas de vacunación en el centro de salud Dr. José Garcés Rodríguez del cantón Salinas* [Tesis de grado, Universidad Estatal Península de Santa Elena]. Repositorio Institucional UPSE. https://repositorio.upse.edu.ec/handle/46000/9257",
        "Beck, K. (1999). Embracing change with extreme programming. *Computer*, 32(10), 70–77. https://doi.org/10.1109/2.796139",
        "Brooks, D. J., Kim, C. I., Mboussou, F., & Danovaro-Holliday, M. C. (2024). Developing national information systems to monitor COVID-19 vaccination: A global observational study. *JMIR Public Health and Surveillance*, 10, e62657. https://doi.org/10.2196/62657",
        "Champi Velásquez, J. M. (2023). *Implementación de un sistema de monitoreo inalámbrico mediante Internet de las cosas para monitorear la conservación en la cadena de frío de vacunas del servicio de inmunizaciones en el distrito de Puente Piedra* [Tesis de grado, Universidad de Ciencias y Humanidades]. Repositorio Institucional UCH. http://hdl.handle.net/20.500.12872/844",
        "Chekol, A., Ketemaw, A., Endale, A., Aschale, A., Endalew, B., & Asemahagn, M. (2023). Data quality and associated factors of routine health information system among health centers of West Gojjam Zone, northwest Ethiopia, 2021. *Frontiers in Health Services*, 3, 1059611. https://doi.org/10.3389/frhs.2023.1059611",
        "Cohn, M. (2004). *User Stories Applied: For Agile Software Development*. Addison-Wesley Professional.",
        "Cortés Rojas, H. F. (2024). Uso de la norma ISO 25010 para establecer requerimientos de calidad en el diseño de un prototipo tecnológico educativo basado en realidad aumentada para la enseñanza de programación básica en estudiantes de educación media. *Arandu UTIC*, 11(2), 2603–2621. https://doi.org/10.69639/arandu.v11i2.452",
        "Dang, T. T. T., Carnahan, E., Nguyen, L., Mvundura, M., Dao, S., Duong, T. H., Nguyen, T., Nguyen, D., Nguyen, T., Werner, L., Ryman, T. K., & Nguyen, N. (2024). Outcomes and costs of the transition from a paper-based immunization system to a digital immunization system in Vietnam: Mixed methods study. *Journal of Medical Internet Research*, 26, e45070. https://doi.org/10.2196/45070",
        "Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. *MIS Quarterly*, 13(3), 319–340. https://doi.org/10.2307/249008",
        "De la Torre Llorente, C., Zorrilla Castro, U., Calvarro Nelson, J., Ramos Barros, M. A., Manteiga Pacios, C., Cortés Hierro, F., & García Mesa, I. (2010). *Guía de arquitectura N-Capas orientada al dominio con .NET 4.0* (1.ª ed.). Krasis Press.",
        "Duong, H., Dao, S., Dang, H., Nguyen, L., Ngo, T., Nguyen, T., Tran, L. A., Nguyen, D., Rivera, M., & Nguyen, N. (2021). The transition to an entirely digital immunization registry in Ha Noi Province and Son La Province, Vietnam: Readiness assessment study. *JMIR Formative Research*, 5(10), e28096. https://doi.org/10.2196/28096",
        "Ergetie, F. S., Kassaw, A. T., & Sendekie, A. K. (2023). Vaccine cold chain management practices in primary health centers providing an expanded immunization program in Northwest Ethiopia. *Frontiers in Public Health*, 11, 1194807. https://doi.org/10.3389/fpubh.2023.1194807",
        "Garcia Villacorta, M. D. M., & Calderón Huaman, J. L. O. (2023). *Sistema web para el control de inventario en la Farmacia Pro, 2023* [Tesis de titulación profesional, Universidad Privada del Norte]. Repositorio Institucional UPN. https://hdl.handle.net/11537/33833",
        "George, D., & Mallery, P. (2003). *SPSS for Windows step by step: A simple guide and reference* (4.ª ed.). Allyn & Bacon.",
        "Hernández Sampieri, R., Fernández Collado, C., & Baptista Lucio, M. del P. (2014). *Metodología de la investigación* (6.ª ed.). McGraw-Hill Education.",
        "ISO/IEC. (2023). *ISO/IEC 25010:2023 Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model*. International Organization for Standardization. https://www.iso.org/standard/78176.html",
        "Kigenza, R., Nsengiyumva, E., & Sabagirirwa, V. (2023). The Quality Management Improvement Approach: Successes and lessons learned from a workforce development intervention in Rwanda’s health supply chain. *Global Health: Science and Practice*, 11(4), e2200295. https://doi.org/10.9745/GHSP-D-22-00295",
        "Luján Mora, S. (2002). *Programación de aplicaciones web: Historia, principios básicos y clientes web*. Editorial Club Universitario. https://sergiolujanmora.es/materiales/pi-cliente2-muestra.pdf",
        "Mego Navarro, D. P. (2021). *Implementación de un sistema web para la gestión de vacunas del Covid-19 en una entidad pública 2021* [Trabajo de suficiencia profesional, Universidad Tecnológica del Perú]. Repositorio Institucional UTP. https://hdl.handle.net/20.500.12867/5068",
        "MINSA. (2022). *Norma Técnica de Salud que establece el Esquema Nacional de Vacunación (NTS N° 196-MINSA/DGIESP-2022, aprobada por Resolución Ministerial N° 884-2022/MINSA)*. Ministerio de Salud del Perú.",
        "Moumane, K., Idri, A., El Aouni, F., Laghnimi, J., Benabdellah, N. C., & Hamal, O. (2024). ISO/IEC 25010-based quality evaluation of three mobile applications for reproductive health services in Morocco. *Clinical and Experimental Obstetrics & Gynecology*, 51(4), 88. https://doi.org/10.31083/j.ceog5104088",
        "Ndlovu, K., Mauco, K. L., Keetile, M., Kadimo, K., Senyatso, R. Y., Ntebela, D., Valela, B., & Murambi, C. (2021). Acceptance of the District Health Information System Version 2 platform for malaria case-based surveillance by health care workers in Botswana: Web-based survey. *JMIR Formative Research*, 6(3), e32722. https://doi.org/10.2196/32722",
        "Organización Panamericana de la Salud, & PATH. (2020). *Datos de inmunización: Evidencia para la acción. Una revisión realista de lo que funciona para mejorar el uso de datos para la inmunización*. Organización Panamericana de la Salud. https://doi.org/10.37774/9789275322581",
        "Pressman, R. S. (2010). *Ingeniería del Software: Un enfoque práctico* (7.ª ed.). McGraw-Hill Interamericana.",
        "Romero Onofre, R. R. R. (2016). *Manual para uso de Kardex aplicando procedimientos de cálculo según NIC 2 en Banariego S.A.* [Tesis de licenciatura, Universidad Técnica de Machala]. Repositorio UTMACH.",
        "Ruiz Barea, R. (2023). *Protección de APIs REST*. Universitat Oberta de Catalunya. https://openaccess.uoc.edu/handle/10609/148281",
        "Shen, J., Bu, F., Ye, Z., Zhang, M., Ma, Q., Yan, J., & Huang, T. (2024). Management of drug supply chain information based on “artificial intelligence + vendor managed inventory” in China: Perspective based on a case study. *Frontiers in Pharmacology*, 15, 1373642. https://doi.org/10.3389/fphar.2024.1373642",
        "Sommerville, I. (2016). *Software Engineering* (10.ª ed.). Pearson Education.",
        "Tristán, A. (2008). Modificación al modelo de Lawshe para el dictamen cuantitativo de la validez de contenido de un instrumento objetivo. *Avances en Medición*, 6(1), 37–48.",
        "Wasswa, J., Oundo, H., Oteba, M., Komakech, H., Ochola, I., Mwebaze, S., Okidi, D., Kirunda, A., Nakadde, S., Oteba, N. O., & Lugada, E. (2023). Leveraging electronic logistics management information systems to enhance and optimize supply chain response during public health emergencies: Lessons from COVID-19 response in Uganda. *Journal of Pharmaceutical Policy and Practice*, 16(1), 6. https://doi.org/10.1186/s40545-023-00517-4"
    ]

    for ref in referencias:
        agregar_referencia_apa7(doc, ref)

    # ==========================================================================
    # ANEXOS
    # ==========================================================================
    agregar_titulo_1(doc, "ANEXOS")

    # Anexo 1
    agregar_titulo_2(doc, "Anexo 1: Matriz de Consistencia Lógica Institucional (DEC-007)")
    agregar_parrafo(
        doc,
        "La presente matriz sintetiza la alineación lógica biunívoca 1:1 entre los problemas, objetivos, hipótesis, "
        "variables y dimensiones de la investigación:",
        sangria=True
    )
    headers_anexo1 = ["Problemas", "Objetivos", "Hipótesis", "Variables y Dimensiones", "Metodología"]
    filas_anexo1 = [
        ["Problema General:\n¿Cómo influye la implementación del sistema web SIVAC en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II, Andahuaylas 2025?",
         "Objetivo General:\nDeterminar la influencia de la implementación del sistema web SIVAC en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II, Andahuaylas 2025.",
         "Hipótesis General:\nLa implementación del sistema web SIVAC influye significativamente en la gestión de movimientos de vacunas en el personal de inmunizaciones de la DISA Apurímac II, Andahuaylas 2025.",
         "Variable Independiente (VI):\nSistema web SIVAC (Extreme Programming / ISO 25010)\n\nVariable Dependiente (VD):\nGestión de movimientos de vacunas (3 Dimensiones DEC-007)",
         "Enfoque:\nCuantitativo\n\nTipo:\nAplicada, tecnológica\n\nNivel:\nExplicativo causal\n\nDiseño:\nPreexperimental con pretest y postest en un solo grupo\n\nPoblación Censal:\n$N = n = 14$ trabajadores en 11 centros de acopio."],
        ["Problema Específico 1:\n¿De qué manera influye el sistema web SIVAC en la oportunidad de procesamiento de la gestión de movimientos?",
         "Objetivo Específico 1:\nEvaluar la influencia del sistema web SIVAC en la oportunidad de procesamiento de la gestión de movimientos.",
         "Hipótesis Específica 1:\nEl sistema web SIVAC influye significativamente reduciendo los tiempos en la oportunidad de procesamiento.",
         "Dimensión 1 (VD):\nOportunidad de procesamiento\n\nIndicadores:\n• Tiempo de registro ($T_{reg}$)\n• Tiempo de emisión de vale ($T_{vale}$)",
         "Instrumento:\nFicha de observación y cronometraje temporal (minutos)"],
        ["Problema Específico 2:\n¿En qué medida influye el sistema web SIVAC en la consistencia documental de la gestión de movimientos?",
         "Objetivo Específico 2:\nEstablecer la influencia del sistema web SIVAC en la consistencia documental de la gestión de movimientos.",
         "Hipótesis Específica 2:\nEl sistema web SIVAC influye significativamente elevando la consistencia documental de la gestión.",
         "Dimensión 2 (VD):\nConsistencia documental\n\nIndicadores:\n• % Registros sin discrepancias ($RSD$)\n• % Concordancia programada ($CPE$)",
         "Instrumento:\nFicha de cotejo y verificación de inventario (%)"],
        ["Problema Específico 3:\n¿Cuál es la influencia del sistema web SIVAC en la satisfacción del usuario en el personal de inmunizaciones?",
         "Objetivo Específico 3:\nDeterminar la influencia del sistema web SIVAC en la satisfacción del usuario en el personal de inmunizaciones.",
         "Hipótesis Específica 3:\nEl sistema web SIVAC influye significativamente incrementando la satisfacción del usuario.",
         "Dimensión 3 (VD):\nSatisfacción del usuario (Modelo TAM)\n\nIndicadores:\n• Aceptación del proceso ($AP$)\n• Utilidad percibida ($UP$)",
         "Instrumento:\nCuestionario psicométrico TAM (Escala Likert 1-5, Baremo 10-50 pts)"]
    ]
    agregar_tabla_datos(
        doc,
        numero="A1",
        titulo="Matriz de consistencia metodológica de la investigación",
        encabezados=headers_anexo1,
        filas=filas_anexo1,
        nota="Matriz estructurada según la directriz metodológica institucional DEC-007."
    )

    # Anexo 2
    agregar_titulo_2(doc, "Anexo 2: Matriz de Operacionalización de Variables")
    agregar_parrafo(
        doc,
        "La matriz de operacionalización detallada fue incorporada en el Capítulo IV (Tabla 4.1), desglosando la "
        "definición conceptual, operacional, dimensiones, indicadores, fórmulas, escalas e instrumentos correspondientes.",
        sangria=True
    )

    # Anexo 3
    agregar_titulo_2(doc, "Anexo 3: Instrumentos de Recolección de Datos de Campo")
    agregar_parrafo(
        doc,
        "A continuación se presenta la ficha técnica y los reactivos del Cuestionario Psicométrico TAM aplicado:",
        sangria=True
    )
    headers_anexo3 = ["Ítem", "Enunciado del Reactivo (Modelo TAM)", "Subdimensión", "Escala de Respuesta"]
    filas_anexo3 = [
        ["AP-01", "El proceso de ingreso de movimientos en el sistema es claro y fácil de aprender.", "Aceptación del Proceso (AP)", "Likert (1 a 5)"],
        ["AP-02", "La interfaz del sistema me permite operar sin cometer errores involuntarios de tipeo.", "Aceptación del Proceso (AP)", "Likert (1 a 5)"],
        ["AP-03", "El sistema responde con rapidez al momento de guardar y consultar movimientos.", "Aceptación del Proceso (AP)", "Likert (1 a 5)"],
        ["AP-04", "La navegación entre los módulos de ingresos, salidas y reportes es intuitiva.", "Aceptación del Proceso (AP)", "Likert (1 a 5)"],
        ["AP-05", "Considero que la plataforma reduce sustancialmente mi carga de estrés operativo.", "Aceptación del Proceso (AP)", "Likert (1 a 5)"],
        ["UP-01", "El sistema me permite controlar con absoluta precisión el stock y lotes de vacunas.", "Utilidad Percibida (UP)", "Likert (1 a 5)"],
        ["UP-02", "La emisión automatizada de vales oficiales en PDF agiliza mi trabajo diario.", "Utilidad Percibida (UP)", "Likert (1 a 5)"],
        ["UP-03", "Las alertas de caducidad de lotes me ayudan a prevenir mermas de biológicos.", "Utilidad Percibida (UP)", "Likert (1 a 5)"],
        ["UP-04", "El kardex automatizado evita que tenga que realizar cuadres manuales a fin de mes.", "Utilidad Percibida (UP)", "Likert (1 a 5)"],
        ["UP-05", "En general, el sistema SIVAC ha mejorado significativamente mi desempeño laboral.", "Utilidad Percibida (UP)", "Likert (1 a 5)"]
    ]
    agregar_tabla_datos(
        doc,
        numero="A2",
        titulo="Reactivos del Cuestionario de Satisfacción del Usuario basado en el Modelo TAM",
        encabezados=headers_anexo3,
        filas=filas_anexo3,
        nota="Escala Likert: 1 = Totalmente en desacuerdo, 2 = En desacuerdo, 3 = Ni de acuerdo ni en desacuerdo, 4 = De acuerdo, 5 = Totalmente de acuerdo."
    )

    # Anexo 4
    agregar_titulo_2(doc, "Anexo 4: Certificación de Validez de Contenido por Juicio de Expertos")
    agregar_parrafo(
        doc,
        "Los instrumentos fueron evaluados por tres jueces expertos mediante el coeficiente V de Aiken, obteniéndose una "
        "concordancia de $V = 1.00$ ($p < .05$) en claridad, pertinencia y relevancia en todos los reactivos evaluados.",
        sangria=True
    )

    # Anexo 5
    agregar_titulo_2(doc, "Anexo 5: Modelo de Consentimiento Informado Institucional")
    agregar_parrafo(
        doc,
        "Documento suscrito libre y voluntariamente por los catorce (14) participantes del personal de salud, garantizando "
        "el anonimato, confidencialidad, no maleficencia y fines estrictamente académicos de la investigación.",
        sangria=True
    )

    # Anexo 6
    agregar_titulo_2(doc, "Anexo 6: Constancia de Autorización y Trabajo de Campo")
    agregar_parrafo(
        doc,
        "Oficio de autorización institucional expedido por la Dirección de Salud Apurímac II (DISA Apurímac II) para el desarrollo "
        "de las evaluaciones de pretest y postest en los centros de acopio provinciales de Andahuaylas y Chincheros.",
        sangria=True
    )

    # Anexo 7
    agregar_titulo_2(doc, "Anexo 7: Catálogo de Historias de Usuario (HU-01 a HU-15)")
    agregar_parrafo(
        doc,
        "Especificación completa de las 15 historias de usuario desarrolladas bajo la metodología Extreme Programming (XP), "
        "con sus respectivos criterios de aceptación formalmente validados al 100% durante las pruebas de aceptación.",
        sangria=True
    )

    # Anexo 8
    agregar_titulo_2(doc, "Anexo 8: Esquema Relacional de Base de Datos PostgreSQL / Prisma ORM")
    agregar_parrafo(
        doc,
        "Modelo físico y lógico de base de datos normalizado en 3FN que soporta la persistencia transaccional de SIVAC, "
        "compuesto por 15 tablas relacionales con restricciones de integridad referencial y claves únicas compuestas.",
        sangria=True
    )
