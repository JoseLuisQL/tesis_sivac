import io, sys, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
DOCX = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.docx"
doc = Document(DOCX)
paras = [p for p in doc.element.body.iterchildren() if p.tag == qn('w:p')]
def txt(p): return ''.join(t.text or '' for t in p.iter(qn('w:t'))).strip()
ref = re.compile(r'^[A-ZÁÉÍÓÚÑ][^.]{0,80}\(\d{4}[a-z]?\)\.')
stats = collections.Counter()
examples = collections.defaultdict(list)
for i,p in enumerate(paras):
    t = txt(p)
    if len(t) < 250: continue
    if ref.match(t): continue
    pPr = p.find(qn('w:pPr'))
    ind = pPr.find(qn('w:ind')) if pPr is not None else None
    sp = pPr.find(qn('w:spacing')) if pPr is not None else None
    fl = ind.get(qn('w:firstLine')) if ind is not None else None
    ln = sp.get(qn('w:line')) if sp is not None else None
    key = (fl, ln)
    stats[key]+=1
    if len(examples[key])<3: examples[key].append((i,t[:60]))
for k,v in stats.most_common(12):
    print(k, v, examples[k][:2])
print('total prose analysed', sum(stats.values()))
