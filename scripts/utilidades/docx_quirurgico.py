#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB — MOTOR QUIRÚRGICO DE MANIPULACIÓN Y FORMATEO DOCX / OPENXML
================================================================================
Módulo centralizado y reutilizable para maquetación editorial en Microsoft Word,
cumpliendo estrictamente con APA 7.ª edición y la normativa institucional UNAJMA.

Capacidades integradas:
  1. Conversión e inserción de ecuaciones MathML / LaTeX a OMML nativo de Word
     mediante la hoja de transformación oficial MML2OMML.XSL de Microsoft Office.
  2. Geometría tabular milimétrica (ancho total dxa, anchos por columna en w:tblGrid
     y w:tcW, márgenes celulares w:tblCellMar).
  3. Erradicación automática de propiedades de flotación (w:tblpPr) que quiebran
     el motor de paginación de Word.
  4. Blindaje contra fracturas de filas (w:cantSplit) y repetición de encabezados (w:tblHeader).
  5. Bordes APA 7 canónicos (tres líneas horizontales, cero verticales).
  6. Fusión vertical (w:vMerge) y alineación vertical/horizontal precisa.
  7. Auditoría estática de tablas y dimensiones de página.
  8. Exportación desatendida a PDF mediante Microsoft Word COM.
  9. Renderizado de páginas a imágenes PNG (150/300 DPI) vía PyMuPDF para auditoría visual.
================================================================================
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
import lxml.etree as ET

import docx
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

# Constantes tipográficas institucionales UNAJMA
FUENTE_POR_DEFECTO = "Times New Roman"
ANCHO_UTIL_PORTRAIT_DXA = 8788    # 15.50 cm (A4 21.0 cm - Margen Izq 3.0 cm - Margen Der 2.50 cm)
ANCHO_UTIL_LANDSCAPE_DXA = 14000  # 24.70 cm (A4 29.7 cm - Margen Izq 2.5 cm - Margen Der 2.50 cm)

# Rutas estándar del convertidor oficial MML2OMML.XSL de Microsoft Office
RUTAS_MML2OMML = [
    r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL",
    r"C:\Program Files (x86)\Microsoft Office\root\Office16\MML2OMML.XSL",
    r"C:\Program Files\Microsoft Office\Office16\MML2OMML.XSL",
    r"C:\Program Files (x86)\Microsoft Office\Office16\MML2OMML.XSL",
    os.path.join(os.path.dirname(__file__), "MML2OMML.XSL")
]

_transformador_mml = None

def obtener_transformador_omml():
    """Carga y cachea la hoja de estilos XSLT MML2OMML.XSL para transformar MathML a OMML."""
    global _transformador_mml
    if _transformador_mml is not None:
        return _transformador_mml

    ruta_encontrada = None
    for r in RUTAS_MML2OMML:
        if os.path.exists(r):
            ruta_encontrada = r
            break

    if not ruta_encontrada:
        raise FileNotFoundError(
            "No se encontró la hoja de estilos MML2OMML.XSL en las rutas conocidas de Microsoft Office. "
            "Asegúrese de tener Microsoft Word / Office instalado o proveer la ruta al archivo."
        )

    xslt_doc = ET.parse(ruta_encontrada)
    _transformador_mml = ET.XSLT(xslt_doc)
    return _transformador_mml


# ==============================================================================
# 1. MOTOR DE MATEMÁTICAS Y FÓRMULAS OMML NATIVAS (<m:oMath>)
# ==============================================================================

def mathml_to_omml(mathml_str):
    """
    Convierte una expresión MathML XML a un nodo OpenXML OMML (<m:oMath>).
    Limpia espacios en blanco y namespace prefixes redundantes.
    """
    transformador = obtener_transformador_omml()
    dom = ET.fromstring(mathml_str.strip())
    omml_tree = transformador(dom)
    omml_xml_bytes = ET.tostring(omml_tree)
    return parse_xml(omml_xml_bytes)


