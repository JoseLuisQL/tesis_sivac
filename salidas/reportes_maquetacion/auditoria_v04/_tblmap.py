import json, io, sys, re, unicodedata
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
import fitz

DOCX = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.docx"
PDF  = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.pdf"
doc = Document(DOCX)
body = doc.element.body
items=[]
ti=0; pi=0
for ch in body.iterchildren():
    tag = ch.tag.split('}')[-1]
    if tag == 'p': items.append(('p', pi)); pi+=1
    elif tag == 'tbl': items.append(('t', ti)); ti+=1

def norm(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]', '', s.lower())

pdf = fitz.open(PDF)
pages_norm = [norm(pdf[i].get_text()) for i in range(pdf.page_count)]

tables = doc.tables
paras = doc.paragraphs
# map table index -> preceding caption paragraph text
caps = {}
lastp = ''
for kind, idx in items:
    if kind=='p':
        t = paras[idx].text.strip()
        if t: lastp = t
    else:
        caps[idx] = lastp

rows=[]
start=0
for k,tb in enumerate(tables):
    try:
        hdr = [c.text.strip() for c in tb.rows[0].cells]
    except Exception:
        hdr = []
    keys=[]
    for h in hdr:
        n = norm(h)
        if len(n)>=3: keys.append(n[:18])
    uniq=[]
    for x in keys:
        if x not in uniq: uniq.append(x)
    key1 = uniq[0] if uniq else ''
    key2 = uniq[-1] if len(uniq)>1 else ''
    found=None
    if key1:
        for p in range(start, len(pages_norm)):
            if key1 in pages_norm[p] and (not key2 or key2 in pages_norm[p]):
                found=p+1; break
    if found: start=found
    rows.append({'t':k,'page':found,'cols':len(tb.columns),'rows':len(tb.rows),'cap':caps.get(k,'')[:85],'keys':uniq[:4]})
for r in rows:
    print(f"T{r['t']:02d} p{str(r['page']):>3} {r['rows']}x{r['cols']:<2} | {r['cap']} | {r['keys']}")
json.dump(rows, open('_tblmap.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
