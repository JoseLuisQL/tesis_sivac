# -*- coding: utf-8 -*-
"""
Validador del manifiesto criptográfico de datos de campo (datos/raw/MANIFEST.json).
Garantiza la Regla Canónica 01: Cero invención o simulación de datos empíricos.
Sin MANIFEST válido firmado por el tesista -> BLOQUEADO (exit code 3).
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad

DECLARACION_EXIGIDA = (
    "Declaro que estos datos provienen de mediciones reales de campo y no han sido simulados."
)


def validar_manifest(ruta_manifest: Path = rutas.DATOS_RAW / "MANIFEST.json") -> dict:
    if not ruta_manifest.exists():
        return {
            "valido": False,
            "estado": "BLOQUEADO: esperando datos de campo",
            "motivo": f"No existe {ruta_manifest}",
            "codigo_salida": 3,
        }
    try:
        data = json.loads(ruta_manifest.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "valido": False,
            "estado": "BLOQUEADO: esperando datos de campo",
            "motivo": f"JSON inválido: {exc}",
            "codigo_salida": 3,
        }

    errores = []
    if data.get("origen") != "campo":
        errores.append("El campo 'origen' debe ser exactamente 'campo'.")
    if data.get("n_esperado") != rutas.N_CENSAL:
        errores.append(f"El campo 'n_esperado' debe ser {rutas.N_CENSAL}.")
    if data.get("declaracion_tesista") != DECLARACION_EXIGIDA:
        errores.append("La declaración jurada del tesista no coincide con el texto literal exigido.")
    if not data.get("firmado_por") or not data.get("fecha_firma"):
        errores.append("Faltan 'firmado_por' o 'fecha_firma'.")

    archivos = data.get("archivos", [])
    if not isinstance(archivos, list) or len(archivos) < 2:
        errores.append("Se requieren los archivos pretest y postest en 'archivos'.")
    else:
        for arch in archivos:
            nombre = arch.get("nombre", "")
            sha_esperado = arch.get("sha256", "")
            ruta_csv = rutas.DATOS_RAW / nombre
            if not ruta_csv.exists():
                errores.append(f"Archivo de campo no encontrado: {ruta_csv}")
            elif not sha_esperado or seguridad.sha256_archivo(ruta_csv) != sha_esperado:
                errores.append(f"Suma SHA-256 no coincide para {nombre}.")

    if errores:
        return {
            "valido": False,
            "estado": "BLOQUEADO: esperando datos de campo",
            "errores": errores,
            "codigo_salida": 3,
        }

    return {
        "valido": True,
        "estado": "DESBLOQUEADO: datos de campo certificados",
        "responsable": data.get("responsable"),
        "codigo_salida": 0,
    }


def main() -> int:
    seguridad.configurar_utf8()
    parser = argparse.ArgumentParser(description="Validador de MANIFEST.json para datos reales de campo")
    parser.add_argument("comando", choices=["validar", "plantilla"], nargs="?", default="validar")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    res = validar_manifest()
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"[SIVAC-THESIS-LAB] Estado de datos de campo: {res['estado']}")
    return res["codigo_salida"]


if __name__ == "__main__":
    sys.exit(main())
