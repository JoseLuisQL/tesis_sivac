#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB - Auditor APA 7 / UNAJMA de documentos .docx. SOLO LECTURA.

Comprobaciones (severidad crítica / mayor / menor, con ubicación):
  MARGENES    márgenes por sección (izq 3.0 cm, resto 2.54 cm)
  FUENTE      fuente y tamaño efectivos de cada run (estilo -> estilos base -> docDefaults)
  INTERLINEADO / SANGRIA   cuerpo justificado a 1.5 con sangría de 1.27 cm en la primera línea
  TABLA       exactamente 3 líneas horizontales, cero verticales, encabezado repetible, filas indivisibles
  ROTULO      «Tabla N» / «Figura N» en negrita, título en cursiva, numeración correlativa
  FIGURA      imagen centrada con >= 300 DPI efectivos al ancho mostrado
  NUMERACION  formato de número de página por sección (romanos preliminares, arábigos reiniciados)
  REFERENCIAS sangría francesa 1.27 cm, orden alfabético, correspondencia citas/entradas
  TEXTO       '&' en español fuera de paréntesis, 'et al' sin punto

Exit code: 0 sin críticos ni mayores, 1 con alguno, 2 uso incorrecto.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from docx import Document  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.table import Table  # noqa: E402
from docx.text.paragraph import Paragraph  # noqa: E402
from unidecode import unidecode  # noqa: E402

from scripts.comun import seguridad  # noqa: E402

FUENTE = "times new roman"
TAM_CUERPO = 12.0
MARGEN_IZQ_CM, MARGEN_OTROS_CM, TOL_CM = 3.0, 2.54, 0.06
SANGRIA_CM, TOL_SANGRIA = 1.27, 0.08
DPI_MIN = 299.0
ORDEN = {"critico": 0, "mayor": 1, "menor": 2}
RE_ROTULO = re.compile(r"^\s*(Tabla|Figura)\s+(\d+(?:\.\d+)?)\s*$", re.I)
RE_TITULO_REF = re.compile(r"^\s*(referencias?(?: bibliogr[aá]ficas?)?|bibliograf[ií]a)\s*$", re.I)
RE_CITA = re.compile(r"\(([^()]*?\b(?:19|20)\d{2}[a-z]?[^()]*?)\)|([A-ZÁÉÍÓÚÑ][\wáéíóúñ-]+)(?:\s+(?:y|et al\.?))?\s*\(((?:19|20)\d{2}[a-z]?)\)")


def _h(sev, regla, donde, detalle):
    return {"severidad": sev, "regla": regla, "donde": donde, "detalle": detalle}


def _norm(t: str) -> str:
    return re.sub(r"[^a-z0-9]", "", unidecode(t).lower())


# ------------------------------------------------------------ propiedades efectivas
def _cadena_estilos(estilo):
    while estilo is not None:
        yield estilo
        estilo = estilo.base_style


def _defecto_doc(doc, xpath: str):
    el = doc.styles.element.xpath(xpath)
    return el[0] if el else None


def fuente_efectiva(doc, par: Paragraph, run) -> tuple[str | None, float | None]:
    nombre = run.font.name
    tam = run.font.size.pt if run.font.size else None
    for est in _cadena_estilos(par.style):
        if nombre is None and est.font.name:
            nombre = est.font.name
        if tam is None and est.font.size:
            tam = est.font.size.pt
    if nombre is None:
        rf = _defecto_doc(doc, "w:docDefaults/w:rPrDefault/w:rPr/w:rFonts")
        if rf is not None:
            nombre = rf.get(qn("w:ascii")) or rf.get(qn("w:hAnsi"))
    if tam is None:
        sz = _defecto_doc(doc, "w:docDefaults/w:rPrDefault/w:rPr/w:sz")
        if sz is not None:
            tam = int(sz.get(qn("w:val"))) / 2
    return (nombre.lower() if nombre else None), tam


def formato_parrafo(par: Paragraph) -> dict:
    """Interlineado, sangrías y alineación resueltos por la cadena de estilos."""
    pf = par.paragraph_format
    out = {"interlineado": pf.line_spacing, "izq": pf.left_indent, "primera": pf.first_line_indent,
           "alineacion": par.alignment}
    for est in _cadena_estilos(par.style):
        epf = est.paragraph_format
        for k, v in (("interlineado", epf.line_spacing), ("izq", epf.left_indent),
                     ("primera", epf.first_line_indent), ("alineacion", epf.alignment)):
            if out[k] is None and v is not None:
                out[k] = v
    return out


