#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Extractor de figuras, gráficos y tablas de PDFs de fuentes.

Recorta cada figura/tabla detectada a 300 DPI exactos, con sidecar JSON de
trazabilidad (fuente + SHA-256, página física e impresa, leyenda, cajas,
confianza) y una cita APA 7 sugerida ("Adaptado de…" / "Reproducido de…").

Detección (sin red, sin OCR):
  1. Leyendas: regex multilingüe (Figura|Fig.|Figure|Tabla|Table|Gráfico|
     Cuadro|Esquema + número + separador) sobre los párrafos del índice.
  2. Regiones gráficas: cajas raster (get_image_info), dibujos vectoriales
     (get_drawings) agrupados por proximidad y, para tablas, cajas de
     pdfplumber.find_tables.
  3. Asociación leyenda -> región más cercana (encima o debajo) en la misma
     columna, sin texto corrido intermedio; o leyenda lateral de margen
     (habitual en libros de texto) alineada verticalmente con la región.
  4. La leyenda se acota por estilo tipográfico (fuente/tamaño) para no arrastrar
     el párrafo contiguo.

Principios anti-alucinación:
  * Solo se emiten regiones asociadas a una leyenda; las demás se cuentan y se
    descartan (y toda región > 85 % de la página sin leyenda se ignora).
  * Dato no confirmable (página impresa, autor, año, título, DOI) ->
    "[VERIFICAR: motivo]". El año nunca se infiere.
  * Página sin capa de texto -> 'requiere_ocr'; Tesseract no se invoca ni se
    inventa texto.
  * Nunca se sobrescribe un recorte existente sin --forzar.

Uso:
    python scripts/fuentes/extractor_figuras.py extraer --pdf X.pdf [--paginas 3,5-7] [--forzar]
    python scripts/fuentes/extractor_figuras.py pagina  --pdf X.pdf --pag N [--clip x0,y0,x1,y1 [--relativo]]
    python scripts/fuentes/extractor_figuras.py listar  [--pdf X.pdf]

Códigos de salida: 0 ok; 1 hallazgos (confianza baja, omitidas, requiere OCR) o fallos; 2 uso incorrecto.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import shutil
import sys
from pathlib import Path

try:  # PyMuPDF >= 1.24: evita el aviso de obsolescencia del alias `fitz` en stderr
    import pymupdf as fitz
    sys.modules.setdefault("fitz", fitz)  # ingesta_pdf (ajeno al módulo) importa `fitz`
except ImportError:  # pragma: no cover - versiones antiguas
    import fitz  # PyMuPDF
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad  # noqa: E402
from scripts.fuentes import texto as tx  # noqa: E402
from scripts.fuentes.ingesta_pdf import cargar_indice  # noqa: E402

VERSION_EXTRACTOR = 1
DPI = 300
ZOOM = DPI / 72.0
MARGEN_PT = 4.0
GAP_CLUSTER_PT = 10.0        # proximidad para unir dibujos/imágenes en un mismo gráfico
GAP_VECINOS_PT = 20.0        # unión de subpaneles vecinos no reclamados
GAP_MAX_LEYENDA_PT = 150.0   # distancia máxima leyenda-región
GAP_ALTA_PT = 30.0
GAP_MEDIA_PT = 72.0
AREA_MAX_SIN_LEYENDA = 0.85
GAP_LATERAL_MAX_PT = 150.0   # distancia horizontal máxima leyenda de margen - región
TOL_VERTICAL_LATERAL_PT = 10.0  # tolerancia de alineación vertical de una leyenda lateral
FRAC_ANCHO_LEYENDA_LATERAL = 0.3  # una leyenda de margen es angosta (<= 30 % del ancho de página)
BANDA_TEXTO_PT = 22.0        # franja de borde donde el texto corrido se recorta
TESSERACT_RUTA = Path(r"C:/Users/jquis/AppData/Local/Programs/Tesseract-OCR/tesseract.exe")

_TIPOS = {
    "figura": "figura", "fig": "figura", "figure": "figura", "grafico": "figura",
    "grafica": "figura", "esquema": "figura", "diagrama": "figura",
    "tabla": "tabla", "table": "tabla", "cuadro": "tabla",
}
RE_LEYENDA = re.compile(
    r"^\s*(?P<etq>(?i:Figura|Fig\.?|Figure|Tabla|Table|Gr[áa]fico|Gr[áa]fica|Cuadro|Esquema|Diagrama))"
    r"\s*(?P<num>\d+(?:[.\-]\d+)*[a-z]?|[A-Z]\d+(?:[.\-]\d+)*|[IVXLC]{1,6})"
    r"(?P<sep>[.:|\-–—)]|\s|$)"
)
_RE_INDICE_TOC = re.compile(r"(?:\.\s?){3,}\s*\d+\s*$|…\s*\d+\s*$")

Caja = tuple[float, float, float, float]


# --------------------------------------------------------------------------
# Utilidades geométricas (funciones puras)
# --------------------------------------------------------------------------
def _ancho(b: Caja) -> float:
    return b[2] - b[0]


def _alto(b: Caja) -> float:
    return b[3] - b[1]


def _area(b: Caja) -> float:
    return max(0.0, _ancho(b)) * max(0.0, _alto(b))


def _union(a: Caja, b: Caja) -> Caja:
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def _solape_h(a: Caja, b: Caja) -> float:
    """Fracción de solape horizontal respecto al ancho menor (0-1)."""
    ov = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    return ov / max(1e-6, min(_ancho(a), _ancho(b)))


def _solape_v(a: Caja, b: Caja) -> float:
    ov = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    return ov / max(1e-6, min(_alto(a), _alto(b)))


def _interseccion_area(a: Caja, b: Caja) -> float:
    return _area((max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])))


def _iou(a: Caja, b: Caja) -> float:
    inter = _interseccion_area(a, b)
    return inter / max(1e-6, _area(a) + _area(b) - inter)


def _separacion(a: Caja, b: Caja) -> float:
    """Distancia mínima entre dos cajas (0 si se tocan o solapan)."""
    dx = max(0.0, max(a[0], b[0]) - min(a[2], b[2]))
    dy = max(0.0, max(a[1], b[1]) - min(a[3], b[3]))
    return max(dx, dy) if (dx == 0 or dy == 0) else (dx * dx + dy * dy) ** 0.5


def _redondear(b: Caja, n: int = 2) -> list[float]:
    return [round(float(v), n) for v in b]


# --------------------------------------------------------------------------
# 1. Leyendas
# --------------------------------------------------------------------------
def clasificar_leyenda(texto: str) -> dict | None:
    """Si el párrafo es una leyenda devuelve {tipo, etiqueta, numero}; si no, None.

    Descarta referencias en el cuerpo ("La Figura 3 muestra…") y entradas de
    índices de tablas/figuras (puntos guía + página).
    """
    if not texto:
        return None
    t = texto.strip()
    m = RE_LEYENDA.match(t)
    if not m:
        return None
    resto = t[m.end():].lstrip()
    sep = m.group("sep")
    if sep.isspace() and resto:
        # "Figura 3 muestra…" es referencia; "Figura 3 Título" / "Table 1 (…)" es leyenda.
        if not (resto[0].isupper() or resto[0] in "(\"“«¿¡-–—:|"):
            return None
    if _RE_INDICE_TOC.search(t):
        return None
    etq = tx.canonico(m.group("etq")).rstrip(".")
    tipo = _TIPOS.get(etq)
    if tipo is None:
        return None
    return {"tipo": tipo, "etiqueta": m.group("etq").rstrip("."), "numero": m.group("num")}


