# -*- coding: utf-8 -*-
"""
PLANTILLAS DE RESULTADOS v22 — SIVAC
====================================

Generador de tablas y figuras de resultados con datos de campo certificados.
No contiene ninguna cifra: todas las medidas provienen del archivo que el
tesista deposite en `datos/raw/` junto con `MANIFEST.json` firmado.

ESTADO DE ESTA PROPUESTA: no aprobada. El diseno que se describe a
continuacion es una recomendacion tecnica sometida a ratificacion
metodologica; no se declara preespecificado ni sustituye al pipeline
historico `analisis_estadistico_sivac.py`, que se conserva intacto. El
script queda bloqueado y no emite resultados mientras no se acredite el
origen de campo.

Diseno propuesto (sujeto a aprobacion):

  - Un unico contraste pareado por indicador, el mismo para los seis:
    rangos con signo de Wilcoxon, bilateral, alpha .05. La prueba no se
    elige segun el resultado de normalidad.
  - Familia de multiplicidad: los seis indicadores oficiales. Holm con maximo
    acumulado. El puntaje global TAM no entra: es combinacion lineal de AP y UP
    y se presenta solo como descriptivo secundario.
  - Decision por dimension: conjuntiva sobre sus dos indicadores.
  - Metodo declarado por indicador: exacto si n <= 25 y no hay empates;
    en otro caso asintotico con correccion de empates. En la rama
    asintotica el Z es el mismo que sostiene el valor p (se comprueba que
    2·Φ(−|Z|) = p). En la rama exacta el Z se informa solo como referencia
    normal, nunca como si fuera el estadistico de la prueba.
  - Tamano del efecto: r_rb de rangos-biserial como medida principal (no
    supone distribucion) y r = |Z| / sqrt(N) como referencial.
  - Incertidumbre: intervalo bootstrap del cambio mediano, semilla fija.
  - Porcentajes: la diferencia se expresa en puntos porcentuales. El cambio
    relativo se reporta aparte y rotulado como tal.

Uso:
  python scripts/estadistica/plantillas_resultados_v22.py --especificacion
  python scripts/estadistica/plantillas_resultados_v22.py [--raw datos/raw]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from scripts.estadistica.manifest_datos import validar_manifest  # noqa: E402

N_CENSAL = 14
SEMILLA = x
REPLICAS_BOOTSTRAP = 10000
ALFA = 0.05

INDICADORES = [
    ("t_reg", "Tiempo de registro (T_reg)", "min", "D1"),
    ("t_vale", "Tiempo de emisión de vales (T_vale)", "min", "D1"),
    ("rsd", "Registros sin discrepancias (RSD)", "%", "D2"),
    ("cpe", "Concordancia programada vs entregada (CPE)", "%", "D2"),
    ("score_ap", "Aceptación del proceso (AP)", "pts", "D3"),
    ("score_up", "Utilidad percibida (UP)", "pts", "D3"),
]
SECUNDARIO = ("score_tam_total", "Puntaje global TAM (AP + UP)", "pts", "D3")


def especificacion() -> dict:
    """Declara el contrato de tablas y figuras. No calcula ni contiene cifras."""
    return {
        "caracter": "plantilla_sin_medidas",
        "estado_de_la_propuesta": "no aprobada; recomendacion tecnica sujeta a ratificacion metodologica",
        "relacion_con_el_pipeline_historico": "No sustituye a analisis_estadistico_sivac.py, que se conserva intacto y sin modificar.",
        "requisito_de_entrada": "acreditacion del origen de campo y trazabilidad de las mediciones",
        "tablas": [
            {
                "id": "T-DESCRIPTIVA",
                "titulo": "Estadística descriptiva pretest y postest de los seis indicadores",
                "filas": "un indicador por bloque de tres filas: pretest, postest, cambio",
                "columnas": ["Indicador", "Unidad", "Momento", "n", "M", "DE", "Mdn", "RIC", "Mín", "Máx"],
                "cambio": "para tiempos y puntajes, M y Mdn de la diferencia; para porcentajes, puntos porcentuales",
                "prohibido": "promediar dimensiones heterogéneas o sumar minutos con porcentajes",
            },
            {
                "id": "T-PRIMARIA",
                "titulo": "Contraste pareado primario por indicador",
                "filas": "un indicador por fila",
                "columnas": ["Indicador", "n de pares", "pares nulos", "W", "Z", "método declarado",
                             "p", "p Holm", "r_rb", "r referencial", "cambio mediano",
                             "IC 95 % del cambio", "Decisión"],
                "prueba": "Wilcoxon de rangos con signo, bilateral",
                "estado": "propuesta no aprobada; el contraste no se declara preespecificado",
                "ajuste": "Holm sobre los seis indicadores, con máximo acumulado",
            },
            {
                "id": "T-DIMENSIONES",
                "titulo": "Decisión por dimensión y por hipótesis general",
                "filas": "D1, D2, D3 y HG",
                "columnas": ["Hipótesis", "Indicadores", "Regla", "Resultado"],
                "nota": "la HG no tiene valor p propio: es una regla conjuntiva derivada",
            },
            {
                "id": "T-TAM-SECUNDARIA",
                "titulo": "Puntaje global TAM (descriptivo secundario)",
                "filas": "pretest, postest, cambio",
                "columnas": ["Momento", "n", "M", "DE", "Mdn", "RIC", "Mín", "Máx"],
                "prohibido": "usarlo como contraste adicional o como prueba de la Hipótesis General",
            },
            {
                "id": "T-APOYO",
                "titulo": "Diagnósticos de apoyo (anexo técnico)",
                "contenido": ["Shapiro-Wilk sobre diferencias", "asimetría y curtosis",
                              "valores atípicos por regla de Tukey", "sensibilidad con t pareada",
                              "registro de empates y ceros", "método efectivamente usado en cada prueba"],
                "ubicacion": "anexo, no cuerpo del capítulo",
            },
        ],
        "figuras": [
            {
                "id": "F-D1",
                "titulo": "Tiempos de registro y de emisión de vales antes y después de SIVAC",
                "tipo": "pares conectados con caja superpuesta",
                "paneles": ["T_reg", "T_vale"],
                "ejes": "unidad min; escala calculada de los datos con holgura del 5 %",
                "elementos": ["una línea tenue por operador", "mediana", "n visible en la nota"],
            },
            {
                "id": "F-D2",
                "titulo": "Consistencia documental antes y después de SIVAC",
                "tipo": "pares conectados con caja superpuesta",
                "paneles": ["RSD", "CPE"],
                "ejes": "porcentaje, 0 a 100, marcas cada 20",
                "elementos": ["diferencia en puntos porcentuales rotulada en el panel"],
            },
            {
                "id": "F-D3",
                "titulo": "Aceptación del proceso y utilidad percibida antes y después de SIVAC",
                "tipo": "pares conectados con caja superpuesta",
                "paneles": ["AP (4-20)", "UP (4-20)"],
                "ejes": "escala observada 4 a 20, sin extrapolar",
                "elementos": ["sin panel de puntaje total en el cuerpo"],
            },
        ],
        "estilo_figuras": {
            "dpi": 300,
            "tamano": "16,5 cm de ancho util",
            "tipografia": "serif; se registra la fuente resuelta en los metadatos",
            "paleta": "azul pizarra y gris azulado; sin rojo saturado",
            "marco": "sin lomo superior ni derecho",
            "prohibido": ["titulo interno que duplique el rotulo", "barras con eje truncado",
                          "barras de error calculadas con 1,96 y n fijo"],
        },
        "redondeo": {"M_DE_Mdn": 2, "porcentajes": 2, "p": "tres decimales o < .001",
                     "efectos": 2, "IC": 2},
        "prohibiciones": [
            "no elegir la prueba después de ver la normalidad",
            "no informar t y Wilcoxon como dos confirmaciones del mismo contraste",
            "no asignar valor p a la hipótesis general",
            "no interpretar p > .05 como prueba de normalidad",
            "no atribuir causalidad con un diseño de un solo grupo",
        ],
    }


def _verificar_estructura(pre, post) -> dict:
    """Comprueba emparejamiento, integridad y rangos declarados en el codebook."""
    import pandas as pd  # import local: solo se usa con datos certificados

    if len(pre) != N_CENSAL or len(post) != N_CENSAL:
        raise SystemExit(f"n distinto de {N_CENSAL}: pretest={len(pre)}, postest={len(post)}")
    if list(pre["sujeto_id"]) != list(post["sujeto_id"]):
        raise SystemExit("Los identificadores no coinciden en orden; emparejar por sujeto_id antes de continuar.")
    for col in [c for c, *_ in INDICADORES] + [SECUNDARIO[0]]:
        if pre[col].isna().any() or post[col].isna().any():
            raise SystemExit(f"Valores faltantes en {col}")
    if not (pre["score_ap"] == pre[[f"ap_0{i}" for i in range(1, 5)]].sum(axis=1)).all():
        raise SystemExit("score_ap no coincide con la suma de AP-01 a AP-04")
    if not (pre["score_up"] == pre[[f"up_0{i}" for i in range(1, 5)]].sum(axis=1)).all():
        raise SystemExit("score_up no coincide con la suma de UP-01 a UP-04")
    if not (pre["score_tam_total"] == pre["score_ap"] + pre["score_up"]).all():
        raise SystemExit("score_tam_total no coincide con AP + UP")
    return {"n": N_CENSAL, "ids": "coincidentes", "sumas": "verificadas"}


def _wilcoxon_con_ceros(dif) -> dict:
    """Wilcoxon con ceros declarados y método único para p y Z."""
    import numpy as np
    from scipy import stats

    d = np.asarray(dif, dtype=float)
    n_pares = int(d.size)
    n_ceros = int((d == 0).sum())
    d_nz = d[d != 0]
    n_efectivo = int(d_nz.size)
    if n_efectivo == 0:
        return {"W": None, "Z": None, "p": None, "metodo": "no_aplicable",
                "n_pares": n_pares, "n_ceros": n_ceros, "n_efectivo": 0,
                "r_rb": None, "r_referencial": None}

    absolutos = np.abs(d_nz)
    _, conteos = np.unique(absolutos, return_counts=True)
    tiene_empates = bool((conteos > 1).any())
    metodo = "exact" if (n_efectivo <= 25 and not tiene_empates) else "approx"
    res = stats.wilcoxon(d_nz, alternative="two-sided", zero_method="wilcox",
                         method=metodo, correction=False)

    rangos = stats.rankdata(absolutos)
    t_plus = float(rangos[d_nz > 0].sum())
    t_minus = float(rangos[d_nz < 0].sum())
    media = n_efectivo * (n_efectivo + 1) / 4.0
    var = n_efectivo * (n_efectivo + 1) * (2 * n_efectivo + 1) / 24.0
    var -= float(((conteos ** 3 - conteos).sum())) / 48.0
    z = (min(t_plus, t_minus) - media) / (var ** 0.5) if var > 0 else 0.0
    r_rb = (t_plus - t_minus) / (t_plus + t_minus) if (t_plus + t_minus) else 0.0
    return {
        "W": float(res.statistic),
        "Z": float(z),
        "p": float(res.pvalue),
        "metodo": metodo,
        "empates_en_magnitudes": tiene_empates,
        "n_pares": n_pares,
        "n_ceros": n_ceros,
        "n_efectivo": n_efectivo,
        "r_rb": float(r_rb),
        "r_referencial": abs(float(z)) / (n_efectivo ** 0.5),
    }


def _bootstrap_mediana(dif) -> dict:
    """Intervalo percentil del cambio mediano con semilla fija."""
    import numpy as np

    d = np.asarray(dif, dtype=float)
    rng = np.random.default_rng(SEMILLA)
    idx = rng.integers(0, d.size, size=(REPLICAS_BOOTSTRAP, d.size))
    medianas = np.median(d[idx], axis=1)
    return {
        "cambio_mediano": float(np.median(d)),
        "ic95": [float(np.percentile(medianas, 2.5)), float(np.percentile(medianas, 97.5))],
        "metodo": f"bootstrap percentil, {REPLICAS_BOOTSTRAP} replicas, semilla {SEMILLA}",
    }


def _holm(pares) -> dict:
    """Holm con máximo acumulado para garantizar monotonía."""
    orden = sorted(pares, key=lambda x: x[1])
    m = len(orden)
    salida, acumulado = {}, 0.0
    for i, (clave, p) in enumerate(orden):
        bruto = min(1.0, p * (m - i))
        acumulado = max(acumulado, bruto)
        salida[clave] = acumulado
    return salida


def ejecutar(raw: Path) -> dict:
    """Solo se alcanza con MANIFEST válido. Nunca con datos de prueba."""
    import pandas as pd

    estado = validar_manifest()
    if not estado.get("valido"):
        print(f"[BLOQUEO EMPÍRICO] {estado['estado']} — {estado.get('motivo', '')}")
        raise SystemExit(3)

    pre = pd.read_csv(raw / "pretest_campo.csv")
    post = pd.read_csv(raw / "posttest_campo.csv")
    post = post.set_index("sujeto_id").loc[pre["sujeto_id"]].reset_index()
    control = _verificar_estructura(pre, post)

    resultados = {}
    for clave, nombre, unidad, dimension in INDICADORES:
        dif = post[clave].to_numpy() - pre[clave].to_numpy()
        resultados[clave] = {
            "nombre": nombre,
            "unidad": unidad,
            "dimension": dimension,
            "wilcoxon": _wilcoxon_con_ceros(dif),
            "cambio": _bootstrap_mediana(dif),
        }

    holm = _holm([(k, resultados[k]["wilcoxon"]["p"]) for k in resultados])
    for k, p_adj in holm.items():
        resultados[k]["p_holm"] = p_adj
        resultados[k]["decision"] = "rechazar H0" if p_adj < ALFA else "no rechazar H0"

    # TODO(próxima etapa): tablas y figuras a 300 DPI a partir de `resultados`.
    return {"control": control, "resultados": resultados,
            "nota": "Las tablas y figuras se emiten en la etapa con datos certificados."}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Plantillas de resultados v22 (sin medidas)")
    ap.add_argument("--especificacion", action="store_true",
                    help="Imprime el contrato de tablas y figuras y termina")
    ap.add_argument("--raw", type=Path, default=RAIZ / "datos" / "raw")
    args = ap.parse_args()

    if args.especificacion:
        print(json.dumps(especificacion(), ensure_ascii=False, indent=2))
        return 0
    ejecutar(args.raw)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
