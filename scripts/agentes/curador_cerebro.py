# -*- coding: utf-8 -*-
"""
Custodio de la Bóveda de Conocimiento en Obsidian y de los Contratos de Handoff (Squad F).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad


def auditar_boveda() -> dict:
    seguridad.configurar_utf8()
    handoffs = sorted(rutas.HANDOFFS_DIR.glob("*.md")) if rutas.HANDOFFS_DIR.exists() else []
    return {
        "agente": "curador-cerebro",
        "squad": "Squad F (Gobernanza, Memoria y Evaluación Externa)",
        "boveda_path": str(rutas.BOVEDA_OBSIDIAN),
        "estado_tesis_presente": rutas.ESTADO_TESIS_MD.exists(),
        "decisiones_presente": rutas.DECISIONES_MD.exists(),
        "total_handoffs": len(handoffs),
        "handoffs": [h.name for h in handoffs],
    }


if __name__ == "__main__":
    print(json.dumps(auditar_boveda(), indent=2, ensure_ascii=False))
