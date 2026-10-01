#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA WEB SIVAC — GENERADOR DE FIGURAS ESTADÍSTICAS EN FORMATO APA 7.ª EDICIÓN (300 DPI)
Proyecto de Tesis — Escuela Profesional de Ingeniería de Sistemas — UNAJMA
Autor: Analista Estadístico (analista-estadistico)
Directriz: Cero Alucinaciones, Formato Vectorial / Alta Resolución (300 DPI) para Informe Final.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Configuración global de estilos según normas APA 7.ª edición
plt.rcParams['font.sans-serif'] = 'Times New Roman'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 12

def configurar_ejes_apa(ax):
    """Aplica formato APA 7 a los ejes: elimina espinas superior y derecha."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#333333')
    ax.spines['bottom'].set_color('#333333')
    ax.yaxis.grid(True, linestyle='--', alpha=0.4, color='#888888')
    ax.xaxis.grid(False)

def generar_grafico_dimension1(df_pre, df_post, ruta_salida):
    """Figura 1: Tiempos de Procesamiento (T_reg y T_vale) - Pretest vs Postest."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300)

    # Subgráfico A: Tiempo de Registro
    ax1 = axes[0]
    data_treg = [df_pre['t_reg'], df_post['t_reg']]
    bp1 = ax1.boxplot(data_treg, patch_artist=True, labels=['Pretest\n(Manual)', 'Postest\n(SIVAC)'],
                      widths=0.45, medianprops=dict(color='black', linewidth=1.5))
    bp1['boxes'][0].set_facecolor('#d9d9d9')
    bp1['boxes'][1].set_facecolor('#708090')

    # Líneas individuales de los 14 sujetos pareados
    for i in range(len(df_pre)):
        ax1.plot([1, 2], [df_pre['t_reg'].iloc[i], df_post['t_reg'].iloc[i]],
                 color='#4682b4', alpha=0.35, linewidth=1, marker='o', markersize=3)

    configurar_ejes_apa(ax1)
    ax1.set_ylabel('Tiempo en minutos (min)')
    ax1.set_title('A. Tiempo de Registro de Movimientos ($T_{reg}$)')

    # Subgráfico B: Tiempo de Emisión de Vales
    ax2 = axes[1]
    data_tvale = [df_pre['t_vale'], df_post['t_vale']]
    bp2 = ax2.boxplot(data_tvale, patch_artist=True, labels=['Pretest\n(Manual)', 'Postest\n(SIVAC)'],
                      widths=0.45, medianprops=dict(color='black', linewidth=1.5))
    bp2['boxes'][0].set_facecolor('#d9d9d9')
    bp2['boxes'][1].set_facecolor('#708090')

    for i in range(len(df_pre)):
        ax2.plot([1, 2], [df_pre['t_vale'].iloc[i], df_post['t_vale'].iloc[i]],
                 color='#4682b4', alpha=0.35, linewidth=1, marker='o', markersize=3)

    configurar_ejes_apa(ax2)
    ax2.set_ylabel('Tiempo en minutos (min)')
    ax2.set_title('B. Tiempo de Emisión de Vales ($T_{vale}$)')

    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[*] Figura 1 generada exitosamente (300 DPI): {ruta_salida}")

