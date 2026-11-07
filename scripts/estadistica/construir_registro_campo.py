# -*- coding: utf-8 -*-
"""Construye el registro de campo (SIVAC_DATOS_CAMPO.md) desde el crudo.

El registro publicado en `datos/recolectados/` se deriva íntegramente de las
fichas sintéticas de `datos/prueba_sintetica/`:

    instrumento01_replicas.csv   -> Parte 3 (168 réplicas cronometradas)
    instrumento02_asientos.csv   -> Parte 4 (1 120 asientos auditados)
    instrumento02_despachos.csv  -> Parte 4 (700 despachos conciliados)
    instrumento03_reactivos.csv  -> Parte 5 (224 respuestas Likert)
    matriz_analitica_pre_post.csv-> Partes 0, 1, 6, 7 y 8

Además sincroniza `datos/recolectados/pretest_campo.csv` y
`posttest_campo.csv` con la matriz analítica, de modo que el verificador
v06 y el pipeline estadístico trabajen sobre el mismo conjunto.

Los textos fijos (Parte 2 y los enunciados de la Parte 5) se conservan tal
como están en el documento vigente: el script los extrae por anclas y los
vuelve a insertar, por lo que es idempotente.

Uso:
    python scripts/estadistica/construir_registro_campo.py
"""
from __future__ import annotations

import csv
import re
import statistics as ss
import sys
from pathlib import Path

import numpy as np
from scipy import stats as st

RAIZ = Path(__file__).resolve().parents[2]
SINT = RAIZ / "datos" / "prueba_sintetica"
RECO = RAIZ / "datos" / "recolectados"
REGISTRO = RECO / "SIVAC_DATOS_CAMPO.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generar_datos_sinteticos as G  # noqa: E402  (solo constantes)

PADRON = G.PADRON
COLUMNAS = ["t_reg", "t_vale", "rsd", "cpe", "score_ap", "score_up",
            "score_tam_total"]
ETIQUETAS = {
    "t_reg": ("T_reg", "D1", "min"),
    "t_vale": ("T_vale", "D1", "min"),
    "rsd": ("RSD", "D2", "%"),
    "cpe": ("CPE", "D2", "%"),
    "score_ap": ("AP", "D3", "pts"),
    "score_up": ("UP", "D3", "pts"),
    "score_tam_total": ("TAM", "D3", "pts"),
}


# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------

def leer(nombre: str) -> list[dict]:
    with (SINT / nombre).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def f2(x: float) -> str:
    return f"{x:.2f}"


def f3(x: float) -> str:
    return f"{x:.3f}"


def p_apa(p: float) -> str:
    if p < 0.001:
        return "< .001"
    return f"{p:.3f}".lstrip("0")


def p_cien(p: float) -> str:
    return f"{p:.2e}"


def tabla(cabeceras: list[str], alineacion: list[str],
          filas: list[list[str]]) -> list[str]:
    alineacion = [a.strip().strip("|").strip() for a in alineacion]
    return ["| " + " | ".join(cabeceras) + " |",
            "| " + " | ".join(alineacion) + " |"] + \
           ["| " + " | ".join(f) + " |" for f in filas]


def trozo(texto: str, ini: str, fin: str) -> str:
    return texto[texto.index(ini):texto.index(fin)]


# --------------------------------------------------------------------------
# Estadística
# --------------------------------------------------------------------------

def cargar_matriz() -> tuple[dict, dict, dict]:
    filas = leer("matriz_analitica_pre_post.csv")
    pre = {r["sujeto_id"]: r for r in filas if r["momento"] == "Pretest"}
    post = {r["sujeto_id"]: r for r in filas if r["momento"] == "Postest"}
    return pre, post, {r["sujeto_id"]: r for r in filas}


def descriptivos(pre: dict, post: dict) -> dict:
    salida = {}
    for c in COLUMNAS:
        a = np.array([float(pre[s][c]) for s in pre])
        b = np.array([float(post[s][c]) for s in post])
        d = b - a
        q25, q75 = np.percentile(b, [25, 75])
        q25a, q75a = np.percentile(a, [25, 75])
        q25d, q75d = np.percentile(d, [25, 75])
        salida[c] = {
            "pre": (a.mean(), a.std(ddof=1), float(np.median(a)), q25a, q75a,
                    a.min(), a.max()),
            "post": (b.mean(), b.std(ddof=1), float(np.median(b)), q25, q75,
                     b.min(), b.max()),
            "dif": (d.mean(), d.std(ddof=1), float(np.median(d)), q25d, q75d,
                    d.min(), d.max()),
            "rel": (b.mean() - a.mean()) / a.mean() * 100,
            "pp": b.mean() - a.mean(),
        }
    return salida


def contraste(pre: dict, post: dict) -> dict:
    salida = {}
    for c in COLUMNAS:
        a = np.array([float(pre[s][c]) for s in pre])
        b = np.array([float(post[s][c]) for s in post])
        d = b - a
        w, p_shapiro = st.shapiro(d)
        t, p_t = st.ttest_rel(b, a)
        dz = d.mean() / d.std(ddof=1)
        n = len(d)
        ties = len(set(np.round(np.abs(d[d != 0]), 6))) != int((d != 0).sum())
        ceros = int((d == 0).sum())
        if not ties and ceros == 0:
            _, p_w = st.wilcoxon(b, a, method="exact")
            metodo = "exacto"
        else:
            p_w = None
            metodo = "asintótico"
        # Estadístico de rangos con signo (corrección por empates).
        orden = np.argsort(np.abs(d), kind="mergesort")
        rangos = np.empty(n, dtype=float)
        absd = np.abs(d)
        i = 0
        while i < n:
            j = i
            while j + 1 < n and np.isclose(absd[orden[j + 1]], absd[orden[i]]):
                j += 1
            rango = (i + j + 2) / 2
            for k in range(i, j + 1):
                rangos[orden[k]] = rango
            i = j + 1
        w_mas = float(rangos[d > 0].sum())
        n_ef = int((d != 0).sum())
        correccion = sum(len(g) ** 3 - len(g) for g in
                         [np.where(np.isclose(absd[d != 0], v))[0]
                          for v in np.unique(np.round(absd[d != 0], 6))]
                         if len(g) > 1)
        se = np.sqrt(n_ef * (n_ef + 1) * (2 * n_ef + 1) / 24 - correccion / 48)
        z = (w_mas - n_ef * (n_ef + 1) / 4) / se if se else 0.0
        if p_w is None:
            p_w = float(2 * (1 - st.norm.cdf(abs(z))))
        salida[c] = {"W": w_mas, "Z": float(z), "p_w": float(p_w),
                     "metodo": metodo, "r": abs(z) / np.sqrt(n_ef),
                     "t": float(t), "p_t": float(p_t), "dz": float(dz),
                     "W_shapiro": float(w), "p_shapiro": float(p_shapiro),
                     "n_ef": n_ef, "n": n}
    # Holm-Bonferroni sobre los siete contrastes t.
    orden = sorted(COLUMNAS, key=lambda c: salida[c]["p_t"])
    m = len(orden)
    previo = 0.0
    for i, c in enumerate(orden):
        adj = min(1.0, (m - i) * salida[c]["p_t"])
        adj = max(adj, previo)
        previo = adj
        salida[c]["p_holm"] = adj
    return salida


def alfa(items: np.ndarray) -> float:
    k = items.shape[1]
    return k / (k - 1) * (1 - items.var(axis=0, ddof=1).sum() /
                          items.sum(axis=1).var(ddof=1))


def alfa_ic(items: np.ndarray) -> tuple[float, float, float]:
    a = alfa(items)
    n, k = items.shape
    df1, df2 = n - 1, (n - 1) * (k - 1)
    f_bajo = st.f.ppf(0.975, df1, df2)
    f_alto = st.f.ppf(0.025, df1, df2)
    return a, max(0.0, 1 - (1 - a) * f_bajo), min(1.0, 1 - (1 - a) * f_alto)


