# Auditoría hoja por hoja del Informe Final v04

**Documento auditado:** `salidas/documentos/informe_final_v04.docx` y su render `informe_final_v04.pdf`  
**Agente:** analista-documental (Squad A y E)  
**Fase:** F8_INTEGRACION_EDITORIAL  
**Fecha:** 2026-10-21  
**Referencia de contraste:** Fany_Tesis_Bachiller_2024.pdf (106 páginas)

---

## 1. Identificación y huella del documento

| Atributo | Valor |
|---|---|
| SHA-256 del DOCX | `134c0ecad628432356f121662adb7b41462d4e32117074a111a9fe0398094887` |
| Tamaño | 15229744 bytes (14.52 MB) |
| Páginas del PDF | 158 |
| Párrafos de nivel superior | 810 |
| Tablas | 59 |
| Imágenes en línea | 49 |
| Ecuaciones OMML | 12 |
| Tablas flotantes (w:tblpPr) | 0 |
| Filas con cantSplit | 462 |
| Filas con tblHeader | 54 |
| Secciones | 5 (la 3.ª horizontal) |
| Páginas horizontales | 143, 144 y 145 |

## 2. Método

Se renderizaron las 158 páginas del PDF a 110 DPI con PyMuPDF (`salidas/reportes_maquetacion/auditoria_v04/p001.png` a `p158.png`), se inspeccionó cada página y se cruzó el resultado visual con el paquete OpenXML (`document.xml`, `styles.xml`, `numbering.xml`). La geometría se midió sobre la rejilla real de cada tabla (`w:tblGrid/w:gridCol`) y sobre las cajas de dibujo del PDF, comparándolas con la caja útil impresa:

- Márgenes declarados: izquierdo 1 701 dxa (3.0 cm), derecho, superior e inferior 1 440 dxa (2.54 cm).
- Caja útil vertical: 11 906 - 1 701 - 1 440 = **8 765 dxa** (15.46 cm).
- Caja útil horizontal: 16 838 - 1 701 - 1 440 = **13 697 dxa** (24.16 cm).
- En el PDF: límite izquierdo x = 85.05 pt, límite derecho x = 523.3 pt (vertical) y x = 769.92 pt (horizontal).

Convención de nombres: en la prosa de este informe, «Tabla N» y «Figura N» aluden al rótulo impreso en el documento; en el JSON, el campo `indice_docx` de una tabla remite al índice del volcado `informe_final_v04_texto_plano.md` (`[TABLA 0]` a `[TABLA 58]`), que coincide con la numeración de trabajo usada en esta auditoría. Ambos valores se conservan para permitir la trazabilidad doble.

Esquema de folios contrastado: páginas 1-3 sin folio (portada, acta, declaración); páginas 4-12 en romanos minúsculas ii-x; páginas 13-158 en arábigos 1-146, reiniciados en la Introducción y continuos hasta el final.

Posición medida del folio: en las 158 páginas el número se alinea a la derecha del encabezado (x = 505 a 526 pt, y = 36 a 49 pt), tanto en romanos como en arábigos. La regla 03 del proyecto admite para los preliminares romanos «centrados o al pie» y exige el cuerpo «en la esquina superior derecha»; el desglose previo de Fany 2024 registró ambos folios al pie derecho. Se marca como [VERIFICAR] con el tesista y no se computa como defecto, porque ambas convenciones se aceptan en la UNAJMA.

## 3. Veredicto global

| Métrica | Valor |
|---|---|
| Páginas revisadas | 158 |
| Páginas CONFORMES | 99 |
| Páginas OBSERVADAS | 59 |
| Defectos registrados | 90 |
| Críticos | 10 |
| Altos | 63 |
| Medios | 10 |
| Bajos | 7 |
| Esquema de folios | CONFORME en las 158 páginas |
| Orden canónico de secciones | CONFORME |

El orden canónico de la tesis se cumple sin inversiones: Portada, Acta, Declaración jurada, Dedicatoria, Agradecimientos, Índice de contenido, Índice de figuras, Índice de tablas, Resumen, Abstract, Chumasqa, Introducción, Capítulos I a VI, Conclusiones, Recomendaciones, Referencias y Anexos 1 a 7. Las deficiencias detectadas son de rotulación, numeración, geometría tabular y control de viudas, no de arquitectura capitular.

## 4. Registro página por página

