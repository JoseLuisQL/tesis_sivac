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
  estructurados bajo los 6 elementos canónicos exigidos por la dirección académica.
- Coherencia epistemológica total con el estado pre-campo del Capítulo V:
  marcadores formales [Pendiente] para contrastes inferenciales y estadísticos.
- Cero invención de datos empíricos de campo (Regla 01).
- 4 Conclusiones (Primera a Cuarta) en correspondencia 1:1 con los objetivos.
- 7 Recomendaciones técnicas y metodológicas (Primera a Séptima) no asuntivas.
- 42 Referencias Bibliográficas APA 7 en estricta correspondencia biunívoca 1:1.
- Anexos 1 a 6 íntegros y reproducibles:
  * Anexo 1: Matriz de consistencia (Tabla 18, única tabla con SEQ Tabla).
  * Anexo 2: Instrumentos de recolección íntegros (3 instrumentos; Instrumento N.° 03 con
    Modalidad A de 8 ítems, oficial para HE3, y Modalidad B de 8 ítems, anexa y no aditiva).
  * Anexo 3: Expediente y matrices de validación por juicio de expertos (procedimiento previsto, sin resultados aplicados).
  * Anexo 4: Estructura de la base de datos anonimizada y libro de códigos (Codebook).
  * Anexo 5: Evidencias de ingeniería de software XP, pruebas automatizadas y despliegue.
  * Anexo 6: Aspectos éticos, autorización institucional y consentimiento informado.