def _cm(v):
    return None if v is None else v.cm if hasattr(v, "cm") else float(v)


# ------------------------------------------------------------ recorrido del cuerpo
def _cuerpo(doc):
    """Itera (tipo, objeto, índice) en orden de aparición: párrafos y tablas."""
    ip = it = 0
    for el in doc.element.body.iterchildren():
        if el.tag == qn("w:p"):
            yield "p", Paragraph(el, doc), ip
            ip += 1
        elif el.tag == qn("w:tbl"):
            yield "t", Table(el, doc), it
            it += 1


def _es_titulo(par: Paragraph) -> bool:
    n = par.style.name.lower() if par.style is not None else ""
    return n.startswith(("heading", "título", "titulo", "title"))


# ------------------------------------------------------------ comprobaciones
def auditar_margenes(doc) -> list[dict]:
    H = []
    for i, s in enumerate(doc.sections, 1):
        for lado, esp in (("left_margin", MARGEN_IZQ_CM), ("right_margin", MARGEN_OTROS_CM),
                          ("top_margin", MARGEN_OTROS_CM), ("bottom_margin", MARGEN_OTROS_CM)):
            v = getattr(s, lado)
            if v is None or abs(v.cm - esp) > TOL_CM:
                H.append(_h("mayor", "MARGENES", f"sección {i}",
                            f"{lado}: {v.cm:.2f} cm (esperado {esp} cm)" if v is not None else f"{lado} sin definir"))
    return H


def auditar_numeracion(doc) -> list[dict]:
    H, fmts = [], []
    for i, s in enumerate(doc.sections, 1):
        pg = s._sectPr.find(qn("w:pgNumType"))
        fmt = pg.get(qn("w:fmt")) if pg is not None else None
        start = pg.get(qn("w:start")) if pg is not None else None
        fmts.append((fmt or "decimal", start))
    if len(fmts) >= 2:
        if fmts[0][0] != "lowerRoman":
            H.append(_h("mayor", "NUMERACION", "sección 1", f"Preliminares con formato «{fmts[0][0]}»; se esperan romanos minúsculos"))
        if fmts[-1][0] != "decimal":
            H.append(_h("mayor", "NUMERACION", f"sección {len(fmts)}", f"Cuerpo con formato «{fmts[-1][0]}»; se esperan arábigos"))
        elif fmts[-1][1] != "1":
            H.append(_h("mayor", "NUMERACION", f"sección {len(fmts)}", "El cuerpo no reinicia la numeración en 1 (falta w:start=1)"))
    else:
        H.append(_h("menor", "NUMERACION", "documento", "Una sola sección: no hay desvinculación entre preliminares y cuerpo"))
    return H


def auditar_parrafos(doc, max_hallazgos_por_regla: int = 12) -> tuple[list[dict], dict]:
    H, cuenta = [], Counter()
    tot_run = fuera = 0

    def agregar(sev, regla, donde, det):
        cuenta[regla] += 1
        if cuenta[regla] <= max_hallazgos_por_regla:
            H.append(_h(sev, regla, donde, det))

    for tipo, obj, idx in _cuerpo(doc):
        if tipo != "p":
            continue
        par = obj
        txt = par.text.strip()
        if not txt:
            continue
        ubic = f"párrafo {idx}: «{txt[:40]}»"
        for run in par.runs:
            if not run.text.strip():
                continue
            tot_run += 1
            nombre, tam = fuente_efectiva(doc, par, run)
            if nombre != FUENTE or (tam is not None and tam < 9.5):
                fuera += 1
                if nombre != FUENTE:
                    agregar("mayor", "FUENTE", ubic, f"Fuente «{nombre}» (esperada Times New Roman)")
                break
        if _es_titulo(par) or RE_ROTULO.match(txt) or len(txt) < 60:
            continue
        f = formato_parrafo(par)
        if f["interlineado"] is not None and f["interlineado"] not in (1.5, 2.0) and f["interlineado"] > 1.0 and abs(f["interlineado"] - 1.5) > 0.05:
            agregar("menor", "INTERLINEADO", ubic, f"Interlineado {f['interlineado']} (esperado 1.5)")
        elif f["interlineado"] is not None and f["interlineado"] <= 1.0 and len(txt) > 200:
            agregar("mayor", "INTERLINEADO", ubic, f"Cuerpo con interlineado sencillo ({f['interlineado']})")
        prim = _cm(f["primera"])
        if len(txt) > 200 and (prim is None or abs(prim - SANGRIA_CM) > TOL_SANGRIA) and not (_cm(f["izq"]) or 0) > 0.1:
            agregar("menor", "SANGRIA", ubic, f"Sangría de primera línea {prim} cm (esperada {SANGRIA_CM} cm)")
    resumen = {"runs_revisados": tot_run, "parrafos_con_fuente_distinta": fuera,
               "hallazgos_por_regla_totales": dict(cuenta)}
    return H, resumen


