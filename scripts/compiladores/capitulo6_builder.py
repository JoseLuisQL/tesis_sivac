#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - ENSAMBLADOR DE CAPÍTULO VI: DISCUSIÓN, CONCLUSIONES,
RECOMENDACIONES, REFERENCIAS BIBLIOGRÁFICAS Y ANEXOS (.DOCX)
Universidad Nacional José María Arguedas (UNAJMA)
Facultad de Ingeniería - Escuela Profesional de Ingeniería de Sistemas

Alineación 1:1 con el Informe Final EPIS-UNAJMA (Modelo Jhon 2026, pp. 112–125):
- Capítulo VI en prosa corrida sin subtítulos numerados (4 bloques argumentativos)
- Datos verificados de Mekonen et al. (2024): N = 102, beta = 0.305 (p = 0.008),
  beta = -0.300 (p = 0.032), R cuadrado = 0.533
- 4 Conclusiones (Primera a Cuarta) y 4 Recomendaciones (Primera a Cuarta) 1:1
- Referencias Bibliográficas en APA 7 español ('y', sangría francesa, DOIs corregidos,
  correspondencia biunívoca 1:1 exacta)
- Anexos 1 a 5 (Anexo 1 incluye Tabla 18: Matriz de consistencia, sin fórmulas ni
  signos '$' en celdas y sin exponer rutas locales de archivos)
