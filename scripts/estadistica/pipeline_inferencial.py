#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Pipeline inferencial (pretest/postest, N = n = 14).

SOLO corre con datos reales certificados: exige datos/raw/MANIFEST.json válido
(ver manifest_datos.py). Sin manifiesto válido el estado es
'BLOQUEADO: esperando datos de campo', el código de salida es 3 y NO se calcula
ni se escribe ninguna cifra.

Flujo:
  1. Manifiesto válido (campos, n_esperado = 14, SHA-256 reales de cada CSV).
  2. Control de calidad por niveles: N1 estructura, N2 rangos/tipos,
     N3 coherencia aritmética de scores, N4 pareo pre/post. Cualquier error
     rechaza el lote (código 1) sin calcular estadísticos.
  3. Descriptivos por indicador y fase.
  4. Diferencias pareadas d = postest - pretest; Shapiro-Wilk sobre d.
  5. Regla de decisión: d normal y variable continua -> t pareada unilateral
     + d_z de Cohen con IC95% (t no central); no normal u ordinal (AP, UP)
     -> Wilcoxon de rangos con signo unilateral.
  6. Confiabilidad del cuestionario TAM de Modalidad A (8 ítems): alfa de
     Cronbach sobre k = 8, omega (un factor, ejes principales) y correlación
     ítem-total corregida por subescala (AP, UP) y en el total.
  7. Multiplicidad: ajuste de Holm reportado aparte.

Decisiones estadísticas documentadas
  * El total de la Modalidad A no se contrasta porque es una combinación lineal
    de AP y UP y su prueba sería redundante; solo se reporta como descriptivo.
  * Wilcoxon: zero_method='wilcox' (se descartan las diferencias nulas; se
    reporta n_efectivo). Z asintótico SIN corrección de continuidad y CON
    corrección por empates en |d|:
        Var(W+) = n(n+1)(2n+1)/24 - sum(t^3 - t)/48,   Z = (W+ - n(n+1)/4)/sqrt(Var)
    p exacta (scipy, method='exact') solo si no hay empates y n_efectivo <= 50;
    con empates la distribución exacta sin empates no es válida y se usa la
    asintótica. p de decisión = exacta si existe; si no, asintótica.
  * Tamaño de efecto (Wilcoxon): r = Z / sqrt(n_efectivo), con n_efectivo =
    pares con diferencia distinta de cero (los que realmente entran al
    estadístico). Convención r = Z/sqrt(N); algunos autores usan N = 2n
    observaciones, lo que reduce r por un factor sqrt(2).
    [VERIFICAR: cita bibliográfica de la convención, a cargo del investigador bibliográfico].
    Se reporta además la correlación biserial de rangos pareada
    r_rb = (W+ - W-)/(W+ + W-).
  * Todos los tamaños de efecto y el signo de Z se calculan sobre d = post - pre
    (positivo = post mayor). La columna 'dirección' indica si coincide con H1.
  * No se usa remuestreo: la semilla se registra por reproducibilidad (no se consume).

Protección de escritura: además de las rutas de seguridad.py, el módulo veta
referencias/ completo y datos/raw/ (manifest_datos.asegurar_destino_modulo).

Códigos de salida: 0 ok, 1 lote rechazado por calidad o error de ejecución,
2 uso incorrecto, 3 BLOQUEADO (sin manifiesto válido).

Uso:
    python scripts/estadistica/pipeline_inferencial.py [--raw DIR] [--manifest RUTA]
           [--salida DIR] [--alfa 0.05] [--json]
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad  # noqa: E402
from scripts.estadistica import manifest_datos  # noqa: E402

VERSION_PIPELINE = "1.0"
SEMILLA = 20260930
SALIDA_DEFECTO = rutas.SALIDAS / "reportes_estadisticos"
N_ESPERADO = rutas.N_CENSAL
IDS_ESPERADOS = [f"TRAB-{i:02d}" for i in range(1, N_ESPERADO + 1)]
ITEMS_AP = [f"ap_{i:02d}" for i in range(1, 5)]
ITEMS_UP = [f"up_{i:02d}" for i in range(1, 5)]
COLUMNAS_OBLIGATORIAS = (
    ["sujeto_id", "t_reg", "t_vale", "rsd", "cpe"] + ITEMS_AP + ["score_ap"]
    + ITEMS_UP + ["score_up", "score_tam_total"]
)
_TOKENS_FALTANTE = {"", "na", "n/a", "nan", "null", "none"}

# columna: (rango, limite_inferior_abierto)
# Puntajes TAM de la Modalidad A (8 ítems): AP y UP suman 4 ítems cada una y el
# total suma los 8 ítems, conforme al Instrumento 03 y a DEC-019.
RANGOS = {
    "t_reg": (0.0, 120.0, True),
    "t_vale": (0.0, 60.0, True),
    "rsd": (0.0, 100.0, False),
    "cpe": (0.0, 100.0, False),
    "score_ap": (4.0, 20.0, False),
    "score_up": (4.0, 20.0, False),
    "score_tam_total": (8.0, 40.0, False),
}

