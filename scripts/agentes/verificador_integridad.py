#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Verificador de integridad (Squad A).

Audita un texto (Markdown de la bóveda o .docx) en ocho frentes:

  1. Separa cuerpo y sección de Referencias.
  2. Extrae citas en texto: (Apellido, 2020), (A y B, 2020), (A et al., 2020), Apellido (2020),
     citas múltiples con ';', páginas (p. 12 / pp. 12-15) y citekeys @clave.
  3. Empareja citas <-> referencias (normalización sin tildes + rapidfuzz >= 90) y reporta:
     citas sin referencia, referencias huérfanas, discrepancias de año/autor.
  4. Valida los DOI (formato y existencia en Crossref; `--sin-red` omite la consulta) y compara
     primer autor, año y título con la referencia escrita.
  5. Cruza con la bóveda: ficha `notas_fuentes_zotero` o PDF indexado del autor/año.
  6. Detecta aserciones sin cita (cifras, porcentajes, años, «según») sin cita en la misma
     oración ni en la siguiente.
  7. Cuenta y lista las marcas [VERIFICAR].
  8. Verifica citas textuales entre comillas contra el PDF indexado (`scripts.fuentes.buscador_citas`).

Dictamen (criterios explícitos):
  * BLOQUEADO_ALERTA_ROJA        -> al menos una: cita sin referencia, DOI inexistente en Crossref
                                    (HTTP 404), cita textual no hallada en su PDF.
  * OBSERVADO_SUBSANABLE         -> sin alerta roja, pero con cualquier otra observación (referencia
                                    huérfana, discrepancia, DOI mal formado o no comprobado, aserción
                                    sin cita, [VERIFICAR], cita textual sin página o no comprobada...).
  * APROBADO_SIN_OBSERVACIONES   -> ninguna de las anteriores.

Principios anti-alucinación: lo que no puede confirmarse queda como «no comprobado» o
`[VERIFICAR: motivo]`; nunca se adivina un dato. Este script es de SOLO LECTURA sobre el texto
auditado; únicamente escribe el informe si se pide `--salida`.

Uso:
    python scripts/agentes/verificador_integridad.py CAPITULO.md [--json | --md] [--sin-red]
                 [--referencias CATALOGO.md] [--salida INFORME] [--sin-boveda]

Códigos de salida: 0 aprobado, 1 observado/bloqueado, 2 uso incorrecto.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

from rapidfuzz import fuzz
from unidecode import unidecode

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad  # noqa: E402
from scripts.fuentes import texto as tx  # noqa: E402

try:  # import tolerante (punto 8)
    from scripts.fuentes import buscador_citas as _bc
except Exception:  # noqa: BLE001
    _bc = None

APROBADO = "APROBADO_SIN_OBSERVACIONES"
OBSERVADO = "OBSERVADO_SUBSANABLE"
BLOQUEADO = "BLOQUEADO_ALERTA_ROJA"
ROJA, OBS, INFO = "ROJA", "OBSERVACION", "INFO"

UMBRAL_FUZZY = 90
CROSSREF_URL = "https://api.crossref.org/works/{doi}"

# ----------------------------------------------------------------------------------------
# Expresiones regulares
# ----------------------------------------------------------------------------------------
_MAY = "A-ZÁÉÍÓÚÑÜ"
_RE_ENCABEZADO_MD = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_RE_ENC_REFERENCIAS = re.compile(
    r"^(?:(?:cap[ií]tulo\s+\w+\s*[.:-]?\s*)?[\dIVXivx]+(?:\.\d+)*\.?\s*)?"
    r"(?:referencias|bibliograf[ií]a|lista de referencias)\b", re.I)
_RE_VERIFICAR = re.compile(r"\[VERIFICAR[^\]]*\]", re.I)
_RE_LOCALIZADOR = re.compile(r"(?:pp?\.|p[áa]gs?\.?)\s*(\d+(?:\s*[-–—]\s*\d+)?)", re.I)
_RE_ANIO = r"(?:19|20)\d{2}[a-z]?"
_RE_PARTE_PAREN = re.compile(
    rf"^(?P<a>[{_MAY}][^\d()]{{1,150}}?),?\s+(?P<y>{_RE_ANIO})"
    r"(?:\s*,\s*(?P<loc>(?:pp?\.|p[áa]gs?\.?)\s*\d+(?:\s*[-–—]\s*\d+)?))?\s*$")
_RE_PREFIJO_VEASE = re.compile(
    r"^(?:v[eé]ase|ver|cf\.|p\.\s*ej\.,?|por ejemplo,?|e\.\s*g\.,?|seg[úu]n)\s+", re.I)
_RE_NARRATIVA = re.compile(
    rf"\((?P<y>{_RE_ANIO})(?:\s*,\s*(?P<loc>(?:pp?\.|p[áa]gs?\.?)\s*\d+(?:\s*[-–—]\s*\d+)?))?\)")
_RE_CITEKEY = re.compile(r"(?<![\w.@])@([A-Za-z][\w:\-]*[A-Za-z0-9])")
_RE_GRUPO_CITEKEY = re.compile(r"\[[^\]\[]*@[^\]\[]*\]")
_RE_INICIAL = re.compile(rf"^[{_MAY}]\.,?$")
_RE_NOMBRE = re.compile(rf"^[{_MAY}][\wáéíóúñüÁÉÍÓÚÑÜ'’\-]*,?$")
_CONECTORES = {"y", "e", "&", "and", "de", "del", "la", "las", "los", "van", "von", "da", "di", "et", "al.", "al"}
_CONECTORES_Y = {"y", "e", "&", "and"}
_NO_AUTORES = {
    "tabla", "figura", "capítulo", "capitulo", "sección", "seccion", "apartado", "dimensión", "dimension",
    "indicador", "ley", "decreto", "resolución", "resolucion", "norma", "artículo", "articulo", "año", "versión",
    "version", "edición", "edicion", "ecuación", "ecuacion", "anexo", "hipótesis", "hipotesis", "objetivo"}
_ADVERBIOS = {
    "asimismo", "además", "ademas", "finalmente", "igualmente", "también", "tambien", "sin", "embargo", "por",
    "ejemplo", "así", "asi", "luego", "entonces", "primero", "segundo", "tercero", "según", "segun", "como",
    "mientras", "cuando", "aunque", "incluso", "adicionalmente", "posteriormente", "inicialmente"}

_RE_ABREV = re.compile(
    r"\b(?:et al|pp?|vs|etc|Dr|Dra|Ing|Sr|Sra|Bach|Lic|Mg|ej|cap|fig|núm|art|ed|aprox|cf|Nº|N°)\.", re.I)
_RE_INICIAL_SUELTA = re.compile(rf"\b[{_MAY}]\.")
_RE_FIN_ORACION = re.compile(rf"(?<=[.!?])\s+(?=[{_MAY}¿¡“\"(\[])")

