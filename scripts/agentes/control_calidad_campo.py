#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Control de calidad de ingesta de datos de campo (Fase 6).

SOLO VALIDA Y REPORTA. Este módulo no crea, simula ni imputa datos empíricos:
lo único que escribe son metadatos (codebook JSON), una plantilla CSV con sola
cabecera y, con --registrar, una línea SHA-256 en datos/checksums_sha256.txt.
Jamás escribe en datos/raw/.

Implementa los 4 niveles de PROTOCOLO_CONTROL_CALIDAD_E_INGESTA.md:

    Nivel 1  Estructura    columnas exactas, 14 filas, TRAB-01..TRAB-14 únicos, cero faltantes
    Nivel 2  Rangos        t_reg (0,120], t_vale (0,60], rsd/cpe [0,100], Likert enteros 1-5
    Nivel 3  Consistencia  score_ap, score_up, score_tam_total y nivel_satisfaccion (baremo)
    Nivel 4  Trazabilidad  SHA-256; registro en datos/checksums_sha256.txt (solo --registrar)

Además emite ADVERTENCIAS (no bloquean) de valores sospechosos para revisión
del tesista: filas duplicadas, varianza cero / straight-lining en Likert y
valores idénticos en más del 70 % de los sujetos.

Uso:
    python scripts/agentes/control_calidad_campo.py validar ARCHIVO.csv [--fase pretest|postest]
                                                     [--registrar] [--centros LISTA.txt] [--json]
    python scripts/agentes/control_calidad_campo.py pares PRETEST.csv POSTEST.csv [--json]
    python scripts/agentes/control_calidad_campo.py esquema [--salida RUTA] [--forzar]
    python scripts/agentes/control_calidad_campo.py plantilla [--fase pretest|postest|ambas] [--forzar]

Códigos de salida: 0 = sin errores, 1 = hallazgos bloqueantes, 2 = uso incorrecto.

Nota sobre Apps Script: la especificación de los formularios digitales y del
script de exportación ya existe en la bóveda
(06_METODOLOGIA_E_INSTRUMENTOS/expediente_juicio_expertos/
ESPECIFICACION_FORMULARIOS_DIGITALES_Y_SCRIPTS.md); este módulo no genera
código Apps Script adicional.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad  # noqa: E402

# ---------------------------------------------------------------------------
# Reglas (única fuente: de aquí se deriva también el codebook JSON)
# ---------------------------------------------------------------------------

N_SUJETOS = rutas.N_CENSAL  # 14
IDS_ESPERADOS = tuple(f"TRAB-{i:02d}" for i in range(1, N_SUJETOS + 1))
FASES = ("PRETEST", "POSTEST")
NIVELES_SATISFACCION = ("Bajo", "Medio", "Alto")
# Baremo institucional sobre score_tam_total: (mínimo, máximo, categoría)
BAREMO = ((10, 22, "Bajo"), (23, 36, "Medio"), (37, 50, "Alto"))
TOKENS_FALTANTE = {"", "na", "n/a", "nan", "null", "none", "nd", "-"}
UMBRAL_IDENTICOS = 0.70

ITEMS_AP = tuple(f"ap_{i:02d}" for i in range(1, 6))
ITEMS_UP = tuple(f"up_{i:02d}" for i in range(1, 6))
COLUMNAS = (
    "sujeto_id", "centro_acopio", "fase", "t_reg", "t_vale", "rsd", "cpe",
    *ITEMS_AP, "score_ap", *ITEMS_UP, "score_up", "score_tam_total",
    "nivel_satisfaccion",
)


@dataclass(frozen=True)
class ReglaColumna:
    """Regla de dominio de una columna (metadato del codebook)."""

    nombre: str
    tipo: str  # texto | decimal | entero
    escala: str
    minimo: float | None
    maximo: float | None
    min_incluido: bool
    max_incluido: bool
    descripcion: str
    dominio: tuple[str, ...] = ()
    derivada: str = ""


