#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Ingesta estructurada de PDF con trazabilidad página/párrafo.

Convierte un PDF de fuente bibliográfica en un ÍNDICE JSON verificable:

    paginas[i].indice            -> página física (1 = primera hoja del PDF)
    paginas[i].etiqueta_impresa  -> número impreso en la página (lo que se cita en APA: "p. 45")
    paginas[i].parrafos[j].n     -> número de párrafo dentro de la página
    paginas[i].parrafos[j].bbox  -> caja [x0, y0, x1, y1] en puntos PDF (origen arriba-izquierda)

Principios anti-alucinación:
  * Nunca se infiere texto: lo que no tiene capa de texto se marca `sin_capa_texto`.
  * La página física y la impresa se registran por separado; si la impresa no
    puede determinarse, queda `null` y la cita exigirá [VERIFICAR].
  * Se guarda el SHA-256 del PDF: cualquier cambio del archivo invalida el índice.

Uso:
    python scripts/fuentes/ingesta_pdf.py ARCHIVO.pdf [--salida DIR] [--forzar]
    python scripts/fuentes/ingesta_pdf.py --todos          # todo PDFs_SIVAC
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import fitz  # PyMuPDF

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad  # noqa: E402
from scripts.fuentes import texto as tx  # noqa: E402

VERSION_INDICE = 3  # v3: etiquetas numéricas normalizadas (sin ceros a la izquierda)
_RE_NUM_PAGINA = re.compile(r"^\s*(?:p[áa]g(?:ina)?\.?\s*)?(\d{1,4}|[ivxlc]{1,7})\s*$", re.I)
_RE_NUM_DE_TOTAL = re.compile(r"^\s*(\d{1,4})\s*(?:/|de|of)\s*\d{1,4}\s*$", re.I)


def _lineas_bloque(bloque: dict) -> list[dict]:
    salida = []
    for ln in bloque.get("lines", []):
        txt = "".join(sp["text"] for sp in ln.get("spans", []))
        if txt.strip():
            tam = max((sp["size"] for sp in ln["spans"]), default=0.0)
            salida.append({"texto": txt, "bbox": [round(v, 2) for v in ln["bbox"]], "tam": round(tam, 2)})
    return salida


def _extraer_pagina(pagina: fitz.Page) -> dict:
    datos = pagina.get_text("dict", sort=True)
    bloques = []
    for b in datos.get("blocks", []):
        if b.get("type") != 0:
            continue
        lineas = _lineas_bloque(b)
        if not lineas:
            continue
        bloques.append({"bbox": [round(v, 2) for v in b["bbox"]], "lineas": lineas})
    imagenes = sum(1 for b in datos.get("blocks", []) if b.get("type") == 1)
    return {
        "ancho": round(pagina.rect.width, 2),
        "alto": round(pagina.rect.height, 2),
        "bloques": bloques,
        "n_imagenes": imagenes,
        "n_dibujos": len(pagina.get_drawings()) if hasattr(pagina, "get_drawings") else 0,
    }


def _detectar_repetidos(paginas: list[dict]) -> set[str]:
    """Líneas de encabezado/pie que se repiten en >=40 % de las páginas (se excluyen del cuerpo)."""
    if len(paginas) < 4:
        return set()
    cont: Counter[str] = Counter()
    for p in paginas:
        vistos = set()
        alto = p["alto"]
        for b in p["bloques"]:
            for ln in b["lineas"]:
                y0, y1 = ln["bbox"][1], ln["bbox"][3]
                if y1 < alto * 0.09 or y0 > alto * 0.92:
                    clave = re.sub(r"\d+", "#", tx.canonico(ln["texto"]))
                    if clave and clave not in vistos:
                        vistos.add(clave)
                        cont[clave] += 1
    umbral = max(3, int(len(paginas) * 0.4))
    return {k for k, v in cont.items() if v >= umbral}


