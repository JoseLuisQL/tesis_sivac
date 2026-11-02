#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Aplicador quirúrgico de correcciones sobre un DOCX.

Resuelve cada orden localizando su ancla original en el documento (índice de
párrafo como pista con tolerancia, búsqueda global única y búsqueda en celdas,
incluidas las anclas que cruzan saltos de párrafo). La sustitución se aplica
como span mínimo: se reemplazan únicamente los caracteres que difieren entre
el ancla y el texto nuevo, preservando el resto de la geometría y el formato
de las runs.

Uso:
    python aplicar_correcciones_redaccion.py \
        --entrada salidas/documentos/informe_final_v05.docx \
        --salida  salidas/documentos/informe_final_v06.docx \
        --json    salidas/reportes_maquetacion/_redaccion_sin_colisiones.json \
                  salidas/reportes_maquetacion/reconciliacion_integridad_v05.json \
        --incluir-tabulares \
        --reporte salidas/reportes_maquetacion/aplicacion_correcciones_v06.json
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import docx
from docx.text.paragraph import Paragraph


# --------------------------------------------------------------------------
# Primitivas de texto
# --------------------------------------------------------------------------

def _txt(par: Paragraph) -> str:
    return "".join(r.text for r in par.runs)


def _offsets(par: Paragraph) -> List[Tuple[int, int]]:
    out, cur = [], 0
    for r in par.runs:
        out.append((cur, cur + len(r.text)))
        cur += len(r.text)
    return out


def _reemplazar_span(par: Paragraph, ini: int, fin: int, nuevo: str) -> bool:
    """Reemplaza [ini, fin) del texto concatenado de las runs de un párrafo."""
    offs = _offsets(par)
    if ini == fin:                                   # inserción pura
        if nuevo == "":
            return False
        for i, (a, b) in enumerate(offs):
            if a <= ini <= b:
                r = par.runs[i]
                o = ini - a
                r.text = r.text[:o] + nuevo + r.text[o:]
                return True
        if not offs and ini == 0:
            return False
        return False
    i_ini = i_fin = None
    o_ini = o_fin = 0
    for i, (a, b) in enumerate(offs):
        if i_ini is None and a <= ini <= b and b > a:
            i_ini, o_ini = i, ini - a
        if a < fin <= b:
            i_fin, o_fin = i, fin - a
            break
    if i_ini is None or i_fin is None:
        return False
    if i_ini == i_fin:
        r = par.runs[i_ini]
        r.text = r.text[:o_ini] + nuevo + r.text[o_fin:]
        return True
    par.runs[i_ini].text = par.runs[i_ini].text[:o_ini] + nuevo
    for i in range(i_ini + 1, i_fin):
        par.runs[i].text = ""
    par.runs[i_fin].text = par.runs[i_fin].text[o_fin:]
    return True


def _span_minimo(ancla: str, nuevo: str) -> Tuple[str, str, str]:
    """Separa (prefijo, original_que_cambia, nuevo_que_reemplaza, sufijo)."""
    pre = 0
    lim = min(len(ancla), len(nuevo))
    while pre < lim and ancla[pre] == nuevo[pre]:
        pre += 1
    suf = 0
    while (suf < lim - pre
           and ancla[len(ancla) - 1 - suf] == nuevo[len(nuevo) - 1 - suf]):
        suf += 1
    return (ancla[:pre],
            ancla[pre:len(ancla) - suf] if suf else ancla[pre:],
            nuevo[pre:len(nuevo) - suf] if suf else nuevo[pre:],
            ancla[len(ancla) - suf:] if suf else "")


def _normalizar_ancla(ancla: str) -> str:
    """Retira pictogramas, selectores de variación y espacios iniciales."""
    conservar = "([¿¡\"'«“"
    limpio = ancla.lstrip()
    while limpio and not (limpio[0].isalnum() or limpio[0] in conservar):
        limpio = limpio[1:]
    return limpio


def _parse_ubicacion(ubicacion: Any) -> Optional[Dict[str, int]]:
    """Traduce 'TABLA 46, fila 8 (Firma), columna 2' a índices del documento.

    En este informe el rótulo 'Tabla n' coincide con doc.tables[n] (el
    desplazamiento es cero); fila y columna son 1-based.
    """
    if not isinstance(ubicacion, str):
        return None
    m = re.search(r"TABLA\s+(\d+)", ubicacion, re.I)
    if not m:
        return None
    out = {"tabla": int(m.group(1))}
    f = re.search(r"fila\s+(\d+)", ubicacion, re.I)
    if f:
        out["fila"] = int(f.group(1)) - 1
    c = re.search(r"columna\s+(\d+)", ubicacion, re.I)
    if c:
        out["columna"] = int(c.group(1)) - 1
    return out


