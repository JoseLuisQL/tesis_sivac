#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Revisor de prosa académica (Squad E). SOLO LECTURA, sin modelos de lenguaje ni red.

Aplica .claude/rules/03_estilo_academico_apa7.md y REPORTA (no reescribe):
  PERSONA     primera persona (yo, nosotros, mi, nuestro, «realizamos»…) fuera de citas textuales
  RELLENO     coloquialismos y frases vacías / de plantilla
  LONGITUD    oraciones > 45 palabras; párrafos fuera de 4-8 oraciones
  CITA        aseveración con cifra o «según» sin cita en el párrafo
  FORMATO     «&» en español, «et al» sin punto, dobles espacios, comillas mezcladas
  VERIFICAR   marcas [VERIFICAR: …] pendientes
  REPETICION  palabra de contenido repetida muy cerca

Cada párrafo recibe un puntaje 0-100 con criterios transparentes (100 - penalizaciones).
Exit code: 0 sin hallazgos mayores, 1 con alguno, 2 uso incorrecto.
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

from scripts.comun import seguridad  # noqa: E402

PENALIZA = {"mayor": 15, "menor": 5}
PRIMERA_PERSONA = re.compile(
    r"\b(yo|nosotros|nosotras|mi|mis|nuestro|nuestra|nuestros|nuestras|me|nos)\b"
    r"|\b(?:realizamos|obtuvimos|aplicamos|encontramos|analizamos|observamos|consideramos|concluimos|hemos|propongo|propusimos|desarrollamos|evaluamos|medimos)\b"
    r"|\b(?:realic[eé]|obtuve|apliqu[eé]|encontr[eé]|analic[eé]|observ[eé]|desarroll[eé]|evalu[eé]|med[ií])\b", re.I)
PRIMERA_PERSONA_AMBIGUA = {"me", "nos", "mi", "mis"}   # «mi» puede ser nota musical; se degrada a menor
RELLENO = [
    "cabe destacar que", "cabe mencionar que", "cabe señalar que", "como es sabido", "como bien se sabe",
    "hoy en día", "en la actualidad", "sin lugar a dudas", "es importante destacar", "es importante mencionar",
    "es de suma importancia", "en conclusión, podemos ver", "a lo largo de la historia", "desde tiempos inmemoriales",
    "de más está decir", "no cabe duda", "por supuesto", "básicamente", "obviamente", "evidentemente",
    "a nivel de", "la verdad es que", "en pocas palabras", "en resumen, se puede decir",
]
INTENSIFICADORES = re.compile(r"\b(muy|bastante|realmente|absolutamente|totalmente|increíblemente|extremadamente)\b", re.I)
RE_CITA_APA = re.compile(r"\([^()]*\b(?:19|20)\d{2}[a-z]?[^()]*\)|[A-ZÁÉÍÓÚÑ][\wáéíóúñ-]+(?:\s+(?:y|et al\.?))?\s*\((?:19|20)\d{2}[a-z]?\)|@\w+|\[\^?\w+\]")
RE_ASEVERACION = re.compile(r"\d+[.,]?\d*\s*%|\b(?:según|de acuerdo con|afirma|señala|sostiene|reporta|demostr[óo]|evidenci[óo]|concluy[óo])\b", re.I)
RE_CITA_TEXTUAL = re.compile(r"[“\"«][^”\"»]{3,}[”\"»]")
STOP = set("""de la que el en y a los del se las por un para con no una su al lo como más pero sus le ya o este sí porque esta entre cuando muy sin sobre también me hasta hay donde quien desde todo nos durante todos uno les ni contra otros ese eso ante ellos e esto mí antes algunos qué unos yo otro otras otra él tanto esa estos mucho quienes nada muchos cual poco ella estar estas algunas algo nosotros mi mis tú te ti tu tus ellas vosotros""".split())


def _hall(sev, regla, parrafo, detalle, fragmento=""):
    return {"severidad": sev, "regla": regla, "parrafo": parrafo, "detalle": detalle, "fragmento": fragmento[:120]}


def _sin_citas_textuales(t: str) -> str:
    return RE_CITA_TEXTUAL.sub(" ", t)


def oraciones(t: str) -> list[str]:
    t = re.sub(r"\b(?:et al|Dr|Dra|Mg|Ing|Lic|Bach|p|pp|vol|núm|no|cap|fig|ej|etc|art)\.", lambda m: m.group(0).replace(".", "§"), t)
    t = re.sub(r"(\d)\.(\d)", r"\1§\2", t)
    partes = re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿¡“\"(])", t.strip())
    return [p.replace("§", ".") for p in partes if p.strip()]


