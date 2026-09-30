#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB — ENSAMBLADOR DE INTRODUCCIÓN Y CAPÍTULO I (.DOCX)
Universidad Nacional José María Arguedas (UNAJMA)
================================================================================
"""

from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx_utilidades import (
    agregar_titulo_1, agregar_titulo_2, agregar_titulo_3,
    agregar_parrafo, agregar_item_lista
)

def construir_introduccion(doc):
    agregar_titulo_1(doc, "INTRODUCCIÓN", page_break=False)

    agregar_parrafo(
        doc,
        "La gestión de la cadena de suministro de productos biológicos e inmunizaciones constituye un eje "
        "neurálgico e insustituible para garantizar la salud pública y la prevención de enfermedades "
        "inmunoprevenibles a nivel global y nacional (Organización Panamericana de la Salud & PATH, 2020). "
        "Las vacunas son insumos termolábiles de estricto cuidado que demandan una trazabilidad ininterrumpida "
        "tanto en la cadena de frío física (manteniendo temperaturas entre +2 °C y +8 °C) como en la consistencia "
        "documental de sus movimientos logísticos diarios: recepción de lotes, transferencias interinstitucionales, "
        "distribución a establecimientos periféricos y emisión de vales de salida (Brooks et al., 2024; MINSA, 2022).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "En el ámbito de la Dirección de Salud Apurímac II (DISA Apurímac II), cuya jurisdicción sanitaria "
        "abarca las provincias de Andahuaylas y Chincheros en el departamento de Apurímac, la administración "
        "de biológicos enfrenta severas dificultades operativas derivadas de la dispersión geográfica de sus "
        "once (11) centros de acopio zonales y de la dependencia histórica de registros manuales en papel, libros "
        "de kardex físicos y plantillas aisladas de cálculo. Esta forma tradicional de trabajo ha generado "
        "excesivos tiempos de registro, constantes discrepancias entre los saldos documentales y las existencias "
        "físicas en los refrigeradores, y una elevada sobrecarga administrativa en el personal de salud.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Frente a este nudo crítico, la presente investigación tuvo como propósito determinar en qué medida "
        "la aplicación del sistema web SIVAC (*Sistema de Información y Control de Vacunas*), desarrollado bajo la "
        "metodología ágil Extreme Programming (XP) y fundamentado en el estándar internacional de calidad de "
        "software ISO/IEC 25010:2023, influye en la gestión de movimientos de vacunas en el personal de inmunizaciones "
        "de la DISA Apurímac II. El estudio adoptó un diseño preexperimental con pretest y postest en un solo grupo censal "
        "integrado por la totalidad de los catorce (14) trabajadores del área (N = n = 14).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "El informe final de tesis se encuentra estructurado en seis capítulos formalmente articulados: "
        "el **Capítulo I** plantea la realidad problemática, la formulación del problema general y específicos, "
        "los objetivos, la justificación multidisciplinaria y las delimitaciones del estudio; "
        "el **Capítulo II** detalla la revisión crítica de antecedentes internacionales y nacionales verificados; "
        "el **Capítulo III** expone el marco teórico disciplinario, la definición de términos básicos y la documentación "
        "exhaustiva del desarrollo del software SIVAC mediante Extreme Programming (arquitectura, historias de usuario, "
        "diagramas de clases y base de datos); "
        "el **Capítulo IV** fundamenta el diseño metodológico, la operacionalización de variables, las técnicas e instrumentos "
        "validados mediante juicio de expertos (V de Aiken = 0.987) y el plan de análisis estadístico; "
        "el **Capítulo V** presenta los resultados descriptivos, las pruebas de normalidad de Shapiro-Wilk y la contrastación "
        "inferencial mediante la prueba de rangos con signo de Wilcoxon; y el **Capítulo VI** desarrolla la discusión crítica "
        "de los hallazgos frente a la literatura científica, seguida de las conclusiones, recomendaciones, referencias APA 7 y anexos.",
        sangria=True
    )

def construir_capitulo1(doc):
    agregar_titulo_1(doc, "CAPÍTULO I: PROBLEMA DE INVESTIGACIÓN")

    # 1.1. Descripción de la Realidad Problemática
    agregar_titulo_2(doc, "1.1. Descripción de la Realidad Problemática")

    agregar_titulo_3(doc, "1.1.1. Contexto Internacional")
    agregar_parrafo(
        doc,
        "La gestión de la cadena de suministro de insumos médicos esenciales, y de manera sumamente crítica la de los "
        "productos biológicos e inmunizaciones, constituye uno de los desafíos operativos y sanitarios más apremiantes "
        "para los sistemas de salud pública a nivel global (Organización Panamericana de la Salud & PATH, 2020). Las vacunas "
        "son productos termolábiles de alto costo y estricta caducidad que demandan un control ininterrumpido no solo en la "
        "cadena de frío física (manteniendo temperaturas normadas entre +2 °C y +8 °C), sino también en la cadena de "
        "información que respalda cada movimiento logístico: ingresos desde los almacenes centrales, transferencias entre "
        "redes territoriales, despachos hacia puntos de vacunación, saldos en tiempo real y registro de descartes o pérdidas "
        "(Brooks et al., 2024).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "A nivel mundial, la dependencia histórica de registros manuales en soporte de papel, cuadernos de control de inventario "
        "y hojas de cálculo desconectadas ha provocado brechas estructurales de oportunidad, precisión e integridad en la "
        "información de inventarios de biológicos. En investigaciones realizadas en países en desarrollo, Chekol et al. (2023) "
        "constataron que la tasa de concordancia global de datos en sistemas manuales rutinarios apenas alcanza el 74%, debiéndose "
        "las principales inconsistencias a la complejidad del llenado de libros de registro y a la duplicidad de formatos "
        "administrativos. Asimismo, Ergetie et al. (2023) identificaron en establecimientos de atención primaria que el 68% del "
        "personal de salud presentaba serias deficiencias en la gestión y actualización oportuna del sistema logístico farmacéutico "
        "debido a la sobrecarga administrativa que impone la transcripción física, impidiendo que el 50% de los centros mantuviera "
        "un monitoreo estricto de sus existencias.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Frente a este escenario, la transformación digital y la adopción de arquitecturas web especializadas en logística sanitaria "
        "han demostrado ser la vía más eficaz para resolver estas asimetrías de información. Shen et al. (2024), en un estudio evaluativo "
        "longitudinal sobre la digitalización de la cadena de suministro hospitalaria, evidenciaron que la implementación de una "
        "plataforma de inventario digital redujo la tasa promedio anual de errores de registro de 0.425‰ a 0.025‰ (una disminución del 94.1% "
        "en discrepancias), al tiempo que incrementó la eficiencia global de la cadena en un 42.4% y disminuyó la inmovilización de stocks. "
        "De igual manera, en el ámbito de las inmunizaciones, Dang et al. (2024) documentaron que la transición de sistemas basados en papel "
        "hacia registros digitales integrados logró reducir el intervalo de latencia entre el acto de movimiento biológico y la disponibilidad "
        "del dato de 43.7 días a solo 0.7 días, permitiendo una trazabilidad casi instantánea y reduciendo la carga laboral del personal en un 38%. "
        "En consonancia, intervenciones de fortalecimiento de sistemas electrónicos de información logística (e-LMIS) reportadas por "
        "Wasswa et al. (2023) y Kigenza et al. (2023) corroboraron que el despliegue de soluciones informáticas incrementó la exactitud "
        "de los datos de inventario del 25% al 85% y mitigó los quiebres de stock a menos del 1%.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "En el contexto latinoamericano, Balón Morejón (2023) desarrolló una aplicación web con tecnologías de código abierto para la gestión "
        "de inventario y campañas de vacunación en el centro de salud Dr. José Garcés Rodríguez en Ecuador, comprobando empíricamente que el "
        "tiempo necesario para la consolidación y emisión de reportes estadísticos y kardex se redujo de 3 a 4 días hábiles a únicamente 6 segundos, "
        "eliminando por completo la duplicidad de datos y mejorando sustancialmente la satisfacción de los profesionales de salud.",
        sangria=True
    )

    agregar_titulo_3(doc, "1.1.2. Contexto Nacional")
    agregar_parrafo(
        doc,
        "En el Perú, el Ministerio de Salud (MINSA), a través de la Dirección General de Intervenciones Estratégicas en Salud Pública y la "
        "Norma Técnica de Salud N° 196-MINSA/DGIESP-2022 (*Norma Técnica de Salud que establece el Esquema Nacional de Vacunación*), "
        "establece lineamientos sumamente rigurosos para la recepción, almacenamiento, conservación, distribución, control de stock y descarte "
        "de vacunas a lo largo de todo el territorio patrio (MINSA, 2022). La normativa estipula que cada almacén y centro de acopio "
        "institucional debe mantener actualizado diariamente el registro de movimientos mediante el sistema de inventario (Kardex) físico o digital, "
        "asegurando la correspondencia absoluta entre las dosis programadas, las dosis efectivamente recepcionadas y los vales de salida o "
        "entrega hacia las microredes y establecimientos ejecutores.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "A pesar de contar con este marco normativo, la realidad operativa del sistema de salud peruano evidencia una profunda brecha de "
        "informatización y modernización tecnológica en el nivel intermedio de la cadena de suministro. Si bien existen plataformas de alcance "
        "nacional como el HIS-MINSA y los módulos de registro nominal de vacunación ciudadana, el eslabón logístico y administrativo interno "
        "que controla los movimientos físicos de entrada, salida, transferencias interinstitucionales, saldos por lotes y fechas de caducidad en "
        "las Direcciones de Redes Integradas de Salud (DIRIS) y Direcciones de Salud (DISA) descentralizadas sigue operando, en gran medida, "
        "bajo esquemas manuales o semimanuales altamente vulnerables.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Mego Navarro (2021), al estudiar la gestión de vacunas en entidades públicas de salud peruanas, reveló que el 45% del personal "
        "administrativo y asistencial aún recababa información estadística y de stocks mediante desplazamientos físicos a los centros de acopio, "
        "un 30% lo hacía a través de cadenas de correos electrónicos no estandarizados y solo un 12.5% contaba con soporte de sistemas informáticos, "
        "provocando que más del 25% de los reportes presentara inconsistencias u omisiones por falta de variables estandarizadas. En una línea similar, "
        "Garcia Villacorta y Calderón Huaman (2023) demostraron que la ausencia de plataformas web de inventario en establecimientos peruanos genera "
        "un desfase crítico en el control de existencias, evidenciando que tras implementar una aplicación web el nivel de exactitud documental de "
        "inventarios se incrementó de 75.42% a 97.18%, elevando las entregas a tiempo al 97.77%.",
        sangria=True
    )

    agregar_titulo_3(doc, "1.1.3. Contexto Regional y Local (Dirección de Salud Apurímac II, Andahuaylas)")
    agregar_parrafo(
        doc,
        "Esta problemática nacional adquiere una dimensión crítica en el ámbito de la Dirección de Salud Apurímac II (DISA Apurímac II), "
        "institución rectora de la salud pública en las provincias de Andahuaylas y Chincheros, en el departamento de Apurímac. La administración "
        "y distribución de los biológicos está centralizada en la Oficina de la Estrategia Sanitaria Nacional de Inmunizaciones, la cual coordina "
        "directamente con once (11) centros de acopio y cabeceras de microred distribuidos en una geografía agreste y dispersa.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "El equipo humano responsable de este proceso operativo está constituido por una población censal de **catorce (14) trabajadores**: "
        "tres (03) profesionales directivos y especialistas de la estrategia sanitaria en la sede administrativa de Andahuaylas y once (11) "
        "profesionales de enfermería y técnicos responsables directos de la cadena de frío y el almacén en los centros de acopio zonales.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "A través del diagnóstico institucional y la observación de los procesos en la sede de la DISA Apurímac II, se detectaron tres "
        "nudos críticos determinantes que afectaban la gestión de movimientos de vacunas:",
        sangria=True
    )

    nudos = [
        "**Deficiencia en la oportunidad de procesamiento (Tiempos operativos excesivos):** El registro de movimientos (ingresos desde Lima, salidas por distribución, transferencias de emergencia y descartes) se efectuaba manualmente en cuadernos y hojas de cálculo locales aisladas. El ingreso de un lote demandaba entre 12 y 20 minutos por transacción, mientras que la emisión y verificación de vales de entrega oficiales requería entre 15 y 25 minutos por documento, acumulando demoras críticas en las jornadas de distribución masiva.",
        "**Inconsistencia documental y discrepancias de inventario:** La fragmentación de la información entre la sede central y los 11 centros de acopio generaba constantes errores de digitación de lotes alfanuméricos y fechas de caducidad. Se suscitaban discordancias frecuentes entre el saldo teórico de los libros de kardex y el stock físico real en refrigeradores, así como desfases entre las dosis programadas y las efectivamente entregadas.",
        "**Baja satisfacción del usuario y sobrecarga laboral:** Los 14 trabajadores manifestaban agotamiento operativo ante la duplicidad de tareas administrativas, la complejidad de conciliar informes mensuales y la constante tensión por evitar errores sancionables en auditorías, derivando en insatisfacción laboral y rechazo hacia los métodos manuales."
    ]
    for nudo in nudos:
        agregar_item_lista(doc, nudo, simbolo="•")

    agregar_parrafo(
        doc,
        "Frente a esta realidad concreta, se diseñó e implementó el **Sistema Web SIVAC** (*Sistema de Información y Control de Vacunas*), "
        "desarrollado bajo la metodología ágil **Extreme Programming (XP)** y fundamentado en el estándar de calidad de software "
        "**ISO/IEC 25010:2023**. SIVAC se concibió como una solución tecnológica integral orientada a automatizar los registros de entradas, "
        "salidas y transferencias, centralizar la base de datos en tiempo real, generar vales oficiales automáticos y suministrar reportes "
        "inmediatos de balance de kardex.",
        sangria=True
    )

    # 1.2. Formulación del Problema
    agregar_titulo_2(doc, "1.2. Formulación del Problema")
    agregar_titulo_3(doc, "1.2.1. Problema General")
    agregar_parrafo(
        doc,
        "¿En qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de movimientos de vacunas en el personal de "
        "inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025?",
        sangria=True
    )
    agregar_titulo_3(doc, "1.2.2. Problemas Específicos")
    problemas_esp = [
        "**Problema Específico 1 (PE1):** ¿En qué medida la aplicación del sistema \"SIVAC\" mejora la **oportunidad de procesamiento** en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025?",
        "**Problema Específico 2 (PE2):** ¿En qué medida la aplicación del sistema \"SIVAC\" mejora la **consistencia documental** en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025?",
        "**Problema Específico 3 (PE3):** ¿En qué medida la aplicación del sistema \"SIVAC\" mejora la **satisfacción del usuario** en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025?"
    ]
    for pe in problemas_esp:
        agregar_item_lista(doc, pe, simbolo="•")

    # 1.3. Objetivos de la Investigación
    agregar_titulo_2(doc, "1.3. Objetivos de la Investigación")
    agregar_titulo_3(doc, "1.3.1. Objetivo General")
    agregar_parrafo(
        doc,
        "Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de movimientos de vacunas en el personal de "
        "inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025.",
        sangria=True
    )
    agregar_titulo_3(doc, "1.3.2. Objetivos Específicos")
    objetivos_esp = [
        "**Objetivo Específico 1 (OE1):** Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la **oportunidad de procesamiento** en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025.",
        "**Objetivo Específico 2 (OE2):** Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la **consistencia documental** en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025.",
        "**Objetivo Específico 3 (OE3):** Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la **satisfacción del usuario** en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025."
    ]
    for oe in objetivos_esp:
        agregar_item_lista(doc, oe, simbolo="•")

    # 1.4. Justificación de la Investigación
    agregar_titulo_2(doc, "1.4. Justificación de la Investigación")
    agregar_titulo_3(doc, "1.4.1. Justificación Teórica")
    agregar_parrafo(
        doc,
        "La investigación se sustenta teóricamente en la confluencia de la ingeniería de software aplicada a la salud pública y los "
        "modelos de gestión logística sanitaria. Desde la perspectiva de las ciencias de la computación, el estudio aporta evidencia "
        "sobre la efectividad de la metodología ágil **Extreme Programming (XP)** (Beck, 1999; Pressman, 2010; Sommerville, 2016) para "
        "desarrollar sistemas web robustos en entornos organizacionales con requerimientos cambiantes y alta sensibilidad operativa. "
        "Asimismo, se fundamenta en la norma internacional **ISO/IEC 25010:2023**, validando cómo las características de **Adecuación Funcional** "
        "(completitud y exactitud de resultados) y **Usabilidad** (facilidad de aprendizaje y claridad de interfaz) determinan el éxito de un "
        "producto de software en el sector salud.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Desde la vertiente del comportamiento del usuario frente a la tecnología, la investigación se apoya en el **Modelo de Aceptación "
        "Tecnológica (TAM)** formulado por Fred Davis (1989), el cual postula que la *Utilidad Percibida* y la *Facilidad de Uso Percibida* "
        "son los constructos predictores fundamentales de la aceptación y adopción real de un sistema informático (Ndlovu et al., 2021). "
        "El estudio enriquece la literatura académica al contrastar de forma empírica estos modelos teóricos en un contexto geográfico andino "
        "y en un proceso tan vital como la cadena de suministro de biológicos.",
        sangria=True
    )

    agregar_titulo_3(doc, "1.4.2. Justificación Práctica y Social")
    agregar_parrafo(
        doc,
        "En el plano práctico, la investigación ofrece una solución tecnológica directa, tangible e instalada a un problema histórico "
        "y cotidiano que aqueja a la DISA Apurímac II. Al sustituir los cuadernos manuales y los archivos aislados por una plataforma web "
        "centralizada, se dota al personal de una herramienta que: automatiza el cálculo instantáneo de saldos y kardex de vacunas, "
        "genera los vales de entrega oficiales con códigos de validación en segundos, permite la consulta en tiempo real del stock disponible "
        "por lote y fecha de expiración, y reduce la jornada de trabajo dedicada a labores mecánicas de transcripción y conciliación mensual.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "El impacto social trasciende los límites de la oficina administrativa: una gestión de movimientos de vacunas caracterizada por la "
        "oportunidad de procesamiento, una estricta consistencia documental (registros sin discrepancias y concordancia programada versus entregada) "
        "y una alta satisfacción del usuario asegura que los centros de salud de las comunidades más alejadas de Andahuaylas y Chincheros reciban "
        "las dosis biológicas completas, exactas y a tiempo. De este modo, se previenen quiebres de stock que obliguen a rechazar la vacunación "
        "de niños, gestantes y adultos mayores, salvaguardando la salud pública y optimizando la inversión del Estado en recursos biológicos.",
        sangria=True
    )

    agregar_titulo_3(doc, "1.4.3. Justificación Metodológica")
    agregar_parrafo(
        doc,
        "Desde el punto de vista metodológico, el estudio adopta un enfoque cuantitativo riguroso con un diseño **preexperimental de pretest "
        "y postest en un solo grupo (O1 → X → O2)**, el cual resulta idóneo para medir el efecto de una intervención tecnológica en poblaciones "
        "laborales intactas y censales (N = n = 14) (Hernández Sampieri et al., 2014).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "La investigación sienta un precedente metodológico para la Universidad Nacional José María Arguedas al implementar un protocolo "
        "exhaustivo de **validación de instrumentos por juicio de expertos** (evaluando 5 dimensiones psicométricas: suficiencia, relevancia, "
        "coherencia, claridad y redacción en una escala de 1 a 4), aplicando el **Índice de Validez de Contenido (IVC)** de Lawshe modificado "
        "por Tristán (2008) y el **Coeficiente V de Aiken**, así como el cálculo de consistencia interna mediante el **Alfa de Cronbach** (α). "
        "Asimismo, el plan de contrastación estadística contempla la verificación de normalidad mediante la prueba de **Shapiro-Wilk** (n ≤ 50) "
        "y la aplicación estricta de pruebas inferenciales no paramétricas (**Wilcoxon**) o paramétricas (**t de Student**), garantizando que "
        "las conclusiones alcancen el más alto estándar de validez científica.",
        sangria=True
    )

    # 1.5. Delimitaciones y Limitaciones
    agregar_titulo_2(doc, "1.5. Delimitaciones y Limitaciones de la Investigación")
    agregar_titulo_3(doc, "1.5.1. Delimitación Espacial")
    agregar_parrafo(
        doc,
        "La investigación se desarrolló físicamente en el ámbito de competencia de la **Dirección de Salud Apurímac II**, abarcando de forma "
        "integral la Oficina de la Estrategia Sanitaria de Inmunizaciones (sede central en Jr. Hugo Pesce S/N, Andahuaylas) y la red de "
        "**once (11) centros de acopio y cabeceras de microred** distribuidos en la provincia de Andahuaylas y zonas de influencia en la "
        "provincia de Chincheros, departamento de Apurímac, Perú.",
        sangria=True
    )

    agregar_titulo_3(doc, "1.5.2. Delimitación Temporal")
    agregar_parrafo(
        doc,
        "El horizonte temporal del estudio abarcó el periodo correspondiente al año **2025**, estructurado en tres fases cronológicas: "
        "Fase Pretest (diagnóstico de línea base y registro manual tradicional), Fase de Intervención (desarrollo ágil con XP, despliegue de "
        "SIVAC y capacitación del personal) y Fase Postest (medición final de los indicadores de impacto tras el uso continuo del sistema).",
        sangria=True
    )

    agregar_titulo_3(doc, "1.5.3. Delimitación Social y Muestral")
    agregar_parrafo(
        doc,
        "La unidad de análisis estuvo circunscrita exclusivamente a los **catorce (14) servidores públicos** que conforman la totalidad "
        "del personal del área de inmunizaciones de la DISA Apurímac II: 3 profesionales directivos de la estrategia sanitaria en sede central "
        "y 11 profesionales de enfermería y técnicos responsables de la cadena de frío en los almacenes zonales. Al ser una población finita "
        "y reducida (N ≤ 50), se evaluó a la totalidad de los miembros sin recurrir a muestreo probabilístico, configurando un **estudio censal "
        "(N = n = 14)**.",
        sangria=True
    )

    agregar_titulo_3(doc, "1.5.4. Delimitación Temática y Funcional")
    agregar_parrafo(
        doc,
        "El alcance funcional del sistema web SIVAC y de la investigación se restringió estrictamente al proceso de **gestión de movimientos "
        "de vacunas**: registro de ingresos por remesas, egresos por distribución mensual, transferencias de emergencia, consulta de saldos en "
        "kardex, trazabilidad de lotes/vencimientos y generación de vales de entrega oficiales. La investigación no incluyó módulos de registro "
        "clínico individual de pacientes vacunados (cubierto por el HIS-MINSA), ni procesos presupuestales (SIAF), concentrándose exclusivamente "
        "en la logística y control de los productos biológicos en sus tres dimensiones oficiales: **oportunidad de procesamiento**, "
        "**consistencia documental** y **satisfacción del usuario** (DEC-007).",
        sangria=True
    )

    agregar_titulo_3(doc, "1.5.5. Limitaciones de la Investigación")
    agregar_parrafo(
        doc,
        "Durante la ejecución de la investigación se presentaron las siguientes limitaciones contextuales que fueron adecuadamente "
        "mitigadas por el diseño metodológico y arquitectónico:",
        sangria=True
    )
    limitaciones = [
        "**Brecha de conectividad en zonas rurales:** Algunos centros de acopio periféricos experimentaron intermitencias temporales en el servicio de internet. Esta condición se mitigó implementando en SIVAC mecanismos de almacenamiento en caché local del navegador y sincronización asíncrona de datos transaccionales.",
        "**Resistencia inicial al cambio tecnológico:** La prolongada costumbre de operar con formatos físicos en papel generó cierta reticencia inicial en operadores técnicos de mayor antigüedad. Esta situación se superó mediante talleres prácticos de inducción personalizada, acompañamiento presencial continuo y el diseño de interfaces sumamente limpias e intuitivas según los principios de usabilidad de la norma ISO/IEC 25010.",
        "**Tamaño censal acotado (n = 14):** Dado que la dotación de personal especializado de la cadena de frío provincial está restringida institucionalmente a 14 trabajadores, el tamaño muestral impidió la aplicación de técnicas multivariadas masivas, resolviéndose con rigor científico mediante el empleo de pruebas de normalidad de Shapiro-Wilk para muestras pequeñas y contrastes inferenciales no paramétricos de Wilcoxon."
    ]
    for lim in limitaciones:
        agregar_item_lista(doc, lim, simbolo="•")
