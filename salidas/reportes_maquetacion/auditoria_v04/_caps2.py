import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
DOCX = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.docx"
doc = Document(DOCX)
paras=[p for p in doc.element.body.iterchildren() if p.tag==qn('w:p')]
def txt(p): return ''.join(t.text or '' for t in p.iter(qn('w:t'))).strip()
order=[];pi=ti=0
for ch in doc.element.body.iterchildren():
    tag=ch.tag.split('}')[-1]
    if tag=='p': order.append(('p',pi)); pi+=1
    elif tag=='tbl': order.append(('t',ti)); ti+=1
prev=[]
for kind,idx in order:
    if kind=='t': prev.append((idx,list(prevp)))
    elif txt(paras[idx]): prevp=(prevp+[idx])[-2:] if 'prevp' in dir() else [idx]
# simpler recompute
prevp=[]; out={}
for kind,idx in order:
    if kind=='t': out[idx]=list(prevp)
    else:
        if txt(paras[idx]): prevp=(prevp+[idx])[-2:]
for k in sorted(out):
    ids=out[k]
    labels=[(i, txt(paras[i])[:70]) for i in ids]
    print(f"T{k:02d} :: " + " || ".join(f"P{i:04d} {t!r}" for i,t in labels))