def _reglas() -> dict[str, ReglaColumna]:
    r: dict[str, ReglaColumna] = {}
    r["sujeto_id"] = ReglaColumna(
        "sujeto_id", "texto", "nominal", None, None, True, True,
        "Código unívoco anonimizado del trabajador (TRAB-01 a TRAB-14).",
        dominio=IDS_ESPERADOS)
    r["centro_acopio"] = ReglaColumna(
        "centro_acopio", "texto", "nominal", None, None, True, True,
        "Establecimiento sede de la medición (texto no vacío; lista oficial "
        "verificable con --centros).")
    r["fase"] = ReglaColumna(
        "fase", "texto", "nominal", None, None, True, True,
        "Momento de medición: PRETEST (O1) o POSTEST (O2).", dominio=FASES)
    r["t_reg"] = ReglaColumna(
        "t_reg", "decimal", "razón (minutos)", 0, 120, False, True,
        "Tiempo de registro de movimiento de vacunas, T_reg (D1, I1.1).")
    r["t_vale"] = ReglaColumna(
        "t_vale", "decimal", "razón (minutos)", 0, 60, False, True,
        "Tiempo de emisión del comprobante de salida / vale, T_vale (D1, I1.2).")
    r["rsd"] = ReglaColumna(
        "rsd", "decimal", "razón (porcentaje)", 0, 100, True, True,
        "Porcentaje de registros sin discrepancias, RSD (D2, I2.1).")
    r["cpe"] = ReglaColumna(
        "cpe", "decimal", "razón (porcentaje)", 0, 100, True, True,
        "Concordancia cantidad programada vs entregada, CPE (D2, I2.2).")
    for i, c in enumerate(ITEMS_AP, 1):
        r[c] = ReglaColumna(c, "entero", "ordinal Likert 1-5", 1, 5, True, True,
                            f"Reactivo {i} de Aceptación del proceso, AP (D3, I3.1, TAM).")
    for i, c in enumerate(ITEMS_UP, 1):
        r[c] = ReglaColumna(c, "entero", "ordinal Likert 1-5", 1, 5, True, True,
                            f"Reactivo {i} de Utilidad percibida, UP (D3, I3.2, TAM).")
    r["score_ap"] = ReglaColumna(
        "score_ap", "entero", "intervalar", 5, 25, True, True,
        "Suma de ap_01..ap_05.", derivada="suma(ap_01..ap_05)")
    r["score_up"] = ReglaColumna(
        "score_up", "entero", "intervalar", 5, 25, True, True,
        "Suma de up_01..up_05.", derivada="suma(up_01..up_05)")
    r["score_tam_total"] = ReglaColumna(
        "score_tam_total", "entero", "intervalar", 10, 50, True, True,
        "Puntuación TAM total = score_ap + score_up.", derivada="score_ap + score_up")
    r["nivel_satisfaccion"] = ReglaColumna(
        "nivel_satisfaccion", "texto", "ordinal", None, None, True, True,
        "Categoría según baremo: 10-22 Bajo, 23-36 Medio, 37-50 Alto.",
        dominio=NIVELES_SATISFACCION, derivada="baremo(score_tam_total)")
    assert set(r) == set(COLUMNAS)
    return {c: r[c] for c in COLUMNAS}  # orden canónico del codebook


REGLAS = _reglas()

# Columnas sobre las que se evalúa "valores idénticos en >70 % de sujetos"
# (se excluyen identificadores y columnas derivadas para reducir ruido).
_COLS_MEDIDAS = ("t_reg", "t_vale", "rsd", "cpe", *ITEMS_AP, *ITEMS_UP)


# ---------------------------------------------------------------------------
# Modelo de hallazgos
# ---------------------------------------------------------------------------

@dataclass
class Hallazgo:
    nivel: int
    codigo: str
    severidad: str  # "error" (bloquea) | "advertencia" (revisión del tesista)
    mensaje: str
    fila: int | None = None  # fila de datos, 1 = primera fila tras la cabecera
    columna: str | None = None
    sujeto_id: str | None = None

    def texto(self) -> str:
        donde = []
        if self.sujeto_id:
            donde.append(self.sujeto_id)
        elif self.fila is not None:
            donde.append(f"fila {self.fila}")
        if self.columna:
            donde.append(self.columna)
        pref = f"[N{self.nivel}/{self.codigo}]"
        return f"{pref} {' / '.join(donde) + ': ' if donde else ''}{self.mensaje}"


@dataclass
class Lectura:
    """CSV leído sin interpretar (todo cadena) para detectar faltantes con exactitud."""

    cabecera: list[str]
    filas: list[dict[str, str]]  # solo filas con el número correcto de celdas
    irregulares: list[tuple[int, int]] = field(default_factory=list)  # (fila, nº celdas)
    total_filas: int = 0
    tiene_bom: bool = False
    error_codificacion: str | None = None  # motivo si el archivo no es UTF-8 válido


# ---------------------------------------------------------------------------
# Lectura y utilidades (funciones puras)
# ---------------------------------------------------------------------------

def leer_csv(ruta: str | Path) -> Lectura:
    """Lee el CSV tal cual (texto). Ignora líneas totalmente vacías."""
    ruta = Path(ruta)
    crudo = ruta.read_bytes()
    tiene_bom = crudo.startswith(b"\xef\xbb\xbf")
    try:
        contenido = crudo.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        # Caso típico: CSV de Excel/Windows guardado en cp1252. Se reporta como
        # hallazgo de Nivel 1; no se adivina otra codificación ni se repara.
        motivo = (f"El archivo no es UTF-8 válido (byte 0x{crudo[exc.start]:02x} en la "
                  f"posición {exc.start}). Posible codificación ANSI/cp1252: en Excel use "
                  "'CSV UTF-8 (delimitado por comas)' y vuelva a exportar.")
        return Lectura([], [], [], 0, tiene_bom, motivo)
    lector = csv.reader(contenido.splitlines())
    try:
        cabecera = [c.strip() for c in next(lector)]
    except StopIteration:
        return Lectura([], [], [], 0, tiene_bom)
    filas: list[dict[str, str]] = []
    irregulares: list[tuple[int, int]] = []
    total = 0
    for celdas in lector:
        if not celdas or all(c == "" for c in celdas) and len(celdas) <= 1:
            continue
        total += 1
        if len(celdas) != len(cabecera):
            irregulares.append((total, len(celdas)))
            continue
        filas.append({c: v for c, v in zip(cabecera, celdas)})
    return Lectura(cabecera, filas, irregulares, total, tiene_bom)


def es_faltante(valor: str | None) -> bool:
    return valor is None or valor.strip().lower() in TOKENS_FALTANTE


def a_numero(valor: str | None) -> float | None:
    """Convierte a float finito o devuelve None (nunca adivina)."""
    if valor is None:
        return None
    try:
        x = float(valor.strip())
    except ValueError:
        return None
    return x if math.isfinite(x) else None


_RE_ENTERO = re.compile(r"[+-]?\d+")
_RE_ENTERO_DECIMAL = re.compile(r"[+-]?\d+\.0+")