| Pág. | Folio | Orientación | Esquema | Folio correcto | Defectos | Veredicto |
|---|---|---|---|---|---|---|
| 1 | - | vertical | sin folio | sí | 0 | CONFORME |
| 2 | - | vertical | sin folio | sí | 1 | OBSERVADA |
| 3 | - | vertical | sin folio | sí | 1 | OBSERVADA |
| 4 | ii | vertical | romano | sí | 0 | CONFORME |
| 5 | iii | vertical | romano | sí | 0 | CONFORME |
| 6 | iv | vertical | romano | sí | 0 | CONFORME |
| 7 | v | vertical | romano | sí | 1 | OBSERVADA |
| 8 | vi | vertical | romano | sí | 1 | OBSERVADA |
| 9 | vii | vertical | romano | sí | 2 | OBSERVADA |
| 10 | viii | vertical | romano | sí | 0 | CONFORME |
| 11 | ix | vertical | romano | sí | 0 | CONFORME |
| 12 | x | vertical | romano | sí | 0 | CONFORME |
| 13 | 1 | vertical | arábigo | sí | 0 | CONFORME |
| 14 | 2 | vertical | arábigo | sí | 0 | CONFORME |
| 15 | 3 | vertical | arábigo | sí | 0 | CONFORME |
| 16 | 4 | vertical | arábigo | sí | 0 | CONFORME |
| 17 | 5 | vertical | arábigo | sí | 0 | CONFORME |
| 18 | 6 | vertical | arábigo | sí | 0 | CONFORME |
| 19 | 7 | vertical | arábigo | sí | 0 | CONFORME |
| 20 | 8 | vertical | arábigo | sí | 0 | CONFORME |
| 21 | 9 | vertical | arábigo | sí | 0 | CONFORME |
| 22 | 10 | vertical | arábigo | sí | 1 | OBSERVADA |
| 23 | 11 | vertical | arábigo | sí | 0 | CONFORME |
| 24 | 12 | vertical | arábigo | sí | 0 | CONFORME |
| 25 | 13 | vertical | arábigo | sí | 0 | CONFORME |
| 26 | 14 | vertical | arábigo | sí | 0 | CONFORME |
| 27 | 15 | vertical | arábigo | sí | 0 | CONFORME |
| 28 | 16 | vertical | arábigo | sí | 0 | CONFORME |
| 29 | 17 | vertical | arábigo | sí | 0 | CONFORME |
| 30 | 18 | vertical | arábigo | sí | 1 | OBSERVADA |
| 31 | 19 | vertical | arábigo | sí | 0 | CONFORME |
| 32 | 20 | vertical | arábigo | sí | 0 | CONFORME |
| 33 | 21 | vertical | arábigo | sí | 0 | CONFORME |
| 34 | 22 | vertical | arábigo | sí | 0 | CONFORME |
| 35 | 23 | vertical | arábigo | sí | 1 | OBSERVADA |
| 36 | 24 | vertical | arábigo | sí | 0 | CONFORME |
| 37 | 25 | vertical | arábigo | sí | 0 | CONFORME |
| 38 | 26 | vertical | arábigo | sí | 0 | CONFORME |
| 39 | 27 | vertical | arábigo | sí | 0 | CONFORME |
| 40 | 28 | vertical | arábigo | sí | 0 | CONFORME |
| 41 | 29 | vertical | arábigo | sí | 0 | CONFORME |
| 42 | 30 | vertical | arábigo | sí | 0 | CONFORME |
| 43 | 31 | vertical | arábigo | sí | 0 | CONFORME |
| 44 | 32 | vertical | arábigo | sí | 0 | CONFORME |
| 45 | 33 | vertical | arábigo | sí | 0 | CONFORME |
| 46 | 34 | vertical | arábigo | sí | 1 | OBSERVADA |
| 47 | 35 | vertical | arábigo | sí | 0 | CONFORME |
| 48 | 36 | vertical | arábigo | sí | 0 | CONFORME |
| 49 | 37 | vertical | arábigo | sí | 0 | CONFORME |
| 50 | 38 | vertical | arábigo | sí | 0 | CONFORME |
| 51 | 39 | vertical | arábigo | sí | 0 | CONFORME |
| 52 | 40 | vertical | arábigo | sí | 2 | OBSERVADA |
| 53 | 41 | vertical | arábigo | sí | 0 | CONFORME |
| 54 | 42 | vertical | arábigo | sí | 0 | CONFORME |
| 55 | 43 | vertical | arábigo | sí | 0 | CONFORME |
| 56 | 44 | vertical | arábigo | sí | 0 | CONFORME |
| 57 | 45 | vertical | arábigo | sí | 0 | CONFORME |
| 58 | 46 | vertical | arábigo | sí | 2 | OBSERVADA |
| 59 | 47 | vertical | arábigo | sí | 0 | CONFORME |
| 60 | 48 | vertical | arábigo | sí | 0 | CONFORME |
| 61 | 49 | vertical | arábigo | sí | 0 | CONFORME |
| 62 | 50 | vertical | arábigo | sí | 0 | CONFORME |
| 63 | 51 | vertical | arábigo | sí | 0 | CONFORME |
| 64 | 52 | vertical | arábigo | sí | 0 | CONFORME |
| 65 | 53 | vertical | arábigo | sí | 1 | OBSERVADA |
| 66 | 54 | vertical | arábigo | sí | 0 | CONFORME |
| 67 | 55 | vertical | arábigo | sí | 0 | CONFORME |
| 68 | 56 | vertical | arábigo | sí | 1 | OBSERVADA |
| 69 | 57 | vertical | arábigo | sí | 0 | CONFORME |
| 70 | 58 | vertical | arábigo | sí | 0 | CONFORME |
| 71 | 59 | vertical | arábigo | sí | 0 | CONFORME |
| 72 | 60 | vertical | arábigo | sí | 0 | CONFORME |
| 73 | 61 | vertical | arábigo | sí | 1 | OBSERVADA |
| 74 | 62 | vertical | arábigo | sí | 1 | OBSERVADA |
| 75 | 63 | vertical | arábigo | sí | 0 | CONFORME |
| 76 | 64 | vertical | arábigo | sí | 0 | CONFORME |
| 77 | 65 | vertical | arábigo | sí | 0 | CONFORME |
| 78 | 66 | vertical | arábigo | sí | 0 | CONFORME |
| 79 | 67 | vertical | arábigo | sí | 0 | CONFORME |
| 80 | 68 | vertical | arábigo | sí | 0 | CONFORME |
| 81 | 69 | vertical | arábigo | sí | 1 | OBSERVADA |
| 82 | 70 | vertical | arábigo | sí | 0 | CONFORME |
| 83 | 71 | vertical | arábigo | sí | 0 | CONFORME |
| 84 | 72 | vertical | arábigo | sí | 0 | CONFORME |
| 85 | 73 | vertical | arábigo | sí | 1 | OBSERVADA |
| 86 | 74 | vertical | arábigo | sí | 1 | OBSERVADA |
| 87 | 75 | vertical | arábigo | sí | 1 | OBSERVADA |
| 88 | 76 | vertical | arábigo | sí | 1 | OBSERVADA |
| 89 | 77 | vertical | arábigo | sí | 1 | OBSERVADA |
| 90 | 78 | vertical | arábigo | sí | 0 | CONFORME |
| 91 | 79 | vertical | arábigo | sí | 1 | OBSERVADA |
| 92 | 80 | vertical | arábigo | sí | 0 | CONFORME |
| 93 | 81 | vertical | arábigo | sí | 0 | CONFORME |
| 94 | 82 | vertical | arábigo | sí | 0 | CONFORME |
| 95 | 83 | vertical | arábigo | sí | 0 | CONFORME |
| 96 | 84 | vertical | arábigo | sí | 1 | OBSERVADA |
| 97 | 85 | vertical | arábigo | sí | 0 | CONFORME |
| 98 | 86 | vertical | arábigo | sí | 0 | CONFORME |
| 99 | 87 | vertical | arábigo | sí | 0 | CONFORME |
| 100 | 88 | vertical | arábigo | sí | 1 | OBSERVADA |
| 101 | 89 | vertical | arábigo | sí | 0 | CONFORME |
| 102 | 90 | vertical | arábigo | sí | 0 | CONFORME |
| 103 | 91 | vertical | arábigo | sí | 1 | OBSERVADA |
| 104 | 92 | vertical | arábigo | sí | 1 | OBSERVADA |
| 105 | 93 | vertical | arábigo | sí | 0 | CONFORME |
| 106 | 94 | vertical | arábigo | sí | 0 | CONFORME |
| 107 | 95 | vertical | arábigo | sí | 0 | CONFORME |
| 108 | 96 | vertical | arábigo | sí | 1 | OBSERVADA |
| 109 | 97 | vertical | arábigo | sí | 0 | CONFORME |
| 110 | 98 | vertical | arábigo | sí | 0 | CONFORME |
| 111 | 99 | vertical | arábigo | sí | 1 | OBSERVADA |
| 112 | 100 | vertical | arábigo | sí | 0 | CONFORME |
| 113 | 101 | vertical | arábigo | sí | 0 | CONFORME |
| 114 | 102 | vertical | arábigo | sí | 0 | CONFORME |
| 115 | 103 | vertical | arábigo | sí | 2 | OBSERVADA |
| 116 | 104 | vertical | arábigo | sí | 1 | OBSERVADA |
| 117 | 105 | vertical | arábigo | sí | 2 | OBSERVADA |
| 118 | 106 | vertical | arábigo | sí | 2 | OBSERVADA |
| 119 | 107 | vertical | arábigo | sí | 0 | CONFORME |
| 120 | 108 | vertical | arábigo | sí | 2 | OBSERVADA |
| 121 | 109 | vertical | arábigo | sí | 1 | OBSERVADA |
| 122 | 110 | vertical | arábigo | sí | 2 | OBSERVADA |
| 123 | 111 | vertical | arábigo | sí | 0 | CONFORME |
| 124 | 112 | vertical | arábigo | sí | 2 | OBSERVADA |
| 125 | 113 | vertical | arábigo | sí | 1 | OBSERVADA |
| 126 | 114 | vertical | arábigo | sí | 4 | OBSERVADA |
| 127 | 115 | vertical | arábigo | sí | 3 | OBSERVADA |
| 128 | 116 | vertical | arábigo | sí | 2 | OBSERVADA |
| 129 | 117 | vertical | arábigo | sí | 2 | OBSERVADA |
| 130 | 118 | vertical | arábigo | sí | 4 | OBSERVADA |
| 131 | 119 | vertical | arábigo | sí | 1 | OBSERVADA |
| 132 | 120 | vertical | arábigo | sí | 0 | CONFORME |
| 133 | 121 | vertical | arábigo | sí | 0 | CONFORME |
| 134 | 122 | vertical | arábigo | sí | 0 | CONFORME |
| 135 | 123 | vertical | arábigo | sí | 0 | CONFORME |
| 136 | 124 | vertical | arábigo | sí | 0 | CONFORME |
| 137 | 125 | vertical | arábigo | sí | 0 | CONFORME |
| 138 | 126 | vertical | arábigo | sí | 0 | CONFORME |
| 139 | 127 | vertical | arábigo | sí | 0 | CONFORME |
| 140 | 128 | vertical | arábigo | sí | 0 | CONFORME |
| 141 | 129 | vertical | arábigo | sí | 1 | OBSERVADA |
| 142 | 130 | vertical | arábigo | sí | 1 | OBSERVADA |
| 143 | 131 | horizontal | arábigo | sí | 1 | OBSERVADA |
| 144 | 132 | horizontal | arábigo | sí | 0 | CONFORME |
| 145 | 133 | horizontal | arábigo | sí | 1 | OBSERVADA |
| 146 | 134 | vertical | arábigo | sí | 1 | OBSERVADA |
| 147 | 135 | vertical | arábigo | sí | 1 | OBSERVADA |
| 148 | 136 | vertical | arábigo | sí | 2 | OBSERVADA |
| 149 | 137 | vertical | arábigo | sí | 4 | OBSERVADA |
| 150 | 138 | vertical | arábigo | sí | 1 | OBSERVADA |
| 151 | 139 | vertical | arábigo | sí | 1 | OBSERVADA |
| 152 | 140 | vertical | arábigo | sí | 0 | CONFORME |
| 153 | 141 | vertical | arábigo | sí | 2 | OBSERVADA |
| 154 | 142 | vertical | arábigo | sí | 2 | OBSERVADA |
| 155 | 143 | vertical | arábigo | sí | 1 | OBSERVADA |
| 156 | 144 | vertical | arábigo | sí | 1 | OBSERVADA |
| 157 | 145 | vertical | arábigo | sí | 6 | OBSERVADA |
| 158 | 146 | vertical | arábigo | sí | 2 | OBSERVADA |

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

