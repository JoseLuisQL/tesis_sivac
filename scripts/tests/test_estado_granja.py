# -*- coding: utf-8 -*-
"""Pruebas de estado_granja sobre una estructura de PRUEBA en tmp_path (fixtures; sin red, sin datos de la tesis)."""

from __future__ import annotations

import json
import subprocess
import sys
import types
from pathlib import Path

import pytest
import requests

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from scripts.agentes import estado_granja as eg  # noqa: E402

AGENTE = "---\nname: {n}\ndescription: d\ntools:\n{t}\nskills:\n{s}\nsquad: Squad X\n---\ncuerpo\n"


def escribir(base: Path, rel: str, texto: str) -> Path:
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8", newline="\n")
    return p


def agente(raiz: Path, nombre: str, tools=("Read",), skills=("sk1",)) -> None:
    t = "\n".join(f"  - {x}" for x in tools)
    s = "\n".join(f"  - {x}" for x in skills)
    escribir(raiz, f".claude/agents/{nombre}.md", AGENTE.format(n=nombre, t=t, s=s))


@pytest.fixture
def ctx(tmp_path) -> eg.Contexto:
    raiz, vault = tmp_path / "ws", tmp_path / "vault"
    (raiz / ".claude/skills/sk1").mkdir(parents=True)
    (raiz / ".claude/skills/sk1/SKILL.md").write_text("x", encoding="utf-8")
    (vault / "00_SISTEMA").mkdir(parents=True)
    return eg.Contexto(raiz=raiz, vault=vault, skills_globales=tmp_path / "glob",
                       pdfs=vault / "pdfs", indices=vault / "idx", sin_word=True)


def estados(res):
    return {r.nombre: r.estado for r in res}


# --- agentes ---------------------------------------------------------------
def test_agentes_validos(ctx):
    agente(ctx.raiz, "director-general", tools=("Read", "Agent"))
    agente(ctx.raiz, "ingeniero-sivac", tools=("Read", "Grep", "Glob"))
    res = eg.seccion_agentes(ctx)
    assert all(r.estado == eg.OK for r in res), [(r.nombre, r.detalle) for r in res]


def test_agente_no_director_con_agent_falla(ctx):
    agente(ctx.raiz, "director-general", tools=("Agent",))
    agente(ctx.raiz, "ingeniero-sivac", tools=("Read", "Grep", "Glob"))
    agente(ctx.raiz, "intruso", tools=("Read", "Agent"))
    assert estados(eg.seccion_agentes(ctx))["'Agent' solo en director-general"] == eg.FALLA


def test_ingeniero_con_write_falla(ctx):
    agente(ctx.raiz, "ingeniero-sivac", tools=("Read", "Grep", "Glob", "Write"))
    assert estados(eg.seccion_agentes(ctx))["ingeniero-sivac solo lectura"] == eg.FALLA


def test_skill_inexistente_falla_y_mcp_es_aviso(ctx):
    agente(ctx.raiz, "ingeniero-sivac", tools=("Read", "Grep", "Glob"), skills=("sk1", "nada", "context7"))
    res = eg.seccion_agentes(ctx)
    e = estados(res)
    assert e["skills existentes"] == eg.FALLA
    assert "ingeniero-sivac→nada" in next(r.detalle for r in res if r.nombre == "skills existentes")
    assert e["skills que son MCP"] == eg.AVISO


def test_skill_global_cuenta(ctx):
    (ctx.skills_globales / "glob1").mkdir(parents=True)
    (ctx.skills_globales / "glob1/SKILL.md").write_text("x", encoding="utf-8")
    agente(ctx.raiz, "ingeniero-sivac", tools=("Read", "Grep", "Glob"), skills=("glob1",))
    assert estados(eg.seccion_agentes(ctx))["skills existentes"] == eg.OK