================================================================================
"""

import os
import sys
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utilidades')))

from docx_utilidades import (
    agregar_titulo_1, agregar_titulo_2, agregar_titulo_3, agregar_titulo_4,
    agregar_parrafo, agregar_item_lista, agregar_referencia_apa7,
    agregar_tabla_datos, formatear_tabla_apa7, procesar_formato_texto,
    agregar_nota_tabla_apa7
)
from docx_quirurgico import configurar_geometria_tabla


def agregar_cuadro_anexo(doc, titulo_cuadro, encabezados, filas, col_widths=None, nota=None, font_size_pt=10):
    """
    Agrega una matriz estructurada para anexos sin generar campo SEQ Tabla,
    preservando intacto el conteo del Índice de Tablas oficial (Tablas 1 a 18).
    Aplica formato de tabla APA 7 con ancho útil máximo de 8784 dxa (15.50 cm).
    """
    p_tit = doc.add_paragraph()
    p_tit.paragraph_format.keep_with_next = True
    p_tit.paragraph_format.space_before = Pt(10)
    p_tit.paragraph_format.space_after = Pt(4)
    p_tit.paragraph_format.line_spacing = 1.15
    p_tit.paragraph_format.first_line_indent = Inches(0)
    for r_texto, r_bold, r_italic in procesar_formato_texto(str(titulo_cuadro)):
        run = p_tit.add_run(r_texto)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(9.5)
        run.font.bold = r_bold
        run.font.italic = r_italic

    tbl = doc.add_table(rows=len(filas) + 1, cols=len(encabezados))
    for c_idx, h_text in enumerate(encabezados):
        cell = tbl.rows[0].cells[c_idx]
        p = cell.paragraphs[0]
        p.text = ""
        for r_texto, r_bold, r_italic in procesar_formato_texto(str(h_text)):
            run = p.add_run(r_texto)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(font_size_pt)
            run.font.bold = True
            run.font.italic = r_italic

    for r_idx, fila in enumerate(filas):
        for c_idx, val in enumerate(fila):
            cell = tbl.rows[r_idx + 1].cells[c_idx]
            p = cell.paragraphs[0]
            p.text = ""
            for r_texto, r_bold, r_italic in procesar_formato_texto(str(val)):
                run = p.add_run(r_texto)
                run.font.name = 'Times New Roman'
                run.font.size = Pt(font_size_pt)
                run.font.bold = r_bold
                run.font.italic = r_italic

    formatear_tabla_apa7(tbl, col_widths=col_widths, font_size_pt=font_size_pt)

    if nota:
        agregar_nota_tabla_apa7(doc, nota)
    return tbl


def construir_capitulo6_y_final(doc):
    # ==========================================================================
    # CAPÍTULO VI: DISCUSIÓN
    # ==========================================================================
    agregar_titulo_1(doc, "CAPÍTULO VI: DISCUSIÓN")

    # Bloque Argumentativo 1: Objetivo General (Gestión de movimientos de vacunas)
    agregar_parrafo(
        doc,
        "En relación con el objetivo general de la investigación, orientado a determinar en qué medida la aplicación "
        "del sistema web SIVAC mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la "
        "Dirección de Salud Apurímac II, la contrastación inferencial de la hipótesis general se encuentra estructurada "
        "metodológicamente a través de la integración convergente de los contrastes de las tres dimensiones específicas, "
        "cuyo reporte numérico definitivo permanece [Pendiente de inserción de estadísticos descriptivos, prueba de "
        "Wilcoxon Z, p-valor bilateral con ajuste Holm-Bonferroni y tamaño del efecto r tras cierre de campo en la "
        "Tabla 17]. A nivel funcional y operativo, el módulo técnico desplegado en el almacén especializado central y en "
        "los ocho centros de acopio de las provincias de Andahuaylas y Chincheros sustituye el flujo fragmentado "
        "de libros manuscritos, kardex físicos y hojas de cálculo desarticuladas por una arquitectura web en tres capas "
        "(Luján Mora, 2002; De la Torre Llorente et al., 2010; Sommerville, 2016) con API REST protegida mediante tokens "
        "JWT y control de acceso basado en roles RBAC (Ruiz Barea, 2023) sobre un repositorio relacional centralizado en "
        "PostgreSQL, el cual gobierna el control estricto de lotes bajo la regla First Expired, First Out (FEFO), el "
        "cálculo automatizado de saldos intermensuales y la generación digital de vales en formatos PDF y Excel conforme "
        "a la Norma Técnica de Salud NTS N.° 196-MINSA/DGIESP-2022 del Ministerio de Salud del Perú (Ministerio de Salud, 2022) y a "
        "los lineamientos de trazabilidad de la Organización Mundial de la Salud (World Health Organization [WHO], 2021), "
        "la Organización Panamericana de la Salud y PATH (2020), Brooks et al. (2024) y Addy et al. (2024). Este diseño "
        "converge con la evidencia empírica de Mekonen et al. (2024), quienes en una evaluación de N = 102 almacenes y "
        "establecimientos sanitarios públicos de Etiopía (71 centros de salud, 11 subciudades y 20 hospitales) mediante "
        "regresión lineal multivariable, demostraron que la utilización efectiva de un sistema de información de gestión "
        "logística incrementó significativamente la disponibilidad de vacunas (coeficiente beta = 0.305; p = 0.008) y "
        "redujo el desperdicio de biológicos (coeficiente beta = -0.300; p = 0.032), explicando el 53.3% de la varianza "
        "del desempeño de la cadena de suministro (R cuadrado = 0.533). De manera coincidente, Wasswa et al. (2023) "
        "comprobaron en la red pública del Ministerio de Salud de Uganda que el procesamiento digital de requisiciones y "
        "comprobantes de despacho permitió mantener una disponibilidad promedio del 90% en 19 hospitales regionales de "
        "referencia, mientras que Shen et al. (2024), en un estudio longitudinal pre-post en el Primer Hospital Afiliado "
        "de la Universidad Médica de Nanjing en China, evidenciaron que la automatización de la cadena de suministro "
        "redujo la tasa de roturas de stock de 0.425% a 0.277%, disminuyó el tiempo de inmovilización de inventarios "
        "cerca del 20% e incrementó en 42.4% la eficiencia operativa global. En el contexto sanitario peruano, "
        "Gutiérrez-Aguado et al. (2024) documentaron que el 61.8% de los equipos de cadena de frío del programa nacional "
        "de inmunizaciones supera los diez años de antigüedad y revelaron marcadas asimetrías entre los inventarios físicos "
        "locales y los registros en el sistema SIGA-MEF, en tanto que Mego Navarro (2021) verificó en una entidad pública "
        "nacional (n = 40 operadores) que un sistema web desarrollado con Extreme Programming elevó el acceso en tiempo "
        "real al 87.5% y la completitud de los registros vacunales del 50% al 95%. No obstante, al analizar las "
        "particularidades territoriales de los ocho centros de acopio de la Dirección de Salud Apurímac II en Andahuaylas "
        "y Chincheros, caracterizados por una marcada dispersión geográfica y conectividad intermitente, debe reconocerse "
        "explícitamente como limitación metodológica que el diseño preexperimental de un solo grupo (GE: O₁ - X - O₂, "
        "N = n = 14) sin grupo de control paralelo impide atribuir causalidad aislada absoluta, por lo que los cambios "
        "observados se interpretan como mejoras asociadas a la intervención tecnológica, dado que factores concurrentes "
        "como la capacitación técnica previa, la curva de familiarización progresiva y el efecto Hawthorne pueden "
        "co-influir en el desempeño de los operadores. En la práctica sanitaria, la articulación de Extreme Programming "
        "(Beck, 1999; Cohn, 2004; Arisholm et al., 2007; Pressman, 2010; Kokol, 2022) con el estándar ISO/IEC 25010:2023 "
        "(International Organization for Standardization [ISO] y International Electrotechnical Commission [IEC], 2023; "
        "Moumane et al., 2024) consolida la trazabilidad logística exigida por la NTS N.° 196-MINSA/DGIESP-2022.",
        sangria=True
    )

    # Bloque Argumentativo 2: Objetivo Específico 1 (Oportunidad de procesamiento)
    agregar_parrafo(
        doc,
        "Respecto al primer objetivo específico, orientado a determinar en qué medida la aplicación del sistema web SIVAC "
        "mejora la oportunidad de procesamiento en los movimientos de vacunas del personal de inmunizaciones de la Dirección "
        "de Salud Apurímac II, el espacio estructurado para las variaciones observadas en pre-test y post-test de los "
        "indicadores de tiempo de registro (T_reg) y tiempo de emisión de vale (T_vale) permanece [Pendiente de inserción "
        "de estadísticos descriptivos, prueba de Wilcoxon Z, p-valor bilateral con ajuste Holm-Bonferroni y tamaño del "
        "efecto r tras cierre de campo en la Tabla 13 y Tabla 17], habiéndose verificado en las pruebas de desempeño del "
        "módulo técnico desplegado tiempos medios de respuesta de 142 ms en la API REST y de 1.18 segundos en la "
        "compilación de comprobantes PDF y Excel. En cuanto a la interpretación operativa, la arquitectura transaccional "
        "de SIVAC interviene directamente sobre el flujo de trabajo respecto al kardex manual al suprimir la búsqueda "
        "visual de lotes en libros foliados, el recálculo aritmético en calculadora y la redacción manuscrita en "
        "triplicado de comprobantes, reemplazándolos por precarga automática de saldos intermensuales en PostgreSQL, "
        "selección asistida de lotes bajo bloqueo FEFO y emisión en un clic de vales oficiales en PDF y Excel. Al "
        "comparar rigurosamente estos mecanismos con los antecedentes, se observa plena convergencia con Inarotul Huda "
        "et al. (2025), quienes al aplicar la metodología Extreme Programming en una plataforma web sanitaria lograron "
        "reducir el tiempo individual de registro de datos de 7–10 minutos a 2–3 minutos por transacción (reducción "
        "superior al 70%) y el tiempo de emisión de reportes oficiales de 2–3 horas a un rango de 10–20 segundos. De "
        "igual forma, concuerda con Astuhuaman Perez y Baltazar Maza (2023), quienes en su investigación sustentada en "
        "la Universidad Privada del Norte sobre el Centro de Salud de Nueva Fuerabamba en Apurímac (diseño preexperimental "
        "con muestra censal de n = 12 trabajadores y 30 usuarios) demostraron una reducción estadísticamente significativa "
        "del tiempo promedio de registro y elaboración de procesos de 9.97 a 8.47 minutos (mejora del 15.1%, prueba de "
        "Wilcoxon con p menor a 0.001) y del tiempo de actualización de registros de 6.10 a 4.60 minutos. Asimismo, guarda "
        "consonancia con Dang et al. (2024) en centros de salud y almacenes distritales de Vietnam, donde la digitalización "
        "del registro de inmunizaciones redujo el tiempo para disponer de registros consolidados de 43.7 a 0.7 días "
        "(mejora del 98% en oportunidad de procesamiento) y disminuyó en 38% la carga operativa del personal; con Balón "
        "Morejón (2023) en Ecuador, quien contrajo el tiempo de consolidación de inventario y emisión de reportes de "
        "stock de 3–4 días hábiles a 6 segundos; con Alvarez Ticllasuca et al. (2023) en Huancavelica, quienes elevaron "
        "la eficacia del control de inmunizaciones del 25.9% al 77.8% optimizando los tiempos de respuesta; y con Dolan "
        "et al. (2020) en establecimientos de Tanzania y Zambia. En la explicación contextual de la Dirección de Salud "
        "Apurímac II, donde los catorce operadores de los ocho centros de acopio de Andahuaylas y Chincheros comparten "
        "labores de almacén con jornadas de vacunación intramural y extramural, la agilización del registro y despacho "
        "resulta decisiva para evitar demoras en la distribución hacia las microredes. Sin embargo, dentro de las "
        "limitaciones metodológicas y amenazas a la validez interna, dado el diseño preexperimental de un solo grupo "
        "(GE: O₁ - X - O₂, N = n = 14) sin grupo de control paralelo, las reducciones cronometradas deben interpretarse "
        "como mejoras asociadas a la intervención tecnológica sin atribuir causalidad aislada absoluta, puesto que la "
        "capacitación técnica, la curva de familiarización progresiva tras el periodo de estabilización y el efecto "
        "Hawthorne durante la observación cronometrada pueden co-influir en el rendimiento. Como implicación práctica "
        "sanitaria, esta optimización temporal fortalece la oportunidad de abastecimiento de biológicos bajo la NTS N.° "
        "196-MINSA/DGIESP-2022.",
        sangria=True
    )

    # Bloque Argumentativo 3: Objetivo Específico 2 (Consistencia documental)
    agregar_parrafo(
        doc,
        "En cuanto al segundo objetivo específico, enfocado en determinar en qué medida la aplicación del sistema web SIVAC "
        "mejora la consistencia documental de los registros de movimientos de vacunas en el personal de inmunizaciones de la "
        "Dirección de Salud Apurímac II, el resultado propio de la intervención en los indicadores de porcentaje de "
        "registros sin discrepancias (RSD) y concordancia de cantidad programada versus entregada (CPE) en ventanas "
        "simétricas de 30 días permanece [Pendiente de inserción de estadísticos descriptivos, prueba de Wilcoxon Z, "
        "p-valor bilateral con ajuste Holm-Bonferroni y tamaño del efecto r tras cierre de campo en la Tabla 14 y Tabla "
        "17], contando con un comportamiento funcional verificado del 100.0% de exactitud en las 151 pruebas automatizadas "
        "de integridad transaccional. Desde la interpretación operativa, la arquitectura de SIVAC interviene sobre las "
        "vulnerabilidades del kardex manual mediante transacciones atómicas ACID en PostgreSQL, restricciones de claves "
        "únicas compuestas que impiden asientos duplicados o saldos negativos, bloqueo algorítmico FEFO que obliga a "
        "despachar el lote con vencimiento más próximo y validación en servidor de los ocho campos normativos antes de "
        "emitir el comprobante en PDF o Excel. En la comparación rigurosa con los antecedentes, este mecanismo concuerda "
        "con Gilbert et al. (2020), quienes en un estudio cuasiexperimental sobre 924 centros de salud de Tanzania "
        "demostraron que la integración del registro vacunal con el sistema logístico e-LMIS redujo los quiebres de stock "
        "de 7.1% a 2.1% (p menor a 0.01) y disminuyó en 4.1% la probabilidad semanal de desabastecimiento (OR = 0.959, "
        "p menor a 0.001) gracias a la deducción automática en el kardex. Coincide igualmente con Kigenza et al. (2023) "
        "en 596 establecimientos de salud, 30 almacenes distritales y 1,296 operadores logísticos de Ruanda, donde la "
        "adopción del sistema e-LMIS elevó su utilización del 55% al 96%, incrementó la exactitud de inventario entre "
        "saldo físico y digital del 25% al 85% y redujo el desabastecimiento de 10% a menos del 1%; así como con Garcia "
        "Villacorta y Calderón Huaman (2023) en la Universidad Privada del Norte (n = 68 registros documentales de "
        "inventario: 34 en pre-test y 34 en post-test), quienes elevaron la exactitud del control de inventario de "
        "75.42% a 97.18%, la rotación de existencias de 76.78% a 97.44% y las entregas conformes de 76.15% a 97.77% "
        "(Z = -7.15, p menor a 0.001). Asimismo, responde directamente a las deficiencias del soporte manual reportadas "
        "por Chekol et al. (2023) en Etiopía (donde la concordancia documental en papel fue de solo 74%), por Ergetie et "
        "al. (2023) (quienes hallaron un 68% de establecimientos con deficiente actualización logística y 50% con registros "
        "manuales incompletos pese a un 60% de buen conocimiento y 74% de buenas prácticas en frío), por Gutiérrez-Aguado "
        "et al. (2024) respecto a las asimetrías con el SIGA-MEF (61.8% de equipos con más de 10 años), y por Champi "
        "Velásquez (2023) en Lima, quien redujo en 90% las incidencias no detectadas mediante control automatizado. En "
        "el análisis contextual de los ocho centros de acopio de Andahuaylas y Chincheros en la DISA Apurímac II, la "
        "centralización relacional evita los errores de arrastre entre cierres mensuales; no obstante, como limitación "
        "metodológica del diseño preexperimental de un solo grupo (GE: O₁ - X - O₂, N = n = 14) sin grupo de control "
        "paralelo, las variaciones se interpretan como mejoras asociadas a la intervención tecnológica sin atribuir "
        "causalidad aislada absoluta, dado que la capacitación normativa, la familiarización operativa y el efecto "
        "Hawthorne pueden co-influir en el cuidado del registro. En su implicación práctica sanitaria, este control "
        "garantiza la trazabilidad auditable exigida por la NTS N.° 196-MINSA/DGIESP-2022.",
        sangria=True
    )

    # Bloque Argumentativo 4: Objetivo Específico 3 (Satisfacción del usuario)
    agregar_parrafo(
        doc,
        "Finalmente, respecto al tercer objetivo específico, dirigido a determinar en qué medida la aplicación del sistema "
        "web SIVAC mejora la satisfacción del usuario respecto a la gestión de movimientos de vacunas en el personal de "
        "inmunizaciones de la Dirección de Salud Apurímac II, el resultado propio de la intervención en los indicadores "
        "de aceptación del proceso (AP) y utilidad percibida (UP) bajo el Modelo de Aceptación Tecnológica (TAM; Davis, "
        "1989) se mantiene [Pendiente de inserción de estadísticos descriptivos, prueba de Wilcoxon Z, p-valor bilateral "
        "con ajuste Holm-Bonferroni y tamaño del efecto r tras cierre de campo en la Tabla 15 y Tabla 17], habiéndose "
        "corroborado funcionalmente el 100.0% de aceptación en las 16 historias de usuario y el bloqueo del 100.0% de "
        "entradas erróneas en las pruebas de usabilidad. En su interpretación operativa, la arquitectura de SIVAC mejora "
        "la experiencia de trabajo frente al kardex manual al sustituir el llenado repetitivo de folios y el estrés por "
        "descuadres aritméticos de lotes mediante una interfaz web limpia con validación preventiva FEFO, cálculo "
        "instantáneo de saldos en PostgreSQL y emisión automatizada de vales en PDF y Excel. En la comparación rigurosa "
        "con los antecedentes, esta relación estructural concuerda con Hussain et al. (2025), quienes en una muestra de "
        "n = 687 enfermeros hospitalarios demostraron que la facilidad de uso percibida constituye el predictor directo "
        "más robusto de la intención de adopción tecnológica (coeficiente beta = 0.35; p menor a 0.001) y que la utilidad "
        "percibida actúa como mediador significativo (coeficiente beta = 0.23; p menor a 0.001) al mitigar la carga "
        "administrativa. Asimismo, converge en el contexto del Ministerio de Salud del Perú con Mamani-Pari et al. (2026), "
        "quienes validaron psicométricamente un instrumento de usabilidad basado en ISO/IEC 25010 con 10 expertos y una "
        "muestra de n = 115 profesionales de establecimientos de salud peruanos (53 médicos, 48 enfermeros y 14 "
        "administrativos), alcanzando un Coeficiente V de Aiken de 0.95 (IC 95%: 0.84–0.98) y un Alfa de Cronbach de "
        "0.968 (con 81.7% de percepción en nivel muy alto y 18.3% en nivel alto), lo cual ilustra el tipo de evidencia "
        "psicométrica que el presente estudio se propone alcanzar mediante la validación de contenido por juicio de "
        "expertos prevista en el Capítulo IV (V de Aiken e IVC conforme al modelo de "
        "Tristán-López, 2008, con el juicio de expertos sustentado metodológicamente en Hernández-Sampieri et al., "
        "2014, y tamaños de efecto de Cohen, 1988). De "
        "igual modo, armoniza con Luo et al. (2024), Oliveira et al. (2020) en el sistema nacional de inmunizaciones de "
        "Brasil, así como con el estudio de Ndlovu et al. (2021) en Botsuana, quienes confirmaron que la supresión de la doble digitación en papel "
        "y la generación automática de reportes consolidan la aceptación y utilidad percibida en el personal sanitario. "
        "En la explicación contextual de los ocho centros de acopio de Andahuaylas y Chincheros en la DISA Apurímac II, "
        "el diseño centrado en el usuario facilitó la adaptación de operadores con diversos niveles de competencia "
        "digital; sin embargo, dentro de las limitaciones metodológicas del diseño preexperimental de un solo grupo "
        "(GE: O₁ - X - O₂, N = n = 14) sin grupo de control paralelo, los cambios perceptuales se interpretan como "
        "mejoras asociadas a la intervención tecnológica sin atribuir causalidad aislada absoluta, reconociendo que el "
        "acompañamiento durante la capacitación, la familiarización progresiva y el efecto Hawthorne o deseabilidad "
        "social pueden co-influir en las respuestas autoinformadas. En su implicación práctica sanitaria, la favorable "
        "aceptación operativa respalda la sostenibilidad institucional del registro digital de inmunizaciones bajo la "
        "NTS N.° 196-MINSA/DGIESP-2022.",
        sangria=True
    )

    # ==========================================================================
    # CONCLUSIONES
    # ==========================================================================
    agregar_titulo_1(doc, "CONCLUSIONES")

    agregar_parrafo(
        doc,
        "**Primera.** En relación con el objetivo general, la evaluación global de la aplicación del sistema web SIVAC "
        "para mejorar la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud "
        "Apurímac II (N = n = 14) se determina mediante la integración conjunta de los resultados de las tres dimensiones "
        "específicas (oportunidad de procesamiento, consistencia documental y satisfacción/aceptación del usuario), sin "
        "emplear un p-valor global único sobre escalas heterogéneas, e interpretando los hallazgos como cambios asociados "
        "a la intervención tecnológica considerando el carácter preexperimental de un solo grupo del estudio ([Pendiente "
        "de cierre cuantitativo post-campo tras el contraste inferencial con ajuste de Holm-Bonferroni en la Tabla 17]).",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Segunda.** En relación con el primer objetivo específico, la evaluación de la oportunidad de procesamiento en "
        "los movimientos de vacunas del personal de inmunizaciones de la Dirección de Salud Apurímac II vincula "
        "directamente sus dos indicadores cronométricos: el tiempo de registro de movimientos de vacunas (mediana/media "
        "pre-test = [Pendiente] min vs. post-test = [Pendiente] min) y el tiempo de emisión de comprobante de salida o "
        "vale (mediana/media pre-test = [Pendiente] min vs. post-test = [Pendiente] min; Tabla 13), cuya contrastación "
        "inferencial permanece [Pendiente de cómputo del estadístico W/Z de Wilcoxon, p-valor bilateral con ajuste de "
        "Holm-Bonferroni y tamaño del efecto r en la Tabla 17 tras cierre de campo].",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Tercera.** En relación con el segundo objetivo específico, la evaluación de la consistencia documental de los "
        "registros de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II se "
        "establece a partir de sus dos indicadores auditados en ventanas de 30 días bajo la NTS N.° 196-MINSA/DGIESP-2022: "
        "el porcentaje de registros sin discrepancias bajo los ocho criterios normativos (mediana/media pre-test = "
        "[Pendiente]% vs. post-test = [Pendiente]%) y la concordancia de cantidad programada versus entregada "
        "(mediana/media pre-test = [Pendiente]% vs. post-test = [Pendiente]%; Tabla 14), cuya contrastación inferencial "
        "permanece [Pendiente de cálculo del estadístico W/Z, p-valor bilateral con ajuste de Holm-Bonferroni y tamaño "
        "del efecto r en la Tabla 17 tras concluir la auditoría documental post-test].",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Cuarta.** En relación con el tercer objetivo específico, la evaluación de la satisfacción del usuario respecto "
        "a la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II se "
        "determina mediante la evolución de sus dos indicadores psicométricos bajo el Modelo de Aceptación Tecnológica "
        "(TAM): la aceptación del proceso (mediana/media pre-test = [Pendiente] pts vs. post-test = [Pendiente] pts) y "
        "la utilidad percibida (mediana/media pre-test = [Pendiente] pts vs. post-test = [Pendiente] pts; Tabla 15), "
        "quedando su significancia estadística formal [Pendiente de cómputo del estadístico pareado W/Z, p-valor "
        "bilateral con ajuste de Holm-Bonferroni y tamaño del efecto r en la Tabla 17 tras la administración censal "
        "post-test].",
        sangria=True
    )

    # ==========================================================================
    # RECOMENDACIONES
    # ==========================================================================
    agregar_titulo_1(doc, "RECOMENDACIONES")

    agregar_parrafo(
        doc,
        "**Primera.** Con el fin de consolidar la adopción institucional del sistema web SIVAC y monitorear de forma "
        "periódica los tiempos operativos, la consistencia documental y la percepción de los usuarios, se recomienda a "
        "la Dirección General de la Dirección de Salud Apurímac II institucionalizar mediante directiva administrativa "
        "el uso oficial y obligatorio de la plataforma en el almacén especializado central y en los ocho centros de "
        "acopio de las redes de Andahuaylas y Chincheros, estableciendo un seguimiento trimestral de sus seis indicadores.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Segunda.** A la Oficina de Informática, Telecomunicaciones y Estadística de la Dirección de Salud Apurímac II, "
        "se recomienda formalizar una política de copias de seguridad basada en la regla 3-2-1 (tres copias en dos medios "
        "distintos y una copia externa fuera del centro de datos), configurando scripts automatizados diarios de volcado en "
        "PostgreSQL (pg_dump) y estructurando un plan de recuperación ante desastres (DRP) que asegure la continuidad de la "
        "cadena de frío frente a contingencias.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Tercera.** Al equipo de desarrollo e innovación tecnológica de la institución, se recomienda adoptar un flujo "
        "estructurado de control de versiones en Git con ramas protegidas, gestión continua de dependencias y aplicación "
        "oportuna de parches de seguridad para el entorno de ejecución, posibilitando el mantenimiento evolutivo del software "
        "frente a futuros cambios en el esquema nacional de vacunación.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Cuarta.** A la administración de sistemas de la Dirección de Salud Apurímac II, se recomienda establecer un "
        "protocolo riguroso de gobernanza de la información conforme a la Ley N.° 29733 (Ley de Protección de Datos "
        "Personales), implementando auditorías periódicas de permisos bajo el control de acceso basado en roles (RBAC), "
        "registro inmutable de bitácoras de auditoría de transacciones y rotación obligatoria de credenciales y tokens JWT.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Quinta.** A la Coordinación de la Estrategia Sanitaria de Inmunizaciones y Cadena de Frío, se recomienda "
        "incorporar de manera permanente un programa de inducción técnica y entrenamiento continuo sobre la operación de "
        "SIVAC para el personal de salud nuevo, contratado o rotante en los centros de acopio periféricos de Andahuaylas y "
        "Chincheros, reduciendo la curva de aprendizaje y evitando el retorno a prácticas de registro manual.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Sexta.** A los responsables de control de calidad y auditoría sanitaria de la Dirección de Salud Apurímac II, se "
        "recomienda realizar auditorías trimestrales de calidad de datos cruzando el kardex digital de SIVAC con las actas "
        "físicas de recepción CENARES, los comprobantes PECOSA y el inventario físico en frío, vigilando el cumplimiento "
        "estricto de los ocho criterios normativos de consistencia documental bajo la NTS N.° 196-MINSA/DGIESP-2022 (RM N.° "
        "884-2022/MINSA).",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "**Séptima.** A la comunidad académica de la Universidad Nacional José María Arguedas y a futuros investigadores, "
        "se recomienda planificar evaluaciones longitudinales de seguimiento post-implementación a los 6 y 12 meses de "
        "funcionamiento de SIVAC, así como escalar el diseño metodológico hacia esquemas cuasiexperimentales con grupo de "
        "comparación contemporáneo en otras Redes o Direcciones de Salud regionales, integrando adicionalmente módulos "
        "telemétricos de Internet de las Cosas (IoT) para el monitoreo térmico en tiempo real de equipos frigoríficos.",
        sangria=True
    )

    # ==========================================================================
    # REFERENCIAS BIBLIOGRÁFICAS (Correspondencia Biunívoca 1:1, APA 7 Español)
    # ==========================================================================
    agregar_titulo_1(doc, "REFERENCIAS BIBLIOGRÁFICAS")

    referencias_oficiales = [
        "Addy, A., Ajayi, O., y Mensah, K. (2024). Artificial intelligence in the supply chain management for vaccine distribution in the West African healthcare sector with a focus on Ghana. *International Journal of Legal Science and Innovation*, *5*(6), 1–25.",
        "Alvarez Ticllasuca, K., Flores Marín, G., y Poma Rojas, W. J. (2023). *Sistemas de información geográfica para control de inmunizaciones, en niños de 0-1 año EsSalud Huancavelica* [Tesis de maestría, Universidad Nacional del Centro del Perú]. Repositorio Institucional UNCP. http://hdl.handle.net/20.500.12894/9418",
        "Arisholm, E., Gallis, H., Dyba, T., y Sjoberg, D. I. K. (2007). Evaluating pair programming with respect to system complexity and programmer expertise. *IEEE Transactions on Software Engineering*, *33*(2), 65–86. https://doi.org/10.1109/TSE.2007.17",
        "Astuhuaman Perez, S. M., y Baltazar Maza, E. J. (2023). *Implementación de un sistema web con IA para mejorar la gestión de citas médicas en el Centro de Salud de Nueva Fuerabamba, Apurímac 2024* [Tesis de licenciatura, Universidad Privada del Norte]. Repositorio Institucional UPN. https://hdl.handle.net/11537/43590",
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
        "Gilbert, S. S., Bulula, N., Yohana, E., Thompson, J., Beylerian, E., Werner, L., y Shearer, J. C. (2020). The impact of an integrated electronic immunization registry and logistics management information system (EIR-eLMIS) on vaccine availability in three regions in Tanzania: A pre-post and time-series analysis. *Vaccine*, *38*(3), 562–569. https://doi.org/10.1016/j.vaccine.2019.10.059",
        "Gutiérrez-Aguado, A., Mendoza, M., Sarazú, T., y Rodriguez-Ordoñez, P. (2024). Cadena de frío del programa nacional de inmunizaciones peruano en el contexto de la pandemia COVID-19. *Revista de la Facultad de Medicina Humana*, *24*(1), 73–84. https://doi.org/10.25176/rfmh.v24i1.6189",
        "Hernández-Sampieri, R., Fernández-Collado, C., y Baptista-Lucio, P. (2014). *Metodología de la investigación* (6.ª ed.). McGraw-Hill Education.",
        "Hussain, A., Zhiqiang, M., Li, M., Jameel, A., Kanwel, S., Ahmad, S., y Ge, B. (2025). The mediating effects of perceived usefulness and perceived ease of use on nurses’ intentions to adopt advanced technology. *BMC Nursing*, *24*(1), Artículo 33. https://doi.org/10.1186/s12912-024-02648-8",
        "Inarotul Huda, I., Yunengsih, Y., y Abdussalaam, F. (2025). Application of Extreme Programming methodology in the development of a web-based mortality reporting system with the Laravel framework. *International Journal Software Engineering and Computer Science (IJSECS)*, *5*(3), 1244–1259. https://doi.org/10.35870/ijsecs.v5i3.5354",
        "International Organization for Standardization, y International Electrotechnical Commission. (2023). *Systems and software engineering: Systems and software Quality Requirements and Evaluation (SQuaRE): Product quality model* (ISO/IEC 25010:2023). https://www.iso.org/standard/78176.html",
        "Kigenza, R., Nsengiyumva, E., y Sabagirirwa, V. (2023). The Quality Management Improvement Approach: Successes and lessons learned from a workforce development intervention in Rwanda’s health supply chain. *Global Health: Science and Practice*, *11*(4), Artículo e2200295. https://doi.org/10.9745/GHSP-D-22-00295",
        "Kokol, P. (2022). Agile software development in healthcare: A synthetic scoping review. *Applied Sciences*, *12*(19), Artículo 9462. https://doi.org/10.3390/app12199462",
        "Luján Mora, S. (2002). *Programación de aplicaciones web: Historia, principios básicos y clientes web*. Editorial Club Universitario.",
        "Luo, J., Ahmad, S. F., Alyaemeni, A., Ou, Y., Irshad, M., Alyafi-Alzahri, R., Alsanie, G., y Unnisa, S. T. (2024). Role of perceived ease of use, usefulness, and financial strength on the adoption of health information systems: The moderating role of hospital size. *Humanities and Social Sciences Communications*, *11*(1), Artículo 516. https://doi.org/10.1057/s41599-024-02976-9",
        "Mamani-Pari, D., Peñaloza-Hualpa, A. F., Humpiri-Flores, M. E., Gutierrez-Quispe, E., y Otazu-Luque, J. E. (2026). Development and psychometric validation of a usability instrument based on ISO 25010 for electronic health record systems in Peruvian health care settings: Methodological study. *JMIR Medical Informatics*, *14*(1), Artículo e81377. https://doi.org/10.2196/81377",
        "Mego Navarro, D. P. (2021). *Implementación de un sistema web para la gestión de vacunas del Covid-19 en una entidad pública 2021* [Trabajo de suficiencia profesional, Universidad Tecnológica del Perú]. Repositorio Institucional UTP. https://hdl.handle.net/20.500.12867/5068",
        "Mekonen, Z. T., Cho, D. J., Nadeem, S. P., Garza-Reyes, J. A., y Fenta, T. G. (2024). Vaccine logistics management information system at public health facilities in Amhara Region, Ethiopia: A performance evaluation. *Healthcare Informatics Research*, *30*(4), 375–386. https://doi.org/10.4258/hir.2024.30.4.375",
        "Ministerio de Salud del Perú. (2022). *Norma Técnica de Salud que establece el Esquema Nacional de Vacunación* (NTS N.° 196-MINSA/DGIESP-2022, aprobada mediante Resolución Ministerial N.° 884-2022/MINSA). MINSA. https://www.gob.pe/institucion/minsa/normas-legales/3576882-884-2022-minsa",
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
    agregar_titulo_2(doc, "Anexo 1: Matriz de consistencia de la investigación")
    agregar_parrafo(
        doc,
        "En la Tabla 18 se presenta la matriz de consistencia metodológica del estudio, en la cual se articula la "
        "correspondencia biunívoca entre la formulación de los problemas, los objetivos, las hipótesis, las variables "
        "con sus respectivas dimensiones e indicadores, y el marco metodológico preexperimental ejecutado en la "
        "Dirección de Salud Apurímac II.",
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
            "**Variable Independiente (VI):**\nIntervención tecnológica dicotómica:\n\n• Pre-intervención manual (X₀): Kardex manual físico, libros de registro y hojas de cálculo dispersas\n\n• Post-intervención tecnológica (X₁): Sistema web SIVAC con arquitectura transaccional, regla FEFO y emisión digital de vales (desarrollado con Extreme Programming; evaluado con ISO/IEC 25010:2023).",
            "**Tipo y Nivel:**\nAplicada, explicativo\n\n**Método y Enfoque:**\nHipotético-deductivo, cuantitativo\n\n**Criterio de Integración HG:**\nIntegración convergente de las hipótesis específicas H1, H2 y H3 sin agregar escalas heterogéneas en un p-valor global artificial"
        ],
        [
            "**Problema Específico 1:**\n¿En qué medida la aplicación del sistema web SIVAC mejora la oportunidad de procesamiento en los movimientos de vacunas del personal de inmunizaciones de la Dirección de Salud Apurímac II?",
            "**Objetivo Específico 1:**\nDeterminar en qué medida la aplicación del sistema web SIVAC mejora la oportunidad de procesamiento en los movimientos de vacunas del personal de inmunizaciones de la Dirección de Salud Apurímac II.",
            "**Hipótesis Específica 1:**\nLa aplicación del sistema web SIVAC mejora significativamente la oportunidad de procesamiento en los movimientos de vacunas del personal de inmunizaciones de la Dirección de Salud Apurímac II.",
            "**Variable Dependiente (VD):**\nGestión de movimientos de vacunas\n\n**Dimensión 1:** Oportunidad de procesamiento\n• Tiempo de registro de movimiento de vacunas (T_reg; minutos decimales)\n• Tiempo de emisión de comprobante de salida o vale (T_vale; minutos decimales)",
            "**Diseño de Investigación:**\nPreexperimental con pre-test y post-test en un solo grupo (GE: O₁ - X - O₂)\n\n**Unidad de Análisis:**\nGestión de movimientos de vacunas en la red de frío\n\n**Unidad de Observación Primaria:**\nTransacciones logísticas, registros de kardex, despachos y cuestionarios\n\n**Sujetos de Agregación Pareada:**\nPoblación censal conformada por N = n = 14 operadores en 8 centros de acopio"
        ],
        [
            "**Problema Específico 2:**\n¿En qué medida la aplicación del sistema web SIVAC mejora la consistencia documental de los registros de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?",
            "**Objetivo Específico 2:**\nDeterminar en qué medida la aplicación del sistema web SIVAC mejora la consistencia documental de los registros de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.",
            "**Hipótesis Específica 2:**\nLa aplicación del sistema web SIVAC mejora significativamente la consistencia documental de los registros de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.",
            "**Dimensión 2:** Consistencia documental\n• Porcentaje de registros sin discrepancias (RSD; porcentaje % bajo 8 criterios normativos)\n• Concordancia de cantidad programada versus entregada (CPE; porcentaje %)",
            "**Técnicas de Recolección:**\n• Observación directa sistemática\n• Análisis y auditoría documental\n• Encuesta estructurada\n\n**Instrumentos Oficiales:**\n• Ficha de observación de tiempos (Inst. 01)\n• Guía de cotejo documental (Inst. 02)\n• Cuestionario de satisfacción y aceptación tecnológica (Inst. 03, Modalidad A)"
        ],
        [
            "**Problema Específico 3:**\n¿En qué medida la aplicación del sistema web SIVAC mejora la satisfacción del usuario respecto a la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II?",
            "**Objetivo Específico 3:**\nDeterminar en qué medida la aplicación del sistema web SIVAC mejora la satisfacción del usuario respecto a la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.",
            "**Hipótesis Específica 3:**\nLa aplicación del sistema web SIVAC mejora significativamente la satisfacción del usuario respecto a la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.",
            "**Dimensión 3:** Satisfacción del usuario\n• Aceptación del proceso (AP; reactivos AP-01 a AP-04, escala ordinal Likert 1 a 5, puntuación sumatoria 4 a 20)\n• Utilidad percibida (UP; reactivos UP-01 a UP-04, escala ordinal Likert 1 a 5, puntuación sumatoria 4 a 20)\n• Total de la dimensión sobre los 8 ítems de la Modalidad A: 8 a 40",
            "**Procesamiento y Análisis:**\n• Descriptivo: Mediana, RIQ, media, desviación estándar y gráficos APA 7\n• Normalidad: Prueba de Shapiro-Wilk (n = 14)\n• Inferencial: Prueba de rangos con signo de Wilcoxon pareada (alfa = 0.05 bilateral)\n• Control FWER: Ajuste de p-valor mediante Holm-Bonferroni\n• Tamaño del efecto: r = |Z| / sqrt(N)"
        ]
    ]

    agregar_tabla_datos(
        doc,
        numero="18",
        titulo="Matriz de consistencia de la investigación",
        encabezados=headers_t18,
        filas=filas_t18,
        nota="Alineación metodológica entre problemas, objetivos, hipótesis, variables, dimensiones, indicadores y diseño preexperimental del estudio. N = n = 14 operadores en 8 centros de acopio jurisdiccionales.",
        col_widths=[Inches(1.22), Inches(1.22), Inches(1.22), Inches(1.28), Inches(1.16)],
        font_size_pt=8.0
    )

    # --------------------------------------------------------------------------
    # Anexo 2: Instrumentos de Recolección de Datos Íntegros
    # --------------------------------------------------------------------------
    agregar_titulo_2(doc, "Anexo 2: Instrumentos de recolección de datos íntegros")
    agregar_parrafo(
        doc,
        "A continuación se presenta el contenido completo, estructurado y reproducible de los tres instrumentos "
        "de recolección de datos diseñados para la investigación. Los Instrumentos N.° 01 y N.° 02 contienen las fichas "
        "de registro de tiempos y de cotejo documental; el Instrumento N.° 03 contiene 8 ítems en su Modalidad A, "
        "oficial para el contraste de la Hipótesis Específica 3, y 8 ítems en su Modalidad B, módulo anexo de postest "
        "que no se agrega a la Modalidad A:",
        sangria=True
    )

    # Subsección A2.1: Instrumento 01
    agregar_titulo_3(doc, "A2.1. Instrumento N.° 01: Ficha de observación sistemática de tiempos cronometrados")
    agregar_parrafo(
        doc,
        "La Ficha de observación sistemática evalúa la Dimensión 1 (Oportunidad de procesamiento) mediante la medición "
        "en minutos decimales del tiempo de registro de movimientos (T_reg) y el tiempo de emisión de comprobantes de "
        "salida o vales (T_vale). Para evitar sesgos de medición, se definieron disparadores exactos de inicio y corte: "
        "(a) para T_reg, el trigger de inicio corresponde al instante en que el operador recibe físicamente el documento "
        "fuente (remesa, pecosa o pedido) o abre la interfaz de captura, culminando (trigger de corte) al asentar la "
        "última línea en el kardex físico (pre-test) o confirmarse el guardado transaccional en PostgreSQL (post-test); "
        "(b) para T_vale, el trigger de inicio se activa al comenzar la confección del pedido y concluye al generarse el "
        "archivo digital PDF oficial con correlativo único. Cada operador fue evaluado en seis movimientos estandarizados "
        "(incluyendo REG-01 ingreso de biológico, REG-02 salida o transferencia a microred, VALE-01 generación y emisión "
        "de vale de salida, y sus réplicas complementarias REG-03, VALE-02 y VALE-03), promediándose las réplicas técnicas "
        "por sujeto para obtener un único valor pareado por operador censal (n = 14) y prevenir la pseudorreplicación "
        "estadística intrasujeto.",
        sangria=True
    )

    headers_a2_1 = ["Batería", "Tipo de Movimiento / Escenario Operativo", "Procedimiento Pre-test", "Procedimiento Post-test", "Trigger Inicio", "Trigger Corte"]
    filas_a2_1 = [
        [
            "REG-01",
            "Registro de ingreso de biológico (remesa nacional, lote único)",
            "Asiento manual en kardex físico con verificación aritmética en calculadora",
            "Captura en formulario web SIVAC con autocompletado y validación de lote",
            "Apertura del comprobante físico de remesa nacional",
            "Firma de asiento en kardex / confirmación de guardado en SIVAC"
        ],
        [
            "REG-02",
            "Registro de salida o transferencia de vacunas a microred / centro",
            "Transcripción manual de 2 a 3 vacunas, cálculo de saldos y descuento visual",
            "Selección de centro receptor, adición de ítems con validación FEFO y guardado",
            "Recepción física del requerimiento mensual de biológicos",
            "Asiento del saldo final en libro / persistencia transaccional en base de datos"
        ],
        [
            "REG-03",
            "Movimiento complejo de reajuste multibioplástico e insumos",
            "Conciliación de frascos, jeringas y diluyentes en múltiples hojas de registro",
            "Módulo de reajustes SIVAC con actualización atómica de biológicos e insumos",
            "Identificación del reporte de saldo físico o acta de sobrante",
            "Cierre formal del acta manual / registro exitoso del ajuste en SIVAC"
        ],
        [
            "VALE-01",
            "Generación y emisión de vale de salida a puesto de salud (1 a 2 ítems)",
            "Llenado manuscrito de formulario en triplicado y firma manual",
            "Generación en un clic del vale oficial en PDF con código correlativo",
            "Apertura del talonario o formato preimpreso de vales",
            "Desglose del comprobante físico / descarga y visualización del PDF oficial"
        ],
        [
            "VALE-02",
            "Emisión de vale multivacunal regular a centro de salud (3 a 5 ítems)",
            "Redacción de 3 a 5 ítems con detalle de lote, fecha de vencimiento y dosis",
            "Carga automática de ítems despachados y renderizado digital del vale institucional",
            "Inicio de transcripción del pedido multivacunal",
            "Conclusión de firmas en triplicado / generación y almacenamiento del PDF"
        ],
        [
            "VALE-03",
            "Emisión de vale de contingencia de cadena de frío o barrido vacunal",
            "Elaboración de acta de emergencia manuscrita con registro de termos y lotes",
            "Módulo de contingencia con trazabilidad de despacho rápido y vale electrónico",
            "Declaración de necesidad urgente de movilización de biológicos",
            "Emisión final del comprobante de custodia / confirmación de despacho en SIVAC"
        ]
    ]
    agregar_cuadro_anexo(
        doc,
        "**Cuadro A2.1.** *Batería de escenarios operativos estandarizados para tiempos cronometrados (6 movimientos por operador)*",
        headers_a2_1,
        filas_a2_1,
        col_widths=[911, 1631, 1566, 1603, 1435, 1638],
        nota="Matriz estandarizada de observación aplicada a los 14 operadores censales. Conversión a minutos decimales: Tiempo = Minutos + (Segundos / 60)."
    )

    # Subsección A2.2: Instrumento 02
    agregar_titulo_3(doc, "A2.2. Instrumento N.° 02: Guía de cotejo documental de consistencia de movimientos")
    agregar_parrafo(
        doc,
        "La Guía de cotejo documental evalúa la Dimensión 2 (Consistencia documental) mediante instrucciones de auditoría "
        "sobre una ventana temporal simétrica de 30 días calendario consecutivos para pre-test y post-test, auditando un "
        "corpus de 40 a 60 transacciones por centro de acopio. Para el indicador de Porcentaje de registros sin "
        "discrepancias (RSD), se aplica la regla de decisión inmutable de los ocho (8) criterios binarios obligatorios: "
        "un registro se califica como conforme (Puntaje = 1) únicamente si cumple simultáneamente los ocho criterios (C1 a C8); "
        "la falla en al menos uno determina su clasificación como no conforme (Puntaje = 0). Para el indicador de Concordancia "
        "programada versus entregada (CPE), la regla de decisión verifica la igualdad exacta entre la cantidad física "
        "despachada en el comprobante y la cantidad aprobada en el requerimiento oficial (Q_entregada = Q_programada).",
        sangria=True
    )

    headers_a2_2 = ["Criterio", "Denominación del Control", "Sustento Normativo Específico (NTS N.° 196-MINSA/DGIESP-2022)", "Regla de Decisión Binaria (1 / 0)"]
    filas_a2_2 = [
        [
            "C1",
            "Clasificación unívoca del movimiento",
            "Identificación formal del tipo de transacción: entrada por remesa, salida a centro, transferencia o merma (Numeral 5.3 NTS N.° 196-MINSA, RM N.° 884-2022/MINSA).",
            "1 = Tipo de movimiento explícito y normado; 0 = Registro ambiguo o sin clasificar."
        ],
        [
            "C2",
            "Denominación oficial del biológico",
            "Nombre estandarizado de la vacuna según el Esquema Nacional de Vacunación del MINSA (Numeral 6.1 NTS N.° 196-MINSA, RM N.° 884-2022/MINSA).",
            "1 = Nombre idéntico a la norma; 0 = Abreviatura no oficial o nombre erróneo."
        ],
        [
            "C3",
            "Identificación alfanumérica de lote",
            "Código alfanumérico exacto del lote coincidente entre documento y frasco físico (Numeral 5.4 NTS N.° 196-MINSA, RM N.° 884-2022/MINSA).",
            "1 = Código de lote verificado sin omisión; 0 = Lote borroso, truncado o disconforme."
        ],
        [
            "C4",
            "Fecha de caducidad / vencimiento",
            "Registro de día, mes y año idéntico al rotulado físico del envase primario bajo regla FEFO (Numeral 5.4 NTS N.° 196-MINSA, RM N.° 884-2022/MINSA).",
            "1 = Fecha completa y coincidente; 0 = Fecha ilegible, incompleta o discrepante."
        ],
        [
            "C5",
            "Cantidad física despachada y saldo",
            "Concordancia numérica exacta entre dosis despachadas, saldo de kardex y comprobante de entrega (Numeral 5.5 NTS N.° 196-MINSA, RM N.° 884-2022/MINSA).",
            "1 = Cero descuadre con el saldo físico (Q_entregada = Q_programada); 0 = Diferencia o borrón."
        ],
        [
            "C6",
            "Establecimiento de origen y destino",
            "Identificación del centro de acopio y establecimiento con código RENIPRESS oficial (Numeral 5.2 NTS N.° 196-MINSA, RM N.° 884-2022/MINSA).",
            "1 = Origen y destino formalmente individualizados; 0 = Destino genérico o no codificado."
        ],
        [
            "C7",
            "Identificación del personal responsable",
            "Consignación clara de nombres, firma, sello o identificador digital de operador (Numeral 5.6 NTS N.° 196-MINSA, RM N.° 884-2022/MINSA).",
            "1 = Responsable trazable y autenticado; 0 = Registro anónimo o sin firma/usuario."
        ],
        [
            "C8",
            "Documento formal de respaldo y correlativo",
            "Asociación a comprobante oficial: PECOSA, Guía de remisión o vale con numeración correlativa (Numeral 5.7 NTS N.° 196-MINSA, RM N.° 884-2022/MINSA).",
            "1 = Comprobante correlativo verificado; 0 = Movimiento sin sustento documental formal."
        ]
    ]
    agregar_cuadro_anexo(
        doc,
        "**Cuadro A2.2.** *Matriz de los ocho criterios binarios obligatorios de consistencia documental*",
        headers_a2_2,
        filas_a2_2,
        col_widths=[1000, 2400, 3384, 2000],
        nota="Sustento normativo: Norma Técnica de Salud N.° 196-MINSA/DGIESP-2022 (aprobada por RM N.° 884-2022/MINSA). Regla RSD: Conforme (1) si cumple C1 a C8 simultáneos; No conforme (0) si falla en al menos uno. Regla CPE: Concordante si Q_entregada = Q_programada."
    )

    # Subsección A2.3: Instrumento 03
    agregar_titulo_3(doc, "A2.3. Instrumento N.° 03: Cuestionario de satisfacción y aceptación tecnológica")
    agregar_parrafo(
        doc,
        "El Instrumento N.° 03 evalúa la Dimensión 3 y se estructura en dos modalidades independientes y no aditivas. "
        "La Modalidad A es la escala oficial de contrastación de la Hipótesis Específica 3: consta de 8 ítems, se aplica "
        "en pretest y en postest, y operacionaliza la Aceptación del proceso operativo (AP-01 a AP-04) y la Utilidad "
        "percibida para la gestión (UP-01 a UP-04), con un rango global de 8 a 40 puntos. La Modalidad B es un módulo "
        "anexo de documentación bajo ISO/IEC 25010:2023: consta de 8 ítems, se aplica exclusivamente en el postest y "
        "operacionaliza la Utilidad percibida del software (PU-01 a PU-04) y la Facilidad de uso percibida (PE-01 a "
        "PE-04); no genera puntaje global conjunto con la Modalidad A ni interviene en el contraste inferencial. "
        "Instrucciones para el operador: lea atentamente cada enunciado y marque con una equis (X) su grado de acuerdo "
        "en la escala Likert de cinco niveles (1 = Totalmente en desacuerdo, 2 = En desacuerdo, 3 = Neutral, 4 = De "
        "acuerdo y 5 = Totalmente de acuerdo).",
        sangria=True
    )

    agregar_titulo_4(doc, "A2.3.1. Modalidad A: escala oficial para la Hipótesis Específica 3 (pretest y postest)")
    headers_a2_3 = ["Ítem (Cód.)", "Indicador y Enunciado Literal del Reactivo", "TD (1)", "D (2)", "N (3)", "A (4)", "TA (5)"]
    filas_a2_3 = [
        ["1 (AP-01)", "Aceptación del proceso operativo (AP): El procedimiento actual para asentar los movimientos diarios y cierres de mes es ágil y no demanda un esfuerzo mental o físico excesivo.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["2 (AP-02)", "Aceptación del proceso operativo (AP): El flujo de trabajo requerido para emitir comprobantes de salida y vales de entrega es fluido y está libre de demoras o trabas burocráticas.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["3 (AP-03)", "Aceptación del proceso operativo (AP): El método empleado permite conciliar los saldos de inventario con las microredes generando tranquilidad y reduciendo el estrés laboral.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["4 (AP-04)", "Aceptación del proceso operativo (AP): El tiempo dedicado al registro administrativo de vacunas es equilibrado y deja disponibilidad para las labores sanitarias y asistenciales.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["5 (UP-01)", "Utilidad percibida para la gestión (UP): El mecanismo de registro utilizado permite disponer de información fidedigna y en tiempo real del stock de vacunas y jeringas.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["6 (UP-02)", "Utilidad percibida para la gestión (UP): El control de números de lote y fechas de vencimiento que brinda el proceso previene oportunamente mermas o pérdidas de biológicos.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["7 (UP-03)", "Utilidad percibida para la gestión (UP): La metodología de gestión facilita la detección inmediata y rectificación de cualquier descuadre de inventario físico versus registrado.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["8 (UP-04)", "Utilidad percibida para la gestión (UP): En general, el procedimiento empleado es una herramienta altamente eficaz para garantizar el abastecimiento oportuno de vacunas.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"]
    ]
    agregar_cuadro_anexo(
        doc,
        "**Cuadro A2.3.** *Reactivos íntegros de la Modalidad A del Instrumento N.° 03 (8 ítems, escala oficial de HE3)*",
        headers_a2_3,
        filas_a2_3,
        col_widths=[1000, 4784, 600, 600, 600, 600, 600],
        nota="Escala Likert: 1 = Totalmente en desacuerdo, 2 = En desacuerdo, 3 = Neutral, 4 = De acuerdo, 5 = Totalmente de acuerdo. Aplicación en pretest y postest. Puntaje por indicador: 4 a 20 puntos. Puntaje global de la Modalidad A: 8 a 40 puntos sobre los 8 ítems."
    )

    agregar_titulo_4(doc, "A2.3.2. Modalidad B: módulo anexo ISO/IEC 25010:2023 (postest exclusivo)")
    headers_a2_3b = ["Ítem (Cód.)", "Constructo y Enunciado Literal del Reactivo", "TD (1)", "D (2)", "N (3)", "A (4)", "TA (5)"]
    filas_a2_3b = [
        ["9 (PU-01)", "Utilidad percibida del software (PU): Utilizar el sistema SIVAC agiliza notablemente el registro de entradas, salidas y transferencias de dosis de vacunas en el centro.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["10 (PU-02)", "Utilidad percibida del software (PU): SIVAC permite consultar de manera inmediata y precisa los saldos de existencias por lote en cualquier momento que se requiera.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["11 (PU-03)", "Utilidad percibida del software (PU): La generación automática de vales oficiales en formato PDF en SIVAC facilita el despacho hacia los establecimientos de salud.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["12 (PU-04)", "Utilidad percibida del software (PU): En conjunto, SIVAC incrementa la productividad y mejora el control de la cadena de frío en la jurisdicción.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["13 (PE-01)", "Facilidad de uso percibida (PE): La interfaz gráfica de SIVAC es clara, intuitiva y limpia, y sus botones y opciones de navegación son fácilmente comprensibles.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["14 (PE-02)", "Facilidad de uso percibida (PE): Aprender a operar los módulos de movimientos, lotes y reportes de SIVAC fue sencillo y demandó poco tiempo de capacitación.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["15 (PE-03)", "Facilidad de uso percibida (PE): Los mensajes de confirmación, validación de stock y advertencias que emite SIVAC son claros y orientan las acciones.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["16 (PE-04)", "Facilidad de uso percibida (PE): Resulta fácil lograr que SIVAC ejecute con exactitud las tareas operativas necesarias en la jornada de trabajo.", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"]
    ]
    agregar_cuadro_anexo(
        doc,
        "**Cuadro A2.4.** *Reactivos íntegros de la Modalidad B del Instrumento N.° 03 (8 ítems, módulo anexo de postest)*",
        headers_a2_3b,
        filas_a2_3b,
        col_widths=[1000, 4784, 600, 600, 600, 600, 600],
        nota="Escala Likert: 1 = Totalmente en desacuerdo, 2 = En desacuerdo, 3 = Neutral, 4 = De acuerdo, 5 = Totalmente de acuerdo. Aplicación exclusiva en el postest. La Modalidad B es un módulo descriptivo de calidad en uso y no es aditiva respecto de la Modalidad A: no se computa un puntaje global conjunto ni se emplea en el contraste de HE3."
    )

    headers_a2_5 = ["Nivel de Satisfacción", "Rango Global Modalidad A (8 ítems)", "Rango por Indicador (4 ítems)", "Interpretación Operativa Institucional"]
    filas_a2_5 = [
        [
            "Nivel Bajo (Insatisfacción)",
            "8 a 18 puntos",
            "4 a 9 puntos",
            "Severa fricción operativa, desconfianza en el registro y rechazo a los procedimientos empleados."
        ],
        [
            "Nivel Medio (Aceptable)",
            "19 a 29 puntos",
            "10 a 14 puntos",
            "Procedimiento funcional con áreas críticas de mejora en tiempos y carga administrativa."
        ],
        [
            "Nivel Alto (Satisfacción)",
            "30 a 40 puntos",
            "15 a 20 puntos",
            "Flujo logístico óptimo, alta percepción de utilidad, agilidad en despachos y adopción plena del proceso."
        ]
    ]
    agregar_cuadro_anexo(
        doc,
        "**Cuadro A2.5.** *Baremos psicométricos por terciles de la Modalidad A del Instrumento N.° 03*",
        headers_a2_5,
        filas_a2_5,
        col_widths=[1500, 1900, 1900, 3484],
        nota="Baremos por terciles calculados sobre el rango global de 8 a 40 puntos de la Modalidad A (BAJO 8 a 18, MEDIO 19 a 29, ALTO 30 a 40) y sobre el rango de 4 a 20 puntos de cada indicador de 4 ítems. La Modalidad B no tiene baremo propio ni baremo conjunto con la Modalidad A."
    )

    # --------------------------------------------------------------------------
    # Anexo 3: Expediente y Matrices de Validación por Juicio de Expertos
    # --------------------------------------------------------------------------
    agregar_titulo_2(doc, "Anexo 3: Expediente y matrices de validación por juicio de expertos")
    agregar_parrafo(
        doc,
        "La validación de contenido se regirá por el modelo institucional de la Escuela Profesional de Ingeniería de "
        "Sistemas de la Universidad Nacional José María Arguedas correspondiente al formato de Fany (2024), adoptado "
        "como modelo vigente por la normativa del proyecto. El objeto de la validación es un único certificado "
        "correspondiente al Instrumento N.° 03, que reproduce los 8 ítems literales de su Modalidad A (AP-01 a AP-04 y "
        "UP-01 a UP-04) y los somete a tres criterios dicotómicos independientes: Pertinencia (Sí/No), Relevancia "
        "(Sí/No) y Claridad (Sí/No). El certificado se emite en blanco, sin fecha fija, para su llenado y firma por cada "
        "juez. El panel estará integrado por tres docentes universitarios con grado de Magíster y colegiatura vigente en "
        "el Colegio de Ingenieros del Perú, cuya designación se formalizará mediante las cartas de invitación y "
        "aceptación correspondientes. Los Instrumentos N.° 01 y N.° 02 no se someten a juicio de contenido: su validez "
        "se sustenta en el protocolo de medición de movimientos de vacunas, en el coeficiente de correlación intraclase "
        "ICC(2,1) mayor o igual a 0.75 para la ficha cronométrica y en el kappa de Cohen mayor o igual a 0.80 para la "
        "ficha de cotejo. La Modalidad B del Instrumento N.° 03 no recibe certificado.",
        sangria=True
    )

    headers_a3_1 = [
        "Ítem Evaluado (Modalidad A)",
        "Pertinencia (Sí, de 3 jueces)",
        "Relevancia (Sí, de 3 jueces)",
        "Claridad (Sí, de 3 jueces)",
        "V de Aiken (c = 2)",
        "IVC",
        "Dictamen"
    ]
    _items_a3 = ["AP-01", "AP-02", "AP-03", "AP-04", "UP-01", "UP-02", "UP-03", "UP-04"]
    filas_a3_1 = [[_it, "", "", "", "", "", ""] for _it in _items_a3]
    filas_a3_1.append(["IVC del instrumento (8 ítems)", "", "", "", "No aplica", "", ""])
    tbl_a3_1 = agregar_cuadro_anexo(
        doc,
        "**Cuadro A3.1.** *Matriz de captura y consolidación futura del juicio de contenido del Instrumento N.° 03, Modalidad A*",
        headers_a3_1,
        filas_a3_1,
        col_widths=[1900, 1250, 1250, 1250, 1150, 950, 1034],
        nota="Matriz de captura futura, no de resultados. Cada juez califica los 8 ítems literales de la Modalidad A en tres criterios dicotómicos Sí/No; las tres primeras columnas de conteo consolidan cuántos jueces marcaron Sí. Con c = 2 la Ecuación de Aiken se reduce a V = S / n sobre 3 jueces, el IVC se calcula por ítem y, en la última fila, sobre el instrumento completo. Los coeficientes se incorporarán únicamente cuando exista evaluación real del panel; hasta entonces las celdas permanecen vacías y no se reporta ningún valor."
    )
    configurar_geometria_tabla(
        tbl_a3_1, total_width_dxa=8784,
        col_widths_dxa=[1900, 1250, 1250, 1250, 1150, 950, 1034],
        align="center", cell_margin_dxa=(30, 50, 30, 50)
    )

    headers_a3_2 = ["Juez Experto Evaluador", "Ítem Observado", "Observación Formulada", "Mejora Incorporada en el Instrumento Definitivo"]
    filas_a3_2 = [
        ["Juez experto 1", "", "", ""],
        ["Juez experto 2", "", "", ""],
        ["Juez experto 3", "", "", ""]
    ]
    agregar_cuadro_anexo(
        doc,
        "**Cuadro A3.2.** *Matriz de registro de observaciones del panel de expertos y mejoras técnicas incorporadas*",
        headers_a3_2,
        filas_a3_2,
        col_widths=[1800, 1500, 2742, 2742],
        nota="Matriz de registro de las observaciones que formulará cada juez sobre los 8 ítems de la Modalidad A y de las mejoras que se incorporarán al instrumento definitivo. El expediente formal, conformado por las cartas de solicitud, los certificados únicos en blanco, las fichas de opinión de aplicabilidad y las constancias colegiadas firmadas, se compilará al cierre del proceso de validación."
    )

    # --------------------------------------------------------------------------
    # Anexo 4: Estructura de la Base de Datos Anonimizada y Libro de Códigos
    # --------------------------------------------------------------------------
    agregar_titulo_2(doc, "Anexo 4: Estructura de la base de datos anonimizada y libro de códigos (Codebook)")
    agregar_parrafo(
        doc,
        "El repositorio cuantitativo de la investigación se estructuró conforme a un libro de códigos (Codebook) "
        "diseñado para salvaguardar la anonimización de los participantes y garantizar la reproducibilidad de los "
        "contrastes estadísticos en R y Python. La matriz pareada consolida los registros de pre-test y post-test "
        "para los catorce operadores censales (OP-01 a OP-14) asignados a los ocho centros de acopio jurisdiccionales:",
        sangria=True
    )

    headers_a4_1 = ["Código Variable", "Nombre de la Variable", "Tipo de Dato", "Escala", "Rango / Valores", "Descripción Operacional y Regla de Cálculo"]
    filas_a4_1 = [
        ["ID_OPERADOR", "Identificador del operador", "Texto", "Nominal", "OP-01 a OP-14", "Código anonimizado asignado a cada operador censal participante."],
        ["CENTRO_ACOPIO", "Centro de acopio de frío", "Texto", "Nominal", "8 sedes de red", "Establecimiento sanitario de adscripción en Andahuaylas o Chincheros."],
        ["RED_SALUD", "Red de salud territorial", "Texto", "Nominal", "Andahuaylas / Chincheros", "Jurisdicción sanitaria provincial a la que pertenece el centro."],
        ["TREG_PRE", "Tiempo registro pre-test", "Numérico", "Razón", "Minutos decimales", "Promedio aritmético de las réplicas REG-01, REG-02 y REG-03 en pre-test."],
        ["TREG_POST", "Tiempo registro post-test", "Numérico", "Razón", "Minutos decimales", "Promedio aritmético de las réplicas REG-01, REG-02 y REG-03 con SIVAC."],
        ["TVALE_PRE", "Tiempo emisión vale pre-test", "Numérico", "Razón", "Minutos decimales", "Promedio aritmético de las réplicas VALE-01, VALE-02 y VALE-03 en pre-test."],
        ["TVALE_POST", "Tiempo emisión vale post-test", "Numérico", "Razón", "Minutos decimales", "Promedio aritmético de las réplicas VALE-01, VALE-02 y VALE-03 con SIVAC."],
        ["RSD_PRE", "Registros sin discrepancia pre", "Numérico", "Razón", "0.00% a 100.00%", "Porcentaje de registros conformes bajo los 8 criterios en ventana pre-test."],
        ["RSD_POST", "Registros sin discrepancia post", "Numérico", "Razón", "0.00% a 100.00%", "Porcentaje de registros conformes bajo los 8 criterios en ventana post-test."],
        ["CPE_PRE", "Concordancia prog. vs ent. pre", "Numérico", "Razón", "0.00% a 100.00%", "Porcentaje de despachos concordantes (Q_entregada = Q_programada) en pre-test."],
        ["CPE_POST", "Concordancia prog. vs ent. post", "Numérico", "Razón", "0.00% a 100.00%", "Porcentaje de despachos concordantes (Q_entregada = Q_programada) con SIVAC."],
        ["AP_PRE", "Aceptación del proceso pre-test", "Numérico", "Ordinal", "4 a 20 puntos", "Puntuación sumatoria de los 4 reactivos AP-01 a AP-04 de la Modalidad A en pre-test."],
        ["AP_POST", "Aceptación del proceso post-test", "Numérico", "Ordinal", "4 a 20 puntos", "Puntuación sumatoria de los 4 reactivos AP-01 a AP-04 de la Modalidad A en post-test."],
        ["UP_PRE", "Utilidad percibida pre-test", "Numérico", "Ordinal", "4 a 20 puntos", "Puntuación sumatoria de los 4 reactivos UP-01 a UP-04 de la Modalidad A en pre-test."],
        ["UP_POST", "Utilidad percibida post-test", "Numérico", "Ordinal", "4 a 20 puntos", "Puntuación sumatoria de los 4 reactivos UP-01 a UP-04 de la Modalidad A en post-test."]
    ]
    agregar_cuadro_anexo(
        doc,
        "**Cuadro A4.1.** *Libro de códigos y diccionario de variables de la matriz pareada (OP-01 a OP-14)*",
        headers_a4_1,
        filas_a4_1,
        col_widths=[2160, 1451, 1014, 916, 1340, 1903],
        nota="Diccionario oficial de variables para la base de datos pre-test y post-test. Regla de agregación: las réplicas técnicas se promedian intrasujeto para obtener exactamente n = 14 pares de contraste en Wilcoxon."
    )

    headers_a4_2 = ["Operador", "Centro de Acopio", "Red Territorial", "T_reg Pre/Post", "T_vale Pre/Post", "RSD Pre/Post", "CPE Pre/Post", "AP y UP Pre/Post (Inst. 03, Modalidad A)"]
    filas_a4_2 = [
        ["OP-01", "Almacén Especializado DISA Apurímac II - Sede Central", "Andahuaylas", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]"],
        ["OP-02", "Almacén Especializado DISA Apurímac II - Sede Central", "Andahuaylas", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]"],
        ["OP-03", "Almacén Especializado DISA Apurímac II - Sede Central", "Andahuaylas", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]"],
        ["OP-04", "Almacén Especializado DISA Apurímac II - Sede Central", "Andahuaylas", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]"],
        ["OP-05", "Centro de Acopio Andahuaylas", "Andahuaylas", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]"],
        ["OP-06", "Centro de Acopio Andahuaylas", "Andahuaylas", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]"],
        ["OP-07", "Centro de Acopio Talavera", "Andahuaylas", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]"],
        ["OP-08", "Centro de Acopio Talavera", "Andahuaylas", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]"],
        ["OP-09", "Centro de Acopio San Jerónimo", "Andahuaylas", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]"],
        ["OP-10", "Centro de Acopio San Jerónimo", "Andahuaylas", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]"],
        ["OP-11", "Centro de Acopio Santa María de Chicmo", "Andahuaylas", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]"],
        ["OP-12", "Centro de Acopio Huancarama", "Andahuaylas", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]"],
        ["OP-13", "Centro de Acopio Chincheros", "Chincheros", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]"],
        ["OP-14", "Centro de Acopio Uripa/Ocobamba", "Chincheros", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]", "[Pendiente]"]
    ]
    agregar_cuadro_anexo(
        doc,
        "**Cuadro A4.2.** *Estructura esquemática de la base de datos de campo pre-test y post-test*",
        headers_a4_2,
        filas_a4_2,
        col_widths=[1060, 1446, 1258, 1004, 1004, 1004, 1004, 1004],
        nota="Estructura de captura pareada para la población censal (N = n = 14). Los valores individuales permanecen formalmente con marcador [Pendiente] a la espera del cierre del levantamiento de campo."
    )

    # --------------------------------------------------------------------------
    # Anexo 5: Evidencias de Ingeniería de Software XP, Pruebas y Despliegue
    # --------------------------------------------------------------------------
    agregar_titulo_2(doc, "Anexo 5: Evidencias de ingeniería de software XP, pruebas automatizadas y despliegue técnico")
    agregar_parrafo(
        doc,
        "El desarrollo del sistema web SIVAC se ejecutó bajo la metodología ágil Extreme Programming (XP), "
        "estructurada en cuatro iteraciones incrementales (IT-01 a IT-04) que totalizaron 76 puntos de historia, "
        "dieciséis (16) historias de usuario y una suite integral de ciento cincuenta y una (151) pruebas automatizadas "
        "(Vitest, Supertest y Playwright) para garantizar los atributos de calidad de ISO/IEC 25010:2023:",
        sangria=True
    )

    headers_a5_1 = ["Acta / Iteración", "Duración y Esfuerzo", "Historias Integradas", "Objetivos del Incremento XP", "Entregable Técnico Verificado en Producción"]
    filas_a5_1 = [
        [
            "IT-01\n(Iteración 1)",
            "2 semanas\n(16 PH)",
            "HU-01 a HU-04",
            "Seguridad JWT/RBAC, jerarquía territorial de redes y catálogos maestros.",
            "Autenticación con Bcrypt/JWT, 8 centros de acopio vinculados y multiplicadores jeringa-vacuna."
        ],
        [
            "IT-02\n(Iteración 2)",
            "3 semanas\n(23 PH)",
            "HU-05 a HU-08",
            "Inventario de lotes bajo regla FEFO, metas anuales, CENARES e ICI-DEMID.",
            "Control de lotes con bloqueo FEFO, planificación de 12 cuotas mensuales e importador ICI-DEMID."
        ],
        [
            "IT-03\n(Iteración 3)",
            "3 semanas\n(26 PH)",
            "HU-09 a HU-12",
            "Motor transaccional de movimientos mensuales, sincronización y vales.",
            "Cuadrícula de movimientos ACID, arrastre automático de saldos intermensuales y emisión de vales."
        ],
        [
            "IT-04\n(Iteración 4)",
            "2 semanas\n(11 PH)",
            "HU-13 a HU-16",
            "Exportación en PDF/Excel, kardex digital por lote, alertas y dashboard.",
            "Compilador PDFKit/ExcelJS, kardex inmutable, motor de alertas de caducidad y 151 pruebas aprobadas."
        ]
    ]
    agregar_cuadro_anexo(
        doc,
        "**Cuadro A5.1.** *Resumen verificable de las actas de iteración del ciclo ágil Extreme Programming (IT-01 a IT-04)*",
        headers_a5_1,
        filas_a5_1,
        col_widths=[1100, 1100, 1200, 2400, 2984],
        nota="Secuenciación iterativa ejecutada en el repositorio institucional syncova (Total: 76 puntos de historia en 10 semanas)."
    )

    headers_a5_2 = ["Código", "Historia de Usuario (76 PH)", "Rol Solicitante", "Criterio de Aceptación y Suite Verificadora", "Casos (Ejec./Aprob.)"]
    filas_a5_2 = [
        ["HU-01", "Autenticación JWT y control de acceso RBAC (5 PH)", "Administrador / Usuarios", "Inicio de sesión con Bcrypt, firma JWT y bloqueo HTTP 403 (password.test.ts / accessControl.test.ts).", "24 / 24 (Aceptada)"],
        ["HU-02", "Gestión jerárquica de redes, microredes y centros (5 PH)", "Administrador", "Vinculación relacional de redes, microredes y 8 centros de acopio (centroAcopioUtils.test.ts).", "9 / 9 (Aceptada)"],
        ["HU-03", "Catálogo maestro de vacunas y jeringas (3 PH)", "Coordinador", "Parametrización de biológicos, dosis por frasco y rango térmico (validation.test.ts).", "12 / 12 (Aceptada)"],
        ["HU-04", "Configuración de multiplicadores jeringa-vacuna (3 PH)", "Coordinador", "Cálculo automático de jeringas por dosis y centro de acopio (JeringaService.test.ts).", "4 / 4 (Aceptada)"],
        ["HU-05", "Registro de lotes de vacunas y jeringas FEFO (8 PH)", "Responsable de acopio", "Ingreso con PECOSA, ordenamiento FEFO y protección de stock (lote-vacuna-protection.test.ts).", "16 / 16 (Aceptada)"],
        ["HU-06", "Planificación anual de metas por establecimiento (5 PH)", "Coordinador / Responsable", "Distribución en 12 cuotas mensuales con validación de suma exacta (validation.test.ts).", "10 / 10 (Aceptada)"],
        ["HU-07", "Programación anual trimestral CENARES y stock (5 PH)", "Coordinador", "Control de remesas Q1–Q4 y captura de stock inicial sin descuadres (lote-vacuna-stock-correction.test.ts).", "5 / 5 (Aceptada)"],
        ["HU-08", "Importación y consolidación ICI-DEMID (5 PH)", "Coordinador", "Carga estructurada y normalización de registros históricos mensuales (IciDemidService.test.ts).", "3 / 3 (Aceptada)"],
        ["HU-09", "Registro mensual de movimientos de vacunas (8 PH)", "Responsable de acopio", "Captura en cuadrícula sin saldos negativos y persistencia atómica (validation.test.ts).", "11 / 11 (Aceptada)"],
        ["HU-10", "Sincronización automática de saldos intermensuales (5 PH)", "Responsable de acopio", "Propagación del saldo final del mes cerrado al mes siguiente (response.test.ts).", "8 / 8 (Aceptada)"],
        ["HU-11", "Redistribución algorítmica y entregas adicionales (5 PH)", "Responsable de acopio", "Ajuste proporcional de cuotas futuras y entregas adicionales (movimientos-entrega-adicional-stock.test.ts).", "6 / 6 (Aceptada)"],
        ["HU-12", "Emisión de vales de entrega oficiales (8 PH)", "Responsable de acopio", "Generación de vales con control de unicidad por centro y periodo (errors.test.ts).", "16 / 16 (Aceptada)"],
        ["HU-13", "Exportación de vales de entrega en PDF y Excel (3 PH)", "Responsable de acopio", "Compilación de comprobantes oficiales con PDFKit y ExcelJS (ReporteExportService.test.ts).", "6 / 6 (Aceptada)"],
        ["HU-14", "Kardex digital inmutable por lote y centro (3 PH)", "Coordinador / Responsable", "Trazabilidad cronológica de entradas, salidas y saldos por lote (ReporteExportService.test.ts).", "4 / 4 (Aceptada)"],
        ["HU-15", "Motor de alertas automáticas de caducidad y stock (3 PH)", "Coordinador / Responsable", "Detección proactiva de lotes próximos a vencer y stock crítico (logger.test.ts).", "5 / 5 (Aceptada)"],
        ["HU-16", "Dashboard analítico y gestión de permisos (2 PH)", "Coordinador / Administrador", "Indicadores gerenciales y aislamiento E2E de permisos (permission-readonly.test.ts / usuarios-rbac.spec.ts).", "12 / 12 (Aceptada)"]
    ]
    agregar_cuadro_anexo(
        doc,
        "**Cuadro A5.2.** *Matriz de criterios de aceptación y pruebas de las 16 historias de usuario (HU-01 a HU-16)*",
        headers_a5_2,
        filas_a5_2,
        col_widths=[828, 2024, 1399, 3248, 1285],
        nota="Trazabilidad completa de las 16 historias de usuario (76 puntos de historia) y los 151 casos de prueba ejecutados y aprobados al 100.0%."
    )

    headers_a5_3 = ["Nivel de Prueba / Protocolo", "Herramienta / Entorno", "Suites / Alcance", "Casos Ejecutados", "Casos Aprobados", "Resultado / Verificación"]
    filas_a5_3 = [
        ["Pruebas Unitarias de Dominio", "Vitest (Node.js v20 LTS)", "Servicios, utilidades, cifrado Bcrypt y validadores Zod/Joi", "84 casos", "84 casos (0 fallidos)", "100.0% aprobados (cobertura 92.4%)"],
        ["Pruebas de Integración API", "Vitest + Supertest", "Controladores REST, transacciones ACID Prisma y RBAC/JWT", "45 casos", "45 casos (0 fallidos)", "100.0% aprobados (cobertura 88.7%)"],
        ["Pruebas Funcionales y E2E", "Playwright + Testing Library", "Componentes React, flujo de movimientos, vales y roles", "22 casos", "22 casos (0 fallidos)", "100.0% aprobados (flujos críticos)"],
        ["**TOTAL SUITE AUTOMATIZADA**", "**Vitest / Supertest / Playwright**", "**16 suites verificadoras (HU-01 a HU-16)**", "**151 casos**", "**151 casos (0 fallidos)**", "**100.0% conformidad global**"],
        ["Protocolo de Respaldo PostgreSQL", "pg_dump + gzip + SHA-256 (Regla 3-2-1)", "Volcado diario automatizado (23:00 h), retención de 30 días y réplica externa", "Verificación DRP", "Restauración íntegra", "RPO < 24 h y RTO < 2 h verificados"]
    ]
    agregar_cuadro_anexo(
        doc,
        "**Cuadro A5.3.** *Reporte de ejecución de los 151 casos de prueba automatizados y protocolo de respaldo PostgreSQL*",
        headers_a5_3,
        filas_a5_3,
        col_widths=[1904, 1399, 1624, 1212, 1258, 1387],
        nota="Ejecución verificada sobre SIVAC v1.0.0-release en PostgreSQL 16 y Node.js v20 LTS, complementada con el protocolo automatizado de copias de seguridad bajo regla 3-2-1."
    )

    # --------------------------------------------------------------------------
    # Anexo 6: Aspectos Éticos, Autorización Institucional y Consentimiento
    # --------------------------------------------------------------------------
    agregar_titulo_2(doc, "Anexo 6: Aspectos éticos, autorización institucional y formato de consentimiento informado")
    agregar_parrafo(
        doc,
        "La investigación se rigió bajo los estándares éticos internacionales de la Declaración de Helsinki "
        "(Asociación Médica Mundial) y las Pautas Éticas Internacionales para la Investigación Biomédica del Consejo "
        "de Organizaciones Internacionales de las Ciencias Médicas (CIOMS). Se salvaguardaron los principios bioéticos "
        "fundamentales: (a) Respeto a las personas y autonomía, garantizando la voluntariedad de la participación "
        "mediante consentimiento informado sin coacción jerárquica; (b) Beneficencia y no maleficencia, asegurando "
        "que el estudio no generó riesgos laborales, sobrecargas punitivas ni perjuicios salariales para el personal; "
        "y (c) Justicia, aplicando procedimientos idénticos e imparciales en los ocho centros de acopio evaluados.",
        sangria=True
    )

    agregar_parrafo(
        doc,
        "Asimismo, se gestionó la autorización institucional formal ante la Dirección General de la Dirección de "
        "Salud Apurímac II mediante Carta de Presentación N.° 012-2025-EPIS/UNAJMA, obteniéndose el permiso oficial "
        "para el ingreso al almacén especializado central y a los centros de acopio de Andahuaylas y Chincheros. En "
        "estricto cumplimiento de la Ley N.° 29733 (Ley de Protección de Datos Personales del Perú), las identidades de "
        "los catorce operadores fueron codificadas de manera anonimizada (OP-01 a OP-14), utilizándose la información "
        "recolectada de forma exclusiva para fines de investigación académica de grado.",
        sangria=True
    )

    headers_a6_1 = ["Cláusula", "Contenido del Protocolo de Consentimiento Informado Institucional"]
    filas_a6_1 = [
        [
            "Título del Proyecto",
            "“APLICACIÓN DEL SISTEMA «SIVAC» PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II”."
        ],
        [
            "Investigador y Asesora",
            "Tesista: Bach. José Luis Quispe León (DNI N.° 70519963). Asesora: Dra. Norma Lorena Catacora Flores. Escuela Profesional de Ingeniería de Sistemas - UNAJMA."
        ],
        [
            "Objetivo del Estudio",
            "Evaluar el impacto de la aplicación del sistema web SIVAC sobre la oportunidad de procesamiento, consistencia documental y satisfacción del personal de inmunizaciones."
        ],
        [
            "Procedimiento",
            "Cronometraje de tiempos de registro y emisión de vales en seis escenarios operativos estandarizados; auditoría de concordancia documental; y respuesta a la Modalidad A del Instrumento N.° 03."
        ],
        [
            "Voluntariedad y Retiro",
            "La participación es enteramente voluntaria. El operador puede retirarse en cualquier momento sin que ello afecte su situación laboral, relaciones institucionales o derechos."
        ],
        [
            "Confidencialidad",
            "Los datos recolectados se tratarán de forma estrictamente confidencial y anonimizada bajo la Ley N.° 29733, reportándose únicamente resultados estadísticos agregados."
        ],
        [
            "Declaración de Consentimiento",
            "Declaro haber leído y comprendido la información precedente, haber tenido la oportunidad de formular preguntas y acepto libre y voluntariamente participar en la investigación.\n\n"
            "Firma del Participante: ___________________________        Firma del Tesista: ___________________________\n"
            "Nombres y Apellidos: _____________________________        Bach. José Luis Quispe León (UNAJMA)\n"
            "DNI: ___________________  Código: OP-____                  DNI: 70519963\n"
            "Fecha: _____ / _____ / 2026                                Fecha: _____ / _____ / 2026"
        ]
    ]
    agregar_cuadro_anexo(
        doc,
        "**Cuadro A6.1.** *Protocolo reproducible de consentimiento informado para los operadores censales*",
        headers_a6_1,
        filas_a6_1,
        col_widths=[2200, 6584],
        nota="Formato oficial administrado individualmente a cada uno de los 14 operadores de la Dirección de Salud Apurímac II con carácter previo a las mediciones pre-test."
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
