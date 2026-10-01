# -*- coding: utf-8 -*-
"""Pruebas de scripts/fuentes/extractor_figuras.py.

Los PDFs se generan en tmp_path (fixtures de PRUEBA, sin datos empíricos de la tesis).
Ejecutar: .venv/Scripts/python.exe -m pytest scripts/tests/test_extractor_figuras.py -q
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import fitz
import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad  # noqa: E402
from scripts.fuentes import extractor_figuras as E  # noqa: E402

PARRAFO = ("Este es un párrafo de texto corrido de prueba que describe el método seguido en el estudio "
           "y ocupa varias líneas para simular el cuerpo de un artículo científico real. ") * 3


def _pdf_con_figura(ruta: Path, con_texto_pagina: bool = True) -> Path:
    """Página A4: texto, figura vectorial con leyenda debajo y texto posterior."""
    doc = fitz.open()
    pg = doc.new_page(width=595, height=842)
    if con_texto_pagina:
        pg.insert_textbox(fitz.Rect(56, 50, 540, 150), PARRAFO, fontsize=10)
    # figura vectorial: 6 barras con rótulos
    for i in range(6):
        pg.draw_rect(fitz.Rect(100 + i * 60, 300 - i * 15, 140 + i * 60, 400), color=(0, 0, 0), fill=(0.3, 0.5, 0.8))
    pg.draw_line((90, 400), (480, 400))
    pg.insert_text((100, 200 + 0), "Eje Y de prueba", fontsize=8)
    pg.insert_text((56, 430), "Figura 1. Barras de prueba generadas para el test.", fontsize=10)
    if con_texto_pagina:
        pg.insert_textbox(fitz.Rect(56, 470, 540, 600), PARRAFO, fontsize=10)
    doc.save(str(ruta))
    doc.close()
    return ruta


def _pdf_con_tabla(ruta: Path) -> Path:
    doc = fitz.open()
    pg = doc.new_page(width=595, height=842)
    pg.insert_text((56, 100), "Tabla 1. Datos ficticios de prueba (sin valor empírico).", fontsize=10)
    x0, y0 = 56, 115
    for f in range(4):
        for c in range(3):
            r = fitz.Rect(x0 + c * 120, y0 + f * 25, x0 + (c + 1) * 120, y0 + (f + 1) * 25)
            pg.draw_rect(r, color=(0, 0, 0), width=0.8)
            pg.insert_text((r.x0 + 5, r.y0 + 16), f"c{f}{c}", fontsize=9)
    pg.insert_textbox(fitz.Rect(56, 260, 540, 400), PARRAFO, fontsize=10)
    doc.save(str(ruta))
    doc.close()
    return ruta


@pytest.fixture()
def entorno(tmp_path):
    return {"indices": tmp_path / "idx", "salida": tmp_path / "out", "tmp": tmp_path}


# ---------------------------------------------------------------- leyendas
@pytest.mark.parametrize("texto,tipo,num", [
    ("Figura 1. Diagrama de flujo", "figura", "1"),
    ("Fig. 2: Modelo", "figura", "2"),
    ("Figure 3 Conceptual framework", "figura", "3"),
    ("FIGURE 2 Self-reported level", "figura", "2"),
    ("Tabla 4. Resultados", "tabla", "4"),
    ("Table 1 Sociodemographic", "tabla", "1"),
    ("Gráfico 5 - Evolución", "figura", "5"),
    ("Cuadro 2. Operacionalización", "tabla", "2"),
    ("Esquema 1: Flujo", "figura", "1"),
    ("Table 2.1. Subtabla", "tabla", "2.1"),
])
def test_leyendas_validas(texto, tipo, num):
    r = E.clasificar_leyenda(texto)
    assert r and r["tipo"] == tipo and r["numero"] == num


@pytest.mark.parametrize("texto", [
    "La Figura 1 muestra los resultados del estudio.",
    "Figure 3 shows the results of the analysis.",
    "Como se observa en la Tabla 2, los valores",
    "Tabla 3 muestra el detalle",
    "Figura 1 .......... 12",
    "Texto cualquiera",
    "",
])
def test_leyendas_rechazadas(texto):
    assert E.clasificar_leyenda(texto) is None


# ---------------------------------------------------------------- geometría
def test_agrupar_cajas_une_cercanas_y_separa_lejanas():
    cajas = [((0, 0, 50, 50), "vector"), ((55, 0, 100, 50), "vector"), ((300, 300, 350, 350), "raster")]
    g = E.agrupar_cajas(cajas, gap=10)
    assert len(g) == 2
    grande = max(g, key=lambda x: x["n"])
    assert grande["n"] == 2 and grande["bbox"] == (0, 0, 100, 50)


def test_solape_y_union():
    assert E._solape_h((0, 0, 10, 10), (5, 20, 15, 30)) == pytest.approx(0.5)
    assert E._union((0, 0, 5, 5), (3, 3, 9, 9)) == (0, 0, 9, 9)


def test_parsear_paginas():
    assert E.parsear_paginas("1,3-5,99", 6) == [1, 3, 4, 5]
    assert E.parsear_paginas(None, 3) == [1, 2, 3]


def test_parsear_clip_relativo_y_errores(tmp_path):
    pdf = _pdf_con_figura(tmp_path / "a.pdf")
    with fitz.open(pdf) as doc:
        page = doc[0]
        r = E.parsear_clip("0,0,0.5,0.5", page, relativo=True)
        assert r.width == pytest.approx(297.5) and r.height == pytest.approx(421)
        with pytest.raises(ValueError):
            E.parsear_clip("0,0,2,1", page, relativo=True)
        with pytest.raises(ValueError):
            E.parsear_clip("1,2,3", page)
        with pytest.raises(ValueError):
            E.parsear_clip("abc", page)
        with pytest.raises(ValueError):
            E.parsear_clip("900,900,950,950", page)  # fuera de la página


# ---------------------------------------------------------------- cita APA
def test_cita_marca_verificar_sin_datos():
    fuente = {"titulo_metadatos": None, "autor_metadatos": None, "doi_detectado": None}
    c = E.construir_cita(fuente, 5, None)
    assert "[VERIFICAR: título]" in c and "[VERIFICAR: autor]" in c and "[VERIFICAR: año]" in c
    assert "página impresa no determinada" in c and "página física 5" in c


def test_cita_completa_sin_verificar_y_modo_reproducido():
    fuente = {"titulo_metadatos": "X", "autor_metadatos": "Y", "doi_detectado": None}
    meta = {"titulo": "Título real", "autor": "Pérez, A.", "anio": 2020, "doi": "10.1000/abc"}
    c = E.construir_cita(fuente, 5, "71", meta, "reproducido")
    assert "VERIFICAR" not in c and c.startswith("Nota. Reproducido de")
    assert "(p. 71)" in c and "Pérez, A., 2020" in c and "https://doi.org/10.1000/abc" in c


def test_cita_doi_detectado_requiere_verificar():
    c = E.construir_cita({"doi_detectado": "10.1/x"}, 1, "1", {"titulo": "T", "autor": "A", "anio": 2001})
    assert "DOI detectado automáticamente" in c


# ---------------------------------------------------------------- extracción
def test_extraer_figura_vectorial_300dpi(entorno):
    pdf = _pdf_con_figura(entorno["tmp"] / "fig.pdf")
    res = E.extraer_pdf(pdf, entorno["salida"], entorno["indices"])
    assert res["resumen"]["figuras"] == 1
    f = res["figuras"][0]
    assert f["tipo"] == "figura" and f["numero"] == "1" and f["estado"] == "creada"
    assert f["confianza"] in ("alta", "media")
    png = Path(f["ruta_png"])
    assert png.name == "figura_p0001_1.png"
    with Image.open(png) as im:
        assert tuple(round(v) for v in im.info["dpi"]) == (300, 300)
        assert im.size == (f["ancho_px"], f["alto_px"])
        # 300 DPI exactos: px ~ pt * 300/72 (tolerancia de 1 px por redondeo)
        x0, y0, x1, y1 = f["bbox_pt"]
        assert abs(im.width - (x1 - x0) * E.ZOOM) <= 2
        assert abs(im.height - (y1 - y0) * E.ZOOM) <= 2
    # el recorte no debe invadir la leyenda (que empieza en y~420) ni el texto corrido posterior
    assert f["bbox_pt"][3] < 425
    assert f["bbox_pt"][1] > 150  # ni el párrafo superior
    sc = json.loads(png.with_suffix(".json").read_text(encoding="utf-8"))
    assert sc["fuente"]["archivo"] == "fig.pdf" and len(sc["fuente"]["sha256"]) == 64
    assert sc["pagina_fisica"] == 1 and sc["dpi"] == 300
    assert "Barras de prueba" in sc["leyenda_textual"]
    assert "VERIFICAR" in sc["cita_sugerida"]  # año/autor no confirmables
    cat = (Path(res["carpeta"]) / "catalogo_figuras.md").read_text(encoding="utf-8")
    assert "![[figura_p0001_1.png]]" in cat and "tipo: catalogo_figuras" in cat


def test_no_sobrescribe_sin_forzar(entorno):
    pdf = _pdf_con_figura(entorno["tmp"] / "fig.pdf")
    E.extraer_pdf(pdf, entorno["salida"], entorno["indices"])
    png = Path(E.carpeta_salida(pdf, entorno["salida"])) / "figura_p0001_1.png"
    mtime = png.stat().st_mtime_ns
    res2 = E.extraer_pdf(pdf, entorno["salida"], entorno["indices"])
    assert res2["figuras"][0]["estado"] == "existente" and png.stat().st_mtime_ns == mtime
    res3 = E.extraer_pdf(pdf, entorno["salida"], entorno["indices"], forzar=True)
    assert res3["figuras"][0]["estado"] == "sobrescrita"


def test_solo_detectar_no_escribe(entorno):
    pdf = _pdf_con_figura(entorno["tmp"] / "fig.pdf")
    res = E.extraer_pdf(pdf, entorno["salida"], entorno["indices"], solo_detectar=True)
    assert res["figuras"][0]["estado"] == "detectada"
    assert not Path(res["carpeta"]).exists()


def test_extraer_tabla_pdfplumber(entorno):
    pdf = _pdf_con_tabla(entorno["tmp"] / "tab.pdf")
    res = E.extraer_pdf(pdf, entorno["salida"], entorno["indices"])
    assert res["resumen"]["tablas"] == 1
    f = res["figuras"][0]
    assert f["tipo"] == "tabla" and f["numero"] == "1"
    assert f["bbox_pt"][1] > 100  # no incluye la leyenda superior (y~100)


def test_leyenda_sin_region_se_omite_y_pagina_de_texto_no_se_recorta(entorno):
    doc = fitz.open()
    pg = doc.new_page()
    pg.insert_textbox(fitz.Rect(56, 50, 540, 700), PARRAFO * 4, fontsize=10)
    pg.insert_text((56, 760), "Figura 9. Leyenda sin gráfico asociado.", fontsize=10)
    ruta = entorno["tmp"] / "texto.pdf"
    doc.save(str(ruta))
    doc.close()
    res = E.extraer_pdf(ruta, entorno["salida"], entorno["indices"])
    assert res["figuras"] == [] and len(res["omitidas"]) == 1


def test_pagina_sin_capa_de_texto_marca_ocr(entorno):
    # Imagen raster sin texto: debe marcarse requiere_ocr, sin inventar texto
    img = entorno["tmp"] / "x.png"
    Image.new("RGB", (400, 300), (200, 200, 200)).save(img)
    doc = fitz.open()
    pg = doc.new_page()
    pg.insert_image(fitz.Rect(50, 50, 500, 400), filename=str(img))
    ruta = entorno["tmp"] / "scan.pdf"
    doc.save(str(ruta))
    doc.close()
    res = E.extraer_pdf(ruta, entorno["salida"], entorno["indices"])
    assert res["paginas_requieren_ocr"] == [1] and res["figuras"] == []
    man = E.recorte_manual(ruta, 1, "50,50,500,400", salida_base=entorno["salida"], carpeta_indices=entorno["indices"])
    assert man["requiere_ocr"] is True and any("OCR" in n for n in man["notas"])


# ---------------------------------------------------------------- manual
def test_recorte_manual_300dpi_y_sin_pisar(entorno):
    pdf = _pdf_con_figura(entorno["tmp"] / "fig.pdf")
    m = E.recorte_manual(pdf, 1, "0.1,0.3,0.9,0.5", relativo=True, salida_base=entorno["salida"],
                         carpeta_indices=entorno["indices"])
    with Image.open(m["ruta_png"]) as im:
        assert tuple(round(v) for v in im.info["dpi"]) == (300, 300)
        assert im.width == pytest.approx(0.8 * 595 * E.ZOOM, abs=2)
    assert m["metodo_deteccion"] == "manual"
    m2 = E.recorte_manual(pdf, 1, "50,250,300,420", salida_base=entorno["salida"], carpeta_indices=entorno["indices"])
    assert m2["archivo_png"] != m["archivo_png"]  # numeración automática, no pisa
    with pytest.raises(FileExistsError):
        E.recorte_manual(pdf, 1, "50,250,300,420", salida_base=entorno["salida"], carpeta_indices=entorno["indices"],
                         n=1)
    with pytest.raises(ValueError):
        E.recorte_manual(pdf, 7, salida_base=entorno["salida"], carpeta_indices=entorno["indices"])


def test_listar(entorno):
    pdf = _pdf_con_figura(entorno["tmp"] / "fig.pdf")
    E.extraer_pdf(pdf, entorno["salida"], entorno["indices"])
    filas = E.listar(entorno["salida"])
    assert len(filas) == 1 and filas[0]["tipo"] == "figura"
    assert E.listar(entorno["salida"], pdf) == filas


# ---------------------------------------------------------------- seguridad / CLI
def test_no_escribe_en_rutas_protegidas():
    with pytest.raises(seguridad.EscrituraProhibida):
        E.guardar_png(Image.new("RGB", (5, 5)), rutas.MODELOS_TESIS / "x.png")
    with pytest.raises(seguridad.EscrituraProhibida):
        E.guardar_json({}, rutas.SYNCOVA / "x.json")


def test_ocr_disponible_no_falla():
    assert isinstance(E.ocr_disponible(), bool)


def test_cli_codigos_de_salida(entorno, capsys):
    pdf = _pdf_con_figura(entorno["tmp"] / "fig.pdf")
    base = ["--salida", str(entorno["salida"]), "--indices", str(entorno["indices"])]
    assert E.main([]) == 2
    assert E.main(["extraer", "--pdf", str(entorno["tmp"] / "no_existe.pdf")] + base) == 2
    assert E.main(["pagina", "--pdf", str(pdf), "--pag", "1", "--clip", "x"] + base) == 2
    rc = E.main(["extraer", "--pdf", str(pdf), "--json"] + base)
    assert rc in (0, 1)
    salida = capsys.readouterr().out
    assert json.loads(salida[salida.index("{"):])["resumen"]["figuras"] == 1
    assert E.main(["listar", "--json"] + base) == 0


# ---------------------------------------------------------------- PDFs reales (solo lectura)
_XP = rutas.PDFS_FUENTES / "Embracing change with extreme programming.pdf"


@pytest.mark.skipif(not _XP.exists(), reason="PDF real no disponible")
def test_pdf_real_xp_detecta_dos_figuras(tmp_path):
    res = E.extraer_pdf(_XP, tmp_path / "out", rutas.INDICES_PDF, solo_detectar=True)
    assert res["resumen"]["figuras"] == 2
    assert {f["numero"] for f in res["figuras"]} == {"1", "2"}
    # etiqueta impresa distinta de la física (p. 1 física = p. 70 impresa)
    assert res["figuras"][0]["etiqueta_impresa"] != str(res["figuras"][0]["pagina_fisica"])


# ---------------------------------------------------------------- correcciones de la verificación
def _pdf_leyenda_lateral(ruta: Path, texto_en_margen: bool = False) -> Path:
    """Maquetación de libro de texto: leyenda corta en el margen izquierdo y gráfico a la derecha."""
    doc = fitz.open()
    pg = doc.new_page(width=531, height=657)
    pg.insert_textbox(fitz.Rect(180, 450, 480, 600), PARRAFO, fontsize=10)
    for i in range(5):
        pg.draw_rect(fitz.Rect(200 + i * 50, 200 - i * 10, 230 + i * 50, 300), color=(0, 0, 0), fill=(0.3, 0.5, 0.8))
    pg.draw_line((190, 300), (460, 300))
    pg.insert_textbox(fitz.Rect(47, 250, 130, 290), "Figure 1.4 Insulin pump hardware", fontsize=8)
    if texto_en_margen:
        rc = pg.insert_textbox(fitz.Rect(47, 100, 130, 240), "Texto corrido del margen que no es una leyenda sino comentario del autor al lado. " * 2, fontsize=7)
        assert rc >= 0  # el texto debe caber para que se dibuje
    doc.save(str(ruta))
    doc.close()
    return ruta


def test_leyenda_lateral_de_margen_se_asocia(entorno):
    pdf = _pdf_leyenda_lateral(entorno["tmp"] / "lat.pdf")
    res = E.extraer_pdf(pdf, entorno["salida"], entorno["indices"], solo_detectar=True)
    assert res["omitidas"] == [] and res["resumen"]["figuras"] == 1
    f = res["figuras"][0]
    assert f["numero"] == "1.4" and f["confianza"] in ("media", "baja")  # nunca 'alta': posición no convencional
    assert any("lateral" in n for n in f["notas"])
    assert f["bbox_pt"][0] > 150  # el recorte no incluye la leyenda del margen


def test_leyenda_lateral_descartada_si_hay_texto_corrido_en_su_margen(entorno):
    pdf = _pdf_leyenda_lateral(entorno["tmp"] / "lat2.pdf", texto_en_margen=True)
    res = E.extraer_pdf(pdf, entorno["salida"], entorno["indices"], solo_detectar=True)
    assert res["resumen"]["figuras"] == 0 and len(res["omitidas"]) == 1


def test_refinar_leyenda_acota_al_estilo_tipografico():
    ley = {"tipo": "figura", "numero": "1", "etiqueta": "Figura", "bbox": (50, 100, 400, 160),
           "texto": "Figura 1: Estilos de API. Fuente: X. Actualmente las API REST son muy populares.",
           "parrafo_id": "p1"}
    lineas = [((50, 100, 300, 110), "Figura 1: Estilos de API. Fuente: X. ", 10.0),
              ((50, 125, 400, 138), "Actualmente las API REST son muy populares", 12.0),
              ((50, 139, 300, 152), "por su flexibilidad.", 12.0)]
    r = E.refinar_leyenda(ley, lineas)
    assert r["texto"] == "Figura 1: Estilos de API. Fuente: X." and r["bbox"] == (50, 100, 300, 110)
    assert r["bbox_parrafo"] == (50, 100, 400, 160)
    # leyenda homogénea: sin cambios
    ley2 = {**ley, "texto": "Figura 1: Solo leyenda", "bbox": (50, 100, 300, 125)}
    assert E.refinar_leyenda(ley2, lineas[:1]) is ley2


def test_leyenda_textual_no_arrastra_el_parrafo_siguiente(entorno):
    doc = fitz.open()
    pg = doc.new_page(width=595, height=842)
    for i in range(5):
        pg.draw_rect(fitz.Rect(100 + i * 60, 300 - i * 15, 140 + i * 60, 400), color=(0, 0, 0), fill=(0.3, 0.5, 0.8))
    pg.draw_line((90, 400), (480, 400))
    pg.insert_text((56, 430), "Figura 1: Barras de prueba. Fuente: ficticia.", fontsize=9)
    pg.insert_textbox(fitz.Rect(56, 434, 540, 520), "Actualmente el texto que sigue es cuerpo del documento. " * 4, fontsize=12)
    ruta = entorno["tmp"] / "arr.pdf"
    doc.save(str(ruta))
    doc.close()
    res = E.extraer_pdf(ruta, entorno["salida"], entorno["indices"], solo_detectar=True)
    assert res["resumen"]["figuras"] == 1
    assert "Actualmente" not in res["figuras"][0]["leyenda_textual"]


def test_escritura_vedada_en_referencias_y_datos_raw(tmp_path):
    for destino in (rutas.REFERENCIAS / "x" / "a.png", rutas.DATOS_RAW / "x" / "a.png"):
        with pytest.raises(seguridad.EscrituraProhibida):
            E.guardar_png(Image.new("RGB", (5, 5)), destino)
        with pytest.raises(seguridad.EscrituraProhibida):
            E.guardar_json({}, destino.with_suffix(".json"))
    E.asegurar_destino(tmp_path / "ok" / "a.png")  # una ruta ajena sí se permite


def test_cli_salida_vedada_no_escribe(entorno):
    pdf = _pdf_con_figura(entorno["tmp"] / "fig.pdf")
    destino = rutas.DATOS_RAW / "_prueba_extractor"
    rc = E.main(["extraer", "--pdf", str(pdf), "--salida", str(destino), "--indices", str(entorno["indices"])])
    assert rc == 1 and not destino.exists()
    rc = E.main(["pagina", "--pdf", str(pdf), "--pag", "1", "--clip", "0,0,200,200", "--salida",
                 str(rutas.REFERENCIAS / "_prueba_extractor"), "--indices", str(entorno["indices"])])
    assert rc == 1 and not (rutas.REFERENCIAS / "_prueba_extractor").exists()


def test_sin_aviso_de_fitz_obsoleto_en_stderr():
    import subprocess
    r = subprocess.run([sys.executable, str(Path(E.__file__)), "--help"], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0 and "deprecated" not in r.stderr


def test_sidecar_declara_criterio_de_confianza(entorno):
    pdf = _pdf_con_figura(entorno["tmp"] / "fig.pdf")
    res = E.extraer_pdf(pdf, entorno["salida"], entorno["indices"], solo_detectar=True)
    assert "no implica revisión visual" in res["figuras"][0]["confianza_criterio"]


_SOMMERVILLE = rutas.PDFS_FUENTES / "Software Engineering.pdf"


@pytest.mark.skipif(not _SOMMERVILLE.exists(), reason="PDF real no disponible")
def test_pdf_real_sommerville_leyendas_laterales(tmp_path):
    res = E.extraer_pdf(_SOMMERVILLE, tmp_path / "out", rutas.INDICES_PDF, solo_detectar=True, paginas="34,35,51")
    nums = {(f["pagina_fisica"], f["numero"]) for f in res["figuras"]}
    assert {(34, "1.4"), (34, "1.5"), (35, "1.6"), (51, "2.2")} <= nums
    assert res["omitidas"] == []
