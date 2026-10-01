# -*- coding: utf-8 -*-
"""Pruebas de descargar_fuente. Sin red: `_get` se sustituye por respuestas simuladas.
Los PDFs y metadatos son fixtures de prueba (no son datos empíricos de la tesis)."""

from __future__ import annotations

import sys
from pathlib import Path

import pymupdf
import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import seguridad  # noqa: E402
from scripts.fuentes import descargar_fuente as df  # noqa: E402

DOI = "10.1234/prueba.2023.001"
TITULO = "Vaccine cold chain management practices in primary health centers"


def crossref_msg(**extra):
    m = {
        "DOI": DOI, "title": [TITULO], "type": "journal-article",
        "author": [{"family": "Ergetie", "given": "Fekadu S."}, {"family": "Kassaw", "given": "Abebe-Tesfaye"}],
        "issued": {"date-parts": [[2023, 5]]}, "container-title": ["Frontiers in Public Health"],
        "volume": "11", "issue": "2", "page": "100-110", "publisher": "Frontiers", "URL": f"https://doi.org/{DOI}",
    }
    m.update(extra)
    return {"message": m}


def hacer_pdf(texto: str, paginas: int = 2) -> bytes:
    doc = pymupdf.open()
    for i in range(paginas):
        p = doc.new_page()
        p.insert_text((72, 100), texto if i == 0 else f"Segunda pagina con contenido de relleno numero {i}" * 2)
    data = doc.tobytes()
    doc.close()
    return data


class Resp:
    def __init__(self, status=200, json_data=None, content=b""):
        self.status_code, self._json, self.content = status, json_data, content

    def json(self):
        if self._json is None:
            raise ValueError("sin json")
        return self._json

    def iter_content(self, chunk_size=1):
        yield self.content


def instalar_red(monkeypatch, rutas_resp: dict):
    """rutas_resp: {subcadena_url: Resp | Exception}. Devuelve la lista de URLs pedidas."""
    pedidas: list[str] = []

    def falso_get(url, **kw):
        pedidas.append(url)
        for clave, val in rutas_resp.items():
            if clave in url:
                if isinstance(val, Exception):
                    raise val
                return val
        return Resp(404)

    monkeypatch.setattr(df, "_get", falso_get)
    return pedidas


@pytest.fixture
def dirs(tmp_path):
    return dict(carpeta_pdfs=tmp_path / "pdfs", carpeta_notas=tmp_path / "notas", carpeta_indices=tmp_path / "idx")


# --- Funciones puras -------------------------------------------------------
@pytest.mark.parametrize("entrada", [DOI, f"https://doi.org/{DOI}", f"doi: {DOI}", f"  HTTP://dx.doi.org/{DOI.upper()} "])
def test_normalizar_doi(entrada):
    assert df.normalizar_doi(entrada) == DOI


def test_normalizar_doi_invalido():
    assert df.normalizar_doi("no es un doi") is None
    assert df.normalizar_doi("") is None


def test_parsear_crossref_y_abstract_jats():
    m = df.parsear_crossref(crossref_msg(abstract="<jats:p>Texto <jats:italic>uno</jats:italic></jats:p>")["message"])
    assert m["anio"] == 2023 and m["titulo"] == TITULO
    assert m["autores"][0] == {"apellido": "Ergetie", "nombre": "Fekadu S."}
    assert m["abstract"] == "Texto uno"


def test_apa7_articulo():
    m = df.parsear_crossref(crossref_msg()["message"])
    assert df.formatear_apa7(m) == (
        f"Ergetie, F. S., & Kassaw, A.-T. (2023). {TITULO}. *Frontiers in Public Health*, *11*(2), 100–110. "
        f"https://doi.org/{DOI}"
    )


def test_apa7_sin_anio_marca_verificar():
    m = df.parsear_crossref(crossref_msg(issued=None)["message"])
    assert "[VERIFICAR" in df.formatear_apa7(m)


def test_apa7_sin_autor_el_titulo_encabeza():
    m = df.parsear_crossref(crossref_msg(author=[])["message"])
    assert df.formatear_apa7(m).startswith(TITULO)


