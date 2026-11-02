import sys, json
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

path = r"C:\MisInvestigaciones\tesis\sivac\salidas\documentos\informe_final_v04.docx"
out  = r"C:\MisInvestigaciones\tesis\sivac\salidas\reportes_maquetacion\auditoria_v04\_structure.json"
doc = Document(path)
body = doc.element.body

items = []
p_idx = 0
t_idx = 0
for child in body.iterchildren():
    if child.tag == qn('w:p'):
        p = Paragraph(child, doc)
        items.append({"kind":"p","idx":p_idx,"style":p.style.name if p.style is not None else "", "text":p.text})
        p_idx += 1
    elif child.tag == qn('w:tbl'):
        t = Table(child, doc)
        items.append({"kind":"t","idx":t_idx,"rows":len(t.rows),"cols":len(t.columns)})
        t_idx += 1

with open(out,"w",encoding="utf-8") as f:
    json.dump({"paras":p_idx,"tables":t_idx,"items":items}, f, ensure_ascii=False)
print("paras",p_idx,"tables",t_idx)
