---
name: referencias-nativas-docx-apa7
description: Formateo e inserción automatizada de la lista de referencias bibliográficas en Microsoft Word (.docx) con sangría francesa de 1.27 cm, estilos APA 7 y enlaces DOI activos para SIVAC-THESIS-LAB.
---

# REFERENCIAS NATIVAS EN WORD (.DOCX) — NORMA APA 7.ª EDICIÓN

> **Propósito:** Esta habilidad proporciona el protocolo y el código en Python (`python-docx`) para generar quirúrgicamente la sección **REFERENCIAS BIBLIOGRÁFICAS** en el archivo Word de la tesis, garantizando sangría francesa exacta de 1.27 cm, interlineado 1.5, tipografía Times New Roman 12 pt y enlaces DOI activos.

---

## 1. Especificaciones de Estilo APA 7 para Referencias en Word

1. **Sangría Francesa (Hanging Indent):**
   - La primera línea de cada referencia comienza alineada al margen izquierdo.
   - La segunda y subsecuentes líneas tienen una sangría obligatoria de **1.27 cm (0.5 pulgadas)**.
   - En OpenXML / python-docx:
     `left_indent = Inches(0.5)`
     `first_line_indent = Inches(-0.5)`
2. **Espaciado e Interlineado:**
   - Interlineado de 1.5 líneas (`line_spacing = 1.5`).
   - Sin espacio extra entre párrafos (`space_after = Pt(0)` o `Pt(6)` según directriz final).
3. **Tipografía:**
   - Times New Roman 12 pt para texto general.
   - Cursiva estricta para:
     - Títulos de libros.
     - Títulos de tesis e informes.
     - Nombres de revistas científicas y números de volumen: *Revista Médica*, *34*(2).
4. **Enlaces DOI / URLs:**
   - Presentados en formato URL completa: `https://doi.org/...`
   - Sin punto final tras el enlace.
   - Formateados como campos de hipervínculo nativos o texto azul/subrayado estándar.
5. **Orden Alfabético:**
   - Estricto orden letra por letra del apellido del primer autor.
   - Tratamiento de caracteres especiales del español (á, é, í, ó, ú, ñ).

---

## 2. Implementación Quirúrgica con `python-docx`

```python
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import unicodedata

def clave_ordenacion_apa7(autor_texto):
    """
    Normaliza el texto para ordenación alfabética ignorando tildes y diacríticos.
    """
    texto_limpio = unicodedata.normalize('NFD', autor_texto)
    return ''.join(c for c in texto_limpio if unicodedata.category(c) != 'Mn').lower()

def agregar_hipervinculo_oxml(paragraph, url, text, color="0000EE", underline=True):
    """
    Inserta un hipervínculo nativo OpenXML en un párrafo de python-docx.
    """
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    hyperlink = parse_xml(
        f'<w:hyperlink {nsdecls("w")} r:id="{r_id}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'  <w:r>'
        f'    <w:rPr>'
        f'      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
        f'      <w:color w:val="{color}"/>'
        f'      <w:sz w:val="24"/>'
        f'      {"<w:u w:val='single'/>" if underline else ""}'
        f'    </w:rPr>'
        f'    <w:t>{text}</w:t>'
        f'  </w:r>'
        f'</w:hyperlink>'
    )
    paragraph._p.append(hyperlink)

def insertar_referencia_apa7(doc, texto_completo, url_doi=None):
    """
    Inserta un párrafo de referencia con sangría francesa exacta de 1.27 cm.
    """
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    # Sangría francesa de 1.27 cm (0.5 in)
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.5)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    
    # Inserción de texto con segmentación de cursivas
    # Formato esperado: "Autor, A. A. (Año). *Título de la obra*. Editorial/Revista."
    partes = texto_completo.split('*')
    for i, parte in enumerate(partes):
        if not parte:
            continue
        run = p.add_run(parte)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        if i % 2 == 1:  # Los fragmentos impares van en cursiva
            run.font.italic = True
            
    # Inserción de enlace DOI si existe
    if url_doi:
        p.add_run(" ")
        agregar_hipervinculo_oxml(p, url_doi, url_doi)
```
