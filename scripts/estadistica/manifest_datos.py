#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — MANIFEST de procedencia de los datos de campo (datos/raw/MANIFEST.json).

El análisis inferencial solo corre con datos REALES certificados por el tesista.
El MANIFEST es esa certificación: declara origen, responsable, instrumentos,
hashes SHA-256 de cada CSV y la declaración literal de no simulación.

Este módulo NUNCA escribe datos ni rellena la declaración del tesista:
  * `plantilla` escribe un formato con campos vacíos.
  * `validar`   comprueba campos, hashes reales y n_esperado == 14.
  * `sellar`    calcula los hashes vacíos de los archivos listados y agrega un sello
                de integridad; exige que la declaración y la firma ya estén escritas
                por el tesista (no las completa).

Códigos de salida: 0 válido/ok, 1 error de ejecución, 2 uso incorrecto,
3 BLOQUEADO (manifiesto ausente o inválido).

Uso:
    python scripts/estadistica/manifest_datos.py plantilla [--forzar]
    python scripts/estadistica/manifest_datos.py validar [--json]
    python scripts/estadistica/manifest_datos.py sellar [--entrada RUTA] [--forzar]
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad  # noqa: E402

DECLARACION_LITERAL = (
    "Declaro que estos datos provienen de mediciones reales de campo y no han sido simulados."
)
ESTADO_BLOQUEADO = "BLOQUEADO: esperando datos de campo"
N_ESPERADO = rutas.N_CENSAL  # 14
FASES = ("pretest", "postest")
CAMPOS_OBLIGATORIOS = (
    "origen", "responsable", "fecha_recoleccion", "instrumentos_versiones",
    "n_esperado", "archivos", "declaracion_tesista", "firmado_por", "fecha_firma",
)
_RE_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_RE_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")

MANIFEST_RAW = rutas.DATOS_RAW / "MANIFEST.json"
MANIFEST_PLANTILLA = rutas.DATOS_PLANTILLAS / "MANIFEST.plantilla.json"


def asegurar_destino_modulo(ruta: str | Path) -> Path:
    """Guarda de escritura del módulo estadístico.

    Aplica seguridad.asegurar_escritura_permitida y, además, veta todo
    referencias/ (inmutable por Regla 01, aunque seguridad.py solo protege tres
    subcarpetas) y datos/raw/ (los resultados nunca se escriben junto a los datos).
    """
    destino = seguridad.asegurar_escritura_permitida(ruta)
    for vedada in (rutas.REFERENCIAS, rutas.DATOS_RAW):
        v = vedada.resolve(strict=False)
        if destino == v or v in destino.parents:
            raise seguridad.EscrituraProhibida(
                f"Escritura denegada en {destino}: {vedada.name}/ es inmutable o reservada a datos de campo. "
                "Ver .claude/rules/01_seguridad.md"
            )
    return destino


# --------------------------------------------------------------------------
# Funciones puras
# --------------------------------------------------------------------------
def plantilla_manifest() -> dict:
    """Formato vacío del MANIFEST. No contiene ningún dato ni declaración."""
    return {
        "_instrucciones": (
            "Completar SOLO con datos reales de campo. origen debe ser 'campo'; "
            "n_esperado debe ser 14; fechas en formato AAAA-MM-DD; fase: pretest|postest; "
            "sha256 puede dejarse vacío y se calcula con el comando 'sellar'. "
            "declaracion_tesista debe ser escrita por el tesista con este texto literal: "
            f"'{DECLARACION_LITERAL}'. Ningún script completa ese campo."
        ),
        "origen": "",
        "responsable": "",
        "fecha_recoleccion": "",
        "instrumentos_versiones": {},
        "n_esperado": None,
        "archivos": [{"nombre": "", "sha256": "", "fase": ""}],
        "declaracion_tesista": "",
        "firmado_por": "",
        "fecha_firma": "",
    }