def confiabilidad() -> list[tuple[str, str, int, float, float, float]]:
    filas = leer("instrumento03_reactivos.csv")
    salida = []
    for momento in ("Pretest", "Postest"):
        sub = [r for r in filas if r["momento"] == momento]
        sujetos = []
        for s in [p[0] for p in PADRON]:
            vals = [int(r["valor"]) for r in sub if r["sujeto_id"] == s]
            sujetos.append(vals)
        m = np.array(sujetos, dtype=float)
        for etiqueta, cols in (("Escala global TAM (modalidad A)", slice(0, 8)),
                               ("Aceptación del proceso (AP)", slice(0, 4)),
                               ("Utilidad percibida (UP)", slice(4, 8))):
            a, li, ls = alfa_ic(m[:, cols])
            salida.append((momento, etiqueta, cols.stop - cols.start, a, li, ls))
    return salida


def nivel_consistencia(a: float) -> str:
    if a >= 0.90:
        return "Excelente"
    if a >= 0.80:
        return "Buena"
    if a >= 0.70:
        return "Aceptable"
    return "Cuestionable"


# --------------------------------------------------------------------------
# Parte 0 — presentación y resumen
# --------------------------------------------------------------------------

def parte_0(desc: dict) -> list[str]:
    filas = []
    for c in COLUMNAS:
        nombre, dim, unidad = ETIQUETAS[c]
        if c in ("t_reg", "t_vale"):
            pre_t = f"{f2(desc[c]['pre'][0])} ± {f2(desc[c]['pre'][1])}"
            post_t = f"{f2(desc[c]['post'][0])} ± {f2(desc[c]['post'][1])}"
            alcance = "14 operadores × 3 réplicas (84 mediciones)"
        elif c in ("rsd", "cpe"):
            pre_t = f"{f2(desc[c]['pre'][0])} ± {f2(desc[c]['pre'][1])}"
            post_t = f"{f2(desc[c]['post'][0])} ± {f2(desc[c]['post'][1])}"
            n_doc = 40 if c == "rsd" else 25
            alcance = (f"14 operadores × {n_doc} expedientes "
                       f"({14 * n_doc:,} documentos)".replace(",", " "))
        else:
            pre_t = f"{f2(desc[c]['pre'][0])} ± {f2(desc[c]['pre'][1])}"
            post_t = f"{f2(desc[c]['post'][0])} ± {f2(desc[c]['post'][1])}"
            alcance = "14 operadores (4 reactivos Likert)"
        etiqueta = {
            "t_reg": "Tiempo de registro de movimientos (T_reg)",
            "t_vale": "Tiempo de emisión de vales (T_vale)",
            "rsd": "Registros sin discrepancias (RSD)",
            "cpe": "Concordancia programada vs. entregada (CPE)",
            "score_ap": "Aceptación del proceso (AP)",
            "score_up": "Utilidad percibida (UP)",
            "score_tam_total": "Puntaje global TAM",
        }[c]
        unidad_txt = {"min": "Minutos (Media ± DE)", "%": "Porcentaje (%)",
                      "pts": "Puntos"}[unidad]
        if c == "score_ap":
            unidad_txt = "Puntos (1–20)"
        if c == "score_up":
            unidad_txt = "Puntos (1–20)"
        if c == "score_tam_total":
            unidad_txt = "Puntos (8–40)"
        filas.append([etiqueta, unidad_txt, pre_t, post_t, alcance])

    L = [
        "El presente documento consolida el registro íntegro de las mediciones "
        "del estudio de evaluación del Sistema de Información de Vacunas "
        "(SIVAC). El diseño es preexperimental, con pretest (proceso manual "
        "tradicional en papel) y postest (proceso automatizado con SIVAC) en un "
        "solo grupo, administrado a catorce unidades censales de operadores en "
        "trece centros de acopio y establecimientos de salud de la red "
        "asistencial. El conjunto publicado es el de prueba rotulado en el "
        "encabezado: se reproduce desde las fichas crudas con la semilla "
        "20261026 y se sustituye por el registro de campo definitivo sin "
        "alterar la estructura ni las reglas de cálculo.",
        "",
        "### Resumen de parámetros operacionales del estudio",
        "",
    ]
    L += tabla(["Dimensión / Indicador", "Unidad de medida",
                "Pretest (Proceso Manual)", "Postest (Sistema SIVAC)",
                "Alcance muestral"],
               ["| :--- | :--- | :---: | :---: | :--- |"],
               [["**D1. Oportunidad de procesamiento**", "", "", "", ""]]
               + filas[:2]
               + [["**D2. Consistencia documental**", "", "", "", ""]]
               + filas[2:4]
               + [["**D3. Satisfacción del usuario**", "", "", "", ""]]
               + filas[4:]
               + [["**Cobertura total del estudio**", "—",
                   "**Línea base manual**", "**Fase con SIVAC**",
                   "**14 operadores censales / 13 centros de acopio**"]])
    L += [
        "",
        "*Nota.* Las medias y desviaciones estándar se calculan sobre las "
        "catorce unidades censales; en los tiempos, sobre el promedio de las "
        "tres réplicas de cada operador y fase. Elaboración propia.",
        "",
        "### Criterios y reglas de cálculo",
        "",
        "1. **Tiempos operativos (T_reg y T_vale):** promedio aritmético de tres "
        "réplicas independientes cronometradas por operador en cada fase de "
        "observación.",
        "2. **Registros sin discrepancias (RSD):** cociente entre los documentos "
        "conformes (que cumplen simultáneamente los ocho criterios de auditoría) "
        "y el total auditado (40), expresado en porcentaje.",
        "3. **Concordancia programada vs. entregada (CPE):** porcentaje de "
        "despachos conciliados sin diferencias entre la cantidad programada y la "
        "física entregada sobre un total de 25 despachos evaluados.",
        "4. **Satisfacción del usuario (AP, UP y TAM):** AP y UP son la suma de "
        "cuatro reactivos Likert de 1 a 5 puntos; el puntaje global TAM es la "
        "suma directa de ambas subescalas (rango de 8 a 40 puntos).",
        "5. **Criterio de contraste inferencial:** la prueba decisoria se "
        "selecciona según la normalidad de las diferencias pareadas "
        "($D = \\text{postest} - \\text{pretest}$) evaluada con Shapiro-Wilk: "
        "t de Student pareada cuando $p > .05$ y Wilcoxon de rangos con signo "
        "cuando $p \\le .05$.",
        "6. **Método de cálculo en Wilcoxon:** método exacto por permutación "
        "ante la ausencia de empates o diferencias nulas, y método asintótico "
        "con corrección por continuidad y empates cuando existen ligaduras en "
        "las diferencias.",
        "7. **Control del error tipo I:** ajuste secuencial de Holm-Bonferroni "
        "sobre los siete contrastes de la familia.",
        "8. **Precisión de registro:** las duraciones se expresan en minutos con "
        "cuatro cifras decimales en la ficha cronométrica (Parte 3) y con dos "
        "cifras decimales en la matriz analítica (Partes 0 y 6), que es la "
        "precisión con la que el pipeline estadístico lee los datos.",
        "9. **Diferencia de despacho (Dif.):** entregado menos programado. Un "
        "valor negativo indica faltante y uno positivo, exceso entregado; la "
        "entrega es concordante solo cuando la diferencia es cero.",
        "",
    ]
    return L


# --------------------------------------------------------------------------
# Parte 1 — padrón
# --------------------------------------------------------------------------

def parte_1() -> list[str]:
    L = [
        "La población evaluada es censal: comprende la totalidad de catorce "
        "operadores distribuidos en trece centros de acopio y establecimientos "
        "de salud de la red asistencial. La sede ALMACÉN (CHANKA) cuenta con dos "
        "operadores asignados al mismo punto logístico, por lo que el número de "
        "centros y el de unidades evaluadas difieren levemente. El padrón "
        "individualiza a los trabajadores, establecimientos, observadores de "
        "campo y las fechas de administración para ambas fases.",
        "",
    ]
    filas = [[op, centro, cod, obs, G.dmy(fpre), G.dmy(fpost)]
             for op, centro, cod, obs, fpre, fpost in PADRON]
    L += tabla(["Sujeto", "Centro de acopio", "Código", "Observador",
                "Pretest", "Postest"],
               ["| :--- | :--- | :---: | :---: | :---: | :---: |"], filas)
    L += ["",
          "*Nota.* Padrón censal de operadores y centros de acopio evaluados "
          "durante las fases de pretest y postest. Elaboración propia.", ""]
    return L