def tiene_notacion_decimal(valor: str | None) -> bool:
    """True si el texto es un entero escrito con decimales nulos ('3.0', '3.00')."""
    return valor is not None and _RE_ENTERO_DECIMAL.fullmatch(valor.strip()) is not None


def a_entero(valor: str | None) -> int | None:
    """Entero por valor: acepta '3' y '3.0' (este último con advertencia en Nivel 2).

    Rechaza '3.5' y la notación exponencial ('1e0'), que nunca se interpreta.
    """
    if valor is None:
        return None
    v = valor.strip()
    if _RE_ENTERO.fullmatch(v):
        return int(v)
    if _RE_ENTERO_DECIMAL.fullmatch(v):
        return int(float(v))
    return None


def categoria_baremo(total: int) -> str | None:
    for lo, hi, cat in BAREMO:
        if lo <= total <= hi:
            return cat
    return None


def _en_rango(x: float, r: ReglaColumna) -> bool:
    if r.minimo is not None:
        if x < r.minimo or (x == r.minimo and not r.min_incluido):
            return False
    if r.maximo is not None:
        if x > r.maximo or (x == r.maximo and not r.max_incluido):
            return False
    return True


def _rotulo_rango(r: ReglaColumna) -> str:
    a = "[" if r.min_incluido else "("
    b = "]" if r.max_incluido else ")"
    return f"{a}{r.minimo:g}, {r.maximo:g}{b}"


def _sid(fila: dict[str, str]) -> str | None:
    v = fila.get("sujeto_id")
    return v.strip() if v and v.strip() else None


# ---------------------------------------------------------------------------
# Nivel 1: estructura
# ---------------------------------------------------------------------------

def _delimitador_sospechoso(cab: list[str]) -> str | None:
    """Detecta ';' o tabulador como separador cuando la cabecera quedó en 1 columna."""
    if len(cab) != 1:
        return None
    for simbolo, nombre in ((";", "punto y coma (;)"), ("\t", "tabulador")):
        partes = [p.strip() for p in cab[0].split(simbolo)]
        if len(partes) > 1 and len(set(partes) & set(COLUMNAS)) >= len(partes) / 2:
            return nombre
    return None


def nivel1_estructura(lec: Lectura, centros_validos: set[str] | None = None) -> list[Hallazgo]:
    h: list[Hallazgo] = []
    cab = lec.cabecera
    if lec.error_codificacion:
        return [Hallazgo(1, "CODIFICACION_INVALIDA", "error", lec.error_codificacion)]
    delim = _delimitador_sospechoso(cab)
    if delim:
        h.append(Hallazgo(1, "DELIMITADOR_INCORRECTO", "error",
                          f"La cabecera llegó en una sola columna: el archivo parece usar "
                          f"{delim} como separador y el protocolo exige coma. En Excel use "
                          "'CSV UTF-8 (delimitado por comas)' o cambie el separador de listas."))
    elif cab != list(COLUMNAS):
        faltan = [c for c in COLUMNAS if c not in cab]
        sobran = [c for c in cab if c not in COLUMNAS]
        dup = [c for c, n in Counter(cab).items() if n > 1]
        if faltan:
            h.append(Hallazgo(1, "COLUMNAS_FALTANTES", "error",
                              f"Faltan columnas del codebook: {', '.join(faltan)}."))
        if sobran:
            h.append(Hallazgo(1, "COLUMNAS_SOBRANTES", "error",
                              f"Columnas no previstas en el codebook: {', '.join(sobran)}."))
        if dup:
            h.append(Hallazgo(1, "COLUMNAS_DUPLICADAS", "error",
                              f"Columnas repetidas: {', '.join(dup)}."))
        if not faltan and not sobran and not dup:
            h.append(Hallazgo(1, "ORDEN_COLUMNAS", "error",
                              "Las columnas existen pero no están en el orden del codebook."))
    if lec.tiene_bom:
        h.append(Hallazgo(1, "BOM_UTF8", "advertencia",
                          "El archivo contiene BOM; el protocolo exige UTF-8 sin BOM."))
    for fila_n, n_celdas in lec.irregulares:
        h.append(Hallazgo(1, "CELDAS_IRREGULARES", "error",
                          f"Tiene {n_celdas} celdas; la cabecera define {len(cab)}.", fila=fila_n))

    if lec.total_filas != N_SUJETOS:
        h.append(Hallazgo(1, "N_FILAS", "error",
                          f"Se esperaban exactamente {N_SUJETOS} filas de datos y hay {lec.total_filas}."))

    # Identificadores
    if "sujeto_id" in cab:
        ids = [(i, _sid(f)) for i, f in enumerate(lec.filas, 1)]
        vistos = Counter(v for _, v in ids if v)
        for v, n in vistos.items():
            if n > 1:
                h.append(Hallazgo(1, "ID_DUPLICADO", "error",
                                  f"El identificador aparece {n} veces.", sujeto_id=v))
        for i, v in ids:
            if v and v not in IDS_ESPERADOS:
                h.append(Hallazgo(1, "ID_INVALIDO", "error",
                                  f"Identificador fuera de TRAB-01..TRAB-{N_SUJETOS:02d}.",
                                  fila=i, sujeto_id=v))
        ausentes = [i for i in IDS_ESPERADOS if i not in vistos]
        if ausentes and not lec.irregulares:
            h.append(Hallazgo(1, "ID_AUSENTES", "error",
                              f"Identificadores ausentes: {', '.join(ausentes)}."))

    # Faltantes (tolerancia cero)
    for i, f in enumerate(lec.filas, 1):
        for col in COLUMNAS:
            if col in f and es_faltante(f[col]):
                h.append(Hallazgo(1, "FALTANTE", "error",
                                  f"Valor faltante o nulo ({f[col]!r}); tolerancia cero.",
                                  fila=i, columna=col, sujeto_id=_sid(f)))

    # Centros de acopio (solo si se entrega la lista oficial)
    if centros_validos is not None:
        for i, f in enumerate(lec.filas, 1):
            c = f.get("centro_acopio", "").strip()
            if c and c not in centros_validos:
                h.append(Hallazgo(1, "CENTRO_NO_OFICIAL", "error",
                                  f"Centro no incluido en la lista oficial: {c!r}.",
                                  fila=i, columna="centro_acopio", sujeto_id=_sid(f)))
    return h


