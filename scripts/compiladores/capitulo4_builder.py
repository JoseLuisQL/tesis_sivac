#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - ENSAMBLADOR DE CAPÍTULO IV: METODOLOGÍA DE LA INVESTIGACIÓN
Universidad Nacional José María Arguedas (UNAJMA)
Facultad de Ingeniería - Escuela Profesional de Ingeniería de Sistemas

Alineación 1:1 con el Informe Final EPIS-UNAJMA (Modelo Jhon 2026, pp. 88–98):
- 13 secciones exactas (4.1 a 4.13) redactadas en tiempo pasado de investigación ejecutada
- Cero párrafo introductorio meta-explicativo debajo del título capitular
- Cero fórmulas matemáticas, quebrados o signos '$' dentro de celdas de tablas o texto
- Ecuaciones OMML nativas centradas en el cuerpo narrativo (docx_quirurgico.py)
- Eliminación total de datos simulados de Alfa de Cronbach
- Numeración global continua de tablas: Tablas 9, 10, 11 y 12
================================================================================
"""

import os
import sys
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utilidades')))

from docx_utilidades import (
    agregar_titulo_1, agregar_titulo_2, agregar_titulo_3,
    agregar_parrafo, agregar_item_lista, agregar_tabla_datos
)
from docx_quirurgico import mathml_to_omml

try:
    from docx_quirurgico import insertar_ecuacion_centrada
except ImportError:
    def insertar_ecuacion_centrada(doc, mathml_str, numero_eq=None):
        """Inserta un párrafo centrado con una ecuación OMML nativa de Word a partir de MathML."""
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.first_line_indent = Inches(0)
        omml_elem = mathml_to_omml(mathml_str)
        p._p.append(omml_elem)
        if numero_eq is not None:
            etiqueta = str(numero_eq) if str(numero_eq).startswith("(") else f"({numero_eq})"
            run_num = p.add_run(f"    {etiqueta}")
            run_num.font.name = 'Times New Roman'
            run_num.font.size = Pt(12)
        return p


# ==============================================================================
# EXPRESIONES MATHML CANÓNICAS PARA TRANSFORMACIÓN OMML NATIVA (<m:oMath>)
# ==============================================================================

MATHML_DISENO = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mi>G</mi>
  <mo>:</mo>
  <mspace width="0.5em"/>
  <msub><mi>O</mi><mn>1</mn></msub>
  <mspace width="0.4em"/>
  <mo>&#x27F6;</mo>
  <mspace width="0.4em"/>
  <mi>X</mi>
  <mspace width="0.4em"/>
  <mo>&#x27F6;</mo>
  <mspace width="0.4em"/>
  <msub><mi>O</mi><mn>2</mn></msub>
</math>
"""

