---
tipo: especificacion
fase: F8
agente: director-general
estado: aprobada_por_tesista
fecha: 2026-11-02
---

# PLANTILLA MAESTRA DE INSTRUMENTOS v05 (PMI-05)

> Documento normativo único para los seis instrumentos del paquete `INSTRUMENTOS_DEFINITIVOS_v05`.
> Toda recompilación debe respetar estas reglas sin excepción. Las diferencias de contenido entre
> instrumentos se permiten; las diferencias de forma, no.

## 1. Página, márgenes y encabezado

| Parámetro | Valor |
|---|---|
| Tamaño | A4 vertical |
| Márgenes | izquierdo 3.0 cm; superior 3.0 cm; derecho 2.5 cm; inferior 2.5 cm |
| Ancho útil | 15.5 cm (8788 dxa) |
| Distancia del encabezado | 0.8 cm (454 dxa) |
| Banda de encabezado | 3 celdas de 2.4 / 10.7 / 2.4 cm; alto de fila exacto 2.0 cm |
| Logotipos | 1.6 cm de alto, iguales; viven en `word/header1.xml` con `headerReference` |
| Cuerpo | sin ninguna imagen |

El encabezado es idéntico en los seis documentos: logotipo UNAJMA, bloque institucional centrado en tres líneas y logotipo de la escuela, sin rejilla.

## 2. Tipografía

| Elemento | Regla |
|---|---|
| Familia | Times New Roman en todo el documento |
| Cuerpo | 10 pt (`w:sz=20`) |
| Tablas | 9.5 pt (`w:sz=19`) |
| Mínimo absoluto | 9.5 pt; ninguna reducción para hacer caber contenido |
| Interlineado | sencillo exacto de 12 pt en tablas; 12 pt exacto en prosa de formulario |
| Párrafos | justificados, sin sangría de primera línea, espacio anterior y posterior 0 salvo lo indicado |

## 3. Ritmo vertical unificado

Toda sección respeta esta jerarquía de espaciado, sin excepciones por documento:

| Nivel | Formato | Espacio anterior | Espacio posterior |
|---|---|---|---|
| Título del documento | negrita 14 pt, izquierda, sin sangría | 12 pt | 2 pt |
| Subtítulo «Ficha técnica» | negrita 10 pt, izquierda | 8 pt | 2 pt |
| Rótulo de sección romana (I, II, III, IV, V) | negrita 10 pt, izquierda | 12 pt | 4 pt |
| Rótulo de bloque (Bloque A, Bloque B) | negrita 10 pt, izquierda | 8 pt | 4 pt |
| Prosa de instrucciones | 10 pt justificado | 2 pt | 2 pt |
| Línea de conteo | negrita 10 pt | 4 pt | 8 pt |
| Tabla | — | 0 | 0 |

Ningún rótulo queda pegado al elemento anterior: el espacio mínimo entre el borde inferior de una tabla y el siguiente rótulo es de 12 pt.

## 4. Ficha técnica — formato único

Tabla de **dos columnas** «Campo | Valor», anchos 3.5 y 12.0 cm, rejilla visible, cuatro filas fijas en este orden:

1. Variable
2. Dimensión
3. Indicador
4. Aplicación

Aplica a los instrumentos 01, 02, 03 y 05. La guía 00 y el consentimiento 04 no llevan ficha técnica.

## 5. Datos generales — formato único

Tabla de **dos columnas** «Campo | Registro», anchos 4.0 y 11.5 cm, rejilla visible, filas de 0.6 cm.

- Instrumentos 01, 02 y 03: N.° de trabajador, Centro de salud, Fecha, Momento.
- Instrumento 04: N.° de trabajador, Centro de salud, Fecha.
- Instrumento 05: Apellidos y nombres, DNI, Especialidad, Institución, Fecha.

Se elimina la disposición de cuatro columnas con campos alternados.

## 6. Tablas de contenido

- Rejilla visible en todas las celdas de los formularios de captura.
- Alto mínimo de fila 0.6 cm en tablas de marcado o llenado; 0.68 cm en tablas de escritura manuscrita.
- Fila de encabezado repetida (`w:tblHeader`) y filas no fragmentables (`w:cantSplit`).
- Sin sombreado, sin fórmulas, sin objetos matemáticos y sin códigos internos.
- Números de fila centrados; texto a la izquierda.

La guía 00 conserva sus dos tablas de referencia con las tres líneas horizontales APA 7, por ser documento normativo y no formulario.

## 7. Cierre unificado

Salvo el consentimiento 04, todo instrumento que recoge datos cierra con esta secuencia:

**IV. Observaciones**
Recuadro vacío a todo el ancho (15.5 cm), alto 2.0 cm, borde visible en los cuatro lados, sin rótulo interno.

**V. Responsable**
Tabla de dos columnas «Campo | Registro», anchos 4.0 y 11.5 cm, tres filas: Nombre del observador, Firma, Fecha («____ / ____ / ____»).

Excepciones:
- **04 Consentimiento:** cierra con «III. Firmas», tabla de dos columnas iguales 7.75 y 7.75 cm, con Nombre, Firma y Fecha de participante e investigador.
- **05 Certificado:** cierra con «IV. Observaciones y opinión de aplicabilidad» y «V. Firma», con la línea de rúbrica de 7.35 cm y el rótulo «Firma y sello del juez validador»; sin línea de DNI, porque ya se captura en los datos del juez.

## 8. Marcas y campos de llenado

- Casilla ☐ siempre unida a su texto con espacio duro (U+00A0); jamás se separan ni se alinean en columnas de anchura fija.
- Series de guiones bajos de longitud uniforme dentro de un mismo bloque; una serie nunca se parte en dos renglones.
- Opciones de marcado en renglones independientes o con separación mínima de 12 pt entre casillas.

## 9. Paginación

- Objetivo: una página por instrumento, salvo el certificado 05, que ocupa dos por la matriz de catorce ítems.
- Si un instrumento no cabe, se reduce primero la casilla de observaciones hasta 1.8 cm, luego el alto de fila hasta el mínimo de la sección 6; nunca se reduce la tipografía ni se elimina contenido.
- Ningún documento puede cerrar con menos de 0.4 cm de holgura inferior.

## 10. Prohibiciones

- No rellenar casillas, nombres, documentos, firmas ni fechas.
- No alterar, añadir, quitar ni reordenar enunciados, ítems o dimensiones.
- No introducir escala distinta de la fijada por DEC-015 y DEC-024 (Pertinencia, Relevancia y Claridad dicotómicas; satisfacción en escala 1 a 5).
- No modificar los otros documentos fuera del alcance de esta plantilla.