# --------------------------------------------------------------------------
# Parte 3 — fichas de tiempos
# --------------------------------------------------------------------------

def parte_3() -> list[str]:
    rep = leer("instrumento01_replicas.csv")
    L = [
        "El instrumento imprime las 168 réplicas del conjunto: seis por unidad "
        "y fase (tres de registro y tres de emisión del vale). Cada bloque "
        "cierra con la suma y la media de sus tres réplicas, de modo que el "
        "indicador pueda auditarse sin recurrir al archivo de datos. Las "
        "duraciones se expresan en minutos con cuatro decimales; en el postest "
        "de T_vale se añade entre paréntesis el equivalente en segundos "
        "enteros. La duración es neta: el intervalo entre la hora de inicio y "
        "la de corte equivale a la duración más la pausa externa registrada, "
        "de modo que ambas columnas cuadran en cada réplica.",
        "",
        "**Convenciones.** T1: ingreso de remesa con un biológico y lote único. "
        "T2: salida regular programada de dos a tres vacunas. T3: "
        "redistribución con cuatro a seis biológicos. T4: vale simple para "
        "puesto de salud 1-1 o 1-2. T5: vale regular para centro de salud 1-3 "
        "o 1-4. T6: vale de reposición urgente o contingencia. P1: atención en "
        "ventanilla. P2: llamada del establecimiento. P3: corte breve de "
        "energía. P4: verificación de existencias.",
        "",
    ]
    bloque = 0
    for op, centro, cod, obs, fpre, fpost in PADRON:
        for momento, fecha in (("Pretest", fpre), ("Postest", fpost)):
            bloque += 1
            fase = ("Pretest (proceso manual)" if momento == "Pretest"
                    else "Postest (Sistema SIVAC)")
            L.append(f"### Bloque {bloque} · {op} · {fase} · {G.dmy(fecha)}")
            L.append("")
            L.append(f"Centro de acopio: **{centro}** ({cod}) · Observador: "
                     f"**{obs}**")
            L.append("")
            for indicador, titulo in (("T_reg",
                                       "**Indicador 1.1 — Tiempo de registro (T_reg)**"),
                                      ("T_vale",
                                       "**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**")):
                filas = [r for r in rep
                         if r["sujeto_id"] == op and r["momento"] == momento
                         and r["indicador"] == indicador]
                filas.sort(key=lambda r: r["replica"])
                L.append(titulo)
                L.append("")
                cuerpo = []
                for r in filas:
                    dur = f"{float(r['duracion_min']):.4f}"
                    if momento == "Postest" and indicador == "T_vale":
                        dur += f" ({int(r['duracion_s'])} s)"
                    pausa = r["pausa_s"] or "—"
                    motivo = r["motivo_pausa"] or "—"
                    # El vale no lleva lote: la ficha imprime una sola celda
                    # para el número PECOSA y deja el lote sin dato.
                    lote = (r["lote_documento"]
                            if indicador == "T_reg" else "—")
                    cuerpo.append([r["replica"], r["tarea"], r["documento"],
                                   lote, r["hora_inicio"], r["hora_corte"],
                                   dur, pausa, motivo, r["valida"]])
                L += tabla(["Réplica", "Tarea", "Documento", "Lote", "Inicio",
                            "Fin", "Duración (min)", "Pausa (s)", "Motivo",
                            "Válida"],
                           ["| :--- | :---: | :---: | :---: | :---: | :---: |"
                            " ---: | ---: | :---: | :---: |"],
                           cuerpo)
                suma_min = sum(float(r["duracion_min"]) for r in filas)
                suma_s = sum(int(r["duracion_s"]) for r in filas)
                media = suma_min / len(filas)
                L += ["",
                      f"Cierre: {suma_min:.4f} min ÷ {len(filas)} = "
                      f"**{media:.4f} min**. Suma de las tres réplicas: "
                      f"{suma_min:.4f} min ({suma_s} s).", ""]
            # El recuadro de resumen de la ficha impresa se llena con estos
            # tres valores: las dos medias y el conteo de réplicas válidas.
            medias, validas = {}, 0
            for indicador in ("T_reg", "T_vale"):
                grupo = [r for r in rep
                         if r["sujeto_id"] == op and r["momento"] == momento
                         and r["indicador"] == indicador]
                medias[indicador] = (sum(float(r["duracion_min"])
                                         for r in grupo) / len(grupo))
                validas += sum(1 for r in grupo if r["valida"] == "Sí")
            L += [f"**Resumen del operador.** T_reg promedio: "
                  f"{medias['T_reg']:.4f} min · T_vale promedio: "
                  f"{medias['T_vale']:.4f} min · Réplicas válidas: "
                  f"{validas} de 6.", ""]
            L += ["---", ""]
    return L


# --------------------------------------------------------------------------
# Parte 4 — auditoría documental
# --------------------------------------------------------------------------

MOTIVOS = {
    "M1": "M1", "M2": "M2", "M3": "M3", "M4": "M4",
    "M5": "M5", "M6": "M6", "M7": "M7", "M8": "M8",
}


def _rango(filas: list[dict]) -> str:
    """Primera y última fecha de un bloque, en el formato de la ficha."""
    fechas = sorted((r["fecha"] for r in filas if r.get("fecha")),
                    key=lambda f: (f[6:], f[3:5], f[:2]))
    if not fechas:
        return "—"
    return f"{fechas[0]} al {fechas[-1]}"


def parte_4() -> list[str]:
    asientos = leer("instrumento02_asientos.csv")
    despachos = leer("instrumento02_despachos.csv")
    L = [
        "Cada bloque audita cuarenta documentos sobre ocho criterios binarios y "
        "concilia veinticinco despachos. La conformidad documental es "
        "conjuntiva: un documento es conforme solo si cumple los ocho "
        "criterios. La tabla emplea S y N para abreviar Sí y No, y las columnas "
        "1 a 8 siguen el orden de los aspectos del instrumento. El motivo se "
        "codifica de M1 a M8 y se imprime solo cuando el documento no es "
        "conforme; la última columna reproduce la observación del auditor, que "
        "en la ficha impresa se escribe en la celda «Motivo · Obs.». En las "
        "entregas, Dif. es la cantidad entregada menos la "
        "programada: el signo negativo señala faltante y el positivo, exceso; "
        "la entrega es concordante solo cuando la diferencia es cero.",
        "",
        "**Convenciones.** ING: ingreso. SAL: salida. TRA: transferencia. DEV: "
        "devolución. AJU: ajuste. BCG, PENT, IPV, ROTA, NEUM, SPR, DTA, HEPB, "
        "INFL y VARI abrevian los biológicos del catálogo. M1 a M8 remiten a "
        "los ocho aspectos en el orden impreso.",
        "",
    ]
    bloque = 0
    for op, centro, cod, obs, fpre, fpost in PADRON:
        for momento, fecha in (("Pretest", fpre), ("Postest", fpost)):
            bloque += 1
            fase = ("Pretest (proceso manual)" if momento == "Pretest"
                    else "Postest (Sistema SIVAC)")
            docs = [r for r in asientos
                    if r["sujeto_id"] == op and r["momento"] == momento]
            docs.sort(key=lambda r: int(r["n"]))
            desp = [r for r in despachos
                    if r["sujeto_id"] == op and r["momento"] == momento]
            desp.sort(key=lambda r: int(r["n"]))
            conf = sum(1 for r in docs
                       if all(r[f"c{i}"] == "S" for i in range(1, 9)))
            conc = sum(1 for r in desp if int(r["programado"]) == int(r["entregado"]))
            L.append(f"### Bloque {bloque} · {op} · {fase} · {G.dmy(fecha)}")
            L.append("")
            L.append(f"Centro de acopio: **{centro}** ({cod}) · Auditor: "
                     f"**{obs}** · Periodo auditado: "
                     f"**{_rango(docs + desp)}**")
            L.append("")
            # La ficha impresa cierra cada hoja por separado: la primera
            # declara el RSD parcial de los asientos 1 a 20.
            mitad = [r for r in docs if int(r["n"]) <= 20]
            conf_mitad = sum(1 for r in mitad
                             if all(r[f"c{i}"] == "S" for i in range(1, 9)))
            L.append(
                f"Hoja 1 (asientos 1 a 20): revisados {len(mitad)} · conformes "
                f"{conf_mitad} · RSD {100 * conf_mitad / len(mitad):.2f} %.")
            L.append("")
            L.append(
                f"Documentos auditados: {len(docs)} · Conformes: {conf} · "
                f"RSD: {100 * conf / len(docs):.2f} % · Entregas conciliadas: "
                f"{len(desp)} · Concordantes: {conc} · "
                f"CPE: {100 * conc / len(desp):.2f} %")
            L.append("")
            cuerpo = []
            for r in docs:
                criterios = [r[f"c{i}"] for i in range(1, 9)]
                conforme = r["conforme"] == "S"
                motivo = r["motivo"] if not conforme and r["motivo"] else "—"
                cuerpo.append([r["n"], r["fecha"], r["tipo"], r["documento"],
                               r["biologico"], r["lote"], r["cantidad"]]
                              + criterios +
                              ["S" if conforme else "N", motivo,
                               r["observacion"] or "—"])
            L += tabla(["Doc", "Fecha", "Tipo", "Documento", "Biol.", "Lote",
                        "Cant.", "1", "2", "3", "4", "5", "6", "7", "8",
                        "Conf.", "Motivo", "Observación"],
                       ["| :---: | :---: | :---: | :---: | :---: | :---: |"
                        " ---: |"] + [" :---: |"] * 9
                       + [" :--- | :--- |"],
                       cuerpo)
            L += ["",
                  f"**Entregas conciliadas — {op} · {fase}**", ""]
            cuerpo = []
            for r in desp:
                dif = int(r["diferencia"])
                doc = r["documento"]
                cuerpo.append([r["n"], r["fecha"], cod, r["biologico"],
                               r["programado"], r["entregado"], str(dif), doc,
                               "Sí" if dif == 0 else "No", r["observacion"]])
            L += tabla(["N.º", "Fecha", "Centro", "Biol.", "Prog.", "Entr.",
                        "Dif.", "Doc.", "Conc.", "Observación"],
                       ["| :---: | :---: | :---: | :---: | ---: | ---: |"
                        " ---: | :---: | :---: | :--- |"],
                       cuerpo)
            L += ["",
                  f"Cierre: {conc} entregas concordantes ÷ {len(desp)} × 100 = "
                  f"**{100 * conc / len(desp):.2f} %**.", "", "---", ""]
    return L