# ---------------------------------------------------------------------------
# Nivel 2: rangos y tipos
# ---------------------------------------------------------------------------

def nivel2_rangos(lec: Lectura, fase_esperada: str | None = None) -> list[Hallazgo]:
    h: list[Hallazgo] = []
    for i, f in enumerate(lec.filas, 1):
        sid = _sid(f)
        for col, r in REGLAS.items():
            if col not in f or es_faltante(f[col]):
                continue  # el faltante ya es error de Nivel 1
            v = f[col].strip()
            if r.tipo == "texto":
                if col == "sujeto_id":
                    continue  # validado en Nivel 1
                if r.dominio and v not in r.dominio:
                    h.append(Hallazgo(2, "DOMINIO", "error",
                                      f"Valor {v!r} fuera del dominio {list(r.dominio)}.",
                                      fila=i, columna=col, sujeto_id=sid))
                elif col == "fase" and fase_esperada and v != fase_esperada:
                    h.append(Hallazgo(2, "FASE_INCOHERENTE", "error",
                                      f"La fase es {v!r} pero el archivo corresponde a {fase_esperada}.",
                                      fila=i, columna=col, sujeto_id=sid))
                continue
            x = a_numero(v)
            if x is None:
                pista = " (¿coma decimal?)" if "," in v else ""
                h.append(Hallazgo(2, "NO_NUMERICO", "error",
                                  f"Valor no numérico: {v!r}{pista}.",
                                  fila=i, columna=col, sujeto_id=sid))
                continue
            if r.tipo == "entero":
                if a_entero(v) is None:
                    h.append(Hallazgo(2, "NO_ENTERO", "error",
                                      f"Se exige un entero y se recibió {v!r}.",
                                      fila=i, columna=col, sujeto_id=sid))
                    continue
                if tiene_notacion_decimal(v):
                    h.append(Hallazgo(2, "ENTERO_CON_DECIMALES", "advertencia",
                                      f"Entero escrito con decimales ({v!r}); se interpreta "
                                      f"como {int(x)}. Corregir la exportación para que sea {int(x)}.",
                                      fila=i, columna=col, sujeto_id=sid))
            if not _en_rango(x, r):
                h.append(Hallazgo(2, "FUERA_DE_RANGO", "error",
                                  f"Valor {v} fuera del rango {_rotulo_rango(r)}.",
                                  fila=i, columna=col, sujeto_id=sid))
    return h


# ---------------------------------------------------------------------------
# Nivel 3: consistencia aritmética y categorial
# ---------------------------------------------------------------------------

def _suma_items(f: dict[str, str], items: tuple[str, ...]) -> int | None:
    vals = [a_entero(f.get(c)) for c in items]
    if any(v is None or not 1 <= v <= 5 for v in vals):
        return None
    return sum(vals)  # type: ignore[arg-type]


def nivel3_consistencia(lec: Lectura) -> list[Hallazgo]:
    h: list[Hallazgo] = []
    for i, f in enumerate(lec.filas, 1):
        sid = _sid(f)
        esperado_ap = _suma_items(f, ITEMS_AP)
        esperado_up = _suma_items(f, ITEMS_UP)
        s_ap, s_up = a_entero(f.get("score_ap")), a_entero(f.get("score_up"))
        s_tam = a_entero(f.get("score_tam_total"))

        if esperado_ap is not None and s_ap is not None and s_ap != esperado_ap:
            h.append(Hallazgo(3, "SCORE_AP", "error",
                              f"score_ap={s_ap} pero la suma de ap_01..ap_05 es {esperado_ap}.",
                              fila=i, columna="score_ap", sujeto_id=sid))
        if esperado_up is not None and s_up is not None and s_up != esperado_up:
            h.append(Hallazgo(3, "SCORE_UP", "error",
                              f"score_up={s_up} pero la suma de up_01..up_05 es {esperado_up}.",
                              fila=i, columna="score_up", sujeto_id=sid))
        if s_ap is not None and s_up is not None and s_tam is not None and s_tam != s_ap + s_up:
            h.append(Hallazgo(3, "SCORE_TAM", "error",
                              f"score_tam_total={s_tam} pero score_ap + score_up = {s_ap + s_up}.",
                              fila=i, columna="score_tam_total", sujeto_id=sid))
        nivel = (f.get("nivel_satisfaccion") or "").strip()
        if s_tam is not None and nivel in NIVELES_SATISFACCION:
            cat = categoria_baremo(s_tam)
            if cat is not None and cat != nivel:
                h.append(Hallazgo(3, "BAREMO", "error",
                                  f"nivel_satisfaccion={nivel!r} pero score_tam_total={s_tam} "
                                  f"corresponde a {cat!r} (10-22 Bajo, 23-36 Medio, 37-50 Alto).",
                                  fila=i, columna="nivel_satisfaccion", sujeto_id=sid))
    return h


