#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expediente COMPLETO de validacion por juicio de expertos (documento para
revision por juicio de expertos, sin dictamen preemitido), tres ejemplares
identicos en blanco.

Esquema v05 (encargo expreso del tesista, 2026-10-19): TRES hojas de
evaluacion de contenido POR experto, una por dimension de la variable
dependiente (DEC-007):
  - Hoja N.° 01: Instrumento N.° 01 (Ficha de tiempos cronometrados),
    Dimension 1 Oportunidad de procesamiento (elementos del protocolo Treg y
    Tvale).
  - Hoja N.° 02: Instrumento N.° 02 (Ficha de cotejo documental),
    Dimension 2 Consistencia documental (elementos y criterios RSD y CPE).
  - Certificado N.° 03: Instrumento N.° 03 Modalidad A, Dimension 3
    Satisfaccion del usuario (los mismos 8 reactivos AP/UP literales).
La variable independiente sigue SOLO informativa (hoja de definicion
operacional, intervencion dicotomica X0/X1, sin PU/PE). Revisar las hojas
NO equivale a contestar datos ni preguntas de percepcion. Columnas de las
hojas: N.° | Elementos de la ficha/protocolo | Pertinencia Si/No |
Relevancia Si/No | Claridad Si/No | Sugerencias. Cada hoja lleva su propio
bloque de cierre en blanco. Adaptacion editorial del modelo Fany 2024 (no
replica exacta; bordado APA 7 del motor). No se restablecen los 8 enunciados
nuevos D1/D2 de la v03. ICC y kappa permanecen como estimadores de
CONFIABILIDAD (no validez); sin coeficientes calculados, sin nuevos umbrales
ni nuevas escalas. Ningun campo lleva calificaciones ni datos ficticios.

Orden de piezas (cada una inicia en pagina nueva):
  1. Carta de presentacion al juez (anuncia las 3 hojas y los 3 instrumentos).
  2. Instrucciones para el juez validador (alcance por hoja).
  3. Hoja informativa: definicion operacional de la intervencion tecnologica.
  4. Panorama de las tres dimensiones (tabla Dimension-Instrumento-Hoja).
  5. Hoja de evaluacion N.° 01 (apaisada): Ficha N.° 01.
  6. Hoja de evaluacion N.° 02 (apaisada): Ficha N.° 02.
  7. Certificado de validez de contenido del Instrumento N.° 03 (Modalidad A).
  8. Instrumento N.° 03 integro (Modalidades A y B, con baremo y protocolo).
  9. Matriz de consistencia (en bloques por problema, para no partir filas).
 10. Matriz de operacionalizacion de variables.
 11. Ficha N.° 01 completa (elementos evaluados en la hoja N.° 01; no se llena).
 12. Ficha N.° 02 completa (elementos evaluados en la hoja N.° 02; no se llena).

Los elementos de las hojas N.° 01 y N.° 02 (ELEMENTOS_HOJA_01/02) se
concilian con el inventario JSON trazable de campos/protocolos encargado al
especialista-instrumentos; las listas de este generador derivan del contenido
ya validado de las fichas y se ajustaran si el inventario aporta campos
adicionales.

Uso:
  --generar          escribe EXPEDIENTE_VALIDACION_SIVAC_COMPLETO_EXPERTO_0N_v05.docx,
                     verifica el archivo guardado y borra el ejemplar si no es conforme.
  --verificar        audita en disco los DOCX v05 ya generados.
  --verificar-pdf P  audita paginacion de un PDF exportado (P = ruta del PDF).
"""
import argparse
import re
import sys
from pathlib import Path

import docx
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Pt, RGBColor

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts" / "utilidades"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import docx_quirurgico as quir  # noqa: E402
import generar_anexo2_validacion_fany as fany  # noqa: E402

RUTA_SALIDA = RAIZ / "salidas" / "documentos" / "anexos_fany"
FUENTE = "Times New Roman"
VERSION = "v05"

TITULO_TESIS = ("APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS MENSUALES DE "
                "VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II")
TESISTA = "Bach. José Luis Quispe León"
ANIO = "2026"

# Anchos utiles en dxa por geometria de seccion (margenes A4: izq 3.0 cm y
# 2.5 cm en los demas lados en retrato; 2.5 cm en apaisada). Recalculados:
#   retrato  : 21.0 - 3.0 - 2.5 = 15.5 cm = 8788 dxa
#   apaisada : 29.7 - 2.5 - 2.5 = 24.7 cm = 14000 dxa (redondeado del motor)
ANCHO_RETRATO = quir.ANCHO_UTIL_PORTRAIT_DXA      # 8788
ANCHO_APAISADA = quir.ANCHO_UTIL_LANDSCAPE_DXA    # 14000
GEOMETRIAS = {
    "unajma": dict(w=21.0, h=29.7, l=3.0, r=2.5, t=2.5, b=2.5, orient=WD_ORIENT.PORTRAIT),
    "apaisada": dict(w=29.7, h=21.0, l=2.5, r=2.5, t=2.5, b=2.5, orient=WD_ORIENT.LANDSCAPE),
}

TAM_CUERPO = 12
TAM_TABLA = 10

TITULO_CERT_03 = ("CERTIFICADO DE VALIDEZ DE CONTENIDO DEL INSTRUMENTO N.° 03: "
                  "CUESTIONARIO DE SATISFACCIÓN CON EL PROCESO OPERATIVO (MODALIDAD A)")
SUBTITULO_CERT_03 = ("Variable dependiente: Gestión de movimientos mensuales de vacunas. "
                     "Dimensión: Satisfacción del usuario.")
TITULO_HOJA_VI = "DEFINICIÓN OPERACIONAL DE LA INTERVENCIÓN TECNOLÓGICA SIVAC"
TITULO_INSTRUCCIONES = "INSTRUCCIONES PARA EL JUEZ VALIDADOR"
TITULO_PANORAMA = "PANORAMA DE LAS TRES DIMENSIONES Y SUS CERTIFICADOS DE EVALUACIÓN"
TITULO_HOJA_01 = ("CERTIFICADO DE VALIDEZ DE CONTENIDO DEL INSTRUMENTO N.° 01: FICHA DE "
                  "OBSERVACIÓN SISTEMÁTICA Y MEDICIÓN DE TIEMPOS CRONOMETRADOS")
SUBTITULO_HOJA_01 = ("Evaluación de elementos, campos y criterios del protocolo de la ficha. "
                     "Variable dependiente: Gestión de movimientos mensuales de vacunas. "
                     "Dimensión 1: Oportunidad de procesamiento.")
TITULO_HOJA_02 = ("CERTIFICADO DE VALIDEZ DE CONTENIDO DEL INSTRUMENTO N.° 02: FICHA DE "
                  "REGISTRO Y COTEJO DOCUMENTAL DE CONSISTENCIA")
SUBTITULO_HOJA_02 = ("Evaluación de elementos, campos y criterios del protocolo de la ficha. "
                     "Variable dependiente: Gestión de movimientos mensuales de vacunas. "
                     "Dimensión 2: Consistencia documental.")
FINALIDAD = "Documento para revisión por juicio de expertos"

# Reactivos LITERALES de la Modalidad A (fuente: Anexo 2 Fany / Instrumento N.° 03).
ITEMS_AP = [
    "El procedimiento actual para asentar los movimientos diarios y cierres de mes es ágil y no demanda un esfuerzo mental o físico excesivo.",
    "El flujo de trabajo requerido para emitir comprobantes de salida y vales de entrega es fluido y está libre de demoras o trabas burocráticas.",
    "El método empleado me permite conciliar los saldos de inventario con las microredes generando tranquilidad y reduciendo el estrés laboral.",
    "El tiempo que dedico al registro administrativo de vacunas es equilibrado y me deja disponibilidad para mis labores sanitarias y asistenciales.",
]
ITEMS_UP = [
    "El mecanismo de registro utilizado me permite disponer de información fidedigna y en tiempo real del stock de vacunas y jeringas.",
    "El control de números de lote y fechas de vencimiento que brinda el proceso previene oportunamente mermas o pérdidas de biológicos.",
    "La metodología de gestión facilita la detección inmediata y rectificación de cualquier descuadre de inventario físico versus registrado.",
    "En general, considero que el procedimiento empleado es una herramienta altamente eficaz para garantizar el abastecimiento oportuno de vacunas.",
]
GRUPO_AP = "Indicador: Aceptación del proceso (AP-01 a AP-04)"
GRUPO_UP = "Indicador: Utilidad percibida (UP-01 a UP-04)"
ACLARACION_CERT = ("Este certificado corresponde a los ocho reactivos de la Modalidad A; no certifica por sí solo "
                   "las otras dimensiones de la variable dependiente, cuyo contenido se somete a juicio en las "
                   "hojas de evaluación N.° 01 y N.° 02, ni la aplicación de la intervención o la confiabilidad, "
                   "que se estima según el plan vigente del estudio.")

# Elementos de las hojas de evaluacion N.° 01 y N.° 02: derivan del contenido
# REAL de las fichas (protocolo de cronometraje y criterios de conformidad).
# Revisar estos elementos NO equivale a contestar datos ni preguntas de
# percepcion; el juez emite juicio de contenido (Sí/No) y sugerencias.
# La conciliacion final con el inventario JSON trazable del
# especialista-instrumentos (campos/protocolos 01/02) se registrara en la
# verificacion; estas listas cubren protocolo, secciones de registro y
# consolidacion de cada ficha.
ELEMENTOS_HOJA_01 = [
    "Datos generales de la observación: identificación del operador (TRAB-01 a TRAB-14), rol institucional, "
    "sede, red o microred y provincia.",
    "Momento de medición: pretest (kardex físico, libros de registro y hojas de cálculo) o postest (sistema "
    "SIVAC), con fecha de la observación.",
    "Instrumento de medición: cronómetro digital con precisión de centésimas de segundo; el tiempo se expresa "
    "en minutos decimales (minutos enteros más segundos divididos entre 60).",
    "Punto de inicio y de fin del indicador Treg: desde que el operador toma el documento fuente o abre la "
    "interfaz para digitar el movimiento, hasta que el movimiento queda grabado, confirmado o asentado con "
    "saldo actualizado.",
    "Punto de inicio y de fin del indicador Tvale: desde que el operador recibe la solicitud de biológicos, "
    "hasta que el vale queda generado, firmado o impreso con numeración correlativa.",
    "Regla de interrupciones: ante eventos ajenos al proceso (corte de energía, sismo, emergencia sanitaria) "
    "el cronómetro se detiene y se registra solo el tiempo neto de trabajo.",
    "Esquema de tareas: cada operador ejecuta tres tareas de registro (REG-01 a REG-03) y tres de emisión de "
    "vales (VALE-01 a VALE-03), estandarizadas por complejidad.",
    "Registro por tarea: hora de inicio, hora de fin, tiempo neto (min:s) y tiempo en minutos decimales, con "
    "columna de incidencias.",
    "Consolidación: las tres mediciones de cada indicador se resumen en un único valor representativo por "
    "operador y momento (promedio y mediana), en minutos.",
]

ELEMENTOS_HOJA_02 = [
    "Datos generales de la auditoría documental: identificación del operador o centro auditado (TRAB-01 a "
    "TRAB-14), centro de acopio o microred y provincia sanitaria.",
    "Momento de medición: pretest (kardex manual, cuadernos y hojas de cálculo) o postest (base de datos y "
    "vales electrónicos de SIVAC), con ventana de auditoría de 30 días calendario.",
    "Regla de conformidad RSD: un registro es conforme (1) solo cuando cumple simultáneamente los ocho "
    "criterios; si incumple al menos uno, es no conforme (0).",
    "Criterio C1: tipo de movimiento clasificado de forma unívoca (entrada por remesa, salida a "
    "establecimiento o ajuste).",
    "Criterio C2: denominación oficial estandarizada del biológico según el esquema regular nacional.",
    "Criterio C3: identificación exacta del número de lote, coincidente con el rótulo del frasco.",
    "Criterio C4: cantidad de dosis o viales exacta y coincidente con el stock físico y el acta de recepción.",
    "Criterio C5: fecha del movimiento consignada completa (día, mes y año) y en secuencia cronológica.",
    "Criterio C6: establecimiento de origen o destino individualizado con su código oficial.",
    "Criterio C7: nombre, firma o usuario responsable del despacho o recepción plenamente trazable.",
    "Criterio C8: documento formal de respaldo asociado y verificado (vale oficial, PECOSA o guía de remisión).",
    "Corpus de auditoría RSD: 40 a 60 registros por ventana temporal, sobre el catálogo de vacunas e insumos "
    "del esquema regular, con veredicto (1/0) y tipo de discrepancia o causa.",
    "Regla de concordancia CPE: una entrega es concordante (1) si la cantidad entregada es idéntica a la "
    "programada o si, siendo distinta, existe un documento oficial archivado que autoriza expresamente la "
    "variación; en cualquier otro caso es no concordante (0).",
    "Registro CPE por entrega: número de documento (vale), cantidad programada, cantidad entregada, diferencia "
    "absoluta, justificación formal acreditada (Sí/No/No aplica), veredicto (1/0) y causa del desfase.",
    "Consolidación: totales de registros y entregas evaluadas, y porcentaje resultante de cada indicador "
    "(RSD y CPE) por momento de medición.",
]

# Encabezados comunes de las hojas de evaluacion de contenido (columna
# elementos + 3 criterios Sí/No + sugerencias), en apaisada.
ENCABEZADOS_HOJA = ["N.°", "Elementos de la ficha / protocolo", "Pertinencia", "", "Relevancia", "", "Claridad",
                    "", "Sugerencias"]

# Ecuaciones narrativas del cuestionario en MathML (el motor las convierte a
# OMML nativo). Las formulas de Treg/Tvale/RSD/CPE pertenecen a las Fichas y se
# citan como protocolo; no se duplican ecuaciones dentro de tablas.
MML_SUBESCALA = """<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mrow><mtext>Puntaje Subescala</mtext><mo>=</mo><munderover><mo>&#x2211;</mo><mrow><mi>j</mi><mo>=</mo><mn>1</mn></mrow><mn>4</mn></munderover><msub><mi>X</mi><mi>j</mi></msub></mrow>
</math>"""
MML_GLOBAL = """<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mrow><mtext>Puntaje Global</mtext><mo>=</mo><munderover><mo>&#x2211;</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mn>8</mn></munderover><msub><mi>X</mi><mi>i</mi></msub></mrow>
</math>"""
MML_ALFA = """<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mrow><mi>&#x3B1;</mi><mo>=</mo><mfrac><mi>k</mi><mrow><mi>k</mi><mo>&#x2212;</mo><mn>1</mn></mrow></mfrac><mrow><mo>(</mo><mn>1</mn><mo>&#x2212;</mo><mfrac><mrow><munderover><mo>&#x2211;</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>k</mi></munderover><msubsup><mi>&#x3C3;</mi><mi>i</mi><mn>2</mn></msubsup></mrow><msubsup><mi>&#x3C3;</mi><mi>t</mi><mn>2</mn></msubsup></mfrac><mo>)</mo></mrow></mrow>
</math>"""
MML_OMEGA = """<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mrow><mi>&#x3C9;</mi><mo>=</mo><mfrac><msup><mrow><mo>(</mo><munderover><mo>&#x2211;</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>k</mi></munderover><msub><mi>&#x3BB;</mi><mi>i</mi></msub><mo>)</mo></mrow><mn>2</mn></msup><mrow><msup><mrow><mo>(</mo><munderover><mo>&#x2211;</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>k</mi></munderover><msub><mi>&#x3BB;</mi><mi>i</mi></msub><mo>)</mo></mrow><mn>2</mn></msup><mo>+</mo><munderover><mo>&#x2211;</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>k</mi></munderover><mrow><mo>(</mo><mn>1</mn><mo>&#x2212;</mo><msubsup><mi>&#x3BB;</mi><mi>i</mi><mn>2</mn></msubsup><mo>)</mo></mrow></mrow></mfrac></mrow>
</math>"""

# Notas al pie del certificado (definicion Claridad CORREGIDA; sin texto corrupto).
NOTA_1 = "Pertinencia: El ítem corresponde al concepto teórico formulado."
NOTA_2 = "Relevancia: El ítem es apropiado para representar al componente o dimensión específica del constructo."
NOTA_3 = "Claridad: El enunciado se entiende sin dificultad; es conciso, exacto y directo."
NOTA_SUF = ("Suficiencia: hay suficiencia cuando los ítems planteados cubren de manera completa la dimensión "
            "evaluada.")

# Reactivos LITERALES de la Modalidad B (módulo anexo TAM; NO son dimensiones de la VI).
ITEMS_PU = [
    "Utilizar el sistema SIVAC agiliza notablemente el registro de entradas, salidas y transferencias de dosis de vacunas en mi centro.",
    "SIVAC me permite consultar de manera inmediata y precisa los saldos de existencias por lote en cualquier momento que lo requiera.",
    "La generación automática de vales oficiales en formato PDF en SIVAC facilita enormemente el despacho hacia los establecimientos de salud.",
    "En conjunto, SIVAC incrementa mi productividad y mejora significativamente el control de la cadena de frío en mi jurisdicción.",
]
ITEMS_PE = [
    "La interfaz gráfica de SIVAC es clara, intuitiva, limpia y sus botones y opciones de navegación son fácilmente comprensibles.",
    "Aprender a operar los módulos de movimientos, lotes y reportes de SIVAC fue sencillo y demandó poco tiempo de capacitación.",
    "Los mensajes de confirmación, validación de stock y advertencias que emite el sistema SIVAC son claros y orientan mis acciones.",
    "Me resulta fácil lograr que SIVAC ejecute con exactitud las tareas operativas que necesito realizar en mi jornada de trabajo.",
]

# Marcadores de inicio de pieza, en el orden obligatorio.
MARCADORES = [
    "Andahuaylas, ",
    TITULO_INSTRUCCIONES,
    TITULO_HOJA_VI,
    TITULO_PANORAMA,
    TITULO_HOJA_01,
    TITULO_HOJA_02,
    "CERTIFICADO DE VALIDEZ DE CONTENIDO DEL INSTRUMENTO N.° 03",
    "INSTRUMENTO N.° 03",
    "MATRIZ DE CONSISTENCIA",
    "MATRIZ DE OPERACIONALIZACIÓN DE VARIABLES",
    "INSTRUMENTO N.° 01",
    "INSTRUMENTO N.° 02",
]

# Textos PROHIBIDOS: legado v03 excluido por el dictamen y marcas prellenadas.
EXCLUIDOS = [
    "(Sin el sistema / tras la implantación",                       # 8 enunciados nuevos D1/D2 de v03
    "Dimensión 1: Utilidad percibida del software SIVAC",           # rótulo PU como dimensión de la VI (v03)
    "Dimensión 2: Facilidad de uso percibida del software SIVAC",   # rótulo PE como dimensión de la VI (v03)
    "DOS certificados",                                             # esquema doble certificado (v03)
    "Se enfatiza en cualquiera de los enunciados",                  # nota Claridad corrupta del escaneo
]

PROHIBIDOS = [r"DEC-\d", r"\bQG-?\d", r"salidas/", r"salidas\\", r"\.md\b", r"jquispe", r"@unajma", r"Cel\.",
              r"9xx", r"\bCIP\b", r"\bPMMV\b", r"\bF[5-9]\b", r"—"]
FUENTES_OK = {FUENTE}


# ------------------------------------------------------------------ utilidades


def _fuente_run(r, size, bold=False, italic=False, sub=False, sup=False):
    r.font.name = FUENTE
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    if sub:
        r.font.subscript = True
    if sup:
        r.font.superscript = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    rf = r._element.rPr.rFonts
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(a), FUENTE)


def par(doc, runs="", size=TAM_CUERPO, align="left", before=0, after=0, line=1.5,
        first=0.0, left=0.0, hanging=0.0, keep_next=False, pbb=False, bold=False, italic=False):
    """Parrafo nativo. `runs`: texto o lista de (texto, negrita, cursiva)."""
    p = doc.add_paragraph()
    p.alignment = {"left": WD_ALIGN_PARAGRAPH.LEFT, "center": WD_ALIGN_PARAGRAPH.CENTER,
                   "right": WD_ALIGN_PARAGRAPH.RIGHT, "both": WD_ALIGN_PARAGRAPH.JUSTIFY}[align]
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    if first:
        pf.first_line_indent = Cm(first)
    if left:
        pf.left_indent = Cm(left)
    if hanging:
        pf.left_indent = Cm(hanging)
        pf.first_line_indent = Cm(-hanging)
    if keep_next:
        pf.keep_with_next = True
    if isinstance(runs, str):
        runs = [(runs, bold, italic)] if runs else []
    for t, b, i in runs:
        _fuente_run(p.add_run(t), size, b, i)
    if pbb:
        quir.asegurar_salto_pagina_parrafo(p)
    return p


def par_formula(doc, partes, size=TAM_CUERPO, before=4, after=4, align="center"):
    """Parrafo narrativo para formulas con ecuacion OMML nativa mediante el
    motor quirurgico: `partes` = lista de (texto, modo) con modo en
    {"", "sub", "sup"}; el primer elemento cuyo modo sea "omml" recibe una
    cadena MathML que mathml_to_omml transforma a <m:oMath> (sin LaTeX ni
    ASCII degradado)."""
    p = doc.add_paragraph()
    p.alignment = {"center": WD_ALIGN_PARAGRAPH.CENTER, "left": WD_ALIGN_PARAGRAPH.LEFT,
                   "both": WD_ALIGN_PARAGRAPH.JUSTIFY}[align]
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = 1.5
    for t, modo in partes:
        if modo == "omml":
            p._p.append(quir.mathml_to_omml(t))
            continue
        _fuente_run(p.add_run(t), size, sub=(modo == "sub"), sup=(modo == "sup"))
    return p


def configurar_normal(doc):
    st = doc.styles["Normal"]
    st.font.name = FUENTE
    st.font.size = Pt(TAM_CUERPO)
    rPr = st.element.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = parse_xml(r"<w:rFonts %s/>" % nsdecls("w"))
        rPr.insert(0, rf)
    for a in list(rf.attrib):
        if "Theme" in a:
            del rf.attrib[a]
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(a), FUENTE)


def aplicar_geometria(sec, clave):
    g = GEOMETRIAS[clave]
    sec.orientation = g["orient"]
    sec.page_width, sec.page_height = Cm(g["w"]), Cm(g["h"])
    sec.left_margin, sec.right_margin = Cm(g["l"]), Cm(g["r"])
    sec.top_margin, sec.bottom_margin = Cm(g["t"]), Cm(g["b"])
    sec.header_distance, sec.footer_distance = Cm(1.0), Cm(0.9)


def pie_pagina(sec):
    """Numero de pagina nativo (campo PAGE) centrado en el pie de la seccion 1;
    las demas secciones lo heredan por enlace por defecto."""
    p = sec.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rPr = '<w:rPr %s><w:rFonts w:ascii="%s" w:hAnsi="%s"/><w:sz w:val="20"/></w:rPr>' % (nsdecls("w"), FUENTE, FUENTE)
    p._p.append(parse_xml('<w:r %s>%s<w:fldChar w:fldCharType="begin"/></w:r>' % (nsdecls("w"), rPr)))
    p._p.append(parse_xml('<w:r %s>%s<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>' % (nsdecls("w"), rPr)))
    p._p.append(parse_xml('<w:r %s>%s<w:fldChar w:fldCharType="end"/></w:r>' % (nsdecls("w"), rPr)))


def nueva_seccion(doc, clave):
    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    aplicar_geometria(sec, clave)
    # El parrafo que aloja el sectPr anterior se reduce a 1 pt para no generar paginas vacias.
    body = doc.element.body
    for p in body.findall(qn("w:p")):
        pPr = p.find(qn("w:pPr"))
        if pPr is not None and pPr.find(qn("w:sectPr")) is not None and pPr.find(qn("w:rPr")) is None:
            s = pPr.find(qn("w:sectPr"))
            s.addprevious(parse_xml(
                '<w:spacing %s w:before="0" w:after="0" w:line="20" w:lineRule="exact"/>' % nsdecls("w")))
            s.addprevious(parse_xml('<w:rPr %s><w:sz w:val="2"/><w:szCs w:val="2"/></w:rPr>' % nsdecls("w")))
    return sec


def _tcw(cell, dxa):
    tcPr = cell._tc.get_or_add_tcPr()
    for w in tcPr.findall(qn("w:tcW")):
        tcPr.remove(w)
    tcPr.insert(0, parse_xml('<w:tcW %s w:w="%d" w:type="dxa"/>' % (nsdecls("w"), dxa)))


def _contenido(cell, texto, size, bold=False, align="left"):
    """Escribe texto multilinea en una celda mediante el motor quirurgico."""
    if texto == "" or texto is None:
        fany.fijar_contenido_celda(cell, fany._p_vacio())
        return
    lineas = [l for l in str(texto).split("\n")]
    ps = []
    for l in lineas:
        if not l.strip():
            continue
        if l.lstrip().startswith("• "):
            ps.append(quir.crear_parrafo_item_lista(l.strip(), fuente=FUENTE, font_size_pt=size, align="left",
                                                    space_before=0, space_after=20,
                                                    left_indent_dxa=200, hanging_dxa=200))
        else:
            ps.append(quir.crear_parrafo_celda(l.strip(), bold=bold, fuente=FUENTE, font_size_pt=size,
                                               align=align, line_spacing=240, space_before=10, space_after=20))
    tc = cell._tc
    for h in list(tc):
        if h.tag != qn("w:tcPr"):
            tc.remove(h)
    for p in ps:
        tc.append(p)


def _linea_inferior_fila(t, fila):
    """Linea horizontal inferior en cada celda de la fila (linea de abarque APA 7).

    APA 7 admite lineas horizontales adicionales para separar abarques
    (encabezados internos o filas de agrupacion); prohibe toda linea vertical.
    """
    for tc in t.rows[fila]._tr.findall(qn("w:tc")):
        tcPr = tc.get_or_add_tcPr()
        tcBorders = tcPr.find(qn("w:tcBorders"))
        if tcBorders is None:
            tcBorders = parse_xml(r'<w:tcBorders %s/>' % nsdecls("w"))
            va = tcPr.find(qn("w:vAlign"))
            if va is not None:
                va.addprevious(tcBorders)
            else:
                tcPr.append(tcBorders)
        for b in tcBorders.findall(qn("w:bottom")):
            tcBorders.remove(b)
        tcBorders.append(parse_xml(
            r'<w:bottom %s w:val="single" w:sz="4" w:space="0" w:color="000000"/>' % nsdecls("w")))


def tabla(doc, encabezado, filas, anchos, total, alto_min=None,
          alinear=None, size=TAM_TABLA, margen=(40, 80, 40, 80)):
    """Tabla nativa APA 7: tres lineas horizontales y cero bordes verticales.

    Adaptacion editorial del modelo Fany 2024 (no réplica exacta): las columnas
    y los espacios de marcado ([  ]) se conservan nativos, pero toda la tabla
    obedece el bordado APA 7 del motor (aplicar_bordes_apa7).
    """
    n = len(anchos)
    assert sum(anchos) == total, (sum(anchos), total)
    t = doc.add_table(rows=1 + len(filas), cols=n)
    quir.configurar_geometria_tabla(t, total, anchos, align="center", cell_margin_dxa=margen)
    quir.aplicar_bordes_apa7(t)
    fany.fijar_disposicion_fija(t)
    alinear = alinear or ["left"] * n
    for c, h in enumerate(encabezado):
        _contenido(t.cell(0, c), h, size, bold=True, align="center")
    for r, fila in enumerate(filas, start=1):
        for c, v in enumerate(fila):
            _contenido(t.cell(r, c), v, size, align=alinear[c])
    for row in t.rows:
        for cell in row.cells:
            cell.vertical_alignment = fany.WD_ALIGN_VERTICAL.CENTER
    if alto_min:
        for row in t.rows[1:]:
            row._tr.get_or_add_trPr().append(parse_xml(
                '<w:trHeight %s w:val="%d" w:hRule="atLeast"/>' % (nsdecls("w"), alto_min)))
    quir.blindar_filas_tabla(t, cant_split=True, repetir_encabezado=True, filas_encabezado=1)
    quir.normalizar_orden_tblPr(t)
    return t


def fusionar_fila(t, fila, texto, total, size=TAM_TABLA):
    """Fusiona una fila completa; tras la fusion, APA 7 exige devolver el ancho
    de celda fusionada y el bordado de tres lineas (la celda fusionada hereda
    la estructura de la primera celda, ya sin bordes verticales)."""
    celdas = t.rows[fila].cells
    m = celdas[0].merge(celdas[-1])
    _tcw(m, total)
    _contenido(m, texto, size, bold=True, align="left")
    return m


def separador(doc):
    par(doc, "", size=6, line=1.0)


# ------------------------------------------------------------------ 1. carta

LISTA_DOCUMENTOS = [
    "Instrucciones para el juez validador.",
    "Hoja informativa de la intervención tecnológica SIVAC (descriptiva, sin evaluación).",
    "Tres certificados de validez de contenido, uno por dimensión: N.° 01 (Instrumento N.° 01, Ficha de "
    "observación y tiempos; oportunidad de procesamiento), N.° 02 (Instrumento N.° 02, Ficha de cotejo "
    "documental; consistencia documental) y N.° 03 (Instrumento N.° 03, ocho reactivos de la Modalidad A; "
    "satisfacción del usuario).",
    "Instrumento N.° 03 íntegro, matrices de consistencia y de operacionalización, y fichas completas N.° 01 "
    "y N.° 02, como sustento de la revisión (no se llenan).",
]


def pieza_carta(doc):
    par(doc, f"Andahuaylas, ........ de ........................ de {ANIO}", align="right", after=2)
    par(doc, "Propuesta para revisión: documento de trabajo entregado al juez para su observación; "
             "no constituye una versión institucional aprobada.", size=9.5, italic=True, after=4)
    par(doc, "Señor(a): ...........................................................", after=0)
    par(doc, "Docente de la Escuela Profesional de Ingeniería de Sistemas", italic=True, after=4)
    par(doc, "De mi mayor consideración:", after=4)
    par(doc, f"Yo, {TESISTA}, tesista de la Escuela Profesional de Ingeniería de Sistemas de la Universidad "
             "Nacional José María Arguedas, me dirijo a usted para solicitarle su colaboración como juez experto "
             "en la revisión y validación de contenido de los tres instrumentos de mi investigación, intitulada "
             f"“{TITULO_TESIS}”. Los tres instrumentos se someten a juicio de contenido mediante igual número de "
             "certificados u hojas de evaluación, uno por dimensión de la variable dependiente; revisarlos no "
             "equivale a contestar datos ni preguntas de percepción.", align="both", first=1.27)
    par(doc, "Presento los siguientes documentos:", after=0, keep_next=True)
    for i, d in enumerate(LISTA_DOCUMENTOS, start=1):
        par(doc, f"{i}.  {d}", hanging=1.27, left=0, after=2)
    par(doc, "Agradezco anticipadamente su atención a la presente.", before=4, first=1.27, after=4)
    par(doc, "Atentamente,", align="center", after=8)
    par(doc, "..........................................................", align="center", line=1.0)
    par(doc, TESISTA, align="center", bold=True, line=1.0)
    par(doc, "Tesista", align="center", line=1.0)


# ------------------------------------------------------------ 2. instrucciones


def pieza_instrucciones(doc):
    par(doc, TITULO_INSTRUCCIONES, bold=True, align="center", pbb=True, after=6)
    par(doc, "Las instrucciones para la revisión del expediente son las siguientes:", after=3)
    par(doc, "1.  El expediente contiene TRES formatos de juicio de contenido, uno por dimensión de la variable "
             "dependiente: N.° 01 (Instrumento N.° 01, oportunidad de procesamiento), N.° 02 (Instrumento N.° 02, "
             "consistencia documental) y N.° 03 (ocho reactivos de la Modalidad A del Instrumento N.° 03, "
             "satisfacción del usuario). Los tres instrumentos del estudio se someten a juicio de contenido. En "
             "los tres formatos, marque con una equis (X) la opción Sí o No en cada uno de "
             "los tres criterios siguientes, por cada elemento o reactivo:", align="both", hanging=1.0, after=3)
    tabla(doc, ["Criterio", "Descripción"], [
        ["Pertinencia", "El ítem corresponde al concepto teórico formulado."],
        ["Relevancia", "El ítem es apropiado para representar al componente o dimensión específica del constructo."],
        ["Claridad", "El enunciado se entiende sin dificultad; es conciso, exacto y directo."],
    ], [1900, ANCHO_RETRATO - 1900], ANCHO_RETRATO)
    separador(doc)
    resto = [
        "Anote sus observaciones en la columna Sugerencias. En los formatos N.° 01 y N.° 02 se evalúan los "
        "elementos del protocolo listados (reglas de medición, criterios y consolidación), consultando las "
        "fichas adjuntas; NO equivale a contestar los datos de campo ni las preguntas de percepción, que "
        "permanecen en blanco.",
        "Complete el bloque de cierre de cada formato: Observaciones sobre la cobertura de la dimensión, "
        "opinión de aplicabilidad (Aplicable, Aplicable después de corregir o No aplicable), sus datos, la "
        "fecha y su firma.",
        "La hoja informativa de la intervención tecnológica (condiciones X0 y X1) es solo descriptiva y no se "
        "califica; el Instrumento N.° 03 se adjunta íntegro como contexto y la Modalidad B no se califica ni se "
        "suma a la Modalidad A; las matrices y las fichas completas N.° 01 y N.° 02 son sustento de la revisión "
        "y no se llenan, pues las mediciones y la evidencia de confiabilidad corresponden al plan vigente del "
        "estudio.",
        "Devuelva los tres formatos completos, con sus observaciones, al investigador.",
    ]
    for i, s in enumerate(resto, start=2):
        par(doc, f"{i}.  {s}", align="both", hanging=1.0, after=3)


# --------------------------------------------------- 3. hoja informativa de la VI


def pieza_hoja_informativa(doc):
    par(doc, TITULO_HOJA_VI, bold=True, align="center", pbb=True, after=2)
    par(doc, "Material explicativo para el juez sobre la intervención tecnológica aplicada en el estudio.",
        italic=True, align="center", size=10, after=6)
    tabla(doc, ["Campo", "Definición operacional"], [
        ["Variable independiente", "Sistema web SIVAC."],
        ["Categoría de operacionalización", "Intervención tecnológica dicotómica."],
        ["Escala", "Nominal dicotómica."],
        ["Condición X0 (pretest)",
         "Ausencia del sistema SIVAC: la gestión de movimientos mensuales de vacunas se realiza con el procedimiento "
         "tradicional (kardex físico, libros de registro y hojas de cálculo)."],
        ["Condición X1 (postest)",
         "Presencia y uso del sistema web SIVAC en la gestión de movimientos mensuales de vacunas, con verificación "
         "documental de la puesta en producción; las fechas pre y post por sí solas no prueban el uso."],
        ["Sustento técnico", "Metodología Extreme Programming y calidad del producto software ISO/IEC 25010:2023."],
    ], [2700, ANCHO_RETRATO - 2700], ANCHO_RETRATO, alto_min=400,
        alinear=["left", "both"])
    par(doc, "Esta hoja describe la intervención; no constituye una escala psicométrica ni un certificado de "
             "validez de contenido de la variable independiente.", align="both", before=8, italic=True, size=10)
    par(doc, "Observaciones del juez (opcional):", bold=True, before=10, after=2, keep_next=True)
    fany.agregar_linea_escritura(doc, before=6, after=8)
    fany.agregar_linea_escritura(doc, before=2, after=8)
    fany.agregar_linea_escritura(doc, before=2, after=2)


# ---------------------------------------------------- 4. panorama de dimensiones


FILAS_PANORAMA = [
    ["Dimensión 1: Oportunidad de procesamiento (Treg, Tvale)",
     "Instrumento N.° 01: Ficha de observación sistemática y medición de tiempos cronometrados",
     "Certificado de validez de contenido N.° 01, hoja de evaluación N.° 01 (elementos de la ficha)"],
    ["Dimensión 2: Consistencia documental (RSD, CPE)",
     "Instrumento N.° 02: Ficha de registro y cotejo documental de consistencia",
     "Certificado de validez de contenido N.° 02, hoja de evaluación N.° 02 (elementos y criterios de la ficha)"],
    ["Dimensión 3: Satisfacción del usuario (AP, UP)",
     "Instrumento N.° 03, Modalidad A: Cuestionario de satisfacción con el proceso operativo",
     "Certificado de validez de contenido N.° 03 (ocho reactivos)"],
]


def pieza_panorama(doc):
    par(doc, TITULO_PANORAMA, bold=True, align="center", pbb=True, after=2)
    par(doc, "Cada dimensión de la variable dependiente se evalúa en su hoja correspondiente; la hoja informativa "
             "de la intervención tecnológica (variable independiente) es descriptiva y no se califica.",
        italic=True, align="center", size=10, after=6)
    tabla(doc, ["Dimensión de la variable dependiente", "Instrumento asociado", "Hoja de evaluación"],
          FILAS_PANORAMA, [3100, 3400, ANCHO_RETRATO - 6500], ANCHO_RETRATO,
          alinear=["both", "both", "both"], alto_min=500)
    par(doc, "Las tres hojas comparten los criterios de Pertinencia, Relevancia y Claridad, y cada una lleva su "
             "propio bloque de cierre. Ninguna hoja registra datos de campo ni respuestas de percepción.",
        align="both", before=6, size=10, italic=True)


# --------------------------------------- 5. hojas de evaluacion N.° 01 y N.° 02

ANCHOS_HOJA = [800, 7420, 620, 620, 620, 620, 620, 620, 2060]  # suma 14000 (apaisada)


def construir_tabla_hoja(doc, grupos):
    """Tabla de evaluacion de contenido en apaisada (14000 dxa): 2 filas de
    encabezado (criterios con subcolumnas Si/No), filas de elementos con celdas
    vacias y columna de sugerencias, con filas de grupo por indicador fusionadas
    a lo ancho. Bordado APA 7 del motor (adaptacion editorial del modelo Fany
    2024, no replica). Los textos visibles son extractos descriptivos fieles y
    breves (sin formulas algebraicas, codigos internos ni versiones de stack);
    la evaluacion se realiza consultando la ficha integra adjunta."""
    anchos = ANCHOS_HOJA
    n_elem = sum(len(filas) for _, filas in grupos)
    n_filas = 2 + len(grupos) + n_elem
    t = doc.add_table(rows=n_filas, cols=9)
    quir.configurar_geometria_tabla(t, ANCHO_APAISADA, anchos, align="center",
                                    cell_margin_dxa=(20, 50, 20, 50))
    quir.aplicar_bordes_apa7(t)
    fany.fijar_disposicion_fija(t)
    # Fusiones del encabezado de dos filas: N.°, Elementos y Sugerencias
    # verticales; criterios en pares horizontales Si/No.
    for c in (0, 1, 8):
        celda = t.cell(0, c).merge(t.cell(1, c))
        celda.width = Cm(anchos[c] / 567.0)
    for c in (2, 4, 6):
        celda = t.cell(0, c).merge(t.cell(0, c + 1))
        celda.width = Cm((anchos[c] + anchos[c + 1]) / 567.0)
    fany.texto_celda(t.cell(0, 0), "N.°", tamano=fany.TAM_ENCABEZADO, negrita=True)
    fany.texto_celda(t.cell(0, 1), "ELEMENTOS DE LA FICHA / PROTOCOLO", tamano=fany.TAM_ENCABEZADO, negrita=True)
    fany.texto_celda_con_superindice(t.cell(0, 2), "Pertinencia", "1", tamano=fany.TAM_ENCABEZADO)
    fany.texto_celda_con_superindice(t.cell(0, 4), "Relevancia", "2", tamano=fany.TAM_ENCABEZADO)
    fany.texto_celda_con_superindice(t.cell(0, 6), "Claridad", "3", tamano=fany.TAM_ENCABEZADO)
    fany.texto_celda(t.cell(0, 8), "Sugerencias", tamano=fany.TAM_ENCABEZADO, negrita=True)
    for c, etiqueta in ETIQUETAS_CERT.items():
        fany.texto_celda(t.cell(1, c), etiqueta, tamano=fany.TAM_ENCABEZADO, negrita=True)
    # Filas de grupo (por indicador) y filas de elementos, numeracion continua.
    fila = 2
    n = 0
    filas_grupo = []
    for etiqueta_grupo, elementos in grupos:
        celda_g = t.cell(fila, 0).merge(t.cell(fila, 8))
        celda_g.width = Cm(ANCHO_APAISADA / 567.0)
        fany.texto_celda(celda_g, etiqueta_grupo, tamano=fany.TAM_DIMENSION, negrita=True,
                         alineacion="left", before=15, after=15, margen_izq_dxa=50)
        filas_grupo.append(fila)
        fila += 1
        for num, texto in elementos:
            fany.texto_celda(t.cell(fila, 0), f"{num:02d}", tamano=9.0, alineacion="center")
            fany.texto_celda(t.cell(fila, 1), texto, tamano=fany.TAM_ITEM, alineacion="both",
                             before=10, after=10, margen_izq_dxa=50)
            for c in fany.COLS_CRITERIO:
                fany.fijar_contenido_celda(t.cell(fila, c), fany._p_vacio())
            fany.fijar_contenido_celda(t.cell(fila, 8), fany._p_vacio())
            fila += 1
            n += 1
    fany.normalizar_celdas_sin_parrafo(t)
    # Lineas de abarque APA 7: bajo la fila de etiquetas Si/No del encabezado
    # y bajo cada fila de grupo por indicador.
    _linea_inferior_fila(t, 1)
    for fg in filas_grupo:
        _linea_inferior_fila(t, fg)
    for row in t.rows:
        for cell in row.cells:
            cell.vertical_alignment = fany.WD_ALIGN_VERTICAL.CENTER
    quir.blindar_filas_tabla(t, cant_split=True, repetir_encabezado=True, filas_encabezado=2)
    quir.normalizar_orden_tblPr(t)
    return t


# Grupos de las hojas N.° 01 y N.° 02: textos tomados LITERALMENTE del campo
# texto_evaluado del JSON sanitizado y trazable del especialista-instrumentos
# (salidas/documentos/anexos_fany/textos_tabla_fichas_v05.json, guardado
# tambien como especificacion durable junto a especificacion_fichas_v05.json
# con las fuentes internas de cada fila): 12 filas para la ficha 01 (4
# comunes + 4 Treg + 4 Tvale) y 20 filas para la ficha 02 (4 comunes + 12
# RSD, con los 8 criterios de conformidad en filas separadas + matriz +
# consolidado, y 4 CPE). Numeracion continua 1..12 y 1..20. Los textos son
# descriptivos, fieles a la fuente y sin ecuaciones, simbolos algebraicos,
# codigos internos, rutas ni versiones de tecnologia; el campo fuente del
# JSON es solo para auditoria interna y no se imprime. La evaluacion se
# realiza consultando la ficha integra adjunta.
GRUPOS_HOJA_01 = [
    ("Identificación y aplicación (elemento común de la ficha)", [
        (1, "Bloque de identificación del operador evaluado: código de trabajador del rango TRAB-01 a TRAB-14, "
            "rol institucional entre responsable de centro de acopio o red de frío y personal de estrategia "
            "sanitaria de inmunizaciones, centro de acopio o sede, red o microred de salud y provincia "
            "sanitaria entre Andahuaylas y Chincheros."),
        (2, "Campo de marcado entre dos condiciones del proceso evaluado: en el pretest el registro se apoya en "
            "kardex físico manual, libros y hojas de cálculo dispersas; en el postest se emplea el sistema web "
            "SIVAC con base de datos relacional. Permite comparar los tiempos del proceso manual frente al "
            "proceso informatizado."),
        (3, "Cronómetro digital calibrado con precisión de centésimas de segundo. La unidad oficial de medida "
            "son los minutos decimales con cuatro cifras significativas: los minutos enteros se suman a la "
            "porción decimal obtenida al dividir los segundos entre sesenta. Todos los tiempos de la ficha se "
            "consignan bajo esta unidad común."),
        (4, "Ante una interrupción imprevista no atribuible al flujo operativo evaluado, como corte de energía, "
            "sismo, llamada de emergencia sanitaria o atención médica no programada, el cronómetro se detiene y "
            "se reanuda al normalizarse la tarea, registrando estrictamente el tiempo neto efectivo de trabajo "
            "del operador."),
    ]),
    ("Indicador: Tiempo de registro de movimiento de vacunas (Treg)", [
        (5, "Lapso requerido por el operador para ingresar, validar y asentar un movimiento de vacunas en el "
            "sistema o registro formal. El tiempo se determina desde que se toma el documento fuente o se abre "
            "la interfaz de digitación hasta que el movimiento queda grabado, confirmado en la base de datos o "
            "asentado con saldo actualizado en el libro oficial."),
        (6, "Inicio: momento exacto en que el operador toma físicamente el documento fuente, guía, pecosa o "
            "remesa, o abre la interfaz para iniciar la digitación de los campos del movimiento. Fin: momento "
            "en que el movimiento queda grabado, confirmado en la base de datos o asentado con saldo "
            "actualizado en el libro oficial."),
        (7, "Tres tareas estandarizadas por operador: registro de remesa nacional de un biológico con lote "
            "único, verificación de vencimiento y dosis totales; despacho programado de dos a tres tipos de "
            "vacunas hacia un centro de salud; y transferencia o ajuste de cuatro a seis ítems, incluidos "
            "jeringas y diluyentes, con verificación de saldos."),
        (8, "Por cada tarea se registran la descripción del movimiento estandarizado, los biológicos y lotes "
            "auditados, el número total de dosis, la hora de inicio y de fin con centésimas, el tiempo neto en "
            "minutos y segundos, el tiempo en minutos decimales y las incidencias; cierra con el promedio de "
            "las tres tareas y la mediana intrasujeto del operador."),
    ]),
    ("Indicador: Tiempo de emisión de comprobante de salida o vale (Tvale)", [
        (9, "Tiempo requerido para procesar el requerimiento de biológicos de una microred, verificar los lotes "
            "disponibles, generar el comprobante oficial de despacho y formalizar la orden imprimible o en "
            "documento electrónico. Se determina desde la apertura o recepción de la solicitud de pedido hasta "
            "que el comprobante queda emitido y formalizado."),
        (10, "Inicio: momento en que el operador recibe o apertura la solicitud de pedido de biológicos para su "
             "despacho a un establecimiento de salud. Fin: momento en que el comprobante de salida o vale "
             "oficial queda generado, visualizado, firmado digitalmente o impreso en documento electrónico con "
             "numeración correlativa."),
        (11, "Tres emisiones estandarizadas por operador: vale simple para puesto de salud de nivel uno o dos "
             "con uno a dos ítems de vacunas; vale regular para centro de salud de nivel tres o cuatro con tres "
             "a cinco ítems e insumos; y vale de emergencia por contingencia de cadena de frío o barrido "
             "vacunal con verificación de lotes y firmas."),
        (12, "Por cada emisión se registran el tipo de vale estandarizado, el número de documento o vale, la "
             "cantidad de ítems, la hora de inicio y de fin con centésimas, el tiempo neto en minutos y "
             "segundos, el tiempo en minutos decimales y las incidencias; cierra con el promedio de las tres "
             "emisiones y la mediana intrasujeto del operador."),
    ]),
]

GRUPOS_HOJA_02 = [
    ("Identificación y aplicación (elemento común de la ficha)", [
        (1, "Bloque de identificación del centro auditado: código de trabajador del rango TRAB-01 a TRAB-14, "
            "centro de acopio provincial o microred, provincia sanitaria entre Andahuaylas y Chincheros, "
            "ventana temporal de auditoría, fecha de ejecución y designación del auditor principal y del "
            "auditor secundario cuando corresponda."),
        (2, "Campo de marcado entre dos condiciones: en el pretest la auditoría contrasta kardex manual físico, "
            "cuadernos de registro y hojas de cálculo; en el postest contrasta la base de datos relacional del "
            "sistema SIVAC y los vales electrónicos generados en formato de documento portable. Sostiene la "
            "comparación de consistencia entre ambos momentos."),
        (3, "La auditoría documental se ejecuta sobre una ventana simétrica estandarizada de treinta días "
            "calendario consecutivos en el pretest y de exactamente treinta días calendario consecutivos en el "
            "postest, contados tras la puesta en producción y la estabilización operativa del sistema, de modo "
            "que ambos periodos resulten comparables."),
        (4, "Se audita un corpus de cuarenta a sesenta documentos o transacciones por ventana temporal, "
            "distribuidos proporcionalmente entre los centros de acopio. En el pretest la evidencia proviene "
            "de cuadernos de control, tarjetas de kardex físico, archivos locales y comprobantes manuales; en "
            "el postest, del registro de transacciones del sistema, reportes de kardex electrónico y "
            "comprobantes generados automáticamente con firma y código de verificación."),
    ]),
    ("Indicador: Porcentaje de registros sin discrepancias (RSD)", [
        (5, "Porcentaje de registros de movimientos de vacunas auditados durante la ventana temporal que "
            "satisfacen con rigor absoluto los ocho criterios obligatorios de integridad y concordancia. Se "
            "obtiene al dividir el número de registros conformes sin discrepancia entre el total de registros "
            "auditados y multiplicar por cien."),
        (6, "Un registro es conforme únicamente cuando cumple simultáneamente y sin excepción los ocho "
            "criterios de calidad frente a la evidencia física y el documento ministerial de respaldo. Basta "
            "una omisión, borrón, enmienda ilegible, error tipográfico, desfase de cálculo o contradicción en "
            "cualquiera de ellos para calificarlo como no conforme, es decir, con discrepancia detectada."),
        (7, "El tipo de movimiento debe estar clasificado de manera unívoca como entrada por remesa, salida a "
            "establecimiento de salud o ajuste. La tipificación debe quedar sin ambigüedad en el registro "
            "auditado, pues una clasificación dudosa o múltiple impide verificar la naturaleza del movimiento y "
            "torna el registro no conforme."),
        (8, "El biológico debe consignarse con su denominación oficial estandarizada según el Esquema Regular "
            "Nacional del Ministerio de Salud. El nombre registrado debe coincidir con la nomenclatura "
            "normativa vigente, evitando abreviaturas informales, de manera que la identidad del insumo "
            "resulte verificable contra el esquema nacional de inmunizaciones."),
        (9, "El número de lote debe identificarse con exactitud y coincidir con el rotulado del frasco. La "
            "correspondencia entre el lote escrito en el documento y el impreso en el envase físico garantiza "
            "la trazabilidad de la partida; cualquier divergencia entre ambos constituye discrepancia y torna "
            "el registro no conforme."),
        (10, "La cantidad de dosis o viales debe ser exacta y coincidente con el stock físico y el acta de "
             "recepción. El dato numérico del registro se coteja contra la existencia real y el documento de "
             "entrega, de forma que todo desfase de cantidad se califique como discrepancia del registro "
             "auditado."),
        (11, "La fecha del movimiento debe consignarse con formato completo de día, mes y año y mantener "
             "secuencia cronológica. La fecha íntegra permite ordenar los asientos y reconstruir el flujo de "
             "existencias; una fecha incompleta, fuera de secuencia o contradictoria con documentos vecinos "
             "torna el registro no conforme."),
        (12, "El establecimiento de origen o destino debe estar plenamente individualizado con su código oficial "
             "del registro nacional de establecimientos de salud. La identificación inequívoca del nodo emisor "
             "o receptor posibilita rastrear el movimiento dentro de la red; su omisión o imprecisión "
             "configura una discrepancia del registro."),
        (13, "El nombre completo, la firma o el usuario responsable del despacho o de la recepción debe quedar "
             "plenamente trazable. Cada movimiento exige un responsable identificable sin ambigüedad, de modo "
             "que la auditoría pueda atribuir la operación a una persona verificable; la ausencia de "
             "responsable torna el registro no conforme."),
        (14, "El registro debe contar con un documento formal de respaldo asociado y verificado, ya sea vale "
             "oficial, comprobante de pedido o guía de remisión. El soporte documental autentica la operación "
             "auditada; si el respaldo falta o no puede verificarse contra él, el registro se califica como no "
             "conforme."),
        (15, "Por cada biológico o insumo auditado, desde la vacuna BCG hasta las cajas térmicas, la matriz "
             "registra la vacuna o insumo, el lote, la cantidad, el veredicto final de conforme o no conforme "
             "y el tipo de discrepancia o causa raíz. La ventana contempla entre cuarenta y sesenta registros "
             "auditados."),
        (16, "Cierre del indicador con cuatro campos: número total de registros evaluados en la ventana, número "
             "de registros conformes sin discrepancia, número de registros con discrepancia o fallas y el "
             "porcentaje de registros sin discrepancias, obtenido al dividir los conformes entre el total "
             "evaluado y multiplicar por cien."),
    ]),
    ("Indicador: Concordancia de cantidad programada frente a entregada (CPE)", [
        (17, "Proporción de despachos y entregas de vacunas evaluadas en las que la cantidad entregada coincide "
             "con la programada, dosis a dosis, o cuenta con justificación documental formal del Ministerio de "
             "Salud debidamente acreditada. Se obtiene al dividir el número de entregas concordantes entre el "
             "total de entregas evaluadas y multiplicar por cien."),
        (18, "Una entrega es concordante si la cantidad despachada e inscrita en el vale oficial es idéntica a "
             "la solicitada en la programación del establecimiento receptor, o si la diferencia cuenta con "
             "documento sustentatorio oficial archivado, como acta de ajuste, memorando de contingencia de "
             "cadena de frío o directiva de racionalización biológica que autorice expresamente la variación; "
             "en caso contrario es no concordante."),
        (19, "Por cada despacho auditado se registran la vacuna o biológico, el número de documento o vale, la "
             "cantidad solicitada o programada, la cantidad entregada conforme, la diferencia absoluta entre "
             "ambas, la justificación formal del Ministerio de Salud acreditada, el veredicto de entrega "
             "concordante o no concordante y la causa raíz del desfase; la ventana contempla entre cuarenta y "
             "sesenta entregas."),
        (20, "Cierre del indicador con cuatro campos: total de entregas o despachos auditados en la ventana, "
             "número de entregas concordantes, exactas o justificadas, número de entregas no concordantes por "
             "desfases injustificados y el porcentaje de concordancia entre programación y entrega, obtenido al "
             "dividir las concordantes entre el total auditado y multiplicar por cien."),
    ]),
]


def pieza_hoja_01(doc):
    fany.TAM_ITEM, fany.TAM_CODIGO, fany.TAM_ENCABEZADO = 10.0, 9.0, 9.5
    fany.TAM_DIMENSION, fany.TAM_BLOQUE = 10.0, 10.0
    nueva_seccion(doc, "apaisada")
    par(doc, TITULO_HOJA_01, bold=True, align="center", size=10.5, line=1.2, after=2, pbb=True)
    par(doc, SUBTITULO_HOJA_01, align="center", size=10, after=5)
    par(doc, "Alcance: el juez evalúa los componentes reales del instrumento y de su protocolo (reglas de "
             "medición, puntos de inicio y fin, batería de tareas y consolidación), consultando la ficha íntegra "
             "adjunta al final del expediente. Esta hoja NO se llena con tiempos ni con datos de campo, y NO "
             "valida el desempeño del sistema SIVAC; los espacios de registro de la ficha permanecen en blanco.",
        align="both", size=10, after=5)
    construir_tabla_hoja(doc, GRUPOS_HOJA_01)
    par(doc, "Observaciones (precisar si los elementos cubren de manera completa la dimensión oportunidad de "
             "procesamiento):", align="both", size=10, italic=True, before=6, after=2, keep_next=True)
    construir_bloque_cierre(doc)
    construir_notas_pie(doc)


def pieza_hoja_02(doc):
    fany.TAM_ITEM, fany.TAM_CODIGO, fany.TAM_ENCABEZADO = 10.0, 9.0, 9.5
    fany.TAM_DIMENSION, fany.TAM_BLOQUE = 10.0, 10.0
    nueva_seccion(doc, "apaisada")
    par(doc, TITULO_HOJA_02, bold=True, align="center", size=10.5, line=1.2, after=2, pbb=True)
    par(doc, SUBTITULO_HOJA_02, align="center", size=10, after=5)
    par(doc, "Alcance: el juez evalúa los componentes reales del instrumento y de su protocolo (regla de "
             "conformidad, criterios de integridad documental, corpus de auditoría y consolidación), consultando "
             "la ficha íntegra adjunta al final del expediente. Esta hoja NO se llena con porcentajes ni con "
             "datos de auditoría, y NO valida el desempeño del sistema SIVAC; los espacios de registro de la "
             "ficha permanecen en blanco.", align="both", size=10, after=5)
    construir_tabla_hoja(doc, GRUPOS_HOJA_02)
    par(doc, "Observaciones (precisar si los elementos cubren de manera completa la dimensión consistencia "
             "documental):", align="both", size=10, italic=True, before=6, after=2, keep_next=True)
    construir_bloque_cierre(doc)
    construir_notas_pie(doc)


# ------------------------------------------------- 6. certificado Instrumento 03

ANCHOS_CERT = [800, 3550, 550, 550, 550, 550, 550, 550, 1138]  # suma 8788 (retrato)

# Etiquetas de los criterios con ortografia acentuada (Sí). Las columnas
# (Pertinencia, Relevancia, Claridad) y los codigos de reactivo se conservan.
ETIQUETAS_CERT = {2: "Sí", 3: "No", 4: "Sí", 5: "No", 6: "Sí", 7: "No"}


def construir_tabla_cert03(doc):
    """Tabla de 9 columnas a 8788 dxa, bordado APA 7 (tres lineas horizontales,
    cero verticales; adaptacion del modelo Fany 2024, no replica): 2 filas de
    encabezado, 2 filas de indicador (AP, UP) y 8 filas de reactivos con codigo
    y celdas vacias."""
    anchos = ANCHOS_CERT
    n_filas = 2 + 2 + 8
    t = doc.add_table(rows=n_filas, cols=fany.COLUMNAS_ESPERADAS)
    quir.configurar_geometria_tabla(t, ANCHO_RETRATO, anchos, align="center",
                                    cell_margin_dxa=(20, 50, 20, 50))
    quir.aplicar_bordes_apa7(t)
    fany.fijar_disposicion_fija(t)
    # Fusiones del encabezado de dos filas.
    for c in (fany.COL_N, fany.COL_ITEM, fany.COL_SUGERENCIAS):
        celda = t.cell(0, c).merge(t.cell(1, c))
        celda.width = Cm(anchos[c] / 567.0)
    for c in (2, 4, 6):
        celda = t.cell(0, c).merge(t.cell(0, c + 1))
        celda.width = Cm((anchos[c] + anchos[c + 1]) / 567.0)
    fany.texto_celda(t.cell(0, fany.COL_N), "N.°", tamano=fany.TAM_ENCABEZADO, negrita=True)
    fany.texto_celda(t.cell(0, fany.COL_ITEM), "REACTIVOS (MODALIDAD A)", tamano=fany.TAM_ENCABEZADO, negrita=True)
    fany.texto_celda_con_superindice(t.cell(0, 2), "Pertinencia", "1", tamano=fany.TAM_ENCABEZADO)
    fany.texto_celda_con_superindice(t.cell(0, 4), "Relevancia", "2", tamano=fany.TAM_ENCABEZADO)
    fany.texto_celda_con_superindice(t.cell(0, 6), "Claridad", "3", tamano=fany.TAM_ENCABEZADO)
    fany.texto_celda(t.cell(0, fany.COL_SUGERENCIAS), "Sugerencias", tamano=fany.TAM_ENCABEZADO, negrita=True)
    for c, etiqueta in ETIQUETAS_CERT.items():
        fany.texto_celda(t.cell(1, c), etiqueta, tamano=fany.TAM_ENCABEZADO, negrita=True)
    # Filas de indicador (agrupacion, NO nuevas dimensiones) y reactivos.
    grupos = [(GRUPO_AP, [("AP-01", ITEMS_AP[0]), ("AP-02", ITEMS_AP[1]),
                          ("AP-03", ITEMS_AP[2]), ("AP-04", ITEMS_AP[3])]),
              (GRUPO_UP, [("UP-01", ITEMS_UP[0]), ("UP-02", ITEMS_UP[1]),
                          ("UP-03", ITEMS_UP[2]), ("UP-04", ITEMS_UP[3])])]
    fila = 2
    for etiqueta_grupo, items in grupos:
        celda_g = t.cell(fila, fany.COL_N).merge(t.cell(fila, fany.COL_ITEM))
        celda_g.width = Cm((anchos[fany.COL_N] + anchos[fany.COL_ITEM]) / 567.0)
        fany.texto_celda(celda_g, etiqueta_grupo, tamano=fany.TAM_DIMENSION, negrita=True,
                         alineacion="left", before=15, after=15, margen_izq_dxa=50)
        for c, etiqueta in ETIQUETAS_CERT.items():
            fany.texto_celda(t.cell(fila, c), etiqueta, tamano=fany.TAM_ENCABEZADO, negrita=True)
        fany.fijar_contenido_celda(t.cell(fila, fany.COL_SUGERENCIAS), fany._p_vacio())
        fila += 1
        for codigo, enunciado in items:
            fany.texto_celda(t.cell(fila, fany.COL_N), codigo, tamano=9.0, alineacion="center")
            fany.texto_celda(t.cell(fila, fany.COL_ITEM), enunciado, tamano=fany.TAM_ITEM,
                             alineacion="both", before=10, after=10, margen_izq_dxa=50)
            for c in fany.COLS_CRITERIO:
                fany.fijar_contenido_celda(t.cell(fila, c), fany._p_vacio())
            fany.fijar_contenido_celda(t.cell(fila, fany.COL_SUGERENCIAS), fany._p_vacio())
            fila += 1
    fany.normalizar_celdas_sin_parrafo(t)
    # Lineas horizontales de abarque APA 7: bajo la fila de etiquetas Si/No del
    # encabezado (fila 1) y bajo cada fila de indicador (AP, UP).
    _linea_inferior_fila(t, 1)
    _linea_inferior_fila(t, 2)
    _linea_inferior_fila(t, 7)
    for row in t.rows:
        for cell in row.cells:
            cell.vertical_alignment = fany.WD_ALIGN_VERTICAL.CENTER
    quir.blindar_filas_tabla(t, cant_split=True, repetir_encabezado=True, filas_encabezado=2)
    quir.normalizar_orden_tblPr(t)
    return t


def construir_bloque_cierre(doc):
    """Bloque inferior de cada hoja de evaluacion: observaciones, opinion de
    aplicabilidad, identidad del juez, fecha, firma. Campos en blanco."""
    T = fany.TAM_BLOQUE
    ps = []
    ps.append(fany.agregar_parrafo(doc, "Observaciones (precisar si hay suficiencia):",
                                   tamano=T, negrita=True, before=4, after=1))
    fany.agregar_linea_escritura(doc, before=6, after=5)
    ps.append(doc.paragraphs[-1])
    fany.agregar_linea_escritura(doc, before=2, after=5)
    ps.append(doc.paragraphs[-1])
    ps.append(fany.agregar_parrafo(
        doc,
        "Opinión de aplicabilidad:      Aplicable [   ]      "
        "Aplicable después de corregir [   ]      No aplicable [   ]",
        tamano=T, before=3, after=3))
    ps.append(fany.agregar_parrafo(
        doc,
        "Apellidos y nombres del juez validador: "
        "......................................................................................",
        tamano=T, before=2, after=2))
    ps.append(fany.agregar_parrafo(
        doc,
        "DNI: ...................................................",
        tamano=T, before=2, after=2))
    ps.append(fany.agregar_parrafo(
        doc,
        "Especialidad del validador: "
        "......................................................................................",
        tamano=T, before=2, after=2))
    ps.append(fany.agregar_parrafo(
        doc,
        "Andahuaylas, ......... de ........................................ del " + ANIO,
        tamano=T, before=4, after=5))
    ps.append(fany.agregar_parrafo(doc, "______________________________", tamano=T,
                                   alineacion=WD_ALIGN_PARAGRAPH.CENTER, before=8, after=0))
    ps.append(fany.agregar_parrafo(doc, "Firma del juez validador", tamano=T,
                                   alineacion=WD_ALIGN_PARAGRAPH.CENTER, before=1, after=0))
    for p in ps:
        p.paragraph_format.keep_with_next = True
    return ps


def construir_notas_pie(doc, tamano=9.0):
    """Notas al pie comunes de las hojas: tres criterios con Claridad CORRECTA
    y nota de suficiencia. El perfil compacto v06 las usa a 9.5 pt (canon);
    el integral v05 conserva 9.0 pt por defecto."""
    fany.agregar_parrafo(doc, "", tamano=4, before=0, after=1)
    S = tamano
    fany.agregar_parrafo_con_superindice(doc, 1, NOTA_1, tamano=S)
    fany.agregar_parrafo_con_superindice(doc, 2, NOTA_2, tamano=S)
    fany.agregar_parrafo_con_superindice(doc, 3, NOTA_3, tamano=S)
    fany.agregar_parrafo_con_superindice(doc, "Nota:", " " + NOTA_SUF, tamano=S, before=1, after=0)


def pieza_certificado03(doc):
    """Certificado de la Dimension 3: inicio en pagina nueva (retrato), tabla
    de reactivos AP/UP, aclaracion de alcance, bloque de cierre propio y notas
    al pie."""
    fany.TAM_ITEM, fany.TAM_CODIGO, fany.TAM_ENCABEZADO = 10.0, 9.0, 9.5
    fany.TAM_DIMENSION, fany.TAM_BLOQUE = 10.0, 10.0
    nueva_seccion(doc, "unajma")
    par(doc, TITULO_CERT_03, bold=True, align="center", size=10.5, line=1.2, after=2)
    par(doc, SUBTITULO_CERT_03, align="center", size=10, after=5)
    construir_tabla_cert03(doc)
    par(doc, ACLARACION_CERT, align="both", size=10, italic=True, before=6, after=2, keep_next=True)
    construir_bloque_cierre(doc)
    construir_notas_pie(doc)


# ------------------------------------------------- 7. cuestionario N.° 03 integro

ESCALA_LIKERT = [
    ["1", "Totalmente en Desacuerdo (TD)", "Rechazo total; la condición no se cumple en absoluto, generando severas trabas operativas."],
    ["2", "En Desacuerdo (D)", "Disconformidad; la condición se cumple de forma deficiente o insuficiente en el flujo diario."],
    ["3", "Neutral / Ni de Acuerdo ni en Desacuerdo (N)", "Posición intermedia; no percibe beneficio claro ni perjuicio apreciable."],
    ["4", "De Acuerdo (A)", "Conformidad; la condición se cumple satisfactoriamente facilitando las labores del área."],
    ["5", "Totalmente de Acuerdo (TA)", "Plena satisfacción; la condición se cumple de manera sobresaliente y altamente eficiente."],
]

BAREMO = [
    ["NIVEL BAJO (Insatisfacción / Rechazo)", "8 a 18 puntos", "4 a 9 puntos",
     "Percepción de sobrecarga administrativa severa, insatisfacción profunda con los métodos de registro, "
     "lentitud, estrés laboral y alta susceptibilidad a errores en los inventarios."],
    ["NIVEL MEDIO (Satisfacción Moderada)", "19 a 29 puntos", "10 a 14 puntos",
     "Percepción de funcionalidad aceptable pero perfectible; satisfacción moderada con áreas de fricción "
     "operativa, demoras puntuales o necesidad de mayor afianzamiento técnico."],
    ["NIVEL ALTO (Plena Satisfacción)", "30 a 40 puntos", "15 a 20 puntos",
     "Elevada complacencia y confort laboral; el sistema o el proceso es valorado como una herramienta "
     "altamente ágil, confiable, transparente y de valor estratégico para la salud pública."],
]


def _filas_likert(codigos, items, encabezado_grupo):
    """Filas de una tabla Likert con fila de agrupacion fusionada."""
    filas = [[encabezado_grupo, ""] * 1 + [""] * 5]
    filas[0] = [encabezado_grupo, "", "", "", "", "", ""]
    for c, i in zip(codigos, items):
        filas.append([c, i, "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"])
    return filas


def _tabla_likert(doc, codigos, items, encabezado_grupo):
    anchos = [900, 5088, 560, 560, 560, 560, 560]  # suma 8788
    filas = _filas_likert(codigos, items, encabezado_grupo)
    t = tabla(doc, ["N.°", "Reactivo", "1 (TD)", "2 (D)", "3 (N)", "4 (A)", "5 (TA)"],
              filas, anchos, ANCHO_RETRATO, alto_min=340,
              alinear=["center", "both", "center", "center", "center", "center", "center"])
    # Fusionar la fila de agrupacion a lo ancho y abarcarla con linea horizontal.
    fusionar_fila(t, 1, encabezado_grupo, ANCHO_RETRATO, size=TAM_TABLA)
    _linea_inferior_fila(t, 1)
    return t


def pieza_cuestionario03(doc):
    nueva_seccion(doc, "unajma")
    par(doc, "INSTRUMENTO N.° 03", bold=True, align="center", after=0, pbb=True)
    par(doc, "CUESTIONARIO DE SATISFACCIÓN DEL USUARIO Y ACEPTACIÓN TECNOLÓGICA (MODELO TAM)",
        bold=True, align="center", after=2)
    par(doc, "Variable evaluada: gestión de movimientos mensuales de vacunas (variable dependiente). Dimensión oficial: "
             "satisfacción del usuario. Técnica: encuesta estructurada autoadministrada. Población objetivo: "
             "personal responsable de la cadena de frío e inmunizaciones de la DISA Apurímac II (N = n = 14).",
        align="both", size=10, after=6)
    # 1. Directrices
    par(doc, "1. Directrices éticas e instrucciones para el participante", bold=True, before=6, after=3,
        keep_next=True)
    par(doc, "El presente instrumento forma parte del proyecto de investigación para optar el Título Profesional "
             "de Ingeniero de Sistemas en la UNAJMA. Su objetivo es evaluar de manera rigurosa la percepción, "
             "fluidez operativa y satisfacción respecto a la gestión y control de movimientos mensuales de vacunas en la "
             "red de frío institucional.", align="both", after=3)
    par(doc, "•  Confidencialidad y anonimato: las respuestas se procesan con reserva y codificación numérica "
             "anonimizada (TRAB-01 a TRAB-14), conforme a la Ley N.° 29733 (Protección de Datos Personales) y "
             "el Código de Ética en Investigación de la UNAJMA.", align="both", hanging=0.8, after=2)
    par(doc, "•  Libertad de respuesta: no existen respuestas correctas o incorrectas; se solicita plasmar con "
             "sinceridad la experiencia real de trabajo.", align="both", hanging=0.8, after=2)
    par(doc, "•  Escala de respuesta: marque con una equis (X) la alternativa que mejor represente su grado de "
             "conformidad con cada proposición:", align="both", hanging=0.8, after=3)
    tabla(doc, ["Puntuación", "Escala verbal", "Significado operativo en la gestión de vacunas"],
          ESCALA_LIKERT, [1300, 2900, ANCHO_RETRATO - 4200], ANCHO_RETRATO,
          alinear=["center", "left", "both"])
    # 2. Datos generales
    par(doc, "2. Datos generales del participante", bold=True, before=10, after=3, keep_next=True, pbb=True)
    tabla(doc, ["Campo", "Registro"], [
        ["Código de participante asignado", "TRAB-____  (TRAB-01 a TRAB-14)"],
        ["Centro de acopio / red / microred", ""],
        ["Provincia de desempeño", "[  ] Andahuaylas   [  ] Chincheros"],
        ["Condición laboral actual", "[  ] Nombrado D.L. 276   [  ] Contratado CAS (D.L. 1057)   [  ] Locación / otro"],
        ["Profesión / cargo operativo", "[  ] Lic. en Enfermería   [  ] Técnico(a) en Enfermería   [  ] Estadístico / soporte"],
        ["Tiempo de experiencia en red de frío", "[  ] Menos de 2 años   [  ] 2 a 5 años   [  ] 6 a 10 años   [  ] Más de 10 años"],
        ["Fecha de aplicación", "______ / ______ / 2025"],
    ], [3800, ANCHO_RETRATO - 3800], ANCHO_RETRATO, alto_min=360)
    # 3. Modalidad A
    par(doc, "3. Modalidad A (oficial para HE3): cuestionario de satisfacción con el proceso operativo",
        bold=True, before=10, after=3, pbb=True, keep_next=True)
    par(doc, "Esta modalidad constituye el instrumento oficial de contrastación inferencial pretest y postest "
             "para la Hipótesis Específica 3. En el pretest (O1) el operador evalúa su satisfacción con el "
             "proceso operativo tradicional (kardex manual físico, cuadernos y archivos Excel locales); en el "
             "postest (O2) evalúa su satisfacción con el proceso operativo mediado mediante el sistema web "
             "SIVAC. Esta simetría estructural permite calcular diferencias pareadas y contrastar la hipótesis "
             "con la prueba de Wilcoxon en n = 14 pares.", align="both", after=3)
    _tabla_likert(doc, ["AP-01", "AP-02", "AP-03", "AP-04"], ITEMS_AP,
                  "Indicador: Aceptación del proceso operativo (AP)")
    par(doc, "", size=4, after=2)
    _tabla_likert(doc, ["UP-01", "UP-02", "UP-03", "UP-04"], ITEMS_UP,
                  "Indicador: Utilidad percibida para la gestión sanitaria (UP)")
    # 4. Modalidad B
    par(doc, "4. Modalidad B (módulo anexo): aceptación tecnológica de SIVAC (modelo TAM clásico)",
        bold=True, before=10, after=3, pbb=True, keep_next=True)
    par(doc, "Módulo complementario de documentación de la calidad del software; se aplica exclusivamente en el "
             "postest, una vez que el personal ha sido capacitado y ha operado el sistema SIVAC en producción. "
             "Documenta los constructos originales de Davis (1989): utilidad percibida del software (PU) y "
             "facilidad de uso percibida (PEOU). Estos reactivos corresponden a la percepción del usuario sobre "
             "el software; no constituyen dimensiones de la variable independiente y no se suman a la "
             "Modalidad A.", align="both", after=3)
    _tabla_likert(doc, ["PU-01", "PU-02", "PU-03", "PU-04"], ITEMS_PU,
                  "Dimensión TAM 1: Utilidad percibida del software SIVAC (PU)")
    par(doc, "", size=4, after=2)
    _tabla_likert(doc, ["PE-01", "PE-02", "PE-03", "PE-04"], ITEMS_PE,
                  "Dimensión TAM 2: Facilidad de uso percibida del software SIVAC (PEOU)")
    # 5. Baremo
    par(doc, "5. Sistema de calificación y baremo de interpretación (Modalidad A)", bold=True, before=10,
        after=3, pbb=True, keep_next=True)
    par(doc, "Puntuación por subescala (AP y UP): suma de 4 reactivos en escala de 1 a 5;", align="both", after=1)
    par_formula(doc, [(MML_SUBESCALA, "omml")], size=10.5)
    par(doc, "para j = 1, 2, 3, 4; rango posible: 4 a 20 puntos.", align="both", after=1)
    par(doc, "Puntuación global: suma de los 8 reactivos de la Modalidad A (AP-01 a AP-04 y UP-01 a UP-04):",
        align="both", after=1)
    par_formula(doc, [(MML_GLOBAL, "omml")], size=10.5)
    par(doc, "para i = 1, …, 8; rango posible: 8 a 40 puntos.", align="both", after=1)
    par(doc, "Declaración sobre la Modalidad B: los 8 reactivos del módulo anexo (PU-01 a PU-04 y PE-01 a PE-04) "
             "no se bareman, no generan puntaje global ni se suman con los de la Modalidad A. Sus respuestas se "
             "reportan de forma descriptiva por reactivo, sin categorización ordinal ni contraste inferencial.",
        align="both", after=3)
    par(doc, "Baremo de interpretación por terciles teóricos: la partición en 8 a 18, 19 a 29 y 30 a 40 "
             "constituye un tercil teórico calculado sobre el rango posible de la suma de los 8 reactivos Likert "
             "de 1 a 5 de la Modalidad A. Los tres rangos no constituyen puntos de corte normativos validados "
             "empíricamente, por cuanto con n = 14 no existe distribución de referencia que los sustente.",
        align="both", after=3)
    tabla(doc, ["Nivel categorial", "Rango global (8 reactivos)", "Rango subescala (4 reactivos)",
                "Interpretación operativa en la DISA Apurímac II"],
          BAREMO, [1900, 1700, 1700, ANCHO_RETRATO - 5300], ANCHO_RETRATO,
          alinear=["left", "center", "center", "both"])
    # 6. Protocolo psicometrico
    par(doc, "6. Protocolo psicométrico de confiabilidad (consistencia interna)", bold=True, before=10, after=3,
        pbb=True, keep_next=True)
    par(doc, "El coeficiente Alfa de Cronbach mide la covariación media entre los reactivos bajo el supuesto de "
             "tau-equivalencia esencial:", align="both", after=1)
    par_formula(doc, [(MML_ALFA, "omml")], size=10.5)
    par(doc, "donde k = 8 es el número total de reactivos de la Modalidad A, σi² es la varianza del reactivo i, "
             "y σt² es la varianza del puntaje global de la Modalidad A.", align="both", after=1)
    par(doc, "Criterio de aceptabilidad psicométrica: alfa igual o mayor que 0.70 (estándar canónico de Nunnally "
             "y Bernstein, 1994, para instrumentos de investigación aplicada; deseable igual o mayor que 0.80).",
        align="both", after=3)
    par(doc, "El coeficiente Omega de McDonald se conserva como referencia conceptual del estimador derivado de "
             "cargas factoriales, con la expresión general:", align="both", after=1)
    par_formula(doc, [(MML_OMEGA, "omml")], size=10.5)
    par(doc, "donde λi es la carga factorial del reactivo i y σt² es la varianza del puntaje total. No se aplica "
             "ni se reporta en este estudio: con n = 14 y k = 8 no converge una solución factorial de dos "
             "factores con ocho indicadores (razón sujeto/reactivo 14/8 = 1.75, inferior al rango de 5 a 10 "
             "recomendado). La estimación de la consistencia interna se restringe al coeficiente Alfa de "
             "Cronbach.", align="both", after=3)
    par(doc, "Muestra piloto de calibración externa (n = 15): como procedimiento previsto del plan psicométrico, "
             "una vez validado el contenido se prevé administrar el instrumento a una muestra piloto "
             "independiente de quince operadores de inmunizaciones de redes sanitarias limítrofes que no forman "
             "parte del estudio censal de la DISA Apurímac II. El protocolo previsto para ese piloto comprende "
             "el intervalo de confianza del 95 % para alfa mediante el método de Feldt, la correlación interítem "
             "media y la revisión de consistencia entre subescalas; este expediente no certifica la ejecución de "
             "dicho piloto ni la aptitud definitiva del instrumento.", align="both", after=3)
    # 7. Registro y conformidad
    par(doc, "7. Registro y conformidad de aplicación (Modalidad A)", bold=True, before=10, after=3,
        keep_next=True)
    par(doc, "Los puntajes anotados a continuación corresponden exclusivamente a la Modalidad A del instrumento "
             "(reactivos AP-01 a AP-04 y UP-01 a UP-04). La Modalidad B no se registra en este bloque por "
             "carecer de puntaje global y de baremación.", align="both", after=3)
    tabla(doc, ["Campo de registro", "Resultado"], [
        ["Puntaje subescala Aceptación del proceso (AP)", "______ / 20 puntos"],
        ["Puntaje subescala Utilidad percibida (UP)", "______ / 20 puntos"],
        ["Puntaje total directo de la Modalidad A (8 reactivos)", "______ / 40 puntos"],
        ["Nivel de satisfacción según el baremo",
         "[  ] Nivel bajo (8 a 18)     [  ] Nivel medio (19 a 29)     [  ] Nivel alto (30 a 40)"],
    ], [4400, ANCHO_RETRATO - 4400], ANCHO_RETRATO, alto_min=360)
    par(doc, "", size=4, before=4)
    par(doc, "Firma del participante: ______________________________________", after=1, line=1.0)
    par(doc, "DNI: ________________________     Fecha: ______ / ______ / 2025", after=1, line=1.0)
    par(doc, "Firma del encuestador: ______________________________     Tesista EPIS-UNAJMA",
        after=0, line=1.0)


# ------------------------------------------------------------------- matrices

MC_PG = ("¿En qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de movimientos mensuales de vacunas en el "
         "personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025?")
SUJ = "en el personal de inmunizaciones de la Dirección de Salud Apurímac II"


def _mc(dim):
    return (f"¿En qué medida la aplicación del sistema \"SIVAC\" mejora la {dim} en la gestión de movimientos mensuales de "
            f"vacunas {SUJ}, Andahuaylas 2025?",
            f"Determinar en qué medida la aplicación del sistema \"SIVAC\" mejora la {dim} en la gestión de "
            f"movimientos mensuales de vacunas {SUJ}, Andahuaylas 2025.",
            f"La aplicación del sistema \"SIVAC\" mejora significativamente la {dim} en la gestión de "
            f"movimientos mensuales de vacunas {SUJ}.")


METODOLOGIA = "\n".join([
    "• Tipo: aplicada.", "• Enfoque: cuantitativo.", "• Nivel: explicativo (alcance evaluativo-comparativo).",
    "• Diseño: preexperimental con pretest y postest en un solo grupo (O1, X, O2).",
    "• Población y muestra: censal, N = n = 14 trabajadores.",
    "• Técnicas e instrumentos: observación con la Ficha N.° 01; cotejo documental con la Ficha N.° 02; "
    "encuesta con el Cuestionario N.° 03.",
    "• Validez: juicio de expertos para los tres instrumentos (Fichas N.° 01 y N.° 02 mediante hojas de "
    "evaluación de contenido del protocolo; Cuestionario N.° 03 mediante certificado de reactivos); la "
    "confiabilidad se estima después, con los datos del estudio.",
    "• Plan estadístico: estadística descriptiva, prueba de normalidad de Shapiro-Wilk y prueba de Wilcoxon "
    "para muestras relacionadas (p < 0.05).",
])

ENCABEZADOS_MC = ["Problemas", "Objetivos", "Hipótesis", "Variables y dimensiones", "Indicadores y escalas",
                  "Metodología"]
ANCHOS_MC = [2300, 2300, 2300, 2100, 2500, 2500]  # suma 14000


def pieza_matriz_consistencia(doc):
    """Matriz de consistencia en CUATRO tablas-bloque (general + 3 especificos):
    ninguna fila excede la altura de la pagina apaisada; contenido integro."""
    nueva_seccion(doc, "apaisada")
    par(doc, "MATRIZ DE CONSISTENCIA", bold=True, align="center", after=2, pbb=True)
    par(doc, TITULO_TESIS, italic=True, align="center", size=TAM_TABLA, line=1.0, after=6)
    d1, d2, d3 = _mc("oportunidad de procesamiento"), _mc("consistencia documental"), _mc("satisfacción del usuario")
    bloques = [
        ["Problema general:\n" + MC_PG,
         "Objetivo general:\nDeterminar en qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de "
         f"movimientos mensuales de vacunas {SUJ}, Andahuaylas 2025.",
         "Hipótesis general:\nLa aplicación del sistema \"SIVAC\" mejora significativamente la gestión de "
         f"movimientos mensuales de vacunas {SUJ}, Andahuaylas 2025.\nSe acepta si se rechaza la hipótesis nula en las "
         "tres hipótesis específicas (p < 0.05).",
         "Variable independiente:\nSistema web SIVAC.\nCondición X0 (pretest): ausencia del sistema; gestión "
         "manual tradicional.\nCondición X1 (postest): presencia y uso del sistema SIVAC.",
         "Escala: dicotómica nominal (0 = pretest, 1 = postest).\nSustento técnico: metodología Extreme "
         "Programming y calidad ISO/IEC 25010:2023.", METODOLOGIA],
        ["Problema específico 1:\n" + d1[0], "Objetivo específico 1:\n" + d1[1], "Hipótesis específica 1:\n" + d1[2],
         "Variable dependiente:\nGestión de movimientos mensuales de vacunas.\nDimensión 1: oportunidad de procesamiento.",
         "• Tiempo de registro de movimientos (Treg), en minutos decimales, escala de razón.\n"
         "• Tiempo de emisión de vales (Tvale), en minutos decimales, escala de razón.\nInstrumento: Ficha N.° 01.", ""],
        ["Problema específico 2:\n" + d2[0], "Objetivo específico 2:\n" + d2[1], "Hipótesis específica 2:\n" + d2[2],
         "Dimensión 2: consistencia documental.",
         "• Registros sin discrepancias (RSD), en porcentaje, escala de razón.\n"
         "• Concordancia entre cantidad programada y entregada (CPE), en porcentaje acotado entre 0 y 100.\n"
         "Instrumento: Ficha N.° 02.", ""],
        ["Problema específico 3:\n" + d3[0], "Objetivo específico 3:\n" + d3[1], "Hipótesis específica 3:\n" + d3[2],
         "Dimensión 3: satisfacción del usuario (satisfacción con el proceso).",
         "• Aceptación del proceso operativo (AP), 4 ítems, 4 a 20 puntos.\n"
         "• Utilidad percibida (UP), 4 ítems, 4 a 20 puntos.\nTotal: 8 ítems, 8 a 40 puntos, escala Likert de 1 a 5.\n"
         "Instrumento: Cuestionario N.° 03, Modalidad A.", ""],
    ]
    for i, bloque in enumerate(bloques):
        if i > 0:
            par(doc, "", size=4, after=2, before=2)
        tabla(doc, ENCABEZADOS_MC, [bloque], ANCHOS_MC, ANCHO_APAISADA)


def _filas_operacionalizacion():
    """Filas literales de la operacionalizacion (compartidas con el perfil v08)."""
    return [
        ["Variable independiente:\nSistema web SIVAC", "Intervención tecnológica", "X0: gestión manual (pretest).\n"
         "X1: gestión con SIVAC (postest).", "Presencia o ausencia del sistema.", "Dicotómica nominal", "Capítulo III"],
        ["Variable dependiente:\nGestión de movimientos mensuales de vacunas", "1. Oportunidad de procesamiento",
         "Tiempo de registro (Treg)", "Minutos transcurridos entre el inicio y el fin del registro de un movimiento.",
         "Minutos decimales, razón", "Ficha N.° 01 (tres tareas por participante)"],
        ["", "", "Tiempo de emisión de vale (Tvale)", "Minutos entre la solicitud y la emisión del comprobante de salida.",
         "Minutos decimales, razón", "Ficha N.° 01 (tres tareas por participante)"],
        ["", "2. Consistencia documental", "Registros sin discrepancias (RSD)",
         "Porcentaje de registros que cumplen simultáneamente los ocho criterios de conformidad.",
         "Porcentaje, razón", "Ficha N.° 02 (40 a 60 registros por ventana de 30 días)"],
        ["", "", "Concordancia programada y entregada (CPE)",
         "Porcentaje de entregas cuya cantidad entregada coincide con la programada o cuenta con justificación formal.",
         "Porcentaje entre 0 y 100, razón", "Ficha N.° 02 (40 a 60 entregas por ventana de 30 días)"],
        ["", "3. Satisfacción del usuario", "Aceptación del proceso operativo (AP)",
         "Conformidad con la agilidad, fluidez y carga de trabajo del proceso (4 ítems, 4 a 20 puntos).",
         "Likert de 1 a 5, ordinal", "Cuestionario N.° 03, Modalidad A"],
        ["", "", "Utilidad percibida (UP)",
         "Percepción de trazabilidad, control de existencias y soporte a la gestión sanitaria (4 ítems, 4 a 20 puntos).",
         "Likert de 1 a 5, ordinal", "Cuestionario N.° 03, Modalidad A"],
    ]


def pieza_operacionalizacion(doc):
    par(doc, "MATRIZ DE OPERACIONALIZACIÓN DE VARIABLES", bold=True, align="center", after=6, pbb=True)
    filas = _filas_operacionalizacion()
    anchos = [2300, 2200, 2300, 3800, 1700, 1700]
    tabla(doc, ["Variable", "Dimensión", "Indicador", "Definición operacional", "Escala", "Instrumento"],
          filas, anchos, ANCHO_APAISADA)
    par(doc, "Nota. Las fórmulas de cálculo de los indicadores se presentan en el cuerpo narrativo del Capítulo IV.",
        size=TAM_TABLA, line=1.0, before=6, italic=True)


# -------------------------------------------------------------------- fichas

def _datos_ficha(doc, filas):
    tabla(doc, ["Campo", "Registro"], filas, [3800, ANCHO_APAISADA - 3800], ANCHO_APAISADA,
          alto_min=400)


def _firmas(doc, lineas):
    par(doc, "", size=6, line=1.0, before=6)
    for l in lineas:
        par(doc, l, line=1.5, before=0)


def pieza_ficha01(doc):
    par(doc, "INSTRUMENTO N.° 01", bold=True, align="center", after=0, pbb=True)
    par(doc, "FICHA DE OBSERVACIÓN SISTEMÁTICA Y MEDICIÓN DE TIEMPOS CRONOMETRADOS", bold=True, align="center",
        after=4)
    par(doc, "Dimensión: oportunidad de procesamiento. Indicadores: tiempo de registro (Treg) y tiempo de emisión "
             "de vale (Tvale). Técnica: observación sistemática directa no participante. Contexto: los elementos "
             "de esta ficha se evalúan en la Hoja de evaluación de contenido N.° 01; esta ficha se adjunta íntegra "
             "y NO se llena.", align="both", after=4)
    par(doc, "1. Datos generales de la observación", bold=True, after=3, keep_next=True)
    _datos_ficha(doc, [
        ["Código del operador evaluado", "TRAB-____  (TRAB-01 a TRAB-14)"],
        ["Rol institucional", "[  ] Responsable de centro de acopio o red de frío   [  ] Personal de la estrategia sanitaria de inmunizaciones"],
        ["Centro de acopio o sede", ""],
        ["Red o microred / provincia", "Provincia:  [  ] Andahuaylas   [  ] Chincheros"],
        ["Momento de medición", "[  ] Pretest (kardex físico, libros de registro y hojas Excel)   [  ] Postest (sistema SIVAC)"],
        ["Fecha de la observación", "______ / ______ / ______"],
        ["Evaluador principal", TESISTA],
        ["Evaluador secundario (si aplica)", ""],
    ])
    par(doc, "2. Protocolo de cronometraje", bold=True, before=8, after=3, keep_next=True)
    for s in [
        "Se emplea un cronómetro digital con precisión de centésimas de segundo. El tiempo se expresa en minutos "
        "decimales: minutos enteros más segundos divididos entre 60.",
        "Treg: inicia cuando el operador toma el documento fuente o abre la interfaz para digitar el movimiento, y "
        "termina cuando el movimiento queda grabado, confirmado o asentado con saldo actualizado.",
        "Tvale: inicia cuando el operador recibe la solicitud de biológicos y termina cuando el vale queda generado, "
        "firmado o impreso con numeración correlativa.",
        "Si ocurre una interrupción ajena al proceso (corte de energía, sismo, emergencia sanitaria), el cronómetro "
        "se detiene y se registra solo el tiempo neto de trabajo.",
        "Cada operador ejecuta tres tareas de registro y tres de emisión de vales. Para el análisis, las tres "
        "mediciones se consolidan en un único valor por operador y momento.",
    ]:
        par(doc, "•  " + s, align="both", hanging=0.8, after=2)
    par(doc, "3. Sección A: medición del tiempo de registro de movimientos (Treg)", bold=True, before=8, after=3,
        keep_next=True)
    anchos = [500, 900, 2900, 1700, 800, 1350, 1350, 1350, 1350, 1800]
    tabla(doc, ["N.°", "Código", "Movimiento estandarizado", "Biológicos y lotes", "Dosis", "Hora de inicio",
                "Hora de fin", "Tiempo neto (min:s)", "Treg (min)", "Incidencias"], [
        ["1", "REG-01", "Ingreso simple de remesa (1 biológico)"] + [""] * 7,
        ["2", "REG-02", "Salida regular programada (2 a 3 vacunas)"] + [""] * 7,
        ["3", "REG-03", "Redistribución o despacho complejo (4 a 6 ítems)"] + [""] * 7,
    ], anchos, ANCHO_APAISADA, alto_min=700,
        alinear=["center", "center", "left", "left", "center", "center", "center", "center", "center", "left"])
    par(doc, "Tiempo representativo del operador (promedio de las tres tareas): ____________ min", before=6, after=0)
    par(doc, "Mediana de las tres tareas: ____________ min")
    par(doc, "4. Sección B: medición del tiempo de emisión de vales (Tvale)", bold=True, before=8, after=3,
        pbb=True)
    tabla(doc, ["N.°", "Código", "Tipo de vale estandarizado", "N.° de documento", "Ítems", "Hora de inicio",
                "Hora de fin", "Tiempo neto (min:s)", "Tvale (min)", "Incidencias"], [
        ["1", "VALE-01", "Vale simple (puesto I-1 o I-2; 1 a 2 biológicos)", "Vale N.°:"] + [""] * 6,
        ["2", "VALE-02", "Vale regular (centro I-3 o I-4; 3 a 5 biológicos)", "Vale N.°:"] + [""] * 6,
        ["3", "VALE-03", "Vale de emergencia o reposición urgente", "Vale N.°:"] + [""] * 6,
    ], anchos, ANCHO_APAISADA, alto_min=700,
        alinear=["center", "center", "left", "left", "center", "center", "center", "center", "center", "left"])
    par(doc, "Tiempo representativo del operador (promedio de las tres tareas): ____________ min", before=6, after=0)
    par(doc, "Mediana de las tres tareas: ____________ min")
    par(doc, "5. Resumen y firmas", bold=True, before=8, after=3, keep_next=True)
    tabla(doc, ["Indicador", "Promedio del operador (min)", "Mediana del operador (min)"], [
        ["Tiempo de registro (Treg)", "", ""], ["Tiempo de emisión de vales (Tvale)", "", ""],
    ], [5400, 4300, 4300], ANCHO_APAISADA, alto_min=420, alinear=["left", "center", "center"])
    par(doc, "Declaración de conformidad: la presente toma de tiempos se realizó respetando los puntos de inicio y "
             "fin del protocolo, con fidelidad y veracidad de los datos registrados.", align="both", before=6, keep_next=True)
    _firmas(doc, [
        "Firma del investigador: ______________________________   " + TESISTA + ", Tesista",
        "V.° B.° del operador observado: ______________________________   Nombre: ______________________",
        "DNI: ________________   Cargo: ______________________   Sede: ______________________",
    ])


CRITERIOS_RSD = [
    "Tipo de movimiento clasificado de forma unívoca (entrada por remesa, salida a establecimiento o ajuste).",
    "Denominación oficial estandarizada del biológico según el esquema regular nacional.",
    "Identificación exacta del número de lote, coincidente con el rótulo del frasco.",
    "Cantidad de dosis o viales exacta y coincidente con el stock físico y el acta de recepción.",
    "Fecha del movimiento consignada completa (día, mes y año) y en secuencia cronológica.",
    "Establecimiento de origen o destino individualizado con su código oficial.",
    "Nombre, firma o usuario responsable del despacho o recepción plenamente trazable.",
    "Documento formal de respaldo asociado y verificado (vale oficial, PECOSA o guía de remisión).",
]
VACUNAS_RSD = ["Vacuna BCG", "Hepatitis B pediátrica", "Vacuna pentavalente", "Neumococo conjugada", "Rotavirus",
               "Antipolio inactivada (IPV)", "Antipolio oral (bOPV)", "Vacuna SPR", "Antiamarílica (AMA)",
               "Influenza adulto", "Influenza pediátrica", "Vacuna contra VPH", "dT adulto", "dTpa gestante",
               "Varicela", "Hepatitis A", "COVID-19", "Jeringas descartables autodesactivables",
               "Diluyentes de biológicos", "Cajas térmicas y paquetes fríos"]
VACUNAS_CPE = ["Vacuna pentavalente", "Neumococo conjugada", "Rotavirus", "Vacuna SPR", "Influenza adulto",
               "Influenza pediátrica", "Vacuna contra VPH", "dT adulto", "Antipolio (IPV o bOPV)", "Vacuna BCG",
               "Antiamarílica (AMA)", "Hepatitis B"]


def pieza_ficha02(doc):
    par(doc, "INSTRUMENTO N.° 02", bold=True, align="center", after=0, pbb=True)
    par(doc, "FICHA DE REGISTRO Y COTEJO DOCUMENTAL DE CONSISTENCIA", bold=True, align="center", after=4)
    par(doc, "Dimensión: consistencia documental. Indicadores: registros sin discrepancias (RSD) y concordancia "
             "entre cantidad programada y entregada (CPE). Técnica: análisis documental. Contexto: los elementos "
             "y criterios de esta ficha se evalúan en la Hoja de evaluación de contenido N.° 02; esta ficha se "
             "adjunta íntegra y NO se llena.", align="both", after=4)
    par(doc, "1. Datos generales de la auditoría documental", bold=True, after=3, keep_next=True)
    _datos_ficha(doc, [
        ["Código del operador o centro auditado", "TRAB-____  (TRAB-01 a TRAB-14)"],
        ["Centro de acopio o microred", ""],
        ["Provincia sanitaria", "[  ] Andahuaylas   [  ] Chincheros"],
        ["Momento de medición", "[  ] Pretest (kardex manual, cuadernos y hojas Excel)   [  ] Postest (base de datos y vales electrónicos de SIVAC)"],
        ["Ventana de auditoría (30 días calendario)", "Del ____ / ____ / ______  al  ____ / ____ / ______"],
        ["Fecha de ejecución de la auditoría", "______ / ______ / ______"],
        ["Auditor principal", TESISTA],
        ["Auditor secundario (si aplica)", ""],
    ])
    par(doc, "2. Criterios de conformidad para RSD", bold=True, before=8, after=3, pbb=True, keep_next=True)
    par(doc, "Un registro es conforme (1) cuando cumple simultáneamente los ocho criterios siguientes; si incumple "
             "al menos uno, es no conforme (0). Se audita un corpus de 40 a 60 registros por ventana temporal.",
        align="both", after=3)
    for i, c in enumerate(CRITERIOS_RSD, start=1):
        par(doc, f"C{i}.  {c}", align="both", hanging=1.2, after=2)
    par(doc, "3. Sección A: auditoría de registros sin discrepancias (RSD)", bold=True, before=8, after=3,
        keep_next=True)
    anchos = [500, 3000, 1200, 1100] + [500] * 8 + [1600, 2600]
    filas = [[f"{i:02d}", v, "", ""] + [""] * 8 + ["[  ] 1   [  ] 0", ""] for i, v in enumerate(VACUNAS_RSD, 1)]
    tabla(doc, ["N.°", "Vacuna o insumo auditado", "Lote", "Cantidad"] + [f"C{i}" for i in range(1, 9)] +
          ["Veredicto (1 conforme, 0 no conforme)", "Tipo de discrepancia o causa"], filas, anchos, ANCHO_APAISADA,
          alto_min=330,
          alinear=["center", "left", "left", "center"] + ["center"] * 8 + ["center", "left"])
    par(doc, "Si el corpus supera las filas disponibles, continúe en una hoja adicional con el mismo formato.",
        size=TAM_TABLA, line=1.0, before=4, italic=True)
    par(doc, "Total de registros evaluados: ______      Registros conformes: ______      Registros con discrepancia: "
             "______      RSD: ______ %", before=6)
    par(doc, "4. Sección B: auditoría de concordancia entre programación y entrega (CPE)", bold=True, before=8,
        after=3, pbb=True)
    par(doc, "Una entrega es concordante (1) si la cantidad entregada es idéntica a la programada o si, siendo "
             "distinta, existe un documento oficial archivado que autoriza expresamente la variación. En cualquier "
             "otro caso es no concordante (0).", align="both", after=3)
    anchos2 = [500, 2700, 1700, 1400, 1400, 1400, 2300, 1200, 1400]
    filas2 = [[f"{i:02d}", v, "Vale N.°:", "", "", "", "[  ] Sí  [  ] No  [  ] N/A", "[  ] 1  [  ] 0", ""]
              for i, v in enumerate(VACUNAS_CPE, 1)]
    tabla(doc, ["N.°", "Vacuna o biológico", "N.° de documento", "Cantidad programada", "Cantidad entregada",
                "Diferencia absoluta", "Justificación formal acreditada", "Veredicto", "Causa del desfase"],
          filas2, anchos2, ANCHO_APAISADA, alto_min=400,
          alinear=["center", "left", "left", "center", "center", "center", "center", "center", "left"])
    par(doc, "Total de entregas auditadas: ______      Entregas concordantes: ______      Entregas no concordantes: "
             "______      CPE: ______ %", before=6)
    par(doc, "5. Resumen y firmas", bold=True, before=8, after=3, keep_next=True)
    tabla(doc, ["Indicador", "Resultado pretest", "Resultado postest", "Variación absoluta"], [
        ["Registros sin discrepancias (RSD)", "______ %", "______ %", "______ %"],
        ["Concordancia programada y entregada (CPE)", "______ %", "______ %", "______ %"],
    ], [5200, 2900, 2900, 3000], ANCHO_APAISADA, alto_min=420,
        alinear=["left", "center", "center", "center"])
    _firmas(doc, [
        "Firma del auditor: ______________________________   " + TESISTA + ", Tesista",
        "V.° B.° de la coordinación de inmunizaciones: ______________________________",
        "Nombre del responsable: ______________________   DNI: ________________",
    ])


# ============================================================ PERFIL COMPACTO v06
# Mandato expreso del tesista (2026-10-19, molesto por las 33 paginas de v05):
# formato MINIMO en orden modelo ITEM (carta breve, instrucciones con tabla de
# criterios y UNA sola tabla continua de validez de contenido de los
# instrumentos que miden la variable dependiente, con numeracion corrida 1..12
# y UN unico cierre al final). Sin hoja informativa de la VI, sin panorama, sin
# matrices, sin fichas completas, sin cuestionario repetido, sin baremos, sin
# formulas ni certificados separados. Objetivo: 4 paginas (maximo 5). El perfil
# integral v05 permanece intacto; este perfil se agrega, genera y verifica por
# separado. Fuente durable: certificado_vd_compacto_v06.json del
# especialista-instrumentos (textos_evaluado y dimensiones; las filas nuevas
# D1/D2 son resumenes descriptivos de componentes reales de las fichas, no
# preguntas nuevas de percepcion; los 8 reactivos de satisfaccion son los
# mismos literales AP/UP de siempre). Ninguna marca prellenada ni juez
# inventado.

VERSION_COMPACTO = "v06"
RUTA_JSON_COMPACTO = RUTA_SALIDA / "certificado_vd_compacto_v06.json"
TITULO_INSTRUCCIONES_COMPACTO = "INSTRUCCIONES PARA VALIDACIÓN DEL INSTRUMENTO"
TITULO_INSTRUMENTO_VALIDACION = "INSTRUMENTO DE VALIDACIÓN"

# Marcadores de piezas del perfil compacto (orden obligatorio).
MARCADORES_COMPACTO = ["Andahuaylas, ", TITULO_INSTRUCCIONES_COMPACTO, TITULO_INSTRUMENTO_VALIDACION]

# Piezas del integral v05 que NO deben aparecer en el compacto (exclusion de
# anexos y hojas separadas ordenada por el tesista).
MARCADORES_ANEXOS_V05 = [
    TITULO_HOJA_VI, TITULO_PANORAMA, TITULO_HOJA_01, TITULO_HOJA_02,
    "CERTIFICADO DE VALIDEZ DE CONTENIDO DEL INSTRUMENTO N.° 03",
    "MATRIZ DE CONSISTENCIA", "MATRIZ DE OPERACIONALIZACIÓN DE VARIABLES",
    "MODALIDAD B", "NIVEL BAJO", "Alfa de Cronbach", "Puntaje Global",
]

_COMPACTO = {}


def _cargar_compacto():
    """Carga y valida el JSON durable del especialista (cache). Exige
    numeracion continua 1..12, tres dimensiones (2+2+8) y los 8 reactivos de
    satisfaccion identicos a los literales AP/UP del cuestionario."""
    if "grupos" not in _COMPACTO:
        import json
        spec = json.loads(RUTA_JSON_COMPACTO.read_text(encoding="utf-8"))
        grupos = []
        for g in spec["grupos"]:
            grupos.append((g["dimension"], [(f["id"], f["texto_evaluado"]) for f in g["filas"]]))
        ids = [i for _, filas in grupos for i, _ in filas]
        if ids != list(range(1, 13)):
            raise ValueError(f"JSON compacto: ids no continuos 1..12: {ids}")
        if [len(f) for _, f in grupos] != [2, 2, 8]:
            raise ValueError("JSON compacto: se esperan 2+2+8 filas por dimension")
        norm = fany._normalizar
        literales = [norm(x) for _, filas in grupos for _, x in filas][4:]
        if literales != [norm(x) for x in ITEMS_AP + ITEMS_UP]:
            raise ValueError("JSON compacto: los reactivos de satisfaccion no son identicos a AP/UP")
        _COMPACTO["spec"] = spec
        _COMPACTO["grupos"] = grupos
    return _COMPACTO


def compacto_carta(doc):
    """Carta MINIMA en orden modelo ITEM: fecha, destinatario en blanco,
    solicitud breve con el titulo exacto, lista corta y firma del tesista."""
    par(doc, f"Andahuaylas, ........ de ........................ de {ANIO}", align="right", after=2)
    par(doc, "Señor(a): ...........................................................", after=0)
    par(doc, "Docente de la Escuela Profesional de Ingeniería de Sistemas", italic=True, after=4)
    par(doc, "De mi mayor consideración:", after=4)
    par(doc, f"Yo, {TESISTA}, tesista de la Escuela Profesional de Ingeniería de Sistemas de la Universidad "
             "Nacional José María Arguedas, me dirijo a usted para solicitarle su colaboración como juez experto "
             "en la validación de contenido de los instrumentos que miden la variable dependiente de mi "
             f"investigación, intitulada “{TITULO_TESIS}”. Los tres instrumentos del estudio se someten a juicio "
             "de contenido mediante un certificado único que integra sus tres dimensiones con numeración "
             "continua; revisarlos no equivale a contestar datos ni preguntas de percepción.",
        align="both", first=1.27)
    par(doc, "Adjunto los siguientes documentos:", before=2, after=0, keep_next=True)
    par(doc, "1.  Instrucciones para la validación del instrumento.", hanging=1.27, after=2)
    par(doc, "2.  Certificado de validez de contenido de los instrumentos que miden la variable dependiente: "
             "gestión de movimientos mensuales de vacunas (una sola tabla continua con las tres dimensiones y un único "
             "bloque de cierre).", hanging=1.27, after=2, align="both")
    par(doc, "Agradezco anticipadamente su atención a la presente.", before=2, first=1.27, after=4)
    par(doc, "Atentamente,", align="center", after=10)
    par(doc, "..........................................................", align="center", line=1.0)
    par(doc, TESISTA, align="center", bold=True, line=1.0)
    par(doc, "Tesista", align="center", line=1.0)


def compacto_instrucciones(doc):
    """Instrucciones de 1 pagina: puntos cortos y guia de los 3 criterios
    SIEMPRE en tabla nativa; aclara objetos distintos (campos/protocolo frente
    a reactivos), que no es una escala unica ni evalua resultados percibidos."""
    par(doc, TITULO_INSTRUCCIONES_COMPACTO, bold=True, align="center", pbb=True, after=6)
    par(doc, "Las instrucciones para la validación del instrumento son las siguientes:", after=3)
    par(doc, "1.  En el certificado de validez de contenido, marque con una equis (X) la opción Sí o No de los "
             "tres criterios siguientes, por cada elemento o reactivo, y anote sus observaciones en la columna "
             "Sugerencias:", align="both", hanging=1.0, after=3)
    tabla(doc, ["Criterio", "Descripción"], [
        ["Pertinencia", "El ítem corresponde al concepto teórico formulado."],
        ["Relevancia", "El ítem es apropiado para representar al componente o dimensión específica del constructo."],
        ["Claridad", "El enunciado se entiende sin dificultad; es conciso, exacto y directo."],
    ], [1900, ANCHO_RETRATO - 1900], ANCHO_RETRATO)
    separador(doc)
    par(doc, "2.  Evalúe los elementos e ítems presentados; las fichas fuente pueden consultarse por separado.",
        align="both", hanging=1.0, after=3)
    par(doc, "3.  La numeración es continua de 1 a 12 en una sola tabla que continúa en la página siguiente, sin "
             "reiniciarse por dimensión; al final complete un único bloque de cierre con sus observaciones, su "
             "opinión de aplicabilidad, sus datos y su firma.", align="both", hanging=1.0, after=3)
    par(doc, "4.  Devuelva el certificado completo al investigador. Agradecemos profundamente su colaboración.",
        align="both", hanging=1.0, after=0)


def compacto_tabla(doc, grupos):
    """UNA sola tabla continua de 9 columnas a 8788 dxa: encabezado de 2 filas,
    3 filas de dimension integradas (con Si/No repetido, como en el modelo Fany)
    y 12 filas de elementos con numeracion corrida 1..12, sin salto de pagina
    entre dimensiones (la tabla fluye con encabezado repetido)."""
    anchos = ANCHOS_CERT
    n_elem = sum(len(filas) for _, filas in grupos)
    t = doc.add_table(rows=2 + len(grupos) + n_elem, cols=9)
    quir.configurar_geometria_tabla(t, ANCHO_RETRATO, anchos, align="center",
                                    cell_margin_dxa=(20, 50, 20, 50))
    quir.aplicar_bordes_apa7(t)
    fany.fijar_disposicion_fija(t)
    for c in (0, 1, 8):
        celda = t.cell(0, c).merge(t.cell(1, c))
        celda.width = Cm(anchos[c] / 567.0)
    for c in (2, 4, 6):
        celda = t.cell(0, c).merge(t.cell(0, c + 1))
        celda.width = Cm((anchos[c] + anchos[c + 1]) / 567.0)
    fany.texto_celda(t.cell(0, 0), "N.°", tamano=fany.TAM_ENCABEZADO, negrita=True)
    fany.texto_celda(t.cell(0, 1), "DIMENSIONES / ÍTEMS (ELEMENTOS)", tamano=fany.TAM_ENCABEZADO, negrita=True)
    fany.texto_celda_con_superindice(t.cell(0, 2), "Pertinencia", "1", tamano=fany.TAM_ENCABEZADO)
    fany.texto_celda_con_superindice(t.cell(0, 4), "Relevancia", "2", tamano=fany.TAM_ENCABEZADO)
    fany.texto_celda_con_superindice(t.cell(0, 6), "Claridad", "3", tamano=fany.TAM_ENCABEZADO)
    fany.texto_celda(t.cell(0, 8), "Sugerencias", tamano=fany.TAM_ENCABEZADO, negrita=True)
    for c, etiqueta in ETIQUETAS_CERT.items():
        fany.texto_celda(t.cell(1, c), etiqueta, tamano=fany.TAM_ENCABEZADO, negrita=True)
    fila = 2
    filas_dim = []
    for etiqueta_dim, elementos in grupos:
        celda_g = t.cell(fila, 0).merge(t.cell(fila, 1))
        celda_g.width = Cm((anchos[0] + anchos[1]) / 567.0)
        fany.texto_celda(celda_g, etiqueta_dim, tamano=fany.TAM_DIMENSION, negrita=True,
                         alineacion="left", before=15, after=15, margen_izq_dxa=50)
        for c, etiqueta in ETIQUETAS_CERT.items():
            fany.texto_celda(t.cell(fila, c), etiqueta, tamano=fany.TAM_ENCABEZADO, negrita=True)
        fany.fijar_contenido_celda(t.cell(fila, 8), fany._p_vacio())
        filas_dim.append(fila)
        fila += 1
        for num, texto in elementos:
            fany.texto_celda(t.cell(fila, 0), str(num), tamano=10.0, alineacion="center")
            fany.texto_celda(t.cell(fila, 1), texto, tamano=fany.TAM_ITEM, alineacion="both",
                             before=10, after=10, margen_izq_dxa=50)
            for c in fany.COLS_CRITERIO:
                fany.fijar_contenido_celda(t.cell(fila, c), fany._p_vacio())
            fany.fijar_contenido_celda(t.cell(fila, 8), fany._p_vacio())
            fila += 1
    fany.normalizar_celdas_sin_parrafo(t)
    _linea_inferior_fila(t, 1)
    for fd in filas_dim:
        _linea_inferior_fila(t, fd)
    for row in t.rows:
        for cell in row.cells:
            cell.vertical_alignment = fany.WD_ALIGN_VERTICAL.CENTER
    quir.blindar_filas_tabla(t, cant_split=True, repetir_encabezado=True, filas_encabezado=2)
    quir.normalizar_orden_tblPr(t)
    return t


def pieza_certificado_compacto(doc):
    """Instrumento de validacion: encabezado, titulo unico del certificado VD,
    nota de alcance, la tabla continua, UN cierre y las notas 1-3."""
    fany.TAM_ITEM, fany.TAM_CODIGO, fany.TAM_ENCABEZADO = 10.0, 9.0, 9.5
    fany.TAM_DIMENSION, fany.TAM_BLOQUE = 10.0, 10.0
    espec = _cargar_compacto()
    par(doc, TITULO_INSTRUMENTO_VALIDACION, bold=True, align="center", pbb=True, after=2)
    par(doc, espec["spec"]["titulo"], bold=True, align="center", size=12, line=1.2, after=2)
    par(doc, espec["spec"]["nota_unica"], align="center", size=10, after=5)
    compacto_tabla(doc, espec["grupos"])
    construir_bloque_cierre(doc)
    construir_notas_pie(doc, tamano=9.5)


def construir_compacto():
    doc = docx.Document()
    configurar_normal(doc)
    aplicar_geometria(doc.sections[0], "unajma")
    pie_pagina(doc.sections[0])
    cp = doc.core_properties
    cp.author, cp.title, cp.last_modified_by = TESISTA, TITULO_INSTRUMENTO_VALIDACION.title(), TESISTA
    cp.comments, cp.subject, cp.keywords = "", "", ""
    compacto_carta(doc)
    compacto_instrucciones(doc)
    pieza_certificado_compacto(doc)
    return doc


def nombre_compacto(n):
    return f"EXPEDIENTE_VALIDACION_SIVAC_COMPACTO_EXPERTO_0{n}_{VERSION_COMPACTO}.docx"


def _auditar_tabla_compacto(t, grupos):
    """Controles estructurales de la tabla unica del certificado compacto."""
    res = []

    def chk(nom, ok, det=""):
        res.append((f"Tabla compacta: {nom}", bool(ok), det))

    trs = t._tbl.findall(qn("w:tr"))
    n_elem = sum(len(filas) for _, filas in grupos)
    chk("17 filas (2 encabezado + 3 dimensiones + 12 elementos)",
        len(trs) == 2 + len(grupos) + n_elem, f"{len(trs)} filas")
    enc_crit = [_txt(trs[1].findall(qn("w:tc"))[c]).strip() for c in fany.COLS_CRITERIO]
    chk("Etiquetas Si/No con tilde", enc_crit == ["Sí", "No", "Sí", "No", "Sí", "No"], ",".join(enc_crit))
    fila, numeros, textos, llenas = 2, [], [], 0
    for etiqueta_dim, elementos in grupos:
        # La fila de dimension tiene las columnas 0-1 fusionadas (gridSpan):
        # leer mediante row.cells, que resuelve las fusiones, no por XML crudo.
        celdas_dim = t.rows[fila].cells
        primera = _txt(celdas_dim[0]._tc).strip()
        si_no = [_txt(celdas_dim[c]._tc).strip() for c in fany.COLS_CRITERIO]
        chk(f"Dimension fila con Si/No repetido ({etiqueta_dim[:34]}...)",
            primera == etiqueta_dim and si_no == ["Sí", "No", "Sí", "No", "Sí", "No"], primera[:40])
        fila += 1
        for num, texto in elementos:
            if fila >= len(trs):
                chk("Filas de elemento suficientes", False,
                    f"faltan filas (se esperaba el elemento {num})")
                return res
            tcs = trs[fila].findall(qn("w:tc"))
            numeros.append(_txt(tcs[0]).strip())
            textos.append(_txt(tcs[1]).strip())
            for c in list(range(2, 9)):
                if _txt(tcs[c]).strip():
                    llenas += 1
            fila += 1
    chk("Numeracion continua 1..12", numeros == [str(i) for i in range(1, 13)], ",".join(numeros[:6]) + "...")
    norm = fany._normalizar
    esperado = [norm(x) for _, filas in grupos for _, x in filas]
    chk("Textos de elementos literales del JSON durable", [norm(x) for x in textos] == esperado)
    chk("Celdas de criterio y sugerencias vacias (sin marcas X)", llenas == 0, f"{llenas} con texto")
    ok_cs = all(tr.find(qn("w:trPr")) is not None and
                tr.find(qn("w:trPr")).find(qn("w:cantSplit")) is not None for tr in trs)
    chk("Filas con cantSplit", ok_cs)
    ok_hd = all(trs[i].find(qn("w:trPr")).find(qn("w:tblHeader")) is not None for i in (0, 1))
    chk("Encabezado de dos filas repetido", ok_hd)
    return res


def verificar_compacto(ruta):
    """Audita el DOCX compacto v06 GUARDADO. Devuelve [(nombre, ok, detalle)]."""
    res = []

    def chk(nombre, ok, det=""):
        res.append((nombre, bool(ok), det))

    espec = _cargar_compacto()
    d = docx.Document(str(ruta))
    body = d.element.body
    txt = "\n".join(t.text or "" for t in body.iter(qn("w:t")))
    plano = re.sub(r"\s+", " ", txt)
    # 1. Estructura de tablas: exactamente 2 (criterios + certificado unico).
    chk("Solo 2 tablas (criterios y certificado unico)", len(d.tables) == 2, str(len(d.tables)))
    cert = [t for t in d.tables
            if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 9
            and int(t._tbl.tblPr.find(qn("w:tblW")).get(qn("w:w"))) == ANCHO_RETRATO]
    chk("UNA sola tabla de certificado (9 columnas a 8788)", len(cert) == 1, str(len(cert)))
    if len(d.tables) == 2 and cert:
        criterios = [t for t in d.tables
                     if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 2]
        if criterios:
            orden = next(i for i, t in enumerate(d.element.body.iter(qn("w:tbl")))
                         if t is criterios[0]._tbl)
            orden_cert = next(i for i, t in enumerate(d.element.body.iter(qn("w:tbl")))
                              if t is cert[0]._tbl)
            chk("Tabla de criterios previa al certificado (orden modelo)",
                len(criterios) == 1 and "Criterio" in _txt(criterios[0]._tbl)
                and orden < orden_cert)
        else:
            chk("Tabla de criterios previa al certificado (orden modelo)", False, "no encontrada")
        res.extend(_auditar_tabla_compacto(cert[0], espec["grupos"]))
    # 2. Orden modelo ITEM: carta, instrucciones, instrumento de validacion.
    pars = [_txt(p) for p in body.findall(qn("w:p"))]
    pos = []
    for m in MARCADORES_COMPACTO:
        idx = next((i for i, t in enumerate(pars) if t.startswith(m)), None)
        pos.append(idx)
    chk("Orden de piezas carta, instrucciones, instrumento de validacion",
        None not in pos and pos == sorted(pos), str(pos))
    chk("Titulo unico del certificado VD presente", espec["spec"]["titulo"] in txt)
    chk("Nota de alcance unica presente", espec["spec"]["nota_unica"] in txt)
    # 3. UN solo cierre al final.
    chk("UN unico bloque de cierre (1 firma, 1 aplicabilidad, 1 identidad del juez)",
        txt.count("Firma del juez validador") == 1
        and txt.count("Apellidos y nombres del juez validador:") == 1
        and txt.count("Opinión de aplicabilidad:") == 1,
        f"firmas={txt.count('Firma del juez validador')}")
    chk("Tres casillas de aplicabilidad en blanco",
        all(x in txt for x in ("Aplicable [   ]", "Aplicable después de corregir [   ]", "No aplicable [   ]")))
    chk(f"Fecha de cierre con dia y mes en blanco y año {ANIO}",
        len(re.findall(r"Andahuaylas, \.+ de \.+ del " + ANIO, txt)) == 1)
    chk("Campos del juez en blanco",
        all(re.fullmatch(r"[\s.]*", re.search(re.escape(e) + r"([^\n]*)", txt).group(1)
                         .replace("DNI", "").replace(":", "")) is not None
            for e in ("Apellidos y nombres del juez validador:", "Especialidad del validador:")))
    # 4. Notas 1-3 y suficiencia.
    faltan_n = [n for n in (NOTA_1, NOTA_2, NOTA_3) if fany._normalizar(n) not in fany._normalizar(txt)]
    chk("Notas 1, 2 y 3 literales (Claridad corregida)", not faltan_n, str(faltan_n))
    chk("Nota de suficiencia presente", "cubren de manera completa la dimensión" in txt)
    # 5. Declaracion de juicio y exclusion total de anexos del integral.
    chk("Los tres instrumentos se someten a juicio de contenido (afirmacion expresa)",
        "se someten a juicio" in txt and "de contenido" in txt)
    presentes = [m for m in MARCADORES_ANEXOS_V05 if m in txt]
    chk("Ausencia de todo anexo del integral v05 (hoja VI, panorama, matrices, fichas, "
        "cuestionario, baremos, formulas, certificados separados)", not presentes, str(presentes[:4]))
    chk("Sin reactivos PU/PE (Modalidad B)",
        not any(fany._normalizar(e) in fany._normalizar(txt) for e in ITEMS_PU + ITEMS_PE))
    # 6. Tablas: geometria y bordado general.
    ok_flo = ok_geo = ok_cs = ok_hd = ok_math = ok_bordes = True
    for t in d.tables:
        tblPr = t._tbl.tblPr
        ok_flo &= tblPr.find(qn("w:tblpPr")) is None
        w = int(tblPr.find(qn("w:tblW")).get(qn("w:w")))
        grid = sum(int(g.get(qn("w:w"))) for g in t._tbl.tblGrid.findall(qn("w:gridCol")))
        ok_geo &= (w == grid and w <= ANCHO_RETRATO)
        for tr in t._tbl.findall(qn("w:tr")):
            trPr = tr.find(qn("w:trPr"))
            ok_cs &= trPr is not None and trPr.find(qn("w:cantSplit")) is not None
        primera = t._tbl.find(qn("w:tr")).find(qn("w:trPr"))
        ok_hd &= primera is not None and primera.find(qn("w:tblHeader")) is not None
        ok_math &= len(t._tbl.xpath('.//*[local-name()="oMath"]')) == 0
        tb = tblPr.find(qn("w:tblBorders"))
        if tb is None:
            ok_bordes = False
            continue
        estados = {l: (tb.find(qn("w:" + l)).get(qn("w:val")) if tb.find(qn("w:" + l)) is not None else None)
                   for l in ("top", "left", "bottom", "right", "insideH", "insideV")}
        ok_bordes &= (estados["top"] == "single" and estados["bottom"] == "single"
                      and not any(estados[l] in ("single", "double", "thick")
                                  for l in ("left", "right", "insideV", "insideH")))
        ok_bordes &= not t._tbl.xpath(".//w:tcBorders/*[self::w:left or self::w:right or self::w:insideV]"
                                      "[@w:val='single']")
    chk("Tablas sin flotacion", ok_flo)
    chk("Ancho de tabla dentro del area util retrato (<= 8788 dxa)", ok_geo)
    chk("Todas las filas con cantSplit", ok_cs)
    chk("Primera fila de cada tabla como encabezado repetido", ok_hd)
    chk("Sin ecuaciones OMML ni formulas en celdas", ok_math)
    chk("Bordes APA 7 en todas las tablas (cero lineas verticales)", ok_bordes)
    chk("Tablas nativas (sin imagenes)",
        len(body.xpath(".//w:drawing")) == 0 and len(body.xpath(".//w:pict")) == 0)
    # 7. Tipografia.
    fuentes, tam = set(), set()
    for r in body.iter(qn("w:r")):
        rPr = r.find(qn("w:rPr"))
        if rPr is None or not _txt(r).strip():
            continue
        rf = rPr.find(qn("w:rFonts"))
        fuentes.add(rf.get(qn("w:ascii")) if rf is not None and rf.get(qn("w:ascii")) else "(heredada)")
        sz = rPr.find(qn("w:sz"))
        if sz is not None:
            tam.add(int(sz.get(qn("w:val"))) / 2)
    chk("Fuente Times New Roman exclusiva", fuentes <= FUENTES_OK, str(sorted(fuentes)))
    chk("Sin tamanos menores a 9 pt", all(x >= 9.0 for x in tam), str(sorted(tam)))
    chk("Sin sombreados ni colores distintos del negro",
        len(body.xpath(".//w:shd[@w:fill and @w:fill!='auto' and @w:fill!='FFFFFF']")) == 0 and
        all(c.get(qn("w:val")).upper() in ("000000", "AUTO") for c in body.iter(qn("w:color"))))
    # 8. Texto prohibido y marcas.
    hall = [p for p in PROHIBIDOS if re.search(p, txt)]
    chk("Sin metadatos internos, contactos ni rayas", not hall, str(hall))
    chk("Sin marcas X ni calificaciones prellenadas",
        not re.search(r"\[\s*[xX]\s*\]", txt) and "×" not in txt)
    # 9. Seccion unica en retrato institucional.
    s = d.sections[0]
    chk("Seccion unica en retrato UNAJMA (A4, margen izq 3.0 cm y 2.5 cm resto)",
        len(d.sections) == 1 and abs(s.page_width.cm - 21.0) < 0.1
        and abs(s.left_margin.cm - 3.0) < 0.05)
    return res


def verificar_pdf_compacto(pdf):
    """Paginacion del PDF compacto: 3 marcadores, 4-5 paginas, sin paginas
    vacias y un unico cierre al final."""
    import pymupdf

    def _norma(s):
        return re.sub(r"\s+", " ", s).strip().lower()

    doc = pymupdf.open(str(pdf))
    res = []
    textos = [p.get_text() for p in doc]
    inicios = []
    for t in textos:
        lineas = [l.strip() for l in t.splitlines() if l.strip()]
        if lineas and re.fullmatch(r"\d+", lineas[0]):
            lineas = lineas[1:]
        inicios.append(_norma(" ".join(lineas[:3])) if lineas else "")
    vacias = [i + 1 for i, t in enumerate(textos) if len(t.strip()) < 30]
    res.append(("Sin paginas vacias", not vacias, str(vacias)))
    for m in MARCADORES_COMPACTO:
        mn = _norma(m)
        pg = next((i for i, ini in enumerate(inicios) if ini.startswith(mn)), None)
        if pg is None:
            res.append((f"Marcador '{m}' presente", False, "no encontrado"))
            continue
        res.append((f"'{m[:48]}...' abre pagina {pg + 1}", True, inicios[pg][:60]))
    plano_objetivo = _norma("Firma del juez validador")
    firma = next((i for i, t in enumerate(textos) if plano_objetivo in _norma(t)), None)
    res.append(("Unico cierre con firma al final del documento",
                firma is not None and firma >= len(textos) - 3,
                f"firma pagina {firma + 1 if firma is not None else None} de {len(textos)}"))
    res.append(("Total de paginas 4 a 5", 4 <= len(doc) <= 5, str(len(doc))))
    return res


# ============================================================ PERFIL v07
# Mandato del tesista (2026-10-19, «CONTINUA»): paquete PARA EXPERTO que
# conserva el nucleo compacto v06 (carta, instrucciones con tabla de criterios
# y UNA matriz de validez continua de 12 entradas con un unico cierre) pero
# (a) aplica REJILLA visible mediante el motor (excepcion deliberada a APA 7
#     solo para formatos de validacion y captura; las matrices resumen
#     conservan las 3 lineas APA 7),
# (b) tablas a TODO el ancho util entre margenes (8788 dxa retrato; 14000 dxa
#     apaisada), con columna N.° estrecha (350 dxa), descripcion maxima y seis
#     opciones de marca iguales,
# (c) incorpora los ANEXOS REALES de sustento: matriz de consistencia
#     compacta (apaisada, nucleo literal), matriz de operacionalizacion y los
#     tres instrumentos de recoleccion EN BLANCO (01 tiempos, 02 cotejo
#     documental, 03 satisfaccion TAM) con el modulo anexo de postest PU/PE
#     como tabla unica sin puntaje ni baremo.
# Celdas largas alineadas a la IZQUIERDA (no justificadas); TNR 12 titulos /
# 10 tablas / 9.5 notas; los reactivos AP/UP permanecen como afirmaciones
# literales (no se convierten en preguntas); los formularios 01/02 son campos
# de captura objetiva (no escalas de percepcion). Objetivo 10-12 paginas
# (maximo 14). Fuente durable: soportes_esenciales_v07.json del
# especialista-instrumentos; la tabla VD continua reutiliza el JSON v06.

VERSION_V07 = "v07"
RUTA_JSON_V07 = RUTA_SALIDA / "soportes_esenciales_v07.json"
DIR_V07 = RUTA_SALIDA / "para_experto_v07"
TITULO_INSTRUCCIONES_V07 = TITULO_INSTRUCCIONES_COMPACTO
TITULO_MATRIZ_VALIDEZ_V07 = TITULO_INSTRUMENTO_VALIDACION
ROTULO_MODALIDAD_B_V07 = ("Módulo anexo de postest: aceptación tecnológica del sistema (solo postest, "
                          "tras su uso). No constituye medición de la Variable Independiente ni se suma a la "
                          "escala de satisfacción.")

ANCHOS_CERT_V07 = [450, 3798, 620, 620, 560, 560, 520, 520, 1140]       # suma 8788
ANCHOS_TAREA_V07 = [350, 850, 5200, 1500, 1500, 1400, 1500, 1700]       # suma 14000
ANCHOS_RSD_V07 = [600, 4550, 1500, 1200, 1900, 4250]                    # suma 14000
ANCHOS_CPE_V07 = [600, 2250, 1700, 1400, 1400, 1200, 2200, 1300, 1950]  # suma 14000
ANCHOS_LIKERT_V07 = [900, 5088, 560, 560, 560, 560, 560]                # suma 8788
ANCHOS_ESCALA_V07 = [1300, 2900, 4588]                                  # suma 8788
assert sum(ANCHOS_CERT_V07) == ANCHO_RETRATO
assert sum(ANCHOS_TAREA_V07) == ANCHO_APAISADA
assert sum(ANCHOS_RSD_V07) == ANCHO_APAISADA
assert sum(ANCHOS_CPE_V07) == ANCHO_APAISADA
assert sum(ANCHOS_LIKERT_V07) == ANCHO_RETRATO
assert sum(ANCHOS_ESCALA_V07) == ANCHO_RETRATO

MARCADORES_V07 = [
    "Andahuaylas, ",
    TITULO_INSTRUCCIONES_V07,
    TITULO_MATRIZ_VALIDEZ_V07,
    "MATRIZ DE CONSISTENCIA",
    "MATRIZ DE OPERACIONALIZACIÓN DE VARIABLES",
    "INSTRUMENTO N.° 01",
    "INSTRUMENTO N.° 02",
    "INSTRUMENTO N.° 03",
]

# Filas representativas de las matrices de auditoria (formulario en blanco;
# el corpus real es de 40 a 60 registros por ventana y continua en hoja
# adicional, segun la especificacion del especialista).
MUESTRA_RSD_V07 = VACUNAS_RSD[:6]
MUESTRA_CPE_V07 = VACUNAS_CPE[:6]

# Tokens de verificacion derivados del JSON durable soportes_esenciales_v07
# (campos no omisibles por instrumento).
TOKENS_SOPORTES_V07 = {
    "01": ["TRAB-01 a TRAB-14", "minutos decimales", "centésimas de segundo", "tiempo neto efectivo",
           "queda grabado", "solicitud de pedido", "REG-01", "REG-03", "VALE-01", "VALE-03",
           "Promedio de las tres tareas", "Mediana"],
    "02": CRITERIOS_RSD + ["40 a 60", "30 días calendario", "Vale N.°", "N/A", "causa raíz"],
    "03": ITEMS_AP + ITEMS_UP + ITEMS_PU + ITEMS_PE +
          ["Totalmente en Desacuerdo", "Totalmente de Acuerdo", "29733", "TRAB-01 a TRAB-14"],
}


def _v07_rejilla(t):
    """Convierte una tabla recien creada a rejilla cerrada (motor) y renormaliza."""
    quir.aplicar_bordes_rejilla(t)
    quir.normalizar_orden_tblPr(t)
    return t


def v07_tabla_rejilla(doc, encabezado, filas, anchos, total, alto_min=None, alinear=None, size=TAM_TABLA,
                      margen=(40, 80, 40, 80), after=None):
    """Tabla nativa de formulario de captura con rejilla cerrada (excepcion
    deliberada a APA 7 solo para formatos de validacion y recoleccion)."""
    t = tabla(doc, encabezado, filas, anchos, total, alto_min=alto_min, alinear=alinear, size=size,
              margen=margen)
    if after is not None:
        # Normaliza el espaciado posterior al bloque tabular (ultima fila).
        for p in t.rows[-1].cells[0].paragraphs:
            p.paragraph_format.space_after = Pt(after)
    return _v07_rejilla(t)


LEYENDA_LIKERT_V07 = ("Escala de respuesta: 1 = Totalmente en Desacuerdo, 2 = En Desacuerdo, "
                      "3 = Ni de Acuerdo ni en Desacuerdo, 4 = De Acuerdo, 5 = Totalmente de Acuerdo.")


def v07_tabla_likert(doc, grupos_likert):
    """Tabla Likert unica de 7 columnas (opciones numericas 1-5 con leyenda
    previa) con filas de agrupacion fusionadas a lo ancho y rejilla cerrada.
    `grupos_likert` = [(etiqueta, codigos, items)]."""
    filas = []
    indices_grupo = []
    for etiqueta, codigos, items in grupos_likert:
        indices_grupo.append(1 + len(filas))  # +1 por la fila de encabezado
        filas.append([etiqueta, "", "", "", "", "", ""])
        for c, i in zip(codigos, items):
            filas.append([c, i, "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"])
    t = tabla(doc, ["N.°", "Reactivo", "1", "2", "3", "4", "5"],
              filas, ANCHOS_LIKERT_V07, ANCHO_RETRATO,
              alinear=["center", "left", "center", "center", "center", "center", "center"])
    for fg in indices_grupo:
        fusionar_fila(t, fg, filas[fg - 1][0], ANCHO_RETRATO, size=TAM_TABLA)
    return _v07_rejilla(t)


# ------------------------------------------------------------------ 1. carta


def v07_carta(doc):
    par(doc, f"Andahuaylas, ........ de ........................ de {ANIO}", align="right", after=2)
    par(doc, "Señor(a): ...........................................................", after=0)
    par(doc, "Docente de la Escuela Profesional de Ingeniería de Sistemas", italic=True, after=4)
    par(doc, "De mi mayor consideración:", after=4)
    par(doc, f"Yo, {TESISTA}, tesista de la Escuela Profesional de Ingeniería de Sistemas de la Universidad "
             "Nacional José María Arguedas, me dirijo a usted para solicitarle su colaboración como juez experto "
             "en la validación de contenido de los instrumentos que miden la variable dependiente de mi "
             f"investigación, intitulada “{TITULO_TESIS}”. Los tres instrumentos del estudio se someten a juicio "
             "de contenido mediante una matriz de validez única que integra las tres dimensiones con numeración "
             "continua; revisarlos no equivale a contestar datos ni preguntas de percepción.",
        align="both", first=1.27)
    par(doc, "Adjunto los siguientes documentos:", before=2, after=0, keep_next=True)
    adjuntos = [
        "Instrucciones para la validación del instrumento.",
        "Matriz de validez de contenido de los instrumentos que miden la variable dependiente: gestión de "
        "movimientos de vacunas (una sola tabla continua con las tres dimensiones, numeración continua de 1 a 12 "
        "y un único bloque de cierre).",
        "Matrices de consistencia y de operacionalización de variables, como sustento de la revisión (no se "
        "llenan).",
        "Instrumentos de recolección en blanco: Ficha N.° 01 de tiempos cronometrados, Ficha N.° 02 de cotejo "
        "documental y Cuestionario N.° 03 de satisfacción, con su módulo anexo de postest.",
    ]
    for i, adj in enumerate(adjuntos, start=1):
        par(doc, f"{i}.  {adj}", hanging=1.27, after=2, align="both")
    par(doc, "Agradezco anticipadamente su atención a la presente.", before=2, first=1.27, after=4)
    par(doc, "Atentamente,", align="center", after=10)
    par(doc, "..........................................................", align="center", line=1.0)
    par(doc, TESISTA, align="center", bold=True, line=1.0)
    par(doc, "Tesista", align="center", line=1.0)


# ----------------------------------------------------------- 2. instrucciones


def v07_instrucciones(doc):
    par(doc, TITULO_INSTRUCCIONES_V07, bold=True, align="center", pbb=True, after=6)
    par(doc, "Las instrucciones para la validación del instrumento son las siguientes:", after=3)
    par(doc, "1.  En la matriz de validez de contenido, marque con una equis (X) la opción Sí o No de los tres "
             "criterios siguientes, por cada elemento o reactivo, y anote sus observaciones en la columna "
             "Sugerencias:", align="both", hanging=1.0, after=3)
    v07_tabla_rejilla(doc, ["Criterio", "Descripción"], [
        ["Pertinencia", "El ítem corresponde al concepto teórico formulado."],
        ["Relevancia", "El ítem es apropiado para representar al componente o dimensión específica del constructo."],
        ["Claridad", "El enunciado se entiende sin dificultad; es conciso, exacto y directo."],
    ], [1900, ANCHO_RETRATO - 1900], ANCHO_RETRATO)
    separador(doc)
    par(doc, "2.  Evalúe los elementos e ítems presentados, consultando las matrices de consistencia y de "
             "operacionalización y los instrumentos de recolección adjuntos; estos sustentos no se llenan.",
        align="both", hanging=1.0, after=3)
    par(doc, "3.  La numeración es continua de 1 a 12 en una sola tabla que continúa en la página siguiente; al "
             "final complete un único bloque de cierre con sus observaciones, su opinión de aplicabilidad, sus "
             "datos y su firma.", align="both", hanging=1.0, after=3)
    par(doc, "4.  Los reactivos del cuestionario se presentan como afirmaciones graduables; devuelva la matriz "
             "completa al investigador. Agradecemos profundamente su colaboración.",
        align="both", hanging=1.0, after=0)


# ------------------------------------------------- 3. matriz de validez VD


def v07_tabla_cert(doc, grupos):
    """UNA sola tabla continua de 9 columnas a 8788 dxa con rejilla cerrada:
    N.° 450 dxa, descripcion 3798 dxa, Pertinencia 2x620, Relevancia 2x560,
    Claridad 2x520 y Sugerencias 1140 dxa (titulos enteros en una linea);
    encabezado de 2 filas, 3 filas de dimension con Si/No repetido y 12 filas
    con numeracion corrida 1..12; celdas largas alineadas a la izquierda."""
    anchos = ANCHOS_CERT_V07
    n_elem = sum(len(filas) for _, filas in grupos)
    t = doc.add_table(rows=2 + len(grupos) + n_elem, cols=9)
    quir.configurar_geometria_tabla(t, ANCHO_RETRATO, anchos, align="center",
                                    cell_margin_dxa=(20, 45, 20, 45))
    quir.aplicar_bordes_rejilla(t)
    fany.fijar_disposicion_fija(t)
    for c in (0, 1, 8):
        celda = t.cell(0, c).merge(t.cell(1, c))
        celda.width = Cm(anchos[c] / 567.0)
    for c in (2, 4, 6):
        celda = t.cell(0, c).merge(t.cell(0, c + 1))
        celda.width = Cm((anchos[c] + anchos[c + 1]) / 567.0)
    fany.texto_celda(t.cell(0, 0), "N.°", tamano=fany.TAM_ENCABEZADO, negrita=True)
    fany.texto_celda(t.cell(0, 1), "DIMENSIONES / ÍTEMS (ELEMENTOS)", tamano=fany.TAM_ENCABEZADO, negrita=True)
    fany.texto_celda_con_superindice(t.cell(0, 2), "Pertinencia", "1", tamano=fany.TAM_ENCABEZADO)
    fany.texto_celda_con_superindice(t.cell(0, 4), "Relevancia", "2", tamano=fany.TAM_ENCABEZADO)
    fany.texto_celda_con_superindice(t.cell(0, 6), "Claridad", "3", tamano=fany.TAM_ENCABEZADO)
    fany.texto_celda(t.cell(0, 8), "Sugerencias", tamano=fany.TAM_ENCABEZADO, negrita=True)
    for c, etiqueta in ETIQUETAS_CERT.items():
        fany.texto_celda(t.cell(1, c), etiqueta, tamano=fany.TAM_ENCABEZADO, negrita=True)
    fila = 2
    for etiqueta_dim, elementos in grupos:
        celda_g = t.cell(fila, 0).merge(t.cell(fila, 1))
        celda_g.width = Cm((anchos[0] + anchos[1]) / 567.0)
        fany.texto_celda(celda_g, etiqueta_dim, tamano=fany.TAM_DIMENSION, negrita=True,
                         alineacion="left", before=15, after=15, margen_izq_dxa=50)
        for c, etiqueta in ETIQUETAS_CERT.items():
            fany.texto_celda(t.cell(fila, c), etiqueta, tamano=fany.TAM_ENCABEZADO, negrita=True)
        fany.fijar_contenido_celda(t.cell(fila, 8), fany._p_vacio())
        fila += 1
        for num, texto in elementos:
            fany.texto_celda(t.cell(fila, 0), str(num), tamano=10.0, alineacion="center")
            fany.texto_celda(t.cell(fila, 1), texto, tamano=fany.TAM_ITEM, alineacion="left",
                             before=10, after=10, margen_izq_dxa=50)
            for c in fany.COLS_CRITERIO:
                fany.fijar_contenido_celda(t.cell(fila, c), fany._p_vacio())
            fany.fijar_contenido_celda(t.cell(fila, 8), fany._p_vacio())
            fila += 1
    fany.normalizar_celdas_sin_parrafo(t)
    for row in t.rows:
        for cell in row.cells:
            cell.vertical_alignment = fany.WD_ALIGN_VERTICAL.CENTER
    quir.blindar_filas_tabla(t, cant_split=True, repetir_encabezado=True, filas_encabezado=2)
    quir.normalizar_orden_tblPr(t)
    return t


def v07_certificado(doc):
    fany.TAM_ITEM, fany.TAM_CODIGO, fany.TAM_ENCABEZADO = 10.0, 10.0, 10.0
    fany.TAM_DIMENSION, fany.TAM_BLOQUE = 10.0, 10.0
    espec = _cargar_compacto()
    par(doc, TITULO_MATRIZ_VALIDEZ_V07, bold=True, align="center", pbb=True, after=2)
    par(doc, espec["spec"]["titulo"], bold=True, align="center", size=12, line=1.2, after=2)
    par(doc, espec["spec"]["nota_unica"], align="center", size=10, after=5)
    v07_tabla_cert(doc, espec["grupos"])
    construir_bloque_cierre(doc)
    construir_notas_pie(doc, tamano=9.5)


# ------------------------------------------------- 4/5. matrices de sustento
# La matriz de consistencia se presenta en versión COMPACTA (mandato v07):
# UNA sola tabla apaisada con el núcleo literal (problema/objetivos/hipótesis
# general + 3 específicos, VI dicotómica X0/X1, VD con 3 dimensiones y 6
# indicadores) y la metodología extensa UNA sola vez como nota bajo la tabla
# (sin estadística desarrollada). La operacionalización reutiliza la pieza
# literal del perfil integral. Ambas conservan el bordado APA 7 (las matrices
# resumen no llevan rejilla).

ENCABEZADOS_MC_V07 = ["Problemas", "Objetivos", "Hipótesis", "Variable / dimensiones", "Indicadores"]
ANCHOS_MC_V07 = [2300, 2300, 2300, 3550, 3550]  # suma 14000

NOTA_METODOLOGIA_V07 = (
    "Nota. Metodología: investigación aplicada, enfoque cuantitativo, nivel explicativo; diseño preexperimental "
    "con pretest y postest en un solo grupo (O1, X, O2); población y muestra censal, N = n = 14 trabajadores; "
    "técnicas e instrumentos: observación sistemática (Ficha N.° 01), cotejo documental (Ficha N.° 02) y "
    "encuesta (Cuestionario N.° 03); validez de contenido por juicio de expertos y confiabilidad estimada con "
    "los datos del estudio; plan estadístico: estadística descriptiva, prueba de Shapiro-Wilk y prueba de "
    "Wilcoxon para muestras relacionadas (p < 0.05).")


def _filas_mc_v07():
    """Filas literales de la matriz de consistencia v07 (fuente unica compartida
    con el perfil vertical v08, que solo las redistribuye en bloques)."""
    d1, d2, d3 = _mc("oportunidad de procesamiento"), _mc("consistencia documental"), _mc("satisfacción del usuario")
    return [
        ["Problema general:\n" + MC_PG,
         "Objetivo general:\nDeterminar en qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de "
         f"movimientos mensuales de vacunas {SUJ}, Andahuaylas 2025.",
         "Hipótesis general:\nLa aplicación del sistema \"SIVAC\" mejora significativamente la gestión de "
         f"movimientos mensuales de vacunas {SUJ}, Andahuaylas 2025.\nSe acepta si se rechaza la hipótesis nula en las "
         "tres hipótesis específicas (p < 0.05).",
         "Variable independiente:\nSistema web SIVAC.\nCondición X0 (pretest): ausencia del sistema; gestión "
         "manual tradicional.\nCondición X1 (postest): presencia y uso del sistema SIVAC.",
         "Escala: dicotómica nominal (0 = pretest, 1 = postest).\nSustento técnico: metodología Extreme "
         "Programming y calidad ISO/IEC 25010:2023."],
        ["Problema específico 1:\n" + d1[0], "Objetivo específico 1:\n" + d1[1],
         "Hipótesis específica 1:\n" + d1[2],
         "Variable dependiente:\nGestión de movimientos mensuales de vacunas.\nDimensión 1: oportunidad de procesamiento.",
         "• Tiempo de registro de movimientos (Treg), en minutos decimales, escala de razón.\n"
         "• Tiempo de emisión de vales (Tvale), en minutos decimales, escala de razón.\nInstrumento: Ficha N.° 01."],
        ["Problema específico 2:\n" + d2[0], "Objetivo específico 2:\n" + d2[1],
         "Hipótesis específica 2:\n" + d2[2],
         "Dimensión 2: consistencia documental.",
         "• Registros sin discrepancias (RSD), en porcentaje, escala de razón.\n"
         "• Concordancia entre cantidad programada y entregada (CPE), en porcentaje acotado entre 0 y 100.\n"
         "Instrumento: Ficha N.° 02."],
        ["Problema específico 3:\n" + d3[0], "Objetivo específico 3:\n" + d3[1],
         "Hipótesis específica 3:\n" + d3[2],
         "Dimensión 3: satisfacción del usuario (satisfacción con el proceso).",
         "• Aceptación del proceso operativo (AP), 4 ítems, 4 a 20 puntos.\n"
         "• Utilidad percibida (UP), 4 ítems, 4 a 20 puntos.\nTotal: 8 ítems, 8 a 40 puntos, escala Likert de 1 a 5.\n"
         "Instrumento: Cuestionario N.° 03, Modalidad A."],
    ]


def v07_matriz_consistencia(doc):
    nueva_seccion(doc, "apaisada")
    par(doc, "MATRIZ DE CONSISTENCIA", bold=True, align="center", after=2, pbb=True)
    par(doc, TITULO_TESIS, italic=True, align="center", size=TAM_TABLA, line=1.0, after=6)
    filas = _filas_mc_v07()
    tabla(doc, ENCABEZADOS_MC_V07, filas, ANCHOS_MC_V07, ANCHO_APAISADA)
    par(doc, NOTA_METODOLOGIA_V07, size=9.5, line=1.0, before=4, italic=True, align="both")


# --------------------------------------------------- 6. instrumento 01 blanco


def v07_ficha01(doc):
    par(doc, "INSTRUMENTO N.° 01", bold=True, align="center", after=0, pbb=True)
    par(doc, "FICHA DE OBSERVACIÓN SISTEMÁTICA Y MEDICIÓN DE TIEMPOS CRONOMETRADOS",
        bold=True, align="center", after=3)
    par(doc, "Dimensión: oportunidad de procesamiento. Indicadores: tiempo de registro (Treg) y tiempo de emisión "
             "de vale (Tvale). Formulario en blanco para captura objetiva de campo; no se llena durante la "
             "validación y sus campos no constituyen escalas de percepción.", align="both", size=10, after=4)
    par(doc, "1. Datos generales de la observación", bold=True, before=4, after=2, keep_next=True)
    v07_tabla_rejilla(doc, ["Campo", "Registro"], [
        ["Código del operador evaluado", "TRAB-____  (TRAB-01 a TRAB-14)"],
        ["Rol institucional", "[  ] Responsable de centro de acopio o red de frío   [  ] Personal de estrategia "
                              "sanitaria de inmunizaciones"],
        ["Centro de acopio o sede / red o microred", "____________________________     Provincia:   "
                                                     "[  ] Andahuaylas   [  ] Chincheros"],
        ["Momento de medición", "[  ] Pretest (kardex físico, libros de registro y hojas de cálculo)   "
                                "[  ] Postest (sistema web SIVAC)"],
        ["Fecha de la observación", "______ / ______ / ______"],
        ["Evaluador principal", TESISTA + "     Secundario (si aplica): ______________________"],
    ], [3800, ANCHO_APAISADA - 3800], ANCHO_APAISADA)
    par(doc, "2. Protocolo de cronometraje y reglas de registro", bold=True, before=4, after=1, keep_next=True)
    for s in [
        "Cronómetro digital con precisión de centésimas de segundo; cada tiempo se consigna en minutos "
        "decimales (minutos enteros más la fracción de segundos sobre sesenta).",
        "Tiempo de registro: inicia al tomar el documento fuente o abrir la digitación y termina cuando el "
        "movimiento queda grabado o asentado con saldo actualizado.",
        "Tiempo de emisión de vales: inicia al recibir o abrir la solicitud de pedido y termina cuando el "
        "comprobante queda generado, firmado o impreso.",
        "Regla de pausa: ante una interrupción externa fortuita el cronómetro se detiene y se reanuda al "
        "normalizarse la tarea; se registra solo el tiempo neto efectivo. La batería consta de tres tareas "
        "de registro y tres de emisión por operador; el promedio o la mediana consolidan su tiempo.",
    ]:
        par(doc, "•  " + s, align="left", hanging=0.8, after=1)
    par(doc, "3. Sección A: tareas de registro (Treg)", bold=True, before=4, after=1, keep_next=True)
    v07_tabla_rejilla(doc, ["N.°", "Código", "Tarea estandarizada", "Hora de inicio", "Hora de fin",
                            "Tiempo neto (min:s)", "Tiempo (min decimales)", "Incidencias"], [
        ["1", "REG-01", "Ingreso simple de remesa (1 biológico)"] + [""] * 5,
        ["2", "REG-02", "Salida regular programada (2 a 3 vacunas)"] + [""] * 5,
        ["3", "REG-03", "Redistribución o despacho complejo (4 a 6 ítems)"] + [""] * 5,
    ], ANCHOS_TAREA_V07, ANCHO_APAISADA, alto_min=480,
        alinear=["center", "center", "left", "center", "center", "center", "center", "left"])
    par(doc, "Promedio de las tres tareas: ____________ min          Mediana: ____________ min",
        before=3, after=1)
    par(doc, "4. Sección B: tareas de emisión de vales (Tvale)", bold=True, before=4, after=1, keep_next=True)
    v07_tabla_rejilla(doc, ["N.°", "Código", "Tarea estandarizada", "Hora de inicio", "Hora de fin",
                            "Tiempo neto (min:s)", "Tiempo (min decimales)", "Incidencias"], [
        ["1", "VALE-01", "Vale simple (puesto I-1 o I-2; 1 a 2 biológicos)\nVale N.°: ________"] + [""] * 5,
        ["2", "VALE-02", "Vale regular (centro I-3 o I-4; 3 a 5 biológicos)\nVale N.°: ________"] + [""] * 5,
        ["3", "VALE-03", "Vale de emergencia por contingencia de cadena de frío\nVale N.°: ________"] + [""] * 5,
    ], ANCHOS_TAREA_V07, ANCHO_APAISADA, alto_min=480,
        alinear=["center", "center", "left", "center", "center", "center", "center", "left"])
    par(doc, "Promedio de las tres tareas: ____________ min          Mediana: ____________ min",
        before=3, after=1)
    par(doc, "5. Declaración y firma", bold=True, before=4, after=1, keep_next=True)
    par(doc, "Declaración: la presente toma de tiempos respetó los puntos de inicio y fin del protocolo y la "
             "regla de pausa, con veracidad de los datos registrados.     Firma del evaluador: "
             "______________________________     " + TESISTA + ", Tesista", align="left", after=0)


# --------------------------------------------------- 7. instrumento 02 blanco


def v07_ficha02(doc):
    par(doc, "INSTRUMENTO N.° 02", bold=True, align="center", after=0, pbb=True)
    par(doc, "FICHA DE REGISTRO Y COTEJO DOCUMENTAL DE CONSISTENCIA", bold=True, align="center", after=2)
    par(doc, "Dimensión: consistencia documental. Indicadores: registros sin discrepancias (RSD) y concordancia "
             "entre cantidad programada y entregada (CPE). Formulario en blanco para auditoría documental; no se "
             "llena durante la validación.", align="both", size=10, after=2)
    par(doc, "1. Datos generales de la auditoría documental", bold=True, before=4, after=2, keep_next=True)
    v07_tabla_rejilla(doc, ["Campo", "Registro"], [
        ["Código del operador o centro auditado", "TRAB-____  (TRAB-01 a TRAB-14)"],
        ["Centro de acopio provincial o microred", "____________________________     Provincia:   "
                                                   "[  ] Andahuaylas   [  ] Chincheros"],
        ["Momento de medición", "[  ] Pretest (kardex manual, cuadernos y hojas de cálculo)   [  ] Postest "
                                "(base de datos y vales electrónicos de SIVAC)"],
        ["Ventana de auditoría", "Del ____ / ____ / ______  al  ____ / ____ / ______  (30 días calendario)"],
        ["Fecha de ejecución de la auditoría", "______ / ______ / ______"],
        ["Auditor principal", TESISTA + "     Secundario (si aplica): ______________________"],
    ], [3800, ANCHO_APAISADA - 3800], ANCHO_APAISADA)
    par(doc, "2. Regla de conformidad y los ocho criterios (RSD)", bold=True, before=4, after=1, keep_next=True)
    par(doc, "Un registro es conforme (1) cuando cumple simultáneamente los ocho criterios siguientes; si "
             "incumple al menos uno, es no conforme (0). Se audita un corpus de 40 a 60 registros por ventana.",
        align="left", size=10, after=1)
    criterios = "  ".join(f"({i}) {c}" for i, c in enumerate(CRITERIOS_RSD, start=1))
    par(doc, criterios, align="both", size=10, line=1.0, after=1)
    par(doc, "3. Matriz de auditoría de registros (RSD)", bold=True, before=4, after=1, keep_next=True)
    filas_rsd = [[f"{i:02d}", v, "", "", "[  ] 1   [  ] 0", ""] for i, v in enumerate(MUESTRA_RSD_V07, 1)]
    filas_rsd.append(["...", "Continúa según el corpus real (40 a 60 registros por ventana)", "", "",
                      "[  ] 1   [  ] 0", ""])
    v07_tabla_rejilla(doc, ["N.°", "Vacuna o insumo auditado", "Lote", "Cantidad",
                            "Veredicto (1 = conforme, 0 = no conforme)", "Tipo de discrepancia o causa raíz"],
                      filas_rsd, ANCHOS_RSD_V07, ANCHO_APAISADA,
                      alinear=["center", "left", "left", "center", "center", "left"])
    par(doc, "Nota: si el corpus supera las filas disponibles, continúe en una hoja adicional con el mismo "
             "formato.", size=9.5, line=1.0, before=3, italic=True)
    par(doc, "Total de registros evaluados: ______      Registros conformes: ______      "
             "Registros con discrepancia: ______      RSD: ______ %", before=2, after=0)
    par(doc, "4. Regla de concordancia y matriz de entregas (CPE)", bold=True, before=4, after=1,
        keep_next=True)
    par(doc, "Una entrega es concordante (1) si la cantidad entregada es idéntica a la programada o si, siendo "
             "distinta, existe un documento sustentatorio oficial archivado que autoriza expresamente la "
             "variación; en cualquier otro caso es no concordante (0). Se auditan de 40 a 60 entregas por "
             "ventana. Consolidado: Total de entregas auditadas ______, concordantes ______, no concordantes "
             "______, CPE ______ %.", align="left", size=10, after=2)
    filas_cpe = [[f"{i:02d}", v, "Vale N.°:", "", "", "", "[  ] Sí [  ] No [  ] N/A", "[  ] 1  [  ] 0", ""]
                 for i, v in enumerate(MUESTRA_CPE_V07, 1)]
    filas_cpe.append(["...", "Continúa en hoja adicional", "", "", "", "",
                      "", "", ""])
    v07_tabla_rejilla(doc, ["N.°", "Vacuna o biológico", "N.° de documento", "Cantidad programada",
                            "Cantidad entregada", "Diferencia", "Justificación formal acreditada",
                            "Veredicto (1 = concordante, 0 = no concordante)", "Causa raíz del desfase"],
                      filas_cpe, ANCHOS_CPE_V07, ANCHO_APAISADA, margen=(20, 40, 20, 40),
                      alinear=["center", "left", "left", "center", "center", "center", "center", "center",
                               "left"], after=0)


# --------------------------------------------------- 8. instrumento 03 blanco


def v07_cuestionario(doc, seccion=True):
    if seccion:
        nueva_seccion(doc, "unajma")
    par(doc, "INSTRUMENTO N.° 03", bold=True, align="center", after=0, pbb=True)
    par(doc, "CUESTIONARIO DE SATISFACCIÓN DEL USUARIO Y ACEPTACIÓN TECNOLÓGICA (MODELO TAM)",
        bold=True, align="center", after=3)
    par(doc, "Variable evaluada: gestión de movimientos mensuales de vacunas (variable dependiente). Dimensión: "
             "satisfacción del usuario. Población objetivo: personal de la cadena de frío e inmunizaciones de la "
             "DISA Apurímac II (N = n = 14). Formulario en blanco; no se llena durante la validación.",
        align="both", size=10, after=4)
    par(doc, "1. Instrucciones para el participante y escala de respuesta (Likert de 5 opciones)", bold=True,
        before=4, after=2, keep_next=True)
    par(doc, "•  Confidencialidad y anonimato bajo código numérico (TRAB-01 a TRAB-14), conforme a la Ley "
             "N.° 29733 de Protección de Datos Personales y el Código de Ética en Investigación de la UNAJMA.",
        align="left", hanging=0.8, after=1)
    par(doc, "•  Libertad de respuesta: no existen respuestas correctas ni incorrectas; marque con una equis (X) "
             "una sola alternativa por reactivo; las proposiciones son afirmaciones que se gradúan, no preguntas.",
        align="left", hanging=0.8, after=3)
    v07_tabla_rejilla(doc, ["Puntuación", "Escala verbal", "Significado operativo"], ESCALA_LIKERT,
                      ANCHOS_ESCALA_V07, ANCHO_RETRATO, alinear=["center", "left", "left"])
    par(doc, "Momento de aplicación (marque el evaluador):    [  ] Pretest (proceso manual)    "
             "[  ] Postest (proceso con el sistema web SIVAC).", before=5, after=2)
    par(doc, "2. Datos generales del participante", bold=True, before=4, after=1, keep_next=True)
    v07_tabla_rejilla(doc, ["Campo", "Registro"], [
        ["Código de participante asignado", "TRAB-____  (TRAB-01 a TRAB-14)"],
        ["Centro de acopio / red / microred", ""],
        ["Provincia de desempeño", "[  ] Andahuaylas   [  ] Chincheros"],
        ["Condición laboral actual", "[  ] Nombrado D.L. 276   [  ] Contratado CAS (D.L. 1057)   "
                                     "[  ] Locación / otro"],
        ["Profesión / cargo operativo", "[  ] Lic. en Enfermería   [  ] Técnico(a) en Enfermería   "
                                        "[  ] Estadístico / soporte"],
        ["Tiempo de experiencia en red de frío", "[  ] Menos de 2 años   [  ] 2 a 5 años   [  ] 6 a 10 años   "
                                                 "[  ] Más de 10 años"],
        ["Fecha de aplicación", "______ / ______ / ______"],
    ], [3800, ANCHO_RETRATO - 3800], ANCHO_RETRATO)
    par(doc, "3. Modalidad A: satisfacción con el proceso operativo (AP y UP)", bold=True, before=6, after=1,
        keep_next=True)
    par(doc, "Ocho afirmaciones literales sobre la gestión del proceso; en el pretest el participante evalúa el "
             "proceso manual y en el postest el proceso mediado por el sistema. " + LEYENDA_LIKERT_V07,
        align="left", size=10, after=1)
    v07_tabla_likert(doc, [
        ("Indicador: Aceptación del proceso operativo (AP)", ["AP-01", "AP-02", "AP-03", "AP-04"], ITEMS_AP),
        ("Indicador: Utilidad percibida para la gestión sanitaria (UP)", ["UP-01", "UP-02", "UP-03", "UP-04"],
         ITEMS_UP),
    ])
    par(doc, "Firma del participante: ______________________________", before=8, after=2)
    par(doc, "Firma del encuestador (Bach. José Luis Quispe León, Tesista): ______________________________",
        after=0)
    par(doc, "4. Modalidad B: módulo anexo de postest", bold=True, before=6, after=1, pbb=True, keep_next=True)
    par(doc, "Código de participante (TRAB): TRAB-______     Fecha de aplicación postest: ____ / ____ / ______",
        before=2, after=2)
    par(doc, ROTULO_MODALIDAD_B_V07 + " " + LEYENDA_LIKERT_V07, align="both", size=10, italic=True, bold=True,
        after=3)
    v07_tabla_likert(doc, [
        ("Utilidad percibida del software (PU)", ["PU-01", "PU-02", "PU-03", "PU-04"], ITEMS_PU),
        ("Facilidad de uso percibida del software (PE)", ["PE-01", "PE-02", "PE-03", "PE-04"], ITEMS_PE),
    ])
    par(doc, "Firma del participante: ______________________________", before=8, after=2)
    par(doc, "Firma del encuestador (Bach. José Luis Quispe León, Tesista): ______________________________",
        after=0)


# ----------------------------------------------------------------- ensamblado v07


def construir_v07():
    doc = docx.Document()
    configurar_normal(doc)
    aplicar_geometria(doc.sections[0], "unajma")
    pie_pagina(doc.sections[0])
    cp = doc.core_properties
    cp.author, cp.title, cp.last_modified_by = TESISTA, "Expediente de validación para experto (v07)", TESISTA
    cp.comments, cp.subject, cp.keywords = "", "", ""
    v07_carta(doc)
    v07_instrucciones(doc)
    v07_certificado(doc)
    v07_matriz_consistencia(doc)
    pieza_operacionalizacion(doc)
    v07_ficha01(doc)
    v07_ficha02(doc)
    v07_cuestionario(doc)
    return doc


def nombre_v07(n):
    return f"EXPEDIENTE_VALIDACION_SIVAC_PARA_EXPERTO_0{n}_{VERSION_V07}.docx"


def _cargar_soportes_v07():
    import json
    return json.loads(RUTA_JSON_V07.read_text(encoding="utf-8"))


def verificar_v07(ruta):
    """Audita el DOCX v07 GUARDADO. Devuelve [(nombre, ok, detalle)]."""
    res = []

    def chk(nombre, ok, det=""):
        res.append((nombre, bool(ok), det))

    espec = _cargar_compacto()
    soportes = _cargar_soportes_v07()
    d = docx.Document(str(ruta))
    body = d.element.body
    txt = "\n".join(t.text or "" for t in body.iter(qn("w:t")))
    plano = re.sub(r"\s+", " ", txt)
    nplano = fany._normalizar(txt)
    # 1. Orden de piezas (modelo ITEM ampliado con los anexos reales).
    pars = [_txt(p) for p in body.findall(qn("w:p"))]
    pos = [next((i for i, t in enumerate(pars) if t.startswith(m)), None) for m in MARCADORES_V07]
    chk("Orden de piezas carta, instrucciones, matriz de validez, matrices, instrumentos 01/02/03",
        None not in pos and pos == sorted(pos), str(pos))
    # 2. Secciones y margenes exactos (retrato institucional + apaisada).
    geoms = []
    for s in d.sections:
        if abs(s.page_width.cm - 21.0) < 0.1 and abs(s.left_margin.cm - 3.0) < 0.05:
            geoms.append(("unajma", 3))
        elif abs(s.page_width.cm - 29.7) < 0.1 and abs(s.left_margin.cm - 2.5) < 0.05:
            geoms.append(("apaisada", 4))
        else:
            geoms.append(("otra", 0))
    chk("Secciones: retrato, apaisada y retrato con margenes exactos",
        geoms == [("unajma", 3), ("apaisada", 4), ("unajma", 3)], str(geoms))
    # 3. Tablas: ancho pleno, sin flotacion, blindaje, sin OMML y bordes por
    # clase (matrices APA 7; formularios con rejilla cerrada).
    ok_flo = ok_cs = ok_hd = ok_math = ok_ancho = ok_bordes = True
    n_rejilla = n_apa = 0
    det_bordes = []
    for t in d.tables:
        tblPr = t._tbl.tblPr
        ok_flo &= tblPr.find(qn("w:tblpPr")) is None
        w = int(tblPr.find(qn("w:tblW")).get(qn("w:w")))
        grid = sum(int(g.get(qn("w:w"))) for g in t._tbl.tblGrid.findall(qn("w:gridCol")))
        ok_ancho &= (w == grid and w in (ANCHO_RETRATO, ANCHO_APAISADA))
        for tr in t._tbl.findall(qn("w:tr")):
            trPr = tr.find(qn("w:trPr"))
            ok_cs &= trPr is not None and trPr.find(qn("w:cantSplit")) is not None
        primera_tr = t._tbl.find(qn("w:tr")).find(qn("w:trPr"))
        ok_hd &= primera_tr is not None and primera_tr.find(qn("w:tblHeader")) is not None
        ok_math &= len(t._tbl.xpath('.//*[local-name()="oMath"]')) == 0
        tb = tblPr.find(qn("w:tblBorders"))
        if tb is None:
            ok_bordes = False
            det_bordes.append("sin tblBorders")
            continue
        estados = {l: (tb.find(qn("w:" + l)).get(qn("w:val")) if tb.find(qn("w:" + l)) is not None else None)
                   for l in ("top", "left", "bottom", "right", "insideH", "insideV")}
        encabezado_tabla = _txt(t._tbl.find(qn("w:tr"))).strip()
        if encabezado_tabla.startswith("Problemas") or encabezado_tabla.startswith("Variable"):
            n_apa += 1
            ok_bordes &= (estados["top"] == "single" and estados["bottom"] == "single"
                          and not any(estados[l] in ("single", "double", "thick")
                                      for l in ("left", "right", "insideV", "insideH")))
            ok_bordes &= not t._tbl.xpath(".//w:tcBorders/*[self::w:left or self::w:right or self::w:insideV]"
                                          "[@w:val='single']")
        else:
            n_rejilla += 1
            if not all(estados[l] == "single" for l in ("top", "left", "bottom", "right", "insideH", "insideV")):
                ok_bordes = False
                det_bordes.append(str(estados))
    chk("Tablas sin flotacion", ok_flo)
    chk("Tablas a todo el ancho util (8788 retrato o 14000 apaisada) sin desbordes", ok_ancho)
    chk("Todas las filas con cantSplit", ok_cs)
    chk("Primera fila de cada tabla como encabezado repetido", ok_hd)
    chk("Sin ecuaciones OMML ni formulas en celdas", ok_math)
    chk(f"Bordes: formularios con rejilla cerrada ({n_rejilla}) y matrices con APA 7 ({n_apa})",
        ok_bordes, str(det_bordes[:3]))
    chk("Tablas nativas (sin imagenes)",
        len(body.xpath(".//w:drawing")) == 0 and len(body.xpath(".//w:pict")) == 0)
    # 4. Matriz de validez unica (heredada del nucleo v06) con numeracion 1..12.
    certs = [t for t in d.tables
             if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 9
             and int(t._tbl.tblPr.find(qn("w:tblW")).get(qn("w:w"))) == ANCHO_RETRATO]
    chk("UNA sola matriz de validez (9 columnas a 8788)", len(certs) == 1, str(len(certs)))
    if certs:
        res.extend(_auditar_tabla_compacto(certs[0], espec["grupos"]))
    chk("Titulo unico de la matriz de validez presente", espec["spec"]["titulo"] in txt)
    chk("Nota de alcance unica presente", espec["spec"]["nota_unica"] in txt)
    # 5. UN unico bloque de cierre del juez (solo al final de la matriz).
    chk("UN unico bloque de cierre del juez",
        txt.count("Firma del juez validador") == 1
        and txt.count("Apellidos y nombres del juez validador:") == 1
        and txt.count("Opinión de aplicabilidad:") == 1,
        f"firmas={txt.count('Firma del juez validador')}")
    chk("Casillas de aplicabilidad en blanco",
        all(x in txt for x in ("Aplicable [   ]", "Aplicable después de corregir [   ]", "No aplicable [   ]")))
    chk("Notas 1, 2 y 3 literales y suficiencia",
        all(fany._normalizar(n) in nplano for n in (NOTA_1, NOTA_2, NOTA_3))
        and "cubren de manera completa la dimensión" in txt)
    # 6. Carta con los 4 adjuntos reales.
    faltan_adj = [a for a in ("Matrices de consistencia", "operacionalización de variables",
                              "Instrumentos de recolección en blanco", "Ficha N.° 01", "Ficha N.° 02",
                              "Cuestionario N.° 03", "módulo anexo de postest") if a not in txt]
    chk("Carta anuncia los 4 adjuntos reales (instrucciones, matriz de validez, matrices sustento, "
        "instrumentos 01/02/03)", not faltan_adj, str(faltan_adj))
    # 7. Anexos reales presentes con su nucleo literal.
    hipotesis = [_mc("oportunidad de procesamiento")[2], _mc("consistencia documental")[2],
                 _mc("satisfacción del usuario")[2]]
    faltan_mc = [h[:30] for h in hipotesis + [MC_PG] if fany._normalizar(h) not in nplano]
    chk("Matriz de consistencia: problema general e hipotesis general y 3 especificas literales",
        not faltan_mc, str(faltan_mc))
    chk("Operacionalizacion: VI dicotomica X0/X1 y escala dicotomica nominal",
        "X0" in txt and "X1" in txt and "Dicotómica nominal" in txt)
    faltan_f01 = [k for k in TOKENS_SOPORTES_V07["01"] if fany._normalizar(k) not in nplano]
    chk("Instrumento 01: campos no omisibles del soporte (identificacion, condicion, inicio/fin, unidad, "
        "regla de pausa, 3+3 tareas, agregacion)", not faltan_f01, str(faltan_f01))
    faltan_f02 = [fany._normalizar(k) for k in TOKENS_SOPORTES_V07["02"]
                  if fany._normalizar(k) not in nplano]
    chk("Instrumento 02: 8 criterios literales, corpus 40 a 60, matrices RSD y CPE con consolidados",
        not faltan_f02, str(faltan_f02[:4]))
    norm = fany._normalizar
    faltan_f03 = [k[:30] for k in TOKENS_SOPORTES_V07["03"] if norm(k) not in nplano]
    chk("Instrumento 03: 8 AP/UP y 8 PU/PE literales, escala Likert de 5 opciones, consentimiento",
        not faltan_f03, str(faltan_f03[:4]))
    codigos_react = [f"{p}-0{i}" for p in ("AP", "UP", "PU", "PE") for i in range(1, 5)]
    chk("Codigos de fila de los 16 reactivos AP/UP y PU/PE presentes en el cuestionario",
        all(c in txt for c in codigos_react),
        str([c for c in codigos_react if c not in txt][:4]))
    chk("Escala Likert completa (1 totalmente en desacuerdo a 5 totalmente de acuerdo)",
        all(e in txt for e in ("Totalmente en Desacuerdo (TD)", "En Desacuerdo (D)",
                               "Ni de Acuerdo ni en Desacuerdo", "De Acuerdo (A)",
                               "Totalmente de Acuerdo (TA)")))
    chk("Rotulo exigido de la Modalidad B presente y literal", ROTULO_MODALIDAD_B_V07 in txt)
    chk("Modalidad B sin puntaje ni baremo (modulo descriptivo de postest)",
        "ni se suma a la escala de satisfacción" in txt)
    # 7b. Numeracion del cuestionario y firmas por modalidad (QA final).
    chk("Numeracion del cuestionario sin saltos (1, 2, 3 Modalidad A, 4 Modalidad B)",
        "1. Instrucciones para el participante" in txt and "2. Datos generales del participante" in txt
        and "3. Modalidad A: satisfacción con el proceso operativo" in txt
        and "4. Modalidad B: módulo anexo de postest" in txt
        and "5. Modalidad" not in txt and "6. Modalidad" not in txt)
    chk("Firmas del participante y encuestador al cierre de la Modalidad A y de la Modalidad B",
        txt.count("Firma del participante: ") == 2
        and txt.count("Firma del encuestador (Bach. José Luis Quispe León, Tesista):") == 2)
    chk("Modalidad B con linea de vinculacion TRAB y fecha postest en blanco",
        "TRAB-______" in txt and "Fecha de aplicación postest: ____ / ____ / ______" in txt)
    chk("Fechas de aplicacion y ventana de auditoria del formulario totalmente en blanco (dia/mes/año)",
        txt.count("______ / ______ / ______") >= 3
        and "Del ____ / ____ / ______  al  ____ / ____ / ______" in txt
        and not re.search(r"Fecha de (aplicación|la observación|ejecución)[^\n]*2025", txt)
        and not re.search(r"Ventana de auditor[^\n]*2025", txt))
    # 8. Exclusion de protocolos psicometricos y estadisticos desarrollados.
    psico = [m for m in ("Alfa de Cronbach", "Omega de McDonald", "baremo", "tercil", "piloto",
                         "puntaje global") if m.lower() in plano.lower()]
    chk("Sin baremos, alfa, omega, terciles ni piloto (formularios puros)", not psico, str(psico))
    n_omml = len(body.xpath('.//*[local-name()="oMath"]'))
    chk("Cero ecuaciones OMML en el paquete v07", n_omml == 0, str(n_omml))
    # 9. Tipografia.
    fuentes, tam = set(), set()
    for r in body.iter(qn("w:r")):
        rPr = r.find(qn("w:rPr"))
        if rPr is None or not _txt(r).strip():
            continue
        rf = rPr.find(qn("w:rFonts"))
        fuentes.add(rf.get(qn("w:ascii")) if rf is not None and rf.get(qn("w:ascii")) else "(heredada)")
        sz = rPr.find(qn("w:sz"))
        if sz is not None:
            tam.add(int(sz.get(qn("w:val"))) / 2)
    chk("Fuente Times New Roman exclusiva", fuentes <= FUENTES_OK, str(sorted(fuentes)))
    chk("Sin tamanos menores a 9 pt", all(x >= 9.0 for x in tam), str(sorted(tam)))
    chk("Sin sombreados ni colores distintos del negro",
        len(body.xpath(".//w:shd[@w:fill and @w:fill!='auto' and @w:fill!='FFFFFF']")) == 0 and
        all(c.get(qn("w:val")).upper() in ("000000", "AUTO") for c in body.iter(qn("w:color"))))
    # 10. Texto prohibido y marcas.
    hall = [p for p in PROHIBIDOS if re.search(p, txt)]
    chk("Sin metadatos internos, contactos ni rayas", not hall, str(hall))
    chk("Sin marcas X ni calificaciones prellenadas",
        not re.search(r"\[\s*[xX]\s*\]", txt) and "×" not in txt)
    return res


def verificar_pdf_v07(pdf):
    """Paginacion del PDF v07: 8 marcadores abren pagina, sin paginas vacias,
    objetivo de 10 a 12 paginas (maximo 14) y cierre unico del juez."""
    import pymupdf

    def _norma(s):
        return re.sub(r"\s+", " ", s).strip().lower()

    doc = pymupdf.open(str(pdf))
    res = []
    textos = [p.get_text() for p in doc]
    inicios = []
    for t in textos:
        lineas = [l.strip() for l in t.splitlines() if l.strip()]
        if lineas and re.fullmatch(r"\d+", lineas[0]):
            lineas = lineas[1:]
        inicios.append(_norma(" ".join(lineas[:3])) if lineas else "")
    vacias = [i + 1 for i, t in enumerate(textos) if len(t.strip()) < 30]
    res.append(("Sin paginas vacias", not vacias, str(vacias)))
    for m in MARCADORES_V07:
        mn = _norma(m)
        pg = next((i for i, ini in enumerate(inicios) if ini.startswith(mn)), None)
        if pg is None:
            res.append((f"Marcador '{m}' presente", False, "no encontrado"))
            continue
        res.append((f"'{m[:48]}...' abre pagina {pg + 1}", True, inicios[pg][:60]))
    firma = next((i for i, t in enumerate(textos) if _norma("Firma del juez validador") in _norma(t)), None)
    res.append(("Cierre unico del juez dentro de la matriz de validez",
                firma is not None and firma <= 5, f"firma pagina {firma + 1 if firma is not None else None}"))
    res.append(("Total de paginas entre 10 y 14", 10 <= len(doc) <= 14, str(len(doc))))
    return res


def generar_v07():
    import shutil
    DIR_V07.mkdir(parents=True, exist_ok=True)
    rutas = [DIR_V07 / nombre_v07(n) for n in (1, 2, 3)]
    existentes = [r for r in rutas if r.exists()]
    if existentes:
        for r in existentes:
            print(f"[OMITIDO] {r.name} ya existe; no se sobrescribe")
        return 0
    maestro = rutas[0]
    construir_v07().save(str(maestro))
    res = verificar_v07(maestro)
    malos = [r for r in res if not r[1]]
    if malos:
        maestro.unlink()
        print(f"[ABORTADO] {maestro.name}: {len(malos)} comprobaciones no conformes; archivo eliminado")
        for nom, _, det in malos:
            print(f"   FALLA {nom} {det}")
        return 1
    print(f"[OK] {maestro.name} ({maestro.stat().st_size:,} bytes): {len(res)} comprobaciones conformes")
    for r in rutas[1:]:
        shutil.copyfile(maestro, r)
        print(f"[OK] {r.name} copia byte-identica del ejemplar 01 ({r.stat().st_size:,} bytes)")
    return 0


# ============================================================ PERFIL VERTICAL v08
# Reorganización y enriquecimiento editorial metodológico: TODAS las páginas A4
# vertical (ancho útil 8788 dxa), incorporando las 6 observaciones críticas del
# tesista:
# 1. Denominación rigurosa: Ficha N.° 01, Ficha N.° 02 y Cuestionario N.° 03.
# 2. Carta mejorada con encabezado Señor(a), los 3 instrumentos articulados y 5 adjuntos.
# 3. Instrucciones mejoradas con Tabla 1 (Criterios), Tabla 2 (Escala 1 a 4) y 5 pautas.
# 4. Matriz de validación de 8 columnas en A4 vertical (8788 dxa) con rejilla completa,
#    2 filas de cabecera repetidas (tblHeader), cantSplit en todas las filas y 12 filas continuas.
# 5. Decisión final sobre aplicabilidad: opinión global (4 opciones), suficiencia de los
#    ítems (Sí/No), líneas de observaciones generales, datos del juez y firma en blanco.
# 6. Reactivos del Cuestionario 03 (Modalidad A) reformulados a una sola idea atómica.
# 7. Ficha N.° 01: Mediana de las 3 tareas como estadístico principal; promedio complementario.
# 8. Ficha N.° 02: Unidad de análisis documental y documentos fuente en encabezado;
#    Criterio 4 de RSD actualizado con orden de pedido o nota de modificación autorizada.
# 9. Matriz de consistencia: Hipótesis general con texto de integración metodológica
#    (eliminado el criterio de rechazo p < 0.05).

VERSION_V08 = "v08"
DIR_V08 = RUTA_SALIDA / "vertical_v08"
ANCHOS_ELEM_2 = [1900, ANCHO_RETRATO - 1900]
ANCHOS_OPER_3 = [1500, 3644, 3644]
ANCHOS_TAREA_V08 = [1000, 2350, 900, 900, 1088, 1150, 1400]
ANCHOS_RSD_V08 = [500, 2300, 1000, 1000, 1600, 2388]
ANCHOS_CPE_A_V08 = [500, 2400, 1488, 1500, 1500, 1400]
ANCHOS_CPE_B_V08 = [500, 2400, 1900, 3988]
ANCHOS_MATRIZ_VALIDEZ_V08 = [420, 1050, 1450, 2868, 750, 750, 750, 750]  # suma exacta 8788 dxa
for _a in (ANCHOS_ELEM_2, ANCHOS_OPER_3, ANCHOS_TAREA_V08, ANCHOS_RSD_V08, ANCHOS_CPE_A_V08, ANCHOS_CPE_B_V08, ANCHOS_MATRIZ_VALIDEZ_V08):
    assert sum(_a) == ANCHO_RETRATO, _a

CABECERA_MATRIZ_V08 = "Elemento"   # distingue matrices académicas (APA 7) de formularios (rejilla)
ENCABEZADOS_TAREA_V08 = ["N.° y código", "Tarea estandarizada", "Hora de inicio", "Hora de fin",
                         "Tiempo neto (min:s)", "Tiempo (min decimales)", "Incidencias"]
ENCABEZADOS_CPE_A_V08 = ["N.°", "Vacuna o biológico", "N.° de documento", "Cantidad programada",
                         "Cantidad entregada", "Diferencia"]
ENCABEZADOS_CPE_B_V08 = ["N.°", "Justificación formal acreditada",
                         "Veredicto (1 = concordante, 0 = no concordante)", "Causa raíz del desfase"]

ITEMS_AP_V08 = [
    "El procedimiento para registrar los movimientos diarios de vacunas se realiza de forma ágil.",
    "El trámite para emitir comprobantes de salida y vales de entrega se efectúa sin demoras innecesarias.",
    "El procedimiento utilizado facilita la conciliación de saldos de vacunas entre el centro de acopio y los establecimientos de salud.",
    "En general, considero satisfactoria la forma en que se gestionan los movimientos de vacunas.",
]

ITEMS_UP_V08 = [
    "El procedimiento de registro permite disponer oportunamente de información actualizada sobre los saldos de vacunas.",
    "El procedimiento de emisión de comprobantes reduce la presencia de errores en la asignación de biológicos.",
    "El procedimiento de conciliación facilita la justificación técnica de las discrepancias entre cantidades programadas y entregadas.",
    "El procedimiento actual de gestión de movimientos contribuye a prevenir el desabastecimiento de vacunas en los establecimientos de salud.",
]

CRITERIOS_RSD_V08 = [
    "Tipo de movimiento clasificado de forma unívoca (entrada por remesa, salida a establecimiento o ajuste).",
    "Denominación oficial estandarizada del biológico según el esquema regular nacional.",
    "Identificación exacta del número de lote, coincidente con el rótulo del frasco.",
    "Cantidad entregada conforme con la orden de pedido aprobada por la coordinación de inmunizaciones o con nota de modificación autorizada.",
    "Fecha del movimiento consignada completa (día, mes y año) y en secuencia cronológica.",
    "Establecimiento de origen o destino individualizado con su código oficial.",
    "Nombre, firma o usuario responsable del despacho o recepción plenamente trazable.",
    "Documento formal de respaldo asociado y verificado (vale oficial, PECOSA o guía de remisión).",
]

FILAS_MATRIZ_VALIDEZ_V08 = [
    (
        "1",
        "Ficha N.° 01\n(Tiempos)",
        "Oportunidad:\nTreg",
        "Tiempo de registro de un movimiento de vacunas: cronometraje de la tarea estandarizada desde que el operador toma el documento o abre la digitación hasta que el movimiento queda grabado o asentado con saldo actualizado, consignado en minutos decimales.",
    ),
    (
        "2",
        "Ficha N.° 01\n(Tiempos)",
        "Oportunidad:\nTvale",
        "Tiempo de emisión del comprobante de salida o vale: cronometraje desde que el operador recibe o abre la solicitud de pedido hasta que el comprobante queda generado, firmado o impreso, consignado en minutos decimales por tarea estandarizada.",
    ),
    (
        "3",
        "Ficha N.° 02\n(Cotejo)",
        "Consistencia:\nRSD",
        "Porcentaje de registros auditados que cumplen simultáneamente los ocho criterios de la ficha: tipo de movimiento, denominación del biológico, lote, cantidad conforme a orden/nota de modificación, fecha, establecimiento, responsable y documento de respaldo; basta un incumplimiento para registrar discrepancia.",
    ),
    (
        "4",
        "Ficha N.° 02\n(Cotejo)",
        "Consistencia:\nCPE",
        "Porcentaje de entregas en las que la cantidad entregada coincide con la programada o cuenta con justificación ministerial acreditada; la ficha coteja ambas cantidades en el vale y el indicador expresa la razón de entregas concordantes sobre el total evaluado.",
    ),
    (
        "5",
        "Cuestionario\nN.° 03",
        "Satisfacción:\nAP-01",
        ITEMS_AP_V08[0],
    ),
    (
        "6",
        "Cuestionario\nN.° 03",
        "Satisfacción:\nAP-02",
        ITEMS_AP_V08[1],
    ),
    (
        "7",
        "Cuestionario\nN.° 03",
        "Satisfacción:\nAP-03",
        ITEMS_AP_V08[2],
    ),
    (
        "8",
        "Cuestionario\nN.° 03",
        "Satisfacción:\nAP-04",
        ITEMS_AP_V08[3],
    ),
    (
        "9",
        "Cuestionario\nN.° 03",
        "Satisfacción:\nUP-01",
        ITEMS_UP_V08[0],
    ),
    (
        "10",
        "Cuestionario\nN.° 03",
        "Satisfacción:\nUP-02",
        ITEMS_UP_V08[1],
    ),
    (
        "11",
        "Cuestionario\nN.° 03",
        "Satisfacción:\nUP-03",
        ITEMS_UP_V08[2],
    ),
    (
        "12",
        "Cuestionario\nN.° 03",
        "Satisfacción:\nUP-04",
        ITEMS_UP_V08[3],
    ),
]

MARCADORES_V08 = [
    f"Andahuaylas, ........ de ........................ de {ANIO}",
    "INSTRUCCIONES PARA LA VALIDACIÓN POR JUICIO DE EXPERTOS",
    "MATRIZ DE VALIDACIÓN DE CONTENIDO POR JUICIO DE EXPERTOS",
    "MATRIZ DE CONSISTENCIA",
    "MATRIZ DE OPERACIONALIZACIÓN DE VARIABLES",
    "INSTRUMENTO N.° 01",
    "INSTRUMENTO N.° 02",
    "INSTRUMENTO N.° 03",
]


def _v08_mantener(t, max_filas=14):
    """Mantiene unida una tabla corta (keep-with-next salvo la última fila)."""
    if len(t.rows) > max_filas:
        return t
    for row in t.rows[:-1]:
        for cell in row.cells:
            for p in cell.paragraphs:
                p.paragraph_format.keep_with_next = True
    return t


def v08_tabla(doc, encabezado, filas, anchos, rejilla=True, mantener=True, **kw):
    kw.setdefault("margen", (30, 70, 30, 70))
    if rejilla:
        t = v07_tabla_rejilla(doc, encabezado, filas, anchos, ANCHO_RETRATO, **kw)
    else:
        t = tabla(doc, encabezado, filas, anchos, ANCHO_RETRATO, **kw)
    return _v08_mantener(t) if mantener else t


def _v08_aire(doc, pts=5):
    par(doc, "", size=pts, line=1.0)


def _separar_etiqueta(texto):
    lineas = texto.split("\n")
    if len(lineas) > 1 and lineas[0].endswith(":"):
        return lineas[0], "\n".join(lineas[1:])
    return None, texto


def _filas_mc_v08():
    """Filas de la matriz de consistencia v08 con la hipótesis general ajustada
    por mandato metodológico del tesista (análisis conjunto e integración)."""
    d1, d2, d3 = _mc("oportunidad de procesamiento"), _mc("consistencia documental"), _mc("satisfacción del usuario")
    hg_v08 = (
        "Hipótesis general:\n"
        f"La aplicación del sistema \"SIVAC\" mejora significativamente la gestión de movimientos mensuales de vacunas {SUJ}, Andahuaylas 2025.\n"
        "La hipótesis general será contrastada a partir de la integración de los resultados obtenidos en las tres "
        "dimensiones específicas (oportunidad, consistencia y satisfacción), mediante un análisis conjunto de la "
        "significancia estadística y el tamaño del efecto en cada indicador."
    )
    return [
        ["Problema general:\n" + MC_PG,
         "Objetivo general:\nDeterminar en qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de "
         f"movimientos mensuales de vacunas {SUJ}, Andahuaylas 2025.",
         hg_v08,
         "Variable independiente:\nSistema web SIVAC.\nCondición X0 (pretest): ausencia del sistema; gestión "
         "manual tradicional.\nCondición X1 (postest): presencia y uso del sistema SIVAC.",
         "Escala: dicotómica nominal (0 = pretest, 1 = postest).\nSustento técnico: metodología Extreme "
         "Programming y calidad ISO/IEC 25010:2023."],
        ["Problema específico 1:\n" + d1[0], "Objetivo específico 1:\n" + d1[1],
         "Hipótesis específica 1:\n" + d1[2],
         "Variable dependiente:\nGestión de movimientos mensuales de vacunas.\nDimensión 1: oportunidad de procesamiento.",
         "• Tiempo de registro de movimientos (Treg), en minutos decimales, escala de razón.\n"
         "• Tiempo de emisión de vales (Tvale), en minutos decimales, escala de razón.\nInstrumento: Ficha N.° 01."],
        ["Problema específico 2:\n" + d2[0], "Objetivo específico 2:\n" + d2[1],
         "Hipótesis específica 2:\n" + d2[2],
         "Dimensión 2: consistencia documental.",
         "• Registros sin discrepancias (RSD), en porcentaje, escala de razón.\n"
         "• Concordancia entre cantidad programada y entregada (CPE), en porcentaje acotado entre 0 y 100.\n"
         "Instrumento: Ficha N.° 02."],
        ["Problema específico 3:\n" + d3[0], "Objetivo específico 3:\n" + d3[1],
         "Hipótesis específica 3:\n" + d3[2],
         "Dimensión 3: satisfacción del usuario (satisfacción con el proceso).",
         "• Aceptación del proceso operativo (AP), 4 ítems, 4 a 20 puntos.\n"
         "• Utilidad percibida (UP), 4 ítems, 4 a 20 puntos.\nTotal: 8 ítems, 8 a 40 puntos, escala Likert de 1 a 5.\n"
         "Instrumento: Cuestionario N.° 03, Modalidad A."],
    ]


def v08_carta(doc):
    par(doc, f"Andahuaylas, ........ de ........................ de {ANIO}", align="right", size=10, after=2, line=1.0)
    par(doc, "Señor(a): ...........................................................", size=10.5, bold=True, after=0, line=1.0)
    par(doc, "Docente / Especialista en: ...........................................................", size=10, italic=True, after=2, line=1.0)
    par(doc, "Presente.-", size=10.5, after=3, line=1.0)
    par(doc, "De mi mayor consideración:", size=10.5, after=2, line=1.0)
    par(doc, f"Yo, {TESISTA}, tesista de la Escuela Profesional de Ingeniería de Sistemas de la Universidad "
             "Nacional José María Arguedas, me dirijo a usted con el debido respeto para solicitarle su valiosa "
             "colaboración como juez experto en la validación de contenido del conjunto de instrumentos de "
             "recolección de datos diseñados para medir la variable dependiente “Gestión de movimientos mensuales de vacunas”, "
             f"en el marco de la investigación titulada “{TITULO_TESIS}”.",
        align="both", first=1.27, size=10, after=2, line=1.15)
    par(doc, "La investigación articula tres instrumentos complementarios orientados a capturar con rigurosidad "
             "técnica y objetiva las tres dimensiones oficiales de la variable dependiente:",
        align="both", first=1.27, size=10, after=1, line=1.15)
    par(doc, "1.  Ficha N.° 01: Ficha de observación sistemática y medición de tiempos cronometrados, destinada a "
             "cuantificar la dimensión Oportunidad de procesamiento mediante el registro de tiempos netos de registro "
             "(Treg) y de emisión de comprobantes de salida o vales (Tvale).",
        align="both", hanging=0.8, size=9.5, after=1, line=1.1)
    par(doc, "2.  Ficha N.° 02: Ficha de registro y cotejo documental de consistencia, destinada a evaluar la "
             "dimensión Consistencia documental mediante la verificación de registros sin discrepancias (RSD) y la "
             "concordancia entre cantidades programadas y entregadas (CPE).",
        align="both", hanging=0.8, size=9.5, after=1, line=1.1)
    par(doc, "3.  Cuestionario N.° 03: Cuestionario de satisfacción del usuario y aceptación tecnológica, destinado a "
             "medir la dimensión Satisfacción del usuario respecto al proceso operativo bajo el modelo TAM (con reactivos "
             "en escala Likert, complementado con un módulo anexo de postest para evaluar la aceptación tecnológica).",
        align="both", hanging=0.8, size=9.5, after=2, line=1.1)
    par(doc, "La labor pericial solicitada consiste en evaluar la pertinencia, relevancia y claridad de cada uno de los "
             "elementos, criterios y reactivos mediante la matriz de validación adjunta, empleando una escala de valoración "
             "del 1 al 4. Con tal propósito, se adjuntan los siguientes documentos oficiales:",
        align="both", first=1.27, size=10, after=1, line=1.15, keep_next=True)
    adjuntos = [
        "Instrucciones para los jueces expertos y criterios de evaluación.",
        "Matriz de validación de contenido por ítem/criterio (escala de valoración del 1 al 4, con decisión final sobre aplicabilidad).",
        "Matriz de consistencia metodológica institucional (documento de consulta técnica; no se llena).",
        "Matriz de operacionalización de variables con las 3 dimensiones y 6 indicadores (documento de consulta; no se llena).",
        "Instrumentos de recolección de datos en blanco: Ficha N.° 01, Ficha N.° 02 y Cuestionario N.° 03 con Modalidad A y B (no se llenan).",
    ]
    for i, adj in enumerate(adjuntos, start=1):
        par(doc, f"{i}.  {adj}", hanging=0.8, size=9.5, after=1, line=1.05, align="both")
    par(doc, "Agradezco de antemano su tiempo, rigor académico y valioso aporte al desarrollo de esta investigación.",
        before=1, first=1.27, size=10, after=3, line=1.15)
    par(doc, "Atentamente,", align="center", size=10, after=8, line=1.0)
    par(doc, "..........................................................", align="center", size=10, line=1.0)
    par(doc, TESISTA, align="center", bold=True, size=10, line=1.0)
    par(doc, "Tesista", align="center", size=10, line=1.0)


def v08_instrucciones(doc):
    par(doc, "INSTRUCCIONES PARA LA VALIDACIÓN POR JUICIO DE EXPERTOS", bold=True, align="center", pbb=True, size=11, after=2, line=1.1)
    par(doc, "Estimado(a) especialista, a continuación se detallan los criterios de evaluación, la escala de valoración "
             "y las pautas metodológicas que guiarán la revisión pericial del conjunto de instrumentos:",
        align="both", size=9.5, after=2, line=1.1)
    par(doc, "Tabla 1. Criterios de evaluación", bold=True, size=9.5, before=1, after=1, keep_next=True)
    v08_tabla(doc, ["Criterio", "Definición operativa"], [
        ["Pertinencia", "El elemento, criterio o reactivo se encuentra estrechamente vinculado con el constructo teórico y la dimensión que pretende medir."],
        ["Relevancia", "El elemento, criterio o reactivo es fundamental y aporta significativamente a la medición representativa del indicador correspondiente."],
        ["Claridad", "La redacción del enunciado o definición es concisa, directa, comprensible y no genera ambigüedades interpretativas."],
    ], [1900, ANCHO_RETRATO - 1900], margen=(20, 45, 20, 45))
    _v08_aire(doc, 2)
    par(doc, "Tabla 2. Escala de valoración", bold=True, size=9.5, before=1, after=1, keep_next=True)
    v08_tabla(doc, ["Nivel", "Denominación", "Descripción operativa"], [
        ["1", "No cumple", "El elemento, criterio o reactivo no cumple con el criterio de evaluación; debe ser descartado o reformulado en su totalidad."],
        ["2", "Cumple parcialmente;\nrequiere modificación mayor", "El elemento, criterio o reactivo cumple de forma deficiente; requiere reestructuración sustancial antes de su aplicación."],
        ["3", "Cumple;\nrequiere modificación menor", "El elemento, criterio o reactivo cumple satisfactoriamente con el criterio evaluado, aunque es susceptible de mejoras puntuales de redacción o estilo."],
        ["4", "Cumple plenamente", "El elemento, criterio o reactivo satisface con total rigurosidad, precisión y exactitud el criterio evaluado; no requiere modificaciones."],
    ], [800, 2600, ANCHO_RETRATO - 3400], alinear=["center", "left", "left"], margen=(20, 45, 20, 45))
    par(doc, "Pautas metodológicas para la validación:", bold=True, size=9.5, before=2, after=1, keep_next=True)
    pautas = [
        "Consigne en cada casilla de la Matriz de Validación una calificación numérica del 1 al 4, conforme a la escala de valoración descrita.",
        "Revise detenidamente las definiciones operacionales y los instrumentos en blanco adjuntos como material de consulta; estos últimos no deben ser llenados.",
        "En la columna “Observaciones y sugerencias”, formule las recomendaciones cualitativas que considere pertinentes para perfeccionar los reactivos y criterios evaluados.",
        "En la sección final, emita su opinión global sobre la aplicabilidad del conjunto de instrumentos, indique si los elementos propuestos son suficientes para medir la variable y registre sus observaciones generales.",
        "Consigne sus datos profesionales completos (apellidos y nombres, DNI, especialidad, fecha) y suscriba la matriz con su firma. Devuelva el expediente al tesista para el procesamiento estadístico de la concordancia entre jueces (coeficiente V de Aiken).",
    ]
    for i, p in enumerate(pautas, start=1):
        par(doc, f"{i}.  {p}", hanging=0.8, size=9.0, after=1, line=1.05, align="both")


def v08_decision_final_cierre(doc):
    """Cierre metodológico del juez validador para v08: decisión sobre aplicabilidad,
    suficiencia de los ítems, observaciones generales y datos del experto con firma."""
    T = 10.0
    ps = []
    p_tit = par(doc, "DECISIÓN FINAL SOBRE LA APLICABILIDAD DEL INSTRUMENTO", bold=True, size=10.5, before=6, after=3, keep_next=True)
    ps.append(p_tit)

    p_op = par(doc, "1. Opinión global sobre el instrumento:", bold=True, size=T, before=2, after=2, keep_next=True)
    ps.append(p_op)
    p_cas = par(doc, "   [   ] Aplicable sin modificaciones\n"
                     "   [   ] Aplicable con modificaciones menores\n"
                     "   [   ] Requiere revisión y reestructuración sustancial\n"
                     "   [   ] No aplicable", size=T, line=1.15, before=1, after=3, keep_next=True)
    ps.append(p_cas)

    p_suf = par(doc, "2. Suficiencia de los elementos evaluados:", bold=True, size=T, before=2, after=1, keep_next=True)
    ps.append(p_suf)
    p_suf_q = par(doc, "¿Los elementos propuestos son suficientes para medir la variable en estudio?\n"
                       "   [   ] Sí          [   ] No", size=T, line=1.15, before=1, after=3, keep_next=True)
    ps.append(p_suf_q)

    p_obs = par(doc, "3. Observaciones y recomendaciones generales:", bold=True, size=T, before=2, after=2, keep_next=True)
    ps.append(p_obs)
    for _ in range(3):
        fany.agregar_linea_escritura(doc, before=4, after=4)
        ps.append(doc.paragraphs[-1])
        doc.paragraphs[-1].paragraph_format.keep_with_next = True

    p_dat = par(doc, "4. Datos del juez validador:", bold=True, size=T, before=3, after=2, keep_next=True)
    ps.append(p_dat)
    ps.append(par(doc, "Apellidos y nombres del juez validador: ...........................................................................................", size=T, before=2, after=2, keep_next=True))
    ps.append(par(doc, "DNI: .....................................................       Especialidad: .....................................................................", size=T, before=2, after=2, keep_next=True))
    ps.append(par(doc, f"Fecha de evaluación: Andahuaylas, ......... de ........................................ del {ANIO}", size=T, before=2, after=6, keep_next=True))

    ps.append(par(doc, "________________________________________", align="center", size=T, before=10, after=1, keep_next=True))
    ps.append(par(doc, "Firma del juez validador", align="center", bold=True, size=T, before=0, after=0))
    for p in ps:
        p.paragraph_format.keep_with_next = True
    return ps


def v08_matriz_validacion(doc):
    par(doc, "MATRIZ DE VALIDACIÓN DE CONTENIDO POR JUICIO DE EXPERTOS", bold=True, align="center", pbb=True, after=2)
    par(doc, "CONJUNTO DE INSTRUMENTOS DE LA VARIABLE DEPENDIENTE: GESTIÓN DE MOVIMIENTOS MENSUALES DE VACUNAS",
        bold=True, align="center", size=11, line=1.15, after=2)
    par(doc, "Instrucción pericial: califique cada elemento en las columnas Pertinencia, Relevancia y Claridad con valores del 1 al 4. "
             "En Oportunidad y Consistencia se evalúan las especificaciones de las fichas operativas; en Satisfacción se evalúan los reactivos del cuestionario.",
        align="center", size=9.5, italic=True, line=1.0, after=4)

    anchos = ANCHOS_MATRIZ_VALIDEZ_V08
    t = doc.add_table(rows=2 + len(FILAS_MATRIZ_VALIDEZ_V08), cols=8)
    quir.configurar_geometria_tabla(t, ANCHO_RETRATO, anchos, align="center", cell_margin_dxa=(20, 35, 20, 35))
    quir.aplicar_bordes_rejilla(t)
    fany.fijar_disposicion_fija(t)

    # Merges verticales para cols 0, 1, 2, 3, 7
    for c in (0, 1, 2, 3, 7):
        celda = t.cell(0, c).merge(t.cell(1, c))
        celda.width = Cm(anchos[c] / 567.0)

    # Merge horizontal para cols 4, 5, 6 en fila 0
    celda_crit = t.cell(0, 4).merge(t.cell(0, 6))
    celda_crit.width = Cm((anchos[4] + anchos[5] + anchos[6]) / 567.0)

    fany.texto_celda(t.cell(0, 0), "N.°", tamano=9.5, negrita=True, alineacion="center")
    fany.texto_celda(t.cell(0, 1), "Instrumento", tamano=9.5, negrita=True, alineacion="center")
    fany.texto_celda(t.cell(0, 2), "Dimensión /\nindicador", tamano=9.5, negrita=True, alineacion="center")
    fany.texto_celda(t.cell(0, 3), "Elemento, criterio o reactivo", tamano=9.5, negrita=True, alineacion="center")
    fany.texto_celda(celda_crit, "Criterios de evaluación (Escala 1 a 4)", tamano=9.5, negrita=True, alineacion="center")
    fany.texto_celda(t.cell(0, 7), "Observaciones y sugerencias", tamano=9.5, negrita=True, alineacion="center")

    fany.texto_celda(t.cell(1, 4), "Pertinencia\n(1–4)", tamano=8.5, negrita=True, alineacion="center")
    fany.texto_celda(t.cell(1, 5), "Relevancia\n(1–4)", tamano=8.5, negrita=True, alineacion="center")
    fany.texto_celda(t.cell(1, 6), "Claridad\n(1–4)", tamano=8.5, negrita=True, alineacion="center")

    for idx, fila_datos in enumerate(FILAS_MATRIZ_VALIDEZ_V08, start=2):
        num_str, inst, dim_ind, elem = fila_datos
        fany.texto_celda(t.cell(idx, 0), num_str, tamano=9.0, alineacion="center")
        fany.texto_celda(t.cell(idx, 1), inst, tamano=8.5, alineacion="center")
        fany.texto_celda(t.cell(idx, 2), dim_ind, tamano=8.5, alineacion="center")
        fany.texto_celda(t.cell(idx, 3), elem, tamano=9.0, alineacion="both", before=3, after=3, margen_izq_dxa=30)
        for c in (4, 5, 6, 7):
            fany.fijar_contenido_celda(t.cell(idx, c), fany._p_vacio())

    fany.normalizar_celdas_sin_parrafo(t)
    for row in t.rows:
        for cell in row.cells:
            cell.vertical_alignment = fany.WD_ALIGN_VERTICAL.CENTER
    quir.blindar_filas_tabla(t, cant_split=True, repetir_encabezado=True, filas_encabezado=2)
    quir.normalizar_orden_tblPr(t)

    # Cierre del juez (opinión global, suficiencia, observaciones y firma)
    v08_decision_final_cierre(doc)


def v08_matriz_consistencia(doc):
    par(doc, "MATRIZ DE CONSISTENCIA", bold=True, align="center", after=2, pbb=True)
    par(doc, TITULO_TESIS, italic=True, align="center", size=TAM_TABLA, line=1.0, after=6)
    bloques = ["Bloque general", "Bloque específico 1", "Bloque específico 2", "Bloque específico 3"]
    campos = ["Problema", "Objetivo", "Hipótesis", "Variable / dimensión", "Indicadores"]
    for i, (fila, titulo) in enumerate(zip(_filas_mc_v08(), bloques)):
        rows = []
        for celda, defecto in zip(fila, campos):
            etiqueta, resto = _separar_etiqueta(celda)
            rows.append([etiqueta or defecto, resto])
        if i:
            _v08_aire(doc, 5)
        v08_tabla(doc, [CABECERA_MATRIZ_V08, titulo], rows, ANCHOS_ELEM_2, rejilla=False,
                  alinear=["left", "left"])
    par(doc, NOTA_METODOLOGIA_V07, size=9.5, line=1.0, before=5, italic=True, align="both")


def v08_operacionalizacion(doc):
    par(doc, "MATRIZ DE OPERACIONALIZACIÓN DE VARIABLES", bold=True, align="center", pbb=True, before=4, after=6,
        keep_next=True)
    f = _filas_operacionalizacion()
    etq = ["Variable", "Dimensión", "Indicador", "Definición operacional", "Escala", "Instrumento"]
    v08_tabla(doc, [CABECERA_MATRIZ_V08, "Contenido"], [[etq[k], f[0][k]] for k in range(6)], ANCHOS_ELEM_2,
              rejilla=False, alinear=["left", "left"])
    for (a, b) in ((1, 2), (3, 4), (5, 6)):
        _v08_aire(doc, 5)
        rows = [[etq[0], f[1][0], ""], [etq[1], f[a][1], ""]]
        for k in (2, 3, 4, 5):
            rows.append([etq[k], f[a][k], f[b][k]])
        t = v08_tabla(doc, [CABECERA_MATRIZ_V08, "Indicador 1", "Indicador 2"], rows, ANCHOS_OPER_3,
                      rejilla=False, alinear=["left", "left", "left"], mantener=False)
        for r, texto in ((1, f[1][0]), (2, f[a][1])):
            m = t.cell(r, 1).merge(t.cell(r, 2))
            _tcw(m, ANCHOS_OPER_3[1] + ANCHOS_OPER_3[2])
            _contenido(m, texto, TAM_TABLA, align="left")
        _v08_mantener(t)
    par(doc, "Nota. Las fórmulas de cálculo de los indicadores se presentan en el cuerpo narrativo del Capítulo IV.",
        size=TAM_TABLA, line=1.0, before=5, italic=True)


def v08_ficha01(doc):
    par(doc, "INSTRUMENTO N.° 01", bold=True, align="center", after=0, pbb=True)
    par(doc, "FICHA DE OBSERVACIÓN SISTEMÁTICA Y MEDICIÓN DE TIEMPOS CRONOMETRADOS",
        bold=True, align="center", after=3)
    par(doc, "Dimensión: oportunidad de procesamiento. Indicadores: tiempo de registro (Treg) y tiempo de emisión "
             "de vale (Tvale). Formulario en blanco para captura objetiva de campo; no se llena durante la "
             "validación y sus campos no constituyen escalas de percepción.", align="both", size=10, line=1.15,
        after=3)
    par(doc, "1. Datos generales de la observación", bold=True, before=3, after=2, keep_next=True)
    v08_tabla(doc, ["Campo", "Registro"], [
        ["Código del operador evaluado", "TRAB-____  (TRAB-01 a TRAB-14)"],
        ["Rol institucional", "[  ] Responsable de centro de acopio o red de frío   [  ] Personal de estrategia "
                              "sanitaria de inmunizaciones"],
        ["Centro de acopio o sede / red o microred", "____________________________     Provincia:   "
                                                     "[  ] Andahuaylas   [  ] Chincheros"],
        ["Momento de medición", "[  ] Pretest (kardex físico, libros de registro y hojas de cálculo)   "
                                "[  ] Postest (sistema web SIVAC)"],
        ["Fecha de la observación", "______ / ______ / ______"],
        ["Evaluador principal", TESISTA + "     Secundario (si aplica): ______________________"],
    ], [3000, ANCHO_RETRATO - 3000])
    par(doc, "2. Protocolo de cronometraje y reglas de registro", bold=True, before=3, after=1, keep_next=True)
    for s in [
        "Cronómetro digital con precisión de centésimas de segundo; cada tiempo se consigna en minutos "
        "decimales (minutos enteros más la fracción de segundos sobre sesenta).",
        "Tiempo de registro: inicia al tomar el documento fuente o abrir la digitación y termina cuando el "
        "movimiento queda grabado o asentado con saldo actualizado.",
        "Tiempo de emisión de vales: inicia al recibir o abrir la solicitud de pedido y termina cuando el "
        "comprobante queda generado, firmado o impreso.",
        "Regla de pausa: ante una interrupción externa fortuita el cronómetro se detiene y se reanuda al "
        "normalizarse la tarea; se registra solo el tiempo neto efectivo. La batería consta de tres tareas "
        "de registro y tres de emisión por operador; la mediana de las tres tareas consolida el desempeño por "
        "operador como estadístico principal, reportándose el promedio como descriptivo complementario.",
    ]:
        par(doc, "•  " + s, align="left", size=10, line=1.15, hanging=0.6, after=1)
    par(doc, "3. Sección A: tareas de registro (Treg)", bold=True, before=3, after=1, keep_next=True)
    al = ["center", "left", "center", "center", "center", "center", "left"]
    v08_tabla(doc, ENCABEZADOS_TAREA_V08, [
        ["1\nREG-01", "Ingreso simple de remesa (1 biológico)"] + [""] * 5,
        ["2\nREG-02", "Salida regular programada (2 a 3 vacunas)"] + [""] * 5,
        ["3\nREG-03", "Redistribución o despacho complejo (4 a 6 ítems)"] + [""] * 5,
    ], ANCHOS_TAREA_V08, alto_min=620, alinear=al, margen=(30, 50, 30, 50))
    par(doc, "Mediana de las tres tareas (estadístico principal): ____________ min          Promedio (descriptivo complementario): ____________ min",
        before=3, after=1, keep_next=True)
    par(doc, "4. Sección B: tareas de emisión de vales (Tvale)", bold=True, before=3, after=1, keep_next=True)
    v08_tabla(doc, ENCABEZADOS_TAREA_V08, [
        ["1\nVALE-01", "Vale simple (puesto I-1 o I-2; 1 a 2 biológicos)\nVale N.°: ________"] + [""] * 5,
        ["2\nVALE-02", "Vale regular (centro I-3 o I-4; 3 a 5 biológicos)\nVale N.°: ________"] + [""] * 5,
        ["3\nVALE-03", "Vale de emergencia por contingencia de cadena de frío\nVale N.°: ________"] + [""] * 5,
    ], ANCHOS_TAREA_V08, alto_min=620, alinear=al, margen=(30, 50, 30, 50))
    par(doc, "Mediana de las tres tareas (estadístico principal): ____________ min          Promedio (descriptivo complementario): ____________ min",
        before=3, after=1, keep_next=True)
    par(doc, "5. Declaración y firma", bold=True, before=3, after=1, keep_next=True)
    p = par(doc, "Declaración: la presente toma de tiempos respetó los puntos de inicio y fin del protocolo y la "
                 "regla de pausa, con veracidad de los datos registrados.     Firma del evaluador: "
                 "______________________________     " + TESISTA + ", Tesista", align="left", after=0)
    p.paragraph_format.keep_together = True


def v08_ficha02(doc):
    par(doc, "INSTRUMENTO N.° 02", bold=True, align="center", after=0, pbb=True)
    par(doc, "FICHA DE REGISTRO Y COTEJO DOCUMENTAL DE CONSISTENCIA", bold=True, align="center", after=2)
    par(doc, "Dimensión: consistencia documental. Indicadores: registros sin discrepancias (RSD) y concordancia "
             "entre cantidad programada y entregada (CPE). Formulario en blanco para auditoría documental; no se "
             "llena durante la validación.", align="both", size=10, line=1.15, after=2)
    par(doc, "1. Datos generales de la auditoría documental", bold=True, before=3, after=2, keep_next=True)
    v08_tabla(doc, ["Campo", "Registro"], [
        ["Código del operador o centro auditado", "TRAB-____  (TRAB-01 a TRAB-14)"],
        ["Centro de acopio provincial o microred", "____________________________     Provincia:   "
                                                   "[  ] Andahuaylas   [  ] Chincheros"],
        ["Unidad de análisis documental", "Movimiento individual de vacuna registrado en documento oficial "
                                          "(kardex físico/hoja de cálculo en pretest; módulo de movimientos en SIVAC en postest)"],
        ["Documentos fuente consultados", "Pretest: Kardex físico, Pecosa física, Cuaderno de control de cadena de frío, Hojas de cálculo locales.\n"
                                          "Postest: Módulo de movimientos de SIVAC, Comprobante de salida digital (vale electrónico), Registro de auditoría del sistema."],
        ["Momento de medición", "[  ] Pretest (kardex manual, cuadernos y hojas de cálculo)   [  ] Postest "
                                "(base de datos y vales electrónicos de SIVAC)"],
        ["Ventana de auditoría", "Del ____ / ____ / ______  al  ____ / ____ / ______  (30 días calendario)"],
        ["Fecha de ejecución de la auditoría", "______ / ______ / ______"],
        ["Auditor principal", TESISTA + "     Secundario (si aplica): ______________________"],
    ], [3000, ANCHO_RETRATO - 3000])
    par(doc, "2. Regla de conformidad y los ocho criterios (RSD)", bold=True, before=3, after=1, keep_next=True)
    par(doc, "Un registro es conforme (1) cuando cumple simultáneamente los ocho criterios siguientes; si "
             "incumple al menos uno, es no conforme (0). Se audita un corpus de 40 a 60 registros por ventana.",
        align="left", size=10, line=1.15, after=1, keep_next=True)
    for i, c in enumerate(CRITERIOS_RSD_V08, start=1):
        par(doc, f"{i}.  {c}", align="left", size=10, line=1.15, hanging=0.6, after=0)
    par(doc, "3. Matriz de auditoría de registros (RSD)", bold=True, before=4, after=1, keep_next=True)
    filas_rsd = [[f"{i:02d}", v, "", "", "[  ] 1   [  ] 0", ""] for i, v in enumerate(MUESTRA_RSD_V07, 1)]
    filas_rsd.append(["...", "Continúa según el corpus real (40 a 60 registros por ventana)", "", "",
                      "[  ] 1   [  ] 0", ""])
    v08_tabla(doc, ["N.°", "Vacuna o insumo auditado", "Lote", "Cantidad",
                    "Veredicto (1 = conforme, 0 = no conforme)", "Tipo de discrepancia o causa raíz"],
              filas_rsd, ANCHOS_RSD_V08, alto_min=430,
              alinear=["center", "left", "left", "center", "center", "left"])
    par(doc, "Nota: si el corpus supera las filas disponibles, continúe en una hoja adicional con el mismo "
             "formato.", size=9.5, line=1.0, before=3, italic=True, keep_next=True)
    par(doc, "Total de registros evaluados: ______      Registros conformes: ______      "
             "Registros con discrepancia: ______      RSD: ______ %", before=2, after=0)
    par(doc, "4. Regla de concordancia y matriz de entregas (CPE)", bold=True, before=4, after=1, keep_next=True)
    par(doc, "Una entrega es concordante (1) si la cantidad entregada es idéntica a la programada o si, siendo "
             "distinta, existe un documento sustentatorio oficial archivado que autoriza expresamente la "
             "variación; en cualquier otro caso es no concordante (0). Se auditan de 40 a 60 entregas por "
             "ventana. Consolidado: Total de entregas auditadas ______, concordantes ______, no concordantes "
             "______, CPE ______ %.", align="left", size=10, line=1.15, after=2, keep_next=True)
    filas_a = [[f"{i:02d}", v, "Vale N.°:", "", "", ""] for i, v in enumerate(MUESTRA_CPE_V07, 1)]
    filas_a.append(["...", "Continúa en hoja adicional", "", "", "", ""])
    filas_b = [[f"{i:02d}", "[  ] Sí [  ] No [  ] N/A", "[  ] 1  [  ] 0", ""]
               for i in range(1, len(MUESTRA_CPE_V07) + 1)]
    filas_b.append(["...", "", "", ""])
    par(doc, "Las dos tablas siguientes se corresponden por número de caso: cantidades (4a) y verificación (4b).",
        size=9.5, line=1.0, italic=True, after=2, keep_next=True)
    v08_tabla(doc, ENCABEZADOS_CPE_A_V08, filas_a, ANCHOS_CPE_A_V08, alto_min=430,
              alinear=["center", "left", "left", "center", "center", "center"], margen=(30, 50, 30, 50))
    _v08_aire(doc, 6)
    v08_tabla(doc, ENCABEZADOS_CPE_B_V08, filas_b, ANCHOS_CPE_B_V08, alto_min=430,
              alinear=["center", "center", "center", "left"], margen=(30, 50, 30, 50))


def v08_cuestionario(doc):
    par(doc, "INSTRUMENTO N.° 03", bold=True, align="center", after=0, pbb=True)
    par(doc, "CUESTIONARIO DE SATISFACCIÓN DEL USUARIO Y ACEPTACIÓN TECNOLÓGICA (MODELO TAM)",
        bold=True, align="center", after=3)
    par(doc, "Variable evaluada: gestión de movimientos mensuales de vacunas (variable dependiente). Dimensión: "
             "satisfacción del usuario. Población objetivo: personal de la cadena de frío e inmunizaciones de la "
             "DISA Apurímac II (N = n = 14). Formulario en blanco; no se llena durante la validación.",
        align="both", size=10, after=4)
    par(doc, "1. Instrucciones para el participante y escala de respuesta (Likert de 5 opciones)", bold=True,
        before=4, after=2, keep_next=True)
    par(doc, "•  Confidencialidad y anonimato bajo código numérico (TRAB-01 a TRAB-14), conforme a la Ley "
             "N.° 29733 de Protección de Datos Personales y el Código de Ética en Investigación de la UNAJMA.",
        align="left", hanging=0.8, after=1)
    par(doc, "•  Libertad de respuesta: no existen respuestas correctas ni incorrectas; marque con una equis (X) "
             "una sola alternativa por reactivo; las proposiciones son afirmaciones que se gradúan, no preguntas.",
        align="left", hanging=0.8, after=3)
    v08_tabla(doc, ["Puntuación", "Escala verbal", "Significado operativo"], ESCALA_LIKERT,
              ANCHOS_ESCALA_V07, alinear=["center", "left", "left"])
    par(doc, "Momento de aplicación (marque el evaluador):    [  ] Pretest (proceso manual)    "
             "[  ] Postest (proceso con el sistema web SIVAC).", before=5, after=2)
    par(doc, "2. Datos generales del participante", bold=True, before=4, after=1, keep_next=True)
    v08_tabla(doc, ["Campo", "Registro"], [
        ["Código de participante asignado", "TRAB-____  (TRAB-01 a TRAB-14)"],
        ["Centro de acopio / red / microred", ""],
        ["Provincia de desempeño", "[  ] Andahuaylas   [  ] Chincheros"],
        ["Condición laboral actual", "[  ] Nombrado D.L. 276   [  ] Contratado CAS (D.L. 1057)   "
                                     "[  ] Locación / otro"],
        ["Profesión / cargo operativo", "[  ] Lic. en Enfermería   [  ] Técnico(a) en Enfermería   "
                                        "[  ] Estadístico / soporte"],
        ["Tiempo de experiencia en red de frío", "[  ] Menos de 2 años   [  ] 2 a 5 años   [  ] 6 a 10 años   "
                                                 "[  ] Más de 10 años"],
        ["Fecha de aplicación", "______ / ______ / ______"],
    ], [3800, ANCHO_RETRATO - 3800])
    par(doc, "3. Modalidad A: satisfacción con el proceso operativo (AP y UP)", bold=True, before=6, after=1,
        keep_next=True)
    par(doc, "Ocho afirmaciones literales sobre la gestión del proceso; en el pretest el participante evalúa el "
             "proceso manual y en el postest el proceso mediado por el sistema. " + LEYENDA_LIKERT_V07,
        align="left", size=10, after=1)
    v07_tabla_likert(doc, [
        ("Indicador: Aceptación del proceso operativo (AP)", ["AP-01", "AP-02", "AP-03", "AP-04"], ITEMS_AP_V08),
        ("Indicador: Utilidad percibida para la gestión sanitaria (UP)", ["UP-01", "UP-02", "UP-03", "UP-04"],
         ITEMS_UP_V08),
    ])
    par(doc, "Firma del participante: ______________________________", before=8, after=2)
    par(doc, "Firma del encuestador (Bach. José Luis Quispe León, Tesista): ______________________________",
        after=0)
    par(doc, "4. Modalidad B: módulo anexo de postest", bold=True, before=6, after=1, pbb=True, keep_next=True)
    par(doc, "Código de participante (TRAB): TRAB-______     Fecha de aplicación postest: ____ / ____ / ______",
        before=2, after=2)
    par(doc, ROTULO_MODALIDAD_B_V07 + " " + LEYENDA_LIKERT_V07, align="both", size=10, italic=True, bold=True,
        after=3)
    v07_tabla_likert(doc, [
        ("Utilidad percibida del software (PU)", ["PU-01", "PU-02", "PU-03", "PU-04"], ITEMS_PU),
        ("Facilidad de uso percibida del software (PE)", ["PE-01", "PE-02", "PE-03", "PE-04"], ITEMS_PE),
    ])
    par(doc, "Firma del participante: ______________________________", before=8, after=2)
    par(doc, "Firma del encuestador (Bach. José Luis Quispe León, Tesista): ______________________________",
        after=0)


def construir_v08():
    doc = docx.Document()
    configurar_normal(doc)
    aplicar_geometria(doc.sections[0], "unajma")
    pie_pagina(doc.sections[0])
    cp = doc.core_properties
    cp.author, cp.title, cp.last_modified_by = TESISTA, "Expediente de validación para experto (v08 vertical)", TESISTA
    cp.comments, cp.subject, cp.keywords = "", "", ""
    v08_carta(doc)
    v08_instrucciones(doc)
    v08_matriz_validacion(doc)
    v08_matriz_consistencia(doc)
    v08_operacionalizacion(doc)
    v08_ficha01(doc)
    v08_ficha02(doc)
    v08_cuestionario(doc)
    return doc


def nombre_v08(n):
    return f"EXPEDIENTE_VALIDACION_SIVAC_VERTICAL_EXPERTO_0{n}_{VERSION_V08}.docx"


def verificar_v08(ruta):
    """Audita el DOCX v08 GUARDADO. Devuelve [(nombre, ok, detalle)]."""
    res = []

    def chk(nombre, ok, det=""):
        res.append((nombre, bool(ok), det))

    d = docx.Document(str(ruta))
    body = d.element.body
    txt = "\n".join(t.text or "" for t in body.iter(qn("w:t")))
    plano = re.sub(r"\s+", " ", txt)
    nplano = fany._normalizar(txt)
    norm = fany._normalizar

    # 1. Orden de piezas principales
    pars = [_txt(p) for p in body.findall(qn("w:p"))]
    pos = [next((i for i, t in enumerate(pars) if t.startswith(m)), None) for m in MARCADORES_V08]
    chk("Orden de piezas carta, instrucciones, matriz de validez, matrices, instrumentos 01/02/03",
        None not in pos and pos == sorted(pos), str(pos))

    # 2. Geometria de secciones: 100% vertical A4
    geo_ok, det_geo = True, []
    for s in d.sections:
        w, h = s.page_width.cm, s.page_height.cm
        orient = s._sectPr.find(qn("w:pgSz")).get(qn("w:orient"))
        ok = (w < h and orient != "landscape" and abs(w - 21.0) < 0.1 and abs(h - 29.7) < 0.1
              and abs(s.left_margin.cm - 3.0) < 0.05 and abs(s.right_margin.cm - 2.5) < 0.05
              and abs(s.top_margin.cm - 2.5) < 0.05 and abs(s.bottom_margin.cm - 2.5) < 0.05)
        geo_ok &= ok
        det_geo.append((round(w, 1), round(h, 1), orient))
    chk("Todas las secciones A4 vertical (ancho<alto, sin landscape, margenes 3/2.5/2.5/2.5)",
        geo_ok and len(d.sections) >= 1, str(det_geo))

    # 3. Tablas OpenXML: geometria, bordes y blindaje
    ok_flo = ok_cs = ok_hd = ok_math = ok_ancho = ok_bordes = ok_neg = ok_filas = ok_ind = True
    n_rejilla = n_apa = 0
    det_bordes = []
    for t in d.tables:
        tblPr = t._tbl.tblPr
        ok_flo &= tblPr.find(qn("w:tblpPr")) is None
        w = int(tblPr.find(qn("w:tblW")).get(qn("w:w")))
        grid = [int(g.get(qn("w:w"))) for g in t._tbl.tblGrid.findall(qn("w:gridCol"))]
        ok_ancho &= (w == sum(grid) == ANCHO_RETRATO)
        ok_neg &= all(x > 0 for x in grid)
        ind = tblPr.find(qn("w:tblInd"))
        ok_ind &= ind is None or int(ind.get(qn("w:w"), "0")) == 0
        for tr in t._tbl.findall(qn("w:tr")):
            trPr = tr.find(qn("w:trPr"))
            ok_cs &= trPr is not None and trPr.find(qn("w:cantSplit")) is not None
            ws = [int(x.get(qn("w:w"))) for x in tr.xpath("./w:tc/w:tcPr/w:tcW")]
            ok_neg &= all(x > 0 for x in ws)
            ok_filas &= sum(ws) == w and len(ws) == len(tr.findall(qn("w:tc")))
        primera_tr = t._tbl.find(qn("w:tr")).find(qn("w:trPr"))
        ok_hd &= primera_tr is not None and primera_tr.find(qn("w:tblHeader")) is not None
        ok_math &= len(t._tbl.xpath('.//*[local-name()="oMath"]')) == 0
        tb = tblPr.find(qn("w:tblBorders"))
        if tb is None:
            ok_bordes = False
            det_bordes.append("sin tblBorders")
            continue
        estados = {l: (tb.find(qn("w:" + l)).get(qn("w:val")) if tb.find(qn("w:" + l)) is not None else None)
                   for l in ("top", "left", "bottom", "right", "insideH", "insideV")}
        enc = _txt(t._tbl.find(qn("w:tr")).find(qn("w:tc"))).strip()
        if enc == CABECERA_MATRIZ_V08:
            n_apa += 1
            ok_bordes &= (estados["top"] == "single" and estados["bottom"] == "single"
                          and not any(estados[l] in ("single", "double", "thick")
                                      for l in ("left", "right", "insideV", "insideH")))
        else:
            n_rejilla += 1
            if not all(estados[l] == "single" for l in ("top", "left", "bottom", "right", "insideH", "insideV")):
                ok_bordes = False
                det_bordes.append(str(estados))
    chk("Tablas sin flotacion", ok_flo)
    chk("Todas las tablas al 100% del ancho util 8788 dxa (tblW = suma de tblGrid)", ok_ancho)
    chk("Sin anchos negativos o nulos ni sangrias de tabla (tblInd)", ok_neg and ok_ind)
    chk("Suma de tcW por fila = ancho de tabla (<= ancho util)", ok_filas)
    chk("Todas las filas con cantSplit", ok_cs)
    chk("Primera fila de cada tabla como encabezado repetido", ok_hd)
    chk("Sin ecuaciones OMML ni formulas en celdas", ok_math)
    chk(f"Bordes: formularios con rejilla cerrada ({n_rejilla}) y matrices con APA 7 ({n_apa})",
        ok_bordes and n_rejilla >= 12 and n_apa == 8, f"rejilla={n_rejilla} apa={n_apa} {det_bordes[:3]}")
    chk("Tablas nativas (sin imagenes)",
        len(body.xpath(".//w:drawing")) == 0 and len(body.xpath(".//w:pict")) == 0)

    # 4. Matriz de validacion de 8 columnas en vertical
    certs = [t for t in d.tables if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 8]
    chk("UNA sola matriz de validacion de 8 columnas a 8788 dxa", len(certs) == 1, str(len(certs)))
    if certs:
        t_val = certs[0]
        trs = t_val._tbl.findall(qn("w:tr"))
        chk("Matriz de validacion con 14 filas (2 encabezado + 12 elementos continuos)", len(trs) == 14, f"{len(trs)} filas")
        grid_w = [int(g.get(qn("w:w"))) for g in t_val._tbl.tblGrid.findall(qn("w:gridCol"))]
        chk("Geometria de 8 columnas coincide exactamente con anchos v08",
            grid_w == ANCHOS_MATRIZ_VALIDEZ_V08, str(grid_w))
        # Encabezado de dos filas repetido
        tr0_hd = trs[0].find(qn("w:trPr")).find(qn("w:tblHeader")) is not None
        tr1_hd = trs[1].find(qn("w:trPr")).find(qn("w:tblHeader")) is not None
        chk("Dos filas de encabezado repetidas (tblHeader)", tr0_hd and tr1_hd)
        # Numeracion 1 a 12 continua y celdas de calificacion vacias
        nums, elem_txts, celdas_llenas = [], [], 0
        for r_idx in range(2, len(trs)):
            tcs = trs[r_idx].findall(qn("w:tc"))
            nums.append(_txt(tcs[0]).strip())
            elem_txts.append(_txt(tcs[3]).strip())
            for c in (4, 5, 6, 7):
                if _txt(tcs[c]).strip():
                    celdas_llenas += 1
        chk("Numeracion continua de elementos 1 a 12 en matriz de validacion",
            nums == [str(i) for i in range(1, 13)], str(nums))
        chk("Casillas de evaluacion (Pertinencia, Relevancia, Claridad, Sugerencias) vacias",
            celdas_llenas == 0, f"{celdas_llenas} celdas con texto")
        esperado_elems = [norm(f[3]) for f in FILAS_MATRIZ_VALIDEZ_V08]
        chk("Enunciados de los 12 elementos corresponden fielmente a v08",
            [norm(x) for x in elem_txts] == esperado_elems)

    # 5. Cierre metodologico del juez validador
    chk("Titulo de la decision final presente",
        "DECISIÓN FINAL SOBRE LA APLICABILIDAD DEL INSTRUMENTO" in txt)
    chk("Cuatro opciones de opinion global presentes y en blanco",
        all(op in txt for op in ("[   ] Aplicable sin modificaciones",
                                 "[   ] Aplicable con modificaciones menores",
                                 "[   ] Requiere revisión y reestructuración sustancial",
                                 "[   ] No aplicable")))
    chk("Pregunta de suficiencia con casillas Si/No presentes",
        "¿Los elementos propuestos son suficientes para medir la variable en estudio?" in txt
        and "[   ] Sí          [   ] No" in txt)
    chk("Lineas de observaciones y datos del juez presentes",
        "Observaciones y recomendaciones generales:" in txt
        and "Apellidos y nombres del juez validador:" in txt
        and "DNI:" in txt and "Especialidad:" in txt
        and "Firma del juez validador" in txt)
    chk("UN unico bloque de cierre del juez validador",
        txt.count("Firma del juez validador") == 1
        and txt.count("Apellidos y nombres del juez validador:") == 1)

    # 6. Carta al juez experto
    chk("Carta con encabezado Señor(a) y Especialista",
        "Señor(a): ..........................................................." in txt
        and "Docente / Especialista en: ..........................................................." in txt)
    chk("Carta con titulo oficial de la tesis", TITULO_TESIS in txt)
    chk("Carta describe los tres instrumentos articulados (Ficha 01, Ficha 02, Cuestionario 03)",
        "Ficha N.° 01: Ficha de observación sistemática" in txt
        and "Ficha N.° 02: Ficha de registro y cotejo documental" in txt
        and "Cuestionario N.° 03: Cuestionario de satisfacción del usuario" in txt)
    chk("Carta anuncia los 5 adjuntos oficiales",
        "1.  Instrucciones para los jueces expertos" in txt
        and "2.  Matriz de validación de contenido por ítem/criterio" in txt
        and "3.  Matriz de consistencia metodológica institucional" in txt
        and "4.  Matriz de operacionalización de variables" in txt
        and "5.  Instrumentos de recolección de datos en blanco" in txt)

    # 7. Instrucciones para expertos
    chk("Instrucciones con Tabla 1 (Criterios) y Tabla 2 (Escala 1 a 4)",
        "Tabla 1. Criterios de evaluación" in txt
        and "Tabla 2. Escala de valoración" in txt
        and "Pertinencia" in txt and "Relevancia" in txt and "Claridad" in txt
        and "Cumple plenamente" in txt and "No cumple" in txt)
    chk("Cinco pautas metodologicas numeradas",
        all(f"{i}.  " in txt for i in range(1, 6)) and "V de Aiken" in txt)

    # 8. Matriz de consistencia
    hg_esperada = "La hipótesis general será contrastada a partir de la integración de los resultados obtenidos"
    chk("Hipotesis general con texto de integracion metodologica (sin regla de rechazo en tres hipotesis)",
        hg_esperada in txt and "Se acepta si se rechaza la hipótesis nula" not in txt)
    bloques_mc = [t for t in d.tables if len(t.columns) == 2 and t.rows
                  and _txt(t.rows[0]._tr).startswith(CABECERA_MATRIZ_V08 + "Bloque")]
    chk("Matriz de consistencia en 4 bloques verticales (general + 3 especificos) de 5 filas",
        len(bloques_mc) == 4 and all(len(t.rows) == 6 for t in bloques_mc), str(len(bloques_mc)))

    # 9. Operacionalizacion de variables
    chk("Operacionalizacion: VI X0/X1, escala dicotomica nominal, 3 dimensiones y 6 indicadores",
        "X0" in txt and "X1" in txt and "Dicotómica nominal" in txt
        and all(k in txt for k in ("Tiempo de registro (Treg)", "Tiempo de emisión de vale (Tvale)",
                                    "Registros sin discrepancias (RSD)",
                                    "Concordancia programada y entregada (CPE)",
                                    "Aceptación del proceso operativo (AP)", "Utilidad percibida (UP)",
                                    "1. Oportunidad de procesamiento", "2. Consistencia documental",
                                    "3. Satisfacción del usuario")))

    # 10. Ficha N.° 01
    chk("Ficha 01: Mediana (estadistico principal) y Promedio (descriptivo complementario)",
        txt.count("Mediana de las tres tareas (estadístico principal):") == 2
        and txt.count("Promedio (descriptivo complementario):") == 2
        and "Regla de pausa" in txt and "Firma del evaluador" in txt)
    capt = [t for t in d.tables if [c.text.strip() for c in t.rows[0].cells] == ENCABEZADOS_TAREA_V08]
    chk("Ficha 01: dos tablas de captura (3 REG + 3 VALE) con N.° y codigo en la misma celda",
        len(capt) == 2 and [r.cells[0].text.replace("\n", " ").strip() for t in capt for r in t.rows[1:]]
        == ["1 REG-01", "2 REG-02", "3 REG-03", "1 VALE-01", "2 VALE-02", "3 VALE-03"])

    # 11. Ficha N.° 02
    chk("Ficha 02: Unidad de analisis y documentos fuente en encabezado",
        "Unidad de análisis documental" in txt
        and "Movimiento individual de vacuna registrado en documento oficial" in txt
        and "Documentos fuente consultados" in txt
        and "Kardex físico, Pecosa física" in txt
        and "Módulo de movimientos de SIVAC" in txt)
    chk("Ficha 02: Criterio 4 con orden de pedido o nota de modificacion autorizada",
        "orden de pedido aprobada por la coordinación de inmunizaciones o con nota de modificación autorizada" in txt)
    chk("Ficha 02: nota de ampliacion del corpus y consolidados RSD y CPE",
        "si el corpus supera las filas disponibles" in txt and "RSD: ______ %" in txt and "CPE ______ %" in txt)

    # 12. Cuestionario N.° 03
    chk("Cuestionario 03: 8 reactivos reformulados de Modalidad A literales",
        all(norm(it) in nplano for it in ITEMS_AP_V08 + ITEMS_UP_V08))
    chk("Cuestionario 03: 8 reactivos de Modalidad B literales",
        all(norm(it) in nplano for it in ITEMS_PU + ITEMS_PE))
    chk("Cuestionario 03: Escala Likert de 5 opciones y rotulo Modalidad B",
        all(e in txt for e in ("Totalmente en Desacuerdo (TD)", "En Desacuerdo (D)",
                               "Ni de Acuerdo ni en Desacuerdo", "De Acuerdo (A)", "Totalmente de Acuerdo (TA)"))
        and ROTULO_MODALIDAD_B_V07 in txt and "ni se suma a la escala de satisfacción" in txt)
    chk("Numeracion del cuestionario (1 a 4) y firmas de Modalidad A y B independientes",
        "1. Instrucciones para el participante" in txt and "2. Datos generales del participante" in txt
        and "3. Modalidad A: satisfacción con el proceso operativo" in txt
        and "4. Modalidad B: módulo anexo de postest" in txt
        and txt.count("Firma del participante: ") == 2
        and txt.count("Firma del encuestador (Bach. José Luis Quispe León, Tesista):") == 2
        and "TRAB-______" in txt and "Fecha de aplicación postest: ____ / ____ / ______" in txt)

    # 13. Seguridad, verificabilidad y estilo
    chk("Fechas de aplicacion en blanco (dia/mes/año)",
        txt.count("______ / ______ / ______") >= 3
        and "Del ____ / ____ / ______  al  ____ / ____ / ______" in txt
        and not re.search(r"Fecha de (aplicación|la observación|ejecución)[^\n]*2025", txt))
    psico = [m for m in ("Alfa de Cronbach", "Omega de McDonald", "baremo", "tercil", "piloto", "puntaje global")
             if m.lower() in plano.lower()]
    chk("Sin baremos, alfa, omega, terciles ni piloto", not psico, str(psico))

    fuentes, tam = set(), set()
    for r in body.iter(qn("w:r")):
        rPr = r.find(qn("w:rPr"))
        if rPr is None or not _txt(r).strip():
            continue
        rf = rPr.find(qn("w:rFonts"))
        fuentes.add(rf.get(qn("w:ascii")) if rf is not None and rf.get(qn("w:ascii")) else "(heredada)")
        sz = rPr.find(qn("w:sz"))
        if sz is not None:
            tam.add(int(sz.get(qn("w:val"))) / 2)
    chk("Fuente Times New Roman exclusiva", fuentes <= FUENTES_OK, str(sorted(fuentes)))
    chk("Sin tamanos menores a 8.5 pt", all(x >= 8.5 for x in tam), str(sorted(tam)))
    chk("Sin sombreados ni colores distintos del negro",
        len(body.xpath(".//w:shd[@w:fill and @w:fill!='auto' and @w:fill!='FFFFFF']")) == 0 and
        all(c.get(qn("w:val")).upper() in ("000000", "AUTO") for c in body.iter(qn("w:color"))))
    chk("Prohibicion absoluta del guion largo / raya (U+2014)", "—" not in txt)
    hall = [p for p in PROHIBIDOS if re.search(p, txt)]
    chk("Sin metadatos internos, contactos ni rayas", not hall, str(hall))
    chk("Sin marcas X ni calificaciones prellenadas", not re.search(r"\[\s*[xX]\s*\]", txt) and "×" not in txt)

    return res


def verificar_pdf_v08(pdf):
    """Paginacion del PDF v08: todas las paginas verticales, marcadores
    presentes, sin paginas vacias ni huerfanas, total <= 16 (objetivo <= 14)."""
    import pymupdf

    def _norma(s):
        return re.sub(r"\s+", " ", s).strip().lower()

    doc = pymupdf.open(str(pdf))
    res = []
    textos = [p.get_text() for p in doc]
    res.append(("Todas las paginas A4 vertical (ancho<alto)", all(p.rect.width < p.rect.height for p in doc), ""))
    inicios = []
    for t in textos:
        lineas = [l.strip() for l in t.splitlines() if l.strip()]
        if lineas and re.fullmatch(r"\d+", lineas[0]):
            lineas = lineas[1:]
        inicios.append(_norma(" ".join(lineas[:3])) if lineas else "")
    res.append(("Sin paginas vacias", not [i + 1 for i, t in enumerate(textos) if len(t.strip()) < 30], ""))
    for m in MARCADORES_V08:
        pg = next((i for i, ini in enumerate(inicios) if ini.startswith(_norma(m))), None)
        res.append((f"'{m[:48]}' abre pagina" + (f" {pg + 1}" if pg is not None else ""), pg is not None, ""))
    firma = next((i for i, t in enumerate(textos) if _norma("Firma del juez validador") in _norma(t)), None)
    res.append(("Cierre unico del juez dentro de la matriz de validez", firma is not None and firma <= 5,
                f"pagina {firma + 1 if firma is not None else None}"))
    pobres = [i + 1 for i, t in enumerate(textos)
              if len([l for l in t.splitlines() if l.strip() and not re.fullmatch(r"\s*\d+\s*", l)]) <= 3]
    res.append(("Sin paginas con 3 lineas o menos (huerfanas)", not pobres, str(pobres)))
    res.append(("Total de paginas <= 16 (objetivo <= 14)", 10 <= len(doc) <= 16, str(len(doc))))
    return res


def generar_v08(sobrescribir=True):
    import shutil
    DIR_V08.mkdir(parents=True, exist_ok=True)
    rutas = [DIR_V08 / nombre_v08(n) for n in (1, 2, 3)]
    existentes = [r for r in rutas if r.exists()]
    if existentes and not sobrescribir:
        for r in existentes:
            print(f"[OMITIDO] {r.name} ya existe; no se sobrescribe")
        return 0
    maestro = rutas[0]
    construir_v08().save(str(maestro))
    res = verificar_v08(maestro)
    malos = [r for r in res if not r[1]]
    if malos:
        print(f"[ABORTADO] {maestro.name}: {len(malos)} comprobaciones no conformes; archivo eliminado")
        for nom, _, det in malos:
            print(f"   FALLA {nom} {det}")
        if maestro.exists():
            maestro.unlink()
        return 1
    print(f"[OK] {maestro.name} ({maestro.stat().st_size:,} bytes): {len(res)} comprobaciones conformes")
    for r in rutas[1:]:
        shutil.copyfile(maestro, r)
        print(f"[OK] {r.name} copia byte-identica del ejemplar 01 ({r.stat().st_size:,} bytes)")
    return 0


# ============================================================ PERFIL MIXTO v09
# Arquitectura de secciones mixta:
#   - Sección 1: A4 vertical retrato (8788 dxa) para Carta, Instrucciones y
#     Matriz de Validación continua (8 cols) con Decisión Final y Firma del Juez.
#   - Sección 2: A4 horizontal apaisada (14000 dxa) para Matriz de Consistencia
#     (5 cols) y Matriz de Operacionalización (6 cols) con bordes académicos APA 7.
#   - Sección 3: A4 vertical retrato (8788 dxa) para Ficha N.° 01, Ficha N.° 02 y
#     Cuestionario N.° 03 (Modalidad A y Modalidad B).
# Incorpora los 5 ajustes metodológicos críticos del tesista:
# 1. Separación de Modalidad B (carta con frase "tres dimensiones definidas para
#    la variable dependiente" y Modalidad B como anexo técnico no aditivo; matriz
#    de validación con 12 elementos estrictos de la VD).
# 2. Corrección sobre V de Aiken (eliminado "concordancia entre jueces", añadido
#    cálculo por elemento/criterio y criterio de decisión V >= 0.80).
# 3. Tarea estandarizada representativa única en Ficha 01 (Opción B): salida
#    programada de 3 biológicos para Treg (REG-E1..E3) y emisión de vale oficial
#    para Tvale (VALE-E1..E3), con mediana principal y promedio por operador.
# 4. Ficha 02: Unidad de análisis documental y unidad de análisis para contraste
#    estadístico pareado de Wilcoxon (n = 14 operadores, TRAB-01 a TRAB-14).
# 5. Criterio 4 de RSD perfeccionado: cantidad concordante con documento fuente
#    (entradas: acta/guía/recepción; salidas: orden/vale/nota de modificación;
#    ajustes: autorización correspondiente).
# 6. Reactivos atómicos de satisfacción (Modalidad A, AP-01..04 y UP-01..04).
# 7. Formato APA 7 estricto en matrices (cero líneas verticales, 3 líneas horizontales).

VERSION_V09 = "v09"
DIR_V09 = RUTA_SALIDA / "expediente_v09"

ANCHOS_MC_V09 = [2300, 2300, 2300, 3550, 3550]        # suma exacta 14000 dxa (apaisada)
ANCHOS_OPER_V09 = [2300, 2200, 2300, 3800, 1700, 1700]  # suma exacta 14000 dxa (apaisada)
ENCABEZADOS_MC_V09 = ["Problemas", "Objetivos", "Hipótesis", "Variable / dimensiones", "Indicadores"]
ENCABEZADOS_OPER_V09 = ["Variable", "Dimensión", "Indicador", "Definición operacional", "Escala", "Instrumento"]

assert sum(ANCHOS_MC_V09) == ANCHO_APAISADA
assert sum(ANCHOS_OPER_V09) == ANCHO_APAISADA

ITEMS_AP_V09 = [
    "El procedimiento para registrar los movimientos diarios de vacunas se realiza de forma ágil.",
    "El trámite para emitir comprobantes de salida y vales de entrega se efectúa sin demoras innecesarias.",
    "El procedimiento utilizado facilita conciliar los saldos de vacunas entre el centro de acopio y los establecimientos de salud.",
    "El tiempo destinado a gestionar los movimientos de vacunas es compatible con mis demás actividades laborales.",
]

ITEMS_UP_V09 = [
    "El procedimiento de registro permite disponer oportunamente de información actualizada sobre los saldos de vacunas.",
    "El procedimiento de emisión de comprobantes facilita la asignación correcta de los biológicos solicitados.",
    "El procedimiento de conciliación facilita identificar y sustentar documentalmente las diferencias entre las cantidades programadas y entregadas.",
    "El procedimiento de gestión facilita el seguimiento oportuno de las existencias de vacunas en los establecimientos de salud.",
]

CRITERIOS_RSD_V09 = [
    "Tipo de movimiento clasificado de forma unívoca (entrada por remesa, salida a establecimiento o ajuste).",
    "Denominación oficial estandarizada del biológico según el esquema regular nacional.",
    "Identificación exacta del número de lote, coincidente con el rótulo del frasco.",
    "Cantidad registrada concordante con el documento fuente que sustenta el movimiento. En entradas, se verifica la concordancia con el acta, guía de remisión o documento de recepción; en salidas, con la orden de pedido, vale autorizado o nota de modificación; y en ajustes, con el documento de autorización correspondiente.",
    "Fecha del movimiento consignada completa (día, mes y año) y en secuencia cronológica.",
    "Establecimiento de origen o destino individualizado con su código oficial.",
    "Nombre, firma o usuario responsable del despacho o recepción plenamente trazable.",
    "Documento formal de respaldo asociado y verificado (vale oficial, PECOSA o guía de remisión).",
]

FILAS_MATRIZ_VALIDEZ_V09 = [
    (
        "1",
        "Ficha N.° 01\n(Tiempos)",
        "Oportunidad:\nTreg",
        "Tiempo de registro de movimientos de vacunas: cronometraje de la tarea estandarizada representativa única (registro de salida programada de tres biológicos con lote, cantidad, fecha, destino y responsable), evaluada mediante tres ensayos homogéneos (REG-E1, REG-E2, REG-E3) por operador, desde que toma el documento fuente o abre la digitación hasta que el movimiento queda grabado con saldo actualizado, expresado en minutos decimales (mediana por operador).",
    ),
    (
        "2",
        "Ficha N.° 01\n(Tiempos)",
        "Oportunidad:\nTvale",
        "Tiempo de emisión de vales de salida: cronometraje de la tarea estandarizada representativa única (emisión de vale oficial para salida programada de tres biológicos a un establecimiento de salud), evaluada mediante tres ensayos homogéneos (VALE-E1, VALE-E2, VALE-E3) por operador, desde que recibe o abre la solicitud de pedido hasta que el comprobante de salida queda generado y disponible para su entrega, impresión o registro institucional, expresado en minutos decimales (mediana por operador).",
    ),
    (
        "3",
        "Ficha N.° 02\n(Cotejo)",
        "Consistencia:\nRSD",
        "Porcentaje de registros sin discrepancias (RSD): proporción de movimientos auditados que cumplen simultáneamente los ocho criterios de conformidad (tipo, biológico, lote, cantidad registrada concordante con el documento fuente que sustenta el movimiento, fecha, establecimiento, responsable y documento de respaldo formal). Se audita un corpus documental por operador y se consolida un porcentaje por cada uno de los 14 operadores para el contraste pareado de Wilcoxon.",
    ),
    (
        "4",
        "Ficha N.° 02\n(Cotejo)",
        "Consistencia:\nCPE",
        "Concordancia entre cantidad programada y entregada (CPE): proporción de entregas en las que la cantidad entregada coincide exactamente con la programada o cuenta con justificación documental autorizada. Se audita el corpus de entregas por operador y se consolida un porcentaje por cada uno de los 14 operadores para el contraste pareado de Wilcoxon.",
    ),
    (
        "5",
        "Cuestionario\nN.° 03",
        "Satisfacción:\nAP-01",
        ITEMS_AP_V09[0],
    ),
    (
        "6",
        "Cuestionario\nN.° 03",
        "Satisfacción:\nAP-02",
        ITEMS_AP_V09[1],
    ),
    (
        "7",
        "Cuestionario\nN.° 03",
        "Satisfacción:\nAP-03",
        ITEMS_AP_V09[2],
    ),
    (
        "8",
        "Cuestionario\nN.° 03",
        "Satisfacción:\nAP-04",
        ITEMS_AP_V09[3],
    ),
    (
        "9",
        "Cuestionario\nN.° 03",
        "Satisfacción:\nUP-01",
        ITEMS_UP_V09[0],
    ),
    (
        "10",
        "Cuestionario\nN.° 03",
        "Satisfacción:\nUP-02",
        ITEMS_UP_V09[1],
    ),
    (
        "11",
        "Cuestionario\nN.° 03",
        "Satisfacción:\nUP-03",
        ITEMS_UP_V09[2],
    ),
    (
        "12",
        "Cuestionario\nN.° 03",
        "Satisfacción:\nUP-04",
        ITEMS_UP_V09[3],
    ),
]

MARCADORES_V09 = [
    f"Andahuaylas, ........ de ........................ de {ANIO}",
    "INSTRUCCIONES PARA LA VALIDACIÓN POR JUICIO DE EXPERTOS",
    "MATRIZ DE VALIDACIÓN DE CONTENIDO POR JUICIO DE EXPERTOS",
    "MATRIZ DE CONSISTENCIA",
    "MATRIZ DE OPERACIONALIZACIÓN DE VARIABLES",
    "INSTRUMENTO N.° 01",
    "INSTRUMENTO N.° 02",
    "INSTRUMENTO N.° 03",
]

NOTA_METODOLOGIA_V09 = (
    "Nota. Metodología: investigación aplicada, enfoque cuantitativo, nivel explicativo; diseño preexperimental "
    "con pretest y postest en un solo grupo (O1, X, O2); población y muestra censal, N = n = 14 operadores; "
    "técnicas e instrumentos: observación sistemática (Ficha N.° 01), cotejo documental (Ficha N.° 02) y "
    "encuesta (Cuestionario N.° 03); validez de contenido por juicio de expertos y confiabilidad estimada con "
    "los datos del estudio. El análisis inferencial incluirá la evaluación de normalidad de las diferencias "
    "pretest-postest mediante la prueba de Shapiro-Wilk. Considerando el tamaño muestral de 14 participantes y el "
    "carácter pareado de las mediciones, la contrastación de hipótesis se realizará mediante la prueba no paramétrica "
    "de rangos con signo de Wilcoxon, con un nivel de significancia de 0.05."
)


def _filas_mc_v09():
    """Filas literales de la matriz de consistencia v09 con la hipótesis general
    ajustada por mandato metodológico del tesista (análisis conjunto e integración)."""
    d1, d2, d3 = _mc("oportunidad de procesamiento"), _mc("consistencia documental"), _mc("satisfacción del usuario")
    hg_v09 = (
        "Hipótesis general:\n"
        f"La aplicación del sistema \"SIVAC\" mejora significativamente la gestión de movimientos mensuales de vacunas {SUJ}, Andahuaylas 2025.\n"
        "La hipótesis general será contrastada a partir de la integración de los resultados obtenidos en las tres "
        "dimensiones específicas (oportunidad, consistencia y satisfacción), mediante un análisis conjunto de la "
        "significancia estadística y el tamaño del efecto en cada indicador."
    )
    return [
        ["Problema general:\n" + MC_PG,
         "Objetivo general:\nDeterminar en qué medida la aplicación del sistema \"SIVAC\" mejora la gestión de "
         f"movimientos mensuales de vacunas {SUJ}, Andahuaylas 2025.",
         hg_v09,
         "Variable independiente:\nSistema web SIVAC.\nCondición X0 (pretest): ausencia del sistema; gestión "
         "manual tradicional.\nCondición X1 (postest): presencia y uso del sistema SIVAC.",
         "Escala: dicotómica nominal (0 = pretest, 1 = postest).\nSustento técnico: metodología Extreme "
         "Programming y calidad ISO/IEC 25010:2023."],
        ["Problema específico 1:\n" + d1[0], "Objetivo específico 1:\n" + d1[1],
         "Hipótesis específica 1:\n" + d1[2],
         "Variable dependiente:\nGestión de movimientos mensuales de vacunas.\nDimensión 1: oportunidad de procesamiento.",
         "• Tiempo de registro de movimientos (Treg), en minutos decimales, escala de razón (tarea estandarizada única en tres ensayos homogéneos).\n"
         "• Tiempo de emisión de vales (Tvale), en minutos decimales, escala de razón (tarea estandarizada única en tres ensayos homogéneos).\n"
         "Instrumento: Ficha N.° 01."],
        ["Problema específico 2:\n" + d2[0], "Objetivo específico 2:\n" + d2[1],
         "Hipótesis específica 2:\n" + d2[2],
         "Dimensión 2: consistencia documental.",
         "• Registros sin discrepancias (RSD), en porcentaje, escala de razón (ocho criterios de conformidad, con cantidad concordante con documento fuente).\n"
         "• Concordancia entre cantidad programada y entregada (CPE), en porcentaje acotado entre 0 y 100.\n"
         "Instrumento: Ficha N.° 02 (consolidado por operador, n = 14 observaciones pareadas de Wilcoxon)."],
        ["Problema específico 3:\n" + d3[0], "Objetivo específico 3:\n" + d3[1],
         "Hipótesis específica 3:\n" + d3[2],
         "Dimensión 3: satisfacción del usuario (satisfacción con el proceso).",
         "• Aceptación del proceso operativo (AP), 4 reactivos atómicos, 4 a 20 puntos.\n"
         "• Utilidad percibida (UP), 4 reactivos atómicos, 4 a 20 puntos.\nTotal: 8 reactivos, 8 a 40 puntos, escala Likert de 1 a 5.\n"
         "Instrumento: Cuestionario N.° 03, Modalidad A (Modalidad B como anexo descriptivo de postest)."],
    ]


def _filas_operacionalizacion_v09():
    """Filas de la matriz de operacionalización v09 con tareas estandarizadas únicas
    y criterio 4 de RSD perfeccionado."""
    return [
        ["Variable independiente:\nSistema web SIVAC", "Intervención tecnológica", "X0: gestión manual (pretest).\n"
         "X1: gestión con SIVAC (postest).", "Presencia o ausencia del sistema.", "Dicotómica nominal", "Capítulo III"],
        ["Variable dependiente:\nGestión de movimientos mensuales de vacunas", "1. Oportunidad de procesamiento",
         "Tiempo de registro (Treg)", "Minutos transcurridos entre el inicio y el fin del registro de la tarea "
         "estandarizada representativa única (tres ensayos homogéneos por operador).",
         "Minutos decimales, razón", "Ficha N.° 01 (tres ensayos por operador)"],
        ["", "", "Tiempo de emisión de vale (Tvale)", "Minutos entre la solicitud y la emisión del comprobante "
         "oficial de salida para la tarea estandarizada única (tres ensayos homogéneos por operador).",
         "Minutos decimales, razón", "Ficha N.° 01 (tres ensayos por operador)"],
        ["", "2. Consistencia documental", "Registros sin discrepancias (RSD)",
         "Porcentaje de registros que cumplen simultáneamente los ocho criterios de conformidad (con cantidad "
         "concordante con documento fuente que sustenta el movimiento).",
         "Porcentaje, razón", "Ficha N.° 02 (40 a 60 registros por ventana de 30 días; consolidado por operador)"],
        ["", "", "Concordancia entre cantidad programada y entregada (CPE)",
         "Porcentaje de entregas cuya cantidad entregada coincide con la programada o cuenta con justificación documental autorizada.",
         "Porcentaje entre 0 y 100, razón", "Ficha N.° 02 (40 a 60 entregas por ventana de 30 días; consolidado por operador)"],
        ["", "3. Satisfacción del usuario", "Aceptación del proceso operativo (AP)",
         "Conformidad con la agilidad, fluidez y carga de trabajo del procedimiento (4 reactivos atómicos, 4 a 20 puntos).",
         "Likert de 1 a 5, ordinal", "Cuestionario N.° 03, Modalidad A"],
        ["", "", "Utilidad percibida (UP)",
         "Percepción de oportunidad informativa, asignación correcta de biológicos, sustento documental y seguimiento de existencias (4 reactivos atómicos, 4 a 20 puntos).",
         "Likert de 1 a 5, ordinal", "Cuestionario N.° 03, Modalidad A"],
    ]


def v09_carta(doc):
    par(doc, f"Andahuaylas, ........ de ........................ de {ANIO}", align="right", size=10, after=2, line=1.0)
    par(doc, "Señor(a): ...........................................................", size=10.5, bold=True, after=0, line=1.0)
    par(doc, "Docente / Especialista en: ...........................................................", size=10, italic=True, after=2, line=1.0)
    par(doc, "Presente.-", size=10.5, after=3, line=1.0)
    par(doc, "De mi mayor consideración:", size=10.5, after=2, line=1.0)
    par(doc, f"Yo, {TESISTA}, tesista de la Escuela Profesional de Ingeniería de Sistemas de la Universidad "
             "Nacional José María Arguedas, me dirijo a usted con el debido respeto para solicitarle su valiosa "
             "colaboración como juez experto en la validación de contenido del conjunto de instrumentos de "
             "recolección de datos diseñados para medir la variable dependiente “Gestión de movimientos mensuales de vacunas”, "
             f"en el marco de la investigación titulada “{TITULO_TESIS}”.",
        align="both", first=1.27, size=10, after=2, line=1.15)
    par(doc, "La investigación articula tres instrumentos complementarios orientados a capturar con rigurosidad "
             "técnica y objetiva las tres dimensiones definidas para la variable dependiente:",
        align="both", first=1.27, size=10, after=1, line=1.15)
    par(doc, "1.  Ficha N.° 01: Ficha de observación sistemática y medición de tiempos cronometrados, destinada a "
             "cuantificar la dimensión Oportunidad de procesamiento mediante el registro de tiempos netos de registro "
             "(Treg) y de emisión de comprobantes de salida o vales (Tvale) a través de una tarea estandarizada representativa "
             "única evaluada en tres ensayos homogéneos.",
        align="both", hanging=0.8, size=9.5, after=1, line=1.1)
    par(doc, "2.  Ficha N.° 02: Ficha de registro y cotejo documental de consistencia, destinada a evaluar la "
             "dimensión Consistencia documental mediante los indicadores registros sin discrepancias (RSD) y "
             "concordancia entre cantidades programadas y entregadas (CPE). Cada movimiento o entrega constituye "
             "una unidad de registro documental; posteriormente, los resultados se consolidan en porcentajes por "
             "operador para el contraste estadístico pretest–postest.",
        align="both", hanging=0.8, size=9.5, after=1, line=1.1)
    par(doc, "3.  Cuestionario N.° 03: Cuestionario de satisfacción con el proceso operativo, Modalidad A, "
             "compuesto por ocho reactivos en escala Likert de cinco categorías, destinado a medir la dimensión "
             "Satisfacción del usuario. Se acompaña la Modalidad B como anexo complementario de consulta técnica para "
             "la evaluación descriptiva postest de la aceptación del software SIVAC, considerando los constructos de "
             "utilidad percibida y facilidad de uso percibida del modelo TAM, sin formar parte de la escala de la "
             "variable dependiente.",
        align="both", hanging=0.8, size=9.5, after=2, line=1.1)
    par(doc, "La labor pericial solicitada consiste en evaluar la pertinencia, relevancia y claridad de cada uno de los "
             "elementos, criterios y reactivos que evalúan la variable dependiente mediante la matriz de validación adjunta, "
             "empleando una escala de valoración del 1 al 4. Con tal propósito, se adjuntan los siguientes documentos oficiales:",
        align="both", first=1.27, size=10, after=1, line=1.15, keep_next=True)
    adjuntos = [
        "Instrucciones para los jueces expertos y criterios de evaluación.",
        "Matriz de validación de contenido por ítem/criterio (escala de valoración del 1 al 4, con decisión final sobre aplicabilidad).",
        "Matriz de consistencia metodológica institucional (documento de consulta técnica; no se llena).",
        "Matriz de operacionalización de variables con las 3 dimensiones y 6 indicadores (documento de consulta; no se llena).",
        "Instrumentos de recolección de datos en blanco: Ficha N.° 01, Ficha N.° 02 y Cuestionario N.° 03 (Modalidad A para la variable dependiente y Modalidad B como anexo descriptivo de postest; no se llenan).",
    ]
    for i, adj in enumerate(adjuntos, start=1):
        par(doc, f"{i}.  {adj}", hanging=0.8, size=9.5, after=1, line=1.05, align="both")
    par(doc, "Agradezco de antemano su tiempo, rigor académico y valioso aporte al desarrollo de esta investigación.",
        before=1, first=1.27, size=10, after=3, line=1.15)
    par(doc, "Atentamente,", align="center", size=10, after=8, line=1.0)
    par(doc, "..........................................................", align="center", size=10, line=1.0)
    par(doc, TESISTA, align="center", bold=True, size=10, line=1.0)
    par(doc, "Tesista", align="center", size=10, line=1.0)


def v09_instrucciones(doc):
    par(doc, "INSTRUCCIONES PARA LA VALIDACIÓN POR JUICIO DE EXPERTOS", bold=True, align="center", pbb=True, size=11, after=2, line=1.1)
    par(doc, "Estimado(a) especialista, a continuación se detallan los criterios de evaluación, la escala de valoración "
             "y las pautas metodológicas que guiarán la revisión pericial del conjunto de instrumentos:",
        align="both", size=9.5, after=2, line=1.1)
    par(doc, "Tabla 1. Criterios de evaluación", bold=True, size=9.5, before=1, after=1, keep_next=True)
    v08_tabla(doc, ["Criterio", "Definición operativa"], [
        ["Pertinencia", "El elemento, criterio o reactivo se encuentra estrechamente vinculado con el constructo teórico y la dimensión que pretende medir."],
        ["Relevancia", "El elemento, criterio o reactivo es fundamental y aporta significativamente a la medición representativa del indicador correspondiente."],
        ["Claridad", "La redacción del enunciado o definición es concisa, directa, comprensible y no genera ambigüedades interpretativas."],
    ], [1900, ANCHO_RETRATO - 1900], margen=(20, 45, 20, 45))
    _v08_aire(doc, 2)
    par(doc, "Tabla 2. Escala de valoración", bold=True, size=9.5, before=1, after=1, keep_next=True)
    v08_tabla(doc, ["Nivel", "Denominación", "Descripción operativa"], [
        ["1", "No cumple", "El elemento, criterio o reactivo no cumple con el criterio de evaluación; debe ser descartado o reformulado en su totalidad."],
        ["2", "Cumple parcialmente;\nrequiere modificación mayor", "El elemento, criterio o reactivo cumple de forma deficiente; requiere reestructuración sustancial antes de su aplicación."],
        ["3", "Cumple;\nrequiere modificación menor", "El elemento, criterio o reactivo cumple satisfactoriamente con el criterio evaluado, aunque es susceptible de mejoras puntuales de redacción o estilo."],
        ["4", "Cumple plenamente", "El elemento, criterio o reactivo satisface con total rigurosidad, precisión y exactitud el criterio evaluado; no requiere modificaciones."],
    ], [800, 2600, ANCHO_RETRATO - 3400], alinear=["center", "left", "left"], margen=(20, 45, 20, 45))
    par(doc, "Pautas metodológicas para la validación:", bold=True, size=9.5, before=2, after=1, keep_next=True)
    pautas = [
        "Consigne en cada casilla de la Matriz de Validación una calificación numérica del 1 al 4, conforme a la escala de valoración descrita.",
        "Revise detenidamente las definiciones operacionales y los instrumentos en blanco adjuntos como material de consulta; estos últimos no deben ser llenados.",
        "En la columna “Observaciones y sugerencias”, formule las recomendaciones cualitativas que considere pertinentes para perfeccionar los reactivos y criterios evaluados.",
        "En la sección final, emita su opinión global sobre la aplicabilidad del conjunto de instrumentos, indique si los elementos propuestos son suficientes para medir la variable y registre sus observaciones generales.",
        "Consigne sus datos profesionales completos (apellidos y nombres, DNI, especialidad, fecha) y suscriba la matriz con su firma. Devuelva el expediente al tesista para el procesamiento de la validez de contenido mediante el coeficiente V de Aiken, calculado para cada elemento y criterio de evaluación.",
    ]
    for i, p in enumerate(pautas, start=1):
        par(doc, f"{i}.  {p}", hanging=0.8, size=9.0, after=1, line=1.05, align="both")
    par(doc, "Criterio de decisión para la validez de contenido: Se considerará que un elemento, criterio o reactivo "
             "presenta validez de contenido adecuada cuando el coeficiente V de Aiken alcance o supere el valor mínimo "
             "establecido para la investigación (V >= 0.80). El valor mínimo de V de Aiken será interpretado conjuntamente "
             "con las observaciones cualitativas de los jueces expertos. Los elementos con valores inferiores a 0.80 serán "
             "revisados, reformulados o excluidos, según corresponda.",
        size=9.0, line=1.05, before=2, after=0, align="both")


def v09_decision_final_cierre(doc):
    """Cierre metodológico del juez validador para v09: decisión sobre aplicabilidad,
    suficiencia de los ítems, observaciones generales y datos del experto con firma."""
    return v08_decision_final_cierre(doc)


def v09_matriz_validacion(doc):
    par(doc, "MATRIZ DE VALIDACIÓN DE CONTENIDO POR JUICIO DE EXPERTOS", bold=True, align="center", pbb=True, after=2)
    par(doc, "CONJUNTO DE INSTRUMENTOS DE LA VARIABLE DEPENDIENTE: GESTIÓN DE MOVIMIENTOS MENSUALES DE VACUNAS",
        bold=True, align="center", size=11, line=1.15, after=2)
    par(doc, "Instrucción pericial: califique cada elemento en las columnas Pertinencia, Relevancia y Claridad con valores del 1 al 4. "
             "En Oportunidad y Consistencia se evalúan las especificaciones de las fichas operativas; en Satisfacción se evalúan los reactivos del cuestionario.",
        align="center", size=9.5, italic=True, line=1.0, after=4)

    anchos = ANCHOS_MATRIZ_VALIDEZ_V08
    t = doc.add_table(rows=2 + len(FILAS_MATRIZ_VALIDEZ_V09), cols=8)
    quir.configurar_geometria_tabla(t, ANCHO_RETRATO, anchos, align="center", cell_margin_dxa=(20, 35, 20, 35))
    quir.aplicar_bordes_rejilla(t)
    fany.fijar_disposicion_fija(t)

    # Merges verticales para cols 0, 1, 2, 3, 7
    for c in (0, 1, 2, 3, 7):
        celda = t.cell(0, c).merge(t.cell(1, c))
        celda.width = Cm(anchos[c] / 567.0)

    # Merge horizontal para cols 4, 5, 6 en fila 0
    celda_crit = t.cell(0, 4).merge(t.cell(0, 6))
    celda_crit.width = Cm((anchos[4] + anchos[5] + anchos[6]) / 567.0)

    fany.texto_celda(t.cell(0, 0), "N.°", tamano=9.5, negrita=True, alineacion="center")
    fany.texto_celda(t.cell(0, 1), "Instrumento", tamano=9.5, negrita=True, alineacion="center")
    fany.texto_celda(t.cell(0, 2), "Dimensión /\nindicador", tamano=9.5, negrita=True, alineacion="center")
    fany.texto_celda(t.cell(0, 3), "Elemento, criterio o reactivo", tamano=9.5, negrita=True, alineacion="center")
    fany.texto_celda(celda_crit, "Criterios de evaluación (Escala 1 a 4)", tamano=9.5, negrita=True, alineacion="center")
    fany.texto_celda(t.cell(0, 7), "Observaciones y sugerencias", tamano=9.5, negrita=True, alineacion="center")

    fany.texto_celda(t.cell(1, 4), "Pertinencia\n(1–4)", tamano=8.5, negrita=True, alineacion="center")
    fany.texto_celda(t.cell(1, 5), "Relevancia\n(1–4)", tamano=8.5, negrita=True, alineacion="center")
    fany.texto_celda(t.cell(1, 6), "Claridad\n(1–4)", tamano=8.5, negrita=True, alineacion="center")

    for idx, fila_datos in enumerate(FILAS_MATRIZ_VALIDEZ_V09, start=2):
        num_str, inst, dim_ind, elem = fila_datos
        fany.texto_celda(t.cell(idx, 0), num_str, tamano=9.0, alineacion="center")
        fany.texto_celda(t.cell(idx, 1), inst, tamano=8.5, alineacion="center")
        fany.texto_celda(t.cell(idx, 2), dim_ind, tamano=8.5, alineacion="center")
        fany.texto_celda(t.cell(idx, 3), elem, tamano=9.0, alineacion="both", before=3, after=3, margen_izq_dxa=30)
        for c in (4, 5, 6, 7):
            fany.fijar_contenido_celda(t.cell(idx, c), fany._p_vacio())

    fany.normalizar_celdas_sin_parrafo(t)
    for row in t.rows:
        for cell in row.cells:
            cell.vertical_alignment = fany.WD_ALIGN_VERTICAL.CENTER
    quir.blindar_filas_tabla(t, cant_split=True, repetir_encabezado=True, filas_encabezado=2)
    quir.normalizar_orden_tblPr(t)

    # Cierre del juez (opinión global, suficiencia, observaciones y firma) en Sección 1
    v09_decision_final_cierre(doc)


def v09_matriz_consistencia(doc):
    """Matriz de consistencia completa en formato académico APA 7 a 14000 dxa (apaisada)."""
    par(doc, "MATRIZ DE CONSISTENCIA", bold=True, align="center", after=2, pbb=True)
    par(doc, TITULO_TESIS, italic=True, align="center", size=TAM_TABLA, line=1.0, after=6)
    filas = _filas_mc_v09()
    tabla(doc, ENCABEZADOS_MC_V09, filas, ANCHOS_MC_V09, ANCHO_APAISADA)
    par(doc, NOTA_METODOLOGIA_V09, size=9.5, line=1.0, before=4, italic=True, align="both")


def v09_operacionalizacion(doc):
    """Matriz de operacionalización completa en formato académico APA 7 a 14000 dxa (apaisada)."""
    par(doc, "MATRIZ DE OPERACIONALIZACIÓN DE VARIABLES", bold=True, align="center", after=6, pbb=True)
    filas = _filas_operacionalizacion_v09()
    tabla(doc, ENCABEZADOS_OPER_V09, filas, ANCHOS_OPER_V09, ANCHO_APAISADA)
    par(doc, "Nota. Las fórmulas de cálculo de los indicadores se presentan en el cuerpo narrativo del Capítulo IV.",
        size=TAM_TABLA, line=1.0, before=6, italic=True)


def v09_ficha01(doc):
    par(doc, "INSTRUMENTO N.° 01", bold=True, align="center", after=0, pbb=True)
    par(doc, "FICHA DE OBSERVACIÓN SISTEMÁTICA Y MEDICIÓN DE TIEMPOS CRONOMETRADOS",
        bold=True, align="center", after=3)
    par(doc, "Dimensión: oportunidad de procesamiento. Indicadores: tiempo de registro (Treg) y tiempo de emisión "
             "de vale (Tvale). Formulario en blanco para captura objetiva de campo; no se llena durante la "
             "validación y sus campos no constituyen escalas de percepción.", align="both", size=10, line=1.15,
        after=3)
    par(doc, "1. Datos generales de la observación", bold=True, before=3, after=2, keep_next=True)
    v08_tabla(doc, ["Campo", "Registro"], [
        ["Código del operador evaluado", "TRAB-____  (TRAB-01 a TRAB-14)"],
        ["Rol institucional", "[  ] Responsable de centro de acopio o red de frío   [  ] Personal de estrategia "
                              "sanitaria de inmunizaciones"],
        ["Centro de acopio o sede / red o microred", "____________________________     Provincia:   "
                                                     "[  ] Andahuaylas   [  ] Chincheros"],
        ["Momento de medición", "[  ] Pretest (kardex físico, libros de registro y hojas de cálculo)   "
                                "[  ] Postest (sistema web SIVAC)"],
        ["Fecha de la observación", "______ / ______ / ______"],
        ["Evaluador principal", TESISTA + "     Secundario (si aplica): ______________________"],
    ], [3000, ANCHO_RETRATO - 3000])
    par(doc, "2. Protocolo de cronometraje y reglas de registro", bold=True, before=3, after=1, keep_next=True)
    for s in [
        "Cronómetro digital con precisión de centésimas de segundo; cada tiempo se consigna en minutos "
        "decimales (minutos enteros más la fracción de segundos sobre sesenta).",
        "Tiempo de registro: inicia al tomar el documento fuente o abrir la digitación y termina cuando el "
        "movimiento queda grabado o asentado con saldo actualizado.",
        "Tiempo de emisión de vales: inicia cuando el operador recibe o abre la solicitud de pedido y termina "
        "cuando el vale o comprobante de salida ha sido generado y queda disponible para su entrega, impresión "
        "o registro institucional, conforme al procedimiento aplicable en cada momento de medición.",
        "Regla de pausa: ante una interrupción externa fortuita el cronómetro se detiene y se reanuda al "
        "normalizarse la tarea; se registra solo el tiempo neto efectivo. La batería consta de tres ensayos "
        "homogéneos de la tarea estandarizada representativa única para registro y tres para emisión por operador; "
        "la mediana de los tres ensayos consolida el desempeño por operador como estadístico principal, reportándose "
        "el promedio como descriptivo complementario.",
        "Los tres ensayos se realizarán con casos equivalentes en complejidad, cantidad de biológicos, datos "
        "requeridos y flujo operativo, pero con datos documentales diferentes. Se utilizarán formatos o casos "
        "previamente preparados para evitar que la repetición inmediata de un mismo caso genere sesgos por memoria, "
        "familiarización o aprendizaje.",
        "El orden de los tres ensayos será el mismo en pretest y postest para todos los participantes.",
    ]:
        par(doc, "•  " + s, align="left", size=10, line=1.15, hanging=0.6, after=1)
    par(doc, "3. Sección A: tareas de registro (Treg)", bold=True, before=3, after=1, keep_next=True)
    al = ["center", "left", "center", "center", "center", "center", "left"]
    v08_tabla(doc, ENCABEZADOS_TAREA_V08, [
        ["1\nREG-E1", "Registro de salida programada de tres biológicos con lote, cantidad, fecha, destino y responsable (Ensayo 1)"] + [""] * 5,
        ["2\nREG-E2", "Registro de salida programada de tres biológicos con lote, cantidad, fecha, destino y responsable (Ensayo 2)"] + [""] * 5,
        ["3\nREG-E3", "Registro de salida programada de tres biológicos con lote, cantidad, fecha, destino y responsable (Ensayo 3)"] + [""] * 5,
    ], ANCHOS_TAREA_V08, alto_min=620, alinear=al, margen=(30, 50, 30, 50))
    par(doc, "Mediana de los tres ensayos (estadístico principal por operador): ____________ min          Promedio: ____________ min",
        before=3, after=1, keep_next=True)
    par(doc, "4. Sección B: tareas de emisión de vales (Tvale)", bold=True, before=3, after=1, keep_next=True)
    v08_tabla(doc, ENCABEZADOS_TAREA_V08, [
        ["1\nVALE-E1", "Emisión de vale oficial para salida programada de tres biológicos a un establecimiento de salud (Ensayo 1)\nVale N.°: ________"] + [""] * 5,
        ["2\nVALE-E2", "Emisión de vale oficial para salida programada de tres biológicos a un establecimiento de salud (Ensayo 2)\nVale N.°: ________"] + [""] * 5,
        ["3\nVALE-E3", "Emisión de vale oficial para salida programada de tres biológicos a un establecimiento de salud (Ensayo 3)\nVale N.°: ________"] + [""] * 5,
    ], ANCHOS_TAREA_V08, alto_min=620, alinear=al, margen=(30, 50, 30, 50))
    par(doc, "Mediana de los tres ensayos (estadístico principal por operador): ____________ min          Promedio: ____________ min",
        before=3, after=1, keep_next=True)
    par(doc, "5. Declaración y firma", bold=True, before=3, after=1, keep_next=True)
    p = par(doc, "Declaración: la presente toma de tiempos respetó los puntos de inicio y fin del protocolo y la "
                 "regla de pausa, con veracidad de los datos registrados.     Firma del evaluador: "
                 "______________________________     " + TESISTA + ", Tesista", align="left", after=0)
    p.paragraph_format.keep_together = True


def v09_ficha02(doc):
    par(doc, "INSTRUMENTO N.° 02", bold=True, align="center", after=0, pbb=True)
    par(doc, "FICHA DE REGISTRO Y COTEJO DOCUMENTAL DE CONSISTENCIA", bold=True, align="center", after=2)
    par(doc, "Dimensión: consistencia documental. Indicadores: registros sin discrepancias (RSD) y concordancia "
             "entre cantidad programada y entregada (CPE). Formulario en blanco para auditoría documental; no se "
             "llena durante la validación.", align="both", size=10, line=1.15, after=2)
    par(doc, "1. Datos generales de la auditoría documental", bold=True, before=3, after=2, keep_next=True)
    v08_tabla(doc, ["Campo", "Registro"], [
        ["Código del operador auditado", "TRAB-____  (TRAB-01 a TRAB-14)"],
        ["Centro de acopio provincial o microred", "____________________________     Provincia:   "
                                                   "[  ] Andahuaylas   [  ] Chincheros"],
        ["Unidad de registro documental", "Cada movimiento individual de vacuna registrado en documento oficial (RSD) "
                                          "y cada entrega programada de biológicos (CPE) (corpus de 40 a 60 registros/entregas por ventana de 30 días)."],
        ["Unidad de análisis para el contraste estadístico pretest-postest", "Cada operador evaluado (TRAB-01 a TRAB-14). Para cada operador se calculará el porcentaje de registros sin discrepancias (RSD) y el porcentaje de entregas concordantes (CPE) en el pretest y postest, obteniéndose 14 pares de observaciones para la prueba de Wilcoxon."],
        ["Documentos fuente consultados", "Pretest: Kardex físico, Pecosa física, Cuaderno de control de cadena de frío, Hojas de cálculo locales.\n"
                                          "Postest: Módulo de movimientos de SIVAC, Comprobante de salida digital (vale electrónico), Registro de auditoría del sistema."],
        ["Momento de medición", "[  ] Pretest (kardex manual, cuadernos y hojas de cálculo)   [  ] Postest "
                                "(base de datos y vales electrónicos de SIVAC)"],
        ["Ventana de auditoría", "Del ____ / ____ / ______  al  ____ / ____ / ______  (30 días calendario)"],
        ["Fecha de ejecución de la auditoría", "______ / ______ / ______"],
        ["Auditor principal", TESISTA + "     Secundario (si aplica): ______________________"],
    ], [3000, ANCHO_RETRATO - 3000])
    par(doc, "2. Regla de conformidad y los ocho criterios (RSD)", bold=True, before=3, after=1, keep_next=True)
    par(doc, "Un registro es conforme (1) cuando cumple simultáneamente los ocho criterios siguientes; si "
             "incumple al menos uno, es no conforme (0). Se audita un corpus de 40 a 60 registros por ventana "
             "de 30 días por operador para consolidar su porcentaje de registros sin discrepancias (n = 14 observaciones "
             "pareadas para la prueba de Wilcoxon).",
        align="left", size=10, line=1.15, after=1, keep_next=True)
    for i, c in enumerate(CRITERIOS_RSD_V09, start=1):
        par(doc, f"{i}.  {c}", align="left", size=10, line=1.15, hanging=0.6, after=0)
    par(doc, "3. Matriz de auditoría de registros (RSD)", bold=True, before=4, after=1, keep_next=True)
    filas_rsd = [[f"{i:02d}", v, "", "", "[  ] 1   [  ] 0", ""] for i, v in enumerate(MUESTRA_RSD_V07, 1)]
    filas_rsd.append(["...", "Continúa según el corpus real (40 a 60 registros por ventana)", "", "",
                      "[  ] 1   [  ] 0", ""])
    v08_tabla(doc, ["N.°", "Vacuna o insumo auditado", "Lote", "Cantidad",
                    "Veredicto (1 = conforme, 0 = no conforme)", "Tipo de discrepancia o causa raíz"],
              filas_rsd, ANCHOS_RSD_V08, alto_min=430,
              alinear=["center", "left", "left", "center", "center", "left"])
    par(doc, "Nota: si el corpus supera las filas disponibles, continúe en una hoja adicional con el mismo "
             "formato.", size=9.5, line=1.0, before=3, italic=True, keep_next=True)
    par(doc, "Total de registros evaluados: ______      Registros conformes: ______      "
             "Registros con discrepancia: ______      RSD consolidado por operador: ______ %", before=2, after=0)
    par(doc, "4. Regla de concordancia y matriz de entregas (CPE)", bold=True, before=4, after=1, keep_next=True)
    par(doc, "Una entrega es concordante (1) si la cantidad entregada es idéntica a la programada o si, siendo "
             "distinta, existe un documento sustentatorio oficial archivado que autoriza expresamente la "
             "variación; en cualquier otro caso es no concordante (0). Se auditan de 40 a 60 entregas por "
             "ventana de 30 días por operador para consolidar su porcentaje de concordancia (n = 14 observaciones "
             "pareadas para la prueba de Wilcoxon). Consolidado: Total de entregas auditadas ______, concordantes ______, "
             "no concordantes ______, CPE consolidado por operador ______ %.", align="left", size=10, line=1.15, after=2, keep_next=True)
    filas_a = [[f"{i:02d}", v, "Vale N.°:", "", "", ""] for i, v in enumerate(MUESTRA_CPE_V07, 1)]
    filas_a.append(["...", "Continúa en hoja adicional", "", "", "", ""])
    filas_b = [[f"{i:02d}", "[  ] Sí [  ] No [  ] N/A", "[  ] 1  [  ] 0", ""]
               for i in range(1, len(MUESTRA_CPE_V07) + 1)]
    filas_b.append(["...", "", "", ""])
    par(doc, "Las dos tablas siguientes se corresponden por número de caso: cantidades (4a) y verificación (4b).",
        size=9.5, line=1.0, italic=True, after=2, keep_next=True)
    v08_tabla(doc, ENCABEZADOS_CPE_A_V08, filas_a, ANCHOS_CPE_A_V08, alto_min=430,
              alinear=["center", "left", "left", "center", "center", "center"], margen=(30, 50, 30, 50))
    _v08_aire(doc, 6)
    v08_tabla(doc, ENCABEZADOS_CPE_B_V08, filas_b, ANCHOS_CPE_B_V08, alto_min=430,
              alinear=["center", "center", "center", "left"], margen=(30, 50, 30, 50))


def v09_cuestionario(doc):
    par(doc, "INSTRUMENTO N.° 03", bold=True, align="center", after=0, pbb=True)
    par(doc, "CUESTIONARIO DE SATISFACCIÓN DEL USUARIO CON EL PROCESO OPERATIVO Y MÓDULO COMPLEMENTARIO DE ACEPTACIÓN TECNOLÓGICA DE SIVAC",
        bold=True, align="center", after=3)
    par(doc, "Variable evaluada: gestión de movimientos mensuales de vacunas (variable dependiente). Dimensión: "
             "satisfacción del usuario. Población objetivo: personal de la cadena de frío e inmunizaciones de la "
             "DISA Apurímac II (N = n = 14). Formulario en blanco; no se llena durante la validación.",
        align="both", size=10, after=4)
    par(doc, "1. Instrucciones para el participante y escala de respuesta (Likert de 5 opciones)", bold=True,
        before=4, after=2, keep_next=True)
    par(doc, "•  Confidencialidad y anonimato bajo código numérico (TRAB-01 a TRAB-14), conforme a la Ley "
             "N.° 29733 de Protección de Datos Personales y el Código de Ética en Investigación de la UNAJMA.",
        align="left", hanging=0.8, after=1)
    par(doc, "•  Libertad de respuesta: no existen respuestas correctas ni incorrectas; marque con una equis (X) "
             "una sola alternativa por reactivo; las proposiciones son afirmaciones que se gradúan, no preguntas.",
        align="left", hanging=0.8, after=3)
    v08_tabla(doc, ["Puntuación", "Escala verbal", "Significado operativo"], ESCALA_LIKERT,
              ANCHOS_ESCALA_V07, alinear=["center", "left", "left"])
    par(doc, "Momento de aplicación (marque el evaluador):    [  ] Pretest (proceso manual)    "
             "[  ] Postest (proceso con el sistema web SIVAC).", before=5, after=2)
    par(doc, "2. Datos generales del participante", bold=True, before=4, after=1, keep_next=True)
    v08_tabla(doc, ["Campo", "Registro"], [
        ["Código de participante asignado", "TRAB-____  (TRAB-01 a TRAB-14)"],
        ["Centro de acopio / red / microred", ""],
        ["Provincia de desempeño", "[  ] Andahuaylas   [  ] Chincheros"],
        ["Condición laboral actual", "[  ] Nombrado D.L. 276   [  ] Contratado CAS (D.L. 1057)   "
                                     "[  ] Locación / otro"],
        ["Profesión / cargo operativo", "[  ] Lic. en Enfermería   [  ] Técnico(a) en Enfermería   "
                                        "[  ] Estadístico / soporte"],
        ["Tiempo de experiencia en red de frío", "[  ] Menos de 2 años   [  ] 2 a 5 años   [  ] 6 a 10 años   "
                                                 "[  ] Más de 10 años"],
        ["Fecha de aplicación", "______ / ______ / ______"],
    ], [3800, ANCHO_RETRATO - 3800])
    par(doc, "3. Modalidad A: satisfacción con el proceso operativo (AP y UP)", bold=True, before=6, after=1,
        keep_next=True)
    par(doc, "Ocho afirmaciones literales sobre la gestión del proceso; en el pretest el participante evalúa el "
             "proceso manual y en el postest el proceso mediado por el sistema. " + LEYENDA_LIKERT_V07,
        align="left", size=10, after=1)
    v07_tabla_likert(doc, [
        ("Indicador: Aceptación del proceso operativo (AP)", ["AP-01", "AP-02", "AP-03", "AP-04"], ITEMS_AP_V09),
        ("Indicador: Utilidad percibida para la gestión sanitaria (UP)", ["UP-01", "UP-02", "UP-03", "UP-04"],
         ITEMS_UP_V09),
    ])
    par(doc, "Firma del participante: ______________________________", before=8, after=2)
    par(doc, "Firma del encuestador (Bach. José Luis Quispe León, Tesista): ______________________________",
        after=0)
    par(doc, "4. Modalidad B: módulo complementario postest de aceptación del software SIVAC", bold=True, before=6, after=1, pbb=True, keep_next=True)
    par(doc, "Código de participante (TRAB): TRAB-______     Fecha de aplicación postest: ____ / ____ / ______",
        before=2, after=2)
    par(doc, "Módulo complementario postest de aceptación del software SIVAC (anexo descriptivo de consulta técnica; no aditivo a la variable dependiente). " + LEYENDA_LIKERT_V07,
        align="both", size=10, italic=True, bold=True, after=3)
    v07_tabla_likert(doc, [
        ("Utilidad percibida del software (PU)", ["PU-01", "PU-02", "PU-03", "PU-04"], ITEMS_PU),
        ("Facilidad de uso percibida del software (PE)", ["PE-01", "PE-02", "PE-03", "PE-04"], ITEMS_PE),
    ])
    par(doc, "Firma del participante: ______________________________", before=8, after=2)
    par(doc, "Firma del encuestador (Bach. José Luis Quispe León, Tesista): ______________________________",
        after=0)


def construir_v09():
    """Construye el expediente de validación v09 con arquitectura de secciones mixta:
    Sección 1 (Retrato A4) -> Sección 2 (Apaisada A4) -> Sección 3 (Retrato A4)."""
    doc = docx.Document()
    configurar_normal(doc)
    aplicar_geometria(doc.sections[0], "unajma")
    pie_pagina(doc.sections[0])
    cp = doc.core_properties
    cp.author, cp.title, cp.last_modified_by = TESISTA, "Expediente de validación para experto (v09 mixto)", TESISTA
    cp.comments, cp.subject, cp.keywords = "", "", ""

    # Sección 1: Retrato A4 (8,788 dxa)
    v09_carta(doc)
    v09_instrucciones(doc)
    v09_matriz_validacion(doc)

    # Sección 2: Apaisada A4 (14,000 dxa)
    nueva_seccion(doc, "apaisada")
    v09_matriz_consistencia(doc)
    v09_operacionalizacion(doc)

    # Sección 3: Retrato A4 (8,788 dxa)
    nueva_seccion(doc, "unajma")
    v09_ficha01(doc)
    v09_ficha02(doc)
    v09_cuestionario(doc)

    return doc


def nombre_v09(n):
    return f"EXPEDIENTE_VALIDACION_SIVAC_EXPERTO_0{n}_{VERSION_V09}.docx"


def verificar_v09(ruta):
    """Audita el DOCX v09 GUARDADO. Devuelve [(nombre, ok, detalle)]."""
    res = []

    def chk(nombre, ok, det=""):
        res.append((nombre, bool(ok), det))

    d = docx.Document(str(ruta))
    body = d.element.body
    txt = "\n".join(t.text or "" for t in body.iter(qn("w:t")))
    plano = re.sub(r"\s+", " ", txt)
    norm = fany._normalizar
    nplano = norm(txt)

    # 1. Orden de piezas principales
    pars = [_txt(p) for p in body.findall(qn("w:p"))]
    pos = [next((i for i, t in enumerate(pars) if t.startswith(m)), None) for m in MARCADORES_V09]
    chk("Orden de piezas carta, instrucciones, matriz de validez, matrices, instrumentos 01/02/03",
        None not in pos and pos == sorted(pos), str(pos))

    # 2. Arquitectura de secciones mixta: Retrato -> Apaisada -> Retrato
    chk("Documento con exactamente tres secciones", len(d.sections) == 3, f"{len(d.sections)} secciones")
    if len(d.sections) == 3:
        s0, s1, s2 = d.sections[0], d.sections[1], d.sections[2]
        s0_ok = (s0.page_width.cm < s0.page_height.cm and abs(s0.page_width.cm - 21.0) < 0.1
                 and abs(s0.page_height.cm - 29.7) < 0.1 and abs(s0.left_margin.cm - 3.0) < 0.05
                 and abs(s0.right_margin.cm - 2.5) < 0.05)
        s1_ok = (s1.page_width.cm > s1.page_height.cm and abs(s1.page_width.cm - 29.7) < 0.1
                 and abs(s1.page_height.cm - 21.0) < 0.1 and abs(s1.left_margin.cm - 2.5) < 0.05
                 and abs(s1.right_margin.cm - 2.5) < 0.05)
        s2_ok = (s2.page_width.cm < s2.page_height.cm and abs(s2.page_width.cm - 21.0) < 0.1
                 and abs(s2.page_height.cm - 29.7) < 0.1 and abs(s2.left_margin.cm - 3.0) < 0.05
                 and abs(s2.right_margin.cm - 2.5) < 0.05)
        chk("Seccion 1 A4 vertical retrato (margenes 3/2.5/2.5/2.5)", s0_ok,
            f"w={round(s0.page_width.cm, 1)} h={round(s0.page_height.cm, 1)} l={round(s0.left_margin.cm, 1)}")
        chk("Seccion 2 A4 horizontal apaisada (margenes 2.5/2.5/2.5/2.5)", s1_ok,
            f"w={round(s1.page_width.cm, 1)} h={round(s1.page_height.cm, 1)} l={round(s1.left_margin.cm, 1)}")
        chk("Seccion 3 A4 vertical retrato (margenes 3/2.5/2.5/2.5)", s2_ok,
            f"w={round(s2.page_width.cm, 1)} h={round(s2.page_height.cm, 1)} l={round(s2.left_margin.cm, 1)}")

    # 3. Tablas OpenXML: geometria, bordes y blindaje
    ok_flo = ok_cs = ok_hd = ok_math = ok_ancho = ok_bordes = ok_neg = ok_filas = ok_ind = True
    n_rejilla = n_apa = 0
    det_bordes = []
    for t in d.tables:
        tblPr = t._tbl.tblPr
        ok_flo &= tblPr.find(qn("w:tblpPr")) is None
        w = int(tblPr.find(qn("w:tblW")).get(qn("w:w")))
        grid = [int(g.get(qn("w:w"))) for g in t._tbl.tblGrid.findall(qn("w:gridCol"))]
        ok_ancho &= (w == sum(grid) and w in (ANCHO_RETRATO, ANCHO_APAISADA))
        ok_neg &= all(x > 0 for x in grid)
        ind = tblPr.find(qn("w:tblInd"))
        ok_ind &= ind is None or int(ind.get(qn("w:w"), "0")) == 0
        for tr in t._tbl.findall(qn("w:tr")):
            trPr = tr.find(qn("w:trPr"))
            ok_cs &= trPr is not None and trPr.find(qn("w:cantSplit")) is not None
            ws = [int(x.get(qn("w:w"))) for x in tr.xpath("./w:tc/w:tcPr/w:tcW")]
            ok_neg &= all(x > 0 for x in ws)
            ok_filas &= sum(ws) == w and len(ws) == len(tr.findall(qn("w:tc")))
        primera_tr = t._tbl.find(qn("w:tr")).find(qn("w:trPr"))
        ok_hd &= primera_tr is not None and primera_tr.find(qn("w:tblHeader")) is not None
        ok_math &= len(t._tbl.xpath('.//*[local-name()="oMath"]')) == 0
        tb = tblPr.find(qn("w:tblBorders"))
        if tb is None:
            ok_bordes = False
            det_bordes.append("sin tblBorders")
            continue
        estados = {l: (tb.find(qn("w:" + l)).get(qn("w:val")) if tb.find(qn("w:" + l)) is not None else None)
                   for l in ("top", "left", "bottom", "right", "insideH", "insideV")}
        enc = _txt(t._tbl.find(qn("w:tr")).find(qn("w:tc"))).strip()
        if enc.startswith("Problemas") or enc.startswith("Variable"):
            n_apa += 1
            ok_bordes &= (estados["top"] == "single" and estados["bottom"] == "single"
                          and not any(estados[l] in ("single", "double", "thick")
                                      for l in ("left", "right", "insideV", "insideH")))
            ok_bordes &= not t._tbl.xpath(".//w:tcBorders/*[self::w:left or self::w:right or self::w:insideV]"
                                          "[@w:val='single']")
        else:
            n_rejilla += 1
            if not all(estados[l] == "single" for l in ("top", "left", "bottom", "right", "insideH", "insideV")):
                ok_bordes = False
                det_bordes.append(str(estados))
    chk("Tablas sin flotacion", ok_flo)
    chk("Todas las tablas al ancho reglamentario (8788 retrato o 14000 apaisada)", ok_ancho)
    chk("Sin anchos negativos o nulos ni sangrias de tabla (tblInd)", ok_neg and ok_ind)
    chk("Suma de tcW por fila = ancho de tabla", ok_filas)
    chk("Todas las filas con cantSplit", ok_cs)
    chk("Primera fila de cada tabla como encabezado repetido", ok_hd)
    chk("Sin ecuaciones OMML ni formulas en celdas", ok_math)
    chk(f"Bordes: formularios y matriz de validacion con rejilla cerrada ({n_rejilla}) y matrices con APA 7 ({n_apa})",
        ok_bordes and n_rejilla == 14 and n_apa == 2, f"rejilla={n_rejilla} apa={n_apa} {det_bordes[:3]}")
    chk("Tablas nativas (sin imagenes)",
        len(body.xpath(".//w:drawing")) == 0 and len(body.xpath(".//w:pict")) == 0)

    # 4. Matriz de validacion de 8 columnas en vertical (Sección 1)
    certs = [t for t in d.tables if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 8]
    chk("UNA sola matriz de validacion de 8 columnas a 8788 dxa", len(certs) == 1, str(len(certs)))
    if certs:
        t_val = certs[0]
        trs = t_val._tbl.findall(qn("w:tr"))
        chk("Matriz de validacion con 14 filas (2 encabezado + 12 elementos continuos)", len(trs) == 14, f"{len(trs)} filas")
        grid_w = [int(g.get(qn("w:w"))) for g in t_val._tbl.tblGrid.findall(qn("w:gridCol"))]
        chk("Geometria de 8 columnas coincide exactamente con anchos v08/v09",
            grid_w == ANCHOS_MATRIZ_VALIDEZ_V08, str(grid_w))
        tr0_hd = trs[0].find(qn("w:trPr")).find(qn("w:tblHeader")) is not None
        tr1_hd = trs[1].find(qn("w:trPr")).find(qn("w:tblHeader")) is not None
        chk("Dos filas de encabezado repetidas (tblHeader)", tr0_hd and tr1_hd)
        nums, elem_txts, celdas_llenas = [], [], 0
        for r_idx in range(2, len(trs)):
            tcs = trs[r_idx].findall(qn("w:tc"))
            nums.append(_txt(tcs[0]).strip())
            elem_txts.append(_txt(tcs[3]).strip())
            for c in (4, 5, 6, 7):
                if _txt(tcs[c]).strip():
                    celdas_llenas += 1
        chk("Numeracion continua de elementos 1 a 12 en matriz de validacion",
            nums == [str(i) for i in range(1, 13)], str(nums))
        chk("Casillas de evaluacion (Pertinencia, Relevancia, Claridad, Sugerencias) vacias",
            celdas_llenas == 0, f"{celdas_llenas} celdas con texto")
        esperado_elems = [norm(f[3]) for f in FILAS_MATRIZ_VALIDEZ_V09]
        obtenido_elems = [norm(e) for e in elem_txts]
        chk("Textos literales de los 12 elementos evaluados en matriz de validacion",
            esperado_elems == obtenido_elems,
            f"coinciden {sum(1 for a, b in zip(esperado_elems, obtenido_elems) if a == b)}/12")

    # 5. Cierre metodologico del juez validador
    chk("Cierre del juez con titulo DECISIÓN FINAL SOBRE LA APLICABILIDAD",
        "DECISIÓN FINAL SOBRE LA APLICABILIDAD DEL INSTRUMENTO" in txt)
    chk("Cuatro opciones de aplicabilidad en blanco presentes",
        "[   ] Aplicable sin modificaciones" in txt
        and "[   ] Aplicable con modificaciones menores" in txt
        and "[   ] Requiere revisión y reestructuración sustancial" in txt
        and "[   ] No aplicable" in txt)
    chk("Pregunta de suficiencia en blanco presente",
        "¿Los elementos propuestos son suficientes para medir la variable en estudio?" in txt
        and "[   ] Sí          [   ] No" in txt)
    chk("Tres lineas de observaciones y datos del juez presentes",
        txt.count("Apellidos y nombres del juez validador:") == 1
        and txt.count("DNI: .....................................................") == 1
        and f"del {ANIO}" in txt)
    chk("Bloque de firma del juez validador unico",
        txt.count("Firma del juez validador") == 1
        and "________________________________________" in txt)

    # 6. Matrices academicas en Seccion 2 (Apaisada)
    mc_t = [t for t in d.tables if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 5
            and int(t._tbl.tblPr.find(qn("w:tblW")).get(qn("w:w"))) == ANCHO_APAISADA]
    chk("Matriz de consistencia completa a 14000 dxa en Seccion 2", len(mc_t) == 1, str(len(mc_t)))
    chk("Hipotesis general con texto de integracion de las tres dimensiones",
        "La hipótesis general será contrastada a partir de la integración" in txt)
    chk("Sin criterio condicional de rechazo en 3 hipotesis (p < 0.05)",
        "Se acepta si se rechaza la hipótesis nula" not in txt)
    oper_t = [t for t in d.tables if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 6
              and int(t._tbl.tblPr.find(qn("w:tblW")).get(qn("w:w"))) == ANCHO_APAISADA]
    chk("Matriz de operacionalizacion completa a 14000 dxa en Seccion 2", len(oper_t) == 1, str(len(oper_t)))

    # 7. Aspectos metodologicos criticos 1 a 6
    # Aspecto 1: Carta y separacion clara de Modalidad B
    chk("Aspecto 1: Carta con frase 'tres dimensiones definidas para la variable dependiente'",
        "las tres dimensiones definidas para la variable dependiente" in txt
        and "las tres dimensiones oficiales de la variable dependiente" not in txt)
    chk("Aspecto 1: Modalidad B descrita como anexo complementario de consulta tecnica en postest",
        "Modalidad B como anexo complementario de consulta técnica para la evaluación descriptiva postest" in txt
        and "sin formar parte de la escala de la variable dependiente" in txt)
    chk("Aspecto 1: Punto 2 de la carta con unidad de registro documental y consolidacion por operador",
        "Cada movimiento o entrega constituye una unidad de registro documental; posteriormente, los resultados se consolidan en porcentajes por operador para el contraste estadístico pretest–postest." in txt
        and "con unidad de análisis dual y consolidación por operador" not in txt)

    # Aspecto 2: V de Aiken y criterio de corte V >= 0.80
    chk("Aspecto 2: Instrucciones con V de Aiken para validez de contenido por elemento/criterio",
        "procesamiento de la validez de contenido mediante el coeficiente V de Aiken, calculado para cada elemento y criterio de evaluación" in txt
        and "concordancia entre jueces" not in txt)
    chk("Aspecto 2: Criterio de decision V >= 0.80 para validez de contenido e interpretacion cualitativa",
        "coeficiente V de Aiken alcance o supere el valor mínimo establecido para la investigación (V >= 0.80)" in txt
        and "El valor mínimo de V de Aiken será interpretado conjuntamente con las observaciones cualitativas de los jueces expertos." in txt)

    # Aspecto 3: Ficha 01 con tarea estandarizada representativa unica, tres repeticiones y control de sesgo
    chk("Aspecto 3: Ficha 01 con tarea representativa unica de registro y tres ensayos REG-E1..E3",
        "Registro de salida programada de tres biológicos con lote, cantidad, fecha, destino y responsable" in txt
        and "REG-E1" in txt and "REG-E2" in txt and "REG-E3" in txt)
    chk("Aspecto 3: Ficha 01 con tarea representativa unica de emision y tres ensayos VALE-E1..E3",
        "Emisión de vale oficial para salida programada de tres biológicos a un establecimiento de salud" in txt
        and "VALE-E1" in txt and "VALE-E2" in txt and "VALE-E3" in txt)
    chk("Aspecto 3: Ficha 01 con control de sesgo de aprendizaje y comparabilidad de los 3 ensayos",
        "Los tres ensayos se realizarán con casos equivalentes en complejidad, cantidad de biológicos, datos requeridos y flujo operativo" in txt
        and "El orden de los tres ensayos será el mismo en pretest y postest para todos los participantes." in txt)
    chk("Aspecto 3: Punto final uniforme de emision de vales en Ficha 01 y matriz de validez",
        "Tiempo de emisión de vales: inicia cuando el operador recibe o abre la solicitud de pedido y termina cuando el vale o comprobante de salida ha sido generado y queda disponible para su entrega, impresión o registro institucional" in txt
        and "hasta que el comprobante de salida queda generado y disponible para su entrega, impresión o registro institucional" in txt)
    chk("Aspecto 3: Mediana de los tres ensayos como estadistico principal por operador",
        txt.count("Mediana de los tres ensayos (estadístico principal por operador): ____________ min          Promedio: ____________ min") == 2)

    # Aspecto 4: Ficha 02 con operador auditado, unidad de registro y pareamiento de Wilcoxon
    chk("Aspecto 4: Ficha 02 declara exclusivamente al operador auditado y unidad de registro documental",
        "Código del operador auditado" in txt
        and "Unidad de registro documental" in txt
        and "Unidad de análisis para el contraste estadístico pretest-postest" in txt
        and "Cada operador evaluado (TRAB-01 a TRAB-14)" in txt
        and "14 pares de observaciones para la prueba de Wilcoxon" in txt)

    # Aspecto 5: Criterio 4 de RSD perfeccionado
    criterio4_esperado = (
        "Cantidad registrada concordante con el documento fuente que sustenta el movimiento. "
        "En entradas, se verifica la concordancia con el acta, guía de remisión o documento de recepción; "
        "en salidas, con la orden de pedido, vale autorizado o nota de modificación; "
        "y en ajustes, con el documento de autorización correspondiente."
    )
    chk("Aspecto 5: Criterio 4 de RSD con redaccion perfeccionada",
        norm(criterio4_esperado) in nplano)

    # Reactivos atómicos de satisfacción (Modalidad A) y título Instrumento 03
    chk("Ocho reactivos atomicos de satisfaccion presentes literalmente en Modalidad A",
        all(norm(it) in nplano for it in ITEMS_AP_V09 + ITEMS_UP_V09))
    chk("Titulo oficial exacto del Instrumento N.° 03",
        "CUESTIONARIO DE SATISFACCIÓN DEL USUARIO CON EL PROCESO OPERATIVO Y MÓDULO COMPLEMENTARIO DE ACEPTACIÓN TECNOLÓGICA DE SIVAC" in txt)
    chk("Sintesis de UP en operacionalizacion con 4 reactivos atomicos",
        "Percepción de oportunidad informativa, asignación correcta de biológicos, sustento documental y seguimiento de existencias" in txt)
    chk("Matriz de consistencia con NOTA_METODOLOGIA_V09",
        "Considerando el tamaño muestral de 14 participantes y el carácter pareado de las mediciones, la contrastación de hipótesis se realizará mediante la prueba no paramétrica de rangos con signo de Wilcoxon" in txt)

    # Modalidad B delimitada con firmas
    chk("Modalidad B rotulada como modulo anexo no aditivo con firmas separadas",
        "4. Modalidad B: módulo complementario postest de aceptación del software SIVAC" in txt
        and "anexo descriptivo de consulta técnica; no aditivo a la variable dependiente" in txt
        and txt.count("Firma del participante: ") == 2
        and txt.count("Firma del encuestador (Bach. José Luis Quispe León, Tesista):") == 2
        and "TRAB-______" in txt and "Fecha de aplicación postest: ____ / ____ / ______" in txt)

    # 8. Seguridad, estilo y verificabilidad
    chk("Fechas de aplicacion en blanco (dia/mes/año)",
        txt.count("______ / ______ / ______") >= 3
        and "Del ____ / ____ / ______  al  ____ / ____ / ______" in txt
        and not re.search(r"Fecha de (aplicación|la observación|ejecución)[^\n]*2025", txt))
    psico = [m for m in ("Alfa de Cronbach", "Omega de McDonald", "baremo", "tercil", "piloto", "puntaje global")
             if m.lower() in plano.lower()]
    chk("Sin baremos, alfa, omega, terciles ni piloto", not psico, str(psico))

    fuentes, tam = set(), set()
    for r in body.iter(qn("w:r")):
        rPr = r.find(qn("w:rPr"))
        if rPr is None or not _txt(r).strip():
            continue
        rf = rPr.find(qn("w:rFonts"))
        fuentes.add(rf.get(qn("w:ascii")) if rf is not None and rf.get(qn("w:ascii")) else "(heredada)")
        sz = rPr.find(qn("w:sz"))
        if sz is not None:
            tam.add(int(sz.get(qn("w:val"))) / 2)
    chk("Fuente Times New Roman exclusiva", fuentes <= FUENTES_OK, str(sorted(fuentes)))
    chk("Sin tamanos menores a 8.5 pt", all(x >= 8.5 for x in tam), str(sorted(tam)))
    chk("Sin sombreados ni colores distintos del negro",
        len(body.xpath(".//w:shd[@w:fill and @w:fill!='auto' and @w:fill!='FFFFFF']")) == 0 and
        all(c.get(qn("w:val")).upper() in ("000000", "AUTO") for c in body.iter(qn("w:color"))))
    chk("Prohibicion absoluta del guion largo / raya (U+2014)", "—" not in txt)
    hall = [p for p in PROHIBIDOS if re.search(p, txt)]
    chk("Sin metadatos internos, contactos ni rayas", not hall, str(hall))
    chk("Sin marcas X ni calificaciones prellenadas", not re.search(r"\[\s*[xX]\s*\]", txt) and "×" not in txt)

    return res


def verificar_pdf_v09(pdf):
    """Paginación y auditoría visual del PDF v09 (arquitectura mixta: retrato/apaisada/retrato)."""
    import pymupdf

    def _norma(s):
        return re.sub(r"\s+", " ", s).strip().lower()

    doc = pymupdf.open(str(pdf))
    res = []
    textos = [p.get_text() for p in doc]

    hay_vert = any(p.rect.width < p.rect.height for p in doc)
    hay_apai = any(p.rect.width > p.rect.height for p in doc)
    res.append(("Páginas con orientación mixta (vertical y apaisada)", hay_vert and hay_apai,
                f"vert={sum(1 for p in doc if p.rect.width < p.rect.height)} apai={sum(1 for p in doc if p.rect.width > p.rect.height)}"))
    res.append(("Primera página es vertical (Carta)", doc[0].rect.width < doc[0].rect.height, ""))
    res.append(("Sin paginas vacias", not [i + 1 for i, t in enumerate(textos) if len(t.strip()) < 30], ""))

    inicios = []
    for t in textos:
        lineas = [l.strip() for l in t.splitlines() if l.strip()]
        if lineas and re.fullmatch(r"\d+", lineas[0]):
            lineas = lineas[1:]
        inicios.append(_norma(" ".join(lineas[:3])) if lineas else "")

    for m in MARCADORES_V09:
        pg = next((i for i, ini in enumerate(inicios) if ini.startswith(_norma(m))), None)
        res.append((f"'{m[:48]}' abre pagina" + (f" {pg + 1}" if pg is not None else ""), pg is not None, ""))

    firma = next((i for i, t in enumerate(textos) if _norma("Firma del juez validador") in _norma(t)), None)
    res.append(("Cierre unico del juez dentro de la matriz de validez (Seccion 1)", firma is not None and firma <= 5,
                f"pagina {firma + 1 if firma is not None else None}"))

    mc_pg = next((i for i, ini in enumerate(inicios) if ini.startswith(_norma("MATRIZ DE CONSISTENCIA"))), None)
    if mc_pg is not None:
        res.append(("Página de Matriz de Consistencia es apaisada", doc[mc_pg].rect.width > doc[mc_pg].rect.height, f"página {mc_pg + 1}"))
    oper_pg = next((i for i, ini in enumerate(inicios) if ini.startswith(_norma("MATRIZ DE OPERACIONALIZACIÓN DE VARIABLES"))), None)
    if oper_pg is not None:
        res.append(("Página de Matriz de Operacionalización es apaisada", doc[oper_pg].rect.width > doc[oper_pg].rect.height, f"página {oper_pg + 1}"))

    pobres = [i + 1 for i, t in enumerate(textos)
              if len([l for l in t.splitlines() if l.strip() and not re.fullmatch(r"\s*\d+\s*", l)]) <= 3]
    res.append(("Sin paginas con 3 lineas o menos (huerfanas)", not pobres, str(pobres)))
    res.append(("Total de paginas entre 10 y 18", 10 <= len(doc) <= 18, str(len(doc))))
    return res


def generar_v09(sobrescribir=True):
    import shutil
    DIR_V09.mkdir(parents=True, exist_ok=True)
    rutas = [DIR_V09 / nombre_v09(n) for n in (1, 2, 3)]
    existentes = [r for r in rutas if r.exists()]
    if existentes and not sobrescribir:
        for r in existentes:
            print(f"[OMITIDO] {r.name} ya existe; no se sobrescribe")
        return 0
    maestro = rutas[0]
    construir_v09().save(str(maestro))
    res = verificar_v09(maestro)
    malos = [r for r in res if not r[1]]
    if malos:
        print(f"[ABORTADO] {maestro.name}: {len(malos)} comprobaciones no conformes; archivo eliminado")
        for nom, _, det in malos:
            print(f"   FALLA {nom} {det}")
        if maestro.exists():
            maestro.unlink()
        return 1
    print(f"[OK] {maestro.name} ({maestro.stat().st_size:,} bytes): {len(res)} comprobaciones conformes")
    for r in rutas[1:]:
        shutil.copyfile(maestro, r)
        print(f"[OK] {r.name} copia byte-identica del ejemplar 01 ({r.stat().st_size:,} bytes)")

    # Exportar a PDF mediante Word COM (si está disponible)
    try:
        pdf_01 = DIR_V09 / f"EXPEDIENTE_VALIDACION_SIVAC_EXPERTO_01_{VERSION_V09}.pdf"
        quir.exportar_docx_a_pdf(maestro, pdf_01)
        print(f"[OK] PDF generado vía Word COM: {pdf_01.name} ({pdf_01.stat().st_size:,} bytes)")
        for n in (2, 3):
            pdf_n = DIR_V09 / f"EXPEDIENTE_VALIDACION_SIVAC_EXPERTO_0{n}_{VERSION_V09}.pdf"
            shutil.copyfile(pdf_01, pdf_n)
            print(f"[OK] {pdf_n.name} copia byte-idéntica del PDF 01")
        # Verificar PDF generado
        res_pdf = verificar_pdf_v09(pdf_01)
        malos_pdf = [r for r in res_pdf if not r[1]]
        print(f"[OK] Auditoría PDF v09: {len(res_pdf) - len(malos_pdf)}/{len(res_pdf)} comprobaciones conformes")
        for nom, ok, det in res_pdf:
            print(f"   [{'OK' if ok else 'FALLA'}] {nom} {det}")
    except Exception as exc:
        print(f"[AVISO] Exportación o auditoría PDF vía Word COM: {exc}")

    return 0


# ----------------------------------------------------------------- ensamblado


def construir_expediente(n):
    doc = docx.Document()
    configurar_normal(doc)
    aplicar_geometria(doc.sections[0], "unajma")
    pie_pagina(doc.sections[0])
    cp = doc.core_properties
    cp.author, cp.title, cp.last_modified_by = TESISTA, "Expediente de revisión y validación por juicio de expertos", TESISTA
    cp.comments, cp.subject, cp.keywords = "", "", ""
    pieza_carta(doc)
    pieza_instrucciones(doc)
    pieza_hoja_informativa(doc)
    pieza_panorama(doc)
    pieza_hoja_01(doc)
    pieza_hoja_02(doc)
    pieza_certificado03(doc)
    pieza_cuestionario03(doc)
    pieza_matriz_consistencia(doc)
    pieza_operacionalizacion(doc)
    pieza_ficha01(doc)
    pieza_ficha02(doc)
    return doc


def nombre_ejemplar(n):
    return f"EXPEDIENTE_VALIDACION_SIVAC_COMPLETO_EXPERTO_0{n}_{VERSION}.docx"


# ------------------------------------------------------------- verificacion

def _txt(el):
    return "".join(t.text or "" for t in el.iter(qn("w:t")))


def _tabla_certificado(d):
    """Localiza la tabla del certificado 03: 9 columnas a ancho de retrato (8788 dxa)."""
    return [t for t in d.tables
            if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 9
            and int(t._tbl.tblPr.find(qn("w:tblW")).get(qn("w:w"))) == ANCHO_RETRATO]


def _tablas_hoja(d):
    """Localiza las tablas de las hojas de evaluacion 01 y 02: 9 columnas a
    ancho apaisado (14000 dxa) con encabezado de elementos."""
    res = []
    for t in d.tables:
        if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) != 9:
            continue
        w = int(t._tbl.tblPr.find(qn("w:tblW")).get(qn("w:w")))
        if w != ANCHO_APAISADA:
            continue
        if "ELEMENTOS DE LA FICHA / PROTOCOLO" in _txt(t._tbl):
            res.append(t)
    return res


def _auditar_hoja(t, grupos, nombre):
    """Controles estructurales de una hoja de evaluacion de contenido."""
    res = []

    def chk(nom, ok, det=""):
        res.append((f"{nombre}: {nom}", bool(ok), det))

    trs = t._tbl.findall(qn("w:tr"))
    n_elem = sum(len(filas) for _, filas in grupos)
    chk("Tabla con 2 encabezado + %d grupo + %d elementos" % (len(grupos), n_elem),
        len(trs) == 2 + len(grupos) + n_elem, f"{len(trs)} filas")
    etiquetas = [_txt(trs[1].findall(qn("w:tc"))[c]).strip() for c in (2, 3, 4, 5, 6, 7)]
    chk("Etiquetas Si/No con tilde", etiquetas == ["Sí", "No", "Sí", "No", "Sí", "No"], ",".join(etiquetas))
    fila, numeros, llenas, textos = 2, [], 0, []
    for etiqueta_grupo, elementos in grupos:
        if fila >= len(trs):
            res.append((f"{nombre}: filas insuficientes para el grupo '{etiqueta_grupo[:38]}...'", False,
                        f"{len(trs)} filas"))
            break
        primera = _txt(trs[fila].findall(qn("w:tc"))[0]).strip()
        res.append((f"{nombre}: fila de grupo '{etiqueta_grupo[:38]}...'", primera == etiqueta_grupo,
                    primera[:50]))
        fila += 1
        for num, texto in elementos:
            if fila >= len(trs):
                res.append((f"{nombre}: faltan filas de elemento (se esperaba {num:02d})", False,
                            f"{len(trs)} filas"))
                return res
            tcs = trs[fila].findall(qn("w:tc"))
            numeros.append(_txt(tcs[0]).strip())
            textos.append(_txt(tcs[1]).strip())
            for c in (2, 3, 4, 5, 6, 7, 8):
                if _txt(tcs[c]).strip():
                    llenas += 1
            fila += 1
    chk("Numeracion continua de elementos", numeros == [f"{i:02d}" for i in range(1, n_elem + 1)],
        ",".join(numeros[:6]) + "...")
    norm = fany._normalizar
    esperado = [norm(texto) for _, filas in grupos for _, texto in filas]
    chk("Textos de elementos literales del generador", [norm(x) for x in textos] == esperado)
    chk("Celdas de criterio y sugerencias vacias (sin marcas X)", llenas == 0, f"{llenas} con texto")
    ok_cs = all(tr.find(qn("w:trPr")) is not None and
                tr.find(qn("w:trPr")).find(qn("w:cantSplit")) is not None for tr in trs)
    chk("Filas con cantSplit", ok_cs)
    ok_hd = all(trs[i].find(qn("w:trPr")).find(qn("w:tblHeader")) is not None for i in (0, 1))
    chk("Encabezado de dos filas repetido", ok_hd)
    return res


def _auditar_certificado(doc):
    """Controles estructurales del certificado de la Dimension 3. Devuelve [(nombre, ok, detalle)]."""
    res = []

    def chk(nombre, ok, det=""):
        res.append((nombre, bool(ok), det))

    body = doc.element.body
    txt = "\n".join(t.text or "" for t in body.iter(qn("w:t")))
    certs = _tabla_certificado(doc)
    chk("Tabla del certificado 03 unica de 9 columnas a 8788", len(certs) == 1, str(len(certs)))
    chk("Titulo del certificado presente", TITULO_CERT_03.replace("\n", " ")[:40] in txt)
    chk("Subtitulo del certificado presente", "Dimensión: Satisfacción del usuario." in txt)
    if certs:
        t = certs[0]
        trs = t._tbl.findall(qn("w:tr"))
        chk("Tabla con 12 filas (2 encabezado, 2 indicador, 8 reactivo)", len(trs) == 12, f"{len(trs)} filas")
        codigos, enunciados, celdas_llenas = [], [], 0
        # Encabezado de columnas de criterio: Sí/No con tilde en Sí (fila 1).
        enc_crit = [_txt(trs[1].findall(qn("w:tc"))[c]).strip() for c in fany.COLS_CRITERIO]
        chk("Etiquetas Sí/No con tilde en el encabezado del certificado",
            enc_crit == ["Sí", "No", "Sí", "No", "Sí", "No"], ",".join(enc_crit))
        for fila in range(2, 12):
            tcs = trs[fila].findall(qn("w:tc"))
            primera = _txt(tcs[0]).strip()
            if primera.startswith("Indicador:"):
                continue
            codigos.append(primera)
            enunciados.append(_txt(tcs[1]).strip())
            for c in fany.COLS_CRITERIO:
                if _txt(tcs[c]).strip():
                    celdas_llenas += 1
        esperados = [f"AP-0{i}" for i in range(1, 5)] + [f"UP-0{i}" for i in range(1, 5)]
        chk("Codigos AP-01 a UP-04 en orden", codigos == esperados, ",".join(codigos))
        norm = fany._normalizar
        esperado = [norm(e) for e in ITEMS_AP + ITEMS_UP]
        chk("Transcripcion literal de los 8 reactivos", [norm(e) for e in enunciados] == esperado)
        chk("Celdas de criterio vacias (sin marcas X)", celdas_llenas == 0, f"{celdas_llenas} con texto")
        ok_cs = all(tr.find(qn("w:trPr")) is not None and
                    tr.find(qn("w:trPr")).find(qn("w:cantSplit")) is not None for tr in trs)
        chk("Filas de la tabla con cantSplit", ok_cs)
        ok_hd = all(trs[i].find(qn("w:trPr")).find(qn("w:tblHeader")) is not None for i in (0, 1))
        chk("Encabezado de dos filas repetido", ok_hd)
    chk("Agrupacion por indicador AP presente", GRUPO_AP in txt)
    chk("Agrupacion por indicador UP presente", GRUPO_UP in txt)
    chk("Aclaracion de alcance presente", ACLARACION_CERT in txt)
    requeridos = [
        "Observaciones (precisar si hay suficiencia):",
        "Opinión de aplicabilidad:",
        "Aplicable [   ]",
        "Aplicable después de corregir [   ]",
        "No aplicable [   ]",
        "Apellidos y nombres del juez validador:",
        "DNI:",
        "Especialidad del validador:",
        "Firma del juez validador",
    ]
    faltan_b = [r for r in requeridos if r not in txt]
    chk("Componentes del bloque de cierre presentes", not faltan_b, str(faltan_b))
    chk("Tres bloques de cierre completos (hojas 01, 02 y certificado 03)",
        txt.count("Firma del juez validador") == 3
        and txt.count("Apellidos y nombres del juez validador:") == 3
        and txt.count("Opinión de aplicabilidad:") == 3,
        f"firmas={txt.count('Firma del juez validador')}")
    chk(f"Fechas de cierre con dia y mes en blanco y el año {ANIO} fijo (3 bloques: hojas 01, 02 y certificado 03)",
        len(re.findall(r"Andahuaylas, \.+ de \.+ del " + ANIO, txt)) == 3,
        str(len(re.findall(r"Andahuaylas, \.+ de \.+ del " + ANIO, txt))))
    faltan_n = [n for n in (NOTA_1, NOTA_2, NOTA_3) if fany._normalizar(n) not in fany._normalizar(txt)]
    chk("Notas 1, 2 y 3 literales (Claridad corregida)", not faltan_n, str(faltan_n))
    chk("Nota de suficiencia presente", "cubren de manera completa la dimensión" in txt)
    ok_juez = True
    for etiqueta in ("Apellidos y nombres del juez validador:", "Especialidad del validador:"):
        m = re.search(re.escape(etiqueta) + r"([^\n]*)", txt)
        resto = m.group(1) if m else "X"
        resto = resto.replace("DNI", "").replace(":", "")
        ok_juez &= bool(m) and re.fullmatch(r"[\s.]*", resto) is not None
    chk("Campos del juez en blanco", ok_juez)
    chk("Sin marcas X ni calificaciones prellenadas",
        not re.search(r"\[\s*[xX]\s*\]", txt) and "×" not in txt)
    return res


def verificar_docx(ruta):
    """Audita el DOCX GUARDADO. Devuelve lista de (nombre, ok, detalle)."""
    res = []

    def chk(nombre, ok, det=""):
        res.append((nombre, bool(ok), det))

    d = docx.Document(str(ruta))
    body = d.element.body
    # 1. Hojas de evaluacion de contenido N.° 01 y N.° 02
    hojas = _tablas_hoja(d)
    chk("Hojas de evaluacion 01 y 02 presentes (2 tablas apaisadas de elementos)", len(hojas) == 2,
        str(len(hojas)))
    if len(hojas) == 2:
        for nombre, ok, det in _auditar_hoja(hojas[0], GRUPOS_HOJA_01, "Hoja 01"):
            res.append((nombre, ok, det))
        for nombre, ok, det in _auditar_hoja(hojas[1], GRUPOS_HOJA_02, "Hoja 02"):
            res.append((nombre, ok, det))
    # 2. Certificado de la Dimension 3
    for nombre, ok, det in _auditar_certificado(d):
        res.append((f"Certificado 03: {nombre}", ok, det))
    # 2. Orden de piezas
    pars = [_txt(p) for p in body.findall(qn("w:p"))]
    pos = []
    for m in MARCADORES:
        idx = next((i for i, t in enumerate(pars) if t.startswith(m)), None)
        pos.append(idx)
    chk("Orden de piezas carta, instrucciones, hoja VI, panorama, hojas 01/02, certificado 03, cuestionario, "
        "matrices, fichas", None not in pos and pos == sorted(pos), str(pos))
    # 3. Inicio de pagina nueva por pieza
    ok_pbb = True
    for m in MARCADORES[1:]:
        p = next(p for p in body.findall(qn("w:p")) if _txt(p).startswith(m))
        pPr = p.find(qn("w:pPr"))
        pbb = pPr is not None and pPr.find(qn("w:pageBreakBefore")) is not None
        prev = p.getprevious()
        tras_seccion = prev is not None and prev.tag == qn("w:p") and prev.find(".//" + qn("w:sectPr")) is not None
        ok_pbb &= (pbb or tras_seccion)
    chk("Cada pieza inicia con salto de pagina o de seccion", ok_pbb)
    # 4. Tablas
    tablas = d.tables
    ok_geo = ok_flo = ok_cs = ok_hd = ok_math = ok_bordes = True
    detalle_geo = []
    detalle_bordes = []
    secs = d.sections
    maximo = max(ANCHO_RETRATO, ANCHO_APAISADA)
    for t in tablas:
        tblPr = t._tbl.tblPr
        ok_flo &= tblPr.find(qn("w:tblpPr")) is None
        w = int(tblPr.find(qn("w:tblW")).get(qn("w:w")))
        grid = sum(int(g.get(qn("w:w"))) for g in t._tbl.tblGrid.findall(qn("w:gridCol")))
        if w != grid or w > maximo:
            ok_geo = False
            detalle_geo.append((w, grid))
        for tr in t._tbl.findall(qn("w:tr")):
            trPr = tr.find(qn("w:trPr"))
            ok_cs &= trPr is not None and trPr.find(qn("w:cantSplit")) is not None
        primera = t._tbl.find(qn("w:tr")).find(qn("w:trPr"))
        ok_hd &= primera is not None and primera.find(qn("w:tblHeader")) is not None
        ok_math &= len(t._tbl.xpath('.//*[local-name()="oMath"]')) == 0
        # Bordes APA 7: top y bottom de tabla en una sola linea; cero lineas
        # verticales (left, right, insideV) y cero interiores horizontales.
        tb = tblPr.find(qn("w:tblBorders"))
        if tb is None:
            ok_bordes = False
            detalle_bordes.append("sin tblBorders")
            continue
        estados = {}
        for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
            el = tb.find(qn("w:" + lado))
            estados[lado] = None if el is None else el.get(qn("w:val"))
        if estados["top"] != "single" or estados["bottom"] != "single":
            ok_bordes = False
            detalle_bordes.append(str(estados))
        if any(estados[l] in ("single", "double", "thick") for l in ("left", "right", "insideV", "insideH")):
            ok_bordes = False
            detalle_bordes.append(str(estados))
        # Cero bordes verticales a nivel de celda.
        verticales = t._tbl.xpath(".//w:tcBorders/*[self::w:left or self::w:right or self::w:insideV]"
                                  "[@w:val='single']")
        if verticales:
            ok_bordes = False
            detalle_bordes.append(f"{len(verticales)} bordes verticales en celdas")
    chk("Tablas sin flotacion", ok_flo)
    chk("Ancho de tabla igual a la suma de columnas y dentro del area util", ok_geo, str(detalle_geo))
    chk("Todas las filas con cantSplit", ok_cs)
    chk("Primera fila de cada tabla como encabezado repetido", ok_hd)
    chk("Sin ecuaciones OMML ni formulas en celdas", ok_math)
    chk("Bordes APA 7 en todas las tablas (cero lineas verticales)", ok_bordes, str(detalle_bordes[:3]))
    chk("Tablas nativas (sin imagenes)", len(body.xpath(".//w:drawing")) == 0 and len(body.xpath(".//w:pict")) == 0)
    # 5. Tipografia y color
    tam = set()
    fuentes = set()
    for r in body.iter(qn("w:r")):
        rPr = r.find(qn("w:rPr"))
        if rPr is None or not _txt(r).strip():
            continue
        rf = rPr.find(qn("w:rFonts"))
        if rf is not None and rf.get(qn("w:ascii")):
            fuentes.add(rf.get(qn("w:ascii")))
        else:
            fuentes.add("(heredada)")
        sz = rPr.find(qn("w:sz"))
        if sz is not None:
            tam.add(int(sz.get(qn("w:val"))) / 2)
    chk("Fuente Times New Roman exclusiva", fuentes <= FUENTES_OK, str(sorted(fuentes)))
    chk("Sin tamanos menores a 9 pt", all(t >= 9.0 for t in tam), str(sorted(tam)))
    chk("Sin sombreados ni colores distintos del negro",
        len(body.xpath(".//w:shd[@w:fill and @w:fill!='auto' and @w:fill!='FFFFFF']")) == 0 and
        all(c.get(qn("w:val")).upper() in ("000000", "AUTO") for c in body.iter(qn("w:color"))))
    # 6. Texto prohibido y contenido clave
    todo = "\n".join(_txt(p) for p in body.iter(qn("w:p")))
    plano = re.sub(r"\s+", " ", todo)
    hall = [p for p in PROHIBIDOS if re.search(p, todo)]
    chk("Sin metadatos internos, contactos, CIP ni raya", not hall, str(hall))
    excl = [e for e in EXCLUIDOS if e in todo]
    chk("Sin legado v03 (8 enunciados nuevos, PU/PE como dimensiones VI, doble certificado, nota corrupta)",
        not excl, str(excl))
    norm = fany._normalizar
    lit_apup = all(norm(e) in norm(todo) for e in ITEMS_AP + ITEMS_UP)
    lit_pupe = all(norm(e) in norm(todo) for e in ITEMS_PU + ITEMS_PE)
    chk("Ocho reactivos AP/UP literales (Modalidad A)", lit_apup)
    chk("Ocho reactivos PU/PE literales (Modalidad B)", lit_pupe)
    chk("X0 y X1 presentes (intervencion dicotomica)", "X0" in todo and "X1" in todo)
    chk("Categoria 'Intervención tecnológica dicotómica' presente",
        "Intervención tecnológica dicotómica" in todo)
    chk("Hoja informativa declara que no es escala psicométrica ni certificado (una sola vez)",
        plano.count("no constituye una escala psicométrica ni un certificado de validez de contenido de la "
                    "variable independiente") == 1
        and "no constituye una escala ni un certificado" not in plano)
    chk("Carta declara propuesta para revision", "Propuesta para revisión" in todo)
    chk("Instrucciones anuncian los TRES formatos de juicio",
        "TRES formatos de juicio" in todo and "Devuelva los tres formatos completos" in todo)
    chk("Carta anuncia los 3 formatos y los 3 instrumentos",
        "TRES formatos de juicio" in todo and "Tercera: hoja" not in todo
        and "se someten a juicio de contenido" in todo)
    chk("Alcance explicito: el juez evalua componentes del protocolo, no contesta datos ni valida desempeno",
        "NO equivale a contestar los datos de campo" in todo
        and "NO valida el desempeño del sistema SIVAC" in todo)
    chk("Panorama de las 3 dimensiones presente (tabla Dimension-Instrumento-Hoja)",
        TITULO_PANORAMA in todo and all(d in todo for d in ("Oportunidad de procesamiento",
                                                            "Consistencia documental", "Satisfacción del usuario")))
    chk("Fichas 01 y 02 adjuntas integras y sin llenar (2 fichas)",
        todo.count("se adjunta íntegra y NO se llena") == 2)
    chk("Tres instrumentos sometidos a juicio de contenido (afirmacion expresa)",
        todo.count("se someten a juicio de contenido") >= 2
        and "como contexto del protocolo evaluado" not in plano)
    chk("Sin afirmaciones heredadas (solo instrumento 03 / unico certificado / fichas sin juicio)",
        "las fichas no reciben" not in plano.lower()
        and "único certificado" not in plano.lower()
        and "solo el Instrumento N.° 03 recibe" not in plano
        and "no reciben juicio" not in plano.lower())
    chk("Elementos de hojas sin formulas algebraicas ni codigos internos",
        not re.search(r"t_fin|t_inicio|Q_prog|Q_ent|I1\.|I2\.|\bC[1-8]:", todo)
        and "Node.js" not in todo and "PostgreSQL" not in todo)
    chk("Cuestionario integro: baremo y protocolo presentes",
        "8 a 40 puntos" in todo and "Alfa de Cronbach" in todo and "Modalidad B" in todo)
    n_omml = len(body.xpath('.//*[local-name()="oMath"]'))
    chk("Cuatro ecuaciones narrativas OMML nativas (subescala, global, alfa, omega)", n_omml == 4,
        f"{n_omml} oMath")  # limite fijo del encargo v05: las 4 de v04, sin fórmulas nuevas
    chk("Ninguna ecuacion OMML dentro de tablas",
        all(len(t._tbl.xpath('.//*[local-name()="oMath"]')) == 0 for t in d.tables))
    chk("Sin LaTeX ni degradacion ASCII de formulas",
        not re.search(r"\\frac|\\sum|\\alpha|\\Sigma|\[\s*k\s*/\s*\(k", todo) and "$" not in todo)
    chk("Piloto externo declarado como previsto y no ejecutado",
        "se prevé administrar el instrumento a una muestra piloto" in plano
        and "no certifica la ejecución de dicho piloto" in plano
        and "se administra a una muestra piloto independiente" not in plano)
    chk("Sin marcas ni calificaciones prellenadas en el expediente",
        not re.search(r"\[\s*[xX]\s*\]", todo) and "×" not in todo)
    # Preliminares+panorama (retrato), hojas 01 y 02 (apaisadas), certificado
    # 03 y cuestionario (retrato), matrices y fichas (apaisada).
    esperado_secs = [("unajma", 3), ("apaisada", 4), ("apaisada", 4),
                     ("unajma", 3), ("unajma", 3), ("apaisada", 4)]
    geoms = []
    for s in secs:
        if abs(s.page_width.cm - 21.0) < 0.1 and abs(s.left_margin.cm - 3.0) < 0.05:
            geoms.append(("unajma", 3))
        elif abs(s.page_width.cm - 29.7) < 0.1 and abs(s.left_margin.cm - 2.5) < 0.05:
            geoms.append(("apaisada", 4))
        else:
            geoms.append(("otra", 0))
    chk("Secciones: retrato institucional y apaisada con margenes exactos", geoms == esperado_secs, str(geoms))
    chk("Ancho util retrato ~8788 dxa y apaisada ~14003 dxa",
        all(8780 <= int(round((s.page_width.cm - s.left_margin.cm - s.right_margin.cm) * 567)) <= 8795
            if s.page_width.cm < 25.0 else
            13995 <= int(round((s.page_width.cm - s.left_margin.cm - s.right_margin.cm) * 567)) <= 14010
            for s in secs))
    return res


def verificar_pdf(pdf):
    """Paginacion: cada pieza inicia arriba de pagina y no hay paginas vacias."""
    import pymupdf

    def _norma(s):
        return re.sub(r"\s+", " ", s).strip().lower()

    doc = pymupdf.open(str(pdf))
    res = []
    textos = [p.get_text() for p in doc]
    # Linea inicial de cada pagina: primera linea no vacia que no sea el folio.
    inicios = []
    for t in textos:
        lineas = [l.strip() for l in t.splitlines() if l.strip()]
        if lineas and re.fullmatch(r"\d+", lineas[0]):
            lineas = lineas[1:]
        inicios.append(_norma(" ".join(lineas[:3])) if lineas else "")
    vacias = [i + 1 for i, t in enumerate(textos) if len(t.strip()) < 30]
    res.append(("Sin paginas vacias", not vacias, str(vacias)))
    for m in MARCADORES:
        mn = _norma(m)
        pg = next((i for i, ini in enumerate(inicios) if ini.startswith(mn)), None)
        if pg is None:
            res.append((f"Marcador '{m}' presente", False, "no encontrado"))
            continue
        res.append((f"'{m[:52]}...' abre pagina {pg + 1}", True, inicios[pg][:60]))
    plano_cert = re.sub(r"\s+", " ", TITULO_CERT_03)
    pgs = [i for i, t in enumerate(textos) if plano_cert in re.sub(r"\s+", " ", t)]
    if pgs:
        fin = next((i for i in range(pgs[0], len(textos))
                    if "cubren de manera completa la dimensión" in textos[i]), None)
        segmento = "".join(textos[pgs[0]:fin + 1]) if fin is not None else textos[pgs[0]]
        cierre = all(x in segmento for x in ("Firma del juez validador", "Apellidos y nombres del juez validador"))
        res.append(("Certificado 03 cierra con su bloque de cierre y notas", cierre,
                    f"titulo paginas {[p + 1 for p in pgs]}, nota pagina {fin + 1 if fin is not None else None}"))
    else:
        res.append(("Certificado 03 presente en el PDF", False, "no encontrado"))
    # Cada hoja nueva 01/02 debe cerrar con su firma en el segmento hasta la
    # siguiente pieza (sin firma cortada a pagina huérfana).
    for titulo, etiqueta in ((TITULO_HOJA_01, "Hoja 01"), (TITULO_HOJA_02, "Hoja 02")):
        plano = re.sub(r"\s+", " ", titulo)
        pg = next((i for i, t in enumerate(textos) if plano in re.sub(r"\s+", " ", t)), None)
        if pg is None:
            res.append((f"{etiqueta} presente en el PDF", False, "no encontrada"))
            continue
        fin = next((i for i in range(pg, len(textos))
                    if "cubren de manera completa la dimensión" in textos[i]), None)
        if fin is None:
            res.append((f"{etiqueta} cierra con notas al pie", False, "sin nota"))
            continue
        segmento = "".join(textos[pg:fin + 1])
        cierre = all(x in segmento for x in ("Firma del juez validador",
                                             "Apellidos y nombres del juez validador"))
        res.append((f"{etiqueta} cierra con su bloque de cierre y notas", cierre,
                    f"titulo pagina {pg + 1}, nota pagina {fin + 1}"))
    res.append(("Total de paginas", True, str(len(doc))))
    return res


# ---------------------------------------------------------------------- CLI


def generar_todos():
    import shutil
    RUTA_SALIDA.mkdir(parents=True, exist_ok=True)
    rutas = [RUTA_SALIDA / nombre_ejemplar(n) for n in (1, 2, 3)]
    existentes = [r for r in rutas if r.exists()]
    if existentes:
        for r in existentes:
            print(f"[OMITIDO] {r.name} ya existe; no se sobrescribe")
        return 0
    maestro = rutas[0]
    construir_expediente(1).save(str(maestro))
    res = verificar_docx(maestro)
    malos = [r for r in res if not r[1]]
    if malos:
        maestro.unlink()
        print(f"[ABORTADO] {maestro.name}: {len(malos)} comprobaciones no conformes; archivo eliminado")
        for nom, _, det in malos:
            print(f"   FALLA {nom} {det}")
        return 1
    print(f"[OK] {maestro.name} ({maestro.stat().st_size:,} bytes): {len(res)} comprobaciones conformes")
    for r in rutas[1:]:
        shutil.copyfile(maestro, r)
        print(f"[OK] {r.name} copia byte-identica del ejemplar 01 ({r.stat().st_size:,} bytes)")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="Expediente COMPLETO de validacion Fany x3 (v05: hoja informativa VI + panorama + hojas de "
                    "evaluacion 01/02 apaisadas + certificado Instrumento 03 Modalidad A + cuestionario integro)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--generar", action="store_true")
    g.add_argument("--verificar", action="store_true")
    g.add_argument("--verificar-pdf", metavar="PDF")
    g.add_argument("--generar-compacto", action="store_true")
    g.add_argument("--verificar-compacto", action="store_true")
    g.add_argument("--verificar-pdf-compacto", metavar="PDF")
    g.add_argument("--generar-v07", action="store_true")
    g.add_argument("--verificar-v07", action="store_true")
    g.add_argument("--verificar-pdf-v07", metavar="PDF")
    g.add_argument("--generar-v08", action="store_true")
    g.add_argument("--verificar-v08", action="store_true")
    g.add_argument("--verificar-pdf-v08", metavar="PDF")
    g.add_argument("--generar-v09", action="store_true")
    g.add_argument("--verificar-v09", action="store_true")
    g.add_argument("--generar-pdf-v09", action="store_true")
    g.add_argument("--verificar-pdf-v09", nargs="?", const=str(DIR_V09 / f"EXPEDIENTE_VALIDACION_SIVAC_EXPERTO_01_{VERSION_V09}.pdf"), metavar="PDF")
    a = ap.parse_args()
    if a.generar:
        return generar_todos()
    if a.verificar:
        rc = 0
        for n in (1, 2, 3):
            ruta = RUTA_SALIDA / nombre_ejemplar(n)
            if not ruta.exists():
                print(f"[FALTA] {ruta.name}")
                rc = 1
                continue
            res = verificar_docx(ruta)
            malos = [r for r in res if not r[1]]
            print(f"{ruta.name}: {len(res) - len(malos)}/{len(res)} conformes")
            for nom, _, det in malos:
                print(f"   FALLA {nom} {det}")
            rc |= 1 if malos else 0
        return rc
    if a.verificar_pdf:
        rc = 0
        for nom, ok, det in verificar_pdf(a.verificar_pdf):
            print(f"  [{'OK' if ok else 'FALLA'}] {nom} {det}")
            rc |= 0 if ok else 1
        return rc
    if a.generar_compacto:
        import shutil
        destino = RUTA_SALIDA / "compacto_v06"
        destino.mkdir(parents=True, exist_ok=True)
        rutas = [destino / nombre_compacto(n) for n in (1, 2, 3)]
        existentes = [r for r in rutas if r.exists()]
        if existentes:
            for r in existentes:
                print(f"[OMITIDO] {r.name} ya existe; no se sobrescribe")
            return 0
        maestro = rutas[0]
        construir_compacto().save(str(maestro))
        res = verificar_compacto(maestro)
        malos = [r for r in res if not r[1]]
        if malos:
            maestro.unlink()
            print(f"[ABORTADO] {maestro.name}: {len(malos)} comprobaciones no conformes; archivo eliminado")
            for nom, _, det in malos:
                print(f"   FALLA {nom} {det}")
            return 1
        print(f"[OK] {maestro.name} ({maestro.stat().st_size:,} bytes): {len(res)} comprobaciones conformes")
        for r in rutas[1:]:
            shutil.copyfile(maestro, r)
            print(f"[OK] {r.name} copia byte-identica del ejemplar 01 ({r.stat().st_size:,} bytes)")
        return 0
    if a.verificar_compacto:
        rc = 0
        destino = RUTA_SALIDA / "compacto_v06"
        for n in (1, 2, 3):
            ruta = destino / nombre_compacto(n)
            if not ruta.exists():
                print(f"[FALTA] {ruta.name}")
                rc = 1
                continue
            res = verificar_compacto(ruta)
            malos = [r for r in res if not r[1]]
            print(f"{ruta.name}: {len(res) - len(malos)}/{len(res)} conformes")
            for nom, _, det in malos:
                print(f"   FALLA {nom} {det}")
            rc |= 1 if malos else 0
        return rc
    if a.verificar_pdf_compacto:
        rc = 0
        for nom, ok, det in verificar_pdf_compacto(a.verificar_pdf_compacto):
            print(f"  [{'OK' if ok else 'FALLA'}] {nom} {det}")
            rc |= 0 if ok else 1
        return rc
    if a.generar_v07:
        return generar_v07()
    if a.verificar_v07:
        rc = 0
        for n in (1, 2, 3):
            ruta = DIR_V07 / nombre_v07(n)
            if not ruta.exists():
                print(f"[FALTA] {ruta.name}")
                rc = 1
                continue
            res = verificar_v07(ruta)
            malos = [r for r in res if not r[1]]
            print(f"{ruta.name}: {len(res) - len(malos)}/{len(res)} conformes")
            for nom, _, det in malos:
                print(f"   FALLA {nom} {det}")
            rc |= 1 if malos else 0
        return rc
    if a.verificar_pdf_v07:
        rc = 0
        for nom, ok, det in verificar_pdf_v07(a.verificar_pdf_v07):
            print(f"  [{'OK' if ok else 'FALLA'}] {nom} {det}")
            rc |= 0 if ok else 1
        return rc
    if a.generar_v08:
        return generar_v08()
    if a.verificar_v08:
        rc = 0
        for n in (1, 2, 3):
            ruta = DIR_V08 / nombre_v08(n)
            if not ruta.exists():
                print(f"[FALTA] {ruta.name}")
                rc = 1
                continue
            res = verificar_v08(ruta)
            malos = [r for r in res if not r[1]]
            print(f"{ruta.name}: {len(res) - len(malos)}/{len(res)} conformes")
            for nom, _, det in malos:
                print(f"   FALLA {nom} {det}")
            rc |= 1 if malos else 0
        return rc
    if a.verificar_pdf_v08:
        rc = 0
        for nom, ok, det in verificar_pdf_v08(a.verificar_pdf_v08):
            print(f"  [{'OK' if ok else 'FALLA'}] {nom} {det}")
            rc |= 0 if ok else 1
        return rc
    if a.generar_v09:
        return generar_v09()
    if a.verificar_v09:
        rc = 0
        for n in (1, 2, 3):
            ruta = DIR_V09 / nombre_v09(n)
            if not ruta.exists():
                print(f"[FALTA] {ruta.name}")
                rc = 1
                continue
            res = verificar_v09(ruta)
            malos = [r for r in res if not r[1]]
            print(f"{ruta.name}: {len(res) - len(malos)}/{len(res)} conformes")
            for nom, _, det in malos:
                print(f"   FALLA {nom} {det}")
            rc |= 1 if malos else 0
        return rc
    if a.generar_pdf_v09:
        maestro = DIR_V09 / nombre_v09(1)
        if not maestro.exists():
            print(f"[FALTA] {maestro.name}; genere primero con --generar-v09")
            return 1
        pdf_01 = DIR_V09 / f"EXPEDIENTE_VALIDACION_SIVAC_EXPERTO_01_{VERSION_V09}.pdf"
        quir.exportar_docx_a_pdf(maestro, pdf_01)
        print(f"[OK] PDF generado vía Word COM: {pdf_01.name} ({pdf_01.stat().st_size:,} bytes)")
        import shutil
        for n in (2, 3):
            pdf_n = DIR_V09 / f"EXPEDIENTE_VALIDACION_SIVAC_EXPERTO_0{n}_{VERSION_V09}.pdf"
            shutil.copyfile(pdf_01, pdf_n)
            print(f"[OK] {pdf_n.name} copia byte-idéntica del PDF 01 ({pdf_n.stat().st_size:,} bytes)")
        return 0
    if a.verificar_pdf_v09:
        rc = 0
        from pathlib import Path
        ruta_pdf = Path(a.verificar_pdf_v09)
        if not ruta_pdf.exists():
            print(f"[FALTA] {ruta_pdf}")
            return 1
        for nom, ok, det in verificar_pdf_v09(ruta_pdf):
            print(f"  [{'OK' if ok else 'FALLA'}] {nom} {det}")
            rc |= 0 if ok else 1
        return rc
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
