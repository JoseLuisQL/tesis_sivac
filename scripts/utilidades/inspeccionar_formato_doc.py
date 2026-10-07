import os
import sys
from pathlib import Path
import docx
from docx.oxml.ns import qn

def inspect_doc(path_str, name):
    print(f"\n=======================================================")
    print(f"=== INSPECCIÓN DE FORMATO: {name} ===")
    print(f"=======================================================")
    if not os.path.exists(path_str):
        print(f"ERROR: No existe {path_str}")
        return
    doc = docx.Document(path_str)

    # 1. Secciones y márgenes
    print("--- SECCIONES Y MÁRGENES ---")
    for i, s in enumerate(doc.sections):
        top = s.top_margin.cm if s.top_margin else 0
        bottom = s.bottom_margin.cm if s.bottom_margin else 0
        left = s.left_margin.cm if s.left_margin else 0
        right = s.right_margin.cm if s.right_margin else 0
        print(f"Sec {i}: Superior={top:.2f}cm, Inferior={bottom:.2f}cm, Izquierdo={left:.2f}cm, Derecho={right:.2f}cm, Orientación={s.orientation}")

    # 2. Párrafos normales de cuerpo
    print("\n--- PÁRRAFOS DE CUERPO (MUESTRA EXTENSA) ---")
    body_samples = 0
    heading_samples = 0
    injected_samples = 0

    for idx, p in enumerate(doc.paragraphs):
        txt = p.text.strip()
        if not txt:
            continue
        pPr = p._p.find(qn('w:pPr'))
        style_name = p.style.name if p.style else 'None'

        # Spacing
        sp = pPr.find(qn('w:spacing')) if pPr is not None else None
        line = sp.get(qn('w:line')) if sp is not None else None
        line_rule = sp.get(qn('w:lineRule')) if sp is not None else None
        before = sp.get(qn('w:before')) if sp is not None else None
        after = sp.get(qn('w:after')) if sp is not None else None

        # Indentation
        ind = pPr.find(qn('w:ind')) if pPr is not None else None
        first_line = ind.get(qn('w:firstLine')) if ind is not None else None
        left = ind.get(qn('w:left')) if ind is not None else None
        hanging = ind.get(qn('w:hanging')) if ind is not None else None

        # Alignment
        jc = pPr.find(qn('w:jc')) if pPr is not None else None
        val_jc = jc.get(qn('w:val')) if jc is not None else None

        # Runs font/size
        runs = p.runs
        font_name = runs[0].font.name if runs and runs[0].font else None
        font_sz = runs[0].font.size.pt if runs and runs[0].font and runs[0].font.size else None

        if "Aspectos Éticos" in txt or "Declaración de Helsinki" in txt or "Hurlbert" in txt or "CPE" in txt:
            print(f"INJECTED P[{idx}] ({style_name}): text='{txt[:45]}...'")
            print(f"   -> font={font_name} {font_sz}pt | line={line} ({line_rule}), bef={before}, aft={after} | ind_fl={first_line}, left={left} | jc={val_jc}")
        elif len(txt) > 100 and body_samples < 8:
            body_samples += 1
            print(f"BODY P[{idx}] ({style_name}): text='{txt[:45]}...'")
            print(f"   -> font={font_name} {font_sz}pt | line={line} ({line_rule}), bef={before}, aft={after} | ind_fl={first_line}, left={left} | jc={val_jc}")
        elif (style_name.startswith('Heading') or txt.startswith('CAPÍTULO') or txt.startswith('1.') or txt.startswith('4.')) and heading_samples < 6:
            heading_samples += 1
            print(f"HEADING P[{idx}] ({style_name}): text='{txt[:45]}...'")
            print(f"   -> font={font_name} {font_sz}pt | line={line} ({line_rule}), bef={before}, aft={after} | ind_fl={first_line} | jc={val_jc}")

# Inspeccionar base y V3
inspect_doc(r'referencias\proyecto_base\PROYECTO_TESIS.docx', 'PROYECTO_TESIS BASE')
inspect_doc(r'salidas\documentos\PROYECTO_TESIS_ACTUALIZADO_V3.docx', 'PROYECTO_TESIS V3 ACTUAL')
