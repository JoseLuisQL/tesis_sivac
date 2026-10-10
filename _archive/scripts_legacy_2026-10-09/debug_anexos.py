import docx
from docx.oxml.ns import qn

doc = docx.Document('salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V2.docx')
body = doc._body._body

print(f"Total children in body: {len(body)}")
for i, child in enumerate(body):
    sp = child.find('.//' + qn('w:sectPr'))
    if sp is not None:
        txt = ''.join(child.itertext())
        tag = child.tag.split('}')[-1]
        print(f"Child {i} ({tag}): sectPr found! Text: {repr(txt[:60])}")

# Let us also inspect the last 15 elements of body
print("\n--- Last 15 elements of body ---")
for i in range(max(0, len(body)-15), len(body)):
    child = body[i]
    tag = child.tag.split('}')[-1]
    txt = ''.join(child.itertext())
    print(f"Index {i} [{tag}]: {repr(txt[:80])}")
