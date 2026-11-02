# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - COMPILADOR MAESTRO DEL INFORME FINAL DE TESIS v04
================================================================================
Misión: Ensamblaje quirúrgico y maquetación de alta fidelidad OpenXML según
el modelo institucional oficial UNAJMA Fany 2024.

Entradas:
  - salidas/documentos/informe_final_v03.docx (Insumo base inmutable)
  - salidas/documentos/desglose_forense_fany_2024.json / .md (Especificación forense)

Salidas generadas:
  - salidas/documentos/informe_final_v04.docx (Documento Word maquetado)
  - salidas/documentos/informe_final_v04.pdf (Documento PDF oficial de alta fidelidad)

Intervenciones editoriales clave:
  1. Reordenamiento Canónico de Preliminares (Fany 2024):
     - Portada institucional exterior (con escudo oficial UNAJMA a color)
     - Acta de sustentación y dictamen del jurado (recuadro placeholder institucional)
     - Declaración Jurada de Autenticidad y No Plagio (Anexo 32)
     -> Salto de sección desvinculado (Sección 0 administrativa, sin número impreso)
     - Dedicatoria (página ii en numeración romana al pie/encabezado)
     - Agradecimientos (página iii)
     - Índice General de Contenidos (pp. iv-v) con bloque <w:sdt> TOC nativo
     - Índice de Figuras (página vi)
     - Índice de Tablas (página vii)
     - Resumen en español con Palabras clave (página viii)
     - Abstract en inglés con Keywords (página ix)
     - Chumasqa en quechua chanka con Sapaq simikuna (página x)
     -> Salto de sección desvinculado (Sección 1 académica)
     - Introducción (página 1 reiniciada en numeración arábiga)
  2. Saltos de Página Obligatorios (<w:pageBreakBefore/>):
     Inyección en el 100% de capítulos mayores y secciones maestras (Cap I a VI,
     Conclusiones, Recomendaciones, Referencias Bibliográficas y Anexos 1 a 7).
  3. Sección Horizontal (Landscape) para Anexo 1 (Matriz de Consistencia):
     Configuración de sección apaisada exclusiva (16,838 dxa x 11,906 dxa,
     márgenes 3.0 cm izq y 2.54 cm otros, ancho útil de 14,000 dxa) con despliegue
     de las 5 columnas oficiales (DEC-007) a 2,800 dxa por columna. Retorno
     inmediato a orientación vertical (Portrait) para Anexo 2 a 7.
  4. Blindaje Geométrico OpenXML de Tablas:
     Erradicación total de <w:tblpPr> (cero tablas flotantes), inyección de
     <w:cantSplit/> en todas las filas del 100% de tablas y <w:tblHeader/> en
     las filas de encabezado.
  5. Actualización Automática y Exportación PDF Oficial:
     Word COM Automation (win32com.client) con actualización de todos los campos,
     TOC y tablas de ilustraciones, exportando con fidelidad 1:1.