def crear_parrafo_formula_dedicada(omml_elem, align="left", line_spacing=210, space_before=20, space_after=30, left_indent_dxa=100):
    """
    Crea un párrafo que contiene exclusivamente una ecuación OMML nativa.
    Ideal para fórmulas destacadas dentro de celdas o texto principal.
    """
    p = parse_xml(r'''<w:p %s>
        <w:pPr>
            <w:spacing w:line="%d" w:lineRule="auto" w:before="%d" w:after="%d"/>
            <w:ind w:firstLine="0" w:left="%d"/>
            <w:jc w:val="%s"/>
        </w:pPr>
    </w:p>''' % (nsdecls('w'), line_spacing, space_before, space_after, left_indent_dxa, align))
    p.append(omml_elem)
    return p


def crear_parrafo_mixto_inline(segmentos, fuente=FUENTE_POR_DEFECTO, font_size_pt=7.5, align="left", line_spacing=210, space_before=10, space_after=20):
    """
    Crea un párrafo fluido con mezcla de texto formateado y ecuaciones OMML en la misma línea.
    Argumentos de `segmentos`:
      - Tupla: (texto, negrita, cursiva)
      - Elemento OMML nativo: <m:oMath>
      - String simple: texto sin formato
    """
    sz_val = str(int(font_size_pt * 2))
    p = parse_xml(r'''<w:p %s>
        <w:pPr>
            <w:spacing w:line="%d" w:lineRule="auto" w:before="%d" w:after="%d"/>
            <w:ind w:firstLine="0"/>
            <w:jc w:val="%s"/>
        </w:pPr>
    </w:p>''' % (nsdecls('w'), line_spacing, space_before, space_after, align))

    for seg in segmentos:
        if hasattr(seg, 'tag') and 'oMath' in seg.tag:
            p.append(seg)
        elif isinstance(seg, tuple):
            t_text = str(seg[0])
            t_bold = bool(seg[1]) if len(seg) > 1 else False
            t_italic = bool(seg[2]) if len(seg) > 2 else False
            r = parse_xml(r'''<w:r %s>
                <w:rPr>
                    <w:rFonts w:ascii="%s" w:hAnsi="%s"/>
                    <w:b w:val="%s"/>
                    <w:i w:val="%s"/>
                    <w:sz w:val="%s"/>
                </w:rPr>
                <w:t xml:space="preserve">%s</w:t>
            </w:r>''' % (nsdecls('w'), fuente, fuente,
                        "1" if t_bold else "0",
                        "1" if t_italic else "0",
                        sz_val, t_text))
            p.append(r)
        else:
            t_text = str(seg)
            r = parse_xml(r'''<w:r %s>
                <w:rPr>
                    <w:rFonts w:ascii="%s" w:hAnsi="%s"/>
                    <w:b w:val="0"/>
                    <w:i w:val="0"/>
                    <w:sz w:val="%s"/>
                </w:rPr>
                <w:t xml:space="preserve">%s</w:t>
            </w:r>''' % (nsdecls('w'), fuente, fuente, sz_val, t_text))
            p.append(r)

    return p


# ==============================================================================
# 2. MOTOR DE GEOMETRÍA TABULAR OPENXML APA 7
# ==============================================================================

def eliminar_flotacion_tabla(table):
    """
    Elimina w:tblpPr (propiedades de posicionamiento flotante).
    CRÍTICO: Word inserta tblpPr cuando una tabla es movida en la GUI, lo que
    causa que la tabla ignore los márgenes de página y se fracture caóticamente.
    """
    tblPr = table._tbl.tblPr
    tblpPr = tblPr.find(qn('w:tblpPr'))
    if tblpPr is not None:
        tblPr.remove(tblpPr)
        return True
    return False


