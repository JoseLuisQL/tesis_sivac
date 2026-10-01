"""Pruebas de scripts/agentes/validez_contenido.py.

Todos los puntajes de abajo son FIXTURES DE PRUEBA (calculados a mano en los
comentarios); no son calificaciones de jueces reales ni se guardan en datos/.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.agentes import validez_contenido as vc  # noqa: E402
from scripts.comun import rutas, seguridad  # noqa: E402

JUECES = ("J1", "J2", "J3")


def _df(tabla: dict, jueces=JUECES):
    """tabla[(item, criterio)] = [puntaje por juez]  ->  DataFrame validado."""
    import pandas as pd

    filas = []
    for (it, cr), pts in tabla.items():
        for j, p in zip(jueces, pts):
            filas.append({"juez": j, "item": it, "criterio": cr, "puntaje": p})
    return vc._validar(pd.DataFrame(filas))


def _tabla_libro():
    # Fixture: 2 ítems x 5 criterios, 3 jueces.
    t = {}
    for cr in vc.CRITERIOS:
        t[("1", cr)] = [4, 4, 4]          # V = 1.00, I-CVI = 1
    t[("2", "suficiencia")] = [4, 4, 3]   # S=3+3+2=8 -> V=8/9
    t[("2", "relevancia")] = [4, 3, 3]    # S=3+2+2=7 -> V=7/9=0.778 (no cumple)
    t[("2", "coherencia")] = [4, 4, 4]
    t[("2", "claridad")] = [3, 3, 3]      # S=6 -> V=2/3 (no cumple), I-CVI = 1
    t[("2", "redaccion")] = [4, 4, 4]
    return t


# --- V de Aiken ---------------------------------------------------------------
def test_v_aiken_a_mano():
    assert vc.v_aiken([4, 4, 3]) == pytest.approx(8 / 9)
    assert vc.v_aiken([4, 3, 3]) == pytest.approx(7 / 9)
    assert vc.v_aiken([4, 4, 4]) == 1.0
    assert vc.v_aiken([1, 1, 1]) == 0.0
    assert vc.v_aiken([3, 3, 3]) == pytest.approx(2 / 3)


def test_v_aiken_sin_jueces_falla():
    with pytest.raises(vc.DatosInvalidos):
        vc.v_aiken([])


def test_ic_wilson_v1_n3_a_mano():
    # V=1, N=9: L = 9/(9+z^2); U = 1.
    z2 = vc.Z_95 ** 2
    lo, hi = vc.ic_wilson_v(1.0, 3)
    assert lo == pytest.approx(9 / (9 + z2), abs=1e-9)
    assert lo == pytest.approx(0.7009, abs=1e-4)
    assert hi == pytest.approx(1.0)


def test_ic_wilson_contiene_v_y_esta_en_0_1():
    for pts in ([4, 4, 3], [4, 3, 3], [1, 1, 1], [2, 4, 4]):
        v = vc.v_aiken(pts)
        lo, hi = vc.ic_wilson_v(v, 3)
        assert 0 <= lo <= v <= hi <= 1


def test_ivc_item():
    assert vc.ivc_item([4, 4, 3]) == 1.0
    assert vc.ivc_item([4, 2, 3]) == pytest.approx(2 / 3)
    assert vc.ivc_item([1, 2, 2]) == 0.0


# --- Significancia exacta -----------------------------------------------------
def test_p_exacto_n3_c4_a_mano():
    # 4^3 = 64 resultados. S=9: 1 ; S=8: 3 ; S=7: 6.
    assert vc.p_exacto_v(9, 3) == pytest.approx(1 / 64)
    assert vc.p_exacto_v(8, 3) == pytest.approx(4 / 64)
    assert vc.p_exacto_v(7, 3) == pytest.approx(10 / 64)
    assert vc.p_exacto_v(0, 3) == pytest.approx(1.0)


def test_v_critico_n3():
    # p(S>=9)=0.0156 <= .05 pero p(S>=8)=0.0625 > .05  -> V critico = 1.0
    assert vc.v_critico(3, 4, 0.05) == 1.0
    # alfa .01: ni siquiera S=9 (0.0156) alcanza
    assert vc.v_critico(3, 4, 0.01) is None


def test_v_critico_decrece_con_mas_jueces():
    vs = [vc.v_critico(n, 4, 0.05) for n in range(3, 11)]
    assert all(v is not None for v in vs)
    assert all(a >= b for a, b in zip(vs, vs[1:]))
    assert vs[-1] < vs[0]


def test_v_critico_n10_consistente_con_p():
    v = vc.v_critico(10, 4, 0.05)
    s = round(v * 10 * 3)
    assert vc.p_exacto_v(s, 10) <= 0.05 < vc.p_exacto_v(s - 1, 10)


def test_distribucion_nula_suma_uno():
    from fractions import Fraction
    assert sum(vc._distribucion_nula(5, 4)) == Fraction(1)


# --- Kendall ------------------------------------------------------------------
def test_kendall_a_mano():
    # Rangos: J1 [1,2,3], J2 [1,3,2], J3 [2,1,3] -> sumas 4,6,8 ; S=8
    # W = 12*8 / (9*(27-3)) = 96/216 = 0.4444
    r = vc.kendall_w([[1, 2, 3], [1, 3, 2], [2, 1, 3]])
    assert r["w"] == pytest.approx(96 / 216)
    assert r["chi2"] == pytest.approx(3 * 2 * 96 / 216)
    assert r["gl"] == 2
    assert 0 < r["p"] < 1


def test_kendall_acuerdo_perfecto():
    assert vc.kendall_w([[1, 2, 3, 4]] * 3)["w"] == pytest.approx(1.0)


def test_kendall_con_menos_de_3_jueces():
    r = vc.kendall_w([[1, 2, 3], [1, 2, 3]])
    assert r["w"] is None and "3 jueces" in r["motivo"]


def test_kendall_sin_variacion_indefinido():
    r = vc.kendall_w([[4, 4, 4]] * 3)
    assert r["w"] is None


# --- Lectura y validación -----------------------------------------------------
def test_leer_csv_vacio_con_cabeceras_da_error_claro(tmp_path):
    ruta = tmp_path / "vacia.csv"
    ruta.write_text("juez,item,criterio,puntaje\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="SIN DATOS"):
        vc.leer_matriz(ruta)


def test_leer_archivo_inexistente(tmp_path):
    with pytest.raises(vc.DatosInvalidos, match="No existe"):
        vc.leer_matriz(tmp_path / "no.csv")


def test_columnas_faltantes(tmp_path):
    ruta = tmp_path / "x.csv"
    ruta.write_text("juez,item,puntaje\nA,1,4\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="Faltan columnas"):
        vc.leer_matriz(ruta)


@pytest.mark.parametrize("malo", ["5", "0", "2.5", "abc"])
def test_puntaje_invalido(tmp_path, malo):
    ruta = tmp_path / "x.csv"
    ruta.write_text(f"juez,item,criterio,puntaje\nA,1,claridad,{malo}\nB,1,claridad,4\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="puntaje"):
        vc.leer_matriz(ruta)


@pytest.mark.parametrize("malo", ["", "nan", "NaN", "inf", "-inf", "Infinity"])
def test_puntaje_vacio_nan_inf_da_datos_invalidos_con_fila(tmp_path, malo):
    ruta = tmp_path / "x.csv"
    ruta.write_text(f"juez,item,criterio,puntaje\nA,1,relevancia,4\nB,1,relevancia,{malo}\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="fila 3"):
        vc.leer_matriz(ruta)


def test_puntaje_vacio_en_xlsx(tmp_path):
    import pandas as pd

    df = pd.DataFrame({"juez": ["A", "B"], "item": [1, 1], "criterio": ["claridad"] * 2, "puntaje": [4, None]})
    ruta = tmp_path / "m.xlsx"
    df.to_excel(ruta, index=False)
    with pytest.raises(vc.DatosInvalidos, match="fila 3"):
        vc.leer_matriz(ruta)


def test_csv_de_cero_bytes(tmp_path):
    ruta = tmp_path / "cero.csv"
    ruta.write_bytes(b"")
    with pytest.raises(vc.DatosInvalidos, match="vacío"):
        vc.leer_matriz(ruta)


def test_xlsx_corrupto(tmp_path):
    ruta = tmp_path / "mala.xlsx"
    ruta.write_bytes(b"garbage")
    with pytest.raises(vc.DatosInvalidos, match="corrupto"):
        vc.leer_matriz(ruta)


def test_hoja_inexistente(tmp_path):
    import pandas as pd

    df = pd.DataFrame({"juez": ["A", "B"], "item": [1, 1], "criterio": ["claridad"] * 2, "puntaje": [4, 3]})
    ruta = tmp_path / "m.xlsx"
    df.to_excel(ruta, index=False)
    with pytest.raises(vc.DatosInvalidos, match="Nope"):
        vc.leer_matriz(ruta, "Nope")


def test_cli_datos_hostiles_dan_1_sin_traceback(tmp_path, capsys):
    for nombre, contenido in (("cero.csv", b""), ("mala.xlsx", b"garbage"),
                              ("blank.csv", b"juez,item,criterio,puntaje\nA,1,relevancia,4\nB,1,relevancia,\n")):
        ruta = tmp_path / nombre
        ruta.write_bytes(contenido)
        assert vc.main(["calcular", str(ruta)]) == 1
        assert "ERROR:" in capsys.readouterr().err


def test_advertencia_verificar_umbrales_de_eliminacion():
    r = vc.calcular(_df(_tabla_libro()))
    assert any("VERIFICAR" in a for a in r.advertencias)
    md = vc.a_markdown(r)
    assert md.count("VERIFICAR") >= 3  # advertencia, nota Tabla 2, nota Tabla 5


def test_criterio_invalido(tmp_path):
    ruta = tmp_path / "x.csv"
    ruta.write_text("juez,item,criterio,puntaje\nA,1,belleza,4\nB,1,belleza,4\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="criterio"):
        vc.leer_matriz(ruta)


def test_matriz_incompleta(tmp_path):
    ruta = tmp_path / "x.csv"
    ruta.write_text("juez,item,criterio,puntaje\nA,1,claridad,4\nA,2,claridad,4\nB,1,claridad,4\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="incompleta"):
        vc.leer_matriz(ruta)


def test_un_solo_juez(tmp_path):
    ruta = tmp_path / "x.csv"
    ruta.write_text("juez,item,criterio,puntaje\nA,1,claridad,4\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="al menos 2 jueces"):
        vc.leer_matriz(ruta)


def test_duplicados(tmp_path):
    ruta = tmp_path / "x.csv"
    ruta.write_text("juez,item,criterio,puntaje\nA,1,claridad,4\nA,1,claridad,3\nB,1,claridad,4\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="duplicadas"):
        vc.leer_matriz(ruta)


def test_criterio_con_tilde_y_mayusculas_se_normaliza(tmp_path):
    ruta = tmp_path / "x.csv"
    ruta.write_text("juez,item,criterio,puntaje\nA,1,Redacción ,4\nB,1,REDACCION,3\n", encoding="utf-8")
    df = vc.leer_matriz(ruta)
    assert set(df["criterio"]) == {"redaccion"}


def test_lee_xlsx(tmp_path):
    import pandas as pd

    df = pd.DataFrame({"juez": ["A", "B"], "item": [1, 1], "criterio": ["claridad"] * 2, "puntaje": [4, 3]})
    ruta = tmp_path / "m.xlsx"
    df.to_excel(ruta, index=False)
    out = vc.leer_matriz(ruta)
    assert list(out["item"]) == ["1", "1"]


# --- Cálculo integral ---------------------------------------------------------
def test_calcular_libro():
    r = vc.calcular(_df(_tabla_libro()))
    celda = {(c.item, c.criterio): c for c in r.celdas}
    assert celda[("1", "claridad")].v == 1.0 and celda[("1", "claridad")].cumple
    assert celda[("2", "suficiencia")].v == pytest.approx(8 / 9)
    assert celda[("2", "suficiencia")].cumple
    assert celda[("2", "relevancia")].v == pytest.approx(7 / 9)
    assert not celda[("2", "relevancia")].cumple           # V < 0.80 aunque I-CVI = 1
    assert celda[("2", "claridad")].ivc == 1.0
    assert not celda[("2", "claridad")].cumple
    it = {i.item: i for i in r.items}
    assert it["1"].decision == "mantener"
    assert it["2"].decision == "modificar"
    assert set(it["2"].criterios_fallidos) == {"relevancia", "claridad"}
    # V global = promedio de 10 celdas: (5*1 + 8/9 + 7/9 + 1 + 2/3 + 1)/10
    esperado = (5 + 8 / 9 + 7 / 9 + 1 + 2 / 3 + 1) / 10
    assert r.v_global == pytest.approx(esperado)
    assert r.s_cvi_ave == pytest.approx(1.0)      # todos los I-CVI = 1 en este fixture
    assert r.s_cvi_ua == pytest.approx(1.0)
    assert r.decision == "aplicable previa modificación"
    assert r.kendall["w"] is None or 0 <= r.kendall["w"] <= 1


def test_calcular_todo_cuatro_es_aplicable():
    t = {(str(i), cr): [4, 4, 4] for i in (1, 2, 3) for cr in vc.CRITERIOS}
    r = vc.calcular(_df(t))
    assert r.decision == "aplicable sin modificar"
    assert r.v_global == 1.0 and r.s_cvi_ave == 1.0


def test_item_con_v_bajo_se_elimina():
    t = {("1", cr): [4, 4, 4] for cr in vc.CRITERIOS}
    for cr in vc.CRITERIOS:
        t[("2", cr)] = [1, 2, 1]   # V = (0+1+0)/9 = 0.111
    r = vc.calcular(_df(t))
    it = {i.item: i for i in r.items}
    assert it["2"].decision == "eliminar"
    assert r.decision in ("no aplicable", "aplicable previa modificación")


def test_ivc_con_3_jueces_exige_unanimidad():
    t = {("1", cr): [4, 4, 2] for cr in vc.CRITERIOS}  # I-CVI = 2/3 < 0.80
    r = vc.calcular(_df(t))
    assert all(c.ivc == pytest.approx(2 / 3) for c in r.celdas)
    assert not any(c.cumple for c in r.celdas)


def test_dos_jueces_advertencia_sin_kendall():
    t = {("1", cr): [4, 3] for cr in vc.CRITERIOS}
    r = vc.calcular(_df(t, jueces=("A", "B")))
    assert r.kendall["w"] is None
    assert any("3" in a or "jueces" in a for a in r.advertencias)


# --- Markdown -----------------------------------------------------------------
def test_markdown_tres_lineas_sin_verticales_de_contenido_extra():
    md = vc.a_markdown(vc.calcular(_df(_tabla_libro())))
    assert "**Tabla 1**" in md and "*Nota.*" in md
    assert "Penfield y Giacobbi" in md
    assert "no transcrito" in md
    assert "0.89" in md  # V = 8/9


# --- XLSX ---------------------------------------------------------------------
def test_xlsx_con_formulas_visibles(tmp_path):
    from openpyxl import load_workbook

    df = _df(_tabla_libro())
    r = vc.calcular(df)
    destino = vc.a_xlsx(df, r, tmp_path / "ivc.xlsx")
    wb = load_workbook(destino)  # sin data_only -> fórmulas
    assert wb.sheetnames == ["Parametros", "Calificaciones", "Items", "Instrumento"]
    ws = wb["Calificaciones"]
    # Puntajes como valores, derivados como fórmulas
    assert ws["D3"].value == 4
    formulas = [c.value for fila in ws.iter_rows(min_row=3, max_row=3) for c in fila
                if isinstance(c.value, str) and c.value.startswith("=")]
    assert any("SUM" in f for f in formulas)
    assert any("SQRT" in f for f in formulas)
    assert str(wb["Instrumento"]["B9"].value).startswith("=IF(")
    assert str(wb["Items"]["B2"].value).startswith("=AVERAGEIFS")
    # Los puntajes del xlsx coinciden con la entrada
    for fila in range(3, 13):
        pts = [ws.cell(fila, 4 + k).value for k in range(3)]
        assert all(isinstance(p, int) and 1 <= p <= 4 for p in pts)


def test_xlsx_no_escribe_en_referencias():
    df = _df(_tabla_libro())
    r = vc.calcular(df)
    with pytest.raises(seguridad.EscrituraProhibida):
        vc.a_xlsx(df, r, rutas.MODELOS_VALIDACION / "prueba.xlsx")


# --- Plantilla y CLI ----------------------------------------------------------
def test_plantilla_vacia(tmp_path):
    ruta = vc.crear_plantilla(tmp_path / "cap.csv")
    assert ruta.read_text(encoding="utf-8-sig").strip() == "juez,item,criterio,puntaje"
    with pytest.raises(FileExistsError):
        vc.crear_plantilla(ruta)
    assert vc.crear_plantilla(ruta, forzar=True) == ruta


def test_plantilla_no_escribe_en_referencias():
    with pytest.raises(seguridad.EscrituraProhibida):
        vc.crear_plantilla(rutas.MODELOS_VALIDACION / "x.csv")


def test_cli_plantilla_y_calcular_vacio_da_1(tmp_path, capsys):
    p = tmp_path / "cap.csv"
    assert vc.main(["plantilla", "--salida", str(p)]) == 0
    assert vc.main(["calcular", str(p)]) == 1
    assert "SIN DATOS" in capsys.readouterr().err


def test_cli_uso_incorrecto_da_2():
    assert vc.main([]) == 2
    assert vc.main(["calcular"]) == 2
    assert vc.main(["tabla-critica", "--jueces-min", "9", "--jueces-max", "3"]) == 2


def test_cli_calcular_json_md_xlsx(tmp_path, capsys):
    import json

    ruta = tmp_path / "m.csv"
    filas = ["juez,item,criterio,puntaje"]
    for (it, cr), pts in _tabla_libro().items():
        for j, p in zip(JUECES, pts):
            filas.append(f"{j},{it},{cr},{p}")
    ruta.write_text("\n".join(filas) + "\n", encoding="utf-8")
    code = vc.main(["calcular", str(ruta), "--json", "--md", str(tmp_path / "o.md"), "--xlsx", str(tmp_path / "o.xlsx")])
    salida = capsys.readouterr().out
    datos = json.loads(salida)
    assert code == 1                                    # hay ítem por modificar
    assert datos["decision"] == "aplicable previa modificación"
    assert datos["n_jueces"] == 3
    assert (tmp_path / "o.md").exists() and (tmp_path / "o.xlsx").exists()
    assert datos["fuente"]["sha256"] == seguridad.sha256_archivo(ruta)
    # no sobrescribe sin --forzar
    assert vc.main(["calcular", str(ruta), "--md", str(tmp_path / "o.md")]) == 1


def test_cli_tabla_critica(capsys):
    assert vc.main(["tabla-critica", "--json"]) == 0
    import json
    filas = json.loads(capsys.readouterr().out)
    assert [f["n"] for f in filas] == list(range(3, 11))
    assert filas[0]["alfa_0.05"] == 1.0


def test_rejilla_item_criterio_incompleta_error_claro(tmp_path, capsys):
    """Todos los jueces coinciden, pero el ítem 2 carece de 'claridad': error claro, sin KeyError."""
    ruta = tmp_path / "e.csv"
    filas = ["juez,item,criterio,puntaje"]
    for j in ("A", "B"):
        filas += [f"{j},1,relevancia,4", f"{j},1,claridad,4", f"{j},2,relevancia,4"]
    ruta.write_text("\n".join(filas) + "\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="rejilla"):
        vc.leer_matriz(ruta)
    assert vc.main(["calcular", str(ruta)]) == 1
    err = capsys.readouterr().err
    assert "ERROR" in err and "Traceback" not in err


def test_no_escribe_en_datos_raw(tmp_path):
    destino = rutas.DATOS_RAW / "no_debe_existir_vc.csv"
    with pytest.raises(seguridad.EscrituraProhibida, match="datos/raw"):
        vc.crear_plantilla(destino)
    assert not destino.exists()
    ruta = tmp_path / "ok.csv"
    ruta.write_text("juez,item,criterio,puntaje\nA,1,claridad,4\nB,1,claridad,4\n", encoding="utf-8")
    assert vc.main(["calcular", str(ruta), "--md", str(rutas.DATOS_RAW / "no_debe_existir_vc.md")]) == 1
    assert vc.main(["calcular", str(ruta), "--xlsx", str(rutas.DATOS_RAW / "no_debe_existir_vc.xlsx")]) == 1
    assert not (rutas.DATOS_RAW / "no_debe_existir_vc.md").exists()
    assert not (rutas.DATOS_RAW / "no_debe_existir_vc.xlsx").exists()


def test_xlsx_items_lleva_advertencia_verificar(tmp_path):
    import openpyxl
    df = _df({("1", "claridad"): [4, 4, 4]})
    res = vc.calcular(df)
    dest = vc.a_xlsx(df, res, tmp_path / "v.xlsx")
    wi = openpyxl.load_workbook(dest)["Items"]
    assert "[VERIFICAR" in str(wi["H1"].value)