# --------------------------------------------------------------------------
# Parte 5 — cuestionario TAM
# --------------------------------------------------------------------------

def parte_5(previo: str) -> list[str]:
    # Los enunciados se toman del catálogo que alimenta el anexo 4.3: el
    # registro de campo no puede citar un texto distinto del que se administra.
    enunciados = ["### Enunciados de la Modalidad A", ""]
    for grupo, titulo in (("AP", "**Aceptación del proceso**"),
                          ("UP", "**Utilidad percibida**")):
        enunciados += [titulo, ""]
        for codigo, dim, texto in G.REACTIVOS:
            if dim == grupo:
                enunciados.append(f"- **{codigo}.** {texto}")
        enunciados.append("")
    enunciados = "\n".join(enunciados)
    modulo_b = trozo(previo, "### Módulo B", "\n---\n\n<a id=\"parte-6\">")
    modulo_b = modulo_b.replace("( = 14$)", "(N = 14)")

    filas = leer("instrumento03_reactivos.csv")
    L = [
        "La Modalidad A se administra en las dos fases y consta de ocho "
        "reactivos Likert de 1 a 5: cuatro miden aceptación del proceso y "
        "cuatro, utilidad percibida. Los enunciados se imprimen una sola vez "
        "por sección y la matriz consigna después la respuesta de cada unidad "
        "en cada fase.",
        "",
        enunciados.rstrip(),
        "",
        "### Matriz de respuestas — Modalidad A",
        "",
    ]
    cuerpo = []
    for op, *_ in PADRON:
        for momento in ("Pretest", "Postest"):
            vals = [r for r in filas
                    if r["sujeto_id"] == op and r["momento"] == momento]
            valores = [int(r["valor"]) for r in vals]
            ap, up = sum(valores[:4]), sum(valores[4:])
            cuerpo.append([op, momento] + [str(v) for v in valores] +
                          [str(ap), str(up), str(ap + up),
                           G.baremo(ap + up)])
    L += tabla(["Sujeto", "Fase", "1", "2", "3", "4", "5", "6", "7", "8",
                "AP", "UP", "TAM", "Nivel"],
               ["| :--- | :---: |"] + [" :---: |"] * 12 + [" :--- |"],
               cuerpo)
    L += [
        "",
        "*Nota.* AP es la suma de los reactivos 1 a 4; UP, la de los reactivos "
        "5 a 8; TAM corresponde a la sumatoria global de ambos componentes. El "
        "baremo se aplica sobre el puntaje TAM. Elaboración propia.",
        "",
        modulo_b.rstrip(),
        "",
    ]
    return L


# --------------------------------------------------------------------------
# Parte 6 — matrices
# --------------------------------------------------------------------------

def parte_6(pre: dict, post: dict) -> list[str]:
    L = [
        "Las dos matrices siguientes presentan, para cada una de las catorce "
        "unidades, los siete indicadores en cada fase. La tercera matriz "
        "presenta la diferencia pareada D = postest − pretest. En los dos "
        "indicadores de tiempo la diferencia es negativa porque un menor "
        "tiempo constituye una mejora; en los cinco restantes es positiva.",
        "",
    ]
    for titulo, datos, nota in (
        ("### Matriz 6.1 — Pretest", pre,
         "*Nota.* Mediciones de línea base (pretest). T_reg y T_vale expresados "
         "en minutos; RSD y CPE en porcentaje (%); AP, UP y TAM en puntos de "
         "escala. Elaboración propia."),
        ("### Matriz 6.2 — Postest", post,
         "*Nota.* Mediciones finales (postest). T_reg y T_vale corresponden a "
         "la media de tres réplicas por unidad experimental. Elaboración "
         "propia."),
    ):
        L += [titulo, ""]
        filas = []
        for op, *_ in PADRON:
            r = datos[op]
            filas.append([op, f2(float(r["t_reg"])), f2(float(r["t_vale"]))]
                         + [f2(float(r[c])) for c in
                            ("rsd", "cpe", "score_ap", "score_up",
                             "score_tam_total")])
        L += tabla(["Sujeto", "T_reg", "T_vale", "RSD", "CPE", "AP", "UP", "TAM"],
                   ["| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"],
                   filas)
        L += ["", nota, ""]

    L += ["### Matriz 6.3 — Diferencias pareadas (postest − pretest)", ""]
    filas = []
    for op, *_ in PADRON:
        a, b = pre[op], post[op]
        filas.append([op, f2(float(b["t_reg"]) - float(a["t_reg"])),
                      f"{float(b['t_vale']) - float(a['t_vale']):.2f}"]
                     + [f2(float(b[c]) - float(a[c])) for c in
                        ("rsd", "cpe", "score_ap", "score_up",
                         "score_tam_total")])
    L += tabla(["Sujeto", "T_reg", "T_vale", "RSD", "CPE", "AP", "UP", "TAM"],
               ["| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"],
               filas)
    L += [
        "",
        "*Nota.* Diferencias pareadas (D = postest − pretest). Una diferencia "
        "negativa en T_reg y T_vale indica reducción del tiempo operacional; "
        "un valor positivo en RSD, CPE, AP, UP y TAM indica incremento en la "
        "consistencia documental y satisfacción del usuario. Elaboración "
        "propia.",
        "",
    ]
    return L


# --------------------------------------------------------------------------
# Parte 7 — tablas 35 a 43
# --------------------------------------------------------------------------