def detectar_leyendas(pagina_indice: dict) -> list[dict]:
    """Leyendas de una página del índice (ordenadas de arriba hacia abajo)."""
    salida = []
    for p in pagina_indice.get("parrafos", []):
        info = clasificar_leyenda(p["texto"])
        if info:
            salida.append({**info, "texto": p["texto"], "bbox": tuple(p["bbox"]), "parrafo_id": p["id"]})
    salida.sort(key=lambda d: (d["bbox"][1], d["bbox"][0]))
    return salida


# --------------------------------------------------------------------------
# 2. Regiones gráficas
# --------------------------------------------------------------------------
def agrupar_cajas(cajas: list[tuple[Caja, str]], gap: float = GAP_CLUSTER_PT) -> list[dict]:
    """Agrupa cajas por proximidad (unión-búsqueda con barrido por x).

    Devuelve [{'bbox', 'n', 'tipos': set}] con la caja unión de cada grupo.
    """
    n = len(cajas)
    padre = list(range(n))

    def raiz(i: int) -> int:
        while padre[i] != i:
            padre[i] = padre[padre[i]]
            i = padre[i]
        return i

    orden = sorted(range(n), key=lambda i: cajas[i][0][0])
    activos: list[int] = []
    for i in orden:
        bi = cajas[i][0]
        activos = [j for j in activos if cajas[j][0][2] + gap >= bi[0]]
        for j in activos:
            bj = cajas[j][0]
            if bi[1] - gap <= bj[3] and bj[1] - gap <= bi[3]:
                padre[raiz(i)] = raiz(j)
        activos.append(i)

    grupos: dict[int, dict] = {}
    for i in range(n):
        r = raiz(i)
        b, k = cajas[i]
        g = grupos.get(r)
        if g is None:
            grupos[r] = {"bbox": b, "n": 1, "tipos": {k}}
        else:
            g["bbox"] = _union(g["bbox"], b)
            g["n"] += 1
            g["tipos"].add(k)
    return list(grupos.values())


def _cluster_valido(g: dict) -> bool:
    b = g["bbox"]
    if _ancho(b) < 20 or _alto(b) < 15 or _area(b) < 1200:
        return False
    return "raster" in g["tipos"] or g["n"] >= 3


def cajas_graficas(page: fitz.Page) -> list[tuple[Caja, str]]:
    """Cajas de imágenes raster y trazos vectoriales de la página (sin fondos de página completa)."""
    pw, ph = page.rect.width, page.rect.height
    pa = pw * ph
    cajas: list[tuple[Caja, str]] = []
    try:
        for info in page.get_image_info():
            b = tuple(info["bbox"])
            if _area(b) < 100:
                continue
            if _area(b) > 0.6 * pa and _ancho(b) > 0.9 * pw and _alto(b) > 0.9 * ph:
                continue  # imagen de página completa (escaneo/fondo)
            cajas.append((b, "raster"))
    except Exception:  # noqa: BLE001
        pass
    try:
        for d in page.get_drawings():
            r = d["rect"]
            b = (r.x0, r.y0, r.x1, r.y1)
            if _ancho(b) < 0.3 and _alto(b) < 0.3:
                continue
            if _ancho(b) > 0.9 * pw and _alto(b) > 0.9 * ph:
                continue  # marco o fondo de página
            # Filetes de encabezado/pie
            if _alto(b) <= 2 and (b[3] < 0.08 * ph or b[1] > 0.93 * ph):
                continue
            cajas.append((b, "vector"))
    except Exception:  # noqa: BLE001
        pass
    return cajas


def regiones_candidatas(page: fitz.Page) -> list[dict]:
    """Clusters gráficos válidos: [{'bbox','n','tipos','metodo'}]."""
    cl = [g for g in agrupar_cajas(cajas_graficas(page)) if _cluster_valido(g)]
    for g in cl:
        t = g["tipos"]
        g["metodo"] = "raster+vectorial" if len(t) > 1 else ("raster" if "raster" in t else "vectorial")
    return cl


def tablas_pdfplumber(ruta_pdf: Path, idx0: int) -> list[Caja]:
    """Cajas de tablas con bordes detectadas por pdfplumber (vacío si falla o no hay)."""
    try:
        import pdfplumber
        with pdfplumber.open(str(ruta_pdf)) as pdf:
            pg = pdf.pages[idx0]
            cajas = []
            for t in pg.find_tables():
                b = tuple(float(v) for v in t.bbox)
                filas = len(t.rows) if getattr(t, "rows", None) is not None else 0
                if filas >= 2 and _ancho(b) > 30 and _alto(b) > 15:
                    cajas.append(b)
            return cajas
    except Exception:  # noqa: BLE001
        return []


# --------------------------------------------------------------------------
# 3. Asociación leyenda <-> región
# --------------------------------------------------------------------------
def _hay_texto_intermedio(ley: Caja, reg: Caja, parrafos: list[dict], lado: str,
                          ley_parrafo: Caja | None = None) -> bool:
    """¿Hay texto corrido entre la leyenda y la región (en su columna)? Si sí, no se asocian."""
    if lado == "arriba":
        y_ini, y_fin = reg[3], ley[1]
    else:
        y_ini, y_fin = ley[3], reg[1]
    if y_fin - y_ini < 4:
        return False
    for p in parrafos:
        b = tuple(p["bbox"])
        if len(p["texto"]) < 60 or b == ley or b == ley_parrafo:
            continue
        cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        if reg[0] <= cx <= reg[2] and reg[1] <= cy <= reg[3]:
            continue  # texto dentro del gráfico (etiquetas)
        if cy <= y_ini + 1 or cy >= y_fin - 1:
            continue
        if _solape_h(b, ley) >= 0.3 or _solape_h(b, reg) >= 0.3:
            return True
    return False