def _lineas_tabla(tbl: Table) -> dict:
    """Bordes efectivos: tblBorders + tcBorders, incluido el formato condicional del estilo de tabla."""
    tblPr = tbl._tbl.tblPr
    b = tblPr.find(qn("w:tblBorders")) if tblPr is not None else None

    def val(el, lado):
        if el is None:
            return None
        x = el.find(qn(f"w:{lado}"))
        return None if x is None else x.get(qn("w:val"))

    directos = {l: val(b, l) for l in ("top", "bottom", "left", "right", "insideH", "insideV")}
    estilo = {}
    try:
        est = tbl.style
        for e in _cadena_estilos(est):
            tb = e.element.find(qn("w:tblPr") + "/" + qn("w:tblBorders")) if e.element is not None else None
            if tb is not None:
                for l in directos:
                    estilo.setdefault(l, val(tb, l))
    except Exception:  # noqa: BLE001
        pass
    efectivo = {l: directos[l] if directos[l] is not None else estilo.get(l) for l in directos}
    bajo_enc = False
    if tbl.rows:
        for c in tbl.rows[0].cells:
            tcb = c._tc.tcPr.find(qn("w:tcBorders")) if c._tc.tcPr is not None else None
            if tcb is not None and val(tcb, "bottom") not in (None, "none", "nil"):
                bajo_enc = True
    cond = False
    try:
        for sp in tbl.style.element.findall(qn("w:tblStylePr")):
            if sp.get(qn("w:type")) == "firstRow" and sp.find(qn("w:tcPr") + "/" + qn("w:tcBorders") + "/" + qn("w:bottom")) is not None:
                cond = True
    except Exception:  # noqa: BLE001
        pass
    return {"efectivo": efectivo, "bajo_encabezado": bajo_enc or cond}


def auditar_tablas(doc) -> list[dict]:
    H = []
    for i, t in enumerate(doc.tables, 1):
        if not t.rows:
            continue
        info = _lineas_tabla(t)
        e = info["efectivo"]
        verticales = [l for l in ("left", "right", "insideV") if e.get(l) not in (None, "none", "nil")]
        if verticales:
            H.append(_h("mayor", "TABLA", f"tabla {i}", f"Bordes verticales presentes ({', '.join(verticales)}); APA 7 no los admite"))
        if e.get("insideH") not in (None, "none", "nil"):
            H.append(_h("mayor", "TABLA", f"tabla {i}", "Líneas horizontales interiores en todas las filas (solo se admiten 3 líneas)"))
        if e.get("top") in (None, "none", "nil") or e.get("bottom") in (None, "none", "nil"):
            H.append(_h("mayor", "TABLA", f"tabla {i}", "Faltan las líneas superior/inferior de la tabla"))
        if not info["bajo_encabezado"]:
            H.append(_h("mayor", "TABLA", f"tabla {i}", "Falta la línea bajo el encabezado"))
        trPr = t.rows[0]._tr.trPr
        if trPr is None or trPr.find(qn("w:tblHeader")) is None:
            H.append(_h("menor", "TABLA", f"tabla {i}", "Encabezado sin repetición entre páginas (w:tblHeader)"))
        sin_cs = sum(1 for r in t.rows if r._tr.trPr is None or r._tr.trPr.find(qn("w:cantSplit")) is None)
        if sin_cs:
            H.append(_h("menor", "TABLA", f"tabla {i}", f"{sin_cs} fila(s) pueden partirse entre páginas (w:cantSplit)"))
    return H


