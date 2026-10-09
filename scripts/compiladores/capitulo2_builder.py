#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - ENSAMBLADOR DE CAPÍTULO II: ANTECEDENTES (.DOCX)
Universidad Nacional José María Arguedas (UNAJMA)
Estructura Oficial de Informe Final de Tesis EPIS-UNAJMA
================================================================================
"""

from docx_utilidades import (
    agregar_titulo_1, agregar_titulo_2, agregar_parrafo
)


def construir_capitulo2(doc):
    agregar_titulo_1(doc, "CAPÍTULO II: ANTECEDENTES")

    # 2.1. Antecedentes internacionales
    agregar_titulo_2(doc, "2.1. Antecedentes internacionales")

    agregar_parrafo(
        doc,
        "Shen et al. (2024), en su artículo científico titulado “Management of drug supply chain "
        "information based on ‘artificial intelligence + vendor managed inventory’ in China: "
        "Perspective based on a case study”, publicado en la revista indexada Frontiers in "
        "Pharmacology, tuvieron como objetivo evaluar la optimización del flujo de información "
        "en la cadena de suministro de medicamentos hospitalarios mediante la implementación de "
        "una plataforma digital en la nube basada en gestión de inventario administrado por el "
        "proveedor e inteligencia artificial (p. 1). Metodológicamente, la investigación "
        "correspondió a un estudio de caso cuantitativo longitudinal con mediciones antes y "
        "después de la intervención tecnológica en el Primer Hospital Afiliado de la Universidad "
        "Médica de Nanjing, auditando los registros transaccionales de almacén y abastecimiento. "
        "Los resultados demostraron una reducción de la tasa de roturas de stock de 0.425% a "
        "0.277%, una disminución del tiempo de inmovilización de inventarios cercana al 20% y un "
        "incremento del 42.4% en la eficiencia operativa global de la cadena de suministro "
        "(p. 1). Los autores concluyeron que la centralización digital de los registros de "
        "inventario elimina las asimetrías de información entre almacenes, disminuye los errores "
        "administrativos de conciliación y garantiza la disponibilidad continua de insumos "
        "farmacéuticos críticos.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Dang et al. (2024), en su investigación longitudinal titulada “Outcomes and costs of "
        "the transition from a paper-based immunization system to a digital immunization system "
        "in Vietnam: Mixed methods study”, publicada en el Journal of Medical Internet Research, "
        "se propusieron evaluar los resultados operativos, la oportunidad de registro y los "
        "costos derivados de la transición desde un sistema de inmunización basado en libros "
        "físicos de papel hacia el Sistema Nacional de Información de Inmunizaciones digital en "
        "Vietnam. El estudio empleó un diseño mixto con evaluaciones comparativas pre-test y "
        "post-test en centros de salud comunales y almacenes distritales de las provincias de "
        "Hanói y Son La, aplicando observación cronometrada de flujos de trabajo y auditoría de "
        "registros de vacunas. Los hallazgos evidenciaron que el tiempo requerido para disponer "
        "de los registros consolidados en el sistema se redujo de 43.7 a 0.7 días, lo que "
        "representó una mejora del 98% en la oportunidad de procesamiento de los datos, además "
        "de registrar un 38% menos de carga operativa en el personal sanitario encargado de "
        "las inmunizaciones. La investigación concluyó que el reemplazo definitivo de los "
        "formatos en papel por una arquitectura web centralizada acelera la trazabilidad de "
        "las vacunas, incrementa la calidad de los datos reportados y libera tiempo operativo "
        "del personal de salud.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Kigenza et al. (2023), en su estudio cuasiexperimental titulado “The Quality Management "
        "Improvement Approach: Successes and lessons learned from a workforce development "
        "intervention in Rwanda’s health supply chain”, publicado en la revista Global Health: "
        "Science and Practice, tuvieron como objetivo determinar el efecto de una intervención "
        "de gestión de calidad apoyada en el sistema electrónico de información de gestión "
        "logística (e-LMIS) sobre el desempeño de la cadena de suministro de salud pública en "
        "Ruanda. El diseño metodológico fue cuantitativo, longitudinal y de alcance nacional, "
        "evaluando una muestra de 596 establecimientos de salud, 30 almacenes distritales y "
        "1,296 operadores logísticos mediante listas de verificación de inventarios y reportes "
        "transaccionales del sistema. Los resultados determinaron que la utilización estandarizada "
        "del sistema electrónico aumentó del 55% al 96%, la exactitud de los datos de inventario "
        "entre el saldo físico y el saldo digital se incrementó del 25% al 85%, y la tasa de "
        "desabastecimiento de insumos se redujo del 10% a menos del 1%. Los autores concluyeron "
        "que la integración del sistema informático e-LMIS con protocolos estandarizados de "
        "control de calidad asegura la consistencia documental de los inventarios y previene "
        "quiebres de stock en las redes de salud.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Balón Morejón (2023), en su tesis de ingeniería titulada “Aplicación web de gestión de "
        "citas, control de inventario y campañas de vacunación en el centro de salud Dr. José "
        "Garcés Rodríguez del cantón Salinas”, sustentada en la Universidad Estatal Península "
        "de Santa Elena en Ecuador, planteó como objetivo desarrollar e implementar una "
        "aplicación web para optimizar el control de inventario de medicamentos, el registro "
        "de biológicos y el seguimiento de campañas de vacunación (p. xii). La investigación "
        "fue de tipo aplicada, con enfoque cuantitativo y diseño descriptivo-propositivo, "
        "diagnosticando que el manejo previo en hojas de cálculo y registros manuales generaba "
        "duplicidad de información, pérdida de trazabilidad de lotes y demoras prolongadas en "
        "la entrega de balances mensuales (p. 10). Los resultados posteriores a la puesta en "
        "producción del sistema web demostraron que el tiempo requerido para consolidar el "
        "inventario y emitir los reportes de stock disminuyó de un rango de 3 a 4 días hábiles "
        "a 6 segundos, eliminando por completo los registros duplicados y automatizando las "
        "alertas de fechas de caducidad (p. xii). El autor concluyó que la sistematización web "
        "del almacén de vacunación agiliza la emisión documental, garantiza la fiabilidad de "
        "los saldos disponibles y eleva la satisfacción operativa de los usuarios institucionales.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Ergetie et al. (2023), en su investigación multicéntrica titulada “Vaccine cold chain "
        "management practices in primary health centers providing an expanded immunization "
        "program in Northwest Ethiopia”, publicada en Frontiers in Public Health, tuvieron como "
        "objetivo evaluar el nivel de conocimiento y las prácticas operativas de gestión de la "
        "cadena de frío e inventario de vacunas en establecimientos de atención primaria (p. 1). "
        "El estudio aplicó un diseño observacional transversal cuantitativo sobre el personal "
        "responsable de inmunizaciones en centros de salud públicos del noroeste de Etiopía, "
        "empleando cuestionarios estructurados y guías de observación técnica de almacenes "
        "biológicos. Los resultados revelaron que el 60% de los profesionales evaluados "
        "presentó un buen nivel de conocimiento y el 74% registró una buena práctica general "
        "en el manejo de la cadena de frío (p. 1); no obstante, se identificó que el 68% de los "
        "establecimientos mantenía deficiencias en la actualización del sistema de información "
        "logística y el 50% carecía de registros completos de movimientos debido al uso "
        "exclusivo de formatos manuales en papel (p. 7). Los autores concluyeron que las "
        "limitaciones en el registro documental y en el control sistematizado de existencias "
        "constituyen un factor crítico de vulnerabilidad para la trazabilidad e integridad de "
        "las vacunas en el primer nivel de atención.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Wasswa et al. (2023), en su estudio evaluativo titulado “Leveraging electronic "
        "logistics management information systems to enhance and optimize supply chain response "
        "during public health emergencies: Lessons from COVID-19 response in Uganda”, publicado "
        "en el Journal of Pharmaceutical Policy and Practice, se plantearon como objetivo "
        "analizar el desempeño del sistema electrónico de información de gestión logística "
        "para optimizar la distribución, trazabilidad y disponibilidad de vacunas e insumos "
        "sanitarios a escala nacional. La metodología fue cuantitativa, descriptiva y "
        "transversal, auditando las transacciones digitales de pedidos, despachos y saldos de "
        "almacén ejecutadas en la red pública del Ministerio de Salud de Uganda. Los resultados "
        "demostraron que el procesamiento digital de requisiciones y comprobantes de despacho "
        "permitió monitorear en tiempo real los lotes distribuidos y mantener una "
        "disponibilidad promedio del 90% en 19 hospitales regionales de referencia, reduciendo "
        "sustancialmente los tiempos de respuesta frente a los procedimientos manuales. El "
        "estudio concluyó que los sistemas web de gestión logística fortalecen la visibilidad "
        "de extremo a extremo en la cadena de frío, aseguran la concordancia entre las "
        "cantidades solicitadas y las despachadas, y previenen el desabastecimiento de "
        "productos biológicos.",
        sangria=True
    )

    # 2.2. Antecedentes nacionales
    agregar_titulo_2(doc, "2.2. Antecedentes nacionales")

    agregar_parrafo(
        doc,
        "Astuhuaman Perez y Baltazar Maza (2024), en su tesis de grado desarrollada en la "
        "Universidad Nacional José María Arguedas titulada “Implementación de un sistema web "
        "con IA para mejorar la gestión de citas médicas en el Centro de Salud de Nueva "
        "Fuerabamba, Apurímac 2024”, tuvieron como objetivo determinar en qué medida la "
        "aplicación de un sistema web mejora la gestión operativa y los tiempos de "
        "procesamiento en un establecimiento de salud de la región Apurímac (p. 17). La "
        "investigación se desarrolló bajo el enfoque cuantitativo, de tipo aplicada, nivel "
        "explicativo y diseño preexperimental con pre-test y post-test en un solo grupo sobre "
        "una muestra censal de 12 trabajadores del establecimiento y 30 usuarios, empleando "
        "fichas de observación cronometrada (p. 56). Los resultados empíricos demostraron una "
        "reducción del tiempo promedio de registro y elaboración de procesos de 9.97 a 8.47 "
        "minutos, equivalente a una mejora del 15.1%, alcanzando significancia estadística en "
        "la prueba de rangos con signo de Wilcoxon con p < 0.001, además de reducir el tiempo "
        "de actualización de registros de 6.10 a 4.60 minutos (p. 87). Los autores concluyeron "
        "que la implementación de sistemas web en establecimientos públicos de salud del "
        "departamento de Apurímac disminuye de manera significativa los tiempos operativos "
        "del personal e incrementa su productividad administrativa.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Mego Navarro (2021), en su investigación titulada “Implementación de un sistema web "
        "para la gestión de vacunas del Covid-19 en una entidad pública 2021”, sustentada en "
        "la Universidad Tecnológica del Perú, planteó como objetivo implementar una plataforma "
        "web para optimizar los procesos de distribución, seguimiento y control de inventarios "
        "de vacunas en una institución sanitaria pública aplicando la metodología ágil Extreme "
        "Programming (p. 39). Metodológicamente, fue un estudio aplicado de enfoque "
        "cuantitativo que estructuró la construcción del software en las cuatro fases de "
        "Extreme Programming (planificación, diseño, codificación y pruebas) y evaluó una "
        "muestra de 40 operadores informáticos y estadísticos vinculados a la gestión vacunal. "
        "En el diagnóstico inicial se determinó que el 45% del personal debía trasladarse "
        "físicamente a los centros de salud para recabar información de vacunas, el 30% "
        "utilizaba correos electrónicos aislados y el 25% de los reportes presentaba "
        "inconsistencias por falta de estandarización (p. 32); tras el despliegue del sistema "
        "web, el 87.5% de los usuarios accedió a la información centralizada en tiempo real "
        "y la completitud de los registros de vacunas se elevó del 50% al 95% (p. 113). El "
        "autor concluyó que el desarrollo de aplicaciones web mediante Extreme Programming "
        "permite entregar incrementos funcionales adaptados a las normas sanitarias peruanas, "
        "optimizando el control y la disponibilidad oportuna de los datos de inmunización.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Garcia Villacorta y Calderón Huaman (2023), en su tesis de ingeniería titulada "
        "“Sistema web para el control de inventario en la Farmacia Pro, 2023”, presentada en "
        "la Universidad Privada del Norte, tuvieron como objetivo determinar en qué medida la "
        "implementación de un sistema web mejora el control de inventario de productos "
        "farmacéuticos. El estudio fue de tipo aplicada, con enfoque cuantitativo, nivel "
        "explicativo y diseño preexperimental con pre-test y post-test en un solo grupo, "
        "evaluando una muestra de 68 registros documentales de inventario (34 en pre-test y "
        "34 en post-test) mediante fichas de observación y cotejo de existencias. Los "
        "resultados cuantitativos evidenciaron que, tras la puesta en operación del sistema "
        "web, la exactitud del control de inventario entre el stock físico y el registrado "
        "aumentó de 75.42% a 97.18%, la rotación de existencias se incrementó de 76.78% a "
        "97.44% y el cumplimiento de entregas conformes y oportunas subió de 76.15% a 97.77%, "
        "obteniendo en la contrastación inferencial un estadístico Z = -7.15 con p < 0.001. "
        "Los autores concluyeron que la automatización de las entradas, salidas y kardex "
        "mediante un sistema web erradica las discrepancias documentales y garantiza la "
        "concordancia física y contable de los inventarios sanitarios.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Champi Velásquez (2023), en su investigación aplicada titulada “Implementación de un "
        "sistema de monitoreo inalámbrico mediante Internet de las cosas para monitorear la "
        "conservación en la cadena de frío de vacunas del servicio de inmunizaciones en el "
        "distrito de Puente Piedra”, sustentada en la Universidad de Ciencias y Humanidades, "
        "tuvo como objetivo implementar una solución tecnológica para supervisar la "
        "conservación térmica y el control de los lotes de vacunas almacenados en el área de "
        "inmunizaciones de un establecimiento público de salud (p. iii). El estudio se "
        "desarrolló bajo un enfoque cuantitativo y diseño preexperimental, diagnosticando que "
        "el registro manual de los controles de cadena de frío en hojas físicas ocasionaba "
        "demoras operativas, omisiones de lectura y riesgos de pérdida de potencia inmunológica "
        "en los biológicos regulados por el Ministerio de Salud (p. 14). Los resultados "
        "demostraron que la automatización del registro y las alertas en tiempo real redujeron "
        "en un 90% las incidencias no detectadas en el almacenamiento frigorífico y aseguraron "
        "la integridad de los datos de conservación por cada lote biológico (p. iii). El autor "
        "concluyó que la incorporación de herramientas informáticas en los servicios públicos "
        "de inmunizaciones resulta determinante para superar la vulnerabilidad de los registros "
        "manuales y garantizar la trazabilidad y calidad de las vacunas.",
        sangria=True
    )
