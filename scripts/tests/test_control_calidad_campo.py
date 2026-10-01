# -*- coding: utf-8 -*-
"""
Pruebas de scripts/agentes/control_calidad_campo.py.

Todos los CSV se fabrican en tmp_path como FIXTURES DE PRUEBA (valores
arbitrarios, sin significado empirico). Nunca se guardan en datos/.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.agentes import control_calidad_campo as cc  # noqa: E402
from scripts.comun import rutas, seguridad  # noqa: E402

PATRONES_AP = [(3, 4, 2, 5, 3), (2, 3, 4, 3, 5), (4, 4, 3, 2, 5), (1, 3, 2, 4, 3), (5, 3, 4, 2, 4),
               (3, 2, 4, 5, 2), (4, 3, 3, 5, 2)]
PATRONES_UP = [(2, 5, 3, 4, 3), (3, 3, 5, 4, 2), (4, 2, 4, 3, 3), (5, 4, 2, 3, 4), (1, 4, 3, 5, 2),
               (3, 5, 2, 4, 4), (2, 4, 5, 3, 3)]


def categoria(total: int) -> str:
    return "Bajo" if total <= 22 else "Medio" if total <= 36 else "Alto"


def fila_fixture(i: int, fase: str) -> dict:
    ap = PATRONES_AP[(i + (0 if fase == "PRETEST" else 3)) % 7]
    up = PATRONES_UP[(i * 2 + (0 if fase == "PRETEST" else 1)) % 7]
    s_ap, s_up = sum(ap), sum(up)
    f = {
        "sujeto_id": f"TRAB-{i:02d}", "centro_acopio": f"Centro {1 + (i % 4)}", "fase": fase,
        "t_reg": 10.5 + i * 1.7, "t_vale": 3.2 + i * 0.9, "rsd": 50.0 + i * 2.5, "cpe": 40.0 + i * 3.1,
        "score_ap": s_ap, "score_up": s_up, "score_tam_total": s_ap + s_up,
        "nivel_satisfaccion": categoria(s_ap + s_up),
    }
    f.update({f"ap_{k + 1:02d}": v for k, v in enumerate(ap)})
    f.update({f"up_{k + 1:02d}": v for k, v in enumerate(up)})
    return f


def escribir(ruta: Path, filas: list[dict], cabecera=None) -> Path:
    cab = cabecera or list(cc.COLUMNAS)
    with open(ruta, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cab)
        for f in filas:
            w.writerow([f.get(c, "") for c in cab])
    return ruta


@pytest.fixture
def validas():
    return [fila_fixture(i, "PRETEST") for i in range(1, 15)]


@pytest.fixture
def chk(tmp_path):
    return tmp_path / "checksums.txt"


def codigos(inf: dict, clave="errores") -> list[str]:
    return [x["codigo"] for x in inf[clave]]


# --- Caso valido ---------------------------------------------------------

def test_csv_valido_aprobado(tmp_path, validas, chk):
    r = escribir(tmp_path / "bd_sivac_pretest.csv", validas)
    inf = cc.validar_archivo(r, ruta_checksums=chk)
    assert inf["estado"] == "APROBADO", inf["errores"]
    assert inf["fase"] == "PRETEST"
    assert inf["filas_datos"] == 14
    assert codigos(inf, "advertencias") == ["CENTROS_SIN_LISTA"]


def test_cli_codigos_de_salida_y_json(tmp_path, validas, capsys):
    ok = escribir(tmp_path / "bd_sivac_pretest.csv", validas)
    c = str(tmp_path / "c.txt")
    assert cc.main(["validar", str(ok), "--checksums", c]) == 0
    capsys.readouterr()
    assert cc.main(["validar", str(ok), "--json", "--checksums", c]) == 0
    assert json.loads(capsys.readouterr().out)["estado"] == "APROBADO"
    validas[0]["t_reg"] = -5
    mal = escribir(tmp_path / "bd_sivac_postest.csv", validas)
    assert cc.main(["validar", str(mal), "--fase", "pretest", "--checksums", c]) == 1
    assert cc.main(["validar", str(tmp_path / "noexiste.csv")]) == 2
    assert cc.main([]) == 2


# --- Nivel 1 -------------------------------------------------------------

def test_n1_columnas_y_filas(tmp_path, validas, chk):
    cab = [c for c in cc.COLUMNAS if c != "cpe"] + ["extra"]
    r = escribir(tmp_path / "a.csv", validas[:13], cab)
    inf = cc.validar_archivo(r, "pretest", ruta_checksums=chk)
    assert {"COLUMNAS_FALTANTES", "COLUMNAS_SOBRANTES", "N_FILAS", "ID_AUSENTES"} <= set(codigos(inf))
    assert inf["estado"] == "RECHAZADO"


def test_n1_ids_duplicados_invalidos_y_faltantes(tmp_path, validas, chk):
    validas[1]["sujeto_id"] = "TRAB-01"
    validas[2]["sujeto_id"] = "TRAB-15"
    validas[3]["t_reg"] = "NA"
    validas[4]["centro_acopio"] = ""
    validas[5]["ap_03"] = "nan"
    inf = cc.validar_archivo(escribir(tmp_path / "a.csv", validas), "pretest", ruta_checksums=chk)
    cods = codigos(inf)
    assert "ID_DUPLICADO" in cods and "ID_INVALIDO" in cods
    assert cods.count("FALTANTE") == 3
    assert "NO_NUMERICO" not in cods  # el faltante no se duplica como error de rango


def test_n1_centros_oficiales(tmp_path, validas, chk):
    r = escribir(tmp_path / "a.csv", validas)
    oficiales = {f"Centro {k}" for k in (1, 2, 3)}
    inf = cc.validar_archivo(r, "pretest", centros_validos=oficiales, ruta_checksums=chk)
    assert "CENTRO_NO_OFICIAL" in codigos(inf)
    assert "CENTROS_SIN_LISTA" not in codigos(inf, "advertencias")


def test_n1_fila_con_celdas_irregulares(tmp_path, validas, chk):
    r = escribir(tmp_path / "a.csv", validas)
    with open(r, "a", encoding="utf-8") as fh:
        fh.write("TRAB-99,solo,tres\n")
    inf = cc.validar_archivo(r, "pretest", ruta_checksums=chk)
    assert "CELDAS_IRREGULARES" in codigos(inf) and "N_FILAS" in codigos(inf)


def test_n1_bom_es_advertencia(tmp_path, validas, chk):
    r = escribir(tmp_path / "a.csv", validas)
    r.write_bytes(b"\xef\xbb\xbf" + r.read_bytes())
    inf = cc.validar_archivo(r, "pretest", ruta_checksums=chk)
    assert inf["estado"] == "APROBADO" and "BOM_UTF8" in codigos(inf, "advertencias")


# --- Nivel 2 -------------------------------------------------------------

@pytest.mark.parametrize("col,valor,codigo", [
    ("t_reg", 0, "FUERA_DE_RANGO"), ("t_reg", 120.01, "FUERA_DE_RANGO"), ("t_reg", -1, "FUERA_DE_RANGO"),
    ("t_vale", 0, "FUERA_DE_RANGO"), ("t_vale", 61, "FUERA_DE_RANGO"),
    ("rsd", 100.5, "FUERA_DE_RANGO"), ("rsd", -0.1, "FUERA_DE_RANGO"), ("cpe", 101, "FUERA_DE_RANGO"),
    ("ap_01", 6, "FUERA_DE_RANGO"), ("ap_02", 0, "FUERA_DE_RANGO"), ("up_05", 3.5, "NO_ENTERO"),
    ("t_vale", "12,5", "NO_NUMERICO"), ("cpe", "abc", "NO_NUMERICO"), ("fase", "POSTEST", "FASE_INCOHERENTE"),
])
def test_n2_valores_invalidos(tmp_path, validas, chk, col, valor, codigo):
    validas[6][col] = valor
    inf = cc.validar_archivo(escribir(tmp_path / "a.csv", validas), "pretest", ruta_checksums=chk)
    assert codigo in codigos(inf)
    assert inf["estado"] == "RECHAZADO"


@pytest.mark.parametrize("col,valor", [
    ("t_reg", 120), ("t_reg", 0.01), ("t_vale", 60), ("rsd", 0), ("rsd", 100), ("cpe", 0), ("cpe", 100),
])
def test_n2_limites_inclusivos_permitidos(tmp_path, validas, chk, col, valor):
    validas[0][col] = valor
    inf = cc.validar_archivo(escribir(tmp_path / "a.csv", validas), "pretest", ruta_checksums=chk)
    assert "FUERA_DE_RANGO" not in codigos(inf)


def test_n2_fase_desconocida_y_entero_como_decimal(tmp_path, validas, chk):
    validas[0]["fase"] = "LINEA_BASE"
    validas[1]["ap_01"] = "3.0"  # entero escrito como decimal: aceptable
    inf = cc.validar_archivo(escribir(tmp_path / "a.csv", validas), "pretest", ruta_checksums=chk)
    assert "DOMINIO" in codigos(inf)
    assert "NO_ENTERO" not in codigos(inf)
    assert "ENTERO_CON_DECIMALES" in codigos(inf, "advertencias")


# --- Nivel 3 -------------------------------------------------------------

def test_n3_scores_y_baremo(tmp_path, validas, chk):
    validas[0]["score_ap"] += 1
    validas[1]["score_up"] -= 1
    validas[2]["score_tam_total"] += 2
    tam = validas[3]["score_tam_total"]
    validas[3]["nivel_satisfaccion"] = "Alto" if categoria(tam) != "Alto" else "Bajo"
    inf = cc.validar_archivo(escribir(tmp_path / "a.csv", validas), "pretest", ruta_checksums=chk)
    assert {"SCORE_AP", "SCORE_UP", "SCORE_TAM", "BAREMO"} <= set(codigos(inf))


@pytest.mark.parametrize("total,esperada", [(10, "Bajo"), (22, "Bajo"), (23, "Medio"), (36, "Medio"),
                                             (37, "Alto"), (50, "Alto"), (9, None), (51, None)])
def test_baremo_fronteras(total, esperada):
    assert cc.categoria_baremo(total) == esperada


# --- Advertencias sospechosas -------------------------------------------

def test_advertencias_no_bloquean(tmp_path, validas, chk):
    validas[1] = {**validas[0], "sujeto_id": "TRAB-02"}  # fila duplicada salvo id
    for c in cc.ITEMS_AP + cc.ITEMS_UP:  # varianza cero
        validas[2][c] = 3
    validas[2].update(score_ap=15, score_up=15, score_tam_total=30, nivel_satisfaccion="Medio")
    for c in cc.ITEMS_AP:  # bloque AP constante
        validas[3][c] = 4
    validas[3]["score_ap"] = 20
    validas[3]["score_tam_total"] = 20 + validas[3]["score_up"]
    validas[3]["nivel_satisfaccion"] = categoria(validas[3]["score_tam_total"])
    inf = cc.validar_archivo(escribir(tmp_path / "a.csv", validas), "pretest", ruta_checksums=chk)
    assert inf["estado"] == "APROBADO", inf["errores"]
    assert {"FILA_DUPLICADA", "VARIANZA_CERO_LIKERT", "STRAIGHT_LINING"} <= set(codigos(inf, "advertencias"))


def test_identicos_mas_de_70_por_ciento(tmp_path, validas, chk):
    for f in validas[:11]:  # 11/14 = 78.6 %
        f["t_reg"] = 30.0
    for f in validas[:10]:  # 10/14 = 71.4 %
        f["cpe"] = 55.0
    for f in validas[:9]:  # 9/14 = 64.3 %: no debe avisar
        f["t_vale"] = 12.0
    inf = cc.validar_archivo(escribir(tmp_path / "a.csv", validas), "pretest", ruta_checksums=chk)
    cols = {x["columna"] for x in inf["advertencias"] if x["codigo"] == "IDENTICOS_70"}
    assert cols == {"t_reg", "cpe"}
    assert inf["estado"] == "APROBADO"


# --- Nivel 4 -------------------------------------------------------------

def test_n4_registro_solo_con_flag_y_alerta_de_cambio(tmp_path, validas, chk):
    r = escribir(tmp_path / "bd_sivac_pretest.csv", validas)
    inf = cc.validar_archivo(r, ruta_checksums=chk)
    assert inf["trazabilidad"]["estado"] == "no_registrado" and not chk.exists()
    inf = cc.validar_archivo(r, registrar=True, ruta_checksums=chk)
    assert inf["trazabilidad"]["estado"] == "registrado"
    sha = seguridad.sha256_archivo(r)
    assert f"{sha}  {r.resolve().as_posix()}" in chk.read_text(encoding="utf-8")
    inf = cc.validar_archivo(r, registrar=True, ruta_checksums=chk)
    assert inf["trazabilidad"]["estado"] == "coincide_con_registro"
    assert chk.read_text(encoding="utf-8").count(sha) == 1
    r.write_text(r.read_text(encoding="utf-8").replace("TRAB-01", "TRAB-01 ", 1), encoding="utf-8")
    inf = cc.validar_archivo(r, ruta_checksums=chk)
    assert inf["estado"] == "RECHAZADO" and "ALERTA_INTEGRIDAD" in codigos(inf)


def test_n4_no_registra_si_hay_errores(tmp_path, validas, chk):
    validas[0]["t_reg"] = -1
    r = escribir(tmp_path / "a.csv", validas)
    inf = cc.validar_archivo(r, "pretest", registrar=True, ruta_checksums=chk)
    assert inf["trazabilidad"]["estado"] == "no_registrado_por_errores" and not chk.exists()


# --- pares ---------------------------------------------------------------

def test_pares_correctos_e_incorrectos(tmp_path):
    pre = escribir(tmp_path / "pre.csv", [fila_fixture(i, "PRETEST") for i in range(1, 15)])
    post = escribir(tmp_path / "post.csv", [fila_fixture(i, "POSTEST") for i in range(1, 15)])
    inf = cc.comprobar_pares(pre, post)
    assert inf["estado"] == "APROBADO" and inf["sujetos_pareados"] == 14

    filas = [fila_fixture(i, "POSTEST") for i in range(1, 14)]
    filas.append({**fila_fixture(14, "POSTEST"), "sujeto_id": "TRAB-20"})
    filas[0]["centro_acopio"] = "Otro"
    post2 = escribir(tmp_path / "post2.csv", filas)
    inf = cc.comprobar_pares(pre, post2)
    assert {"SIN_POSTEST", "SIN_PRETEST"} <= set(codigos(inf))
    assert "CENTRO_DISTINTO" in codigos(inf, "advertencias")
    assert inf["estado"] == "RECHAZADO"
    assert "ARCHIVOS_IDENTICOS" in codigos(cc.comprobar_pares(pre, pre))
    assert cc.main(["pares", str(pre), str(post)]) == 0
    assert cc.main(["pares", str(pre), str(post2)]) == 1


# --- esquema / plantilla / guardas --------------------------------------

def test_codebook_derivado_de_reglas(tmp_path):
    destino = tmp_path / "codebook.json"
    assert cc.main(["esquema", "--salida", str(destino)]) == 0
    cb = json.loads(destino.read_text(encoding="utf-8"))
    assert [c["nombre"] for c in cb["columnas"]] == list(cc.COLUMNAS)
    por = {c["nombre"]: c for c in cb["columnas"]}
    assert por["t_reg"]["rango"]["notacion"] == "(0, 120]"
    assert por["rsd"]["rango"]["notacion"] == "[0, 100]"
    assert por["ap_03"]["rango"]["notacion"] == "[1, 5]"
    assert por["score_tam_total"]["derivada_de"] == "score_ap + score_up"
    assert cb["identificadores"][0] == "TRAB-01" and len(cb["identificadores"]) == 14
    assert cc.main(["esquema", "--salida", str(destino)]) == 1  # no pisa sin --forzar
    assert cc.main(["esquema", "--salida", str(destino), "--forzar"]) == 0


def test_plantilla_solo_cabecera(tmp_path):
    assert cc.main(["plantilla", "--carpeta", str(tmp_path)]) == 0
    for fase in ("pretest", "postest"):
        lineas = (tmp_path / f"plantilla_bd_sivac_{fase}.csv").read_text(encoding="utf-8").splitlines()
        assert lineas == [",".join(cc.COLUMNAS)]
    assert cc.main(["plantilla", "--carpeta", str(tmp_path)]) == 1


def test_guardas_de_escritura():
    with pytest.raises(seguridad.EscrituraProhibida):
        cc.escribir_json(rutas.DATOS_RAW / "codebook.json", {})
    with pytest.raises(seguridad.EscrituraProhibida):
        cc.escribir_plantilla("pretest", rutas.DATOS_RAW)
    with pytest.raises(seguridad.EscrituraProhibida):
        cc.escribir_json(rutas.MODELOS_TESIS / "x.json", {})
    assert cc.main(["plantilla", "--carpeta", str(rutas.DATOS_RAW)]) == 1
    assert not (rutas.DATOS_RAW / "plantilla_bd_sivac_pretest.csv").exists()


def test_csv_cuarentena_solo_lectura():
    """Valida un CSV real de la cuarentena sin registrar ni escribir nada."""
    q = rutas.DATOS / "_cuarentena_no_empiricos" / "bd_sivac_pretest.csv"
    if not q.exists():
        pytest.skip("No hay CSV de cuarentena")
    antes = seguridad.sha256_archivo(q)
    sombra = q.parent / "nunca_se_escribe.txt"
    inf = cc.validar_archivo(q, ruta_checksums=sombra)
    assert inf["filas_datos"] == 14
    assert seguridad.sha256_archivo(q) == antes
    assert not sombra.exists()


# --- Correcciones de la verificacion independiente -----------------------

def test_csv_cp1252_es_hallazgo_n1_no_traceback(tmp_path, validas, chk, capsys):
    validas[0]["centro_acopio"] = "Centro Ñandú"
    r = escribir(tmp_path / "bd_sivac_pretest.csv", validas)
    r.write_bytes(r.read_text(encoding="utf-8").encode("cp1252"))
    inf = cc.validar_archivo(r, ruta_checksums=chk)
    assert inf["estado"] == "RECHAZADO"
    assert codigos(inf) == ["CODIFICACION_INVALIDA"]
    assert cc.main(["validar", str(r), "--checksums", str(chk)]) == 1
    assert "CODIFICACION_INVALIDA" in capsys.readouterr().out


def test_bytes_arbitrarios_no_lanzan(tmp_path, chk):
    r = tmp_path / "basura.csv"
    r.write_bytes(b"\x96\xff\xfe\x00abc")
    inf = cc.validar_archivo(r, ruta_checksums=chk)
    assert "CODIFICACION_INVALIDA" in codigos(inf)


def test_pares_con_cp1252_reporta_codificacion(tmp_path, validas):
    pre = escribir(tmp_path / "pre.csv", validas)
    validas_post = [fila_fixture(i, "POSTEST") for i in range(1, 15)]
    validas_post[0]["centro_acopio"] = "Ñ"
    post = escribir(tmp_path / "post.csv", validas_post)
    post.write_bytes(post.read_text(encoding="utf-8").encode("cp1252"))
    inf = cc.comprobar_pares(pre, post)
    assert "CODIFICACION_INVALIDA" in codigos(inf)
    assert cc.main(["pares", str(pre), str(post)]) == 1


def test_centros_inexistente_o_ilegible_sale_con_2(tmp_path, validas, capsys):
    ok = escribir(tmp_path / "bd_sivac_pretest.csv", validas)
    c = str(tmp_path / "c.txt")
    assert cc.main(["validar", str(ok), "--centros", str(tmp_path / "noexiste.txt"), "--checksums", c]) == 2
    assert "No existe el archivo de centros" in capsys.readouterr().err
    malo = tmp_path / "centros.txt"
    malo.write_bytes(b"Centro \xd1\n")
    assert cc.main(["validar", str(ok), "--centros", str(malo), "--checksums", c]) == 2
    assert cc.main(["validar", str(ok), "--centros", str(tmp_path), "--checksums", c]) == 2


def test_delimitador_punto_y_coma_mensaje_claro(tmp_path, validas, chk):
    r = escribir(tmp_path / "semi.csv", validas)
    r.write_text(r.read_text(encoding="utf-8").replace(",", ";"), encoding="utf-8")
    inf = cc.validar_archivo(r, "pretest", ruta_checksums=chk)
    assert "DELIMITADOR_INCORRECTO" in codigos(inf)
    assert "COLUMNAS_SOBRANTES" not in codigos(inf)
    assert inf["estado"] == "RECHAZADO"


def test_entero_con_decimales_advierte_y_exponencial_se_rechaza(tmp_path, validas, chk):
    validas[1]["ap_01"] = "3.0"
    inf = cc.validar_archivo(escribir(tmp_path / "a.csv", validas), "pretest", ruta_checksums=chk)
    assert "ENTERO_CON_DECIMALES" in codigos(inf, "advertencias")
    assert cc.a_entero("3.0") == 3 and cc.a_entero("1e0") is None and cc.a_entero("3.5") is None
    validas[2]["up_02"] = "1e0"
    inf2 = cc.validar_archivo(escribir(tmp_path / "b.csv", validas), "pretest", ruta_checksums=chk)
    assert "NO_ENTERO" in codigos(inf2)


def test_checksum_fuera_del_workspace_usa_ruta_completa(tmp_path, validas, chk):
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    r1 = escribir(tmp_path / "a" / "bd_sivac_pretest.csv", validas)
    otras = [fila_fixture(i, "PRETEST") for i in range(1, 15)]
    otras[0]["t_reg"] = 99.0
    r2 = escribir(tmp_path / "b" / "bd_sivac_pretest.csv", otras)
    assert cc.validar_archivo(r1, registrar=True, ruta_checksums=chk)["trazabilidad"]["estado"] == "registrado"
    inf2 = cc.validar_archivo(r2, registrar=True, ruta_checksums=chk)
    assert inf2["trazabilidad"]["estado"] == "registrado"  # no colisiona con r1
    assert "ALERTA_INTEGRIDAD" not in codigos(inf2)
    assert len(cc.leer_checksums(chk)) == 2
