import pymupdf
import json
import re
import os

pdf_path = r'C:\MisInvestigaciones\tesis\sivac\referencias\modelos_tesis\Fany_Tesis_Bachiller_2024.pdf'
doc = pymupdf.open(pdf_path)

data = {
    'metadatos_documento': {
        'archivo_fuente': 'Fany_Tesis_Bachiller_2024.pdf',
        'ruta': pdf_path,
        'paginas_totales': len(doc),
        'autora': 'Fany Quispe Tello',
        'asesor': 'MSc. Edwing Alcides Maquera Flores',
        'institucion': 'Universidad Nacional José María Arguedas (UNAJMA)',
        'facultad': 'Facultad de Ingeniería',
        'escuela': 'Escuela Profesional de Ingeniería de Sistemas (EPIS)',
        'titulo': 'INFLUENCIA DEL APLICATIVO WEBFQT PARA EL SEGUIMIENTO DE PROYECTOS DE INVERSIÓN PÚBLICA EN LA MUNICIPALIDAD DISTRITAL DE PORVENIR',
        'anio': 2024,
        'fecha_auditoria': '2026-10-21',
        'auditor': 'analista-documental (Squad A / Squad E)'
    },
    'resumen_estructural': {
        'total_paginas_preliminares': 23,
        'total_paginas_cuerpo_capitular': 43,
        'total_paginas_finales_referencias': 6,
        'total_paginas_anexos': 34,
        'orientacion_general': 'PORTRAIT',
        'paginas_landscape': [73, 74],
        'paginas_escaneadas_sin_texto': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 104, 105, 106],
        'ubicacion_numeracion': 'PIE_DE_PAGINA_DERECHA',
        'fuente_predominante': 'Arial',
        'tamanio_cuerpo_pt': 11.0,
        'interlineado': '1.5 lineas',
        'sangria_primera_linea_cm': 1.25
    },
    'paginas': []
}

