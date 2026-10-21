# -*- coding: utf-8 -*-
"""
Auditor normativo de documentos Word (.docx) en modo solo lectura contra APA 7 y UNAJMA (Squad E).
Verifica márgenes (3.5 / 2.5 cm -> 1985 / 1418 dxa), Times New Roman 12 pt,
tablas de 3 líneas horizontales sin verticales (<w:tblpPr> prohibido),
encabezados repetibles (<w:tblHeader/>), filas indivisibles (<w:cantSplit/>),
sangría francesa 1.27 cm (720 dxa) y fórmulas nativas OMML (<m:oMath>).
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad
from scripts.utilidades.docx_quirurgico import auditar_docx_openxml


def main() -> int:
    seguridad.configurar_utf8()
    parser = argparse.ArgumentParser(description="Auditor APA 7 / UNAJMA sobre archivos .docx en modo solo lectura")
    parser.add_argument("comando", nargs="?", default="auditar", help="Comando (auditar)")
    parser.add_argument("ruta_docx", nargs="?", help="Ruta del archivo .docx a auditar")
    parser.add_argument("--solo", default="margenes,numeracion,tablas,figuras,referencias", help=" Secciones a auditar")
    parser.add_argument("--md", action="store_true", help="Emitir reporte en formato Markdown")
    parser.add_argument("--json", action="store_true", help="Emitir reporte en formato JSON")
    args = parser.parse_args()

    objetivo = Path(args.ruta_docx) if args.ruta_docx else (rutas.SALIDAS_DOCUMENTOS / "informe_final_v02.docx")
    reporte = auditar_docx_openxml(objetivo)

    if args.md and not args.json:
        print(f"# Auditoría Normativa APA 7 / UNAJMA — `{objetivo.name}`\n")
        print(f"- **Existe:** `{reporte.get('existe')}`")
        print(f"- **SHA-256:** `{reporte.get('sha256', 'N/A')}`")
        print(f"- **Márgenes UNAJMA (1985/1418 dxa):** `{'OK' if reporte.get('margenes_unajma_ok') else 'OBSERVADO'}`")
        print(f"- **Tablas Totales / Sin Flotación:** `{reporte.get('tablas_total', 0)}` (`{reporte.get('tablas_flotantes', 0)}` flotantes)")
        print(f"- **Referencias con Sangría Francesa (720 dxa):** `{reporte.get('referencias_sangria_francesa', 0)}`")
        print(f"- **Fórmulas Matemáticas Nativas OMML:** `{reporte.get('formulas_omml', 0)}`")
        print(f"- **Dictamen Global:** `{'APROBADO' if reporte.get('cumple_apa7') else 'CON HALLAZGOS'}`")
    else:
        print(json.dumps(reporte, indent=2, ensure_ascii=False))

    return 0 if reporte.get("cumple_apa7", False) else 1


if __name__ == "__main__":
    sys.exit(main())
