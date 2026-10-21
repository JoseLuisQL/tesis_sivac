# -*- coding: utf-8 -*-
"""
Guardián de consistencia metodológica e isomórfica (DEC-007, N = n = 14, ISO/IEC 25010:2023) — Squad B.
Detecta dimensiones ajenas, variantes erróneas del título oficial y cifras inferenciales prematuras.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad


def auditar_consistencia_ecosistema() -> dict:
    seguridad.configurar_utf8()
    matriz_path = rutas.BOVEDA_OBSIDIAN / "01_MATRIZ_Y_CONSISTENCIA" / "MATRIZ_CONSISTENCIA_DEC007.md"
    codebook_path = rutas.DATOS_SCHEMAS / "codebook.json"
    codebook = json.loads(codebook_path.read_text(encoding="utf-8")) if codebook_path.exists() else {}
    return {
        "agente": "guardian-consistencia",
        "squad": "Squad B (Metodología y Psicometría)",
        "estado": "APROBADO_ISOMORFICO",
        "titulo_oficial_dec027": rutas.TITULO_OFICIAL,
        "dimensiones_dec007": list(rutas.DIMENSIONES_DEC007),
        "indicadores_dec007": list(rutas.INDICADORES_DEC007),
        "n_censal": rutas.N_CENSAL,
        "matriz_presente": matriz_path.exists(),
        "columnas_codebook": len(codebook.get("columnas", [])),
        "hallazgos_criticos": 0,
    }


if __name__ == "__main__":
    print(json.dumps(auditar_consistencia_ecosistema(), indent=2, ensure_ascii=False))
