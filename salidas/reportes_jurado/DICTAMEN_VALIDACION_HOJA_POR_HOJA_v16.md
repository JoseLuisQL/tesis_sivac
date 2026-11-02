# DICTAMEN DE VALIDACIÓN HOJA POR HOJA
## Informe Final de Tesis SIVAC — versión 16

**Documento auditado:** `salidas/documentos/informe_final_v16.docx`
**SHA-256:** `cffa62d25dffba58ebc3aba59776b89f1a50aab2e5e145c123005946e73698e5`
**Exportación PDF:** `salidas/documentos/informe_final_v16.pdf`, 159 páginas
**Fecha:** 2026-10-21
**Fase:** F8_INTEGRACION_EDITORIAL

**Nota de rectificación (2026-10-21):** este dictamen conserva los resultados preliminares comunicados por los tramos. La comprobación posterior contra el XML detectó errores de conteo y de atribución que se documentan en `salidas/reportes_maquetacion/plan_maquetacion_aclaraciones_20261021.json`. No debe leerse el porcentaje de páginas clasificadas como una medida validada de calidad global, ni como aprobación de impresión. Hay 36 identificadores B/C/M enumerados, no 41. La evidencia posterior confirmó cinco iteraciones XP y que la imagen de Figura 44 es código auténtico cuya descripción debe corregirse. Las nuevas puntuaciones de jueces fueron comunicadas por el tesista después de esta auditoría y no deben confundirse con los certificados que este dictamen inspeccionó.

---

## 1. Resultado global

| Tramo | Páginas | Conformes | Con defecto | Revisor |
|---|---:|---:|---:|---|
| Preliminares y capítulos I-II | 1-40 | 25 | 15 | analista-documental |
| Figuras y tablas iniciales | 41-80 | 37 | 3 | maquetador-docx |
| Aparato tabular y casos de prueba | 81-120 | 26 | 14 | analista-documental |
| Resultados, discusión, referencias y anexos | 121-159 | 11 | 28 | verificador-integridad |
| **Total** | **159** | **99** | **60** | |

**Conformidad global: 99 de 159 páginas, equivalente al 62,3 %.**

Las 60 páginas clasificadas inicialmente con defecto no implican 60 defectos independientes: varios comparten causa. El apartado 3 enumera 36 identificadores distintos (7 B, 7 C y 22 M), además del diagnóstico de resolución de imágenes. Su procedencia y pertinencia se contrastan en la revisión posterior indicada en la nota de rectificación.

**Páginas con defecto por tramo:**

- 1-40: 1, 3, 7, 10, 11, 12, 15, 28, 32, 35, 36, 37, 38, 39, 40
- 41-80: 51, 73, 79
- 81-120: 85, 86, 88, 89, 97, 99, 100, 103, 109, 113, 114, 116, 119, 120
- 121-159: 122, 123, 125, 126, 127, 128, 129, 130, 131, 132, 134, 137, 138, 139, 140, 141, 142, 143, 145, 146, 147, 148, 149, 150, 151, 152, 153, 156

---

## 2. Lo que quedó verificado como correcto

La auditoría no solo buscó defectos; confirmó un conjunto amplio de propiedades que sostienen la calidad del documento:

- **Geometría:** cero bloques fuera de margen en las 159 páginas. Márgenes de 3,0 cm izquierdo y 2,5 cm en los tres restantes, con borde derecho en 526,4 pt.
- **Tipografía:** Times New Roman 12 pt, interlineado 1,5 con paso de línea de 20,7 pt, sangría de primera línea de 1,27 cm en el cuerpo y ausencia de sangría en títulos y rótulos.
- **Tablas:** las 51 tablas del cuerpo presentan tres líneas horizontales y cero verticales; el encabezado se repite en los once saltos de página detectados en el tramo 41-80 y en los nueve del tramo 81-120; ninguna fila quedó partida por la mitad.
- **Rótulos:** en las 51 tablas y las 48 figuras con imagen, el rótulo precede al objeto y ninguno quedó separado por un salto de página.
- **Paginación:** folios romanos en preliminares, sin número impreso en la carátula; arábigos continuos de 1 a 143 en el cuerpo, en la esquina superior derecha.
- **Notación estadística:** cero p-valores con cero inicial en todo el documento; el único del tramo 81-120 es `p > .05`.
- **Bibliografía:** correspondencia 1:1 sin alertas rojas. Las cinco entradas dictaminadas en la v16 están correctas: Addy (2023) como autor único con URL, OPS y PATH (2019) con handle 10665.2/50482, Balón Morejón (2023) sin URL, ISO/IEC 25010:2023 con enlace oficial y Quispe Tello (2024) con repositorio UNAJMA y handle. La lista de 53 entradas conserva el orden alfabético en los empalmes verificados, con sangría francesa de 1,27 cm e interlineado 1,5.
- **Cita de Quispe Tello:** cuatro apariciones correctas —p. 24 con localizador 36, p. 115 con 62, p. 116 con 62 y el asentamiento de p. 142—. No queda residuo de «Fany (2024)».
- **Sumas de la Tabla 49 y 50:** verificadas fila por fila; la desagregación AP + UP coincide con el total TAM en las 14 filas.
- **Conclusiones y recomendaciones:** alineadas con los objetivos y con las tres dimensiones de DEC-007, sin deriva metodológica.

---

## 3. Inventario consolidado de defectos

### 3.1 Bloqueantes de impresión

Estos defectos impiden considerar el documento listo para impresión o para presentación al jurado.

| ID | Pág. | Defecto | Origen | Subsanación |
|---|---|---|---|---|
| B-01 | 3 | Doble marcador «[Completar DNI oficial antes de impresión]» en la carátula | Residuo de plantilla | Requiere decisión del tesista: completar el dato o dejarlo manuscrito |
| B-02 | 15 | Residuo «[Pending]» al cierre del ABSTRACT | Residuo de edición | Suprimir el token o traducirlo; corrección editorial segura |
| B-03 | 116 | Tres marcadores «[Pendiente]» en celdas de resultados de la Tabla 34 | Vacío de datos | **BLOQUEADO:** exige los coeficientes V de Aiken e IVC que no constan en el Capítulo V ni en el Anexo 3 |
| B-04 | 150-151 | Anexo 3 con «[Por completar por el juez]» para ambos coeficientes y para la aplicabilidad | Vacío de datos | **BLOQUEADO:** depende de los jueces validadores |
| B-05 | 97 | La Figura 44 muestra un archivo fuente TypeScript, mientras su nota describe la consola de ejecución al 100 % de casos | Error de inserción | Requiere la captura correcta del tesista |
| B-06 | 152 | Tabla 47 con fórmulas dentro de celdas y asterisco ASCII de multiplicación | Contra la regla UNAJMA de cero fórmulas en celdas | Reemplazar por descripción textual; la fórmula va al cuerpo narrativo |
| B-07 | 153 | Nota de la Tabla 48 con residuo «…los tres jueces.) con confiabilidad Alfa de Cronbach > 0.90.» y afirmación de fiabilidad no sustentada | Residuo de edición | Depurar la nota y retirar la afirmación no respaldada |

### 3.2 Defectos de contenido y coherencia

Requieren decisión del tesista porque afectan el sentido del texto o los datos.

| ID | Pág. | Defecto | Dictamen del auditor |
|---|---|---|---|
| C-01 | 99-100 y 121 | CP-06 declara 1,15 min de registro (antes 14,8) y CP-11 declara 1,45 s de emisión; la Tabla 36 reporta T_reg de 37,18 a 7,18 min y T_vale de 3,04 min | No son la misma medición: los casos de prueba miden una operación unitaria en entorno controlado y la Tabla 36 mide el proceso mensual completo de 14 operadores. Los cocientes lo confirman —6,2 veces y 125,8 veces—. El defecto es que **el documento no declara esa diferencia de alcance** y que el antecedente «antes 14,8 min» no coincide con el pretest oficial de 37,18 min. Subsanable con una nota metodológica; no se alteran las cifras oficiales de la D1 |
| C-02 | 19 y 141 | OPS y PATH citadas como 2020 en el cuerpo y como 2019 en la referencia | Unificar el año; la entrada bibliográfica está verificada como 2019 |
| C-03 | 156 | El texto remite a «Tabla A6.1» y el rótulo dice «Tabla 51»; se declaran cinco iteraciones y la tabla muestra cuatro distintas (1, 2, 3, 3, 4) | Unificar la remisión y el recuento |
| C-04 | 134 | Duplicación literal de la aserción FEFO y bloqueo de stock en el mismo párrafo | Suprimir la repetición |
| C-05 | 120 | La nota de la Tabla 35 atribuye la fuente a «Matriz de recolección de campo SIVAC (2026)», mientras la p. 119 declara datos provisionales de prueba | Alinear la nota con la condición declarada de los datos, conforme a DEC-014 |
| C-06 | 7 | «(T_reg y T_vale)» con guiones bajos en el cuerpo | Sustituir por la notación matemática o por prosa |
| C-07 | 114 | Fórmula de Kappa como texto plano, sin OMML nativo | Convertir a ecuación nativa o a prosa con definición de términos |