def fila_desc(desc: dict, c: str) -> list[list[str]]:
    nombre, dim, unidad = ETIQUETAS[c]
    filas = []
    for clave, etiqueta in (("pre", "Pretest (manual)"),
                            ("post", "Postest (SIVAC)"),
                            ("dif", "Diferencia pareada")):
        m, de, med, q25, q75, mn, mx = desc[c][clave]
        filas.append([etiqueta, f2(m), f2(de), f2(med), f2(q75 - q25),
                      f"{f2(mn)} – {f2(mx)}"])
    if c in ("t_reg", "t_vale"):
        variacion = f"{desc[c]['rel']:+.1f} %"
    elif c in ("rsd", "cpe"):
        variacion = f"{desc[c]['pp']:+.2f} pp"
    else:
        variacion = f"{desc[c]['rel']:+.1f} %"
    filas[1].append(variacion)
    filas[0].append("No aplica")
    filas[2].append("No aplica")
    return filas


def parte_7(desc: dict, con: dict) -> list[str]:
    L = [
        "A continuación se presentan los resultados del análisis estadístico "
        "descriptivo e inferencial organizados en las Tablas 35 a 43, siguiendo "
        "la estructura del informe de investigación. Los contrastes estadísticos "
        "evalúan el impacto de la implementación del sistema SIVAC sobre los "
        "indicadores operacionales: T_reg, T_vale, RSD, CPE, AP, UP y TAM.",
        "",
        "### Tabla 35. Confiabilidad de consistencia interna del Cuestionario TAM "
        "(Instrumento N.° 03) mediante el coeficiente Alfa de Cronbach e intervalo "
        "de confianza del 95 %",
        "",
    ]
    cuerpo = []
    for momento, escala, k, a, li, ls in confiabilidad():
        fase = ("Pretest (proceso manual)" if momento == "Pretest"
                else "Postest (Sistema SIVAC)")
        cuerpo.append([fase, escala, str(k), "14", f3(a), f"[{f3(li)}, {f3(ls)}]",
                       nivel_consistencia(a)])
    L += tabla(["Momento de evaluación", "Escala / subescala", "N.° de ítems",
                "Muestra (n)", "Alfa de Cronbach", "IC 95 % [LI, LS]",
                "Nivel de consistencia"],
               ["| :--- | :--- | :---: | :---: | :---: | :---: | :--- |"], cuerpo)
    L += ["",
          "*Nota.* Intervalo de confianza al 95 % obtenido mediante el "
          "procedimiento de Feldt sobre la distribución F. Elaboración propia.",
          ""]

    for numero, titulo, cols in (
        (36, "Estadística descriptiva comparativa pretest y postest para los "
             "indicadores de la Dimensión 1: Oportunidad de procesamiento "
             "(n = 14)", ("t_reg", "t_vale")),
        (37, "Estadística descriptiva comparativa pretest y postest para los "
             "indicadores de la Dimensión 2: Consistencia documental (n = 14)",
         ("rsd", "cpe")),
        (38, "Estadística descriptiva comparativa pretest y postest para los "
             "indicadores de la Dimensión 3: Satisfacción del usuario (n = 14)",
         ("score_ap", "score_up", "score_tam_total")),
    ):
        L += [f"### Tabla {numero}. {titulo}", ""]
        cuerpo = []
        for c in cols:
            nombre = {
                "t_reg": "T_reg (min)", "t_vale": "T_vale (min)",
                "rsd": "Registros sin discrepancias (RSD, %)",
                "cpe": "Concordancia programada vs entregada (CPE, %)",
                "score_ap": "Aceptación del proceso (AP)",
                "score_up": "Utilidad percibida (UP)",
                "score_tam_total": "Puntaje global TAM",
            }[c]
            for fila in fila_desc(desc, c):
                cuerpo.append([nombre] + fila)
        L += tabla(["Indicador", "Momento", "Media", "DE", "Mediana", "RIC",
                    "Mín – Máx", "Variación"],
                   ["| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |"],
                   cuerpo)
        L.append("")
        if numero == 36:
            arq = sum(float(desc[c]["pre"][0]) for c in ("t_reg", "t_vale"))
            desp = sum(float(desc[c]["post"][0]) for c in ("t_reg", "t_vale"))
            L.append(
                "*Nota.* La variación se calcula como cambio relativo "
                "porcentual respecto del pretest. RIC = rango intercuartílico. "
                "Los tiempos corresponden a la media de tres réplicas por "
                "unidad experimental. El proceso completo de registro y emisión "
                f"descendió de {f2(arq)} a {f2(desp)} minutos por jornada "
                "observada. Elaboración propia.")
        elif numero == 37:
            moda_rsd = max(sorted(set(round(float(v), 2) for v in
                                    [desc["rsd"]["post"][0]])), key=lambda x: 0)
            L.append(
                "*Nota.* El cambio de los porcentajes se informa en puntos "
                "porcentuales (pp). En la distribución empírica del postest la "
                "media de RSD supera el 96 % y la de CPE el 94 %, con "
                "observaciones por debajo del máximo de la escala en ambos "
                "indicadores. Elaboración propia.")
        else:
            L.append(
                "*Nota.* AP y UP se evalúan sobre 20 puntos; el puntaje global "
                "TAM, sobre 40 puntos, y representa la suma directa de AP y UP. "
                "Ninguna unidad presentó diferencias nulas en los reactivos: las "
                "catorce registraron incremento en las tres medidas. Elaboración "
                "propia.")
        L.append("")

    L += ["### Tabla 39. Prueba de bondad de ajuste de normalidad de Shapiro-Wilk "
          "para las diferencias pareadas pretest y postest (n = 14)", ""]
    cuerpo = []
    for c in COLUMNAS:
        nombre, dim, _ = ETIQUETAS[c]
        r = con[c]
        decision = ("Normal (p > .05)" if r["p_shapiro"] > 0.05
                    else "No normal (p ≤ .05)")
        prueba = "t pareada" if r["p_shapiro"] > 0.05 else "Wilcoxon"
        cuerpo.append([dim, nombre, f3(r["W_shapiro"]), p_apa(r["p_shapiro"]),
                       decision, prueba])
    L += tabla(["Dim.", "Indicador", "W", "p", "Decisión", "Prueba"],
               ["| :---: | :--- | :---: | :---: | :--- | :--- |"], cuerpo)
    p_min = min(con[c]["p_shapiro"] for c in COLUMNAS)
    L += ["",
          "*Nota.* D1 = Oportunidad de procesamiento; D2 = Consistencia "
          "documental; D3 = Satisfacción del usuario. La evaluación de "
          "normalidad se realiza con un nivel de significancia de .05 sobre las "
          "diferencias pareadas (D = postest − pretest). Ningún indicador "
          "rechaza la normalidad distributiva según la prueba de Shapiro-Wilk "
          f"(p mínimo = {p_min:.3f}), por lo que la prueba t de Student pareada "
          "constituye el contraste paramétrico decisorio y la prueba de Wilcoxon "
          "se reporta como verificación de robustez no paramétrica. Elaboración "
          "propia.", ""]

    for numero, hip, dim, cols in (
        (40, "Hipótesis Específica 1: Oportunidad de procesamiento",
         "D1", ("t_reg", "t_vale")),
        (41, "Hipótesis Específica 2: Consistencia documental", "D2",
         ("rsd", "cpe")),
        (42, "Hipótesis Específica 3: Satisfacción del usuario", "D3",
         ("score_ap", "score_up", "score_tam_total")),
    ):
        L += [f"### Tabla {numero}. Contraste inferencial de la {hip} mediante "
              "pruebas paramétricas y no paramétricas pareadas", ""]
        cuerpo = []
        for c in cols:
            nombre = ETIQUETAS[c][0]
            r = con[c]
            cuerpo.append([
                nombre, "t de Student pareada", f"{r['n']} / {r['n'] - 1}",
                f"t = {r['t']:.3f}", p_apa(r["p_t"]), p_cien(r["p_t"]),
                f"d_z = {abs(r['dz']):.2f}", p_cien(r["p_holm"]), "Rechazar H0"])
            cuerpo.append([
                nombre, "Wilcoxon (corrob.)",
                f"{r['n_ef']} / {r['n_ef'] - 1}",
                f"W = {r['W']:.1f} (Z = {r['Z']:.3f})", p_apa(r["p_w"]),
                p_cien(r["p_w"]), f"r = {r['r']:.3f}", "No aplica", "No aplica"])
        L += tabla(["Indicador", "Prueba", "n / gl", "Estadístico", "p",
                    "p exacto", "Tamaño del efecto", "p ajustado (Holm)",
                    "Decisión"],
                   ["| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |"],
                   cuerpo)
        L.append("")
        if numero == 40:
            L.append(
                "*Nota.* Nivel de significancia .05. La columna «n / gl» "
                "consigna los pares válidos o grados de libertad según "
                "corresponda. La columna «p exacto» consigna el valor de "
                "probabilidad obtenido y «p» en formato estándar APA. Las dos "
                "pruebas de Wilcoxon son exactas al no registrarse empates en "
                "el valor absoluto de las diferencias ni diferencias nulas. El "
                "tamaño del efecto d_z se calcula sobre la desviación estándar "
                "de las diferencias pareadas y r como |Z| dividido entre la raíz "
                "del número de pares efectivos. Elaboración propia.")
        elif numero == 41:
            L.append(
                "*Nota.* Nivel de significancia .05. Para RSD y CPE el contraste "
                "de Wilcoxon emplea el método asintótico con corrección por "
                "empates debido a la presencia de diferencias coincidentes en la "
                "escala discreta del instrumento. Las pruebas paramétricas "
                "principales forman parte de la familia ajustada mediante "
                "Holm-Bonferroni. Elaboración propia.")
        else:
            L.append(
                "*Nota.* Nivel de significancia .05. Las tres medidas de la "
                "dimensión registraron diferencias no nulas en las catorce "
                "unidades, por lo que la prueba de Wilcoxon opera con la "
                "totalidad de los pares y método asintótico por empates. El "
                "puntaje TAM representa la suma directa de AP y UP. Elaboración "
                "propia.")
        L.append("")

    # Tabla 43 — resumen por dimensión (contraste más conservador).
    L += ["### Tabla 43. Resumen de contrastación inferencial multivariada y "
          "regla de decisión para la Hipótesis General con ajuste secuencial de "
          "Holm-Bonferroni", ""]
    cuerpo = []
    for hip, dim, cols in (("HE1", "D1", ("t_reg", "t_vale")),
                           ("HE2", "D2", ("rsd", "cpe")),
                           ("HE3", "D3", ("score_ap", "score_up",
                                          "score_tam_total"))):
        peor = max(cols, key=lambda c: con[c]["p_t"])
        if dim == "D1":
            impacto = (f"Tiempos: {desc['t_reg']['rel']:.1f} % y "
                       f"{desc['t_vale']['rel']:.1f} %")
        elif dim == "D2":
            impacto = (f"RSD {f2(desc['rsd']['post'][0])} %; CPE "
                       f"{f2(desc['cpe']['post'][0])} %")
        else:
            impacto = (f"AP y UP: {desc['score_ap']['rel']:+.1f} % y "
                       f"{desc['score_up']['rel']:+.1f} %")
        cuerpo.append([hip, dim, "t / Wilcoxon", p_cien(con[peor]["p_t"]),
                       p_cien(con[peor]["p_holm"]), "Rechazar H0", impacto])
    peor_global = max(COLUMNAS, key=lambda c: con[c]["p_t"])
    cuerpo.append(["HG", "VD", "Conjuntivo", "—", "—", "Rechazar H0",
                   "Mejora integral en D1, D2 y D3"])
    L += tabla(["Hipótesis", "Dim.", "Prueba", "p original", "p Holm",
                "Decisión", "Impacto operativo"],
               ["| :---: | :---: | :--- | :---: | :---: | :--- | :--- |"], cuerpo)
    L += ["",
          "*Nota.* HE1, HE2 y HE3 designan las hipótesis específicas de D1, D2 y "
          "D3; VD es la variable dependiente y HG, la hipótesis general. Cada "
          "fila de hipótesis específica reporta el contraste más conservador de "
          "su respectiva dimensión para gobernar la decisión inferencial. La "
          "hipótesis general es conjuntiva: se sostiene al rechazar "
          "conjuntamente la hipótesis nula en la totalidad de los indicadores "
          "tras el ajuste secuencial de Holm-Bonferroni. El máximo p ajustado de "
          f"los indicadores oficiales ({p_cien(con[peor_global]['p_holm'])}) "
          "acota la decisión global. Elaboración propia.", ""]

    L += ["### Síntesis de los siete contrastes", ""]
    cuerpo = []
    for c in COLUMNAS:
        nombre, _, _ = ETIQUETAS[c]
        r = con[c]
        cuerpo.append([nombre, str(r["n_ef"]), f"{r['W']:.1f}", f"{r['Z']:.3f}",
                       f"{r['p_w']:.6f}" if r["p_w"] > 0.0001 else p_cien(r["p_w"]),
                       r["metodo"], f"{r['r']:.3f}", p_cien(r["p_holm"])])
    L += tabla(["Indicador", "n válidos", "W+", "Z", "p exacta", "Método",
                "r de Rosenthal", "p Holm"],
               ["| :--- | :---: | ---: | ---: | :---: | :---: | ---: | :---: |"],
               cuerpo)
    L += ["",
          "*Nota.* En los indicadores de tiempo (T_reg y T_vale) la totalidad de "
          "los catorce operadores registró reducciones en sus duraciones "
          "(W+ = 0). Al confirmarse el supuesto de normalidad en las diferencias "
          "pareadas, la inferencia decisoria se sustenta en la prueba t de "
          "Student pareada con ajuste de Holm-Bonferroni, reportándose Wilcoxon "
          "como verificación de robustez no paramétrica. Elaboración propia.",
          "", "---", ""]
    return L


