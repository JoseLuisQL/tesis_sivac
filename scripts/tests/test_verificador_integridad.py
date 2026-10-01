# -*- coding: utf-8 -*-
"""Pruebas del verificador de integridad.

Todo el texto es un FIXTURE DE PRUEBA con defectos sembrados; no son datos empíricos de la tesis.
Sin red: Crossref y el buscador de citas se sustituyen por dobles.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.agentes import verificador_integridad as vi  # noqa: E402

TEXTO_PRUEBA = """---
tipo: borrador
---
# Capítulo de prueba

Los sistemas web mejoran los tiempos de registro (Mego, 2021). Asimismo, Duryea et al. (2021) hallaron
mejoras en la asistencia a controles. Varios estudios lo confirman (Mego y Pérez, 2021; Ramos, 2019, p. 12).

La cobertura alcanzó 85 % en el periodo observado y además se reportó una mejora sustancial.

Según el modelo, la utilidad percibida es determinante. Sin embargo, no se menciona ninguna fuente.

Un autor señaló que «el sistema reduce de forma significativa los tiempos de registro de vacunas» (Mego, 2021, p. 5).

Un caso sin respaldo (Fantasma, 2020) y uno con año distinto (Ramos, 2018).

Pendiente de revisar [VERIFICAR: página exacta de la cifra].

## Referencias

Duryea, E. L., Adhikari, E. H., & Nelson, D. B. (2021). Comparison between in-person and audio-only virtual prenatal visits. *JAMA Network Open*, 4(4). https://doi.org/10.1001/jamanetworkopen.2021.5854

Mego, A. (2021). Sistema web con XP en COVID. *Revista X*, 1(1). https://doi.org/10.9999/inexistente.123

Ramos, J. (2019). Gestión de vacunas. *Revista Y*, 2(2).

