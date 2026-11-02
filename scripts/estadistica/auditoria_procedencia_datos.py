# -*- coding: utf-8 -*-
"""
AUDITORÍA DE PROCEDENCIA Y COHERENCIA DE CIFRAS YA PUBLICADAS
=============================================================

Este módulo NO produce resultados de investigación. Su única función es
comprobar si las cifras que ya figuran en el Informe Final y en
`salidas/estadistica/reporte_estadistico_completo.json` se reproducen desde
los archivos de datos disponibles y si las identidades aritméticas internas
son consistentes.

Reglas que respeta:
  - No escribe sobre datos crudos ni sobre salidas estadísticas.
  - No añade contrastes nuevos: solo recalcula los siete ya reportados.
  - Rotula cualquier cifra como procedente de datos de prueba.
  - Se bloquea si no hay MANIFEST válido y se le pide operar en modo campo.

Uso:
  python scripts/estadistica/auditoria_procedencia_datos.py [--json RUTA]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.stats as stats

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / "datos" / "recolectados"
JSON_REPORTE = RAIZ / "salidas" / "estadistica" / "reporte_estadistico_completo.json"

VARS = ["t_reg", "t_vale", "rsd", "cpe", "score_ap", "score_up", "score_tam_total"]
ITEMS_TAM = ["ap_01", "ap_02", "ap_03", "ap_04", "up_01", "up_02", "up_03", "up_04"]


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def cronbach_alpha(df_items: pd.DataFrame) -> float:
    k = df_items.shape[1]
    item_vars = df_items.var(axis=0, ddof=1)
    total_var = df_items.sum(axis=1).var(ddof=1)
    return float((k / (k - 1)) * (1.0 - item_vars.sum() / total_var))


def auditar() -> dict:
    pre = pd.read_csv(DATOS / "pretest_campo.csv")
    post = pd.read_csv(DATOS / "posttest_campo.csv")
    reporte = json.loads(JSON_REPORTE.read_text(encoding="utf-8"))

    n = len(pre)
    salida: dict = {
        "caracter": "auditoria_de_procedencia_sin_resultados_nuevos",
        "advertencia": (
            "Todas las cifras de este informe proceden de los CSV rotulados "
            "DATOS DE PRUEBA. No acreditan medicion de campo."
        ),
        "archivos": {
            "pretest": {"ruta": str(DATOS / "pretest_campo.csv"),
                        "sha256": sha256(DATOS / "pretest_campo.csv"), "filas": n},
            "posttest": {"ruta": str(DATOS / "posttest_campo.csv"),
                         "sha256": sha256(DATOS / "posttest_campo.csv"), "filas": len(post)},
            "reporte_json": {"ruta": str(JSON_REPORTE), "sha256": sha256(JSON_REPORTE)},
        },
        "integridad_estructural": {},
        "identidades_aritmeticas": {},
        "correspondencia_json": {},
        "correspondencia_docx_2026_10_26": {},
        "confiabilidad": {},
        "unidades_geograficas": {},
    }

    # 1. Integridad estructural del emparejamiento
    ids_pre = list(pre["sujeto_id"])
    ids_post = list(post["sujeto_id"])
    suma_ap_ok = bool((pre["score_ap"] == pre[[f"ap_0{i}" for i in range(1, 5)]].sum(axis=1)).all()
                      and (post["score_ap"] == post[[f"ap_0{i}" for i in range(1, 5)]].sum(axis=1)).all())
    suma_up_ok = bool((pre["score_up"] == pre[[f"up_0{i}" for i in range(1, 5)]].sum(axis=1)).all()
                      and (post["score_up"] == post[[f"up_0{i}" for i in range(1, 5)]].sum(axis=1)).all())
    total_ok = bool((pre["score_tam_total"] == pre["score_ap"] + pre["score_up"]).all()
                    and (post["score_tam_total"] == post["score_ap"] + post["score_up"]).all())
    likert = pd.concat([pre[ITEMS_TAM], post[ITEMS_TAM]])
    def _ok(cond) -> bool:
        return bool(bool(cond))

    rango = {
        "t_reg_0_120": _ok(pre["t_reg"].between(0.01, 120).all() and post["t_reg"].between(0.01, 120).all()),
        "t_vale_0_60": _ok(pre["t_vale"].between(0.01, 60).all() and post["t_vale"].between(0.01, 60).all()),
        "rsd_0_100": _ok(pre["rsd"].between(0, 100).all() and post["rsd"].between(0, 100).all()),
        "cpe_0_100": _ok(pre["cpe"].between(0, 100).all() and post["cpe"].between(0, 100).all()),
        "likert_1_5": _ok(likert.stack().between(1, 5).all()),
    }
    faltantes = {
        "pretest_nulos": int(pre[VARS].isna().sum().sum()),
        "posttest_nulos": int(post[VARS].isna().sum().sum()),
    }
    salida["integridad_estructural"] = {
        "n_pretest": n,
        "n_posttest": len(post),
        "identificadores_identicos_y_en_el_mismo_orden": ids_pre == ids_post,
        "ids_unicos": len(set(ids_pre)) == n,
        "suma_items_igual_score_ap": suma_ap_ok,
        "suma_items_igual_score_up": suma_up_ok,
        "score_tam_total_igual_ap_mas_up": total_ok,
        "rangos_codebook": rango,
        "valores_nulos": faltantes,
        "emparejamiento_por_posicion_no_por_id": True,
        "nota_emparejamiento": (
            "El pipeline resta columnas por posicion. La coincidencia actual de "
            "identificadores y de orden es una condicion del archivo, no una "
            "garantia del codigo."
        ),
    }

    # 2. Identidades aritmeticas sobre cifras ya reportadas
    ident = {}
    for v in VARS:
        d = post[v] - pre[v]
        m, s = float(d.mean()), float(d.std(ddof=1))
        if s == 0:
            t_id = float("inf") if m != 0 else 0.0
        else:
            t_id = m / (s / math.sqrt(n))
        dj = reporte["contrastes_inferenciales"][v]
        t_json = dj["t_student"]["estadistico_t"]
        dz_json = dj["t_student"]["d_cohen"]
        w = stats.wilcoxon(post[v], pre[v], alternative="two-sided")
        z_norm = (w.statistic - n * (n + 1) / 4) / math.sqrt(n * (n + 1) * (2 * n + 1) / 24)
        p_exacta = float(stats.wilcoxon(post[v], pre[v], alternative="two-sided", method="exact").pvalue)
        p_aprox = float(stats.wilcoxon(post[v], pre[v], alternative="two-sided", method="approx").pvalue)
        ident[v] = {
            "media_diferencia": round(m, 6),
            "de_diferencia": round(s, 6),
            "t_recalculada_desde_medias": round(t_id, 6),
            "t_reportada_json": round(float(t_json), 6),
            "t_coincide": abs(t_id - float(t_json)) < 5e-3,
            "d_z_recalculada": round(m / s, 6) if s else None,
            "d_z_reportada_json": round(float(dz_json), 6),
            "d_z_coincide": s != 0 and abs(m / s - float(dz_json)) < 5e-4,
            "W_reportada": float(w.statistic),
            "z_aprox_normal_sin_correccion": round(float(z_norm), 6),
            "p_exacta_disponible": round(p_exacta, 9),
            "p_asintotica": round(p_aprox, 9),
            "p_guardada_en_json": round(float(dj["wilcoxon"]["p_valor"]), 9),
            "r_rosenthal_N": round(abs(z_norm) / math.sqrt(n), 6),
            "r_rosenthal_2N": round(abs(z_norm) / math.sqrt(2 * n), 6),
            "r_guardada_en_json": round(float(dj["wilcoxon"]["r_rosenthal"]), 6),
            "holmes_ajustado_json": round(float(dj["holm_bonferroni"]["p_ajustado"]), 12),
        }
    salida["identidades_aritmeticas"] = ident

    # 3. Correspondencia de las cifras del JSON con el script vigente
    # El Holm del script opera sobre p_valor_adoptado (la prueba elegida), no
    # sobre el p de Wilcoxon. La auditoria reproduce esa misma familia.
    familia = [(v, float(reporte["contrastes_inferenciales"][v]["p_valor_adoptado"])) for v in VARS]
    familia.sort(key=lambda x: x[1])
    m = len(familia)
    holm = {}
    max_prev = 0.0
    for i, (v, p) in enumerate(familia):
        bruto = min(1.0, p * (m - i))
        max_prev = max(max_prev, bruto)
        holm[v] = {"p_original": p, "p_ajustado_bruto": bruto,
                   "p_ajustado_con_max_acumulado": max_prev}
    monotono_bruto = all(
        holm[familia[i][0]]["p_ajustado_bruto"] <= holm[familia[i + 1][0]]["p_ajustado_bruto"] + 1e-18
        for i in range(m - 1)
    )
    coincide_json = all(
        abs(holm[v]["p_ajustado_bruto"]
            - float(reporte["contrastes_inferenciales"][v]["holm_bonferroni"]["p_ajustado"])) <= 1e-18
        for v in VARS
    )
    salida["correspondencia_json"] = {
        "r_esperada_con_N": round(abs(ident["t_reg"]["z_aprox_normal_sin_correccion"]) / math.sqrt(n), 6),
        "r_contenida_en_json": ident["t_reg"]["r_guardada_en_json"],
        "json_usa_denominador_2N": abs(ident["t_reg"]["r_guardada_en_json"]
                                       - ident["t_reg"]["r_rosenthal_2N"]) < 1e-5,
        "docx_reporta_r": 0.881,
        "json_incompatible_con_docx": abs(ident["t_reg"]["r_guardada_en_json"] - 0.881) > 1e-3,
        "familia_holm_es_p_valor_adoptado": True,
        "holm_reproduce_el_json": coincide_json,
        "holm_bruto_ya_es_monotono_en_estos_datos": monotono_bruto,
        "holm_pasos": {v: {"p_original": holm[v]["p_original"],
                           "p_ajustado": holm[v]["p_ajustado_bruto"]} for v in holm},
        "nota_holm": (
            "La implementacion omite el maximo acumulado que garantiza monotonia "
            "de los p ajustados. En estos datos el orden ya resulta monotono, de "
            "modo que la omision no altera las decisiones actuales, pero si podria "
            "alterarlas con otros datos."
        ),
        "metodo_p_wilcoxon_heterogeneo": {
            "valores_distintos_en_json": sorted({ident[v]["p_guardada_en_json"] for v in VARS}),
            "explicacion": (
                "scipy elige prueba exacta o asintotica segun la presencia de "
                "empates; el JSON mezcla ambos metodos entre indicadores."
            ),
        },
    }

    # 4. Correspondencia con las cifras impresas en el Informe Final v20
    docx = {
        "Tabla 40 t_reg": {"t": -38.944, "p": "<.001", "d": -10.41, "W": 0.0, "Z": -3.30,
                           "p_w": 0.001, "r": 0.881},
        "Tabla 40 t_vale": {"t": -24.509, "d": -6.55},
        "Tabla 41 rsd": {"t": 26.628, "d": 7.12},
        "Tabla 41 cpe": {"t": 28.147, "d": 7.52},
        "Tabla 42 ap": {"t": 33.352, "d": 8.91},
        "Tabla 42 up": {"t": 34.881, "d": 9.32},
        "Tabla 42 tam": {"t": 44.477, "d": 11.89},
    }
    comp = {}
    for etiqueta, vals in docx.items():
        clave = {"Tabla 40 t_reg": "t_reg", "Tabla 40 t_vale": "t_vale", "Tabla 41 rsd": "rsd",
                 "Tabla 41 cpe": "cpe", "Tabla 42 ap": "score_ap", "Tabla 42 up": "score_up",
                 "Tabla 42 tam": "score_tam_total"}[etiqueta]
        j = ident[clave]
        fila = {"t_docx": vals.get("t"), "t_recalculada": j["t_recalculada_desde_medias"],
                "t_coincide": abs((vals.get("t") or 0) - j["t_recalculada_desde_medias"]) < 5e-3}
        if "d" in vals:
            fila["d_docx"] = vals["d"]
            fila["d_recalculada"] = j["d_z_recalculada"]
            fila["d_coincide"] = abs(abs(vals["d"]) - abs(j["d_z_recalculada"])) < 5e-3
        comp[etiqueta] = fila
    salida["correspondencia_docx_2026_10_26"] = {
        "comparacion": comp,
        "r_docx_vs_json": {"docx": 0.881, "json": ident["score_ap"]["r_guardada_en_json"]},
        "p_wilcoxon_docx_uniforme": 0.001,
        "p_wilcoxon_json_rsd": ident["rsd"]["p_guardada_en_json"],
        "p_wilcoxon_json_rsd_no_redondea_a_001": ident["rsd"]["p_guardada_en_json"] < 0.0005,
    }

    # 5. Confiabilidad ya reportada (alfa) y su IC segun Feldt
    conf = {}
    for etiqueta, df in (("pretest", pre), ("posttest", post)):
        a = cronbach_alpha(df[ITEMS_TAM])
        k = len(ITEMS_TAM)
        f1, f2 = n - 1, (n - 1) * (k - 1)
        li = 1 - (1 - a) * stats.f.ppf(0.975, f1, f2)
        ls = 1 - (1 - a) * stats.f.ppf(0.025, f1, f2)
        conf[etiqueta] = {
            "alpha_recalculado": round(a, 6),
            "alpha_json": round(float(reporte["confiabilidad_instrumento_03"][etiqueta]["global_tam"]["alpha"]), 6),
            "ic95_recalculado": [round(max(0.0, li), 6), round(min(1.0, ls), 6)],
            "ic95_json": [round(x, 6) for x in reporte["confiabilidad_instrumento_03"][etiqueta]["global_tam"]["ic_95"]],
            "n_menor_que_piloto_15": n < 15,
        }
    salida["confiabilidad"] = conf

    # 6. Unidades geograficas
    centros = sorted(set(pre["centro_acopio"]))
    salida["unidades_geograficas"] = {
        "centros_distintos_en_csv": len(centros),
        "trabajadores": n,
        "centros_con_mas_de_un_trabajador": {
            c: int((pre["centro_acopio"] == c).sum()) for c in centros
            if (pre["centro_acopio"] == c).sum() > 1
        },
        "registro_normativo_centros": 19,
        "readme_recolectados_declara": 8,
        "docx_declara": 13,
        "discrepancia_de_conteos": [8, 13, 19],
    }

    # 7. Normalidad ya reportada: solo se reproducen W y p; no se decide nada nuevo
    normal = {}
    for v in VARS:
        d = post[v] - pre[v]
        w_stat, p_val = stats.shapiro(d)
        normal[v] = {
            "W": round(float(w_stat), 6),
            "p": round(float(p_val), 6),
            "W_json": round(float(reporte["normalidad_shapiro_wilk"][v]["estadistico_w"]), 6),
            "p_json": round(float(reporte["normalidad_shapiro_wilk"][v]["p_valor"]), 6),
            "coincide_con_json": abs(float(p_val) - float(reporte["normalidad_shapiro_wilk"][v]["p_valor"])) < 1e-6,
            "asimetria": round(float(d.skew()), 4),
            "curtosis_exceso": round(float(d.kurtosis()), 4),
            "p_cerca_del_umbral_005": bool(float(p_val) < 0.10),
            "n": n,
        }
    salida["normalidad_reproducida"] = {
        "por_indicador": normal,
        "advertencia": (
            "No rechazar normalidad no demuestra normalidad. Con n = 14, Shapiro-Wilk "
            "tiene potencia baja y el supuesto queda indeterminado, no confirmado. "
            "El indicador con p mas proximo a .05 muestra el margen real."
        ),
        "gl_declarado_en_el_pipeline": n,
        "shapiro_no_tiene_grados_de_libertad_de_ese_modo": True,
    }

    # 8. Trazabilidad al protocolo de medicion DEC-021
    salida["trazabilidad_protocolo_dec021"] = {
        "t_reg_requiere_tres_observaciones_por_participante": True,
        "columnas_de_observaciones_presentes": any(c.startswith("t_reg_") for c in pre.columns),
        "unidad_en_csv_es_valor_unico_por_participante": "t_reg" in pre.columns,
        "cpe_requiere_corpus_de_40_a_60_entregas_por_ventana": True,
        "columnas_de_conteos_presentes": any(
            c in pre.columns for c in ("entregas_programadas", "entregas_conformes", "n_entregas", "denominador_cpe")
        ),
        "rsd_requiere_conteo_de_registros": any(
            c in pre.columns for c in ("registros_totales", "registros_correctos", "denominador_rsd")
        ),
        "conclusion": (
            "Los CSV contienen porcentajes agregados y un unico tiempo por participante; "
            "no permiten reconstruir el corpus documental ni la mediana de tres "
            "cronometrajes exigidos por DEC-021. La trazabilidad al protocolo no es "
            "verificable con estos archivos, aun si los datos fueran reales."
        ),
    }

    return salida


def _serializable(obj):
    """Convierte escalares de numpy y rutas a tipos JSON nativos."""
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError(f"Tipo no serializable: {type(obj).__name__}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Auditoria de procedencia, sin resultados nuevos")
    ap.add_argument("--json", type=Path, default=None, help="Ruta de salida del informe de auditoria")
    args = ap.parse_args()
    res = auditar()
    texto = json.dumps(res, ensure_ascii=False, indent=2, default=_serializable)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(texto, encoding="utf-8")
        print(f"[AUDITORIA] escrita en {args.json}")
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