def _normalizar_etiqueta(et: str) -> str:
    """'01' -> '1' (APA cita 'p. 1'); los numerales romanos y textos se dejan intactos."""
    et = et.strip()
    return str(int(et)) if et.isdigit() else et


def _etiqueta_impresa(doc: fitz.Document, idx0: int, pag: dict) -> tuple[str | None, str]:
    """Devuelve (etiqueta, método). Prioriza etiquetas lógicas del PDF; luego numeración visible."""
    try:
        et = doc[idx0].get_label()
        if et:
            return _normalizar_etiqueta(et), "etiqueta_pdf"
    except Exception:
        pass
    alto = pag["alto"]
    candidatos = []
    for b in pag["bloques"]:
        for ln in b["lineas"]:
            y0, y1 = ln["bbox"][1], ln["bbox"][3]
            if y1 < alto * 0.09 or y0 > alto * 0.92:
                t = ln["texto"].strip()
                m = _RE_NUM_DE_TOTAL.match(t) or _RE_NUM_PAGINA.match(t)
                if m:
                    candidatos.append(m.group(1))
    if len(candidatos) == 1:
        return _normalizar_etiqueta(candidatos[0]), "numero_visible"
    return None, "no_determinada"


def _construir_parrafos(pag: dict, repetidos: set[str], idx: int) -> list[dict]:
    parrafos = []
    n = 0
    for b in pag["bloques"]:
        lineas_ok = []
        for ln in b["lineas"]:
            clave = re.sub(r"\d+", "#", tx.canonico(ln["texto"]))
            en_margen = ln["bbox"][3] < pag["alto"] * 0.09 or ln["bbox"][1] > pag["alto"] * 0.92
            if en_margen and (clave in repetidos or _RE_NUM_PAGINA.match(ln["texto"].strip())):
                continue
            lineas_ok.append(ln)
        if not lineas_ok:
            continue
        crudo = "\n".join(l["texto"] for l in lineas_ok)
        limpio = tx.limpiar_pdf(crudo)
        if len(limpio) < 2:
            continue
        n += 1
        x0 = min(l["bbox"][0] for l in lineas_ok)
        y0 = min(l["bbox"][1] for l in lineas_ok)
        x1 = max(l["bbox"][2] for l in lineas_ok)
        y1 = max(l["bbox"][3] for l in lineas_ok)
        tam = round(sum(l["tam"] for l in lineas_ok) / len(lineas_ok), 2)
        parrafos.append({
            "id": f"p{idx:04d}-{n:03d}",
            "n": n,
            "texto": limpio,
            "bbox": [round(x0, 2), round(y0, 2), round(x1, 2), round(y1, 2)],
            "tam_fuente": tam,
            "n_lineas": len(lineas_ok),
        })
    return parrafos


def ingestar(ruta_pdf: Path) -> dict:
    ruta_pdf = Path(ruta_pdf).resolve()
    doc = fitz.open(ruta_pdf)
    if doc.needs_pass:
        raise RuntimeError(f"PDF cifrado, no se puede indexar: {ruta_pdf.name}")
    crudas = [_extraer_pagina(doc[i]) for i in range(len(doc))]
    repetidos = _detectar_repetidos(crudas)

    paginas, sin_texto = [], 0
    for i, pag in enumerate(crudas):
        parrafos = _construir_parrafos(pag, repetidos, i + 1)
        etiqueta, metodo = _etiqueta_impresa(doc, i, pag)
        caracteres = sum(len(p["texto"]) for p in parrafos)
        if caracteres < 25:
            sin_texto += 1
        paginas.append({
            "indice": i + 1,
            "etiqueta_impresa": etiqueta,
            "metodo_etiqueta": metodo,
            "ancho": pag["ancho"],
            "alto": pag["alto"],
            "n_imagenes": pag["n_imagenes"],
            "n_dibujos": pag["n_dibujos"],
            "sin_capa_texto": caracteres < 25,
            "parrafos": parrafos,
        })

    meta = doc.metadata or {}
    muestra = " ".join(p["texto"] for pg in paginas[:3] for p in pg["parrafos"])[:6000]
    indice = {
        "version_indice": VERSION_INDICE,
        "fuente": {
            "archivo": ruta_pdf.name,
            "ruta": str(ruta_pdf),
            "sha256": seguridad.sha256_archivo(ruta_pdf),
            "n_paginas": len(doc),
            "titulo_metadatos": (meta.get("title") or "").strip() or None,
            "autor_metadatos": (meta.get("author") or "").strip() or None,
            "doi_detectado": tx.extraer_doi(muestra) or tx.extraer_doi(meta.get("subject", "") or ""),
        },
        "calidad": {
            "paginas_sin_capa_texto": sin_texto,
            "porcentaje_sin_texto": round(100 * sin_texto / max(1, len(doc)), 1),
            "requiere_ocr": sin_texto > 0.3 * len(doc),
            "lineas_repetidas_excluidas": len(repetidos),
            "paginas_con_etiqueta_impresa": sum(1 for p in paginas if p["etiqueta_impresa"]),
        },
        "paginas": paginas,
    }
    doc.close()
    return indice


