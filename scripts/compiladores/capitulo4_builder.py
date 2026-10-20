#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - ENSAMBLADOR DE CAPÍTULO IV: METODOLOGÍA DE LA INVESTIGACIÓN
Universidad Nacional José María Arguedas (UNAJMA)
Facultad de Ingeniería - Escuela Profesional de Ingeniería de Sistemas

Alineación 1:1 con el Informe Final EPIS-UNAJMA (Modelo Jhon 2026, pp. 88–98):
- 14 secciones canónicas (4.1 a 4.14) redactadas en tiempo pasado de investigación ejecutada
- Cero párrafo introductorio meta-explicativo debajo del título capitular
- Cero fórmulas matemáticas, quebrados o signos de dólar dentro de celdas de tablas o texto
- Ecuaciones OMML nativas centradas en el cuerpo narrativo (docx_quirurgico.py)
- Numeración global continua de tablas: Tablas 9, 10, 11 y 12 (SEQ Tabla)
- Cuadros metodológicos complementarios formateados bajo APA 7 sin campo SEQ Tabla
- Preservación estricta de las 12 ecuaciones OMML nativas
================================================================================
"""

import os
import sys
from docx.shared import Inches, Pt, Twips
from docx.text.paragraph import Paragraph
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utilidades')))

from docx_utilidades import (
    agregar_titulo_1, agregar_titulo_2, agregar_titulo_3, agregar_titulo_4,
    agregar_parrafo, agregar_item_lista, agregar_tabla_datos,
    formatear_tabla_apa7, procesar_formato_texto
)
from docx_quirurgico import (
    mathml_to_omml, crear_parrafo_formula_dedicada, aplicar_formato_formula_dedicada,
    ANCHO_UTIL_PORTRAIT_DXA, LINE_SPACING_1_0_DXA
)

try:
    from docx_quirurgico import insertar_ecuacion_centrada
except ImportError:
    def insertar_ecuacion_centrada(doc, mathml_str, numero_eq=None):
        """
        Inserta una ecuación OMML nativa de Word a partir de MathML.
        La ecuación se sitúa sobre un tab stop centrado en la mitad del área de
        texto (4394 dxa) y, cuando lleva numeración, el número se alinea al
        margen derecho mediante un tab stop derecho (8788 dxa), sin espacios
        literales de relleno.
        """
        omml_elem = mathml_to_omml(mathml_str)
        p_xml = crear_parrafo_formula_dedicada(
            omml_elem,
            align="left",
            line_spacing=LINE_SPACING_1_0_DXA,
            space_before=60,
            space_after=120,
            left_indent_dxa=0
        )
        doc.element.body.insert_element_before(p_xml, 'w:sectPr')
        p = Paragraph(p_xml, doc._body)

        if numero_eq is None:
            aplicar_formato_formula_dedicada(p)
            return p

        # Tabulaciones nativas: centro del área de texto y margen derecho.
        p.paragraph_format.tab_stops.add_tab_stop(
            Twips(ANCHO_UTIL_PORTRAIT_DXA // 2), WD_TAB_ALIGNMENT.CENTER
        )
        p.paragraph_format.tab_stops.add_tab_stop(
            Twips(ANCHO_UTIL_PORTRAIT_DXA), WD_TAB_ALIGNMENT.RIGHT
        )

        # Tabulador previo a la ecuación (la centra sobre el tab stop central).
        run_tab_previo = p.add_run()
        run_tab_previo.add_tab()
        omml_elem.addprevious(run_tab_previo._r)

        # Tabulador posterior y número de ecuación alineado al margen derecho.
        run_tab_final = p.add_run()
        run_tab_final.add_tab()
        etiqueta = str(numero_eq) if str(numero_eq).startswith("(") else f"({numero_eq})"
        run_num = p.add_run(etiqueta)
        run_num.font.name = 'Times New Roman'
        run_num.font.size = Pt(12)
        return p


# ==============================================================================
# EXPRESIONES MATHML CANÓNICAS PARA TRANSFORMACIÓN OMML NATIVA (<m:oMath>)
# ==============================================================================

MATHML_DISENO = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mi>GE</mi>
  <mo>:</mo>
  <msub><mi>O</mi><mn>1</mn></msub>
  <mo>&#x2192;</mo>
  <mi>X</mi>
  <mo>&#x2192;</mo>
  <msub><mi>O</mi><mn>2</mn></msub>
</math>
"""