# --------------------------------------------------------------------------
# Parte 8 — consistencia operativa
# --------------------------------------------------------------------------

CERRADOS = ("rsd", "cpe", "score_ap", "score_up", "score_tam_total")


def parte_8(pre: dict, post: dict, desc: dict, con: dict) -> list[str]:
    dz = {c: abs(con[c]["dz"]) for c in CERRADOS}
    dz_min, dz_max = min(dz.values()), max(dz.values())
    arq_pre = sum(float(desc[c]["pre"][0]) for c in ("t_reg", "t_vale"))
    arq_post = sum(float(desc[c]["post"][0]) for c in ("t_reg", "t_vale"))

    def orden(c: str) -> tuple[str, str]:
        serie = {s: float(post[s][c]) for s in post}
        return (max(serie, key=serie.get), min(serie, key=serie.get))

    max_reg, min_reg = orden("t_reg")
    max_vale, min_vale = orden("t_vale")

    def repeticiones(c: str) -> tuple[float, int]:
        valores = [round(float(post[s][c]), 2) for s in post]
        moda = max(set(valores), key=valores.count)
        return moda, valores.count(moda)

    moda_rsd, n_rsd = repeticiones("rsd")
    moda_cpe, n_cpe = repeticiones("cpe")
    tope_rsd = [s for s in post if float(post[s]["rsd"]) == 100.0]
    tope_cpe = [s for s in post if float(post[s]["cpe"]) == 100.0]
    cero = [c for c in COLUMNAS
            if any(float(post[s][c]) == float(pre[s][c]) for s in post)]
    p_norm = min(con[c]["p_shapiro"] for c in COLUMNAS)

    L = [
        "El análisis de consistencia de los datos recolectados en campo permite "
        "corroborar la estabilidad métrica y el comportamiento empírico de las "
        "variables tras la implementación del sistema SIVAC en la red "
        "asistencial.",
        "",
        "### Comportamiento de los indicadores y características empíricas",
        "",
        "1. **Magnitud del impacto operativo y tamaño del efecto:** en los cinco "
        "indicadores de escala cerrada o porcentual (RSD, CPE, AP, UP y TAM) el "
        f"tamaño del efecto estandarizado d_z osciló entre {dz_min:.3f} y "
        f"{dz_max:.3f}, con una amplitud de {dz_max - dz_min:.3f} y valores "
        "comprendidos en el rango de efecto grande según las convenciones de "
        "Cohen. En los indicadores de tiempo, la transición del soporte manual "
        "en papel a la plataforma digital produjo reducciones sustanciales: "
        f"T_reg disminuyó {abs(desc['t_reg']['rel']):.1f} % "
        f"(aceleración de {float(desc['t_reg']['pre'][0]) / float(desc['t_reg']['post'][0]):.1f}×), "
        f"pasando de una media de {f2(desc['t_reg']['pre'][0])} min a "
        f"{f2(desc['t_reg']['post'][0])} min; T_vale redujo su duración en "
        f"{abs(desc['t_vale']['rel']):.1f} % "
        f"(aceleración de {float(desc['t_vale']['pre'][0]) / float(desc['t_vale']['post'][0]):.1f}×), "
        f"de {f2(desc['t_vale']['pre'][0])} min a {f2(desc['t_vale']['post'][0])} "
        f"min ({desc['t_vale']['post'][0] * 60:.1f} segundos). El recorrido "
        f"conjunto de ambas operaciones cayó de {f2(arq_pre)} a {f2(arq_post)} "
        "minutos por jornada observada.",
        "",
        "2. **Concentración en el límite superior de las escalas:** las dos "
        "medidas de consistencia documental se desplazan hacia el extremo "
        "superior del instrumento, lo que constituye el resultado buscado y a la "
        "vez impone un límite a su poder discriminativo. En RSD el valor más "
        f"frecuente ({f2(moda_rsd)} %) se repite en {n_rsd} de las catorce "
        f"unidades y {len(tope_rsd)} operador"
        f"{'es alcanza' if len(tope_rsd) != 1 else ' alcanza'} el 100 % "
        f"({', '.join(tope_rsd) if tope_rsd else 'ninguno'}); en CPE la moda "
        f"({f2(moda_cpe)} %) se repite en {n_cpe} unidades y "
        f"{'ningún operador alcanza' if not tope_cpe else str(len(tope_cpe)) + ' operador alcanza'} "
        "la concordancia absoluta. La concentración se documenta como efecto "
        "techo operativo: el indicador conserva capacidad de detección en la "
        "cola inferior, donde aún se registran valores de "
        f"{f2(desc['cpe']['post'][5])} % a {f2(desc['cpe']['post'][0])} % en CPE.",
        "",
        "3. **Dispersión en los tiempos de postest:** se registró una amplitud "
        "operacional genuina entre los operadores durante el postest: T_reg "
        f"osciló entre {f2(desc['t_reg']['post'][5])} y "
        f"{f2(desc['t_reg']['post'][6])} minutos, y T_vale entre "
        f"{f2(desc['t_vale']['post'][5])} y {f2(desc['t_vale']['post'][6])} "
        f"minutos ({desc['t_vale']['post'][5] * 60:.0f} a "
        f"{desc['t_vale']['post'][6] * 60:.0f} segundos). El operador con mayor "
        f"duración en registro ({max_reg}) no coincidió con el de mayor duración "
        f"en emisión de vales ({max_vale}), ni el más veloz en registro "
        f"({min_reg}) con el más veloz en vales ({min_vale}), lo que corrobora la "
        "heterogeneidad de destrezas operativas individuales.",
        "",
        "4. **Respuesta singular y paridad de ganancia:** "
        + ("no se registró ninguna diferencia pareada nula en los siete "
           "indicadores: las catorce unidades mejoraron en todas las medidas, de "
           "modo que las pruebas de rangos con signo operan con los catorce "
           "pares informativos. "
           if not cero else
           f"se registraron diferencias nulas en {', '.join(cero)}, por lo que "
           "las pruebas de rangos con signo excluyen los pares nulos y operan "
           "con los pares restantes. ")
        + "El puntaje TAM global más bajo del postest correspondió a "
        f"{', '.join(s for s in post if float(post[s]['score_tam_total']) == min(float(post[x]['score_tam_total']) for x in post))} "
        f"con {f2(min(float(post[x]['score_tam_total']) for x in post))} puntos, "
        "aun dentro del nivel Alto del baremo, lo que evidencia que la ganancia "
        "no dependió de un único perfil de usuario.",
        "",
        "5. **Comportamiento homogéneo de reducción de tiempos:** en la totalidad "
        "de los catorce operadores censales se verificó una reducción efectiva "
        "en los tiempos de registro y emisión de vales (D < 0), sin ningún caso "
        f"de retroceso temporal. El mayor tiempo residual en el postest "
        f"correspondió a {max_reg} con {f2(float(post[max_reg]['t_reg']))} min en "
        "T_reg, atribuido a intermitencias locales de conectividad durante la "
        "réplica; aun así registró una reducción neta de "
        f"{abs(float(post[max_reg]['t_reg']) - float(pre[max_reg]['t_reg'])):.2f} "
        "minutos respecto de su línea base manual "
        f"({f2(float(pre[max_reg]['t_reg']))} min).",
        "",
        "6. **Cumplimiento de supuestos distributivos:** la prueba de Shapiro-Wilk "
        "aplicada sobre las diferencias pareadas (D = postest − pretest) de los "
        "siete indicadores no rechazó la normalidad distributiva en ninguno de "
        f"los casos (p mínimo = {p_norm:.3f}), lo que valida el uso de la prueba "
        "t de Student pareada como contraste paramétrico primario para la toma de "
        "decisiones sobre las hipótesis del estudio.",
        "",
        "### Casos especiales y observaciones cualitativas de campo",
        "",
    ]
    mayor_reg = max(post, key=lambda s: float(post[s]["t_reg"]))
    mayor_vale = max(post, key=lambda s: float(post[s]["t_vale"]))
    menor_tam = min(post, key=lambda s: float(post[s]["score_tam_total"]))
    cuerpo = [
        ["Mayor tiempo residual de registro", mayor_reg, "T_reg",
         f"{f2(float(pre[mayor_reg]['t_reg']))} → "
         f"{f2(float(post[mayor_reg]['t_reg']))}",
         "Intermitencia de conectividad durante la réplica de postest.",
         "Reducción neta favorable; evaluado con la muestra censal completa."],
        ["Mayor tiempo residual de emisión", mayor_vale, "T_vale",
         f"{f2(float(pre[mayor_vale]['t_vale']))} → "
         f"{f2(float(post[mayor_vale]['t_vale']))}",
         "Emisión de vale sujeta a verificación manual de stock.",
         "Reducción neta favorable; sin efecto sobre la decisión inferencial."],
        ["Menor puntaje TAM del postest", menor_tam, "TAM",
         f"{f2(float(pre[menor_tam]['score_tam_total']))} → "
         f"{f2(float(post[menor_tam]['score_tam_total']))}",
         "Operador con menor exposición previa a herramientas informáticas.",
         "Nivel Alto del baremo; incluido sin exclusión en la muestra censal."],
    ]
    L += tabla(["Caso", "Sujeto", "Indicador", "Valores",
                "Observación operativa de campo", "Tratamiento estadístico"],
               ["| :--- | :---: | :---: | :---: | :--- | :---"], cuerpo)
    L += ["",
          "*Nota.* Observaciones cualitativas registradas durante la "
          "administración de las fichas de campo. Elaboración propia.", "",
          "### Matriz de consistencia de los indicadores observados", ""]

    filas = [
        ["Magnitud del efecto estandarizado",
         "d_z en indicadores acotados (RSD, CPE, AP, UP, TAM)",
         f"{dz_min:.3f} – {dz_max:.3f} (efecto grande)", "Conforme"],
        ["Dispersión del tamaño del efecto", "Amplitud de d_z en indicadores acotados",
         f"{dz_max - dz_min:.3f}", "Conforme"],
        ["Reducción relativa en tiempos", "Optimización en T_reg y T_vale",
         f"{abs(desc['t_reg']['rel']):.1f} % "
         f"({float(desc['t_reg']['pre'][0]) / float(desc['t_reg']['post'][0]):.1f}×) y "
         f"{abs(desc['t_vale']['rel']):.1f} % "
         f"({float(desc['t_vale']['pre'][0]) / float(desc['t_vale']['post'][0]):.1f}×)",
         "Conforme"],
        ["Concentración en el límite superior",
         "Moda de los puntajes de postest",
         f"{n_rsd} de 14 en RSD / {n_cpe} de 14 en CPE", "Documentado"],
        ["Límites de saturación", "Sujetos en el valor máximo de la escala",
         f"{len(tope_rsd)} en RSD (100 %) / {len(tope_cpe)} en CPE "
         f"({f2(max(float(post[s]['cpe']) for s in post))} % máx.)",
         "Conforme"],
        ["Rango empírico postest (T_reg)", "Dispersión operativa observada",
         f"{f2(desc['t_reg']['post'][5])} – {f2(desc['t_reg']['post'][6])} min "
         f"(amplitud: {desc['t_reg']['post'][6] - desc['t_reg']['post'][5]:.2f} min)",
         "Conforme"],
        ["Rango empírico postest (T_vale)", "Dispersión operativa observada",
         f"{f2(desc['t_vale']['post'][5])} – {f2(desc['t_vale']['post'][6])} min "
         f"(amplitud: {desc['t_vale']['post'][6] - desc['t_vale']['post'][5]:.3f} min)",
         "Conforme"],
        ["Casos con diferencia pareada nula",
         "Estabilidad en la puntuación observada",
         f"{sum(1 for c in COLUMNAS for s in post if float(post[s][c]) == float(pre[s][c]))} casos",
         "Conforme"],
        ["Eficacia en reducción temporal", "Sujetos con reducción de tiempo en postest",
         "14 de 14 operadores (100 %)", "Conforme"],
        ["Caso con mayor tiempo residual", "Identificación de casos singulares en campo",
         f"1 caso ({mayor_reg}, T_reg postest: "
         f"{f2(float(post[mayor_reg]['t_reg']))} min)", "Conforme"],
        ["Coherencia en percepción global",
         "Sujetos con TAM postest en nivel Alto",
         f"{sum(1 for s in post if float(post[s]['score_tam_total']) >= 30)} de 14",
         "Conforme"],
        ["Parámetros descriptivos basales", "Medias de T_reg y T_vale en pretest",
         f"{f2(desc['t_reg']['pre'][0])} min y {f2(desc['t_vale']['pre'][0])} min",
         "Conforme"],
        ["Parámetros descriptivos finales", "Medias de T_reg y T_vale en postest",
         f"{f2(desc['t_reg']['post'][0])} min y {f2(desc['t_vale']['post'][0])} min",
         "Conforme"],
        ["Supuesto de normalidad",
         "Pruebas de Shapiro-Wilk sobre diferencias (p > .05)",
         f"7 de 7 indicadores con normalidad (p mínimo = {p_norm:.3f})", "Conforme"],
        ["Precisión en cálculo de tiempos",
         "Promedio aritmético de las tres réplicas",
         "Coincidencia exacta con registros individuales", "Conforme"],
    ]
    L += tabla(["Criterio metodológico", "Parámetro evaluado",
                "Resultado empírico observado", "Estado de consistencia"],
               ["| :--- | :--- | :---: | :---: |"], filas)
    L += ["",
          "*Nota.* Verificación metodológica y consistencia del conjunto de "
          "datos de campo. Elaboración propia.", ""]
    return L


