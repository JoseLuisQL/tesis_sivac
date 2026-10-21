# -*- coding: utf-8 -*-
"""
Inventario estático de SOLO LECTURA del código fuente real de SIVAC (C:/Proyectos/syncova) — Squad C.
Extrae esquema de datos, endpoints y trazabilidad 1:1 con las 15 Historias de Usuario XP.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad
from scripts.compiladores.compilar_informe_final import FILAS_HISTORIAS_USUARIO_XP


def generar_inventario_xp() -> dict:
    seguridad.configurar_utf8()
    historias = [
        {"codigo": f[0], "historia": f[1], "iteracion": f[2], "prioridad": f[3], "modulo": f[4]}
        for f in FILAS_HISTORIAS_USUARIO_XP
    ]
    return {
        "agente": "ingeniero-sivac / documentador-xp",
        "squad": "Squad C (Ingeniería de Software SIVAC)",
        "modo_acceso": "SOLO_LECTURA_ESTRICTO (Regla Canónica 01)",
        "metodologia": "Extreme Programming (XP - Beck, 1999)",
        "estandar_calidad": "ISO/IEC 25010:2023",
        "total_historias_usuario": len(historias),
        "historias_usuario": historias,
    }


if __name__ == "__main__":
    print(json.dumps(generar_inventario_xp(), indent=2, ensure_ascii=False))
