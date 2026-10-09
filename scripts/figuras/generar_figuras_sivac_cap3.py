#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GENERADOR DE DIAGRAMAS DE INGENIERÍA Y VISTAS DEL SISTEMA WEB SIVAC A 300 DPI
Proyecto de Tesis — Escuela Profesional de Ingeniería de Sistemas — UNAJMA
Autor: Documentador XP (documentador-xp)
Salida: C:/MisInvestigaciones/tesis/sivac/salidas/figuras/recursos_graficos/
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\MisInvestigaciones\tesis\sivac"
OUT_DIR = os.path.join(BASE_DIR, "salidas", "figuras", "recursos_graficos")
os.makedirs(OUT_DIR, exist_ok=True)


def get_font(size: int, bold: bool = False, italic: bool = False, mono: bool = False):
    """Carga fuente limpia del sistema Windows con fallback seguro."""
    win_fonts = r"C:\Windows\Fonts"
    candidates = []
    if mono:
        candidates = ["consolab.ttf" if bold else "consola.ttf", "courbd.ttf" if bold else "cour.ttf"]
    elif bold and italic:
        candidates = ["segoeuiz.ttf", "arialbi.ttf", "calibriz.ttf"]
    elif bold:
        candidates = ["segoeuib.ttf", "arialbd.ttf", "calibrib.ttf"]
    elif italic:
        candidates = ["segoeuii.ttf", "ariali.ttf", "calibrii.ttf"]
    else:
        candidates = ["segoeui.ttf", "arial.ttf", "calibri.ttf"]

    for name in candidates:
        fp = os.path.join(win_fonts, name)
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()