# (etiqueta, columna, dirección de H1 sobre d = post - pre, ordinal)
INDICADORES = [
    ("T_reg", "t_reg", "less", False),
    ("T_vale", "t_vale", "less", False),
    ("RSD", "rsd", "greater", False),
    ("CPE", "cpe", "greater", False),
    ("AP", "score_ap", "greater", True),
    ("UP", "score_up", "greater", True),
]
ETIQUETA_DIRECCION = {"less": "post < pre", "greater": "post > pre"}


# ==========================================================================
# Formato
# ==========================================================================
def fmt_num(x, dec: int = 2) -> str:
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return "—"
    return f"{x:.{dec}f}"


def fmt_p(p) -> str:
    """APA: 3 decimales sin cero inicial; '< .001' cuando aplique."""
    if p is None or not math.isfinite(p):
        return "—"
    if p < 0.001:
        return "< .001"
    if p > 0.9995:
        return "> .999"
    return f"{p:.3f}".lstrip("0")


def _py(obj):
    """Convierte tipos numpy a tipos JSON nativos (redondeo a 10 decimales)."""
    if isinstance(obj, dict):
        return {str(k): _py(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_py(v) for v in obj]
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating, float)):
        v = float(obj)
        return round(v, 10) if math.isfinite(v) else None
    return obj


# ==========================================================================
# Estadística (funciones puras)
# ==========================================================================
def descriptivos(x) -> dict:
    """Media, DE (n-1), mediana, RIC (Q3-Q1, interpolación lineal), mínimo y máximo."""
    a = np.asarray(x, dtype=float)
    n = int(a.size)
    if n == 0:
        return {"n": 0, "media": None, "de": None, "mediana": None, "q1": None,
                "q3": None, "ric": None, "min": None, "max": None}
    q1, q3 = np.percentile(a, [25, 75])
    return {
        "n": n,
        "media": float(a.mean()),
        "de": float(a.std(ddof=1)) if n > 1 else None,
        "mediana": float(np.median(a)),
        "q1": float(q1),
        "q3": float(q3),
        "ric": float(q3 - q1),
        "min": float(a.min()),
        "max": float(a.max()),
    }


def shapiro_diferencias(d, alfa: float = 0.05) -> dict:
    """Shapiro-Wilk sobre las diferencias. No evaluable si n<3 o d constante."""
    a = np.asarray(d, dtype=float)
    if a.size < 3:
        return {"W": None, "p": None, "normal": None, "motivo": "n < 3"}
    if np.ptp(a) == 0:
        return {"W": None, "p": None, "normal": None, "motivo": "diferencias constantes (varianza nula)"}
    w, p = stats.shapiro(a)
    return {"W": float(w), "p": float(p), "normal": bool(p >= alfa), "motivo": None}


def elegir_prueba(normal, ordinal: bool) -> str:
    """Regla de decisión: t pareada solo si continua y normal; si no, Wilcoxon."""
    if ordinal or normal is not True:
        return "wilcoxon"
    return "t_pareada"


def _ncp_por_inversion(t_abs: float, gl: int, cola: float) -> float | None:
    """ncp tal que P(T_nc <= t_abs | ncp) = cola, con t_abs >= 0.

    Busca un intervalo [t_abs - w, t_abs + w] con cambio de signo, ensanchándolo
    (w = 5, 10, 20, 40) y descartando puntos donde nct.cdf no es finita (saturación
    numérica). Devuelve None si ningún intervalo funciona.
    """
    from scipy.optimize import brentq

    def f(ncp: float) -> float:
        return float(stats.nct.cdf(t_abs, gl, ncp)) - cola

    for w in (5.0, 10.0, 20.0, 40.0):
        a, b = t_abs - w, t_abs + w
        fa, fb = f(a), f(b)
        if math.isfinite(fa) and math.isfinite(fb) and fa * fb < 0:
            try:
                return float(brentq(f, a, b, xtol=1e-10))
            except (ValueError, RuntimeError):
                return None
    return None


def ic_dz(dz: float, n: int, confianza: float = 0.95) -> tuple[float, float] | None:
    """IC de d_z por inversión de la t no central (Cumming y Finch).

    Se resuelve sobre |t| y se refleja si t < 0 (P(T<=t|ncp) = 1 - P(T<=-t|-ncp)),
    lo que evita la saturación numérica de nct.cdf. None solo si no converge.
    """
    if n < 2 or not math.isfinite(dz):
        return None
    gl = n - 1
    t_obs = dz * math.sqrt(n)
    t_abs = abs(t_obs)
    a = (1.0 - confianza) / 2.0
    lo = _ncp_por_inversion(t_abs, gl, 1.0 - a)
    hi = _ncp_por_inversion(t_abs, gl, a)
    if lo is None or hi is None:
        return None
    if t_obs < 0:
        lo, hi = -hi, -lo
    return lo / math.sqrt(n), hi / math.sqrt(n)


