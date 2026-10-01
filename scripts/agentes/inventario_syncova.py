#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Inventario de SOLO LECTURA del código real de SIVAC (syncova).

Garantiza la trazabilidad 1:1 código-tesis de la sección 3.3 (Extreme Programming)
produciendo un inventario reproducible y fijado a un commit:

  * stack (package.json: dependencias y scripts npm, versiones DECLARADAS),
  * estructura de carpetas (niveles 1 y 2),
  * esquema Prisma (modelos, campos, relaciones, enums),
  * endpoints Express por análisis estático (método, ruta completa, archivo:línea,
    middlewares y autenticación detectada),
  * rutas de React Router y el componente de página asociado,
  * pruebas (archivos *.test.* / *.spec.*), variables de entorno (SOLO nombres),
    migraciones y commit documentado.

Garantías de seguridad:
  * Este módulo NUNCA escribe en el repositorio inspeccionado: solo abre archivos en
    modo lectura. La única escritura (opcional, de informes) ocurre fuera de él, en
    `escritura_segura.py`, y rechaza destinos dentro del repositorio inspeccionado.
  * No lee node_modules, .git (salvo HEAD/refs/packed-refs), dist, build, coverage ni
    secretos (.env*, *.pem, *.key, credenciales): se omiten por nombre, sin abrirlos.
  * Análisis estático con expresiones regulares: lo que no puede determinarse queda
    como None / "[VERIFICAR: motivo]"; nunca se infiere.

Uso:
    python scripts/agentes/inventario_syncova.py inventario [--raiz RUTA] [--json]
    python scripts/agentes/inventario_syncova.py inventario --guardar
    python scripts/agentes/inventario_syncova.py trazar HU-05 vale [--json]

Códigos de salida: 0 correcto, 1 hallazgos/fallos, 2 uso incorrecto.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad  # noqa: E402

VERSION_INVENTARIO = 1
MAX_BYTES_ARCHIVO = 2_000_000

# --------------------------------------------------------------------------- exclusiones
DIRS_EXCLUIDOS = {
    "node_modules", ".git", "dist", "build", "coverage", ".next", ".cache", ".vite",
    ".turbo", "__pycache__", "test-results", "playwright-report", ".playwright-cli",
    "output", "uploads", ".claude", ".agents", ".factory", ".idea", ".vscode",
}
_RE_SECRETO = re.compile(
    r"""^(
        \.env($|\..*)                      # .env, .env.local, .env.example ...
      | .*\.(pem|key|p12|pfx|jks|keystore|ppk)$
      | id_(rsa|dsa|ecdsa|ed25519)(\..*)?$
      | .*(credential|secret)s?.*\.(json|ya?ml|txt|ini|properties|env|xml|toml)$
      | service-account.*\.json$
    )""",
    re.I | re.X,
)
EXT_CODIGO = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}
EXT_LEIBLES = EXT_CODIGO | {".prisma"}
EXT_TRAZA_EXTRA = {".md"}
_RE_PRUEBA = re.compile(r"\.(test|spec)\.[A-Za-z0-9]+$")


def es_secreto(nombre: str) -> bool:
    """True si el nombre de archivo corresponde a un secreto que no debe leerse."""
    return bool(_RE_SECRETO.match(nombre))