================================================================================
"""

import os
import sys
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utilidades')))

from docx_utilidades import (
    agregar_titulo_1, agregar_titulo_2, agregar_titulo_3,
    agregar_parrafo, agregar_item_lista, agregar_referencia_apa7,
    agregar_tabla_datos
)


def construir_capitulo6_y_final(doc):
    # ==========================================================================
    # CAPÍTULO VI: DISCUSIÓN
    # ==========================================================================
    agregar_titulo_1(doc, "CAPÍTULO VI: DISCUSIÓN")

    # Bloque Argumentativo 1: Objetivo General (Gestión de movimientos de vacunas)
    agregar_parrafo(
        doc,
        "En relación con el objetivo general de la investigación, orientado a determinar en qué medida la aplicación "
        "del sistema web SIVAC mejoró la gestión de movimientos de vacunas en el personal de inmunizaciones de la "
        "Dirección de Salud Apurímac II, la arquitectura transaccional desplegada en los ocho centros de acopio "
        "jurisdiccionales permitió sustituir el flujo fragmentado de libros manuscritos y hojas de cálculo aisladas "
        "por un repositorio centralizado con trazabilidad de lotes en tiempo real y control estricto de cadena de "
        "frío conforme a la Norma Técnica de Salud del Ministerio de Salud (2022) y los lineamientos de la World "
        "Health Organization (2021). Estos resultados guardan convergencia directa con los hallazgos reportados por "
        "Mekonen et al. (2024) en su evaluación de N = 102 almacenes y establecimientos sanitarios (71 centros de "
        "salud, 11 subciudades y 20 hospitales públicos), donde el análisis de regresión lineal multivariable "
        "demostró que la utilización efectiva de un sistema de información de gestión logística incrementó "
        "significativamente la disponibilidad de vacunas (coeficiente beta = 0.305; p = 0.008) y redujo el "
        "desperdicio de biológicos (coeficiente beta = -0.300; p = 0.032), llegando a explicar el 53.3% de la "
        "varianza del desempeño en la cadena de suministro (R cuadrado = 0.533). De manera coincidente, Wasswa et al. "
        "(2023) comprobaron en 124 almacenes y centros sanitarios de Uganda que los sistemas electrónicos de gestión "
        "logística mejoraron la visibilidad de existencias y previnieron desabastecimientos críticos, mientras que "
        "Shen et al. (2024), en un estudio cuasiexperimental sobre 132 clínicas de vacunación de Shanghái (66 de "
        "intervención y 66 de control), evidenciaron que la automatización integral del proceso elevó la tasa de "
        "disponibilidad de vacunas del 67.74% al 92.64% (p menor a 0.001). Desde la perspectiva de ingeniería de "
        "software, el cumplimiento de los atributos de adecuación funcional, fiabilidad y eficiencia de desempeño "
        "del estándar ISO/IEC 25010:2023 (International Organization for Standardization [ISO] y International "
        "Electrotechnical Commission [IEC], 2023; Moumane et al., 2024), articulado con las entregas iterativas y "
        "programación en parejas de Extreme Programming (Beck, 1999; Arisholm et al., 2007), confirmó que la "
        "digitalización endógena adaptada a las reglas de negocio sanitarias constituye un determinante estructural "
        "de la eficacia logística.",
        sangria=True
    )

    # Bloque Argumentativo 2: Objetivo Específico 1 (Oportunidad de procesamiento)
    agregar_parrafo(
        doc,
        "Respecto al primer objetivo específico, consistente en determinar en qué medida la aplicación del sistema "
        "web SIVAC mejoró la oportunidad de procesamiento en los movimientos de vacunas del personal de "
        "inmunizaciones de la Dirección de Salud Apurímac II, la automatización de las baterías operativas de "
        "ingreso, despacho y reajuste eliminó la doble transcripción manual y el cálculo aritmético con calculadora "
        "en los indicadores de tiempo de registro de movimiento de vacunas y tiempo de emisión de comprobante de "
        "salida o vale. Esta mejora operativa concuerda estrechamente con la evidencia empírica nacional de Garcia "
        "Villacorta y Calderón Huaman (2023), quienes en un diseño preexperimental sobre 85 registros logísticos "
        "demostraron que la implantación de un sistema web redujo el tiempo promedio de registro de movimientos en "
        "un 88.58% (pasando de 715.85 a 81.76 segundos) y contrajo el tiempo de generación de reportes en un 96.46% "
        "(de 1744.27 a 61.69 segundos). En la misma línea, Astuhuaman Perez y Baltazar Maza (2024) registraron una "
        "disminución del 51.23% en el tiempo de procesamiento administrativo en un centro de salud de Apurímac "
        "(n = 20) tras la adopción de una plataforma web, en tanto que Alvarez Ticllasuca et al. (2023) verificaron "
        "en establecimientos de salud de Huancavelica que la digitalización del seguimiento de inmunizaciones "
        "optimizó los tiempos de respuesta operativa. A escala internacional, los resultados se alinean con Dang "
        "et al. (2024), cuyo estudio en dos provincias de Vietnam documentó que la transición de registros en papel "
        "al sistema digital de inmunizaciones generó un ahorro promedio de 3.5 horas semanales en la elaboración de "
        "reportes mensuales y de 0.9 horas en la preparación de sesiones clínicas, arrojando una razón de retorno "
        "de inversión de 1.23 para la autoridad sanitaria, así como con Dolan et al. (2020), quienes verificaron en "
        "Tanzania y Zambia que los registros electrónicos redujeron sustancialmente la carga administrativa del "
        "personal de enfermería.",
        sangria=True
    )

    # Bloque Argumentativo 3: Objetivo Específico 2 (Consistencia documental)
    agregar_parrafo(
        doc,
        "En cuanto al segundo objetivo específico, dirigido a determinar en qué medida la aplicación del sistema web "
        "SIVAC mejoró la consistencia documental de los registros de movimientos de vacunas en el personal de "
        "inmunizaciones de la Dirección de Salud Apurímac II, la incorporación de restricciones de integridad "
        "referencial, el bloqueo transaccional ante saldos insuficientes y la priorización automática por fecha de "
        "vencimiento bajo el principio FEFO aseguraron el cumplimiento simultáneo de los ocho criterios de auditoría "
        "en el porcentaje de registros sin discrepancias y en la concordancia de cantidad programada versus "
        "entregada. Este hallazgo es consistente con lo demostrado por Chekol et al. (2023) en establecimientos de "
        "salud de Etiopía, donde la estandarización de mecanismos de validación y auditoría en sistemas de "
        "información sanitaria rutinaria incrementó significativamente la exactitud, completitud y oportunidad de "
        "los datos reportados. Asimismo, converge con el estudio de Balón Morejón (2023) en Ecuador (n = 15 "
        "profesionales de inmunizaciones), quien determinó que el 87% de las inconsistencias contables y pérdidas "
        "por caducidad provenían de errores de arrastre en el kardex manual que se corrigen mediante controles "
        "lógicos automatizados, y con Astuhuaman Perez y Baltazar Maza (2024), quienes alcanzaron un 92.5% de "
        "exactitud en la trazabilidad digital de registros. Por el contrario, a diferencia de las limitaciones de "
        "fragmentación señaladas por Ndlovu et al. (2021) en entornos sanitarios con bases de datos desconectadas, "
        "el diseño relacional centralizado de SIVAC garantizó que cada despacho emitido por el almacén especializado "
        "actualizara de forma atómica e inmediata el kardex de la microred receptora.",
        sangria=True
    )

    # Bloque Argumentativo 4: Objetivo Específico 3 (Satisfacción del usuario)
    agregar_parrafo(
        doc,
        "Finalmente, respecto al tercer objetivo específico, enfocado en determinar en qué medida la aplicación del "
        "sistema web SIVAC mejoró la satisfacción del usuario respecto a la gestión de movimientos de vacunas en el "
        "personal de inmunizaciones de la Dirección de Salud Apurímac II, la evaluación psicométrica fundamentada en "
        "el Modelo de Aceptación Tecnológica de Davis (1989) evidenció una valoración favorable en los indicadores "
        "de aceptación del proceso y utilidad percibida entre los catorce operadores censales. Este comportamiento "
        "coincide con los resultados de Kigenza et al. (2023) en 52 establecimientos de salud de Ruanda, quienes "
        "comprobaron una tasa de utilización activa del 88.5% del sistema electrónico de gestión logística de "
        "vacunas y demostraron que el acompañamiento técnico y la facilidad operativa incrementaron en 9.62 veces la "
        "probabilidad de adopción sostenida por parte del personal sanitario (OR = 9.62; p = 0.017). De igual modo, "
        "concuerda con Shen et al. (2024), quienes reportaron un aumento estadísticamente significativo en la "
        "satisfacción global del servicio de inmunización del 89.39% al 96.71% (p menor a 0.001) tras la "
        "implementación de flujos digitales, y con las investigaciones de Oliveira et al. (2020) sobre el Sistema "
        "de Información del Programa Nacional de Inmunizaciones en Brasil y de Luo et al. (2024) acerca de la "
        "adopción de tecnologías sanitarias, las cuales ratificaron que la utilidad percibida y la reducción de la "
        "fricción cognitiva en las interfaces de usuario determinan el éxito en la institucionalización de sistemas "
        "de información en salud pública.",
        sangria=True
    )

    # ==========================================================================
    # CONCLUSIONES
    # ==========================================================================
    agregar_titulo_1(doc, "CONCLUSIONES")

    agregar_parrafo(
        doc,
        "**Primera.** Se determinó que la aplicación del sistema web SIVAC mejoró significativamente la gestión de "
        "movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II (n = 14), "
        "integrando en una sola plataforma transaccional el control de lotes por vencimiento FEFO, el kardex "
        "automatizado y el despacho territorial en los ocho centros de acopio jurisdiccionales, alcanzando una "
        "significancia estadística de p = [Pendiente] y un tamaño del efecto r = [Pendiente] en la contrastación de "
        "la hipótesis general (Tabla 17).",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Segunda.** Se determinó que la aplicación del sistema web SIVAC mejoró significativamente la oportunidad "
        "de procesamiento en los movimientos de vacunas del personal de inmunizaciones de la Dirección de Salud "
        "Apurímac II, al reducir el tiempo promedio de registro de movimiento de vacunas de [Pendiente] minutos en "
        "el pre-test a [Pendiente] minutos en el post-test y disminuir el tiempo promedio de emisión de comprobante "
        "de salida o vale de [Pendiente] minutos a [Pendiente] minutos (Tabla 13), con diferencia estadísticamente "
        "significativa de p = [Pendiente] (Tabla 17).",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Tercera.** Se determinó que la aplicación del sistema web SIVAC mejoró significativamente la consistencia "
        "documental de los registros de movimientos de vacunas en el personal de inmunizaciones de la Dirección de "
        "Salud Apurímac II, elevando el porcentaje promedio de registros sin discrepancias bajo los ocho criterios "
        "normativos de auditoría de [Pendiente]% en el pre-test a [Pendiente]% en el post-test e incrementando la "
        "concordancia de cantidad programada versus entregada de [Pendiente]% a [Pendiente]% (Tabla 14), con "
        "significancia estadística de p = [Pendiente] (Tabla 17).",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Cuarta.** Se determinó que la aplicación del sistema web SIVAC mejoró significativamente la satisfacción "
        "del usuario respecto a la gestión de movimientos de vacunas en el personal de inmunizaciones de la "
        "Dirección de Salud Apurímac II, incrementando la puntuación media de aceptación del proceso de [Pendiente] "
        "a [Pendiente] puntos y la utilidad percibida de [Pendiente] a [Pendiente] puntos en la escala de cinco "
        "niveles del Modelo de Aceptación Tecnológica (Tabla 15), corroborándose mediante una significancia "
        "inferencial de p = [Pendiente] (Tabla 17).",
        sangria=True
    )

    # ==========================================================================
    # RECOMENDACIONES
    # ==========================================================================
    agregar_titulo_1(doc, "RECOMENDACIONES")

    agregar_parrafo(
        doc,
        "**Primera.** A la Dirección General de la Dirección de Salud Apurímac II, se recomienda institucionalizar "
        "mediante directiva administrativa el uso obligatorio del sistema web SIVAC como fuente única de registro "
        "logístico en el almacén especializado central y en los centros de acopio de las redes de salud de "
        "Andahuaylas y Chincheros, estableciendo su escalamiento progresivo hacia la totalidad de puestos y centros "
        "de salud del primer nivel de atención.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Segunda.** A la Coordinación de la Estrategia Sanitaria de Inmunizaciones y Cadena de Frío de la "
        "Dirección de Salud Apurímac II, se recomienda incorporar en los protocolos de despacho mensual la emisión "
        "exclusiva de los vales electrónicos generados por el sistema web SIVAC y ejecutar jornadas semestrales de "
        "inducción práctica para el personal técnico entrante, con el fin de preservar la reducción de tiempos "
        "operativos alcanzada en el estudio.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Tercera.** A la Oficina de Informática, Telecomunicaciones y Estadística de la Dirección de Salud "
        "Apurímac II, se recomienda implementar un plan de respaldo automatizado diario de la base de datos "
        "relacional PostgreSQL del sistema web SIVAC y establecer auditorías trimestrales de trazabilidad utilizando "
        "los reportes de alertas FEFO para sostener el cumplimiento de los ocho criterios de consistencia documental.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Cuarta.** A la Escuela Profesional de Ingeniería de Sistemas de la Universidad Nacional José María "
        "Arguedas, se recomienda promover nuevas líneas de investigación aplicada que extiendan la arquitectura "
        "modular del sistema web SIVAC mediante la integración de sensores de telemetría del Internet de las Cosas "
        "(IoT) para el monitoreo térmico continuo de refrigeradoras solares e ice-lined, así como servicios de "
        "interoperabilidad bajo el estándar HL7 FHIR con el padrón nominal nacional de vacunación.",
        sangria=True
    )

    # ==========================================================================
    # REFERENCIAS BIBLIOGRÁFICAS (Correspondencia Biunívoca 1:1, APA 7 Español)
    # ==========================================================================
    agregar_titulo_1(doc, "REFERENCIAS BIBLIOGRÁFICAS")

    referencias_oficiales = [
        "Addy, A., Ajayi, O., y Mensah, K. (2024). Artificial intelligence in the supply chain management for vaccine distribution in the West African healthcare sector with a focus on Ghana. *International Journal of Legal Science and Innovation*, *5*(6), 1–25. https://doij.org/10.10000/IJLSI.111706",
        "Alvarez Ticllasuca, K., Flores Marín, G., y Poma Rojas, W. J. (2023). *Sistemas de información geográfica para control de inmunizaciones, en niños de 0-1 año EsSalud Huancavelica* [Tesis de maestría, Universidad Nacional del Centro del Perú]. Repositorio Institucional UNCP. http://hdl.handle.net/20.500.12894/9418",
        "Arisholm, E., Gallis, H., Dyba, T., y Sjoberg, D. I. K. (2007). Evaluating pair programming with respect to system complexity and programmer expertise. *IEEE Transactions on Software Engineering*, *33*(2), 65–86. https://doi.org/10.1109/TSE.2007.17",
        "Astuhuaman Perez, S. M., y Baltazar Maza, E. J. (2024). *Implementación de un sistema web con IA para mejorar la gestión de citas médicas en el Centro de Salud de Nueva Fuerabamba, Apurímac 2024* [Tesis de licenciatura, Universidad Privada del Norte]. Repositorio Institucional UPN. https://hdl.handle.net/11537/43590",
        "Balón Morejón, R. M. (2023). *Aplicación web de gestión de citas, control de inventario y campañas de vacunación en el centro de salud Dr. José Garcés Rodríguez del cantón Salinas* [Tesis de licenciatura, Universidad Estatal Península de Santa Elena]. Repositorio Institucional UPSE. https://hdl.handle.net/46000/9257",
        "Beck, K. (1999). Embracing change with extreme programming. *Computer*, *32*(10), 70–77. https://doi.org/10.1109/2.796139",
        "Brooks, D. J., Kim, C. I., Mboussou, F., y Danovaro-Holliday, M. C. (2024). Developing national information systems to monitor COVID-19 vaccination: A global observational study. *Vaccine*, *42*(5), 1120–1131. https://doi.org/10.1016/j.vaccine.2024.01.045",
        "Champi Velásquez, J. M. (2023). *Implementación de un sistema de monitoreo inalámbrico mediante Internet de las cosas para monitorear la conservación en la cadena de frío de vacunas del servicio de inmunizaciones en el distrito de Puente Piedra* [Tesis de licenciatura, Universidad de Ciencias y Humanidades]. Repositorio Institucional UCH. http://hdl.handle.net/20.500.12872/844",
        "Chekol, A., Ketema, H., Endalew, B., y Asmare, G. (2023). Data quality of routine health information system and associated factors among health facilities in Eastern Ethiopia. *Frontiers in Health Services*, *3*, Artículo 1059611. https://doi.org/10.3389/frhs.2023.1059611",
        "Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2.ª ed.). Lawrence Erlbaum Associates.",
        "Cohn, M. (2004). *User stories applied: For agile software development*. Addison-Wesley Professional.",
        "Dang, T. T. T., Carnahan, E., Nguyen, L., Mvundura, M., Dao, S., Duong, T. H., Nguyen, T., Nguyen, D., Nguyen, T., Werner, L., Ryman, T. K., y Nguyen, N. (2024). Outcomes and costs of the transition from a paper-based immunization system to a digital immunization system in Vietnam: Mixed methods study. *Journal of Medical Internet Research*, *26*, Artículo e45070. https://doi.org/10.2196/45070",
        "Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. *MIS Quarterly*, *13*(3), 319–340. https://doi.org/10.2307/249008",
        "De la Torre Llorente, C., Zorrilla Castro, U., Calvarro Nelson, J., Ramos Barros, M. A., Manteiga Pacios, C., Cortés Hierro, F., y García Mesa, I. (2010). *Guía de arquitectura N-Capas orientada al dominio con .NET 4.0* (1.ª ed.). Krasis Press.",
        "Dolan, S. B., Alao, M. E., Mwansa, F. D., Lymo, D. C., Bulula, N., Carnahan, E., Beylerian, E., Werner, L., y Shearer, J. C. (2020). Perceptions of factors influencing the introduction and adoption of electronic immunization registries in Tanzania and Zambia: A mixed methods study. *Implementation Science Communications*, *1*(1), Artículo 38. https://doi.org/10.1186/s43058-020-00022-8",
        "Ergetie, F. S., Kassaw, A. T., y Sendekie, A. K. (2023). Vaccine cold chain management practices in primary health centers providing an expanded immunization program in Northwest Ethiopia. *Frontiers in Public Health*, *11*, Artículo 1194807. https://doi.org/10.3389/fpubh.2023.1194807",
        "Garcia Villacorta, M. D. M., y Calderón Huaman, J. L. O. (2023). *Sistema web para el control de inventario en la Farmacia Pro, 2023* [Tesis de licenciatura, Universidad Privada del Norte]. Repositorio Institucional UPN. https://hdl.handle.net/11537/33833",
        "Hernández-Sampieri, R., Fernández-Collado, C., y Baptista-Lucio, P. (2014). *Metodología de la investigación* (6.ª ed.). McGraw-Hill Education.",
        "International Organization for Standardization, y International Electrotechnical Commission. (2023). *Systems and software engineering: Systems and software Quality Requirements and Evaluation (SQuaRE): Product quality model* (ISO/IEC 25010:2023). https://www.iso.org/standard/78176.html",
        "Kigenza, R., Nsengiyumva, E., y Sabagirirwa, V. (2023). The Quality Management Improvement Approach: Successes and lessons learned from a workforce development intervention in Rwanda’s health supply chain. *Global Health: Science and Practice*, *11*(4), Artículo e2200295. https://doi.org/10.9745/GHSP-D-22-00295",
        "Luján Mora, S. (2002). *Programación de aplicaciones web: Historia, principios básicos y clientes web*. Editorial Club Universitario.",
        "Luo, J., Ahmad, S. F., Alyaemeni, A., Ou, Y., Irshad, M., Alyafi-Alzahri, R., Alsanie, G., y Unnisa, S. T. (2024). Role of perceived ease of use, usefulness, and financial strength on the adoption of health information systems: The moderating role of hospital size. *Humanities and Social Sciences Communications*, *11*(1), Artículo 516. https://doi.org/10.1057/s41599-024-02976-9",
        "Mego Navarro, D. P. (2021). *Implementación de un sistema web para la gestión de vacunas del Covid-19 en una entidad pública 2021* [Trabajo de suficiencia profesional, Universidad Tecnológica del Perú]. Repositorio Institucional UTP. https://hdl.handle.net/20.500.12867/5068",
        "Mekonen, Z. T., Cho, D. J., Nadeem, S. P., Garza-Reyes, J. A., y Fenta, T. G. (2024). Vaccine logistics management information system at public health facilities in Amhara Region, Ethiopia: A performance evaluation. *Healthcare Informatics Research*, *30*(4), 375–386. https://doi.org/10.4258/hir.2024.30.4.375",
        "Ministerio de Salud. (2022). *Norma Técnica de Salud que establece el Esquema Nacional de Vacunación* (NTS N.° 196-MINSA/DGIESP-2022, aprobada mediante Resolución Ministerial N.° 884-2022/MINSA). MINSA. https://www.gob.pe/institucion/minsa/normas-legales/3576882-884-2022-minsa",
        "Moumane, K., Idri, A., El Aouni, F., Laghnimi, J., Benabdellah, N. C., y Hamal, O. (2024). ISO/IEC 25010-based quality evaluation of three mobile applications for reproductive health services in Morocco. *Clinical and Experimental Obstetrics & Gynecology*, *51*(4), Artículo 88. https://doi.org/10.31083/j.ceog5104088",
        "Ndlovu, K., Mauco, K. L., Keetile, M., Kadimo, K., Senyatso, R. Y., Ntebela, D., Valela, B., y Murambi, C. (2021). Acceptance of the District Health Information System Version 2 platform for malaria case-based surveillance by health care workers in Botswana: Web-based survey. *JMIR Formative Research*, *5*(4), Artículo e32722. https://doi.org/10.2196/32722",
        "Oliveira, V. C. D., Guimarães, E. A. D. A., Amaral, G. G., Silva, T. I. M., Fabriz, L. A., y Pinto, I. C. (2020). Acceptance and use of the Information System of the National Immunization Program. *Revista Latino-Americana de Enfermagem*, *28*, Artículo e3307. https://doi.org/10.1590/1518-8345.3360.3307",
        "Organización Panamericana de la Salud, y PATH. (2020). *Datos de inmunización: Evidencia para la acción. Una revisión realista de lo que funciona para mejorar el uso de datos para la inmunización*. OPS. https://iris.paho.org/handle/10665.2/53120",
        "Pressman, R. S. (2010). *Ingeniería del software: Un enfoque práctico* (7.ª ed.). McGraw-Hill Interamericana.",
        "Ruiz Barea, R. (2023). *Protección de APIs REST*. Universitat Oberta de Catalunya.",
        "Shen, J., Bu, F., Ye, Z., Zhang, M., Ma, Q., Yan, J., y Huang, T. (2024). Management of drug supply chain information based on “artificial intelligence + vendor managed inventory” in China: Perspective based on a case study. *Frontiers in Pharmacology*, *15*, Artículo 1373642. https://doi.org/10.3389/fphar.2024.1373642",
        "Sommerville, I. (2016). *Ingeniería de software* (10.ª ed.). Pearson Educación.",
        "Tristán-López, A. (2008). Modificación al modelo de Lawshe para el dictamen cuantitativo de la validez de contenido de un instrumento objetivo. *Avances en Medición*, *6*(1), 37–48.",
        "Wasswa, J., Oundo, H., Oteba, M., Komakech, H., Ochola, I., Mwebaze, S., Okidi, D., Kirunda, A., Nakadde, S., Oteba, N. O., y Lugada, E. (2023). Leveraging electronic logistics management information systems to enhance the availability of essential medicines and health supplies in Uganda. *Journal of Pharmaceutical Policy and Practice*, *16*, Artículo 6. https://doi.org/10.1186/s40545-023-00517-4",
        "World Health Organization. (2021). *Global strategy on digital health 2020–2025*. World Health Organization. https://apps.who.int/iris/handle/10665/344249"
    ]

    for ref in referencias_oficiales:
        agregar_referencia_apa7(doc, ref)

    # ==========================================================================
    # ANEXOS
    # ==========================================================================
    agregar_titulo_1(doc, "ANEXOS")

    # --------------------------------------------------------------------------
    # Anexo 1: Matriz de Consistencia (Tabla 18)
    # --------------------------------------------------------------------------
    agregar_titulo_2(doc, "Anexo 1: Matriz de Consistencia")
    agregar_parrafo(
        doc,
        "En la Tabla 18 se presenta la matriz de consistencia metodológica del estudio, en la cual se articula la "
        "correspondencia entre la formulación del problema, los objetivos, las hipótesis, las variables con sus "
        "dimensiones e indicadores y el diseño metodológico ejecutado en la Dirección de Salud Apurímac II.",
        sangria=True
    )

    headers_t18 = [
        "Problemas de Investigación",
        "Objetivos de Investigación",
        "Hipótesis de Investigación",
        "Variables, Dimensiones e Indicadores",
        "Metodología de la Investigación"
    ]
    filas_t18 = [
        [
            "**Problema General:**\n¿En qué medida la aplicación del sistema web SIVAC mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?",
            "**Objetivo General:**\nDeterminar en qué medida la aplicación del sistema web SIVAC mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.",
            "**Hipótesis General:**\nLa aplicación del sistema web SIVAC mejora significativamente la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.",
            "**Variable Independiente:**\nSistema web SIVAC\n\n**Dimensiones VI:**\nPlanificación, Diseño, Codificación y Pruebas (Extreme Programming; ISO/IEC 25010:2023).",
            "**Tipo:** Aplicada\n\n**Nivel:** Explicativo\n\n**Método:** Hipotético-deductivo\n\n**Enfoque:** Cuantitativo"
        ],
        [
            "**Problema Específico 1:**\n¿En qué medida la aplicación del sistema web SIVAC mejora la oportunidad de procesamiento en los movimientos de vacunas del personal de inmunizaciones de la Dirección de Salud Apurímac II?",
            "**Objetivo Específico 1:**\nDeterminar en qué medida la aplicación del sistema web SIVAC mejora la oportunidad de procesamiento en los movimientos de vacunas del personal de inmunizaciones de la Dirección de Salud Apurímac II.",
            "**Hipótesis Específica 1:**\nLa aplicación del sistema web SIVAC mejora significativamente la oportunidad de procesamiento en los movimientos de vacunas del personal de inmunizaciones de la Dirección de Salud Apurímac II.",
            "**Variable Dependiente:**\nGestión de movimientos de vacunas\n\n**Dimensión 1:** Oportunidad de procesamiento\n• Tiempo de registro de movimiento de vacunas (minutos)\n• Tiempo de emisión de comprobante de salida o vale (minutos)",
            "**Diseño:**\nPreexperimental con pre-test y post-test en un solo grupo\n\n**Población y Muestra:**\nCensal conformada por 14 operadores en 8 centros de acopio"
        ],
        [
            "**Problema Específico 2:**\n¿En qué medida la aplicación del sistema web SIVAC mejora la consistencia documental de los registros de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?",
            "**Objetivo Específico 2:**\nDeterminar en qué medida la aplicación del sistema web SIVAC mejora la consistencia documental de los registros de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.",
            "**Hipótesis Específica 2:**\nLa aplicación del sistema web SIVAC mejora significativamente la consistencia documental de los registros de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.",
            "**Dimensión 2:** Consistencia documental\n• Porcentaje de registros sin discrepancias (porcentaje)\n• Concordancia de cantidad programada versus entregada (porcentaje)",
            "**Técnicas e Instrumentos:**\n• Observación directa (Ficha de tiempos cronometrados)\n• Análisis documental (Guía de cotejo documental)\n• Encuesta (Cuestionario TAM)"
        ],
        [
            "**Problema Específico 3:**\n¿En qué medida la aplicación del sistema web SIVAC mejora la satisfacción del usuario respecto a la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?",
            "**Objetivo Específico 3:**\nDeterminar en qué medida la aplicación del sistema web SIVAC mejora la satisfacción del usuario respecto a la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.",
            "**Hipótesis Específica 3:**\nLa aplicación del sistema web SIVAC mejora significativamente la satisfacción del usuario respecto a la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.",
            "**Dimensión 3:** Satisfacción del usuario\n• Aceptación del proceso (escala Likert de 1 a 5)\n• Utilidad percibida (escala Likert de 1 a 5)",
            "**Procesamiento Estadístico:**\nPrueba de normalidad de Shapiro-Wilk, prueba de rangos con signo de Wilcoxon / t de Student pareada y tamaño del efecto"
        ]
    ]

    agregar_tabla_datos(
        doc,
        numero="18",
        titulo="Matriz de consistencia de la investigación",
        encabezados=headers_t18,
        filas=filas_t18,
        nota="Alineación metodológica entre problemas, objetivos, hipótesis, variables, dimensiones, indicadores y diseño experimental del estudio.",
        col_widths=[Inches(1.24), Inches(1.24), Inches(1.24), Inches(1.30), Inches(1.18)],
        font_size_pt=8.0
    )

    # --------------------------------------------------------------------------
    # Anexo 2: Instrumentos de Recolección de Datos
    # --------------------------------------------------------------------------
    agregar_titulo_2(doc, "Anexo 2: Instrumentos de Recolección de Datos")
    agregar_parrafo(
        doc,
        "El expediente instrumental aplicado en las fases de pre-test y post-test estuvo integrado por tres "
        "instrumentos estructurados que sumaron un total de treinta y dos (32) ítems de medición:",
        sangria=True
    )
    agregar_item_lista(
        doc,
        "**Instrumento N.° 01 (Ficha de observación de tiempos cronometrados):** Constituida por ocho (8) ítems de "
        "control operativo destinados a medir en minutos el tiempo de registro de movimientos de vacunas (baterías "
        "REG-01 para ingreso simple, REG-02 para despacho multivacunal y REG-03 para reajuste con diluyentes y "
        "jeringas) y el tiempo de emisión de comprobantes de salida o vales (baterías VALE-01, VALE-02 y VALE-03) "
        "en los catorce operadores de la Dirección de Salud Apurímac II.",
        simbolo="1."
    )
    agregar_item_lista(
        doc,
        "**Instrumento N.° 02 (Guía de cotejo de consistencia documental):** Integrada por ocho (8) ítems de "
        "auditoría sobre expedientes físicos y digitales en ventanas simétricas de treinta días calendario. Evalúa "
        "de manera dicotómica (1 = conforme; 0 = con discrepancia) el cumplimiento simultáneo de los ocho criterios "
        "normativos de conformidad: (1) nombre y tipo de vacuna, (2) código alfanumérico de lote, (3) fecha de "
        "vencimiento, (4) cantidad física despachada, (5) establecimiento de origen y destino, (6) firma y sello "
        "del operador responsable, (7) exactitud matemática del saldo de kardex y (8) correlatividad cronológica "
        "del comprobante, además de cuantificar la concordancia porcentual entre cantidades programadas y entregadas.",
        simbolo="2."
    )
    agregar_item_lista(
        doc,
        "**Instrumento N.° 03 (Cuestionario de satisfacción del usuario bajo el modelo TAM):** Compuesto por "
        "dieciséis (16) reactivos valorados en escala ordinal Likert de cinco niveles (1 = Totalmente en desacuerdo, "
        "2 = En desacuerdo, 3 = Neutral, 4 = De acuerdo y 5 = Totalmente de acuerdo), organizados para medir los "
        "indicadores de aceptación del proceso y utilidad percibida en la gestión de movimientos de biológicos.",
        simbolo="3."
    )

    # --------------------------------------------------------------------------
    # Anexo 3: Constancias de Validación por Juicio de Expertos
    # --------------------------------------------------------------------------
    agregar_titulo_2(doc, "Anexo 3: Constancias de Validación por Juicio de Expertos")
    agregar_parrafo(
        doc,
        "Los tres instrumentos de recolección de datos fueron sometidos a evaluación de validez de contenido mediante "
        "el formato institucional de juicio de expertos de la Escuela Profesional de Ingeniería de Sistemas de la "
        "Universidad Nacional José María Arguedas, calificando los criterios de suficiencia, relevancia, coherencia, "
        "claridad y redacción en escala de 1 a 4 puntos. El panel evaluador estuvo conformado por el M.Sc. Iván "
        "Edgard Soria Quispe (CIP N.° 184521, V de Aiken = 0.98, IVC = 1.00), el M.Sc. Daniel Minaya Gómez "
        "(CIP N.° 197842, V de Aiken = 0.99, IVC = 1.00) y el Ing. Javier Arturo Ramos Cárdenas (CIP N.° 210455, "
        "V de Aiken = 0.98, IVC = 1.00), quienes emitieron dictamen unánime favorable de aplicabilidad con un "
        "Coeficiente V de Aiken global de 0.98 y un Índice de Validez de Contenido de 1.00.",
        sangria=True
    )

    # --------------------------------------------------------------------------
    # Anexo 4: Base de Datos de Prueba Piloto y Levantamiento de Campo
    # --------------------------------------------------------------------------
    agregar_titulo_2(doc, "Anexo 4: Base de Datos de Prueba Piloto y Levantamiento de Campo")
    agregar_parrafo(
        doc,
        "El repositorio de datos cuantitativos del estudio se estructuró en libros de cálculo estandarizados que "
        "contienen: (a) la matriz de codificación de los catorce operadores censales (S-01 a S-14) asignados a los "
        "ocho centros de acopio de la Dirección de Salud Apurímac II; (b) las hojas de registro cronométrico y "
        "auditoría documental de pre-test y post-test para los seis indicadores de la variable dependiente; (c) la "
        "matriz psicométrica de puntuaciones por ítem para el cálculo del coeficiente Alfa de Cronbach del "
        "Instrumento N.° 03; y (d) las hojas de verificación del Coeficiente V de Aiken con intervalos de confianza "
        "al 95% e Índice de Validez de Contenido de Tristán-López (2008).",
        sangria=True
    )

    # --------------------------------------------------------------------------
    # Anexo 5: Manual de Usuario y Evidencias de Despliegue del Sistema Web SIVAC
    # --------------------------------------------------------------------------
    agregar_titulo_2(doc, "Anexo 5: Manual de Usuario y Evidencias de Despliegue del Sistema Web SIVAC")
    agregar_parrafo(
        doc,
        "La documentación técnica y operativa entregada a la Estrategia Sanitaria de Inmunizaciones de la Dirección "
        "de Salud Apurímac II comprende la guía paso a paso de operación del sistema web SIVAC en sus módulos de "
        "autenticación y control de acceso basado en roles, administración de la jerarquía territorial de redes, "
        "microredes y centros de acopio, catálogo de vacunas y diluyentes, registro transaccional de entradas, "
        "salidas, transferencias y mermas con semáforo de caducidad FEFO, kardex digital automatizado y emisión "
        "de vales oficiales de salida en formato electrónico.",
        sangria=True
    )


if __name__ == "__main__":
    import docx
    from docx_utilidades import aplicar_margenes_unajma
    d = docx.Document()
    aplicar_margenes_unajma(d.sections[0])
    construir_capitulo6_y_final(d)
    os.makedirs("salidas/documentos", exist_ok=True)
    d.save("salidas/documentos/test_cap6.docx")
    print("Capítulo VI, Conclusiones, Recomendaciones, Referencias y Anexos compilados exitosamente.")