def t_pareada(post, pre, alternativa: str, confianza: float = 0.95) -> dict:
    """t pareada unilateral sobre d = post - pre, con dz e IC95% de dz y de la media de d."""
    post, pre = np.asarray(post, float), np.asarray(pre, float)
    d = post - pre
    n = int(d.size)
    gl = n - 1
    md, sd = float(d.mean()), float(d.std(ddof=1))
    if sd == 0:
        return {"prueba": "t_pareada", "n": n, "gl": gl, "t": None, "p": None,
                "media_dif": md, "de_dif": sd, "ic95_media_dif": None,
                "dz": None, "ic95_dz": None,
                "motivo": "DE de las diferencias nula: t no definida"}
    res = stats.ttest_rel(post, pre, alternative=alternativa)
    ee = sd / math.sqrt(n)
    tc = stats.t.ppf(1 - (1 - confianza) / 2, gl)
    dz = md / sd
    ic = ic_dz(dz, n, confianza)
    return {
        "prueba": "t_pareada", "n": n, "gl": gl, "t": float(res.statistic), "p": float(res.pvalue),
        "media_dif": md, "de_dif": sd, "ic95_media_dif": [md - tc * ee, md + tc * ee],
        "dz": dz, "ic95_dz": list(ic) if ic else None, "motivo": None,
    }


def wilcoxon_signo(d, alternativa: str) -> dict:
    """Wilcoxon de rangos con signo sobre d = post - pre (documentación en la cabecera del módulo)."""
    d = np.round(np.asarray(d, dtype=float), 9)
    n_total = int(d.size)
    dnz = d[d != 0]
    n_ef = int(dnz.size)
    base = {"prueba": "wilcoxon", "n_total": n_total, "n_efectivo": n_ef,
            "n_ceros": n_total - n_ef, "zero_method": "wilcox"}
    if n_ef == 0:
        return {**base, "w_plus": None, "w_minus": None, "z": None, "p_asintotica": None,
                "p_exacta": None, "p": None, "metodo_p": None, "empates": False,
                "r": None, "r_rb": None,
                "motivo": "todas las diferencias son nulas: el contraste no es estimable"}
    absd = np.abs(dnz)
    rangos = stats.rankdata(absd)
    w_plus = float(rangos[dnz > 0].sum())
    w_minus = float(rangos[dnz < 0].sum())
    _, conteos = np.unique(absd, return_counts=True)
    empates = bool((conteos > 1).any())
    corr_emp = float(((conteos ** 3 - conteos).sum()) / 48.0)
    var = n_ef * (n_ef + 1) * (2 * n_ef + 1) / 24.0 - corr_emp
    if var <= 0:
        return {**base, "w_plus": w_plus, "w_minus": w_minus, "z": None, "p_asintotica": None,
                "p_exacta": None, "p": None, "metodo_p": None, "empates": empates,
                "r": None, "r_rb": None, "motivo": "varianza nula de W+"}
    z = (w_plus - n_ef * (n_ef + 1) / 4.0) / math.sqrt(var)
    if alternativa == "greater":
        p_asint = float(stats.norm.sf(z))
    elif alternativa == "less":
        p_asint = float(stats.norm.cdf(z))
    else:
        p_asint = float(2 * stats.norm.sf(abs(z)))
    p_exacta = None
    motivo_exacta = None
    if empates:
        motivo_exacta = "empates en |d|: la distribución exacta sin empates no es válida"
    elif n_ef > 50:
        motivo_exacta = "n_efectivo > 50: se usa la aproximación asintótica"
    else:
        p_exacta = float(stats.wilcoxon(dnz, alternative=alternativa, method="exact",
                                        zero_method="wilcox").pvalue)
    if p_exacta is not None:
        p, metodo = p_exacta, "exacta"
    else:
        p, metodo = p_asint, "asintótica (Z con corrección por empates)"
    return {
        **base, "w_plus": w_plus, "w_minus": w_minus, "z": float(z),
        "p_asintotica": p_asint, "p_exacta": p_exacta, "motivo_p_exacta": motivo_exacta,
        "p": p, "metodo_p": metodo, "empates": empates,
        "r": float(z / math.sqrt(n_ef)),
        "r_rb": float((w_plus - w_minus) / (w_plus + w_minus)),
        "motivo": None,
    }


def holm_ajuste(pvalores: list[float]) -> list[float]:
    """Ajuste de Holm (step-down) de una familia de p-valores."""
    m = len(pvalores)
    orden = sorted(range(m), key=lambda i: pvalores[i])
    ajustados = [0.0] * m
    previo = 0.0
    for rango, i in enumerate(orden):
        valor = min(1.0, (m - rango) * pvalores[i])
        previo = max(previo, valor)
        ajustados[i] = previo
    return ajustados


def alfa_cronbach(items) -> float | None:
    X = np.asarray(items, dtype=float)
    if X.ndim != 2 or X.shape[1] < 2 or X.shape[0] < 2:
        return None
    k = X.shape[1]
    var_total = X.sum(axis=1).var(ddof=1)
    if var_total == 0:
        return None
    return float(k / (k - 1) * (1 - X.var(axis=0, ddof=1).sum() / var_total))


