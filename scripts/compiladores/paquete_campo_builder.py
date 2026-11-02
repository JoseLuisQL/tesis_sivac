# -*- coding: utf-8 -*-
"""
Constructor canónico del paquete de campo SIVAC y de la guía de llenado.

Emite los formularios individuales de un trabajador (código TRAB-XX) y la guía de
campo en PDF, sobre el motor quirúrgico ``scripts/utilidades/docx_quirurgico.py``.

Etapa 1: ``--paquete TRAB-01`` emite un paquete completo y ``--guia`` emite la guía.
Etapa 2 no requiere cambios de código: basta con invocar otro código de participante.

Geometría de referencia: A4 vertical, márgenes 3.0 / 2.5 / 2.5 / 2.5 cm, ancho útil
8788 dxa. Toda tabla del paquete suma 8788 dxa exactos. Rejilla visible en los
formularios por excepción declarada (DEC-025 y DEC-026), aplicada con
``aplicar_bordes_rejilla`` del motor.

Uso:
    python scripts/compiladores/paquete_campo_builder.py --paquete TRAB-01
    python scripts/compiladores/paquete_campo_builder.py --guia
    python scripts/compiladores/paquete_campo_builder.py --manifiesto --paquete TRAB-01
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

import docx
from docx.enum.section import WD_SECTION
from docx.enum.table import (
    WD_ALIGN_VERTICAL,
    WD_ROW_HEIGHT_RULE,
    WD_TABLE_ALIGNMENT,
)
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Cm, Pt, Twips

from scripts.comun import seguridad
from scripts.utilidades import docx_quirurgico as quir

# --------------------------------------------------------------------------- #
# Rutas canónicas
# --------------------------------------------------------------------------- #
DESTINO = RAIZ / "salidas" / "instrumentos" / "PAQUETE_CAMPO_14_20261022"
MAESTROS = DESTINO / "_MAESTROS_DOCX"
GUIA_PDF = DESTINO / "00_GUIA_DE_CAMPO_SIVAC_20261022.pdf"
GUIA_MD = RAIZ / "salidas" / "reportes_maquetacion" / "guia_campo_contenido_20261022.md"
MODELO_RECTOR = (
    RAIZ / "salidas" / "evidencias" / "instrumentos_aplicados"
    / "EXPEDIENTE_VALIDACION_JUICIO_EXPERTOS_MODELO_FANY.docx"
)
ESPECIFICACION = RAIZ / "salidas" / "reportes_maquetacion" / "especificacion_paquete_campo_20261022.json"
RENDER = RAIZ / "salidas" / "reportes_maquetacion" / "paginas_control_paquete_20261022"
MANIFIESTO = DESTINO / "_MANIFIESTO_EMISION_ETAPA1.json"
MANIFIESTO_ETAPA2 = DESTINO / "_MANIFIESTO_EMISION_ETAPA2.json"
MANIFIESTO_GLOBAL = DESTINO / "_MANIFIESTO_EMISION.json"

ANCHO_UTIL = 8788
TIPOGRAFIA = "Times New Roman"

TITULO_TESIS = (
    "APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS "
    "MENSUALES DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE "
    "SALUD APURÍMAC II"
)

_ALIN = {
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "center": WD_ALIGN_PARAGRAPH.CENTER,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
    "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
}


# --------------------------------------------------------------------------- #
# Utilidades de documento
# --------------------------------------------------------------------------- #
def documento_nuevo() -> Any:
    """Documento A4 vertical con márgenes UNAJMA y Normal TNR 12 pt a 1.5."""
    doc = docx.Document()
    seccion = doc.sections[0]
    seccion.page_width = Cm(21.0)
    seccion.page_height = Cm(29.7)
    quir.normalizar_margenes_secciones(doc, izquierdo_cm=3.0, derecho_cm=2.5,
                                       superior_cm=2.5, inferior_cm=2.5)
    estilo = doc.styles["Normal"]
    estilo.font.name = TIPOGRAFIA
    estilo.font.size = Pt(12)
    pf = estilo.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.5
    doc.core_properties.title = "Paquete de campo SIVAC"
    doc.core_properties.author = "SIVAC"
    doc.core_properties.comments = ""
    return doc


def _fuente(run, tam: float, negrita: bool = False, cursiva: bool = False) -> None:
    run.font.name = TIPOGRAFIA
    run.font.size = Pt(tam)
    run.font.bold = negrita
    run.font.italic = cursiva


def _runs(p, texto: str, tam: float, negrita: bool = False, cursiva: bool = False) -> None:
    """Escribe el texto alternando negrita con la marca **...**."""
    partes = str(texto).split("**")
    for indice, parte in enumerate(partes):
        if not parte:
            continue
        run = p.add_run(parte)
        _fuente(run, tam, negrita or (indice % 2 == 1), cursiva)


def parrafo(doc, texto: str, *, tam: float = 12, negrita: bool = False, cursiva: bool = False,
            alineacion: str = "justify", antes: float = 0, despues: float = 0,
            interlineado: float = 1.5, sangria: Optional[float] = None,
            izquierda: Optional[float] = None, salto: bool = False,
            keep: bool = False) -> Any:
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(antes)
    pf.space_after = Pt(despues)
    pf.line_spacing = interlineado
    p.alignment = _ALIN[alineacion]
    if salto:
        pf.page_break_before = True
    if keep:
        pf.keep_with_next = True
    if sangria is not None:
        pf.first_line_indent = Cm(sangria)
    if izquierda is not None:
        pf.left_indent = Cm(izquierda)
    _runs(p, texto, tam, negrita, cursiva)
    return p


def titulo(doc, texto: str, *, tam: float = 13, salto: bool = False,
           antes: float = 0, despues: float = 6, alineacion: str = "left") -> Any:
    p = parrafo(doc, texto.upper(), tam=tam, negrita=True, alineacion=alineacion,
                antes=antes, despues=despues, interlineado=1.15, salto=salto, keep=True)
    return p


def nota(doc, texto: str, *, antes: float = 2, despues: float = 6, alineacion: str = "justify") -> Any:
    """Nota de formulario: 9.5 pt, interlineado sencillo, sin sangría (Regla 03)."""
    return parrafo(doc, texto, tam=9.5, alineacion=alineacion, antes=antes,
                   despues=despues, interlineado=1.0)


def _celda_texto(celda, texto: str, *, tam: float = 10, negrita: bool = False,
                 alineacion: str = "left") -> None:
    celda.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p = celda.paragraphs[0]
    p.clear()
    pf = p.paragraph_format
    pf.space_before = Pt(1)
    pf.space_after = Pt(1)
    pf.line_spacing = 1.0
    p.alignment = _ALIN[alineacion]
    lineas = str(texto).split("\n")
    for indice, linea in enumerate(lineas):
        run = p.add_run(linea)
        _fuente(run, tam, negrita)
        if indice < len(lineas) - 1:
            run.add_break()


def _proteger_fila(tr, cabecera: bool = False) -> None:
    """cantSplit y tblHeader delegados en el motor (no se reimplementa OpenXML)."""
    quir._preparar_tr(tr, cant_split=True, tbl_header=cabecera)


_FUENTES = {False: "C:/Windows/Fonts/times.ttf", True: "C:/Windows/Fonts/timesbd.ttf"}


def _ancho_dxa(texto: str, tam: float, negrita: bool = False) -> int:
    """Ancho tipográfico de un texto en dxa, medido con la Times real."""
    from PIL import ImageFont

    fuente = ImageFont.truetype(_FUENTES[negrita], 100)
    return int(fuente.getlength(texto) / 100 * tam * 20)


def _verificar_cabecera(anchos: Sequence[int], fila: Sequence[str], tam: float,
                        margenes_lr: int) -> None:
    """Impide que una palabra de cabecera se quiebre por falta de columna.

    Word no divide palabras sin guion: un token más ancho que la celda útil se
    parte a la mitad. La comprobación se hace en negrita, que es la variante
    con la que se compone la cabecera.
    """
    for ancho, celda in zip(anchos, fila):
        for linea in str(celda).split("\n"):
            for token in linea.split():
                # 5 % de holgura: la composición de Word en el PDF resulta algo
                # más ancha que la medición aislada del glifo (ajuste de línea).
                necesario = int(_ancho_dxa(token, tam, negrita=True) * 1.05) + 2 * margenes_lr
                if necesario > ancho:
                    raise ValueError(
                        f"La cabecera «{token}» necesita {necesario} dxa y la "
                        f"columna ofrece {ancho}; se quebraría dentro de la palabra."
                    )


def tabla(doc, anchos: Sequence[int], filas: Sequence[Sequence[str]], *,
          cabecera: bool = True, tam: float = 10, alto_min_cm: Optional[float] = None,
          alineaciones: Optional[Sequence[str]] = None, margenes_lr: int = 57,
          fusiones: Sequence[int] = (), negrita_datos: bool = False,
          tam_cabecera: Optional[float] = None) -> Any:
    """Tabla nativa con geometría exacta, rejilla visible y filas no fragmentables."""
    anchos = list(anchos)
    if sum(anchos) != ANCHO_UTIL:
        raise ValueError(f"Los anchos suman {sum(anchos)} dxa y deben sumar {ANCHO_UTIL}")
    n_filas, n_cols = len(filas), len(anchos)
    if cabecera and filas:
        _verificar_cabecera(anchos, filas[0], tam_cabecera or tam, margenes_lr)
    t = doc.add_table(rows=n_filas, cols=n_cols)
    t.autofit = False
    quir.configurar_geometria_tabla(
        t, total_width_dxa=ANCHO_UTIL, col_widths_dxa=[Twips(w) for w in anchos]
    )
    for j, ancho in enumerate(anchos):
        t.columns[j].width = Twips(ancho)
    for i, fila in enumerate(filas):
        es_cabecera = cabecera and i == 0
        for j in range(n_cols):
            valor = fila[j] if j < len(fila) else ""
            alineacion = "center" if es_cabecera else (
                alineaciones[j] if alineaciones else "left"
            )
            _celda_texto(t.cell(i, j), valor, tam=(tam_cabecera or tam) if es_cabecera else tam,
                         negrita=es_cabecera or negrita_datos, alineacion=alineacion)
    for i in fusiones:
        celda = t.cell(i, 0).merge(t.cell(i, n_cols - 1))
        celda.width = Twips(ANCHO_UTIL)
        # La fusión conserva un párrafo por celda de origen: se retiran los vacíos
        # para que la fila de grupo mida una sola línea.
        parrafos = celda._tc.findall(qn("w:p"))
        for sobrante in parrafos[1:]:
            if not "".join(t.text or "" for t in sobrante.iter(qn("w:t"))).strip():
                celda._tc.remove(sobrante)
        _celda_texto(celda, filas[i][0], tam=tam, negrita=True, alineacion="left")
    filas_obj = list(t.rows)
    for i, fila in enumerate(filas_obj):
        tr = fila._tr
        _proteger_fila(tr, cabecera=(cabecera and i == 0))
        if alto_min_cm:
            fila.height = Cm(alto_min_cm)
            fila.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        if i < len(filas_obj) - 1:
            for celda in fila.cells:
                for p in celda.paragraphs:
                    p.paragraph_format.keep_with_next = True
    quir.aplicar_bordes_rejilla(t)
    quir.ajustar_margenes_celda(doc, len(doc.tables) - 1, margenes_lr, margenes_lr)
    return t


def cabecera_y_pie(doc, texto_cabecera: str, pie: bool = True) -> None:
    """Encabezado de control y pie con número de página.

    El motor no expone un constructor de pie; el número se resuelve con un campo
    PAGE nativo de Word (``w:fldSimple``), sin geometría ni contenido adicional.
    """
    from docx.oxml import OxmlElement

    seccion = doc.sections[0]
    hp = seccion.header.paragraphs[0]
    hp.text = ""
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp.paragraph_format.space_after = Pt(0)
    run = hp.add_run(texto_cabecera)
    _fuente(run, 9)
    if not pie:
        return
    fp = seccion.footer.paragraphs[0]
    fp.text = ""
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.paragraph_format.space_before = Pt(0)
    run = fp.add_run("Página ")
    _fuente(run, 9)
    campo = OxmlElement("w:fldSimple")
    campo.set(qn("w:instr"), " PAGE ")
    interior = OxmlElement("w:r")
    texto = OxmlElement("w:t")
    texto.text = "1"
    interior.append(texto)
    campo.append(interior)
    fp._p.append(campo)


# --------------------------------------------------------------------------- #
# Bloques comunes de los formularios
# --------------------------------------------------------------------------- #
def bloque_cabecera(doc, codigo: str, fase: str, *, ventana: bool = False,
                    sujeto: str = "Código de participante",
                    etiqueta_fecha: str = "Fecha de aplicación") -> None:
    """Cabecera común: código, centro en blanco, fase, fecha en blanco, investigador."""
    filas = [
        [sujeto, codigo],
        ["Código de centro", "____________________"],
        ["Fase", fase],
    ]
    if ventana:
        filas.append(["Ventana auditada (30 días)", "del ____ / ____ / ______ al ____ / ____ / ______"])
        filas.append(["Fecha de auditoría", "____ / ____ / ______"])
    else:
        filas.append([etiqueta_fecha, "____ / ____ / ______"])
    filas.append(["Investigador", "____________________________________"])
    tabla(doc, [2600, 6188], filas, cabecera=False, tam=10, alto_min_cm=0.75,
          alineaciones=["left", "left"])


def bloque_observaciones(doc, titulo_bloque: str, alto_cm: float = 2.6,
                         antes: float = 8) -> None:
    parrafo(doc, titulo_bloque, tam=10, negrita=True, alineacion="left",
            antes=antes, despues=2, interlineado=1.0, keep=True)
    tabla(doc, [ANCHO_UTIL], [[""]], cabecera=False, tam=10, alto_min_cm=alto_cm,
          margenes_lr=57)


def encabezado_documento(doc, nombre: str, fase: str, *, subtitulo: str = "") -> None:
    titulo(doc, nombre, tam=13, despues=0)
    if subtitulo:
        parrafo(doc, subtitulo, tam=11, cursiva=True, alineacion="left",
                antes=0, despues=6, interlineado=1.0)
    else:
        parrafo(doc, "", tam=6, alineacion="left", despues=4, interlineado=1.0)


# --------------------------------------------------------------------------- #
# Reactivos literales del modelo rector (tablas 14 y 15)
# --------------------------------------------------------------------------- #
def extraer_reactivos(ruta_modelo: Path = MODELO_RECTOR) -> Dict[str, List[Dict[str, str]]]:
    """Extrae los literales de reactivos de las tablas 14 y 15 del modelo rector.

    Nunca se retranscriben a mano: la tabla 14 es la Modalidad A (AP/UP) y la
    tabla 15 la Modalidad B (PU/PE). Se conserva el rótulo de la fila de grupo
    fusionada tal como figura en el modelo.
    """
    documento = docx.Document(str(ruta_modelo))

    def _leer(indice: int, patron: str) -> List[Dict[str, str]]:
        filas: List[Dict[str, str]] = []
        grupo = ""
        for fila in documento.tables[indice].rows[1:]:
            celdas = [c.text.strip() for c in fila.cells]
            if len(set(celdas)) == 1:
                grupo = celdas[0]
                continue
            if re.match(patron, celdas[0]):
                filas.append({"codigo": celdas[0], "texto": celdas[1], "grupo": grupo})
        return filas

    modalidad_a = _leer(14, r"^(AP|UP)-\d{2}$")
    modalidad_b = _leer(15, r"^(PU|PE)-\d{2}$")
    if len(modalidad_a) != 8 or len(modalidad_b) != 8:
        raise RuntimeError(
            f"El modelo rector no devolvió ocho reactivos por modalidad: "
            f"A={len(modalidad_a)}, B={len(modalidad_b)}"
        )
    return {"A": modalidad_a, "B": modalidad_b}


# --------------------------------------------------------------------------- #
# Documentos del paquete
# --------------------------------------------------------------------------- #
def construir_guia_paquete(doc, codigo: str) -> None:
    cabecera_y_pie(doc, f"Paquete {codigo}")
    titulo(doc, "Guía del paquete de campo", tam=14, despues=2)
    parrafo(doc, f"Paquete {codigo}", tam=12, negrita=True, alineacion="left",
            despues=8, interlineado=1.0)
    parrafo(
        doc,
        "Este paquete contiene las hojas de una sola persona. El código impreso "
        "identifica el paquete y no el nombre del trabajador. Guarde todas las hojas "
        "juntas y no mezcle documentos de dos paquetes.",
        tam=12, despues=6,
    )
    parrafo(doc, "Qué contiene", tam=12, negrita=True, alineacion="left",
            antes=4, despues=3, interlineado=1.0, keep=True)
    tabla(
        doc, [2200, 6588],
        [
            ["Carpeta", "Documentos"],
            ["01_PRE", "Consentimiento (dos copias), Ficha 01 de tiempos, Ficha 02 de auditoría, Cuestionario A e instrucciones al participante."],
            ["02_POST", "Ficha 01 de tiempos, Ficha 02 de auditoría, Cuestionario A, Cuestionario B e instrucciones al participante."],
            ["03_DEVOLUCION", "Hoja de recepción de documentos."],
        ],
        tam=10,
    )
    parrafo(doc, "Orden de uso", tam=12, negrita=True, alineacion="left",
            antes=8, despues=3, interlineado=1.0, keep=True)
    pasos = [
        "1. Leer las instrucciones al participante y entregarlas.",
        "2. Explicar y firmar el consentimiento. Guardarlo en sobre aparte.",
        "3. Observar y cronometrar las tareas en la Ficha 01.",
        "4. Auditar los documentos de movimiento en la Ficha 02.",
        "5. Aplicar el Cuestionario A.",
        "6. Aplicar el Cuestionario B solo en la etapa final.",
        "7. Revisar que no falte ninguna hoja y firmar la hoja de recepción.",
    ]
    for paso in pasos:
        parrafo(doc, paso, tam=12, alineacion="left", interlineado=1.15, despues=1)
    parrafo(doc, "Quién llena cada hoja", tam=12, negrita=True, alineacion="left",
            antes=8, despues=3, interlineado=1.0, keep=True)
    tabla(
        doc, [3000, 2900, 2888],
        [
            ["Hoja", "Quién la llena", "Quién firma"],
            ["Consentimiento", "Participante", "Participante e investigador"],
            ["Ficha 01 de tiempos", "Observador", "Observador"],
            ["Ficha 02 de auditoría", "Auditor", "Auditor"],
            ["Cuestionarios A y B", "Participante", "No requiere firma"],
        ],
        tam=10,
    )
    parrafo(doc, "No hacer", tam=12, negrita=True, alineacion="left",
            antes=8, despues=3, interlineado=1.0, keep=True)
    prohibiciones = [
        "• No escribir el nombre del trabajador, su documento de identidad ni el nombre del establecimiento.",
        "• No aplicar el Cuestionario B en la etapa inicial.",
        "• No sumar los puntajes del Cuestionario A con los del Cuestionario B.",
        "• No firmar por otra persona ni firmar una hoja en blanco.",
        "• No anotar una fecha de aplicación que no corresponda.",
        "• No completar una tarea que no se realizó.",
        "• No incluir el certificado de expertos dentro de este paquete.",
    ]
    for linea in prohibiciones:
        parrafo(doc, linea, tam=11, alineacion="left", interlineado=1.15, despues=1)


def _cuerpo_consentimiento(doc, codigo: str, copia: str, salto: bool) -> None:
    titulo(doc, "Consentimiento informado voluntario", tam=13, salto=salto, despues=2,
           alineacion="center")
    parrafo(doc, copia, tam=10, alineacion="center", despues=6, interlineado=1.0)
    parrafo(doc, f"**Título del estudio:** {TITULO_TESIS}.", tam=10, despues=6,
            interlineado=1.0)
    parrafo(
        doc,
        "Este estudio se realiza sobre la gestión de movimientos mensuales de vacunas "
        "en el personal de inmunizaciones de la Dirección de Salud Apurímac II. Se mide "
        "la oportunidad de procesamiento, la consistencia documental y la satisfacción "
        "del usuario. Antes de decidir, lea este documento y formule las preguntas que "
        "necesite.",
        antes=0, despues=2,
    )
    parrafo(
        doc,
        "El estudio lo conduce el Bach. José Luis Quispe León, bajo la asesoría de la "
        "Dra. Norma Lorena Catacora Flores, de la Escuela Profesional de Ingeniería de "
        "Sistemas de la Universidad Nacional José María Arguedas.",
        despues=2,
    )
    parrafo(
        doc,
        "Si acepta participar, se observarán y cronometrarán tres tareas de registro y "
        "tres de emisión de vales. Se auditarán documentos de movimiento de stock, sin "
        "revisar datos de pacientes. Se aplicará un cuestionario de ocho reactivos al "
        "inicio y el mismo al final, más un módulo de ocho reactivos que no se suma al "
        "anterior. Ninguna actividad modifica su trabajo habitual.",
        despues=2,
    )
    parrafo(
        doc,
        "La participación es voluntaria y no es obligatoria. Puede retirarse en "
        "cualquier momento, sin explicar el motivo. El retiro no afecta su situación "
        "laboral ni su evaluación de desempeño. Si se retira, sus registros se excluyen "
        "del análisis.",
        despues=2,
    )
    parrafo(
        doc,
        "Sus respuestas y sus tiempos se identifican solo con un código de participante. "
        "Su nombre, su documento de identidad y el nombre del establecimiento no se "
        "escriben en las fichas. Los resultados se presentan de forma agregada. El "
        "consentimiento firmado se guarda en un sobre aparte y la relación entre código y "
        "nombre se conserva bajo llave.",
        despues=2,
    )
    parrafo(
        doc,
        "La participación no implica riesgo físico ni intervención sobre su salud. La "
        "única molestia previsible es el tiempo dedicado. No recibe pago ni beneficio "
        "económico. El beneficio esperado es aportar evidencia para mejorar el registro y "
        "el control de los movimientos.",
        despues=2,
    )
    parrafo(
        doc,
        "Declaro que se me explicó el propósito y los procedimientos del estudio. Declaro "
        "que mis preguntas fueron respondidas y que participo de manera voluntaria. "
        "Acepto que mis tiempos y mis respuestas se registren bajo un código. Acepto que "
        "se usen solo para los fines descritos.",
        despues=2,
    )
    tabla(
        doc, [2200, 2194, 2400, 1994],
        [
            ["Firma del participante", "________________",
             "Firma del investigador", "________________"],
            ["Documento de identidad", "____________",
             "Documento de identidad", "____________"],
        ],
        cabecera=False, tam=10, alto_min_cm=0.7, alineaciones=["left"] * 4,
    )
    nota(doc, "Fecha: ____ / ____ / ______     "
              "Correo de contacto: ____________________     "
              "Teléfono: ____________________", antes=2)


def construir_consentimiento(doc, codigo: str) -> None:
    cabecera_y_pie(doc, f"Paquete {codigo}")
    _cuerpo_consentimiento(doc, codigo, "Copia para el participante", salto=False)
    _cuerpo_consentimiento(doc, codigo, "Copia para el investigador", salto=True)


def _nota_protocolo_tiempos(doc) -> None:
    nota(
        doc,
        "**Nota de protocolo.** Use un cronómetro digital calibrado y anote la hora de "
        "inicio y la de fin con segundos. Convierta el tiempo a minutos decimales: los "
        "minutos más los segundos divididos entre sesenta. El registro inicia cuando el "
        "operador toma el documento fuente o abre el módulo del sistema, y termina cuando "
        "el movimiento queda guardado y balanceado. La emisión del vale inicia al recibir "
        "o abrir la solicitud y termina cuando el vale queda generado, firmado o impreso "
        "con numeración oficial. Toda interrupción externa se pausa y se anota; el tiempo "
        "pausado no se cuenta. Si la tarea no se completa en la misma sesión, se anula, "
        "se anota el motivo y se repite dentro de la ventana. Una tarea no se anula por "
        "ser lenta: solo por interrupción externa, desviación del protocolo o ayuda "
        "sustantiva del investigador.",
        antes=4, despues=6,
    )


_TAREAS_REGISTRO = [
    ("REG-01", "Ingreso simple de remesa, con un biológico y lote único."),
    ("REG-02", "Salida regular programada, de dos a tres vacunas hacia puesto de salud."),
    ("REG-03", "Redistribución con varios biológicos, de cuatro a seis ítems."),
    ("VALE-01", "Vale simple para puesto de salud I-1 o I-2, de una a dos vacunas."),
    ("VALE-02", "Vale regular para centro de salud I-3 o I-4, de tres a cinco vacunas."),
    ("VALE-03", "Vale de reposición urgente o contingencia de cadena de frío."),
]


def _mapa_interno() -> Dict[str, Any]:
    """Correspondencia entre números visibles y códigos internos no impresos."""
    fuente = extraer_reactivos()
    return {
        "tareas": [
            {"visible": indice, "interno": codigo}
            for indice, (codigo, _) in enumerate(_TAREAS_REGISTRO, 1)
        ],
        "reactivos": {
            "cuestionario_satisfaccion": [
                {"visible": indice, "interno": reactivo["codigo"]}
                for indice, reactivo in enumerate(fuente["A"], 1)
            ],
            "cuestionario_complementario": [
                {"visible": indice, "interno": reactivo["codigo"]}
                for indice, reactivo in enumerate(fuente["B"], 1)
            ],
        },
        "criterios": [
            {"visible": nombre, "interno": codigo}
            for codigo, _, nombre in _CRITERIOS
        ],
        "documentos": [
            {"visible": indice, "interno": f"D-{indice:02d}"}
            for indice in range(1, 7)
        ],
        "entregas": [
            {"visible": indice, "interno": f"E-{indice:02d}"}
            for indice in range(1, 25)
        ],
        "incidencias": [
            {"visible": indice, "interno": f"H-{indice:02d}"}
            for indice in range(1, 13)
        ],
    }

# Reparto revisado: Descripción recibe 3 476 dxa para que ninguna tarea ocupe más
# de dos líneas (la descripción más larga mide 2 851 dxa por línea). Las columnas
# restantes conservan el ancho mínimo que exige su palabra más larga a 9.5 pt, más
# 15 dxa de margen por lado. Suma exacta 8 788 dxa.
_ANCHOS_FICHA01 = [900, 2939, 742, 742, 950, 620, 620, 1275]
_CABECERA_FICHA01 = [
    "Tarea", "Descripción", "Hora inicio", "Hora fin", "Duración (min decimales)",
    "Pausa (sí/no y causa)", "Válida (sí/no)", "Observaciones",
]


def _tabla_tiempos(doc, tareas: Sequence[Tuple[str, str]]) -> None:
    filas = [_CABECERA_FICHA01]
    for codigo, descripcion in tareas:
        filas.append([codigo, descripcion, "", "", "", "", "", ""])
    tabla(doc, _ANCHOS_FICHA01, filas, tam=10, tam_cabecera=9.5, alto_min_cm=0.9,
          alineaciones=["center", "left", "center", "center", "center", "center",
                        "center", "left"], margenes_lr=15)


def construir_ficha01(doc, codigo: str, fase: str) -> None:
    cabecera_y_pie(doc, f"Paquete {codigo} · Fase {fase}")
    encabezado_documento(doc, "Ficha 01. Observación y medición de tiempos", fase,
                         subtitulo="Oportunidad de procesamiento: tiempo de registro y "
                                   "tiempo de emisión de vales")
    bloque_cabecera(doc, codigo, fase)
    _nota_protocolo_tiempos(doc)
    parrafo(doc, "Sección A. Tareas de registro", tam=12, negrita=True,
            alineacion="left", antes=2, despues=3, interlineado=1.0, keep=True)
    _tabla_tiempos(doc, _TAREAS_REGISTRO[:3])
    parrafo(doc, "Sección B. Tareas de emisión de vales", tam=12, negrita=True,
            alineacion="left", antes=10, despues=3, interlineado=1.0, keep=True)
    _tabla_tiempos(doc, _TAREAS_REGISTRO[3:])
    parrafo(doc, "Cierre de la ficha", tam=12, negrita=True, alineacion="left",
            antes=12, despues=3, interlineado=1.0, keep=True, salto=True)
    tabla(
        doc, [3688, 1700, 1700, 1700],
        [
            ["Indicador", "Media (minutos decimales)", "Mediana (minutos decimales)",
             "Tareas válidas (número)"],
            ["Tiempo de registro (REG-01 a REG-03)", "", "", ""],
            ["Tiempo de emisión de vales (VALE-01 a VALE-03)", "", "", ""],
        ],
        tam=10, alto_min_cm=0.9,
        alineaciones=["left", "center", "center", "center"],
    )
    nota(doc, "La mediana de las tres tareas es el valor principal del trabajador en la "
              "fase y la media es el complemento descriptivo. Si solo se completan dos "
              "tareas válidas, se anota el número real y no se completa la tercera.",
         antes=4, despues=8)
    bloque_observaciones(doc, "Observaciones del observador", alto_cm=5.0)
    parrafo(doc, "Incidencias de la sesión", tam=12, negrita=True, alineacion="left",
            antes=10, despues=3, interlineado=1.0, keep=True)
    filas_incidencias: List[List[str]] = [[
        "N.°", "Hora", "Tarea afectada",
        "Causa\n(interrupción externa / desviación del protocolo / ayuda del investigador)",
        "Acción\n(pausa / anulación / repetición)", "Observaciones",
    ]]
    for numero in range(1, 7):
        filas_incidencias.append([str(numero), "", "", "", "", ""])
    tabla(doc, [600, 700, 1500, 2800, 1800, 1388], filas_incidencias, tam=10,
          tam_cabecera=9, alto_min_cm=1.1, margenes_lr=30,
          alineaciones=["center", "center", "left", "left", "left", "left"])
    parrafo(doc, "Firma del observador: ______________________________________", tam=12,
            alineacion="left", antes=10, despues=2, interlineado=1.0)
    parrafo(doc, "Hora de inicio de la sesión: __________     Hora de fin de la sesión: "
                 "__________", tam=12, alineacion="left", despues=0, interlineado=1.0)


_ANCHOS_RSD = [500, 1400, 780] + [340] * 8 + [950, 2438]
_CABECERA_RSD = (["N.°", "Tipo de documento", "Fecha"]
                 + [f"C{i}" for i in range(1, 9)]
                 + ["Conforme (sí/no)", "Motivo"])


def _tabla_rsd(doc, filas_datos: int = 12, alto_cm: float = 0.9) -> None:
    filas = [_CABECERA_RSD]
    for numero in range(1, filas_datos + 1):
        filas.append([str(numero)] + [""] * 12)
    tabla(doc, _ANCHOS_RSD, filas, tam=10, tam_cabecera=9.5, alto_min_cm=alto_cm,
          alineaciones=["center"] * 3 + ["center"] * 8 + ["center", "left"],
          margenes_lr=30)


def _tabla_cpe(doc, filas_datos: int = 12) -> None:
    cabecera = ["N.°", "Cantidad programada", "Cantidad entregada", "Diferencia",
                "Documento que autoriza", "Concordante (sí/no)"]
    filas = [cabecera]
    for numero in range(1, filas_datos + 1):
        filas.append([str(numero)] + [""] * 5)
    tabla(doc, [600, 1650, 1650, 1250, 2388, 1250], filas, tam=10, tam_cabecera=9.5,
          alto_min_cm=0.6, margenes_lr=40,
          alineaciones=["center", "center", "center", "center", "left", "center"])


def construir_ficha02(doc, codigo: str, fase: str) -> None:
    cabecera_y_pie(doc, f"Paquete {codigo} · Fase {fase}")
    encabezado_documento(doc, "Ficha 02. Auditoría documental", fase,
                         subtitulo="Consistencia documental: registros sin discrepancias "
                                   "y concordancia programada con entregada")
    bloque_cabecera(doc, codigo, fase, ventana=True)
    nota(
        doc,
        "**Regla de conformidad.** Un documento es conforme solo si cumple los ocho "
        "criterios a la vez; si falla uno, es no conforme. La unidad del indicador de "
        "registros sin discrepancias es el documento de movimiento: asiento de kardex, "
        "vale, PECOSA, guía de remisión o registro electrónico. La unidad del indicador "
        "de concordancia es la entrega o despacho. No se auditan tarjetas de vacunación "
        "con datos de pacientes: si un documento los contiene, se tapan o no se escanea.",
        antes=4, despues=6,
    )
    parrafo(doc, "Sección A. Registro de documentos auditados", tam=12, negrita=True,
            alineacion="left", antes=2, despues=3, interlineado=1.0, keep=True)

    def _titulo(y):  # noqa: ANN001 - alias de estilo para el párrafo de criterios
        return parrafo(doc, y, tam=10, negrita=True, alineacion="left", despues=2, interlineado=1.0, keep=True)

    _titulo("Criterios abreviados de las columnas C1 a C8")
    parrafo(
        doc,
        "C1 Tipo de movimiento. C2 Denominación del biológico. C3 Número de lote. "
        "C4 Cantidad de dosis o viales. C5 Fecha del movimiento en formato completo. "
        "C6 Establecimiento de origen o destino con código oficial. C7 Nombre, firma o "
        "usuario responsable trazable. C8 Documento formal de respaldo verificado.",
        tam=9.5, alineacion="left", despues=2, interlineado=1.0,
    )
    nota(doc, "El texto íntegro de los ocho criterios figura en la guía de campo, "
              "sección 7.5.", antes=0, despues=6)
    _tabla_rsd(doc, 12)
    nota(doc, "Si el corpus excede estas doce filas, continúe en la hoja de "
              "continuación del kit del investigador.", antes=2, despues=4)
    parrafo(doc, "Sección B. Concordancia entre cantidad programada y entregada",
            tam=12, negrita=True, alineacion="left", antes=8, despues=3,
            interlineado=1.0, keep=True, salto=True)
    _tabla_cpe(doc, 12)
    parrafo(doc, "Cierre de la ficha", tam=12, negrita=True, alineacion="left",
            antes=8, despues=3, interlineado=1.0, keep=True)
    tabla(
        doc, [2600, 1300, 2600, 2288],
        [
            ["Concepto", "Valor", "Concepto", "Valor"],
            ["Documentos auditados (total)", "", "Documentos conformes", ""],
            ["Documentos no conformes", "", "Registros sin discrepancias (porcentaje)", ""],
            ["Entregas evaluadas (total)", "", "Entregas concordantes", ""],
            ["Entregas no concordantes", "", "Concordancia programada y entregada (porcentaje)", ""],
        ],
        tam=10, alto_min_cm=0.9,
        alineaciones=["left", "center", "left", "center"],
    )
    parrafo(
        doc,
        "El indicador de registros sin discrepancias se expresa como el número de "
        "documentos conformes entre el total de documentos auditados, en porcentaje. El "
        "indicador de concordancia se expresa como el número de entregas concordantes "
        "entre el total de entregas evaluadas, en porcentaje. Ambos se anotan como "
        "proporción de documentos y de entregas, no como suma de dosis.",
        antes=4, despues=4,
    )
    bloque_observaciones(doc, "Observaciones del auditor", alto_cm=2.0)
    parrafo(doc, "Firma del auditor: ______________________________________", tam=12,
            alineacion="left", antes=10, despues=2, interlineado=1.0)
    parrafo(doc, "Fecha de cierre de la ficha: ____ / ____ / ______", tam=12,
            alineacion="left", despues=0, interlineado=1.0)


_ANCHOS_CUESTIONARIO = [900, 5088, 560, 560, 560, 560, 560]
_ESCALA = [
    "1\nTotalmente en desacuerdo",
    "2\nEn desacuerdo",
    "3\nNi de acuerdo ni en desacuerdo",
    "4\nDe acuerdo",
    "5\nTotalmente de acuerdo",
]


def _bloque_cuestionario(doc, codigo: str, fase: str, reactivos: Sequence[Dict[str, str]],
                         rotulo: str, aviso: Optional[str] = None) -> None:
    filas: List[List[str]] = [["N.°", "Reactivo", "1", "2", "3", "4", "5"]]
    fusiones: List[int] = []
    grupo_actual = None
    for reactivo in reactivos:
        if reactivo["grupo"] != grupo_actual:
            grupo_actual = reactivo["grupo"]
            fusiones.append(len(filas))
            filas.append([grupo_actual] + [""] * 6)
        filas.append([reactivo["codigo"], reactivo["texto"], "[  ]", "[  ]", "[  ]",
                      "[  ]", "[  ]"])
    tabla(doc, _ANCHOS_CUESTIONARIO, filas, tam=10, fusiones=fusiones,
          alineaciones=["center", "left", "center", "center", "center", "center", "center"])
    if aviso:
        nota(doc, aviso, antes=4, despues=2)


def _documento_cuestionario(doc, codigo: str, fase: str, modalidad: str) -> None:
    reactivos = extraer_reactivos()
    cabecera_y_pie(doc, f"Paquete {codigo} · Fase {fase}")
    if modalidad == "A":
        encabezado_documento(doc, "Cuestionario A. Satisfacción del usuario", fase,
                             subtitulo="Modalidad A. Ocho reactivos con escala de 1 a 5")
    else:
        encabezado_documento(doc, "Cuestionario B. Módulo complementario", fase,
                             subtitulo="Solo postest. Módulo independiente del "
                                       "Cuestionario A, sin baremo")
    bloque_cabecera(doc, codigo, fase)
    if modalidad == "A":
        instruccion = (
            "Lea cada enunciado y marque con una X una sola casilla por reactivo. La "
            "escala va de 1 a 5: 1 es totalmente en desacuerdo y 5 es totalmente de "
            "acuerdo. No hay respuestas correctas ni incorrectas. Responda según su "
            "experiencia en el registro y control de movimientos de vacunas."
        )
    else:
        instruccion = (
            "Lea cada enunciado y marque con una X una sola casilla por reactivo. La "
            "escala va de 1 a 5: 1 es totalmente en desacuerdo y 5 es totalmente de "
            "acuerdo. No hay respuestas correctas ni incorrectas. Responda según su "
            "experiencia con el sistema SIVAC."
        )
    parrafo(doc, instruccion, tam=12, antes=4, despues=6)
    parrafo(doc, "Escala de valoración", tam=10, negrita=True, alineacion="left",
            antes=2, despues=3, interlineado=1.0, keep=True)
    tabla(doc, [1758, 1758, 1758, 1757, 1757], [_ESCALA], cabecera=False, tam=9.5,
          alineaciones=["center"] * 5, margenes_lr=40)
    parrafo(doc, "", tam=4, alineacion="left", antes=0, despues=4, interlineado=1.0)
    if modalidad == "A":
        aviso = ("El Cuestionario A se aplica en la etapa inicial y en la etapa final "
                 "con los mismos ocho reactivos. No se suma con el Cuestionario B.")
    else:
        aviso = ("No se suma al Cuestionario A y no tiene puntaje global ni baremo.")
    _bloque_cuestionario(doc, codigo, fase, reactivos[modalidad], modalidad, aviso)
    bloque_observaciones(doc, "Observaciones del participante (opcional)",
                         alto_cm=1.6 if modalidad == "A" else 1.1)


def construir_cuestionario_a(doc, codigo: str, fase: str) -> None:
    _documento_cuestionario(doc, codigo, fase, "A")


def construir_cuestionario_b(doc, codigo: str, fase: str) -> None:
    _documento_cuestionario(doc, codigo, fase, "B")


def construir_instrucciones(doc, codigo: str, fase: str) -> None:
    cabecera_y_pie(doc, f"Paquete {codigo} · Fase {fase}")
    encabezado_documento(doc, "Instrucciones para el participante", fase,
                         subtitulo="Lectura previa a la aplicación")
    bloque_cabecera(doc, codigo, fase)
    parrafo(doc, "Qué se le pedirá", tam=12, negrita=True, alineacion="left",
            antes=6, despues=2, interlineado=1.0, keep=True)
    if fase == "PRE":
        parrafo(
            doc,
            "Se observarán y cronometrarán tres tareas de registro y tres tareas de "
            "emisión de vales, tal como usted las realiza habitualmente. Después se "
            "revisarán documentos de movimiento de stock, sin datos de pacientes. Al "
            "final responderá un cuestionario de ocho enunciados sobre su trabajo.",
            despues=4,
        )
    else:
        parrafo(
            doc,
            "Se observarán y cronometrarán tres tareas de registro y tres tareas de "
            "emisión de vales realizadas con el sistema SIVAC. Después se revisarán los "
            "registros de movimiento del período. Al final responderá el mismo "
            "cuestionario de ocho enunciados de la etapa inicial.",
            despues=4,
        )
    parrafo(doc, "No hay respuestas correctas ni incorrectas", tam=12, negrita=True,
            alineacion="left", antes=6, despues=2, interlineado=1.0, keep=True)
    parrafo(
        doc,
        "El cuestionario recoge su opinión, no su rendimiento. Responda con sinceridad y "
        "según lo que usted experimenta en su jornada. Nadie evalúa su desempeño con "
        "estas respuestas.",
        despues=4,
    )
    parrafo(doc, "Cómo marcar", tam=12, negrita=True, alineacion="left",
            antes=6, despues=2, interlineado=1.0, keep=True)
    parrafo(
        doc,
        "Cada enunciado tiene cinco casillas. Marque con una X una sola casilla por "
        "enunciado. La escala va de 1 a 5: 1 es totalmente en desacuerdo, 2 es en "
        "desacuerdo, 3 es ni de acuerdo ni en desacuerdo, 4 es de acuerdo y 5 es "
        "totalmente de acuerdo. Si se equivoca, no borre: pida una hoja nueva.",
        despues=4,
    )
    parrafo(doc, "Puede detenerse cuando lo necesite", tam=12, negrita=True,
            alineacion="left", antes=6, despues=2, interlineado=1.0, keep=True)
    parrafo(
        doc,
        "Puede interrumpir la actividad si su trabajo lo requiere. Puede retirarse del "
        "estudio en cualquier momento, sin explicar el motivo y sin consecuencia alguna "
        "para su situación laboral. Si se retira, sus registros se informan como dato "
        "faltante.",
        despues=4,
    )
    parrafo(doc, "Sus datos se identifican con un código", tam=12, negrita=True,
            alineacion="left", antes=6, despues=2, interlineado=1.0, keep=True)
    parrafo(
        doc,
        "Su nombre, su documento de identidad y el nombre de su establecimiento no se "
        "escriben en las hojas. Todo se registra con un código de participante. Los "
        "resultados se presentan de forma agregada.",
        despues=4,
    )
    parrafo(doc, "A quién consultar", tam=12, negrita=True, alineacion="left",
            antes=6, despues=2, interlineado=1.0, keep=True)
    parrafo(
        doc,
        "Si tiene dudas sobre la actividad o sobre el uso de sus datos, consulte con el "
        "investigador responsable en el momento de la aplicación. También puede "
        "dirigirse a la asesora de la tesis a través de la Escuela Profesional de "
        "Ingeniería de Sistemas.",
        despues=6,
    )


_DOCUMENTOS_ENTREGADOS = [
    "Consentimiento informado, copia del participante",
    "Consentimiento informado, copia del investigador",
    "Ficha 01 de observación y tiempos, etapa inicial",
    "Ficha 02 de auditoría documental, etapa inicial",
    "Cuestionario A, etapa inicial",
    "Instrucciones al participante, etapa inicial",
    "Ficha 01 de observación y tiempos, etapa final",
    "Ficha 02 de auditoría documental, etapa final",
    "Cuestionario A, etapa final",
    "Cuestionario B, etapa final",
    "Instrucciones al participante, etapa final",
]


def construir_recepcion(doc, codigo: str) -> None:
    cabecera_y_pie(doc, f"Paquete {codigo}")
    encabezado_documento(doc, "Hoja de recepción de documentos", "PRE y POST",
                         subtitulo="Control de devolución del paquete")
    bloque_cabecera(doc, codigo, "PRE y POST", etiqueta_fecha="Fecha de recepción")
    parrafo(
        doc,
        "Marque cada documento cuando sea devuelto. Si un documento no se aplicó, "
        "anótelo en observaciones y registre el motivo. No se considera devuelto un "
        "documento que no fue firmado por quien corresponda.",
        tam=10, antes=4, despues=6, interlineado=1.0,
    )
    filas: List[List[str]] = [["N.°", "Documento", "Entregado (sí/no)",
                               "Devuelto (sí/no)", "Observaciones"]]
    for numero, documento in enumerate(_DOCUMENTOS_ENTREGADOS, start=1):
        filas.append([str(numero), documento, "", "", ""])
    tabla(doc, [600, 4300, 1100, 1100, 1688], filas, tam=10, alto_min_cm=0.8,
          alineaciones=["center", "left", "center", "center", "left"])
    parrafo(doc, "Firma de quien entrega: ______________________________________",
            tam=12, alineacion="left", antes=14, despues=4, interlineado=1.0)
    parrafo(doc, "Firma de quien recibe: ______________________________________",
            tam=12, alineacion="left", despues=4, interlineado=1.0)
    parrafo(doc, "Fecha de devolución: ____ / ____ / ______", tam=12,
            alineacion="left", despues=0, interlineado=1.0)


# --------------------------------------------------------------------------- #
# Kit del investigador
# --------------------------------------------------------------------------- #
KIT = DESTINO / "90_KIT_INVESTIGADOR"
MAESTROS_KIT = MAESTROS / "90_KIT_INVESTIGADOR"
_CABECERA_KIT = "Kit del investigador · SIVAC"




_CODIGOS = [f"TRAB-{indice:02d}" for indice in range(1, 15)]


def _filas_vacias(columnas: Sequence[str], filas: int,
                  numerada: bool = True,
                  codigos: Optional[int] = None) -> List[List[str]]:
    """Cabecera y filas en blanco; la primera columna es el número de fila.

    ``codigos`` indica el índice de la columna que recibe los catorce códigos
    impresos, para que la hoja sirva de control sin escribir a mano.
    """
    resultado: List[List[str]] = [list(columnas)]
    for numero in range(1, filas + 1):
        fila = [""] * len(columnas)
        if numerada:
            fila[0] = str(numero)
        if codigos is not None and numero <= len(_CODIGOS):
            fila[codigos] = _CODIGOS[numero - 1]
        resultado.append(fila)
    return resultado


def construir_leeme_kit(doc) -> None:
    cabecera_y_pie(doc, _CABECERA_KIT)
    titulo(doc, "Kit del investigador", tam=14, despues=2)
    parrafo(doc, "Índice y reglas de custodia", tam=11, cursiva=True, alineacion="left",
            despues=8, interlineado=1.0)
    parrafo(
        doc,
        "Este kit reúne las hojas de control del investigador. No forma parte de "
        "ningún paquete de participante y no se entrega a los trabajadores. Se conserva "
        "completo hasta el cierre del análisis.",
        tam=12, despues=6,
    )
    filas: List[List[str]] = [["N.°", "Documento", "Uso"]]
    indice = [
        ("Control privado de código y nombre",
         "Único documento que relaciona el código con el nombre del trabajador."),
        ("Hoja de puntuación del Cuestionario A, etapa inicial",
         "Traslada AP, UP, total y nivel de cada trabajador."),
        ("Hoja de puntuación del Cuestionario A, etapa final",
         "Repite el traslado con la misma estructura."),
        ("Registro de campo",
         "Fechas de aplicación, estado y recepción de cada paquete."),
        ("Registro de ausencias",
         "Ausencias, tareas afectadas y reprogramación."),
        ("Control de exposición a SIVAC",
         "Primera utilización, módulos usados y días de uso en el postest."),
        ("Calibración entre observadores",
         "Quince observaciones simultáneas a ciegas para el coeficiente intraclase."),
        ("Calibración entre auditores",
         "Treinta registros auditados a ciegas para el kappa de Cohen."),
        ("Hoja de continuación de la Ficha 02",
         "Doce filas adicionales para el corpus documental."),
        ("Trazabilidad y escaneo",
         "Folio, documento, páginas, archivo y verificación de legibilidad."),
        ("Matriz de captura de instrumentos",
         "Libro de trabajo con una hoja por conjunto de datos y una hoja de parámetros."),
    ]
    for numero, (documento, uso) in enumerate(indice, start=1):
        filas.append([str(numero), documento, uso])
    tabla(doc, [600, 3200, 4988], filas, tam=10, alto_min_cm=0.7,
          alineaciones=["center", "left", "left"], margenes_lr=50)
    parrafo(doc, "Advertencia de custodia", tam=12, negrita=True, alineacion="left",
            antes=10, despues=3, interlineado=1.0, keep=True)
    guarda = [
        "• El control privado de código y nombre se guarda bajo llave y no se escanea.",
        "• Los originales firmados se archivan aparte de las hojas anónimas.",
        "• Las copias digitales permanecen en disco local; no se suben a servicios, "
        "nubes ni mensajería.",
        "• El kit no se fotografía ni se comparte con terceros.",
        "• Si falta una hoja, se anota la incidencia; no se reconstruye con datos de prueba.",
    ]
    for linea in guarda:
        parrafo(doc, linea, tam=11, alineacion="left", interlineado=1.15, despues=2)


def construir_control_privado(doc) -> None:
    cabecera_y_pie(doc, _CABECERA_KIT)
    titulo(doc, "Control privado de código y nombre", tam=14, despues=2)
    parrafo(doc, "CONFIDENCIAL. NO ESCANEAR", tam=12, negrita=True, alineacion="center",
            antes=2, despues=6, interlineado=1.0)
    parrafo(
        doc,
        "Este es el único documento del estudio que relaciona el código del "
        "participante con su nombre. Se llena a mano antes de la primera visita y se "
        "guarda bajo llave, separado de las fichas. No se fotografía, no se escanea y "
        "no se envía por mensajería.",
        tam=11, despues=6,
    )
    filas = _filas_vacias(["N.°", "Código", "Nombre y apellidos",
                           "Documento de identidad", "Medio de contacto",
                           "Observaciones"], 14, codigos=1)
    tabla(doc, [600, 1100, 2338, 1900, 1400, 1450], filas, tam=10, alto_min_cm=1.3,
          alineaciones=["center", "center", "left", "left", "left", "left"])


def construir_puntuacion(doc, fase: str) -> None:
    cabecera_y_pie(doc, _CABECERA_KIT)
    titulo(doc, "Hoja de puntuación del Cuestionario A", tam=14, despues=2)
    parrafo(doc, f"Etapa {'inicial' if fase == 'PRE' else 'final'}", tam=11, cursiva=True,
            alineacion="left", despues=6, interlineado=1.0)
    parrafo(
        doc,
        "Traslade a esta hoja la marca de cada reactivo tal como figura en el "
        "cuestionario. AP es la suma de AP-01 a AP-04, de 4 a 20. UP es la suma de "
        "UP-01 a UP-04, de 4 a 20. El total es la suma de AP y UP, de 8 a 40.",
        tam=11, despues=6,
    )
    cabecera = (["Código"] + [f"AP-0{i}" for i in range(1, 5)]
                + [f"UP-0{i}" for i in range(1, 5)]
                + ["AP\n(4 a 20)", "UP\n(4 a 20)", "Total\n(8 a 40)", "Nivel"])
    filas = _filas_vacias(cabecera, 14, numerada=False, codigos=0)
    anchos = [1060] + [610] * 8 + [700, 700, 700, 748]
    tabla(doc, anchos, filas, tam=10, tam_cabecera=9, alto_min_cm=1.2,
          alineaciones=["center"] * 13, margenes_lr=50)
    nota(doc, "Nivel por terciles teóricos del total: de 8 a 18 bajo, de 19 a 29 medio "
              "y de 30 a 40 alto. El nivel es un tercil teórico, no un baremo normativo.",
         antes=4, despues=2)


def construir_registro_campo(doc) -> None:
    cabecera_y_pie(doc, _CABECERA_KIT)
    titulo(doc, "Registro de campo", tam=14, despues=2)
    parrafo(doc, "Control de aplicación y devolución de los paquetes", tam=11,
            cursiva=True, alineacion="left", despues=6, interlineado=1.0)
    filas = _filas_vacias(["N.°", "Código", "Fecha de aplicación inicial",
                           "Fecha de aplicación final", "Estado del paquete",
                           "Recepción (sí/no)", "Observaciones"], 14, codigos=1)
    tabla(doc, [600, 1100, 1040, 1040, 1700, 1400, 1908], filas, tam=10,
          alto_min_cm=1.3,
          alineaciones=["center", "center", "center", "center", "left", "center", "left"])


def construir_ausencias(doc) -> None:
    cabecera_y_pie(doc, _CABECERA_KIT)
    titulo(doc, "Registro de ausencias", tam=14, despues=2)
    parrafo(doc, "Toda ausencia se anota y se intenta reprogramar dentro de la misma "
                 "ventana de treinta días.", tam=11, cursiva=True, alineacion="left",
            despues=6, interlineado=1.0)
    filas = _filas_vacias(["Código", "Fase", "Fecha", "Motivo", "Tareas afectadas",
                           "Reprogramada (sí/no)", "Nueva fecha", "Estado"], 14,
                          numerada=False, codigos=0)
    tabla(doc, [900, 700, 900, 1960, 1388, 1340, 900, 700], filas, tam=10,
          tam_cabecera=9, alto_min_cm=1.3,
          alineaciones=["center", "center", "center", "left", "left", "center",
                        "center", "center"], margenes_lr=50)
    nota(doc, "Si la ausencia no se reprograma, se marca faltante. No se imputa ni se "
              "sustituye el dato.", antes=4, despues=2)


def construir_exposicion(doc) -> None:
    cabecera_y_pie(doc, _CABECERA_KIT)
    titulo(doc, "Control de exposición a SIVAC", tam=14, despues=2)
    parrafo(doc, "Sin registro de exposición no se declara válido el postest", tam=11,
            cursiva=True, alineacion="left", despues=6, interlineado=1.0)
    filas = _filas_vacias(["Código", "Primera utilización", "Módulos",
                           "Fecha de capacitación", "Días de uso en postest",
                           "Uso previo (sí/no)", "Observaciones"], 14, numerada=False,
                          codigos=0)
    tabla(doc, [900, 1300, 1200, 1500, 1400, 1100, 1388], filas, tam=10,
          tam_cabecera=9, alto_min_cm=1.2,
          alineaciones=["center", "center", "left", "center", "center", "center",
                        "left"], margenes_lr=50)
    nota(doc, "No se inventa un mínimo de días: el criterio lo aprueba la asesora antes "
              "del postest y se anota la fecha de esa decisión.", antes=4, despues=2)


def construir_calibracion_icc(doc) -> None:
    cabecera_y_pie(doc, _CABECERA_KIT)
    titulo(doc, "Calibración entre observadores", tam=14, despues=2)
    parrafo(doc, "Quince observaciones simultáneas, a ciegas, con cronómetros "
                 "independientes", tam=11, cursiva=True, alineacion="left", despues=6,
            interlineado=1.0)
    filas = _filas_vacias(["N.°", "Fecha", "Tarea", "Tiempo observador 1",
                           "Tiempo observador 2", "Diferencia absoluta",
                           "Dentro de tolerancia (sí/no)", "Observaciones"], 15)
    tabla(doc, [600, 900, 900, 1384, 1384, 1150, 1200, 1270], filas, tam=10,
          tam_cabecera=9, alto_min_cm=1.2,
          alineaciones=["center"] * 7 + ["left"], margenes_lr=45)
    nota(doc, "El coeficiente de correlación intraclase se calcula con las quince "
              "observaciones recogidas; no se anota de antemano. Criterio: coeficiente "
              "mayor o igual a 0,75 y diferencia absoluta menor a cinco segundos.",
         antes=4, despues=2)


def construir_calibracion_kappa(doc) -> None:
    cabecera_y_pie(doc, _CABECERA_KIT)
    titulo(doc, "Calibración entre auditores", tam=14, despues=2)
    parrafo(doc, "Treinta registros auditados a ciegas por ambos auditores", tam=11,
            cursiva=True, alineacion="left", despues=4, interlineado=1.0)
    filas = _filas_vacias(["N.°", "Registro", "Auditor 1", "Auditor 2", "Acuerdo",
                           "Causa", "Observaciones"], 30)
    tabla(doc, [600, 1300, 1400, 1400, 1000, 1800, 1288], filas, tam=10,
          tam_cabecera=9, alto_min_cm=0.62,
          alineaciones=["center", "center", "center", "center", "center", "left",
                        "left"], margenes_lr=45)
    nota(doc, "El kappa de Cohen se calcula con los treinta registros recogidos. "
              "Criterio: kappa mayor o igual a 0,80. Si no se alcanza, se revisan los "
              "ocho criterios y se repite la ronda.", antes=4, despues=2)


def construir_continuacion(doc) -> None:
    cabecera_y_pie(doc, _CABECERA_KIT)
    titulo(doc, "Hoja de continuación de la Ficha 02", tam=14, despues=2)
    parrafo(doc, "Sección A. Registro de documentos auditados", tam=11, cursiva=True,
            alineacion="left", despues=4, interlineado=1.0)
    parrafo(doc, "Mismas columnas y mismos criterios que la sección A de la Ficha 02. "
                 "Úsela cuando el corpus exceda las doce filas de la ficha.",
            tam=10, despues=6, interlineado=1.0)
    _tabla_rsd(doc, 12, alto_cm=1.4)


def construir_trazabilidad(doc) -> None:
    cabecera_y_pie(doc, _CABECERA_KIT)
    titulo(doc, "Trazabilidad y escaneo", tam=14, despues=2)
    parrafo(doc, "Solo se escanean documentos sin datos de pacientes. El consentimiento "
                 "se escanea aparte.", tam=11, cursiva=True, alineacion="left",
            despues=6, interlineado=1.0)
    filas = _filas_vacias(["Folio", "Código", "Fase", "Documento", "Páginas",
                           "Fecha de escaneo", "Archivo", "Legible (sí/no)"], 13,
                          numerada=False)
    tabla(doc, [700, 1000, 700, 2200, 800, 1300, 1300, 788], filas, tam=10,
          tam_cabecera=9, alto_min_cm=1.5,
          alineaciones=["center", "center", "center", "left", "center", "center",
                        "left", "center"], margenes_lr=45)


def construir_matriz_captura(ruta: Path) -> Path:
    """Libro de trabajo con las catorce hojas de captura y la hoja de parámetros."""
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter

    especificacion = json.loads(ESPECIFICACION.read_text(encoding="utf-8"))
    hojas = especificacion["matriz_captura"]["hojas"]
    libro = Workbook()
    libro.remove(libro.active)
    fina = Side(style="thin", color="000000")
    borde = Border(left=fina, right=fina, top=fina, bottom=fina)
    for hoja in hojas:
        pagina = libro.create_sheet(hoja["nombre"])
        for j, columna in enumerate(hoja["columnas"], start=1):
            celda = pagina.cell(row=1, column=j, value=columna)
            celda.font = Font(name="Calibri", bold=True, size=11)
            celda.alignment = Alignment(horizontal="center", vertical="center",
                                        wrap_text=True)
            celda.border = borde
            celda.fill = PatternFill("solid", fgColor="D9E1F2")
            pagina.column_dimensions[get_column_letter(j)].width = max(
                12, min(28, len(columna) + 4))
        pagina.freeze_panes = "A2"
        pagina.row_dimensions[1].height = 30
    parametros = libro.create_sheet("PARAMETROS")
    parametros.append(["Parámetro", "Valor registrado", "Opciones"])
    parametros.append([
        "Modo de corpus",
        "",
        "A: 40 a 60 documentos globales por ventana, distribuidos entre centros. "
        "B: 40 a 60 documentos por trabajador y ventana. "
        "C: otro número acordado con la asesora.",
    ])
    parametros.append(["Decisión de la asesora", "", "Se anota el nombre y la fecha de la decisión."])
    parametros.append(["Fecha del pretest", "", "Se anota la fecha real de aplicación."])
    parametros.append(["Fecha del postest", "", "Se anota la fecha real de aplicación."])
    for j, ancho in enumerate([28, 30, 90], start=1):
        parametros.column_dimensions[get_column_letter(j)].width = ancho
    for celda in parametros[1]:
        celda.font = Font(name="Calibri", bold=True, size=11)
        celda.fill = PatternFill("solid", fgColor="D9E1F2")
        celda.border = borde
    for fila in parametros.iter_rows(min_row=2, max_row=parametros.max_row,
                                     max_col=3):
        for celda in fila:
            celda.alignment = Alignment(vertical="top", wrap_text=True)
            celda.border = borde
    ruta.parent.mkdir(parents=True, exist_ok=True)
    seguridad.asegurar_escritura_permitida(ruta)
    libro.save(str(ruta))
    return ruta


def _registro_kit() -> List[Dict[str, Any]]:
    return [
        {"clave": "leeme", "rel": "00_LEEME_KIT.pdf", "constructor": construir_leeme_kit,
         "nombre": "Leeme del kit", "fase": "transversal"},
        {"clave": "control_privado", "rel": "01_CONTROL_PRIVADO_CODIGO_NOMBRE.pdf",
         "constructor": construir_control_privado,
         "nombre": "Control privado de código y nombre", "fase": "transversal"},
        {"clave": "puntuacion_pre", "rel": "02_HOJA_PUNTUACION_A_PRE.pdf",
         "constructor": construir_puntuacion, "nombre": "Hoja de puntuación PRE",
         "fase": "PRE"},
        {"clave": "puntuacion_post", "rel": "03_HOJA_PUNTUACION_A_POST.pdf",
         "constructor": construir_puntuacion, "nombre": "Hoja de puntuación POST",
         "fase": "POST"},
        {"clave": "registro_campo", "rel": "04_REGISTRO_DE_CAMPO.pdf",
         "constructor": construir_registro_campo, "nombre": "Registro de campo",
         "fase": "transversal"},
        {"clave": "ausencias", "rel": "05_REGISTRO_DE_AUSENCIAS.pdf",
         "constructor": construir_ausencias, "nombre": "Registro de ausencias",
         "fase": "transversal"},
        {"clave": "exposicion", "rel": "06_CONTROL_DE_EXPOSICION_SIVAC.pdf",
         "constructor": construir_exposicion, "nombre": "Control de exposición a SIVAC",
         "fase": "transversal"},
        {"clave": "icc", "rel": "07_CALIBRACION_ICC.pdf",
         "constructor": construir_calibracion_icc,
         "nombre": "Calibración entre observadores", "fase": "transversal"},
        {"clave": "kappa", "rel": "08_CALIBRACION_KAPPA.pdf",
         "constructor": construir_calibracion_kappa,
         "nombre": "Calibración entre auditores", "fase": "transversal"},
        {"clave": "continuacion", "rel": "09_HOJA_DE_CONTINUACION_FICHA_02.pdf",
         "constructor": construir_continuacion,
         "nombre": "Hoja de continuación de la Ficha 02", "fase": "transversal"},
        {"clave": "trazabilidad", "rel": "10_TRAZABILIDAD_Y_ESCANEO.pdf",
         "constructor": construir_trazabilidad, "nombre": "Trazabilidad y escaneo",
         "fase": "transversal"},
    ]


def construir_kit(con_pdf: bool = True,
                  solo: Optional[Sequence[str]] = None) -> Dict[str, Any]:
    hechos: List[Dict[str, Any]] = []
    for entrada in _registro_kit():
        if solo is not None and entrada["clave"] not in solo:
            continue
        doc = documento_nuevo()
        if entrada["fase"] in ("PRE", "POST"):
            entrada["constructor"](doc, entrada["fase"])
        else:
            entrada["constructor"](doc)
        _cierre_documento(doc)
        maestro = MAESTROS_KIT / entrada["rel"].replace(".pdf", ".docx")
        seguridad.asegurar_escritura_permitida(maestro)
        maestro.parent.mkdir(parents=True, exist_ok=True)
        doc.save(str(maestro))
        pdf = KIT / entrada["rel"]
        pdf.parent.mkdir(parents=True, exist_ok=True)
        if con_pdf:
            seguridad.asegurar_escritura_permitida(pdf)
            if pdf.exists():
                pdf.unlink()
            quir.exportar_docx_a_pdf(maestro, pdf)
        hechos.append({"clave": entrada["clave"], "docx": str(maestro), "pdf": str(pdf)})
    if solo is None:
        matriz = construir_matriz_captura(KIT / "11_MATRIZ_CAPTURA_INSTRUMENTOS.xlsx")
        hechos.append({"clave": "matriz", "docx": None, "pdf": None, "xlsx": str(matriz)})
    return {"kit": hechos}


# --------------------------------------------------------------------------- #
# Registro de formularios del paquete
# --------------------------------------------------------------------------- #
def _registro() -> List[Dict[str, Any]]:
    return [
        {"clave": "guia_paquete", "rel": "00_GUIA_DEL_PAQUETE.pdf", "fase": "",
         "constructor": construir_guia_paquete, "nombre": "Guía del paquete",
         "con_fase": False},
        {"clave": "consentimiento", "rel": "01_PRE/01_CONSENTIMIENTO.pdf", "fase": "PRE",
         "constructor": construir_consentimiento, "nombre": "Consentimiento informado",
         "con_fase": False},
        {"clave": "ficha01_pre", "rel": "01_PRE/02_FICHA_01_TIEMPOS_PRE.pdf", "fase": "PRE",
         "constructor": construir_ficha01, "nombre": "Ficha 01 de tiempos PRE",
         "con_fase": True},
        {"clave": "ficha02_pre", "rel": "01_PRE/03_FICHA_02_AUDITORIA_PRE.pdf", "fase": "PRE",
         "constructor": construir_ficha02, "nombre": "Ficha 02 de auditoría PRE",
         "con_fase": True},
        {"clave": "cuestionario_a_pre", "rel": "01_PRE/04_CUESTIONARIO_A_PRE.pdf", "fase": "PRE",
         "constructor": construir_cuestionario_a, "nombre": "Cuestionario A PRE",
         "con_fase": True},
        {"clave": "instrucciones_pre", "rel": "01_PRE/05_INSTRUCCIONES_PARTICIPANTE.pdf",
         "fase": "PRE", "constructor": construir_instrucciones,
         "nombre": "Instrucciones al participante PRE", "con_fase": True},
        {"clave": "ficha01_post", "rel": "02_POST/06_FICHA_01_TIEMPOS_POST.pdf", "fase": "POST",
         "constructor": construir_ficha01, "nombre": "Ficha 01 de tiempos POST",
         "con_fase": True},
        {"clave": "ficha02_post", "rel": "02_POST/07_FICHA_02_AUDITORIA_POST.pdf", "fase": "POST",
         "constructor": construir_ficha02, "nombre": "Ficha 02 de auditoría POST",
         "con_fase": True},
        {"clave": "cuestionario_a_post", "rel": "02_POST/08_CUESTIONARIO_A_POST.pdf",
         "fase": "POST", "constructor": construir_cuestionario_a,
         "nombre": "Cuestionario A POST", "con_fase": True},
        {"clave": "cuestionario_b_post", "rel": "02_POST/09_CUESTIONARIO_B_POST.pdf",
         "fase": "POST", "constructor": construir_cuestionario_b,
         "nombre": "Cuestionario B POST", "con_fase": True},
        {"clave": "instrucciones_post", "rel": "02_POST/10_INSTRUCCIONES_PARTICIPANTE.pdf",
         "fase": "POST", "constructor": construir_instrucciones,
         "nombre": "Instrucciones al participante POST", "con_fase": True},
        {"clave": "recepcion", "rel": "03_DEVOLUCION/HOJA_DE_RECEPCION.pdf", "fase": "",
         "constructor": construir_recepcion, "nombre": "Hoja de recepción",
         "con_fase": False},
    ]


# --------------------------------------------------------------------------- #
# Guía de campo: maquetación del contenido markdown
# --------------------------------------------------------------------------- #
def _anchos_proporcionales(filas: Sequence[Sequence[str]], ancho: int = ANCHO_UTIL,
                           minimo: int = 430) -> List[int]:
    """Reparte el ancho útil sin que ninguna palabra se parta entre dos líneas.

    Cada columna recibe primero el ancho que exige su palabra más larga; el espacio
    restante se reparte en proporción al contenido. Así «TRAB-01» o «Observaciones»
    no se quiebran por dentro.
    """
    columnas = max(len(f) for f in filas)
    minimos: List[int] = []
    pesos: List[float] = []
    for j in range(columnas):
        textos = [str(f[j]) for f in filas if j < len(f)]
        palabra = max((max((len(w) for w in t.split()), default=1) for t in textos),
                      default=1)
        es_rotulo = bool(textos) and textos[0].isupper()
        centimetros = palabra * (0.185 if es_rotulo else 0.165) + 0.30
        minimos.append(max(minimo, int(round(centimetros * 567))))
        pesos.append(float(max(6, max((len(t) for t in textos), default=4))))
    base = sum(minimos)
    if base >= ancho:
        anchos = [int(round(minimo_ * ancho / base)) for minimo_ in minimos]
    else:
        resto = ancho - base
        total_peso = sum(pesos)
        anchos = [minimos[j] + int(round(resto * pesos[j] / total_peso))
                  for j in range(columnas)]
    diferencia = ancho - sum(anchos)
    orden = sorted(range(columnas), key=lambda k: pesos[k], reverse=True)
    indice = 0
    while diferencia != 0:
        k = orden[indice % columnas]
        paso = 1 if diferencia > 0 else -1
        if anchos[k] + paso >= minimo:
            anchos[k] += paso
            diferencia -= paso
        indice += 1
        if indice > 20000:
            break
    return anchos


def _tabla_md(doc, bloque: Sequence[str]) -> None:
    filas: List[List[str]] = []
    for linea in bloque:
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in celdas if c):
            continue
        filas.append(celdas)
    if not filas:
        return
    columnas = max(len(f) for f in filas)
    filas = [(f + [""] * columnas)[:columnas] for f in filas]
    anchos = _anchos_proporcionales(filas)
    tabla(doc, anchos, filas, tam=10, margenes_lr=57, tam_cabecera=9.5 if columnas >= 6 else None)


def renderizar_guia(doc, ruta_md: Path) -> None:
    """Maqueta íntegramente el contenido de la guía de campo."""
    lineas = ruta_md.read_text(encoding="utf-8").splitlines()
    i = 0
    primer_salto = True
    pendiente_salto = False
    while i < len(lineas):
        linea = lineas[i]
        despojada = linea.strip()
        if not despojada:
            i += 1
            continue
        if despojada == "---":
            if primer_salto:
                pendiente_salto = True
                primer_salto = False
            i += 1
            continue
        if despojada.startswith("```"):
            i += 1
            bloque = []
            while i < len(lineas) and not lineas[i].strip().startswith("```"):
                bloque.append(lineas[i].rstrip())
                i += 1
            i += 1
            for texto in bloque:
                parrafo(doc, texto or " ", tam=9.5, alineacion="left",
                        interlineado=1.0, izquierda=0.5, despues=0)
            parrafo(doc, "", tam=4, despues=4, interlineado=1.0)
            continue
        if despojada.startswith("|"):
            bloque = []
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                bloque.append(lineas[i])
                i += 1
            _tabla_md(doc, bloque)
            parrafo(doc, "", tam=4, despues=4, interlineado=1.0)
            continue
        if despojada.startswith("### "):
            parrafo(doc, despojada[4:], tam=11.5, negrita=True, alineacion="left",
                    antes=10, despues=3, interlineado=1.15, keep=True)
        elif despojada.startswith("## "):
            parrafo(doc, despojada[3:], tam=12.5, negrita=True, alineacion="left",
                    antes=14, despues=5, interlineado=1.15, keep=True,
                    salto=pendiente_salto)
            pendiente_salto = False
        elif despojada.startswith("# "):
            parrafo(doc, despojada[2:], tam=15, negrita=True, alineacion="center",
                    antes=0, despues=10, interlineado=1.15, keep=True)
        elif despojada.startswith("> "):
            nota(doc, despojada[2:], antes=6, despues=8)
        elif despojada.startswith("- "):
            parrafo(doc, "• " + despojada[2:], tam=12, alineacion="justify",
                    izquierda=0.6, sangria=-0.6, despues=2, interlineado=1.5)
        elif re.match(r"^\d+\.\s", despojada):
            parrafo(doc, despojada, tam=12, alineacion="justify", izquierda=0.6,
                    sangria=-0.6, despues=2, interlineado=1.5)
        else:
            es_rotulo = despojada.startswith("**") and ":**" in despojada.split("**")[1] + "**"
            parrafo(doc, despojada, tam=12, antes=0, despues=4, interlineado=1.5,
                    alineacion="left" if es_rotulo else "justify")
        i += 1


def construir_guia_campo() -> Any:
    doc = documento_nuevo()
    cabecera_y_pie(doc, "Guía de campo · SIVAC")
    renderizar_guia(doc, GUIA_MD)
    parrafo(doc, "", tam=6, alineacion="left", interlineado=1.0)
    return doc


# --------------------------------------------------------------------------- #
# Emisión y verificación
# --------------------------------------------------------------------------- #
def _ruta_maestro(codigo: str, rel: str) -> Path:
    return MAESTROS / codigo / rel.replace("/", "_").replace(".pdf", ".docx")


def construir_paquete(codigo: str, solo: Optional[Sequence[str]] = None,
                      con_pdf: bool = True) -> Dict[str, Any]:
    if not re.fullmatch(r"TRAB-(0[1-9]|1[0-4])", codigo):
        raise ValueError(f"Código de participante no válido: {codigo}")
    destino = DESTINO / f"PAQ-{codigo}"
    registro = _registro()
    if solo:
        registro = [r for r in registro if r["clave"] in solo]
    hechos: List[Dict[str, Any]] = []
    for entrada in registro:
        doc = documento_nuevo()
        if entrada["con_fase"]:
            entrada["constructor"](doc, codigo, entrada["fase"])
        else:
            entrada["constructor"](doc, codigo)
        _cierre_documento(doc)
        maestro = _ruta_maestro(codigo, entrada["rel"])
        seguridad.asegurar_escritura_permitida(maestro)
        maestro.parent.mkdir(parents=True, exist_ok=True)
        doc.save(str(maestro))
        pdf = destino / entrada["rel"]
        pdf.parent.mkdir(parents=True, exist_ok=True)
        if con_pdf:
            seguridad.asegurar_escritura_permitida(pdf)
            if pdf.exists():
                pdf.unlink()
            quir.exportar_docx_a_pdf(maestro, pdf)
        hechos.append({"clave": entrada["clave"], "docx": str(maestro), "pdf": str(pdf)})
    return {"codigo": codigo, "documentos": hechos}


def construir_guia(con_pdf: bool = True) -> Dict[str, Any]:
    doc = construir_guia_campo()
    maestro = MAESTROS / "00_GUIA_DE_CAMPO_SIVAC_20261022.docx"
    seguridad.asegurar_escritura_permitida(maestro)
    maestro.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(maestro))
    if con_pdf:
        seguridad.asegurar_escritura_permitida(GUIA_PDF)
        if GUIA_PDF.exists():
            GUIA_PDF.unlink()
        quir.exportar_docx_a_pdf(maestro, GUIA_PDF)
    return {"docx": str(maestro), "pdf": str(GUIA_PDF)}


def _paginas_pdf(ruta: Path) -> int:
    import pymupdf

    with pymupdf.open(str(ruta)) as documento:
        return documento.page_count


def _texto_pdf(ruta: Path) -> str:
    import pymupdf

    partes = []
    with pymupdf.open(str(ruta)) as documento:
        for pagina in documento:
            partes.append(pagina.get_text("text"))
    return "\n".join(partes)


def _normalizar_texto(texto: str) -> str:
    return " ".join(texto.split())


def _pruebas_por_frase(documentos: Sequence[Dict[str, Any]]) -> Dict[str, bool]:
    """Constata frases y ausencias en los PDF vigentes, sin afirmaciones fijas."""
    por_clave = {Path(d["docx"]).stem: d for d in documentos}

    def texto(clave: str) -> str:
        ruta = por_clave.get(clave, {}).get("pdf")
        return _normalizar_texto(_texto_pdf(Path(ruta))) if ruta else ""

    texto_b = texto("04_MODULO_COMPLEMENTARIO_B_POST")
    texto_a = texto("03_CUESTIONARIO_SATISFACCION_A")
    texto_f01 = texto("01_FICHA_TIEMPOS")
    texto_f02 = texto("02_FICHA_AUDITORIA_DOCUMENTAL")
    texto_00 = texto("00_INSTRUMENTOS_RECOLECCION_SIVAC")
    texto_apoyos = texto(
        "05_APOYOS_INVESTIGADOR_INSTRUCCIONES_CIERRE_CONTINUACIONES")
    todos = _normalizar_texto(" ".join(
        texto(Path(d["docx"]).stem) for d in documentos
        if Path(d["docx"]).stem in por_clave))
    titulo_b = "Cuestionario complementario sobre el uso de SIVAC"
    pie_b = "Instrumento 3, módulo B · SIVAC"
    inicio_vale = (
        "El tiempo de emisión inicia al recibir o abrir la solicitud y termina "
        "cuando el vale queda generado, firmado o impreso con numeración "
        "oficial.")
    codigos = re.compile(
        r"\b(?:C[1-8]|D-\d{2}|E-\d{2}|H-\d{2}|AP-\d{2}|UP-\d{2}|"
        r"PU-\d{2}|PE-\d{2}|REG-\d{2}|VALE-\d{2})\b|"
        r"\((?:AP|UP|PU|PE)\)|\bIndicador:|\bT_reg\b|\bT_vale\b|"
        r"\bRSD\b|\bCPE\b|\bTRAB\b")
    etiquetas = [nombre for _, _, nombre in _CRITERIOS]
    return {
        "B_titulo_modulo_sin_instrumento_4": (
            titulo_b in texto_b and "Instrumento 4" not in texto_b),
        "B_pie_instrumento_3_modulo_b": pie_b in texto_b,
        "conjunto_sin_instrumento_4": "Instrumento 4" not in texto_00,
        "todos_los_entregables_sin_instrumento_4": (
            "Instrumento 4" not in todos),
        "F01_remision_protocolo_y_registro": (
            "Criterios de inicio, fin, pausa y validez: sección Protocolo "
            "del observador de los apoyos." in texto_f01
            and "Incidencias: registro de incidencias y su continuación."
            in texto_f01),
        "F02_remision_continuacion": (
            "continúe desde el documento 5 en Continuación. Registro "
            "documental" in texto_f02),
        "AB_neutralidad_de_fuente": (
            "No hay respuestas correctas ni incorrectas" in texto_a
            and "No hay respuestas correctas ni incorrectas" in texto_b),
        "apoyos_inicio_vale_literal": (
            _normalizar_texto(inicio_vale) in texto_apoyos),
        "apoyos_causas_acciones_incidencia": all(
            frase in texto_apoyos for frase in (
                "interrupción externa", "desviación del protocolo",
                "ayuda sustantiva del investigador", "pausa", "anulación",
                "repetición")),
        "sin_glifos_checkbox_o_corchetes": not any(
            glifo in todos for glifo in ("□", "☐", "[ ]", "[  ]")),
        "sin_codigos_protocolo_visibles": not codigos.search(todos),
        "etiquetas_por_nombre": all(nombre in texto_f02 for nombre in etiquetas)
                                and "C1" not in texto_f02,
        "apoyos_sin_tabla_conversion": (
            "Conversión rápida" not in texto_apoyos
            and "3 + 15/60" not in texto_apoyos),
        "apoyos_ejemplo_conversion_coma": (
            "3,25 minutos" in texto_apoyos and "3.25 minutos" not in texto_apoyos),
        "apoyos_horas_vacias_con_guion_bajo": "__:__" in texto_apoyos,
    }


def _tablas_docx(ruta: Path) -> List[Dict[str, Any]]:
    documento = docx.Document(str(ruta))
    detalle: List[Dict[str, Any]] = []
    for indice, t in enumerate(documento.tables):
        grid = [int(g.get(qn("w:w"))) for g in t._tbl.tblGrid.gridCol_lst]
        tblPr = t._tbl.tblPr
        bordes = tblPr.find(qn("w:tblBorders"))
        inside_v = None
        if bordes is not None:
            nodo = bordes.find(qn("w:insideV"))
            inside_v = nodo.get(qn("w:val")) if nodo is not None else None
        filas = t._tbl.tr_lst
        cant = sum(1 for tr in filas if tr.find(qn("w:trPr")) is not None
                   and tr.find(qn("w:trPr")).find(qn("w:cantSplit")) is not None)
        head = sum(1 for tr in filas if tr.find(qn("w:trPr")) is not None
                   and tr.find(qn("w:trPr")).find(qn("w:tblHeader")) is not None)
        detalle.append({
            "indice": indice,
            "filas": len(filas),
            "columnas": len(grid),
            "ancho_dxa": sum(grid),
            "flotante": tblPr.find(qn("w:tblpPr")) is not None,
            "insideV": inside_v,
            "filas_cantSplit": cant,
            "filas_tblHeader": head,
        })
    return detalle


_PROHIBIDOS = ["DEC-", "—", "MANUAL", "v19", "TODO", "TrueFalse"]
_PATRON_FECHA = re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b")
_PATRON_TRAB = re.compile(r"TRAB-\d{2}")
# Borde inferior del área imprimible: A4 841.92 pt menos el margen inferior de 2.5 cm.
_TOPE_INFERIOR_PT = 841.92 - 70.87


def _desborde_inferior(ruta: Path) -> float:
    """Holgura negativa (en puntos) del contenido respecto del margen inferior."""
    import pymupdf

    exceso = 0.0
    with pymupdf.open(str(ruta)) as documento:
        for pagina in documento:
            for bloque in pagina.get_text("blocks"):
                if bloque[1] < 55 or bloque[1] >= 785:
                    continue
                exceso = max(exceso, float(bloque[3]) - _TOPE_INFERIOR_PT)
    return round(max(0.0, exceso), 2)


def verificar_formulario(pdf: Path, docx_maestro: Path) -> Dict[str, Any]:
    """Controles de texto, páginas, geometría, rejilla y auditoría del motor."""
    texto = _texto_pdf(pdf)
    codigos = sorted(set(_PATRON_TRAB.findall(texto)))
    tablas = _tablas_docx(docx_maestro)
    audit = quir.auditar_docx_openxml(docx_maestro)
    return {
        "pdf": str(pdf),
        "docx": str(docx_maestro),
        "paginas": _paginas_pdf(pdf),
        "desborde_inferior_pt": _desborde_inferior(pdf),
        "bytes_pdf": pdf.stat().st_size,
        "sha256_pdf": seguridad.sha256_archivo(pdf),
        "bytes_docx": docx_maestro.stat().st_size,
        "sha256_docx": seguridad.sha256_archivo(docx_maestro),
        "codigos_trab": codigos,
        "fechas_impresas": _PATRON_FECHA.findall(texto),
        "tokens_prohibidos": [t for t in _PROHIBIDOS if t in texto],
        "tablas": tablas,
        "tablas_fuera_de_ancho": [t["indice"] for t in tablas if t["ancho_dxa"] != ANCHO_UTIL],
        "tablas_sin_rejilla": [t["indice"] for t in tablas
                               if t["insideV"] != "single" and t["filas"] > 0],
        "tablas_flotantes": [t["indice"] for t in tablas if t["flotante"]],
        "filas_sin_cantsplit": [t["indice"] for t in tablas
                                if t["filas_cantSplit"] != t["filas"]],
        "auditoria_motor": audit,
    }


def escribir_manifiesto(codigo: str) -> Dict[str, Any]:
    destino = DESTINO / f"PAQ-{codigo}"
    archivos: List[Dict[str, Any]] = []
    verificaciones: Dict[str, Any] = {"formularios": {}, "general": {}}
    registro = _registro()
    for entrada in registro:
        pdf = destino / entrada["rel"]
        maestro = _ruta_maestro(codigo, entrada["rel"])
        if not pdf.exists() or not maestro.exists():
            continue
        control = verificar_formulario(pdf, maestro)
        archivos.append({
            "ruta": str(pdf),
            "documento": entrada["nombre"],
            "fase": entrada["fase"] or "transversal",
            "paginas": control["paginas"],
            "bytes": control["bytes_pdf"],
            "sha256": control["sha256_pdf"],
        })
        archivos.append({
            "ruta": str(maestro),
            "documento": f"Maestro DOCX · {entrada['nombre']}",
            "fase": entrada["fase"] or "transversal",
            "paginas": None,
            "bytes": control["bytes_docx"],
            "sha256": control["sha256_docx"],
        })
        verificaciones["formularios"][entrada["rel"]] = control
    if GUIA_PDF.exists():
        maestro_guia = MAESTROS / "00_GUIA_DE_CAMPO_SIVAC_20261022.docx"
        archivos.append({
            "ruta": str(GUIA_PDF),
            "documento": "Guía de campo SIVAC",
            "fase": "transversal",
            "paginas": _paginas_pdf(GUIA_PDF),
            "bytes": GUIA_PDF.stat().st_size,
            "sha256": seguridad.sha256_archivo(GUIA_PDF),
        })
        if maestro_guia.exists():
            archivos.append({
                "ruta": str(maestro_guia),
                "documento": "Maestro DOCX · Guía de campo",
                "fase": "transversal",
                "paginas": None,
                "bytes": maestro_guia.stat().st_size,
                "sha256": seguridad.sha256_archivo(maestro_guia),
            })
            verificaciones["general"]["guia"] = {
                "auditoria_motor": quir.auditar_docx_openxml(maestro_guia),
                "tablas": _tablas_docx(maestro_guia),
                "paginas": _paginas_pdf(GUIA_PDF),
            }

    formularios = list(verificaciones["formularios"].values())
    verificaciones["general"].update({
        "documentos_emitidos": len(formularios),
        "todos_con_codigo": all(c["codigos_trab"] == [codigo] for c in formularios),
        "sin_fechas_impresas": all(not c["fechas_impresas"] for c in formularios),
        "sin_tokens_prohibidos": all(not c["tokens_prohibidos"] for c in formularios),
        "todas_las_tablas_en_ancho": all(not c["tablas_fuera_de_ancho"] for c in formularios),
        "rejilla_completa": all(not c["tablas_sin_rejilla"] for c in formularios),
        "sin_tablas_flotantes": all(not c["tablas_flotantes"] for c in formularios),
        "filas_no_fragmentables": all(not c["filas_sin_cantsplit"] for c in formularios),
        "margenes_unajma": all(c["auditoria_motor"]["margenes_unajma_ok"] for c in formularios),
        "paginas_en_rango": all(1 <= c["paginas"] <= 3 for c in formularios),
        "sin_desborde_inferior": all(c["desborde_inferior_pt"] == 0 for c in formularios),
    })

    manifiesto = {
        "meta": {
            "titulo": "Manifiesto de emisión del paquete de campo SIVAC, etapa 1 de 2",
            "fecha": "2026-10-22",
            "agente": "maquetador-docx",
            "squad": "E",
            "fase": "F8_INTEGRACION_EDITORIAL",
            "paquete": f"PAQ-{codigo}",
            "etapa": "1 de 2: muestra completa de un paquete y guía de campo",
            "motor": "scripts/utilidades/docx_quirurgico.py + scripts/compiladores/paquete_campo_builder.py",
        },
        "divergencias_declaradas": [
            {
                "tema": "Ruta de destino",
                "especificacion": "salidas/evidencias/instrumentos_aplicados/paquetes_campo_20261022",
                "destino_real": str(DESTINO.relative_to(RAIZ)).replace("\\", "/"),
                "decision": "El destino único del paquete es el declarado por la Dirección; "
                            "la ruta de la especificación queda subordinada.",
            },
            {
                "tema": "Conteo de documentos",
                "detalle": "La comisión enumera doce rutas bajo el rótulo de once PDF. "
                           "Se emiten las doce rutas enumeradas: once formularios más la "
                           "guía del paquete.",
            },
            {
                "tema": "Literales de reactivos",
                "detalle": "Los ocho reactivos de la modalidad A y los ocho de la "
                           "modalidad B se extraen programáticamente de las tablas 14 y "
                           "15 del modelo rector en cada compilación.",
            },
            {
                "tema": "Código en el consentimiento",
                "detalle": "El consentimiento imprime el código del paquete para "
                           "vincularlo con su sobre. No imprime nombre, documento de "
                           "identidad, fecha ni firma.",
            },
        ],
        "archivos": archivos,
        "verificaciones": verificaciones,
    }
    MANIFIESTO.parent.mkdir(parents=True, exist_ok=True)
    MANIFIESTO.write_text(json.dumps(manifiesto, indent=2, ensure_ascii=False),
                          encoding="utf-8")
    return manifiesto


def renderizar_control(codigo: str) -> Dict[str, Any]:
    destino = DESTINO / f"PAQ-{codigo}"
    RENDER.mkdir(parents=True, exist_ok=True)
    generadas: List[str] = []
    for entrada in _registro():
        pdf = destino / entrada["rel"]
        if not pdf.exists():
            continue
        resultado = quir.renderizar_paginas_pdf(pdf, [1], dpi=110, salida_dir=RENDER)
        generadas.extend(resultado["renderizadas"])
    if GUIA_PDF.exists():
        paginas = min(3, _paginas_pdf(GUIA_PDF))
        resultado = quir.renderizar_paginas_pdf(GUIA_PDF, list(range(1, paginas + 1)),
                                               dpi=110, salida_dir=RENDER)
        generadas.extend(resultado["renderizadas"])
    return {"renderizadas": generadas}


def _control_compacto(control: Dict[str, Any]) -> Dict[str, Any]:
    """Reduce el control de un formulario a los datos que exige el manifiesto."""
    return {
        "paginas": control["paginas"],
        "desborde_inferior_pt": control["desborde_inferior_pt"],
        "bytes_pdf": control["bytes_pdf"],
        "sha256_pdf": control["sha256_pdf"],
        "bytes_docx": control["bytes_docx"],
        "sha256_docx": control["sha256_docx"],
        "codigos_trab": control["codigos_trab"],
        "fechas_impresas": control["fechas_impresas"],
        "tokens_prohibidos": control["tokens_prohibidos"],
        "tablas": len(control["tablas"]),
        "tablas_fuera_de_ancho": control["tablas_fuera_de_ancho"],
        "tablas_sin_rejilla": control["tablas_sin_rejilla"],
        "tablas_flotantes": control["tablas_flotantes"],
        "filas_sin_cantsplit": control["filas_sin_cantsplit"],
        "margenes_unajma_ok": control["auditoria_motor"]["margenes_unajma_ok"],
        "cumple_apa7": control["auditoria_motor"]["cumple_apa7"],
    }


def _verificar_paquete(codigo: str) -> Dict[str, Any]:
    destino = DESTINO / f"PAQ-{codigo}"
    archivos: List[Dict[str, Any]] = []
    formularios: Dict[str, Any] = {}
    for entrada in _registro():
        pdf = destino / entrada["rel"]
        maestro = _ruta_maestro(codigo, entrada["rel"])
        if not pdf.exists() or not maestro.exists():
            continue
        control = _control_compacto(verificar_formulario(pdf, maestro))
        formularios[entrada["rel"]] = control
        archivos.append({
            "ruta": str(pdf), "documento": entrada["nombre"],
            "fase": entrada["fase"] or "transversal", "paginas": control["paginas"],
            "bytes": control["bytes_pdf"], "sha256": control["sha256_pdf"],
        })
        archivos.append({
            "ruta": str(maestro), "documento": f"Maestro DOCX · {entrada['nombre']}",
            "fase": entrada["fase"] or "transversal", "paginas": None,
            "bytes": control["bytes_docx"], "sha256": control["sha256_docx"],
        })
    lista = list(formularios.values())
    verificaciones = {
        "documentos": len(lista),
        "codigo_exclusivo": all(c["codigos_trab"] == [codigo] for c in lista),
        "paginas_en_rango": all(1 <= c["paginas"] <= 3 for c in lista),
        "sin_desborde_inferior": all(c["desborde_inferior_pt"] == 0 for c in lista),
        "sin_fechas_impresas": all(not c["fechas_impresas"] for c in lista),
        "sin_tokens_prohibidos": all(not c["tokens_prohibidos"] for c in lista),
        "todas_las_tablas_en_ancho": all(not c["tablas_fuera_de_ancho"] for c in lista),
        "rejilla_completa": all(not c["tablas_sin_rejilla"] for c in lista),
        "sin_tablas_flotantes": all(not c["tablas_flotantes"] for c in lista),
        "filas_no_fragmentables": all(not c["filas_sin_cantsplit"] for c in lista),
        "margenes_unajma": all(c["margenes_unajma_ok"] for c in lista),
        "cumple_apa7": all(c["cumple_apa7"] for c in lista),
    }
    verificaciones["carpeta_conforme"] = all(
        valor for clave, valor in verificaciones.items()
        if isinstance(valor, bool)
    )
    return {"archivos": archivos, "formularios": formularios,
            "verificaciones": verificaciones,
            "bytes": sum(a["bytes"] for a in archivos)}


def _verificar_kit() -> Dict[str, Any]:
    archivos: List[Dict[str, Any]] = []
    formularios: Dict[str, Any] = {}
    for entrada in _registro_kit():
        pdf = KIT / entrada["rel"]
        maestro = MAESTROS_KIT / entrada["rel"].replace(".pdf", ".docx")
        if not pdf.exists() or not maestro.exists():
            continue
        control = _control_compacto(verificar_formulario(pdf, maestro))
        formularios[entrada["rel"]] = control
        archivos.append({
            "ruta": str(pdf), "documento": entrada["nombre"],
            "fase": entrada["fase"], "paginas": control["paginas"],
            "bytes": control["bytes_pdf"], "sha256": control["sha256_pdf"],
        })
        archivos.append({
            "ruta": str(maestro), "documento": f"Maestro DOCX · {entrada['nombre']}",
            "fase": entrada["fase"], "paginas": None,
            "bytes": control["bytes_docx"], "sha256": control["sha256_docx"],
        })
    matriz = KIT / "11_MATRIZ_CAPTURA_INSTRUMENTOS.xlsx"
    hojas = []
    if matriz.exists():
        from openpyxl import load_workbook

        libro = load_workbook(str(matriz), read_only=True)
        hojas = libro.sheetnames
        libro.close()
        archivos.append({
            "ruta": str(matriz), "documento": "Matriz de captura de instrumentos",
            "fase": "transversal", "paginas": None, "hojas": hojas,
            "bytes": matriz.stat().st_size,
            "sha256": seguridad.sha256_archivo(matriz),
        })
    lista = list(formularios.values())
    codigos = sorted({codigo for c in lista for codigo in c["codigos_trab"]})
    verificaciones = {
        "documentos": len(lista),
        "codigos_impresos": codigos,
        "catorce_codigos": len(codigos) == 14,
        "paginas_en_rango": all(1 <= c["paginas"] <= 3 for c in lista),
        "sin_desborde_inferior": all(c["desborde_inferior_pt"] == 0 for c in lista),
        "sin_fechas_impresas": all(not c["fechas_impresas"] for c in lista),
        "sin_tokens_prohibidos": all(not c["tokens_prohibidos"] for c in lista),
        "todas_las_tablas_en_ancho": all(not c["tablas_fuera_de_ancho"] for c in lista),
        "rejilla_completa": all(not c["tablas_sin_rejilla"] for c in lista),
        "sin_tablas_flotantes": all(not c["tablas_flotantes"] for c in lista),
        "filas_no_fragmentables": all(not c["filas_sin_cantsplit"] for c in lista),
        "margenes_unajma": all(c["margenes_unajma_ok"] for c in lista),
        "cumple_apa7": all(c["cumple_apa7"] for c in lista),
        "matriz_catorce_hojas": len([h for h in hojas if h != "PARAMETROS"]) == 14,
        "matriz_con_parametros": "PARAMETROS" in hojas,
    }
    verificaciones["carpeta_conforme"] = all(
        valor for clave, valor in verificaciones.items() if isinstance(valor, bool)
    )
    return {"archivos": archivos, "formularios": formularios,
            "verificaciones": verificaciones,
            "bytes": sum(a["bytes"] for a in archivos)}


def _resumen_guia() -> Dict[str, Any]:
    maestro = MAESTROS / "00_GUIA_DE_CAMPO_SIVAC_20261022.docx"
    if not (GUIA_PDF.exists() and maestro.exists()):
        return {}
    return {
        "ruta": str(GUIA_PDF),
        "paginas": _paginas_pdf(GUIA_PDF),
        "bytes": GUIA_PDF.stat().st_size,
        "sha256": seguridad.sha256_archivo(GUIA_PDF),
        "maestro_docx": str(maestro),
        "bytes_docx": maestro.stat().st_size,
        "sha256_docx": seguridad.sha256_archivo(maestro),
        "auditoria_motor": quir.auditar_docx_openxml(maestro),
        "desborde_inferior_pt": _desborde_inferior(GUIA_PDF),
    }


def _manifiesto_base(titulo: str, etapa: str) -> Dict[str, Any]:
    return {
        "meta": {
            "titulo": titulo,
            "fecha": "2026-10-22",
            "agente": "maquetador-docx",
            "squad": "E",
            "fase": "F8_INTEGRACION_EDITORIAL",
            "etapa": etapa,
            "destino": str(DESTINO.relative_to(RAIZ)).replace("\\", "/"),
            "motor": "scripts/utilidades/docx_quirurgico.py + "
                     "scripts/compiladores/paquete_campo_builder.py",
        },
        "divergencias_declaradas": [
            {
                "tema": "Ruta de destino",
                "especificacion": "salidas/evidencias/instrumentos_aplicados/paquetes_campo_20261022",
                "destino_real": str(DESTINO.relative_to(RAIZ)).replace("\\", "/"),
                "decision": "El destino único del paquete es el declarado por la Dirección; "
                            "la ruta de la especificación queda subordinada.",
            },
            {
                "tema": "Conteo de documentos",
                "detalle": "La comisión enumera doce rutas bajo el rótulo de once PDF. "
                           "Se emiten las doce rutas enumeradas: once formularios más la "
                           "guía del paquete, en cada uno de los catorce paquetes.",
            },
            {
                "tema": "Literales de reactivos",
                "detalle": "Los ocho reactivos de la modalidad A y los ocho de la "
                           "modalidad B se extraen programáticamente de las tablas 14 y "
                           "15 del modelo rector en cada compilación.",
            },
            {
                "tema": "Identificación del investigador en el consentimiento",
                "detalle": "El consentimiento nombra al tesista y a la asesora, y deja en "
                           "blanco el correo y el teléfono de contacto. No imprime nombre "
                           "de participante, establecimiento ni fecha.",
            },
            {
                "tema": "Anchos de la Ficha 01",
                "detalle": "Los siete anchos indicados en la corrección suman 9 788 dxa y "
                           "no 8 788. Se conservó la jerarquía pedida y se ajustó el "
                           "reparto a 8 788 dxa: Descripción queda en 2 939 dxa, que "
                           "mantiene todas las tareas en dos líneas; Duración, Pausa, "
                           "Válida y Observaciones reciben el ancho que impide que su "
                           "palabra más larga se quiebre dentro de la celda.",
            },
            {
                "tema": "Numeración de incidencias",
                "detalle": "La tabla de incidencias de la Ficha 01 agrega la columna N.° "
                           "para numerar sus seis filas, según lo pedido.",
            },
        ],
    }


def escribir_manifiesto_etapa2() -> Dict[str, Any]:
    """Manifiesto de la etapa 2: trece paquetes nuevos y el kit del investigador."""
    paquetes: Dict[str, Any] = {}
    for indice in range(2, 15):
        codigo = f"TRAB-{indice:02d}"
        paquetes[codigo] = _verificar_paquete(codigo)
    kit = _verificar_kit()
    manifiesto = _manifiesto_base(
        "Manifiesto de emisión del paquete de campo SIVAC, etapa 2 de 2",
        "2 de 2: trece paquetes restantes y kit del investigador",
    )
    manifiesto["paquetes"] = paquetes
    manifiesto["kit"] = kit
    manifiesto["totales"] = {
        "paquetes": len(paquetes),
        "formularios_por_paquete": 12,
        "pdf_de_paquetes": sum(p["verificaciones"]["documentos"] for p in paquetes.values()),
        "pdf_del_kit": kit["verificaciones"]["documentos"],
        "carpetas_conformes": sum(1 for p in paquetes.values()
                                  if p["verificaciones"]["carpeta_conforme"]),
        "kit_conforme": kit["verificaciones"]["carpeta_conforme"],
        "bytes": sum(p["bytes"] for p in paquetes.values()) + kit["bytes"],
    }
    MANIFIESTO_ETAPA2.write_text(json.dumps(manifiesto, indent=2, ensure_ascii=False),
                                 encoding="utf-8")
    return manifiesto


def escribir_manifiesto_global() -> Dict[str, Any]:
    """Manifiesto consolidado: catorce paquetes, kit y guía."""
    paquetes: Dict[str, Any] = {}
    for indice in range(1, 15):
        codigo = f"TRAB-{indice:02d}"
        paquetes[codigo] = _verificar_paquete(codigo)
    kit = _verificar_kit()
    guia = _resumen_guia()
    manifiesto = _manifiesto_base(
        "Manifiesto de emisión del paquete de campo SIVAC",
        "Emisión completa: catorce paquetes, kit del investigador y guía de campo",
    )
    manifiesto["guia"] = guia
    manifiesto["paquetes"] = paquetes
    manifiesto["kit"] = kit
    manifiesto["totales"] = {
        "paquetes": len(paquetes),
        "pdf_de_paquetes": sum(p["verificaciones"]["documentos"] for p in paquetes.values()),
        "pdf_del_kit": kit["verificaciones"]["documentos"],
        "pdf_de_la_guia": 1 if guia else 0,
        "carpetas_conformes": sum(1 for p in paquetes.values()
                                  if p["verificaciones"]["carpeta_conforme"]),
        "kit_conforme": kit["verificaciones"]["carpeta_conforme"],
        "guia_conforme": bool(guia) and guia["auditoria_motor"]["cumple_apa7"],
        "bytes": sum(p["bytes"] for p in paquetes.values()) + kit["bytes"]
                 + (guia["bytes"] if guia else 0),
    }
    MANIFIESTO_GLOBAL.write_text(json.dumps(manifiesto, indent=2, ensure_ascii=False),
                                 encoding="utf-8")
    return manifiesto


def _cierre_documento(doc) -> None:
    """Cierra el cuerpo con un párrafo mínimo tras la última tabla.

    Word exige un párrafo después de una tabla final y, si no existe, inserta uno
    con el tamaño del estilo Normal, que puede desbordar a una página vacía. Se
    declara explícitamente con 1 pt para que no consuma renglón.
    """
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(1)


# --------------------------------------------------------------------------- #
# Modo editorial aislado: rediseño de claridad (Fany, folio 68)
#
# Emite una carpeta nueva sin tocar el paquete de catorce, los maestros previos,
# el expediente de jueces ni el informe. Reutiliza el motor y los helpers de
# arriba; no reimplementa OpenXML. Solo reorganiza la presentación: conserva
# los campos crudos del formulario emitido y los dieciséis reactivos literales.
# --------------------------------------------------------------------------- #
REDISENO = RAIZ / "salidas" / "instrumentos" / "INSTRUMENTOS_REDISENADOS_FANY_20261022_v01"
REDISENO_RENDER = REDISENO / "control_visual"
APOYOS = REDISENO / "APOYOS_INVESTIGADOR"

# Iteración v02: misma composición, cabecera institucional nativa en todas las
# páginas y ajustes de claridad. Destino aislado; v01 no se reemite ni se toca.
REDISENO_V02 = RAIZ / "salidas" / "instrumentos" / "INSTRUMENTOS_REDISENADOS_FANY_20261022_v02"
REDISENO_V02_RENDER = REDISENO_V02 / "control_visual"
APOYOS_V02 = REDISENO_V02 / "APOYOS_INVESTIGADOR"
ASSETS_V02 = REDISENO_V02 / "_assets"
LOGO_UNAJMA = RAIZ / "LOGO-UNAJMA.jpg"
LOGO_EPIS = RAIZ / "LOGO-EPIS.jpg"
LOGO_UNAJMA_RECORTE = ASSETS_V02 / "LOGO-UNAJMA-recorte.png"

_CABECERA_LINEAS = (
    "UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS",
    "Facultad de Ingeniería",
    "Escuela Profesional de Ingeniería de Sistemas",
)
_ANCHOS_CABECERA = [1900, 4988, 1900]
_ALTO_LOGO_CM = 1.2
_DISTANCIA_CABECERA_CM = 0.5

_ANCHOS_ID = [2000, 2000, 1200, 3588]
_ANCHOS_TAREA = [2400, 1500, 1900, 2988]
_ANCHOS_INCIDENCIAS = [700, 900, 1500, 2388, 1800, 1500]
_ANCHOS_CONSOLIDADO = [3400, 1800, 1800, 1788]
_ANCHOS_CRITERIOS = [700, 8088]
_ANCHOS_BLOQUE_CAB = [1900, 2494, 1400, 2994]
_ANCHOS_BLOQUE_CAB_V02 = [2450, 2144, 1400, 2794]
_ANCHOS_REJILLA = [700, 2574, 560, 560, 700, 2574, 560, 560]
_ANCHOS_VEREDICTO = [1400, 2600, 2600, 2188]
_ANCHOS_CPE = [700, 1700, 1700, 1300, 1888, 1500]
_ANCHOS_CONTEO = [5600, 3188]
_ANCHOS_CUESTIONARIO = [900, 5088, 560, 560, 560, 560, 560]
_ANCHOS_ESCALA = [1758, 1758, 1758, 1757, 1757]

# Limpieza profesional v02: una sola jerarquía, dos tablas de tareas, bloques
# de auditoría compactos y columnas Likert de 9 mm. Destino candidato aislado.
CANDIDATO_LIMPIEZA = (RAIZ / "salidas" / "archivo"
                      / "_CANDIDATO_LIMPIEZA_INSTRUMENTOS_20261022")
CANDIDATO_MARCADO = (RAIZ / "salidas" / "archivo"
                     / "_CANDIDATO_MARCADO_CLARO_20261022")
_ANCHOS_F01_LIMPIA = [3108, 1100, 1100, 1000, 620, 620, 620, 620]
_ANCHOS_F02_MATRIZ = [4788, 1000, 1000, 1000, 1000]
_ANCHOS_F02_META = [1600, 3000, 2188, 2000]
_ANCHOS_F02_META_COMPACTO = [1600, 7188]
_ANCHOS_F02_RESULTADO = [1500, 1800, 1800, 3688]
_ANCHOS_CPE_LIMPIA = [600, 1500, 1500, 1000, 2188, 1000, 1000]
_ANCHOS_LIKERT = [800, 5438, 510, 510, 510, 510, 510]
_ANCHOS_CONTROL_APLICACION = [1200, 900, 2200, 1400, 1600, 1488]
_LIMPIEZA_FOOTERS = (
    "Instrumento 1 · SIVAC",
    "Instrumento 2 · SIVAC",
    "Instrumento 3 · SIVAC",
    "Instrumento 3, módulo B · SIVAC",
    "Apoyos del investigador · SIVAC",
)

_ESCALA_ETIQUETAS = [
    "Totalmente en desacuerdo",
    "En desacuerdo",
    "Ni de acuerdo ni en desacuerdo",
    "De acuerdo",
    "Totalmente de acuerdo",
]

_CRITERIOS = [
    ("C1", "Tipo de movimiento clasificado unívocamente: entrada por remesa, "
           "salida a establecimiento de salud o ajuste.", "Tipo de movimiento"),
    ("C2", "Denominación oficial estandarizada del biológico según el esquema "
           "regular nacional del Ministerio de Salud.", "Denominación del biológico"),
    ("C3", "Identificación exacta del número de lote, con rotulado del frasco "
           "coincidente con el documento.", "Número de lote"),
    ("C4", "Cantidad de dosis o viales exacta y coincidente con el stock físico "
           "y el acta de recepción.", "Cantidad de dosis o viales"),
    ("C5", "Fecha del movimiento consignada con formato completo y secuencia "
           "cronológica.", "Fecha del movimiento"),
    ("C6", "Establecimiento de origen o destino plenamente individualizado con "
           "código oficial.", "Establecimiento y código oficial"),
    ("C7", "Nombre completo, firma o usuario responsable del despacho o recepción "
           "plenamente trazable.", "Responsable identificable"),
    ("C8", "Documento formal de respaldo asociado y verificado: vale oficial, "
           "PECOSA, guía de remisión o acta.", "Documento de respaldo"),
]
_GRUPOS_VISIBLES = {
    "AP": "Aceptación del proceso",
    "UP": "Utilidad percibida para la gestión",
    "PU": "Utilidad del sistema",
    "PE": "Facilidad de uso",
}


def _campo(p, instruccion: str, texto: str = "1", tam: float = 9.5) -> None:
    """Inserta un campo nativo de Word con tipografía explícita."""
    from docx.oxml import OxmlElement

    campo = OxmlElement("w:fldSimple")
    campo.set(qn("w:instr"), instruccion)
    run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    fuentes = OxmlElement("w:rFonts")
    for atributo in ("w:ascii", "w:hAnsi", "w:cs"):
        fuentes.set(qn(atributo), TIPOGRAFIA)
    rPr.append(fuentes)
    for etiqueta in ("w:sz", "w:szCs"):
        nodo = OxmlElement(etiqueta)
        nodo.set(qn("w:val"), str(int(round(tam * 2))))
        rPr.append(nodo)
    run.append(rPr)
    nodo_texto = OxmlElement("w:t")
    nodo_texto.text = texto
    nodo_texto.set(qn("xml:space"), "preserve")
    run.append(nodo_texto)
    campo.append(run)
    p._p.append(campo)


def _cabecera_pie(seccion, rotulo: str, pie: str) -> None:
    """Cabecera con el formulario y la página; pie con el instrumento y el código."""
    cabecera = seccion.header.paragraphs[0]
    cabecera.text = ""
    cabecera.alignment = WD_ALIGN_PARAGRAPH.LEFT
    cabecera.paragraph_format.space_after = Pt(0)
    # La plantilla define tabulaciones heredadas (centro 4680, derecha 9360).
    # Deben anularse de forma explícita: clear_all() solo borra las propias y
    # las del estilo siguen activas, por lo que un rótulo corto saltaría a la
    # tabulación central y la página quedaría al centro de la cabecera.
    tabulaciones = cabecera.paragraph_format.tab_stops
    tabulaciones.add_tab_stop(Twips(4680), WD_TAB_ALIGNMENT.CLEAR)
    tabulaciones.add_tab_stop(Twips(9360), WD_TAB_ALIGNMENT.CLEAR)
    tabulaciones.add_tab_stop(Twips(ANCHO_UTIL), WD_TAB_ALIGNMENT.RIGHT)
    run = cabecera.add_run(rotulo)
    _fuente(run, 9.5)
    run = cabecera.add_run("\tPágina ")
    _fuente(run, 9.5)
    _campo(cabecera, " PAGE ")
    run = cabecera.add_run(" de ")
    _fuente(run, 9.5)
    _campo(cabecera, " NUMPAGES ")

    pata = seccion.footer.paragraphs[0]
    pata.text = ""
    pata.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pata.paragraph_format.space_before = Pt(0)
    run = pata.add_run(pie)
    _fuente(run, 9.5)


def _borde_inferior_parrafo(p, color: str = "BFBFBF", sz: int = 4) -> None:
    """Regla fina nativa bajo la línea de control de la cabecera."""
    from docx.oxml import OxmlElement

    pPr = p._p.get_or_add_pPr()
    anterior = pPr.find(qn("w:pBdr"))
    if anterior is not None:
        pPr.remove(anterior)
    bordes = OxmlElement("w:pBdr")
    inferior = OxmlElement("w:bottom")
    inferior.set(qn("w:val"), "single")
    inferior.set(qn("w:sz"), str(sz))
    inferior.set(qn("w:space"), "1")
    inferior.set(qn("w:color"), color)
    bordes.append(inferior)
    for etiqueta in ("w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku",
                     "w:wordWrap", "w:overflowPunct", "w:topLinePunct",
                     "w:autoSpaceDE", "w:autoSpaceDN", "w:bidi",
                     "w:adjustRightInd", "w:snapToGrid", "w:spacing",
                     "w:ind", "w:contextualSpacing", "w:mirrorIndents",
                     "w:suppressOverlap", "w:jc", "w:textDirection",
                     "w:textAlignment", "w:textboxTightWrap",
                     "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr",
                     "w:sectPr", "w:pPrChange"):
        hallado = pPr.find(qn(etiqueta))
        if hallado is not None:
            hallado.addprevious(bordes)
            return
    pPr.append(bordes)


def _insertar_en_tblpr(tblPr, nuevo, etiquetas: Sequence[str]) -> None:
    for etiqueta in etiquetas:
        hallado = tblPr.find(qn(etiqueta))
        if hallado is not None:
            hallado.addprevious(nuevo)
            return
    tblPr.append(nuevo)


def _tabla_cabecera_institucional(header, anchos: Sequence[int]) -> Any:
    """Tabla de tres columnas, sin bordes y con columnas laterales iguales."""
    from docx.oxml import OxmlElement

    t = header.add_table(rows=1, cols=3, width=Cm(15.5))
    t.autofit = False
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    quir.configurar_geometria_tabla(
        t, total_width_dxa=ANCHO_UTIL,
        col_widths_dxa=[Twips(w) for w in anchos])
    for indice, ancho in enumerate(anchos):
        t.columns[indice].width = Twips(ancho)
        t.cell(0, indice).width = Twips(ancho)

    tblPr = t._tbl.tblPr
    for estilo in tblPr.findall(qn("w:tblStyle")):
        tblPr.remove(estilo)
    medida = tblPr.find(qn("w:tblW"))
    if medida is not None:
        medida.set(qn("w:type"), "dxa")
        medida.set(qn("w:w"), str(ANCHO_UTIL))
    bordes_previos = tblPr.find(qn("w:tblBorders"))
    if bordes_previos is not None:
        tblPr.remove(bordes_previos)
    bordes = OxmlElement("w:tblBorders")
    for borde in ("top", "left", "bottom", "right", "insideH", "insideV"):
        elemento = OxmlElement(f"w:{borde}")
        elemento.set(qn("w:val"), "nil")
        elemento.set(qn("w:sz"), "0")
        elemento.set(qn("w:space"), "0")
        elemento.set(qn("w:color"), "auto")
        bordes.append(elemento)
    _insertar_en_tblpr(tblPr, bordes, ("w:shd", "w:tblLayout", "w:tblCellMar",
                                       "w:tblLook"))
    disposicion = OxmlElement("w:tblLayout")
    disposicion.set(qn("w:type"), "fixed")
    _insertar_en_tblpr(tblPr, disposicion, ("w:tblCellMar", "w:tblLook"))
    margenes = OxmlElement("w:tblCellMar")
    for lado in ("top", "left", "bottom", "right"):
        elemento = OxmlElement(f"w:{lado}")
        elemento.set(qn("w:w"), "0")
        elemento.set(qn("w:type"), "dxa")
        margenes.append(elemento)
    _insertar_en_tblpr(tblPr, margenes, ("w:tblLook",))

    for celda in t.rows[0].cells:
        celda.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for p in celda.paragraphs:
            pf = p.paragraph_format
            pf.space_before = Pt(0)
            pf.space_after = Pt(0)
            pf.line_spacing = 1.0
    return t


def _logo_en_celda(celda, ruta: Path, descripcion: str,
                   alineacion: str = "center") -> None:
    p = celda.paragraphs[0]
    p.alignment = _ALIN[alineacion]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run()
    run.add_picture(str(ruta), height=Cm(_ALTO_LOGO_CM))
    for docPr in run._r.iter(qn("wp:docPr")):
        docPr.set("descr", descripcion)
        docPr.set("title", descripcion)


def _cabecera_institucional(seccion, rotulo: str, pie: str) -> None:
    """Cabecera nativa repetida: logos inline, bloque institucional y página."""
    if seccion.header.is_linked_to_previous:
        seccion.header.is_linked_to_previous = False
    if seccion.footer.is_linked_to_previous:
        seccion.footer.is_linked_to_previous = False
    seccion.header_distance = Cm(_DISTANCIA_CABECERA_CM)
    seccion.footer_distance = Cm(1.25)

    cabecera = seccion.header
    for sobrante in list(cabecera.paragraphs)[1:]:
        sobrante._element.getparent().remove(sobrante._element)
    linea = cabecera.paragraphs[0]

    t = _tabla_cabecera_institucional(cabecera, _ANCHOS_CABECERA)
    linea._p.addprevious(t._tbl)
    _logo_en_celda(t.cell(0, 0), LOGO_UNAJMA_RECORTE, "Logotipo UNAJMA",
                   alineacion="left")
    _logo_en_celda(t.cell(0, 2), LOGO_EPIS, "Logotipo EPIS",
                   alineacion="right")

    celda_texto = t.cell(0, 1)
    for indice, texto in enumerate(_CABECERA_LINEAS):
        p = celda_texto.paragraphs[0] if indice == 0 else celda_texto.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(texto)
        _fuente(run, 8.5, negrita=(indice == 0))

    linea.text = ""
    linea.alignment = WD_ALIGN_PARAGRAPH.LEFT
    linea.paragraph_format.space_before = Pt(2)
    linea.paragraph_format.space_after = Pt(0)
    linea.paragraph_format.line_spacing = 1.0
    tabulaciones = linea.paragraph_format.tab_stops
    tabulaciones.add_tab_stop(Twips(4680), WD_TAB_ALIGNMENT.CLEAR)
    tabulaciones.add_tab_stop(Twips(9360), WD_TAB_ALIGNMENT.CLEAR)
    tabulaciones.add_tab_stop(Twips(ANCHO_UTIL), WD_TAB_ALIGNMENT.RIGHT)
    run = linea.add_run(rotulo)
    _fuente(run, 9, negrita=True)
    run = linea.add_run("\tPágina ")
    _fuente(run, 9)
    _campo(linea, " PAGE ", tam=9)
    run = linea.add_run(" de ")
    _fuente(run, 9)
    _campo(linea, " NUMPAGES ", tam=9)
    _borde_inferior_parrafo(linea)

    pata = seccion.footer.paragraphs[0]
    pata.text = ""
    pata.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pata.paragraph_format.space_before = Pt(0)
    pata.paragraph_format.space_after = Pt(0)
    run = pata.add_run(pie)
    _fuente(run, 8.5)


def documento_rediseno(titulo_doc: str) -> Any:
    doc = documento_nuevo()
    doc.core_properties.title = titulo_doc
    doc.core_properties.author = "SIVAC"
    return doc


def _salto(doc) -> None:
    """Salto de página sin renglón visible (1 pt) antes de una tabla."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.page_break_before = True
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(1)