def test_campo_faltante_y_yaml_roto(ctx):
    escribir(ctx.raiz, ".claude/agents/a.md", "---\nname: a\ndescription: d\n---\n")
    escribir(ctx.raiz, ".claude/agents/b.md", "sin frontmatter")
    e = estados(eg.seccion_agentes(ctx))
    assert e["frontmatter (campos)"] == eg.FALLA
    assert e["b.md"] == eg.FALLA


# --- AGENTS.md -------------------------------------------------------------
def test_agents_md_coherencia(ctx):
    agente(ctx.raiz, "uno")
    agente(ctx.raiz, "dos")
    escribir(ctx.raiz, "AGENTS.md", "| Squad | Agente |\n|---|---|\n| **A** | `uno` | x |\n| **B** | `fantasma` | x |\n")
    r = eg.seccion_agents_md(ctx)[0]
    assert r.estado == eg.FALLA and "fantasma" in r.detalle and "dos" in r.detalle
    escribir(ctx.raiz, "AGENTS.md", "| **A** | `uno` | x |\n| **B** | `dos` | x |\n")
    assert eg.seccion_agents_md(ctx)[0].estado == eg.OK


# --- hooks -----------------------------------------------------------------
def test_hooks(ctx):
    bueno = escribir(ctx.raiz, ".claude/hooks/ok.cjs", "const a = 1;\n")
    malo = escribir(ctx.raiz, ".claude/hooks/mal.cjs", "const = ;;\n")
    cfg = {"hooks": {"Stop": [{"hooks": [
        {"type": "command", "command": f'node "{bueno}"'},
        {"type": "command", "command": f'node "{malo}"'},
        {"type": "command", "command": f'node "{ctx.raiz}/.claude/hooks/no_existe.cjs"'}]}]}}
    escribir(ctx.raiz, ".claude/settings.json", json.dumps(cfg))
    e = estados(eg.seccion_hooks(ctx))
    assert e["Stop: ok.cjs"] == eg.OK
    assert e["Stop: mal.cjs"] == eg.FALLA
    assert e["Stop: no_existe.cjs"] == eg.FALLA


def test_hooks_sin_settings(ctx):
    assert eg.seccion_hooks(ctx)[0].estado == eg.FALLA