def correlacion_item_total_corregida(items) -> list[float | None]:
    """r entre cada ítem y la suma de los demás; None si algún lado es constante."""
    X = np.asarray(items, dtype=float)
    salida: list[float | None] = []
    for j in range(X.shape[1]):
        resto = np.delete(X, j, axis=1).sum(axis=1)
        if X[:, j].std() == 0 or resto.std() == 0:
            salida.append(None)
        else:
            salida.append(float(np.corrcoef(X[:, j], resto)[0, 1]))
    return salida


def omega_desde_correlacion(R, max_iter: int = 2000, tol: float = 1e-10) -> tuple[float | None, str | None]:
    """Omega total de McDonald con un factor común (ejes principales iterados).

    Devuelve (omega, motivo_si_None). Caso Heywood o no convergencia -> None.
    """
    R = np.asarray(R, dtype=float)
    k = R.shape[0]
    if k < 3 or not np.isfinite(R).all():
        return None, "se requieren >= 3 ítems con correlaciones definidas"
    try:
        h = 1.0 - 1.0 / np.diag(np.linalg.inv(R))
    except np.linalg.LinAlgError:
        h = np.full(k, 0.5)
    for _ in range(max_iter):
        Rr = R.copy()
        np.fill_diagonal(Rr, h)
        valores, vectores = np.linalg.eigh(Rr)
        lam_max = valores[-1]
        if lam_max <= 0:
            return None, "autovalor dominante no positivo"
        carga = vectores[:, -1] * math.sqrt(lam_max)
        if carga.sum() < 0:
            carga = -carga
        h_nuevo = carga ** 2
        if np.max(np.abs(h_nuevo - h)) < tol:
            h = h_nuevo
            break
        h = h_nuevo
    else:
        return None, "no convergió el ajuste de un factor"
    if (h >= 1.0).any():
        return None, "solución de Heywood (comunalidad >= 1)"
    s = carga.sum()
    return float(s ** 2 / (s ** 2 + (1.0 - h).sum())), None


def confiabilidad_subescala(df: pd.DataFrame, items: list[str]) -> dict:
    X = df[items].to_numpy(dtype=float)
    alfa = alfa_cronbach(X)
    itc = correlacion_item_total_corregida(X)
    if X.shape[0] < 2 or (X.std(axis=0) == 0).any():
        omega, motivo = None, "ítem(s) constante(s): correlación no definida"
    else:
        omega, motivo = omega_desde_correlacion(np.corrcoef(X, rowvar=False))
    return {
        "k_items": len(items), "n": int(X.shape[0]), "alfa_cronbach": alfa,
        "omega_total": omega, "omega_motivo_nulo": motivo,
        "omega_advertencia": "n = 14: la estimación factorial es inestable; interpretar como exploratoria",
        "item_total_corregida": {it: r for it, r in zip(items, itc)},
    }


# ==========================================================================
# Lectura y control de calidad
# ==========================================================================
def _hallazgo(nivel, fase, mensaje, columna=None, sujeto=None) -> dict:
    return {"nivel": nivel, "fase": fase, "columna": columna, "sujeto_id": sujeto, "mensaje": mensaje}


def leer_csv_bytes(contenido: bytes) -> pd.DataFrame:
    """Lee el CSV como texto (sin inferir tipos) para que el QC vea los valores originales."""
    return pd.read_csv(io.BytesIO(contenido), dtype=str, keep_default_na=False, encoding="utf-8-sig")