def auditar_rotulos_y_figuras(doc) -> list[dict]:
    H = []
    secuencia = {"tabla": [], "figura": []}
    elementos = list(_cuerpo(doc))
    for k, (tipo, obj, idx) in enumerate(elementos):
        if tipo != "p":
            continue
        m = RE_ROTULO.match(obj.text)
        if not m:
            continue
        clase = m.group(1).lower()
        secuencia[clase].append(m.group(2))
        runs = [r for r in obj.runs if r.text.strip()]
        if not runs or not all(r.bold for r in runs):
            H.append(_h("menor", "ROTULO", f"párrafo {idx}: «{obj.text.strip()}»", "El rótulo debe ir en negrita"))
        sig = elementos[k + 1][1] if k + 1 < len(elementos) and elementos[k + 1][0] == "p" else None
        if sig is not None and sig.text.strip():
            r2 = [r for r in sig.runs if r.text.strip()]
            if not r2 or not all(r.italic for r in r2):
                H.append(_h("menor", "ROTULO", f"párrafo {idx}: «{obj.text.strip()}»", "El título debe ir en cursiva"))
    for clase, nums in secuencia.items():
        enteros = [int(n.split(".")[0]) for n in nums if n.split(".")[0].isdigit()]
        if enteros and all("." not in n for n in nums) and enteros != list(range(1, len(enteros) + 1)):
            H.append(_h("mayor", "ROTULO", clase, f"Numeración no correlativa: {nums[:15]}"))
    # Figuras: DPI efectivo al ancho mostrado
    for i, shp in enumerate(doc.inline_shapes, 1):
        try:
            blip = shp._inline.graphic.graphicData.pic.blipFill.blip
            parte = doc.part.related_parts[blip.embed]
            from io import BytesIO

            from PIL import Image
            with Image.open(BytesIO(parte.blob)) as im:
                px = im.size[0]
            pulg = shp.width.inches
            dpi = px / pulg if pulg else 0
            if dpi < DPI_MIN:
                H.append(_h("mayor", "FIGURA", f"imagen {i}", f"{dpi:.0f} DPI efectivos ({px} px en {pulg:.2f} in); mínimo 300"))
            el = shp._inline
            while el is not None and el.tag != qn("w:p"):
                el = el.getparent()
            par = Paragraph(el, doc)
            if par.alignment is None or int(par.alignment) != 1:
                H.append(_h("menor", "FIGURA", f"imagen {i}", "La imagen no está centrada"))
        except Exception as e:  # noqa: BLE001
            H.append(_h("menor", "FIGURA", f"imagen {i}", f"No se pudo evaluar ({type(e).__name__})"))
    return H


