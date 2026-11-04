---
tipo: instrumento
fase: F8
agente: maquetador-docx
estado: borrador
fecha: 2026-11-03
---

| [Logotipo UNAJMA] | **UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS**<br>Facultad de Ingeniería<br>Escuela Profesional de Ingeniería de Sistemas | [Logotipo EPIS] |
|---|---|---|

# Guía de aplicación de los instrumentos

**Archivo:** `00_GUIA_DE_APLICACION_v06.docx`. **Orden de aplicación:** 00. **Páginas:** 1.

## Función en el trabajo de campo

No mide: ordena la aplicación de los cinco instrumentos y fija las reglas operativas del trabajo de campo.

## Estructura

- Instrumentos
- Los cuatro instantes y las dos fórmulas
- Reglas operativas

## Geometría de las tablas

- Instrumentos: 3.1, 4.0, 4.6 y 3.8 cm
- Instantes y fórmulas: 3.1 y 12.4 cm
- Reglas operativas: 3.6 y 11.9 cm

## Cambios respecto de v05

- Una sola definición por indicador: T_reg = corte de registro − inicio; T_vale = emisión − solicitud de despacho.
- Once reglas operativas: réplicas y mediana, interrupción externa, documento conforme (ocho criterios), despacho conforme (igualdad exacta), hoja de continuación, doble codificación del 20 %, trabajador ausente, dos centros, operación no ocurrida, numeración y cálculo de porcentajes.

## Producción

A4 vertical; margen izquierdo 3.0 cm; superior 3.0 cm; derecho e inferior 2.5 cm; ancho útil 15.5 cm; distancia del encabezado 0.8 cm. Banda institucional de tres celdas de 2.4, 10.7 y 2.4 cm en `word/header1.xml`, con altura de fila exacta de 2.0 cm, ambos logotipos a 1.6 cm y `vAlign` centrado; el cuerpo no contiene imágenes. Times New Roman 10 pt en el cuerpo y 9.5 pt en las tablas; ninguna fuente por debajo de 9.5 pt. Bordes: contorno y separadores horizontales nativos en las tablas de captura —`w:top`, `w:left`, `w:bottom`, `w:right`, `w:insideH`—, con `w:insideV` solo en las columnas de marcado, de modo que los campos de texto quedan abiertos para escribir de corrido; el contorno dobla el grosor de las separaciones internas. La fila de encabezado va sombreada en gris claro y la columna de numeración como carril de lectura. Todas las filas con `cantSplit`; la fila de encabezado con `tblHeader`. Cero OMML, cero tablas flotantes y cero códigos internos visibles.

## Control medido

- Bordes verticales dibujados: 12 (contorno de cada tabla y separadores de las columnas de marcado).
- Tablas flotantes: 0.
- OMML: 0.
- Fuente mínima: 9.5 pt; en tablas: 9.5 pt.
- Altura mínima de fila de captura: None cm.
- Holgura inferior: 0.74 cm.
- SHA-256 del DOCX: `becc4cd91fb6d6294e292434d039a7dcb5838681e8594cc8db7e6143c6c76ae3`.

## Límites que el maquetador no debe cruzar

No se altera ni se reordena el contenido de los ítems, los criterios de conformidad ni las escalas. No se añaden ni se quitan filas, columnas o documentos. No se escribe ningún código interno en el formulario. No se colocan fórmulas ni objetos matemáticos en las celdas. No se rellena ninguna casilla.

Esta nota no se imprime.
