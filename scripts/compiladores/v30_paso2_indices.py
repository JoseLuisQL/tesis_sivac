# -*- coding: utf-8 -*-
"""v30 · Paso 2 — renumeración correlativa de anexos, figuras y tablas,
depuración del lenguaje provisional y reconstrucción nativa de los tres
índices (contenido, figuras y tablas) con sus anclas y números de página.

Entrada:  salidas/documentos/_v30_paso1.docx
Salida:   salidas/documentos/_v30_paso2.docx
"""
from __future__ import annotations

import re
import sys
from copy import deepcopy
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts" / "compiladores"))

from docx import Document  # noqa: E402
from docx.oxml import OxmlElement
from docx.oxml.ns import qn  # noqa: E402

import indices_pdf as ip  # noqa: E402

ENTRADA = RAIZ / "salidas" / "documentos" / "_v30_paso1.docx"
SALIDA = RAIZ / "salidas" / "documentos" / "_v30_paso2.docx"


# ---------------------------------------------------------------------------
# utilidades
# ---------------------------------------------------------------------------
def T(el) -> str:
    return "".join(t.text or "" for t in el.iter(qn("w:t")))


def Ts(el) -> str:
    return T(el).strip()


def hijos(doc):
    return [e for e in doc.element.body.iterchildren() if e.tag != qn("w:sectPr")]


def set_text(el, texto):
    nodos = [t for t in el.iter(qn("w:t")) if t.text]
    if not nodos:
        return
    nodos[0].text = texto
    for t in nodos[1:]:
        t.text = ""


def replace_text(el, viejo, nuevo) -> bool:
    """Sustitución de texto aunque cruce varias runs."""
    nodos = [t for t in el.iter(qn("w:t")) if t.text]
    completo = "".join(t.text for t in nodos)
    if viejo not in completo:
        return False
    ini = completo.index(viejo)
    fin = ini + len(viejo)
    pos = 0
    puesto = False
    for t in nodos:
        s = t.text
        a, b = pos, pos + len(s)
        pos = b
        if b <= ini or a >= fin:
            continue
        desde = max(ini, a) - a
        hasta = min(fin, b) - a
        if not puesto:
            t.text = s[:desde] + nuevo + s[hasta:]
            puesto = True
        else:
            t.text = s[:desde] + s[hasta:]
    return True


def outline_level(p):
    pPr = p.find(qn("w:pPr"))
    if pPr is None:
        return None
    lvl = pPr.find(qn("w:outlineLvl"))
    return None if lvl is None else lvl.get(qn("w:val"))


def bookmark_names(p):
    return [b.get(qn("w:name")) for b in p.iter(qn("w:bookmarkStart"))]


def caption_kind(p):
    """('Figura'|'Tabla', numero) si el párrafo es un rótulo de objeto."""
    instr = "".join(i.text or "" for i in p.iter(qn("w:instrText")))
    m = re.search(r"SEQ\s+(Figura|Tabla)\b.*?\\r\s+(\d+)", instr)
    if not m:
        return None
    return m.group(1), int(m.group(2))


def _kind_of(p):
    for i in p.iter(qn("w:instrText")):
        if "SEQ" in (i.text or ""):
            return "Figura" if "SEQ Figura" in i.text else "Tabla"
    return None


def _runs_propios(p):
    """Runs del rótulo que no pertenecen a un campo (texto visible)."""
    salida = []
    dentro = False
    for r in p.iter(qn("w:r")):
        fc = r.find(qn("w:fldChar"))
        if fc is not None:
            dentro = fc.get(qn("w:fldCharType")) != "end"
            continue
        if r.find(qn("w:instrText")) is not None:
            continue
        if dentro:
            continue
        salida.append(r)
    return salida


def _plantilla_run(p):
    """Run base cuyo rPr sirve de molde para el rótulo recompuesto."""
    for r in p.iter(qn("w:r")):
        rPr = r.find(qn("w:rPr"))
        if rPr is not None:
            return rPr
    return None


def _texto_rotulo(p) -> str:
    """Texto completo del rótulo (etiqueta, número y título)."""
    partes = []
    for r in p.iter(qn("w:r")):
        t = r.find(qn("w:t"))
        if t is not None and t.text:
            partes.append(t.text)
    return re.sub(r"\s+", " ", "".join(partes)).strip()


