# -*- coding: utf-8 -*-
"""Figuras 300 DPI replicando el estilo SPSS 3D del modelo Fany (2024): barras con tapa y lateral,
cuadro blanco con el porcentaje en el centro de la barra, eje 'Porcentaje', rejilla gris, fondo blanco."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

TEAL, BLUE, RED, GREEN, ORANGE, LBLUE = "#00B09B", "#1090E8", "#E8434B", "#5CC535", "#D2512F", "#5B9BE8"
SHADE = {TEAL: ("#007A6C", "#006E60"), BLUE: ("#0B63A8", "#0A5A99"), RED: ("#9E2A30", "#8E2429"),
         GREEN: ("#3A8A1F", "#337C1B"), ORANGE: ("#8F3A20", "#7F331C"), LBLUE: ("#3B6FB0", "#33629E")}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})


def barras3d(ax, x, h, col, w=0.7, dx=0.12, dy=None, ymax=1, etiqueta=None, fs=8):
    dy = dy if dy is not None else ymax*0.04
    top, side = SHADE[col]
    ax.add_patch(Rectangle((x-w/2, 0), w, h, fc=col, ec="none", zorder=3))
    ax.add_patch(Polygon([(x-w/2, h), (x-w/2+dx, h+dy), (x+w/2+dx, h+dy), (x+w/2, h)], fc=top, ec="none", zorder=3))
    ax.add_patch(Polygon([(x+w/2, 0), (x+w/2+dx, dy), (x+w/2+dx, h+dy), (x+w/2, h)], fc=side, ec="none", zorder=3))
    if etiqueta:
        ax.text(x, h/2 if h > ymax*0.08 else h+dy+ymax*0.03, etiqueta, ha="center", va="center", fontsize=fs, zorder=5,
                bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="#555555", lw=0.6))


def marco(ax, cats, ymax, ylabel="Porcentaje", titulo=None, paso=None):
    ax.set_xlim(-0.7, len(cats)-0.2); ax.set_ylim(0, ymax*1.08)
    ax.set_xticks(range(len(cats))); ax.set_xticklabels(cats)
    if paso: ax.set_yticks(np.arange(0, ymax*1.05, paso))
    ax.set_ylabel(ylabel, fontweight="bold", fontsize=9)
    ax.grid(axis="y", color="#CCCCCC", lw=0.8, zorder=0)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color("#666666")
    ax.tick_params(length=0)
    if titulo: ax.set_title(titulo, fontweight="bold", fontsize=10, pad=10)


def guardar(fig, ruta):
    fig.savefig(ruta, dpi=300, facecolor="white", bbox_inches="tight"); plt.close(fig); print("[FIGURA]", ruta.name)


def fig_niveles(R, lab, ruta, titulo):
    d = R["niveles_satisfaccion"][lab]; cats = ["Bajo", "Medio", "Alto"]
    fig, ax = plt.subplots(figsize=(6.4, 4.0)); marco(ax, cats, 100, paso=20, titulo=titulo)
    for i, (c, col) in enumerate(zip(cats, (TEAL, LBLUE, ORANGE) if lab == "pretest" else (GREEN, RED, BLUE))):
        barras3d(ax, i, d[c]["pct"], col, ymax=100, etiqueta=f'{d[c]["pct"]:.2f}%' if d[c]["f"] else None)
        if not d[c]["f"]: ax.text(i, 3, "0.00%", ha="center", fontsize=8, bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="#555", lw=.6), zorder=5)
    guardar(fig, ruta)


def fig_pares(pre, post, vars_, nombres, ylabel, ymax, ruta, titulo, fmt="{:.2f}", paso=None, sufijo=""):
    fig, ax = plt.subplots(figsize=(7.2, 4.2)); n = len(vars_)
    marco(ax, nombres, ymax, ylabel=ylabel, titulo=titulo, paso=paso)
    w = 0.34
    for i, v in enumerate(vars_):
        for k, (df, col) in enumerate(((pre, TEAL), (post, BLUE))):
            m = df[v].mean(); ic = 2.160369*df[v].std(ddof=1)/np.sqrt(len(df))  # t(.975,13)
            x = i+(-w/2-0.02 if k == 0 else w/2+0.02)
            barras3d(ax, x, m, col, w=w, dx=0.06, ymax=ymax, etiqueta=fmt.format(m)+sufijo, fs=7.5)
            ax.errorbar(x, m, yerr=ic, color="black", capsize=3, lw=0.9, zorder=6)
    ax.legend(handles=[Rectangle((0, 0), 1, 1, fc=TEAL), Rectangle((0, 0), 1, 1, fc=BLUE)],
              labels=["Pretest (proceso manual)", "Postest (con SIVAC)"], frameon=False, loc="upper right", fontsize=8)
    ax.text(0.01, -0.16, "Barras de error: IC 95% de la media (t13 = 2.160).", transform=ax.transAxes, fontsize=7, style="italic")
    guardar(fig, ruta)


def fig_box(pre, post, ruta):
    fig, axs = plt.subplots(1, 2, figsize=(8, 4.2))
    for ax, v, t, ym in zip(axs, ("t_reg", "t_vale"), ("Tiempo de registro (T_reg)", "Tiempo de emisión de vale (T_vale)"), (50, 30)):
        bp = ax.boxplot([pre[v], post[v]], patch_artist=True, widths=.5, medianprops=dict(color="black", lw=1.4),
                        tick_labels=["Pretest", "Postest"])
        for b, c in zip(bp["boxes"], (TEAL, BLUE)): b.set_facecolor(c)
        ax.set_title(t, fontweight="bold", fontsize=9.5); ax.set_ylabel("Minutos"); ax.set_ylim(0, ym)
        ax.grid(axis="y", color="#CCCCCC"); [ax.spines[s].set_visible(False) for s in ("top", "right")]
    guardar(fig, ruta)


def fig_likert(R, ruta):
    from matplotlib.colors import to_rgb
    its = list(R["items_likert"].keys()); cols = ["#D2512F", "#F2A07B", "#D9D9D9", "#8EC9F2", "#1090E8"]
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.4), sharey=True)
    for ax, lab, t in zip(axs, ("pretest", "postest"), ("Pretest (proceso manual)", "Postest (con SIVAC)")):
        left = np.zeros(len(its))
        for k in range(1, 6):
            p = np.array([R["items_likert"][i][lab]["porcentajes"][str(k)] for i in its])
            ax.barh(range(len(its)), p, left=left, color=cols[k-1], edgecolor="white", label=str(k), zorder=3)
            for j, (a, b) in enumerate(zip(left, p)):
                if b >= 7: ax.text(a+b/2, j, f"{b:.1f}", ha="center", va="center", fontsize=7, zorder=5)
            left += p
        ax.set_yticks(range(len(its))); ax.set_yticklabels([i.upper().replace("_", "-") for i in its]); ax.invert_yaxis()
        ax.set_xlim(0, 100); ax.set_xlabel("Porcentaje"); ax.set_title(t, fontweight="bold", fontsize=10)
        [ax.spines[s].set_visible(False) for s in ("top", "right")]
    axs[1].legend(title="Escala Likert", ncol=5, frameon=False, loc="upper center", bbox_to_anchor=(-0.05, -0.12), fontsize=8)
    guardar(fig, ruta)


def fig_dif(pre, post, ruta):
    fig, axs = plt.subplots(2, 3, figsize=(10, 5.6))
    from scipy import stats
    for ax, (v, t) in zip(axs.ravel(), (("t_reg", "T_reg"), ("t_vale", "T_vale"), ("rsd", "RSD"), ("cpe", "CPE"), ("score_ap", "AP"), ("score_up", "UP"))):
        d = np.sort((post[v]-pre[v]).values); q = stats.norm.ppf((np.arange(1, 15)-0.375)/(14+0.25))
        ax.scatter(q, d, color=BLUE, s=22, zorder=3)
        b, a = np.polyfit(q, d, 1); ax.plot(q, a+b*q, color=RED, lw=1)
        ax.set_title(f"Q-Q de diferencias: {t}", fontsize=9, fontweight="bold"); ax.set_xlabel("Cuantil normal teórico", fontsize=8); ax.set_ylabel("Diferencia (Post-Pre)", fontsize=8)
        ax.grid(color="#DDDDDD")
    fig.tight_layout(); guardar(fig, ruta)


def generar(R, pre, post, out, IND, DIMS):
    fig_niveles(R, "pretest", out/"fig_e01_niveles_satisfaccion_pretest_300dpi.png", "Nivel de satisfacción TAM antes del SIVAC")
    fig_niveles(R, "postest", out/"fig_e02_niveles_satisfaccion_postest_300dpi.png", "Nivel de satisfacción TAM con el SIVAC")
    fig_pares(pre, post, ["t_reg", "t_vale"], ["T_reg (registro)", "T_vale (vale de salida)"], "Minutos", 45, out/"fig_e03_tiempos_medias_300dpi.png", "Oportunidad: tiempos medios por operación", paso=10)
    fig_pares(pre, post, ["rsd", "cpe"], ["RSD", "CPE"], "Porcentaje", 100, out/"fig_e04_consistencia_medias_300dpi.png", "Consistencia documental", fmt="{:.2f}", sufijo="%", paso=20)
    fig_pares(pre, post, ["score_ap", "score_up", "score_tam_total"], ["Aceptación (AP, 4-20)", "Utilidad (UP, 4-20)", "Global TAM (8-40)"], "Puntaje", 40, out/"fig_e05_satisfaccion_tam_medias_300dpi.png", "Satisfacción del usuario (modelo TAM)", paso=10)
    fig_box(pre, post, out/"fig_e06_tiempos_boxplot_300dpi.png")
    fig_likert(R, out/"fig_e07_likert_items_300dpi.png")
    fig_dif(pre, post, out/"fig_e08_qq_diferencias_300dpi.png")
