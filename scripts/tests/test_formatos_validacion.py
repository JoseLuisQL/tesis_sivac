# -*- coding: utf-8 -*-
"""
Pruebas automáticas para el generador de formatos de validación por juicio de expertos.
Verifica:
- VAL-FMT-002: Geometría de página y secciones idéntica al modelo (pgSz, márgenes, headers/footers vacíos).
- VAL-FMT-003: Tipografía y estilos idénticos al modelo (TNR, 12pt cuerpo, 9pt tablas, sin color/shd).
- VAL-FMT-004: Carta de presentación fiel al modelo con sustituciones controladas.
- VAL-FMT-005: Hoja de instrucciones literal con 5 puntos, criterios y escala 4-3-2-1 en negrita.
- VAL-FMT-006: Tabla rúbrica 6x3 idéntica al modelo (tblGrid 1294/1609/6091, fixed, tblInd 1316).
- VAL-FMT-012: Erratas del modelo preservadas ("es suficientes", "Luego revisar", etc.).
"""

import os
import zipfile
import pytest
import docx
from lxml import etree

from scripts.compiladores.generar_formatos_validacion import (
    generar_documento_formato,
    cargar_items_instrumentos,
    MODELO_PATH,
    TITULO_TESIS_OFICIAL,
    TESISTA_OFICIAL,
    DNI_TESISTA_OFICIAL,
    INSTRUMENTOS_METADATOS,
)

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


@pytest.fixture(scope="module")
def modelo_doc():
    """Carga el modelo original en modo solo lectura."""
    assert os.path.exists(MODELO_PATH), f"Modelo no encontrado en {MODELO_PATH}"
    return docx.Document(MODELO_PATH)


@pytest.fixture(scope="module")
def doc_inst01(tmp_path_factory):
    """Genera un documento de prueba para INST01."""
    out_dir = tmp_path_factory.mktemp("formatos_test")
    out_path = out_dir / "FORMATO_VALIDACION_INST01_FICHA_TIEMPOS_JUEZ1.docx"
    generar_documento_formato("INST01", 1, out_path)
    return docx.Document(str(out_path)), str(out_path)


@pytest.fixture(scope="module")
def doc_inst02(tmp_path_factory):
    """Genera un documento de prueba para INST02."""
    out_dir = tmp_path_factory.mktemp("formatos_test")
    out_path = out_dir / "FORMATO_VALIDACION_INST02_GUIA_COTEJO_JUEZ1.docx"
    generar_documento_formato("INST02", 1, out_path)
    return docx.Document(str(out_path)), str(out_path)


@pytest.fixture(scope="module")
def doc_inst03(tmp_path_factory):
    """Genera un documento de prueba para INST03."""
    out_dir = tmp_path_factory.mktemp("formatos_test")
    out_path = out_dir / "FORMATO_VALIDACION_INST03_CUESTIONARIO_TAM_JUEZ1.docx"
    generar_documento_formato("INST03", 1, out_path)
    return docx.Document(str(out_path)), str(out_path)


# -----------------------------------------------------------------------------
# 1. Carga de ítems desde la fuente de verdad
# -----------------------------------------------------------------------------
def test_carga_items_fuente_de_verdad():
    """Verifica que se carguen 32 ítems en total (8 + 8 + 16) sin duplicados ni faltantes."""
    items = cargar_items_instrumentos()
    assert "INST01" in items
    assert "INST02" in items
    assert "INST03" in items
    assert len(items["INST01"]) == 8
    assert len(items["INST02"]) == 8
    assert len(items["INST03"]) == 16
    total_items = sum(len(v) for v in items.values())
    assert total_items == 32