def auditar_referencias(doc) -> tuple[list[dict], dict]:
    H = []
    pars = [p for p in doc.paragraphs]
    cab = next((i for i, p in enumerate(pars) if RE_TITULO_REF.match(p.text)), None)
    citas_texto = set()
    for i, p in enumerate(pars):
        if cab is not None and i >= cab:
            break
        for m in RE_CITA.finditer(p.text):
            if m.group(1):
                for trozo in re.split(r";", m.group(1)):
                    a = re.search(r"([A-ZÁÉÍÓÚÑ][\wáéíóúñ-]+)[^0-9]*((?:19|20)\d{2})", trozo)
                    if a:
                        citas_texto.add((_norm(a.group(1)), a.group(2)))
            elif m.group(2):
                citas_texto.add((_norm(m.group(2)), m.group(3)[:4]))
    if cab is None:
        return [_h("mayor", "REFERENCIAS", "documento", "No se encontró el encabezado «Referencias»")], {"citas_unicas": len(citas_texto)}
    entradas = []
    for p in pars[cab + 1:]:
        if _es_titulo(p) and p.text.strip():
            break
        if p.text.strip():
            entradas.append(p)
    claves = []          # (apellido_principal, año)
    tokens_entrada = []  # (conjunto de apellidos del bloque de autores, año)
    for n, p in enumerate(entradas, 1):
        f = formato_parrafo(p)
        izq, prim = _cm(f["izq"]), _cm(f["primera"])
        if izq is None or prim is None or abs(izq - SANGRIA_CM) > TOL_SANGRIA or abs(prim + SANGRIA_CM) > TOL_SANGRIA:
            H.append(_h("mayor", "REFERENCIAS", f"entrada {n}: «{p.text[:50]}»", "Sin sangría francesa de 1.27 cm"))
        anio_m = re.search(r"\(((?:19|20)\d{2})[a-z]?\)", p.text)
        bloque = p.text[:anio_m.start()] if anio_m else p.text[:120]
        anio = anio_m.group(1) if anio_m else ""
        # Todos los apellidos del bloque de autores (apellidos compuestos: «Hernández Sampieri», «Balón Morejón»)
        toks = {_norm(w) for w in re.findall(r"[A-ZÁÉÍÓÚÑ][\wáéíóúñ'-]{2,}", bloque)}
        toks.discard("")
        m = re.match(r"\s*([A-ZÁÉÍÓÚÑ][\wáéíóúñ'-]+)", p.text)
        claves.append((_norm(m.group(1)) if m else "", anio))
        tokens_entrada.append((toks, anio))
        if "&" in p.text and re.search(r"y", p.text[:60]):
            H.append(_h("menor", "TEXTO", f"entrada {n}", "Mezcla de «&» y «y» en la lista de autores"))
    orden = [_norm(p.text) for p in entradas]
    desorden = [i for i in range(1, len(orden)) if orden[i] < orden[i - 1]]
    if desorden:
        i = desorden[0]
        H.append(_h("mayor", "REFERENCIAS", "lista", f"Fuera de orden alfabético ({len(desorden)} caso(s)); primero: "
                    f"«{entradas[i - 1].text[:35]}» antes de «{entradas[i].text[:35]}»"))

    def listada(apellido: str, anio: str) -> bool:
        return any(apellido in toks and (not anio or not y or y == anio) for toks, y in tokens_entrada)

    def citada(toks: set, anio: str) -> bool:
        return any(a in toks and (not anio or not y or y == anio) for a, y in citas_texto)

    sin_ref = sorted(c for c in citas_texto if not listada(*c))
    sin_cita = sorted(k for k, (toks, y) in zip(claves, tokens_entrada) if k[0] and not citada(toks, y))
    for a, y in sin_ref[:15]:
        H.append(_h("mayor", "REFERENCIAS", f"cita ({a}, {y})", "Cita en el texto sin entrada en Referencias"))
    for a, y in sin_cita[:15]:
        H.append(_h("menor", "REFERENCIAS", f"entrada ({a}, {y})", "Referencia sin ninguna cita en el texto"))
    return H, {"entradas": len(entradas), "citas_unicas": len(citas_texto), "citas_sin_referencia": len(sin_ref),
               "referencias_sin_cita": len(sin_cita)}


def auditar_texto(doc) -> list[dict]:
    H, n = [], 0
    for tipo, obj, idx in _cuerpo(doc):
        if tipo != "p" or not obj.text.strip():
            continue
        t = obj.text
        if re.search(r"\bet al\b(?!\.)", t) and n < 8:
            n += 1
            H.append(_h("menor", "TEXTO", f"párrafo {idx}", "«et al» sin punto final"))
        fuera = re.sub(r"\([^()]*\)", "", t)
        if re.search(r"[A-ZÁÉÍÓÚÑ][\wáéíóúñ-]+\s+&\s+[A-ZÁÉÍÓÚÑ]", fuera) and n < 8:
            n += 1
            H.append(_h("menor", "TEXTO", f"párrafo {idx}", "«&» fuera de paréntesis; en español se usa «y»"))
    return H