# --- reglas y schemas ------------------------------------------------------
def test_reglas_y_schemas(ctx):
    for n in eg.REGLAS_ESPERADAS[:3]:
        escribir(ctx.raiz, f".claude/rules/{n}", "# r")
    escribir(ctx.raiz, ".claude/schemas/bueno.schema.json",
             json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"}))
    escribir(ctx.raiz, ".claude/schemas/malo.schema.json", json.dumps({"type": 12}))
    escribir(ctx.raiz, ".claude/schemas/roto.schema.json", "{no json")
    e = estados(eg.seccion_reglas_schemas(ctx))
    assert e["reglas canónicas"] == eg.FALLA  # falta la 04
    assert e["schema bueno.schema.json"] == eg.OK
    assert e["schema malo.schema.json"] == eg.FALLA
    assert e["schema roto.schema.json"] == eg.FALLA


# --- MCP -------------------------------------------------------------------
def test_mcp_variables_sin_imprimir_valores(ctx, monkeypatch):
    monkeypatch.setenv("VAR_PRESENTE", "SECRETO-NO-IMPRIMIR")
    monkeypatch.delenv("VAR_AUSENTE", raising=False)
    cfg = {"mcpServers": {
        "a": {"type": "http", "url": "https://x", "headers": {"Authorization": "Bearer ${VAR_PRESENTE}"}},
        "b": {"type": "http", "url": "https://x", "headers": {"Authorization": "Bearer ${VAR_AUSENTE}"}},
        "c": {"command": "comando-que-no-existe-xyz", "args": []}}}
    escribir(ctx.raiz, ".mcp.json", json.dumps(cfg))
    res = eg.seccion_mcp(ctx)
    e = estados(res)
    assert e["a: variables"] == eg.OK
    assert e["b: variables"] == eg.FALLA
    assert e["c: ejecutable comando-que-no-existe-xyz"] == eg.FALLA
    assert "SECRETO-NO-IMPRIMIR" not in json.dumps([r.__dict__ for r in res])


def test_mcp_variable_en_settings_local(ctx, monkeypatch):
    monkeypatch.delenv("VAR_LOCAL", raising=False)
    escribir(ctx.raiz, ".claude/settings.local.json", json.dumps({"env": {"VAR_LOCAL": "x"}}))
    escribir(ctx.raiz, ".mcp.json", json.dumps({"mcpServers": {"a": {"url": "${VAR_LOCAL}"}}}))
    assert estados(eg.seccion_mcp(ctx))["a: variables"] == eg.OK


def test_mcp_sin_archivo(ctx):
    assert eg.seccion_mcp(ctx)[0].estado == eg.FALLA


# --- zotero (mock de red) --------------------------------------------------
class Resp:
    def __init__(self, code=200, data=None):
        self.status_code, self._d = code, data

    def json(self):
        return self._d


def test_zotero_ok(monkeypatch):
    def falso(url, **kw):
        assert kw["proxies"] == {"http": None, "https": None}
        return Resp(200, [{"key": eg.rutas.ZOTERO_COLECCION}]) if "collections" in url else Resp(200)
    monkeypatch.setattr(eg.requests, "get", falso)
    assert all(r.estado == eg.OK for r in eg.seccion_zotero())


def test_zotero_inactivo(monkeypatch):
    def falso(url, **kw):
        raise requests.ConnectionError("rechazada")
    monkeypatch.setattr(eg.requests, "get", falso)
    assert all(r.estado == eg.FALLA for r in eg.seccion_zotero())


def test_zotero_sin_coleccion(monkeypatch):
    monkeypatch.setattr(eg.requests, "get",
                        lambda url, **kw: Resp(200, [{"key": "OTRA"}]) if "collections" in url else Resp(200))
    assert estados(eg.seccion_zotero())[f"colección {eg.rutas.ZOTERO_COLECCION}"] == eg.FALLA


# --- seguridad y salidas ---------------------------------------------------
def git(raiz: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(raiz), *args], check=True, capture_output=True)


def git_init(raiz: Path) -> None:
    raiz.mkdir(parents=True, exist_ok=True)
    git(raiz, "init", "-q")
    git(raiz, "config", "user.email", "t@t")
    git(raiz, "config", "user.name", "t")


def test_referencias_modificadas(ctx):
    git_init(ctx.raiz)
    escribir(ctx.raiz, "referencias/a.txt", "original")
    git(ctx.raiz, "add", ".")
    git(ctx.raiz, "commit", "-qm", "x")
    assert estados(eg.seccion_seguridad(ctx))["referencias/ inmutable"] == eg.OK
    (ctx.raiz / "referencias/a.txt").write_text("alterado", encoding="utf-8")
    assert estados(eg.seccion_seguridad(ctx))["referencias/ inmutable"] == eg.FALLA


def test_datos_raw_sin_manifest(ctx):
    git_init(ctx.raiz)
    escribir(ctx.raiz, "datos/raw/prueba.csv", "a,b\n")  # fixture vacío de prueba, no es dato de la tesis
    r = next(x for x in eg.seccion_seguridad(ctx) if x.nombre == "datos/raw")
    assert r.estado == eg.AVISO and "CRÍTICO" in r.detalle
    escribir(ctx.raiz, "datos/raw/MANIFEST.md", "prueba.csv entregado por el tesista")
    r = next(x for x in eg.seccion_seguridad(ctx) if x.nombre == "datos/raw")
    assert r.estado == eg.OK


def test_datos_raw_vacio(ctx):
    git_init(ctx.raiz)
    (ctx.raiz / "datos/raw").mkdir(parents=True)
    assert next(x for x in eg.seccion_seguridad(ctx) if x.nombre == "datos/raw").estado == eg.OK