def _titulo_formulario(doc, numero: str, titulo_texto: str, subtitulo: str,
                       fijo: Optional[str] = None) -> None:
    # El formulario ya se identifica en la cabecera de página; no se repite aquí.
    parrafo(doc, titulo_texto, tam=13, negrita=True, alineacion="left",
            despues=1, interlineado=1.05)
    parrafo(doc, subtitulo, tam=10.5, cursiva=True, alineacion="left",
            despues=2, interlineado=1.0)
    if fijo:
        parrafo(doc, fijo, tam=10, negrita=True, alineacion="left",
                despues=3, interlineado=1.0)


def _rol_aplicacion(doc, rol: str, momento: str) -> None:
    """Línea breve de responsabilidad y momento, sin fechas ni aplicación real."""
    parrafo(doc, f"Lo completa: {rol}. {momento}", tam=9.5, cursiva=True,
            alineacion="left", despues=2, interlineado=1.0)


def _instrucciones(doc, lineas: Sequence[str], despues: float = 1) -> None:
    parrafo(doc, "Instrucciones", tam=10, negrita=True, alineacion="left",
            antes=3, despues=2, interlineado=1.0, keep=True)
    for indice, linea in enumerate(lineas, 1):
        parrafo(doc, f"{indice}. {linea}", tam=10, alineacion="left",
                despues=despues, interlineado=1.0)


