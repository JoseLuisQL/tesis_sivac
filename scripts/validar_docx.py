#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - AUDITOR Y VALIDADOR INTEGRAL DE DOCUMENTOS .DOCX / OPENXML
Universidad Nacional José María Arguedas (UNAJMA)
Facultad de Ingeniería - Escuela Profesional de Ingeniería de Sistemas
================================================================================

Herramienta de auditoría estática y validación estructural OpenXML nativa.
Verifica que los documentos generados cumplan estrictamente con las directrices
institucionales UNAJMA, normas APA 7.ª edición y los estándares del proyecto SIVAC:

Verificaciones ejecutadas:
  1. Ausencia total de tablas flotantes (<w:tblpPr>).
  2. Indivisibilidad de filas en saltos de página (<w:cantSplit/> en todas las filas).
  3. Repetición de encabezados de tabla (<w:tblHeader/> en la fila 0).
  4. Geometría tabular y ancho máximo frente al límite portrait (8788 dxa / 15.50 cm).
  5. Ausencia de residuos de delimitadores de dólares ($) y sintaxis LaTeX no convertida.
  6. Censo e integridad de ecuaciones matemáticas nativas OMML (<m:oMath>).
  7. Detección y prevención de párrafos vacíos redundantes.
  8. Presencia y poblado de índices nativos (TOC, Lista de Tablas, Lista de Figuras).

Códigos de salida:
  0: Aprobado (documento sin observaciones críticas ni estructurales).
  1: Con observaciones (se detectaron incumplimientos o advertencias mayores).
  2: Error de ejecución o archivo no encontrado.
================================================================================
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import docx
from docx.oxml.ns import qn

# Constantes de geometría y maquetación UNAJMA / APA 7
ANCHO_UTIL_PORTRAIT_DXA = 8788   # 15.50 cm (A4 21.0 cm - Margen Izq 3.0 cm - Margen Der 2.50 cm)
ANCHO_UTIL_LANDSCAPE_DXA = 14000 # 24.70 cm (A4 29.7 cm - Margen Izq 2.5 cm - Margen Der 2.50 cm)
DXA_POR_CM = 567.0               # 1 cm = 567 dxa (aprox. 566.929)

# Expresiones regulares para detección de LaTeX residual o caracteres $
RE_DOLLAR = re.compile(r"\$")
RE_LATEX_COMMANDS = re.compile(
    r"\\[a-zA-Z]+(?:\*|\b|(?=[{^_\s\d]))|"
    r"\\(?:alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|"
    r"pi|rho|sigma|tau|upsilon|phi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|"
    r"Upsilon|Phi|Psi|Omega|sum|prod|int|frac|sqrt|partial|times|cdot|pm|leq|geq|neq|"
    r"approx|equiv|forall|exists|in|notin|subset|subseteq|cup|cap|to|rightarrow|"
    r"longrightarrow|leftarrow|longleftarrow|leftrightarrow|text|mathbf|mathit|mathrm|"
    r"begin|end|left|right|over|choose)\b",
    re.IGNORECASE
)
RE_LATEX_SUB_SUPER = re.compile(r"[_^]\{[^{}]+\}")
RE_LATEX_DELIMITED = re.compile(r"\$\$?[^$\n]+?\$?\$")


# ==============================================================================
# CLASE DE AUDITORÍA OPENXML
# ==============================================================================

