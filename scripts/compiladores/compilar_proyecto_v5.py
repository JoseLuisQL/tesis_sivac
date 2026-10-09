#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - COMPILADOR QUIRÚRGICO DE PROYECTO DE TESIS V5.0
================================================================================
Universidad Nacional José María Arguedas (UNAJMA)
Escuela Profesional de Ingeniería de Sistemas (EPIS)

Genera:
  salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V5_NORMALIZADO.docx

Insumo maestro:
  salidas/documentos/CAPITULO_II_MARCO_TEORICO_CONSOLIDADO.md

Modificaciones quirúrgicas integradas:
  1. Reemplazo integral y armónico del Capítulo II (Marco Teórico):
     - Párrafo de encuadre epistemológico del capítulo.
     - 2.1 Antecedentes de investigación:
       * Párrafo introductorio metodológico de la revisión sistemática.
       * 2.1.1 Antecedentes a nivel internacional: 6 estudios completos
         (Shen et al., 2024; Dang et al., 2024; Kigenza et al., 2023;
          Balón Morejón, 2023; Ergetie et al., 2023; Wasswa et al., 2023).
       * 2.1.2 Antecedentes a nivel nacional: 4 investigaciones completas
         (Astuhuaman & Baltazar, 2024; Mego Navarro, 2021;
          Garcia & Calderón, 2023; Champi Velásquez, 2023).
     - 2.2 Bases teóricas (consolidado en 2 ejes temáticos canónicos):
       * 2.2.1 Sistema web (Arquitectura, XP, ISO/IEC 25010:2023).
       * 2.2.2 Gestión de movimientos de vacunas (Cadena de frío/MINSA, Kardex,
         Dimensión 1 Oportunidad, Dimensión 2 Consistencia, Dimensión 3 TAM).
       * 4 tablas nativas APA 7 de tres líneas (8788 dxa) y 3 figuras esquemáticas.
     - 2.3 Marco conceptual: 16 conceptos de la A a la Z en formato continuo normal.
  2. Sección de Referencias Bibliográficas:
     - 27 referencias biunívocas 1:1 verificadas con Zotero, estilo Bibliografa,
       sangría francesa 1.27 cm e interlineado 1.5.
  3. Preservación estricta de imágenes en alta resolución (rId14, rId16, rId15).
  4. Cero párrafos vacíos y cumplimiento total de parámetros OpenXML UNAJMA.