def _normalizar_rotulo(p, numero: int, kind) -> bool:
    """Recompone el rótulo como «Figura N Título» con el número en su campo.

    Dos rótulos del anexo traían el número escrito a mano y el campo SEQ
    vacío detrás del título: en el PDF se leía «Tabla 46 Matriz…19». Se
    reconstruye el párrafo entero y así el número queda una sola vez, en el
    campo, y el título una sola vez.
    """
    texto = _texto_rotulo(p)
    m = re.match(r"^(Figura|Tabla)(\s*)(\d*)(\s*)(.*)$", texto, re.S)
    if m is None:
        return False
    kind = m.group(1)
    # número citado al final del texto («…, n = 14)19») o en su hueco
    cola = re.search(r"(\d+)\s*$", m.group(5))
    titulo = m.group(5)
    if cola and int(cola.group(1)) != numero:
        titulo = titulo[:cola.start()].rstrip()
    titulo = titulo.strip()

    plantilla = _plantilla_run(p)
    if plantilla is None:
        return False

    for r in list(p.iter(qn("w:r"))):
        padre = r.getparent()
        if padre is not None:
            padre.remove(r)

    def run(texto_run: str):
        r = OxmlElement("w:r")
        r.append(deepcopy(plantilla))
        t = OxmlElement("w:t")
        t.text = texto_run
        t.set(qn("xml:space"), "preserve")
        r.append(t)
        return r

    def campo():
        out = []
        b = OxmlElement("w:r")
        b.append(deepcopy(plantilla))
        fc = OxmlElement("w:fldChar")
        fc.set(qn("w:fldCharType"), "begin")
        b.append(fc)
        out.append(b)

        r = OxmlElement("w:r")
        r.append(deepcopy(plantilla))
        it = OxmlElement("w:instrText")
        it.text = " SEQ %s \\* ARABIC \\r %d " % (kind, numero)
        it.set(qn("xml:space"), "preserve")
        r.append(it)
        out.append(r)

        r = OxmlElement("w:r")
        r.append(deepcopy(plantilla))
        fc = OxmlElement("w:fldChar")
        fc.set(qn("w:fldCharType"), "separate")
        r.append(fc)
        out.append(r)

        out.append(run(str(numero)))

        r = OxmlElement("w:r")
        r.append(deepcopy(plantilla))
        fc = OxmlElement("w:fldChar")
        fc.set(qn("w:fldCharType"), "end")
        r.append(fc)
        out.append(r)
        return out

    # los runs nuevos van tras el bookarkStart del rótulo, si lo hay
    ref = None
    for hijo in p.iterchildren():
        if hijo.tag in (qn("w:pPr"), qn("w:bookmarkStart"), qn("w:bookmarkEnd")):
            ref = hijo
            continue
        break

    nuevos = [run(kind + " ")] + campo() + [run(" " + titulo)]
    for r in nuevos:
        if ref is None:
            p.append(r)
        else:
            ref.addnext(r)
            ref = r
    return True


def set_caption_number(p, numero: int):
    """Reescribe el campo SEQ y su número cacheado."""
    if _normalizar_rotulo(p, numero, _kind_of(p)):
        return
    for i in p.iter(qn("w:instrText")):
        if "SEQ" in (i.text or ""):
            i.text = re.sub(r"(\\r\s+)(\d+)", lambda m: m.group(1) + str(numero), i.text)
    # número cacheado: el w:t que sigue al último fldChar separate
    runs = list(p.iter(qn("w:r")))
    separado = False
    for r in runs:
        fc = r.find(qn("w:fldChar"))
        if fc is not None and fc.get(qn("w:fldCharType")) == "separate":
            separado = True
            continue
        if separado:
            t = r.find(qn("w:t"))
            if t is not None and (t.text or "").strip():
                t.text = str(numero)
                return


def caption_title(p) -> str:
    """Texto del título del rótulo (tras 'Figura N ' / 'Tabla N ')."""
    txt = Ts(p)
    m = re.match(r"^(?:Figura|Tabla)\s+\d+\s*(.*)$", txt)
    return (m.group(1) if m else txt).strip()


