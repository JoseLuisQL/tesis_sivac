#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Curador del Cerebro (Squad F): auditoría y mantenimiento
NO DESTRUCTIVO del vault de Obsidian.

Comandos de solo lectura:
    auditar                 frontmatter, enlaces rotos, huérfanas, duplicados, vacías,
                            conteo por carpeta canónica, bandeja 99_INBOX, validado/borrador
    enlaces <nota>          enlaces salientes y entrantes de una nota
    backlinks [<nota>]      entrantes de una nota, o ranking de notas más enlazadas

Comandos con escritura mínima y segura (nunca borran, mueven ni renombran):
    crear-nota              crea una nota con frontmatter válido; falla si ya existe
    registrar-bitacora      añade (append-only) una entrada a bitacoras/<agente>.md
    registrar-handoff       crea un handoff validado contra handoff.schema.json (<= 300 palabras)
    marcar-estado           edita solo las líneas `estado:` y `fecha_actualizacion:`
                            del frontmatter y lo deja registrado en la bitácora

Uso (desde la raíz del repo):
    .venv/Scripts/python.exe scripts/agentes/curador_cerebro.py auditar [--json]
    .venv/Scripts/python.exe scripts/agentes/curador_cerebro.py enlaces "MOC-01-Metodologia-Epistemologia"
    .venv/Scripts/python.exe scripts/agentes/curador_cerebro.py crear-nota --ruta 99_INBOX/x.md \
        --tipo nota --fase F1 --agente curador-cerebro --estado borrador --titulo "X"

El vault se toma de SIVAC_VAULT (o --vault). Códigos de salida: 0 ok, 1 hallazgos/fallos, 2 uso incorrecto.
Principios: cero invención (lo no confirmable se reporta, no se adivina); el script carece de
operaciones de borrado, movimiento o renombrado sobre el vault.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad  # noqa: E402

AGENTE = "curador-cerebro"
CLAVES_OBLIGATORIAS = ("tipo", "fase", "agente", "estado", "fecha_actualizacion")
# Alias aceptados (notas históricas del vault usan estas variantes).
ALIAS_CLAVES = {
    "agente": ("agente_emisor", "director", "creado_por"),
    "fecha_actualizacion": ("fecha",),
}
CARPETAS_CANONICAS = (
    "00_SISTEMA", "01_MOCS", "02_PROYECTOS", "03_CONCEPTOS_ATOMICOS",
    "04_LITERATURA_Y_FUENTES", "05_MODELOS_Y_REFERENCIAS", "06_METODOLOGIA_E_INSTRUMENTOS",
    "07_ESTADISTICA_Y_DATOS", "08_SISTEMA_Y_AGENTES", "09_CANVAS_Y_DIAGRAMAS", "99_INBOX",
)
PREFIJOS_AGENTES = ("00_SISTEMA/", "08_SISTEMA_Y_AGENTES/")
ESTADOS_VALIDADO = {"validado", "aprobado", "verificado", "completado", "completado_exitoso", "cerrado"}
ESTADOS_BORRADOR = {"borrador", "pendiente", "en_progreso", "en_revision", "parcial", "bloqueado", "inicial"}
LIMITE_PALABRAS_HANDOFF = 300
_RE_WIKILINK = re.compile(r"(!?)\[\[([^\]\n]*)\]\]")
_RE_CODIGO = re.compile(r"```.*?```|~~~.*?~~~|`[^`\n]*`", re.S)
_RE_COMENT = re.compile(r"<!--.*?-->", re.S)
_RE_AGENTE = re.compile(r"^[a-z0-9][a-z0-9\-]{1,60}$")
_RE_ESTADO = re.compile(r"^[a-z0-9_áéíóúñ\-]{2,40}$")