def control_calidad_fase(df: pd.DataFrame, fase: str) -> tuple[pd.DataFrame | None, list[dict]]:
    """QC niveles N1-N3 de un CSV. Devuelve (DataFrame numérico | None, hallazgos)."""
    h: list[dict] = []
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    faltan = [c for c in COLUMNAS_OBLIGATORIAS if c not in df.columns]
    if faltan:
        h.append(_hallazgo("N1-estructura", fase, f"Faltan columnas obligatorias: {', '.join(faltan)}"))
        return None, h
    # --- N1: estructura ---
    if len(df) != N_ESPERADO:
        h.append(_hallazgo("N1-estructura", fase, f"Se esperaban {N_ESPERADO} filas de datos; hay {len(df)}"))
    ids = df["sujeto_id"].str.strip()
    duplicados = sorted(ids[ids.duplicated()].unique())
    if duplicados:
        h.append(_hallazgo("N1-estructura", fase, f"sujeto_id duplicado(s): {', '.join(duplicados)}"))
    if sorted(ids.tolist()) != IDS_ESPERADOS:
        h.append(_hallazgo("N1-estructura", fase, "sujeto_id debe cubrir exactamente TRAB-01 a TRAB-14"))
    if "fase" in df.columns:
        fases = set(df["fase"].str.strip().str.upper())
        if fases != {fase.upper()}:
            h.append(_hallazgo("N1-estructura", fase,
                               f"La columna 'fase' ({sorted(fases)}) no coincide con la fase del manifiesto ({fase.upper()})",
                               columna="fase"))
    numericas = COLUMNAS_OBLIGATORIAS[1:]
    num = pd.DataFrame({"sujeto_id": ids.values})
    faltantes_celda = False
    for col in numericas:
        bruto = df[col].str.strip()
        es_falt = bruto.str.lower().isin(_TOKENS_FALTANTE)
        for idx in np.flatnonzero(es_falt.to_numpy()):
            faltantes_celda = True
            h.append(_hallazgo("N1-estructura", fase, "Valor faltante", col, ids.iloc[idx]))
        conv = pd.to_numeric(bruto.where(~es_falt), errors="coerce")
        es_inf = np.isinf(conv.to_numpy(dtype=float))
        for idx in np.flatnonzero(es_inf):
            h.append(_hallazgo("N2-rangos", fase, f"Valor no finito: {bruto.iloc[idx]!r}", col, ids.iloc[idx]))
        conv = conv.where(~es_inf)
        for idx in np.flatnonzero((conv.isna() & ~es_falt & ~es_inf).to_numpy()):
            h.append(_hallazgo("N2-rangos", fase, f"Valor no numérico: {bruto.iloc[idx]!r}", col, ids.iloc[idx]))
        num[col] = conv.to_numpy(dtype=float)
    # --- N2: rangos y tipos ---
    for col, (lo, hi, lo_abierto) in RANGOS.items():
        for idx, v in enumerate(num[col]):
            if math.isnan(v):
                continue
            fuera = (v <= lo if lo_abierto else v < lo) or v > hi
            if fuera:
                cierre = "(" if lo_abierto else "["
                h.append(_hallazgo("N2-rangos", fase, f"{v} fuera de rango {cierre}{lo:g}, {hi:g}]", col, ids.iloc[idx]))
    for col in ITEMS_AP + ITEMS_UP:
        for idx, v in enumerate(num[col]):
            if math.isnan(v):
                continue
            if v != int(v) or not 1 <= v <= 5:
                h.append(_hallazgo("N2-rangos", fase, f"{v} no es un entero Likert 1-5", col, ids.iloc[idx]))
    # --- N3: coherencia de scores ---
    for col_score, items in (("score_ap", ITEMS_AP), ("score_up", ITEMS_UP)):
        suma = num[items].sum(axis=1, skipna=False)
        for idx in range(len(num)):
            if math.isnan(suma.iloc[idx]) or math.isnan(num[col_score].iloc[idx]):
                continue
            if num[col_score].iloc[idx] != suma.iloc[idx]:
                h.append(_hallazgo("N3-coherencia", fase,
                                   f"{col_score}={num[col_score].iloc[idx]:g} no coincide con la suma de ítems ({suma.iloc[idx]:g})",
                                   col_score, ids.iloc[idx]))
    total = num["score_ap"] + num["score_up"]
    for idx in range(len(num)):
        if math.isnan(total.iloc[idx]) or math.isnan(num["score_tam_total"].iloc[idx]):
            continue
        if num["score_tam_total"].iloc[idx] != total.iloc[idx]:
            h.append(_hallazgo("N3-coherencia", fase,
                               f"score_tam_total={num['score_tam_total'].iloc[idx]:g} != score_ap + score_up ({total.iloc[idx]:g})",
                               "score_tam_total", ids.iloc[idx]))
    if h:
        return None, h
    return num.sort_values("sujeto_id").reset_index(drop=True), h


def control_calidad_pareo(pre: pd.DataFrame, post: pd.DataFrame) -> list[dict]:
    """N4: pares pre/post completos (mismos sujetos en ambas fases)."""
    h = []
    sp, sq = set(pre["sujeto_id"]), set(post["sujeto_id"])
    for s in sorted(sp - sq):
        h.append(_hallazgo("N4-pareo", "pareo", "Sujeto presente en pretest y ausente en postest", sujeto=s))
    for s in sorted(sq - sp):
        h.append(_hallazgo("N4-pareo", "pareo", "Sujeto presente en postest y ausente en pretest", sujeto=s))
    return h


