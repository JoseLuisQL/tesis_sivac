# -*- coding: utf-8 -*-
"""Paquete de instrumentos v19.

Maqueta definitiva de las hojas de recolección, calcada del modelo de tesis
``referencias/modelos_tesis/Fany_Tesis_Bachiller_2024.pdf`` (anexos 2 y 3,
páginas 62-70):

1. Rótulo del anexo: ``Anexo 4.1.`` en negrita y el título en redonda, 12 pt.
2. Párrafo de objetivo con sangría de primera línea y interlineado 1,5, como
   el cuerpo de la tesis. Sin etiqueta «Objetivo.» y sin subordinadas largas.
3. Bloque de identificación: rótulo en negrita y campo abierto a la derecha.
4. Rejilla de captura: contorno y separadores de 0,5 pt, encabezados en
   negrita, bandas de dimensión y columnas de ancho fijo.
5. Nota al pie con la fuente y la fórmula del indicador.

Reglas de composición: Times New Roman; 12 pt en el texto, 9-10 pt en las
rejillas y 8,5 pt en las notas; A4 con márgenes 3 / 2,5 / 2,5 / 2,5 cm; sin
sombreado, sin color y sin relleno. Cada instrumento ocupa una hoja; el 02
ocupa tres (dos de asientos y una de despachos) y se puede insertar en el
cuerpo de la tesis con las mismas funciones.

Cambios respecto de la v16: se restituye la paginación (la v16 desbordaba a
dos y cuatro hojas), se elimina el texto de escenario repetido en cada fila
—va en una banda, como en el modelo— y la nota cita la fuente normativa.

Uso
---
    python scripts/compiladores/instrumentos_recoleccion_v19_builder.py
    python scripts/compiladores/instrumentos_recoleccion_v19_builder.py --solo 03 04
    python scripts/compiladores/instrumentos_recoleccion_v19_builder.py --sin-pdf
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
from docx.table import Table  # noqa: E402

VERSION = "v19"
BASE = RAIZ / "salidas" / "instrumentos" / ("INSTRUMENTOS_DEFINITIVOS_" + VERSION)
DIR_PDF = BASE / "01_IMPRIMIBLES"
DIR_DOCX = BASE / "02_EDITABLES"
DIR_FUENTES = BASE / "03_FUENTES"
DIR_CONTROL = BASE / "04_CONTROL_VISUAL"

FUENTE = base.FUENTE
CUERPO = 12.0
TABLA = 10.0
REJILLA = 9.0
NOTA = 8.5
ANCHO = base.ANCHO          # 15,5 cm

nueva_pagina = base.nueva_pagina
cerrar = base.cerrar
salto = base.salto
nota = base.nota
tabla = base.tabla
_run = base._run

MOMENTO = "[  ] Antes        [  ] Con el SIVAC"


# ---------------------------------------------------------------------------
# Piezas de página
# ---------------------------------------------------------------------------

def rotulo(doc: Document, fijo: str, resto: str, cuerpo: float = CUERPO,
           nueva_hoja: bool = False) -> None:
    """Rótulo del anexo en negrita, como en el modelo de tesis."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    if nueva_hoja:
        pf.page_break_before = True
    pf.space_before = Pt(0)
    pf.space_after = Pt(8)
    pf.line_spacing = 1.15
    pf.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    _run(p, fijo + " " + resto, size=cuerpo, bold=True)


