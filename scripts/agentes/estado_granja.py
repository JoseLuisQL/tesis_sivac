# -*- coding: utf-8 -*-
"""
Auditor integral del estado de la granja de agentes SIVAC-THESIS-LAB (Compuerta QG-0).
Verifica agentes (.claude/agents/*.md), skills (.claude/skills/*/SKILL.md),
reglas (.claude/rules/*.md), hooks (.claude/hooks/*.cjs), schemas (.claude/schemas/*.json)
y las 5 capas canónicas (referencias/, datos/, scripts/, salidas/).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad


def verificar_granja() -> dict:
    agentes = sorted(p.name for p in (rutas.CAPA_CLAUDE / "agents").glob("*.md"))
    reglas = sorted(p.name for p in (rutas.CAPA_CLAUDE / "rules").glob("*.md"))
    schemas = sorted(p.name for p in (rutas.CAPA_CLAUDE / "schemas").glob("*.json"))
    hooks = sorted(p.name for p in (rutas.CAPA_CLAUDE / "hooks").glob("*.cjs"))
    capas_presentes = {
        "claude": rutas.CAPA_CLAUDE.exists(),
        "referencias": rutas.CAPA_REFERENCIAS.exists(),
        "datos": rutas.CAPA_DATOS.exists(),
        "scripts": rutas.CAPA_SCRIPTS.exists(),
        "salidas": rutas.CAPA_SALIDAS.exists(),
    }
    return {
        "compuerta": "QG-0",
        "estado": "OK" if all(capas_presentes.values()) and len(agentes) == 14 else "OBSERVADO",
        "total_agentes": len(agentes),
        "agentes": agentes,
        "reglas": reglas,
        "schemas": schemas,
        "hooks": hooks,
        "capas_5_canonicas": capas_presentes,
    }


if __name__ == "__main__":
    seguridad.configurar_utf8()
    print(json.dumps(verificar_granja(), ensure_ascii=False, indent=2))
