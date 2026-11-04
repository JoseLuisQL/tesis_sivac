# -*- coding: utf-8 -*-
"""Paquete de instrumentos v16.

Corrige la maqueta de la v15 sin cambiar el contenido metodológico. Las
hojas siguen el orden de los anexos del modelo
``referencias/modelos_tesis/Fany_Tesis_Bachiller_2024.pdf``:

1. Rótulo del anexo: ``Anexo 4.1.`` en negrita y la descripción en redonda.
2. Un párrafo de objetivo, corto, sin subordinadas largas.
3. Bloque de identificación (rótulo en negrita, campo abierto).
4. Rejilla de captura con bandas de dimensión y columnas de ancho fijo.
5. Nota al pie de dos líneas como máximo.

Cambios respecto de la v15: las rejillas ocupan el alto útil de la hoja
(no quedan 130 pt en blanco), la escala Likert tiene columnas iguales y
centradas, el cuestionario lleva la numeración correlativa 1 a 8 junto al
código AP/UP, y las notas se reducen a la fórmula y al criterio.

Uso
---
    python scripts/compiladores/instrumentos_recoleccion_v16_builder.py
    python scripts/compiladores/instrumentos_recoleccion_v16_builder.py --solo 03 04
    python scripts/compiladores/instrumentos_recoleccion_v16_builder.py --sin-pdf
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts" / "compiladores"))

import instrumentos_recoleccion_v14_builder as base  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.shared import Cm, Pt  # noqa: E402

VERSION = "v16"
BASE = RAIZ / "salidas" / "instrumentos" / ("INSTRUMENTOS_DEFINITIVOS_" + VERSION)
DIR_PDF = BASE / "01_IMPRIMIBLES"
DIR_DOCX = BASE / "02_EDITABLES"
DIR_FUENTES = BASE / "03_FUENTES"
DIR_CONTROL = BASE / "04_CONTROL_VISUAL"

FUENTE = base.FUENTE
CUERPO = 12.0          # dentro de la tesis
CUERPO_HOJA = 11.0     # hoja suelta
TABLA = 10.0
REJILLA = 9.0
NOTA = 8.5
ANCHO = base.ANCHO     # 15,5 cm

nueva_pagina = base.nueva_pagina
cerrar = base.cerrar
salto = base.salto
nota = base.nota
tabla = base.tabla
_run = base._run


# ---------------------------------------------------------------------------
# Piezas de página
# ---------------------------------------------------------------------------

def rotulo(doc: Document, fijo: str, resto: str, cuerpo: float = CUERPO) -> None:
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(10)
    pf.line_spacing = 1.0
    pf.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    _run(p, fijo, size=cuerpo, bold=True)
    _run(p, " " + resto, size=cuerpo)


def objetivo(doc: Document, texto: str, cuerpo: float = CUERPO,
             despues: float = 12) -> None:
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.first_line_indent = Cm(0)
    pf.space_before = Pt(0)
    pf.space_after = Pt(despues)
    pf.line_spacing = 1.0
    _run(p, texto, size=cuerpo)


def hueco(doc: Document, puntos: float = 8) -> None:
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.0
    p.add_run("").font.size = Pt(puntos)


def identificacion(doc: Document, filas: Sequence[Sequence[Any]],
                   anchos: Sequence[float], size: float = 9.5,
                   altura: float = 0.80) -> None:
    tabla(doc, filas, anchos, alturas=[altura] * len(filas),
          negritas=tuple(range(len(filas))), izq=(1, 3), size=size,
          margenes=(95, 95, 30, 30))


def bloque(doc: Document, filas: Sequence[Sequence[Any]],
           anchos: Sequence[float], alturas: Sequence[Optional[float]],
           negritas: Sequence[int], izq: Sequence[int] = (),
           verticales: Sequence[Tuple[int, int, int]] = (),
           size: float = REJILLA,
           margenes: Tuple[int, int, int, int] = (75, 75, 18, 18)):
    tabla(doc, filas, anchos, alturas=alturas, negritas=negritas, izq=izq,
          verticales=verticales, size=size, margenes=margenes)


# ---------------------------------------------------------------------------
# Anexo 4.1 — Instrumento N.° 01
# ---------------------------------------------------------------------------

def pagina_tiempos(doc: Document, cuerpo: float = CUERPO) -> None:
    rotulo(doc, "Anexo 4.1.",
           "Instrumento N.° 01: ficha de registro de tiempos operativos",
           cuerpo)
    objetivo(doc,
             "El objetivo es medir el tiempo de registro de un movimiento de "
             "vacunas (T_reg) y el de emisión del vale de salida (T_vale), "
             "antes y con el SIVAC.", cuerpo, despues=16)

    identificacion(doc, [
        ["Operador (OP)", "", "Centro de acopio", ""],
        ["Fecha", "", "Momento", "[  ] Antes        [  ] Con el SIVAC"],
        ["Hoja", "____ de ____", "Observador", ""],
    ], [3.4, 4.3, 3.2, 4.6])

    hueco(doc, 16)
    filas: List[List[Any]] = [
        [("REGISTRO DEL MOVIMIENTO DE VACUNAS (T_reg)", 5, True)],
        ["N.°", "Lote o documento", "Hora de inicio", "Hora de corte",
         "T_reg (min)"],
    ]
    alturas: List[Optional[float]] = [0.55, 0.75]
    datos = [
        ("1", "REG-01. Ingreso de lote al almacén"),
        ("2", "REG-01. Ingreso de lote al almacén"),
        ("3", "REG-02. Salida o transferencia a la red"),
        ("4", "REG-02. Salida o transferencia a la red"),
    ]
    for numero, escenario in datos:
        filas.append([numero, escenario, "", "", ""])
        alturas.append(1.36)
    bloque(doc, filas, [1.1, 7.9, 2.3, 2.3, 1.9], alturas,
           negritas=(0, 1), izq=(1,))

    hueco(doc, 14)
    filas = [
        [("EMISIÓN DEL VALE DE SALIDA (T_vale)", 5, True)],
        ["N.°", "Vale PECOSA N.°", "Hora de solicitud", "Hora de emisión",
         "T_vale (min)"],
        ["1", "VALE-01", "", "", ""],
        ["2", "VALE-01", "", "", ""],
    ]
    bloque(doc, filas, [1.1, 7.9, 2.3, 2.3, 1.9],
           [0.55, 0.75, 1.36, 1.36], negritas=(0, 1))

    hueco(doc, 14)
    bloque(doc, [
        [("RESUMEN DEL OPERADOR", 3, True)],
        ["T_reg promedio (min)", "T_vale promedio (min)",
         "Mediciones válidas"],
        ["", "", ""],
    ], [5.1667] * 3, [0.50, 0.70, 1.10], negritas=(0, 1))

    hueco(doc, 14)
    bloque(doc, [
        [("OBSERVACIONES", 1, True)],
        [""], [""], [""],
    ], [ANCHO], [0.45, 1.05, 1.05, 1.05], negritas=(0,))

    hueco(doc, 4)
    nota(doc, "T_reg = hora de corte − hora de inicio. "
              "T_vale = hora de emisión − hora de solicitud. "
              "Si la operación se interrumpe, se anota el motivo y se repite "
              "la medición.", antes=8)


# ---------------------------------------------------------------------------
# Anexo 4.2 — Instrumento N.° 02
# ---------------------------------------------------------------------------

CRITERIOS: Tuple[str, ...] = (
    "Biológico", "Lote", "Vencimiento", "Cantidad", "Origen y destino",
    "Responsable", "Saldo", "Correlatividad",
)

ANCHOS_ASIENTO = [0.85, 1.75, 2.45, 2.55, 1.30, 0.95] + [0.66] * 8 + [0.98]


def _ident_documental(doc: Document, hoja: str = "____ de ____") -> None:
    identificacion(doc, [
        ["Operador (OP)", "", "Centro de acopio", ""],
        ["Periodo auditado", "del ____ al ____", "Momento",
         "[  ] Antes        [  ] Con el SIVAC"],
        ["Hoja", hoja, "Auditor", ""],
    ], [3.4, 4.3, 3.2, 4.6])


def pagina_documental_a(doc: Document, cuerpo: float = CUERPO) -> None:
    rotulo(doc, "Anexo 4.2.",
           "Instrumento N.° 02: ficha de auditoría del kardex", cuerpo)
    objetivo(doc,
             "El objetivo es verificar que cada asiento del kardex coincida "
             "con el documento que lo sustenta y obtener el porcentaje de "
             "registros sin discrepancias (RSD).", cuerpo, despues=12)
    _ident_documental(doc)

    hueco(doc, 12)
    filas: List[List[Any]] = [
        [("BLOQUE A. ASIENTOS DEL KARDEX", 15, True)],
        [("N.°", 1), ("DATOS DEL ASIENTO", 5),
         ("CRITERIOS DE CONFORMIDAD", 8), ("Conf.", 1)],
        ["", "Fecha", "Documento", "Biológico", "Lote", "Cant."] +
        [str(n) for n in range(1, 9)] + [""],
    ]
    alturas: List[Optional[float]] = [0.45, 0.55, 0.55]
    for n in range(1, 21):
        filas.append([str(n)] + [""] * 14)
        alturas.append(1.02)
    bloque(doc, filas, ANCHOS_ASIENTO, alturas, negritas=(0, 1, 2),
           izq=(2, 3), verticales=((1, 2, 0), (1, 2, 14)), size=8.6,
           margenes=(45, 45, 10, 10))

    hueco(doc, 12)
    bloque(doc, [
        ["Asientos revisados", "Asientos conformes", "RSD (%)"],
        ["", "", ""],
    ], [5.1667] * 3, [0.55, 0.90], negritas=(0,))

    hueco(doc, 12)
    bloque(doc, [
        [("OBSERVACIONES", 1, True)],
        [""], [""],
    ], [ANCHO], [0.45, 0.95, 0.95], negritas=(0,))

    nota(doc, "Criterios: 1 biológico, 2 lote, 3 vencimiento, 4 cantidad "
              "física, 5 origen y destino, 6 responsable y firma, 7 saldo "
              "aritmético, 8 correlatividad. S = conforme, N = no conforme. "
              "RSD = asientos conformes ÷ asientos revisados × 100.", antes=8)


def pagina_documental_b(doc: Document, cuerpo: float = CUERPO) -> None:
    rotulo(doc, "Anexo 4.2.",
           "Instrumento N.° 02: conciliación de despachos (continuación)",
           cuerpo)
    objetivo(doc,
             "El objetivo es comparar la cantidad programada con la entregada "
             "en cada despacho y obtener el porcentaje de concordancia "
             "programado-entregado (CPE).", cuerpo, despues=12)
    _ident_documental(doc, "2 de 2")

    hueco(doc, 12)
    anchos = [0.90, 1.85, 3.30, 2.10, 2.00, 1.90, 2.05, 1.40]
    filas: List[List[Any]] = [
        [("BLOQUE B. DESPACHOS CONCILIADOS", 8, True)],
        ["N.°", "Fecha", "Biológico", "Programado", "Entregado", "Diferencia",
         "Documento", "Conf."],
    ]
    alturas: List[Optional[float]] = [0.45, 0.70]
    for n in range(1, 15):
        filas.append([str(n)] + [""] * 7)
        alturas.append(1.30)
    bloque(doc, filas, anchos, alturas, negritas=(0, 1), izq=(2,))

    hueco(doc, 12)
    bloque(doc, [
        ["Despachos evaluados", "Despachos conformes", "CPE (%)"],
        ["", "", ""],
    ], [5.1667] * 3, [0.55, 0.90], negritas=(0,))

    hueco(doc, 12)
    bloque(doc, [
        [("OBSERVACIONES", 1, True)],
        [""], [""],
    ], [ANCHO], [0.45, 0.95, 0.95], negritas=(0,))

    nota(doc, "El despacho es conforme cuando la cantidad entregada iguala la "
              "programada y el documento coincide con el registro. "
              "CPE = despachos conformes ÷ despachos evaluados × 100.",
         antes=8)


# ---------------------------------------------------------------------------
# Anexo 4.3 — Instrumento N.° 03
# ---------------------------------------------------------------------------

REACTIVOS_AP: Tuple[Tuple[str, str], ...] = (
    ("AP-01", "El registro de los movimientos de vacunas se hace sin demoras."),
    ("AP-02", "Emitir un vale de salida toma pocos pasos."),
    ("AP-03", "La conciliación mensual de saldos resulta sencilla."),
    ("AP-04", "El trabajo diario es ordenado y cómodo."),
)

REACTIVOS_UP: Tuple[Tuple[str, str], ...] = (
    ("UP-01", "El control de vacunas mejora mi rendimiento."),
    ("UP-02", "La información llega a tiempo para decidir."),
    ("UP-03", "Los errores de vencimiento o de stock se detectan a tiempo."),
    ("UP-04", "La forma de trabajo sirve para la gestión diaria de la DISA."),
)

D1 = "Dimensión 1: aceptación del proceso (AP)"
D2 = "Dimensión 2: utilidad percibida (UP)"


def _escala_likert(doc: Document) -> None:
    filas = [
        [("ESCALA DE MEDICIÓN LIKERT", 5, True)],
        [("Nomenclatura", 5, True)],
        ["Muy en\ndesacuerdo", "En\ndesacuerdo", "Indiferente", "De acuerdo",
         "Totalmente\nde acuerdo"],
        [("Valoración", 5, True)],
        ["1", "2", "3", "4", "5"],
    ]
    tabla(doc, filas, [3.1] * 5, alturas=[0.50, 0.40, 1.05, 0.40, 0.45],
          size=REJILLA, negritas=(0, 1, 3, 4), margenes=(80, 80, 14, 14),
          centrada=True)
    base.par(doc, "Nota. Elaboración propia.", sangria=False, size=NOTA,
             despues=14, alineacion="left", interlinea=1.0)


def pagina_cuestionario(doc: Document, cuerpo: float = CUERPO) -> None:
    rotulo(doc, "Anexo 4.3.",
           "Instrumento N.° 03: cuestionario de satisfacción del usuario",
           cuerpo)
    objetivo(doc,
             "El objetivo es conocer la aceptación del proceso (AP) y la "
             "utilidad percibida (UP) del sistema SIVAC en el personal de "
             "inmunizaciones. Son ocho preguntas de respuesta anónima.",
             cuerpo, despues=12)

    identificacion(doc, [
        ["Operador (OP)", "", "Centro de acopio", ""],
        ["Fecha", "", "Momento", "[  ] Antes        [  ] Con el SIVAC"],
    ], [3.4, 4.3, 3.2, 4.6])
    hueco(doc, 14)

    _escala_likert(doc)

    anchos = [1.10, 1.30, 7.90, 1.04, 1.04, 1.04, 1.04, 1.04]
    filas: List[List[Any]] = [
        [("VARIABLE DEPENDIENTE: GESTIÓN DE MOVIMIENTOS MENSUALES DE VACUNAS",
          8, True)],
        [("N.°", 1), ("Código", 1), ("Reactivo", 1),
         ("Escala de medición (1 a 5)", 5)],
        ["", "", "", "1", "2", "3", "4", "5"],
    ]
    alturas: List[Optional[float]] = [0.60, 0.50, 0.40]
    negritas = [0, 1, 2]

    filas.append([(D1, 8, True)])
    alturas.append(0.45)
    negritas.append(len(filas) - 1)
    n = 0
    for codigo, texto in REACTIVOS_AP:
        n += 1
        filas.append([str(n), codigo, texto, "", "", "", "", ""])
        alturas.append(1.42)
    for codigo, texto in REACTIVOS_UP:
        n += 1
        if n == 5:
            filas.append([(D2, 8, True)])
            alturas.append(0.45)
            negritas.append(len(filas) - 1)
        filas.append([str(n), codigo, texto, "", "", "", "", ""])
        alturas.append(1.42)

    tabla(doc, filas, anchos, alturas=alturas, size=TABLA,
          negritas=tuple(negritas), izq=(2,),
          verticales=((1, 2, 0), (1, 2, 1)), margenes=(70, 70, 20, 20))

    nota(doc, "Elaboración propia, sobre el modelo de aceptación tecnológica "
              "de Davis (1989). Cada dimensión suma 4 ítems (4 a 20 puntos) y "
              "el total es la suma de las dos (8 a 40 puntos). Marque una sola "
              "opción por ítem.", antes=10)


# ---------------------------------------------------------------------------
# Anexo 3 — Formato de validación
# ---------------------------------------------------------------------------

DIM1 = "DIMENSIÓN 1: OPORTUNIDAD DE PROCESAMIENTO"
DIM2 = "DIMENSIÓN 2: CONSISTENCIA DOCUMENTAL"
DIM3 = "DIMENSIÓN 3: SATISFACCIÓN DEL USUARIO"

COMPONENTES: Tuple[Tuple[str, str], ...] = (
    ("Ficha 01: las horas de inicio y de corte permiten calcular el tiempo de "
     "registro (T_reg).", DIM1),
    ("Ficha 01: las horas de solicitud y de emisión permiten calcular el "
     "tiempo del vale (T_vale).", DIM1),
    ("Ficha 02: los ocho criterios verifican identificación, existencia y "
     "registro del asiento.", DIM2),
    ("Ficha 02: los bloques A y B permiten calcular el RSD y el CPE.", DIM2),
    ("AP-01. El registro de los movimientos de vacunas se hace sin demoras.",
     DIM3),
    ("AP-02. Emitir un vale de salida toma pocos pasos.", DIM3),
    ("AP-03. La conciliación mensual de saldos resulta sencilla.", DIM3),
    ("AP-04. El trabajo diario es ordenado y cómodo.", DIM3),
    ("UP-01. El control de vacunas mejora mi rendimiento.", DIM3),
    ("UP-02. La información llega a tiempo para decidir.", DIM3),
    ("UP-03. Los errores de vencimiento o de stock se detectan a tiempo.", DIM3),
    ("UP-04. La forma de trabajo sirve para la gestión diaria de la DISA.", DIM3),
)

JUECES: Tuple[Tuple[str, str, str], ...] = (
    ("1", "Ingeniero de Sistemas / software y bases de datos",
     "Magíster en Ingeniería de Sistemas"),
    ("2", "Licenciado en Enfermería / inmunizaciones y cadena de frío",
     "Magíster en Salud Pública"),
    ("3", "Metodólogo / estadística y medición cuantitativa",
     "Doctor en Ciencias de la Educación"),
)


def pagina_validacion(doc: Document, juez: Tuple[str, str, str],
                      cuerpo: float = CUERPO) -> None:
    numero, perfil, grado = juez
    rotulo(doc, "Anexo 3.",
           "Formato de validación por juicio de expertos", cuerpo)
    objetivo(doc,
             "El objetivo es valorar la pertinencia, la relevancia y la "
             "claridad de los doce componentes del instrumento. Cada "
             "componente se califica de 1 a 4: 1 no cumple y 4 cumple "
             "plenamente.", cuerpo, despues=12)

    identificacion(doc, [
        ["Juez", "N.° " + numero, "DNI", ""],
        ["Apellidos y nombres", "", "Fecha", ""],
        ["Grado académico", grado, "Especialidad", perfil],
        ["Institución", "", "Correo", ""],
    ], [3.6, 4.4, 2.5, 5.0], size=8.8, altura=0.78)

    hueco(doc, 12)
    anchos = [0.90, 6.55, 1.85, 1.85, 1.85, 2.50]
    filas: List[List[Any]] = [
        [("CERTIFICADO DE VALIDEZ DE CONTENIDO DEL INSTRUMENTO QUE MIDE LA "
          "VARIABLE DEPENDIENTE: GESTIÓN DE MOVIMIENTOS MENSUALES DE VACUNAS",
          6, True)],
        ["N.°", "Dimensión / componente", "Pertinencia\n(1 a 4)",
         "Relevancia\n(1 a 4)", "Claridad\n(1 a 4)", "Sugerencias"],
    ]
    alturas: List[Optional[float]] = [0.62, 0.72]
    negritas = [0, 1]
    previa = None
    n = 0
    for texto, dimension in COMPONENTES:
        if dimension != previa:
            filas.append([(dimension, 6, True)])
            alturas.append(0.40)
            negritas.append(len(filas) - 1)
            previa = dimension
        n += 1
        filas.append([str(n), texto, "", "", "", ""])
        alturas.append(1.02)

    bloque(doc, filas, anchos, alturas, negritas=negritas, izq=(1,),
           size=8.6, margenes=(60, 60, 14, 14))

    hueco(doc, 14)
    bloque(doc, [
        [("Observaciones y sugerencias", 1, True)],
        [""], [""],
        [("Opinión de aplicabilidad:     [  ] Aplicable        "
          "[  ] Aplicable después de corregir        [  ] No aplicable", 1)],
        [("Lugar y fecha: ____________________________        "
          "Firma: ____________________________", 1)],
    ], [ANCHO], [0.42, 0.95, 0.95, 0.50, 0.95], negritas=(0,), izq=(3, 4),
        size=9.0, margenes=(90, 90, 28, 28))

    nota(doc, "Escala: 1 no cumple, 2 cumple parcialmente, 3 cumple, "
              "4 cumple plenamente. Pertinencia: el componente mide el "
              "indicador. Relevancia: es necesario para la variable. "
              "Claridad: se comprende sin dificultad.", antes=10)


# ---------------------------------------------------------------------------
# Documentos
# ---------------------------------------------------------------------------

def doc_tiempos(cuerpo: float = CUERPO) -> Document:
    doc = nueva_pagina()
    pagina_tiempos(doc, cuerpo)
    cerrar(doc)
    return doc


def doc_documental(cuerpo: float = CUERPO) -> Document:
    doc = nueva_pagina()
    pagina_documental_a(doc, cuerpo)
    salto(doc)
    pagina_documental_b(doc, cuerpo)
    cerrar(doc)
    return doc


def doc_cuestionario(cuerpo: float = CUERPO) -> Document:
    doc = nueva_pagina()
    pagina_cuestionario(doc, cuerpo)
    cerrar(doc)
    return doc


def doc_validacion(cuerpo: float = CUERPO) -> Document:
    doc = nueva_pagina()
    for i, juez in enumerate(JUECES):
        if i:
            salto(doc)
        pagina_validacion(doc, juez, cuerpo)
    cerrar(doc)
    return doc


# ---------------------------------------------------------------------------
# Exportación
# ---------------------------------------------------------------------------

CARTA = RAIZ / "CARTA-DE-AUTORIZACION.pdf"

DOCUMENTOS: Dict[str, Tuple[str, Any]] = {
    "01_CARTA_AUTORIZACION": (
        "Carta de autorización institucional", CARTA),
    "02_FORMATO_VALIDACION": (
        "Anexo 3. Formato de validación por juicio de expertos",
        doc_validacion),
    "03_INSTRUMENTO_01_TIEMPOS": (
        "Anexo 4.1. Ficha de registro de tiempos", doc_tiempos),
    "04_INSTRUMENTO_02_DOCUMENTAL": (
        "Anexo 4.2. Ficha de auditoría documental", doc_documental),
    "05_INSTRUMENTO_03_CUESTIONARIO": (
        "Anexo 4.3. Cuestionario de satisfacción del usuario",
        doc_cuestionario),
}

PAGINAS_ESPERADAS = {
    "01_CARTA_AUTORIZACION": 2,
    "02_FORMATO_VALIDACION": 3,
    "03_INSTRUMENTO_01_TIEMPOS": 1,
    "04_INSTRUMENTO_02_DOCUMENTAL": 2,
    "05_INSTRUMENTO_03_CUESTIONARIO": 1,
}

ORDEN_PAQUETE = ("01_CARTA_AUTORIZACION", "03_INSTRUMENTO_01_TIEMPOS",
                 "04_INSTRUMENTO_02_DOCUMENTAL",
                 "05_INSTRUMENTO_03_CUESTIONARIO",
                 "02_FORMATO_VALIDACION")

LEEME = """# Instrumentos de recolección de datos (v16)

