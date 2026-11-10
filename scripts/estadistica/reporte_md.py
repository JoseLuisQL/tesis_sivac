# -*- coding: utf-8 -*-
"""Genera REPORTE_ESTADISTICO_FINAL.md con todas las tablas a partir del JSON/dataframes (sin cifras escritas a mano)."""
import json

def f(x, d=2):
    return "—" if x is None else f"{x:.{d}f}"

def pf(p):
    return "< .001" if p < 0.001 else f"{p:.3f}"

def tabla(h, rows):
    return ["| " + " | ".join(h) + " |", "|" + "|".join("---" for _ in h) + "|"] + ["| " + " | ".join(map(str, r)) + " |" for r in rows] + [""]

def escribir_md(R, pre, post, ruta, IND, EXTRA, DIMS):
    L = ["# Reporte estadístico final SIVAC (n = 14, pretest–postest)", "",
         f"Diseño: {R['metadatos']['diseno']}. α = {R['metadatos']['alfa']}. Regla: {R['metadatos']['regla']}.", ""]
    todos = IND + EXTRA
    L += ["## Tabla 1. Estadísticos descriptivos", ""]
    rows = []
    for v, nom, u, dm, s in todos:
        D = R["descriptivos"][v]
        for lab, k in (("Pretest", "pretest"), ("Postest", "postest"), ("Diferencia", "diferencia")):
            d = D[k]
            rows.append([nom if k == "pretest" else "", lab, f(d["media"]), f(d["de"]), f(d["mediana"]), f(d["iqr"]),
                         f(d["min"]), f(d["max"]), f(d["asimetria"]), f(d["curtosis"])])
    L += tabla(["Indicador", "Momento", "Media", "DE", "Mediana", "RIC", "Mín", "Máx", "Asimetría", "Curtosis"], rows)
    rows = [[R["descriptivos"][v]["nombre"], R["descriptivos"][v]["unidad"], f(R["descriptivos"][v]["cambio_pct"], 1) + "%"] for v, *_ in todos]
    L += ["## Tabla 2. Cambio porcentual de la media", ""] + tabla(["Indicador", "Unidad", "Cambio %"], rows)
    L += ["## Tabla 3. Niveles de satisfacción TAM (baremo: Bajo 8–18, Medio 19–29, Alto 30–40)", ""]
    rows = [[n, R["niveles_satisfaccion"]["pretest"][n]["f"], f(R["niveles_satisfaccion"]["pretest"][n]["pct"]) + "%",
             R["niveles_satisfaccion"]["postest"][n]["f"], f(R["niveles_satisfaccion"]["postest"][n]["pct"]) + "%"] for n in ("Bajo", "Medio", "Alto")]
    L += tabla(["Nivel", "f pre", "% pre", "f post", "% post"], rows)
    L += ["## Tabla 4. Frecuencias y porcentajes por ítem Likert (1–5)", ""]
    rows = []
    for it, o in R["items_likert"].items():
        for lab in ("pretest", "postest"):
            fr = o[lab]["frecuencias"]; pc = o[lab]["porcentajes"]
            rows.append([it.upper().replace("_", "-"), lab] + [f"{fr[str(k)]} ({pc[str(k)]:.1f}%)" for k in range(1, 6)] + [f(o[lab]["media"]), f(o[lab]["de"])])
    L += tabla(["Ítem", "Momento", "1", "2", "3", "4", "5", "Media", "DE"], rows)
    L += ["## Tabla 5. Confiabilidad (alfa de Cronbach)", ""]
    rows = []
    for lab, o in R["confiabilidad"].items():
        for k, c in o.items():
            rows.append([lab, k, c["k"], c["n"], f(c["alfa"], 3), f"[{c['ic95'][0]:.3f}; {c['ic95'][1]:.3f}]"])
    L += tabla(["Muestra", "Escala", "k", "n", "α", "IC 95%"], rows)
    L += ["## Tabla 6. Normalidad Shapiro–Wilk (n = 14 ≤ 50)", ""]
    rows = []
    for v, nom, *_ in todos:
        N = R["normalidad_shapiro_wilk"][v]
        for lab, k in (("Pretest", "pretest"), ("Postest", "postest"), ("Diferencia", "diferencia")):
            s = N[k]; rows.append([nom if k == "pretest" else "", lab, f(s["W"], 3), s["gl"], pf(s["p"]), "Normal" if s["normal"] else "No normal"])
    L += tabla(["Indicador", "Variable", "W", "gl", "p", "Decisión"], rows)
    L += ["Normalidad por ítem Likert (diferencias Post–Pre):", ""]
    rows = []
    for it, o in R["items_likert"].items():
        s = o["shapiro_diferencias"]
        rows.append([it.upper().replace("_", "-"), f(s["W"], 3), s["gl"], pf(s["p"]), "Normal" if s["normal"] else "No normal"] if s else [it, "—", "14", "—", "sin variabilidad"])
    L += tabla(["Ítem", "W", "gl", "p", "Decisión"], rows)
    L += ["## Tabla 7. Contraste de hipótesis por indicador (prueba adoptada según normalidad de las diferencias)", ""]
    rows = []
    for v, nom, *_ in todos:
        c = R["contrastes"][v]; t = c["t_student"]; w = c["wilcoxon"]
        rows.append([nom, c["prueba_adoptada"], f(t["dif_media"]), f"[{t['ic95'][0]:.2f}; {t['ic95'][1]:.2f}]",
                     f"t({t['gl']}) = {t['t']:.2f}" if "Student" in c["prueba_adoptada"] else f"Z = {w['Z']:.2f}",
                     pf(c["p_adoptado"]), pf(c["p_holm"]) if "p_holm" in c else "—",
                     f"{c['tipo_efecto'].split()[0]} = {c['efecto']:.2f} ({c['magnitud_efecto']})",
                     "Rechaza H0" if c["rechaza_H0"] else "No rechaza"])
    L += tabla(["Indicador", "Prueba", "Dif. media", "IC 95%", "Estadístico", "p", "p Holm", "Tamaño de efecto", "Decisión"], rows)
    L += ["## Tabla 8. Pruebas complementarias por indicador (sensibilidad)", ""]
    rows = []
    for v, nom, *_ in todos:
        c = R["contrastes"][v]; t = c["t_student"]; w = c["wilcoxon"]
        rows.append([nom, f"t({t['gl']}) = {t['t']:.2f}", pf(t["p"]), f(t["dz"]), f(t["g_hedges"]),
                     f"W+ = {w['W_pos']:.1f}; W− = {w['W_neg']:.1f}", f(w["Z"], 3), pf(w["p_asintotica"]),
                     pf(w["p_exacta"]) if w["p_exacta"] is not None else "—", f(w["r_rosenthal"]),
                     f"{w['hodges_lehmann']:.2f} [{w['ic95_hl'][0]:.2f}; {w['ic95_hl'][1]:.2f}]"])
    L += tabla(["Indicador", "t", "p", "dz", "g Hedges", "Rangos", "Z", "p asint.", "p exacta", "r", "HL [IC95%]"], rows)
    L += ["## Tabla 9. Wilcoxon por ítem Likert (Post–Pre)", ""]
    rows = []
    for it, o in R["items_likert"].items():
        w = o["wilcoxon"]
        rows.append([it.upper().replace("_", "-"), f"{w['n_neg']}/{w['n_pos']}/{w['n_emp']}", f(w["Z"], 3), pf(w["p_asintotica"]), f(w["r_rosenthal"]),
                     f"{w['hodges_lehmann']:.2f} [{w['ic95_hl'][0]:.2f}; {w['ic95_hl'][1]:.2f}]"])
    L += tabla(["Ítem", "Neg/Pos/Emp", "Z", "p asintótica", "r", "HL [IC95%]"], rows)
    L += ["## Tabla 10. Índices compuestos z por dimensión y general (hipótesis específicas y general)", "", R["compuestos_nota"], ""]
    rows = []
    for k, c in R["compuestos"].items():
        t = c["t_student"]
        rows.append([DIMS.get(k, "General"), f(c["pre"]["media"]), f(c["post"]["media"]), f"W = {c['shapiro_diferencias']['W']:.3f}; p = {pf(c['shapiro_diferencias']['p'])}",
                     c["prueba_adoptada"], f"t({t['gl']}) = {t['t']:.2f}", pf(c["p_adoptado"]), f"[{t['ic95'][0]:.2f}; {t['ic95'][1]:.2f}]",
                     f"{f(c['efecto'])} ({c['magnitud_efecto']})", "Rechaza H0" if c["rechaza_H0"] else "No rechaza"])
    L += tabla(["Dimensión", "Media pre", "Media post", "Shapiro-Wilk dif.", "Prueba", "Estadístico", "p", "IC 95% dif.", "dz", "Decisión"], rows)
    L += ["## Decisión sobre hipótesis", ""]
    for k, h in R["hipotesis"].items():
        L.append(f"- **{k}**: {h['decision']}" + (f" ({h['dimension']})" if "dimension" in h else ""))
    L += ["", "Fórmulas: t = d̄ / (s_d/√n), gl = n−1; dz = d̄/s_d; Z = (W+ − μ)/σ con μ = n(n+1)/4, σ² = n(n+1)(2n+1)/24 − Σ(t³−t)/48; r = |Z|/√n; Holm: p(i)·(m−i+1) con monotonía, m = 6."]
    ruta.write_text("\n".join(L), encoding="utf-8")
