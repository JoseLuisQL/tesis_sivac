# -*- coding: utf-8 -*-
"""Informe final v29: el ANEXO 4 reproduce las hojas v22 y los códigos TRAB.

La v28 seguía imprimiendo en el anexo las hojas v21 (sin pausa, sin motivo,
sin tipo de asiento, sin columna de validez y sin observación por fila) y
rotulaba a los operadores como OP-01 a OP-14, mientras el paquete que se
imprime y se llena, el padrón, el libro de captura y los CSV usan TRAB-01 a
TRAB-14. Este paso, sin tocar redacción ni estadísticos:

1. Sustituye OP-01 a OP-14 por TRAB-01 a TRAB-14 en el texto.
2. Rehace el ANEXO 4 con las cinco hojas del paquete v22: tiempos, auditoría
   (dos hojas) y conciliación (una), y cuestionario.
3. Rehace los índices en dos pasadas con LibreOffice.

El número de páginas no cambia (cinco hojas de anexo), de modo que el índice
general se conserva; aun así se refresca y se verifica.

El módulo es autónomo: ``informe_v27_anexos`` importa el compilador v21, que a
su vez depende del motor v14 que ya no está en el repositorio. Aquí se
reproducen sólo las utilidades de inserción (rango del anexo, cortes de
sección, salto de página), aplicadas a los constructores v22.

Uso
---
    python scripts/compiladores/informe_v29_anexo4_v22.py
    python scripts/compiladores/informe_v29_anexo4_v22.py --sin-pdf
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import List, Sequence, Tuple

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts" / "compiladores"))

import indices_pdf as IDX  # noqa: E402
import instrumentos_recoleccion_v22_builder as INS  # noqa: E402
from docx import Document  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402

ENTRADA = RAIZ / "salidas" / "documentos" / "informe_final_v28.docx"
SALIDA = RAIZ / "salidas" / "documentos" / "informe_final_v29.docx"
PDF = RAIZ / "salidas" / "documentos" / "informe_final_v29.pdf"

# Párrafos donde el informe todavía rotula a los operadores con OP.
PARRAFOS_OP = (574, 640)

# Texto del ANEXO 4 de la v27, con el identificador que usan las hojas.
TEXTO_ANEXO4 = (
    "Se incluyen las hojas de recolección aplicadas en campo: la ficha de "
    "registro de tiempos (Instrumento N.° 01), con las seis tareas "
    "cronometradas; la ficha de auditoría y cotejo documental (Instrumento "
    "N.° 02), con dos hojas de veinte asientos cada una y una hoja de "
    "veinticinco despachos; y el cuestionario de satisfacción del usuario "
    "(Instrumento N.° 03). Cada hoja se imprime y se llena a mano; los "
    "identificadores TRAB-01 a TRAB-14 mantienen el anonimato y permiten "
    "aparear el pretest con el postest."
)


# ---------------------------------------------------------------------------
# Utilidades de inserción (las de la v27, sin arrastrar el motor v14)
# ---------------------------------------------------------------------------

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
    runs = par.runs
    if not runs:
        par.add_run(texto)
        return
    runs[0].text = texto
    for r in runs[1:]:
        r.text = ""


def _fijar_texto_el(p_el, texto: str) -> None:
    from docx.text.paragraph import Paragraph

    _fijar_texto(Paragraph(p_el, None), texto)


def _rango_anexo(doc: Document, inicial: str, siguiente: str) -> Tuple[int, int]:
    hijos = list(doc.element.body.iterchildren())
    ini = fin = None
    for i, el in enumerate(hijos):
        t = "".join(el.itertext()).strip()
        if t.startswith(inicial) and ini is None:
            ini = i
        elif t.startswith(siguiente) and ini is not None:
            fin = i
            break
    if ini is None or fin is None:
        raise RuntimeError("no se encontró el bloque %s" % inicial)
    return ini, fin


def _cortes(elementos: Sequence) -> List:
    """Copia los ``w:sectPr`` que vivían en el bloque borrado."""
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
    if not cortes or ancla.tag != qn("w:p"):
        return
    pPr = ancla.find(qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        ancla.insert(0, pPr)
    for sect in cortes:
        pPr.append(sect)


def _igualar_marcas(elementos: Sequence) -> None:
    """Fija la altura de la marca de párrafo al tamaño de letra del párrafo.

    Sin esto, los párrafos vacíos de separación toman la marca del ``Normal``
    de la tesis (12 pt) y cada hoja crece lo justo para empujar la nota al pie
    a una página nueva.
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