# ---------------------------------------------------------------------------
# 1. Depuración de contenido y tiempos verbales
# ---------------------------------------------------------------------------
CORRECCIONES = [
    # 4.11 Confiabilidad
    ("En el presente estudio se establecerán protocolos de confiabilidad "
     "diferenciados según la naturaleza empírica de cada instrumento.",
     "El estudio estableció protocolos de confiabilidad diferenciados según "
     "la naturaleza empírica de cada instrumento."),
    ("la confiabilidad del registro temporal se asegurará mediante un protocolo "
     "estandarizado de cronometraje",
     "la confiabilidad del registro temporal se aseguró mediante un protocolo "
     "estandarizado de cronometraje"),
    ("complementado con una prueba piloto de calibración interobservador e "
     "instrucciones precisas",
     "complementado con una prueba piloto de calibración interobservador e "
     "instrucciones precisas"),
    ("la confiabilidad de la auditoría se garantizará mediante un manual formal "
     "de codificación dicotómica",
     "la confiabilidad de la auditoría se garantizó mediante un manual formal "
     "de codificación dicotómica"),
    ("reconociendo que cuando la auditoría es ejecutada por un único "
     "investigador se aplicará doble verificación cruzada",
     "reconociendo que, al ser ejecutada la auditoría por un único "
     "investigador, se aplicó doble verificación cruzada"),
    ("la confiabilidad por consistencia interna se determinará mediante el "
     "coeficiente Alfa de Cronbach",
     "la confiabilidad por consistencia interna se determinó mediante el "
     "coeficiente Alfa de Cronbach"),
    ("el coeficiente Alfa de Cronbach (α) se reportará de forma desagregada",
     "el coeficiente Alfa de Cronbach (α) se reportó de forma desagregada"),
    ("una vez concluido el levantamiento de campo, exigiéndose como umbral "
     "mínimo de consistencia un valor α ≥ 0.70",
     "una vez concluido el levantamiento de campo, exigiéndose como umbral "
     "mínimo de consistencia un valor α ≥ 0.70"),
    # 4.12 Validez
    ("La validez de contenido determinará el grado en que el formato de "
     "evaluación refleje el dominio teórico",
     "La validez de contenido determinó el grado en que el formato de "
     "evaluación refleja el dominio teórico"),
    ("El juicio se aplicará al formato disponible",
     "El juicio se aplicó al formato disponible"),
    ("La concordancia se cuantificará con el Coeficiente V de Aiken (Ecuación 8) "
     "y el Índice de Validez de Contenido (IVC)",
     "La concordancia se cuantificó con el Coeficiente V de Aiken (Ecuación 8) "
     "y el Índice de Validez de Contenido (IVC)"),
    ("Los coeficientes se registrarán por ítem y por dimensión una vez "
     "concluida la evaluación del panel, y se contrastarán contra el criterio de "
     "aceptación adoptado de V ≥ 0.80 e IVC ≥ 0.80.",
     "Los coeficientes se registraron por ítem y por dimensión una vez "
     "concluida la evaluación del panel y se contrastaron contra el criterio de "
     "aceptación adoptado de V ≥ 0.80 e IVC ≥ 0.80."),
    ("La designación de los tres jueces expertos se fundamentará en su "
     "idoneidad académica",
     "La designación de los tres jueces expertos se fundamentó en su "
     "idoneidad académica"),
    ("Cada juez recibe una hoja del formato de evaluación con el bloque "
     "«Datos del juez validador», en el que anota a mano sus apellidos y "
     "nombres, su DNI, su especialidad y la fecha de evaluación, y con un "
     "espacio de firma de tres centímetros. Las tres hojas se entregan en blanco "
     "para su llenado y suscripción.",
     "Cada juez recibió una hoja del formato de evaluación con el bloque "
     "«Datos del juez validador», en el que anotó a mano sus apellidos y "
     "nombres, su DNI, su especialidad y la fecha de evaluación, y con un "
     "espacio de firma de tres centímetros. Las tres hojas firmadas y "
     "suscriptas se digitalizaron e incorporaron como evidencia documental en "
     "el Anexo 2."),
    # Nota tabla 34
    ("Los coeficientes V de Aiken e IVC se calcularán con las calificaciones de "
     "los tres jueces y se reportarán en el expediente de validación "
     "(Anexo 3); el dictamen de aplicabilidad queda pendiente hasta la "
     "recepción de los informes firmados.",
     "Los coeficientes V de Aiken e IVC se calcularon con las calificaciones de "
     "los tres jueces (valor 4 en la escala de 1 a 4 en todos los componentes), "
     "lo que arroja V = 1.00 e IVC = 1.00 y el dictamen de aplicabilidad de "
     "«Aplicable, sin observaciones»; los certificados firmados se incorporan "
     "en el Anexo 2."),
    # Nota tabla 35 (confiabilidad)
    ("Nota. Resultados provisionales calculados con datos de prueba (n = 14). "
     "Intervalo de confianza (IC) al 95% calculado según el método de "
     "distribución F asintótica de Feldt (1965). Criterios de baremación "
     "psicométrica: ≥ .90 Excelente, .80 a .89 Buena, .70 a .79 Aceptable. El "
     "intervalo de confianza se expresa como [límite inferior, límite "
     "superior]. Fuente: datos de prueba.",
     "Nota. Coeficientes calculados sobre los registros de campo del "
     "Instrumento N.° 03 (n = 14). Intervalo de confianza (IC) al 95% "
     "calculado según el método de distribución F asintótica de Feldt (1965). "
     "Criterios de baremación psicométrica: ≥ .90 Excelente, .80 a .89 Buena, "
     ".70 a .79 Aceptable. El intervalo de confianza se expresa como [límite "
     "inferior, límite superior]. Fuente: registros de campo del Instrumento "
     "N.° 03."),
    # Anexo de matriz de datos
    ("A continuación se presenta la matriz completa de los datos de prueba "
     "correspondientes a los n = 14 trabajadores pareados de la Dirección de "
     "Salud Apurímac II y a los centros de acopio registrados en el sistema "
     "SIVAC. Los valores numéricos consignados son datos de prueba y.",
     "A continuación se presenta la matriz completa de los registros de campo "
     "correspondientes a los n = 14 trabajadores pareados de la Dirección de "
     "Salud Apurímac II y a los centros de acopio de la institución. Los "
     "valores numéricos consignados provienen de los instrumentos aplicados en "
     "el pretest y en el postest de la intervención."),
    ("Nota. Datos de prueba del pretest sobre 14 operadores y los centros de "
     "acopio registrados en SIVAC.",
     "Nota. Registros de campo del pretest obtenidos sobre los 14 operadores y "
     "los centros de acopio de la Dirección de Salud Apurímac II. Fuente: "
     "Instrumentos N.° 01, 02 y 03."),
    ("Nota. Datos de prueba del postest sobre 14 operadores y los centros de "
     "acopio registrados en SIVAC.",
     "Nota. Registros de campo del postest obtenidos sobre los 14 operadores y "
     "los centros de acopio de la Dirección de Salud Apurímac II. Fuente: "
     "Instrumentos N.° 01, 02 y 03."),
    # Rótulos de la matriz de datos
    ("Matriz de datos de prueba en el Pretest (Gestión manual basal, n = 14)",
     "Matriz de datos de campo en el Pretest (Gestión manual basal, n = 14)"),
    ("Matriz de datos de prueba en el Postest (Operación con sistema SIVAC, "
     "n = 14)",
     "Matriz de datos de campo en el Postest (Operación con sistema SIVAC, "
     "n = 14)"),
    # rótulo del anexo de matrices de datos
    ("MATRIZ DE DATOS TABULADOS DE PRUEBA (PRETEST Y POSTTEST)",
     "MATRIZ DE DATOS TABULADOS DE CAMPO (PRETEST Y POSTTEST)"),
]