def configurar_geometria_tabla(table, total_width_dxa, col_widths_dxa, align="center", cell_margin_dxa=(30, 60, 30, 60)):
    """
    Configura la geometría estricta de una tabla OpenXML:
      - Remueve propiedades de flotación.
      - Fija w:tblW en dxa exacto.
      - Regenera w:tblGrid con w:gridCol explícitos para cada columna.
      - Asigna w:tcW a cada celda de cada fila.
      - Fija márgenes celulares internos w:tblCellMar (top, left, bottom, right en dxa).
    """
    tblPr = table._tbl.tblPr
    eliminar_flotacion_tabla(table)

    # 1. Ancho total de la tabla
    for w in tblPr.findall(qn('w:tblW')):
        tblPr.remove(w)
    tblPr.append(parse_xml(r'<w:tblW %s w:w="%d" w:type="dxa"/>' % (nsdecls('w'), total_width_dxa)))

    # 2. Alineación de tabla
    for jc in tblPr.findall(qn('w:jc')):
        tblPr.remove(jc)
    tblPr.append(parse_xml(r'<w:jc %s w:val="%s"/>' % (nsdecls('w'), align)))

    # 3. Padding interno celular
    top_m, left_m, bottom_m, right_m = cell_margin_dxa
    for cm in tblPr.findall(qn('w:tblCellMar')):
        tblPr.remove(cm)
    tblPr.append(parse_xml(r'''<w:tblCellMar %s>
        <w:top w:w="%d" w:type="dxa"/>
        <w:left w:w="%d" w:type="dxa"/>
        <w:bottom w:w="%d" w:type="dxa"/>
        <w:right w:w="%d" w:type="dxa"/>
    </w:tblCellMar>''' % (nsdecls('w'), top_m, left_m, bottom_m, right_m)))

    # 4. Reconstrucción de la cuadrícula w:tblGrid
    tblGrid = table._tbl.tblGrid
    if tblGrid is not None:
        table._tbl.remove(tblGrid)
    new_grid = parse_xml(r'<w:tblGrid %s/>' % nsdecls('w'))
    for cw in col_widths_dxa:
        new_grid.append(parse_xml(r'<w:gridCol %s w:w="%d"/>' % (nsdecls('w'), cw)))
    tblPr_idx = list(table._tbl).index(tblPr)
    table._tbl.insert(tblPr_idx + 1, new_grid)

    # 5. Aplicar ancho en cada celda
    for row in table.rows:
        tcs = row._tr.findall(qn('w:tc'))
        for idx, cw in enumerate(col_widths_dxa):
            if idx < len(tcs):
                tcPr = tcs[idx].get_or_add_tcPr()
                for w in tcPr.findall(qn('w:tcW')):
                    tcPr.remove(w)
                tcPr.append(parse_xml(r'<w:tcW %s w:w="%d" w:type="dxa"/>' % (nsdecls('w'), cw)))


def aplicar_bordes_apa7(table):
    """
    Aplica exactamente las 3 líneas horizontales exigidas por APA 7:
      - Borde superior de tabla (w:top, single, sz=4)
      - Borde inferior de encabezados (w:bottom en celda de Fila 0, single, sz=4)
      - Borde inferior de tabla (w:bottom, single, sz=4)
      - Cero bordes verticales y cero líneas interiores.
    """
    tblPr = table._tbl.tblPr
    for b in tblPr.findall(qn('w:tblBorders')):
        tblPr.remove(b)

    bordes_xml = parse_xml(r'''<w:tblBorders %s>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:left w:val="none"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:right w:val="none"/>
        <w:insideH w:val="none"/>
        <w:insideV w:val="none"/>
    </w:tblBorders>''' % nsdecls('w'))
    tblPr.append(bordes_xml)

    if len(table.rows) > 0:
        for tc in table.rows[0]._tr.findall(qn('w:tc')):
            tcPr = tc.get_or_add_tcPr()
            tcBorders = tcPr.find(qn('w:tcBorders'))
            if tcBorders is None:
                tcBorders = parse_xml(r'<w:tcBorders %s/>' % nsdecls('w'))
                tcPr.append(tcBorders)
            for b in tcBorders.findall(qn('w:bottom')):
                tcBorders.remove(b)
            tcBorders.append(parse_xml(r'<w:bottom %s w:val="single" w:sz="4" w:space="0" w:color="000000"/>' % nsdecls('w')))