| Archivo | Contenido | Hojas |
| --- | --- | --- |
| 01_CARTA_AUTORIZACION | Permiso institucional firmado | 2 |
| 03_INSTRUMENTO_01_TIEMPOS | Ficha de registro de tiempos (T_reg y T_vale) | 1 |
| 04_INSTRUMENTO_02_DOCUMENTAL | Ficha de auditoría del kardex y de despachos | 2 |
| 05_INSTRUMENTO_03_CUESTIONARIO | Cuestionario de satisfacción del usuario (8 ítems) | 1 |
| 02_FORMATO_VALIDACION | Formato de validación por juicio de expertos, uno por juez | 3 |
| 00_PAQUETE_COMPLETO | Todos los documentos en un solo PDF, en orden de uso | 9 |

Cada hoja sigue el orden del modelo de tesis
(`referencias/modelos_tesis/Fany_Tesis_Bachiller_2024.pdf`, anexos 2 y 3):
rótulo del anexo en negrita, objetivo, bloque de identificación, rejilla de
captura y nota al pie. Times New Roman, A4, márgenes 3 / 2,5 / 2,5 / 2,5.

Los conteos coinciden con la tesis: cuatro operaciones cronometradas, dos
vales, veinte asientos de kardex, catorce despachos, ocho criterios de
conformidad y ocho reactivos AP/UP.

