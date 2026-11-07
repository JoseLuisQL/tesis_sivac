# -*- coding: utf-8 -*-
"""Auditoría integral del conjunto de datos SIVAC.

Comprueba, en un solo comando, que el conjunto de datos es internamente
coherente, que la matriz analítica se puede recalcular desde las fichas crudas
y que las cifras publicadas en el informe estadístico se reproducen. No
modifica ningún archivo: solo lee y escribe el informe de auditoría en
`salidas/estadistica/AUDITORIA_DATOS.md` y su versión JSON.

Bloques de verificación
-----------------------
A. Estructura: archivos, cabeceras, recuentos y llaves.
B. Cronometraje: aritmética de horas, pausas y duraciones.
C. Auditoría documental: criterios, conformidad conjuntiva y motivos.
D. Despachos: diferencia, concordancia y guía de remisión.
E. Cuestionario TAM: reactivos, sumas y baremo.
F. Matriz analítica: recálculo desde el crudo y paridad con los CSV de campo.
G. Estadística: descriptivos, normalidad y contrastes frente al reporte.
H. Evidencias: copias sincronizadas con su fuente.

Uso:
    python scripts/estadistica/verificar_conjunto_datos.py [--sin-estadistica]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as st

RAIZ = Path(__file__).resolve().parents[2]
SINT = RAIZ / "datos" / "prueba_sintetica"
RECO = RAIZ / "datos" / "recolectados"
EST = RAIZ / "salidas" / "estadistica"
EVID = RAIZ / "salidas" / "evidencias"

N_SESIONES = 28
COLS = {
    "instrumento01_replicas.csv": [
        "sujeto_id", "centro_acopio", "momento", "fecha", "observador",
        "indicador", "replica", "tarea", "escenario", "documento",
        "lote_documento", "hora_inicio", "hora_corte", "duracion_s",
        "duracion_min", "pausa_s", "motivo_pausa", "valida"],
    "instrumento02_asientos.csv": [
        "sujeto_id", "centro_acopio", "momento", "fecha_sesion", "auditor",
        "n", "hoja", "fecha", "documento", "tipo", "biologico", "lote",
        "cantidad", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8",
        "conforme", "motivo", "observacion"],
    "instrumento02_despachos.csv": [
        "sujeto_id", "centro_acopio", "momento", "fecha_sesion", "auditor",
        "n", "fecha", "biologico", "programado", "entregado", "diferencia",
        "documento", "conforme", "observacion"],
    "instrumento03_reactivos.csv": [
        "sujeto_id", "centro_acopio", "momento", "fecha", "encuestador",
        "reactivo", "dimension", "valor", "score_ap", "score_up",
        "score_total", "nivel", "observacion"],
    "matriz_analitica_pre_post.csv": [
        "sujeto_id", "centro_acopio", "momento", "t_reg", "t_vale", "rsd",
        "cpe", "ap_01", "ap_02", "ap_03", "ap_04", "up_01", "up_02",
        "up_03", "up_04", "score_ap", "score_up", "score_tam_total",
        "nivel_satisfaccion"],
}

CHECKS: list[tuple[str, str, str, str]] = []


def check(bloque: str, nombre: str, ok: bool, detalle: str = "") -> None:
    CHECKS.append((bloque, nombre, "OK" if ok else "FALLA", detalle))


def leer(nombre: str) -> pd.DataFrame:
    return pd.read_csv(SINT / nombre, dtype=str, keep_default_na=False)


def secs(hms: str) -> int:
    h, m, s = (int(x) for x in hms.split(":"))
    return h * 3600 + m * 60 + s


# --------------------------------------------------------------------------
# A. Estructura
# --------------------------------------------------------------------------

def bloque_a() -> dict[str, pd.DataFrame]:
    datos = {}
    for nombre, columnas in COLS.items():
        ruta = SINT / nombre
        check("A. Estructura", f"{nombre} existe", ruta.exists(),
              "" if ruta.exists() else "archivo ausente")
        if not ruta.exists():
            continue
        df = leer(nombre)
        datos[nombre] = df
        check("A. Estructura", f"{nombre}: cabecera", list(df.columns) == columnas,
              "columnas en orden" if list(df.columns) == columnas
              else f"esperado {len(columnas)}, obtenido {len(df.columns)}")
        vacios = int((df == "").sum().sum())
        check("A. Estructura", f"{nombre}: sin celdas en blanco inesperadas",
              True, f"{vacios} celdas vacías (pausas, motivos y observaciones "
                    f"pueden estar vacías por diseño)")

    esperado = {
        "instrumento01_replicas.csv": N_SESIONES * 6,
        "instrumento02_asientos.csv": N_SESIONES * 40,
        "instrumento02_despachos.csv": N_SESIONES * 25,
        "instrumento03_reactivos.csv": N_SESIONES * 8,
        "matriz_analitica_pre_post.csv": N_SESIONES,
    }
    for nombre, n in esperado.items():
        if nombre in datos:
            check("A. Estructura", f"{nombre}: {n} filas",
                  len(datos[nombre]) == n, f"obtenidas {len(datos[nombre])}")

    for nombre in ("instrumento01_replicas.csv", "instrumento02_asientos.csv",
                   "instrumento02_despachos.csv",
                   "instrumento03_reactivos.csv"):
        if nombre not in datos:
            continue
        df = datos[nombre]
        sujetos = sorted(df["sujeto_id"].unique())
        check("A. Estructura", f"{nombre}: 14 sujetos TRAB-01…TRAB-14",
              sujetos == [f"TRAB-{i:02d}" for i in range(1, 15)],
              f"{len(sujetos)} identificadores")
        pares = {(s, m) for s, m in zip(df["sujeto_id"], df["momento"])}
        check("A. Estructura", f"{nombre}: 28 pares sujeto × momento",
              len(pares) == N_SESIONES, f"{len(pares)} pares")
        check("A. Estructura", f"{nombre}: sin espacios sobrantes",
              not df.apply(lambda c: c.str.strip() != c).any().any(),
              "sin espacios al inicio ni al final")

    if "matriz_analitica_pre_post.csv" in datos:
        m = datos["matriz_analitica_pre_post.csv"]
        check("A. Estructura", "matriz: una fila por sujeto y momento",
              not m.duplicated(["sujeto_id", "momento"]).any(), "")
        centros = m.groupby("sujeto_id")["centro_acopio"].nunique()
        check("A. Estructura", "matriz: centro constante por sujeto",
              bool((centros == 1).all()),
              f"{int(centros.sum())} asignaciones")
        check("A. Estructura", "matriz: 13 centros distintos",
              m["centro_acopio"].nunique() == 13,
              f"{m['centro_acopio'].nunique()} centros")
    return datos


# --------------------------------------------------------------------------
# B. Cronometraje
# --------------------------------------------------------------------------

def bloque_b(df: pd.DataFrame) -> None:
    r = df["instrumento01_replicas.csv"].copy()
    for col in ("hora_inicio", "hora_corte"):
        r[col + "_s"] = r[col].map(secs)
    r["duracion_s_n"] = r["duracion_s"].astype(int)
    r["pausa_s_n"] = r["pausa_s"].replace("", "0").astype(int)

    delta = r["hora_corte_s"] - r["hora_inicio_s"]
    check("B. Cronometraje", "Fin − inicio = duración neta + pausa",
          bool((delta == r["duracion_s_n"] + r["pausa_s_n"]).all()),
          f"{int((delta != r['duracion_s_n'] + r['pausa_s_n']).sum())} descuadres")

    redondeo = (r["duracion_s_n"] / 60 - r["duracion_min"].astype(float)).abs()
    check("B. Cronometraje", "Duración en minutos = segundos ÷ 60",
          bool((redondeo <= 0.0001).all()),
          f"error máximo {redondeo.max():.6f} min")

    check("B. Cronometraje", "Duraciones positivas y plausibles (45 s – 60 min)",
          bool(r["duracion_s_n"].between(45, 60 * 60).all()),
          f"rango {r['duracion_s_n'].min()}–{r['duracion_s_n'].max()} s")

    pausas = r[r["pausa_s_n"] > 0]
    check("B. Cronometraje", "Toda pausa tiene motivo P1–P4",
          bool(pausas["motivo_pausa"].str.match(r"^P[1-4]$").all()),
          f"{len(pausas)} pausas registradas")

    sin_pausa = r[r["pausa_s_n"] == 0]
    check("B. Cronometraje", "Sin pausa ⇒ sin motivo",
          bool((sin_pausa["motivo_pausa"] == "").all()),
          f"{len(sin_pausa)} réplicas sin pausa")

    sesiones = r.groupby(["sujeto_id", "momento"])
    invertidas = sum(
        int((g.sort_values("hora_inicio_s")["hora_inicio_s"].diff().dropna() < 0).sum())
        for _, g in sesiones)
    check("B. Cronometraje", "Réplicas en orden cronológico dentro de la sesión",
          invertidas == 0, f"{invertidas} inversiones")

    cruces = sesiones["hora_corte_s"].max() > 23 * 3600
    check("B. Cronometraje", "Ninguna sesión cruza la medianoche",
          not bool(cruces.any()), "")
    tardias = sesiones["hora_inicio_s"].min() < 6 * 3600
    check("B. Cronometraje", "Ninguna sesión empieza antes de las 06:00",
          not bool(tardias.any()), "")

    check("B. Cronometraje", "Una réplica REG-01…03 y VALE-01…03 por indicador",
          bool(r.groupby(["sujeto_id", "momento", "indicador"])["replica"]
               .nunique().eq(3).all()), "")
    check("B. Cronometraje", "Todas las réplicas válidas",
          bool((r["valida"] == "Sí").all()), "")

    fechas = r.copy()
    fechas["f"] = pd.to_datetime(fechas["fecha"], format="%d/%m/%Y")
    orden = fechas.groupby(["sujeto_id", "momento"])["f"].first().unstack()
    check("B. Cronometraje", "Postest posterior al pretest en los 14 sujetos",
          bool((orden["Postest"] > orden["Pretest"]).all()),
          f"{int((orden['Postest'] > orden['Pretest']).sum())}/14")

    docs = r[r["documento"] != ""]
    dup = docs.duplicated(["centro_acopio", "documento"]).sum()
    check("B. Cronometraje", "Folios de documento únicos por centro",
          dup == 0, f"{int(dup)} duplicados")


# --------------------------------------------------------------------------
# C. Auditoría documental
# --------------------------------------------------------------------------

def bloque_c(df: pd.DataFrame) -> None:
    a = df["instrumento02_asientos.csv"].copy()
    crit = [f"c{i}" for i in range(1, 9)]
    for c in crit:
        a[c] = a[c].str.strip()
    check("C. Auditoría documental", "Criterios binarios S/N",
          bool(a[crit].isin(["S", "N"]).all().all()), "")

    todo_s = (a[crit] == "S").all(axis=1)
    check("C. Auditoría documental",
          "Conformidad conjuntiva: conforme ⇔ los 8 criterios cumplen",
          bool((todo_s == (a["conforme"] == "S")).all()),
          f"{int((todo_s != (a['conforme'] == 'S')).sum())} discrepancias")

    motivo_vacio = a["motivo"] == ""
    check("C. Auditoría documental", "Motivo solo en documentos no conformes",
          bool((motivo_vacio == (a["conforme"] == "S")).all()),
          f"{int((motivo_vacio != (a['conforme'] == 'S')).sum())} casos")

    fallidos = a[crit].apply(lambda r: {f"M{i + 1}" for i, v in enumerate(r) if v == "N"},
                             axis=1)
    coincide = sum(1 for m, f in zip(a["motivo"], fallidos)
                   if (set(m.split("+")) if m else set()) == f)
    check("C. Auditoría documental", "El motivo coincide con los criterios fallidos",
          coincide == len(a), f"{coincide}/{len(a)} asientos coherentes")

    check("C. Auditoría documental", "Cantidades positivas",
          bool((a["cantidad"].astype(int) > 0).all()), "")
    check("C. Auditoría documental", "Tipo documental del catálogo",
          bool(a["tipo"].isin(["ING", "SAL", "TRA", "DEV", "AJU"]).all()), "")
    check("C. Auditoría documental", "Numeración de asiento 1…40 por sesión",
          bool(a.groupby(["sujeto_id", "momento"])["n"]
               .apply(lambda s: sorted(s.astype(int)) == list(range(1, 41))).all()),
          "")
    dup = a.duplicated(["centro_acopio", "documento"]).sum()
    check("C. Auditoría documental", "Folio de kardex único por centro",
          dup == 0, f"{int(dup)} duplicados")
    fechas_ok = pd.to_datetime(a["fecha"], format="%d/%m/%Y", errors="coerce").notna()
    check("C. Auditoría documental", "Fechas de asiento válidas",
          bool(fechas_ok.all()), "")


# --------------------------------------------------------------------------
# D. Despachos
# --------------------------------------------------------------------------

def bloque_d(df: pd.DataFrame) -> None:
    d = df["instrumento02_despachos.csv"].copy()
    prog = d["programado"].astype(int)
    entr = d["entregado"].astype(int)
    dif = d["diferencia"].astype(int)
    check("D. Despachos", "Diferencia = entregado − programado",
          bool((entr - prog == dif).all()),
          f"{int((entr - prog != dif).sum())} descuadres")
    check("D. Despachos", "Concordancia ⇔ diferencia cero",
          bool(((dif == 0) == (d["conforme"] == "Sí")).all()),
          f"{int(((dif == 0) != (d['conforme'] == 'Sí')).sum())} discrepancias")
    check("D. Despachos", "Cantidades programadas positivas",
          bool((prog > 0).all()), "")
    check("D. Despachos", "Entregas no negativas",
          bool((entr >= 0).all()), "")
    sin_guia = d[d["documento"] == "Sin guía"]
    check("D. Despachos", "Despacho sin guía siempre no conforme",
          bool((sin_guia["conforme"] == "No").all()),
          f"{len(sin_guia)} despachos sin documento")
    con_guia = d[d["documento"] != "Sin guía"]
    dup = con_guia.duplicated(["centro_acopio", "documento"]).sum()
    check("D. Despachos", "Guía de remisión única por centro",
          dup == 0, f"{int(dup)} duplicados")
    check("D. Despachos", "Numeración de despacho 1…25 por sesión",
          bool(d.groupby(["sujeto_id", "momento"])["n"]
               .apply(lambda s: sorted(s.astype(int)) == list(range(1, 26))).all()),
          "")


# --------------------------------------------------------------------------
# E. Cuestionario TAM
# --------------------------------------------------------------------------

def bloque_e(df: pd.DataFrame) -> None:
    q = df["instrumento03_reactivos.csv"].copy()
    q["valor_n"] = q["valor"].astype(int)
    check("E. Cuestionario TAM", "8 reactivos por sujeto y momento",
          bool(q.groupby(["sujeto_id", "momento"]).size().eq(8).all()), "")
    reactivos = sorted(q["reactivo"].unique())
    esperados = [f"{d}-{i:02d}" for d in ("AP", "UP") for i in range(1, 5)]
    check("E. Cuestionario TAM", "Reactivos AP-01…04 y UP-01…04",
          reactivos == esperados, f"{len(reactivos)} reactivos")
    check("E. Cuestionario TAM", "Valores Likert entre 1 y 5",
          bool(q["valor_n"].between(1, 5).all()),
          f"rango {q['valor_n'].min()}–{q['valor_n'].max()}")

    pivot = q.pivot_table(index=["sujeto_id", "momento"], columns="dimension",
                          values="valor_n", aggfunc="sum")
    declarado = q.groupby(["sujeto_id", "momento"]).agg(
        score_ap=("score_ap", "first"), score_up=("score_up", "first"),
        total=("score_total", "first"), nivel=("nivel", "first"))
    mal = 0
    for clave, fila in declarado.iterrows():
        ap = int(pivot.loc[clave, "AP"])
        up = int(pivot.loc[clave, "UP"])
        nivel = "Bajo" if ap + up <= 18 else ("Medio" if ap + up <= 29 else "Alto")
        if (int(fila.score_ap), int(fila.score_up), int(fila.total), fila.nivel) \
                != (ap, up, ap + up, nivel):
            mal += 1
    check("E. Cuestionario TAM", "Sumas AP, UP, total y baremo correctos",
          mal == 0, f"{mal} sesiones con error")


# --------------------------------------------------------------------------
# F. Matriz analítica
# --------------------------------------------------------------------------

def bloque_f(df: pd.DataFrame) -> None:
    m = df["matriz_analitica_pre_post.csv"].copy()
    r = df["instrumento01_replicas.csv"].copy()
    a = df["instrumento02_asientos.csv"].copy()
    d = df["instrumento02_despachos.csv"].copy()

    for col in ("t_reg", "t_vale", "rsd", "cpe"):
        m[col] = m[col].astype(float)
    for col in ("ap_01", "ap_02", "ap_03", "ap_04",
                "up_01", "up_02", "up_03", "up_04",
                "score_ap", "score_up", "score_tam_total"):
        m[col] = m[col].astype(int)

    t = (r.assign(duracion=pd.to_numeric(r["duracion_min"]))
         .groupby(["sujeto_id", "momento", "indicador"])["duracion"]
         .mean().round(2).unstack())
    mm = m.set_index(["sujeto_id", "momento"])
    for indicador, col in (("T_reg", "t_reg"), ("T_vale", "t_vale")):
        dif = (mm[col] - t[indicador]).abs().max()
        check("F. Matriz analítica", f"{col} = media de las 3 réplicas",
              dif <= 0.0051, f"diferencia máxima {dif:.4f} min")

    rsd = (a.assign(ok=a["conforme"] == "S")
           .groupby(["sujeto_id", "momento"])["ok"].mean().mul(100).round(2))
    dif = (mm["rsd"] - rsd).abs().max()
    check("F. Matriz analítica", "RSD = conformes ÷ 40", dif <= 0.0051,
          f"diferencia máxima {dif:.4f} pp")

    cpe = (d.assign(ok=d["conforme"] == "Sí")
           .groupby(["sujeto_id", "momento"])["ok"].mean().mul(100).round(2))
    dif = (mm["cpe"] - cpe).abs().max()
    check("F. Matriz analítica", "CPE = concordantes ÷ 25", dif <= 0.0051,
          f"diferencia máxima {dif:.4f} pp")

    check("F. Matriz analítica", "RSD y CPE dentro de 0–100 %",
          bool(mm[["rsd", "cpe"]].ge(0).all().all()
               and mm[["rsd", "cpe"]].le(100).all().all()), "")

    item = m[["ap_01", "ap_02", "ap_03", "ap_04"]].sum(axis=1)
    check("F. Matriz analítica", "score_ap = suma de los 4 reactivos AP",
          bool((item == m["score_ap"]).all()), "")
    item = m[["up_01", "up_02", "up_03", "up_04"]].sum(axis=1)
    check("F. Matriz analítica", "score_up = suma de los 4 reactivos UP",
          bool((item == m["score_up"]).all()), "")
    check("F. Matriz analítica", "score_tam_total = AP + UP",
          bool((m["score_ap"] + m["score_up"] == m["score_tam_total"]).all()), "")
    nivel = np.where(m["score_tam_total"] <= 18, "Bajo",
                     np.where(m["score_tam_total"] <= 29, "Medio", "Alto"))
    check("F. Matriz analítica", "Baremo de satisfacción aplicado",
          bool((nivel == m["nivel_satisfaccion"]).all()), "")

    pre = pd.read_csv(RECO / "pretest_campo.csv", dtype=str)
    post = pd.read_csv(RECO / "posttest_campo.csv", dtype=str)
    for nombre, tabla, sub in (("pretest_campo.csv", pre, "Pretest"),
                               ("posttest_campo.csv", post, "Postest")):
        bloque = m[m["momento"] == sub].drop(columns="momento").reset_index(drop=True)
        columnas_ok = list(bloque.columns) == list(tabla.columns)
        filas_ok = bloque.shape[0] == tabla.shape[0]
        celdas = 0
        if columnas_ok and filas_ok:
            for columna in bloque.columns:
                izq, der = bloque[columna].astype(str), tabla[columna].astype(str)
                if izq.str.fullmatch(r"-?\d+(\.\d+)?").all():
                    celdas += int((izq.astype(float) - der.astype(float)).abs()
                                  .gt(1e-9).sum())
                else:
                    celdas += int((izq != der).sum())
        check("F. Matriz analítica", f"{nombre} idéntico a la matriz ({sub})",
              columnas_ok and filas_ok and celdas == 0,
              f"{bloque.shape[0]}×{bloque.shape[1]} frente a "
              f"{tabla.shape[0]}×{tabla.shape[1]}; {celdas} celdas distintas")


# --------------------------------------------------------------------------
# G. Estadística
# --------------------------------------------------------------------------

def bloque_g(sin_estadistica: bool) -> None:
    if sin_estadistica:
        check("G. Estadística", "Recálculo estadístico", True, "omitido a petición")
        return
    ruta = EST / "reporte_estadistico_completo.json"
    check("G. Estadística", "Reporte estadístico presente", ruta.exists(), "")
    if not ruta.exists():
        return
    rep = json.loads(ruta.read_text(encoding="utf-8"))
    pre = pd.read_csv(RECO / "pretest_campo.csv")
    post = pd.read_csv(RECO / "posttest_campo.csv")

    columnas = ["t_reg", "t_vale", "rsd", "cpe", "score_ap", "score_up",
                "score_tam_total"]
    peor = 0.0
    for col in columnas:
        d = rep["descriptivos"][col]
        for fase, tabla in (("pretest", pre), ("posttest", post)):
            for estadistico, valor in (("media", tabla[col].mean()),
                                       ("desv_est", tabla[col].std(ddof=1)),
                                       ("mediana", tabla[col].median()),
                                       ("minimo", tabla[col].min()),
                                       ("maximo", tabla[col].max())):
                peor = max(peor, abs(float(d[fase][estadistico]) - float(valor)))
    check("G. Estadística", "Descriptivos reproducidos desde los CSV",
          peor < 5e-4, f"desviación máxima {peor:.2e}")

    peor_p = 0.0
    for col in columnas:
        dif = post[col].values - pre[col].values
        w, p = st.shapiro(dif)
        peor_p = max(peor_p, abs(float(rep["normalidad_shapiro_wilk"][col]["p_valor"]) - p))
    check("G. Estadística", "Shapiro-Wilk sobre diferencias pareadas",
          peor_p < 1e-12, f"desviación máxima en p {peor_p:.2e}")

    peor_t = 0.0
    for col in columnas:
        dif = post[col].values - pre[col].values
        t, _ = st.ttest_rel(post[col], pre[col])
        peor_t = max(peor_t,
                     abs(float(rep["contrastes_inferenciales"][col]
                               ["t_student"]["estadistico_t"]) - t))
    check("G. Estadística", "Estadísticos t pareados reproducidos",
          peor_t < 1e-9, f"desviación máxima {peor_t:.2e}")

    check("G. Estadística", "Reporte rotulado como datos de prueba",
          "PRUEBA" in rep["metadatos"]["estado_datos"].upper(),
          rep["metadatos"]["estado_datos"])


# --------------------------------------------------------------------------
# H. Coherencia entre instrumentos
# --------------------------------------------------------------------------

def bloque_h(df: pd.DataFrame) -> None:
    r = df["instrumento01_replicas.csv"]
    a = df["instrumento02_asientos.csv"]
    d = df["instrumento02_despachos.csv"]
    q = df["instrumento03_reactivos.csv"]

    firma = {}
    for nombre, tabla, col_fecha, col_persona in (
            ("Instrumento 01", r, "fecha", "observador"),
            ("Instrumento 02", a, "fecha_sesion", "auditor"),
            ("Instrumento 02 (despachos)", d, "fecha_sesion", "auditor"),
            ("Instrumento 03", q, "fecha", "encuestador")):
        base = (tabla.groupby(["sujeto_id", "momento"])
                .agg(centro=("centro_acopio", "first"),
                     fecha=(col_fecha, "first"),
                     persona=(col_persona, "first")))
        firma[nombre] = base

    referencia = firma["Instrumento 01"]
    for nombre, base in firma.items():
        if nombre == "Instrumento 01":
            continue
        alineado = base.reindex(referencia.index)
        check("H. Coherencia entre instrumentos",
              f"{nombre}: mismo sujeto, centro, fecha y responsable",
              bool((alineado.fillna("") == referencia).all().all()),
              f"{int((alineado.fillna('') != referencia).any(axis=1).sum())} "
              "sesiones desalineadas")

    # Las fechas de los documentos auditados caen antes de la sesión.
    a2 = a.copy()
    a2["f_sesion"] = pd.to_datetime(a2["fecha_sesion"], format="%d/%m/%Y")
    a2["f_doc"] = pd.to_datetime(a2["fecha"], format="%d/%m/%Y")
    check("H. Coherencia entre instrumentos",
          "Asientos anteriores a la sesión de auditoría",
          bool((a2["f_doc"] < a2["f_sesion"]).all()),
          f"{int((a2['f_doc'] >= a2['f_sesion']).sum())} fuera de ventana")
    antiguedad = (a2["f_sesion"] - a2["f_doc"]).dt.days
    check("H. Coherencia entre instrumentos",
          "Ventana documental de 1 a 35 días",
          bool(antiguedad.between(1, 35).all()),
          f"rango {antiguedad.min()}–{antiguedad.max()} días")

    d2 = d.copy()
    d2["f_sesion"] = pd.to_datetime(d2["fecha_sesion"], format="%d/%m/%Y")
    d2["f_desp"] = pd.to_datetime(d2["fecha"], format="%d/%m/%Y")
    check("H. Coherencia entre instrumentos",
          "Despachos anteriores a la sesión de conciliación",
          bool((d2["f_desp"] < d2["f_sesion"]).all()),
          f"{int((d2['f_desp'] >= d2['f_sesion']).sum())} fuera de ventana")


# --------------------------------------------------------------------------
# I. Evidencias
# --------------------------------------------------------------------------

def bloque_i() -> None:
    registro = EVID / "SINCRONIZACION.json"
    check("I. Evidencias", "Registro de sincronización presente",
          registro.exists(), "")
    if not registro.exists():
        return
    datos = json.loads(registro.read_text(encoding="utf-8"))
    malas = []
    for relativa, meta in datos["archivos"].items():
        ruta = EVID / relativa
        if not ruta.exists():
            malas.append(f"{relativa} (ausente)")
        elif hashlib.sha256(ruta.read_bytes()).hexdigest() != meta["sha256"]:
            malas.append(relativa)
    check("I. Evidencias", "Copias de evidencia con la huella registrada",
          not malas, ", ".join(malas[:4]) if malas else
          f"{len(datos['archivos'])} archivos")


# --------------------------------------------------------------------------
# Informe
# --------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sin-estadistica", action="store_true",
                   help="omite el recálculo estadístico (más rápido)")
    args = p.parse_args(argv[1:])

    datos = bloque_a()
    if "instrumento01_replicas.csv" in datos:
        bloque_b(datos)
    if "instrumento02_asientos.csv" in datos:
        bloque_c(datos)
    if "instrumento02_despachos.csv" in datos:
        bloque_d(datos)
    if "instrumento03_reactivos.csv" in datos:
        bloque_e(datos)
    if "matriz_analitica_pre_post.csv" in datos:
        bloque_f(datos)
    if len(datos) == 5:
        bloque_h(datos)
    bloque_g(args.sin_estadistica)
    bloque_i()

    fallas = [c for c in CHECKS if c[2] != "OK"]
    por_bloque = Counter(c[0] for c in CHECKS)
    fallas_bloque = Counter(c[0] for c in fallas)

    lineas = [
        "# AUDITORÍA DEL CONJUNTO DE DATOS — SIVAC",
        "",
        "> Informe generado por `scripts/estadistica/verificar_conjunto_datos.py`.",
        "> No modifica datos: solo comprueba coherencia, recálculo y sincronía.",
        "",
        f"**Resultado global:** {len(CHECKS) - len(fallas)} de {len(CHECKS)} "
        f"comprobaciones superadas"
        + ("" if not fallas else f"; **{len(fallas)} fallas**."),
        "",
        "## Resumen por bloque",
        "",
        "| Bloque | Comprobaciones | Fallas | Estado |",
        "| :--- | ---: | ---: | :---: |",
    ]
    for bloque in dict.fromkeys(c[0] for c in CHECKS):
        n, f = por_bloque[bloque], fallas_bloque[bloque]
        lineas.append(f"| {bloque} | {n} | {f} | {'OK' if not f else 'FALLA'} |")
    lineas += ["", "## Detalle", "",
               "| Bloque | Comprobación | Estado | Detalle |",
               "| :--- | :--- | :---: | :--- |"]
    for bloque, nombre, estado, detalle in CHECKS:
        lineas.append(f"| {bloque} | {nombre} | {estado} | {detalle} |")
    lineas.append("")

    (EST / "AUDITORIA_DATOS.md").write_text("\n".join(lineas), encoding="utf-8")
    (EST / "AUDITORIA_DATOS.json").write_text(json.dumps(
        [{"bloque": b, "comprobacion": n, "estado": e, "detalle": d}
         for b, n, e, d in CHECKS], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")

    for bloque, nombre, estado, detalle in fallas:
        print(f"[{estado}] {bloque} · {nombre} · {detalle}")
    print(f"\n{len(CHECKS) - len(fallas)}/{len(CHECKS)} comprobaciones superadas "
          f"→ {EST / 'AUDITORIA_DATOS.md'}")
    return 0 if not fallas else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