def test_salidas_docx_prematuro(ctx):
    escribir(ctx.raiz, "salidas/documentos/informe_final_v01.docx", "x")
    escribir(ctx.raiz, "salidas/figuras/f.png", "x")
    assert estados(eg.seccion_salidas(ctx))["entregables .docx"] == eg.AVISO
    escribir(ctx.vault, "00_SISTEMA/ESTADO_TESIS.md", "Autorizado por el tesista: informe_final_v01.docx\n")
    assert estados(eg.seccion_salidas(ctx))["entregables .docx"] == eg.OK


@pytest.mark.parametrize("linea", [
    "- informe_final_v01.docx: NO autorizado por el tesista",
    "informe_final_v01.docx no ha sido autorizado",
    "Autorización pendiente: informe_final_v01.docx",
    "informe_final_v01.docx desautorizado",
    "[ ] autorizado informe_final_v01.docx",
])
def test_salidas_autorizacion_negada_no_da_ok(ctx, linea):
    escribir(ctx.raiz, "salidas/documentos/informe_final_v01.docx", "x")
    escribir(ctx.vault, "00_SISTEMA/ESTADO_TESIS.md", linea + "\n")
    r = next(x for x in eg.seccion_salidas(ctx) if x.nombre == "entregables .docx")
    assert r.estado == eg.AVISO and "informe_final_v01.docx" in r.detalle


def test_salidas_negativa_prevalece_sobre_afirmativa(ctx):
    escribir(ctx.raiz, "salidas/documentos/a.docx", "x")
    escribir(ctx.vault, "00_SISTEMA/ESTADO_TESIS.md",
             "Autorizado por el tesista: a.docx\nAhora: a.docx NO autorizado (revocado)\n")
    assert estados(eg.seccion_salidas(ctx))["entregables .docx"] == eg.AVISO


def test_salidas_docx_en_subcarpeta_se_detecta(ctx):
    escribir(ctx.raiz, "salidas/documentos/sub/x.docx", "x")
    escribir(ctx.raiz, "salidas/documentos/~$tmp.docx", "x")  # bloqueo de Word: se ignora
    r = next(x for x in eg.seccion_salidas(ctx) if x.nombre == "entregables .docx")
    assert r.estado == eg.AVISO and "sub/x.docx" in r.detalle and "tmp" not in r.detalle
    escribir(ctx.vault, "00_SISTEMA/ESTADO_TESIS.md", "Autorizado por el tesista: sub/x.docx\n")
    assert estados(eg.seccion_salidas(ctx))["entregables .docx"] == eg.OK


def test_salidas_nombre_con_sin_no_es_negacion_y_subcadena_no_autoriza(ctx):
    escribir(ctx.raiz, "salidas/documentos/sin_titulo.docx", "x")
    escribir(ctx.raiz, "salidas/documentos/v01.docx", "x")
    escribir(ctx.vault, "00_SISTEMA/ESTADO_TESIS.md",
             "Autorizado: sin_titulo.docx\nAutorizado: informe_v01.docx\n")
    r = next(x for x in eg.seccion_salidas(ctx) if x.nombre == "entregables .docx")
    assert "sin_titulo.docx" not in r.detalle   # autorizado correctamente
    assert "v01.docx" in r.detalle              # 'informe_v01.docx' no autoriza 'v01.docx'


def test_salidas_autorizaciones_json(ctx):
    escribir(ctx.raiz, "salidas/documentos/a.docx", "x")
    escribir(ctx.raiz, "salidas/documentos/b.docx", "x")
    escribir(ctx.raiz, "salidas/documentos/AUTORIZACIONES.json", json.dumps({"a.docx": True, "b.docx": False}))
    r = next(x for x in eg.seccion_salidas(ctx) if x.nombre == "entregables .docx")
    assert r.estado == eg.AVISO and r.extra["negados"] == ["b.docx"]