def test_citekey_y_nombre_pdf():
    m = df.parsear_crossref(crossref_msg(author=[{"family": "Peña-Álvarez", "given": "J"}])["message"])
    assert df.generar_citekey(m) == "penaalvarez2023vaccine"
    assert df.nombre_pdf(m) == "Peña-Álvarez - 2023 - vaccine-cold-chain-management-practices.pdf"


def test_validar_pdf_casos():
    meta = df.parsear_crossref(crossref_msg()["message"])
    assert df.validar_pdf(hacer_pdf(TITULO), meta)["ok"]
    assert "%PDF-" in df.validar_pdf(b"<html>no soy pdf</html>", meta)["motivo"]
    otro = df.validar_pdf(hacer_pdf("Quantum chromodynamics lattice simulations of baryon spectra and gluon fields"), meta)
    assert not otro["ok"] and "figuran" in otro["motivo"]
    vacio = pymupdf.open()
    vacio.new_page()
    assert "requiere OCR" in df.validar_pdf(vacio.tobytes(), meta)["motivo"]


# --- Red simulada ----------------------------------------------------------
def test_verificar_404_no_verificada(monkeypatch):
    instalar_red(monkeypatch, {"crossref": Resp(404)})
    r = df.verificar_doi(DOI)
    assert r["estado"] == "no_verificada" and not r["verificado"] and r["metadatos"] is None


def test_verificar_error_de_red(monkeypatch):
    instalar_red(monkeypatch, {"crossref": requests.ConnectionError("caido")})
    r = df.verificar_doi(DOI)
    assert r["estado"] == "error_red" and "[VERIFICAR" in r["avisos"][0]


def test_verificar_doi_invalido():
    assert df.verificar_doi("xyz")["estado"] == "doi_invalido"


def test_get_reintenta_en_429(monkeypatch):
    llamadas = []

    def falso(url, **kw):
        llamadas.append(1)
        return Resp(429) if len(llamadas) < 3 else Resp(200, {"ok": 1})

    monkeypatch.setattr(df.requests, "get", falso)
    monkeypatch.setattr(df.time, "sleep", lambda s: None)
    assert df._get("http://x").status_code == 200 and len(llamadas) == 3


def test_flujo_completo(monkeypatch, dirs):
    pedidas = instalar_red(monkeypatch, {
        "crossref": Resp(200, crossref_msg(abstract="<jats:p>Resumen de prueba.</jats:p>")),
        "openalex": Resp(200, {"best_oa_location": {"pdf_url": "https://oa.test/a.pdf", "is_oa": True}}),
        "oa.test/a.pdf": Resp(200, content=hacer_pdf(TITULO)),
    })
    r = df.procesar_doi(DOI, **dirs)
    assert r["estado"] == "completado", r
    pdf = Path(r["pdf_local"])
    assert pdf.exists() and pdf.parent == dirs["carpeta_pdfs"] and pdf.name.startswith("Ergetie - 2023 - ")
    ficha = Path(r["ficha"]).read_text(encoding="utf-8")
    assert "verificado: true" in ficha and "Resumen de prueba." in ficha and "[[MOC_01_TESIS_SIVAC]]" in ficha
    assert "## Hallazgos citables" in ficha and "## Referencia APA 7" in ficha and "*Frontiers in Public Health*" in ficha
    assert r["zotero_payload"]["doi"] == DOI and r["zotero_payload"]["pdf_local"] == str(pdf)
    assert list(dirs["carpeta_indices"].glob("*.idx.json"))
    assert not any("unpaywall" in u for u in pedidas)  # sin UNPAYWALL_EMAIL


def test_pdf_equivocado_se_descarta(monkeypatch, dirs):
    instalar_red(monkeypatch, {
        "crossref": Resp(200, crossref_msg()),
        "openalex": Resp(200, {"open_access": {"oa_url": "https://oa.test/mal.pdf"}}),
        "oa.test": Resp(200, content=hacer_pdf("Quantum chromodynamics lattice simulations of baryon spectra and gluon fields")),
    })
    r = df.procesar_doi(DOI, **dirs)
    assert r["estado"] == "sin_pdf" and r["pdf_local"] is None and r["pdf_rechazados"]
    assert not list(dirs["carpeta_pdfs"].glob("*.pdf")) if dirs["carpeta_pdfs"].exists() else True
    ficha = Path(r["ficha"]).read_text(encoding="utf-8")
    assert "verificado: true" in ficha and "pdf_local: null" in ficha
    assert "PDF no disponible en acceso abierto: solicitar al tesista" in ficha
    assert "Abstract no disponible" in ficha