def _fecha_valida(valor) -> bool:
    if not isinstance(valor, str) or not _RE_FECHA.match(valor):
        return False
    try:
        _dt.date.fromisoformat(valor)
        return True
    except ValueError:
        return False


def _texto_no_vacio(valor) -> bool:
    return isinstance(valor, str) and bool(valor.strip())


def validar_estructura(m: dict) -> list[str]:
    """Valida campos y tipos (sin tocar el disco). Devuelve lista de errores."""
    err: list[str] = []
    if not isinstance(m, dict):
        return ["El MANIFEST debe ser un objeto JSON."]
    for c in CAMPOS_OBLIGATORIOS:
        if c not in m:
            err.append(f"Falta el campo obligatorio '{c}'.")
    if err:
        return err
    if m["origen"] != "campo":
        err.append("origen debe ser exactamente 'campo'.")
    if not _texto_no_vacio(m["responsable"]):
        err.append("responsable (nombre del tesista) está vacío.")
    if not _fecha_valida(m["fecha_recoleccion"]):
        err.append("fecha_recoleccion debe ser una fecha válida AAAA-MM-DD.")
    iv = m["instrumentos_versiones"]
    if not isinstance(iv, dict) or not iv or not all(
        _texto_no_vacio(k) and _texto_no_vacio(v) for k, v in iv.items()
    ):
        err.append("instrumentos_versiones debe ser un objeto no vacío {instrumento: versión}.")
    if isinstance(m["n_esperado"], bool) or m["n_esperado"] != N_ESPERADO:
        err.append(f"n_esperado debe ser {N_ESPERADO} (población censal).")
    arch = m["archivos"]
    if not isinstance(arch, list) or not arch:
        err.append("archivos debe ser una lista no vacía.")
    else:
        fases: list[str] = []
        nombres: list[str] = []
        for i, a in enumerate(arch):
            if not isinstance(a, dict):
                err.append(f"archivos[{i}] no es un objeto.")
                continue
            nombre = a.get("nombre")
            if not _texto_no_vacio(nombre) or Path(nombre).name != nombre or not nombre.lower().endswith(".csv"):
                err.append(f"archivos[{i}].nombre debe ser un nombre de archivo .csv sin carpetas.")
            else:
                nombres.append(nombre)
            if a.get("fase") not in FASES:
                err.append(f"archivos[{i}].fase debe ser 'pretest' o 'postest'.")
            else:
                fases.append(a["fase"])
            if not (isinstance(a.get("sha256"), str) and _RE_SHA256.match(a["sha256"])):
                err.append(f"archivos[{i}].sha256 ausente o no es un SHA-256 hexadecimal (ejecutar 'sellar').")
        if len(set(nombres)) != len(nombres):
            err.append("archivos contiene nombres repetidos.")
        for f in FASES:
            if fases.count(f) != 1:
                err.append(f"Debe declararse exactamente un archivo de fase '{f}' (hay {fases.count(f)}).")
    if m["declaracion_tesista"] != DECLARACION_LITERAL:
        err.append("declaracion_tesista no coincide con el texto literal exigido (debe escribirla el tesista).")
    if not _texto_no_vacio(m["firmado_por"]):
        err.append("firmado_por está vacío.")
    if not _fecha_valida(m["fecha_firma"]):
        err.append("fecha_firma debe ser una fecha válida AAAA-MM-DD.")
    return err


def validar_contra_disco(m: dict, dir_raw: Path) -> list[str]:
    """Comprueba que los SHA-256 declarados coinciden con los archivos reales
    y que no hay CSV en dir_raw sin declarar."""
    err: list[str] = []
    declarados = set()
    archivos = m.get("archivos", [])
    for a in archivos if isinstance(archivos, list) else []:
        if not isinstance(a, dict) or not isinstance(a.get("nombre"), str):
            continue
        declarados.add(a["nombre"])
        ruta = dir_raw / a["nombre"]
        if not ruta.is_file():
            err.append(f"Archivo declarado no existe en {dir_raw}: {a['nombre']}")
            continue
        real = seguridad.sha256_archivo(ruta)
        if a.get("sha256") != real:
            err.append(
                f"SHA-256 no coincide para {a['nombre']} (declarado {str(a.get('sha256'))[:12]}, real {real[:12]}): "
                "el archivo fue alterado o el manifiesto está desactualizado."
            )
    if dir_raw.is_dir():
        for p in sorted(dir_raw.glob("*.csv")):
            if p.name not in declarados:
                err.append(f"CSV presente en {dir_raw.name}/ sin declarar en el MANIFEST: {p.name}")
    return err


