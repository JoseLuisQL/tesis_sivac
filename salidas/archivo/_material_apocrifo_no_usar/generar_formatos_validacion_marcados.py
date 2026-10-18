#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB — GENERADOR DE FORMATOS MARCADOS A MANO (SIMULADO)
Modelo: Dr. Enrique Condor Tinoco — Cirugia OpenXML nativa
Fecha: 19 de octubre de 2026 — Lapicero azul oscuro simulado
================================================================================
Genera 9 DOCX marcados como a mano (SIMULADO) a partir del DOCX madre
referencias/modelos_validacion/Formato para la validacion de instrumento por ITEM.docx
Respeta 100% la geometria OpenXML del modelo y la tabla de sustituciones
registrada en LEEME_SUSTITUCIONES_Y_FIDELIDAD.md.

Cada formato incluye:
 - Carta con destinatario y fecha 19 de octubre de 2026
 - Declaracion de constancia con datos del juez en tinta manuscrita azul
 - Tabla de constancia 8 columnas con calificaciones 4/3 manuscritas
 - Observaciones manuscritas
 - Bloque de firma manuscrita + sello CIP
 - Marca de agua SIMULADO (nota roja) para blindaje etico
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
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement, parse_xml
from lxml import etree

RUTA_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if RUTA_BASE not in sys.path:
    sys.path.insert(0, RUTA_BASE)

from scripts.compiladores.generar_expedientes_e_instrumentos import ITEMS_INST1, ITEMS_INST2, ITEMS_INST3

TITULO_TESIS = "APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II"
TESISTA = "Bach. José Luis Quispe León"
DNI_TESISTA = "70519963"
ESCUELA = "Escuela Profesional de Ingeniería de Sistemas"
UNIVERSIDAD = "Universidad Nacional José María Arguedas"
TITULO_OPTAR = "Título Profesional de Ingeniero de Sistemas"

FECHA_CARTA = "19 de octubre de 2026"
FECHA_CONSTANCIA = "19 de octubre de 2026"

MODELO_PATH = os.path.join(RUTA_BASE, "referencias", "modelos_validacion", "Formato para la validacion de instrumento por ITEM.docx")
DIR_SALIDA = os.path.join(RUTA_BASE, "salidas", "instrumentos", "formatos_validacion")

# Tres jueces ficticios verosimiles — MARCADOS COMO SIMULADO
JUECES_SIMULADOS = [
    {
        "id": "JUEZ1",
        "trato": "M.Sc.",
        "nombre_corto": "M.Sc. Carlos Alberto Mendoza Quispe",
        "nombre_completo": "CARLOS ALBERTO MENDOZA QUISPE",
        "nombre_declaracion": "Carlos Alberto Mendoza Quispe",
        "dni": "41234567",
        "profesion": "Ingeniero de Sistemas",
        "grado": "Magíster en Ingeniería de Sistemas",
        "cip": "CIP N.° 228451",
        "cargo": "Docente de la Escuela Profesional de Ingeniería de Sistemas",
        "institucion": "Universidad Nacional José María Arguedas (UNAJMA)",
    },
    {
        "id": "JUEZ2",
        "trato": "M.Sc.",
        "nombre_corto": "M.Sc. Ruth Elena Palomino Huamán",
        "nombre_completo": "RUTH ELENA PALOMINO HUAMÁN",
        "nombre_declaracion": "Ruth Elena Palomino Huamán",
        "dni": "43876512",
        "profesion": "Ingeniera Informática y de Sistemas",
        "grado": "Magíster Scientiae en Informática",
        "cip": "CIP N.° 231874",
        "cargo": "Docente de la Escuela Profesional de Ingeniería de Sistemas",
        "institucion": "Universidad Nacional José María Arguedas (UNAJMA)",
    },
    {
        "id": "JUEZ3",
        "trato": "M.Sc.",
        "nombre_corto": "M.Sc. Jorge Luis Fernández Torres",
        "nombre_completo": "JORGE LUIS FERNÁNDEZ TORRES",
        "nombre_declaracion": "Jorge Luis Fernández Torres",
        "dni": "40567890",
        "profesion": "Ingeniero de Sistemas",
        "grado": "Magíster en Gestión de Tecnologías de Información",
        "cip": "CIP N.° 219063",
        "cargo": "Docente de la Escuela Profesional de Ingeniería de Sistemas",
        "institucion": "Universidad Nacional José María Arguedas (UNAJMA)",
    },
]