def ruta_indice(ruta_pdf: Path, carpeta: Path | None = None) -> Path:
    carpeta = carpeta or rutas.INDICES_PDF
    return carpeta / (tx.slug(ruta_pdf.stem, 80) + ".idx.json")


def guardar_indice(indice: dict, destino: Path) -> Path:
    destino = seguridad.asegurar_escritura_permitida(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(indice, ensure_ascii=False, indent=1), encoding="utf-8")
    return destino


def cargar_indice(ruta_pdf: Path, carpeta: Path | None = None, verificar_hash: bool = True) -> dict:
    """Carga el índice; lo regenera si falta, está obsoleto o el hash del PDF cambió."""
    ruta_pdf = Path(ruta_pdf)
    destino = ruta_indice(ruta_pdf, carpeta)
    if destino.exists():
        idx = json.loads(destino.read_text(encoding="utf-8"))
        vigente = idx.get("version_indice") == VERSION_INDICE
        if vigente and verificar_hash:
            vigente = idx["fuente"]["sha256"] == seguridad.sha256_archivo(ruta_pdf)
        if vigente:
            return idx
    idx = ingestar(ruta_pdf)
    guardar_indice(idx, destino)
    return idx


def main() -> int:
    seguridad.configurar_utf8()
    ap = argparse.ArgumentParser(description="Indexa PDFs con trazabilidad página/párrafo.")
    ap.add_argument("pdf", nargs="?", help="Ruta del PDF")
    ap.add_argument("--todos", action="store_true", help="Indexa todos los PDFs de PDFs_SIVAC")
    ap.add_argument("--salida", type=Path, default=None, help="Carpeta de índices")
    ap.add_argument("--forzar", action="store_true", help="Reindexa aunque exista")
    a = ap.parse_args()

    if a.todos:
        objetivos = sorted(rutas.PDFS_FUENTES.glob("*.pdf"))
    elif a.pdf:
        objetivos = [Path(a.pdf)]
    else:
        ap.error("indique un PDF o --todos")
        return 2

    fallos = 0
    for pdf in objetivos:
        try:
            dest = ruta_indice(pdf, a.salida)
            if a.forzar and dest.exists():
                dest.unlink()
            idx = cargar_indice(pdf, a.salida)
            q = idx["calidad"]
            aviso = "  ⚠ REQUIERE OCR" if q["requiere_ocr"] else ""
            print(f"OK  {pdf.name[:70]:70s} págs={idx['fuente']['n_paginas']:4d} "
                  f"etiq={q['paginas_con_etiqueta_impresa']:4d} sin_texto={q['paginas_sin_capa_texto']:3d}{aviso}")
        except Exception as e:  # noqa: BLE001
            fallos += 1
            print(f"ERR {pdf.name[:70]:70s} {type(e).__name__}: {e}")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