Las tres tablas de resultados por dimensión comparten la misma rejilla de 8 981 dxa con 10 columnas. El exceso de 216 dxa se reparte 0.19 cm por lado y en el PDF se materializa en un desplazamiento de 6 pt sobre el margen izquierdo y 5.5 pt sobre el derecho. La columna más comprometida es la de tamaño muestral: 682 dxa en T36, 411 dxa en T37 y 634 dxa en T38. Con 411 dxa (0.72 cm) el texto se fractura a media palabra (Momen to, Variació n, Median a, 1 4).

### 7.2 Tablas de 8 y 9 columnas (T39 a T43)

T39 (8 columnas), T40, T41 y T42 (9 columnas) y T43 (8 columnas) repiten la rejilla de 8 981 dxa. Las columnas de decisión estadística caen por debajo de 800 dxa y los encabezados se parten en tres líneas: p-valor Ajusta do Holm, Decisió n sobre H0,1, Hipótesi s de Investigació n. En T41 la columna más estrecha mide 635 dxa y en T40, 791 dxa.

### 7.3 Matriz de consistencia en horizontal (T44)

La Tabla A1.1 mide 14 000 dxa exactos (24.69 cm) sobre una caja útil de 13 697 dxa. El exceso de 303 dxa (0.53 cm) hace que la tabla sobresalga 8.25 pt por la izquierda y 7.7 pt por la derecha del área imprimible. Ninguna celda desborda su propia columna, pero el conjunto invade los márgenes laterales de la sección horizontal.

### 7.4 Matrices de datos de 18 columnas (T52 y T53)

Las matrices del pretest y del postest son el punto más débil del documento. Con 18 columnas sobre 8 981 dxa, el ancho medio es de 499 dxa (0.88 cm) y el mínimo de 363 dxa (0.64 cm) en T52 y 400 dxa (0.71 cm) en T53. Las etiquetas de centro de acopio ocupan tres líneas, las cifras se separan del entero (3 8. 5 0) y las cabeceras quedan ilegibles (suj eto_id, centr o_aco pio, nivel_s atisfaccion). La tabla arranca en x = 107.1 pt, muy lejos del margen, porque Word centra el excedente.

## 8. Pictogramas y marcadores de plantilla

| Clase | Unicode | Cantidad | Ubicación |
|---|---|---|---|
| Cámara | U+1F4F7 | 4 | Tablas de las cajas A7.1 a A7.4, páginas 157-158 |
| Mano escribiendo | U+270D | 3 | Certificados de los expertos 1, 2 y 3, páginas 148-149 |

Los siete pictogramas son ajenos al registro editorial institucional. El reemplazo textual sobrio ya está redactado en el JSON de auditoría: «Espacio reservado para fotografía de evidencia en campo» y «Firma y sello del juez validador».

Marcadores de plantilla pendientes: acta de sustentación con instrucción de inserción y dictamen prellenado (p2); DNI del autor con doble marcador (p3); advertencia DATOS DE PRUEBA - REEMPLAZAR (DEC-007) impresa en el cuerpo del Capítulo V (p115); nombre, DNI y firma de los tres jueces (pp. 148-149); instrucción para el tesista en las cuatro cajas del Anexo 7 (pp. 157-158).

## 9. Fichas por página observada

### Página 2 (folio sin folio, vertical) — OBSERVADA

- `parrafo` · **TEXTO_INCOMPLETO** (alta): Acta de sustentación armada con una instrucción editorial entre corchetes (espacio reservado para insertar el acta oficial escaneada) y con el dictamen prellenado APROBADO CON MENCION; fecha, jurado y firmas quedan en blanco.
  - Corrección: Sustituir la caja de instrucción por el acta oficial firmada; retirar el dictamen prellenado.

### Página 3 (folio sin folio, vertical) — OBSERVADA

- `P0018` · **TEXTO_INCOMPLETO** (alta): La declaración jurada conserva dos marcadores de identidad: DNI N.° [Completar DNI oficial antes de impresión] en el encabezado y de nuevo bajo la línea de firma.
  - Corrección: Reemplazar ambos marcadores por el número de DNI real.

### Página 7 (folio v, vertical) — OBSERVADA

