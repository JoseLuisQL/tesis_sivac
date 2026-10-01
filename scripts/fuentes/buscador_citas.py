#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Buscador de citas: localiza DÓNDE está una afirmación en las fuentes indexadas.

Trabaja sobre los índices de `ingesta_pdf.py` (página física, etiqueta impresa, párrafo) y permite:

  * buscar(consulta)              -> coincidencias con página física, página impresa y párrafo.
  * verificar_cita_textual(frag)  -> ¿la cita textual existe de verdad en el PDF?
  * formatear_cita_apa7(coinc.)   -> "(Apellido, año, p. X)" usando SOLO la página impresa.

Búsqueda en dos etapas:
  1. LITERAL   sobre el texto canónico (sin tildes, ligaduras, guiones de corte, comillas tipográficas),
               concatenando los párrafos del documento: una cita que cruza salto de página se encuentra igual.
  2. APROXIMADA con rapidfuzz (partial_ratio / token_set_ratio) sobre ventanas de 1 a 3 párrafos
               consecutivos; cada candidato se refina con el alineamiento exacto de la mejor subcadena.

Principios anti-alucinación:
  * Si el mejor score < 60 -> "sin coincidencia confiable" (no se fuerza ningún resultado).
  * `verificada` solo si la coincidencia es literal, o la similitud es >= 97, las cifras coinciden Y las
    palabras coinciden una a una con la fuente (alineamiento por palabras: una palabra añadida, omitida o
    sustituida —«not», «untested»— basta para no verificar, pues puede invertir el sentido).
  * La página citada es SIEMPRE la impresa; si no está determinada se emite [VERIFICAR: ...].
  * Las páginas sin capa de texto (requieren OCR) no se buscan y se avisa de ello.

Uso:
    python scripts/fuentes/buscador_citas.py buscar "texto" [--pdf parte_nombre] [--k 5] [--json]
    python scripts/fuentes/buscador_citas.py verificar "cita textual" --pdf parte_nombre [--json]

Códigos de salida: 0 ok, 1 sin coincidencia / cita no verificada, 2 uso incorrecto (incluye PDF ausente,
ambiguo, corrupto o cifrado).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from bisect import bisect_right
from dataclasses import dataclass, field
from pathlib import Path

from rapidfuzz import fuzz, process
from rapidfuzz.distance import Levenshtein

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad  # noqa: E402


# `ingesta_pdf` hace `import fitz`, y ese alias imprime en STDOUT un aviso de deprecación (ensucia `--json`).
# Se registra `pymupdf` (el nombre vigente de la misma biblioteca) bajo el alias `fitz` antes de importarlo.
import pymupdf  # noqa: E402

sys.modules.setdefault("fitz", pymupdf)
from scripts.fuentes import ingesta_pdf  # noqa: E402
from scripts.fuentes import texto as tx  # noqa: E402

UMBRAL_SIN_COINCIDENCIA = 60.0  # por debajo: "sin coincidencia confiable"
UMBRAL_VERIFICADA = 97.0        # similitud mínima para dar por verificada una cita no literal
UMBRAL_PALABRA = 90.0           # similitud mínima entre dos palabras para tolerarlas como "la misma" (OCR/tipografía)
LONGITUD_MINIMA = 8             # caracteres canónicos mínimos de una consulta
VENTANA_MAX = 3                 # párrafos consecutivos por ventana aproximada
MSG_SIN_COINCIDENCIA = "sin coincidencia confiable"

_RE_NUMERO = re.compile(r"\d+(?:[.,]\d+)*")
_RE_ELIPSIS_BORDE = re.compile(r"^\s*(?:\[?\s*(?:\.{2,}|…)\s*\]?)\s*|\s*(?:\[?\s*(?:\.{2,}|…)\s*\]?)\s*$")


class PdfNoEncontrado(LookupError):
    """La parte del nombre no corresponde a ningún PDF."""


class PdfIlegible(RuntimeError):
    """El PDF está corrupto, cifrado o no se puede indexar."""


class PdfAmbiguo(LookupError):
    """La parte del nombre corresponde a más de un PDF."""

    def __init__(self, parte: str, candidatos: list[str]):
        self.parte = parte
        self.candidatos = candidatos
        super().__init__(f"'{parte}' es ambiguo; candidatos: " + " | ".join(candidatos))