def auditar(ruta: str | Path, solo: set[str] | None = None) -> dict:
    ruta = Path(ruta)
    doc = Document(str(ruta))
    H: list[dict] = []
    resumen: dict = {}
    todos = {"margenes", "numeracion", "parrafos", "tablas", "figuras", "referencias", "texto"}
    activos = solo or todos
    if "margenes" in activos:
        H += auditar_margenes(doc)
    if "numeracion" in activos:
        H += auditar_numeracion(doc)
    if "parrafos" in activos:
        h, r = auditar_parrafos(doc)
        H += h
        resumen["parrafos"] = r
    if "tablas" in activos:
        H += auditar_tablas(doc)
    if "figuras" in activos:
        H += auditar_rotulos_y_figuras(doc)
    if "referencias" in activos:
        h, r = auditar_referencias(doc)
        H += h
        resumen["referencias"] = r
    if "texto" in activos:
        H += auditar_texto(doc)
    H.sort(key=lambda x: (ORDEN[x["severidad"]], x["regla"]))
    cuenta = Counter(x["severidad"] for x in H)
    resumen.update({"secciones": len(doc.sections), "tablas": len(doc.tables), "imagenes": len(doc.inline_shapes),
                    "parrafos_totales": len(doc.paragraphs)})
    return {"archivo": str(ruta), "sha256": seguridad.sha256_archivo(ruta), "resumen": resumen,
            "totales": {"critico": cuenta["critico"], "mayor": cuenta["mayor"], "menor": cuenta["menor"]},
            "por_regla": dict(Counter(x["regla"] for x in H)), "hallazgos": H}


def a_texto(inf: dict, max_filas: int = 50) -> str:
    t = inf["totales"]
    L = [f"Auditoría APA 7 / UNAJMA - {inf['archivo']}", f"SHA-256: {inf['sha256'][:16]}…",
         f"Resumen: {inf['resumen']}", f"CRÍTICOS {t['critico']} | MAYORES {t['mayor']} | menores {t['menor']}",
         f"Por regla: {inf['por_regla']}", ""]
    for h in inf["hallazgos"][:max_filas]:
        L.append(f"[{h['severidad'].upper():7}] {h['regla']:12} {h['donde']}: {h['detalle']}")
    if len(inf["hallazgos"]) > max_filas:
        L.append(f"… y {len(inf['hallazgos']) - max_filas} más (use --json o --md)")
    return "\n".join(L)


def a_markdown(inf: dict) -> str:
    t = inf["totales"]
    L = ["# Auditoría APA 7 / UNAJMA", "", f"- Archivo: `{inf['archivo']}`", f"- SHA-256: `{inf['sha256']}`",
         f"- Críticos **{t['critico']}** · Mayores **{t['mayor']}** · Menores {t['menor']}", "",
         "| Severidad | Regla | Ubicación | Detalle |", "|---|---|---|---|"]
    for h in inf["hallazgos"]:
        L.append(f"| {h['severidad']} | {h['regla']} | {h['donde']} | {h['detalle']} |")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    seguridad.configurar_utf8()
    ap = argparse.ArgumentParser(description="Auditor APA 7 / UNAJMA de .docx (solo lectura).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("auditar")
    p.add_argument("docx")
    p.add_argument("--solo", help="margenes,numeracion,parrafos,tablas,figuras,referencias,texto")
    p.add_argument("--json", action="store_true")
    p.add_argument("--md", action="store_true")
    p.add_argument("--salida")
    p = sub.add_parser("resumen-estructura")
    p.add_argument("docx")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    ruta = Path(a.docx)
    if not ruta.is_file() or ruta.suffix.lower() != ".docx":
        print(f"ERROR: se requiere un .docx existente: {ruta}", file=sys.stderr)
        return 2
    try:
        if a.cmd == "resumen-estructura":
            doc = Document(str(ruta))
            estilos = Counter(p.style.name for p in doc.paragraphs if p.text.strip())
            print(json.dumps({"secciones": len(doc.sections), "tablas": len(doc.tables), "imagenes": len(doc.inline_shapes),
                              "estilos": dict(estilos.most_common(15))}, ensure_ascii=False, indent=1))
            return 0
        solo = set(a.solo.split(",")) if a.solo else None
        inf = auditar(ruta, solo)
    except Exception as e:  # noqa: BLE001  (archivo corrupto, cifrado, no es un zip válido...)
        print(f"ERROR: no se pudo auditar {ruta.name}: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    cuerpo = json.dumps(inf, ensure_ascii=False, indent=1) if a.json else a_markdown(inf) if a.md else a_texto(inf)
    if a.salida:
        from scripts.agentes.escritura_segura import escribir_salida
        try:
            escribir_salida(a.salida, cuerpo)
        except (seguridad.EscrituraProhibida, FileExistsError) as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2
    print(cuerpo)
    return 1 if inf["totales"]["critico"] or inf["totales"]["mayor"] else 0


if __name__ == "__main__":
    sys.exit(main())
