"""Pruebas de scripts/utilidades/editor_docx.py con DOCX de PRUEBA generados en tmp_path."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
from docx import Document
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm
from lxml import etree
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad  # noqa: E402
from scripts.utilidades import editor_docx as ed  # noqa: E402


def _pgnum(sec, fmt, start=None):
    for viejo in sec._sectPr.findall(qn("w:pgNumType")):   # add_section() hereda el de la sección previa
        sec._sectPr.remove(viejo)
    pg = OxmlElement("w:pgNumType")
    pg.set(qn("w:fmt"), fmt)
    if start is not None:
        pg.set(qn("w:start"), str(start))
    sec._sectPr.append(pg)


@pytest.fixture
def base(tmp_path) -> Path:
    """Documento de prueba: 2 secciones (romanos y arábigos), una tabla, una figura, runs partidos."""
    d = Document()
    s0 = d.sections[0]
    s0.left_margin = Cm(3.0)
    _pgnum(s0, "lowerRoman")
    d.add_paragraph("Resumen del trabajo")
    p = d.add_paragraph()
    for txt, b in (("El ", False), ("sistema ", False), ("SIVAC", True), (" reduce los tiempos", False)):
        r = p.add_run(txt)
        r.bold = b
    d.add_section(WD_SECTION.NEW_PAGE)
    s1 = d.sections[1]
    s1.left_margin = Cm(3.0)
    _pgnum(s1, "decimal", 1)
    d.add_paragraph("Introducción")
    d.add_paragraph("Texto del cuerpo con una sola mención de Beck.")
    t = d.add_table(rows=2, cols=2)
    t.cell(0, 0).text, t.cell(0, 1).text, t.cell(1, 0).text, t.cell(1, 1).text = "A", "B", "1", "2"
    png = tmp_path / "img.png"
    Image.new("RGB", (100, 60), "white").save(png)
    d.add_paragraph().add_run().add_picture(str(png), width=Cm(3))
    d.add_paragraph("Referencias")
    for ref in ("Beck, K. (1999). *Extreme programming explained*. Addison-Wesley.",
                "Sommerville, I. (2016). *Software engineering*. Pearson."):
        d.add_paragraph(ref)
    ruta = tmp_path / "base.docx"
    d.save(str(ruta))
    return ruta


@pytest.fixture
def png_grande(tmp_path) -> Path:
    p = tmp_path / "grande.png"
    Image.new("RGB", (1800, 900), "white").save(p, dpi=(300, 300))
    return p


def _abrir(e: "ed.EditorDocx") -> Document:
    e.guardar()
    return Document(str(e.destino))


# ------------------------------------------------------------------ seguridad del destino
def test_destino_igual_al_origen_rechazado(base):
    with pytest.raises(seguridad.EscrituraProhibida):
        ed.EditorDocx(base, base)


@pytest.mark.parametrize("destino", [rutas.REFERENCIAS / "x.docx", rutas.DATOS_RAW / "x.docx", rutas.SYNCOVA / "x.docx"])
def test_destino_en_zonas_inmutables_rechazado(base, destino):
    with pytest.raises(seguridad.EscrituraProhibida):
        ed.EditorDocx(base, destino)
    assert not destino.exists()


def test_destino_debe_ser_docx(base, tmp_path):
    with pytest.raises(ed.EditorError):
        ed.EditorDocx(base, tmp_path / "x.txt")


def test_no_pisa_version_existente(base, tmp_path):
    out = tmp_path / "v.docx"
    ed.EditorDocx(base, out).guardar()
    with pytest.raises(FileExistsError):
        ed.EditorDocx(base, out)


def test_original_queda_intacto(base, tmp_path):
    antes = seguridad.sha256_archivo(base)
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    e.reemplazar_texto("mención de Beck", "mención de Fowler")
    e.guardar()
    assert seguridad.sha256_archivo(base) == antes


# ------------------------------------------------------------------ versionado
def test_siguiente_version(tmp_path):
    assert ed.siguiente_version(tmp_path).name == "informe_final_v01.docx"
    (tmp_path / "informe_final_v01.docx").write_bytes(b"x")
    (tmp_path / "informe_final_v07.docx").write_bytes(b"x")
    assert ed.siguiente_version(tmp_path).name == "informe_final_v08.docx"


# ------------------------------------------------------------------ reemplazo
def test_reemplazo_entre_runs_conserva_negrita_de_runs_no_afectados(base, tmp_path):
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    e.reemplazar_texto("El sistema ", "Este módulo ")          # cruza los runs 0 y 1
    d = _abrir(e)
    p = next(p for p in d.paragraphs if "módulo" in p.text)
    assert p.text == "Este módulo SIVAC reduce los tiempos"
    assert [r.text for r in p.runs if r.bold] == ["SIVAC"], "la negrita del run no afectado debe conservarse"


def test_reemplazo_que_abarca_texto_en_negrita_adopta_el_formato_del_primer_run(base, tmp_path):
    # Comportamiento documentado: el texto nuevo toma el formato del primer run afectado.
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    e.reemplazar_texto("sistema SIVAC reduce", "módulo acelera")
    d = _abrir(e)
    p = next(p for p in d.paragraphs if "módulo" in p.text)
    assert p.text == "El módulo acelera los tiempos"
    assert not any(r.bold for r in p.runs)


def test_reemplazo_ambiguo_exige_ocurrencia(base, tmp_path):
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    with pytest.raises(ed.AnclaError):
        e.reemplazar_texto("Beck", "Fowler")                    # cuerpo y referencia
    e.reemplazar_texto("Beck", "Fowler", ocurrencia=1)          # con ocurrencia explícita se permite


def test_reemplazo_inexistente(base, tmp_path):
    with pytest.raises(ed.AnclaError):
        ed.EditorDocx(base, tmp_path / "v.docx").reemplazar_texto("no existe esto", "x")


def test_reemplazo_dry_run_no_escribe(base, tmp_path):
    out = tmp_path / "v.docx"
    e = ed.EditorDocx(base, out, dry_run=True)
    e.reemplazar_texto("mención de Beck", "mención de Fowler")
    inf = e.guardar()
    assert not out.exists() and inf["dry_run"] and inf["cambios"][0]["antes"] == "mención de Beck"


# ------------------------------------------------------------------ secciones intactas
def test_secciones_y_numeracion_identicas_tras_editar(base, tmp_path):
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    e.insertar_parrafo_despues("Introducción", "Nuevo párrafo con **énfasis**.")
    e.reemplazar_texto("mención de Beck", "mención de Beck y Andres")
    inf = e.guardar()
    assert inf["verificacion"]["ok"], inf["verificacion"]
    d0, d1 = Document(str(base)), Document(str(e.destino))
    assert len(d0.sections) == len(d1.sections) == 2
    for a, b in zip(d0.sections, d1.sections):
        assert etree.tostring(a._sectPr, method="c14n") == etree.tostring(b._sectPr, method="c14n")
    pg = [s._sectPr.find(qn("w:pgNumType")) for s in d1.sections]
    assert pg[0].get(qn("w:fmt")) == "lowerRoman" and pg[1].get(qn("w:fmt")) == "decimal"
    assert pg[1].get(qn("w:start")) == "1"


def test_insertar_parrafo_hereda_formato_del_modelo(base, tmp_path):
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    e.insertar_parrafo_despues("Texto del cuerpo", "Añadido *cursiva* y **negrita**.", modelo="Texto del cuerpo")
    d = _abrir(e)
    nuevo = next(p for p in d.paragraphs if p.text.startswith("Añadido"))
    assert nuevo.text == "Añadido cursiva y negrita."
    assert any(r.italic for r in nuevo.runs) and any(r.bold for r in nuevo.runs)


def test_no_duplica_salto_de_seccion_al_clonar(base, tmp_path):
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    pars = e.doc.paragraphs
    idx_fin = next(i for i, p in enumerate(pars) if e._termina_seccion(p))
    e.insertar_parrafo_despues(idx_fin, "Tras el salto", modelo=idx_fin)
    inf = e.guardar()
    assert inf["verificacion"]["ok"]
    assert len(Document(str(e.destino)).sections) == 2


# ------------------------------------------------------------------ tabla APA 7
def test_tabla_apa7_tres_lineas_sin_verticales(base, tmp_path):
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    e.insertar_tabla_apa7("Texto del cuerpo", 1, "Ejemplo de tabla", ["Indicador", "Valor"],
                          [["T_reg", "1"], ["T_vale", "2"]], nota="Elaboración propia.")
    inf = e.guardar()
    assert inf["verificacion"]["ok"], inf["verificacion"]
    d = Document(str(e.destino))
    assert len(d.tables) == 2
    t = d.tables[0] if "Indicador" in d.tables[0].cell(0, 0).text else d.tables[1]
    b = t._tbl.tblPr.find(qn("w:tblBorders"))
    assert b.find(qn("w:top")).get(qn("w:val")) == "single" and b.find(qn("w:bottom")).get(qn("w:val")) == "single"
    for lado in ("left", "right", "insideH", "insideV"):
        assert b.find(qn(f"w:{lado}")).get(qn("w:val")) == "none"
    assert t.rows[0]._tr.trPr.find(qn("w:tblHeader")) is not None
    assert all(r._tr.trPr.find(qn("w:cantSplit")) is not None for r in t.rows)
    assert t.cell(0, 0)._tc.tcPr.find(qn("w:tcBorders")).find(qn("w:bottom")) is not None
    txt = [p.text for p in d.paragraphs]
    i = txt.index("Tabla 1")
    assert txt[i + 1] == "Ejemplo de tabla"
    assert "Nota. Elaboración propia." in txt
    assert d.paragraphs[i].runs[0].bold and d.paragraphs[i + 1].runs[0].italic


def test_tabla_filas_desiguales_rechazada(base, tmp_path):
    with pytest.raises(ed.EditorError):
        ed.EditorDocx(base, tmp_path / "v.docx").insertar_tabla_apa7("Introducción", 1, "t", ["a", "b"], [["x"]])


def test_tabla_xml_valido_orden_de_elementos(base, tmp_path):
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    e.insertar_tabla_apa7("Introducción", 1, "t", ["a", "b"], [["x", "y"]])
    e.guardar()
    d = Document(str(e.destino))
    tblPr = d.tables[0]._tbl.tblPr
    orden = [etree.QName(h).localname for h in tblPr]
    assert orden.index("tblBorders") < orden.index("tblCellMar")
    trPr = d.tables[0].rows[0]._tr.trPr
    assert [etree.QName(h).localname for h in trPr] == ["cantSplit", "tblHeader"]


# ------------------------------------------------------------------ figura APA 7
def test_figura_con_dpi_suficiente(base, tmp_path, png_grande):
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    e.insertar_figura_apa7("Texto del cuerpo", 1, "Arquitectura", png_grande, "Adaptado de Beck (1999, p. 10).", ancho_cm=12)
    inf = e.guardar()
    assert inf["verificacion"]["ok"], inf["verificacion"]
    d = Document(str(e.destino))
    assert len(d.inline_shapes) == 2
    assert inf["cambios"][0]["dpi_efectivo"] >= 300


def test_figura_de_baja_resolucion_abortada(base, tmp_path):
    chica = tmp_path / "chica.png"
    Image.new("RGB", (300, 200), "white").save(chica)
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    with pytest.raises(ed.EditorError, match="DPI"):
        e.insertar_figura_apa7("Introducción", 1, "x", chica, "n", ancho_cm=14)
    assert not (tmp_path / "v.docx").exists()


def test_figura_imagen_inexistente(base, tmp_path):
    with pytest.raises(ed.EditorError):
        ed.EditorDocx(base, tmp_path / "v.docx").insertar_figura_apa7("Introducción", 1, "x", tmp_path / "no.png", "n")


# ------------------------------------------------------------------ referencias
def test_referencia_en_orden_alfabetico_con_sangria_francesa(base, tmp_path):
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    e.insertar_referencia_apa7("Pressman, R. (2010). *Ingeniería del software*. McGraw-Hill.")
    e.insertar_referencia_apa7("Álvarez, J. (2023). *Sistemas de información*. Universidad.")
    d = _abrir(e)
    txt = [p.text for p in d.paragraphs]
    i = txt.index("Referencias")
    orden = [t.split(",")[0] for t in txt[i + 1:i + 5]]
    assert orden == ["Álvarez", "Beck", "Pressman", "Sommerville"]
    p = next(p for p in d.paragraphs if p.text.startswith("Pressman"))
    assert abs(p.paragraph_format.left_indent.cm - 1.27) < 0.01
    assert abs(p.paragraph_format.first_line_indent.cm + 1.27) < 0.01


def test_referencia_duplicada_rechazada(base, tmp_path):
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    with pytest.raises(ed.EditorError, match="duplicada"):
        e.insertar_referencia_apa7("Beck, K. (1999). *Extreme programming explained*. Addison-Wesley.")


def test_sin_encabezado_referencias(tmp_path):
    d = Document()
    d.add_paragraph("Sin referencias")
    p = tmp_path / "a.docx"
    d.save(str(p))
    with pytest.raises(ed.AnclaError):
        ed.EditorDocx(p, tmp_path / "b.docx").insertar_referencia_apa7("X, Y. (2020). Z.")


# ------------------------------------------------------------------ eliminar
def test_eliminar_exige_confirmar_y_protege_secciones_e_imagenes(base, tmp_path):
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    with pytest.raises(ed.EditorError, match="confirmar"):
        e.eliminar_parrafo("Introducción")
    idx_sec = next(i for i, p in enumerate(e.doc.paragraphs) if e._termina_seccion(p))
    with pytest.raises(ed.EditorError, match="sección"):
        e.eliminar_parrafo(idx_sec, confirmar=True)
    idx_img = next(i for i, p in enumerate(e.doc.paragraphs) if p._p.findall(".//" + qn("w:drawing")))
    with pytest.raises(ed.EditorError, match="imagen"):
        e.eliminar_parrafo(idx_img, confirmar=True)


def test_eliminar_con_imagen_forzada_mantiene_verificacion(base, tmp_path):
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    idx_img = next(i for i, p in enumerate(e.doc.paragraphs) if p._p.findall(".//" + qn("w:drawing")))
    e.eliminar_parrafo(idx_img, confirmar=True, forzar=True)
    inf = e.guardar()
    assert inf["verificacion"]["ok"], inf["verificacion"]
    assert len(Document(str(e.destino)).inline_shapes) == 0


def test_eliminar_parrafo_simple(base, tmp_path):
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    e.eliminar_parrafo("Resumen del trabajo", confirmar=True)
    assert "Resumen del trabajo" not in [p.text for p in _abrir(e).paragraphs]


# ------------------------------------------------------------------ búsqueda, log, CLI
def test_buscar_parrafos(base, tmp_path):
    e = ed.EditorDocx(base, tmp_path / "v.docx", dry_run=True)
    assert len(e.buscar_parrafos("sivac")) == 1
    assert len(e.buscar_parrafos(r"^Intro", regex=True)) == 1
    assert e.buscar_parrafos("inexistente") == []


def test_ancla_ambigua_e_indice_fuera_de_rango(base, tmp_path):
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    with pytest.raises(ed.AnclaError, match="ambigua"):
        e.insertar_parrafo_despues("e", "x")
    with pytest.raises(ed.AnclaError):
        e.insertar_parrafo_despues(9999, "x")


def test_registro_de_cambios_con_sha256(base, tmp_path):
    import json
    e = ed.EditorDocx(base, tmp_path / "v.docx")
    e.reemplazar_texto("mención de Beck", "mención de Fowler")
    e.guardar()
    log = json.loads((tmp_path / "v.docx.cambios.json").read_text(encoding="utf-8"))
    assert log["sha256_origen"] == seguridad.sha256_archivo(base)
    assert log["cambios"][0]["operacion"] == "reemplazar_texto"
    assert log["verificacion"]["ok"]


def test_cli_codigos_de_salida(base, tmp_path, capsys):
    out = tmp_path / "cli.docx"
    assert ed.main(["reemplazar", str(base), str(out), "mención de Beck", "mención de Fowler"]) == 0
    assert out.exists()
    assert ed.main(["reemplazar", str(base), str(out), "mención de Beck", "x"]) == 2   # ya existe
    assert ed.main(["reemplazar", str(base), str(base), "mención de Beck", "x"]) == 2  # destino == origen
    assert ed.main(["reemplazar", str(base), str(rutas.REFERENCIAS / "x.docx"), "mención de Beck", "x"]) == 2
    assert ed.main(["reemplazar", str(base), str(tmp_path / "amb.docx"), "Beck", "x"]) == 2  # ambiguo
    assert ed.main(["buscar", str(base), "Introducción"]) == 0
    assert ed.main(["buscar", str(base), "zzz"]) == 1
    assert ed.main(["comando-inexistente"]) == 2
    assert ed.main(["reemplazar", str(tmp_path / "noexiste.docx"), str(tmp_path / "o.docx"), "a", "b"]) == 2