# ----------------------------------------------------------------------------------------
# Modelo de documento (párrafos aplanados en orden de lectura, cruzando páginas)
# ----------------------------------------------------------------------------------------
@dataclass
class Unidad:
    ordinal: int          # posición 1-based entre TODOS los párrafos del documento
    pagina_fisica: int
    etiqueta_impresa: str | None
    metodo_etiqueta: str | None
    n: int                # número de párrafo dentro de la página
    id: str
    texto: str
    canon: str


@dataclass
class Documento:
    nombre: str
    ruta: str
    unidades: list[Unidad]
    unido: str = ""                                   # canon de todas las unidades unidas por " "
    inicios: list[int] = field(default_factory=list)  # offset de cada unidad dentro de `unido`
    avisos: list[str] = field(default_factory=list)


def resolver_pdf(parte: str | Path, carpeta: Path | None = None) -> Path:
    """Resuelve un PDF por ruta exacta o coincidencia parcial del nombre (sin tildes ni mayúsculas)."""
    p = Path(str(parte))
    if p.suffix.lower() == ".pdf" and p.exists():
        return p
    carpeta = Path(carpeta) if carpeta else rutas.PDFS_FUENTES
    pdfs = sorted(carpeta.glob("*.pdf"))
    buscado = tx.canonico(str(parte))
    if not buscado:
        raise PdfNoEncontrado(f"nombre de PDF vacío")
    exactos = [f for f in pdfs if tx.canonico(f.stem) == buscado or f.name == str(parte)]
    if len(exactos) == 1:
        return exactos[0]
    parciales = [f for f in pdfs if buscado in tx.canonico(f.stem)]
    if not parciales:
        raise PdfNoEncontrado(f"ningún PDF coincide con '{parte}' en {carpeta}")
    if len(parciales) > 1:
        raise PdfAmbiguo(str(parte), [f.name for f in parciales])
    return parciales[0]


def construir_documento(indice: dict, nombre: str, ruta: str = "") -> Documento:
    """Aplana un índice de ingesta_pdf en unidades consecutivas y precalcula el texto canónico unido."""
    unidades: list[Unidad] = []
    ordinal = 0
    sin_texto = 0
    for pag in indice.get("paginas", []):
        if pag.get("sin_capa_texto"):
            sin_texto += 1
        et = pag.get("etiqueta_impresa")
        metodo = pag.get("metodo_etiqueta")
        if metodo == "no_determinada":
            et = None
        for par in pag.get("parrafos", []):
            ordinal += 1
            canon = tx.canonico(par.get("texto", ""))
            if not canon:
                continue
            unidades.append(Unidad(ordinal, pag["indice"], et if et not in ("", None) else None,
                                   metodo, par.get("n", 0), par.get("id", ""), par.get("texto", ""), canon))
    inicios: list[int] = []
    partes: list[str] = []
    pos = 0
    for u in unidades:
        inicios.append(pos)
        partes.append(u.canon)
        pos += len(u.canon) + 1
    doc = Documento(nombre=nombre, ruta=ruta, unidades=unidades, unido=" ".join(partes), inicios=inicios)
    if sin_texto:
        doc.avisos.append(f"{nombre}: {sin_texto} página(s) sin capa de texto; requiere OCR "
                          f"(no se buscó en ellas, no se inventa texto)")
    return doc


_CACHE: dict[tuple, Documento] = {}


def cargar_documento(ruta_pdf: Path, carpeta_indices: Path | None = None,
                     verificar_hash: bool = True) -> Documento:
    """Carga (y memoriza en proceso) el documento indexado de un PDF."""
    ruta_pdf = Path(ruta_pdf)
    clave = (str(ruta_pdf), str(carpeta_indices), ruta_pdf.stat().st_mtime_ns, ruta_pdf.stat().st_size)
    if clave not in _CACHE:
        try:
            idx = ingesta_pdf.cargar_indice(ruta_pdf, carpeta_indices, verificar_hash=verificar_hash)
        except (RuntimeError, ValueError, OSError) as e:  # incluye FileDataError (corrupto) y PDF cifrado
            causa = str(e).strip().splitlines()[0] if str(e).strip() else type(e).__name__
            raise PdfIlegible(f"{ruta_pdf.name}: PDF corrupto, cifrado o ilegible ({causa})") from e
        _CACHE[clave] = construir_documento(idx, ruta_pdf.name, str(ruta_pdf))
    return _CACHE[clave]


