#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB (Squad B) - Validez de contenido por juicio de expertos.

Modelo vigente: certificado Fany 2024 (DEC-015). Cada item se califica con tres
criterios dicotomicos (Pertinencia, Relevancia y Claridad), cada uno con marca
de Si (1) o No (0). Alcance de un solo instrumento (DEC-020): el certificado
cubre los 8 items de la Modalidad A del Instrumento N. 03 (AP-01 a AP-04 y
UP-01 a UP-04). Los Instrumentos N. 01 y N. 02 no se someten a juicio de
contenido.

Calcula, a partir de matrices de calificaciones REALES entregadas por los jueces:

  * V de Aiken por item y criterio, con IC 95 % (metodo de puntuacion de Wilson).
  * Indice de validez de contenido: I-CVI por item/criterio, S-CVI/Ave y S-CVI/UA.
  * W de Kendall (opcional, exige >= 3 jueces).
  * Significancia de V bajo la hipotesis nula de categorias equiprobables
    (distribucion exacta, sin tablas transcritas).
  * Decision por item (mantener / modificar / eliminar) y por instrumento
    (aplicable sin modificar / previa modificacion / no aplicable).
  * Tablas en Markdown (estilo APA 7) y un .xlsx con formulas visibles.

Entrada (CSV o XLSX, formato largo): columnas
    juez, item, criterio (pertinencia|relevancia|claridad), puntaje (0 = No, 1 = Si)

Formulas
--------
V de Aiken (Aiken, 1985), con l = 0 (puntaje minimo) y c = 2 categorias:
    S = sum_j (s_j - l)              V = S / (n * (c - 1))
Con criterios dicotomicos la formula se reduce a V = S / n. Con tres jueces, V
solo puede tomar cuatro valores: 0.000, 0.333, 0.667 y 1.000. El umbral de 0.80
exige unanimidad perfecta de los tres jueces en cada item. No es un defecto del
modelo: es su consecuencia aritmetica y se declara en toda tabla o figura que
reporte V.

IC 95 % de V (Penfield y Giacobbi, 2004; limites de puntuacion de Wilson),
con N = n (c - 1) = n, z = 1.96:
    L = [2 N V + z^2 - z sqrt(4 N V (1 - V) + z^2)] / [2 (N + z^2)]
    U = [2 N V + z^2 + z sqrt(4 N V (1 - V) + z^2)] / [2 (N + z^2)]
    (equivale al intervalo de Wilson de una proporcion V con N ensayos).
I-CVI (Lynn, 1986; Polit y Beck, 2006): proporcion de jueces que marcan Si.
    S-CVI/Ave = media de los I-CVI;  S-CVI/UA = proporcion de items con I-CVI = 1.
W de Kendall con correccion por empates (m jueces, n items):
    W = 12 S / (m^2 (n^3 - n) - m sum_j T_j),  T_j = sum (t^3 - t) por juez,
    S = sum (R_i - R_media)^2;  chi2 = m (n - 1) W,  gl = n - 1.
Significancia de V: p = P(S_nula >= S_obs), con S_nula = suma de n puntuaciones
    independientes uniformes en {0,...,c-1} (categorias equiprobables), calculada
    por convolucion exacta con enteros. El V critico es el menor V con p <= alfa
    (unilateral). Con c = 2 y tres jueces el menor valor p alcanzable es 0.125,
    de modo que ninguna V resulta significativa al 5 % con esa configuracion. Son
    valores CALCULADOS, no transcritos de la tabla impresa de Aiken (1985).

Umbrales del proyecto: V >= 0.80 e I-CVI >= 0.80. Con tres jueces y c = 2 ambos
umbrales exigen unanimidad: V = 1.00 e I-CVI = 1.00.
Las reglas de decision por item/instrumento son reglas operativas de este modulo
(parametrizables), no una prescripcion de la literatura.

Uso:
    python scripts/agentes/validez_contenido.py plantilla [--salida CSV] [--forzar]
    python scripts/agentes/validez_contenido.py calcular ENTRADA [--hoja H] [--md RUTA]
                                                 [--xlsx RUTA] [--json] [--forzar]
    python scripts/agentes/validez_contenido.py tabla-critica
                                                 [--jueces-min 3 --jueces-max 10] [--json]

Codigos de salida: 0 ok (instrumento aplicable sin modificar), 1 hallazgos/fallos
(datos ausentes o invalidos, items por modificar/eliminar), 2 uso incorrecto.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import unicodedata
from dataclasses import asdict, dataclass, field
from datetime import datetime
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad  # noqa: E402

# --- Constantes -----------------------------------------------------------------
# Modelo Fany 2024 (DEC-015): tres criterios dicotomicos Si/No. El valor
# favorable es 1 (Si) y el desfavorable es 0 (No).
CRITERIOS = ("pertinencia", "relevancia", "claridad")
ETIQUETAS = {
    "pertinencia": "Pertinencia",
    "relevancia": "Relevancia",
    "claridad": "Claridad",
}
COLUMNAS = ("juez", "item", "criterio", "puntaje")
C_CATEGORIAS = 2
L_MINIMO = 0
CORTE_APROBACION = 1  # I-CVI: solo la marca de Si cuenta como acuerdo favorable
Z_95 = 1.959963984540054  # cuantil normal 0.975
# ADVERTENCIA ARITMETICA (no alterar sin nueva decision metodologica):
# Con criterios dicotomicos (c = 2) y n = 3 jueces, V = S / [n(c-1)] se reduce a
# V = S / n. Por tanto V solo puede tomar cuatro valores: 0.000, 0.333, 0.667 y
# 1.000. El umbral de 0.80 exige unanimidad perfecta de los tres jueces en cada
# item. Esto no es un defecto a corregir: es la consecuencia aritmetica del
# modelo Fany 2024 (DEC-015) y debe declararse en toda tabla o figura que
# reporte V.
UMBRAL_V = 0.80
UMBRAL_IVC = 0.80
UMBRAL_ELIMINAR_V = 0.50  # regla operativa: V del item por debajo => eliminar
UMBRAL_ELIMINAR_RELEVANCIA = 0.50  # regla operativa: I-CVI de relevancia por debajo => eliminar
EPS = 1e-9
PLANTILLA_DEFECTO = rutas.DATOS_PLANTILLAS / "validez_contenido_captura.csv"


