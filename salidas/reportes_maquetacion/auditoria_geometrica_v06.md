# Auditoría geométrica y editorial — `informe_final_v06.docx`

**Fase:** F8_INTEGRACION_EDITORIAL
**Fecha:** 2026-10-21
**Squad:** E — Redacción, Estilo y Maquetación Editorial
**Agente:** `maquetador-docx`
**Alcance:** auditoría de solo lectura, hoja por hoja, del XML de `salidas/documentos/informe_final_v06.docx`.

---

## 0. Trazabilidad del documento auditado

| Dato | Valor |
|---|---|
| Archivo | `C:\MisInvestigaciones\tesis\sivac\salidas\documentos\informe_final_v06.docx` |
| Tamaño | 14 667 113 bytes |
| Modificación | 2026-10-21 16:52:05 |
| SHA-256 | `df8885a2977b009b44fc94a0eda44af60d638bbf8d7cb5a6ea68255607cb4f5a` |
| Modificación aplicada | **Ninguna.** No se guardó, sobrescribió ni recompiló el DOCX. |
| PDF de la versión | No existe PDF de la v06. La referencia de paginación es el PDF de la v05 (156 páginas). |

La numeración de página que aparece en este informe es **página física estimada** (la carátula es la página 1). La numeración impresa del cuerpo se obtiene restando 16: la página física 17 corresponde a la página impresa 1.

---

## 1. Resumen ejecutivo

| Indicador | Resultado |
|---|---|
| Tablas | 59 (54 de datos, 1 carátula, 4 marcos de fotografía) |
| Tablas que exceden el ancho útil | **0** |
| Tablas sin `<w:tblHeader/>` | **0** |
| Tablas flotantes (`<w:tblpPr>`) | **0** |
| Filas con `<w:cantSplit/>` | **100 %** |
| Rótulos de tabla y figura | 103 (51 tablas + 52 figuras), numeración correlativa sin saltos ni duplicados |
| Defectos inventariados | **409 instancias** agrupadas en 70 entradas |
| Páginas estimadas | **162** (margen ±3) |

La geometría OpenXML de las tablas está **conforme**: no hay flotación, no hay tablas sin encabezado repetido, no hay filas partidas y ningún `tblGrid` supera el ancho útil. Los defectos se concentran en el **contenido de las celdas**, en la **composición de las figuras** y en la **homogeneidad de rótulos y notas**, no en la estructura tabular.

**Ancho útil real.** El cálculo institucional es 11 906 − 1 701 − 1 440 = **8 765 dxa** (15,46 cm) en vertical y **13 697 dxa** (24,18 cm) en horizontal. El valor 8 786 dxa que circula en algunas órdenes no corresponde a esta geometría de márgenes. La tabla más ancha en vertical mide exactamente 8 765 dxa y la más ancha en horizontal 13 630 dxa: ambas caben, pero sin holgura alguna.

---

## 2. Tablas y geometría

### 2.1 Estado estructural (conforme)

- Las 59 tablas usan `<w:tblLayout w:type="fixed"/>`, declaración explícita de `<w:tblW>` en dxa y `<w:tblGrid>` completo.
- `<w:tblHeader/>` está presente en la fila 1 de las 59 tablas y sólo en la fila 1.
- `<w:cantSplit/>` cubre el 100 % de las filas (462 filas).
- Bordes APA 7 correctos en las 54 tablas de datos: `<w:tblBorders>` con superior e inferior, sin `insideH` ni `insideV`, y borde inferior de cabecera resuelto con `<w:tcBorders>` en todas las celdas de la fila 1. Las 5 tablas restantes son la carátula y los cuatro marcos de fotografía, que no son tablas de datos.
- El único giro de página (horizontal) está en las secciones 3 y 5, con geometría coherente.

### 2.2 Tablas que no caben en una página

Todas repiten cabecera y ninguna fila se corta, por lo que el corte es técnicamente admisible; se listan por su impacto en la composición.