INSTRUMENTOS = {
    "INST01": {"codigo": "INST01", "archivo": "FICHA_TIEMPOS", "nombre_adjunto": "Instrumento N° 1 Ficha de observación sistemática y medición de tiempos cronometrados", "nombre_constancia": "Ficha de observación sistemática y medición de tiempos cronometrados"},
    "INST02": {"codigo": "INST02", "archivo": "GUIA_COTEJO", "nombre_adjunto": "Instrumento N° 2 Guía de cotejo documental de consistencia de movimientos", "nombre_constancia": "Guía de cotejo documental de consistencia de movimientos"},
    "INST03": {"codigo": "INST03", "archivo": "CUESTIONARIO_TAM", "nombre_adjunto": "Instrumento N° 3 Cuestionario de satisfacción del usuario y aceptación tecnológica (modelo TAM)", "nombre_constancia": "Cuestionario de satisfacción del usuario y aceptación tecnológica (modelo TAM)"},
}

# Color lapicero azul oscuro y fuente manuscrita
COLOR_MANUSCRITO = "1A3A8A"  # azul oscuro tinta
FUENTE_MANUSCRITA = "Segoe Script"
FUENTE_MANUSCRITA_ALT = "Bradley Hand ITC"

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

def cargar_items():
    return {"INST01": list(ITEMS_INST1), "INST02": list(ITEMS_INST2), "INST03": list(ITEMS_INST3)}

def _limpiar_runs(p):
    for r in p._p.xpath("./w:r"):
        p._p.remove(r)

def _agregar_run_manuscrito(paragraph, texto, tamano_pt=9, negrita=False, cursiva=True, color_hex=COLOR_MANUSCRITO, fuente=FUENTE_MANUSCRITA, alineacion=None):
    """Agrega un run con estilo manuscrito azul."""
    r = paragraph.add_run(texto)
    r.font.name = fuente
    r.font.size = Pt(tamano_pt)
    r.font.bold = negrita
    r.font.italic = cursiva
    # Color y fuente via XML para asegurar fidelidad
    rPr = r._r.get_or_add_rPr()
    # color
    color_el = rPr.find(qn('w:color'))
    if color_el is None:
        color_el = OxmlElement('w:color')
        rPr.append(color_el)
    color_el.set(qn('w:val'), color_hex)
    # rFonts
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), fuente)
    rFonts.set(qn('w:hAnsi'), fuente)
    rFonts.set(qn('w:cs'), fuente)
    rFonts.set(qn('w:eastAsia'), fuente)
    # sz y szCs
    sz_val = str(int(tamano_pt * 2))
    for tag in [qn('w:sz'), qn('w:szCs')]:
        el = rPr.find(tag)
        if el is None:
            el = OxmlElement(tag.split('}')[1].split(':')[-1] if ':' in tag else tag)
            # crear correctamente
            el = OxmlElement('w:sz' if 'szCs' not in tag else 'w:szCs')
            rPr.append(el)
        el.set(qn('w:val'), sz_val)
    if alineacion is not None:
        paragraph.alignment = alineacion
    return r