class DatosInvalidos(ValueError):
    """La matriz de calificaciones no existe, está vacía o es inconsistente."""


# --- Modelo de resultados -------------------------------------------------------
@dataclass
class ResultadoCelda:
    item: str
    criterio: str
    n: int
    s: int
    v: float
    ic_inf: float
    ic_sup: float
    p_exacto: float
    ivc: float
    cumple: bool


@dataclass
class ResultadoItem:
    item: str
    v: float
    ivc: float
    criterios_fallidos: list[str]
    decision: str
    motivo: str


@dataclass
class ResultadoInstrumento:
    n_jueces: int
    n_items: int
    criterios: list[str]
    v_global: float
    s_cvi_ave: float
    s_cvi_ua: float
    por_criterio: dict
    kendall: dict
    decision: str
    motivo: str
    celdas: list[ResultadoCelda] = field(default_factory=list)
    items: list[ResultadoItem] = field(default_factory=list)
    advertencias: list[str] = field(default_factory=list)
    fuente: dict = field(default_factory=dict)


# --- Funciones puras: estadistica -----------------------------------------------
def v_aiken(puntajes: list[int], c: int = C_CATEGORIAS, l: int = L_MINIMO) -> float:
    """V de Aiken = S / (n (c-1)), S = sum (s - l). Con c = 2 y l = 0: V = S / n."""
    n = len(puntajes)
    if n == 0:
        raise DatosInvalidos("V de Aiken requiere al menos un juez.")
    return sum(s - l for s in puntajes) / (n * (c - 1))


def ic_wilson_v(v: float, n: int, c: int = C_CATEGORIAS, z: float = Z_95) -> tuple[float, float]:
    """IC de V por puntuacion de Wilson (Penfield y Giacobbi, 2004), N = n (c-1)."""
    big_n = n * (c - 1)
    raiz = z * math.sqrt(max(4 * big_n * v * (1 - v) + z * z, 0.0))
    den = 2 * (big_n + z * z)
    inf = (2 * big_n * v + z * z - raiz) / den
    sup = (2 * big_n * v + z * z + raiz) / den
    return max(0.0, inf), min(1.0, sup)


def ivc_item(puntajes: list[int], corte: int = CORTE_APROBACION) -> float:
    """I-CVI: proporcion de jueces con marca de Si (puntaje >= 1)."""
    return sum(1 for s in puntajes if s >= corte) / len(puntajes)


def _distribucion_nula(n: int, c: int) -> list[Fraction]:
    """P(S = k), k = 0..n(c-1), con n puntuaciones uniformes en {0..c-1} (exacta)."""
    dist = [Fraction(1)]
    for _ in range(n):
        nueva = [Fraction(0)] * (len(dist) + c - 1)
        for k, p in enumerate(dist):
            for d in range(c):
                nueva[k + d] += p / c
        dist = nueva
    return dist


def p_exacto_v(s: int, n: int, c: int = C_CATEGORIAS) -> float:
    """p unilateral = P(S_nula >= s) bajo categorias equiprobables."""
    dist = _distribucion_nula(n, c)
    return float(sum(dist[max(s, 0):]))


def v_critico(n: int, c: int = C_CATEGORIAS, alfa: float = 0.05) -> float | None:
    """Menor V significativo (unilateral) por distribucion nula exacta; None si inalcanzable."""
    dist = _distribucion_nula(n, c)
    cola = Fraction(0)
    critico = None
    for s in range(len(dist) - 1, -1, -1):
        cola += dist[s]
        if cola <= Fraction(alfa).limit_denominator(1_000_000):
            critico = s
        else:
            break
    return None if critico is None else critico / (n * (c - 1))


def tabla_v_critico(c: int = C_CATEGORIAS, n_min: int = 3, n_max: int = 10,
                    alfas: tuple[float, ...] = (0.05, 0.01, 0.001)) -> list[dict]:
    filas = []
    for n in range(n_min, n_max + 1):
        fila = {"n": n}
        for a in alfas:
            vc = v_critico(n, c, a)
            fila[f"alfa_{a}"] = None if vc is None else round(vc, 4)
        filas.append(fila)
    return filas


def _rangos_promedio(valores: list[float]) -> list[float]:
    orden = sorted(range(len(valores)), key=lambda i: valores[i])
    rangos = [0.0] * len(valores)
    i = 0
    while i < len(orden):
        j = i
        while j + 1 < len(orden) and valores[orden[j + 1]] == valores[orden[i]]:
            j += 1
        for k in range(i, j + 1):
            rangos[orden[k]] = (i + j) / 2 + 1
        i = j + 1
    return rangos


def kendall_w(matriz: list[list[float]]) -> dict:
    """W de Kendall con correccion por empates. matriz[juez][item] = puntaje."""
    m = len(matriz)
    if m < 3:
        return {"w": None, "motivo": f"requiere >= 3 jueces (hay {m})"}
    n = len(matriz[0])
    if n < 2:
        return {"w": None, "motivo": "requiere >= 2 items"}
    rangos = [_rangos_promedio(f) for f in matriz]
    sumas = [sum(rangos[j][i] for j in range(m)) for i in range(n)]
    media = sum(sumas) / n
    s = sum((r - media) ** 2 for r in sumas)
    t = 0.0
    for f in matriz:
        conteo: dict[float, int] = {}
        for v in f:
            conteo[v] = conteo.get(v, 0) + 1
        t += sum(c ** 3 - c for c in conteo.values())
    den = m * m * (n ** 3 - n) - m * t
    if den <= 0:
        return {"w": None, "motivo": "todos los jueces asignan el mismo puntaje a todos los items (W indefinido)"}
    w = 12 * s / den
    chi2 = m * (n - 1) * w
    from scipy.stats import chi2 as dist_chi2
    return {"w": w, "chi2": chi2, "gl": n - 1, "p": float(dist_chi2.sf(chi2, n - 1)), "m": m, "n": n}


