"""Pruebas de scripts/agentes/inventario_syncova.py.

Todo el repositorio Express/Prisma/React se fabrica en tmp_path (FIXTURE de prueba):
no hay datos empíricos de la tesis ni se toca syncova real salvo lectura opcional.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.agentes import escritura_segura, inventario_syncova as inv  # noqa: E402
from scripts.comun import rutas, seguridad  # noqa: E402

SCHEMA = '''
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
enum EstadoVale {
  borrador
  emitido @map("EMITIDO")
}
// comentario
model Vacuna {
  id      String  @id @default(uuid())
  nombre  String  @unique
  activo  Boolean @default(true)
  vales   ValeDetalle[]
  @@map("vacunas")
}
model Vale {
  id        String  @id
  estado    EstadoVale @default(borrador)
  detalles  ValeDetalle[]
  @@map("vales")
}
model ValeDetalle {
  id        String  @id
  valeId    String  @map("vale_id")
  vacunaId  String?
  cantidad  Int
  vale      Vale    @relation(fields: [valeId], references: [id])
  vacuna    Vacuna? @relation(fields: [vacunaId], references: [id])
}
'''

RUTAS_VALES = '''
import { Router } from 'express';
import { authenticate } from '@/middleware/auth';
import { validatePermissions } from '@/middleware/permissions';
import { ValeController } from '@/controllers/ValeController';
const router = Router();
// router.get('/comentado', ValeController.no);
router.get('/publico', ValeController.publico);
router.use(authenticate);
const soloAdmin = validatePermissions(['admin']);
router.get('/', ValeController.listar);
router.post('/emitir', soloAdmin, ValeController.emitir);
router.delete('/:id', validatePermissions(['admin']), async (req, res) => { res.end(); });
export default router;
'''

RUTAS_AUTH = '''
import { Router } from 'express';
import { AuthController } from '../controllers/AuthController';
const router = Router();
router.post('/login', AuthController.login);
export default router;
'''

INDEX_TS = '''
import express from 'express';
import valesRoutes from '@/routes/vales';
import authRoutes from './routes/auth';
const app = express();
app.get('/health', (req, res) => res.json({ ok: true }));
app.use('/api/auth', authRoutes);
app.use('/api/vales', valesRoutes);
const port = process.env.PORT || 3000;
const { JWT_SECRET, DB_HOST = 'x' } = process.env;
'''

APP_ROUTES = '''
import React, { lazy } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from '../auth/ProtectedRoute';
const Vales = lazy(() => import('../Vales/Vales'));
export default () => (
  <Routes>
    <Route path="/" element={<Navigate to="/vales" replace />} />
    <Route path="/vales/*" element={<ProtectedRoute requiredRoles={['administrador']}><Vales /></ProtectedRoute>} />
    {/* <Route path="/muerta" element={<Otra />} /> */}
  </Routes>
);
'''


def _w(base: Path, rel: str, txt: str) -> None:
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:   # escribe en tmp_path de PRUEBA
        f.write(txt)


@pytest.fixture()
def repo(tmp_path):
    r = tmp_path / "falso_syncova"
    _w(r, "package.json", json.dumps({"name": "front", "version": "1.2.3", "scripts": {"dev": "vite"},
                                      "dependencies": {"react": "^18.3.1", "react-router-dom": "^6.20.1"},
                                      "devDependencies": {"vite": "^5.4.19"}}))
    _w(r, "backend/package.json", json.dumps({"name": "back", "version": "0.1.0", "scripts": {"test": "jest"},
                                              "dependencies": {"express": "^4.18.2", "@prisma/client": "^5.7.1"},
                                              "devDependencies": {"jest": "^29.0.0"}}))
    _w(r, "backend/prisma/schema.prisma", SCHEMA)
    _w(r, "backend/prisma/migrations/20260101_inicial/migration.sql", "CREATE TABLE x();")
    _w(r, "backend/src/index.ts", INDEX_TS)
    _w(r, "backend/src/routes/vales.ts", RUTAS_VALES)
    _w(r, "backend/src/routes/auth.ts", RUTAS_AUTH)
    _w(r, "backend/src/__tests__/vale.test.ts", "describe('v', () => {\n  it('a', () => {});\n  test('b', () => {});\n});")
    _w(r, "src/components/routing/AppRoutes.tsx", APP_ROUTES)
    _w(r, "src/components/Vales/Vales.tsx", "export default function Vales(){ return null }")
    _w(r, "tests/ui/e2e.spec.ts", "test('e2e', async () => {});")
    # Secretos y excluidos: contienen marcas que NO deben aparecer jamás.
    _w(r, ".env", "SUPER_SECRETO_VALOR=abc123")
    _w(r, "backend/.env.local", "OTRO_SECRETO=zzz")
    _w(r, "certs/server.pem", "-----BEGIN PRIVATE KEY-----")
    _w(r, "config/credentials.json", '{"token": "ULTRASECRETO"}')
    _w(r, "node_modules/pkg/index.js", "process.env.DESDE_NODE_MODULES; router.get('/nm', x);")
    _w(r, "dist/bundle.js", "process.env.DESDE_DIST;")
    _w(r, ".git/HEAD", "ref: refs/heads/main\n")
    _w(r, ".git/refs/heads/main", "a" * 40 + "\n")
    return r


# --------------------------------------------------------------------------- utilidades
def test_quitar_comentarios_conserva_posiciones_y_cadenas():
    src = "a // x\nb /* y\nz */ c '//no'"
    out = inv.quitar_comentarios(src)
    assert len(out) == len(src) and out.count("\n") == src.count("\n")
    assert "x" not in out.split("\n")[0] and "'//no'" in out


def test_es_secreto():
    for n in (".env", ".env.local", ".env.example", "a.pem", "k.key", "credentials.json", "id_rsa", "service-account-x.json"):
        assert inv.es_secreto(n), n
    for n in ("env.ts", "schema.prisma", "keyboard.ts", "package.json"):
        assert not inv.es_secreto(n), n


def test_extraer_args_respeta_anidamiento():
    t = "x.get('/a,b', f(1, 2), [1,2], (req) => { return 1, 2 })"
    args, fin = inv.extraer_args(t, t.index("("))
    assert len(args) == 4 and t[fin] == ")"


# --------------------------------------------------------------------------- Prisma
def test_prisma_modelos_campos_enums_relaciones():
    p = inv.parsear_prisma(SCHEMA, "schema.prisma")
    assert p["proveedor_bd"] == "postgresql"
    assert [m["nombre"] for m in p["modelos"]] == ["Vacuna", "Vale", "ValeDetalle"]
    assert p["modelos"][0]["tabla"] == "vacunas"
    vac = {c["nombre"]: c for c in p["modelos"][0]["campos"]}
    assert vac["id"]["pk"] and vac["nombre"]["unico"] and vac["activo"]["default"] == "true"
    enum = p["enums"][0]
    assert enum["nombre"] == "EstadoVale" and enum["valores"][1] == {"nombre": "emitido", "map": "EMITIDO"}
    rel = {(r["origen"], r["campo"]): r for r in p["relaciones"]}
    assert rel[("ValeDetalle", "vale")]["cardinalidad_desde_origen"] == "N:1"
    assert rel[("ValeDetalle", "vale")]["fields"] == ["valeId"]
    assert rel[("Vale", "detalles")]["cardinalidad_desde_origen"] == "1:N"
    det = {c["nombre"]: c for c in p["modelos"][2]["campos"]}
    assert det["vacunaId"]["opcional"] is True


# --------------------------------------------------------------------------- Express
def test_endpoints_prefijos_y_autenticacion(repo):
    ex = inv.extraer_endpoints(inv.Arbol(repo))
    e = {(x["metodo"], x["ruta"]): x for x in ex["endpoints"]}
    assert ("GET", "/health") in e and e[("GET", "/health")]["autenticacion"] == "ninguna"
    assert ("POST", "/api/auth/login") in e
    assert e[("POST", "/api/auth/login")]["autenticacion"] == "ninguna"
    assert ("GET", "/api/vales/comentado") not in e            # comentario ignorado
    assert e[("GET", "/api/vales/publico")]["autenticacion"] == "ninguna"   # antes del router.use(authenticate)
    listar = e[("GET", "/api/vales")]
    assert listar["autenticacion"] == "obligatoria" and listar["origen_autenticacion"] == "router.use"
    emitir = e[("POST", "/api/vales/emitir")]
    assert emitir["autorizacion"] == ["soloAdmin"]             # alias de validatePermissions
    borrar = e[("DELETE", "/api/vales/:id")]
    assert borrar["handler"] == "(función en línea)" and borrar["autorizacion"]
    assert e[("GET", "/api/vales")]["archivo_linea"] == "backend/src/routes/vales.ts:11"
    assert ex["total"] == 6                                      # /nm de node_modules excluido


# --------------------------------------------------------------------------- React Router
def test_rutas_react(repo):
    rr = inv.extraer_rutas_react(inv.Arbol(repo))
    assert rr["total"] == 2                                      # la ruta comentada no cuenta
    v = next(x for x in rr["rutas"] if x["path"] == "/vales/*")
    assert v["componente"] == "Vales" and v["protegida"] and v["roles_requeridos"] == ["administrador"]
    assert v["archivo_componente"] == "src/components/Vales/Vales.tsx"
    assert next(x for x in rr["rutas"] if x["path"] == "/")["redirige_a"] == "/vales"


# --------------------------------------------------------------------------- inventario completo
def test_inventario_completo_y_exclusiones(repo):
    i = inv.construir_inventario(repo)
    r = i["resumen"]
    assert r["modelos"] == 3 and r["enums"] == 1 and r["endpoints"] == 6 and r["rutas_react"] == 2
    assert r["archivos_prueba"] == 2 and r["casos_prueba_aprox"] == 3 and r["migraciones_prisma"] == 1
    assert i["commit"]["commit"] == "a" * 40 and i["commit"]["fuente"].startswith(".git/HEAD")
    nombres_env = {v["nombre"] for v in i["variables_entorno"]["variables"]}
    assert {"PORT", "JWT_SECRET", "DB_HOST"} <= nombres_env
    assert "DESDE_NODE_MODULES" not in nombres_env and "DESDE_DIST" not in nombres_env
    assert ".env" in i["estructura"]["secretos_omitidos"] and "certs/server.pem" in i["estructura"]["secretos_omitidos"]
    blob = json.dumps(i, ensure_ascii=False)
    for prohibido in ("SUPER_SECRETO_VALOR", "abc123", "OTRO_SECRETO", "ULTRASECRETO", "PRIVATE KEY", "zzz"):
        assert prohibido not in blob, prohibido
    tec = {t["paquete"] for t in i["stack"]["tecnologias_clave"]}
    assert {"react", "express", "@prisma/client", "jest", "vite"} <= tec
    assert len(i["huella_sha256"]) == 64
    md = inv.a_markdown(i)
    assert "## Endpoints Express" in md and "a" * 40 in md and "SUPER_SECRETO_VALOR" not in md


def test_lectura_de_secreto_denegada(repo):
    with pytest.raises(PermissionError):
        inv._leer_texto(repo / ".env")


def test_commit_desde_packed_refs(tmp_path):
    r = tmp_path / "r"
    _w(r, ".git/HEAD", "ref: refs/heads/dev\n")
    _w(r, ".git/packed-refs", "# pack-refs\n" + "b" * 40 + " refs/heads/dev\n")
    g = inv._commit_manual(r)
    assert g["commit"] == "b" * 40 and g["rama"] == "dev"


def test_sin_git_no_inventa_commit(tmp_path):
    r = tmp_path / "sin_git"
    _w(r, "a.ts", "const x = 1;")
    g = inv.info_git(r)
    assert g["commit"] is None and any("VERIFICAR" in a for a in g["advertencias"])


# --------------------------------------------------------------------------- trazar
def test_trazar_por_palabra_sin_acentos(repo):
    i = inv.construir_inventario(repo)
    t = inv.trazar(repo, ["VALE"], inventario=i)
    assert {m["modelo"] for m in t["modelos"]} >= {"Vale", "ValeDetalle"}
    assert any(e["ruta"] == "/api/vales/emitir" for e in t["endpoints"])
    assert any(x["path"] == "/vales/*" for x in t["rutas_react"])
    assert any(p["archivo"].endswith("vale.test.ts") for p in t["pruebas"])
    assert any(m["archivo_linea"].startswith("backend/prisma/schema.prisma:") for m in t["menciones"])
    assert "node_modules" not in json.dumps(t)
    vacio = inv.trazar(repo, ["HU-99"], inventario=i)
    assert vacio["total_coincidencias"] == 0


# --------------------------------------------------------------------------- solo lectura
def test_codigo_no_contiene_escrituras_sobre_el_repositorio():
    """Inspección estática: el módulo no escribe, mueve ni borra nada."""
    for archivo in (Path(inv.__file__),):
        codigo = inv.quitar_comentarios(archivo.read_text(encoding="utf-8"))
        assert not re.search(r"open\([^)]*,\s*['\"][^'\"]*[wax+][^'\"]*['\"]", codigo), "open() en modo escritura"
        assert not re.search(r"mode\s*=\s*['\"][^'\"]*[wax+]", codigo)
        for prohibido in ("write_text", "write_bytes", ".write(", "os.remove", "os.unlink", "os.rename",
                          "os.replace", "os.makedirs", "os.mkdir", "shutil.", ".unlink(", ".rmdir(",
                          ".mkdir(", ".touch(", "rmtree", ".rename(", ".replace(Path", ".chmod("):
            assert prohibido not in codigo, prohibido
        # Solo se invoca git en modo lectura.
        subcomandos = re.findall(r'_git\(\s*"([^"]+)"', codigo)
        assert subcomandos and set(subcomandos) <= {"rev-parse", "log"}, subcomandos


def test_subprocess_git_solo_lectura():
    codigo = Path(inv.__file__).read_text(encoding="utf-8")
    assert not re.search(r'_git\(\s*"(commit|add|checkout|reset|clean|push|pull|fetch|gc|config|stash|rm|mv)"', codigo)
    assert codigo.count("subprocess.run(") == 1


def test_escritor_rechaza_destino_dentro_del_repositorio(repo):
    with pytest.raises(seguridad.EscrituraProhibida):
        escritura_segura.escribir_salida(repo / "inventario.md", "x", no_escribir_en=repo)
    with pytest.raises(seguridad.EscrituraProhibida):
        escritura_segura.escribir_salida(rutas.SYNCOVA / "x.md", "x")


def test_cli_no_modifica_el_repositorio_y_guarda_fuera(repo, tmp_path, capsys):
    antes = sorted((p.relative_to(repo).as_posix(), p.stat().st_mtime_ns, p.stat().st_size)
                   for p in repo.rglob("*") if p.is_file())
    salida = tmp_path / "salida" / "inv.json"
    md = tmp_path / "salida" / "inv.md"
    rc = inv.main(["inventario", "--raiz", str(repo), "--salida-json", str(salida), "--salida-md", str(md)])
    assert rc == 0 and salida.is_file() and md.is_file()
    assert json.loads(salida.read_text(encoding="utf-8"))["resumen"]["modelos"] == 3
    despues = sorted((p.relative_to(repo).as_posix(), p.stat().st_mtime_ns, p.stat().st_size)
                     for p in repo.rglob("*") if p.is_file())
    assert antes == despues
    # Destino dentro del repositorio: rechazado.
    with pytest.raises(seguridad.EscrituraProhibida):
        inv.main(["inventario", "--raiz", str(repo), "--salida-md", str(repo / "x.md")])


def test_cli_json_trazar_y_uso_incorrecto(repo, capsys):
    assert inv.main(["trazar", "--raiz", str(repo), "vale", "--json"]) == 0
    datos = json.loads(capsys.readouterr().out)
    assert datos["total_coincidencias"] > 0
    assert inv.main(["trazar", "--raiz", str(repo), "palabra_inexistente_xyz"]) == 1
    assert inv.main(["inventario", "--raiz", str(repo / "no_existe")]) == 2
    with pytest.raises(SystemExit) as e:
        inv.main([])
    assert e.value.code == 2


# --------------------------------------------------------------------------- lectura real (opcional)
@pytest.mark.skipif(not (rutas.SYNCOVA / "backend" / "prisma" / "schema.prisma").is_file(),
                    reason="syncova no disponible")
def test_syncova_real_solo_lectura():
    """Humo sobre el repositorio real; verifica que no cambia nada (mtime/tamaño de archivos clave)."""
    claves = [rutas.SYNCOVA / "backend/prisma/schema.prisma", rutas.SYNCOVA / "package.json",
              rutas.SYNCOVA / "backend/src/index.ts"]
    antes = [(p.stat().st_mtime_ns, p.stat().st_size) for p in claves]
    i = inv.construir_inventario(rutas.SYNCOVA)
    assert i["resumen"]["modelos"] > 0 and i["resumen"]["endpoints"] > 0
    assert re.fullmatch(r"[0-9a-f]{40}", i["commit"]["commit"] or "")
    assert ".env" in i["estructura"]["secretos_omitidos"]
    assert "node_modules" in i["estructura"]["excluidos"]
    assert antes == [(p.stat().st_mtime_ns, p.stat().st_size) for p in claves]


# --------------------------------------------------------------------------- correcciones de verificación
@pytest.mark.parametrize("destino", [
    rutas.REFERENCIAS / "x.md",
    rutas.REFERENCIAS / "proyecto_base" / "x.md",
    rutas.DATOS_RAW / "x.json",
    rutas.RAIZ / "PROYECTO_TESIS.docx",
    rutas.SALIDAS / "PROYECTO_TESIS.docx",
])
def test_escritor_veta_referencias_datos_raw_y_proyecto_base(destino):
    with pytest.raises(seguridad.EscrituraProhibida):
        escritura_segura.escribir_salida(destino, "x")
    assert not destino.exists() or destino.name == "PROYECTO_TESIS.docx"


def test_cli_rechaza_destinos_vetados(repo):
    for opcion, destino in (("--salida-md", rutas.REFERENCIAS / "x.md"), ("--salida-json", rutas.DATOS_RAW / "x.json")):
        with pytest.raises(seguridad.EscrituraProhibida):
            inv.main(["inventario", "--raiz", str(repo), opcion, str(destino)])
    assert not (rutas.REFERENCIAS / "x.md").exists() and not (rutas.DATOS_RAW / "x.json").exists()


def test_subdirectorio_de_otro_repo_no_atribuye_commit(tmp_path):
    repo_padre = tmp_path / "padre"
    _w(repo_padre, "sub/a.ts", "const x = 1;")
    subprocess.run(["git", "init", "-q", str(repo_padre)], check=True)
    subprocess.run(["git", "-C", str(repo_padre), "-c", "user.name=t", "-c", "user.email=t@t", "commit",
                    "-q", "--allow-empty", "-m", "init"], check=True)
    g = inv.info_git(repo_padre / "sub")
    assert g["commit"] is None and any("VERIFICAR" in a for a in g["advertencias"])
    assert inv.info_git(repo_padre)["commit"] is not None


def test_variables_integradas_de_vite_no_cuentan(tmp_path):
    r = tmp_path / "r"
    _w(r, "src/a.ts", "const d = import.meta.env.DEV; const m = import.meta.env.MODE; const u = import.meta.env.VITE_API_URL; const n = process.env.NODE_ENV; const p = process.env.PORT;")
    e = inv.extraer_env(inv.Arbol(r))
    assert {v["nombre"] for v in e["variables"]} == {"VITE_API_URL", "PORT"} and e["total"] == 2
    assert {v["nombre"] for v in e["integradas_excluidas"]} == {"DEV", "MODE", "NODE_ENV"}


def test_enmascarar_secretos():
    assert "tu_jwt" not in inv.enmascarar_secretos('JWT_SECRET="tu_jwt_secret_muy_seguro"')
    assert "CAMBIAR" not in inv.enmascarar_secretos("JWT_SECRET=CAMBIAR_SECRET_LARGO")
    assert "eyJhbGciOiJIUzI1NiJ9" not in inv.enmascarar_secretos("Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abcdefghij")
    assert inv.enmascarar_secretos("const port = 3000;") == "const port = 3000;"


def test_trazar_enmascara_valores_de_secretos(tmp_path):
    r = tmp_path / "r"
    _w(r, "README.md", "Configurar vale\n" + 'JWT_SECRET="valor_real_123" para vale\n')
    tr = inv.trazar(r, ["vale"])
    assert all("valor_real_123" not in m["texto"] for m in tr["menciones"]) and tr["menciones"]


# --- Defectos hallados por el verificador independiente (regresión) -------------------
@pytest.mark.parametrize("linea,secreto", [
    ("- **Admin**: usuario: `admin`, password: `Admin123!`", "Admin123!"),
    ("- **Contraseña**: `Admin123!`", "Admin123!"),
    ("const ADMIN_PASS = 'Zx9!secreto'", "Zx9!secreto"),
    ("DB_PASS=hunter2hunter2", "hunter2hunter2"),
    ("clave: 'MiClaveSuperSecreta'", "MiClaveSuperSecreta"),
    ("DATABASE_URL=postgresql://usuario:pw_de_base@localhost:5432/db", "pw_de_base"),
    ("key: 'AIzaSyA1234567890abcdefghijklmnopqrstuv'", "AIzaSyA1234567890abcdefghijklmnopqrstuv"),
])
def test_enmascarar_cubre_nombres_y_urls_con_credenciales(linea, secreto):
    assert secreto not in inv.enmascarar_secretos(linea)


def test_enmascarar_no_toca_texto_inocuo():
    for s in ("const passengers = 3;", "ver el pasaporte digital", "import { authRoutes } from './auth'"):
        assert inv.enmascarar_secretos(s) == s


def test_no_lee_a_traves_de_enlaces_simbolicos_hacia_fuera(tmp_path):
    externo = tmp_path / "externo"
    externo.mkdir()
    (externo / ".env").write_text("TOKEN_INTERNO=valor_que_no_debe_salir\n", encoding="utf-8")
    (externo / "otro.ts").write_text("export const x = 'fuera_del_repo';\n", encoding="utf-8")
    r = tmp_path / "r"
    _w(r, "src/a.ts", "export const ok = 1;\n")
    try:
        (r / "src" / "enlace.ts").symlink_to(externo / ".env")
        (r / "src" / "enlace2.ts").symlink_to(externo / "otro.ts")
    except (OSError, NotImplementedError):
        pytest.skip("este sistema no permite crear enlaces simbólicos sin privilegios")
    arbol = inv.Arbol(r)
    assert "src/enlace.ts" not in arbol.archivos and "src/enlace2.ts" not in arbol.archivos
    assert {"src/enlace.ts", "src/enlace2.ts"} <= set(arbol.enlaces_omitidos)
    tr = inv.trazar(r, ["valor_que_no_debe_salir", "fuera_del_repo"])
    assert tr["total_coincidencias"] == 0


def test_escritor_solo_admite_salidas_y_no_pisa(tmp_path, monkeypatch):
    # Fuera de salidas/ y del temporal: vault, CLAUDE.md, .claude, scripts, datos.
    for destino in (rutas.VAULT / "nota.md", rutas.RAIZ / "CLAUDE.md", rutas.RAIZ / ".claude" / "settings.json",
                    rutas.RAIZ / "scripts" / "x.py", rutas.DATOS / "x.csv"):
        with pytest.raises(seguridad.EscrituraProhibida):
            escritura_segura.escribir_salida(destino, "x")
    # Destino permitido (temporal del SO): se crea; no se pisa sin autorización explícita.
    ok = tmp_path / "salida.md"
    escritura_segura.escribir_salida(ok, "uno")
    with pytest.raises(FileExistsError):
        escritura_segura.escribir_salida(ok, "dos")
    assert ok.read_text(encoding="utf-8") == "uno"
    escritura_segura.escribir_salida(ok, "dos", sobrescribir=True)
    assert ok.read_text(encoding="utf-8") == "dos"