def test_sin_url_oa(monkeypatch, dirs):
    instalar_red(monkeypatch, {"crossref": Resp(200, crossref_msg()), "openalex": Resp(404)})
    r = df.procesar_doi(DOI, **dirs)
    assert r["estado"] == "sin_pdf" and r["zotero_payload"]["tags"][-1] == "sin-pdf"


def test_html_en_lugar_de_pdf(monkeypatch, dirs):
    instalar_red(monkeypatch, {
        "crossref": Resp(200, crossref_msg()),
        "openalex": Resp(200, {"best_oa_location": {"pdf_url": "https://oa.test/x.pdf", "is_oa": True}}),
        "oa.test": Resp(200, content=b"<html>login</html>"),
    })
    r = df.procesar_doi(DOI, **dirs)
    assert r["pdf_local"] is None and "%PDF-" in r["pdf_rechazados"][0]["motivo"]


def test_abstract_desde_openalex(monkeypatch, dirs):
    instalar_red(monkeypatch, {
        "crossref": Resp(200, crossref_msg()),
        "openalex": Resp(200, {"abstract_inverted_index": {"Hola": [0], "mundo": [1]}}),
    })
    ficha = Path(df.procesar_doi(DOI, **dirs)["ficha"]).read_text(encoding="utf-8")
    assert "Hola mundo" in ficha and "OpenAlex" in ficha


def test_unpaywall_solo_con_email(monkeypatch, dirs):
    monkeypatch.setenv("UNPAYWALL_EMAIL", "a@b.org")
    pedidas = instalar_red(monkeypatch, {
        "crossref": Resp(200, crossref_msg()), "openalex": Resp(404),
        "unpaywall": Resp(200, {"best_oa_location": {"url_for_pdf": "https://oa.test/u.pdf"}}),
        "oa.test/u.pdf": Resp(200, content=hacer_pdf(TITULO)),
    })
    assert df.procesar_doi(DOI, **dirs)["estado"] == "completado"
    assert any("unpaywall" in u for u in pedidas)


def test_no_pisa_ficha_ni_duplica_pdf(monkeypatch, dirs):
    red = {
        "crossref": Resp(200, crossref_msg()),
        "openalex": Resp(200, {"best_oa_location": {"pdf_url": "https://oa.test/a.pdf", "is_oa": True}}),
        "oa.test": Resp(200, content=hacer_pdf(TITULO)),
    }
    instalar_red(monkeypatch, red)
    r1 = df.procesar_doi(DOI, **dirs)
    contenido = Path(r1["ficha"]).read_text(encoding="utf-8")
    r2 = df.procesar_doi(DOI, **dirs)  # misma fuente: detecta ficha por DOI
    assert r2["estado"] == "ficha_existente" and Path(r1["ficha"]).read_text(encoding="utf-8") == contenido
    assert len(list(dirs["carpeta_pdfs"].glob("*.pdf"))) == 1


def test_crear_ficha_colision_de_citekey(dirs):
    meta = df.parsear_crossref(crossref_msg()["message"])
    datos = {"verificado": True, "pdf_local": None}
    f1 = df.crear_ficha(meta, "ergetie2023vaccine", datos, dirs["carpeta_notas"])
    f2 = df.crear_ficha(meta, "ergetie2023vaccine", datos, dirs["carpeta_notas"])
    assert f1.name == "@ergetie2023vaccine.md" and f2.name == "@ergetie2023vaccine_2.md"


def test_guardar_pdf_mismo_sha_no_duplica(tmp_path):
    meta = df.parsear_crossref(crossref_msg()["message"])
    data = hacer_pdf(TITULO)
    p1, dup1 = df.guardar_pdf(data, meta, tmp_path)
    p2, dup2 = df.guardar_pdf(data, meta, tmp_path)
    assert p1 == p2 and not dup1 and dup2
    p3, _ = df.guardar_pdf(hacer_pdf(TITULO, paginas=3), meta, tmp_path)  # otro contenido, mismo nombre
    assert p3 != p1 and len(list(tmp_path.glob("*.pdf"))) == 2