# --- frontmatter con cadenas separadas por comas ---------------------------
def test_frontmatter_tools_y_skills_como_cadena(ctx):
    escribir(ctx.raiz, ".claude/agents/ingeniero-sivac.md",
             "---\nname: ingeniero-sivac\ndescription: d\ntools: Read, Grep, Glob\nskills: sk1\nsquad: S\n---\n")
    escribir(ctx.raiz, ".claude/agents/director-general.md",
             "---\nname: director-general\ndescription: d\ntools: Read, Agent\nskills: sk1, context7\nsquad: S\n---\n")
    res = eg.seccion_agentes(ctx)
    e = estados(res)
    assert e["skills existentes"] == eg.OK, [(r.nombre, r.detalle) for r in res]
    assert e["ingeniero-sivac solo lectura"] == eg.OK
    assert e["'Agent' solo en director-general"] == eg.OK


def test_como_lista():
    assert eg.como_lista("a, b ,,c") == ["a", "b", "c"]
    assert eg.como_lista(["a", " b "]) == ["a", "b"]
    assert eg.como_lista(None) == []


# --- datos/raw: otras extensiones ------------------------------------------
def test_datos_raw_json_parquet_detectados(ctx):
    git_init(ctx.raiz)
    escribir(ctx.raiz, "datos/raw/prueba.json", "{}")        # fixture de prueba, no es dato de la tesis
    escribir(ctx.raiz, "datos/raw/prueba.parquet", "x")
    r = next(x for x in eg.seccion_seguridad(ctx) if x.nombre == "datos/raw")
    assert r.estado == eg.AVISO and "prueba.json" in r.detalle and "prueba.parquet" in r.detalle


# --- MCP: variable vacía ---------------------------------------------------
def test_mcp_variable_vacia_cuenta_como_ausente(ctx, monkeypatch):
    monkeypatch.setenv("VAR_VACIA_X", "")
    escribir(ctx.raiz, ".mcp.json", json.dumps({"mcpServers": {"a": {"url": "${VAR_VACIA_X}"}}}))
    assert estados(eg.seccion_mcp(ctx))["a: variables"] == eg.FALLA


# --- hooks con espacios sin comillas ---------------------------------------
def test_extraer_scripts_cjs():
    assert eg.extraer_scripts_cjs('node "C:/a b/h.cjs" --x') == ["C:/a b/h.cjs"]
    assert eg.extraer_scripts_cjs("node C:/a b/h x.cjs") == ["C:/a b/h x.cjs"]
    assert eg.extraer_scripts_cjs("node $CLAUDE_PROJECT_DIR/.claude/hooks/h.cjs") == [
        "$CLAUDE_PROJECT_DIR/.claude/hooks/h.cjs"]
    assert eg.extraer_scripts_cjs("echo nada") == []


