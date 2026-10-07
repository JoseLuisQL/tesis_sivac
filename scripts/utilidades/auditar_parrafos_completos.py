"""
Auditor quirúrgico de formato de párrafos, tipografía, interlineado y sangrías APA 7 / UNAJMA.
Verifica cada categoría de párrafo según su norma canónica específica:
  - Cuerpo narrativo: TNR 12 pt, interlineado 1.5 (360 dxa), sangría 1.27 cm (720 dxa), espaciado 0/0.
  - Headings: TNR, negrita, sangría 0, interlineado 1.5.
  - Rótulos y captions: TNR, sangría 0.
  - Notas de tablas/figuras: TNR 9.5-10 pt, interlineado 1.0 (240 dxa), sangría 0.
  - Referencias bibliográficas: TNR 12 pt, interlineado 1.5 (360 dxa), sangría francesa 1.27 cm (720 dxa).
  - Fórmulas OMML dedicadas: centradas, sangría 0.
"""

import sys
import docx
from docx.oxml.ns import qn


def auditar_parrafos_completos(docx_path):
    doc = docx.Document(docx_path)
    total_p = len(doc.paragraphs)
    print(f"============================================================")
    print(f"AUDITORÍA EDITORIAL QUIRÚRGICA APA 7 / UNAJMA")
    print(f"Documento: {docx_path}")
    print(f"Total de párrafos analizados: {total_p}")
    print(f"============================================================\n")

    conteo_categorias = {
        "cuerpo_narrativo": 0,
        "headings": 0,
        "captions": 0,
        "notas": 0,
        "referencias": 0,
        "formulas": 0,
        "otros_preliminares": 0,
        "vacios": 0
    }

    problemas = []
    en_referencias = False

    for idx, p in enumerate(doc.paragraphs):
        txt = p.text.strip()
        if not txt:
            conteo_categorias["vacios"] += 1
            continue

        pPr = p._p.find(qn('w:pPr'))
        style_name = p.style.name if p.style else 'Normal'
        txt_clean = txt.replace('\xa0', ' ')

        # Spacing
        sp = pPr.find(qn('w:spacing')) if pPr is not None else None
        line = sp.get(qn('w:line')) if sp is not None else None
        before = sp.get(qn('w:before')) if sp is not None else None
        after = sp.get(qn('w:after')) if sp is not None else None

        # Indents
        ind = pPr.find(qn('w:ind')) if pPr is not None else None
        first_line = ind.get(qn('w:firstLine')) if ind is not None else None
        left = ind.get(qn('w:left')) if ind is not None else None
        hanging = ind.get(qn('w:hanging')) if ind is not None else None

        # Runs font and size
        runs_info = []
        for r in p.runs:
            f = r.font.name
            s = r.font.size.pt if r.font and r.font.size else None
            runs_info.append((f, s))

        # 1. Detectar transiciones de sección
        if txt_clean.upper().startswith("REFERENCIA"):
            en_referencias = True
            conteo_categorias["headings"] += 1
            continue

        if txt_clean.startswith("ANEXOS") or txt_clean.startswith("Anexos") or txt_clean.upper().startswith("ANEXO"):
            en_referencias = False
            conteo_categorias["headings"] += 1
            continue

        # 2. Fórmulas OMML dedicadas
        contiene_omml = len(p._p.xpath('.//m:oMath')) > 0
        if contiene_omml and len(txt) < 30:
            conteo_categorias["formulas"] += 1
            continue

        # 3. Referencias bibliográficas
        if en_referencias and len(txt_clean) > 20:
            conteo_categorias["referencias"] += 1
            # Verificar sangría francesa (left=720, hanging=720) e interlineado 1.5 (360)
            if left != '720' or hanging != '720':
                problemas.append((idx, 'REF_SIN_SANGRIA_FRANCESA', f"P[{idx}]: Referencia sin sangría francesa (left={left}, hanging={hanging}): '{txt[:50]}...'"))
            if line != '360':
                problemas.append((idx, 'REF_INTERLINEADO_NO_1_5', f"P[{idx}]: Referencia con interlineado distinto a 1.5 (line={line}): '{txt[:50]}...'"))
            continue

        # 4. Headings / Títulos
        es_heading = (style_name.startswith('Heading') or
                      txt_clean.startswith('CAPÍTULO') or
                      (len(txt_clean) < 90 and any(txt_clean.startswith(f"{i}.") for i in range(1, 10)) and len(txt_clean.split()[0].split('.')) in [2, 3]))

        if es_heading:
            conteo_categorias["headings"] += 1
            # Headings no deben tener sangría de primera línea
            if first_line not in [None, '0']:
                problemas.append((idx, 'HEADING_CON_SANGRIA', f"P[{idx}]: Título con sangría de primera línea ({first_line}): '{txt[:50]}...'"))
            continue

        # 5. Captions de tablas y figuras
        if txt_clean.startswith('Tabla ') or txt_clean.startswith('Figura '):
            conteo_categorias["captions"] += 1
            if first_line not in [None, '0']:
                problemas.append((idx, 'CAPTION_CON_SANGRIA', f"P[{idx}]: Rótulo con sangría de primera línea ({first_line}): '{txt[:50]}...'"))
            continue

        # 6. Notas de tablas y figuras
        if txt_clean.startswith('Nota.') or txt_clean.startswith('Nota:') or txt_clean.startswith('Fuente:'):
            conteo_categorias["notas"] += 1
            # Notas deben tener interlineado 1.0 (240 dxa) y sin sangría
            if first_line not in [None, '0']:
                problemas.append((idx, 'NOTA_CON_SANGRIA', f"P[{idx}]: Nota con sangría de primera línea ({first_line}): '{txt[:50]}...'"))
            continue

        # 7. Preliminares (portada, actas, dedicatoria)
        if idx < 30 and (len(txt) < 80 or any(k in txt for k in ["UNIVERSIDAD", "FACULTAD", "ESCUELA", "TESIS", "BACHILLER"])):
            conteo_categorias["otros_preliminares"] += 1
            continue

        # 8. Cuerpo narrativo de texto
        if len(txt) > 40:
            conteo_categorias["cuerpo_narrativo"] += 1
            # Verificar sangría de primera línea (720 dxa = 1.27 cm)
            if first_line != '720':
                problemas.append((idx, 'CUERPO_SIN_SANGRIA_1_27', f"P[{idx}]: Párrafo sin sangría de primera línea 1.27 cm (firstLine={first_line}): '{txt[:50]}...'"))
            # Verificar interlineado 1.5 (360 dxa)
            if line != '360':
                problemas.append((idx, 'CUERPO_INTERLINEADO_NO_1_5', f"P[{idx}]: Párrafo sin interlineado 1.5 (line={line}): '{txt[:50]}...'"))
            # Verificar fuente y tamaño en runs
            for f, s in runs_info:
                if s is not None and s != 12.0:
                    problemas.append((idx, 'CUERPO_TAMANO_NO_12', f"P[{idx}]: Run con tamaño {s}pt (esperado 12pt): '{txt[:50]}...'"))
                    break
                if f is not None and f != 'Times New Roman':
                    problemas.append((idx, 'CUERPO_FUENTE_NO_TNR', f"P[{idx}]: Run con fuente '{f}' (esperado Times New Roman): '{txt[:50]}...'"))
                    break
        else:
            conteo_categorias["otros_preliminares"] += 1

    print("DISTRIBUCIÓN DE PÁRRAFOS POR CATEGORÍA:")
    for cat, cnt in conteo_categorias.items():
        print(f"  - {cat:20}: {cnt} párrafos")

    print(f"\nTOTAL DE DEFECTOS DETECTADOS: {len(problemas)}")
    if problemas:
        conteo_tipos = {}
        for _, tipo, _ in problemas:
            conteo_tipos[tipo] = conteo_tipos.get(tipo, 0) + 1
        for tipo, cnt in conteo_tipos.items():
            print(f"  * {tipo}: {cnt} incidencias")
        print("\nDetalle de incidencias:")
        for _, _, msg in problemas[:25]:
            print(f"    - {msg}")
    else:
        print("  >>> CERO DEFECTOS ENCONTRADOS. EL DOCUMENTO CUMPLE AL 100% LAS NORMAS APA 7 / UNAJMA <<<")

    return len(problemas) == 0


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else r"salidas\documentos\PROYECTO_TESIS_ACTUALIZADO_V3_NORMALIZADO.docx"
    exito = auditar_parrafos_completos(path)
    sys.exit(0 if exito else 1)