def _negrita_fila(t, indice: int, tam: Optional[float] = None) -> None:
    for celda in t.rows[indice].cells:
        for p in celda.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.bold = True
                if tam is not None:
                    run.font.size = Pt(tam)


def _negrita_columna(t, columna: int, filas: Sequence[int]) -> None:
    for indice in filas:
        for p in t.rows[indice].cells[columna].paragraphs:
            for run in p.runs:
                run.font.bold = True


def _mantener_con_siguiente(t) -> None:
    for celda in t.rows[-1].cells:
        for p in celda.paragraphs:
            p.paragraph_format.keep_with_next = True


def _fusionar(t, fila: int, desde: int, hasta: int, texto: str,
              tam: float = 10, negrita: bool = False) -> None:
    celda = t.cell(fila, desde).merge(t.cell(fila, hasta))
    sobrantes = celda._tc.findall(qn("w:p"))
    for parrafo_sobrante in sobrantes[1:]:
        celda._tc.remove(parrafo_sobrante)
    _celda_texto(celda, texto, tam=tam, negrita=negrita, alineacion="left")


def _identificacion(doc, filas: Sequence[Sequence[str]],
                    fusiones: Sequence[Tuple[int, int, int, str]] = (),
                    alto_cm: float = 0.7) -> Any:
    t = tabla(doc, _ANCHOS_ID, filas, cabecera=False, tam=10, alto_min_cm=alto_cm,
              alineaciones=["left"] * 4, margenes_lr=57)
    for fila, desde, hasta, texto in fusiones:
        _fusionar(t, fila, desde, hasta, texto)
    _negrita_columna(t, 0, list(range(len(filas))))
    return t