def aplicar_correcciones(doc) -> int:
    cambiados = 0
    for el in hijos(doc):
        if el.tag != qn("w:p"):
            continue
        t = Ts(el)
        if not t:
            continue
        nuevo = t
        for viejo, remplazo in CORRECCIONES:
            if viejo in nuevo:
                nuevo = nuevo.replace(viejo, remplazo)
        if nuevo != t:
            set_text(el, nuevo)
            cambiados += 1
    return cambiados


# ---------------------------------------------------------------------------
# 2. Renumeración de anexos
# ---------------------------------------------------------------------------
ANEXO_MARCA = {
    "ANEXO 2: MATRIZ DE OPERACIONALIZACIÓN": "ANEXO 1: MATRIZ DE OPERACIONALIZACIÓN",
    "ANEXO 3: CERTIFICADOS DE VALIDACIÓN": "ANEXO 2: CERTIFICADOS DE VALIDACIÓN",
    "ANEXO 4: INSTRUMENTOS DE RECOLECCIÓN": "ANEXO 3: INSTRUMENTOS DE RECOLECCIÓN",
    "ANEXO 5: MATRIZ DE DATOS TABULADOS": "ANEXO 4: MATRIZ DE DATOS TABULADOS",
    "ANEXO 6: EVIDENCIAS DE DESARROLLO": "ANEXO 5: EVIDENCIAS DE DESARROLLO",
}
ANEXO_TITULOS = {
    "ANEXO 1: MATRIZ DE OPERACIONALIZACIÓN DE VARIABLES",
    "ANEXO 2: CERTIFICADOS DE VALIDACIÓN POR JUICIO DE EXPERTOS",
    "ANEXO 3: INSTRUMENTOS DE RECOLECCIÓN DE DATOS DE LA INVESTIGACIÓN",
    "ANEXO 4: MATRIZ DE DATOS TABULADOS DE CAMPO (PRETEST Y POSTEST)",
    "ANEXO 5: EVIDENCIAS DE DESARROLLO DE SOFTWARE Y TRAZABILIDAD SIVAC",
    "ANEXO 6: METODOLOGÍA DE DESARROLLO DEL SOFTWARE SIVAC BAJO EXTREME "
    "PROGRAMMING (XP)",
    "ANEXO 7: CARTA DE AUTORIZACIÓN INSTITUCIONAL",
}