# --- Lectura y validacion de datos ----------------------------------------------
def normalizar_criterio(texto: str) -> str:
    """Minusculas sin diacriticos ni caracteres ajenos a las letras latinas."""
    base = unicodedata.normalize("NFKD", str(texto).strip().lower())
    base = "".join(ch for ch in base if not unicodedata.combining(ch))
    return "".join(ch for ch in base if "a" <= ch <= "z")


def leer_matriz(ruta: str | Path, hoja: str | None = None):
    """Lee CSV/XLSX en formato largo y devuelve un DataFrame validado (juez,item,criterio,puntaje)."""
    import pandas as pd

    ruta = Path(ruta)
    if not ruta.exists():
        raise DatosInvalidos(f"No existe el archivo de calificaciones: {ruta}")
    if ruta.suffix.lower() in (".xlsx", ".xlsm"):
        try:
            libro = pd.ExcelFile(ruta)
        except Exception as e:  # zip/openpyxl/pandas: cualquier archivo ilegible
            raise DatosInvalidos(f"No se pudo abrir el libro Excel {ruta} ({type(e).__name__}): "
                                 "archivo corrupto o no es un .xlsx valido") from e
        if hoja is not None and hoja not in libro.sheet_names:
            raise DatosInvalidos(f"La hoja '{hoja}' no existe en {ruta.name}; hojas disponibles: {libro.sheet_names}")
        try:
            df = libro.parse(sheet_name=hoja if hoja is not None else 0, dtype=object)
        except Exception as e:
            raise DatosInvalidos(f"No se pudo leer la hoja de {ruta.name} ({type(e).__name__}: {e})") from e
        finally:
            libro.close()
    elif ruta.suffix.lower() in (".csv", ".txt"):
        if ruta.stat().st_size == 0:
            raise DatosInvalidos(f"El archivo está vacío (0 bytes): {ruta}")
        df = None
        for enc in ("utf-8-sig", "cp1252"):
            try:
                df = pd.read_csv(ruta, sep=None, engine="python", encoding=enc, dtype=object)
                break
            except UnicodeDecodeError:
                continue
            except pd.errors.EmptyDataError:
                raise DatosInvalidos(f"El archivo está vacío: {ruta}")
            except (csv.Error, pd.errors.ParserError) as e:
                raise DatosInvalidos(f"No se pudo interpretar {ruta.name} como CSV ({e}); "
                                     f"se esperaban las columnas {list(COLUMNAS)} separadas por coma o punto y coma") from e
        if df is None:
            raise DatosInvalidos(f"No se pudo decodificar {ruta}")
    else:
        raise DatosInvalidos(f"Formato no soportado ({ruta.suffix}); use .csv o .xlsx")

    df.columns = [str(c).strip().lower() for c in df.columns]
    faltan = [c for c in COLUMNAS if c not in df.columns]
    if faltan:
        raise DatosInvalidos(f"Faltan columnas obligatorias {faltan}; se esperaba {list(COLUMNAS)}")
    df = df[list(COLUMNAS)].dropna(how="all")
    if df.empty:
        raise DatosInvalidos(
            "SIN DATOS: la matriz no contiene calificaciones de jueces. Este modulo no "
            "calcula ni simula nada sin calificaciones reales (use 'plantilla' para capturar)."
        )
    return _validar(df)


def _validar(df):
    vmin, vmax = L_MINIMO, C_CATEGORIAS - 1
    errores = []
    df = df.copy()
    df["juez"] = df["juez"].map(lambda x: str(x).strip() if x == x and x is not None else "")
    df["item"] = df["item"].map(lambda x: _texto_item(x))
    df["criterio"] = df["criterio"].map(lambda x: normalizar_criterio(x) if x == x and x is not None else "")
    for i, fila in df.iterrows():
        pos = i + 2
        if not fila["juez"]:
            errores.append(f"fila {pos}: juez vacío")
        if not fila["item"]:
            errores.append(f"fila {pos}: item vacío")
        if fila["criterio"] not in CRITERIOS:
            errores.append(f"fila {pos}: criterio '{fila['criterio']}' no válido {list(CRITERIOS)}")
    puntajes = []
    for i, v in df["puntaje"].items():
        pos = i + 2
        if v is None or (isinstance(v, float) and math.isnan(v)) or str(v).strip() == "":
            errores.append(f"fila {pos}: puntaje vacío (el juez dejó la celda sin llenar)")
            puntajes.append(None)
            continue
        try:
            x = float(str(v).strip().replace(",", "."))
        except (TypeError, ValueError):
            errores.append(f"fila {pos}: puntaje no numérico ({v!r})")
            puntajes.append(None)
            continue
        if not math.isfinite(x):
            errores.append(f"fila {pos}: puntaje no finito ({v!r}); se esperaba 0 (No) o 1 (Si)")
            puntajes.append(None)
            continue
        if x != int(x) or not (vmin <= int(x) <= vmax):
            errores.append(f"fila {pos}: puntaje fuera de {vmin}-{vmax} o no entero ({v!r}); "
                           "se esperaba 0 (No) o 1 (Si)")
            puntajes.append(None)
        else:
            puntajes.append(int(x))
    df["puntaje"] = puntajes
    if errores:
        raise DatosInvalidos("Datos inválidos:\n  - " + "\n  - ".join(errores[:25])
                             + (f"\n  ... y {len(errores) - 25} más" if len(errores) > 25 else ""))
    dup = df[df.duplicated(["juez", "item", "criterio"], keep=False)]
    if not dup.empty:
        ej = dup.head(5)[["juez", "item", "criterio"]].values.tolist()
        raise DatosInvalidos(f"Calificaciones duplicadas (juez, item, criterio): {ej}")
    jueces = list(dict.fromkeys(df["juez"]))
    if len(jueces) < 2:
        raise DatosInvalidos(f"Se requieren al menos 2 jueces (hay {len(jueces)}).")
    celdas = set(zip(df["item"], df["criterio"]))
    items_v = list(dict.fromkeys(df["item"]))
    criterios_v = sorted(set(df["criterio"]))
    rejilla = {(it, cr) for it in items_v for cr in criterios_v}
    if celdas != rejilla:
        falta = sorted(rejilla - celdas)[:6]
        raise DatosInvalidos(
            "Matriz incompleta: la rejilla item x criterio no está completa; "
            f"ningun juez califica {falta} (cada item debe tener los mismos criterios: {criterios_v})."
        )
    for j in jueces:
        propias = set(zip(df.loc[df["juez"] == j, "item"], df.loc[df["juez"] == j, "criterio"]))
        if propias != celdas:
            faltan = sorted(celdas - propias)[:6]
            raise DatosInvalidos(f"Matriz incompleta: el juez '{j}' no califica {faltan} (todos los jueces deben calificar todas las celdas item x criterio).")
    return df.reset_index(drop=True)


