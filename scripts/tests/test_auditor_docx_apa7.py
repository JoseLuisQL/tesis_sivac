"""Pruebas de scripts/utilidades/auditor_docx_apa7.py con DOCX de PRUEBA en tmp_path."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas  # noqa: E402
from scripts.utilidades import auditor_docx_apa7 as au  # noqa: E402
from scripts.utilidades import editor_docx as ed  # noqa: E402

LARGO = ("El sistema web SIVAC se evaluó en el personal de inmunizaciones de la Dirección de Salud Apurímac II "
         "para determinar su influencia en los tiempos de registro y en la consistencia documental (Beck, 1999). ") * 2


def _pg(sec, fmt, start=None):
    for v in sec._sectPr.findall(qn("w:pgNumType")):
        sec._sectPr.remove(v)
    e = OxmlElement("w:pgNumType")
    e.set(qn("w:fmt"), fmt)
    if start:
        e.set(qn("w:start"), str(start))
    sec._sectPr.append(e)


def _margenes(sec, izq=3.0, otros=2.54):
    sec.left_margin, sec.right_margin = Cm(izq), Cm(otros)
    sec.top_margin = sec.bottom_margin = Cm(otros)


def _estilo_base(d, fuente="Times New Roman"):
    st = d.styles["Normal"]
    st.font.name, st.font.size = fuente, Pt(12)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), fuente)


def _parrafo(d, texto, sangria=1.27, interl=1.5):
    p = d.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(sangria)
    p.paragraph_format.line_spacing = interl
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(texto)
    return p


@pytest.fixture
def conforme(tmp_path) -> Path:
    d = Document()
    _estilo_base(d)
    s0 = d.sections[0]
    _margenes(s0)
    _pg(s0, "lowerRoman")
    _parrafo(d, LARGO)
    d.add_section(WD_SECTION.NEW_PAGE)
    s1 = d.sections[1]
    _margenes(s1)
    _pg(s1, "decimal", 1)
    _parrafo(d, LARGO)
    png = tmp_path / "f.png"
    Image.new("RGB", (1800, 900), "white").save(png, dpi=(300, 300))
    base = tmp_path / "base.docx"
    d.add_paragraph("Referencias").runs[0].bold = True
    d.save(str(base))
    e = ed.EditorDocx(base, tmp_path / "conforme.docx")
    e.insertar_tabla_apa7(1, 1, "Tabla conforme", ["A", "B"], [["x", "1"]], nota="Nota de prueba.")
    e.insertar_figura_apa7(1, 1, "Figura conforme", png, "Nota de figura.", ancho_cm=12)
    e.insertar_referencia_apa7("Beck, K. (1999). *Extreme programming explained*. Addison-Wesley.")
    e.guardar()
    return tmp_path / "conforme.docx"


def _reglas(inf, sev=None):
    return {h["regla"] for h in inf["hallazgos"] if sev is None or h["severidad"] == sev}


def test_documento_conforme_sin_criticos_ni_mayores(conforme):
    inf = au.auditar(conforme)
    graves = [h for h in inf["hallazgos"] if h["severidad"] in ("critico", "mayor")]
    assert graves == [], graves
    assert inf["resumen"]["tablas"] == 1 and inf["resumen"]["imagenes"] == 1


# --- defectos sembrados: cada uno debe detectarse ---------------------------------------
def test_detecta_fuente_arial(tmp_path):
    d = Document()
    _estilo_base(d, "Arial")
    _parrafo(d, LARGO)
    d.save(str(tmp_path / "a.docx"))
    assert "FUENTE" in _reglas(au.auditar(tmp_path / "a.docx"), "mayor")


def test_detecta_margenes_incorrectos(tmp_path):
    d = Document()
    _estilo_base(d)
    _margenes(d.sections[0], izq=2.0, otros=1.5)
    d.save(str(tmp_path / "a.docx"))
    assert len([h for h in au.auditar(tmp_path / "a.docx")["hallazgos"] if h["regla"] == "MARGENES"]) == 4


def test_detecta_interlineado_sencillo_y_sin_sangria(tmp_path):
    d = Document()
    _estilo_base(d)
    _parrafo(d, LARGO, sangria=0, interl=1.0)
    d.save(str(tmp_path / "a.docx"))
    r = _reglas(au.auditar(tmp_path / "a.docx"))
    assert {"INTERLINEADO", "SANGRIA"} <= r


def test_detecta_tabla_con_bordes_verticales(tmp_path):
    d = Document()
    _estilo_base(d)
    t = d.add_table(rows=2, cols=2)
    t.style = "Table Grid"
    d.save(str(tmp_path / "a.docx"))
    inf = au.auditar(tmp_path / "a.docx")
    det = " ".join(h["detalle"] for h in inf["hallazgos"] if h["regla"] == "TABLA")
    assert "verticales" in det and "interiores" in det


def test_detecta_figura_de_baja_resolucion(tmp_path):
    d = Document()
    _estilo_base(d)
    png = tmp_path / "f.png"
    Image.new("RGB", (300, 200), "white").save(png)
    d.add_paragraph().add_run().add_picture(str(png), width=Cm(14))
    d.save(str(tmp_path / "a.docx"))
    inf = au.auditar(tmp_path / "a.docx")
    assert any(h["regla"] == "FIGURA" and "DPI" in h["detalle"] for h in inf["hallazgos"])


def test_detecta_referencias_sin_sangria_desorden_y_huerfanas(tmp_path):
    d = Document()
    _estilo_base(d)
    _parrafo(d, "Según Pressman (2010) el proceso es iterativo y lo confirma (Sommerville, 2016).")
    d.add_paragraph("Referencias")
    d.add_paragraph("Sommerville, I. (2016). Software engineering. Pearson.")
    d.add_paragraph("Beck, K. (1999). Extreme programming explained. Addison-Wesley.")
    d.save(str(tmp_path / "a.docx"))
    inf = au.auditar(tmp_path / "a.docx")
    det = [h["detalle"] for h in inf["hallazgos"] if h["regla"] == "REFERENCIAS"]
    assert any("sangría francesa" in x for x in det)
    assert any("alfabético" in x for x in det)
    assert any("sin entrada" in x for x in det)          # Pressman citado, no listado
    assert any("sin ninguna cita" in x for x in det)     # Beck listado, no citado


def test_detecta_numeracion_incorrecta(tmp_path):
    d = Document()
    _estilo_base(d)
    d.add_paragraph("a")
    d.add_section(WD_SECTION.NEW_PAGE)
    _pg(d.sections[0], "decimal")
    _pg(d.sections[1], "decimal")           # cuerpo sin reinicio
    d.save(str(tmp_path / "a.docx"))
    det = " ".join(h["detalle"] for h in au.auditar(tmp_path / "a.docx")["hallazgos"] if h["regla"] == "NUMERACION")
    assert "romanos" in det and "reinicia" in det


def test_detecta_rotulos_sin_formato_y_numeracion_salteada(tmp_path):
    d = Document()
    _estilo_base(d)
    d.add_paragraph("Tabla 1")
    d.add_paragraph("Titulo sin cursiva")
    d.add_paragraph("Tabla 3")
    d.save(str(tmp_path / "a.docx"))
    det = " ".join(h["detalle"] for h in au.auditar(tmp_path / "a.docx")["hallazgos"] if h["regla"] == "ROTULO")
    assert "negrita" in det and "correlativa" in det


def test_detecta_ampersand_y_et_al(tmp_path):
    d = Document()
    _estilo_base(d)
    _parrafo(d, "Como señalan Beck & Andres en su obra y Pérez et al en otra, el método es iterativo y flexible.")
    d.save(str(tmp_path / "a.docx"))
    assert any("&" in h["detalle"] or "et al" in h["detalle"] for h in au.auditar(tmp_path / "a.docx")["hallazgos"])


# --- solo lectura, CLI ------------------------------------------------------------------
def test_no_modifica_el_documento(conforme):
    antes = conforme.read_bytes()
    au.auditar(conforme)
    assert conforme.read_bytes() == antes


def test_codigo_sin_escrituras_sobre_el_docx():
    import re
    codigo = Path(au.__file__).read_text(encoding="utf-8")
    assert not re.search(r"\.save\(|\.write_bytes\(|os\.remove|unlink\(|shutil\.", codigo)


def test_cli_codigos_de_salida(conforme, tmp_path, capsys):
    assert au.main(["auditar", str(conforme)]) == 0
    malo = Document()
    _estilo_base(malo, "Arial")
    _parrafo(malo, LARGO)
    malo.save(str(tmp_path / "malo.docx"))
    assert au.main(["auditar", str(tmp_path / "malo.docx")]) == 1
    assert au.main(["auditar", str(tmp_path / "noexiste.docx")]) == 2
    (tmp_path / "corrupto.docx").write_bytes(b"esto no es un zip")
    assert au.main(["auditar", str(tmp_path / "corrupto.docx")]) == 2
    assert au.main(["auditar", str(tmp_path)]) == 2
    assert au.main([]) == 2
    capsys.readouterr()
    assert au.main(["auditar", str(conforme), "--json"]) == 0
    assert '"totales"' in capsys.readouterr().out


def test_cli_salida_respeta_vetos(conforme, tmp_path):
    assert au.main(["auditar", str(conforme), "--md", "--salida", str(tmp_path / "inf.md")]) == 0
    assert au.main(["auditar", str(conforme), "--md", "--salida", str(tmp_path / "inf.md")]) == 2
    assert au.main(["auditar", str(conforme), "--salida", str(rutas.REFERENCIAS / "x.md")]) == 2


def test_resumen_estructura(conforme, capsys):
    assert au.main(["resumen-estructura", str(conforme)]) == 0
    assert '"secciones": 2' in capsys.readouterr().out


def test_figura_no_centrada_se_reporta_sin_error(tmp_path):
    d = Document()
    _estilo_base(d)
    png = tmp_path / "f.png"
    Image.new("RGB", (1800, 900), "white").save(png, dpi=(300, 300))
    d.add_paragraph().add_run().add_picture(str(png), width=Cm(12))      # alineación por defecto: izquierda
    d.save(str(tmp_path / "a.docx"))
    hall = au.auditar(tmp_path / "a.docx")["hallazgos"]
    assert any(h["regla"] == "FIGURA" and "centrada" in h["detalle"] for h in hall)
    assert not any("No se pudo evaluar" in h["detalle"] for h in hall)


@pytest.mark.parametrize("titulo", ["Referencias", "REFERENCIAS BIBLIOGRÁFICAS", "Referencia Bibliográfica", "Bibliografía"])
def test_reconoce_variantes_del_encabezado_de_referencias(tmp_path, titulo):
    d = Document()
    _estilo_base(d)
    d.add_paragraph(titulo)
    d.save(str(tmp_path / "a.docx"))
    det = " ".join(h["detalle"] for h in au.auditar(tmp_path / "a.docx")["hallazgos"])
    assert "No se encontró el encabezado" not in det


def test_apellidos_compuestos_se_emparejan_con_cualquier_componente(tmp_path):
    d = Document()
    _estilo_base(d)
    _parrafo(d, "Según Sampieri (2014) y Morejón (2023) el método es válido y reproducible en contextos similares.")
    d.add_paragraph("Referencias")
    for r in ("Balón Morejón, J. (2023). Sistema de control. Universidad.",
              "Hernández Sampieri, R. (2014). Metodología de la investigación. McGraw-Hill."):
        p = d.add_paragraph(r)
        p.paragraph_format.left_indent, p.paragraph_format.first_line_indent = Cm(1.27), Cm(-1.27)
    d.save(str(tmp_path / "a.docx"))
    det = [h["detalle"] for h in au.auditar(tmp_path / "a.docx")["hallazgos"] if h["regla"] == "REFERENCIAS"]
    assert not any("sin entrada" in x or "sin ninguna cita" in x for x in det), det
