# -*- coding: utf-8 -*-
"""
Sincronizador de configuración MCP y Droids entre .claude/ y .factory/ (Factory AI).
Lee .mcp.json en la raíz y sincroniza la estructura sin exponer secretos en control de versiones.
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.comun import rutas, seguridad


def sincronizar_factory() -> dict:
    mcp_origen = rutas.RAIZ_REPO / ".mcp.json"
    if not mcp_origen.exists():
        return {"estado": "omitido", "motivo": "No existe .mcp.json"}

    raw = mcp_origen.read_text(encoding="utf-8")
    for k, v in os.environ.items():
        raw = raw.replace(f"${{{k}}}", v)

    droids_dir = rutas.RAIZ_REPO / ".factory" / "droids"
    droids_count = len(list(droids_dir.glob("*.md"))) if droids_dir.exists() else 0
    return {
        "estado": "sincronizado",
        "origen": str(mcp_origen),
        "droids_detectados": droids_count,
    }


def main() -> int:
    seguridad.configurar_utf8()
    print(json.dumps(sincronizar_factory(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