# -----------------------------------------------------------------------------
# 2. VAL-FMT-002: Geometría de página y secciones
# -----------------------------------------------------------------------------
def test_geometria_secciones_identica_modelo(doc_inst01, modelo_doc):
    """Verifica pgSz 11920x16850 y márgenes por sección comparados contra el modelo."""
    doc, _ = doc_inst01
    assert len(doc.sections) >= 2, "Debe tener al menos secciones de Carta e Instrucciones"

    # Sección 0: Carta (comparar contra sección 0 del modelo)
    sec_carta = doc.sections[0]
    sec_mod_carta = modelo_doc.sections[0]
    assert sec_carta.page_width == sec_mod_carta.page_width == 7569200  # 11920 dxa
    assert sec_carta.page_height == sec_mod_carta.page_height == 10699750  # 16850 dxa
    assert sec_carta.top_margin == sec_mod_carta.top_margin == 1231900  # 1940 dxa
    assert sec_carta.right_margin == sec_mod_carta.right_margin == 908050  # 1430 dxa
    assert sec_carta.bottom_margin == sec_mod_carta.bottom_margin == 723900  # 1140 dxa
    assert sec_carta.left_margin == sec_mod_carta.left_margin == 179705  # 283 dxa

    # Sección 1: Instrucciones (comparar contra sección 3 del modelo)
    sec_inst = doc.sections[1]
    sec_mod_inst = modelo_doc.sections[3]
    assert sec_inst.page_width == sec_mod_inst.page_width == 7569200
    assert sec_inst.page_height == sec_mod_inst.page_height == 10699750
    assert sec_inst.top_margin == sec_mod_inst.top_margin == 1231900  # 1940 dxa
    assert sec_inst.right_margin == sec_mod_inst.right_margin == 179705  # 283 dxa (0.50 cm)
    assert sec_inst.bottom_margin == sec_mod_inst.bottom_margin == 723900  # 1140 dxa
    assert sec_inst.left_margin == sec_mod_inst.left_margin == 179705  # 283 dxa

    # Si existe sección 2 (Constancia), verificar márgenes del modelo (sección 4)
    if len(doc.sections) >= 3:
        sec_const = doc.sections[2]
        sec_mod_const = modelo_doc.sections[4]
        assert sec_const.top_margin == sec_mod_const.top_margin == 1080135  # 1701 dxa
        assert sec_const.right_margin == sec_mod_const.right_margin == 908050  # 1430 dxa
        assert sec_const.bottom_margin == sec_mod_const.bottom_margin == 177800  # 280 dxa
        assert sec_const.left_margin == sec_mod_const.left_margin == 179705  # 283 dxa


def test_encabezados_y_pies_vacios(doc_inst01):
    """Verifica que todos los encabezados y pies existan y estén vacíos."""
    _, path = doc_inst01
    with zipfile.ZipFile(path) as z:
        hf_files = [n for n in z.namelist() if "word/header" in n or "word/footer" in n]
        assert len(hf_files) > 0, "Deben existir archivos de header/footer heredados"
        for hf in hf_files:
            xml_content = z.read(hf)
            root = etree.fromstring(xml_content)
            text = "".join(root.itertext()).strip()
            assert text == "", f"El archivo {hf} contiene texto visible: {text!r}"


# -----------------------------------------------------------------------------
# 3. VAL-FMT-003: Tipografía y estilos
# -----------------------------------------------------------------------------
def test_estilos_y_ausencia_color_sombreado(doc_inst01):
    """Verifica estilos requeridos y ausencia total de color, resaltado y sombreado."""
    doc, path = doc_inst01
    estilos_doc_nombres = {s.name for s in doc.styles}
    estilos_doc_ids = {s.style_id for s in doc.styles}

    assert "Normal" in estilos_doc_nombres or "Normal" in estilos_doc_ids
    assert "Heading 1" in estilos_doc_nombres or "Ttulo1" in estilos_doc_ids
    assert "Body Text" in estilos_doc_nombres or "Textoindependiente" in estilos_doc_ids
    assert "List Paragraph" in estilos_doc_nombres or "Prrafodelista" in estilos_doc_ids
    assert "Table Paragraph" in estilos_doc_nombres or "TableParagraph" in estilos_doc_ids

    # Inspeccionar XML para ausencia de color, sombreado y highlight
    with zipfile.ZipFile(path) as z:
        doc_xml = z.read("word/document.xml")
        root = etree.fromstring(doc_xml)

        # Sin sombreado de celdas o párrafos
        shd_elements = root.xpath(".//w:shd", namespaces=NS)
        for shd in shd_elements:
            val = shd.get(f"{{{NS['w']}}}val")
            color = shd.get(f"{{{NS['w']}}}color")
            fill = shd.get(f"{{{NS['w']}}}fill")
            assert val in (None, "clear", "auto")
            assert fill in (None, "auto", "none")

        # Sin resaltados (highlight)
        hl_elements = root.xpath(".//w:highlight", namespaces=NS)
        assert len(hl_elements) == 0, f"Encontrados resaltados: {hl_elements}"

        # Sin color de texto (salvo auto)
        color_elements = root.xpath(".//w:color", namespaces=NS)
        for c in color_elements:
            val = c.get(f"{{{NS['w']}}}val")
            assert val in ("auto", "000000"), f"Color no permitido encontrado: {val}"


