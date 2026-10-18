#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA WEB SIVAC — PIPELINE DE ANÁLISIS ESTADÍSTICO REPRODUCIBLE (FASE 6 / 7)
Proyecto de Tesis — Escuela Profesional de Ingeniería de Sistemas — UNAJMA
Autor: Analista Estadístico (analista-estadistico)
Directriz: Cero Alucinaciones, Verificabilidad Matemática Total y Formato APA 7.
"""

import os
import sys
import hashlib
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.comun import rutas, seguridad  # noqa: E402
from scripts.estadistica import manifest_datos  # noqa: E402

def calcular_sha256(ruta_archivo):
    """Calcula el hash SHA-256 de un archivo para control de integridad."""
    sha256 = hashlib.sha256()
    with open(ruta_archivo, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def validar_matriz(df, fase_esperada):
    """Ejecuta los controles de calidad de nivel 1, 2 y 3 sobre un DataFrame."""
    print(f"[*] Validando matriz para fase: {fase_esperada}...")

    # 1. Integridad estructural
    assert len(df) == 14, f"Error: Se esperaban 14 sujetos censales, se encontraron {len(df)}."
    assert "sujeto_id" in df.columns, "Error: Falta la columna 'sujeto_id'."

    # Verificar códigos de sujeto TRAB-01 a TRAB-14
    codigos_esperados = [f"TRAB-{i:02d}" for i in range(1, 15)]
    codigos_reales = sorted(df["sujeto_id"].tolist())
    assert codigos_reales == codigos_esperados, f"Error en códigos de sujeto: {codigos_reales}"

    # 2. Cero valores nulos
    assert not df.isnull().values.any(), "Error: La matriz contiene celdas nulas o vacías."

    # 3. Verificación de cotas de rango
    assert (df["t_reg"] > 0).all() and (df["t_reg"] <= 120).all(), "Error en rango de t_reg (0, 120]."
    assert (df["t_vale"] > 0).all() and (df["t_vale"] <= 60).all(), "Error en rango de t_vale (0, 60]."
    assert (df["rsd"] >= 0).all() and (df["rsd"] <= 100).all(), "Error en rango de rsd [0, 100]."
    assert (df["cpe"] >= 0).all() and (df["cpe"] <= 100).all(), "Error en rango de cpe [0, 100]."

    # Ítems TAM (Modalidad A: 4 ítems AP + 4 ítems UP = 8 ítems)
    items_tam = [f"ap_{i:02d}" for i in range(1, 5)] + [f"up_{i:02d}" for i in range(1, 5)]
    for col in items_tam:
        assert col in df.columns, f"Error: Falta el ítem {col}."
        assert df[col].isin([1, 2, 3, 4, 5]).all(), f"Error en reactivo {col}: valores fuera de 1-5."

    # Consistencia aritmética TAM
    calc_ap = df[[f"ap_{i:02d}" for i in range(1, 5)]].sum(axis=1)
    calc_up = df[[f"up_{i:02d}" for i in range(1, 5)]].sum(axis=1)
    calc_total = calc_ap + calc_up

    assert (df["score_ap"] == calc_ap).all(), "Error: Inconsistencia en score_ap (rango 4-20)."
    assert (df["score_up"] == calc_up).all(), "Error: Inconsistencia en score_up (rango 4-20)."
    assert (df["score_tam_total"] == calc_total).all(), "Error: Inconsistencia en score_tam_total (rango 8-40)."

    print(f"    [OK] Matriz {fase_esperada} validada exitosamente (14 observaciones conformes).")
    return True

def calcular_alfa_cronbach(df_items):
    """
    Calcula el Coeficiente Alfa de Cronbach para una matriz de ítems (n_obs x k_items).
    Fórmula: alpha = (k / (k - 1)) * (1 - sum(var_i) / var_total)
    """
    k = df_items.shape[1]
    if k <= 1:
        return 0.0
    var_items = df_items.var(axis=0, ddof=1)
    puntuacion_total = df_items.sum(axis=1)
    var_total = puntuacion_total.var(ddof=1)

    if var_total == 0:
        return 1.0
    alpha = (k / (k - 1.0)) * (1.0 - (var_items.sum() / var_total))
    return float(alpha)

def analisis_discriminacion_items(df_items):
    """Calcula la correlación corregida ítem-total (r_itc) y el alfa si el ítem es eliminado."""
    k = df_items.shape[1]
    resultados = []
    puntuacion_total = df_items.sum(axis=1)

    for col in df_items.columns:
        # Puntuación total sin el ítem actual
        total_sin_item = puntuacion_total - df_items[col]
        # Correlación de Pearson corregida
        r_itc, _ = stats.pearsonr(df_items[col], total_sin_item)
        # Alfa sin este ítem
        sub_df = df_items.drop(columns=[col])
        alpha_drop = calcular_alfa_cronbach(sub_df)

        resultados.append({
            "item": col.upper(),
            "media_item": df_items[col].mean(),
            "desv_item": df_items[col].std(ddof=1),
            "r_itc": r_itc,
            "alfa_si_eliminado": alpha_drop
        })
    return pd.DataFrame(resultados)

def ejecutar_prueba_shapiro(diferencias, nombre_variable):
    """Ejecuta la prueba de bondad de ajuste de Shapiro-Wilk para muestras reducidas."""
    stat_w, p_val = stats.shapiro(diferencias)
    normal = p_val > 0.05
    return {
        "variable": nombre_variable,
        "estadistico_W": stat_w,
        "p_valor": p_val,
        "distribucion_normal": normal,
        "decision": "Distribución Normal (p > 0.05)" if normal else "Distribución No Normal (p <= 0.05)"
    }

def ejecutar_prueba_wilcoxon(x_post, x_pre, nombre_variable, direccion_esperada="mayor"):
    """
    Ejecuta la prueba de rangos con signo de Wilcoxon para muestras relacionadas.
    Calcula: estadístico W, p-valor bilateral y unilateral, Z asintótico y tamaño de efecto r de Rosenthal.
    """
    diff = x_post - x_pre
    n = len(diff)

    # scipy.stats.wilcoxon
    # Si direccion esperada es 'menor' (tiempos), alternative='less' (x_post < x_pre)
    # Si direccion esperada es 'mayor' (satisfaccion/consistencia), alternative='greater' (x_post > x_pre)
    alt = "less" if direccion_esperada == "menor" else "greater"

    res_wilcoxon = stats.wilcoxon(x_post, x_pre, alternative=alt)
    res_two_sided = stats.wilcoxon(x_post, x_pre, alternative="two-sided")

    # Calcular Z tipificado a partir del p-valor bilateral
    # Z = norm.ppf(1 - p_two_sided / 2) con signo según la dirección
    z_score = stats.norm.ppf(1.0 - (res_two_sided.pvalue / 2.0))
    if direccion_esperada == "menor" and (diff.mean() > 0):
        z_score = -abs(z_score)
    elif direccion_esperada == "mayor" and (diff.mean() < 0):
        z_score = -abs(z_score)
    else:
        z_score = abs(z_score)

    # Tamaño del efecto r de Rosenthal: r = |Z| / sqrt(2*n)
    r_rosenthal = abs(z_score) / np.sqrt(2.0 * n)

    # Magnitud de Cohen (1988)
    if r_rosenthal < 0.10:
        magnitud = "Despreciable"
    elif r_rosenthal < 0.30:
        magnitud = "Pequeño"
    elif r_rosenthal < 0.50:
        magnitud = "Mediano"
    else:
        magnitud = "Grande (Fuerte impacto)"

    return {
        "variable": nombre_variable,
        "n_pares": n,
        "estadistico_W": res_wilcoxon.statistic,
        "z_score": z_score,
        "p_valor_unilateral": res_wilcoxon.pvalue,
        "p_valor_bilateral": res_two_sided.pvalue,
        "r_rosenthal": r_rosenthal,
        "magnitud_efecto": magnitud,
        "decision": "Rechazar H0 (p <= 0.05)" if res_wilcoxon.pvalue <= 0.05 else "No rechazar H0"
    }

def ejecutar_prueba_t_student(x_post, x_pre, nombre_variable, direccion_esperada="mayor"):
    """Prueba paramétrica complementaria t de Student para muestras relacionadas."""
    diff = x_post - x_pre
    n = len(diff)
    gl = n - 1

    alt = "less" if direccion_esperada == "menor" else "greater"
    res_t = stats.ttest_rel(x_post, x_pre, alternative=alt)

    # d de Cohen para muestras relacionadas: d = mean(diff) / std(diff)
    d_cohen = abs(diff.mean()) / diff.std(ddof=1)

    return {
        "variable": nombre_variable,
        "gl": gl,
        "estadistico_t": res_t.statistic,
        "p_valor": res_t.pvalue,
        "d_cohen": d_cohen,
        "decision": "Rechazar H0 (p <= 0.05)" if res_t.pvalue <= 0.05 else "No rechazar H0"
    }

def df_a_markdown(df):
    """Convierte un DataFrame a Markdown sin depender de tabulate."""
    headers = [str(c) for c in df.columns]
    filas = []
    for _, row in df.iterrows():
        filas.append([str(v) for v in row.values])
    header_str = "| " + " | ".join(headers) + " |"
    sep_str = "| " + " | ".join(["---"] * len(headers)) + " |"
    body_str = "\n".join(["| " + " | ".join(f) + " |" for f in filas])
    return f"{header_str}\n{sep_str}\n{body_str}"

def generar_reporte_estadistico_completo(ruta_pretest, ruta_postest, ruta_salida_md):
    """Pipeline integral que procesa los datos reales y genera las tablas para el Capítulo V."""
    print("=" * 80)
    print("SIVAC-THESIS-LAB: INICIANDO PIPELINE DE ANÁLISIS ESTADÍSTICO INFERENCIAL")
    print("=" * 80)

    # Compuerta de procedencia: sin MANIFEST válido (datos reales certificados) no se calcula nada.
    dir_raw = os.path.dirname(os.path.abspath(ruta_pretest))
    ev = manifest_datos.evaluar(os.path.join(dir_raw, "MANIFEST.json"), dir_raw)
    if not ev["valido"]:
        print(f"[!] Estado: {manifest_datos.ESTADO_BLOQUEADO}")
        for e in ev["errores"]:
            print(f"  - {e}")
        print("[!] Use scripts/estadistica/pipeline_inferencial.py (vía oficial) una vez sellado datos/raw/MANIFEST.json.")
        return False
    if os.path.dirname(os.path.abspath(ruta_postest)) != dir_raw:
        print("[!] Pretest y postest deben estar en la misma carpeta certificada por el MANIFEST.")
        return False
    if not os.path.exists(ruta_pretest) or not os.path.exists(ruta_postest):
        print(f"[!] Error: Faltan archivos de datos:\n  Pretest: {ruta_pretest}\n  Postest: {ruta_postest}")
        print("[!] Estado: BLOQUEADO (Esperando entrega de datos de campo por el tesista).")
        return False

    df_pre = pd.read_csv(ruta_pretest)
    df_post = pd.read_csv(ruta_postest)

    # 1. Validar matrices
    validar_matriz(df_pre, "PRETEST")
    validar_matriz(df_post, "POSTEST")

    # 2. Generar matriz pareada
    df_pre_sorted = df_pre.sort_values("sujeto_id").reset_index(drop=True)
    df_post_sorted = df_post.sort_values("sujeto_id").reset_index(drop=True)

    indicadores = [
        ("t_reg", "Tiempo de Registro de Movimientos (min)", "menor"),
        ("t_vale", "Tiempo de Emisión de Vales (min)", "menor"),
        ("rsd", "% Registros sin Discrepancias", "mayor"),
        ("cpe", "% Entregas con Cantidad Conforme", "mayor"),
        ("score_ap", "Aceptación del Proceso (TAM - AP)", "mayor"),
        ("score_up", "Utilidad Percibida (TAM - UP)", "mayor"),
        ("score_tam_total", "Puntaje Total de Satisfacción TAM", "mayor")
    ]

    # Rangos declarados de los puntajes TAM (Instrumento 03, Modalidad A: 8 ítems)
    rangos_tam = {"score_ap": (4, 20), "score_up": (4, 20), "score_tam_total": (8, 40)}
    for col, (lo, hi) in rangos_tam.items():
        fuera = (df_pre_sorted[col] < lo) | (df_pre_sorted[col] > hi) | \
                (df_post_sorted[col] < lo) | (df_post_sorted[col] > hi)
        assert not fuera.any(), f"Error de rango declarado: {col} debe estar en [{lo}, {hi}]."

    # 3. Confiabilidad de Cronbach para Instrumento TAM (Modalidad A, k = 8)
    items_tam = [f"ap_{i:02d}" for i in range(1, 5)] + [f"up_{i:02d}" for i in range(1, 5)]
    alfa_pre = calcular_alfa_cronbach(df_pre_sorted[items_tam])
    alfa_post = calcular_alfa_cronbach(df_post_sorted[items_tam])
    discrim_post = analisis_discriminacion_items(df_post_sorted[items_tam])

    print("\n[+] CONFIABILIDAD PSICOMÉTRICA (ALFA DE CRONBACH - TAM):")
    print(f"    - Pretest:  alpha = {alfa_pre:.4f}")
    print(f"    - Postest:  alpha = {alfa_post:.4f}")

    # 4. Pruebas de Normalidad (Shapiro-Wilk)
    print("\n[+] PRUEBAS DE NORMALIDAD DE SHAPIRO-WILK (DIFERENCIAS PAREADAS):")
    shapiro_resultados = []
    for col, desc, _ in indicadores:
        diff = df_post_sorted[col] - df_pre_sorted[col]
        res_sh = ejecutar_prueba_shapiro(diff, desc)
        shapiro_resultados.append(res_sh)
        print(f"    - {desc:45s}: W = {res_sh['estadistico_W']:.4f}, p = {res_sh['p_valor']:.4e} -> {res_sh['decision']}")

    # 5. Contrastes de Hipótesis Inferencial (Wilcoxon y t-Student)
    print("\n[+] CONTRASTES DE HIPÓTESIS INFERENCIAL (WILCOXON & T-STUDENT):")
    wilcoxon_resultados = []
    ttest_resultados = []

    for col, desc, direc in indicadores:
        res_w = ejecutar_prueba_wilcoxon(df_post_sorted[col], df_pre_sorted[col], desc, direccion_esperada=direc)
        res_t = ejecutar_prueba_t_student(df_post_sorted[col], df_pre_sorted[col], desc, direccion_esperada=direc)
        wilcoxon_resultados.append(res_w)
        ttest_resultados.append(res_t)
        print(f"    - {desc:45s}: Z = {res_w['z_score']:.3f}, p = {res_w['p_valor_unilateral']:.4e}, r = {res_w['r_rosenthal']:.3f} ({res_w['magnitud_efecto']})")

    print(f"\n[+] Guardando reporte formal en Markdown: {ruta_salida_md}")

    # Escritura del informe Markdown
    ruta_salida_md = str(manifest_datos.asegurar_destino_modulo(ruta_salida_md))
    os.makedirs(os.path.dirname(ruta_salida_md), exist_ok=True)
    with open(ruta_salida_md, "w", encoding="utf-8") as f:
        f.write("# RESULTADOS ESTADÍSTICOS INFERENCIALES Y DESCRIPTIVOS — PROYECTO SIVAC\n\n")
        f.write("## 1. Confiabilidad del Instrumento Psicométrico TAM\n\n")
        f.write(f"- **Alfa de Cronbach Pretest (8 ítems):** $\\alpha = {alfa_pre:.4f}$\n")
        f.write(f"- **Alfa de Cronbach Postest (8 ítems):** $\\alpha = {alfa_post:.4f}$\n\n")
        f.write("### Tabla de Discriminación Ítem-Total (Postest):\n\n")
        f.write(df_a_markdown(discrim_post))
        f.write("\n\n## 2. Pruebas de Normalidad de Shapiro-Wilk (Diferencias Pareadas):\n\n")
        df_sh = pd.DataFrame(shapiro_resultados)
        f.write(df_a_markdown(df_sh))
        f.write("\n\n## 3. Contrastes Inferenciales de Hipótesis (Prueba de Wilcoxon):\n\n")
        df_wx = pd.DataFrame(wilcoxon_resultados)
        f.write(df_a_markdown(df_wx))
        f.write("\n\n## 4. Contrastes Paramétricos de Verificación (Prueba t de Student):\n\n")
        df_tt = pd.DataFrame(ttest_resultados)
        f.write(df_a_markdown(df_tt))
        f.write("\n")

    print("[*] Proceso culminado exitosamente.")
    return True

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    pretest_csv = os.path.join(base_dir, "datos", "raw", "bd_sivac_pretest.csv")
    if not os.path.exists(pretest_csv):
        pretest_csv = os.path.join(base_dir, "datos", "bd_sivac_pretest.csv")
    postest_csv = os.path.join(base_dir, "datos", "raw", "bd_sivac_postest.csv")
    if not os.path.exists(postest_csv):
        postest_csv = os.path.join(base_dir, "datos", "bd_sivac_postest.csv")
    salida_reporte = os.path.join(base_dir, "salidas", "reportes_jurado", "reporte_estadistico_sivac.md")

    seguridad.configurar_utf8()
    ok = generar_reporte_estadistico_completo(pretest_csv, postest_csv, salida_reporte)
    sys.exit(0 if ok else 3)  # 3 = BLOQUEADO (sin manifiesto válido o sin datos)