# ----------------------------------------------------------------------------------------
# Normalización de la consulta
# ----------------------------------------------------------------------------------------
def normalizar_consulta(consulta: str) -> str:
    """Canónico de la consulta, sin elipsis ni corchetes de omisión en los bordes."""
    previa = _RE_ELIPSIS_BORDE.sub("", consulta or "")
    return tx.canonico(previa)


def _numeros(texto: str) -> list[str]:
    return [n.replace(",", ".") for n in _RE_NUMERO.findall(texto)]


def _palabras(texto: str) -> list[str]:
    """Palabras canónicas sin puntuación pegada (así «ready.» y «ready» son la misma palabra)."""
    return [w for w in (t.strip(".,;:()-/") for t in texto.split()) if w]


def comparar_palabras(q: str, region: str) -> dict:
    """Alineamiento palabra a palabra entre la cita y la región de la fuente.

    Una cita textual no literal solo es aceptable si las palabras coinciden una a una. Se tolera, como mucho,
    una diferencia de grafía mínima dentro de una palabra (similitud >= UMBRAL_PALABRA, sin cifras distintas).
    NO se tolera: palabra de la cita ausente en la fuente (p. ej. «not» añadido), palabra de la fuente omitida
    en medio de la cita, ni sustitución por otra palabra (p. ej. «untested» por «tested», que invierte el sentido).
    Las palabras de la fuente que sobran en los BORDES de la región sí se admiten (la región se ampara a límites
    de palabra y no equivale a la cita).
    Devuelve {'coinciden': bool, 'problemas': [str]}.
    """
    a, b = _palabras(q), _palabras(region)
    ops = Levenshtein.opcodes(a, b)
    problemas: list[str] = []
    n_ops = len(ops)
    for k, op in enumerate(ops):
        tag = op.tag
        if tag == "equal":
            continue
        pa, pb = a[op.src_start:op.src_end], b[op.dest_start:op.dest_end]
        if tag == "delete":
            problemas.append(f"palabra(s) de la cita ausentes en la fuente: {pa}")
        elif tag == "insert":
            en_borde = k == 0 or k == n_ops - 1
            if not en_borde:
                problemas.append(f"la fuente tiene palabra(s) omitida(s) en la cita: {pb}")
        else:  # replace
            if len(pa) != len(pb):
                problemas.append(f"cita {pa} difiere de la fuente {pb}")
                continue
            for x, y in zip(pa, pb):
                distintas_cifras = _numeros(x) != _numeros(y)
                if distintas_cifras or fuzz.ratio(x, y) < UMBRAL_PALABRA:
                    problemas.append(f"palabra '{x}' de la cita != '{y}' de la fuente")
    return {"coinciden": not problemas, "problemas": problemas}


# ----------------------------------------------------------------------------------------
# Etapa 1: literal
# ----------------------------------------------------------------------------------------
def _unidad_en(doc: Documento, offset: int) -> int:
    return max(0, bisect_right(doc.inicios, offset) - 1)


def buscar_literal(doc: Documento, q: str) -> list[dict]:
    """Ocurrencias literales de `q` (ya canónica) con límite de palabra en ambos extremos."""
    salida: list[dict] = []
    vistos: set[int] = set()
    texto = doc.unido
    pos = texto.find(q)
    while pos != -1:
        fin = pos + len(q)
        # Límite de palabra solo en consultas cortas (evita que "cat" coincida con "category");
        # una cita larga cortada a mitad de palabra sigue siendo literal.
        if len(q) >= 25:
            antes_ok = despues_ok = True
        else:
            antes_ok = pos == 0 or not texto[pos - 1].isalnum() or not q[0].isalnum()
            despues_ok = fin == len(texto) or not texto[fin].isalnum() or not q[-1].isalnum()
        if antes_ok and despues_ok:
            i = _unidad_en(doc, pos)
            j = _unidad_en(doc, fin - 1)
            if i not in vistos:
                vistos.add(i)
                salida.append({"ini": i, "fin": j, "score": 100.0, "tipo": "literal"})
        pos = texto.find(q, pos + 1)
    return salida


