## 5. Defectos por tipo

| Tipo | Cantidad | Páginas afectadas |
|---|---|---|
| ROTULO_INCORRECTO | 15 | 22, 30, 68, 74, 100, 103, 116, 117, 121, 124, 126, 127, 128, 130, ... |
| TABLA_DESBORDADA | 14 | 71, 116, 118, 120, 122, 124, 126, 127, 129, 130, 143, 153, 154, 156 |
| CELDA_ILEGIBLE | 11 | 118, 120, 122, 126, 127, 129, 130, 146, 150, 153, 154 |
| TEXTO_INCOMPLETO | 10 | 2, 3, 8, 9, 115, 148, 149, 157, 158 |
| VIUDA_HUERFANA | 9 | 125, 128, 131, 141, 142, 145, 147, 151, 155 |
| EMOJI | 7 | 148, 149, 157, 158 |
| TEXTO_CORTADO | 7 | 81, 85, 86, 87, 88, 89, 96 |
| ENCABEZADO_HUERFANO | 6 | 58, 65, 91, 117, 126, 130 |
| SALTO_PAGINA_AUSENTE | 5 | 46, 58, 104, 108, 111 |
| NUMERACION_SALTADA | 3 | 35, 52 |
| DESORDEN_SECCION | 1 | 7 |
| ESPACIADO_INCORRECTO | 1 | 9 |
| TEXTO_DUPLICADO | 1 | 157 |

## 6. Defectos críticos

Se registran 10 defectos de severidad crítica. Ninguno de ellos es un error de redacción: son fallas que impiden la impresión oficial del documento o inducen a error al lector.

- **p7, encabezado** (DESORDEN_SECCION): El índice de contenido termina en REFERENCIAS BIBLIOGRÁFICAS tras el apartado 3.2: omite el 3.3 (Metodología XP, pp. 40-85), el CAPÍTULO V, el CAPÍTULO VI, CONCLUSIONES, RECOMENDACIONES y ANEXOS.
  - Corrección: Aplicar estilos Heading 1 a 3 a todos los títulos y regenerar el campo TOC.
- **p115, parrafo n.º 619** (TEXTO_INCOMPLETO): Advertencia interna impresa en el cuerpo del Capítulo V: declara que los resultados corresponden a DATOS DE PRUEBA - REEMPLAZAR (DEC-007) e incluye rutas y comandos del repositorio.
  - Corrección: Retirar la advertencia del informe final y trasladarla a una nota interna no impresa.
- **p120, tabla n.º 37** (CELDA_ILEGIBLE): La columna n mide 411 dxa (0.72 cm), la más estrecha del documento: fractura palabras y cifras (Momen to, Variació n, Median a, 1 4).
  - Corrección: Eliminar la columna n, constante igual a 14, o ensancharla a 700 dxa.
- **p127, tabla n.º 41** (CELDA_ILEGIBLE): La columna más estrecha mide 635 dxa (1.12 cm): Concordanc ia, Wilcoxo n, Rechaz ar, Gran de.
  - Corrección: Ampliar las columnas de indicador y decisión; abreviar encabezados.
- **p153, tabla n.º 52** (TABLA_DESBORDADA): Matriz de datos del pretest con 18 columnas y 15 filas: 8 981 dxa de rejilla frente a 8 765 dxa útiles (216 dxa de exceso). En el PDF arranca en x = 107.1 pt y llega a x = 528.8 pt frente al límite derecho de 523.3 pt.
  - Corrección: Reducir la rejilla a 8 765 dxa; pasar la matriz a horizontal o dividirla en dos tablas.
- **p153, tabla n.º 52** (CELDA_ILEGIBLE): Con 18 columnas el ancho medio es de 499 dxa (0.88 cm) y el mínimo de 363 dxa (0.64 cm): las cifras se fracturan hasta en cuatro líneas (3 8. 5 0), ALMACEN (CHANKA) ocupa tres líneas y las cabeceras se leen suj eto_id, centr o_aco pio, nivel_s atisfaccion.
  - Corrección: Dividir en dos tablas de 9 columnas o girar a horizontal con anchos mínimos de 700 dxa.
- **p154, tabla n.º 53** (TABLA_DESBORDADA): Matriz de datos del postest con 18 columnas y 15 filas: 8 981 dxa de rejilla frente a 8 765 dxa útiles, con el mismo desborde de 5.5 pt sobre el margen derecho.
  - Corrección: Reducir la rejilla a 8 765 dxa o pasar la matriz a orientación horizontal.
- **p154, tabla n.º 53** (CELDA_ILEGIBLE): Mismas patologías que la matriz del pretest: columna mínima de 400 dxa (0.71 cm), cifras y etiquetas partidas en varias líneas, cabeceras ilegibles.
  - Corrección: Dividir la matriz o ampliar columnas en horizontal.
- **p157, parrafo** (TEXTO_INCOMPLETO): Las cuatro cajas del Anexo 7 conservan la instrucción editorial Instrucción para el tesista: Insertar en este espacio la fotografía correspondiente a, visible en el documento final.
  - Corrección: Insertar las fotografías definitivas a 300 DPI o retirar el anexo.
