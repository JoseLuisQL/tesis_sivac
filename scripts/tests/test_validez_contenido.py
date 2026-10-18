"""Pruebas de scripts/agentes/validez_contenido.py.

Todos los puntajes de abajo son FIXTURES SINTETICOS de prueba, calculados a mano
en los comentarios; no son calificaciones de jueces reales ni se guardan en
datos/. El modulo no tiene modo de datos simulados: la plantilla que emite solo
contiene cabeceras.

Modelo unico del modulo: certificado dicotomico de Fany 2024 (DEC-015), con tres
criterios (pertinencia, relevancia, claridad) y marca 0 = No, 1 = Si. La escala
ordinal de 1 a 4 con cinco criterios del modelo Condor Tinoco ya no existe en
este modulo: quedo superada por DEC-015 y no se expone como argumento.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.agentes import validez_contenido as vc  # noqa: E402
from scripts.comun import rutas, seguridad  # noqa: E402

JUECES = ("J1", "J2", "J3")


def _df(tabla: dict, jueces=JUECES):
    """tabla[(item, criterio)] = [marca por juez]  ->  DataFrame validado."""
    import pandas as pd

    filas = []
    for (it, cr), pts in tabla.items():
        for j, p in zip(jueces, pts):
            filas.append({"juez": j, "item": it, "criterio": cr, "puntaje": p})
    return vc._validar(pd.DataFrame(filas))


def _tabla_items(*pares):
    """Genera una tabla completa (unanimidad en todos los criterios)."""
    return {(it, cr): list(marcas) for it, marcas in pares for cr in vc.CRITERIOS}


# --- Constantes del modelo vigente (DEC-015) ----------------------------------
def test_constantes_dicotomicas():
    assert vc.CRITERIOS == ("pertinencia", "relevancia", "claridad")
    assert set(vc.ETIQUETAS) == set(vc.CRITERIOS)
    assert vc.C_CATEGORIAS == 2
    assert vc.L_MINIMO == 0
    assert vc.CORTE_APROBACION == 1
    assert vc.UMBRAL_V == 0.80 and vc.UMBRAL_IVC == 0.80


# --- V de Aiken ---------------------------------------------------------------
def test_v_aiken_dicotomico_es_s_entre_n():
    """V = S / (n (c - 1)) con c = 2 y l = 0 se reduce a V = S / n."""
    assert vc.v_aiken([1, 1, 1]) == pytest.approx(1.0)
    assert vc.v_aiken([1, 1, 0]) == pytest.approx(2 / 3)
    assert vc.v_aiken([1, 0, 0]) == pytest.approx(1 / 3)
    assert vc.v_aiken([0, 0, 0]) == pytest.approx(0.0)


def test_v_aiken_forma_general_reduce_a_s_entre_n():
    # La parametrizacion explicita (c = 2, l = 0) debe reproducir la reduccion V = S/n
    # para cualquier combinacion de marcas, no solo para los casos sueltos de arriba.
    for k in range(4):
        marcas = [1] * k + [0] * (3 - k)
        assert vc.v_aiken(marcas, c=2, l=0) == pytest.approx(k / 3)
        assert vc.v_aiken(marcas, c=2, l=0) == vc.v_aiken(marcas)


def test_v_aiken_sin_jueces_falla():
    with pytest.raises(vc.DatosInvalidos):
        vc.v_aiken([])


def test_umbral_080_exige_unanimidad_con_tres_jueces():
    """Con tres jueces y c = 2, solo S = 3 alcanza V >= 0.80."""
    for marcas in ([1, 1, 1], [1, 1, 0], [1, 0, 0], [0, 0, 0]):
        v = vc.v_aiken(marcas)
        assert v == pytest.approx(sum(marcas) / 3)
        assert (v >= vc.UMBRAL_V) is (sum(marcas) == 3)
    assert vc.v_aiken([1, 1, 0]) == pytest.approx(0.6666667, abs=1e-6)
    assert vc.v_aiken([1, 1, 0]) < vc.UMBRAL_V


def test_demostracion_sintetica_tres_jueces():
    """DEMOSTRACION TAREA C (datos sinteticos propios, nunca de campo).

    Un item, tres criterios y tres jueces:
      Pertinencia: Si, Si, Si -> S = 3 -> V = 3/3 = 1.000  (cumple)
      Relevancia:  Si, Si, No -> S = 2 -> V = 2/3 = 0.667  (no cumple)
      Claridad:    Si, No, No -> S = 1 -> V = 1/3 = 0.333  (no cumple)
    El corte 0.80 solo se alcanza en la fila unanime.
    """
    tabla = {
        ("AP-01", "pertinencia"): [1, 1, 1],
        ("AP-01", "relevancia"): [1, 1, 0],
        ("AP-01", "claridad"): [1, 0, 0],
    }
    df = _df(tabla)
    r = vc.calcular(df)
    celda = {c.criterio: c for c in r.celdas}
    esperado = {"pertinencia": (3, 1.0), "relevancia": (2, 2 / 3), "claridad": (1, 1 / 3)}
    for cr, (s, v) in esperado.items():
        assert celda[cr].s == s
        assert celda[cr].v == pytest.approx(v)
        assert celda[cr].v == pytest.approx(celda[cr].s / 3)   # V = S / n
        assert celda[cr].cumple is (s == 3)
    assert celda["relevancia"].ivc == pytest.approx(2 / 3)
    assert celda["claridad"].ivc == pytest.approx(1 / 3)
    assert r.criterios == list(vc.CRITERIOS)


# --- I-CVI y Wilson -----------------------------------------------------------
def test_ivc_item():
    assert vc.ivc_item([1, 1, 1]) == 1.0
    assert vc.ivc_item([1, 1, 0]) == pytest.approx(2 / 3)
    assert vc.ivc_item([0, 0, 0]) == 0.0


def test_ic_wilson_v1_n3_a_mano():
    # c = 2 -> N = n (c - 1) = 3: L = 3/(3+z^2); U = 1.
    z2 = vc.Z_95 ** 2
    lo, hi = vc.ic_wilson_v(1.0, 3)
    assert lo == pytest.approx(3 / (3 + z2), abs=1e-9)
    assert lo == pytest.approx(0.4385, abs=1e-4)
    assert hi == pytest.approx(1.0)


def test_ic_wilson_contiene_v_y_esta_en_0_1():
    for marcas in ([1, 1, 1], [1, 1, 0], [1, 0, 0], [0, 0, 0]):
        v = vc.v_aiken(marcas)
        lo, hi = vc.ic_wilson_v(v, 3)
        assert 0 <= lo <= v <= hi <= 1


# --- Significancia exacta -----------------------------------------------------
def test_p_exacto_dicotomico_n3_a_mano():
    # 2^3 = 8 resultados equiprobables: S=3 -> 1/8; S>=2 -> 4/8; S>=1 -> 7/8; S>=0 -> 1.
    assert vc.p_exacto_v(3, 3) == pytest.approx(1 / 8)
    assert vc.p_exacto_v(2, 3) == pytest.approx(4 / 8)
    assert vc.p_exacto_v(1, 3) == pytest.approx(7 / 8)
    assert vc.p_exacto_v(0, 3) == pytest.approx(1.0)


def test_v_critico_n10_consistente_con_p():
    # Con c = 2 el denominador es n, de modo que s = round(V * n).
    # El V critico es el MENOR S cuya cola unilateral no supera alfa.
    v = vc.v_critico(10, 2, 0.05)
    s = round(v * 10)
    assert vc.p_exacto_v(s, 10) <= 0.05
    assert vc.p_exacto_v(s - 1, 10) > 0.05


def test_v_critico_dicotomico_n3_y_n4_inalcanzable():
    """Con c = 2 la unanimidad ocurre con p = 1/8 (n=3) y 1/16 (n=4): nada es significativo al 5 %."""
    assert vc.v_critico(3, 2, 0.05) is None
    assert vc.v_critico(3, 2, 0.01) is None
    assert vc.v_critico(4, 2, 0.05) is None
    assert vc.v_critico(5, 2, 0.05) == 1.0    # p = 1/32 = 0.031 <= 0.05 solo con unanimidad


def test_v_critico_dicotomico_es_el_menor_s_que_no_supera_alfa():
    """Para cada n entre 3 y 10, el V critico es el menor s con p(S >= s) <= alfa; si ni la
    unanimidad alcanza, no existe region de rechazo y el valor es None."""
    for n in range(3, 11):
        v = vc.v_critico(n, 2, 0.05)
        if v is None:
            assert vc.p_exacto_v(n, n) > 0.05          # ni el suceso mas extremo alcanza
            continue
        s = round(v * n)
        assert vc.p_exacto_v(s, n) <= 0.05             # s pertenece a la region de rechazo
        if s > 0:
            assert vc.p_exacto_v(s - 1, n) > 0.05      # y es el menor que lo hace


def test_tabla_v_critico_dicotomica():
    filas = vc.tabla_v_critico(2, 3, 10)
    assert [f["n"] for f in filas] == list(range(3, 11))
    assert filas[0]["alfa_0.05"] is None      # n = 3
    assert filas[1]["alfa_0.05"] is None      # n = 4
    assert filas[2]["alfa_0.05"] == 1.0       # n = 5


def test_distribucion_nula_suma_uno():
    from fractions import Fraction
    for n in (3, 5, 8):
        assert sum(vc._distribucion_nula(n, 2)) == Fraction(1)


# --- Kendall ------------------------------------------------------------------
def test_kendall_a_mano():
    # Rangos: J1 [1,2,3], J2 [1,3,2], J3 [2,1,3] -> sumas 4, 6, 8; S = 8
    # W = 12*8 / (9*(27-3)) = 96/216 = 0.4444
    r = vc.kendall_w([[1, 2, 3], [1, 3, 2], [2, 1, 3]])
    assert r["w"] == pytest.approx(96 / 216)
    assert r["chi2"] == pytest.approx(3 * 2 * 96 / 216)
    assert r["gl"] == 2
    assert 0 < r["p"] < 1


def test_kendall_acuerdo_perfecto():
    assert vc.kendall_w([[1, 2, 3, 4]] * 3)["w"] == pytest.approx(1.0)


def test_kendall_sin_variacion_es_indefinido():
    # Tres jueces que puntuan exactamente igual todos los items: el denominador con
    # correccion por empates se anula (9*24 - 3*72 = 0) y W no es calculable.
    r = vc.kendall_w([[1, 1, 1]] * 3)
    assert r["w"] is None and "indefinido" in r["motivo"]


def test_kendall_con_menos_de_3_jueces():
    r = vc.kendall_w([[1, 2, 3], [1, 2, 3]])
    assert r["w"] is None and "3 jueces" in r["motivo"]


def test_kendall_con_un_solo_item():
    r = vc.kendall_w([[1], [0], [1]])
    assert r["w"] is None and "2 items" in r["motivo"]


# --- Lectura y validacion ------------------------------------------------------
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
    ruta.write_text("juez,item,puntaje\nA,1,1\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="Faltan columnas"):
        vc.leer_matriz(ruta)


def test_rechaza_puntaje_fuera_de_0_1(tmp_path):
    ruta = tmp_path / "x.csv"
    ruta.write_text("juez,item,criterio,puntaje\nA,1,pertinencia,4\nB,1,pertinencia,1\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="0-1"):
        vc.leer_matriz(ruta)


@pytest.mark.parametrize("malo", ["2", "5", "-1", "2.5", "abc"])
def test_puntaje_invalido(tmp_path, malo):
    ruta = tmp_path / "x.csv"
    ruta.write_text(f"juez,item,criterio,puntaje\nA,1,claridad,{malo}\nB,1,claridad,1\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="puntaje"):
        vc.leer_matriz(ruta)


@pytest.mark.parametrize("malo", ["", "nan", "NaN", "inf", "-inf", "Infinity"])
def test_puntaje_vacio_nan_inf_da_datos_invalidos_con_fila(tmp_path, malo):
    ruta = tmp_path / "x.csv"
    ruta.write_text(f"juez,item,criterio,puntaje\nA,1,relevancia,1\nB,1,relevancia,{malo}\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="fila 3"):
        vc.leer_matriz(ruta)


def test_puntaje_vacio_en_xlsx(tmp_path):
    import pandas as pd

    df = pd.DataFrame({"juez": ["A", "B"], "item": [1, 1], "criterio": ["claridad"] * 2, "puntaje": [1, None]})
    ruta = tmp_path / "m.xlsx"
    df.to_excel(ruta, index=False)
    with pytest.raises(vc.DatosInvalidos, match="fila 3"):
        vc.leer_matriz(ruta)


def test_csv_de_cero_bytes(tmp_path):
    ruta = tmp_path / "cero.csv"
    ruta.write_bytes(b"")
    with pytest.raises(vc.DatosInvalidos, match="vac"):
        vc.leer_matriz(ruta)


def test_xlsx_corrupto(tmp_path):
    ruta = tmp_path / "mala.xlsx"
    ruta.write_bytes(b"garbage")
    with pytest.raises(vc.DatosInvalidos, match="corrupto"):
        vc.leer_matriz(ruta)


def test_hoja_inexistente(tmp_path):
    import pandas as pd

    df = pd.DataFrame({"juez": ["A", "B"], "item": [1, 1], "criterio": ["claridad"] * 2, "puntaje": [1, 0]})
    ruta = tmp_path / "m.xlsx"
    df.to_excel(ruta, index=False)
    with pytest.raises(vc.DatosInvalidos, match="Nope"):
        vc.leer_matriz(ruta, "Nope")


def test_rechaza_criterio_ajeno_al_modelo_fany(tmp_path):
    """El criterio 'suficiencia' pertenece al modelo Condor, superado por DEC-015."""
    ruta = tmp_path / "x.csv"
    ruta.write_text("juez,item,criterio,puntaje\nA,1,suficiencia,1\nB,1,suficiencia,1\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="criterio"):
        vc.leer_matriz(ruta)


def test_matriz_incompleta(tmp_path):
    ruta = tmp_path / "x.csv"
    ruta.write_text("juez,item,criterio,puntaje\nA,1,claridad,1\nA,2,claridad,1\nB,1,claridad,1\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="incompleta"):
        vc.leer_matriz(ruta)


def test_resalta_rejilla_item_criterio_incompleta(tmp_path):
    """Todos los jueces coinciden, pero un item carece de un criterio del otro item."""
    ruta = tmp_path / "e.csv"
    filas = ["juez,item,criterio,puntaje"]
    for j in ("A", "B"):
        filas += [f"{j},1,relevancia,1", f"{j},1,claridad,1", f"{j},2,relevancia,1"]
    ruta.write_text("\n".join(filas) + "\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="rejilla"):
        vc.leer_matriz(ruta)


def test_un_solo_juez(tmp_path):
    ruta = tmp_path / "x.csv"
    ruta.write_text("juez,item,criterio,puntaje\nA,1,claridad,1\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="al menos 2 jueces"):
        vc.leer_matriz(ruta)


def test_duplicados(tmp_path):
    ruta = tmp_path / "x.csv"
    ruta.write_text("juez,item,criterio,puntaje\nA,1,claridad,1\nA,1,claridad,0\nB,1,claridad,1\n", encoding="utf-8")
    with pytest.raises(vc.DatosInvalidos, match="duplicadas"):
        vc.leer_matriz(ruta)


def test_criterio_con_tilde_y_mayusculas_se_normaliza(tmp_path):
    ruta = tmp_path / "x.csv"
    ruta.write_text("juez,item,criterio,puntaje\nA,1,Claridad ,1\nB,1,CLARIDAD,0\n", encoding="utf-8")
    df = vc.leer_matriz(ruta)
    assert set(df["criterio"]) == {"claridad"}


def test_lee_xlsx(tmp_path):
    import pandas as pd

    df = pd.DataFrame({"juez": ["A", "B"], "item": [1, 1], "criterio": ["claridad"] * 2, "puntaje": [1, 0]})
    ruta = tmp_path / "m.xlsx"
    df.to_excel(ruta, index=False)
    out = vc.leer_matriz(ruta)
    assert list(out["item"]) == ["1", "1"]


# --- Calculo integral ---------------------------------------------------------
def test_calcular_tres_jueces_dos_items():
    t = {}
    for cr in vc.CRITERIOS:
        t[("AP-01", cr)] = [1, 1, 1]      # unanimidad: V = 1.00, I-CVI = 1
        t[("UP-01", cr)] = [1, 1, 0]      # dos marcas: V = 0.67, I-CVI = 0.67
    r = vc.calcular(_df(t))
    celda = {(c.item, c.criterio): c for c in r.celdas}
    assert r.criterios == list(vc.CRITERIOS)
    assert r.n_jueces == 3 and r.n_items == 2
    assert celda[("AP-01", "pertinencia")].v == 1.0
    assert celda[("AP-01", "pertinencia")].cumple
    assert celda[("UP-01", "pertinencia")].v == pytest.approx(2 / 3)
    assert celda[("UP-01", "pertinencia")].s == 2
    assert not celda[("UP-01", "pertinencia")].cumple
    it = {i.item: i for i in r.items}
    assert it["AP-01"].decision == "mantener"
    assert it["UP-01"].decision == "modificar"
    assert set(it["UP-01"].criterios_fallidos) == set(vc.CRITERIOS)
    assert r.v_global == pytest.approx((3 * 1 + 3 * (2 / 3)) / 6)
    assert r.s_cvi_ave == pytest.approx((1 + 2 / 3) / 2)
    assert r.s_cvi_ua == pytest.approx(0.5)
    assert r.decision == "aplicable previa modificacion"


def test_calcular_unanimidad_total_es_aplicable():
    t = _tabla_items(("AP-01", [1, 1, 1]), ("UP-04", [1, 1, 1]))
    r = vc.calcular(_df(t))
    assert r.decision == "aplicable sin modificar"
    assert r.v_global == 1.0 and r.s_cvi_ave == 1.0 and r.s_cvi_ua == 1.0


def test_item_con_v_bajo_se_elimina():
    t = _tabla_items(("AP-01", [1, 1, 1]), ("AP-02", [0, 0, 0]))
    r = vc.calcular(_df(t))
    it = {i.item: i for i in r.items}
    assert it["AP-02"].v == 0.0
    assert it["AP-02"].decision == "eliminar"
    assert r.decision in ("no aplicable", "aplicable previa modificacion")


def test_criterio_no_unanime_no_cumple():
    t = _tabla_items(("AP-01", [1, 1, 0]))   # I-CVI = 2/3 < 0.80 en los tres criterios
    r = vc.calcular(_df(t))
    assert all(c.ivc == pytest.approx(2 / 3) for c in r.celdas)
    assert not any(c.cumple for c in r.celdas)


def test_dos_jueces_advertencia_sin_kendall():
    t = _tabla_items(("AP-01", [1, 0]))
    r = vc.calcular(_df(t, jueces=("A", "B")))
    assert r.kendall["w"] is None
    assert any("jueces" in a for a in r.advertencias)


def test_advertencia_aritmetica_fany_presente():
    r = vc.calcular(_df(_tabla_items(("AP-01", [1, 1, 1]))))
    assert any("unanimidad" in a for a in r.advertencias)
    assert any("VERIFICAR" in a for a in r.advertencias)


# --- Markdown -----------------------------------------------------------------
def test_markdown_declara_modelo_fany_y_tres_criterios():
    md = vc.a_markdown(vc.calcular(_df(_tabla_items(("AP-01", [1, 1, 1])))))
    assert "**Tabla 1**" in md and "*Nota.*" in md
    assert "Modelo aplicado: certificado Fany 2024" in md
    assert "Pertinencia, Relevancia y Claridad" in md
    assert "exige unanimidad" in md
    assert "Penfield y Giacobbi" in md
    assert "no se transcribe" in md
    assert md.count("VERIFICAR") >= 3


# --- XLSX ---------------------------------------------------------------------
def test_xlsx_con_formulas_visibles(tmp_path):
    from openpyxl import load_workbook

    t = {}
    for cr in vc.CRITERIOS:
        t[("AP-01", cr)] = [1, 1, 1]
        t[("UP-01", cr)] = [1, 0, 1]
    df = _df(t)
    r = vc.calcular(df)
    destino = vc.a_xlsx(df, r, tmp_path / "ivc.xlsx")
    wb = load_workbook(destino)                 # sin data_only -> formulas
    assert wb.sheetnames == ["Parametros", "Calificaciones", "Items", "Instrumento"]
    ws = wb["Calificaciones"]
    assert ws["D3"].value == 1                  # el puntaje se escribe como valor
    formulas = [c.value for fila in ws.iter_rows(min_row=3, max_row=3) for c in fila
                if isinstance(c.value, str) and c.value.startswith("=")]
    assert any("SUM" in f for f in formulas)
    assert any("SQRT" in f for f in formulas)
    assert str(wb["Instrumento"]["B9"].value).startswith("=IF(")
    assert str(wb["Items"]["B2"].value).startswith("=AVERAGEIFS")
    for fila in range(3, 9):
        pts = [ws.cell(fila, 4 + k).value for k in range(3)]
        assert all(p in (0, 1) for p in pts)


def test_xlsx_escribe_c_dos_y_l_cero(tmp_path):
    from openpyxl import load_workbook

    df = _df(_tabla_items(("AP-01", [1, 1, 1]), ("UP-01", [1, 1, 0])))
    r = vc.calcular(df)
    destino = vc.a_xlsx(df, r, tmp_path / "fany.xlsx")
    ws = load_workbook(destino)["Parametros"]
    assert ws["B3"].value == 2                  # c
    assert ws["B4"].value == 0                  # l
    assert ws["B11"].value == 1                 # corte de aprobacion
    assert ws["B10"].value == 0.8               # umbral I-CVI
    cal = load_workbook(destino)["Calificaciones"]
    assert any(isinstance(c.value, str) and c.value.startswith("=IF(") for c in cal[3])


def test_xlsx_items_lleva_advertencia_verificar(tmp_path):
    import openpyxl

    df = _df({("1", "claridad"): [1, 1, 1]})
    res = vc.calcular(df)
    dest = vc.a_xlsx(df, res, tmp_path / "v.xlsx")
    wi = openpyxl.load_workbook(dest)["Items"]
    assert "[VERIFICAR" in str(wi["H1"].value)


def test_xlsx_no_escribe_en_referencias():
    df = _df(_tabla_items(("AP-01", [1, 1, 1])))
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


def _csv(tmp_path, tabla, nombre="m.csv"):
    filas = ["juez,item,criterio,puntaje"]
    for (it, cr), pts in tabla.items():
        for j, p in zip(JUECES, pts):
            filas.append(f"{j},{it},{cr},{p}")
    ruta = tmp_path / nombre
    ruta.write_text("\n".join(filas) + "\n", encoding="utf-8")
    return ruta


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

    ruta = _csv(tmp_path, _tabla_items(("AP-01", [1, 1, 1]), ("UP-01", [1, 1, 0])))
    code = vc.main(["calcular", str(ruta), "--json",
                    "--md", str(tmp_path / "o.md"), "--xlsx", str(tmp_path / "o.xlsx")])
    datos = json.loads(capsys.readouterr().out)
    assert code == 1                                    # hay item por modificar
    assert datos["decision"] == "aplicable previa modificacion"
    assert datos["n_jueces"] == 3 and datos["n_items"] == 2
    assert datos["criterios"] == list(vc.CRITERIOS)
    assert "modelo" not in datos                        # modelo unico, sin perfil alterno
    assert (tmp_path / "o.md").exists() and (tmp_path / "o.xlsx").exists()
    assert datos["fuente"]["sha256"] == seguridad.sha256_archivo(ruta)
    # no sobrescribe sin --forzar
    assert vc.main(["calcular", str(ruta), "--md", str(tmp_path / "o.md")]) == 1


def test_cli_calcular_unanime_da_0(tmp_path, capsys):
    import json

    ruta = _csv(tmp_path, _tabla_items(("AP-01", [1, 1, 1])))
    assert vc.main(["calcular", str(ruta), "--json"]) == 0
    datos = json.loads(capsys.readouterr().out)
    assert datos["decision"] == "aplicable sin modificar"
    assert datos["celdas"][0]["v"] == pytest.approx(1.0)


def test_cli_datos_hostiles_dan_1_sin_traceback(tmp_path, capsys):
    for nombre, contenido in (("cero.csv", b""), ("mala.xlsx", b"garbage"),
                              ("blank.csv", b"juez,item,criterio,puntaje\nA,1,relevancia,1\nB,1,relevancia,\n")):
        ruta = tmp_path / nombre
        ruta.write_bytes(contenido)
        assert vc.main(["calcular", str(ruta)]) == 1
        assert "ERROR:" in capsys.readouterr().err


def test_cli_tabla_critica_dicotomica(capsys):
    assert vc.main(["tabla-critica", "--json"]) == 0
    import json
    filas = json.loads(capsys.readouterr().out)
    assert [f["n"] for f in filas] == list(range(3, 11))
    assert filas[0]["alfa_0.05"] is None       # n = 3: p(unanimidad) = 0.125 > 0.05
    assert filas[2]["alfa_0.05"] == 1.0        # n = 5


def test_no_escribe_en_datos_raw(tmp_path):
    destino = rutas.DATOS_RAW / "no_debe_existir_vc.csv"
    with pytest.raises(seguridad.EscrituraProhibida, match="datos/raw"):
        vc.crear_plantilla(destino)
    assert not destino.exists()
    ruta = _csv(tmp_path, _tabla_items(("AP-01", [1, 1, 1])), "ok.csv")
    assert vc.main(["calcular", str(ruta), "--md", str(rutas.DATOS_RAW / "no_debe_existir_vc.md")]) == 1
    assert vc.main(["calcular", str(ruta), "--xlsx", str(rutas.DATOS_RAW / "no_debe_existir_vc.xlsx")]) == 1
    assert not (rutas.DATOS_RAW / "no_debe_existir_vc.md").exists()
    assert not (rutas.DATOS_RAW / "no_debe_existir_vc.xlsx").exists()