def test_no_escribe_en_rutas_protegidas(dirs):
    from scripts.comun import rutas
    meta = df.parsear_crossref(crossref_msg()["message"])
    with pytest.raises(seguridad.EscrituraProhibida):
        df.guardar_pdf(b"%PDF-1.4", meta, rutas.MODELOS_TESIS)
    with pytest.raises(seguridad.EscrituraProhibida):
        df.crear_ficha(meta, "x", {"verificado": True}, rutas.REFERENCIAS / "modelos_validacion")


def test_cli_verificar_y_lote(monkeypatch, tmp_path, capsys):
    instalar_red(monkeypatch, {"crossref": Resp(200, crossref_msg())})
    assert df.main(["verificar", DOI, "--json"]) == 0
    assert '"estado": "verificada"' in capsys.readouterr().out
    lista = tmp_path / "dois.txt"
    lista.write_text(f"# comentario\n{DOI}\n10.9999/noexiste\n", encoding="utf-8")
    instalar_red(monkeypatch, {f"{DOI}": Resp(200, crossref_msg())})
    assert df.main(["lote", "--archivo", str(lista), "--solo-verificar"]) == 1  # el segundo da 404
    assert "no_verificada" in capsys.readouterr().out
    assert df.main(["lote", "--archivo", str(tmp_path / "nada.txt")]) == 2
    assert df.main([]) == 2


# --- Correcciones del verificador -------------------------------------------
def _cifrado():
    doc = pymupdf.open()
    doc.new_page().insert_text((72, 100), TITULO)
    datos = doc.tobytes(encryption=pymupdf.PDF_ENCRYPT_AES_256, user_pw="x", owner_pw="y")
    doc.close()
    return datos


def test_validar_pdf_cifrado_no_lanza():
    meta = df.parsear_crossref(crossref_msg()["message"])
    v = df.validar_pdf(_cifrado(), meta)
    assert not v["ok"] and "cifrado" in v["motivo"]


def test_procesar_doi_con_pdf_cifrado_no_lanza(monkeypatch, dirs):
    instalar_red(monkeypatch, {
        "crossref": Resp(200, crossref_msg()),
        "openalex": Resp(200, {"best_oa_location": {"pdf_url": "https://oa.test/c.pdf", "is_oa": True}}),
        "oa.test": Resp(200, content=_cifrado()),
    })
    r = df.procesar_doi(DOI, **dirs)
    assert r["estado"] == "sin_pdf" and "cifrado" in r["pdf_rechazados"][0]["motivo"]


def test_lote_no_aborta_por_excepcion(monkeypatch, tmp_path, capsys):
    def explota(doi, **kw):
        if "malo" in doi:
            raise RuntimeError("fallo simulado")
        return {"estado": "verificada", "doi": doi, "entrada": doi, "avisos": []}

    monkeypatch.setattr(df, "procesar_doi", explota)
    lista = tmp_path / "l.txt"
    lista.write_text("10.1/malo\n10.1/bueno\n", encoding="utf-8")
    assert df.main(["lote", "--archivo", str(lista), "--json"]) == 1
    salida = capsys.readouterr().out
    assert "error_inesperado" in salida and "10.1/bueno" in salida and '"verificada"' in salida


def test_titulo_subconjunto_de_palabras_ya_no_valida():
    """Antes token_set_ratio daba 100 si las palabras del título estaban dispersas en el PDF."""
    meta = {"doi": DOI, "titulo": "Vaccine stock management information system"}
    ajeno = ("Vaccine cold chain. Information about stock levels. A management system for hospitals. "
             "Vaccine systems and information flows across the health network, with stock and management notes.")
    assert not df.validar_pdf(hacer_pdf(ajeno), meta)["ok"]


@pytest.mark.parametrize("titulo", ["Data", "Health", "Software Engineering", "Data Quality"])
def test_titulo_generico_no_valida_por_texto(titulo):
    v = df.validar_pdf(hacer_pdf(f"{titulo} systems article about data health and software engineering quality"),
                       {"doi": DOI, "titulo": titulo})
    assert not v["ok"] and "genérico" in v["motivo"]