def leer_parrafos(ruta: Path) -> list[tuple[int, str]]:
    """(número de párrafo, texto) ignorando frontmatter YAML, código, encabezados y tablas Markdown."""
    if ruta.suffix.lower() == ".docx":
        from docx import Document
        return [(i, p.text) for i, p in enumerate(Document(str(ruta)).paragraphs, 1) if p.text.strip()]
    crudo = ruta.read_text(encoding="utf-8-sig")
    lineas = crudo.splitlines()
    if lineas and lineas[0].strip() == "---":
        fin = next((i for i in range(1, len(lineas)) if lineas[i].strip() == "---"), 0)
        lineas = lineas[fin + 1:]
    salida, buf, en_codigo, n = [], [], False, 0

    def volcar():
        nonlocal buf, n
        if buf:
            n += 1
            salida.append((n, " ".join(buf)))
            buf = []

    for ln in lineas:
        s = ln.strip()
        if s.startswith("```"):
            volcar()
            en_codigo = not en_codigo
            continue
        if en_codigo or not s or s.startswith(("#", "|", ">", "---", "![[", "<!--")) or re.match(r"^[-*+]\s|^\d+\.\s", s):
            volcar()
            continue
        buf.append(s)
    volcar()
    return salida


def revisar_parrafo(n: int, texto: str, modo: str = "informe") -> list[dict]:
    H: list[dict] = []
    limpio = _sin_citas_textuales(texto)
    oras = oraciones(texto)
    # Persona
    for m in PRIMERA_PERSONA.finditer(limpio):
        palabra = m.group(0).lower()
        H.append(_hall("menor" if palabra in PRIMERA_PERSONA_AMBIGUA else "mayor", "PERSONA", n,
                       f"Primera persona («{m.group(0)}»); la tesis se redacta en tercera persona o impersonal",
                       limpio[max(0, m.start() - 30):m.end() + 30]))
        break
    # Relleno
    bajo = unidecode(limpio).lower()
    for frase in RELLENO:
        if unidecode(frase).lower() in bajo:
            H.append(_hall("mayor", "RELLENO", n, f"Frase de relleno o coloquial: «{frase}»"))
    k = len(INTENSIFICADORES.findall(limpio))
    if k >= 2:
        H.append(_hall("menor", "RELLENO", n, f"{k} intensificadores (muy, bastante, realmente…): sustituir por datos"))
    # Longitud
    for o in oras:
        pal = len(o.split())
        if pal > 45:
            H.append(_hall("menor", "LONGITUD", n, f"Oración de {pal} palabras (máximo recomendado 45)", o))
    if len(limpio.split()) >= 40 and not 4 <= len(oras) <= 8:
        H.append(_hall("menor", "LONGITUD", n, f"Párrafo de {len(oras)} oraciones (rango 4 a 8)"))
    # Citas
    if RE_ASEVERACION.search(limpio) and not RE_CITA_APA.search(texto):
        H.append(_hall("mayor", "CITA", n, "Aseveración con cifra o atribución sin cita en el párrafo", limpio[:100]))
    # Formato
    if re.search(r"\bet al\b(?!\.)", texto):
        H.append(_hall("menor", "FORMATO", n, "«et al» sin punto final"))
    if re.search(r"[A-ZÁÉÍÓÚÑ][\wáéíóúñ-]+\s+&\s+[A-ZÁÉÍÓÚÑ]", re.sub(r"\([^()]*\)", "", texto)):
        H.append(_hall("menor", "FORMATO", n, "«&» fuera de paréntesis; en español se usa «y»"))
    if re.search(r"\S {2,}\S", texto):
        H.append(_hall("menor", "FORMATO", n, "Espacios dobles"))
    if ("“" in texto or "”" in texto) and '"' in texto:
        H.append(_hall("menor", "FORMATO", n, "Comillas tipográficas y rectas mezcladas"))
    for m in re.finditer(r"\[VERIFICAR[^\]]*\]", texto):
        H.append(_hall("menor", "VERIFICAR", n, f"Pendiente: {m.group(0)[:90]}"))
    # Repetición léxica (palabras de contenido >= 6 letras, >= 4 veces en el párrafo)
    palabras = [w for w in re.findall(r"[a-záéíóúñü]{6,}", limpio.lower()) if w not in STOP]
    for w, c in Counter(palabras).most_common(3):
        if c >= 4 and len(limpio.split()) < 220:
            H.append(_hall("menor", "REPETICION", n, f"«{w}» aparece {c} veces en el párrafo"))
            break
    return H


