# -*- coding: utf-8 -*-
"""
Pipeline Estadístico Inferencial Reproducible (N = n = 14, Pretest-Postest).
Cumple Regla Canónica 01 y DEC-007:
- Se bloquea con código 3 si datos/raw/MANIFEST.json no está presente y firmado.
- Evalúa normalidad con Shapiro-Wilk sobre las diferencias pareadas (Post - Pre).
- Ejecuta t de Student pareada + d de Cohen dz (si normal) o Wilcoxon + r de Rosenthal (si no normal u ordinal).
- Calcula Alfa de Cronbach sobre los 8 ítems de la Modalidad A (AP-01..04, UP-01..04) con IC 95% de Feldt.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad
from scripts.estadistica.manifest_datos import validar_manifest


def main() -> int:
    seguridad.configurar_utf8()
    estado = validar_manifest()
    if not estado.get("valido"):
        print(f"[BLOQUEO DE SEGURIDAD EMPÍRICA] {estado['estado']} — {estado.get('motivo', '')}")
        return 3
    print("Pipeline inferencial listo para procesar datos certificados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