def objetivo(doc: Document, texto: str, cuerpo: float = CUERPO,
             despues: float = 14) -> None:
    """Párrafo de objetivo: sangría de 1,25 cm e interlineado 1,5."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.first_line_indent = Cm(1.25)
    pf.space_before = Pt(0)
    pf.space_after = Pt(despues)
    pf.line_spacing = 1.5
    _run(p, texto, size=cuerpo)


def hueco(doc: Document, puntos: float = 10) -> None:
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.0
    p.add_run("").font.size = Pt(puntos)
    p.runs[0].font.name = FUENTE
    p.runs[0].font.size = Pt(puntos)


def identificacion(doc: Document, filas: Sequence[Sequence[Any]],
                   anchos: Sequence[float], size: float = 9.0,
                   altura: float = 0.72) -> Table:
    """Bloque rótulo/campo: rótulo en negrita y campo abierto."""
    return tabla(doc, filas, anchos, alturas=[altura] * len(filas),
                 negritas=tuple(range(len(filas))), izq=(1, 3), size=size,
                 margenes=(90, 90, 30, 30))


def rejilla(doc: Document, filas: Sequence[Sequence[Any]],
            anchos: Sequence[float], alturas: Sequence[Optional[float]],
            negritas: Sequence[int], izq: Sequence[int] = (),
            verticales: Sequence[Tuple[int, int, int]] = (),
            size: float = REJILLA,
            margenes: Tuple[int, int, int, int] = (70, 70, 16, 16)) -> Table:
    return tabla(doc, filas, anchos, alturas=alturas, negritas=negritas,
                 izq=izq, verticales=verticales, size=size, margenes=margenes)


# ---------------------------------------------------------------------------
# Anexo 4.1 — Instrumento N.° 01: tiempos
# ---------------------------------------------------------------------------

def pagina_tiempos(doc: Document, cuerpo: float = CUERPO) -> None:
    rotulo(doc, "Anexo 4.1.",
           "Instrumento N.° 01: ficha de registro de tiempos operativos",
           cuerpo)
    objetivo(doc,
             "El objetivo es medir el tiempo de registro de un movimiento de "
             "vacunas y el de emisión del vale de salida, antes y con el "
             "SIVAC. La ficha registra seis operaciones: tres de registro y "
             "tres de emisión del vale.", cuerpo)

    identificacion(doc, [
        ["Operador (OP)", "", "Centro de acopio", ""],
        ["Fecha", "", "Momento", MOMENTO],
        ["Observador", "", "Periodo", "del ____ al ____"],
    ], [3.0, 4.3, 3.0, 5.2])

    hueco(doc, 10)
    anchos = [1.00, 4.60, 3.70, 2.10, 2.05, 2.05]
    filas: List[List[Any]] = [
        [("REGISTRO DEL MOVIMIENTO DE VACUNAS (T_reg)", 6, True)],
        ["N.°", "Escenario y tarea observada", "Lote o documento",
         "Hora de inicio", "Hora de corte", "T_reg (min)"],
        ["1", "REG-01. Ingreso de lote al almacén (T1)", "", "", "", ""],
        ["2", "REG-02. Salida o transferencia a la red (T2)", "", "", "", ""],
        ["3", "REG-03. Redistribución a la red (T3)", "", "", "", ""],
        [("EMISIÓN DEL VALE DE SALIDA (T_vale)", 6, True)],
        ["N.°", "Escenario y tarea observada", "Vale PECOSA N.°",
         "Hora de solicitud", "Hora de emisión", "T_vale (min)"],
        ["1", "VALE-01. Vale simple para puesto de salud (T4)", "", "", "",
         ""],
        ["2", "VALE-02. Vale regular para centro de salud (T5)", "", "", "",
         ""],
        ["3", "VALE-03. Vale de reposición o contingencia (T6)", "", "", "",
         ""],
    ]
    alturas: List[Optional[float]] = [0.45, 0.92,
                                      1.20, 1.20, 1.20,
                                      0.45, 0.92,
                                      1.20, 1.20, 1.20]
    rejilla(doc, filas, anchos, alturas,
            negritas=(0, 1, 5, 6), izq=(1, 2))

    hueco(doc, 10)
    rejilla(doc, [
        [("RESUMEN DEL OPERADOR", 3, True)],
        ["T_reg promedio (min)", "T_vale promedio (min)",
         "Réplicas válidas (de 6)"],
        ["", "", ""],
    ], [5.1667] * 3, [0.42, 0.80, 0.90], negritas=(0, 1))

    hueco(doc, 10)
    rejilla(doc, [
        [("OBSERVACIONES", 1, True)],
        [""], [""], [""],
    ], [ANCHO], [0.40, 0.95, 0.95, 0.95], negritas=(0,))

    nota(doc, "Elaboración propia. T_reg = hora de corte − hora de inicio; "
              "T_vale = hora de emisión − hora de solicitud. Cada tarea se "
              "cronometra una vez; si la operación se interrumpe por una causa "
              "ajena al proceso, se anota el motivo y se repite la medición "
              "hasta completar las tres réplicas de cada indicador.",
         antes=8, size=NOTA)


# ---------------------------------------------------------------------------
# Anexo 4.2 — Instrumento N.° 02: auditoría documental
# ---------------------------------------------------------------------------

CRITERIOS: Tuple[str, ...] = (
    "Biológico", "Lote", "Vencimiento", "Cantidad", "Origen y destino",
    "Responsable", "Saldo", "Correlatividad",
)

ANCHOS_A = [0.75, 1.55, 2.55, 2.45, 1.35, 0.95] + [0.65] * 8 + [0.92]


def _ident_documental(doc: Document, hoja: str = "____ de ____") -> None:
    identificacion(doc, [
        ["Operador (OP)", "", "Centro de acopio", ""],
        ["Periodo auditado", "del ____ al ____", "Momento", MOMENTO],
        ["Hoja", hoja, "Auditor", ""],
    ], [3.0, 4.3, 3.0, 5.2])


def _tabla_asientos(doc: Document, desde: int, hasta: int,
                    alturas: Optional[Sequence[Optional[float]]] = None
                    ) -> None:
    filas: List[List[Any]] = [
        [("BLOQUE A. ASIENTOS DEL KARDEX", 15, True)],
        [("N.°", 1), ("DATOS DEL ASIENTO", 5),
         ("CRITERIOS DE CONFORMIDAD", 8), ("Conf.", 1)],
        ["", "Fecha", "Documento", "Biológico", "Lote", "Cant."] +
        [str(n) for n in range(1, 9)] + [""],
    ]
    if alturas is None:
        alturas = [0.42, 0.50, 0.50] + [0.555] * (hasta - desde + 1)
    for n in range(desde, hasta + 1):
        filas.append([str(n)] + [""] * 14)
    rejilla(doc, filas, ANCHOS_A, alturas, negritas=(0, 1, 2),
            izq=(2, 3), verticales=((1, 2, 0), (1, 2, 14)), size=8.5,
            margenes=(40, 40, 8, 8))


def pagina_documental_a(doc: Document, cuerpo: float = CUERPO) -> None:
    rotulo(doc, "Anexo 4.2.",
           "Instrumento N.° 02: ficha de auditoría del kardex", cuerpo)
    objetivo(doc,
             "El objetivo es verificar que cada asiento del kardex coincida "
             "con el documento que lo sustenta. La ficha audita cuarenta "
             "asientos por operador y momento, veinte en cada hoja, con ocho "
             "criterios de conformidad.", cuerpo, despues=10)
    _ident_documental(doc, "1 de 2 (bloque A)")

    hueco(doc, 8)
    _tabla_asientos(doc, 1, 20)

    hueco(doc, 8)
    rejilla(doc, [
        ["Asientos revisados (hoja 1)", "Asientos conformes",
         "RSD acumulado (%)"],
        ["", "", ""],
    ], [5.1667] * 3, [0.50, 0.76], negritas=(0,))

    hueco(doc, 8)
    rejilla(doc, [
        [("OBSERVACIONES", 1, True)],
        [""], [""],
    ], [ANCHO], [0.36, 0.70, 0.70], negritas=(0,))

    nota(doc, "Fuente: NTS N.° 196-MINSA/DGIESP-2022 y elaboración propia. "
              "Criterios: 1 biológico, 2 lote, 3 vencimiento, 4 cantidad "
              "física, 5 origen y destino, 6 responsable y firma, 7 saldo "
              "aritmético, 8 correlatividad. Si un criterio no se cumple, el "
              "asiento no es conforme. "
              "RSD = asientos conformes ÷ asientos revisados × 100.",
         antes=6, size=NOTA)


def pagina_documental_b(doc: Document, cuerpo: float = CUERPO,
                        nueva_hoja: bool = False) -> None:
    rotulo(doc, "Anexo 4.2.",
           "Instrumento N.° 02: ficha de auditoría del kardex "
           "(continuación)", cuerpo, nueva_hoja=nueva_hoja)
    objetivo(doc,
             "El objetivo es completar la auditoría del kardex del mismo "
             "operador y momento. Esta hoja registra los asientos 21 a 40 con "
             "los mismos ocho criterios.", cuerpo, despues=10)
    _ident_documental(doc, "2 de 2 (bloque A)")

    hueco(doc, 8)
    _tabla_asientos(doc, 21, 40)

    hueco(doc, 8)
    rejilla(doc, [
        ["Asientos revisados (total)", "Asientos conformes",
         "RSD (%)"],
        ["", "", ""],
    ], [5.1667] * 3, [0.50, 0.76], negritas=(0,))

    hueco(doc, 8)
    rejilla(doc, [
        [("OBSERVACIONES", 1, True)],
        [""], [""],
    ], [ANCHO], [0.36, 0.70, 0.70], negritas=(0,))

    nota(doc, "Elaboración propia. Las dos hojas se archivan juntas: la suma "
              "de asientos revisados de ambas debe ser cuarenta. "
              "RSD = asientos conformes ÷ asientos revisados × 100.",
         antes=6, size=NOTA)


def pagina_documental_c(doc: Document, cuerpo: float = CUERPO,
                        nueva_hoja: bool = False) -> None:
    rotulo(doc, "Anexo 4.2.",
           "Instrumento N.° 02: conciliación de despachos",
           cuerpo, nueva_hoja=nueva_hoja)
    objetivo(doc,
             "El objetivo es comparar la cantidad programada con la entregada "
             "en cada despacho del operador y momento auditados. La ficha "
             "concilia veinticinco despachos.", cuerpo, despues=10)
    _ident_documental(doc, "1 de 1 (bloque B)")

    hueco(doc, 8)
    anchos = [0.85, 1.60, 2.90, 1.95, 1.90, 1.80, 1.95, 1.35, 1.10]
    filas: List[List[Any]] = [
        [("BLOQUE B. DESPACHOS CONCILIADOS", 9, True)],
        ["N.°", "Fecha", "Biológico", "Programado", "Entregado", "Diferencia",
         "Documento", "Conf.", "Obs."],
    ]
    alturas: List[Optional[float]] = [0.40, 0.62] + [0.475] * 25
    for n in range(1, 26):
        filas.append([str(n)] + [""] * 8)
    rejilla(doc, filas, anchos, alturas, negritas=(0, 1), izq=(2,),
            size=8.0, margenes=(40, 40, 6, 6))

    hueco(doc, 8)
    rejilla(doc, [
        ["Despachos evaluados", "Despachos conformes", "CPE (%)"],
        ["", "", ""],
    ], [5.1667] * 3, [0.46, 0.66], negritas=(0,), size=8.5)

    hueco(doc, 8)
    rejilla(doc, [
        [("OBSERVACIONES", 1, True)],
        [""],
    ], [ANCHO], [0.34, 0.72], negritas=(0,), size=8.5)

    nota(doc, "Elaboración propia. El despacho es conforme cuando la cantidad "
              "entregada iguala la programada y el documento coincide con el "
              "registro; una diferencia se anota, no se corrige en la hoja. "
              "CPE = despachos conformes ÷ despachos evaluados × 100.",
         antes=6, size=NOTA)


# ---------------------------------------------------------------------------
# Anexo 4.3 — Instrumento N.° 03: cuestionario
# ---------------------------------------------------------------------------

# Enunciados transcritos literalmente de la Tabla 48 del informe final: una
# sola redacción para el cuestionario, el formato de validación y la tesis.
REACTIVOS_AP: Tuple[Tuple[str, str], ...] = (
    ("AP-01", "El procedimiento de registro de movimientos de vacunas resulta "
              "ágil y sin demoras innecesarias."),
    ("AP-02", "La emisión de comprobantes y vales de salida se realiza con "
              "facilidad y claridad en los pasos requeridos."),
    ("AP-03", "El flujo operativo para conciliar saldos mensuales reduce la "
              "fatiga y el esfuerzo administrativo."),
    ("AP-04", "Considero que la modalidad de trabajo empleada es cómoda, "
              "ordenada y eficiente para mis labores."),
)

REACTIVOS_UP: Tuple[Tuple[str, str], ...] = (
    ("UP-01", "La plataforma o método de trabajo mejora mi productividad y "
              "desempeño en el control de vacunas."),
    ("UP-02", "El sistema proporciona información precisa y oportuna para la "
              "toma de decisiones en inmunizaciones."),
    ("UP-03", "La aplicación de reglas automáticas de control (como FEFO) "
              "evita errores y vencimiento de biológicos."),
    ("UP-04", "En términos generales, considero sumamente útil la herramienta "
              "para la gestión institucional en la DISA."),
)

D1 = "Dimensión 1: Aceptación del proceso (AP)"
D2 = "Dimensión 2: Utilidad percibida (UP)"


def _escala_likert(doc: Document) -> None:
    filas = [
        [("ESCALA DE MEDICIÓN LIKERT", 5, True)],
        [("Nomenclatura", 5, True)],
        ["Muy en\ndesacuerdo", "En\ndesacuerdo", "Indiferente", "De acuerdo",
         "Totalmente\nde acuerdo"],
        [("Valoración", 5, True)],
        ["1", "2", "3", "4", "5"],
    ]
    tabla(doc, filas, [3.1] * 5, alturas=[0.48, 0.38, 0.98, 0.38, 0.45],
          size=REJILLA, negritas=(0, 1, 3, 4), margenes=(80, 80, 12, 12),
          centrada=True)
    p = base.par(doc, "Nota. Elaboración propia.", sangria=False, size=NOTA,
                 despues=12, alineacion="left", interlinea=1.0)
    p.paragraph_format.space_before = Pt(4)


def pagina_cuestionario(doc: Document, cuerpo: float = CUERPO) -> None:
    rotulo(doc, "Anexo 4.3.",
           "Instrumento N.° 03: cuestionario de satisfacción del usuario",
           cuerpo)
    objetivo(doc,
             "El objetivo es conocer la aceptación del proceso y la utilidad "
             "percibida del sistema SIVAC en el personal de inmunizaciones. "
             "Son ocho preguntas de respuesta anónima.", cuerpo, despues=12)

    identificacion(doc, [
        ["Operador (OP)", "", "Centro de acopio", ""],
        ["Fecha", "", "Momento", MOMENTO],
    ], [3.0, 4.3, 3.0, 5.2])
    hueco(doc, 12)

    _escala_likert(doc)

    anchos = [1.05, 1.35, 8.00, 1.02, 1.02, 1.02, 1.02, 1.02]
    filas: List[List[Any]] = [
        [("VARIABLE DEPENDIENTE: GESTIÓN DE MOVIMIENTOS MENSUALES DE VACUNAS",
          8, True)],
        [("N.°", 1), ("Código", 1), ("Reactivo", 1),
         ("Escala de medición (1 a 5)", 5)],
        ["", "", "", "1", "2", "3", "4", "5"],
    ]
    alturas: List[Optional[float]] = [0.55, 0.48, 0.38]
    negritas = [0, 1, 2]

    filas.append([(D1, 8, True)])
    alturas.append(0.42)
    negritas.append(len(filas) - 1)
    n = 0
    for codigo, texto in REACTIVOS_AP:
        n += 1
        filas.append([str(n), codigo, texto, "", "", "", "", ""])
        alturas.append(1.30)
    for codigo, texto in REACTIVOS_UP:
        n += 1
        if n == 5:
            filas.append([(D2, 8, True)])
            alturas.append(0.42)
            negritas.append(len(filas) - 1)
        filas.append([str(n), codigo, texto, "", "", "", "", ""])
        alturas.append(1.30)

    tabla(doc, filas, anchos, alturas=alturas, size=REJILLA,
          negritas=tuple(negritas), izq=(2,),
          verticales=((1, 2, 0), (1, 2, 1)), margenes=(65, 65, 16, 16))

    nota(doc, "Elaboración propia, sobre el modelo de aceptación tecnológica "
              "de Davis (1989). Cada dimensión suma cuatro ítems (4 a 20 "
              "puntos) y el total es la suma de las dos (8 a 40 puntos). "
              "Marque una sola opción por ítem.", antes=10, size=NOTA)


# ---------------------------------------------------------------------------
# Anexo 3 — Formato de validación por juicio de expertos
# ---------------------------------------------------------------------------

DIM1 = "DIMENSIÓN 1: OPORTUNIDAD DE PROCESAMIENTO"
DIM2 = "DIMENSIÓN 2: CONSISTENCIA DOCUMENTAL"
DIM3 = "DIMENSIÓN 3: SATISFACCIÓN DEL USUARIO"

COMPONENTES: Tuple[Tuple[str, str], ...] = (
    # Dimensión 1 y 2: los cuatro campos que sostienen T_reg, T_vale, RSD y CPE.
    ("Ficha 01. Las horas de inicio y de corte permiten calcular el tiempo "
     "de registro (T_reg).", DIM1),
    ("Ficha 01. Las horas de solicitud y de emisión permiten calcular el "
     "tiempo del vale (T_vale).", DIM1),
    ("Ficha 02. Los ocho criterios verifican identificación, existencia y "
     "registro del asiento.", DIM2),
    ("Ficha 02. Los bloques A y B permiten calcular el RSD y el CPE.", DIM2),
    # Dimensión 3: los ocho reactivos, con la redacción del cuestionario.
) + tuple((codigo + ". " + texto, DIM3)
          for codigo, texto in REACTIVOS_AP + REACTIVOS_UP)

# El grado, la especialidad y la institución los consigna cada juez al
# firmar: el formato se entrega en blanco para no atribuir credenciales que
# todavía no están acreditadas documentalmente.
JUECES: Tuple[Tuple[str, str, str], ...] = (
    ("1", "", ""),
    ("2", "", ""),
    ("3", "", ""),
)


def pagina_validacion(doc: Document, juez: Tuple[str, str, str],
                      cuerpo: float = CUERPO,
                      nueva_hoja: bool = False) -> None:
    numero, perfil, grado = juez
    rotulo(doc, "Anexo 3.",
           "Formato de validación por juicio de expertos", cuerpo,
           nueva_hoja=nueva_hoja)
    objetivo(doc,
             "El objetivo es valorar la pertinencia, la relevancia y la "
             "claridad de los doce componentes del instrumento. Cada "
             "componente se califica de 1 a 4.", cuerpo, despues=8)

    identificacion(doc, [
        ["Juez", "N.° " + numero, "DNI", ""],
        ["Apellidos y nombres", "", "Fecha", ""],
        ["Grado académico", grado, "Especialidad", perfil],
        ["Institución", "", "Correo", ""],
    ], [3.5, 4.5, 2.4, 5.1], size=8.5, altura=0.64)

    hueco(doc, 10)
    anchos = [0.80, 6.65, 1.85, 1.80, 1.60, 2.80]
    filas: List[List[Any]] = [
        [("CERTIFICADO DE VALIDEZ DE CONTENIDO DEL INSTRUMENTO QUE MIDE LA "
          "VARIABLE DEPENDIENTE: GESTIÓN DE MOVIMIENTOS MENSUALES DE VACUNAS",
          6, True)],
        ["N.°", "Dimensión / componente", "Pertinencia\n(1 a 4)",
         "Relevancia\n(1 a 4)", "Claridad\n(1 a 4)", "Sugerencias"],
    ]
    alturas: List[Optional[float]] = [0.58, 0.66]
    negritas = [0, 1]
    previa = None
    n = 0
    for texto, dimension in COMPONENTES:
        if dimension != previa:
            filas.append([(dimension, 6, True)])
            alturas.append(0.38)
            negritas.append(len(filas) - 1)
            previa = dimension
        n += 1
        filas.append([str(n), texto, "", "", "", ""])
        alturas.append(0.74)

    rejilla(doc, filas, anchos, alturas, negritas=negritas, izq=(1,),
            size=8.5, margenes=(55, 55, 12, 12))

    hueco(doc, 8)
    rejilla(doc, [
        [("Observaciones y sugerencias", 1, True)],
        [""], [""],
        [("Opinión de aplicabilidad:     [  ] Aplicable        "
          "[  ] Aplicable después de corregir        [  ] No aplicable", 1)],
        [("Lugar y fecha: __________________________        "
          "Firma: __________________________", 1)],
    ], [ANCHO], [0.34, 0.68, 0.68, 0.42, 0.70], negritas=(0,), izq=(3, 4),
        size=9.0, margenes=(90, 90, 26, 26))

    nota(doc, "Elaboración propia. Pertinencia: el componente mide el "
              "indicador. Relevancia: es necesario para medir la variable. "
              "Claridad: se comprende sin dificultad.", antes=6, size=NOTA)


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
    pagina_documental_b(doc, cuerpo, nueva_hoja=True)
    pagina_documental_c(doc, cuerpo, nueva_hoja=True)
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
        pagina_validacion(doc, juez, cuerpo, nueva_hoja=bool(i))
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
    "04_INSTRUMENTO_02_DOCUMENTAL": 3,
    "05_INSTRUMENTO_03_CUESTIONARIO": 1,
}

ORDEN_PAQUETE = ("01_CARTA_AUTORIZACION", "03_INSTRUMENTO_01_TIEMPOS",
                 "04_INSTRUMENTO_02_DOCUMENTAL",
                 "05_INSTRUMENTO_03_CUESTIONARIO",
                 "02_FORMATO_VALIDACION")

LEEME = """# Instrumentos de recolección de datos (v19)