def _leer_texto(ruta: Path) -> str:
    """ÚNICA función de lectura del módulo: modo 'r', rechaza secretos y archivos enormes."""
    if es_secreto(ruta.name):
        raise PermissionError(f"Lectura de secreto denegada: {ruta.name}")
    try:
        if ruta.stat().st_size > MAX_BYTES_ARCHIVO:
            return ""
        with open(ruta, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


# --------------------------------------------------------------------------- recorrido
class Arbol:
    """Listado de archivos (rutas POSIX relativas) sin excluidos ni secretos."""

    def __init__(self, raiz: Path):
        self.raiz = raiz
        self.archivos: list[str] = []
        self.dirs_excluidos: Counter = Counter()
        self.secretos_omitidos: list[str] = []
        self.enlaces_omitidos: list[str] = []
        self._cache: dict[str, str] = {}
        self._recorrer()

    def _recorrer(self) -> None:
        raiz_real = self.raiz.resolve(strict=False)
        for actual, dirs, files in os.walk(self.raiz):
            rel_dir = Path(actual).relative_to(self.raiz)
            podar = [d for d in dirs if d in DIRS_EXCLUIDOS or d.endswith(".egg-info")]
            for d in podar:
                self.dirs_excluidos[d] += 1
            dirs[:] = sorted(d for d in dirs if d not in podar)
            for nombre in sorted(files):
                rel = (rel_dir / nombre).as_posix()
                if es_secreto(nombre):
                    self.secretos_omitidos.append(rel)
                elif not self._dentro_del_repo(self.raiz / rel, raiz_real):
                    self.enlaces_omitidos.append(rel)  # enlace simbólico hacia fuera del repositorio
                else:
                    self.archivos.append(rel)

    @staticmethod
    def _dentro_del_repo(ruta: Path, raiz_real: Path) -> bool:
        """False si el archivo es un enlace cuyo destino real cae fuera del repositorio o es secreto."""
        try:
            destino = ruta.resolve(strict=True)
        except OSError:
            return False
        if es_secreto(destino.name):
            return False
        try:
            destino.relative_to(raiz_real)
        except ValueError:
            return False
        return True

    def texto(self, rel: str) -> str:
        if rel not in self._cache:
            self._cache[rel] = _leer_texto(self.raiz / rel)
        return self._cache[rel]

    def con_ext(self, exts: set[str]) -> list[str]:
        return [a for a in self.archivos if PurePosixPath(a).suffix.lower() in exts]


# --------------------------------------------------------------------------- utilidades de texto
def quitar_comentarios(src: str) -> str:
    """Sustituye comentarios JS/TS por espacios conservando saltos de línea y posiciones."""
    out: list[str] = []
    i, n, estado = 0, len(src), None
    while i < n:
        c = src[i]
        if estado is None:
            d = src[i:i + 2]
            if d == "//":
                j = src.find("\n", i)
                j = n if j < 0 else j
                out.append(" " * (j - i))
                i = j
                continue
            if d == "/*":
                j = src.find("*/", i + 2)
                j = n if j < 0 else j + 2
                out.append(re.sub(r"[^\n]", " ", src[i:j]))
                i = j
                continue
            if c in "'\"`":
                estado = c
            out.append(c)
            i += 1
        else:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(src[i + 1])
                i += 2
                continue
            if c == estado or (estado != "`" and c == "\n"):
                estado = None
            i += 1
    return "".join(out)


def extraer_args(t: str, i_abre: int):
    """Argumentos de nivel superior de la llamada cuyo '(' está en t[i_abre].

    Devuelve ([(offset, texto)], índice_del_paréntesis_de_cierre) o (None, len) si no cierra.
    """
    prof, ini, i, n, estado = 0, i_abre + 1, i_abre, len(t), None
    args: list[tuple[int, str]] = []
    while i < n:
        c = t[i]
        if estado:
            if c == "\\":
                i += 2
                continue
            if c == estado or (estado != "`" and c == "\n"):
                estado = None
        else:
            if c in "'\"`":
                estado = c
            elif c in "([{":
                prof += 1
            elif c in ")]}":
                prof -= 1
                if prof == 0:
                    if t[ini:i].strip():
                        args.append((ini, t[ini:i]))
                    return args, i
            elif c == "," and prof == 1:
                args.append((ini, t[ini:i]))
                ini = i + 1
        i += 1
    return None, n


def _linea(t: str, pos: int) -> int:
    return t.count("\n", 0, pos) + 1


def _compacta(s: str, limite: int = 90) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= limite else s[: limite - 1] + "…"


def _literal(arg: str) -> str | None:
    m = re.fullmatch(r"\s*(['\"`])((?:(?!\1).)*)\1\s*", arg, re.S)
    if m and "${" not in m.group(2):
        return m.group(2)
    return None


def _normalizar(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


# --------------------------------------------------------------------------- git (solo lectura)
def info_git(raiz: Path) -> dict:
    """Commit documentado. Usa 'git rev-parse HEAD' (lectura) y, si falla, lee HEAD/refs."""
    info = {"commit": None, "formato_hash": None, "rama": None, "fecha_commit": None,
            "asunto": None, "fuente": None, "advertencias": []}
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")

    def _git(*args: str) -> str | None:
        try:
            r = subprocess.run(["git", "-C", str(raiz), *args], capture_output=True,
                               text=True, timeout=20, env=env, encoding="utf-8", errors="replace")
        except (OSError, subprocess.SubprocessError):
            return None
        return r.stdout.strip() if r.returncode == 0 else None

    manual = _commit_manual(raiz)
    # 'git -C <dir>' sube hasta el .git ancestro: solo se acepta si la raíz ES la raíz del repo.
    top = _git("rev-parse", "--show-toplevel")
    es_raiz_repo = bool(top) and os.path.normcase(os.path.realpath(top)) == os.path.normcase(os.path.realpath(raiz))
    via_git = _git("rev-parse", "HEAD") if es_raiz_repo else None
    if top and not es_raiz_repo:
        info["advertencias"].append(
            f"[VERIFICAR: {raiz} es un subdirectorio del repositorio git {top}; "
            "el commit de ese repositorio no se atribuye a esta raíz]")
    if via_git and re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", via_git):
        info["commit"], info["fuente"] = via_git, "git rev-parse HEAD"
        info["rama"] = _git("rev-parse", "--abbrev-ref", "HEAD")
        meta = _git("log", "-1", "--format=%cI%x1f%s")
        if meta and "\x1f" in meta:
            info["fecha_commit"], info["asunto"] = meta.split("\x1f", 1)
        if manual["commit"] and manual["commit"] != via_git:
            info["advertencias"].append("HEAD leído de .git difiere de git rev-parse HEAD")
    elif manual["commit"]:
        info["commit"], info["rama"], info["fuente"] = manual["commit"], manual["rama"], ".git/HEAD (lectura directa)"
    elif not top or es_raiz_repo:
        info["advertencias"].append("[VERIFICAR: no se pudo determinar el commit (¿no es un repositorio git?)]")
    if info["commit"]:
        info["formato_hash"] = "sha256" if len(info["commit"]) == 64 else "sha1"
    return info


def _commit_manual(raiz: Path) -> dict:
    res = {"commit": None, "rama": None}
    gitdir = raiz / ".git"
    try:
        if gitdir.is_file():  # worktree / submódulo
            m = re.match(r"gitdir:\s*(.+)", _leer_git(gitdir))
            if not m:
                return res
            gitdir = (raiz / m.group(1).strip()).resolve()
        head = _leer_git(gitdir / "HEAD").strip()
        if head.startswith("ref:"):
            ref = head[4:].strip()
            res["rama"] = ref.removeprefix("refs/heads/")
            loose = gitdir / ref
            if loose.is_file():
                res["commit"] = _leer_git(loose).strip()
            else:
                packed = gitdir / "packed-refs"
                if packed.is_file():
                    for ln in _leer_git(packed).splitlines():
                        if ln.endswith(" " + ref):
                            res["commit"] = ln.split()[0]
        elif re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head):
            res["commit"] = head
    except OSError:
        pass
    if res["commit"] and not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", res["commit"]):
        res["commit"] = None
    return res


def _leer_git(ruta: Path) -> str:
    with open(ruta, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


# --------------------------------------------------------------------------- stack y scripts
def extraer_stack(arbol: Arbol) -> dict:
    paquetes = []
    for rel in arbol.archivos:
        if PurePosixPath(rel).name != "package.json":
            continue
        try:
            d = json.loads(arbol.texto(rel) or "{}")
        except json.JSONDecodeError:
            paquetes.append({"archivo": rel, "error": "[VERIFICAR: package.json no es JSON válido]"})
            continue
        paquetes.append({
            "archivo": rel, "nombre": d.get("name"), "version": d.get("version"),
            "tipo_modulo": d.get("type"),
            "dependencias": d.get("dependencies", {}), "dependencias_dev": d.get("devDependencies", {}),
            "scripts": d.get("scripts", {}), "motor": d.get("engines"),
        })
    todas: dict[str, str] = {}
    for p in paquetes:
        for k, v in {**p.get("dependencias", {}), **p.get("dependencias_dev", {})}.items():
            todas.setdefault(k, v)
    conocidos = {
        "react": "Biblioteca de interfaz", "vite": "Empaquetador/dev server", "typescript": "Lenguaje",
        "express": "Servidor HTTP", "@prisma/client": "ORM (cliente)", "prisma": "ORM (CLI)",
        "react-router-dom": "Enrutamiento cliente", "tailwindcss": "Estilos", "jest": "Pruebas unitarias",
        "vitest": "Pruebas unitarias", "@playwright/test": "Pruebas E2E", "axios": "Cliente HTTP",
        "jsonwebtoken": "Autenticación JWT", "bcrypt": "Hash de contraseñas", "recharts": "Gráficos",
        "exceljs": "Exportación Excel", "zod": "Validación", "express-validator": "Validación",
        "joi": "Validación", "pg": "Driver PostgreSQL", "tsx": "Ejecución TS", "helmet": "Seguridad HTTP",
        "cors": "CORS", "express-rate-limit": "Limitación de tasa",
    }
    tecnologias = [{"paquete": k, "rol": r, "version_declarada": todas[k]} for k, r in conocidos.items() if k in todas]
    return {"paquetes": paquetes, "tecnologias_clave": tecnologias,
            "nota": "Versiones declaradas (rango semver) en package.json; no se leyó node_modules ni lockfiles."}


# --------------------------------------------------------------------------- estructura
_ARQ = {"controllers", "services", "routes", "middleware", "models", "repositories", "hooks",
        "contexts", "utils", "types", "config", "components", "pages", "scripts"}


def extraer_estructura(arbol: Arbol, profundidad: int = 2) -> dict:
    conteo: Counter = Counter()
    raiz_archivos = []
    for rel in arbol.archivos:
        partes = rel.split("/")
        if len(partes) == 1:
            raiz_archivos.append(rel)
        for n in range(1, min(profundidad, len(partes) - 1) + 1):
            conteo["/".join(partes[:n])] += 1
    carpetas = [{"ruta": k, "nivel": k.count("/") + 1, "archivos": v} for k, v in sorted(conteo.items())]
    arq: Counter = Counter()
    for rel in arbol.con_ext(EXT_CODIGO):
        if _RE_PRUEBA.search(rel) or "/__tests__/" in rel:
            continue
        partes = rel.split("/")[:-1]
        for i, p in enumerate(partes):
            if p in _ARQ:
                arq["/".join(partes[: i + 1])] += 1
    modulos_ui: Counter = Counter()
    for rel in arbol.con_ext({".tsx", ".jsx"}):
        m = re.match(r"(?:.*/)?src/components/([^/]+)/", rel)
        if m:
            modulos_ui[m.group(1)] += 1
    return {"carpetas": carpetas, "archivos_raiz": raiz_archivos,
            "carpetas_arquitectura_codigo": dict(sorted(arq.items())),
            "modulos_ui_tsx": dict(sorted(modulos_ui.items())),
            "excluidos": dict(sorted(arbol.dirs_excluidos.items())),
            "secretos_omitidos": sorted(arbol.secretos_omitidos),
            "total_archivos_analizables": len(arbol.archivos)}


# --------------------------------------------------------------------------- Prisma
_RE_BLOQUE = re.compile(r"^\s*(model|enum|view|type)\s+(\w+)\s*\{")
_RE_CAMPO = re.compile(r"^\s*(\w+)\s+(Unsupported\([^)]*\)|[A-Za-z_]\w*)(\[\])?(\?)?\s*(.*)$")


def parsear_prisma(texto: str, archivo: str) -> dict:
    modelos, enums, provider = [], [], None
    m = re.search(r"datasource\s+\w+\s*\{[^}]*?provider\s*=\s*\"([^\"]+)\"", texto, re.S)
    if m:
        provider = m.group(1)
    actual = None
    for n, crudo in enumerate(texto.splitlines(), 1):
        ln = re.sub(r"//.*$", "", crudo)
        if actual is None:
            b = _RE_BLOQUE.match(ln)
            if b:
                actual = {"tipo": b.group(1), "nombre": b.group(2), "linea": n, "campos": [],
                          "atributos": [], "valores": []}
            continue
        if ln.strip().startswith("}"):
            (enums if actual["tipo"] == "enum" else modelos).append(actual)
            actual = None
            continue
        s = ln.strip()
        if not s:
            continue
        if actual["tipo"] == "enum":
            v = re.match(r"(\w+)\s*(.*)$", s)
            if v:
                mp = re.search(r'@map\("([^"]*)"\)', v.group(2))
                actual["valores"].append({"nombre": v.group(1), "map": mp.group(1) if mp else None})
            continue
        if s.startswith("@@"):
            actual["atributos"].append(_compacta(s, 160))
            continue
        c = _RE_CAMPO.match(ln)
        if c:
            attrs = c.group(5)
            campo = {"nombre": c.group(1), "tipo": c.group(2), "lista": bool(c.group(3)),
                     "opcional": bool(c.group(4)), "linea": n,
                     "pk": "@id" in attrs, "unico": "@unique" in attrs,
                     "default": (re.search(r"@default\((.*?)\)(?=\s*(@|$))", attrs) or [None, None])[1],
                     "map": (re.search(r'@map\("([^"]*)"\)', attrs) or [None, None])[1],
                     "atributos": _compacta(attrs, 160)}
            rel = re.search(r"@relation\((.*)\)", attrs)
            if rel:
                arg = rel.group(1)
                nom = re.match(r'\s*"([^"]+)"', arg) or re.search(r'name:\s*"([^"]+)"', arg)
                f = re.search(r"fields:\s*\[([^\]]*)\]", arg)
                r = re.search(r"references:\s*\[([^\]]*)\]", arg)
                campo["relacion"] = {
                    "nombre": nom.group(1) if nom else None,
                    "fields": [x.strip() for x in f.group(1).split(",") if x.strip()] if f else [],
                    "references": [x.strip() for x in r.group(1).split(",") if x.strip()] if r else [],
                }
            actual["campos"].append(campo)
    nombres_modelo = {m["nombre"] for m in modelos}
    nombres_enum = {e["nombre"] for e in enums}
    relaciones = []
    for mo in modelos:
        mp = next((re.search(r'@@map\("([^"]*)"\)', a) for a in mo["atributos"] if "@@map" in a), None)
        mo["tabla"] = mp.group(1) if mp else None
        for c in mo["campos"]:
            c["es_relacion"] = c["tipo"] in nombres_modelo
            c["es_enum"] = c["tipo"] in nombres_enum
            if c["es_relacion"]:
                lado_fk = bool(c.get("relacion", {}).get("fields"))
                relaciones.append({
                    "origen": mo["nombre"], "campo": c["nombre"], "destino": c["tipo"],
                    "cardinalidad_desde_origen": "1:N" if c["lista"] else ("N:1" if lado_fk else "1:1 (lado inverso)"),
                    "lado_clave_foranea": lado_fk,
                    "fields": c.get("relacion", {}).get("fields", []),
                    "references": c.get("relacion", {}).get("references", []),
                    "archivo_linea": f"{archivo}:{c['linea']}",
                })
    return {"archivo": archivo, "proveedor_bd": provider, "modelos": modelos,
            "enums": enums, "relaciones": relaciones}


def extraer_prisma(arbol: Arbol) -> dict:
    esquemas = [parsear_prisma(arbol.texto(r), r) for r in arbol.archivos if r.endswith(".prisma")]
    if not esquemas:
        return {"esquemas": [], "modelos": [], "enums": [], "relaciones": [],
                "advertencia": "[VERIFICAR: no se encontró schema.prisma]"}
    return {"esquemas": [e["archivo"] for e in esquemas], "proveedor_bd": esquemas[0]["proveedor_bd"],
            "modelos": [dict(m, archivo=e["archivo"]) for e in esquemas for m in e["modelos"]],
            "enums": [dict(x, archivo=e["archivo"]) for e in esquemas for x in e["enums"]],
            "relaciones": [r for e in esquemas for r in e["relaciones"]]}


# --------------------------------------------------------------------------- Express
_RE_DECL = re.compile(r"\b(?:const|let|var)\s+(\w+)\s*(?::\s*[\w.<>]+)?\s*=\s*"
                      r"(express\s*\.\s*Router|Router|express)\s*\(")
_RE_LLAMADA = re.compile(r"(?<![\w.$])(\w+)\s*\.\s*(get|post|put|patch|delete|use|all)\s*\(")
_RE_IMPORT = re.compile(r"""import\s+(?:(\w+)|\*\s+as\s+(\w+))\s*(?:,\s*\{[^}]*\})?\s+from\s+['"]([^'"]+)['"]"""
                        r"""|(?:const|let|var)\s+(\w+)\s*=\s*require\(\s*['"]([^'"]+)['"]\s*\)""")
_RE_AUTENTICACION = re.compile(r"^(authenticate\w*|requireAuth\w*|verifyToken\w*|isAuthenticated\w*|"
                               r"ensureAuth\w*|protect|jwtAuth\w*|passport\.authenticate)\b")
_RE_AUTORIZACION = re.compile(r"^(authorize\w*|validatePermissions|requirePermissions|denyRoles|requireRole\w*|"
                              r"checkResourcePermission\w*|requireCentroAcopioAssignment|checkEstablecimiento\w*)\b")
_METODOS_HTTP = {"get", "post", "put", "patch", "delete", "all"}
_EXTS_RESOLUCION = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs")


def _mapa_imports(t: str) -> dict[str, str]:
    mapa = {}
    for m in _RE_IMPORT.finditer(t):
        nombre = m.group(1) or m.group(2) or m.group(4)
        if nombre:
            mapa[nombre] = m.group(3) or m.group(5)
    for m in re.finditer(r"(?:const|let|var)\s+(\w+)\s*=\s*(?:React\.)?lazy\(\s*\(\s*\)\s*=>\s*import\(\s*['\"]([^'\"]+)['\"]", t):
        mapa[m.group(1)] = m.group(2)
    return mapa


def resolver_modulo(arbol: Arbol, origen: str, spec: str) -> str | None:
    """Resuelve un import relativo o con alias '@/' a un archivo del repositorio."""
    if spec.startswith("."):
        base = PurePosixPath(origen).parent / spec
    elif spec.startswith("@/"):
        partes = PurePosixPath(origen).parts
        if "src" not in partes:
            return None
        base = PurePosixPath(*partes[: partes.index("src") + 1]) / spec[2:]
    else:
        return None
    partes_n: list[str] = []
    for p in base.parts:
        if p == "..":
            if partes_n:
                partes_n.pop()
        elif p != ".":
            partes_n.append(p)
    cand = "/".join(partes_n)
    conocidos = set(arbol.archivos)
    if cand in conocidos:
        return cand
    for ext in _EXTS_RESOLUCION:
        if cand + ext in conocidos:
            return cand + ext
    for ext in _EXTS_RESOLUCION:
        if f"{cand}/index{ext}" in conocidos:
            return f"{cand}/index{ext}"
    return None


def _unir(prefijo: str, ruta: str) -> str:
    r = "/" + "/".join(x for x in (prefijo + "/" + ruta).split("/") if x)
    return r or "/"


def extraer_endpoints(arbol: Arbol) -> dict:
    archivos = {}
    for rel in arbol.con_ext(EXT_CODIGO):
        if _RE_PRUEBA.search(rel) or "/__tests__/" in rel:
            continue
        t = quitar_comentarios(arbol.texto(rel))
        decl = {m.group(1): ("app" if m.group(2) == "express" else "router") for m in _RE_DECL.finditer(t)}
        if decl:
            archivos[rel] = (t, decl)

    info: dict[str, dict] = {}
    for rel, (t, decl) in archivos.items():
        alias_autz = set()
        for m in re.finditer(r"\b(?:const|let|var)\s+(\w+)\s*=\s*(\w+)\s*\(", t):
            if _RE_AUTORIZACION.match(m.group(2)):
                alias_autz.add(m.group(1))
        imports = _mapa_imports(t)
        rutas_, usos, montajes, globales_path = [], [], [], []
        for m in _RE_LLAMADA.finditer(t):
            recv, metodo = m.group(1), m.group(2)
            if recv not in decl:
                continue
            args, _ = extraer_args(t, m.end() - 1)
            if args is None:
                continue
            textos = [a[1] for a in args]
            linea = _linea(t, m.start())
            if metodo == "use":
                lit = _literal(textos[0]) if textos else None
                resto = textos[1:] if lit is not None else textos
                hijo, mws = None, []
                for a in resto:
                    nombre = a.strip()
                    if re.fullmatch(r"\w+", nombre) and nombre in imports:
                        dest = resolver_modulo(arbol, rel, imports[nombre])
                        if dest and dest in archivos:
                            hijo = dest
                            continue
                    mws.append(_compacta(a))
                if hijo:
                    montajes.append({"hijo": hijo, "prefijo": lit or "", "mws": mws, "linea": linea})
                elif lit is None or lit == "/":
                    usos.append({"linea": linea, "mws": mws})
                elif decl[recv] == "app":
                    globales_path.append({"prefijo": lit, "mws": mws})
                continue
            if metodo not in _METODOS_HTTP or not textos:
                continue
            lit = _literal(textos[0])
            resto = textos[1:] if lit is not None else textos
            handler = _compacta(resto[-1]) if resto else None
            if handler and ("=>" in handler or handler.startswith(("async", "function"))):
                handler = "(función en línea)"
            mws = [_compacta(a) for a in resto[:-1]]
            rutas_.append({"metodo": metodo.upper(), "ruta_local": lit if lit is not None else f"[VERIFICAR: ruta dinámica {_compacta(textos[0], 40)}]",
                           "linea": linea, "handler": handler, "mws": mws, "receptor": recv})
        info[rel] = {"rutas": rutas_, "usos": usos, "montajes": montajes, "globales": globales_path,
                     "tipos": set(decl.values()), "alias_autz": alias_autz}

    padres: dict[str, list[tuple[str, dict]]] = {}
    for rel, d in info.items():
        for mo in d["montajes"]:
            padres.setdefault(mo["hijo"], []).append((rel, mo))

    memo: dict[str, list[tuple[str, list[str]]]] = {}

    def prefijos(rel: str, visitando: tuple = ()) -> list[tuple[str, list[str]]]:
        if rel in memo:
            return memo[rel]
        if rel in visitando:
            return [("", [])]
        res = []
        for padre, mo in padres.get(rel, []):
            for pp, pm in prefijos(padre, visitando + (rel,)):
                res.append((_unir(pp, mo["prefijo"]) if (pp or mo["prefijo"]) else "", pm + mo["mws"]))
        if not res:
            res = [("", [])]
        memo[rel] = res
        return res

    def clasifica(nombres: list[str], alias: set[str]):
        aut, autz = "ninguna", []
        for n in nombres:
            base = re.match(r"[\w.]+", n)
            b = base.group(0) if base else n
            if _RE_AUTENTICACION.match(b):
                aut = "obligatoria"
            elif b == "optionalAuth" and aut == "ninguna":
                aut = "opcional"
            if _RE_AUTORIZACION.match(b) or b in alias:
                autz.append(n)
        return aut, autz

    endpoints = []
    for rel, d in sorted(info.items()):
        es_app = "app" in d["tipos"]
        montado = rel in padres
        for r in d["rutas"]:
            for pref, mws_montaje in prefijos(rel):
                ruta = _unir(pref, r["ruta_local"]) if not r["ruta_local"].startswith("[VERIFICAR") else r["ruta_local"]
                globales = []
                for g in (info[p]["globales"] for p in info if "app" in info[p]["tipos"]):
                    for gg in g:
                        if ruta.startswith(gg["prefijo"]):
                            globales += gg["mws"]
                usos = [m for u in d["usos"] if u["linea"] < r["linea"] for m in u["mws"]]
                orden = [("endpoint", r["mws"]), ("router.use", usos), ("montaje", mws_montaje + globales)]
                nombres = [n for _, lst in orden for n in lst]
                aut, autz = clasifica(nombres, d["alias_autz"] | set().union(*(i["alias_autz"] for i in info.values())))
                origen = None
                for etiqueta, lst in orden:
                    if clasifica(lst, d["alias_autz"])[0] == aut and aut != "ninguna":
                        origen = etiqueta
                        break
                endpoints.append({
                    "metodo": r["metodo"], "ruta": ruta, "ruta_local": r["ruta_local"],
                    "archivo": rel, "linea": r["linea"], "archivo_linea": f"{rel}:{r['linea']}",
                    "handler": r["handler"], "middlewares": nombres,
                    "autenticacion": aut, "origen_autenticacion": origen, "autorizacion": autz,
                    "montaje": "app" if es_app else ("router montado" if montado else "[VERIFICAR: router sin montaje detectado]"),
                })
    por_metodo = Counter(e["metodo"] for e in endpoints)
    return {"total": len(endpoints), "por_metodo": dict(sorted(por_metodo.items())),
            "sin_autenticacion": sum(1 for e in endpoints if e["autenticacion"] == "ninguna"),
            "archivos_de_rutas": sorted(info), "endpoints": endpoints,
            "nota": "Análisis estático por regex: no resuelve router.route() encadenado ni rutas dinámicas. "
                    "autenticacion='ninguna' significa que no se detectó middleware de autenticación en la cadena "
                    "endpoint/router.use/montaje; no prueba que la ruta sea pública (puede autenticarse dentro del controlador)."}


# --------------------------------------------------------------------------- React Router
def extraer_rutas_react(arbol: Arbol) -> dict:
    res = []
    for rel in arbol.con_ext({".tsx", ".jsx"}):
        if _RE_PRUEBA.search(rel) or "/__tests__/" in rel:
            continue
        crudo = arbol.texto(rel)
        if "<Route" not in crudo:
            continue
        t = quitar_comentarios(crudo)
        imports = _mapa_imports(t)
        for m in re.finditer(r"<Route\b", t):
            i, prof, estado = m.end(), 0, None
            while i < len(t):
                c = t[i]
                if estado:
                    if c == "\\":
                        i += 2
                        continue
                    if c == estado:
                        estado = None
                elif c in "'\"`":
                    estado = c
                elif c == "{":
                    prof += 1
                elif c == "}":
                    prof -= 1
                elif c == ">" and prof == 0:
                    break
                i += 1
            etiqueta = t[m.start(): i + 1]
            p = re.search(r'\bpath=(?:"([^"]*)"|\{\s*[\'"]([^\'"]*)[\'"]\s*\})', etiqueta)
            idx = bool(re.search(r"\bindex\b", etiqueta))
            comps = [c for c in re.findall(r"<([A-Z]\w*)", etiqueta[6:])]
            roles = re.search(r"requiredRoles=\{\[([^\]]*)\]\}", etiqueta)
            envoltorios = {"ProtectedRoute", "Suspense", "Route", "Fragment"}
            principal = next((c for c in comps if c not in envoltorios), None)
            redirige = re.search(r'<Navigate\b[^>]*\bto="([^"]*)"', etiqueta)
            archivo_comp = resolver_modulo(arbol, rel, imports[principal]) if principal in imports else None
            res.append({
                "path": (p.group(1) if p and p.group(1) is not None else (p.group(2) if p else None)),
                "index": idx, "componente": principal if principal != "Navigate" else None,
                "redirige_a": redirige.group(1) if redirige else None,
                "roles_requeridos": [x.strip().strip("'\"") for x in roles.group(1).split(",") if x.strip()] if roles else [],
                "protegida": "ProtectedRoute" in comps, "archivo": rel, "linea": _linea(t, m.start()),
                "archivo_linea": f"{rel}:{_linea(t, m.start())}", "archivo_componente": archivo_comp,
            })
    return {"total": len(res), "rutas": res,
            "nota": "Solo <Route> declarativas; las rutas con /* delegan en sub-rutas del módulo (ver archivo del componente)."}


# --------------------------------------------------------------------------- pruebas, env, migraciones
def extraer_pruebas(arbol: Arbol, stack: dict) -> dict:
    archivos = []
    for rel in arbol.archivos:
        if not _RE_PRUEBA.search(rel):
            continue
        t = quitar_comentarios(arbol.texto(rel))
        casos = len(re.findall(r"(?m)^\s*(?:it|test)(?:\.(?:only|skip|each))?\s*\(", t))
        desc = len(re.findall(r"(?m)^\s*describe(?:\.(?:only|skip|each))?\s*\(", t))
        archivos.append({"archivo": rel, "casos": casos, "suites": desc,
                         "tipo": "e2e" if (".spec." in rel or "/tests/" in rel) else "unitaria"})
    configs = [r for r in arbol.archivos if re.search(r"(^|/)(jest|vitest|playwright)\.config\.\w+$", r)]
    marcos = sorted({t["paquete"] for t in stack["tecnologias_clave"] if t["paquete"] in ("jest", "vitest", "@playwright/test")})
    return {"archivos": len(archivos), "casos_aprox": sum(a["casos"] for a in archivos),
            "detalle": archivos, "configuraciones": configs, "marcos_declarados": marcos,
            "nota": "Casos contados por regex (it/test al inicio de línea); it.each cuenta como 1."}


# Variables integradas de Node/Vite (import.meta.env): no son configuración definida por el proyecto.
ENV_INTEGRADAS = {"DEV", "PROD", "MODE", "SSR", "BASE_URL", "NODE_ENV"}


def extraer_env(arbol: Arbol) -> dict:
    usos: dict[str, list[str]] = {}
    for rel in arbol.con_ext(EXT_CODIGO):
        t = quitar_comentarios(arbol.texto(rel))
        hallados: list[tuple[str, int]] = []
        for m in re.finditer(r"(?:process\.env|import\.meta\.env)\.([A-Za-z_]\w*)", t):
            hallados.append((m.group(1), _linea(t, m.start())))
        for m in re.finditer(r"(?:process\.env|import\.meta\.env)\[\s*['\"]([A-Za-z_]\w*)['\"]\s*\]", t):
            hallados.append((m.group(1), _linea(t, m.start())))
        for m in re.finditer(r"\{([^{}]*)\}\s*=\s*process\.env\b", t):
            for nom in re.findall(r"(\w+)\s*(?::[^,}]+)?(?:=[^,}]+)?(?:,|$)", m.group(1)):
                hallados.append((nom, _linea(t, m.start())))
        for nom, ln in hallados:
            usos.setdefault(nom, []).append(f"{rel}:{ln}")
    propias = [{"nombre": k, "usos": len(v), "ejemplos": v[:3]} for k, v in sorted(usos.items()) if k not in ENV_INTEGRADAS]
    integradas = [{"nombre": k, "usos": len(v), "ejemplos": v[:3]} for k, v in sorted(usos.items()) if k in ENV_INTEGRADAS]
    variables = propias
    return {"total": len(variables), "variables": variables,
            "integradas_excluidas": integradas,
            "nota": "Total = variables definidas por el proyecto; se excluyen las integradas de Node/Vite (" + ", ".join(sorted(ENV_INTEGRADAS)) + "), listadas aparte. Solo NOMBRES referenciados en código; no se lee ningún archivo .env* ni se guardan valores."}


def extraer_migraciones(arbol: Arbol) -> dict:
    prisma, sql_sueltos = {}, []
    for rel in arbol.archivos:
        m = re.match(r"(.*/prisma/migrations)/([^/]+)/([^/]+)$", rel)
        if m:
            prisma.setdefault((m.group(1), m.group(2)), []).append(m.group(3))
        elif rel.endswith(".sql") and "/migrations/" in "/" + rel and "/prisma/" not in "/" + rel:
            sql_sueltos.append(rel)
    detalle = []
    for (base, nombre), fs in sorted(prisma.items(), key=lambda x: x[0][1]):
        f = re.match(r"(\d{8,14})_", nombre)
        detalle.append({"nombre": nombre, "carpeta": base, "fecha_prefijo": f.group(1) if f else None,
                        "tiene_migration_sql": "migration.sql" in fs})
    return {"prisma_total": len(detalle), "prisma": detalle, "sql_manuales": sql_sueltos}


# --------------------------------------------------------------------------- inventario completo
def construir_inventario(raiz: str | Path, profundidad: int = 2) -> dict:
    raiz = Path(raiz).expanduser().resolve(strict=False)
    arbol = Arbol(raiz)
    stack = extraer_stack(arbol)
    inv = {
        "version_inventario": VERSION_INVENTARIO,
        "raiz": str(raiz),
        "commit": info_git(raiz),
        "stack": stack,
        "estructura": extraer_estructura(arbol, profundidad),
        "prisma": extraer_prisma(arbol),
        "express": extraer_endpoints(arbol),
        "react_router": extraer_rutas_react(arbol),
        "pruebas": extraer_pruebas(arbol, stack),
        "variables_entorno": extraer_env(arbol),
        "migraciones": extraer_migraciones(arbol),
    }
    inv["resumen"] = {
        "commit": inv["commit"]["commit"],
        "modelos": len(inv["prisma"]["modelos"]), "enums": len(inv["prisma"]["enums"]),
        "relaciones": len(inv["prisma"]["relaciones"]),
        "endpoints": inv["express"]["total"], "endpoints_sin_autenticacion": inv["express"]["sin_autenticacion"],
        "rutas_react": inv["react_router"]["total"],
        "archivos_prueba": inv["pruebas"]["archivos"], "casos_prueba_aprox": inv["pruebas"]["casos_aprox"],
        "variables_entorno": inv["variables_entorno"]["total"],
        "migraciones_prisma": inv["migraciones"]["prisma_total"],
        "paquetes_npm": len(stack["paquetes"]),
    }
    canon = json.dumps(inv, sort_keys=True, ensure_ascii=False, default=str)
    inv["huella_sha256"] = hashlib.sha256(canon.encode("utf-8")).hexdigest()
    inv["generado_en"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return inv


# --------------------------------------------------------------------------- Markdown
def _fila(celdas) -> str:
    return "| " + " | ".join(str(c).replace("|", "\\|").replace("\n", " ") for c in celdas) + " |"


def _tabla(cab, filas) -> list[str]:
    return [_fila(cab), _fila(["---"] * len(cab)), *[_fila(f) for f in filas], ""]


def a_markdown(inv: dict) -> str:
    g, r = inv["commit"], inv["resumen"]
    L = ["# Inventario del código SIVAC (syncova)", "",
         f"- Repositorio: `{inv['raiz']}` (solo lectura)",
         f"- Commit documentado: `{g['commit']}` ({g['formato_hash']}; rama `{g['rama']}`; fuente: {g['fuente']})",
         f"- Fecha del commit: {g['fecha_commit']} — {g['asunto']}",
         f"- Huella SHA-256 del inventario: `{inv['huella_sha256']}`",
         f"- Generado: {inv['generado_en']}", ""]
    L += [f"> {a}" for a in g["advertencias"]]
    L += ["## Resumen", ""] + _tabla(["Elemento", "Cantidad"], [(k, v) for k, v in r.items() if k != "commit"])
    L += ["## Stack", ""]
    L += _tabla(["Paquete", "Rol", "Versión declarada"], [(t["paquete"], t["rol"], t["version_declarada"]) for t in inv["stack"]["tecnologias_clave"]])
    for p in inv["stack"]["paquetes"]:
        L += [f"### {p['archivo']} ({p.get('nombre')} {p.get('version')})", "",
              f"Dependencias: {len(p.get('dependencias', {}))}; devDependencies: {len(p.get('dependencias_dev', {}))}", ""]
        if p.get("scripts"):
            L += _tabla(["Script npm", "Comando"], [(k, f"`{v}`") for k, v in p["scripts"].items()])
    L += ["## Estructura (niveles 1 y 2)", ""]
    L += _tabla(["Carpeta", "Archivos"], [(c["ruta"], c["archivos"]) for c in inv["estructura"]["carpetas"]])
    L += ["Excluidos (no leídos): " + ", ".join(f"{k} ({v})" for k, v in inv["estructura"]["excluidos"].items()),
          f"Secretos omitidos sin abrir: {len(inv['estructura']['secretos_omitidos'])}", ""]
    L += ["## Esquema Prisma", ""]
    L += _tabla(["Modelo", "Tabla", "Campos", "Archivo:línea"],
                [(m["nombre"], m["tabla"], len(m["campos"]), f"{m['archivo']}:{m['linea']}") for m in inv["prisma"]["modelos"]])
    for m in inv["prisma"]["modelos"]:
        L += [f"### {m['nombre']}", ""]
        L += _tabla(["Campo", "Tipo", "Mod.", "PK/UK", "Default"],
                    [(c["nombre"], c["tipo"] + ("[]" if c["lista"] else "") + ("?" if c["opcional"] else ""),
                      "relación" if c["es_relacion"] else ("enum" if c["es_enum"] else ""),
                      ("PK " if c["pk"] else "") + ("UK" if c["unico"] else ""), c["default"] or "") for c in m["campos"]])
    L += ["### Enums", ""]
    L += _tabla(["Enum", "Valores"], [(e["nombre"], ", ".join(v["nombre"] for v in e["valores"])) for e in inv["prisma"]["enums"]])
    L += ["### Relaciones", ""]
    L += _tabla(["Origen.campo", "Destino", "Cardinalidad", "FK", "Archivo:línea"],
                [(f"{x['origen']}.{x['campo']}", x["destino"], x["cardinalidad_desde_origen"], ",".join(x["fields"]), x["archivo_linea"]) for x in inv["prisma"]["relaciones"]])
    L += ["## Endpoints Express", "", f"Total: {inv['express']['total']}; sin autenticación detectada: {inv['express']['sin_autenticacion']}", ""]
    L += _tabla(["Método", "Ruta", "Autenticación", "Autorización", "Handler", "Archivo:línea"],
                [(e["metodo"], e["ruta"], e["autenticacion"], "; ".join(e["autorizacion"]), e["handler"], e["archivo_linea"]) for e in inv["express"]["endpoints"]])
    L += ["## Rutas React Router", ""]
    L += _tabla(["Path", "Componente", "Roles", "Archivo componente", "Archivo:línea"],
                [(x["path"] or ("(index)" if x["index"] else ""), x["componente"] or (f"→ {x['redirige_a']}" if x["redirige_a"] else ""),
                  ",".join(x["roles_requeridos"]), x["archivo_componente"] or "", x["archivo_linea"]) for x in inv["react_router"]["rutas"]])
    L += ["## Pruebas", "", f"Archivos: {inv['pruebas']['archivos']}; casos (aprox.): {inv['pruebas']['casos_aprox']}; marcos: {', '.join(inv['pruebas']['marcos_declarados'])}", ""]
    L += _tabla(["Archivo", "Tipo", "Suites", "Casos"], [(p["archivo"], p["tipo"], p["suites"], p["casos"]) for p in inv["pruebas"]["detalle"]])
    L += ["## Variables de entorno (solo nombres)", ""]
    L += _tabla(["Variable", "Usos", "Ejemplos"], [(v["nombre"], v["usos"], ", ".join(v["ejemplos"])) for v in inv["variables_entorno"]["variables"]])
    L += ["## Migraciones", "", f"Prisma: {inv['migraciones']['prisma_total']}; SQL manuales: {len(inv['migraciones']['sql_manuales'])}", ""]
    L += _tabla(["Migración", "Prefijo de fecha"], [(m["nombre"], m["fecha_prefijo"]) for m in inv["migraciones"]["prisma"]])
    L += [f"- `{s}`" for s in inv["migraciones"]["sql_manuales"]] + [""]
    return "\n".join(L)


# --------------------------------------------------------------------------- trazar
_RE_ASIGNA_SECRETO = re.compile(
    r"""(?ix)
    (\b[\w.-]*(?:secret|token|pass(?:w(?:or)?d)?(?-i:(?![a-z]))|pwd|contrase[ñn]a|clave|api[_-]?key|private[_-]?key|credential|auth(?-i:(?![a-z])))[\w.-]*
    [*_"'`]*\s*[:=]\s*)
    ("[^"\n]*"|'[^'\n]*'|`[^`\n]*`|[^\s,;]+)""")
_RE_TOKENS = re.compile(
    r"\b(?:eyJ[\w-]{10,}\.[\w-]{10,}\.[\w-]{5,}|AKIA[0-9A-Z]{16}|AIza[\w-]{30,}|gh[pousr]_\w{20,}|sk-[\w-]{20,})(?!\w)")
# Credenciales embebidas en URLs: esquema://usuario:clave@host
_RE_URL_CRED = re.compile(r"(\b[a-z][a-z0-9+.-]*://[^\s:/@]+:)[^\s@/]+(@)", re.I)


def enmascarar_secretos(linea: str) -> str:
    """Oculta valores de asignaciones con nombre sensible, credenciales en URL y tokens reconocibles."""
    linea = _RE_URL_CRED.sub(lambda m: m.group(1) + "***" + m.group(2), linea)
    linea = _RE_ASIGNA_SECRETO.sub(lambda m: m.group(1) + "***", linea)
    return _RE_TOKENS.sub("***", linea)


def trazar(raiz: str | Path, terminos: list[str], max_menciones: int = 40, inventario: dict | None = None) -> dict:
    """Busca piezas del sistema relacionadas con los términos (OR, sin distinguir acentos/mayúsculas)."""
    raiz = Path(raiz).expanduser().resolve(strict=False)
    inv = inventario or construir_inventario(raiz)
    arbol = Arbol(raiz)
    ns = [_normalizar(t) for t in terminos if t.strip()]

    def coincide(*textos) -> bool:
        h = _normalizar(" ".join(str(x) for x in textos if x))
        return any(n in h for n in ns)

    endpoints = [e for e in inv["express"]["endpoints"]
                 if coincide(e["metodo"], e["ruta"], e["handler"], e["archivo"], " ".join(e["middlewares"]))]
    modelos = []
    for m in inv["prisma"]["modelos"]:
        campos = [c["nombre"] for c in m["campos"] if coincide(c["nombre"], c["tipo"], c["map"])]
        if coincide(m["nombre"], m["tabla"]) or campos:
            modelos.append({"modelo": m["nombre"], "tabla": m["tabla"], "archivo_linea": f"{m['archivo']}:{m['linea']}",
                            "campos_coincidentes": campos})
    enums = [{"enum": e["nombre"], "archivo": e["archivo"]} for e in inv["prisma"]["enums"]
             if coincide(e["nombre"], " ".join(v["nombre"] for v in e["valores"]))]
    rutas_react = [x for x in inv["react_router"]["rutas"] if coincide(x["path"], x["componente"], x["archivo_componente"], x["archivo"])]
    archivos = [a for a in arbol.archivos if coincide(a) and PurePosixPath(a).suffix.lower() in EXT_CODIGO | {".prisma", ".md", ".sql"}]
    menciones, total_menc = [], 0
    for rel in arbol.con_ext(EXT_LEIBLES | EXT_TRAZA_EXTRA):
        n_rel = 0
        for i, ln in enumerate(arbol.texto(rel).splitlines(), 1):
            if coincide(ln):
                total_menc += 1
                if n_rel < 3 and len(menciones) < max_menciones:
                    menciones.append({"archivo_linea": f"{rel}:{i}", "texto": enmascarar_secretos(_compacta(ln.strip(), 140))})
                n_rel += 1
    pruebas = [p for p in inv["pruebas"]["detalle"] if coincide(p["archivo"]) or any(
        m["archivo_linea"].startswith(p["archivo"] + ":") for m in menciones)]
    total = len(endpoints) + len(modelos) + len(enums) + len(rutas_react) + len(archivos) + total_menc
    return {"terminos": terminos, "commit": inv["commit"]["commit"], "total_coincidencias": total,
            "endpoints": endpoints, "modelos": modelos, "enums": enums, "rutas_react": rutas_react,
            "archivos": archivos, "pruebas": pruebas, "menciones": menciones,
            "menciones_total": total_menc,
            "nota": "Coincidencia textual; un HU-xx solo aparece si el código o la documentación del repositorio lo cita literalmente."}


def traza_a_texto(tr: dict) -> str:
    L = [f"Traza de {tr['terminos']} sobre commit {tr['commit']}: {tr['total_coincidencias']} coincidencias", ""]
    L.append(f"ENDPOINTS ({len(tr['endpoints'])})")
    L += [f"  {e['metodo']:<6} {e['ruta']:<55} {e['archivo_linea']}" for e in tr["endpoints"]]
    L.append(f"MODELOS ({len(tr['modelos'])})")
    L += [f"  {m['modelo']} [{m['tabla']}] {m['archivo_linea']}  campos: {', '.join(m['campos_coincidentes'])}" for m in tr["modelos"]]
    L.append(f"ENUMS ({len(tr['enums'])})")
    L += [f"  {e['enum']}  {e['archivo']}" for e in tr["enums"]]
    L.append(f"RUTAS REACT ({len(tr['rutas_react'])})")
    L += [f"  {x['path']} -> {x['componente']}  {x['archivo_linea']}" for x in tr["rutas_react"]]
    L.append(f"ARCHIVOS ({len(tr['archivos'])})")
    L += [f"  {a}" for a in tr["archivos"][:60]]
    L.append(f"PRUEBAS ({len(tr['pruebas'])})")
    L += [f"  {p['archivo']} ({p['casos']} casos)" for p in tr["pruebas"]]
    L.append(f"MENCIONES ({tr['menciones_total']} en total; se muestran {len(tr['menciones'])})")
    L += [f"  {m['archivo_linea']}: {m['texto']}" for m in tr["menciones"]]
    return "\n".join(L)


# --------------------------------------------------------------------------- CLI
def _texto_resumen(inv: dict) -> str:
    g = inv["commit"]
    L = [f"Inventario SIVAC (solo lectura) — {inv['raiz']}",
         f"Commit: {g['commit']} ({g['formato_hash']}, rama {g['rama']}, {g['fuente']})",
         f"Huella SHA-256 del inventario: {inv['huella_sha256']}", ""]
    L += [f"  {k:<30} {v}" for k, v in inv["resumen"].items() if k != "commit"]
    L += [f"ADVERTENCIA: {a}" for a in g["advertencias"]]
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    seguridad.configurar_utf8()
    p = argparse.ArgumentParser(description="Inventario de solo lectura del código SIVAC (syncova).")
    sub = p.add_subparsers(dest="cmd", required=True)
    for nombre in ("inventario", "trazar"):
        sp = sub.add_parser(nombre)
        sp.add_argument("--raiz", default=str(rutas.SYNCOVA), help="repositorio a inspeccionar (defecto: syncova)")
        sp.add_argument("--json", action="store_true", help="salida JSON por stdout")
    pi = sub.choices["inventario"]
    pi.add_argument("--profundidad", type=int, default=2)
    pi.add_argument("--guardar", action="store_true", help="escribe JSON y Markdown en salidas/inventario_syncova/")
    pi.add_argument("--salida-json")
    pi.add_argument("--salida-md")
    pi.add_argument("--sobrescribir", action="store_true", help="permite reemplazar archivos de salida existentes")
    pi.add_argument("--markdown", action="store_true", help="imprime el Markdown completo")
    pt = sub.choices["trazar"]
    pt.add_argument("terminos", nargs="+", help="HU-xx o palabras (se combinan con OR)")
    pt.add_argument("--max-menciones", type=int, default=40)
    a = p.parse_args(argv)

    raiz = Path(a.raiz).expanduser()
    if not raiz.is_dir():
        print(f"ERROR: no existe el directorio {raiz}", file=sys.stderr)
        return 2

    if a.cmd == "trazar":
        tr = trazar(raiz, a.terminos, a.max_menciones)
        print(json.dumps(tr, ensure_ascii=False, indent=2) if a.json else traza_a_texto(tr))
        return 0 if tr["total_coincidencias"] else 1

    inv = construir_inventario(raiz, a.profundidad)
    md = a_markdown(inv)
    destinos = []
    if a.guardar:
        base = rutas.SALIDAS / "inventario_syncova"
        corto = (inv["commit"]["commit"] or "sin_commit")[:8]
        destinos += [(base / f"inventario_syncova_{corto}.json", None), (base / f"inventario_syncova_{corto}.md", None)]
    if a.salida_json:
        destinos.append((Path(a.salida_json), "json"))
    if a.salida_md:
        destinos.append((Path(a.salida_md), "md"))
    if destinos:
        from scripts.agentes.escritura_segura import escribir_salida
        for ruta, tipo in destinos:
            es_json = tipo == "json" or (tipo is None and ruta.suffix == ".json")
            cuerpo = json.dumps(inv, ensure_ascii=False, indent=2, default=str) if es_json else md
            try:
                print(f"Escrito: {escribir_salida(ruta, cuerpo, no_escribir_en=raiz, sobrescribir=a.sobrescribir)}",
                      file=sys.stderr)
            except FileExistsError:
                print(f"ERROR: ya existe {ruta}. Use --sobrescribir si desea reemplazarlo.", file=sys.stderr)
                return 2
    if a.json:
        print(json.dumps(inv, ensure_ascii=False, indent=2, default=str))
    elif a.markdown:
        print(md)
    else:
        print(_texto_resumen(inv))
    criticos = (not inv["commit"]["commit"]) or not inv["prisma"]["modelos"] or inv["express"]["total"] == 0
    return 1 if criticos else 0


if __name__ == "__main__":
    sys.exit(main())
