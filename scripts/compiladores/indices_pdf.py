# -*- coding: utf-8 -*-
"""Utilidades de texto, índices paginados y conversión a PDF del informe.

Extraído de ``informe_v27_anexos`` para que los pasos posteriores puedan
rehacer los índices sin arrastrar el constructor de instrumentos (que depende
de un módulo histórico que ya no está en el repositorio).
"""

from __future__ import annotations

import re
import shutil
import subprocess
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ESTILOS_INDICE = ("Tabladeilustraciones", "TDC1", "TDC2", "TDC3", "TDC")


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
    perfil = "file:///tmp/lo_profile_v23"
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


def alinear_sin_justificar(doc: Document) -> int:
    """Pasa a izquierda los párrafos justificados que llevan saltos suaves.

    LibreOffice estira la línea que termina en ``<w:br/>`` para llenar el
    ancho justificado, y quedan renglones con palabras desperdigadas (pasa
    en los bloques A/B/C de las hipótesis y en el listado de Shapiro-Wilk).
    Un párrafo con enunciados en varias líneas se lee mejor alineado a la
    izquierda, como el resto de las listas del informe.
    """
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    cambiados = 0
    for par in doc.paragraphs:
        if par.paragraph_format.alignment != WD_ALIGN_PARAGRAPH.JUSTIFY:
            continue
        if par._p.findall(".//" + qn("w:br")):
            par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            cambiados += 1
    return cambiados



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