# ----------------------------------------------------------------------------------------
# Etapa 2: aproximada
# ----------------------------------------------------------------------------------------
def _tamanos_ventana(long_q: int) -> list[int]:
    tam = list(range(1, VENTANA_MAX + 1))
    if long_q > 900:  # cita muy larga: amplía la ventana para que quepa completa
        tam += [4, 5, 6]
    return tam


def _ventana(doc: Documento, i: int, tam: int) -> tuple[str, list[int]]:
    """Texto canónico de las unidades i..i+tam-1 y el offset de cada una dentro de la ventana."""
    us = doc.unidades[i:i + tam]
    offs, pos, partes = [], 0, []
    for u in us:
        offs.append(pos)
        partes.append(u.canon)
        pos += len(u.canon) + 1
    return " ".join(partes), offs


def _refinar(doc: Documento, q: str, i: int, tam: int) -> dict:
    """Alineamiento exacto de la mejor subcadena de la ventana: devuelve rango de unidades y similitud."""
    w, offs = _ventana(doc, i, tam)
    if len(q) <= len(w):
        al = fuzz.partial_ratio_alignment(q, w)
        ini_c, fin_c, score = al.dest_start, al.dest_end, al.score
    else:  # consulta más larga que la ventana: comparación completa (partial_ratio inflaría el score)
        ini_c, fin_c = 0, len(w)
        score = fuzz.ratio(q, w)
    a = max(0, bisect_right(offs, ini_c) - 1)
    b = max(a, bisect_right(offs, max(ini_c, fin_c - 1)) - 1)
    # Región ampliada a límites de palabra (para la verificación de cifras).
    r0, r1 = ini_c, fin_c
    while r0 > 0 and w[r0 - 1] != " ":
        r0 -= 1
    while r1 < len(w) and w[r1] != " ":
        r1 += 1
    return {"ini": i + a, "fin": i + b, "score": float(score), "region": w[r0:r1], "tipo": "aproximada"}


def _ventanas_doc(doc: Documento, tam: int) -> list[str]:
    """Textos canónicos de todas las ventanas de `tam` párrafos (memorizados por documento)."""
    cache = doc.__dict__.setdefault("_vent", {})
    if tam not in cache:
        cache[tam] = [_ventana(doc, i, tam)[0] for i in range(0, max(1, len(doc.unidades) - tam + 1))]
    return cache[tam]


def buscar_aproximada(doc: Documento, q: str, limite: int = 10,
                      minimo: float = UMBRAL_SIN_COINCIDENCIA) -> list[dict]:
    """Candidatos aproximados (ya refinados y sin solapes), ordenados por score descendente.

    Cuidado con `partial_ratio`: si la ventana es MÁS CORTA que la consulta compara la ventana contra la
    mejor subcadena de la consulta y puede dar 100 por un título de tres palabras. Por eso solo se usa con
    ventanas de longitud >= consulta; las ventanas más cortas se puntúan con `ratio` (comparación completa).
    """
    n_tokens = len(q.split())
    candidatos: dict[tuple[int, int], float] = {}
    for tam in _tamanos_ventana(len(q)):
        ventanas = _ventanas_doc(doc, tam)
        largas = [i for i, w in enumerate(ventanas) if len(w) >= len(q)]
        cortas = [i for i, w in enumerate(ventanas) if len(w) < len(q) and len(w) >= 0.5 * len(q)]
        trabajos = [(largas, fuzz.partial_ratio, 1.0)]
        if n_tokens >= 4:
            trabajos.append((largas, fuzz.token_set_ratio, 0.9))
        trabajos.append((cortas, fuzz.ratio, 1.0))
        for indices, scorer, peso in trabajos:
            if not indices:
                continue
            res = process.extract(q, [ventanas[i] for i in indices], scorer=scorer, limit=limite * 4,
                                  score_cutoff=minimo / peso)
            for _, sc, pos in res:
                clave = (indices[pos], tam)
                candidatos[clave] = max(candidatos.get(clave, 0.0), sc * peso)
    refinados: list[dict] = []
    for (i, tam), _sc in sorted(candidatos.items(), key=lambda kv: -kv[1])[:limite * 6]:
        # El score final es SIEMPRE el del alineamiento exacto de la mejor subcadena; token_set_ratio
        # solo genera candidatos y nunca infla la similitud.
        refinados.append(_refinar(doc, q, i, tam))
    refinados.sort(key=lambda r: (-r["score"], r["ini"]))
    elegidos: list[dict] = []
    for r in refinados:
        if r["score"] < minimo:
            continue
        if any(not (r["fin"] < e["ini"] or r["ini"] > e["fin"]) for e in elegidos):
            continue  # solapa con una coincidencia mejor
        elegidos.append(r)
        if len(elegidos) >= limite:
            break
    return elegidos


