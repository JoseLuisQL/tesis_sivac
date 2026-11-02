import json, io, sys
from docx import Document
from docx.oxml.ns import qn
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
path = r"C:\MisInvestigaciones\tesis\sivac\salidas\documentos\informe_final_v04.docx"
doc = Document(path)
out=[]
# sections
for si,s in enumerate(doc.sections):
    out.append({"sec":si,"orient":s.orientation,"pw":s.page_width.twips if s.page_width else None,
                "ph":s.page_height.twips if s.page_height else None,
                "l":s.left_margin.twips,"r":s.right_margin.twips,"t":s.top_margin.twips,"b":s.bottom_margin.twips})
print("SECTIONS")
for x in out: print(x)

tbls = doc.tables
for i,t in enumerate(tbls):
    tblPr = t._tbl.tblPr
    w = tblPr.find(qn('w:tblW'))
    tblW = w.get(qn('w:w')) if w is not None else None
    grid = t._tbl.find(qn('w:tblGrid'))
    cols = [int(g.get(qn('w:w'))) for g in grid.findall(qn('w:gridCol'))] if grid is not None else []
    layout = tblPr.find(qn('w:tblLayout'))
    style = t.style.name if t.style is not None else ''
    # first row cell widths
    print(f"T{i:02d} rows={len(t.rows)} cols={len(t.columns)} grid_sum={sum(cols)} min={min(cols) if cols else 0} max={max(cols) if cols else 0} tblW={tblW} layout={layout.get(qn('w:type')) if layout is not None else None} style={style} cols={cols}")
