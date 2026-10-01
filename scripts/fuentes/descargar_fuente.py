#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Descarga verificada de fuentes bibliográficas (Squad A).

Dado un DOI: obtiene metadatos verificados en Crossref, localiza el PDF de acceso
abierto (OpenAlex y, opcionalmente, Unpaywall), lo descarga, lo VALIDA contra los
metadatos (un PDF equivocado se descarta), lo archiva en la base bibliográfica, lo
indexa con `ingesta_pdf` y genera la ficha de Obsidian. Deja listo el payload para
que el agente registre la fuente en Zotero con la herramienta MCP `zotero_add_item`
(este script NO escribe en Zotero).

Principios anti-alucinación:
  * Si Crossref responde 404, la fuente NO se da por verificada y no se archiva nada.
  * Ningún dato se adivina: lo ausente queda `null` o `[VERIFICAR: motivo]`.
  * Un PDF se acepta solo si empieza por %PDF-, abre con PyMuPDF (no cifrado) y
    (a) el DOI de Crossref aparece en sus 2 primeras páginas, o (b) el título completo
    de Crossref aparece como frase en ellas (contiguo, o difuso >= 95 con todas sus
    palabras significativas presentes). Títulos de menos de 3 palabras significativas
    solo se aceptan por DOI: son demasiado genéricos para validar por texto.
  * Nunca se pisa un PDF ni una ficha existente.
  * Sin Tesseract no se hace OCR: un PDF sin capa de texto no puede validarse y se
    descarta con el aviso "requiere OCR".

Uso:
    python scripts/fuentes/descargar_fuente.py doi 10.3389/fpubh.2023.1194807
    python scripts/fuentes/descargar_fuente.py verificar 10.3389/fpubh.2023.1194807
    python scripts/fuentes/descargar_fuente.py lote --archivo dois.txt [--solo-verificar]
    python scripts/fuentes/descargar_fuente.py titulo "texto del título"   # solo candidatos
    (todas aceptan --json; códigos de salida: 0 ok, 1 hallazgos/fallos, 2 uso incorrecto)

Variables de entorno opcionales: UNPAYWALL_EMAIL (habilita Unpaywall), SIVAC_MAILTO.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import sys
import time
from datetime import date
from pathlib import Path
from urllib.parse import quote

import requests
from rapidfuzz import fuzz

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad  # noqa: E402

# `ingesta_pdf` hace `import fitz`, alias que imprime un aviso de deprecación y ensucia la salida (--json).
# Se registra `pymupdf` (mismo paquete, nombre vigente) bajo el alias `fitz` antes de importarlo.
import pymupdf  # noqa: E402

sys.modules.setdefault("fitz", pymupdf)
from scripts.fuentes import ingesta_pdf  # noqa: E402
from scripts.fuentes import texto as tx  # noqa: E402

UMBRAL_TITULO = 95        # partial_ratio mínimo de la frase-título (modo difuso)
MIN_PALABRAS_TITULO = 3   # sin DOI en texto, el título debe tener >= 3 palabras significativas
MAX_BYTES_PDF = 150 * 1024 * 1024
MAX_APELLIDO = 40         # tope del apellido en nombres de archivo y citekey (autores institucionales largos)
MAX_RUTA = 240            # tope de la ruta completa (límite clásico de Windows: 260)
TESSERACT_EXE = r"C:/Users/jquis/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"
MAILTO = os.environ.get("SIVAC_MAILTO", "sivac-thesis-lab@example.org")
USER_AGENT = f"sivac-thesis-lab/1.0 (tesis UNAJMA; mailto:{MAILTO})"
URL_CROSSREF = "https://api.crossref.org/works/{doi}"
URL_OPENALEX = "https://api.openalex.org/works/doi:{doi}"
URL_UNPAYWALL = "https://api.unpaywall.org/v2/{doi}?email={email}"

_STOPWORDS = {
    "a", "an", "the", "of", "on", "in", "for", "and", "or", "to", "with", "from", "by",
    "at", "as", "is", "are", "towards", "toward", "de", "del", "la", "las", "el", "los",
    "un", "una", "y", "en", "para", "por", "con", "al", "sobre", "hacia",
}


# ---------------------------------------------------------------------------
# Utilidades puras
# ---------------------------------------------------------------------------
def normalizar_doi(entrada: str) -> str | None:
    """Devuelve el DOI limpio en minúsculas (sin URL ni prefijo 'doi:') o None."""
    if not entrada:
        return None
    t = entrada.strip()
    t = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", t, flags=re.I)
    doi = tx.extraer_doi(t)
    return doi.lower() if doi else None


def tesseract_disponible() -> bool:
    return bool(shutil.which("tesseract")) or Path(TESSERACT_EXE).exists()