_RE_PORCENTAJE = re.compile(r"\d+(?:[.,]\d+)?\s*(?:%|‰|por ciento)", re.I)
_RE_ANIO_SUELTO = re.compile(r"\b(?:19[5-9]\d|20[0-3]\d)\b")
_RE_CIFRA = re.compile(r"(?<![\w.,/-])(?:\d{1,3}(?:[.,]\d{3})+|\d+[.,]\d{2,}|\d{2,})(?![\w/-])")
_RE_SEGUN = re.compile(r"\b(?:seg[úu]n|de acuerdo con|conforme a|de acuerdo a)\b", re.I)
_RE_REFERENCIA_INTERNA = re.compile(
    r"\b(?:tabla|figura|cap[ií]tulo|secci[oó]n|apartado|dimensi[oó]n(?:es)?|indicador(?:es)?|objetivo|"
    r"hip[oó]tesis|[ií]tem|ecuaci[oó]n|anexo|fase|paso|art[ií]culo|n\.?[º°]|n[úu]mero)s?\s*[\d.]+(?:\s*(?:y|e|,)\s*[\d.]+)*",
    re.I)
_RE_TITULO_PREVIO = re.compile(r"(?:titulad[oa]s?|denominad[oa]s?|llamad[oa]s?|intitulad[oa]s?|t[ií]tulo|rotulad[oa]s?)[^\w]{0,6}$",
                               re.I)


# ----------------------------------------------------------------------------------------
# Utilidades de normalización
# ----------------------------------------------------------------------------------------
def norm(texto: str) -> str:
    """Minúsculas, sin tildes ni puntuación (apellidos y comparación difusa)."""
    t = unidecode(texto or "").lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return t.strip()


def _limpiar_md(texto: str) -> str:
    """Quita marcas de énfasis, matemáticas LaTeX y enlaces; conserva [VERIFICAR] y [@clave]."""
    t = re.sub(r"\$[^$\n]*\$", " ", texto)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"\[([^\]]+)\]\((?:https?://|#)[^)]*\)", r"\1", t)
    t = t.replace("**", "").replace("*", "")
    t = re.sub(r"(?<!\w)_|_(?!\w)", "", t)
    t = t.replace("<br>", " ").replace("&nbsp;", " ")
    return re.sub(r"[ \t]+", " ", t).strip()


def _apellidos_cita(a: str) -> list[str]:
    return [norm(x) for x in re.split(r"\s+(?:y|e|&|and)\s+|,\s*", a) if norm(x) and norm(x) not in {"et al", "al"}]


def coincide_apellido(cita: str, ref: str) -> int:
    """Puntaje 0-100 de coincidencia de apellido (tolerante a grafía y a apellido compuesto parcial)."""
    c, r = norm(cita), norm(ref)
    if not c or not r:
        return 0
    if c == r:
        return 100
    ct, rt = c.split(), r.split()
    if set(ct) <= set(rt) or set(rt) <= set(ct):
        return 100
    return int(fuzz.ratio(c, r))


# ----------------------------------------------------------------------------------------
# 1. Lectura y división del documento
# ----------------------------------------------------------------------------------------
def leer_lineas(ruta: Path) -> list[dict]:
    """Devuelve líneas {n, texto, nivel}; nivel = 1..6 si es encabezado, si no 0."""
    ruta = Path(ruta)
    ext = ruta.suffix.lower()
    if ext == ".docx":
        return _leer_docx(ruta)
    if ext in {".md", ".markdown", ".txt"}:
        return _leer_md(ruta.read_text(encoding="utf-8-sig"))
    raise ValueError(f"extensión no soportada: {ext} (use .md o .docx)")


def _leer_md(contenido: str) -> list[dict]:
    lineas = contenido.splitlines()
    inicio = 0
    if lineas and lineas[0].strip() == "---":  # frontmatter YAML
        for i in range(1, len(lineas)):
            if lineas[i].strip() == "---":
                inicio = i + 1
                break
    salida, en_codigo = [], False
    for i in range(inicio, len(lineas)):
        bruta = lineas[i]
        if bruta.strip().startswith("```"):
            en_codigo = not en_codigo
            continue
        if en_codigo:
            continue
        m = _RE_ENCABEZADO_MD.match(bruta)
        salida.append({"n": i + 1, "texto": m.group(2) if m else bruta, "nivel": len(m.group(1)) if m else 0,
                       "raw": bruta})
    return salida


def _leer_docx(ruta: Path) -> list[dict]:
    import docx  # python-docx

    d = docx.Document(str(ruta))
    salida, n = [], 0
    for p in d.paragraphs:
        n += 1
        estilo = (p.style.name or "").lower() if p.style is not None else ""
        nivel = 0
        m = re.match(r"(?:heading|t[ií]tulo)\s*(\d)", estilo)
        if m:
            nivel = int(m.group(1))
        elif estilo == "title":
            nivel = 1
        texto = p.text.strip()
        if not texto:
            salida.append({"n": n, "texto": "", "nivel": 0, "raw": ""})
            continue
        if not nivel and len(texto) < 70 and _RE_ENC_REFERENCIAS.match(texto):
            nivel = 1
        salida.append({"n": n, "texto": texto, "nivel": nivel, "raw": texto})
    for t in d.tables:
        for fila in t.rows:
            n += 1
            celdas = []
            for c in fila.cells:
                if c.text.strip() and c.text.strip() not in celdas:
                    celdas.append(c.text.strip())
            if celdas:
                salida.append({"n": n, "texto": "| " + " | ".join(celdas) + " |", "nivel": 0,
                               "raw": "| " + " | ".join(celdas) + " |"})
    return salida


def dividir_cuerpo_y_referencias(lineas: list[dict]) -> tuple[list[dict], list[dict], bool]:
    """(cuerpo, lineas_referencias, encontrada). La sección termina en el siguiente encabezado del mismo o mayor rango."""
    idx = None
    for i, ln in enumerate(lineas):
        es_enc = ln["nivel"] > 0 or (len(ln["texto"]) < 70 and ln["texto"].isupper())
        if es_enc and _RE_ENC_REFERENCIAS.match(_limpiar_md(ln["texto"])):
            idx = i
            break
    if idx is None:
        return lineas, [], False
    nivel = lineas[idx]["nivel"] or 1
    fin = len(lineas)
    for j in range(idx + 1, len(lineas)):
        if 0 < lineas[j]["nivel"] <= nivel:
            fin = j
            break
    return lineas[:idx] + lineas[fin:], lineas[idx + 1:fin], True