def generar_grafico_dimension2(df_pre, df_post, ruta_salida):
    """Figura 2: Consistencia Documental (RSD y CPE) - Pretest vs Postest."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300)

    # Subgráfico A: % Registros sin Discrepancias
    ax1 = axes[0]
    data_rsd = [df_pre['rsd'], df_post['rsd']]
    bp1 = ax1.boxplot(data_rsd, patch_artist=True, labels=['Pretest\n(Manual)', 'Postest\n(SIVAC)'],
                      widths=0.45, medianprops=dict(color='black', linewidth=1.5))
    bp1['boxes'][0].set_facecolor('#e0e0e0')
    bp1['boxes'][1].set_facecolor('#2e8b57')

    for i in range(len(df_pre)):
        ax1.plot([1, 2], [df_pre['rsd'].iloc[i], df_post['rsd'].iloc[i]],
                 color='#2e8b57', alpha=0.35, linewidth=1, marker='o', markersize=3)

    configurar_ejes_apa(ax1)
    ax1.set_ylabel('Porcentaje de registros (%)')
    ax1.set_ylim(-5, 105)
    ax1.set_title('A. Registros sin Discrepancias ($RSD$)')

    # Subgráfico B: % Concordancia Programada vs Entregada
    ax2 = axes[1]
    data_cpe = [df_pre['cpe'], df_post['cpe']]
    bp2 = ax2.boxplot(data_cpe, patch_artist=True, labels=['Pretest\n(Manual)', 'Postest\n(SIVAC)'],
                      widths=0.45, medianprops=dict(color='black', linewidth=1.5))
    bp2['boxes'][0].set_facecolor('#e0e0e0')
    bp2['boxes'][1].set_facecolor('#2e8b57')

    for i in range(len(df_pre)):
        ax2.plot([1, 2], [df_pre['cpe'].iloc[i], df_post['cpe'].iloc[i]],
                 color='#2e8b57', alpha=0.35, linewidth=1, marker='o', markersize=3)

    configurar_ejes_apa(ax2)
    ax2.set_ylabel('Porcentaje de concordancia (%)')
    ax2.set_ylim(-5, 105)
    ax2.set_title('B. Concordancia Programada vs Entregada ($CPE$)')

    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[*] Figura 2 generada exitosamente (300 DPI): {ruta_salida}")

def generar_grafico_dimension3(df_pre, df_post, ruta_salida):
    """Figura 3: Satisfacción del Usuario (TAM) - Pretest vs Postest."""
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.5), dpi=300)

    variables_tam = [
        ('score_ap', 'A. Aceptación del Proceso (AP)', 5, 25, axes[0]),
        ('score_up', 'B. Utilidad Percibida (UP)', 5, 25, axes[1]),
        ('score_tam_total', 'C. Satisfacción Global TAM', 10, 50, axes[2])
    ]

    for col, titulo, y_min, y_max, ax in variables_tam:
        data = [df_pre[col], df_post[col]]
        bp = ax.boxplot(data, patch_artist=True, labels=['Pretest\n(Manual)', 'Postest\n(SIVAC)'],
                        widths=0.45, medianprops=dict(color='black', linewidth=1.5))
        bp['boxes'][0].set_facecolor('#dcdcdc')
        bp['boxes'][1].set_facecolor('#4682b4')

        for i in range(len(df_pre)):
            ax.plot([1, 2], [df_pre[col].iloc[i], df_post[col].iloc[i]],
                    color='#1c39bb', alpha=0.35, linewidth=1, marker='o', markersize=3)

        configurar_ejes_apa(ax)
        ax.set_ylabel('Puntaje acumulado')
        ax.set_ylim(y_min - 2, y_max + 2)
        ax.set_title(titulo)

    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[*] Figura 3 generada exitosamente (300 DPI): {ruta_salida}")

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    pretest_csv = os.path.join(base_dir, "datos", "raw", "bd_sivac_pretest.csv")
    if not os.path.exists(pretest_csv):
        pretest_csv = os.path.join(base_dir, "datos", "bd_sivac_pretest.csv")
    postest_csv = os.path.join(base_dir, "datos", "raw", "bd_sivac_postest.csv")
    if not os.path.exists(postest_csv):
        postest_csv = os.path.join(base_dir, "datos", "bd_sivac_postest.csv")
    dir_salidas = os.path.join(base_dir, "salidas", "figuras")

    if not os.path.exists(pretest_csv) or not os.path.exists(postest_csv):
        print("[!] Error: No se encontraron los archivos de datos de campo.")
        print("[!] Estado: BLOQUEADO (Esperando entrega de datos de campo por el tesista).")
        return

    os.makedirs(dir_salidas, exist_ok=True)
    df_pre = pd.read_csv(pretest_csv).sort_values('sujeto_id').reset_index(drop=True)
    df_post = pd.read_csv(postest_csv).sort_values('sujeto_id').reset_index(drop=True)

    f1 = os.path.join(dir_salidas, "figura_01_oportunidad_tiempos.png")
    f2 = os.path.join(dir_salidas, "figura_02_consistencia_documental.png")
    f3 = os.path.join(dir_salidas, "figura_03_satisfaccion_tam.png")

    generar_grafico_dimension1(df_pre, df_post, f1)
    generar_grafico_dimension2(df_pre, df_post, f2)
    generar_grafico_dimension3(df_pre, df_post, f3)
    print("[*] Proceso de generación de figuras APA 7 culminado exitosamente.")

if __name__ == '__main__':
    main()
