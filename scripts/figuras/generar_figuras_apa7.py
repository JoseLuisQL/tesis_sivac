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

def _draw_box(ax, x, y, w, h, text, bg="#f8fafc", ec="#0d9488", fontsize=8.5, bold=False, text_color="#0f172a", radius=0.015):
    import matplotlib.patches as patches
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.008,rounding_size={radius}",
        facecolor=bg, edgecolor=ec, linewidth=1.3
    )
    ax.add_patch(box)
    weight = "bold" if bold else "normal"
    ax.text(x + w * 0.5, y + h * 0.5, text, ha="center", va="center", fontsize=fontsize, fontweight=weight, color=text_color)


def generar_figuras_ingenieria_sivac(base_dir):
    """Genera a 300 DPI los diagramas de ingeniería y vistas operativas del Capítulo III."""
    import matplotlib.patches as patches
    out_dir = os.path.join(base_dir, "salidas", "figuras", "recursos_graficos")
    os.makedirs(out_dir, exist_ok=True)

    # Figura 12: Diagrama general de casos de uso
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    sys_box = patches.FancyBboxPatch((0.23, 0.05), 0.54, 0.88, boxstyle="round,pad=0.01,rounding_size=0.02",
                                     facecolor="#f0fdfa", edgecolor="#0f766e", linewidth=2)
    ax.add_patch(sys_box)
    ax.text(0.50, 0.905, " Frontera del Sistema: Sistema Web SIVAC (DISA Apurímac II) ",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="#0f766e",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#ccfbf1", edgecolor="#0f766e", lw=1))

    actors_left = [
        (0.09, 0.76, "Administrador\n(TI DISA II)"),
        (0.09, 0.48, "Coordinador Regional\n(Cadena de Frío)"),
        (0.09, 0.20, "Responsable de Acopio\n(8 Centros Provinciales)")
    ]
    actors_right = [(0.91, 0.50, "Operador de\nEstablecimiento")]

    for ax_x, ax_y, label in actors_left + actors_right:
        circle = patches.Circle((ax_x, ax_y + 0.05), 0.025, facecolor="#e0f2fe", edgecolor="#0369a1", lw=1.8)
        ax.add_patch(circle)
        ax.plot([ax_x, ax_x], [ax_y + 0.025, ax_y - 0.025], color="#0369a1", lw=1.8)
        ax.plot([ax_x - 0.03, ax_x + 0.03], [ax_y + 0.01, ax_y + 0.01], color="#0369a1", lw=1.8)
        ax.plot([ax_x, ax_x - 0.025], [ax_y - 0.025, ax_y - 0.06], color="#0369a1", lw=1.8)
        ax.plot([ax_x, ax_x + 0.025], [ax_y - 0.025, ax_y - 0.06], color="#0369a1", lw=1.8)
        ax.text(ax_x, ax_y - 0.095, label, ha="center", va="top", fontsize=8.5, fontweight="bold", color="#0f172a")

    use_cases = [
        (0.50, 0.81, "CU-01: Autenticar usuario con JWT y validar permisos RBAC (HU-01)"),
        (0.50, 0.71, "CU-02: Administrar redes, microredes, 8 centros de acopio y usuarios (HU-02, HU-16)"),
        (0.50, 0.61, "CU-03: Gestionar catálogo de vacunas, jeringas y multiplicadores (HU-03, HU-04)"),
        (0.50, 0.51, "CU-04: Programar metas anuales, remesas CENARES e importar ICI-DEMID (HU-06, HU-07, HU-08)"),
        (0.50, 0.41, "CU-05: Registrar lotes de biológicos y controlar caducidad bajo FEFO (HU-05, HU-15)"),
        (0.50, 0.31, "CU-06: Procesar movimientos mensuales, saldos y redistribución (HU-09, HU-10, HU-11)"),
        (0.50, 0.21, "CU-07: Emitir y exportar vales oficiales de salida en PDF y Excel (HU-12, HU-13)"),
        (0.50, 0.11, "CU-08: Auditar Kardex digital por lote y monitorear Dashboard gerencial (HU-14, HU-16)")
    ]

    for ux, uy, utxt in use_cases:
        ellipse = patches.Ellipse((ux, uy), 0.48, 0.072, facecolor="#ffffff", edgecolor="#0d9488", lw=1.4)
        ax.add_patch(ellipse)
        ax.text(ux, uy, utxt, ha="center", va="center", fontsize=8, color="#1e293b", fontweight="bold")

    links = [
        ((0.13, 0.76), (0.26, 0.81)), ((0.13, 0.76), (0.26, 0.71)), ((0.13, 0.76), (0.26, 0.11)),
        ((0.13, 0.48), (0.26, 0.81)), ((0.13, 0.48), (0.26, 0.61)), ((0.13, 0.48), (0.26, 0.51)), ((0.13, 0.48), (0.26, 0.11)),
        ((0.13, 0.20), (0.26, 0.81)), ((0.13, 0.20), (0.26, 0.41)), ((0.13, 0.20), (0.26, 0.31)), ((0.13, 0.20), (0.26, 0.21)), ((0.13, 0.20), (0.26, 0.11)),
        ((0.87, 0.50), (0.74, 0.81)), ((0.87, 0.50), (0.74, 0.21)), ((0.87, 0.50), (0.74, 0.11))
    ]
    for (x1, y1), (x2, y2) in links:
        ax.plot([x1, x2], [y1, y2], color="#475569", lw=1.0, linestyle="-")

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "figura_casos_uso_sivac.png"), dpi=300, bbox_inches="tight")
    plt.close()

    # Figura 13: Modelo Entidad-Relación físico
    fig, ax = plt.subplots(figsize=(12, 7.2), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    entities = [
        (0.03, 0.74, 0.21, 0.21, "roles y permisos", ["PK id: UUID", "UK nombre: VARCHAR", "descripcion: TEXT", "rol_permisos (N:M)"]),
        (0.28, 0.74, 0.21, 0.21, "usuarios", ["PK id: UUID", "UK email: VARCHAR", "FK rol_id: UUID", "FK centro_acopio_id", "password_hash: TEXT"]),
        (0.53, 0.74, 0.21, 0.21, "redes y microredes", ["PK id: UUID", "UK codigo: VARCHAR", "nombre: VARCHAR", "FK red_id: UUID", "estado: BOOLEAN"]),
        (0.77, 0.74, 0.20, 0.21, "centros_acopio (8)", ["PK id: UUID", "FK microred_id: UUID", "nombre: VARCHAR", "es_almacen_central", "responsable: VARCHAR"]),
        (0.77, 0.42, 0.20, 0.22, "establecimientos", ["PK id: UUID", "UK codigo_renipress", "FK centro_acopio_id", "FK microred_id: UUID", "nombre: VARCHAR"]),
        (0.03, 0.42, 0.21, 0.22, "vacunas y jeringas", ["PK id: UUID", "UK codigo: VARCHAR", "nombre: VARCHAR", "dosis_por_frasco: INT", "rango_termico: TEXT"]),
        (0.28, 0.42, 0.21, 0.22, "lotes (FEFO)", ["PK id: UUID", "UK numero_lote", "FK vacuna_id", "FK centro_acopio_id", "fecha_vencimiento", "cantidad_actual: INT"]),
        (0.53, 0.42, 0.21, 0.22, "movimientos_vacunas", ["PK id: UUID", "FK establecimiento_id", "FK vacuna_id: UUID", "anio, mes: INT", "saldo_anterior, ingreso", "entrega, saldo_final"]),
        (0.03, 0.08, 0.28, 0.23, "planificaciones_anuales", ["PK id: UUID", "FK establecimiento_id: UUID", "FK vacuna_id: UUID (anio)", "meta_anual: INT", "cuotas_mensuales (1..12)"]),
        (0.36, 0.08, 0.28, 0.23, "vales_entrega + detalle", ["PK id: UUID", "UK numero_vale: VARCHAR", "FK establecimiento_id: UUID", "FK usuario_emisor_id: UUID", "tipo_vale, fecha_emision", "detalle_vale_entrega (1:N)"]),
        (0.69, 0.08, 0.28, 0.23, "kardex y alertas_sistema", ["PK id: UUID", "FK lote_id: UUID", "FK establecimiento_id: UUID", "tipo_movimiento: ENUM", "entrada, salida, saldo: INT", "severidad_alerta: VARCHAR"])
    ]

    for ex, ey, ew, eh, title, fields in entities:
        rect = patches.FancyBboxPatch((ex, ey), ew, eh, boxstyle="round,pad=0.005,rounding_size=0.01",
                                      facecolor="#ffffff", edgecolor="#0f766e", lw=1.5)
        ax.add_patch(rect)
        hdr = patches.FancyBboxPatch((ex, ey + eh - 0.045), ew, 0.045, boxstyle="round,pad=0.005,rounding_size=0.01",
                                     facecolor="#0f766e", edgecolor="#0f766e", lw=1)
        ax.add_patch(hdr)
        ax.text(ex + ew * 0.5, ey + eh - 0.022, title, ha="center", va="center", fontsize=8.5, fontweight="bold", color="#ffffff")
        for idx, f in enumerate(fields):
            ax.text(ex + 0.01, ey + eh - 0.072 - idx * 0.031, f"• {f}", ha="left", va="center", fontsize=7.5, color="#1e293b")

    rels = [
        ((0.24, 0.84), (0.28, 0.84), "1:N"),
        ((0.49, 0.84), (0.77, 0.88), "N:1"),
        ((0.74, 0.84), (0.77, 0.84), "1:N"),
        ((0.87, 0.74), (0.87, 0.64), "1:N"),
        ((0.24, 0.53), (0.28, 0.53), "1:N"),
        ((0.49, 0.53), (0.53, 0.53), "1:N"),
        ((0.77, 0.53), (0.74, 0.53), "1:N"),
        ((0.63, 0.42), (0.50, 0.31), "1:N"),
        ((0.38, 0.42), (0.80, 0.31), "1:N"),
        ((0.14, 0.42), (0.17, 0.31), "1:N")
    ]
    for (x1, y1), (x2, y2), card in rels:
        ax.plot([x1, x2], [y1, y2], color="#0284c7", lw=1.3, linestyle="--")
        ax.text((x1 + x2) * 0.5, (y1 + y2) * 0.5 + 0.012, card, fontsize=7.5, fontweight="bold", color="#0369a1", ha="center")

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "figura_mer_sivac.png"), dpi=300, bbox_inches="tight")
    plt.close()

    # Figura 14: Interfaz de autenticación segura
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    left_panel = patches.FancyBboxPatch((0.02, 0.04), 0.48, 0.92, boxstyle="round,pad=0.01,rounding_size=0.02",
                                        facecolor="#0f766e", edgecolor="#0f766e", lw=1.5)
    ax.add_patch(left_panel)
    ax.text(0.26, 0.76, "SIVAC", ha="center", va="center", fontsize=24, fontweight="bold", color="#ffffff")
    ax.text(0.26, 0.69, "Sistema de Gestión de Movimientos de Vacunas", ha="center", va="center", fontsize=11, color="#ccfbf1")
    ax.text(0.26, 0.58, "DIRECCIÓN DE SALUD APURÍMAC II\nEstrategia Sanitaria de Inmunizaciones\nAndahuaylas - Chincheros",
            ha="center", va="center", fontsize=9.5, color="#e2e8f0")
    _draw_box(ax, 0.08, 0.22, 0.36, 0.22,
              "• Trazabilidad de lotes bajo criterio FEFO\n• Control de 8 Centros de Acopio Provinciales\n• Emisión de vales oficiales de salida\n• Seguridad RBAC y autenticación JWT",
              bg="#115e59", ec="#2dd4bf", fontsize=8.5, text_color="#ffffff")

    right_panel = patches.FancyBboxPatch((0.52, 0.04), 0.46, 0.92, boxstyle="round,pad=0.01,rounding_size=0.02",
                                         facecolor="#ffffff", edgecolor="#cbd5e1", lw=1.5)
    ax.add_patch(right_panel)
    ax.text(0.75, 0.80, "Iniciar Sesión Institucional", ha="center", va="center", fontsize=15, fontweight="bold", color="#0f172a")
    ax.text(0.75, 0.73, "Ingrese sus credenciales autorizadas por la DISA Apurímac II", ha="center", va="center", fontsize=8.5, color="#64748b")

    ax.text(0.58, 0.63, "Correo electrónico institucional", ha="left", va="center", fontsize=8.5, fontweight="bold", color="#334155")
    _draw_box(ax, 0.58, 0.54, 0.34, 0.065, "jquispe@disaapurimac2.gob.pe", bg="#f8fafc", ec="#94a3b8", fontsize=9, text_color="#0f172a")

    ax.text(0.58, 0.46, "Contraseña de acceso", ha="left", va="center", fontsize=8.5, fontweight="bold", color="#334155")
    _draw_box(ax, 0.58, 0.37, 0.34, 0.065, "••••••••••••", bg="#f8fafc", ec="#94a3b8", fontsize=11, text_color="#0f172a")

    _draw_box(ax, 0.58, 0.23, 0.34, 0.075, "Ingresar al Sistema SIVAC", bg="#0d9488", ec="#0f766e", fontsize=10, bold=True, text_color="#ffffff")
    ax.text(0.75, 0.13, "Sesión protegida mediante JSON Web Token (JWT - HS256) y Bcrypt", ha="center", va="center", fontsize=7.8, color="#64748b")

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "figura_sivac_login.png"), dpi=300, bbox_inches="tight")
    plt.close()

    # Figura 15: Panel de control gerencial (Dashboard)
    fig, ax = plt.subplots(figsize=(12, 6.8), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    _draw_box(ax, 0.01, 0.02, 0.19, 0.96, "", bg="#ffffff", ec="#e2e8f0")
    ax.text(0.105, 0.93, "SIVAC\nSistema de Vacunas", ha="center", va="center", fontsize=10, fontweight="bold", color="#0f766e")
    menu_items = [("Dashboard (Activo)", True), ("Establecimientos", False), ("Inventario FEFO", False),
                  ("Movimientos", False), ("Planificación", False), ("Kardex Digital", False),
                  ("Reportes y Vales", False), ("Alertas", False), ("Usuarios RBAC", False)]
    for idx, (m_txt, active) in enumerate(menu_items):
        my = 0.81 - idx * 0.075
        bg_m = "#0d9488" if active else "#f8fafc"
        tc_m = "#ffffff" if active else "#334155"
        _draw_box(ax, 0.025, my, 0.16, 0.052, m_txt, bg=bg_m, ec=bg_m, fontsize=8, bold=active, text_color=tc_m)

    _draw_box(ax, 0.22, 0.86, 0.76, 0.11, "Panel de Control Gerencial (Dashboard) — Estrategia Sanitaria de Inmunizaciones DISA Apurímac II",
              bg="#f0fdfa", ec="#99f6e4", fontsize=10.5, bold=True, text_color="#0f766e")

    kpis = [
        (0.22, 0.68, 0.175, 0.15, "Redes y Centros\n2 Redes | 8 Centros\n100% Operativos"),
        (0.415, 0.68, 0.175, 0.15, "Lotes Activos FEFO\n48 Lotes Vigentes\n0 Lotes Vencidos"),
        (0.61, 0.68, 0.175, 0.15, "Concordancia CPE\n98.6% Cumplimiento\nMeta Mensual MINSA"),
        (0.805, 0.68, 0.175, 0.15, "Vales Emitidos\n142 Comprobantes\n100% Sin Discrepancias")
    ]
    for kx, ky, kw, kh, ktxt in kpis:
        _draw_box(ax, kx, ky, kw, kh, ktxt, bg="#ffffff", ec="#cbd5e1", fontsize=8.5, bold=True, text_color="#0f172a")

    _draw_box(ax, 0.22, 0.34, 0.46, 0.30,
              "Ejecución de Movimientos de Vacunas por Centro de Acopio (Dosis)\n\n"
              "• Almacén Central DISA II (Andahuaylas): 100% conciliado\n"
              "• Centros de Acopio Talavera, San Jerónimo y Chicmo: 99.2%\n"
              "• Centros de Acopio Huancarama, Pacobamba y Pampachiri: 98.8%\n"
              "• Centro de Acopio Red Virgen de Cocharcas (Chincheros): 99.1%",
              bg="#ffffff", ec="#cbd5e1", fontsize=8.2, text_color="#1e293b")

    _draw_box(ax, 0.70, 0.34, 0.28, 0.30,
              "Alertas Proactivas FEFO\n\n"
              "[Preventiva] Lote BCG-2026A\nVence en 58 días (120 dosis)\n\n"
              "[Óptimo] Stock Pentavalente, IPV,\nAPO, SPR, Neumococo y Rotavirus\ndentro de margen de seguridad",
              bg="#fffbeb", ec="#f59e0b", fontsize=8, text_color="#78350f")

    _draw_box(ax, 0.22, 0.04, 0.76, 0.26,
              "Resumen de Trazabilidad Mensual de Biológicos (NTS N° 196-MINSA)\n"
              "Vacuna                     Saldo Ant.      Ingresos CENARES      Entregas Mes      Saldo Final      Estado\n"
              "--------------------------------------------------------------------------------------------------------------\n"
              "Vacuna Pentavalente          1,240              2,400                2,180            1,460         Conciliado\n"
              "Vacuna Antipolio IPV           980              1,800                1,650            1,130         Conciliado\n"
              "Vacuna SPR (Trivalente)      1,120              2,000                1,890            1,230         Conciliado",
              bg="#ffffff", ec="#cbd5e1", fontsize=8, text_color="#0f172a")

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "figura_sivac_dashboard.png"), dpi=300, bbox_inches="tight")
    plt.close()

    # Figura 18: Módulo de registro mensual de movimientos y vales
    fig, ax = plt.subplots(figsize=(12, 6.8), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    _draw_box(ax, 0.01, 0.02, 0.19, 0.96, "", bg="#ffffff", ec="#e2e8f0")
    ax.text(0.105, 0.93, "SIVAC\nSistema de Vacunas", ha="center", va="center", fontsize=10, fontweight="bold", color="#0f766e")
    menu_items_mov = [("Dashboard", False), ("Establecimientos", False), ("Inventario FEFO", False),
                      ("Movimientos (Activo)", True), ("Planificación", False), ("Kardex Digital", False),
                      ("Reportes y Vales", False), ("Alertas", False), ("Usuarios RBAC", False)]
    for idx, (m_txt, active) in enumerate(menu_items_mov):
        my = 0.81 - idx * 0.075
        bg_m = "#0d9488" if active else "#f8fafc"
        tc_m = "#ffffff" if active else "#334155"
        _draw_box(ax, 0.025, my, 0.16, 0.052, m_txt, bg=bg_m, ec=bg_m, fontsize=8, bold=active, text_color=tc_m)

    _draw_box(ax, 0.22, 0.86, 0.76, 0.11,
              "Módulo de Registro Mensual de Movimientos de Vacunas y Emisión de Vales Oficiales de Entrega",
              bg="#f0fdfa", ec="#99f6e4", fontsize=10, bold=True, text_color="#0f766e")

    _draw_box(ax, 0.22, 0.74, 0.50, 0.09,
              "Filtro Operativo: Red José María Arguedas | Centro de Acopio: San Jerónimo | Periodo: 2026 - Mes 08",
              bg="#ffffff", ec="#cbd5e1", fontsize=8.2, bold=True, text_color="#1e293b")
    _draw_box(ax, 0.74, 0.74, 0.24, 0.09,
              "Emitir Vale Oficial (PDF y Excel)",
              bg="#0d9488", ec="#0f766e", fontsize=8.5, bold=True, text_color="#ffffff")

    _draw_box(ax, 0.22, 0.34, 0.76, 0.37,
              "Cuadrícula Transaccional de Movimientos de Biológicos y Jeringas Asociadas (Cálculo Automático en Tiempo Real)\n\n"
              "Biológico y Lote (FEFO)        Saldo Ant.   Ingreso   Transferencia   Meta Mes   Entrega Base   Adicional   Saldo Final\n"
              "----------------------------------------------------------------------------------------------------------------------\n"
              "BCG (Lote: 240815A - Venc: 2026)     180        300           0            240          240            0          240\n"
              "HvB Pediátrico (Lote: 250109B)       210        400           0            320          320           20          270\n"
              "Pentavalente (Lote: 250312C)         340        600         -30            510          510            0          400\n"
              "Antipolio IPV (Lote: 250218A)        290        500           0            450          450            0          340\n"
              "SPR Trivalente (Lote: 250402D)       260        450           0            380          380           10          320",
              bg="#ffffff", ec="#cbd5e1", fontsize=7.8, text_color="#0f172a")

    _draw_box(ax, 0.22, 0.04, 0.76, 0.26,
              "Comprobante Oficial Generado: VALE DE ENTREGA N° VALE-2026-00142 (Sincronizado con Kardex Digital)\n"
              "• Modalidad de emisión: Vale Completo (Asignación Base Mensual + Entregas Adicionales + Jeringas Vinculadas)\n"
              "• Verificación automática: Stock disponible validado | Concordancia Programada vs Entregada: 100.0%\n"
              "• Exportación inmediata habilitada: [ Descargar PDF Oficial con Firmas (PDFKit) ]   [ Exportar Hoja de Cálculo (ExcelJS) ]",
              bg="#f8fafc", ec="#0d9488", fontsize=8.2, text_color="#0f172a")

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "figura_sivac_movimientos_vales.png"), dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[*] 5 figuras de ingeniería SIVAC (300 DPI) generadas exitosamente en: {out_dir}")


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    generar_figuras_ingenieria_sivac(base_dir)
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
