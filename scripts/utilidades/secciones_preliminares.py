#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - ENSAMBLADOR DE PÁGINAS PRELIMINARES UNAJMA
Sección 1 del documento (Numeración en romanos minúsculas: i, ii, iii...)
================================================================================
"""

import os
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx_utilidades import (
    agregar_titulo_1, agregar_titulo_2, agregar_parrafo, agregar_item_lista,
    agregar_indice_contenido_nativo, agregar_indice_tablas_nativo, agregar_indice_figuras_nativo
)

def construir_seccion_preliminares(doc, base_dir):
    escudo_path = os.path.join(base_dir, "salidas", "figuras", "recursos_graficos", "escudo_unajma.png")
    if not os.path.exists(escudo_path):
        escudo_path = os.path.join(base_dir, "salidas", "recursos_graficos", "escudo_unajma.png")

    # --------------------------------------------------------------------------
    # 1. PORTADA INSTITUCIONAL EXTERIOR (ANEXO 17 - FORMATO EMPASTADO)
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
    run_c = p_pie.add_run("ANDAHUAYLAS - PERÚ\n2026")
    run_c.font.name = 'Times New Roman'
    run_c.font.size = Pt(11)
    run_c.font.bold = True

    # --------------------------------------------------------------------------
    # 2. DECLARACIÓN JURADA DE AUTENTICIDAD Y NO PLAGIO (ANEXO 32)
    # --------------------------------------------------------------------------
    p_dec_tit = agregar_titulo_1(doc, "DECLARACIÓN JURADA DE AUTENTICIDAD Y NO PLAGIO (ANEXO 32)", incluir_en_toc=False)
    p_dec_tit.paragraph_format.space_before = Pt(0)
    p_dec_tit.paragraph_format.space_after = Pt(8)

    p_dec_intro = agregar_parrafo(
        doc,
        "Yo, **José Luis Quispe León**, con Documento Nacional de Identidad N° **[DNI]**, "
        "graduado de la Escuela Profesional de Ingeniería de Sistemas de la Facultad de Ingeniería de la "
        "Universidad Nacional José María Arguedas, con domicilio real en la ciudad de Andahuaylas, "
        "departamento de Apurímac;",
        sangria=True
    )
    p_dec_intro.paragraph_format.line_spacing = 1.15
    p_dec_intro.paragraph_format.space_after = Pt(4)

    p_dec_jur = agregar_parrafo(doc, "**DECLARO BAJO JURAMENTO QUE:**", sangria=False, negrita=True)
    p_dec_jur.paragraph_format.space_before = Pt(4)
    p_dec_jur.paragraph_format.space_after = Pt(4)

    declaraciones = [
        "La tesis titulada: ***\"APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II\"***, es obra de mi exclusiva autoría intelectual, bajo la asesoría y dirección metodológica de mi Asesora de Tesis.",
        "No contiene plagio, fraude, colusión, copia literal no autorizada ni apropiación de ideas ajenas. Toda cita, tabla, algoritmo, figura o extracto de fuentes científicas nacionales e internacionales ha sido debidamente referenciado y citado conforme a las normas de estilo de la American Psychological Association (APA 7.ª edición).",
        "No contiene invención, falsificación ni alteración de datos empíricos de campo; las mediciones del pretest y postest provienen exclusivamente de registros reales y observaciones directas en los centros de acopio de la Dirección de Salud Apurímac II.",
        "No ha sido presentada previa ni simultáneamente ante ninguna otra universidad, instituto superior ni entidad académica para la obtención de grado académico, título profesional o certificación técnica alguna.",
        "Asumo plenamente la responsabilidad civil, penal, ética y administrativa en caso de comprobarse cualquier falsedad o infracción a la Ley sobre el Derecho de Autor (Decreto Legislativo N° 822) y el Reglamento de Grados y Títulos de la UNAJMA."
    ]
    for idx, dec in enumerate(declaraciones, 1):
        p_item = agregar_item_lista(doc, dec, simbolo=f"{idx}.")
        p_item.paragraph_format.line_spacing = 1.15
        p_item.paragraph_format.space_after = Pt(3)

    p_dec_fe = agregar_parrafo(
        doc,
        "En fe de lo cual firmo la presente declaración en la ciudad de Andahuaylas, a los 30 días del mes de septiembre de 2026.",
        sangria=True
    )
    p_dec_fe.paragraph_format.line_spacing = 1.15
    p_dec_fe.paragraph_format.space_before = Pt(4)
    p_dec_fe.paragraph_format.space_after = Pt(4)

    p_firma = doc.add_paragraph()
    p_firma.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_firma.paragraph_format.space_before = Pt(28)
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
    # 3. DEDICATORIA
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
        "A mi Asesora de Tesis, Dra. Norma Lorena Catacora Flores, por su guía metodológica rigurosa, su paciencia orientadora y su generosa disposición para encauzar el desarrollo y la contrastación científica de esta investigación.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "A los señores miembros del Jurado Dictaminador, por sus valiosas observaciones, aportes constructivos y exigencia académica, los cuales permitieron elevar significativamente la calidad técnica y metodológica del presente informe final.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "A la **Dirección de Salud Apurímac II**, a sus autoridades de la Estrategia Sanitaria de Inmunizaciones y a los 14 profesionales de los 8 centros de acopio provinciales, por su apertura institucional, su valioso tiempo y su compromiso incondicional durante la fase de recolección de datos y validación operativa del sistema web SIVAC.",
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
        "Esta investigación tuvo como finalidad determinar en qué medida la aplicación del sistema “SIVAC” mejora la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II. El estudio se desarrolló bajo un enfoque cuantitativo, tipo aplicada, nivel explicativo y diseño preexperimental con pretest y postest en un solo grupo (O1 → X → O2). La población censal estuvo conformada por los 14 trabajadores de salud responsables de los 8 centros de acopio provinciales de las redes de Andahuaylas y Chincheros (N = n = 14). El sistema web SIVAC fue construido mediante la metodología ágil Extreme Programming (XP) a lo largo de cuatro iteraciones (76 puntos de historia y 16 historias de usuario) y evaluado bajo el estándar internacional ISO/IEC 25010:2023. La recolección de datos empleó fichas de observación cronométrica, guías de cotejo documental y un cuestionario estructurado basado en el Modelo de Aceptación Tecnológica (TAM), validados por juicio de tres expertos con un coeficiente V de Aiken global de 0.987 e Índice de Validez de Contenido de 1.00. El protocolo de contrastación inferencial se estructuró mediante la prueba de normalidad de Shapiro-Wilk y la prueba de rangos con signo de Wilcoxon para muestras relacionadas (α = 0.05), evaluando el tiempo de registro y emisión de vales en la dimensión de oportunidad de procesamiento, los registros sin discrepancias y la concordancia programada versus entregada en la dimensión de consistencia documental, así como la aceptación del proceso y la utilidad percibida en la dimensión de satisfacción del usuario.",
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
        "This research aimed to determine the extent to which the application of the \"SIVAC\" system improves vaccine movement management among immunization healthcare personnel at the Apurímac II Health Directorate. The study was conducted under a quantitative approach, applied type, explanatory level, and a pre-experimental design with a single-group pretest and posttest (O1 → X → O2). The census population comprised all 14 healthcare workers responsible for the 8 provincial cold chain storage centers across the Andahuaylas and Chincheros health networks (N = n = 14). The SIVAC web system was built using the Extreme Programming (XP) agile methodology across four iterations (76 story points and 16 user stories) and evaluated under the international ISO/IEC 25010:2023 quality standard. Data collection utilized chronometric observation sheets, documentary auditing checklists, and a structured questionnaire based on the Technology Acceptance Model (TAM), validated by three expert judges with an overall Aiken's V coefficient of 0.987 and a Content Validity Index of 1.00. The inferential hypothesis testing protocol was structured using the Shapiro-Wilk normality test and the Wilcoxon signed-rank test for related samples (α = 0.05), evaluating recording and voucher issuance times within the processing timeliness dimension, discrepancy-free records and scheduled-versus-delivered concordance within the documentary consistency dimension, as well as process acceptance and perceived usefulness within the user satisfaction dimension.",
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
        "Kay yachaymaskhaypa hatun munayninmi karqa SIVAC sutiyniyuq web llikapa yanapayninwan imaynatas hampi churanakuna apaykachay allinchakusqanta tupuy, Dirección de Salud Apurímac II nisqapi inmunizaciones llamk’aqkunapi. Kay t’aqwiyqa rurakurqa yupay yachayman chayanapaq (cuantitativo), taripasqa kawsaymanta (aplicada), sut’inchasqa (explicativo), ch’ulla kuskachasqa qutupi qallariy qawariywan tukupay tupuywan (O1 → X → O2). Llapan llamk’aqkunam karqanku chunka tawayuq (N = n = 14) hampi kamayuqkuna pusaq hampi waqaychana wasikunapi Andahuaylas hinallataq Chincheros llaqtakunapi. SIVAC web llikataqa rurarqanku Extreme Programming (XP) utqaylla yachaywan tawa muyuriypi (qanchis chunka suqtayuq llamk’ana yupaywan chunka suqtayuq willanakuykunawan), hinallataq qawarikurqa ISO/IEC 25010:2023 kamachiywan. Willaykuna huñunapaqqa llamk’achikurqam pacha tupuna rapikunata, qillqakuna qawana rapikunata, hinallataq TAM (Technology Acceptance Model) tapukuykunata, kimsantin yachaywasi amawtakunapa allin nisqanwan Aiken V yupaypi (0.987). Chimpapuray tupuyqa wakichikurqa Shapiro-Wilk hinallataq Wilcoxon yupaywan (α = 0.05), chaywanmi qawarikurqa qillqakuna ruray pacha utqaylla ruraypi, hampi yupaykunapi mana pantaykuna qillqa chiqap kayninpi, hinallataq llamk’aqkunapa kusisqa chaskikuynin TAM kamachiywan.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**Chawpi rimaykuna:** Web llika, Extreme Programming, hampi waqaychay, chiri apaykachay, qillqa chiqap kaynin, TAM yachay, Wilcoxon chimpapuray.",
        sangria=False
    )

    # --------------------------------------------------------------------------
    # 8. ÍNDICE DE CONTENIDO
    # --------------------------------------------------------------------------
    agregar_titulo_1(doc, "ÍNDICE DE CONTENIDO", incluir_en_toc=False)
    agregar_indice_contenido_nativo(doc)

    # --------------------------------------------------------------------------
    # 9. ÍNDICE DE TABLAS
    # --------------------------------------------------------------------------
    agregar_titulo_1(doc, "ÍNDICE DE TABLAS", incluir_en_toc=False)
    agregar_indice_tablas_nativo(doc)

    # --------------------------------------------------------------------------
    # 10. ÍNDICE DE FIGURAS
    # --------------------------------------------------------------------------
    agregar_titulo_1(doc, "ÍNDICE DE FIGURAS", incluir_en_toc=False)
    agregar_indice_figuras_nativo(doc)

    print("[*] Sección de preliminares construida exitosamente.")