- `encabezado` · **DESORDEN_SECCION** (critica): El índice de contenido termina en REFERENCIAS BIBLIOGRÁFICAS tras el apartado 3.2: omite el 3.3 (Metodología XP, pp. 40-85), el CAPÍTULO V, el CAPÍTULO VI, CONCLUSIONES, RECOMENDACIONES y ANEXOS.
  - Corrección: Aplicar estilos Heading 1 a 3 a todos los títulos y regenerar el campo TOC.

### Página 8 (folio vi, vertical) — OBSERVADA

- `encabezado` · **TEXTO_INCOMPLETO** (alta): El índice de figuras enumera solo Figura 1 a Figura 10; faltan las 35 figuras del Capítulo III y las cuatro del Anexo 7.
  - Corrección: Regenerar la lista de figuras con rótulos nativos y numeración única.

### Página 9 (folio vii, vertical) — OBSERVADA

- `encabezado` · **TEXTO_INCOMPLETO** (alta): El índice de tablas enumera solo Tabla 1 a Tabla 5; faltan las tablas 6-26, las tablas 13-21 del Capítulo V y las tablas de los Anexos 1-6.
  - Corrección: Regenerar la lista de tablas completa a partir de rótulos SEQ.
- `P0047` · **ESPACIADO_INCORRECTO** (baja): La entrada Tabla 4 del índice de tablas es la única sin línea de puntos conductores hasta el número de página.
  - Corrección: Restituir el tabulador con relleno de puntos en esa entrada.

### Página 22 (folio 10, vertical) — OBSERVADA

- `P0113` · **ROTULO_INCORRECTO** (alta): El texto remite a la Tabla 10 del Capítulo IV para la matriz de operacionalización; en el Capítulo IV esa matriz es la Tabla 3 y la Tabla 10 es un diccionario de datos del Capítulo III.
  - Corrección: Corregir la referencia cruzada a Tabla 3.

### Página 30 (folio 18, vertical) — OBSERVADA

- `TABLA 1` · **ROTULO_INCORRECTO** (alta): La tabla de síntesis de antecedentes (14 filas x 6 columnas, pp. 30-33) carece de rótulo Tabla N: solo lleva título descriptivo.
  - Corrección: Asignar número correlativo y anteponer el rótulo.

### Página 35 (folio 23, vertical) — OBSERVADA

- `encabezado` · **NUMERACION_SALTADA** (alta): La numeración de figuras reinicia tres veces: Figuras 1-10 en el Capítulo III (pp. 35-46), Figuras 1-35 en el mismo capítulo (pp. 46-97) y Figuras 5-7 en el Capítulo V.
  - Corrección: Renumerar las figuras de forma continua y actualizar todas las referencias cruzadas.

### Página 46 (folio 34, vertical) — OBSERVADA

- `TABLA 2` · **SALTO_PAGINA_AUSENTE** (alta): El rótulo Tabla 1 Dimensiones, indicadores y escalas de medición queda al pie de p46 y la tabla (7 x 4) se desarrolla en p47.
  - Corrección: Aplicar keepNext al rótulo y al título.

### Página 52 (folio 40, vertical) — OBSERVADA

- `P0253` · **NUMERACION_SALTADA** (alta): Segunda tabla rotulada Tabla 1 (roles y responsabilidades, 7 x 4) coexistiendo con la Tabla 1 de P0201; la numeración del Capítulo III arranca en 1 pese a las tablas previas.
  - Corrección: Renumerar de forma continua y eliminar el rótulo duplicado.
- `encabezado` · **NUMERACION_SALTADA** (alta): La numeración de tablas reinicia en el Capítulo III (1 a 26), vuelve a reiniciar en el Capítulo IV (2 a 5) y salta a 13 en el Capítulo V (13 a 21).
  - Corrección: Aplicar numeración continua 1 a 59 en el cuerpo y reservar A1.1 a A7.4 para los anexos.

### Página 58 (folio 46, vertical) — OBSERVADA

- `P0278` · **ENCABEZADO_HUERFANO** (alta): El rótulo Tabla 6 queda como último bloque de p58 (y = 758 pt de 842) y el título, la tabla y la nota pasan a p59.
  - Corrección: Aplicar keepNext al rótulo y al título.
- `encabezado` · **SALTO_PAGINA_AUSENTE** (alta): Causa sistémica: de 115 párrafos de rótulo (Tabla/Figura) solo 15 tienen keepNext, por lo que rótulos y títulos se separan de su objeto en pp. 46, 58, 81, 85-89, 96, 104, 108, 111, 117 y 130.
  - Corrección: Aplicar keepNext a todos los rótulos y títulos mediante docx_quirurgico.

### Página 65 (folio 53, vertical) — OBSERVADA

- `P0326` · **ENCABEZADO_HUERFANO** (alta): El encabezado 3.3.2.4. Modelado Conceptual, Lógico y Físico de la Base de Datos queda al pie de p65 sin ninguna línea de texto debajo.
  - Corrección: Aplicar keepNext a los encabezados de nivel 2 y 3.

### Página 68 (folio 56, vertical) — OBSERVADA

- `P0345` · **ROTULO_INCORRECTO** (baja): Párrafo de nota que comienza con la palabra Tabla (Tabla maestra que representa el nivel superior de la estructura sanitaria) y resulta capturable por cualquier índice automático de tablas.
  - Corrección: Reformular el inicio del párrafo.

### Página 71 (folio 59, vertical) — OBSERVADA

- `TABLA 17` · **TABLA_DESBORDADA** (baja): Sobrancho leve y sistemático (pp. 71-93) en las tablas de cinco y seis columnas del Capítulo III: T14 (8 856 dxa), T17 (8 961), T19 (8 900), T22 (8 895), T23 (8 817) y T27 (8 898) frente a 8 765 dxa útiles. El exceso de 52 a 196 dxa no recorta texto, pero invade el margen derecho.
  - Corrección: Reajustar la rejilla de esas seis tablas a 8 765 dxa.

### Página 74 (folio 62, vertical) — OBSERVADA

- `P0372` · **ROTULO_INCORRECTO** (baja): Párrafo que comienza con Tabla sin ser rótulo (Tabla central transaccional con restricción de unicidad uk_movimiento_establecimiento_vacuna_mes_anio).
  - Corrección: Reformular el inicio del párrafo.

### Página 81 (folio 69, vertical) — OBSERVADA

- `P0408` · **TEXTO_CORTADO** (alta): El rótulo Figura 14 queda al pie de p81 (y = 751 pt) y su título descriptivo pasa a p82: número y título en páginas distintas.
  - Corrección: Unir rótulo y título en un párrafo único con keepNext.

### Página 85 (folio 73, vertical) — OBSERVADA

- `P0441` · **TEXTO_CORTADO** (alta): El rótulo Figura 21 queda al pie de p85 y su título pasa a p86.
  - Corrección: Aplicar keepNext y unir rótulo y título.

### Página 86 (folio 74, vertical) — OBSERVADA

- `P0445` · **TEXTO_CORTADO** (alta): El rótulo Figura 23 queda al pie de p86 y su título pasa a p87.
  - Corrección: Aplicar keepNext y unir rótulo y título.

### Página 87 (folio 75, vertical) — OBSERVADA

- `P0449` · **TEXTO_CORTADO** (alta): El rótulo Figura 25 queda al pie de p87 y su título pasa a p88.
  - Corrección: Aplicar keepNext y unir rótulo y título.

