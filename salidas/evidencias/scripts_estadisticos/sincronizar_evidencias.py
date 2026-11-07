# -*- coding: utf-8 -*-
"""Sincroniza las copias de evidencia con las fuentes canónicas.

`salidas/evidencias/` conserva copias de la base de datos, del reporte
estadístico y de los scripts para que el expediente se pueda revisar sin
navegar el repositorio. Esas copias se desincronizan en cuanto se regenera el
conjunto de datos, de modo que este script las vuelve a derivar de su fuente
única y deja un registro de huellas SHA-256 en `SINCRONIZACION.json`.

No corrige ni reescribe datos: solo copia byte a byte y, en el caso del libro
Excel, lo reconstruye desde los CSV con `exportar_libro_campo.py`.

Uso:
    python scripts/estadistica/sincronizar_evidencias.py [--verificar]

`--verificar` no escribe: compara y devuelve código 1 si alguna copia difiere.
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
RECO = RAIZ / "datos" / "recolectados"
SINT = RAIZ / "datos" / "prueba_sintetica"
EST = RAIZ / "salidas" / "estadistica"
FIG = RAIZ / "salidas" / "figuras" / "estadistica"
EVID = RAIZ / "salidas" / "evidencias"
BASE = EVID / "base_de_datos"
TABLAS = EVID / "tablas_resultados"
FIGURAS = EVID / "figuras_spss_300dpi"
SCRIPTS = EVID / "scripts_estadisticos"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import exportar_libro_campo as LIBRO  # noqa: E402

COPias = [
    (RECO / "pretest_campo.csv", BASE / "pretest_campo.csv"),
    (RECO / "posttest_campo.csv", BASE / "posttest_campo.csv"),
    (SINT / "instrumento01_replicas.csv", BASE / "instrumento01_replicas.csv"),
    (SINT / "instrumento02_asientos.csv", BASE / "instrumento02_asientos.csv"),
    (SINT / "instrumento02_despachos.csv", BASE / "instrumento02_despachos.csv"),
    (SINT / "instrumento03_reactivos.csv", BASE / "instrumento03_reactivos.csv"),
    (SINT / "matriz_analitica_pre_post.csv",
     BASE / "matriz_analitica_pre_post.csv"),
    (SINT / "control_integridad.json", BASE / "control_integridad.json"),
    (RECO / "SIVAC_DATOS_CAMPO.md", BASE / "SIVAC_DATOS_CAMPO.md"),
    (RECO / "README.md", BASE / "README_DECLARACION_DEC007.md"),
    (EST / "reporte_estadistico_completo.json",
     TABLAS / "reporte_estadistico_completo.json"),
    (RAIZ / "scripts" / "estadistica" / "analisis_estadistico_sivac.py",
     SCRIPTS / "analisis_estadistico_sivac.py"),
    (RAIZ / "scripts" / "estadistica" / "generar_datos_sinteticos.py",
     SCRIPTS / "generar_datos_sinteticos.py"),
    (RAIZ / "scripts" / "estadistica" / "construir_registro_campo.py",
     SCRIPTS / "construir_registro_campo.py"),
    (RAIZ / "scripts" / "estadistica" / "consolidar_libro_captura.py",
     SCRIPTS / "consolidar_libro_captura.py"),
    (RAIZ / "scripts" / "estadistica" / "exportar_libro_campo.py",
     SCRIPTS / "exportar_libro_campo.py"),
    (RAIZ / "scripts" / "estadistica" / "sincronizar_evidencias.py",
     SCRIPTS / "sincronizar_evidencias.py"),
    (RAIZ / "scripts" / "estadistica" / "verificar_conjunto_datos.py",
     SCRIPTS / "verificar_conjunto_datos.py"),
    (RAIZ / "scripts" / "estadistica" / "inventario_datos.py",
     SCRIPTS / "inventario_datos.py"),
    (RAIZ / "scripts" / "utilidades" / "consultar_db_sivac.py",
     SCRIPTS / "consultar_db_sivac.py"),
] + [
    (FIG / f"figura_d{d}_{nombre}_spss.png", FIGURAS / f"figura_d{d}_{nombre}_spss.png")
    for d, nombre in ((1, "tiempos_boxplots"), (2, "consistencia_barras"),
                      (3, "satisfaccion_tam"))
]


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def filas(ruta: Path) -> int:
    with ruta.open(encoding="utf-8", newline="") as fh:
        return sum(1 for _ in csv.reader(fh)) - 1


def main(argv: list[str]) -> int:
    verificar = "--verificar" in argv
    faltantes = [(o, d) for o, d in COPias if not o.exists()]
    if faltantes:
        for origen, _ in faltantes:
            print(f"[FALTA] {origen.relative_to(RAIZ)}")
        return 2

    libro = BASE / "datos_recolectados_pre_post.xlsx"
    if verificar:
        LIBRO.exportar(BASE / "_libro_tmp.xlsx")
        diferencias = []
        for origen, destino in COPias:
            if not destino.exists() or sha256(origen) != sha256(destino):
                diferencias.append(str(destino.relative_to(RAIZ)))
        if sha256(BASE / "_libro_tmp.xlsx") != sha256(libro):
            diferencias.append(str(libro.relative_to(RAIZ)))
        (BASE / "_libro_tmp.xlsx").unlink()
        if diferencias:
            print("[DESINCRONIZADO]")
            for ruta in diferencias:
                print(f"  {ruta}")
            return 1
        print("[OK] Las copias de evidencia coinciden con las fuentes.")
        return 0

    for origen, destino in COPias:
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origen, destino)
    LIBRO.exportar(libro)

    registro = {
        "generado_por": "scripts/estadistica/sincronizar_evidencias.py",
        "fuente_unica": "datos/recolectados y datos/prueba_sintetica",
        "archivos": {
            str(destino.relative_to(EVID)): {
                "sha256": sha256(destino),
                "bytes": destino.stat().st_size,
            }
            for _, destino in COPias
        } | {
            str(libro.relative_to(EVID)): {
                "sha256": sha256(libro), "bytes": libro.stat().st_size}
        },
        "filas": {
            "pretest_campo.csv": filas(RECO / "pretest_campo.csv"),
            "posttest_campo.csv": filas(RECO / "posttest_campo.csv"),
            "instrumento01_replicas.csv":
                filas(SINT / "instrumento01_replicas.csv"),
            "instrumento02_asientos.csv":
                filas(SINT / "instrumento02_asientos.csv"),
            "instrumento02_despachos.csv":
                filas(SINT / "instrumento02_despachos.csv"),
            "instrumento03_reactivos.csv":
                filas(SINT / "instrumento03_reactivos.csv"),
        },
    }
    (EVID / "SINCRONIZACION.json").write_text(
        json.dumps(registro, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print(f"[OK] {len(COPias) + 1} archivos sincronizados en "
          f"{EVID.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