# ----------------------------------------------------------------------------------------
# Construcción de resultados
# ----------------------------------------------------------------------------------------
def _es_prosa(texto: str) -> bool:
    """Prosa = al menos 8 palabras; descarta rótulos de figura/tabla, encabezados y números de página."""
    return len(texto.split()) >= 8


def _contexto(doc: Documento, desde: int, paso: int, alcance: int = 4) -> str | None:
    """Primer párrafo en prosa a partir de `desde` en la dirección `paso` (hasta `alcance` unidades)."""
    i = desde
    for _ in range(alcance):
        if not 0 <= i < len(doc.unidades):
            return None
        if _es_prosa(doc.unidades[i].texto):
            return doc.unidades[i].texto
        i += paso
    return None


def _coincidencia(doc: Documento, h: dict) -> dict:
    u = doc.unidades[h["ini"]]
    uf = doc.unidades[h["fin"]]
    previo = _contexto(doc, h["ini"] - 1, -1)
    siguiente = _contexto(doc, h["fin"] + 1, +1)
    c = {
        "pdf": doc.nombre,
        "pagina_fisica": u.pagina_fisica,
        "etiqueta_impresa": u.etiqueta_impresa,
        "metodo_etiqueta": u.metodo_etiqueta,
        "parrafo": {"n": u.n, "id": u.id},
        "parrafo_global": u.ordinal,
        "texto_del_parrafo": u.texto,
        "score": round(h["score"], 1),
        "tipo": h["tipo"],
        "contexto": {"previo": previo, "siguiente": siguiente},
    }
    if h["fin"] != h["ini"]:  # la coincidencia cruza párrafos (y quizá página)
        c["abarca"] = {
            "pagina_fisica_fin": uf.pagina_fisica,
            "etiqueta_impresa_fin": uf.etiqueta_impresa,
            "parrafo_fin": {"n": uf.n, "id": uf.id},
            "texto": " ".join(x.texto for x in doc.unidades[h["ini"]:h["fin"] + 1]),
        }
    if "region" in h:
        c["_region"] = h["region"]  # uso interno (verificación); se elimina antes de devolver
    return c


def _documentos(pdfs, carpeta_pdfs, carpeta_indices, verificar_hash) -> tuple[list[Documento], list[str]]:
    carpeta = Path(carpeta_pdfs) if carpeta_pdfs else rutas.PDFS_FUENTES
    if pdfs:
        rutas_pdf = [resolver_pdf(p, carpeta) for p in ([pdfs] if isinstance(pdfs, (str, Path)) else pdfs)]
    else:
        rutas_pdf = sorted(carpeta.glob("*.pdf"))
    docs, avisos, fallos = [], [], []
    for r in rutas_pdf:
        try:
            d = cargar_documento(r, carpeta_indices, verificar_hash)
        except PdfIlegible as e:
            fallos.append(str(e))  # un PDF dañado no aborta la búsqueda en los demás
            continue
        docs.append(d)
        avisos.extend(d.avisos)
    if fallos and not docs:
        raise PdfIlegible(" | ".join(fallos))
    avisos.extend(f"OMITIDO: {f}" for f in fallos)
    return docs, avisos


