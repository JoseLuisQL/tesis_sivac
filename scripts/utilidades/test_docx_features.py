import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = docx.Document()
sec = doc.sections[0]
sec.page_width = Cm(21.0)
sec.page_height = Cm(29.7)
sec.left_margin = Cm(3.0)
sec.right_margin = Cm(2.54)
sec.top_margin = Cm(2.54)
sec.bottom_margin = Cm(2.54)

# Set page number in header
header = sec.header
p = header.paragraphs[0]
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
run = p.add_run()
run.font.name = 'Times New Roman'
run.font.size = Pt(10)
fld = OxmlElement('w:fldSimple')
fld.set(qn('w:instr'), 'PAGE')
run._r.append(fld)

# Test APA Table
tbl = doc.add_table(rows=3, cols=3)
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
tblPr = tbl._tbl.tblPr
tblBorders = parse_xml(
    r'<w:tblBorders %s>'
    r'  <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
    r'  <w:left w:val="none"/>'
    r'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
    r'  <w:right w:val="none"/>'
    r'  <w:insideH w:val="none"/>'
    r'  <w:insideV w:val="none"/>'
    r'</w:tblBorders>' % nsdecls('w')
)
tblPr.append(tblBorders)

# Header row bottom border
header_tr = tbl.rows[0]._tr
trPr = header_tr.get_or_add_trPr()
trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))
for cell in tbl.rows[0].cells:
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        r'<w:tcBorders %s>'
        r'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        r'</w:tcBorders>' % nsdecls('w')
    )
    tcPr.append(tcBorders)

doc.save('salidas/test_apa7.docx')
print('Test docx saved successfully!')