| Tabla | Página física | Altura estimada |
|---|---|---|
| Tabla 1. Síntesis de antecedentes | 37 | 2,3 páginas |
| Tabla 4. Requerimientos funcionales | 61 | 1,5 páginas |
| Tabla 7. Planning Game | 65 | 1,1 páginas |
| Tabla 27. Casos de prueba de aceptación | 101 | 1,6 páginas |
| Tabla 44. Matriz de consistencia (horizontal) | 148 | 1,3 páginas |
| Tabla 45. Matriz de operacionalización | 151 | 1,1 páginas |

### 2.3 Desbordamiento de contenido en celdas

No hay desbordamiento de tabla, pero sí **77 palabras que no caben en el ancho útil de su columna** (medición con métricas reales de Times New Roman, descontando 216 dxa de relleno). Afectan a 19 tablas:

| Tabla | Pág. | Casos | Peor caso (requiere / dispone) |
|---|---|---|---|
| Tabla 1 | 37 | 15 | `descriptivo-propositiva` 1 854 / 1 387 dxa |
| Tabla 34 | 120 | 12 | `196-MINSA/DGIESP-2022` 2 232 / 1 422 dxa |
| Tabla 32 | 112 | 7 | `cronometrados` 1 186 / 991 dxa |
| Tabla 49 | 157 | 7 | `satisfaccion` 847 / 449 dxa |
| Tabla 50 | 158 | 7 | `satisfaccion` 847 / 449 dxa |
| Tabla 26 | 100 | 6 | `movimientos-entrega-adicional-stock.test.ts` 3 496 / 1 537 dxa |
| Tabla 37 | 129 | 4 | `+32.43%` 655 / 597 dxa |
| Tabla 45 | 151 | 4 | `post-intervención` 1 398 / 1 245 dxa |
| Tabla 27 | 101 | 3 | `Parametrización` 1 296 / 1 277 dxa |
| Tabla 19 | 82 | 2 | `inter-establecimientos.` 1 813 / 1 645 dxa |
| Tabla 43 | 138 | 2 | `multidimensional` 1 261 / 1 199 dxa |
| Tablas 7, 14, 17, 21, 22, 23, 33, 51 | 65–160 | 1 c/u | entre 10 y 753 dxa de exceso |

**Caso crítico — Tablas 49 y 50 (horizontales).** El `tblGrid` es `[1100, 2100, 651 × 15, 665]` = 13 630 dxa. Las cabeceras se partieron a mano con una barra: `ap_/01`, `up_/01`, `score_/ap`, `score_/tam_total`, `nivel_/satisfaccion`. La barra no existe en el identificador original: es un artefacto de salto manual y corrompe el nombre de la variable. En una columna de 651 dxa sólo caben 449 dxa de texto: `satisfaccion` necesita 847.

**Caso crítico — Tabla 26.** Los nombres de archivo de las suites (`.test.ts`) requieren hasta 3 496 dxa en una columna de 1 537 dxa; desbordan sobre la columna vecina.

La corrección OpenXML concreta de cada caso está en el JSON, entrada por entrada. La regla general es redistribuir el `tblGrid` conservando la suma (8 765 o 13 630 dxa), actualizar `<w:tcW w:type="dxa"/>` en cada celda y, cuando el token sea un identificador sin espacios, insertar `<w:br/>` en el separador lógico (guion, barra o guion bajo) en lugar de partir la palabra.

### 2.4 Tamaño de fuente en celdas

Doce tablas no usan 10 pt:

- **9 pt:** Tablas 35, 36, 37, 38, 39, 40, 41, 42 y 43 (páginas 125–138).
- **8,5 y 9 pt mezclados:** Tablas 49 y 50 (páginas 157–158).
- **9 y 10 pt mezclados:** marcos de fotografía 56–59 y carátula.

Corrección: `<w:sz w:val="20"/>` y `<w:szCs w:val="20"/>` en cada `<w:rPr>` de celda, recalculando la altura de fila si el texto gana una línea.

---

## 3. Figuras

