---
name: extraccion-figuras-pdf-docx
description: Procedimientos para extracción, optimización y escalado a 300 DPI de diagramas UML, esquemas arquitecturales y capturas de pantalla desde PDFs y DOCX para SIVAC-THESIS-LAB.
---

# EXTRACCIÓN Y TRATAMIENTO DE FIGURAS Y DIAGRAMAS (300 DPI)

> **Propósito:** Esta habilidad define los procedimientos técnicos en Python para extraer diagramas, esquemas de bases de datos y capturas de pantalla desde archivos PDF y DOCX, asegurando una resolución mínima de 300 DPI y estricto apego al formato de figuras de APA 7.

---

## 1. Extracción de Imágenes desde Documentos Word (.docx)

Los documentos `.docx` son contenedores ZIP donde las imágenes residen en `word/media/`.

```python
import zipfile
import os
from PIL import Image

def extraer_imagenes_docx(ruta_docx, carpeta_salida, dpi_objetivo=300):
    os.makedirs(carpeta_salida, exist_ok=True)
    with zipfile.ZipFile(ruta_docx, 'r') as docx_zip:
        for file_info in docx_zip.infolist():
            if file_info.filename.startswith('word/media/'):
                nombre_base = os.path.basename(file_info.filename)
                if not nombre_base:
                    continue
                ruta_temp = os.path.join(carpeta_salida, nombre_base)
                with open(ruta_temp, 'wb') as f:
                    f.write(docx_zip.read(file_info.filename))
                
                # Procesar y asegurar 300 DPI
                try:
                    with Image.open(ruta_temp) as img:
                        # Guardar con metadatos de 300 DPI
                        ruta_final = os.path.join(carpeta_salida, f"proc_{nombre_base}")
                        img.save(ruta_final, dpi=(dpi_objetivo, dpi_objetivo))
                except Exception as e:
                    print(f"Error procesando {nombre_base}: {e}")
```

---

## 2. Extracción de Gráficos Vectoriales y Renderizado de Páginas PDF a 300 DPI

Para extraer esquemas o diagramas completos desde páginas de tesis o manuales:

```python
import fitz  # PyMuPDF
import os

def renderizar_pagina_pdf_300dpi(ruta_pdf, num_pagina, ruta_salida_png, zoom=4.166):
    """
    Renderiza una página PDF a 300 DPI (72 DPI estándar * 4.166 = 300 DPI).
    """
    doc = fitz.open(ruta_pdf)
    pagina = doc.load_page(num_pagina - 1)
    
    mat = fitz.Matrix(zoom, zoom)
    pix = pagina.get_pixmap(matrix=mat, alpha=False)
    pix.save(ruta_salida_png)
    doc.close()
```

---

## 3. Optimización de Capturas de Pantalla de la Interfaz SIVAC (Capítulo III)

Para las 15 Historias de Usuario (HU-01 a HU-15), las capturas de la aplicación web SIVAC deben prepararse con:
1. **Recorte quirúgico:** Eliminar barras del navegador y áreas irrelevantes.
2. **Borde sutil:** Contorno gris claro de 1 px (`#D3D3D3`) para delimitar fondos blancos del cuerpo del texto.
3. **Nitidez y Contraste:** Redimensionamiento mediante remuestreo de alta calidad (`Image.Resampling.LANCZOS`).
4. **Metadatos EXIF / JFIF:** Configurados a `300 x 300` DPI.