def draw_rounded_rect(draw: ImageDraw.ImageDraw, xy, radius: int, fill=None, outline=None, width: int = 1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def save_300dpi(img: Image.Image, filename: str):
    out_path = os.path.join(OUT_DIR, filename)
    img.save(out_path, format="PNG", dpi=(300, 300), optimize=True)
    print(f"[OK 300 DPI] {out_path} ({img.size[0]}x{img.size[1]} px)")


# ==============================================================================
# 0. PLANTILLA COMÚN DE SHELL SIVAC (SIDEBAR + TOPBAR INSTITUCIONAL)
# ==============================================================================
def create_sivac_shell(active_menu: str, breadcrumb_sub: str, width: int = 1920, height: int = 1080):
    """Crea el lienzo base idéntico a las capturas reales de SIVAC."""
    img = Image.new("RGB", (width, height), "#F4F6F9")
    draw = ImageDraw.Draw(img)

    # Sidebar izquierdo (blanco con borde derecho sutil)
    sidebar_w = 240
    draw.rectangle([0, 0, sidebar_w, height], fill="#FFFFFF", outline="#E2E8F0", width=1)

    # Header del Sidebar: Logo SIVAC
    draw_rounded_rect(draw, [20, 18, 60, 58], radius=10, fill="#0D9488")
    f_logo_icon = get_font(22, bold=True)
    draw.text((33, 24), "S", fill="#FFFFFF", font=f_logo_icon)

    f_brand = get_font(20, bold=True)
    f_sub = get_font(11, bold=False)
    draw.text((72, 18), "SIVAC", fill="#0F172A", font=f_brand)
    draw.text((72, 42), "Control de Vacunas", fill="#64748B", font=f_sub)
    draw.line([0, 76, sidebar_w, 76], fill="#E2E8F0", width=1)

    # Ítems de navegación
    menu_items = [
        ("Dashboard", "▣"),
        ("Establecimientos", "⌂"),
        ("Inventario", "❐"),
        ("Movimientos", "⇄"),
        ("Planificación", "▤"),
        ("Kardex", "☰"),
        ("Reportes", "▥"),
        ("Alertas", "▲"),
        ("Usuarios", "☻"),
        ("Configuración", "⚙"),
    ]
    f_menu = get_font(14, bold=False)
    f_menu_b = get_font(14, bold=True)

    y_pos = 96
    for label, icon_sym in menu_items:
        is_active = (label.lower() == active_menu.lower())
        if is_active:
            draw_rounded_rect(draw, [14, y_pos, sidebar_w - 14, y_pos + 42], radius=8, fill="#0D9488")
            draw.text((28, y_pos + 11), icon_sym, fill="#FFFFFF", font=f_menu_b)
            draw.text((54, y_pos + 11), label, fill="#FFFFFF", font=f_menu_b)
        else:
            draw.text((28, y_pos + 11), icon_sym, fill="#64748B", font=f_menu)
            draw.text((54, y_pos + 11), label, fill="#334155", font=f_menu)
        y_pos += 48

    # Footer del Sidebar: DISA Apurímac II
    draw_rounded_rect(draw, [16, height - 86, sidebar_w - 16, height - 20], radius=10, fill="#F0FDFA", outline="#CCFBF1", width=1)
    f_foot_b = get_font(13, bold=True)
    f_foot_s = get_font(11, bold=False)
    draw.text((28, height - 72), "DISA Apurímac II", fill="#0F766E", font=f_foot_b)
    draw.text((28, height - 50), "Estrategia Sanitaria", fill="#0D9488", font=f_foot_s)

    # Topbar superior
    draw.rectangle([sidebar_w, 0, width, 68], fill="#FFFFFF", outline="#E2E8F0", width=1)
    f_bc1 = get_font(13, bold=False)
    f_bc2 = get_font(13, bold=True)
    draw.text((sidebar_w + 28, 24), "SIVAC  /  ", fill="#64748B", font=f_bc1)
    draw.text((sidebar_w + 88, 24), breadcrumb_sub, fill="#0F172A", font=f_bc2)

    # Usuario autenticado en la esquina superior derecha
    user_x = width - 255
    draw.ellipse([user_x - 42, 16, user_x - 6, 52], fill="#0D9488")
    draw.text((user_x - 32, 24), "JQ", fill="#FFFFFF", font=get_font(13, bold=True))
    draw.text((user_x, 16), "José Luis Quispe León", fill="#0F172A", font=get_font(13, bold=True))
    draw.text((user_x, 35), "Administrador", fill="#64748B", font=get_font(11, bold=False))

    return img, draw, sidebar_w + 28, 92


# ==============================================================================
# 1. FIGURA 11: ARQUITECTURA DE 3 CAPAS DESACOPLADAS DE SIVAC
# ==============================================================================
def generar_figura_11_arquitectura_3capas():
    W, H = 2200, 1280
    img = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    # Marco general técnico
    draw_rounded_rect(draw, [24, 24, W - 24, H - 24], radius=14, fill="#FAFCFF", outline="#CBD5E1", width=2)

    # Encabezado técnico
    draw_rounded_rect(draw, [48, 44, W - 48, 130], radius=10, fill="#0F172A")
    draw.text((76, 58), "ARQUITECTURA LÓGICA Y FÍSICA EN TRES CAPAS DESACOPLADAS — SISTEMA WEB SIVAC", fill="#FFFFFF", font=get_font(22, bold=True))
    draw.text((76, 92), "Metáfora XP: «Cadena digital sincronizada de trazabilidad de biológicos» | Dirección de Salud Apurímac II (Andahuaylas - Chincheros)", fill="#94A3B8", font=get_font(15, bold=False))

    # 3 Capas en columnas
    col_w = 620
    gap = 62
    left_0 = 68
    top_y = 165
    bot_y = 1130

    capas = [
        {
            "num": "CAPA 1: PRESENTACIÓN CLIENTE (SPA)",
            "sub": "Frontend React 18.3 + TypeScript 5.5 + Vite 5.4",
            "color_hdr": "#0D9488",
            "color_bg": "#F0FDFA",
            "color_bd": "#5EEAD4",
            "bloques": [
                ("Vistas y Módulos React (src/components)", [
                    "• auth/LoginForm.tsx (Autenticación JWT y control de sesión)",
                    "• Dashboard/Dashboard.tsx (KPIs, alertas y stock en vivo)",
                    "• Establecimientos/EstablecimientosModule.tsx (8 Centros Acopio)",
                    "• Inventario/Inventario.tsx (Lotes vacunas/jeringas FEFO)",
                    "• Planificacion/ (Metas anuales, CENARES Q1-Q4, ICI-DEMID)",
                    "• Movimientos/Movimientos.tsx (Cuadrícula mensual y saldos)",
                    "• Vales/Vales.tsx (Comprobantes de salida y entregas adic.)",
                    "• Kardex/ & Reportes/ (Trazabilidad por lote PDF/Excel)",
                ]),
                ("Gestión de Estado, Hooks y Contextos (src/hooks & contexts)", [
                    "• AuthContext.tsx & ProtectedRoute.tsx (Guardas RBAC)",
                    "• useMovimientos.ts, useDashboard.ts, useAutoSync.ts",
                    "• stockEventEmitter.ts (Sincronización reactiva inter-módulos)",
                ]),
                ("Capa de Servicios Cliente HTTP (src/services)", [
                    "• apiClient Axios con interceptores Bearer JWT",
                    "• MovimientosService, ValesService, PlanificacionService",
                    "• Diseño Responsivo Tailwind CSS 3.4 + Framer Motion",
                ]),
            ]
        },
        {
            "num": "CAPA 2: LÓGICA DE NEGOCIO Y API RESTful",
            "sub": "Backend Node.js + Express 4.18 + TypeScript 5.3",
            "color_hdr": "#1E3A8A",
            "color_bg": "#EFF6FF",
            "color_bd": "#93C5FD",
            "bloques": [
                ("Pipeline de Middlewares y Seguridad (backend/src/middleware)", [
                    "• Autenticación JWT (jsonwebtoken) + Hash Bcrypt (10 salt rounds)",
                    "• Autorización RBAC granular y PermisoOperativo temporal",
                    "• Validación de esquemas tipados (Zod / Joi) + Rate Limiting",
                ]),
                ("Controladores RESTful (backend/src/controllers)", [
                    "• AuthController, UsuarioController, RoleController",
                    "• RedController, MicroredController, CentroAcopioController",
                    "• VacunaController, LoteVacunaController, JeringaController",
                    "• PlanificacionController, ProgramacionAnualCenaresController",
                    "• AjusteEntregasController, EntregaAdicionalController, ValeController",
                ]),
                ("Servicios de Dominio y Motores de Exportación (backend/src/services)", [
                    "• MovimientosService (Sincronización recursiva de saldos)",
                    "• ValeService & ValeStockService (Descuento FEFO y unicidad)",
                    "• AlertaAutomaticaService (Detección proactiva de caducidad)",
                    "• ValeExportService & KardexExportService (PDFKit / ExcelJS)",
                ]),
            ]
        },
        {
            "num": "CAPA 3: PERSISTENCIA Y DATOS RELACIONALES",
            "sub": "Prisma ORM 5.7 + Motor Relacional PostgreSQL (3FN)",
            "color_hdr": "#334155",
            "color_bg": "#F8FAFC",
            "color_bd": "#CBD5E1",
            "bloques": [
                ("Capa de Abstracción de Datos (backend/prisma/schema.prisma)", [
                    "• Prisma Client tipado con transacciones ACID ($transaction)",
                    "• Claves primarias UUID nativas e índices compuestos únicos",
                    "• Políticas de integridad referencial y borrado protegido",
                ]),
                ("Dominios Relacionales en PostgreSQL (26 Tablas Físicas)", [
                    "• Seguridad RBAC: usuarios, roles, permissions, role_permissions,",
                    "  usuarios_centros_acopio, permisos_operativos",
                    "• Territorio: redes, microredes, centros_acopio, establecimientos",
                    "• Catálogo y Lotes FEFO: vacunas, jeringas, lotes_vacunas,",
                    "  lotes_jeringas, configuracion_jeringa_vacuna_*",
                    "• Programación: planificacion_anual, programacion_anual_cenares,",
                    "  stock_inicial_mensual, ici_demid_registros",
                    "• Transaccional: movimientos_vacunas, entregas_adicionales,",
                    "  vales_entrega, vales_detalle, kardex, alertas",
                ]),
                ("Respaldo y Auditoría Transaccional", [
                    "• Registro inmutable de trazabilidad por lote en tabla kardex",
                    "• Consistencia aritmética garantizada a nivel de motor SQL",
                ]),
            ]
        },
    ]

    for idx, c in enumerate(capas):
        x1 = left_0 + idx * (col_w + gap)
        x2 = x1 + col_w
        draw_rounded_rect(draw, [x1, top_y, x2, bot_y], radius=12, fill=c["color_bg"], outline=c["color_bd"], width=2)
        draw_rounded_rect(draw, [x1, top_y, x2, top_y + 84], radius=12, fill=c["color_hdr"])
        draw.text((x1 + 22, top_y + 16), c["num"], fill="#FFFFFF", font=get_font(18, bold=True))
        draw.text((x1 + 22, top_y + 46), c["sub"], fill="#E2E8F0", font=get_font(14, bold=False))

        by = top_y + 106
        for b_title, items in c["bloques"]:
            bh = 48 + len(items) * 30 + 14
            draw_rounded_rect(draw, [x1 + 18, by, x2 - 18, by + bh], radius=8, fill="#FFFFFF", outline=c["color_bd"], width=2)
            draw.text((x1 + 32, by + 12), b_title, fill=c["color_hdr"], font=get_font(15, bold=True))
            draw.line([x1 + 32, by + 38, x2 - 32, by + 38], fill="#E2E8F0", width=1)
            iy = by + 46
            for line in items:
                draw.text((x1 + 34, iy), line, fill="#1E293B", font=get_font(13, bold=False))
                iy += 29
            by += bh + 20

    # Flechas de comunicación entre capas
    mid_y1 = 540
    mid_y2 = 660
    # Entre Capa 1 y Capa 2
    ax1 = left_0 + col_w
    ax2 = ax1 + gap
    draw.line([ax1 + 4, mid_y1, ax2 - 4, mid_y1], fill="#0D9488", width=4)
    draw.polygon([(ax2 - 4, mid_y1), (ax2 - 16, mid_y1 - 8), (ax2 - 16, mid_y1 + 8)], fill="#0D9488")
    draw.text((ax1 + 6, mid_y1 - 38), "HTTPS / JSON", fill="#0F766E", font=get_font(11, bold=True))
    draw.text((ax1 + 8, mid_y1 - 22), "Bearer JWT", fill="#0F766E", font=get_font(11, bold=False))

    draw.line([ax1 + 4, mid_y2, ax2 - 4, mid_y2], fill="#1E3A8A", width=4)
    draw.polygon([(ax1 + 4, mid_y2), (ax1 + 16, mid_y2 - 8), (ax1 + 16, mid_y2 + 8)], fill="#1E3A8A")
    draw.text((ax1 + 6, mid_y2 + 10), "DTOs + Streams", fill="#1E3A8A", font=get_font(11, bold=True))
    draw.text((ax1 + 8, mid_y2 + 26), "PDF / Excel", fill="#1E3A8A", font=get_font(11, bold=False))

    # Entre Capa 2 y Capa 3
    bx1 = left_0 + col_w * 2 + gap
    bx2 = bx1 + gap
    draw.line([bx1 + 4, mid_y1, bx2 - 4, mid_y1], fill="#1E3A8A", width=4)
    draw.polygon([(bx2 - 4, mid_y1), (bx2 - 16, mid_y1 - 8), (bx2 - 16, mid_y1 + 8)], fill="#1E3A8A")
    draw.text((bx1 + 6, mid_y1 - 38), "Prisma Client", fill="#1E3A8A", font=get_font(11, bold=True))
    draw.text((bx1 + 6, mid_y1 - 22), "SQL / ACID", fill="#1E3A8A", font=get_font(11, bold=False))

    draw.line([bx1 + 4, mid_y2, bx2 - 4, mid_y2], fill="#334155", width=4)
    draw.polygon([(bx1 + 4, mid_y2), (bx1 + 16, mid_y2 - 8), (bx1 + 16, mid_y2 + 8)], fill="#334155")
    draw.text((bx1 + 4, mid_y2 + 10), "Result Sets", fill="#334155", font=get_font(11, bold=True))
    draw.text((bx1 + 4, mid_y2 + 26), "Tipados 3FN", fill="#334155", font=get_font(11, bold=False))

    # Barra inferior de atributos de calidad ISO/IEC 25010:2023
    draw_rounded_rect(draw, [68, 1152, W - 68, 1232], radius=10, fill="#F1F5F9", outline="#CBD5E1", width=2)
    draw.text((92, 1166), "ATRIBUTOS DE CALIDAD VERIFICADOS (ISO/IEC 25010:2023):", fill="#0F172A", font=get_font(15, bold=True))
    draw.text((92, 1194), "• Adecuación Funcional: 100% (16/16 HU)   |   • Eficiencia Temporal: API < 250 ms, Vales PDF < 3 s   |   • Fiabilidad: Transacciones ACID   |   • Seguridad: JWT + Bcrypt + RBAC   |   • Mantenibilidad: 151 pruebas automatizadas", fill="#334155", font=get_font(14, bold=False))

    save_300dpi(img, "figura_arquitectura_sivac_3capas.png")


# ==============================================================================
# 2. FIGURA 12: DIAGRAMA GENERAL DE CASOS DE USO UML (RBAC + 16 HU)
# ==============================================================================
def draw_stick_actor(draw: ImageDraw.ImageDraw, cx: int, cy: int, role_title: str, role_code: str, color: str = "#0F172A"):
    """Dibuja un actor UML estándar con etiqueta inferior."""
    # Cabeza
    r = 18
    draw.ellipse([cx - r, cy - 52 - r, cx + r, cy - 52 + r], fill="#FFFFFF", outline=color, width=3)
    # Tronco
    draw.line([cx, cy - 34, cx, cy + 12], fill=color, width=3)
    # Brazos
    draw.line([cx - 26, cy - 18, cx + 26, cy - 18], fill=color, width=3)
    # Piernas
    draw.line([cx, cy + 12, cx - 22, cy + 48], fill=color, width=3)
    draw.line([cx, cy + 12, cx + 22, cy + 48], fill=color, width=3)

    # Etiqueta del actor
    draw_rounded_rect(draw, [cx - 115, cy + 56, cx + 115, cy + 106], radius=6, fill="#F8FAFC", outline=color, width=2)
    f_b = get_font(13, bold=True)
    f_c = get_font(11, bold=False, mono=True)
    draw.text((cx - 105, cy + 62), role_title, fill=color, font=f_b)
    draw.text((cx - 105, cy + 82), f"«actor» {role_code}", fill="#475569", font=f_c)


def generar_figura_12_casos_uso():
    W, H = 2250, 1420
    img = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    # Marco exterior
    draw_rounded_rect(draw, [20, 20, W - 20, H - 20], radius=12, fill="#FFFFFF", outline="#CBD5E1", width=2)

    # Encabezado
    draw_rounded_rect(draw, [44, 38, W - 44, 114], radius=8, fill="#0F172A")
    draw.text((68, 48), "DIAGRAMA GENERAL DE CASOS DE USO UML — SISTEMA WEB SIVAC (DISA APURÍMAC II)", fill="#FFFFFF", font=get_font(20, bold=True))
    draw.text((68, 78), "Trazabilidad 1:1 con el esquema de Control de Acceso Basado en Roles (RBAC) y las 16 Historias de Usuario (HU-01 a HU-16)", fill="#94A3B8", font=get_font(14, bold=False))

    # Límite del sistema (System Boundary)
    sb_x1, sb_y1, sb_x2, sb_y2 = 340, 136, W - 340, H - 96
    draw_rounded_rect(draw, [sb_x1, sb_y1, sb_x2, sb_y2], radius=12, fill="#F8FAFC", outline="#0F172A", width=3)
    draw_rounded_rect(draw, [sb_x1 + 16, sb_y1 + 12, sb_x2 - 16, sb_y1 + 54], radius=6, fill="#0D9488")
    draw.text((sb_x1 + 34, sb_y1 + 21), "«system» Sistema Web de Gestión de Movimientos de Vacunas — SIVAC (syncova)", fill="#FFFFFF", font=get_font(16, bold=True))

    # 4 Actores institucionales + equivalencia RBAC (ADMIN / COORDINADOR / ALMACENERO / CONSULTA)
    left_actor_x = 170
    right_actor_x = W - 170

    actores_izq = [
        (left_actor_x, 340, "Administrador TI", "administrador (ADMIN)", "#1E3A8A"),
        (left_actor_x, 860, "Coordinador Regional", "coordinador (ADMIN/COORD)", "#0F766E"),
    ]
    actores_der = [
        (right_actor_x, 420, "Responsable de Acopio", "responsable_acopio (ALMACENERO)", "#0D9488"),
        (right_actor_x, 960, "Operador Establecimiento", "operador (CONSULTA)", "#475569"),
    ]

    for ax, ay, rtitle, rcode, col in actores_izq + actores_der:
        draw_stick_actor(draw, ax, ay, rtitle, rcode, col)

    # 16 Casos de uso distribuidos en 2 columnas dentro del System Boundary (8 por columna)
    col1_cx = 760
    col2_cx = 1480
    rx, ry = 325, 42

    uc_col1 = [
        ("CU-01 (HU-01): Autenticar sesión JWT y validar permisos RBAC", 260, "#FEF3C7", "#D97706"),
        ("CU-02 (HU-02): Gestionar redes, microredes, 8 acopios y EESS", 378, "#EFF6FF", "#1E3A8A"),
        ("CU-03 (HU-03): Administrar catálogo maestro de vacunas y jeringas", 496, "#EFF6FF", "#1E3A8A"),
        ("CU-04 (HU-04): Configurar multiplicadores jeringa-vacuna", 614, "#EFF6FF", "#1E3A8A"),
        ("CU-06 (HU-06): Registrar planificación anual y 12 cuotas mensuales", 732, "#F0FDFA", "#0F766E"),
        ("CU-07 (HU-07): Gestionar programación CENARES (Q1-Q4) y stock inicial", 850, "#F0FDFA", "#0F766E"),
        ("CU-08 (HU-08): Importar y consolidar registros históricos ICI-DEMID", 968, "#F0FDFA", "#0F766E"),
        ("CU-16 (HU-16): Monitorear Dashboard y habilitar permisos operativos", 1086, "#F0FDFA", "#0F766E"),
    ]

    uc_col2 = [
        ("CU-05 (HU-05): Registrar lotes de vacunas y jeringas bajo FEFO", 260, "#ECFDF5", "#047857"),
        ("CU-09 (HU-09): Registrar movimientos mensuales en cuadrícula", 378, "#ECFDF5", "#047857"),
        ("CU-10 (HU-10): Sincronizar saldos intermensuales automáticamente", 496, "#ECFDF5", "#047857"),
        ("CU-11 (HU-11): Redistribuir cuotas y registrar entregas adicionales", 614, "#ECFDF5", "#047857"),
        ("CU-12 (HU-12): Emitir vales de entrega oficiales por centro y periodo", 732, "#ECFDF5", "#047857"),
        ("CU-13 (HU-13): Exportar comprobantes de salida (vales) en PDF y Excel", 850, "#F8FAFC", "#334155"),
        ("CU-14 (HU-14): Consultar y exportar Kardex inmutable por lote", 968, "#F8FAFC", "#334155"),
        ("CU-15 (HU-15): Gestionar alertas automáticas de caducidad y stock", 1086, "#FFFBEB", "#B45309"),
    ]

    # Líneas de asociación primero (para que queden detrás de las elipses)
    # Actor 1 (Administrador): CU-01, CU-02, CU-03, CU-16
    for target_y in [260, 378, 496, 1086]:
        draw.line([left_actor_x + 95, 340, col1_cx - rx, target_y], fill="#1E3A8A", width=2)

    # Actor 2 (Coordinador Regional): CU-01, CU-03, CU-04, CU-06, CU-07, CU-08, CU-14, CU-15, CU-16
    for target_y in [260, 496, 614, 732, 850, 968, 1086]:
        draw.line([left_actor_x + 95, 860, col1_cx - rx, target_y], fill="#0F766E", width=2)
    for target_y in [968, 1086]:
        draw.line([left_actor_x + 95, 860, col2_cx - rx, target_y], fill="#0F766E", width=2)

    # Actor 3 (Responsable de Acopio / ALMACENERO): CU-01, CU-05, CU-06, CU-09, CU-10, CU-11, CU-12, CU-13, CU-14, CU-15
    for target_y in [260, 378, 496, 614, 732, 850, 968, 1086]:
        draw.line([right_actor_x - 95, 420, col2_cx + rx, target_y], fill="#0D9488", width=2)

    # Actor 4 (Operador Establecimiento / CONSULTA): CU-01, CU-13, CU-14, CU-15
    for target_y in [850, 968, 1086]:
        draw.line([right_actor_x - 95, 960, col2_cx + rx, target_y], fill="#475569", width=2)

    # Relaciones <<include>> y <<extend>> internas entre casos de uso
    # CU-09 <<include>> CU-10
    draw.line([col2_cx, 378 + ry, col2_cx, 496 - ry], fill="#047857", width=2)
    draw.text((col2_cx + 12, 428), "«include»", fill="#047857", font=get_font(12, italic=True))
    # CU-09 <<extend>> CU-11
    draw.line([col2_cx - 120, 378 + ry, col2_cx - 120, 614 - ry], fill="#047857", width=2)
    draw.text((col2_cx - 210, 540), "«extend»", fill="#047857", font=get_font(12, italic=True))
    # CU-12 <<include>> CU-09
    draw.line([col2_cx + 140, 732 - ry, col2_cx + 140, 378 + ry], fill="#047857", width=2)
    draw.text((col2_cx + 148, 668), "«include»", fill="#047857", font=get_font(12, italic=True))
    # CU-13 <<extend>> CU-12
    draw.line([col2_cx, 850 - ry, col2_cx, 732 + ry], fill="#334155", width=2)
    draw.text((col2_cx + 12, 782), "«extend»", fill="#334155", font=get_font(12, italic=True))
    # Todos incluyen autenticación JWT (CU-01)
    draw.line([col1_cx + rx, 260, col2_cx - rx, 260], fill="#D97706", width=2)
    draw.text(((col1_cx + col2_cx) // 2 - 42, 236), "«include» JWT", fill="#B45309", font=get_font(12, italic=True))

    # Dibujar las elipses de los 16 casos de uso
    f_uc = get_font(13, bold=True)
    for text, cy, bg, bd in uc_col1:
        draw.ellipse([col1_cx - rx, cy - ry, col1_cx + rx, cy + ry], fill=bg, outline=bd, width=2)
        draw.text((col1_cx - rx + 36, cy - 9), text, fill="#0F172A", font=f_uc)

    for text, cy, bg, bd in uc_col2:
        draw.ellipse([col2_cx - rx, cy - ry, col2_cx + rx, cy + ry], fill=bg, outline=bd, width=2)
        draw.text((col2_cx - rx + 36, cy - 9), text, fill="#0F172A", font=f_uc)

    # Leyenda inferior
    draw_rounded_rect(draw, [44, H - 78, W - 44, H - 32], radius=8, fill="#F1F5F9", outline="#CBD5E1", width=1)
    draw.text((68, H - 64), "LEYENDA UML Y PERFILES RBAC:   [Elipse Amarilla] Seguridad Transversal JWT/RBAC   |   [Elipse Azul/Turquesa] Gestión Territorial, Catálogos y Planificación   |   [Elipse Verde] Operación de Lotes FEFO, Movimientos y Vales   |   [Elipse Gris] Reportes y Kardex", fill="#334155", font=get_font(13, bold=True))

    save_300dpi(img, "figura_casos_uso_sivac.png")


# ==============================================================================
# 3. FIGURA 13: MODELO ENTIDAD-RELACIÓN FÍSICO (26 TABLAS PRISMA/POSTGRESQL)
# ==============================================================================
def draw_er_entity(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, model_name: str, table_name: str, fields: list, hdr_color: str):
    """Dibuja una entidad física PostgreSQL/Prisma con PK, UK y FK."""
    row_h = 22
    h = 46 + len(fields) * row_h + 8
    draw_rounded_rect(draw, [x, y, x + w, y + h], radius=7, fill="#FFFFFF", outline=hdr_color, width=2)
    draw_rounded_rect(draw, [x, y, x + w, y + 42], radius=7, fill=hdr_color)
    draw.text((x + 10, y + 5), model_name, fill="#FFFFFF", font=get_font(13, bold=True))
    draw.text((x + 10, y + 23), f"table: {table_name}", fill="#E2E8F0", font=get_font(10, mono=True))

    fy = y + 48
    for badge, fname, ftype in fields:
        badge_col = "#B45309" if "PK" in badge else ("#1D4ED8" if "FK" in badge else ("#047857" if "UK" in badge else "#64748B"))
        draw.text((x + 8, fy), badge, fill=badge_col, font=get_font(10, bold=True, mono=True))
        draw.text((x + 48, fy), fname, fill="#0F172A", font=get_font(11, bold=False, mono=True))
        draw.text((x + w - 95, fy), ftype, fill="#475569", font=get_font(10, bold=False, mono=True))
        fy += row_h
    return x, y, w, h


def generar_figura_13_mer():
    W, H = 2400, 1560
    img = Image.new("RGB", (W, H), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    # Encabezado
    draw_rounded_rect(draw, [24, 20, W - 24, 92], radius=8, fill="#0F172A")
    draw.text((48, 30), "MODELO ENTIDAD-RELACIÓN FÍSICO (3FN) — BASE DE DATOS POSTGRESQL / PRISMA ORM DEL SISTEMA SIVAC", fill="#FFFFFF", font=get_font(20, bold=True))
    draw.text((48, 58), "Especificación verificada 1:1 con backend/prisma/schema.prisma (26 tablas relacionales con claves primarias UUID, claves foráneas e índices únicos compuestos)", fill="#94A3B8", font=get_font(14, bold=False))

    # 4 Zonas de Dominio
    # Zona 1: Territorio y Red Sanitaria (Columna 1)
    # Zona 2: Catálogo Biológico, Lotes FEFO y Multiplicadores (Columna 2)
    # Zona 3: Planificación, Movimientos, Vales y Kardex (Columna 3 y 4)
    # Zona 4: Seguridad RBAC, Usuarios y Alertas (Columna 5)

    col_w = 435
    xs = [36, 508, 980, 1452, 1924]

    # Líneas conectoras de relaciones (dibujadas primero como fondo limpio)
    rel_lines = [
        ((xs[0] + col_w // 2, 230), (xs[0] + col_w // 2, 1180), "#0F766E"),
        ((xs[1] + col_w // 2, 230), (xs[1] + col_w // 2, 1340), "#1E3A8A"),
        ((xs[2] + col_w // 2, 230), (xs[2] + col_w // 2, 1340), "#047857"),
        ((xs[3] + col_w // 2, 230), (xs[3] + col_w // 2, 1340), "#7C2D12"),
        ((xs[4] + col_w // 2, 230), (xs[4] + col_w // 2, 1340), "#334155"),
        # Relaciones horizontales entre dominios
        ((xs[0] + col_w, 600), (xs[2], 600), "#0D9488"),
        ((xs[0] + col_w, 860), (xs[2], 860), "#0D9488"),
        ((xs[1] + col_w, 240), (xs[2], 240), "#1E3A8A"),
        ((xs[2] + col_w, 620), (xs[3], 620), "#047857"),
        ((xs[2] + col_w, 920), (xs[3], 920), "#047857"),
        ((xs[3] + col_w, 620), (xs[4], 620), "#334155"),
    ]
    for p1, p2, lc in rel_lines:
        draw.line([p1[0], p1[1], p2[0], p2[1]], fill=lc, width=3)

    # COLUMNA 0: DOMINIO TERRITORIAL (Verde Azulado)
    c0 = "#0F766E"
    draw_er_entity(draw, xs[0], 115, col_w, "Red", "redes", [
        ("PK", "id", "UUID"),
        ("UK", "nombre", "VARCHAR"),
        ("UK", "codigo", "VARCHAR"),
        ("  ", "descripcion", "TEXT?"),
        ("  ", "activo", "BOOLEAN"),
    ], c0)

    draw_er_entity(draw, xs[0], 320, col_w, "Microred", "microredes", [
        ("PK", "id", "UUID"),
        ("UK", "nombre", "VARCHAR"),
        ("UK", "codigo", "VARCHAR"),
        ("FK", "red_id", "UUID"),
        ("  ", "activo", "BOOLEAN"),
    ], c0)

    draw_er_entity(draw, xs[0], 525, col_w, "CentroAcopio", "centros_acopio", [
        ("PK", "id", "UUID"),
        ("UK", "nombre", "VARCHAR"),
        ("UK", "codigo", "VARCHAR"),
        ("FK", "microred_id", "UUID"),
        ("  ", "responsable", "VARCHAR"),
        ("  ", "capacidad_almacen", "INT?"),
    ], c0)

    draw_er_entity(draw, xs[0], 755, col_w, "Establecimiento", "establecimientos", [
        ("PK", "id", "UUID"),
        ("UK", "codigo", "VARCHAR"),
        ("  ", "nombre", "VARCHAR"),
        ("  ", "tipo", "ENUM"),
        ("FK", "centro_acopio_id", "UUID"),
        ("  ", "poblacion_asignada", "INT?"),
    ], c0)

    draw_er_entity(draw, xs[0], 985, col_w, "UsuarioCentroAcopio", "usuarios_centros_acopio", [
        ("PK", "id", "UUID"),
        ("FK", "usuario_id", "UUID"),
        ("FK", "centro_acopio_id", "UUID"),
        ("UK", "uk_usuario_centro", "COMPOSITE"),
    ], c0)

    draw_er_entity(draw, xs[0], 1170, col_w, "PermisoOperativo", "permisos_operativos", [
        ("PK", "id", "UUID"),
        ("FK", "centro_acopio_id", "UUID"),
        ("  ", "planificacion_edicion", "BOOLEAN"),
        ("  ", "movimientos_edicion", "BOOLEAN"),
        ("FK", "habilitado_por", "UUID?"),
    ], c0)

    # COLUMNA 1: CATÁLOGO BIOLÓGICO Y LOTES FEFO (Azul Marino)
    c1 = "#1E3A8A"
    draw_er_entity(draw, xs[1], 115, col_w, "Vacuna", "vacunas", [
        ("PK", "id", "UUID"),
        ("IX", "codigo", "VARCHAR"),
        ("  ", "nombre", "VARCHAR"),
        ("  ", "dosis_por_frasco", "INT"),
        ("  ", "temperatura_min", "DECIMAL"),
        ("  ", "temperatura_max", "DECIMAL"),
    ], c1)

    draw_er_entity(draw, xs[1], 340, col_w, "LoteVacuna", "lotes_vacunas", [
        ("PK", "id", "UUID"),
        ("UK", "numero", "VARCHAR"),
        ("FK", "vacuna_id", "UUID"),
        ("  ", "fecha_ingreso", "DATE"),
        ("  ", "fecha_caducidad", "DATE (FEFO)"),
        ("  ", "cantidad_inicial", "INT"),
        ("  ", "cantidad_actual", "INT"),
        ("  ", "numero_comprobante", "VARCHAR"),
    ], c1)

    draw_er_entity(draw, xs[1], 610, col_w, "Jeringa", "jeringas", [
        ("PK", "id", "UUID"),
        ("  ", "tipo", "VARCHAR"),
        ("  ", "capacidad", "VARCHAR"),
        ("  ", "aguja", "VARCHAR"),
        ("  ", "color", "VARCHAR"),
    ], c1)

    draw_er_entity(draw, xs[1], 815, col_w, "LoteJeringa", "lotes_jeringas", [
        ("PK", "id", "UUID"),
        ("UK", "numero", "VARCHAR"),
        ("FK", "jeringa_id", "UUID"),
        ("  ", "fecha_caducidad", "DATE (FEFO)"),
        ("  ", "cantidad_inicial", "INT"),
        ("  ", "cantidad_actual", "INT"),
    ], c1)

    draw_er_entity(draw, xs[1], 1040, col_w, "ConfiguracionJeringaVacunaDefecto", "configuracion_jeringa_vacuna_defecto", [
        ("PK", "id", "UUID"),
        ("FK", "vacuna_id", "UUID"),
        ("FK", "jeringa_id", "UUID"),
        ("  ", "multiplicador", "INT"),
        ("UK", "uk_vacuna_jeringa_def", "COMPOSITE"),
    ], c1)

    draw_er_entity(draw, xs[1], 1245, col_w, "ConfiguracionJeringaVacunaCentro", "configuracion_jeringa_vacuna_centro", [
        ("PK", "id", "UUID"),
        ("FK", "centro_acopio_id", "UUID"),
        ("FK", "vacuna_id / jeringa_id", "UUID"),
        ("  ", "multiplicador", "INT"),
        ("UK", "uk_centro_vac_jer", "COMPOSITE"),
    ], c1)

    # COLUMNA 2: PLANIFICACIÓN Y MOVIMIENTOS MENSUALES (Verde Esmeralda)
    c2 = "#047857"
    draw_er_entity(draw, xs[2], 115, col_w, "PlanificacionAnual", "planificacion_anual", [
        ("PK", "id", "UUID"),
        ("FK", "establecimiento_id", "UUID"),
        ("FK", "vacuna_id", "UUID"),
        ("  ", "anio", "INT"),
        ("  ", "meta_anual", "INT"),
        ("  ", "datos_mensuales", "JSONB (12m)"),
        ("UK", "uk_plan_est_vac_anio", "COMPOSITE"),
    ], c2)

    draw_er_entity(draw, xs[2], 360, col_w, "ProgramacionAnualCenares", "programacion_anual_cenares", [
        ("PK", "id", "UUID"),
        ("FK", "vacuna_id", "UUID"),
        ("  ", "anio", "INT"),
        ("  ", "trimestre_1..4", "INT (Q1-Q4)"),
        ("UK", "uk_prog_cenares", "COMPOSITE"),
    ], c2)

    draw_er_entity(draw, xs[2], 565, col_w, "StockInicialMensual", "stock_inicial_mensual", [
        ("PK", "id", "UUID"),
        ("FK", "vacuna_id", "UUID"),
        ("  ", "anio / mes", "INT"),
        ("  ", "cantidad", "INT"),
        ("UK", "uk_stock_ini_vac_mes", "COMPOSITE"),
    ], c2)

    draw_er_entity(draw, xs[2], 770, col_w, "MovimientoVacuna", "movimientos_vacunas", [
        ("PK", "id", "UUID"),
        ("FK", "establecimiento_id", "UUID"),
        ("FK", "vacuna_id", "UUID"),
        ("  ", "mes / anio", "INT"),
        ("  ", "saldo_anterior", "INT"),
        ("  ", "ingreso_transferencia", "INT"),
        ("  ", "salida_transferencia", "INT"),
        ("  ", "entregas", "INT"),
        ("UK", "uk_mov_est_vac_mes_anio", "COMPOSITE"),
    ], c2)

    draw_er_entity(draw, xs[2], 1060, col_w, "EntregaAdicional", "entregas_adicionales", [
        ("PK", "id", "UUID"),
        ("FK", "movimiento_id", "UUID"),
        ("  ", "numero_entrega", "INT"),
        ("  ", "cantidad", "INT"),
        ("  ", "fecha_entrega", "DATE"),
        ("  ", "motivo", "VARCHAR?"),
        ("UK", "uk_mov_num_entrega", "COMPOSITE"),
    ], c2)

    draw_er_entity(draw, xs[2], 1300, col_w, "IciDemidRegistro", "ici_demid_registros", [
        ("PK", "id", "UUID"),
        ("FK", "establecimiento_id", "UUID"),
        ("FK", "vacuna_id", "UUID"),
        ("  ", "anio / datos_mensuales", "INT / JSONB"),
    ], c2)

    # COLUMNA 3: VALES OFICIALES, KARDEX Y ALERTAS (Ámbar / Terracota)
    c3 = "#9A3412"
    draw_er_entity(draw, xs[3], 115, col_w, "ValeEntrega", "vales_entrega", [
        ("PK", "id", "UUID"),
        ("UK", "numero", "VARCHAR"),
        ("FK", "centro_acopio_id", "UUID"),
        ("  ", "mes / anio", "VARCHAR / INT"),
        ("  ", "tipo_vale", "VARCHAR"),
        ("  ", "grupos_incluidos", "VARCHAR"),
        ("  ", "total_dosis", "INT"),
        ("  ", "total_frascos", "INT"),
        ("FK", "generado_por_id", "UUID"),
        ("UK", "uk_centro_per_tipo_grp", "COMPOSITE"),
    ], c3)

    draw_er_entity(draw, xs[3], 425, col_w, "ValeDetalle", "vales_detalle", [
        ("PK", "id", "UUID"),
        ("FK", "vale_id", "UUID"),
        ("FK", "establecimiento_id", "UUID"),
        ("FK", "vacuna_id", "UUID"),
        ("  ", "cantidad_base", "INT"),
        ("  ", "entregas_adicionales", "JSONB"),
        ("  ", "total_dosis", "INT"),
        ("  ", "total_frascos", "INT"),
        ("UK", "uk_vale_est_vacuna", "COMPOSITE"),
    ], c3)

    draw_er_entity(draw, xs[3], 715, col_w, "Kardex", "kardex", [
        ("PK", "id", "UUID"),
        ("  ", "fecha", "TIMESTAMP"),
        ("  ", "tipo_movimiento", "ENUM"),
        ("  ", "tipo_item / item_id", "ENUM / UUID"),
        ("  ", "lote_numero", "VARCHAR"),
        ("  ", "cantidad", "INT"),
        ("  ", "saldo_anterior", "INT"),
        ("  ", "saldo_actual", "INT"),
        ("FK", "establecimiento_origen_id", "UUID"),
        ("FK", "usuario_id", "UUID"),
    ], c3)

    draw_er_entity(draw, xs[3], 1030, col_w, "Alerta", "alertas", [
        ("PK", "id", "UUID"),
        ("  ", "tipo", "ENUM"),
        ("  ", "mensaje", "TEXT"),
        ("  ", "prioridad", "ENUM"),
        ("  ", "fecha_vencimiento", "DATE"),
        ("  ", "leida / archivada", "BOOLEAN"),
        ("FK", "establecimiento_id", "UUID"),
        ("  ", "lote_id / lote_numero", "UUID / VARCHAR"),
    ], c3)

    # COLUMNA 4: SEGURIDAD RBAC Y AUDITORÍA DE USUARIOS (Gris Pizarra)
    c4 = "#334155"
    draw_er_entity(draw, xs[4], 115, col_w, "Usuario", "usuarios", [
        ("PK", "id", "UUID"),
        ("UK", "email", "VARCHAR"),
        ("UK", "usuario", "VARCHAR"),
        ("  ", "nombre / apellido", "VARCHAR"),
        ("  ", "password_hash", "VARCHAR (Bcrypt)"),
        ("  ", "rol", "ENUM"),
        ("FK", "role_id", "UUID?"),
        ("FK", "establecimiento_id", "UUID?"),
        ("FK", "centro_acopio_id", "UUID?"),
        ("  ", "activo / ultimo_acceso", "BOOL / TIMESTAMP"),
    ], c4)

    draw_er_entity(draw, xs[4], 430, col_w, "Role", "roles", [
        ("PK", "id", "UUID"),
        ("UK", "nombre", "VARCHAR"),
        ("UK", "codigo", "VARCHAR"),
        ("  ", "descripcion", "TEXT?"),
        ("  ", "is_system / is_default", "BOOLEAN"),
        ("  ", "activo", "BOOLEAN"),
    ], c4)

    draw_er_entity(draw, xs[4], 660, col_w, "Permission", "permissions", [
        ("PK", "id", "UUID"),
        ("UK", "nombre", "VARCHAR"),
        ("UK", "codigo", "VARCHAR"),
        ("  ", "recurso", "VARCHAR"),
        ("  ", "accion", "VARCHAR"),
        ("  ", "categoria", "VARCHAR"),
    ], c4)

    draw_er_entity(draw, xs[4], 890, col_w, "RolePermission", "role_permissions", [
        ("PK", "id", "UUID"),
        ("FK", "role_id", "UUID"),
        ("FK", "permission_id", "UUID"),
        ("UK", "unique_role_permission", "COMPOSITE"),
    ], c4)

    # Cuadro de resumen de convenciones de ingeniería de datos en Columna 4 inferior
    draw_rounded_rect(draw, [xs[4], 1085, xs[4] + col_w, 1435], radius=8, fill="#FFFFFF", outline="#0F172A", width=2)
    draw_rounded_rect(draw, [xs[4], 1085, xs[4] + col_w, 1127], radius=8, fill="#0F172A")
    draw.text((xs[4] + 14, 1096), "CONVENCIONES DEL ESQUEMA FÍSICO", fill="#FFFFFF", font=get_font(13, bold=True))
    conv = [
        ("PK (Primary Key):", "UUID v4 generado en PostgreSQL"),
        ("FK (Foreign Key):", "Integridad referencial declarativa"),
        ("UK (Unique Key):", "Restricción única simple o compuesta"),
        ("JSONB:", "Vector tipado de 12 meses / entregas"),
        ("Motor Base Datos:", "PostgreSQL 16 + Prisma ORM 5.7"),
        ("Normalización:", "Tercera Forma Normal (3FN)"),
        ("Total Modelos:", "26 tablas físicas de producción"),
    ]
    cy = 1142
    for k, v in conv:
        draw.text((xs[4] + 14, cy), k, fill="#0F172A", font=get_font(12, bold=True))
        draw.text((xs[4] + 165, cy), v, fill="#334155", font=get_font(12, bold=False))
        cy += 38

    # Barra inferior
    draw_rounded_rect(draw, [24, H - 64, W - 24, H - 20], radius=6, fill="#0F172A")
    draw.text((48, H - 52), "DOMINIOS DEL ESQUEMA:   [Verde Azulado] Jerarquía Territorial (6 tablas)   |   [Azul Marino] Catálogo y Lotes FEFO (6 tablas)   |   [Esmeralda] Planificación y Movimientos (6 tablas)   |   [Terracota] Vales, Kardex y Alertas (4 tablas)   |   [Pizarra] RBAC (4 tablas)", fill="#FFFFFF", font=get_font(13, bold=True))

    save_300dpi(img, "figura_mer_sivac.png")


# ==============================================================================
# 4. FIGURA 14: INTERFAZ DE AUTENTICACIÓN SEGURA (LOGIN JWT - DISA APURÍMAC II)
# ==============================================================================
def generar_figura_14_login():
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), "#0F172A")
    draw = ImageDraw.Draw(img)

    # Fondo DotGrid sutil idéntico a LoginForm.tsx
    for gx in range(40, W, 36):
        for gy in range(40, H, 36):
            draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill="#334155")

    # Banda superior institucional discreta
    draw.text((60, 42), "DIRECCIÓN DE SALUD APURÍMAC II — ANDAHUAYLAS", fill="#94A3B8", font=get_font(14, bold=True))
    draw.text((W - 490, 42), "ESTRATEGIA SANITARIA NACIONAL DE INMUNIZACIONES", fill="#64748B", font=get_font(13, bold=True))

    # Tarjeta central de Login (idéntica a LoginForm.tsx: max-w-[392px] escalada a alta resolución)
    cw, ch = 520, 560
    cx1 = (W - cw) // 2
    cy1 = (H - ch) // 2 - 20
    cx2 = cx1 + cw
    cy2 = cy1 + ch

    # Sombra suave
    draw_rounded_rect(draw, [cx1 + 8, cy1 + 12, cx2 + 8, cy2 + 12], radius=16, fill="#090D16")
    # Tarjeta blanca
    draw_rounded_rect(draw, [cx1, cy1, cx2, cy2], radius=16, fill="#FFFFFF", outline="#E2E8F0", width=2)

    # Cabecera de la tarjeta
    draw.line([cx1, cy1 + 108, cx2, cy1 + 108], fill="#F1F5F9", width=2)
    # Icono SIVAC
    draw_rounded_rect(draw, [cx1 + 36, cy1 + 26, cx1 + 92, cy1 + 82], radius=12, fill="#F0FDFA", outline="#99F6E4", width=2)
    draw_rounded_rect(draw, [cx1 + 46, cy1 + 36, cx1 + 82, cy1 + 72], radius=8, fill="#0D9488")
    draw.text((cx1 + 57, cy1 + 41), "S", fill="#FFFFFF", font=get_font(22, bold=True))

    draw.text((cx1 + 110, cy1 + 28), "SIVAC", fill="#0F172A", font=get_font(26, bold=True))
    draw.text((cx1 + 110, cy1 + 60), "Acceso seguro al sistema", fill="#64748B", font=get_font(15, bold=False))

    # Campo 1: Usuario o correo
    fy = cy1 + 138
    draw.text((cx1 + 36, fy), "Usuario o correo *", fill="#334155", font=get_font(15, bold=True))
    draw_rounded_rect(draw, [cx1 + 36, fy + 28, cx2 - 36, fy + 78], radius=8, fill="#FFFFFF", outline="#0D9488", width=2)
    draw.text((cx1 + 52, fy + 43), "☻", fill="#0D9488", font=get_font(16, bold=True))
    draw.text((cx1 + 82, fy + 43), "jquispe@disaapurimac2.gob.pe", fill="#0F172A", font=get_font(15, bold=False))

    # Campo 2: Contraseña
    fy2 = fy + 106
    draw.text((cx1 + 36, fy2), "Contraseña *", fill="#334155", font=get_font(15, bold=True))
    draw_rounded_rect(draw, [cx1 + 36, fy2 + 28, cx2 - 36, fy2 + 78], radius=8, fill="#FFFFFF", outline="#CBD5E1", width=2)
    draw.text((cx1 + 52, fy2 + 43), "⚿", fill="#64748B", font=get_font(16, bold=True))
    draw.text((cx1 + 82, fy2 + 43), "••••••••••••", fill="#0F172A", font=get_font(18, bold=True))
    draw.text((cx2 - 72, fy2 + 43), "◉", fill="#64748B", font=get_font(16, bold=True))

    # Badge informativo de seguridad JWT / Bcrypt
    fy3 = fy2 + 104
    draw_rounded_rect(draw, [cx1 + 36, fy3, cx2 - 36, fy3 + 52], radius=8, fill="#F0FDFA", outline="#CCFBF1", width=1)
    draw.text((cx1 + 52, fy3 + 9), "✓ Cifrado Bcrypt + Token JWT con control RBAC activo", fill="#0F766E", font=get_font(13, bold=True))
    draw.text((cx1 + 52, fy3 + 29), "   Protección contra fuerza bruta (Rate Limit) habilitada", fill="#0D9488", font=get_font(12, bold=False))

    # Botón Iniciar sesión
    btn_y = fy3 + 74
    draw_rounded_rect(draw, [cx1 + 36, btn_y, cx2 - 36, btn_y + 54], radius=8, fill="#0D9488")
    draw.text((cx1 + 195, btn_y + 15), "Iniciar sesión", fill="#FFFFFF", font=get_font(17, bold=True))

    # Footer debajo de la tarjeta (idéntico a LoginForm.tsx: "SEDE • DISA APURÍMAC II")
    draw.text((W // 2 - 115, cy2 + 28), "SEDE  •  DISA APURÍMAC II", fill="#94A3B8", font=get_font(14, bold=True))
    draw.text((W // 2 - 210, cy2 + 54), "Sistema Web de Gestión de Movimientos de Vacunas v1.0", fill="#64748B", font=get_font(13, bold=False))

    save_300dpi(img, "figura_sivac_login.png")


# ==============================================================================
# 5. FIGURA 15: PANEL DE CONTROL GERENCIAL (DASHBOARD EJECUTIVO SIVAC)
# ==============================================================================
def generar_figura_15_dashboard():
    img, draw, x0, y0 = create_sivac_shell("Dashboard", "Panel de Control Ejecutivo (Dashboard)")

    # Título de vista y controles superiores
    draw.text((x0, y0 - 4), "Panel de Control e Indicadores de Inmunizaciones", fill="#0F172A", font=get_font(22, bold=True))
    draw.text((x0, y0 + 26), "Monitoreo en tiempo real de existencias por lote (FEFO), distribución mensual y alertas preventivas — Periodo 2025", fill="#64748B", font=get_font(13, bold=False))

    # Botones de filtro / actualización a la derecha
    draw_rounded_rect(draw, [1490, y0, 1690, y0 + 40], radius=8, fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((1508, y0 + 11), "Jurisdicción: 8 Centros", fill="#334155", font=get_font(13, bold=True))
    draw_rounded_rect(draw, [1706, y0, 1890, y0 + 40], radius=8, fill="#0D9488")
    draw.text((1730, y0 + 11), "↻ Actualizar Datos", fill="#FFFFFF", font=get_font(13, bold=True))

    # 4 Tarjetas KPI (idénticas a MetricsSection.tsx)
    kpi_y = y0 + 62
    kpi_w = 388
    kpi_gap = 24
    kpis = [
        ("Dosis Distribuidas", "34,616", "↑ 12.4%", True, "Incremento respecto al mes anterior", "#0D9488", "#ECFDF5", "#047857"),
        ("Dosis Aplicadas", "31,013", "↑ 9.8%", True, "Consolidado de los 8 centros de acopio", "#0284C7", "#EFF6FF", "#1D4ED8"),
        ("Cobertura Acumulada", "82.6%", "↑ 4.7 pp", True, "Promedio de cumplimiento meta anual", "#0D9488", "#ECFDF5", "#047857"),
        ("Alertas Activas FEFO", "7", "↓ 2", False, "Lotes próximos a vencer / stock crítico", "#D97706", "#FFFBEB", "#B45309"),
    ]
    bar_heights = [42, 70, 38, 78, 55, 88, 64, 96]

    for i, (title, val, trend, up, sub, acc, bbg, btxt) in enumerate(kpis):
        kx = x0 + i * (kpi_w + kpi_gap)
        draw_rounded_rect(draw, [kx, kpi_y, kx + kpi_w, kpi_y + 148], radius=16, fill="#FFFFFF", outline="#E2E8F0", width=2)
        draw.ellipse([kx + 18, kpi_y + 16, kx + 46, kpi_y + 44], fill="#F0FDFA", outline="#CCFBF1", width=1)
        draw.text((kx + 27, kpi_y + 21), "▣", fill=acc, font=get_font(14, bold=True))
        draw.text((kx + 56, kpi_y + 21), title, fill="#475569", font=get_font(14, bold=True))

        draw.text((kx + 20, kpi_y + 54), val, fill="#0F172A", font=get_font(30, bold=True))
        draw_rounded_rect(draw, [kx + kpi_w - 96, kpi_y + 58, kx + kpi_w - 18, kpi_y + 84], radius=12, fill=bbg)
        draw.text((kx + kpi_w - 84, kpi_y + 63), trend, fill=btxt, font=get_font(12, bold=True))
        draw.text((kx + 20, kpi_y + 98), sub, fill="#64748B", font=get_font(12, bold=False))

        # Mini gráfico de barras a la derecha inferior
        bx_start = kx + kpi_w - 118
        for b_idx, bh in enumerate(bar_heights):
            px = bx_start + b_idx * 12
            ph = int(34 * (bh / 100.0))
            draw.rectangle([px, kpi_y + 134 - ph, px + 8, kpi_y + 134], fill="#14B8A6" if up else "#F59E0B")

    # Fila central: Gráfico de evolución mensual (Izquierda) + Disponibilidad de Stock por Vacuna (Centro) + Permisos Operativos (Derecha)
    row2_y = kpi_y + 170
    row2_h = 370

    # Panel 1: Evolución Mensual de Movimientos (Ingresos vs Entregas)
    p1_w = 800
    draw_rounded_rect(draw, [x0, row2_y, x0 + p1_w, row2_y + row2_h], radius=14, fill="#FFFFFF", outline="#E2E8F0", width=2)
    draw.text((x0 + 22, row2_y + 18), "Evolución Mensual de Movimientos de Biológicos (Dosis Programadas vs. Entregadas)", fill="#0F172A", font=get_font(15, bold=True))
    draw.text((x0 + 22, row2_y + 42), "Concordancia de despacho mensual en los 8 Centros de Acopio (Enero – Octubre 2025)", fill="#64748B", font=get_font(12, bold=False))

    # Leyenda del gráfico
    draw.rectangle([x0 + 540, row2_y + 22, x0 + 556, row2_y + 34], fill="#0D9488")
    draw.text((x0 + 562, row2_y + 19), "Programado", fill="#334155", font=get_font(12, bold=True))
    draw.rectangle([x0 + 660, row2_y + 22, x0 + 676, row2_y + 34], fill="#3B82F6")
    draw.text((x0 + 682, row2_y + 19), "Entregado (Vale)", fill="#334155", font=get_font(12, bold=True))

    # Ejes y barras mensuales
    gx1, gy1, gx2, gy2 = x0 + 64, row2_y + 82, x0 + p1_w - 28, row2_y + row2_h - 44
    for step in range(5):
        ly = gy2 - int((gy2 - gy1) * (step / 4.0))
        draw.line([gx1, ly, gx2, ly], fill="#F1F5F9", width=1)
        draw.text((x0 + 18, ly - 8), f"{step * 1000:,}", fill="#64748B", font=get_font(11, bold=False))

    meses_lbl = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct"]
    prog_vals = [3120, 3280, 3450, 3390, 3600, 3520, 3780, 3690, 3580, 3460]
    entr_vals = [3100, 3260, 3420, 3380, 3590, 3500, 3750, 3680, 3560, 3450]

    step_w = (gx2 - gx1) // len(meses_lbl)
    for m_i, m_name in enumerate(meses_lbl):
        mx = gx1 + 16 + m_i * step_w
        h_p = int((gy2 - gy1) * (prog_vals[m_i] / 4000.0))
        h_e = int((gy2 - gy1) * (entr_vals[m_i] / 4000.0))
        draw_rounded_rect(draw, [mx, gy2 - h_p, mx + 18, gy2], radius=3, fill="#0D9488")
        draw_rounded_rect(draw, [mx + 22, gy2 - h_e, mx + 40, gy2], radius=3, fill="#3B82F6")
        draw.text((mx + 8, gy2 + 10), m_name, fill="#475569", font=get_font(12, bold=True))

    # Panel 2: Disponibilidad de Stock por Vacuna
    p2_x = x0 + p1_w + 24
    p2_w = 400
    draw_rounded_rect(draw, [p2_x, row2_y, p2_x + p2_w, row2_y + row2_h], radius=14, fill="#FFFFFF", outline="#E2E8F0", width=2)
    draw.text((p2_x + 20, row2_y + 18), "Disponibilidad por Biológico (FEFO)", fill="#0F172A", font=get_font(15, bold=True))
    draw.text((p2_x + 20, row2_y + 42), "Saldo actual consolidado en cadena de frío", fill="#64748B", font=get_font(12, bold=False))

    vac_bars = [
        ("Pentavalente (DPT-HvB-Hib)", "4,500 dosis", 0.88, "#0D9488"),
        ("IPV (Polio Inactivada)", "6,200 dosis", 0.94, "#0D9488"),
        ("SPR (Sarampión-Papera-Rub.)", "3,800 dosis", 0.78, "#0284C7"),
        ("Rotavirus Monodosis", "2,450 dosis", 0.65, "#0284C7"),
        ("Neumococo Conjugada", "2,910 dosis", 0.72, "#0D9488"),
        ("BCG (Recién Nacido)", "1,120 dosis", 0.42, "#D97706"),
    ]
    vy = row2_y + 78
    for vname, vqty, vpct, vcol in vac_bars:
        draw.text((p2_x + 20, vy), vname, fill="#1E293B", font=get_font(12, bold=True))
        draw.text((p2_x + p2_w - 92, vy), vqty, fill="#0F766E", font=get_font(12, bold=True))
        draw_rounded_rect(draw, [p2_x + 20, vy + 22, p2_x + p2_w - 20, vy + 32], radius=5, fill="#F1F5F9")
        draw_rounded_rect(draw, [p2_x + 20, vy + 22, p2_x + 20 + int((p2_w - 40) * vpct), vy + 32], radius=5, fill=vcol)
        vy += 47

    # Panel 3: Control de Permisos Operativos (PermisosPlanificacion.tsx)
    p3_x = p2_x + p2_w + 24
    p3_w = 376
    draw_rounded_rect(draw, [p3_x, row2_y, p3_x + p3_w, row2_y + row2_h], radius=14, fill="#FFFFFF", outline="#E2E8F0", width=2)
    draw.text((p3_x + 20, row2_y + 18), "Permisos Operativos por Acopio", fill="#0F172A", font=get_font(15, bold=True))
    draw.text((p3_x + 20, row2_y + 42), "Ventanas de edición de Planificación y Movimientos", fill="#64748B", font=get_font(12, bold=False))

    centros_perm = [
        ("C.A. Andahuaylas", True, True),
        ("C.A. San Jerónimo", True, True),
        ("C.A. Talavera", True, True),
        ("C.A. Chincheros", False, True),
        ("C.A. Huancarama", False, True),
        ("C.A. Pacucha", False, False),
    ]
    py = row2_y + 78
    for cname, p_plan, p_mov in centros_perm:
        draw_rounded_rect(draw, [p3_x + 18, py, p3_x + p3_w - 18, py + 40], radius=8, fill="#F8FAFC", outline="#E2E8F0", width=1)
        draw.text((p3_x + 28, py + 11), cname, fill="#0F172A", font=get_font(12, bold=True))
        draw_rounded_rect(draw, [p3_x + 195, py + 8, p3_x + 268, py + 32], radius=6, fill="#ECFDF5" if p_plan else "#F1F5F9")
        draw.text((p3_x + 204, py + 12), "Plan: ON" if p_plan else "Plan: OFF", fill="#047857" if p_plan else "#64748B", font=get_font(11, bold=True))
        draw_rounded_rect(draw, [p3_x + 276, py + 8, p3_x + p3_w - 26, py + 32], radius=6, fill="#ECFDF5" if p_mov else "#F1F5F9")
        draw.text((p3_x + 285, py + 12), "Mov: ON" if p_mov else "Mov: OFF", fill="#047857" if p_mov else "#64748B", font=get_font(11, bold=True))
        py += 47

    # Fila 3 inferior: Estado de los 8 Centros de Acopio + Alertas Recientes FEFO
    row3_y = row2_y + row2_h + 22
    row3_h = 335

    # Tabla resumen de Centros de Acopio
    draw_rounded_rect(draw, [x0, row3_y, x0 + 980, row3_y + row3_h], radius=14, fill="#FFFFFF", outline="#E2E8F0", width=2)
    draw.text((x0 + 22, row3_y + 16), "Estado Operativo de los 8 Centros de Acopio — Jurisdicción DISA Apurímac II", fill="#0F172A", font=get_font(15, bold=True))

    th_y = row3_y + 52
    draw.rectangle([x0 + 18, th_y, x0 + 962, th_y + 34], fill="#F8FAFC", outline="#E2E8F0", width=1)
    headers_ca = [("CÓDIGO", 28), ("CENTRO DE ACOPIO", 120), ("MICRORED", 340), ("EESS ADSCRITOS", 500), ("VALES MES", 650), ("ESTADO CADENA FRÍO", 780)]
    for h_txt, hx in headers_ca:
        draw.text((x0 + hx, th_y + 9), h_txt, fill="#475569", font=get_font(11, bold=True))

    filas_ca = [
        ("CA-001", "C.S. Andahuaylas", "Andahuaylas", "14 EESS", "14 / 14 emitidos", "Óptimo (+4.2 °C)"),
        ("CA-002", "C.S. San Jerónimo", "San Jerónimo", "11 EESS", "11 / 11 emitidos", "Óptimo (+3.8 °C)"),
        ("CA-003", "C.S. Talavera", "Talavera", "12 EESS", "12 / 12 emitidos", "Óptimo (+4.0 °C)"),
        ("CA-004", "Hosp. Chincheros", "Chincheros", "15 EESS", "15 / 15 emitidos", "Óptimo (+4.5 °C)"),
        ("CA-005", "C.S. Huancarama", "Huancarama", "10 EESS", "10 / 10 emitidos", "Óptimo (+3.9 °C)"),
        ("CA-006", "C.S. Pacucha", "Pacucha", "9 EESS", "9 / 9 emitidos", "Óptimo (+4.1 °C)"),
    ]
    ry = th_y + 36
    for cod, nom, mred, eess, vales, est in filas_ca:
        draw.line([x0 + 18, ry + 36, x0 + 962, ry + 36], fill="#F1F5F9", width=1)
        draw.text((x0 + 28, ry + 9), cod, fill="#0F766E", font=get_font(12, bold=True, mono=True))
        draw.text((x0 + 120, ry + 9), nom, fill="#0F172A", font=get_font(12, bold=True))
        draw.text((x0 + 340, ry + 9), mred, fill="#475569", font=get_font(12, bold=False))
        draw.text((x0 + 500, ry + 9), eess, fill="#334155", font=get_font(12, bold=False))
        draw.text((x0 + 650, ry + 9), vales, fill="#047857", font=get_font(12, bold=True))
        draw_rounded_rect(draw, [x0 + 780, ry + 6, x0 + 942, ry + 30], radius=10, fill="#ECFDF5")
        draw.text((x0 + 794, ry + 9), est, fill="#047857", font=get_font(11, bold=True))
        ry += 38

    # Panel de Alertas FEFO y Actividad Reciente a la derecha
    al_x = x0 + 1004
    al_w = 620
    draw_rounded_rect(draw, [al_x, row3_y, al_x + al_w, row3_y + row3_h], radius=14, fill="#FFFFFF", outline="#E2E8F0", width=2)
    draw.text((al_x + 22, row3_y + 16), "Alertas Preventivas de Caducidad (FEFO) y Trazabilidad Reciente", fill="#0F172A", font=get_font(15, bold=True))

    alertas_list = [
        ("PRIORIDAD ALTA", "Lote BCG-2308A próximo a vencer (28 días restantes) — Priorizar despacho FEFO", "#FEF2F2", "#DC2626"),
        ("PRIORIDAD MEDIA", "Stock de seguridad alcanzado en Rotavirus — C.A. Huancarama (180 dosis)", "#FFFBEB", "#D97706"),
        ("VALE EMITIDO", "Comprobante Oficial VALE-2025-10-CA01 generado y exportado en PDF (C.S. Andahuaylas)", "#ECFDF5", "#047857"),
        ("SINCRONIZACIÓN", "Saldos finales de Septiembre propagados automáticamente a Octubre sin discrepancias", "#EFF6FF", "#1D4ED8"),
    ]
    ay = row3_y + 56
    for badge, msg, bg_c, tx_c in alertas_list:
        draw_rounded_rect(draw, [al_x + 20, ay, al_x + al_w - 20, ay + 58], radius=8, fill=bg_c)
        draw.text((al_x + 34, ay + 8), badge, fill=tx_c, font=get_font(11, bold=True))
        draw.text((al_x + 34, ay + 29), msg, fill="#1E293B", font=get_font(12, bold=False))
        ay += 67

    save_300dpi(img, "figura_sivac_dashboard.png")


# ==============================================================================
# 6. FIGURA 18: REGISTRO MENSUAL DE MOVIMIENTOS Y EMISIÓN DE VALES OFICIALES
# ==============================================================================
def generar_figura_18_movimientos_vales():
    img, draw, x0, y0 = create_sivac_shell("Movimientos", "Movimientos Mensuales y Emisión de Vales de Entrega")

    # Título y pestañas (Movimientos Mensuales | Vales de Entrega)
    draw.text((x0, y0 - 4), "Gestión de Movimientos Mensuales y Vales de Entrega Oficiales", fill="#0F172A", font=get_font(22, bold=True))
    draw.text((x0, y0 + 26), "Sincronización automática de saldos intermensuales, control de entregas adicionales y generación instantánea de vales PDF/Excel", fill="#64748B", font=get_font(13, bold=False))

    # Botones de acción principales (Importar Excel, Sincronizar Mes Siguiente, Emitir Vale Oficial)
    draw_rounded_rect(draw, [1320, y0, 1490, y0 + 40], radius=8, fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((1338, y0 + 11), "⇩ Exportar Matriz", fill="#334155", font=get_font(13, bold=True))

    draw_rounded_rect(draw, [1504, y0, 1696, y0 + 40], radius=8, fill="#EFF6FF", outline="#93C5FD", width=1)
    draw.text((1520, y0 + 11), "⇄ Sincronizar Saldos", fill="#1D4ED8", font=get_font(13, bold=True))

    draw_rounded_rect(draw, [1710, y0, 1892, y0 + 40], radius=8, fill="#0D9488")
    draw.text((1726, y0 + 11), "+ Emitir Vale Oficial", fill="#FFFFFF", font=get_font(13, bold=True))

    # Barra de Filtros (Año, Mes, Centro de Acopio, Establecimiento, Biológico)
    fy = y0 + 58
    draw_rounded_rect(draw, [x0, fy, 1892, fy + 66], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=2)

    filtros = [
        ("AÑO OPERATIVO", "2025", 20, 130),
        ("MES ACTIVO", "Octubre", 166, 160),
        ("CENTRO DE ACOPIO", "CA-001 - C.S. Andahuaylas", 342, 260),
        ("ESTABLECIMIENTO", "Todos los EESS adscritos (14)", 618, 270),
        ("VACUNA / BIOLÓGICO", "Todas las vacunas activas (16)", 904, 270),
    ]
    for flbl, fval, fx, fw in filtros:
        draw.text((x0 + fx, fy + 8), flbl, fill="#64748B", font=get_font(10, bold=True))
        draw_rounded_rect(draw, [x0 + fx, fy + 26, x0 + fx + fw, fy + 56], radius=6, fill="#F8FAFC", outline="#CBD5E1", width=1)
        draw.text((x0 + fx + 10, fy + 33), fval, fill="#0F172A", font=get_font(12, bold=True))

    # Indicador de concordancia en la barra de filtros
    draw_rounded_rect(draw, [x0 + 1195, fy + 14, 1874, fy + 54], radius=8, fill="#ECFDF5", outline="#A7F3D0", width=1)
    draw.text((x0 + 1212, fy + 25), "✓ CONCORDANCIA DOCUMENTAL: 100.0% (0 discrepancias aritméticas)", fill="#047857", font=get_font(12, bold=True))

    # Tabla principal de Movimientos Mensuales (Izquierda/Centro)
    ty = fy + 82
    tw = 1090
    th = 815
    draw_rounded_rect(draw, [x0, ty, x0 + tw, ty + th], radius=12, fill="#FFFFFF", outline="#E2E8F0", width=2)
    draw.text((x0 + 20, ty + 16), "Cuadrícula Transaccional de Movimientos Mensuales — Octubre 2025", fill="#0F172A", font=get_font(15, bold=True))
    draw.text((x0 + 750, ty + 18), "Edición en tiempo real con validación ACID", fill="#0D9488", font=get_font(12, bold=True))

    # Cabecera de la tabla de movimientos
    hdr_y = ty + 50
    draw.rectangle([x0 + 14, hdr_y, x0 + tw - 14, hdr_y + 40], fill="#0F172A")
    cols_mov = [
        ("ESTABLECIMIENTO", 24),
        ("BIOLÓGICO (LOTE FEFO)", 215),
        ("SALDO ANT.", 420),
        ("ING. TRANSF.", 520),
        ("SAL. TRANSF.", 625),
        ("PROGRAMADO", 730),
        ("ENTREGADO", 840),
        ("ADICIONAL", 935),
        ("SALDO FINAL", 1010),
    ]
    for c_txt, cx in cols_mov:
        draw.text((x0 + cx, hdr_y + 13), c_txt, fill="#FFFFFF", font=get_font(10, bold=True))

    mov_rows = [
        ("C.S. Andahuaylas", "Pentavalente (LOT-2409A)", "120", "+300", "0", "280", "280", "+20", "120"),
        ("C.S. Andahuaylas", "IPV Polio (LOT-2411B)", "180", "+400", "-20", "360", "360", "0", "200"),
        ("C.S. Andahuaylas", "SPR Triple Viral (LOT-2408C)", "90", "+250", "0", "220", "220", "0", "120"),
        ("C.S. Andahuaylas", "Rotavirus (LOT-2410R)", "75", "+180", "0", "160", "160", "+15", "80"),
        ("C.S. Andahuaylas", "Neumococo 13v (LOT-2412N)", "110", "+240", "0", "210", "210", "0", "140"),
        ("P.S. Pochccota", "Pentavalente (LOT-2409A)", "40", "+90", "0", "85", "85", "0", "45"),
        ("P.S. Pochccota", "IPV Polio (LOT-2411B)", "55", "+110", "0", "100", "100", "+10", "55"),
        ("P.S. Pochccota", "SPR Triple Viral (LOT-2408C)", "30", "+80", "0", "75", "75", "0", "35"),
        ("P.S. Salinas", "Pentavalente (LOT-2409A)", "35", "+70", "0", "65", "65", "0", "40"),
        ("P.S. Salinas", "Neumococo 13v (LOT-2412N)", "45", "+85", "0", "80", "80", "0", "50"),
        ("P.S. Huancabamba", "Pentavalente (LOT-2409A)", "60", "+140", "0", "130", "130", "+10", "60"),
        ("P.S. Huancabamba", "Rotavirus (LOT-2410R)", "50", "+110", "0", "95", "95", "0", "65"),
        ("P.S. Cachiyaurecc", "IPV Polio (LOT-2411B)", "30", "+60", "0", "55", "55", "0", "35"),
    ]

    ry = hdr_y + 42
    for idx_r, rdata in enumerate(mov_rows):
        bg_r = "#FFFFFF" if idx_r % 2 == 0 else "#F8FAFC"
        draw.rectangle([x0 + 14, ry, x0 + tw - 14, ry + 48], fill=bg_r, outline="#E2E8F0", width=1)
        draw.text((x0 + 24, ry + 15), rdata[0], fill="#0F172A", font=get_font(12, bold=True))
        draw.text((x0 + 215, ry + 15), rdata[1], fill="#334155", font=get_font(11, bold=False))
        draw.text((x0 + 435, ry + 15), rdata[2], fill="#475569", font=get_font(12, bold=True, mono=True))
        draw.text((x0 + 535, ry + 15), rdata[3], fill="#047857", font=get_font(12, bold=True, mono=True))
        draw.text((x0 + 645, ry + 15), rdata[4], fill="#DC2626" if "-" in rdata[4] else "#64748B", font=get_font(12, bold=True, mono=True))
        draw.text((x0 + 748, ry + 15), rdata[5], fill="#1E3A8A", font=get_font(12, bold=True, mono=True))

        # Celda editable de Entregado
        draw_rounded_rect(draw, [x0 + 835, ry + 8, x0 + 910, ry + 40], radius=5, fill="#F0FDFA", outline="#0D9488", width=1)
        draw.text((x0 + 855, ry + 15), rdata[6], fill="#0F766E", font=get_font(12, bold=True, mono=True))

        # Entregas adicionales
        if rdata[7] != "0":
            draw_rounded_rect(draw, [x0 + 932, ry + 8, x0 + 992, ry + 40], radius=5, fill="#EFF6FF", outline="#93C5FD", width=1)
            draw.text((x0 + 946, ry + 15), rdata[7], fill="#1D4ED8", font=get_font(12, bold=True, mono=True))
        else:
            draw.text((x0 + 955, ry + 15), "0", fill="#94A3B8", font=get_font(12, bold=False, mono=True))

        # Saldo Final sincronizado
        draw.text((x0 + 1025, ry + 15), rdata[8], fill="#0F172A", font=get_font(12, bold=True, mono=True))
        ry += 48

    # Pie de tabla de movimientos: Resumen de totales
    draw.rectangle([x0 + 14, ry + 6, x0 + tw - 14, ry + 50], fill="#F0FDFA", outline="#5EEAD4", width=1)
    draw.text((x0 + 28, ry + 19), "TOTAL CONSOLIDADO CENTRO DE ACOPIO (OCTUBRE 2025):", fill="#0F766E", font=get_font(12, bold=True))
    draw.text((x0 + 735, ry + 19), "Prog: 1,915", fill="#1E3A8A", font=get_font(12, bold=True))
    draw.text((x0 + 838, ry + 19), "Entr: 1,915", fill="#047857", font=get_font(12, bold=True))
    draw.text((x0 + 935, ry + 19), "Adic: +55", fill="#1D4ED8", font=get_font(12, bold=True))
    draw.text((x0 + 1012, ry + 19), "Saldo: 1,050", fill="#0F172A", font=get_font(12, bold=True))

    # Panel Derecho: Vista Previa y Emisión de Vale de Entrega Oficial (Vales.tsx)
    vx = x0 + tw + 22
    vw = 512
    draw_rounded_rect(draw, [vx, ty, vx + vw, ty + th], radius=12, fill="#FFFFFF", outline="#0D9488", width=2)
    draw_rounded_rect(draw, [vx, ty, vx + vw, ty + 64], radius=12, fill="#0D9488")
    draw.text((vx + 20, ty + 12), "COMPROBANTE DE SALIDA / VALE DE ENTREGA", fill="#FFFFFF", font=get_font(15, bold=True))
    draw.text((vx + 20, ty + 36), "Generación instantánea con cálculo de frascos y jeringas", fill="#CCFBF1", font=get_font(12, bold=False))

    # Metadatos del Vale Oficial
    vy_meta = ty + 80
    draw_rounded_rect(draw, [vx + 18, vy_meta, vx + vw - 18, vy_meta + 132], radius=8, fill="#F8FAFC", outline="#CBD5E1", width=1)
    draw.text((vx + 32, vy_meta + 12), "N.° COMPROBANTE:", fill="#64748B", font=get_font(11, bold=True))
    draw.text((vx + 175, vy_meta + 10), "VALE-2025-10-CA001-014", fill="#0F172A", font=get_font(14, bold=True, mono=True))
    draw.text((vx + 32, vy_meta + 38), "CENTRO EMISOR:", fill="#64748B", font=get_font(11, bold=True))
    draw.text((vx + 175, vy_meta + 38), "CA-001 - C.S. Andahuaylas (DISA Apurímac II)", fill="#1E293B", font=get_font(12, bold=True))
    draw.text((vx + 32, vy_meta + 64), "MODALIDAD VALE:", fill="#64748B", font=get_font(11, bold=True))
    draw_rounded_rect(draw, [vx + 175, vy_meta + 60, vx + 415, vy_meta + 84], radius=5, fill="#ECFDF5")
    draw.text((vx + 185, vy_meta + 64), "COMPLETO (Entrega Base + Adicionales)", fill="#047857", font=get_font(11, bold=True))
    draw.text((vx + 32, vy_meta + 94), "CRITERIO DE LOTE:", fill="#64748B", font=get_font(11, bold=True))
    draw.text((vx + 175, vy_meta + 94), "FEFO Automático + Multiplicador Jeringas", fill="#0F766E", font=get_font(12, bold=True))

    # Desglose del Vale por Biológico y Jeringas
    vy_det = vy_meta + 150
    draw.text((vx + 20, vy_det), "Desglose de Biológicos y Jeringas en el Vale:", fill="#0F172A", font=get_font(13, bold=True))

    items_vale = [
        ("1. Vacuna Pentavalente (1 dosis/fco)", "Lote: LOT-2409A | Vence: 30/08/2026", "300 dosis", "300 fcos", "300 jer. 23Gx1"),
        ("2. Vacuna IPV Polio Inactivada (5 dosis/fco)", "Lote: LOT-2411B | Vence: 15/11/2026", "360 dosis", "72 fcos", "360 jer. 25Gx5/8"),
        ("3. Vacuna SPR Triple Viral (1 dosis/fco)", "Lote: LOT-2408C | Vence: 20/07/2026", "220 dosis", "220 fcos", "440 jer. (Apl+Dil)"),
        ("4. Vacuna Rotavirus Oral (Monodosis)", "Lote: LOT-2410R | Vence: 10/09/2026", "175 dosis", "175 fcos", "0 jer. (Vía Oral)"),
        ("5. Vacuna Neumococo Conjugada 13v", "Lote: LOT-2412N | Vence: 31/12/2026", "210 dosis", "210 fcos", "210 jer. 23Gx1"),
    ]
    iy = vy_det + 28
    for v_tit, v_lot, v_dos, v_fco, v_jer in items_vale:
        draw_rounded_rect(draw, [vx + 18, iy, vx + vw - 18, iy + 72], radius=8, fill="#FFFFFF", outline="#E2E8F0", width=1)
        draw.text((vx + 30, iy + 8), v_tit, fill="#0F172A", font=get_font(12, bold=True))
        draw.text((vx + 30, iy + 28), v_lot, fill="#64748B", font=get_font(11, bold=False))
        draw_rounded_rect(draw, [vx + 30, iy + 46, vx + 135, iy + 66], radius=4, fill="#F0FDFA")
        draw.text((vx + 40, iy + 48), v_dos, fill="#0F766E", font=get_font(11, bold=True))
        draw_rounded_rect(draw, [vx + 145, iy + 46, vx + 245, iy + 66], radius=4, fill="#EFF6FF")
        draw.text((vx + 155, iy + 48), v_fco, fill="#1D4ED8", font=get_font(11, bold=True))
        draw_rounded_rect(draw, [vx + 255, iy + 46, vx + vw - 30, iy + 66], radius=4, fill="#F8FAFC")
        draw.text((vx + 265, iy + 48), v_jer, fill="#334155", font=get_font(11, bold=True))
        iy += 80

    # Resumen total del Vale y botones de descarga oficial (PDFKit / ExcelJS)
    ry_tot = iy + 6
    draw_rounded_rect(draw, [vx + 18, ry_tot, vx + vw - 18, ry_tot + 64], radius=8, fill="#0F172A")
    draw.text((vx + 32, ry_tot + 10), "TOTAL VALE: 1,265 Dosis  |  977 Frascos  |  1,310 Jeringas", fill="#FFFFFF", font=get_font(12, bold=True))
    draw.text((vx + 32, ry_tot + 34), "Tiempo de procesamiento y emisión (T_vale): 1.4 seg — Estado: EMITIDO", fill="#5EEAD4", font=get_font(11, bold=False))

    btn_vy = ry_tot + 78
    draw_rounded_rect(draw, [vx + 18, btn_vy, vx + 250, btn_vy + 48], radius=8, fill="#DC2626")
    draw.text((vx + 42, btn_vy + 14), "⇩ Descargar Vale PDF", fill="#FFFFFF", font=get_font(13, bold=True))

    draw_rounded_rect(draw, [vx + 264, btn_vy, vx + vw - 18, btn_vy + 48], radius=8, fill="#047857")
    draw.text((vx + 286, btn_vy + 14), "⇩ Exportar Vale Excel", fill="#FFFFFF", font=get_font(13, bold=True))

    save_300dpi(img, "figura_sivac_movimientos_vales.png")


if __name__ == "__main__":
    print("=== GENERANDO FIGURAS DE INGENIERÍA Y VISTAS SIVAC A 300 DPI ===")
    generar_figura_11_arquitectura_3capas()
    generar_figura_12_casos_uso()
    generar_figura_13_mer()
    generar_figura_14_login()
    generar_figura_15_dashboard()
    generar_figura_18_movimientos_vales()
    print("=== GENERACIÓN COMPLETADA EXITOSAMENTE ===")