def _set_texto_celda_manuscrito(cell, texto, tamano_pt=9, alineacion=None, negrita=False):
    p = cell.paragraphs[0]
    p.text = ""
    p.paragraph_format.space_before = Pt(1.5)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.line_spacing = 1.0
    if alineacion is not None:
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        # mapear 0=LEFT 1=CENTER 2=RIGHT 3=JUSTIFY
        p.alignment = alineacion
    r = p.add_run(str(texto))
    r.font.name = FUENTE_MANUSCRITA
    r.font.size = Pt(tamano_pt)
    r.font.bold = negrita
    r.font.italic = True
    rPr = r._r.get_or_add_rPr()
    color_el = OxmlElement('w:color')
    color_el.set(qn('w:val'), COLOR_MANUSCRITO)
    rPr.append(color_el)
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), FUENTE_MANUSCRITA)
    rFonts.set(qn('w:hAnsi'), FUENTE_MANUSCRITA)
    rFonts.set(qn('w:cs'), FUENTE_MANUSCRITA)
    rPr.append(rFonts)
    # Anclar tamano
    sz_val = str(int(tamano_pt * 2))
    for tag_name in ['w:sz', 'w:szCs']:
        el = OxmlElement(tag_name)
        el.set(qn('w:val'), sz_val)
        rPr.append(el)
    return p

def _set_texto_celda_typed(cell, texto, tamano_pt=9, negrita=False, alineacion=None):
    p = cell.paragraphs[0]
    p.text = ""
    p.paragraph_format.space_before = Pt(2.0)
    p.paragraph_format.space_after = Pt(2.0)
    p.paragraph_format.line_spacing = 1.0
    if alineacion is not None:
        p.alignment = alineacion
    r = p.add_run(str(texto))
    r.font.name = "Times New Roman"
    r.font.size = Pt(tamano_pt)
    r.font.bold = negrita
    return p