def _opcion_lateral(ley: dict, cb: Caja, parrafos: list[dict], ancho_pag: float | None) -> dict | None:
    """Leyenda de margen (a la izquierda/derecha del gráfico, alineada verticalmente con él).

    Es la maquetación habitual de libros de texto (p. ej. Sommerville, Pressman). Para no confundirla
    con columnas de un artículo a dos columnas se exige que la leyenda sea angosta, que su centro
    vertical caiga dentro del rango vertical de la región, que no haya texto corrido en su mismo
    margen a la altura de la región y que no haya texto corrido entre la leyenda y la región.
    """
    lb = ley["bbox"]
    if ancho_pag and _ancho(lb) > FRAC_ANCHO_LEYENDA_LATERAL * ancho_pag:
        return None
    cy = (lb[1] + lb[3]) / 2
    if not (cb[1] - TOL_VERTICAL_LATERAL_PT <= cy <= cb[3] + TOL_VERTICAL_LATERAL_PT):
        return None
    if lb[2] <= cb[0] + 2:
        lado, gap, banda = "derecha", max(0.0, cb[0] - lb[2]), (lb[2], cb[0])
    elif lb[0] >= cb[2] - 2:
        lado, gap, banda = "izquierda", max(0.0, lb[0] - cb[2]), (cb[2], lb[0])
    else:
        return None
    if gap > GAP_LATERAL_MAX_PT:
        return None
    propio = ley.get("bbox_parrafo")
    for p in parrafos:
        b = tuple(p["bbox"])
        if len(p["texto"]) < 60 or b == lb or b == propio:
            continue
        if b[1] < cb[3] and b[3] > cb[1] and _solape_h(b, lb) >= 0.5:
            return None  # texto corrido en el mismo margen: no es una leyenda de margen
        if b[0] >= banda[0] - 1 and b[2] <= banda[1] + 1 and b[1] < lb[3] and b[3] > lb[1]:
            return None  # texto corrido entre la leyenda y la región
    return {"lado": lado, "gap": gap, "convencional": False, "recorte": None, "lateral": True,
            "puntaje": gap + 10.0}


def opciones_para_leyenda(ley: dict, candidatos: list[dict], parrafos: list[dict],
                          ancho_pag: float | None = None) -> list[dict]:
    """Regiones posibles para una leyenda, ordenadas por puntaje (menor = mejor)."""
    lb = ley["bbox"]
    ops = []
    for i, c in enumerate(candidatos):
        cb = c["bbox"]
        if _solape_h(lb, cb) < 0.5:
            lat = _opcion_lateral(ley, cb, parrafos, ancho_pag)
            if lat:
                ops.append({"idx": i, **lat})
            continue
        recorte = None
        if _interseccion_area(lb, cb) > 0.6 * _area(lb):
            # Leyenda dentro del marco del gráfico: se recorta la región para excluirla.
            if (lb[1] + lb[3]) / 2 >= (cb[1] + cb[3]) / 2:
                lado, recorte = "arriba", (cb[0], cb[1], cb[2], lb[1])
            else:
                lado, recorte = "abajo", (cb[0], lb[3], cb[2], cb[3])
            gap = 0.0
            if _alto(recorte) < 15:
                continue
        elif cb[3] <= lb[1] + 12:
            lado, gap = "arriba", max(0.0, lb[1] - cb[3])
        elif cb[1] >= lb[3] - 12:
            lado, gap = "abajo", max(0.0, cb[1] - lb[3])
        else:
            continue
        if gap > GAP_MAX_LEYENDA_PT:
            continue
        if recorte is None and _hay_texto_intermedio(lb, cb, parrafos, lado, ley.get("bbox_parrafo")):
            continue
        convencional = (ley["tipo"] == "figura" and lado == "arriba") or (ley["tipo"] == "tabla" and lado == "abajo")
        ops.append({"idx": i, "lado": lado, "gap": gap, "convencional": convencional, "recorte": recorte,
                    "puntaje": gap + (0.0 if convencional else 25.0)})
    ops.sort(key=lambda o: o["puntaje"])
    return ops


def _ampliar_con_vecinos(reg: Caja, lb: Caja, libres: list[tuple[int, dict]],
                         lateral: bool = False) -> tuple[Caja, list[int], bool]:
    """Une subpaneles vecinos no reclamados que quedan dentro de la banda horizontal de la leyenda
    (o, si la leyenda es lateral, de la propia región)."""
    if lateral:
        lim_x0, lim_x1 = reg[0] - 40, reg[2] + 40
    else:
        lim_x0 = min(lb[0], reg[0]) - 15
        lim_x1 = max(lb[2], reg[2]) + 15
    usados: list[int] = []
    cambio = True
    while cambio:
        cambio = False
        for i, c in libres:
            if i in usados:
                continue
            cb = c["bbox"]
            if _separacion(reg, cb) > GAP_VECINOS_PT:
                continue
            u = _union(reg, cb)
            if u[0] < lim_x0 or u[2] > lim_x1:
                continue
            if _solape_v(reg, cb) < 0.3 and _solape_h(reg, cb) < 0.3:
                continue
            # No cruzar la leyenda
            if _interseccion_area(u, lb) > 0:
                continue
            reg, cambio = u, True
            usados.append(i)
    return reg, usados, bool(usados)


def asociar(leyendas: list[dict], candidatos_fig: list[dict], candidatos_tab: list[dict],
            parrafos: list[dict], ancho: float, alto: float) -> list[dict]:
    """Asigna una región a cada leyenda (asignación voraz sin repetir región)."""
    area_pag = ancho * alto
    opciones = []
    for li, ley in enumerate(leyendas):
        cands = candidatos_tab if ley["tipo"] == "tabla" else candidatos_fig
        if ley["tipo"] == "tabla" and not cands:
            cands = candidatos_fig  # tabla sin bordes detectables por pdfplumber: probar trazos
        opciones.append(opciones_para_leyenda(ley, cands, parrafos, ancho))

    orden = sorted(range(len(leyendas)), key=lambda i: opciones[i][0]["puntaje"] if opciones[i] else 1e9)
    usados_por_tipo: dict[tuple[str, int], int] = {}
    resultado: dict[int, dict] = {}
    for li in orden:
        ley = leyendas[li]
        cands = candidatos_tab if ley["tipo"] == "tabla" and candidatos_tab else candidatos_fig
        elegida = None
        for k, o in enumerate(opciones[li]):
            if (id(cands), o["idx"]) in usados_por_tipo:
                continue
            elegida = (k, o)
            break
        if elegida is None:
            resultado[li] = {"leyenda": ley, "region": None, "motivo": "sin región gráfica asociable"}
            continue
        k, o = elegida
        usados_por_tipo[(id(cands), o["idx"])] = li
        base = cands[o["idx"]]
        # ambigüedad: otra opción libre con puntaje comparable
        rivales = [r for r in opciones[li] if r is not o and (id(cands), r["idx"]) not in usados_por_tipo]
        ambigua = any(r["puntaje"] <= o["puntaje"] * 1.6 + 10 for r in rivales)
        libres = [(i, c) for i, c in enumerate(cands) if (id(cands), i) not in usados_por_tipo]
        reg0 = tuple(o["recorte"]) if o.get("recorte") else tuple(base["bbox"])
        reg, extra, fusion = _ampliar_con_vecinos(reg0, ley["bbox"], libres, bool(o.get("lateral")))
        for i in extra:
            usados_por_tipo[(id(cands), i)] = li
        notas = []
        if fusion:
            notas.append("subpaneles vecinos unidos en una sola región")
        if o.get("recorte"):
            notas.append("leyenda dentro del marco del gráfico: región recortada para excluirla")
        if ambigua:
            notas.append("otra región candidata a distancia comparable")
        if k > 0:
            notas.append("región preferida ya asignada a otra leyenda")
        if o.get("lateral"):
            notas.append(f"leyenda lateral de margen (región a la {o['lado']} de la leyenda) alineada verticalmente con ella")
        elif not o["convencional"]:
            notas.append(f"región {o['lado']} de la leyenda (posición no convencional)")
        frac = _area(reg) / max(1e-6, area_pag)
        min_dim = min(_ancho(reg), _alto(reg))
        if frac > AREA_MAX_SIN_LEYENDA or o["gap"] > GAP_MEDIA_PT:
            conf = "baja"
        elif o["convencional"] and o["gap"] <= GAP_ALTA_PT and not ambigua and not fusion and k == 0 and not o.get("recorte") \
                and frac <= 0.7 and min_dim >= 30:
            conf = "alta"
        else:
            conf = "media"
        if frac > AREA_MAX_SIN_LEYENDA:
            notas.append("región mayor al 85 % de la página: revisar que no sea texto corrido")
        resultado[li] = {"leyenda": ley, "region": reg, "metodo": base["metodo"] + ("+subpaneles" if fusion else ""),
                         "confianza": conf, "gap_pt": round(o["gap"], 1), "notas": notas}
    return [resultado[i] for i in range(len(leyendas))]