# ==========================================================================
# Análisis
# ==========================================================================
def analizar(pre: pd.DataFrame, post: pd.DataFrame, alfa: float = 0.05) -> dict:
    """Ejecuta descriptivos, normalidad, contrastes, Holm y confiabilidad (datos ya validados)."""
    desc, contrastes = {}, []
    for etiqueta, col, direccion, ordinal in INDICADORES:
        x_pre, x_post = pre[col].to_numpy(float), post[col].to_numpy(float)
        d = x_post - x_pre
        desc[etiqueta] = {"columna": col, "pretest": descriptivos(x_pre), "postest": descriptivos(x_post),
                          "diferencias": descriptivos(d)}
        norm = shapiro_diferencias(d, alfa)
        prueba = elegir_prueba(norm["normal"], ordinal)
        if prueba == "t_pareada":
            r = t_pareada(x_post, x_pre, direccion)
            coincide = None if r["media_dif"] == 0 else (r["media_dif"] < 0) == (direccion == "less")
        else:
            r = wilcoxon_signo(d, direccion)
            coincide = None if not r["z"] else (r["z"] < 0) == (direccion == "less")
        motivo_prueba = (
            "variable ordinal (Likert): se usa prueba no paramétrica" if ordinal
            else "diferencias no normales o normalidad no evaluable" if prueba == "wilcoxon"
            else "diferencias normales (Shapiro-Wilk)"
        )
        p = r.get("p")
        contrastes.append({
            "indicador": etiqueta, "columna": col, "h1": ETIQUETA_DIRECCION[direccion],
            "alternativa": direccion, "ordinal": ordinal, "normalidad": norm,
            "prueba": prueba, "motivo_prueba": motivo_prueba, "resultado": r,
            "direccion_coincide_h1": coincide, "alfa": alfa,
            "rechaza_h0": (p < alfa) if p is not None else None,
        })
    # Holm (reportado aparte) sobre los contrastes con p definida
    con_p = [i for i, c in enumerate(contrastes) if c["resultado"].get("p") is not None]
    ajustados = holm_ajuste([contrastes[i]["resultado"]["p"] for i in con_p])
    holm = []
    for i, p_aj in zip(con_p, ajustados):
        holm.append({"indicador": contrastes[i]["indicador"], "p": contrastes[i]["resultado"]["p"],
                     "p_holm": p_aj, "rechaza_h0_holm": p_aj < alfa})
    # Total de la Modalidad A: solo descriptivo. No se contrasta porque es una
    # combinación lineal de AP y UP y su prueba sería redundante (ver cabecera).
    desc["Total de la Modalidad A (8 ítems)"] = {
        "columna": "score_tam_total", "pretest": descriptivos(pre["score_tam_total"]),
        "postest": descriptivos(post["score_tam_total"]),
        "diferencias": descriptivos(post["score_tam_total"].to_numpy(float) - pre["score_tam_total"].to_numpy(float)),
    }
    conf = {}
    for fase, df in (("pretest", pre), ("postest", post)):
        conf[fase] = {
            "AP": confiabilidad_subescala(df, ITEMS_AP),
            "UP": confiabilidad_subescala(df, ITEMS_UP),
            "Total": confiabilidad_subescala(df, ITEMS_AP + ITEMS_UP),
        }
    return {"descriptivos": desc, "contrastes": contrastes, "multiplicidad_holm": holm, "confiabilidad": conf}


# ==========================================================================
# Tablas y reporte
# ==========================================================================
def _tabla(id_, titulo, encabezados, filas, nota) -> dict:
    return {"id": id_, "titulo": titulo, "encabezados": encabezados, "filas": filas, "nota": nota}


def construir_tablas(res: dict) -> list[dict]:
    desc = res["descriptivos"]
    filas = []
    for ind, bloque in desc.items():
        for fase in ("pretest", "postest"):
            b = bloque[fase]
            filas.append([ind, fase.capitalize(), fmt_num(b["media"]), fmt_num(b["de"]), fmt_num(b["mediana"]),
                          fmt_num(b["ric"]), fmt_num(b["min"]), fmt_num(b["max"])])
    t1 = _tabla(
        "T1", "Estadísticos descriptivos por indicador y momento de medición",
        ["Indicador", "Momento", "M", "DE", "Mdn", "RIC", "Mín", "Máx"], filas,
        "N = 14. M = media; DE = desviación estándar (n − 1); Mdn = mediana; RIC = rango intercuartílico (Q3 − Q1, interpolación lineal). "
        "AP y UP corresponden a puntajes sumados de 4 ítems cada uno (4-20); el total TAM suma 8 ítems (8-40).")
    filas = []
    for c in res["contrastes"]:
        n = c["normalidad"]
        filas.append([c["indicador"], fmt_num(n["W"], 3), fmt_p(n["p"]),
                      "Normal" if n["normal"] else ("No normal" if n["normal"] is False else "No evaluable"),
                      "t pareada" if c["prueba"] == "t_pareada" else "Wilcoxon", c["motivo_prueba"]])
    t2 = _tabla("T2", "Prueba de normalidad de Shapiro-Wilk sobre las diferencias (postest − pretest) y prueba seleccionada",
                ["Indicador", "W", "p", "Distribución de d", "Prueba", "Criterio"], filas,
                "Regla de decisión: t pareada si la variable es continua y d es normal (p ≥ α); Wilcoxon si d no es normal o la variable es ordinal.")
    filas = []
    for c in res["contrastes"]:
        r = c["resultado"]
        if c["prueba"] == "t_pareada":
            ic = r.get("ic95_dz")
            filas.append([c["indicador"], c["h1"], f"t({r['gl']}) = {fmt_num(r['t'])}", fmt_p(r["p"]),
                          f"dz = {fmt_num(r['dz'])}" + (f" [{fmt_num(ic[0])}, {fmt_num(ic[1])}]" if ic else ""),
                          f"n = {r['n']}", "Sí" if c["rechaza_h0"] else "No"])
        else:
            filas.append([c["indicador"], c["h1"], f"Z = {fmt_num(r['z'])} (W+ = {fmt_num(r['w_plus'], 1)})",
                          fmt_p(r["p"]) + (" (exacta)" if r["metodo_p"] == "exacta" else " (asintótica)" if r["p"] is not None else ""),
                          f"r = {fmt_num(r['r'])}; r_rb = {fmt_num(r['r_rb'])}",
                          f"n efectivo = {r['n_efectivo']}", "Sí" if c["rechaza_h0"] else "No"])
    t3 = _tabla("T3", "Contraste de hipótesis unilateral postest frente a pretest",
                ["Indicador", "H1", "Estadístico", "p", "Tamaño del efecto", "n", f"Rechaza H0 (α = {res['alfa']:g})"], filas,
                "Las diferencias se calculan como postest − pretest; los tamaños de efecto conservan ese signo. dz: d de Cohen para muestras relacionadas con IC 95 % "
                "(t no central). Wilcoxon: ceros descartados (zero_method = wilcox), Z sin corrección de continuidad y con corrección por empates; "
                "r = Z/√n efectivo; r_rb = correlación biserial de rangos pareada.")
    filas = [[h["indicador"], fmt_p(h["p"]), fmt_p(h["p_holm"]), "Sí" if h["rechaza_h0_holm"] else "No"] for h in res["multiplicidad_holm"]]
    total_c = len(res["contrastes"])
    en_familia = {h["indicador"] for h in res["multiplicidad_holm"]}
    excluidos = [c["indicador"] for c in res["contrastes"] if c["indicador"] not in en_familia]
    if excluidos:
        familia = (f"Familia: {len(en_familia)} de {total_c} contrastes de los indicadores de la VD; se excluyen del ajuste "
                   f"por no ser estimables (p no definida): {', '.join(excluidos)}.")
    else:
        familia = f"Familia: los {total_c} contrastes de los indicadores de la VD."
    t4 = _tabla("T4", "Ajuste de multiplicidad de Holm (reportado aparte)",
                ["Indicador", "p", "p ajustada (Holm)", f"Rechaza H0 (α = {res['alfa']:g})"], filas,
                f"{familia} El ajuste no sustituye al contraste individual; la decisión se toma con p ajustada < α = {res['alfa']:g}.")
    filas = []
    for fase in ("pretest", "postest"):
        for esc in ("AP", "UP", "Total"):
            b = res["confiabilidad"][fase][esc]
            itc = [v for v in b["item_total_corregida"].values() if v is not None]
            rango = f"{fmt_num(min(itc))} a {fmt_num(max(itc))}" if itc else "—"
            filas.append([fase.capitalize(), esc, str(b["k_items"]), fmt_num(b["alfa_cronbach"], 3), fmt_num(b["omega_total"], 3), rango])
    t5 = _tabla("T5", "Confiabilidad del cuestionario TAM por subescala y momento",
                ["Momento", "Subescala", "Ítems", "α de Cronbach", "ω total", "r ítem-total corregida (rango)"], filas,
                "ω estimado con un factor común (ejes principales); con n = 14 es inestable y se interpreta como exploratorio. '—' indica no estimable.")
    return [t1, t2, t3, t4, t5]


