---
name: figuras-de-fuentes-pdf
description: Extrae figuras, gráficos y tablas de los PDFs de fuentes bibliográficas a 300 DPI con su leyenda, página física e impresa y cita APA 7 "Adaptado de", con revisión visual obligatoria. Usar cada vez que se necesite reproducir o adaptar una figura de una fuente indexada.
---

# FIGURAS DE FUENTES BIBLIOGRÁFICAS (PDF → PNG 300 DPI con trazabilidad)

`$PY` = `C:/MisInvestigaciones/tesis/sivac/.venv/Scripts/python.exe`, desde la raíz del repositorio. Herramienta: `scripts/fuentes/extractor_figuras.py`.

## 1. Comandos
```
# Vista previa: no escribe nada
$PY scripts/fuentes/extractor_figuras.py extraer --pdf "parte del nombre o ruta" --solo-detectar [--paginas 34,35,51] --json

# Extraer: PNG 300 DPI + JSON sidecar por figura + catalogo_figuras.md con enlaces ![[…]]
$PY scripts/fuentes/extractor_figuras.py extraer --pdf "…" [--paginas 3,5-7] \
    --autor "Sommerville, I." --anio 2016 --titulo "Software engineering" --editorial Pearson \
    --modo adaptado|reproducido [--con-leyenda] [--forzar]

# Recorte manual de cualquier región
$PY scripts/fuentes/extractor_figuras.py pagina --pdf "…" --pag N --clip x0,y0,x1,y1

$PY scripts/fuentes/extractor_figuras.py listar --pdf "…"
```
Salida por defecto: `obsidian_vault/_adjuntos/figuras_fuentes/<slug-del-pdf>/figura_pNNNN_k.png`. No sobrescribe sin `--forzar` y rechaza escribir en `referencias/`, `datos/raw/` y `syncova`.

## 2. Qué hacer según el resultado
| Campo del sidecar | Acción |
|---|---|
| `confianza: alta` | Abrir el PNG con `Read` y confirmar que la figura está completa |
| `confianza: media` o `baja` | **Revisión visual obligatoria**; si está cortada, `pagina --clip` con coordenadas corregidas |
| `omitidas` (leyenda sin región asociable) | No inventar la figura; ver la página y recortar con `pagina --clip` |
| `requiere_ocr` o sin capa de texto | No se detecta leyenda; Tesseract no está instalado; informar al tesista |
| `cita_sugerida` con `[VERIFICAR: …]` | Completar autor, año y página impresa con `citacion-exacta-pdf` |

«Alta» indica que leyenda y región se asociaron sin ambigüedad en la geometría. **No reemplaza la revisión visual.**

## 3. Cita APA 7
Pie de figura: *Nota.* Adaptado de *Título de la obra* (p. X), por A. Apellido, año, Editorial. La página X es la **impresa**, no la física. Si se reproduce sin cambios, añadir la mención de permiso cuando corresponda.

## 4. Insertar en el informe
Solo con el editor de DOCX con control de formato (`scripts/utilidades/editor_docx.py`, cuando esté disponible), que exige ≥ 300 DPI efectivos al ancho pedido y centra la imagen con «Figura N» en negrita, título en cursiva y «Nota.» al pie. No pegar imágenes a mano.