def componer(constructor) -> List:
    """Ejecuta un constructor de hoja en un documento vacío y devuelve su XML."""
    doc = INS.nueva_pagina()
    constructor(doc)
    INS.cerrar(doc)
    elementos = [deepcopy(h) for h in doc.element.body.iterchildren()
                 if h.tag != qn("w:sectPr")]
    _igualar_marcas(elementos)
    return elementos


def empezar_pagina(elementos: List) -> List:
    """Marca el primer párrafo del bloque con ``pageBreakBefore``."""
    bloques = list(elementos)
    for el in bloques:
        if el.tag != qn("w:p"):
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
            pPr.insert(0, OxmlElement("w:pageBreakBefore"))
        return bloques
    return bloques


# ---------------------------------------------------------------------------
# Pasos
# ---------------------------------------------------------------------------

def paso_codigos(doc: Document) -> None:
    """Alinea el identificador del informe con el del padrón y las hojas."""
    for indice in PARRAFOS_OP:
        if not reemplazar(doc.paragraphs[indice], "OP-01 a OP-14",
                          "TRAB-01 a TRAB-14"):
            raise SystemExit("no se encontró «OP-01 a OP-14» en el párrafo %d"
                             % indice)


def paso_anexo4(doc: Document) -> None:
    """Rehace el ANEXO 4 con las cinco hojas del paquete v22."""
    cuerpo = doc.element.body
    ini, fin = _rango_anexo(doc, "ANEXO 4:", "ANEXO 5:")
    hijos = list(cuerpo.iterchildren())
    intro = hijos[ini + 1]
    _fijar_texto_el(intro, TEXTO_ANEXO4)
    sobrantes = hijos[ini + 2:fin]
    cortes = _cortes(sobrantes)
    for el in sobrantes:
        cuerpo.remove(el)

    paginas = (INS.pagina_tiempos, INS.pagina_documental_a,
               INS.pagina_documental_b, INS.pagina_documental_c,
               INS.pagina_cuestionario)
    ancla = intro
    for constructor in paginas:
        for el in empezar_pagina(componer(constructor)):
            ancla.addnext(el)
            ancla = el
    _cerrar_seccion(cortes, ancla)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin-pdf", action="store_true")
    args = ap.parse_args()

    doc = Document(ENTRADA)
    paso_codigos(doc)
    paso_anexo4(doc)
    IDX.marcar_actualizacion(doc)
    doc.save(SALIDA)
    print("guardado", SALIDA)
    if args.sin_pdf:
        return

    with tempfile.TemporaryDirectory() as tmp:
        referencia = Path(tmp) / "referencia.pdf"
        IDX.convertir(SALIDA, referencia)
        doc2 = Document(SALIDA)
        cambios = IDX.refrescar_indices(doc2, referencia)
        print("entradas de índice corregidas:", len(cambios))
        doc2.save(SALIDA)
        IDX.convertir(SALIDA, PDF)

    import fitz

    final = Document(SALIDA)
    problemas = IDX.verificar(PDF, final)
    print("páginas del PDF:", len(fitz.open(PDF)))
    if problemas:
        print("desajustes de índice:", len(problemas))
        for p in problemas[:15]:
            print("  ", p)
    else:
        print("índices verificados: sin desajustes")


if __name__ == "__main__":
    main()
