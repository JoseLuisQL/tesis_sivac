#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - MOTOR DE INSPECCION VISUAL Y AUDITORIA ESTRUCTURAL OPENXML
================================================================================
Modulo centralizado del Squad C / Squad E para la inspeccion y verificacion
quirurgica de documentos Word (.docx) y sus renders PDF.

Capacidades del motor:
  1. Deteccion y verificacion de saltos de pagina obligatorios (w:pageBreakBefore)
     en titulos de capitulos (I al V), preliminares institucionales, referencias
     bibliograficas y anexos.
  2. Deteccion de solapamiento potencial en tablas:
     - Celdas con w:line < 240 dxa o w:lineRule="exact" coexistiendo con formulas
       OMML (m:oMath) o bloques de texto multilineal.
     - Filas con w:trHeight w:hRule="exact" que bloquean el crecimiento natural
       de la celda provocando truncamiento o clipping.
     - Deteccion de tablas flotantes (w:tblpPr).
  3. Deteccion de espaciados gigantescos o malformaciones en listas con vinetas:
     - Falta de w:ind hanging (sangria invertida donde firstLine > 0 y left = 0).
     - Espaciados excesivos entre elementos (w:before / w:after > 240 dxa).
     - Sangria izquierda desmedida (w:left > 1440 dxa).
  4. Deteccion de rios tipograficos por quiebres manuales (<w:br/>) en parrafos
     justificados (w:jc w:val="both") que generan espaciados forzados anormales.
  5. Extraccion y verificacion de renders PDF a PNG via PyMuPDF:
     - Deteccion de paginas huerfanas / casi en blanco (densidad de tinta < 0.3%).
     - Deteccion de desborde de margenes seguros institucionales (A4 UNAJMA).
     - Deteccion de colisiones visuales entre bloques de contenido.
================================================================================
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import docx
from docx.oxml.ns import qn

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None

try:
    from PIL import Image, ImageStat
except ImportError:
    Image = None
    ImageStat = None

# Constantes de geometria y maquetacion UNAJMA / APA 7
TWIPS_POR_CM = 566.929
PUNTOS_POR_CM = 28.3465
PAGE_WIDTH_A4_PT = 595.32
PAGE_HEIGHT_A4_PT = 841.92

# Margenes seguros en puntos (A4: 595.32 x 841.92 pt)
# Izquierdo institucional: 3.0 cm (~85.0 pt) -> tolerancia segura 75.0 pt
# Derecho institucional: 2.5 cm (~70.8 pt) -> limite derecho 524.5 pt -> tolerancia 535.0 pt
# Superior: 2.5 cm (~70.8 pt) -> limite sup 60.0 pt
# Inferior: 2.5 cm (~70.8 pt) -> limite inf 780.0 pt
SAFE_MARGIN_LEFT_PT = 75.0
SAFE_MARGIN_RIGHT_PT = 535.0
SAFE_MARGIN_TOP_PT = 60.0
SAFE_MARGIN_BOTTOM_PT = 780.0

# Expresiones regulares canonicas para estructura capitular y preliminares
RE_CAPITULO = re.compile(
    r"^\s*CAP[I\u00cd]TULO\s+([IVXLCDM]+|\d+)\.?\s*.*$",
    re.I,
)
RE_PRELIMINARES_OBLIGATORIOS = re.compile(
    r"^\s*(INTRODUCCI[O\u00d3]N|RESUMEN|ABSTRACT|CHUMASQA|DEDICATORIA|AGRADECIMIENTOS|"
    r"[I\u00cd]NDICE\s+GENERAL|[I\u00cd]NDICE\s+DE\s+CONTENIDO|[I\u00cd]NDICE\s+DE\s+TABLAS|"
    r"LISTA\s+DE\s+TABLAS|[I\u00cd]NDICE\s+DE\s+FIGURAS|LISTA\s+DE\s+FIGURAS)\s*$",
    re.I,
)
RE_REFERENCIAS = re.compile(
    r"^\s*(REFERENCIAS?(?:\s+BIBLIOGR[\u00c1A]FICAS?)?|BIBLIOGRAF[I\u00cd]A)\s*$",
    re.I,
)
RE_ANEXOS_MAESTRO = re.compile(
    r"^\s*(ANEXOS?(\s+\d+.*)?)\s*$",
    re.I,
)
RE_GLIFO_VINETA = re.compile(r"^[\s\u2022\u2023\u25e6\u2043\u2219\-\u2013\u2014\*\u00b7]\s*")


@dataclass
class DefectoEditorial:
    categoria: str       # SALTO_PAGINA, SOLAPAMIENTO_TABLA, LISTA_VINETA, RIO_TIPOGRAFICO, RENDER_VISUAL
    codigo: str          # Identificador programmatico del defecto
    severidad: str       # CRITICA, ALTA, MEDIA, BAJA
    ubicacion: str       # Ej: P[96], Tabla 5 (Fila 2, Col 3), Pagina PDF 48
    descripcion: str     # Explicacion clara y concisa del hallazgo
    contexto: str        # Fragmento de texto o valores XML involucrados
    recomendacion: str   # Accion tecnica concreta para corregirlo


@dataclass
class MetricasInspeccion:
    total_parrafos: int = 0
    total_tablas: int = 0
    total_celdas: int = 0
    total_formulas_omml: int = 0
    total_listas_detectadas: int = 0
    total_quiebres_br: int = 0
    total_paginas_pdf: int = 0
    defectos_criticos: int = 0
    defectos_altos: int = 0
    defectos_medios: int = 0
    defectos_bajos: int = 0
    estado_general: str = "PENDIENTE"  # APROBADO, OBSERVADO, RECHAZADO