def _identificacion_apoyo(doc) -> None:
    """Identificación breve de una hoja suelta de cierre o continuación."""
    _identificacion(doc, [
        ["Código", "TRAB-______", "Fase", "________________ (INICIAL o FINAL)"],
        ["Código de centro", "__________", "Fecha", "____/____/______"],
    ])


def _banda(doc, texto: str) -> Any:
    t = tabla(doc, [ANCHO_UTIL], [[texto]], cabecera=False, tam=10,
              alto_min_cm=0.55, alineaciones=["left"], margenes_lr=57)
    _negrita_fila(t, 0, tam=10)
    t.rows[0].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
    return t


def _bloque_tarea(doc, codigo: str, descripcion: str) -> None:
    """Bloque vertical de una tarea: título, tiempos, pausa, validez y nota."""
    filas = [
        [f"{codigo}. {descripcion}", "", "", ""],
        ["Hora de inicio", "__:__:__", "Hora de fin", "__:__:__"],
        ["Duración (minutos decimales)", "________", "Pausa (Sí / No)",
         "Causa: ____________"],
        ["Tarea válida (Sí / No)", "________", "Observaciones",
         "____________________"],
    ]
    t = tabla(doc, _ANCHOS_TAREA, filas, cabecera=False, tam=10, alto_min_cm=0.8,
              fusiones=[0], alineaciones=["left"] * 4, margenes_lr=40)
    _negrita_columna(t, 0, [2, 3])
    _mantener_con_siguiente(t)


def _tabla_incidencias(doc, desde: int, filas_datos: int,
                       alto_cm: float = 0.7) -> Any:
    cabecera = ["N.°", "Hora", "Tarea afectada", "Causa", "Acción",
                "Observaciones"]
    filas = [cabecera]
    for numero in range(desde, desde + filas_datos):
        filas.append([f"H-{numero:02d}", "", "", "", "", ""])
    return tabla(doc, _ANCHOS_INCIDENCIAS, filas, tam=10, tam_cabecera=9.5,
                 alto_min_cm=alto_cm, margenes_lr=40,
                 alineaciones=["center", "center", "left", "left", "left", "left"])


def _consolidado_tiempos(doc) -> None:
    parrafo(doc, "Consolidado por indicador y fase", tam=10, negrita=True,
            alineacion="left", antes=8, despues=2, interlineado=1.0, keep=True)
    tabla(
        doc, _ANCHOS_CONSOLIDADO,
        [
            ["Indicador", "Media (minutos decimales)", "Mediana (minutos decimales)",
             "Tareas válidas (número)"],
            ["Tiempo de registro (REG-01 a REG-03)", "", "", ""],
            ["Tiempo de emisión de vales (VALE-01 a VALE-03)", "", "", ""],
        ],
        tam=10, tam_cabecera=9.5, alto_min_cm=0.8, margenes_lr=40,
        alineaciones=["left", "center", "center", "center"],
    )
    nota(doc, "La mediana de las tres tareas es el valor principal del trabajador "
              "en la fase; la media es el complemento descriptivo. Si solo hay dos "
              "tareas válidas, anote 2 y no complete la tercera.", antes=2,
         despues=4)


def _cuerpo_ficha01(doc, con_salto: bool = True,
                    version: str = "v01") -> None:
    _titulo_formulario(
        doc, "01", "Instrumento 1. Ficha de observación de tiempos",
        "Oportunidad de procesamiento: tiempo de registro y tiempo de emisión de vales")
    if version == "v02":
        _rol_aplicacion(doc, "observador",
                        "Fase INICIAL: antes de la intervención; fase FINAL: después.")
    _identificacion(doc, [
        ["Código", "TRAB-______", "Fase", "________________ (INICIAL o FINAL)"],
        ["Código de centro", "__________", "Fecha", "____/____/______"],
        ["Observador", "", "", ""],
    ], fusiones=[(2, 1, 3, "____________________________________________________")])
    _instrucciones(doc, [
        "Cronometre con un cronómetro digital y anote la hora de inicio y la de fin "
        "con segundos.",
        "El tiempo de registro empieza cuando el operador toma el documento fuente o "
        "abre el módulo, y termina cuando el movimiento queda guardado y balanceado.",
        "El tiempo de emisión empieza cuando se recibe o abre la solicitud, y termina "
        "cuando el vale queda generado, firmado o impreso con numeración oficial.",
        "Si hay una interrupción externa, pause el cronómetro y anote la causa. El "
        "tiempo pausado no se cuenta.",
        "Si la tarea no se completa, anule, anote el motivo y repítala dentro de la "
        "ventana. No anule una tarea por ser lenta.",
        "Convierta a minutos decimales: los minutos más los segundos divididos entre "
        "sesenta.",
    ])
    _banda(doc, "A. Tareas de registro (tiempo de registro)")
    for codigo, descripcion in _TAREAS_REGISTRO[:3]:
        _bloque_tarea(doc, codigo, descripcion)

    if con_salto:
        _salto(doc)
    _banda(doc, "B. Tareas de emisión de vales (tiempo de emisión)")
    for codigo, descripcion in _TAREAS_REGISTRO[3:]:
        _bloque_tarea(doc, codigo, descripcion)
    _consolidado_tiempos(doc)

    parrafo(doc, "Incidencias de la sesión", tam=10, negrita=True,
            alineacion="left", antes=6, despues=2, interlineado=1.0, keep=True)
    _tabla_incidencias(doc, 1, 4)
    nota(doc, "Causa: interrupción externa, desviación del protocolo o ayuda del "
              "investigador. Acción: pausa, anulación o repetición. Si hay más de "
              "cuatro incidencias, continúe en la hoja H-05 de los apoyos del "
              "investigador.", antes=2, despues=4)

    bloque_observaciones(doc, "Observaciones del observador", alto_cm=1.7)
    parrafo(doc, "Firma del observador: ______________________________________",
            tam=11, alineacion="left", antes=6, despues=1, interlineado=1.0)
    parrafo(doc, "Hora de inicio de la sesión: __________     Hora de fin de la "
                 "sesión: __________", tam=11, alineacion="left", despues=0,
            interlineado=1.0)


