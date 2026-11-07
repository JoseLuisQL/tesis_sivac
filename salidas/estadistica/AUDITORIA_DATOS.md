# AUDITORÍA DEL CONJUNTO DE DATOS — SIVAC

> Informe generado por `scripts/estadistica/verificar_conjunto_datos.py`.
> No modifica datos: solo comprueba coherencia, recálculo y sincronía.

**Resultado global:** 115 de 115 comprobaciones superadas

## Resumen por bloque

| Bloque | Comprobaciones | Fallas | Estado |
| :--- | ---: | ---: | :---: |
| A. Estructura | 35 | 0 | OK |
| B. Cronometraje | 12 | 0 | OK |
| C. Auditoría documental | 9 | 0 | OK |
| D. Despachos | 7 | 0 | OK |
| E. Cuestionario TAM | 4 | 0 | OK |
| F. Matriz analítica | 11 | 0 | OK |
| G. Estadística | 5 | 0 | OK |
| H. Coherencia entre instrumentos | 6 | 0 | OK |
| I. Evidencias | 2 | 0 | OK |
| J. Informe final | 10 | 0 | OK |
| K. Libro de anexos (XLSX) | 14 | 0 | OK |

## Detalle

| Bloque | Comprobación | Estado | Detalle |
| :--- | :--- | :---: | :--- |
| A. Estructura | instrumento01_replicas.csv existe | OK |  |
| A. Estructura | instrumento01_replicas.csv: cabecera | OK | columnas en orden |
| A. Estructura | instrumento01_replicas.csv: sin celdas en blanco inesperadas | OK | 224 celdas vacías (pausas, motivos y observaciones pueden estar vacías por diseño) |
| A. Estructura | instrumento02_asientos.csv existe | OK |  |
| A. Estructura | instrumento02_asientos.csv: cabecera | OK | columnas en orden |
| A. Estructura | instrumento02_asientos.csv: sin celdas en blanco inesperadas | OK | 1788 celdas vacías (pausas, motivos y observaciones pueden estar vacías por diseño) |
| A. Estructura | instrumento02_despachos.csv existe | OK |  |
| A. Estructura | instrumento02_despachos.csv: cabecera | OK | columnas en orden |
| A. Estructura | instrumento02_despachos.csv: sin celdas en blanco inesperadas | OK | 0 celdas vacías (pausas, motivos y observaciones pueden estar vacías por diseño) |
| A. Estructura | instrumento03_reactivos.csv existe | OK |  |
| A. Estructura | instrumento03_reactivos.csv: cabecera | OK | columnas en orden |
| A. Estructura | instrumento03_reactivos.csv: sin celdas en blanco inesperadas | OK | 0 celdas vacías (pausas, motivos y observaciones pueden estar vacías por diseño) |
| A. Estructura | matriz_analitica_pre_post.csv existe | OK |  |
| A. Estructura | matriz_analitica_pre_post.csv: cabecera | OK | columnas en orden |
| A. Estructura | matriz_analitica_pre_post.csv: sin celdas en blanco inesperadas | OK | 0 celdas vacías (pausas, motivos y observaciones pueden estar vacías por diseño) |
| A. Estructura | instrumento01_replicas.csv: 168 filas | OK | obtenidas 168 |
| A. Estructura | instrumento02_asientos.csv: 1120 filas | OK | obtenidas 1120 |
| A. Estructura | instrumento02_despachos.csv: 700 filas | OK | obtenidas 700 |
| A. Estructura | instrumento03_reactivos.csv: 224 filas | OK | obtenidas 224 |
| A. Estructura | matriz_analitica_pre_post.csv: 28 filas | OK | obtenidas 28 |
| A. Estructura | instrumento01_replicas.csv: 14 sujetos TRAB-01…TRAB-14 | OK | 14 identificadores |
| A. Estructura | instrumento01_replicas.csv: 28 pares sujeto × momento | OK | 28 pares |
| A. Estructura | instrumento01_replicas.csv: sin espacios sobrantes | OK | sin espacios al inicio ni al final |
| A. Estructura | instrumento02_asientos.csv: 14 sujetos TRAB-01…TRAB-14 | OK | 14 identificadores |
| A. Estructura | instrumento02_asientos.csv: 28 pares sujeto × momento | OK | 28 pares |
| A. Estructura | instrumento02_asientos.csv: sin espacios sobrantes | OK | sin espacios al inicio ni al final |
| A. Estructura | instrumento02_despachos.csv: 14 sujetos TRAB-01…TRAB-14 | OK | 14 identificadores |
| A. Estructura | instrumento02_despachos.csv: 28 pares sujeto × momento | OK | 28 pares |
| A. Estructura | instrumento02_despachos.csv: sin espacios sobrantes | OK | sin espacios al inicio ni al final |
| A. Estructura | instrumento03_reactivos.csv: 14 sujetos TRAB-01…TRAB-14 | OK | 14 identificadores |
| A. Estructura | instrumento03_reactivos.csv: 28 pares sujeto × momento | OK | 28 pares |
| A. Estructura | instrumento03_reactivos.csv: sin espacios sobrantes | OK | sin espacios al inicio ni al final |
| A. Estructura | matriz: una fila por sujeto y momento | OK |  |
| A. Estructura | matriz: centro constante por sujeto | OK | 14 asignaciones |
| A. Estructura | matriz: 13 centros distintos | OK | 13 centros |
| B. Cronometraje | Fin − inicio = duración neta + pausa | OK | 0 descuadres |
| B. Cronometraje | Duración en minutos = segundos ÷ 60 | OK | error máximo 0.000033 min |
| B. Cronometraje | Duraciones positivas y plausibles (45 s – 60 min) | OK | rango 90–2947 s |
| B. Cronometraje | Toda pausa tiene motivo P1–P4 | OK | 56 pausas registradas |
| B. Cronometraje | Sin pausa ⇒ sin motivo | OK | 112 réplicas sin pausa |
| B. Cronometraje | Réplicas en orden cronológico dentro de la sesión | OK | 0 inversiones |
| B. Cronometraje | Ninguna sesión cruza la medianoche | OK |  |
| B. Cronometraje | Ninguna sesión empieza antes de las 06:00 | OK |  |
| B. Cronometraje | Una réplica REG-01…03 y VALE-01…03 por indicador | OK |  |
| B. Cronometraje | Todas las réplicas válidas | OK |  |
| B. Cronometraje | Postest posterior al pretest en los 14 sujetos | OK | 14/14 |
| B. Cronometraje | Folios de documento únicos por centro | OK | 0 duplicados |
| C. Auditoría documental | Criterios binarios S/N | OK |  |
| C. Auditoría documental | Conformidad conjuntiva: conforme ⇔ los 8 criterios cumplen | OK | 0 discrepancias |
| C. Auditoría documental | Motivo solo en documentos no conformes | OK | 0 casos |
| C. Auditoría documental | El motivo coincide con los criterios fallidos | OK | 1120/1120 asientos coherentes |
| C. Auditoría documental | Cantidades positivas | OK |  |
| C. Auditoría documental | Tipo documental del catálogo | OK |  |
| C. Auditoría documental | Numeración de asiento 1…40 por sesión | OK |  |
| C. Auditoría documental | Folio de kardex único por centro | OK | 0 duplicados |
| C. Auditoría documental | Fechas de asiento válidas | OK |  |
| D. Despachos | Diferencia = entregado − programado | OK | 0 descuadres |
| D. Despachos | Concordancia ⇔ diferencia cero | OK | 0 discrepancias |
| D. Despachos | Cantidades programadas positivas | OK |  |
| D. Despachos | Entregas no negativas | OK |  |
| D. Despachos | Despacho sin guía siempre no conforme | OK | 53 despachos sin documento |
| D. Despachos | Guía de remisión única por centro | OK | 0 duplicados |
| D. Despachos | Numeración de despacho 1…25 por sesión | OK |  |
| E. Cuestionario TAM | 8 reactivos por sujeto y momento | OK |  |
| E. Cuestionario TAM | Reactivos AP-01…04 y UP-01…04 | OK | 8 reactivos |
| E. Cuestionario TAM | Valores Likert entre 1 y 5 | OK | rango 1–5 |
| E. Cuestionario TAM | Sumas AP, UP, total y baremo correctos | OK | 0 sesiones con error |
| F. Matriz analítica | t_reg = media de las 3 réplicas | OK | diferencia máxima 0.0000 min |
| F. Matriz analítica | t_vale = media de las 3 réplicas | OK | diferencia máxima 0.0000 min |
| F. Matriz analítica | RSD = conformes ÷ 40 | OK | diferencia máxima 0.0000 pp |
| F. Matriz analítica | CPE = concordantes ÷ 25 | OK | diferencia máxima 0.0000 pp |
| F. Matriz analítica | RSD y CPE dentro de 0–100 % | OK |  |
| F. Matriz analítica | score_ap = suma de los 4 reactivos AP | OK |  |
| F. Matriz analítica | score_up = suma de los 4 reactivos UP | OK |  |
| F. Matriz analítica | score_tam_total = AP + UP | OK |  |
| F. Matriz analítica | Baremo de satisfacción aplicado | OK |  |
| F. Matriz analítica | pretest_campo.csv idéntico a la matriz (Pretest) | OK | 14×18 frente a 14×18; 0 celdas distintas |
| F. Matriz analítica | posttest_campo.csv idéntico a la matriz (Postest) | OK | 14×18 frente a 14×18; 0 celdas distintas |
| G. Estadística | Reporte estadístico presente | OK |  |
| G. Estadística | Descriptivos reproducidos desde los CSV | OK | desviación máxima 0.00e+00 |
| G. Estadística | Shapiro-Wilk sobre diferencias pareadas | OK | desviación máxima en p 0.00e+00 |
| G. Estadística | Estadísticos t pareados reproducidos | OK | desviación máxima 0.00e+00 |
| G. Estadística | Reporte rotulado como datos de prueba | OK | DATOS DE PRUEBA – REEMPLAZAR (DEC-007) |
| H. Coherencia entre instrumentos | Instrumento 02: mismo sujeto, centro, fecha y responsable | OK | 0 sesiones desalineadas |
| H. Coherencia entre instrumentos | Instrumento 02 (despachos): mismo sujeto, centro, fecha y responsable | OK | 0 sesiones desalineadas |
| H. Coherencia entre instrumentos | Instrumento 03: mismo sujeto, centro, fecha y responsable | OK | 0 sesiones desalineadas |
| H. Coherencia entre instrumentos | Asientos anteriores a la sesión de auditoría | OK | 0 fuera de ventana |
| H. Coherencia entre instrumentos | Ventana documental de 1 a 35 días | OK | rango 1–34 días |
| H. Coherencia entre instrumentos | Despachos anteriores a la sesión de conciliación | OK | 0 fuera de ventana |
| I. Evidencias | Registro de sincronización presente | OK |  |
| I. Evidencias | Copias de evidencia con la huella registrada | OK | 22 archivos |
| J. Informe final | Informe final versionado presente | OK | informe_final_v28.docx |
| J. Informe final | Alfas de Cronbach del informe coinciden con el reporte | OK | 6 escalas revisadas |
| J. Informe final | Descriptivos del informe coinciden con el reporte | OK | 21 filas |
| J. Informe final | Contrastes del informe coinciden con el reporte | OK | 14 filas |
| J. Informe final | Decisión por hipótesis consistente con Holm | OK | HE1-HE3 revisadas |
| J. Informe final | Matrices pretest y postest del anexo presentes | OK | 2 matrices |
| J. Informe final | Matriz pretest del anexo igual a los CSV | OK | 14 sujetos |
| J. Informe final | Matriz postest del anexo igual a los CSV | OK | 14 sujetos |
| J. Informe final | Figuras del informe son las figuras vigentes | OK | 3 figuras |
| J. Informe final | El informe advierte que son datos de prueba | OK | informe=sí; reporte=DATOS DE PRUEBA – REEMPLAZAR (DEC-007) |
| K. Libro de anexos (XLSX) | Libro de tablas de anexos presente | OK | TABLAS_ANEXOS_SIVAC.xlsx |
| K. Libro de anexos (XLSX) | Hojas del libro en el orden previsto | OK | 12 hojas |
| K. Libro de anexos (XLSX) | Registro de paridad del libro presente | OK |  |
| K. Libro de anexos (XLSX) | Portada identifica el informe vigente | OK | informe_final_v28.docx |
| K. Libro de anexos (XLSX) | Portada declara el total de tablas del informe | OK | se esperaban 84 tablas |
| K. Libro de anexos (XLSX) | El libro no cita versiones anteriores del informe | OK |  |
| K. Libro de anexos (XLSX) | Registro de paridad coherente con el libro | OK | informe_final_v28.docx |
| K. Libro de anexos (XLSX) | Matriz pretest igual a los CSV de campo | OK | 14 sujetos × 18 columnas |
| K. Libro de anexos (XLSX) | Matriz postest igual a los CSV de campo | OK | 14 sujetos × 18 columnas |
| K. Libro de anexos (XLSX) | Descriptivos del libro coinciden con el reporte | OK | 21 filas |
| K. Libro de anexos (XLSX) | Alfas e intervalos del libro coinciden con el reporte | OK | 6 escalas |
| K. Libro de anexos (XLSX) | Shapiro-Wilk del libro coincide con el reporte | OK | 7 indicadores |
| K. Libro de anexos (XLSX) | Contrastes del libro coinciden con el reporte | OK | 7 t pareadas y 7 Wilcoxon |
| K. Libro de anexos (XLSX) | El libro rotula los datos como de prueba | OK |  |