def _texto_item(x) -> str:
    if x is None or x != x:
        return ""
    s = str(x).strip()
    if s.endswith(".0") and s[:-2].isdigit():
        s = s[:-2]
    return s


# --- Calculo principal ----------------------------------------------------------
def calcular(df, umbral_v: float = UMBRAL_V, umbral_ivc: float = UMBRAL_IVC,
             fuente: dict | None = None) -> ResultadoInstrumento:
    jueces = list(dict.fromkeys(df["juez"]))
    items = list(dict.fromkeys(df["item"]))
    criterios = [cr for cr in CRITERIOS if cr in set(df["criterio"])]
    n = len(jueces)
    advertencias = [
        "[VERIFICAR] Las reglas de eliminacion por item (V < "
        f"{UMBRAL_ELIMINAR_V:.2f} o I-CVI de relevancia < {UMBRAL_ELIMINAR_RELEVANCIA:.2f}) son operativas del "
        "modulo, sin respaldo bibliografico; requieren confirmacion del tesista y la asesora.",
        "Modelo Fany 2024 (DEC-015): tres criterios dicotomicos (Pertinencia, Relevancia y Claridad) "
        "y V = S/n con c = 2. Con tres jueces, V solo alcanza 0.000, 0.333, 0.667 o 1.000, "
        "de modo que el umbral de 0.80 exige unanimidad.",
    ]
    if n < 3:
        advertencias.append(f"Solo {n} jueces: no se calcula W de Kendall y la potencia de la V es baja.")
    idx = {(r.item, r.criterio, r.juez): int(r.puntaje) for r in df.itertuples()}

    celdas: list[ResultadoCelda] = []
    for it in items:
        for cr in criterios:
            pts = [idx[(it, cr, j)] for j in jueces]
            s = sum(x - L_MINIMO for x in pts)
            v = s / (n * (C_CATEGORIAS - 1))
            lo, hi = ic_wilson_v(v, n)
            ivc = ivc_item(pts)
            cumple = v >= umbral_v - EPS and ivc >= umbral_ivc - EPS
            celdas.append(ResultadoCelda(it, cr, n, s, v, lo, hi, p_exacto_v(s, n), ivc, cumple))

    resultados_items: list[ResultadoItem] = []
    for it in items:
        cs = [c for c in celdas if c.item == it]
        v_it = sum(c.v for c in cs) / len(cs)
        ivc_it = sum(c.ivc for c in cs) / len(cs)
        fallidos = [c.criterio for c in cs if not c.cumple]
        rel = next((c for c in cs if c.criterio == "relevancia"), None)
        if not fallidos:
            dec, mot = "mantener", "todos los criterios cumplen V e I-CVI"
        elif v_it < UMBRAL_ELIMINAR_V - EPS or (rel is not None and rel.ivc < UMBRAL_ELIMINAR_RELEVANCIA - EPS):
            dec = "eliminar"
            mot = (f"V del item {v_it:.2f} < {UMBRAL_ELIMINAR_V:.2f}" if v_it < UMBRAL_ELIMINAR_V - EPS
                   else f"I-CVI de relevancia {rel.ivc:.2f} < {UMBRAL_ELIMINAR_RELEVANCIA:.2f}")
        else:
            dec, mot = "modificar", "no cumplen: " + ", ".join(ETIQUETAS[cr] for cr in fallidos)
        resultados_items.append(ResultadoItem(it, v_it, ivc_it, fallidos, dec, mot))

    v_global = sum(c.v for c in celdas) / len(celdas)
    s_ave = sum(r.ivc for r in resultados_items) / len(resultados_items)
    s_ua = sum(1 for r in resultados_items if r.ivc >= 1 - EPS) / len(resultados_items)
    por_criterio = {}
    for cr in criterios:
        cs = [c for c in celdas if c.criterio == cr]
        matriz = [[idx[(it, cr, j)] for it in items] for j in jueces]
        por_criterio[cr] = {
            "v_promedio": sum(c.v for c in cs) / len(cs),
            "s_cvi_ave": sum(c.ivc for c in cs) / len(cs),
            "kendall": kendall_w(matriz),
        }
    matriz_global = [[sum(idx[(it, cr, j)] for cr in criterios) / len(criterios) for it in items] for j in jueces]
    kendall = kendall_w(matriz_global)

    n_mod = sum(1 for r in resultados_items if r.decision == "modificar")
    n_eli = sum(1 for r in resultados_items if r.decision == "eliminar")
    if n_mod == 0 and n_eli == 0 and v_global >= umbral_v - EPS and s_ave >= umbral_ivc - EPS:
        dec_i, mot_i = "aplicable sin modificar", "todos los items se mantienen; V global y S-CVI/Ave >= umbral"
    elif v_global < umbral_v - EPS or s_ave < umbral_ivc - EPS:
        dec_i = "no aplicable"
        mot_i = f"V global {v_global:.2f} o S-CVI/Ave {s_ave:.2f} por debajo del umbral ({umbral_v:.2f})"
    else:
        dec_i = "aplicable previa modificacion"
        mot_i = f"{n_mod} item(s) por modificar y {n_eli} por eliminar; indicadores globales >= umbral"
    return ResultadoInstrumento(
        n_jueces=n, n_items=len(items), criterios=criterios, v_global=v_global,
        s_cvi_ave=s_ave, s_cvi_ua=s_ua, por_criterio=por_criterio, kendall=kendall,
        decision=dec_i, motivo=mot_i, celdas=celdas, items=resultados_items,
        advertencias=advertencias, fuente=fuente or {},
    )


