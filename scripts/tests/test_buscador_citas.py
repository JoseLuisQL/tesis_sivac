"""Pruebas de scripts/fuentes/buscador_citas.py (sin red; PDFs de PRUEBA en tmp_path + 1 PDF real en solo lectura)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import fitz
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas  # noqa: E402
from scripts.fuentes import buscador_citas as bc  # noqa: E402

P1 = ("El sistema de informacion de inmunizaciones permite registrar cada movimiento de vacunas en la "
      "red de frio con trazabilidad completa y reduce el tiempo medio de registro a 12 minutos por "
      "documento emitido durante la jornada ordinaria de trabajo del personal.")
P2 = ("La consistencia documental se evalua comparando la cantidad programada contra la entregada en "
      "cada vale de salida, de modo que el 85 % de los registros debe estar libre de discrepancias "
      "antes de cerrar el periodo mensual de reporte del establecimiento.")
P3 = ("Finalmente la satisfaccion del usuario se mide con una escala tipo Likert de cinco puntos que "
      "recoge la utilidad percibida y la aceptacion del proceso por parte de los catorce trabajadores.")


def _pdf(ruta: Path, paginas: list[list[str]], numerar: bool = True) -> Path:
    doc = fitz.open()
    for i, parrafos in enumerate(paginas, 1):
        pg = doc.new_page()
        y = 80
        for par in parrafos:
            pg.insert_textbox(fitz.Rect(72, y, 540, y + 120), par, fontsize=11)
            y += 130
        if numerar:
            pg.insert_text((300, 815), str(i + 10), fontsize=10)  # etiqueta impresa = física + 10
    doc.save(ruta)
    doc.close()
    return ruta


@pytest.fixture()
def entorno(tmp_path):
    carpeta = tmp_path / "pdfs"
    carpeta.mkdir()
    idx = tmp_path / "idx"
    _pdf(carpeta / "Manual Vacunas Alfa.pdf", [[P1, P2], [P3]])
    _pdf(carpeta / "Manual Vacunas Beta.pdf", [[P3]], numerar=False)
    return carpeta, idx


def _buscar(entorno, texto, pdfs="Alfa", **kw):
    carpeta, idx = entorno
    return bc.buscar(texto, pdfs=pdfs, carpeta_pdfs=carpeta, carpeta_indices=idx, **kw)


# ---- búsqueda -------------------------------------------------------------------------
def test_literal_con_pagina_impresa(entorno):
    r = _buscar(entorno, P2[20:140])
    c = r["coincidencias"][0]
    assert c["tipo"] == "literal" and c["score"] == 100
    assert c["pagina_fisica"] == 1 and c["etiqueta_impresa"] == "11"
    assert c["parrafo"]["n"] >= 1 and c["parrafo"]["id"].startswith("p0001-")
    assert "consistencia documental" in c["texto_del_parrafo"]
    assert c["contexto"]["previo"] is not None  # hay párrafo anterior (P1)


def test_literal_tolera_saltos_de_linea_y_tildes_y_ligaduras(entorno):
    consulta = "la consistencia docu-\nmental se evalúa comparando la cantidad programada  contra la entregada"
    r = _buscar(entorno, consulta)
    assert r["coincidencias"][0]["tipo"] == "literal"
    assert r["coincidencias"][0]["pagina_fisica"] == 1


def test_cita_cruza_salto_de_pagina(entorno):
    q = P2[-80:] + " " + P3[:80]
    r = _buscar(entorno, q)
    c = r["coincidencias"][0]
    assert c["tipo"] == "literal"
    assert c["pagina_fisica"] == 1 and c["abarca"]["pagina_fisica_fin"] == 2
    assert bc.formatear_cita_apa7(c, ["Rojas"], 2024, "textual") == "(Rojas, 2024, pp. 11-12)"


def test_aproximada_sobrevive_a_cambio_de_palabra(entorno):
    q = P1.replace("permite registrar", "permite anotar")
    r = _buscar(entorno, q)
    c = r["coincidencias"][0]
    assert c["tipo"] == "aproximada" and 60 <= c["score"] < 100
    assert c["pagina_fisica"] == 1


def test_sin_coincidencia_confiable_no_fuerza_resultados(entorno):
    r = _buscar(entorno, "xyzzy quantum banana hospital zebra orbital")
    assert r["estado"] == bc.MSG_SIN_COINCIDENCIA and r["coincidencias"] == []


def test_consulta_corta_no_busca(entorno):
    assert _buscar(entorno, "de la")["estado"] == bc.MSG_SIN_COINCIDENCIA


def test_etiqueta_none_si_no_hay_numero_impreso(entorno):
    r = _buscar(entorno, P3[10:120], pdfs="Beta")
    c = r["coincidencias"][0]
    assert c["etiqueta_impresa"] is None and c["pagina_fisica"] == 1


def test_busca_en_todos_los_pdfs_si_no_se_indica(entorno):
    r = _buscar(entorno, P3[10:120], pdfs=None)
    assert {c["pdf"] for c in r["coincidencias"]} == {"Manual Vacunas Alfa.pdf", "Manual Vacunas Beta.pdf"}


def test_pdf_ambiguo_lista_candidatos(entorno):
    carpeta, idx = entorno
    with pytest.raises(bc.PdfAmbiguo) as e:
        bc.resolver_pdf("manual vacunas", carpeta)
    assert len(e.value.candidatos) == 2
    with pytest.raises(bc.PdfNoEncontrado):
        bc.resolver_pdf("inexistente", carpeta)
    assert bc.resolver_pdf("ALFA", carpeta).name == "Manual Vacunas Alfa.pdf"


def test_pagina_sin_capa_de_texto_avisa_ocr(tmp_path):
    carpeta = tmp_path / "pdfs"
    carpeta.mkdir()
    doc = fitz.open()
    doc.new_page()  # página vacía: sin capa de texto
    pg = doc.new_page()
    pg.insert_textbox(fitz.Rect(72, 80, 540, 200), P1, fontsize=11)
    doc.save(carpeta / "Mixto.pdf")
    doc.close()
    r = bc.buscar(P1[:100], pdfs="Mixto", carpeta_pdfs=carpeta, carpeta_indices=tmp_path / "i")
    assert any("OCR" in a for a in r["avisos"])
    assert r["coincidencias"][0]["pagina_fisica"] == 2


# ---- verificación ---------------------------------------------------------------------
def test_verificar_literal(entorno):
    carpeta, idx = entorno
    v = bc.verificar_cita_textual(P1[30:160], "Alfa", carpeta, idx)
    assert v["verificada"] and v["literal"] and v["similitud"] == 100 and v["etiqueta_impresa"] == "11"


def test_cifra_alterada_no_se_verifica(entorno):
    carpeta, idx = entorno
    alterada = P2.replace("85 %", "58 %")
    v = bc.verificar_cita_textual(alterada, "Alfa", carpeta, idx)
    assert not v["verificada"] and not v["literal"]
    assert v["cifras_coinciden"] is False and v["similitud"] > 90
    assert v["pagina_fisica"] == 1  # orienta dónde está la frase original


def test_palabra_alterada_bajo_97_no_se_verifica(entorno):
    carpeta, idx = entorno
    v = bc.verificar_cita_textual(P1.replace("trazabilidad completa", "seguimiento parcial"), "Alfa", carpeta, idx)
    assert not v["verificada"]


def test_cita_inventada_no_se_verifica(entorno):
    carpeta, idx = entorno
    v = bc.verificar_cita_textual("La vacunacion domiciliaria elimina por completo el riesgo epidemiologico", "Alfa", carpeta, idx)
    assert not v["verificada"] and v["pagina_fisica"] is None


# ---- formato APA 7 --------------------------------------------------------------------
C_OK = {"etiqueta_impresa": "72", "pagina_fisica": 3, "parrafo_global": 40}
C_NONE = {"etiqueta_impresa": None, "pagina_fisica": 9, "parrafo_global": 40}


def test_apa7_autores():
    assert bc.formatear_cita_apa7(C_OK, "Beck", 2000) == "(Beck, 2000, p. 72)"
    assert bc.formatear_cita_apa7(C_OK, ["Beck", "Fowler"], 2000) == "(Beck y Fowler, 2000, p. 72)"
    assert bc.formatear_cita_apa7(C_OK, ["Beck", "Fowler", "Jeffries"], 2000, "textual") == "(Beck et al., 2000, p. 72)"


def test_apa7_sin_etiqueta_impresa_exige_verificar():
    s = bc.formatear_cita_apa7(C_NONE, ["Pressman"], 2010)
    assert s == "(Pressman, 2010, p. [VERIFICAR: página impresa no determinada; pág. PDF 9])"


def test_apa7_parrafo_para_normas():
    assert bc.formatear_cita_apa7(C_OK, "MINSA", 2018, localizador="parrafo", numero_parrafo=12) == "(MINSA, 2018, párr. 12)"


def test_apa7_tipo_invalido():
    with pytest.raises(ValueError):
        bc.formatear_cita_apa7(C_OK, "Beck", 2000, tipo="otro")


# ---- CLI ------------------------------------------------------------------------------
def test_cli_pdf_ambiguo_sale_2(capsys):
    assert bc.main(["buscar", "algo suficientemente largo", "--pdf", "a"]) == 2
    assert "ambiguo" in capsys.readouterr().err


def test_cli_uso_incorrecto_sale_2():
    assert bc.main(["verificar", "texto"]) == 2  # falta --pdf


# ---- PDF real (solo lectura) ----------------------------------------------------------
PDF_REAL = rutas.PDFS_FUENTES / "Embracing change with extreme programming.pdf"


@pytest.mark.skipif(not PDF_REAL.exists(), reason="PDF real no disponible")
def test_pdf_real_parrafo_literal_y_cifra_alterada(capsys):
    doc = bc.cargar_documento(PDF_REAL)
    par = next(u for u in doc.unidades if u.texto.startswith("the team full-time"))
    cita = par.texto[:200]
    r = bc.buscar(cita, pdfs="Embracing change")
    c = r["coincidencias"][0]
    assert c["tipo"] == "literal" and c["pagina_fisica"] == par.pagina_fisica
    assert c["etiqueta_impresa"] == par.etiqueta_impresa
    v = bc.verificar_cita_textual(cita, "Embracing change")
    assert v["verificada"] and v["literal"]
    assert bc.main(["verificar", cita, "--pdf", "Embracing change"]) == 0
    capsys.readouterr()
    alterada = cita.replace("40-hour", "35-hour")
    assert alterada != cita
    v2 = bc.verificar_cita_textual(alterada, "Embracing change")
    assert not v2["verificada"] and not v2["literal"]
    assert bc.main(["verificar", alterada, "--pdf", "Embracing change", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["verificada"] is False


# ---- defectos corregidos: inversión de sentido, PDFs dañados, contexto en prosa ---------------
def test_palabra_insertada_que_invierte_sentido_no_se_verifica(entorno):
    carpeta, idx = entorno
    inv = P1.replace("permite registrar", "no permite registrar")
    v = bc.verificar_cita_textual(inv, "Alfa", carpeta, idx)
    assert not v["verificada"] and not v["literal"]
    assert "no" in v["tokens_ausentes"] or v["palabras_difieren"]


def test_palabra_sustituida_o_anadida_no_se_verifica(entorno):
    carpeta, idx = entorno
    v = bc.verificar_cita_textual(P1.replace("completa", "incompleta"), "Alfa", carpeta, idx)
    assert not v["verificada"] and v["palabras_difieren"]
    v2 = bc.verificar_cita_textual(P1 + " el equipo", "Alfa", carpeta, idx)
    assert not v2["verificada"]


def test_comparar_palabras_unidad():
    assert bc.comparar_palabras("a b c d e", "a b c d e")["coinciden"]
    assert not bc.comparar_palabras("a b not c d", "a b c d")["coinciden"]
    assert not bc.comparar_palabras("ready tested done", "ready untested done")["coinciden"]
    assert not bc.comparar_palabras("uno dos cuatro", "uno dos tres cuatro")["coinciden"]
    # palabras sobrantes de la fuente en los bordes de la región no cuentan
    assert bc.comparar_palabras("dos tres", "uno dos tres cuatro")["coinciden"]
    # variante mínima de grafía sin cifras distintas se tolera
    assert bc.comparar_palabras("comportamiento del sistema", "comportamiento del sistemas")["coinciden"]
    assert not bc.comparar_palabras("12 minutos", "13 minutos")["coinciden"]


def test_pdf_corrupto_y_cifrado_no_revientan(tmp_path):
    carpeta = tmp_path / "pdfs"
    carpeta.mkdir()
    (carpeta / "Corrupto.pdf").write_bytes(b"esto no es un pdf")
    cif = fitz.open()
    cif.new_page().insert_text((72, 100), "hola mundo secreto bien largo", fontsize=11)
    cif.save(carpeta / "Cifrado.pdf", encryption=fitz.PDF_ENCRYPT_AES_256, owner_pw="o", user_pw="u")
    cif.close()
    _pdf(carpeta / "Sano.pdf", [[P1]])
    idx = tmp_path / "idx"
    for nombre in ("Corrupto", "Cifrado"):
        with pytest.raises(bc.PdfIlegible):
            bc.verificar_cita_textual(P1, nombre, carpeta, idx)
    # buscar en todos: el dañado se omite con aviso y el sano responde
    r = bc.buscar(P1[:100], carpeta_pdfs=carpeta, carpeta_indices=idx)
    assert r["coincidencias"] and r["coincidencias"][0]["pdf"] == "Sano.pdf"
    assert sum("OMITIDO" in a for a in r["avisos"]) == 2


def test_cli_pdf_corrupto_sale_2(tmp_path, monkeypatch, capsys):
    carpeta = tmp_path / "pdfs"
    carpeta.mkdir()
    (carpeta / "Corrupto.pdf").write_bytes(b"basura")
    monkeypatch.setattr(rutas, "PDFS_FUENTES", carpeta)
    assert bc.main(["verificar", "planificacion ano nino prueba larga", "--pdf", "Corrupto"]) == 2
    err = capsys.readouterr().err
    assert "ERROR" in err and "Traceback" not in err


def test_contexto_salta_rotulos_sueltos(tmp_path):
    carpeta = tmp_path / "pdfs"
    carpeta.mkdir()
    doc = fitz.open()
    pg = doc.new_page()
    pg.insert_textbox(fitz.Rect(72, 60, 540, 150), P2, fontsize=11)
    pg.insert_textbox(fitz.Rect(72, 200, 300, 220), "Task", fontsize=11)
    pg.insert_textbox(fitz.Rect(72, 260, 540, 380), P1, fontsize=11)
    doc.save(carpeta / "Ctx.pdf")
    doc.close()
    r = bc.buscar(P1[:120], pdfs="Ctx", carpeta_pdfs=carpeta, carpeta_indices=tmp_path / "i")
    previo = r["coincidencias"][0]["contexto"]["previo"]
    assert previo is not None and previo != "Task" and "consistencia documental" in previo
