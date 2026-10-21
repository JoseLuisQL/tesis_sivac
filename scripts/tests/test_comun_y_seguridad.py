# -*- coding: utf-8 -*-
"""
Pruebas unitarias de seguridad, bloqueo de escritura en rutas protegidas y bloqueo empírico sin MANIFEST.json.
"""
import pytest
from pathlib import Path
from scripts.comun import rutas, seguridad
from scripts.estadistica.manifest_datos import validar_manifest


def test_bloqueo_rutas_protegidas():
    for ruta_prohibida in [
        "C:/Proyectos/syncova/src/app.ts",
        "referencias/modelos_tesis/fany_2024.pdf",
        "referencias/proyecto_base/PROYECTO_TESIS.docx",
        "datos/raw/pretest_simulado.csv",
    ]:
        with pytest.raises(PermissionError):
            seguridad.asegurar_escritura_permitida(ruta_prohibida)


def test_pipeline_bloqueado_sin_manifest(tmp_path: Path):
    res = validar_manifest(tmp_path / "MANIFEST_INEXISTENTE.json")
    assert res["valido"] is False
    assert res["codigo_salida"] == 3
    assert "BLOQUEADO" in res["estado"]