def test_doi_en_texto_valida_titulo_generico():
    v = df.validar_pdf(hacer_pdf(f"Software Engineering. https://doi.org/{DOI} contenido del articulo"),
                       {"doi": DOI, "titulo": "Software Engineering"})
    assert v["ok"] and v["modo_validacion"] == "doi" and v["doi_en_texto"]


def test_titulo_exacto_valida_sin_doi():
    v = df.validar_pdf(hacer_pdf(TITULO), {"doi": DOI, "titulo": TITULO})
    assert v["ok"] and v["modo_validacion"] == "titulo_exacto"


def _pdfs_reales():
    from scripts.comun import rutas
    return sorted(rutas.PDFS_FUENTES.glob("*.pdf")) if rutas.PDFS_FUENTES.exists() else []


@pytest.mark.skipif(not _pdfs_reales(), reason="bóveda con PDFs no disponible")
def test_pdfs_reales_titulos_ajenos_o_genericos_no_pasan():
    """Solo lectura sobre la bóveda (los 30 PDFs reales): ningún título ajeno/genérico valida un PDF."""
    datos = {p.name: p.read_bytes() for p in _pdfs_reales()}
    for titulo in ("Vaccine stock management information system", "Data Quality in routine health information systems",
                   "Data", "Health", "Software Engineering"):
        ok = [n for n, b in datos.items() if df.validar_pdf(b, {"doi": "10.0000/zz", "titulo": titulo})["ok"]]
        assert ok == [], (titulo, ok)


@pytest.mark.skipif(not _pdfs_reales(), reason="bóveda con PDFs no disponible")
def test_pdfs_reales_titulo_propio_solo_valida_su_pdf():
    """El título real completo (Ergetie et al., 2023, Front. Public Health) acepta únicamente su PDF entre los reales."""
    titulo = ("Vaccine cold chain management practices in primary health centers providing an expanded "
              "immunization program in Northwest Ethiopia: self-reported and actual practice observational study")
    ok = [p.name for p in _pdfs_reales()
          if df.validar_pdf(p.read_bytes(), {"doi": "10.0000/zz", "titulo": titulo})["ok"]]
    assert len(ok) == 1 and ok[0].startswith("Vaccine cold chain management practices")


def test_citekey_apellido_compuesto_completo_y_relleno():
    m = {"autores": [{"apellido": "García Márquez"}], "anio": 2020, "titulo": "La Ñandú del río"}
    assert df.generar_citekey(m) == "garciamarquez2020nandu"
    m2 = {"autores": [{"apellido": "Van der Berg"}], "anio": 2020, "titulo": "Studies of things"}
    assert df.generar_citekey(m2) == "vanderberg2020studies"
    sin = {"autores": [], "anio": None, "titulo": "Some topic"}
    assert df.generar_citekey(sin) == "anonsfsome"
    av = df.avisos_citekey(sin)
    assert len(av) == 2 and all("[VERIFICAR" in a for a in av)
    assert df.avisos_citekey(m) == []


def test_apa7_numero_sin_volumen():
    m = df.parsear_crossref(crossref_msg(volume=None, issue="4")["message"])
    assert "*Frontiers in Public Health*, (4), 100–110" in df.formatear_apa7(m)


def test_apa7_libro_con_edicion_y_capitulo_con_editores():
    libro = {"autores": [{"apellido": "Perez", "nombre": "Juan"}], "anio": 2020, "titulo": "Libro",
             "editorial": "Pub", "edicion": "2", "doi": None}
    assert df.formatear_apa7(libro) == "Perez, J. (2020). *Libro* (2nd ed.). Pub."
    cap = df.parsear_crossref({"DOI": "10.1/x", "title": ["Capitulo uno"], "type": "book-chapter",
                               "author": [{"family": "Diaz", "given": "Ana"}], "issued": {"date-parts": [[2019]]},
                               "container-title": ["Manual de vacunas"], "publisher": "Editorial X", "page": "10-20",
                               "editor": [{"family": "Lopez", "given": "Maria"}, {"family": "Ruiz", "given": "Pedro"}]})
    assert df.formatear_apa7(cap) == (
        "Diaz, A. (2019). Capitulo uno. In M. Lopez & P. Ruiz (Eds.), *Manual de vacunas* (pp. 10–20). "
        "Editorial X. https://doi.org/10.1/x")