class InspectorVisualDocx:
    """Motor de inspeccion estructural OpenXML y visual PDF para documentos de tesis."""

    def __init__(self, docx_path: str | Path, pdf_path: Optional[str | Path] = None):
        self.docx_path = Path(docx_path).resolve()
        if not self.docx_path.exists():
            raise FileNotFoundError(f"No existe el archivo DOCX: {self.docx_path}")

        self.pdf_path: Optional[Path] = None
        if pdf_path:
            p = Path(pdf_path).resolve()
            if p.exists():
                self.pdf_path = p
        else:
            candidato = self.docx_path.with_suffix(".pdf")
            if candidato.exists():
                self.pdf_path = candidato

        self.doc = docx.Document(str(self.docx_path))
        self.defectos: List[DefectoEditorial] = []
        self.metricas = MetricasInspeccion()
        self.defectos: List[DefectoEditorial] = []
        self.metricas = MetricasInspeccion()

    # =========================================================================
    # 1. AUDITORIA DE SALTOS DE PAGINA OBLIGATORIOS (w:pageBreakBefore)
    # =========================================================================
    def auditar_saltos_pagina(self) -> List[DefectoEditorial]:
        """
        Verifica que cada capitulo, seccion preliminar mayor, referencias y anexos
        inicien estrictamente en una nueva pagina mediante:
          a) w:pageBreakBefore activo en w:pPr
          b) w:br con w:type="page" inmediatamente anterior o dentro del run inicial
          c) Salto de seccion de tipo pagina siguiente (w:sectPr no continuo)
        """
        hallazgos: List[DefectoEditorial] = []
        parrafos = self.doc.paragraphs
        self.metricas.total_parrafos = len(parrafos)

        for idx, p in enumerate(parrafos):
            txt = p.text.strip().replace("\xa0", " ")
            if not txt:
                continue

            es_capitulo = bool(RE_CAPITULO.match(txt))
            es_preliminar = bool(RE_PRELIMINARES_OBLIGATORIOS.match(txt))
            es_referencias = bool(RE_REFERENCIAS.match(txt))
            es_anexo = bool(RE_ANEXOS_MAESTRO.match(txt))

            # Excluir menciones en indice o tabla de contenidos
            if idx < 90 and any(k in txt.upper() for k in ["PAG", "PAGINA", ".....", "\t"]):
                continue

            if not (es_capitulo or es_preliminar or es_referencias or es_anexo):
                continue

            # El primer parrafo del documento ya inicia en pagina 1 por definicion
            if idx == 0:
                continue

            # Si es un anexo especifico (ej: Anexo 1) y el parrafo previo inmediato es "ANEXOS",
            # inician en la misma pagina por diseño editorial formal para evitar paginas huerfanas
            if es_anexo and idx > 0 and parrafos[idx - 1].text.strip().upper() == "ANEXOS":
                continue

            # Inspeccion XML del parrafo actual
            pPr = p._p.find(qn("w:pPr"))
            pb_before = False
            if pPr is not None:
                pbb_elem = pPr.find(qn("w:pageBreakBefore"))
                if pbb_elem is not None:
                    val = pbb_elem.get(qn("w:val"))
                    if val not in ("0", "false", "off"):
                        pb_before = True

            # Verificar si contiene un salto de pagina manual en sus propios runs
            tiene_br_page_propio = False
            for r in p._p.findall(qn("w:r")):
                for br in r.findall(qn("w:br")):
                    if br.get(qn("w:type")) == "page":
                        tiene_br_page_propio = True
                        break
                if tiene_br_page_propio:
                    break

            # Verificar si el parrafo anterior inmediato contiene salto de pagina o seccion
            tiene_salto_previo = False
            k = idx - 1
            while k >= 0 and k >= idx - 3:
                p_prev = parrafos[k]
                for br in p_prev._p.xpath(".//w:br[@w:type=\"page\"]"):
                    tiene_salto_previo = True
                    break
                sect = p_prev._p.xpath(".//w:sectPr")
                if sect:
                    sect_type = sect[0].find(qn("w:type"))
                    type_val = sect_type.get(qn("w:val")) if sect_type is not None else "nextPage"
                    if type_val != "continuous":
                        tiene_salto_previo = True
                        break
                if tiene_salto_previo or p_prev.text.strip():
                    break
                k -= 1

            if not (pb_before or tiene_br_page_propio or tiene_salto_previo):
                tipo_sec = (
                    "Capitulo"
                    if es_capitulo
                    else "Referencias"
                    if es_referencias
                    else "Anexos"
                    if es_anexo
                    else "Seccion Preliminar"
                )
                defecto = DefectoEditorial(
                    categoria="SALTO_PAGINA",
                    codigo="FALTA_SALTO_PAGINA_OBLIGATORIO",
                    severidad="ALTA",
                    ubicacion=f"Parrafo [{idx}]",
                    descripcion=f"{tipo_sec} \"{txt[:45]}...\" no inicia en pagina nueva.",
                    contexto=f"Texto: \"{txt[:60]}\" | pageBreakBefore={pb_before}, brPage={tiene_br_page_propio}, saltoPrevio={tiene_salto_previo}",
                    recomendacion="Inyectar <w:pageBreakBefore/> en w:pPr del parrafo o preceder con salto de pagina formal.",
                )
                hallazgos.append(defecto)

        self.defectos.extend(hallazgos)
        return hallazgos


    # =========================================================================
    # 2. AUDITORIA DE SOLAPAMIENTO POTENCIAL EN TABLAS
    # =========================================================================
    def auditar_solapamiento_tablas(self) -> List[DefectoEditorial]:
        hallazgos: List[DefectoEditorial] = []
        tablas = self.doc.tables
        self.metricas.total_tablas = len(tablas)

        for t_idx, table in enumerate(tablas):
            tblPr = table._tbl.tblPr
            if tblPr.find(qn("w:tblpPr")) is not None:
                hallazgos.append(DefectoEditorial(
                    categoria="SOLAPAMIENTO_TABLA",
                    codigo="TABLA_FLOTANTE_RIESGO_SOLAPAMIENTO",
                    severidad="CRITICA",
                    ubicacion=f"Tabla {t_idx + 1}",
                    descripcion="Tabla con propiedades de flotacion.",
                    contexto="w:tblpPr presente",
                    recomendacion="Eliminar w:tblpPr"
                ))

            if len(table.rows) > 3:
                r0_trPr = table.rows[0]._tr.trPr
                if r0_trPr is None or r0_trPr.find(qn("w:tblHeader")) is None:
                    hallazgos.append(DefectoEditorial(
                        categoria="SOLAPAMIENTO_TABLA",
                        codigo="TABLA_SIN_TBL_HEADER",
                        severidad="MEDIA",
                        ubicacion=f"Tabla {t_idx + 1}, Fila 0",
                        descripcion=f"Tabla {t_idx + 1} ({len(table.rows)} filas) carece de w:tblHeader en fila 0.",
                        contexto="w:tblHeader ausente",
                        recomendacion="Inyectar w:tblHeader en la fila 0 para repeticion en saltos de pagina."
                    ))

            for r_idx, row in enumerate(table.rows):
                trPr = row._tr.trPr
                h_rule = None
                h_val = None
                if trPr is not None:
                    trHeight = trPr.find(qn("w:trHeight"))
                    if trHeight is not None:
                        h_rule = trHeight.get(qn("w:hRule"))
                        h_val = trHeight.get(qn("w:val"))

                    cant_split = trPr.find(qn("w:cantSplit"))
                    if cant_split is None:
                        hallazgos.append(DefectoEditorial(
                            categoria="SOLAPAMIENTO_TABLA",
                            codigo="FILA_SIN_CANT_SPLIT",
                            severidad="MEDIA",
                            ubicacion=f"Tabla {t_idx + 1}, Fila {r_idx}",
                            descripcion=f"Fila {r_idx} de Tabla {t_idx + 1} carece de w:cantSplit.",
                            contexto="w:cantSplit ausente",
                            recomendacion="Inyectar w:cantSplit en w:trPr de la fila."
                        ))

                for c_idx, cell in enumerate(row.cells):
                    self.metricas.total_celdas += 1
                    omml_elems = cell._tc.xpath(".//m:oMath | .//m:oMathPara")
                    if omml_elems:
                        self.metricas.total_formulas_omml += len(omml_elems)

                    c_txt = cell.text.strip()
                    if h_rule == "exact" and (omml_elems or len(cell.paragraphs) > 1 or len(c_txt) > 50):
                        hallazgos.append(DefectoEditorial(
                            categoria="SOLAPAMIENTO_TABLA",
                            codigo="FILA_ALTURA_EXACTA_SOLAPAMIENTO",
                            severidad="ALTA",
                            ubicacion=f"Tabla {t_idx + 1}, Fila {r_idx}, Col {c_idx}",
                            descripcion=f"Fila {r_idx} tiene altura fija exact (val={h_val}) con contenido multilineal o OMML.",
                            contexto=f"w:hRule=exact, val={h_val}, omml={len(omml_elems)}",
                            recomendacion="Cambiar w:hRule a atLeast o retirar w:trHeight para auto-ajuste."
                        ))

                    for p_idx, p in enumerate(cell.paragraphs):
                        pPr = p._p.find(qn("w:pPr"))
                        if pPr is None:
                            continue
                        sp = pPr.find(qn("w:spacing"))
                        if sp is None:
                            continue
                        line_str = sp.get(qn("w:line"))
                        rule_str = sp.get(qn("w:lineRule")) or "auto"
                        try:
                            line_val = int(line_str) if line_str is not None else None
                        except (ValueError, TypeError):
                            line_val = None

                        p_txt = p.text.strip()
                        if rule_str == "exact":
                            hallazgos.append(DefectoEditorial(
                                categoria="SOLAPAMIENTO_TABLA",
                                codigo="CELDA_INTERLINEADO_EXACTO",
                                severidad="ALTA",
                                ubicacion=f"Tabla {t_idx + 1}, Fila {r_idx}, Col {c_idx}, P[{p_idx}]",
                                descripcion=f"Parrafo en celda tiene lineRule=exact (line={line_str} dxa).",
                                contexto=f"w:lineRule=exact, w:line={line_str}",
                                recomendacion="Cambiar lineRule a auto con interlineado minimo de 200-240 dxa."
                            ))

                        if line_val is not None and line_val < 200:
                            if omml_elems:
                                hallazgos.append(DefectoEditorial(
                                    categoria="SOLAPAMIENTO_TABLA",
                                    codigo="CELDA_INTERLINEADO_COMPRIMIDO_OMML",
                                    severidad="ALTA",
                                    ubicacion=f"Tabla {t_idx + 1}, Fila {r_idx}, Col {c_idx}, P[{p_idx}]",
                                    descripcion=f"Interlineado de {line_val} dxa (< 200 dxa) en celda con formulas OMML.",
                                    contexto=f"w:line={line_val}, formulas_omml={len(omml_elems)}",
                                    recomendacion="Aumentar w:line a minimo 220-240 dxa en celdas con ecuaciones OMML."
                                ))
                            elif len(p_txt) > 60 or len(cell.paragraphs) > 1:
                                hallazgos.append(DefectoEditorial(
                                    categoria="SOLAPAMIENTO_TABLA",
                                    codigo="CELDA_INTERLINEADO_MUY_COMPRIMIDO",
                                    severidad="MEDIA",
                                    ubicacion=f"Tabla {t_idx + 1}, Fila {r_idx}, Col {c_idx}, P[{p_idx}]",
                                    descripcion=f"Interlineado de {line_val} dxa (< 200 dxa) en celda con texto denso.",
                                    contexto=f"w:line={line_val}, longitud={len(p_txt)}",
                                    recomendacion="Ajustar w:line a 200-240 dxa para legibilidad tipografica en celdas."
                                ))

        self.defectos.extend(hallazgos)
        return hallazgos

    # =========================================================================
    # 3. AUDITORIA DE LISTAS CON VINETAS Y NUMERACIONES
    # =========================================================================
    def auditar_listas_vinetas(self) -> List[DefectoEditorial]:
        hallazgos: List[DefectoEditorial] = []
        parrafos = self.doc.paragraphs

        for idx, p in enumerate(parrafos):
            txt = p.text.strip().replace("\xa0", " ")
            if not txt:
                continue

            pPr = p._p.find(qn("w:pPr"))
            if pPr is None:
                continue

            es_lista_xml = pPr.find(qn("w:numPr")) is not None
            es_lista_glifo = bool(RE_GLIFO_VINETA.match(txt))
            es_lista_estilo = False
            style_name = p.style.name if p.style else ""
            if any(k in style_name.lower() for k in ["list", "lista", "bullet"]):
                es_lista_estilo = True

            if not (es_lista_xml or es_lista_glifo or es_lista_estilo):
                continue

            self.metricas.total_listas_detectadas += 1

            ind = pPr.find(qn("w:ind"))
            first_line = 0
            left = 0
            hanging = 0
            if ind is not None:
                try:
                    first_line = int(ind.get(qn("w:firstLine")) or 0)
                except (ValueError, TypeError):
                    first_line = 0
                try:
                    left = int(ind.get(qn("w:left")) or 0)
                except (ValueError, TypeError):
                    left = 0
                try:
                    hanging = int(ind.get(qn("w:hanging")) or 0)
                except (ValueError, TypeError):
                    hanging = 0

            # 1. Sangria invertida en listas
            if (first_line > 0 and hanging == 0 and left == 0) or (first_line > 0 and hanging == 0 and left < first_line):
                hallazgos.append(DefectoEditorial(
                    categoria="LISTA_VINETA",
                    codigo="LISTA_SANGRIA_INVERTIDA",
                    severidad="ALTA",
                    ubicacion=f"Parrafo [{idx}]",
                    descripcion=f"Elemento de lista tiene sangria comun/invertida (firstLine={first_line} dxa, left={left}, hanging={hanging}).",
                    contexto=f"firstLine={first_line}, left={left}, hanging={hanging}",
                    recomendacion="Aplicar sangria francesa formal: w:left=720 (o 360) con w:hanging=360 y w:firstLine=0."
                ))

            # 2. Sangria izquierda desmedida
            if left > 1440:
                hallazgos.append(DefectoEditorial(
                    categoria="LISTA_VINETA",
                    codigo="LISTA_SANGRIA_DESMEDIDA",
                    severidad="MEDIA",
                    ubicacion=f"Parrafo [{idx}]",
                    descripcion=f"Elemento de lista tiene sangria izquierda desmedida (left={left} dxa > 2.54 cm).",
                    contexto=f"left={left} dxa",
                    recomendacion="Reducir w:left a valores institucionales estandar (720 dxa = 1.27 cm o 360 dxa = 0.63 cm)."
                ))

            # 3. Espaciado excesivo entre elementos de lista
            sp = pPr.find(qn("w:spacing"))
            if sp is not None:
                try:
                    before_val = int(sp.get(qn("w:before")) or 0)
                except (ValueError, TypeError):
                    before_val = 0
                try:
                    after_val = int(sp.get(qn("w:after")) or 0)
                except (ValueError, TypeError):
                    after_val = 0

                if before_val > 240 or after_val > 240:
                    hallazgos.append(DefectoEditorial(
                        categoria="LISTA_VINETA",
                        codigo="LISTA_ESPACIADO_EXCESIVO",
                        severidad="MEDIA",
                        ubicacion=f"Parrafo [{idx}]",
                        descripcion=f"Elemento de lista con espaciado vertical excesivo (before={before_val} dxa, after={after_val} dxa).",
                        contexto=f"before={before_val}, after={after_val}",
                        recomendacion="Fijar w:before=0 y w:after=60-120 dxa (3-6 pt) para mantener cohesion en listas."
                    ))

        self.defectos.extend(hallazgos)
        return hallazgos

    # =========================================================================
    # 4. AUDITORIA DE RIOS TIPOGRAFICOS POR QUIEBRES MANUALES (<w:br/>)
    # =========================================================================
    def auditar_rios_tipograficos(self) -> List[DefectoEditorial]:
        hallazgos: List[DefectoEditorial] = []
        parrafos = self.doc.paragraphs

        for idx, p in enumerate(parrafos):
            pPr = p._p.find(qn("w:pPr"))
            alineacion = "both"
            if pPr is not None:
                jc = pPr.find(qn("w:jc"))
                if jc is not None:
                    alineacion = jc.get(qn("w:val")) or "both"

            br_manuales = []
            for r in p._p.findall(qn("w:r")):
                for br in r.findall(qn("w:br")):
                    br_type = br.get(qn("w:type"))
                    if br_type != "page":
                        br_manuales.append(br)

            if not br_manuales:
                continue

            self.metricas.total_quiebres_br += len(br_manuales)
            txt_completo = p.text.strip().replace("\xa0", " ")

            if alineacion == "both":
                fragmentos = []
                frag_actual = []
                for node in p._p.iterchildren():
                    if node.tag == qn("w:r"):
                        for child in node.iterchildren():
                            if child.tag == qn("w:t"):
                                frag_actual.append(child.text or "")
                            elif child.tag == qn("w:br") and child.get(qn("w:type")) != "page":
                                fragmentos.append("".join(frag_actual))
                                frag_actual = []
                if frag_actual:
                    fragmentos.append("".join(frag_actual))

                for f_idx, frag in enumerate(fragmentos[:-1]):
                    frag_clean = frag.strip()
                    longitud = len(frag_clean)
                    if 0 < longitud < 65:
                        hallazgos.append(DefectoEditorial(
                            categoria="RIO_TIPOGRAFICO",
                            codigo="RIO_TIPOGRAFICO_BR_JUSTIFICADO",
                            severidad="CRITICA" if longitud < 40 else "ALTA",
                            ubicacion=f"Parrafo [{idx}], Fragmento {f_idx + 1}",
                            descripcion=f"Quiebre manual <w:br/> en parrafo justificado con linea corta ({longitud} caracteres).",
                            contexto=f"Linea afectada: {frag_clean[:50]} ({longitud} chars)",
                            recomendacion="Reemplazar <w:br/> por salto de parrafo formal (<w:p>) o eliminar el quiebre manual."
                        ))

            if len(br_manuales) >= 3:
                hallazgos.append(DefectoEditorial(
                    categoria="RIO_TIPOGRAFICO",
                    codigo="PSEUDOPARRAFO_AGRUPADO_BR",
                    severidad="MEDIA",
                    ubicacion=f"Parrafo [{idx}]",
                    descripcion=f"Parrafo empaqueta {len(br_manuales)} quiebres de linea manuales.",
                    contexto=f"Texto: {txt_completo[:50]}... | Total w:br={len(br_manuales)}",
                    recomendacion="Dividir el bloque en parrafos independientes con sus propios estilos y sangrias APA 7."
                ))

        self.defectos.extend(hallazgos)
        return hallazgos

    # =========================================================================
    # 5. AUDITORIA VISUAL DE RENDERS PDF A PNG VIA PYMUPDF
    # =========================================================================
    def auditar_visual_pdf(self, output_png_dir: Optional[str | Path] = None) -> List[DefectoEditorial]:
        hallazgos: List[DefectoEditorial] = []

        if fitz is None:
            hallazgos.append(DefectoEditorial(
                categoria="RENDER_VISUAL",
                codigo="PYMUPDF_NO_INSTALADO",
                severidad="BAJA",
                ubicacion="Sistema",
                descripcion="PyMuPDF no esta disponible en el entorno.",
                contexto="fitz is None",
                recomendacion="Instalar pymupdf en el entorno virtual."
            ))
            self.defectos.extend(hallazgos)
            return hallazgos

        if not self.pdf_path or not self.pdf_path.exists():
            hallazgos.append(DefectoEditorial(
                categoria="RENDER_VISUAL",
                codigo="PDF_NO_ENCONTRADO",
                severidad="BAJA",
                ubicacion=str(self.docx_path),
                descripcion=f"No se encontro archivo PDF para {self.docx_path.name}.",
                contexto=f"pdf_path={self.pdf_path}",
                recomendacion="Compilar o exportar a PDF antes de auditar render visual."
            ))
            self.defectos.extend(hallazgos)
            return hallazgos

        out_dir = Path(output_png_dir).resolve() if output_png_dir else None
        if out_dir:
            out_dir.mkdir(parents=True, exist_ok=True)

        import io
        doc_pdf = fitz.open(str(self.pdf_path))
        self.metricas.total_paginas_pdf = len(doc_pdf)

        for p_idx in range(len(doc_pdf)):
            page = doc_pdf[p_idx]
            pix = page.get_pixmap(dpi=150)
            p_num = p_idx + 1

            if out_dir:
                png_path = out_dir / f"pagina_{p_num:02d}.png"
                pix.save(str(png_path))

            # 1. Densidad de tinta y pagina huerfana
            if Image is not None:
                img_data = pix.tobytes()
                img = Image.open(io.BytesIO(img_data)).convert("L")
                histogram = img.histogram()
                total_pixels = img.width * img.height
                pixels_tinta = sum(histogram[:240])
                densidad_tinta = pixels_tinta / total_pixels if total_pixels > 0 else 0.0

                text_page = page.get_text().strip()
                palabras = len(text_page.split())

                if p_num > 1 and densidad_tinta < 0.003 and palabras < 20:
                    hallazgos.append(DefectoEditorial(
                        categoria="RENDER_VISUAL",
                        codigo="PAGINA_HUERFANA_CASI_BLANCO",
                        severidad="ALTA",
                        ubicacion=f"Pagina PDF {p_num}",
                        descripcion=f"Pagina {p_num} es casi blanca (densidad tinta: {densidad_tinta*100:.2f}%, palabras: {palabras}).",
                        contexto=f"densidad={densidad_tinta:.4f}, palabras={palabras}, texto={text_page[:35]}",
                        recomendacion="Revisar saltos de pagina redundantes o tablas desbordadas que empujan saltos en blanco."
                    ))

            # 2. Desborde de margenes seguros institucionales
            blocks = page.get_text("blocks")
            text_rects = []

            # Discriminar orientación de página (vertical portrait vs apaisada landscape)
            es_landscape = page.rect.width > 600.0
            if es_landscape:
                lim_left = 55.0
                lim_right = page.rect.width - 55.0
                lim_top = 45.0
                lim_bottom = page.rect.height - 45.0
            else:
                lim_left = SAFE_MARGIN_LEFT_PT - 6.0
                lim_right = SAFE_MARGIN_RIGHT_PT + 8.0
                lim_top = 55.0
                lim_bottom = 795.0

            words = page.get_text("words")

            for b_idx, b in enumerate(blocks):
                x0, y0, x1, y1 = b[:4]
                b_text = b[4].strip() if len(b) > 4 else ""

                if not b_text or len(b_text) < 3:
                    continue

                # Ignorar encabezados y pies de pagina normales
                if y0 < lim_top or y1 > lim_bottom:
                    continue

                text_rects.append((fitz.Rect(x0, y0, x1, y1), b_text, b_idx))

                if x0 < lim_left:
                    hallazgos.append(DefectoEditorial(
                        categoria="RENDER_VISUAL",
                        codigo="DESBORDE_MARGEN_IZQUIERDO",
                        severidad="MEDIA",
                        ubicacion=f"Pagina PDF {p_num}, Bloque {b_idx}",
                        descripcion=f"Contenido excede el margen izquierdo seguro ({x0:.1f} pt < {lim_left:.1f} pt).",
                        contexto=f"x0={x0:.1f}, texto={b_text[:40]}",
                        recomendacion="Verificar sangrias negativas de parrafos o celdas de tablas desalineadas."
                    ))

                if x1 > lim_right:
                    hallazgos.append(DefectoEditorial(
                        categoria="RENDER_VISUAL",
                        codigo="DESBORDE_MARGEN_DERECHO",
                        severidad="MEDIA",
                        ubicacion=f"Pagina PDF {p_num}, Bloque {b_idx}",
                        descripcion=f"Contenido excede el margen derecho seguro ({x1:.1f} pt > {lim_right:.1f} pt).",
                        contexto=f"x1={x1:.1f}, texto={b_text[:40]}",
                        recomendacion="Verificar ancho de tablas o formulas largas sin quiebre."
                    ))

            # 3. Colisiones y solapamientos visuales reales entre bloques
            for i in range(len(text_rects)):
                r_a, txt_a, idx_a = text_rects[i]
                for j in range(i + 1, len(text_rects)):
                    r_b, txt_b, idx_b = text_rects[j]
                    inter = fitz.Rect(r_a).intersect(r_b)
                    if not inter.is_empty and inter.width > 15.0 and inter.height > 6.0:
                        # Validar a nivel de palabras para descartar falsos positivos de celdas adyacentes o saltos de línea envueltos en tablas
                        wa = [w for w in words if w[5] == idx_a]
                        wb = [w for w in words if w[5] == idx_b]
                        hay_colision_real = False
                        col_desc = ""
                        for w1 in wa:
                            r1 = fitz.Rect(w1[:4])
                            for w2 in wb:
                                r2 = fitz.Rect(w2[:4])
                                winter = r1.intersect(r2)
                                # Descartar colisiones irrelevantes o fracciones donde numerador y denominador solo tocan la barra
                                if not winter.is_empty and winter.width > 6.0 and winter.height > 6.0:
                                    hay_colision_real = True
                                    col_desc = f"'{w1[4]}' vs '{w2[4]}' ({winter.width:.1f}x{winter.height:.1f} pt)"
                                    break
                            if hay_colision_real:
                                break

                        if hay_colision_real:
                            hallazgos.append(DefectoEditorial(
                                categoria="RENDER_VISUAL",
                                codigo="COLISION_BLOQUES_VISUALES",
                                severidad="ALTA",
                                ubicacion=f"Pagina PDF {p_num}",
                                descripcion="Colision y solapamiento visual directo detectado entre bloques de texto en PDF.",
                                contexto=f"Bloque A: {txt_a[:25]} | Bloque B: {txt_b[:25]} | Solapamiento: {col_desc}",
                                recomendacion="Verificar tablas flotantes o saltos de linea negativos en el documento DOCX."
                            ))

        doc_pdf.close()
        self.defectos.extend(hallazgos)
        return hallazgos

    # =========================================================================
    # 6. EJECUCION INTEGRAL Y REPORTES
    # =========================================================================
    def ejecutar_auditoria_completa(self, output_png_dir: Optional[str | Path] = None) -> MetricasInspeccion:
        self.defectos = []
        self.auditar_saltos_pagina()
        self.auditar_solapamiento_tablas()
        self.auditar_listas_vinetas()
        self.auditar_rios_tipograficos()
        self.auditar_visual_pdf(output_png_dir=output_png_dir)

        self.metricas.defectos_criticos = sum(1 for d in self.defectos if d.severidad == "CRITICA")
        self.metricas.defectos_altos = sum(1 for d in self.defectos if d.severidad == "ALTA")
        self.metricas.defectos_medios = sum(1 for d in self.defectos if d.severidad == "MEDIA")
        self.metricas.defectos_bajos = sum(1 for d in self.defectos if d.severidad == "BAJA")

        if self.metricas.defectos_criticos > 0 or self.metricas.defectos_altos > 0:
            self.metricas.estado_general = "RECHAZADO"
        elif self.metricas.defectos_medios > 0:
            self.metricas.estado_general = "OBSERVADO"
        else:
            self.metricas.estado_general = "APROBADO"

        return self.metricas

    def to_dict(self) -> Dict[str, Any]:
        return {
            "documento_docx": str(self.docx_path),
            "documento_pdf": str(self.pdf_path) if self.pdf_path else None,
            "metricas": asdict(self.metricas),
            "total_defectos": len(self.defectos),
            "defectos": [asdict(d) for d in self.defectos],
        }

    def generar_reporte_texto(self) -> str:
        lineas = []
        lineas.append("=" * 72)
        lineas.append("SIVAC-THESIS-LAB - REPORTE DE INSPECCION VISUAL Y AUDITORIA OPENXML")
        lineas.append("=" * 72)
        lineas.append(f"Archivo DOCX: {self.docx_path.name}")
        if self.pdf_path:
            lineas.append(f"Archivo PDF : {self.pdf_path.name}")
        lineas.append(f"Estado      : {self.metricas.estado_general}")
        lineas.append("-" * 72)
        lineas.append("METRICAS CUANTITATIVAS:")
        lineas.append(f"  - Total Parrafos       : {self.metricas.total_parrafos}")
        lineas.append(f"  - Total Tablas         : {self.metricas.total_tablas}")
        lineas.append(f"  - Total Celdas         : {self.metricas.total_celdas}")
        lineas.append(f"  - Formulas OMML        : {self.metricas.total_formulas_omml}")
        lineas.append(f"  - Listas Detectadas    : {self.metricas.total_listas_detectadas}")
        lineas.append(f"  - Quiebres w:br        : {self.metricas.total_quiebres_br}")
        lineas.append(f"  - Paginas PDF          : {self.metricas.total_paginas_pdf}")
        lineas.append("-" * 72)
        lineas.append("DEFECTOS POR SEVERIDAD:")
        lineas.append(f"  - Criticos : {self.metricas.defectos_criticos}")
        lineas.append(f"  - Altos    : {self.metricas.defectos_altos}")
        lineas.append(f"  - Medios   : {self.metricas.defectos_medios}")
        lineas.append(f"  - Bajos    : {self.metricas.defectos_bajos}")
        lineas.append(f"  - TOTAL    : {len(self.defectos)}")
        lineas.append("=" * 72)

        if not self.defectos:
            lineas.append("EXCELENTE: 0 defectos detectados. El documento cumple al 100% las compuertas.")
        else:
            lineas.append("\nDETALLE DE DEFECTOS REGISTRADOS:")
            for idx, d in enumerate(self.defectos, 1):
                lineas.append(f"\n[{idx:02d}] [{d.severidad}] ({d.categoria}) {d.codigo} en {d.ubicacion}")
                lineas.append(f"     Descripcion  : {d.descripcion}")
                lineas.append(f"     Contexto     : {d.contexto}")
                lineas.append(f"     Recomendacion: {d.recomendacion}")

        lineas.append("\n" + "=" * 72)
        return "\n".join(lineas)

    def generar_reporte_markdown(self) -> str:
        md = []
        md.append("# Reporte de Auditoria Editorial y Visual OpenXML")
        md.append(f"- **Documento DOCX:** `{self.docx_path.name}`")
        if self.pdf_path:
            md.append(f"- **Documento PDF:** `{self.pdf_path.name}` ({self.metricas.total_paginas_pdf} paginas)")
        md.append(f"- **Estado General:** `{self.metricas.estado_general}`")
        md.append("")
        md.append("## Resumen de Metricas Estructurales")
        md.append("| Metrica | Valor |")
        md.append("|---|---|")
        md.append(f"| Total Parrafos | {self.metricas.total_parrafos} |")
        md.append(f"| Total Tablas | {self.metricas.total_tablas} |")
        md.append(f"| Total Celdas | {self.metricas.total_celdas} |")
        md.append(f"| Formulas OMML en Celdas | {self.metricas.total_formulas_omml} |")
        md.append(f"| Listas Detectadas | {self.metricas.total_listas_detectadas} |")
        md.append(f"| Quiebres Manuales (w:br) | {self.metricas.total_quiebres_br} |")
        md.append(f"| Defectos Criticos | {self.metricas.defectos_criticos} |")
        md.append(f"| Defectos Altos | {self.metricas.defectos_altos} |")
        md.append(f"| Defectos Medios | {self.metricas.defectos_medios} |")
        md.append(f"| Defectos Bajos | {self.metricas.defectos_bajos} |")
        md.append("")
        if not self.defectos:
            md.append("### Resultado: APROBADO (0 Defectos)")
            md.append("El documento satisface plenamente los estandares de maquetacion editorial UNAJMA y APA 7.")
        else:
            md.append("## Hallazgos y Defectos Detectados")
            md.append("| # | Categoria | Severidad | Ubicacion | Codigo | Descripcion |")
            md.append("|---|---|---|---|---|---|")
            for idx, d in enumerate(self.defectos, 1):
                md.append(f"| {idx} | {d.categoria} | **{d.severidad}** | {d.ubicacion} | `{d.codigo}` | {d.descripcion} |")
            md.append("")
            md.append("### Acciones de Mitigacion Recomendadas")
            for idx, d in enumerate(self.defectos, 1):
                md.append(f"- **[{idx}] {d.codigo} ({d.ubicacion}):** {d.recomendacion}")
        return "\n".join(md)

