"""Pruebas de scripts/agentes/guardian_consistencia.py (archivos de PRUEBA en tmp_path)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.agentes import guardian_consistencia as g  # noqa: E402
from scripts.comun import rutas  # noqa: E402


def _reglas(txt: str, nombre: str = "a.md") -> set[str]:
    return {h["regla"] for h in g.analizar(Path(nombre), txt.splitlines(), nombre)}


def _hall(txt: str, nombre: str = "a.md") -> list[dict]:
    return g.analizar(Path(nombre), txt.splitlines(), nombre)


# --- título -----------------------------------------------------------------
def test_titulo_oficial_no_genera_hallazgos():
    assert "TITULO" not in _reglas(f"Título: {rutas.TITULO_OFICIAL}")
    con_comillas_rectas = rutas.TITULO_OFICIAL.replace("“", '"').replace("”", '"')
    assert "TITULO" not in _reglas("*" + con_comillas_rectas + "*")


def test_titulo_antiguo_detectado():
    h = _hall("Sistema web SIVAC y su influencia en la gestión de movimientos de vacunas")
    assert h and h[0]["regla"] == "TITULO" and h[0]["severidad"] == "mayor"


def test_titulo_deformado_detectado():
    assert "TITULO" in _reglas("APLICACIÓN DEL SISTEMA “SIVAC” PARA OPTIMIZAR EL CONTROL DE INSUMOS DE SALUD EN EL PERSONAL")


def test_titulo_con_anio_adosado_es_menor():
    h = _hall(rutas.TITULO_OFICIAL + ", ANDAHUAYLAS 2025")
    assert any(x["regla"] == "TITULO" and x["severidad"] == "menor" for x in h)


# --- autoría ----------------------------------------------------------------
def test_autoria():
    assert "AUTORIA" not in _reglas(f"Tesista: {rutas.TESISTA}. Asesora: {rutas.ASESORA}")
    assert "AUTORIA" in _reglas("Autor: Bach. Juan Pérez Gómez")
    assert "AUTORIA" in _reglas("Asesora: Dra. María López Ruiz")


# --- DEC-007 ----------------------------------------------------------------
def test_dec007():
    assert "DEC007" not in _reglas("Las tres dimensiones de la variable dependiente son oportunidad, consistencia y satisfacción.")
    assert "DEC007" in _reglas("La dimensión fiabilidad del sistema mide la disponibilidad.")
    assert "DEC007" in _reglas("La variable dependiente tiene cuatro dimensiones.")
    assert "DEC007" not in _reglas("El modelo tiene cuatro dimensiones de calidad ISO.")   # no es la VD


# --- diseño / ISO -----------------------------------------------------------
def test_n_censal():
    assert "DISENO" not in _reglas("La muestra censal es N = n = 14 trabajadores.")
    assert "DISENO" in _reglas("La muestra fue de n = 30 trabajadores.")
    assert "DISENO" in _reglas("Se trabajó con una muestra de 20 participantes.")
    assert "DISENO" not in _reglas("Se aplicó n = 30 iteraciones del algoritmo.")   # sin contexto de muestra


def test_iso():
    assert "ISO" not in _reglas("Evaluado con ISO/IEC 25010:2023.")
    assert "ISO" not in _reglas("Norma ISO/IEC 25010 sin edición.")
    assert "ISO" in _reglas("Calidad según ISO/IEC 25010:2011.")


# --- inferencia prematura ---------------------------------------------------
def test_inferencia_prematura_es_critica():
    h = _hall("Se obtuvo W = 0.0, Z = -3.297 y p = .00049; r = 0.623.")
    crit = [x for x in h if x["regla"] == "INFERENCIA"]
    assert crit and crit[0]["severidad"] == "critico"


def test_inferencia_validada_con_datos_reales_se_exime():
    txt = "---\nestado: validado_con_datos_reales\n---\nW = 0.0, Z = -3.297, p = .00049"
    assert "INFERENCIA" not in _reglas(txt)


def test_umbrales_y_formulas_no_son_resultados():
    assert "INFERENCIA" not in _reglas("Si p > 0.05 la distribución es normal; se exige p < .05 y r = |Z|/sqrt(n).")
    assert "INFERENCIA" not in _reglas("Un solo estadístico aislado: p = .032")   # requiere >= 2 tipos distintos


# --- dictámenes -------------------------------------------------------------
def test_dictamen_con_puntaje_es_mayor():
    h = _hall("Dictamen del jurado simulado\nCalificación: 19.75 / 20.0", "DICTAMEN_X.md")
    assert any(x["regla"] == "DICTAMEN" and x["severidad"] == "mayor" for x in h)
    assert "DICTAMEN" not in _reglas("Receta de cocina 3/20 de taza", "receta.md")


# --- escaneo, exclusiones, CLI ----------------------------------------------
def test_escanear_respeta_exclusiones(tmp_path):
    mal = "Sistema web SIVAC y su influencia en la gestión\n"
    (tmp_path / "ok.md").write_text("Sin problemas.\n", encoding="utf-8")
    (tmp_path / "mal.md").write_text(mal, encoding="utf-8")
    for d in ("_cuarentena_no_empiricos", ".git", "referencias", "tests"):
        (tmp_path / d).mkdir()
        (tmp_path / d / "x.md").write_text(mal, encoding="utf-8")
    inf = g.escanear(tmp_path)
    assert inf["archivos_leidos"] == 2 and inf["totales"]["mayor"] == 1
    assert g.escanear(tmp_path, incluir_cuarentena=True)["totales"]["mayor"] == 2


def test_escanear_docx(tmp_path):
    from docx import Document
    d = Document()
    d.add_paragraph("Sistema web SIVAC y su influencia en la gestión")
    t = d.add_table(rows=1, cols=1)
    t.cell(0, 0).text = "Tesista: Bach. Pedro Ramos Soto"
    d.save(str(tmp_path / "a.docx"))
    reglas = {h["regla"] for h in g.escanear(tmp_path)["hallazgos"]}
    assert {"TITULO", "AUTORIA"} <= reglas


def test_cli_codigos_de_salida(tmp_path, capsys):
    (tmp_path / "limpio.md").write_text("Texto neutro.\n", encoding="utf-8")
    assert g.main(["escanear", str(tmp_path)]) == 0
    (tmp_path / "crit.md").write_text("W = 1.5, Z = 2.1, p = .03\n", encoding="utf-8")
    assert g.main(["escanear", str(tmp_path)]) == 1
    assert g.main(["escanear", str(tmp_path / "noexiste")]) == 2
    assert g.main([]) == 2


def test_cli_salida_no_pisa_y_respeta_vetos(tmp_path):
    (tmp_path / "a.md").write_text("ok\n", encoding="utf-8")
    out = tmp_path / "informe.md"
    assert g.main(["escanear", str(tmp_path), "--md", "--salida", str(out)]) == 0 and out.exists()
    assert g.main(["escanear", str(tmp_path), "--md", "--salida", str(out)]) == 2
    assert g.main(["escanear", str(tmp_path), "--salida", str(rutas.REFERENCIAS / "x.md")]) == 2


def test_no_modifica_lo_escaneado(tmp_path):
    f = tmp_path / "a.md"
    f.write_text("Sistema web SIVAC y su influencia en la gestión\n", encoding="utf-8")
    antes = f.read_bytes()
    g.escanear(tmp_path)
    assert f.read_bytes() == antes


def test_codigo_sin_escrituras_sobre_lo_escaneado():
    import re
    codigo = Path(g.__file__).read_text(encoding="utf-8")
    assert not re.search(r"\.write_text\(|\.write_bytes\(|os\.remove|unlink\(|shutil\.|open\([^)]*['\"][wax]", codigo)


def test_preguntas_y_objetivos_no_son_el_titulo():
    # Formulaciones legítimas de la matriz de consistencia: NO deben marcarse como título distinto.
    for s in ('¿En qué medida la aplicación del sistema "SIVAC" mejora la gestión de movimientos de vacunas?',
              'Determinar en qué medida la aplicación del sistema SIVAC mejora la oportunidad de procesamiento.',
              'La aplicación del sistema “SIVAC” mejora significativamente la consistencia documental.'):
        assert "TITULO" not in _reglas(s), s


def test_fiabilidad_psicometrica_no_es_dimension_ajena():
    assert "DEC007" not in _reglas("El análisis de fiabilidad mediante alfa de Cronbach de la dimensión 3 del cuestionario.")
    assert "DEC007" in _reglas("La segunda dimensión de la variable es la fiabilidad del inventario.")


def test_n_de_estudio_citado_se_degrada_a_menor():
    h = _hall("Astuhuaman y Baltazar (2024) trabajaron con una muestra de 596 participantes.")
    assert [x["severidad"] for x in h if x["regla"] == "DISENO"] == ["menor"]
    h = _hall("Se trabajó con una muestra de 30 trabajadores.")
    assert [x["severidad"] for x in h if x["regla"] == "DISENO"] == ["mayor"]