### 3.3 Defectos de maquetación

Corregibles de forma nativa sin intervenir el contenido sustantivo.

| ID | Pág. | Defecto |
|---|---|---|
| M-01 | 36, 37, 38, 109, 116 | Fracturas intra-palabra en celdas: «Casuiexperimenta/l», «desabastecimient/o», «preexperimenta/l», «Cuasiexperimenta/l», «Establecimiento/s», «Astuhuama/n», «Valoració/n», «cronometrad/os», «interobservad/or», «interevaluado/r», «[Pendien/te]», «[Pend/iente]» |
| M-02 | 36-38 | Columna 6 de la Tabla 1 demasiado estrecha, causa raíz de las fracturas del tramo |
| M-03 | 73, 79 | Notas de las Tablas 10 y 19 sin el prefijo «Nota.» ni cursiva |
| M-04 | 120 | «Nota.» y «Fuente:» en redonda, a diferencia del resto del documento |
| M-05 | 113-114 | Nota de la Tabla 33 huérfana al inicio de la página siguiente |
| M-06 | 12 | Títulos de las Tablas 1, 29 y 31 en negrita en lugar de cursiva |
| M-07 | 103 | «Donde:» aislado al pie, con las viñetas continuando en la página siguiente |
| M-08 | 85, 86, 88, 125, 126, 127, 128, 129, 130 | Estiramiento extremo del justificado, con huecos interpalabra de hasta 9,4 pt y uno de 42,6 pt en la p. 119 |
| M-09 | 137-143 | Cursivas APA 7 ausentes en catorce entradas bibliográficas: títulos de revista y de obra sin cursiva en Brooks, Chekol, Cronbach, Feldt, George, Hernández-Sampieri, Holm, Mamani-Pari, Ndlovu, Razali, Rosenthal, Shapiro, Venkatesh y Wilcoxon |
| M-10 | 140 | Coma espuria en la entrada ISO/IEC: «Standardization, e» |
| M-11 | 131-132 | Tabla 43 fragmentada sin rótulo de continuación, con una fila aislada que deja la página 132 al 85 % vacía |
| M-12 | 145-147 | Tabla 44 fragmentada sin rótulo de continuación |
| M-13 | 148-149 | Tabla 45 fragmentada sin rótulo de continuación, con filas de una dimensión aisladas y página al 80 % vacía |
| M-14 | 150-151 | Anexo 3 con «(Juez 1)» y «(Juez 2)» duplicados, paréntesis desbalanceado, cabecera repetida y ausencia de la tercera línea de tabla |
| M-15 | 10, 12 | Índices con líneas de puntos sin texto en las entradas de las Figuras 41, 42, 45 y de las Tablas 28 y 33 |
| M-16 | 11 | Folio ix con una sola entrada y 95 % de la página vacío |
| M-17 | 28 | Página con dos líneas y 93 % vacía |
| M-18 | 32, 35, 39 | Cortes de línea dentro de «(p < .01)», de «0.84–0.98» y de la cita «2010, p. iv)» |
| M-19 | 39 | Niveles 3 y 4 de encabezado con idéntico formato de negrita cursiva |
| M-20 | 119 | Coeficientes Alpha en prosa con forma «.939» frente a «0.939» en la Tabla 35 |
| M-21 | 89 | Figura 28 con texto de interfaz a 3-4 pt, ilegible en impresión |
| M-22 | 81, 108 | Igualdades dentro de celdas: «(MSD = Saldo / CPA)» y «(Q_entregada = Q_programada)», contrarias al espíritu de la Regla 03 |