def ampliar_con_texto(region: Caja, lineas: list[tuple[Caja, str]], excluir: list[Caja]) -> Caja:
    """Incluye rótulos cortos (ejes, etiquetas) pegados a la región; nunca párrafos ni leyendas."""
    r = region
    for lb, txt in lineas:
        if len(txt.strip()) > 90 or not txt.strip():
            continue
        if any(_interseccion_area(lb, e) > 0.3 * _area(lb) for e in excluir):
            continue
        cy = (lb[1] + lb[3]) / 2
        if cy < region[1] - 6 or cy > region[3] + 10:
            continue
        if lb[0] < region[0] - 25 or lb[2] > region[2] + 25:
            continue
        r = _union(r, lb)
    return r


# --------------------------------------------------------------------------
# 4. Cita APA 7 y metadatos
# --------------------------------------------------------------------------
def ocr_disponible() -> bool:
    return bool(shutil.which("tesseract")) or TESSERACT_RUTA.exists()


def construir_cita(fuente: dict, pagina_fisica: int, etiqueta: str | None, meta: dict | None = None,
                   modo: str = "adaptado") -> str:
    """Nota APA 7 sugerida. Todo dato no confirmado se marca [VERIFICAR: motivo]."""
    meta = meta or {}
    if meta.get("titulo"):
        titulo = meta["titulo"]
    elif fuente.get("titulo_metadatos"):
        titulo = f"{fuente['titulo_metadatos']} [VERIFICAR: título tomado de los metadatos del PDF]"
    else:
        titulo = "[VERIFICAR: título]"
    if meta.get("autor"):
        autor = meta["autor"]
    elif fuente.get("autor_metadatos"):
        autor = f"{fuente['autor_metadatos']} [VERIFICAR: autor tomado de los metadatos del PDF]"
    else:
        autor = "[VERIFICAR: autor]"
    anio = str(meta["anio"]) if meta.get("anio") else "[VERIFICAR: año]"
    if etiqueta:
        pag = f"p. {etiqueta}"
    else:
        pag = f"p. [VERIFICAR: página impresa no determinada; página física {pagina_fisica} del PDF]"
    doi = meta.get("doi")
    enlace = ""
    if doi:
        enlace = f" (https://doi.org/{doi})"
    elif fuente.get("doi_detectado"):
        enlace = f" (https://doi.org/{fuente['doi_detectado']}) [VERIFICAR: DOI detectado automáticamente en el texto]"
    editorial = f", {meta['editorial']}" if meta.get("editorial") else ""
    verbo = "Reproducido de" if modo == "reproducido" else "Adaptado de"
    return f"Nota. {verbo} *{titulo}* ({pag}), por {autor}, {anio}{editorial}{enlace}."


def _fuente_sidecar(indice: dict) -> dict:
    f = indice["fuente"]
    return {"archivo": f["archivo"], "sha256": f["sha256"]}


# --------------------------------------------------------------------------
# 5. Render y escritura
# --------------------------------------------------------------------------
def rect_con_margen(caja: Caja, page: fitz.Page, margen: float = MARGEN_PT) -> fitz.Rect:
    r = fitz.Rect(caja[0] - margen, caja[1] - margen, caja[2] + margen, caja[3] + margen)
    return r & page.rect


def excluir_leyendas(rect: fitz.Rect, leyendas: list[Caja]) -> fitz.Rect:
    """Recorta el rectángulo para que el margen no invada la caja de ninguna leyenda (misma columna)."""
    r = fitz.Rect(rect)
    for lb in leyendas:
        if _solape_h((r.x0, r.y0, r.x1, r.y1), lb) < 0.3:
            continue
        centro_l = (lb[1] + lb[3]) / 2
        if centro_l >= (r.y0 + r.y1) / 2 and r.y1 > lb[1] > r.y0:
            r.y1 = lb[1] - 0.5          # leyenda debajo
        elif centro_l < (r.y0 + r.y1) / 2 and r.y0 < lb[3] < r.y1:
            r.y0 = lb[3] + 0.5          # leyenda encima
    return r


def ajustar_margen_a_texto(rect: fitz.Rect, caja: Caja, lineas: list[tuple[Caja, str]],
                           excepciones: list[Caja]) -> fitz.Rect:
    """Si el margen de 4 pt invade una línea de texto corrido contigua (no rótulo del gráfico), lo repliega.

    `caja` es la región sin margen. Solo se tocan los bordes superior e inferior.
    """
    r = fitz.Rect(rect)
    for lb, txt in lineas:
        if not txt.strip() or any(_interseccion_area(lb, e) > 0.3 * _area(lb) for e in excepciones):
            continue
        if _solape_h(lb, (r.x0, r.y0, r.x1, r.y1)) < 0.3:
            continue
        if _interseccion_area(lb, caja) > 0.3 * _area(lb):
            # Texto corrido que solo roza la franja superior/inferior de un fondo raster: se recorta.
            if len(txt.strip()) >= 25 and _ancho(lb) >= 0.6 * _ancho(caja) * 0.5:
                if lb[3] <= caja[1] + BANDA_TEXTO_PT and lb[1] < caja[1] + BANDA_TEXTO_PT / 2:
                    r.y0 = max(r.y0, lb[3] + 0.3)
                elif lb[1] >= caja[3] - BANDA_TEXTO_PT and lb[3] > caja[3] - BANDA_TEXTO_PT / 2:
                    r.y1 = min(r.y1, lb[1] - 0.3)
            continue
        if lb[3] > r.y0 and lb[3] <= caja[1] + 1.0 and lb[1] < caja[1]:
            r.y0 = max(r.y0, lb[3] + 0.3)      # línea justo encima
        elif lb[1] < r.y1 and lb[1] >= caja[3] - 1.0 and lb[3] > caja[3]:
            r.y1 = min(r.y1, lb[1] - 0.3)      # línea justo debajo
    return r


