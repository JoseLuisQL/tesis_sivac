import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
DOCX = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.docx"
doc = Document(DOCX)
for name in ['Normal','Titulo 1','Heading 1','Caption','table of figures']:
    try:
        st = doc.styles[name]
    except KeyError:
        continue
    pPr = st.element.find(qn('w:pPr'))
    info = {}
    if pPr is not None:
        for tag in ['w:spacing','w:ind','w:jc','w:keepNext']:
            el = pPr.find(qn(tag))
            if el is not None: info[tag] = dict(el.attrib)
    print(name, '->', info)
print()
for sec in doc.sections:
    print('pgMar', {k:getattr(sec,k) for k in ['left_margin','right_margin','top_margin','bottom_margin']}, 'orient', sec.orientation, 'pw', sec.page_width, 'ph', sec.page_height)
