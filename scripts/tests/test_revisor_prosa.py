"""Pruebas de scripts/agentes/revisor_prosa.py (textos de PRUEBA en tmp_path)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.agentes import revisor_prosa as rp  # noqa: E402
from scripts.comun import rutas  # noqa: E402

BUENO = ("El tiempo de registro de movimientos constituye un indicador central de la oportunidad de procesamiento. "
         "Según Beck (1999), la retroalimentación frecuente reduce los defectos acumulados durante el desarrollo. "
         "En el personal de inmunizaciones, la demora en la digitación genera descuadres entre el saldo y el stock físico. "
         "Por consiguiente, se midió el intervalo entre la entrega del lote y su registro en el sistema. "
         "Este procedimiento permitió comparar las condiciones previa y posterior a la intervención.")


def _h(texto: str):
    return rp.revisar_parrafo(1, texto)


def _reglas(texto: str) -> set[str]:
    return {h["regla"] for h in _h(texto)}


def test_parrafo_bien_redactado_sin_hallazgos_mayores():
    h = _h(BUENO)
    assert [x for x in h if x["severidad"] == "mayor"] == []
    assert rp.puntaje(h) >= 85


def test_primera_persona_detectada():
    assert "PERSONA" in _reglas("Nosotros realizamos la medición en los centros de acopio durante tres semanas.")
    assert "PERSONA" in _reglas("Obtuvimos resultados favorables en la mayoría de los casos observados.")


def test_primera_persona_dentro_de_cita_textual_no_cuenta():
    assert "PERSONA" not in _reglas('Como afirma Beck (1999), «nosotros creemos en el cambio constante» en el proceso.')


def test_relleno_y_coloquialismos():
    h = _h("Hoy en día, cabe destacar que el sistema es básicamente muy bueno y realmente útil.")
    assert "RELLENO" in {x["regla"] for x in h}
    assert sum(1 for x in h if x["regla"] == "RELLENO") >= 3


def test_oracion_demasiado_larga():
    larga = " ".join(["palabra"] * 60) + "."
    assert "LONGITUD" in _reglas(larga)


def test_parrafo_corto_fuera_de_rango():
    texto = "Primera oración con contenido suficiente para contar palabras. Segunda oración también presente. " * 1
    texto = texto + " ".join(["relleno"] * 30) + "."
    assert "LONGITUD" in _reglas(texto)


def test_aseveracion_sin_cita():
    assert "CITA" in _reglas("El 85 % de los establecimientos presenta descuadres en el inventario de vacunas.")
    assert "CITA" in _reglas("Según la norma técnica, los registros deben conservarse cinco años.")
    assert "CITA" not in _reglas("El 85 % de los establecimientos presenta descuadres (Kigenza et al., 2023).")
    assert "CITA" not in _reglas("Kigenza et al. (2023) reportaron que el 85 % mejoró su concordancia de inventario.")


def test_formato():
    assert "FORMATO" in _reglas("Como señalan Beck & Andres en su obra, el método es iterativo.")
    assert "FORMATO" in _reglas("Pérez et al demostraron la relación entre ambas variables de estudio.")
    assert "FORMATO" in _reglas("Texto con  espacios dobles en medio de la oración.")
    assert "FORMATO" not in _reglas("Como señalan (Beck & Andres, 1999), el método es iterativo.")


def test_marcas_verificar():
    h = _h("El valor es 12 (p. [VERIFICAR: página exacta en Pressman, 2010]) según la obra.")
    assert any(x["regla"] == "VERIFICAR" for x in h)


def test_repeticion_lexica():
    assert "REPETICION" in _reglas("El sistema registra. El sistema valida. El sistema almacena. El sistema reporta datos.")


def test_oraciones_no_se_parten_en_abreviaturas():
    o = rp.oraciones("Según Pérez et al. (2020) y la Dra. Flores, el p. 12 indica 3.5 puntos. Luego se concluyó.")
    assert len(o) == 2


def test_lectura_md_ignora_frontmatter_codigo_y_tablas(tmp_path):
    md = tmp_path / "a.md"
    md.write_text("---\nestado: borrador\n---\n# Título\n\nPárrafo real del texto académico.\n\n```python\nnosotros = 1\n```\n"
                  "| a | b |\n|---|---|\n\n- viñeta\n\nSegundo párrafo real.\n", encoding="utf-8")
    assert [t for _, t in rp.leer_parrafos(md)] == ["Párrafo real del texto académico.", "Segundo párrafo real."]


def test_revisar_archivo_y_cli(tmp_path, capsys):
    md = tmp_path / "a.md"
    md.write_text(BUENO + "\n\nNosotros realizamos todo. Hoy en día es muy importante.\n", encoding="utf-8")
    inf = rp.revisar(md)
    assert inf["parrafos"] == 2 and inf["totales"]["mayor"] >= 1 and inf["peores_parrafos"][0]["parrafo"] == 2
    assert rp.main(["revisar", str(md)]) == 1
    ok = tmp_path / "ok.md"
    ok.write_text(BUENO + "\n", encoding="utf-8")
    assert rp.main(["revisar", str(ok)]) == 0
    assert rp.main(["revisar", str(tmp_path / "no.md")]) == 2
    assert rp.main(["revisar", str(tmp_path)]) == 2
    assert rp.main([]) == 2


def test_conteo_de_palabras(tmp_path):
    md = tmp_path / "r.md"
    md.write_text("uno dos tres cuatro cinco\n\nseis siete\n", encoding="utf-8")
    assert rp.main(["conteo-palabras", str(md), "--esperado", "7"]) == 0
    assert rp.main(["conteo-palabras", str(md), "--esperado", "250"]) == 1


def test_salida_no_pisa_y_respeta_vetos(tmp_path):
    md = tmp_path / "a.md"
    md.write_text(BUENO + "\n", encoding="utf-8")
    out = tmp_path / "inf.md"
    assert rp.main(["revisar", str(md), "--md", "--salida", str(out)]) == 0 and out.exists()
    assert rp.main(["revisar", str(md), "--md", "--salida", str(out)]) == 2
    assert rp.main(["revisar", str(md), "--salida", str(rutas.REFERENCIAS / "x.md")]) == 2


def test_no_modifica_el_texto_y_sin_escrituras_en_codigo(tmp_path):
    import re
    md = tmp_path / "a.md"
    md.write_text("Nosotros hicimos todo.\n", encoding="utf-8")
    antes = md.read_bytes()
    rp.revisar(md)
    assert md.read_bytes() == antes
    codigo = Path(rp.__file__).read_text(encoding="utf-8")
    assert not re.search(r"\.write_text\(|\.write_bytes\(|os\.remove|unlink\(|shutil\.", codigo)
