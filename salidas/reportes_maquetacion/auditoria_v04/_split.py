import io, sys, re, unicodedata, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
import pymupdf
DOCX = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.docx"
PDF  = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.pdf"
doc = Document(DOCX)
pdf = pymupdf.open(PDF)
def norm(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c)) if False else s
    s = re.sub(r'[^a-z0-9]', '', s.lower())
    return s
pnorm = [norm(pdf[i].get_text()) for i in range(pdf.page_count)]
# table pages corrected from manual/visual mapping
tblmap = json.load(open('_tblmap.json', encoding='utf-8'))
manual = {36:118,37:120,38:122,39:124,40:126,41:127,42:129,43:130,22:78,23:78,24:79,48:149,57:157,58:158}
paras = doc.paragraphs
# paragraph index -> text
plist = [p.text.strip() for p in paras]
# table -> preceding paragraph idx via body order
from docx.oxml.ns import qn
order=[]; pi=ti=0
for ch in doc.element.body.iterchildren():
    tag=ch.tag.split('}')[-1]
    if tag=='p': order.append(('p',pi)); pi+=1
    elif tag=='tbl': order.append(('t',ti)); ti+=1
prev={}
last=None
for kind,idx in order:
    if kind=='p':
        if plist[idx]: last=idx
    else: prev[idx]=last
for k in range(len(doc.tables)):
    tp = manual.get(k) or tblmap[k]['page']
    if not tp: continue
    capidx = prev.get(k)
    if capidx is None: continue
    # candidate caption + following title
    cands=[plist[capidx]]
    if capidx+1 < len(plist): cands.append(plist[capidx+1])
    key=None
    for c in cands:
        n=norm(c)
        if len(n)>25: key=n; break
    if not key: continue
    pcap=None
    for p in range(max(0,tp-3), min(len(pnorm), tp+1)):
        if key in pnorm[p]:
            pcap=p+1
    if pcap and pcap!=tp:
        print(f"T{k:02d} tabla p{tp} caption p{pcap} :: {plist[capidx][:70]}")
print()
print("=== LAST BLOCK PER PAGE (possible orphan heading) ===")
for p in range(pdf.page_count):
    blocks=[b for b in pdf[p].get_text('blocks') if b[4].strip()]
    if not blocks: continue
    blocks=[b for b in blocks if b[1] > 55 and b[3] < pdf[p].rect.height-40]
    if not blocks: continue
    last=max(blocks, key=lambda b:b[3])
    txt=last[4].strip().replace('\n',' ')
    if len(txt) < 90 and not txt.endswith(('.', ':', ';')):
        print(f"p{p+1:03d} y1={last[3]:.0f}/{pdf[p].rect.height:.0f} :: {txt[:88]}")