# ---------------------------------------------------------------------------
# Valores sospechosos (ADVERTENCIAS: no bloquean)
# ---------------------------------------------------------------------------

def advertencias_sospechosas(lec: Lectura) -> list[Hallazgo]:
    h: list[Hallazgo] = []
    filas = lec.filas
    if len(lec.cabecera) <= 1:  # delimitador erróneo: las heurísticas serían ruido
        return h

    # 1) Filas duplicadas (todas las columnas salvo el identificador)
    por_contenido: dict[tuple, list[int]] = {}
    for i, f in enumerate(filas, 1):
        clave = tuple(f.get(c, "").strip() for c in COLUMNAS if c != "sujeto_id")
        por_contenido.setdefault(clave, []).append(i)
    for idxs in por_contenido.values():
        if len(idxs) > 1:
            ids = ", ".join(_sid(filas[i - 1]) or f"fila {i}" for i in idxs)
            h.append(Hallazgo(1, "FILA_DUPLICADA", "advertencia",
                              f"Filas con contenido idéntico (salvo sujeto_id): {ids}. "
                              "Verificar que no sea una copia accidental."))

    # 2) Varianza cero y straight-lining por sujeto
    for i, f in enumerate(filas, 1):
        ap = [a_entero(f.get(c)) for c in ITEMS_AP]
        up = [a_entero(f.get(c)) for c in ITEMS_UP]
        if any(v is None for v in ap + up):
            continue
        sid = _sid(f)
        todos = ap + up
        if len(set(todos)) == 1:
            h.append(Hallazgo(2, "VARIANZA_CERO_LIKERT", "advertencia",
                              f"Las 10 respuestas Likert son idénticas ({todos[0]}); "
                              "posible respuesta automática.", fila=i, sujeto_id=sid))
            continue
        patrones = []
        if len(set(ap)) == 1:
            patrones.append(f"bloque AP constante ({ap[0]})")
        if len(set(up)) == 1:
            patrones.append(f"bloque UP constante ({up[0]})")
        for nombre, bloque in (("AP", ap), ("UP", up)):
            if bloque in ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]):
                patrones.append(f"bloque {nombre} en secuencia monótona {bloque}")
        if patrones:
            h.append(Hallazgo(2, "STRAIGHT_LINING", "advertencia",
                              "Patrón de respuesta uniforme: " + "; ".join(patrones) + ".",
                              fila=i, sujeto_id=sid))

    # 3) Valores idénticos en >70 % de sujetos por columna medida
    for col in _COLS_MEDIDAS:
        vals = [a_numero(f.get(col)) for f in filas]
        vals = [v for v in vals if v is not None]
        if len(vals) < 2:
            continue
        valor, n = Counter(vals).most_common(1)[0]
        if n / len(vals) > UMBRAL_IDENTICOS:
            h.append(Hallazgo(2, "IDENTICOS_70", "advertencia",
                              f"El valor {valor:g} se repite en {n} de {len(vals)} sujetos "
                              f"({n / len(vals):.0%} > {UMBRAL_IDENTICOS:.0%}).", columna=col))
    return h


# ---------------------------------------------------------------------------
# Nivel 4: trazabilidad SHA-256
# ---------------------------------------------------------------------------

RUTA_CHECKSUMS = rutas.DATOS / "checksums_sha256.txt"
_ENCABEZADO_CHECKSUMS = (
    "# Firmas SHA-256 de archivos de datos de campo validados (formato: <sha256>  <ruta>)\n"
    "# Generado por scripts/agentes/control_calidad_campo.py --registrar\n"
)


def _nombre_registro(ruta: Path) -> str:
    """Ruta relativa al workspace (separadores '/') o, fuera de él, la ruta absoluta.

    Usar la ruta completa evita que dos archivos homónimos de carpetas distintas
    colisionen en el registro de checksums.
    """
    absoluta = ruta.resolve()
    try:
        return absoluta.relative_to(rutas.RAIZ.resolve()).as_posix()
    except ValueError:
        return absoluta.as_posix()


def leer_checksums(ruta_checksums: Path) -> dict[str, str]:
    reg: dict[str, str] = {}
    if not ruta_checksums.exists():
        return reg
    for linea in ruta_checksums.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        partes = linea.split(None, 1)
        if len(partes) == 2:
            reg[partes[1].strip()] = partes[0].lower()
    return reg


def _asegurar_salida(ruta: Path) -> Path:
    """Guarda de escritura: rutas inmutables y datos/raw/ quedan vedadas."""
    destino = seguridad.asegurar_escritura_permitida(ruta)
    raw = rutas.DATOS_RAW.resolve(strict=False)
    try:
        destino.relative_to(raw)
    except ValueError:
        return destino
    raise seguridad.EscrituraProhibida(
        f"Este módulo nunca escribe en datos/raw/: {destino}")


