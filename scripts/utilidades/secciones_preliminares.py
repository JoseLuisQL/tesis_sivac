#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB — ENSAMBLADOR DE PÁGINAS PRELIMINARES UNAJMA
Sección 1 del documento (Numeración en romanos minúsculas: i, ii, iii...)
================================================================================
"""

import os
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx_utilidades import (
    agregar_titulo_1, agregar_titulo_2, agregar_parrafo, agregar_item_lista
)

def construir_seccion_preliminares(doc, base_dir):
    escudo_path = os.path.join(base_dir, "salidas", "figuras", "recursos_graficos", "escudo_unajma.png")
    if not os.path.exists(escudo_path):
        escudo_path = os.path.join(base_dir, "salidas", "recursos_graficos", "escudo_unajma.png")

    # --------------------------------------------------------------------------
    # 1. PORTADA INSTITUCIONAL EXTERIOR (ANEXO 17 — FORMATO EMPASTADO)
    # --------------------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(2)
    p_inst.paragraph_format.line_spacing = 1.15
    run = p_inst.add_run("UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS\n")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(15)
    run.font.bold = True
    run_fac = p_inst.add_run("FACULTAD DE INGENIERÍA\n")
    run_fac.font.name = 'Times New Roman'
    run_fac.font.size = Pt(13)
    run_fac.font.bold = True
    run_esc = p_inst.add_run("ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS")
    run_esc.font.name = 'Times New Roman'
    run_esc.font.size = Pt(12)
    run_esc.font.bold = True

    # Escudo oficial centrado
    p_esc = doc.add_paragraph()
    p_esc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_esc.paragraph_format.space_before = Pt(12)
    p_esc.paragraph_format.space_after = Pt(12)
    if os.path.exists(escudo_path):
        p_esc.add_run().add_picture(escudo_path, width=Inches(1.8))
    else:
        run_esc_alt = p_esc.add_run("[ESCUDO OFICIAL DE LA UNAJMA]")
        run_esc_alt.font.name = 'Times New Roman'
        run_esc_alt.font.size = Pt(11)
        run_esc_alt.font.italic = True

    # Tipo de Documento
    p_tipo = doc.add_paragraph()
    p_tipo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tipo.paragraph_format.space_before = Pt(6)
    p_tipo.paragraph_format.space_after = Pt(12)
    run_t = p_tipo.add_run("TESIS")
    run_t.font.name = 'Times New Roman'
    run_t.font.size = Pt(14)
    run_t.font.bold = True

    # Título oficial de la tesis
    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tit.paragraph_format.space_before = Pt(8)
    p_tit.paragraph_format.space_after = Pt(14)
    p_tit.paragraph_format.line_spacing = 1.3
    run_tit = p_tit.add_run(
        "APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS "
        "DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE "
        "SALUD APURÍMAC II"
    )
    run_tit.font.name = 'Times New Roman'
    run_tit.font.size = Pt(13)
    run_tit.font.bold = True

    # Propósito de grado
    p_prop = doc.add_paragraph()
    p_prop.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_prop.paragraph_format.space_before = Pt(10)
    p_prop.paragraph_format.space_after = Pt(14)
    p_prop.paragraph_format.line_spacing = 1.15
    run_p1 = p_prop.add_run("Para optar el Título Profesional de:\n")
    run_p1.font.name = 'Times New Roman'
    run_p1.font.size = Pt(11)
    run_p2 = p_prop.add_run("INGENIERO DE SISTEMAS")
    run_p2.font.name = 'Times New Roman'
    run_p2.font.size = Pt(12)
    run_p2.font.bold = True

    # Línea de investigación
    p_lin = doc.add_paragraph()
    p_lin.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lin.paragraph_format.space_before = Pt(6)
    p_lin.paragraph_format.space_after = Pt(14)
    p_lin.paragraph_format.line_spacing = 1.15
    run_l1 = p_lin.add_run("LÍNEA DE INVESTIGACIÓN:\n")
    run_l1.font.name = 'Times New Roman'
    run_l1.font.size = Pt(10)
    run_l1.font.bold = True
    run_l2 = p_lin.add_run("Tecnologías de Información y Comunicación en Salud")
    run_l2.font.name = 'Times New Roman'
    run_l2.font.size = Pt(11)

    # Autor y Asesor
    p_aut = doc.add_paragraph()
    p_aut.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_aut.paragraph_format.space_before = Pt(8)
    p_aut.paragraph_format.space_after = Pt(18)
    p_aut.paragraph_format.line_spacing = 1.15
    run_a1 = p_aut.add_run("AUTOR:\n")
    run_a1.font.name = 'Times New Roman'
    run_a1.font.size = Pt(10)
    run_a1.font.bold = True
    run_a2 = p_aut.add_run("Bach. José Luis Quispe León\n")
    run_a2.font.name = 'Times New Roman'
    run_a2.font.size = Pt(11)
    run_a3 = p_aut.add_run("ORCID: 0009-0000-0000-0000\n\n")
    run_a3.font.name = 'Times New Roman'
    run_a3.font.size = Pt(9.5)

    run_as1 = p_aut.add_run("ASESORA:\n")
    run_as1.font.name = 'Times New Roman'
    run_as1.font.size = Pt(10)
    run_as1.font.bold = True
    run_as2 = p_aut.add_run("Dra. Norma Lorena Catacora Flores\n")
    run_as2.font.name = 'Times New Roman'
    run_as2.font.size = Pt(11)
    run_as3 = p_aut.add_run("ORCID: 0000-0000-0000-0000")
    run_as3.font.name = 'Times New Roman'
    run_as3.font.size = Pt(9.5)

    # Ciudad y año
    p_pie = doc.add_paragraph()
    p_pie.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_pie.paragraph_format.space_before = Pt(14)
    p_pie.paragraph_format.space_after = Pt(0)
    p_pie.paragraph_format.line_spacing = 1.15
    run_c = p_pie.add_run("ANDAHUAYLAS — PERÚ\n2026")
    run_c.font.name = 'Times New Roman'
    run_c.font.size = Pt(11)
    run_c.font.bold = True

    # --------------------------------------------------------------------------
    # 2. CARÁTULA INTERIOR (ANEXO 17 — PAPEL BOND)
    # --------------------------------------------------------------------------
    doc.add_page_break()
    p_inst2 = doc.add_paragraph()
    p_inst2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst2.paragraph_format.space_before = Pt(12)
    p_inst2.paragraph_format.space_after = Pt(20)
    p_inst2.paragraph_format.line_spacing = 1.15
    r2_1 = p_inst2.add_run("UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS\n")
    r2_1.font.name = 'Times New Roman'
    r2_1.font.size = Pt(15)
    r2_1.font.bold = True
    r2_2 = p_inst2.add_run("FACULTAD DE INGENIERÍA\n")
    r2_2.font.name = 'Times New Roman'
    r2_2.font.size = Pt(13)
    r2_2.font.bold = True
    r2_3 = p_inst2.add_run("ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS")
    r2_3.font.name = 'Times New Roman'
    r2_3.font.size = Pt(12)
    r2_3.font.bold = True

    p_tit2 = doc.add_paragraph()
    p_tit2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tit2.paragraph_format.space_before = Pt(30)
    p_tit2.paragraph_format.space_after = Pt(30)
    p_tit2.paragraph_format.line_spacing = 1.3
    r2_tit = p_tit2.add_run(
        "APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS "
        "DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE "
        "SALUD APURÍMAC II"
    )
    r2_tit.font.name = 'Times New Roman'
    r2_tit.font.size = Pt(13)
    r2_tit.font.bold = True

    p_pres2 = doc.add_paragraph()
    p_pres2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_pres2.paragraph_format.space_before = Pt(20)
    p_pres2.paragraph_format.space_after = Pt(20)
    p_pres2.paragraph_format.line_spacing = 1.15
    r2_p1 = p_pres2.add_run("TESIS PRESENTADA PARA OPTAR EL TÍTULO PROFESIONAL DE:\n")
    r2_p1.font.name = 'Times New Roman'
    r2_p1.font.size = Pt(11)
    r2_p2 = p_pres2.add_run("INGENIERO DE SISTEMAS")
    r2_p2.font.name = 'Times New Roman'
    r2_p2.font.size = Pt(12)
    r2_p2.font.bold = True

    p_aut2 = doc.add_paragraph()
    p_aut2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_aut2.paragraph_format.space_before = Pt(20)
    p_aut2.paragraph_format.space_after = Pt(40)
    p_aut2.paragraph_format.line_spacing = 1.15
    r2_a1 = p_aut2.add_run("AUTOR:\n")
    r2_a1.font.name = 'Times New Roman'
    r2_a1.font.size = Pt(10)
    r2_a1.font.bold = True
    r2_a2 = p_aut2.add_run("Bach. José Luis Quispe León\n\n")
    r2_a2.font.name = 'Times New Roman'
    r2_a2.font.size = Pt(11)
    r2_as1 = p_aut2.add_run("ASESORA:\n")
    r2_as1.font.name = 'Times New Roman'
    r2_as1.font.size = Pt(10)
    r2_as1.font.bold = True
    r2_as2 = p_aut2.add_run("Dra. Norma Lorena Catacora Flores")
    r2_as2.font.name = 'Times New Roman'
    r2_as2.font.size = Pt(11)

    p_pie2 = doc.add_paragraph()
    p_pie2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_pie2.paragraph_format.space_before = Pt(40)
    p_pie2.paragraph_format.space_after = Pt(0)
    r2_c = p_pie2.add_run("ANDAHUAYLAS — PERÚ\n2026")
    r2_c.font.name = 'Times New Roman'
    r2_c.font.size = Pt(11)
    r2_c.font.bold = True

    # --------------------------------------------------------------------------
    # 3. DECLARACIÓN JURADA DE AUTENTICIDAD Y NO PLAGIO (ANEXO 32)
    # --------------------------------------------------------------------------
    agregar_titulo_1(doc, "DECLARACIÓN JURADA DE AUTENTICIDAD Y NO PLAGIO (ANEXO 32)")
    agregar_parrafo(
        doc,
        "Yo, **José Luis Quispe León**, con Documento Nacional de Identidad N° **[DNI]**, "
        "graduado de la Escuela Profesional de Ingeniería de Sistemas de la Facultad de Ingeniería de la "
        "Universidad Nacional José María Arguedas, con domicilio real en la ciudad de Andahuaylas, "
        "departamento de Apurímac;",
        sangria=True
    )
    agregar_parrafo(doc, "**DECLARO BAJO JURAMENTO QUE:**", sangria=False, negrita=True)

    declaraciones = [
        "La tesis titulada: ***\"APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II\"***, es obra de mi exclusiva autoría intelectual, bajo la asesoría y dirección metodológica de mi Asesora de Tesis.",
        "No contiene plagio, fraude, colusión, copia literal no autorizada ni apropiación de ideas ajenas. Toda cita, tabla, algoritmo, figura o extracto de fuentes científicas nacionales e internacionales ha sido debidamente referenciado y citado conforme a las normas de estilo de la American Psychological Association (APA 7.ª edición).",
        "No contiene invención, falsificación ni alteración de datos empíricos de campo; las mediciones del pretest y postest provienen exclusivamente de registros reales y observaciones directas en los centros de acopio de la Dirección de Salud Apurímac II.",
        "No ha sido presentada previa ni simultáneamente ante ninguna otra universidad, instituto superior ni entidad académica para la obtención de grado académico, título profesional o certificación técnica alguna.",
        "Asumo plenamente la responsabilidad civil, penal, ética y administrativa en caso de comprobarse cualquier falsedad o infracción a la Ley sobre el Derecho de Autor (Decreto Legislativo N° 822) y el Reglamento de Grados y Títulos de la UNAJMA."
    ]
    for idx, dec in enumerate(declaraciones, 1):
        agregar_item_lista(doc, dec, simbolo=f"{idx}.")

    agregar_parrafo(
        doc,
        "En fe de lo cual firmo la presente declaración en la ciudad de Andahuaylas, a los 30 días del mes de septiembre de 2026.",
        sangria=True
    )

    p_firma = doc.add_paragraph()
    p_firma.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_firma.paragraph_format.space_before = Pt(45)
    p_firma.paragraph_format.space_after = Pt(0)
    p_firma.paragraph_format.line_spacing = 1.15
    run_f1 = p_firma.add_run("_______________________________________\n")
    run_f1.font.name = 'Times New Roman'
    run_f2 = p_firma.add_run("Bach. José Luis Quispe León\n")
    run_f2.font.name = 'Times New Roman'
    run_f2.font.bold = True
    run_f3 = p_firma.add_run("DNI N° [DNI]\nAutor de la Tesis")
    run_f3.font.name = 'Times New Roman'

    # --------------------------------------------------------------------------
    # 4. DEDICATORIA
    # --------------------------------------------------------------------------
    agregar_titulo_1(doc, "DEDICATORIA")
    agregar_parrafo(
        doc,
        "*A Dios, por brindarme la salud, la fortaleza espiritual y la perseverancia inquebrantable a lo largo de cada etapa de mi formación académica y profesional.*",
        sangria=True, cursiva=True
    )
    agregar_parrafo(
        doc,
        "*A mis padres, cuyo amor infinito, ejemplo de sacrificio y apoyo constante han sido el motor que impulsó mis sueños de convertirme en Ingeniero de Sistemas.*",
        sangria=True, cursiva=True
    )
    agregar_parrafo(
        doc,
        "*A mis hermanos y seres queridos, por su comprensión, palabras de aliento y compañía permanente en los momentos de mayor exigencia de esta investigación.*",
        sangria=True, cursiva=True
    )
    agregar_parrafo(
        doc,
        "*Al personal de salud e inmunizaciones de la Dirección de Salud Apurímac II, cuya abnegada labor diaria en las zonas rurales de Andahuaylas y Chincheros inspiró la creación del sistema web SIVAC para dignificar y agilizar su servicio a la comunidad.*",
        sangria=True, cursiva=True
    )

    # --------------------------------------------------------------------------
    # 5. AGRADECIMIENTOS
    # --------------------------------------------------------------------------
    agregar_titulo_1(doc, "AGRADECIMIENTOS")
    agregar_parrafo(
        doc,
        "A mi alma mater, la **Universidad Nacional José María Arguedas (UNAJMA)**, y de manera especial a la **Escuela Profesional de Ingeniería de Sistemas**, por acogerme en sus aulas y formarme con sólidos principios científicos, tecnológicos, humanísticos y éticos.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "A mi Asesora de Tesis, Dra. Norma Lorena Catacora Flores, por su guía metodológica rigurosa, su paciencia orientadora y su generosa disposición para encauzar el desarrollo y la contrastación científica de este proyecto.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "A los señores miembros del Jurado Dictaminador, por sus valiosas observaciones, aportes constructivos y exigencia académica, los cuales permitieron elevar significativamente la calidad técnica y metodológica del presente informe final.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "A la **Dirección de Salud Apurímac II**, a sus autoridades de la Estrategia Sanitaria de Inmunizaciones y a los 14 profesionales de los 11 centros de acopio provinciales, por su apertura institucional, su valioso tiempo y su compromiso incondicional durante la fase de recolección de datos y pruebas de campo del sistema SIVAC.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "A mis entrañables amigos y compañeros de promoción, por los retos compartidos en los laboratorios de programación y por su sincera amistad que perdura a través del tiempo.",
        sangria=True
    )

    # --------------------------------------------------------------------------
    # 6. RESUMEN (ESPAÑOL)
    # --------------------------------------------------------------------------
    agregar_titulo_1(doc, "RESUMEN")
    agregar_parrafo(
        doc,
        "La presente investigación tuvo como objetivo determinar en qué medida la aplicación del sistema “SIVAC” mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II. El estudio fue de tipo aplicada, enfoque cuantitativo, nivel explicativo y diseño preexperimental con pretest y postest en un solo grupo (O1 → X → O2). La población censal estuvo conformada por los 14 trabajadores de salud responsables de los 11 centros de acopio provinciales de las redes de Andahuaylas y Chincheros (N = n = 14). El sistema SIVAC fue desarrollado bajo la metodología ágil Extreme Programming (XP) a lo largo de 5 iteraciones (71 puntos de historia y 15 historias de usuario) y evaluado con el estándar internacional ISO/IEC 25010:2023. La recolección de datos empleó fichas de observación cronométrica, fichas de cotejo documental y un cuestionario psicométrico basado en el Modelo de Aceptación Tecnológica (TAM), validados por juicio de tres expertos con un coeficiente V de Aiken global de 0.987. El contraste inferencial mediante la prueba de rangos con signo de Wilcoxon para muestras relacionadas se ejecutará una vez concluido el levantamiento de datos empíricos de campo certificados. Se prevé evaluar las variaciones en el tiempo de registro y emisión de vales, la consistencia documental sin discrepancias de kardex y el nivel de satisfacción del usuario bajo el modelo TAM. Se proyecta que SIVAC optimice la trazabilidad biológica en la cadena de frío provincial.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Palabras clave:** Sistema web, Extreme Programming, gestión de vacunas, cadena de frío, consistencia documental, Modelo de Aceptación Tecnológica (TAM), prueba de Wilcoxon.",
        sangria=False
    )

    # --------------------------------------------------------------------------
    # 7. ABSTRACT (INGLÉS)
    # --------------------------------------------------------------------------
    agregar_titulo_1(doc, "ABSTRACT")
    agregar_parrafo(
        doc,
        "The objective of this research was to determine the extent to which the implementation of the \"SIVAC\" system improves vaccine movement management among immunization healthcare personnel at the Apurímac II Health Directorate. The study adopted an applied type, quantitative approach, explanatory level, and a pre-experimental design with one-group pretest and posttest (O1 → X → O2). The census population comprised all 14 healthcare workers managing the 11 provincial cold chain storage facilities across the Andahuaylas and Chincheros health networks (N = n = 14). The SIVAC web system was developed following the Extreme Programming (XP) agile methodology across 5 iterations (71 story points and 15 user stories) and evaluated under the international ISO/IEC 25010:2023 quality standard. Data collection utilized chronometric observation sheets, documentary auditing checklists, and a psychometric questionnaire based on the Technology Acceptance Model (TAM), validated by three university expert judges yielding an overall Aiken's V coefficient of 0.987. Inferential hypothesis testing using the Wilcoxon signed-rank test for related samples will be executed upon completion and certification of empirical field data collection. The study aims to evaluate variations in monthly recording and voucher issuance times, documentary consistency eliminating kardex discrepancies, and user satisfaction under the TAM framework. It is anticipated that SIVAC optimizes biological traceability across provincial cold chain logistics.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Keywords:** Web system, Extreme Programming, vaccine management, cold chain, documentary consistency, Technology Acceptance Model (TAM), Wilcoxon test.",
        sangria=False
    )

    # --------------------------------------------------------------------------
    # 8. CHUMASQA (QUECHUA CHANKA)
    # --------------------------------------------------------------------------
    agregar_titulo_1(doc, "CHUMASQA")
    agregar_parrafo(
        doc,
        "Kay llamk’aypa hatun munayninmi karqan yachay SIVAC sutiyniyuq web llikapa yanapayninwan imaynatas allinchakun hampi churanakuna apaykachay Dirección de Salud Apurímac II nisqapi llamk’aqkunapaq, Andahuaylas 2025 watapi. Kay yachaymaskhayqa qillqasqam karqan taripasqa kawsaymanta (aplicada), yupay yachayman chayanapaq (cuantitativo), sut’inchasqa (explicativo), ch’ulla kuskachasqa qutupi qallariy qawariywan tukupay tupuywan (O1 → X → O2). Llapan llamk’aqkunam karqanku chunka tawayuq (N = n = 14) hampi kamayuqkuna chunka hukniyuq hampi waqaychana wasikunapi Andahuaylas hinallataq Chincheros llaqtakunapi. SIVAC web llikataqa rurarqanku Extreme Programming (XP) utqaylla yachaywan pichqa muyuriypi (qanchis chunka hukniyuq llamk’ana yupaywan chunka pichqayuq willanakuykunawan), hinallataq qawarisqa ISO/IEC 25010:2023 kamachiywan. Willaykuna huñunapaqqa llamk’achirqankum pacha tupuna rapikunata, qillqakuna qawana rapikunata, hinallataq TAM (Technology Acceptance Model) tapukuykunata, kimsantin yachaywasi yachachiqkunapa qawarisqanta Aiken V yupaywan (0.987). Wilcoxon yupaywan chimpapurayqa rurakunqa hampi waqaychana wasikunapi chiqap yupaykuna huñusqa kaptinmi. Chaywanmi qawarikunqa qillqakuna ruray pacha, hampi yupaykunapi mana pantaykuna, hinallataq llamk’aqkunapa kusisqa kawsaynin TAM kamachiywan. Suyakuntaqmi SIVAC web llikaqa hampi waqaychay chiripi ancha allin yanapaq kananta.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Chawpi rimaykuna:** Web llika, Extreme Programming, hampi waqaychay, chiri apaykachay, qillqa allinchay, TAM yachay, Wilcoxon chimpapuray.",
        sangria=False
    )

    # --------------------------------------------------------------------------
    # 9. ÍNDICE GENERAL
    # --------------------------------------------------------------------------
    agregar_titulo_1(doc, "ÍNDICE GENERAL")
    indices = [
        ("DEDICATORIA", "ii"),
        ("AGRADECIMIENTOS", "iii"),
        ("RESUMEN", "iv"),
        ("ABSTRACT", "v"),
        ("CHUMASQA", "vi"),
        ("ÍNDICE GENERAL", "vii"),
        ("ÍNDICE DE TABLAS", "viii"),
        ("ÍNDICE DE FIGURAS", "ix"),
        ("INTRODUCCIÓN", "1"),
        ("CAPÍTULO I: PROBLEMA DE INVESTIGACIÓN", "3"),
        ("1.1. Descripción de la Realidad Problemática", "3"),
        ("1.2. Formulación del Problema", "8"),
        ("1.3. Objetivos de la Investigación", "9"),
        ("1.4. Justificación de la Investigación", "10"),
        ("1.5. Delimitaciones y Limitaciones", "12"),
        ("CAPÍTULO II: ANTECEDENTES DE LA INVESTIGACIÓN", "14"),
        ("2.1. Antecedentes a Nivel Internacional", "14"),
        ("2.2. Antecedentes a Nivel Nacional", "20"),
        ("2.3. Síntesis y Matriz Comparativa de Antecedentes", "25"),
        ("CAPÍTULO III: MARCO TEÓRICO", "27"),
        ("3.1. Bases Teóricas Disciplinarias", "27"),
        ("3.2. Definición de Términos Básicos", "35"),
        ("3.3. Metodología de Desarrollo del Software SIVAC (Extreme Programming - XP)", "38"),
        ("CAPÍTULO IV: METODOLOGÍA DE LA INVESTIGACIÓN", "58"),
        ("4.1. Tipo, Enfoque, Nivel y Diseño de Investigación", "58"),
        ("4.2. Hipótesis de Investigación", "61"),
        ("4.3. Variables y Operacionalización", "63"),
        ("4.4. Población, Muestra y Muestreo", "66"),
        ("4.5. Técnicas e Instrumentos de Recolección de Datos", "68"),
        ("4.6. Validación y Confiabilidad de los Instrumentos", "70"),
        ("4.7. Plan de Análisis Estadístico", "74"),
        ("CAPÍTULO V: RESULTADOS Y CONTRASTACIÓN DE HIPÓTESIS", "77"),
        ("5.1. Análisis Descriptivo de la Variable Independiente (SIVAC)", "77"),
        ("5.2. Análisis Descriptivo de la Variable Dependiente", "81"),
        ("5.3. Pruebas de Normalidad de Shapiro-Wilk", "88"),
        ("5.4. Contrastación Inferencial de Hipótesis (Wilcoxon)", "90"),
        ("5.5. Evaluación Psicométrica Postest del Cuestionario TAM", "95"),
        ("CAPÍTULO VI: DISCUSIÓN", "97"),
        ("6.1. Contrastación de Resultados con Antecedentes", "97"),
        ("6.2. Implicancias Sanitarias y Tecnológicas", "104"),
        ("6.3. Limitaciones Metodológicas y del Trabajo de Campo", "106"),
        ("CONCLUSIONES", "108"),
        ("RECOMENDACIONES", "111"),
        ("REFERENCIAS BIBLIOGRÁFICAS", "114"),
        ("ANEXOS", "122"),
        ("Anexo 1: Matriz de Consistencia Metodológica Definitiva", "123"),
        ("Anexo 2: Matriz de Operacionalización de Variables", "125"),
        ("Anexo 3: Instrumentos de Recolección de Datos Validados", "128"),
        ("Anexo 4: Certificados de Validación por Juicio de Expertos (Aiken V = 0.987)", "134")
    ]
    for tit, pag in indices:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_before = Pt(1)
        p_item.paragraph_format.space_after = Pt(1)
        p_item.paragraph_format.line_spacing = 1.15
        p_item.paragraph_format.first_line_indent = Inches(0)
        es_cap = tit.startswith("CAPÍTULO") or tit in ["DEDICATORIA", "AGRADECIMIENTOS", "RESUMEN", "ABSTRACT", "CHUMASQA", "ÍNDICE GENERAL", "ÍNDICE DE TABLAS", "ÍNDICE DE FIGURAS", "INTRODUCCIÓN", "CONCLUSIONES", "RECOMENDACIONES", "REFERENCIAS BIBLIOGRÁFICAS", "ANEXOS"]
        sangria = Inches(0) if es_cap else Inches(0.3)
        p_item.paragraph_format.left_indent = sangria

        r_t = p_item.add_run(tit)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(11)
        r_t.font.bold = es_cap

        puntos = " " + "." * max(5, 75 - len(tit) - len(pag) - (6 if not es_cap else 0)) + " "
        r_dots = p_item.add_run(puntos)
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(120, 120, 120)

        r_p = p_item.add_run(pag)
        r_p.font.name = 'Times New Roman'
        r_p.font.size = Pt(11)
        r_p.font.bold = es_cap

    # --------------------------------------------------------------------------
    # 10. ÍNDICE DE TABLAS
    # --------------------------------------------------------------------------
    agregar_titulo_1(doc, "ÍNDICE DE TABLAS")
    tablas_idx = [
        ("Tabla 2.1", "Matriz de correspondencia de antecedentes de investigación", "26"),
        ("Tabla 3.1", "Modelo de calidad del producto de software según ISO/IEC 25010:2023", "30"),
        ("Tabla 3.2", "Pila tecnológica y componentes de arquitectura de software de SIVAC", "41"),
        ("Tabla 3.3", "Matriz consolidada de Historias de Usuario de SIVAC (15 HU)", "45"),
        ("Tabla 4.1", "Matriz de Operacionalización de las Variables de Estudio", "64"),
        ("Tabla 4.2", "Distribución de la Población Censal por Centro de Acopio y Microred", "67"),
        ("Tabla 4.3", "Evaluación de Validez de Contenido por Juicio de Expertos (Coeficiente V de Aiken)", "72"),
        ("Tabla 5.1", "Métricas de Calidad de Software del Sistema Web SIVAC (ISO/IEC 25010:2023)", "78"),
        ("Tabla 5.2", "Tiempos de Registro Mensual de Movimientos de Vacunas (T_reg) Pretest vs Postest", "82"),
        ("Tabla 5.3", "Tiempos de Emisión de Vales Oficiales de Entrega (T_vale) Pretest vs Postest", "83"),
        ("Tabla 5.4", "Porcentaje de Registros sin Discrepancias (RSD) Pretest vs Postest", "85"),
        ("Tabla 5.5", "Porcentaje de Concordancia Programada vs Entregada (CPE) Pretest vs Postest", "86"),
        ("Tabla 5.6", "Puntuaciones del Modelo de Aceptación Tecnológica (TAM) Pretest vs Postest", "87"),
        ("Tabla 5.7", "Pruebas de Normalidad de Shapiro-Wilk sobre Diferencias Pareadas", "89"),
        ("Tabla 5.8", "Síntesis de Contrastación Inferencial de Hipótesis mediante Prueba de Wilcoxon", "91"),
        ("Tabla 5.9", "Confiabilidad Psicométrica Postest del Cuestionario TAM (Alfa de Cronbach)", "96")
    ]
    for num, tit, pag in tablas_idx:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(2)
        p_t.paragraph_format.space_after = Pt(2)
        p_t.paragraph_format.line_spacing = 1.15
        p_t.paragraph_format.first_line_indent = Inches(0)

        r_n = p_t.add_run(f"{num}: ")
        r_n.font.name = 'Times New Roman'
        r_n.font.size = Pt(11)
        r_n.font.bold = True

        r_t = p_t.add_run(tit)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(11)
        r_t.font.italic = True

        puntos = " " + "." * max(5, 75 - len(num) - len(tit) - len(pag) - 3) + " "
        r_dots = p_t.add_run(puntos)
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(120, 120, 120)

        r_p = p_t.add_run(pag)
        r_p.font.name = 'Times New Roman'
        r_p.font.size = Pt(11)

    # --------------------------------------------------------------------------
    # 11. ÍNDICE DE FIGURAS
    # --------------------------------------------------------------------------
    agregar_titulo_1(doc, "ÍNDICE DE FIGURAS")
    figuras_idx = [
        ("Figura 3.1", "Diagrama de Arquitectura N-Capas Desacoplada y API REST de SIVAC", "40"),
        ("Figura 3.2", "Fases iterativas de la metodología ágil Extreme Programming (XP)", "43"),
        ("Figura 3.3", "Diagrama de Entidad-Relación (DER) de Base de Datos PostgreSQL/Prisma", "48"),
        ("Figura 4.1", "Diagrama del Procedimiento Metodológico en Tres Etapas (Pretest, XP, Postest)", "69"),
        ("Figura 5.1", "Diagrama de Cajas Pareado de Tiempos de Procesamiento (T_reg y T_vale) a 300 DPI", "84"),
        ("Figura 5.2", "Diagrama de Cajas Pareado de Consistencia Documental (RSD y CPE) a 300 DPI", "87"),
        ("Figura 5.3", "Diagrama de Cajas Pareado de Satisfacción del Usuario (TAM Total, AP, UP) a 300 DPI", "88")
    ]
    for num, tit, pag in figuras_idx:
        p_f = doc.add_paragraph()
        p_f.paragraph_format.space_before = Pt(2)
        p_f.paragraph_format.space_after = Pt(2)
        p_f.paragraph_format.line_spacing = 1.15
        p_f.paragraph_format.first_line_indent = Inches(0)

        r_n = p_f.add_run(f"{num}: ")
        r_n.font.name = 'Times New Roman'
        r_n.font.size = Pt(11)
        r_n.font.bold = True

        r_t = p_f.add_run(tit)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(11)
        r_t.font.italic = True

        puntos = " " + "." * max(5, 75 - len(num) - len(tit) - len(pag) - 3) + " "
        r_dots = p_f.add_run(puntos)
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(120, 120, 120)

        r_p = p_f.add_run(pag)
        r_p.font.name = 'Times New Roman'
        r_p.font.size = Pt(11)

    print("[*] Sección de preliminares construida exitosamente.")
