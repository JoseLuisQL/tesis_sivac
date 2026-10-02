import fitz
import os

pdf_path = 'salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V2.pdf'
doc = fitz.open(pdf_path)

print(f'Total de paginas del PDF: {len(doc)}')

t5_pages = []
t12_pages = []

for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    if 'Operacionalización de variables' in text and page_num > 10:
        t5_pages.append(page_num)
    if 'Matriz de Consistencia' in text and page_num > 10:
        t12_pages.append(page_num)

print(f'Paginas encontradas para Tabla 5: {[p+1 for p in t5_pages]}')
print(f'Paginas encontradas para Tabla 12: {[p+1 for p in t12_pages]}')

out_dir = os.path.join('salidas', 'figuras', 'verificacion')
os.makedirs(out_dir, exist_ok=True)

for p in t5_pages:
    page = doc[p]
    pix = page.get_pixmap(dpi=150)
    img_name = os.path.join(out_dir, f'pagina_tabla5_{p+1}.png')
    pix.save(img_name)
    print(f'Guardada: {img_name}')

for p in t12_pages:
    page = doc[p]
    pix = page.get_pixmap(dpi=150)
    img_name = os.path.join(out_dir, f'pagina_tabla12_{p+1}.png')
    pix.save(img_name)
    print(f'Guardada: {img_name}')