def tabla_a_markdown(t: dict) -> str:
    enc = "| " + " | ".join(t["encabezados"]) + " |"
    sep = "|" + "|".join("---" for _ in t["encabezados"]) + "|"
    cuerpo = ["| " + " | ".join(str(c) for c in fila) + " |" for fila in t["filas"]]
    return "\n".join([f"**Tabla {t['id'][1:]}**", "", f"*{t['titulo']}*", "", enc, sep, *cuerpo, "", f"*Nota.* {t['nota']}", ""])


def construir_markdown(resultado: dict) -> str:
    pr = resultado["procedencia"]
    L = [
        "# Reporte estadístico inferencial — SIVAC", "",
        f"**Tesis:** {rutas.TITULO_OFICIAL}", "",
        f"**Estado:** {resultado['estado']}  |  **Pipeline:** v{resultado['version_pipeline']}  |  "
        f"**α:** {resultado['alfa']:g}  |  **Semilla:** {resultado['semilla']} (sin remuestreo)", "",
        "## Procedencia certificada", "",
        f"- Responsable: {pr['responsable']}; firmado por {pr['firmado_por']} ({pr['fecha_firma']}).",
        f"- Fecha de recolección: {pr['fecha_recoleccion']}; n esperado: {pr['n_esperado']}.",
        f"- Instrumentos: {', '.join(f'{k} {v}' for k, v in pr['instrumentos_versiones'].items())}.",
        f"- Sello del manifiesto: {pr.get('sello_sha256') or 'sin sello (ejecutar manifest_datos.py sellar)'}.",
        *[f"- {a['fase']}: `{a['nombre']}` SHA-256 `{a['sha256']}`" for a in pr["archivos"]], "",
        "## Control de calidad", "",
        "Niveles aprobados: " + ", ".join(resultado["control_calidad"]["niveles_aprobados"]) + ".", "",
    ]
    for t in resultado["tablas"]:
        L.append(tabla_a_markdown(t))
    L += ["## Entorno", "", "- " + "; ".join(f"{k} {v}" for k, v in resultado["entorno"].items()), ""]
    return "\n".join(L)


# ==========================================================================
# Orquestación
# ==========================================================================
def _bloqueado(errores: list[str]) -> dict:
    return {"estado": manifest_datos.ESTADO_BLOQUEADO, "bloqueado": True, "errores": errores}


