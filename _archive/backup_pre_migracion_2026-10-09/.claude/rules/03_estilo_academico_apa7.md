---
description: Reglas de estilo académico, normas APA 7 y política de cero alucinaciones
---

# REGLA CANÓNICA 03: ESTILO ACADÉMICO, APA 7 Y CERO ALUCINACIONES

## 1. Tono y Prosa Académica
- **Estilo:** Formal, impersonal, objetivo y riguroso en español científico.
- **Voz:** Tercera persona del singular ("se observó", "el análisis determinó", "se concluye"), evitando pronombres personales de primera persona.
- **Densidad Conceptual:** Párrafos de 4 a 8 oraciones estructurados según la fórmula:
  1. *Oración tópica:* Aserción clara del argumento principal.
  2. *Evidencia:* Datos o citas verificadas que sustentan la afirmación.
  3. *Análisis:* Interpretación crítica de la evidencia en el contexto de SIVAC y DISA Apurímac II.
  4. *Transición:* Conexión lógica con la siguiente idea.
- **Prohibición de Relleno (*Fluff-Free*):** Prohibido el uso de frases vacías, lugares comunes o retórica innecesaria.

## 2. Política de Cero Alucinaciones y Verificabilidad
1. **Correspondencia Biunívoca 1:1:** Toda fuente citada en el cuerpo del texto debe aparecer exactamente en la lista final de Referencias Bibliográficas, y toda referencia listada debe contar con al menos una cita activa en el texto.
2. **Identificador Verificable:** Toda cita teórica debe contar con citekey en Zotero (`@citekey`), DOI activo verificado o URL académica comprobable mediante You.com / Firecrawl.
3. **Prohibición de Invención Bibliográfica:** Prohibido inventar autores, títulos, años, números de página o citas directas. Si una referencia no puede corroborarse al 100%, se etiqueta como `[VERIFICAR: motivo]` y se reporta en el handoff.

## 3. Tipografía y Maquetación Editorial Quirúrgica (UNAJMA / APA 7)
Todas las herramientas, compiladores y agentes que generen o modifiquen documentos Word (`.docx`) deben implementar estrictamente los parámetros OpenXML a través de `scripts/utilidades/docx_quirurgico.py`:

1. **Cuerpo de Texto General:**
   - **Fuente:** Times New Roman 12 pt (`<w:sz w:val="24"/>` y `<w:szCs w:val="24"/>`).
   - **Interlineado:** 1.5 líneas obligatorio (`<w:spacing w:line="360" w:lineRule="auto"/>`). Queda prohibido el interlineado simple (240 dxa) en cuerpo de texto.
   - **Sangría de Primera Línea:** 1.27 cm / 0.5 pulgadas obligatorio en cada párrafo narrativo (`<w:ind w:firstLine="720" w:left="0" w:right="0"/>`).
   - **Espaciado entre párrafos:** Cero puntos anterior y cero puntos posterior (`<w:spacing w:before="0" w:after="0"/>`).
   - **Alineación:** Justificado (`<w:jc w:val="both"/>`).

2. **Títulos y Encabezados (Headings):**
   - **Sin sangría:** Cero sangría de primera línea y cero margen izquierdo (`<w:ind w:firstLine="0" w:left="0"/>`).
   - **Fuente:** Times New Roman, Negrita (`<w:b w:val="1"/>`). Nivel 1: 12 pt o 14 pt (centrado o izquierda). Nivel 2: 12 pt (izquierda). Nivel 3: 12 pt (cursiva y negrita, izquierda).
   - **Espaciado:** Espacio anterior proporcional (12 a 18 pt / 240 a 360 dxa) y posterior (6 pt / 120 dxa). Interlineado 1.5 (`w:line="360"`).

3. **Rótulos y Captions de Tablas y Figuras:**
   - **Rótulo:** Negrita (ej. **Tabla 1** o **Figura 1**), alineado a la izquierda, sin sangría (`firstLine="0"`), espacio anterior 12 pt (240 dxa), espacio posterior 2 pt (40 dxa).
   - **Título descriptivo:** Cursiva (ej. *Operacionalización de variables*), alineado a la izquierda, sin sangría, espacio posterior 6 pt (120 dxa).

4. **Notas de Tablas y Figuras:**
   - **Fuente:** Times New Roman 9.5 pt o 10 pt (`w:sz="19"` o `w:sz="20"`).
   - **Interlineado:** Sencillo 1.0 (`<w:spacing w:line="240" w:lineRule="auto"/>`).
   - **Sangría:** Sin sangría de primera línea (`firstLine="0"`).
   - **Espaciado:** Anterior 3 pt (60 dxa), posterior 12 pt (240 dxa).
   - **Prefijo:** "*Nota.*" o "*Fuente:*" en cursiva inicial.

5. **Referencias Bibliográficas:**
   - **Sangría francesa:** 1.27 cm obligatoria (`<w:ind w:left="720" w:hanging="720"/>`).
   - **Interlineado:** 1.5 líneas (`w:line="360"`).
   - **Fuente:** Times New Roman 12 pt.
   - **Espaciado posterior:** 6 pt (120 dxa).

6. **Márgenes y Paginación Desvinculada:**
   - **Márgenes:** Izquierdo 3.0 cm (para empastado), Superior 2.5 cm, Derecho 2.5 cm, Inferior 2.5 cm.
   - **Páginas preliminares:** Romanos en minúscula (i, ii, iii...), centrados o al pie, iniciando en carátula (sin imprimir número).
   - **Cuerpo de la tesis:** Números arábigos reiniciados en 1 en la Introducción, ubicados en la esquina superior derecha.

## 4. Tablas y Figuras APA 7
- **Tablas:** Formato formal APA 7 de tres líneas horizontales (borde superior, borde inferior de encabezados y borde inferior de tabla). **Cero líneas verticales**. Tamaño de fuente en celdas: 10 pt. Fila de encabezado repetida (`<w:tblHeader/>`) y filas no fragmentables (`<w:cantSplit/>`).
- **Figuras:** Imágenes vectoriales o rasterizadas a **300 DPI**, con número de figura en negrita, título en cursiva, y nota de figura explicativa al pie indicando la fuente.

### Prohibición de Fórmulas Matemáticas Dentro de Celdas de Tablas (Estándar UNAJMA)
- **Contenido estrictamente textual en tablas:** Las celdas de todas las tablas del proyecto (Operacionalización de Variables, Matriz de Consistencia, fichas metodológicas, cuadros de resumen, etc.) deben contener **ÚNICAMENTE texto formal descriptivo**, dimensiones, nombres de indicadores, unidades de medida y escalas de valoración, conforme al estándar institucional UNAJMA reflejado en la tesis modelo de Jhon (2026).
- **Prohibición absoluta de OMML / MathML en tablas:** Queda estrictamente prohibido incrustar ecuaciones fraccionarias, expresiones algebraicas complejas, bloques MathML o elementos OMML (`<m:oMath>`) dentro de celdas de tablas.
- **Emplazamiento exclusivo en cuerpo narrativo:** Toda fórmula matemática para el cálculo y cuantificación de indicadores debe ubicarse exclusivamente en el cuerpo narrativo del documento (en el Capítulo IV / Metodología o en la sección de Técnicas y Métodos de Procesamiento de Datos), como ecuaciones dedicadas, centradas, numeradas correlativamente y acompañadas de la definición formal de cada uno de sus términos y variables.