def test_hook_con_espacios_sin_comillas(ctx):
    h = escribir(ctx.raiz, ".claude/hooks/h x.cjs", "const a = 1;\n")
    cfg = {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": f"node {h}"}]}]}}
    escribir(ctx.raiz, ".claude/settings.json", json.dumps(cfg))
    assert estados(eg.seccion_hooks(ctx))["Stop: h x.cjs"] == eg.OK


# --- índices de PDF con JSON de tipo inesperado -----------------------------
def test_indice_con_json_no_objeto_no_rompe_la_seccion(ctx):
    import fitz
    from scripts.fuentes import ingesta_pdf
    ctx.pdfs.mkdir(parents=True)
    for n in ("a", "b"):
        doc = fitz.open()
        doc.new_page().insert_text((72, 72), f"Texto de prueba {n} suficientemente largo para el fixture.")
        doc.save(ctx.pdfs / f"{n}.pdf")
        doc.close()
    a = ctx.pdfs / "a.pdf"
    ingesta_pdf.guardar_indice(ingesta_pdf.ingestar(a), ingesta_pdf.ruta_indice(a, ctx.indices))
    destino_b = ingesta_pdf.ruta_indice(ctx.pdfs / "b.pdf", ctx.indices)
    destino_b.parent.mkdir(parents=True, exist_ok=True)
    destino_b.write_text("[]", encoding="utf-8")
    res = eg.seccion_indices(ctx)
    assert res[0].nombre == "índices vigentes" and res[0].estado == eg.FALLA
    assert "ilegibles" in res[0].detalle and "b.pdf" in res[0].detalle


# --- índices de PDF --------------------------------------------------------
def test_indices_pdf(ctx):
    import fitz
    from scripts.fuentes import ingesta_pdf
    ctx.pdfs.mkdir(parents=True)
    pdf = ctx.pdfs / "prueba.pdf"
    doc = fitz.open()
    doc.new_page().insert_text((72, 72), "Texto de prueba suficientemente largo para la capa de texto del fixture.")
    doc.save(pdf)
    doc.close()
    assert eg.seccion_indices(ctx)[0].estado == eg.FALLA  # sin índice
    ingesta_pdf.guardar_indice(ingesta_pdf.ingestar(pdf), ingesta_pdf.ruta_indice(pdf, ctx.indices))
    assert eg.seccion_indices(ctx)[0].estado == eg.OK
    d = fitz.open(pdf)
    d.new_page()
    d.saveIncr()
    d.close()
    r = eg.seccion_indices(ctx)[0]
    assert r.estado == eg.FALLA and "obsoleto" in r.detalle


# --- entorno ---------------------------------------------------------------
def test_tesseract_ausente_es_aviso(monkeypatch):
    monkeypatch.setattr(eg, "TESSERACT", Path("Z:/no/existe/tesseract.exe"))
    monkeypatch.setattr(eg.shutil, "which", lambda n: None)
    r = eg.comprobar_tesseract()[0]
    assert r.estado == eg.AVISO and "OCR no disponible" in r.detalle


def test_r_ausente_es_falla(monkeypatch):
    monkeypatch.setattr(eg, "RSCRIPT", Path("Z:/no/existe/Rscript.exe"))
    monkeypatch.setattr(eg.shutil, "which", lambda n: None)
    assert eg.comprobar_r()[0].estado == eg.FALLA


def test_word_omitido():
    assert eg.comprobar_word(True)[0].detalle.startswith("omitido")


def test_word_cierra_con_quit(monkeypatch):
    llamadas = []

    class FalsoWord:
        Version = "99"

        def Quit(self):
            llamadas.append("quit")

    cliente = types.SimpleNamespace(Dispatch=lambda n: FalsoWord(), DispatchEx=lambda n: FalsoWord())
    monkeypatch.setitem(sys.modules, "win32com", types.SimpleNamespace(client=cliente))
    monkeypatch.setitem(sys.modules, "win32com.client", cliente)
    assert eg.comprobar_word(False)[0].estado == eg.OK
    assert llamadas == ["quit"]


# --- orquestación y CLI ----------------------------------------------------
def test_resumen_y_tabla():
    res = [eg.Resultado("s", "a", eg.OK), eg.Resultado("s", "b", eg.FALLA, "mal")]
    assert eg.resumen(res) == {eg.OK: 1, eg.AVISO: 0, eg.FALLA: 1}
    assert "1 FALLA" in eg.formatear_tabla(res)


def test_seccion_rota_no_oculta_las_demas(ctx, monkeypatch):
    monkeypatch.setitem(eg.SECCIONES, "mcp", lambda c: 1 / 0)
    res = eg.ejecutar(ctx, ["mcp", "agents_md"])
    assert {r.seccion for r in res} == {"mcp", "agents_md"}
    assert any(r.nombre == "error interno" and r.estado == eg.FALLA for r in res)


def test_cli_json_y_codigos():
    script = str(RAIZ / "scripts/agentes/estado_granja.py")
    uso = subprocess.run([sys.executable, script, "--solo", "nada"], capture_output=True, text=True)
    assert uso.returncode == 2
    ok = subprocess.run([sys.executable, script, "--json", "--solo", "reglas,hooks"],
                        capture_output=True, text=True, encoding="utf-8")
    datos = json.loads(ok.stdout)
    assert set(datos) == {"resumen", "ok", "resultados"}
    assert ok.returncode == (0 if datos["ok"] else 1)