def renderizar(page: fitz.Page, rect: fitz.Rect) -> Image.Image:
    """Renderiza el recorte a 300 DPI (zoom = 300/72)."""
    pix = page.get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM), clip=rect, colorspace=fitz.csRGB, alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def _rutas_vedadas() -> tuple[Path, ...]:
    """Carpetas donde este módulo jamás escribe, además de las protegidas por seguridad.py."""
    return (rutas.REFERENCIAS, rutas.DATOS_RAW)


def asegurar_destino(ruta: str | Path) -> Path:
    """Guarda propia del módulo: seguridad.py más veda de referencias/ completa y datos/raw/."""
    destino = seguridad.asegurar_escritura_permitida(ruta)
    for vedada in _rutas_vedadas():
        try:
            destino.relative_to(vedada.resolve(strict=False))
        except ValueError:
            continue
        raise seguridad.EscrituraProhibida(
            f"Escritura denegada en {destino}: {vedada} es inmutable o de datos de campo "
            "(ver .claude/rules/01_seguridad.md)")
    return destino


def guardar_png(img: Image.Image, destino: Path) -> Path:
    destino = asegurar_destino(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    img.save(destino, format="PNG", dpi=(DPI, DPI))
    return destino


def guardar_json(datos: dict, destino: Path) -> Path:
    destino = asegurar_destino(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    return destino


def carpeta_salida(ruta_pdf: Path, salida_base: Path | None = None) -> Path:
    return (Path(salida_base) if salida_base else rutas.FIGURAS_FUENTES) / tx.slug(Path(ruta_pdf).stem, 80)


def _sidecar(indice: dict, pag_idx: dict, rect: fitz.Rect, img: Image.Image, nombre_png: str, *,
             tipo: str, numero: str | None, leyenda: str | None, metodo: str, confianza: str,
             notas: list[str], meta: dict | None, modo: str, requiere_ocr: bool) -> dict:
    pf = pag_idx["indice"]
    et = pag_idx.get("etiqueta_impresa")
    d = {
        "version_extractor": VERSION_EXTRACTOR,
        "archivo_png": nombre_png,
        "fuente": _fuente_sidecar(indice),
        "pagina_fisica": pf,
        "etiqueta_impresa": et,
        "metodo_etiqueta": pag_idx.get("metodo_etiqueta"),
        "tipo": tipo,
        "numero": numero,
        "leyenda_textual": leyenda,
        "bbox_pt": _redondear((rect.x0, rect.y0, rect.x1, rect.y1)),
        "bbox_px": [round(rect.x0 * ZOOM), round(rect.y0 * ZOOM), round(rect.x1 * ZOOM), round(rect.y1 * ZOOM)],
        "dpi": DPI,
        "ancho_px": img.width,
        "alto_px": img.height,
        "metodo_deteccion": metodo,
        "confianza": confianza,
        "confianza_criterio": "geométrica (distancia, posición y ambigüedad leyenda-región); no implica revisión visual",
        "notas": notas,
        "requiere_ocr": requiere_ocr,
        "ocr_disponible": ocr_disponible(),
        "cita_modo": modo,
        "cita_sugerida": construir_cita(indice["fuente"], pf, et, meta, modo),
        "aviso": "Verificar licencia/permiso de reproducción de la fuente y contrastar visualmente el recorte "
                 "antes de incluirlo en el informe.",
        "fecha_extraccion": _dt.date.today().isoformat(),
    }
    return d


# --------------------------------------------------------------------------
# 6. Extracción por PDF
# --------------------------------------------------------------------------
def parsear_paginas(spec: str | None, total: int) -> list[int]:
    """'3,5-7' -> [3,5,6,7] (base 1, acotado a 1..total)."""
    if not spec:
        return list(range(1, total + 1))
    salida: set[int] = set()
    for parte in spec.split(","):
        parte = parte.strip()
        if not parte:
            continue
        if "-" in parte:
            a, b = parte.split("-", 1)
            salida.update(range(int(a), int(b) + 1))
        else:
            salida.add(int(parte))
    return sorted(p for p in salida if 1 <= p <= total)


def _lineas_con_tamano(page: fitz.Page) -> list[tuple[Caja, str, float]]:
    """Líneas de texto de la página con el tamaño de fuente dominante (primer span)."""
    lineas = []
    for b in page.get_text("dict").get("blocks", []):
        if b.get("type") != 0:
            continue
        for ln in b.get("lines", []):
            spans = [sp for sp in ln.get("spans", []) if sp["text"].strip()]
            if spans:
                lineas.append((tuple(ln["bbox"]), "".join(sp["text"] for sp in ln["spans"]), float(spans[0]["size"])))
    return lineas


def _unir_lineas(textos: list[str]) -> str:
    """Une líneas de una leyenda (de-guionado al final de línea y espacios colapsados)."""
    out = ""
    for t in (x.strip() for x in textos):
        if not t:
            continue
        if out.endswith("-") and t[:1].islower():
            out = out[:-1] + t
        else:
            out = f"{out} {t}" if out else t
    return re.sub(r"\s+", " ", out).strip()


def refinar_leyenda(ley: dict, lineas: list[tuple[Caja, str, float]]) -> dict:
    """Acota la leyenda a sus propias líneas cuando el índice la unió con el texto contiguo.

    Criterio: la leyenda termina donde cambia el tamaño de fuente (> 0.6 pt) o donde hay un salto
    vertical mayor que el tamaño de letra. Si no hay líneas comparables, se devuelve sin cambios.
    """
    pb = ley["bbox"]
    propias = sorted((x for x in lineas
                      if pb[0] - 2 <= (x[0][0] + x[0][2]) / 2 <= pb[2] + 2 and pb[1] - 2 <= (x[0][1] + x[0][3]) / 2 <= pb[3] + 2),
                     key=lambda x: (round(x[0][1]), x[0][0]))
    if len(propias) < 2:
        return ley
    ref = propias[0][2]
    keep = [propias[0]]
    for ln in propias[1:]:
        prev = keep[-1]
        if abs(ln[2] - ref) > 0.6 or ln[0][1] - prev[0][3] > max(ref, 6.0):
            break
        keep.append(ln)
    if len(keep) == len(propias):
        return ley
    caja = keep[0][0]
    for ln in keep[1:]:
        caja = _union(caja, ln[0])
    texto = _unir_lineas([k[1] for k in keep])
    if clasificar_leyenda(texto) is None:
        return ley
    return {**ley, "texto": texto, "bbox": tuple(caja), "bbox_parrafo": tuple(pb)}


def _lineas_pagina(page: fitz.Page) -> list[tuple[Caja, str]]:
    lineas = []
    for b in page.get_text("dict").get("blocks", []):
        if b.get("type") != 0:
            continue
        for ln in b.get("lines", []):
            txt = "".join(sp["text"] for sp in ln.get("spans", []))
            if txt.strip():
                lineas.append((tuple(ln["bbox"]), txt))
    return lineas


def detectar_pagina(doc: fitz.Document, ruta_pdf: Path, pag_idx: dict) -> dict:
    """Detecta figuras/tablas de una página. Devuelve {'detecciones', 'omitidas', 'regiones_sin_leyenda'}."""
    i0 = pag_idx["indice"] - 1
    page = doc[i0]
    pw, ph = page.rect.width, page.rect.height
    leyendas = detectar_leyendas(pag_idx)
    if leyendas:
        lineas_tam = _lineas_con_tamano(page)
        leyendas = [refinar_leyenda(l, lineas_tam) for l in leyendas]
    if not leyendas:
        n_sin = sum(1 for c in regiones_candidatas(page) if _area(c["bbox"]) <= AREA_MAX_SIN_LEYENDA * pw * ph)
        return {"detecciones": [], "omitidas": [], "regiones_sin_leyenda": n_sin}

    cands = regiones_candidatas(page)
    tablas = []
    if any(l["tipo"] == "tabla" for l in leyendas):
        tablas = [{"bbox": b, "n": 1, "tipos": {"tabla"}, "metodo": "tabla_pdfplumber"}
                  for b in tablas_pdfplumber(ruta_pdf, i0)]
    cands_fig = [c for c in cands if not any(_iou(c["bbox"], t["bbox"]) > 0.5 or
                                             _interseccion_area(c["bbox"], t["bbox"]) > 0.8 * _area(c["bbox"])
                                             for t in tablas)]
    res = asociar(leyendas, cands_fig, tablas, pag_idx["parrafos"], pw, ph)

    lineas = _lineas_pagina(page)
    excluir = [l["bbox"] for l in leyendas]
    detecciones, omitidas = [], []
    usadas = 0
    for r in res:
        ley = r["leyenda"]
        if r["region"] is None:
            omitidas.append({"pagina_fisica": pag_idx["indice"], "tipo": ley["tipo"], "numero": ley["numero"],
                             "leyenda_textual": ley["texto"][:200], "motivo": r["motivo"]})
            continue
        usadas += 1
        reg = ampliar_con_texto(r["region"], lineas, excluir)
        detecciones.append({**r, "region": reg})
    sin_leyenda = max(0, len(cands) + len(tablas) - usadas)
    return {"detecciones": detecciones, "omitidas": omitidas, "regiones_sin_leyenda": sin_leyenda}


def extraer_pdf(ruta_pdf: Path, salida_base: Path | None = None, carpeta_indices: Path | None = None,
                forzar: bool = False, meta: dict | None = None, modo: str = "adaptado",
                solo_detectar: bool = False, paginas: str | None = None, con_leyenda: bool = False) -> dict:
    """Extrae todas las figuras/tablas con leyenda del PDF. Devuelve un resumen serializable."""
    ruta_pdf = Path(ruta_pdf).resolve()
    indice = cargar_indice(ruta_pdf, carpeta_indices)
    carpeta = carpeta_salida(ruta_pdf, salida_base)
    if not solo_detectar:
        asegurar_destino(carpeta / "catalogo_figuras.md")  # falla pronto si la salida está vedada
    doc = fitz.open(ruta_pdf)
    objetivo = set(parsear_paginas(paginas, len(doc)))
    figuras, omitidas, ocr_pags, sin_leyenda = [], [], [], 0
    try:
        for pag_idx in indice["paginas"]:
            pf = pag_idx["indice"]
            if pf not in objetivo:
                continue
            if pag_idx.get("sin_capa_texto") and (pag_idx.get("n_imagenes", 0) > 0 or pag_idx.get("n_dibujos", 0) > 0):
                ocr_pags.append(pf)
                continue
            det = detectar_pagina(doc, ruta_pdf, pag_idx)
            lineas = _lineas_pagina(doc[pf - 1])
            excluir = [x["leyenda"]["bbox"] for x in det["detecciones"]]
            omitidas.extend(det["omitidas"])
            sin_leyenda += det["regiones_sin_leyenda"]
            for n, d in enumerate(det["detecciones"], start=1):
                ley = d["leyenda"]
                caja = _union(d["region"], ley["bbox"]) if con_leyenda else d["region"]
                page = doc[pf - 1]
                rect = rect_con_margen(caja, page)
                rect = ajustar_margen_a_texto(rect, caja, lineas, [] if con_leyenda else excluir)
                if not con_leyenda:
                    rect = excluir_leyendas(rect, [x["leyenda"]["bbox"] for x in det["detecciones"]])
                nombre = f"figura_p{pf:04d}_{n}.png"
                destino = carpeta / nombre
                existente = destino.exists()
                if solo_detectar:
                    estado = "detectada"
                    img = None
                elif existente and not forzar:
                    estado = "existente"
                    img = None
                else:
                    img = renderizar(page, rect)
                    guardar_png(img, destino)
                    estado = "sobrescrita" if existente else "creada"
                if img is None:
                    ancho_px = round(rect.width * ZOOM)
                    alto_px = round(rect.height * ZOOM)
                    img_dummy = Image.new("RGB", (ancho_px, alto_px))
                else:
                    img_dummy = img
                sc = _sidecar(indice, pag_idx, rect, img_dummy, nombre, tipo=ley["tipo"], numero=ley["numero"],
                              leyenda=ley["texto"][:600], metodo=d["metodo"], confianza=d["confianza"],
                              notas=d["notas"], meta=meta, modo=modo, requiere_ocr=False)
                if estado in ("creada", "sobrescrita"):
                    guardar_json(sc, destino.with_suffix(".json"))
                elif estado == "existente" and destino.with_suffix(".json").exists():
                    sc = json.loads(destino.with_suffix(".json").read_text(encoding="utf-8"))
                figuras.append({**sc, "estado": estado, "ruta_png": str(destino)})
    finally:
        doc.close()

    if figuras and not solo_detectar:
        escribir_catalogo(carpeta, indice)
    return {
        "pdf": ruta_pdf.name,
        "carpeta": str(carpeta),
        "n_paginas": indice["fuente"]["n_paginas"],
        "figuras": figuras,
        "omitidas": omitidas,
        "paginas_requieren_ocr": ocr_pags,
        "regiones_sin_leyenda": sin_leyenda,
        "ocr_disponible": ocr_disponible(),
        "resumen": resumen_confianza(figuras),
    }


def resumen_confianza(figuras: list[dict]) -> dict:
    r = {"total": len(figuras), "figuras": 0, "tablas": 0, "alta": 0, "media": 0, "baja": 0}
    for f in figuras:
        r["tablas" if f["tipo"] == "tabla" else "figuras"] += 1
        r[f["confianza"]] = r.get(f["confianza"], 0) + 1
    return r


# --------------------------------------------------------------------------
# 7. Recorte manual
# --------------------------------------------------------------------------
def parsear_clip(texto: str, page: fitz.Page, relativo: bool = False) -> fitz.Rect:
    """'x0,y0,x1,y1' (puntos PDF, origen arriba-izquierda; o fracciones 0-1 con relativo)."""
    try:
        v = [float(x) for x in texto.replace(";", ",").split(",")]
    except ValueError as e:
        raise ValueError(f"clip inválido: {texto!r}") from e
    if len(v) != 4:
        raise ValueError("clip requiere 4 valores: x0,y0,x1,y1")
    if relativo:
        if not all(0.0 <= x <= 1.0 for x in v):
            raise ValueError("con --relativo los valores deben estar entre 0 y 1")
        v = [v[0] * page.rect.width, v[1] * page.rect.height, v[2] * page.rect.width, v[3] * page.rect.height]
    r = fitz.Rect(*v) & page.rect
    if r.width < 5 or r.height < 5:
        raise ValueError(f"clip vacío o fuera de la página ({page.rect.width:.0f}x{page.rect.height:.0f} pt): {texto}")
    return r


def _siguiente_n(carpeta: Path, prefijo: str) -> int:
    n = 1
    while (carpeta / f"{prefijo}_{n}.png").exists():
        n += 1
    return n


def recorte_manual(ruta_pdf: Path, pag: int, clip: str | None = None, relativo: bool = False,
                   salida_base: Path | None = None, carpeta_indices: Path | None = None,
                   forzar: bool = False, n: int | None = None, tipo: str = "figura", leyenda: str | None = None,
                   meta: dict | None = None, modo: str = "adaptado") -> dict:
    ruta_pdf = Path(ruta_pdf).resolve()
    indice = cargar_indice(ruta_pdf, carpeta_indices)
    if not 1 <= pag <= indice["fuente"]["n_paginas"]:
        raise ValueError(f"página fuera de rango: {pag} (el PDF tiene {indice['fuente']['n_paginas']})")
    pag_idx = indice["paginas"][pag - 1]
    doc = fitz.open(ruta_pdf)
    try:
        page = doc[pag - 1]
        rect = parsear_clip(clip, page, relativo) if clip else fitz.Rect(page.rect)
        img = renderizar(page, rect)
        carpeta = carpeta_salida(ruta_pdf, salida_base)
        asegurar_destino(carpeta / "catalogo_figuras.md")
        prefijo = f"manual_p{pag:04d}"
        n_sel = n if n is not None else _siguiente_n(carpeta, prefijo)
        destino = carpeta / f"{prefijo}_{n_sel}.png"
        if destino.exists() and not forzar:
            raise FileExistsError(f"ya existe {destino.name}; use --forzar para sobrescribir")
        # Leyenda: la indicada, o la más cercana (solapada o a <=40 pt) de la página
        numero, texto_ley, notas = None, leyenda, []
        if texto_ley is None:
            mejor = None
            for ley in detectar_leyendas(pag_idx):
                lb = ley["bbox"]
                d = _separacion((rect.x0, rect.y0, rect.x1, rect.y1), lb)
                if d <= 40 and (mejor is None or d < mejor[0]):
                    mejor = (d, ley)
            if mejor:
                texto_ley, numero = mejor[1]["texto"][:600], mejor[1]["numero"]
                tipo = mejor[1]["tipo"]
        confianza = "alta" if texto_ley else "media"
        if not texto_ley:
            notas.append("recorte manual sin leyenda localizada: completar leyenda y cita")
        requiere_ocr = bool(pag_idx.get("sin_capa_texto"))
        if requiere_ocr:
            notas.append("requiere OCR: la página no tiene capa de texto; su contenido textual no es citable sin OCR")
        guardar_png(img, destino)
        sc = _sidecar(indice, pag_idx, rect, img, destino.name, tipo=tipo, numero=numero, leyenda=texto_ley,
                      metodo="manual", confianza=confianza, notas=notas, meta=meta, modo=modo,
                      requiere_ocr=requiere_ocr)
        guardar_json(sc, destino.with_suffix(".json"))
        escribir_catalogo(carpeta, indice)
        return {**sc, "estado": "creada", "ruta_png": str(destino)}
    finally:
        doc.close()


# --------------------------------------------------------------------------
# 8. Catálogo y listado
# --------------------------------------------------------------------------
def _leer_sidecars(carpeta: Path) -> list[dict]:
    datos = []
    for j in sorted(carpeta.glob("*.json")):
        try:
            d = json.loads(j.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(d, dict) and "archivo_png" in d:
            datos.append(d)
    datos.sort(key=lambda d: (d["pagina_fisica"], d["archivo_png"]))
    return datos


def escribir_catalogo(carpeta: Path, indice: dict | None = None) -> Path:
    """Genera catalogo_figuras.md (enlaces ![[...]] estilo Obsidian) a partir de los sidecars."""
    items = _leer_sidecars(carpeta)
    archivo = indice["fuente"]["archivo"] if indice else (items[0]["fuente"]["archivo"] if items else carpeta.name)
    sha = indice["fuente"]["sha256"] if indice else (items[0]["fuente"]["sha256"] if items else "")
    r = resumen_confianza(items)
    lineas = [
        "---",
        "tipo: catalogo_figuras",
        "fase: F3",
        "agente: extractor_figuras",
        "estado: generado",
        f"fecha_actualizacion: {_dt.date.today().isoformat()}",
        f"fuente_pdf: \"{archivo}\"",
        f"sha256: {sha}",
        "---",
        f"# Catálogo de figuras y tablas — {archivo}",
        "",
        f"Total: {r['total']} ({r['figuras']} figuras, {r['tablas']} tablas). "
        f"Confianza: alta {r['alta']}, media {r['media']}, baja {r['baja']} (baja = revisión visual obligatoria).",
        "",
    ]
    for d in items:
        et = d["etiqueta_impresa"] or f"[VERIFICAR: impresa no determinada; física {d['pagina_fisica']}]"
        titulo = f"{d['tipo'].capitalize()} {d['numero']}" if d.get("numero") else f"{d['tipo'].capitalize()} (manual)"
        lineas += [
            f"## {titulo} — p. física {d['pagina_fisica']} / impresa {et}",
            "",
            f"![[{d['archivo_png']}]]",
            "",
            f"- Leyenda: {d['leyenda_textual'] or '[VERIFICAR: sin leyenda]'}",
            f"- Confianza: {d['confianza']} · Método: {d['metodo_deteccion']} · {d['ancho_px']}x{d['alto_px']} px a {d['dpi']} DPI",
            f"- Cita sugerida: {d['cita_sugerida']}",
        ]
        if d.get("notas"):
            lineas.append(f"- Notas: {'; '.join(d['notas'])}")
        lineas.append("")
    destino = asegurar_destino(carpeta / "catalogo_figuras.md")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(lineas), encoding="utf-8")
    return destino


def listar(salida_base: Path | None = None, pdf: Path | None = None) -> list[dict]:
    """Catálogo de recortes ya extraídos (todas las fuentes o la de un PDF)."""
    base = Path(salida_base) if salida_base else rutas.FIGURAS_FUENTES
    carpetas = [carpeta_salida(pdf, base)] if pdf else sorted(p for p in base.glob("*") if p.is_dir())
    filas = []
    for c in carpetas:
        for d in _leer_sidecars(c):
            filas.append({"carpeta": c.name, "archivo_png": d["archivo_png"], "tipo": d["tipo"], "numero": d.get("numero"),
                          "pagina_fisica": d["pagina_fisica"], "etiqueta_impresa": d["etiqueta_impresa"],
                          "confianza": d["confianza"], "metodo": d["metodo_deteccion"],
                          "leyenda": (d["leyenda_textual"] or "")[:90]})
    return filas


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def _meta_desde_args(a: argparse.Namespace) -> dict:
    return {k: v for k, v in {"titulo": getattr(a, "titulo", None), "autor": getattr(a, "autor", None),
                              "anio": getattr(a, "anio", None), "editorial": getattr(a, "editorial", None),
                              "doi": getattr(a, "doi", None)}.items() if v}


def _imprimir_resumen(res: dict) -> None:
    print(f"PDF: {res['pdf']}  ({res['n_paginas']} págs)  ->  {res['carpeta']}")
    for f in res["figuras"]:
        et = f["etiqueta_impresa"] or "s/e"
        print(f"  [{f['estado']:10s}] {f['archivo_png']:24s} {f['tipo']:6s} {str(f['numero']):>5s} "
              f"pág.fís={f['pagina_fisica']:>4d} impr={et:>5s} conf={f['confianza']:5s} "
              f"{f['ancho_px']}x{f['alto_px']}px  {f['metodo_deteccion']}")
        for n in f["notas"]:
            print(f"      nota: {n}")
    for o in res["omitidas"]:
        print(f"  [omitida  ] pág.fís={o['pagina_fisica']} {o['tipo']} {o['numero']}: {o['motivo']} — {o['leyenda_textual'][:70]}")
    if res["paginas_requieren_ocr"]:
        aviso = "" if res["ocr_disponible"] else " (Tesseract no disponible)"
        print(f"  REQUIERE OCR en páginas: {res['paginas_requieren_ocr']}{aviso}")
    r = res["resumen"]
    print(f"Resumen: {r['total']} ({r['figuras']} figuras, {r['tablas']} tablas) — alta {r['alta']}, "
          f"media {r['media']}, baja {r['baja']}; omitidas {len(res['omitidas'])}; "
          f"regiones gráficas sin leyenda {res['regiones_sin_leyenda']}")


def main(argv: list[str] | None = None) -> int:
    seguridad.configurar_utf8()
    comun = argparse.ArgumentParser(add_help=False)
    comun.add_argument("--json", action="store_true", help="Salida JSON para máquina")
    comun.add_argument("--salida", type=Path, default=None, help="Carpeta base de salida (def.: vault/_adjuntos/figuras_fuentes)")
    comun.add_argument("--indices", type=Path, default=None, help="Carpeta de índices .idx.json (def.: la del vault)")
    meta = argparse.ArgumentParser(add_help=False)
    for k, h in (("titulo", "título de la fuente"), ("autor", "autor(es) en formato APA"), ("anio", "año de publicación"),
                 ("editorial", "editorial"), ("doi", "DOI (sin https://doi.org/)")):
        meta.add_argument(f"--{k}", default=None, help=f"Para la cita: {h}")
    meta.add_argument("--modo", choices=("adaptado", "reproducido"), default="adaptado", help="Fórmula de la cita")

    ap = argparse.ArgumentParser(description="Extrae figuras/tablas de PDFs a 300 DPI con trazabilidad.")
    sub = ap.add_subparsers(dest="cmd")
    e = sub.add_parser("extraer", parents=[comun, meta], help="Detecta y recorta todas las figuras/tablas con leyenda")
    e.add_argument("--pdf", required=True, type=Path)
    e.add_argument("--paginas", default=None, help="Ej.: 3,5-7 (páginas físicas)")
    e.add_argument("--forzar", action="store_true", help="Sobrescribe recortes existentes")
    e.add_argument("--solo-detectar", action="store_true", help="No escribe nada; solo informa")
    e.add_argument("--con-leyenda", action="store_true", help="Incluye la leyenda dentro del recorte")
    m = sub.add_parser("pagina", parents=[comun, meta], help="Recorte manual de una región a 300 DPI")
    m.add_argument("--pdf", required=True, type=Path)
    m.add_argument("--pag", required=True, type=int, help="Página física (1 = primera hoja)")
    m.add_argument("--clip", default=None, help="x0,y0,x1,y1 en puntos (origen arriba-izquierda)")
    m.add_argument("--relativo", action="store_true", help="--clip en fracciones 0-1 de la página")
    m.add_argument("--tipo", choices=("figura", "tabla"), default="figura")
    m.add_argument("--leyenda", default=None, help="Leyenda textual (si no, se busca la más cercana)")
    m.add_argument("--n", type=int, default=None, help="Número de archivo explícito (con --forzar para sobrescribir)")
    m.add_argument("--forzar", action="store_true")
    li = sub.add_parser("listar", parents=[comun], help="Catálogo de recortes ya extraídos")
    li.add_argument("--pdf", type=Path, default=None)

    try:
        a = ap.parse_args(argv)
    except SystemExit as se:
        return 2 if se.code not in (0, None) else 0
    if not a.cmd:
        ap.print_usage(sys.stderr)
        return 2

    try:
        if a.cmd == "extraer":
            if not a.pdf.exists():
                print(f"ERROR: no existe {a.pdf}", file=sys.stderr)
                return 2
            res = extraer_pdf(a.pdf, a.salida, a.indices, a.forzar, _meta_desde_args(a), a.modo,
                              a.solo_detectar, a.paginas, a.con_leyenda)
            if a.json:
                print(json.dumps(res, ensure_ascii=False, indent=1))
            else:
                _imprimir_resumen(res)
            hallazgos = res["resumen"]["baja"] or res["omitidas"] or res["paginas_requieren_ocr"]
            return 1 if hallazgos else 0
        if a.cmd == "pagina":
            if not a.pdf.exists():
                print(f"ERROR: no existe {a.pdf}", file=sys.stderr)
                return 2
            res = recorte_manual(a.pdf, a.pag, a.clip, a.relativo, a.salida, a.indices, a.forzar, a.n, a.tipo,
                                 a.leyenda, _meta_desde_args(a), a.modo)
            if a.json:
                print(json.dumps(res, ensure_ascii=False, indent=1))
            else:
                print(f"OK {res['ruta_png']}\n   {res['ancho_px']}x{res['alto_px']} px a {res['dpi']} DPI · "
                      f"pág.fís={res['pagina_fisica']} impr={res['etiqueta_impresa']} · conf={res['confianza']}")
                print(f"   {res['cita_sugerida']}")
                for n in res["notas"]:
                    print(f"   nota: {n}")
            return 1 if res["requiere_ocr"] else 0
        if a.cmd == "listar":
            filas = listar(a.salida, a.pdf)
            if a.json:
                print(json.dumps(filas, ensure_ascii=False, indent=1))
            else:
                for f in filas:
                    print(f"{f['carpeta'][:34]:34s} {f['archivo_png']:24s} {f['tipo']:6s} {str(f['numero']):>5s} "
                          f"pf={f['pagina_fisica']:>4d} conf={f['confianza']:5s} {f['leyenda']}")
                print(f"Total: {len(filas)}")
            return 0
    except (ValueError, FileExistsError) as e:
        print(f"ERROR de uso: {e}", file=sys.stderr)
        return 2
    except seguridad.EscrituraProhibida as e:
        print(f"ERROR de seguridad: {e}", file=sys.stderr)
        return 1
    except Exception as e:  # noqa: BLE001
        print(f"ERROR {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