# ----------------------------------------------------------------------------
# Utilidades puras
# ----------------------------------------------------------------------------
def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def normalizar_nombre(s: str) -> str:
    """Nombre normalizado para detectar duplicados: sin tildes, minúsculas, solo alfanumérico."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60] or "sin-titulo"


def leer_texto(ruta: Path) -> str:
    return ruta.read_text(encoding="utf-8-sig", errors="replace")


def separar_frontmatter(texto: str) -> tuple[str | None, str]:
    """Devuelve (bloque_yaml | None, cuerpo). None si no hay frontmatter delimitado."""
    lineas = texto.lstrip("﻿").splitlines(keepends=True)
    if not lineas or lineas[0].strip() != "---":
        return None, texto
    for i in range(1, len(lineas)):
        if lineas[i].strip() in ("---", "..."):
            return "".join(lineas[1:i]), "".join(lineas[i + 1:])
    return None, texto


def parsear_frontmatter(texto: str) -> tuple[dict | None, str | None, str]:
    """(datos, error, cuerpo). datos=None y error=None -> sin frontmatter."""
    bloque, cuerpo = separar_frontmatter(texto)
    if bloque is None:
        if texto.lstrip("﻿").startswith("---"):
            return None, "frontmatter sin cierre '---'", cuerpo
        return None, None, cuerpo
    try:
        datos = yaml.safe_load(bloque)
    except yaml.YAMLError as e:
        return None, f"YAML inválido: {str(e).splitlines()[0]}", cuerpo
    if datos is None:
        datos = {}
    if not isinstance(datos, dict):
        return None, "el frontmatter no es un mapa clave: valor", cuerpo
    return datos, None, cuerpo


def extraer_wikilinks(cuerpo: str) -> list[dict]:
    """Enlaces [[destino#ancla|alias]] fuera de bloques de código y comentarios."""
    limpio = _RE_COMENT.sub("", _RE_CODIGO.sub("", cuerpo))
    salida = []
    for m in _RE_WIKILINK.finditer(limpio):
        bruto = m.group(2)
        destino = bruto.split("|", 1)[0].rstrip("\\")      # `\|` = pipe escapado en tablas
        destino = destino.split("#", 1)[0].split("^", 1)[0].strip()
        salida.append({"bruto": bruto, "destino": nfc(destino), "embed": bool(m.group(1))})
    return salida


def valor_clave(datos: dict, clave: str) -> Any:
    """Valor de una clave obligatoria aceptando alias históricos; (None) si falta."""
    for k in (clave, *ALIAS_CLAVES.get(clave, ())):
        v = datos.get(k)
        if v not in (None, "", []):
            return v
    return None


def clasificar_estado(estado: Any) -> str:
    if estado in (None, ""):
        return "sin_estado"
    e = str(estado).strip().lower()
    if e in ESTADOS_VALIDADO or e.startswith(("aprobado", "verificado", "definitivo", "completado")):
        return "validado"
    if e in ESTADOS_BORRADOR or e.startswith(("borrador", "pendiente", "en_")):
        return "borrador"
    return "otro"


# ----------------------------------------------------------------------------
# Modelo del vault
# ----------------------------------------------------------------------------
class Vault:
    """Lectura del vault: notas, archivos adjuntos, índices de resolución y enlaces."""

    def __init__(self, raiz: Path):
        self.raiz = Path(raiz)
        self.notas: dict[str, dict] = {}       # ruta relativa (posix, con .md) -> info
        self.archivos: list[str] = []          # rutas relativas de todo archivo no-md
        self.canvas: list[str] = []
        self._construir()

    # -- construcción -------------------------------------------------------
    def _rel(self, p: Path) -> str:
        return nfc(p.relative_to(self.raiz).as_posix())

    def _construir(self) -> None:
        for p in sorted(self.raiz.rglob("*")):
            if not p.is_file():
                continue
            partes = p.relative_to(self.raiz).parts
            if any(x.startswith(".") for x in partes):   # .obsidian, .trash, .git
                continue
            rel = self._rel(p)
            if p.suffix.lower() == ".md":
                self.notas[rel] = self._leer_nota(p, rel)
            else:
                self.archivos.append(rel)
                if p.suffix.lower() == ".canvas":
                    self.canvas.append(rel)
        self._indexar()
        self._resolver_enlaces()

    def _leer_nota(self, p: Path, rel: str) -> dict:
        texto = leer_texto(p)
        datos, error, cuerpo = parsear_frontmatter(texto)
        alias = []
        if datos:
            a = datos.get("aliases", datos.get("alias"))
            alias = [str(x) for x in a] if isinstance(a, list) else ([str(a)] if a else [])
        return {
            "ruta": rel, "nombre": nfc(p.stem), "bytes": p.stat().st_size,
            "vacia": not texto.strip(), "solo_frontmatter": bool(texto.strip()) and not cuerpo.strip(),
            "frontmatter": datos, "error_fm": error, "alias": alias,
            "enlaces": extraer_wikilinks(cuerpo), "salientes": [], "entrantes": set(),
        }

    def _indexar(self) -> None:
        self.por_ruta: dict[str, str] = {}
        self.por_nombre: dict[str, list[str]] = defaultdict(list)
        self.por_alias: dict[str, list[str]] = defaultdict(list)
        self.por_archivo: dict[str, list[str]] = defaultdict(list)
        for rel, n in self.notas.items():
            self.por_ruta[rel[:-3].lower()] = rel
            self.por_nombre[n["nombre"].lower()].append(rel)
            for a in n["alias"]:
                self.por_alias[nfc(a).lower()].append(rel)
        for rel in self.archivos:
            self.por_ruta[rel.lower()] = rel
            self.por_archivo[rel.rsplit("/", 1)[-1].lower()].append(rel)

    # -- resolución ---------------------------------------------------------
    def resolver(self, destino: str) -> list[str]:
        """Rutas que satisface un destino de wikilink (vacío = sin coincidencia)."""
        t = nfc(destino.strip().replace("\\", "/")).lower()
        t = t[:-3] if t.endswith(".md") else t
        if not t:
            return []
        if "/" in t:
            if t in self.por_ruta:
                return [self.por_ruta[t]]
            return [r for k, r in self.por_ruta.items() if k.endswith("/" + t)]
        if t in self.por_nombre:
            return list(self.por_nombre[t])
        if t in self.por_alias:
            return list(self.por_alias[t])
        if t in self.por_archivo:
            return list(self.por_archivo[t])
        return []

    def _resolver_enlaces(self) -> None:
        for rel, n in self.notas.items():
            for e in n["enlaces"]:
                if not e["destino"]:            # [[#ancla]] -> enlace interno, siempre válido
                    e["resuelto"], e["ambiguo"] = [rel], False
                    continue
                dest = self.resolver(e["destino"])
                e["resuelto"], e["ambiguo"] = dest, len(dest) > 1
                for d in dest[:1]:
                    if d != rel and d in self.notas:
                        self.notas[d]["entrantes"].add(rel)
        # Canvas: los nodos de tipo archivo cuentan como referencias entrantes.
        for cv in self.canvas:
            try:
                datos = json.loads(leer_texto(self.raiz / cv))
            except (OSError, ValueError):
                continue
            for nodo in datos.get("nodes", []):
                if nodo.get("type") == "file" and nodo.get("file"):
                    dest = self.resolver(nodo["file"])
                    if dest and dest[0] in self.notas:
                        self.notas[dest[0]]["entrantes"].add(cv)

    def localizar(self, ref: str) -> list[str]:
        """Resuelve una referencia de usuario (ruta, nombre o alias) a notas existentes."""
        return [r for r in self.resolver(ref) if r in self.notas]

    def carpeta_superior(self, rel: str) -> str:
        return rel.split("/", 1)[0] if "/" in rel else "(raíz)"


# ----------------------------------------------------------------------------
# Auditoría (pura, sin efectos)
# ----------------------------------------------------------------------------
def es_nota_de_agente(n: dict) -> bool:
    if n["ruta"].startswith(PREFIJOS_AGENTES):
        return True
    fm = n["frontmatter"] or {}
    return any(k in fm for k in ("agente", "agente_emisor", "director", "creado_por"))


def auditar_vault(v: Vault) -> dict:
    """Devuelve el informe completo de la auditoría (estructura serializable)."""
    frontmatter = {"invalidos": [], "incompletos": [], "sin_frontmatter_agente": [],
                   "por_alias": [], "evaluadas": 0, "sin_frontmatter_total": 0}
    enlaces_rotos, ambiguos, vacias, solo_fm = [], [], [], []
    estados = Counter()
    estados_raw = Counter()
    nombres: dict[str, list[str]] = defaultdict(list)
    por_carpeta = Counter()
    enlaces_total = 0

    for rel, n in v.notas.items():
        por_carpeta[v.carpeta_superior(rel)] += 1
        nombres[normalizar_nombre(n["nombre"])].append(rel)
        if n["vacia"]:
            vacias.append(rel)
        elif n["solo_frontmatter"]:
            solo_fm.append(rel)
        if n["error_fm"]:
            frontmatter["invalidos"].append({"nota": rel, "error": n["error_fm"]})
        if n["frontmatter"] is None and not n["error_fm"]:
            frontmatter["sin_frontmatter_total"] += 1
        fm = n["frontmatter"]
        estado = valor_clave(fm, "estado") if fm else None
        estados[clasificar_estado(estado)] += 1
        if estado not in (None, ""):
            estados_raw[str(estado)] += 1
        if es_nota_de_agente(n) and not n["error_fm"]:
            frontmatter["evaluadas"] += 1
            if fm is None:
                frontmatter["sin_frontmatter_agente"].append(rel)
            else:
                faltan = [k for k in CLAVES_OBLIGATORIAS if valor_clave(fm, k) is None]
                if faltan:
                    frontmatter["incompletos"].append({"nota": rel, "faltan": faltan})
                usados = [k for k in CLAVES_OBLIGATORIAS if k not in fm and valor_clave(fm, k) is not None]
                if usados:
                    frontmatter["por_alias"].append(rel)
        for e in n["enlaces"]:
            enlaces_total += 1
            if not e["resuelto"]:
                enlaces_rotos.append({"origen": rel, "destino": e["destino"] or e["bruto"], "embed": e["embed"]})
            elif e["ambiguo"]:
                ambiguos.append({"origen": rel, "destino": e["destino"], "candidatos": e["resuelto"]})

    huerfanas = sorted(r for r, n in v.notas.items() if not n["entrantes"] and r != "HOME.md" and not n["vacia"])
    duplicados = [{"nombre_normalizado": k, "notas": sorted(vs)} for k, vs in sorted(nombres.items()) if len(vs) > 1]
    inbox = sorted(r for r in v.notas if r.startswith("99_INBOX/"))
    sin_clasificar = [r for r in inbox if clasificar_estado(valor_clave(v.notas[r]["frontmatter"] or {}, "estado")) != "validado"]
    canonicas = {c: por_carpeta.get(c, 0) for c in CARPETAS_CANONICAS}
    fuera = {c: k for c, k in por_carpeta.items() if c not in CARPETAS_CANONICAS}
    faltantes = [c for c in CARPETAS_CANONICAS if not (v.raiz / c).is_dir()]

    informe = {
        "vault": str(v.raiz), "fecha": dt.date.today().isoformat(),
        "totales": {"notas": len(v.notas), "archivos_no_md": len(v.archivos), "enlaces": enlaces_total},
        "por_carpeta": canonicas, "fuera_de_estructura_canonica": fuera, "carpetas_canonicas_ausentes": faltantes,
        "frontmatter": frontmatter,
        "enlaces_rotos": enlaces_rotos, "enlaces_ambiguos": ambiguos,
        "huerfanas": huerfanas, "duplicados": duplicados,
        "vacias": sorted(vacias), "solo_frontmatter": sorted(solo_fm),
        "inbox": {"total": len(inbox), "sin_clasificar": sin_clasificar},
        "estados": dict(estados), "estados_detalle": dict(estados_raw.most_common()),
    }
    informe["errores"] = (len(frontmatter["invalidos"]) + len(enlaces_rotos) + len(vacias))
    informe["avisos"] = (len(frontmatter["incompletos"]) + len(frontmatter["sin_frontmatter_agente"])
                         + len(huerfanas) + len(duplicados) + len(sin_clasificar) + len(ambiguos))
    return informe


def _lista(titulo: str, items: list, formato, maximo: int) -> list[str]:
    out = [f"\n{titulo} ({len(items)})"]
    for it in items[:maximo]:
        out.append("  - " + formato(it))
    if len(items) > maximo:
        out.append(f"  ... y {len(items) - maximo} más (use --json o --max)")
    return out


def formatear_auditoria(inf: dict, maximo: int = 15) -> str:
    t = inf["totales"]
    L = [f"AUDITORÍA DEL VAULT  {inf['vault']}  ({inf['fecha']})",
         f"Notas: {t['notas']} | archivos no-md: {t['archivos_no_md']} | wikilinks: {t['enlaces']}",
         "\nNotas por carpeta canónica"]
    for c, k in inf["por_carpeta"].items():
        L.append(f"  {c:<34}{k:>5}")
    if inf["fuera_de_estructura_canonica"]:
        L.append("  Fuera de estructura canónica: " + ", ".join(f"{c}={k}" for c, k in inf["fuera_de_estructura_canonica"].items()))
    if inf["carpetas_canonicas_ausentes"]:
        L.append("  Carpetas canónicas ausentes: " + ", ".join(inf["carpetas_canonicas_ausentes"]))
    fm = inf["frontmatter"]
    L.append(f"\nFrontmatter: {fm['evaluadas']} notas de agente evaluadas; {fm['sin_frontmatter_total']} notas en total sin frontmatter")
    L += _lista("YAML inválido [ERROR]", fm["invalidos"], lambda x: f"{x['nota']}: {x['error']}", maximo)
    L += _lista("Notas de agente con claves faltantes [aviso]", fm["incompletos"], lambda x: f"{x['nota']}: faltan {', '.join(x['faltan'])}", maximo)
    L += _lista("Notas de agente sin frontmatter [aviso]", fm["sin_frontmatter_agente"], str, maximo)
    L += _lista("Wikilinks rotos [ERROR]", inf["enlaces_rotos"], lambda x: f"{x['origen']} -> [[{x['destino']}]]", maximo)
    L += _lista("Wikilinks ambiguos [aviso]", inf["enlaces_ambiguos"], lambda x: f"{x['origen']} -> [[{x['destino']}]] ({len(x['candidatos'])} candidatos)", maximo)
    L += _lista("Notas huérfanas (sin entrantes) [aviso]", inf["huerfanas"], str, maximo)
    L += _lista("Duplicados por nombre normalizado [aviso]", inf["duplicados"], lambda x: " | ".join(x["notas"]), maximo)
    L += _lista("Archivos vacíos [ERROR]", inf["vacias"], str, maximo)
    L += _lista("Notas con solo frontmatter (sin cuerpo)", inf["solo_frontmatter"], str, maximo)
    L += _lista("99_INBOX sin clasificar [aviso]", inf["inbox"]["sin_clasificar"], str, maximo)
    e = inf["estados"]
    L.append(f"\nEstado: validado={e.get('validado', 0)} borrador={e.get('borrador', 0)} "
             f"otro={e.get('otro', 0)} sin_estado={e.get('sin_estado', 0)}")
    L.append(f"\nRESUMEN: {inf['errores']} errores, {inf['avisos']} avisos")
    return "\n".join(L)


# ----------------------------------------------------------------------------
# Escritura segura
# ----------------------------------------------------------------------------
class ErrorCurador(Exception):
    """Error controlado de uso o de validación (salida 1)."""


def destino_en_vault(vault: Path, rel: str) -> Path:
    """Valida que `rel` apunte dentro del vault, sin '..', y que esté permitido escribirlo."""
    rel = rel.replace("\\", "/")
    if rel.startswith("/") or rel.endswith("/"):
        raise ErrorCurador(f"Ruta relativa no válida: {rel!r}")
    if not rel or ".." in Path(rel).parts or Path(rel).is_absolute() or ":" in rel:
        raise ErrorCurador(f"Ruta relativa no válida: {rel!r}")
    if any(p.startswith(".") for p in Path(rel).parts):
        raise ErrorCurador("No se escribe en carpetas ocultas del vault (.obsidian, etc.).")
    destino = (Path(vault) / rel).resolve(strict=False)
    try:
        destino.relative_to(Path(vault).resolve(strict=False))
    except ValueError as e:
        raise ErrorCurador(f"La ruta sale del vault: {destino}") from e
    return seguridad.asegurar_escritura_permitida(destino)


def _escalar_yaml(valor: str) -> str:
    """Serializa un escalar YAML seguro (comillas si contiene caracteres especiales)."""
    return json.dumps(valor, ensure_ascii=False) if re.search(r"[:#\[\]{}&*!|>'\"%@`,\n]|^\s|\s$", valor) else valor


def crear_nota(vault: Path, ruta: str, tipo: str, fase: str, agente: str, estado: str,
               titulo: str, texto: str = "", fecha: str | None = None) -> Path:
    if not ruta.lower().endswith(".md"):
        raise ErrorCurador("La ruta de la nota debe terminar en .md")
    if not _RE_AGENTE.match(agente):
        raise ErrorCurador("Nombre de agente inválido (minúsculas, dígitos y guiones).")
    if not _RE_ESTADO.match(estado):
        raise ErrorCurador("Estado inválido (minúsculas, dígitos, '_' o '-').")
    for nombre, val in (("tipo", tipo), ("fase", fase), ("titulo", titulo)):
        if not val.strip():
            raise ErrorCurador(f"El campo {nombre} no puede estar vacío.")
    destino = destino_en_vault(vault, ruta)
    fecha = fecha or dt.date.today().isoformat()
    cuerpo = f"---\ntipo: {_escalar_yaml(tipo)}\nfase: {_escalar_yaml(fase)}\nagente: {agente}\nestado: {estado}\n" \
             f"fecha_actualizacion: {fecha}\n---\n\n# {titulo}\n\n{texto.strip()}\n"
    destino.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(destino, "x", encoding="utf-8", newline="\n") as f:   # 'x': falla si existe
            f.write(cuerpo)
    except FileExistsError as e:
        raise ErrorCurador(f"La nota ya existe; no se sobrescribe: {destino}") from e
    return destino


def registrar_bitacora(vault: Path, agente: str, texto: str, ahora: dt.datetime | None = None) -> Path:
    if not _RE_AGENTE.match(agente):
        raise ErrorCurador("Nombre de agente inválido (minúsculas, dígitos y guiones).")
    if not texto.strip():
        raise ErrorCurador("El texto de la bitácora no puede estar vacío.")
    destino = destino_en_vault(vault, f"08_SISTEMA_Y_AGENTES/bitacoras/{agente}.md")
    ahora = ahora or dt.datetime.now()
    destino.parent.mkdir(parents=True, exist_ok=True)
    nuevo = not destino.exists()
    with open(destino, "a", encoding="utf-8", newline="\n") as f:        # solo añade al final
        if nuevo:
            f.write(f"# BITÁCORA DEL AGENTE: {agente.upper()}\n")
        f.write(f"\n## {ahora:%Y-%m-%d %H:%M} — {agente}\n{texto.strip()}\n")
    return destino


def contar_palabras(registro: dict) -> int:
    def palabras(x: Any) -> int:
        if isinstance(x, str):
            return len(x.split())
        if isinstance(x, list):
            return sum(palabras(i) for i in x)
        return 0
    return sum(palabras(v) for k, v in registro.items() if k != "fecha")


def validar_handoff(registro: dict, esquema_ruta: Path | None = None) -> list[str]:
    """Errores de validación del handoff contra el esquema JSON y el límite de palabras."""
    import jsonschema
    esquema_ruta = esquema_ruta or (rutas.SCHEMAS_CLAUDE / "handoff.schema.json")
    esquema = json.loads(Path(esquema_ruta).read_text(encoding="utf-8"))
    validador = jsonschema.Draft7Validator(esquema, format_checker=jsonschema.FormatChecker())
    errores = [f"{'/'.join(map(str, e.absolute_path)) or '(raíz)'}: {e.message}" for e in validador.iter_errors(registro)]
    try:
        dt.date.fromisoformat(str(registro.get("fecha", "")))
    except ValueError:
        errores.append("fecha: debe ser una fecha válida AAAA-MM-DD")
    if not _RE_AGENTE.match(str(registro.get("agente", ""))):
        errores.append("agente: debe ser minúsculas, dígitos y guiones (nombre de archivo seguro)")
    n = contar_palabras(registro)
    if n > LIMITE_PALABRAS_HANDOFF:
        errores.append(f"extensión: {n} palabras exceden el límite de {LIMITE_PALABRAS_HANDOFF}")
    return errores


def _seccion(titulo: str, items: list[str]) -> str:
    return f"## {titulo}\n" + ("\n".join(f"- {i}" for i in items) if items else "- (ninguno)") + "\n"


def registrar_handoff(vault: Path, registro: dict, tarea: str, esquema_ruta: Path | None = None) -> Path:
    errores = validar_handoff(registro, esquema_ruta)
    if errores:
        raise ErrorCurador("Handoff inválido:\n  - " + "\n  - ".join(errores))
    destino = destino_en_vault(vault, f"08_SISTEMA_Y_AGENTES/handoffs/{registro['fecha']}_{registro['agente']}_{slug(tarea)}.md")
    md = (f"---\ntipo: handoff\nfase: {_escalar_yaml(registro['fase'])}\nagente: {registro['agente']}\n"
          f"estado: {registro['estado']}\nfecha_actualizacion: {registro['fecha']}\nfecha: {registro['fecha']}\n---\n\n"
          f"# HANDOFF — {registro['agente']} — {tarea.strip()}\n\n"
          f"## Estado\n- {registro['estado']}\n\n"
          + _seccion("Productos generados", registro["productos_generados"]) + "\n"
          + _seccion("Hallazgos clave", registro["hallazgos_clave"]) + "\n"
          + _seccion("Pendientes / [VERIFICAR]", registro["pendientes_o_verificar"]) + "\n"
          + _seccion("Riesgos o incoherencias", registro.get("riesgos_o_incoherencias", [])) + "\n"
          f"## Siguiente acción sugerida\n{registro['siguiente_accion_sugerida']}\n")
    destino.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(destino, "x", encoding="utf-8", newline="\n") as f:
            f.write(md)
    except FileExistsError as e:
        raise ErrorCurador(f"El handoff ya existe; no se sobrescribe: {destino}") from e
    return destino


def _edita_linea(lineas: list[str], ini: int, fin: int, clave: str, valor: str) -> tuple[bool, str | None]:
    """Reemplaza `clave:` dentro de lineas[ini:fin] o la inserta antes de `fin`. -> (cambió, previo)."""
    patron = re.compile(rf"^{clave}\s*:(.*?)(\r?\n?)$")
    for i in range(ini, fin):
        m = patron.match(lineas[i])
        if m:
            previo = m.group(1).strip()
            lineas[i] = f"{clave}: {valor}{m.group(2) or chr(10)}"
            return previo != valor, previo
    eol = "\r\n" if lineas[0].endswith("\r\n") else "\n"
    lineas.insert(fin, f"{clave}: {valor}{eol}")
    return True, None


def marcar_estado(vault: Path, ref: str, estado: str, fecha: str | None = None,
                  simular: bool = False) -> dict:
    """Cambia solo `estado:` y `fecha_actualizacion:`; registra el cambio en la bitácora del curador."""
    if not _RE_ESTADO.match(estado):
        raise ErrorCurador("Estado inválido (minúsculas, dígitos, '_' o '-').")
    v = Vault(vault)
    candidatas = v.localizar(ref)
    if not candidatas:
        raise ErrorCurador(f"No se encontró la nota: {ref}")
    if len(candidatas) > 1:
        raise ErrorCurador("Referencia ambigua, use la ruta completa: " + ", ".join(candidatas))
    rel = candidatas[0]
    destino = destino_en_vault(vault, rel)
    crudo = destino.read_bytes()
    bom = crudo.startswith(b"\xef\xbb\xbf")
    texto = crudo.decode("utf-8-sig")
    lineas = texto.splitlines(keepends=True)
    if not lineas or lineas[0].strip() != "---":
        raise ErrorCurador("La nota no tiene frontmatter; no se modifica (use crear-nota para notas nuevas).")
    cierre = next((i for i in range(1, len(lineas)) if lineas[i].strip() in ("---", "...")), None)
    if cierre is None:
        raise ErrorCurador("Frontmatter sin cierre '---'; no se modifica.")
    fecha = fecha or dt.date.today().isoformat()
    _, previo = _edita_linea(lineas, 1, cierre, "estado", estado)
    cierre = next(i for i in range(1, len(lineas)) if lineas[i].strip() in ("---", "..."))
    _edita_linea(lineas, 1, cierre, "fecha_actualizacion", fecha)
    nuevo = "".join(lineas)
    datos, error, _ = parsear_frontmatter(nuevo)
    if error or datos is None or str(datos.get("estado")) != estado:
        raise ErrorCurador(f"La edición produciría un frontmatter inválido ({error}); no se escribió nada.")
    resultado = {"nota": rel, "estado_previo": previo, "estado_nuevo": estado, "fecha_actualizacion": fecha,
                 "simulacion": simular}
    if not simular:
        with open(destino, "wb") as f:                     # edición in situ, sin copias .bak en el vault
            f.write((b"\xef\xbb\xbf" if bom else b"") + nuevo.encode("utf-8"))
        registrar_bitacora(vault, AGENTE, f"marcar-estado `{rel}`: estado `{previo}` -> `{estado}` "
                                          f"(fecha_actualizacion {fecha}).")
    return resultado


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
def _salida(args: argparse.Namespace, datos: Any, texto: str) -> None:
    print(json.dumps(datos, ensure_ascii=False, indent=2, default=list) if args.json else texto)


def _vault(args: argparse.Namespace) -> Vault:
    raiz = Path(args.vault) if args.vault else rutas.VAULT
    if not raiz.is_dir():
        raise ErrorCurador(f"El vault no existe: {raiz}")
    return Vault(raiz)


def _una_nota(v: Vault, ref: str) -> str:
    c = v.localizar(ref)
    if not c:
        raise ErrorCurador(f"No se encontró la nota: {ref}")
    if len(c) > 1:
        raise ErrorCurador("Referencia ambigua, use la ruta completa: " + ", ".join(c))
    return c[0]


def cmd_auditar(a: argparse.Namespace) -> int:
    inf = auditar_vault(_vault(a))
    _salida(a, inf, formatear_auditoria(inf, a.max))
    return 1 if inf["errores"] or (a.estricto and inf["avisos"]) else 0


def datos_enlaces(v: Vault, rel: str) -> dict:
    n = v.notas[rel]
    sal = [{"destino": e["destino"] or "(ancla interna)", "resuelto": e["resuelto"], "embed": e["embed"]} for e in n["enlaces"]]
    return {"nota": rel, "salientes": sal, "entrantes": sorted(n["entrantes"])}


def cmd_enlaces(a: argparse.Namespace) -> int:
    v = _vault(a)
    d = datos_enlaces(v, _una_nota(v, a.nota))
    L = [f"Nota: {d['nota']}", f"\nSalientes ({len(d['salientes'])})"]
    L += [f"  - [[{s['destino']}]] -> {', '.join(s['resuelto']) if s['resuelto'] else 'ROTO'}" for s in d["salientes"]]
    L += [f"\nEntrantes ({len(d['entrantes'])})"] + [f"  - {e}" for e in d["entrantes"]]
    _salida(a, d, "\n".join(L))
    return 0


def cmd_backlinks(a: argparse.Namespace) -> int:
    v = _vault(a)
    if a.nota:
        rel = _una_nota(v, a.nota)
        ent = sorted(v.notas[rel]["entrantes"])
        _salida(a, {"nota": rel, "entrantes": ent}, f"Backlinks de {rel} ({len(ent)})\n" + "\n".join(f"  - {e}" for e in ent))
        return 0
    rank = sorted(((len(n["entrantes"]), r) for r, n in v.notas.items()), reverse=True)[: a.max]
    datos = [{"nota": r, "entrantes": k} for k, r in rank]
    _salida(a, datos, "Notas más enlazadas\n" + "\n".join(f"  {k:>4}  {r}" for k, r in rank))
    return 0


def cmd_crear_nota(a: argparse.Namespace) -> int:
    ruta = crear_nota(Path(a.vault) if a.vault else rutas.VAULT, a.ruta, a.tipo, a.fase, a.agente,
                      a.estado, a.titulo, a.texto or "")
    _salida(a, {"creada": str(ruta)}, f"Nota creada: {ruta}")
    return 0


def cmd_bitacora(a: argparse.Namespace) -> int:
    ruta = registrar_bitacora(Path(a.vault) if a.vault else rutas.VAULT, a.agente, a.texto)
    _salida(a, {"bitacora": str(ruta)}, f"Entrada añadida a {ruta}")
    return 0


def cmd_handoff(a: argparse.Namespace) -> int:
    if a.desde_json:
        registro = json.loads(Path(a.desde_json).read_text(encoding="utf-8"))
        tarea = a.tarea or registro.pop("tarea", "")
    else:
        registro = {"fecha": a.fecha or dt.date.today().isoformat(), "agente": a.agente, "fase": a.fase,
                    "estado": a.estado, "productos_generados": a.producto or [], "hallazgos_clave": a.hallazgo or [],
                    "pendientes_o_verificar": a.pendiente or [], "riesgos_o_incoherencias": a.riesgo or [],
                    "siguiente_accion_sugerida": a.siguiente}
        tarea = a.tarea
    if not tarea:
        raise ErrorCurador("Falta --tarea (nombre corto de la tarea para el archivo).")
    ruta = registrar_handoff(Path(a.vault) if a.vault else rutas.VAULT, registro, tarea)
    _salida(a, {"handoff": str(ruta), "palabras": contar_palabras(registro)}, f"Handoff creado: {ruta} ({contar_palabras(registro)} palabras)")
    return 0


def cmd_marcar_estado(a: argparse.Namespace) -> int:
    r = marcar_estado(Path(a.vault) if a.vault else rutas.VAULT, a.nota, a.estado, simular=a.simular)
    _salida(a, r, ("[SIMULACIÓN] " if r["simulacion"] else "") +
            f"{r['nota']}: estado {r['estado_previo']!r} -> {r['estado_nuevo']!r} ({r['fecha_actualizacion']})")
    return 0


def construir_parser() -> argparse.ArgumentParser:
    comun = argparse.ArgumentParser(add_help=False)
    comun.add_argument("--vault", help="Ruta del vault (por defecto SIVAC_VAULT o la canónica).")
    comun.add_argument("--json", action="store_true", help="Salida JSON para máquina.")
    p = argparse.ArgumentParser(prog="curador_cerebro", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("auditar", parents=[comun], help="Auditoría de solo lectura del vault.")
    s.add_argument("--max", type=int, default=15, help="Máximo de elementos listados por hallazgo.")
    s.add_argument("--estricto", action="store_true", help="Salida 1 también si hay solo avisos.")
    s.set_defaults(f=cmd_auditar)

    s = sub.add_parser("enlaces", parents=[comun], help="Enlaces entrantes/salientes de una nota.")
    s.add_argument("nota"); s.set_defaults(f=cmd_enlaces)

    s = sub.add_parser("backlinks", parents=[comun], help="Entrantes de una nota o ranking general.")
    s.add_argument("nota", nargs="?"); s.add_argument("--max", type=int, default=20); s.set_defaults(f=cmd_backlinks)

    s = sub.add_parser("crear-nota", parents=[comun], help="Crea una nota con frontmatter válido (no sobrescribe).")
    s.add_argument("--ruta", required=True, help="Ruta relativa al vault, con .md")
    s.add_argument("--tipo", required=True); s.add_argument("--fase", required=True)
    s.add_argument("--agente", required=True); s.add_argument("--estado", default="borrador")
    s.add_argument("--titulo", required=True); s.add_argument("--texto")
    s.set_defaults(f=cmd_crear_nota)

    s = sub.add_parser("registrar-bitacora", parents=[comun], help="Añade una entrada a la bitácora del agente.")
    s.add_argument("agente"); s.add_argument("texto"); s.set_defaults(f=cmd_bitacora)

    s = sub.add_parser("registrar-handoff", parents=[comun], help="Crea un handoff validado (<= 300 palabras).")
    s.add_argument("--desde-json", help="Archivo JSON con el registro completo (campos del esquema).")
    s.add_argument("--tarea", help="Nombre corto de la tarea (parte del nombre de archivo).")
    s.add_argument("--agente"); s.add_argument("--fase"); s.add_argument("--fecha")
    s.add_argument("--estado", choices=["completado", "parcial", "bloqueado"], default="completado")
    s.add_argument("--producto", action="append"); s.add_argument("--hallazgo", action="append")
    s.add_argument("--pendiente", action="append"); s.add_argument("--riesgo", action="append")
    s.add_argument("--siguiente", default="")
    s.set_defaults(f=cmd_handoff)

    s = sub.add_parser("marcar-estado", parents=[comun], help="Edita solo estado/fecha_actualizacion del frontmatter.")
    s.add_argument("nota"); s.add_argument("estado")
    s.add_argument("--simular", action="store_true", help="No escribe; muestra el cambio.")
    s.set_defaults(f=cmd_marcar_estado)
    return p


def main(argv: list[str] | None = None) -> int:
    seguridad.configurar_utf8()
    parser = construir_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        return args.f(args)
    except (ErrorCurador, seguridad.EscrituraProhibida) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except ValueError as e:                     # JSON de entrada malformado
        print(f"ERROR de entrada: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
