import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import pymupdf
PDF = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.pdf"
pdf = pymupdf.open(PDF)
def report(pno):
    pg = pdf[pno-1]
    W,H = pg.rect.width, pg.rect.height
    xs0=[]; xs1=[]
    for d in pg.get_drawings():
        r = d['rect']
        if r.width < 1 and r.height < 1: continue
        if r.width > 30 or r.height > 30:
            xs0.append(r.x0); xs1.append(r.x1)
    print(f"p{pno:03d} W={W:.2f} H={H:.2f} right_limit={W-72:.2f} left_limit=85.05  drawings x0min={min(xs0) if xs0 else None} x1max={max(xs1) if xs1 else None}")
for p in [46,47,58,59,104,105,108,109,111,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,136,139,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158]:
    report(p)
print()
print("images / drawings counts p143:", len(pdf[142].get_drawings()), "p153:", len(pdf[152].get_drawings()))