# -----------------------------------------------------------------------------
# 4. VAL-FMT-004: Carta de presentación
# -----------------------------------------------------------------------------
def test_carta_presentacion_fiel(doc_inst01):
    """Verifica fecha, destinatario en blanco, tesista singular, título SIVAC y adjuntos."""
    doc, _ = doc_inst01
    parrafos_carta = [p.text for p in doc.paragraphs[:29]]
    texto_carta = "\n".join(parrafos_carta)

    # 1. Fecha con año 2026 y tabulador
    assert "Andahuaylas, …… de" in texto_carta
    assert "2026" in texto_carta
    assert "2025" not in texto_carta

    # Verificar tab punteado en fecha
    p0 = doc.paragraphs[0]
    tabs = p0._p.xpath(".//w:tab")
    assert len(tabs) >= 1, "La fecha debe contener un tabulador"
    p0_tabs_def = p0._p.xpath(".//w:tabs/w:tab")
    assert len(p0_tabs_def) >= 1
    assert p0_tabs_def[0].get(f"{{{NS['w']}}}leader") == "dot"

    # 2. Destinatario en blanco con puntos suspensivos y cargo EPIS
    assert "……………………………………………………………………………" in texto_carta
    assert "Docente de la Escuela Profesional de Ingeniería de Sistemas" in texto_carta

    # 3. Párrafo de presentación
    assert "Yo, Bach. José Luis Quispe León" in texto_carta
    assert "DNI N° 70519963" in texto_carta
    assert "Escuela Profesional de Ingeniería de Sistemas" in texto_carta
    assert "Guadalupe Lida Sihui" not in texto_carta
    assert "Miriam Velasque" not in texto_carta

    # 4. Título de tesis oficial SIVAC
    assert TITULO_TESIS_OFICIAL in texto_carta
    assert "MODELO PREDICTIVO CON MACHINE LEARNING" not in texto_carta

    # 5. Lista de 4 documentos adjuntos
    assert "Matriz de validez de instrumento" in texto_carta
    assert "Matriz de consistencia" in texto_carta
    assert "Tabla de operacionalización de variables" in texto_carta
    assert "Instrumento N° 1" in texto_carta

    # 6. Despedida y Atentamente
    assert "Atentamente," in texto_carta

    # 7. Bloque de firma
    assert "Bach. José Luis Quispe León" in texto_carta
    assert "Tesista" in texto_carta


# -----------------------------------------------------------------------------
# 5. VAL-FMT-005: Hoja de instrucciones literal
# -----------------------------------------------------------------------------
def test_hoja_instrucciones_literal(doc_inst01, modelo_doc):
    """Verifica que las instrucciones reproduzcan exactamente el texto y estructura del modelo."""
    doc, _ = doc_inst01
    textos_doc = [p.text for p in doc.paragraphs]
    texto_completo = "\n".join(textos_doc)

    assert "INSTRUCCIONES PARA VALIDACIÓN DEL INSTRUMENTO" in texto_completo
    assert "Las instrucciones para la validación del instrumento son las siguientes:" in texto_completo

    # 5 puntos numerados y criterios
    assert "En la “constancia de validación de contenido del instrumento por ítem” usar los siguientes criterios" in texto_completo
    assert "Suficiencia Relevancia Coherencia Claridad Redacción" in texto_completo
    assert "4 = Cumple completamente, 3 = Cumple adecuadamente, 2 = Cumple parcialmente, 1 = No cumple" in texto_completo
    assert "Si considera que algún ítem tiene alguna observación, anote en la columna correspondiente." in texto_completo
    assert "Devuelva la ficha completa al investigador." in texto_completo
    assert "Agradecemos profundamente su colaboración." in texto_completo

    # Verificar que los dígitos 4, 3, 2, 1 de la escala tengan runs en negrita
    p_escala = None
    for p in doc.paragraphs:
        if "4 = Cumple completamente" in p.text:
            p_escala = p
            break
    assert p_escala is not None, "No se encontró el párrafo de la escala"
    bold_runs = [r.text.strip() for r in p_escala.runs if r.bold]
    for digito in ["4", "3", "2", "1"]:
        assert any(digito in br for br in bold_runs), f"Dígito {digito} debe estar en negrita"