### 3.4 Resolución de la compuerta de 300 DPI

La auditoría detectó una discrepancia entre revisores que se resolvió midiendo ambas capas.

| Capa | Resultado |
|---|---|
| DOCX | 44 de las 48 figuras numeradas cumplen, entre 306 y 497 DPI |
| Figuras 1, 2, 6 y 9 | Incumplen de origen: 257, 260, 137 y 183 DPI |
| Escudo de carátula | 118 DPI; no es figura numerada y no le alcanza la compuerta |
| PDF v16 | Las 49 imágenes quedan entre 118 y 260 DPI, la mayoría exactamente en 200 |

**Conclusión:** la reducción del PDF no proviene de las figuras sino de la exportación. Word reduce las imágenes a unas 200-220 ppi al generar el PDF. Son dos remediaciones distintas: regenerar cuatro figuras y reexportar sin reducción de imágenes.

---

## 4. Plan de corrección propuesto para la v17

### Lote A — Corrección editorial nativa, sin intervención del tesista

Comprende los defectos M-01 a M-22 y B-02, más C-06 y C-07 cuando la notación pueda resolverse sin alterar el sentido. Se ejecuta con `scripts/utilidades/docx_quirurgico.py` en una cadena de órdenes única.

### Lote B — Requiere decisión o insumo del tesista

| Punto | Decisión necesaria |
|---|---|
| B-01, p. 3 | ¿Se completa el DNI en el archivo o se deja para manuscrito? |
| B-03 y B-04 | V de Aiken e IVC de la Tabla 34 y del Anexo 3: sin estos coeficientes el vacío no puede cerrarse sin inventar datos |
| B-05, p. 97 | Aportar la captura correcta de la consola o retirar la figura |
| B-06, p. 152 | Aprobar la conversión de las fórmulas de la Tabla 47 a descripción textual |
| C-01 | Aprobar la nota metodológica que distingue el alcance de CP-06 y CP-11 frente a la Tabla 36 |
| C-02 | Confirmar el año de OPS y PATH |
| C-03 | Confirmar si las iteraciones son cuatro o cinco |
| C-05 | Confirmar la condición de los datos y ajustar la nota de la Tabla 35 |

### Lote C — Figuras y exportación

1. Regenerar las Figuras 1, 2, 6 y 9 a 300 DPI como mínimo.
2. Reevaluar la Figura 28, cuyo texto interno resulta ilegible a 3-4 pt.
3. Reexportar el PDF sin reducción de imágenes. Rectificación técnica del 2026-10-21: `Document.ExportAsFixedFormat2` expone `OptimizeForImageQuality=True`, documentado por Microsoft Learn, para conservar la calidad original. Debe comprobarse su disponibilidad en Word y medirse el PDF resultante; no es necesario asumir de antemano que se requiere modificar el registro. Evidencia en `salidas/reportes_maquetacion/exportacion_pdf_calidad_fuente_20261021.json`.

---

## 5. Trazabilidad

Informes de relevo por tramo, con la tabla página por página completa:

- `08_SISTEMA_Y_AGENTES/handoffs/2026-10-21_analista-documental_validacion_hoja_p001_p040.md`
- `08_SISTEMA_Y_AGENTES/handoffs/2026-10-21_maquetador-docx_validacion_hoja_p041_p080.md`
- `08_SISTEMA_Y_AGENTES/handoffs/2026-10-21_analista-documental_validacion_hoja_p081_p120.md`
- `08_SISTEMA_Y_AGENTES/handoffs/2026-10-21_verificador-integridad_validacion_hoja_p121_p159.md`

Insumos de la auditoría:

- `salidas/reportes_maquetacion/v16_paginas/p001.png` a `p159.png`
- `salidas/reportes_maquetacion/v16_texto_por_pagina.md`
- `salidas/reportes_maquetacion/v16_metricas_paginas.json`

Medición de DPI por capa: extracción de las dimensiones en píxeles de cada parte de `word/media/` del DOCX contrastadas con su extensión de presentación, y extracción de las imágenes embebidas del PDF con su rectángulo de dibujo.

---

*Ningún archivo del documento auditado fue modificado durante esta validación. Las mediciones de DPI, los recortes de zoom y las verificaciones de sumas se ejecutaron en modo de solo lectura.*