def puntaje(hallazgos: list[dict]) -> int:
    return max(0, 100 - sum(PENALIZA[h["severidad"]] for h in hallazgos))


def revisar(ruta: str | Path) -> dict:
    ruta = Path(ruta)
    pars = leer_parrafos(ruta)
    todos, por_parrafo = [], []
    for n, t in pars:
        h = revisar_parrafo(n, t)
        todos += h
        por_parrafo.append({"parrafo": n, "palabras": len(t.split()), "puntaje": puntaje(h), "hallazgos": len(h)})
    cuenta = Counter(h["severidad"] for h in todos)
    prom = round(sum(p["puntaje"] for p in por_parrafo) / len(por_parrafo), 1) if por_parrafo else None
    peores = sorted(por_parrafo, key=lambda p: p["puntaje"])[:10]
    return {"archivo": str(ruta), "parrafos": len(pars), "palabras": sum(p["palabras"] for p in por_parrafo),
            "puntaje_promedio": prom, "totales": {"mayor": cuenta["mayor"], "menor": cuenta["menor"]},
            "por_regla": dict(Counter(h["regla"] for h in todos)), "peores_parrafos": peores, "hallazgos": todos}


def contar_palabras(ruta: str | Path) -> dict:
    pars = leer_parrafos(Path(ruta))
    return {"archivo": str(ruta), "palabras": sum(len(t.split()) for _, t in pars), "parrafos": len(pars)}


def a_texto(inf: dict, max_filas: int = 40) -> str:
    t = inf["totales"]
    L = [f"Revisión de prosa — {inf['archivo']}",
         f"Párrafos {inf['parrafos']} | palabras {inf['palabras']} | puntaje promedio {inf['puntaje_promedio']}/100 | "
         f"MAYORES {t['mayor']} | menores {t['menor']}", f"Por regla: {inf['por_regla']}", ""]
    for h in sorted(inf["hallazgos"], key=lambda x: (x["severidad"] != "mayor", x["parrafo"]))[:max_filas]:
        L.append(f"[{h['severidad'].upper():5}] p.{h['parrafo']:<4} {h['regla']:10} {h['detalle']}")
    if len(inf["hallazgos"]) > max_filas:
        L.append(f"… y {len(inf['hallazgos']) - max_filas} más (use --json o --md)")
    L.append("\nPeores párrafos: " + ", ".join(f"p.{p['parrafo']} ({p['puntaje']})" for p in inf["peores_parrafos"][:6]))
    return "\n".join(L)


def a_markdown(inf: dict) -> str:
    L = ["# Revisión de prosa académica", "", f"- Archivo: `{inf['archivo']}`", f"- Párrafos: {inf['parrafos']} · Palabras: {inf['palabras']}",
         f"- Puntaje promedio: **{inf['puntaje_promedio']}/100** · Mayores {inf['totales']['mayor']} · Menores {inf['totales']['menor']}", "",
         "| Sev. | Párrafo | Regla | Detalle |", "|---|---|---|---|"]
    for h in sorted(inf["hallazgos"], key=lambda x: (x["severidad"] != "mayor", x["parrafo"])):
        L.append(f"| {h['severidad']} | {h['parrafo']} | {h['regla']} | {h['detalle']} |")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    seguridad.configurar_utf8()
    ap = argparse.ArgumentParser(description="Revisor de prosa académica (solo reporta).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("revisar")
    p.add_argument("archivo")
    p.add_argument("--json", action="store_true")
    p.add_argument("--md", action="store_true")
    p.add_argument("--salida")
    p = sub.add_parser("conteo-palabras")
    p.add_argument("archivo")
    p.add_argument("--esperado", type=int, help="Falla (exit 1) si el conteo es distinto")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    ruta = Path(a.archivo)
    if not ruta.is_file() or ruta.suffix.lower() not in {".md", ".txt", ".docx"}:
        print(f"ERROR: se requiere un .md, .txt o .docx existente: {ruta}", file=sys.stderr)
        return 2
    try:
        if a.cmd == "conteo-palabras":
            r = contar_palabras(ruta)
            print(json.dumps(r, ensure_ascii=False))
            return 1 if a.esperado is not None and r["palabras"] != a.esperado else 0
        inf = revisar(ruta)
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: no se pudo revisar {ruta.name}: {type(e).__name__}: {e}", file=sys.stderr)
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
    return 1 if inf["totales"]["mayor"] else 0


if __name__ == "__main__":
    sys.exit(main())