def nivel4_trazabilidad(archivo: Path, registrar: bool, hay_errores: bool,
                        ruta_checksums: Path = RUTA_CHECKSUMS) -> tuple[dict, list[Hallazgo]]:
    h: list[Hallazgo] = []
    sha = seguridad.sha256_archivo(archivo)
    nombre = _nombre_registro(archivo)
    previos = leer_checksums(ruta_checksums)
    info = {"sha256": sha, "nombre_registro": nombre, "estado": "no_registrado", "registrado": False}

    previo = previos.get(nombre)
    if previo is not None and previo != sha:
        info["estado"] = "discrepancia"
        info["sha256_registrado"] = previo
        h.append(Hallazgo(4, "ALERTA_INTEGRIDAD", "error",
                          f"El SHA-256 actual no coincide con el registrado para {nombre}: "
                          f"{sha[:16]}… vs {previo[:16]}…. Archivo modificado tras su registro."))
        return info, h
    if previo == sha:
        info["estado"] = "coincide_con_registro"
        info["registrado"] = True
        return info, h
    if registrar:
        if hay_errores:
            info["estado"] = "no_registrado_por_errores"
            h.append(Hallazgo(4, "REGISTRO_OMITIDO", "advertencia",
                              "No se registra el checksum: el archivo no superó los niveles 1-3."))
        else:
            destino = _asegurar_salida(ruta_checksums)
            destino.parent.mkdir(parents=True, exist_ok=True)
            nuevo = not destino.exists()
            with open(destino, "a", encoding="utf-8", newline="\n") as fh:
                if nuevo:
                    fh.write(_ENCABEZADO_CHECKSUMS)
                fh.write(f"{sha}  {nombre}\n")
            info["estado"] = "registrado"
            info["registrado"] = True
    return info, h


# ---------------------------------------------------------------------------
# Orquestación de 'validar' y 'pares'
# ---------------------------------------------------------------------------

def inferir_fase(archivo: Path, lec: Lectura, fase_cli: str | None) -> str | None:
    if fase_cli:
        return fase_cli.upper()
    nombre = archivo.name.lower()
    if "pretest" in nombre:
        return "PRETEST"
    if "postest" in nombre or "posttest" in nombre:
        return "POSTEST"
    fases = {f.get("fase", "").strip() for f in lec.filas} - {""}
    if len(fases) == 1 and next(iter(fases)) in FASES:
        return next(iter(fases))
    return None


def validar_archivo(archivo: Path, fase: str | None = None, registrar: bool = False,
                    centros_validos: set[str] | None = None,
                    ruta_checksums: Path = RUTA_CHECKSUMS) -> dict:
    lec = leer_csv(archivo)
    fase_res = inferir_fase(archivo, lec, fase)
    hallazgos: list[Hallazgo] = []
    hallazgos += nivel1_estructura(lec, centros_validos)
    if not lec.error_codificacion:  # sin texto legible no hay niveles 2-3 que evaluar
        hallazgos += nivel2_rangos(lec, fase_res)
        hallazgos += nivel3_consistencia(lec)
        hallazgos += advertencias_sospechosas(lec)
    hay_errores = any(x.severidad == "error" for x in hallazgos)
    info4, h4 = nivel4_trazabilidad(archivo, registrar, hay_errores, ruta_checksums)
    hallazgos += h4
    errores = [x for x in hallazgos if x.severidad == "error"]
    avisos = [x for x in hallazgos if x.severidad == "advertencia"]
    niveles = {
        str(n): {"errores": sum(1 for x in errores if x.nivel == n),
                 "advertencias": sum(1 for x in avisos if x.nivel == n)}
        for n in (1, 2, 3, 4)
    }
    if centros_validos is None:
        avisos.append(Hallazgo(1, "CENTROS_SIN_LISTA", "advertencia",
                               "[VERIFICAR: no se entregó la lista oficial de centros de acopio "
                               "(--centros); solo se comprobó que el campo no esté vacío]."))
    return {
        "archivo": str(archivo),
        "fase": fase_res,
        "filas_datos": lec.total_filas,
        "estado": "RECHAZADO" if errores else "APROBADO",
        "niveles": niveles,
        "trazabilidad": info4,
        "errores": [asdict(x) for x in errores],
        "advertencias": [asdict(x) for x in avisos],
    }


def comprobar_pares(pre: Path, post: Path) -> dict:
    """Correspondencia pretest/postest por sujeto_id (no genera la matriz pareada)."""
    lp, lq = leer_csv(pre), leer_csv(post)
    h: list[Hallazgo] = []
    for etiqueta, lec in (("PRETEST", lp), ("POSTEST", lq)):
        if lec.error_codificacion:
            h.append(Hallazgo(1, "CODIFICACION_INVALIDA", "error", f"{etiqueta}: {lec.error_codificacion}"))

    def ids_de(lec: Lectura, etiqueta: str) -> dict[str, dict[str, str]]:
        salida: dict[str, dict[str, str]] = {}
        for i, f in enumerate(lec.filas, 1):
            sid = _sid(f)
            if not sid:
                h.append(Hallazgo(1, "ID_VACIO", "error", f"{etiqueta}: sujeto_id vacío.", fila=i))
            elif sid in salida:
                h.append(Hallazgo(1, "ID_DUPLICADO", "error", f"{etiqueta}: identificador repetido.", sujeto_id=sid))
            else:
                salida[sid] = f
        return salida

    a, b = ids_de(lp, "PRETEST"), ids_de(lq, "POSTEST")
    for sid in sorted(set(a) - set(b)):
        h.append(Hallazgo(1, "SIN_POSTEST", "error", "Existe en el pretest y no en el postest.", sujeto_id=sid))
    for sid in sorted(set(b) - set(a)):
        h.append(Hallazgo(1, "SIN_PRETEST", "error", "Existe en el postest y no en el pretest.", sujeto_id=sid))
    for etiqueta, dic, esperada in (("PRETEST", a, "PRETEST"), ("POSTEST", b, "POSTEST")):
        malas = sorted({f.get("fase", "").strip() for f in dic.values()} - {esperada})
        if malas:
            h.append(Hallazgo(2, "FASE_INCOHERENTE", "error",
                              f"El archivo {etiqueta} contiene valores de fase {malas}; se esperaba {esperada}."))
    for sid in sorted(set(a) & set(b)):
        ca, cb = a[sid].get("centro_acopio", "").strip(), b[sid].get("centro_acopio", "").strip()
        if ca != cb:
            h.append(Hallazgo(1, "CENTRO_DISTINTO", "advertencia",
                              f"Centro distinto entre fases ({ca!r} vs {cb!r}); confirmar con el cuaderno de campo.",
                              sujeto_id=sid))
    if pre.resolve() == post.resolve() or seguridad.sha256_archivo(pre) == seguridad.sha256_archivo(post):
        h.append(Hallazgo(4, "ARCHIVOS_IDENTICOS", "error",
                          "El pretest y el postest tienen el mismo contenido (mismo SHA-256)."))
    errores = [x for x in h if x.severidad == "error"]
    return {
        "pretest": str(pre), "postest": str(post),
        "sujetos_pretest": len(a), "sujetos_postest": len(b),
        "sujetos_pareados": len(set(a) & set(b)),
        "estado": "RECHAZADO" if errores else "APROBADO",
        "errores": [asdict(x) for x in errores],
        "advertencias": [asdict(x) for x in h if x.severidad == "advertencia"],
    }


