import docx

doc = docx.Document('salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V3_NORMALIZADO.docx')
body = doc._body._element

print(f"Total elementos en body: {len(body)}")
for idx, child in enumerate(body):
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        p_obj = docx.text.paragraph.Paragraph(child, doc)
        txt = p_obj.text.strip()
        if any(marker in txt for marker in ['2.1', '2.2', '2.3', 'CAPÍTULO III', 'CAPÍTULO V', 'Referencia Bibliográfica', 'ANEXOS']):
            print(f"[{idx}] <w:p> style={p_obj.style.name}: {txt[:65]}")
    elif tag == 'tbl':
        tbl_obj = docx.table.Table(child, doc)
        print(f"[{idx}] <w:tbl> filas={len(tbl_obj.rows)}, cols={len(tbl_obj.columns)}")