================================================================================
"""

import os
import sys
import copy
import re
from pathlib import Path
import docx
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from xml.sax.saxutils import escape

# Ajustar sys.path para importar scripts/utilidades/docx_quirurgico.py
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utilidades.docx_quirurgico import (
    FUENTE_POR_DEFECTO,
    LINE_SPACING_1_5_DXA,
    LINE_SPACING_1_0_DXA,
    SANGRIA_PRIMERA_LINEA_DXA,
    SANGRIA_FRANCESA_DXA,
    FONT_SIZE_BODY_PT,
    FONT_SIZE_TABLE_PT,
    FONT_SIZE_NOTE_PT,
    configurar_geometria_tabla,
    aplicar_bordes_apa7,
    blindar_filas_tabla,
    eliminar_flotacion_tabla,
    crear_parrafo_celda
)

DOCX_ORIGEN = str(PROJECT_ROOT / "salidas" / "documentos" / "PROYECTO_TESIS_ACTUALIZADO_V4_NORMALIZADO.docx")
DOCX_DESTINO = str(PROJECT_ROOT / "salidas" / "documentos" / "PROYECTO_TESIS_ACTUALIZADO_V5_NORMALIZADO.docx")
MD_INSUMO = str(PROJECT_ROOT / "salidas" / "documentos" / "CAPITULO_II_MARCO_TEORICO_CONSOLIDADO.md")

def parse_inline_runs(md_text):
    """Convierte **negrita**, *cursiva* y texto plano en tuplas (texto, bold, italic)."""
    parts = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*)', md_text)
    runs = []
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            runs.append((part[2:-2], True, False))
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            runs.append((part[1:-1], False, True))
        else:
            runs.append((part, False, False))
    return runs

def crear_parrafo_runs(runs_data, sangria=True, align="both"):
    """Crea un párrafo con múltiples runs de texto con formato APA 7."""
    pPr_xml = f'''<w:pPr {nsdecls("w")}>
        <w:spacing w:line="{LINE_SPACING_1_5_DXA}" w:lineRule="auto" w:before="0" w:after="0"/>
        <w:ind w:firstLine="{SANGRIA_PRIMERA_LINEA_DXA if sangria else 0}" w:left="0" w:right="0"/>
        <w:jc w:val="{align}"/>
    </w:pPr>'''
    p = parse_xml(f'<w:p {nsdecls("w")}>{pPr_xml}</w:p>')

    for txt, negrita, cursiva in runs_data:
        r = parse_xml(f'''<w:r {nsdecls("w")}>
            <w:rPr>
                <w:rFonts w:ascii="{FUENTE_POR_DEFECTO}" w:hAnsi="{FUENTE_POR_DEFECTO}" w:eastAsia="{FUENTE_POR_DEFECTO}" w:cs="{FUENTE_POR_DEFECTO}"/>
                <w:b w:val="{'1' if negrita else '0'}"/>
                <w:i w:val="{'1' if cursiva else '0'}"/>
                <w:sz w:val="24"/>
                <w:szCs w:val="24"/>
            </w:rPr>
            <w:t xml:space="preserve">{escape(txt)}</w:t>
        </w:r>''')
        p.append(r)
    return p

def crear_parrafo_subtitulo(texto):
    """Crea un subtítulo temático de sección en negrita (sin numeración decimal, sin sangría)."""
    pPr_xml = f'''<w:pPr {nsdecls("w")}>
        <w:spacing w:line="{LINE_SPACING_1_5_DXA}" w:lineRule="auto" w:before="240" w:after="120"/>
        <w:ind w:firstLine="0" w:left="0" w:right="0"/>
        <w:jc w:val="left"/>
        <w:keepNext/>
    </w:pPr>'''
    p = parse_xml(f'<w:p {nsdecls("w")}>{pPr_xml}</w:p>')
    r = parse_xml(f'''<w:r {nsdecls("w")}>
        <w:rPr>
            <w:rFonts w:ascii="{FUENTE_POR_DEFECTO}" w:hAnsi="{FUENTE_POR_DEFECTO}"/>
            <w:b w:val="1"/>
            <w:i w:val="0"/>
            <w:sz w:val="24"/>
            <w:szCs w:val="24"/>
        </w:rPr>
        <w:t xml:space="preserve">{escape(texto)}</w:t>
    </w:r>''')
    p.append(r)
    return p

def crear_parrafo_heading(texto, nivel=2):
    """Crea un encabezado numerado oficial (Ttulo2 o Ttulo3)."""
    pPr_xml = f'''<w:pPr {nsdecls("w")}>
        <w:pStyle w:val="Ttulo{nivel}"/>
        <w:spacing w:line="{LINE_SPACING_1_5_DXA}" w:lineRule="auto" w:before="240" w:after="120"/>
        <w:ind w:firstLine="0" w:left="0" w:right="0"/>
        <w:jc w:val="left"/>
        <w:keepNext/>
    </w:pPr>'''
    p = parse_xml(f'<w:p {nsdecls("w")}>{pPr_xml}</w:p>')
    r = parse_xml(f'''<w:r {nsdecls("w")}>
        <w:rPr>
            <w:rFonts w:ascii="{FUENTE_POR_DEFECTO}" w:hAnsi="{FUENTE_POR_DEFECTO}"/>
            <w:b w:val="1"/>
            <w:i w:val="{'1' if nivel == 3 else '0'}"/>
            <w:sz w:val="24"/>
            <w:szCs w:val="24"/>
        </w:rPr>
        <w:t xml:space="preserve">{escape(texto)}</w:t>
    </w:r>''')
    p.append(r)
    return p

def crear_caption_tabla(numero, titulo):
    """Genera los dos párrafos de caption de una tabla según APA 7."""
    p_num = parse_xml(f'''<w:p {nsdecls("w")}>
        <w:pPr>
            <w:spacing w:line="{LINE_SPACING_1_5_DXA}" w:lineRule="auto" w:before="240" w:after="40"/>
            <w:ind w:firstLine="0" w:left="0" w:right="0"/>
            <w:jc w:val="left"/>
            <w:keepNext/>
        </w:pPr>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="{FUENTE_POR_DEFECTO}" w:hAnsi="{FUENTE_POR_DEFECTO}"/>
                <w:b w:val="1"/>
                <w:sz w:val="24"/>
                <w:szCs w:val="24"/>
            </w:rPr>
            <w:t xml:space="preserve">Tabla {numero}</w:t>
        </w:r>
    </w:p>''')

    p_tit = parse_xml(f'''<w:p {nsdecls("w")}>
        <w:pPr>
            <w:spacing w:line="{LINE_SPACING_1_5_DXA}" w:lineRule="auto" w:before="0" w:after="120"/>
            <w:ind w:firstLine="0" w:left="0" w:right="0"/>
            <w:jc w:val="left"/>
            <w:keepNext/>
        </w:pPr>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="{FUENTE_POR_DEFECTO}" w:hAnsi="{FUENTE_POR_DEFECTO}"/>
                <w:i w:val="1"/>
                <w:sz w:val="24"/>
                <w:szCs w:val="24"/>
            </w:rPr>
            <w:t xml:space="preserve">{escape(titulo)}</w:t>
        </w:r>
    </w:p>''')
    return [p_num, p_tit]

def crear_caption_figura(numero, titulo):
    """Genera los dos párrafos de caption de una figura según APA 7."""
    p_num = parse_xml(f'''<w:p {nsdecls("w")}>
        <w:pPr>
            <w:spacing w:line="{LINE_SPACING_1_5_DXA}" w:lineRule="auto" w:before="240" w:after="40"/>
            <w:ind w:firstLine="0" w:left="0" w:right="0"/>
            <w:jc w:val="left"/>
            <w:keepNext/>
        </w:pPr>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="{FUENTE_POR_DEFECTO}" w:hAnsi="{FUENTE_POR_DEFECTO}"/>
                <w:b w:val="1"/>
                <w:sz w:val="24"/>
                <w:szCs w:val="24"/>
            </w:rPr>
            <w:t xml:space="preserve">Figura {numero}</w:t>
        </w:r>
    </w:p>''')

    p_tit = parse_xml(f'''<w:p {nsdecls("w")}>
        <w:pPr>
            <w:spacing w:line="{LINE_SPACING_1_5_DXA}" w:lineRule="auto" w:before="0" w:after="120"/>
            <w:ind w:firstLine="0" w:left="0" w:right="0"/>
            <w:jc w:val="left"/>
            <w:keepNext/>
        </w:pPr>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="{FUENTE_POR_DEFECTO}" w:hAnsi="{FUENTE_POR_DEFECTO}"/>
                <w:i w:val="1"/>
                <w:sz w:val="24"/>
                <w:szCs w:val="24"/>
            </w:rPr>
            <w:t xml:space="preserve">{escape(titulo)}</w:t>
        </w:r>
    </w:p>''')
    return [p_num, p_tit]

def crear_nota_tabla_figura(nota_texto):
    """Genera un párrafo de nota de tabla o figura con formato APA 7."""
    if nota_texto.startswith("Nota."):
        prefijo = "Nota."
        cuerpo = nota_texto[5:]
    elif nota_texto.startswith("*Nota.*"):
        prefijo = "Nota."
        cuerpo = nota_texto[7:]
    else:
        prefijo = "Nota."
        cuerpo = " " + nota_texto

    p = parse_xml(f'''<w:p {nsdecls("w")}>
        <w:pPr>
            <w:spacing w:line="{LINE_SPACING_1_0_DXA}" w:lineRule="auto" w:before="60" w:after="240"/>
            <w:ind w:firstLine="0" w:left="0" w:right="0"/>
            <w:jc w:val="both"/>
        </w:pPr>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="{FUENTE_POR_DEFECTO}" w:hAnsi="{FUENTE_POR_DEFECTO}"/>
                <w:i w:val="1"/>
                <w:sz w:val="19"/>
                <w:szCs w:val="19"/>
            </w:rPr>
            <w:t xml:space="preserve">{escape(prefijo)}</w:t>
        </w:r>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="{FUENTE_POR_DEFECTO}" w:hAnsi="{FUENTE_POR_DEFECTO}"/>
                <w:sz w:val="19"/>
                <w:szCs w:val="19"/>
            </w:rPr>
            <w:t xml:space="preserve">{escape(cuerpo)}</w:t>
        </w:r>
    </w:p>''')
    return p

def construir_tabla_apa7(doc_context, headers, data_rows, col_widths, align_cols=None):
    """
    Construye una tabla OpenXML con formato estricto APA 7:
    - 3 líneas horizontales
    - Cero líneas verticales
    - tblHeader, cantSplit, márgenes celulares, texto a 10 pt
    """
    tbl = doc_context.add_table(rows=len(data_rows) + 1, cols=len(headers))
    eliminar_flotacion_tabla(tbl)

    total_w = sum(col_widths)
    configurar_geometria_tabla(tbl, total_w, col_widths, align="center")
    aplicar_bordes_apa7(tbl)
    blindar_filas_tabla(tbl)

    # 1. Encabezados
    for c_idx, h_text in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        for p_elem in list(cell._tc.findall(qn('w:p'))):
            cell._tc.remove(p_elem)
        p_cell = crear_parrafo_celda(h_text, bold=True, italic=False, fuente=FUENTE_POR_DEFECTO, font_size_pt=10.0, align="center", line_spacing=LINE_SPACING_1_0_DXA, space_before=20, space_after=20)
        cell._tc.append(p_cell)

    # 2. Filas de datos
    for r_idx, row_data in enumerate(data_rows):
        for c_idx, val in enumerate(row_data):
            cell = tbl.cell(r_idx + 1, c_idx)
            for p_elem in list(cell._tc.findall(qn('w:p'))):
                cell._tc.remove(p_elem)

            align = "left"
            if align_cols and c_idx < len(align_cols):
                align = align_cols[c_idx]

            p_cell = crear_parrafo_celda(val, bold=False, italic=False, fuente=FUENTE_POR_DEFECTO, font_size_pt=10.0, align=align, line_spacing=LINE_SPACING_1_0_DXA, space_before=20, space_after=20)
            cell._tc.append(p_cell)

    tbl_elem = tbl._tbl
    doc_context._body._element.remove(tbl_elem)
    return tbl_elem

def crear_parrafo_referencia(runs_data):
    """Genera un elemento <w:p> de referencia bibliográfica con sangría francesa APA 7."""
    pPr_xml = f'''<w:pPr {nsdecls("w")}>
        <w:pStyle w:val="Bibliografa"/>
        <w:spacing w:line="{LINE_SPACING_1_5_DXA}" w:lineRule="auto" w:before="0" w:after="120"/>
        <w:ind w:left="{SANGRIA_FRANCESA_DXA}" w:hanging="{SANGRIA_FRANCESA_DXA}" w:right="0"/>
        <w:jc w:val="both"/>
    </w:pPr>'''
    p = parse_xml(f'<w:p {nsdecls("w")}>{pPr_xml}</w:p>')

    for txt, negrita, cursiva in runs_data:
        r = parse_xml(f'''<w:r {nsdecls("w")}>
            <w:rPr>
                <w:rFonts w:ascii="{FUENTE_POR_DEFECTO}" w:hAnsi="{FUENTE_POR_DEFECTO}" w:eastAsia="{FUENTE_POR_DEFECTO}" w:cs="{FUENTE_POR_DEFECTO}"/>
                <w:b w:val="{'1' if negrita else '0'}"/>
                <w:i w:val="{'1' if cursiva else '0'}"/>
                <w:sz w:val="24"/>
                <w:szCs w:val="24"/>
            </w:rPr>
            <w:t xml:space="preserve">{escape(txt)}</w:t>
        </w:r>''')
        p.append(r)
    return p

def centrar_parrafo_drawing(p_elem):
    """Asegura que el párrafo clonado con <w:drawing> esté centrado, sin sangría y con keepNext."""
    p_clon = copy.deepcopy(p_elem)
    old_pPr = p_clon.find(qn('w:pPr'))
    if old_pPr is not None:
        p_clon.remove(old_pPr)
    pPr_xml = f'''<w:pPr {nsdecls("w")}>
        <w:spacing w:line="{LINE_SPACING_1_0_DXA}" w:lineRule="auto" w:before="120" w:after="120"/>
        <w:ind w:firstLine="0" w:left="0" w:right="0"/>
        <w:jc w:val="center"/>
        <w:keepNext/>
    </w:pPr>'''
    p_clon.insert(0, parse_xml(pPr_xml))
    return p_clon

def parsear_capitulo2_md(doc, md_path, mapa_figuras):
    """Lee CAPITULO_II_MARCO_TEORICO_CONSOLIDADO.md y genera los elementos OpenXML."""
    lineas = Path(md_path).read_text(encoding="utf-8").splitlines()
    elementos_cap2 = []
    elementos_refs = []
    seccion = None
    en_yaml = False
    en_codigo = False
    figura_actual = None
    i = 0
    n = len(lineas)

    while i < n:
        raw = lineas[i].strip()
        if i == 0 and raw == "---":
            en_yaml = True
            i += 1
            continue
        if en_yaml:
            if raw == "---":
                en_yaml = False
            i += 1
            continue
        if raw.startswith("```"):
            if not en_codigo:
                en_codigo = True
            else:
                en_codigo = False
                if figura_actual and figura_actual in mapa_figuras:
                    elementos_cap2.append(centrar_parrafo_drawing(mapa_figuras[figura_actual]))
                    figura_actual = None
            i += 1
            continue
        if en_codigo:
            i += 1
            continue
        if not raw or raw == "---":
            i += 1
            continue

        # Ignorar título de nivel 1 porque ya existe en el docx base
        if raw == "# CAPÍTULO II. MARCO TEÓRICO":
            seccion = "intro_cap2"
            i += 1
            continue

        if raw == "## 2.1 Antecedentes de investigación":
            seccion = "2.1"
            elementos_cap2.append(crear_parrafo_heading("2.1 Antecedentes de investigación", nivel=2))
            i += 1
            continue

        if raw == "## 2.2 Bases teóricas":
            seccion = "2.2"
            elementos_cap2.append(crear_parrafo_heading("2.2 Bases teóricas", nivel=2))
            i += 1
            continue

        if raw == "## 2.3 Marco conceptual":
            seccion = "2.3"
            elementos_cap2.append(crear_parrafo_heading("2.3 Marco conceptual", nivel=2))
            i += 1
            continue

        if raw == "## Referencias bibliográficas citadas":
            seccion = "refs"
            i += 1
            continue

        if seccion == "refs":
            elementos_refs.append(crear_parrafo_referencia(parse_inline_runs(raw)))
            i += 1
            continue

        # Encabezados de nivel 3 (###)
        if raw.startswith("### "):
            # Estandarizar puntos en numeración decimal según convención del docx base
            sub_titulo = raw[4:].strip()
            if sub_titulo.startswith("2.1.1 "):
                sub_titulo = sub_titulo.replace("2.1.1 ", "2.1.1. ")
            elif sub_titulo.startswith("2.1.2 "):
                sub_titulo = sub_titulo.replace("2.1.2 ", "2.1.2. ")
            elementos_cap2.append(crear_parrafo_heading(sub_titulo, nivel=3))
            i += 1
            continue

        # Detección de Tablas
        m_tab = re.match(r'^\*\*Tabla\s+(\d+)\*\*$', raw)
        if m_tab:
            num_t = m_tab.group(1)
            titulo_t = ""
            if i + 1 < n and lineas[i + 1].strip().startswith("*"):
                titulo_t = lineas[i + 1].strip().strip("*").strip()
                i += 1
            elementos_cap2.extend(crear_caption_tabla(num_t, titulo_t))
            i += 1
            continue

        # Detección de Figuras
        m_fig = re.match(r'^\*\*Figura\s+(\d+)\*\*$', raw)
        if m_fig:
            num_f = int(m_fig.group(1))
            figura_actual = num_f
            titulo_f = ""
            if i + 1 < n and lineas[i + 1].strip().startswith("*"):
                titulo_f = lineas[i + 1].strip().strip("*").strip()
                i += 1
            elementos_cap2.extend(crear_caption_figura(num_f, titulo_f))
            i += 1
            continue

        # Tablas Markdown
        if raw.startswith("|"):
            filas_md = []
            while i < n and lineas[i].strip().startswith("|"):
                fila_str = lineas[i].strip()
                celdas = [c.strip() for c in fila_str.strip("|").split("|")]
                if not all(re.match(r'^[-:\s]+$', c) for c in celdas):
                    filas_md.append(celdas)
                i += 1
            if len(filas_md) >= 2:
                headers = filas_md[0]
                data_rows = filas_md[1:]
                col_widths = [2200, 3294, 3294] if len(headers) == 3 else [2000, 2000, 2788, 2000]
                elementos_cap2.append(construir_tabla_apa7(doc, headers, data_rows, col_widths))
            continue

        # Notas de Tabla / Figura
        if raw.startswith("*Nota.*") or raw.startswith("Nota."):
            elementos_cap2.append(crear_nota_tabla_figura(raw))
            i += 1
            continue

        # Subtítulos temáticos dentro de 2.2
        if seccion == "2.2" and re.match(r'^\*\*[^*]+\*\*$', raw):
            elementos_cap2.append(crear_parrafo_subtitulo(raw[2:-2].strip()))
            i += 1
            continue

        # Listas con viñetas
        if raw.startswith("- "):
            texto_item = "• " + raw[2:].strip()
            elementos_cap2.append(crear_parrafo_runs(parse_inline_runs(texto_item), sangria=True))
            i += 1
            continue

        # Párrafos narrativos estándar
        elementos_cap2.append(crear_parrafo_runs(parse_inline_runs(raw), sangria=True))
        i += 1

    return elementos_cap2, elementos_refs

def texto_plano_elemento(elem):
    return "".join(t.text or "" for t in elem.findall(".//" + qn("w:t"))).strip()

def compilar_v5():
    doc = docx.Document(DOCX_ORIGEN)
    body = doc._body._element

    # 1. Extraer y clonar las 3 figuras de alta resolución
    mapa_rids = {"rId14": 1, "rId16": 2, "rId15": 3}
    mapa_figuras = {}
    ns_a = "{http://schemas.openxmlformats.org/drawingml/2006/main}blip"
    for child in body:
        if child.tag == qn("w:p"):
            for blip in child.findall(".//" + ns_a):
                rid = blip.get(qn("r:embed"))
                if rid in mapa_rids:
                    mapa_figuras[mapa_rids[rid]] = copy.deepcopy(child)

    print(f"Figuras extraídas y resguardadas: {list(mapa_figuras.keys())}")

    # 2. Parsear el archivo maestro Markdown de Capítulo II
    elementos_cap2, elementos_refs = parsear_capitulo2_md(doc, MD_INSUMO, mapa_figuras)
    print(f"Elementos procesados para Capítulo II: {len(elementos_cap2)}")
    print(f"Referencias bibliográficas procesadas: {len(elementos_refs)}")

    # 3. Localizar límites de Capítulo II en el DOCX
    idx_cap2 = None
    idx_cap3 = None
    for idx, child in enumerate(body):
        if child.tag == qn("w:p"):
            txt = texto_plano_elemento(child)
            if "CAPÍTULO II." in txt and "MARCO TEÓRICO" in txt and idx_cap2 is None:
                idx_cap2 = idx
            elif txt.startswith("CAPÍTULO III.") and idx_cap3 is None:
                idx_cap3 = idx

    if idx_cap2 is None or idx_cap3 is None:
        raise RuntimeError(f"Límites de Capítulo II / Capítulo III no hallados: idx_cap2={idx_cap2}, idx_cap3={idx_cap3}")

    print(f"Sustituyendo bloque Capítulo II desde párrafo [{idx_cap2 + 1}] hasta [{idx_cap3}]...")

    # Remover todo el contenido interior del Capítulo II (conservando el encabezado Ttulo1)
    for child in list(body[idx_cap2 + 1:idx_cap3]):
        body.remove(child)

    # Insertar los nuevos elementos estructurados
    for offset, elem in enumerate(elementos_cap2):
        body.insert(idx_cap2 + 1 + offset, elem)

    # 4. Localizar límites de Referencias Bibliográficas
    idx_ref = None
    idx_anexos = None
    for idx, child in enumerate(body):
        if child.tag == qn("w:p"):
            txt = texto_plano_elemento(child)
            if txt == "Referencia Bibliográfica" and idx_ref is None:
                idx_ref = idx
            elif txt == "ANEXOS" and idx_anexos is None:
                idx_anexos = idx

    if idx_ref is None or idx_anexos is None:
        raise RuntimeError(f"Límites de Referencias / ANEXOS no hallados: idx_ref={idx_ref}, idx_anexos={idx_anexos}")

    print(f"Sustituyendo bloque Referencias Bibliográficas desde [{idx_ref + 1}] hasta [{idx_anexos}]...")
    for child in list(body[idx_ref + 1:idx_anexos]):
        body.remove(child)

    for offset, elem in enumerate(elementos_refs):
        body.insert(idx_ref + 1 + offset, elem)

    # 5. Normalizar citas residuales si quedaran en otras secciones
    reemplazos = [
        ("OPS y PATH, s. f.", "OPS y PATH, 2020"),
        ("OPS y PATH (s. f.)", "OPS y PATH (2020)"),
        ("Ndlovu et al., 2021", "Ndlovu et al., 2022"),
        ("Ndlovu et al. (2021)", "Ndlovu et al. (2022)"),
    ]
    for t_elem in body.findall(".//" + qn("w:t")):
        if t_elem.text:
            nuevo = t_elem.text
            for viejo, rep in reemplazos:
                nuevo = nuevo.replace(viejo, rep)
            t_elem.text = nuevo

    # 6. Eliminar párrafos vacíos a partir de CAPÍTULO I
    en_cuerpo = False
    ns_m_omath = "{http://schemas.openxmlformats.org/officeDocument/2006/math}oMath"
    ns_m_omathpara = "{http://schemas.openxmlformats.org/officeDocument/2006/math}oMathPara"
    for child in list(body):
        if child.tag == qn("w:p"):
            txt = texto_plano_elemento(child)
            if txt.startswith("CAPÍTULO I."):
                en_cuerpo = True
            if en_cuerpo and not txt:
                tiene_especial = (
                    child.find(".//" + qn("w:drawing")) is not None
                    or child.find(".//" + ns_m_omath) is not None
                    or child.find(".//" + ns_m_omathpara) is not None
                    or child.find(".//" + qn("w:sectPr")) is not None
                    or child.find(".//" + qn("w:br")) is not None
                )
                if not tiene_especial:
                    body.remove(child)

    doc.save(DOCX_DESTINO)
    print(f"Compilación V5 finalizada con éxito: {DOCX_DESTINO}")

if __name__ == "__main__":
    compilar_v5()
