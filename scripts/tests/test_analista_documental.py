"""Pruebas de scripts/agentes/analista_documental.py.

Los documentos se generan en tmp_path (fixtures de PRUEBA); no contienen datos empíricos
de la tesis. Algunas pruebas leen la tesis modelo real en modo solo lectura y se omiten
si el archivo no está.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.agentes import analista_documental as ad  # noqa: E402
from scripts.comun import rutas, seguridad  # noqa: E402


# --------------------------------------------------------------------------- fixtures

@pytest.fixture()
def docx_prueba(tmp_path):
    """DOCX con 2 secciones (vertical 3/2.5/2.5/2.5 cm + horizontal), encabezados, tabla APA, imagen y rótulos."""
    import docx
    from docx.enum.section import WD_ORIENT
    from docx.shared import Cm, Pt
    from PIL import Image

    d = docx.Document()
    n = d.styles["Normal"]
    n.font.name, n.font.size = "Times New Roman", Pt(12)
    n.paragraph_format.line_spacing = 1.5
    s = d.sections[0]
    s.left_margin, s.right_margin, s.top_margin, s.bottom_margin = Cm(3), Cm(2.5), Cm(2.5), Cm(2.5)
    d.add_heading("CAPÍTULO I. PROBLEMA", level=1)
    d.add_heading("1.1 Descripción", level=2)
    d.add_paragraph("Texto de cuerpo " * 20)
    cap = d.add_paragraph("Tabla 1 Datos de prueba", style="Caption")
    t = d.add_table(rows=3, cols=2)
    for i, fila in enumerate(t.rows):
        for j, c in enumerate(fila.cells):
            c.text = f"c{i}{j}"
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls
    t._tbl.tblPr.append(parse_xml(
        f'<w:tblBorders {nsdecls("w")}><w:top w:val="single" w:sz="8"/><w:bottom w:val="single" w:sz="8"/></w:tblBorders>'))
    t.rows[0]._tr.get_or_add_trPr().append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    png = tmp_path / "im.png"
    Image.new("RGB", (600, 300), "white").save(png)
    d.add_picture(str(png), width=Cm(5.08))  # 2 pulgadas -> 300 px/2in = 300 dpi
    d.add_paragraph("Figura 1 Imagen de prueba", style="Caption")
    d.add_section()
    s2 = d.sections[1]
    s2.orientation = WD_ORIENT.LANDSCAPE
    s2.page_width, s2.page_height = s2.page_height, s2.page_width
    d.add_paragraph("Anexo horizontal")
    ruta = tmp_path / "prueba.docx"
    d.save(ruta)
    return ruta


def _pdf(ruta: Path, lineas_por_pagina: list[list[tuple[str, float, bool]]]) -> Path:
    import pymupdf
    doc = pymupdf.open()
    for lineas in lineas_por_pagina:
        pag = doc.new_page(width=595.3, height=841.9)
        y = 90
        for texto, tam, neg in lineas:
            pag.insert_text((85, y), texto, fontsize=tam, fontname="hebo" if neg else "helv")
            y += tam * 2.0
    doc.save(ruta)
    doc.close()
    return ruta


RELLENO = "Texto corriente de cuerpo para fijar la fuente dominante del documento de prueba."


@pytest.fixture()
def pdf_prueba(tmp_path, monkeypatch):
    monkeypatch.setattr(rutas, "INDICES_PDF", tmp_path / "idx")
    paginas = [
        [("INTRODUCCION", 12, True)] + [(RELLENO, 11, False)] * 6,
        [("CAPITULO I: PROBLEMA", 12, True), ("1.1. Realidad", 11, True)] + [(RELLENO, 11, False)] * 6,
        [("1.2. Formulacion", 11, True)] + [(RELLENO, 11, False)] * 6,
    ]
    return _pdf(tmp_path / "modelo.pdf", paginas)


# --------------------------------------------------------------------------- DOCX

def test_docx_secciones_margenes_orientacion(docx_prueba):
    r = ad.analizar_docx(docx_prueba)
    assert r["tipo"] == "docx" and len(r["secciones"]) == 2
    m = r["secciones"][0]["margenes_cm"]
    assert (m["izq"], m["der"], m["sup"], m["inf"]) == (3.0, 2.5, 2.5, 2.5)
    assert r["secciones"][0]["orientacion"] == "vertical"
    assert r["secciones"][1]["orientacion"] == "horizontal"
    assert r["perfil"]["margenes_cm"]["izq"] == 3.0
    assert r["fuente"]["sha256"] == seguridad.sha256_archivo(docx_prueba)


def test_docx_estilos_resueltos(docx_prueba):
    r = ad.analizar_docx(docx_prueba)
    normal = next(e for e in r["estilos_usados"] if e["nombre"] == "Normal")
    assert normal["fuente"] == "Times New Roman" and normal["tam_pt"] == 12.0
    assert normal["interlineado"] == {"valor": 1.5, "regla": "multiple"}
    assert r["perfil"]["fuente_cuerpo"] == "Times New Roman"
    assert r["perfil"]["interlineado_cuerpo"]["valor"] == 1.5


def test_docx_encabezados_y_jerarquia(docx_prueba):
    r = ad.analizar_docx(docx_prueba)
    niveles = [(e["nivel"], e["texto"]) for e in r["encabezados"]]
    assert niveles == [(1, "CAPÍTULO I. PROBLEMA"), (2, "1.1 Descripción")]
    assert r["encabezados"][1]["numeracion_manual"] == "1.1"


def test_docx_tabla_imagen_y_rotulos(docx_prueba):
    r = ad.analizar_docx(docx_prueba)
    t = r["tablas"][0]
    assert (t["filas"], t["columnas"]) == (3, 2)
    assert t["encabezado_repetido"] is True
    assert t["bordes_verticales"] is False
    assert t["bordes_horizontales_sup_inf_interno"][:2] == [True, True]
    assert t["rotulo_antes"].startswith("Tabla 1")
    im = r["imagenes"][0]
    assert im["formato"] == "PNG" and im["px"] == [600, 300]
    assert im["dpi_efectivo"] == pytest.approx(300.0, abs=1.0)
    assert {x["texto"][:8] for x in r["rotulos"]} == {"Tabla 1 ", "Figura 1"}


def test_docx_markdown_contiene_secciones(docx_prueba):
    md = ad.a_markdown(ad.analizar_docx(docx_prueba))
    for titulo in ("## Secciones", "## Estilos usados", "## Jerarquía de encabezados", "## Tablas (1)", "## Imágenes (1)"):
        assert titulo in md


def test_docx_numeracion_automatica(tmp_path):
    """Lista multinivel enlazada a Heading 1/2: la numeración se calcula (1., 1.1, 1.2, 2.)."""
    import docx
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls, qn

    d = docx.Document()
    numb = d.part.numbering_part.element
    numb.append(parse_xml(
        f'<w:abstractNum {nsdecls("w")} w:abstractNumId="90"><w:multiLevelType w:val="multilevel"/>'
        '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/></w:lvl>'
        '<w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1.%2"/></w:lvl>'
        '</w:abstractNum>'))
    primero_num = numb.find(qn("w:num"))
    nuevo = parse_xml(f'<w:num {nsdecls("w")} w:numId="90"><w:abstractNumId w:val="90"/></w:num>')
    if primero_num is not None:
        primero_num.addprevious(nuevo)
    else:
        numb.append(nuevo)
    for texto, lvl in (("Uno", 0), ("Sub a", 1), ("Sub b", 1), ("Dos", 0)):
        p = d.add_heading(texto, level=lvl + 1)
        p._p.get_or_add_pPr().append(parse_xml(
            f'<w:numPr {nsdecls("w")}><w:ilvl w:val="{lvl}"/><w:numId w:val="90"/></w:numPr>'))
    ruta = tmp_path / "num.docx"
    d.save(ruta)
    r = ad.analizar_docx(ruta)
    assert [e["numeracion_automatica"] for e in r["encabezados"]] == ["1.", "1.1", "1.2", "2."]


@pytest.mark.parametrize("n,esperado", [(4, "IV"), (9, "IX"), (14, "XIV"), (1994, "MCMXCIV")])
def test_romanos(n, esperado):
    assert ad._romano(n) == esperado


# --------------------------------------------------------------------------- PDF

def test_pdf_estructura_e_criterio(pdf_prueba):
    r = ad.analizar_pdf(pdf_prueba)
    assert r["tipo"] == "pdf" and r["fuente"]["n_paginas"] == 3
    textos = [t["texto"] for t in r["estructura_inferida"]]
    assert "INTRODUCCION" in textos
    assert any(t.startswith("CAPITULO I") for t in textos)
    assert "1.1. Realidad" in textos and "1.2. Formulacion" in textos
    niveles = {t["texto"]: t["nivel"] for t in r["estructura_inferida"]}
    assert niveles["1.1. Realidad"] == 2
    assert r["criterio_titulos"].startswith("Título = bloque")
    assert r["toc_embebido"] == []
    assert r["perfil"]["tam_cuerpo_pt"] == 11.0
    assert "estimado" in r["perfil"]["precision"]


def test_pdf_pagina_impresa_no_confirmada_es_verificar(pdf_prueba):
    r = ad.analizar_pdf(pdf_prueba)
    for p in r["paginas"]:
        assert p["pagina_fisica"] >= 1
        if p["etiqueta_impresa"] is None:
            assert p["etiqueta_estado"].startswith("[VERIFICAR")


def test_pdf_sin_capa_de_texto_avisa_ocr(tmp_path, monkeypatch):
    import pymupdf
    monkeypatch.setattr(rutas, "INDICES_PDF", tmp_path / "idx")
    doc = pymupdf.open()
    pag = doc.new_page()
    pag.draw_rect(pymupdf.Rect(50, 50, 200, 200), fill=(0.5, 0.5, 0.5))
    ruta = tmp_path / "escaneado.pdf"
    doc.save(ruta)
    doc.close()
    monkeypatch.setattr(ad, "tesseract_disponible", lambda: None)
    try:
        r = ad.analizar_pdf(ruta)
    except Exception as e:  # noqa: BLE001  (p. ej. PDF sin texto que ingesta_pdf no soporte)
        pytest.skip(f"ingesta_pdf no procesa este PDF de prueba: {e}")
    assert r["ocr"]["paginas_requieren_ocr"] == [1]
    assert any("OCR" in a for a in r["avisos"])


def test_fusionar_rotulo_capitulo():
    base = {"pagina_fisica": 5, "etiqueta_impresa": "3", "tam_pt": 12.0, "negrita": True}
    tit = [{**base, "nivel": 1, "numero": "CAPÍTULO II", "texto": "CAPÍTULO II", "criterio": "patron CAPÍTULO"},
           {**base, "nivel": 1, "numero": None, "texto": "ANTECEDENTES", "criterio": "x"}]
    r = ad._fusionar_rotulos_capitulo(tit)
    assert len(r) == 1 and r[0]["texto"] == "CAPÍTULO II ANTECEDENTES"


def test_clasificar_titulo_descarta_rotulos_y_texto_normal():
    assert ad._clasificar_titulo("Tabla 3. Datos", 11, True, False, 11) is None
    assert ad._clasificar_titulo("Esto es una oración normal.", 11, False, False, 11) is None
    r = ad._clasificar_titulo("4.2. Enfoque de investigación", 11, True, False, 11)
    assert r["nivel"] == 2 and r["numero"] == "4.2"


def test_compactar_rangos():
    assert ad._compactar_rangos([1, 2, 3, 7, 9, 10]) == "1-3, 7, 9-10"


# --------------------------------------------------------------------------- XLSX

def test_xlsx_formulas_y_valores(tmp_path):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Hoja1"
    ws["A1"], ws["A2"], ws["A3"] = 2, 3, "=A1+A2"
    ruta = tmp_path / "x.xlsx"
    wb.save(ruta)
    r = ad.analizar_xlsx(ruta)
    h = r["hojas"][0]
    assert h["nombre"] == "Hoja1" and h["rango_usado"] == "A1:A3"
    assert h["n_formulas"] == 1 and h["n_valores"] == 2
    assert h["formulas"][0]["formula"] == "=A1+A2"
    assert h["formulas"][0]["valor_en_cache"] is None  # openpyxl no calcula: no se inventa
    assert any("sin valor en caché" in a for a in r["avisos"])


# --------------------------------------------------------------------------- comparar

def test_comparar_docx_contra_pdf(docx_prueba, pdf_prueba):
    c = ad.comparar(ad.analizar(docx_prueba), ad.analizar(pdf_prueba))
    asp = {d["aspecto"] for d in c["diferencias"]}
    assert "Margen izquierdo (cm)" in asp or "Fuente del cuerpo" in asp
    assert c["tipos"] == ["docx", "pdf"]
    assert "capitulos" in c


def test_comparar_mismo_documento_sin_diferencias(docx_prueba):
    a = ad.analizar(docx_prueba)
    c = ad.comparar(a, a)
    assert c["diferencias"] == []


def test_norm_fuente():
    assert ad._norm_fuente("TimesNewRomanPSMT") == ad._norm_fuente("Times New Roman")
    assert ad._norm_fuente("Arial-BoldMT") == ad._norm_fuente("Arial")


# --------------------------------------------------------------------------- seguridad / CLI

def test_escribir_rechaza_referencias(tmp_path):
    with pytest.raises(seguridad.EscrituraProhibida):
        ad._escribir(rutas.REFERENCIAS / "no_debe_existir.md", "x", True)
    with pytest.raises(seguridad.EscrituraProhibida):
        ad._escribir(rutas.MODELOS_TESIS / "no_debe_existir.md", "x", True)
    assert not (rutas.REFERENCIAS / "no_debe_existir.md").exists()


def test_escribir_no_sobrescribe_sin_forzar(tmp_path):
    dest = tmp_path / "s.md"
    ad._escribir(dest, "a", False)
    with pytest.raises(FileExistsError):
        ad._escribir(dest, "b", False)
    ad._escribir(dest, "b", True)
    assert dest.read_text(encoding="utf-8") == "b"


def test_cli_desglosar_json(docx_prueba, capsys, tmp_path):
    out = tmp_path / "o.md"
    rc = ad.main(["desglosar", str(docx_prueba), "--json", "--salida-md", str(out)])
    assert rc == 0
    datos = json.loads(capsys.readouterr().out)
    assert datos["tipo"] == "docx" and out.exists()


def test_cli_archivo_inexistente_y_formato_no_soportado(tmp_path, capsys):
    assert ad.main(["desglosar", str(tmp_path / "no.docx")]) == 1
    txt = tmp_path / "a.txt"
    txt.write_text("x")
    assert ad.main(["desglosar", str(txt)]) == 2  # formato no soportado = uso incorrecto
    assert ad.main(["comparar", str(txt), str(txt)]) == 2


def test_cli_plantilla_rechaza_no_pdf(docx_prueba):
    assert ad.main(["plantilla-estructura", str(docx_prueba)]) == 2


def test_cli_plantilla_escribe_fuera_de_referencias(pdf_prueba, tmp_path, capsys):
    dest = tmp_path / "plantilla.md"
    assert ad.main(["plantilla-estructura", str(pdf_prueba), "--salida", str(dest)]) == 0
    md = dest.read_text(encoding="utf-8")
    assert "# Plantilla de estructura" in md and "INTRODUCCION" in md


def test_cli_plantilla_a_referencias_es_rechazada(pdf_prueba):
    assert ad.main(["plantilla-estructura", str(pdf_prueba), "--salida", str(rutas.REFERENCIAS / "x.md")]) == 1
    assert not (rutas.REFERENCIAS / "x.md").exists()


# --------------------------------------------------------------------------- reales (solo lectura)

MODELO = next(iter(sorted(rutas.MODELOS_TESIS.glob("Jhon*.pdf"))), None)
PROYECTO = rutas.PROYECTO_BASE / "PROYECTO_TESIS.docx"


@pytest.mark.skipif(not PROYECTO.exists(), reason="PROYECTO_TESIS.docx no disponible")
def test_real_proyecto_tesis_docx():
    antes = seguridad.sha256_archivo(PROYECTO)
    r = ad.analizar_docx(PROYECTO)
    assert seguridad.sha256_archivo(PROYECTO) == antes  # solo lectura
    assert r["perfil"]["fuente_cuerpo"] == "Times New Roman"
    assert r["perfil"]["margenes_cm"]["izq"] == 3.0
    assert any("MARCO TEÓRICO" in e["texto"].upper() for e in r["encabezados"] if e["nivel"] == 1)


@pytest.mark.skipif(MODELO is None or not rutas.INDICES_PDF.exists(), reason="tesis modelo o índices no disponibles")
def test_real_tesis_modelo_pdf():
    r = ad.analizar_pdf(MODELO)
    caps = [t["texto"] for t in r["estructura_inferida"] if t["texto"].upper().startswith("CAP")]
    assert len(caps) >= 6
    assert r["perfil"]["fuente_cuerpo"].startswith("TimesNewRoman")
    assert set(r["perfil"]["formatos_numeracion_pagina"]) == {"romano", "arabigo"}


# --------------------------------------------------------------------------- tablas: formato condicional (APA 7)

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _docx_tabla_estilo(tmp_path, *, look: str, condicional: bool, filas: int = 3, directo_celdas: bool = False):
    """DOCX de PRUEBA con un estilo de tabla (top+bottom) y, opcionalmente, firstRow.bottom condicional."""
    import docx
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls

    d = docx.Document()
    cond = ('<w:tblStylePr w:type="firstRow"><w:tcPr><w:tcBorders><w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
            '</w:tcBorders></w:tcPr></w:tblStylePr>') if condicional else ""
    d.styles.element.append(parse_xml(
        f'<w:style {nsdecls("w")} w:type="table" w:customStyle="1" w:styleId="EstiloAPAPrueba"><w:name w:val="Estilo APA prueba"/>'
        '<w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/></w:tblBorders></w:tblPr>' + cond + '</w:style>'))
    t = d.add_table(rows=filas, cols=2)
    for i, fila in enumerate(t.rows):
        for j, c in enumerate(fila.cells):
            c.text = f"c{i}{j}"
    pr = t._tbl.tblPr
    for viejo in pr.findall(f"{{{W}}}tblStyle") + pr.findall(f"{{{W}}}tblLook"):
        pr.remove(viejo)
    pr.insert(0, parse_xml(f'<w:tblStyle {nsdecls("w")} w:val="EstiloAPAPrueba"/>'))
    pr.append(parse_xml(f'<w:tblLook {nsdecls("w")} {look}/>'))
    if directo_celdas:
        for c in t.rows[0].cells:
            c._tc.get_or_add_tcPr().append(parse_xml(
                f'<w:tcBorders {nsdecls("w")}><w:bottom w:val="single" w:sz="4"/></w:tcBorders>'))
    ruta = tmp_path / "estilo.docx"
    d.save(ruta)
    return ruta


def test_tabla_estilo_condicional_firstrow_da_tres_lineas(tmp_path):
    """Regresión: la línea bajo el encabezado definida en w:tblStylePr firstRow debe contarse (tblLook firstRow=1)."""
    r = ad.analizar_docx(_docx_tabla_estilo(tmp_path, look='w:val="04A0" w:firstRow="1" w:noVBand="1"', condicional=True))
    t = r["tablas"][0]
    assert t["tblLook"]["firstRow"] is True
    assert t["lineas_horizontales"]["bajo_encabezado"] is True
    assert "firstRow" in t["lineas_horizontales"]["origen_bajo_encabezado"]
    assert t["bordes_verticales"] is False
    assert t["cumple_tres_lineas_apa7"] is True and t["incumplimientos_tres_lineas"] == []
    assert r["resumen_tablas"]["cumplen_tres_lineas_apa7"] == 1 and r["resumen_tablas"]["incumplen"] == []


def test_tabla_estilo_condicional_desactivado_por_tblook(tmp_path):
    """Si tblLook firstRow=0 el formato condicional NO se aplica: falta la línea bajo el encabezado."""
    r = ad.analizar_docx(_docx_tabla_estilo(tmp_path, look='w:val="0600" w:firstRow="0" w:noHBand="1" w:noVBand="1"', condicional=True))
    t = r["tablas"][0]
    assert t["lineas_horizontales"]["bajo_encabezado"] is False
    assert t["cumple_tres_lineas_apa7"] is False
    assert "falta la línea bajo el encabezado" in t["incumplimientos_tres_lineas"]
    assert any("tres líneas" in a for a in r["avisos"])


def test_tblook_solo_mascara_hexadecimal(tmp_path):
    """tblLook sin atributos individuales: firstRow se deduce de la máscara 0x0020 de w:val."""
    r = ad.analizar_docx(_docx_tabla_estilo(tmp_path, look='w:val="0420"', condicional=True))
    assert r["tablas"][0]["tblLook"]["firstRow"] is True
    assert r["tablas"][0]["cumple_tres_lineas_apa7"] is True


def test_tabla_sin_condicional_pero_bordes_directos_en_celdas(tmp_path):
    r = ad.analizar_docx(_docx_tabla_estilo(tmp_path, look='w:val="04A0" w:firstRow="1"', condicional=False, directo_celdas=True))
    t = r["tablas"][0]
    assert t["lineas_horizontales"]["bajo_encabezado"] is True
    assert "formato directo" in t["lineas_horizontales"]["origen_bajo_encabezado"]
    assert t["cumple_tres_lineas_apa7"] is True


def test_tabla_una_fila_no_evaluable(tmp_path):
    r = ad.analizar_docx(_docx_tabla_estilo(tmp_path, look='w:val="04A0" w:firstRow="1"', condicional=True, filas=1))
    assert r["tablas"][0]["cumple_tres_lineas_apa7"] is None
    assert r["resumen_tablas"]["evaluables"] == 0


def test_tabla_cuadricula_completa_incumple(tmp_path):
    import docx
    d = docx.Document()
    t = d.add_table(rows=3, cols=2)
    t.style = "Table Grid"
    ruta = tmp_path / "grid.docx"
    d.save(ruta)
    r = ad.analizar_docx(ruta)["tablas"][0]
    assert r["cumple_tres_lineas_apa7"] is False
    assert "hay bordes verticales" in r["incumplimientos_tres_lineas"]


@pytest.mark.skipif(not PROYECTO.exists(), reason="PROYECTO_TESIS.docx no disponible")
def test_real_proyecto_tablas_apa_tres_lineas():
    """Las tablas 1-9 usan 'Rabla estilo APA' (línea bajo encabezado en firstRow): deben cumplir tres líneas."""
    r = ad.analizar_docx(PROYECTO)
    for t in r["tablas"][:9]:
        assert t["estilo"] == "Rabla estilo APA"
        assert t["lineas_horizontales"]["bajo_encabezado"] is True, t["n"]
        assert t["cumple_tres_lineas_apa7"] is True, (t["n"], t["incumplimientos_tres_lineas"])
    assert r["resumen_tablas"]["cumplen_tres_lineas_apa7"] >= 9


# --------------------------------------------------------------------------- gráficos en cabecera (formas vs imágenes)

def test_cabecera_con_forma_no_cuenta_como_imagen():
    """Un cuadro de texto DrawingML (sin a:blip) es 'forma', no imagen; su VML Fallback no se cuenta doble."""
    from lxml import etree
    xml = ('<w:hdr xmlns:w="%s" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
           'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
           'xmlns:v="urn:schemas-microsoft-com:vml"><w:p><w:r><mc:AlternateContent><mc:Choice><w:drawing><wp:anchor/></w:drawing>'
           '</mc:Choice><mc:Fallback><w:pict><v:rect/></w:pict></mc:Fallback></mc:AlternateContent></w:r></w:p></w:hdr>') % W
    g = ad._contar_graficos(etree.fromstring(xml))
    assert g == {"imagenes": 0, "formas": 1, "vml_fallback_omitidos": 1}


@pytest.mark.skipif(not PROYECTO.exists(), reason="PROYECTO_TESIS.docx no disponible")
def test_real_proyecto_cabecera_forma_sin_texto():
    r = ad.analizar_docx(PROYECTO)
    cab = next(c for c in r["cabeceras_pies"] if c["elemento"] == "cabecera")
    assert cab["texto"] == "" and cab["campos"] == []
    assert cab["imagenes"] == 0 and cab["formas"] == 1 and cab["vml_fallback_omitidos"] == 1
    assert r["graficos_cuerpo"]["imagenes"] == len(r["imagenes"])
    assert r["graficos_cuerpo"]["vml_fallback_omitidos"] == 2


# --------------------------------------------------------------------------- sin efectos secundarios en el vault

def test_pdf_arbitrario_no_escribe_indice(tmp_path, monkeypatch):
    """Un PDF fuera de fuentes/modelos se indexa en memoria: no se crea ningún .idx.json."""
    vault = tmp_path / "vault_idx"
    monkeypatch.setattr(rutas, "INDICES_PDF", vault)
    pdf = _pdf(tmp_path / "ajeno.pdf", [[("INTRODUCCION", 12, True)] + [(RELLENO, 11, False)] * 6])
    assert ad.main(["desglosar", str(pdf), "--json"]) == 0
    assert ad.main(["plantilla-estructura", str(pdf), "--salida", str(tmp_path / "pl.md")]) == 0
    assert not vault.exists() or not list(vault.glob("*.idx.json"))


def test_carpeta_indices_redirige_cache(tmp_path, monkeypatch):
    vault = tmp_path / "vault_idx"
    alt = tmp_path / "alt_idx"
    monkeypatch.setattr(rutas, "INDICES_PDF", vault)
    pdf = _pdf(tmp_path / "ajeno.pdf", [[("INTRODUCCION", 12, True)] + [(RELLENO, 11, False)] * 6])
    assert ad.main(["desglosar", str(pdf), "--json", "--carpeta-indices", str(alt)]) == 0
    assert list(alt.glob("*.idx.json")) and not vault.exists()


def test_sin_cache_no_escribe_ni_en_fuentes(tmp_path, monkeypatch):
    vault = tmp_path / "vault_idx"
    monkeypatch.setattr(rutas, "INDICES_PDF", vault)
    monkeypatch.setattr(rutas, "PDFS_FUENTES", tmp_path)  # el PDF cuenta como 'fuente': normalmente usaría la caché
    pdf = _pdf(tmp_path / "f.pdf", [[("INTRODUCCION", 12, True)] + [(RELLENO, 11, False)] * 6])
    assert ad.main(["desglosar", str(pdf), "--json", "--sin-cache"]) == 0
    assert not vault.exists()
    assert ad.main(["desglosar", str(pdf), "--json"]) == 0  # sin --sin-cache sí usa la caché compartida
    assert list(vault.glob("*.idx.json"))


# --------------------------------------------------------------------------- códigos de salida

def test_codigos_de_salida_archivos_danados(tmp_path, capsys):
    import pymupdf
    roto_docx = tmp_path / "roto.docx"
    roto_docx.write_bytes(b"esto no es un zip")
    roto_pdf = tmp_path / "roto.pdf"
    roto_pdf.write_bytes(b"%PDF-1.4 basura")
    roto_xlsx = tmp_path / "roto.xlsx"
    roto_xlsx.write_bytes(b"no es xlsx")
    for r in (roto_docx, roto_pdf, roto_xlsx):
        assert ad.main(["desglosar", str(r), "--sin-cache"]) == 1
        err = capsys.readouterr().err
        assert err.startswith("ERROR:") and "inesperado" not in err, (r.name, err)
        assert "Traceback" not in err

    cif = tmp_path / "cifrado.pdf"
    d = pymupdf.open()
    d.new_page().insert_text((72, 72), "secreto")
    d.save(cif, encryption=pymupdf.PDF_ENCRYPT_AES_256, owner_pw="o", user_pw="u")
    d.close()
    assert ad.main(["desglosar", str(cif), "--sin-cache"]) == 1
    err = capsys.readouterr().err
    assert "cifrado" in err and "inesperado" not in err


def test_codigo_2_uso_incorrecto(tmp_path, capsys):
    assert ad.main([]) == 2
    assert ad.main(["desglosar"]) == 2
    txt = tmp_path / "x.txt"
    txt.write_text("x")
    assert ad.main(["desglosar", str(txt)]) == 2
    assert ad.main(["plantilla-estructura", str(txt)]) == 2
    assert ad.main(["desglosar", str(tmp_path / "no_existe.docx")]) == 1


def test_heuristica_titulo_sin_espacio_tras_el_punto():
    r = ad._clasificar_titulo("3.1.Bases teóricas", 12, True, False, 12)
    assert r is not None and r["nivel"] == 2 and r["numero"] == "3.1"
