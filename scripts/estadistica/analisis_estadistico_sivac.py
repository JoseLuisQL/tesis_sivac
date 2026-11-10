# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB - Pipeline estadistico final (n = 14, pretest-postest, un grupo).
Entrada : datos de campo transcritos de los Instrumentos 01-03 manuscritos
          (salidas/evidencias/base_de_datos/*.csv; verificados contra los PDF).
Salidas : salidas/estadistica/{reporte_estadistico_completo.json, REPORTE_ESTADISTICO_FINAL.md}
          salidas/figuras/estadistica/*.png (300 DPI, estilo SPSS del modelo Fany 2024)
Uso     : python3 scripts/estadistica/analisis_estadistico_sivac.py
Regla de decision: n=14 <= 50 -> Shapiro-Wilk sobre las diferencias pareadas (Post-Pre);
p > .05 -> t pareada + d de Cohen (dz); p <= .05 -> Wilcoxon + r de Rosenthal.
Correccion de Holm sobre la familia de 6 indicadores primarios.
"""
import itertools, json, math, sys
from pathlib import Path
import numpy as np, pandas as pd, scipy.stats as st

RAIZ = Path(__file__).resolve().parents[2]
BD = RAIZ / "salidas" / "evidencias" / "base_de_datos"
OUT_E = RAIZ / "salidas" / "estadistica"
OUT_F = RAIZ / "salidas" / "figuras" / "estadistica"
OUT_E.mkdir(parents=True, exist_ok=True); OUT_F.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(Path(__file__).resolve().parent))

ALFA = 0.05
IND = [  # var, nombre, unidad, dimension, sentido (+1 mayor es mejor, -1 menor es mejor)
    ("t_reg", "Tiempo de registro (T_reg)", "min", "D1", -1),
    ("t_vale", "Tiempo de emision de vales (T_vale)", "min", "D1", -1),
    ("rsd", "Registros sin discrepancias (RSD)", "%", "D2", +1),
    ("cpe", "Concordancia programada vs entregada (CPE)", "%", "D2", +1),
    ("score_ap", "Aceptacion del proceso (AP)", "pts (4-20)", "D3", +1),
    ("score_up", "Utilidad percibida (UP)", "pts (4-20)", "D3", +1),
]
EXTRA = [("score_tam_total", "Puntaje global TAM (AP+UP)", "pts (8-40)", "D3", +1)]
ITEMS = [f"{a}_0{i}" for a in ("ap", "up") for i in range(1, 5)]
DIMS = {"D1": "Oportunidad", "D2": "Consistencia documental", "D3": "Satisfaccion del usuario"}


def desc(x):
    x = np.asarray(x, float); n = len(x)
    q1, q3 = np.percentile(x, [25, 75])  # metodo lineal
    sk = st.skew(x, bias=False); ku = st.kurtosis(x, bias=False)
    return dict(n=n, media=x.mean(), de=x.std(ddof=1), ee=x.std(ddof=1) / math.sqrt(n),
                mediana=float(np.median(x)), q1=q1, q3=q3, iqr=q3 - q1, min=x.min(), max=x.max(),
                asimetria=sk, ee_asimetria=math.sqrt(6*n*(n-1)/((n-2)*(n+1)*(n+3))),
                curtosis=ku)


def ee_curt(n):
    ees = math.sqrt(6*n*(n-1)/((n-2)*(n+1)*(n+3)))
    return 2*ees*math.sqrt((n**2-1)/((n-3)*(n+5)))


def desc2(x):
    d = desc(x); d["ee_curtosis"] = ee_curt(len(x)); return d


def cronbach(df):
    k = df.shape[1]; n = df.shape[0]
    a = k/(k-1)*(1-df.var(ddof=1).sum()/df.sum(axis=1).var(ddof=1))
    f = 1-a; d1, d2 = n-1, (n-1)*(k-1)
    return dict(alfa=a, k=k, n=n, ic95=[max(0, 1-f*st.f.ppf(.975, d1, d2)), min(1, 1-f*st.f.ppf(.025, d1, d2))])


def shapiro(x):
    w, p = st.shapiro(x); return dict(W=float(w), gl=len(x), p=float(p), normal=bool(p > ALFA))


def signed_rank_dist(n):
    c = np.zeros(n*(n+1)//2+1); c[0] = 1
    for r in range(1, n+1):
        c2 = c.copy(); c2[r:] += c[:-r]; c = c2
    return c / 2**n


def wilcoxon_full(diff):
    d = np.asarray(diff, float); d = d[d != 0]; n = len(d)
    ranks = st.rankdata(np.abs(d)); Wp = ranks[d > 0].sum(); Wm = ranks[d < 0].sum()
    T = min(Wp, Wm)
    _, cnt = np.unique(np.abs(d), return_counts=True)
    mu = n*(n+1)/4; var = n*(n+1)*(2*n+1)/24 - (cnt**3-cnt).sum()/48
    z = (Wp-mu)/math.sqrt(var)  # Z signo: negativo si predominan rangos negativos (Post<Pre)
    p_asin = 2*st.norm.sf(abs(z))
    exact = len(cnt) == n  # sin empates
    p_ex = float(min(1, 2*signed_rank_dist(n)[:int(T)+1].sum())) if exact else None
    # Hodges-Lehmann + IC95 (Walsh) con distribucion exacta (sin empates) o normal
    walsh = np.sort([(a+b)/2 for a, b in itertools.combinations_with_replacement(d, 2)])
    M = len(walsh)
    if exact:
        cdf = np.cumsum(signed_rank_dist(n)); k = int(np.searchsorted(cdf, ALFA/2, side="right"))  # P(W<k)<=.025
    else:
        k = int(math.floor(mu - 1.96*math.sqrt(var)))
    k = max(k, 0)
    hl = float(np.median(walsh)); ic = [float(walsh[k]), float(walsh[M-1-k])]
    return dict(n_efectivo=n, W_pos=float(Wp), W_neg=float(Wm), T=float(T), Z=float(z), p_asintotica=float(p_asin),
                p_exacta=p_ex, r_rosenthal=abs(z)/math.sqrt(n), hodges_lehmann=hl, ic95_hl=ic,
                n_neg=int((d < 0).sum()), n_pos=int((d > 0).sum()), n_emp=14-n)


def contraste(pre, post, sentido):
    pre = np.asarray(pre, float); post = np.asarray(post, float); d = post-pre; n = len(d)
    sw = shapiro(d)
    t = st.ttest_rel(post, pre); sd = d.std(ddof=1); se = sd/math.sqrt(n)
    tc = st.t.ppf(1-ALFA/2, n-1)
    p_uni = float(st.ttest_rel(post, pre, alternative="less" if sentido < 0 else "greater").pvalue)
    tt = dict(t=float(t.statistic), gl=n-1, p=float(t.pvalue), p_unilateral=p_uni, dif_media=float(d.mean()), ee=se,
              ic95=[float(d.mean()-tc*se), float(d.mean()+tc*se)], dz=float(d.mean()/sd),
              g_hedges=float(d.mean()/sd*(1-3/(4*(n-1)-1))))
    w = wilcoxon_full(d)
    w["p_unilateral_exacta"] = (w["p_exacta"]/2 if w["p_exacta"] is not None else w["p_asintotica"]/2)
    adopt = "t de Student pareada" if sw["normal"] else "Wilcoxon de rangos con signo"
    return dict(shapiro_diferencias=sw, t_student=tt, wilcoxon=w, prueba_adoptada=adopt,
                p_adoptado=tt["p"] if sw["normal"] else (w["p_exacta"] if w["p_exacta"] is not None else w["p_asintotica"]),
                efecto=(tt["dz"] if sw["normal"] else w["r_rosenthal"]),
                tipo_efecto="d de Cohen (dz)" if sw["normal"] else "r de Rosenthal")


def magnitud(v, tipo):
    v = abs(v)
    if tipo.startswith("d"): return "grande" if v >= .8 else "mediano" if v >= .5 else "pequeno" if v >= .2 else "trivial"
    return "grande" if v >= .5 else "mediano" if v >= .3 else "pequeno" if v >= .1 else "trivial"


def nivel(t): return "Bajo" if t <= 18 else "Medio" if t <= 29 else "Alto"


def main():
    m = pd.read_csv(BD/"matriz_analitica_pre_post.csv")
    pre = m[m.momento == "Pretest"].set_index("sujeto_id").sort_index()
    post = m[m.momento == "Postest"].set_index("sujeto_id").sort_index()
    assert list(pre.index) == list(post.index) and len(pre) == 14
    n = len(pre)
    # coherencia aritmetica interna
    for df in (pre, post):
        assert (df[ITEMS[:4]].sum(1) == df.score_ap).all() and (df[ITEMS[4:]].sum(1) == df.score_up).all()
        assert (df.score_ap+df.score_up == df.score_tam_total).all()
        assert (df.score_tam_total.map(nivel) == df.nivel_satisfaccion).all()

    R = dict(metadatos=dict(n=n, diseno="Preexperimental O1-X-O2, un grupo", alfa=ALFA,
                            fuente="Instrumentos 01, 02 y 03 manuscritos (datos/recolectados/*.pdf)",
                            regla="Shapiro-Wilk (n<=50) sobre diferencias; t pareada si p>.05, Wilcoxon si p<=.05; Holm sobre 6 indicadores"))
    todos = IND+EXTRA
    # descriptivos
    R["descriptivos"] = {}
    for v, nom, u, dm, s in todos:
        R["descriptivos"][v] = dict(nombre=nom, unidad=u, dimension=dm, pretest=desc2(pre[v]), postest=desc2(post[v]),
                                    diferencia=desc2(post[v]-pre[v]),
                                    cambio_pct=float((post[v].mean()-pre[v].mean())/pre[v].mean()*100))
    # items Likert
    R["items_likert"] = {}
    for it in ITEMS:
        o = {}
        for lab, df in (("pretest", pre), ("postest", post)):
            fr = df[it].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)
            o[lab] = dict(frecuencias={str(k): int(c) for k, c in fr.items()},
                          porcentajes={str(k): float(c/n*100) for k, c in fr.items()}, **{k: float(v) for k, v in desc2(df[it]).items() if k in ("media", "de", "mediana", "iqr", "min", "max")})
        dd = post[it]-pre[it]
        o["wilcoxon"] = {k: v for k, v in wilcoxon_full(dd).items()}
        o["shapiro_diferencias"] = shapiro(dd) if dd.nunique() > 1 else None
        R["items_likert"][it] = o
    # niveles
    R["niveles_satisfaccion"] = {}
    for lab, df in (("pretest", pre), ("postest", post)):
        c = df.score_tam_total.map(nivel).value_counts().reindex(["Bajo", "Medio", "Alto"], fill_value=0)
        R["niveles_satisfaccion"][lab] = {k: dict(f=int(v), pct=float(v/n*100)) for k, v in c.items()}
    # confiabilidad
    R["confiabilidad"] = {lab: dict(global_tam=cronbach(df[ITEMS]), AP=cronbach(df[ITEMS[:4]]), UP=cronbach(df[ITEMS[4:]]))
                          for lab, df in (("pretest", pre), ("postest", post), ("ambos_momentos_n28", m))}
    # normalidad
    R["normalidad_shapiro_wilk"] = {}
    for v, nom, u, dm, s in todos:
        R["normalidad_shapiro_wilk"][v] = dict(indicador=nom, pretest=shapiro(pre[v]), postest=shapiro(post[v]),
                                               diferencia=shapiro(post[v]-pre[v]))
    # contrastes
    C = {v: contraste(pre[v], post[v], s) for v, _, _, _, s in todos}
    prim = [v for v, *_ in IND]
    ps = sorted([(C[v]["p_adoptado"], v) for v in prim]); run = 0
    for rank, (p, v) in enumerate(ps):
        run = max(run, min(1, p*(len(ps)-rank))); C[v]["p_holm"] = run
    for v, nom, u, dm, s in todos:
        c = C[v]; c["indicador"] = nom; c["dimension"] = dm; c["sentido_mejora"] = "disminuir" if s < 0 else "aumentar"
        c["magnitud_efecto"] = magnitud(c["efecto"], c["tipo_efecto"])
        c["mejora_en_direccion_esperada"] = bool((post[v].mean()-pre[v].mean())*s > 0)
        ph = c.get("p_holm", c["p_adoptado"])
        c["rechaza_H0"] = bool(ph < ALFA and c["mejora_en_direccion_esperada"])
    R["contrastes"] = C
    # compuestos por dimension y general (z con SD agrupada pre+post, orientado a mejora)
    Z = {}
    for v, _, _, dm, s in IND:
        allv = np.concatenate([pre[v], post[v]]); mu, sd = allv.mean(), allv.std(ddof=1)
        Z[v] = (pd.DataFrame({"pre": (pre[v]-mu)/sd*s, "post": (post[v]-mu)/sd*s}))
    comp = {}
    for d in DIMS:
        vs = [v for v, _, _, dm, _ in IND if dm == d]
        comp[d] = (pd.DataFrame({"pre": sum(Z[v]["pre"] for v in vs)/len(vs), "post": sum(Z[v]["post"] for v in vs)/len(vs)}))
    comp["GENERAL"] = pd.DataFrame({"pre": sum(comp[d]["pre"] for d in DIMS)/3, "post": sum(comp[d]["post"] for d in DIMS)/3})
    R["compuestos"] = {}
    for k, df in comp.items():
        c = contraste(df["pre"], df["post"], +1)
        c["pre"] = desc2(df["pre"]); c["post"] = desc2(df["post"])
        c["mejora_en_direccion_esperada"] = bool(df["post"].mean() > df["pre"].mean())
        c["magnitud_efecto"] = magnitud(c["efecto"], c["tipo_efecto"])
        c["rechaza_H0"] = bool(c["p_adoptado"] < ALFA and c["mejora_en_direccion_esperada"])
        R["compuestos"][k] = c
    R["compuestos_nota"] = ("Indice z orientado a mejora (mayor = mejor): cada indicador se estandariza con media y DE de los 28 valores "
                            "pre+post y se invierte en tiempos; dimension = media de sus 2 indicadores; general = media de las 3 dimensiones.")
    # hipotesis
    H = {}
    for i, (d, vs) in enumerate({"D1": ["t_reg", "t_vale"], "D2": ["rsd", "cpe"], "D3": ["score_ap", "score_up"]}.items(), 1):
        H[f"HE{i}"] = dict(dimension=DIMS[d], compuesto=R["compuestos"][d]["rechaza_H0"],
                           indicadores={v: C[v]["rechaza_H0"] for v in vs},
                           decision="Se rechaza H0" if R["compuestos"][d]["rechaza_H0"] and all(C[v]["rechaza_H0"] for v in vs) else "No se rechaza H0")
    gen = R["compuestos"]["GENERAL"]["rechaza_H0"] and all(h["decision"] == "Se rechaza H0" for h in H.values())
    H["HG"] = dict(decision="Se rechaza H0" if gen else "No se rechaza H0", compuesto=R["compuestos"]["GENERAL"]["rechaza_H0"])
    R["hipotesis"] = H
    (OUT_E/"reporte_estadistico_completo.json").write_text(json.dumps(R, indent=2, ensure_ascii=False, default=float), encoding="utf-8")
    from reporte_md import escribir_md
    escribir_md(R, pre, post, OUT_E/"REPORTE_ESTADISTICO_FINAL.md", IND, EXTRA, DIMS)
    from figuras_spss import generar
    generar(R, pre, post, OUT_F, IND, DIMS)
    print("OK", gen)


if __name__ == "__main__":
    main()