# ---------------------------------------------------------------------------
# Esquema (codebook) y plantilla
# ---------------------------------------------------------------------------

def construir_codebook() -> dict:
    """Codebook derivado de las reglas. Es metadato: no contiene datos de campo."""
    cols = []
    for pos, (nombre, r) in enumerate(REGLAS.items(), 1):
        c = {
            "posicion": pos, "nombre": nombre, "tipo": r.tipo, "escala": r.escala,
            "obligatorio": True, "descripcion": r.descripcion,
        }
        if r.minimo is not None:
            c["rango"] = {"minimo": r.minimo, "maximo": r.maximo,
                          "minimo_incluido": r.min_incluido, "maximo_incluido": r.max_incluido,
                          "notacion": _rotulo_rango(r)}
        if r.dominio:
            c["dominio"] = list(r.dominio)
        if r.derivada:
            c["derivada_de"] = r.derivada
        cols.append(c)
    return {
        "tipo": "codebook_datos_campo",
        "aviso": "Metadato de estructura; no contiene datos empíricos.",
        "tesis": rutas.TITULO_OFICIAL,
        "diseno": "Preexperimental O1 -> X -> O2, un solo grupo",
        "fuente_reglas": "06_METODOLOGIA_E_INSTRUMENTOS/protocolos_calidad_datos/PROTOCOLO_CONTROL_CALIDAD_E_INGESTA.md",
        "codificacion": "UTF-8 sin BOM, separador coma, cabecera en la primera línea",
        "n_filas_por_archivo": N_SUJETOS,
        "identificadores": list(IDS_ESPERADOS),
        "fases": list(FASES),
        "faltantes_tolerados": 0,
        "baremo_satisfaccion": [{"minimo": lo, "maximo": hi, "categoria": c} for lo, hi, c in BAREMO],
        "advertencias_no_bloqueantes": [
            "fila duplicada (salvo sujeto_id)", "varianza cero en Likert por sujeto",
            "straight-lining", f"valores idénticos en >{UMBRAL_IDENTICOS:.0%} de sujetos"],
        "columnas": cols,
    }