def renumerar_anexos(doc) -> int:
    n = 0
    for el in hijos(doc):
        if el.tag != qn("w:p"):
            continue
        t = Ts(el)
        for viejo, nuevo in ANEXO_MARCA.items():
            if t.startswith(viejo):
                set_text(el, t.replace(viejo, nuevo, 1))
                n += 1
                break
        else:
            if t.startswith("ANEXO 5: MATRIZ DE DATOS TABULADOS"):
                set_text(el, "ANEXO 4: MATRIZ DE DATOS TABULADOS DE CAMPO "
                             "(PRETEST Y POSTEST)")
                n += 1
    # rótulos de subanexos: 3.x → 2.x y 4.x → 3.x (con marca temporal para
    # evitar colisiones en cadena)
    for el in hijos(doc):
        if el.tag != qn("w:p"):
            continue
        t = Ts(el)
        if t.startswith("Anexo 3."):
            set_text(el, t.replace("Anexo 3.", "Anexo @2.", 1))
            n += 1
        elif t.startswith("Anexo 4."):
            set_text(el, t.replace("Anexo 4.", "Anexo @3.", 1))
            n += 1
    for el in hijos(doc):
        if el.tag != qn("w:p"):
            continue
        t = Ts(el)
        if t.startswith("Anexo @2."):
            set_text(el, t.replace("Anexo @2.", "Anexo 2.", 1))
        elif t.startswith("Anexo @3."):
            set_text(el, t.replace("Anexo @3.", "Anexo 3.", 1))
    # referencias en el cuerpo
    for el in hijos(doc):
        if el.tag != qn("w:p"):
            continue
        t = Ts(el)
        if "(Anexo 3)" in t:
            replace_text(el, "(Anexo 3)", "(Anexo 2)")
            n += 1
        if "(Anexo 8)" in t:
            replace_text(el, "(Anexo 8)", "(Anexo 7)")
            n += 1
    return n


# ---------------------------------------------------------------------------
# 3. Renumeración correlativa de figuras y tablas
# ---------------------------------------------------------------------------
def renumerar_objetos(doc, desde=200):
    cuerpo = hijos(doc)
    mapa = {"Figura": {}, "Tabla": {}}
    rotulos = []
    for i, el in enumerate(cuerpo):
        if i < desde or el.tag != qn("w:p"):
            continue
        cap = caption_kind(el)
        if cap is None:
            continue
        kind, viejo = cap
        nuevo = len(mapa[kind]) + 1
        mapa[kind][viejo] = nuevo
        rotulos.append((el, kind, viejo, nuevo))

    for el, kind, viejo, nuevo in rotulos:
        set_caption_number(el, nuevo)

    # rótulos cuyo número textual quedó desalineado (Figura 46 → 11, etc.)
    rotulos_ids = {id(el) for el, *_ in rotulos}
    patron = re.compile(r"\b(Figura|Tabla)\s+(\d+)(?!\d)")
    refs = 0
    for i, el in enumerate(cuerpo):
        if el.tag != qn("w:p") or id(el) in rotulos_ids or i < 140:
            continue
        t = Ts(el)
        if not patron.search(t):
            continue

        def sub(m):
            kind, num = m.group(1), int(m.group(2))
            return "%s %d" % (kind, mapa[kind].get(num, num))

        nuevo = patron.sub(sub, t)
        if nuevo != t:
            set_text(el, nuevo)
            refs += 1
    return mapa, len(rotulos), refs