def buscar(consulta: str, pdfs=None, k: int = 5, carpeta_pdfs: Path | None = None,
           carpeta_indices: Path | None = None, verificar_hash: bool = True) -> dict:
    """Localiza `consulta` en las fuentes indexadas.

    Devuelve un dict: {consulta, estado ('ok'|'sin coincidencia confiable'), mensaje, coincidencias[], avisos[]}.
    Cada coincidencia: pdf, pagina_fisica, etiqueta_impresa (None si no se pudo determinar), parrafo {n,id},
    texto_del_parrafo, score (0-100), tipo ('literal'|'aproximada'), contexto {previo, siguiente}
    (y `abarca` si la cita cruza párrafos o páginas).
    """
    q = normalizar_consulta(consulta)
    salida = {"consulta": consulta, "estado": "ok", "mensaje": "", "coincidencias": [], "avisos": []}
    if len(q) < LONGITUD_MINIMA:
        salida.update(estado=MSG_SIN_COINCIDENCIA,
                      mensaje=f"consulta demasiado corta (< {LONGITUD_MINIMA} caracteres): {MSG_SIN_COINCIDENCIA}")
        return salida
    docs, salida["avisos"] = _documentos(pdfs, carpeta_pdfs, carpeta_indices, verificar_hash)
    literales: list[tuple[Documento, dict]] = []
    for d in docs:
        literales.extend((d, h) for h in buscar_literal(d, q))
    hallazgos = [(d, h) for d, h in literales[:k]]
    if len(hallazgos) < k:
        aprox: list[tuple[Documento, dict]] = []
        for d in docs:
            for h in buscar_aproximada(d, q, limite=k):
                if any(d is dl and not (h["fin"] < hl["ini"] or h["ini"] > hl["fin"]) for dl, hl in literales):
                    continue
                aprox.append((d, h))
        aprox.sort(key=lambda t: -t[1]["score"])
        hallazgos += aprox[:k - len(hallazgos)]
    hallazgos = [(d, h) for d, h in hallazgos if h["score"] >= UMBRAL_SIN_COINCIDENCIA]
    if not hallazgos:
        salida.update(estado=MSG_SIN_COINCIDENCIA, mensaje=MSG_SIN_COINCIDENCIA)
        return salida
    for d, h in hallazgos:
        c = _coincidencia(d, h)
        c.pop("_region", None)
        salida["coincidencias"].append(c)
    return salida


# ----------------------------------------------------------------------------------------
# Verificación de cita textual
# ----------------------------------------------------------------------------------------
def verificar_cita_textual(fragmento: str, pdf, carpeta_pdfs: Path | None = None,
                           carpeta_indices: Path | None = None, verificar_hash: bool = True) -> dict:
    """¿Existe `fragmento` en `pdf`? 'verificada' solo si es literal o (similitud >= 97, cifras idénticas y palabras coincidentes una a una)."""
    vacio = {"verificada": False, "literal": False, "pagina_fisica": None, "etiqueta_impresa": None,
             "parrafo": None, "similitud": None, "cifras_coinciden": None, "tokens_ausentes": [],
             "palabras_difieren": [],
             "motivo": "", "avisos": []}
    q = normalizar_consulta(fragmento)
    if len(q) < LONGITUD_MINIMA:
        vacio["motivo"] = f"fragmento demasiado corto (< {LONGITUD_MINIMA} caracteres)"
        return vacio
    docs, avisos = _documentos([pdf], carpeta_pdfs, carpeta_indices, verificar_hash)
    doc = docs[0]
    vacio["avisos"] = avisos
    lit = buscar_literal(doc, q)
    if lit:
        c = _coincidencia(doc, lit[0])
        vacio.update(verificada=True, literal=True, similitud=100.0, cifras_coinciden=True,
                     pagina_fisica=c["pagina_fisica"], etiqueta_impresa=c["etiqueta_impresa"],
                     parrafo=c["parrafo"], motivo="coincidencia literal",
                     n_ocurrencias=len(lit))
        if "abarca" in c:
            vacio["abarca"] = c["abarca"]
        return vacio
    aprox = buscar_aproximada(doc, q, limite=1)
    if not aprox:
        vacio["motivo"] = MSG_SIN_COINCIDENCIA
        return vacio
    h = aprox[0]
    c = _coincidencia(doc, h)
    region = h.get("region", "")
    nums_q = _numeros(q)
    nums_r = set(_numeros(region))
    faltan = [n for n in nums_q if n not in nums_r]
    cifras_ok = not faltan
    region_tokens = set(_palabras(region))
    ausentes = [t for t in _palabras(q) if t not in region_tokens]
    cmp_pal = comparar_palabras(q, region)
    sim = round(h["score"], 1)
    verificada = sim >= UMBRAL_VERIFICADA and cifras_ok and cmp_pal["coinciden"]
    if verificada:
        motivo = (f"similitud {sim} >= {UMBRAL_VERIFICADA:g}, cifras y palabras coincidentes "
                  f"(no literal: solo difiere la grafía)")
    elif not cifras_ok:
        motivo = f"cifras de la cita ausentes en la fuente: {faltan} (similitud {sim})"
    elif sim < UMBRAL_SIN_COINCIDENCIA:
        motivo = MSG_SIN_COINCIDENCIA
    elif not cmp_pal["coinciden"]:
        motivo = ("la cita difiere de la fuente en palabras (puede invertir el sentido): "
                  + "; ".join(cmp_pal["problemas"][:3]) + f" (similitud {sim})")
    else:
        motivo = f"similitud {sim} < {UMBRAL_VERIFICADA:g}: no se verifica como cita textual"
    vacio.update(verificada=verificada, literal=False, similitud=sim, cifras_coinciden=cifras_ok,
                 tokens_ausentes=ausentes, palabras_difieren=cmp_pal["problemas"], motivo=motivo)
    if sim >= UMBRAL_SIN_COINCIDENCIA:  # ubicación de la coincidencia más cercana (solo orientativa)
        vacio.update(pagina_fisica=c["pagina_fisica"], etiqueta_impresa=c["etiqueta_impresa"],
                     parrafo=c["parrafo"], texto_fuente=c["texto_del_parrafo"])
        if "abarca" in c:
            vacio["abarca"] = c["abarca"]
    return vacio