def escribir_json(ruta: Path, contenido: dict, forzar: bool = False) -> Path:
    destino = _asegurar_salida(ruta)
    if destino.exists() and not forzar:
        raise FileExistsError(f"Ya existe {destino}; use --forzar para regenerar el metadato.")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(contenido, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return destino


def escribir_plantilla(fase: str, carpeta: Path, forzar: bool = False) -> Path:
    """CSV con SOLO la cabecera (cero filas de datos)."""
    destino = _asegurar_salida(carpeta / f"plantilla_bd_sivac_{fase.lower()}.csv")
    if destino.exists() and not forzar:
        raise FileExistsError(f"Ya existe {destino}; use --forzar para regenerar la plantilla.")
    destino.parent.mkdir(parents=True, exist_ok=True)
    with open(destino, "w", encoding="utf-8", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerow(COLUMNAS)
    return destino


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _imprimir_informe(inf: dict) -> None:
    print(f"Archivo : {inf['archivo']}")
    print(f"Fase    : {inf['fase'] or '[VERIFICAR: no determinada]'}   Filas de datos: {inf['filas_datos']}")
    for n, nombre in ((1, "Estructura"), (2, "Rangos"), (3, "Consistencia"), (4, "Trazabilidad")):
        d = inf["niveles"][str(n)]
        marca = "OK " if d["errores"] == 0 else "FALLA"
        print(f"  Nivel {n} {nombre:<13} {marca}  errores={d['errores']}  advertencias={d['advertencias']}")
    t = inf["trazabilidad"]
    print(f"  SHA-256 {t['sha256']}  [{t['estado']}]")
    for e in inf["errores"]:
        print("  ERROR      " + Hallazgo(**e).texto())
    for a in inf["advertencias"]:
        print("  ADVERTENCIA " + Hallazgo(**a).texto())
    print(f"ESTADO: {inf['estado']}")


def _imprimir_pares(inf: dict) -> None:
    print(f"Pretest: {inf['pretest']}\nPostest: {inf['postest']}")
    print(f"Sujetos pretest={inf['sujetos_pretest']} postest={inf['sujetos_postest']} "
          f"pareados={inf['sujetos_pareados']}")
    for e in inf["errores"]:
        print("  ERROR      " + Hallazgo(**e).texto())
    for a in inf["advertencias"]:
        print("  ADVERTENCIA " + Hallazgo(**a).texto())
    print(f"ESTADO: {inf['estado']}")


class UsoIncorrecto(Exception):
    """Argumento de entrada inválido (código de salida 2)."""


def _cargar_centros(ruta: str | None) -> set[str] | None:
    if not ruta:
        return None
    archivo = Path(ruta)
    if not archivo.is_file():
        raise UsoIncorrecto(f"No existe el archivo de centros: {archivo}")
    try:
        lineas = archivo.read_text(encoding="utf-8-sig").splitlines()
    except UnicodeDecodeError as exc:
        raise UsoIncorrecto(f"La lista de centros no es UTF-8 válido: {archivo} ({exc.reason}).") from exc
    except OSError as exc:
        raise UsoIncorrecto(f"No se pudo leer la lista de centros {archivo}: {exc}") from exc
    return {ln.strip() for ln in lineas if ln.strip() and not ln.startswith("#")}


def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="control_calidad_campo.py",
        description="Control de calidad de datos de campo SIVAC (solo valida y reporta).")
    sub = p.add_subparsers(dest="orden", required=True)

    v = sub.add_parser("validar", help="Valida un CSV pretest/postest (niveles 1-4).")
    v.add_argument("archivo")
    v.add_argument("--fase", choices=["pretest", "postest"], help="Fase esperada (si no, se infiere).")
    v.add_argument("--registrar", action="store_true",
                   help="Registra el SHA-256 en datos/checksums_sha256.txt si el archivo aprueba.")
    v.add_argument("--centros", help="Archivo de texto con los centros de acopio oficiales (uno por línea).")
    v.add_argument("--checksums", help="Ruta alternativa del registro de checksums.")
    v.add_argument("--json", action="store_true", help="Salida JSON.")

    q = sub.add_parser("pares", help="Comprueba la correspondencia pretest/postest por sujeto_id.")
    q.add_argument("pretest")
    q.add_argument("postest")
    q.add_argument("--json", action="store_true")

    e = sub.add_parser("esquema", help="Escribe el codebook JSON (metadato).")
    e.add_argument("--salida", help="Por defecto datos/schemas/codebook.json")
    e.add_argument("--forzar", action="store_true")
    e.add_argument("--json", action="store_true")

    t = sub.add_parser("plantilla", help="Escribe un CSV vacío con solo la cabecera.")
    t.add_argument("--fase", choices=["pretest", "postest", "ambas"], default="ambas")
    t.add_argument("--carpeta", help="Por defecto datos/plantillas/")
    t.add_argument("--forzar", action="store_true")
    t.add_argument("--json", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    seguridad.configurar_utf8()
    try:
        args = construir_parser().parse_args(argv)
    except SystemExit as exc:  # argparse ya imprimió el uso
        return 2 if exc.code not in (0, None) else 0

    try:
        if args.orden == "validar":
            archivo = Path(args.archivo)
            if not archivo.is_file():
                print(f"No existe el archivo: {archivo}", file=sys.stderr)
                return 2
            inf = validar_archivo(
                archivo, args.fase, args.registrar, _cargar_centros(args.centros),
                Path(args.checksums) if args.checksums else RUTA_CHECKSUMS)
            if args.json:
                print(json.dumps(inf, ensure_ascii=False, indent=2))
            else:
                _imprimir_informe(inf)
            return 1 if inf["estado"] == "RECHAZADO" else 0

        if args.orden == "pares":
            for r in (args.pretest, args.postest):
                if not Path(r).is_file():
                    print(f"No existe el archivo: {r}", file=sys.stderr)
                    return 2
            inf = comprobar_pares(Path(args.pretest), Path(args.postest))
            if args.json:
                print(json.dumps(inf, ensure_ascii=False, indent=2))
            else:
                _imprimir_pares(inf)
            return 1 if inf["estado"] == "RECHAZADO" else 0

        if args.orden == "esquema":
            destino = escribir_json(Path(args.salida) if args.salida else rutas.DATOS_SCHEMAS / "codebook.json",
                                    construir_codebook(), args.forzar)
            print(json.dumps({"escrito": str(destino)}, ensure_ascii=False) if args.json
                  else f"Codebook escrito en {destino}")
            return 0

        if args.orden == "plantilla":
            carpeta = Path(args.carpeta) if args.carpeta else rutas.DATOS_PLANTILLAS
            fases = ("pretest", "postest") if args.fase == "ambas" else (args.fase,)
            escritas = [str(escribir_plantilla(f, carpeta, args.forzar)) for f in fases]
            if args.json:
                print(json.dumps({"escritas": escritas}, ensure_ascii=False))
            else:
                for r in escritas:
                    print(f"Plantilla (solo cabecera) escrita en {r}")
            return 0
    except UsoIncorrecto as exc:
        print(f"ERROR DE USO: {exc}", file=sys.stderr)
        return 2
    except (seguridad.EscrituraProhibida, FileExistsError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:  # entrada ilegible (permisos, ruta inválida): no es un rechazo de datos
        print(f"ERROR DE ENTRADA/SALIDA: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