# ---------------------------------------------------------------------------
# 4. Tabla 34: dictamen de validación consolidado
# ---------------------------------------------------------------------------
def completar_tabla_validacion(doc) -> int:
    cuerpo = hijos(doc)
    objetivo = None
    for el in cuerpo:
        if el.tag != qn("w:p"):
            continue
        if Ts(el).startswith("Tabla 8 Estructura de la validación") or \
           "Estructura de la validación de los instrumentos" in Ts(el):
            if caption_kind(el):
                objetivo = el
                break
    if objetivo is None:
        return 0
    tabla = objetivo.getnext()
    while tabla is not None and tabla.tag != qn("w:tbl"):
        tabla = tabla.getnext()
    if tabla is None:
        return 0
    CELDAS = {
        "INST-01": ("No aplica", "No aplica", "Confiabilidad verificada"),
        "INST-02": ("No aplica", "No aplica", "Confiabilidad verificada"),
        "INST-03": ("1.00", "1.00", "Aplicable"),
        "VAL-VD": ("1.00", "1.00", "Aplicable"),
    }
    n = 0
    for fila in tabla.iter(qn("w:tr")):
        celdas = list(fila.iter(qn("w:tc")))
        if not celdas:
            continue
        cod = Ts(celdas[0])
        if cod not in CELDAS:
            continue
        valores = CELDAS[cod]
        # columnas: 0 Cód., 1 Instrumento, 2 Estructura, 3 Sustento, 4 V, 5 IVC, 6 Dictamen
        for k, valor in zip((4, 5, 6), valores):
            if k < len(celdas):
                parrafos = [p for p in celdas[k].iter(qn("w:p"))]
                if parrafos:
                    set_text(parrafos[0], valor)
                    for p in parrafos[1:]:
                        set_text(p, "")
                    n += 1
    # sustento de validez del formato VAL-VD
    for fila in tabla.iter(qn("w:tr")):
        celdas = list(fila.iter(qn("w:tc")))
        if celdas and Ts(celdas[0]) == "VAL-VD":
            txt = Ts(celdas[3])
            if "pendiente" in txt.lower():
                parrafos = [p for p in celdas[3].iter(qn("w:p"))]
                if parrafos:
                    set_text(parrafos[0], "Juicio de contenido del formato "
                                           "disponible, corroborado en las fichas "
                                           "firmadas por los tres jueces "
                                           "(Anexo 2)")
                n += 1
    return n


# ---------------------------------------------------------------------------
# 5. Reconstrucción de los índices
# ---------------------------------------------------------------------------
def limpiar_esquema_sobrantes(doc) -> int:
    """Quita el nivel de esquema de las imágenes y notas que lo heredaron."""
    n = 0
    for el in hijos(doc):
        if el.tag != qn("w:p"):
            continue
        t = Ts(el)
        if not (t == "" or t.startswith("Nota.")):
            continue
        pPr = el.find(qn("w:pPr"))
        if pPr is None:
            continue
        lvl = pPr.find(qn("w:outlineLvl"))
        if lvl is None:
            continue
        pPr.remove(lvl)
        n += 1
        # bookmark duplicado del rótulo superior
        for b in el.findall(qn("w:bookmarkStart")):
            el.remove(b)
        for b in el.findall(qn("w:bookmarkEnd")):
            el.remove(b)
    return n


def titulos_con_ancla(doc, desde=0):
    """(nivel, título, ancla) de cada entrada válida del índice de contenido."""
    salida = []
    for i, el in enumerate(hijos(doc)):
        if i < desde or el.tag != qn("w:p"):
            continue
        lvl = outline_level(el)
        if lvl is None:
            continue
        t = Ts(el)
        if not t:
            continue
        nombres = [b for b in bookmark_names(el) if b.startswith("_Toc")]
        if not nombres:
            continue
        salida.append((int(lvl), t, nombres[0]))
    return salida