MATHML_TREG = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <msub><mover><mi>T</mi><mo>&#x00AF;</mo></mover><mrow><mi>r</mi><mi>e</mi><mi>g</mi><mo>,</mo><mi>i</mi></mrow></msub>
  <mo>=</mo>
  <mfrac>
    <mrow>
      <munderover>
        <mo>&#x2211;</mo>
        <mrow><mi>j</mi><mo>=</mo><mn>1</mn></mrow>
        <msub><mi>k</mi><mi>i</mi></msub>
      </munderover>
      <mrow><mo>(</mo><msub><mi>t</mi><mrow><mi>f</mi><mi>i</mi><mi>n</mi><mo>,</mo><mi>i</mi><mi>j</mi></mrow></msub><mo>&#x2212;</mo><msub><mi>t</mi><mrow><mi>i</mi><mi>n</mi><mi>i</mi><mi>c</mi><mi>i</mi><mi>o</mi><mo>,</mo><mi>i</mi><mi>j</mi></mrow></msub><mo>)</mo></mrow>
    </mrow>
    <msub><mi>k</mi><mi>i</mi></msub>
  </mfrac>
</math>
"""

MATHML_TVALE = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <msub><mover><mi>T</mi><mo>&#x00AF;</mo></mover><mrow><mi>v</mi><mi>a</mi><mi>l</mi><mi>e</mi><mo>,</mo><mi>i</mi></mrow></msub>
  <mo>=</mo>
  <mfrac>
    <mrow>
      <munderover>
        <mo>&#x2211;</mo>
        <mrow><mi>j</mi><mo>=</mo><mn>1</mn></mrow>
        <msub><mi>m</mi><mi>i</mi></msub>
      </munderover>
      <mrow><mo>(</mo><msub><mi>t</mi><mrow><mi>e</mi><mi>m</mi><mi>i</mi><mi>s</mi><mi>i</mi><mi>o</mi><mi>n</mi><mo>,</mo><mi>i</mi><mi>j</mi></mrow></msub><mo>&#x2212;</mo><msub><mi>t</mi><mrow><mi>s</mi><mi>o</mi><mi>l</mi><mi>i</mi><mi>c</mi><mi>i</mi><mi>t</mi><mi>u</mi><mi>d</mi><mo>,</mo><mi>i</mi><mi>j</mi></mrow></msub><mo>)</mo></mrow>
    </mrow>
    <msub><mi>m</mi><mi>i</mi></msub>
  </mfrac>
</math>
"""

MATHML_RSD = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mi>R</mi><mi>S</mi><msub><mi>D</mi><mi>i</mi></msub>
  <mo>=</mo>
  <mfenced open="(" close=")">
    <mfrac>
      <msub><mi>N</mi><mrow><mi>c</mi><mi>o</mi><mi>n</mi><mi>f</mi><mi>o</mi><mi>r</mi><mi>m</mi><mi>e</mi><mi>s</mi><mo>,</mo><mi>i</mi></mrow></msub>
      <msub><mi>N</mi><mrow><mi>t</mi><mi>o</mi><mi>t</mi><mi>a</mi><mi>l</mi><mo>,</mo><mi>i</mi></mrow></msub>
    </mfrac>
  </mfenced>
  <mo>&#x00D7;</mo>
  <mn>100</mn>
</math>
"""

MATHML_CPE = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mi>C</mi><mi>P</mi><msub><mi>E</mi><mi>i</mi></msub>
  <mo>=</mo>
  <mfenced open="(" close=")">
    <mfrac>
      <msub><mi>N</mi><mrow><mi>c</mi><mi>o</mi><mi>n</mi><mi>c</mi><mi>o</mi><mi>r</mi><mi>d</mi><mi>a</mi><mi>n</mi><mi>t</mi><mi>e</mi><mi>s</mi><mo>,</mo><mi>i</mi></mrow></msub>
      <msub><mi>N</mi><mrow><mi>d</mi><mi>e</mi><mi>s</mi><mi>p</mi><mi>a</mi><mi>c</mi><mi>h</mi><mi>o</mi><mi>s</mi><mo>,</mo><mi>i</mi></mrow></msub>
    </mfrac>
  </mfenced>
  <mo>&#x00D7;</mo>
  <mn>100</mn>
</math>
"""

MATHML_AP = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mi>A</mi><msub><mi>P</mi><mi>i</mi></msub>
  <mo>=</mo>
  <munderover>
    <mo>&#x2211;</mo>
    <mrow><mi>j</mi><mo>=</mo><mn>1</mn></mrow>
    <mn>4</mn>
  </munderover>
  <msub><mi>X</mi><mrow><mi>A</mi><mi>P</mi><mo>,</mo><mi>i</mi><mi>j</mi></mrow></msub>
</math>
"""

MATHML_UP = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mi>U</mi><msub><mi>P</mi><mi>i</mi></msub>
  <mo>=</mo>
  <munderover>
    <mo>&#x2211;</mo>
    <mrow><mi>j</mi><mo>=</mo><mn>1</mn></mrow>
    <mn>4</mn>
  </munderover>
  <msub><mi>X</mi><mrow><mi>U</mi><mi>P</mi><mo>,</mo><mi>i</mi><mi>j</mi></mrow></msub>
</math>
"""

MATHML_ALFA = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mi>&#x03B1;</mi>
  <mo>=</mo>
  <mfrac>
    <mi>K</mi>
    <mrow><mi>K</mi><mo>&#x2212;</mo><mn>1</mn></mrow>
  </mfrac>
  <mfenced open="[" close="]">
    <mrow>
      <mn>1</mn>
      <mo>&#x2212;</mo>
      <mfrac>
        <mrow>
          <munderover>
            <mo>&#x2211;</mo>
            <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow>
            <mi>K</mi>
          </munderover>
          <msubsup><mi>S</mi><mi>i</mi><mn>2</mn></msubsup>
        </mrow>
        <msubsup><mi>S</mi><mi>T</mi><mn>2</mn></msubsup>
      </mfrac>
    </mrow>
  </mfenced>
</math>
"""

MATHML_AIKEN = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mi>V</mi>
  <mo>=</mo>
  <mfrac>
    <mi>S</mi>
    <mi>n</mi>
  </mfrac>
</math>
"""

MATHML_T_STUDENT = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mi>t</mi>
  <mo>=</mo>
  <mfrac>
    <mover><mi>d</mi><mo>&#x00AF;</mo></mover>
    <mrow>
      <msub><mi>s</mi><mi>d</mi></msub>
      <mo>/</mo>
      <msqrt><mi>n</mi></msqrt>
    </mrow>
  </mfrac>
</math>
"""

MATHML_WILCOXON = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mi>Z</mi>
  <mo>=</mo>
  <mfrac>
    <mrow>
      <mi>W</mi>
      <mo>&#x2212;</mo>
      <mfrac>
        <mrow><mi>n</mi><mo>(</mo><mi>n</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow>
        <mn>4</mn>
      </mfrac>
    </mrow>
    <msqrt>
      <mfrac>
        <mrow><mi>n</mi><mo>(</mo><mi>n</mi><mo>+</mo><mn>1</mn><mo>)</mo><mo>(</mo><mn>2</mn><mi>n</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow>
        <mn>24</mn>
      </mfrac>
    </msqrt>
  </mfrac>
</math>
"""

MATHML_EFECTO_R = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mi>r</mi>
  <mo>=</mo>
  <mfrac>
    <mrow><mo>|</mo><mi>Z</mi><mo>|</mo></mrow>
    <msqrt><msub><mi>N</mi><mrow><mi>v</mi><mi>a</mi><mi>l</mi><mi>i</mi><mi>d</mi><mi>o</mi><mi>s</mi></mrow></msub></msqrt>
  </mfrac>
</math>
"""


def agregar_cuadro_complementario(doc, titulo_texto, encabezados, filas, nota_texto=None, col_widths=None, font_size_pt=9.0):
    """Inserta un cuadro metodológico complementario formateado en APA 7 sin campo SEQ Tabla."""
    p_tit = doc.add_paragraph()
    p_tit.paragraph_format.keep_with_next = True
    p_tit.paragraph_format.space_before = Pt(12)
    p_tit.paragraph_format.space_after = Pt(4)
    p_tit.paragraph_format.line_spacing = 1.0
    p_tit.paragraph_format.first_line_indent = Inches(0)

    partes_tit = procesar_formato_texto(titulo_texto)
    for r_texto, r_bold, r_italic in partes_tit:
        run_t = p_tit.add_run(r_texto)
        run_t.font.name = 'Times New Roman'
        run_t.font.size = Pt(10)
        run_t.font.bold = True or r_bold
        run_t.font.italic = r_italic

    tbl = doc.add_table(rows=len(filas) + 1, cols=len(encabezados))
    for c_idx, h_text in enumerate(encabezados):
        cell = tbl.rows[0].cells[c_idx]
        p = cell.paragraphs[0]
        p.text = ""
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r_texto, r_bold, r_italic in procesar_formato_texto(h_text):
            r = p.add_run(r_texto)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(font_size_pt)
            r.font.bold = True
            r.font.italic = r_italic

    for r_idx, fila in enumerate(filas):
        for c_idx, val in enumerate(fila):
            cell = tbl.rows[r_idx + 1].cells[c_idx]
            p = cell.paragraphs[0]
            p.text = ""
            for r_texto, r_bold, r_italic in procesar_formato_texto(val):
                r = p.add_run(r_texto)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(font_size_pt)
                r.font.bold = r_bold
                r.font.italic = r_italic

    formatear_tabla_apa7(tbl, col_widths=col_widths, font_size_pt=font_size_pt)

    if nota_texto:
        p_not = doc.add_paragraph()
        p_not.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_not.paragraph_format.space_before = Pt(4)
        p_not.paragraph_format.space_after = Pt(12)
        p_not.paragraph_format.line_spacing = 1.0
        p_not.paragraph_format.first_line_indent = Inches(0)
        run_lbl = p_not.add_run("Nota. ")
        run_lbl.font.name = 'Times New Roman'
        run_lbl.font.size = Pt(9.5)
        run_lbl.font.italic = True
        for r_texto, r_bold, r_italic in procesar_formato_texto(nota_texto):
            r = p_not.add_run(r_texto)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            r.font.bold = r_bold
            r.font.italic = r_italic


def construir_capitulo4(doc):
    agregar_titulo_1(doc, "CAPÍTULO IV: METODOLOGÍA DE LA INVESTIGACIÓN")

    # ==========================================================================
    # 4.1. Tipo de investigación
    # ==========================================================================
    agregar_titulo_2(doc, "4.1. Tipo de investigación")
    agregar_parrafo(
        doc,
        "La investigación fue de tipo aplicada, por cuanto utilizó los principios de la ingeniería de software, "
        "la metodología ágil Extreme Programming (Beck, 1999) y el estándar internacional de calidad ISO/IEC 25010:2023 "
        "(International Organization for Standardization [ISO] e International Electrotechnical Commission [IEC], 2023) "
        "para diseñar, construir y desplegar el sistema web SIVAC con el propósito directo de resolver la problemática "
        "operativa en el control de movimientos de productos biológicos de la Dirección de Salud Apurímac II. Conforme "
        "a Hernández-Sampieri et al. (2014, p. 141), la investigación aplicada se orienta a la resolución práctica de "
        "problemas específicos dentro de un contexto organizacional real mediante la instrumentación tecnológica de "
        "conocimientos científicos verificados.",
        sangria=True
    )

    # ==========================================================================
    # 4.2. Nivel de investigación
    # ==========================================================================
    agregar_titulo_2(doc, "4.2. Nivel de investigación")
    agregar_parrafo(
        doc,
        "La investigación se enmarcó en el tipo aplicada y nivel explicativo de evaluación de intervención tecnológica; "
        "no obstante, debido a la naturaleza del diseño preexperimental de un solo grupo sin grupo de control paralelo, "
        "el alcance inferencial se orienta a determinar la existencia de cambios estadísticamente significativos asociados "
        "a la aplicación del sistema web SIVAC entre el pre-test y el post-test, reconociendo las amenazas a la validez "
        "interna (historia, maduración, efecto de aprendizaje y familiarización tecnológica), las cuales fueron mitigadas "
        "mediante ventanas de observación simétricas y protocolos estandarizados. Conforme a Hernández-Sampieri et al. "
        "(2014), los estudios explicativos evalúan en qué condiciones se manifiesta el efecto de una intervención sobre "
        "las dimensiones del fenómeno estudiado, aportando evidencia empírica cuantitativa sobre la optimización de los "
        "procesos operativos en la cadena de frío sanitaria.",
        sangria=True
    )

    # ==========================================================================
    # 4.3. Método de investigación
    # ==========================================================================
    agregar_titulo_2(doc, "4.3. Método de investigación")
    agregar_parrafo(
        doc,
        "Se empleó el método hipotético-deductivo, articulado sistemáticamente a lo largo de siete fases consecutivas "
        "previstas durante el desarrollo de la investigación: (1) diagnóstico basal de los flujos de información, tiempos "
        "y discrepancias documentales en la cadena de frío de la Dirección de Salud Apurímac II; (2) desarrollo e ingeniería "
        "del sistema web SIVAC aplicando las cuatro fases de Extreme Programming y el estándar ISO/IEC 25010:2023; (3) "
        "validación de contenido de los instrumentos por juicio de expertos y formalización del protocolo de confiabilidad; (4) "
        "medición basal pre-test (O₁) de los seis indicadores bajo la gestión manual tradicional; (5) despliegue institucional, "
        "capacitación técnica y periodo de estabilización operativa del sistema (X); (6) medición post-test (O₂) "
        "bajo la gestión digitalizada automatizada; y (7) procesamiento bioestadístico, verificación de normalidad y "
        "contrastación formal de las hipótesis formuladas (Hernández-Sampieri et al., 2014).",
        sangria=True
    )

    # ==========================================================================
    # 4.4. Enfoque de investigación
    # ==========================================================================
    agregar_titulo_2(doc, "4.4. Enfoque de investigación")
    agregar_parrafo(
        doc,
        "La investigación se desarrolló bajo el enfoque cuantitativo, caracterizado por la recolección secuencial y "
        "probatoria de datos numéricos estandarizados y el uso del análisis estadístico descriptivo e inferencial para "
        "establecer patrones de comportamiento y probar las hipótesis formuladas (Hernández-Sampieri et al., 2014). "
        "En virtud de este enfoque, las tres dimensiones de la gestión de movimientos mensuales de vacunas fueron medidas "
        "en escalas métricas y ordinales rigurosas: tiempos cronometrados expresados en minutos, proporciones "
        "auditadas de exactitud documental en porcentaje y puntuaciones psicométricas de aceptación tecnológica "
        "en escala de cinco niveles.",
        sangria=True
    )

    # ==========================================================================
    # 4.5. Diseño de la investigación
    # ==========================================================================
    agregar_titulo_2(doc, "4.5. Diseño de la investigación")
    agregar_parrafo(
        doc,
        "Se adoptó un diseño experimental en su variante preexperimental de pre-test y post-test con un solo grupo. "
        "Según Hernández-Sampieri et al. (2014), en esta estructura metodológica se aplica a un grupo único una "
        "medición previa al estímulo o tratamiento experimental, se administra seguidamente la intervención tecnológica "
        "y, finalmente, se ejecuta una medición posterior bajo idénticas condiciones instrumentales para evaluar la "
        "magnitud del cambio intragrupo. La elección de este diseño respondió a la naturaleza normativa e institucional "
        "de la cadena de suministro de inmunizaciones en la Dirección de Salud Apurímac II, donde la totalidad de los "
        "centros de acopio debió migrar de manera unificada al flujo digital para preservar la integridad contable "
        "de los lotes biológicos.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "El esquema formal que representó el diseño preexperimental de la investigación fue el siguiente:",
        sangria=True
    )

    insertar_ecuacion_centrada(doc, MATHML_DISENO)

    agregar_parrafo(doc, "Donde:", sangria=False, negrita=True)
    agregar_item_lista(
        doc,
        "**GE:** Grupo experimental único conformado por la totalidad censal del personal operativo de inmunizaciones "
        "y cadena de frío de la Dirección de Salud Apurímac II (14 trabajadores).",
        simbolo="•"
    )
    agregar_item_lista(
        doc,
        "**O₁:** Medición previa (pre-test) de los seis indicadores de la gestión de movimientos mensuales de vacunas bajo el "
        "procedimiento tradicional manual (libros foliados, cuadernos de cargo y hojas de cálculo aisladas) a lo largo "
        "de una ventana de observación estandarizada de 30 días calendario.",
        simbolo="•"
    )
    agregar_item_lista(
        doc,
        "**X:** Intervención tecnológica experimental, conformada por el despliegue del sistema web SIVAC, inducción "
        "técnica estandarizada y periodo de estabilización operativa.",
        simbolo="•"
    )
    agregar_item_lista(
        doc,
        "**O₂:** Medición posterior (post-test) de los mismos seis indicadores de la gestión de movimientos "
        "mensuales de vacunas ejecutada mediante el sistema web SIVAC a lo largo de una ventana simétrica de 30 días calendario.",
        simbolo="•"
    )

    agregar_parrafo(
        doc,
        "Para garantizar la validez metodológica interna y neutralizar potenciales sesgos de reactividad, historia "
        "o fatiga en las mediciones, se implementó un protocolo temporal simétrico compuesto por cuatro etapas: (a) "
        "una ventana basal pre-test (O₁) de 30 días calendario; (b) una fase de inducción y capacitación técnica estandarizada "
        "de 5 días hábiles sobre los módulos de SIVAC a los 14 operadores; (c) un periodo de estabilización operativa de 10 días "
        "calendario en producción asistida previo al inicio del post-test, orientado a mitigar el sesgo derivado de la curva "
        "inicial de aprendizaje tecnológico; y (d) una ventana post-test (O₂) simétrica de 30 días calendario bajo idénticas "
        "condiciones de demanda institucional. En el siguiente cuadro se detalla el cronograma y protocolo de ejecución de la "
        "intervención preexperimental.",
        sangria=True
    )

    headers_cronograma = [
        "Etapa de Intervención",
        "Actividades Operativas Desarrolladas",
        "Ventana Temporal",
        "Control de Amenazas a la Validez"
    ]
    filas_cronograma = [
        [
            "Etapa 1: Medición basal pre-test (O₁)",
            "Auditoría retrospectiva y concurrente de libros de kardex manuales, cronometraje in situ de registros y vales pecosa físicos, y aplicación de la Modalidad A del Instrumento N.° 03 en línea base.",
            "30 días calendario",
            "Observación directa bajo condiciones rutinarias para evitar reactividad del personal."
        ],
        [
            "Etapa 2: Despliegue y capacitación técnica (X)",
            "Instalación de SIVAC en servidores y terminales, inducción teórico-práctica estandarizada a los 14 operadores censales y entrega de manuales operativos.",
            "5 días hábiles",
            "Estandarización del dominio operativo de la plataforma en todos los centros de acopio."
        ],
        [
            "Etapa 3: Estabilización operativa (X)",
            "Uso asistido de SIVAC en operaciones diarias con soporte técnico in situ, resolución de dudas transaccionales y ajuste de perfiles de usuario.",
            "10 días calendario",
            "Mitigación del sesgo de curva de aprendizaje inicial y familiarización tecnológica previa al post-test."
        ],
        [
            "Etapa 4: Medición post-test (O₂)",
            "Auditoría de registros transaccionales digitales en base de datos SIVAC, cronometraje digital de operaciones y vales, y aplicación de las modalidades A y B del Instrumento N.° 03 tras la intervención.",
            "30 días calendario",
            "Ventana temporal idéntica a O₁ bajo igual régimen de demanda y flujo de biológicos."
        ]
    ]
    agregar_cuadro_complementario(
        doc,
        titulo_texto="Cronograma y protocolo de ejecución de la intervención preexperimental",
        encabezados=headers_cronograma,
        filas=filas_cronograma,
        nota_texto="Estructura temporal diseñada para mitigar amenazas a la validez interna mediante ventanas simétricas de 30 días calendario y un intervalo de estabilización operativa previo a la recolección post-test.",
        col_widths=[Inches(1.30), Inches(2.40), Inches(1.10), Inches(1.30)],
        font_size_pt=9.0
    )

    # ==========================================================================
    # 4.6. Población de estudio
    # ==========================================================================
    agregar_titulo_2(doc, "4.6. Población de estudio")
    agregar_parrafo(
        doc,
        "Conforme a Hernández-Sampieri et al. (2014), la población constituye el conjunto de todos los casos que "
        "concuerdan con determinadas especificaciones de contenido, lugar y tiempo. En la presente investigación, "
        "la población de estudio estuvo conformada por la totalidad del personal técnico, asistencial y administrativo "
        "responsable de la recepción, almacenamiento, control de kardex, despacho y emisión de vales de productos "
        "biológicos en la cadena de inmunizaciones y cadena de frío de la Dirección de Salud Apurímac II, ascendiendo "
        "a un universo finito de catorce (N = 14) operadores distribuidos en el almacén especializado central y los "
        "centros de acopio de las redes de salud jurisdiccionales.",
        sangria=True
    )

    # ==========================================================================
    # 4.7. Muestra
    # ==========================================================================
    agregar_titulo_2(doc, "4.7. Muestra")
    agregar_parrafo(
        doc,
        "Debido a que la población objetivo fue reducida, finita y plenamente accesible para la intervención "
        "tecnológica, no se aplicó ninguna fórmula de muestreo probabilístico y se trabajó con una población censal "
        "(N = n = 14), abarcando al 100% de los operadores de la cadena de frío e inmunizaciones de la jurisdicción "
        "sanitaria (Hernández-Sampieri et al., 2014). En la Tabla 9 se detalla la distribución del personal evaluado "
        "según su centro de acopio y función operativa desempeñada.",
        sangria=True
    )

    headers_t9 = [
        "Centro de Acopio / Dependencia Sanitaria",
        "Función Operativa en la Cadena de Inmunizaciones",
        "Personal (n)",
        "Porcentaje (%)"
    ]
    filas_t9 = [
        [
            "Almacén Especializado DISA Apurímac II - Sede Central",
            "Coordinación de Estrategia Sanitaria de Inmunizaciones y Cadena de Frío",
            "4",
            "28.57%"
        ],
        [
            "Centro de Acopio Andahuaylas",
            "Responsables de Almacén de Vacunas y Control de Kardex",
            "2",
            "14.29%"
        ],
        [
            "Centro de Acopio Talavera",
            "Responsables de Cadena de Frío y Despacho de Biológicos",
            "2",
            "14.29%"
        ],
        [
            "Centro de Acopio San Jerónimo",
            "Responsables de Cadena de Frío y Despacho de Biológicos",
            "2",
            "14.29%"
        ],
        [
            "Centro de Acopio Santa María de Chicmo",
            "Responsable de Almacén de Inmunizaciones de Microred",
            "1",
            "7.14%"
        ],
        [
            "Centro de Acopio Huancarama",
            "Responsable de Almacén de Inmunizaciones de Microred",
            "1",
            "7.14%"
        ],
        [
            "Centro de Acopio Chincheros",
            "Responsable de Cadena de Frío y Distribución Territorial",
            "1",
            "7.14%"
        ],
        [
            "Centro de Acopio Uripa/Ocobamba",
            "Responsable de Cadena de Frío y Distribución Territorial",
            "1",
            "7.14%"
        ],
        [
            "**Total**",
            "**Población y Muestra Censal (N = n = 14)**",
            "**14**",
            "**100.00%**"
        ]
    ]
    agregar_tabla_datos(
        doc,
        numero="9",
        titulo="Distribución de la población y muestra censal por función operativa y centro de acopio en la DISA Apurímac II",
        encabezados=headers_t9,
        filas=filas_t9,
        nota="Padrón nominal del personal técnico y administrativo de la Estrategia Sanitaria de Inmunizaciones y Cadena de Frío de la Dirección de Salud Apurímac II.",
        col_widths=[Inches(2.3), Inches(2.2), Inches(0.8), Inches(0.8)],
        font_size_pt=9.5
    )

    # ==========================================================================
    # 4.8. Unidad de análisis
    # ==========================================================================
    agregar_titulo_2(doc, "4.8. Unidad de análisis")
    agregar_parrafo(
        doc,
        "En la arquitectura metodológica del estudio se diferenció estrictamente la unidad de observación primaria "
        "de la unidad de análisis estadístico pareado. Las unidades de observación primarias correspondieron a los eventos "
        "transaccionales específicos recolectados en campo: las operaciones cronometradas de registro y despacho, los asientos "
        "y expedientes de kardex auditados, las órdenes de distribución conciliadas y las respuestas a los cuestionarios "
        "psicométricos administrados. Por su parte, la unidad de análisis estadístico pareado estuvo constituida de manera "
        "invariable por cada uno de los catorce operadores (OP-01 a OP-14, N = n = 14) que gestionaron la cadena de "
        "inmunizaciones en ambos periodos de observación.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Para posibilitar los contrastes pareados intrasujeto requeridos por las pruebas de Wilcoxon y t de Student, "
        "se aplicó una regla formal de agregación matemática por operador que consolidó las observaciones primarias "
        "en un único par ordenado (O₁ᵢ, O₂ᵢ) por cada trabajador: (a) para el Tiempo de registro (T_reg), se calculó el promedio "
        "aritmético en minutos de las k operaciones observadas para el operador i en cada periodo; (b) para el Tiempo de emisión "
        "de vales (T_vale), se calculó el promedio aritmético en minutos de los m vales emitidos por el operador i en cada periodo; "
        "(c) para los Registros sin discrepancias (RSD), se obtuvo el porcentaje de registros conformes (que cumplen simultáneamente "
        "los 8 criterios normativos) sobre el total de registros auditados al operador i en la ventana de 30 días; (d) para la "
        "Concordancia programada vs. entregada (CPE), se determinó el porcentaje de despachos concordantes sobre el total de "
        "despachos auditados al operador i; y (e) para la Aceptación del proceso (AP) y la Utilidad "
        "percibida (UP), se utilizó el puntaje sumativo directo obtenido por el operador i en cada subescala "
        "de 4 ítems (rango de 4 a 20 puntos), correspondiendo a AP-01 a AP-04 y a UP-01 a UP-04.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Asimismo, se definieron explícitamente los criterios de inclusión y el tamaño muestral efectivo (n efectivo) por "
        "indicador. Dado que los 4 operadores de la sede central y los 10 responsables de centros de acopio periféricos "
        "pueden ejecutar volúmenes diferenciados de emisión de vales frente a recepción física de biológicos, se reporta "
        "con transparencia el n efectivo de pares válidos por cada indicador cuando un operador no emita comprobantes de "
        "salida en ambos periodos o presente diferencia nula en los rangos con signo de Wilcoxon (O₂ᵢ - O₁ᵢ = 0). En el "
        "cuadro siguiente se detalla la correspondencia entre unidades de observación primaria, reglas de agregación "
        "pareada por operador y criterios de inclusión.",
        sangria=True
    )

    headers_unidades = [
        "Dimensión e Indicador",
        "Unidad de Observación Primaria",
        "Regla de Agregación Pareada por Operador",
        "Criterio de Inclusión / n Efectivo"
    ]
    filas_unidades = [
        [
            "Dimensión 1:\nTiempo de registro (T_reg)",
            "Operaciones individuales de registro de movimientos (ingresos y egresos).",
            "Promedio aritmético en minutos de las k operaciones del operador i en la ventana de 30 días.",
            "n = 14 operadores con operaciones de registro observadas en pre-test y post-test."
        ],
        [
            "Dimensión 1:\nTiempo de emisión de vale (T_vale)",
            "Eventos de confección y emisión de comprobantes de salida o vales pecosa.",
            "Promedio aritmético en minutos de los m vales emitidos por el operador i en el periodo.",
            "n efectivo correspondiente a los operadores con emisión de vales en ambos periodos."
        ],
        [
            "Dimensión 2:\nRegistros sin discrepancias (RSD)",
            "Asientos de kardex y transacciones de control de lotes auditados.",
            "Porcentaje de registros con 8 criterios aprobados simultáneamente sobre el total del operador i.",
            "n = 14 operadores con expedientes de kardex auditados en pre-test y post-test."
        ],
        [
            "Dimensión 2:\nConcordancia programada vs. entregada (CPE)",
            "Despachos de vacunas conciliados contra órdenes oficiales de requerimiento.",
            "Porcentaje de despachos con coincidencia exacta (Q_entregada = Q_programada) del operador i.",
            "n = 14 operadores con despachos conciliados en pre-test y post-test."
        ],
        [
            "Dimensión 3:\nAceptación del proceso (AP)",
            "Respuestas individuales a los reactivos AP-01 a AP-04 del cuestionario psicométrico de la Modalidad A.",
            "Puntaje sumativo directo de los 4 reactivos de Aceptación del proceso operativo (rango de 4 a 20 puntos).",
            "n = 14 operadores censales que completaron el cuestionario en ambas etapas."
        ],
        [
            "Dimensión 3:\nUtilidad percibida (UP)",
            "Respuestas individuales a los reactivos UP-01 a UP-04 del cuestionario psicométrico de la Modalidad A.",
            "Puntaje sumativo directo de los 4 reactivos de Utilidad percibida para la gestión (rango de 4 a 20 puntos).",
            "n = 14 operadores censales que completaron el cuestionario en ambas etapas."
        ]
    ]
    agregar_cuadro_complementario(
        doc,
        titulo_texto="Estructura de unidades de observación primaria, reglas de agregación pareada y criterios de inclusión",
        encabezados=headers_unidades,
        filas=filas_unidades,
        nota_texto="Diferenciación metodológica entre las unidades empíricas observadas en campo y los pares agregados por operador (N = 14) requeridos para el análisis estadístico inferencial.",
        col_widths=[Inches(1.60), Inches(1.50), Inches(1.80), Inches(1.20)],
        font_size_pt=9.0
    )

    # ==========================================================================
    # 4.9. Operacionalización de variables
    # ==========================================================================
    agregar_titulo_2(doc, "4.9. Operacionalización de variables")

    agregar_titulo_3(doc, "4.9.1. Variable independiente: Sistema web SIVAC")
    agregar_parrafo(
        doc,
        "La variable independiente (Sistema web SIVAC) se define operacionalmente como una intervención tecnológica "
        "dicotómica administrada en el entorno de trabajo: condición basal pre-intervención (X₀: gestión manual en formatos "
        "físicos y libros de kardex) frente a condición post-intervención (X₁: gestión digitalizada mediante el sistema "
        "web SIVAC). Su ingeniería bajo Extreme Programming y su verificación técnica bajo el estándar ISO/IEC 25010:2023 "
        "se documentan en el Capítulo III como sustento de construcción del artefacto tecnológico.",
        sangria=True
    )

    agregar_titulo_3(doc, "4.9.2. Variable dependiente: Gestión de movimientos mensuales de vacunas")
    agregar_parrafo(
        doc,
        "La variable dependiente (Gestión de movimientos mensuales de vacunas) se definió conceptualmente como el proceso "
        "técnico-administrativo y logístico que regula la recepción, conservación, registro contable en kardex y "
        "distribución de productos biológicos e insumos complementarios a través de los niveles de la cadena de frío "
        "sanitaria (Ministerio de Salud, 2022). Operacionalmente, esta variable fue medida mediante tres dimensiones "
        "oficiales fijadas por la normativa metodológica del estudio: oportunidad de procesamiento, consistencia "
        "documental y satisfacción del usuario, desglosadas en seis indicadores cuantitativos cuyos atributos descriptivos "
        "se presentan en la Tabla 10.",
        sangria=True
    )

    headers_t10 = [
        "Variable",
        "Definición Operacional",
        "Dimensiones",
        "Indicadores",
        "Unidad de Medida",
        "Escala de Valoración"
    ]
    filas_t10 = [
        [
            "**Variable Independiente:**\nSistema web SIVAC",
            "Intervención tecnológica dicotómica: condición basal pre-intervención (X₀: gestión manual en formatos físicos) vs. condición post-intervención (X₁: gestión digitalizada mediante el sistema web SIVAC). Su ingeniería bajo XP y verificación técnica bajo ISO/IEC 25010:2023 se documentan en el Capítulo III.",
            "Intervención tecnológica dicotómica",
            "Condición basal pre-intervención (X₀: gestión manual en formatos físicos)\n\nCondición post-intervención (X₁: gestión digitalizada mediante el sistema web SIVAC)",
            "Condición operativa del sistema",
            "Nominal dicotómica (X₀ = Manual, X₁ = SIVAC)"
        ],
        [
            "**Variable Dependiente:**\nGestión de movimientos mensuales de vacunas",
            "Desempeño integral del proceso logístico de registro, control documental y despacho de biológicos en la cadena de frío sanitaria.",
            "1. Oportunidad de procesamiento",
            "Tiempo de registro de movimiento de vacunas (T_reg)\n\nTiempo de emisión de comprobante de salida o vale (T_vale)",
            "Minutos cronometrados por transacción (promedio pareado)",
            "De razón (continua)"
        ],
        [
            "**Variable Dependiente:**\nGestión de movimientos mensuales de vacunas",
            "Desempeño integral del proceso logístico de registro, control documental y despacho de biológicos en la cadena de frío sanitaria.",
            "2. Consistencia documental",
            "Porcentaje de registros sin discrepancias (RSD)\n\nConcordancia de cantidad programada versus entregada (CPE)",
            "Porcentaje de exactitud y conformidad documental",
            "De razón (0% a 100%)"
        ],
        [
            "**Variable Dependiente:**\nGestión de movimientos mensuales de vacunas",
            "Desempeño integral del proceso logístico de registro, control documental y despacho de biológicos en la cadena de frío sanitaria.",
            "3. Satisfacción del usuario",
            "Aceptación del proceso operativo (AP: reactivos AP-01 a AP-04)\n\nUtilidad percibida para la gestión (UP: reactivos UP-01 a UP-04)",
            "Puntaje sumativo en cuestionario psicométrico (4 a 20 puntos por indicador; 8 a 40 puntos en el total de la dimensión)",
            "Ordinal / Intervalar (total de la dimensión: 8 a 40)"
        ]
    ]
    agregar_tabla_datos(
        doc,
        numero="10",
        titulo="Operacionalización de las variables de investigación",
        encabezados=headers_t10,
        filas=filas_t10,
        nota="Estructura metodológica de variables, dimensiones, indicadores, unidades de medida y escalas de valoración del estudio conforme a las 3 dimensiones oficiales de la variable dependiente.",
        col_widths=[Inches(0.98), Inches(1.38), Inches(0.93), Inches(1.23), Inches(0.84), Inches(0.74)],
        font_size_pt=9.0
    )

    agregar_parrafo(
        doc,
        "La cuantificación matemática de los seis indicadores de la variable dependiente se efectuó mediante las "
        "expresiones formales descritas a continuación, las cuales rigen el procesamiento de las observaciones empíricas.",
        sangria=True
    )

    # Ecuación (1): T_reg
    agregar_parrafo(
        doc,
        "El primer indicador de la dimensión oportunidad de procesamiento, correspondiente al tiempo promedio de "
        "registro de movimientos mensuales de vacunas para el operador i, se calculó mediante la Ecuación 1:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_TREG, numero_eq=1)
    agregar_parrafo(
        doc,
        "Donde el término de la izquierda representa el tiempo medio de registro del operador i en minutos, los términos "
        "t_fin y t_inicio corresponden a los instantes exactos de culminación e inicio de cada una de las k operaciones "
        "observadas para dicho operador, y el denominador ki indica el total de registros cronometrados en la ventana de "
        "observación respectiva.",
        sangria=True
    )

    # Ecuación (2): T_vale
    agregar_parrafo(
        doc,
        "El segundo indicador de la dimensión oportunidad de procesamiento, referido al tiempo promedio de emisión de "
        "comprobante de salida o vale pecosa para el operador i, se determinó a través de la Ecuación 2:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_TVALE, numero_eq=2)
    agregar_parrafo(
        doc,
        "Donde la expresión representa el tiempo medio de emisión de comprobantes del operador i en minutos, t_emision "
        "y t_solicitud registran los instantes de entrega formal del vale impreso o generado y de recepción de la "
        "solicitud de despacho, y mi constituye el número total de vales gestionados por dicho operador en el periodo.",
        sangria=True
    )

    # Ecuación (3): RSD
    agregar_parrafo(
        doc,
        "En la segunda dimensión, referida a la consistencia documental, el porcentaje de registros sin discrepancias "
        "del operador i se calculó como la proporción de asientos que cumplieron simultáneamente los ocho criterios "
        "normativos de control sobre el total auditado, conforme a la Ecuación 3:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_RSD, numero_eq=3)
    agregar_parrafo(
        doc,
        "Donde el numerador cuantifica los movimientos del operador i que aprobaron los ocho criterios normativos de "
        "conformidad simultánea (identificación del biológico, lote, vencimiento, cantidad física, centro de origen o "
        "destino, identificación del responsable, saldo aritmético y correlatividad temporal) y el denominador representa "
        "el total de asientos auditados a dicho operador durante la ventana de evaluación.",
        sangria=True
    )

    # Ecuación (4): CPE
    agregar_parrafo(
        doc,
        "El segundo indicador de la dimensión consistencia documental, correspondiente a la concordancia de cantidad "
        "programada versus entregada, evaluó el porcentaje de despachos concordantes auditados al operador i mediante "
        "la Ecuación 4:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_CPE, numero_eq=4)
    agregar_parrafo(
        doc,
        "Donde el numerador representa el número de despachos auditados en los que la cantidad física entregada en el "
        "vale coincidió con exactitud matemática con la cantidad programada en la orden oficial (Q_entregada = Q_programada), "
        "y el denominador expresa el total de despachos auditados al operador i en el periodo, garantizando que el "
        "indicador quede acotado estrictamente en el rango de 0% a 100% y evitando distorsiones por sobredespacho.",
        sangria=True
    )

    # Ecuación (5): AP
    agregar_parrafo(
        doc,
        "Dentro de la tercera dimensión, orientada a la satisfacción del usuario bajo el Modelo de Aceptación Tecnológica "
        "(Davis, 1989), el indicador de aceptación del proceso se cuantificó como el puntaje sumativo directo obtenido por "
        "el operador i en los cuatro reactivos AP-01 a AP-04 que integran la subescala de aceptación del proceso "
        "operativo, según la Ecuación 5:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_AP, numero_eq=5)
    agregar_parrafo(
        doc,
        "Donde cada término representa la calificación ordinal asignada por el operador i al reactivo j (del reactivo "
        "AP-01 al reactivo AP-04) en la escala Likert de 1 a 5 puntos, arrojando un puntaje sumativo acotado en el "
        "intervalo de 4 a 20 puntos.",
        sangria=True
    )

    # Ecuación (6): UP
    agregar_parrafo(
        doc,
        "Finalmente, el indicador de utilidad percibida cuantificó la valoración del personal respecto a la eficacia "
        "instrumental del sistema para optimizar su desempeño laboral en la cadena de frío, calculándose como el puntaje "
        "sumativo en los cuatro reactivos UP-01 a UP-04 de la subescala correspondiente mediante la Ecuación 6:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_UP, numero_eq=6)
    agregar_parrafo(
        doc,
        "Donde los términos acumulan las puntuaciones otorgadas por el operador i a los reactivos UP-01 a UP-04 en la "
        "escala Likert de 1 a 5 puntos, configurando un puntaje sumativo individual comprendido entre 4 y 20 puntos.",
        sangria=True
    )

    # ==========================================================================
    # 4.10. Técnicas e instrumentos de recolección de datos
    # ==========================================================================
    agregar_titulo_2(doc, "4.10. Técnicas e instrumentos de recolección de datos")

    agregar_titulo_3(doc, "4.10.1. Técnicas de recolección de datos")
    agregar_parrafo(
        doc,
        "Se emplearon tres técnicas empíricas complementarias alineadas con la naturaleza de cada dimensión evaluada "
        "(Hernández-Sampieri et al., 2014):",
        sangria=True
    )
    agregar_item_lista(
        doc,
        "**Observación directa cronometrada:** Se aplicó para medir in situ y de manera no intrusiva la duración "
        "exacta de las operaciones de registro de movimientos y de emisión de vales de salida ejecutadas por los "
        "catorce operadores tanto en el procedimiento manual como en el sistema web SIVAC.",
        simbolo="a)"
    )
    agregar_item_lista(
        doc,
        "**Análisis documental (auditoría de registros):** Se utilizó para examinar de forma sistemática y "
        "retrospectiva los asientos del kardex físico, las solicitudes de requerimiento y las guías de remisión en "
        "el pre-test, contrastándolos frente a los reportes transaccionales y comprobantes digitales generados en el "
        "post-test.",
        simbolo="b)"
    )
    agregar_item_lista(
        doc,
        "**Encuesta psicométrica:** Se administró al personal censal de inmunizaciones con el propósito de recabar "
        "su valoración estructurada sobre la aceptación del proceso y la utilidad percibida en ambas etapas del "
        "estudio, fundamentándose en el Modelo de Aceptación Tecnológica (Davis, 1989).",
        simbolo="c)"
    )

    agregar_titulo_3(doc, "4.10.2. Instrumentos de recolección de datos")
    agregar_parrafo(
        doc,
        "En correspondencia directa con las técnicas descritas, se diseñaron y aplicaron tres instrumentos de recolección "
        "de datos con especificaciones operativas rigurosas: (a) el Instrumento N.° 01, Ficha de observación de tiempos "
        "cronometrados, estructurada con campos de control temporal y tres escenarios operativos estandarizados (REG-01: "
        "registro de ingreso de lote de vacuna; REG-02: registro de salida o transferencia; y VALE-01: emisión de vale pecosa) "
        "con disparadores unívocos de inicio y fin de cronometraje; (b) el Instrumento N.° 02, Guía de cotejo documental, "
        "conformada por ocho criterios binarios de verificación de conformidad formal emanados de las disposiciones de la "
        "Norma Técnica de Salud NTS N.° 196-MINSA/DGIESP-2022 (aprobada por Resolución Ministerial N.° 884-2022/MINSA) sobre "
        "gestión de la cadena de frío, regla FEFO, factores de pérdida y saldos de kardex; y (c) el Instrumento N.° 03, "
        "Cuestionario cuya Modalidad A constituye la escala oficial de contrastación de la Hipótesis Específica 3 y está "
        "integrada por 8 ítems en escala Likert de 5 puntos (1 = Totalmente en desacuerdo, 2 = En desacuerdo, 3 = Neutral, "
        "4 = De acuerdo y 5 = Totalmente de acuerdo), distribuidos en dos indicadores de 4 reactivos cada uno: Aceptación "
        "del proceso operativo (AP-01 a AP-04) y Utilidad percibida para la gestión (UP-01 a UP-04), con un rango global "
        "de 8 a 40 puntos y aplicación en pretest y postest. El mismo Instrumento N.° 03 incorpora, como módulo anexo "
        "de aplicación exclusiva en el postest, la Modalidad B, compuesta por 8 ítems adicionales (PU-01 a PU-04 y PE-01 "
        "a PE-04) destinados a documentar los constructos clásicos de utilidad y facilidad de uso percibidas del software "
        "bajo ISO/IEC 25010:2023. Ambas modalidades no son aditivas y la Modalidad B no interviene en el contraste "
        "inferencial. En la Tabla 11 se sintetiza la correspondencia metodológica.",
        sangria=True
    )

    headers_t11 = [
        "Dimensión Evaluada",
        "Indicadores",
        "Técnica de Recolección",
        "Instrumento de Medición",
        "Estructura e Ítems"
    ]
    filas_t11 = [
        [
            "1. Oportunidad de procesamiento",
            "Tiempo de registro de movimiento de vacunas\n\nTiempo de emisión de comprobante de salida o vale",
            "Observación directa cronometrada",
            "Instrumento N.° 01:\nFicha de observación de tiempos cronometrados",
            "Escenarios estandarizados (REG-01, REG-02 y VALE-01) con disparadores unívocos de cronometraje"
        ],
        [
            "2. Consistencia documental",
            "Porcentaje de registros sin discrepancias\n\nConcordancia de cantidad programada versus entregada",
            "Análisis documental y auditoría de kardex",
            "Instrumento N.° 02:\nGuía de cotejo de consistencia documental",
            "8 criterios binarios de conformidad contable sustentados en la NTS N.° 196-MINSA/DGIESP-2022"
        ],
        [
            "3. Satisfacción del usuario",
            "Aceptación del proceso\n\nUtilidad percibida",
            "Encuesta psicométrica estructurada",
            "Instrumento N.° 03:\nCuestionario de satisfacción del usuario y aceptación tecnológica",
            "Modalidad A (oficial para HE3): 8 ítems Likert de 1 a 5, en pretest y postest, con 4 ítems para Aceptación del proceso (AP-01 a AP-04) y 4 para Utilidad percibida (UP-01 a UP-04).\n\nModalidad B (anexo ISO/IEC 25010:2023): 8 ítems Likert de 1 a 5, exclusivos del postest, con 4 ítems para Utilidad percibida del software (PU-01 a PU-04) y 4 para Facilidad de uso percibida (PE-01 a PE-04). No aditiva respecto de la Modalidad A."
        ]
    ]
    agregar_tabla_datos(
        doc,
        numero="11",
        titulo="Relación de técnicas e instrumentos de recolección de datos por dimensión e indicador",
        encabezados=headers_t11,
        filas=filas_t11,
        nota="Correspondencia metodológica entre las tres dimensiones de la variable dependiente y los tres instrumentos diseñados.",
        col_widths=[Inches(1.13), Inches(1.43), Inches(1.08), Inches(1.28), Inches(1.18)],
        font_size_pt=9.5
    )

    # ==========================================================================
    # 4.11. Confiabilidad de los instrumentos
    # ==========================================================================
    agregar_titulo_2(doc, "4.11. Confiabilidad de los instrumentos")
    agregar_parrafo(
        doc,
        "La confiabilidad se refiere al grado en que la aplicación repetida de un instrumento al mismo sujeto u objeto "
        "produce resultados consistentes y coherentes (Hernández-Sampieri et al., 2014). En el presente estudio se "
        "establecerán protocolos de confiabilidad diferenciados según la naturaleza empírica de cada instrumento. Para el "
        "Instrumento N.° 01 (Ficha de observación de tiempos cronometrados), la confiabilidad del registro temporal se "
        "asegurará mediante un protocolo estandarizado de cronometraje con disparadores unívocos de inicio (apertura del "
        "formulario de captura) y corte (confirmación de guardado y emisión), complementado con una prueba piloto de "
        "calibración interobservador e instrucciones precisas de manejo de interrupciones no imputables a la plataforma.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Para el Instrumento N.° 02 (Guía de cotejo de consistencia documental), la confiabilidad de la auditoría se "
        "garantizará mediante un manual formal de codificación dicotómica para los ocho criterios normativos de la NTS "
        "N.° 196-MINSA/DGIESP-2022 y la verificación de la concordancia interevaluador a través del coeficiente Kappa de "
        "Cohen (κ = (P_o - P_e) / (1 - P_e)), reconociendo que cuando la auditoría es ejecutada por un único investigador "
        "se aplicará doble verificación cruzada sobre una submuestra aleatoria del 20% de expedientes para asegurar que κ >= 0.80.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Para el Instrumento N.° 03, en su Modalidad A oficial de 8 ítems en escala Likert de 1 a 5, la confiabilidad por "
        "consistencia interna se determinará mediante el coeficiente Alfa de Cronbach (α), cuya formulación matemática "
        "se expresa en la Ecuación 7:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_ALFA, numero_eq=7)
    agregar_parrafo(
        doc,
        "Donde el parámetro K representa el número de reactivos analizados, la sumatoria acumula las varianzas de los "
        "ítems individuales y el denominador indica la varianza del puntaje total de la escala. En concordancia con "
        "las directrices psicométricas y el principio de cero invención de datos empíricos, el coeficiente Alfa de Cronbach "
        "(α) se reportará de forma desagregada para la subescala de Aceptación del proceso operativo (AP-01 a AP-04, "
        "4 ítems), para la subescala de Utilidad percibida para la gestión (UP-01 a UP-04, 4 ítems) y para el puntaje "
        "global de la Modalidad A sobre los 8 ítems que la integran, una vez concluido el levantamiento de campo, "
        "exigiéndose como umbral mínimo de consistencia un valor α >= 0.70 (Hernández-Sampieri et al., 2014). La "
        "Modalidad B no forma parte de esa estimación y, de reportarse su consistencia interna, se presentará como "
        "indicador descriptivo separado, sin agregación con la Modalidad A.",
        sangria=True
    )

    # ==========================================================================
    # 4.12. Validez de los instrumentos
    # ==========================================================================
    agregar_titulo_2(doc, "4.12. Validez de los instrumentos")
    agregar_parrafo(
        doc,
        "La validez de contenido determinará el grado en que el instrumento refleje con fidelidad y exhaustividad "
        "el dominio teórico de las dimensiones evaluadas (Hernández-Sampieri et al., 2014). Este procedimiento se "
        "ejecutará mediante juicio de expertos con tres docentes e investigadores con grado de Magíster de la Escuela "
        "Profesional de Ingeniería de Sistemas de la Universidad Nacional José María Arguedas. El objeto del juicio es "
        "un único certificado de validez de contenido correspondiente al Instrumento N.° 03, que reproduce literalmente "
        "los 8 ítems de su Modalidad A (AP-01 a AP-04 y UP-01 a UP-04) y los somete a tres criterios dicotómicos "
        "independientes por ítem: Pertinencia (Sí/No), Relevancia (Sí/No) y Claridad (Sí/No). La cuantificación de la "
        "concordancia se realizará mediante el Coeficiente V de Aiken (Ecuación 8) y el Índice de Validez de Contenido "
        "(IVC), ambos derivados del modelo de Tristán-López (2008), que para tres jueces fija un valor mínimo por ítem "
        "de 0.5823:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_AIKEN, numero_eq=8)
    agregar_parrafo(
        doc,
        "Donde S representa la sumatoria de las valoraciones favorables asignadas por los jueces al ítem, n indica el "
        "número de expertos evaluadores (3 jueces) y c denota el número de categorías de la escala de valoración, que "
        "bajo criterios dicotámicos Sí/No adopta el valor c = 2, de modo que el denominador n(c - 1) se reduce a n. Los "
        "indicadores se reportarán en la Tabla 12 una vez concluida la evaluación del panel, y se contrastarán contra el "
        "umbral de aceptación de 0.80 que el presente estudio adopta como criterio propio, más estricto que el mínimo "
        "de 0.5823 fijado por Tristán-López (2008) para tres jueces. Los Instrumentos N.° 01 y N.° 02 no se "
        "someten a juicio de contenido, por cuanto no son escalas sino fichas de registro: su validez se sustenta en el "
        "protocolo de medición de movimientos mensuales de vacunas (PMMV), en el coeficiente de correlación intraclase ICC(2,1) "
        "mayor o igual a 0.75 para la ficha cronométrica y en el kappa de Cohen mayor o igual a 0.80 para la ficha de "
        "cotejo documental. Corresponde explicitar una consecuencia aritmética del valor c = 2 sobre el umbral de "
        "aceptación: con tres jueces y criterios dicotómicos, la Ecuación 8 solo puede adoptar cuatro valores, 0, 0.333, "
        "0.667 y 1.000, de modo que el umbral de 0.80 se alcanza únicamente con unanimidad perfecta de los tres jueces, "
        "y un solo voto negativo en un ítem lo deja en 0.667 y lo reprueba. El umbral de 0.80 no constituye, por tanto, "
        "un margen tolerante, sino una exigencia de consenso total. Por esa razón el resultado se reportará ítem por "
        "ítem con su intervalo de confianza de Wilson y no como un promedio que oculte la falta de consenso.",
        sangria=True
    )

    headers_t12 = [
        "Cód.",
        "Instrumento Evaluado",
        "Estructura Operativa",
        "Sustento de Validez",
        "V de Aiken",
        "IVC",
        "Dictamen"
    ]
    filas_t12 = [
        [
            "INST-01",
            "Instrumento N.° 01:\nFicha de observación de tiempos cronometrados",
            "Escenarios operativos REG-01, REG-02 y VALE-01 con disparadores unívocos de cronometraje",
            "No se somete a juicio de contenido. Protocolo PMMV e ICC(2,1) >= 0.75 entre observadores",
            "No aplica",
            "No aplica",
            "Acreditado por protocolo y concordancia interobservador"
        ],
        [
            "INST-02",
            "Instrumento N.° 02:\nGuía de cotejo documental",
            "8 criterios binarios de conformidad contable conforme a la NTS N.° 196-MINSA/DGIESP-2022",
            "No se somete a juicio de contenido. Regla de 8 criterios y kappa de Cohen >= 0.80 entre evaluadores",
            "No aplica",
            "No aplica",
            "Acreditado por protocolo y concordancia interevaluador"
        ],
        [
            "INST-03",
            "Instrumento N.° 03:\nCuestionario de satisfacción del usuario y aceptación tecnológica (Modalidad A)",
            "8 ítems Likert de 1 a 5: AP-01 a AP-04 (Aceptación del proceso) y UP-01 a UP-04 (Utilidad percibida)",
            "Juicio de contenido mediante certificado único con criterios dicotómicos Pertinencia, Relevancia y Claridad",
            "[Pendiente]",
            "[Pendiente]",
            "[Pendiente]"
        ]
    ]
    agregar_tabla_datos(
        doc,
        numero="12",
        titulo="Estructura de la validación de los instrumentos de recolección de datos",
        encabezados=headers_t12,
        filas=filas_t12,
        nota="Solo el Instrumento N.° 03 (Modalidad A) se somete a juicio de contenido. Los valores del Coeficiente V de Aiken, del Índice de Validez de Contenido y el dictamen se registrarán una vez concluida la evaluación del panel de tres jueces expertos con el certificado único del instrumento; no se reporta ningún coeficiente mientras no exista evaluación real.",
        col_widths=[Inches(0.60), Inches(1.14), Inches(1.14), Inches(1.36), Inches(0.58), Inches(0.43), Inches(0.85)],
        font_size_pt=10
    )

    agregar_parrafo(
        doc,
        "La designación de los tres jueces expertos se fundamentará en su idoneidad académica, experiencia docente e "
        "investigativa en ingeniería de sistemas, diseño de sistemas de información transaccionales y auditoría de sistemas "
        "de información en la Universidad Nacional José María Arguedas, a fin de asegurar la rigurosidad técnica de los "
        "artefactos de medición. Cada juez emitirá un certificado único sobre el Instrumento N.° 03, cuyo modelo es el "
        "formato institucional de Fany (2024) adoptado por la normativa del proyecto, y lo entregará en blanco para su "
        "llenado manuscrito. Como consideración metodológica complementaria, se reconoce que la pertinencia "
        "logística-sanitaria de los criterios de control de las fichas 01 y 02 se respalda directamente en los "
        "lineamientos normativos obligatorios de la NTS N.° 196-MINSA/DGIESP-2022 aplicable en la Dirección de Salud "
        "Apurímac II.",
        sangria=True
    )

    # ==========================================================================
    # 4.13. Técnicas estadísticas para el procesamiento de la información
    # ==========================================================================
    agregar_titulo_2(doc, "4.13. Técnicas estadísticas para el procesamiento de la información")
    agregar_parrafo(
        doc,
        "El procesamiento estadístico de los datos recolectados en el pre-test y post-test se estructuró mediante rutinas "
        "computacionales reproducibles en Python (scipy.stats, statsmodels, pingouin) y el entorno bioestadístico R. "
        "En una primera fase descriptiva, se calcularon para cada indicador medidas de tendencia central (media aritmética, "
        "mediana) y de dispersión (desviación estándar, rango intercuartílico), junto con valores extremos mínimos y máximos.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "En la fase inferencial, considerando el tamaño reducido de la población censal (N = 14) y la presencia de escalas "
        "ordinales en la tercera dimensión, la prueba de los rangos con signo de Wilcoxon constituyó el estimador primario "
        "robusto y uniforme para muestras pareadas pequeñas, complementada por la prueba t de Student pareada (Ecuación 9) "
        "únicamente en los indicadores continuos cuyas diferencias pareadas (dᵢ = O₂ᵢ - O₁ᵢ) confirmaron normalidad en la "
        "prueba de Shapiro-Wilk (p > 0.05):",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_T_STUDENT, numero_eq=9)
    agregar_parrafo(
        doc,
        "Donde el numerador representa la media aritmética de las diferencias pareadas entre el post-test y el pre-test, "
        "y el denominador corresponde al error estándar de dichas diferencias para los n operadores evaluados. En la "
        "prueba de los rangos con signo de Wilcoxon, el estadístico Z estandarizado se calculó según la Ecuación 10:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_WILCOXON, numero_eq=10)
    agregar_parrafo(
        doc,
        "Donde W representa la suma de rangos con signo asignados a las diferencias absolutas no nulas y n indica el "
        "número de pares con diferencia distinta de cero. Para cuantificar la relevancia práctica de la mejora más allá "
        "de la significancia estadística, se estimó el tamaño del efecto mediante el coeficiente de correlación de tamaño "
        "del efecto basado en el estadístico estandarizado Z (propuesto por Rosenthal, 1991, sobre los umbrales de Cohen, "
        "1988: pequeño >= 0.10, mediano >= 0.30, grande >= 0.50), formulado en la Ecuación 11:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_EFECTO_R, numero_eq=11)
    agregar_parrafo(
        doc,
        "Donde el valor absoluto del estadístico Z se divide entre la raíz cuadrada del número de pares válidos con "
        "diferencia distinta de cero (N_válidos), interpretándose la magnitud del efecto bajo los umbrales de Cohen (1988): "
        "pequeño >= 0.10, mediano >= 0.30 y grande >= 0.50.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Finalmente, para controlar la tasa de error por múltiples contrastes y precisar la direccionalidad inferencial, "
        "todas las pruebas se evaluaron con significancia bilateral (α = 0.05 a dos colas) por prudencia metodológica, "
        "verificando la dirección teórica esperada del cambio en las medianas o medias, y aplicando la corrección secuencial "
        "de Holm-Bonferroni sobre los seis indicadores para controlar rigurosamente la tasa de error familiar tipo I (FWER).",
        sangria=True
    )

    # ==========================================================================
    # 4.14. Consideraciones éticas y salvaguarda institucional
    # ==========================================================================
    agregar_titulo_2(doc, "4.14. Consideraciones éticas y salvaguarda institucional")
    agregar_parrafo(
        doc,
        "La ejecución de la presente investigación se rigió por los principios éticos de la investigación científica "
        "y la salvaguarda de la gestión sanitaria pública en la Dirección de Salud Apurímac II. En primer lugar, se "
        "tramitó la debida autorización institucional ante la Dirección General y la Coordinación de la Estrategia "
        "Sanitaria de Inmunizaciones y Cadena de Frío de la entidad, garantizando que las intervenciones técnicas no "
        "alteraran la provisión regular de biológicos a los establecimientos de salud jurisdiccionales.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "En segundo lugar, se garantizó el principio de autonomía y voluntariedad mediante la suscripción del consentimiento "
        "informado por parte de los catorce operadores participantes, asegurando la confidencialidad estricta y el "
        "anonimato de sus datos personales mediante la asignación de identificadores alfanuméricos correlativos (OP-01 a "
        "OP-14). Asimismo, se resguardó la confidencialidad de la información estratégica institucional, restringiendo el "
        "acceso a los registros y velando porque el estudio no involucrara datos clínicos nominales de pacientes ni menores "
        "de edad, limitándose estrictamente al control transaccional y volumétrico de lotes.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Por último, se aplicó una salvaguarda de contingencia sanitaria durante la etapa de transición operativa entre "
        "el procedimiento tradicional y el sistema web SIVAC: durante el periodo de capacitación y estabilización, el personal "
        "mantuvo el registro de respaldo físico en kardex en paralelo al flujo digital para asegurar cero riesgo de pérdida "
        "de trazabilidad o desabastecimiento en la cadena de frío provincial.",
        sangria=True
    )


if __name__ == "__main__":
    import docx
    from docx_utilidades import aplicar_margenes_unajma
    d = docx.Document()
    aplicar_margenes_unajma(d.sections[0])
    construir_capitulo4(d)
    os.makedirs("salidas/documentos", exist_ok=True)
    d.save("salidas/documentos/test_cap4.docx")
    print("Capítulo IV compilado exitosamente.")