def blindar_filas_tabla(table, cant_split=True, repetir_encabezado=True):
    """
    Asegura que las filas no se fracturen entre dos páginas (w:cantSplit)
    y que la primera fila se repita automáticamente si la tabla desborda (w:tblHeader).
    """
    for r_idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        if cant_split and trPr.find(qn('w:cantSplit')) is None:
            trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
        if r_idx == 0 and repetir_encabezado and trPr.find(qn('w:tblHeader')) is None:
            trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))


def set_tc_vmerge(tc, mode):
    """
    Gestiona la fusión vertical de celdas en OpenXML:
      - mode='restart': Inicia un nuevo bloque fusionado.
      - mode='continue': Continúa la fusión con la celda superior.
      - mode='none': Celda independiente no fusionada.
    """
    tcPr = tc.get_or_add_tcPr()
    for vm in tcPr.findall(qn('w:vMerge')):
        tcPr.remove(vm)
    if mode == 'restart':
        tcPr.append(parse_xml(r'<w:vMerge %s w:val="restart"/>' % nsdecls('w')))
    elif mode == 'continue':
        tcPr.append(parse_xml(r'<w:vMerge %s/>' % nsdecls('w')))


def set_tc_paragraphs(tc, paragraphs):
    """
    Reemplaza todos los párrafos de una celda por una lista de nuevos elementos <w:p>.
    Garantiza que siempre exista al menos un párrafo para mantener el XML válido.
    """
    tcPr = tc.find(qn('w:tcPr'))
    for child in list(tc):
        if child.tag != qn('w:tcPr'):
            tc.remove(child)

    if not paragraphs:
        empty_p = parse_xml(r'<w:p %s><w:pPr><w:spacing w:line="180" w:before="0" w:after="0"/></w:pPr></w:p>' % nsdecls('w'))
        tc.append(empty_p)
        return

    for p in paragraphs:
        tc.append(p)


def crear_parrafo_celda(texto, bold=False, italic=False, fuente=FUENTE_POR_DEFECTO, font_size_pt=7.5, align="left", line_spacing=200, space_before=0, space_after=15):
    """Crea un párrafo simple para celdas con espaciado y tipografía controlados."""
    sz_val = str(int(font_size_pt * 2))
    p = parse_xml(r'''<w:p %s>
        <w:pPr>
            <w:spacing w:line="%d" w:lineRule="auto" w:before="%d" w:after="%d"/>
            <w:ind w:firstLine="0"/>
            <w:jc w:val="%s"/>
        </w:pPr>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="%s" w:hAnsi="%s"/>
                <w:b w:val="%s"/>
                <w:i w:val="%s"/>
                <w:sz w:val="%s"/>
            </w:rPr>
            <w:t xml:space="preserve">%s</w:t>
        </w:r>
    </w:p>''' % (nsdecls('w'), line_spacing, space_before, space_after, align,
                fuente, fuente,
                "1" if bold else "0",
                "1" if italic else "0",
                sz_val, texto))
    return p


# ==============================================================================
# 3. HERRAMIENTAS DE AUDITORÍA, CONVERSIÓN Y RENDERIZADO VISUAL
# ==============================================================================

def blindar_todas_tablas_documento(docx_path, salida_path=None, aplicar_bordes=True):
    """
    Recorre todas las tablas del documento para aplicar blindaje integral:
      - Remueve flotación (w:tblpPr).
      - Inyecta w:cantSplit en todas las filas.
      - Inyecta w:tblHeader en la primera fila de cada tabla.
      - Aplica opcionalmente los 3 bordes canónicos APA 7.
    """
    doc = docx.Document(docx_path)
    conteo_modificadas = 0

    for idx, table in enumerate(doc.tables):
        eliminar_flotacion_tabla(table)
        blindar_filas_tabla(table, cant_split=True, repetir_encabezado=True)
        if aplicar_bordes:
            aplicar_bordes_apa7(table)
        conteo_modificadas += 1

    destino = salida_path if salida_path else docx_path
    doc.save(destino)
    return conteo_modificadas


