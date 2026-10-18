#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - Squad B (Metodologia y Psicometria)
GENERADOR DE MATRIZ AUTOMATIZADA DE CALCULO DE IVC Y V DE AIKEN
Modelo Metodologico Institucional: certificado Fany 2024 (DEC-015)
================================================================================
Genera el libro Excel automatizado en:
salidas/instrumentos/MATRIZ_CALCULO_IVC_AIKEN_SIVAC.xlsx

Alcance: un solo instrumento (DEC-020). El certificado de validez de contenido
cubre exclusivamente los 8 items de la Modalidad A del Instrumento N. 03
(AP-01 a AP-04 y UP-01 a UP-04). Los Instrumentos N. 01 y N. 02 no se someten a
juicio de contenido; su validez se sustenta en el protocolo de medicion de
movimientos de vacunas, en el ICC(2,1) y en el kappa de Cohen.

Criterios: tres, dicotomicos Si/No (Pertinencia, Relevancia y Claridad), con
1 = Si y 0 = No. Con c = 2 y n = 3 jueces, V = S / [n(c-1)] se reduce a V = S/n,
de modo que V solo puede tomar los valores 0.000, 0.333, 0.667 y 1.000.

Atribucion y umbral: Tristán-López (2008) fija, para tres jueces, un minimo por
item de 0.5823 (0.58). El umbral de 0.80 que aplica esta matriz no proviene de
esa fuente: es un criterio propio del presente estudio, mas estricto que el de
Tristán-López, y asi debe declararse en el informe. Con c = 2 y n = 3, ese
umbral propio exige unanimidad perfecta de los tres jueces en cada item.

Incluye:
1. Hoja "Matriz_IVC_Detallada": Registro de calificaciones por criterio para los
   3 jueces expertos independientes, con formulas nativas:
   - Codificacion binaria: =IF(celda=1, 1, 0)
   - Suma de acuerdos: =SUM(rango)
   - IVC por criterio: =Suma/3
   - V de Aiken por criterio: =S/(3*(2-1)) = S/3
2. Hoja "Resumen_Consolidado": Sintesis por item e instrumento con formulas:
   - IVC del item: =AVERAGE(criterios)
   - V de Aiken del item: =AVERAGE(criterios)
   - Intervalos de confianza Wilson al 95 % con N = n(c-1) = 3
   - Umbrales de 0.80 para IVC y V, con dictamen general.
3. Hoja "Fundamento_y_Baremos": Marco teorico, formulas canonicas y criterios.

Las calificaciones NO se precargan: deben provenir de los formatos Fany 2024
aplicados por los jueces reales (DEC-014 y DEC-016).
================================================================================
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Ítems oficiales del Instrumento N. 03, Modalidad A (DEC-019 y DEC-020).
# Son los únicos 8 ítems que reciben certificado de validez de contenido.
ITEMS_MODALIDAD_A = [
    ("AP-01", "El procedimiento para registrar movimientos diarios y cierres no demanda esfuerzo excesivo", "Satisfacción del usuario", "Aceptación del proceso (AP)"),
    ("AP-02", "El flujo de trabajo para emitir vales de entrega es fluido y libre de trabas burocráticas", "Satisfacción del usuario", "Aceptación del proceso (AP)"),
    ("AP-03", "El método permite conciliar saldos con microredes reduciendo estrés e incertidumbre", "Satisfacción del usuario", "Aceptación del proceso (AP)"),
    ("AP-04", "El tiempo dedicado al registro deja disponibilidad para tareas sanitarias y asistenciales", "Satisfacción del usuario", "Aceptación del proceso (AP)"),
    ("UP-01", "El mecanismo permite disponer de información fidedigna y en tiempo real del stock", "Satisfacción del usuario", "Utilidad percibida (UP)"),
    ("UP-02", "El control de lotes y vencimientos previene oportunamente mermas y pérdidas de biológicos", "Satisfacción del usuario", "Utilidad percibida (UP)"),
    ("UP-03", "Facilita la detección inmediata y rectificación de cualquier descuadre de existencias", "Satisfacción del usuario", "Utilidad percibida (UP)"),
    ("UP-04", "En general, es una herramienta altamente eficaz para asegurar el abastecimiento de vacunas", "Satisfacción del usuario", "Utilidad percibida (UP)"),
]

