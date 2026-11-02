import io, sys, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import pymupdf
PDF = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.pdf"
pdf = pymupdf.open(PDF)
print("=== p2 ==="); print(pdf[1].get_text())
print("=== p3 ==="); print(pdf[2].get_text())
st = json.load(open('_structure.json', encoding='utf-8'))
paras=[it for it in st['items'] if it['kind']=='p']
print("=== FIGURE CAPTIONS AND NOTE PRESENCE ===")
for i,p in enumerate(paras):
    t=(p['text'] or '').strip()
    if re.match(r'^Figura\s+[A-Z0-9]', t):
        nxt=[ (paras[j]['text'] or '').strip() for j in range(i+1, min(i+4,len(paras))) ]
        has = any(x.startswith('Nota') for x in nxt)
        print(f"P{p['idx']:04d} nota={has} :: {t[:80]} || next={nxt[0][:60]!r}")
