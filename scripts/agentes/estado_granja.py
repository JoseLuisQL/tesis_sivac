#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Estado de la granja (QG-0): comprobación integral del ecosistema.

Una sola orden para el Director General. Verifica y reporta OK / FALLA / AVISO en
diez secciones:

    1 entorno      venv, librerías, R, Tesseract, Word COM, Node, git
    2 zotero       servidor local (ping) y colección 4XAQ6D3D
    3 mcp          .mcp.json: variables de entorno (solo presencia) y npx
    4 agentes      frontmatter, skills existentes, 'Agent' solo en el director,
                   ingeniero-sivac de solo lectura
    5 agents_md    coherencia AGENTS.md vs .claude/agents/*.md
    6 hooks        scripts .cjs de settings.json existen y pasan node --check
    7 reglas       reglas (.claude/rules) y schemas JSON (Draft 2020-12) válidos
    8 seguridad    referencias/ sin cambios en git; datos/raw sin CSV sin MANIFEST
    9 salidas      entregables prematuros (.docx sin autorización registrada)
    10 indices_pdf índices de PDF existentes y vigentes (sha256)

Convención de autorización de entregables (sección 9): se examinan los .docx de
salidas/documentos y sus subcarpetas (recursivo). Un .docx se considera autorizado
solo si figura en una cláusula afirmativa (sin negación: "no", "sin", "pendiente",
"falta", "desautorizado", "rechazado", "false", "[ ]"...) de
salidas/documentos/AUTORIZACIONES.md|.txt|.json, o de una línea con la palabra
"autoriz" de 00_SISTEMA/ESTADO_TESIS.md del vault. Si hay una cláusula negativa
para el mismo archivo, prevalece la negativa (criterio conservador). Un archivo en
una subcarpeta debe citarse con su ruta relativa a salidas/documentos.

Nunca se imprimen valores de variables de entorno ni secretos.

Uso:
    python scripts/agentes/estado_granja.py              # tabla legible
    python scripts/agentes/estado_granja.py --json       # salida de máquina
    python scripts/agentes/estado_granja.py --sin-word   # omite Word COM
    python scripts/agentes/estado_granja.py --solo entorno,agentes

Códigos de salida: 0 sin FALLA, 1 hay FALLA, 2 uso incorrecto.
Las rutas base se pueden sobrescribir con SIVAC_ROOT / SIVAC_VAULT.
"""

from __future__ import annotations

import argparse
import importlib.metadata as md
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad  # noqa: E402

OK, FALLA, AVISO = "OK", "FALLA", "AVISO"

RSCRIPT = Path(r"C:/Users/jquis/AppData/Local/Programs/R/R-4.6.1/bin/Rscript.exe")
TESSERACT = Path(r"C:/Users/jquis/AppData/Local/Programs/Tesseract-OCR/tesseract.exe")
ZOTERO_URL = "http://127.0.0.1:23119"
SIN_PROXY = {"http": None, "https": None}

# (distribución pip, obligatoria)
LIBRERIAS = (
    "PyMuPDF", "pdfplumber", "python-docx", "lxml", "rapidfuzz", "pandas", "numpy",
    "scipy", "statsmodels", "pingouin", "requests", "habanero", "pytesseract",
    "pywin32", "pytest", "jsonschema", "PyYAML",
)
# Nombres que en el frontmatter de un agente son servidores MCP y no carpetas de skill.
NOMBRES_MCP = {"context7", "firecrawl", "ydc-server", "playwright", "zotero"}
HERRAMIENTAS_INGENIERO = {"Read", "Grep", "Glob"}
CAMPOS_AGENTE = ("name", "description", "tools", "skills", "squad")
REGLAS_ESPERADAS = (
    "01_seguridad.md", "02_metodologia_dec007.md",
    "03_estilo_academico_apa7.md", "04_protocolo_agentes.md",
)
EXT_DATOS = {
    ".csv", ".tsv", ".xlsx", ".xlsm", ".xls", ".ods", ".sav", ".zsav", ".dta",
    ".json", ".parquet", ".feather", ".rds", ".rdata", ".rda", ".pkl", ".pickle",
}


@dataclass
class Resultado:
    seccion: str
    nombre: str
    estado: str
    detalle: str = ""
    extra: dict = field(default_factory=dict)


@dataclass
class Contexto:
    raiz: Path
    vault: Path
    skills_globales: Path
    pdfs: Path
    indices: Path
    sin_word: bool = False

    @classmethod
    def por_defecto(cls, sin_word: bool = False) -> "Contexto":
        return cls(
            raiz=rutas.RAIZ, vault=rutas.VAULT,
            skills_globales=Path.home() / ".claude" / "skills",
            pdfs=rutas.PDFS_FUENTES, indices=rutas.INDICES_PDF, sin_word=sin_word,
        )


def _r(seccion: str, nombre: str, estado: str, detalle: str = "", **extra) -> Resultado:
    return Resultado(seccion, nombre, estado, detalle, extra)


def _ejecutar(cmd: list[str], timeout: int = 30) -> tuple[int, str]:
    """Ejecuta un comando y devuelve (código, salida combinada). Código -1 si no se pudo lanzar."""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           encoding="utf-8", errors="replace")
        return p.returncode, (p.stdout + p.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        return -1, f"{type(e).__name__}: {e}"


# --------------------------------------------------------------------------
# 1. Entorno
# --------------------------------------------------------------------------
def comprobar_venv(ctx: Contexto) -> list[Resultado]:
    py = ctx.raiz / ".venv" / "Scripts" / "python.exe"
    if not py.exists():
        py = ctx.raiz / ".venv" / "bin" / "python"
    if not py.exists():
        return [_r("entorno", "venv", FALLA, f"No existe .venv en {ctx.raiz}")]
    usa_venv = Path(sys.executable).resolve() == py.resolve()
    if usa_venv:
        return [_r("entorno", "venv", OK, f"{py} (intérprete activo)")]
    return [_r("entorno", "venv", AVISO,
               f"Existe {py}, pero esta corrida usa {sys.executable}")]


def comprobar_librerias() -> list[Resultado]:
    versiones, faltan = {}, []
    for dist in LIBRERIAS:
        try:
            versiones[dist] = md.version(dist)
        except md.PackageNotFoundError:
            faltan.append(dist)
    if faltan:
        return [_r("entorno", "librerías", FALLA, "Faltan: " + ", ".join(faltan),
                   versiones=versiones)]
    resumen = ", ".join(f"{k} {v}" for k, v in versiones.items())
    return [_r("entorno", "librerías", OK, resumen, versiones=versiones)]


def comprobar_r() -> list[Resultado]:
    exe = RSCRIPT if RSCRIPT.exists() else (Path(shutil.which("Rscript")) if shutil.which("Rscript") else None)
    if exe is None:
        return [_r("entorno", "R (Rscript)", FALLA, f"No se encontró {RSCRIPT} ni Rscript en PATH")]
    cod, salida = _ejecutar([str(exe), "--version"], timeout=30)
    if cod != 0:
        return [_r("entorno", "R (Rscript)", FALLA, f"{exe} no responde: {salida[:120]}")]
    return [_r("entorno", "R (Rscript)", OK, f"{salida.splitlines()[0] if salida else exe}")]


def comprobar_tesseract() -> list[Resultado]:
    exe = TESSERACT if TESSERACT.exists() else (Path(shutil.which("tesseract")) if shutil.which("tesseract") else None)
    if exe is None:
        return [_r("entorno", "Tesseract (OCR)", AVISO,
                   "OCR no disponible: las páginas sin capa de texto no se pueden citar")]
    cod, salida = _ejecutar([str(exe), "--version"], timeout=20)
    if cod != 0:
        return [_r("entorno", "Tesseract (OCR)", AVISO, f"{exe} no responde: {salida[:120]}")]
    return [_r("entorno", "Tesseract (OCR)", OK, salida.splitlines()[0] if salida else str(exe))]


def comprobar_word(sin_word: bool) -> list[Resultado]:
    if sin_word:
        return [_r("entorno", "Word COM", AVISO, "omitido (--sin-word)")]
    word = None
    try:
        import pythoncom
        import win32com.client
        pythoncom.CoInitialize()
        try:
            # DispatchEx crea SIEMPRE un proceso propio: Dispatch se adheriría a un
            # Word ya abierto por el usuario y el Quit() posterior lo cerraría.
            dispatch = getattr(win32com.client, "DispatchEx", None) or win32com.client.Dispatch
            word = dispatch("Word.Application")
            try:
                word.Visible = False
                word.DisplayAlerts = 0
            except Exception:
                pass
            return [_r("entorno", "Word COM", OK, f"Word {getattr(word, 'Version', '?')} disponible por COM")]
        finally:
            if word is not None:
                try:
                    word.Quit()
                except Exception:
                    pass
            pythoncom.CoUninitialize()
    except Exception as e:  # ImportError, com_error, etc.
        return [_r("entorno", "Word COM", AVISO, f"No disponible: {type(e).__name__}: {str(e)[:100]}")]


def comprobar_herramienta(nombre: str, exe: str) -> list[Resultado]:
    ruta = shutil.which(exe)
    if not ruta:
        return [_r("entorno", nombre, FALLA, f"'{exe}' no está en PATH")]
    cod, salida = _ejecutar([ruta, "--version"], timeout=20)
    if cod != 0:
        return [_r("entorno", nombre, FALLA, f"{ruta} falló: {salida[:100]}")]
    return [_r("entorno", nombre, OK, salida.splitlines()[0])]


def seccion_entorno(ctx: Contexto) -> list[Resultado]:
    return (comprobar_venv(ctx) + comprobar_librerias() + comprobar_r()
            + comprobar_tesseract() + comprobar_word(ctx.sin_word)
            + comprobar_herramienta("Node", "node") + comprobar_herramienta("git", "git"))


# --------------------------------------------------------------------------
# 2. Zotero
# --------------------------------------------------------------------------
def seccion_zotero(ctx: Contexto | None = None) -> list[Resultado]:
    salida: list[Resultado] = []
    try:
        resp = requests.get(f"{ZOTERO_URL}/connector/ping", timeout=5, proxies=SIN_PROXY)
    except requests.RequestException as e:
        motivo = f"Servidor Zotero inactivo ({type(e).__name__}); no se pueden registrar fuentes"
        return [_r("zotero", "ping /connector/ping", FALLA, motivo),
                _r("zotero", f"colección {rutas.ZOTERO_COLECCION}", FALLA, "no verificable sin servidor")]
    if resp.status_code != 200:
        salida.append(_r("zotero", "ping /connector/ping", FALLA, f"HTTP {resp.status_code}"))
    else:
        salida.append(_r("zotero", "ping /connector/ping", OK, "Zotero responde"))

    try:
        resp = requests.get(f"{ZOTERO_URL}/api/users/0/collections", timeout=10, proxies=SIN_PROXY,
                            params={"limit": 200}, headers={"Zotero-Allowed-Request": "1"})
        if resp.status_code != 200:
            raise ValueError(f"HTTP {resp.status_code}")
        claves = {c.get("key") for c in resp.json()}
    except (requests.RequestException, ValueError) as e:
        salida.append(_r("zotero", f"colección {rutas.ZOTERO_COLECCION}", FALLA,
                         f"No se pudo listar colecciones: {type(e).__name__}: {str(e)[:80]}"))
        return salida
    if rutas.ZOTERO_COLECCION in claves:
        salida.append(_r("zotero", f"colección {rutas.ZOTERO_COLECCION}", OK,
                         f"presente ({len(claves)} colecciones)"))
    else:
        salida.append(_r("zotero", f"colección {rutas.ZOTERO_COLECCION}", FALLA,
                         f"No figura entre las {len(claves)} colecciones devueltas"))
    return salida


# --------------------------------------------------------------------------
# 3. MCP
# --------------------------------------------------------------------------
_RE_VAR = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-[^}]*)?\}")


def _variables_referenciadas(obj) -> set[str]:
    if isinstance(obj, str):
        return set(_RE_VAR.findall(obj))
    if isinstance(obj, dict):
        return set().union(*(_variables_referenciadas(v) for v in obj.values())) if obj else set()
    if isinstance(obj, list):
        return set().union(*(_variables_referenciadas(v) for v in obj)) if obj else set()
    return set()


def _env_locales(raiz: Path) -> set[str]:
    """Nombres (solo nombres, nunca valores) definidos y no vacíos en el bloque env de settings*.json."""
    nombres: set[str] = set()
    for archivo in ("settings.json", "settings.local.json"):
        try:
            env = json.loads((raiz / ".claude" / archivo).read_text(encoding="utf-8")).get("env", {})
        except (OSError, ValueError):
            continue
        if isinstance(env, dict):
            nombres |= {k for k, v in env.items() if v}
    return nombres


def seccion_mcp(ctx: Contexto) -> list[Resultado]:
    ruta = ctx.raiz / ".mcp.json"
    try:
        cfg = json.loads(ruta.read_text(encoding="utf-8"))
    except OSError:
        return [_r("mcp", ".mcp.json", FALLA, f"No existe {ruta}")]
    except ValueError as e:
        return [_r("mcp", ".mcp.json", FALLA, f"JSON inválido: {e}")]
    servidores = cfg.get("mcpServers", {})
    if not servidores:
        return [_r("mcp", ".mcp.json", FALLA, "Sin mcpServers")]

    salida = [_r("mcp", ".mcp.json", OK, "servidores: " + ", ".join(servidores))]
    locales = _env_locales(ctx.raiz)
    for nombre, srv in servidores.items():
        faltan = sorted(v for v in _variables_referenciadas(srv) if not os.environ.get(v) and v not in locales)
        if faltan:
            salida.append(_r("mcp", f"{nombre}: variables", FALLA, "Sin definir: " + ", ".join(faltan)))
        else:
            n = len(_variables_referenciadas(srv))
            salida.append(_r("mcp", f"{nombre}: variables", OK,
                             f"{n} variable(s) presente(s) (valores no mostrados)" if n else "sin variables"))
        cmd = srv.get("command")
        if cmd:
            if shutil.which(cmd):
                salida.append(_r("mcp", f"{nombre}: ejecutable {cmd}", OK, "encontrado en PATH"))
            else:
                salida.append(_r("mcp", f"{nombre}: ejecutable {cmd}", FALLA, f"'{cmd}' no está en PATH"))
    return salida


# --------------------------------------------------------------------------
# 4. Agentes
# --------------------------------------------------------------------------
_RE_FRONTMATTER = re.compile(r"\A\ufeff?---\r?\n(.*?)\r?\n---", re.S)


def parsear_frontmatter(ruta: Path) -> dict:
    """Devuelve el frontmatter YAML o lanza ValueError con el motivo."""
    import yaml
    m = _RE_FRONTMATTER.match(ruta.read_text(encoding="utf-8"))
    if not m:
        raise ValueError("sin frontmatter YAML")
    try:
        datos = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        raise ValueError(f"YAML inválido: {str(e)[:80]}")
    if not isinstance(datos, dict):
        raise ValueError("frontmatter no es un mapa")
    return datos


def como_lista(valor) -> list[str]:
    """Normaliza un campo de frontmatter (lista YAML o cadena separada por comas) a lista de str."""
    if valor is None:
        return []
    if isinstance(valor, str):
        return [x.strip() for x in valor.split(",") if x.strip()]
    if isinstance(valor, (list, tuple, set)):
        return [str(x).strip() for x in valor if str(x).strip()]
    return [str(valor).strip()]


def cargar_agentes(raiz: Path) -> tuple[dict[str, dict], list[Resultado]]:
    agentes, problemas = {}, []
    carpeta = raiz / ".claude" / "agents"
    for ruta in sorted(carpeta.glob("*.md")):
        try:
            agentes[ruta.stem] = parsear_frontmatter(ruta)
        except ValueError as e:
            problemas.append(_r("agentes", ruta.name, FALLA, str(e)))
    return agentes, problemas


def skill_existe(skill: str, ctx: Contexto) -> bool:
    return any((base / skill / "SKILL.md").is_file()
               for base in (ctx.raiz / ".claude" / "skills", ctx.skills_globales))


def seccion_agentes(ctx: Contexto) -> list[Resultado]:
    agentes, salida = cargar_agentes(ctx.raiz)
    if not agentes and not salida:
        return [_r("agentes", ".claude/agents", FALLA, "No hay agentes")]

    faltan_campos, nombre_distinto, skills_falla, skills_mcp = [], [], [], set()
    con_agent = []
    for stem, fm in agentes.items():
        ausentes = [c for c in CAMPOS_AGENTE if not fm.get(c)]
        if ausentes:
            faltan_campos.append(f"{stem}({','.join(ausentes)})")
        if fm.get("name") and fm["name"] != stem:
            nombre_distinto.append(f"{stem}≠{fm['name']}")
        herramientas = como_lista(fm.get("tools"))
        if "Agent" in herramientas and stem != "director-general":
            con_agent.append(stem)
        for sk in como_lista(fm.get("skills")):
            if skill_existe(sk, ctx):
                continue
            if sk in NOMBRES_MCP:
                skills_mcp.add(sk)
            else:
                skills_falla.append(f"{stem}→{sk}")

    salida.append(_r("agentes", "frontmatter (campos)", FALLA if faltan_campos else OK,
                     "Incompletos: " + "; ".join(faltan_campos) if faltan_campos
                     else f"{len(agentes)} agentes con {', '.join(CAMPOS_AGENTE)}"))
    salida.append(_r("agentes", "name == archivo", FALLA if nombre_distinto else OK,
                     "; ".join(nombre_distinto) if nombre_distinto else "coinciden"))
    salida.append(_r("agentes", "skills existentes", FALLA if skills_falla else OK,
                     "No existen: " + "; ".join(skills_falla) if skills_falla
                     else "todas las skills referenciadas existen"))
    if skills_mcp:
        salida.append(_r("agentes", "skills que son MCP", AVISO,
                         f"{', '.join(sorted(skills_mcp))}: listados como skill pero son servidores MCP, no hay SKILL.md"))
    salida.append(_r("agentes", "'Agent' solo en director-general", FALLA if con_agent else OK,
                     "Lo listan: " + ", ".join(con_agent) if con_agent else "solo el director puede delegar"))

    ing = agentes.get("ingeniero-sivac")
    if ing is None:
        salida.append(_r("agentes", "ingeniero-sivac solo lectura", FALLA, "agente no encontrado"))
    else:
        tools = set(como_lista(ing.get("tools")))
        if tools == HERRAMIENTAS_INGENIERO:
            salida.append(_r("agentes", "ingeniero-sivac solo lectura", OK, "tools = Read, Grep, Glob"))
        else:
            salida.append(_r("agentes", "ingeniero-sivac solo lectura", FALLA,
                             f"tools = {sorted(tools)}; se exige exactamente {sorted(HERRAMIENTAS_INGENIERO)}"))
    return salida


# --------------------------------------------------------------------------
# 5. AGENTS.md vs agentes reales
# --------------------------------------------------------------------------
_RE_FILA_AGENTE = re.compile(r"^\|[^|]*\|\s*`([a-z][a-z0-9-]+)`\s*\|", re.M)


def seccion_agents_md(ctx: Contexto) -> list[Resultado]:
    ruta = ctx.raiz / "AGENTS.md"
    if not ruta.is_file():
        return [_r("agents_md", "AGENTS.md", FALLA, "No existe AGENTS.md")]
    en_md = set(_RE_FILA_AGENTE.findall(ruta.read_text(encoding="utf-8")))
    reales = {p.stem for p in (ctx.raiz / ".claude" / "agents").glob("*.md")}
    solo_md, solo_real = sorted(en_md - reales), sorted(reales - en_md)
    if solo_md or solo_real:
        partes = []
        if solo_md:
            partes.append("en AGENTS.md sin archivo: " + ", ".join(solo_md))
        if solo_real:
            partes.append("archivo sin fila en AGENTS.md: " + ", ".join(solo_real))
        return [_r("agents_md", "AGENTS.md vs agentes", FALLA, "; ".join(partes))]
    return [_r("agents_md", "AGENTS.md vs agentes", OK, f"{len(reales)} agentes coinciden")]


# --------------------------------------------------------------------------
# 6. Hooks
# --------------------------------------------------------------------------
_RE_CJS_COMILLAS = re.compile(r"\"([^\"]+\.cjs)\"|'([^']+\.cjs)'")
# Ruta sin comillas (admite espacios): opcionalmente precedida por "node [--opciones]".
_RE_CJS_LIBRE = re.compile(
    r"(?:^|[\s;&|])(?:node(?:\.exe)?\s+(?:-\S+\s+)*)?"
    r"([^\s\"'|&;<>][^\"'|&;<>]*?\.cjs)(?=\s|$|[\"'|&;<>])")


def extraer_scripts_cjs(cmd: str) -> list[str]:
    """Rutas .cjs citadas en un comando de hook (con comillas, o sin ellas aunque tengan espacios)."""
    encontradas = [a or b for a, b in _RE_CJS_COMILLAS.findall(cmd)]
    resto = _RE_CJS_COMILLAS.sub(" ", cmd)
    encontradas += [m.group(1).strip() for m in _RE_CJS_LIBRE.finditer(resto)]
    return encontradas


def _comandos_hooks(cfg: dict) -> list[tuple[str, str]]:
    """Pares (evento, comando) declarados en settings.json."""
    cmds = []
    for evento, grupos in (cfg.get("hooks") or {}).items():
        for grupo in grupos:
            for h in grupo.get("hooks", []):
                if h.get("command"):
                    cmds.append((evento, h["command"]))
    return cmds


def seccion_hooks(ctx: Contexto) -> list[Resultado]:
    ruta = ctx.raiz / ".claude" / "settings.json"
    try:
        cfg = json.loads(ruta.read_text(encoding="utf-8"))
    except OSError:
        return [_r("hooks", "settings.json", FALLA, f"No existe {ruta}")]
    except ValueError as e:
        return [_r("hooks", "settings.json", FALLA, f"JSON inválido: {e}")]
    comandos = _comandos_hooks(cfg)
    if not comandos:
        return [_r("hooks", "settings.json", FALLA, "No declara hooks")]

    salida, node = [], shutil.which("node")
    for evento, cmd in comandos:
        for crudo in extraer_scripts_cjs(cmd):
            crudo = (crudo.replace("${CLAUDE_PROJECT_DIR}", str(ctx.raiz))
                     .replace("$CLAUDE_PROJECT_DIR", str(ctx.raiz)))
            script = Path(crudo) if Path(crudo).is_absolute() else ctx.raiz / crudo
            etiqueta = f"{evento}: {script.name}"
            if not script.is_file():
                salida.append(_r("hooks", etiqueta, FALLA, f"No existe {script}"))
                continue
            if not node:
                salida.append(_r("hooks", etiqueta, FALLA, "node no está en PATH para node --check"))
                continue
            cod, msg = _ejecutar([node, "--check", str(script)], timeout=20)
            salida.append(_r("hooks", etiqueta, OK if cod == 0 else FALLA,
                             "existe y node --check correcto" if cod == 0 else f"node --check: {msg[:120]}"))
    if not salida:
        salida.append(_r("hooks", "settings.json", FALLA, "Los hooks no referencian scripts .cjs"))
    return salida


# --------------------------------------------------------------------------
# 7. Reglas y schemas
# --------------------------------------------------------------------------
def seccion_reglas_schemas(ctx: Contexto) -> list[Resultado]:
    salida = []
    carpeta = ctx.raiz / ".claude" / "rules"
    ausentes = [n for n in REGLAS_ESPERADAS
                if not (carpeta / n).is_file() or (carpeta / n).stat().st_size == 0]
    salida.append(_r("reglas", "reglas canónicas", FALLA if ausentes else OK,
                     "Faltan o vacías: " + ", ".join(ausentes) if ausentes
                     else f"{len(REGLAS_ESPERADAS)} reglas presentes"))

    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
    archivos = sorted((ctx.raiz / ".claude" / "schemas").glob("*.json"))
    if not archivos:
        return salida + [_r("reglas", "schemas JSON", FALLA, "No hay schemas en .claude/schemas")]
    for arch in archivos:
        try:
            Draft202012Validator.check_schema(json.loads(arch.read_text(encoding="utf-8")))
            salida.append(_r("reglas", f"schema {arch.name}", OK, "válido (Draft 2020-12)"))
        except ValueError as e:
            salida.append(_r("reglas", f"schema {arch.name}", FALLA, f"JSON inválido: {str(e)[:100]}"))
        except SchemaError as e:
            salida.append(_r("reglas", f"schema {arch.name}", FALLA, f"schema inválido: {e.message[:100]}"))
    return salida


# --------------------------------------------------------------------------
# 8. Seguridad
# --------------------------------------------------------------------------
def seccion_seguridad(ctx: Contexto) -> list[Resultado]:
    salida = []
    cod, msg = _ejecutar(["git", "-C", str(ctx.raiz), "status", "--porcelain", "--", "referencias"], timeout=30)
    if cod != 0:
        salida.append(_r("seguridad", "referencias/ inmutable", AVISO,
                         f"No se pudo consultar git ({msg[:80]}); inmutabilidad no verificada"))
    else:
        lineas = [ln for ln in msg.splitlines() if ln.strip()]
        modificadas = [ln for ln in lineas if not ln.startswith("??")]
        sin_versionar = [ln for ln in lineas if ln.startswith("??")]
        if modificadas:
            salida.append(_r("seguridad", "referencias/ inmutable", FALLA,
                             f"{len(modificadas)} cambio(s) respecto a git: " + "; ".join(m.strip() for m in modificadas[:5])))
        elif sin_versionar:
            salida.append(_r("seguridad", "referencias/ inmutable", AVISO,
                             "referencias/ sin versionar en git: no se puede demostrar que no fue modificada"))
        else:
            salida.append(_r("seguridad", "referencias/ inmutable", OK, "sin cambios respecto a git"))

    raw = ctx.raiz / "datos" / "raw"
    todos = [p for p in raw.rglob("*") if p.is_file()] if raw.is_dir() else []
    manifiestos = [p for p in todos if p.name.upper().startswith("MANIFEST")]
    datos = [p for p in todos if p.suffix.lower() in EXT_DATOS and p not in manifiestos]
    if not datos:
        salida.append(_r("seguridad", "datos/raw", OK,
                         "sin archivos de datos con extensión reconocida (csv, tsv, xlsx, sav, json, "
                         "parquet, dta...); análisis inferencial BLOQUEADO"))
    elif not manifiestos:
        salida.append(_r("seguridad", "datos/raw", AVISO,
                         "CRÍTICO: hay datos sin MANIFEST (procedencia no documentada): "
                         + ", ".join(p.name for p in datos[:5])))
    else:
        texto = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in manifiestos)
        sin_listar = [p.name for p in datos if p.name not in texto]
        if sin_listar:
            salida.append(_r("seguridad", "datos/raw", AVISO,
                             "CRÍTICO: datos no listados en el MANIFEST: " + ", ".join(sin_listar[:5])))
        else:
            salida.append(_r("seguridad", "datos/raw", OK, f"{len(datos)} archivo(s) listados en MANIFEST"))
    return salida


# --------------------------------------------------------------------------
# 9. Salidas
# --------------------------------------------------------------------------
_RE_NEGACION = re.compile(
    r"\b(?:no|not|sin|nunca|jam[aá]s|pendientes?|faltan?|falta|negad[oa]s?|denegad[oa]s?|"
    r"rechazad[oa]s?|revocad[oa]s?|desautoriz\w*|false|falso)\b|\[\s\]|[❌✗✘]",
    re.I)


def _clausulas(texto: str) -> list[str]:
    """Divide el texto en cláusulas (líneas, subdivididas por ';') para evaluar la polaridad por separado."""
    return [c.strip() for ln in texto.splitlines() for c in ln.split(";") if c.strip()]


def _clausulas_autorizacion(ctx: Contexto) -> list[tuple[str, bool]]:
    """Cláusulas candidatas (texto, exige_palabra_autoriz) de AUTORIZACIONES.* y ESTADO_TESIS.md."""
    salida: list[tuple[str, bool]] = []
    docs = ctx.raiz / "salidas" / "documentos"
    for ruta in sorted(docs.glob("AUTORIZACIONES.*")) if docs.is_dir() else []:
        texto = ruta.read_text(encoding="utf-8", errors="replace")
        if ruta.suffix.lower() == ".json":
            try:
                datos = json.loads(texto)
            except ValueError:
                datos = None
            if isinstance(datos, dict):  # {"archivo.docx": true|false|"texto"}
                for k, v in datos.items():
                    afirmativo = v is True or (isinstance(v, str) and v.strip() != "")
                    salida.append((f"{k}: {v if isinstance(v, str) and afirmativo else ('autorizado' if afirmativo else 'no autorizado')}", False))
                continue
            if isinstance(datos, list):  # ["archivo.docx", ...] = lista de autorizados
                salida += [(str(x), False) for x in datos]
                continue
        salida += [(c, False) for c in _clausulas(texto)]
    estado = ctx.vault / "00_SISTEMA" / "ESTADO_TESIS.md"
    if estado.is_file():
        texto = estado.read_text(encoding="utf-8", errors="replace")
        salida += [(c, True) for c in _clausulas(texto) if "autoriz" in c.lower()]
    return salida


def estado_autorizacion(rel: str, clausulas: list[tuple[str, bool]]) -> str:
    """'autorizado' | 'negado' | 'sin_registro' para un .docx (ruta relativa a salidas/documentos).

    Una cláusula afirmativa autoriza; una negativa (ver _RE_NEGACION) niega y prevalece.
    El nombre del archivo se retira de la cláusula antes de buscar negaciones, para que
    un nombre como 'sin_titulo.docx' no se interprete como negación.
    """
    candidatos = sorted({rel, f"documentos/{rel}", f"salidas/documentos/{rel}"}, key=len, reverse=True)
    patron = re.compile("|".join(
        r"(?<![\w.\-/])" + re.escape(c) + r"(?![\w\-]|\.\w)" for c in candidatos), re.I)
    positivo = negativo = False
    for texto, exige_autoriz in clausulas:
        texto = texto.replace("\\", "/")
        if not patron.search(texto):
            continue
        sin_nombre = patron.sub(" ", texto)
        if _RE_NEGACION.search(sin_nombre):
            negativo = True
        elif not exige_autoriz or "autoriz" in texto.lower():
            positivo = True
    return "negado" if negativo else ("autorizado" if positivo else "sin_registro")


def seccion_salidas(ctx: Contexto) -> list[Resultado]:
    base = ctx.raiz / "salidas"
    if not base.is_dir():
        return [_r("salidas", "salidas/", FALLA, f"No existe {base}")]
    archivos = sorted(p for p in base.rglob("*") if p.is_file())
    conteo: dict[str, int] = {}
    for p in archivos:
        clave = p.relative_to(base).parts[0] if len(p.relative_to(base).parts) > 1 else "(raíz)"
        conteo[clave] = conteo.get(clave, 0) + 1
    listado = ", ".join(f"{k}: {v}" for k, v in sorted(conteo.items())) or "vacía"
    salida = [_r("salidas", "contenido de salidas/", OK, listado,
                 archivos=[str(p.relative_to(ctx.raiz)).replace("\\", "/") for p in archivos])]

    carpeta_docs = base / "documentos"
    docx = sorted(p for p in carpeta_docs.rglob("*.docx")
                  if p.is_file() and not p.name.startswith("~$")) if carpeta_docs.is_dir() else []
    clausulas = _clausulas_autorizacion(ctx)
    sin_registro, negados = [], []
    for p in docx:
        rel = p.relative_to(carpeta_docs).as_posix()
        veredicto = estado_autorizacion(rel, clausulas)
        if veredicto == "negado":
            negados.append(rel)
        elif veredicto == "sin_registro":
            sin_registro.append(rel)
    if sin_registro or negados:
        partes = []
        if negados:
            partes.append("Autorización NEGADA o pendiente según el registro: " + ", ".join(negados))
        if sin_registro:
            partes.append("Sin autorización registrada del tesista: " + ", ".join(sin_registro))
        salida.append(_r("salidas", "entregables .docx", AVISO, "; ".join(partes),
                         negados=negados, sin_registro=sin_registro))
    else:
        salida.append(_r("salidas", "entregables .docx", OK,
                         f"{len(docx)} .docx, todos autorizados" if docx else "sin .docx en salidas/documentos"))
    return salida


# --------------------------------------------------------------------------
# 10. Índices de PDF
# --------------------------------------------------------------------------
def seccion_indices(ctx: Contexto) -> list[Resultado]:
    from scripts.fuentes import ingesta_pdf
    if not ctx.pdfs.is_dir():
        return [_r("indices_pdf", "PDFs de fuentes", FALLA, f"No existe {ctx.pdfs}")]
    pdfs = sorted(ctx.pdfs.glob("*.pdf"))
    if not pdfs:
        return [_r("indices_pdf", "PDFs de fuentes", AVISO, "Sin PDFs en la carpeta de fuentes")]
    faltan, obsoletos, dañados = [], [], []
    for pdf in pdfs:
        destino = ingesta_pdf.ruta_indice(pdf, ctx.indices)
        if not destino.is_file():
            faltan.append(pdf.name)
            continue
        try:
            idx = json.loads(destino.read_text(encoding="utf-8"))
            if not isinstance(idx, dict) or not isinstance(idx.get("fuente"), dict):
                raise ValueError("estructura de índice inesperada")
            vigente = (idx.get("version_indice") == ingesta_pdf.VERSION_INDICE
                       and idx["fuente"].get("sha256") == seguridad.sha256_archivo(pdf))
        except (ValueError, KeyError, TypeError, AttributeError, OSError):
            dañados.append(pdf.name)
            continue
        if not vigente:
            obsoletos.append(pdf.name)
    problemas = []
    if faltan:
        problemas.append(f"{len(faltan)} sin índice ({', '.join(faltan[:3])}…)" if len(faltan) > 3
                         else f"sin índice: {', '.join(faltan)}")
    if obsoletos:
        problemas.append(f"{len(obsoletos)} obsoleto(s) (hash o versión): {', '.join(obsoletos[:3])}")
    if dañados:
        problemas.append(f"ilegibles: {', '.join(dañados[:3])}")
    if problemas:
        return [_r("indices_pdf", "índices vigentes", FALLA, "; ".join(problemas) +
                   " → regenerar con scripts/fuentes/ingesta_pdf.py --todos",
                   total=len(pdfs))]
    return [_r("indices_pdf", "índices vigentes", OK, f"{len(pdfs)}/{len(pdfs)} PDFs con índice vigente (sha256)",
               total=len(pdfs))]


# --------------------------------------------------------------------------
# Orquestación y CLI
# --------------------------------------------------------------------------
SECCIONES = {
    "entorno": seccion_entorno,
    "zotero": seccion_zotero,
    "mcp": seccion_mcp,
    "agentes": seccion_agentes,
    "agents_md": seccion_agents_md,
    "hooks": seccion_hooks,
    "reglas": seccion_reglas_schemas,
    "seguridad": seccion_seguridad,
    "salidas": seccion_salidas,
    "indices_pdf": seccion_indices,
}


def ejecutar(ctx: Contexto, solo: list[str] | None = None) -> list[Resultado]:
    resultados: list[Resultado] = []
    for nombre, fn in SECCIONES.items():
        if solo and nombre not in solo:
            continue
        try:
            resultados += fn(ctx)
        except Exception as e:  # una sección rota no debe ocultar las demás
            resultados.append(_r(nombre, "error interno", FALLA, f"{type(e).__name__}: {str(e)[:120]}"))
    return resultados


def resumen(resultados: list[Resultado]) -> dict[str, int]:
    return {e: sum(1 for r in resultados if r.estado == e) for e in (OK, AVISO, FALLA)}


def formatear_tabla(resultados: list[Resultado]) -> str:
    ancho = max((len(r.nombre) for r in resultados), default=10)
    lineas, seccion = [], None
    for r in resultados:
        if r.seccion != seccion:
            seccion = r.seccion
            lineas.append(f"\n[{seccion}]")
        lineas.append(f"  {r.estado:<5} {r.nombre:<{ancho}}  {r.detalle}")
    res = resumen(resultados)
    lineas.append(f"\nResumen: {res[OK]} OK, {res[AVISO]} AVISO, {res[FALLA]} FALLA")
    return "\n".join(lineas).lstrip("\n")


def main(argv: list[str] | None = None) -> int:
    seguridad.configurar_utf8()
    ap = argparse.ArgumentParser(description="Estado de la granja de agentes (QG-0).")
    ap.add_argument("--json", action="store_true", help="salida JSON para máquina")
    ap.add_argument("--sin-word", action="store_true", help="omite la prueba de Word COM")
    ap.add_argument("--solo", help="secciones separadas por coma: " + ",".join(SECCIONES))
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code not in (0, None) else 0
    solo = [s.strip() for s in args.solo.split(",")] if args.solo else None
    if solo and (desconocidas := [s for s in solo if s not in SECCIONES]):
        print(f"Secciones desconocidas: {', '.join(desconocidas)}", file=sys.stderr)
        return 2

    resultados = ejecutar(Contexto.por_defecto(sin_word=args.sin_word), solo)
    res = resumen(resultados)
    if args.json:
        print(json.dumps({"resumen": res, "ok": res[FALLA] == 0,
                          "resultados": [asdict(r) for r in resultados]}, ensure_ascii=False, indent=1))
    else:
        print(formatear_tabla(resultados))
    return 1 if res[FALLA] else 0


if __name__ == "__main__":
    sys.exit(main())