def sello_contenido(m: dict) -> str:
    """SHA-256 del contenido canónico del manifiesto (sin el propio sello)."""
    base = {k: v for k, v in m.items() if k != "sello_sha256"}
    canon = json.dumps(base, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def evaluar(ruta_manifest: Path, dir_raw: Path) -> dict:
    """Evalúa el manifiesto y devuelve {estado, valido, sellado, errores, manifest}."""
    ruta_manifest, dir_raw = Path(ruta_manifest), Path(dir_raw)
    if not ruta_manifest.is_file():
        return {"estado": ESTADO_BLOQUEADO, "valido": False, "sellado": False,
                "errores": [f"No existe el MANIFEST: {ruta_manifest}"], "manifest": None}
    try:
        m = json.loads(ruta_manifest.read_text(encoding="utf-8-sig"))
    except UnicodeDecodeError as e:
        return {"estado": ESTADO_BLOQUEADO, "valido": False, "sellado": False,
                "errores": [f"MANIFEST no está codificado en UTF-8 (guardar como UTF-8): {e}"], "manifest": None}
    except (ValueError, OSError) as e:  # JSONDecodeError es ValueError
        return {"estado": ESTADO_BLOQUEADO, "valido": False, "sellado": False,
                "errores": [f"MANIFEST ilegible o JSON inválido: {e}"], "manifest": None}
    errores = validar_estructura(m)
    if not errores:
        errores += validar_contra_disco(m, dir_raw)
        if "sello_sha256" in m and m["sello_sha256"] != sello_contenido(m):
            errores.append("sello_sha256 no coincide: el MANIFEST fue modificado después de sellarse.")
    valido = not errores
    return {
        "estado": "VALIDO" if valido else ESTADO_BLOQUEADO,
        "valido": valido,
        "sellado": bool(valido and "sello_sha256" in m),
        "errores": errores,
        "manifest": m if valido else None,
    }


def sellar_manifest(m: dict, dir_raw: Path) -> tuple[dict | None, list[str]]:
    """Completa SOLO los sha256 vacíos y agrega sello. No toca la declaración."""
    err: list[str] = []
    if not isinstance(m, dict):
        return None, ["El MANIFEST debe ser un objeto JSON."]
    m = json.loads(json.dumps(m))  # copia profunda
    m.pop("_instrucciones", None)
    if m.get("declaracion_tesista") != DECLARACION_LITERAL:
        err.append("declaracion_tesista debe estar ya escrita por el tesista con el texto literal; sellar no la completa.")
    if not _texto_no_vacio(m.get("firmado_por")):
        err.append("firmado_por debe estar escrito por el tesista; sellar no lo completa.")
    if not _fecha_valida(m.get("fecha_firma")):
        err.append("fecha_firma debe estar escrita por el tesista (AAAA-MM-DD); sellar no la completa.")
    if err:
        return None, err
    archivos = m.get("archivos")
    for a in archivos if isinstance(archivos, list) else []:
        if not isinstance(a, dict) or not _texto_no_vacio(a.get("nombre")) or Path(a["nombre"]).name != a["nombre"]:
            continue
        ruta = Path(dir_raw) / a["nombre"]
        if not ruta.is_file():
            err.append(f"Archivo declarado no existe: {a['nombre']}")
            continue
        real = seguridad.sha256_archivo(ruta)
        if not a.get("sha256"):
            a["sha256"] = real
        elif a["sha256"] != real:
            err.append(f"SHA-256 declarado no coincide con el archivo real: {a['nombre']} (no se sobrescribe).")
    if err:
        return None, err
    err = validar_estructura(m) + validar_contra_disco(m, Path(dir_raw))
    if err:
        return None, err
    m["sello_sha256"] = sello_contenido(m)
    return m, []


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def _escribir_json(ruta: Path, obj: dict) -> None:
    destino = asegurar_destino_modulo(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cmd_plantilla(args) -> int:
    destino = Path(args.salida)
    if destino.exists() and not args.forzar:
        print(f"Ya existe {destino}; use --forzar para regenerar la plantilla vacía.", file=sys.stderr)
        return 1
    _escribir_json(destino, plantilla_manifest())
    print(f"Plantilla vacía escrita en {destino} (sin datos ni declaración).")
    return 0


def cmd_validar(args) -> int:
    res = evaluar(Path(args.manifest), Path(args.raw))
    salida = {k: v for k, v in res.items() if k != "manifest"}
    if args.json:
        print(json.dumps(salida, indent=2, ensure_ascii=False))
    else:
        print(f"Estado: {res['estado']}")
        for e in res["errores"]:
            print(f"  - {e}")
        if res["valido"]:
            print(f"MANIFEST válido ({'sellado' if res['sellado'] else 'sin sello de integridad'}).")
    return 0 if res["valido"] else 3


def cmd_sellar(args) -> int:
    entrada = Path(args.entrada or args.manifest)
    if not entrada.is_file():
        print(f"{ESTADO_BLOQUEADO}: no existe {entrada}", file=sys.stderr)
        return 3
    try:
        m = json.loads(entrada.read_text(encoding="utf-8-sig"))
    except UnicodeDecodeError as e:
        print(f"{ESTADO_BLOQUEADO}: el MANIFEST no está en UTF-8: {e}", file=sys.stderr)
        return 3
    except ValueError as e:
        print(f"JSON inválido: {e}", file=sys.stderr)
        return 1
    sellado, err = sellar_manifest(m, Path(args.raw))
    if err:
        print("No se selló el MANIFEST:")
        for e in err:
            print(f"  - {e}")
        return 3
    destino = Path(args.manifest)
    if destino.exists() and destino.resolve() != entrada.resolve() and not args.forzar:
        print(f"Ya existe {destino}; use --forzar para reemplazarlo.", file=sys.stderr)
        return 1
    _escribir_json(destino, sellado)
    print(f"MANIFEST sellado en {destino} (sello {sellado['sello_sha256'][:16]}).")
    return 0


def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="MANIFEST de procedencia de datos de campo (SIVAC).")
    sub = p.add_subparsers(dest="cmd", required=True)
    comunes = argparse.ArgumentParser(add_help=False)
    comunes.add_argument("--manifest", default=str(MANIFEST_RAW), help="Ruta del MANIFEST.json")
    comunes.add_argument("--raw", default=str(rutas.DATOS_RAW), help="Carpeta de datos crudos")
    sp = sub.add_parser("plantilla", help="Escribe la plantilla vacía")
    sp.add_argument("--salida", default=str(MANIFEST_PLANTILLA))
    sp.add_argument("--forzar", action="store_true")
    sv = sub.add_parser("validar", parents=[comunes], help="Valida campos, hashes y n_esperado")
    sv.add_argument("--json", action="store_true")
    ss = sub.add_parser("sellar", parents=[comunes], help="Calcula hashes y sella (no rellena la declaración)")
    ss.add_argument("--entrada", help="MANIFEST a sellar (por defecto el de --manifest)")
    ss.add_argument("--forzar", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    seguridad.configurar_utf8()
    args = construir_parser().parse_args(argv)
    try:
        return {"plantilla": cmd_plantilla, "validar": cmd_validar, "sellar": cmd_sellar}[args.cmd](args)
    except seguridad.EscrituraProhibida as e:
        print(f"ERROR de seguridad: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
