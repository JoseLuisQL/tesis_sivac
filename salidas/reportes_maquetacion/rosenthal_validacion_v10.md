# Validación del recálculo de la r de Rosenthal sobre el informe final v10

**Documento base:** `salidas/documentos/informe_final_v10.docx` (solo lectura, sin modificaciones).

**Fórmula corregida:** r = |Z| / sqrt(N), donde N es el número de pares válidos con diferencia distinta de cero (N = 14).

**Fórmula previa:** r = |Z| / sqrt(2N), que producía 0.623 en los siete indicadores.

El estadístico Z no se modifica. Cada valor corregido se obtuvo dividiendo el Z original entre la raíz cuadrada de N; no se aplicó un factor de conversión directo a la cifra previa.

## 1. Tabla de recálculo

| Indicador | Z | N | r anterior | r correcto | Magnitud (Cohen, 1988) |
|---|---:|---:|---:|---:|---|
| Tiempo de registro (T_reg) | -3.296 | 14 | 0.623 | 0.881 | Grande (r >= 0.50) |
| Tiempo de emisión de vales (T_vale) | -3.296 | 14 | 0.623 | 0.881 | Grande (r >= 0.50) |
| Registros sin discrepancias (RSD) | -3.296 | 14 | 0.623 | 0.881 | Grande (r >= 0.50) |
| Concordancia programada vs entregada (CPE) | -3.296 | 14 | 0.623 | 0.881 | Grande (r >= 0.50) |
| Aceptación del proceso (AP) | -3.296 | 14 | 0.623 | 0.881 | Grande (r >= 0.50) |
| Utilidad percibida (UP) | -3.296 | 14 | 0.623 | 0.881 | Grande (r >= 0.50) |
| Puntaje global TAM (AP + UP) | -3.296 | 14 | 0.623 | 0.881 | Grande (r >= 0.50) |

**Comprobación aritmética:** 3.296 / sqrt(14) = 3.296 / 3.741657 = 0.8808, que se reporta como 0.881. El valor previo, 3.296 / sqrt(28) = 3.296 / 5.291503 = 0.6228, se reportaba como 0.623.

## 2. Ubicaciones corregidas en el DOCX

| Ubicación | Texto previo | Texto corregido |
|---|---|---|
| Tabla 40, filas 3 y 5, columna 5 | r = 0.62 (grande) | r = 0.881 (grande) |
| Tabla 41, filas 3 y 5, columna 5 | r = 0.62 (grande) | r = 0.881 (grande) |
| Tabla 42, filas 3, 5 y 7, columna 5 | r = 0.62 (grande) | r = 0.881 (grande) |
| Párrafo 686 | r de Rosenthal de 0.62; r de Rosenthal = 0.62 | r de Rosenthal de 0.881; r de Rosenthal = 0.881 |
| Párrafo 689 (nota Tabla 40) | (|Z| / sqrt(2n)) | (|Z| / sqrt(N)), donde N es el número de pares válidos |
| Párrafo 692 | r de Rosenthal de 0.62; r = 0.62 | r de Rosenthal de 0.881; r = 0.881 |
| Párrafo 698 | r = 0.62 (AP); r = 0.62 (UP) | r = 0.881 (AP); r = 0.881 (UP) |
| Párrafo 701 (nota Tabla 42) | r > 0.60 | r >= 0.50 |
| Párrafo 705 (decisión general) | r > 0.60 | r >= 0.50 |

Las filas y columnas de las tablas se expresan en base 1, contando la fila de encabezado como fila 1.

## 3. Coherencia con el resto del documento

- La Ecuación 11 ya formula r = |Z| / sqrt(N_válidos); no requiere cambios.
- La Tabla 44 (matriz de consistencia) ya declara el tamaño del efecto como r = |Z| / sqrt(N); no requiere cambios.
- El párrafo 639 ya define la división entre la raíz cuadrada del número de pares válidos; no requiere cambios.
- Ninguna frase del documento califica el efecto de r como mediano. Las expresiones existentes de efecto grande son compatibles con el valor corregido de 0.881.

## 4. Alcance de la corrección

- Se emiten 16 órdenes quirúrgicas en `salidas/reportes_maquetacion/rosenthal_v10_ordenes.json`: siete celdas de tabla y nueve sustituciones en párrafos y notas.
- El libro `salidas/estadistica/TABLAS_ANEXOS_SIVAC_v2.xlsx` fue regenerado con r = 0.881 en las hojas `12_CONTRASTES` y `14_SPSS_SALIDAS`, y con la nota de fórmula corregida.
- No se alteraron p-valores, estadísticos t o W, medias, desviaciones estándar, tamaños del efecto d de Cohen ni decisiones de hipótesis.
- El DOCX v10 no fue editado; la aplicación de las órdenes corresponde al maquetador.
