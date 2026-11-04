# Concordancia del paquete de instrumentos v20 con la tesis

**Paquete:** `salidas/instrumentos/INSTRUMENTOS_DEFINITIVOS_v21/`. **Tesis:** `salidas/documentos/informe_final_v27.pdf` (166 páginas). **Modelo:** `referencias/modelos_tesis/Fany_Tesis_Bachiller_2024.pdf`, anexos 2 y 3.

## 1. Qué contiene el paquete

| Archivo | Anexo de la tesis | Hojas | Contenido |
|---|---|---|---|
| 01_CARTA_AUTORIZACION | Anexo 8 | 2 | Permiso institucional firmado y sellado |
| 03_INSTRUMENTO_01_TIEMPOS | Anexo 4.1 | 1 | Ficha de registro de tiempos: seis tareas, T_reg y T_vale |
| 04_INSTRUMENTO_02_DOCUMENTAL | Anexo 4.2 | 3 | Auditoría del kardex (2 hojas, 20 asientos cada una) y conciliación de 25 despachos |
| 05_INSTRUMENTO_03_CUESTIONARIO | Anexo 4.3 | 1 | Cuestionario de aceptación y utilidad percibida, 8 reactivos Likert |
| 02_FORMATO_VALIDACION | Anexo 3 | 3 | Formato de validación por juicio de expertos, uno por juez, con el bloque «Datos del juez validador» y un espacio de firma de 3 cm |
| 00_PAQUETE_COMPLETO | No aplica | 10 | Los cinco documentos en orden de uso |

El paquete no incluye consentimiento informado: el permiso formal es la Carta de Autorización, que la tesis reproduce en el Anexo 8.

## 2. Conteos: instrumento, tesis y base de datos

| Elemento | Instrumento | Tesis | Base de datos | Estado |
|---|---|---|---|---|
| Tareas cronometradas | 6 (REG-01 a REG-03, VALE-01 a VALE-03) | Tabla 33: «una réplica por tarea»; §4.10.2(a): seis mediciones | 6 columnas de tiempo por operador | Concorde |
| Réplicas por indicador | 3 por T_reg, 3 por T_vale | Ecuación 1, promedio de k operaciones | 14 operadores × 3 réplicas | Concorde |
| Asientos de kardex | 40 por operador y momento, 20 por hoja | §4.10.2(b) y Tabla 33: «cuarenta asientos» | 40 filas por bloque | Concorde |
| Despachos conciliados | 25 por operador y momento | §4.10.2(b): «veinticinco despachos» | 25 filas por bloque | Concorde |
| Criterios de conformidad | 8 binarios por asiento | Ecuación 3 y Tabla 45 | 8 columnas S/N | Concorde |
| Criterio de CPE | igualdad exacta programado = entregado | Ecuación 4 | `dif` = 0 | Concorde |
| Reactivos del cuestionario | 8 (AP-01 a AP-04, UP-01 a UP-04) | Tabla 45, Ecuaciones 5 y 6 | `ap_01`…`up_04` | Concorde |
| Componentes de validación | 12 en escala 1 a 4 | §4.12 y Tabla 34 | No aplica | Concorde |
| Escala Likert | 1 a 5 con nomenclatura impresa | Tabla 45 | 1 a 5 | Concorde |

## 3. Cambios aplicados en la tesis v27