### Página 88 (folio 76, vertical) — OBSERVADA

- `P0453` · **TEXTO_CORTADO** (alta): El rótulo Figura 27 queda al pie de p88 y su título pasa a p89.
  - Corrección: Aplicar keepNext y unir rótulo y título.

### Página 89 (folio 77, vertical) — OBSERVADA

- `P0457` · **TEXTO_CORTADO** (alta): El rótulo Figura 29 queda al pie de p89 y su título pasa a p90.
  - Corrección: Aplicar keepNext y unir rótulo y título.

### Página 91 (folio 79, vertical) — OBSERVADA

- `P0492` · **ENCABEZADO_HUERFANO** (alta): El encabezado 3.3.4. Fase IV: Pruebas de Calidad del Software queda al pie de p91 sin texto debajo.
  - Corrección: Aplicar keepNext a los encabezados.

### Página 96 (folio 84, vertical) — OBSERVADA

- `P0518` · **TEXTO_CORTADO** (alta): El rótulo Figura 35 queda al pie de p96 y su título pasa a p97.
  - Corrección: Aplicar keepNext y unir rótulo y título.

### Página 100 (folio 88, vertical) — OBSERVADA

- `TABLA 29` · **ROTULO_INCORRECTO** (alta): La tabla Cronograma y protocolo de ejecución de la intervención preexperimental (5 x 4) no lleva rótulo Tabla N.
  - Corrección: Asignar número correlativo y anteponer el rótulo.

### Página 103 (folio 91, vertical) — OBSERVADA

- `TABLA 31` · **ROTULO_INCORRECTO** (alta): La tabla Estructura de unidades de observación primaria, reglas de agregación pareada y criterios de inclusión (7 x 4) no lleva rótulo Tabla N.
  - Corrección: Asignar número correlativo y anteponer el rótulo.

### Página 104 (folio 92, vertical) — OBSERVADA

- `TABLA 32` · **SALTO_PAGINA_AUSENTE** (alta): El rótulo Tabla 3 Operacionalización de las variables de investigación queda al pie de p104 y la tabla se desarrolla en p105.
  - Corrección: Aplicar keepNext al rótulo y al título.

### Página 108 (folio 96, vertical) — OBSERVADA

- `TABLA 33` · **SALTO_PAGINA_AUSENTE** (alta): El rótulo Tabla 4 Relación de técnicas e instrumentos de recolección de datos queda al pie de p108 y la tabla se desarrolla en p109.
  - Corrección: Aplicar keepNext al rótulo y al título.

### Página 111 (folio 99, vertical) — OBSERVADA

- `TABLA 34` · **SALTO_PAGINA_AUSENTE** (alta): El rótulo Tabla 5 Estructura de la validación de los instrumentos queda al pie de p111 y la tabla (4 x 7) se desarrolla en p112.
  - Corrección: Aplicar keepNext al rótulo y al título.

### Página 115 (folio 103, vertical) — OBSERVADA

- `P0619` · **TEXTO_INCOMPLETO** (critica): Advertencia interna impresa en el cuerpo del Capítulo V: declara que los resultados corresponden a DATOS DE PRUEBA - REEMPLAZAR (DEC-007) e incluye rutas y comandos del repositorio.
  - Corrección: Retirar la advertencia del informe final y trasladarla a una nota interna no impresa.

### Página 116 (folio 104, vertical) — OBSERVADA

- `TABLA 35` · **TABLA_DESBORDADA** (alta): Tabla descriptiva de 8 columnas y 7 filas con 8 981 dxa de rejilla frente a 8 765 dxa útiles (216 dxa de exceso, 0.19 cm por lado).
  - Corrección: Reducir la rejilla a 8 765 dxa y redistribuir columnas.
- `P0623` · **ROTULO_INCORRECTO** (alta): En la Tabla 4 se consolidan los coeficientes remite a la Tabla 4 del Capítulo IV (técnicas e instrumentos); la tabla de confiabilidad es la Tabla 13.
  - Corrección: Corregir la referencia a Tabla 13.

### Página 117 (folio 105, vertical) — OBSERVADA

- `P0631` · **ENCABEZADO_HUERFANO** (alta): El rótulo Tabla 14 y su título quedan al pie de p117 y la tabla (7 x 10) aparece sola en p118.
  - Corrección: Aplicar keepNext al rótulo y al título.
- `P0630` · **ROTULO_INCORRECTO** (alta): En la Tabla 5 y en la Figura 6 se detallan remite a objetos del Capítulo IV; lo correcto es Tabla 14 y Figura 5.
  - Corrección: Corregir ambas referencias cruzadas.

### Página 118 (folio 106, vertical) — OBSERVADA

- `TABLA 36` · **TABLA_DESBORDADA** (alta): Tabla de 10 columnas y 7 filas con rejilla de 8 981 dxa frente a 8 765 dxa de caja útil (márgenes 3.0 / 2.54 / 2.54 cm): excede 216 dxa, 0.19 cm por lado. En el PDF llega a x = 528.8 pt frente al límite derecho de 523.3 pt y arranca en x = 79.0 pt frente al límite izquierdo de 85.05 pt.
  - Corrección: Reducir la rejilla a 8 765 dxa; valorar orientación horizontal o fusión de columnas.
- `TABLA 36` · **CELDA_ILEGIBLE** (media): La columna n mide 682 dxa (1.20 cm) y la de indicador 1 061 dxa (1.87 cm): encabezados partidos en tres y cuatro líneas y celdas de indicador en cinco líneas.
  - Corrección: Ampliar las columnas de texto y reducir el cuerpo a 9 pt dentro de la tabla.

### Página 120 (folio 108, vertical) — OBSERVADA

- `TABLA 37` · **TABLA_DESBORDADA** (alta): Tabla de 10 columnas y 7 filas con rejilla de 8 981 dxa frente a 8 765 dxa útiles (216 dxa de exceso); en el PDF llega a x = 528.8 pt frente al límite de 523.3 pt.
  - Corrección: Reducir la rejilla a 8 765 dxa.
- `TABLA 37` · **CELDA_ILEGIBLE** (critica): La columna n mide 411 dxa (0.72 cm), la más estrecha del documento: fractura palabras y cifras (Momen to, Variació n, Median a, 1 4).
  - Corrección: Eliminar la columna n, constante igual a 14, o ensancharla a 700 dxa.

### Página 121 (folio 109, vertical) — OBSERVADA

- `P0648` · **ROTULO_INCORRECTO** (alta): En la Tabla 7 y en la Figura 8 se presenta: los objetos de la Dimensión 3 son la Tabla 16 y la Figura 7.
  - Corrección: Corregir ambas referencias cruzadas.

### Página 122 (folio 110, vertical) — OBSERVADA

- `TABLA 38` · **TABLA_DESBORDADA** (alta): Tabla de 10 columnas y 10 filas con rejilla de 8 981 dxa frente a 8 765 dxa útiles (216 dxa de exceso); en el PDF alcanza x = 528.8 pt.
  - Corrección: Reducir la rejilla a 8 765 dxa.