def _limpiar_jats(texto: str) -> str:
    """Quita etiquetas JATS/HTML del abstract de Crossref."""
    t = re.sub(r"<jats:title>.*?</jats:title>", " ", texto or "", flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def _abstract_openalex(indice_invertido: dict | None) -> str | None:
    if not indice_invertido:
        return None
    posiciones: list[tuple[int, str]] = []
    for palabra, lista in indice_invertido.items():
        posiciones.extend((p, palabra) for p in lista)
    return " ".join(p for _, p in sorted(posiciones)) or None


def _anio_crossref(item: dict) -> int | None:
    for clave in ("issued", "published-print", "published-online", "published", "created"):
        try:
            return int(item[clave]["date-parts"][0][0])
        except (KeyError, IndexError, TypeError, ValueError):
            continue
    return None


def parsear_crossref(mensaje: dict) -> dict:
    """Convierte el objeto `message` de Crossref en metadatos normalizados."""
    autores = []
    for a in mensaje.get("author", []) or []:
        if a.get("family"):
            autores.append({"apellido": a["family"].strip(), "nombre": (a.get("given") or "").strip()})
        elif a.get("name"):
            autores.append({"apellido": a["name"].strip(), "nombre": "", "institucional": True})
    editores = []
    for e in mensaje.get("editor", []) or []:
        if e.get("family"):
            editores.append({"apellido": e["family"].strip(), "nombre": (e.get("given") or "").strip()})
    titulos = mensaje.get("title") or []
    subt = mensaje.get("subtitle") or []
    revistas = mensaje.get("container-title") or []
    return {
        "doi": (mensaje.get("DOI") or "").lower() or None,
        "titulo": html.unescape(titulos[0]).strip() if titulos else None,
        "subtitulo": subt[0].strip() if subt else None,
        "autores": autores,
        "editores": editores,
        "edicion": str(mensaje["edition-number"]) if mensaje.get("edition-number") else None,
        "anio": _anio_crossref(mensaje),
        "revista": html.unescape(revistas[0]).strip() if revistas else None,
        "editorial": mensaje.get("publisher"),
        "volumen": mensaje.get("volume"),
        "numero": mensaje.get("issue"),
        "paginas": mensaje.get("page"),
        "articulo": mensaje.get("article-number"),
        "tipo": mensaje.get("type"),
        "url": mensaje.get("URL"),
        "abstract": _limpiar_jats(mensaje["abstract"]) if mensaje.get("abstract") else None,
    }


def _iniciales(nombre: str) -> str:
    partes = []
    for palabra in nombre.replace(".", " ").split():
        sub = [s for s in palabra.split("-") if s]
        partes.append("-".join(s[0].upper() + "." for s in sub))
    return " ".join(partes)


def _autor_apa(a: dict) -> str:
    if a.get("institucional") or not a.get("nombre"):
        return a["apellido"]
    return f"{a['apellido']}, {_iniciales(a['nombre'])}"


def formatear_apa7(meta: dict) -> str:
    """Referencia APA 7 con cursivas en *…*. Lo ausente se omite o se marca [VERIFICAR]."""
    autores = [_autor_apa(a) for a in meta.get("autores") or []]
    if not autores:
        bloque_autor = ""
    elif len(autores) == 1:
        bloque_autor = autores[0]
    elif len(autores) <= 20:
        bloque_autor = ", ".join(autores[:-1]) + ", & " + autores[-1]
    else:
        bloque_autor = ", ".join(autores[:19]) + ", . . . " + autores[-1]
    anio = meta.get("anio")
    fecha = f"({anio})." if anio else "(s. f.). [VERIFICAR: año ausente en Crossref]"  # ya incluye su punto final
    titulo = meta.get("titulo") or "[VERIFICAR: título ausente]"
    if meta.get("subtitulo") and meta["subtitulo"].lower() not in titulo.lower():
        titulo = f"{titulo}: {meta['subtitulo']}"
    sep = "" if titulo.rstrip().endswith(("?", "!", ".")) else "."

    enlace = f" https://doi.org/{meta['doi']}" if meta.get("doi") else ""
    tipo = meta.get("tipo")
    if tipo == "book-chapter" and meta.get("revista"):
        return _apa_capitulo(meta, bloque_autor, fecha, titulo, sep, enlace)
    if meta.get("revista") and tipo != "book":
        fuente = f"*{meta['revista']}*"
        if meta.get("volumen"):
            fuente += f", *{meta['volumen']}*"
            if meta.get("numero"):
                fuente += f"({meta['numero']})"
        elif meta.get("numero"):  # sin volumen el número no se descarta
            fuente += f", ({meta['numero']})"
        if meta.get("paginas"):
            fuente += f", {str(meta['paginas']).replace('-', '–')}"
        elif meta.get("articulo"):
            fuente += f", Article {meta['articulo']}"
        cuerpo = f"{titulo}{sep} {fuente}."
        if not bloque_autor:  # APA: sin autor, el título ocupa su lugar
            return f"{titulo}{sep} {fecha} {fuente}.{enlace}".strip()
    else:
        ed = f" ({_ordinal_edicion(meta['edicion'])} ed.)" if meta.get("edicion") else ""
        edit = f" {meta['editorial']}." if meta.get("editorial") else ""
        cuerpo = f"*{titulo}*{ed}{sep}{edit}"
        if not bloque_autor:
            return f"*{titulo}*{ed}{sep} {fecha}{edit}{enlace}".strip()
    return f"{bloque_autor} {fecha} {cuerpo}{enlace}".strip()


def _ordinal_edicion(numero: str) -> str:
    """'2' -> '2nd' (APA 7 en inglés); otro texto se devuelve tal cual."""
    if not str(numero).isdigit():
        return str(numero)
    n = int(numero)
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


def _editor_apa(e: dict) -> str:
    return f"{_iniciales(e['nombre'])} {e['apellido']}".strip() if e.get("nombre") else e["apellido"]


def _apa_capitulo(meta: dict, bloque_autor: str, fecha: str, titulo: str, sep: str, enlace: str) -> str:
    """Capítulo de libro: 'Autor (año). Título. En Editor (Ed.), *Libro* (ed., pp.). Editorial.'"""
    eds = [_editor_apa(e) for e in meta.get("editores") or []]
    if eds:
        lista = eds[0] if len(eds) == 1 else (f"{eds[0]} & {eds[1]}" if len(eds) == 2 else ", ".join(eds[:-1]) + ", & " + eds[-1])
        bloque_ed = f"In {lista} ({'Ed.' if len(eds) == 1 else 'Eds.'}), "
    else:
        bloque_ed = "In "
    extra = []
    if meta.get("edicion"):
        extra.append(f"{_ordinal_edicion(meta['edicion'])} ed.")
    if meta.get("paginas"):
        extra.append(f"pp. {str(meta['paginas']).replace('-', '–')}")
    detalle = f" ({', '.join(extra)})" if extra else ""
    editorial = f" {meta['editorial']}." if meta.get("editorial") else ""
    resto = f"{bloque_ed}*{meta['revista']}*{detalle}.{editorial}"
    if not bloque_autor:
        return f"{titulo}{sep} {fecha} {resto}{enlace}".strip()
    return f"{bloque_autor} {fecha} {titulo}{sep} {resto}{enlace}".strip()


def generar_citekey(meta: dict) -> str:
    """apellido1 completo + año + primera palabra significativa del título (minúsculas, sin tildes).

    El apellido compuesto se conserva entero ('García Márquez' -> 'garciamarquez'). Si falta
    autor o año se usan 'anon' / 'sf' como relleno; `avisos_citekey` lo reporta.
    """
    autores = meta.get("autores") or []
    ap = re.sub(r"[^a-z0-9]", "", tx.canonico(autores[0]["apellido"] if autores else "anon"))[:MAX_APELLIDO] or "anon"
    anio = str(meta.get("anio") or "sf")
    palabra = ""
    for w in tx.tokens(meta.get("titulo") or ""):
        w = re.sub(r"[^a-z0-9]", "", tx.canonico(w))
        if w and w not in _STOPWORDS and len(w) > 2 and not w.isdigit():
            palabra = w
            break
    return f"{ap}{anio}{palabra}"


def avisos_citekey(meta: dict) -> list[str]:
    """Avisos [VERIFICAR] cuando el citekey usa relleno ('anon', 'sf') por datos ausentes."""
    av = []
    if not (meta.get("autores") or []):
        av.append("[VERIFICAR: citekey con relleno 'anon': Crossref no entregó autores]")
    if not meta.get("anio"):
        av.append("[VERIFICAR: citekey con relleno 'sf': Crossref no entregó año]")
    return av


def nombre_pdf(meta: dict, max_total: int | None = None) -> str:
    """'Apellido - año - titulo-corto.pdf' con longitud acotada.

    El apellido se trunca a MAX_APELLIDO caracteres; si se indica `max_total` (largo
    disponible para el nombre de archivo incluida la extensión), el título corto se
    recorta y, en último caso, también el apellido, para no exceder el límite de ruta.
    """
    autores = meta.get("autores") or []
    ap = (autores[0]["apellido"].strip() if autores else "Anonimo")
    ap = re.sub(r'[<>:"/\|?*\x00-\x1f]', "", ap).strip(" .")[:MAX_APELLIDO].rstrip(" .") or "Anonimo"
    palabras = [w for w in tx.slug(meta.get("titulo") or "", 120).split("-") if w and w not in _STOPWORDS]
    corto = "-".join(palabras[:5])[:60].strip("-") or "sin-titulo"
    anio = meta.get("anio") or "sf"
    if max_total is not None:
        fijo = len(f" - {anio} - ") + len(".pdf")
        disponible = max(max_total - fijo, 2)          # para apellido + título corto
        if len(ap) + len(corto) > disponible:
            corto = corto[: max(disponible - len(ap), 1)].strip("-") or "s"
        if len(ap) + len(corto) > disponible:
            ap = ap[: max(disponible - len(corto), 1)].rstrip(" .") or "A"
    return f"{ap} - {anio} - {corto}.pdf"


# ---------------------------------------------------------------------------
# Red (toda la E/S HTTP pasa por _get para poder simularla en pruebas)
# ---------------------------------------------------------------------------
def _get(url: str, *, headers: dict | None = None, timeout: int = 30, reintentos: int = 3,
         espera: float = 1.5, stream: bool = False):
    """GET con reintentos ante errores de red, 429 y 5xx. Devuelve la última respuesta."""
    cab = {"User-Agent": USER_AGENT, **(headers or {})}
    ultima_exc: Exception | None = None
    resp = None
    for intento in range(1, reintentos + 1):
        try:
            resp = requests.get(url, headers=cab, timeout=timeout, stream=stream, allow_redirects=True)
            if resp.status_code == 429 or resp.status_code >= 500:
                ultima_exc = None
            else:
                return resp
        except requests.RequestException as e:
            ultima_exc = e
            resp = None
        if intento < reintentos:
            time.sleep(espera * intento)
    if resp is not None:
        return resp
    raise ultima_exc or requests.RequestException("sin respuesta")


def consultar_crossref(doi: str, **kw) -> dict | None:
    """Metadatos normalizados o None si Crossref responde 404 (DOI no verificado)."""
    r = _get(URL_CROSSREF.format(doi=quote(doi, safe="/")), **kw)
    if r.status_code == 404:
        return None
    if r.status_code != 200:
        raise requests.RequestException(f"Crossref respondió HTTP {r.status_code}")
    return parsear_crossref(r.json()["message"])


def consultar_openalex(doi: str, **kw) -> dict:
    """Devuelve {'pdf_urls': [...], 'abstract': str|None}. Falla de red => vacío."""
    vacio = {"pdf_urls": [], "abstract": None}
    try:
        r = _get(URL_OPENALEX.format(doi=quote(doi, safe="/")), **kw)
        if r.status_code != 200:
            return vacio
        d = r.json()
    except (requests.RequestException, ValueError):
        return vacio
    urls: list[str] = []
    for loc in [d.get("best_oa_location"), d.get("primary_location"), *(d.get("locations") or [])]:
        if loc and loc.get("pdf_url") and (loc.get("is_oa") or loc is d.get("best_oa_location")):
            urls.append(loc["pdf_url"])
    oa = (d.get("open_access") or {}).get("oa_url")
    if oa:
        urls.append(oa)
    return {"pdf_urls": list(dict.fromkeys(urls)), "abstract": _abstract_openalex(d.get("abstract_inverted_index"))}


def consultar_unpaywall(doi: str, **kw) -> list[str]:
    email = os.environ.get("UNPAYWALL_EMAIL")
    if not email:
        return []
    try:
        r = _get(URL_UNPAYWALL.format(doi=quote(doi, safe="/"), email=quote(email)), **kw)
        if r.status_code != 200:
            return []
        d = r.json()
    except (requests.RequestException, ValueError):
        return []
    urls = [l["url_for_pdf"] for l in [d.get("best_oa_location")] + (d.get("oa_locations") or []) if l and l.get("url_for_pdf")]
    return list(dict.fromkeys(urls))


def buscar_candidatos_titulo(titulo: str, limite: int = 5, **kw) -> list[dict]:
    """Candidatos de Crossref para un título (NUNCA se elige uno automáticamente)."""
    r = _get(f"https://api.crossref.org/works?query.bibliographic={quote(titulo)}&rows={limite}", **kw)
    if r.status_code != 200:
        raise requests.RequestException(f"Crossref respondió HTTP {r.status_code}")
    salida = []
    for it in r.json()["message"].get("items", []):
        m = parsear_crossref(it)
        m["similitud_titulo"] = round(fuzz.token_set_ratio(tx.canonico(titulo), tx.canonico(m["titulo"] or "")), 1)
        salida.append(m)
    return salida


def descargar_bytes(url: str, **kw) -> bytes:
    """Descarga el contenido (con tope de tamaño). Lanza RequestException si no es 200."""
    r = _get(url, stream=True, headers={"Accept": "application/pdf,*/*;q=0.8"}, **kw)
    if r.status_code != 200:
        raise requests.RequestException(f"HTTP {r.status_code} en {url}")
    partes, total = [], 0
    for trozo in r.iter_content(chunk_size=1 << 16):
        total += len(trozo)
        if total > MAX_BYTES_PDF:
            raise requests.RequestException("PDF excede el tamaño máximo permitido")
        partes.append(trozo)
    return b"".join(partes)


# ---------------------------------------------------------------------------
# Validación de PDF
# ---------------------------------------------------------------------------
def _palabras_significativas(titulo: str) -> list[str]:
    palabras = []
    for w in tx.canonico(titulo).replace("-", " ").split():
        w = re.sub(r"\W", "", w)
        if w and w not in _STOPWORDS and len(w) > 1:
            palabras.append(w)
    return palabras


def coincide_titulo(titulo: str, texto_pdf: str) -> tuple[bool, float, str]:
    """Decide si el título completo aparece como FRASE en el texto del PDF.

    Devuelve (coincide, puntaje 0-100, modo). No usa token_set_ratio (daba 100 con
    cualquier subconjunto de palabras). Modos: 'exacto' (subcadena contigua tras
    normalizar), 'difuso' (partial_ratio >= UMBRAL_TITULO Y todas las palabras
    significativas presentes), 'generico' (título demasiado corto) o 'no'.
    """
    c_tit = re.sub(r"[\s\-]+", " ", tx.canonico(titulo))
    c_txt = re.sub(r"[\s\-]+", " ", tx.canonico(texto_pdf))
    palabras = _palabras_significativas(titulo)
    if len(palabras) < MIN_PALABRAS_TITULO:
        return False, 0.0, "generico"
    if c_tit and c_tit in c_txt:
        return True, 100.0, "exacto"
    puntaje = round(fuzz.partial_ratio(c_tit, c_txt), 1)
    vocab = set(re.findall(r"\w+", c_txt))
    if puntaje >= UMBRAL_TITULO and all(w in vocab for w in palabras):
        return True, puntaje, "difuso"
    return False, puntaje, "no"


_RE_DOI_GENERICO = re.compile(r"10\.\d{4,9}/[a-z0-9._;()/:<>\-]+")
_RE_REFERENCIAS = re.compile(r"\b(references|referencias|bibliograf[ií]a|bibliography|literature cited)\b")


def doi_propio_en_texto(doi: str, texto: str) -> bool:
    """¿El DOI de la fuente figura como DOI PROPIO del documento en el texto dado?

    Exige (1) coincidencia exacta con límites (un DOI que es prefijo de otro más largo,
    p. ej. 10.1000/abc dentro de 10.1000/abc123, NO cuenta); (2) que no aparezca después de
    un encabezado de referencias/bibliografía (allí solo se cita a otros); y (3) que sea el
    primer DOI del texto (un artículo ajeno que cita otros DOI antes no cuenta).
    """
    doi = (doi or "").lower().strip()
    if not doi:
        return False
    t = re.sub(r"(10\.\d{4,9}/)\s+", r"\1", texto.lower())  # DOI partido justo tras la barra
    patron = r"(?<![a-z0-9])" + re.escape(doi) + r"(?![a-z0-9_/\-]|\.[a-z0-9])"
    m = re.search(patron, t)
    if not m:
        return False
    ref = _RE_REFERENCIAS.search(t)
    if ref and ref.start() < m.start():
        return False
    primero = _RE_DOI_GENERICO.search(t)
    return primero is None or primero.start() == m.start()


def validar_pdf(contenido: bytes, meta: dict) -> dict:
    """Valida un PDF descargado contra los metadatos. No escribe nada.

    Criterio: (a) el DOI de Crossref figura, exacto y como DOI propio, en las 2 primeras páginas, o (b) el título
    completo figura como frase (ver `coincide_titulo`). PDF cifrado, corrupto, HTML o
    sin capa de texto se rechazan con motivo; nunca se propaga una excepción.
    """
    import pymupdf

    res = {"ok": False, "motivo": None, "similitud_titulo": None, "doi_en_texto": False,
           "modo_validacion": None, "paginas": None}
    if not contenido.startswith(b"%PDF-"):
        res["motivo"] = "el contenido no empieza por %PDF- (probablemente una página HTML)"
        return res
    try:
        doc = pymupdf.open(stream=contenido, filetype="pdf")
    except Exception as e:  # noqa: BLE001
        res["motivo"] = f"PyMuPDF no pudo abrir el PDF: {type(e).__name__}"
        return res
    try:
        if doc.needs_pass or doc.is_encrypted:
            res["motivo"] = "PDF cifrado con contraseña: no se puede leer ni validar"
            return res
        res["paginas"] = doc.page_count
        if doc.page_count == 0:
            res["motivo"] = "PDF sin páginas"
            return res
        texto = " ".join(doc[i].get_text() for i in range(min(2, doc.page_count)))
    except Exception as e:  # noqa: BLE001  (PDF hostil: estructura dañada al leer páginas)
        res["motivo"] = f"no se pudo leer el texto del PDF: {type(e).__name__}: {e}"
        return res
    finally:
        doc.close()
    if len(texto.strip()) < 40:
        aviso = "Tesseract disponible pero este script no realiza OCR" if tesseract_disponible() else "Tesseract no instalado"
        res["motivo"] = f"requiere OCR: las 2 primeras páginas no tienen capa de texto ({aviso}); no se puede validar el título"
        return res
    res["doi_en_texto"] = doi_propio_en_texto(meta.get("doi") or "", texto)
    titulo = meta.get("titulo")
    if titulo:
        coincide, puntaje, modo = coincide_titulo(titulo, texto)
        res["similitud_titulo"] = puntaje
    else:
        coincide, modo = False, "sin_titulo"
    if res["doi_en_texto"]:
        res["ok"], res["modo_validacion"] = True, "doi"
        return res
    if coincide:
        res["ok"], res["modo_validacion"] = True, f"titulo_{modo}"
        return res
    if not titulo:
        res["motivo"] = "Crossref no entregó título y el DOI no figura en el PDF: no hay con qué validarlo"
    elif modo == "generico":
        res["motivo"] = (f"título demasiado genérico (< {MIN_PALABRAS_TITULO} palabras significativas) y el DOI no figura "
                         "en las 2 primeras páginas: no se puede validar por título")
    else:
        res["motivo"] = (f"ni el DOI ni el título completo figuran en las 2 primeras páginas "
                         f"(similitud de frase {res['similitud_titulo']} < {UMBRAL_TITULO} o faltan palabras del título)")
    return res


# ---------------------------------------------------------------------------
# Archivo, ficha y orquestación
# ---------------------------------------------------------------------------
def buscar_pdf_duplicado(sha: str, carpeta: Path) -> Path | None:
    for pdf in sorted(carpeta.glob("*.pdf")) if carpeta.exists() else []:
        if seguridad.sha256_archivo(pdf) == sha:
            return pdf
    return None


def guardar_pdf(contenido: bytes, meta: dict, carpeta: Path) -> tuple[Path, bool]:
    """Guarda sin pisar. Devuelve (ruta, era_duplicado). Mismo sha256 => reutiliza."""
    import hashlib

    sha = hashlib.sha256(contenido).hexdigest()
    existente = buscar_pdf_duplicado(sha, carpeta)
    if existente:
        return existente, True
    # Presupuesto: ruta de la carpeta + separador + nombre + sufijo ' (NN)' de desambiguación.
    base = nombre_pdf(meta, max_total=max(MAX_RUTA - len(str(Path(carpeta).resolve())) - 1 - len(" (99)"), 24))
    destino = carpeta / base
    n = 2
    while destino.exists():
        destino = carpeta / f"{Path(base).stem} ({n}).pdf"
        n += 1
    destino = seguridad.asegurar_escritura_permitida(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with open(destino, "xb") as f:
        f.write(contenido)
    return destino, False


def ficha_existente_para_doi(doi: str, carpeta: Path) -> Path | None:
    patron = re.compile(r'^doi:\s*["\']?([^"\'\s]+)', re.I | re.M)
    for md in sorted(carpeta.glob("*.md")) if carpeta.exists() else []:
        try:
            cabecera = "\n".join(md.read_text(encoding="utf-8").splitlines()[:40])
        except OSError:
            continue
        m = patron.search(cabecera)
        if m and m.group(1).lower() == doi.lower():
            return md
    return None


def _q(valor) -> str:
    """Escalar YAML seguro (JSON es YAML válido)."""
    return json.dumps(valor, ensure_ascii=False)


def construir_ficha(meta: dict, citekey: str, datos: dict) -> str:
    """Texto Markdown de la ficha. `datos`: verificado, pdf_local, sha256, paginas, fuente_metadatos, abstract, avisos."""
    autores = [_autor_apa(a) for a in meta.get("autores") or []]
    fm = [
        "---",
        "tipo: literatura",
        f"citekey: {_q(citekey)}",
        f"doi: {_q(meta.get('doi'))}",
        f"titulo: {_q(meta.get('titulo'))}",
        f"anio: {_q(meta.get('anio'))}",
        "autores:" + ("" if autores else " []"),
        *[f"  - {_q(a)}" for a in autores],
        f"verificado: {str(bool(datos['verificado'])).lower()}",
        f"pdf_local: {_q(datos.get('pdf_local'))}",
        f"sha256: {_q(datos.get('sha256'))}",
        f"paginas: {_q(datos.get('paginas'))}",
        f"fuente_metadatos: {_q(datos.get('fuente_metadatos'))}",
        f"fecha_ingreso: {date.today().isoformat()}",
        f"estado: {_q('pendiente_hallazgos' if datos.get('pdf_local') else 'sin_pdf_solicitar_al_tesista')}",
        "---",
        "",
        f"# @{citekey}",
        "",
        "## Referencia APA 7",
        "",
        formatear_apa7(meta),
        "",
        "## Resumen",
        "",
    ]
    if datos.get("abstract"):
        fm += [f"> Abstract según {datos.get('fuente_abstract', 'la fuente de metadatos')} (sin edición):", "", datos["abstract"], ""]
    else:
        fm += ["Abstract no disponible", ""]
    fm += ["## Estado del PDF", ""]
    if datos.get("pdf_local"):
        fm += [f"PDF archivado: `{datos['pdf_local']}` ({datos.get('paginas')} págs., sha256 `{datos.get('sha256')}`)."]
    else:
        fm += ["PDF no disponible en acceso abierto: solicitar al tesista"]
    for a in datos.get("avisos") or []:
        fm += [f"- Aviso: {a}"]
    fm += ["", "## Hallazgos citables", "", "<!-- Completar con el buscador de citas (página impresa + párrafo); si no se confirma la página impresa: [VERIFICAR] -->", "",
           "## Vínculos", "", "- [[MOC_01_TESIS_SIVAC]]", ""]
    return "\n".join(fm)


def crear_ficha(meta: dict, citekey_base: str, datos: dict, carpeta: Path) -> Path:
    """Crea la ficha sin sobrescribir: si '@citekey' existe usa '@citekey_2', '_3', …"""
    carpeta = seguridad.asegurar_escritura_permitida(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    citekey, n = citekey_base, 2
    while (carpeta / f"@{citekey}.md").exists():
        citekey = f"{citekey_base}_{n}"
        n += 1
    destino = seguridad.asegurar_escritura_permitida(carpeta / f"@{citekey}.md")
    with open(destino, "x", encoding="utf-8") as f:
        f.write(construir_ficha(meta, citekey, datos))
    return destino


def verificar_doi(doi_entrada: str, **kw) -> dict:
    """Solo metadatos (Crossref). No descarga ni escribe."""
    doi = normalizar_doi(doi_entrada)
    res = {"entrada": doi_entrada, "doi": doi, "estado": None, "verificado": False, "metadatos": None,
           "citekey": None, "referencia_apa7": None, "avisos": []}
    if not doi:
        res["estado"] = "doi_invalido"
        res["avisos"].append("[VERIFICAR: la entrada no contiene un DOI reconocible]")
        return res
    try:
        meta = consultar_crossref(doi, **kw)
    except requests.RequestException as e:
        res["estado"] = "error_red"
        res["avisos"].append(f"[VERIFICAR: no se pudo consultar Crossref ({type(e).__name__}: {e})]")
        return res
    if meta is None:
        res["estado"] = "no_verificada"
        res["avisos"].append("Crossref respondió 404: la fuente NO se da por verificada")
        return res
    res.update(estado="verificada", verificado=True, metadatos=meta, citekey=generar_citekey(meta),
               referencia_apa7=formatear_apa7(meta))
    res["avisos"].extend(avisos_citekey(meta))
    return res


def procesar_doi(doi_entrada: str, *, carpeta_pdfs: Path | None = None, carpeta_notas: Path | None = None,
                 carpeta_indices: Path | None = None, descargar: bool = True, **kw) -> dict:
    """Flujo completo: verificar, descargar, validar, archivar, indexar, ficha, payload Zotero."""
    carpeta_pdfs = Path(carpeta_pdfs or rutas.PDFS_FUENTES)
    carpeta_notas = Path(carpeta_notas or rutas.NOTAS_FUENTES)
    res = verificar_doi(doi_entrada, **kw)
    res.update(pdf_local=None, sha256=None, paginas=None, ficha=None, zotero_payload=None, pdf_rechazados=[])
    if not res["verificado"]:
        return res
    meta, doi = res["metadatos"], res["doi"]

    previa = ficha_existente_para_doi(doi, carpeta_notas)
    if previa and not descargar:
        res["avisos"].append(f"Ya existe una ficha con este DOI: {previa.name}")
    if previa and descargar:
        res["estado"] = "ficha_existente"
        res["ficha"] = str(previa)
        res["avisos"].append(f"Ya existe una ficha con este DOI ({previa.name}); no se descarga ni se sobrescribe nada")
        pdf_previo = _pdf_de_ficha(previa)
        if pdf_previo:
            res["pdf_local"] = pdf_previo
        else:
            res["avisos"].append("[VERIFICAR: la ficha previa no declara 'pdf_local' válido (formato antiguo o sin PDF); "
                                 "no registrar en Zotero como con/sin PDF hasta confirmarlo]")
        res["zotero_payload"] = _payload(doi, pdf_previo, True, pdf_conocido=bool(pdf_previo))
        return res
    if not descargar:
        return res

    oa = consultar_openalex(doi, **kw)
    candidatos = list(dict.fromkeys(oa["pdf_urls"] + consultar_unpaywall(doi, **kw)))
    abstract, fuente_abs = meta.get("abstract"), "Crossref"
    if not abstract and oa["abstract"]:
        abstract, fuente_abs = oa["abstract"], "OpenAlex"
    fuente_meta = "Crossref" + (" + OpenAlex" if oa["pdf_urls"] or oa["abstract"] else "")

    pdf_ruta, sha, paginas, pdf_nuevo = None, None, None, False
    for url in candidatos:
        try:
            contenido = descargar_bytes(url, **kw)
        except requests.RequestException as e:
            res["pdf_rechazados"].append({"url": url, "motivo": f"descarga fallida: {e}"})
            continue
        try:
            v = validar_pdf(contenido, meta)
        except Exception as e:  # noqa: BLE001  (defensa en profundidad: un PDF hostil no aborta el lote)
            v = {"ok": False, "motivo": f"error inesperado al validar el PDF: {type(e).__name__}: {e}"}
        if not v["ok"]:
            res["pdf_rechazados"].append({"url": url, "motivo": v["motivo"]})
            continue
        try:
            pdf_ruta, duplicado = guardar_pdf(contenido, meta, carpeta_pdfs)
        except OSError as e:
            # PDF validado pero no archivable (ruta demasiado larga, disco, permisos): se informa, no se pierde la ficha.
            res["avisos"].append(f"[VERIFICAR: el PDF validado no pudo archivarse ({type(e).__name__}: {e}); "
                                 "descargarlo manualmente]")
            pdf_ruta = None
            break
        pdf_nuevo = not duplicado
        sha, paginas = seguridad.sha256_archivo(pdf_ruta), v["paginas"]
        if duplicado:
            res["avisos"].append(f"El PDF ya existía (mismo sha256): {pdf_ruta.name}; no se duplicó")
        break

    if pdf_ruta:
        try:
            idx = ingesta_pdf.cargar_indice(pdf_ruta, carpeta_indices)
            paginas = idx["fuente"]["n_paginas"]
            if idx["calidad"]["requiere_ocr"]:
                res["avisos"].append("El PDF tiene páginas sin capa de texto: requiere OCR para citarlas")
        except Exception as e:  # noqa: BLE001
            res["avisos"].append(f"[VERIFICAR: PDF archivado pero no se pudo indexar ({type(e).__name__}: {e})]")
        res["pdf_local"], res["sha256"], res["paginas"] = str(pdf_ruta), sha, paginas
    else:
        res["avisos"].append("PDF no disponible en acceso abierto: solicitar al tesista")

    datos = {"verificado": True, "pdf_local": res["pdf_local"], "sha256": sha, "paginas": paginas,
             "fuente_metadatos": fuente_meta, "abstract": abstract, "fuente_abstract": fuente_abs,
             "avisos": res["avisos"] + [f"PDF descartado ({r['url']}): {r['motivo']}" for r in res["pdf_rechazados"]]}
    try:
        ficha = crear_ficha(meta, res["citekey"], datos, carpeta_notas)
    except Exception as e:  # noqa: BLE001
        # Rollback: no dejar un PDF huérfano sin ficha (solo si lo creó esta corrida).
        if pdf_ruta and pdf_nuevo:
            try:
                Path(pdf_ruta).unlink()
            except OSError:
                pass
        res.update(estado="error_ficha", pdf_local=None, sha256=None, paginas=None)
        res["avisos"].append(f"[VERIFICAR: no se pudo crear la ficha ({type(e).__name__}: {e}); "
                             "se revirtió el PDF descargado para no dejar huérfanos]")
        return res
    res["ficha"] = str(ficha)
    res["citekey"] = ficha.stem.lstrip("@")
    res["estado"] = "completado" if pdf_ruta else "sin_pdf"
    res["zotero_payload"] = _payload(doi, res["pdf_local"], True)
    return res


def _pdf_de_ficha(ficha: Path) -> str | None:
    """Lee `pdf_local` del frontmatter de una ficha existente; None si falta, es null o el archivo no existe."""
    try:
        cab = "\n".join(ficha.read_text(encoding="utf-8").splitlines()[:40])
    except OSError:
        return None
    m = re.search(r"^pdf_local:\s*(.+)$", cab, re.M)
    if not m:
        return None
    try:
        valor = json.loads(m.group(1).strip())
    except ValueError:
        return None
    return valor if isinstance(valor, str) and Path(valor).exists() else None


def _payload(doi: str, pdf_local: str | None, verificado: bool, pdf_conocido: bool = True) -> dict:
    """Payload para zotero_add_item. `pdf_conocido=False`: no se evaluó el PDF (no se etiqueta)."""
    tags = ["sivac-thesis-lab", "verificado" if verificado else "por-verificar"]
    if pdf_conocido:
        tags.append("pdf-local" if pdf_local else "sin-pdf")
    return {"doi": doi, "coleccion": rutas.ZOTERO_COLECCION, "pdf_local": pdf_local, "tags": tags}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _resumen_humano(r: dict) -> str:
    l = [f"[{r['estado']}] {r.get('doi') or r.get('entrada')}"]
    if r.get("metadatos"):
        m = r["metadatos"]
        l.append(f"  título : {m['titulo']}")
        l.append(f"  autores: {', '.join(_autor_apa(a) for a in m['autores']) or '(sin autores)'}  año: {m['anio']}")
        l.append(f"  citekey: {r['citekey']}")
        l.append(f"  APA 7  : {r['referencia_apa7']}")
    if r.get("pdf_local"):
        l.append(f"  PDF    : {r['pdf_local']} ({r['paginas']} págs.)")
    if r.get("ficha"):
        l.append(f"  ficha  : {r['ficha']}")
    for x in r.get("pdf_rechazados") or []:
        l.append(f"  PDF descartado: {x['url']} -> {x['motivo']}")
    for a in r["avisos"]:
        l.append(f"  aviso  : {a}")
    if r.get("zotero_payload"):
        l.append("  zotero_payload: " + json.dumps(r["zotero_payload"], ensure_ascii=False))
    return "\n".join(l)


def _exito(r: dict) -> bool:
    return r["estado"] in ("completado", "sin_pdf", "ficha_existente", "verificada")


def _procesar_seguro(doi: str, **kw) -> dict:
    """procesar_doi sin propagar excepciones: un DOI problemático no aborta el lote."""
    try:
        return procesar_doi(doi, **kw)
    except Exception as e:  # noqa: BLE001
        return {"entrada": doi, "doi": normalizar_doi(doi), "estado": "error_inesperado", "verificado": False,
                "metadatos": None, "citekey": None, "referencia_apa7": None, "pdf_local": None,
                "avisos": [f"[VERIFICAR: error inesperado al procesar ({type(e).__name__}: {e})]"]}


def leer_lista_dois(ruta: Path) -> list[str]:
    """Lee un archivo de DOI (uno por línea; '#' comenta). Lanza ValueError con mensaje claro si no se puede usar.

    Acepta UTF-8 (con o sin BOM) y UTF-16/UTF-32 con BOM; cualquier otra codificación
    (p. ej. cp1252 del Bloc de notas) se rechaza en lugar de adivinarla.
    """
    import codecs

    ruta = Path(ruta)
    if not ruta.exists():
        raise ValueError(f"No existe el archivo: {ruta}")
    if not ruta.is_file():
        raise ValueError(f"La ruta no es un archivo: {ruta}")
    try:
        datos = ruta.read_bytes()
    except OSError as e:
        raise ValueError(f"No se pudo leer {ruta}: {type(e).__name__}: {e}") from e
    if datos.startswith((codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)):
        codificacion = "utf-32"
    elif datos.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        codificacion = "utf-16"
    else:
        codificacion = "utf-8-sig"
    try:
        texto = datos.decode(codificacion)
    except UnicodeDecodeError as e:
        raise ValueError(f"El archivo {ruta} no es texto UTF-8 válido ({e.reason} en el byte {e.start}); "
                         "guárdelo como UTF-8 (en el Bloc de notas: Guardar como > Codificación UTF-8).") from e
    if "\x00" in texto:
        raise ValueError(f"El archivo {ruta} contiene bytes nulos (¿UTF-16 sin BOM o archivo binario?); guárdelo como UTF-8.")
    lineas = [l.strip().lstrip("\ufeff").strip() for l in texto.splitlines()]
    dois = [l for l in lineas if l and not l.startswith("#")]
    if not dois:
        raise ValueError(f"El archivo {ruta} no contiene ningún DOI (vacío o solo comentarios); no se procesó nada.")
    return dois


def main(argv: list[str] | None = None) -> int:
    seguridad.configurar_utf8()
    ap = argparse.ArgumentParser(description="Descarga verificada de fuentes por DOI (Crossref + OA).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for nombre, ayuda in (("doi", "Verifica, descarga, archiva, indexa y crea la ficha"),
                          ("verificar", "Solo metadatos (no descarga ni escribe)")):
        p = sub.add_parser(nombre, help=ayuda)
        p.add_argument("doi")
        p.add_argument("--json", action="store_true")
    p = sub.add_parser("lote", help="Procesa un archivo con un DOI por línea")
    p.add_argument("--archivo", required=True, type=Path)
    p.add_argument("--solo-verificar", action="store_true")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("titulo", help="Lista candidatos de Crossref para un título (no elige ninguno)")
    p.add_argument("titulo")
    p.add_argument("--json", action="store_true")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0

    if a.cmd in ("doi", "verificar"):
        r = _procesar_seguro(a.doi, descargar=(a.cmd == "doi"))
        print(json.dumps(r, ensure_ascii=False, indent=1) if a.json else _resumen_humano(r))
        return 0 if _exito(r) else 1
    if a.cmd == "lote":
        try:
            dois = leer_lista_dois(a.archivo)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            return 2
        resultados = [_procesar_seguro(d, descargar=not a.solo_verificar) for d in dois]
        if a.json:
            print(json.dumps(resultados, ensure_ascii=False, indent=1))
        else:
            print("\n\n".join(_resumen_humano(r) for r in resultados))
        return 0 if all(_exito(r) for r in resultados) else 1
    if a.cmd == "titulo":
        try:
            cands = buscar_candidatos_titulo(a.titulo)
        except requests.RequestException as e:
            print(f"Error de red: {e}", file=sys.stderr)
            return 1
        if a.json:
            print(json.dumps(cands, ensure_ascii=False, indent=1))
        else:
            for c in cands:
                print(f"{c['similitud_titulo']:5.1f}  {c['doi']}  {c['anio']}  {c['titulo']}")
            print("Candidatos sin confirmar: elija el DOI correcto y use el subcomando 'verificar'.")
        return 0 if cands else 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