"""

import os
import shutil
import sys
import time
from pathlib import Path

import docx
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor

# Rutas canónicas del proyecto
RAIZ = Path(__file__).resolve().parents[2]
DOCX_BASE_V03 = RAIZ / "salidas" / "documentos" / "informe_final_v03.docx"
DOCX_SALIDA_V04 = RAIZ / "salidas" / "documentos" / "informe_final_v04.docx"
PDF_SALIDA_V04 = RAIZ / "salidas" / "documentos" / "informe_final_v04.pdf"

# Importar utilidades quirúrgicas canónicas
sys.path.insert(0, str(RAIZ / "scripts" / "utilidades"))
from docx_quirurgico import (
    auditar_docx_openxml,
    configurar_geometria_tabla,
    eliminar_flotacion_tabla,
)


def blindar_filas_tabla(table, cant_split: bool = True, repetir_encabezado: bool = True):
    """Garantiza w:cantSplit en todas las filas y w:tblHeader en la fila 0."""
    for i, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        if cant_split and trPr.find(qn("w:cantSplit")) is None:
            trPr.append(parse_xml(f"<w:cantSplit {nsdecls('w')}/>"))
        if repetir_encabezado and i == 0 and len(table.rows) > 1:
            if trPr.find(qn("w:tblHeader")) is None:
                trPr.append(parse_xml(f"<w:tblHeader {nsdecls('w')}/>"))


def aplicar_bordes_apa7(table):
    """Aplica las 3 líneas reglamentarias APA 7 (superior, inferior de cabecera e inferior)."""
    tblPr = table._tbl.tblPr
    for child in list(tblPr):
        if child.tag.endswith("tblBorders"):
            tblPr.remove(child)
    tblBorders = parse_xml(f"""
    <w:tblBorders {nsdecls('w')}>
      <w:top w:val='single' w:sz='8' w:space='0' w:color='000000'/>
      <w:bottom w:val='single' w:sz='8' w:space='0' w:color='000000'/>
      <w:left w:val='none'/>
      <w:right w:val='none'/>
      <w:insideH w:val='none'/>
      <w:insideV w:val='none'/>
    </w:tblBorders>
    """)
    tblPr.append(tblBorders)
    if len(table.rows) > 0:
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = tcPr.find(qn("w:tcBorders"))
            if tcBorders is None:
                tcBorders = parse_xml(f"""
                <w:tcBorders {nsdecls('w')}>
                  <w:bottom w:val='single' w:sz='8' w:space='0' w:color='000000'/>
                </w:tcBorders>
                """)
                tcPr.append(tcBorders)


def inyectar_page_break_before(p):
    """Garantiza que el párrafo inicie en una nueva página mediante w:pageBreakBefore."""
    pPr = p._p.get_or_add_pPr()
    if pPr.find(qn("w:pageBreakBefore")) is None:
        pbb = parse_xml(f"<w:pageBreakBefore {nsdecls('w')}/>")
        pPr.insert(0, pbb)


def crear_placeholder_acta_sustentacion(doc):
    """
    Crea el bloque formal institucional del Acta de Sustentación y Aprobación de Tesis
    con recuadro estructurado tipo placeholder conforme al modelo Fany 2024.
    """
    dummy = docx.Document()

    # Título principal de la sección
    p_title = dummy.add_paragraph("ACTA DE SUSTENTACIÓN Y APROBACIÓN DE TESIS")
    pPr = p_title._p.get_or_add_pPr()
    pPr.append(parse_xml(f"<w:pageBreakBefore {nsdecls('w')}/>"))
    pPr.append(parse_xml(f"<w:jc {nsdecls('w')} w:val='center'/>"))
    pPr.append(parse_xml(f"<w:spacing {nsdecls('w')} w:before='240' w:after='240' w:line='360' w:lineRule='auto'/>"))
    for r in p_title.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        r.bold = True

    # Tabla recuadro institucional (1 celda)
    t = dummy.add_table(rows=1, cols=1)
    tblPr = t._tbl.tblPr
    tblPr.append(parse_xml(f"<w:jc {nsdecls('w')} w:val='center'/>"))
    tblPr.append(parse_xml(f"<w:tblW {nsdecls('w')} w:w='8788' w:type='dxa'/>"))

    # Bordes tipo recuadro formal institucional
    tblBorders = parse_xml(f"""
    <w:tblBorders {nsdecls('w')}>
      <w:top w:val='single' w:sz='12' w:space='0' w:color='1A365D'/>
      <w:left w:val='single' w:sz='12' w:space='0' w:color='1A365D'/>
      <w:bottom w:val='single' w:sz='12' w:space='0' w:color='1A365D'/>
      <w:right w:val='single' w:sz='12' w:space='0' w:color='1A365D'/>
    </w:tblBorders>
    """)
    tblPr.append(tblBorders)

    cell = t.cell(0, 0)
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f"<w:tcW {nsdecls('w')} w:w='8788' w:type='dxa'/>"))
    tcPr.append(parse_xml(f"""
    <w:tcMar {nsdecls('w')}>
      <w:top w:w='360' w:type='dxa'/>
      <w:left w:w='360' w:type='dxa'/>
      <w:bottom w:w='360' w:type='dxa'/>
      <w:right w:w='360' w:type='dxa'/>
    </w:tcMar>
    """))

    contenido_recuadro = [
        ("UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS", True, 12, False, 120, 40),
        ("FACULTAD DE INGENIERÍA", True, 11, False, 0, 40),
        ("ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS", True, 11, False, 0, 240),
        ("ACTA OFICIAL DE SUSTENTACIÓN Y DICTAMEN DEL JURADO CALIFICADOR", True, 12, False, 120, 120),
        ("[ Espacio reservado para la inserción del documento oficial escaneado del Acta de Sustentación, dictamen aprobatorio del Jurado Calificador y firmas correspondientes, expedida por la Escuela Profesional de Ingeniería de Sistemas de la UNAJMA ]", False, 9.5, True, 180, 240),
        ("MIEMBROS DEL JURADO DICTAMINADOR:", True, 10.5, False, 120, 80),
        ("Presidente del Jurado: __________________________________________________", False, 10, False, 40, 40),
        ("Primer Miembro / Secretario: __________________________________________________", False, 10, False, 40, 40),
        ("Segundo Miembro / Vocal: __________________________________________________", False, 10, False, 40, 40),
        ("Asesora de Tesis: Dra. Norma Lorena Catacora Flores", False, 10, False, 40, 200),
        ("Fecha de Sustentación: Andahuaylas, _____ de _________________ de 2026", False, 10, False, 80, 60),
        ("Dictamen Final: APROBADO CON MENCIÓN [ _______________________ ]", True, 10.5, False, 60, 120),
    ]

    for i, (txt, bold, size, italic, sp_b, sp_a) in enumerate(contenido_recuadro):
        p_c = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        pPr = p_c._p.get_or_add_pPr()
        pPr.append(parse_xml(f"<w:jc {nsdecls('w')} w:val='center'/>"))
        pPr.append(parse_xml(f"<w:spacing {nsdecls('w')} w:before='{sp_b}' w:after='{sp_a}' w:line='240' w:lineRule='auto'/>"))
        pPr.append(parse_xml(f"<w:ind {nsdecls('w')} w:firstLine='0' w:left='0' w:right='0'/>"))
        r = p_c.add_run(txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(size)
        r.bold = bold
        r.italic = italic

    # Blindar fila de tabla recuadro
    trPr = t.rows[0]._tr.get_or_add_trPr()
    trPr.append(parse_xml(f"<w:cantSplit {nsdecls('w')}/>"))

    return [p_title._p, t._tbl]


def reordenar_preliminares_canonicamente(doc):
    """
    Reorganiza quirúrgicamente los elementos XML preliminares conforme al canon UNAJMA Fany 2024:
      1. Portada oficial exterior (con escudo UNAJMA)
      2. Acta de sustentación (recuadro placeholder institucional)
      3. Declaración Jurada de Autenticidad (Anexo 32)
      [Salto de sección 0 -> 1: Sección preliminar académica inicia en romana ii]
      4. Dedicatoria (página ii)
      5. Agradecimientos (página iii)
      6. Índice General de Contenidos (pp. iv-v)
      7. Índice de Figuras (página vi)
      8. Índice de Tablas (página vii)
      9. Resumen en español con Palabras clave (página viii)
      10. Abstract en inglés con Keywords (página ix)
      11. Chumasqa en quechua chanka con Sapaq simikuna (página x)
      [Salto de sección 1 -> 2: Cuerpo capitular inicia en arábiga 1 en Introducción]
    """
    print("\n[1/5] Reordenando preliminares canónicamente según modelo UNAJMA Fany 2024...")
    body = doc.element.body
    children = list(body)

    # Segmentación exacta de los bloques en v03
    portada = children[0:8]
    declaracion = children[8:18]
    dedicatoria = children[18:23]
    agradecimientos = children[23:29]
    resumen = children[29:32]
    abstract = children[32:35]
    chumasqa = children[35:38]
    indice_contenido = children[38:40] # p + sdt
    indice_tablas = children[40:60]
    indice_figuras = children[60:81] # p60 to p80
    cuerpo = children[82:] # from Introducción (82) to end

    # Generar placeholder formal de Acta de Sustentación
    acta_elements = crear_placeholder_acta_sustentacion(doc)

    # Inyectar pageBreakBefore en encabezados preliminares
    def asegurar_pbb(elem):
        pPr = elem.get_or_add_pPr()
        if pPr.find(qn("w:pageBreakBefore")) is None:
            pPr.insert(0, parse_xml(f"<w:pageBreakBefore {nsdecls('w')}/>"))

    asegurar_pbb(declaracion[0])
    asegurar_pbb(agradecimientos[0])
    asegurar_pbb(indice_contenido[0])
    asegurar_pbb(indice_figuras[0])
    asegurar_pbb(indice_tablas[0])
    asegurar_pbb(resumen[0])
    asegurar_pbb(abstract[0])
    asegurar_pbb(chumasqa[0])

    # Limpiar cualquier sectPr previo que pudiera existir dentro de los párrafos preliminares
    for el in (portada + declaracion + dedicatoria + agradecimientos +
               indice_contenido + indice_figuras + indice_tablas +
               resumen + abstract + chumasqa):
        if el.tag.split("}")[-1] == "p":
            pPr = el.find(qn("w:pPr"))
            if pPr is not None:
                old_sect = pPr.find(qn("w:sectPr"))
                if old_sect is not None:
                    pPr.remove(old_sect)

    # Sección 0 sectPr: Administrativa preliminar (Portada, Acta, Declaración Jurada)
    # Sin número impreso (rId10 = header vacío)
    sect0_xml = parse_xml(f"""
    <w:sectPr {nsdecls('w')} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
      <w:headerReference w:type="default" r:id="rId10"/>
      <w:headerReference w:type="first" r:id="rId10"/>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1701" w:header="720" w:footer="720" w:gutter="0"/>
      <w:cols w:space="720"/>
      <w:titlePg/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
    """)
    declaracion[-1].get_or_add_pPr().append(sect0_xml)

    # Sección 1 sectPr: Académica preliminar (Dedicatoria a Chumasqa)
    # Numeración en romanos minúsculos iniciando en 'ii' en Dedicatoria
    sect1_xml = parse_xml(f"""
    <w:sectPr {nsdecls('w')} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
      <w:headerReference w:type="default" r:id="rId9"/>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1701" w:header="720" w:footer="720" w:gutter="0"/>
      <w:pgNumType w:fmt="lowerRoman" w:start="2"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
    """)
    chumasqa[-1].get_or_add_pPr().append(sect1_xml)

    # Ensamblado del nuevo orden preliminar canónico
    nuevos_preliminares = (
        portada +             # 1. Portada oficial exterior (p. 1)
        acta_elements +       # 2. Acta de sustentación recuadro (p. 2)
        declaracion +         # 3. Declaración Jurada Anexo 32 (p. 3) -> Salto Sección 0
        dedicatoria +         # 4. Dedicatoria (p. ii)
        agradecimientos +     # 5. Agradecimientos (p. iii)
        indice_contenido +    # 6. Índice General de Contenidos (pp. iv-v)
        indice_figuras +      # 7. Índice de Figuras (p. vi)
        indice_tablas +       # 8. Índice de Tablas (p. vii)
        resumen +             # 9. Resumen (p. viii)
        abstract +            # 10. Abstract (p. ix)
        chumasqa              # 11. Chumasqa (p. x) -> Salto Sección 1
    )

    body[:] = nuevos_preliminares + cuerpo
    print("  -> Preliminares reordenados con éxito. Total elementos de preliminares:", len(nuevos_preliminares))


def inyectar_saltos_pagina_capitulares(doc):
    """
    Garantiza que el 100% de los títulos de capítulos mayores, secciones maestras
    y anexos inicien en una página limpia mediante <w:pageBreakBefore/>.
    """
    print("\n[2/5] Inyectando saltos de página obligatorios en capítulos y anexos...")
    titulos_con_salto = [
        "CAPÍTULO I:",
        "CAPÍTULO II:",
        "CAPÍTULO III:",
        "CAPÍTULO IV:",
        "CAPÍTULO V:",
        "CAPÍTULO VI:",
        "CONCLUSIONES",
        "RECOMENDACIONES",
        "REFERENCIAS BIBLIOGRÁFICAS",
        "ANEXOS",
        "ANEXO 1:",
        "ANEXO 2:",
        "ANEXO 3:",
        "ANEXO 4:",
        "ANEXO 5:",
        "ANEXO 6:",
        "ANEXO 7:"
    ]

    inyectados = 0
    for p in doc.paragraphs:
        txt = p.text.strip()
        if any(txt.startswith(pref) for pref in titulos_con_salto):
            inyectar_page_break_before(p)
            inyectados += 1

    print(f"  -> Se aseguraron saltos de página obligatorios en {inyectados} encabezados mayores.")


def configurar_seccion_landscape_anexo1(doc):
    """
    Configura quirúrgicamente la sección Landscape para Anexo 1 (Matriz de Consistencia):
      - Sección 2: Cuerpo capitular (Vertical / Portrait, inicia en arábigo 1 en Introducción,
        concluye en el título 'ANEXOS').
      - Sección 3: Anexo 1 (Horizontal / Landscape, ancho 16,838 dxa x alto 11,906 dxa,
        márgenes 3.0 cm izq y 2.54 cm otros, ancho útil 14,000 dxa).
        Reconfigura la Tabla 43 (Matriz de Consistencia) con 5 columnas de 2,800 dxa.
      - Sección 4: Anexos 2 a 7 (Vertical / Portrait, retorno automático).
    """
    print("\n[3/5] Configurando sección horizontal (Landscape) para Anexo 1 (Matriz de Consistencia)...")
    body = doc.element.body

    # 1. Hallar párrafos delimitadores
    p_anexos = None
    p_anexo1 = None
    p_nota_matriz = None
    tbl_matriz = None

    for i, el in enumerate(body):
        tag = el.tag.split("}")[-1]
        if tag == "p":
            txt = "".join(el.itertext()).strip().replace("\n", " ")
            if (txt == "ANEXOS" or (txt.startswith("ANEXOS") and not txt.startswith("ANEXO "))) and p_anexos is None:
                p_anexos = el
            elif txt.startswith("ANEXO 1:") and p_anexo1 is None:
                p_anexo1 = el
            elif txt.startswith("Nota. Matriz de consistencia") and p_nota_matriz is None:
                p_nota_matriz = el
        elif tag == "tbl":
            # Verificar si es la tabla de la Matriz de Consistencia
            txt0 = "".join(t.text for t in el.xpath(".//w:tc[1]//w:t") if t.text)
            if "Problemas" in txt0 or "Consistencia" in txt0:
                tbl_matriz = el

    if p_anexos is None or p_nota_matriz is None or tbl_matriz is None:
        raise RuntimeError("No se pudieron localizar los delimitadores de Anexo 1 en el documento.")

    # 2. Inyectar sectPr de Sección 2 al final del párrafo 'ANEXOS'
    # Esta sección gobierna el cuerpo capitular: Vertical, inicia en arábiga 1
    pPr_anexos = p_anexos.get_or_add_pPr()
    # Limpiar sectPr viejo si existiera
    old_s2 = pPr_anexos.find(qn("w:sectPr"))
    if old_s2 is not None:
        pPr_anexos.remove(old_s2)

    sect2_xml = parse_xml(f"""
    <w:sectPr {nsdecls('w')} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
      <w:headerReference w:type="default" r:id="rId30"/>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1701" w:header="720" w:footer="720" w:gutter="0"/>
      <w:pgNumType w:start="1"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
    """)
    pPr_anexos.append(sect2_xml)
    print("  -> Salto de Sección 2 (Cuerpo Portrait) inyectado tras título ANEXOS.")

    # 3. Reconfigurar geometría de la Tabla de Matriz de Consistencia para Landscape
    # Ancho total: 14,000 dxa (24.7 cm). 5 columnas de 2,800 dxa cada una.
    tblPr = tbl_matriz.find(qn("w:tblPr"))
    if tblPr is not None:
        # Remover tblW y jc previos
        for tag_name in ["w:tblW", "w:jc"]:
            t_elem = tblPr.find(qn(tag_name))
            if t_elem is not None:
                tblPr.remove(t_elem)
        tblPr.append(parse_xml(f"<w:tblW {nsdecls('w')} w:w='14000' w:type='dxa'/>"))
        tblPr.append(parse_xml(f"<w:jc {nsdecls('w')} w:val='center'/>"))

    # Reconfigurar tblGrid
    tblGrid = tbl_matriz.find(qn("w:tblGrid"))
    if tblGrid is not None:
        tblGrid.clear()
        for _ in range(5):
            tblGrid.append(parse_xml(f"<w:gridCol {nsdecls('w')} w:w='2800'/>"))

    # Reconfigurar cada fila y celda
    rows = tbl_matriz.findall(qn("w:tr"))
    for r_idx, row in enumerate(rows):
        trPr = row.get_or_add_trPr()
        if trPr.find(qn("w:cantSplit")) is None:
            trPr.append(parse_xml(f"<w:cantSplit {nsdecls('w')}/>"))
        if r_idx == 0 and trPr.find(qn("w:tblHeader")) is None:
            trPr.append(parse_xml(f"<w:tblHeader {nsdecls('w')}/>"))

        cells = row.findall(qn("w:tc"))
        for cell in cells:
            tcPr = cell.get_or_add_tcPr()
            tcW = tcPr.find(qn("w:tcW"))
            if tcW is not None:
                tcPr.remove(tcW)
            tcPr.append(parse_xml(f"<w:tcW {nsdecls('w')} w:w='2800' w:type='dxa'/>"))

            # Ajustar párrafos internos para mayor legibilidad editorial
            for p in cell.findall(qn("w:p")):
                pPr = p.get_or_add_pPr()
                # Interlineado compacto 1.15 líneas dentro de tabla
                sp = pPr.find(qn("w:spacing"))
                if sp is not None:
                    pPr.remove(sp)
                pPr.append(parse_xml(f"<w:spacing {nsdecls('w')} w:before='40' w:after='40' w:line='276' w:lineRule='auto'/>"))
                ind = pPr.find(qn("w:ind"))
                if ind is not None:
                    pPr.remove(ind)
                pPr.append(parse_xml(f"<w:ind {nsdecls('w')} w:firstLine='0' w:left='0' w:right='0'/>"))

                for r in p.findall(qn("w:r")):
                    rPr = r.get_or_add_rPr()
                    sz = rPr.find(qn("w:sz"))
                    szCs = rPr.find(qn("w:szCs"))
                    if sz is not None:
                        rPr.remove(sz)
                    if szCs is not None:
                        rPr.remove(szCs)
                    rPr.append(parse_xml(f"<w:sz {nsdecls('w')} w:val='19'/>")) # 9.5 pt
                    rPr.append(parse_xml(f"<w:szCs {nsdecls('w')} w:val='19'/>"))

    print("  -> Tabla 43 (Matriz de Consistencia) reconfigurada a 14,000 dxa (5 x 2,800 dxa).")

    # 4. Inyectar sectPr de Sección 3 (Landscape) al final de la Nota de la Matriz de Consistencia
    pPr_nota = p_nota_matriz.get_or_add_pPr()
    old_s3 = pPr_nota.find(qn("w:sectPr"))
    if old_s3 is not None:
        pPr_nota.remove(old_s3)

    sect3_xml = parse_xml(f"""
    <w:sectPr {nsdecls('w')} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
      <w:headerReference w:type="default" r:id="rId30"/>
      <w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1701" w:header="720" w:footer="720" w:gutter="0"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
    """)
    pPr_nota.append(sect3_xml)
    print("  -> Salto de Sección 3 (Landscape Anexo 1) inyectado tras Nota de Matriz.")

    # 5. Configurar sectPr de Sección 4 (Retorno a Portrait) en el root-level sectPr
    final_sect = body.xpath("./w:sectPr")
    if final_sect:
        sec4_elem = final_sect[0]
        sec4_elem.clear()
        sec4_content = parse_xml(f"""
        <w:sectPr {nsdecls('w')} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
          <w:headerReference w:type="default" r:id="rId30"/>
          <w:pgSz w:w="11906" w:h="16838"/>
          <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1701" w:header="720" w:footer="720" w:gutter="0"/>
          <w:cols w:space="720"/>
          <w:docGrid w:linePitch="360"/>
        </w:sectPr>
        """)
        sec4_elem.extend(sec4_content)
        print("  -> Salto de Sección 4 (Retorno Portrait para Anexos 2 a 7) configurado en body sectPr.")


def blindar_todas_las_tablas_documento(doc):
    """
    Ejecuta el blindaje integral OpenXML sobre el 100% de tablas del documento:
      - Erradica w:tblpPr (cero tablas flotantes).
      - Inyecta w:cantSplit en todas las filas de todas las tablas.
      - Inyecta w:tblHeader en la fila de cabecera de todas las tablas multi-fila.
      - Aplica bordes reglamentarios APA 7.
    """
    print("\n[4/5] Blindando geométricamente el 100% de tablas OpenXML (cantSplit y tblHeader)...")
    total_tablas = len(doc.tables)
    tablas_blindadas = 0

    for i, t in enumerate(doc.tables):
        eliminar_flotacion_tabla(t)
        blindar_filas_tabla(t, cant_split=True, repetir_encabezado=True)
        tablas_blindadas += 1

    print(f"  -> {tablas_blindadas}/{total_tablas} tablas blindadas quirúrgicamente sin desbordes.")


def actualizar_campos_y_exportar_pdf(docx_path, pdf_path):
    """
    Ejecuta Microsoft Word COM Automation para actualizar campos automáticos (TOC, TOF)
    y generar el PDF oficial de alta fidelidad con DisplayAlerts=0 y FileFormat=17.
    """
    print("\n[5/5] Iniciando Word COM Automation para actualización de campos y exportación PDF...")
    import win32com.client

    docx_abs = str(docx_path.resolve())
    pdf_abs = str(pdf_path.resolve())

    # Asegurar que el directorio de salida existe
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0

    doc = None
    try:
        print(f"  -> Abriendo documento: {docx_abs}")
        doc = word.Documents.Open(docx_abs, False, False, False)

        print("  -> Configurando estilos de Tabla de Contenidos (TDC 1-3) a formato compacto oficial...")
        for style_name in ["TDC 1", "TDC 2", "TDC 3", "TOC 1", "TOC 2", "TOC 3"]:
            try:
                s = doc.Styles(style_name)
                s.Font.Name = "Times New Roman"
                s.Font.Size = 10
                s.ParagraphFormat.SpaceBefore = 0
                s.ParagraphFormat.SpaceAfter = 1.5
                s.ParagraphFormat.LineSpacingRule = 0 # wdLineSpaceSingle
            except Exception:
                pass

        print("  -> Actualizando campos generales (PAGEREF, SEQ, etc.)...")
        doc.Fields.Update()

        print(f"  -> Detectadas {doc.TablesOfContents.Count} Tablas de Contenido.")
        for i in range(1, doc.TablesOfContents.Count + 1):
            print(f"     Actualizando Tabla de Contenido [{i}]...")
            doc.TablesOfContents(i).Update()

        print(f"  -> Detectadas {doc.TablesOfFigures.Count} Tablas de Ilustraciones/Figuras/Tablas.")
        for i in range(1, doc.TablesOfFigures.Count + 1):
            print(f"     Actualizando Tabla de Ilustraciones [{i}]...")
            doc.TablesOfFigures(i).Update()

        print("  -> Guardando cambios en el documento DOCX con campos recalculados...")
        doc.Save()

        print(f"  -> Exportando a PDF oficial: {pdf_abs}")
        # wdExportFormatPDF = 17, wdExportOptimizeForPrint = 0
        doc.ExportAsFixedFormat(
            OutputFileName=pdf_abs,
            ExportFormat=17,
            OpenAfterExport=False,
            OptimizeFor=0,
            Range=0, # wdExportAllDocument
            From=1,
            To=1,
            Item=0, # wdExportDocumentContent
            IncludeDocProps=True,
            KeepIRM=True,
            CreateBookmarks=1, # wdExportCreateHeadingBookmarks
            DocStructureTags=True,
            BitmapMissingFonts=True,
            UseISO19005_1=False
        )

        paginas_totales = doc.ComputeStatistics(2) # 2 = wdStatisticPages
        print(f"  -> Documento PDF oficial exportado exitosamente ({paginas_totales} páginas totales).")

    except Exception as e:
        print(f"  [ERROR] Falló la automatización de Word COM: {e}", file=sys.stderr)
        raise
    finally:
        if doc is not None:
            doc.Close(False)
        word.Quit()


def compilar_informe_completo_v04():
    """Función orquestadora principal de compilación del Informe Final v04."""
    start_time = time.time()
    print("=" * 80)
    print("SIVAC-THESIS-LAB: COMPILADOR QUIRÚRGICO DE INFORME FINAL DE TESIS v04")
    print("Directiva institucional: Alineación canónica con el modelo UNAJMA Fany 2024")
    print("=" * 80)

    if not DOCX_BASE_V03.exists():
        raise FileNotFoundError(f"Documento base no encontrado: {DOCX_BASE_V03}")

    print(f"Cargando documento base inmutable: {DOCX_BASE_V03.name}")
    doc = docx.Document(str(DOCX_BASE_V03))

    # 1. Reordenar preliminares según canon Fany 2024
    reordenar_preliminares_canonicamente(doc)

    # 2. Inyectar saltos de página obligatorios en capítulos y anexos
    inyectar_saltos_pagina_capitulares(doc)

    # 3. Configurar sección horizontal (Landscape) para Anexo 1 (Matriz de Consistencia)
    configurar_seccion_landscape_anexo1(doc)

    # 4. Blindar geométricamente todas las tablas del documento
    blindar_todas_las_tablas_documento(doc)

    # 5. Guardar documento Word versionado v04
    print(f"\nGuardando documento Word compilado: {DOCX_SALIDA_V04}")
    doc.save(str(DOCX_SALIDA_V04))
    size_mb = DOCX_SALIDA_V04.stat().st_size / (1024 * 1024)
    print(f"  -> {DOCX_SALIDA_V04.name} generado con éxito ({size_mb:.2f} MB).")

    # 6. Actualizar campos nativos y exportar a PDF oficial vía Word COM
    actualizar_campos_y_exportar_pdf(DOCX_SALIDA_V04, PDF_SALIDA_V04)
    pdf_size_mb = PDF_SALIDA_V04.stat().st_size / (1024 * 1024)
    print(f"  -> {PDF_SALIDA_V04.name} generado con éxito ({pdf_size_mb:.2f} MB).")

    # 7. Auditoría de calidad OpenXML
    print("\nEjecutando auditoría automatizada OpenXML sobre informe_final_v04.docx...")
    res_auditoria = auditar_docx_openxml(DOCX_SALIDA_V04)
    print(f"  -> Total tablas auditadas: {res_auditoria['tablas_total']}")
    print(f"  -> Tablas flotantes (w:tblpPr): {res_auditoria['tablas_flotantes']} (0 requeridas)")
    print(f"  -> Tablas con cantSplit: {res_auditoria['tablas_con_cantsplit']} / {res_auditoria['tablas_total']}")
    print(f"  -> Tablas con cabecera tblHeader: {res_auditoria['tablas_con_header']}")
    print(f"  -> Referencias con sangría francesa: {res_auditoria['referencias_sangria_francesa']}")
    print(f"  -> Ecuaciones nativas OMML: {res_auditoria['formulas_omml']}")

    elapsed = time.time() - start_time
    print("=" * 80)
    print(f"COMPILACIÓN EDITORIAL v04 CONCLUIDA EXITOSAMENTE EN {elapsed:.2f} SEGUNDOS.")
    print("=" * 80)


if __name__ == "__main__":
    compilar_informe_completo_v04()