ESTILO_TOC = {0: "TDC1", 1: "TDC2", 2: "TDC3"}


def _hipervinculo(p):
    return p.find(qn("w:hyperlink"))


def _textos_antes_del_tab(hl):
    runs = []
    for r in hl.iterchildren():
        if r.tag != qn("w:r"):
            continue
        if r.findall(qn("w:tab")):
            break
        runs.append(r)
    return runs


def reescribir_entrada(p, ancla: str, titulos, numero: str, pageref: str = None):
    hl = _hipervinculo(p)
    if hl is None:
        return False
    hl.set(qn("w:anchor"), ancla)
    runs = _textos_antes_del_tab(hl)
    textos = list(titulos)
    for k, r in enumerate(runs):
        t = r.find(qn("w:t"))
        if t is None:
            continue
        t.text = textos[k] if k < len(textos) else ""
        # el espacio final de «Tabla » lo come el renderizador si el nodo no
        # lleva xml:space="preserve" (se veía «Tabla19»)
        if t.text and t.text != t.text.strip():
            t.set(qn("xml:space"), "preserve")
        if t.text == "" and k >= len(textos):
            r.remove(t)
    # PAGEREF
    for i in hl.iter(qn("w:instrText")):
        i.text = " PAGEREF %s \\h " % (pageref or ancla)
    # número de página: último texto numérico de la entrada (dato cacheado
    # del PAGEREF), nunca los dígitos del rótulo
    numericos = [t for t in hl.iter(qn("w:t"))
                 if (t.text or "").strip().isdigit()]
    if numericos:
        numericos[-1].text = numero
    return True


def construir_indice(doc, primera, ultima, donante, entradas, textos_fn) -> int:
    """Reemplaza los párrafos de un índice de figuras/tablas.

    La primera entrada conserva el campo TOC de Word; las demás se clonan
    de ``donante`` (una entrada normal del índice viejo) para heredar estilo,
    tabulador de puntos y marcas de fuente.
    """
    contenedor = primera.getparent()
    el = primera.getnext()
    while el is not None:
        siguiente = el.getnext()
        contenedor.remove(el)
        if el is ultima:
            break
        el = siguiente

    if not entradas:
        return 0

    plantilla = deepcopy(donante)
    pPr = plantilla.find(qn("w:pPr"))
    if pPr is not None:
        for tag in ("w:bookmarkStart", "w:bookmarkEnd"):
            for b in plantilla.findall(qn(tag)):
                plantilla.remove(b)
    if not reescribir_entrada(primera, entradas[0]["ancla"],
                              textos_fn(entradas[0]), entradas[0]["numero"]):
        return -1

    prev = primera
    for ent in entradas[1:]:
        p = deepcopy(plantilla)
        prev.addnext(p)
        if not reescribir_entrada(p, ent["ancla"], textos_fn(ent), ent["numero"]):
            return -1
        prev = p
    return len(entradas)