- `TABLA 38` · **CELDA_ILEGIBLE** (media): La columna más estrecha mide 634 dxa (1.12 cm); Constructo/subescala y Momento evaluado se parten en cuatro líneas y las etiquetas TAM se apilan verticalmente.
  - Corrección: Ampliar columnas de texto y abreviar encabezados.

### Página 124 (folio 112, vertical) — OBSERVADA

- `TABLA 39` · **TABLA_DESBORDADA** (alta): Tabla de 8 columnas y 8 filas con rejilla de 8 981 dxa frente a 8 765 dxa útiles; en el PDF alcanza x = 528.8 pt.
  - Corrección: Reducir la rejilla a 8 765 dxa.
- `P0659` · **ROTULO_INCORRECTO** (alta): La Tabla 8 resume las decisiones: la tabla de normalidad que sigue es la Tabla 17.
  - Corrección: Corregir la referencia a Tabla 17.

### Página 125 (folio 113, vertical) — OBSERVADA

- `TABLA 39` · **VIUDA_HUERFANA** (media): La tabla de 8 filas se fragmenta entre p124 y p125; la segunda página arrastra el remanente de filas con el encabezado repetido.
  - Corrección: Mantener la tabla en una página o dividirla por dimensión con subtítulos propios.

### Página 126 (folio 114, vertical) — OBSERVADA

- `P0672` · **ENCABEZADO_HUERFANO** (alta): 5.4.2. Contrastación de la Hipótesis Específica 2 queda al pie de p126 sin texto debajo.
  - Corrección: Aplicar keepNext al encabezado.
- `TABLA 40` · **TABLA_DESBORDADA** (alta): Tabla de 9 columnas y 5 filas con rejilla de 8 981 dxa frente a 8 765 dxa útiles (216 dxa de exceso).
  - Corrección: Reducir la rejilla a 8 765 dxa.
- `TABLA 40` · **CELDA_ILEGIBLE** (alta): Encabezados fracturados: p-valor Ajusta do Holm y Decisió n sobre H0,1; la columna más estrecha mide 791 dxa (1.40 cm).
  - Corrección: Abreviar encabezados y redistribuir anchos.
- `P0668` · **ROTULO_INCORRECTO** (alta): (Tabla 9) remite al diccionario de datos; el contraste de la HE1 se presenta en la Tabla 18.
  - Corrección: Corregir la referencia a Tabla 18.

### Página 127 (folio 115, vertical) — OBSERVADA

- `TABLA 41` · **TABLA_DESBORDADA** (alta): Tabla de 9 columnas y 5 filas con rejilla de 8 981 dxa frente a 8 765 dxa útiles (216 dxa de exceso).
  - Corrección: Reducir la rejilla a 8 765 dxa.
- `TABLA 41` · **CELDA_ILEGIBLE** (critica): La columna más estrecha mide 635 dxa (1.12 cm): Concordanc ia, Wilcoxo n, Rechaz ar, Gran de.
  - Corrección: Ampliar las columnas de indicador y decisión; abreviar encabezados.
- `P0675` · **ROTULO_INCORRECTO** (alta): (Tabla 10): el contraste de la HE2 se presenta en la Tabla 19.
  - Corrección: Corregir la referencia a Tabla 19.

### Página 128 (folio 116, vertical) — OBSERVADA

- `TABLA 41` · **VIUDA_HUERFANA** (media): La tabla se divide entre p127 y p128 con el encabezado repetido, dejando la segunda página con el remanente de filas.
  - Corrección: Reajustar anchos y altura para mantener la tabla en una página.
- `P0682` · **ROTULO_INCORRECTO** (alta): (Tabla 11): el contraste de la HE3 se presenta en la Tabla 20.
  - Corrección: Corregir la referencia a Tabla 20.

### Página 129 (folio 117, vertical) — OBSERVADA

- `TABLA 42` · **TABLA_DESBORDADA** (alta): Tabla de 9 columnas y 7 filas con rejilla de 8 981 dxa frente a 8 765 dxa útiles (216 dxa de exceso).
  - Corrección: Reducir la rejilla a 8 765 dxa.
- `TABLA 42` · **CELDA_ILEGIBLE** (alta): Encabezados fracturados: Estadísti co t, p-valor Ajusta do Holm, Decisió n sobre H0,3.
  - Corrección: Abreviar encabezados y redistribuir anchos.

### Página 130 (folio 118, vertical) — OBSERVADA

- `P0691` · **ENCABEZADO_HUERFANO** (alta): El rótulo Tabla 21 y su título quedan al pie de p130 y la tabla continúa sola en p131.
  - Corrección: Aplicar keepNext al rótulo y al título.
- `TABLA 43` · **TABLA_DESBORDADA** (alta): Tabla de 8 columnas y 5 filas con rejilla de 8 981 dxa frente a 8 765 dxa útiles (216 dxa de exceso).
  - Corrección: Reducir la rejilla a 8 765 dxa.
- `TABLA 43` · **CELDA_ILEGIBLE** (alta): Encabezados fracturados: Hipótesi s de Investigació n, Decisió n, Operativ a; celdas Rechaz ar H0,1 y Reducció n > 15%.
  - Corrección: Reducir el número de columnas y abreviar encabezados.
- `P0690` · **ROTULO_INCORRECTO** (alta): En la Tabla 12 se presenta el balance consolidado: la tabla resumen es la Tabla 21.
  - Corrección: Corregir la referencia a Tabla 21.

### Página 131 (folio 119, vertical) — OBSERVADA

- `TABLA 43` · **VIUDA_HUERFANA** (alta): p131 contiene solo las filas finales y la nota de la Tabla 21 (938 caracteres en toda la página); más del 60 por ciento del área queda en blanco.
  - Corrección: Cerrar la tabla en p130 reduciendo altura de fila o cuerpo tipográfico.

### Página 141 (folio 129, vertical) — OBSERVADA

- `P0752` · **VIUDA_HUERFANA** (media): Página con una sola referencia (World Health Organization, 2021), 160 caracteres, y más del 80 por ciento del área en blanco.
  - Corrección: Ajustar el interlineado de la lista para evitar el arrastre de una sola entrada.

### Página 142 (folio 130, vertical) — OBSERVADA

- `P0753` · **VIUDA_HUERFANA** (baja): Página dedicada exclusivamente a la palabra ANEXOS (12 caracteres), sin otro contenido.
  - Corrección: Integrar la portadilla con el primer anexo o eliminarla.

### Página 143 (folio 131, horizontal) — OBSERVADA

- `TABLA 44` · **TABLA_DESBORDADA** (alta): Matriz de consistencia en orientación horizontal con rejilla de 14 000 dxa frente a 13 697 dxa de caja útil (21.0 - 3.0 - 2.54 - 2.54 cm): excede 303 dxa (0.53 cm). En el PDF abarca de x = 76.8 a 777.6 pt frente a los límites de 85.05 y 769.92 pt.
  - Corrección: Reducir la rejilla a 13 697 dxa o ampliar la caja útil horizontal a 3.0 / 2.0 cm.

### Página 145 (folio 133, horizontal) — OBSERVADA

- `TABLA 44` · **VIUDA_HUERFANA** (media): p145 contiene solo las dos últimas filas y la nota de la Tabla A1.1; el resto de la página queda en blanco.
  - Corrección: Ajustar anchos y altura de fila para cerrar la matriz en p144.