def _recorte_cola(parrafos: Sequence[Paragraph], orden: Dict[str, Any]) -> Optional[str]:
    """Elimina una cola duplicada verificando las dos orillas del corte.

    La orden declara el índice del párrafo, el desplazamiento de corte y los
    60 caracteres inmediatamente anteriores y posteriores. Si cualquiera de
    las dos orillas no coincide literalmente, la orden no se aplica: nunca se
    borra texto sobre una suposición de posición.
    """
    indice = orden.get("indice_docx")
    if indice is None or not (0 <= int(indice) < len(parrafos)):
        return None
    par = parrafos[int(indice)]
    texto = _txt(par)
    desde = int(orden["recorte_cola"]["desde"])
    prefijo = orden["recorte_cola"].get("prefijo", "")
    sufijo = orden["recorte_cola"].get("sufijo", "")
    if desde <= 0 or desde >= len(texto):
        return None
    if prefijo and texto[max(0, desde - len(prefijo)):desde] != prefijo:
        return None
    if sufijo and texto[desde:desde + len(sufijo)] != sufijo:
        return None
    if _reemplazar_span(par, desde, len(texto), ""):
        return "recorte_cola"
    return None


def _texto_normalizado(texto: str) -> Tuple[str, List[int], List[int]]:
    """Colapsa espacios y saltos. Devuelve (normalizado, inicios, fines)."""
    chars, ini, fin = [], [], []
    i = 0
    while i < len(texto):
        if texto[i].isspace():
            j = i
            while j < len(texto) and texto[j].isspace():
                j += 1
            chars.append(" ")
            ini.append(i)
            fin.append(j)
            i = j
        else:
            chars.append(texto[i])
            ini.append(i)
            fin.append(i + 1)
            i += 1
    return "".join(chars), ini, fin


def _aplicar_en_parrafos(parrafos: Sequence[Paragraph], ancla: str,
                         nuevo: str) -> Optional[str]:
    """Aplica la corrección sobre una secuencia de párrafos unidos por '\\n'."""
    if not parrafos:
        return None

    texto = ""
    for i, p in enumerate(parrafos):
        texto += _txt(p)
        if i < len(parrafos) - 1:
            texto += "\n"

    norm, ini, fin = _texto_normalizado(texto)

    for candidata in (ancla, _normalizar_ancla(ancla)):
        for ref, mid in ((candidata, nuevo),):
            na = re.sub(r"\s+", " ", ref).strip()
            nn = mid.strip()          # conserva la microtipografía original
            if not na:
                continue
            p = norm.find(na)
            if p < 0:
                continue

            # Ancla truncada a mitad de palabra: el verificador recortó el
            # texto, de modo que el contenedor debe reemplazarse por completo.
            corte = p + len(na)
            truncada = (na[-1:].isalnum() and corte < len(norm)
                        and norm[corte].isalnum())
            if truncada:
                if len(parrafos) == 1:
                    par = parrafos[0]
                    if _reemplazar_span(par, p, len(_txt(par)), nn):
                        return "reemplazo_integro"
                elif p == 0:
                    if _reemplazar_span(parrafos[0], 0, len(_txt(parrafos[0])), nn):
                        for q in parrafos[1:]:
                            for r in q.runs:
                                r.text = ""
                        return "reemplazo_integro_multiparrafo"

            # Tramos que realmente difieren entre el ancla y el texto nuevo.
            cambios = [op for op in difflib.SequenceMatcher(None, na, nn).get_opcodes()
                       if op[0] != "equal"]
            if not cambios:
                return None                      # ya está aplicado
            logrados = 0
            for tag, i1, i2, j1, j2 in reversed(cambios):
                g_ini = ini[p + i1] if p + i1 < len(ini) else len(texto)
                g_fin = fin[p + i2 - 1] if i2 > i1 else g_ini
                if _aplicar_span_global(parrafos, texto, g_ini, g_fin, nn[j1:j2]):
                    logrados += 1
            if logrados == len(cambios):
                return "diferencia_minima" if len(cambios) == 1 else "multiples_tramos"
    return None