# ----------------------------------------------------------------------------------------
# Formato APA 7
# ----------------------------------------------------------------------------------------
def _autores_apa(autores, conector: str = "y") -> str:
    if isinstance(autores, str):
        lista = [autores.strip()]
    else:
        lista = [a.strip() for a in autores if a and a.strip()]
    if not lista:
        return "[VERIFICAR: autor]"
    if len(lista) == 1:
        return lista[0]
    if len(lista) == 2:
        return f"{lista[0]} {conector} {lista[1]}"
    return f"{lista[0]} et al."  # APA 7: tres o más autores, desde la primera mención


def formatear_cita_apa7(coincidencia: dict, autores, anio, tipo: str = "parafrasis",
                        localizador: str = "pagina", numero_parrafo: int | None = None,
                        conector: str = "y") -> str:
    """Cita parentética APA 7 a partir de una coincidencia (o del resultado de verificar_cita_textual).

    * localizador='pagina': usa SOLO la etiqueta impresa; si es None -> [VERIFICAR: ... pág. PDF N].
    * localizador='parrafo': "párr. N" para obras sin páginas (normas); N = `numero_parrafo` si se da,
      si no el ordinal del párrafo en el índice (puede diferir de la numeración del documento: confirmar).
    * tipo: 'parafrasis' | 'textual' (ambos llevan localizador aquí; la cita textual lo exige por APA).
    """
    if tipo not in ("parafrasis", "textual"):
        raise ValueError("tipo debe ser 'parafrasis' o 'textual'")
    if localizador not in ("pagina", "parrafo"):
        raise ValueError("localizador debe ser 'pagina' o 'parrafo'")
    aut = _autores_apa(autores, conector)
    anio_txt = str(anio).strip() if anio not in (None, "") else "[VERIFICAR: año]"
    if localizador == "parrafo":
        n = numero_parrafo if numero_parrafo is not None else coincidencia.get("parrafo_global")
        loc = f"párr. {n}" if n is not None else "párr. [VERIFICAR: número de párrafo no determinado]"
        return f"({aut}, {anio_txt}, {loc})"
    abarca = coincidencia.get("abarca") or {}
    ini = coincidencia.get("etiqueta_impresa")
    fin = abarca.get("etiqueta_impresa_fin", ini) if abarca else ini
    pf_ini = coincidencia.get("pagina_fisica")
    pf_fin = abarca.get("pagina_fisica_fin", pf_ini) if abarca else pf_ini
    if not ini or not fin:
        rango = f"pág. PDF {pf_ini}" if pf_fin == pf_ini else f"pág. PDF {pf_ini}-{pf_fin}"
        return f"({aut}, {anio_txt}, p. [VERIFICAR: página impresa no determinada; {rango}])"
    loc = f"p. {ini}" if ini == fin else f"pp. {ini}-{fin}"
    return f"({aut}, {anio_txt}, {loc})"


# ----------------------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------------------
def _recorte(t: str | None, n: int = 260) -> str:
    t = (t or "").replace("\n", " ")
    return t if len(t) <= n else t[:n].rstrip() + "…"


