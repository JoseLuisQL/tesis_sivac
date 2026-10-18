#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB - Squad B (Metodología y Psicometría) & Formatos Worker
GENERADOR DE FORMATOS DE VALIDACIÓN POR JUICIO DE EXPERTOS EN BLANCO
Modelo derivado del formato del Dr. Enrique Cóndor Tinoco (EPIS-UNAJMA),
superado por DEC-015

[SUPERADO POR DEC-015 - 2026-10-18]
La CLI de este script está bloqueada. El modelo institucional vigente es
Fany 2024 y el generador vigente es
scripts/compiladores/generar_anexo2_validacion_fany.py, que escribe en
salidas/documentos/anexos_fany/. Este módulo se conserva únicamente porque la
suite scripts/tests/test_formatos_validacion.py audita con él la fidelidad del
modelo heredado.
================================================================================
Este script reproduce, para auditoría del modelo heredado, los formatos de
validación por juicio de expertos para los tres instrumentos de la tesis SIVAC:
  1. INST01: Ficha de observación de tiempos cronometrados (8 ítems)
  2. INST02: Guía de cotejo documental de consistencia (8 ítems)
  3. INST03: Cuestionario de satisfacción del usuario TAM (8 reactivos
     baremables de la Modalidad A y 8 reactivos de módulo anexo de la
     Modalidad B; DEC-019 y DEC-020)

Estructura de cada formato:
  - Parte 1: Carta formal de solicitud (1 página por juez)
  - Parte 2: Hoja de instrucciones para validación
  - Parte 3: Tabla rúbrica de evaluación 6x3 (5 criterios + encabezado)
  - Parte 4: Constancia de validación por ítem con tabla de 8 columnas y firma

Estrategia de fidelidad:
  Abre una copia del DOCX modelo 'Formato para la validacion de instrumento por
  ITEM.docx' (solo lectura en referencias/) para heredar estilos, numbering,
  settings y sectPr. Sustituye únicamente el texto específico de SIVAC registrado
  en FV/LEEME_SUSTITUCIONES_Y_FIDELIDAD.md. Preserva erratas del modelo y
  garantiza formato 100% en blanco (sin puntajes, CIP, fecha de constancia ni
  veredicto).