def _aplicar_span_global(parrafos: Sequence[Paragraph], texto: str,
                         g_ini: int, g_fin: int, nuevo: str) -> bool:
    """Traduce offsets globales a (párrafo, offset local) y sustituye."""
    cursor = 0
    for k, p in enumerate(parrafos):
        t = _txt(p)
        a, b = cursor, cursor + len(t)
        if a <= g_ini <= b and (g_fin <= b or k == len(parrafos) - 1):
            fin_local = min(g_fin - a, len(t))
            return _reemplazar_span(p, g_ini - a, fin_local, nuevo)
        cursor = b + 1                            # +1 por el '\n' de unión
    return False


# --------------------------------------------------------------------------
# Búsqueda de contenedores
# --------------------------------------------------------------------------

def _buscar_parrafos(parrafos: List[Paragraph], ancla: str, pista: Optional[int],
                     nuevo: str = "") -> Tuple[Optional[int], str]:
    candidatas = [ancla, _normalizar_ancla(ancla)]
    if pista is not None:
        for d in list(range(-3, 4)):
            j = pista + d
            if 0 <= j < len(parrafos):
                if any(c in _txt(parrafos[j]) for c in candidatas if c):
                    return j, "indice_con_tolerancia" if d else "indice"
    hits = [i for i, p in enumerate(parrafos)
            if any(c in _txt(p) for c in candidatas if c)]
    if len(hits) == 1:
        return hits[0], "busqueda_unica"
    if len(hits) > 1 and nuevo:
        # Desempate por similitud con el texto de reemplazo.
        puntajes = sorted(
            ((difflib.SequenceMatcher(None, _txt(parrafos[i]), nuevo).ratio(), i)
             for i in hits), reverse=True)
        mejor, idx = puntajes[0]
        segundo = puntajes[1][0] if len(puntajes) > 1 else 0.0
        if mejor >= 0.55 and mejor - segundo >= 0.10:
            return idx, f"similitud:{mejor:.2f}"
        return None, f"ambigua_en_parrafos:{hits}:mejor={mejor:.2f}"
    return (None, f"ambigua_en_parrafos:{hits}" if hits else "no_localizada")


def _buscar_celdas(tablas, ancla: str, restriccion: Optional[Dict[str, int]] = None):
    hits = []
    candidatas = [re.sub(r"\s+", " ", c).strip()
                  for c in (ancla, _normalizar_ancla(ancla))]
    candidatas = [c for c in candidatas if c]
    rango = ([restriccion["tabla"]]
             if restriccion and "tabla" in restriccion else range(len(tablas)))
    for it in rango:
        if it >= len(tablas):
            continue
        tabla = tablas[it]
        filas = ([restriccion["fila"]]
                 if restriccion and "fila" in restriccion
                 and restriccion["fila"] < len(tabla.rows)
                 else range(len(tabla.rows)))
        for fi in filas:
            fila = tabla.rows[fi]
            vistos = set()
            for co, celda in enumerate(fila.cells):
                if (restriccion and "columna" in restriccion
                        and restriccion["columna"] != co):
                    continue
                clave = id(celda._tc)
                if clave in vistos:          # celda combinada repetida
                    continue
                vistos.add(clave)
                unido = re.sub(r"\s+", " ",
                               "\n".join(_txt(p) for p in celda.paragraphs))
                if any(c in unido for c in candidatas):
                    hits.append((it, fi, co, celda))
    return hits


# --------------------------------------------------------------------------
# Carga
# --------------------------------------------------------------------------

