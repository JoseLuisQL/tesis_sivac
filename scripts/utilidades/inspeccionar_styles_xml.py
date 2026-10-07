import docx
from docx.oxml.ns import qn
import lxml.etree as ET

def inspect_styles(docx_path):
    print(f"\n=== INSPECTING STYLES: {docx_path} ===")
    doc = docx.Document(docx_path)
    xml_content = doc.styles._element.xml
    root = ET.fromstring(xml_content.encode('utf-8'))
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Check default paragraph properties
    docDefaults = root.find('.//w:docDefaults', ns)
    if docDefaults is not None:
        pPrDefault = docDefaults.find('.//w:pPrDefault', ns)
        rPrDefault = docDefaults.find('.//w:rPrDefault', ns)
        print("--- DOC DEFAULTS ---")
        if rPrDefault is not None:
            rFonts = rPrDefault.find('.//w:rFonts', ns)
            sz = rPrDefault.find('.//w:sz', ns)
            szCs = rPrDefault.find('.//w:szCs', ns)
            print("  rFonts:", rFonts.attrib if rFonts is not None else None)
            val_sz = sz.get(qn('w:val')) if sz is not None else None
            print("  sz (half-pts):", sz.attrib if sz is not None else None, f"({int(val_sz)/2}pt)" if val_sz else "")
        if pPrDefault is not None:
            sp = pPrDefault.find('.//w:spacing', ns)
            ind = pPrDefault.find('.//w:ind', ns)
            jc = pPrDefault.find('.//w:jc', ns)
            print("  spacing:", sp.attrib if sp is not None else None)
            print("  ind:", ind.attrib if ind is not None else None)
            print("  jc:", jc.attrib if jc is not None else None)

    # Check specific styles
    for style in root.findall('.//w:style', ns):
        s_id = style.get(qn('w:styleId'))
        if s_id in ['Normal', 'Heading1', 'Heading2', 'Heading3', 'Heading4', 'DefaultParagraphFont', 'Cita', 'Quote']:
            name = style.find('.//w:name', ns)
            name_val = name.get(qn('w:val')) if name is not None else ''
            print(f"\n--- STYLE: {s_id} ({name_val}) ---")
            pPr = style.find('.//w:pPr', ns)
            rPr = style.find('.//w:rPr', ns)
            if rPr is not None:
                rFonts = rPr.find('.//w:rFonts', ns)
                sz = rPr.find('.//w:sz', ns)
                b = rPr.find('.//w:b', ns)
                i = rPr.find('.//w:i', ns)
                color = rPr.find('.//w:color', ns)
                val_sz = sz.get(qn('w:val')) if sz is not None else None
                print("  rFonts:", rFonts.attrib if rFonts is not None else None)
                print("  sz:", sz.attrib if sz is not None else None, f"({int(val_sz)/2}pt)" if val_sz else "")
                print("  bold:", b.attrib if b is not None else None, "italic:", i.attrib if i is not None else None)
            if pPr is not None:
                sp = pPr.find('.//w:spacing', ns)
                ind = pPr.find('.//w:ind', ns)
                jc = pPr.find('.//w:jc', ns)
                print("  spacing:", sp.attrib if sp is not None else None)
                print("  ind:", ind.attrib if ind is not None else None)
                print("  jc:", jc.attrib if jc is not None else None)

inspect_styles('referencias/proyecto_base/PROYECTO_TESIS.docx')