# =============================================================================
# FUNCION PRINCIPAL Y CLI
# =============================================================================
def auditar_documento_completo(
    docx_path: str | Path,
    pdf_path: Optional[str | Path] = None,
    output_png_dir: Optional[str | Path] = None
) -> Tuple[MetricasInspeccion, List[DefectoEditorial]]:
    inspector = InspectorVisualDocx(docx_path=docx_path, pdf_path=pdf_path)
    metricas = inspector.ejecutar_auditoria_completa(output_png_dir=output_png_dir)
    return metricas, inspector.defectos


def main():
    parser = argparse.ArgumentParser(
        description="SIVAC-THESIS-LAB - Inspector Visual y Auditor Estructural OpenXML"
    )
    subparsers = parser.add_subparsers(dest="comando", help="Comandos disponibles")

    # Comando auditar (completo)
    p_auditar = subparsers.add_parser("auditar", help="Auditoria integral de todos los factores editoriales")
    p_auditar.add_argument("docx", help="Ruta al archivo .docx")
    p_auditar.add_argument("--pdf", default=None, help="Ruta al archivo .pdf (opcional)")
    p_auditar.add_argument("--render-dir", default=None, help="Directorio donde guardar renders PNG de paginas")
    p_auditar.add_argument("--json", action="store_true", help="Emitir reporte en formato JSON por stdout")
    p_auditar.add_argument("--salida-md", default=None, help="Guardar reporte detallado en archivo Markdown")

    # Comandos especificos
    p_saltos = subparsers.add_parser("saltos", help="Auditar unicamente saltos de pagina obligatorios")
    p_saltos.add_argument("docx", help="Ruta al archivo .docx")

    p_tablas = subparsers.add_parser("tablas", help="Auditar unicamente solapamiento y anomalias en tablas")
    p_tablas.add_argument("docx", help="Ruta al archivo .docx")

    p_listas = subparsers.add_parser("listas", help="Auditar geometria y sangrias en listas con vinetas")
    p_listas.add_argument("docx", help="Ruta al archivo .docx")

    p_rios = subparsers.add_parser("rios", help="Auditar rios tipograficos por quiebres manuales w:br")
    p_rios.add_argument("docx", help="Ruta al archivo .docx")

    p_render = subparsers.add_parser("render", help="Auditoria visual y exportacion de paginas PDF a PNG")
    p_render.add_argument("docx", help="Ruta al archivo .docx")
    p_render.add_argument("--pdf", default=None, help="Ruta al archivo .pdf")
    p_render.add_argument("--out-dir", required=True, help="Directorio para almacenar PNGs")

    args = parser.parse_args()

    if not args.comando or args.comando == "auditar":
        docx_target = getattr(args, "docx", None)
        if not docx_target:
            parser.print_help()
            sys.exit(2)

        inspector = InspectorVisualDocx(docx_path=args.docx, pdf_path=getattr(args, "pdf", None))
        inspector.ejecutar_auditoria_completa(output_png_dir=getattr(args, "render_dir", None))

        if getattr(args, "json", False):
            print(json.dumps(inspector.to_dict(), indent=2, ensure_ascii=False))
        else:
            print(inspector.generar_reporte_texto())

        if getattr(args, "salida_md", None):
            with open(args.salida_md, "w", encoding="utf-8") as f:
                f.write(inspector.generar_reporte_markdown())
            print(f"\nReporte Markdown guardado en: {args.salida_md}")

        sys.exit(1 if inspector.metricas.defectos_criticos > 0 or inspector.metricas.defectos_altos > 0 else 0)

    elif args.comando == "saltos":
        inspector = InspectorVisualDocx(docx_path=args.docx)
        hallazgos = inspector.auditar_saltos_pagina()
        print(f"Saltos auditados: {len(hallazgos)} observaciones encontradas.\n")
        for h in hallazgos:
            print(f"[{h.severidad}] {h.ubicacion}: {h.descripcion}")
        sys.exit(1 if hallazgos else 0)

    elif args.comando == "tablas":
        inspector = InspectorVisualDocx(docx_path=args.docx)
        hallazgos = inspector.auditar_solapamiento_tablas()
        print(f"Tablas auditadas: {len(hallazgos)} observaciones encontradas.\n")
        for h in hallazgos:
            print(f"[{h.severidad}] {h.ubicacion}: {h.descripcion}")
        sys.exit(1 if hallazgos else 0)

    elif args.comando == "listas":
        inspector = InspectorVisualDocx(docx_path=args.docx)
        hallazgos = inspector.auditar_listas_vinetas()
        print(f"Listas auditadas: {len(hallazgos)} observaciones encontradas.\n")
        for h in hallazgos:
            print(f"[{h.severidad}] {h.ubicacion}: {h.descripcion}")
        sys.exit(1 if hallazgos else 0)

    elif args.comando == "rios":
        inspector = InspectorVisualDocx(docx_path=args.docx)
        hallazgos = inspector.auditar_rios_tipograficos()
        print(f"Rios auditados: {len(hallazgos)} observaciones encontradas.\n")
        for h in hallazgos:
            print(f"[{h.severidad}] {h.ubicacion}: {h.descripcion}")
        sys.exit(1 if hallazgos else 0)

    elif args.comando == "render":
        inspector = InspectorVisualDocx(docx_path=args.docx, pdf_path=args.pdf)
        hallazgos = inspector.auditar_visual_pdf(output_png_dir=args.out_dir)
        print(f"Renders exportados a: {args.out_dir}")
        print(f"Observaciones visuales: {len(hallazgos)}")
        for h in hallazgos:
            print(f"[{h.severidad}] {h.ubicacion}: {h.descripcion}")
        sys.exit(1 if hallazgos else 0)


if __name__ == "__main__":
    main()