================================================================================
"""

import os
import sys
import copy
import shutil
import tempfile
import argparse
from pathlib import Path
import docx
from lxml import etree

# Asegurar importación de módulos del proyecto
RUTA_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if RUTA_BASE not in sys.path:
    sys.path.insert(0, RUTA_BASE)

from scripts.compiladores.generar_expedientes_e_instrumentos import (
    ITEMS_INST1,
    ITEMS_INST2,
    ITEMS_INST3,
)

# -----------------------------------------------------------------------------
# CONSTANTES INSTITUCIONALES Y METADATOS SIVAC (ÚNICA FUENTE DE VERDAD)
# -----------------------------------------------------------------------------
TITULO_TESIS_OFICIAL = (
    "APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE "
    "VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II"
)
TESISTA_OFICIAL = "Bach. José Luis Quispe León"
DNI_TESISTA_OFICIAL = "70519963"
ESCUELA_OFICIAL = "Escuela Profesional de Ingeniería de Sistemas"
UNIVERSIDAD_OFICIAL = "Universidad Nacional José María Arguedas"
TITULO_A_OPTAR = "Título Profesional de Ingeniero de Sistemas"
ANO_OFICIAL = "2026"
CIUDAD_OFICIAL = "Andahuaylas"

MODELO_PATH = os.path.join(
    RUTA_BASE,
    "referencias",
    "modelos_validacion",
    "Formato para la validacion de instrumento por ITEM.docx",
)
DIR_SALIDA_DEFECTO = os.path.join(
    RUTA_BASE, "salidas", "instrumentos", "formatos_validacion"
)

# Metadatos de instrumentos SIVAC
INSTRUMENTOS_METADATOS = {
    "INST01": {
        "numero": 1,
        "codigo": "INST01",
        "nombre_archivo": "FICHA_TIEMPOS",
        "nombre_adjunto": (
            "Instrumento N° 1 Ficha de observación sistemática y medición de "
            "tiempos cronometrados"
        ),
        "nombre_constancia": (
            "Ficha de observación sistemática y medición de tiempos cronometrados"
        ),
        "total_items": 8,
    },
    "INST02": {
        "numero": 2,
        "codigo": "INST02",
        "nombre_archivo": "GUIA_COTEJO",
        "nombre_adjunto": (
            "Instrumento N° 2 Guía de cotejo documental de consistencia de "
            "movimientos"
        ),
        "nombre_constancia": (
            "Guía de cotejo documental de consistencia de movimientos"
        ),
        "total_items": 8,
    },
    "INST03": {
        "numero": 3,
        "codigo": "INST03",
        "nombre_archivo": "CUESTIONARIO_TAM",
        "nombre_adjunto": (
            "Instrumento N° 3 Cuestionario de satisfacción del usuario y "
            "aceptación tecnológica (modelo TAM)"
        ),
        "nombre_constancia": (
            "Cuestionario de satisfacción del usuario y aceptación tecnológica "
            "(modelo TAM)"
        ),
        # Alcance certificable (DEC-019 y DEC-020): 8 reactivos baremables de la
        # Modalidad A. Los 8 reactivos de módulo anexo de la Modalidad B no
        # reciben certificado de contenido.
        "total_items": 8,
        "total_items_modalidad_b": 8,
    },
}

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def cargar_items_instrumentos():
    """Carga los ítems oficiales de los tres instrumentos desde la fuente de verdad.

    Retorna un diccionario:
      {"INST01": list_items_inst1, "INST02": list_items_inst2, "INST03": list_items_inst3}

    Composición conforme a DEC-019 y DEC-020:
      - Instrumento 01: 8 ítems (sin juicio de contenido).
      - Instrumento 02: 8 ítems (sin juicio de contenido).
      - Instrumento 03: 8 reactivos baremables de la Modalidad A (AP-01 a AP-04 y
        UP-01 a UP-04), los únicos que reciben certificado de validez de contenido,
        más 8 reactivos de módulo anexo de la Modalidad B (PU-01 a PU-04 y
        PE-01 a PE-04), sin certificado de contenido.
    La lista completa del Instrumento 03 conserva sus 16 reactivos porque el
    modelo heredado los reproduce; el alcance certificado es el de la Modalidad A.
    """
    return {
        "INST01": list(ITEMS_INST1),
        "INST02": list(ITEMS_INST2),
        "INST03": list(ITEMS_INST3),
    }


def _limpiar_runs_parrafo(p):
    """Elimina los runs hijos de un párrafo preservando intacto el elemento pPr."""
    for r in p._p.xpath("./w:r"):
        p._p.remove(r)


def generar_documento_formato(
    codigo_instrumento,
    num_juez=1,
    ruta_salida=None,
    incluir_tabla_constancia=True,
):
    """Genera un archivo DOCX de validación a partir del modelo heredado.

    El modelo de referencia (Cóndor Tinoco) quedó superado por DEC-015; esta
    función se conserva solo porque la suite de pruebas audita con ella la
    fidelidad del modelo heredado. Los formatos vigentes son los certificados
    en blanco del modelo Fany 2024 generados por
    scripts/compiladores/generar_anexo2_validacion_fany.py.

    Parámetros:
      codigo_instrumento (str): 'INST01', 'INST02' o 'INST03'.
      num_juez (int): 1, 2 o 3.
      ruta_salida (str|Path): Ruta donde guardar el archivo generado.
      incluir_tabla_constancia (bool): Si es True, incluye la tabla de constancia
                                       (desarrollada en feature posterior).
    Retorna:
      Path al archivo DOCX generado.
    """
    if codigo_instrumento not in INSTRUMENTOS_METADATOS:
        raise ValueError(f"Código de instrumento desconocido: {codigo_instrumento}")

    meta = INSTRUMENTOS_METADATOS[codigo_instrumento]

    if ruta_salida is None:
        os.makedirs(DIR_SALIDA_DEFECTO, exist_ok=True)
        nombre_archivo = (
            f"FORMATO_VALIDACION_{meta['codigo']}_{meta['nombre_archivo']}_JUEZ{num_juez}.docx"
        )
        ruta_salida = os.path.join(DIR_SALIDA_DEFECTO, nombre_archivo)
    else:
        ruta_salida = str(ruta_salida)
        os.makedirs(os.path.dirname(os.path.abspath(ruta_salida)), exist_ok=True)

    # 1. Abrir COPIA temporal del modelo (jamás escribir en referencias/)
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_modelo_path = os.path.join(tmpdir, "modelo_temp.docx")
        shutil.copy2(MODELO_PATH, temp_modelo_path)
        doc = docx.Document(temp_modelo_path)
        body = doc._body._element

        # =========================================================================
        # PARTE 1: CARTA DE PRESENTACIÓN (P000 a P028)
        # =========================================================================
        # P000: Fecha ("Andahuaylas, …… de [tab punteado] de 2026")
        p0 = doc.paragraphs[0]
        for r in p0.runs:
            if "2025" in r.text:
                r.text = r.text.replace("2025", ANO_OFICIAL)

        # P004: Destinatario en blanco con puntos suspensivos (idéntico a Carta 3 P062)
        p4 = doc.paragraphs[4]
        _limpiar_runs_parrafo(p4)
        p4.add_run("                    ……………………………………………………………………………")

        # P005: Cargo del destinatario
        p5 = doc.paragraphs[5]
        _limpiar_runs_parrafo(p5)
        p5.add_run(f"                   Docente de la {ESCUELA_OFICIAL}")

        # P008: Párrafo de presentación (Bach. José Luis Quispe León en singular)
        p8 = doc.paragraphs[8]
        _limpiar_runs_parrafo(p8)
        p8.add_run("Yo, ")
        r_nombre = p8.add_run(TESISTA_OFICIAL)
        r_nombre.bold = True
        p8.add_run(
            f" con DNI N° {DNI_TESISTA_OFICIAL}, tesista de la {ESCUELA_OFICIAL}, "
            "me dirijo a usted con el debido respeto y me presento y expongo:\xa0"
        )

        # P009: Párrafo de petición (Título SIVAC y grado a optar)
        p9 = doc.paragraphs[9]
        _limpiar_runs_parrafo(p9)
        p9.add_run(
            "Dada su experiencia profesional y méritos académicos, recurrimos a su "
            "honorable persona para solicitarle su inapreciable colaboración como "
            "experto para la validación del instrumento de nuestra investigación que "
            "adjuntamos como anexo al presente, del trabajo de investigación intitulado "
        )
        r_titulo = p9.add_run(f"“{TITULO_TESIS_OFICIAL}”")
        r_titulo.bold = True
        p9.add_run(
            f"; para optar el {TITULO_A_OPTAR}, sus observaciones y "
            "recomendaciones como juez de validación serán de gran ayuda para "
            "perfeccionar los instrumentos de investigación. "
        )

        # P015: Cuarto documento adjunto (Instrumento correspondiente)
        p15 = doc.paragraphs[15]
        _limpiar_runs_parrafo(p15)
        p15.add_run(meta["nombre_adjunto"])

        # P025 a P028: Bloque de firma única del tesista centrada con espacios/NBSP
        p25 = doc.paragraphs[25]
        _limpiar_runs_parrafo(p25)
        p25.add_run("                                        ……………………………………….…")

        p26 = doc.paragraphs[26]
        _limpiar_runs_parrafo(p26)
        p26.add_run(f"                                    {TESISTA_OFICIAL}")

        p27 = doc.paragraphs[27]
        _limpiar_runs_parrafo(p27)
        p27.add_run("                                                Tesista")

        p28 = doc.paragraphs[28]
        _limpiar_runs_parrafo(p28)
        p28.add_run(f"                                            DNI N° {DNI_TESISTA_OFICIAL}")

        # En el sectPr de P028, remover w:type continuous para salto de página limpio a Instrucciones
        for t in p28._p.xpath("./w:pPr/w:sectPr/w:type"):
            t.getparent().remove(t)

        # =========================================================================
        # PARTE 2 Y 3: HOJA DE INSTRUCCIONES Y TABLA RÚBRICA 6x3 (P088 a P101)
        # =========================================================================
        # Los elementos 88 a 101 corresponden a la Hoja de Instrucciones y Rúbrica
        # del modelo heredado (Cóndor Tinoco, superado por DEC-015). Se conservan
        # 100% literales e intactos, heredando
        # la lista numerada, criterios, escala y la tabla de 6x3 con tblGrid
        # 1294/1609/6091, fixed layout y bordes sz 4.

        # =========================================================================
        # PARTE 4: CONSTANCIA DE VALIDACIÓN POR ÍTEM (P102 a P115 y final sectPr)
        # =========================================================================
        # Body[102] es el Título "CONSTANCIA DE VALIDACIÓN DE CONTENIDO DEL INSTRUMENTO POR ÍTEM"
        # Body[103] es el Párrafo de Declaración con campos en blanco
        p103 = docx.text.paragraph.Paragraph(body[103], doc)
        _limpiar_runs_parrafo(p103)
        p103.add_run(
            "Quien suscribe, ………………………………………………………………, con DNI Nº………………, "
            "de profesión…………………………………………………………. con Grado de ..…...………………………………………………………………………., "
            "por medio de la presente hago constar que he revisado con fines de "
            f"validación el instrumento de recolección de datos {meta['nombre_constancia']} "
            f"del proyecto de investigación “{TITULO_TESIS_OFICIAL}” para los efectos "
            f"de su aplicación, presentado por el tesista {TESISTA_OFICIAL}. "
            "Luego revisar el instrumento, puedo formular las siguientes apreciaciones:"
        )

        # Body[104] es el párrafo espaciador previo a la tabla de constancia

        # Body[105] es la Tabla de Constancia de 8 columnas del modelo heredado
        # (Cóndor Tinoco, superado por DEC-015).
        # Se adapta sustituyendo las filas de autoaprendizaje por los ítems oficiales
        # de la tesis SIVAC (INST01=8, INST02=8, INST03=16; total 9/9/17 filas)
        tbl_const = body[105]
        rows_tbl = tbl_const.findall("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tr")
        template_row = copy.deepcopy(rows_tbl[1])
        for r in rows_tbl[1:]:
            tbl_const.remove(r)

        # Limpiar negrita en párrafo de ítem de la fila plantilla para texto regular
        tcs_template = template_row.findall("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc")
        pPr_item = tcs_template[1].find(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr")
        if pPr_item is not None:
            rPr_item = pPr_item.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr")
            if rPr_item is not None:
                b_tag = rPr_item.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}b")
                if b_tag is not None:
                    rPr_item.remove(b_tag)

        # Cargar los ítems oficiales correspondientes al instrumento
        items_dict = cargar_items_instrumentos()
        items_instrumento = items_dict[codigo_instrumento]

        for idx, item in enumerate(items_instrumento):
            tr_item = copy.deepcopy(template_row)
            tcs = tr_item.findall("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc")

            # Col 0: Nº (1..N) en 9 pt (sz 18)
            t0 = tcs[0].find(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t")
            if t0 is not None:
                t0.text = str(idx + 1)

            # Col 1: Texto del ítem oficial en 9 pt (sz 18), justificado
            item_text = item[1] if isinstance(item, (tuple, list)) else str(item)
            t1 = tcs[1].find(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t")
            if t1 is not None:
                t1.text = item_text

            # Cols 2 a 7: Celdas vacías de calificación y observaciones (sin marcas ni texto)
            for c_idx in range(2, 8):
                for r_elem in tcs[c_idx].xpath(".//w:r"):
                    r_elem.getparent().remove(r_elem)

            tbl_const.append(tr_item)

        # Body[106] a [111]: 6 párrafos vacíos de espacio de firma (10 pt)
        # Body[112]: Línea de firma (4 tabs + 28 guiones bajos 10 pt)
        # Body[113]: Rótulo "Firma" centrado 10 pt
        # Body[114]: Rótulo "DNI: ……………………….." centrado 10 pt
        # Body[115]: Párrafo espaciador centrado 10 pt

        # =========================================================================
        # REORGANIZACIÓN DEL CUERPO (BODY CHILDREN)
        # =========================================================================
        # Conservar solo:
        # - Carta 1 adaptada (0 a 28)
        # - Instrucciones + Rúbrica (88 a 101)
        # - Constancia título, declaración y espaciador (102, 103, 104)
        # - Tabla de constancia de 8 columnas adaptada (105)
        # - Bloque de firma en blanco (106 a 115)
        # - sectPr final del documento (body[-1])
        elementos_conservar = []
        for i in range(29):
            elementos_conservar.append(body[i])
        for i in range(88, 102):
            elementos_conservar.append(body[i])
        elementos_conservar.append(body[102])
        elementos_conservar.append(body[103])
        elementos_conservar.append(body[104])
        elementos_conservar.append(tbl_const)
        for i in range(106, 116):
            elementos_conservar.append(body[i])
        elementos_conservar.append(body[-1])

        for c in list(body):
            body.remove(c)
        for c in elementos_conservar:
            body.append(c)

        doc.save(ruta_salida)

    return Path(ruta_salida)


def main():
    """Punto de entrada de línea de comandos (CLI).

    BLOQUEADO POR DEC-015 (2026-10-18)
    ----------------------------------
    El modelo institucional de referencia ya no es el formato Cóndor Tinoco, sino
    el modelo Fany 2024 (Anexo 2, páginas impresas 62 a 65), con criterios
    dicotómicos Sí/No de Pertinencia, Relevancia y Claridad. Ejecutar esta CLI
    volvería a escribir formatos obsoletos con escala 1-4 en la ruta oficial
    salidas/instrumentos/formatos_validacion/.

    La función generar_documento_formato() se conserva intacta porque la suite
    scripts/tests/test_formatos_validacion.py la usa para auditar la fidelidad
    del modelo heredado. El generador vigente es
    scripts/compiladores/generar_anexo2_validacion_fany.py.
    """
    raise SystemExit(
        "Generacion bloqueada por DEC-015: el modelo Condor fue reemplazado por "
        "el modelo Fany 2024. Usar scripts/compiladores/"
        "generar_anexo2_validacion_fany.py, que produce los certificados en "
        "blanco en salidas/documentos/anexos_fany/."
    )


def _main_deshabilitado():
    """Cuerpo original de la CLI, preservado solo como referencia histórica."""
    parser = argparse.ArgumentParser(
        description="Generador de formatos de validación por juicio de expertos SIVAC."
    )
    parser.add_argument(
        "--instrumento",
        choices=["INST01", "INST02", "INST03", "todos"],
        default="todos",
        help="Instrumento a generar (default: todos)",
    )
    parser.add_argument(
        "--juez",
        choices=["1", "2", "3", "todos"],
        default="todos",
        help="Número de juez (default: todos)",
    )
    parser.add_argument(
        "--salida",
        default=DIR_SALIDA_DEFECTO,
        help="Directorio de salida para los formatos DOCX",
    )

    args = parser.parse_args()

    instrumentos = (
        ["INST01", "INST02", "INST03"]
        if args.instrumento == "todos"
        else [args.instrumento]
    )
    jueces = [1, 2, 3] if args.juez == "todos" else [int(args.juez)]

    print("========================================================================")
    print("SIVAC - GENERADOR DE FORMATOS DE VALIDACIÓN POR JUICIO DE EXPERTOS")
    print("========================================================================")
    print(f"Directorio de salida: {args.salida}")
    print(f"Instrumentos a generar: {instrumentos}")
    print(f"Jueces: {jueces}")
    print("------------------------------------------------------------------------")

    generados = []
    for cod_inst in instrumentos:
        for num_juez in jueces:
            meta = INSTRUMENTOS_METADATOS[cod_inst]
            nombre_archivo = (
                f"FORMATO_VALIDACION_{meta['codigo']}_{meta['nombre_archivo']}_JUEZ{num_juez}.docx"
            )
            ruta_out = os.path.join(args.salida, nombre_archivo)
            out_file = generar_documento_formato(cod_inst, num_juez, ruta_out)
            generados.append(out_file)
            print(f" [OK] Generado: {os.path.basename(out_file)}")

    print("------------------------------------------------------------------------")
    print(f"Total de formatos generados: {len(generados)}")
    print("========================================================================")


if __name__ == "__main__":
    main()