- **p158, tabla n.º 58** (TEXTO_INCOMPLETO): Cuarta caja del Anexo 7 con la misma instrucción editorial y sin fotografía insertada.
  - Corrección: Insertar la fotografía definitiva o retirar la caja.

## 7. Geometría de las tablas

La rejilla se midió directamente sobre `w:tblGrid`. Se consideran desbordadas las tablas cuya suma de columnas excede la caja útil; se separa el exceso significativo (más de 25 dxa, es decir, más de 0.04 cm) del desajuste de redondeo.

| Tabla | Filas | Cols. | Rejilla dxa | Exceso dxa | Ancho medio | Col. mínima |
|---|---|---|---|---|---|---|
| T44 | 5 | 5 | 14000 | +303 | 2800 | 2800 |
| T35 | 7 | 8 | 8981 | +216 | 1122 | 1062 |
| T36 | 7 | 10 | 8981 | +216 | 898 | 682 |
| T37 | 7 | 10 | 8981 | +216 | 898 | 411 |
| T38 | 10 | 10 | 8981 | +216 | 898 | 634 |
| T39 | 8 | 8 | 8981 | +216 | 1122 | 863 |
| T40 | 5 | 9 | 8981 | +216 | 997 | 791 |
| T41 | 5 | 9 | 8981 | +216 | 997 | 635 |
| T42 | 7 | 9 | 8981 | +216 | 997 | 727 |
| T43 | 5 | 8 | 8981 | +216 | 1122 | 871 |
| T52 | 15 | 18 | 8981 | +216 | 498 | 363 |
| T53 | 15 | 18 | 8981 | +216 | 498 | 400 |
| T54 | 6 | 5 | 8981 | +216 | 1796 | 1474 |
| T17 | 10 | 5 | 8961 | +196 | 1792 | 1753 |
| T19 | 12 | 5 | 8900 | +135 | 1780 | 1753 |
| T27 | 16 | 6 | 8898 | +133 | 1483 | 1461 |
| T22 | 11 | 5 | 8895 | +130 | 1779 | 1753 |
| T14 | 10 | 5 | 8856 | +91 | 1771 | 1753 |
| T23 | 10 | 5 | 8817 | +52 | 1763 | 1753 |

Catorce tablas más presentan un exceso de 19 a 25 dxa (0.03 a 0.04 cm), atribuible al redondeo de Word al declarar el ancho de tabla: T00, T01, T02, T03, T04, T07, T13, T29, T30, T31, T32, T33, T34 y T45. Ese desajuste no recorta texto, pero conviene normalizarlo a 8 765 dxa en la misma cirugía.

### 7.1 Tablas de 10 columnas (T36, T37, T38)

Las tres tablas de la Dimensión 1 y 2 comparten la misma rejilla de 8 981 dxa con 10 columnas. El exceso de 216 dxa se reparte 0.19 cm por lado y en el PDF se materializa en un desplazamiento de 6 pt sobre el margen izquierdo y 5.5 pt sobre el derecho. La columna más comprometida es la de tamaño muestral: 682 dxa en T36, 411 dxa en T37 y 634 dxa en T38. Con 411 dxa (0.72 cm) el texto se fractura a media palabra (Momen to, Variació n, Median a, 1 4).

### 7.2 Tablas de 8 y 9 columnas (T39 a T43)

T39 (8 columnas), T40, T41 y T42 (9 columnas) y T43 (8 columnas) repiten la rejilla de 8 981 dxa. Las columnas de decisión estadística caen por debajo de 800 dxa y los encabezados se parten en tres líneas: p-valor Ajusta do Holm, Decisió n sobre H0,1, Hipótesi s de Investigació n. En T41 la columna más estrecha mide 635 dxa y en T40, 791 dxa.

### 7.3 Matriz de consistencia en horizontal (T44)

La Tabla A1.1 mide 14 000 dxa exactos (24.69 cm) sobre una caja útil de 13 697 dxa. El exceso de 303 dxa (0.53 cm) hace que la tabla sobresalga 8.25 pt por la izquierda y 7.7 pt por la derecha del área imprimible. Ninguna celda desborda su propia columna, pero el conjunto invade los márgenes laterales de la sección horizontal.

### 7.4 Matrices de datos de 18 columnas (T52 y T53)

Las matrices del pretest y del postest son el punto más débil del documento. Con 18 columnas sobre 8 981 dxa, el ancho medio es de 499 dxa (0.88 cm) y el mínimo de 363 dxa (0.64 cm) en T52 y 400 dxa (0.71 cm) en T53. Las etiquetas de centro de acopio ocupan tres líneas, las cifras se separan del entero (3 8. 5 0) y las cabeceras quedan ilegibles (suj eto_id, centr o_aco pio, nivel_s atisfaccion). La tabla arranca en x = 107.1 pt, muy lejos del margen, porque Word centra el excedente.