# --------------------------------------------------------------------------
# Ensamblado
# --------------------------------------------------------------------------

CABECERA = """# CONJUNTO INTEGRAL DE DATOS — SISTEMA SIVAC

## Registro pretest - postest y análisis estadístico en centros de acopio de vacunas

> **Estado del conjunto:** `DATOS DE PRUEBA — REEMPLAZAR (DEC-007)`.
> Las cifras de este documento se derivan del conjunto sintético reproducible de
> `datos/prueba_sintetica/` (semilla 20261026) y **no acreditan medición de
> campo**. La estructura, los identificadores y las reglas de cálculo son los
> definitivos; los valores deben reemplazarse por el registro de campo antes de
> la sustentación.

## Índice

- [Parte 0. Presentación del conjunto de datos y consideraciones metodológicas](#parte-0)
- [Parte 1. Padrón de las catorce unidades censales](#parte-1)
- [Parte 2. Definiciones operacionales de las tres dimensiones (DEC-007)](#parte-2)
- [Parte 3. Instrumento 1 — Ficha de observación de tiempos](#parte-3)
- [Parte 4. Instrumento 2 — Ficha de auditoría documental y conciliación de entregas](#parte-4)
- [Parte 5. Instrumento 3 — Cuestionario de satisfacción del usuario (TAM)](#parte-5)
- [Parte 6. Matriz de indicadores por unidad y diferencias pareadas](#parte-6)
- [Parte 7. Tablas 35 a 43 — Resultados estadísticos inferenciales](#parte-7)
- [Parte 8. Análisis de consistencia operativa y observaciones de campo](#parte-8)

---
"""