CRITERIOS = [
    "Pertinencia",
    "Relevancia",
    "Claridad",
]

N_JUECES = 3
C_CATEGORIAS = 2
# ATRIBUCION DEL UMBRAL: Tristán-López (2008) fija, para tres jueces, un minimo
# por item de 0.5823 (0.58). El 0.80 es criterio propio del presente estudio,
# mas estricto que el de la fuente, y no se le atribuye a Tristán-López.
#
# ADVERTENCIA ARITMETICA: con c = 2 y n = 3, V = S / [n(c-1)] = S / 3. V solo
# alcanza 0.000, 0.333, 0.667 y 1.000; el umbral propio de 0.80 equivale a
# unanimidad perfecta de los tres jueces en cada item. No es un defecto: es la
# consecuencia aritmetica del modelo dicotomico Fany 2024 (DEC-015).
UMBRAL_IVC = 0.80
UMBRAL_V = 0.80


def construir_libro_excel(ruta_salida, calificaciones):
    """Construye el libro a partir de calificaciones reales de los jueces.

    calificaciones: dict codigo_item -> lista de 3 tuplas, una por criterio
    (Pertinencia, Relevancia, Claridad), cada tupla con la marca 0 (No) o 1 (Si)
    de cada uno de los 3 jueces. Ejemplo: {"AP-01": [(1, 1, 1), (1, 1, 0), (1, 1, 1)]}.
    """
    if not calificaciones:
        raise ValueError(
            "Sin calificaciones reales de los jueces no se construye la matriz "
            "(DEC-014 y Regla Canónica 01, sección 3)."
        )
    faltantes = [cod for cod, *_ in ITEMS_MODALIDAD_A if cod not in calificaciones]
    if faltantes:
        raise ValueError(
            f"Faltan las calificaciones de los ítems {faltantes}. El certificado "
            "cubre los 8 ítems de la Modalidad A del Instrumento N. 03 (DEC-020)."
        )
    for cod, *_ in ITEMS_MODALIDAD_A:
        filas_crit = calificaciones[cod]
        if len(filas_crit) != len(CRITERIOS):
            raise ValueError(f"{cod}: se esperaban {len(CRITERIOS)} criterios y hay {len(filas_crit)}.")
        for marcas in filas_crit:
            if len(marcas) != N_JUECES or any(m not in (0, 1) for m in marcas):
                raise ValueError(
                    f"{cod}: cada criterio requiere {N_JUECES} marcas dicotómicas 0 o 1 "
                    f"(recibido {marcas})."
                )

    wb = openpyxl.Workbook()
    ws_default = wb.active
    wb.remove(ws_default)

    AZUL_UNAJMA = "002060"
    AZUL_SECUNDARIO = "1F497D"
    GRIS_ENCABEZADO = "F2F2F2"
    VERDE_APROBADO = "E2EFDA"
    VERDE_TEXTO = "276A3C"
    BLANCO = "FFFFFF"

    font_titulo = Font(name="Times New Roman", size=13, bold=True, color=AZUL_UNAJMA)
    font_subtitulo = Font(name="Times New Roman", size=10, italic=True)
    font_header = Font(name="Times New Roman", size=10, bold=True, color=BLANCO)
    font_body = Font(name="Times New Roman", size=9)
    font_decision = Font(name="Times New Roman", size=9, bold=True, color=VERDE_TEXTO)

    fill_header_azul = PatternFill(start_color=AZUL_UNAJMA, end_color=AZUL_UNAJMA, fill_type="solid")
    fill_header_sec = PatternFill(start_color=AZUL_SECUNDARIO, end_color=AZUL_SECUNDARIO, fill_type="solid")
    fill_aprobado = PatternFill(start_color=VERDE_APROBADO, end_color=VERDE_APROBADO, fill_type="solid")
    fill_gris_suave = PatternFill(start_color="F9F9F9", end_color="F9F9F9", fill_type="solid")

    thin_border_side = Side(style="thin", color="D9D9D9")
    border_celda = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    # =========================================================================
    # HOJA 1: MATRIZ_IVC_DETALLADA
    # =========================================================================
    ws1 = wb.create_sheet(title="Matriz_IVC_Detallada")
    ws1.views.sheetView[0].showGridLines = True

    ws1["A1"] = "UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS - FACULTAD DE INGENIERÍA"
    ws1["A1"].font = font_titulo
    ws1["A2"] = "MATRIZ OFICIAL DE CÁLCULO DEL ÍNDICE DE VALIDEZ DE CONTENIDO (IVC) Y COEFICIENTE V DE AIKEN"
    ws1["A2"].font = Font(name="Times New Roman", size=11, bold=True, color=AZUL_SECUNDARIO)
    ws1["A3"] = ("PROYECTO: APLICACIÓN DEL SISTEMA SIVAC PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS "
                 "- DISA APURÍMAC II")
    ws1["A3"].font = font_subtitulo
    ws1["A4"] = ("Alcance: Instrumento N. 03, Modalidad A (DEC-020). Criterios dicotómicos Sí/No del modelo "
                 "Fany 2024 (DEC-015): 1 = Sí, 0 = No. Con c = 2 y n = 3, V = S/3.")
    ws1["A4"].font = font_subtitulo

    headers_ws1 = [
        ("A6", "Instrumento"),
        ("B6", "Código"),
        ("C6", "Ítem Evaluado"),
        ("D6", "Criterio"),
        ("E6", "Juez 1"),
        ("F6", "Juez 2"),
        ("G6", "Juez 3"),
        ("H6", "Cod. Bin\nJuez 1"),
        ("I6", "Cod. Bin\nJuez 2"),
        ("J6", "Cod. Bin\nJuez 3"),
        ("K6", "Suma\nAcuerdos"),
        ("L6", "IVC\nCriterio"),
        ("M6", "V Aiken\nCriterio"),
        ("N6", "Decisión Criterio\n(IVC >= 0.80)"),
    ]

    for coord, text in headers_ws1:
        c = ws1[coord]
        c.value = text
        c.font = font_header
        c.fill = fill_header_azul
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    ws1.row_dimensions[6].height = 32

    row_idx = 7
    mapa_filas_resumen = {}
    nombre_inst = "Inst. 03: Cuestionario TAM (Modalidad A)"
    for cod, desc, dim, ind in ITEMS_MODALIDAD_A:
        start_row_item = row_idx
        marcas_por_criterio = calificaciones[cod]

        for crit_idx, crit_nom in enumerate(CRITERIOS):
            s1, s2, s3 = marcas_por_criterio[crit_idx]
            r = row_idx

            ws1.cell(r, 1, nombre_inst)
            ws1.cell(r, 2, cod)
            ws1.cell(r, 3, desc)
            ws1.cell(r, 4, crit_nom)
            ws1.cell(r, 5, s1)
            ws1.cell(r, 6, s2)
            ws1.cell(r, 7, s3)

            # Codificacion binaria: 1 = Si, 0 = No
            ws1.cell(r, 8, f"=IF(E{r}=1, 1, 0)")
            ws1.cell(r, 9, f"=IF(F{r}=1, 1, 0)")
            ws1.cell(r, 10, f"=IF(G{r}=1, 1, 0)")

            # Suma de acuerdos y calculo de IVC por criterio
            ws1.cell(r, 11, f"=SUM(H{r}:J{r})")
            ws1.cell(r, 12, f"=K{r}/{N_JUECES}")

            # V de Aiken con c = 2 y n = 3: V = S / [n(c-1)] = S / 3
            ws1.cell(r, 13, f"=K{r}/({N_JUECES}*({C_CATEGORIAS}-1))")

            # Decisión por criterio: umbral institucional de 0.80
            ws1.cell(r, 14, f'=IF(L{r}>={UMBRAL_IVC}, "Válido", "Observado")')

            for col_c in range(1, 15):
                cel = ws1.cell(r, col_c)
                cel.font = font_body
                cel.border = border_celda
                if col_c in [1, 2, 4]:
                    cel.alignment = Alignment(horizontal="left", vertical="center")
                elif col_c == 3:
                    cel.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
                elif col_c in [5, 6, 7, 8, 9, 10, 11]:
                    cel.alignment = Alignment(horizontal="center", vertical="center")
                elif col_c in [12, 13]:
                    cel.alignment = Alignment(horizontal="center", vertical="center")
                    cel.number_format = "0.000"
                elif col_c == 14:
                    cel.alignment = Alignment(horizontal="center", vertical="center")
                    cel.font = font_decision

            row_idx += 1

        end_row_item = row_idx - 1
        mapa_filas_resumen[cod] = (nombre_inst, desc, dim, ind, start_row_item, end_row_item)

    # =========================================================================
    # HOJA 2: RESUMEN_CONSOLIDADO
    # =========================================================================
    ws2 = wb.create_sheet(title="Resumen_Consolidado")
    ws2.views.sheetView[0].showGridLines = True

    ws2["A1"] = "UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS - FACULTAD DE INGENIERÍA"
    ws2["A1"].font = font_titulo
    ws2["A2"] = "CONSOLIDADO PSICOMÉTRICO: ÍNDICE DE VALIDEZ DE CONTENIDO (IVC) Y COEFICIENTE V DE AIKEN"
    ws2["A2"].font = Font(name="Times New Roman", size=11, bold=True, color=AZUL_SECUNDARIO)
    ws2["A3"] = ("CRITERIOS DE ACEPTACIÓN: IVC >= 0.80 y V de Aiken >= 0.80, umbrales propios del "
                 "presente estudio, más estrictos que el mínimo de 0.5823 que fija Tristán-López (2008) "
                 "para tres jueces. Con c = 2 y n = 3, ambos umbrales exigen unanimidad de los tres "
                 "jueces en cada ítem.")
    ws2["A3"].font = font_subtitulo

    headers_ws2 = [
        ("A5", "N"),
        ("B5", "Código"),
        ("C5", "Instrumento Oficial"),
        ("D5", "Dimensión / Indicador"),
        ("E5", "Ítem Evaluado"),
        ("F5", "IVC Promedio\n(I-CVI)"),
        ("G5", "V de Aiken\nPromedio"),
        ("H5", "IC 95 % Inferior\n(Wilson)"),
        ("I5", "IC 95 % Superior\n(Wilson)"),
        ("J5", "Decisión Psicométrica\nInstitucional"),
        ("K5", "Veredicto Operativo"),
    ]

    for coord, text in headers_ws2:
        c = ws2[coord]
        c.value = text
        c.font = font_header
        c.fill = fill_header_sec
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    ws2.row_dimensions[5].height = 32

    r_res = 6
    item_num = 1
    n_ensayos = N_JUECES * (C_CATEGORIAS - 1)

    for cod, (nombre_inst, desc, dim, ind, s_row, e_row) in mapa_filas_resumen.items():
        ws2.cell(r_res, 1, item_num)
        ws2.cell(r_res, 2, cod)
        ws2.cell(r_res, 3, nombre_inst)
        ws2.cell(r_res, 4, f"{dim} / {ind}")
        ws2.cell(r_res, 5, desc)

        ws2.cell(r_res, 6, f"=AVERAGE(Matriz_IVC_Detallada!L{s_row}:L{e_row})")
        ws2.cell(r_res, 7, f"=AVERAGE(Matriz_IVC_Detallada!M{s_row}:M{e_row})")

        # Intervalo de Wilson al 95 % para V de Aiken con N = n(c-1) = 3
        ws2.cell(r_res, 8, f"=(2*{n_ensayos}*G{r_res} + 3.8416 - 1.96*SQRT(4*{n_ensayos}*G{r_res}*(1-G{r_res}) + 3.8416))/(2*({n_ensayos} + 3.8416))")
        ws2.cell(r_res, 9, f"=(2*{n_ensayos}*G{r_res} + 3.8416 + 1.96*SQRT(4*{n_ensayos}*G{r_res}*(1-G{r_res}) + 3.8416))/(2*({n_ensayos} + 3.8416))")

        # Decisión psicométrica con umbral único de 0.80
        ws2.cell(r_res, 10, f'=IF(AND(F{r_res}>={UMBRAL_IVC}, G{r_res}>={UMBRAL_V}), "VÁLIDO (unanimidad)", "OBSERVADO")')
        ws2.cell(r_res, 11, f'=IF(F{r_res}>={UMBRAL_IVC}, "Aplicable sin modificación", "Revisión mayor")')

        for c_idx in range(1, 12):
            cel = ws2.cell(r_res, c_idx)
            cel.font = font_body
            cel.border = border_celda
            if c_idx in [1, 2]:
                cel.alignment = Alignment(horizontal="center", vertical="center")
            elif c_idx in [3, 4]:
                cel.alignment = Alignment(horizontal="left", vertical="center")
            elif c_idx == 5:
                cel.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            elif c_idx in [6, 7, 8, 9]:
                cel.alignment = Alignment(horizontal="center", vertical="center")
                cel.number_format = "0.000"
            elif c_idx in [10, 11]:
                cel.alignment = Alignment(horizontal="center", vertical="center")
                cel.font = font_decision
                cel.fill = fill_aprobado

        r_res += 1
        item_num += 1

    r_total = r_res + 1
    ws2.merge_cells(start_row=r_total, start_column=1, end_row=r_total, end_column=5)
    c_tot = ws2.cell(r_total, 1, "PROMEDIO GLOBAL DEL INSTRUMENTO (S-CVI/Ave y V de Aiken total):")
    c_tot.font = Font(name="Times New Roman", size=10, bold=True, color=AZUL_UNAJMA)
    c_tot.alignment = Alignment(horizontal="right", vertical="center")

    c_ivc_tot = ws2.cell(r_total, 6, f"=AVERAGE(F6:F{r_res-1})")
    c_ivc_tot.font = Font(name="Times New Roman", size=10, bold=True)
    c_ivc_tot.number_format = "0.000"
    c_ivc_tot.alignment = Alignment(horizontal="center", vertical="center")

    c_v_tot = ws2.cell(r_total, 7, f"=AVERAGE(G6:G{r_res-1})")
    c_v_tot.font = Font(name="Times New Roman", size=10, bold=True)
    c_v_tot.number_format = "0.000"
    c_v_tot.alignment = Alignment(horizontal="center", vertical="center")

    c_ic_inf = ws2.cell(r_total, 8, f"=AVERAGE(H6:H{r_res-1})")
    c_ic_inf.font = Font(name="Times New Roman", size=9, bold=True)
    c_ic_inf.number_format = "0.000"
    c_ic_inf.alignment = Alignment(horizontal="center", vertical="center")

    c_ic_sup = ws2.cell(r_total, 9, f"=AVERAGE(I6:I{r_res-1})")
    c_ic_sup.font = Font(name="Times New Roman", size=9, bold=True)
    c_ic_sup.number_format = "0.000"
    c_ic_sup.alignment = Alignment(horizontal="center", vertical="center")

    ws2.cell(r_total, 10, f'=IF(AND(F{r_total}>={UMBRAL_IVC}, G{r_total}>={UMBRAL_V}), "VALIDEZ GLOBAL SUFICIENTE", "OBSERVADO")')
    ws2.cell(r_total, 10).font = Font(name="Times New Roman", size=10, bold=True, color=VERDE_TEXTO)
    ws2.cell(r_total, 10).alignment = Alignment(horizontal="center", vertical="center")
    ws2.cell(r_total, 10).fill = fill_aprobado

    ws2.cell(r_total, 11, "APLICABLE EN CAMPO")
    ws2.cell(r_total, 11).font = Font(name="Times New Roman", size=10, bold=True, color=VERDE_TEXTO)
    ws2.cell(r_total, 11).alignment = Alignment(horizontal="center", vertical="center")
    ws2.cell(r_total, 11).fill = fill_aprobado

    for c_i in range(1, 12):
        ws2.cell(r_total, c_i).border = Border(top=Side(style="medium", color=AZUL_UNAJMA), bottom=Side(style="double", color=AZUL_UNAJMA))

    # =========================================================================
    # HOJA 3: FUNDAMENTO_Y_BAREMOS
    # =========================================================================
    ws3 = wb.create_sheet(title="Fundamento_y_Baremos")
    ws3.views.sheetView[0].showGridLines = True

    ws3["A1"] = "MARCO PSICOMÉTRICO Y CRITERIOS DE DECISIÓN - JUICIO DE EXPERTOS UNAJMA"
    ws3["A1"].font = font_titulo
    ws3["A2"] = "MODELO VIGENTE: CERTIFICADO FANY 2024 (DEC-015) Y ALCANCE DE UN SOLO INSTRUMENTO (DEC-020)"
    ws3["A2"].font = Font(name="Times New Roman", size=11, bold=True, color=AZUL_SECUNDARIO)

    lineas_fundamento = [
        ("1. MODELO DE VALIDEZ DE CONTENIDO ADOPTADO: FANY 2024 (DEC-015)", True),
        ("El certificado vigente califica cada ítem con tres criterios dicotómicos: Pertinencia, Relevancia y Claridad,", False),
        ("cada uno con respuesta Sí o No. Se abandona la escala ordinal de cuatro categorías y los cinco criterios del", False),
        ("modelo Cóndor Tinoco, superado por DEC-015 y archivado en cuarentena.", False),
        ("a) Codificación: 1 = Sí (acuerdo favorable) y 0 = No (acuerdo desfavorable).", False),
        ("b) IVC por criterio (IVC_ik): número de marcas Sí dividido entre N = 3 jueces.", False),
        ("c) IVC por ítem (I-CVI_i): promedio aritmético de los IVC de los 3 criterios.", False),
        ("d) IVC total del instrumento (S-CVI/Ave): promedio aritmético de los I-CVI de los 8 ítems.", False),
        ("e) Alcance: solo el Instrumento N. 03, Modalidad A (AP-01 a AP-04 y UP-01 a UP-04). Los Instrumentos", False),
        ("   N. 01 y N. 02 no se someten a juicio de contenido (DEC-020).", False),
        ("", False),
        ("2. COEFICIENTE V DE AIKEN Y LÍMITES DE WILSON AL 95 %", True),
        ("a) Coeficiente V de Aiken (1985): V = S / [ n * (c - 1) ], con S = Suma(s_j - l), l = 0 (mínimo),", False),
        ("   c = 2 (categorías) y n = 3 (jueces). La fórmula se reduce a V = S / 3.", False),
        ("b) Valores alcanzables: con n = 3, V solo puede tomar 0.000, 0.333, 0.667 y 1.000. El umbral de 0.80", False),
        ("   exige unanimidad perfecta de los tres jueces en cada ítem. No es un defecto: es la consecuencia", False),
        ("   aritmética del modelo dicotómico y debe declararse así en el informe.", False),
        ("c) Intervalo de confianza asintótico de Wilson al 95 % (Penfield y Giacobbi, 2004):", False),
        ("   L = [ 2*N*V + z^2 - z*sqrt(4*N*V*(1-V) + z^2) ] / [ 2*(N + z^2) ]", False),
        ("   U = [ 2*N*V + z^2 + z*sqrt(4*N*V*(1-V) + z^2) ] / [ 2*(N + z^2) ]", False),
        ("   donde N = n * (c - 1) = 3 ensayos y z = 1.96.", False),
        ("", False),
        ("3. UMBRALES DE ACEPTABILIDAD Y ATRIBUCIÓN", True),
        ("Para N = 3 jueces evaluadores independientes:", False),
        ("- Mínimo por ítem fijado por Tristán-López (2008) para tres jueces: 0.5823 (0.58).", False),
        ("- Umbral adoptado por el presente estudio: IVC >= 0.80, criterio propio y más estricto que el", False),
        ("   de la fuente; no se atribuye a Tristán-López. Equivale a 3 de 3 marcas Sí.", False),
        ("- Si IVC < 0.80: el ítem se reformula sustancialmente o se elimina.", False),
        ("- Umbral institucional global: IVC_total >= 0.80 (requisito para dictamen de aplicable).", False),
        ("- Coeficiente V de Aiken global: V >= 0.80 (unanimidad inter-jueces).", False),
    ]

    r_f = 4
    for txt, es_titulo in lineas_fundamento:
        c = ws3.cell(r_f, 1, txt)
        if es_titulo:
            c.font = Font(name="Times New Roman", size=10, bold=True, color=AZUL_UNAJMA)
            c.fill = fill_gris_suave
        else:
            c.font = font_body
        r_f += 1

    for ws in [ws1, ws2, ws3]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or "")
                if "\n" in val_str:
                    lines = val_str.split("\n")
                    max_len = max(max_len, max(len(l) for l in lines))
                else:
                    max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 10), 46)

    ws1.column_dimensions["A"].width = 34
    ws1.column_dimensions["B"].width = 12
    ws1.column_dimensions["C"].width = 45
    ws1.column_dimensions["D"].width = 14

    ws2.column_dimensions["A"].width = 6
    ws2.column_dimensions["B"].width = 12
    ws2.column_dimensions["C"].width = 34
    ws2.column_dimensions["D"].width = 28
    ws2.column_dimensions["E"].width = 48
    ws2.column_dimensions["J"].width = 26
    ws2.column_dimensions["K"].width = 25

    ws3.column_dimensions["A"].width = 110

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    wb.save(ruta_salida)
    print(f"[OK] Archivo Excel generado en: {ruta_salida}")


if __name__ == "__main__":
    # ---------------------------------------------------------------------
    # BLOQUEADO POR DEC-014 (2026-10-18)
    #
    # Esta matriz prellenaba las calificaciones de los tres jueces expertos y
    # calculaba sobre ellas el IVC y la V de Aiken. Los jueces no evaluaron los
    # instrumentos, de modo que toda cifra producida por este script carece de
    # respaldo empirico (Regla Canonica 01, seccion 3).
    #
    # La matriz original se conserva en cuarentena en:
    #   salidas/archivo/_material_apocrifo_no_usar/
    #
    # Cuando existan las calificaciones manuscritas reales de los jueces, la
    # matriz debe reconstruirse a partir de esos datos y no de valores
    # precargados. Requiere nuevo pronunciamiento del tesista.
    # ---------------------------------------------------------------------
    raise SystemExit(
        "Generación bloqueada por DEC-014: la matriz de IVC contendría "
        "calificaciones de jueces sin respaldo empírico. Reconstruir a partir "
        "de los formatos Fany en blanco una vez aplicados por los jueces reales."
    )