- 52 rótulos, numeración 1–52 sin saltos ni duplicados; 48 imágenes para 48 figuras.
- Todas las imágenes están centradas, dentro de la caja de texto (máximo 14,73 × 13,21 cm) y sin flotación.
- **38 figuras (11 a 48) tienen la imagen antes del rótulo.** El lector ve primero el gráfico y después «Figura N» con su título. Las figuras 1 a 10 sí respetan el orden rótulo → imagen → nota. Corrección: reordenar los hijos de `<w:body>` para que el párrafo con `<w:drawing>` quede entre el rótulo y la nota, conservando `<w:keepNext/>` en rótulo e imagen.
- **4 figuras sin imagen (49 a 52, páginas 161–162).** En su lugar hay un marco de una celda con el texto «ESPACIO RESERVADO PARA FOTOGRAFÍA DE EVIDENCIA», situado por encima del rótulo. Además del contenido faltante, el marco está en la posición que correspondería a la imagen, no a la nota.
- **5 imágenes por debajo de 300 DPI:**

| Imagen | Figura | Pág. | DPI efectivo |
|---|---|---|---|
| Escudo de carátula | — | 1 | 118 |
| `rId21` | Figura 6 | 47 | 137 |
| `rId24` | Figura 9 | 52 | 183 |
| `rId16` | Figura 1 | 42 | 257 |
| `rId17` | Figura 2 | 43 | 260 |

El resto está entre 306 y 497 DPI.

- Los títulos de las figuras 49 a 52 terminan en punto, práctica que APA 7 no admite en rótulos.

---

## 4. Rótulos y notas

| Defecto | Alcance | Páginas |
|---|---|---|
| Título en negrita en lugar de cursiva | Tabla 1, Tabla 29, Tabla 31 | 37, 108, 111 |
| Número del rótulo sin negrita (la etiqueta sí es negrita) | 88 de 103 rótulos | 55–162 |
| Rótulo a 10 pt en lugar de 12 pt | 18 rótulos: Tabla 1, Figuras 1–10, Tabla 2, Tablas 29–34 | 37–120 |
| Rótulo sin estilo de párrafo (formato directo) | 103 de 103 | todo el documento |
| Nota de tabla sin el prefijo «*Nota.*» en cursiva | 24 notas | 61, 63, 64, 65, 66, 68, 73, 77–86, 101, 103 |

Las notas sí están a 9,5 pt con interlineado sencillo (`w:line="240"`), conforme. El prefijo es lo único que falta: se resuelve anteponiendo un run en cursiva con `Nota. ` al primer run del párrafo.

Ningún rótulo usa un estilo de párrafo: los 103 tienen `<w:pPr>` sin `<w:pStyle>`. Los índices funcionan sólo porque los campos `SEQ` existen, pero eso explica la deriva de tamaños y negritas. La corrección estructural es definir «Título de ilustración» en `styles.xml` y aplicarlo a los 103 rótulos.

---

## 5. Contenido duplicado y referencias cruzadas

Ocho párrafos contienen **dos veces el mismo bloque redactado con variantes**, con artefactos de puntuación y referencias cruzadas antiguas:

| Elemento | Pág. | Referencia vigente / obsoleta |
|---|---|---|
| 380 | 68 | Figura 3 / Figura 13 |
| 393 | 71 | Figura 6 / Figura 16 |
| 472 | 87 | Tabla 23 / Tabla 25 |
| 686 | 124 | Tabla 4 / Tabla 35 |
| 693 | 126 | Tabla 5 y Figura 6 / Tabla 36 y Figura 46 |
| 701 | 128 | Tabla 6 y Figura 7 / Tabla 37 y Figura 47 |
| 709 | 130 | Tabla 7 y Figura 8 / Tabla 38 y Figura 48 |
| 750 | 138 | Tabla 12 / Tabla 43 |

Artefactos detectados: «emparejadas., los resultados», «Figura 7., la implantación», «desarrollo. priorizando», «psicométrico de .800», «desarrollo. priorizando el rendimiento», y fragmentos en minúscula al inicio de oración («desacoplado en capas…», «web SIVAC mejora…»). La duplicación infla el documento en aproximadamente 1,2 páginas.