def _bloque_documento(doc, numero: int, version: str = "v01") -> None:
    """Bloque vertical de un documento auditado, con los ocho criterios."""
    v02 = version == "v02"
    cabecera = tabla(
        doc, _ANCHOS_BLOQUE_CAB_V02 if v02 else _ANCHOS_BLOQUE_CAB,
        [
            [(f"Bloque de auditoría D-{numero:02d}" if v02
              else f"Documento D-{numero:02d}"), "", "", ""],
            [("N.° del documento revisado" if v02 else "N.° de documento"),
             "________", "Fecha", "____/____/______"],
            ["Tipo de documento", "", "", ""],
        ],
        cabecera=False, tam=10, alto_min_cm=0.65, fusiones=[0], margenes_lr=40,
        alineaciones=["left"] * 4,
    )
    _negrita_fila(cabecera, 0, tam=10)
    cabecera.rows[0].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
    _negrita_columna(cabecera, 0, [1, 2])
    _fusionar(cabecera, 2, 1, 3,
              "kardex / vale / PECOSA / guía de remisión / registro electrónico")
    _mantener_con_siguiente(cabecera)

    filas = [["Código", "Criterio", "Sí", "No", "Código", "Criterio", "Sí", "No"]]
    for indice in range(4):
        izquierda = _CRITERIOS[indice]
        derecha = _CRITERIOS[indice + 4]
        filas.append([izquierda[0], izquierda[2], "", "",
                      derecha[0], derecha[2], "", ""])
    rejilla = tabla(doc, _ANCHOS_REJILLA, filas, tam=9.5, tam_cabecera=9.5,
                    alto_min_cm=0.6, margenes_lr=40,
                    alineaciones=["center", "left", "center", "center"] * 2)
    _mantener_con_siguiente(rejilla)

    tabla(
        doc, _ANCHOS_VEREDICTO,
        [["Veredicto", "CONFORME / NO CONFORME",
          "Causa de la no conformidad", "________________"]],
        cabecera=False, tam=9.5, alto_min_cm=0.85, margenes_lr=40,
        alineaciones=["left"] * 4,
    )


def _tabla_cpe_rediseno(doc, desde: int, filas_datos: int,
                        alto_cm: float = 0.6) -> Any:
    cabecera = ["N.°", "Cantidad programada", "Cantidad entregada", "Diferencia",
                "Documento que autoriza", "Concordante (Sí / No)"]
    filas = [cabecera]
    for numero in range(desde, desde + filas_datos):
        filas.append([f"E-{numero:02d}", "", "", "", "", ""])
    return tabla(doc, _ANCHOS_CPE, filas, tam=10, tam_cabecera=9.5,
                 alto_min_cm=alto_cm, margenes_lr=40,
                 alineaciones=["center", "center", "center", "center", "left",
                               "center"])


def _conteos_cierre(doc) -> None:
    parrafo(doc, "Conteos de cierre de la ficha", tam=10, negrita=True,
            alineacion="left", antes=6, despues=2, interlineado=1.0, keep=True)
    tabla(
        doc, _ANCHOS_CONTEO,
        [
            ["Concepto", "Valor"],
            ["Documentos auditados (total)", ""],
            ["Documentos conformes", ""],
            ["Documentos no conformes", ""],
            ["Entregas evaluadas (total)", ""],
            ["Entregas concordantes", ""],
            ["Entregas no concordantes", ""],
        ],
        tam=10, tam_cabecera=9.5, alto_min_cm=0.55, margenes_lr=40,
        alineaciones=["left", "center"],
    )
    nota(doc, "Los porcentajes se calculan en la hoja de cierre del investigador. "
              "No se anotan en esta ficha.", antes=2, despues=3)


def _cuerpo_ficha02(doc, con_salto: bool = True,
                    version: str = "v01") -> None:
    _titulo_formulario(
        doc, "02", "Instrumento 2. Ficha de auditoría documental",
        "Consistencia documental: registros sin discrepancias y concordancia "
        "programada con entregada")
    if version == "v02":
        _rol_aplicacion(doc, "auditor",
                        "Fase INICIAL: antes de la intervención; fase FINAL: después.")
    _identificacion(doc, [
        ["Código", "TRAB-______", "Fase", "________________ (INICIAL o FINAL)"],
        ["Código de centro", "__________", "Fecha", "____/____/______"],
        ["Ventana auditada", "", "", ""],
        ["Auditor", "", "", ""],
    ], fusiones=[
        (2, 1, 3, "del ____/____/______ al ____/____/______"),
        (3, 1, 3, "____________________________________________________"),
    ])
    _instrucciones(doc, [
        "Audite solo documentos de movimiento de stock. No audite tarjetas de "
        "vacunación ni documentos con datos de pacientes.",
        "Califique cada documento con los ocho criterios de la tabla siguiente. Un "
        "documento es conforme solo si cumple los ocho a la vez.",
        "Registre proporciones de documentos y de entregas. No sume dosis.",
        "Anote el número del documento auditado en cada bloque y conserve el orden "
        "correlativo.",
        "Si un documento no cabe en la hoja, continúe en la hoja de continuación con "
        "el mismo número de bloque.",
    ])
    tabla(
        doc, [4394, 4394],
        [
            ["Regla de conformidad", "Regla de concordancia"],
            ["Un documento es conforme solo si cumple los ocho criterios a la vez; "
             "si falla uno, es no conforme.",
             "Una entrega es concordante si la cantidad entregada es igual a la "
             "programada, o si la diferencia tiene un documento formal archivado que "
             "la autoriza. No se suman dosis: la concordancia es una proporción de "
             "entregas."],
        ],
        tam=9.5, tam_cabecera=9.5, alto_min_cm=0.7, margenes_lr=57,
        alineaciones=["left", "left"],
    )

    parrafo(doc, "Criterios de conformidad", tam=10, negrita=True,
            alineacion="left", antes=6, despues=2, interlineado=1.0, keep=True)
    filas = [["Código", "Criterio"]]
    filas.extend([[codigo, texto] for codigo, texto, _ in _CRITERIOS])
    tabla(doc, _ANCHOS_CRITERIOS, filas, tam=9.5, tam_cabecera=9.5,
          alto_min_cm=0.6, margenes_lr=40, alineaciones=["center", "left"])
    nota(doc, "Cada bloque repite la etiqueta corta del criterio. El texto completo "
              "se califica una sola vez por documento.", antes=2, despues=4)

    _bloque_documento(doc, 1, version=version)
    for numero in (2, 3, 4):
        _bloque_documento(doc, numero, version=version)
    _bloque_documento(doc, 5, version=version)
    nota(doc, "Si el corpus excede estos cinco bloques, continúe desde D-06 en la "
              "hoja de continuación de los apoyos.", antes=1, despues=0)

    parrafo(doc, "Entregas. Concordancia entre cantidad programada y entregada",
            tam=10, negrita=True, alineacion="left", antes=6, despues=2,
            interlineado=1.0, keep=True)
    _tabla_cpe_rediseno(doc, 1, 12)
    nota(doc, "Si hay más de doce entregas, continúe en la hoja de continuación "
              "desde E-13, en los apoyos del investigador.", antes=2, despues=3)
    _conteos_cierre(doc)
    bloque_observaciones(doc, "Observaciones del auditor", alto_cm=1.8)
    parrafo(doc, "Firma del auditor: ______________________________________",
            tam=11, alineacion="left", antes=6, despues=1, interlineado=1.0)
    parrafo(doc, "Fecha de cierre de la ficha: ____/____/______", tam=11,
            alineacion="left", despues=0, interlineado=1.0)


def _leyenda_escala(doc) -> None:
    tabla(
        doc, _ANCHOS_ESCALA,
        [_ESCALA_ETIQUETAS, ["1", "2", "3", "4", "5"]],
        cabecera=False, tam=9.5, alto_min_cm=0.55, margenes_lr=30,
        alineaciones=["center"] * 5,
    )
    # La fila de valores se compone en negrita y 10 pt, después de la etiqueta.
    ultima = doc.tables[-1]
    _negrita_fila(ultima, 1, tam=10)


def _tabla_reactivos(doc, reactivos: Sequence[Dict[str, str]]) -> None:
    filas: List[List[str]] = []
    fusiones: List[int] = []
    cabeceras: List[int] = []
    grupo_actual = None
    for reactivo in reactivos:
        if reactivo["grupo"] != grupo_actual:
            grupo_actual = reactivo["grupo"]
            fusiones.append(len(filas))
            filas.append([grupo_actual, "", "", "", "", "", ""])
            cabeceras.append(len(filas))
            filas.append(["N.°", "Enunciado", "1", "2", "3", "4", "5"])
        filas.append([reactivo["codigo"], reactivo["texto"], "", "", "", "", ""])
    t = tabla(doc, _ANCHOS_CUESTIONARIO, filas, cabecera=False, tam=10,
              alto_min_cm=0.75, fusiones=fusiones, margenes_lr=40,
              alineaciones=["center", "left", "center", "center", "center",
                            "center", "center"])
    for indice in cabeceras:
        _negrita_fila(t, indice, tam=10)


def _cuerpo_cuestionario_a(doc, version: str = "v01") -> None:
    v02 = version == "v02"
    reactivos = extraer_reactivos()["A"]
    _titulo_formulario(
        doc, "03", "Instrumento 3. Cuestionario A. Satisfacción del usuario",
        "Modalidad A. Ocho reactivos con escala de 1 a 5")
    if v02:
        _rol_aplicacion(
            doc, "participante",
            "Fase INICIAL: antes de la intervención; fase FINAL: después.")
    parrafo(doc, "Este cuestionario recoge su experiencia en la gestión de movimientos "
                 "de vacunas. Sus respuestas son confidenciales y se identifican solo "
                 "mediante un código.", tam=10, alineacion="left", despues=3,
            interlineado=1.0)
    _identificacion(doc, [
        ["Código", "TRAB-______", "Fase", "________________ (INICIAL o FINAL)"],
        ["Código de centro", "________________", "Fecha", "____/____/______"],
        [("Investigador (admin.)" if v02 else "Investigador"), "", "", ""],
    ], fusiones=[(2, 1, 3, "____________________________________")],
       alto_cm=0.65)
    if v02:
        parrafo(doc, "Los campos de identificación son administrativos y los completa "
                     "el investigador; no son preguntas para el participante.",
                tam=9, cursiva=True, alineacion="left", despues=2,
                interlineado=1.0)
    if v02:
        lineas_instrucciones = [
            "Marque con una X una sola casilla por enunciado.",
            "La escala va de 1 a 5: 1 es totalmente en desacuerdo y 5 es totalmente "
            "de acuerdo.",
            "No escriba su nombre, apellido ni documento de identidad. Use solo el "
            "código que le entregue el investigador.",
        ]
    else:
        lineas_instrucciones = [
            "Marque con una X una sola casilla por enunciado.",
            "1 es totalmente en desacuerdo y 5 es totalmente de acuerdo. No hay "
            "respuestas correctas ni incorrectas.",
            "Responda según su experiencia en el registro y control de movimientos de "
            "vacunas.",
            "No escriba su nombre, apellido ni documento de identidad. Use solo el "
            "código que le entregue el investigador.",
        ]
    _instrucciones(doc, lineas_instrucciones)
    _leyenda_escala(doc)
    _tabla_reactivos(doc, reactivos)
    if not v02:
        nota(doc, "Esta hoja no se suma con el Módulo B. El puntaje se traslada a la "
                  "hoja de cierre del investigador y no se calcula en presencia del "
                  "participante.", antes=3, despues=0)
    bloque_observaciones(doc, "Observaciones del participante (opcional)",
                         alto_cm=0.9, antes=5 if not v02 else 4)


def _cuerpo_modulo_b(doc, version: str = "v01") -> None:
    v02 = version == "v02"
    reactivos = extraer_reactivos()["B"]
    _titulo_formulario(
        doc, "04", "Módulo B. Cuestionario complementario",
        "Módulo complementario del Instrumento 3. No se suma al Cuestionario A.",
        fijo=(None if v02
              else "Aplicación: solo al final, después de usar SIVAC."))
    if v02:
        _rol_aplicacion(doc, "participante",
                        "Fase FINAL: después de usar SIVAC.")
    parrafo(doc, "Este módulo recoge su experiencia con el uso de SIVAC en la gestión "
                 "de movimientos de vacunas. Sus respuestas son confidenciales y se "
                 "identifican solo mediante un código.", tam=10, alineacion="left",
            despues=1, interlineado=1.0)
    _identificacion(doc, [
        ["Código", "TRAB-______", "Fase", "FINAL"],
        ["Código de centro", "________________", "Fecha", "____/____/______"],
        [("Investigador (admin.)" if v02 else "Investigador"), "", "", ""],
    ], fusiones=[(2, 1, 3, "____________________________________")],
       alto_cm=0.65)
    if v02:
        parrafo(doc, "Los campos de identificación son administrativos y los completa "
                     "el investigador; no son preguntas para el participante.",
                tam=9, cursiva=True, alineacion="left", despues=2,
                interlineado=1.0)
        lineas_instrucciones = [
            "Este módulo se aplica solo al final, después de haber usado SIVAC.",
            "Marque con una X una sola casilla por enunciado, de 1 a 5.",
            "No escriba su nombre, apellido ni documento de identidad. Use solo el "
            "código que le entregue el investigador.",
        ]
        despues_instrucciones = 1
    else:
        lineas_instrucciones = [
            "Este módulo se aplica solo al final, después de haber usado SIVAC.",
            "Marque con una X una sola casilla por enunciado. La escala es la misma de "
            "1 a 5.",
            "No hay respuestas correctas ni incorrectas.",
            "Este módulo no se suma al Cuestionario A y no tiene puntaje global.",
            "No escriba su nombre, apellido ni documento de identidad.",
        ]
        despues_instrucciones = 0
    _instrucciones(doc, lineas_instrucciones, despues=despues_instrucciones)
    _leyenda_escala(doc)
    _tabla_reactivos(doc, reactivos)
    if not v02:
        nota(doc, "No se suma al Cuestionario A. Si no se aplica, se registra como no "
                  "aplicado y no se imputa.", antes=1, despues=0)
    bloque_observaciones(doc, "Observaciones del participante (opcional)",
                         alto_cm=0.9, antes=3 if not v02 else 4)


def _cabecera_limpia(seccion, pie: str) -> None:
    """Cabecera institucional sin rótulo de formulario; solo página a la derecha."""
    if seccion.header.is_linked_to_previous:
        seccion.header.is_linked_to_previous = False
    if seccion.footer.is_linked_to_previous:
        seccion.footer.is_linked_to_previous = False
    seccion.header_distance = Cm(_DISTANCIA_CABECERA_CM)
    seccion.footer_distance = Cm(1.25)
    cabecera = seccion.header
    for sobrante in list(cabecera.paragraphs)[1:]:
        sobrante._element.getparent().remove(sobrante._element)
    linea = cabecera.paragraphs[0]
    t = _tabla_cabecera_institucional(cabecera, _ANCHOS_CABECERA)
    linea._p.addprevious(t._tbl)
    _logo_en_celda(t.cell(0, 0), LOGO_UNAJMA_RECORTE, "Logotipo UNAJMA",
                   alineacion="left")
    _logo_en_celda(t.cell(0, 2), LOGO_EPIS, "Logotipo EPIS",
                   alineacion="right")
    celda_texto = t.cell(0, 1)
    for indice, texto in enumerate(_CABECERA_LINEAS):
        p = celda_texto.paragraphs[0] if indice == 0 else celda_texto.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(texto)
        _fuente(run, 8.5, negrita=(indice == 0))

    linea.text = ""
    linea.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    linea.paragraph_format.space_before = Pt(2)
    linea.paragraph_format.space_after = Pt(0)
    linea.paragraph_format.line_spacing = 1.0
    tabulaciones = linea.paragraph_format.tab_stops
    tabulaciones.add_tab_stop(Twips(4680), WD_TAB_ALIGNMENT.CLEAR)
    tabulaciones.add_tab_stop(Twips(9360), WD_TAB_ALIGNMENT.CLEAR)
    run = linea.add_run("Página ")
    _fuente(run, 9)
    _campo(linea, " PAGE ", tam=9)
    run = linea.add_run(" de ")
    _fuente(run, 9)
    _campo(linea, " NUMPAGES ", tam=9)
    _borde_inferior_parrafo(linea, color="808080", sz=4)

    pata = seccion.footer.paragraphs[0]
    pata.text = ""
    pata.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pata.paragraph_format.space_before = Pt(0)
    pata.paragraph_format.space_after = Pt(0)
    run = pata.add_run(pie)
    _fuente(run, 8.5)


def _tabla_limpia(doc, anchos, filas, *, cabecera=True, tam=10,
                  alto_min_cm=None, alineaciones=None, fusiones=(),
                  tam_cabecera=None, margen_vertical=60):
    """Tabla de campo con padding 80/60 dxa y rejilla exterior 1 pt."""
    t = tabla(doc, anchos, filas, cabecera=cabecera, tam=tam,
              alto_min_cm=alto_min_cm, alineaciones=alineaciones,
              margenes_lr=80, fusiones=fusiones, tam_cabecera=tam_cabecera)
    quir.ajustar_margenes_celda(doc, len(doc.tables) - 1, 80, 80,
                                margen_vertical, margen_vertical)
    quir.aplicar_bordes_campo(t)
    return t


def _pulir_tablas(doc) -> None:
    """Uniforma padding 80/60 dxa y rejilla 1 pt/0.5 pt en todas las tablas."""
    for indice in range(len(doc.tables)):
        quir.ajustar_margenes_celda(doc, indice, 80, 80, 60, 60)
        quir.aplicar_bordes_campo(doc.tables[indice])


def _h1_limpio(doc, texto: str) -> None:
    parrafo(doc, texto, tam=12, negrita=True, alineacion="left",
            antes=12, despues=6, interlineado=1.0, keep=True)


def _proposito_limpio(doc, texto: str) -> None:
    parrafo(doc, texto, tam=10.5, alineacion="left", despues=6,
            interlineado=1.0)


def _seccion_limpia(doc, texto: str, antes: float = 10) -> None:
    parrafo(doc, texto, tam=10, negrita=True, alineacion="left",
            antes=antes, despues=4, interlineado=1.0, keep=True)


def _instrucciones_limpias(doc, lineas: Sequence[str], tam: float = 12,
                           interlineado: float = 1.15, despues: float = 3) -> None:
    _seccion_limpia(doc, "Instrucciones")
    for indice, linea in enumerate(lineas, 1):
        parrafo(doc, f"{indice}. {linea}", tam=tam, alineacion="left",
                despues=despues, interlineado=interlineado)


def _nota_limpia(doc, texto: str, antes: float = 3, despues: float = 9) -> None:
    parrafo(doc, texto, tam=9.5, alineacion="left", antes=antes,
            despues=despues, interlineado=1.0)


def _separador(doc, alto_pt: float = 8) -> None:
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(alto_pt)
    pf.line_spacing = Pt(1)


def _identificacion_limpia(doc, filas, fusiones=(), alto_cm: float = 0.9) -> Any:
    etiquetas = {
        "Código": "Identificador del participante",
        "Código de centro": "Identificador del centro",
        "TRAB-______": "________________",
    }
    filas = [[etiquetas.get(valor, valor) for valor in fila] for fila in filas]
    filas = [[valor.replace("TRAB-______", "________________")
              for valor in fila] for fila in filas]
    t = _tabla_limpia(doc, _ANCHOS_ID, filas, cabecera=False, tam=10,
                      alto_min_cm=alto_cm, alineaciones=["left"] * 4)
    for fila, inicio, fin, texto in fusiones:
        celda = t.cell(fila, inicio).merge(t.cell(fila, fin))
        parrafos = celda._tc.findall(qn("w:p"))
        for sobrante in parrafos[1:]:
            if not "".join(t_nodo.text or ""
                           for t_nodo in sobrante.iter(qn("w:t"))).strip():
                celda._tc.remove(sobrante)
        _celda_texto(celda, texto, tam=10, alineacion="left")
    _negrita_columna(t, 0, list(range(len(filas))))
    return t


def _linea_continuacion_limpia(doc) -> None:
    parrafo(doc, "Identificador del participante: ______________   Fase "
                 "________ (INICIAL o FINAL)   Fecha ____/____/______",
            tam=8.5, alineacion="left", antes=0, despues=6, interlineado=1.0)


def _tabla_tareas_limpia(doc, tareas: Sequence[Tuple[str, str]],
                         desde: int) -> Any:
    filas = [
        ["Tarea", "Inicio", "Fin", "Tiempo (min)", "Pausa", "", "Válida", ""],
        ["", "", "", "", "Sí", "No", "Sí", "No"],
    ]
    for indice, (_, descripcion) in enumerate(tareas, desde):
        filas.append([
            f"{indice}. {descripcion}",
            "__:__:__",
            "__:__:__",
            "",
            "",
            "",
            "",
            "",
        ])
    t = _tabla_limpia(doc, _ANCHOS_F01_LIMPIA, filas, cabecera=False, tam=10,
                      alto_min_cm=1.0,
                      alineaciones=["left", "center", "center", "center",
                                    "center", "center", "center", "center"])
    for columna in range(4):
        t.cell(0, columna).merge(t.cell(1, columna))
    t.cell(0, 4).merge(t.cell(0, 5))
    t.cell(0, 6).merge(t.cell(0, 7))
    for indice in (0, 1):
        for celda in t.rows[indice].cells:
            for p in celda.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.bold = True
                    _fuente(run, 10)
    t.rows[0].height = Cm(0.65)
    t.rows[0].height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
    t.rows[1].height = Cm(0.55)
    t.rows[1].height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
    for fila in t.rows[2:]:
        fila.height = Cm(1.0)
        fila.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
    for fila in t.rows[:2]:
        trPr = fila._tr.get_or_add_trPr()
        if trPr.find(qn("w:tblHeader")) is None:
            trPr.append(OxmlElement("w:tblHeader"))
    return t


def _matriz_documentos_limpia(doc, numeros: Sequence[int],
                              compacto: bool = False) -> None:
    if compacto:
        meta = []
        for numero in numeros:
            meta.append([
                f"Documento {numero}",
                "N.º o serie: ______________   Tipo: ______________   "
                "Fecha: ____/____/______",
            ])
        m = _tabla_limpia(doc, _ANCHOS_F02_META_COMPACTO, meta, cabecera=False,
                          tam=9.5, alto_min_cm=0.55,
                          alineaciones=["left", "left"], margen_vertical=30)
    else:
        meta = [["Documento", "N.º o serie", "Tipo", "Fecha"]]
        for numero in numeros:
            meta.append([f"Documento {numero}", "", "", "____/____/______"])
        m = _tabla_limpia(doc, _ANCHOS_F02_META, meta, tam=10, tam_cabecera=9.5,
                          alto_min_cm=0.8,
                          alineaciones=["left", "left", "left", "center"])
    _nota_limpia(doc, "Marque una X en Sí o No para cada aspecto y documento."
                      + (" Definiciones y regla de concordancia: apoyos del "
                         "auditor." if compacto else ""),
                 antes=2 if compacto else 3, despues=2 if compacto else 3)
    filas = [["Aspecto a revisar", f"Documento {numeros[0]}", "",
              f"Documento {numeros[1]}", ""],
             ["", "Sí", "No", "Sí", "No"]]
    filas.extend([[nombre, "", "", "", ""]
                  for _, _, nombre in _CRITERIOS])
    t = _tabla_limpia(doc, _ANCHOS_F02_MATRIZ, filas, cabecera=False, tam=10,
                      alto_min_cm=0.8 if compacto else 0.9,
                      alineaciones=["left", "center", "center", "center",
                                    "center"],
                      margen_vertical=30 if compacto else 60)
    t.cell(0, 1).merge(t.cell(0, 2))
    t.cell(0, 3).merge(t.cell(0, 4))
    t.cell(0, 0).merge(t.cell(1, 0))
    for indice in (0, 1):
        for celda in t.rows[indice].cells:
            for p in celda.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.bold = True
                    _fuente(run, 9.5)
    t.rows[0].height = Cm(0.55 if compacto else 1.0)
    t.rows[0].height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
    t.rows[1].height = Cm(0.45 if compacto else 0.85)
    t.rows[1].height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
    for fila in t.rows[2:]:
        fila.height = Cm(0.9 if compacto else 0.95)
        fila.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
    if compacto:
        for fila in t.rows:
            for celda in fila.cells:
                for p in celda.paragraphs:
                    p.paragraph_format.space_before = Pt(0)
                    p.paragraph_format.space_after = Pt(0)
                    p.paragraph_format.line_spacing = 1.0
        for fila in m.rows:
            for celda in fila.cells:
                for p in celda.paragraphs:
                    p.paragraph_format.space_before = Pt(0)
                    p.paragraph_format.space_after = Pt(0)
                    p.paragraph_format.line_spacing = 1.0
    resultado = [["Documento", "Conforme", "No conforme", "Motivo"]]
    for numero in numeros:
        resultado.append([f"Documento {numero}", "", "", ""])
    r = _tabla_limpia(doc, _ANCHOS_F02_RESULTADO, resultado, tam=10,
                      tam_cabecera=9.5, alto_min_cm=0.65 if compacto else 0.85,
                      alineaciones=["left", "center", "center", "left"],
                      margen_vertical=30 if compacto else 60)
    if compacto:
        for fila in r.rows:
            for celda in fila.cells:
                for p in celda.paragraphs:
                    p.paragraph_format.space_before = Pt(0)
                    p.paragraph_format.space_after = Pt(0)
                    p.paragraph_format.line_spacing = 1.0
    _separador(doc, 4 if compacto else 8)


def _tabla_cpe_limpia(doc, desde: int, filas_datos: int) -> Any:
    filas = [["N.º", "Programada", "Entregada", "Diferencia",
              "Documento que autoriza", "Concordancia", ""],
             ["", "", "", "", "", "Sí", "No"]]
    for numero in range(desde, desde + filas_datos):
        filas.append([str(numero), "", "", "", "", "", ""])
    t = _tabla_limpia(doc, _ANCHOS_CPE_LIMPIA, filas, cabecera=False, tam=10,
                      alto_min_cm=0.9,
                      alineaciones=["center", "center", "center", "center",
                                    "left", "center", "center"])
    for columna in range(5):
        t.cell(0, columna).merge(t.cell(1, columna))
    t.cell(0, 5).merge(t.cell(0, 6))
    for indice in (0, 1):
        for celda in t.rows[indice].cells:
            for p in celda.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.bold = True
                    _fuente(run, 9.5)
    t.rows[0].height = Cm(0.8)
    t.rows[0].height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
    for fila in t.rows[2:]:
        fila.height = Cm(0.9)
        fila.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
    return t


def _observacion_limpia(doc, titulo: str, alto_cm: float = 1.4) -> None:
    if titulo:
        parrafo(doc, titulo, tam=10, negrita=True, alineacion="left",
                antes=8, despues=3, interlineado=1.0, keep=True)
    _tabla_limpia(doc, [ANCHO_UTIL], [[""]], cabecera=False, tam=10,
                  alto_min_cm=alto_cm)


def _grupo_visible(grupo: str) -> str:
    """Devuelve la etiqueta descriptiva sin el código interno del modelo."""
    for codigo, nombre in _GRUPOS_VISIBLES.items():
        if f"({codigo})" in grupo:
            return nombre
    return grupo


def _tabla_reactivos_limpia(doc, reactivos: Sequence[Dict[str, str]]) -> Any:
    filas: List[List[str]] = []
    fusiones: List[int] = []
    cabeceras: List[int] = []
    grupo_actual = None
    contador = 0
    for reactivo in reactivos:
        if reactivo["grupo"] != grupo_actual:
            grupo_actual = reactivo["grupo"]
            fusiones.append(len(filas))
            filas.append([_grupo_visible(grupo_actual),
                          "", "", "", "", "", ""])
            cabeceras.append(len(filas))
            filas.append(["N.º", "Enunciado", "1", "2", "3", "4", "5"])
        contador += 1
        filas.append([str(contador), reactivo["texto"], "", "", "", "", ""])
    t = _tabla_limpia(doc, _ANCHOS_LIKERT, filas, cabecera=False, tam=10,
                      alto_min_cm=0.7, fusiones=fusiones,
                      alineaciones=["center", "left", "center", "center",
                                    "center", "center", "center"])
    for indice in cabeceras:
        _negrita_fila(t, indice, tam=10)
    for fila in t.rows:
        for celda in fila.cells[1:2]:
            for p in celda.paragraphs:
                p.paragraph_format.line_spacing = 1.15
    return t


def _cuerpo_ficha01_limpio(doc) -> None:
    _h1_limpio(doc, "Instrumento 1. Ficha de observación de tiempos")
    _proposito_limpio(doc, "Oportunidad de procesamiento: tiempo de registro y "
                           "tiempo de emisión de vales.")
    _identificacion_limpia(doc, [
        ["Código", "TRAB-______", "Fase",
         "________________ (INICIAL o FINAL)"],
        ["Código de centro", "________________", "Fecha",
         "____/____/______"],
        ["Observador", "", "", ""],
    ], fusiones=[(2, 1, 3, "________________________________________________")])
    _instrucciones_limpias(doc, [
        "Cronometre con segundos y anote la hora de inicio y de fin.",
        "Si hay pausa, marque Sí y registre la causa en el registro de "
        "incidencias de los apoyos; el tiempo pausado no se cuenta.",
        "Convierta a minutos decimales: minutos más segundos divididos entre 60.",
    ])
    _seccion_limpia(doc, "A. Registro de movimientos")
    _tabla_tareas_limpia(doc, _TAREAS_REGISTRO[:3], 1)
    _seccion_limpia(doc, "B. Emisión de vales")
    _tabla_tareas_limpia(doc, _TAREAS_REGISTRO[3:], 4)
    _nota_limpia(doc, "Formato __:__:__. Criterios de inicio, fin, pausa y "
                      "validez: sección Protocolo del observador de los apoyos. "
                      "Incidencias: registro de incidencias y su continuación.",
                 antes=2, despues=2)
    _tabla_limpia(doc, [ANCHO_UTIL], [["Observaciones:"]], cabecera=False,
                  tam=9.5, alto_min_cm=0.7, alineaciones=["left"])
    parrafo(doc, "Firma del observador: ______________________     Inicio de la "
                 "sesión: ________     Fin: ________", tam=10, alineacion="left",
            antes=2, despues=0, interlineado=1.0)


def _cuerpo_ficha02_limpio(doc) -> None:
    _h1_limpio(doc, "Instrumento 2. Ficha de auditoría documental")
    _proposito_limpio(doc, "Consistencia documental: registros sin discrepancias "
                           "y concordancia programada con entregada.")
    _identificacion_limpia(doc, [
        ["Código", "TRAB-______", "Fase",
         "________________ (INICIAL o FINAL)"],
        ["Código de centro", "________________", "Fecha",
         "____/____/______"],
        ["Ventana auditada", "", "", ""],
    ], fusiones=[
        (2, 1, 3, "del ____/____/______ al ____/____/______   "
                  "Auditor: ____________________"),
    ], alto_cm=0.8)
    _instrucciones_limpias(doc, [
        "Audite solo documentos de movimiento de stock; no audite tarjetas de "
        "vacunación.",
        "Califique los ocho aspectos: conforme solo si todos se marcan Sí.",
    ], tam=10.5, interlineado=1.0, despues=2)
    _seccion_limpia(doc, "Registro documental. Documentos 1 y 2", antes=3)
    _matriz_documentos_limpia(doc, [1, 2], compacto=True)
    _nota_limpia(doc, "Para los documentos 3 y 4, continúe en la página "
                      "siguiente con el mismo correlativo real.",
                 antes=2, despues=0)
    _salto(doc)
    _linea_continuacion_limpia(doc)
    _seccion_limpia(doc, "Registro documental. Documentos 3 y 4", antes=0)
    _matriz_documentos_limpia(doc, [3, 4])
    _nota_limpia(doc, "Para más documentos, continúe desde el documento 5 en "
                      "Continuación. Registro documental de los apoyos, "
                      "manteniendo el correlativo real.",
                 antes=2, despues=0)
    _salto(doc)
    _linea_continuacion_limpia(doc)
    _seccion_limpia(doc, "Entregas. Concordancia programada y entregada", antes=0)
    _tabla_cpe_limpia(doc, 1, 12)
    _nota_limpia(doc, "Para más entregas, continúe desde la entrega 13 en "
                      "Continuación. Entregas de los apoyos, manteniendo el "
                      "correlativo real.",
                 antes=2, despues=2)
    _nota_limpia(doc, "Concordante: igual a lo programado o diferencia "
                      "autorizada. No se suman dosis.", antes=0, despues=5)
    _tabla_limpia(doc, [ANCHO_UTIL], [["Observaciones:"]], cabecera=False,
                  tam=9.5, alto_min_cm=0.9, alineaciones=["left"])
    parrafo(doc, "Firma del auditor: ______________________________     "
                 "Fecha: ____/____/______", tam=10, alineacion="left",
            antes=4, despues=0, interlineado=1.0)