El paquete no incluye consentimiento informado. La Carta de Autorización es
el permiso formal de la institución.
"""


def compilar(solo: Optional[Sequence[str]] = None, con_pdf: bool = True
             ) -> Dict[str, Any]:
    import fitz

    for directorio in (DIR_PDF, DIR_DOCX, DIR_FUENTES, DIR_CONTROL):
        directorio.mkdir(parents=True, exist_ok=True)
    manifiesto: Dict[str, Any] = {
        "version": VERSION,
        "fecha": base.sello_compilacion(),
        "modelo": "referencias/modelos_tesis/Fany_Tesis_Bachiller_2024.pdf",
        "tipografia": FUENTE,
        "documentos": {},
    }
    for nombre, (descripcion, constructor) in DOCUMENTOS.items():
        if solo and not any(nombre.startswith(s) for s in solo):
            continue
        if isinstance(constructor, Path):
            pdf = DIR_PDF / f"{nombre}_{VERSION}.pdf"
            pdf.write_bytes(constructor.read_bytes())
            base.normalizar_pdf(constructor, pdf)
            entrada: Dict[str, Any] = {
                "descripcion": descripcion,
                "pdf": str(pdf.relative_to(RAIZ)),
                "sha256_pdf": base.sha256(pdf),
                "origen": str(constructor.relative_to(RAIZ)),
            }
            entrada["paginas"] = fitz.open(pdf).page_count
            base.control_visual(pdf, DIR_CONTROL)
            manifiesto["documentos"][nombre] = entrada
            print(f"{nombre}: {entrada['paginas']} p.")
            continue

        doc = constructor()
        docx = DIR_DOCX / f"{nombre}_{VERSION}.docx"
        doc.save(docx)
        base.fijar_marcas_zip(docx)
        entrada = {
            "descripcion": descripcion,
            "docx": str(docx.relative_to(RAIZ)),
            "sha256_docx": base.sha256(docx),
        }
        if con_pdf:
            pdf = DIR_PDF / f"{nombre}_{VERSION}.pdf"
            base.exportar_pdf(docx, pdf)
            paginas = fitz.open(pdf).page_count
            esperadas = PAGINAS_ESPERADAS.get(nombre)
            if esperadas and paginas != esperadas:
                print(f"  aviso: {nombre} tiene {paginas} p., se esperaban "
                      f"{esperadas}")
            entrada.update({
                "pdf": str(pdf.relative_to(RAIZ)),
                "paginas": paginas,
                "sha256_pdf": base.sha256(pdf),
            })
            base.control_visual(pdf, DIR_CONTROL)
        manifiesto["documentos"][nombre] = entrada
        print(f"{nombre}: {entrada.get('paginas', '-')} p.")

    completo = fitz.open()
    for nombre in ORDEN_PAQUETE:
        entrada = manifiesto["documentos"].get(nombre)
        if not entrada or "pdf" not in entrada:
            continue
        completo.insert_pdf(fitz.open(RAIZ / entrada["pdf"]))
    destino = DIR_PDF / f"00_PAQUETE_COMPLETO_{VERSION}.pdf"
    import tempfile
    with tempfile.TemporaryDirectory() as temporal:
        crudo = Path(temporal) / "paquete.pdf"
        metadatos = completo.metadata or {}
        metadatos["creationDate"] = base.SELLO
        metadatos["modDate"] = ""
        completo.set_metadata(metadatos)
        completo.save(crudo, garbage=4, deflate=True)
        completo.close()
        base.normalizar_pdf(crudo, destino)
    manifiesto["paquete_completo"] = {
        "pdf": str(destino.relative_to(RAIZ)),
        "paginas": fitz.open(destino).page_count,
        "sha256_pdf": base.sha256(destino),
    }
    base.control_visual(destino, DIR_CONTROL)
    print(f"00_PAQUETE_COMPLETO: {manifiesto['paquete_completo']['paginas']} p.")

    (BASE / "LEEME.md").write_text(LEEME, encoding="utf-8")
    shutil.copy2(Path(__file__), DIR_FUENTES / Path(__file__).name)
    (BASE / ("MANIFIESTO_" + VERSION + ".json")).write_text(
        json.dumps(manifiesto, ensure_ascii=False, indent=2),
        encoding="utf-8")
    return manifiesto


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solo", nargs="*")
    parser.add_argument("--sin-pdf", action="store_true")
    args = parser.parse_args()
    compilar(args.solo, con_pdf=not args.sin_pdf)


if __name__ == "__main__":
    main()