for idx, page in enumerate(doc):
    p_num = idx + 1
    rect = page.rect
    w, h = rect.width, rect.height
    orient = 'LANDSCAPE' if w > h else 'PORTRAIT'
    rot = page.rotation
    
    text = page.get_text('text')
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    imgs = page.get_images()
    is_scan = (len(lines) == 0 and len(imgs) > 0)
    
    blocks = page.get_text('blocks')
    label = None
    label_bbox = None
    label_type = 'NO_IMPRESA'
    
    limit_y = 520 if orient == 'LANDSCAPE' else 760
    for b in blocks:
        txt = b[4].strip()
        if b[1] > limit_y and len(txt) <= 6:
            if re.match(r'^(i|ii|iii|iv|v|vi|vii|viii|ix|x)$', txt, re.IGNORECASE):
                label = txt
                label_bbox = [round(b[0], 1), round(b[1], 1), round(b[2], 1), round(b[3], 1)]
                label_type = 'ROMANO_MINUSCULA'
                break
            elif re.match(r'^\d+$', txt):
                label = txt
                label_bbox = [round(b[0], 1), round(b[1], 1), round(b[2], 1), round(b[3], 1)]
                label_type = 'ARABIGO'
                break

    fonts = set()
    sizes = set()
    dict_blocks = page.get_text('dict')['blocks']
    min_x, min_y, max_x, max_y = 9999, 9999, 0, 0
    for b in dict_blocks:
        if 'lines' in b:
            for l in b['lines']:
                for s in l['spans']:
                    if s['text'].strip():
                        fonts.add(s['font'])
                        sizes.add(round(s['size'], 1))
                        bx0, by0, bx1, by1 = l['bbox']
                        min_x = min(min_x, bx0)
                        min_y = min(min_y, by0)
                        max_x = max(max_x, bx1)
                        max_y = max(max_y, by1)
                        
    headings = []
    for l in lines:
        if any(k in l.upper() for k in ['CAPITULO', 'CAPÍTULO', 'INTRODUCCI', 'ÍNDICE', 'INDICE', 'RESUMEN', 'ABSTRACT', 'CHUMASQA', 'DEDICATORIA', 'AGRADECIMIENTO', 'CONCLUSIONES', 'RECOMENDACIONES', 'BIBLIOGRAFÍA', 'ANEXO']):
            if len(l) < 90:
                headings.append(l)
        elif re.match(r'^\d+\.\d+(\.\d+)?\b', l) and len(l) < 80:
            headings.append(l)

    tables = [l for l in lines if re.match(r'^Tabla\s+\d+', l, re.IGNORECASE)]
    figures = [l for l in lines if re.match(r'^Figura\s+\d+', l, re.IGNORECASE)]

    if p_num == 1:
        sec = 'PORTADA_OFICIAL'
        cat = 'PAGINAS_PRELIMINARES'
        desc = 'Portada oficial institucional UNAJMA (Anexo 17) con escudo oficial a color, título, autora, asesor, grado y fecha.'
    elif 2 <= p_num <= 14:
        sec = 'DOCUMENTO_ADMINISTRATIVO_ESCANEADO'
        cat = 'PAGINAS_PRELIMINARES'
        desc = f'Página escaneada de trámite administrativo institucional ({p_num-1}/13): acta de sustentación, informe Turnitin, conformidad asesor, dictámenes del jurado calificador.'
    elif p_num == 15:
        sec = 'DEDICATORIA'
        cat = 'PAGINAS_PRELIMINARES'
        desc = 'Dedicatoria personal de la tesista (a su padre, madre, hermanos y familia).'
    elif p_num == 16:
        sec = 'AGRADECIMIENTO'
        cat = 'PAGINAS_PRELIMINARES'
        desc = 'Agradecimiento a Dios, a la UNAJMA, docentes de la EPIS, asesor y compañeros.'
    elif 17 <= p_num <= 18:
        sec = 'INDICE_GENERAL'
        cat = 'PAGINAS_PRELIMINARES'
        desc = f'Índice general de contenidos ({p_num-16}/2), jerarquía capitular decimal con tabulación punteada y número de página.'
    elif p_num == 19:
        sec = 'INDICE_DE_FIGURAS'
        cat = 'PAGINAS_PRELIMINARES'
        desc = 'Índice de figuras (Figura 1 a Figura 9) con título descriptivo y página.'
    elif p_num == 20:
        sec = 'INDICE_DE_TABLAS'
        cat = 'PAGINAS_PRELIMINARES'
        desc = 'Índice de tablas (Tabla 1 a Tabla 19) con título descriptivo y página.'
    elif p_num == 21:
        sec = 'RESUMEN'
        cat = 'PAGINAS_PRELIMINARES'
        desc = 'Resumen estructurado en un solo párrafo en español con 5 palabras clave.'
    elif p_num == 22:
        sec = 'ABSTRACT'
        cat = 'PAGINAS_PRELIMINARES'
        desc = 'Abstract en inglés formal con 5 keywords.'
    elif p_num == 23:
        sec = 'CHUMASQA'
        cat = 'PAGINAS_PRELIMINARES'
        desc = 'Chumasqa en lengua originaria quechua chanka con 5 sapaq simikuna (keywords).'
    elif p_num == 24:
        sec = 'INTRODUCCION'
        cat = 'CUERPO_PRINCIPAL'
        desc = 'Introducción general de la investigación: motivación, justificación y síntesis capitular.'
    elif 25 <= p_num <= 28:
        sec = 'CAPITULO_I_PROBLEMA_DE_INVESTIGACION'
        cat = 'CUERPO_PRINCIPAL'
        desc = f'Capítulo I: Problema de Investigación ({p_num-24}/4). Realidad problemática, formulación general/específica, justificación e hipótesis.'
    elif 29 <= p_num <= 36:
        sec = 'CAPITULO_II_ANTECEDENTES'
        cat = 'CUERPO_PRINCIPAL'
        desc = f'Capítulo II: Antecedentes ({p_num-28}/8). Antecedentes internacionales, nacionales y locales según formato canónico UNAJMA.'
    elif 37 <= p_num <= 47:
        sec = 'CAPITULO_III_MARCO_TEORICO'
        cat = 'CUERPO_PRINCIPAL'
        desc = f'Capítulo III: Marco Teórico ({p_num-36}/11). Bases teóricas del software, Scrum/XP, gestión de proyectos y marco conceptual.'
    elif 48 <= p_num <= 53:
        sec = 'CAPITULO_IV_METODOLOGIA_DE_LA_INVESTIGACION'
        cat = 'CUERPO_PRINCIPAL'
        desc = f'Capítulo IV: Metodología ({p_num-47}/6). Tipo, nivel, diseño preexperimental, operacionalización, técnicas e instrumentos, validación y análisis de datos.'
    elif 54 <= p_num <= 63:
        sec = 'CAPITULO_V_RESULTADOS'
        cat = 'CUERPO_PRINCIPAL'
        desc = f'Capítulo V: Resultados ({p_num-53}/10). Juicio de expertos, confiabilidad, descriptivos pretest/postest, normalidad Shapiro-Wilk y contrastación de hipótesis.'
    elif 64 <= p_num <= 66:
        sec = 'CAPITULO_VI_DISCUSION'
        cat = 'CUERPO_PRINCIPAL'
        desc = f'Capítulo VI: Discusión ({p_num-63}/3). Triangulación de resultados frente a antecedentes y bases teóricas.'
    elif p_num == 67:
        sec = 'CONCLUSIONES'
        cat = 'SECCIONES_FINALES'
        desc = 'Conclusiones generales y específicas alineadas 1:1 a los objetivos de la investigación.'
    elif p_num == 68:
        sec = 'RECOMENDACIONES'
        cat = 'SECCIONES_FINALES'
        desc = 'Recomendaciones prácticas para la entidad beneficiaria, la universidad y futuros investigadores.'
    elif 69 <= p_num <= 72:
        sec = 'BIBLIOGRAFIA'
        cat = 'SECCIONES_FINALES'
        desc = f'Bibliografía y Referencias ({p_num-68}/4) en formato APA 7 con sangría francesa y DOIs.'
    elif 73 <= p_num <= 74:
        sec = 'ANEXO_1_MATRIZ_DE_CONSISTENCIA'
        cat = 'ANEXOS'
        desc = f'Anexo 1: Matriz de Consistencia ({p_num-72}/2) en orientación HORIZONTAL (LANDSCAPE).'
    elif 75 <= p_num <= 80:
        sec = 'ANEXO_2_INSTRUMENTO_DE_VALIDACION'
        cat = 'ANEXOS'
        desc = f'Anexo 2: Instrumentos y certificados de validación por juicio de 3 expertos ({p_num-74}/6).'
    elif 81 <= p_num <= 83:
        sec = 'ANEXO_3_INSTRUMENTO_DE_RECOJO_DE_DATOS'
        cat = 'ANEXOS'
        desc = f'Anexo 3: Instrumento de recolección de datos ({p_num-80}/3), cuestionario en escala Likert.'
    elif 84 <= p_num <= 90:
        sec = 'ANEXO_4_METODOLOGIA_DESARROLLO_XP'
        cat = 'ANEXOS'
        desc = f'Anexo 4: Metodología de desarrollo XP ({p_num-83}/7), historias de usuario HU-01 a HU-04, diagramas de actividades.'
    elif p_num == 91:
        sec = 'ANEXO_5_DIAGRAMA_RELACIONAL_BD'
        cat = 'ANEXOS'
        desc = 'Anexo 5: Diagrama físico relacional de la base de datos MySQL/PostgreSQL.'
    elif 92 <= p_num <= 95:
        sec = f'ANEXO_{p_num-86}_DIAGRAMA_CASOS_DE_USO'
        cat = 'ANEXOS'
        desc = f'Anexo {p_num-86}: Diagrama de casos de uso UML para roles del sistema.'
    elif p_num == 96:
        sec = 'ANEXO_10_ORGANIGRAMA'
        cat = 'ANEXOS'
        desc = 'Anexo 10: Organigrama estructural de la entidad intervenida.'
    elif 97 <= p_num <= 103:
        sec = f'ANEXO_{p_num-86}_CAPTURA_INTERFAZ_SOFTWARE'
        cat = 'ANEXOS'
        desc = f'Anexo {p_num-86}: Capturas de pantalla e interfaces de módulos del software desarrollado.'
    elif 104 <= p_num <= 106:
        sec = 'DOCUMENTOS_ESCANEADOS_FINALES'
        cat = 'ANEXOS'
        desc = f'Documentos finales escaneados ({p_num-103}/3): Constancia de aplicación y conformidad emitida por la entidad beneficiaria.'
    else:
        sec = 'DESCONOCIDO'
        cat = 'OTROS'
        desc = ''

    margins_cm = {}
    if min_x < 9999:
        margins_cm = {
            'izquierdo': round(min_x / 72 * 2.54, 2),
            'superior': round(min_y / 72 * 2.54, 2),
            'derecho': round((w - max_x) / 72 * 2.54, 2),
            'inferior': round((h - max_y) / 72 * 2.54, 2)
        }

    page_obj = {
        'pagina_pdf': p_num,
        'pagina_impresa_etiqueta': label,
        'seccion': sec,
        'categoria': cat,
        'orientacion': orient,
        'dimensiones_pt': [round(w, 2), round(h, 2)],
        'rotacion_grados': rot,
        'es_escaneo_imagen': is_scan,
        'titulos_encabezados': headings[:4],
        'primeras_lineas': lines[:3] if lines else [],
        'posicion_numeracion': label_bbox,
        'tipo_numeracion': label_type,
        'fuentes_detectadas': sorted(list(fonts)),
        'tamanios_fuente_pt': sorted(list(sizes)),
        'margenes_estimados_cm': margins_cm,
        'tablas': tables,
        'figuras': figures,
        'imagenes_count': len(imgs),
        'descripcion_forense': desc
    }
    data['paginas'].append(page_obj)

output_json_path = r'C:\MisInvestigaciones\tesis\sivac\salidas\documentos\desglose_forense_fany_2024.json'
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('JSON written successfully to', output_json_path)
print('Total pages documented:', len(data['paginas']))