class AuditorDocxOpenXML:
    """Auditor exhaustivo de documentos Microsoft Word (.docx) para SIVAC-THESIS-LAB."""

    def __init__(self, ruta_docx: str, limite_ancho_dxa: int = ANCHO_UTIL_PORTRAIT_DXA,
                 tolerancia_dxa: int = 5, verbose: bool = False):
        self.ruta_docx = os.path.abspath(ruta_docx)
        self.limite_ancho_dxa = limite_ancho_dxa
        self.tolerancia_dxa = tolerancia_dxa
        self.verbose = verbose

        if not os.path.isfile(self.ruta_docx):
            raise FileNotFoundError(f"No se encontró el archivo .docx en la ruta: {self.ruta_docx}")

        self.tamano_bytes = os.path.getsize(self.ruta_docx)
        self.doc = docx.Document(self.ruta_docx)
        self.observaciones: List[Dict[str, Any]] = []
        self.resultados_pruebas: Dict[str, Any] = {}

    def registrar_observacion(self, severidad: str, regla: str, ubicacion: str,
                              detalle: str, evidencia: Optional[str] = None):
        """Registra un hallazgo o incumplimiento detectado."""
        self.observaciones.append({
            "severidad": severidad.upper(),  # CRITICO, MAYOR, MENOR, INFO
            "regla": regla,
            "ubicacion": ubicacion,
            "detalle": detalle,
            "evidencia": evidencia
        })

    # --------------------------------------------------------------------------
    # 1. VERIFICACIÓN: Ausencia de Tablas Flotantes (w:tblpPr)
    # --------------------------------------------------------------------------
    def auditar_tablas_flotantes(self) -> Dict[str, Any]:
        """
        Comprueba que ninguna tabla contenga propiedades de posicionamiento flotante (<w:tblpPr>).
        Las tablas flotantes causan desbordes impredecibles de márgenes y fallas de paginación.
        """
        tablas_flotantes = []
        total_tablas = len(self.doc.tables)

        for idx, table in enumerate(self.doc.tables):
            tblPr = table._tbl.tblPr
            tblpPr = tblPr.find(qn("w:tblpPr"))
            if tblpPr is not None:
                # Extraer atributos de flotación
                attrs = dict(tblpPr.attrib)
                tablas_flotantes.append({
                    "indice_tabla": idx + 1,
                    "atributos": attrs
                })
                self.registrar_observacion(
                    severidad="CRITICO",
                    regla="TABLA_FLOTANTE",
                    ubicacion=f"Tabla {idx + 1}",
                    detalle=f"La tabla posee elemento <w:tblpPr> (tabla flotante). Esto quiebra la paginación OpenXML.",
                    evidencia=str(attrs)
                )

        aprobado = len(tablas_flotantes) == 0
        resultado = {
            "regla": "AUSENCIA_TABLAS_FLOTANTES",
            "descripcion": "Verificación de ausencia de tablas flotantes (<w:tblpPr>)",
            "total_tablas": total_tablas,
            "tablas_flotantes": len(tablas_flotantes),
            "aprobado": aprobado,
            "detalles": tablas_flotantes
        }
        self.resultados_pruebas["tablas_flotantes"] = resultado
        return resultado

    # --------------------------------------------------------------------------
    # 2. VERIFICACIÓN: Filas con w:cantSplit
    # --------------------------------------------------------------------------
    def auditar_cant_split(self) -> Dict[str, Any]:
        """
        Comprueba que todas las filas de todas las tablas tengan la propiedad <w:cantSplit/>,
        garantizando que ninguna fila se parta a la mitad entre dos páginas.
        """
        total_filas = 0
        filas_con_cant_split = 0
        tablas_con_faltantes = []

        for t_idx, table in enumerate(self.doc.tables):
            filas_tabla = len(table.rows)
            total_filas += filas_tabla
            filas_sin_split = []

            for r_idx, row in enumerate(table.rows):
                trPr = row._tr.trPr
                tiene_cs = trPr is not None and trPr.find(qn("w:cantSplit")) is not None
                if tiene_cs:
                    filas_con_cant_split += 1
                else:
                    filas_sin_split.append(r_idx)

            if filas_sin_split:
                tablas_con_faltantes.append({
                    "indice_tabla": t_idx + 1,
                    "total_filas": filas_tabla,
                    "filas_sin_cantsplit": filas_sin_split
                })
                self.registrar_observacion(
                    severidad="MAYOR",
                    regla="FILAS_CANTSPLIT",
                    ubicacion=f"Tabla {t_idx + 1}",
                    detalle=f"{len(filas_sin_split)} de {filas_tabla} filas carecen de <w:cantSplit/>.",
                    evidencia=f"Filas afectadas (0-based): {filas_sin_split}"
                )

        aprobado = len(tablas_con_faltantes) == 0
        resultado = {
            "regla": "FILAS_INDIVISIBLES_CANTSPLIT",
            "descripcion": "Blindaje contra partición de filas en saltos de página (<w:cantSplit/>)",
            "total_tablas": len(self.doc.tables),
            "total_filas": total_filas,
            "filas_con_cantsplit": filas_con_cant_split,
            "tablas_afectadas": len(tablas_con_faltantes),
            "aprobado": aprobado,
            "detalles": tablas_con_faltantes
        }
        self.resultados_pruebas["cant_split"] = resultado
        return resultado

    # --------------------------------------------------------------------------
    # 3. VERIFICACIÓN: Encabezados con w:tblHeader
    # --------------------------------------------------------------------------
    def auditar_tbl_header(self) -> Dict[str, Any]:
        """
        Comprueba que la primera fila (fila 0) de cada tabla tenga asignada la etiqueta
        <w:tblHeader/>, asegurando la repetición automática del encabezado en desbordes.
        """
        total_tablas = len(self.doc.tables)
        tablas_sin_header = []

        for t_idx, table in enumerate(self.doc.tables):
            if len(table.rows) == 0:
                continue

            fila_0 = table.rows[0]
            trPr = fila_0._tr.trPr
            tiene_header = trPr is not None and trPr.find(qn("w:tblHeader")) is not None

            if not tiene_header:
                tablas_sin_header.append(t_idx + 1)
                self.registrar_observacion(
                    severidad="MAYOR",
                    regla="ENCABEZADO_TBLHEADER",
                    ubicacion=f"Tabla {t_idx + 1}",
                    detalle="La fila 0 no tiene <w:tblHeader/>. Si la tabla desborda, no repetirá encabezado.",
                    evidencia=None
                )

        aprobado = len(tablas_sin_header) == 0
        resultado = {
            "regla": "REPETICION_ENCABEZADO_TBLHEADER",
            "descripcion": "Configuración de repetición automática de cabecera (<w:tblHeader/>)",
            "total_tablas": total_tablas,
            "tablas_sin_header": len(tablas_sin_header),
            "tablas_afectadas": tablas_sin_header,
            "aprobado": aprobado
        }
        self.resultados_pruebas["tbl_header"] = resultado
        return resultado

    # --------------------------------------------------------------------------
    # 4. VERIFICACIÓN: Ancho de Tablas frente a Límite Portrait (8788 dxa)
    # --------------------------------------------------------------------------
    def auditar_anchos_tablas(self) -> Dict[str, Any]:
        """
        Verifica que el ancho efectivo de cada tabla respete los márgenes de página útiles
        institucionales (8788 dxa = 15.50 cm en vertical portrait).
        Calcula el ancho mediante tblW, tblGrid (gridCol sum) y tcW sum en celdas.
        """
        total_tablas = len(self.doc.tables)
        desgloses_tablas = []
        tablas_excedidas = []
        limite_efectivo = self.limite_ancho_dxa + self.tolerancia_dxa

        for t_idx, table in enumerate(self.doc.tables):
            tblPr = table._tbl.tblPr
            tblW_elem = tblPr.find(qn("w:tblW"))
            tblW_val = 0
            tblW_type = "none"
            if tblW_elem is not None:
                tblW_type = tblW_elem.get(qn("w:type"), "none")
                tblW_raw = tblW_elem.get(qn("w:w"))
                if tblW_raw and tblW_raw.isdigit():
                    tblW_val = int(tblW_raw)

            # Suma de gridCol en tblGrid
            tblGrid = table._tbl.tblGrid
            grid_sum = 0
            columnas_count = 0
            if tblGrid is not None:
                cols = tblGrid.findall(qn("w:gridCol"))
                columnas_count = len(cols)
                for col in cols:
                    w = col.get(qn("w:w"))
                    if w and w.isdigit():
                        grid_sum += int(w)

            # Suma de tcW en fila 0
            tcw_sum = 0
            if len(table.rows) > 0:
                for cell in table.rows[0].cells:
                    tcPr = cell._tc.get_or_add_tcPr()
                    tcW = tcPr.find(qn("w:tcW"))
                    if tcW is not None:
                        w = tcW.get(qn("w:w"))
                        if w and w.isdigit():
                            tcw_sum += int(w)

            # Ancho efectivo gobernante
            ancho_efectivo = max(tblW_val if tblW_type == "dxa" else 0, grid_sum, tcw_sum)
            if ancho_efectivo == 0 and tblW_val > 0:
                ancho_efectivo = tblW_val

            ancho_cm = ancho_efectivo / DXA_POR_CM
            excedido = ancho_efectivo > limite_efectivo

            info_tabla = {
                "indice_tabla": t_idx + 1,
                "columnas": columnas_count if columnas_count > 0 else len(table.columns),
                "tblW_type": tblW_type,
                "tblW_val": tblW_val,
                "grid_sum_dxa": grid_sum,
                "tcw_sum_dxa": tcw_sum,
                "ancho_efectivo_dxa": ancho_efectivo,
                "ancho_efectivo_cm": round(ancho_cm, 2),
                "excedido": excedido
            }
            desgloses_tablas.append(info_tabla)

            if excedido:
                tablas_excedidas.append(info_tabla)
                self.registrar_observacion(
                    severidad="CRITICO",
                    regla="ANCHO_TABLA_EXCEDIDO",
                    ubicacion=f"Tabla {t_idx + 1}",
                    detalle=(f"Ancho efectivo de {ancho_efectivo} dxa ({ancho_cm:.2f} cm) supera el límite "
                             f"portrait de {self.limite_ancho_dxa} dxa (15.50 cm)."),
                    evidencia=f"tblW={tblW_val}, gridCol_sum={grid_sum}, tcw_sum={tcw_sum}"
                )

        aprobado = len(tablas_excedidas) == 0
        resultado = {
            "regla": "GEOMETRIA_ANCHO_TABLAS",
            "descripcion": f"Control de ancho tabular máximo portrait (<= {self.limite_ancho_dxa} dxa / 15.50 cm)",
            "total_tablas": total_tablas,
            "limite_dxa": self.limite_ancho_dxa,
            "tablas_excedidas": len(tablas_excedidas),
            "aprobado": aprobado,
            "detalles": desgloses_tablas
        }
        self.resultados_pruebas["anchos_tablas"] = resultado
        return resultado

    # --------------------------------------------------------------------------
    # 5. VERIFICACIÓN: Escaneo de Residuos de Signos $ y LaTeX no convertido
    # --------------------------------------------------------------------------
    def auditar_residuos_latex_y_dolar(self) -> Dict[str, Any]:
        """
        Escanea exhaustivamente todos los párrafos del documento y celdas de tabla
        en búsqueda de signos de dólar ($) aislados o delimitadores LaTeX, así como
        comandos y sintaxis de subíndices/superíndices LaTeX no transformados a OMML.
        """
        residuos_detectados = []

        def inspeccionar_texto(texto: str, ubicacion: str):
            if not texto:
                return

            # 1. Búsqueda de signos de dólar ($)
            if RE_DOLLAR.search(texto):
                # Extraer fragmentos con $
                matches_dolar = [m.start() for m in RE_DOLLAR.finditer(texto)]
                for m_idx in matches_dolar:
                    inicio = max(0, m_idx - 30)
                    fin = min(len(texto), m_idx + 31)
                    snippet = texto[inicio:fin].replace("\n", " ")
                    residuos_detectados.append({
                        "tipo": "SIGNO_DOLAR",
                        "ubicacion": ubicacion,
                        "patron": "$",
                        "snippet": f"...{snippet}..."
                    })
                    self.registrar_observacion(
                        severidad="CRITICO",
                        regla="RESIDUO_SIGNO_DOLAR",
                        ubicacion=ubicacion,
                        detalle="Se detectó el carácter '$' en el texto. Probable residuo de notación matemática LaTeX.",
                        evidencia=snippet
                    )

            # 2. Búsqueda de comandos de LaTeX (ej. \frac, \sum, \alpha, \text, etc.)
            for match in RE_LATEX_COMMANDS.finditer(texto):
                cmd = match.group(0)
                inicio = max(0, match.start() - 25)
                fin = min(len(texto), match.end() + 25)
                snippet = texto[inicio:fin].replace("\n", " ")
                residuos_detectados.append({
                    "tipo": "COMANDO_LATEX",
                    "ubicacion": ubicacion,
                    "patron": cmd,
                    "snippet": f"...{snippet}..."
                })
                self.registrar_observacion(
                    severidad="CRITICO",
                    regla="RESIDUO_COMANDO_LATEX",
                    ubicacion=ubicacion,
                    detalle=f"Se detectó macro o comando LaTeX sin compilar: '{cmd}'.",
                    evidencia=snippet
                )

            # 3. Búsqueda de subíndices/superíndices LaTeX no convertidos (ej. T_{reg}, R^{2})
            for match in RE_LATEX_SUB_SUPER.finditer(texto):
                subsup = match.group(0)
                inicio = max(0, match.start() - 20)
                fin = min(len(texto), match.end() + 20)
                snippet = texto[inicio:fin].replace("\n", " ")
                residuos_detectados.append({
                    "tipo": "LATEX_SUB_SUPER",
                    "ubicacion": ubicacion,
                    "patron": subsup,
                    "snippet": f"...{snippet}..."
                })
                self.registrar_observacion(
                    severidad="CRITICO",
                    regla="RESIDUO_LATEX_SUBSUPER",
                    ubicacion=ubicacion,
                    detalle=f"Se detectó sintaxis LaTeX de subíndice o superíndice: '{subsup}'.",
                    evidencia=snippet
                )

        # Escanear párrafos del cuerpo principal
        for p_idx, p in enumerate(self.doc.paragraphs):
            # Obtener texto sin oMath (el texto en <w:t>)
            inspeccionar_texto(p.text, f"Párrafo {p_idx + 1}")

        # Escanear párrafos de celdas de tabla
        for t_idx, table in enumerate(self.doc.tables):
            for r_idx, row in enumerate(table.rows):
                for c_idx, cell in enumerate(row.cells):
                    for cp_idx, cp in enumerate(cell.paragraphs):
                        inspeccionar_texto(
                            cp.text,
                            f"Tabla {t_idx + 1}, Fila {r_idx + 1}, Celda {c_idx + 1}, Párrafo {cp_idx + 1}"
                        )

        aprobado = len(residuos_detectados) == 0
        resultado = {
            "regla": "ESCANEO_RESIDUOS_LATEX_Y_DOLAR",
            "descripcion": "Verificación de ausencia total de sintaxis LaTeX ($ o macros) en texto editable",
            "total_residuos": len(residuos_detectados),
            "aprobado": aprobado,
            "detalles": residuos_detectados
        }
        self.resultados_pruebas["residuos_latex"] = resultado
        return resultado

    # --------------------------------------------------------------------------
    # 6. VERIFICACIÓN: Censo e Inspección de Ecuaciones OMML (<m:oMath>)
    # --------------------------------------------------------------------------
    def auditar_ecuaciones_omml(self) -> Dict[str, Any]:
        """
        Censa, extrae e inspecciona la integridad de las ecuaciones matemáticas nativas
        de Microsoft Word estructuradas en OMML (<m:oMath> y <m:oMathPara>).
        Detecta operadores n-arios incompletos (<m:nary> vacíos) que renderizan cajas punteadas.
        """
        ecuaciones = []
        nary_defectuosos = []

        def procesar_parrafo_omml(p, ubicacion: str):
            omath_elements = p._p.findall(".//" + qn("m:oMath"))
            for om_idx, om in enumerate(omath_elements):
                # Extraer texto de la fórmula
                textos = [t.text for t in om.findall(".//" + qn("m:t")) if t.text]
                formula_texto = "".join(textos).strip()

                # Es bloque display (<m:oMathPara>) o inline?
                parent_tag = om.getparent().tag if om.getparent() is not None else ""
                es_display = parent_tag.endswith("oMathPara")

                # Detectar numeración de ecuación adyacente (ej. "(1)")
                texto_adyacente = p.text.strip()
                re_num = re.search(r"\((\d+)\)", texto_adyacente)
                numero_ecuacion = re_num.group(1) if re_num else None

                # Comprobar integridad de operadores <m:nary>
                naries = om.findall(".//" + qn("m:nary"))
                for nary in naries:
                    e_elem = nary.find(qn("m:e"))
                    if e_elem is not None and len(list(e_elem)) == 0 and not (e_elem.text and e_elem.text.strip()):
                        nary_defectuosos.append({
                            "ubicacion": ubicacion,
                            "formula": formula_texto
                        })
                        self.registrar_observacion(
                            severidad="MAYOR",
                            regla="OMML_NARY_VACIO",
                            ubicacion=ubicacion,
                            detalle="Nodo <m:nary> con elemento <m:e> vacío. Word mostrará un recuadro punteado de operando faltante.",
                            evidencia=formula_texto
                        )

                ecuaciones.append({
                    "indice": len(ecuaciones) + 1,
                    "ubicacion": ubicacion,
                    "numero_etiqueta": f"({numero_ecuacion})" if numero_ecuacion else "Sin número",
                    "tipo": "Display (bloque)" if es_display else "En línea (inline)",
                    "formula_texto": formula_texto,
                    "longitud_texto": len(formula_texto)
                })

        # Recorrer párrafos del documento
        for p_idx, p in enumerate(self.doc.paragraphs):
            procesar_parrafo_omml(p, f"Párrafo {p_idx + 1}")

        # Recorrer tablas (por si existieran fórmulas dentro de celdas)
        for t_idx, table in enumerate(self.doc.tables):
            for r_idx, row in enumerate(table.rows):
                for c_idx, cell in enumerate(row.cells):
                    for cp_idx, cp in enumerate(cell.paragraphs):
                        procesar_parrafo_omml(
                            cp,
                            f"Tabla {t_idx + 1}, Fila {r_idx + 1}, Celda {c_idx + 1}, Párrafo {cp_idx + 1}"
                        )

        aprobado = len(nary_defectuosos) == 0
        resultado = {
            "regla": "ECUACIONES_NATIVAS_OMML",
            "descripcion": "Censo, renderizado e integridad de fórmulas nativas OMML (<m:oMath>)",
            "total_ecuaciones": len(ecuaciones),
            "defectos_nary": len(nary_defectuosos),
            "aprobado": aprobado,
            "detalles": ecuaciones
        }
        self.resultados_pruebas["ecuaciones_omml"] = resultado
        return resultado

    # --------------------------------------------------------------------------
    # 7. VERIFICACIÓN: Párrafos Vacíos Redundantes
    # --------------------------------------------------------------------------
    def auditar_parrafos_vacios_redundantes(self) -> Dict[str, Any]:
        """
        Detecta párrafos completamente vacíos que no contienen texto, ni ecuaciones,
        ni imágenes (<w:drawing>/<w:pict>), ni campos complejos de Word (<w:fldChar>/<w:instrText>),
        ni configuraciones de sección (<w:sectPr>).
        Identifica tanto secuencias consecutivas de párrafos vacíos como párrafos vacíos innecesarios.
        """
        parrafos_vacios_cuerpo = []

        def es_parrafo_semanticamente_vacio(p) -> bool:
            # 1. Tiene texto legible?
            if p.text and p.text.strip():
                return False
            # 2. Tiene ecuaciones OMML?
            if p._p.findall(".//" + qn("m:oMath")):
                return False
            # 3. Tiene imágenes o dibujos OpenXML?
            if p._p.findall(".//" + qn("w:drawing")) or p._p.findall(".//" + qn("w:pict")):
                return False
            # 4. Tiene campos complejos de Word (TOC, número de página, SEQ)?
            if p._p.findall(".//" + qn("w:fldChar")) or p._p.findall(".//" + qn("w:instrText")):
                return False
            # 5. Tiene Structured Document Tags (TDC nativa)?
            if p._p.findall(".//" + qn("w:sdt")):
                return False
            # 6. Es el portador de propiedades de sección (<w:sectPr>)?
            if p._p.findall(".//" + qn("w:sectPr")):
                return False
            return True

        for p_idx, p in enumerate(self.doc.paragraphs):
            if es_parrafo_semanticamente_vacio(p):
                # Obtener estilo y contexto
                estilo = p.style.name if p.style else "Normal"
                parrafos_vacios_cuerpo.append({
                    "indice_parrafo": p_idx + 1,
                    "estilo": estilo
                })

        # Detectar consecutivos
        consecutivos = []
        if len(parrafos_vacios_cuerpo) > 1:
            for i in range(len(parrafos_vacios_cuerpo) - 1):
                idx1 = parrafos_vacios_cuerpo[i]["indice_parrafo"]
                idx2 = parrafos_vacios_cuerpo[i + 1]["indice_parrafo"]
                if idx2 == idx1 + 1:
                    consecutivos.append((idx1, idx2))

        # Registrar observaciones
        if consecutivos:
            for c1, c2 in consecutivos:
                self.registrar_observacion(
                    severidad="MAYOR",
                    regla="PARRAFOS_VACIOS_CONSECUTIVOS",
                    ubicacion=f"Párrafos {c1} y {c2}",
                    detalle="Párrafos vacíos consecutivos detectados. Indican saltos de línea rústicos en vez de interlineado OpenXML.",
                    evidencia=None
                )

        if parrafos_vacios_cuerpo:
            for pv in parrafos_vacios_cuerpo:
                self.registrar_observacion(
                    severidad="MENOR",
                    regla="PARRAFO_VACIO_AISLADO",
                    ubicacion=f"Párrafo {pv['indice_parrafo']}",
                    detalle="Párrafo visualmente vacío sin contenido, campos ni objetos OpenXML.",
                    evidencia=f"Estilo: {pv['estilo']}"
                )

        # Tablas: verificar celdas con párrafos vacíos redundantes (más de 1 párrafo donde alguno es vacío)
        celdas_con_parrafos_redundantes = []
        for t_idx, table in enumerate(self.doc.tables):
            for r_idx, row in enumerate(table.rows):
                for c_idx, cell in enumerate(row.cells):
                    if len(cell.paragraphs) > 1:
                        for cp_idx, cp in enumerate(cell.paragraphs):
                            if es_parrafo_semanticamente_vacio(cp):
                                celdas_con_parrafos_redundantes.append({
                                    "tabla": t_idx + 1,
                                    "fila": r_idx + 1,
                                    "celda": c_idx + 1,
                                    "parrafo": cp_idx + 1
                                })
                                self.registrar_observacion(
                                    severidad="MENOR",
                                    regla="CELDA_PARRAFO_VACIO_REDUNDANTE",
                                    ubicacion=f"Tabla {t_idx + 1}, Fila {r_idx + 1}, Celda {c_idx + 1}",
                                    detalle=f"Párrafo {cp_idx + 1} vacío redundante dentro de una celda con múltiples párrafos.",
                                    evidencia=None
                                )

        # Criterio de aprobación: No debe haber párrafos vacíos consecutivos ni párrafos vacíos redundantes
        aprobado = len(consecutivos) == 0 and len(parrafos_vacios_cuerpo) == 0

        resultado = {
            "regla": "PARRAFOS_VACIOS_REDUNDANTES",
            "descripcion": "Verificación de ausencia de párrafos vacíos y saltos de línea no semánticos",
            "parrafos_vacios_cuerpo": len(parrafos_vacios_cuerpo),
            "secuencias_consecutivas": len(consecutivos),
            "celdas_con_redundancias": len(celdas_con_parrafos_redundantes),
            "aprobado": aprobado,
            "detalles": {
                "vacios": parrafos_vacios_cuerpo,
                "consecutivos": consecutivos,
                "celdas": celdas_con_parrafos_redundantes
            }
        }
        self.resultados_pruebas["parrafos_vacios"] = resultado
        return resultado

    # --------------------------------------------------------------------------
    # 8. VERIFICACIÓN: Presencia y Poblado de Índices Nativos (TOC, Tablas, Figuras)
    # --------------------------------------------------------------------------
    def auditar_indices_nativos(self) -> Dict[str, Any]:
        """
        Regla 8: Presencia y Poblado de Índices Nativos (TOC, Lista de Tablas, Lista de Figuras).
        Comprueba que los bloques de índices nativos existan y contengan entradas pobladas
        con sus respectivos números de página y puntos de relleno tras la renderización de Word COM:
          - Tabla de Contenido (<w:sdt> con docPartGallery "Table of Contents"): >= 50 entradas pobladas.
          - Lista de Tablas (campo TOC \\h \\z \\c "Tabla" / estilo table of figures): >= 18 entradas pobladas.
          - Lista de Figuras (campo TOC \\h \\z \\c "Figura" / estilo table of figures): >= 19 entradas pobladas.
        """
        # 1. Inspeccionar Tabla de Contenidos (<w:sdt> con docPartGallery "Table of Contents")
        sdts = self.doc.element.findall('.//' + qn('w:sdt'))
        toc_sdt = None
        for sdt in sdts:
            gallery = sdt.find('.//' + qn('w:docPartGallery'))
            if gallery is not None and gallery.get(qn('w:val')) == 'Table of Contents':
                toc_sdt = sdt
                break

        entradas_toc_texto = []
        if toc_sdt is None:
            self.registrar_observacion(
                severidad="CRITICO",
                regla="TOC_SDT_FALTANTE",
                ubicacion="Preliminares: Índice de Contenido",
                detalle="No se encontró el elemento <w:sdt> para la Tabla de Contenido nativa."
            )
        else:
            content = toc_sdt.find(qn('w:sdtContent'))
            if content is not None:
                paras = content.findall(qn('w:p'))
                for p in paras:
                    txt = "".join(p.itertext()).strip()
                    if txt:
                        entradas_toc_texto.append(txt)

            if len(entradas_toc_texto) == 0:
                self.registrar_observacion(
                    severidad="CRITICO",
                    regla="INDICE_CONTENIDO_VACIO",
                    ubicacion="Preliminares: Índice de Contenido",
                    detalle="Índice de Contenido vacío: no contiene entradas pobladas ni números de página en el documento guardado."
                )
            elif len(entradas_toc_texto) < 50:
                self.registrar_observacion(
                    severidad="MAYOR",
                    regla="INDICE_CONTENIDO_INCOMPLETO",
                    ubicacion="Preliminares: Índice de Contenido",
                    detalle=f"Índice de Contenido incompleto: solo contiene {len(entradas_toc_texto)} entradas pobladas (esperado >= 50)."
                )

        # 2. Inspeccionar Listas de Ilustraciones (Tablas y Figuras)
        entradas_tablas = []
        entradas_figuras = []
        en_indice_tablas = False
        en_indice_figuras = False

        for p in self.doc.paragraphs:
            txt = p.text.strip()
            if "ÍNDICE DE TABLAS" in txt.upper():
                en_indice_tablas = True
                en_indice_figuras = False
                continue
            elif "ÍNDICE DE FIGURAS" in txt.upper():
                en_indice_tablas = False
                en_indice_figuras = True
                continue
            elif (en_indice_tablas or en_indice_figuras) and (txt.startswith("INTRODUCCIÓN") or "CAPÍTULO" in txt.upper()):
                en_indice_tablas = False
                en_indice_figuras = False
                continue

            if en_indice_tablas:
                estilo = (p.style.name or "").lower()
                pStyle = p._p.find('.//' + qn('w:pStyle'))
                val_style = (pStyle.get(qn('w:val')) or "").lower() if pStyle is not None else ""
                if txt and (txt.startswith("Tabla ") or "table of figures" in estilo or "tabladeilustraciones" in val_style):
                    entradas_tablas.append(txt)
            elif en_indice_figuras:
                estilo = (p.style.name or "").lower()
                pStyle = p._p.find('.//' + qn('w:pStyle'))
                val_style = (pStyle.get(qn('w:val')) or "").lower() if pStyle is not None else ""
                if txt and (txt.startswith("Figura ") or "table of figures" in estilo or "tabladeilustraciones" in val_style):
                    entradas_figuras.append(txt)

        if len(entradas_tablas) == 0:
            self.registrar_observacion(
                severidad="CRITICO",
                regla="INDICE_TABLAS_VACIO",
                ubicacion="Preliminares: Índice de Tablas",
                detalle="Índice de Tablas vacío: no contiene entradas de tablas pobladas ni números de página."
            )
        elif len(entradas_tablas) < 18:
            self.registrar_observacion(
                severidad="MAYOR",
                regla="INDICE_TABLAS_INCOMPLETO",
                ubicacion="Preliminares: Índice de Tablas",
                detalle=f"Índice de Tablas incompleto: detectadas {len(entradas_tablas)} entradas (esperadas 18)."
            )

        if len(entradas_figuras) == 0:
            self.registrar_observacion(
                severidad="CRITICO",
                regla="INDICE_FIGURAS_VACIO",
                ubicacion="Preliminares: Índice de Figuras",
                detalle="Índice de Figuras vacío: no contiene entradas de figuras pobladas ni números de página."
            )
        elif len(entradas_figuras) < 19:
            self.registrar_observacion(
                severidad="MAYOR",
                regla="INDICE_FIGURAS_INCOMPLETO",
                ubicacion="Preliminares: Índice de Figuras",
                detalle=f"Índice de Figuras incompleto: detectadas {len(entradas_figuras)} entradas (esperadas 19)."
            )

        aprobado = (toc_sdt is not None and len(entradas_toc_texto) >= 50 and
                    len(entradas_tablas) >= 18 and len(entradas_figuras) >= 19)

        resultado = {
            "regla": "INDICES_NATIVOS_POBLADOS",
            "descripcion": "Verificación de presencia y poblado de TOC, Lista de Tablas y Lista de Figuras",
            "toc_presente": toc_sdt is not None,
            "toc_entradas": len(entradas_toc_texto),
            "tablas_entradas": len(entradas_tablas),
            "figuras_entradas": len(entradas_figuras),
            "aprobado": aprobado,
            "detalles": {
                "toc_muestra": entradas_toc_texto[:5],
                "tablas_muestra": entradas_tablas[:3],
                "figuras_muestra": entradas_figuras[:3]
            }
        }
        self.resultados_pruebas["indices_nativos"] = resultado
        return resultado

    # --------------------------------------------------------------------------
    # EJECUCIÓN MAESTRA DE TODAS LAS AUDITORÍAS
    # --------------------------------------------------------------------------
    def auditar_todo(self) -> Dict[str, Any]:
        """Ejecuta en secuencia la totalidad del paquete de pruebas."""
        self.observaciones.clear()
        self.resultados_pruebas.clear()

        self.auditar_tablas_flotantes()
        self.auditar_cant_split()
        self.auditar_tbl_header()
        self.auditar_anchos_tablas()
        self.auditar_residuos_latex_y_dolar()
        self.auditar_ecuaciones_omml()
        self.auditar_parrafos_vacios_redundantes()
        self.auditar_indices_nativos()

        # Conteo de severidades
        criticos = sum(1 for o in self.observaciones if o["severidad"] == "CRITICO")
        mayores = sum(1 for o in self.observaciones if o["severidad"] == "MAYOR")
        menores = sum(1 for o in self.observaciones if o["severidad"] == "MENOR")

        # Estado global: Aprobado si no existen observaciones críticas ni mayores
        estado_aprobado = (criticos == 0 and mayores == 0)

        resumen_final = {
            "archivo": self.ruta_docx,
            "tamano_kb": round(self.tamano_bytes / 1024, 2),
            "total_parrafos": len(self.doc.paragraphs),
            "total_tablas": len(self.doc.tables),
            "total_secciones": len(self.doc.sections),
            "aprobado": estado_aprobado,
            "conteo_severidad": {
                "criticos": criticos,
                "mayores": mayores,
                "menores": menores,
                "total": len(self.observaciones)
            },
            "pruebas": self.resultados_pruebas,
            "observaciones": self.observaciones
        }
        return resumen_final