Además, el párrafo 423 (pág. 76) remite a «las Tablas 8 a 22» cuando el diccionario de datos ocupa las **Tablas 10 a 24**.

**Causa raíz:** no existen campos `REF` ni marcadores de referencia en todo el documento (0 campos `REF`, 0 marcadores `_Ref`). Las menciones «en la Tabla N» son texto estático; cualquier renumeración las deja obsoletas. Hay 103 campos `SEQ` y 214 `PAGEREF`, pero ningún `REF`.

**Marcador pendiente:** la Tabla 34 (pág. 120), fila 4, columnas 5–7, contiene `[Pendiente]` en la fila del tercer juez validador (V de Aiken, IVC y dictamen).

---

## 6. Párrafos, referencias y secciones

- Cuerpo narrativo: 284 párrafos; 279 justificados, 274 con interlineado 360 y 220 con sangría de primera línea de 720 dxa. Las excepciones son listas con viñeta, palabras clave y bloques legales de la declaración jurada, no párrafos narrativos.
- Encabezados: 129 párrafos con `<w:outlineLvl>` (23 de nivel 0, 30 de nivel 1, 58 de nivel 2 y 18 de nivel 3) y ningún estilo de encabezado. El TOC usa `\o "1-3"`, por lo que los 18 de nivel 3 quedan fuera del índice: 23 + 30 + 58 = 111 entradas, que es exactamente lo que muestra el índice. Es coherente, pero la estructura depende de formato directo.
- Referencias bibliográficas: 42 entradas, todas con sangría francesa de 720 dxa, interlineado 360, 12 pt, justificadas y 120 dxa de espaciado posterior. **Ninguna tiene hipervínculo nativo** (`w:hyperlink` = 0), pese a que la norma institucional pide DOIs y URLs activos.
- Secciones: 7. Márgenes correctos en todas (izquierdo 1 701 dxa, resto 1 440 dxa). Sección 1 en romanos minúsculos desde ii; sección 2 en arábigos desde 1. Encabezados y pies desvinculados. El documento no tiene saltos de página explícitos: los cortes son por `sectPr`, correcto.

**Dos defectos de paginación:**

1. Los romanos minúsculos están en el **encabezado alineado a la derecha** (páginas i–xiv). El modelo UNAJMA los ubica centrados al pie.
2. Los encabezados de las secciones 3, 4, 5 y 6 conservan como resultado cacheado el valor «1»; al abrir el documento en un visor que no repagina se lee «1» en todas esas páginas. Se corrige marcando los campos como sucios o refrescando con Word COM antes de exportar.

---

## 7. Campos e índices

| Campo | Estado |
|---|---|
| `TOC \o "1-3" \h \z \u` | 111 entradas cacheadas, íntegras |
| `TOC \h \z \c "Figura"` | 52 entradas cacheadas, íntegras |
| `TOC \h \z \c "Tabla"` | 51 entradas cacheadas, íntegras |
| `SEQ Tabla` / `SEQ Figura` | 51 + 52, correlativos, sin saltos ni duplicados |
| `PAGEREF` | 214, con marcadores `_Toc` existentes |
| `REF` | **0** |

Los índices conservan la paginación de la v05: la última entrada (Anexo 7) figura en la página 138. Con el crecimiento de la v06 la última página impresa estimada es 146, de modo que las entradas quedan corridas unas 6 páginas. Los tres índices requieren actualización antes de exportar el PDF.

---

## 8. Estimación de paginación

El ancla es el PDF de la v05: 156 páginas físicas, con cortes de orientación en 1–141 (vertical), 142–144 (horizontal), 145–150 (vertical), 151–152 (horizontal) y 153–156 (vertical). La v06 agrega unos 22 800 caracteres en el cuerpo respecto de la v05 (300 540 frente a 277 735 caracteres en el cuerpo), equivalentes a unas 6 páginas.