def construir_bloques(lineas: list[dict]) -> list[dict]:
    """Agrupa líneas en bloques {linea, texto, tipo}: encabezado, tabla (una fila por bloque) o párrafo."""
    bloques, buf, ini = [], [], None

    def volcar():
        nonlocal buf, ini
        if buf:
            bloques.append({"linea": ini, "texto": _limpiar_md(" ".join(buf)), "tipo": "parrafo"})
        buf, ini = [], None

    for ln in lineas:
        t = ln["texto"].strip()
        if ln["nivel"] > 0:
            volcar()
            bloques.append({"linea": ln["n"], "texto": _limpiar_md(t), "tipo": "encabezado"})
        elif not t or re.fullmatch(r"[-=_*\s]{3,}", t):
            volcar()
        elif t.startswith("|"):
            volcar()
            if re.fullmatch(r"\|[\s:|\-]+\|?", t):
                continue
            bloques.append({"linea": ln["n"], "texto": _limpiar_md(t.strip("| ")), "tipo": "tabla"})
        elif t.startswith(">"):
            volcar()
            bloques.append({"linea": ln["n"], "texto": _limpiar_md(t.lstrip("> ")), "tipo": "parrafo"})
        else:
            if ini is None:
                ini = ln["n"]
            buf.append(re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", t) if not buf else t)
    volcar()
    return bloques


# ----------------------------------------------------------------------------------------
# 2. Extracción de citas en texto
# ----------------------------------------------------------------------------------------
def _primer_autor_narrativa(prefijo: str) -> tuple[str, list[str], int] | None:
    """Camina hacia atrás desde «(año)» recolectando el bloque de autores.

    Devuelve (texto_autores, autores, offset_inicio) o None.
    """
    toks = [(m.group(), m.start()) for m in re.finditer(r"\S+", prefijo)]
    recogidos: list[tuple[str, int]] = []
    for tok, pos in reversed(toks[-40:]):
        base = tok.rstrip(",")
        bajo = base.lower()
        if _RE_INICIAL.match(tok) or bajo == "al." or bajo in _CONECTORES or _RE_NOMBRE.match(tok):
            recogidos.append((tok, pos))
            # un punto final (que no sea inicial / "al.") corta: la palabra ya se tomó, pero no se sigue
            continue
        break
    recogidos.reverse()
    # recortar conectores iniciales y adverbios de inicio de oración
    while recogidos:
        base = recogidos[0][0].rstrip(",")
        bajo = base.lower()
        if bajo in _CONECTORES or bajo in _NO_AUTORES and False:
            recogidos.pop(0)
        elif recogidos[0][0].endswith(",") and (bajo in _ADVERBIOS or bajo.endswith("mente")):
            recogidos.pop(0)
        elif bajo in _ADVERBIOS or bajo.endswith("mente"):
            recogidos.pop(0)
        else:
            break
    # tokens que terminan en «.» y no son inicial ni «al.» son fin de oración: quedarse con lo posterior
    for i in range(len(recogidos) - 1, -1, -1):
        t = recogidos[i][0]
        if t.endswith(".") and not _RE_INICIAL.match(t) and t.lower() != "al.":
            recogidos = recogidos[i + 1:]
            break
    if not recogidos:
        return None
    palabras = [t for t, _ in recogidos]
    hay_inicial = any(_RE_INICIAL.match(t) for t in palabras)
    hay_y = any(t.lower() in _CONECTORES_Y for t in palabras)
    if not hay_inicial and not hay_y and any(t.endswith(",") for t in palabras[:-1]):
        # «Metodológicamente, Shen et al.»: solo cuenta lo posterior a la última coma
        k = max(i for i, t in enumerate(palabras[:-1]) if t.endswith(",")) + 1
        recogidos, palabras = recogidos[k:], palabras[k:]
    while recogidos and recogidos[0][0].lower().rstrip(",") in _CONECTORES:
        recogidos.pop(0)
        palabras.pop(0)
    if not palabras:
        return None
    # primer autor: hasta la primera coma / conector «y» / «et»
    nombre: list[str] = []
    for t in palabras:
        if t.lower().rstrip(",") in {"y", "e", "&", "and", "et"}:
            break
        nombre.append(t.rstrip(","))
        if t.endswith(","):
            break
    primer = " ".join(nombre).strip()
    if not primer or primer.lower() in _NO_AUTORES or _RE_INICIAL.match(primer):
        return None
    autores = [primer]
    resto = " ".join(palabras[len(nombre):])
    if "et al" not in resto.lower() and not hay_inicial:
        extra = [x.strip(" ,") for x in re.split(r"\s+(?:y|e|&|and)\s+|,\s*", resto) if x.strip(" ,")]
        autores += [x for x in extra if x.lower() not in {"et", "al.", "al"}]
    return " ".join(palabras), autores, recogidos[0][1]


def extraer_citas(bloques: list[dict]) -> list[dict]:
    """Citas en texto de todos los bloques; cada una con bloque, posición y oración por resolver después."""
    citas: list[dict] = []
    for bi, b in enumerate(bloques):
        texto = b["texto"]
        if not texto:
            continue
        ocupado: list[tuple[int, int]] = []

        # a) Citekeys estilo Pandoc [@a; @b, p. 12] y @clave sueltas
        for g in _RE_GRUPO_CITEKEY.finditer(texto):
            loc = _RE_LOCALIZADOR.search(g.group())
            for k in _RE_CITEKEY.finditer(g.group()):
                citas.append(_cita("citekey", b, bi, g.start(), g.end(), g.group(), [], None,
                                   _norm_loc(loc), k.group(1)))
            ocupado.append((g.start(), g.end()))
        for k in _RE_CITEKEY.finditer(texto):
            if not any(a <= k.start() < z for a, z in ocupado):
                citas.append(_cita("citekey", b, bi, k.start(), k.end(), k.group(), [], None, None, k.group(1)))
                ocupado.append((k.start(), k.end()))

        # b) Parentéticas (Autor, 2020; Otro et al., 2021, p. 3)
        for m in re.finditer(r"\(([^()]{3,400})\)", texto):
            if any(a <= m.start() < z for a, z in ocupado):
                continue
            partes = [p.strip() for p in m.group(1).split(";")]
            validas = []
            for p in partes:
                p2 = _RE_PREFIJO_VEASE.sub("", p)
                mp = _RE_PARTE_PAREN.match(p2)
                if mp and mp.group("a").strip().lower().split()[0] not in _NO_AUTORES:
                    validas.append((p2, mp))
            if not validas:
                continue
            for p2, mp in validas:
                a = mp.group("a").strip()
                autores = [x for x in _apellidos_lista(a)]
                citas.append(_cita("parentetica", b, bi, m.start(), m.end(), f"({p2})", autores,
                                   mp.group("y"), _norm_loc(mp.group("loc") and _RE_LOCALIZADOR.search(mp.group("loc"))),
                                   None, et_al=bool(re.search(r"\bet al\b", a, re.I))))
            ocupado.append((m.start(), m.end()))

        # c) Narrativas: Autor (2020) / Autor et al. (2020, p. 3)
        for m in _RE_NARRATIVA.finditer(texto):
            if any(a <= m.start() < z for a, z in ocupado):
                continue
            prefijo = texto[:m.start()]
            r = _primer_autor_narrativa(prefijo)
            if not r:
                continue
            bloque_autores, autores, inicio = r
            loc = _RE_LOCALIZADOR.search(m.group("loc") or "")
            citas.append(_cita("narrativa", b, bi, inicio, m.end(), texto[inicio:m.end()], autores, m.group("y"),
                               _norm_loc(loc), None, et_al="et al" in bloque_autores.lower()))
            ocupado.append((inicio, m.end()))
    return citas


def _apellidos_lista(a: str) -> list[str]:
    a = re.sub(r"\bet al\.?", "", a, flags=re.I)
    return [x.strip() for x in re.split(r"\s+(?:y|e|&|and)\s+|,\s*", a) if x.strip(" .")]


def _norm_loc(m) -> str | None:
    if not m:
        return None
    num = m.group(1) if hasattr(m, "group") else str(m)
    return re.sub(r"\s*[-–—]\s*", "-", num).strip()


def _cita(tipo, bloque, bi, ini, fin, texto, autores, anio, loc, clave, et_al=False) -> dict:
    return {"tipo": tipo, "texto": texto.strip(), "autor1": autores[0] if autores else None, "autores": autores,
            "et_al": et_al, "anio": anio, "localizador": loc, "citekey": clave, "linea": bloque["linea"],
            "_bloque": bi, "_ini": ini, "_fin": fin}


# ----------------------------------------------------------------------------------------
# 3. Referencias
# ----------------------------------------------------------------------------------------
_RE_ANIO_REF = re.compile(rf"\(\s*({_RE_ANIO}|s\.\s?f\.|n\.d\.)\s*\)")


def parsear_referencias(lineas: list[dict]) -> list[dict]:
    """Entradas APA de una sección de referencias (lista numerada, viñetas o párrafos)."""
    entradas: list[list[dict]] = []
    actual: list[dict] = []
    for ln in lineas:
        t = ln["texto"].strip()
        if ln["nivel"] > 0 or t.startswith(">") or re.fullmatch(r"[-=_*\s]{3,}", t) or t.startswith("|"):
            if actual:
                entradas.append(actual)
                actual = []
            continue
        if not t:
            if actual:
                entradas.append(actual)
                actual = []
            continue
        if re.match(r"^\s*(?:\d+[.)]|[-*+])\s+", t) and actual:
            entradas.append(actual)
            actual = []
        actual.append({"n": ln["n"], "t": re.sub(r"^\s*(?:\d+[.)]|[-*+])\s+", "", t)})
    if actual:
        entradas.append(actual)
    salida = []
    for e in entradas:
        bruto = " ".join(x["t"] for x in e)
        ref = parsear_referencia(bruto, e[0]["n"])
        if ref:
            salida.append(ref)
    return salida


def parsear_referencia(bruto: str, linea: int = 0) -> dict | None:
    claves = re.findall(r"(?<![\w.@])@([A-Za-z][\w:\-]*[A-Za-z0-9])", bruto)
    limpio = _limpiar_md(re.sub(r"`[^`]*`", " ", bruto))
    m = _RE_ANIO_REF.search(limpio)
    if not m:
        return None
    antes = limpio[:m.start()].strip(" .")
    anio = m.group(1).lower()
    resto = limpio[m.end():].lstrip(". ")
    titulo = re.split(r"\.\s", resto, maxsplit=1)[0].strip(" .“”\"") if resto else ""
    titulo = re.sub(r"\[[^\]]*\]", "", titulo).strip(" .")
    surnames = re.findall(
        rf"(?:^|[,&]\s*|\by\s+)(?:&\s*)?([{_MAY}][^,&]*?),\s*(?:[{_MAY}]\.[\s\-]*)+", antes)
    surnames = [s.strip() for s in surnames if s.strip()]
    if not surnames:  # autor corporativo o sin iniciales
        surnames = [re.split(r",", antes)[0].strip()] if antes else []
    doi = tx.extraer_doi(limpio)
    return {"linea": linea, "texto": limpio, "autor1": surnames[0] if surnames else None, "autores": surnames,
            "anio": anio, "titulo": titulo, "doi": doi.lower() if doi else None, "citekeys": claves,
            "doi_bruto": doi}


# ----------------------------------------------------------------------------------------
# Emparejamiento citas <-> referencias
# ----------------------------------------------------------------------------------------
def emparejar(citas: list[dict], refs: list[dict]) -> dict:
    """Asigna a cada cita su referencia (o la ausencia) y arma los hallazgos de correspondencia."""
    hallazgos: list[dict] = []
    usadas: set[int] = set()
    clave_a_ref = {k.lower(): i for i, r in enumerate(refs) for k in r["citekeys"]}
    for c in citas:
        c["ref"] = None
        c["estado"] = None
        if c["tipo"] == "citekey":
            i = clave_a_ref.get((c["citekey"] or "").lower())
            if i is None:
                c["estado"] = "sin_referencia"
                hallazgos.append(_h("CITA_SIN_REFERENCIA", ROJA, c["linea"],
                                    f"La citekey @{c['citekey']} no corresponde a ninguna referencia.", c["texto"]))
            else:
                c["ref"], c["estado"] = i, "ok"
                usadas.add(i)
            continue
        cand = [(coincide_apellido(c["autor1"], r["autor1"] or ""), i) for i, r in enumerate(refs)]
        cand = [(s, i) for s, i in cand if s >= UMBRAL_FUZZY]
        if not cand:
            c["estado"] = "sin_referencia"
            hallazgos.append(_h("CITA_SIN_REFERENCIA", ROJA, c["linea"],
                                f"Cita «{c['texto']}» sin referencia correspondiente (primer autor: {c['autor1']}).",
                                c["texto"]))
            continue
        mismo_anio = [(s, i) for s, i in cand if refs[i]["anio"] == (c["anio"] or "").lower()]
        if not mismo_anio:  # misma letra de sufijo ausente: comparar solo el número
            mismo_anio = [(s, i) for s, i in cand
                          if refs[i]["anio"][:4] == (c["anio"] or "")[:4] and
                          (len(refs[i]["anio"]) == 4 or len((c["anio"] or "")) == 4)]
        if not mismo_anio:
            s, i = max(cand)
            c["ref"], c["estado"] = i, "discrepancia_anio"
            usadas.add(i)
            hallazgos.append(_h(
                "DISCREPANCIA_ANIO", OBS, c["linea"],
                f"Cita «{c['texto']}» con año {c['anio']}; la referencia de {refs[i]['autor1']} indica {refs[i]['anio']}.",
                c["texto"]))
            continue
        s, i = max(mismo_anio)
        c["ref"], c["estado"] = i, "ok"
        usadas.add(i)
        # segundo autor (solo si la cita lista explícitamente dos autores)
        if len(c["autores"]) >= 2 and not c["et_al"] and len(refs[i]["autores"]) >= 2:
            for k, a in enumerate(c["autores"][1:], start=1):
                if k < len(refs[i]["autores"]) and coincide_apellido(a, refs[i]["autores"][k]) < UMBRAL_FUZZY:
                    c["estado"] = "discrepancia_autor"
                    hallazgos.append(_h(
                        "DISCREPANCIA_AUTOR", OBS, c["linea"],
                        f"En «{c['texto']}» el autor n.º {k + 1} «{a}» no coincide con la referencia "
                        f"({refs[i]['autores'][k]}).", c["texto"]))
                    break
    return {"hallazgos": hallazgos, "usadas": usadas}


def _h(codigo: str, severidad: str, linea, mensaje: str, detalle: str = "") -> dict:
    return {"codigo": codigo, "severidad": severidad, "linea": linea, "mensaje": mensaje, "detalle": detalle}


# ----------------------------------------------------------------------------------------
# 4. DOI
# ----------------------------------------------------------------------------------------
def consultar_crossref(doi: str, timeout: float = 15.0) -> dict:
    """Consulta Crossref. {'existe': True|False|None, 'titulo','autor1','anios','error'}.

    existe=False solo ante HTTP 404 (el DOI no está registrado); cualquier otro fallo -> None (no comprobado).
    """
    import requests

    try:
        r = requests.get(CROSSREF_URL.format(doi=quote(doi, safe="/")), timeout=timeout,
                         headers={"User-Agent": "SIVAC-THESIS-LAB/1.0 (verificacion-bibliografica)"})
    except Exception as e:  # noqa: BLE001
        return {"existe": None, "error": f"{type(e).__name__}: {e}"}
    if r.status_code == 404:
        return {"existe": False, "error": "HTTP 404 (DOI no registrado en Crossref)"}
    if r.status_code != 200:
        return {"existe": None, "error": f"HTTP {r.status_code}"}
    try:
        msg = r.json()["message"]
    except Exception as e:  # noqa: BLE001
        return {"existe": None, "error": f"respuesta ilegible: {e}"}
    autor1 = None
    for a in msg.get("author") or []:
        autor1 = a.get("family") or a.get("name")
        if autor1:
            break
    anios = []
    for k in ("issued", "published-print", "published-online", "published"):
        try:
            anios.append(str(msg[k]["date-parts"][0][0]))
        except Exception:  # noqa: BLE001
            pass
    titulo = (msg.get("title") or [""])[0]
    return {"existe": True, "titulo": titulo, "autor1": autor1, "anios": sorted(set(anios)), "error": None}


def comparar_con_crossref(ref: dict, meta: dict) -> list[str]:
    """Discrepancias entre la referencia escrita y Crossref (primer autor, año, título aproximado)."""
    d = []
    if meta.get("autor1") and ref.get("autor1") and coincide_apellido(meta["autor1"], ref["autor1"]) < 85:
        d.append(f"primer autor: referencia «{ref['autor1']}» vs Crossref «{meta['autor1']}»")
    if meta.get("anios") and ref.get("anio") and ref["anio"][:4] not in meta["anios"]:
        d.append(f"año: referencia {ref['anio']} vs Crossref {'/'.join(meta['anios'])}")
    if meta.get("titulo") and ref.get("titulo"):
        s = fuzz.token_set_ratio(norm(ref["titulo"]), norm(meta["titulo"]))
        if s < 80:
            d.append(f"título poco similar (similitud {s:.0f}): «{ref['titulo'][:70]}» vs «{meta['titulo'][:70]}»")
    return d


def validar_dois(refs: list[dict], sin_red: bool, consultor=None) -> tuple[list[dict], list[dict]]:
    consultor = consultor or consultar_crossref
    filas, hallazgos, cache = [], [], {}
    for r in refs:
        if not r["doi_bruto"]:
            filas.append({"referencia": _etiqueta_ref(r), "doi": None, "formato": None, "crossref": "sin DOI",
                          "discrepancias": []})
            continue
        doi = r["doi_bruto"]
        formato = bool(re.fullmatch(r"10\.\d{4,9}/\S+", doi))
        fila = {"referencia": _etiqueta_ref(r), "doi": doi, "formato": formato, "crossref": None, "discrepancias": []}
        if not formato:
            fila["crossref"] = "formato inválido"
            hallazgos.append(_h("DOI_FORMATO", OBS, r["linea"], f"DOI con formato inválido: {doi}", _etiqueta_ref(r)))
        elif sin_red:
            fila["crossref"] = "no comprobado (--sin-red)"
            hallazgos.append(_h("DOI_NO_COMPROBADO", INFO, r["linea"],
                                f"DOI {doi} sin resolver contra Crossref (--sin-red).", _etiqueta_ref(r)))
        else:
            meta = cache.get(doi.lower()) or consultor(doi)
            cache[doi.lower()] = meta
            if meta.get("existe") is False:
                fila["crossref"] = "INEXISTENTE"
                hallazgos.append(_h("DOI_INEXISTENTE", ROJA, r["linea"],
                                    f"El DOI {doi} no existe en Crossref ({meta.get('error')}).", _etiqueta_ref(r)))
            elif meta.get("existe") is None:
                fila["crossref"] = f"no comprobado ({meta.get('error')})"
                hallazgos.append(_h("DOI_NO_COMPROBADO", OBS, r["linea"],
                                    f"DOI {doi} no pudo comprobarse: {meta.get('error')}.", _etiqueta_ref(r)))
            else:
                disc = comparar_con_crossref(r, meta)
                fila["crossref"] = "existe" if not disc else "existe con discrepancias"
                fila["discrepancias"] = disc
                fila["crossref_meta"] = {k: meta.get(k) for k in ("titulo", "autor1", "anios")}
                for x in disc:
                    hallazgos.append(_h("DOI_DISCREPANCIA", OBS, r["linea"], f"DOI {doi}: {x}", _etiqueta_ref(r)))
        filas.append(fila)
    return filas, hallazgos


def _etiqueta_ref(r: dict) -> str:
    return f"{r.get('autor1') or '?'} ({r.get('anio') or 's. f.'})"


# ----------------------------------------------------------------------------------------
# 5. Cruce con la bóveda
# ----------------------------------------------------------------------------------------
def _frontmatter(ruta: Path) -> dict:
    try:
        t = ruta.read_text(encoding="utf-8-sig")
    except Exception:  # noqa: BLE001
        return {}
    if not t.startswith("---"):
        return {}
    fin = t.find("\n---", 3)
    bloque = t[3:fin] if fin > 0 else ""
    d = {}
    for ln in bloque.splitlines():
        m = re.match(r"^([\wáéíóúñ]+)\s*:\s*(.*)$", ln)
        if m:
            d[m.group(1).lower()] = m.group(2).strip().strip("\"'")
    return d


class Boveda:
    """Fichas Zotero y PDFs indexados (solo lectura; carga perezosa)."""

    def __init__(self, carpeta_fichas: Path | None = None, carpeta_pdfs: Path | None = None,
                 carpeta_indices: Path | None = None):
        self.carpeta_fichas = Path(carpeta_fichas) if carpeta_fichas else rutas.NOTAS_FUENTES
        self.carpeta_pdfs = Path(carpeta_pdfs) if carpeta_pdfs else rutas.PDFS_FUENTES
        self.carpeta_indices = Path(carpeta_indices) if carpeta_indices else rutas.INDICES_PDF
        self._fichas: list[dict] | None = None
        self._pdfs: list[Path] | None = None
        self._dois_pdf: dict[str, Path] | None = None

    @property
    def fichas(self) -> list[dict]:
        if self._fichas is None:
            self._fichas = []
            if self.carpeta_fichas.exists():
                for p in sorted(self.carpeta_fichas.glob("*.md")):
                    fm = _frontmatter(p)
                    if fm:
                        fm["_archivo"] = p.name
                        self._fichas.append(fm)
        return self._fichas

    @property
    def pdfs(self) -> list[Path]:
        if self._pdfs is None:
            self._pdfs = sorted(self.carpeta_pdfs.glob("*.pdf")) if self.carpeta_pdfs.exists() else []
        return self._pdfs

    @property
    def dois_pdf(self) -> dict[str, Path]:
        if self._dois_pdf is None:
            self._dois_pdf = {}
            if self.carpeta_indices.exists():
                for pdf in self.pdfs:
                    idx = self.carpeta_indices / (tx.slug(pdf.stem, 80) + ".idx.json")
                    if idx.exists():
                        try:
                            doi = json.loads(idx.read_text(encoding="utf-8"))["fuente"].get("doi_detectado")
                        except Exception:  # noqa: BLE001
                            doi = None
                        if doi:
                            self._dois_pdf[doi.lower()] = pdf
        return self._dois_pdf

    def buscar_ficha(self, ref: dict) -> dict | None:
        for f in self.fichas:
            if ref["doi"] and f.get("doi", "").lower() == ref["doi"]:
                return f
            if any(k.lower() == (f.get("citekey") or "").lower() for k in ref["citekeys"]) and f.get("citekey"):
                return f
        ap = norm(ref["autor1"] or "")
        for f in self.fichas:
            anio = (f.get("anio") or f.get("ano") or f.get("año") or f.get("year") or "")[:4]
            if anio and anio == ref["anio"][:4] and ap:
                autores = norm(f.get("autores") or f.get("autor") or "")
                primero = norm(re.split(r",|&| y ", f.get("autores") or "")[0]) if f.get("autores") else ""
                if primero and (set(ap.split()) <= set(primero.split()) or coincide_apellido(ap, primero) >= UMBRAL_FUZZY):
                    return f
                if ap and ap in autores and len(ap) > 3:
                    return f
        tit = norm(ref["titulo"] or "")
        if len(tit) > 20:
            for f in self.fichas:
                if fuzz.ratio(tit, norm(f.get("titulo") or "")) >= 90:
                    return f
        return None

    def buscar_pdf(self, ref: dict, ficha: dict | None) -> Path | None:
        if ficha:
            for k in ("archivo_pdf", "pdf_cotejado"):
                nombre = Path((ficha.get(k) or "").replace("\\", "/")).name
                if nombre:
                    for p in self.pdfs:
                        if p.name == nombre:
                            return p
        if ref["doi"] and ref["doi"] in self.dois_pdf:
            return self.dois_pdf[ref["doi"]]
        tit = norm(ref["titulo"] or "")
        if len(tit) >= 25:
            mejor = None
            for p in self.pdfs:
                stem = norm(p.stem)
                if len(stem) < 20:
                    continue
                if tit.startswith(stem[:60]) or stem.startswith(tit[:60]):
                    return p
                s = fuzz.ratio(stem[:70], tit[:len(stem[:70])])
                if s >= 92 and (mejor is None or s > mejor[0]):
                    mejor = (s, p)
            if mejor:
                return mejor[1]
        return None


def cruzar_boveda(refs: list[dict], usadas: set[int], boveda: Boveda | None) -> tuple[list[dict], list[dict]]:
    filas, hallazgos = [], []
    for i, r in enumerate(refs):
        fila = {"referencia": _etiqueta_ref(r), "citada": i in usadas, "ficha": None, "pdf": None,
                "estado": "sin_boveda"}
        if boveda is not None:
            ficha = boveda.buscar_ficha(r)
            pdf = boveda.buscar_pdf(r, ficha)
            fila["ficha"] = ficha["_archivo"] if ficha else None
            fila["pdf"] = pdf.name if pdf else None
            fila["_pdf_ruta"] = str(pdf) if pdf else None
            fila["estado"] = "respaldada" if (ficha or pdf) else "sin_respaldo"
            if i in usadas and not (ficha or pdf):
                hallazgos.append(_h(
                    "SIN_RESPALDO_BOVEDA", OBS, r["linea"],
                    f"{_etiqueta_ref(r)}: sin ficha en notas_fuentes_zotero ni PDF indexado; "
                    f"{'solo respaldada por DOI' if r['doi'] else 'sin DOI'} [VERIFICAR: registrar en Zotero].",
                    r["texto"][:160]))
        filas.append(fila)
    return filas, hallazgos


# ----------------------------------------------------------------------------------------
# 6. Aserciones sin cita
# ----------------------------------------------------------------------------------------
def _oraciones(texto: str) -> list[tuple[int, int]]:
    """Spans (ini, fin) de oraciones, protegiendo abreviaturas e iniciales."""
    prot = _RE_ABREV.sub(lambda m: m.group().replace(".", "\u0001"), texto)
    prot = _RE_INICIAL_SUELTA.sub(lambda m: m.group().replace(".", "\u0001"), prot)
    spans, ini = [], 0
    for m in _RE_FIN_ORACION.finditer(prot):
        spans.append((ini, m.start()))
        ini = m.end()
    spans.append((ini, len(texto)))
    return [(a, b) for a, b in spans if texto[a:b].strip()]


def detectar_aserciones_sin_cita(bloques: list[dict], citas: list[dict]) -> list[dict]:
    por_bloque: dict[int, list[dict]] = {}
    for c in citas:
        por_bloque.setdefault(c["_bloque"], []).append(c)
    salida = []
    for bi, b in enumerate(bloques):
        if b["tipo"] == "encabezado" or not b["texto"]:
            continue
        texto = b["texto"]
        spans = [(0, len(texto))] if b["tipo"] == "tabla" else _oraciones(texto)
        cites_b = por_bloque.get(bi, [])
        tiene = []
        for (a, z) in spans:
            tiene.append(any(a <= c["_ini"] < z or a < c["_fin"] <= z for c in cites_b))
        for k, (a, z) in enumerate(spans):
            if tiene[k] or (k + 1 < len(spans) and tiene[k + 1]):
                continue
            oracion = texto[a:z]
            limpia = oracion
            limpia = _RE_VERIFICAR.sub(" ", limpia)
            limpia = _RE_REFERENCIA_INTERNA.sub(" ", limpia)
            disparadores = []
            if _RE_PORCENTAJE.search(limpia):
                disparadores.append("porcentaje")
            if _RE_ANIO_SUELTO.search(limpia):
                disparadores.append("año")
            sin_pct = _RE_PORCENTAJE.sub(" ", limpia)
            sin_pct = _RE_ANIO_SUELTO.sub(" ", sin_pct)
            if _RE_CIFRA.search(sin_pct):
                disparadores.append("cifra")
            if _RE_SEGUN.search(limpia):
                disparadores.append("«según»")
            if disparadores:
                salida.append({"linea": b["linea"], "oracion": oracion.strip()[:220],
                               "disparadores": disparadores})
    return salida


# ----------------------------------------------------------------------------------------
# 7. Marcas [VERIFICAR]
# ----------------------------------------------------------------------------------------
def listar_verificar(lineas: list[dict]) -> list[dict]:
    return [{"linea": ln["n"], "marca": m.group()} for ln in lineas for m in _RE_VERIFICAR.finditer(ln["texto"])]


# ----------------------------------------------------------------------------------------
# 8. Citas textuales
# ----------------------------------------------------------------------------------------
_RE_COMILLAS = re.compile(r"“([^”]{20,}?)”|\"([^\"\n]{20,}?)\"|«([^»]{20,}?)»")


def _primera_pagina(loc: str | None) -> str | None:
    return re.split(r"-", loc)[0].strip() if loc else None


def verificar_citas_textuales(bloques: list[dict], citas: list[dict], refs: list[dict],
                              filas_boveda: list[dict], buscador=None) -> tuple[list[dict], list[dict]]:
    buscador = buscador if buscador is not None else _bc
    por_bloque: dict[int, list[dict]] = {}
    for c in citas:
        por_bloque.setdefault(c["_bloque"], []).append(c)
    resultados, hallazgos = [], []
    for bi, b in enumerate(bloques):
        if b["tipo"] == "encabezado":
            continue
        texto = b["texto"]
        for m in _RE_COMILLAS.finditer(texto):
            frag = next(g for g in m.groups() if g).strip()
            if len(frag.split()) < 6:
                continue
            if _RE_TITULO_PREVIO.search(texto[max(0, m.start() - 24):m.start()]):
                continue  # título de obra, no cita textual
            # cita asociada: la más cercana dentro de la ventana [-200, +160]
            cand = [c for c in por_bloque.get(bi, []) if -160 <= c["_ini"] - m.end() <= 200 or
                    (c["_ini"] <= m.start() and m.start() - c["_fin"] <= 200)]
            if not cand:
                continue  # entrecomillado sin cita cercana: fuera de alcance (podría ser término o cita de otro texto)
            c = min(cand, key=lambda x: abs(x["_ini"] - m.end()))
            res = {"linea": b["linea"], "fragmento": frag[:200], "cita": c["texto"], "pagina_citada": c["localizador"],
                   "estado": None, "detalle": ""}
            if not c["localizador"]:
                hallazgos.append(_h("CITA_TEXTUAL_SIN_PAGINA", OBS, b["linea"],
                                    f"Cita textual sin número de página: «{frag[:80]}…» {c['texto']}", c["texto"]))
            fila = filas_boveda[c["ref"]] if c.get("ref") is not None and filas_boveda else None
            if buscador is None:
                res.update(estado="no_comprobado", detalle="módulo buscador_citas no disponible")
            elif not fila or not fila.get("_pdf_ruta"):
                res.update(estado="no_comprobado", detalle="fuente sin PDF indexado en la bóveda")
            else:
                try:
                    v = buscador.verificar_cita_textual(frag, fila["_pdf_ruta"])
                except Exception as e:  # noqa: BLE001
                    v = None
                    res.update(estado="no_comprobado", detalle=f"error del buscador: {type(e).__name__}: {e}")
                if v is not None:
                    res["pdf"] = fila["pdf"]
                    res["similitud"] = v.get("similitud")
                    res["etiqueta_impresa"] = v.get("etiqueta_impresa")
                    res["pagina_fisica"] = v.get("pagina_fisica")
                    if v.get("verificada"):
                        res.update(estado="verificada", detalle=v.get("motivo", ""))
                        pc, pe = _primera_pagina(c["localizador"]), v.get("etiqueta_impresa")
                        if pc and pe and pc != str(pe).lstrip("0"):
                            hallazgos.append(_h(
                                "CITA_TEXTUAL_PAGINA", OBS, b["linea"],
                                f"Cita textual hallada en p. {pe} del PDF, pero se cita p. {pc}.", c["texto"]))
                        elif pc and not pe:
                            hallazgos.append(_h(
                                "CITA_TEXTUAL_PAGINA", OBS, b["linea"],
                                f"Cita hallada (pág. PDF {v.get('pagina_fisica')}) pero la página impresa no se "
                                f"pudo determinar [VERIFICAR: página impresa de «{frag[:40]}…»].", c["texto"]))
                    elif any("ocr" in str(a).lower() for a in v.get("avisos", [])):
                        res.update(estado="no_comprobado", detalle="requiere OCR: " + v.get("motivo", ""))
                        hallazgos.append(_h("CITA_TEXTUAL_NO_COMPROBADA", OBS, b["linea"],
                                            f"Cita textual no comprobable (PDF requiere OCR): «{frag[:80]}…»", c["texto"]))
                    else:
                        res.update(estado="no_hallada", detalle=v.get("motivo", ""))
                        hallazgos.append(_h(
                            "CITA_TEXTUAL_NO_HALLADA", ROJA, b["linea"],
                            f"Cita textual no hallada en {fila['pdf']}: «{frag[:80]}…» ({v.get('motivo')}).",
                            c["texto"]))
            if res["estado"] == "no_comprobado" and not any(h["detalle"] == c["texto"] and h["codigo"].startswith("CITA_TEXTUAL_NO_COMP")
                                                           for h in hallazgos):
                hallazgos.append(_h("CITA_TEXTUAL_NO_COMPROBADA", OBS, b["linea"],
                                    f"Cita textual no comprobada ({res['detalle']}): «{frag[:80]}…»", c["texto"]))
            resultados.append(res)
    return resultados, hallazgos


# ----------------------------------------------------------------------------------------
# Orquestación
# ----------------------------------------------------------------------------------------
def dictaminar(hallazgos: list[dict]) -> str:
    if any(h["severidad"] == ROJA for h in hallazgos):
        return BLOQUEADO
    if any(h["severidad"] == OBS for h in hallazgos):
        return OBSERVADO
    return APROBADO


def auditar(ruta: Path, sin_red: bool = False, catalogo: Path | None = None, boveda: Boveda | None = None,
            usar_boveda: bool = True, consultor=None, buscador=None) -> dict:
    ruta = Path(ruta)
    lineas = leer_lineas(ruta)
    cuerpo, lin_refs, encontrada = dividir_cuerpo_y_referencias(lineas)
    avisos: list[str] = []
    origen_refs = "documento"
    refs = parsear_referencias(lin_refs) if encontrada else []
    if not encontrada or not refs:
        cat = Path(catalogo) if catalogo else rutas.LITERATURA / "REFERENCIAS_SIVAC.md"
        if cat.exists():
            lin_cat = leer_lineas(cat)
            _, lr, enc = dividir_cuerpo_y_referencias(lin_cat)
            refs = parsear_referencias(lr if enc else lin_cat)
            origen_refs = f"catálogo externo: {cat.name}"
            avisos.append("El documento no contiene sección de Referencias; se contrastó con el catálogo "
                          f"{cat} ({len(refs)} entradas). Las referencias huérfanas no se reportan "
                          "(el catálogo es global).")
        else:
            avisos.append("El documento no contiene sección de Referencias y no se halló catálogo alternativo.")
            origen_refs = "ninguno"

    bloques = construir_bloques(cuerpo)
    citas = extraer_citas(bloques)
    emp = emparejar(citas, refs)
    hallazgos = list(emp["hallazgos"])

    if origen_refs == "documento":
        for i, r in enumerate(refs):
            if i not in emp["usadas"]:
                hallazgos.append(_h("REFERENCIA_HUERFANA", OBS, r["linea"],
                                    f"Referencia huérfana (sin cita en el texto): {_etiqueta_ref(r)}.", r["texto"][:160]))

    filas_doi, h_doi = validar_dois(refs, sin_red, consultor)
    if origen_refs != "documento":  # solo DOI de referencias efectivamente citadas
        citados = {_etiqueta_ref(refs[i]) for i in emp["usadas"]}
        filas_doi = [f for f in filas_doi if f["referencia"] in citados]
        h_doi = [h for h in h_doi if h["detalle"] in citados]
    hallazgos += h_doi

    if boveda is None and usar_boveda:
        boveda = Boveda()
    filas_boveda, h_bov = cruzar_boveda(refs, emp["usadas"], boveda if usar_boveda else None)
    hallazgos += h_bov

    aserciones = detectar_aserciones_sin_cita(bloques, citas)
    for a in aserciones:
        hallazgos.append(_h("ASERCION_SIN_CITA", OBS, a["linea"],
                            f"Aserción sin cita ({', '.join(a['disparadores'])}): «{a['oracion'][:110]}»", ""))

    marcas = listar_verificar(lineas)
    for m in marcas:
        hallazgos.append(_h("VERIFICAR", OBS, m["linea"], f"Marca pendiente {m['marca']}", ""))

    textuales, h_txt = verificar_citas_textuales(bloques, citas, refs, filas_boveda, buscador)
    hallazgos += h_txt
    hallazgos.sort(key=lambda h: ({ROJA: 0, OBS: 1, INFO: 2}[h["severidad"]], h["linea"] or 0))

    cont = {s: sum(1 for h in hallazgos if h["severidad"] == s) for s in (ROJA, OBS, INFO)}
    resumen = {
        "citas": len(citas), "referencias": len(refs), "origen_referencias": origen_refs,
        "citas_sin_referencia": sum(1 for c in citas if c["estado"] == "sin_referencia"),
        "referencias_huerfanas": sum(1 for h in hallazgos if h["codigo"] == "REFERENCIA_HUERFANA"),
        "discrepancias_anio_autor": sum(1 for h in hallazgos if h["codigo"] in ("DISCREPANCIA_ANIO", "DISCREPANCIA_AUTOR")),
        "dois_con_referencia": sum(1 for f in filas_doi if f["doi"]),
        "dois_inexistentes": sum(1 for h in hallazgos if h["codigo"] == "DOI_INEXISTENTE"),
        "aserciones_sin_cita": len(aserciones), "marcas_verificar": len(marcas),
        "citas_textuales": len(textuales),
        "citas_textuales_no_halladas": sum(1 for t in textuales if t["estado"] == "no_hallada"),
        "hallazgos_rojos": cont[ROJA], "observaciones": cont[OBS], "informativos": cont[INFO],
    }
    citas_pub = [{k: v for k, v in c.items() if not k.startswith("_")} for c in citas]
    for c in citas_pub:
        c["referencia"] = _etiqueta_ref(refs[c["ref"]]) if c.get("ref") is not None else None
        c.pop("ref", None)
    filas_b_pub = [{k: v for k, v in f.items() if not k.startswith("_")} for f in filas_boveda]
    return {
        "archivo": str(ruta), "dictamen": dictaminar(hallazgos), "criterios": CRITERIOS, "resumen": resumen,
        "hallazgos": hallazgos, "citas": citas_pub,
        "referencias": [{"linea": r["linea"], "autor1": r["autor1"], "anio": r["anio"], "doi": r["doi"],
                         "titulo": r["titulo"], "citekeys": r["citekeys"]} for r in refs],
        "doi": filas_doi, "boveda": filas_b_pub, "aserciones_sin_cita": aserciones,
        "verificar": marcas, "citas_textuales": textuales, "avisos": avisos,
        "red": "omitida (--sin-red)" if sin_red else "Crossref",
    }


CRITERIOS = {
    BLOQUEADO: "al menos una alerta roja: cita sin referencia, DOI inexistente en Crossref (HTTP 404) o cita textual no hallada en su PDF",
    OBSERVADO: "sin alertas rojas, con observaciones subsanables (referencia huérfana, discrepancia de año/autor/DOI, "
               "aserción sin cita, [VERIFICAR], cita textual sin página o no comprobada, DOI no comprobado, sin respaldo en bóveda)",
    APROBADO: "sin alertas rojas ni observaciones",
}


# ----------------------------------------------------------------------------------------
# Presentación
# ----------------------------------------------------------------------------------------
def a_markdown(inf: dict, max_filas: int = 60) -> str:
    r = inf["resumen"]
    o = [f"# Informe de integridad — {Path(inf['archivo']).name}", "",
         f"**Dictamen:** `{inf['dictamen']}`  ", f"**Criterio:** {inf['criterios'][inf['dictamen']]}  ",
         f"**Referencias contrastadas:** {r['origen_referencias']}  ", f"**Verificación DOI:** {inf['red']}", ""]
    for a in inf["avisos"]:
        o.append(f"> Aviso: {a}")
    o += ["", "## Resumen", "", "| Indicador | Valor |", "|---|---|"]
    for k, v in r.items():
        o.append(f"| {k.replace('_', ' ')} | {v} |")
    for sev, titulo in ((ROJA, "Alertas rojas"), (OBS, "Observaciones"), (INFO, "Informativos")):
        hs = [h for h in inf["hallazgos"] if h["severidad"] == sev]
        o += ["", f"## {titulo} ({len(hs)})", ""]
        if not hs:
            o.append("Ninguna.")
        for h in hs[:max_filas]:
            o.append(f"- [{h['codigo']}] línea {h['linea']}: {h['mensaje']}")
        if len(hs) > max_filas:
            o.append(f"- … y {len(hs) - max_filas} más (ver --json).")
    o += ["", "## DOI", "", "| Referencia | DOI | Crossref |", "|---|---|---|"]
    for f in inf["doi"]:
        o.append(f"| {f['referencia']} | {f['doi'] or '—'} | {f['crossref']} |")
    o += ["", "## Bóveda", "", "| Referencia | Ficha | PDF |", "|---|---|---|"]
    for f in inf["boveda"]:
        o.append(f"| {f['referencia']} | {f['ficha'] or '—'} | {f['pdf'] or '—'} |")
    return "\n".join(o) + "\n"


def a_texto(inf: dict, max_filas: int = 25) -> str:
    r = inf["resumen"]
    o = [f"DICTAMEN: {inf['dictamen']}", f"  criterio: {inf['criterios'][inf['dictamen']]}",
         f"  archivo: {inf['archivo']}", f"  referencias contrastadas: {r['origen_referencias']}",
         f"  DOI: {inf['red']}"]
    o += [f"  AVISO: {a}" for a in inf["avisos"]]
    o.append("RESUMEN: " + ", ".join(f"{k}={v}" for k, v in r.items() if k != "origen_referencias"))
    for sev, et in ((ROJA, "ALERTA ROJA"), (OBS, "OBSERVACION"), (INFO, "INFO")):
        hs = [h for h in inf["hallazgos"] if h["severidad"] == sev]
        for h in hs[:max_filas]:
            o.append(f"[{et}] {h['codigo']} l.{h['linea']}: {h['mensaje']}")
        if len(hs) > max_filas:
            o.append(f"[{et}] … {len(hs) - max_filas} más (use --json o --md)")
    return "\n".join(o)


def main(argv: list[str] | None = None) -> int:
    seguridad.configurar_utf8()
    ap = argparse.ArgumentParser(description="Auditoría de integridad de citas, referencias y DOI.")
    ap.add_argument("archivo", help="Texto a auditar (.md o .docx)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--json", action="store_true", help="Salida JSON")
    g.add_argument("--md", action="store_true", help="Salida Markdown")
    ap.add_argument("--sin-red", action="store_true", help="No consultar Crossref")
    ap.add_argument("--referencias", type=Path, default=None,
                    help="Catálogo de referencias alterno si el documento carece de sección Referencias")
    ap.add_argument("--sin-boveda", action="store_true", help="No cruzar con la bóveda ni verificar citas textuales")
    ap.add_argument("--salida", type=Path, default=None, help="Guardar el informe en este archivo")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return int(e.code) if isinstance(e.code, int) else 2
    ruta = Path(a.archivo)
    if not ruta.exists() or ruta.suffix.lower() not in {".md", ".markdown", ".txt", ".docx"}:
        print(f"ERROR: archivo inexistente o de tipo no soportado: {ruta}", file=sys.stderr)
        return 2
    try:
        inf = auditar(ruta, sin_red=a.sin_red, catalogo=a.referencias, usar_boveda=not a.sin_boveda)
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    salida = (json.dumps(inf, ensure_ascii=False, indent=2) if a.json else
              a_markdown(inf) if a.md else a_texto(inf))
    if a.salida:
        try:
            destino = seguridad.asegurar_no_sobrescribe(ruta, a.salida)
        except seguridad.EscrituraProhibida as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(salida, encoding="utf-8")
        print(f"Informe guardado en {destino}")
    else:
        print(salida)
    return 0 if inf["dictamen"] == APROBADO else 1


if __name__ == "__main__":
    sys.exit(main())
