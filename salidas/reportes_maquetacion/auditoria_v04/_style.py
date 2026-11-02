import io, sys, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Twips
DOCX = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.docx"
doc = Document(DOCX)
body = doc.element.body
paras = [p for p in body.iterchildren() if p.tag == qn('w:p')]
print('body paragraphs:', len(paras))
fonts=collections.Counter(); sizes=collections.Counter()
line=collections.Counter(); ind=collections.Counter(); jc=collections.Counter()
keep=0
for p in paras:
    pPr = p.find(qn('w:pPr'))
    sp = pPr.find(qn('w:spacing')) if pPr is not None else None
    if sp is not None:
        line[sp.get(qn('w:line'))]+=1
    else:
        line['none']+=1
    indEl = pPr.find(qn('w:ind')) if pPr is not None else None
    if indEl is not None:
        ind[(indEl.get(qn('w:firstLine')), indEl.get(qn('w:left')), indEl.get(qn('w:hanging')))]+=1
    else: ind['none']+=1
    j = pPr.find(qn('w:jc')) if pPr is not None else None
    jc[j.get(qn('w:val')) if j is not None else 'none']+=1
    for r in p.iter(qn('w:r')):
        rPr = r.find(qn('w:rPr'))
        if rPr is None: fonts['inherit']+=1; sizes['inherit']+=1; continue
        f = rPr.find(qn('w:rFonts'))
        fonts[f.get(qn('w:ascii')) if f is not None else 'inherit']+=1
        s = rPr.find(qn('w:sz'))
        sizes[s.get(qn('w:val')) if s is not None else 'inherit']+=1
print('FONTS', fonts.most_common(10))
print('SIZES', sizes.most_common(10))
print('LINE', line.most_common(8))
print('IND top', ind.most_common(8))
print('JC', jc.most_common(6))
