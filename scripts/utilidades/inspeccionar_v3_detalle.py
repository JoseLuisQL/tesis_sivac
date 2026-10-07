import docx
import re

doc = docx.Document('salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V3_NORMALIZADO.docx')
print(f"Total párrafos: {len(doc.paragraphs)}")

for i, p in enumerate(doc.paragraphs):
    xml = p._p.xml
    if 'w:drawing' in xml:
        embeds = re.findall(r'r:embed="([^"]+)"', xml)
        print(f"Párrafo {i} tiene dibujo. Texto: {p.text.strip()[:60]} | Embeds: {embeds}")