### Página 146 (folio 134, vertical) — OBSERVADA

- `TABLA 45` · **CELDA_ILEGIBLE** (media): La matriz de operacionalización (6 columnas, 8 766 dxa) comprime la primera columna hasta partir palabras (Variable Independie nte) y apila las definiciones en 8 a 10 líneas por celda.
  - Corrección: Ampliar las columnas de variable y definición; mover la definición operacional a una nota.

### Página 147 (folio 135, vertical) — OBSERVADA

- `TABLA 45` · **VIUDA_HUERFANA** (media): La Tabla A2.1 se prolonga a p147 con tres filas y su nota, dejando el resto de la página vacío.
  - Corrección: Reducir altura de fila o cuerpo tipográfico para cerrar la tabla en p146.

### Página 148 (folio 136, vertical) — OBSERVADA

- `TABLA 46` · **TEXTO_INCOMPLETO** (alta): Certificado del Experto 1 con el nombre sustituido por Evaluador Pericial Designado (Experto 1), DNI [Registrado en expediente] y firma no insertada.
  - Corrección: Insertar nombre, grado, institución, DNI y firma reales del juez validador.
- `TABLA 46` · **EMOJI** (alta): El pictograma U+270D precede a ESPACIO RESERVADO PARA INSERCION DE FIRMA Y SELLO ESCANEADO DEL EXPERTO.
  - Corrección: Sustituir el pictograma por un recuadro rotulado Firma y sello del juez validador.

### Página 149 (folio 137, vertical) — OBSERVADA

- `TABLA 47` · **TEXTO_INCOMPLETO** (alta): Certificado del Experto 2 con nombre genérico, DNI [Registrado en expediente] y firma no insertada.
  - Corrección: Insertar los datos reales del juez validador.
- `TABLA 47` · **EMOJI** (alta): Segundo pictograma U+270D en el espacio de firma del Experto 2.
  - Corrección: Reemplazar por un recuadro de firma sin pictogramas.
- `TABLA 48` · **TEXTO_INCOMPLETO** (alta): Certificado del Experto 3 con nombre genérico, DNI [Registrado en expediente] y firma no insertada.
  - Corrección: Insertar los datos reales del juez validador.
- `TABLA 48` · **EMOJI** (alta): Tercer pictograma U+270D en el espacio de firma del Experto 3.
  - Corrección: Reemplazar por un recuadro de firma sin pictogramas.

### Página 150 (folio 138, vertical) — OBSERVADA

- `TABLA 49` · **CELDA_ILEGIBLE** (media): La ficha A4.1 comprime cuatro columnas de 2 191 dxa (3.86 cm) y corta fórmulas como (Total registros conformes sin error / Total transacciones auditadas) * 100 en seis líneas.
  - Corrección: Trasladar las fórmulas al cuerpo narrativo, conforme a la prohibición de fórmulas en celdas.

### Página 151 (folio 139, vertical) — OBSERVADA

- `TABLA 51` · **VIUDA_HUERFANA** (alta): La Tabla A4.3 (cuestionario TAM) se prolonga a p152, donde queda una sola fila (UP-04) y la nota; el 80 por ciento de la página queda en blanco.
  - Corrección: Reducir el enunciado de los reactivos o el interlineado para cerrar la tabla en p151.

### Página 153 (folio 141, vertical) — OBSERVADA

- `TABLA 52` · **TABLA_DESBORDADA** (critica): Matriz de datos del pretest con 18 columnas y 15 filas: 8 981 dxa de rejilla frente a 8 765 dxa útiles (216 dxa de exceso). En el PDF arranca en x = 107.1 pt y llega a x = 528.8 pt frente al límite derecho de 523.3 pt.
  - Corrección: Reducir la rejilla a 8 765 dxa; pasar la matriz a horizontal o dividirla en dos tablas.
- `TABLA 52` · **CELDA_ILEGIBLE** (critica): Con 18 columnas el ancho medio es de 499 dxa (0.88 cm) y el mínimo de 363 dxa (0.64 cm): las cifras se fracturan hasta en cuatro líneas (3 8. 5 0), ALMACEN (CHANKA) ocupa tres líneas y las cabeceras se leen suj eto_id, centr o_aco pio, nivel_s atisfaccion.
  - Corrección: Dividir en dos tablas de 9 columnas o girar a horizontal con anchos mínimos de 700 dxa.

### Página 154 (folio 142, vertical) — OBSERVADA

- `TABLA 53` · **TABLA_DESBORDADA** (critica): Matriz de datos del postest con 18 columnas y 15 filas: 8 981 dxa de rejilla frente a 8 765 dxa útiles, con el mismo desborde de 5.5 pt sobre el margen derecho.
  - Corrección: Reducir la rejilla a 8 765 dxa o pasar la matriz a orientación horizontal.
- `TABLA 53` · **CELDA_ILEGIBLE** (critica): Mismas patologías que la matriz del pretest: columna mínima de 400 dxa (0.71 cm), cifras y etiquetas partidas en varias líneas, cabeceras ilegibles.
  - Corrección: Dividir la matriz o ampliar columnas en horizontal.

### Página 155 (folio 143, vertical) — OBSERVADA

- `TABLA 53` · **VIUDA_HUERFANA** (baja): La segunda página de la matriz ocupa por completo p155 sin encabezado de sección ni contexto.
  - Corrección: Repetir el encabezado de columna y rotular la continuación.

### Página 156 (folio 144, vertical) — OBSERVADA

- `TABLA 54` · **TABLA_DESBORDADA** (media): La Tabla A6.1 (5 columnas, 8 981 dxa) excede la caja útil en 216 dxa; en el PDF llega a x = 528.8 pt frente al límite de 523.3 pt.
  - Corrección: Reducir la rejilla a 8 765 dxa.

### Página 157 (folio 145, vertical) — OBSERVADA

- `TABLA 55` · **EMOJI** (alta): La caja de la Figura A7.1 contiene el pictograma U+1F4F7 (cámara) antes de ESPACIO RESERVADO PARA FOTOGRAFIA DE EVIDENCIA EN CAMPO.
  - Corrección: Sustituir el pictograma por el texto Espacio reservado para fotografía de evidencia en campo.
- `TABLA 56` · **EMOJI** (alta): La caja de la Figura A7.2 repite el pictograma U+1F4F7.
  - Corrección: Eliminar el pictograma y conservar solo el rótulo textual.
- `TABLA 57` · **EMOJI** (alta): La caja de la Figura A7.3 repite el pictograma U+1F4F7.
  - Corrección: Eliminar el pictograma y conservar solo el rótulo textual.
- `parrafo` · **TEXTO_INCOMPLETO** (critica): Las cuatro cajas del Anexo 7 conservan la instrucción editorial Instrucción para el tesista: Insertar en este espacio la fotografía correspondiente a, visible en el documento final.
  - Corrección: Insertar las fotografías definitivas a 300 DPI o retirar el anexo.
- `P0804` · **ROTULO_INCORRECTO** (alta): El rótulo Figura A7.3 queda al pie de p157 y su título y su nota pasan a p158, separados de la caja correspondiente.
  - Corrección: Unir rótulo, título, caja y nota con keepNext.
