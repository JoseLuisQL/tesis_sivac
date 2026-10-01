#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Guardián de consistencia (Squad B). SOLO LECTURA.

Detecta deriva de identidad y de metodología en .md / .txt / .py / .json / .docx:

  1. TITULO       título antiguo o deformado (debe ser rutas.TITULO_OFICIAL)
  2. AUTORIA      tesista o asesora distintos de los oficiales
  3. DEC007       dimensiones ajenas a las tres oficiales o recuentos distintos de tres
  4. DISENO       N distinto de 14 en contexto de muestra/población censal
  5. ISO          ISO/IEC 25010 con edición distinta de 2023
  6. INFERENCIA   cifras inferenciales (p =, W =, Z =, t(gl) =, r =, d =) en archivos sin
                  estado 'validado_con_datos_reales' -> CRÍTICO: resultado sin sustento empírico
  7. DICTAMEN     puntaje 'X / 20' de jurado sobre contenido no validado

Exit code: 0 sin críticos, 1 con críticos, 2 uso incorrecto.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from unidecode import unidecode  # noqa: E402

from scripts.comun import rutas, seguridad  # noqa: E402

EXT = {".md", ".txt", ".py", ".json", ".docx", ".cjs", ".js"}
MAX_BYTES = 3_000_000
DIRS_EXCLUIDOS = {".git", ".venv", ".claude", "node_modules", "__pycache__", ".obsidian", "vendor", "external_skills",
                  "_cuarentena_no_empiricos", "indices_pdf", "referencias", "tests", ".pytest_cache", "_adjuntos"}
ARCHIVOS_EXCLUIDOS = {"guardian_consistencia.py"}
ESTADO_VALIDADO = "validado_con_datos_reales"
ESTADO_INVALIDADO = "invalido_sin_datos_reales"
ORDEN = {"critico": 0, "mayor": 1, "menor": 2}