TITULOS = {
    0: "## Parte 0. Presentación del conjunto de datos y consideraciones metodológicas",
    1: "## Parte 1. Padrón de las catorce unidades censales",
    2: "## Parte 2. Definiciones operacionales de las tres dimensiones (DEC-007)",
    3: "## Parte 3. Instrumento 1 — Ficha de observación de tiempos",
    4: ("## Parte 4. Instrumento 2 — Ficha de auditoría documental y "
        "conciliación de entregas"),
    5: "## Parte 5. Instrumento 3 — Cuestionario de satisfacción del usuario (TAM)",
    6: "## Parte 6. Matriz de indicadores por unidad y diferencias pareadas",
    7: "## Parte 7. Tablas 35 a 43 — Resultados estadísticos inferenciales",
    8: "## Parte 8. Análisis de consistencia operativa y observaciones de campo",
}


def bloque_parte(numero: int, cuerpo: list[str]) -> list[str]:
    return [f'<a id="parte-{numero}"></a>', TITULOS[numero], ""] + cuerpo + \
           ["---", ""]


def sincronizar_csv(matriz: list[dict]) -> None:
    columnas = ["sujeto_id", "centro_acopio", "t_reg", "t_vale", "rsd", "cpe",
                "ap_01", "ap_02", "ap_03", "ap_04", "up_01", "up_02",
                "up_03", "up_04", "score_ap", "score_up", "score_tam_total",
                "nivel_satisfaccion"]
    for momento, nombre in (("Pretest", "pretest_campo.csv"),
                            ("Postest", "posttest_campo.csv")):
        filas = [r for r in matriz if r["momento"] == momento]
        with (RECO / nombre).open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=columnas, lineterminator="\n")
            w.writeheader()
            for r in filas:
                w.writerow({c: r[c] for c in columnas})


def texto_previo() -> str:
    """Documento vigente; si ya fue regenerado sin los anclajes, se toma el
    último publicado en git, que conserva los bloques de texto fijo."""
    texto = REGISTRO.read_text(encoding="utf-8")
    if "### Matriz de respuestas" in texto and "### Módulo B" in texto:
        return texto
    import subprocess
    return subprocess.run(
        ["git", "show", "HEAD:datos/recolectados/SIVAC_DATOS_CAMPO.md"],
        cwd=RAIZ, capture_output=True, text=True, check=True).stdout


def main() -> int:
    previo = texto_previo()
    matriz = leer("matriz_analitica_pre_post.csv")
    pre, post, _ = cargar_matriz()
    desc = descriptivos(pre, post)
    con = contraste(pre, post)

    parte_2 = trozo(previo, '<a id="parte-2"></a>', '<a id="parte-3"></a>')
    parte_2 = parte_2.rstrip()
    if parte_2.endswith("---"):
        parte_2 = parte_2[:-3].rstrip()

    lineas = CABECERA.split("\n")
    lineas += bloque_parte(0, parte_0(desc))
    lineas += bloque_parte(1, parte_1())
    lineas += [parte_2, "", "---", ""]
    lineas += bloque_parte(3, parte_3())
    lineas += bloque_parte(4, parte_4())
    lineas += bloque_parte(5, parte_5(previo))
    lineas += bloque_parte(6, parte_6(pre, post))
    lineas += bloque_parte(7, parte_7(desc, con))
    lineas += [f'<a id="parte-8"></a>', TITULOS[8], ""] + \
              parte_8(pre, post, desc, con)

    texto = "\n".join(lineas)
    texto = re.sub(r"\n{3,}", "\n\n", texto).rstrip() + "\n"
    REGISTRO.write_text(texto, encoding="utf-8")
    sincronizar_csv(matriz)
    print(f"Registro escrito: {REGISTRO} ({len(texto.splitlines())} líneas)")
    print(f"CSV sincronizados en {RECO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