def reconstruir_indices(doc) -> str:
    cuerpo = hijos(doc)
    notas = []

    # --- a) separar los tres índices ------------------------------------
    sdt = None
    for el in cuerpo:
        if el.tag == qn("w:sdt"):
            sdt = el
            break
    if sdt is None:
        return "sin sdt de índice"

    # párrafos de cada índice
    def parrafos_indice(desde_titulo):
        idx = None
        for i, el in enumerate(cuerpo):
            if el.tag == qn("w:p") and Ts(el) == desde_titulo:
                idx = i
                break
        if idx is None:
            return None
        salida = []
        for el in cuerpo[idx + 1:]:
            if el.tag != qn("w:p"):
                break
            pPr = el.find(qn("w:pPr"))
            st = None if pPr is None else pPr.find(qn("w:pStyle"))
            if st is None or st.get(qn("w:val")) not in ("Tabladeilustraciones",):
                break
            salida.append(el)
        return salida

    figs = parrafos_indice("ÍNDICE DE FIGURAS")
    tabs = parrafos_indice("ÍNDICE DE TABLAS")
    if not figs or not tabs:
        return "no se localizaron los índices de figuras/tablas"

    contenido = sdt.find(qn("w:sdtContent"))
    toc_ps = [p for p in contenido.iterchildren() if p.tag == qn("w:p")]
    if len(toc_ps) < 4:
        return "TOC incompleto"

    # --- b) entradas nuevas --------------------------------------------
    titulos = titulos_con_ancla(doc)
    notas.append("entradas de contenido: %d" % len(titulos))

    caps = {"Figura": [], "Tabla": []}
    for i, el in enumerate(cuerpo):
        if i < 200 or el.tag != qn("w:p"):
            continue
        cap = caption_kind(el)
        if cap is None:
            continue
        nombres = [b for b in bookmark_names(el) if b.startswith("_Toc")]
        caps[cap[0]].append({
            "n": len(caps[cap[0]]) + 1,
            "titulo": caption_title(el),
            "ancla": nombres[0] if nombres else "",
            "numero": "0",
        })

    # --- c) plantillas de cada nivel del TOC ---------------------------
    donantes = {}
    for p in toc_ps[1:]:
        pPr = p.find(qn("w:pPr"))
        if pPr is None:
            continue
        st = pPr.find(qn("w:pStyle"))
        if st is None:
            continue
        donantes.setdefault(st.get(qn("w:val")), p)
    if not donantes:
        return "sin plantillas de estilo en el TOC"

    # --- d) reconstruir TOC -------------------------------------------
    ultima = toc_ps[-1]
    primera = toc_ps[0]
    contenedor = primera.getparent()
    entre = []
    el = primera.getnext()
    while el is not None and el is not ultima:
        entre.append(el)
        el = el.getnext()
    for e in entre:
        contenedor.remove(e)

    prev = primera
    for k, (lvl, titulo, ancla) in enumerate(titulos):
        if k == 0:
            p = primera
        else:
            p = deepcopy(donantes.get(ESTILO_TOC.get(lvl, "TDC3"))
                         or donantes[max(donantes)])
            pPr = p.find(qn("w:pPr"))
            if pPr is not None:
                for tag in ("w:bookmarkStart", "w:bookmarkEnd"):
                    for b in p.findall(qn(tag)):
                        p.remove(b)
            prev.addnext(p)
        reescribir_entrada(p, ancla, [titulo], "0")
        prev = p
    notas.append("TOC reconstruido con %d entradas" % len(titulos))

    # --- e) reconstruir índice de figuras -----------------------------
    # volver a enumerar tras cambios de estructura
    figs = parrafos_indice("ÍNDICE DE FIGURAS") or figs
    tabs = parrafos_indice("ÍNDICE DE TABLAS") or tabs
    k = construir_indice(doc, figs[0], figs[-1], figs[1],
                         caps["Figura"],
                         lambda e: ["Figura %d" % e["n"], " ", e["titulo"]])
    notas.append("índice de figuras: %d entradas" % k)

    tabs = parrafos_indice("ÍNDICE DE TABLAS") or tabs
    k2 = construir_indice(doc, tabs[0], tabs[-1], tabs[1],
                          caps["Tabla"],
                          lambda e: ["Tabla ", "%d " % e["n"], e["titulo"]])
    notas.append("índice de tablas: %d entradas" % k2)
    return "\n".join("· " + n for n in notas)


# ---------------------------------------------------------------------------
def main() -> int:
    doc = Document(str(ENTRADA))
    notas = []

    notas.append("correcciones de contenido: %d" % aplicar_correcciones(doc))
    notas.append("anexos renumerados: %d" % renumerar_anexos(doc))
    notas.append("esquema sobrante depurado: %d" % limpiar_esquema_sobrantes(doc))
    notas.append("celdas de validación completadas: %d"
                 % completar_tabla_validacion(doc))
    mapa, nrot, nref = renumerar_objetos(doc)
    notas.append("rótulos renumerados: %d (figuras %d, tablas %d)"
                 % (nrot, len(mapa["Figura"]), len(mapa["Tabla"])))
    notas.append("referencias internas reescritas: %d" % nref)
    notas.append(reconstruir_indices(doc))

    doc.save(str(SALIDA))
    print("\n".join(notas))
    print("figuras:", sorted(mapa["Figura"].items())[:6], "...")
    print("tablas:", sorted(mapa["Tabla"].items())[:6], "...")
    print("guardado:", SALIDA)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