Huérfano, P. (2017). Una referencia que nadie cita. *Revista Z*, 3(3).
"""


@pytest.fixture
def md_prueba(tmp_path):
    p = tmp_path / "capitulo_prueba.md"
    p.write_text(TEXTO_PRUEBA, encoding="utf-8")
    return p


def _crossref_falso(doi: str) -> dict:
    if "inexistente" in doi:
        return {"existe": False, "error": "HTTP 404 (DOI no registrado en Crossref)"}
    return {"existe": True, "titulo": "Comparison between in-person and audio-only virtual prenatal visits",
            "autor1": "Duryea", "anios": ["2021"], "error": None}


# --------------------------------------------------------------------------------------------
# Separación de secciones
# --------------------------------------------------------------------------------------------
def test_divide_cuerpo_y_referencias(md_prueba):
    lineas = vi.leer_lineas(md_prueba)
    cuerpo, refs, hallada = vi.dividir_cuerpo_y_referencias(lineas)
    assert hallada
    assert all("Huérfano" not in ln["texto"] for ln in cuerpo)
    assert any("Huérfano" in ln["texto"] for ln in refs)


def test_sin_seccion_referencias():
    lineas = vi._leer_md("# Título\n\nTexto sin referencias (Autor, 2020).\n")
    _, refs, hallada = vi.dividir_cuerpo_y_referencias(lineas)
    assert not hallada and refs == []


def test_encabezado_referencias_mayusculas():
    lineas = vi._leer_md("# REFERENCIAS BIBLIOGRÁFICAS\n\nPérez, J. (2020). Título. *R*, 1(1).\n")
    _, lin_refs, hallada = vi.dividir_cuerpo_y_referencias(lineas)
    assert hallada and len(vi.parsear_referencias(lin_refs)) == 1


# --------------------------------------------------------------------------------------------
# Extracción de citas
# --------------------------------------------------------------------------------------------
def _citas(texto: str) -> list[dict]:
    return vi.extraer_citas(vi.construir_bloques(vi._leer_md(texto)))


def test_cita_parentetica_simple():
    c = _citas("Texto (Mego, 2021).")
    assert len(c) == 1 and c[0]["autor1"] == "Mego" and c[0]["anio"] == "2021"


def test_cita_dos_autores_y_et_al():
    c = _citas("Uno (Mego y Pérez, 2021) y otro (Duryea et al., 2021).")
    assert c[0]["autores"] == ["Mego", "Pérez"]
    assert c[1]["autor1"] == "Duryea" and c[1]["et_al"]


def test_citas_multiples_con_punto_y_coma_y_pagina():
    c = _citas("Varios (Mego, 2021; Ramos, 2019, p. 12; Luna, 2020, pp. 3-5).")
    assert [x["autor1"] for x in c] == ["Mego", "Ramos", "Luna"]
    assert c[1]["localizador"] == "12" and c[2]["localizador"] == "3-5"


def test_cita_narrativa():
    c = _citas("Como señaló Duryea et al. (2021, p. 7) la asistencia mejoró.")
    assert len(c) == 1 and c[0]["tipo"] == "narrativa"
    assert c[0]["autor1"] == "Duryea" and c[0]["localizador"] == "7"


def test_citekeys_pandoc():
    c = _citas("Resultado [@Mego2021; @Ramos2019, p. 4] y también @Luna2020.")
    claves = sorted(x["citekey"] for x in c)
    assert claves == ["Luna2020", "Mego2021", "Ramos2019"]


def test_no_confunde_tabla_ni_figura_con_cita():
    assert _citas("Se muestra en (Tabla 2020, 2021) y (Figura 3, 2020).") == []


# --------------------------------------------------------------------------------------------
# Referencias y emparejamiento
# --------------------------------------------------------------------------------------------
def test_parsear_referencia_extrae_autor_anio_doi():
    r = vi.parsear_referencia(
        "Duryea, E. L., Adhikari, E. H., & Nelson, D. B. (2021). Un título. *JAMA*, 4(4). "
        "https://doi.org/10.1001/jamanetworkopen.2021.5854")
    assert r["autor1"] == "Duryea" and r["anio"] == "2021"
    assert r["doi"] == "10.1001/jamanetworkopen.2021.5854"
    assert r["autores"][:3] == ["Duryea", "Adhikari", "Nelson"]


def test_emparejar_detecta_sin_referencia_huerfana_y_anio(md_prueba):
    inf = vi.auditar(md_prueba, sin_red=True, usar_boveda=False)
    codigos = [h["codigo"] for h in inf["hallazgos"]]
    assert "CITA_SIN_REFERENCIA" in codigos
    assert "REFERENCIA_HUERFANA" in codigos
    assert "DISCREPANCIA_ANIO" in codigos
    sin_ref = [h for h in inf["hallazgos"] if h["codigo"] == "CITA_SIN_REFERENCIA"]
    assert any("Fantasma" in h["mensaje"] for h in sin_ref)
    huerfanas = [h for h in inf["hallazgos"] if h["codigo"] == "REFERENCIA_HUERFANA"]
    assert any("Huérfano" in h["mensaje"] for h in huerfanas)


def test_tolerancia_de_grafia_tildes():
    citas = _citas("Texto (Perez, 2020).")
    refs = [vi.parsear_referencia("Pérez, J. (2020). Título. *R*, 1(1).", 1)]
    emp = vi.emparejar(citas, refs)
    assert emp["hallazgos"] == [] and emp["usadas"] == {0}


def test_coincide_apellido_compuesto():
    assert vi.coincide_apellido("Catacora", "Catacora Flores") == 100
    assert vi.coincide_apellido("Mego", "Zapata") < 90


# --------------------------------------------------------------------------------------------
# DOI
# --------------------------------------------------------------------------------------------
def test_doi_inexistente_es_alerta_roja(md_prueba):
    inf = vi.auditar(md_prueba, sin_red=False, usar_boveda=False, consultor=_crossref_falso)
    rojos = [h["codigo"] for h in inf["hallazgos"] if h["severidad"] == vi.ROJA]
    assert "DOI_INEXISTENTE" in rojos
    assert inf["dictamen"] == vi.BLOQUEADO
    assert inf["resumen"]["dois_inexistentes"] == 1


def test_doi_sin_red_no_consulta(md_prueba):
    def prohibido(_doi):  # pragma: no cover
        raise AssertionError("no debe consultarse la red con --sin-red")

    inf = vi.auditar(md_prueba, sin_red=True, usar_boveda=False, consultor=prohibido)
    assert all("no comprobado" in f["crossref"] for f in inf["doi"] if f["doi"])
    assert "DOI_INEXISTENTE" not in [h["codigo"] for h in inf["hallazgos"]]


def test_doi_formato_invalido():
    ref = vi.parsear_referencia("Luna, A. (2020). T. *R*. https://doi.org/10.1234/abc", 1)
    ref["doi_bruto"] = "10.12/x"  # registrante de 2 dígitos: formato inválido
    filas, hs = vi.validar_dois([ref], True)
    assert filas[0]["formato"] is False and filas[0]["crossref"] == "formato inválido"
    assert [h["codigo"] for h in hs] == ["DOI_FORMATO"]


def test_referencia_sin_doi_se_marca():
    filas, hs = vi.validar_dois([vi.parsear_referencia("Luna, A. (2020). T. *R*, 1(1).", 1)], True)
    assert filas[0]["crossref"] == "sin DOI" and hs == []


def test_comparar_con_crossref_detecta_discrepancias():
    ref = {"autor1": "Zapata", "anio": "2019", "titulo": "Un tema completamente distinto de lo publicado"}
    meta = {"autor1": "Duryea", "anios": ["2021"], "titulo": "Comparison between in-person and audio-only visits"}
    d = vi.comparar_con_crossref(ref, meta)
    assert len(d) == 3


def test_crossref_error_de_red_es_no_comprobado(monkeypatch):
    import requests

    def falla(*a, **k):
        raise requests.ConnectionError("sin conexión")

    monkeypatch.setattr(requests, "get", falla)
    r = vi.consultar_crossref("10.1000/xyz")
    assert r["existe"] is None and "ConnectionError" in r["error"]


def test_crossref_404_es_inexistente(monkeypatch):
    import requests

    class R:
        status_code = 404

    monkeypatch.setattr(requests, "get", lambda *a, **k: R())
    assert vi.consultar_crossref("10.1000/xyz")["existe"] is False


# --------------------------------------------------------------------------------------------
# Aserciones sin cita y [VERIFICAR]
# --------------------------------------------------------------------------------------------
def test_asercion_sin_cita_y_con_cita_en_siguiente():
    texto = ("La cobertura alcanzó 85 % en el periodo. No hay fuente.\n\n"
             "La prevalencia fue de 40 %. Esto se sustenta en (Mego, 2021).\n")
    bl = vi.construir_bloques(vi._leer_md(texto))
    ases = vi.detectar_aserciones_sin_cita(bl, vi.extraer_citas(bl))
    assert len(ases) == 1 and "85" in ases[0]["oracion"]


def test_segun_sin_cita_se_detecta(md_prueba):
    inf = vi.auditar(md_prueba, sin_red=True, usar_boveda=False)
    assert any("según" in " ".join(a["disparadores"]) for a in inf["aserciones_sin_cita"])


def test_referencias_internas_no_disparan():
    bl = vi.construir_bloques(vi._leer_md("Como se muestra en la Tabla 12 y la Figura 3 del capítulo 2.\n"))
    assert vi.detectar_aserciones_sin_cita(bl, []) == []


def test_marcas_verificar(md_prueba):
    inf = vi.auditar(md_prueba, sin_red=True, usar_boveda=False)
    assert inf["resumen"]["marcas_verificar"] == 1
    assert "página exacta" in inf["verificar"][0]["marca"]


# --------------------------------------------------------------------------------------------
# Citas textuales
# --------------------------------------------------------------------------------------------
class _BuscadorFalso:
    def __init__(self, verificada: bool, etiqueta="5"):
        self.verificada, self.etiqueta = verificada, etiqueta

    def verificar_cita_textual(self, fragmento, pdf):
        return {"verificada": self.verificada, "similitud": 100.0 if self.verificada else 40.0,
                "etiqueta_impresa": self.etiqueta, "pagina_fisica": 5, "motivo": "simulado", "avisos": []}


def _bloques_y_citas(texto):
    bl = vi.construir_bloques(vi._leer_md(texto))
    return bl, vi.extraer_citas(bl)


TXT_TEXTUAL = ("Se afirmó que «el sistema reduce de forma significativa los tiempos de registro de vacunas» "
               "(Mego, 2021, p. 5).\n")
REF_MEGO = [vi.parsear_referencia("Mego, A. (2021). Sistema web. *R*, 1(1).", 1)]


def _resolver(citas):
    vi.emparejar(citas, REF_MEGO)
    return [{"referencia": "Mego (2021)", "pdf": "mego.pdf", "_pdf_ruta": "/tmp/mego.pdf"}]


def test_cita_textual_no_hallada_es_roja():
    bl, citas = _bloques_y_citas(TXT_TEXTUAL)
    filas = _resolver(citas)
    res, hs = vi.verificar_citas_textuales(bl, citas, REF_MEGO, filas, buscador=_BuscadorFalso(False))
    assert res[0]["estado"] == "no_hallada"
    assert [h["codigo"] for h in hs if h["severidad"] == vi.ROJA] == ["CITA_TEXTUAL_NO_HALLADA"]


def test_cita_textual_verificada_sin_hallazgos():
    bl, citas = _bloques_y_citas(TXT_TEXTUAL)
    filas = _resolver(citas)
    res, hs = vi.verificar_citas_textuales(bl, citas, REF_MEGO, filas, buscador=_BuscadorFalso(True))
    assert res[0]["estado"] == "verificada" and hs == []


def test_cita_textual_pagina_distinta():
    bl, citas = _bloques_y_citas(TXT_TEXTUAL)
    filas = _resolver(citas)
    _, hs = vi.verificar_citas_textuales(bl, citas, REF_MEGO, filas, buscador=_BuscadorFalso(True, etiqueta="9"))
    assert [h["codigo"] for h in hs] == ["CITA_TEXTUAL_PAGINA"]


def test_cita_textual_sin_pdf_es_no_comprobada():
    bl, citas = _bloques_y_citas(TXT_TEXTUAL)
    vi.emparejar(citas, REF_MEGO)
    filas = [{"referencia": "Mego (2021)", "pdf": None, "_pdf_ruta": None}]
    res, hs = vi.verificar_citas_textuales(bl, citas, REF_MEGO, filas, buscador=_BuscadorFalso(True))
    assert res[0]["estado"] == "no_comprobado"
    assert all(h["severidad"] != vi.ROJA for h in hs)


def test_titulo_entre_comillas_no_es_cita_textual():
    bl, citas = _bloques_y_citas(
        "El estudio titulado «Sistema web para la gestión de vacunas en el sector salud» (Mego, 2021) es citado.\n")
    vi.emparejar(citas, REF_MEGO)
    res, _ = vi.verificar_citas_textuales(bl, citas, REF_MEGO, [{"pdf": None, "_pdf_ruta": None}],
                                          buscador=_BuscadorFalso(True))
    assert res == []


def test_buscador_ausente_marca_no_comprobado(monkeypatch):
    monkeypatch.setattr(vi, "_bc", None)
    bl, citas = _bloques_y_citas(TXT_TEXTUAL)
    filas = _resolver(citas)
    res, _ = vi.verificar_citas_textuales(bl, citas, REF_MEGO, filas)
    assert res[0]["estado"] == "no_comprobado" and "no disponible" in res[0]["detalle"]


# --------------------------------------------------------------------------------------------
# Dictamen, docx y CLI
# --------------------------------------------------------------------------------------------
def test_dictamen_criterios():
    assert vi.dictaminar([]) == vi.APROBADO
    assert vi.dictaminar([{"severidad": vi.OBS}]) == vi.OBSERVADO
    assert vi.dictaminar([{"severidad": vi.INFO}]) == vi.APROBADO
    assert vi.dictaminar([{"severidad": vi.OBS}, {"severidad": vi.ROJA}]) == vi.BLOQUEADO


def test_documento_limpio_aprobado(tmp_path):
    p = tmp_path / "limpio.md"
    p.write_text("# Texto\n\nLa gestión mejoró con el sistema (Ramos, 2019).\n\n## Referencias\n\n"
                 "Ramos, J. (2019). Gestión de vacunas. *Revista Y*, 2(2).\n", encoding="utf-8")
    inf = vi.auditar(p, sin_red=True, usar_boveda=False)
    assert inf["dictamen"] == vi.APROBADO, inf["hallazgos"]


def test_docx_equivale_a_md(tmp_path):
    docx = pytest.importorskip("docx")
    d = docx.Document()
    d.add_heading("Capítulo", 1)
    d.add_paragraph("La gestión mejoró con el sistema (Ramos, 2019). Otra cita (Fantasma, 2020).")
    d.add_heading("Referencias", 1)
    d.add_paragraph("Ramos, J. (2019). Gestión de vacunas. Revista Y, 2(2).")
    ruta = tmp_path / "doc.docx"
    d.save(str(ruta))
    inf = vi.auditar(ruta, sin_red=True, usar_boveda=False)
    assert inf["resumen"]["referencias"] == 1
    assert inf["resumen"]["citas_sin_referencia"] == 1
    assert inf["dictamen"] == vi.BLOQUEADO


def test_catalogo_alterno_cuando_no_hay_referencias(tmp_path):
    cuerpo = tmp_path / "cap.md"
    cuerpo.write_text("# Cap\n\nLa gestión mejoró (Ramos, 2019).\n", encoding="utf-8")
    cat = tmp_path / "cat.md"
    cat.write_text("# Referencias\n\nRamos, J. (2019). Gestión. *R*, 1(1).\n", encoding="utf-8")
    inf = vi.auditar(cuerpo, sin_red=True, catalogo=cat, usar_boveda=False)
    assert inf["resumen"]["citas_sin_referencia"] == 0
    assert "catálogo externo" in inf["resumen"]["origen_referencias"]


def test_cli_json_y_codigos_de_salida(md_prueba, capsys):
    rc = vi.main([str(md_prueba), "--json", "--sin-red", "--sin-boveda"])
    out = json.loads(capsys.readouterr().out)
    assert rc == 1 and out["dictamen"] == vi.BLOQUEADO


def test_cli_uso_incorrecto(tmp_path, capsys):
    assert vi.main([str(tmp_path / "noexiste.md")]) == 2
    assert vi.main([]) == 2


def test_cli_md_y_salida_no_pisa_original(md_prueba, tmp_path, capsys):
    assert vi.main([str(md_prueba), "--md", "--sin-red", "--sin-boveda"]) == 1
    assert "# Informe de integridad" in capsys.readouterr().out
    assert vi.main([str(md_prueba), "--sin-red", "--sin-boveda", "--salida", str(md_prueba)]) == 2
    informe = tmp_path / "informe.md"
    vi.main([str(md_prueba), "--md", "--sin-red", "--sin-boveda", "--salida", str(informe)])
    assert informe.exists()


def test_no_escribe_en_referencias(md_prueba):
    from scripts.comun import rutas, seguridad

    with pytest.raises(seguridad.EscrituraProhibida):
        seguridad.asegurar_no_sobrescribe(md_prueba, rutas.MODELOS_TESIS / "x.md")
