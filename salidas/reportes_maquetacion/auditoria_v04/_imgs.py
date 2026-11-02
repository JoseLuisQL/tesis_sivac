import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
DOCX = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.docx"
doc = Document(DOCX)
paras = [p for p in doc.element.body.iterchildren() if p.tag == qn('w:p')]
def txt(p): return ''.join(t.text or '' for t in p.iter(qn('w:t'))).strip()
def has_img(p): return p.find('.//'+qn('w:drawing')) is not None or p.find('.//'+qn('w:pict')) is not None
imgs=[]
for i,p in enumerate(paras):
    if has_img(p):
        nxt=''
        for j in range(i+1, min(i+5,len(paras))):
            t=txt(paras[j])
            if t: nxt=t; break
        imgs.append((i,nxt[:70]))
print('inline images:', len(imgs))
for i,n in imgs:
    print(f"  img at P{i:04d} -> next={n!r}")
caps=[(i,txt(p)) for i,p in enumerate(paras) if re.match(r'^Figura\s+[A-Z0-9]', txt(p))]
print('figure captions:', len(caps))
imgpara={i for i,_ in imgs}
for i,c in caps:
    near=any(abs(i-k)<=3 for k in imgpara)
    print(f"  cap P{i:04d} img_near={near} :: {c[:60]}")
