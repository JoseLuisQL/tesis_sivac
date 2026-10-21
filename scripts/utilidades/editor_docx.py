# -*- coding: utf-8 -*-
"""
Editor quirúrgico versionado de documentos .docx preservando sectPr, estilos, campos e imágenes (Squad E).
Exige destino != origen en salidas/documentos/informe_final_vNN.docx y genera log .cambios.json.
"""
import argparse
import json
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad


def siguiente_version_informe() -> Path:
    rutas.SALIDAS_DOCUMENTOS.mkdir(parents=True, exist_ok=True)
    existentes = sorted(rutas.SALIDAS_DOCUMENTOS.glob("informe_final_v*.docx"))
    if not existentes:
        return rutas.SALIDAS_DOCUMENTOS / "informe_final_v01.docx"
    ultimo = existentes[-1].stem.replace("informe_final_v", "")
    num = int(ultimo) + 1 if ultimo.isdigit() else len(existentes) + 1
    return rutas.SALIDAS_DOCUMENTOS / f"informe_final_v{num:02d}.docx"


def reemplazar_en_docx(
    origen: Path,
    destino: Path,
    texto_buscar: str,
    texto_nuevo: str,
    dry_run: bool = False,
) -> dict:
    seguridad.asegurar_no_sobrescribe(origen, destino)
    with zipfile.ZipFile(origen, "r") as zf_in:
        doc_xml = zf_in.read("word/document.xml").decode("utf-8")
        ocurrencias = doc_xml.count(texto_buscar)
        if not dry_run:
            destino.parent.mkdir(parents=True, exist_ok=True)
            nuevo_xml = doc_xml.replace(texto_buscar, texto_nuevo)
            with zipfile.ZipFile(destino, "w", compression=zipfile.ZIP_DEFLATED) as zf_out:
                for item in zf_in.infolist():
                    if item.filename == "word/document.xml":
                        zf_out.writestr(item, nuevo_xml.encode("utf-8"))
                    else:
                        zf_out.writestr(item, zf_in.read(item.filename))

    registro = {
        "comando": "reemplazar",
        "origen": str(origen),
        "sha256_origen": seguridad.sha256_archivo(origen),
        "destino": str(destino),
        "sha256_destino": seguridad.sha256_archivo(destino) if (not dry_run and destino.exists()) else None,
        "ocurrencias_reemplazadas": ocurrencias,
        "dry_run": dry_run,
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
    }
    if not dry_run:
        Path(str(destino) + ".cambios.json").write_text(
            json.dumps(registro, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    return registro


def main() -> int:
    seguridad.configurar_utf8()
    parser = argparse.ArgumentParser(description="Editor quirúrgico versionado de DOCX (Squad E)")
    parser.add_argument("comando", nargs="?", default="siguiente-version")
    parser.add_argument("origen", nargs="?")
    parser.add_argument("destino", nargs="?")
    parser.add_argument("buscar", nargs="?", default="")
    parser.add_argument("nuevo", nargs="?", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.comando == "siguiente-version" or not args.origen:
        print(json.dumps({"siguiente_version": str(siguiente_version_informe())}, ensure_ascii=False))
        return 0

    if args.comando == "reemplazar" and args.origen and args.destino:
        res = reemplazar_en_docx(Path(args.origen), Path(args.destino), args.buscar, args.nuevo, args.dry_run)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0

    shutil.copy2(args.origen, seguridad.asegurar_no_sobrescribe(args.origen, args.destino))
    return 0


if __name__ == "__main__":
    sys.exit(main())
