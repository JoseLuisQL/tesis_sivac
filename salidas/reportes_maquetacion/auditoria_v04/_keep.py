import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
DOCX = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.docx"
doc = Document(DOCX)
paras=[p for p in doc.element.body.iterchildren() if p.tag==qn('w:p')]
def txt(p): return ''.join(t.text or '' for t in p.iter(qn('w:t'))).strip()
cnt=0; withk=0
for i,p in enumerate(paras):
    t=txt(p)
    if re.match(r'^(Tabla|Figura)\s+(A?\d|[IVX])', t):
        cnt+=1
        pPr=p.find(qn('w:pPr'))
        k = pPr is not None and pPr.find(qn('w:keepNext')) is not None
        withk += 1 if k else 0
        if not k and i<700:
            print(f"P{i:04d} keepNext=NO :: {t[:60]}")
print('total caption-like', cnt, 'with keepNext', withk)