# --- Markdown (estilo APA 7) ----------------------------------------------------
def _f(x: float | None, d: int = 2) -> str:
    return "n/c" if x is None else f"{x:.{d}f}"


def _tabla_md(num: int, titulo: str, cabeza: list[str], filas: list[list[str]], nota: str) -> str:
    out = [f"**Tabla {num}**", "", f"*{titulo}*", ""]
    out.append("| " + " | ".join(cabeza) + " |")
    out.append("|" + "|".join("---" for _ in cabeza) + "|")
    out += ["| " + " | ".join(f) + " |" for f in filas]
    out += ["", f"*Nota.* {nota}", ""]
    return "\n".join(out)


def _nota_v_critico(n: int) -> str:
    """Nota que sustituye la tabla de V critico de la escala ordinal."""
    valores = ", ".join(f"{k / n:.3f}" for k in range(n + 1))
    return (
        "*Nota.* Con criterios dicotomicos (c = 2) y n jueces, V = S/n solo puede tomar "
        f"los valores k/n. Con n = {n} los valores alcanzables son {valores}. "
        "El umbral de 0.80 equivale a unanimidad perfecta de los jueces en cada item: "
        "con tres jueces, V = 0.667 no alcanza el umbral. La tabla de V critico impresa por "
        "Aiken (1985) para escalas ordinales no aplica a este modelo y no se transcribe. "
        "[VERIFICAR: la convencion de cola unilateral y de desempate de la prueba exacta "
        "requiere cotejo con la fuente antes de citar valores de p derivados de ella.]\n"
    )


def a_markdown(r: ResultadoInstrumento) -> str:
    n = r.n_jueces
    nota_v = (f"V = V de Aiken (c = {C_CATEGORIAS}, l = {L_MINIMO}, n = {n}); criterios: Pertinencia, "
              "Relevancia y Claridad, dicotomicos Si/No; "
              "IC = intervalo de confianza al 95 % por puntuacion de Wilson (Penfield y Giacobbi, 2004); "
              "p = probabilidad exacta unilateral bajo categorias equiprobables; "
              "I-CVI = proporcion de jueces que marcan Si. Umbrales: V >= "
              f"{UMBRAL_V:.2f} e I-CVI >= {UMBRAL_IVC:.2f}. Con tres jueces, V = S/n solo alcanza "
              "0.000, 0.333, 0.667 o 1.000, de modo que el umbral exige unanimidad.")
    t1 = _tabla_md(1, "V de Aiken e indice de validez de contenido por item y criterio",
                   ["Item", "Criterio", "S", "V", "IC 95 %", "p", "I-CVI", "Cumple"],
                   [[c.item, ETIQUETAS[c.criterio], str(c.s), _f(c.v), f"[{_f(c.ic_inf)}; {_f(c.ic_sup)}]",
                     f"{c.p_exacto:.3f}", _f(c.ivc), "Si" if c.cumple else "No"] for c in r.celdas], nota_v)
    t2 = _tabla_md(2, "Decision por item",
                   ["Item", "V", "I-CVI", "Decision", "Motivo"],
                   [[i.item, _f(i.v), _f(i.ivc), i.decision, i.motivo] for i in r.items],
                   "V e I-CVI del item son el promedio de sus criterios. Reglas de decision operativas del modulo: "
                   f"eliminar si V del item < {UMBRAL_ELIMINAR_V:.2f} o I-CVI de relevancia < {UMBRAL_ELIMINAR_RELEVANCIA:.2f}; "
                   "modificar si falla algun criterio; mantener en los demas casos. "
                   "[VERIFICAR: estos umbrales de eliminacion son una regla operativa del modulo, sin respaldo en la "
                   "literatura ni en el modelo UNAJMA; requieren confirmacion del tesista y la asesora.]")
    filas3 = []
    for cr in r.criterios:
        d = r.por_criterio[cr]
        k = d["kendall"]
        filas3.append([ETIQUETAS[cr], _f(d["v_promedio"]), _f(d["s_cvi_ave"]),
                       _f(k.get("w")) if k.get("w") is not None else "n/c"])
    t3 = _tabla_md(3, "Indicadores por criterio", ["Criterio", "V promedio", "S-CVI/Ave", "W de Kendall"], filas3,
                   "W de Kendall calculada sobre los items con correccion por empates; \"n/c\" indica que no es "
                   "calculable (menos de 3 jueces o puntajes sin variacion).")
    k = r.kendall
    kw = (f"W = {k['w']:.3f}, chi2({k['gl']}) = {k['chi2']:.2f}, p = {k['p']:.3f}" if k.get("w") is not None
          else f"no calculable ({k.get('motivo')})")
    t4 = _tabla_md(4, "Validez de contenido del instrumento",
                   ["Indicador", "Valor"],
                   [["Jueces", str(n)], ["Items", str(r.n_items)], ["V global", _f(r.v_global, 3)],
                    ["S-CVI/Ave", _f(r.s_cvi_ave, 3)], ["S-CVI/UA", _f(r.s_cvi_ua, 3)],
                    ["Concordancia (W de Kendall)", kw], ["Decision", r.decision]],
                   r.motivo + ".")
    enc = ["# Validez de contenido por juicio de expertos", ""]
    enc += ["Modelo aplicado: certificado Fany 2024 (DEC-015), tres criterios dicotomicos Si/No. "
            "Escala de captura: 0 = No, 1 = Si.", ""]
    if r.fuente:
        enc += [f"Fuente de datos: `{r.fuente.get('archivo')}` (SHA-256 `{r.fuente.get('sha256')}`). "
                f"Generado: {r.fuente.get('generado')}.", ""]
    if r.advertencias:
        enc += ["> Advertencias: " + " ".join(r.advertencias), ""]
    return "\n".join(enc) + "\n" + "\n".join([t1, t2, t3, t4]) + "\n" + _nota_v_critico(n)


