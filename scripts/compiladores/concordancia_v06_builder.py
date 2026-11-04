# -*- coding: utf-8 -*-
"""Compila CONCORDANCIA_v06 (DOCX + PDF) a partir de CONCORDANCIA_v06.md.

El .md es la fuente y manda el orden de los bloques; este script solo le da
la manufactura del paquete (A4, márgenes 3/3/2.5/2.5, Times New Roman 10 pt
cuerpo y 9.5 pt tablas, contorno con separadores horizontales) y comprueba que
no pase de dos páginas.

Uso:
    python scripts/compiladores/concordancia_v06_builder.py
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from scripts.compiladores.instrumentos_recoleccion_v06_builder import (  # noqa: E402
    fijar_marcas_zip, normalizar_pdf)
PAQUETE = RAIZ / "salidas" / "instrumentos" / "INSTRUMENTOS_DEFINITIVOS_v06"
FUENTE = PAQUETE / "CONCORDANCIA_v06.md"
DESTINO_DOCX = PAQUETE / "02_EDITABLES" / "CONCORDANCIA_v06.docx"
DESTINO_PDF = PAQUETE / "01_IMPRIMIBLES" / "CONCORDANCIA_v06.pdf"

ANCHO_UTIL_CM = 15.5
COLUMNAS_CAMBIOS_CM = (0.8, 6.0, 3.9, 4.79)
COLUMNAS_NUMEROS_CM = (6.3, 3.2, 3.2, 2.8)

_TOKEN = re.compile(r"(\*\*.+?\*\*|`[^`]+`)")


def _dxa(valor_cm: float) -> int:
    return int(round(valor_cm * 567))


def _rejilla(tabla) -> None:
    """Cierra todas las celdas: contorno y separadores internos, H y V."""
    tbl_pr = tabla._tbl.tblPr
    for hijo in tbl_pr.findall(qn("w:tblBorders")):
        tbl_pr.remove(hijo)
    bordes = OxmlElement("w:tblBorders")
    for lado, tamano in (("top", 8), ("left", 8), ("bottom", 8),
                         ("right", 8), ("insideH", 4), ("insideV", 4)):
        el = OxmlElement(f"w:{lado}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(tamano))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")
        bordes.append(el)
    tbl_pr.append(bordes)


def _geometria(tabla, anchos_cm) -> None:
    """Fija el ancho de columnas (w:tblLayout fixed) para que no se mueva."""
    tabla.autofit = False
    tbl_pr = tabla._tbl.tblPr
    for hijo in tbl_pr.findall(qn("w:tblLayout")):
        tbl_pr.remove(hijo)
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tbl_pr.append(layout)
    for hijo in tbl_pr.findall(qn("w:tblW")):
        tbl_pr.remove(hijo)
    ancho = OxmlElement("w:tblW")
    ancho.set(qn("w:type"), "dxa")
    ancho.set(qn("w:w"), str(_dxa(sum(anchos_cm))))
    tbl_pr.append(ancho)
    for fila in tabla.rows:
        for celda, valor in zip(fila.cells, anchos_cm):
            celda.width = Cm(valor)
    grid = tabla._tbl.find(qn("w:tblGrid"))
    if grid is not None:
        for columna, valor in zip(grid.findall(qn("w:gridCol")), anchos_cm):
            columna.set(qn("w:w"), str(_dxa(valor)))


def _trozos(texto: str):
    """Parte el texto en (contenido, negrita, monoespaciado)."""
    for trozo in _TOKEN.split(texto):
        if not trozo:
            continue
        if trozo.startswith("**") and trozo.endswith("**"):
            yield trozo[2:-2], True, False
        elif trozo.startswith("`") and trozo.endswith("`"):
            yield trozo[1:-1], False, True
        else:
            yield trozo, False, False


def _escribir(parrafo, texto: str, tamano: float, negrita: bool = False,
              cursiva: bool = False, fuente: str = "Times New Roman") -> None:
    for contenido, neg, mono in _trozos(texto):
        run = parrafo.add_run(contenido)
        run.font.name = fuente
        run.font.size = Pt(tamano)
        run.bold = neg or negrita
        run.italic = cursiva
        if mono:
            run.font.name = "Courier New"
            run.font.size = Pt(tamano - 0.5)


def _sin_sangria(celda, texto: str, negrita: bool = False,
                 tamano: float = 8.5) -> None:
    parrafo = celda.paragraphs[0]
    fmt = parrafo.paragraph_format
    fmt.space_before = Pt(0)
    fmt.space_after = Pt(0)
    fmt.line_spacing = Pt(tamano + 1.6)
    parrafo.alignment = WD_ALIGN_PARAGRAPH.LEFT
    _escribir(parrafo, texto, tamano, negrita=negrita)


def _parrafo(doc, texto: str, tamano: float = 9.5, negrita: bool = False,
             antes: float = 0, despues: float = 4, sangria_cm: float = 0,
             justificar: bool = True, cursiva: bool = False):
    parrafo = doc.add_paragraph()
    fmt = parrafo.paragraph_format
    fmt.space_before = Pt(antes)
    fmt.space_after = Pt(despues)
    fmt.line_spacing = Pt(tamano + 2.2)
    fmt.left_indent = Cm(sangria_cm)
    fmt.alignment = (WD_ALIGN_PARAGRAPH.JUSTIFY if justificar
                     else WD_ALIGN_PARAGRAPH.LEFT)
    _escribir(parrafo, texto, tamano, negrita=negrita, cursiva=cursiva)
    return parrafo


def _titulo(doc, texto: str, tamano: float = 13) -> None:
    parrafo = doc.add_paragraph()
    fmt = parrafo.paragraph_format
    fmt.space_before = Pt(0)
    fmt.space_after = Pt(6)
    fmt.line_spacing = Pt(tamano + 3)
    fmt.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = parrafo.add_run(texto)
    run.font.name = "Times New Roman"
    run.font.size = Pt(tamano)
    run.bold = True


# ---------------------------------------------------------------------------
# Lectura del .md en bloques ordenados
# ---------------------------------------------------------------------------

def _bloques(texto: str):
    """Devuelve [(tipo, contenido)] respetando el orden del documento."""
    salida = []
    tabla = []
    for linea in texto.split("\n"):
        if linea.startswith("|"):
            tabla.append(linea)
            continue
        if tabla:
            salida.append(("tabla", _filas(tabla)))
            tabla = []
        limpia = linea.strip()
        if not limpia:
            continue
        if limpia.startswith("# "):
            salida.append(("h1", limpia[2:].strip()))
        elif limpia.startswith("## "):
            salida.append(("h2", limpia[3:].strip()))
        elif limpia.startswith("- "):
            salida.append(("li", limpia[2:].strip()))
        else:
            salida.append(("p", limpia))
    if tabla:
        salida.append(("tabla", _filas(tabla)))
    return salida


def _filas(lineas):
    filas = []
    for linea in lineas:
        if set(linea.replace("|", "").strip()) <= set("-: "):
            continue
        filas.append([c.strip() for c in linea.strip().strip("|").split("|")])
    return filas


def _tabla(doc, filas, anchos_cm) -> None:
    tabla = doc.add_table(rows=len(filas), cols=len(anchos_cm))
    tabla.alignment = WD_TABLE_ALIGNMENT.LEFT
    tabla.style = None
    _rejilla(tabla)
    _geometria(tabla, anchos_cm)
    for indice, fila in enumerate(filas):
        for celda, valor, ancho in zip(tabla.rows[indice].cells, fila,
                                       anchos_cm):
            _sin_sangria(celda, valor, negrita=(indice == 0),
                         tamano=(8.5 if indice == 0 else 8.4))
            celda.width = Cm(ancho)


def construir() -> Path:
    doc = Document()
    seccion = doc.sections[0]
    seccion.page_width = Cm(21.0)
    seccion.page_height = Cm(29.7)
    seccion.left_margin = Cm(3.0)
    seccion.top_margin = Cm(3.0)
    seccion.right_margin = Cm(2.5)
    seccion.bottom_margin = Cm(2.5)

    estilo = doc.styles["Normal"]
    estilo.font.name = "Times New Roman"
    estilo.font.size = Pt(10)
    estilo.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    estilo.paragraph_format.space_before = Pt(0)
    estilo.paragraph_format.space_after = Pt(0)

    bloques = _bloques(FUENTE.read_text(encoding="utf-8"))
    for posicion, (tipo, contenido) in enumerate(bloques):
        siguiente = bloques[posicion + 1][0] if posicion + 1 < len(bloques) else ""
        if tipo == "h1":
            _titulo(doc, contenido)
        elif tipo == "h2":
            parrafo = _parrafo(doc, contenido, tamano=10.5, negrita=True,
                               antes=9, despues=3, justificar=False)
            parrafo.paragraph_format.keep_with_next = True
        elif tipo == "p":
            parrafo = _parrafo(doc, contenido, despues=4)
            parrafo.paragraph_format.keep_with_next = (siguiente == "tabla")
        elif tipo == "li":
            _parrafo(doc, "• " + contenido, despues=3, sangria_cm=0.4)
        elif tipo == "tabla":
            anchos = (COLUMNAS_CAMBIOS_CM if contenido[0][0] == "#"
                      else COLUMNAS_NUMEROS_CM)
            _tabla(doc, contenido, anchos)
            _parrafo(doc, "", tamano=4, despues=0)

    DESTINO_DOCX.parent.mkdir(parents=True, exist_ok=True)
    doc.save(DESTINO_DOCX)
    fijar_marcas_zip(DESTINO_DOCX)
    return DESTINO_DOCX


def exportar_pdf(docx: Path) -> Path:
    if shutil.which("soffice") is None:
        print("[concordancia] sin LibreOffice: solo DOCX")
        return docx
    with tempfile.TemporaryDirectory() as temporal:
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                        "--outdir", temporal, str(docx)],
                       check=True, capture_output=True, timeout=180)
        normalizar_pdf(Path(temporal) / (docx.stem + ".pdf"), DESTINO_PDF)
    return DESTINO_PDF


def paginas(pdf: Path) -> int:
    try:
        import fitz
    except ModuleNotFoundError:
        return -1
    return fitz.open(pdf).page_count


def main() -> int:
    docx = construir()
    pdf = exportar_pdf(docx)
    total = paginas(pdf) if pdf.suffix == ".pdf" else -1
    print(f"[concordancia] DOCX {docx}")
    print(f"[concordancia] PDF  {pdf}  páginas={total}")
    if total > 2:
        print("[concordancia] AVISO: excede las dos páginas")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