def _imprimir_busqueda(res: dict, cita: dict | None) -> None:
    print(f'Consulta: "{_recorte(res["consulta"], 120)}"')
    for a in res["avisos"]:
        print(f"  AVISO: {a}")
    if res["estado"] != "ok":
        print(f"  => {res['mensaje']}")
        return
    for i, c in enumerate(res["coincidencias"], 1):
        et = c["etiqueta_impresa"] if c["etiqueta_impresa"] else "no determinada"
        print(f"\n[{i}] {c['tipo'].upper()} score={c['score']}  {c['pdf']}")
        print(f"    pág. PDF {c['pagina_fisica']} | pág. impresa {et} | párr. {c['parrafo']['n']} ({c['parrafo']['id']})")
        if "abarca" in c:
            print(f"    abarca hasta pág. PDF {c['abarca']['pagina_fisica_fin']} "
                  f"(impresa {c['abarca']['etiqueta_impresa_fin'] or 'no determinada'}), "
                  f"párr. {c['abarca']['parrafo_fin']['id']}")
        print(f"    texto: {_recorte(c['texto_del_parrafo'])}")
        if c["contexto"]["previo"]:
            print(f"    previo: {_recorte(c['contexto']['previo'], 140)}")
        if c["contexto"]["siguiente"]:
            print(f"    siguiente: {_recorte(c['contexto']['siguiente'], 140)}")
        if cita:
            print(f"    cita APA 7: {formatear_cita_apa7(c, **cita)}")


def main(argv: list[str] | None = None) -> int:
    seguridad.configurar_utf8()
    ap = argparse.ArgumentParser(description="Localiza y verifica citas en las fuentes indexadas.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("buscar", help="Busca una afirmación o fragmento")
    b.add_argument("texto")
    b.add_argument("--pdf", action="append", help="parte del nombre del PDF (repetible)")
    b.add_argument("--k", type=int, default=5)
    b.add_argument("--json", action="store_true")
    b.add_argument("--autores", help='apellidos separados por coma, p. ej. "Beck" o "Beck,Fowler"')
    b.add_argument("--anio")
    b.add_argument("--tipo", choices=["parafrasis", "textual"], default="parafrasis")
    b.add_argument("--parrafo", action="store_true", help="citar con 'párr. N' en vez de página")
    v = sub.add_parser("verificar", help="Verifica una cita textual")
    v.add_argument("texto")
    v.add_argument("--pdf", required=True)
    v.add_argument("--json", action="store_true")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        if a.cmd == "buscar":
            if a.k < 1:
                print("--k debe ser >= 1", file=sys.stderr)
                return 2
            res = buscar(a.texto, pdfs=a.pdf, k=a.k)
            cita = None
            if a.autores:
                cita = {"autores": [x.strip() for x in a.autores.split(",") if x.strip()], "anio": a.anio,
                        "tipo": a.tipo, "localizador": "parrafo" if a.parrafo else "pagina"}
                for c in res["coincidencias"]:
                    c["cita_apa7"] = formatear_cita_apa7(c, **cita)
            if a.json:
                print(json.dumps(res, ensure_ascii=False, indent=2))
            else:
                _imprimir_busqueda(res, cita)
            return 0 if res["estado"] == "ok" else 1
        res = verificar_cita_textual(a.texto, a.pdf)
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(f'Cita: "{_recorte(a.texto, 120)}"')
            for av in res["avisos"]:
                print(f"  AVISO: {av}")
            print(f"  VERIFICADA: {'SI' if res['verificada'] else 'NO'}  (literal={res['literal']}, "
                  f"similitud={res['similitud']})")
            print(f"  motivo: {res['motivo']}")
            if res["pagina_fisica"] is not None:
                et = res["etiqueta_impresa"] or "no determinada"
                print(f"  ubicación: pág. PDF {res['pagina_fisica']} | impresa {et} | "
                      f"párr. {res['parrafo']['n']} ({res['parrafo']['id']})")
            if res.get("tokens_ausentes") and not res["literal"]:
                print(f"  palabras de la cita no halladas en la región: {res['tokens_ausentes'][:12]}")
            if res.get("palabras_difieren") and not res["literal"]:
                print(f"  diferencias palabra a palabra: {res['palabras_difieren'][:4]}")
        return 0 if res["verificada"] else 1
    except (PdfNoEncontrado, PdfAmbiguo, PdfIlegible) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        if isinstance(e, PdfAmbiguo):
            for c in e.candidatos:
                print(f"  - {c}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
