# -*- coding: utf-8 -*-
"""v30 · Paso 3 — paginación real de los tres índices.

Convierte el borrador a PDF con LibreOffice, localiza cada título en el PDF
y escribe en cada entrada de índice el folio impreso de su página (romano en
los preliminares, arábigo en el cuerpo). Después vuelve a convertir para
entregar el PDF final y verifica que índice y página coincidan.

Entrada:  salidas/documentos/_v30_paso2.docx
Salidas:  salidas/documentos/_v30_paso3.docx
          salidas/documentos/informe_final_v30.docx
          salidas/documentos/informe_final_v30.pdf
"""
from __future__ import annotations

import re
import shutil
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts" / "compiladores"))

from docx import Document  # noqa: E402

import indices_pdf as IDX  # noqa: E402

DOCS = RAIZ / "salidas" / "documentos"
ENTRADA = DOCS / "_v30_paso2.docx"
BORRADOR = DOCS / "_v30_paso3.docx"
FINAL_DOCX = DOCS / "informe_final_v30.docx"
FINAL_PDF = DOCS / "informe_final_v30.pdf"


def _grupo(titulo: str) -> str:
    """A qué índice pertenece una entrada."""
    m = re.match(r"^(Figura|Tabla)\s+\d+", titulo)
    if m:
        return m.group(1).lower()
    return "contenido"


def paginar(doc, pdf: Path, etiqueta: str) -> int:
    """Escribe el folio real en cada entrada de índice."""
    entradas = IDX.entradas_indice(doc)
    # Los tres índices se paginan por separado: el orden del documento
    # reinicia de cero al pasar del índice de contenido al de figuras.
    grupos = {}
    for el in entradas:
        titulo = IDX.titulo_entrada(el)
        clave = titulo.strip()
        if not clave:
            continue
        grupos.setdefault(_grupo(clave), []).append((el, clave))
    print("%s: %d grupos (contenido, figuras, tablas)" % (etiqueta, len(grupos)))

    cambios = 0
    sin_pagina = []
    for nombre, lista in grupos.items():
        paginas = IDX.paginas_por_titulo_ordenado(pdf, [c for _, c in lista])
        for el, clave in lista:
            folio = paginas.get(clave)
            if folio is None:
                sin_pagina.append(clave)
                continue
            if IDX.fijar_numero(el, folio):
                cambios += 1
    print("%s: %d entradas paginadas, %d sin página"
          % (etiqueta, cambios, len(sin_pagina)))
    for t in sin_pagina[:10]:
        print("   sin página:", t[:70])
    return cambios


def main() -> int:
    doc = Document(str(ENTRADA))

    with tempfile.TemporaryDirectory() as tmp:
        ref = Path(tmp) / "referencia.pdf"
        IDX.convertir(ENTRADA, ref)
        print("referencia: %d páginas" % len(__import__("fitz").open(ref)))
        paginar(doc, ref, "índices")

    doc.save(str(BORRADOR))
    print("guardado:", BORRADOR)

    shutil.copyfile(BORRADOR, FINAL_DOCX)
    IDX.convertir(FINAL_DOCX, FINAL_PDF)
    print("pdf final: %d páginas" % len(__import__("fitz").open(FINAL_PDF)))

    problemas = IDX.verificar(FINAL_PDF, Document(str(FINAL_DOCX)))
    if problemas:
        print("desajustes de índice: %d" % len(problemas))
        for p in problemas[:20]:
            print("   ", p)
    else:
        print("índices verificados: sin desajustes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