def _cuerpo_cuestionario_a_limpio(doc) -> None:
    reactivos = extraer_reactivos()["A"]
    _h1_limpio(doc, "Instrumento 3. Cuestionario de satisfacción del usuario")
    _proposito_limpio(doc, "Aceptación del proceso y utilidad percibida. No "
                           "hay respuestas correctas ni incorrectas. "
                           "Información confidencial para uso académico.")
    _identificacion_limpia(doc, [
        ["Código", "TRAB-______", "Fase",
         "________________ (INICIAL o FINAL)"],
        ["Código de centro", "________________", "Fecha",
         "____/____/______"],
    ])
    _instrucciones_limpias(doc, [
        "Marque una sola casilla por enunciado según su experiencia.",
        "No escriba nombre ni documento de identidad; use solo el código "
        "asignado.",
    ])
    _tabla_escala_limpia(doc)
    _tabla_reactivos_limpia(doc, reactivos)


def _cuerpo_modulo_b_limpio(doc) -> None:
    reactivos = extraer_reactivos()["B"]
    _h1_limpio(doc, "Cuestionario complementario sobre el uso de SIVAC")
    _proposito_limpio(doc, "Complemento del instrumento 3; solo medición final; "
                           "no se suma al Cuestionario de satisfacción. No hay "
                           "respuestas correctas ni incorrectas. Información "
                           "confidencial para uso académico.")
    _identificacion_limpia(doc, [
        ["Código", "TRAB-______", "Fase", "FINAL"],
        ["Código de centro", "________________", "Fecha",
         "____/____/______"],
    ])
    _instrucciones_limpias(doc, [
        "Marque una sola casilla por enunciado según su experiencia.",
        "No escriba nombre ni documento de identidad; use solo el código "
        "asignado.",
    ])
    _tabla_escala_limpia(doc)
    _tabla_reactivos_limpia(doc, reactivos)


def _tabla_escala_limpia(doc) -> Any:
    t = _tabla_limpia(doc, _ANCHOS_ESCALA,
                      [["1", "2", "3", "4", "5"], _ESCALA_ETIQUETAS],
                      cabecera=False, tam=9.5, alto_min_cm=0.5,
                      alineaciones=["center"] * 5)
    _negrita_fila(t, 0, tam=10)
    return t


def _apoyos_protocolo(doc) -> None:
    _h1_limpio(doc, "Apoyos del investigador. Protocolo y registro")
    _seccion_limpia(doc, "Quién llena cada hoja")
    _tabla_limpia(
        doc, [2600, 2200, 2200, 1788],
        [
            ["Hoja", "Quién la llena", "Quién firma", "Fase"],
            ["Ficha de observación de tiempos", "Observador", "Observador",
             "INICIAL o FINAL"],
            ["Ficha de auditoría documental", "Auditor", "Auditor",
             "INICIAL o FINAL"],
            ["Cuestionario de satisfacción", "Participante", "No requiere firma",
             "INICIAL o FINAL"],
            ["Cuestionario complementario", "Participante", "No requiere firma",
             "FINAL"],
        ],
        tam=10, tam_cabecera=9.5, alto_min_cm=0.7,
        alineaciones=["left"] * 4,
    )
    _seccion_limpia(doc, "Protocolo del observador")
    for indice, linea in enumerate([
        "Inicio del registro: cuando el operador toma el documento fuente o "
        "abre el módulo.",
        "Fin del registro: cuando el movimiento queda guardado y balanceado.",
        "El tiempo de emisión inicia al recibir o abrir la solicitud y termina "
        "cuando el vale queda generado, firmado o impreso con numeración "
        "oficial.",
        "Pausa: solo por interrupción externa; detenga el cronómetro y anote la "
        "causa en el registro de incidencias.",
        "Tarea no completada: anule, anote el motivo y repítala dentro de la "
        "ventana; nunca la anule por ser lenta.",
        "Conversión: divida los segundos entre 60 y súmelos a los minutos. "
        "Ejemplo de conversión, no medición: 3 minutos y 15 segundos equivalen "
        "a 3,25 minutos.",
        "Identificación: use el mismo identificador del participante en la "
        "medición inicial y final; no escriba nombres.",
        "Cierre: firme la ficha y anote la hora de inicio y de fin de la sesión.",
    ], 1):
        parrafo(doc, f"{indice}. {linea}", tam=10.5, alineacion="left",
                despues=3, interlineado=1.1)
    _seccion_limpia(doc, "Registro de incidencias")
    _tabla_incidencias_limpia(doc, 1, 4)
    _nota_limpia(doc, "Referencia: identificador del participante, fase y tarea "
                      "de registro o emisión; si la incidencia afecta un "
                      "documento, anote su número o serie. Causa: interrupción "
                      "externa, desviación del protocolo o ayuda sustantiva del "
                      "investigador. Acción: pausa, anulación o repetición. Si "
                      "hay más de cuatro, continúe en el Registro de "
                      "incidencias de los apoyos.",
                 antes=2, despues=0)


def _apoyos_criterios(doc) -> None:
    _h1_limpio(doc, "Apoyos del investigador. Criterios y control")
    _seccion_limpia(doc, "Criterios de conformidad")
    filas = [["Aspecto", "Definición"]]
    filas.extend([[nombre, texto] for _, texto, nombre in _CRITERIOS])
    _tabla_limpia(doc, [2600, 6188], filas, tam=10, tam_cabecera=9.5,
                  alto_min_cm=0.65, alineaciones=["left", "left"])
    _seccion_limpia(doc, "Regla de concordancia")
    parrafo(doc, "Una entrega es concordante si la cantidad entregada es igual a "
                 "la programada, o si la diferencia tiene un documento formal "
                 "archivado que la autoriza. La concordancia es una proporción de "
                 "entregas; no se suman dosis.", tam=10.5, alineacion="left",
            despues=8, interlineado=1.15)
    _seccion_limpia(doc, "Control de aplicación y observaciones")
    filas_control = [["Identificador del participante", "Fase", "Formulario",
                      "Fecha", "Investigador", "Observación"]]
    for indice in range(8):
        formulario = ("Cuestionario de satisfacción" if indice < 4
                      else "Cuestionario complementario")
        filas_control.append(["________", "", formulario,
                              "___/___/____", "", ""])
    _tabla_limpia(doc, [1700, 900, 2100, 1400, 1400, 1288], filas_control,
                  tam=9.5, tam_cabecera=9.5, alto_min_cm=0.9,
                  alineaciones=["center", "center", "left", "center", "left",
                                "left"])
    _nota_limpia(doc, "Una fila por aplicación; observación opcional A o B.",
                 antes=2, despues=0)


def _apoyos_instrucciones(doc) -> None:
    _titulo_formulario(
        doc, "APOYO", "Apoyos del investigador. Instrucciones esenciales",
        "Qué hoja se llena, en qué orden y con qué límites")
    parrafo(doc, "Quién llena cada hoja", tam=10, negrita=True, alineacion="left",
            antes=4, despues=2, interlineado=1.0, keep=True)
    tabla(
        doc, [2600, 2200, 2200, 1788],
        [
            ["Hoja", "Quién la llena", "Quién firma", "Fase"],
            ["01. Ficha de tiempos", "Observador", "Observador",
             "INICIAL o FINAL"],
            ["02. Ficha de auditoría", "Auditor", "Auditor", "INICIAL o FINAL"],
            ["03. Cuestionario A", "Participante", "No requiere firma",
             "INICIAL o FINAL"],
            ["04. Módulo B", "Participante", "No requiere firma", "Solo FINAL"],
        ],
        tam=10, tam_cabecera=9.5, alto_min_cm=0.7, margenes_lr=40,
        alineaciones=["left"] * 4,
    )
    parrafo(doc, "Orden de aplicación", tam=10, negrita=True, alineacion="left",
            antes=8, despues=2, interlineado=1.0, keep=True)
    for indice, linea in enumerate([
        "Firme el consentimiento antes de aplicar cualquier hoja y guárdelo aparte. "
        "No se reproduce en este conjunto.",
        "Fase inicial: aplique 01, 02 y 03. No aplique el Módulo B.",
        "Fase final: repita 01, 02 y 03 y agregue 04.",
        "Anote la fase con las palabras INICIAL o FINAL. No use marcas preimpresas.",
        "Escriba solo el código TRAB y el código de centro. No escriba nombres, "
        "documentos de identidad ni el nombre del establecimiento.",
        "No invente fechas, respuestas, mediciones ni firmas.",
    ], 1):
        parrafo(doc, f"{indice}. {linea}", tam=10, alineacion="left", despues=1,
                interlineado=1.0)
    parrafo(doc, "Límites de uso", tam=10, negrita=True, alineacion="left",
            antes=8, despues=2, interlineado=1.0, keep=True)
    for linea in [
        "No sume el Módulo B con el Cuestionario A.",
        "No anote puntajes en las hojas del participante.",
        "No audite documentos con datos de pacientes.",
        "No incluya documentos de validación por expertos dentro del paquete de campo.",
        "No complete una tarea o una entrega que no se realizó.",
    ]:
        parrafo(doc, f"• {linea}", tam=10, alineacion="left", despues=1,
                interlineado=1.0)


def _apoyos_cierre(doc) -> None:
    _h1_limpio(doc, "Apoyos del investigador. Hoja de cierre")
    _proposito_limpio(doc, "Concentra los conteos de la fase; no se entrega al "
                           "participante.")
    _identificacion_limpia(doc, [
        ["Código", "TRAB-______", "Fase",
         "________________ (INICIAL o FINAL)"],
        ["Código de centro", "________________", "Fecha de cierre",
         "____/____/______"],
    ])
    _seccion_limpia(doc, "A. Oportunidad de procesamiento")
    tabla(
        doc, [3600, 1500, 1800, 1888],
        [
            ["Indicador", "Tareas válidas", "Media (minutos)", "Mediana (minutos)"],
            ["Tiempo de registro de movimientos", "", "", ""],
            ["Tiempo de emisión de vales", "", "", ""],
        ],
        tam=10, tam_cabecera=9.5, alto_min_cm=0.7, margenes_lr=40,
        alineaciones=["left", "center", "center", "center"],
    )
    _seccion_limpia(doc, "B. Consistencia documental")
    _tabla_limpia(
        doc, [4388, 2200, 2200],
        [
            ["Conteo crudo", "Documentos", "Entregas"],
            ["Total registrado", "", ""],
            ["Conformes o concordantes", "", ""],
            ["No conformes o no concordantes", "", ""],
        ],
        tam=10, tam_cabecera=9.5, alto_min_cm=0.65,
        alineaciones=["left", "center", "center"],
    )
    parrafo(doc, "Registros sin discrepancias", tam=10, negrita=True,
            alineacion="left", antes=8, despues=2, interlineado=1.0, keep=True)
    parrafo(doc, "Para calcular los registros sin discrepancias, divida el "
                 "número de documentos conformes entre el total de documentos "
                 "auditados y multiplique el resultado por cien.", tam=10,
            alineacion="left", despues=1, interlineado=1.0)
    parrafo(doc, "Para calcular la concordancia programada y entregada, divida "
                 "el número de entregas concordantes entre el total de entregas "
                 "evaluadas y multiplique el resultado por cien.", tam=10,
            alineacion="left", despues=1, interlineado=1.0)
    _nota_limpia(doc, "El denominador es el total de documentos auditados y el "
                      "total de entregas evaluadas. No se suman dosis.",
                 antes=1, despues=3)
    tabla(
        doc, [4200, 1500, 1500, 1588],
        [
            ["Indicador", "Numerador", "Denominador", "Porcentaje"],
            ["Registros sin discrepancias", "", "", ""],
            ["Concordancia programada y entregada", "", "", ""],
        ],
        tam=10, tam_cabecera=9.5, alto_min_cm=0.7, margenes_lr=40,
        alineaciones=["left", "center", "center", "center"],
    )
    parrafo(doc, "Modo de corpus: ________    (A global por ventana / B por "
                 "trabajador y ventana / C otro)", tam=10, alineacion="left",
            antes=4, despues=2, interlineado=1.0)
    _seccion_limpia(doc, "C. Satisfacción del usuario")
    tabla(
        doc, [5200, 1800, 1788],
        [
            ["Indicador", "Suma", "Media"],
            ["Aceptación del proceso, cuatro reactivos", "", ""],
            ["Utilidad percibida para la gestión, cuatro reactivos", "", ""],
            ["Total del Cuestionario de satisfacción, ocho reactivos", "", ""],
        ],
        tam=10, tam_cabecera=9.5, alto_min_cm=0.7, margenes_lr=40,
        alineaciones=["left", "center", "center"],
    )
    _nota_limpia(doc, "Terciles: hoja de puntuación vigente del investigador.",
                 antes=2, despues=3)
    parrafo(doc, "Firma de consolidación: ______________________     Fecha de "
                 "cierre: ____/____/______", tam=10, alineacion="left", antes=6,
            despues=0, interlineado=1.0)


def _continuacion_rsd(doc, version: str = "v01", desde: int = 6) -> None:
    _titulo_formulario(
        doc, "CONTINUACIÓN", "Continuación de la Ficha 02. Documentos auditados",
        "Continúe el correlativo real de los bloques D; no reinicie en D-06 si la "
        "ficha ya avanzó.")
    _identificacion_apoyo(doc)
    for numero in range(desde, desde + 3):
        _bloque_documento(doc, numero, version=version)


def _continuacion_cpe(doc) -> None:
    _titulo_formulario(
        doc, "CONTINUACIÓN", "Continuación de la Ficha 02. Entregas",
        "Continúe el correlativo real de las entregas E; no reinicie en E-13 si la "
        "ficha ya avanzó.")
    _identificacion_apoyo(doc)
    _tabla_cpe_rediseno(doc, 13, 12, alto_cm=1.4)
    nota(doc, "Si hay más de veinticuatro entregas, abra otra hoja y continúe la "
              "numeración correlativa.", antes=2, despues=0)


def _continuacion_incidencias(doc) -> None:
    _titulo_formulario(
        doc, "CONTINUACIÓN", "Continuación de la Ficha 01. Incidencias",
        "Continúe el correlativo real de las incidencias H; no reinicie en H-05 si "
        "la ficha ya avanzó.")
    _identificacion_apoyo(doc)
    _tabla_incidencias(doc, 5, 8, alto_cm=1.7)
    nota(doc, "Causa: interrupción externa, desviación del protocolo o ayuda del "
              "investigador. Acción: pausa, anulación o repetición.", antes=2,
         despues=0)