def ejecutar(raw: Path, ruta_manifest: Path, salida: Path | None, alfa: float = 0.05) -> tuple[int, dict]:
    """Devuelve (código_de_salida, resultado). Escribe archivos solo si salida no es None y todo pasó."""
    raw, ruta_manifest = Path(raw), Path(ruta_manifest)
    ev = manifest_datos.evaluar(ruta_manifest, raw)
    if not ev["valido"]:
        return 3, _bloqueado(ev["errores"])
    m = ev["manifest"]
    hallazgos: list[dict] = []
    dfs: dict[str, pd.DataFrame] = {}
    archivos = []
    for a in m["archivos"]:
        contenido = (raw / a["nombre"]).read_bytes()
        sha = hashlib.sha256(contenido).hexdigest()
        if sha != a["sha256"]:
            return 3, _bloqueado([f"SHA-256 de {a['nombre']} no coincide con el MANIFEST al momento de la lectura."])
        archivos.append({"nombre": a["nombre"], "fase": a["fase"], "sha256": sha})
        try:
            df_bruto = leer_csv_bytes(contenido)
        except Exception as e:  # CSV ilegible
            hallazgos.append(_hallazgo("N1-estructura", a["fase"], f"CSV ilegible: {e}"))
            continue
        num, h = control_calidad_fase(df_bruto, a["fase"])
        hallazgos += h
        if num is not None:
            dfs[a["fase"]] = num
    if len(dfs) == 2:
        hallazgos += control_calidad_pareo(dfs["pretest"], dfs["postest"])
    if hallazgos:
        return 1, {"estado": "RECHAZADO: el control de calidad detectó errores; no se calculó ningún estadístico",
                   "bloqueado": False, "rechazado_por_calidad": True, "hallazgos": hallazgos}
    pre, post = dfs["pretest"], dfs["postest"]
    res = analizar(pre, post, alfa)
    resultado = {
        "estado": "COMPLETADO", "bloqueado": False, "version_pipeline": VERSION_PIPELINE,
        "semilla": SEMILLA, "remuestreo": "no utilizado", "alfa": alfa,
        "entorno": {"python": sys.version.split()[0], "numpy": np.__version__, "scipy": scipy.__version__,
                    "pandas": pd.__version__},
        "procedencia": {
            "origen": m["origen"], "responsable": m["responsable"], "fecha_recoleccion": m["fecha_recoleccion"],
            "instrumentos_versiones": m["instrumentos_versiones"], "n_esperado": m["n_esperado"],
            "firmado_por": m["firmado_por"], "fecha_firma": m["fecha_firma"],
            "sello_sha256": m.get("sello_sha256"), "archivos": archivos,
        },
        "control_calidad": {"niveles_aprobados": ["N1-estructura", "N2-rangos", "N3-coherencia", "N4-pareo"],
                            "hallazgos": []},
        **res,
    }
    resultado["tablas"] = construir_tablas(resultado)
    resultado = _py(resultado)
    if salida is not None:
        escribir_salidas(resultado, Path(salida))
    return 0, resultado


def escribir_salidas(resultado: dict, salida: Path) -> list[Path]:
    destino = manifest_datos.asegurar_destino_modulo(salida)
    destino.mkdir(parents=True, exist_ok=True)
    p_json, p_md = destino / "resultados_inferenciales.json", destino / "reporte_estadistico.md"
    p_json.write_text(json.dumps(resultado, indent=2, ensure_ascii=False, sort_keys=False) + "\n", encoding="utf-8")
    p_md.write_text(construir_markdown(resultado), encoding="utf-8")
    return [p_json, p_md]


def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Pipeline inferencial SIVAC: solo con datos reales certificados.")
    p.add_argument("--raw", default=str(rutas.DATOS_RAW), help="Carpeta de CSV crudos")
    p.add_argument("--manifest", default=None, help="MANIFEST.json (por defecto <raw>/MANIFEST.json)")
    p.add_argument("--salida", default=str(SALIDA_DEFECTO), help="Carpeta de reportes")
    p.add_argument("--alfa", type=float, default=0.05)
    p.add_argument("--json", action="store_true", help="Imprime el resultado en JSON")
    return p


def main(argv: list[str] | None = None) -> int:
    seguridad.configurar_utf8()
    args = construir_parser().parse_args(argv)
    if not 0 < args.alfa < 1:
        print("--alfa debe estar en (0, 1)", file=sys.stderr)
        return 2
    manifest = Path(args.manifest) if args.manifest else Path(args.raw) / "MANIFEST.json"
    try:
        codigo, res = ejecutar(Path(args.raw), manifest, Path(args.salida), args.alfa)
    except seguridad.EscrituraProhibida as e:
        print(f"ERROR de seguridad: {e}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"Estado: {res['estado']}")
        for e in res.get("errores", []):
            print(f"  - {e}")
        for h in res.get("hallazgos", []):
            ubic = " ".join(str(x) for x in (h["columna"], h["sujeto_id"]) if x)
            print(f"  - [{h['nivel']}] {h['fase']} {ubic}: {h['mensaje']}")
        if codigo == 0:
            print(f"Reportes escritos en {args.salida}")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