# --- XLSX con formulas visibles -------------------------------------------------
def a_xlsx(df, r: ResultadoInstrumento, destino: str | Path, umbral_v: float = UMBRAL_V, umbral_ivc: float = UMBRAL_IVC) -> Path:
    """Escribe el libro con formulas (V de Aiken con c = 2 y tres criterios dicotomicos)."""
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter as L

    destino = seguridad.asegurar_escritura_permitida(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    jueces = list(dict.fromkeys(df["juez"]))
    items = list(dict.fromkeys(df["item"]))
    criterios = r.criterios
    idx = {(x.item, x.criterio, x.juez): int(x.puntaje) for x in df.itertuples()}
    n = len(jueces)
    negrita = Font(bold=True)
    relleno = PatternFill("solid", fgColor="DDDDDD")

    wb = Workbook()
    # Parametros
    wp = wb.active
    wp.title = "Parametros"
    params = [
        ("c (categorias)", C_CATEGORIAS), ("l (puntaje minimo)", L_MINIMO), ("n (jueces)", n),
        ("alfa", 0.05), ("z", "=NORMSINV(1-B6/2)"), ("N = n*(c-l)", "=B5*(B3-B4)"),
        ("Umbral V", umbral_v), ("Umbral I-CVI", umbral_ivc), ("Corte de aprobacion (I-CVI)", CORTE_APROBACION),
        ("Eliminar si V del item <", UMBRAL_ELIMINAR_V), ("Eliminar si I-CVI relevancia <", UMBRAL_ELIMINAR_RELEVANCIA),
    ]
    wp["A1"], wp["B1"] = "Parametro", "Valor"
    for c in ("A1", "B1"):
        wp[c].font = negrita
    for i, (k, v) in enumerate(params, start=3):
        wp.cell(i, 1, k)
        wp.cell(i, 2, v)
    wp["A15"] = ("Formulas: S = suma de marcas Si; V = S/(n(c-1)) = S/n; IC Wilson (Penfield y Giacobbi, 2004); "
                 "I-CVI = jueces con marca Si / n.")
    fuente = r.fuente or {}
    wp["A16"] = (f"Fuente: {fuente.get('archivo', '')}  SHA-256: {fuente.get('sha256', '')}  "
                 f"Generado: {fuente.get('generado', '')}")
    wp["A17"] = ("Las calificaciones son las entregadas por los jueces; este libro no las modifica. "
                 "Hoja 'Instrumento': W de Kendall calculada en Python (valor, no formula).")
    wp["A18"] = ("Modelo Fany 2024 (DEC-015): tres criterios dicotomicos Si/No de Pertinencia, Relevancia y Claridad. "
                 "Con tres jueces, V solo alcanza 0.000, 0.333, 0.667 o 1.000; el umbral de 0.80 exige unanimidad.")
    wp.column_dimensions["A"].width = 34
    P = {"c": "Parametros!$B$3", "l": "Parametros!$B$4", "n": "Parametros!$B$5", "z": "Parametros!$B$7",
         "N": "Parametros!$B$8", "uv": "Parametros!$B$9", "ui": "Parametros!$B$10", "corte": "Parametros!$B$11",
         "ev": "Parametros!$B$12", "er": "Parametros!$B$13"}

    # Calificaciones
    ws = wb.create_sheet("Calificaciones")
    c_sc0 = 4                       # primera columna de puntajes (D)
    c_bin0 = c_sc0 + n + 1          # binaria (tras una columna en blanco)
    c_sum = c_bin0 + n
    c_ivc = c_sum + 1
    c_s = c_ivc + 2
    c_v, c_lo, c_hi, c_cum = c_s + 1, c_s + 2, c_s + 3, c_s + 4
    ws.cell(2, 2, "Item")
    ws.cell(2, 3, "Criterio")
    for k, j in enumerate(jueces):
        ws.cell(2, c_sc0 + k, f"Experto {k + 1} ({j})")
        ws.cell(2, c_bin0 + k, f"Binaria E{k + 1}")
    for col, t in ((c_sum, "Suma"), (c_ivc, "IVC por criterio"), (c_s, "S"), (c_v, "V de Aiken"),
                   (c_lo, "IC95 inf"), (c_hi, "IC95 sup"), (c_cum, "Cumple")):
        ws.cell(2, col, t)
    for c in range(2, c_cum + 1):
        ws.cell(2, c).font = negrita
        ws.cell(2, c).fill = relleno
        ws.cell(2, c).alignment = Alignment(wrap_text=True, horizontal="center")
    fila = 3
    for it in items:
        for cr in criterios:
            ws.cell(fila, 2, int(it) if it.isdigit() else it)
            ws.cell(fila, 3, ETIQUETAS[cr])
            for k, j in enumerate(jueces):
                ws.cell(fila, c_sc0 + k, idx[(it, cr, j)])
                sc = f"{L(c_sc0 + k)}{fila}"
                ws.cell(fila, c_bin0 + k, f"=IF({sc}=1,1,0)")
            rng_sc = f"{L(c_sc0)}{fila}:{L(c_sc0 + n - 1)}{fila}"
            rng_bin = f"{L(c_bin0)}{fila}:{L(c_bin0 + n - 1)}{fila}"
            ws.cell(fila, c_sum, f"=SUM({rng_bin})")
            ws.cell(fila, c_ivc, f"={L(c_sum)}{fila}/{P['n']}")
            ws.cell(fila, c_s, f"=SUM({rng_sc})-{P['n']}*{P['l']}")
            S, V = f"{L(c_s)}{fila}", f"{L(c_v)}{fila}"
            ws.cell(fila, c_v, f"={S}/({P['n']}*({P['c']}-{P['l']}))")
            raiz = f"{P['z']}*SQRT(4*{P['N']}*{V}*(1-{V})+{P['z']}^2)"
            ws.cell(fila, c_lo, f"=MAX(0,(2*{P['N']}*{V}+{P['z']}^2-{raiz})/(2*({P['N']}+{P['z']}^2)))")
            ws.cell(fila, c_hi, f"=MIN(1,(2*{P['N']}*{V}+{P['z']}^2+{raiz})/(2*({P['N']}+{P['z']}^2)))")
            ws.cell(fila, c_cum, f'=IF(AND({V}>={P["uv"]}-0.000000001,{L(c_ivc)}{fila}>={P["ui"]}-0.000000001),"Si","No")')
            for col in (c_ivc, c_v, c_lo, c_hi):
                ws.cell(fila, col).number_format = "0.000"
            fila += 1
    ultima = fila - 1
    col_item = f"Calificaciones!$B$3:$B${ultima}"
    col_crit = f"Calificaciones!$C$3:$C${ultima}"
    col_v = f"Calificaciones!${L(c_v)}$3:${L(c_v)}${ultima}"
    col_ivc = f"Calificaciones!${L(c_ivc)}$3:${L(c_ivc)}${ultima}"
    col_cum = f"Calificaciones!${L(c_cum)}$3:${L(c_cum)}${ultima}"
    ws.column_dimensions["C"].width = 14

    # Items
    wi = wb.create_sheet("Items")
    for c, t in enumerate(("Item", "V del item", "I-CVI del item", "Criterios que no cumplen", "I-CVI relevancia", "Decision"), start=1):
        wi.cell(1, c, t).font = negrita
        wi.cell(1, c).fill = relleno
    wi.cell(1, 8, "[VERIFICAR: los umbrales de eliminar/modificar (hoja Parametros) son una regla operativa del "
                  "modulo, sin respaldo bibliografico; requieren confirmacion del tesista y la asesora.]")
    for k, it in enumerate(items, start=2):
        clave = int(it) if it.isdigit() else it
        wi.cell(k, 1, clave)
        wi.cell(k, 2, f"=AVERAGEIFS({col_v},{col_item},A{k})")
        wi.cell(k, 3, f"=AVERAGEIFS({col_ivc},{col_item},A{k})")
        wi.cell(k, 4, f'=COUNTIFS({col_item},A{k},{col_cum},"No")')
        if "relevancia" in criterios:
            wi.cell(k, 5, f'=SUMIFS({col_ivc},{col_item},A{k},{col_crit},"Relevancia")')
            cond_rel = f"OR(B{k}<{P['ev']},E{k}<{P['er']})"
        else:
            wi.cell(k, 5, "n/a")
            cond_rel = f"B{k}<{P['ev']}"
        wi.cell(k, 6, f'=IF(D{k}=0,"mantener",IF({cond_rel},"eliminar","modificar"))')
        wi.cell(k, 2).number_format = wi.cell(k, 3).number_format = wi.cell(k, 5).number_format = "0.000"
    fin_i = len(items) + 1

    # Instrumento
    wn = wb.create_sheet("Instrumento")
    wn["A1"], wn["B1"] = "Indicador", "Valor"
    wn["A1"].font = wn["B1"].font = negrita
    rng_ic = f"Items!$C$2:$C${fin_i}"
    filas = [
        ("Jueces", "=Parametros!B5"), ("Items", f"=COUNTA(Items!A2:A{fin_i})"),
        ("V global", f"=AVERAGE({col_v})"), ("S-CVI/Ave", f"=AVERAGE({rng_ic})"),
        ("S-CVI/UA", f'=COUNTIF({rng_ic},">=0.999999999")/COUNT({rng_ic})'),
        ("Items a modificar", f'=COUNTIF(Items!F2:F{fin_i},"modificar")'),
        ("Items a eliminar", f'=COUNTIF(Items!F2:F{fin_i},"eliminar")'),
    ]
    for k, (a, b) in enumerate(filas, start=2):
        wn.cell(k, 1, a)
        wn.cell(k, 2, b)
    for k in (4, 5, 6):
        wn.cell(k, 2).number_format = "0.000"
    wn["A9"] = "Decision del instrumento"
    wn["B9"] = (f'=IF(AND(B7=0,B8=0,B4>={P["uv"]}-0.000000001,B5>={P["ui"]}-0.000000001),"aplicable sin modificar",'
                f'IF(OR(B4<{P["uv"]}-0.000000001,B5<{P["ui"]}-0.000000001),"no aplicable","aplicable previa modificacion"))')
    wn["A9"].font = negrita
    wn["A11"] = "Por criterio"
    wn["A11"].font = negrita
    for c, t in enumerate(("Criterio", "V promedio", "S-CVI/Ave", "W de Kendall (valor Python)"), start=1):
        wn.cell(12, c, t).font = negrita
    for k, cr in enumerate(criterios, start=13):
        wn.cell(k, 1, ETIQUETAS[cr])
        wn.cell(k, 2, f"=AVERAGEIFS({col_v},{col_crit},A{k})")
        wn.cell(k, 3, f"=AVERAGEIFS({col_ivc},{col_crit},A{k})")
        w = r.por_criterio[cr]["kendall"].get("w")
        wn.cell(k, 4, "n/c" if w is None else round(w, 4))
        wn.cell(k, 2).number_format = wn.cell(k, 3).number_format = "0.000"
    kw = r.kendall.get("w")
    wn.cell(14 + len(criterios), 1, "W de Kendall global (valor Python)")
    wn.cell(14 + len(criterios), 2, "n/c" if kw is None else round(kw, 4))
    wn.column_dimensions["A"].width = 36
    wn.column_dimensions["B"].width = 26
    wb.save(destino)
    return destino


# --- Plantilla de captura (SIEMPRE vacia) ---------------------------------------
def crear_plantilla(destino: str | Path = PLANTILLA_DEFECTO, forzar: bool = False) -> Path:
    """CSV solo con cabeceras. Nunca contiene calificaciones."""
    destino = _permitir_salida(destino)
    if destino.exists() and not forzar:
        raise FileExistsError(f"Ya existe {destino}; use --forzar para reemplazarla (podria contener datos reales).")
    destino.parent.mkdir(parents=True, exist_ok=True)
    with open(destino, "w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f).writerow(COLUMNAS)
    return destino


# --- CLI ------------------------------------------------------------------------
def _construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Validez de contenido por juicio de expertos (V de Aiken, I-CVI, W de Kendall).")
    sub = p.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("plantilla", help="crea un CSV de captura VACIO (solo cabeceras)")
    sp.add_argument("--salida", default=str(PLANTILLA_DEFECTO))
    sp.add_argument("--forzar", action="store_true")
    sc = sub.add_parser("calcular", help="calcula a partir de calificaciones reales de jueces")
    sc.add_argument("entrada")
    sc.add_argument("--hoja", default=None, help="hoja del XLSX (por defecto la primera)")
    sc.add_argument("--md", default=None, help="ruta de salida del informe Markdown")
    sc.add_argument("--xlsx", default=None, help="ruta de salida del libro con formulas")
    sc.add_argument("--forzar", action="store_true", help="permite sobrescribir --md/--xlsx existentes")
    sc.add_argument("--json", action="store_true")
    st = sub.add_parser("tabla-critica", help="V de Aiken critico por distribucion nula exacta")
    st.add_argument("--jueces-min", type=int, default=3)
    st.add_argument("--jueces-max", type=int, default=10)
    st.add_argument("--json", action="store_true")
    return p


def _permitir_salida(ruta) -> Path:
    """Guarda de escritura del modulo: ademas de la general, prohibe datos/raw/."""
    dest = seguridad.asegurar_escritura_permitida(ruta)
    try:
        dest.resolve().relative_to(Path(rutas.DATOS_RAW).resolve())
    except ValueError:
        return dest
    raise seguridad.EscrituraProhibida(
        f"Prohibido escribir en datos/raw/ (datos de campo inmutables, solo los entrega el tesista): {dest}"
    )


def _guardar_texto(ruta: str, texto: str, forzar: bool) -> Path:
    dest = _permitir_salida(ruta)
    if dest.exists() and not forzar:
        raise FileExistsError(f"Ya existe {dest}; use --forzar para reemplazar.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(texto, encoding="utf-8")
    return dest


def main(argv: list[str] | None = None) -> int:
    seguridad.configurar_utf8()
    parser = _construir_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code not in (0, None) else 0

    try:
        if args.cmd == "plantilla":
            dest = crear_plantilla(args.salida, args.forzar)
            print(f"Plantilla VACIA creada (solo cabeceras {list(COLUMNAS)}; modelo Fany 2024: 0 = No, 1 = Si): {dest}")
            return 0

        if args.cmd == "tabla-critica":
            if args.jueces_min < 2 or args.jueces_max < args.jueces_min:
                print("Parámetros inválidos.", file=sys.stderr)
                return 2
            filas = tabla_v_critico(C_CATEGORIAS, args.jueces_min, args.jueces_max)
            if args.json:
                print(json.dumps(filas, ensure_ascii=False, indent=2))
            else:
                print(f"V critico unilateral (c={C_CATEGORIAS}, categorias equiprobables, distribucion exacta)")
                print("n    alfa=.05   alfa=.01   alfa=.001")
                for f in filas:
                    print(f"{f['n']:<4} " + "  ".join(f"{(_f(f[f'alfa_{a}']) if f[f'alfa_{a}'] is not None else 'inalc.')}" for a in (0.05, 0.01, 0.001)))
            return 0

        # calcular
        ruta = Path(args.entrada)
        df = leer_matriz(ruta, args.hoja)
        fuente = {"archivo": str(ruta), "sha256": seguridad.sha256_archivo(ruta),
                  "generado": datetime.now().isoformat(timespec="seconds")}
        res = calcular(df, fuente=fuente)
        md = a_markdown(res)
        if args.md:
            print(f"Markdown: {_guardar_texto(args.md, md, args.forzar)}", file=sys.stderr)
        if args.xlsx:
            dest = _permitir_salida(args.xlsx)
            if dest.exists() and not args.forzar:
                raise FileExistsError(f"Ya existe {dest}; use --forzar para reemplazar.")
            print(f"XLSX: {a_xlsx(df, res, dest)}", file=sys.stderr)
        if args.json:
            print(json.dumps(asdict(res), ensure_ascii=False, indent=2, default=float))
        else:
            print(md)
        return 0 if res.decision == "aplicable sin modificar" else 1
    except (DatosInvalidos, FileExistsError, seguridad.EscrituraProhibida) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