def _cargar(rutas: List[Path], incluir_tabulares: bool) -> List[Dict[str, Any]]:
    ordenes: List[Dict[str, Any]] = []
    for ruta in rutas:
        if not ruta.exists():
            print(f"[AVISO] No existe: {ruta}")
            continue
        data = json.loads(ruta.read_text(encoding="utf-8"))
        items = data.get("sustituciones", []) if isinstance(data, dict) else data
        for item in items:
            item = dict(item)
            item["_origen"] = ruta.name
            ordenes.append(item)
        if incluir_tabulares and isinstance(data, dict):
            for item in data.get("correcciones_tabulares", []):
                item = dict(item)
                item["_origen"] = ruta.name
                ordenes.append(item)
    return ordenes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", required=True)
    ap.add_argument("--salida", required=True)
    ap.add_argument("--json", nargs="+", required=True)
    ap.add_argument("--reporte", required=True)
    ap.add_argument("--incluir-tabulares", action="store_true")
    ap.add_argument("--excluir-indices", default="")
    ap.add_argument("--solo-verificar", action="store_true")
    args = ap.parse_args()

    excluidos = {int(x) for x in args.excluir_indices.split(",") if x.strip().isdigit()}
    entrada, salida = Path(args.entrada), Path(args.salida)
    if not entrada.exists():
        print(f"[ERROR] No existe: {entrada}")
        return 2

    ordenes = _cargar([Path(p) for p in args.json], args.incluir_tabulares)
    doc = docx.Document(str(entrada))
    parrafos, tablas = doc.paragraphs, doc.tables
    print(f"Órdenes: {len(ordenes)} | Documento: {len(parrafos)} párrafos, {len(tablas)} tablas")

    aplicadas, fallidas, omitidas = [], [], []

    for o in ordenes:
        ancla = (o.get("ancla_original") or "").strip()
        nuevo = o.get("texto_nuevo")

        if "recorte_cola" in o:
            modo = _recorte_cola(parrafos, o)
            if modo:
                aplicadas.append({**o, "modo": modo,
                                  "resuelto_en": int(o["indice_docx"])})
            else:
                fallidas.append({**o, "motivo": "orillas del corte no coinciden"})
            continue
        if "filas_propuestas" in o:
            omitidas.append({**o, "motivo": "reconstrucción de tabla (delegada)"})
            continue
        if o.get("indice_docx") is not None and int(o["indice_docx"]) in excluidos:
            omitidas.append({**o, "motivo": "excluida explícitamente"})
            continue
        if not ancla or nuevo is None:
            fallidas.append({**o, "motivo": "ancla o texto_nuevo ausente"})
            continue

        pista = int(o["indice_docx"]) if o.get("indice_docx") is not None else None
        ubic = _parse_ubicacion(o.get("ubicacion"))
        idx, motivo = _buscar_parrafos(parrafos, ancla, pista, nuevo)
        if idx is not None:
            modo = _aplicar_en_parrafos([parrafos[idx]], ancla, nuevo)
            if modo:
                aplicadas.append({**o, "modo": f"parrafo/{motivo}/{modo}",
                                  "resuelto_en": idx})
                continue

        hits = _buscar_celdas(tablas, ancla, ubic)
        if not hits and ubic:
            hits = _buscar_celdas(tablas, ancla, None)
        if len(hits) > 1:
            # Nunca se propaga a ciegas: anclas idénticas pueden requerir
            # reemplazos distintos (p. ej. Juez 1 / Juez 2 / Juez 3).
            fallidas.append({**o, "motivo": f"ancla ambigua en {len(hits)} celdas",
                             "candidatas": [(h[0], h[1], h[2]) for h in hits]})
            continue
        if len(hits) == 1:
            it, fi, co, celda = hits[0]
            modo = _aplicar_en_parrafos(celda.paragraphs, ancla, nuevo)
            if modo:
                aplicadas.append({**o, "modo": f"celda/{modo}",
                                  "tabla": it, "fila": fi, "columna": co})
                continue
            fallidas.append({**o, "motivo": "localizada en celda pero no sustituible"})
            continue
        if len(hits) > 1:
            fallidas.append({**o, "motivo": f"ancla ambigua en {len(hits)} celdas",
                             "candidatas": [(h[0], h[1], h[2]) for h in hits]})
            continue
        fallidas.append({**o, "motivo": motivo})

    if not args.solo_verificar:
        salida.parent.mkdir(parents=True, exist_ok=True)
        doc.save(str(salida))

    reporte = {
        "metadatos": {"entrada": str(entrada),
                      "salida": None if args.solo_verificar else str(salida),
                      "ordenes": len(ordenes), "aplicadas": len(aplicadas),
                      "omitidas": len(omitidas), "fallidas": len(fallidas),
                      "excluidos": sorted(excluidos),
                      "solo_verificar": args.solo_verificar},
        "aplicadas": aplicadas, "omitidas": omitidas, "fallidas": fallidas,
    }
    ruta_rep = Path(args.reporte)
    ruta_rep.parent.mkdir(parents=True, exist_ok=True)
    ruta_rep.write_text(json.dumps(reporte, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Aplicadas: {len(aplicadas)} | Omitidas: {len(omitidas)} | Fallidas: {len(fallidas)}")
    for f in fallidas:
        print(f"  - P{f.get('indice_docx')}: {f.get('motivo')}")
    print(f"Reporte: {ruta_rep}")
    return 0 if not fallidas else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
