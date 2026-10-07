---
name: apa7-es-tesis
description: Normas oficiales APA 7.ª edición en español para citación, referencias, tablas y figuras en la tesis SIVAC.
---

# Guía Operativa de Normas APA 7 en Español

## 1. Citación en el Texto
- **Un autor:** Pérez (2023) o (Pérez, 2023).
- **Dos autores:** Pérez y Gómez (2022) o (Pérez & Gómez, 2022) según modelo institucional (en español se prefiere "y").
- **Tres o más autores:** Desde la primera mención: Pérez et al. (2024) o (Pérez et al., 2024).
- **Citas directas cortas (< 40 palabras):** Entre comillas dentro del párrafo, incorporando autor, año y página: (Pérez, 2023, p. 45).
- **Citas directas largas (≥ 40 palabras):** En bloque independiente con sangría de 1.27 cm (0.5 in) a la izquierda, sin comillas, interlineado doble, con página al final.
- **Paráfrasis:** Reescritura legítima del concepto, siempre con autor y año. No requiere comillas.

## 2. Formato de Tablas y Figuras
### Tablas:
- **Número:** En negrita arriba (ej. **Tabla 1**).
- **Título:** Línea siguiente en cursiva y con mayúscula inicial (ej. *Distribución de frecuencias de tiempos de procesamiento*).
- **Líneas horizontales:** Solo tres líneas principales (superior, inferior del encabezado e inferior de la tabla). Sin líneas verticales.
- **Nota:** Al pie de la tabla: *Nota.* Explicación de abreviaturas o fuente. Adaptado de... o Elaboración propia.
- **Prohibición de fórmulas matemáticas en celdas (Estándar UNAJMA):**
  - Las celdas de las tablas (Operacionalización de Variables, Matriz de Consistencia, etc.) deben contener **ÚNICAMENTE texto formal descriptivo**, dimensiones, nombres de indicadores, unidades de medida y escalas de valoración.
  - Queda estrictamente prohibido incrustar ecuaciones fraccionarias, MathML u OMML dentro de celdas de tablas (estándar institucional UNAJMA, tesis modelo Jhon 2026).
  - Toda fórmula matemática de cálculo de indicadores debe ubicarse exclusivamente en el cuerpo narrativo del documento (Capítulo IV / Metodología o Plan de Tratamiento de Datos), como ecuaciones dedicadas numeradas y centradas con su respectiva definición de variables.

### Figuras:
- **Número:** En negrita arriba (ej. **Figura 1**).
- **Título:** Línea siguiente en cursiva.
- **Imagen:** Clara, legible, resolución mínima de 300 DPI.
- **Nota:** Al pie de la figura: *Nota.* Descripción o fuente.

## 3. Lista de Referencias
- Orden alfabético estricto. Sangría francesa de 1.27 cm (`<w:ind w:left="720" w:hanging="720"/>`).
- Interlineado 1.5 líneas (`<w:spacing w:line="360" w:lineRule="auto"/>`).
- Espaciado posterior 6 pt (`w:after="120"`).
- Artículos con DOI en formato URL activa: `https://doi.org/...`.
- Toda referencia listada debe haber sido citada en el texto, y toda cita en el texto debe figurar en la lista.

## 4. Tipografía, Interlineado y Sangrías en Microsoft Word (.docx / OpenXML)
Todo documento o capítulo generado en Word debe implementar obligatoriamente las siguientes especificaciones técnicas mediante `scripts/utilidades/docx_quirurgico.py`:
- **Cuerpo de texto narrativo:**
  - Tipografía: Times New Roman 12 pt (`<w:sz w:val="24"/>` y `<w:szCs w:val="24"/>`).
  - Interlineado: 1.5 líneas (`<w:spacing w:line="360" w:lineRule="auto"/>`).
  - Sangría de primera línea: 1.27 cm / 0.5 in (`<w:ind w:firstLine="720" w:left="0" w:right="0"/>`).
  - Espaciado: 0 pt anterior y 0 pt posterior (`<w:spacing w:before="0" w:after="0"/>`).
  - Alineación: Justificado (`<w:jc w:val="both"/>`).
- **Encabezados (Headings 1, 2, 3, 4):**
  - Sin sangría (`<w:ind w:firstLine="0" w:left="0"/>`).
  - Negrita, Times New Roman, espaciado anterior 12-18 pt y posterior 6 pt.
- **Rótulos y títulos de tablas y figuras:**
  - Sin sangría (`firstLine="0"`), alineación izquierda, espaciado controlado.
- **Notas de tablas y figuras:**
  - Times New Roman 9.5 o 10 pt, interlineado sencillo (1.0 = 240 dxa), sin sangría.