# ==============================================================================
# FORMATEO DE SALIDA EN TERMINAL
# ==============================================================================

def imprimir_informe_consola(resumen: Dict[str, Any], verbose: bool = False):
    """Genera un reporte visual estructurado y formal en la consola."""
    sep_ancho = 80
    linea_doble = "=" * sep_ancho
    linea_simple = "-" * sep_ancho

    print("\n" + linea_doble)
    print("SIVAC-THESIS-LAB: INFORME DE VALIDACIÓN Y AUDITORÍA OPENXML DOCX")
    print("Universidad Nacional José María Arguedas (UNAJMA) - EPIS")
    print(linea_doble)

    print(f"Archivo analizado : {resumen['archivo']}")
    print(f"Tamaño en disco   : {resumen['tamano_kb']} KB")
    print(f"Estructura docx   : {resumen['total_secciones']} secciones | {resumen['total_parrafos']} párrafos | {resumen['total_tablas']} tablas")
    print(linea_simple)

    pruebas = resumen["pruebas"]

    # 1. Tablas Flotantes
    p1 = pruebas["tablas_flotantes"]
    st1 = "[OK] APROBADO" if p1["aprobado"] else "[FALLO] CRÍTICO"
    print(f"1. Ausencia de Tablas Flotantes (<w:tblpPr>)      : {st1}")
    print(f"   -> Tablas evaluadas: {p1['total_tablas']} | Flotantes detectadas: {p1['tablas_flotantes']}")

    # 2. Filas Indivisibles (cantSplit)
    p2 = pruebas["cant_split"]
    st2 = "[OK] APROBADO" if p2["aprobado"] else "[FALLO] MAYOR"
    print(f"2. Indivisibilidad de Filas (<w:cantSplit/>)       : {st2}")
    print(f"   -> Filas con cantSplit: {p2['filas_con_cantsplit']}/{p2['total_filas']} | Tablas afectadas: {p2['tablas_afectadas']}")

    # 3. Encabezados Repetibles (tblHeader)
    p3 = pruebas["tbl_header"]
    st3 = "[OK] APROBADO" if p3["aprobado"] else "[FALLO] MAYOR"
    print(f"3. Encabezados Repetibles (<w:tblHeader/>)         : {st3}")
    print(f"   -> Tablas evaluadas: {p3['total_tablas']} | Tablas sin cabecera: {p3['tablas_sin_header']}")

    # 4. Ancho Geométrico de Tablas
    p4 = pruebas["anchos_tablas"]
    st4 = "[OK] APROBADO" if p4["aprobado"] else "[FALLO] CRÍTICO"
    max_ancho = max([t["ancho_efectivo_dxa"] for t in p4["detalles"]]) if p4["detalles"] else 0
    max_cm = max_ancho / DXA_POR_CM
    print(f"4. Límite Portrait de Tablas (<= {p4['limite_dxa']} dxa / 15.5 cm): {st4}")
    print(f"   -> Ancho máximo detectado: {max_ancho} dxa ({max_cm:.2f} cm) | Tablas excedidas: {p4['tablas_excedidas']}")

    # 5. Residuos LaTeX y Dólares
    p5 = pruebas["residuos_latex"]
    st5 = "[OK] APROBADO" if p5["aprobado"] else "[FALLO] CRÍTICO"
    print(f"5. Ausencia de Sintaxis LaTeX y Signos '$'       : {st5}")
    print(f"   -> Residuos detectados en texto editable: {p5['total_residuos']}")

    # 6. Ecuaciones OMML
    p6 = pruebas["ecuaciones_omml"]
    st6 = "[OK] APROBADO" if p6["aprobado"] else "[FALLO] MAYOR"
    print(f"6. Fórmulas Nativas OMML (<m:oMath>)               : {st6}")
    print(f"   -> Ecuaciones censadas: {p6['total_ecuaciones']} | Defectos n-arios (<m:nary>): {p6['defectos_nary']}")

    # 7. Párrafos Vacíos
    p7 = pruebas["parrafos_vacios"]
    st7 = "[OK] APROBADO" if p7["aprobado"] else "[OBSERVACIÓN]"
    print(f"7. Control de Párrafos Vacíos Redundantes         : {st7}")
    print(f"   -> Párrafos vacíos: {p7['parrafos_vacios_cuerpo']} | Consecutivos: {p7['secuencias_consecutivas']} | Redundancias tabla: {p7['celdas_con_redundancias']}")

    # 8. Índices Nativos Poblados
    p8 = pruebas.get("indices_nativos")
    if p8:
        st8 = "[OK] APROBADO" if p8["aprobado"] else "[FALLO] CRÍTICO"
        print(f"8. Índices Nativos Poblados (TOC, Tablas, Figuras): {st8}")
        print(f"   -> TOC: {p8['toc_entradas']} entradas | Tablas: {p8['tablas_entradas']}/18 | Figuras: {p8['figuras_entradas']}/19")

    print(linea_simple)

    # Detalle de ecuaciones encontradas si verbose o general
    if p6["total_ecuaciones"] > 0 and (verbose or p6["defectos_nary"] > 0):
        print("\n[+] DETALLE DE ECUACIONES OMML CENSADAS:")
        for eq in p6["detalles"]:
            etiqueta = eq["numero_etiqueta"]
            tipo = eq["tipo"]
            ub = eq["ubicacion"]
            txt = eq["formula_texto"][:65] + ("..." if len(eq["formula_texto"]) > 65 else "")
            print(f"    - Eq {eq['indice']:02d} {etiqueta:<10} [{tipo} en {ub}]: {txt}")
        print(linea_simple)

    # Detalle de tablas si verbose
    if verbose and p4["detalles"]:
        print("\n[+] GEOMETRÍA DE TODAS LAS TABLAS:")
        print(f"    {'Tabla':<8} {'Cols':<6} {'tblW':<10} {'gridCol':<12} {'tcW sum':<12} {'Ancho Efec':<14} {'Estado':<10}")
        print("    " + "-" * 72)
        for t in p4["detalles"]:
            st_t = "EXCEDE" if t["excedido"] else "OK"
            print(f"    Tabla {t['indice_tabla']:<2} {t['columnas']:<6} {t['tblW_val']:<10} {t['grid_sum_dxa']:<12} "
                  f"{t['tcw_sum_dxa']:<12} {t['ancho_efectivo_dxa']} ({t['ancho_efectivo_cm']}cm)   {st_t}")
        print(linea_simple)

    # Observaciones registradas
    obs = resumen["observaciones"]
    if obs:
        print(f"\n[!] OBSERVACIONES DETECTADAS ({len(obs)}):")
        for idx, o in enumerate(obs, start=1):
            sev = o["severidad"]
            ub = o["ubicacion"]
            det = o["detalle"]
            ev = f" | Evidencia: {o['evidencia']}" if o.get("evidencia") else ""
            print(f"    [{idx:02d}] [{sev}] en {ub}: {det}{ev}")
        print(linea_simple)

    # Veredicto
    sev_cnt = resumen["conteo_severidad"]
    print(f"\nRESUMEN DE SEVERIDAD: {sev_cnt['criticos']} Críticos | {sev_cnt['mayores']} Mayores | {sev_cnt['menores']} Menores")

    if resumen["aprobado"]:
        print("\n" + "#" * sep_ancho)
        print(">>> VEREDICTO FINAL: APROBADO (DOCUMENTO APTO PARA DEFENSA Y REVISIÓN JURADO) <<<")
        print("#" * sep_ancho + "\n")
    else:
        print("\n" + "!" * sep_ancho)
        print(">>> VEREDICTO FINAL: CON OBSERVACIONES (REQUIERE SUBSANACIÓN EDITORIAL) <<<")
        print("!" * sep_ancho + "\n")