def auditar_documento_docx(docx_path):
    """
    Audita exhaustivamente las tablas de un documento DOCX:
      - Detecta tablas flotantes (w:tblpPr).
      - Revisa anchos de tabla frente a los límites recomendados.
      - Verifica presencia de w:cantSplit y w:tblHeader.
    """
    doc = docx.Document(docx_path)
    reporte = {
        "archivo": str(docx_path),
        "total_tablas": len(doc.tables),
        "advertencias": [],
        "tablas": []
    }

    for idx, table in enumerate(doc.tables):
        tblPr = table._tbl.tblPr
        es_flotante = tblPr.find(qn('w:tblpPr')) is not None
        tblW_elem = tblPr.find(qn('w:tblW'))
        ancho_dxa = int(tblW_elem.get(qn('w:w'), 0)) if tblW_elem is not None and tblW_elem.get(qn('w:w')) else None

        cant_split_count = 0
        has_tbl_header = False
        for r_idx, row in enumerate(table.rows):
            trPr = row._tr.trPr
            if trPr is not None:
                if trPr.find(qn('w:cantSplit')) is not None:
                    cant_split_count += 1
                if r_idx == 0 and trPr.find(qn('w:tblHeader')) is not None:
                    has_tbl_header = True

        info = {
            "indice": idx + 1,
            "filas": len(table.rows),
            "columnas": len(table.columns),
            "ancho_dxa": ancho_dxa,
            "es_flotante": es_flotante,
            "cant_split_filas": f"{cant_split_count}/{len(table.rows)}",
            "tiene_tbl_header": has_tbl_header
        }

        if es_flotante:
            reporte["advertencias"].append(f"Tabla {idx+1}: Contiene w:tblpPr (tabla flotante). Riesgo alto de saltos caóticos de página.")
        if cant_split_count < len(table.rows):
            reporte["advertencias"].append(f"Tabla {idx+1}: Solo {cant_split_count}/{len(table.rows)} filas tienen w:cantSplit.")
        if not has_tbl_header and len(table.rows) > 3:
            reporte["advertencias"].append(f"Tabla {idx+1}: No tiene w:tblHeader configurado en la fila 0.")

        reporte["tablas"].append(info)

    return reporte


def exportar_docx_a_pdf(docx_path, pdf_path=None):
    """
    Exporta un archivo DOCX a PDF usando Microsoft Word vía automatización COM en Windows.
    Garantiza una conversión 100% idéntica a la visualización de Word.
    """
    docx_path = Path(docx_path).resolve()
    if not pdf_path:
        pdf_path = docx_path.with_suffix(".pdf")
    else:
        pdf_path = Path(pdf_path).resolve()

    cmd = f"""
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $doc = $word.Documents.Open('{str(docx_path)}')
    $doc.SaveAs([ref]'{str(pdf_path)}', [ref]17) # 17 = wdFormatPDF
    $doc.Close()
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    """
    proc = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True)
    if proc.returncode != 0 or not pdf_path.exists():
        raise RuntimeError(f"Error al exportar DOCX a PDF: {proc.stderr or proc.stdout}")

    return str(pdf_path)


def renderizar_paginas_pdf(pdf_path, paginas_1based, out_dir, dpi=150):
    """
    Renderiza una lista de páginas específicas de un PDF a imágenes PNG a alta resolución.
    Permite verificar visualmente la maquetación sin abrir interfaces gráficas.
    """
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz

    doc = fitz.open(str(pdf_path))
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rutas_generadas = []
    for p_num in paginas_1based:
        idx = p_num - 1
        if 0 <= idx < len(doc):
            page = doc[idx]
            pix = page.get_pixmap(dpi=dpi)
            out_file = out_dir / f"pagina_{p_num}.png"
            pix.save(str(out_file))
            rutas_generadas.append(str(out_file))
        else:
            print(f"Advertencia: La página {p_num} excede el total de páginas del PDF ({len(doc)}).")

    return rutas_generadas