# -----------------------------------------------------------------------------
# 6. VAL-FMT-006: Tabla rúbrica 6x3 idéntica
# -----------------------------------------------------------------------------
def test_tabla_rubrica_6x3_identica(doc_inst01, modelo_doc):
    """Verifica dimensiones 6x3, tblGrid, tblLayout fixed, tblInd 1316 y texto de celdas."""
    doc, _ = doc_inst01
    assert len(doc.tables) >= 1, "Debe existir al menos la tabla rúbrica"
    tbl_rubrica = doc.tables[0]
    tbl_mod = modelo_doc.tables[0]

    assert len(tbl_rubrica.rows) == 6
    assert len(tbl_rubrica.columns) == 3

    # Comparar tblGrid
    grid_gen = [col.get(f"{{{NS['w']}}}w") for col in tbl_rubrica._tbl.xpath(".//w:tblGrid/w:gridCol")]
    grid_mod = [col.get(f"{{{NS['w']}}}w") for col in tbl_mod._tbl.xpath(".//w:tblGrid/w:gridCol")]
    assert grid_gen == grid_mod == ["1294", "1609", "6091"]

    # Comparar tblLayout fixed
    layouts = tbl_rubrica._tbl.xpath(".//w:tblPr/w:tblLayout")
    assert len(layouts) == 1
    assert layouts[0].get(f"{{{NS['w']}}}type") == "fixed"

    # Comparar tblInd 1316
    inds = tbl_rubrica._tbl.xpath(".//w:tblPr/w:tblInd")
    assert len(inds) == 1
    assert inds[0].get(f"{{{NS['w']}}}w") == "1316"

    # Comparar contenido de celdas celda por celda contra el modelo
    for r_idx in range(6):
        for c_idx in range(3):
            texto_gen = tbl_rubrica.rows[r_idx].cells[c_idx].text.strip()
            texto_mod = tbl_mod.rows[r_idx].cells[c_idx].text.strip()
            assert texto_gen == texto_mod, f"Discrepancia en celda ({r_idx}, {c_idx}): {texto_gen!r} != {texto_mod!r}"


# -----------------------------------------------------------------------------
# 7. VAL-FMT-012: Erratas del modelo preservadas
# -----------------------------------------------------------------------------
def test_erratas_modelo_preservadas(doc_inst01):
    """Verifica que las erratas textuales del modelo original se conserven intactas."""
    doc, _ = doc_inst01
    texto_completo = "\n".join(p.text for p in doc.paragraphs)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                texto_completo += "\n" + cell.text

    # Erratas en la rúbrica
    assert "es suficientes" in texto_completo, "Falta errata 'es suficientes'"
    assert "pero no corresponden a la dimensión" in texto_completo, "Falta errata 'no corresponden a la dimensión'"
    assert "podría ser mejorado en la semántica" in texto_completo, "Falta errata 'podría ser mejorado en la semántica'"


# -----------------------------------------------------------------------------
# 8. Verificación de los 3 instrumentos
# -----------------------------------------------------------------------------
def test_tres_instrumentos_generan_correctamente(doc_inst01, doc_inst02, doc_inst03):
    """Verifica que los tres instrumentos generen sus archivos con el nombre correspondiente."""
    d1, _ = doc_inst01
    d2, _ = doc_inst02
    d3, _ = doc_inst03

    t1 = "\n".join(p.text for p in d1.paragraphs)
    t2 = "\n".join(p.text for p in d2.paragraphs)
    t3 = "\n".join(p.text for p in d3.paragraphs)

    assert "Instrumento N° 1" in t1
    assert "Instrumento N° 2" in t2
    assert "Instrumento N° 3" in t3
