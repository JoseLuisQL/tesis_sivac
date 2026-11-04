---
tipo: instrumento
fase: F8
agente: maquetador-docx
estado: borrador
fecha: 2026-11-03
---

| [Logotipo UNAJMA] | **UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS**<br>Facultad de Ingeniería<br>Escuela Profesional de Ingeniería de Sistemas | [Logotipo EPIS] |
|---|---|---|

# Ficha de tiempos

**Archivo:** `01_FICHA_TIEMPOS_v06.docx`. **Orden de aplicación:** 01. **Páginas:** 1.

## Función en el trabajo de campo

Oportunidad de procesamiento: tiempo de registro (T_reg) y tiempo de emisión del comprobante o vale (T_vale), en minutos.

## Estructura

- I. Datos generales
- II. Instrucciones
- III. Contenido
- IV. Observaciones
- V. Responsable

## Geometría de las tablas

- Datos generales: 3.3, 3.5, 2.5 y 6.2 cm
- Bloques A y B: 0.8, 3.9, 2.5, 2.8, 2.5 y 3.0 cm
- Observaciones: 15.5 cm
- Responsable: 4.1, 4.9, 1.6 y 4.9 cm

## Cambios respecto de v05

- El bloque A admite tres réplicas de T_reg y el bloque B tres de T_vale; la fila identifica el escenario (ingreso, salida, transferencia; vale regular, reposición, transferencia).
- Se añade la columna «Solicitud de despacho», de modo que T_vale = emisión − solicitud, como en la Ecuación 2.
- Se elimina la ficha técnica: sus datos ya están en la guía y en las instrucciones, y no se llenan en campo.
- Cada fila de medición mide 1.0 cm y la hoja cabe en una página.

## Producción

A4 vertical; margen izquierdo 3.0 cm; superior 3.0 cm; derecho e inferior 2.5 cm; ancho útil 15.5 cm; distancia del encabezado 0.8 cm. Banda institucional de tres celdas de 2.4, 10.7 y 2.4 cm en `word/header1.xml`, con altura de fila exacta de 2.0 cm, ambos logotipos a 1.6 cm y `vAlign` centrado; el cuerpo no contiene imágenes. Times New Roman 10 pt en el cuerpo y 9.5 pt en las tablas; ninguna fuente por debajo de 9.5 pt. Bordes: contorno y separadores horizontales nativos en las tablas de captura —`w:top`, `w:left`, `w:bottom`, `w:right`, `w:insideH`—, con `w:insideV` solo en las columnas de marcado, de modo que los campos de texto quedan abiertos para escribir de corrido; el contorno dobla el grosor de las separaciones internas. La fila de encabezado va sombreada en gris claro y la columna de numeración como carril de lectura. Todas las filas con `cantSplit`; la fila de encabezado con `tblHeader`. Cero OMML, cero tablas flotantes y cero códigos internos visibles.

## Control medido

- Bordes verticales dibujados: 48 (contorno de cada tabla y separadores de las columnas de marcado).
- Tablas flotantes: 0.
- OMML: 0.
- Fuente mínima: 9.5 pt; en tablas: 9.5 pt.
- Altura mínima de fila de captura: 1.0 cm.
- Holgura inferior: 0.79 cm.
- SHA-256 del DOCX: `e74eabf4fe8e6738e01e99429357397dbaf77698146d390cfdda1eca2edc7153`.

## Límites que el maquetador no debe cruzar

No se altera ni se reordena el contenido de los ítems, los criterios de conformidad ni las escalas. No se añaden ni se quitan filas, columnas o documentos. No se escribe ningún código interno en el formulario. No se colocan fórmulas ni objetos matemáticos en las celdas. No se rellena ninguna casilla.

Esta nota no se imprime.
