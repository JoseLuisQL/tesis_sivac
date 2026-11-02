import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
DOCX = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.docx"
doc = Document(DOCX)
for k in [46,47,48,50,51,52,53,55,56,57,58]:
    tb = doc.tables[k]
    print(f"===== T{k:02d} {len(tb.rows)}x{len(tb.columns)} =====")
    for ri,row in enumerate(tb.rows[:6]):
        cells=[]
        seen=set()
        for c in row.cells:
            if id(c._tc) in seen: continue
            seen.add(id(c._tc))
            cells.append(c.text.replace('\n',' / ')[:110])
        print(f"  r{ri}: " + " | ".join(cells))
    print()