- `P0800` · **TEXTO_DUPLICADO** (baja): La nota Registro fotográfico de verificación en campo. Dirección de Salud Apurímac II (2026). se repite literalmente cuatro veces (P0800, P0803, P0806, P0809).
  - Corrección: Diferenciar cada nota con la fecha y el lugar específicos de la toma.

### Página 158 (folio 146, vertical) — OBSERVADA

- `TABLA 58` · **EMOJI** (alta): La caja de la Figura A7.4 repite el pictograma U+1F4F7.
  - Corrección: Eliminar el pictograma y conservar solo el rótulo textual.
- `TABLA 58` · **TEXTO_INCOMPLETO** (critica): Cuarta caja del Anexo 7 con la misma instrucción editorial y sin fotografía insertada.
  - Corrección: Insertar la fotografía definitiva o retirar la caja.

## 10. Control de inmutabilidad

Los archivos de referencia y el documento auditado se abrieron en modo de solo lectura. No se ejecutó ninguna escritura sobre `informe_final_v04.docx` ni sobre `informe_final_v04.pdf`: la huella SHA-256 registrada en el apartado 1 corresponde al estado previo y posterior a la auditoría. Los únicos archivos creados son los PNG de render, los auxiliares de medición y este informe, todos bajo `salidas/reportes_maquetacion/`.

## 11. Recomendaciones priorizadas

1. **Cirugía de rejilla (bloqueante).** Llevar a 8 765 dxa las diecinueve tablas con exceso significativo y a 13 697 dxa la Tabla A1.1. En T37 eliminar la columna n, constante igual a 14, y redistribuir su ancho entre las columnas de texto.
2. **Matrices de 18 columnas (bloqueante).** Dividir T52 y T53 en dos tablas de 9 columnas (identificación y puntajes) o trasladarlas a una sección horizontal con anchos mínimos de 700 dxa. Con la rejilla actual el dato no es legible en papel.
3. **Control de rótulos (bloqueante para QG-9).** Aplicar keepNext a los 115 párrafos de rótulo y a todos los encabezados de nivel 2 y 3; unir número y título de figura en un párrafo único. Esto resuelve las dieciocho separaciones detectadas entre páginas 46 y 130 y en el Anexo 7.
4. **Renumeración única.** Asignar numeración continua a tablas (1 a 59) y figuras (1 a 52), actualizar las once referencias cruzadas erróneas del Capítulo V y regenerar los índices de figuras y de tablas a partir de campos SEQ.
5. **Regeneración del índice de contenido.** Aplicar Heading 1 a 3 a todas las secciones; hoy el índice omite el 3.3, el Capítulo V, el Capítulo VI, Conclusiones, Recomendaciones y Anexos.
6. **Limpieza editorial.** Retirar la advertencia de datos de prueba, sustituir los siete pictogramas, completar los datos de los certificados y del acta, e insertar las fotografías del Anexo 7 o retirar las cajas.
7. **Control de viudas.** Ajustar interlineado y altura de fila en pp. 131, 141, 145, 147, 151 y 155 para evitar páginas con menos del 20 por ciento de ocupación.

---

## Anexo A. Inventario completo de tablas

| Tabla | Filas | Cols. | Rejilla dxa | Exceso sobre caja útil |
|---|---|---|---|---|
| T00 | 1 | 1 | 8788 | +23 |
| T01 | 14 | 6 | 8784 | +19 |
| T02 | 7 | 4 | 8784 | +19 |
| T03 | 5 | 3 | 8766 | +1 |
| T04 | 17 | 3 | 8766 | +1 |
| T05 | 9 | 4 | 8764 | -1 |
| T06 | 7 | 4 | 8764 | -1 |
| T07 | 16 | 6 | 8766 | +1 |
| T08 | 6 | 5 | 8765 | +0 |
| T09 | 10 | 5 | 8765 | +0 |
| T10 | 8 | 5 | 8765 | +0 |
| T11 | 7 | 5 | 8765 | +0 |
| T12 | 9 | 5 | 8765 | +0 |
| T13 | 8 | 5 | 8778 | +13 |
| T14 | 10 | 5 | 8856 | +91 |
| T15 | 10 | 5 | 8765 | +0 |
| T16 | 7 | 5 | 8765 | +0 |
| T17 | 10 | 5 | 8961 | +196 |
| T18 | 7 | 5 | 8765 | +0 |
| T19 | 12 | 5 | 8900 | +135 |
| T20 | 8 | 5 | 8765 | +0 |
| T21 | 11 | 5 | 8765 | +0 |
| T22 | 11 | 5 | 8895 | +130 |
| T23 | 10 | 5 | 8817 | +52 |
| T24 | 10 | 5 | 8765 | +0 |
| T25 | 13 | 4 | 8764 | -1 |
| T26 | 7 | 5 | 8765 | +0 |
| T27 | 16 | 6 | 8898 | +133 |
| T28 | 9 | 5 | 8765 | +0 |
| T29 | 5 | 4 | 8784 | +19 |
| T30 | 10 | 4 | 8784 | +19 |
| T31 | 7 | 4 | 8784 | +19 |
| T32 | 5 | 6 | 8784 | +19 |
| T33 | 4 | 5 | 8783 | +18 |
| T34 | 4 | 7 | 8784 | +19 |
| T35 | 7 | 8 | 8981 | +216 |
| T36 | 7 | 10 | 8981 | +216 |
| T37 | 7 | 10 | 8981 | +216 |
| T38 | 10 | 10 | 8981 | +216 |
| T39 | 8 | 8 | 8981 | +216 |
| T40 | 5 | 9 | 8981 | +216 |
| T41 | 5 | 9 | 8981 | +216 |
| T42 | 7 | 9 | 8981 | +216 |
| T43 | 5 | 8 | 8981 | +216 |
| T44 | 5 | 5 | 14000 | +303 |
| T45 | 5 | 6 | 8766 | +1 |
| T46 | 8 | 2 | 8764 | -1 |
| T47 | 8 | 2 | 8764 | -1 |
| T48 | 8 | 2 | 8764 | -1 |
| T49 | 4 | 4 | 8764 | -1 |
| T50 | 4 | 4 | 8764 | -1 |
| T51 | 9 | 4 | 8764 | -1 |
| T52 | 15 | 18 | 8981 | +216 |
| T53 | 15 | 18 | 8981 | +216 |
| T54 | 6 | 5 | 8981 | +216 |
| T55 | 1 | 1 | 8640 | -125 |
| T56 | 1 | 1 | 8640 | -125 |
| T57 | 1 | 1 | 8640 | -125 |
| T58 | 1 | 1 | 8640 | -125 |

## Anexo B. Correspondencia con el JSON

El registro estructurado `auditoria_hoja_por_hoja_v04.json` contiene los 158 veredictos de página, los 90 defectos con la estructura exigida (`pagina`, `elemento`, `indice_docx`, `tipo`, `descripcion`, `severidad`, `correccion_sugerida`) y las mediciones agregadas. Los índices `indice_docx` de párrafo corresponden a la numeración P del volcado `informe_final_v04_texto_plano.md`; los de tabla corresponden a la numeración TABLA del mismo volcado.