| Archivo | Contenido | Hojas |
| --- | --- | --- |
| 01_CARTA_AUTORIZACION | Permiso institucional firmado | 2 |
| 03_INSTRUMENTO_01_TIEMPOS | Ficha de registro de tiempos (T_reg y T_vale) | 1 |
| 04_INSTRUMENTO_02_DOCUMENTAL | Ficha de auditoría del kardex (2 hojas) y de despachos (1 hoja) | 3 |
| 05_INSTRUMENTO_03_CUESTIONARIO | Cuestionario de satisfacción del usuario (8 ítems) | 1 |
| 02_FORMATO_VALIDACION | Formato de validación por juicio de expertos, uno por juez | 3 |
| 00_PAQUETE_COMPLETO | Todos los documentos en un solo PDF, en orden de uso | 10 |
| CONCORDANCIA | Trazabilidad de cada hoja con la tesis y la base de datos | 2 |

Cada hoja sigue el modelo de tesis
(`referencias/modelos_tesis/Fany_Tesis_Bachiller_2024.pdf`, anexos 2 y 3):
rótulo del anexo en negrita, párrafo de objetivo con sangría, bloque de
identificación, rejilla de captura y nota al pie. Times New Roman, A4,
márgenes 3 / 2,5 / 2,5 / 2,5 cm.

Los conteos coinciden con la tesis y con la base de datos: seis operaciones
cronometradas (tres de registro y tres de emisión del vale), cuarenta
asientos de kardex por operador y momento —veinte en cada hoja—,
veinticinco despachos por operador y momento, ocho criterios de
conformidad y ocho reactivos AP/UP.

El paquete no incluye consentimiento informado. La Carta de Autorización es
el permiso formal de la institución.
"""


def compilar(solo: Optional[Sequence[str]] = None, con_pdf: bool = True
             ) -> Dict[str, Any]:
    import fitz

    for directorio in (DIR_PDF, DIR_DOCX, DIR_FUENTES, DIR_CONTROL):
        directorio.mkdir(parents=True, exist_ok=True)
    for previo in DIR_CONTROL.glob("*.png"):
        previo.unlink()
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
