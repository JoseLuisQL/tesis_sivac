import os
import zipfile
import xml.etree.ElementTree as ET
import docx
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import win32com.client

test_docx = os.path.abspath("salidas/documentos/test_toc.docx")
doc = docx.Document()

# 1. SDT TOC
p_dummy = doc.add_paragraph()
sdt_xml = f"""<w:sdt xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:sdtPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
    <w:docPartObj>
      <w:docPartGallery w:val="Table of Contents"/>
      <w:docPartUnique/>
    </w:docPartObj>
  </w:sdtPr>
  <w:sdtContent>
    <w:p>
      <w:pPr>
        <w:pStyle w:val="TDC1"/>
        <w:tabs>
          <w:tab w:val="right" w:leader="dot" w:pos="8921"/>
        </w:tabs>
      </w:pPr>
      <w:r><w:fldChar w:fldCharType="begin"/></w:r>
      <w:r><w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText></w:r>
      <w:r><w:fldChar w:fldCharType="separate"/></w:r>
      <w:r><w:t>Actualizando tabla de contenido...</w:t></w:r>
      <w:r><w:fldChar w:fldCharType="end"/></w:r>
    </w:p>
  </w:sdtContent>
</w:sdt>"""
sdt_elem = parse_xml(sdt_xml)
p_dummy._p.addprevious(sdt_elem)
doc._body._body.remove(p_dummy._p)

# 2. Table of Tables (Lista de Tablas)
p_tablas = doc.add_paragraph()
p_tablas._p.append(parse_xml(r'''<w:r %s><w:fldChar w:fldCharType="begin"/></w:r>''' % nsdecls('w')))
p_tablas._p.append(parse_xml(r'''<w:r %s><w:instrText xml:space="preserve"> TOC \h \z \c "Tabla" </w:instrText></w:r>''' % nsdecls('w')))
p_tablas._p.append(parse_xml(r'''<w:r %s><w:fldChar w:fldCharType="separate"/></w:r>''' % nsdecls('w')))
p_tablas._p.append(parse_xml(r'''<w:r %s><w:t>Actualizando lista de tablas...</w:t></w:r>''' % nsdecls('w')))
p_tablas._p.append(parse_xml(r'''<w:r %s><w:fldChar w:fldCharType="end"/></w:r>''' % nsdecls('w')))

# 3. Table of Figures (Lista de Figuras)
p_figuras = doc.add_paragraph()
p_figuras._p.append(parse_xml(r'''<w:r %s><w:fldChar w:fldCharType="begin"/></w:r>''' % nsdecls('w')))
p_figuras._p.append(parse_xml(r'''<w:r %s><w:instrText xml:space="preserve"> TOC \h \z \c "Figura" </w:instrText></w:r>''' % nsdecls('w')))
p_figuras._p.append(parse_xml(r'''<w:r %s><w:fldChar w:fldCharType="separate"/></w:r>''' % nsdecls('w')))
p_figuras._p.append(parse_xml(r'''<w:r %s><w:t>Actualizando lista de figuras...</w:t></w:r>''' % nsdecls('w')))
p_figuras._p.append(parse_xml(r'''<w:r %s><w:fldChar w:fldCharType="end"/></w:r>''' % nsdecls('w')))

# Page break
doc.add_page_break()

# Heading 1 with outlineLvl 0
p1 = doc.add_paragraph("CAPÍTULO I: INTRODUCCIÓN")
p1._p.get_or_add_pPr().append(parse_xml(r'<w:outlineLvl %s w:val="0"/>' % nsdecls('w')))

# Heading 2 with outlineLvl 1
p2 = doc.add_paragraph("1.1 Descripción de la realidad")
p2._p.get_or_add_pPr().append(parse_xml(r'<w:outlineLvl %s w:val="1"/>' % nsdecls('w')))

# Heading 3 with outlineLvl 2
p3 = doc.add_paragraph("1.1.1 Antecedentes del problema")
p3._p.get_or_add_pPr().append(parse_xml(r'<w:outlineLvl %s w:val="2"/>' % nsdecls('w')))

# Heading without outlineLvl
p4 = doc.add_paragraph("ÍNDICE DE CONTENIDO (NO DEBE SALIR)")

