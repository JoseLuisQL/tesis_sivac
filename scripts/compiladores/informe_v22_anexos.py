# -*- coding: utf-8 -*-
"""Informe final v21: anexos reales, texto coherente e índices al día.

Toma ``informe_final_v20.docx`` y lo deja concordante con el paquete de
instrumentos v18 y con el modelo de la tesis de referencia:

1. Sustituye el ANEXO 3 (tres tablas resumen por juez) por el formato real de
   validación, una hoja por juez.
2. Sustituye el ANEXO 4 (tres tablas resumen de instrumentos) por las hojas
   reales de recolección: ficha de tiempos, ficha documental (dos hojas) y
   cuestionario de satisfacción.
3. Elimina la Modalidad B del Instrumento 03 en todo el documento y ajusta la
   escala Likert a la que figura impresa en el cuestionario.
4. Reemplaza el consentimiento informado por la Carta de Autorización
   institucional, que se incorpora escaneada como ANEXO 8.
5. Renumera las tablas 49-51 a 46-48 y rehace los tres índices (contenido,
   figuras y tablas) con la paginación real del PDF.

El rehacer de los índices se hace en dos pasadas: se compone el DOCX, se
renderiza con LibreOffice, se leen del PDF las páginas donde cae cada título
y se escriben esos números en los campos PAGEREF del DOCX. El PDF final se
exporta de ese DOCX, de modo que índice y cuerpo coinciden.

Uso
---
    python scripts/compiladores/informe_v21_anexos.py
    python scripts/compiladores/informe_v21_anexos.py --sin-pdf
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
from copy import deepcopy
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts" / "compiladores"))

import instrumentos_recoleccion_v18_builder as INS  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Cm, Pt  # noqa: E402

ENTRADA = RAIZ / "salidas" / "documentos" / "informe_final_v20.docx"
SALIDA = RAIZ / "salidas" / "documentos" / "informe_final_v22.docx"
PDF = RAIZ / "salidas" / "documentos" / "informe_final_v22.pdf"
CARTA = RAIZ / "CARTA-DE-AUTORIZACION.pdf"

ANCHO_UTIL = 15.5
BM_ANEXO8 = "_Toc243584933"
BM_ID_ANEXO8 = "250"

ESTILOS_INDICE = ("Tabladeilustraciones", "TDC1", "TDC2", "TDC3", "TDC")


# ---------------------------------------------------------------------------
# Utilidades de texto
# ---------------------------------------------------------------------------

def _texto(par) -> str:
    """Texto del párrafo leyendo todos los ``w:t``.

    No sirve ``par.runs``: las entradas de los índices y los hipervínculos
    guardan el texto en runs anidados dentro de ``w:hyperlink``, que
    ``Paragraph.runs`` no devuelve.
    """
    el = getattr(par, "_p", par)
    return "".join(t.text or "" for t in el.iter(qn("w:t")))


def reemplazar(par, viejo: str, nuevo: str) -> bool:
    """Sustituye ``viejo`` por ``nuevo`` aunque cruce varias runs."""
    el = getattr(par, "_p", par)
    nodos = list(el.iter(qn("w:t")))
    completo = "".join(t.text or "" for t in nodos)
    if viejo not in completo:
        return False
    ini = completo.index(viejo)
    fin = ini + len(viejo)
    pos = 0
    puesto = False
    for t in nodos:
        s = t.text or ""
        a, b = pos, pos + len(s)
        pos = b
        if b <= ini or a >= fin:
            continue
        desde = max(ini, a) - a
        hasta = min(fin, b) - a
        if not puesto:
            t.text = s[:desde] + nuevo + s[hasta:]
            puesto = True
        else:
            t.text = s[:desde] + s[hasta:]
    return True


def _fijar_texto(par, texto: str) -> None:
    """Deja el texto íntegro en la primera run y vacía el resto."""
    runs = par.runs
    if not runs:
        par.add_run(texto)
        return
    runs[0].text = texto
    for r in runs[1:]:
        r.text = ""


def _parrafos(doc: Document):
    for p in doc.paragraphs:
        yield p
    for t in doc.tables:
        for fila in t.rows:
            for celda in fila.cells:
                for p in celda.paragraphs:
                    yield p


# ---------------------------------------------------------------------------
# Inserción de elementos compuestos aparte
# ---------------------------------------------------------------------------

def componer(constructor, **kwargs) -> List:
    """Ejecuta un constructor de hoja en un documento vacío y devuelve su XML."""
    doc = INS.nueva_pagina()
    constructor(doc, **kwargs)
    INS.cerrar(doc)
    cuerpo = doc.element.body
    elementos = [deepcopy(h) for h in cuerpo.iterchildren()
                 if h.tag != qn("w:sectPr")]
    _igualar_marcas(elementos)
    return elementos


def _igualar_marcas(elementos: Sequence) -> None:
    """Fija la altura de la marca de párrafo al tamaño de letra del párrafo.

    La hoja se compone con su propio ``Normal`` de 12 pt, pero al insertarla
    en la tesis cada marca de párrafo toma el ``rPr`` del estilo ``Normal`` de
    la tesis. En los párrafos vacíos que sirven de separación (``hueco``) esa
    marca manda sobre la altura de la línea y cada hoja crecía unos puntos de
    más, justo lo que hacía saltar la nota al pie a una página nueva.
    """
    for el in elementos:
        for p in el.iter(qn("w:p")):
            tamanos = [int(s.get(qn("w:val")))
                       for s in p.iter(qn("w:sz"))
                       if s.get(qn("w:val"), "").isdigit()]
            if not tamanos:
                continue
            pPr = p.find(qn("w:pPr"))
            if pPr is None:
                continue
            marca = pPr.find(qn("w:rPr"))
            if marca is None:
                marca = OxmlElement("w:rPr")
                sect = pPr.find(qn("w:sectPr"))
                if sect is not None:
                    sect.addprevious(marca)
                else:
                    pPr.append(marca)
            for etiqueta in ("w:sz", "w:szCs"):
                previo = marca.find(qn(etiqueta))
                if previo is None:
                    previo = OxmlElement(etiqueta)
                    marca.append(previo)
                previo.set(qn("w:val"), str(max(tamanos)))


def empezar_pagina(elementos: List) -> List:
    """Hace que el bloque arranque en hoja nueva.

    El salto se marca con ``pageBreakBefore`` en el primer párrafo del propio
    bloque. Anteponer un párrafo vacío costaba una línea de 15 pt y era lo
    que empujaba el pie de cada hoja (la nota y la firma) a la página
    siguiente.
    """
    bloques = list(elementos)
    for el in bloques:
        if el.tag != qn("w:p"):
            # sin párrafo donde colgar el salto: se antepone uno mínimo
            p = OxmlElement("w:p")
            pPr = OxmlElement("w:pPr")
            pPr.append(OxmlElement("w:pageBreakBefore"))
            esp = OxmlElement("w:spacing")
            esp.set(qn("w:before"), "0")
            esp.set(qn("w:after"), "0")
            esp.set(qn("w:line"), "20")
            esp.set(qn("w:lineRule"), "exact")
            pPr.append(esp)
            p.append(pPr)
            return [p] + bloques
        pPr = el.find(qn("w:pPr"))
        if pPr is None:
            pPr = OxmlElement("w:pPr")
            el.insert(0, pPr)
        if pPr.find(qn("w:pageBreakBefore")) is None:
            # pageBreakBefore debe ir antes de spacing/ind/jc en el esquema
            corte = OxmlElement("w:pageBreakBefore")
            previo = pPr.find(qn("w:spacing"))
            if previo is not None:
                previo.addprevious(corte)
            else:
                pPr.append(corte)
        break
    return bloques


# ---------------------------------------------------------------------------
# Texto del cuerpo
# ---------------------------------------------------------------------------

TEXTO_4102 = (
    "En correspondencia directa con las técnicas descritas, se diseñaron y "
    "aplicaron tres instrumentos de recolección de datos con especificaciones "
    "operativas rigurosas: (a) el Instrumento N.° 01, Ficha de Registro "
    "Cronométrico de Tiempos Operativos, estructurada con campos de control "
    "temporal y tres escenarios operativos estandarizados (REG-01: registro "
    "de ingreso de lote de vacuna; REG-02: registro de salida o "
    "transferencia; y VALE-01: emisión de vale PECOSA) con disparadores "
    "unívocos de inicio y fin de cronometraje; (b) el Instrumento N.° 02, "
    "Ficha de Auditoría y Cotejo Documental de Lotes y Kardex, conformada por "
    "ocho criterios binarios de verificación de conformidad formal emanados "
    "de las disposiciones de la Norma Técnica de Salud NTS N.° "
    "196-MINSA/DGIESP-2022 (aprobada por Resolución Ministerial N.° "
    "884-2022/MINSA) sobre gestión de la cadena de frío, regla FEFO, factores "
    "de pérdida y saldos de kardex; y (c) el Instrumento N.° 03, Cuestionario "
    "de Satisfacción del Usuario bajo el Modelo TAM, escala oficial de "
    "contrastación de la Hipótesis Específica 3, integrado por 8 ítems en "
    "escala Likert de 5 puntos (1 = Muy en desacuerdo, 2 = En desacuerdo, 3 = "
    "Indiferente, 4 = De acuerdo y 5 = Totalmente de acuerdo), distribuidos "
    "en dos dimensiones de 4 reactivos cada una: aceptación del proceso "
    "operativo (AP-01 a AP-04) y utilidad percibida para la gestión (UP-01 a "
    "UP-04), con un rango global de 8 a 40 puntos y aplicación en pretest y "
    "postest. En la Tabla 33 se sintetiza la correspondencia metodológica."
)

TEXTO_NOTA34 = (
    "Nota. El formato de evaluación disponible comprende la matriz de la "
    "variable dependiente con 12 componentes (4 campos de las dimensiones 1 y "
    "2 y 8 reactivos AP/UP) en escala experta de 1 a 4, y el cuestionario TAM "
    "con 8 reactivos en escala Likert de 1 a 5. Los coeficientes V de Aiken e "
    "IVC se calcularán con las calificaciones de los tres jueces y se "
    "reportarán en el expediente de validación (Anexo 3); el dictamen de "
    "aplicabilidad queda pendiente hasta la recepción de los informes "
    "firmados."
)

TEXTO_ETICA = (
    "En segundo lugar, se garantizó el principio de autonomía y voluntariedad "
    "mediante la Carta de Autorización N.° 001-2026-DISA APURÍMAC II/OESI, "
    "otorgada por la responsable de la Oficina de Estrategia Sanitaria de "
    "Inmunizaciones, que autoriza el acceso a los registros de movimientos de "
    "vacunas, la observación directa del proceso, la aplicación de los "
    "instrumentos y la operación piloto del sistema SIVAC (Anexo 8). La "
    "participación de los catorce operadores fue voluntaria y sus datos se "
    "mantuvieron anónimos mediante identificadores alfanuméricos correlativos "
    "(OP-01 a OP-14). Asimismo, se resguardó la confidencialidad de la "
    "información estratégica institucional, restringiendo el acceso a los "
    "registros y velando porque el estudio no involucrara datos clínicos "
    "nominales de pacientes ni menores de edad, limitándose estrictamente al "
    "control transaccional y volumétrico de lotes."
)

TEXTO_ANEXO3 = (
    "Se presentan los tres formatos de evaluación por juicio de expertos, uno "
    "por cada juez del panel. El formato valora los doce componentes del "
    "instrumento (cuatro campos de las dimensiones 1 y 2 y ocho reactivos "
    "AP/UP) en escala de 1 a 4, según pertinencia, relevancia y claridad. Los "
    "coeficientes V de Aiken e IVC se calculan a partir de las calificaciones "
    "registradas en estos formatos, una vez recibidos los tres informes "
    "firmados."
)

TEXTO_ANEXO4 = (
    "Se incluyen las hojas de recolección aplicadas en campo: la ficha de "
    "registro de tiempos (Instrumento N.° 01), la ficha de auditoría y cotejo "
    "documental (Instrumento N.° 02) y el cuestionario de satisfacción del "
    "usuario (Instrumento N.° 03). Cada hoja se imprime y se llena a mano; "
    "los identificadores OP-01 a OP-14 mantienen el anonimato y permiten "
    "aparear el pretest con el postest."
)

CAMBIOS: Sequence[Tuple[str, str]] = (
    # --- Instrumento 03: una sola modalidad, ocho ítems
    ("Para el Instrumento N.° 03, en su Modalidad A oficial de 8 ítems en "
     "escala Likert de 1 a 5",
     "Para el Instrumento N.° 03, de 8 ítems en escala Likert de 1 a 5"),
    ("y para el puntaje global de la Modalidad A sobre los 8 ítems que la "
     "integran",
     "y para el puntaje global sobre los 8 ítems que lo integran"),
    (" La Modalidad B no forma parte de esa estimación y, de reportarse "
     "su consistencia interna, se presentará como indicador descriptivo "
     "separado, sin agregación con la Modalidad A.", ""),
    ("y por el cuestionario TAM de la Modalidad A con 8 reactivos en escala "
     "Likert de 1 a 5",
     "y por el cuestionario TAM con 8 reactivos en escala Likert de 1 a 5"),
    ("Para determinar la homogeneidad interna de la Modalidad A del "
     "Cuestionario TAM",
     "Para determinar la homogeneidad interna del Cuestionario TAM"),
    ("Puntaje Global TAM (Modalidad A, escala sumativa de 8 a 40 puntos)",
     "Puntaje Global TAM (escala sumativa de 8 a 40 puntos)"),
    ("Nota. Evaluado mediante el Cuestionario TAM, Modalidad A.",
     "Nota. Evaluado mediante el Cuestionario TAM."),
    ("Nota. Evaluado con la Modalidad A del Instrumento 03.",
     "Nota. Evaluado con el Instrumento 03."),
    ("Modalidad A (oficial para HE3): 8 ítems Likert de 1 a 5, en pretest "
     "y postest, con 4 ítems para Aceptación del proceso (AP-01 a AP-04) "
     "y 4 para Utilidad percibida (UP-01 a UP-04).  Modalidad B (anexo "
     "ISO/IEC 25010:2023): 8 ítems Likert de 1 a 5, exclusivos del "
     "postest, con 4 ítems para Utilidad percibida del software (PU-01 a "
     "PU-04) y 4 para Facilidad de uso percibida (PE-01 a PE-04). No "
     "aditiva respecto de la Modalidad A.",
     "8 ítems Likert de 1 a 5, aplicados en pretest y postest, con 4 "
     "ítems para Aceptación del proceso (AP-01 a AP-04) y 4 para Utilidad "
     "percibida (UP-01 a UP-04). Dos dimensiones de 4 reactivos y un "
     "rango global de 8 a 40 puntos."),
    ("Juicio de contenido sobre el formato disponible de la Modalidad A",
     "Juicio de contenido sobre el formato disponible del Instrumento 03"),
    ("Juicio de contenido del formato disponible; resultado comunicado "
     "condicional, pendiente de cotejo",
     "Juicio de contenido del formato disponible; pendiente de las fichas "
     "firmadas por los tres jueces"),
    ("1.000 comunicado (condicional)", "Por calcular"),
    ("Sin dictamen", "Pendiente de dictamen"),
    ("Escala Global TAM (Modalidad A)", "Escala Global TAM"),
    ("Cuestionario de satisfacción y aceptación tecnológica (Inst. 03, "
     "Modalidad A)",
     "Cuestionario de satisfacción y aceptación tecnológica (Inst. 03)"),
    ("Total de la dimensión sobre los 8 ítems de la Modalidad A: 8 a 40",
     "Total de la dimensión sobre los 8 ítems: 8 a 40"),
    ("aplicación de la Modalidad A del Instrumento N.° 03 en línea base",
     "aplicación del Instrumento N.° 03 en línea base"),
    ("del cuestionario psicométrico de la Modalidad A.",
     "del cuestionario psicométrico."),
    ("Cuestionario TAM (Modalidad A, ocho ítems Likert)",
     "Cuestionario TAM (ocho ítems Likert)"),
)


def paso_texto(doc: Document) -> List[str]:
    aplicados: List[str] = []
    for p in _parrafos(doc):
        for viejo, nuevo in CAMBIOS:
            if viejo in _texto(p):
                reemplazar(p, viejo, nuevo)
                aplicados.append(viejo[:55])
    return aplicados


def paso_parrafos(doc: Document) -> None:
    """Reescritura íntegra de los párrafos cuyo texto cambia de raíz."""
    objetivos = {
        "En correspondencia directa con las técnicas descritas": TEXTO_4102,
        "Nota. El formato de evaluación disponible comprende": TEXTO_NOTA34,
        "En segundo lugar, se garantizó el principio de autonomía": TEXTO_ETICA,
    }
    for p in doc.paragraphs:
        t = _texto(p)
        for aguja, nuevo in objetivos.items():
            if t.startswith(aguja):
                _fijar_texto(p, nuevo)
                break


# ---------------------------------------------------------------------------
# Anexos
# ---------------------------------------------------------------------------

def _rango_anexo(doc: Document, inicial: str, siguiente: str) -> Tuple[int, int]:
    kids = list(doc.element.body.iterchildren())
    ini = fin = None
    for i, el in enumerate(kids):
        t = "".join(el.itertext()).strip()
        if t.startswith(inicial) and ini is None:
            ini = i
        elif t.startswith(siguiente) and ini is not None:
            fin = i
            break
    if ini is None or fin is None:
        raise RuntimeError("no se encontró el bloque %s" % inicial)
    return ini, fin


def paso_anexo3(doc: Document) -> None:
    """Rehace el ANEXO 3: una hoja real de validación por juez."""
    cuerpo = doc.element.body
    ini, fin = _rango_anexo(doc, "ANEXO 3:", "ANEXO 4:")
    kids = list(cuerpo.iterchildren())
    intro = kids[ini + 1]
    _fijar_texto_el(intro, TEXTO_ANEXO3)
    sobrantes = kids[ini + 2:fin]
    cortes = _cortes(sobrantes)
    for el in sobrantes:
        cuerpo.remove(el)

    ancla = intro
    for juez in INS.JUECES:
        bloques = empezar_pagina(
            componer(INS.pagina_validacion, juez=juez, cuerpo=12.0))
        for el in bloques:
            ancla.addnext(el)
            ancla = el
    _cerrar_seccion(cortes, ancla)


def _fijar_texto_el(p_el, texto: str) -> None:
    """Igual que _fijar_texto pero sobre un elemento XML suelto."""
    from docx.text.paragraph import Paragraph
    _fijar_texto(Paragraph(p_el, None), texto)


def _cortes(elementos: Sequence) -> List:
    """Copia los cortes de sección que vivían en el bloque borrado.

    El ANEXO 4 cierra una sección (párrafo con ``w:sectPr``); si se elimina
    junto con el resto del bloque, los anexos siguientes heredan la
    orientación de la sección anterior y el documento se desarma.
    """
    cortes = []
    for el in elementos:
        pPr = el.find(qn("w:pPr"))
        if pPr is None:
            continue
        sect = pPr.find(qn("w:sectPr"))
        if sect is not None:
            cortes.append(deepcopy(sect))
    return cortes


def _cerrar_seccion(cortes: Sequence, ancla) -> None:
    """Cuelga los cortes del último párrafo del bloque insertado.

    Un párrafo vacío propio para portar el ``w:sectPr`` añadía una línea al
    final del anexo y empujaba el título siguiente.
    """
    if not cortes or ancla.tag != qn("w:p"):
        return
    pPr = ancla.find(qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        ancla.insert(0, pPr)
    for sect in cortes:
        pPr.append(sect)


def paso_anexo4(doc: Document) -> None:
    """Rehace el ANEXO 4 con las cuatro hojas reales de recolección."""
    cuerpo = doc.element.body
    ini, fin = _rango_anexo(doc, "ANEXO 4:", "ANEXO 5:")
    kids = list(cuerpo.iterchildren())
    intro = kids[ini + 1]
    _fijar_texto_el(intro, TEXTO_ANEXO4)
    sobrantes = kids[ini + 2:fin]
    cortes = _cortes(sobrantes)
    for el in sobrantes:
        cuerpo.remove(el)

    paginas = [
        (INS.pagina_tiempos, {}),
        (INS.pagina_documental_a, {}),
        (INS.pagina_documental_b, {}),
        (INS.pagina_cuestionario, {}),
    ]
    ancla = intro
    for constructor, kwargs in paginas:
        bloques = empezar_pagina(componer(constructor, cuerpo=12.0, **kwargs))
        for el in bloques:
            ancla.addnext(el)
            ancla = el
    _cerrar_seccion(cortes, ancla)


def paso_anexo8(doc: Document) -> None:
    """Agrega el ANEXO 8 con la Carta de Autorización escaneada."""
    import fitz

    cuerpo = doc.element.body
    hijos = list(cuerpo.iterchildren())
    modelo = None
    for el in hijos:
        if "".join(el.itertext()).strip().startswith("ANEXO 7:"):
            modelo = deepcopy(el)
            break
    if modelo is None:
        raise RuntimeError("no se encontró el rótulo del ANEXO 7")
    for bm in modelo.iter(qn("w:bookmarkStart")):
        bm.set(qn("w:id"), BM_ID_ANEXO8)
        bm.set(qn("w:name"), BM_ANEXO8)
    for bm in modelo.iter(qn("w:bookmarkEnd")):
        bm.set(qn("w:id"), BM_ID_ANEXO8)
    for t in modelo.iter(qn("w:t")):
        if t.text:
            t.text = "ANEXO 8: CARTA DE AUTORIZACIÓN INSTITUCIONAL"
            break
    for t in modelo.iter(qn("w:lastRenderedPageBreak")):
        pass
    cuerpo.insert(len(hijos) - 1, modelo)

    intro = doc.add_paragraph()
    intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    intro.paragraph_format.first_line_indent = Cm(1.25)
    intro.paragraph_format.space_after = Pt(10)
    intro.paragraph_format.line_spacing = 1.5
    r = intro.add_run(
        "La Dirección de Salud Apurímac II autoriza la ejecución del proyecto, "
        "el acceso a los registros de movimientos de vacunas, la observación "
        "del proceso, la aplicación de los instrumentos y la operación piloto "
        "del sistema SIVAC en el área de inmunizaciones. El documento firmado "
        "y sellado se reproduce a continuación.")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    documento = fitz.open(CARTA)
    for i, pagina in enumerate(documento, start=1):
        pix = pagina.get_pixmap(dpi=200)
        ruta = Path(tempfile.gettempdir()) / ("carta_v22_%d.png" % i)
        pix.save(ruta)
        par = doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.space_after = Pt(0)
        par.paragraph_format.space_before = Pt(0)
        par.paragraph_format.line_spacing = 1.0
        if i > 1:
            par.paragraph_format.page_break_before = True
        # La primera hoja comparte página con el rótulo y el párrafo de
        # presentación: se reduce lo justo para que quepa entera y no quede
        # una página con cuatro líneas.
        ancho = Cm(ANCHO_UTIL) if i > 1 else Cm(ANCHO_UTIL - 1.2)
        par.add_run().add_picture(str(ruta), width=ancho)


def normalizar_saltos(doc: Document) -> int:
    """Anula el espacio anterior de los párrafos que abren página.

    Word ignora ``w:spacing/@before`` en la primera línea de una página, pero
    LibreOffice lo respeta. Con el salto de página explícito eso metía 12 pt
    de más en cada rótulo de anexo y, en las páginas apaisadas del Anexo 5,
    empujaba la nota al pie a una hoja nueva. Se deja en cero, que es lo que
    Word ya estaba mostrando.
    """
    tocados = 0
    for p in doc.paragraphs:
        if not p.paragraph_format.page_break_before:
            continue
        if p.paragraph_format.space_before:
            p.paragraph_format.space_before = Pt(0)
            tocados += 1
    return tocados


def reenumerar_tablas(doc: Document) -> None:
    """Tabla 49/50/51 -> 46/47/48 en rótulos e índice.

    En el rótulo solo se toca el campo SEQ (``\\r``) y su resultado en
    caché: el texto literal «Tabla » va aparte y reemplazarlo dejaba el
    número duplicado («Tabla 4646»). En las entradas del índice el número es
    texto suelto dentro del hipervínculo y ahí sí hay que reescribirlo.
    """
    objetivos = {49: 46, 50: 47, 51: 48}
    for p in _parrafos(doc):
        estilo = _estilo(p)
        es_indice = estilo in ESTILOS_INDICE
        hubo = False
        for instr in p._p.iter(qn("w:instrText")):
            if instr.text and "SEQ Tabla" in instr.text:
                m = re.search(r"\\r (\d+)", instr.text)
                if m and int(m.group(1)) in objetivos:
                    nuevo = objetivos[int(m.group(1))]
                    instr.text = re.sub(r"\\r \d+", r"\\r %d" % nuevo,
                                        instr.text)
                    _fijar_resultado(p, m.group(1), str(nuevo))
                    hubo = True
        if es_indice:
            for viejo, nuevo in objetivos.items():
                if re.search(r"Tabla %d\b" % viejo, _texto(p)):
                    reemplazar(p, "Tabla %d" % viejo, "Tabla %d" % nuevo)
                    hubo = True


def _estilo(p) -> Optional[str]:
    try:
        return p.style.style_id
    except Exception:
        return None


def _fijar_resultado(p, viejo: str, nuevo: str) -> None:
    """Cambia el número en caché del campo SEQ (runs de solo dígitos)."""
    for t in p._p.iter(qn("w:t")):
        if (t.text or "").strip() == viejo:
            t.text = nuevo
            return


def quitar_entradas_indice_tablas(doc: Document) -> None:
    """Quita del índice de tablas las tres entradas de instrumentos.

    Esas tablas resumen desaparecieron del ANEXO 4 al sustituirlo por las
    hojas reales; sus entradas quedaban apuntando a marcadores inexistentes.
    """
    for p in doc.paragraphs:
        if p.style is None or p.style.style_id != "Tabladeilustraciones":
            continue
        texto = _texto(p).strip()
        if texto.startswith(("Tabla 46 Instrumento N.° 01",
                             "Tabla 47 Instrumento N.° 02",
                             "Tabla 48 Instrumento N.° 03")):
            p._p.getparent().remove(p._p)


def paso_modalidad(doc: Document) -> List[str]:
    """Deja una sola modalidad del Instrumento 03 en todo el documento.

    El cuestionario impreso no distingue modalidades: 8 reactivos AP/UP en
    pretest y postest. Las celdas de las Tablas 33 y 34 conservaban el texto
    de la versión anterior, con la Modalidad B y con la nota «(Modalidad A)»
    dentro del nombre del instrumento.
    """
    arreglados: List[str] = []
    for p in _parrafos(doc):
        t = _texto(p)
        if "Modalidad B" not in t and "Modalidad A" not in t:
            continue
        if "Modalidad B" in t:
            _fijar_texto(
                p,
                "8 ítems Likert de 1 a 5, aplicados en pretest y postest, "
                "con 4 ítems para Aceptación del proceso (AP-01 a AP-04) y 4 "
                "para Utilidad percibida (UP-01 a UP-04). Dos dimensiones de "
                "4 reactivos y un rango global de 8 a 40 puntos.")
            arreglados.append("celda Modalidad B")
            continue
        for viejo, nuevo in (
            ("bajo el Modelo TAM (Modalidad A)", "bajo el Modelo TAM"),
            ("(Modalidad A, ocho ítems Likert)", "(ocho ítems Likert)"),
            ("(Modalidad A: AP y UP)", ""),
            ("(Modalidad A)", ""),
            (", Modalidad A.", "."),
            ("cuestionario TAM, Modalidad A.", "cuestionario TAM."),
            ("Modalidad A", ""),
        ):
            if viejo in _texto(p):
                reemplazar(p, viejo, nuevo)
                arreglados.append(viejo)
                break
        # limpieza de dobles espacios y espacios antes de coma o punto
        t = _texto(p)
        limpio = re.sub(r"\s{2,}", " ", t)
        limpio = re.sub(r"\s+([,.;:])", r"\1", limpio).strip()
        if limpio != t and p.runs:
            _fijar_texto(p, limpio)
    return arreglados


def agregar_entrada_toc(doc: Document) -> None:
    """Añade la entrada del ANEXO 8 al índice de contenido."""
    cuerpo = doc.element.body
    sdt = [k for k in cuerpo.iterchildren() if k.tag == qn("w:sdt")][0]
    content = sdt.find(qn("w:sdtContent"))
    entradas = [p for p in content.iterchildren() if p.tag == qn("w:p")]
    modelo = None
    for p in entradas:
        if "".join(p.itertext()).strip().startswith("ANEXO 7:"):
            modelo = p
            break
    if modelo is None:
        raise RuntimeError("no se encontró la entrada del ANEXO 7 en el índice")
    nuevo = deepcopy(modelo)
    for link in nuevo.iter(qn("w:hyperlink")):
        link.set(qn("w:anchor"), BM_ANEXO8)
    for instr in nuevo.iter(qn("w:instrText")):
        if "PAGEREF" in (instr.text or ""):
            instr.text = " PAGEREF %s \\h " % BM_ANEXO8
    primero = True
    for t in nuevo.iter(qn("w:t")):
        if primero and t.text and t.text.startswith("ANEXO 7"):
            t.text = "ANEXO 8: CARTA DE AUTORIZACIÓN INSTITUCIONAL"
            primero = False
    modelo.addnext(nuevo)


# ---------------------------------------------------------------------------
# Índices: paginación real
# ---------------------------------------------------------------------------

def _norm(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texto).strip().lower()


def titulo_entrada(p_el) -> str:
    """Texto del título de una entrada de índice (antes del tabulador).

    La primera entrada lleva delante el campo TOC, cuyo resultado es el
    propio título: por eso el primer tabulador (el de la sangría) no corta y
    sí el que precede al número de página.
    """
    trozos: List[str] = []
    for el in p_el.iter(qn("w:t"), qn("w:tab")):
        if el.tag == qn("w:tab"):
            if trozos:
                break
            continue
        if el.text:
            trozos.append(el.text)
    return "".join(trozos)


def _nodo_numero(p_el):
    """Nodo ``w:t`` que muestra el número de página de una entrada.

    Es el último texto de la entrada: en la primera conviven el campo TOC y el
    PAGEREF, y buscar tras el primer separador devolvía el propio título.
    """
    nodos = [t for t in p_el.iter(qn("w:t")) if (t.text or "").strip()]
    return nodos[-1] if nodos else None


def numero_entrada(p_el) -> Optional[str]:
    """Número cacheado del PAGEREF de una entrada de índice."""
    nodo = _nodo_numero(p_el)
    return nodo.text.strip() if nodo is not None else None


def fijar_numero(p_el, valor: str) -> bool:
    nodo = _nodo_numero(p_el)
    if nodo is None:
        return False
    nodo.text = valor
    return True


def entradas_indice(doc: Document) -> List:
    cuerpo = doc.element.body
    salida = []
    for el in cuerpo.iterchildren():
        if el.tag == qn("w:sdt"):
            content = el.find(qn("w:sdtContent"))
            for p in content.iterchildren():
                if p.tag == qn("w:p"):
                    salida.append(p)
            continue
        if el.tag != qn("w:p"):
            continue
        pPr = el.find(qn("w:pPr"))
        if pPr is None or pPr.find(qn("w:pStyle")) is None:
            continue
        est = pPr.find(qn("w:pStyle")).get(qn("w:val"))
        if est in ESTILOS_INDICE:
            salida.append(el)
    return salida


def _folio(pagina) -> Optional[str]:
    """Número impreso de la página: cabecera en el cuerpo, pie en los
    preliminares. El índice de la tesis numera con ese folio, no con la
    posición del PDF (las portadas y los preliminares no llevan número)."""
    alto = pagina.rect.height
    for banda in ((0, alto * 0.09), (alto * 0.9, alto)):
        for bloque in pagina.get_text("blocks"):
            if bloque[1] < banda[0] or bloque[3] > banda[1]:
                continue
            texto = bloque[4].strip()
            if re.fullmatch(r"\d{1,4}", texto):
                return texto
    return None


def paginas_por_titulo(pdf: Path, titulos: Sequence[str]) -> Dict[str, str]:
    import fitz

    doc = fitz.open(pdf)
    paginas = [_norm(p.get_text()) for p in doc]
    folios = [_folio(p) for p in doc]
    doc.close()
    resultado: Dict[str, str] = {}
    for titulo in titulos:
        clave = _norm(titulo)
        if not clave:
            continue
        for i in range(len(paginas) - 1, -1, -1):
            if clave and clave in paginas[i] and folios[i]:
                resultado[titulo] = folios[i]
                break
        else:
            # reintento con el arranque del título (títulos muy largos)
            corto = clave[:60]
            if corto:
                for i in range(len(paginas) - 1, -1, -1):
                    if corto in paginas[i] and folios[i]:
                        resultado[titulo] = folios[i]
                        break
    return resultado


def refrescar_indices(doc: Document, pdf_referencia: Path) -> Dict[str, str]:
    entradas = entradas_indice(doc)
    titulos = [titulo_entrada(e) for e in entradas]
    paginas = paginas_por_titulo(pdf_referencia, titulos)
    cambios: Dict[str, str] = {}
    for el, titulo in zip(entradas, titulos):
        actual = numero_entrada(el)
        if actual is None or not actual.strip().isdigit():
            continue  # materia preliminar en números romanos
        nueva = paginas.get(titulo)
        if nueva is None:
            continue
        if nueva != actual.strip():
            fijar_numero(el, nueva)
            cambios[titulo] = "%s -> %s" % (actual.strip(), nueva)
    return cambios


# ---------------------------------------------------------------------------
# LibreOffice
# ---------------------------------------------------------------------------

def _soffice() -> str:
    for cand in ("soffice", "libreoffice"):
        ruta = shutil.which(cand)
        if ruta:
            return ruta
    raise RuntimeError("no se encontró LibreOffice")


def convertir(docx: Path, pdf: Path, timeout: int = 1200) -> None:
    perfil = "file:///tmp/lo_profile_v22"
    subprocess.run(
        [_soffice(), "-env:UserInstallation=" + perfil, "--headless",
         "--norestore", "--convert-to", "pdf", "--outdir", str(pdf.parent),
         str(docx)],
        check=True, timeout=timeout, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)
    producido = pdf.parent / (docx.stem + ".pdf")
    if producido != pdf:
        producido.replace(pdf)


def marcar_actualizacion(doc: Document) -> None:
    ajustes = doc.settings.element
    if ajustes.find(qn("w:updateFields")) is None:
        el = OxmlElement("w:updateFields")
        el.set(qn("w:val"), "true")
        ajustes.append(el)


# ---------------------------------------------------------------------------
# Verificación
# ---------------------------------------------------------------------------

def verificar(pdf: Path, doc: Document) -> List[str]:
    """Compara el número impreso en cada índice con la página real."""
    import fitz

    documento = fitz.open(pdf)
    paginas = [_norm(p.get_text()) for p in documento]
    folios = [_folio(p) for p in documento]
    problemas: List[str] = []
    for el in entradas_indice(doc):
        titulo = titulo_entrada(el)
        impreso = numero_entrada(el)
        if not titulo or impreso is None or not impreso.strip().isdigit():
            continue
        clave = _norm(titulo)
        real = None
        for i in range(len(paginas) - 1, -1, -1):
            if clave and clave in paginas[i]:
                real = folios[i]
                break
        if real is None:
            continue
        if real != impreso.strip():
            problemas.append("%s: índice %s, real %s" % (titulo[:60], impreso, real))
    documento.close()
    return problemas


# ---------------------------------------------------------------------------
# Principal
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin-pdf", action="store_true")
    args = ap.parse_args()

    doc = Document(ENTRADA)
    paso_parrafos(doc)
    aplicados = paso_texto(doc)
    print("cambios de texto:", len(aplicados))
    print("modalidad unificada:", len(paso_modalidad(doc)))
    normalizar_saltos(doc)
    paso_anexo3(doc)
    paso_anexo4(doc)
    quitar_entradas_indice_tablas(doc)
    reenumerar_tablas(doc)
    paso_anexo8(doc)
    agregar_entrada_toc(doc)
    marcar_actualizacion(doc)
    doc.save(SALIDA)
    print("guardado", SALIDA)
    if args.sin_pdf:
        return

    with tempfile.TemporaryDirectory() as tmp:
        ref = Path(tmp) / "referencia.pdf"
        convertir(SALIDA, ref)
        doc2 = Document(SALIDA)
        cambios = refrescar_indices(doc2, ref)
        print("entradas de índice corregidas:", len(cambios))
        doc2.save(SALIDA)
        convertir(SALIDA, PDF)

    final = Document(SALIDA)
    problemas = verificar(PDF, final)
    print("páginas del PDF:", len(__import__("fitz").open(PDF)))
    if problemas:
        print("desajustes de índice:", len(problemas))
        for p in problemas[:15]:
            print("  ", p)
    else:
        print("índices verificados: sin desajustes")


if __name__ == "__main__":
    main()
