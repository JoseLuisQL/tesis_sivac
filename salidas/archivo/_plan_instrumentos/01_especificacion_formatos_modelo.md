# 01 - Especificación forense de los formatos modelo de validación (Dr. Enrique Cóndor Tinoco, EPIS-UNAJMA)

> Fuente (inmutable, solo lectura): `C:\MisInvestigaciones\tesis\sivac\referencias\modelos_validacion\`
> Método: descompresión del OpenXML de los 2 DOCX (`word/document.xml`, `styles.xml`, `numbering.xml`, `settings.xml`, headers/footers, rels), volcado programático (lxml) de párrafos, runs y tablas, lectura de las 14 págs. de texto digital del PDF de ejemplo, inspección visual (render a 110 dpi) de los 4 PDF escaneados y recorrido de celdas/fórmulas del XLSX con openpyxl.
> Alcance: solo describe el modelo. No se inventan puntajes, firmas ni datos de jueces. Los datos del proyecto origen (autoaprendizaje, Sihui/Velasque, Soria/Minaya/Ramos) se citan únicamente como "texto del modelo" y NO deben pasar al formato SIVAC.
> Los volcados crudos reproducibles quedan en `_tmp/` (`formato_dump.txt`, `correc_dump.txt`, `dump_docx.py`, `ejem.txt`, `cuest.txt`).

---

## 1 Inventario por archivo

| # | Archivo | Tipo / tamaño | Qué contiene (estructura real) | Rol para SIVAC |
|---|---|---|---|---|
| 1 | `Formato para la validacion de instrumento por ITEM.docx` | DOCX, 47 319 B, 5 secciones, creado 2025-06-10, modificado 2025-07-06 (autor `LAPT-EPIS-03`, último `Guadalupe Sihui`, rev. 8). Word 16.0 | (a) Carta de solicitud 1 (a M.Sc. Iván Soria Solís), (b) carta 2 (a Mag. Daniel Minaya Gutiérrez), (c) carta 3 (destinatario en blanco "……", "Docente del Centro Preuniversitario"), (d) hoja "INSTRUCCIONES PARA VALIDACIÓN DEL INSTRUMENTO" con tabla rúbrica 6x3, (e) "CONSTANCIA DE VALIDACIÓN DE CONTENIDO DEL INSTRUMENTO POR ÍTEM" en blanco (datos del experto en puntos suspensivos) con tabla 25x8 y firma, (f) la misma constancia ya con datos de Javier Ramos (con tabla 25x8) | Plantilla madre: 3 cartas + instrucciones + constancia por ítem |
| 2 | `CORRECION DE FORMATOS.docx` | DOCX, 39 375 B, 1 sección, rev. 9 (modificado 2025-07-06 15:50) | 3 constancias por ítem consecutivas (Soria, Minaya, Ramos) con los datos del experto ya escritos (subrayados) y tabla 25x8 vacía; salto de página entre ellas; firma + "DNI: ……" | Versión "corregida" de la constancia (datos del experto pre-llenados); es la base del formato de constancia entregado a cada juez |
| 3 | `PUNTUACION IVC.xlsx` | XLSX, 20 900 B, 2 hojas (`Hoja1`, `Hoja2`), creado 2025-07-06 por Guadalupe Sihui | Matriz 120 filas x 3 jueces; binarización y IVC por criterio | Lógica de cálculo (ver sección 5) |
| 4 | `EJEMPLO DE PUNTUACION DE VALIDACION.pdf` | PDF digital, 14 págs, 595x842 pt (A4), 22 056 caracteres de texto | Guía didáctica del Dr. Cóndor: "Validez de instrumento. Caso práctico... paso a paso" con caso ficticio "Sistema de información ABCD" (Univ. las Colinas) | Método (promedios >= 3.3; IVC >= 0.58 con 3 jueces) y fórmulas |
| 5 | `Constancias de validacion .pdf` | PDF escaneado (CamScanner), 9 págs, sin capa de texto (18 imágenes) | 3 constancias firmadas seguidas, 3 págs c/u, orden: Minaya (pp. 1-3), Soria (pp. 4-6), Ramos (pp. 7-9) | Muestra del formato ya llenado a mano, firmado y sellado |
| 6 | `Validación Ing Daniel Minaya.pdf` | PDF escaneado, 4 págs | p.1 instrucciones; pp. 2-4 constancia (ítems 1-10, 10-21, 22-24 + firma) | idem |
| 7 | `Validación Ing Ivan Soria .pdf` | PDF escaneado, 4 págs | Idem Minaya (p.1 instrucciones + 3 págs constancia) | idem |
| 8 | `Validacion Ing Javier Ramos.pdf` | PDF escaneado, 3 págs | Solo constancia (3 págs); NO incluye hoja de instrucciones | idem |
| 9 | `Cuestionario para identificar el nivel de autoaprendizaje en estudiantes del Centro Pre Universitario – UNAJMA.pdf` | PDF (impresión de Google Forms), 11 págs, 4 417 caracteres de texto, 2 imágenes (banner) | Instrumento sometido a juicio: cabecera con imagen, descripción, instrucciones con tabla de escala 5-4-3-2-1, 6 secciones y 24 ítems Likert de frecuencia | Es el "instrumento" que el experto recibe; sirve para ver cómo se presenta (no es formato de validación) |

Notas Obsidian leídas (no modificadas): `05_MODELOS_Y_REFERENCIAS/unajma_validacion_condor_tinoco/{ANALISIS_INTEGRAL_MODELOS_VALIDACION, DESGLOSE_EJEMPLOS_VALIDACION, PLANTILLA_JUICIO_EXPERTOS_UNAJMA, ejemplos_desglosados/*}.md`, y el listado de `06_METODOLOGIA_E_INSTRUMENTOS/` (`expediente_juicio_expertos/`, `instrumentos_sivac/`). Coincido con `ANALISIS_INTEGRAL` en errores y discrepancias, salvo lo señalado en la sección 6. Atención: `PLANTILLA_JUICIO_EXPERTOS_UNAJMA.md` NO es réplica fiel (usa otros descriptores de escala, otro texto de carta y añade veredicto/CIP/fecha que el modelo original no tiene); no debe usarse como referencia de fidelidad.

---

## 2 Especificación OpenXML / visual de cada formato

### 2.0 Parámetros comunes a ambos DOCX
- **Fuente base:** `Normal` = Times New Roman (ascii/hAnsi/eastAsia/cs), idioma `es-ES`. `docDefaults`: tema minorHAnsi (Calibri) 11 pt pero Normal lo sobrescribe a TNR; `widowControl=0`, `autoSpaceDE/DN=0`. `fontTable`: Symbol, Times New Roman, Calibri, Arial, Cambria (Arial no se usa en el cuerpo).
- **Estilos usados:** `Textoindependiente` (Body Text, basado en Normal, **sz 24 = 12 pt**), `Prrafodelista` (List Paragraph, ind left 1514 hanging 359), `Ttulo1` (Heading 1: **negrita 14 pt**, `spacing before=9`, `ind left=1767 hanging=1748`, outlineLvl 0), `TableParagraph` (basado en Normal, sin cambios; el tamaño se pone por run), `Tablaconcuadrcula` (Table Grid: bordes single sz 4 color auto, 6 líneas), `TableNormal` (cell margins 0).
- **Tamaños de run:** cuerpo de cartas y constancia 12 pt; **tablas 9 pt (sz 18)**; firma/DNI/pie de firma 10 pt (sz 20); lista de adjuntos 12 pt (sz 24). Kerning/char-spacing fino (`w:spacing` -2..-10) en muchos runs (artefacto de conversión desde PDF; cosmético, no replicar).
- **Página (todas las secciones):** `pgSz w=11920 h=16850` dxa = 21.03 x 29.72 cm (casi A4: A4 = 11906 x 16838). **Vertical.** Sin columnas (`cols space=720`, una columna). Sin `gutter`.
- **Headers/footers:** existen header1-5/footer1-5 (DOCX 1) o header1/footer1 (DOCX 2), pero todos contienen **un único párrafo vacío** `Textoindependiente` con `spacing line=14 auto` y `sz` 20/15/2: **no hay encabezado, pie, logo, numeración de página ni membrete**. `pgNumType start=1` en 3 secciones sin número visible.
- **settings:** zoom 90% (DOCX1) / 80% (DOCX2); `compatibilityMode=14`; `defaultTabStop=720`.
- **Numeración (`numbering.xml`):** `numId 2` -> abstractNum 0 = viñeta símbolo (Symbol, left 1515, hanging 360, 12 pt) usada en la lista de adjuntos de las cartas; `numId 1` -> abstractNum 1 = decimal "%1." (left 1527, hanging 360, jc right, TNR) usada en las 5 viñetas numeradas de las Instrucciones.
- **Casillas/checkbox:** NO existen (ningún `w14:checkbox`, ningún símbolo de casilla, ningún `w:fldChar`/form field). No hay veredicto "aplicable/no aplicable" en ningún formato original.
- **Sombreado:** NO existe en ninguna tabla (sin `w:shd`). **Color:** todo negro; única excepción un run residual en la constancia de Ramos (DOCX1, P116) con color `EE0000` y resaltado amarillo (marca de edición, no es parte del formato).

### 2.1 DOCX 1 - Formato para la validación por ÍTEM (5 secciones)

Cada tramo termina en `w:sectPr` dentro del último párrafo del tramo (P028, P059, P087, P100) y la última sección va al final del cuerpo.

| Sección | Contenido | Márgenes (dxa / cm) | Header/Footer dist. | Tipo / otros |
|---|---|---|---|---|
| S1 | Carta 1 (Soria) | top 1940 (3.42), right 1430 (2.52), bottom 1140 (2.01), left **283 (0.50)** | 424 / 950 | `continuous`, `pgNumType start=1`, hdr rId7/ftr rId8 |
| S2 | Carta 2 (Minaya) | igual a S1 | 424 / 950 | `continuous`, hdr rId9/ftr rId10 |
| S3 | Carta 3 (en blanco) | igual a S1 | 424 / 950 | sin `type` (= nextPage), hdr rId11/ftr rId12 |
| S4 | Instrucciones + tabla rúbrica | top 1940, **right 283 (0.50)**, bottom 1140, left 283 | 424 / 950 | hdr rId13/ftr rId14 |
| S5 (final) | Constancia en blanco + constancia Ramos | top **1701 (3.00)**, right 1430, bottom **280 (0.49)**, left 283 | **0 / 0** | hdr rId15/ftr rId16 |

Observación: el margen izquierdo de 0.50 cm es solo nominal; la mayor parte del texto se desplaza con sangrías propias (ver abajo). Las secciones S1 y S2 están marcadas `continuous`; en Word el salto real entre cartas depende de que cada carta llene una página (ver sección 6, ambigüedad A-1).

**Carta de solicitud (S1-S3), párrafo por párrafo**
- Fecha: `Textoindependiente`, `ind left=5605`, tab con puntos (`tab left leader=dot pos=9426`) -> "Andahuaylas, …… de[tab punteado]de 2025". Es un campo manuscrito/completable: día y mes.
- 2 párrafos vacíos; "Señor (a):" (`ind left 1155`, `after=240`); nombre del destinatario (Carta 1: `M.SC. IVAN SORIA SOLIS`; Carta 2: sangrado con espacios `Mag. Daniel Minaya Gutiérrez`; Carta 3: `……………………………………………………………………………` puntos); línea de cargo alineada con espacios/tab: "Docente de la Escuela Profesional de Ingeniería de Sistemas" (Carta 3: "Docente del Centro Preuniversitario “UNAJMA”").
- "De nuestra mayor consideración:" (`jc=both`, `ind left 1155`, `after=240`).
- Párrafo de presentación (`jc=both`, `ind left 1155`) y párrafo de petición (`jc=both`, `ind left 1155`); algunos runs en negrita (ver texto literal).
- "Presentamos los siguientes documentos:" (`ind left 1155`) + **4 viñetas** (`Prrafodelista`, numId 2, `ind left 1514 hanging 359`, 12 pt; líneas 2 y 3 con `line=293 exact`).
- Despedida: `ind left=1155 right=648 firstLine=705`, `before=275`, interlineado `line=242 auto`.
- "Atentamente," centrado (`jc=center`, `ind right=1002`), 5-6 párrafos vacíos (`line=298 exact`, `before=1`) como espacio de firma.
- Línea de firmas: `Prrafodelista` con 2 secuencias de puntos suspensivos "……………………………………….…" separadas por espacios (12 pt).
- Nombres de las dos tesistas en una línea con espacios; "Tesista    Tesista"; "DNI N° 70233314    DNI N° 76189071" (el último párrafo de cada carta lleva el `sectPr`). Alineación hecha con espacios y NBSP, no con tabuladores ni tabla.

**Hoja de instrucciones (S4)**
- Título "INSTRUCCIONES PARA VALIDACIÓN DEL INSTRUMENTO": negrita 12 pt, centrado, `ind left 1205 right 1002`.
- Lista numerada (decimal, `ind left≈1526 hanging 359`): 5 puntos (ver texto literal). Entre el punto 1 y 2 hay una lista sin viñeta de los 5 criterios: un solo párrafo "Suficiencia Relevancia Coherencia Claridad Redacción" con `ind right=8207` que fuerza el salto a una línea por criterio (truco de sangría derecha; en Word se ven 5 líneas).
- Escala "4 = Cumple completamente, 3 = Cumple adecuadamente, 2 = Cumple parcialmente, 1 = No cumple" en una línea (`ind left 1527`, `jc=both`, `before=74`) con los 4 dígitos en **negrita** y el resto normal.
- **Tabla rúbrica** (`TableNormal`, `tblW auto`, `tblInd 1316`, **`tblLayout fixed`**, bordes single sz 4 negro en las 6 líneas, `tblLook 01E0`):
  - `tblGrid`: **1294 / 1609 / 6091** dxa (total 8994).
  - 6 filas: encabezado (`trHeight 354`), Suficiencia (1036), Relevancia (1034), Coherencia (1034), Claridad (alto no volcado, similar), Redacción (827). Sin merges (`gridSpan`/`vMerge` = 0). Sin sombreado.
  - Texto 9 pt (`sz 18`), encabezado en negrita ("Criterios" `ind left 302`, "Descripción" `ind left 345`, "Indicadores" centrado). Col 1: nombre del criterio en **negrita**, precedido de un párrafo vacío (`before=121`) que lo baja verticalmente. Col 2 justificada (`jc=both`, `ind left 104 right 98`). Col 3: 4 párrafos, uno por nivel; el número y "=" van en **negrita**, el descriptor en normal; algunos con `line=206/207 exact`.
  - Tras la tabla: párrafos 4 y 5 numerados y "Agradecemos profundamente su colaboración." en negrita (`ind left 1167`).

**Constancia por ítem (S5)**
- Título: estilo `Ttulo1` ("CONSTANCIA DE VALIDACIÓN DE CONTENIDO DEL INSTRUMENTO POR ÍTEM"), negrita 14 pt, `ind left 3939 hanging 1779` (se renderiza centrado en 2 líneas), `before=0`.
- Párrafo de declaración: `Textoindependiente`, `jc=both`, `ind left 1474`, `before=248`, **`line=360 auto` (interlineado 1.5)**, 12 pt. Contiene los campos con puntos suspensivos (ver sección 4).
- Párrafo vacío `jc=both ind left 1039 right 1034`, y luego la **tabla de ítems**:
  - Estilo `Tablaconcuadrcula` (bordes sz 4, auto), `tblW 10387 dxa`, **`tblInd 392`**, sin `tblLayout fixed` (autofit), `tblLook 04A0`.
  - `tblGrid` **8 columnas: 482 / 2497 / 1130 / 1130 / 1156 / 1130 / 1130 / 1732** = 10 387 dxa.
  - **25 filas** (1 encabezado + 24 ítems), `trHeight val=263` (at-least), cada celda `noWrap` + `hideMark` en las filas 0-23. Sin merges ni sombreado. No hay `tblHeader` (el encabezado **no se repite** al cambiar de página; así se ve en los escaneos).
  - Encabezado: "Nº | Ítem | Suficiencia | Relevancia | Coherencia | Claridad | Redacción | Observaciones" en **negrita 9 pt**, `TableParagraph`, `ind left 80`, `before=31`.
  - Celdas de ítem: Nº 9 pt (no justificado, `Normal`); texto del ítem `jc=both`, 9 pt (hereda `TableParagraph` en fila 1, `Normal` en el resto: diferencia de estilo sin efecto visual); celdas de criterio y observaciones **vacías** (aquí el experto escribe a mano 1-4).
  - La tabla excede el margen derecho: borde izquierdo en 283+392 = 675 dxa y borde derecho en 675+10 387 = 11 062; el margen derecho de página termina en 11 920-1430 = 10 490 (sobresale ≈ 572 dxa = 1.0 cm). Es parte de lo que se ve en los escaneos (la tabla ocupa casi todo el ancho).
- Cierre: 6-7 párrafos vacíos (`before=150`), línea de firma `        ____________________________` (28 guiones bajos) tras 4 tabuladores (10 pt), "Firma" (10 pt, centrado, `ind right 846`, `line=360`), "DNI: ……………………….." (10 pt, centrado, `ind right 851`). Un párrafo vacío final con `ind right 851`.
- Salto de página explícito (`w:br type=page`, párrafo de 10 pt) entre constancias.

### 2.2 DOCX 2 - CORRECION DE FORMATOS
- 1 sección: pgSz 11920 x 16850; márgenes top 1701, right 1430, **bottom 280**, left 283; header/footer 0/0 (idénticos a S5 del DOCX 1). Un header/footer vacío.
- Contenido: 3 bloques idénticos al de la constancia del DOCX 1 (mismo `Ttulo1`, mismo párrafo `line=360`, misma tabla 25x8 con **los mismos anchos 482/2497/1130/1130/1156/1130/1130/1732**, misma firma), separados por `w:br page`.
- Diferencia clave respecto a la "constancia en blanco" del DOCX 1: los campos del experto vienen **pre-escritos** y subrayados (`u`; los nombres en negrita+subrayado), y los puntos suspensivos se sustituyen por runs subrayados con espacios (que reproducen la línea de puntos). En la de Ramos, el campo "con Grado de ...." se reemplazó por ", con 07 años de experiencia de enseñanza en el Centro Preuniversitario UNAJMA" y se agregó ":" tras "tesistas".
- Texto de la declaración idéntico en las 3 (salvo lo anterior). Las 24 filas de ítems son idénticas a las del DOCX 1 (con un salto de línea interno en el ítem 1 de Ramos).

### 2.3 PDF - EJEMPLO DE PUNTUACION DE VALIDACION (14 págs, texto digital)
- Membrete repetido en cada pág.: línea 1 "Universidad Nacional José María Arguedas – Escuela de Posgrado" (cursiva), línea 2 "Maestría en Ingeniería de Sistemas, mención Tecnologías de la Información y Comunicación" (cursiva, negrita); pie "Dr. Enrique Edgardo Condor Tinoco" (cursiva, alineado a la derecha). Tipografía sans-serif tipo Calibri/Candara; no es el formato de las constancias.
- Pág. 1: título "Validez de instrumento", "Caso práctico: Desarrollo del análisis de la validez de instrumento paso a paso", "Asignatura: Diseño y Desarrollo del Trabajo de Investigación"; §1 tabla técnicas/instrumentos/validez/confiabilidad. Págs. 1-3: §2 operacionalización ABCD (tabla de 6 columnas + nota sobre columna "tipo de indicador"). Págs. 3-4: §3 población por dimensión. Págs. 4-7: §4 instrumentos 1-4 (con columnas Nº | Ítem | Dimensión | Indicador | Escala). Págs. 7-9: §5 validez por promedios (3 expertos, criterios C, R, Co, escala 1-4 "Deficiente/Regular/Bueno/Muy bueno", umbral 3.3). Págs. 9-11: §6 IVC (binario 3-4=1; 1-2=0; Tristán 2008; IVC >= 0.58; tabla N expertos 3/4/5 -> 0.58/0.75/0.78; fórmula IVC por ítem = nº de expertos que marcaron 3 o 4 / total de expertos, como imagen). Págs. 11-14: §7 IVC con los 5 criterios (Suficiencia, Relevancia, Coherencia, Claridad, Redacción), tabla de 5 ítems x 5 criterios x 3 expertos, codificación binaria, IVC por ítem (promedio de criterios), IVC total.

### 2.4 PDFs escaneados de constancias firmadas (Soria, Minaya: 4 págs; Ramos: 3 págs; Consolidado: 9 págs)
Descripción visual verificada (render 110 dpi de Ramos p.1-3, Soria p.1-2 y 4, Minaya p.1 y 4, Consolidado p.1; miniaturas del consolidado completo). Papel con marca "Escaneado con CamScanner" en el pie de cada imagen (no es parte del formato).
- **Soria/Minaya p.1 - Instrucciones:** coincide con S4 del DOCX 1 (título centrado en negrita, 5 puntos numerados, lista de criterios, escala, tabla rúbrica 3 columnas con bordes negros, "Agradecemos profundamente su colaboración." en negrita). Texto en TNR serif. Ramos no incluye esta hoja.
- **Constancia, pág. 1 de 3:** título centrado en negrita 2 líneas; párrafo "Quien suscribe, … con DNI Nº …, de profesión … con Grado de …, por medio…" con los datos a mano (bolígrafo azul) sobre líneas de puntos; tabla con encabezado en negrita ("Nº, Ítem, Suficiencia, Relevancia, Coherencia, Claridad, Redacción, Observaciones"), ítems 1-9 completos y el 10 cortado al pie.
- **Pág. 2:** continuación sin encabezado de tabla repetido (empieza en la 2.ª parte del ítem 10 "adicional de estudio porque existen cursos que requieren mayor dedicación") hasta el ítem 21.
- **Pág. 3 (4.ª en Soria/Minaya):** ítems 22-24 y debajo, **a mano y con sello**: sello azul UNAJMA (escudo + "UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS" + nombre y grado impreso del docente + "DOCENTE") estampado sobre la firma manuscrita, línea "Firma", y "DNI: ….." con el número a mano sobre los puntos. En Ramos el sello dice "UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS" y el DNI es manuscrito sobre la línea.
- En todos los casos: los 5 criterios llenados a mano con dígitos 3/4; **columna Observaciones vacía**; sin fecha, sin lugar, sin veredicto, sin CIP, sin casilla alguna.
- Los ítems impresos en los escaneos (p. ej. ítem 1 "Me preocupo por la presentación de mis trabajos de los cursos.", ítem 2 "Establezco metas a corto plazo (diarias o semanales) así como metas a largo plazo (mensuales o para el ciclo).", ítem 5 "Me esfuerzo por mantener un alto nivel de calidad en todas mis tareas.") **difieren de los del DOCX** (ver sección 6, A-5).

### 2.5 PDF - Cuestionario (instrumento sometido a juicio, 11 págs)
Impresión de Google Forms: pág. 1 banner fotográfico, título "Cuestionario para identificar el nivel de autoaprendizaje en estudiantes del Centro Pre Universitario – UNAJMA", correo del usuario, "* Indica que la pregunta es obligatoria", encabezado "Items para identificar el nivel de autoaprendizaje", párrafo de presentación, "Instrucciones: Lee cada afirmación y marca con una X…" con tabla de escala (Siempre 5 / A menudo 4 / A veces 3 / Rara vez 2 / Nunca 1). Después 24 ítems, uno por tarjeta, con 5 radio buttons (Siempre … Nunca), agrupados por secciones: "Nivel motivacional: Establecimiento de metas" (1-3/5), "Nivel contextual: Estructuración del ambiente", "Nivel contextual: Gestión del tiempo", "Nivel cognitivo: Estrategias resolutivas", "Nivel conductual: Búsqueda de ayuda", "Nivel conductual: Autoevaluación". Última pág.: botones Atrás/Enviar/Borrar formulario y pie de Google. Es un formato web, no es plantilla Word.

---

## 3 Texto literal de cada formato

> Se transcribe exactamente como figura (incluidas las erratas, marcadas con `[sic]` solo cuando aporta). `⟦…⟧` = campo variable. `[TAB]` = tabulador. Tipografía y negritas indicadas en la sección 2.

### 3.1 Carta de solicitud al experto (3 copias; solo cambia el destinatario)

```
                                                              Andahuaylas, …… de[TAB punteado]de 2025

Señor (a):
⟦Carta 1: M.SC. IVAN SORIA SOLIS | Carta 2: Mag. Daniel Minaya Gutiérrez | Carta 3: ……………………………………………………………………………⟧
    Docente de la Escuela Profesional de Ingeniería de Sistemas      (Carta 3: Docente del Centro Preuniversitario “UNAJMA”)

De nuestra mayor consideración:

[NEGRITA] Nosotras, Guadalupe Lida Sihui Llacctarimay con DNI N° 70233314 y Miriam Velasque Ccorisoncco con DNI N° 76189071, tesistas del Programa de Maestría en Ingeniería de Sistemas con mención en Tecnologías de la Información y Comunicación, nos dirigimos a usted con el debido respeto y nos presentamos y exponemos:

[NEGRITA] Dada su experiencia profesional y méritos académicos, recurrimos a su honorable persona para solicitarle su inapreciable colaboración como experto para la validación del instrumento de nuestra investigación que adjuntamos como anexo al presente, del trabajo de investigación intitulado “MODELO PREDICTIVO CON MACHINE LEARNING PARA IDENTIFICAR EL NIVEL DE AUTOAPRENDIZAJE EN ESTUDIANTES DEL CENTRO PRE-UNIVERSITARIO, ANDAHUAYLAS - 2025”; para obtener el grado de Magister en Ingeniería de Sistemas con mención en Tecnologías de la Información y Comunicación, sus observaciones y recomendaciones como juez de validación serán de gran ayuda para perfeccionar los instrumentos de investigación.

Presentamos los siguientes documentos:
  •  Matriz de validez de instrumento
  •  Matriz de consistencia
  •  Tabla de operacionalización de variables
  •  Instrumento N° 1 Cuestionario para identificar el nivel de autoaprendizaje en estudiantes del Centro Pre Universitario – UNAJMA

    Nos despedimos de Ud. reiterándole mis saludos y del mismo modo agradeciéndole por su debida atención a la presente.

                                       Atentamente,

        ……………………………………….…             ……………………………………….…
                            Guadalupe Lida Sihui Llacctarimay                    Miriam Velasque Ccorisoncco
                                                Tesista                                                                Tesista
                                            DNI N° 70233314                                                    DNI N° 76189071
```
(Los dos párrafos largos aparecen en negrita en el XML; el resto en normal. Erratas del modelo: "Nosotras … mis saludos" mezcla 1.ª plural/singular, "Magister".)

### 3.2 Hoja de instrucciones

```
                      INSTRUCCIONES PARA VALIDACIÓN DEL INSTRUMENTO         [negrita, centrado]
Las instrucciones para la validación del instrumento son las siguientes:
1. En la “constancia de validación de contenido del instrumento por ítem” usar los siguientes criterios
      Suficiencia
      Relevancia
      Coherencia
      Claridad
      Redacción
2. En la “constancia de validación de contenido del instrumento por ítem” y “constancia de validación de contenido global del instrumento”, usar las siguientes escalas de valoración para calificar a cada criterio:
      4 = Cumple completamente, 3 = Cumple adecuadamente, 2 = Cumple parcialmente, 1 = No cumple
3. La siguiente tabla muestra los criterios e indicadores que se tendrán en cuenta en la “constancia de validación de contenido del instrumento por ítem”
   [TABLA RÚBRICA - ver 3.3]
4. Si considera que algún ítem tiene alguna observación, anote en la columna correspondiente.
5. Devuelva la ficha completa al investigador.
Agradecemos profundamente su colaboración.      [negrita]
```

### 3.3 Tabla rúbrica (3 columnas; 1 encabezado + 5 criterios)

| Criterios | Descripción | Indicadores |
|---|---|---|
| **Suficiencia** | ¿El ítem abarca suficientemente el contenido? | **1** = El ítem no es suficientes para medir el indicador. / **2** = El ítem mide algún aspecto del indicador, pero no corresponden a la dimensión / **3** = El ítem podría modificarse para poder contribuir completamente a la evaluación de la dimensión. / **4** = El ítem es suficientes. |
| **Relevancia** | ¿El ítem es pertinente para la variable? | **1** = El ítem puede ser eliminado sin que se vea afectada la medición de la dimensión. / **2** = El ítem tiene poca relevancia / **3** = El ítem es relativamente importante / **4** = El ítem es muy relevante y debe ser considerado. |
| **Coherencia** | ¿El ítem está alineado con los objetivos y dimensiones? | **1** = El ítem no tiene relación lógica con la dimensión. / **2** = El ítem tiene una relación tangencial con la dimensión / **3** = El ítem tiene una relación moderada con el indicador que está midiendo. / **4** = El ítem se encuentra completamente relacionado con el indicador que está midiendo. |
| **Claridad** | ¿El ítem es comprensible? | **1** = El ítem no está claro. / **2** = El ítem requiere muchas modificaciones / **3** = El ítem requiere una modificación muy específica de algunos de los términos / **4** = El ítem es claro y se entiende |
| **Redacción** | ¿El ítem está correctamente redactado? | **1** = La redacción del ítem no es adecuada. / **2** = La redacción del ítem tiene que ser mejorada en su sintaxis. / **3** = La redacción del ítem podría ser mejorado en la semántica. / **4** = La redacción es entendible y adecuada. |

Encabezado de la tabla: "Criterios | Descripción | Indicadores". Cabecera en negrita; "n =" en negrita en la columna 3. En el docx hay tabuladores dentro de "¿El ítem está alineado con los objetivos\ty dimensiones?" y de "¿El\títem\testá correctamente redactado?" (artefacto de justificado; el texto se lee con espacios).

### 3.4 Constancia de validación de contenido del instrumento por ítem

```
        CONSTANCIA DE VALIDACIÓN DE CONTENIDO DEL INSTRUMENTO POR ÍTEM            [negrita 14 pt, centrado, 2 líneas]

   Quien suscribe, ………………………………………………………………, con DNI Nº………………, de profesión…………………………………………………………. con Grado de ..…...………………………………………………………………………., por medio de la presente hago constar que he revisado con fines de validación el instrumento de recolección de datos Cuestionario para identificar el nivel de autoaprendizaje en estudiantes del Centro Pre Universitario – UNAJMA del proyecto de investigación “MODELO PREDICTIVO CON MACHINE LEARNING PARA IDENTIFICAR EL NIVEL DE AUTOAPRENDIZAJE EN ESTUDIANTES DEL CENTRO PRE-UNIVERSITARIO, ANDAHUAYLAS - 2025” para los efectos de su aplicación, presentado por las tesistas Miriam Velasque Ccorisoncco y Guadalupe Lida Sihui Llacctarimay. Luego revisar el instrumento, puedo formular las siguientes apreciaciones:

 ┌────┬──────────────┬────────────┬───────────┬───────────┬─────────┬───────────┬───────────────┐
 │ Nº │ Ítem         │ Suficiencia│ Relevancia│ Coherencia│ Claridad│ Redacción │ Observaciones │
 ├────┼──────────────┼────────────┼───────────┼───────────┼─────────┼───────────┼───────────────┤
 │ 1…24 │ ⟦texto del ítem⟧ │            │           │           │         │           │               │
 └────┴──────────────┴────────────┴───────────┴───────────┴─────────┴───────────┴───────────────┘

                                  ____________________________
                                              Firma
                                      DNI: ………………………..
```
Variante en DOCX 2 / PDFs: Soria = "IVAN SORIA SOLIS … con DNI Nº 40725333, de profesión Ingeniero Informático y de Sistemas con Grado de Magister Scientiae en Informática"; Minaya = "DANIEL MINAYA GUTIÉRREZ … DNI 44254814 … Ingeniero Informático y de Sistemas … Magister"; Ramos = "JAVIER RAMOS GONZALES, con DNI Nº 44844286, de profesión Ingeniero de Sistemas, con 07 años de experiencia de enseñanza en el Centro Preuniversitario UNAJMA por medio de la presente…" y "presentado por las tesistas:" con dos puntos. Frase errata: "Luego revisar el instrumento" (falta "de"). En DOCX 2 los campos del experto están en un run subrayado (nombre también en negrita).

Ítems del modelo (24, del DOCX; difieren en 1, 2, 5 y orden 20/21 de los escaneos y del Google Forms):
1 Me esfuerzo por mantener un orden en mis estudios para acercarme a mis objetivos preuniversitarios. - 2 Me organizo con metas claras para lograr ingresar a la universidad. - 3 Mantengo un alto nivel de aprendizaje en mis cursos. - 4 Establezco metas para ayudarme a administrar el tiempo de estudio de mis cursos. - 5 Mantengo un alto nivel de compromiso en mis estudios para lograr mi ingreso a la universidad. - 6 Elijo el lugar donde estudio para evitar demasiadas distracciones. - 7 Encuentro un lugar cómodo para estudiar. - 8 Sé dónde puedo estudiar de manera más eficiente para los cursos. - 9 Elijo un momento con pocas distracciones para estudiar para mis cursos. - 10 Organizó tiempo adicional de estudio porque existen cursos que requieren mayor dedicación. - 11 Intento agendar un tiempo de estudio cada día a la misma hora o de forma semanal y siempre miro mi horario. - 12 A pesar de tener clases todos los días, administro mi tiempo para estudiar por mi cuenta. - 13 Intento tomar notas más detalladas durante las clases ya que las considero esenciales para estudiar después. - 14 Utilizo la lectura en voz alta como estrategia para evitar distracciones mientras estudio lo visto en clase. - 15 Organizo mis preguntas previamente para participar activamente en clase. - 16 Resuelvo ejercicios adicionales por iniciativa propia para dominar el contenido del curso. - 17 Pregunto a alguien que tenga conocimientos sobre el contenido del curso para que pueda consultar con él o ella cuando necesite ayuda. - 18 Comparto mis problemas con mis compañeros de clase, para identificar nuestras dificultades y sepamos cómo solucionar nuestros problemas (académicos). - 19 Me esfuerzo por coordinar reuniones en persona con mis compañeros cuando lo considero útil para mi aprendizaje. - 20 Sintetizo los contenidos del curso por mi cuenta para evaluar qué tanto he comprendido. - 21 Soy constante al solicitar orientación de un docente cuando la necesito. - 22 Me formulo preguntas mientras estudio para profundizar en el contenido del curso. - 23 Converso con mis compañeros en clase para comparar y verificar mi progreso académico. - 24 Me comunico con mis compañeros para saber qué estoy aprendiendo, diferente de lo que ellos están aprendiendo.

### 3.5 PDF de ejemplo del Dr. Cóndor - textos normativos literales relevantes

- Escala (§5, método de promedios): "Escala de valoración: 1 = Deficiente, 2 = Regular, 3 = Bueno, 4 = Muy bueno". Criterios en §5: "Claridad (C): ¿El ítem está redactado claramente? / Relevancia (R): ¿El ítem es pertinente respecto al objetivo del instrumento? / Coherencia (Co): ¿El ítem es coherente con el indicador y la dimensión que pretende medir?". "Todos los ítems superan el puntaje promedio de 3.3 por criterio, considerado como valor mínimo aceptable."
- §6: "Se considera “válido” el ítem si fue calificado con 3 o 4. → se codifica como 1 / Se considera “no válido” si fue calificado con 1 o 2. → se codifica como 0". Escala de relevancia: "1 No relevante, 2 Poco relevante, 3 Bastante relevante, 4 Muy relevante (esencial)".
- "Criterio de aceptación (Lawshe modificado para 3 expertos): Según el método de Lawshe modificado por Tristán (2008), con 3 expertos, un ítem debe alcanzar un IVC ≥ 0.58 para considerarse válido."
- Fórmula impresa (imagen): "IVC por ítem = Número de expertos que marcaron 3 o 4 / Total de expertos"; ejemplo "IVC₂ = (1+0+1)/3 = 2/3 = 0.67". "IVC total = (1.00+0.67+1.00+0.67+1.005) / 5 = 4.345/ 5 = 0.87" [sic, "1.005" por "1.00" ÷5].
- Tabla "N° Expertos / IVC mínimo aceptable": 3 -> ≥ 0.58; 4 -> ≥ 0.75; 5 -> ≥ 0.78. "Con 3 expertos, un ítem necesita al menos 2 expertos que lo califiquen con 3 o 4 para ser aceptado (2/3 = 0.67)."
- §7: "Supongamos que tenemos 5 ítems evaluados en los 5 criterios por los 3 expertos"; "IVC por ítem (promedio de los criterios por ítem)"; "IVC del instrumento completo… 0.892, lo cual indica muy alta validez de contenido… Ítem 2 tiene un IVC de 0.53, por debajo del umbral. Según los criterios, debería ser revisado, reformulado o eliminado."
- El PDF **no contiene** Aiken ni el umbral 0.80.

### 3.6 Cuestionario (instrumento) - cabecera literal (p.1)
"Items para identificar el nivel de autoaprendizaje / Este cuestionario busca conocer tus percepciones, actitudes y comportamientos frente al autoaprendizaje. No hay respuestas correctas o incorrectas; responde con sinceridad según tu experiencia. La información será confidencial y usada solo con fines académicos. / Instrucciones: Lee cada afirmación y marca con una X la opción que mejor refleje tu opinión. Tomando en cuenta la siguiente escala de valores: [Siempre 5 | A menudo 4 | A veces 3 | Rara vez 2 | Nunca 1]".

---

## 4 Campos manuscritos (experto/tesista) vs texto fijo del formato

### 4.1 Carta de solicitud
| Elemento | Naturaleza | Detalle |
|---|---|---|
| "Andahuaylas, …… de [punteado] de 2025" | **Manuscrito/completable** | día y mes con puntos de relleno (tab dot leader pos 9426). Año "2025" y "Andahuaylas" son fijos |
| "Señor (a):" / grado y nombre / cargo | **Fijo por carta** (el destinatario cambia; en la 3.ª queda en puntos) | |
| Presentación (tesistas, DNI, programa), título de tesis, grado a optar | **Fijo** (datos del proyecto) | cambia al adaptar a SIVAC |
| Lista de 4 adjuntos | **Fijo** | |
| "……………………….…   ……………………….…" | **Firma manuscrita** de las 2 tesistas (líneas de puntos) | |
| Nombres, "Tesista", "DNI N° …" | **Fijo** (impreso) | |

### 4.2 Hoja de instrucciones
Todo **fijo**. No tiene campos. (En el escaneo no hay marcas manuales.)

### 4.3 Constancia por ítem
| Elemento | Naturaleza | Detalle |
|---|---|---|
| "Quien suscribe, ………" | **Manuscrito del experto**: nombres y apellidos | línea de puntos tras "suscribe," |
| "con DNI Nº ………" | **Manuscrito**: DNI | |
| "de profesión ………" | **Manuscrito**: profesión | |
| "con Grado de ………" | **Manuscrito**: grado académico | (no hay campo CIP, ni universidad, ni cargo, ni años de experiencia, salvo la variante Ramos) |
| Nombre del instrumento, título del proyecto, tesistas, "Luego revisar el instrumento, puedo formular las siguientes apreciaciones:" | **Fijo** (cambia por proyecto/instrumento) | |
| Columna "Nº" y columna "Ítem" | **Fijo** (impreso) | 24 filas en el modelo |
| Columnas Suficiencia / Relevancia / Coherencia / Claridad / Redacción | **Manuscrito del experto**: dígito 1-4 por celda (en las 120 celdas; 24 ítems x 5 criterios) | celdas vacías, 1130/1156 dxa de ancho |
| Columna "Observaciones" | **Manuscrito del experto** (opcional; vacía en los 72 renglones de las 3 constancias reales) | 1732 dxa |
| "____________________________ / Firma" | **Firma manuscrita** + **sello institucional** estampado en el escaneo (nombre, grado, "DOCENTE", escudo UNAJMA) | el sello no está en el Word; lo pone el experto o la oficina |
| "DNI: ………………………" | **Manuscrito**: DNI al pie de la firma | |
| Fecha, lugar, veredicto, CIP, constancia global | **No existen** en el formato original | |

---

## 5 Lógica del XLSX (`PUNTUACION IVC.xlsx`)

- **Hojas:** `Hoja1` (B2:N125) y `Hoja2` (B2:H122). Sin hojas ocultas, sin formato condicional, sin validación de datos, sin paneles inmovilizados, sin color de pestaña. Fuente Aptos Narrow 11, sin rellenos de color.
- **Hoja1, bloque A (B-F):** encabezados B2 "Item", C2 "Criterio", D2 "Experto 1 Ivan", E2 "Experto 2 Daniel", F2 "Experto 3 Javier" (negrita). Filas 3-122 = **24 ítems x 5 criterios** (cada ítem ocupa 5 filas; B combinado B3:B7, B8:B12, …, B118:B122, centrado). Criterio en C: "Suficiencia ", "Relevancia", "Coherencia", "Claridad", "Redacción " (con espacio final en 2 de ellos). Valores D:F = calificaciones **tipeadas** 1-4 (distribución real: 260 cuatros y 100 treses; ningún 1 ni 2). Bordes finos con borde superior medio al inicio.
- **Hoja1, bloque B (H-N):** H "Item" (combinado H3:H7, etc.), I "Criterio", **J2:L2 combinado "Codificacion binaria"**, M "Suma", N "IVC por criterio".
  - J:L (binarización por juez): **valores constantes 0/1 escritos a mano** (no fórmula). Se verificó que coinciden con `=IF(D>=3,1,0)` en las 360 celdas (0 discrepancias), pero la lógica no está en el archivo.
  - M3:M122: **`=SUM(Jn:Ln)`** (120 fórmulas).
  - N3:N122: **`=Mn/3`** (120 fórmulas). Divisor 3 codificado a mano (acopla el archivo a N=3 jueces).
  - **H125:I125: "IVC total" = `=24/24`** (valor fijo 1; NO es promedio). No existe IVC por ítem (promedio de sus 5 criterios) ni el IVC total como `=AVERAGE(N3:N122)`.
- **Hoja2:** copia estructural del bloque B (D2:F2 combinado "Codificacion binaria", G "Suma", H "IVC por criterio") **sin fórmulas**; H3:H122 precargado con el valor 1 (constante), D:G vacíos. Sirve de "reporte consolidado" pero es estático.
- **Umbrales:** el XLSX **no contiene ningún umbral** (ni 0.58 ni 0.80), ni V de Aiken, ni veredicto. Los umbrales de Tristán (2008) están solo en el PDF de ejemplo (3 jueces ≥ 0.58; 4 ≥ 0.75; 5 ≥ 0.78) y la aceptación de promedio por criterio > 3.3. V de Aiken no figura en ningún archivo del modelo.
- **Resultado numérico del modelo:** como todas las notas son 3 o 4, los 120 IVC por criterio = 1.00 (el IVC total 1.00 coincide por azar con el `=24/24`).
- **Regla de cálculo del modelo (reconstruida):** `binario = 1 si nota ≥ 3`; `Suma = Σ binarios`; `IVC criterio = Suma/3`; `IVC ítem = promedio de sus 5 criterios` (PDF §7); `IVC total = promedio de IVC de ítems`; aceptación por ítem ≥ 0.58.
- **Discrepancia ya detectada (no reconfirmada por mí celda a celda):** Ramos ítem 3 aparece como 3-4-4-3-4 en el xlsx contra 4-4-3-4-4 en el escaneo firmado (según `ANALISIS_INTEGRAL`).

---

## 6 Ambigüedades y puntos que decidir

- **A-1 Saltos de página entre cartas:** S1 y S2 están marcadas `continuous`; sin LibreOffice/Word no pude renderizar el DOCX para comprobar la paginación. Recomendación: en la réplica forzar `nextPage` entre cartas (resultado visual esperado: una carta por página).
- **A-2 Sin membrete, número de página ni logo** en el DOCX (headers/footers vacíos). La réplica exacta del modelo = hoja sin membrete. Si la EPIS exige escudo/banner institucional, es una **adición** al modelo, no réplica. El agente definió en su ficha "banner de 1212x128 px" y "veredicto binario con CIP", elementos que **no existen** en los modelos reales: decidir si se añaden (se desviaría del "exactamente igual") o se respetan al milímetro.
- **A-3 Escala impresa:** las constancias y la hoja de instrucciones usan "4 = Cumple completamente, 3 = Cumple adecuadamente, 2 = Cumple parcialmente, 1 = No cumple"; el PDF de ejemplo usa "Deficiente/Regular/Bueno/Muy bueno" y "No relevante…Muy relevante". El formato oficial entregado al juez es el primero.
- **A-4 Erratas del modelo** (para réplica "exacta" vs corregida): "no es suficientes", "El ítem es suficientes", "pero no corresponden a la dimensión", "podría ser mejorado en la semántica", "Luego revisar el instrumento", "Organizó" (ítem 10), "Magister", "Nosotras … mis saludos". Decisión del tesista: mantener (réplica estricta) o corregir (recomendado por `ANALISIS_INTEGRAL` §5.1). Las instrucciones del encargo dicen "exactamente iguales"; propongo mantener la estructura y corregir únicamente la concordancia gramatical con aprobación previa.
- **A-5 Inconsistencia interna del modelo:** los ítems 1, 2, 5 y el orden 20/21 de la constancia firmada (escaneos) no coinciden con los del DOCX/Google Forms (verificado visualmente: ítem 1 y 2 y 5 distintos en Soria p.2, Minaya p.1 del consolidado y Ramos p.1). Para SIVAC la constancia debe imprimirse con la **versión final congelada** del instrumento.
- **A-6 Campos que el modelo no tiene:** fecha, lugar, veredicto/aplicabilidad, CIP, universidad de procedencia, "constancia de validación global del instrumento" (las instrucciones la mencionan en el punto 2, pero **ningún archivo la contiene**; no se puede réplica exacta de algo inexistente). Decidir si se agregan y cómo (propuesta: documento aparte, no modifica la constancia por ítem).
- **A-7 Tipo de instrumento:** el modelo valida un cuestionario de ítems de opinión. Para las fichas 1 y 2 de SIVAC (cronométrica y registro documental) la columna "Ítem" se llenaría con el campo/variable/unidad; la rúbrica de la hoja de instrucciones dice "ítem" y "variable", que sigue siendo válida pero hay que decidir si se recuerda que "ítem" = campo de registro.
- **A-8 Rigidez de anchos:** la constancia usa 8 columnas con anchos exactos 482/2497/1130/1130/1156/1130/1130/1732 y 9 pt. Con 24 ítems cabe en ~2.3 págs. (ítems de ~2 líneas). Un ítem más largo (SIVAC) crece verticalmente (`noWrap` solo afecta a celdas sin texto largo). Si SIVAC tiene un número distinto de ítems (p. ej. 10 TAM + campos de fichas) la constancia por instrumento tendrá otro número de filas: mantener 25 como "máximo" no aplica.
- **A-9 Cantidad de jueces y panel:** 3 constancias por instrumento (Soria, Minaya, Ramos en el modelo). Cada constancia se imprime una por juez (DOCX 2 = 3 hojas con datos pre-escritos). Los datos del experto (nombre, DNI, grado) pueden pre-llenarse subrayados como en `CORRECION DE FORMATOS.docx`, pero solo con datos reales confirmados por el tesista; si no, dejar los puntos suspensivos del DOCX 1.
- **A-10 Sombreado/color/checkbox/CIP:** confirmado que NO hay en el modelo; cualquier casilla de aplicabilidad o sombreado de encabezado sería una desviación.
- **A-11 Verificación visual parcial:** revisé íntegramente el texto y XML de ambos DOCX y el texto digital del PDF de ejemplo y del cuestionario; de los escaneos revisé visualmente Ramos pp.1-3, Soria pp.1, 2 y 4, Minaya pp.1 y 4, miniaturas del consolidado y el cuestionario completo, pero no transcribí los DNI manuscritos ni validé celda por celda las 360 calificaciones (no necesario para el formato en blanco).
- **A-12 Falta de LibreOffice/Word en el entorno** para comparar pixel a pixel la réplica; la verificación de la réplica debe hacerse por comparación de XML (anchos, márgenes, estilos) más revisión humana del PDF exportado desde Word.