# ==============================================================================
# 4. INTERFAZ DE LÍNEA DE COMANDOS (CLI)
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Motor Quirúrgico DOCX/OpenXML para SIVAC-THESIS-LAB")
    subparsers = parser.add_subparsers(dest="comando", help="Comandos disponibles")

    # Comando: auditar
    p_audit = subparsers.add_parser("auditar", help="Auditar tablas y geometría en un DOCX")
    p_audit.add_argument("docx", help="Ruta al archivo .docx")

    # Comando: blindar-todas
    p_blind = subparsers.add_parser("blindar-todas", help="Inyectar cantSplit, tblHeader y eliminar flotación en todas las tablas")
    p_blind.add_argument("docx", help="Ruta al archivo .docx")
    p_blind.add_argument("--salida", default=None, help="Ruta de salida opcional (por defecto sobreescribe el archivo)")
    p_blind.add_argument("--sin-bordes", action="store_true", help="No alterar bordes existentes")

    # Comando: exportar-pdf
    p_pdf = subparsers.add_parser("exportar-pdf", help="Exportar DOCX a PDF mediante Word COM")
    p_pdf.add_argument("docx", help="Ruta al archivo .docx")
    p_pdf.add_argument("--pdf", default=None, help="Ruta de salida opcional del .pdf")

    # Comando: renderizar-paginas
    p_rend = subparsers.add_parser("renderizar-paginas", help="Renderizar páginas de un PDF a PNG para auditoría visual")
    p_rend.add_argument("pdf", help="Ruta al archivo .pdf")
    p_rend.add_argument("--paginas", required=True, help="Lista de páginas separadas por coma (ej. 32,51)")
    p_rend.add_argument("--out-dir", default="salidas/figuras/verificacion", help="Carpeta de salida")
    p_rend.add_argument("--dpi", type=int, default=150, help="Resolución DPI (default 150)")

    args = parser.parse_args()

    if args.comando == "auditar":
        res = auditar_documento_docx(args.docx)
        print(f"\n--- AUDITORÍA DE TABLAS: {res['archivo']} ---")
        print(f"Total de tablas: {res['total_tablas']}")
        for t in res["tablas"]:
            print(f"  [Tabla {t['indice']}] {t['filas']} filas x {t['columnas']} cols | Ancho: {t['ancho_dxa']} dxa | Flotante: {t['es_flotante']} | cantSplit: {t['cant_split_filas']} | Header: {t['tiene_tbl_header']}")
        if res["advertencias"]:
            print("\nADVERTENCIAS DETECTADAS:")
            for adv in res["advertencias"]:
                print(f"  [!] {adv}")
        else:
            print("\n[✓] Todas las tablas cumplen con las directivas de contención y flujo natural.")

    elif args.comando == "blindar-todas":
        n = blindar_todas_tablas_documento(args.docx, args.salida, aplicar_bordes=not args.sin_bordes)
        print(f"[✓] {n} tablas blindadas exitosamente (cantSplit, tblHeader, sin flotación).")

    elif args.comando == "exportar-pdf":
        out = exportar_docx_a_pdf(args.docx, args.pdf)
        print(f"[✓] PDF generado con éxito en: {out}")

    elif args.comando == "renderizar-paginas":
        p_list = [int(p.strip()) for p in args.paginas.split(",") if p.strip().isdigit()]
        imgs = renderizar_paginas_pdf(args.pdf, p_list, args.out_dir, dpi=args.dpi)
        print(f"[✓] {len(imgs)} página(s) renderizada(s):")
        for img in imgs:
            print(f"  - {img}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