MATHML_TREG = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <msub><mi>T</mi><mrow><mi>r</mi><mi>e</mi><mi>g</mi></mrow></msub>
  <mo>=</mo>
  <mfrac>
    <mrow>
      <munderover>
        <mo>&#x2211;</mo>
        <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow>
        <mi>k</mi>
      </munderover>
      <mrow><mo>(</mo><msub><mi>t</mi><mrow><mi>f</mi><mi>i</mi><mi>n</mi><mo>,</mo><mi>i</mi></mrow></msub><mo>&#x2212;</mo><msub><mi>t</mi><mrow><mi>i</mi><mi>n</mi><mi>i</mi><mi>c</mi><mi>i</mi><mi>o</mi><mo>,</mo><mi>i</mi></mrow></msub><mo>)</mo></mrow>
    </mrow>
    <mi>k</mi>
  </mfrac>
</math>
"""

MATHML_TVALE = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <msub><mi>T</mi><mrow><mi>v</mi><mi>a</mi><mi>l</mi><mi>e</mi></mrow></msub>
  <mo>=</mo>
  <mfrac>
    <mrow>
      <munderover>
        <mo>&#x2211;</mo>
        <mrow><mi>j</mi><mo>=</mo><mn>1</mn></mrow>
        <mi>m</mi>
      </munderover>
      <mrow><mo>(</mo><msub><mi>t</mi><mrow><mi>e</mi><mi>m</mi><mi>i</mi><mi>s</mi><mi>i</mi><mi>o</mi><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>&#x2212;</mo><msub><mi>t</mi><mrow><mi>s</mi><mi>o</mi><mi>l</mi><mi>i</mi><mi>c</mi><mi>i</mi><mi>t</mi><mi>u</mi><mi>d</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>)</mo></mrow>
    </mrow>
    <mi>m</mi>
  </mfrac>
</math>
"""

MATHML_RSD = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mi>R</mi><mi>S</mi><mi>D</mi>
  <mo>=</mo>
  <mfenced open="(" close=")">
    <mfrac>
      <msub><mi>N</mi><mrow><mi>c</mi><mi>o</mi><mi>r</mi><mi>r</mi><mi>e</mi><mi>c</mi><mi>t</mi><mi>o</mi><mi>s</mi></mrow></msub>
      <msub><mi>N</mi><mrow><mi>t</mi><mi>o</mi><mi>t</mi><mi>a</mi><mi>l</mi></mrow></msub>
    </mfrac>
  </mfenced>
  <mo>&#x00D7;</mo>
  <mn>100</mn>
</math>
"""

MATHML_CPE = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mi>C</mi><mi>P</mi><mi>E</mi>
  <mo>=</mo>
  <mfenced open="(" close=")">
    <mfrac>
      <msub><mi>Q</mi><mrow><mi>e</mi><mi>n</mi><mi>t</mi><mi>r</mi><mi>e</mi><mi>g</mi><mi>a</mi><mi>d</mi><mi>a</mi></mrow></msub>
      <msub><mi>Q</mi><mrow><mi>p</mi><mi>r</mi><mi>o</mi><mi>g</mi><mi>r</mi><mi>a</mi><mi>m</mi><mi>a</mi><mi>d</mi><mi>a</mi></mrow></msub>
    </mfrac>
  </mfenced>
  <mo>&#x00D7;</mo>
  <mn>100</mn>
</math>
"""

MATHML_AP = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mi>A</mi><mi>P</mi>
  <mo>=</mo>
  <mfrac>
    <mrow>
      <munderover>
        <mo>&#x2211;</mo>
        <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow>
        <msub><mi>k</mi><mrow><mi>A</mi><mi>P</mi></mrow></msub>
      </munderover>
      <msub><mi>X</mi><mrow><mi>A</mi><mi>P</mi><mo>,</mo><mi>i</mi></mrow></msub>
    </mrow>
    <msub><mi>k</mi><mrow><mi>A</mi><mi>P</mi></mrow></msub>
  </mfrac>
</math>
"""

MATHML_UP = """
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mi>U</mi><mi>P</mi>
  <mo>=</mo>
  <mfrac>
    <mrow>
      <munderover>
        <mo>&#x2211;</mo>
        <mrow><mi>j</mi><mo>=</mo><mn>1</mn></mrow>
        <msub><mi>k</mi><mrow><mi>U</mi><mi>P</mi></mrow></msub>
      </munderover>
      <msub><mi>X</mi><mrow><mi>U</mi><mi>P</mi><mo>,</mo><mi>j</mi></mrow></msub>
    </mrow>
    <msub><mi>k</mi><mrow><mi>U</mi><mi>P</mi></mrow></msub>
  </mfrac>
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
    <mrow><mi>n</mi><mo>(</mo><mi>c</mi><mo>&#x2212;</mo><mn>1</mn><mo>)</mo></mrow>
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
  <msub><mi>r</mi><mrow><mi>r</mi><mi>b</mi></mrow></msub>
  <mo>=</mo>
  <mfrac>
    <mrow><mo>|</mo><mi>Z</mi><mo>|</mo></mrow>
    <msqrt><mi>n</mi></msqrt>
  </mfrac>
</math>
"""


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
        "(International Organization for Standardization [ISO] y International Electrotechnical Commission [IEC], 2023) "
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
        "El estudio se enmarcó en el nivel explicativo, dado que no se limitó a describir las deficiencias del registro "
        "manual ni a correlacionar pasivamente fenómenos administrativos, sino que demostró la relación de causalidad "
        "existente entre la introducción deliberada de la variable independiente (Sistema web SIVAC) y la mejora "
        "cuantificable producida sobre la variable dependiente (Gestión de movimientos de vacunas). De acuerdo con "
        "Hernández-Sampieri et al. (2014), los estudios explicativos tienen como finalidad determinar las causas de "
        "los eventos y establecer en qué condiciones se manifiesta el efecto de un tratamiento experimental sobre "
        "las dimensiones de oportunidad de procesamiento, consistencia documental y satisfacción del usuario.",
        sangria=True
    )

    # ==========================================================================
    # 4.3. Método de investigación
    # ==========================================================================
    agregar_titulo_2(doc, "4.3. Método de investigación")
    agregar_parrafo(
        doc,
        "Se empleó el método hipotético-deductivo, el cual partió de la observación sistemática de las demoras "
        "operativas y discrepancias de saldo en el kardex físico de la cadena de frío provincial, prosiguió con la "
        "formulación de las hipótesis general y específicas fundamentadas en el marco teórico de los sistemas de "
        "información de gestión logística en salud, y culminó con la deducción de consecuencias contrastables "
        "empíricamente mediante pruebas estadísticas de comparación pretest y postest (Hernández-Sampieri et al., 2014). "
        "Este procedimiento garantizó la objetividad en la verificación de las hipótesis planteadas frente a la realidad "
        "operativa de la institución sanitaria.",
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
        "En virtud de este enfoque, las tres dimensiones de la gestión de movimientos de vacunas fueron medidas "
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
        "El diagrama formal que representó el diseño de la investigación fue el siguiente:",
        sangria=True
    )

    insertar_ecuacion_centrada(doc, MATHML_DISENO)

    agregar_parrafo(doc, "Donde:", sangria=False, negrita=True)
    agregar_item_lista(
        doc,
        "**G:** Grupo único experimental conformado por la totalidad censal del personal operativo de inmunizaciones "
        "y cadena de frío de la Dirección de Salud Apurímac II (14 trabajadores).",
        simbolo="•"
    )
    agregar_item_lista(
        doc,
        "**O1:** Medición previa (pre-test) de los indicadores de la gestión de movimientos de vacunas bajo el "
        "procedimiento tradicional manual (libros foliados, cuadernos de cargo y hojas de cálculo aisladas).",
        simbolo="•"
    )
    agregar_item_lista(
        doc,
        "**X:** Aplicación del estímulo experimental, consistente en la puesta en producción y uso operativo del "
        "sistema web SIVAC.",
        simbolo="•"
    )
    agregar_item_lista(
        doc,
        "**O2:** Medición posterior (post-test) de los mismos seis indicadores de la gestión de movimientos de "
        "vacunas ejecutada mediante el sistema web SIVAC.",
        simbolo="•"
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
        "La unidad de análisis estuvo constituida por cada operador técnico y administrativo de la cadena de "
        "inmunizaciones de la Dirección de Salud Apurímac II (sujetos S-01 a S-14), conjuntamente con las transacciones "
        "documentales de movimiento de productos biológicos y vales oficiales de salida ejecutados por dicho personal "
        "durante los periodos simétricos de observación del pre-test y post-test.",
        sangria=True
    )

    # ==========================================================================
    # 4.9. Operacionalización de variables
    # ==========================================================================
    agregar_titulo_2(doc, "4.9. Operacionalización de variables")

    agregar_titulo_3(doc, "4.9.1. Variable independiente: Sistema web SIVAC")
    agregar_parrafo(
        doc,
        "El sistema web SIVAC se definió conceptualmente como la plataforma informática transaccional de arquitectura "
        "cliente-servidor de tres capas construida bajo la metodología ágil Extreme Programming (Beck, 1999) y evaluada "
        "conforme al modelo de calidad de producto ISO/IEC 25010:2023 (ISO y IEC, 2023). Operacionalmente, el sistema "
        "automatizó el control de inventario por lotes bajo la regla FEFO (primero en expirar, primero en salir), el "
        "registro de movimientos de entradas, salidas, reajustes y mermas, y la emisión inmediata de comprobantes de "
        "salida en formato electrónico estandarizado.",
        sangria=True
    )

    agregar_titulo_3(doc, "4.9.2. Variable dependiente: Gestión de movimientos de vacunas")
    agregar_parrafo(
        doc,
        "La gestión de movimientos de vacunas se definió conceptualmente como el proceso técnico-administrativo y "
        "logístico que regula la recepción, conservación, registro contable en kardex y distribución de productos "
        "biológicos e insumos complementarios a través de los niveles de la cadena de frío sanitaria (Ministerio de "
        "Salud, 2022). Operacionalmente, esta variable fue medida mediante tres dimensiones oficiales: oportunidad de "
        "procesamiento, consistencia documental y satisfacción del usuario, desglosadas en seis indicadores "
        "cuantitativos cuyos atributos descriptivos se presentan en la Tabla 10.",
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
            "Plataforma tecnológica web desarrollada mediante las fases de la metodología ágil Extreme Programming y verificada bajo los atributos del estándar ISO/IEC 25010:2023.",
            "Planificación\n\nDiseño\n\nCodificación\n\nPruebas",
            "Historias de usuario y plan de entregas\n\nArquitectura de datos y prototipos de interfaz\n\nMódulos transaccionales e integración continua\n\nPruebas unitarias y pruebas de aceptación",
            "Cumplimiento de artefactos de ingeniería y casos de prueba",
            "Nominal / De razón"
        ],
        [
            "**Variable Dependiente:**\nGestión de movimientos de vacunas",
            "Desempeño integral del proceso de registro, control documental y despacho de biológicos evaluado en tiempos de ejecución, exactitud de asientos y percepción del operador.",
            "1. Oportunidad de procesamiento",
            "Tiempo de registro de movimiento de vacunas\n\nTiempo de emisión de comprobante de salida o vale",
            "Minutos cronometrados por transacción",
            "De razón (continua)"
        ],
        [
            "**Variable Dependiente:**\nGestión de movimientos de vacunas",
            "Desempeño integral del proceso de registro, control documental y despacho de biológicos evaluado en tiempos de ejecución, exactitud de asientos y percepción del operador.",
            "2. Consistencia documental",
            "Porcentaje de registros sin discrepancias\n\nConcordancia de cantidad programada versus entregada",
            "Porcentaje de exactitud y cumplimiento documental",
            "De razón (0% a 100%)"
        ],
        [
            "**Variable Dependiente:**\nGestión de movimientos de vacunas",
            "Desempeño integral del proceso de registro, control documental y despacho de biológicos evaluado en tiempos de ejecución, exactitud de asientos y percepción del operador.",
            "3. Satisfacción del usuario",
            "Aceptación del proceso\n\nUtilidad percibida",
            "Puntaje en cuestionario psicométrico bajo el modelo TAM",
            "Ordinal (Likert de 1 a 5)"
        ]
    ]
    agregar_tabla_datos(
        doc,
        numero="10",
        titulo="Operacionalización de las variables de investigación",
        encabezados=headers_t10,
        filas=filas_t10,
        nota="Estructura metodológica de variables, dimensiones, indicadores, unidades de medida y escalas de valoración del estudio.",
        col_widths=[Inches(0.98), Inches(1.38), Inches(0.93), Inches(1.23), Inches(0.84), Inches(0.74)],
        font_size_pt=9.0
    )

    agregar_parrafo(
        doc,
        "La cuantificación matemática de los seis indicadores de la variable dependiente se efectuó en el cuerpo "
        "analítico del estudio mediante las expresiones formales que se detallan a continuación.",
        sangria=True
    )

    # Ecuación (1): T_reg
    agregar_parrafo(
        doc,
        "El primer indicador de la dimensión oportunidad de procesamiento, correspondiente al tiempo de registro de "
        "movimiento de vacunas, se cuantificó mediante la media aritmética de los intervalos cronometrados por "
        "operador, expresada en la Ecuación 1:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_TREG, numero_eq=1)
    agregar_parrafo(
        doc,
        "Donde el término de resultado representa el tiempo promedio de registro de movimientos en minutos, los "
        "instantes inicial y final corresponden a la apertura y conclusión formal de cada asiento transaccional, y "
        "el denominador indica el número total de transacciones observadas por operador.",
        sangria=True
    )

    # Ecuación (2): T_vale
    agregar_parrafo(
        doc,
        "El segundo indicador de la primera dimensión, referido al tiempo de emisión de comprobante de salida o vale, "
        "se determinó a través del promedio de duración de la generación documental del despacho, según la Ecuación 2:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_TVALE, numero_eq=2)
    agregar_parrafo(
        doc,
        "Donde el indicador expresa el tiempo promedio de emisión del comprobante de salida en minutos, calculado a "
        "partir de la diferencia entre el instante de impresión o exportación del documento oficial y el instante de "
        "solicitud de despacho sobre el total de vales emitidos.",
        sangria=True
    )

    # Ecuación (3): RSD
    agregar_parrafo(
        doc,
        "En la segunda dimensión, consistente en la consistencia documental, el porcentaje de registros sin "
        "discrepancias se calculó como la razón porcentual de asientos que cumplieron simultáneamente los ocho "
        "criterios de auditoría técnica respecto al total de registros evaluados, conforme a la Ecuación 3:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_RSD, numero_eq=3)
    agregar_parrafo(
        doc,
        "Donde el numerador contabiliza el número de movimientos auditados que aprobaron de forma simultánea los ocho "
        "criterios de control interno (identificación del biológico, código de lote, fecha de vencimiento, cantidad "
        "física, centro de origen o destino, identificación del responsable, exactitud del saldo aritmético y "
        "correlatividad cronológica) y el denominador representa el total de asientos revisados en el periodo.",
        sangria=True
    )

    # Ecuación (4): CPE
    agregar_parrafo(
        doc,
        "El segundo indicador de la dimensión consistencia documental, denominado concordancia de cantidad programada "
        "versus entregada, midió el grado de exactitud volumétrica en la ejecución de las órdenes de distribución "
        "mediante la Ecuación 4:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_CPE, numero_eq=4)
    agregar_parrafo(
        doc,
        "Donde el numerador representa la cantidad de dosis y diluyentes efectivamente despachados y conciliados en "
        "conformidad con el acta de recepción, y el denominador expresa la cantidad total programada en el "
        "requerimiento oficial del establecimiento de salud.",
        sangria=True
    )

    # Ecuación (5): AP
    agregar_parrafo(
        doc,
        "Dentro de la tercera dimensión, orientada a la satisfacción del usuario bajo el Modelo de Aceptación "
        "Tecnológica de Davis (1989), el indicador de aceptación del proceso se obtuvo promediando las calificaciones "
        "asignadas por cada operador a los reactivos de adecuación del flujo de trabajo, como se define en la Ecuación 5:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_AP, numero_eq=5)
    agregar_parrafo(
        doc,
        "Donde cada término del sumatorio corresponde a la puntuación ordinal otorgada por el operador en la escala "
        "de cinco niveles y el denominador representa el número de reactivos que integran la subescala de aceptación "
        "del proceso.",
        sangria=True
    )

    # Ecuación (6): UP
    agregar_parrafo(
        doc,
        "Finalmente, el indicador de utilidad percibida cuantificó la valoración del personal respecto a la eficacia "
        "instrumental del sistema para optimizar su desempeño laboral en la cadena de frío, calculándose mediante la "
        "Ecuación 6:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_UP, numero_eq=6)
    agregar_parrafo(
        doc,
        "Donde el numerador acumula las puntuaciones asignadas en los reactivos de eficacia y control logístico de "
        "la subescala correspondiente y el denominador indica la cantidad total de ítems evaluados en dicho componente.",
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
        "En correspondencia directa con las técnicas descritas, se diseñaron y aplicaron tres instrumentos de "
        "medición compuestos por un total de treinta y dos (32) ítems o criterios de evaluación: (a) el Instrumento "
        "N.° 01, Ficha de observación de tiempos cronometrados (8 ítems de control temporal); (b) el Instrumento "
        "N.° 02, Guía de cotejo de consistencia documental (8 ítems de auditoría sobre los ocho criterios de "
        "conformidad); y (c) el Instrumento N.° 03, Cuestionario de satisfacción del usuario bajo el modelo TAM "
        "(16 ítems en escala Likert de cinco puntos: 1 = Totalmente en desacuerdo, 2 = En desacuerdo, 3 = Neutral, "
        "4 = De acuerdo y 5 = Totalmente de acuerdo). En la Tabla 11 se sintetiza la correspondencia entre dimensiones, "
        "indicadores, técnicas e instrumentos.",
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
            "8 ítems de medición cronométrica en baterías estandarizadas de registro y despacho"
        ],
        [
            "2. Consistencia documental",
            "Porcentaje de registros sin discrepancias\n\nConcordancia de cantidad programada versus entregada",
            "Análisis documental y auditoría de kardex",
            "Instrumento N.° 02:\nGuía de cotejo de consistencia documental",
            "8 ítems de verificación dicotómica bajo los ocho criterios de conformidad contable"
        ],
        [
            "3. Satisfacción del usuario",
            "Aceptación del proceso\n\nUtilidad percibida",
            "Encuesta psicométrica estructurada",
            "Instrumento N.° 03:\nCuestionario de satisfacción del usuario (Modelo TAM)",
            "16 reactivos en escala ordinal Likert de 1 a 5 puntos distribuidos por subescalas"
        ]
    ]
    agregar_tabla_datos(
        doc,
        numero="11",
        titulo="Relación de técnicas e instrumentos de recolección de datos por dimensión e indicador",
        encabezados=headers_t11,
        filas=filas_t11,
        nota="Correspondencia metodológica entre las tres dimensiones de la variable dependiente y los tres instrumentos validados.",
        col_widths=[Inches(1.13), Inches(1.43), Inches(1.08), Inches(1.28), Inches(1.18)],
        font_size_pt=9.5
    )

    # ==========================================================================
    # 4.11. Confiabilidad de los instrumentos
    # ==========================================================================
    agregar_titulo_2(doc, "4.11. Confiabilidad de los instrumentos")
    agregar_parrafo(
        doc,
        "La confiabilidad se refiere al grado en que la aplicación repetida de un instrumento al mismo sujeto u "
        "objeto produce resultados consistentes y coherentes (Hernández-Sampieri et al., 2014). Para los Instrumentos "
        "N.° 01 (Ficha de observación de tiempos cronometrados) y N.° 02 (Guía de cotejo de consistencia documental), "
        "la confiabilidad estuvo garantizada por su naturaleza de medición física y de auditoría objetiva no "
        "psicométrica: el primero empleó cronometraje digital calibrado con precisión centesimal sobre puntos de "
        "inicio y corte inequívocos, mientras que el segundo aplicó una verificación dicotómica de cumplimiento "
        "simultáneo sobre ocho criterios normativos de control de inventario, eliminando la subjetividad del evaluador.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Para el Instrumento N.° 03 (Cuestionario de satisfacción del usuario bajo el modelo TAM, conformado por 16 "
        "ítems politómicos en escala Likert de 1 a 5), la confiabilidad por consistencia interna se determinó mediante "
        "el coeficiente Alfa de Cronbach, cuya formulación matemática se presenta en la Ecuación 7:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_ALFA, numero_eq=7)
    agregar_parrafo(
        doc,
        "Donde el coeficiente representa el índice Alfa de Cronbach, el parámetro de dimensión indica el número de "
        "ítems del cuestionario (16 reactivos), el sumatorio acumula las varianzas individuales de cada ítem y el "
        "denominador corresponde a la varianza de los puntajes totales observados. En estricto cumplimiento del "
        "principio de integridad científica y cero invención de datos empíricos, el coeficiente Alfa de Cronbach "
        "de la aplicación definitiva se registra como [Pendiente de cálculo tras levantamiento de campo], considerándose "
        "como umbral mínimo aceptable un valor igual o superior a 0.70 (Hernández-Sampieri et al., 2014).",
        sangria=True
    )

    # ==========================================================================
    # 4.12. Validez de los instrumentos
    # ==========================================================================
    agregar_titulo_2(doc, "4.12. Validez de los instrumentos")
    agregar_parrafo(
        doc,
        "La validez de contenido determinó el grado en que los instrumentos reflejaron un dominio específico de "
        "contenido de las dimensiones medidas (Hernández-Sampieri et al., 2014). Este proceso se ejecutó mediante "
        "el técnica de juicio de tres (3) expertos con grado académico de Magíster e Ingeniero de Sistemas y "
        "experiencia acreditada en ingeniería de software y gestión sanitaria, quienes evaluaron los treinta y dos (32) "
        "ítems del expediente instrumental bajo cinco criterios: suficiencia, relevancia, coherencia, claridad y "
        "redacción, utilizando una escala ordinal de cuatro niveles (1 = No cumple a 4 = Alto nivel). La cuantificación "
        "de la concordancia se realizó mediante el Coeficiente V de Aiken, expresado en la Ecuación 8, complementado "
        "con el Índice de Validez de Contenido (IVC) de Tristán-López (2008):",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_AIKEN, numero_eq=8)
    agregar_parrafo(
        doc,
        "Donde el numerador representa la sumatoria de los puntajes asignados por los expertos disminuidos en el valor "
        "mínimo de la escala, el primer factor del denominador indica el número de jueces evaluadores (tres expertos) "
        "y el segundo factor corresponde a la amplitud de la escala de valoración (cuatro categorías). En la Tabla 12 "
        "se expone el consolidado de la validación por juicio de expertos, cuyo resultado global alcanzó un Coeficiente "
        "V de Aiken de 0.98 y un Índice de Validez de Contenido de 1.00, superando el umbral crítico de 0.80 establecido "
        "por Tristán-López (2008) y ratificando la plena aplicabilidad de los instrumentos.",
        sangria=True
    )

    headers_t12 = [
        "N.°",
        "Juez Experto Evaluador",
        "Grado Académico y Registro",
        "Especialidad Profesional",
        "V de Aiken",
        "IVC",
        "Dictamen"
    ]
    filas_t12 = [
        [
            "1",
            "M.Sc. Iván Soria Solís",
            "Magíster Scientiae en Informática\nCIP N.° 184521",
            "Tecnologías de la Información, Sistemas y Métodos",
            "0.98",
            "1.00",
            "Aprobado / Aplicable"
        ],
        [
            "2",
            "M.Sc. Daniel Minaya Gutiérrez",
            "Magíster en Informática y Sistemas\nCIP N.° 197842",
            "Calidad de Software y Métodos Cuantitativos",
            "0.99",
            "1.00",
            "Aprobado / Aplicable"
        ],
        [
            "3",
            "M.Sc. Javier Ramos Gonzales",
            "Magíster en Ingeniería de Sistemas\nCIP N.° 210455",
            "Sistemas de Información y Arquitectura Web",
            "0.98",
            "1.00",
            "Aprobado / Aplicable"
        ],
        [
            "**Prom.**",
            "**Consolidado Global del Panel de Expertos**",
            "**3 Jueces Calificados**",
            "**Evaluación Integral de 32 Ítems (Instrumentos 01, 02 y 03)**",
            "**0.98**",
            "**1.00**",
            "**Validez Excelente**"
        ]
    ]
    agregar_tabla_datos(
        doc,
        numero="12",
        titulo="Consolidado de validación de los instrumentos por juicio de expertos",
        encabezados=headers_t12,
        filas=filas_t12,
        nota="Resultados obtenidos a partir de las constancias de validación suscritas por los tres expertos bajo el modelo institucional de la EPIS-UNAJMA.",
        col_widths=[Inches(0.44), Inches(1.33), Inches(1.23), Inches(1.33), Inches(0.59), Inches(0.49), Inches(0.69)],
        font_size_pt=9.0
    )

    # ==========================================================================
    # 4.13. Técnicas estadísticas para el procesamiento de la información
    # ==========================================================================
    agregar_titulo_2(doc, "4.13. Técnicas estadísticas para el procesamiento de la información")
    agregar_parrafo(
        doc,
        "El procesamiento estadístico de los datos recolectados en el pre-test y post-test se estructuró mediante "
        "rutinas computacionales reproducibles en el lenguaje Python (librerías científicas scipy.stats, statsmodels "
        "y pingouin) y el entorno bioestadístico R. En la primera fase se aplicó la estadística descriptiva para cada "
        "uno de los seis indicadores en ambas etapas experimentales, calculando medidas de tendencia central (media "
        "aritmética y mediana), medidas de dispersión (desviación estándar y rango intercuartílico) y valores extremos "
        "(mínimo y máximo).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "En la segunda fase, previa a la contrastación de hipótesis y dado el tamaño de la población censal (n = 14), "
        "se estableció la verificación del supuesto de normalidad sobre las diferencias intrasujeto entre el post-test "
        "y el pre-test mediante la prueba de Shapiro-Wilk a un nivel de significancia de 0.05. Cuando las diferencias "
        "pareadas se ajustan a una distribución normal (valor de probabilidad superior a 0.05), se aplica la prueba "
        "paramétrica t de Student para muestras relacionadas, definida en la Ecuación 9:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_T_STUDENT, numero_eq=9)
    agregar_parrafo(
        doc,
        "Donde el numerador representa la media aritmética de las diferencias pareadas entre el post-test y el pre-test, "
        "el denominador incluye la desviación estándar de dichas diferencias dividida por la raíz cuadrada del tamaño "
        "censal (14 operadores). De forma complementaria y como prueba principal ante distribuciones asimétricas o "
        "escalas ordinales (valor de probabilidad menor o igual a 0.05 en Shapiro-Wilk), se aplica la prueba no "
        "paramétrica de rangos con signo de Wilcoxon para muestras pareadas, cuya aproximación normal se expresa en "
        "la Ecuación 10:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_WILCOXON, numero_eq=10)
    agregar_parrafo(
        doc,
        "Donde el estadístico de suma de rangos cuantifica las diferencias positivas o negativas ordenadas por magnitud "
        "y el parámetro poblacional corresponde al número de pares evaluados. Finalmente, para determinar la magnitud "
        "práctica de la mejora lograda por el sistema web SIVAC más allá de la significancia estadística, se incluyó "
        "el cálculo del tamaño del efecto mediante el coeficiente de correlación rango-biserial o índice no paramétrico "
        "propuesto por Cohen (1988), formulado en la Ecuación 11:",
        sangria=True
    )
    insertar_ecuacion_centrada(doc, MATHML_EFECTO_R, numero_eq=11)
    agregar_parrafo(
        doc,
        "Donde el valor absoluto del estadístico estandarizado se divide entre la raíz cuadrada del número de sujetos "
        "observados, interpretándose la magnitud del efecto como pequeña (alrededor de 0.10), moderada (alrededor de "
        "0.30) o grande (igual o superior a 0.50) conforme a los criterios canónicos de Cohen (1988).",
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
