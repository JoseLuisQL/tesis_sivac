import json, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
import fitz
DOCX = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.docx"
PDF  = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.pdf"
doc = Document(DOCX)
body = doc.element.body
sdts = body.findall(qn('w:sdt'))
print('SDT count:', len(sdts))
for i,s in enumerate(sdts):
    ps = s.findall('.//'+qn('w:p'))
    print(f'  sdt{i}: paras={len(ps)} first={("".join(t.text or "" for t in ps[0].iter(qn("w:t")))[:80]) if ps else ""!r}')
    instr = s.findall('.//'+qn('w:instrText'))
    print('    instr:', [x.text for x in instr][:3])
print()
print('=== P619 full ===')
for p in doc.paragraphs:
    if p.text.startswith('ADVERTENCIA METODOL'):
        print(p.text)
        break
print()
pdf = fitz.open(PDF)
print('=== TOC p6 ===')
print(pdf[5].get_text())
print('=== TOC p7 ===')
print(pdf[6].get_text())
print('=== p8 ===')
print(pdf[7].get_text())
print('=== p9 ===')
print(pdf[8].get_text())