def test_rollback_pdf_si_falla_la_ficha(monkeypatch, dirs):
    instalar_red(monkeypatch, {
        "crossref": Resp(200, crossref_msg()),
        "openalex": Resp(200, {"best_oa_location": {"pdf_url": "https://oa.test/a.pdf", "is_oa": True}}),
        "oa.test": Resp(200, content=hacer_pdf(TITULO)),
    })

    def falla(*a, **k):
        raise OSError("disco lleno")

    monkeypatch.setattr(df, "crear_ficha", falla)
    r = df.procesar_doi(DOI, **dirs)
    assert r["estado"] == "error_ficha" and r["pdf_local"] is None
    assert not list(dirs["carpeta_pdfs"].glob("*.pdf"))
    assert any("[VERIFICAR" in a for a in r["avisos"])


def test_ficha_previa_informa_pdf_local(monkeypatch, dirs):
    instalar_red(monkeypatch, {
        "crossref": Resp(200, crossref_msg()),
        "openalex": Resp(200, {"best_oa_location": {"pdf_url": "https://oa.test/a.pdf", "is_oa": True}}),
        "oa.test": Resp(200, content=hacer_pdf(TITULO)),
    })
    r1 = df.procesar_doi(DOI, **dirs)
    r2 = df.procesar_doi(DOI, **dirs)
    assert r2["estado"] == "ficha_existente" and r2["pdf_local"] == r1["pdf_local"]
    assert "pdf-local" in r2["zotero_payload"]["tags"]


def test_ficha_previa_formato_antiguo_no_etiqueta(monkeypatch, dirs):
    dirs["carpeta_notas"].mkdir(parents=True)
    (dirs["carpeta_notas"] / "@viejo.md").write_text(f'---\ndoi: "{DOI}"\n---\n# viejo\n', encoding="utf-8")
    instalar_red(monkeypatch, {"crossref": Resp(200, crossref_msg())})
    r = df.procesar_doi(DOI, **dirs)
    assert r["estado"] == "ficha_existente" and r["pdf_local"] is None
    assert "pdf-local" not in r["zotero_payload"]["tags"] and "sin-pdf" not in r["zotero_payload"]["tags"]
    assert any("[VERIFICAR" in a for a in r["avisos"])


# --- Correcciones de la verificación independiente (fixtures de prueba, no datos de la tesis) ---
def test_doi_prefijo_de_otro_doi_no_valida():
    """10.1000/abc es prefijo de 10.1000/abc123456: no debe contar como coincidencia."""
    meta = {"doi": "10.1000/abc", "titulo": "A completely different title about quantum lattice physics"}
    v = df.validar_pdf(hacer_pdf("This paper is about something else entirely, see doi 10.1000/abc123456 for other text here"), meta)
    assert not v["ok"] and not v["doi_en_texto"]


def test_doi_citado_en_referencias_no_valida():
    meta = {"doi": "10.1000/abc", "titulo": "A completely different title about quantum lattice physics"}
    v = df.validar_pdf(hacer_pdf("Unrelated article about other matters entirely. References: Smith J. doi:10.1000/abc more text"), meta)
    assert not v["ok"]


def test_doi_ajeno_primero_y_citado_despues_no_valida():
    meta = {"doi": "10.1000/abc", "titulo": "A completely different title about quantum lattice physics"}
    v = df.validar_pdf(hacer_pdf("Article https://doi.org/10.5555/propio.1 body text that cites also 10.1000/abc in passing"), meta)
    assert not v["ok"]


@pytest.mark.parametrize("texto,esperado", [
    ("Article doi:10.1000/abc. Published 2023", True),
    ("https://doi.org/10.1000/ABC text", True),
    ("doi 10.1000/abc.", True),
    ("doi 10.1000/abc.v2", False),
    ("doi 10.1000/abc123", False),
    ("doi 10.1000/abc-2", False),
    ("", False),
])
def test_doi_propio_en_texto(texto, esperado):
    assert df.doi_propio_en_texto("10.1000/abc", texto) is esperado


def test_citekey_omite_numeros_del_titulo():
    m = {"autores": [{"apellido": "García-Márquez"}], "anio": 2020, "titulo": "The 2020 Vaccine"}
    assert df.generar_citekey(m) == "garciamarquez2020vaccine"
