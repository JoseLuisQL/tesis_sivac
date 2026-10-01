# -*- coding: utf-8 -*-
"""
Pruebas de manifest_datos.py y pipeline_inferencial.py.

AVISO: todos los valores numéricos de este archivo son FIXTURES DE PRUEBA
(ejemplos de libro o generados con semilla en tmp_path). No son datos de la
tesis, no se guardan en datos/ y no deben citarse jamás como resultados.

Ejecutar:
    .venv/Scripts/python.exe -m pytest scripts/tests/test_pipeline_inferencial.py -q
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pingouin as pg
import pytest
from scipy import stats

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from scripts.comun import rutas, seguridad  # noqa: E402
from scripts.estadistica import manifest_datos as md  # noqa: E402
from scripts.estadistica import pipeline_inferencial as pi  # noqa: E402

PY = sys.executable

# Ejemplo de libro: Hollander & Wolfe (escala de depresión de Hamilton), n = 9.
# Resultado conocido: W+ = 40, p exacta unilateral = 0.01953125 (= 10/512).
HW_X = np.array([1.83, 0.50, 1.62, 2.48, 1.68, 1.88, 1.55, 3.06, 1.30])
HW_Y = np.array([0.878, 0.647, 0.598, 2.05, 1.06, 1.29, 1.06, 3.14, 1.29])


# --------------------------------------------------------------------------
# Generadores de FIXTURES de prueba (semilla fija, solo en tmp_path)
# --------------------------------------------------------------------------
def _csv_fixture(fase: str, semilla: int, mejora: bool) -> pd.DataFrame:
    rng = np.random.default_rng(semilla)
    n = 14
    base_t = 40 if not mejora else 20
    ap = rng.integers(2 if not mejora else 3, 5 if not mejora else 6, size=(n, 5))
    up = rng.integers(2 if not mejora else 3, 5 if not mejora else 6, size=(n, 5))
    df = pd.DataFrame({"sujeto_id": [f"TRAB-{i:02d}" for i in range(1, n + 1)]})
    df["fase"] = fase.upper()
    df["t_reg"] = np.round(rng.uniform(base_t, base_t + 15, n), 2)
    df["t_vale"] = np.round(rng.uniform(base_t / 4, base_t / 4 + 8, n), 2)
    df["rsd"] = np.round(rng.uniform(60 if not mejora else 85, 80 if not mejora else 99, n), 2)
    df["cpe"] = np.round(rng.uniform(60 if not mejora else 85, 80 if not mejora else 99, n), 2)
    for j in range(5):
        df[f"ap_{j + 1:02d}"] = ap[:, j]
        df[f"up_{j + 1:02d}"] = up[:, j]
    df["score_ap"] = ap.sum(axis=1)
    df["score_up"] = up.sum(axis=1)
    df["score_tam_total"] = df["score_ap"] + df["score_up"]
    return df


def _montar(tmp_path: Path, pre: pd.DataFrame | None = None, post: pd.DataFrame | None = None,
            con_manifest: bool = True) -> tuple[Path, Path]:
    raw = tmp_path / "raw"
    raw.mkdir()
    pre = _csv_fixture("pretest", 1, False) if pre is None else pre
    post = _csv_fixture("postest", 2, True) if post is None else post
    pre.to_csv(raw / "pretest.csv", index=False)
    post.to_csv(raw / "postest.csv", index=False)
    manifest = raw / "MANIFEST.json"
    if con_manifest:
        m = {
            "origen": "campo", "responsable": "Tesista de Prueba", "fecha_recoleccion": "2026-01-15",
            "instrumentos_versiones": {"cuestionario_tam": "v-prueba"}, "n_esperado": 14,
            "archivos": [{"nombre": "pretest.csv", "sha256": "", "fase": "pretest"},
                         {"nombre": "postest.csv", "sha256": "", "fase": "postest"}],
            "declaracion_tesista": md.DECLARACION_LITERAL, "firmado_por": "Tesista de Prueba",
            "fecha_firma": "2026-01-20",
        }
        sellado, err = md.sellar_manifest(m, raw)
        assert not err, err
        manifest.write_text(json.dumps(sellado), encoding="utf-8")
    return raw, manifest


# ==========================================================================
# Estadística contra ejemplos de libro / scipy / pingouin
# ==========================================================================
def test_wilcoxon_libro_hollander_wolfe():
    d = HW_X - HW_Y
    r = pi.wilcoxon_signo(d, "greater")
    assert r["w_plus"] == 40.0 and r["n_efectivo"] == 9 and r["n_ceros"] == 0
    assert r["p_exacta"] == pytest.approx(10 / 512)
    assert r["metodo_p"] == "exacta"
    ref = stats.wilcoxon(d, alternative="greater", method="approx", correction=False)
    assert r["p_asintotica"] == pytest.approx(ref.pvalue, rel=1e-9)
    # Z manual: (40 - 22.5) / sqrt(9*10*19/24)
    assert r["z"] == pytest.approx((40 - 22.5) / math.sqrt(9 * 10 * 19 / 24))
    assert r["r"] == pytest.approx(r["z"] / 3.0)
    assert r["r_rb"] == pytest.approx((40 - 5) / 45)


def test_wilcoxon_empates_y_ceros_contra_scipy_y_pingouin():
    d = np.array([1, 2, 2, -1, 0, 3, 4, -2.0])  # fixture de prueba con empates y un cero
    r = pi.wilcoxon_signo(d, "greater")
    assert r["n_ceros"] == 1 and r["n_efectivo"] == 7 and r["empates"] is True
    assert r["p_exacta"] is None  # con empates no se usa la exacta sin empates
    ref = stats.wilcoxon(d, alternative="greater", method="approx", zero_method="wilcox", correction=False)
    assert r["w_plus"] == ref.statistic
    assert r["z"] == pytest.approx(1.4497648712181508)
    assert r["p_asintotica"] == pytest.approx(ref.pvalue, rel=1e-9)
    assert r["p"] == r["p_asintotica"]
    pgres = pg.wilcoxon(d, alternative="greater")
    assert pgres["W_val"].iloc[0] == r["w_plus"]


def test_wilcoxon_direccion_less_y_todas_nulas():
    d = HW_X - HW_Y
    r = pi.wilcoxon_signo(-d, "less")
    assert r["p_exacta"] == pytest.approx(10 / 512)
    assert r["z"] < 0
    nulo = pi.wilcoxon_signo(np.zeros(5), "greater")
    assert nulo["p"] is None and "nulas" in nulo["motivo"]


def test_t_pareada_contra_scipy_y_pingouin_y_ic_dz():
    post, pre = HW_X, HW_Y  # fixture de libro reutilizado como pares continuos
    r = pi.t_pareada(post, pre, "greater")
    ref = stats.ttest_rel(post, pre, alternative="greater")
    assert r["t"] == pytest.approx(ref.statistic) and r["p"] == pytest.approx(ref.pvalue)
    assert r["gl"] == 8
    d = post - pre
    assert r["dz"] == pytest.approx(d.mean() / d.std(ddof=1))
    pgres = pg.ttest(post, pre, paired=True, alternative="greater")
    assert r["t"] == pytest.approx(pgres["T"].iloc[0]) and r["p"] == pytest.approx(pgres["p_val"].iloc[0])
    # Definición del IC: los extremos invierten la t no central a 0.975 / 0.025
    lo, hi = r["ic95_dz"]
    t_obs = r["dz"] * math.sqrt(9)
    assert stats.nct.cdf(t_obs, 8, lo * 3) == pytest.approx(0.975, abs=1e-6)
    assert stats.nct.cdf(t_obs, 8, hi * 3) == pytest.approx(0.025, abs=1e-6)
    assert lo < r["dz"] < hi


def test_t_pareada_diferencias_constantes_no_definida():
    r = pi.t_pareada(np.array([5.0, 6, 7]), np.array([4.0, 5, 6]), "greater")
    assert r["t"] is None and r["p"] is None and "nula" in r["motivo"]


def test_shapiro_y_regla_de_decision():
    rng = np.random.default_rng(7)
    d = rng.normal(size=14)  # fixture de prueba
    s = pi.shapiro_diferencias(d)
    ref = stats.shapiro(d)
    assert s["W"] == pytest.approx(ref.statistic) and s["p"] == pytest.approx(ref.pvalue)
    assert pi.shapiro_diferencias(np.ones(10))["normal"] is None
    assert pi.elegir_prueba(True, False) == "t_pareada"
    assert pi.elegir_prueba(False, False) == "wilcoxon"
    assert pi.elegir_prueba(True, True) == "wilcoxon"  # ordinal: nunca t
    assert pi.elegir_prueba(None, False) == "wilcoxon"


def test_holm_ejemplo_conocido():
    aj = pi.holm_ajuste([0.01, 0.04, 0.03, 0.005])
    assert aj == pytest.approx([0.03, 0.06, 0.06, 0.02])


def test_descriptivos_contra_numpy():
    x = [2, 4, 4, 4, 5, 5, 7, 9]  # ejemplo de libro: media 5, DE poblacional 2
    d = pi.descriptivos(x)
    assert d["media"] == 5.0 and d["mediana"] == 4.5
    assert d["de"] == pytest.approx(np.std(x, ddof=1))
    assert d["ric"] == pytest.approx(np.percentile(x, 75) - np.percentile(x, 25))


def test_alfa_cronbach_contra_pingouin_e_item_total():
    rng = np.random.default_rng(11)
    latente = rng.normal(size=40)
    X = np.column_stack([latente + rng.normal(scale=0.8, size=40) for _ in range(5)])  # fixture
    df = pd.DataFrame(X, columns=list("abcde"))
    assert pi.alfa_cronbach(X) == pytest.approx(pg.cronbach_alpha(df)[0])
    itc = pi.correlacion_item_total_corregida(X)
    assert itc[0] == pytest.approx(np.corrcoef(X[:, 0], X[:, 1:].sum(axis=1))[0, 1])


def test_omega_un_factor_valor_analitico():
    # Correlaciones de un factor con cargas 0.8: omega = (4*.8)^2 / ((4*.8)^2 + 4*(1-.64)) = 0.87671...
    R = np.full((4, 4), 0.64)
    np.fill_diagonal(R, 1.0)
    om, motivo = pi.omega_desde_correlacion(R)
    assert motivo is None
    assert om == pytest.approx(10.24 / (10.24 + 1.44), abs=1e-6)
    om2, motivo2 = pi.omega_desde_correlacion(np.eye(2))
    assert om2 is None and motivo2


def test_formato_p_apa():
    assert pi.fmt_p(0.0004) == "< .001"
    assert pi.fmt_p(0.0196) == ".020"
    assert pi.fmt_p(0.5) == ".500"
    assert pi.fmt_p(None) == "—"


# ==========================================================================
# Control de calidad
# ==========================================================================
def test_qc_acepta_fixture_valido():
    num, h = pi.control_calidad_fase(pi.leer_csv_bytes(_csv_fixture("pretest", 1, False).to_csv(index=False).encode()), "pretest")
    assert h == [] and len(num) == 14


@pytest.mark.parametrize("col,valor,nivel", [
    ("t_reg", 0, "N2-rangos"),          # intervalo abierto en 0
    ("t_reg", 121, "N2-rangos"),
    ("t_vale", 60.5, "N2-rangos"),
    ("rsd", 100.5, "N2-rangos"),
    ("cpe", -1, "N2-rangos"),
    ("ap_01", 6, "N2-rangos"),
    ("up_02", 2.5, "N2-rangos"),
    ("t_reg", "abc", "N2-rangos"),
    ("score_ap", 99, "N3-coherencia"),
    ("score_tam_total", 1, "N3-coherencia"),
    ("t_vale", "", "N1-estructura"),
    ("rsd", "NA", "N1-estructura"),
])
def test_qc_rechaza_valores_invalidos(col, valor, nivel):
    df = _csv_fixture("pretest", 1, False).astype(object)
    df.loc[3, col] = valor
    num, h = pi.control_calidad_fase(pi.leer_csv_bytes(df.to_csv(index=False).encode()), "pretest")
    assert num is None and any(x["nivel"] == nivel for x in h)


def test_qc_estructura_filas_ids_y_columnas():
    df = _csv_fixture("pretest", 1, False)
    _, h = pi.control_calidad_fase(pi.leer_csv_bytes(df.iloc[:13].to_csv(index=False).encode()), "pretest")
    assert any("filas" in x["mensaje"] for x in h)
    dup = df.copy(); dup.loc[1, "sujeto_id"] = "TRAB-01"
    _, h = pi.control_calidad_fase(pi.leer_csv_bytes(dup.to_csv(index=False).encode()), "pretest")
    assert any("duplicado" in x["mensaje"] for x in h)
    sin_col = df.drop(columns=["cpe"])
    _, h = pi.control_calidad_fase(pi.leer_csv_bytes(sin_col.to_csv(index=False).encode()), "pretest")
    assert any("cpe" in x["mensaje"] for x in h)
    mal_fase = df.copy(); mal_fase["fase"] = "POSTEST"
    _, h = pi.control_calidad_fase(pi.leer_csv_bytes(mal_fase.to_csv(index=False).encode()), "pretest")
    assert any(x["columna"] == "fase" for x in h)


def test_qc_pareo_incompleto():
    a = _csv_fixture("pretest", 1, False)
    num_a, _ = pi.control_calidad_fase(pi.leer_csv_bytes(a.to_csv(index=False).encode()), "pretest")
    b = num_a.copy(); b.loc[0, "sujeto_id"] = "TRAB-99"
    assert pi.control_calidad_pareo(num_a, b)


# ==========================================================================
# Manifiesto
# ==========================================================================
def test_plantilla_es_vacia_y_no_valida():
    p = md.plantilla_manifest()
    assert p["declaracion_tesista"] == "" and p["firmado_por"] == "" and p["origen"] == ""
    assert md.validar_estructura(p)  # inválida a propósito


def test_sellar_no_rellena_declaracion(tmp_path):
    raw, _ = _montar(tmp_path, con_manifest=False)
    m = {"origen": "campo", "responsable": "T", "fecha_recoleccion": "2026-01-15",
         "instrumentos_versiones": {"q": "1"}, "n_esperado": 14,
         "archivos": [{"nombre": "pretest.csv", "sha256": "", "fase": "pretest"},
                      {"nombre": "postest.csv", "sha256": "", "fase": "postest"}],
         "declaracion_tesista": "", "firmado_por": "", "fecha_firma": ""}
    sellado, err = md.sellar_manifest(m, raw)
    assert sellado is None and any("declaracion_tesista" in e for e in err)
    m["declaracion_tesista"] = "texto distinto"
    assert md.sellar_manifest(m, raw)[0] is None


def test_manifest_detecta_alteracion_de_archivo_y_csv_no_declarado(tmp_path):
    raw, manifest = _montar(tmp_path)
    assert md.evaluar(manifest, raw)["valido"]
    (raw / "postest.csv").write_text("alterado", encoding="utf-8")
    ev = md.evaluar(manifest, raw)
    assert not ev["valido"] and any("SHA-256" in e for e in ev["errores"])
    (tmp_path / "otro").mkdir()
    raw2, manifest2 = _montar(tmp_path / "otro")
    (raw2 / "extra.csv").write_text("x", encoding="utf-8")
    assert any("sin declarar" in e for e in md.evaluar(manifest2, raw2)["errores"])


def test_manifest_rechaza_n_distinto_y_origen_distinto_y_sello_manipulado(tmp_path):
    raw, manifest = _montar(tmp_path)
    m = json.loads(manifest.read_text(encoding="utf-8"))
    for campo, valor in (("n_esperado", 13), ("origen", "simulado"), ("declaracion_tesista", "x")):
        malo = dict(m); malo[campo] = valor
        assert md.validar_estructura(malo)
    manip = dict(m); manip["responsable"] = "Otro"
    manifest.write_text(json.dumps(manip), encoding="utf-8")
    assert any("sello" in e for e in md.evaluar(manifest, raw)["errores"])


# ==========================================================================
# Pipeline: bloqueo, rechazo y corrida completa
# ==========================================================================
def test_sin_manifiesto_bloquea_y_no_produce_cifras(tmp_path):
    raw, manifest = _montar(tmp_path, con_manifest=False)
    salida = tmp_path / "salida"
    codigo, res = pi.ejecutar(raw, manifest, salida)
    assert codigo == 3 and res["estado"] == "BLOQUEADO: esperando datos de campo"
    assert set(res) == {"estado", "bloqueado", "errores"}  # ninguna cifra
    assert not salida.exists()


def test_cli_sin_manifiesto_exit_3(tmp_path):
    raw = tmp_path / "raw"; raw.mkdir()
    p = subprocess.run([PY, str(RAIZ / "scripts/estadistica/pipeline_inferencial.py"), "--raw", str(raw),
                        "--salida", str(tmp_path / "s"), "--json"], capture_output=True, text=True, encoding="utf-8")
    assert p.returncode == 3
    assert json.loads(p.stdout)["estado"] == "BLOQUEADO: esperando datos de campo"
    assert not (tmp_path / "s").exists()


def test_valor_fuera_de_rango_rechaza_lote_sin_estadisticos(tmp_path):
    pre = _csv_fixture("pretest", 1, False)
    pre.loc[0, "t_reg"] = 500.0
    raw, manifest = _montar(tmp_path, pre=pre)
    salida = tmp_path / "salida"
    codigo, res = pi.ejecutar(raw, manifest, salida)
    assert codigo == 1 and res["rechazado_por_calidad"]
    assert any(h["columna"] == "t_reg" and h["sujeto_id"] == "TRAB-01" for h in res["hallazgos"])
    assert "contrastes" not in res and not salida.exists()


def test_archivo_alterado_tras_sellar_bloquea(tmp_path):
    raw, manifest = _montar(tmp_path)
    with open(raw / "pretest.csv", "a", encoding="utf-8") as f:
        f.write("\n")
    codigo, res = pi.ejecutar(raw, manifest, tmp_path / "s")
    assert codigo == 3 and "contrastes" not in res


def test_corrida_completa_fixture_y_reproducibilidad(tmp_path):
    raw, manifest = _montar(tmp_path)
    s1, s2 = tmp_path / "s1", tmp_path / "s2"
    c1, r1 = pi.ejecutar(raw, manifest, s1)
    c2, r2 = pi.ejecutar(raw, manifest, s2)
    assert c1 == 0 and c2 == 0
    assert (s1 / "resultados_inferenciales.json").read_text(encoding="utf-8") == (s2 / "resultados_inferenciales.json").read_text(encoding="utf-8")
    assert (s1 / "reporte_estadistico.md").is_file()
    por_ind = {c["indicador"]: c for c in r1["contrastes"]}
    assert set(por_ind) == {"T_reg", "T_vale", "RSD", "CPE", "AP", "UP"}
    assert por_ind["AP"]["prueba"] == "wilcoxon" and por_ind["UP"]["prueba"] == "wilcoxon"
    assert por_ind["T_reg"]["alternativa"] == "less" and por_ind["RSD"]["alternativa"] == "greater"
    assert len(r1["multiplicidad_holm"]) == 6
    assert {t["id"] for t in r1["tablas"]} == {"T1", "T2", "T3", "T4", "T5"}
    # Contraste con scipy sobre los mismos datos
    pre = pd.read_csv(raw / "pretest.csv").sort_values("sujeto_id")
    post = pd.read_csv(raw / "postest.csv").sort_values("sujeto_id")
    ref = stats.ttest_rel(post["t_reg"], pre["t_reg"], alternative="less")
    if por_ind["T_reg"]["prueba"] == "t_pareada":
        assert por_ind["T_reg"]["resultado"]["p"] == pytest.approx(ref.pvalue, abs=1e-9)
    assert por_ind["T_reg"]["direccion_coincide_h1"] is True
    assert r1["confiabilidad"]["pretest"]["AP"]["k_items"] == 5


def test_no_escribe_en_datos_raw_ni_protegidas(tmp_path):
    raw, manifest = _montar(tmp_path)
    with pytest.raises(seguridad.EscrituraProhibida):
        pi.escribir_salidas({"procedencia": {}}, rutas.DATOS_RAW)
    with pytest.raises(seguridad.EscrituraProhibida):
        pi.escribir_salidas({}, rutas.MODELOS_TESIS / "x")


# ==========================================================================
# CLI del manifiesto sobre el repo (sin tocar datos/raw)
# ==========================================================================
def test_cli_manifest_validar_bloqueado_y_plantilla(tmp_path):
    script = str(RAIZ / "scripts/estadistica/manifest_datos.py")
    p = subprocess.run([PY, script, "validar", "--manifest", str(tmp_path / "no.json"), "--raw", str(tmp_path)],
                       capture_output=True, text=True, encoding="utf-8")
    assert p.returncode == 3 and "BLOQUEADO" in p.stdout
    out = tmp_path / "plantilla.json"
    p = subprocess.run([PY, script, "plantilla", "--salida", str(out)], capture_output=True, text=True, encoding="utf-8")
    assert p.returncode == 0
    contenido = json.loads(out.read_text(encoding="utf-8"))
    assert contenido["declaracion_tesista"] == "" and contenido["archivos"][0]["sha256"] == ""


# ==========================================================================
# Regresiones del informe del verificador (valores = FIXTURES de prueba)
# ==========================================================================
@pytest.mark.parametrize("t", [-12.0, -8.23, -2.56, -0.5, 0.0, 0.3, 2.0, 2.56, 4.0, 8.0, 8.23, 12.0, 20.0, 30.0])
def test_ic_dz_siempre_definido_e_invierte_la_t_no_central(t):
    n = 14
    r = pi.ic_dz(t / math.sqrt(n), n)
    assert r is not None, f"IC de dz no definido para t = {t}"
    lo, hi = r
    assert lo < hi
    assert stats.nct.cdf(t, n - 1, lo * math.sqrt(n)) == pytest.approx(0.975, abs=1e-6)
    assert stats.nct.cdf(t, n - 1, hi * math.sqrt(n)) == pytest.approx(0.025, abs=1e-6)


def test_ic_dz_referencia_independiente_y_simetria():
    n = 14
    lo, hi = pi.ic_dz(8.23 / math.sqrt(n), n)
    assert lo * math.sqrt(n) == pytest.approx(4.4957, abs=1e-3)  # brentq independiente del verificador
    lo2, hi2 = pi.ic_dz(-8.23 / math.sqrt(n), n)
    assert (lo2, hi2) == pytest.approx((-hi, -lo), abs=1e-8)


def test_t_pareada_moderada_trae_ic_dz():
    rng = np.random.default_rng(1)
    pre = rng.normal(30, 5, 14)
    post = pre - 0.68 * 5 + rng.normal(0, 5, 14)
    r = pi.t_pareada(post, pre, "less")
    assert r["ic95_dz"] is not None and r["ic95_dz"][0] < r["dz"] < r["ic95_dz"][1]


@pytest.mark.parametrize("destino", ["referencias/x", "referencias", "referencias/../referencias/y",
                                     "referencias/modelos_tesis/z"])
def test_salida_en_referencias_prohibida(destino):
    ruta = rutas.RAIZ / destino
    with pytest.raises(seguridad.EscrituraProhibida):
        md.asegurar_destino_modulo(ruta)
    with pytest.raises(seguridad.EscrituraProhibida):
        pi.escribir_salidas({"procedencia": {}}, ruta)
    assert not (rutas.REFERENCIAS / "x").exists()


def test_pipeline_ejecutar_no_escribe_en_referencias(tmp_path):
    raw, manifest = _montar(tmp_path)
    with pytest.raises(seguridad.EscrituraProhibida):
        pi.ejecutar(raw, manifest, rutas.REFERENCIAS / "x")
    assert not (rutas.REFERENCIAS / "x").exists()


def test_cli_salida_referencias_exit_1(tmp_path):
    raw, manifest = _montar(tmp_path)
    p = subprocess.run([PY, str(RAIZ / "scripts/estadistica/pipeline_inferencial.py"), "--raw", str(raw),
                        "--manifest", str(manifest), "--salida", str(rutas.REFERENCIAS / "x")],
                       capture_output=True, text=True, encoding="utf-8")
    assert p.returncode == 1 and "seguridad" in p.stderr
    assert not (rutas.REFERENCIAS / "x").exists()


@pytest.mark.parametrize("col,valor", [("ap_01", "inf"), ("rsd", "inf"), ("t_reg", "-inf"), ("score_ap", "-inf")])
def test_valores_infinitos_rechazan_lote_sin_traceback(tmp_path, col, valor):
    post = _csv_fixture("postest", 2, True).astype({col: object})
    post.loc[0, col] = valor
    raw, manifest = _montar(tmp_path, post=post)
    codigo, res = pi.ejecutar(raw, manifest, None)
    assert codigo == 1 and res["rechazado_por_calidad"]
    assert any(h["columna"] == col and "no finito" in h["mensaje"] for h in res["hallazgos"])
    assert "contrastes" not in res


def test_manifest_no_utf8_bloquea_con_exit_3(tmp_path):
    raw, manifest = _montar(tmp_path)
    manifest.write_bytes(b'{"origen": "camp\xf3"}')
    ev = md.evaluar(manifest, raw)
    assert not ev["valido"] and any("UTF-8" in e for e in ev["errores"])
    codigo, res = pi.ejecutar(raw, manifest, None)
    assert codigo == 3 and res["bloqueado"]
    p = subprocess.run([PY, str(RAIZ / "scripts/estadistica/manifest_datos.py"), "validar",
                        "--manifest", str(manifest), "--raw", str(raw)],
                       capture_output=True, text=True, encoding="utf-8")
    assert p.returncode == 3 and "BLOQUEADO" in p.stdout
    p = subprocess.run([PY, str(RAIZ / "scripts/estadistica/pipeline_inferencial.py"), "--raw", str(raw),
                        "--manifest", str(manifest), "--salida", str(tmp_path / "s")],
                       capture_output=True, text=True, encoding="utf-8")
    assert p.returncode == 3 and "Traceback" not in p.stderr


def test_holm_nota_coherente_con_contrastes_no_estimables_y_alfa(tmp_path):
    pre = _csv_fixture("pretest", 1, False)
    post = _csv_fixture("postest", 2, True)
    for col in [f"ap_{i:02d}" for i in range(1, 6)] + [f"up_{i:02d}" for i in range(1, 6)]:
        post[col] = pre[col]
    post["score_ap"], post["score_up"] = pre["score_ap"], pre["score_up"]
    post["score_tam_total"] = pre["score_tam_total"]
    raw, manifest = _montar(tmp_path, pre=pre, post=post)
    codigo, res = pi.ejecutar(raw, manifest, tmp_path / "s", alfa=0.10)
    assert codigo == 0 and len(res["multiplicidad_holm"]) == 4
    t4 = next(t for t in res["tablas"] if t["id"] == "T4")
    assert "seis" not in t4["nota"] and "4 de 6" in t4["nota"] and "AP" in t4["nota"] and "UP" in t4["nota"]
    assert "α = 0.1" in t4["encabezados"][-1]
    t3 = next(t for t in res["tablas"] if t["id"] == "T3")
    assert "α = 0.1" in t3["encabezados"][-1]


def test_ruta_legada_sin_manifiesto_queda_bloqueada(tmp_path):
    script = str(RAIZ / "scripts/estadistica/analisis_estadistico_sivac.py")
    p = subprocess.run([PY, script], capture_output=True, text=True, encoding="utf-8", cwd=str(tmp_path))
    assert p.returncode == 3 and "BLOQUEADO" in p.stdout
