import docx
doc = docx.Document('salidas/PROYECTO_TESIS_CONSOLIDADO_v02.docx')
for i, p in enumerate(doc.paragraphs):
    for r in p.runs:
        if 'graphic' in r._r.xml:
            # find blip
            xml = r._r.xml
            import re
            m = re.findall(r'embed="([^"]+)"', xml)
            targets = [doc.part.rels[rid].target_ref for rid in m if rid in doc.part.rels]
            print(f'Paragraph {i}: text="{p.text[:60]}" -> images: {targets}')