def _guardar(doc, ruta: Path) -> Path:
    seguridad.asegurar_escritura_permitida(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    _cierre_documento(doc)
    doc.save(str(ruta))
    return ruta


def _exportar(docx_path: Path, pdf_path: Path) -> Dict[str, Any]:
    seguridad.asegurar_escritura_permitida(pdf_path)
    if pdf_path.exists():
        pdf_path.unlink()
    return quir.exportar_docx_a_pdf(docx_path, pdf_path)


def _fuente_minima(ruta_docx: Path) -> Optional[float]:
    documento = docx.Document(str(ruta_docx))
    tamanos: List[float] = []

    def _revisar(parrafos) -> None:
        for p in parrafos:
            for run in p.runs:
                if run.font.size is not None:
                    tamanos.append(float(run.font.size.pt))

    _revisar(documento.paragraphs)
    for t in documento.tables:
        for fila in t.rows:
            for celda in fila.cells:
                _revisar(celda.paragraphs)
    for seccion in documento.sections:
        _revisar(seccion.header.paragraphs)
        _revisar(seccion.footer.paragraphs)
    return min(tamanos) if tamanos else None


def _reactivos_en_docx(ruta_docx: Path) -> Dict[str, str]:
    documento = docx.Document(str(ruta_docx))
    encontrados: Dict[str, str] = {}
    for t in documento.tables:
        for fila in t.rows:
            celdas = [c.text.strip() for c in fila.cells]
            for indice, celda in enumerate(celdas[:-1]):
                if re.match(r"^(AP|UP|PU|PE)-\d{2}$", celda):
                    encontrados.setdefault(celda, celdas[indice + 1])
    return encontrados


def _reactivos_ordenados_en_docx(ruta_docx: Path) -> List[str]:
    """Lee los enunciados visibles en orden, sin depender de códigos impresos."""
    documento = docx.Document(str(ruta_docx))
    textos: List[str] = []
    for t in documento.tables:
        for fila in t.rows:
            celdas = [c.text.strip() for c in fila.cells]
            if (len(celdas) >= 7 and re.fullmatch(r"\d{1,2}", celdas[0])
                    and len(celdas[1]) > 30):
                textos.append(re.sub(r"\s+", " ", celdas[1]).strip())
    return textos


_CAMPOS_PARTICIPANTE = (
    "Código de centro",
    "Investigador",
    "Observaciones del participante (opcional)",
)


def _alto_ultima_tabla_cm(ruta_docx: Path) -> Optional[float]:
    """Alto mínimo declarado en la última tabla (recuadro de observaciones)."""
    documento = docx.Document(str(ruta_docx))
    if not documento.tables:
        return None
    alto = documento.tables[-1].rows[0].height
    return round(alto.cm, 2) if alto is not None else None


def _control_rediseno(docx_path: Path, pdf_path: Path) -> Dict[str, Any]:
    texto = _texto_pdf(pdf_path)
    tablas = _tablas_docx(docx_path)
    fuentes = _PROHIBIDOS + ["ISO", "baremo", "U+2014"]
    return {
        "docx": str(docx_path),
        "pdf": str(pdf_path),
        "sha256_docx": seguridad.sha256_archivo(docx_path),
        "sha256_pdf": seguridad.sha256_archivo(pdf_path),
        "bytes_docx": docx_path.stat().st_size,
        "bytes_pdf": pdf_path.stat().st_size,
        "paginas": _paginas_pdf(pdf_path),
        "tablas": len(tablas),
        "tablas_detalle": tablas,
        "ancho_max_dxa": max((t["ancho_dxa"] for t in tablas), default=0),
        "tablas_fuera_de_ancho": [t["indice"] for t in tablas
                                  if t["ancho_dxa"] != ANCHO_UTIL],
        "tablas_flotantes": [t["indice"] for t in tablas if t["flotante"]],
        "tablas_sin_rejilla": [t["indice"] for t in tablas
                               if t["insideV"] != "single" and t["filas"] > 0],
        "filas_sin_cantsplit": [t["indice"] for t in tablas
                                if t["filas_cantSplit"] != t["filas"]],
        "desborde_inferior_pt": _desborde_inferior(pdf_path),
        "fuente_minima_pt": _fuente_minima(docx_path),
        "tokens_prohibidos": [t for t in fuentes if t in texto],
        "fechas_impresas": _PATRON_FECHA.findall(texto),
        "trab_con_numero": _PATRON_TRAB.findall(texto),
        "campos_participante": {
            campo: campo in texto for campo in _CAMPOS_PARTICIPANTE
        },
        "observaciones_alto_cm": (
            _alto_ultima_tabla_cm(docx_path)
            if "Observaciones del participante (opcional)" in texto else None
        ),
        "auditoria_motor": quir.auditar_docx_openxml(docx_path),
    }


def _control_cabecera_nativa(docx_path: Path, pdf_path: Path) -> Dict[str, Any]:
    """Audita la cabecera en el DOCX y su posición real en cada página del PDF."""
    import pymupdf

    documento = docx.Document(str(docx_path))
    secciones: List[Dict[str, Any]] = []
    for indice, seccion in enumerate(documento.sections):
        cabecera = seccion.header
        tabla = cabecera.tables[0] if cabecera.tables else None
        grid = ([int(g.get(qn("w:w"))) for g in tabla._tbl.tblGrid.gridCol_lst]
                if tabla is not None else [])
        tblPr = tabla._tbl.tblPr if tabla is not None else None
        bordes = tblPr.find(qn("w:tblBorders")) if tblPr is not None else None
        bordes_nil = bool(bordes is not None) and all(
            (borde.get(qn("w:val")) in ("nil", "none"))
            for borde in list(bordes))
        inline = list(cabecera._element.iter(qn("wp:inline")))
        anclas = list(cabecera._element.iter(qn("wp:anchor")))
        imagenes: List[Dict[str, Any]] = []
        for nodo in inline:
            extension = nodo.find(qn("wp:extent"))
            blip = next(nodo.iter(qn("a:blip")), None)
            rid = blip.get(qn("r:embed")) if blip is not None else None
            destino = (cabecera.part.rels[rid].target_ref
                       if rid and rid in cabecera.part.rels else None)
            ancho = int(extension.get("cx")) if extension is not None else 0
            alto = int(extension.get("cy")) if extension is not None else 0
            imagenes.append({
                "relacion": rid,
                "destino": destino,
                "cx_emu": ancho,
                "cy_emu": alto,
                "relacion_aspecto": round(ancho / alto, 6) if alto else None,
            })
        instr = [nodo.get(qn("w:instr")) for nodo in
                 cabecera._element.iter(qn("w:fldSimple"))]
        texto = "".join(cabecera._element.itertext())
        secciones.append({
            "indice": indice,
            "vinculada_anterior": cabecera.is_linked_to_previous,
            "tablas": len(cabecera.tables),
            "columnas_dxa": grid,
            "columnas_laterales_iguales": (
                len(grid) == 3 and grid[0] == grid[2]),
            "bordes_nil": bordes_nil,
            "flotante": (tblPr is not None
                         and tblPr.find(qn("w:tblpPr")) is not None),
            "imagenes_inline": len(inline),
            "imagenes_ancla": len(anclas),
            "imagenes": imagenes,
            "campos": instr,
            "page": any("PAGE" in (i or "") and "NUMPAGES" not in (i or "")
                        for i in instr),
            "numpages": any("NUMPAGES" in (i or "") for i in instr),
            "lineas_institucionales": all(
                linea in texto for linea in _CABECERA_LINEAS),
            "distancia_cabecera_cm": round(seccion.header_distance.cm, 3),
            "margen_superior_cm": round(seccion.top_margin.cm, 3),
            "margen_inferior_cm": round(seccion.bottom_margin.cm, 3),
            "margen_izquierdo_cm": round(seccion.left_margin.cm, 3),
            "margen_derecho_cm": round(seccion.right_margin.cm, 3),
            "ancho_pagina_cm": round(seccion.page_width.cm, 3),
            "alto_pagina_cm": round(seccion.page_height.cm, 3),
        })

    paginas: List[Dict[str, Any]] = []
    with pymupdf.open(str(pdf_path)) as pdf:
        for numero, pagina in enumerate(pdf, 1):
            ancho_pagina = float(pagina.rect.width)
            alto_pagina = float(pagina.rect.height)
            contenido_izq = 3.0 / 2.54 * 72
            contenido_der = ancho_pagina - 2.5 / 2.54 * 72
            spans: List[Tuple[List[float], str]] = []
            for bloque in pagina.get_text("dict")["blocks"]:
                if bloque.get("type") != 0:
                    continue
                for linea in bloque.get("lines", []):
                    for span in linea.get("spans", []):
                        texto_span = str(span.get("text", "")).strip()
                        if texto_span:
                            spans.append(([float(v) for v in span["bbox"]],
                                          texto_span))
            logos = sorted(
                [info for info in pagina.get_image_info()
                 if info.get("bbox")],
                key=lambda info: float(info["bbox"][0]))
            cabecera_texto = [s for s in spans if any(
                linea in s[1] for linea in _CABECERA_LINEAS)]
            rotulo = [s for s in spans if "FORMULARIO" in s[1]
                      or "APOYOS DEL INVESTIGADOR" in s[1]]
            paginacion = [s for s in spans if "Página" in s[1]]
            paginacion += [s for s in spans
                           if re.fullmatch(r"\d+", s[1])
                           and s[0][1] < 70 and s[0][0] > 450]
            cuerpo = [s for s in spans
                      if s[0][1] >= 66 and s[0][1] < 750
                      and not any(linea in s[1] for linea in _CABECERA_LINEAS)
                      and "FORMULARIO" not in s[1]
                      and "APOYOS DEL INVESTIGADOR" not in s[1]
                      and "Página" not in s[1]]
            cuerpo_top = min((s[0][1] for s in cuerpo), default=None)
            piezas = cabecera_texto + rotulo + paginacion
            cabecera_bottom = max(
                [s[0][3] for s in piezas]
                + [float(info["bbox"][3]) for info in logos],
                default=None)
            pagina_bbox = None
            if paginacion:
                pagina_bbox = [
                    min(s[0][0] for s in paginacion),
                    min(s[0][1] for s in paginacion),
                    max(s[0][2] for s in paginacion),
                    max(s[0][3] for s in paginacion),
                ]
            izquierdo = logos[0]["bbox"] if logos else None
            derecho = logos[-1]["bbox"] if len(logos) >= 2 else None
            alto_izq = (float(izquierdo[3]) - float(izquierdo[1])
                        if izquierdo else None)
            alto_der = (float(derecho[3]) - float(derecho[1])
                        if derecho else None)
            centro_izq = ((float(izquierdo[1]) + float(izquierdo[3])) / 2
                          if izquierdo else None)
            centro_der = ((float(derecho[1]) + float(derecho[3])) / 2
                          if derecho else None)
            inset_izq = (float(izquierdo[0]) - contenido_izq
                         if izquierdo else None)
            inset_der = (contenido_der - float(derecho[2])
                         if derecho else None)
            solape = None
            if derecho is not None and pagina_bbox is not None:
                p = pagina_bbox
                solape = not (float(derecho[2]) < p[0]
                              or p[2] < float(derecho[0])
                              or float(derecho[3]) < p[1]
                              or p[3] < float(derecho[1]))
            paginas.append({
                "pagina": numero,
                "alto_pagina_pt": round(alto_pagina, 2),
                "logos": len(logos),
                "alto_logo_izq_pt": round(alto_izq, 2) if alto_izq else None,
                "alto_logo_der_pt": round(alto_der, 2) if alto_der else None,
                "diferencia_alto_logos_pt": (
                    round(abs(alto_izq - alto_der), 2)
                    if alto_izq and alto_der else None),
                "centro_vertical_logos_pt": (
                    round(abs(centro_izq - centro_der), 2)
                    if centro_izq and centro_der else None),
                "inset_izq_pt": round(inset_izq, 2) if inset_izq is not None else None,
                "inset_der_pt": round(inset_der, 2) if inset_der is not None else None,
                "diferencia_simetria_pt": (
                    round(abs(inset_izq - inset_der), 2)
                    if inset_izq is not None and inset_der is not None else None),
                "cabecera_bottom_pt": (
                    round(cabecera_bottom, 2) if cabecera_bottom else None),
                "cuerpo_top_pt": round(cuerpo_top, 2) if cuerpo_top else None,
                "separacion_cabecera_cuerpo_pt": (
                    round(cuerpo_top - cabecera_bottom, 2)
                    if cuerpo_top and cabecera_bottom else None),
                "margen_superior_respetado": (
                    cuerpo_top is not None and cuerpo_top >= 70.0),
                "sin_empuje_de_cabecera": (
                    cuerpo_top is not None and cuerpo_top <= 78.0),
                "sin_solape_epis_paginacion": (solape is False
                                               if solape is not None else None),
                "rotulo_en_cabecera": bool(rotulo),
                "paginacion_en_cabecera": bool(paginacion),
            })
    return {
        "secciones": secciones,
        "paginas": paginas,
        "todas_las_paginas_con_dos_logos": all(
            p["logos"] == 2 for p in paginas),
        "todas_las_paginas_sin_solape": all(
            p["sin_solape_epis_paginacion"] is not False for p in paginas),
        "todas_las_paginas_sin_empuje": all(
            p["sin_empuje_de_cabecera"] for p in paginas),
        "altura_visual_uniforme": all(
            (p["diferencia_alto_logos_pt"] or 0) <= 0.75 for p in paginas),
        "simetria_lateral": all(
            (p["diferencia_simetria_pt"] or 0) <= 1.5 for p in paginas),
        "secciones_desvinculadas": all(
            not s["vinculada_anterior"] for s in secciones),
        "todas_las_secciones_con_tabla": all(
            s["tablas"] == 1 and s["columnas_laterales_iguales"]
            for s in secciones),
        "imagenes_solo_inline": all(
            s["imagenes_inline"] == 2 and s["imagenes_ancla"] == 0
            for s in secciones),
        "campos_nativos": all(s["page"] and s["numpages"] for s in secciones),
    }


_REDISENO_REGISTRO = [
    ("01_FICHA_TIEMPOS", "FORMULARIO 01 · FICHA DE OBSERVACIÓN DE TIEMPOS",
     "Instrumento 1 · Código TRAB-______", "Instrumento 1. Ficha de observación de tiempos"),
    ("02_FICHA_AUDITORIA_DOCUMENTAL",
     "FORMULARIO 02 · FICHA DE AUDITORÍA DOCUMENTAL",
     "Instrumento 2 · Código TRAB-______",
     "Instrumento 2. Ficha de auditoría documental"),
    ("03_CUESTIONARIO_SATISFACCION_A", "FORMULARIO 03 · CUESTIONARIO A",
     "Instrumento 3 · Código TRAB-______",
     "Instrumento 3. Cuestionario A. Satisfacción del usuario"),
    ("04_MODULO_COMPLEMENTARIO_B_POST", "FORMULARIO 04 · MÓDULO B",
     "Instrumento 3, módulo B · Código TRAB-______",
     "Módulo B. Cuestionario complementario"),
]


def _preparar_logo_unajma() -> Path:
    """Deriva una copia con solo el margen blanco y el marco azul externo recortados."""
    from PIL import Image

    ASSETS_V02.mkdir(parents=True, exist_ok=True)
    with Image.open(LOGO_UNAJMA) as original:
        recorte = original.convert("RGB").crop((348, 154, 1707, 1914))
        recorte.save(LOGO_UNAJMA_RECORTE, optimize=True)
    return LOGO_UNAJMA_RECORTE


def construir_rediseno_fany(con_pdf: bool = True, con_render: bool = True,
                            version: str = "v01") -> Dict[str, Any]:
    """Emite la carpeta nueva, sus PDF y el manifiesto propio. No toca lo anterior."""
    if version not in ("v01", "v02"):
        raise ValueError("La versión editorial debe ser v01 o v02")
    v02 = version == "v02"
    destino = REDISENO_V02 if v02 else REDISENO
    render_dir = REDISENO_V02_RENDER if v02 else REDISENO_RENDER
    apoyos_dir = APOYOS_V02 if v02 else APOYOS
    cabecera = _cabecera_institucional if v02 else _cabecera_pie
    destino.mkdir(parents=True, exist_ok=True)
    apoyos_dir.mkdir(parents=True, exist_ok=True)
    render_dir.mkdir(parents=True, exist_ok=True)
    if v02:
        _preparar_logo_unajma()

    constructores = {
        "01_FICHA_TIEMPOS": lambda doc: _cuerpo_ficha01(doc, version=version),
        "02_FICHA_AUDITORIA_DOCUMENTAL": lambda doc: _cuerpo_ficha02(
            doc, version=version),
        "03_CUESTIONARIO_SATISFACCION_A": lambda doc: _cuerpo_cuestionario_a(
            doc, version=version),
        "04_MODULO_COMPLEMENTARIO_B_POST": lambda doc: _cuerpo_modulo_b(
            doc, version=version),
    }
    documentos: List[Dict[str, Any]] = []
    renders: List[str] = []

    for clave, rotulo, pie, titulo_doc in _REDISENO_REGISTRO:
        doc = documento_rediseno(titulo_doc)
        cabecera(doc.sections[0], rotulo, pie)
        constructores[clave](doc)
        ruta_docx = destino / f"{clave}.docx"
        _guardar(doc, ruta_docx)
        ruta_pdf = destino / f"{clave}.pdf"
        if con_pdf:
            _exportar(ruta_docx, ruta_pdf)
            control = _control_rediseno(ruta_docx, ruta_pdf)
            if v02:
                control["cabecera_institucional"] = _control_cabecera_nativa(
                    ruta_docx, ruta_pdf)
            if con_render:
                renders.extend(quir.renderizar_paginas_pdf(
                    ruta_pdf, list(range(1, control["paginas"] + 1)), dpi=120,
                    salida_dir=render_dir)["renderizadas"])
            documentos.append(control)

    # Documento reunido: mismas páginas, sin portada vacía, secciones desvinculadas.
    reunido = documento_rediseno("Instrumentos de recolección SIVAC")
    cabecera(reunido.sections[0], _REDISENO_REGISTRO[0][1],
             _REDISENO_REGISTRO[0][2])
    _cuerpo_ficha01(reunido, con_salto=True, version=version)
    for indice, constructor in ((1, lambda d: _cuerpo_ficha02(d, version=version)),
                                (2, lambda d: _cuerpo_cuestionario_a(
                                    d, version=version)),
                                (3, lambda d: _cuerpo_modulo_b(
                                    d, version=version))):
        seccion = reunido.add_section(WD_SECTION.NEW_PAGE)
        seccion.header.is_linked_to_previous = False
        seccion.footer.is_linked_to_previous = False
        cabecera(seccion, _REDISENO_REGISTRO[indice][1],
                 _REDISENO_REGISTRO[indice][2])
        constructor(reunido)
    ruta_docx = destino / "00_INSTRUMENTOS_RECOLECCION_SIVAC.docx"
    _guardar(reunido, ruta_docx)
    ruta_pdf = destino / "00_INSTRUMENTOS_RECOLECCION_SIVAC.pdf"
    if con_pdf:
        _exportar(ruta_docx, ruta_pdf)
        control = _control_rediseno(ruta_docx, ruta_pdf)
        if v02:
            control["cabecera_institucional"] = _control_cabecera_nativa(
                ruta_docx, ruta_pdf)
        if con_render:
            renders.extend(quir.renderizar_paginas_pdf(
                ruta_pdf, list(range(1, control["paginas"] + 1)), dpi=120,
                salida_dir=render_dir)["renderizadas"])
        documentos.append(control)

    # Apoyos del investigador en un solo documento.
    apoyos = documento_rediseno("Apoyos del investigador")
    cabecera(apoyos.sections[0], "APOYOS DEL INVESTIGADOR · SIVAC",
             "Apoyos del investigador · Código TRAB-______")
    _apoyos_instrucciones(apoyos)
    for titulo, constructor in (
        ("APOYOS DEL INVESTIGADOR · HOJA DE CIERRE", _apoyos_cierre),
        ("APOYOS DEL INVESTIGADOR · CONTINUACIÓN RSD",
         lambda d: _continuacion_rsd(d, version=version)),
        ("APOYOS DEL INVESTIGADOR · CONTINUACIÓN CPE", _continuacion_cpe),
        ("APOYOS DEL INVESTIGADOR · CONTINUACIÓN INCIDENCIAS",
         _continuacion_incidencias),
    ):
        _salto(apoyos)
        titulo_parrafo = apoyos.add_paragraph()
        titulo_parrafo.paragraph_format.space_after = Pt(0)
        titulo_parrafo.paragraph_format.line_spacing = Pt(1)
        constructor(apoyos)
    ruta_docx = apoyos_dir / "05_APOYOS_INVESTIGADOR_INSTRUCCIONES_CIERRE_CONTINUACIONES.docx"
    _guardar(apoyos, ruta_docx)
    ruta_pdf = apoyos_dir / "05_APOYOS_INVESTIGADOR_INSTRUCCIONES_CIERRE_CONTINUACIONES.pdf"
    if con_pdf:
        _exportar(ruta_docx, ruta_pdf)
        control = _control_rediseno(ruta_docx, ruta_pdf)
        if v02:
            control["cabecera_institucional"] = _control_cabecera_nativa(
                ruta_docx, ruta_pdf)
        if con_render:
            renders.extend(quir.renderizar_paginas_pdf(
                ruta_pdf, list(range(1, control["paginas"] + 1)), dpi=120,
                salida_dir=render_dir)["renderizadas"])
        documentos.append(control)

    # Igualdad literal de los dieciséis reactivos con el modelo rector.
    fuente = extraer_reactivos()
    esperado = {r["codigo"]: r["texto"] for grupo in fuente.values() for r in grupo}
    observado: Dict[str, str] = {}
    for clave in ("03_CUESTIONARIO_SATISFACCION_A",
                  "04_MODULO_COMPLEMENTARIO_B_POST",
                  "00_INSTRUMENTOS_RECOLECCION_SIVAC"):
        ruta = REDISENO / f"{clave}.docx"
        if ruta.exists():
            observado.update(_reactivos_en_docx(ruta))
    igualdad = {
        codigo: {
            "igual": observado.get(codigo) == texto,
            "longitud_fuente": len(texto),
            "longitud_salida": len(observado.get(codigo, "")),
        }
        for codigo, texto in esperado.items()
    }
    control_por_clave = {Path(d["docx"]).stem: d for d in documentos}
    control_a = control_por_clave.get("03_CUESTIONARIO_SATISFACCION_A", {})
    control_b = control_por_clave.get("04_MODULO_COMPLEMENTARIO_B_POST", {})

    manifiesto = {
        "meta": {
            "fecha": "2026-10-22",
            "agente": "maquetador-docx",
            "fase": "F8",
            "squad": "Squad E (Redacción y Maquetación)",
            "version": version,
            "destino": str(destino),
            "modo": "rediseno editorial aislado; no sustituye el paquete de catorce",
            "fuente_reactivos": str(MODELO_RECTOR),
            "regla_extraccion": "tablas identificadas por código AP/UP en 14 y PU/PE en 15; sin retranscripción manual",
        },
        "fuentes_preservadas_sha256": {
            "referencias/modelos_tesis/Fany_Tesis_Bachiller_2024.pdf":
                seguridad.sha256_archivo(RAIZ / "referencias" / "modelos_tesis"
                                         / "Fany_Tesis_Bachiller_2024.pdf"),
            "salidas/evidencias/instrumentos_aplicados/EXPEDIENTE_VALIDACION_JUICIO_EXPERTOS_MODELO_FANY.docx":
                seguridad.sha256_archivo(MODELO_RECTOR),
            "salidas/instrumentos/PAQUETE_CAMPO_14_20261022/_MANIFIESTO_EMISION.json":
                seguridad.sha256_archivo(DESTINO / "_MANIFIESTO_EMISION.json"),
            "salidas/documentos/informe_final_v19.docx":
                seguridad.sha256_archivo(RAIZ / "salidas" / "documentos"
                                         / "informe_final_v19.docx"),
        },
        "documentos": documentos,
        "reactivos": {
            "total_esperado": len(esperado),
            "igualdad_completa": all(v["igual"] for v in igualdad.values()),
            "detalle": igualdad,
        },
        "pruebas_rd05": {
            "A_campos_completos": all(
                control_a.get("campos_participante", {}).get(campo, False)
                for campo in _CAMPOS_PARTICIPANTE),
            "B_campos_completos": all(
                control_b.get("campos_participante", {}).get(campo, False)
                for campo in _CAMPOS_PARTICIPANTE),
            "A_observaciones_alto_cm": control_a.get("observaciones_alto_cm"),
            "B_observaciones_alto_cm": control_b.get("observaciones_alto_cm"),
            "A_una_pagina": control_a.get("paginas") == 1,
            "B_una_pagina": control_b.get("paginas") == 1,
            "B_fase_fija_final": "Fase" in _texto_pdf(Path(control_b["pdf"]))
                                  and "FINAL" in _texto_pdf(Path(control_b["pdf"])),
            "sin_codigos_trab_completos": all(
                not d.get("trab_con_numero") for d in documentos),
        },
        "correcciones_direccion": {
            "fecha_aplicacion": "2026-10-22",
            "aplicadas": [
                {"id": "RD-01", "estado": "aplicada",
                 "detalle": "Nota de continuación desde D-06 reubicada después de D-05 y antes de Entregas, en la página 2 de la Ficha 02."},
                {"id": "RD-02", "estado": "aplicada",
                 "detalle": "Identificación con TRAB, fase en blanco, centro y fecha en cierre y continuaciones; correlativo real sin reinicio."},
                {"id": "RD-03", "estado": "aplicada",
                 "detalle": "Presentación y confidencialidad con código en A y B, sin alterar reactivos, escalas ni una página por hoja."},
                {"id": "RD-04", "estado": "aplicada",
                 "detalle": "Cálculo del cierre en instrucciones narrativas, sin ecuaciones; regla CPE y nota de no sumar dosis conservadas."},
                {"id": "RD-05", "estado": "aplicada",
                 "detalle": "Restituidos código de centro e investigador en la cabecera de A y B, y recuadro opcional de observaciones al pie; B mantiene fase fija FINAL."},
            ],
        },
        "prevalencias_gobernanza": [
            "No se adopta ni imprime la atribución de un certificado único al Instrumento 03 como regla vigente. Las referencias del JSON del especialista a ese punto están superadas y son ajenas a este rediseño editorial.",
            "No se afirma que exista un anexo firmado remitido a expertos ni se describe un juicio inspeccionado. La fuente se denomina versión fuente preservada.",
            "La secuencia 04 es una decisión editorial de este rediseño, no una preferencia atribuida al tesista.",
            "Los campos nuevos de C-03 quedan excluidos: prevalece la fuente real emitida y no se agregan campos empíricos.",
            "Los cálculos se concentran en la hoja de cierre. No se emiten afirmaciones de estimabilidad psicométrica ni umbrales nuevos en documentos de uso.",
        ],
        "correspondencia_campos": [
            {"origen": "Encabezado Paquete TRAB-XX · Fase PRE/POST",
             "destino": "Cabecera de identificación con Fase en blanco (01, 02, 03) y rótulo fijo final (04)"},
            {"origen": "Código TRAB-XX y código de centro", "destino": "Cabecera de 01, 02, 03 y 04"},
            {"origen": "Fecha de aplicación", "destino": "Línea en blanco en la cabecera de las cuatro hojas"},
            {"origen": "Observador o investigador", "destino": "Cabecera y firma de la Ficha 01; campo Investigador en la cabecera de 03 y 04"},
            {"origen": "Tarea y descripción (tabla de ocho columnas)", "destino": "Título de cada bloque de tarea, con la descripción literal del constructor vigente"},
            {"origen": "Hora de inicio, hora de fin y duración", "destino": "Rejilla interna del bloque de tarea"},
            {"origen": "Pausa con causa", "destino": "Rejilla interna del bloque de tarea"},
            {"origen": "Tarea válida", "destino": "Rejilla interna del bloque de tarea"},
            {"origen": "Observaciones por tarea", "destino": "Rejilla interna del bloque de tarea"},
            {"origen": "Media, mediana y tareas válidas", "destino": "Consolidado de la página 2 de la Ficha 01"},
            {"origen": "Incidencias: número, hora, tarea, causa, acción y observaciones",
             "destino": "Tabla de incidencias de la Ficha 01 y continuación H-05"},
            {"origen": "Observaciones del observador y firma", "destino": "Cierre de la Ficha 01"},
            {"origen": "Horas de inicio y fin de la sesión", "destino": "Pie de la Ficha 01"},
            {"origen": "Ventana auditada y fecha de auditoría", "destino": "Cabecera de la Ficha 02"},
            {"origen": "Tabla RSD de trece columnas: número, tipo, fecha, C1 a C8, conforme y motivo",
             "destino": "Bloques D-01 a D-05 con rejilla de ocho criterios y veredicto; continuación D-06"},
            {"origen": "Criterios C1 a C8", "destino": "Leyenda completa una vez y etiqueta corta en cada bloque"},
            {"origen": "Tabla CPE: número, programada, entregada, diferencia, documento y concordante",
             "destino": "Tabla compacta de seis columnas en la Ficha 02 y continuación E-13"},
            {"origen": "Conteos de cierre y porcentajes", "destino": "Conteos crudos en la Ficha 02; porcentajes en la hoja de cierre"},
            {"origen": "Observaciones, firma y fecha de cierre del auditor", "destino": "Cierre de la Ficha 02"},
            {"origen": "Reactivos AP-01 a AP-04 y UP-01 a UP-04", "destino": "Tabla del Cuestionario A, extracción literal del rector"},
            {"origen": "Reactivos PU-01 a PU-04 y PE-01 a PE-04", "destino": "Tabla del Módulo B, extracción literal del rector"},
            {"origen": "Escala de 1 a 5", "destino": "Leyenda unificada de etiqueta y valor en 03 y 04"},
            {"origen": "Código de participante, código de centro, fase, fecha de aplicación e investigador",
             "destino": "Cabecera compacta del Cuestionario A y del Módulo B; en B la fase se imprime fija como FINAL"},
            {"origen": "Observaciones del participante", "destino": "Recuadro opcional al pie del Cuestionario A y del Módulo B, de 0.9 cm"},
            {"origen": "Puntajes, sumas y terciles teóricos", "destino": "Hoja de cierre y hoja de puntuación vigente del kit, sin duplicar baremos"},
            {"origen": "Consentimiento informado", "destino": "Soporte separado existente; no se reproduce"},
            {"origen": "Calibración, matriz de captura, manual y certificado de jueces", "destino": "Soportes separados existentes; no se reproducen"},
        ],
        "divergencias": [
            {"id": "C-03", "tema": "Campos de biológico, lote, dosis, vacuna, causa y vale o requerimiento",
             "decision": "Excluidos. Prevalece la fuente real emitida: el formulario vigente no los contiene y no se agregan campos empíricos.",
             "estado": "cerrado por prevalencia de la fuente emitida"},
            {"id": "D-01", "tema": "Geometría de Fany",
             "decision": "No se adopta Arial 11 ni el ancho de 17.01 cm. Se usa Times New Roman 12/10/9.5 y 8788 dxa.",
             "estado": "resuelto editorialmente"},
            {"id": "D-02", "tema": "Identificación de Fany",
             "decision": "Fany no recoge código de participante. SIVAC conserva TRAB en blanco para emparejar pretest y postest.",
             "estado": "resuelto editorialmente"},
            {"id": "D-03", "tema": "Tabla de trece columnas de la Ficha 02",
             "decision": "Sustituida por bloques verticales con los mismos campos crudos; no se pierde ningún criterio.",
             "estado": "resuelto editorialmente"},
            {"id": "D-04", "tema": "Casillas con corchetes literales",
             "decision": "Se eliminan; la rejilla dibuja la casilla vacía.",
             "estado": "resuelto editorialmente"},
            {"id": "D-05", "tema": "Capacidad de la ficha",
             "decision": "Cinco bloques RSD y doce entregas CPE en la hoja base; el excedente pasa a continuación correlativa entregada.",
             "estado": "resuelto editorialmente"},
            {"id": "C-02", "tema": "Modo de corpus",
             "decision": "El campo queda en blanco con tres opciones; no se fija tamaño.",
             "estado": "pendiente de aprobación"},
        ],
        "continuaciones_entregadas": [
            "RSD desde D-06",
            "CPE desde E-13",
            "Incidencias desde H-05",
        ],
        "render": renders,
        "pendientes": [
            "Revisión visual del tesista y de la asesora antes de imprimir.",
            "Definir el modo de corpus antes del pretest.",
        ],
    }
    if v02:
        controles_cabecera = {
            Path(d["docx"]).stem: d.get("cabecera_institucional", {})
            for d in documentos
        }
        manifiesto["cabecera_institucional"] = {
            "tabla_columnas_dxa": _ANCHOS_CABECERA,
            "columnas_laterales_iguales": _ANCHOS_CABECERA[0] == _ANCHOS_CABECERA[2],
            "alto_logo_cm": _ALTO_LOGO_CM,
            "distancia_cabecera_cm": _DISTANCIA_CABECERA_CM,
            "margen_superior_cm": 2.5,
            "lineas": list(_CABECERA_LINEAS),
            "logos": {
                "unajma_fuente": {
                    "ruta": str(LOGO_UNAJMA),
                    "sha256": seguridad.sha256_archivo(LOGO_UNAJMA),
                    "bytes": LOGO_UNAJMA.stat().st_size,
                },
                "unajma_derivado": {
                    "ruta": str(LOGO_UNAJMA_RECORTE),
                    "sha256": seguridad.sha256_archivo(LOGO_UNAJMA_RECORTE),
                    "bytes": LOGO_UNAJMA_RECORTE.stat().st_size,
                    "recorte_px": [348, 154, 1707, 1914],
                    "criterio": "solo margen blanco y marco azul externo; escudo, símbolos y texto intactos",
                },
                "epis": {
                    "ruta": str(LOGO_EPIS),
                    "sha256": seguridad.sha256_archivo(LOGO_EPIS),
                    "bytes": LOGO_EPIS.stat().st_size,
                },
            },
            "auditoria_por_documento": controles_cabecera,
        }
        manifiesto["cambios_v02"] = [
            {"id": "V02-01", "estado": "aplicada",
             "detalle": "Cabecera institucional nativa de tres columnas sin bordes en todas las páginas y en las cuatro secciones del documento reunido; logos DrawingML inline, nunca anclados."},
            {"id": "V02-02", "estado": "aplicada",
             "detalle": "Logotipo UNAJMA derivado con recorte de margen y marco externo; EPIS original. Altura visual común de 1.2 cm, sin deformación."},
            {"id": "V02-03", "estado": "aplicada",
             "detalle": "Línea de control con rótulo del formulario a la izquierda y PAGE/NUMPAGES arriba a la derecha, con regla fina de separación."},
            {"id": "V02-04", "estado": "aplicada",
             "detalle": "Rol y momento de aplicación en el cuerpo inicial de 01 a 04: observador, auditor o participante; sin fechas ni aplicación atribuida. En B se retiró el rótulo duplicado de aplicación."},
            {"id": "V02-05", "estado": "aplicada",
             "detalle": "Campos de identificación marcados como administrativos en A y B; el investigador no se presenta como pregunta al participante."},
            {"id": "V02-06", "estado": "aplicada",
             "detalle": "Bloques D rotulados como bloque de auditoría y campo separado para el número del documento revisado; códigos fuente intactos."},
            {"id": "V02-07", "estado": "aplicada",
             "detalle": "Instrucciones del participante limitadas a marcar de 1 a 5 y confidencialidad; notas de puntaje o imputación retiradas de las hojas del participante."},
        ]
        manifiesto["pruebas_v02"] = {
            "cabecera_en_todas_las_paginas": all(
                c.get("todas_las_paginas_con_dos_logos")
                and c.get("todas_las_paginas_sin_solape")
                and c.get("todas_las_paginas_sin_empuje")
                for c in controles_cabecera.values()),
            "altura_visual_uniforme": all(
                c.get("altura_visual_uniforme")
                for c in controles_cabecera.values()),
            "simetria_lateral": all(
                c.get("simetria_lateral")
                for c in controles_cabecera.values()),
            "secciones_desvinculadas": all(
                c.get("secciones_desvinculadas")
                for c in controles_cabecera.values()),
            "imagenes_solo_inline": all(
                c.get("imagenes_solo_inline")
                for c in controles_cabecera.values()),
            "campos_nativos_page_numpages": all(
                c.get("campos_nativos")
                for c in controles_cabecera.values()),
            "A_una_pagina": control_a.get("paginas") == 1,
            "B_una_pagina": control_b.get("paginas") == 1,
            "A_campos_completos": all(
                control_a.get("campos_participante", {}).get(campo, False)
                for campo in _CAMPOS_PARTICIPANTE),
            "B_campos_completos": all(
                control_b.get("campos_participante", {}).get(campo, False)
                for campo in _CAMPOS_PARTICIPANTE),
            "reactivos_16_iguales": all(v["igual"] for v in igualdad.values()),
        }
        manifiesto["instrucciones_participante_v02"] = {
            "A": [
                "Marque con una X una sola casilla por enunciado.",
                "La escala va de 1 a 5: 1 es totalmente en desacuerdo y 5 es totalmente de acuerdo.",
                "No escriba su nombre, apellido ni documento de identidad. Use solo el código que le entregue el investigador.",
            ],
            "B": [
                "Este módulo se aplica solo al final, después de haber usado SIVAC.",
                "Marque con una X una sola casilla por enunciado, de 1 a 5.",
                "No escriba su nombre, apellido ni documento de identidad. Use solo el código que le entregue el investigador.",
            ],
            "nota": "Las reglas de puntaje, imputación o suma se concentran en la hoja de cierre de los apoyos del investigador.",
        }
    ruta_manifiesto = destino / "MANIFIESTO.json"
    ruta_manifiesto.write_text(
        json.dumps(manifiesto, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifiesto


def _tabla_incidencias_limpia(doc, desde: int, filas_datos: int) -> Any:
    filas = [["N.º", "Tarea o documento, fase y fecha", "Hora", "Causa",
              "Acción", "Observaciones"]]
    for numero in range(desde, desde + filas_datos):
        filas.append([str(numero), "", "__:__", "", "", ""])
    t = _tabla_limpia(
        doc, [650, 3088, 900, 1600, 1100, 1450], filas, tam=10,
        tam_cabecera=9.5, alto_min_cm=0.9,
        alineaciones=["center", "left", "center", "left", "left", "left"])
    _negrita_fila(t, 0, tam=9.5)
    return t


def _continuacion_rsd_limpia(doc) -> None:
    _h1_limpio(doc, "Continuación. Registro documental")
    _identificacion_limpia(doc, [
        ["Código", "TRAB-______", "Fase",
         "________________ (INICIAL o FINAL)"],
        ["Código de centro", "________________", "Fecha",
         "____/____/______"],
    ])
    _seccion_limpia(doc, "Documentos 5 y 6")
    _matriz_documentos_limpia(doc, [5, 6])
    _nota_limpia(doc, "Continúe el correlativo real de los documentos "
                      "auditados; no reinicie la numeración.", antes=2,
                 despues=0)


def _continuacion_cpe_limpia(doc) -> None:
    _h1_limpio(doc, "Continuación. Entregas")
    _identificacion_limpia(doc, [
        ["Código", "TRAB-______", "Fase",
         "________________ (INICIAL o FINAL)"],
        ["Código de centro", "________________", "Fecha",
         "____/____/______"],
    ])
    _tabla_cpe_limpia(doc, 13, 12)
    _seccion_limpia(doc, "Continuación. Registro de incidencias", antes=7)
    _tabla_incidencias_limpia(doc, 5, 8)


def _continuacion_incidencias_limpia(doc) -> None:
    _h1_limpio(doc, "Continuación. Registro de incidencias")
    _identificacion_limpia(doc, [
        ["Código", "TRAB-______", "Fase",
         "________________ (INICIAL o FINAL)"],
        ["Código de centro", "________________", "Fecha",
         "____/____/______"],
    ])
    _tabla_incidencias_limpia(doc, 5, 8)
    _nota_limpia(doc, "Cada fila enlaza el identificador, la fase y la tarea o "
                      "documento; si afecta un documento, anote su número o "
                      "serie. Causa: interrupción externa, desviación o ayuda "
                      "del investigador.", antes=3, despues=0)


def _control_limpio(docx_path: Path, pdf_path: Path,
                    render_dir: Path, con_render: bool) -> Dict[str, Any]:
    control = _control_rediseno(docx_path, pdf_path)
    control["cabecera_institucional"] = _control_cabecera_nativa(
        docx_path, pdf_path)
    if con_render:
        control["render"] = quir.renderizar_paginas_pdf(
            pdf_path, list(range(1, control["paginas"] + 1)), dpi=120,
            salida_dir=render_dir)["renderizadas"]
    return control


def _reporte_marcado(manifiesto: Dict[str, Any], destino: Path,
                     *, publicado: bool) -> Path:
    pruebas = manifiesto.get("pruebas_limpieza", {})
    documentos = [{
        "docx": d.get("docx"),
        "pdf": d.get("pdf"),
        "paginas": d.get("paginas"),
        "sha256_docx": d.get("sha256_docx"),
        "sha256_pdf": d.get("sha256_pdf"),
        "ancho_max_dxa": d.get("ancho_max_dxa"),
        "dos_logos": d.get("cabecera_institucional", {}).get(
            "todas_las_paginas_con_dos_logos"),
    } for d in manifiesto.get("documentos", [])]
    reporte = {
        "meta": {
            "fecha": "2026-10-22",
            "agente": "maquetador-docx",
            "fase": "F8_INTEGRACION_EDITORIAL",
            "squad": "Squad E",
            "version": "v02-marcado-claro",
            "estado": ("publicado en v02 vigente" if publicado
                       else "candidato en staging, pendiente de publicar"),
            "destino": str(destino),
        },
        "resumen": {
            "paginas_por_documento": pruebas.get("paginas_por_documento"),
            "reactivos_16_iguales": pruebas.get("reactivos_16_iguales"),
            "control_marcado": {
                "sin_glifos_checkbox": pruebas.get(
                    "sin_glifos_checkbox_o_corchetes"),
                "sin_codigos_protocolo_visibles": pruebas.get(
                    "sin_codigos_protocolo_visibles"),
                "etiquetas_por_nombre": pruebas.get("etiquetas_por_nombre"),
            },
        },
        "documentos": documentos,
        "controles": pruebas,
        "mapa_interno": manifiesto.get("mapa_interno"),
        "antes_despues": [
            {"antes": "C1 a C8 y Sí □ No □ en ocho columnas",
             "despues": "Ocho aspectos nombrados; Sí/No en celdas vacías para dos documentos por página"},
            {"antes": "Pausa y Válida con □ Sí / □ No en una celda",
             "despues": "Dos columnas Sí/No con celdas vacías; tareas visibles 1 a 6"},
            {"antes": "Entregas E-01 a E-12 con Sí □ No □",
             "despues": "Entregas 1 a 12 con columnas Concordancia Sí/No vacías"},
            {"antes": "Reactivos AP-01/UP-01/PU-01/PE-01",
             "despues": "Reactivos numerados 1 a 8, bandas con nombre y códigos solo en el mapa interno"},
        ],
        "bordes_vacios": {
            "celdas_respuesta": "vacías, sin caracteres ni controles",
            "ancho_minimo_respuesta_dxa": 620,
            "alto_minimo_fila_cm": 0.9,
        },
        "nota_alcance": ("Corrección de marcado y etiquetas visibles; no cambia "
                         "reactivos, dimensiones ni reglas. QG-5 abierta."),
    }
    ruta = (RAIZ / "salidas" / "reportes_maquetacion"
            / "marcado_claro_v02_20261022.json")
    ruta.write_text(json.dumps(reporte, indent=2, ensure_ascii=False),
                    encoding="utf-8")
    return ruta


def _reporte_limpieza(manifiesto: Dict[str, Any], destino: Path,
                      *, publicado: bool) -> Path:
    pruebas = manifiesto.get("pruebas_limpieza", {})
    documentos = []
    for doc in manifiesto.get("documentos", []):
        documentos.append({
            "docx": doc.get("docx"),
            "pdf": doc.get("pdf"),
            "paginas": doc.get("paginas"),
            "sha256_docx": doc.get("sha256_docx"),
            "sha256_pdf": doc.get("sha256_pdf"),
            "desborde_inferior_pt": doc.get("desborde_inferior_pt"),
            "ancho_max_dxa": doc.get("ancho_max_dxa"),
            "dos_logos": doc.get("cabecera_institucional", {}).get(
                "todas_las_paginas_con_dos_logos"),
        })
    reporte = {
        "meta": {
            "fecha": "2026-10-22",
            "agente": "maquetador-docx",
            "fase": "F8_INTEGRACION_EDITORIAL",
            "squad": "Squad E",
            "version": "v02-limpieza",
            "estado": ("publicado en v02 vigente" if publicado
                       else "candidato en staging, pendiente de publicar"),
            "destino": str(destino),
            "criterios": [
                "criterios_jurado_limpieza_instrumentos_20261022.json",
                "criterios_metodologicos_limpieza_instrumentos_20261022.json",
            ],
            "prevalencias_direccion": [
                "Fase administrativa visible para emparejar pre y post; sin explicación de hipótesis.",
                "H1 de 12 pt, no 16 pt; sin rótulo FORMULARIO en el cuerpo.",
                "Sin campo biológico nuevo ni límite ciego 7+5; páginas medidas por contenido.",
                "Sin rótulos de validado, V, IVC ni sellos; QG-5 abierta.",
            ],
        },
        "resumen": {
            "paginas_instrumentos": pruebas.get("total_instrumentos"),
            "paginas_apoyos": pruebas.get("paginas_por_documento", {}).get(
                "05_APOYOS_INVESTIGADOR_INSTRUCCIONES_CIERRE_CONTINUACIONES"),
            "paginas_por_documento": pruebas.get("paginas_por_documento"),
            "reactivos_16_iguales": pruebas.get("reactivos_16_iguales"),
            "A_una_pagina": pruebas.get("A_una_pagina"),
            "B_una_pagina": pruebas.get("B_una_pagina"),
            "F01_dos_tablas": pruebas.get("F01_dos_tablas_tiempo"),
            "F02_bloques_en_hoja": "D-01 a D-04; D-05 a D-07 en continuación",
        },
        "documentos": documentos,
        "controles": pruebas,
        "protocolo_validacion": manifiesto.get("protocolo_validacion"),
        "mapa_campos": manifiesto.get("mapa_campos"),
        "cambios_limpieza": manifiesto.get("cambios_limpieza"),
        "preservacion": manifiesto.get("fuentes_preservadas_sha256"),
        "nota_alcance": ("Edición de composición y rotulados; no acredita validación "
                         "de contenido ni cierra QG-5. Los 16 reactivos y las "
                         "unidades se conservan literales."),
    }
    ruta = (RAIZ / "salidas" / "reportes_maquetacion"
            / "limpieza_profesional_v02_20261022.json")
    ruta.write_text(json.dumps(reporte, indent=2, ensure_ascii=False),
                    encoding="utf-8")
    return ruta


def construir_limpieza_fany(destino: Optional[Path] = None,
                            con_pdf: bool = True,
                            con_render: bool = True,
                            solo_reexportar: Optional[Sequence[str]] = None
                            ) -> Dict[str, Any]:
    """Emite la limpieza profesional en staging o publica en v02.

    No toca v01, el respaldo ni los maestros. Reutiliza el constructor, el
    motor de tablas y la cabecera nativa; solo cambia la composición.
    ``solo_reexportar`` permite corregir B, el conjunto y los apoyos sin
    volver a exportar 01, 02 ni A.
    """
    destino = Path(destino) if destino else CANDIDATO_LIMPIEZA
    render_dir = destino / "control_visual"
    apoyos_dir = destino / "APOYOS_INVESTIGADOR"
    destino.mkdir(parents=True, exist_ok=True)
    apoyos_dir.mkdir(parents=True, exist_ok=True)
    render_dir.mkdir(parents=True, exist_ok=True)
    _preparar_logo_unajma()
    previo = None
    if solo_reexportar is not None:
        ruta_previa = destino / "MANIFIESTO.json"
        if not ruta_previa.exists():
            raise FileNotFoundError(
                "La reemisión selectiva requiere el manifiesto del candidato")
        previo = json.loads(ruta_previa.read_text(encoding="utf-8"))

    constructores = (
        ("01_FICHA_TIEMPOS", _cuerpo_ficha01_limpio, _LIMPIEZA_FOOTERS[0],
         "Instrumento 1. Ficha de observación de tiempos"),
        ("02_FICHA_AUDITORIA_DOCUMENTAL", _cuerpo_ficha02_limpio,
         _LIMPIEZA_FOOTERS[1],
         "Instrumento 2. Ficha de auditoría documental"),
        ("03_CUESTIONARIO_SATISFACCION_A", _cuerpo_cuestionario_a_limpio,
         _LIMPIEZA_FOOTERS[2],
         "Instrumento 3. Cuestionario A. Satisfacción del usuario"),
        ("04_MODULO_COMPLEMENTARIO_B_POST", _cuerpo_modulo_b_limpio,
         _LIMPIEZA_FOOTERS[3],
         "Módulo B. Cuestionario complementario del Instrumento 3"),
    )
    documentos: List[Dict[str, Any]] = []
    for clave, constructor, pie, titulo_doc in constructores:
        if solo_reexportar is not None and clave not in solo_reexportar:
            continue
        doc = documento_rediseno(titulo_doc)
        _cabecera_limpia(doc.sections[0], pie)
        constructor(doc)
        _pulir_tablas(doc)
        ruta_docx = destino / f"{clave}.docx"
        _guardar(doc, ruta_docx)
        ruta_pdf = destino / f"{clave}.pdf"
        if con_pdf:
            _exportar(ruta_docx, ruta_pdf)
            documentos.append(_control_limpio(ruta_docx, ruta_pdf,
                                              render_dir, con_render))

    if solo_reexportar is None or "CONJUNTO_00" in solo_reexportar:
        reunido = documento_rediseno("Instrumentos de recolección SIVAC")
        _cabecera_limpia(reunido.sections[0], _LIMPIEZA_FOOTERS[0])
        _cuerpo_ficha01_limpio(reunido)
        for indice, constructor in enumerate((
                _cuerpo_ficha02_limpio, _cuerpo_cuestionario_a_limpio,
                _cuerpo_modulo_b_limpio), 1):
            seccion = reunido.add_section(WD_SECTION.NEW_PAGE)
            seccion.header.is_linked_to_previous = False
            seccion.footer.is_linked_to_previous = False
            _cabecera_limpia(seccion, _LIMPIEZA_FOOTERS[indice])
            constructor(reunido)
        _pulir_tablas(reunido)
        ruta_docx = destino / "00_INSTRUMENTOS_RECOLECCION_SIVAC.docx"
        _guardar(reunido, ruta_docx)
        ruta_pdf = destino / "00_INSTRUMENTOS_RECOLECCION_SIVAC.pdf"
        if con_pdf:
            _exportar(ruta_docx, ruta_pdf)
            documentos.append(_control_limpio(ruta_docx, ruta_pdf, render_dir,
                                              con_render))

    if solo_reexportar is None or "APOYOS" in solo_reexportar:
        apoyos = documento_rediseno("Apoyos del investigador")
        _cabecera_limpia(apoyos.sections[0], _LIMPIEZA_FOOTERS[4])
        _apoyos_protocolo(apoyos)
        for constructor in (_apoyos_criterios, _apoyos_cierre,
                            _continuacion_rsd_limpia, _continuacion_cpe_limpia):
            _salto(apoyos)
            constructor(apoyos)
        _pulir_tablas(apoyos)
        ruta_docx = apoyos_dir / "05_APOYOS_INVESTIGADOR_INSTRUCCIONES_CIERRE_CONTINUACIONES.docx"
        _guardar(apoyos, ruta_docx)
        ruta_pdf = apoyos_dir / "05_APOYOS_INVESTIGADOR_INSTRUCCIONES_CIERRE_CONTINUACIONES.pdf"
        if con_pdf:
            _exportar(ruta_docx, ruta_pdf)
            documentos.append(_control_limpio(ruta_docx, ruta_pdf, render_dir,
                                              con_render))

    if solo_reexportar is not None:
        reutilizados = {
            Path(d["docx"]).stem: d for d in previo.get("documentos", [])
        }
        construidos = {Path(d["docx"]).stem for d in documentos}
        for clave, control in reutilizados.items():
            if clave not in construidos:
                documentos.append(control)
        orden = [clave for clave, *_ in constructores]
        orden += ["00_INSTRUMENTOS_RECOLECCION_SIVAC",
                  "05_APOYOS_INVESTIGADOR_INSTRUCCIONES_CIERRE_CONTINUACIONES"]
        documentos.sort(
            key=lambda d: orden.index(Path(d["docx"]).stem)
            if Path(d["docx"]).stem in orden else len(orden))
        vigentes = {
            Path(ruta).name for d in documentos for ruta in d.get("render", [])
        }
        for png in render_dir.glob("*.png"):
            if png.name not in vigentes:
                png.unlink()

    fuente = extraer_reactivos()
    observado = {
        "A": _reactivos_ordenados_en_docx(
            destino / "03_CUESTIONARIO_SATISFACCION_A.docx"),
        "B": _reactivos_ordenados_en_docx(
            destino / "04_MODULO_COMPLEMENTARIO_B_POST.docx"),
    }
    igualdad: Dict[str, Dict[str, Any]] = {}
    for grupo, reactivos in fuente.items():
        for indice, reactivo in enumerate(reactivos):
            texto = re.sub(r"\s+", " ", reactivo["texto"]).strip()
            salida = observado[grupo][indice] if indice < len(observado[grupo]) else ""
            igualdad[reactivo["codigo"]] = {
                "igual": salida == texto,
                "longitud_fuente": len(texto),
                "longitud_salida": len(salida),
            }
    por_clave = {Path(d["docx"]).stem: d for d in documentos}
    reunido_control = por_clave["00_INSTRUMENTOS_RECOLECCION_SIVAC"]
    a_control = por_clave["03_CUESTIONARIO_SATISFACCION_A"]
    b_control = por_clave["04_MODULO_COMPLEMENTARIO_B_POST"]
    cabeceras = {k: d.get("cabecera_institucional", {})
                 for k, d in por_clave.items()}
    marcado = destino == CANDIDATO_MARCADO
    es_candidato = destino in (CANDIDATO_LIMPIEZA, CANDIDATO_MARCADO)
    respaldo = (RAIZ / "salidas" / "archivo"
                / ("INSTRUMENTOS_V02_ANTES_MARCADO_CLARO_20261022" if marcado
                   else "INSTRUMENTOS_V02_ANTES_LIMPIEZA_20261022"))
    manifiesto = {
        "meta": {
            "fecha": "2026-10-22",
            "agente": "maquetador-docx",
            "fase": "F8",
            "squad": "Squad E",
            "version": "v02-marcado-claro" if marcado else "v02-limpieza",
            "destino": str(destino),
            "modo": ("candidato aislado previo a publicación"
                     if es_candidato else "publicado en v02"),
            "origen_respaldo": str(respaldo),
        },
        "fuentes_preservadas_sha256": {
            "respaldo_manifest": seguridad.sha256_archivo(
                RAIZ / "salidas" / "archivo"
                / "INSTRUMENTOS_V02_ANTES_LIMPIEZA_20261022" / "MANIFIESTO.json"),
            "builder": seguridad.sha256_archivo(
                RAIZ / "scripts" / "compiladores" / "paquete_campo_builder.py"),
            "motor": seguridad.sha256_archivo(
                RAIZ / "scripts" / "utilidades" / "docx_quirurgico.py"),
            "logo_unajma": seguridad.sha256_archivo(LOGO_UNAJMA),
            "logo_epis": seguridad.sha256_archivo(LOGO_EPIS),
            "informe_final_v19": seguridad.sha256_archivo(
                RAIZ / "salidas" / "documentos" / "informe_final_v19.docx"),
        },
        "documentos": documentos,
        "reactivos": {
            "total_esperado": sum(len(grupo) for grupo in fuente.values()),
            "igualdad_completa": all(v["igual"] for v in igualdad.values()),
            "detalle": igualdad,
        },
        "mapa_campos": [
            {"origen": "F01: seis bloques verticales de tres filas",
             "destino": "Dos tablas de tres tareas: Tarea, Inicio, Fin, Tiempo, Pausa, Válida"},
            {"origen": "F01: causa de pausa y observaciones por tarea",
             "destino": "Tabla H-01 a H-04 del apoyo y continuación H-05"},
            {"origen": "F01: consolidado de media, mediana y tareas válidas",
             "destino": "Hoja de cierre del investigador"},
            {"origen": "F01: tabla de incidencias en la hoja de campo",
             "destino": "Apoyo, continuación H-05 a H-12"},
            {"origen": "F01: seis instrucciones y conversión decimal",
             "destino": "Tres instrucciones en la hoja; protocolo completo y conversión en apoyo"},
            {"origen": "F02: tabla completa C1-C8 y reglas duplicadas",
             "destino": "Apoyo, criterios C1-C8 una sola vez y regla de concordancia"},
            {"origen": "F02: bloques D-01 a D-05 y rejilla de ocho criterios",
             "destino": "Bloques D-01 a D-04 en la hoja; D-05 a D-07 en continuación"},
            {"origen": "F02: conteos crudos en la hoja",
             "destino": "Hoja de cierre del investigador, tabla de conteo crudo"},
            {"origen": "A/B: Investigador (admin.) y observaciones opcionales",
             "destino": "Apoyo, Control de aplicación y observaciones"},
            {"origen": "Pie con segundo campo TRAB escribible",
             "destino": "Pie de identificación breve; TRAB solo en la cabecera administrativa"},
        ],
        "mapa_interno": _mapa_interno(),
        "cambios_limpieza": [
            {"id": "L01", "detalle": "H1 única de 12 pt; se retiró el rótulo FORMULARIO de la cabecera y el subtítulo cursivo."},
            {"id": "L02", "detalle": "Cabecera solo con institución, logos y paginación; pie con ID breve sin campos escribibles."},
            {"id": "L03", "detalle": "Ritmo 12/6 pt en H1, 10 pt antes de sección y separación entre tablas."},
            {"id": "L04", "detalle": "F01 con dos tablas de tres tareas y seis columnas; pausa y validez con casillas."},
            {"id": "L05", "detalle": "F02 con bloques D-01 a D-04, rejilla C1-C8 en una línea, CPE de seis columnas y D-05 en apoyo."},
            {"id": "L06", "detalle": "A/B con una H1, dos instrucciones, anclajes una vez y columnas Likert de 9 mm."},
            {"id": "L07", "detalle": "Apoyos con protocolo, criterios, control administrativo, cierre y continuaciones."},
        ],
        "pruebas_limpieza": {
            "paginas_por_documento": {k: d["paginas"] for k, d in por_clave.items()},
            "total_instrumentos": reunido_control["paginas"],
            "A_una_pagina": a_control["paginas"] == 1,
            "B_una_pagina": b_control["paginas"] == 1,
            "reactivos_16_iguales": all(v["igual"] for v in igualdad.values()),
            "dos_logos_todas_las_paginas": all(
                c.get("todas_las_paginas_con_dos_logos") for c in cabeceras.values()),
            "sin_formulario_en_cabecera": all(
                not any(p.get("rotulo_en_cabecera") for p in c.get("paginas", []))
                for c in cabeceras.values()),
            "paginacion_en_todas_las_paginas": all(
                all(p.get("paginacion_en_cabecera") for p in c.get("paginas", []))
                for c in cabeceras.values()),
            "secciones_desvinculadas": all(
                c.get("secciones_desvinculadas") for c in cabeceras.values()),
            "imagenes_solo_inline": all(
                c.get("imagenes_solo_inline") for c in cabeceras.values()),
            "sin_desborde_inferior": all(
                d["desborde_inferior_pt"] == 0 for d in documentos),
            "ancho_maximo_dxa": max(d["ancho_max_dxa"] for d in documentos),
            "fuente_minima_pt": min(d["fuente_minima_pt"] for d in documentos),
            "sin_tokens_prohibidos": all(
                not d["tokens_prohibidos"] for d in documentos),
        },
        "render": [r for d in documentos for r in d.get("render", [])],
        "pendientes": [
            "Revisión visual del candidato por el Director antes de publicar en v02.",
            "Confirmar que el tesista abra la carpeta v02 publicada, no el respaldo.",
        ],
    }
    manifiesto["pruebas_limpieza"].update(_pruebas_por_frase(documentos))
    f01 = por_clave["01_FICHA_TIEMPOS"]
    manifiesto["pruebas_limpieza"]["F01_dos_tablas_tiempo"] = (
        sum(1 for t in _tablas_docx(Path(f01["docx"]))
            if t["columnas"] == 8) == 2)
    manifiesto["protocolo_validacion"] = [
        {"documento": "01_FICHA_TIEMPOS",
         "frase": ("Criterios de inicio, fin, pausa y validez: sección "
                   "Protocolo del observador de los apoyos. Incidencias: "
                   "H-01 y siguientes."),
         "constatacion": "remisión final separa protocolo de registro; no "
                         "atribuye el protocolo a H-01 a H-04"},
        {"documento": "02_FICHA_AUDITORIA_DOCUMENTAL",
         "frase": ("Para más entregas, continúe desde E-13 en Continuación. "
                   "Entregas de los apoyos, manteniendo el correlativo real."),
         "constatacion": "remisión bajo E-12 en la tercera página"},
        {"documento": "03_CUESTIONARIO_SATISFACCION_A / 04_MODULO_COMPLEMENTARIO_B_POST",
         "frase": "No hay respuestas correctas ni incorrectas",
         "constatacion": "neutralidad de fuente en A y B, una sola página"},
        {"documento": "04_MODULO_COMPLEMENTARIO_B_POST",
         "frase": "Módulo B. Cuestionario complementario del Instrumento 3",
         "constatacion": "presente en cuerpo y pie; ausencia literal de "
                         "'Instrumento 4'"},
        {"documento": "00_INSTRUMENTOS_RECOLECCION_SIVAC",
         "frase": "Módulo B. Cuestionario complementario del Instrumento 3",
         "constatacion": "presente en el conjunto; ausencia literal de "
                         "'Instrumento 4'"},
        {"documento": "05_APOYOS_INVESTIGADOR_INSTRUCCIONES_CIERRE_CONTINUACIONES",
         "frase": ("El tiempo de emisión inicia al recibir o abrir la "
                   "solicitud y termina cuando el vale queda generado, "
                   "firmado o impreso con numeración oficial."),
         "constatacion": "frase literal presente en el protocolo"},
        {"documento": "05_APOYOS_INVESTIGADOR_INSTRUCCIONES_CIERRE_CONTINUACIONES",
         "frase": ("Causa: interrupción externa, desviación del protocolo o "
                   "ayuda sustantiva del investigador. Acción: pausa, "
                   "anulación o repetición."),
         "constatacion": "causas y acciones presentes en la nota de H-01 a H-04"},
        {"documento": "05_APOYOS_INVESTIGADOR_INSTRUCCIONES_CIERRE_CONTINUACIONES",
         "frase": ("Ejemplo de conversión, no medición: 3 minutos y 15 "
                   "segundos equivalen a 3,25 minutos."),
         "constatacion": "ejemplo con coma decimal; sin tabla 'Conversión "
                         "rápida' y sin '3 + 15/60'"},
        {"documento": "05_APOYOS_INVESTIGADOR_INSTRUCCIONES_CIERRE_CONTINUACIONES",
         "frase": "__:__",
         "constatacion": "horas vacías de H-01 a H-12 con guion bajo"},
    ]
    ruta_manifiesto = destino / "MANIFIESTO.json"
    ruta_manifiesto.write_text(
        json.dumps(manifiesto, indent=2, ensure_ascii=False), encoding="utf-8")
    if destino == CANDIDATO_MARCADO:
        _reporte_marcado(manifiesto, destino, publicado=False)
    else:
        _reporte_limpieza(manifiesto, destino, publicado=False)
    return manifiesto


def _reemplazar_rutas(obj, origen: str, destino: str):
    if isinstance(obj, str):
        return obj.replace(origen, destino)
    if isinstance(obj, list):
        return [_reemplazar_rutas(v, origen, destino) for v in obj]
    if isinstance(obj, dict):
        return {k: _reemplazar_rutas(v, origen, destino) for k, v in obj.items()}
    return obj


def publicar_limpieza_candidato() -> Dict[str, Any]:
    """Copia el candidato aprobado a v02 y reescribe rutas del manifiesto."""
    if not (CANDIDATO_LIMPIEZA / "MANIFIESTO.json").exists():
        raise FileNotFoundError("No existe el candidato de limpieza")
    respaldo_manifest = (RAIZ / "salidas" / "archivo"
                         / "INSTRUMENTOS_V02_ANTES_LIMPIEZA_20261022"
                         / "MANIFIESTO.json")
    control_manifest = REDISENO_V02 / "MANIFIESTO.json"
    if not control_manifest.exists():
        control_manifest = respaldo_manifest
    control = json.loads(control_manifest.read_text(encoding="utf-8"))
    for doc in control.get("documentos", []):
        for clave, campo in (("docx", "sha256_docx"),
                             ("pdf", "sha256_pdf")):
            ruta = Path(doc[clave])
            if not ruta.exists():
                raise RuntimeError(f"Falta un archivo vigente: {ruta}")
            actual = seguridad.sha256_archivo(ruta)
            if actual != doc[campo]:
                raise RuntimeError(
                    f"Cambio ajeno detectado en {ruta}; no se sobrescribe. "
                    f"Actual {actual}, control {doc[campo]}")
    for patron in ("*.docx", "*.pdf"):
        for ruta in CANDIDATO_LIMPIEZA.glob(patron):
            objetivo = REDISENO_V02 / ruta.name
            if (objetivo.exists()
                    and seguridad.sha256_archivo(objetivo)
                    == seguridad.sha256_archivo(ruta)):
                continue
            shutil.copy2(ruta, objetivo)
    for ruta in (CANDIDATO_LIMPIEZA / "APOYOS_INVESTIGADOR").glob("*"):
        objetivo = APOYOS_V02 / ruta.name
        if (objetivo.exists()
                and seguridad.sha256_archivo(objetivo)
                == seguridad.sha256_archivo(ruta)):
            continue
        shutil.copy2(ruta, objetivo)
    if REDISENO_V02_RENDER.exists():
        shutil.rmtree(REDISENO_V02_RENDER)
    shutil.copytree(CANDIDATO_LIMPIEZA / "control_visual",
                    REDISENO_V02_RENDER)
    manifiesto = json.loads(
        (CANDIDATO_LIMPIEZA / "MANIFIESTO.json").read_text(encoding="utf-8"))
    manifiesto = _reemplazar_rutas(
        manifiesto, str(CANDIDATO_LIMPIEZA), str(REDISENO_V02))
    manifiesto["meta"]["modo"] = "publicado en v02"
    manifiesto["meta"]["publicado_desde"] = str(CANDIDATO_LIMPIEZA)
    manifiesto["meta"]["sha256_candidato"] = seguridad.sha256_archivo(
        CANDIDATO_LIMPIEZA / "MANIFIESTO.json")
    manifiesto["meta"]["respaldo_manifest_sha256"] = seguridad.sha256_archivo(
        respaldo_manifest)
    for cambio in manifiesto.get("cambios_limpieza", []):
        if cambio.get("id") == "L05":
            cambio["detalle"] = (
                "F02 en tres páginas: bloques D-01 a D-04, CPE E-01 a E-12 "
                "en página propia y líneas de código y fase en las "
                "continuaciones; D-05 a D-07 en apoyo.")
        elif cambio.get("id") == "L06":
            cambio["detalle"] = (
                "A/B con una H1, presentación confidencial, instrucción "
                "única de marcado, anclajes una vez y columnas Likert de "
                "9 mm; reactivos literales.")
    manifiesto["pendientes"] = [
        "Cotejo visual del tesista sobre la v02 publicada.",
        "QG-5 permanece abierta: esta edición no acredita validación de "
        "contenido.",
    ]
    pruebas = manifiesto.setdefault("pruebas_limpieza", {})
    pruebas["F02_tres_paginas_CPE_propia"] = (
        pruebas.get("paginas_por_documento", {}).get(
            "02_FICHA_AUDITORIA_DOCUMENTAL") == 3)
    pruebas.update(_pruebas_por_frase(manifiesto["documentos"]))
    for doc in manifiesto.get("documentos", []):
        for clave, campo, bytes_campo in (
                ("docx", "sha256_docx", "bytes_docx"),
                ("pdf", "sha256_pdf", "bytes_pdf")):
            ruta = Path(doc[clave])
            doc[campo] = seguridad.sha256_archivo(ruta)
            doc[bytes_campo] = ruta.stat().st_size
    (REDISENO_V02 / "MANIFIESTO.json").write_text(
        json.dumps(manifiesto, indent=2, ensure_ascii=False), encoding="utf-8")
    _reporte_limpieza(manifiesto, REDISENO_V02, publicado=True)
    return manifiesto


def publicar_marcado_claro() -> Dict[str, Any]:
    """Publica el candidato de marcado claro tras cotejar el manifiesto actual."""
    if not (CANDIDATO_MARCADO / "MANIFIESTO.json").exists():
        raise FileNotFoundError("No existe el candidato de marcado claro")
    control = json.loads(
        (REDISENO_V02 / "MANIFIESTO.json").read_text(encoding="utf-8"))
    for doc in control.get("documentos", []):
        for clave, campo in (("docx", "sha256_docx"),
                             ("pdf", "sha256_pdf")):
            ruta = Path(doc[clave])
            if not ruta.exists():
                raise RuntimeError(f"Falta un archivo vigente: {ruta}")
            actual = seguridad.sha256_archivo(ruta)
            if actual != doc[campo]:
                raise RuntimeError(
                    f"Cambio ajeno detectado en {ruta}; no se sobrescribe. "
                    f"Actual {actual}, control {doc[campo]}")
    for patron in ("*.docx", "*.pdf"):
        for ruta in CANDIDATO_MARCADO.glob(patron):
            objetivo = REDISENO_V02 / ruta.name
            if (objetivo.exists()
                    and seguridad.sha256_archivo(objetivo)
                    == seguridad.sha256_archivo(ruta)):
                continue
            shutil.copy2(ruta, objetivo)
    for ruta in (CANDIDATO_MARCADO / "APOYOS_INVESTIGADOR").glob("*"):
        objetivo = APOYOS_V02 / ruta.name
        if (objetivo.exists()
                and seguridad.sha256_archivo(objetivo)
                == seguridad.sha256_archivo(ruta)):
            continue
        shutil.copy2(ruta, objetivo)
    if REDISENO_V02_RENDER.exists():
        shutil.rmtree(REDISENO_V02_RENDER)
    shutil.copytree(CANDIDATO_MARCADO / "control_visual",
                    REDISENO_V02_RENDER)
    manifiesto = json.loads(
        (CANDIDATO_MARCADO / "MANIFIESTO.json").read_text(encoding="utf-8"))
    manifiesto = _reemplazar_rutas(
        manifiesto, str(CANDIDATO_MARCADO), str(REDISENO_V02))
    manifiesto["meta"]["modo"] = "publicado en v02"
    manifiesto["meta"]["publicado_desde"] = str(CANDIDATO_MARCADO)
    manifiesto["meta"]["sha256_candidato"] = seguridad.sha256_archivo(
        CANDIDATO_MARCADO / "MANIFIESTO.json")
    fuentes = manifiesto.setdefault("fuentes_preservadas_sha256", {})
    fuentes["builder"] = seguridad.sha256_archivo(
        RAIZ / "scripts" / "compiladores" / "paquete_campo_builder.py")
    fuentes["motor"] = seguridad.sha256_archivo(
        RAIZ / "scripts" / "utilidades" / "docx_quirurgico.py")
    manifiesto["pendientes"] = [
        "Cotejo visual del tesista sobre la v02 publicada.",
        "QG-5 permanece abierta: esta edición no acredita validación de "
        "contenido.",
    ]
    pruebas = manifiesto.setdefault("pruebas_limpieza", {})
    pruebas.update(_pruebas_por_frase(manifiesto["documentos"]))
    for doc in manifiesto.get("documentos", []):
        for clave, campo, bytes_campo in (
                ("docx", "sha256_docx", "bytes_docx"),
                ("pdf", "sha256_pdf", "bytes_pdf")):
            ruta = Path(doc[clave])
            doc[campo] = seguridad.sha256_archivo(ruta)
            doc[bytes_campo] = ruta.stat().st_size
    (REDISENO_V02 / "MANIFIESTO.json").write_text(
        json.dumps(manifiesto, indent=2, ensure_ascii=False), encoding="utf-8")
    _reporte_marcado(manifiesto, REDISENO_V02, publicado=True)
    return manifiesto


def main() -> int:
    seguridad.configurar_utf8()
    parser = argparse.ArgumentParser(description="Constructor del paquete de campo SIVAC")
    parser.add_argument("--paquete", help="Código de participante a emitir, por ejemplo TRAB-01")
    parser.add_argument("--todos", action="store_true", help="Emite los catorce paquetes")
    parser.add_argument("--kit", action="store_true", help="Emite el kit del investigador")
    parser.add_argument("--solo-kit", help="Claves del kit separadas por coma, sin reemitir el resto")
    parser.add_argument("--guia", action="store_true", help="Emite la guía de campo")
    parser.add_argument("--solo", help="Claves de formulario separadas por coma")
    parser.add_argument("--sin-pdf", action="store_true", help="Genera solo los DOCX maestros")
    parser.add_argument("--sin-render", action="store_true", help="Omite el renderizado de control")
    parser.add_argument("--manifiesto", action="store_true", help="Reescribe el manifiesto de etapa 1")
    parser.add_argument("--manifiestos", action="store_true",
                        help="Reescribe el manifiesto de etapa 2 y el consolidado")
    parser.add_argument("--rediseno-fany", action="store_true",
                        help="Emite la carpeta nueva de rediseño editorial aislado")
    parser.add_argument("--version-editorial", choices=("v01", "v02"),
                        default="v01",
                        help="Versión del rediseño aislado; v01 se conserva intacta")
    parser.add_argument("--limpieza-profesional", action="store_true",
                        help="Emite el candidato de limpieza compositiva en staging")
    parser.add_argument("--publicar-limpieza", action="store_true",
                        help="Copia a v02 el candidato de limpieza ya revisado")
    parser.add_argument("--reemitir-b", action="store_true",
                        help="Reemite solo módulo B, conjunto y apoyos; "
                             "conserva 01, 02 y A")
    parser.add_argument("--reemitir-ajustes", action="store_true",
                        help="Reemite F01, F02, A, B y conjunto; conserva apoyos")
    parser.add_argument("--marcado-claro", action="store_true",
                        help="Emite el candidato de marcado claro en staging")
    parser.add_argument("--publicar-marcado", action="store_true",
                        help="Publica en v02 el candidato de marcado claro")
    args = parser.parse_args()

    if args.marcado_claro or args.publicar_marcado:
        if args.publicar_marcado:
            resumen = publicar_marcado_claro()
            destino = REDISENO_V02
        else:
            resumen = construir_limpieza_fany(
                destino=CANDIDATO_MARCADO, con_pdf=not args.sin_pdf,
                con_render=not args.sin_render)
            destino = CANDIDATO_MARCADO
        print(json.dumps({
            "modo": resumen["meta"]["modo"],
            "destino": str(destino),
            "paginas": resumen.get("pruebas_limpieza", {}).get(
                "paginas_por_documento", {}),
            "control": {
                "sin_glifos": resumen.get("pruebas_limpieza", {}).get(
                    "sin_glifos_checkbox_o_corchetes"),
                "sin_codigos": resumen.get("pruebas_limpieza", {}).get(
                    "sin_codigos_protocolo_visibles"),
            },
        }, ensure_ascii=False, indent=2))
        return 0

    if (args.limpieza_profesional or args.publicar_limpieza
            or args.reemitir_b or args.reemitir_ajustes):
        if args.publicar_limpieza:
            resumen = publicar_limpieza_candidato()
            destino = REDISENO_V02
        else:
            if args.reemitir_ajustes:
                solo = {"01_FICHA_TIEMPOS", "02_FICHA_AUDITORIA_DOCUMENTAL",
                        "03_CUESTIONARIO_SATISFACCION_A",
                        "04_MODULO_COMPLEMENTARIO_B_POST", "CONJUNTO_00"}
            elif args.reemitir_b:
                solo = {"04_MODULO_COMPLEMENTARIO_B_POST", "CONJUNTO_00",
                        "APOYOS"}
            else:
                solo = None
            resumen = construir_limpieza_fany(con_pdf=not args.sin_pdf,
                                              con_render=not args.sin_render,
                                              solo_reexportar=solo)
            destino = CANDIDATO_LIMPIEZA
        print(json.dumps({
            "modo": resumen["meta"]["modo"],
            "destino": str(destino),
            "paginas": resumen.get("pruebas_limpieza", {}).get(
                "paginas_por_documento", {}),
            "reactivos_16_iguales": resumen.get("pruebas_limpieza", {}).get(
                "reactivos_16_iguales"),
        }, ensure_ascii=False, indent=2))
        return 0

    if args.rediseno_fany:
        resumen = construir_rediseno_fany(con_pdf=not args.sin_pdf,
                                          con_render=not args.sin_render,
                                          version=args.version_editorial)
        print(json.dumps({
            "version": resumen["meta"].get("version"),
            "destino": resumen["meta"]["destino"],
            "documentos": [
                {"docx": d["docx"], "pdf": d["pdf"], "paginas": d["paginas"],
                 "sha256_pdf": d["sha256_pdf"], "desborde_pt": d["desborde_inferior_pt"],
                 "tokens_prohibidos": d["tokens_prohibidos"]}
                for d in resumen["documentos"]
            ],
            "reactivos_igualdad_completa": resumen["reactivos"]["igualdad_completa"],
            "render": len(resumen["render"]),
        }, indent=2, ensure_ascii=False))
        return 0

    resumen: Dict[str, Any] = {}
    if args.guia:
        resumen["guia"] = construir_guia(con_pdf=not args.sin_pdf)
    solo = [s.strip() for s in args.solo.split(",")] if args.solo else None
    codigos: List[str] = []
    if args.todos:
        codigos = [f"TRAB-{indice:02d}" for indice in range(1, 15)]
    elif args.paquete:
        codigos = [args.paquete]
    if codigos:
        resumen["paquetes"] = [
            construir_paquete(codigo, solo=solo, con_pdf=not args.sin_pdf)
            for codigo in codigos
        ]
        if not args.sin_render and not args.sin_pdf and codigos == ["TRAB-01"]:
            resumen["render"] = renderizar_control(codigos[0])
        resumen["manifiesto_etapa1"] = {
            "ruta": str(MANIFIESTO),
            "verificaciones": escribir_manifiesto(codigos[0])["verificaciones"]["general"],
        }
    if args.kit or args.solo_kit:
        solo_kit = ([s.strip() for s in args.solo_kit.split(",") if s.strip()]
                    if args.solo_kit else None)
        resumen["kit"] = construir_kit(con_pdf=not args.sin_pdf, solo=solo_kit)
        if not args.sin_render and not args.sin_pdf:
            RENDER.mkdir(parents=True, exist_ok=True)
            hechas = []
            for entrada in _registro_kit():
                if solo_kit is not None and entrada["clave"] not in solo_kit:
                    continue
                pdf = KIT / entrada["rel"]
                if pdf.exists():
                    hechas.extend(quir.renderizar_paginas_pdf(
                        pdf, [1], dpi=110, salida_dir=RENDER)["renderizadas"])
            resumen["render_kit"] = hechas
    if args.manifiestos:
        etapa2 = escribir_manifiesto_etapa2()
        global_ = escribir_manifiesto_global()
        resumen["manifiestos"] = {
            "etapa2": {"ruta": str(MANIFIESTO_ETAPA2), "totales": etapa2["totales"]},
            "global": {"ruta": str(MANIFIESTO_GLOBAL), "totales": global_["totales"]},
        }
    elif args.manifiesto and not codigos:
        resumen["manifiesto"] = str(MANIFIESTO)
    print(json.dumps(resumen, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