# ==============================================================================
# PUNTO DE ENTRADA CLI
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Auditor y Validador Exhaustivo OpenXML (.docx) para SIVAC-THESIS-LAB.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python scripts/validar_docx.py salidas/documentos/informe_final_v01.docx
  python scripts/validar_docx.py salidas/documentos/informe_final_v01.docx --verbose
  python scripts/validar_docx.py salidas/documentos/informe_final_v01.docx --json
        """
    )
    parser.add_argument(
        "ruta_docx",
        type=str,
        help="Ruta al archivo .docx que se desea auditar y validar."
    )
    parser.add_argument(
        "--limite-ancho-dxa",
        type=int,
        default=ANCHO_UTIL_PORTRAIT_DXA,
        help=f"Límite máximo de ancho en dxa para tablas portrait (default: {ANCHO_UTIL_PORTRAIT_DXA} dxa / 15.50 cm)."
    )
    parser.add_argument(
        "--tolerancia-dxa",
        type=int,
        default=5,
        help="Tolerancia en dxa para redondeos de ancho (default: 5 dxa)."
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Muestra detalle exhaustivo de tablas, ecuaciones censadas y análisis pormenorizado."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emite el informe completo en formato JSON a stdout para integración en pipelines CI/CD."
    )

    args = parser.parse_args()

    try:
        auditor = AuditorDocxOpenXML(
            ruta_docx=args.ruta_docx,
            limite_ancho_dxa=args.limite_ancho_dxa,
            tolerancia_dxa=args.tolerancia_dxa,
            verbose=args.verbose
        )
        resumen = auditor.auditar_todo()

        if args.json:
            print(json.dumps(resumen, indent=2, ensure_ascii=False))
        else:
            imprimir_informe_consola(resumen, verbose=args.verbose)

        # Código de salida
        sys.exit(0 if resumen["aprobado"] else 1)

    except FileNotFoundError as e:
        print(f"[ERROR] Archivo no encontrado: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"[ERROR INESPERADO] Falla durante la auditoría: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