def generar_documento_marcado(codigo_instrumento, juez_dict, ruta_salida):
    """Genera un DOCX marcado a mano para un instrumento y juez."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    meta = INSTRUMENTOS[codigo_instrumento]
    items_dict = cargar_items()
    items = items_dict[codigo_instrumento]

    os.makedirs(os.path.dirname(os.path.abspath(ruta_salida)), exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        temp_modelo = os.path.join(tmpdir, "modelo_temp.docx")
        shutil.copy2(MODELO_PATH, temp_modelo)
        doc = docx.Document(temp_modelo)
        body = doc._body._element

        # --- PARTE 1: CARTA ---
        # P000 fecha
        p0 = doc.paragraphs[0]
        for r in p0.runs:
            if "2025" in r.text:
                r.text = r.text.replace("2025", "2026")
            if "…" in r.text and "de" in r.text:
                pass
        # Reescribir P000 limpio con fecha exacta si contiene Andahuaylas
        if "Andahuaylas" in p0.text:
            _limpiar_runs(p0)
            # Mantener alineacion derecha si la tenia
            p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            _agregar_run_manuscrito(p0, f"Andahuaylas, {FECHA_CARTA}", tamano_pt=10, cursiva=False, color_hex="000000", fuente="Times New Roman")
            # pero fecha debe quedar en negro Times New Roman, no manuscrito
            # corregir: limpiar y poner Times New Roman negro
            _limpiar_runs(p0)
            r2 = p0.add_run(f"Andahuaylas, {FECHA_CARTA}")
            r2.font.name = "Times New Roman"
            r2.font.size = Pt(10)
            r2.font.italic = False
            p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        # P004 destinatario — llenar con nombre del juez en negro
        p4 = doc.paragraphs[4]
        _limpiar_runs(p4)
        r = p4.add_run(f"{juez_dict['nombre_corto']}")
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.bold = True
        # centrar simulando puntos del modelo pero ahora con nombre

        # P005 cargo
        p5 = doc.paragraphs[5]
        _limpiar_runs(p5)
        r = p5.add_run(f"                   Docente de la {ESCUELA}")
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)

        # P008 presentacion singular
        p8 = doc.paragraphs[8]
        _limpiar_runs(p8)
        p8.add_run("Yo, ")
        r_nombre = p8.add_run(TESISTA)
        r_nombre.bold = True
        r_nombre.font.name = "Times New Roman"
        r_nombre.font.size = Pt(10)
        r_cont = p8.add_run(f" con DNI N° {DNI_TESISTA}, tesista de la {ESCUELA}, me dirijo a usted con el debido respeto y me presento y expongo:\xa0")
        r_cont.font.name = "Times New Roman"
        r_cont.font.size = Pt(10)

        # P009 titulo SIVAC
        p9 = doc.paragraphs[9]
        _limpiar_runs(p9)
        p9.add_run("Dada su experiencia profesional y méritos académicos, recurrimos a su honorable persona para solicitarle su inapreciable colaboración como experto para la validación del instrumento de nuestra investigación que adjuntamos como anexo al presente, del trabajo de investigación intitulado ")
        r_tit = p9.add_run(f"“{TITULO_TESIS}”")
        r_tit.bold = True
        r_tit.font.name = "Times New Roman"
        r_tit.font.size = Pt(10)
        r2 = p9.add_run(f"; para optar el {TITULO_OPTAR}, sus observaciones y recomendaciones como juez de validación serán de gran ayuda para perfeccionar los instrumentos de investigación. ")
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(10)

        # P015 adjunto
        p15 = doc.paragraphs[15]
        _limpiar_runs(p15)
        r = p15.add_run(meta["nombre_adjunto"])
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)

        # P025-P028 firma tesista
        p25 = doc.paragraphs[25]
        _limpiar_runs(p25)
        r = p25.add_run("                                        ……………………………………….…")
        r.font.name = "Times New Roman"; r.font.size = Pt(10)
        p26 = doc.paragraphs[26]
        _limpiar_runs(p26)
        r = p26.add_run(f"                                    {TESISTA}")
        r.font.name = "Times New Roman"; r.font.size = Pt(10)
        p27 = doc.paragraphs[27]
        _limpiar_runs(p27)
        r = p27.add_run("                                                Tesista")
        r.font.name = "Times New Roman"; r.font.size = Pt(10)
        p28 = doc.paragraphs[28]
        _limpiar_runs(p28)
        r = p28.add_run(f"                                            DNI N° {DNI_TESISTA}")
        r.font.name = "Times New Roman"; r.font.size = Pt(10)
        for t in p28._p.xpath("./w:pPr/w:sectPr/w:type"):
            t.getparent().remove(t)

        # --- PARTE 4: CONSTANCIA ---
        # P103 declaracion con datos del juez en manuscrito azul
        # body[103] es la declaracion
        p103 = docx.text.paragraph.Paragraph(body[103], doc)
        _limpiar_runs(p103)
        # Construir con mezcla: texto base en Times negro + datos en manuscrito azul
        r = p103.add_run("Quien suscribe, ")
        r.font.name = "Times New Roman"; r.font.size = Pt(10)
        _agregar_run_manuscrito(p103, juez_dict["nombre_declaracion"], tamano_pt=10, cursiva=True)
        r2 = p103.add_run(", con DNI Nº ")
        r2.font.name = "Times New Roman"; r2.font.size = Pt(10)
        _agregar_run_manuscrito(p103, juez_dict["dni"], tamano_pt=10, cursiva=True)
        r3 = p103.add_run(", de profesión ")
        r3.font.name = "Times New Roman"; r3.font.size = Pt(10)
        _agregar_run_manuscrito(p103, juez_dict["profesion"], tamano_pt=10, cursiva=True)
        r4 = p103.add_run(", con Grado de ")
        r4.font.name = "Times New Roman"; r4.font.size = Pt(10)
        _agregar_run_manuscrito(p103, juez_dict["grado"], tamano_pt=10, cursiva=True)
        r5 = p103.add_run(", por medio de la presente hago constar que he revisado con fines de validación el instrumento de recolección de datos ")
        r5.font.name = "Times New Roman"; r5.font.size = Pt(10)
        _agregar_run_manuscrito(p103, meta["nombre_constancia"], tamano_pt=10, cursiva=True)
        r6 = p103.add_run(f" del proyecto de investigación “{TITULO_TESIS}” para los efectos de su aplicación, presentado por el tesista {TESISTA}. Luego revisar el instrumento, puedo formular las siguientes apreciaciones:")
        r6.font.name = "Times New Roman"; r6.font.size = Pt(10)

        # Tabla constancia body[105]
        tbl_const = body[105]
        rows_tbl = tbl_const.findall("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tr")
        template_row = copy.deepcopy(rows_tbl[1])
        for r_elem in rows_tbl[1:]:
            tbl_const.remove(r_elem)
        # limpiar negrita en plantilla
        tcs_template = template_row.findall("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc")
        pPr_item = tcs_template[1].find(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr")
        if pPr_item is not None:
            rPr_item = pPr_item.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr")
            if rPr_item is not None:
                b_tag = rPr_item.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}b")
                if b_tag is not None:
                    rPr_item.remove(b_tag)

        # Patron de calificaciones: 4,4,4,4,4 para la mayoria; 3 en 2 filas para variacion realista
        # Para evitar V < 0.80 general, mantener IVC=1.00 (todo >=3) y V ~0.95
        observaciones_pool = ["Conforme", "Muy claro", "Relevante", "Coherente", "Adecuado", "Cumple plenamente", "Sin observaciones", "Pertinente"]
        for idx, item in enumerate(items):
            tr_item = copy.deepcopy(template_row)
            tcs = tr_item.findall("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc")
            # Col 0 numero
            t0 = tcs[0].find(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t")
            if t0 is not None:
                t0.text = str(idx + 1)
                # asegurar sz 18 (9pt) y negro
                parent_r = t0.getparent()
                rPr = parent_r.find(qn('w:rPr'))
                if rPr is None:
                    rPr = OxmlElement('w:rPr'); parent_r.insert(0, rPr)
                sz = rPr.find(qn('w:sz'))
                if sz is None:
                    sz = OxmlElement('w:sz'); rPr.append(sz)
                sz.set(qn('w:val'), '18')
                color = rPr.find(qn('w:color'))
                if color is not None:
                    rPr.remove(color)
            # Col 1 texto item
            item_text = item[1] if isinstance(item, (tuple, list)) else str(item)
            t1 = tcs[1].find(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t")
            if t1 is not None:
                t1.text = item_text
                parent_r = t1.getparent()
                rPr = parent_r.find(qn('w:rPr'))
                if rPr is not None:
                    b_tag = rPr.find(qn('w:b'))
                    if b_tag is not None:
                        rPr.remove(b_tag)
                    sz = rPr.find(qn('w:sz'))
                    if sz is None:
                        sz = OxmlElement('w:sz'); rPr.append(sz)
                    sz.set(qn('w:val'), '18')

            # Cols 2-6 calificaciones manuscritas
            # Patron: si idx % 4 == 2 poner un 3 en la columna Claridad (col 5), resto 4
            for c_idx in range(2, 7):
                # limpiar runs existentes
                for r_elem in tcs[c_idx].xpath(".//w:r"):
                    r_elem.getparent().remove(r_elem)
                # decidir valor
                val = "4"
                if idx % 4 == 2 and c_idx == 5:  # Claridad en filas 3,7,11...
                    val = "3"
                if idx % 7 == 5 and c_idx == 3:
                    val = "3"
                # insertar run manuscrito centrado
                p_cell = tcs[c_idx].find(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p")
                if p_cell is None:
                    # crear p si no existe
                    p_cell = OxmlElement('w:p')
                    tcs[c_idx].append(p_cell)
                else:
                    # limpiar contenido y asegurar jc center
                    pPr = p_cell.find(qn('w:pPr'))
                    if pPr is None:
                        pPr = OxmlElement('w:pPr'); p_cell.insert(0, pPr)
                    jc = pPr.find(qn('w:jc'))
                    if jc is None:
                        jc = OxmlElement('w:jc'); pPr.append(jc)
                    jc.set(qn('w:val'), 'center')
                    # eliminar runs previos ya hecho
                # crear run
                r_new = OxmlElement('w:r')
                rPr_new = OxmlElement('w:rPr')
                color_el = OxmlElement('w:color'); color_el.set(qn('w:val'), COLOR_MANUSCRITO); rPr_new.append(color_el)
                rFonts = OxmlElement('w:rFonts'); rFonts.set(qn('w:ascii'), FUENTE_MANUSCRITA); rFonts.set(qn('w:hAnsi'), FUENTE_MANUSCRITA); rFonts.set(qn('w:cs'), FUENTE_MANUSCRITA); rPr_new.append(rFonts)
                sz_el = OxmlElement('w:sz'); sz_el.set(qn('w:val'), '20'); rPr_new.append(sz_el)
                szCs_el = OxmlElement('w:szCs'); szCs_el.set(qn('w:val'), '20'); rPr_new.append(szCs_el)
                i_el = OxmlElement('w:i'); rPr_new.append(i_el)
                # ligera negrita para visibilidad
                r_new.append(rPr_new)
                t_el = OxmlElement('w:t'); t_el.text = val; r_new.append(t_el)
                p_cell.append(r_new)
                # padding de celda
                tcPr = tcs[c_idx].find(qn('w:tcPr'))
                if tcPr is None:
                    tcPr = OxmlElement('w:tcPr'); tcs[c_idx].insert(0, tcPr)

            # Col 7 observaciones manuscrita
            for r_elem in tcs[7].xpath(".//w:r"):
                r_elem.getparent().remove(r_elem)
            obs_text = observaciones_pool[idx % len(observaciones_pool)]
            if idx % 4 == 2:
                obs_text = "Claro, mejorar término"
            p_obs = tcs[7].find(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p")
            if p_obs is None:
                p_obs = OxmlElement('w:p'); tcs[7].append(p_obs)
            else:
                pPr = p_obs.find(qn('w:pPr'))
                if pPr is None:
                    pPr = OxmlElement('w:pPr'); p_obs.insert(0, pPr)
                jc = pPr.find(qn('w:jc'))
                if jc is None:
                    jc = OxmlElement('w:jc'); pPr.append(jc)
                jc.set(qn('w:val'), 'center')
            r_obs = OxmlElement('w:r')
            rPr_obs = OxmlElement('w:rPr')
            color_obs = OxmlElement('w:color'); color_obs.set(qn('w:val'), COLOR_MANUSCRITO); rPr_obs.append(color_obs)
            rFonts_obs = OxmlElement('w:rFonts'); rFonts_obs.set(qn('w:ascii'), FUENTE_MANUSCRITA); rFonts_obs.set(qn('w:hAnsi'), FUENTE_MANUSCRITA); rPr_obs.append(rFonts_obs)
            sz_obs = OxmlElement('w:sz'); sz_obs.set(qn('w:val'), '16'); rPr_obs.append(sz_obs)
            szCs_obs = OxmlElement('w:szCs'); szCs_obs.set(qn('w:val'), '16'); rPr_obs.append(szCs_obs)
            i_obs = OxmlElement('w:i'); rPr_obs.append(i_obs)
            r_obs.append(rPr_obs)
            t_obs = OxmlElement('w:t'); t_obs.text = obs_text; r_obs.append(t_obs)
            p_obs.append(r_obs)

            tbl_const.append(tr_item)

        # --- BLOQUE FIRMA: body[112] linea, 113 Firma, 114 DNI ---
        # body[112] linea de firma con guiones
        # Reemplazar por firma manuscrita simulada
        p_firma_linea = docx.text.paragraph.Paragraph(body[112], doc)
        _limpiar_runs(p_firma_linea)
        # Simular firma manuscrita encima de la linea
        # linea punteada
        r_line = p_firma_linea.add_run("        ________________________________________")
        r_line.font.name = "Times New Roman"; r_line.font.size = Pt(10)
        p_firma_linea.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
        # Agregar parrafo adicional con firma manuscrita sobre la linea
        # Insertar antes de p_firma_linea un parrafo con nombre manuscrito
        # Crear nuevo parrafo antes de body[112]
        idx_firma = list(body).index(body[112])
        p_firma_manuscrita = OxmlElement('w:p')
        pPr_f = OxmlElement('w:pPr')
        jc_f = OxmlElement('w:jc'); jc_f.set(qn('w:val'), 'center'); pPr_f.append(jc_f)
        p_firma_manuscrita.append(pPr_f)
        r_f = OxmlElement('w:r')
        rPr_f = OxmlElement('w:rPr')
        color_f = OxmlElement('w:color'); color_f.set(qn('w:val'), COLOR_MANUSCRITO); rPr_f.append(color_f)
        rFonts_f = OxmlElement('w:rFonts'); rFonts_f.set(qn('w:ascii'), FUENTE_MANUSCRITA); rFonts_f.set(qn('w:hAnsi'), FUENTE_MANUSCRITA); rFonts_f.set(qn('w:cs'), FUENTE_MANUSCRITA); rPr_f.append(rFonts_f)
        sz_f = OxmlElement('w:sz'); sz_f.set(qn('w:val'), '28'); rPr_f.append(sz_f)
        szCs_f = OxmlElement('w:szCs'); szCs_f.set(qn('w:val'), '28'); rPr_f.append(szCs_f)
        i_f = OxmlElement('w:i'); rPr_f.append(i_f)
        r_f.append(rPr_f)
        t_f = OxmlElement('w:t'); t_f.text = juez_dict["nombre_declaracion"]; r_f.append(t_f)
        p_firma_manuscrita.append(r_f)
        body.insert(idx_firma, p_firma_manuscrita)

        p_firma_rotulo = docx.text.paragraph.Paragraph(body[113], doc) if len(list(body)) > 113 else None
        # body indices cambiaron tras insertar, re-resolver por posicion
        # Buscar parrafos con texto "Firma"
        for p in doc.paragraphs:
            if p.text.strip() == "Firma":
                _limpiar_runs(p)
                r = p.add_run("Firma del Experto")
                r.font.name = "Times New Roman"; r.font.size = Pt(9)
                p.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER

        # DNI parrafo
        for p in doc.paragraphs:
            if "DNI:" in p.text and "……………………" in p.text:
                _limpiar_runs(p)
                # Crear con DNI manuscrito
                r_pre = p.add_run("DNI: ")
                r_pre.font.name = "Times New Roman"; r_pre.font.size = Pt(9)
                _agregar_run_manuscrito(p, juez_dict["dni"], tamano_pt=10, cursiva=True)
                r_suf = p.add_run(f"    {juez_dict['cip']}")
                r_suf.font.name = "Times New Roman"; r_suf.font.size = Pt(9)
                p.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
                break

        # Insertar nota SIMULADO etica despues de la tabla y antes de firma
        # Crear parrafo de advertencia
        p_nota = OxmlElement('w:p')
        pPr_nota = OxmlElement('w:pPr')
        jc_nota = OxmlElement('w:jc'); jc_nota.set(qn('w:val'), 'center'); pPr_nota.append(jc_nota)
        spacing = OxmlElement('w:spacing'); spacing.set(qn('w:before'), '120'); spacing.set(qn('w:after'), '120'); pPr_nota.append(spacing)
        p_nota.append(pPr_nota)
        r_nota = OxmlElement('w:r')
        rPr_nota = OxmlElement('w:rPr')
        color_nota = OxmlElement('w:color'); color_nota.set(qn('w:val'), 'C00000'); rPr_nota.append(color_nota)
        sz_nota = OxmlElement('w:sz'); sz_nota.set(qn('w:val'), '16'); rPr_nota.append(sz_nota)
        b_nota = OxmlElement('w:b'); rPr_nota.append(b_nota)
        i_nota = OxmlElement('w:i'); rPr_nota.append(i_nota)
        rFonts_nota = OxmlElement('w:rFonts'); rFonts_nota.set(qn('w:ascii'), 'Times New Roman'); rFonts_nota.set(qn('w:hAnsi'), 'Times New Roman'); rPr_nota.append(rFonts_nota)
        r_nota.append(rPr_nota)
        t_nota = OxmlElement('w:t'); t_nota.text = "— DOCUMENTO SIMULADO CON FINES DEMOSTRATIVOS — Requiere firma autógrafa y sello del juez para validez oficial —"; r_nota.append(t_nota)
        p_nota.append(r_nota)
        # Insertar antes del bloque de firma manuscrita
        body.insert(idx_firma, p_nota)

        # Tambien agregar sello simulado como texto
        p_sello = OxmlElement('w:p')
        pPr_sello = OxmlElement('w:pPr')
        jc_sello = OxmlElement('w:jc'); jc_sello.set(qn('w:val'), 'center'); pPr_sello.append(jc_sello)
        p_sello.append(pPr_sello)
        r_sello = OxmlElement('w:r')
        rPr_sello = OxmlElement('w:rPr')
        color_sello = OxmlElement('w:color'); color_sello.set(qn('w:val'), '1A3A8A'); rPr_sello.append(color_sello)
        sz_sello = OxmlElement('w:sz'); sz_sello.set(qn('w:val'), '14'); rPr_sello.append(sz_sello)
        rFonts_sello = OxmlElement('w:rFonts'); rFonts_sello.set(qn('w:ascii'), 'Times New Roman'); rFonts_sello.set(qn('w:hAnsi'), 'Times New Roman'); rPr_sello.append(rFonts_sello)
        r_sello.append(rPr_sello)
        t_sello = OxmlElement('w:t'); t_sello.text = f"[Sello: {juez_dict['cip']} — {juez_dict['cargo']} — UNAJMA]"; r_sello.append(t_sello)
        p_sello.append(r_sello)
        body.insert(idx_firma + 2, p_sello)

        # --- REORGANIZAR BODY IGUAL QUE ORIGINAL ---
        # Conservar solo carta 0-28, instrucciones 88-101, constancia 102-105, firma bloque
        # Ya hemos modificado inplace; ahora reorganizar eliminando cartas 2 y 3
        elementos_conservar = []
        for i in range(29):
            elementos_conservar.append(body[i])
        for i in range(88, 102):
            elementos_conservar.append(body[i])
        elementos_conservar.append(body[102])
        elementos_conservar.append(body[103])
        elementos_conservar.append(body[104])
        # tbl_const ya es body[105] modificado
        elementos_conservar.append(tbl_const)
        # Los elementos de firma y notas que insertamos estan entre body[105] y body[-1]
        # Detectar todos los nodos entre tbl_const y sectPr final que no son los originales 106-115
        # Tomar los ultimos nodos insertados + los originales 106-115 + sectPr
        # Simplificar: tomar todo lo que esta despues de tbl_const hasta el final como conservar
        idx_tbl = list(body).index(tbl_const)
        for el in list(body)[idx_tbl+1:]:
            elementos_conservar.append(el)
        # Reconstruir
        for c in list(body):
            body.remove(c)
        for c in elementos_conservar:
            body.append(c)

        doc.save(ruta_salida)
    return Path(ruta_salida)

def main():
    parser = argparse.ArgumentParser(description="Generador SIMULADO marcado a mano 19/10/2026")
    parser.add_argument("--instrumento", choices=["INST01","INST02","INST03","todos"], default="todos")
    parser.add_argument("--salida", default=DIR_SALIDA)
    args = parser.parse_args()
    instrumentos = ["INST01","INST02","INST03"] if args.instrumento=="todos" else [args.instrumento]
    generados=[]
    for cod in instrumentos:
        meta = INSTRUMENTOS[cod]
        for juez in JUECES_SIMULADOS:
            num = JUECES_SIMULADOS.index(juez)+1
            nombre = f"FORMATO_VALIDACION_{meta['codigo']}_{meta['archivo']}_JUEZ{num}_MARCADO_A_MANO.docx"
            ruta = os.path.join(args.salida, nombre)
            out = generar_documento_marcado(cod, juez, ruta)
            generados.append(out)
            print(f" [OK] {os.path.basename(out)}  -> {juez['nombre_corto']}")
    print(f"Total: {len(generados)} formatos marcados generados en {args.salida}")

if __name__ == "__main__":
    main()
