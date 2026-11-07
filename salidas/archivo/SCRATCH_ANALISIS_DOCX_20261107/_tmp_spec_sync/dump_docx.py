import sys, json
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

def iter_block_items(parent):
    from docx.document import Document as _Doc
    if isinstance(parent, _Doc):
        parent_elm = parent.element.body
    else:
        parent_elm = parent._tc
    for child in parent_elm.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, parent)
        elif child.tag == qn('w:tbl'):
            yield Table(child, parent)

def dump(path):
    doc = Document(path)
    print("="*100)
    print("FILE:", path)
    print("SECTIONS:", len(doc.sections))
    for i, s in enumerate(doc.sections):
        print(f"  sec{i}: page={s.page_width}x{s.page_height} margins L={s.left_margin} R={s.right_margin} T={s.top_margin} B={s.bottom_margin} hdr={s.header_distance}")
    idx=0
    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            t = block.text
            print(f"[P{idx}] style={block.style.name!r} :: {t!r}")
        else:
            print(f"[T{idx}] rows={len(block.rows)} cols={len(block.columns)}")
            # grid widths
            tbl = block._tbl
            grid = tbl.find(qn('w:tblGrid'))
            widths = []
            if grid is not None:
                for gc in grid.findall(qn('w:gridCol')):
                    widths.append(gc.get(qn('w:w')))
            print("    gridWidths:", widths)
            for ri,row in enumerate(block.rows):
                cells = row.cells
                vals=[]
                for c in cells:
                    vals.append(c.text.replace("\n"," | "))
                # dedupe merged repeats? keep raw
                trPr = row._tr.find(qn('w:trPr'))
                h = None; cant=False; hdr=False
                if trPr is not None:
                    th = trPr.find(qn('w:trHeight'))
                    if th is not None: h = (th.get(qn('w:val')), th.get(qn('w:hRule')))
                    if trPr.find(qn('w:cantSplit')) is not None: cant=True
                    if trPr.find(qn('w:tblHeader')) is not None: hdr=True
                print(f"    R{ri} h={h} cant={cant} hdr={hdr} :: {vals}")
        idx+=1

for p in sys.argv[1:]:
    dump(p)