def _norm(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", unidecode(t).lower())


TITULO_OK = _norm(rutas.TITULO_OFICIAL)
RE_TITULO_ANTIGUO = re.compile(r"sistema\s+web\s+sivac\s+y\s+su\s+influencia", re.I)
RE_TITULO_INICIO = re.compile(r"aplicaci[oó]n\s+del\s+sistema\s+[“”\"']?\s*sivac[“”\"']?\s+para\s+\w+", re.I)
RE_BACH = re.compile(r"\bBach\.\s+([A-ZÁÉÍÓÚÑ][\wáéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][\wáéíóúñ]+){1,3})")
RE_ASESOR = re.compile(r"\bAsesor[a]?\b[^\n]{0,40}?\b(?:Dra?\.|Mg\.|Ing\.|M\.Sc\.)\s*([A-ZÁÉÍÓÚÑ][\wáéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][\wáéíóúñ]+){1,4})")
RE_NUM_SUJETOS = re.compile(r"\b[Nn]\s*=\s*(\d{1,4})\b")
RE_MUESTRA = re.compile(r"muestra\s+(?:de|es de|censal de|conformada por)\s+(\d{1,4})\b", re.I)
CTX_MUESTRA = re.compile(r"muestra|poblaci[oó]n|censal|trabajadores|personal|participantes", re.I)
RE_ISO = re.compile(r"ISO\s*/?\s*IEC\s*25010\s*[:\-]?\s*(\d{4})?", re.I)
DIMENSIONES_AJENAS = re.compile(r"fiabilidad|confiabilidad del inventario|inteligencia artificial|eficiencia del sistema", re.I)
CTX_PSICOMETRIA = re.compile(r"cronbach|alfa|omega|subdimensi|coeficiente|confiabilidad global|escala|subescala|cuestionario|instrumento|psicom[eé]tric|[ií]tem", re.I)
CTX_ANTECEDENTE = re.compile(r"\(\s*[A-ZÁÉÍÓÚÑ][^()]{1,90}?,?\s*(?:19|20)\d{2}[a-z]?\s*\)|[A-ZÁÉÍÓÚÑ][\wáéíóúñ-]+(?:\s+(?:y|&|et al\.)\s*[A-ZÁÉÍÓÚÑ]?[\wáéíóúñ-]*)?\s*\(\s*(?:19|20)\d{2}[a-z]?\s*\)|et al\.|antecedente|estudio (?:de|realizado)", re.I)
RE_CUENTA_DIM = re.compile(r"\b(dos|tres|cuatro|cinco|seis|[2-9])\s+dimensiones", re.I)
CUENTAS_OK = {"tres", "3"}

PATRONES_INFERENCIA = {
    "p": re.compile(r"\bp\s*(?:=\s*\.?\d|<\s*\.?0*1\b|<\s*0?\.001)", re.I),
    "W": re.compile(r"\bW\s*=\s*-?\d"),
    "Z": re.compile(r"\bZ\s*=\s*-?\d"),
    "t": re.compile(r"\bt\s*\(\s*\d+\s*\)\s*=\s*-?\d"),
    "r": re.compile(r"\br\s*=\s*-?0?\.\d"),
    "d": re.compile(r"\bd(?:_?z)?\s*=\s*-?\d"),
}
RE_DICTAMEN = re.compile(r"\b(\d{1,2}(?:[.,]\d{1,2})?)\s*/\s*20(?:[.,]0+)?\b")


def _hallazgo(sev, regla, archivo, linea, texto, detalle):
    return {"severidad": sev, "regla": regla, "archivo": str(archivo), "linea": linea,
            "texto": texto.strip()[:160], "detalle": detalle}


def leer_lineas(ruta: Path) -> list[str]:
    if ruta.suffix.lower() == ".docx":
        from docx import Document
        d = Document(str(ruta))
        lineas = [p.text for p in d.paragraphs]
        for t in d.tables:
            for fila in t.rows:
                lineas.append(" | ".join(c.text for c in fila.cells))
        return lineas
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return ruta.read_text(encoding=enc).splitlines()
        except UnicodeDecodeError:
            continue
    return []


def estado_frontmatter(lineas: list[str]) -> str | None:
    if not lineas or lineas[0].strip() != "---":
        return None
    for ln in lineas[1:25]:
        if ln.strip() == "---":
            break
        m = re.match(r"\s*estado\s*:\s*(\S+)", ln)
        if m:
            return m.group(1).strip("\"'")
    return None


def analizar(ruta: Path, lineas: list[str] | None = None, nombre: str | None = None) -> list[dict]:
    lineas = lineas if lineas is not None else leer_lineas(ruta)
    nombre = nombre or ruta.name
    H: list[dict] = []
    estado = estado_frontmatter(lineas)
    validado = estado == ESTADO_VALIDADO

    for i, ln in enumerate(lineas, 1):
        # 1. Título
        if RE_TITULO_ANTIGUO.search(ln):
            H.append(_hallazgo("mayor", "TITULO", ruta, i, ln, "Título antiguo; debe ser el oficial (CLAUDE.md §1)"))
        m = RE_TITULO_INICIO.search(ln)
        if m:
            resto = ln[m.start():]
            n = _norm(resto)
            if len(n) >= 60 and not n.startswith(TITULO_OK[:60]):
                H.append(_hallazgo("mayor", "TITULO", ruta, i, ln, "Título con texto distinto al oficial"))
            elif n.startswith(TITULO_OK) and "andahuaylas" in n[len(TITULO_OK):len(TITULO_OK) + 25]:
                H.append(_hallazgo("menor", "TITULO", ruta, i, ln, "El título oficial no lleva «Andahuaylas 2025» adosado"))

        # 2. Autoría
        for m in RE_BACH.finditer(ln):
            if _norm(m.group(1)) != _norm(rutas.TESISTA.replace("Bach. ", "")):
                H.append(_hallazgo("mayor", "AUTORIA", ruta, i, ln, f"Tesista distinto del oficial: «{m.group(1)}»"))
        m = RE_ASESOR.search(ln)
        if m and _norm(m.group(1)) != _norm(rutas.ASESORA.replace("Dra. ", "")):
            H.append(_hallazgo("mayor", "AUTORIA", ruta, i, ln, f"Asesor(a) distinto(a) del oficial: «{m.group(1)}»"))

        # 3. DEC-007
        if re.search(r"dimensi", ln, re.I) and DIMENSIONES_AJENAS.search(ln) and not CTX_PSICOMETRIA.search(ln):
            H.append(_hallazgo("mayor", "DEC007", ruta, i, ln, "Dimensión ajena a las tres oficiales (DEC-007)"))
        for m in RE_CUENTA_DIM.finditer(ln):
            if m.group(1).lower() not in CUENTAS_OK and re.search(r"variable dependiente|gesti[oó]n de movimientos|\bVD\b", ln, re.I):
                H.append(_hallazgo("mayor", "DEC007", ruta, i, ln, f"Recuento de dimensiones distinto de tres: «{m.group(0)}»"))

        # 4. Diseño censal
        if CTX_MUESTRA.search(ln):
            for m in list(RE_NUM_SUJETOS.finditer(ln)) + list(RE_MUESTRA.finditer(ln)):
                if int(m.group(1)) != rutas.N_CENSAL:
                    citado = bool(CTX_ANTECEDENTE.search(ln))
                    H.append(_hallazgo("menor" if citado else "mayor", "DISENO", ruta, i, ln,
                                       f"N distinto de {rutas.N_CENSAL}: «{m.group(0)}»"
                                       + (" (probable estudio citado como antecedente: revisar)" if citado else "")))

        # 5. ISO
        for m in RE_ISO.finditer(ln):
            if m.group(1) and m.group(1) != "2023":
                H.append(_hallazgo("mayor", "ISO", ruta, i, ln, f"ISO/IEC 25010:{m.group(1)}; la tesis usa 2023"))

    # 6. Inferencia prematura (nivel de archivo)
    es_antecedente = bool(re.search(r"capitulo2|capitulo_ii|antecedente", nombre, re.I))
    if not validado and not es_antecedente:
        if estado == ESTADO_INVALIDADO:
            # Archivo formalmente marcado y bloqueado como no empírico
            pass
        else:
            tipos, primera = Counter(), {}
            for i, ln in enumerate(lineas, 1):
                if CTX_ANTECEDENTE.search(ln):
                    continue
                for k, rx in PATRONES_INFERENCIA.items():
                    if rx.search(ln):
                        tipos[k] += 1
                        primera.setdefault(k, (i, ln))
            if len(tipos) >= 2:
                i, ln = min(primera.values())
                H.append(_hallazgo("critico", "INFERENCIA", ruta, i, ln,
                                   f"Cifras inferenciales ({', '.join(sorted(tipos))}) sin estado '{ESTADO_VALIDADO}': "
                                   f"resultado sin sustento empírico (no existen datos de campo certificados)"))

    # 7. Dictámenes
    es_dictamen = bool(re.search(r"dictamen|reportes_jurado|jurado", nombre, re.I)) or any(
        re.search(r"dictamen|jurado", ln, re.I) for ln in lineas[:40])
    if es_dictamen and not validado and estado != ESTADO_INVALIDADO:
        for i, ln in enumerate(lineas, 1):
            m = RE_DICTAMEN.search(ln)
            if m:
                H.append(_hallazgo("mayor", "DICTAMEN", ruta, i, ln,
                                   f"Puntaje «{m.group(0)}» de jurado sobre contenido no validado con datos reales"))
                break
    return H


def escanear(raiz: str | Path, incluir_cuarentena: bool = False) -> dict:
    raiz = Path(raiz).resolve(strict=False)
    excl = set(DIRS_EXCLUIDOS)
    if incluir_cuarentena:
        excl -= {"_cuarentena_no_empiricos"}
    archivos = [raiz] if raiz.is_file() else sorted(
        p for p in raiz.rglob("*") if p.is_file() and not (set(p.relative_to(raiz).parts[:-1]) & excl))
    hallazgos, leidos, omitidos = [], 0, []
    for p in archivos:
        if p.suffix.lower() not in EXT or p.name in ARCHIVOS_EXCLUIDOS or p.name.endswith(".idx.json"):
            continue
        try:
            if p.stat().st_size > MAX_BYTES:
                omitidos.append(f"{p.name} (> {MAX_BYTES // 1_000_000} MB)")
                continue
            hallazgos += analizar(p)
            leidos += 1
        except Exception as e:  # noqa: BLE001
            omitidos.append(f"{p.name} ({type(e).__name__})")
    hallazgos.sort(key=lambda h: (ORDEN[h["severidad"]], h["archivo"], h["linea"]))
    cuenta = Counter(h["severidad"] for h in hallazgos)
    return {"raiz": str(raiz), "archivos_leidos": leidos, "omitidos": omitidos,
            "totales": {"critico": cuenta["critico"], "mayor": cuenta["mayor"], "menor": cuenta["menor"]},
            "por_regla": dict(Counter(h["regla"] for h in hallazgos)), "hallazgos": hallazgos}


def a_texto(inf: dict, max_filas: int = 60) -> str:
    t = inf["totales"]
    L = [f"Guardián de consistencia — {inf['raiz']}",
         f"Archivos leídos: {inf['archivos_leidos']} | CRÍTICOS {t['critico']} | MAYORES {t['mayor']} | menores {t['menor']}",
         f"Por regla: {inf['por_regla']}", ""]
    for h in inf["hallazgos"][:max_filas]:
        L.append(f"[{h['severidad'].upper():7}] {h['regla']:10} {h['archivo']}:{h['linea']}")
        L.append(f"           {h['detalle']}")
    if len(inf["hallazgos"]) > max_filas:
        L.append(f"… y {len(inf['hallazgos']) - max_filas} hallazgos más (use --json o --md)")
    if inf["omitidos"]:
        L.append("Omitidos: " + "; ".join(inf["omitidos"][:10]))
    return "\n".join(L)


def a_markdown(inf: dict) -> str:
    t = inf["totales"]
    L = ["# Informe del Guardián de Consistencia", "", f"- Ruta: `{inf['raiz']}`",
         f"- Archivos leídos: {inf['archivos_leidos']}", f"- Críticos: **{t['critico']}** · Mayores: **{t['mayor']}** · Menores: {t['menor']}",
         "", "| Severidad | Regla | Archivo:línea | Detalle |", "|---|---|---|---|"]
    for h in inf["hallazgos"]:
        L.append(f"| {h['severidad']} | {h['regla']} | `{h['archivo']}:{h['linea']}` | {h['detalle']} |")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    seguridad.configurar_utf8()
    ap = argparse.ArgumentParser(description="Guardián de consistencia metodológica (solo lectura).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("escanear", help="Escanea un archivo o carpeta")
    p.add_argument("ruta")
    p.add_argument("--json", action="store_true")
    p.add_argument("--md", action="store_true")
    p.add_argument("--salida", help="Guardar el informe en este archivo (nuevo)")
    p.add_argument("--incluir-cuarentena", action="store_true")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    ruta = Path(a.ruta)
    if not ruta.exists():
        print(f"ERROR: no existe {ruta}", file=sys.stderr)
        return 2
    inf = escanear(ruta, a.incluir_cuarentena)
    cuerpo = json.dumps(inf, ensure_ascii=False, indent=1) if a.json else a_markdown(inf) if a.md else a_texto(inf)
    if a.salida:
        from scripts.agentes.escritura_segura import escribir_salida
        try:
            print(f"Escrito: {escribir_salida(a.salida, cuerpo)}", file=sys.stderr)
        except (seguridad.EscrituraProhibida, FileExistsError) as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2
    print(cuerpo)
    return 1 if inf["totales"]["critico"] else 0


if __name__ == "__main__":
    sys.exit(main())
