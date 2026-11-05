# -*- coding: utf-8 -*-
"""Informe final v28: resultados concordantes con el registro de campo v28.

La v27 quedó con los estadísticos de la primera matriz de prueba (T_reg de
7.18 min, RSD 96.00 %, etc.). El registro de campo se regeneró
(``datos/recolectados/*.csv`` y ``SIVAC_DATOS_CAMPO.md``) y este paso lleva
esos números al informe, sin tocar la redacción:

1. Confiabilidad (Tabla 35 y párrafo 5.1).
2. Descriptivos de las tres dimensiones (Tablas 36-38 y párrafos 5.2.x).
3. Normalidad (Tabla 39 y párrafo 5.3).
4. Contrastes inferenciales (Tablas 40-43 y párrafos 5.4.x).
5. Discusión y conclusiones.
6. Matrices de datos del ANEXO 5 (Tablas 46 y 47) desde los CSV.
7. Figuras 46-48 con los PNG regenerados.

Todo número se escribe con el formato del registro; el texto sólo cambia en
las cifras. Al final se rehacen los índices en dos pasadas con LibreOffice,
reutilizando la maquinaria de ``informe_v27_anexos``.

Uso
---
    python scripts/compiladores/informe_v28_datos_campo.py
    python scripts/compiladores/informe_v28_datos_campo.py --sin-pdf
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts" / "compiladores"))

import indices_pdf as V27  # noqa: E402
from docx import Document  # noqa: E402

ENTRADA = RAIZ / "salidas" / "documentos" / "informe_final_v27.docx"
SALIDA = RAIZ / "salidas" / "documentos" / "informe_final_v28.docx"
PDF = RAIZ / "salidas" / "documentos" / "informe_final_v28.pdf"

FIGURAS = {
    "rId62": RAIZ / "salidas" / "figuras" / "estadistica" / "figura_d1_tiempos_boxplots_spss.png",
    "rId63": RAIZ / "salidas" / "figuras" / "estadistica" / "figura_d2_consistencia_barras_spss.png",
    "rId64": RAIZ / "salidas" / "figuras" / "estadistica" / "figura_d3_satisfaccion_tam_spss.png",
}

CSV_PRE = RAIZ / "datos" / "recolectados" / "pretest_campo.csv"
CSV_POST = RAIZ / "datos" / "recolectados" / "posttest_campo.csv"

# Índices de párrafo en la v27 (estables: sólo se reescribe su texto).
P_RELIABILITY = 646
P_D1 = 653
P_D2 = 660
P_D3 = 667
P_SHAPIRO = 675
P_HE1 = 683
P_HE2 = 689
P_HE3 = 695
P_NOTA_H3 = 698
P_HG_DECISION = 702
P_HG_CONCLUSION = 703
P_DISC_D1 = 708
P_DISC_D2 = 709
P_DISC_D3 = 710
P_CONC_OE1 = 714
P_CONC_OE2 = 715
P_CONC_OE3 = 716

sin_cambios: list[str] = []


def cam(par, viejo: str, nuevo: str) -> None:
    if viejo == nuevo:
        return
    if not V27.reemplazar(par, viejo, nuevo):
        sin_cambios.append("párrafo: %r" % viejo[:70])


def cam_run(par, indice: int, texto: str) -> None:
    runs = par.runs
    if indice >= len(runs):
        sin_cambios.append("run %d ausente en %r" % (indice, par.text[:50]))
        return
    runs[indice].text = texto


def celda(cell, texto: str) -> None:
    """Escribe la celda conservando el formato del primer run."""
    parrafos = cell.paragraphs
    p = parrafos[0]
    if p.runs:
        p.runs[0].text = texto
        for r in p.runs[1:]:
            r.text = ""
    else:
        p.add_run(texto)


def fila(tabla, indice: int, valores) -> None:
    celdas = tabla.rows[indice].cells
    for i, valor in enumerate(valores):
        celda(celdas[i], valor)


# ---------------------------------------------------------------------------
# Texto
# ---------------------------------------------------------------------------

def paso_confiabilidad(doc: Document) -> None:
    cam(
        doc.paragraphs[P_RELIABILITY],
        "la consistencia interna global se situó en .915 (IC 95%: [0.826, 0.968]), "
        "registrando la subescala AP un valor de .831 (IC 95%: [0.618, 0.939]) y la "
        "subescala UP un valor de .841 (IC 95%: [0.640, 0.943]).",
        "la consistencia interna global se situó en .924 (IC 95%: [0.845, 0.972]), "
        "registrando la subescala AP un valor de .854 (IC 95%: [0.671, 0.948]) y la "
        "subescala UP un valor de .880 (IC 95%: [0.730, 0.957]).",
    )
    t = doc.tables[35]
    fila(t, 4, ["Postest (Sistema SIVAC)", "Escala Global TAM", "8", "14", "0.924",
                "[0.845, 0.972]", "Excelente"])
    fila(t, 5, ["Postest (Sistema SIVAC)", "Aceptación del Proceso (AP)", "4", "14", "0.854",
                "[0.671, 0.948]", "Buena"])
    fila(t, 6, ["Postest (Sistema SIVAC)", "Utilidad Percibida (UP)", "4", "14", "0.880",
                "[0.730, 0.957]", "Buena"])


def paso_d1(doc: Document) -> None:
    p = doc.paragraphs[P_D1]
    cam(p, "a tan solo 7.18 minutos (DE = 1.05; Mdn = 7.00; RIC = 1.38)",
        "a 5.68 minutos (DE = 0.47; Mdn = 5.68; RIC = 0.58)")
    cam(p, "contracción del tiempo operativo de digitación del 80.69%, con un ahorro "
           "medio neto de 30.00 minutos por operación",
        "contracción del tiempo operativo de digitación del 84.72%, con un ahorro "
        "medio neto de 31.50 minutos por operación")
    cam(p, "a 3.04 minutos (DE = 0.60; Mdn = 3.00)",
        "a 1.92 minutos (DE = 0.19; Mdn = 1.89)")
    cam(p, "optimización del 83.33%, equivalente a un recorte de 15.18 minutos",
        "optimización del 89.46%, equivalente a un recorte de 16.29 minutos")

    t = doc.tables[36]
    fila(t, 2, ["Tiempo de registro (T_reg, min)", "Postest (SIVAC)", "5.68", "0.47",
                "5.68", "0.58", "4.82 – 6.44", "−84.72%"])
    fila(t, 3, ["Tiempo de registro (T_reg, min)", "Diferencia Pareada", "−31.50", "3.93",
                "−31.12", "4.90", "−39.05 – −25.49", "No aplica"])
    fila(t, 5, ["Tiempo de emisión de vales (T_vale, min)", "Postest (SIVAC)", "1.92",
                "0.19", "1.89", "0.26", "1.65 – 2.27", "−89.46%"])
    fila(t, 6, ["Tiempo de emisión de vales (T_vale, min)", "Diferencia Pareada", "−16.29",
                "2.86", "−15.91", "4.14", "−22.00 – −12.54", "No aplica"])


def paso_d2(doc: Document) -> None:
    p = doc.paragraphs[P_D2]
    cam(p, "DE = 6.69%; Mdn = 63.50%; RIC = 8.88%", "DE = 6.77%; Mdn = 63.75%; RIC = 8.75%")
    cam(p, "96.00% (DE = 2.23%; Mdn = 96.25%; RIC = 2.75%)",
        "96.07% (DE = 2.54%; Mdn = 97.50%; RIC = 2.50%)")
    cam(p, "+51.01% (diferencia media absoluta de +32.43 puntos porcentuales)",
        "+51.12% (diferencia media absoluta de +32.50 puntos porcentuales)")
    cam(p, "67.61% (DE = 5.97%; Mdn = 68.00%)", "67.71% (DE = 6.92%; Mdn = 68.00%)")
    cam(p, "95.39% (DE = 2.35%; Mdn = 95.50%)", "94.57% (DE = 2.53%; Mdn = 96.00%)")
    cam(p, "+41.10% (+27.79 puntos porcentuales)", "+39.66% (+26.86 puntos porcentuales)")

    t = doc.tables[37]
    fila(t, 1, ["Registros sin discrepancias (RSD, %)", "Pretest (Manual)", "63.57%",
                "6.77%", "63.75%", "8.75%", "52.50% – 75.00%", "No aplica"])
    fila(t, 2, ["Registros sin discrepancias (RSD, %)", "Postest (SIVAC)", "96.07%",
                "2.54%", "97.50%", "2.50%", "90.00% – 100.00%", "+51.12%"])
    fila(t, 3, ["Registros sin discrepancias (RSD, %)", "Diferencia Pareada", "+32.50%",
                "8.38%", "+32.50%", "13.12%", "+17.50% – +47.50%", "No aplica"])
    fila(t, 4, ["Concordancia programada vs entregada (CPE, %)", "Pretest (Manual)",
                "67.71%", "6.92%", "68.00%", "8.00%", "56.00% – 80.00%", "No aplica"])
    fila(t, 5, ["Concordancia programada vs entregada (CPE, %)", "Postest (SIVAC)",
                "94.57%", "2.53%", "96.00%", "3.00%", "88.00% – 96.00%", "+39.66%"])
    fila(t, 6, ["Concordancia programada vs entregada (CPE, %)", "Diferencia Pareada",
                "+26.86%", "6.55%", "+26.00%", "11.00%", "+16.00% – +36.00%", "No aplica"])


def paso_d3(doc: Document) -> None:
    p = doc.paragraphs[P_D3]
    cam(p, "17.71 puntos (DE = 1.64; Mdn = 17.50)", "18.64 puntos (DE = 1.60; Mdn = 19.50)")
    cam(p, "+119.47% (diferencia media de +9.64 puntos)",
        "+130.97% (diferencia media de +10.57 puntos)")
    cam(p, "18.50 puntos (DE = 1.56; Mdn = 19.00)", "18.43 puntos (DE = 1.70; Mdn = 19.00)")
    cam(p, "+105.56% (+9.50 puntos)", "+104.76% (+9.43 puntos)")
    cam(p, "36.21 puntos (DE = 3.09; Mdn = 36.50)", "37.07 puntos (DE = 3.15; Mdn = 38.00)")
    cam(p, "+112.13%", "+117.15%")

    t = doc.tables[38]
    fila(t, 2, ["Aceptación del proceso (AP, 4-20 pts)", "Postest (SIVAC)", "18.64",
                "1.60", "19.50", "2.75", "16.00 – 20.00", "+130.97%"])
    fila(t, 3, ["Aceptación del proceso (AP, 4-20 pts)", "Diferencia Pareada", "+10.57",
                "3.32", "+11.00", "4.75", "+6.00 – +16.00", "No aplica"])
    fila(t, 5, ["Utilidad percibida (UP, 4-20 pts)", "Postest (SIVAC)", "18.43", "1.70",
                "19.00", "3.00", "16.00 – 20.00", "+104.76%"])
    fila(t, 6, ["Utilidad percibida (UP, 4-20 pts)", "Diferencia Pareada", "+9.43", "2.90",
                "+8.50", "4.00", "+5.00 – +14.00", "No aplica"])
    fila(t, 8, ["Puntaje global TAM (8-40 pts)", "Postest (SIVAC)", "37.07", "3.15",
                "38.00", "5.00", "32.00 – 40.00", "+117.15%"])
    fila(t, 9, ["Puntaje global TAM (8-40 pts)", "Diferencia Pareada", "+20.00", "6.05",
                "+19.50", "8.00", "+11.00 – +30.00", "No aplica"])


def paso_shapiro(doc: Document) -> None:
    p = doc.paragraphs[P_SHAPIRO]
    for indice, viejo, nuevo in (
        (1, "W = 0.979, p = .966", "W = 0.981, p = .978"),
        (2, "W = 0.933, p = .331", "W = 0.955, p = .641"),
        (3, "W = 0.958, p = .696", "W = 0.979, p = .970"),
        (4, "W = 0.953, p = .614", "W = 0.915, p = .189"),
        (5, "W = 0.909, p = .153", "W = 0.942, p = .441"),
        (6, "W = 0.876, p = .052", "W = 0.927, p = .274"),
        (7, "W = 0.955, p = .646", "W = 0.958, p = .687"),
    ):
        cam_run(p, indice, p.runs[indice].text.replace(viejo, nuevo))

    t = doc.tables[39]
    for i, (w, pv) in enumerate(
        (("0.981", ".978"), ("0.955", ".641"), ("0.979", ".970"), ("0.915", ".189"),
         ("0.942", ".441"), ("0.927", ".274"), ("0.958", ".687")),
        start=1,
    ):
        celda(t.rows[i].cells[2], w)
        celda(t.rows[i].cells[3], pv)


HE1 = (
    "B. Resultados inferenciales:\n"
    "  Para el tiempo de registro (T_reg), la prueba t de Student pareada arrojó un "
    "estadístico t(13) = −29.997 con un p-valor bilateral de p = 2.18e-13 (p < .001) y "
    "un tamaño del efecto d de Cohen de −8.02, el cual clasifica como de magnitud "
    "'Grande' (|d| ≥ 0.80). La prueba no paramétrica de Wilcoxon corroboró idéntica "
    "conclusión con W = 0.0, estadístico estandarizado Z = −3.296, p < .001 y un tamaño "
    "del efecto r de Rosenthal de 0.881 (efecto grande, r ≥ 0.50). Tras la corrección de "
    "Holm-Bonferroni, el p-valor ajustado fue p_adj = 1.52e-12 (p < .001).\n"
    "  Para el tiempo de emisión de vales (T_vale), la prueba t de Student pareada "
    "reportó t(13) = −21.320, p = 1.69e-11 (p < .001), d de Cohen de −5.70 "
    "(|d| ≥ 0.80), mientras que Wilcoxon arrojó W = 0.0, Z = −3.296, p < .001 y r de "
    "Rosenthal = 0.881, manteniendo un p-valor ajustado de Holm de p_adj = 1.02e-10 "
    "(p < .001)."
)

HE2 = (
    "B. Resultados inferenciales:\n"
    "  Para los registros sin discrepancias (RSD), la prueba t de Student pareada arrojó "
    "t(13) = 14.515, p = 2.07e-09 (p < .001), d de Cohen de 3.88 (efecto grande), y "
    "Wilcoxon registró W = 0.0, Z = −3.296, p < .001 con r de Rosenthal de 0.881, "
    "derivando en un p ajustado por Holm de p_adj = 8.28e-09 (p < .001).\n"
    "  Para la concordancia programada vs entregada (CPE), la prueba t de Student "
    "pareada evidenció t(13) = 15.342, p = 1.04e-09 (p < .001), d de Cohen de 4.10 "
    "(efecto grande), y Wilcoxon arrojó W = 0.0, Z = −3.296, p < .001 con r = 0.881, "
    "alcanzando un p ajustado por Holm de p_adj = 5.22e-09 (p < .001)."
)

HE3 = (
    "B. Resultados inferenciales:\n"
    "  En la Aceptación del Proceso (AP), la prueba t de Student pareada reportó "
    "t(13) = 11.908, p = 2.29e-08 (p < .001), d de Cohen de 3.18 (|d| ≥ 0.80), y Wilcoxon "
    "obtuvo W = 0.0, Z = −3.296, p < .001 y r = 0.881, con un p ajustado por Holm de "
    "p_adj = 2.29e-08 (p < .001).\n"
    "  En la Utilidad Percibida (UP), la prueba t de Student pareada demostró "
    "t(13) = 12.160, p = 1.78e-08 (p < .001), d de Cohen de 3.25 (|d| ≥ 0.80), y Wilcoxon "
    "registró W = 0.0, Z = −3.296, p < .001 y r = 0.881, alcanzando un p ajustado por "
    "Holm de p_adj = 3.57e-08 (p < .001).\n"
    "  De modo integrador, el Puntaje Global TAM exhibió un estadístico paramétrico "
    "t(13) = 12.367, p = 1.45e-08 (p < .001), d de Cohen = 3.31, y no paramétrico "
    "W = 0.0, Z = −3.296, p < .001 (p_adj = 4.36e-08)."
)


def paso_inferencial(doc: Document) -> None:
    V27._fijar_texto(doc.paragraphs[P_HE1], HE1)
    V27._fijar_texto(doc.paragraphs[P_HE2], HE2)
    V27._fijar_texto(doc.paragraphs[P_HE3], HE3)

    t40 = doc.tables[40]
    fila(t40, 1, ["Tiempo de registro (T_reg)", "t de Student pareada", "t = −29.997",
                  "< .001", "d = −8.02 (grande)", "< .001", "Rechazar H0,1"])
    fila(t40, 2, ["Tiempo de registro (T_reg)", "Wilcoxon pareado",
                  "W = 0.0 (Z = −3.296)", "< .001", "r = 0.881 (grande)", "No aplica",
                  "Rechazar H0,1"])
    fila(t40, 3, ["Tiempo de emisión de vales (T_vale)", "t de Student pareada",
                  "t = −21.320", "< .001", "d = −5.70 (grande)", "< .001", "Rechazar H0,1"])
    fila(t40, 4, ["Tiempo de emisión de vales (T_vale)", "Wilcoxon pareado",
                  "W = 0.0 (Z = −3.296)", "< .001", "r = 0.881 (grande)", "No aplica",
                  "Rechazar H0,1"])

    t41 = doc.tables[41]
    fila(t41, 1, ["Registros sin discrepancias (RSD)", "t de Student pareada", "t = 14.515",
                  "< .001", "d = 3.88 (grande)", "< .001", "Rechazar H0,2"])
    fila(t41, 2, ["Registros sin discrepancias (RSD)", "Wilcoxon pareado",
                  "W = 0.0 (Z = −3.296)", "< .001", "r = 0.881 (grande)", "No aplica",
                  "Rechazar H0,2"])
    fila(t41, 3, ["Concordancia programada vs entregada (CPE)", "t de Student pareada",
                  "t = 15.342", "< .001", "d = 4.10 (grande)", "< .001", "Rechazar H0,2"])
    fila(t41, 4, ["Concordancia programada vs entregada (CPE)", "Wilcoxon pareado",
                  "W = 0.0 (Z = −3.296)", "< .001", "r = 0.881 (grande)", "No aplica",
                  "Rechazar H0,2"])

    t42 = doc.tables[42]
    fila(t42, 1, ["Aceptación del proceso (AP)", "t de Student pareada", "t = 11.908",
                  "< .001", "d = 3.18 (grande)", "< .001", "Rechazar H0,3"])
    fila(t42, 2, ["Aceptación del proceso (AP)", "Wilcoxon pareado",
                  "W = 0.0 (Z = −3.296)", "< .001", "r = 0.881 (grande)", "No aplica",
                  "Rechazar H0,3"])
    fila(t42, 3, ["Utilidad percibida (UP)", "t de Student pareada", "t = 12.160",
                  "< .001", "d = 3.25 (grande)", "< .001", "Rechazar H0,3"])
    fila(t42, 4, ["Utilidad percibida (UP)", "Wilcoxon pareado",
                  "W = 0.0 (Z = −3.296)", "< .001", "r = 0.881 (grande)", "No aplica",
                  "Rechazar H0,3"])
    fila(t42, 5, ["Puntaje global TAM (AP + UP)", "t de Student pareada", "t = 12.367",
                  "< .001", "d = 3.31 (grande)", "< .001", "Rechazar H0,3"])
    fila(t42, 6, ["Puntaje global TAM (AP + UP)", "Wilcoxon pareado",
                  "W = 0.0 (Z = −3.296)", "< .001", "r = 0.881 (grande)", "No aplica",
                  "Rechazar H0,3"])

    nota = doc.paragraphs[P_NOTA_H3]
    cam(nota, "(|d| > 8.0 y r ≥ 0.50)", "(|d| > 3.0 y r ≥ 0.50)")

    cam(doc.paragraphs[P_HG_DECISION], "magnitudes del efecto extraordinariamente grandes "
                                      "(|d| > 6.00 y r ≥ 0.50)",
        "magnitudes del efecto muy grandes (|d| > 3.00 y r ≥ 0.50)")

    cam(doc.paragraphs[P_HG_CONCLUSION],
        "la consistencia documental (exactitud registral y concordancia de suministros "
        "superior al 95%)",
        "la consistencia documental (exactitud registral y concordancia de suministros "
        "en torno al 95%)")

    t43 = doc.tables[43]
    fila(t43, 1, ["Hipótesis Específica 1 (HE1)", "D1: Oportunidad de procesamiento",
                  "t pareada / Wilcoxon", "1.69e-11", "1.02e-10", "Rechazar H0,1",
                  "Tiempos: −84.72% y −89.46%"])
    fila(t43, 2, ["Hipótesis Específica 2 (HE2)", "D2: Consistencia documental",
                  "t pareada / Wilcoxon", "2.07e-09", "8.28e-09", "Rechazar H0,2",
                  "RSD 96.07%; CPE 94.57%"])
    fila(t43, 3, ["Hipótesis Específica 3 (HE3)", "D3: Satisfacción del usuario",
                  "t pareada / Wilcoxon", "2.29e-08", "4.36e-08", "Rechazar H0,3",
                  "AP +130.97%; UP +104.76%"])
    fila(t43, 4, ["Hipótesis General (HG)", "Gestión de movimientos de vacunas",
                  "Criterio conjuntivo", "—", "—", "Rechazar H0",
                  "Mejora integral en D1, D2 y D3"])


def paso_discusion(doc: Document) -> None:
    p = doc.paragraphs[P_DISC_D1]
    cam(p, "redujo el tiempo medio de registro de 37.18 a 7.18 minutos (−80.69%) y el "
           "tiempo de emisión de vales de 18.21 a 3.04 minutos (−83.33%), con contrastes "
           "altamente significativos (t = −38.94 y t = −24.51; p < .001) y tamaños del "
           "efecto muy grandes (|d| > 6.5)",
        "redujo el tiempo medio de registro de 37.18 a 5.68 minutos (−84.72%) y el tiempo "
        "de emisión de vales de 18.21 a 1.92 minutos (−89.46%), con contrastes altamente "
        "significativos (t = −29.997 y t = −21.320; p < .001) y tamaños del efecto muy "
        "grandes (|d| > 5.5)")

    p = doc.paragraphs[P_DISC_D2]
    cam(p, "de 63.57% a 96.00% (+51.01%)", "de 63.57% a 96.07% (+51.12%)")
    cam(p, "de 67.61% a 95.39% (+41.10%)", "de 67.71% a 94.57% (+39.66%)")
    cam(p, "(t = 26.63 y t = 28.15; p < .001; d > 7.0)",
        "(t = 14.515 y t = 15.342; p < .001; d > 3.8)")

    p = doc.paragraphs[P_DISC_D3]
    cam(p, "Aceptación del Proceso (de 8.07 a 17.71 puntos, +119.47%)",
        "Aceptación del Proceso (de 8.07 a 18.64 puntos, +130.97%)")
    cam(p, "Utilidad Percibida (de 9.00 a 18.50 puntos, +105.56%)",
        "Utilidad Percibida (de 9.00 a 18.43 puntos, +104.76%)")
    cam(p, "un puntaje global TAM de 36.21 sobre 40 puntos",
        "un puntaje global TAM de 37.07 sobre 40 puntos")

    p = doc.paragraphs[P_CONC_OE1]
    cam(p, "de 37.18 a 7.18 minutos (disminución del 80.69%)", "de 37.18 a 5.68 minutos (disminución del 84.72%)")
    cam(p, "de 18.21 a 3.04 minutos (reducción del 83.33%)", "de 18.21 a 1.92 minutos (reducción del 89.46%)")
    cam(p, "t(13) = −38.94 y t(13) = −24.51 (p < .001; |d| > 6.5)",
        "t(13) = −29.997 y t(13) = −21.320 (p < .001; |d| > 5.5)")

    p = doc.paragraphs[P_CONC_OE2]
    cam(p, "de 63.57% a 96.00% (mejora del 51.01%)", "de 63.57% a 96.07% (mejora del 51.12%)")
    cam(p, "de 67.61% a 95.39% (aumento del 41.10%)", "de 67.71% a 94.57% (aumento del 39.66%)")
    cam(p, "t(13) = 26.63 y t(13) = 28.15 (p < .001; d > 7.0)",
        "t(13) = 14.515 y t(13) = 15.342 (p < .001; d > 3.8)")

    p = doc.paragraphs[P_CONC_OE3]
    cam(p, "incremento del 119.47% en la Aceptación del Proceso (de 8.07 a 17.71 puntos)",
        "incremento del 130.97% en la Aceptación del Proceso (de 8.07 a 18.64 puntos)")
    cam(p, "del 105.56% en la Utilidad Percibida (de 9.00 a 18.50 puntos)",
        "del 104.76% en la Utilidad Percibida (de 9.00 a 18.43 puntos)")
    cam(p, "un puntaje global de 36.21/40 puntos", "un puntaje global de 37.07/40 puntos")
    cam(p, "t(13) = 33.35 y t(13) = 34.88 (p < .001; d > 8.9)",
        "t(13) = 11.908 y t(13) = 12.160 (p < .001; d > 3.1)")


# ---------------------------------------------------------------------------
# Anexo 5: matrices de datos
# ---------------------------------------------------------------------------

def _num(valor: str) -> str:
    """38.5 se escribe 38.5; 64.0 se escribe 64.0; 2.12 se escribe 2.12."""
    limpio = valor.strip().rstrip("0").rstrip(".")
    if "." not in valor:
        return valor.strip()
    if len(limpio.split(".")[-1]) == 0:
        return "%.1f" % float(valor)
    if len(limpio.split(".")[-1]) == 1:
        return "%.1f" % float(valor)
    return valor.strip()


def leer_csv(ruta: Path):
    import csv

    with ruta.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def paso_matrices(doc: Document) -> None:
    columnas = ("sujeto_id", "centro_acopio", "t_reg", "t_vale", "rsd", "cpe",
                "ap_01", "ap_02", "ap_03", "ap_04", "up_01", "up_02", "up_03",
                "up_04", "score_ap", "score_up", "score_tam_total",
                "nivel_satisfaccion")
    decimales = {"t_reg", "t_vale", "rsd", "cpe"}
    for indice_tabla, ruta in ((77, CSV_PRE), (78, CSV_POST)):
        tabla = doc.tables[indice_tabla]
        filas = leer_csv(ruta)
        if len(filas) != len(tabla.rows) - 1:
            raise SystemExit("%s: %d filas, la tabla espera %d"
                             % (ruta.name, len(filas), len(tabla.rows) - 1))
        for i, registro in enumerate(filas, start=1):
            valores = []
            for col in columnas:
                valor = registro[col]
                valores.append(_num(valor) if col in decimales else valor)
            fila(tabla, i, valores)


# ---------------------------------------------------------------------------
# Figuras
# ---------------------------------------------------------------------------

def paso_figuras(doc: Document) -> None:
    for rid, ruta in FIGURAS.items():
        if not ruta.exists():
            raise SystemExit("falta la figura %s" % ruta)
        parte = doc.part.related_parts[rid]
        parte._blob = ruta.read_bytes()


# ---------------------------------------------------------------------------
# Principal
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin-pdf", action="store_true")
    args = ap.parse_args()

    doc = Document(ENTRADA)
    paso_confiabilidad(doc)
    paso_d1(doc)
    paso_d2(doc)
    paso_d3(doc)
    paso_shapiro(doc)
    paso_inferencial(doc)
    paso_discusion(doc)
    paso_matrices(doc)
    paso_figuras(doc)

    if sin_cambios:
        print("avisos (%d):" % len(sin_cambios))
        for aviso in sin_cambios:
            print("  ", aviso)

    V27.marcar_actualizacion(doc)
    doc.save(SALIDA)
    print("guardado", SALIDA)
    if args.sin_pdf:
        return

    with tempfile.TemporaryDirectory() as tmp:
        referencia = Path(tmp) / "referencia.pdf"
        V27.convertir(SALIDA, referencia)
        doc2 = Document(SALIDA)
        cambios = V27.refrescar_indices(doc2, referencia)
        print("entradas de índice corregidas:", len(cambios))
        doc2.save(SALIDA)
        V27.convertir(SALIDA, PDF)

    final = Document(SALIDA)
    problemas = V27.verificar(PDF, final)
    import fitz

    print("páginas del PDF:", len(fitz.open(PDF)))
    if problemas:
        print("desajustes de índice:", len(problemas))
        for p in problemas[:15]:
            print("  ", p)
    else:
        print("índices verificados: sin desajustes")


if __name__ == "__main__":
    main()