# Caption for Table 1
p_cap_tab = doc.add_paragraph()
p_cap_tab._p.append(parse_xml(r'''<w:r %s><w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t xml:space="preserve">Tabla </w:t></w:r>''' % nsdecls('w')))
p_cap_tab._p.append(parse_xml(r'''<w:r %s><w:fldChar w:fldCharType="begin"/></w:r>''' % nsdecls('w')))
p_cap_tab._p.append(parse_xml(r'''<w:r %s><w:instrText xml:space="preserve"> SEQ Tabla \* ARABIC </w:instrText></w:r>''' % nsdecls('w')))
p_cap_tab._p.append(parse_xml(r'''<w:r %s><w:fldChar w:fldCharType="separate"/></w:r>''' % nsdecls('w')))
p_cap_tab._p.append(parse_xml(r'''<w:r %s><w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t>1</w:t></w:r>''' % nsdecls('w')))
p_cap_tab._p.append(parse_xml(r'''<w:r %s><w:fldChar w:fldCharType="end"/></w:r>''' % nsdecls('w')))
p_cap_tab._p.append(parse_xml(r'''<w:r %s><w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t xml:space="preserve"> </w:t></w:r>''' % nsdecls('w')))
p_cap_tab._p.append(parse_xml(r'''<w:r %s><w:rPr><w:i/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t>Operacionalización de Variables</w:t></w:r>''' % nsdecls('w')))

# Caption for Figure 1
p_cap_fig = doc.add_paragraph()
p_cap_fig._p.append(parse_xml(r'''<w:r %s><w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t xml:space="preserve">Figura </w:t></w:r>''' % nsdecls('w')))
p_cap_fig._p.append(parse_xml(r'''<w:r %s><w:fldChar w:fldCharType="begin"/></w:r>''' % nsdecls('w')))
p_cap_fig._p.append(parse_xml(r'''<w:r %s><w:instrText xml:space="preserve"> SEQ Figura \* ARABIC </w:instrText></w:r>''' % nsdecls('w')))
p_cap_fig._p.append(parse_xml(r'''<w:r %s><w:fldChar w:fldCharType="separate"/></w:r>''' % nsdecls('w')))
p_cap_fig._p.append(parse_xml(r'''<w:r %s><w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t>1</w:t></w:r>''' % nsdecls('w')))
p_cap_fig._p.append(parse_xml(r'''<w:r %s><w:fldChar w:fldCharType="end"/></w:r>''' % nsdecls('w')))
p_cap_fig._p.append(parse_xml(r'''<w:r %s><w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t xml:space="preserve"> </w:t></w:r>''' % nsdecls('w')))
p_cap_fig._p.append(parse_xml(r'''<w:r %s><w:rPr><w:i/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t>Arquitectura SIVAC</w:t></w:r>''' % nsdecls('w')))

doc.save(test_docx)
print("Saved test document, now testing Word COM update...")

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0
wdoc = word.Documents.Open(test_docx)

# Update fields
print(f"TOCs count: {wdoc.TablesOfContents.Count}")
for i in range(1, wdoc.TablesOfContents.Count + 1):
    wdoc.TablesOfContents.Item(i).Update()

print(f"Figures TOC count: {wdoc.TablesOfFigures.Count}")
for i in range(1, wdoc.TablesOfFigures.Count + 1):
    wdoc.TablesOfFigures.Item(i).Update()

for f in wdoc.Fields:
    f.Update()

wdoc.Save()
wdoc.Close(SaveChanges=True)
word.Quit()
print("Word COM updated and closed successfully!")

# Inspect results
with zipfile.ZipFile(test_docx, "r") as z:
    root = ET.fromstring(z.read("word/document.xml"))
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    print("=== INSPECTING XML AFTER COM UPDATE ===")
    for p in root.findall(".//w:p", ns):
        txt = "".join([t.text or "" for t in p.findall(".//w:t", ns)]).strip()
        if txt:
            pStyle = p.find(".//w:pStyle", ns)
            style_name = pStyle.attrib.get(f"{{{ns['w']}}}val") if pStyle is not None else "Normal"
            print(f"[{style_name}] {txt}")