| Sección | Contenido | Páginas estimadas |
|---|---|---|
| S0 | Carátula | 2 |
| S1 | Preliminares (romanos i–xiv) | 14 |
| S2 | Cuerpo: capítulos I–V y referencias | 131 |
| S3 | Anexo 1, matriz de consistencia (horizontal) | 3 |
| S4 | Anexos 2 a 4 (vertical) | 6 |
| S5 | Tablas 49 y 50 (horizontal) | 2 |
| S6 | Anexos 5 a 7 (vertical) | 4 |
| **Total** | | **162** (margen ±3) |

Página impresa final estimada: **146**.

---

## 9. Plan de corrección priorizado

1. Eliminar los 8 párrafos con bloque duplicado y corregir sus referencias cruzadas (páginas 68–138).
2. Reordenar imagen y rótulo en las 38 figuras 11–48: el rótulo siempre arriba.
3. Insertar las 4 imágenes faltantes de las figuras 49–52 y retirar los marcos de reemplazo.
4. Reemplazar los 3 marcadores `[Pendiente]` de la Tabla 34 por los valores definitivos.
5. Corregir el desbordamiento de la Tabla 26 (nombres de archivo) y de las Tablas 49–50 (identificadores segmentados).
6. Normalizar los 103 rótulos: número en negrita, título en cursiva, 12 pt y estilo de párrafo propio.
7. Anteponer el prefijo «*Nota.*» en cursiva a las 24 notas de tabla que carecen de él.
8. Elevar a 10 pt las celdas de las 12 tablas que están a 9 pt o 8,5 pt.
9. Sustituir las 5 imágenes con menos de 300 DPI (Figuras 1, 2, 6, 9 y escudo de carátula).
10. Refrescar TOC, TOF y TOT, marcar los campos `PAGE` y convertir las menciones a Tabla y Figura en campos `REF`.

Estas correcciones no se aplicaron en esta comisión. La reconstrucción de la Tabla 30 y el refresco de índices corresponden a una comisión separada, según lo ordenado.

---

## Anexo. Ubicación estimada de las 59 tablas

| # | Tabla | Pág. |
|---|---|---|
| 1 | Carátula (marco) | 2 |
| 2 | Tabla 1. Síntesis de antecedentes | 37 |
| 3 | Tabla 2. Dimensiones e indicadores | 55 |
| 4 | Tabla 3. Roles de usuarios | 61 |
| 5 | Tabla 4. Requerimientos funcionales | 61 |
| 6 | Tabla 5. Requerimientos no funcionales | 63 |
| 7 | Tabla 6. Trazabilidad | 64 |
| 8 | Tabla 7. Planning Game | 65 |
| 9 | Tabla 8. Plan de iteraciones | 67 |
| 10 | Tabla 9. RBAC | 73 |
| 11–25 | Tablas 10–24. Diccionario de datos | 76–86 |
| 26 | Tabla 25. Stack tecnológico | 87 |
| 27 | Tabla 26. Suites de pruebas | 100 |
| 28 | Tabla 27. Casos de aceptación | 101 |
| 29 | Tabla 28. Calidad ISO/IEC 25010 | 103 |
| 30 | Tabla 29. Cronograma de intervención | 108 |
| 31 | Tabla 30. Población y muestra | 109 |
| 32 | Tabla 31. Unidades de observación | 111 |
| 33 | Tabla 32. Operacionalización | 112 |
| 34 | Tabla 33. Técnicas e instrumentos | 116 |
| 35 | Tabla 34. Validación de instrumentos | 120 |
| 36–44 | Tablas 35–43. Confiabilidad y contrastes | 125–138 |
| 45 | Tabla 44. Matriz de consistencia (horizontal) | 148 |
| 46 | Tabla 45. Operacionalización (anexo) | 151 |
| 47–49 | Formularios de validación (sin rótulo) | 153–154 |
| 50–52 | Tablas 46–48. Instrumentos | 155–156 |
| 53–54 | Tablas 49–50. Matrices de datos (horizontal) | 157–158 |
| 55 | Tabla 51. Historias de usuario | 160 |
| 56–59 | Marcos de fotografía (sin rótulo) | 160–162 |

El inventario completo, con la corrección OpenXML de cada defecto, está en `auditoria_geometrica_v06.json`.