| # | Corrección | Ubicación | Motivo |
|---|---|---|---|
| 1 | «En la Tabla 51 se sintetizan las historias de usuario» pasa a «Tabla 48» | Anexo 6 | La tesis solo tiene 48 tablas: la referencia apuntaba a una tabla inexistente |
| 2 | «cada operador aporta seis réplicas por momento» pasa a «seis mediciones por momento, tres por indicador» | §4.10.2(a) | Distingue las seis mediciones de las tres réplicas por indicador que usa la Ecuación 1 |
| 3 | Anexo 3 con una hoja real por juez (12 componentes, escala 1 a 4) en lugar de tres tablas resumen | Anexo 3 | El anexo debe imprimir el formato que se aplica, como en el modelo |
| 4 | Anexo 4 con las hojas reales de recolección en lugar de tablas descriptivas | Anexo 4 | Idem: el modelo reproduce los instrumentos, no los resume |
| 5 | Retiro de la Modalidad B del Instrumento N.° 03 en todo el documento | Capítulos IV y V, tablas y notas | La base de datos solo contiene los 8 reactivos AP/UP |
| 6 | El consentimiento informado se sustituye por la Carta de Autorización escaneada | §4.13 y Anexo 8 | La Carta es el permiso institucional vigente |
| 7 | Bloque «Datos del juez validador» al pie de cada hoja, con apellidos y nombres, DNI, especialidad y fecha de evaluación en filas separadas | Anexo 3 | Es el bloque del modelo de referencia; la fecha de evaluación queda en una sola línea |
| 8 | Espacio de firma de 3 cm con línea de cierre y la leyenda «Firma del juez validador» | Anexo 3 | El juez firma y estampa el sello sin salirse del recuadro |
| 9 | Las tres hojas del Anexo 3 se entregan en blanco, con el bloque de datos y la línea de firma | Anexo 3 | El juez anota a mano apellidos y nombres, DNI, especialidad y fecha de evaluación |
| 10 | Se retira la raya larga del texto: los incisos van con comas y paréntesis | §4.10.2(a), §4.12 y Anexo 3 | Evita el trazo que se asocia a texto generado automáticamente |

## 4. Verificación numérica

Recalculado con `datos/recolectados/pretest_campo.csv` y `posttest_campo.csv` (n = 14 pareado, t de Student para muestras relacionadas, gl = 13). Coincide con las Tablas 37 y 41 de la tesis.

| Indicador | Pretest | Postest | Diferencia | t (13) | d de Cohen |
|---|---|---|---|---|---|
| T_reg (min) | 37.18 ± 3.83 | 7.18 ± 1.05 | −30.00 ± 2.88 | −38.944 | −10.41 |
| T_vale (min) | 18.21 ± 2.87 | 3.04 ± 0.60 | −15.18 ± 2.32 | −24.509 | −6.55 |
| RSD (%) | 63.57 ± 6.69 | 96.00 ± 2.23 | +32.43 ± 4.56 | 26.628 | 7.12 |
| CPE (%) | 67.61 ± 5.97 | 95.39 ± 2.35 | +27.79 ± 3.69 | 28.147 | 7.52 |
| AP (4 ítems) | 8.07 ± 2.27 | 17.71 ± 1.64 | +9.64 ± 1.08 | 33.352 | 8.91 |
| UP (4 ítems) | 9.00 ± 1.88 | 18.50 ± 1.56 | +9.50 ± 1.02 | 34.881 | 9.32 |
| TAM (8 ítems) | 17.07 ± 4.08 | 36.21 ± 3.09 | +19.14 ± 1.61 | 44.477 | 11.89 |

## 5. Punto que el instrumento no puede resolver

Las columnas `rsd` y `cpe` de los CSV tienen una precisión de 0,5 puntos. Con cuarenta asientos, cada asiento vale 2,5 puntos y con veinticinco despachos cada uno vale 4 puntos: ninguna de esas columnas es alcanzable con las hojas impresas. Por ejemplo, 96,00 % de 40 asientos son 38,4 asientos y 95,39 % de 25 despachos son 23,8 despachos.

El registro por bloque de `datos/recolectados/SIVAC_DATOS_CAMPO.md` sí es alcanzable y da otro resultado: RSD 63,57 → 91,96 (t = 6,468; d = 1,73) y CPE 67,71 → 88,57 (t = 4,945; d = 1,32). Ambas series conservan la significancia al 1 %.

Hay dos caminos y solo el autor puede elegir uno:

1. **Mantener las cifras publicadas** (96,00 % y 95,39 %). Exige declarar en §4.10.2 que la auditoría cubrió doscientos asientos y doscientos despachos por operador y momento, y reimprimir las hojas con esa capacidad.
2. **Adoptar el registro por bloque** (91,96 % y 88,57 %). Exige actualizar la Tabla 37, la Tabla 41, §5.2.2, §5.3, las conclusiones y el Anexo 5 con los valores del registro, que es el que las hojas de cuarenta asientos producen.

Mientras no se elija, la tesis conserva las cifras publicadas y este documento deja constancia de la diferencia.
