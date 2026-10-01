# -*- coding: utf-8 -*-
"""Pruebas de curador_cerebro sobre un vault de PRUEBA en tmp_path (fixtures, no son datos de la tesis)."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from scripts.agentes import curador_cerebro as cc  # noqa: E402

FM_OK = "---\ntipo: nota\nfase: F1\nagente: redactor-academico\nestado: borrador\nfecha_actualizacion: 2026-01-02\n---\n"


def escribir(base: Path, rel: str, texto: str) -> Path:
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8", newline="\n")
    return p


@pytest.fixture
def vault(tmp_path) -> Path:
    v = tmp_path / "vault"
    for c in cc.CARPETAS_CANONICAS:
        (v / c).mkdir(parents=True)
    escribir(v, "HOME.md", "# Home\n[[MOC-01]] [[03_CONCEPTOS_ATOMICOS/Concepto-A|alias]]\n")
    escribir(v, "01_MOCS/MOC-01.md", FM_OK + "# MOC\n[[Concepto-A]] [[Nota Fantasma]] y `[[en-codigo]]`\n")
    escribir(v, "03_CONCEPTOS_ATOMICOS/Concepto-A.md", "# A\nVer [[MOC-01#sec|el moc]] y [[Alias Útil]].\n")
    escribir(v, "03_CONCEPTOS_ATOMICOS/Concepto_Á.md", "# dup normalizado\n")
    escribir(v, "03_CONCEPTOS_ATOMICOS/Concepto-A2.md", "---\naliases: [Alias Útil]\n---\n# A2\n")
    escribir(v, "03_CONCEPTOS_ATOMICOS/Huerfana.md", "# Nadie me enlaza\n")
    escribir(v, "08_SISTEMA_Y_AGENTES/bitacoras/x.md", "---\ntipo: bitacora\nagente: x\n---\n# x\n")   # incompleta
    escribir(v, "08_SISTEMA_Y_AGENTES/handoffs/mal.md", "---\ntipo: [sin cerrar\n---\ncuerpo\n")        # YAML inválido
    escribir(v, "08_SISTEMA_Y_AGENTES/handoffs/sin.md", "# sin frontmatter\n")
    escribir(v, "99_INBOX/suelta.md", "# suelta\n")
    escribir(v, "00_SISTEMA/vacia.md", "")
    escribir(v, "02_PROYECTOS/Validada.md", FM_OK.replace("borrador", "validado") + "# v\n")
    (v / ".obsidian").mkdir()
    escribir(v, ".obsidian/oculta.md", "# ignorada [[roto-oculto]]\n")
    return v


# ---------------------------------------------------------------- funciones puras
def test_separar_y_parsear_frontmatter():
    d, e, c = cc.parsear_frontmatter(FM_OK + "cuerpo")
    assert e is None and d["agente"] == "redactor-academico" and c == "cuerpo"
    assert cc.parsear_frontmatter("sin fm")[:2] == (None, None)
    assert "sin cierre" in cc.parsear_frontmatter("---\ntipo: x\n")[1]
    assert "YAML" in cc.parsear_frontmatter("---\na: [b\n---\n")[1]


def test_wikilinks_ignora_codigo_y_normaliza():
    enl = cc.extraer_wikilinks("[[A#h|x]] ![[img.png]] `[[no]]` ```\n[[tampoco]]\n``` <!-- [[nada]] --> [[#interno]]")
    assert [e["destino"] for e in enl] == ["A", "img.png", ""]
    assert enl[1]["embed"] is True
    assert cc.extraer_wikilinks(r"| [[Ruta/Nota\|alias]] |")[0]["destino"] == "Ruta/Nota"


def test_normalizar_y_estado():
    assert cc.normalizar_nombre("Concepto_Á") == cc.normalizar_nombre("concepto-a")
    assert cc.clasificar_estado("Validado") == "validado"
    assert cc.clasificar_estado("borrador") == "borrador"
    assert cc.clasificar_estado(None) == "sin_estado"
    assert cc.clasificar_estado("xyz") == "otro"


# ---------------------------------------------------------------- auditoría
def test_auditar_detecta_hallazgos(vault):
    inf = cc.auditar_vault(cc.Vault(vault))
    assert inf["totales"]["notas"] == 12                           # .obsidian excluido
    rotos = {e["destino"] for e in inf["enlaces_rotos"]}
    assert rotos == {"Nota Fantasma"}                              # código y .obsidian no cuentan
    assert "03_CONCEPTOS_ATOMICOS/Huerfana.md" in inf["huerfanas"]
    assert "03_CONCEPTOS_ATOMICOS/Concepto-A2.md" not in inf["huerfanas"]   # enlazada por alias
    assert "HOME.md" not in inf["huerfanas"]
    assert any(len(d["notas"]) == 2 for d in inf["duplicados"])
    assert inf["vacias"] == ["00_SISTEMA/vacia.md"]
    assert inf["frontmatter"]["invalidos"][0]["nota"].endswith("mal.md")
    inc = {x["nota"]: x["faltan"] for x in inf["frontmatter"]["incompletos"]}
    assert set(inc["08_SISTEMA_Y_AGENTES/bitacoras/x.md"]) == {"fase", "estado", "fecha_actualizacion"}
    assert "08_SISTEMA_Y_AGENTES/handoffs/sin.md" in inf["frontmatter"]["sin_frontmatter_agente"]
    assert inf["inbox"]["sin_clasificar"] == ["99_INBOX/suelta.md"]
    assert inf["estados"]["validado"] == 1 and inf["estados"]["borrador"] >= 1
    assert inf["por_carpeta"]["01_MOCS"] == 1 and inf["por_carpeta"]["99_INBOX"] == 1
    assert inf["errores"] > 0
    assert "RESUMEN" in cc.formatear_auditoria(inf)


def test_resolucion_por_ruta_nombre_y_alias(vault):
    v = cc.Vault(vault)
    assert v.resolver("Concepto-A") == ["03_CONCEPTOS_ATOMICOS/Concepto-A.md"]
    assert v.resolver("03_CONCEPTOS_ATOMICOS/Concepto-A") == ["03_CONCEPTOS_ATOMICOS/Concepto-A.md"]
    assert v.resolver("concepto-a.md") == ["03_CONCEPTOS_ATOMICOS/Concepto-A.md"]
    assert v.resolver("Alias Útil") == ["03_CONCEPTOS_ATOMICOS/Concepto-A2.md"]
    assert v.resolver("no-existe") == []


def test_enlaces_y_backlinks(vault):
    v = cc.Vault(vault)
    d = cc.datos_enlaces(v, "03_CONCEPTOS_ATOMICOS/Concepto-A.md")
    assert sorted(d["entrantes"]) == ["01_MOCS/MOC-01.md", "HOME.md"]
    assert any(s["destino"] == "MOC-01" for s in d["salientes"])
    assert cc.main(["enlaces", "Concepto-A", "--vault", str(vault), "--json"]) == 0
    assert cc.main(["enlaces", "inexistente", "--vault", str(vault)]) == 1
    assert cc.main(["backlinks", "--vault", str(vault)]) == 0


def test_canvas_cuenta_como_entrante(vault):
    (vault / "09_CANVAS_Y_DIAGRAMAS" / "m.canvas").write_text(
        json.dumps({"nodes": [{"type": "file", "file": "03_CONCEPTOS_ATOMICOS/Huerfana.md"}]}), encoding="utf-8")
    assert "03_CONCEPTOS_ATOMICOS/Huerfana.md" not in cc.auditar_vault(cc.Vault(vault))["huerfanas"]


def test_auditar_no_modifica_el_vault(vault):
    antes = {p: p.read_bytes() for p in vault.rglob("*") if p.is_file()}
    cc.main(["auditar", "--vault", str(vault)])
    assert {p: p.read_bytes() for p in vault.rglob("*") if p.is_file()} == antes


# ---------------------------------------------------------------- escritura
def test_crear_nota_valida_y_no_sobrescribe(vault, capsys):
    args = ["crear-nota", "--vault", str(vault), "--ruta", "99_INBOX/nueva.md", "--tipo", "nota",
            "--fase", "F1", "--agente", "curador-cerebro", "--estado", "borrador", "--titulo", "Título: con dos puntos"]
    assert cc.main(args) == 0
    p = vault / "99_INBOX/nueva.md"
    d, e, _ = cc.parsear_frontmatter(p.read_text(encoding="utf-8"))
    assert e is None and all(d.get(k) for k in cc.CLAVES_OBLIGATORIAS)
    contenido = p.read_bytes()
    assert cc.main(args) == 1                                      # existe -> falla
    assert p.read_bytes() == contenido


@pytest.mark.parametrize("ruta", ["../fuera.md", "/abs.md", "C:/x.md", ".obsidian/x.md", "sin_ext.txt"])
def test_crear_nota_rechaza_rutas_peligrosas(vault, ruta):
    with pytest.raises(cc.ErrorCurador):
        cc.crear_nota(vault, ruta, "nota", "F1", "curador-cerebro", "borrador", "T")


def test_bitacora_append_only(vault):
    cc.registrar_bitacora(vault, "agente-x", "primera")
    p = vault / "08_SISTEMA_Y_AGENTES/bitacoras/agente-x.md"
    t1 = p.read_text(encoding="utf-8")
    cc.registrar_bitacora(vault, "agente-x", "segunda")
    t2 = p.read_text(encoding="utf-8")
    assert t2.startswith(t1) and "segunda" in t2 and t2.count("# BITÁCORA") == 1
    with pytest.raises(cc.ErrorCurador):
        cc.registrar_bitacora(vault, "../malo", "x")
    with pytest.raises(cc.ErrorCurador):
        cc.registrar_bitacora(vault, "agente-x", "  ")


def handoff_base(**kw):
    r = {"fecha": "2026-09-30", "agente": "curador-cerebro", "fase": "F1", "estado": "completado",
         "productos_generados": ["a.md"], "hallazgos_clave": ["h"], "pendientes_o_verificar": [],
         "siguiente_accion_sugerida": "seguir"}
    r.update(kw)
    return r


def test_handoff_valido_y_archivo(vault):
    p = cc.registrar_handoff(vault, handoff_base(), "Auditoría inicial")
    assert p.name == "2026-09-30_curador-cerebro_auditoria-inicial.md"
    d, e, _ = cc.parsear_frontmatter(p.read_text(encoding="utf-8"))
    assert e is None and d["tipo"] == "handoff"
    with pytest.raises(cc.ErrorCurador):                          # no sobrescribe
        cc.registrar_handoff(vault, handoff_base(), "Auditoría inicial")


def test_handoff_rechaza_esquema_y_longitud(vault):
    assert cc.validar_handoff(handoff_base(estado="hecho"))
    assert cc.validar_handoff(handoff_base(fecha="2026-13-40"))
    r = handoff_base(); del r["fase"]
    assert any("fase" in e for e in cc.validar_handoff(r))
    assert cc.validar_handoff(handoff_base(extra="no permitido"))
    largo = handoff_base(hallazgos_clave=["palabra " * 301])
    assert any("palabras" in e for e in cc.validar_handoff(largo))
    with pytest.raises(cc.ErrorCurador):
        cc.registrar_handoff(vault, largo, "largo")
    assert cc.validar_handoff(handoff_base(hallazgos_clave=["palabra " * 100])) == []


def test_marcar_estado_edita_solo_lineas_y_registra(vault):
    rel = "01_MOCS/MOC-01.md"
    antes = (vault / rel).read_text(encoding="utf-8")
    r = cc.marcar_estado(vault, "MOC-01", "validado", fecha="2026-05-05")
    assert r["estado_previo"] == "borrador"
    despues = (vault / rel).read_text(encoding="utf-8")
    difer = [(a, b) for a, b in zip(antes.splitlines(), despues.splitlines()) if a != b]
    assert sorted(b for _, b in difer) == ["estado: validado", "fecha_actualizacion: 2026-05-05"]
    assert antes.split("---\n", 2)[2] == despues.split("---\n", 2)[2]           # cuerpo intacto
    assert not list(vault.rglob("*.bak"))
    bit = (vault / "08_SISTEMA_Y_AGENTES/bitacoras/curador-cerebro.md").read_text(encoding="utf-8")
    assert "borrador" in bit and "validado" in bit


def test_marcar_estado_inserta_claves_faltantes_y_simula(vault):
    rel = "08_SISTEMA_Y_AGENTES/bitacoras/x.md"
    contenido = (vault / rel).read_bytes()
    cc.marcar_estado(vault, rel, "borrador", simular=True)
    assert (vault / rel).read_bytes() == contenido
    cc.marcar_estado(vault, rel, "borrador", fecha="2026-05-05")
    d, e, _ = cc.parsear_frontmatter((vault / rel).read_text(encoding="utf-8"))
    assert e is None and d["estado"] == "borrador" and str(d["fecha_actualizacion"]) == "2026-05-05"


def test_marcar_estado_rechaza_casos_invalidos(vault):
    with pytest.raises(cc.ErrorCurador):
        cc.marcar_estado(vault, "Huerfana", "validado")            # sin frontmatter
    with pytest.raises(cc.ErrorCurador):
        cc.marcar_estado(vault, "no-existe", "validado")
    with pytest.raises(cc.ErrorCurador):
        cc.marcar_estado(vault, "MOC-01", "Estado Malo!")


def test_no_hay_operaciones_destructivas_en_el_codigo():
    """El propio módulo no puede borrar, mover ni renombrar."""
    codigo = Path(cc.__file__).read_text(encoding="utf-8")
    codigo = re.sub(r'""".*?"""', "", codigo, flags=re.S)           # ignora docstrings
    prohibidos = ["os.remove", "os.unlink", ".unlink(", "rmtree", "shutil.move", "os.rename", ".rename(",
                  "os.replace", ".replace_path", "os.rmdir", ".rmdir(", "send2trash", "shutil.copy", "os.removedirs"]
    hallados = [p for p in prohibidos if p in codigo]
    assert not hallados, hallados
    assert not re.search(r"Path\([^)]*\)\.replace\(|\bp\.replace\(", codigo)


def test_cli_subproceso_con_variable_de_entorno(vault):
    py = RAIZ / ".venv" / "Scripts" / "python.exe"
    exe = str(py) if py.exists() else sys.executable
    env = {**os.environ, "SIVAC_VAULT": str(vault), "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([exe, str(RAIZ / "scripts/agentes/curador_cerebro.py"), "auditar", "--json"],
                       capture_output=True, text=True, encoding="utf-8", env=env)
    assert r.returncode == 1                                       # hay errores (fixture los contiene)
    assert json.loads(r.stdout)["totales"]["notas"] == 12
    r = subprocess.run([exe, str(RAIZ / "scripts/agentes/curador_cerebro.py"), "no-es-comando"],
                       capture_output=True, text=True, env=env)
    assert r.returncode == 2
