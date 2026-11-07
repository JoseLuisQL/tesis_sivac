# CONJUNTO INTEGRAL DE DATOS — SISTEMA SIVAC

## Registro pretest - postest y análisis estadístico en centros de acopio de vacunas

> **Estado del conjunto:** `DATOS DE PRUEBA — REEMPLAZAR (DEC-007)`.
> Las cifras de este documento se derivan del conjunto sintético reproducible de
> `datos/prueba_sintetica/` (semilla 20261026) y **no acreditan medición de
> campo**. La estructura, los identificadores y las reglas de cálculo son los
> definitivos; los valores deben reemplazarse por el registro de campo antes de
> la sustentación.

## Índice

- [Parte 0. Presentación del conjunto de datos y consideraciones metodológicas](#parte-0)
- [Parte 1. Padrón de las catorce unidades censales](#parte-1)
- [Parte 2. Definiciones operacionales de las tres dimensiones (DEC-007)](#parte-2)
- [Parte 3. Instrumento 1 — Ficha de observación de tiempos](#parte-3)
- [Parte 4. Instrumento 2 — Ficha de auditoría documental y conciliación de entregas](#parte-4)
- [Parte 5. Instrumento 3 — Cuestionario de satisfacción del usuario (TAM)](#parte-5)
- [Parte 6. Matriz de indicadores por unidad y diferencias pareadas](#parte-6)
- [Parte 7. Tablas 35 a 43 — Resultados estadísticos inferenciales](#parte-7)
- [Parte 8. Análisis de consistencia operativa y observaciones de campo](#parte-8)

---

<a id="parte-0"></a>
## Parte 0. Presentación del conjunto de datos y consideraciones metodológicas

El presente documento consolida el registro íntegro de las mediciones del estudio de evaluación del Sistema de Información de Vacunas (SIVAC). El diseño es preexperimental, con pretest (proceso manual tradicional en papel) y postest (proceso automatizado con SIVAC) en un solo grupo, administrado a catorce unidades censales de operadores en trece centros de acopio y establecimientos de salud de la red asistencial. El conjunto publicado es el de prueba rotulado en el encabezado: se reproduce desde las fichas crudas con la semilla 20261026 y se sustituye por el registro de campo definitivo sin alterar la estructura ni las reglas de cálculo.

### Resumen de parámetros operacionales del estudio

| Dimensión / Indicador | Unidad de medida | Pretest (Proceso Manual) | Postest (Sistema SIVAC) | Alcance muestral |
| :--- | :--- | :---: | :---: | :--- |
| **D1. Oportunidad de procesamiento** |  |  |  |  |
| Tiempo de registro de movimientos (T_reg) | Minutos (Media ± DE) | 37.18 ± 3.83 | 5.68 ± 0.47 | 14 operadores × 3 réplicas (84 mediciones) |
| Tiempo de emisión de vales (T_vale) | Minutos (Media ± DE) | 18.21 ± 2.87 | 1.92 ± 0.19 | 14 operadores × 3 réplicas (84 mediciones) |
| **D2. Consistencia documental** |  |  |  |  |
| Registros sin discrepancias (RSD) | Porcentaje (%) | 63.57 ± 6.77 | 96.07 ± 2.54 | 14 operadores × 40 expedientes (560 documentos) |
| Concordancia programada vs. entregada (CPE) | Porcentaje (%) | 67.71 ± 6.92 | 94.57 ± 2.53 | 14 operadores × 25 expedientes (350 documentos) |
| **D3. Satisfacción del usuario** |  |  |  |  |
| Aceptación del proceso (AP) | Puntos (1–20) | 8.07 ± 2.27 | 18.64 ± 1.60 | 14 operadores (4 reactivos Likert) |
| Utilidad percibida (UP) | Puntos (1–20) | 9.00 ± 1.88 | 18.43 ± 1.70 | 14 operadores (4 reactivos Likert) |
| Puntaje global TAM | Puntos (8–40) | 17.07 ± 4.08 | 37.07 ± 3.15 | 14 operadores (4 reactivos Likert) |
| **Cobertura total del estudio** | — | **Línea base manual** | **Fase con SIVAC** | **14 operadores censales / 13 centros de acopio** |

*Nota.* Las medias y desviaciones estándar se calculan sobre las catorce unidades censales; en los tiempos, sobre el promedio de las tres réplicas de cada operador y fase. Elaboración propia.

### Criterios y reglas de cálculo

1. **Tiempos operativos (T_reg y T_vale):** promedio aritmético de tres réplicas independientes cronometradas por operador en cada fase de observación.
2. **Registros sin discrepancias (RSD):** cociente entre los documentos conformes (que cumplen simultáneamente los ocho criterios de auditoría) y el total auditado (40), expresado en porcentaje.
3. **Concordancia programada vs. entregada (CPE):** porcentaje de despachos conciliados sin diferencias entre la cantidad programada y la física entregada sobre un total de 25 despachos evaluados.
4. **Satisfacción del usuario (AP, UP y TAM):** AP y UP son la suma de cuatro reactivos Likert de 1 a 5 puntos; el puntaje global TAM es la suma directa de ambas subescalas (rango de 8 a 40 puntos).
5. **Criterio de contraste inferencial:** la prueba decisoria se selecciona según la normalidad de las diferencias pareadas ($D = \text{postest} - \text{pretest}$) evaluada con Shapiro-Wilk: t de Student pareada cuando $p > .05$ y Wilcoxon de rangos con signo cuando $p \le .05$.
6. **Método de cálculo en Wilcoxon:** método exacto por permutación ante la ausencia de empates o diferencias nulas, y método asintótico con corrección por continuidad y empates cuando existen ligaduras en las diferencias.
7. **Control del error tipo I:** ajuste secuencial de Holm-Bonferroni sobre los siete contrastes de la familia.
8. **Precisión de registro:** las duraciones se expresan en minutos con cuatro cifras decimales en la ficha cronométrica (Parte 3) y con dos cifras decimales en la matriz analítica (Partes 0 y 6), que es la precisión con la que el pipeline estadístico lee los datos.
9. **Diferencia de despacho (Dif.):** entregado menos programado. Un valor negativo indica faltante y uno positivo, exceso entregado; la entrega es concordante solo cuando la diferencia es cero.

---

<a id="parte-1"></a>
## Parte 1. Padrón de las catorce unidades censales

La población evaluada es censal: comprende la totalidad de catorce operadores distribuidos en trece centros de acopio y establecimientos de salud de la red asistencial. La sede ALMACÉN (CHANKA) cuenta con dos operadores asignados al mismo punto logístico, por lo que el número de centros y el de unidades evaluadas difieren levemente. El padrón individualiza a los trabajadores, establecimientos, observadores de campo y las fechas de administración para ambas fases.

| Sujeto | Centro de acopio | Código | Observador | Pretest | Postest |
| :--- | :--- | :---: | :---: | :---: | :---: |
| TRAB-01 | ALMACÉN (CHANKA) | CHANKA-001 | OBS-01 | 10/08/2026 | 12/10/2026 |
| TRAB-02 | ALMACÉN (CHANKA) | CHANKA-001 | OBS-02 | 10/08/2026 | 12/10/2026 |
| TRAB-03 | Hospital Andahuaylas | S/C | OBS-01 | 11/08/2026 | 13/10/2026 |
| TRAB-04 | Hospital ESSALUD Andahuaylas | 11214 | OBS-02 | 11/08/2026 | 13/10/2026 |
| TRAB-05 | Centro de Salud Andahuaylas | 6804 | OBS-01 | 12/08/2026 | 14/10/2026 |
| TRAB-06 | Talavera | 4195 | OBS-02 | 12/08/2026 | 14/10/2026 |
| TRAB-07 | San Jeronimo | 4167-SJ | OBS-01 | 13/08/2026 | 15/10/2026 |
| TRAB-08 | Huancaray | 4158 | OBS-02 | 13/08/2026 | 15/10/2026 |
| TRAB-09 | Chicmo | 4202 | OBS-01 | 14/08/2026 | 16/10/2026 |
| TRAB-10 | Huancabamba | 4172 | OBS-02 | 14/08/2026 | 16/10/2026 |
| TRAB-11 | Pampachiri | 4167 | OBS-01 | 07/09/2026 | 19/10/2026 |
| TRAB-12 | San Antonio de Cachi | 4160 | OBS-02 | 07/09/2026 | 19/10/2026 |
| TRAB-13 | Turpo | 4163 | OBS-01 | 08/09/2026 | 20/10/2026 |
| TRAB-14 | Kishuara | 4183 | OBS-02 | 08/09/2026 | 20/10/2026 |

*Nota.* Padrón censal de operadores y centros de acopio evaluados durante las fases de pretest y postest. Elaboración propia.

---

<a id="parte-2"></a>
## Parte 2. Definiciones operacionales de las tres dimensiones (DEC-007)

La variable dependiente se organiza en las tres dimensiones oficiales fijadas por DEC-007 y en seis indicadores. La taxonomía es cerrada: no se agregó ninguna dimensión ni indicador, y los nombres se conservan literalmente. La tabla enuncia la definición y la unidad de cada indicador; las fórmulas se desarrollan en el cuerpo narrativo, conforme a la prohibición de expresiones matemáticas dentro de celdas.

| Dimensión | Definición | Indicador | Unidad | Escala |
| :--- | :--- | :---: | :---: | :--- |
| D1. Oportunidad de procesamiento | Registro y emisión en mínimo tiempo. | T_reg | Minutos | Razón, continua |
| D1. Oportunidad de procesamiento | Ibídem. | T_vale | Minutos | Razón, continua |
| D2. Consistencia documental | Exactitud y concordancia registro-movimiento. | RSD | Porcentaje | Razón, continua |
| D2. Consistencia documental | Ibídem. | CPE | Porcentaje | Razón, continua |
| D3. Satisfacción del usuario | Complacencia y utilidad percibidas (TAM). | AP | Puntos (1–20) | Intervalo, discreta |
| D3. Satisfacción del usuario | Ibídem. | UP | Puntos (1–20) | Intervalo, discreta |
| D3. Satisfacción del usuario | Ibídem. | TAM | Puntos (8–40) | Intervalo, discreta |

*Nota.* Definiciones conforme a la directiva DEC-007 y a la matriz de consistencia del proyecto. Elaboración propia.

### Fórmulas de cuantificación

El tiempo de registro se obtiene como promedio de tres réplicas independientes de la misma unidad y fase:

$$T_{reg} = \frac{1}{3}\sum_{i=1}^{3} t_i$$

donde $t_i$ es la duración neta, en minutos, de la réplica $i$, medida desde el inicio hasta el fin de la operación y descontada la pausa registrada. El tiempo de emisión del vale se calcula con la misma expresión sobre sus tres réplicas.

El porcentaje de registros sin discrepancias se obtiene del cociente entre los documentos que cumplen los ocho criterios y el total auditado:

$$RSD = \frac{\text{documentos conformes}}{40}\times 100$$

La concordancia entre cantidad programada y entregada se calcula sobre los despachos conciliados:

$$CPE = \frac{\text{entregas concordantes}}{25}\times 100$$

La aceptación del proceso y la utilidad percibida son la suma de cuatro reactivos Likert, y el puntaje global es su suma determinista:

$$AP = \sum_{j=1}^{4} a_j, \qquad UP = \sum_{j=1}^{4} b_j, \qquad TAM = AP + UP$$

donde $a_j$ y $b_j$ toman valores enteros de 1 a 5. El baremo del puntaje global se fija antes de observar los datos:

| Nivel | Rango de TAM | Lectura |
| :--- | :---: | :--- |
| Bajo | 8 – 18 | Rechazo o indiferencia hacia el sistema |
| Medio | 19 – 29 | Aceptación parcial, adopción incompleta |
| Alto | 30 – 40 | Aceptación y utilidad declaradas |

*Nota.* Baremo de interpretación sobre el puntaje global TAM de 8 a 40 puntos. Elaboración propia.

---

<a id="parte-3"></a>
## Parte 3. Instrumento 1 — Ficha de observación de tiempos

El instrumento imprime las 168 réplicas del conjunto: seis por unidad y fase (tres de registro y tres de emisión del vale). Cada bloque cierra con la suma y la media de sus tres réplicas, de modo que el indicador pueda auditarse sin recurrir al archivo de datos. Las duraciones se expresan en minutos con cuatro decimales; en el postest de T_vale se añade entre paréntesis el equivalente en segundos enteros. La duración es neta: el intervalo entre la hora de inicio y la de corte equivale a la duración más la pausa externa registrada, de modo que ambas columnas cuadran en cada réplica.

**Convenciones.** T1: ingreso de remesa con un biológico y lote único. T2: salida regular programada de dos a tres vacunas. T3: redistribución con cuatro a seis biológicos. T4: vale simple para puesto de salud 1-1 o 1-2. T5: vale regular para centro de salud 1-3 o 1-4. T6: vale de reposición urgente o contingencia. P1: atención en ventanilla. P2: llamada del establecimiento. P3: corte breve de energía. P4: verificación de existencias.

### Bloque 1 · TRAB-01 · Pretest (proceso manual) · 10/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 08:05:22 | 35.3667 | — | — | Sí |
| REG-02 | T2 | 08:05:22 | 08:46:25 | 39.5500 | 90 | P3 | Sí |
| REG-03 | T3 | 08:46:25 | 09:27:00 | 40.5833 | — | — | Sí |

Cierre: 115.5000 min ÷ 3 = **38.5000 min**. Suma de las tres réplicas: 115.5000 min (6930 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 09:29:49 | 09:47:26 | 16.8667 | 45 | P3 | Sí |
| VALE-02 | T5 | 09:47:26 | 10:06:01 | 18.5833 | — | — | Sí |
| VALE-03 | T6 | 10:06:01 | 10:28:34 | 20.0500 | 150 | P4 | Sí |

Cierre: 55.5000 min ÷ 3 = **18.5000 min**. Suma de las tres réplicas: 55.5000 min (3330 s).

---

### Bloque 2 · TRAB-01 · Postest (Sistema SIVAC) · 12/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 08:00:00 | 08:04:52 | 4.8667 | — | — | Sí |
| REG-02 | T2 | 08:04:52 | 08:10:22 | 5.5000 | — | — | Sí |
| REG-03 | T3 | 08:10:22 | 08:16:07 | 5.7500 | — | — | Sí |

Cierre: 16.1167 min ÷ 3 = **5.3722 min**. Suma de las tres réplicas: 16.1167 min (967 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 08:17:51 | 08:19:54 | 2.0500 (123 s) | — | — | Sí |
| VALE-02 | T5 | 08:19:54 | 08:21:55 | 2.0167 (121 s) | — | — | Sí |
| VALE-03 | T6 | 08:21:55 | 08:24:13 | 2.3000 (138 s) | — | — | Sí |

Cierre: 6.3667 min ÷ 3 = **2.1222 min**. Suma de las tres réplicas: 6.3667 min (382 s).

---

### Bloque 3 · TRAB-02 · Pretest (proceso manual) · 10/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:15:00 | 07:53:07 | 37.3667 | 45 | P3 | Sí |
| REG-02 | T2 | 07:53:07 | 08:36:03 | 42.9333 | — | — | Sí |
| REG-03 | T3 | 08:36:03 | 09:21:45 | 45.7000 | — | — | Sí |

Cierre: 126.0000 min ÷ 3 = **42.0000 min**. Suma de las tres réplicas: 126.0000 min (7560 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 09:25:29 | 09:46:06 | 20.6167 | — | — | Sí |
| VALE-02 | T5 | 09:46:06 | 10:08:35 | 22.4833 | — | — | Sí |
| VALE-03 | T6 | 10:08:35 | 10:32:29 | 22.9000 | 60 | P3 | Sí |

Cierre: 66.0000 min ÷ 3 = **22.0000 min**. Suma de las tres réplicas: 66.0000 min (3960 s).

---

### Bloque 4 · TRAB-02 · Postest (Sistema SIVAC) · 12/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:50:00 | 07:55:16 | 5.2667 | — | — | Sí |
| REG-02 | T2 | 07:55:16 | 08:01:06 | 5.8333 | — | — | Sí |
| REG-03 | T3 | 08:01:06 | 08:07:41 | 6.0833 | 30 | P2 | Sí |

Cierre: 17.1833 min ÷ 3 = **5.7278 min**. Suma de las tres réplicas: 17.1833 min (1031 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 08:09:10 | 08:10:58 | 1.8000 (108 s) | — | — | Sí |
| VALE-02 | T5 | 08:10:58 | 08:12:42 | 1.7333 (104 s) | — | — | Sí |
| VALE-03 | T6 | 08:12:42 | 08:14:39 | 1.9500 (117 s) | — | — | Sí |

Cierre: 5.4833 min ÷ 3 = **1.8278 min**. Suma de las tres réplicas: 5.4833 min (329 s).

---

### Bloque 5 · TRAB-03 · Pretest (proceso manual) · 11/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:45:00 | 08:15:41 | 30.6833 | — | — | Sí |
| REG-02 | T2 | 08:15:41 | 08:52:47 | 35.6000 | 90 | P2 | Sí |
| REG-03 | T3 | 08:52:47 | 09:31:30 | 38.7167 | — | — | Sí |

Cierre: 105.0000 min ÷ 3 = **35.0000 min**. Suma de las tres réplicas: 105.0000 min (6300 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 09:34:19 | 09:49:40 | 15.3500 | — | — | Sí |
| VALE-02 | T5 | 09:49:40 | 10:05:35 | 15.9167 | — | — | Sí |
| VALE-03 | T6 | 10:05:35 | 10:22:19 | 16.7333 | — | — | Sí |

Cierre: 48.0000 min ÷ 3 = **16.0000 min**. Suma de las tres réplicas: 48.0000 min (2880 s).

---

### Bloque 6 · TRAB-03 · Postest (Sistema SIVAC) · 13/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 08:15:00 | 08:19:41 | 4.6833 | — | — | Sí |
| REG-02 | T2 | 08:19:41 | 08:25:12 | 5.5167 | — | — | Sí |
| REG-03 | T3 | 08:25:12 | 08:31:01 | 5.8167 | — | — | Sí |

Cierre: 16.0167 min ÷ 3 = **5.3389 min**. Suma de las tres réplicas: 16.0167 min (961 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 08:33:09 | 08:34:43 | 1.5667 (94 s) | — | — | Sí |
| VALE-02 | T5 | 08:34:43 | 08:36:31 | 1.8000 (108 s) | — | — | Sí |
| VALE-03 | T6 | 08:36:31 | 08:38:19 | 1.8000 (108 s) | — | — | Sí |

Cierre: 5.1667 min ÷ 3 = **1.7222 min**. Suma de las tres réplicas: 5.1667 min (310 s).

---

### Bloque 7 · TRAB-04 · Pretest (proceso manual) · 11/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 08:00:00 | 08:32:02 | 31.0333 | 60 | P4 | Sí |
| REG-02 | T2 | 08:32:02 | 09:06:12 | 34.1667 | — | — | Sí |
| REG-03 | T3 | 09:06:12 | 09:42:30 | 35.3000 | 60 | P4 | Sí |

Cierre: 100.5000 min ÷ 3 = **33.5000 min**. Suma de las tres réplicas: 100.5000 min (6030 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 09:47:50 | 10:01:43 | 13.8833 | — | — | Sí |
| VALE-02 | T5 | 10:01:43 | 10:18:58 | 14.7500 | 150 | P2 | Sí |
| VALE-03 | T6 | 10:18:58 | 10:37:20 | 16.3667 | 120 | P4 | Sí |

Cierre: 45.0000 min ÷ 3 = **15.0000 min**. Suma de las tres réplicas: 45.0000 min (2700 s).

---

### Bloque 8 · TRAB-04 · Postest (Sistema SIVAC) · 13/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 08:30:00 | 08:34:57 | 4.9500 | — | — | Sí |
| REG-02 | T2 | 08:34:57 | 08:40:41 | 5.7333 | — | — | Sí |
| REG-03 | T3 | 08:40:41 | 08:47:46 | 6.0833 | 60 | P2 | Sí |

Cierre: 16.7666 min ÷ 3 = **5.5889 min**. Suma de las tres réplicas: 16.7666 min (1006 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 08:49:27 | 08:51:35 | 2.1333 (128 s) | — | — | Sí |
| VALE-02 | T5 | 08:51:35 | 08:53:45 | 2.1667 (130 s) | — | — | Sí |
| VALE-03 | T6 | 08:53:45 | 08:55:58 | 2.2167 (133 s) | — | — | Sí |

Cierre: 6.5167 min ÷ 3 = **2.1722 min**. Suma de las tres réplicas: 6.5167 min (391 s).

---

### Bloque 9 · TRAB-05 · Pretest (proceso manual) · 12/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:20:00 | 07:58:26 | 36.9333 | 90 | P3 | Sí |
| REG-02 | T2 | 07:58:26 | 08:38:44 | 40.3000 | — | — | Sí |
| REG-03 | T3 | 08:38:44 | 09:21:30 | 42.7667 | — | — | Sí |

Cierre: 120.0000 min ÷ 3 = **40.0000 min**. Suma de las tres réplicas: 120.0000 min (7200 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 09:25:35 | 09:44:26 | 18.8500 | — | — | Sí |
| VALE-02 | T5 | 09:44:26 | 10:05:20 | 20.9000 | — | — | Sí |
| VALE-03 | T6 | 10:05:20 | 10:28:35 | 21.7500 | 90 | P1 | Sí |

Cierre: 61.5000 min ÷ 3 = **20.5000 min**. Suma de las tres réplicas: 61.5000 min (3690 s).

---

### Bloque 10 · TRAB-05 · Postest (Sistema SIVAC) · 14/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:45:00 | 07:50:33 | 5.5500 | — | — | Sí |
| REG-02 | T2 | 07:50:33 | 07:57:00 | 6.4500 | — | — | Sí |
| REG-03 | T3 | 07:57:00 | 08:03:27 | 6.4500 | — | — | Sí |

Cierre: 18.4500 min ÷ 3 = **6.1500 min**. Suma de las tres réplicas: 18.4500 min (1107 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 08:05:46 | 08:07:36 | 1.8333 (110 s) | — | — | Sí |
| VALE-02 | T5 | 08:07:36 | 08:09:29 | 1.8833 (113 s) | — | — | Sí |
| VALE-03 | T6 | 08:09:29 | 08:11:21 | 1.8667 (112 s) | — | — | Sí |

Cierre: 5.5833 min ÷ 3 = **1.8611 min**. Suma de las tres réplicas: 5.5833 min (335 s).

---

### Bloque 11 · TRAB-06 · Pretest (proceso manual) · 12/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:40:00 | 08:14:54 | 32.4000 | 150 | P4 | Sí |
| REG-02 | T2 | 08:14:54 | 08:51:13 | 36.3167 | — | — | Sí |
| REG-03 | T3 | 08:51:13 | 09:33:00 | 40.7833 | 60 | P1 | Sí |

Cierre: 109.5000 min ÷ 3 = **36.5000 min**. Suma de las tres réplicas: 109.5000 min (6570 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 09:37:52 | 09:55:17 | 15.9167 | 90 | P4 | Sí |
| VALE-02 | T5 | 09:55:17 | 10:14:50 | 17.5500 | 120 | P2 | Sí |
| VALE-03 | T6 | 10:14:50 | 10:34:52 | 17.5333 | 150 | P4 | Sí |

Cierre: 51.0000 min ÷ 3 = **17.0000 min**. Suma de las tres réplicas: 51.0000 min (3060 s).

---

### Bloque 12 · TRAB-06 · Postest (Sistema SIVAC) · 14/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 08:10:00 | 08:14:34 | 4.5667 | — | — | Sí |
| REG-02 | T2 | 08:14:34 | 08:19:49 | 4.5000 | 45 | P2 | Sí |
| REG-03 | T3 | 08:19:49 | 08:25:13 | 5.4000 | — | — | Sí |

Cierre: 14.4667 min ÷ 3 = **4.8222 min**. Suma de las tres réplicas: 14.4667 min (868 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 08:27:08 | 08:29:38 | 1.5000 (90 s) | 60 | P2 | Sí |
| VALE-02 | T5 | 08:29:38 | 08:31:19 | 1.6833 (101 s) | — | — | Sí |
| VALE-03 | T6 | 08:31:19 | 08:33:09 | 1.8333 (110 s) | — | — | Sí |

Cierre: 5.0166 min ÷ 3 = **1.6722 min**. Suma de las tres réplicas: 5.0166 min (301 s).

---

### Bloque 13 · TRAB-07 · Pretest (proceso manual) · 13/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 08:09:21 | 39.3500 | — | — | Sí |
| REG-02 | T2 | 08:09:21 | 08:52:53 | 43.5333 | — | — | Sí |
| REG-03 | T3 | 08:52:53 | 09:42:00 | 49.1167 | — | — | Sí |

Cierre: 132.0000 min ÷ 3 = **44.0000 min**. Suma de las tres réplicas: 132.0000 min (7920 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 09:44:26 | 10:07:35 | 22.1500 | 60 | P3 | Sí |
| VALE-02 | T5 | 10:07:35 | 10:32:15 | 23.6667 | 60 | P1 | Sí |
| VALE-03 | T6 | 10:32:15 | 10:58:26 | 26.1833 | — | — | Sí |

Cierre: 72.0000 min ÷ 3 = **24.0000 min**. Suma de las tres réplicas: 72.0000 min (4320 s).

---

### Bloque 14 · TRAB-07 · Postest (Sistema SIVAC) · 15/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 08:00:00 | 08:04:15 | 4.2500 | — | — | Sí |
| REG-02 | T2 | 08:04:15 | 08:09:54 | 4.9000 | 45 | P1 | Sí |
| REG-03 | T3 | 08:09:54 | 08:16:36 | 5.7000 | 60 | P2 | Sí |

Cierre: 14.8500 min ÷ 3 = **4.9500 min**. Suma de las tres réplicas: 14.8500 min (891 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 08:18:23 | 08:20:14 | 1.8500 (111 s) | — | — | Sí |
| VALE-02 | T5 | 08:20:14 | 08:22:58 | 1.9833 (119 s) | 45 | P2 | Sí |
| VALE-03 | T6 | 08:22:58 | 08:25:08 | 2.1667 (130 s) | — | — | Sí |

Cierre: 6.0000 min ÷ 3 = **2.0000 min**. Suma de las tres réplicas: 6.0000 min (360 s).

---

### Bloque 15 · TRAB-08 · Pretest (proceso manual) · 13/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:15:00 | 07:44:03 | 29.0500 | — | — | Sí |
| REG-02 | T2 | 07:44:03 | 08:17:13 | 32.1667 | 60 | P1 | Sí |
| REG-03 | T3 | 08:17:13 | 08:53:30 | 34.7833 | 90 | P3 | Sí |

Cierre: 96.0000 min ÷ 3 = **32.0000 min**. Suma de las tres réplicas: 96.0000 min (5760 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 08:59:18 | 09:12:59 | 13.6833 | — | — | Sí |
| VALE-02 | T5 | 09:12:59 | 09:27:49 | 14.0833 | 45 | P3 | Sí |
| VALE-03 | T6 | 09:27:49 | 09:46:03 | 15.7333 | 150 | P1 | Sí |

Cierre: 43.4999 min ÷ 3 = **14.5000 min**. Suma de las tres réplicas: 43.4999 min (2610 s).

---

### Bloque 16 · TRAB-08 · Postest (Sistema SIVAC) · 15/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:50:00 | 07:55:08 | 5.1333 | — | — | Sí |
| REG-02 | T2 | 07:55:08 | 08:01:44 | 6.1000 | 30 | P2 | Sí |
| REG-03 | T3 | 08:01:44 | 08:08:16 | 6.5333 | — | — | Sí |

Cierre: 17.7666 min ÷ 3 = **5.9222 min**. Suma de las tres réplicas: 17.7666 min (1066 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 08:08:25 | 08:10:16 | 1.8500 (111 s) | — | — | Sí |
| VALE-02 | T5 | 08:10:16 | 08:12:16 | 2.0000 (120 s) | — | — | Sí |
| VALE-03 | T6 | 08:12:16 | 08:14:18 | 2.0333 (122 s) | — | — | Sí |

Cierre: 5.8833 min ÷ 3 = **1.9611 min**. Suma de las tres réplicas: 5.8833 min (353 s).

---

### Bloque 17 · TRAB-09 · Pretest (proceso manual) · 14/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:45:00 | 08:14:19 | 29.3167 | — | — | Sí |
| REG-02 | T2 | 08:14:19 | 08:46:16 | 30.9500 | 60 | P1 | Sí |
| REG-03 | T3 | 08:46:16 | 09:20:30 | 34.2333 | — | — | Sí |

Cierre: 94.5000 min ÷ 3 = **31.5000 min**. Suma de las tres réplicas: 94.5000 min (5670 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 09:22:59 | 09:37:10 | 13.4333 | 45 | P4 | Sí |
| VALE-02 | T5 | 09:37:10 | 09:51:51 | 14.6833 | — | — | Sí |
| VALE-03 | T6 | 09:51:51 | 10:11:14 | 16.8833 | 150 | P1 | Sí |

Cierre: 44.9999 min ÷ 3 = **15.0000 min**. Suma de las tres réplicas: 44.9999 min (2700 s).

---

### Bloque 18 · TRAB-09 · Postest (Sistema SIVAC) · 16/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 08:15:00 | 08:20:38 | 5.6333 | — | — | Sí |
| REG-02 | T2 | 08:20:38 | 08:26:55 | 6.2833 | — | — | Sí |
| REG-03 | T3 | 08:26:55 | 08:33:02 | 6.1167 | — | — | Sí |

Cierre: 18.0333 min ÷ 3 = **6.0111 min**. Suma de las tres réplicas: 18.0333 min (1082 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 08:34:07 | 08:35:40 | 1.5500 (93 s) | — | — | Sí |
| VALE-02 | T5 | 08:35:40 | 08:38:24 | 1.7333 (104 s) | 60 | P2 | Sí |
| VALE-03 | T6 | 08:38:24 | 08:40:04 | 1.6667 (100 s) | — | — | Sí |

Cierre: 4.9500 min ÷ 3 = **1.6500 min**. Suma de las tres réplicas: 4.9500 min (297 s).

---

### Bloque 19 · TRAB-10 · Pretest (proceso manual) · 14/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 08:00:00 | 08:35:58 | 35.9667 | — | — | Sí |
| REG-02 | T2 | 08:35:58 | 09:15:27 | 38.4833 | 60 | P4 | Sí |
| REG-03 | T3 | 09:15:27 | 10:00:00 | 42.5500 | 120 | P2 | Sí |

Cierre: 117.0000 min ÷ 3 = **39.0000 min**. Suma de las tres réplicas: 117.0000 min (7020 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 10:05:51 | 10:25:39 | 17.8000 | 120 | P3 | Sí |
| VALE-02 | T5 | 10:25:39 | 10:47:05 | 19.4333 | 120 | P1 | Sí |
| VALE-03 | T6 | 10:47:05 | 11:08:21 | 21.2667 | — | — | Sí |

Cierre: 58.5000 min ÷ 3 = **19.5000 min**. Suma de las tres réplicas: 58.5000 min (3510 s).

---

### Bloque 20 · TRAB-10 · Postest (Sistema SIVAC) · 16/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 08:30:00 | 08:35:42 | 5.7000 | — | — | Sí |
| REG-02 | T2 | 08:35:42 | 08:42:35 | 6.1333 | 45 | P1 | Sí |
| REG-03 | T3 | 08:42:35 | 08:49:37 | 7.0333 | — | — | Sí |

Cierre: 18.8666 min ÷ 3 = **6.2889 min**. Suma de las tres réplicas: 18.8666 min (1132 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 08:51:56 | 08:53:45 | 1.8167 (109 s) | — | — | Sí |
| VALE-02 | T5 | 08:53:45 | 08:55:37 | 1.8667 (112 s) | — | — | Sí |
| VALE-03 | T6 | 08:55:37 | 08:58:03 | 1.9333 (116 s) | 30 | P2 | Sí |

Cierre: 5.6167 min ÷ 3 = **1.8722 min**. Suma de las tres réplicas: 5.6167 min (337 s).

---

### Bloque 21 · TRAB-11 · Pretest (proceso manual) · 07/09/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:20:00 | 07:52:35 | 32.5833 | — | — | Sí |
| REG-02 | T2 | 07:52:35 | 08:29:52 | 37.2833 | — | — | Sí |
| REG-03 | T3 | 08:29:52 | 09:12:30 | 41.1333 | 90 | P1 | Sí |

Cierre: 110.9999 min ÷ 3 = **37.0000 min**. Suma de las tres réplicas: 110.9999 min (6660 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 09:18:19 | 09:35:13 | 16.9000 | — | — | Sí |
| VALE-02 | T5 | 09:35:13 | 09:54:29 | 18.2667 | 60 | P2 | Sí |
| VALE-03 | T6 | 09:54:29 | 10:13:19 | 18.8333 | — | — | Sí |

Cierre: 54.0000 min ÷ 3 = **18.0000 min**. Suma de las tres réplicas: 54.0000 min (3240 s).

---

### Bloque 22 · TRAB-11 · Postest (Sistema SIVAC) · 19/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:45:00 | 07:51:03 | 6.0500 | — | — | Sí |
| REG-02 | T2 | 07:51:03 | 07:57:25 | 6.3667 | — | — | Sí |
| REG-03 | T3 | 07:57:25 | 08:04:19 | 6.9000 | — | — | Sí |

Cierre: 19.3167 min ÷ 3 = **6.4389 min**. Suma de las tres réplicas: 19.3167 min (1159 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 08:04:25 | 08:06:55 | 1.7500 (105 s) | 45 | P1 | Sí |
| VALE-02 | T5 | 08:06:55 | 08:09:11 | 1.7667 (106 s) | 30 | P2 | Sí |
| VALE-03 | T6 | 08:09:11 | 08:11:00 | 1.8167 (109 s) | — | — | Sí |

Cierre: 5.3334 min ÷ 3 = **1.7778 min**. Suma de las tres réplicas: 5.3334 min (320 s).

---

### Bloque 23 · TRAB-12 · Pretest (proceso manual) · 07/09/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:40:00 | 08:19:06 | 37.1000 | 120 | P1 | Sí |
| REG-02 | T2 | 08:19:06 | 09:00:00 | 40.9000 | — | — | Sí |
| REG-03 | T3 | 09:00:00 | 09:46:30 | 46.5000 | — | — | Sí |

Cierre: 124.5000 min ÷ 3 = **41.5000 min**. Suma de las tres réplicas: 124.5000 min (7470 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 09:50:39 | 10:11:41 | 20.0333 | 60 | P2 | Sí |
| VALE-02 | T5 | 10:11:41 | 10:33:01 | 21.3333 | — | — | Sí |
| VALE-03 | T6 | 10:33:01 | 10:54:39 | 21.6333 | — | — | Sí |

Cierre: 62.9999 min ÷ 3 = **21.0000 min**. Suma de las tres réplicas: 62.9999 min (3780 s).

---

### Bloque 24 · TRAB-12 · Postest (Sistema SIVAC) · 19/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 08:10:00 | 08:15:46 | 5.0167 | 45 | P1 | Sí |
| REG-02 | T2 | 08:15:46 | 08:21:50 | 6.0667 | — | — | Sí |
| REG-03 | T3 | 08:21:50 | 08:27:58 | 6.1333 | — | — | Sí |

Cierre: 17.2167 min ÷ 3 = **5.7389 min**. Suma de las tres réplicas: 17.2167 min (1033 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 08:29:03 | 08:31:57 | 1.9000 (114 s) | 60 | P2 | Sí |
| VALE-02 | T5 | 08:31:57 | 08:33:56 | 1.9833 (119 s) | — | — | Sí |
| VALE-03 | T6 | 08:33:56 | 08:36:16 | 2.3333 (140 s) | — | — | Sí |

Cierre: 6.2166 min ÷ 3 = **2.0722 min**. Suma de las tres réplicas: 6.2166 min (373 s).

---

### Bloque 25 · TRAB-13 · Pretest (proceso manual) · 08/09/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 08:00:33 | 30.5500 | — | — | Sí |
| REG-02 | T2 | 08:00:33 | 08:34:45 | 34.2000 | — | — | Sí |
| REG-03 | T3 | 08:34:45 | 09:13:00 | 37.2500 | 60 | P1 | Sí |

Cierre: 102.0000 min ÷ 3 = **34.0000 min**. Suma de las tres réplicas: 102.0000 min (6120 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 09:19:00 | 09:34:21 | 15.3500 | — | — | Sí |
| VALE-02 | T5 | 09:34:21 | 09:50:26 | 16.0833 | — | — | Sí |
| VALE-03 | T6 | 09:50:26 | 10:09:30 | 18.0667 | 60 | P2 | Sí |

Cierre: 49.5000 min ÷ 3 = **16.5000 min**. Suma de las tres réplicas: 49.5000 min (2970 s).

---

### Bloque 26 · TRAB-13 · Postest (Sistema SIVAC) · 20/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 08:00:00 | 08:05:00 | 5.0000 | — | — | Sí |
| REG-02 | T2 | 08:05:00 | 08:10:33 | 5.5500 | — | — | Sí |
| REG-03 | T3 | 08:10:33 | 08:16:35 | 6.0333 | — | — | Sí |

Cierre: 16.5833 min ÷ 3 = **5.5278 min**. Suma de las tres réplicas: 16.5833 min (995 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 08:18:46 | 08:20:49 | 2.0500 (123 s) | — | — | Sí |
| VALE-02 | T5 | 08:20:49 | 08:23:02 | 2.2167 (133 s) | — | — | Sí |
| VALE-03 | T6 | 08:23:02 | 08:26:35 | 2.5500 (153 s) | 60 | P2 | Sí |

Cierre: 6.8167 min ÷ 3 = **2.2722 min**. Suma de las tres réplicas: 6.8167 min (409 s).

---

### Bloque 27 · TRAB-14 · Pretest (proceso manual) · 08/09/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:15:00 | 07:48:56 | 31.4333 | 150 | P4 | Sí |
| REG-02 | T2 | 07:48:56 | 08:24:46 | 35.0833 | 45 | P4 | Sí |
| REG-03 | T3 | 08:24:46 | 09:06:15 | 41.4833 | — | — | Sí |

Cierre: 107.9999 min ÷ 3 = **36.0000 min**. Suma de las tres réplicas: 107.9999 min (6480 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 09:12:25 | 09:31:21 | 16.4333 | 150 | P3 | Sí |
| VALE-02 | T5 | 09:31:21 | 09:48:55 | 17.5667 | — | — | Sí |
| VALE-03 | T6 | 09:48:55 | 10:08:10 | 18.5000 | 45 | P4 | Sí |

Cierre: 52.5000 min ÷ 3 = **17.5000 min**. Suma de las tres réplicas: 52.5000 min (3150 s).

---

### Bloque 28 · TRAB-14 · Postest (Sistema SIVAC) · 20/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:50:00 | 07:54:59 | 4.9833 | — | — | Sí |
| REG-02 | T2 | 07:54:59 | 08:00:32 | 5.5500 | — | — | Sí |
| REG-03 | T3 | 08:00:32 | 08:06:53 | 6.3500 | — | — | Sí |

Cierre: 16.8833 min ÷ 3 = **5.6278 min**. Suma de las tres réplicas: 16.8833 min (1013 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 08:07:58 | 08:09:49 | 1.8500 (111 s) | — | — | Sí |
| VALE-02 | T5 | 08:09:49 | 08:11:47 | 1.9667 (118 s) | — | — | Sí |
| VALE-03 | T6 | 08:11:47 | 08:13:40 | 1.8833 (113 s) | — | — | Sí |

Cierre: 5.7000 min ÷ 3 = **1.9000 min**. Suma de las tres réplicas: 5.7000 min (342 s).

---

---

<a id="parte-4"></a>
## Parte 4. Instrumento 2 — Ficha de auditoría documental y conciliación de entregas

Cada bloque audita cuarenta documentos sobre ocho criterios binarios y concilia veinticinco despachos. La conformidad documental es conjuntiva: un documento es conforme solo si cumple los ocho criterios. La tabla emplea S y N para abreviar Sí y No, y las columnas 1 a 8 siguen el orden de los aspectos del instrumento. El motivo se codifica de M1 a M8 y se imprime solo cuando el documento no es conforme. En las entregas, Dif. es la cantidad entregada menos la programada: el signo negativo señala faltante y el positivo, exceso; la entrega es concordante solo cuando la diferencia es cero.

**Convenciones.** ING: ingreso. SAL: salida. TRA: transferencia. DEV: devolución. AJU: ajuste. BCG, PENT, IPV, ROTA, NEUM, SPR, DTA, HEPB, INFL y VARI abrevian los biológicos del catálogo. M1 a M8 remiten a los ocho aspectos en el orden impreso.

### Bloque 1 · TRAB-01 · Pretest (proceso manual) · 10/08/2026

Documentos auditados: 40 · Conformes: 25 · RSD: 62.50 % · Entregas conciliadas: 25 · Concordantes: 16 · CPE: 64.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | AJU | HEPB | HEPB-2603-786K | 100 | S | S | S | S | S | S | S | S | S | — |
| 2 | ING | ROTA | ROTA-2605-833M | 240 | S | S | S | S | S | N | S | S | N | M6 |
| 3 | TRA | INFL | INFL-2504-261K | 40 | S | S | S | S | S | S | S | S | S | — |
| 4 | SAL | IPV | IPV-2507-805M | 40 | S | S | S | S | S | S | S | S | S | — |
| 5 | TRA | SPR | SPR-2608-539M | 240 | S | S | S | S | N | S | S | S | N | M5 |
| 6 | ING | SPR | SPR-2606-500M | 50 | S | S | S | S | S | N | S | S | N | M6 |
| 7 | SAL | VARI | VARI-2501-250M | 30 | S | S | S | S | S | S | S | S | S | — |
| 8 | TRA | ROTA | ROTA-2502-563B | 40 | S | S | S | S | S | N | S | S | N | M6 |
| 9 | SAL | DTA | DTA-2606-829K | 60 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | PENT | PENT-2508-232M | 40 | S | S | S | S | N | S | S | S | N | M5 |
| 11 | AJU | DTA | DTA-2505-409K | 30 | N | S | S | S | S | S | S | N | N | M1+M8 |
| 12 | AJU | VARI | VARI-2607-979A | 300 | S | S | S | S | S | S | S | S | S | — |
| 13 | SAL | HEPB | HEPB-2509-474M | 40 | S | S | S | S | S | S | N | S | N | M7 |
| 14 | SAL | INFL | INFL-2604-777M | 50 | S | S | S | S | S | S | S | S | S | — |
| 15 | TRA | IPV | IPV-2605-698M | 300 | S | S | S | S | S | S | S | S | S | — |
| 16 | ING | NEUM | NEUM-2505-638K | 60 | S | S | N | S | S | S | N | S | N | M3+M7 |
| 17 | ING | VARI | VARI-2508-818M | 180 | S | S | N | S | S | S | S | S | N | M3 |
| 18 | ING | PENT | PENT-2508-232M | 30 | S | S | S | S | S | S | S | N | N | M8 |
| 19 | ING | HEPB | HEPB-2609-521M | 60 | S | S | S | S | S | S | S | S | S | — |
| 20 | SAL | HEPB | HEPB-2609-521M | 50 | S | S | S | S | S | S | S | S | S | — |
| 21 | ING | HEPB | HEPB-2609-917M | 120 | S | S | S | S | S | S | S | S | S | — |
| 22 | TRA | PENT | PENT-2606-251M | 40 | S | S | S | S | S | S | S | S | S | — |
| 23 | SAL | SPR | SPR-2603-471K | 150 | S | S | S | S | S | S | N | S | N | M7 |
| 24 | SAL | SPR | SPR-2609-423M | 30 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | VARI | VARI-2508-818M | 300 | S | S | S | S | S | S | S | S | S | — |
| 26 | DEV | ROTA | ROTA-2502-563B | 20 | S | S | S | S | S | N | N | S | N | M6+M7 |
| 27 | SAL | HEPB | HEPB-2602-318M | 60 | S | S | S | S | S | S | S | N | N | M8 |
| 28 | SAL | NEUM | NEUM-2505-638K | 300 | S | N | S | S | S | S | S | S | N | M2 |
| 29 | AJU | SPR | SPR-2606-500M | 60 | S | S | S | S | S | S | S | S | S | — |
| 30 | SAL | PENT | PENT-2606-391A | 120 | S | S | S | S | S | S | S | S | S | — |
| 31 | DEV | SPR | SPR-2609-423M | 20 | S | S | S | S | S | S | S | S | S | — |
| 32 | ING | SPR | SPR-2609-423M | 40 | S | S | S | S | S | S | N | S | N | M7 |
| 33 | TRA | ROTA | ROTA-2502-563B | 50 | S | S | S | S | S | S | S | S | S | — |
| 34 | SAL | IPV | IPV-2503-662B | 30 | S | S | S | S | S | S | S | S | S | — |
| 35 | SAL | NEUM | NEUM-2505-638K | 180 | S | S | S | S | S | S | S | S | S | — |
| 36 | ING | DTA | DTA-2603-463K | 30 | S | S | S | S | S | S | S | S | S | — |
| 37 | ING | ROTA | ROTA-2507-417A | 150 | S | S | S | S | S | S | S | S | S | — |
| 38 | TRA | ROTA | ROTA-2602-464A | 300 | S | S | S | S | S | S | S | S | S | — |
| 39 | DEV | VARI | VARI-2509-637K | 100 | S | S | S | S | S | S | S | S | S | — |
| 40 | SAL | ROTA | ROTA-2602-464A | 60 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-01 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 24/07/2026 | CHANKA-001 | PENT | 50 | 50 | 0 | GR-CHANKA001-6241 | Sí |
| 2 | 28/07/2026 | CHANKA-001 | PENT | 150 | 150 | 0 | GR-CHANKA001-4432 | Sí |
| 3 | 13/07/2026 | CHANKA-001 | DTA | 150 | 150 | 0 | GR-CHANKA001-3735 | Sí |
| 4 | 03/08/2026 | CHANKA-001 | BCG | 180 | 185 | 5 | Sin guía | No |
| 5 | 24/07/2026 | CHANKA-001 | IPV | 150 | 150 | 0 | GR-CHANKA001-3108 | Sí |
| 6 | 20/07/2026 | CHANKA-001 | HEPB | 80 | 80 | 0 | GR-CHANKA001-1676 | Sí |
| 7 | 26/07/2026 | CHANKA-001 | VARI | 120 | 120 | 0 | GR-CHANKA001-2127 | Sí |
| 8 | 29/07/2026 | CHANKA-001 | NEUM | 120 | 110 | -10 | GR-CHANKA001-7575 | No |
| 9 | 09/08/2026 | CHANKA-001 | DTA | 200 | 200 | 0 | GR-CHANKA001-2202 | Sí |
| 10 | 01/08/2026 | CHANKA-001 | NEUM | 30 | 25 | -5 | GR-CHANKA001-9318 | No |
| 11 | 13/07/2026 | CHANKA-001 | VARI | 200 | 210 | 10 | GR-CHANKA001-8494 | No |
| 12 | 09/08/2026 | CHANKA-001 | INFL | 100 | 100 | 0 | GR-CHANKA001-2987 | Sí |
| 13 | 15/07/2026 | CHANKA-001 | DTA | 100 | 100 | 0 | GR-CHANKA001-4034 | Sí |
| 14 | 17/07/2026 | CHANKA-001 | BCG | 100 | 100 | 0 | GR-CHANKA001-5666 | Sí |
| 15 | 23/07/2026 | CHANKA-001 | VARI | 200 | 200 | 0 | GR-CHANKA001-4055 | Sí |
| 16 | 07/08/2026 | CHANKA-001 | HEPB | 30 | 30 | 0 | GR-CHANKA001-5775 | Sí |
| 17 | 28/07/2026 | CHANKA-001 | HEPB | 80 | 80 | 0 | GR-CHANKA001-6660 | Sí |
| 18 | 22/07/2026 | CHANKA-001 | NEUM | 80 | 80 | 0 | GR-CHANKA001-8468 | Sí |
| 19 | 05/08/2026 | CHANKA-001 | SPR | 180 | 175 | -5 | Sin guía | No |
| 20 | 28/07/2026 | CHANKA-001 | INFL | 120 | 110 | -10 | GR-CHANKA001-2123 | No |
| 21 | 21/07/2026 | CHANKA-001 | INFL | 180 | 170 | -10 | GR-CHANKA001-5216 | No |
| 22 | 23/07/2026 | CHANKA-001 | PENT | 180 | 180 | 0 | GR-CHANKA001-7823 | Sí |
| 23 | 07/08/2026 | CHANKA-001 | ROTA | 60 | 50 | -10 | GR-CHANKA001-4330 | No |
| 24 | 31/07/2026 | CHANKA-001 | VARI | 40 | 40 | 0 | GR-CHANKA001-1877 | Sí |
| 25 | 05/08/2026 | CHANKA-001 | IPV | 20 | 25 | 5 | Sin guía | No |

Cierre: 16 entregas concordantes ÷ 25 × 100 = **64.00 %**.

---

### Bloque 2 · TRAB-01 · Postest (Sistema SIVAC) · 12/10/2026

Documentos auditados: 40 · Conformes: 38 · RSD: 95.00 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | ING | NEUM | NEUM-2505-638K | 60 | S | S | S | S | S | S | S | S | S | — |
| 2 | SAL | NEUM | NEUM-2506-884B | 300 | S | S | S | S | S | S | S | S | S | — |
| 3 | ING | DTA | DTA-2603-463K | 120 | S | S | S | S | S | S | S | S | S | — |
| 4 | TRA | IPV | IPV-2605-698M | 60 | S | S | S | S | S | S | S | S | S | — |
| 5 | ING | INFL | INFL-2508-359M | 50 | S | S | S | S | S | S | S | S | S | — |
| 6 | TRA | ROTA | ROTA-2502-563B | 50 | S | S | S | S | S | S | S | S | S | — |
| 7 | SAL | HEPB | HEPB-2609-521M | 200 | S | S | S | S | S | S | S | S | S | — |
| 8 | TRA | NEUM | NEUM-2507-181K | 200 | S | S | S | S | S | S | S | S | S | — |
| 9 | AJU | HEPB | HEPB-2509-474M | 300 | S | S | S | S | S | S | S | S | S | — |
| 10 | AJU | BCG | BCG-2507-694K | 120 | S | S | S | S | S | S | S | S | S | — |
| 11 | SAL | HEPB | HEPB-2609-521M | 60 | S | S | S | S | S | S | S | S | S | — |
| 12 | ING | BCG | BCG-2504-789B | 80 | S | S | S | S | S | S | S | S | S | — |
| 13 | AJU | BCG | BCG-2606-808K | 150 | S | S | S | S | S | S | S | S | S | — |
| 14 | AJU | NEUM | NEUM-2506-884B | 150 | S | S | S | S | S | S | S | S | S | — |
| 15 | TRA | SPR | SPR-2608-539M | 30 | S | S | S | S | S | S | S | S | S | — |
| 16 | AJU | INFL | INFL-2607-737M | 300 | S | S | S | S | S | S | S | S | S | — |
| 17 | ING | SPR | SPR-2606-500M | 100 | S | S | S | S | S | S | S | S | S | — |
| 18 | ING | PENT | PENT-2606-251M | 40 | S | N | S | S | N | S | S | S | N | M2+M5 |
| 19 | TRA | VARI | VARI-2503-521A | 80 | S | S | S | S | S | S | S | S | S | — |
| 20 | ING | BCG | BCG-2607-654A | 20 | S | S | S | S | S | S | S | S | S | — |
| 21 | ING | BCG | BCG-2504-789B | 60 | S | S | S | S | S | S | N | S | N | M7 |
| 22 | DEV | ROTA | ROTA-2502-563B | 150 | S | S | S | S | S | S | S | S | S | — |
| 23 | AJU | SPR | SPR-2609-423M | 60 | S | S | S | S | S | S | S | S | S | — |
| 24 | SAL | BCG | BCG-2606-808K | 120 | S | S | S | S | S | S | S | S | S | — |
| 25 | SAL | DTA | DTA-2602-236K | 100 | S | S | S | S | S | S | S | S | S | — |
| 26 | DEV | BCG | BCG-2507-694K | 30 | S | S | S | S | S | S | S | S | S | — |
| 27 | TRA | INFL | INFL-2508-359M | 300 | S | S | S | S | S | S | S | S | S | — |
| 28 | ING | INFL | INFL-2504-261K | 120 | S | S | S | S | S | S | S | S | S | — |
| 29 | SAL | SPR | SPR-2504-185M | 80 | S | S | S | S | S | S | S | S | S | — |
| 30 | DEV | HEPB | HEPB-2509-474M | 60 | S | S | S | S | S | S | S | S | S | — |
| 31 | ING | DTA | DTA-2505-409K | 240 | S | S | S | S | S | S | S | S | S | — |
| 32 | ING | HEPB | HEPB-2602-318M | 240 | S | S | S | S | S | S | S | S | S | — |
| 33 | SAL | ROTA | ROTA-2507-417A | 150 | S | S | S | S | S | S | S | S | S | — |
| 34 | ING | SPR | SPR-2609-423M | 100 | S | S | S | S | S | S | S | S | S | — |
| 35 | ING | IPV | IPV-2605-698M | 120 | S | S | S | S | S | S | S | S | S | — |
| 36 | ING | VARI | VARI-2508-818M | 300 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | BCG | BCG-2607-654A | 40 | S | S | S | S | S | S | S | S | S | — |
| 38 | TRA | BCG | BCG-2504-789B | 20 | S | S | S | S | S | S | S | S | S | — |
| 39 | SAL | INFL | INFL-2604-777M | 180 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | INFL | INFL-2607-737M | 180 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-01 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 11/10/2026 | CHANKA-001 | HEPB | 200 | 200 | 0 | GR-CHANKA001-4781 | Sí |
| 2 | 29/09/2026 | CHANKA-001 | BCG | 30 | 30 | 0 | GR-CHANKA001-1850 | Sí |
| 3 | 22/09/2026 | CHANKA-001 | INFL | 20 | 20 | 0 | GR-CHANKA001-2190 | Sí |
| 4 | 09/10/2026 | CHANKA-001 | NEUM | 150 | 150 | 0 | GR-CHANKA001-7585 | Sí |
| 5 | 07/10/2026 | CHANKA-001 | NEUM | 50 | 50 | 0 | GR-CHANKA001-8026 | Sí |
| 6 | 16/09/2026 | CHANKA-001 | PENT | 60 | 60 | 0 | GR-CHANKA001-2923 | Sí |
| 7 | 14/09/2026 | CHANKA-001 | INFL | 100 | 100 | 0 | GR-CHANKA001-1722 | Sí |
| 8 | 23/09/2026 | CHANKA-001 | NEUM | 120 | 120 | 0 | GR-CHANKA001-7582 | Sí |
| 9 | 25/09/2026 | CHANKA-001 | SPR | 180 | 180 | 0 | GR-CHANKA001-8022 | Sí |
| 10 | 28/09/2026 | CHANKA-001 | HEPB | 20 | 20 | 0 | GR-CHANKA001-7345 | Sí |
| 11 | 23/09/2026 | CHANKA-001 | INFL | 80 | 80 | 0 | GR-CHANKA001-4497 | Sí |
| 12 | 14/09/2026 | CHANKA-001 | INFL | 80 | 80 | 0 | GR-CHANKA001-3941 | Sí |
| 13 | 10/10/2026 | CHANKA-001 | IPV | 50 | 50 | 0 | GR-CHANKA001-1210 | Sí |
| 14 | 18/09/2026 | CHANKA-001 | INFL | 20 | 20 | 0 | GR-CHANKA001-3023 | Sí |
| 15 | 11/10/2026 | CHANKA-001 | HEPB | 80 | 80 | 0 | GR-CHANKA001-3579 | Sí |
| 16 | 17/09/2026 | CHANKA-001 | SPR | 50 | 50 | 0 | GR-CHANKA001-3955 | Sí |
| 17 | 22/09/2026 | CHANKA-001 | SPR | 180 | 175 | -5 | GR-CHANKA001-5298 | No |
| 18 | 08/10/2026 | CHANKA-001 | DTA | 80 | 80 | 0 | GR-CHANKA001-2736 | Sí |
| 19 | 28/09/2026 | CHANKA-001 | IPV | 40 | 40 | 0 | GR-CHANKA001-7712 | Sí |
| 20 | 30/09/2026 | CHANKA-001 | DTA | 50 | 50 | 0 | GR-CHANKA001-9653 | Sí |
| 21 | 11/10/2026 | CHANKA-001 | PENT | 60 | 60 | 0 | GR-CHANKA001-8780 | Sí |
| 22 | 02/10/2026 | CHANKA-001 | INFL | 180 | 180 | 0 | GR-CHANKA001-5902 | Sí |
| 23 | 17/09/2026 | CHANKA-001 | VARI | 20 | 20 | 0 | GR-CHANKA001-4982 | Sí |
| 24 | 07/10/2026 | CHANKA-001 | ROTA | 150 | 150 | 0 | GR-CHANKA001-4411 | Sí |
| 25 | 30/09/2026 | CHANKA-001 | INFL | 150 | 150 | 0 | GR-CHANKA001-5857 | Sí |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 3 · TRAB-02 · Pretest (proceso manual) · 10/08/2026

Documentos auditados: 40 · Conformes: 23 · RSD: 57.50 % · Entregas conciliadas: 25 · Concordantes: 16 · CPE: 64.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | TRA | BCG | BCG-2606-808K | 200 | S | S | S | S | S | S | S | S | S | — |
| 2 | DEV | ROTA | ROTA-2605-833M | 180 | S | S | S | S | S | S | S | S | S | — |
| 3 | ING | INFL | INFL-2508-359M | 240 | S | S | S | S | S | N | S | S | N | M6 |
| 4 | ING | VARI | VARI-2509-637K | 20 | S | S | S | S | S | S | S | N | N | M8 |
| 5 | SAL | VARI | VARI-2508-818M | 20 | S | S | S | S | S | S | S | S | S | — |
| 6 | ING | DTA | DTA-2505-409K | 200 | N | S | S | S | S | S | S | S | N | M1 |
| 7 | ING | INFL | INFL-2604-777M | 300 | S | S | S | N | S | N | S | S | N | M4+M6 |
| 8 | SAL | VARI | VARI-2509-637K | 50 | S | S | S | S | S | S | S | S | S | — |
| 9 | ING | NEUM | NEUM-2506-884B | 300 | S | S | S | S | S | S | S | N | N | M8 |
| 10 | SAL | DTA | DTA-2505-409K | 300 | S | S | S | S | S | S | S | S | S | — |
| 11 | ING | SPR | SPR-2609-423M | 240 | S | S | S | S | S | N | S | S | N | M6 |
| 12 | AJU | HEPB | HEPB-2609-917M | 150 | S | S | S | S | S | S | S | S | S | — |
| 13 | TRA | IPV | IPV-2605-698M | 30 | S | S | S | S | S | N | S | S | N | M6 |
| 14 | SAL | SPR | SPR-2603-471K | 240 | S | S | S | S | S | N | S | S | N | M6 |
| 15 | TRA | SPR | SPR-2504-185M | 50 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | PENT | PENT-2605-322M | 180 | S | S | S | S | S | S | S | S | S | — |
| 17 | ING | HEPB | HEPB-2609-917M | 100 | S | S | S | S | S | S | S | S | S | — |
| 18 | ING | NEUM | NEUM-2505-688A | 30 | S | S | S | S | S | S | S | S | S | — |
| 19 | SAL | IPV | IPV-2608-446B | 200 | S | S | S | S | S | S | S | S | S | — |
| 20 | ING | INFL | INFL-2603-792B | 40 | S | N | S | S | S | S | S | S | N | M2 |
| 21 | ING | ROTA | ROTA-2603-156K | 300 | S | N | S | S | S | N | S | S | N | M2+M6 |
| 22 | SAL | INFL | INFL-2504-261K | 50 | S | S | S | S | S | S | N | S | N | M7 |
| 23 | SAL | IPV | IPV-2507-805M | 300 | S | S | S | N | S | S | S | S | N | M4 |
| 24 | DEV | PENT | PENT-2504-482M | 80 | S | S | S | S | S | S | S | S | S | — |
| 25 | SAL | NEUM | NEUM-2507-181K | 200 | S | S | S | S | S | S | S | S | S | — |
| 26 | ING | IPV | IPV-2507-805M | 120 | S | S | S | S | S | S | S | S | S | — |
| 27 | SAL | INFL | INFL-2508-359M | 300 | S | S | S | S | S | S | S | S | S | — |
| 28 | ING | PENT | PENT-2606-391A | 120 | S | S | S | S | S | S | S | S | S | — |
| 29 | SAL | NEUM | NEUM-2505-638K | 100 | S | N | S | S | S | N | S | S | N | M2+M6 |
| 30 | ING | ROTA | ROTA-2603-156K | 100 | S | S | S | S | S | S | S | S | S | — |
| 31 | SAL | ROTA | ROTA-2605-833M | 300 | S | S | S | S | S | S | S | S | S | — |
| 32 | AJU | SPR | SPR-2606-500M | 180 | S | S | S | S | S | S | S | S | S | — |
| 33 | SAL | HEPB | HEPB-2509-474M | 40 | S | S | S | S | S | S | S | S | S | — |
| 34 | TRA | INFL | INFL-2504-261K | 100 | S | S | S | S | S | S | S | N | N | M8 |
| 35 | TRA | HEPB | HEPB-2509-474M | 20 | S | S | S | S | S | S | S | S | S | — |
| 36 | TRA | HEPB | HEPB-2609-521M | 180 | S | S | S | S | S | S | S | N | N | M8 |
| 37 | TRA | ROTA | ROTA-2605-833M | 150 | S | S | S | S | S | S | S | S | S | — |
| 38 | SAL | VARI | VARI-2503-521A | 40 | S | S | S | S | S | S | N | S | N | M7 |
| 39 | ING | NEUM | NEUM-2509-952A | 120 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | DTA | DTA-2505-409K | 300 | N | N | S | S | S | S | S | S | N | M1+M2 |

**Entregas conciliadas — TRAB-02 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 08/08/2026 | CHANKA-001 | PENT | 60 | 50 | -10 | GR-CHANKA001-1391 | No |
| 2 | 08/08/2026 | CHANKA-001 | SPR | 180 | 180 | 0 | GR-CHANKA001-4527 | Sí |
| 3 | 07/08/2026 | CHANKA-001 | BCG | 50 | 45 | -5 | GR-CHANKA001-6852 | No |
| 4 | 17/07/2026 | CHANKA-001 | PENT | 40 | 35 | -5 | GR-CHANKA001-3436 | No |
| 5 | 25/07/2026 | CHANKA-001 | SPR | 150 | 150 | 0 | GR-CHANKA001-8093 | Sí |
| 6 | 23/07/2026 | CHANKA-001 | IPV | 30 | 30 | 0 | GR-CHANKA001-6827 | Sí |
| 7 | 16/07/2026 | CHANKA-001 | BCG | 180 | 175 | -5 | GR-CHANKA001-4192 | No |
| 8 | 22/07/2026 | CHANKA-001 | NEUM | 30 | 30 | 0 | GR-CHANKA001-4466 | Sí |
| 9 | 17/07/2026 | CHANKA-001 | DTA | 100 | 100 | 0 | GR-CHANKA001-3315 | Sí |
| 10 | 13/07/2026 | CHANKA-001 | SPR | 80 | 80 | 0 | GR-CHANKA001-8065 | Sí |
| 11 | 23/07/2026 | CHANKA-001 | SPR | 80 | 80 | 0 | GR-CHANKA001-9786 | Sí |
| 12 | 13/07/2026 | CHANKA-001 | NEUM | 40 | 40 | 0 | GR-CHANKA001-6745 | Sí |
| 13 | 31/07/2026 | CHANKA-001 | BCG | 20 | 15 | -5 | GR-CHANKA001-8464 | No |
| 14 | 14/07/2026 | CHANKA-001 | INFL | 20 | 20 | 0 | GR-CHANKA001-7586 | Sí |
| 15 | 07/08/2026 | CHANKA-001 | INFL | 200 | 195 | -5 | GR-CHANKA001-6078 | No |
| 16 | 28/07/2026 | CHANKA-001 | SPR | 80 | 85 | 5 | Sin guía | No |
| 17 | 14/07/2026 | CHANKA-001 | DTA | 40 | 40 | 0 | GR-CHANKA001-7464 | Sí |
| 18 | 29/07/2026 | CHANKA-001 | INFL | 60 | 60 | 0 | GR-CHANKA001-5236 | Sí |
| 19 | 02/08/2026 | CHANKA-001 | INFL | 30 | 30 | 0 | GR-CHANKA001-6589 | Sí |
| 20 | 07/08/2026 | CHANKA-001 | ROTA | 40 | 40 | 0 | GR-CHANKA001-4368 | Sí |
| 21 | 17/07/2026 | CHANKA-001 | ROTA | 200 | 200 | 0 | GR-CHANKA001-3382 | Sí |
| 22 | 23/07/2026 | CHANKA-001 | ROTA | 100 | 100 | 0 | GR-CHANKA001-2232 | Sí |
| 23 | 30/07/2026 | CHANKA-001 | NEUM | 30 | 20 | -10 | GR-CHANKA001-8955 | No |
| 24 | 05/08/2026 | CHANKA-001 | NEUM | 200 | 200 | 0 | GR-CHANKA001-8622 | Sí |
| 25 | 20/07/2026 | CHANKA-001 | PENT | 40 | 45 | 5 | Sin guía | No |

Cierre: 16 entregas concordantes ÷ 25 × 100 = **64.00 %**.

---

### Bloque 4 · TRAB-02 · Postest (Sistema SIVAC) · 12/10/2026

Documentos auditados: 40 · Conformes: 39 · RSD: 97.50 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | TRA | ROTA | ROTA-2507-417A | 60 | S | S | S | S | S | S | S | S | S | — |
| 2 | SAL | PENT | PENT-2605-322M | 20 | S | S | S | S | S | S | S | S | S | — |
| 3 | SAL | PENT | PENT-2606-391A | 60 | S | S | S | S | S | S | S | S | S | — |
| 4 | DEV | INFL | INFL-2607-737M | 20 | S | S | S | S | S | S | S | S | S | — |
| 5 | ING | DTA | DTA-2602-236K | 60 | S | S | S | S | S | S | S | S | S | — |
| 6 | DEV | DTA | DTA-2602-797A | 40 | S | S | S | S | S | S | S | S | S | — |
| 7 | TRA | ROTA | ROTA-2507-417A | 150 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | INFL | INFL-2603-792B | 40 | S | S | S | S | S | S | S | S | S | — |
| 9 | TRA | PENT | PENT-2504-482M | 30 | S | S | S | S | S | S | S | S | S | — |
| 10 | DEV | HEPB | HEPB-2509-474M | 200 | N | S | S | S | S | S | S | N | N | M1+M8 |
| 11 | DEV | IPV | IPV-2608-446B | 240 | S | S | S | S | S | S | S | S | S | — |
| 12 | SAL | SPR | SPR-2606-500M | 30 | S | S | S | S | S | S | S | S | S | — |
| 13 | SAL | DTA | DTA-2602-236K | 50 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | ROTA | ROTA-2605-833M | 150 | S | S | S | S | S | S | S | S | S | — |
| 15 | AJU | IPV | IPV-2504-587B | 40 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | ROTA | ROTA-2507-417A | 200 | S | S | S | S | S | S | S | S | S | — |
| 17 | ING | HEPB | HEPB-2509-474M | 40 | S | S | S | S | S | S | S | S | S | — |
| 18 | ING | INFL | INFL-2508-359M | 150 | S | S | S | S | S | S | S | S | S | — |
| 19 | ING | DTA | DTA-2602-236K | 240 | S | S | S | S | S | S | S | S | S | — |
| 20 | DEV | PENT | PENT-2606-251M | 240 | S | S | S | S | S | S | S | S | S | — |
| 21 | SAL | INFL | INFL-2508-359M | 30 | S | S | S | S | S | S | S | S | S | — |
| 22 | AJU | VARI | VARI-2508-818M | 240 | S | S | S | S | S | S | S | S | S | — |
| 23 | ING | ROTA | ROTA-2602-464A | 120 | S | S | S | S | S | S | S | S | S | — |
| 24 | ING | SPR | SPR-2609-423M | 20 | S | S | S | S | S | S | S | S | S | — |
| 25 | SAL | SPR | SPR-2609-423M | 40 | S | S | S | S | S | S | S | S | S | — |
| 26 | ING | NEUM | NEUM-2509-952A | 80 | S | S | S | S | S | S | S | S | S | — |
| 27 | SAL | DTA | DTA-2602-236K | 60 | S | S | S | S | S | S | S | S | S | — |
| 28 | ING | DTA | DTA-2606-829K | 200 | S | S | S | S | S | S | S | S | S | — |
| 29 | SAL | BCG | BCG-2507-694K | 40 | S | S | S | S | S | S | S | S | S | — |
| 30 | SAL | BCG | BCG-2607-654A | 150 | S | S | S | S | S | S | S | S | S | — |
| 31 | SAL | INFL | INFL-2508-359M | 30 | S | S | S | S | S | S | S | S | S | — |
| 32 | SAL | SPR | SPR-2608-539M | 40 | S | S | S | S | S | S | S | S | S | — |
| 33 | SAL | HEPB | HEPB-2609-917M | 300 | S | S | S | S | S | S | S | S | S | — |
| 34 | SAL | HEPB | HEPB-2602-318M | 30 | S | S | S | S | S | S | S | S | S | — |
| 35 | DEV | ROTA | ROTA-2602-464A | 80 | S | S | S | S | S | S | S | S | S | — |
| 36 | SAL | IPV | IPV-2507-805M | 20 | S | S | S | S | S | S | S | S | S | — |
| 37 | ING | IPV | IPV-2605-698M | 180 | S | S | S | S | S | S | S | S | S | — |
| 38 | DEV | BCG | BCG-2504-789B | 20 | S | S | S | S | S | S | S | S | S | — |
| 39 | ING | BCG | BCG-2507-694K | 240 | S | S | S | S | S | S | S | S | S | — |
| 40 | TRA | SPR | SPR-2504-185M | 50 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-02 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 15/09/2026 | CHANKA-001 | BCG | 120 | 120 | 0 | GR-CHANKA001-1288 | Sí |
| 2 | 14/09/2026 | CHANKA-001 | SPR | 80 | 80 | 0 | GR-CHANKA001-6127 | Sí |
| 3 | 30/09/2026 | CHANKA-001 | NEUM | 80 | 80 | 0 | GR-CHANKA001-4433 | Sí |
| 4 | 22/09/2026 | CHANKA-001 | BCG | 180 | 180 | 0 | GR-CHANKA001-5996 | Sí |
| 5 | 19/09/2026 | CHANKA-001 | IPV | 20 | 15 | -5 | GR-CHANKA001-2687 | No |
| 6 | 28/09/2026 | CHANKA-001 | NEUM | 20 | 20 | 0 | GR-CHANKA001-4728 | Sí |
| 7 | 29/09/2026 | CHANKA-001 | HEPB | 60 | 60 | 0 | GR-CHANKA001-7151 | Sí |
| 8 | 15/09/2026 | CHANKA-001 | INFL | 200 | 200 | 0 | GR-CHANKA001-5188 | Sí |
| 9 | 05/10/2026 | CHANKA-001 | VARI | 100 | 100 | 0 | GR-CHANKA001-3977 | Sí |
| 10 | 14/09/2026 | CHANKA-001 | VARI | 120 | 120 | 0 | GR-CHANKA001-4824 | Sí |
| 11 | 19/09/2026 | CHANKA-001 | HEPB | 100 | 100 | 0 | GR-CHANKA001-4811 | Sí |
| 12 | 14/09/2026 | CHANKA-001 | BCG | 30 | 30 | 0 | GR-CHANKA001-5989 | Sí |
| 13 | 07/10/2026 | CHANKA-001 | PENT | 150 | 150 | 0 | GR-CHANKA001-4803 | Sí |
| 14 | 26/09/2026 | CHANKA-001 | IPV | 30 | 30 | 0 | GR-CHANKA001-4098 | Sí |
| 15 | 07/10/2026 | CHANKA-001 | HEPB | 200 | 200 | 0 | GR-CHANKA001-2919 | Sí |
| 16 | 16/09/2026 | CHANKA-001 | BCG | 80 | 80 | 0 | GR-CHANKA001-1862 | Sí |
| 17 | 18/09/2026 | CHANKA-001 | DTA | 30 | 30 | 0 | GR-CHANKA001-3910 | Sí |
| 18 | 17/09/2026 | CHANKA-001 | SPR | 30 | 30 | 0 | GR-CHANKA001-3523 | Sí |
| 19 | 06/10/2026 | CHANKA-001 | DTA | 40 | 40 | 0 | GR-CHANKA001-5900 | Sí |
| 20 | 11/10/2026 | CHANKA-001 | HEPB | 150 | 150 | 0 | GR-CHANKA001-9114 | Sí |
| 21 | 25/09/2026 | CHANKA-001 | VARI | 120 | 120 | 0 | GR-CHANKA001-4193 | Sí |
| 22 | 22/09/2026 | CHANKA-001 | PENT | 150 | 150 | 0 | GR-CHANKA001-6155 | Sí |
| 23 | 22/09/2026 | CHANKA-001 | HEPB | 50 | 50 | 0 | GR-CHANKA001-3771 | Sí |
| 24 | 28/09/2026 | CHANKA-001 | DTA | 40 | 40 | 0 | GR-CHANKA001-7426 | Sí |
| 25 | 01/10/2026 | CHANKA-001 | HEPB | 150 | 150 | 0 | GR-CHANKA001-3253 | Sí |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 5 · TRAB-03 · Pretest (proceso manual) · 11/08/2026

Documentos auditados: 40 · Conformes: 26 · RSD: 65.00 % · Entregas conciliadas: 25 · Concordantes: 18 · CPE: 72.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | TRA | INFL | INFL-2508-359M | 150 | S | S | S | S | S | S | S | N | N | M8 |
| 2 | SAL | SPR | SPR-2603-471K | 100 | N | S | S | S | N | S | S | S | N | M1+M5 |
| 3 | SAL | INFL | INFL-2504-261K | 300 | S | S | N | S | S | N | S | S | N | M3+M6 |
| 4 | ING | BCG | BCG-2606-296K | 150 | S | S | S | S | S | S | S | S | S | — |
| 5 | AJU | NEUM | NEUM-2505-688A | 180 | S | S | S | S | S | S | S | S | S | — |
| 6 | DEV | ROTA | ROTA-2605-833M | 180 | S | S | S | S | S | S | S | S | S | — |
| 7 | ING | VARI | VARI-2607-979A | 100 | S | S | S | S | S | S | S | S | S | — |
| 8 | DEV | HEPB | HEPB-2609-521M | 60 | S | S | S | S | S | S | S | S | S | — |
| 9 | TRA | SPR | SPR-2609-423M | 300 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | ROTA | ROTA-2602-464A | 100 | S | S | N | S | S | S | S | S | N | M3 |
| 11 | SAL | INFL | INFL-2508-359M | 200 | S | S | S | S | S | S | S | S | S | — |
| 12 | SAL | BCG | BCG-2507-694K | 180 | S | S | S | S | S | S | S | S | S | — |
| 13 | TRA | ROTA | ROTA-2507-417A | 30 | S | S | S | S | S | S | S | S | S | — |
| 14 | TRA | SPR | SPR-2608-539M | 180 | S | S | S | S | S | S | S | S | S | — |
| 15 | ING | DTA | DTA-2606-829K | 120 | S | S | S | S | S | S | S | N | N | M8 |
| 16 | SAL | VARI | VARI-2607-979A | 120 | S | S | S | S | S | S | S | S | S | — |
| 17 | SAL | HEPB | HEPB-2609-917M | 200 | S | S | S | S | S | N | S | S | N | M6 |
| 18 | SAL | VARI | VARI-2607-979A | 80 | S | S | S | S | S | S | S | S | S | — |
| 19 | SAL | HEPB | HEPB-2509-474M | 30 | S | S | S | S | S | S | S | S | S | — |
| 20 | SAL | HEPB | HEPB-2609-521M | 150 | S | S | S | S | S | S | S | S | S | — |
| 21 | TRA | IPV | IPV-2504-587B | 100 | S | S | S | S | S | S | N | S | N | M7 |
| 22 | SAL | IPV | IPV-2504-587B | 60 | S | S | S | S | S | S | S | S | S | — |
| 23 | DEV | BCG | BCG-2606-296K | 20 | S | S | S | S | S | S | S | S | S | — |
| 24 | ING | DTA | DTA-2602-797A | 300 | S | S | S | S | S | S | S | S | S | — |
| 25 | SAL | PENT | PENT-2606-251M | 200 | S | S | S | S | S | S | S | S | S | — |
| 26 | AJU | BCG | BCG-2606-296K | 30 | S | S | N | S | S | N | S | S | N | M3+M6 |
| 27 | ING | VARI | VARI-2501-250M | 60 | S | N | S | S | S | S | S | S | N | M2 |
| 28 | TRA | DTA | DTA-2602-236K | 300 | S | S | S | S | S | S | S | S | S | — |
| 29 | SAL | DTA | DTA-2606-829K | 150 | S | S | S | S | S | S | S | S | S | — |
| 30 | ING | VARI | VARI-2509-637K | 80 | S | S | S | S | S | S | S | S | S | — |
| 31 | DEV | INFL | INFL-2603-792B | 60 | S | S | S | S | S | S | S | S | S | — |
| 32 | AJU | NEUM | NEUM-2506-884B | 100 | S | S | S | S | S | S | S | S | S | — |
| 33 | TRA | HEPB | HEPB-2609-917M | 60 | S | N | S | S | S | S | S | S | N | M2 |
| 34 | SAL | IPV | IPV-2504-587B | 200 | S | S | S | S | S | N | S | S | N | M6 |
| 35 | SAL | BCG | BCG-2606-808K | 40 | S | S | N | S | S | S | S | S | N | M3 |
| 36 | TRA | INFL | INFL-2603-792B | 150 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | DTA | DTA-2602-797A | 40 | S | S | S | S | S | S | N | S | N | M7 |
| 38 | SAL | NEUM | NEUM-2506-884B | 240 | S | S | S | S | S | N | S | S | N | M6 |
| 39 | SAL | IPV | IPV-2507-805M | 60 | S | S | S | S | S | S | S | S | S | — |
| 40 | SAL | DTA | DTA-2603-463K | 20 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-03 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 30/07/2026 | S/C | SPR | 50 | 50 | 0 | GR-SC-4248 | Sí |
| 2 | 10/08/2026 | S/C | PENT | 150 | 150 | 0 | GR-SC-9647 | Sí |
| 3 | 28/07/2026 | S/C | NEUM | 30 | 30 | 0 | GR-SC-2504 | Sí |
| 4 | 08/08/2026 | S/C | ROTA | 120 | 120 | 0 | GR-SC-9062 | Sí |
| 5 | 19/07/2026 | S/C | SPR | 120 | 110 | -10 | Sin guía | No |
| 6 | 25/07/2026 | S/C | SPR | 100 | 100 | 0 | GR-SC-9684 | Sí |
| 7 | 02/08/2026 | S/C | IPV | 20 | 20 | 0 | GR-SC-9449 | Sí |
| 8 | 05/08/2026 | S/C | INFL | 30 | 30 | 0 | GR-SC-3368 | Sí |
| 9 | 24/07/2026 | S/C | HEPB | 30 | 30 | 0 | GR-SC-5066 | Sí |
| 10 | 04/08/2026 | S/C | DTA | 20 | 40 | 20 | GR-SC-8635 | No |
| 11 | 29/07/2026 | S/C | PENT | 200 | 200 | 0 | GR-SC-9222 | Sí |
| 12 | 28/07/2026 | S/C | ROTA | 200 | 200 | 0 | GR-SC-2905 | Sí |
| 13 | 27/07/2026 | S/C | SPR | 120 | 125 | 5 | GR-SC-7390 | No |
| 14 | 18/07/2026 | S/C | DTA | 100 | 100 | 0 | GR-SC-2580 | Sí |
| 15 | 10/08/2026 | S/C | DTA | 100 | 100 | 0 | GR-SC-1707 | Sí |
| 16 | 15/07/2026 | S/C | INFL | 120 | 115 | -5 | GR-SC-1956 | No |
| 17 | 29/07/2026 | S/C | HEPB | 100 | 100 | 0 | GR-SC-7610 | Sí |
| 18 | 31/07/2026 | S/C | IPV | 180 | 180 | 0 | GR-SC-9332 | Sí |
| 19 | 25/07/2026 | S/C | IPV | 100 | 90 | -10 | Sin guía | No |
| 20 | 24/07/2026 | S/C | DTA | 40 | 60 | 20 | GR-SC-5940 | No |
| 21 | 26/07/2026 | S/C | BCG | 50 | 50 | 0 | GR-SC-4901 | Sí |
| 22 | 09/08/2026 | S/C | ROTA | 100 | 100 | 0 | GR-SC-9309 | Sí |
| 23 | 17/07/2026 | S/C | SPR | 50 | 40 | -10 | Sin guía | No |
| 24 | 15/07/2026 | S/C | PENT | 40 | 40 | 0 | GR-SC-3636 | Sí |
| 25 | 10/08/2026 | S/C | HEPB | 200 | 200 | 0 | GR-SC-2525 | Sí |

Cierre: 18 entregas concordantes ÷ 25 × 100 = **72.00 %**.

---

### Bloque 6 · TRAB-03 · Postest (Sistema SIVAC) · 13/10/2026

Documentos auditados: 40 · Conformes: 38 · RSD: 95.00 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | ING | VARI | VARI-2503-521A | 60 | S | S | S | S | S | S | S | S | S | — |
| 2 | SAL | DTA | DTA-2603-463K | 120 | S | S | S | S | S | S | S | S | S | — |
| 3 | AJU | INFL | INFL-2603-792B | 150 | S | S | S | S | S | S | S | S | S | — |
| 4 | TRA | ROTA | ROTA-2605-833M | 40 | S | S | S | S | S | S | S | S | S | — |
| 5 | TRA | DTA | DTA-2602-797A | 40 | S | S | S | S | S | S | S | S | S | — |
| 6 | ING | ROTA | ROTA-2603-156K | 80 | S | S | S | S | S | S | S | S | S | — |
| 7 | DEV | INFL | INFL-2603-792B | 60 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | BCG | BCG-2504-789B | 100 | S | S | S | S | S | S | S | S | S | — |
| 9 | DEV | NEUM | NEUM-2505-638K | 60 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | SPR | SPR-2609-423M | 240 | S | S | S | S | S | S | S | N | N | M8 |
| 11 | ING | DTA | DTA-2602-797A | 20 | S | S | S | S | S | S | S | S | S | — |
| 12 | DEV | BCG | BCG-2504-789B | 240 | S | S | S | S | S | S | S | S | S | — |
| 13 | TRA | HEPB | HEPB-2603-786K | 240 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | ROTA | ROTA-2602-464A | 300 | S | S | S | S | S | S | S | S | S | — |
| 15 | TRA | INFL | INFL-2603-792B | 30 | S | S | S | S | S | S | S | S | S | — |
| 16 | AJU | SPR | SPR-2603-471K | 60 | S | S | S | S | S | S | S | S | S | — |
| 17 | SAL | NEUM | NEUM-2505-638K | 300 | S | S | S | S | S | S | S | S | S | — |
| 18 | SAL | IPV | IPV-2608-446B | 100 | S | S | S | S | S | S | S | S | S | — |
| 19 | ING | SPR | SPR-2609-423M | 150 | S | S | S | S | S | S | S | S | S | — |
| 20 | ING | BCG | BCG-2607-654A | 180 | S | S | S | S | S | S | S | S | S | — |
| 21 | SAL | BCG | BCG-2607-654A | 30 | S | S | S | S | S | S | S | S | S | — |
| 22 | SAL | BCG | BCG-2607-654A | 200 | S | S | S | S | S | S | S | S | S | — |
| 23 | SAL | BCG | BCG-2607-654A | 50 | S | S | S | S | S | S | S | S | S | — |
| 24 | TRA | VARI | VARI-2509-637K | 240 | S | S | S | S | S | S | S | S | S | — |
| 25 | SAL | DTA | DTA-2603-463K | 240 | S | S | S | S | S | S | S | S | S | — |
| 26 | TRA | INFL | INFL-2604-777M | 200 | S | S | S | S | S | S | S | S | S | — |
| 27 | SAL | INFL | INFL-2607-737M | 30 | S | S | S | S | S | S | S | S | S | — |
| 28 | SAL | PENT | PENT-2504-482M | 20 | S | S | S | S | S | S | S | S | S | — |
| 29 | SAL | IPV | IPV-2507-805M | 150 | S | S | S | S | S | S | S | S | S | — |
| 30 | TRA | INFL | INFL-2607-737M | 100 | S | S | S | S | S | S | S | S | S | — |
| 31 | TRA | VARI | VARI-2509-637K | 180 | S | S | S | S | S | S | S | S | S | — |
| 32 | SAL | HEPB | HEPB-2603-786K | 50 | S | S | S | S | S | S | S | S | S | — |
| 33 | SAL | VARI | VARI-2501-250M | 20 | S | S | S | S | S | S | S | S | S | — |
| 34 | DEV | SPR | SPR-2603-471K | 240 | S | S | S | S | S | S | S | S | S | — |
| 35 | TRA | IPV | IPV-2605-698M | 150 | N | S | S | S | S | S | S | N | N | M1+M8 |
| 36 | ING | HEPB | HEPB-2602-318M | 60 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | HEPB | HEPB-2509-474M | 240 | S | S | S | S | S | S | S | S | S | — |
| 38 | SAL | IPV | IPV-2503-662B | 150 | S | S | S | S | S | S | S | S | S | — |
| 39 | ING | SPR | SPR-2609-423M | 50 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | ROTA | ROTA-2502-563B | 150 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-03 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 30/09/2026 | S/C | ROTA | 80 | 80 | 0 | GR-SC-8716 | Sí |
| 2 | 29/09/2026 | S/C | INFL | 40 | 40 | 0 | GR-SC-9536 | Sí |
| 3 | 20/09/2026 | S/C | PENT | 120 | 120 | 0 | GR-SC-8667 | Sí |
| 4 | 15/09/2026 | S/C | INFL | 200 | 200 | 0 | GR-SC-9230 | Sí |
| 5 | 30/09/2026 | S/C | IPV | 180 | 180 | 0 | GR-SC-9134 | Sí |
| 6 | 03/10/2026 | S/C | INFL | 40 | 40 | 0 | GR-SC-2371 | Sí |
| 7 | 07/10/2026 | S/C | HEPB | 60 | 60 | 0 | GR-SC-8182 | Sí |
| 8 | 24/09/2026 | S/C | SPR | 20 | 20 | 0 | GR-SC-4770 | Sí |
| 9 | 19/09/2026 | S/C | DTA | 80 | 80 | 0 | GR-SC-1217 | Sí |
| 10 | 26/09/2026 | S/C | VARI | 50 | 50 | 0 | GR-SC-7871 | Sí |
| 11 | 06/10/2026 | S/C | DTA | 40 | 40 | 0 | GR-SC-8895 | Sí |
| 12 | 30/09/2026 | S/C | SPR | 200 | 200 | 0 | GR-SC-1650 | Sí |
| 13 | 20/09/2026 | S/C | IPV | 80 | 80 | 0 | GR-SC-1202 | Sí |
| 14 | 22/09/2026 | S/C | SPR | 30 | 30 | 0 | GR-SC-2784 | Sí |
| 15 | 19/09/2026 | S/C | BCG | 100 | 100 | 0 | GR-SC-5757 | Sí |
| 16 | 02/10/2026 | S/C | PENT | 20 | 20 | 0 | GR-SC-1925 | Sí |
| 17 | 23/09/2026 | S/C | SPR | 50 | 45 | -5 | GR-SC-5460 | No |
| 18 | 24/09/2026 | S/C | INFL | 50 | 50 | 0 | GR-SC-5851 | Sí |
| 19 | 29/09/2026 | S/C | PENT | 200 | 200 | 0 | GR-SC-4258 | Sí |
| 20 | 08/10/2026 | S/C | BCG | 50 | 50 | 0 | GR-SC-6675 | Sí |
| 21 | 18/09/2026 | S/C | VARI | 150 | 150 | 0 | GR-SC-8253 | Sí |
| 22 | 28/09/2026 | S/C | ROTA | 200 | 200 | 0 | GR-SC-6369 | Sí |
| 23 | 27/09/2026 | S/C | BCG | 100 | 100 | 0 | GR-SC-6547 | Sí |
| 24 | 22/09/2026 | S/C | HEPB | 50 | 50 | 0 | GR-SC-5518 | Sí |
| 25 | 04/10/2026 | S/C | HEPB | 80 | 80 | 0 | GR-SC-7852 | Sí |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 7 · TRAB-04 · Pretest (proceso manual) · 11/08/2026

Documentos auditados: 40 · Conformes: 29 · RSD: 72.50 % · Entregas conciliadas: 25 · Concordantes: 19 · CPE: 76.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | DEV | SPR | SPR-2606-500M | 60 | S | S | S | S | S | S | S | S | S | — |
| 2 | ING | INFL | INFL-2508-359M | 180 | S | S | S | S | S | S | S | N | N | M8 |
| 3 | ING | BCG | BCG-2606-808K | 180 | S | S | S | S | S | S | S | S | S | — |
| 4 | DEV | HEPB | HEPB-2603-786K | 120 | S | S | S | S | S | S | S | S | S | — |
| 5 | SAL | VARI | VARI-2503-521A | 240 | S | S | S | S | S | S | S | S | S | — |
| 6 | TRA | IPV | IPV-2608-446B | 40 | S | S | S | S | S | S | S | S | S | — |
| 7 | TRA | HEPB | HEPB-2602-318M | 60 | S | S | S | S | N | S | S | S | N | M5 |
| 8 | AJU | BCG | BCG-2606-296K | 180 | S | S | S | S | S | S | S | S | S | — |
| 9 | ING | INFL | INFL-2607-737M | 40 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | PENT | PENT-2605-322M | 300 | S | N | S | S | S | S | S | S | N | M2 |
| 11 | SAL | DTA | DTA-2602-236K | 60 | S | S | S | S | S | N | S | S | N | M6 |
| 12 | SAL | NEUM | NEUM-2505-638K | 80 | S | S | S | S | S | N | S | S | N | M6 |
| 13 | ING | VARI | VARI-2503-521A | 150 | S | S | S | S | S | S | S | S | S | — |
| 14 | DEV | BCG | BCG-2606-296K | 120 | S | S | S | S | S | S | S | S | S | — |
| 15 | SAL | VARI | VARI-2508-818M | 20 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | NEUM | NEUM-2509-952A | 240 | S | S | S | S | S | S | N | S | N | M7 |
| 17 | SAL | PENT | PENT-2606-251M | 150 | S | S | S | S | S | S | S | S | S | — |
| 18 | SAL | HEPB | HEPB-2603-786K | 120 | S | S | S | S | S | S | S | S | S | — |
| 19 | SAL | NEUM | NEUM-2505-688A | 40 | S | S | S | S | S | S | S | S | S | — |
| 20 | ING | INFL | INFL-2508-359M | 30 | S | S | S | S | S | N | S | S | N | M6 |
| 21 | ING | HEPB | HEPB-2509-474M | 80 | S | S | S | S | S | S | S | S | S | — |
| 22 | SAL | PENT | PENT-2606-251M | 300 | S | S | S | S | S | S | S | S | S | — |
| 23 | ING | VARI | VARI-2509-637K | 100 | S | S | S | S | S | S | S | S | S | — |
| 24 | TRA | SPR | SPR-2606-500M | 150 | S | S | N | S | S | S | S | S | N | M3 |
| 25 | ING | BCG | BCG-2504-789B | 20 | S | N | S | S | S | N | S | S | N | M2+M6 |
| 26 | ING | NEUM | NEUM-2509-952A | 240 | S | S | S | S | S | S | S | S | S | — |
| 27 | SAL | VARI | VARI-2508-818M | 150 | S | S | S | S | S | S | S | S | S | — |
| 28 | ING | DTA | DTA-2602-797A | 120 | S | S | S | N | S | S | S | S | N | M4 |
| 29 | SAL | HEPB | HEPB-2509-474M | 100 | S | S | S | S | S | S | S | S | S | — |
| 30 | ING | DTA | DTA-2602-236K | 50 | S | S | S | S | S | S | S | S | S | — |
| 31 | TRA | ROTA | ROTA-2502-563B | 20 | S | S | S | S | S | S | S | S | S | — |
| 32 | SAL | ROTA | ROTA-2603-156K | 80 | S | S | S | S | S | S | S | S | S | — |
| 33 | TRA | BCG | BCG-2607-654A | 60 | S | S | S | S | S | S | S | S | S | — |
| 34 | TRA | HEPB | HEPB-2609-917M | 50 | S | S | S | S | S | S | S | S | S | — |
| 35 | TRA | BCG | BCG-2606-808K | 300 | S | S | S | S | S | S | S | S | S | — |
| 36 | TRA | DTA | DTA-2505-409K | 200 | N | S | S | S | S | S | S | N | N | M1+M8 |
| 37 | DEV | INFL | INFL-2607-737M | 150 | S | S | S | S | S | S | S | S | S | — |
| 38 | SAL | BCG | BCG-2507-694K | 240 | S | S | S | S | S | S | S | S | S | — |
| 39 | SAL | SPR | SPR-2603-471K | 80 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | PENT | PENT-2606-251M | 50 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-04 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 18/07/2026 | 11214 | PENT | 180 | 180 | 0 | GR-11214-1867 | Sí |
| 2 | 17/07/2026 | 11214 | ROTA | 60 | 60 | 0 | GR-11214-3727 | Sí |
| 3 | 23/07/2026 | 11214 | INFL | 200 | 200 | 0 | GR-11214-7535 | Sí |
| 4 | 15/07/2026 | 11214 | BCG | 20 | 20 | 0 | GR-11214-6917 | Sí |
| 5 | 09/08/2026 | 11214 | HEPB | 20 | 25 | 5 | Sin guía | No |
| 6 | 07/08/2026 | 11214 | HEPB | 200 | 210 | 10 | GR-11214-3436 | No |
| 7 | 05/08/2026 | 11214 | INFL | 150 | 150 | 0 | GR-11214-3215 | Sí |
| 8 | 29/07/2026 | 11214 | INFL | 60 | 60 | 0 | GR-11214-8558 | Sí |
| 9 | 28/07/2026 | 11214 | SPR | 30 | 30 | 0 | GR-11214-6777 | Sí |
| 10 | 17/07/2026 | 11214 | BCG | 20 | 20 | 0 | GR-11214-3444 | Sí |
| 11 | 07/08/2026 | 11214 | SPR | 60 | 60 | 0 | GR-11214-8380 | Sí |
| 12 | 28/07/2026 | 11214 | HEPB | 20 | 20 | 0 | GR-11214-8787 | Sí |
| 13 | 05/08/2026 | 11214 | DTA | 120 | 110 | -10 | Sin guía | No |
| 14 | 14/07/2026 | 11214 | DTA | 200 | 200 | 0 | GR-11214-6766 | Sí |
| 15 | 25/07/2026 | 11214 | ROTA | 100 | 100 | 0 | GR-11214-6379 | Sí |
| 16 | 04/08/2026 | 11214 | ROTA | 40 | 40 | 0 | GR-11214-7297 | Sí |
| 17 | 04/08/2026 | 11214 | PENT | 180 | 180 | 0 | GR-11214-4321 | Sí |
| 18 | 05/08/2026 | 11214 | DTA | 20 | 20 | 0 | GR-11214-1658 | Sí |
| 19 | 09/08/2026 | 11214 | VARI | 200 | 190 | -10 | GR-11214-3780 | No |
| 20 | 15/07/2026 | 11214 | PENT | 40 | 40 | 0 | GR-11214-1328 | Sí |
| 21 | 10/08/2026 | 11214 | HEPB | 80 | 80 | 0 | GR-11214-9574 | Sí |
| 22 | 19/07/2026 | 11214 | BCG | 100 | 95 | -5 | GR-11214-3004 | No |
| 23 | 10/08/2026 | 11214 | HEPB | 50 | 55 | 5 | Sin guía | No |
| 24 | 02/08/2026 | 11214 | ROTA | 200 | 200 | 0 | GR-11214-8880 | Sí |
| 25 | 20/07/2026 | 11214 | DTA | 180 | 180 | 0 | GR-11214-7473 | Sí |

Cierre: 19 entregas concordantes ÷ 25 × 100 = **76.00 %**.

---

### Bloque 8 · TRAB-04 · Postest (Sistema SIVAC) · 13/10/2026

Documentos auditados: 40 · Conformes: 36 · RSD: 90.00 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | AJU | PENT | PENT-2605-322M | 100 | S | S | S | S | S | S | S | S | S | — |
| 2 | SAL | NEUM | NEUM-2505-688A | 50 | S | S | S | S | S | S | S | S | S | — |
| 3 | SAL | INFL | INFL-2604-777M | 30 | S | S | S | S | S | S | S | S | S | — |
| 4 | ING | DTA | DTA-2505-409K | 180 | S | S | S | S | S | S | S | S | S | — |
| 5 | ING | VARI | VARI-2508-818M | 30 | S | S | S | S | S | S | S | S | S | — |
| 6 | ING | INFL | INFL-2603-792B | 120 | S | S | S | S | S | S | S | S | S | — |
| 7 | TRA | INFL | INFL-2607-737M | 180 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | PENT | PENT-2504-482M | 180 | S | S | S | S | S | S | S | S | S | — |
| 9 | SAL | DTA | DTA-2505-409K | 300 | S | S | S | S | S | S | S | S | S | — |
| 10 | ING | VARI | VARI-2607-979A | 50 | S | S | S | S | S | S | S | S | S | — |
| 11 | AJU | DTA | DTA-2505-409K | 180 | S | S | S | S | S | S | S | S | S | — |
| 12 | SAL | NEUM | NEUM-2505-638K | 50 | S | S | S | S | S | S | S | S | S | — |
| 13 | ING | PENT | PENT-2606-391A | 180 | S | S | S | S | S | S | S | S | S | — |
| 14 | ING | DTA | DTA-2603-463K | 200 | S | S | S | S | S | S | S | S | S | — |
| 15 | SAL | IPV | IPV-2608-446B | 30 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | DTA | DTA-2603-463K | 30 | S | S | S | S | S | S | S | S | S | — |
| 17 | ING | NEUM | NEUM-2506-884B | 300 | S | S | S | S | S | S | S | S | S | — |
| 18 | DEV | ROTA | ROTA-2602-464A | 240 | S | S | S | S | S | S | S | S | S | — |
| 19 | DEV | PENT | PENT-2508-232M | 300 | S | S | S | S | S | S | S | S | S | — |
| 20 | ING | SPR | SPR-2608-539M | 100 | S | S | S | S | S | S | S | S | S | — |
| 21 | DEV | SPR | SPR-2606-500M | 100 | S | S | S | S | S | S | S | S | S | — |
| 22 | DEV | PENT | PENT-2508-232M | 200 | S | S | S | S | S | S | S | S | S | — |
| 23 | TRA | NEUM | NEUM-2506-884B | 240 | S | S | S | S | S | S | S | S | S | — |
| 24 | ING | ROTA | ROTA-2602-464A | 120 | S | N | S | S | S | S | S | N | N | M2+M8 |
| 25 | ING | IPV | IPV-2608-446B | 20 | S | S | S | S | S | S | S | S | S | — |
| 26 | TRA | HEPB | HEPB-2603-786K | 20 | S | S | S | S | S | N | S | S | N | M6 |
| 27 | SAL | DTA | DTA-2603-463K | 40 | S | S | S | S | S | S | S | S | S | — |
| 28 | TRA | VARI | VARI-2501-250M | 120 | S | S | S | N | S | S | S | S | N | M4 |
| 29 | TRA | SPR | SPR-2609-423M | 120 | S | S | S | S | S | S | S | S | S | — |
| 30 | SAL | HEPB | HEPB-2602-318M | 150 | S | S | S | S | S | S | S | S | S | — |
| 31 | SAL | VARI | VARI-2607-979A | 200 | S | S | S | S | S | S | S | S | S | — |
| 32 | SAL | INFL | INFL-2607-737M | 180 | S | S | S | S | S | S | S | S | S | — |
| 33 | ING | PENT | PENT-2504-482M | 30 | S | S | S | S | S | S | S | S | S | — |
| 34 | SAL | VARI | VARI-2503-521A | 240 | S | S | S | S | S | S | S | S | S | — |
| 35 | DEV | INFL | INFL-2508-359M | 60 | S | S | S | S | S | S | S | S | S | — |
| 36 | SAL | INFL | INFL-2603-792B | 30 | S | S | S | S | S | S | S | N | N | M8 |
| 37 | TRA | DTA | DTA-2603-463K | 120 | S | S | S | S | S | S | S | S | S | — |
| 38 | TRA | DTA | DTA-2505-409K | 30 | S | S | S | S | S | S | S | S | S | — |
| 39 | SAL | DTA | DTA-2606-829K | 30 | S | S | S | S | S | S | S | S | S | — |
| 40 | SAL | BCG | BCG-2607-654A | 300 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-04 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 27/09/2026 | 11214 | INFL | 30 | 30 | 0 | GR-11214-8358 | Sí |
| 2 | 20/09/2026 | 11214 | DTA | 20 | 15 | -5 | GR-11214-2646 | No |
| 3 | 21/09/2026 | 11214 | NEUM | 30 | 30 | 0 | GR-11214-4720 | Sí |
| 4 | 28/09/2026 | 11214 | HEPB | 40 | 40 | 0 | GR-11214-7322 | Sí |
| 5 | 01/10/2026 | 11214 | DTA | 60 | 60 | 0 | GR-11214-8699 | Sí |
| 6 | 08/10/2026 | 11214 | PENT | 120 | 120 | 0 | GR-11214-3294 | Sí |
| 7 | 06/10/2026 | 11214 | INFL | 60 | 60 | 0 | GR-11214-8543 | Sí |
| 8 | 15/09/2026 | 11214 | IPV | 40 | 40 | 0 | GR-11214-3071 | Sí |
| 9 | 17/09/2026 | 11214 | SPR | 100 | 100 | 0 | GR-11214-5337 | Sí |
| 10 | 19/09/2026 | 11214 | INFL | 80 | 80 | 0 | GR-11214-3298 | Sí |
| 11 | 30/09/2026 | 11214 | NEUM | 20 | 20 | 0 | GR-11214-4903 | Sí |
| 12 | 02/10/2026 | 11214 | IPV | 20 | 20 | 0 | GR-11214-3021 | Sí |
| 13 | 26/09/2026 | 11214 | NEUM | 60 | 60 | 0 | GR-11214-6153 | Sí |
| 14 | 18/09/2026 | 11214 | DTA | 50 | 50 | 0 | GR-11214-9366 | Sí |
| 15 | 21/09/2026 | 11214 | ROTA | 50 | 50 | 0 | GR-11214-8952 | Sí |
| 16 | 08/10/2026 | 11214 | DTA | 150 | 150 | 0 | GR-11214-2689 | Sí |
| 17 | 24/09/2026 | 11214 | HEPB | 120 | 120 | 0 | GR-11214-4777 | Sí |
| 18 | 02/10/2026 | 11214 | SPR | 30 | 30 | 0 | GR-11214-4071 | Sí |
| 19 | 04/10/2026 | 11214 | INFL | 180 | 180 | 0 | GR-11214-8141 | Sí |
| 20 | 04/10/2026 | 11214 | PENT | 50 | 50 | 0 | GR-11214-5550 | Sí |
| 21 | 26/09/2026 | 11214 | DTA | 80 | 80 | 0 | GR-11214-8085 | Sí |
| 22 | 24/09/2026 | 11214 | INFL | 50 | 50 | 0 | GR-11214-7863 | Sí |
| 23 | 22/09/2026 | 11214 | ROTA | 50 | 50 | 0 | GR-11214-5388 | Sí |
| 24 | 04/10/2026 | 11214 | IPV | 20 | 20 | 0 | GR-11214-8203 | Sí |
| 25 | 29/09/2026 | 11214 | IPV | 60 | 60 | 0 | GR-11214-8920 | Sí |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 9 · TRAB-05 · Pretest (proceso manual) · 12/08/2026

Documentos auditados: 40 · Conformes: 22 · RSD: 55.00 % · Entregas conciliadas: 25 · Concordantes: 15 · CPE: 60.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | AJU | VARI | VARI-2501-250M | 150 | N | S | S | S | S | N | S | S | N | M1+M6 |
| 2 | ING | IPV | IPV-2504-587B | 50 | S | S | S | S | S | S | S | S | S | — |
| 3 | SAL | PENT | PENT-2605-322M | 300 | S | S | S | S | S | S | S | S | S | — |
| 4 | SAL | INFL | INFL-2504-261K | 240 | S | S | S | S | S | S | S | S | S | — |
| 5 | ING | IPV | IPV-2503-662B | 150 | S | S | S | S | S | S | S | S | S | — |
| 6 | DEV | SPR | SPR-2608-539M | 80 | S | S | S | S | S | N | S | S | N | M6 |
| 7 | DEV | ROTA | ROTA-2605-833M | 120 | S | S | S | S | S | S | S | S | S | — |
| 8 | DEV | DTA | DTA-2603-463K | 180 | S | S | N | S | S | S | S | S | N | M3 |
| 9 | TRA | IPV | IPV-2507-805M | 30 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | IPV | IPV-2507-805M | 80 | S | N | S | S | S | S | S | S | N | M2 |
| 11 | SAL | BCG | BCG-2606-296K | 100 | N | S | S | S | S | S | S | S | N | M1 |
| 12 | ING | SPR | SPR-2603-471K | 20 | N | S | S | S | S | S | S | S | N | M1 |
| 13 | AJU | ROTA | ROTA-2507-417A | 200 | S | S | S | S | S | S | S | N | N | M8 |
| 14 | SAL | IPV | IPV-2507-805M | 150 | S | S | S | S | S | S | S | S | S | — |
| 15 | SAL | BCG | BCG-2507-694K | 20 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | VARI | VARI-2501-250M | 120 | S | S | S | S | S | S | S | S | S | — |
| 17 | DEV | VARI | VARI-2509-637K | 120 | S | S | S | S | S | S | N | S | N | M7 |
| 18 | SAL | INFL | INFL-2504-261K | 200 | S | S | N | S | N | S | S | S | N | M3+M5 |
| 19 | ING | IPV | IPV-2504-587B | 300 | S | S | S | S | S | S | S | S | S | — |
| 20 | ING | NEUM | NEUM-2509-952A | 20 | S | S | S | S | S | S | S | S | S | — |
| 21 | ING | IPV | IPV-2605-698M | 50 | S | S | S | S | S | S | S | S | S | — |
| 22 | SAL | SPR | SPR-2609-423M | 100 | S | S | S | S | S | S | S | S | S | — |
| 23 | ING | VARI | VARI-2501-250M | 150 | S | S | S | S | S | S | S | S | S | — |
| 24 | SAL | DTA | DTA-2606-829K | 100 | S | S | S | S | S | S | S | S | S | — |
| 25 | DEV | VARI | VARI-2607-979A | 180 | S | S | S | S | S | S | S | S | S | — |
| 26 | ING | ROTA | ROTA-2602-464A | 240 | S | S | N | S | N | S | S | S | N | M3+M5 |
| 27 | ING | ROTA | ROTA-2603-156K | 30 | S | S | S | S | N | S | N | S | N | M5+M7 |
| 28 | SAL | IPV | IPV-2507-805M | 40 | S | S | S | S | S | S | N | S | N | M7 |
| 29 | SAL | SPR | SPR-2603-471K | 80 | S | S | S | S | S | S | N | S | N | M7 |
| 30 | AJU | ROTA | ROTA-2602-464A | 30 | S | N | S | S | S | S | S | S | N | M2 |
| 31 | SAL | VARI | VARI-2501-250M | 120 | S | S | S | S | S | S | S | S | S | — |
| 32 | DEV | BCG | BCG-2606-296K | 120 | S | S | S | S | S | S | N | S | N | M7 |
| 33 | SAL | PENT | PENT-2508-232M | 40 | S | S | S | S | S | S | S | S | S | — |
| 34 | SAL | SPR | SPR-2609-423M | 50 | S | S | S | S | S | S | S | N | N | M8 |
| 35 | ING | HEPB | HEPB-2603-786K | 300 | S | S | S | S | S | S | S | S | S | — |
| 36 | TRA | SPR | SPR-2606-500M | 30 | S | S | S | S | S | S | N | S | N | M7 |
| 37 | TRA | BCG | BCG-2606-296K | 20 | S | S | S | S | S | S | S | S | S | — |
| 38 | SAL | SPR | SPR-2603-471K | 30 | S | S | S | S | S | S | S | S | S | — |
| 39 | ING | ROTA | ROTA-2507-417A | 100 | S | S | S | S | S | S | S | S | S | — |
| 40 | SAL | HEPB | HEPB-2603-786K | 300 | S | S | S | S | S | S | N | S | N | M7 |

**Entregas conciliadas — TRAB-05 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 31/07/2026 | 6804 | SPR | 100 | 100 | 0 | GR-6804-6088 | Sí |
| 2 | 16/07/2026 | 6804 | BCG | 60 | 60 | 0 | GR-6804-9607 | Sí |
| 3 | 20/07/2026 | 6804 | NEUM | 80 | 70 | -10 | GR-6804-1382 | No |
| 4 | 22/07/2026 | 6804 | HEPB | 100 | 100 | 0 | GR-6804-3006 | Sí |
| 5 | 31/07/2026 | 6804 | SPR | 40 | 40 | 0 | GR-6804-8690 | Sí |
| 6 | 17/07/2026 | 6804 | PENT | 60 | 60 | 0 | GR-6804-1790 | Sí |
| 7 | 28/07/2026 | 6804 | SPR | 80 | 80 | 0 | GR-6804-5929 | Sí |
| 8 | 20/07/2026 | 6804 | PENT | 80 | 80 | 0 | GR-6804-8048 | Sí |
| 9 | 10/08/2026 | 6804 | VARI | 60 | 60 | 0 | GR-6804-7842 | Sí |
| 10 | 23/07/2026 | 6804 | BCG | 40 | 45 | 5 | Sin guía | No |
| 11 | 19/07/2026 | 6804 | SPR | 120 | 120 | 0 | GR-6804-5906 | Sí |
| 12 | 05/08/2026 | 6804 | ROTA | 20 | 15 | -5 | Sin guía | No |
| 13 | 28/07/2026 | 6804 | VARI | 80 | 90 | 10 | GR-6804-6122 | No |
| 14 | 30/07/2026 | 6804 | VARI | 80 | 80 | 0 | GR-6804-9240 | Sí |
| 15 | 26/07/2026 | 6804 | VARI | 100 | 100 | 0 | GR-6804-6073 | Sí |
| 16 | 01/08/2026 | 6804 | ROTA | 100 | 90 | -10 | GR-6804-2782 | No |
| 17 | 03/08/2026 | 6804 | NEUM | 60 | 60 | 0 | GR-6804-8089 | Sí |
| 18 | 22/07/2026 | 6804 | ROTA | 30 | 30 | 0 | GR-6804-8501 | Sí |
| 19 | 20/07/2026 | 6804 | SPR | 80 | 70 | -10 | Sin guía | No |
| 20 | 27/07/2026 | 6804 | VARI | 50 | 50 | 0 | GR-6804-9502 | Sí |
| 21 | 10/08/2026 | 6804 | BCG | 40 | 40 | 0 | GR-6804-1815 | Sí |
| 22 | 11/08/2026 | 6804 | HEPB | 180 | 185 | 5 | Sin guía | No |
| 23 | 04/08/2026 | 6804 | HEPB | 40 | 30 | -10 | Sin guía | No |
| 24 | 15/07/2026 | 6804 | SPR | 40 | 30 | -10 | Sin guía | No |
| 25 | 20/07/2026 | 6804 | PENT | 30 | 25 | -5 | Sin guía | No |

Cierre: 15 entregas concordantes ÷ 25 × 100 = **60.00 %**.

---

### Bloque 10 · TRAB-05 · Postest (Sistema SIVAC) · 14/10/2026

Documentos auditados: 40 · Conformes: 39 · RSD: 97.50 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | DEV | IPV | IPV-2503-662B | 20 | S | S | S | S | S | S | S | S | S | — |
| 2 | ING | VARI | VARI-2607-979A | 120 | S | S | S | S | S | S | S | S | S | — |
| 3 | SAL | DTA | DTA-2602-236K | 240 | S | S | S | S | S | S | S | S | S | — |
| 4 | TRA | NEUM | NEUM-2505-688A | 80 | S | S | S | S | S | S | S | S | S | — |
| 5 | TRA | NEUM | NEUM-2509-952A | 300 | S | S | S | S | S | S | S | S | S | — |
| 6 | ING | IPV | IPV-2608-446B | 150 | S | S | S | S | S | S | S | S | S | — |
| 7 | DEV | IPV | IPV-2608-446B | 20 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | VARI | VARI-2509-637K | 100 | S | S | S | S | S | S | S | S | S | — |
| 9 | SAL | SPR | SPR-2609-423M | 60 | S | S | S | S | S | S | S | S | S | — |
| 10 | TRA | PENT | PENT-2605-322M | 300 | S | S | S | S | S | S | S | S | S | — |
| 11 | AJU | DTA | DTA-2505-409K | 100 | S | S | S | S | S | S | S | S | S | — |
| 12 | DEV | SPR | SPR-2609-423M | 150 | S | S | S | S | S | S | S | S | S | — |
| 13 | ING | VARI | VARI-2509-637K | 150 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | NEUM | NEUM-2507-181K | 300 | S | S | S | S | S | S | S | S | S | — |
| 15 | SAL | INFL | INFL-2504-261K | 100 | S | S | S | S | S | S | S | S | S | — |
| 16 | TRA | PENT | PENT-2606-391A | 40 | S | S | S | S | S | S | S | S | S | — |
| 17 | TRA | NEUM | NEUM-2509-952A | 80 | S | S | S | S | S | S | S | S | S | — |
| 18 | SAL | BCG | BCG-2507-694K | 120 | S | S | S | S | S | S | S | S | S | — |
| 19 | DEV | NEUM | NEUM-2505-638K | 50 | S | S | S | S | S | S | S | S | S | — |
| 20 | ING | VARI | VARI-2503-521A | 40 | S | S | S | S | S | S | S | S | S | — |
| 21 | ING | DTA | DTA-2602-236K | 40 | S | S | S | S | S | S | S | S | S | — |
| 22 | DEV | ROTA | ROTA-2502-563B | 240 | S | S | S | S | S | S | S | S | S | — |
| 23 | DEV | IPV | IPV-2503-662B | 50 | S | S | S | S | S | S | S | S | S | — |
| 24 | SAL | VARI | VARI-2607-979A | 80 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | DTA | DTA-2603-463K | 120 | S | S | S | S | S | S | S | S | S | — |
| 26 | SAL | SPR | SPR-2606-500M | 20 | S | S | S | S | S | S | S | S | S | — |
| 27 | SAL | IPV | IPV-2503-662B | 80 | S | S | S | S | S | S | S | S | S | — |
| 28 | SAL | IPV | IPV-2608-446B | 180 | S | S | S | S | S | S | S | S | S | — |
| 29 | SAL | BCG | BCG-2606-296K | 300 | S | S | S | S | S | N | S | N | N | M6+M8 |
| 30 | ING | IPV | IPV-2504-587B | 100 | S | S | S | S | S | S | S | S | S | — |
| 31 | TRA | PENT | PENT-2606-391A | 60 | S | S | S | S | S | S | S | S | S | — |
| 32 | AJU | ROTA | ROTA-2603-156K | 150 | S | S | S | S | S | S | S | S | S | — |
| 33 | SAL | IPV | IPV-2504-587B | 30 | S | S | S | S | S | S | S | S | S | — |
| 34 | TRA | HEPB | HEPB-2509-474M | 120 | S | S | S | S | S | S | S | S | S | — |
| 35 | TRA | IPV | IPV-2605-698M | 30 | S | S | S | S | S | S | S | S | S | — |
| 36 | DEV | BCG | BCG-2607-654A | 60 | S | S | S | S | S | S | S | S | S | — |
| 37 | AJU | SPR | SPR-2609-423M | 40 | S | S | S | S | S | S | S | S | S | — |
| 38 | SAL | PENT | PENT-2605-322M | 20 | S | S | S | S | S | S | S | S | S | — |
| 39 | TRA | INFL | INFL-2603-792B | 20 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | ROTA | ROTA-2605-833M | 60 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-05 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 13/10/2026 | 6804 | INFL | 40 | 40 | 0 | GR-6804-2129 | Sí |
| 2 | 08/10/2026 | 6804 | ROTA | 60 | 60 | 0 | GR-6804-2187 | Sí |
| 3 | 18/09/2026 | 6804 | HEPB | 50 | 50 | 0 | GR-6804-4034 | Sí |
| 4 | 06/10/2026 | 6804 | HEPB | 180 | 180 | 0 | GR-6804-4894 | Sí |
| 5 | 26/09/2026 | 6804 | VARI | 100 | 100 | 0 | GR-6804-7460 | Sí |
| 6 | 30/09/2026 | 6804 | DTA | 30 | 30 | 0 | GR-6804-2940 | Sí |
| 7 | 09/10/2026 | 6804 | ROTA | 20 | 20 | 0 | GR-6804-7200 | Sí |
| 8 | 02/10/2026 | 6804 | VARI | 80 | 80 | 0 | GR-6804-6556 | Sí |
| 9 | 22/09/2026 | 6804 | SPR | 150 | 150 | 0 | GR-6804-6841 | Sí |
| 10 | 13/10/2026 | 6804 | DTA | 60 | 60 | 0 | GR-6804-7949 | Sí |
| 11 | 13/10/2026 | 6804 | IPV | 80 | 80 | 0 | GR-6804-7297 | Sí |
| 12 | 06/10/2026 | 6804 | NEUM | 60 | 60 | 0 | GR-6804-2842 | Sí |
| 13 | 05/10/2026 | 6804 | NEUM | 30 | 30 | 0 | GR-6804-3368 | Sí |
| 14 | 07/10/2026 | 6804 | INFL | 80 | 70 | -10 | GR-6804-9557 | No |
| 15 | 09/10/2026 | 6804 | ROTA | 50 | 50 | 0 | GR-6804-6188 | Sí |
| 16 | 17/09/2026 | 6804 | BCG | 60 | 60 | 0 | GR-6804-2040 | Sí |
| 17 | 17/09/2026 | 6804 | INFL | 120 | 120 | 0 | GR-6804-3347 | Sí |
| 18 | 23/09/2026 | 6804 | NEUM | 180 | 180 | 0 | GR-6804-9651 | Sí |
| 19 | 12/10/2026 | 6804 | IPV | 20 | 20 | 0 | GR-6804-5301 | Sí |
| 20 | 09/10/2026 | 6804 | IPV | 20 | 20 | 0 | GR-6804-4632 | Sí |
| 21 | 10/10/2026 | 6804 | VARI | 200 | 200 | 0 | GR-6804-2854 | Sí |
| 22 | 18/09/2026 | 6804 | PENT | 30 | 30 | 0 | GR-6804-9050 | Sí |
| 23 | 30/09/2026 | 6804 | VARI | 180 | 180 | 0 | GR-6804-1963 | Sí |
| 24 | 13/10/2026 | 6804 | VARI | 200 | 200 | 0 | GR-6804-2049 | Sí |
| 25 | 22/09/2026 | 6804 | INFL | 80 | 80 | 0 | GR-6804-4263 | Sí |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 11 · TRAB-06 · Pretest (proceso manual) · 12/08/2026

Documentos auditados: 40 · Conformes: 26 · RSD: 65.00 % · Entregas conciliadas: 25 · Concordantes: 17 · CPE: 68.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | TRA | HEPB | HEPB-2609-917M | 200 | S | S | S | S | S | S | S | S | S | — |
| 2 | AJU | ROTA | ROTA-2602-464A | 240 | S | S | S | S | S | S | S | S | S | — |
| 3 | SAL | IPV | IPV-2503-662B | 240 | S | S | S | S | S | S | S | S | S | — |
| 4 | AJU | HEPB | HEPB-2602-318M | 120 | S | S | S | S | S | S | S | S | S | — |
| 5 | SAL | IPV | IPV-2503-662B | 300 | S | S | S | S | S | S | S | S | S | — |
| 6 | ING | IPV | IPV-2504-587B | 300 | S | N | S | S | S | S | S | S | N | M2 |
| 7 | SAL | SPR | SPR-2606-500M | 120 | S | S | S | S | S | S | S | S | S | — |
| 8 | DEV | DTA | DTA-2606-829K | 100 | S | S | S | S | S | S | N | S | N | M7 |
| 9 | SAL | VARI | VARI-2508-818M | 100 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | DTA | DTA-2602-236K | 100 | S | S | S | S | S | S | S | S | S | — |
| 11 | SAL | NEUM | NEUM-2506-884B | 150 | S | S | S | S | S | N | S | S | N | M6 |
| 12 | ING | PENT | PENT-2606-251M | 80 | S | S | S | S | S | S | N | S | N | M7 |
| 13 | ING | VARI | VARI-2501-250M | 30 | S | S | S | S | S | S | N | S | N | M7 |
| 14 | AJU | HEPB | HEPB-2609-917M | 50 | S | S | S | S | S | S | S | N | N | M8 |
| 15 | DEV | VARI | VARI-2503-521A | 300 | S | S | S | S | S | S | S | S | S | — |
| 16 | ING | NEUM | NEUM-2505-638K | 180 | N | S | S | S | S | S | S | S | N | M1 |
| 17 | ING | BCG | BCG-2607-654A | 100 | S | S | S | N | S | S | S | S | N | M4 |
| 18 | TRA | INFL | INFL-2607-737M | 20 | S | S | S | S | S | N | S | S | N | M6 |
| 19 | SAL | DTA | DTA-2602-236K | 180 | S | S | S | S | S | S | S | S | S | — |
| 20 | ING | VARI | VARI-2503-521A | 60 | S | S | S | S | S | S | S | S | S | — |
| 21 | DEV | DTA | DTA-2602-236K | 40 | S | S | S | S | S | S | S | S | S | — |
| 22 | ING | SPR | SPR-2606-500M | 200 | S | S | S | S | S | S | S | S | S | — |
| 23 | ING | BCG | BCG-2507-694K | 30 | S | S | S | S | S | S | N | S | N | M7 |
| 24 | AJU | NEUM | NEUM-2506-884B | 40 | S | N | S | S | N | S | S | S | N | M2+M5 |
| 25 | TRA | SPR | SPR-2504-185M | 100 | S | S | S | S | S | S | S | S | S | — |
| 26 | SAL | BCG | BCG-2606-296K | 300 | S | S | S | S | S | S | S | S | S | — |
| 27 | TRA | VARI | VARI-2501-250M | 40 | S | S | S | S | S | S | S | S | S | — |
| 28 | AJU | IPV | IPV-2504-587B | 240 | S | S | S | S | S | S | S | S | S | — |
| 29 | DEV | VARI | VARI-2509-637K | 20 | S | S | S | S | S | S | N | N | N | M7+M8 |
| 30 | SAL | DTA | DTA-2602-797A | 60 | S | S | S | S | S | S | S | S | S | — |
| 31 | SAL | ROTA | ROTA-2602-464A | 20 | S | S | S | S | S | S | S | S | S | — |
| 32 | TRA | SPR | SPR-2504-185M | 30 | S | S | S | S | S | S | S | S | S | — |
| 33 | SAL | NEUM | NEUM-2505-688A | 180 | S | S | S | S | S | S | S | S | S | — |
| 34 | DEV | NEUM | NEUM-2507-181K | 60 | S | S | S | S | S | S | S | S | S | — |
| 35 | TRA | SPR | SPR-2608-539M | 300 | S | S | S | S | S | S | S | N | N | M8 |
| 36 | ING | SPR | SPR-2603-471K | 50 | S | S | N | S | S | S | S | N | N | M3+M8 |
| 37 | DEV | INFL | INFL-2603-792B | 30 | S | S | S | S | S | S | S | S | S | — |
| 38 | TRA | SPR | SPR-2504-185M | 150 | S | S | S | S | S | S | S | S | S | — |
| 39 | ING | VARI | VARI-2501-250M | 100 | S | S | S | S | S | S | S | S | S | — |
| 40 | DEV | INFL | INFL-2504-261K | 100 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-06 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 07/08/2026 | 4195 | NEUM | 80 | 70 | -10 | GR-4195-2012 | No |
| 2 | 17/07/2026 | 4195 | DTA | 20 | 20 | 0 | GR-4195-3772 | Sí |
| 3 | 23/07/2026 | 4195 | DTA | 120 | 110 | -10 | Sin guía | No |
| 4 | 28/07/2026 | 4195 | INFL | 80 | 85 | 5 | Sin guía | No |
| 5 | 16/07/2026 | 4195 | INFL | 200 | 200 | 0 | GR-4195-8848 | Sí |
| 6 | 10/08/2026 | 4195 | PENT | 20 | 20 | 0 | GR-4195-7694 | Sí |
| 7 | 05/08/2026 | 4195 | SPR | 60 | 55 | -5 | Sin guía | No |
| 8 | 06/08/2026 | 4195 | SPR | 180 | 180 | 0 | GR-4195-2264 | Sí |
| 9 | 11/08/2026 | 4195 | ROTA | 40 | 40 | 0 | GR-4195-7384 | Sí |
| 10 | 07/08/2026 | 4195 | NEUM | 180 | 175 | -5 | Sin guía | No |
| 11 | 07/08/2026 | 4195 | SPR | 120 | 120 | 0 | GR-4195-8005 | Sí |
| 12 | 27/07/2026 | 4195 | IPV | 120 | 120 | 0 | GR-4195-8916 | Sí |
| 13 | 28/07/2026 | 4195 | SPR | 50 | 50 | 0 | GR-4195-2347 | Sí |
| 14 | 25/07/2026 | 4195 | HEPB | 80 | 80 | 0 | GR-4195-4392 | Sí |
| 15 | 02/08/2026 | 4195 | HEPB | 120 | 120 | 0 | GR-4195-2406 | Sí |
| 16 | 20/07/2026 | 4195 | VARI | 20 | 20 | 0 | GR-4195-6789 | Sí |
| 17 | 15/07/2026 | 4195 | IPV | 40 | 40 | 0 | GR-4195-9244 | Sí |
| 18 | 18/07/2026 | 4195 | INFL | 120 | 120 | 0 | GR-4195-4040 | Sí |
| 19 | 07/08/2026 | 4195 | PENT | 150 | 140 | -10 | GR-4195-3834 | No |
| 20 | 11/08/2026 | 4195 | IPV | 100 | 100 | 0 | GR-4195-1697 | Sí |
| 21 | 18/07/2026 | 4195 | VARI | 30 | 30 | 0 | GR-4195-4156 | Sí |
| 22 | 09/08/2026 | 4195 | BCG | 40 | 35 | -5 | GR-4195-3566 | No |
| 23 | 22/07/2026 | 4195 | BCG | 180 | 180 | 0 | GR-4195-1646 | Sí |
| 24 | 19/07/2026 | 4195 | VARI | 180 | 180 | 0 | GR-4195-1414 | Sí |
| 25 | 30/07/2026 | 4195 | DTA | 200 | 190 | -10 | Sin guía | No |

Cierre: 17 entregas concordantes ÷ 25 × 100 = **68.00 %**.

---

### Bloque 12 · TRAB-06 · Postest (Sistema SIVAC) · 14/10/2026

Documentos auditados: 40 · Conformes: 38 · RSD: 95.00 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | TRA | PENT | PENT-2606-251M | 200 | S | S | S | S | S | S | S | S | S | — |
| 2 | DEV | BCG | BCG-2606-808K | 60 | S | S | S | S | S | S | S | S | S | — |
| 3 | SAL | BCG | BCG-2606-808K | 180 | S | S | S | S | S | S | S | S | S | — |
| 4 | TRA | HEPB | HEPB-2509-474M | 60 | S | S | S | S | S | S | S | S | S | — |
| 5 | ING | INFL | INFL-2603-792B | 240 | S | S | S | S | S | S | S | S | S | — |
| 6 | DEV | BCG | BCG-2606-296K | 180 | S | S | S | S | S | S | S | S | S | — |
| 7 | SAL | PENT | PENT-2606-391A | 100 | S | S | S | S | S | S | S | S | S | — |
| 8 | ING | INFL | INFL-2607-737M | 50 | S | S | S | S | S | S | S | S | S | — |
| 9 | TRA | DTA | DTA-2602-236K | 80 | S | S | S | S | S | S | S | S | S | — |
| 10 | TRA | IPV | IPV-2605-698M | 40 | S | S | S | S | S | S | S | S | S | — |
| 11 | ING | ROTA | ROTA-2502-563B | 20 | S | S | S | S | S | S | S | S | S | — |
| 12 | TRA | DTA | DTA-2505-409K | 100 | S | S | S | S | S | S | S | S | S | — |
| 13 | TRA | VARI | VARI-2508-818M | 100 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | BCG | BCG-2507-694K | 200 | S | S | S | S | S | S | S | S | S | — |
| 15 | ING | IPV | IPV-2605-698M | 300 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | ROTA | ROTA-2507-417A | 30 | S | S | S | S | S | S | S | S | S | — |
| 17 | ING | PENT | PENT-2504-482M | 240 | S | S | S | S | S | S | S | S | S | — |
| 18 | SAL | NEUM | NEUM-2507-181K | 300 | S | S | S | S | S | S | S | S | S | — |
| 19 | SAL | ROTA | ROTA-2602-464A | 80 | S | S | S | S | S | S | S | S | S | — |
| 20 | SAL | IPV | IPV-2608-446B | 150 | S | S | S | S | S | S | S | S | S | — |
| 21 | DEV | IPV | IPV-2503-662B | 240 | S | S | S | S | N | N | S | S | N | M5+M6 |
| 22 | SAL | IPV | IPV-2507-805M | 20 | S | S | S | S | S | S | S | S | S | — |
| 23 | SAL | IPV | IPV-2605-698M | 30 | S | S | S | S | S | S | S | S | S | — |
| 24 | TRA | NEUM | NEUM-2505-638K | 30 | S | S | S | S | S | S | S | S | S | — |
| 25 | SAL | HEPB | HEPB-2603-786K | 200 | S | S | S | S | S | S | S | S | S | — |
| 26 | ING | ROTA | ROTA-2602-464A | 50 | S | S | S | S | S | S | S | S | S | — |
| 27 | SAL | SPR | SPR-2606-500M | 50 | S | S | S | S | S | S | S | S | S | — |
| 28 | SAL | BCG | BCG-2607-654A | 200 | S | S | S | S | S | S | S | S | S | — |
| 29 | AJU | PENT | PENT-2606-251M | 30 | S | S | S | S | S | S | S | S | S | — |
| 30 | SAL | VARI | VARI-2607-979A | 50 | S | S | S | S | S | S | S | S | S | — |
| 31 | ING | PENT | PENT-2508-232M | 240 | S | S | S | S | S | S | S | S | S | — |
| 32 | TRA | IPV | IPV-2605-698M | 240 | S | S | S | S | S | S | S | S | S | — |
| 33 | TRA | SPR | SPR-2603-471K | 200 | S | S | S | S | S | S | S | S | S | — |
| 34 | ING | HEPB | HEPB-2609-917M | 180 | S | S | S | S | S | S | S | S | S | — |
| 35 | DEV | IPV | IPV-2608-446B | 300 | S | S | S | S | S | S | S | S | S | — |
| 36 | ING | NEUM | NEUM-2505-688A | 80 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | DTA | DTA-2603-463K | 60 | S | S | S | S | S | S | S | S | S | — |
| 38 | TRA | INFL | INFL-2604-777M | 50 | S | S | S | S | S | S | S | S | S | — |
| 39 | DEV | IPV | IPV-2507-805M | 40 | S | S | N | S | S | S | S | S | N | M3 |
| 40 | TRA | HEPB | HEPB-2603-786K | 150 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-06 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 09/10/2026 | 4195 | NEUM | 40 | 40 | 0 | GR-4195-7921 | Sí |
| 2 | 03/10/2026 | 4195 | IPV | 200 | 200 | 0 | GR-4195-5455 | Sí |
| 3 | 28/09/2026 | 4195 | IPV | 200 | 200 | 0 | GR-4195-4487 | Sí |
| 4 | 19/09/2026 | 4195 | IPV | 60 | 55 | -5 | GR-4195-4224 | No |
| 5 | 18/09/2026 | 4195 | ROTA | 60 | 60 | 0 | GR-4195-3537 | Sí |
| 6 | 06/10/2026 | 4195 | VARI | 30 | 30 | 0 | GR-4195-9774 | Sí |
| 7 | 19/09/2026 | 4195 | IPV | 30 | 30 | 0 | GR-4195-1945 | Sí |
| 8 | 09/10/2026 | 4195 | INFL | 100 | 100 | 0 | GR-4195-7753 | Sí |
| 9 | 29/09/2026 | 4195 | NEUM | 20 | 20 | 0 | GR-4195-4157 | Sí |
| 10 | 03/10/2026 | 4195 | DTA | 60 | 60 | 0 | GR-4195-3093 | Sí |
| 11 | 16/09/2026 | 4195 | VARI | 180 | 180 | 0 | GR-4195-7096 | Sí |
| 12 | 05/10/2026 | 4195 | VARI | 200 | 200 | 0 | GR-4195-7793 | Sí |
| 13 | 25/09/2026 | 4195 | INFL | 200 | 200 | 0 | GR-4195-8922 | Sí |
| 14 | 20/09/2026 | 4195 | ROTA | 150 | 150 | 0 | GR-4195-3123 | Sí |
| 15 | 13/10/2026 | 4195 | DTA | 60 | 60 | 0 | GR-4195-7041 | Sí |
| 16 | 09/10/2026 | 4195 | PENT | 50 | 50 | 0 | GR-4195-8803 | Sí |
| 17 | 17/09/2026 | 4195 | SPR | 40 | 40 | 0 | GR-4195-9303 | Sí |
| 18 | 04/10/2026 | 4195 | IPV | 50 | 50 | 0 | GR-4195-1264 | Sí |
| 19 | 30/09/2026 | 4195 | IPV | 40 | 40 | 0 | GR-4195-5932 | Sí |
| 20 | 22/09/2026 | 4195 | INFL | 40 | 40 | 0 | GR-4195-1459 | Sí |
| 21 | 04/10/2026 | 4195 | IPV | 20 | 20 | 0 | GR-4195-4331 | Sí |
| 22 | 28/09/2026 | 4195 | VARI | 100 | 100 | 0 | GR-4195-4245 | Sí |
| 23 | 13/10/2026 | 4195 | ROTA | 180 | 180 | 0 | GR-4195-6745 | Sí |
| 24 | 27/09/2026 | 4195 | BCG | 60 | 60 | 0 | GR-4195-2894 | Sí |
| 25 | 13/10/2026 | 4195 | HEPB | 180 | 180 | 0 | GR-4195-5514 | Sí |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 13 · TRAB-07 · Pretest (proceso manual) · 13/08/2026

Documentos auditados: 40 · Conformes: 21 · RSD: 52.50 % · Entregas conciliadas: 25 · Concordantes: 14 · CPE: 56.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | ING | NEUM | NEUM-2509-952A | 200 | S | S | S | S | S | S | S | S | S | — |
| 2 | ING | DTA | DTA-2602-236K | 30 | S | S | S | S | S | S | S | S | S | — |
| 3 | TRA | HEPB | HEPB-2609-521M | 80 | S | S | S | S | S | S | S | S | S | — |
| 4 | DEV | VARI | VARI-2509-637K | 200 | S | S | S | S | S | S | N | S | N | M7 |
| 5 | SAL | PENT | PENT-2508-232M | 40 | S | S | S | S | S | S | N | S | N | M7 |
| 6 | SAL | IPV | IPV-2504-587B | 200 | S | S | S | S | S | S | S | S | S | — |
| 7 | SAL | SPR | SPR-2608-539M | 100 | S | N | S | S | S | S | S | N | N | M2+M8 |
| 8 | AJU | NEUM | NEUM-2506-884B | 40 | S | S | S | S | S | N | S | S | N | M6 |
| 9 | ING | BCG | BCG-2507-694K | 30 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | SPR | SPR-2608-539M | 180 | S | S | S | S | S | S | S | S | S | — |
| 11 | TRA | IPV | IPV-2504-587B | 50 | S | S | N | S | S | S | S | S | N | M3 |
| 12 | AJU | PENT | PENT-2606-251M | 50 | S | S | S | S | S | N | S | S | N | M6 |
| 13 | SAL | PENT | PENT-2605-322M | 180 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | HEPB | HEPB-2609-917M | 180 | S | S | N | S | S | S | S | S | N | M3 |
| 15 | SAL | PENT | PENT-2508-232M | 300 | S | S | S | S | S | S | S | S | S | — |
| 16 | ING | HEPB | HEPB-2609-521M | 120 | S | S | S | S | S | S | S | N | N | M8 |
| 17 | SAL | DTA | DTA-2603-463K | 180 | S | S | S | S | S | S | S | S | S | — |
| 18 | DEV | SPR | SPR-2609-423M | 120 | S | N | S | S | S | S | S | S | N | M2 |
| 19 | ING | PENT | PENT-2508-232M | 200 | S | S | S | S | S | S | S | S | S | — |
| 20 | SAL | PENT | PENT-2508-232M | 80 | N | S | S | S | S | S | S | S | N | M1 |
| 21 | SAL | NEUM | NEUM-2505-688A | 100 | S | S | S | S | S | S | S | S | S | — |
| 22 | DEV | INFL | INFL-2603-792B | 20 | S | S | S | S | S | N | S | S | N | M6 |
| 23 | SAL | HEPB | HEPB-2609-521M | 30 | S | S | S | S | S | S | S | S | S | — |
| 24 | SAL | NEUM | NEUM-2505-688A | 120 | S | S | S | S | S | S | S | S | S | — |
| 25 | ING | SPR | SPR-2603-471K | 50 | S | S | S | S | S | S | S | S | S | — |
| 26 | ING | NEUM | NEUM-2505-688A | 80 | S | S | S | S | S | S | S | S | S | — |
| 27 | TRA | ROTA | ROTA-2507-417A | 240 | S | S | S | S | S | S | S | S | S | — |
| 28 | DEV | IPV | IPV-2504-587B | 120 | S | S | S | S | S | S | S | S | S | — |
| 29 | SAL | BCG | BCG-2606-808K | 20 | S | S | N | N | S | S | S | S | N | M3+M4 |
| 30 | SAL | HEPB | HEPB-2609-521M | 50 | S | S | S | S | S | S | S | N | N | M8 |
| 31 | TRA | DTA | DTA-2602-236K | 60 | S | S | S | S | S | S | S | S | S | — |
| 32 | DEV | IPV | IPV-2507-805M | 40 | S | S | S | S | S | S | N | S | N | M7 |
| 33 | TRA | IPV | IPV-2504-587B | 50 | S | S | S | S | S | S | S | S | S | — |
| 34 | TRA | DTA | DTA-2602-236K | 150 | S | S | S | S | S | N | S | S | N | M6 |
| 35 | DEV | VARI | VARI-2501-250M | 20 | S | N | S | N | S | S | S | S | N | M2+M4 |
| 36 | ING | PENT | PENT-2508-232M | 120 | S | S | S | S | S | S | S | S | S | — |
| 37 | ING | DTA | DTA-2505-409K | 120 | S | S | S | S | S | S | N | S | N | M7 |
| 38 | ING | BCG | BCG-2606-808K | 80 | S | S | S | S | S | S | S | S | S | — |
| 39 | DEV | PENT | PENT-2504-482M | 50 | S | S | S | S | S | S | S | N | N | M8 |
| 40 | ING | IPV | IPV-2608-446B | 180 | S | S | N | S | S | S | N | S | N | M3+M7 |

**Entregas conciliadas — TRAB-07 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 30/07/2026 | 4167-SJ | SPR | 40 | 40 | 0 | GR-4167SJ-8383 | Sí |
| 2 | 23/07/2026 | 4167-SJ | BCG | 150 | 145 | -5 | GR-4167SJ-8716 | No |
| 3 | 27/07/2026 | 4167-SJ | ROTA | 180 | 180 | 0 | GR-4167SJ-8736 | Sí |
| 4 | 04/08/2026 | 4167-SJ | INFL | 120 | 115 | -5 | GR-4167SJ-8022 | No |
| 5 | 09/08/2026 | 4167-SJ | NEUM | 20 | 20 | 0 | GR-4167SJ-7298 | Sí |
| 6 | 10/08/2026 | 4167-SJ | DTA | 60 | 60 | 0 | GR-4167SJ-4875 | Sí |
| 7 | 31/07/2026 | 4167-SJ | SPR | 100 | 100 | 0 | GR-4167SJ-8432 | Sí |
| 8 | 31/07/2026 | 4167-SJ | DTA | 20 | 20 | 0 | GR-4167SJ-3921 | Sí |
| 9 | 31/07/2026 | 4167-SJ | INFL | 180 | 185 | 5 | Sin guía | No |
| 10 | 08/08/2026 | 4167-SJ | INFL | 180 | 170 | -10 | Sin guía | No |
| 11 | 26/07/2026 | 4167-SJ | IPV | 60 | 60 | 0 | GR-4167SJ-4991 | Sí |
| 12 | 02/08/2026 | 4167-SJ | DTA | 100 | 100 | 0 | GR-4167SJ-5279 | Sí |
| 13 | 12/08/2026 | 4167-SJ | VARI | 150 | 150 | 0 | GR-4167SJ-7220 | Sí |
| 14 | 18/07/2026 | 4167-SJ | PENT | 40 | 40 | 0 | GR-4167SJ-8240 | Sí |
| 15 | 27/07/2026 | 4167-SJ | PENT | 50 | 40 | -10 | GR-4167SJ-9794 | No |
| 16 | 26/07/2026 | 4167-SJ | INFL | 50 | 55 | 5 | GR-4167SJ-3790 | No |
| 17 | 11/08/2026 | 4167-SJ | VARI | 40 | 40 | 0 | GR-4167SJ-1428 | Sí |
| 18 | 27/07/2026 | 4167-SJ | PENT | 180 | 175 | -5 | Sin guía | No |
| 19 | 10/08/2026 | 4167-SJ | HEPB | 30 | 25 | -5 | GR-4167SJ-5622 | No |
| 20 | 05/08/2026 | 4167-SJ | HEPB | 60 | 60 | 0 | GR-4167SJ-4865 | Sí |
| 21 | 29/07/2026 | 4167-SJ | ROTA | 180 | 180 | 0 | GR-4167SJ-2764 | Sí |
| 22 | 25/07/2026 | 4167-SJ | DTA | 40 | 35 | -5 | GR-4167SJ-6281 | No |
| 23 | 30/07/2026 | 4167-SJ | SPR | 150 | 155 | 5 | GR-4167SJ-6810 | No |
| 24 | 19/07/2026 | 4167-SJ | DTA | 200 | 220 | 20 | GR-4167SJ-6169 | No |
| 25 | 25/07/2026 | 4167-SJ | HEPB | 150 | 150 | 0 | GR-4167SJ-5873 | Sí |

Cierre: 14 entregas concordantes ÷ 25 × 100 = **56.00 %**.

---

### Bloque 14 · TRAB-07 · Postest (Sistema SIVAC) · 15/10/2026

Documentos auditados: 40 · Conformes: 40 · RSD: 100.00 % · Entregas conciliadas: 25 · Concordantes: 23 · CPE: 92.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | SAL | HEPB | HEPB-2602-318M | 120 | S | S | S | S | S | S | S | S | S | — |
| 2 | TRA | IPV | IPV-2605-698M | 40 | S | S | S | S | S | S | S | S | S | — |
| 3 | TRA | HEPB | HEPB-2602-318M | 240 | S | S | S | S | S | S | S | S | S | — |
| 4 | SAL | HEPB | HEPB-2609-521M | 50 | S | S | S | S | S | S | S | S | S | — |
| 5 | SAL | PENT | PENT-2508-232M | 20 | S | S | S | S | S | S | S | S | S | — |
| 6 | ING | VARI | VARI-2503-521A | 100 | S | S | S | S | S | S | S | S | S | — |
| 7 | DEV | PENT | PENT-2508-232M | 200 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | DTA | DTA-2505-409K | 300 | S | S | S | S | S | S | S | S | S | — |
| 9 | ING | HEPB | HEPB-2603-786K | 40 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | INFL | INFL-2603-792B | 60 | S | S | S | S | S | S | S | S | S | — |
| 11 | SAL | BCG | BCG-2504-789B | 80 | S | S | S | S | S | S | S | S | S | — |
| 12 | TRA | DTA | DTA-2602-236K | 120 | S | S | S | S | S | S | S | S | S | — |
| 13 | ING | VARI | VARI-2503-521A | 60 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | SPR | SPR-2608-539M | 20 | S | S | S | S | S | S | S | S | S | — |
| 15 | TRA | PENT | PENT-2606-251M | 80 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | DTA | DTA-2603-463K | 180 | S | S | S | S | S | S | S | S | S | — |
| 17 | TRA | BCG | BCG-2607-654A | 30 | S | S | S | S | S | S | S | S | S | — |
| 18 | ING | NEUM | NEUM-2505-638K | 120 | S | S | S | S | S | S | S | S | S | — |
| 19 | ING | HEPB | HEPB-2602-318M | 80 | S | S | S | S | S | S | S | S | S | — |
| 20 | SAL | INFL | INFL-2607-737M | 150 | S | S | S | S | S | S | S | S | S | — |
| 21 | SAL | HEPB | HEPB-2609-521M | 40 | S | S | S | S | S | S | S | S | S | — |
| 22 | ING | NEUM | NEUM-2505-688A | 60 | S | S | S | S | S | S | S | S | S | — |
| 23 | ING | ROTA | ROTA-2605-833M | 50 | S | S | S | S | S | S | S | S | S | — |
| 24 | TRA | DTA | DTA-2602-797A | 40 | S | S | S | S | S | S | S | S | S | — |
| 25 | ING | INFL | INFL-2504-261K | 100 | S | S | S | S | S | S | S | S | S | — |
| 26 | ING | DTA | DTA-2602-236K | 300 | S | S | S | S | S | S | S | S | S | — |
| 27 | AJU | SPR | SPR-2608-539M | 180 | S | S | S | S | S | S | S | S | S | — |
| 28 | TRA | NEUM | NEUM-2505-638K | 100 | S | S | S | S | S | S | S | S | S | — |
| 29 | AJU | PENT | PENT-2606-391A | 120 | S | S | S | S | S | S | S | S | S | — |
| 30 | ING | DTA | DTA-2603-463K | 200 | S | S | S | S | S | S | S | S | S | — |
| 31 | ING | VARI | VARI-2508-818M | 200 | S | S | S | S | S | S | S | S | S | — |
| 32 | SAL | HEPB | HEPB-2509-474M | 300 | S | S | S | S | S | S | S | S | S | — |
| 33 | TRA | PENT | PENT-2606-391A | 60 | S | S | S | S | S | S | S | S | S | — |
| 34 | SAL | HEPB | HEPB-2609-917M | 60 | S | S | S | S | S | S | S | S | S | — |
| 35 | TRA | INFL | INFL-2604-777M | 40 | S | S | S | S | S | S | S | S | S | — |
| 36 | ING | IPV | IPV-2507-805M | 120 | S | S | S | S | S | S | S | S | S | — |
| 37 | TRA | INFL | INFL-2604-777M | 300 | S | S | S | S | S | S | S | S | S | — |
| 38 | TRA | INFL | INFL-2604-777M | 20 | S | S | S | S | S | S | S | S | S | — |
| 39 | ING | PENT | PENT-2605-322M | 100 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | DTA | DTA-2602-797A | 60 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-07 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 05/10/2026 | 4167-SJ | HEPB | 60 | 60 | 0 | GR-4167SJ-9273 | Sí |
| 2 | 14/10/2026 | 4167-SJ | ROTA | 100 | 100 | 0 | GR-4167SJ-4426 | Sí |
| 3 | 20/09/2026 | 4167-SJ | DTA | 50 | 50 | 0 | GR-4167SJ-7589 | Sí |
| 4 | 18/09/2026 | 4167-SJ | SPR | 180 | 180 | 0 | GR-4167SJ-7609 | Sí |
| 5 | 30/09/2026 | 4167-SJ | VARI | 150 | 150 | 0 | GR-4167SJ-4013 | Sí |
| 6 | 19/09/2026 | 4167-SJ | BCG | 60 | 60 | 0 | GR-4167SJ-4872 | Sí |
| 7 | 01/10/2026 | 4167-SJ | IPV | 50 | 50 | 0 | GR-4167SJ-1468 | Sí |
| 8 | 19/09/2026 | 4167-SJ | SPR | 60 | 60 | 0 | GR-4167SJ-7299 | Sí |
| 9 | 22/09/2026 | 4167-SJ | BCG | 80 | 80 | 0 | GR-4167SJ-6855 | Sí |
| 10 | 23/09/2026 | 4167-SJ | HEPB | 50 | 50 | 0 | GR-4167SJ-7905 | Sí |
| 11 | 25/09/2026 | 4167-SJ | BCG | 180 | 180 | 0 | GR-4167SJ-6929 | Sí |
| 12 | 25/09/2026 | 4167-SJ | VARI | 50 | 55 | 5 | Sin guía | No |
| 13 | 05/10/2026 | 4167-SJ | BCG | 150 | 150 | 0 | GR-4167SJ-8817 | Sí |
| 14 | 21/09/2026 | 4167-SJ | SPR | 40 | 40 | 0 | GR-4167SJ-3816 | Sí |
| 15 | 07/10/2026 | 4167-SJ | IPV | 40 | 40 | 0 | GR-4167SJ-6802 | Sí |
| 16 | 23/09/2026 | 4167-SJ | NEUM | 100 | 100 | 0 | GR-4167SJ-4904 | Sí |
| 17 | 01/10/2026 | 4167-SJ | HEPB | 80 | 80 | 0 | GR-4167SJ-6822 | Sí |
| 18 | 27/09/2026 | 4167-SJ | VARI | 150 | 150 | 0 | GR-4167SJ-1748 | Sí |
| 19 | 12/10/2026 | 4167-SJ | VARI | 40 | 40 | 0 | GR-4167SJ-4351 | Sí |
| 20 | 12/10/2026 | 4167-SJ | HEPB | 150 | 150 | 0 | GR-4167SJ-3571 | Sí |
| 21 | 30/09/2026 | 4167-SJ | DTA | 20 | 20 | 0 | GR-4167SJ-5299 | Sí |
| 22 | 06/10/2026 | 4167-SJ | SPR | 50 | 55 | 5 | GR-4167SJ-5135 | No |
| 23 | 25/09/2026 | 4167-SJ | ROTA | 200 | 200 | 0 | GR-4167SJ-9153 | Sí |
| 24 | 20/09/2026 | 4167-SJ | VARI | 40 | 40 | 0 | GR-4167SJ-6990 | Sí |
| 25 | 26/09/2026 | 4167-SJ | INFL | 200 | 200 | 0 | GR-4167SJ-9129 | Sí |

Cierre: 23 entregas concordantes ÷ 25 × 100 = **92.00 %**.

---

### Bloque 15 · TRAB-08 · Pretest (proceso manual) · 13/08/2026

Documentos auditados: 40 · Conformes: 30 · RSD: 75.00 % · Entregas conciliadas: 25 · Concordantes: 20 · CPE: 80.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | ING | HEPB | HEPB-2609-917M | 60 | S | S | S | S | S | S | S | S | S | — |
| 2 | ING | DTA | DTA-2505-409K | 120 | S | S | S | S | N | S | S | S | N | M5 |
| 3 | TRA | PENT | PENT-2508-232M | 100 | S | S | S | S | S | S | S | S | S | — |
| 4 | ING | IPV | IPV-2503-662B | 30 | S | N | S | S | S | S | S | S | N | M2 |
| 5 | SAL | BCG | BCG-2504-789B | 50 | S | S | S | S | S | S | S | S | S | — |
| 6 | ING | BCG | BCG-2607-654A | 40 | S | S | S | S | S | S | S | S | S | — |
| 7 | ING | SPR | SPR-2603-471K | 240 | S | S | S | S | S | S | S | S | S | — |
| 8 | ING | ROTA | ROTA-2603-156K | 180 | S | S | S | S | S | S | S | S | S | — |
| 9 | ING | NEUM | NEUM-2507-181K | 300 | S | S | S | S | S | S | S | S | S | — |
| 10 | ING | IPV | IPV-2605-698M | 240 | S | S | S | S | S | S | S | S | S | — |
| 11 | DEV | INFL | INFL-2607-737M | 180 | S | S | S | S | S | S | S | S | S | — |
| 12 | ING | IPV | IPV-2605-698M | 30 | S | N | S | S | S | N | S | S | N | M2+M6 |
| 13 | SAL | NEUM | NEUM-2507-181K | 120 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | VARI | VARI-2503-521A | 30 | S | S | S | S | S | S | S | S | S | — |
| 15 | SAL | BCG | BCG-2607-654A | 120 | S | S | S | S | S | S | S | S | S | — |
| 16 | DEV | HEPB | HEPB-2603-786K | 180 | S | S | S | S | S | S | S | S | S | — |
| 17 | SAL | DTA | DTA-2505-409K | 150 | S | S | S | S | S | S | S | S | S | — |
| 18 | SAL | IPV | IPV-2503-662B | 300 | S | S | S | S | S | N | S | S | N | M6 |
| 19 | AJU | BCG | BCG-2606-808K | 120 | S | S | S | S | N | S | S | S | N | M5 |
| 20 | ING | INFL | INFL-2603-792B | 80 | S | S | S | S | S | S | S | S | S | — |
| 21 | SAL | INFL | INFL-2607-737M | 50 | S | S | S | S | N | N | S | S | N | M5+M6 |
| 22 | TRA | NEUM | NEUM-2505-638K | 300 | S | S | S | S | S | S | S | S | S | — |
| 23 | SAL | INFL | INFL-2504-261K | 40 | S | S | S | S | S | S | S | S | S | — |
| 24 | TRA | SPR | SPR-2603-471K | 100 | S | S | S | S | S | S | S | S | S | — |
| 25 | AJU | VARI | VARI-2501-250M | 240 | S | S | S | S | S | S | S | S | S | — |
| 26 | SAL | NEUM | NEUM-2505-638K | 80 | S | S | S | S | S | S | S | S | S | — |
| 27 | SAL | PENT | PENT-2606-251M | 40 | S | S | S | S | S | S | S | S | S | — |
| 28 | ING | HEPB | HEPB-2509-474M | 200 | S | S | S | S | S | S | S | S | S | — |
| 29 | TRA | IPV | IPV-2503-662B | 180 | S | S | S | S | S | N | S | S | N | M6 |
| 30 | SAL | HEPB | HEPB-2603-786K | 80 | S | S | S | S | S | S | S | S | S | — |
| 31 | SAL | INFL | INFL-2508-359M | 40 | S | S | S | S | S | S | S | S | S | — |
| 32 | ING | SPR | SPR-2504-185M | 30 | S | S | S | S | S | N | S | S | N | M6 |
| 33 | SAL | SPR | SPR-2603-471K | 80 | S | S | S | S | S | N | S | S | N | M6 |
| 34 | TRA | VARI | VARI-2503-521A | 30 | S | S | S | S | S | S | S | S | S | — |
| 35 | ING | VARI | VARI-2509-637K | 150 | S | S | S | S | S | S | S | S | S | — |
| 36 | SAL | NEUM | NEUM-2506-884B | 80 | S | S | S | S | S | N | S | S | N | M6 |
| 37 | SAL | SPR | SPR-2609-423M | 20 | S | S | S | S | S | S | S | S | S | — |
| 38 | TRA | HEPB | HEPB-2509-474M | 150 | S | S | S | S | S | S | S | S | S | — |
| 39 | SAL | BCG | BCG-2507-694K | 120 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | SPR | SPR-2609-423M | 180 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-08 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 26/07/2026 | 4158 | ROTA | 150 | 150 | 0 | GR-4158-3958 | Sí |
| 2 | 26/07/2026 | 4158 | INFL | 120 | 120 | 0 | GR-4158-4638 | Sí |
| 3 | 27/07/2026 | 4158 | INFL | 50 | 50 | 0 | GR-4158-9067 | Sí |
| 4 | 11/08/2026 | 4158 | NEUM | 80 | 80 | 0 | GR-4158-2226 | Sí |
| 5 | 03/08/2026 | 4158 | BCG | 50 | 50 | 0 | GR-4158-7299 | Sí |
| 6 | 12/08/2026 | 4158 | NEUM | 60 | 60 | 0 | GR-4158-2464 | Sí |
| 7 | 03/08/2026 | 4158 | HEPB | 100 | 120 | 20 | GR-4158-5440 | No |
| 8 | 01/08/2026 | 4158 | VARI | 100 | 100 | 0 | GR-4158-6849 | Sí |
| 9 | 11/08/2026 | 4158 | IPV | 150 | 150 | 0 | GR-4158-1302 | Sí |
| 10 | 26/07/2026 | 4158 | DTA | 30 | 30 | 0 | GR-4158-8967 | Sí |
| 11 | 11/08/2026 | 4158 | VARI | 100 | 100 | 0 | GR-4158-7180 | Sí |
| 12 | 30/07/2026 | 4158 | ROTA | 200 | 200 | 0 | GR-4158-2373 | Sí |
| 13 | 24/07/2026 | 4158 | HEPB | 180 | 180 | 0 | GR-4158-5162 | Sí |
| 14 | 31/07/2026 | 4158 | DTA | 120 | 120 | 0 | GR-4158-1939 | Sí |
| 15 | 27/07/2026 | 4158 | INFL | 30 | 30 | 0 | GR-4158-1772 | Sí |
| 16 | 04/08/2026 | 4158 | INFL | 30 | 25 | -5 | Sin guía | No |
| 17 | 09/08/2026 | 4158 | IPV | 80 | 75 | -5 | GR-4158-5530 | No |
| 18 | 25/07/2026 | 4158 | NEUM | 50 | 50 | 0 | GR-4158-3825 | Sí |
| 19 | 01/08/2026 | 4158 | INFL | 120 | 110 | -10 | GR-4158-3719 | No |
| 20 | 30/07/2026 | 4158 | ROTA | 50 | 50 | 0 | GR-4158-3752 | Sí |
| 21 | 23/07/2026 | 4158 | HEPB | 100 | 100 | 0 | GR-4158-6817 | Sí |
| 22 | 09/08/2026 | 4158 | DTA | 50 | 50 | 0 | GR-4158-6025 | Sí |
| 23 | 19/07/2026 | 4158 | SPR | 150 | 150 | 0 | GR-4158-4624 | Sí |
| 24 | 21/07/2026 | 4158 | BCG | 20 | 20 | 0 | GR-4158-7997 | Sí |
| 25 | 11/08/2026 | 4158 | PENT | 180 | 170 | -10 | GR-4158-3238 | No |

Cierre: 20 entregas concordantes ÷ 25 × 100 = **80.00 %**.

---

### Bloque 16 · TRAB-08 · Postest (Sistema SIVAC) · 15/10/2026

Documentos auditados: 40 · Conformes: 39 · RSD: 97.50 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | DEV | DTA | DTA-2505-409K | 40 | S | S | S | S | S | S | S | S | S | — |
| 2 | TRA | NEUM | NEUM-2505-638K | 150 | S | S | S | S | S | S | S | S | S | — |
| 3 | SAL | IPV | IPV-2504-587B | 100 | S | S | S | S | S | S | S | S | S | — |
| 4 | AJU | PENT | PENT-2504-482M | 180 | S | S | S | S | S | S | S | S | S | — |
| 5 | AJU | DTA | DTA-2602-236K | 50 | S | S | S | S | S | S | S | S | S | — |
| 6 | TRA | INFL | INFL-2508-359M | 20 | S | S | S | S | S | S | S | S | S | — |
| 7 | AJU | ROTA | ROTA-2602-464A | 240 | S | S | S | S | S | S | S | S | S | — |
| 8 | DEV | VARI | VARI-2503-521A | 240 | S | S | S | S | S | S | S | S | S | — |
| 9 | SAL | IPV | IPV-2503-662B | 240 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | BCG | BCG-2606-808K | 40 | S | S | S | S | S | S | S | S | S | — |
| 11 | ING | IPV | IPV-2605-698M | 50 | S | S | S | S | S | S | S | S | S | — |
| 12 | DEV | SPR | SPR-2609-423M | 60 | S | S | S | S | S | S | S | S | S | — |
| 13 | AJU | ROTA | ROTA-2602-464A | 150 | S | S | S | S | S | S | S | S | S | — |
| 14 | AJU | IPV | IPV-2608-446B | 200 | S | S | S | S | S | S | S | S | S | — |
| 15 | SAL | BCG | BCG-2606-296K | 150 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | INFL | INFL-2607-737M | 300 | S | S | S | S | S | S | S | S | S | — |
| 17 | AJU | INFL | INFL-2603-792B | 200 | S | S | S | S | S | S | S | S | S | — |
| 18 | SAL | VARI | VARI-2508-818M | 120 | S | S | S | S | S | S | S | S | S | — |
| 19 | SAL | DTA | DTA-2603-463K | 50 | S | S | S | S | S | S | S | S | S | — |
| 20 | DEV | NEUM | NEUM-2506-884B | 40 | S | S | S | S | S | N | N | S | N | M6+M7 |
| 21 | SAL | VARI | VARI-2508-818M | 60 | S | S | S | S | S | S | S | S | S | — |
| 22 | AJU | VARI | VARI-2607-979A | 300 | S | S | S | S | S | S | S | S | S | — |
| 23 | ING | HEPB | HEPB-2603-786K | 20 | S | S | S | S | S | S | S | S | S | — |
| 24 | DEV | BCG | BCG-2606-296K | 150 | S | S | S | S | S | S | S | S | S | — |
| 25 | SAL | VARI | VARI-2607-979A | 20 | S | S | S | S | S | S | S | S | S | — |
| 26 | ING | INFL | INFL-2604-777M | 30 | S | S | S | S | S | S | S | S | S | — |
| 27 | ING | DTA | DTA-2602-797A | 200 | S | S | S | S | S | S | S | S | S | — |
| 28 | AJU | VARI | VARI-2503-521A | 120 | S | S | S | S | S | S | S | S | S | — |
| 29 | ING | NEUM | NEUM-2509-952A | 200 | S | S | S | S | S | S | S | S | S | — |
| 30 | DEV | BCG | BCG-2606-296K | 20 | S | S | S | S | S | S | S | S | S | — |
| 31 | SAL | BCG | BCG-2606-296K | 120 | S | S | S | S | S | S | S | S | S | — |
| 32 | SAL | HEPB | HEPB-2509-474M | 180 | S | S | S | S | S | S | S | S | S | — |
| 33 | ING | VARI | VARI-2508-818M | 50 | S | S | S | S | S | S | S | S | S | — |
| 34 | ING | HEPB | HEPB-2603-786K | 180 | S | S | S | S | S | S | S | S | S | — |
| 35 | SAL | NEUM | NEUM-2507-181K | 120 | S | S | S | S | S | S | S | S | S | — |
| 36 | SAL | PENT | PENT-2508-232M | 30 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | BCG | BCG-2504-789B | 60 | S | S | S | S | S | S | S | S | S | — |
| 38 | DEV | SPR | SPR-2608-539M | 300 | S | S | S | S | S | S | S | S | S | — |
| 39 | TRA | VARI | VARI-2501-250M | 120 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | SPR | SPR-2609-423M | 300 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-08 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 14/10/2026 | 4158 | ROTA | 40 | 40 | 0 | GR-4158-3490 | Sí |
| 2 | 03/10/2026 | 4158 | SPR | 40 | 40 | 0 | GR-4158-7925 | Sí |
| 3 | 18/09/2026 | 4158 | HEPB | 150 | 150 | 0 | GR-4158-2447 | Sí |
| 4 | 01/10/2026 | 4158 | BCG | 40 | 40 | 0 | GR-4158-2406 | Sí |
| 5 | 03/10/2026 | 4158 | SPR | 30 | 30 | 0 | GR-4158-2941 | Sí |
| 6 | 08/10/2026 | 4158 | NEUM | 100 | 100 | 0 | GR-4158-3063 | Sí |
| 7 | 13/10/2026 | 4158 | HEPB | 150 | 150 | 0 | GR-4158-3339 | Sí |
| 8 | 20/09/2026 | 4158 | SPR | 40 | 40 | 0 | GR-4158-3012 | Sí |
| 9 | 12/10/2026 | 4158 | IPV | 100 | 100 | 0 | GR-4158-2705 | Sí |
| 10 | 14/10/2026 | 4158 | BCG | 120 | 120 | 0 | GR-4158-4511 | Sí |
| 11 | 10/10/2026 | 4158 | HEPB | 50 | 50 | 0 | GR-4158-2766 | Sí |
| 12 | 18/09/2026 | 4158 | SPR | 120 | 120 | 0 | GR-4158-9642 | Sí |
| 13 | 26/09/2026 | 4158 | DTA | 50 | 40 | -10 | GR-4158-8312 | No |
| 14 | 05/10/2026 | 4158 | IPV | 60 | 60 | 0 | GR-4158-8198 | Sí |
| 15 | 21/09/2026 | 4158 | SPR | 20 | 20 | 0 | GR-4158-4148 | Sí |
| 16 | 19/09/2026 | 4158 | BCG | 120 | 120 | 0 | GR-4158-8501 | Sí |
| 17 | 22/09/2026 | 4158 | BCG | 20 | 20 | 0 | GR-4158-8581 | Sí |
| 18 | 01/10/2026 | 4158 | VARI | 200 | 200 | 0 | GR-4158-7008 | Sí |
| 19 | 21/09/2026 | 4158 | PENT | 180 | 180 | 0 | GR-4158-7584 | Sí |
| 20 | 26/09/2026 | 4158 | NEUM | 180 | 180 | 0 | GR-4158-6335 | Sí |
| 21 | 11/10/2026 | 4158 | DTA | 80 | 80 | 0 | GR-4158-6765 | Sí |
| 22 | 17/09/2026 | 4158 | NEUM | 200 | 200 | 0 | GR-4158-4871 | Sí |
| 23 | 12/10/2026 | 4158 | SPR | 200 | 200 | 0 | GR-4158-8203 | Sí |
| 24 | 01/10/2026 | 4158 | SPR | 150 | 150 | 0 | GR-4158-7269 | Sí |
| 25 | 10/10/2026 | 4158 | BCG | 50 | 50 | 0 | GR-4158-4204 | Sí |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 17 · TRAB-09 · Pretest (proceso manual) · 14/08/2026

Documentos auditados: 40 · Conformes: 29 · RSD: 72.50 % · Entregas conciliadas: 25 · Concordantes: 19 · CPE: 76.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | ING | PENT | PENT-2508-232M | 20 | S | S | S | S | S | S | S | S | S | — |
| 2 | SAL | BCG | BCG-2606-296K | 60 | S | S | S | S | S | N | S | S | N | M6 |
| 3 | SAL | VARI | VARI-2503-521A | 20 | S | S | S | S | S | S | S | S | S | — |
| 4 | SAL | INFL | INFL-2504-261K | 200 | S | S | S | S | S | S | S | S | S | — |
| 5 | ING | IPV | IPV-2605-698M | 30 | S | N | S | S | S | S | S | S | N | M2 |
| 6 | ING | ROTA | ROTA-2605-833M | 20 | S | S | S | S | S | S | S | S | S | — |
| 7 | TRA | SPR | SPR-2608-539M | 80 | S | S | S | S | S | S | S | S | S | — |
| 8 | TRA | NEUM | NEUM-2505-688A | 50 | S | S | S | S | S | S | S | S | S | — |
| 9 | SAL | INFL | INFL-2607-737M | 150 | S | S | S | S | S | N | S | S | N | M6 |
| 10 | DEV | VARI | VARI-2509-637K | 20 | S | S | S | S | S | S | S | S | S | — |
| 11 | SAL | VARI | VARI-2501-250M | 50 | S | S | S | S | S | S | S | S | S | — |
| 12 | SAL | SPR | SPR-2608-539M | 80 | S | S | S | S | S | S | S | S | S | — |
| 13 | ING | HEPB | HEPB-2609-521M | 30 | S | S | S | S | S | S | S | S | S | — |
| 14 | ING | VARI | VARI-2501-250M | 300 | S | N | S | S | S | S | S | S | N | M2 |
| 15 | DEV | BCG | BCG-2606-296K | 100 | S | S | S | S | S | S | S | S | S | — |
| 16 | ING | ROTA | ROTA-2605-833M | 80 | S | S | S | S | S | S | S | S | S | — |
| 17 | TRA | VARI | VARI-2607-979A | 200 | S | S | S | S | S | S | S | S | S | — |
| 18 | ING | VARI | VARI-2509-637K | 50 | S | S | S | S | S | S | S | S | S | — |
| 19 | TRA | PENT | PENT-2605-322M | 300 | S | S | S | S | S | S | S | S | S | — |
| 20 | TRA | SPR | SPR-2608-539M | 80 | S | S | S | S | S | S | S | S | S | — |
| 21 | SAL | IPV | IPV-2503-662B | 180 | S | S | S | S | S | N | S | S | N | M6 |
| 22 | ING | DTA | DTA-2505-409K | 30 | S | S | S | S | N | S | S | N | N | M5+M8 |
| 23 | SAL | IPV | IPV-2503-662B | 150 | S | S | S | S | S | S | S | S | S | — |
| 24 | DEV | SPR | SPR-2609-423M | 80 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | DTA | DTA-2602-236K | 150 | S | S | S | S | S | S | S | S | S | — |
| 26 | ING | NEUM | NEUM-2507-181K | 40 | S | S | S | S | S | S | S | S | S | — |
| 27 | ING | ROTA | ROTA-2603-156K | 20 | S | S | S | S | S | S | S | S | S | — |
| 28 | SAL | NEUM | NEUM-2505-638K | 150 | S | S | S | S | S | S | S | S | S | — |
| 29 | SAL | HEPB | HEPB-2603-786K | 20 | S | S | S | S | S | S | S | S | S | — |
| 30 | ING | DTA | DTA-2606-829K | 100 | S | S | S | S | S | N | S | S | N | M6 |
| 31 | TRA | NEUM | NEUM-2509-952A | 30 | N | S | S | S | N | S | S | S | N | M1+M5 |
| 32 | SAL | VARI | VARI-2501-250M | 150 | S | S | S | S | S | S | S | S | S | — |
| 33 | SAL | ROTA | ROTA-2502-563B | 300 | S | S | S | S | S | S | S | S | S | — |
| 34 | DEV | PENT | PENT-2606-251M | 240 | S | S | S | S | S | S | N | S | N | M7 |
| 35 | TRA | VARI | VARI-2509-637K | 50 | N | S | S | S | S | S | S | S | N | M1 |
| 36 | SAL | DTA | DTA-2603-463K | 60 | S | N | S | S | S | S | S | S | N | M2 |
| 37 | ING | INFL | INFL-2607-737M | 240 | S | S | S | S | S | S | S | S | S | — |
| 38 | ING | PENT | PENT-2508-232M | 80 | S | S | S | S | S | S | S | S | S | — |
| 39 | SAL | HEPB | HEPB-2609-917M | 40 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | ROTA | ROTA-2605-833M | 80 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-09 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 02/08/2026 | 4202 | ROTA | 150 | 150 | 0 | GR-4202-5948 | Sí |
| 2 | 26/07/2026 | 4202 | DTA | 120 | 110 | -10 | GR-4202-3689 | No |
| 3 | 13/08/2026 | 4202 | VARI | 30 | 30 | 0 | GR-4202-3241 | Sí |
| 4 | 22/07/2026 | 4202 | DTA | 100 | 100 | 0 | GR-4202-7223 | Sí |
| 5 | 13/08/2026 | 4202 | PENT | 200 | 200 | 0 | GR-4202-8743 | Sí |
| 6 | 31/07/2026 | 4202 | DTA | 120 | 120 | 0 | GR-4202-2847 | Sí |
| 7 | 18/07/2026 | 4202 | VARI | 100 | 100 | 0 | GR-4202-4982 | Sí |
| 8 | 01/08/2026 | 4202 | VARI | 80 | 80 | 0 | GR-4202-4892 | Sí |
| 9 | 10/08/2026 | 4202 | ROTA | 100 | 95 | -5 | GR-4202-5538 | No |
| 10 | 27/07/2026 | 4202 | ROTA | 20 | 20 | 0 | GR-4202-9570 | Sí |
| 11 | 29/07/2026 | 4202 | BCG | 30 | 30 | 0 | GR-4202-4533 | Sí |
| 12 | 27/07/2026 | 4202 | SPR | 120 | 120 | 0 | GR-4202-7713 | Sí |
| 13 | 23/07/2026 | 4202 | DTA | 40 | 45 | 5 | Sin guía | No |
| 14 | 31/07/2026 | 4202 | NEUM | 30 | 30 | 0 | GR-4202-4087 | Sí |
| 15 | 22/07/2026 | 4202 | DTA | 150 | 150 | 0 | GR-4202-5093 | Sí |
| 16 | 11/08/2026 | 4202 | VARI | 40 | 30 | -10 | GR-4202-8509 | No |
| 17 | 09/08/2026 | 4202 | DTA | 20 | 15 | -5 | Sin guía | No |
| 18 | 02/08/2026 | 4202 | VARI | 80 | 80 | 0 | GR-4202-8645 | Sí |
| 19 | 23/07/2026 | 4202 | SPR | 50 | 40 | -10 | Sin guía | No |
| 20 | 28/07/2026 | 4202 | HEPB | 80 | 80 | 0 | GR-4202-5052 | Sí |
| 21 | 30/07/2026 | 4202 | DTA | 180 | 180 | 0 | GR-4202-2504 | Sí |
| 22 | 20/07/2026 | 4202 | HEPB | 200 | 200 | 0 | GR-4202-8855 | Sí |
| 23 | 19/07/2026 | 4202 | SPR | 60 | 60 | 0 | GR-4202-6777 | Sí |
| 24 | 30/07/2026 | 4202 | INFL | 200 | 200 | 0 | GR-4202-2834 | Sí |
| 25 | 12/08/2026 | 4202 | ROTA | 200 | 200 | 0 | GR-4202-8116 | Sí |

Cierre: 19 entregas concordantes ÷ 25 × 100 = **76.00 %**.

---

### Bloque 18 · TRAB-09 · Postest (Sistema SIVAC) · 16/10/2026

Documentos auditados: 40 · Conformes: 39 · RSD: 97.50 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | ING | DTA | DTA-2505-409K | 180 | S | S | S | S | S | S | S | S | S | — |
| 2 | SAL | ROTA | ROTA-2605-833M | 180 | S | S | S | S | S | S | S | S | S | — |
| 3 | SAL | HEPB | HEPB-2609-917M | 80 | S | S | S | S | S | S | S | S | S | — |
| 4 | SAL | BCG | BCG-2606-808K | 200 | S | S | S | S | S | S | S | S | S | — |
| 5 | SAL | DTA | DTA-2505-409K | 150 | S | S | S | S | S | S | S | S | S | — |
| 6 | ING | PENT | PENT-2606-251M | 30 | S | S | S | S | S | S | S | S | S | — |
| 7 | ING | VARI | VARI-2508-818M | 100 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | INFL | INFL-2508-359M | 100 | S | S | S | S | S | S | S | S | S | — |
| 9 | DEV | VARI | VARI-2607-979A | 120 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | INFL | INFL-2504-261K | 180 | S | S | S | S | S | S | S | S | S | — |
| 11 | ING | INFL | INFL-2607-737M | 30 | S | S | S | S | S | S | S | S | S | — |
| 12 | SAL | ROTA | ROTA-2603-156K | 200 | S | S | S | S | S | S | S | S | S | — |
| 13 | ING | IPV | IPV-2507-805M | 300 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | DTA | DTA-2505-409K | 40 | S | S | S | S | S | S | S | S | S | — |
| 15 | ING | ROTA | ROTA-2602-464A | 30 | S | S | S | S | S | S | S | S | S | — |
| 16 | ING | PENT | PENT-2504-482M | 30 | S | S | S | S | S | S | S | S | S | — |
| 17 | SAL | PENT | PENT-2504-482M | 60 | S | S | S | S | S | S | S | S | S | — |
| 18 | SAL | IPV | IPV-2608-446B | 240 | S | S | S | S | S | S | S | S | S | — |
| 19 | TRA | HEPB | HEPB-2602-318M | 120 | S | S | S | S | S | S | S | S | S | — |
| 20 | SAL | PENT | PENT-2605-322M | 150 | S | S | S | S | S | S | S | S | S | — |
| 21 | ING | DTA | DTA-2505-409K | 80 | S | S | S | S | S | S | S | S | S | — |
| 22 | SAL | BCG | BCG-2606-296K | 60 | S | S | S | S | S | S | S | S | S | — |
| 23 | SAL | VARI | VARI-2501-250M | 20 | S | S | S | S | S | S | S | S | S | — |
| 24 | ING | NEUM | NEUM-2505-638K | 100 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | IPV | IPV-2608-446B | 150 | S | S | S | S | S | S | S | S | S | — |
| 26 | DEV | NEUM | NEUM-2507-181K | 150 | S | S | S | S | S | S | S | S | S | — |
| 27 | TRA | ROTA | ROTA-2602-464A | 100 | S | S | S | S | S | S | S | S | S | — |
| 28 | TRA | ROTA | ROTA-2507-417A | 40 | S | S | S | S | S | S | S | S | S | — |
| 29 | ING | HEPB | HEPB-2609-521M | 80 | S | S | S | S | S | S | S | S | S | — |
| 30 | SAL | DTA | DTA-2603-463K | 60 | S | S | S | S | S | S | S | S | S | — |
| 31 | AJU | PENT | PENT-2508-232M | 180 | S | S | S | S | S | S | S | S | S | — |
| 32 | TRA | ROTA | ROTA-2605-833M | 120 | S | S | S | S | S | S | S | S | S | — |
| 33 | DEV | VARI | VARI-2501-250M | 120 | S | S | S | S | S | S | S | S | S | — |
| 34 | ING | INFL | INFL-2508-359M | 120 | S | S | S | S | S | S | S | S | S | — |
| 35 | SAL | BCG | BCG-2504-789B | 300 | S | S | S | S | S | S | S | S | S | — |
| 36 | SAL | PENT | PENT-2508-232M | 300 | S | S | S | S | S | S | S | S | S | — |
| 37 | ING | IPV | IPV-2504-587B | 100 | S | S | S | N | S | N | S | S | N | M4+M6 |
| 38 | DEV | NEUM | NEUM-2509-952A | 180 | S | S | S | S | S | S | S | S | S | — |
| 39 | TRA | HEPB | HEPB-2509-474M | 180 | S | S | S | S | S | S | S | S | S | — |
| 40 | DEV | SPR | SPR-2608-539M | 240 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-09 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 29/09/2026 | 4202 | IPV | 60 | 60 | 0 | GR-4202-3659 | Sí |
| 2 | 07/10/2026 | 4202 | IPV | 60 | 60 | 0 | GR-4202-8307 | Sí |
| 3 | 24/09/2026 | 4202 | PENT | 20 | 20 | 0 | GR-4202-1582 | Sí |
| 4 | 30/09/2026 | 4202 | INFL | 60 | 60 | 0 | GR-4202-6429 | Sí |
| 5 | 03/10/2026 | 4202 | NEUM | 180 | 180 | 0 | GR-4202-4746 | Sí |
| 6 | 21/09/2026 | 4202 | INFL | 40 | 45 | 5 | Sin guía | No |
| 7 | 20/09/2026 | 4202 | BCG | 40 | 40 | 0 | GR-4202-1876 | Sí |
| 8 | 23/09/2026 | 4202 | NEUM | 120 | 120 | 0 | GR-4202-2415 | Sí |
| 9 | 20/09/2026 | 4202 | VARI | 30 | 30 | 0 | GR-4202-8737 | Sí |
| 10 | 25/09/2026 | 4202 | INFL | 50 | 50 | 0 | GR-4202-3145 | Sí |
| 11 | 21/09/2026 | 4202 | DTA | 50 | 50 | 0 | GR-4202-6375 | Sí |
| 12 | 19/09/2026 | 4202 | IPV | 120 | 120 | 0 | GR-4202-9105 | Sí |
| 13 | 06/10/2026 | 4202 | VARI | 60 | 60 | 0 | GR-4202-9784 | Sí |
| 14 | 18/09/2026 | 4202 | ROTA | 60 | 60 | 0 | GR-4202-3744 | Sí |
| 15 | 20/09/2026 | 4202 | IPV | 30 | 30 | 0 | GR-4202-4527 | Sí |
| 16 | 14/10/2026 | 4202 | ROTA | 180 | 180 | 0 | GR-4202-3840 | Sí |
| 17 | 02/10/2026 | 4202 | DTA | 30 | 30 | 0 | GR-4202-6396 | Sí |
| 18 | 30/09/2026 | 4202 | IPV | 30 | 30 | 0 | GR-4202-4107 | Sí |
| 19 | 20/09/2026 | 4202 | SPR | 150 | 150 | 0 | GR-4202-6320 | Sí |
| 20 | 26/09/2026 | 4202 | INFL | 20 | 20 | 0 | GR-4202-6561 | Sí |
| 21 | 24/09/2026 | 4202 | NEUM | 20 | 20 | 0 | GR-4202-3006 | Sí |
| 22 | 24/09/2026 | 4202 | DTA | 30 | 30 | 0 | GR-4202-9143 | Sí |
| 23 | 15/10/2026 | 4202 | NEUM | 80 | 80 | 0 | GR-4202-3186 | Sí |
| 24 | 13/10/2026 | 4202 | BCG | 100 | 100 | 0 | GR-4202-4110 | Sí |
| 25 | 26/09/2026 | 4202 | ROTA | 120 | 120 | 0 | GR-4202-5053 | Sí |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 19 · TRAB-10 · Pretest (proceso manual) · 14/08/2026

Documentos auditados: 40 · Conformes: 24 · RSD: 60.00 % · Entregas conciliadas: 25 · Concordantes: 16 · CPE: 64.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | ING | NEUM | NEUM-2505-688A | 150 | S | S | S | S | S | S | S | S | S | — |
| 2 | TRA | HEPB | HEPB-2602-318M | 40 | S | S | S | S | S | S | S | S | S | — |
| 3 | ING | SPR | SPR-2608-539M | 240 | S | S | S | S | S | S | S | N | N | M8 |
| 4 | TRA | DTA | DTA-2606-829K | 40 | S | S | S | S | S | S | S | S | S | — |
| 5 | DEV | PENT | PENT-2508-232M | 40 | S | S | S | S | S | S | S | S | S | — |
| 6 | ING | BCG | BCG-2607-654A | 40 | S | S | S | S | N | S | S | S | N | M5 |
| 7 | DEV | IPV | IPV-2605-698M | 300 | S | S | S | S | S | S | S | N | N | M8 |
| 8 | DEV | PENT | PENT-2606-251M | 100 | S | S | S | S | S | S | S | S | S | — |
| 9 | DEV | NEUM | NEUM-2507-181K | 150 | S | S | S | S | S | S | S | S | S | — |
| 10 | TRA | DTA | DTA-2603-463K | 50 | S | S | S | S | S | S | S | N | N | M8 |
| 11 | ING | NEUM | NEUM-2509-952A | 50 | S | S | S | S | S | S | S | N | N | M8 |
| 12 | DEV | VARI | VARI-2503-521A | 20 | S | S | S | S | S | S | S | S | S | — |
| 13 | DEV | IPV | IPV-2605-698M | 150 | S | S | S | S | S | S | S | S | S | — |
| 14 | AJU | NEUM | NEUM-2505-638K | 80 | S | S | S | S | S | S | S | S | S | — |
| 15 | SAL | IPV | IPV-2507-805M | 50 | S | S | S | S | S | S | S | S | S | — |
| 16 | ING | INFL | INFL-2504-261K | 240 | N | S | S | S | S | S | S | S | N | M1 |
| 17 | AJU | NEUM | NEUM-2509-952A | 60 | S | S | S | S | S | S | S | S | S | — |
| 18 | DEV | IPV | IPV-2504-587B | 20 | S | S | S | S | S | S | S | N | N | M8 |
| 19 | DEV | SPR | SPR-2606-500M | 20 | S | S | S | S | S | S | S | S | S | — |
| 20 | AJU | BCG | BCG-2606-296K | 240 | S | S | S | S | S | S | S | S | S | — |
| 21 | ING | NEUM | NEUM-2506-884B | 180 | S | S | S | S | S | S | S | S | S | — |
| 22 | AJU | BCG | BCG-2606-808K | 120 | S | S | S | S | S | S | N | S | N | M7 |
| 23 | AJU | HEPB | HEPB-2509-474M | 150 | N | S | S | S | S | S | S | N | N | M1+M8 |
| 24 | ING | DTA | DTA-2602-797A | 80 | S | S | S | S | S | N | N | S | N | M6+M7 |
| 25 | DEV | SPR | SPR-2608-539M | 120 | S | S | S | S | S | S | S | S | S | — |
| 26 | AJU | IPV | IPV-2507-805M | 300 | S | S | S | S | S | S | S | N | N | M8 |
| 27 | TRA | BCG | BCG-2606-296K | 300 | S | S | S | S | S | N | S | S | N | M6 |
| 28 | DEV | NEUM | NEUM-2507-181K | 300 | S | S | S | S | S | S | S | S | S | — |
| 29 | TRA | INFL | INFL-2504-261K | 40 | S | S | S | S | S | N | N | S | N | M6+M7 |
| 30 | DEV | INFL | INFL-2603-792B | 40 | S | S | S | S | S | S | S | N | N | M8 |
| 31 | TRA | PENT | PENT-2605-322M | 240 | S | S | S | S | S | S | S | S | S | — |
| 32 | ING | PENT | PENT-2606-251M | 80 | S | S | S | S | S | S | S | S | S | — |
| 33 | SAL | IPV | IPV-2605-698M | 200 | S | S | S | S | S | S | S | S | S | — |
| 34 | ING | SPR | SPR-2606-500M | 60 | S | S | S | S | N | S | N | S | N | M5+M7 |
| 35 | SAL | SPR | SPR-2609-423M | 40 | S | S | S | S | S | S | S | S | S | — |
| 36 | TRA | BCG | BCG-2606-808K | 60 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | SPR | SPR-2504-185M | 120 | S | S | S | S | S | S | N | S | N | M7 |
| 38 | AJU | IPV | IPV-2605-698M | 240 | S | S | S | S | S | S | S | S | S | — |
| 39 | TRA | INFL | INFL-2604-777M | 30 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | INFL | INFL-2607-737M | 240 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-10 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 03/08/2026 | 4172 | HEPB | 200 | 200 | 0 | GR-4172-2299 | Sí |
| 2 | 29/07/2026 | 4172 | HEPB | 100 | 90 | -10 | GR-4172-2089 | No |
| 3 | 02/08/2026 | 4172 | ROTA | 180 | 180 | 0 | GR-4172-5744 | Sí |
| 4 | 13/08/2026 | 4172 | DTA | 200 | 200 | 0 | GR-4172-9379 | Sí |
| 5 | 09/08/2026 | 4172 | INFL | 150 | 150 | 0 | GR-4172-7524 | Sí |
| 6 | 17/07/2026 | 4172 | IPV | 60 | 50 | -10 | Sin guía | No |
| 7 | 04/08/2026 | 4172 | SPR | 200 | 205 | 5 | Sin guía | No |
| 8 | 30/07/2026 | 4172 | NEUM | 40 | 40 | 0 | GR-4172-3875 | Sí |
| 9 | 11/08/2026 | 4172 | PENT | 100 | 100 | 0 | GR-4172-4738 | Sí |
| 10 | 01/08/2026 | 4172 | IPV | 20 | 20 | 0 | GR-4172-6093 | Sí |
| 11 | 18/07/2026 | 4172 | SPR | 60 | 50 | -10 | GR-4172-2907 | No |
| 12 | 30/07/2026 | 4172 | ROTA | 120 | 110 | -10 | GR-4172-6132 | No |
| 13 | 17/07/2026 | 4172 | DTA | 150 | 150 | 0 | GR-4172-1744 | Sí |
| 14 | 21/07/2026 | 4172 | NEUM | 200 | 205 | 5 | Sin guía | No |
| 15 | 30/07/2026 | 4172 | DTA | 150 | 155 | 5 | Sin guía | No |
| 16 | 10/08/2026 | 4172 | SPR | 20 | 15 | -5 | GR-4172-3281 | No |
| 17 | 11/08/2026 | 4172 | VARI | 150 | 150 | 0 | GR-4172-5488 | Sí |
| 18 | 06/08/2026 | 4172 | ROTA | 40 | 40 | 0 | GR-4172-3711 | Sí |
| 19 | 24/07/2026 | 4172 | ROTA | 100 | 100 | 0 | GR-4172-4756 | Sí |
| 20 | 11/08/2026 | 4172 | SPR | 30 | 10 | -20 | GR-4172-4103 | No |
| 21 | 22/07/2026 | 4172 | IPV | 20 | 20 | 0 | GR-4172-6373 | Sí |
| 22 | 26/07/2026 | 4172 | ROTA | 100 | 100 | 0 | GR-4172-7563 | Sí |
| 23 | 13/08/2026 | 4172 | NEUM | 80 | 80 | 0 | GR-4172-9376 | Sí |
| 24 | 29/07/2026 | 4172 | IPV | 100 | 100 | 0 | GR-4172-9762 | Sí |
| 25 | 01/08/2026 | 4172 | NEUM | 20 | 20 | 0 | GR-4172-9486 | Sí |

Cierre: 16 entregas concordantes ÷ 25 × 100 = **64.00 %**.

---

### Bloque 20 · TRAB-10 · Postest (Sistema SIVAC) · 16/10/2026

Documentos auditados: 40 · Conformes: 39 · RSD: 97.50 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | ING | BCG | BCG-2606-808K | 20 | S | S | S | S | S | S | S | S | S | — |
| 2 | DEV | BCG | BCG-2607-654A | 100 | S | S | S | S | S | S | S | S | S | — |
| 3 | TRA | IPV | IPV-2503-662B | 240 | S | S | S | S | S | S | S | S | S | — |
| 4 | SAL | BCG | BCG-2507-694K | 100 | S | S | S | S | S | S | S | S | S | — |
| 5 | TRA | DTA | DTA-2603-463K | 200 | S | S | S | S | S | S | S | S | S | — |
| 6 | ING | IPV | IPV-2605-698M | 50 | S | S | S | S | S | S | S | S | S | — |
| 7 | AJU | ROTA | ROTA-2605-833M | 50 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | SPR | SPR-2608-539M | 50 | S | S | S | S | S | S | S | S | S | — |
| 9 | SAL | ROTA | ROTA-2602-464A | 120 | S | S | S | S | S | S | S | S | S | — |
| 10 | AJU | ROTA | ROTA-2602-464A | 200 | S | S | S | S | S | S | S | S | S | — |
| 11 | ING | NEUM | NEUM-2506-884B | 100 | S | S | S | S | S | S | S | S | S | — |
| 12 | DEV | IPV | IPV-2503-662B | 180 | S | S | S | S | S | S | S | S | S | — |
| 13 | SAL | BCG | BCG-2504-789B | 240 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | HEPB | HEPB-2509-474M | 100 | S | S | S | S | S | S | S | S | S | — |
| 15 | TRA | ROTA | ROTA-2605-833M | 300 | S | S | S | S | S | S | S | S | S | — |
| 16 | DEV | HEPB | HEPB-2603-786K | 240 | S | S | S | S | S | S | S | S | S | — |
| 17 | TRA | DTA | DTA-2602-236K | 80 | S | S | S | S | S | S | S | S | S | — |
| 18 | AJU | DTA | DTA-2505-409K | 100 | S | S | S | S | S | S | S | S | S | — |
| 19 | AJU | HEPB | HEPB-2609-917M | 300 | S | S | S | S | S | S | S | S | S | — |
| 20 | ING | HEPB | HEPB-2609-521M | 180 | S | S | S | S | S | S | S | S | S | — |
| 21 | ING | INFL | INFL-2504-261K | 100 | S | S | S | S | S | S | S | S | S | — |
| 22 | TRA | HEPB | HEPB-2603-786K | 80 | S | S | S | S | S | S | S | S | S | — |
| 23 | TRA | ROTA | ROTA-2602-464A | 150 | S | S | S | N | S | S | N | S | N | M4+M7 |
| 24 | SAL | INFL | INFL-2607-737M | 30 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | PENT | PENT-2606-251M | 30 | S | S | S | S | S | S | S | S | S | — |
| 26 | SAL | INFL | INFL-2504-261K | 150 | S | S | S | S | S | S | S | S | S | — |
| 27 | ING | IPV | IPV-2608-446B | 80 | S | S | S | S | S | S | S | S | S | — |
| 28 | ING | PENT | PENT-2606-391A | 100 | S | S | S | S | S | S | S | S | S | — |
| 29 | TRA | PENT | PENT-2504-482M | 200 | S | S | S | S | S | S | S | S | S | — |
| 30 | TRA | SPR | SPR-2504-185M | 50 | S | S | S | S | S | S | S | S | S | — |
| 31 | TRA | PENT | PENT-2605-322M | 40 | S | S | S | S | S | S | S | S | S | — |
| 32 | ING | IPV | IPV-2608-446B | 50 | S | S | S | S | S | S | S | S | S | — |
| 33 | SAL | VARI | VARI-2501-250M | 100 | S | S | S | S | S | S | S | S | S | — |
| 34 | ING | PENT | PENT-2606-391A | 40 | S | S | S | S | S | S | S | S | S | — |
| 35 | AJU | PENT | PENT-2606-391A | 30 | S | S | S | S | S | S | S | S | S | — |
| 36 | SAL | IPV | IPV-2608-446B | 150 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | PENT | PENT-2504-482M | 30 | S | S | S | S | S | S | S | S | S | — |
| 38 | AJU | BCG | BCG-2504-789B | 150 | S | S | S | S | S | S | S | S | S | — |
| 39 | ING | SPR | SPR-2504-185M | 60 | S | S | S | S | S | S | S | S | S | — |
| 40 | SAL | VARI | VARI-2501-250M | 150 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-10 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 03/10/2026 | 4172 | INFL | 50 | 50 | 0 | GR-4172-6210 | Sí |
| 2 | 20/09/2026 | 4172 | NEUM | 80 | 80 | 0 | GR-4172-2025 | Sí |
| 3 | 19/09/2026 | 4172 | IPV | 60 | 60 | 0 | GR-4172-7539 | Sí |
| 4 | 12/10/2026 | 4172 | PENT | 80 | 80 | 0 | GR-4172-6040 | Sí |
| 5 | 11/10/2026 | 4172 | NEUM | 200 | 200 | 0 | GR-4172-7963 | Sí |
| 6 | 15/10/2026 | 4172 | IPV | 30 | 30 | 0 | GR-4172-9294 | Sí |
| 7 | 23/09/2026 | 4172 | IPV | 30 | 30 | 0 | GR-4172-7542 | Sí |
| 8 | 02/10/2026 | 4172 | BCG | 50 | 50 | 0 | GR-4172-7949 | Sí |
| 9 | 18/09/2026 | 4172 | VARI | 50 | 45 | -5 | GR-4172-3729 | No |
| 10 | 13/10/2026 | 4172 | NEUM | 40 | 40 | 0 | GR-4172-1836 | Sí |
| 11 | 11/10/2026 | 4172 | IPV | 150 | 150 | 0 | GR-4172-2360 | Sí |
| 12 | 25/09/2026 | 4172 | DTA | 150 | 150 | 0 | GR-4172-5539 | Sí |
| 13 | 27/09/2026 | 4172 | DTA | 60 | 60 | 0 | GR-4172-9728 | Sí |
| 14 | 27/09/2026 | 4172 | VARI | 80 | 80 | 0 | GR-4172-2139 | Sí |
| 15 | 23/09/2026 | 4172 | DTA | 40 | 40 | 0 | GR-4172-5867 | Sí |
| 16 | 10/10/2026 | 4172 | ROTA | 20 | 20 | 0 | GR-4172-9450 | Sí |
| 17 | 03/10/2026 | 4172 | IPV | 100 | 100 | 0 | GR-4172-9047 | Sí |
| 18 | 11/10/2026 | 4172 | ROTA | 200 | 200 | 0 | GR-4172-6659 | Sí |
| 19 | 15/10/2026 | 4172 | NEUM | 20 | 20 | 0 | GR-4172-8787 | Sí |
| 20 | 18/09/2026 | 4172 | ROTA | 150 | 150 | 0 | GR-4172-5421 | Sí |
| 21 | 28/09/2026 | 4172 | ROTA | 50 | 50 | 0 | GR-4172-5820 | Sí |
| 22 | 01/10/2026 | 4172 | IPV | 50 | 50 | 0 | GR-4172-8083 | Sí |
| 23 | 06/10/2026 | 4172 | ROTA | 150 | 150 | 0 | GR-4172-2882 | Sí |
| 24 | 12/10/2026 | 4172 | VARI | 200 | 200 | 0 | GR-4172-2435 | Sí |
| 25 | 21/09/2026 | 4172 | HEPB | 180 | 180 | 0 | GR-4172-4413 | Sí |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 21 · TRAB-11 · Pretest (proceso manual) · 07/09/2026

Documentos auditados: 40 · Conformes: 25 · RSD: 62.50 % · Entregas conciliadas: 25 · Concordantes: 17 · CPE: 68.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | SAL | HEPB | HEPB-2609-917M | 300 | S | S | S | S | S | S | N | S | N | M7 |
| 2 | ING | PENT | PENT-2605-322M | 40 | S | S | S | S | S | S | S | S | S | — |
| 3 | DEV | SPR | SPR-2606-500M | 100 | S | S | S | S | S | S | S | S | S | — |
| 4 | ING | NEUM | NEUM-2507-181K | 240 | N | S | S | S | S | S | S | S | N | M1 |
| 5 | DEV | INFL | INFL-2508-359M | 20 | S | S | S | S | S | S | S | S | S | — |
| 6 | SAL | VARI | VARI-2501-250M | 150 | S | S | S | S | S | S | S | S | S | — |
| 7 | TRA | PENT | PENT-2605-322M | 80 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | ROTA | ROTA-2507-417A | 100 | S | S | N | S | S | S | S | S | N | M3 |
| 9 | TRA | DTA | DTA-2603-463K | 30 | S | S | S | S | S | S | S | S | S | — |
| 10 | TRA | NEUM | NEUM-2509-952A | 80 | S | S | S | S | S | N | S | S | N | M6 |
| 11 | ING | VARI | VARI-2509-637K | 40 | S | S | S | S | N | S | N | S | N | M5+M7 |
| 12 | DEV | HEPB | HEPB-2509-474M | 60 | S | S | S | S | S | S | S | S | S | — |
| 13 | SAL | DTA | DTA-2606-829K | 80 | S | S | S | S | S | S | S | S | S | — |
| 14 | ING | HEPB | HEPB-2603-786K | 40 | S | S | S | S | S | S | S | S | S | — |
| 15 | ING | HEPB | HEPB-2609-521M | 40 | S | S | S | S | S | N | S | S | N | M6 |
| 16 | SAL | IPV | IPV-2507-805M | 20 | N | S | S | N | S | S | S | S | N | M1+M4 |
| 17 | SAL | DTA | DTA-2606-829K | 150 | S | S | S | S | S | S | S | S | S | — |
| 18 | ING | ROTA | ROTA-2602-464A | 200 | S | S | S | S | S | S | S | S | S | — |
| 19 | ING | VARI | VARI-2508-818M | 60 | S | S | S | S | S | S | S | S | S | — |
| 20 | TRA | SPR | SPR-2608-539M | 60 | S | S | S | S | S | S | S | N | N | M8 |
| 21 | SAL | INFL | INFL-2504-261K | 200 | S | S | S | S | S | S | S | S | S | — |
| 22 | SAL | DTA | DTA-2602-236K | 20 | S | S | S | S | N | S | S | S | N | M5 |
| 23 | TRA | NEUM | NEUM-2507-181K | 180 | S | S | N | S | S | S | S | S | N | M3 |
| 24 | ING | BCG | BCG-2507-694K | 100 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | VARI | VARI-2607-979A | 60 | S | S | S | S | S | S | S | S | S | — |
| 26 | SAL | PENT | PENT-2606-391A | 100 | S | S | S | S | S | S | S | S | S | — |
| 27 | DEV | INFL | INFL-2603-792B | 50 | S | S | S | S | S | S | S | S | S | — |
| 28 | TRA | HEPB | HEPB-2609-917M | 20 | S | S | S | S | S | S | S | S | S | — |
| 29 | TRA | VARI | VARI-2503-521A | 150 | N | S | S | S | S | S | S | S | N | M1 |
| 30 | ING | ROTA | ROTA-2605-833M | 100 | S | S | S | S | N | S | S | S | N | M5 |
| 31 | ING | BCG | BCG-2606-296K | 60 | S | S | S | S | S | S | S | S | S | — |
| 32 | SAL | INFL | INFL-2603-792B | 20 | S | N | S | S | S | S | S | S | N | M2 |
| 33 | ING | SPR | SPR-2606-500M | 30 | S | S | S | S | S | S | S | S | S | — |
| 34 | SAL | ROTA | ROTA-2603-156K | 100 | S | S | S | S | S | S | S | S | S | — |
| 35 | ING | DTA | DTA-2602-797A | 60 | S | S | S | S | S | N | S | S | N | M6 |
| 36 | ING | SPR | SPR-2603-471K | 60 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | VARI | VARI-2508-818M | 30 | S | S | S | S | S | S | S | S | S | — |
| 38 | TRA | PENT | PENT-2504-482M | 60 | S | S | S | S | S | S | S | S | S | — |
| 39 | TRA | INFL | INFL-2603-792B | 120 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | VARI | VARI-2509-637K | 150 | S | S | S | N | S | S | N | S | N | M4+M7 |

**Entregas conciliadas — TRAB-11 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 06/09/2026 | 4167 | VARI | 200 | 200 | 0 | GR-4167-1211 | Sí |
| 2 | 14/08/2026 | 4167 | INFL | 20 | 20 | 0 | GR-4167-7815 | Sí |
| 3 | 29/08/2026 | 4167 | SPR | 150 | 150 | 0 | GR-4167-4643 | Sí |
| 4 | 14/08/2026 | 4167 | PENT | 50 | 50 | 0 | GR-4167-8191 | Sí |
| 5 | 28/08/2026 | 4167 | DTA | 120 | 120 | 0 | GR-4167-3964 | Sí |
| 6 | 21/08/2026 | 4167 | INFL | 30 | 30 | 0 | GR-4167-7702 | Sí |
| 7 | 19/08/2026 | 4167 | VARI | 50 | 50 | 0 | GR-4167-1387 | Sí |
| 8 | 17/08/2026 | 4167 | HEPB | 100 | 100 | 0 | GR-4167-4834 | Sí |
| 9 | 05/09/2026 | 4167 | INFL | 180 | 170 | -10 | Sin guía | No |
| 10 | 01/09/2026 | 4167 | IPV | 80 | 75 | -5 | Sin guía | No |
| 11 | 20/08/2026 | 4167 | DTA | 60 | 55 | -5 | Sin guía | No |
| 12 | 15/08/2026 | 4167 | ROTA | 100 | 100 | 0 | GR-4167-3772 | Sí |
| 13 | 05/09/2026 | 4167 | ROTA | 80 | 80 | 0 | GR-4167-3469 | Sí |
| 14 | 05/09/2026 | 4167 | SPR | 80 | 60 | -20 | GR-4167-3782 | No |
| 15 | 31/08/2026 | 4167 | PENT | 40 | 40 | 0 | GR-4167-4546 | Sí |
| 16 | 19/08/2026 | 4167 | DTA | 80 | 75 | -5 | GR-4167-4070 | No |
| 17 | 12/08/2026 | 4167 | NEUM | 180 | 180 | 0 | GR-4167-4850 | Sí |
| 18 | 11/08/2026 | 4167 | ROTA | 20 | 20 | 0 | GR-4167-4434 | Sí |
| 19 | 29/08/2026 | 4167 | DTA | 30 | 25 | -5 | Sin guía | No |
| 20 | 11/08/2026 | 4167 | DTA | 60 | 60 | 0 | GR-4167-3263 | Sí |
| 21 | 05/09/2026 | 4167 | HEPB | 40 | 40 | 0 | GR-4167-2689 | Sí |
| 22 | 28/08/2026 | 4167 | HEPB | 60 | 60 | 0 | GR-4167-4886 | Sí |
| 23 | 30/08/2026 | 4167 | INFL | 120 | 110 | -10 | GR-4167-8823 | No |
| 24 | 25/08/2026 | 4167 | HEPB | 20 | 20 | 0 | GR-4167-6865 | Sí |
| 25 | 14/08/2026 | 4167 | INFL | 40 | 60 | 20 | GR-4167-2484 | No |

Cierre: 17 entregas concordantes ÷ 25 × 100 = **68.00 %**.

---

### Bloque 22 · TRAB-11 · Postest (Sistema SIVAC) · 19/10/2026

Documentos auditados: 40 · Conformes: 38 · RSD: 95.00 % · Entregas conciliadas: 25 · Concordantes: 23 · CPE: 92.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | SAL | ROTA | ROTA-2602-464A | 60 | S | S | S | S | S | S | S | S | S | — |
| 2 | ING | IPV | IPV-2608-446B | 180 | S | S | S | S | S | S | S | S | S | — |
| 3 | ING | HEPB | HEPB-2603-786K | 200 | S | S | S | S | S | S | S | S | S | — |
| 4 | TRA | SPR | SPR-2608-539M | 20 | S | S | S | S | S | S | S | S | S | — |
| 5 | SAL | BCG | BCG-2507-694K | 200 | S | S | S | S | S | S | S | S | S | — |
| 6 | AJU | IPV | IPV-2503-662B | 80 | S | S | S | S | S | S | S | S | S | — |
| 7 | ING | HEPB | HEPB-2609-521M | 60 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | PENT | PENT-2504-482M | 80 | S | S | S | S | S | S | S | S | S | — |
| 9 | AJU | ROTA | ROTA-2605-833M | 80 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | ROTA | ROTA-2605-833M | 80 | S | S | S | S | S | S | S | S | S | — |
| 11 | ING | ROTA | ROTA-2507-417A | 150 | S | S | S | S | S | S | S | S | S | — |
| 12 | TRA | HEPB | HEPB-2609-521M | 80 | S | S | S | S | S | S | S | S | S | — |
| 13 | SAL | DTA | DTA-2505-409K | 50 | S | S | S | S | S | S | S | S | S | — |
| 14 | TRA | ROTA | ROTA-2605-833M | 100 | S | S | S | S | S | S | S | S | S | — |
| 15 | SAL | NEUM | NEUM-2505-688A | 30 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | ROTA | ROTA-2502-563B | 50 | S | S | S | S | S | S | S | S | S | — |
| 17 | TRA | HEPB | HEPB-2603-786K | 200 | S | S | S | S | S | S | S | S | S | — |
| 18 | AJU | SPR | SPR-2606-500M | 50 | S | S | S | S | S | S | S | S | S | — |
| 19 | AJU | IPV | IPV-2503-662B | 180 | S | S | S | S | S | S | S | S | S | — |
| 20 | TRA | SPR | SPR-2603-471K | 150 | S | S | S | S | S | S | S | S | S | — |
| 21 | SAL | ROTA | ROTA-2507-417A | 180 | S | S | S | S | S | S | S | S | S | — |
| 22 | TRA | DTA | DTA-2603-463K | 300 | S | S | S | S | S | S | S | S | S | — |
| 23 | TRA | BCG | BCG-2504-789B | 150 | S | S | S | S | S | S | S | S | S | — |
| 24 | ING | INFL | INFL-2504-261K | 20 | S | S | S | S | S | S | S | S | S | — |
| 25 | AJU | VARI | VARI-2509-637K | 40 | S | S | S | S | S | S | S | S | S | — |
| 26 | TRA | BCG | BCG-2606-808K | 100 | S | S | S | S | S | S | S | S | S | — |
| 27 | SAL | IPV | IPV-2605-698M | 180 | S | S | S | S | S | S | S | S | S | — |
| 28 | SAL | VARI | VARI-2508-818M | 80 | S | S | S | S | S | S | S | S | S | — |
| 29 | DEV | NEUM | NEUM-2505-638K | 40 | S | S | S | S | S | S | S | S | S | — |
| 30 | DEV | BCG | BCG-2607-654A | 50 | S | S | S | S | S | S | S | S | S | — |
| 31 | TRA | PENT | PENT-2504-482M | 300 | S | S | S | N | S | S | S | N | N | M4+M8 |
| 32 | ING | PENT | PENT-2606-391A | 300 | S | S | S | S | S | S | S | S | S | — |
| 33 | DEV | DTA | DTA-2602-236K | 40 | S | S | S | S | S | S | S | S | S | — |
| 34 | SAL | INFL | INFL-2604-777M | 30 | S | S | S | S | S | S | S | S | S | — |
| 35 | ING | DTA | DTA-2602-797A | 100 | S | S | S | S | S | S | S | N | N | M8 |
| 36 | SAL | PENT | PENT-2606-391A | 20 | S | S | S | S | S | S | S | S | S | — |
| 37 | TRA | PENT | PENT-2508-232M | 300 | S | S | S | S | S | S | S | S | S | — |
| 38 | SAL | BCG | BCG-2607-654A | 150 | S | S | S | S | S | S | S | S | S | — |
| 39 | SAL | SPR | SPR-2603-471K | 20 | S | S | S | S | S | S | S | S | S | — |
| 40 | AJU | NEUM | NEUM-2505-638K | 300 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-11 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 27/09/2026 | 4167 | SPR | 30 | 20 | -10 | GR-4167-8318 | No |
| 2 | 18/10/2026 | 4167 | DTA | 30 | 30 | 0 | GR-4167-5445 | Sí |
| 3 | 11/10/2026 | 4167 | ROTA | 80 | 80 | 0 | GR-4167-4397 | Sí |
| 4 | 11/10/2026 | 4167 | PENT | 180 | 180 | 0 | GR-4167-5105 | Sí |
| 5 | 10/10/2026 | 4167 | VARI | 50 | 50 | 0 | GR-4167-2083 | Sí |
| 6 | 29/09/2026 | 4167 | HEPB | 50 | 50 | 0 | GR-4167-6731 | Sí |
| 7 | 24/09/2026 | 4167 | HEPB | 180 | 180 | 0 | GR-4167-7974 | Sí |
| 8 | 22/09/2026 | 4167 | HEPB | 60 | 60 | 0 | GR-4167-5938 | Sí |
| 9 | 29/09/2026 | 4167 | DTA | 60 | 60 | 0 | GR-4167-6730 | Sí |
| 10 | 23/09/2026 | 4167 | PENT | 200 | 200 | 0 | GR-4167-2959 | Sí |
| 11 | 08/10/2026 | 4167 | SPR | 180 | 180 | 0 | GR-4167-2494 | Sí |
| 12 | 25/09/2026 | 4167 | ROTA | 40 | 40 | 0 | GR-4167-3307 | Sí |
| 13 | 11/10/2026 | 4167 | DTA | 150 | 150 | 0 | GR-4167-9209 | Sí |
| 14 | 01/10/2026 | 4167 | IPV | 30 | 30 | 0 | GR-4167-6528 | Sí |
| 15 | 05/10/2026 | 4167 | SPR | 60 | 60 | 0 | GR-4167-1406 | Sí |
| 16 | 18/10/2026 | 4167 | ROTA | 100 | 100 | 0 | GR-4167-6920 | Sí |
| 17 | 15/10/2026 | 4167 | DTA | 150 | 150 | 0 | GR-4167-6556 | Sí |
| 18 | 12/10/2026 | 4167 | VARI | 100 | 100 | 0 | GR-4167-5641 | Sí |
| 19 | 16/10/2026 | 4167 | IPV | 40 | 40 | 0 | GR-4167-7127 | Sí |
| 20 | 23/09/2026 | 4167 | PENT | 30 | 30 | 0 | GR-4167-7629 | Sí |
| 21 | 13/10/2026 | 4167 | IPV | 100 | 100 | 0 | GR-4167-9342 | Sí |
| 22 | 17/10/2026 | 4167 | ROTA | 50 | 70 | 20 | GR-4167-1862 | No |
| 23 | 04/10/2026 | 4167 | SPR | 100 | 100 | 0 | GR-4167-1745 | Sí |
| 24 | 17/10/2026 | 4167 | IPV | 80 | 80 | 0 | GR-4167-1648 | Sí |
| 25 | 09/10/2026 | 4167 | PENT | 50 | 50 | 0 | GR-4167-3398 | Sí |

Cierre: 23 entregas concordantes ÷ 25 × 100 = **92.00 %**.

---

### Bloque 23 · TRAB-12 · Pretest (proceso manual) · 07/09/2026

Documentos auditados: 40 · Conformes: 23 · RSD: 57.50 % · Entregas conciliadas: 25 · Concordantes: 15 · CPE: 60.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | TRA | DTA | DTA-2602-797A | 120 | S | S | S | S | S | S | S | S | S | — |
| 2 | ING | DTA | DTA-2602-797A | 300 | S | S | S | S | S | S | S | S | S | — |
| 3 | SAL | SPR | SPR-2504-185M | 60 | S | S | S | S | N | S | S | S | N | M5 |
| 4 | TRA | ROTA | ROTA-2605-833M | 20 | S | N | N | S | S | S | S | S | N | M2+M3 |
| 5 | ING | ROTA | ROTA-2605-833M | 50 | S | S | S | S | S | S | S | S | S | — |
| 6 | ING | SPR | SPR-2504-185M | 200 | S | N | S | S | S | S | N | S | N | M2+M7 |
| 7 | ING | DTA | DTA-2505-409K | 200 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | BCG | BCG-2606-296K | 100 | S | S | S | S | S | S | S | S | S | — |
| 9 | ING | VARI | VARI-2501-250M | 200 | S | S | S | S | S | S | N | S | N | M7 |
| 10 | SAL | PENT | PENT-2504-482M | 40 | S | S | S | S | S | S | S | S | S | — |
| 11 | SAL | VARI | VARI-2508-818M | 80 | S | S | S | S | N | S | S | S | N | M5 |
| 12 | DEV | NEUM | NEUM-2507-181K | 60 | S | S | S | S | S | S | S | S | S | — |
| 13 | ING | DTA | DTA-2606-829K | 120 | S | S | S | S | S | S | S | S | S | — |
| 14 | TRA | ROTA | ROTA-2603-156K | 80 | S | S | S | S | S | S | S | S | S | — |
| 15 | TRA | DTA | DTA-2505-409K | 150 | S | S | S | S | S | S | S | N | N | M8 |
| 16 | ING | IPV | IPV-2507-805M | 300 | S | S | S | S | S | S | S | S | S | — |
| 17 | TRA | INFL | INFL-2604-777M | 100 | S | S | S | N | S | S | S | S | N | M4 |
| 18 | SAL | PENT | PENT-2606-251M | 120 | S | S | S | S | S | S | S | S | S | — |
| 19 | SAL | PENT | PENT-2605-322M | 40 | S | S | S | S | S | S | S | S | S | — |
| 20 | AJU | IPV | IPV-2608-446B | 20 | S | S | S | S | S | S | S | S | S | — |
| 21 | TRA | VARI | VARI-2501-250M | 300 | S | S | S | S | S | S | N | S | N | M7 |
| 22 | TRA | INFL | INFL-2504-261K | 300 | S | S | S | S | S | S | S | N | N | M8 |
| 23 | DEV | HEPB | HEPB-2509-474M | 150 | S | S | S | S | S | S | S | S | S | — |
| 24 | SAL | SPR | SPR-2603-471K | 20 | N | N | S | S | S | S | S | S | N | M1+M2 |
| 25 | SAL | HEPB | HEPB-2609-917M | 30 | S | S | S | S | S | S | S | S | S | — |
| 26 | DEV | ROTA | ROTA-2507-417A | 200 | S | S | S | S | N | S | S | S | N | M5 |
| 27 | ING | DTA | DTA-2505-409K | 150 | S | S | S | S | S | S | S | S | S | — |
| 28 | AJU | DTA | DTA-2606-829K | 50 | S | S | S | S | S | S | S | S | S | — |
| 29 | ING | NEUM | NEUM-2506-884B | 40 | S | S | S | S | S | N | S | S | N | M6 |
| 30 | AJU | BCG | BCG-2606-808K | 50 | S | S | S | S | S | S | S | S | S | — |
| 31 | TRA | VARI | VARI-2503-521A | 200 | S | S | S | S | S | S | N | S | N | M7 |
| 32 | SAL | PENT | PENT-2605-322M | 30 | S | S | S | S | S | S | S | S | S | — |
| 33 | DEV | SPR | SPR-2504-185M | 30 | S | S | S | S | S | S | S | S | S | — |
| 34 | TRA | HEPB | HEPB-2509-474M | 100 | S | S | S | S | S | N | S | S | N | M6 |
| 35 | SAL | VARI | VARI-2503-521A | 60 | S | S | S | S | S | S | N | S | N | M7 |
| 36 | SAL | PENT | PENT-2504-482M | 40 | S | S | S | S | S | S | S | S | S | — |
| 37 | AJU | VARI | VARI-2509-637K | 50 | S | S | S | S | N | S | S | S | N | M5 |
| 38 | TRA | ROTA | ROTA-2602-464A | 50 | S | S | S | S | N | N | S | S | N | M5+M6 |
| 39 | SAL | BCG | BCG-2607-654A | 120 | S | S | S | S | S | S | S | S | S | — |
| 40 | SAL | PENT | PENT-2508-232M | 200 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-12 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 18/08/2026 | 4160 | HEPB | 80 | 80 | 0 | GR-4160-9178 | Sí |
| 2 | 02/09/2026 | 4160 | ROTA | 100 | 100 | 0 | GR-4160-2390 | Sí |
| 3 | 31/08/2026 | 4160 | HEPB | 50 | 40 | -10 | Sin guía | No |
| 4 | 24/08/2026 | 4160 | NEUM | 50 | 50 | 0 | GR-4160-7766 | Sí |
| 5 | 01/09/2026 | 4160 | ROTA | 60 | 60 | 0 | GR-4160-2946 | Sí |
| 6 | 03/09/2026 | 4160 | IPV | 50 | 50 | 0 | GR-4160-4738 | Sí |
| 7 | 04/09/2026 | 4160 | BCG | 120 | 120 | 0 | GR-4160-3216 | Sí |
| 8 | 10/08/2026 | 4160 | NEUM | 50 | 50 | 0 | GR-4160-2793 | Sí |
| 9 | 16/08/2026 | 4160 | SPR | 40 | 40 | 0 | GR-4160-5778 | Sí |
| 10 | 30/08/2026 | 4160 | ROTA | 200 | 205 | 5 | Sin guía | No |
| 11 | 23/08/2026 | 4160 | NEUM | 60 | 60 | 0 | GR-4160-1903 | Sí |
| 12 | 14/08/2026 | 4160 | IPV | 20 | 20 | 0 | GR-4160-7159 | Sí |
| 13 | 19/08/2026 | 4160 | PENT | 80 | 90 | 10 | GR-4160-2370 | No |
| 14 | 18/08/2026 | 4160 | VARI | 180 | 180 | 0 | GR-4160-5412 | Sí |
| 15 | 21/08/2026 | 4160 | INFL | 20 | 25 | 5 | Sin guía | No |
| 16 | 25/08/2026 | 4160 | NEUM | 80 | 70 | -10 | GR-4160-7730 | No |
| 17 | 14/08/2026 | 4160 | HEPB | 100 | 105 | 5 | Sin guía | No |
| 18 | 17/08/2026 | 4160 | ROTA | 80 | 80 | 0 | GR-4160-9764 | Sí |
| 19 | 14/08/2026 | 4160 | HEPB | 50 | 40 | -10 | Sin guía | No |
| 20 | 25/08/2026 | 4160 | PENT | 50 | 40 | -10 | GR-4160-9463 | No |
| 21 | 25/08/2026 | 4160 | PENT | 20 | 20 | 0 | GR-4160-7681 | Sí |
| 22 | 22/08/2026 | 4160 | NEUM | 60 | 60 | 0 | GR-4160-1619 | Sí |
| 23 | 13/08/2026 | 4160 | PENT | 80 | 80 | 0 | GR-4160-1989 | Sí |
| 24 | 28/08/2026 | 4160 | ROTA | 120 | 140 | 20 | GR-4160-4715 | No |
| 25 | 06/09/2026 | 4160 | SPR | 80 | 85 | 5 | Sin guía | No |

Cierre: 15 entregas concordantes ÷ 25 × 100 = **60.00 %**.

---

### Bloque 24 · TRAB-12 · Postest (Sistema SIVAC) · 19/10/2026

Documentos auditados: 40 · Conformes: 39 · RSD: 97.50 % · Entregas conciliadas: 25 · Concordantes: 23 · CPE: 92.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | TRA | BCG | BCG-2507-694K | 200 | S | S | S | S | S | S | S | S | S | — |
| 2 | TRA | BCG | BCG-2606-296K | 150 | S | S | S | S | S | S | S | S | S | — |
| 3 | SAL | BCG | BCG-2607-654A | 100 | S | S | S | S | S | S | S | S | S | — |
| 4 | ING | DTA | DTA-2606-829K | 240 | S | S | S | S | S | S | S | S | S | — |
| 5 | ING | HEPB | HEPB-2609-521M | 80 | S | S | S | S | S | S | S | S | S | — |
| 6 | SAL | NEUM | NEUM-2506-884B | 200 | S | S | S | S | S | S | S | S | S | — |
| 7 | ING | HEPB | HEPB-2603-786K | 150 | S | S | S | N | S | S | N | S | N | M4+M7 |
| 8 | SAL | SPR | SPR-2608-539M | 100 | S | S | S | S | S | S | S | S | S | — |
| 9 | AJU | IPV | IPV-2605-698M | 60 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | PENT | PENT-2606-391A | 50 | S | S | S | S | S | S | S | S | S | — |
| 11 | SAL | BCG | BCG-2504-789B | 200 | S | S | S | S | S | S | S | S | S | — |
| 12 | ING | HEPB | HEPB-2509-474M | 150 | S | S | S | S | S | S | S | S | S | — |
| 13 | SAL | VARI | VARI-2501-250M | 20 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | SPR | SPR-2606-500M | 80 | S | S | S | S | S | S | S | S | S | — |
| 15 | ING | BCG | BCG-2507-694K | 20 | S | S | S | S | S | S | S | S | S | — |
| 16 | TRA | SPR | SPR-2606-500M | 150 | S | S | S | S | S | S | S | S | S | — |
| 17 | SAL | DTA | DTA-2602-797A | 50 | S | S | S | S | S | S | S | S | S | — |
| 18 | ING | INFL | INFL-2603-792B | 80 | S | S | S | S | S | S | S | S | S | — |
| 19 | ING | INFL | INFL-2504-261K | 120 | S | S | S | S | S | S | S | S | S | — |
| 20 | AJU | ROTA | ROTA-2602-464A | 100 | S | S | S | S | S | S | S | S | S | — |
| 21 | TRA | PENT | PENT-2504-482M | 150 | S | S | S | S | S | S | S | S | S | — |
| 22 | AJU | PENT | PENT-2606-251M | 240 | S | S | S | S | S | S | S | S | S | — |
| 23 | ING | INFL | INFL-2504-261K | 100 | S | S | S | S | S | S | S | S | S | — |
| 24 | ING | ROTA | ROTA-2507-417A | 60 | S | S | S | S | S | S | S | S | S | — |
| 25 | SAL | DTA | DTA-2602-236K | 30 | S | S | S | S | S | S | S | S | S | — |
| 26 | ING | PENT | PENT-2504-482M | 40 | S | S | S | S | S | S | S | S | S | — |
| 27 | AJU | BCG | BCG-2607-654A | 60 | S | S | S | S | S | S | S | S | S | — |
| 28 | SAL | HEPB | HEPB-2509-474M | 150 | S | S | S | S | S | S | S | S | S | — |
| 29 | TRA | INFL | INFL-2603-792B | 180 | S | S | S | S | S | S | S | S | S | — |
| 30 | SAL | INFL | INFL-2508-359M | 300 | S | S | S | S | S | S | S | S | S | — |
| 31 | DEV | NEUM | NEUM-2505-638K | 100 | S | S | S | S | S | S | S | S | S | — |
| 32 | SAL | DTA | DTA-2602-797A | 300 | S | S | S | S | S | S | S | S | S | — |
| 33 | ING | SPR | SPR-2504-185M | 180 | S | S | S | S | S | S | S | S | S | — |
| 34 | AJU | NEUM | NEUM-2509-952A | 60 | S | S | S | S | S | S | S | S | S | — |
| 35 | AJU | NEUM | NEUM-2505-688A | 300 | S | S | S | S | S | S | S | S | S | — |
| 36 | TRA | SPR | SPR-2504-185M | 200 | S | S | S | S | S | S | S | S | S | — |
| 37 | ING | ROTA | ROTA-2507-417A | 100 | S | S | S | S | S | S | S | S | S | — |
| 38 | ING | ROTA | ROTA-2507-417A | 30 | S | S | S | S | S | S | S | S | S | — |
| 39 | SAL | NEUM | NEUM-2509-952A | 30 | S | S | S | S | S | S | S | S | S | — |
| 40 | SAL | NEUM | NEUM-2509-952A | 240 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-12 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 06/10/2026 | 4160 | PENT | 120 | 120 | 0 | GR-4160-1801 | Sí |
| 2 | 26/09/2026 | 4160 | SPR | 180 | 180 | 0 | GR-4160-3137 | Sí |
| 3 | 13/10/2026 | 4160 | ROTA | 150 | 150 | 0 | GR-4160-1641 | Sí |
| 4 | 22/09/2026 | 4160 | INFL | 200 | 200 | 0 | GR-4160-8194 | Sí |
| 5 | 04/10/2026 | 4160 | SPR | 100 | 100 | 0 | GR-4160-3844 | Sí |
| 6 | 10/10/2026 | 4160 | HEPB | 200 | 200 | 0 | GR-4160-9702 | Sí |
| 7 | 04/10/2026 | 4160 | IPV | 30 | 30 | 0 | GR-4160-2073 | Sí |
| 8 | 12/10/2026 | 4160 | PENT | 180 | 180 | 0 | GR-4160-2362 | Sí |
| 9 | 10/10/2026 | 4160 | INFL | 120 | 120 | 0 | GR-4160-8511 | Sí |
| 10 | 12/10/2026 | 4160 | PENT | 30 | 30 | 0 | GR-4160-2770 | Sí |
| 11 | 26/09/2026 | 4160 | VARI | 80 | 80 | 0 | GR-4160-4872 | Sí |
| 12 | 04/10/2026 | 4160 | NEUM | 20 | 10 | -10 | GR-4160-8865 | No |
| 13 | 16/10/2026 | 4160 | NEUM | 30 | 20 | -10 | GR-4160-8470 | No |
| 14 | 21/09/2026 | 4160 | HEPB | 200 | 200 | 0 | GR-4160-1638 | Sí |
| 15 | 03/10/2026 | 4160 | DTA | 50 | 50 | 0 | GR-4160-5542 | Sí |
| 16 | 09/10/2026 | 4160 | DTA | 40 | 40 | 0 | GR-4160-7068 | Sí |
| 17 | 12/10/2026 | 4160 | NEUM | 120 | 120 | 0 | GR-4160-5263 | Sí |
| 18 | 07/10/2026 | 4160 | VARI | 50 | 50 | 0 | GR-4160-8633 | Sí |
| 19 | 05/10/2026 | 4160 | DTA | 120 | 120 | 0 | GR-4160-1362 | Sí |
| 20 | 18/10/2026 | 4160 | SPR | 30 | 30 | 0 | GR-4160-7352 | Sí |
| 21 | 21/09/2026 | 4160 | HEPB | 50 | 50 | 0 | GR-4160-1877 | Sí |
| 22 | 04/10/2026 | 4160 | PENT | 100 | 100 | 0 | GR-4160-1575 | Sí |
| 23 | 18/10/2026 | 4160 | NEUM | 120 | 120 | 0 | GR-4160-3586 | Sí |
| 24 | 05/10/2026 | 4160 | HEPB | 180 | 180 | 0 | GR-4160-1533 | Sí |
| 25 | 28/09/2026 | 4160 | INFL | 100 | 100 | 0 | GR-4160-9524 | Sí |

Cierre: 23 entregas concordantes ÷ 25 × 100 = **92.00 %**.

---

### Bloque 25 · TRAB-13 · Pretest (proceso manual) · 08/09/2026

Documentos auditados: 40 · Conformes: 27 · RSD: 67.50 % · Entregas conciliadas: 25 · Concordantes: 18 · CPE: 72.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | SAL | ROTA | ROTA-2603-156K | 20 | S | S | S | S | S | S | N | S | N | M7 |
| 2 | ING | INFL | INFL-2504-261K | 30 | S | S | S | S | S | S | S | N | N | M8 |
| 3 | AJU | HEPB | HEPB-2609-917M | 80 | S | N | S | S | S | N | S | S | N | M2+M6 |
| 4 | DEV | HEPB | HEPB-2609-521M | 300 | S | S | N | S | S | N | S | S | N | M3+M6 |
| 5 | SAL | INFL | INFL-2504-261K | 240 | S | S | S | S | S | S | S | S | S | — |
| 6 | ING | BCG | BCG-2606-296K | 150 | S | S | S | S | S | S | S | S | S | — |
| 7 | ING | HEPB | HEPB-2602-318M | 180 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | ROTA | ROTA-2502-563B | 180 | S | S | S | S | S | S | S | S | S | — |
| 9 | TRA | HEPB | HEPB-2603-786K | 200 | S | N | S | S | S | S | S | S | N | M2 |
| 10 | SAL | ROTA | ROTA-2602-464A | 40 | S | S | S | S | S | S | S | S | S | — |
| 11 | SAL | SPR | SPR-2504-185M | 20 | S | N | S | S | S | S | S | S | N | M2 |
| 12 | SAL | IPV | IPV-2605-698M | 20 | S | S | S | S | S | S | S | S | S | — |
| 13 | ING | INFL | INFL-2604-777M | 30 | S | S | S | S | S | S | S | S | S | — |
| 14 | TRA | HEPB | HEPB-2603-786K | 50 | S | S | S | S | S | S | S | S | S | — |
| 15 | SAL | DTA | DTA-2505-409K | 120 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | IPV | IPV-2605-698M | 240 | S | S | S | S | S | S | S | N | N | M8 |
| 17 | TRA | NEUM | NEUM-2506-884B | 120 | S | S | S | S | S | S | S | S | S | — |
| 18 | TRA | PENT | PENT-2605-322M | 120 | S | S | S | S | S | S | S | S | S | — |
| 19 | DEV | ROTA | ROTA-2602-464A | 240 | S | S | S | S | S | S | S | S | S | — |
| 20 | DEV | IPV | IPV-2507-805M | 50 | S | S | S | S | N | S | S | S | N | M5 |
| 21 | TRA | IPV | IPV-2608-446B | 50 | S | N | S | S | S | S | S | S | N | M2 |
| 22 | DEV | NEUM | NEUM-2509-952A | 40 | S | S | S | S | S | S | S | S | S | — |
| 23 | ING | SPR | SPR-2504-185M | 60 | S | S | S | S | S | N | S | N | N | M6+M8 |
| 24 | ING | SPR | SPR-2603-471K | 60 | S | S | S | S | S | S | S | S | S | — |
| 25 | ING | HEPB | HEPB-2609-521M | 300 | S | S | S | S | S | S | S | S | S | — |
| 26 | TRA | PENT | PENT-2504-482M | 20 | S | S | S | S | S | N | S | S | N | M6 |
| 27 | ING | BCG | BCG-2606-808K | 30 | S | S | S | S | S | S | S | S | S | — |
| 28 | ING | PENT | PENT-2606-251M | 50 | S | S | S | S | S | S | S | S | S | — |
| 29 | DEV | SPR | SPR-2609-423M | 40 | S | S | S | S | S | S | S | S | S | — |
| 30 | ING | VARI | VARI-2501-250M | 100 | S | S | S | S | S | S | S | S | S | — |
| 31 | ING | VARI | VARI-2501-250M | 120 | S | S | S | S | S | S | S | S | S | — |
| 32 | ING | BCG | BCG-2507-694K | 240 | S | S | S | S | S | S | S | S | S | — |
| 33 | TRA | HEPB | HEPB-2609-521M | 20 | S | S | S | S | S | S | S | S | S | — |
| 34 | TRA | VARI | VARI-2503-521A | 200 | S | S | S | S | S | S | S | S | S | — |
| 35 | ING | SPR | SPR-2603-471K | 200 | S | S | S | S | S | S | S | S | S | — |
| 36 | DEV | INFL | INFL-2607-737M | 50 | S | S | N | S | S | S | S | S | N | M3 |
| 37 | SAL | INFL | INFL-2504-261K | 40 | S | S | S | S | S | S | S | S | S | — |
| 38 | SAL | NEUM | NEUM-2505-638K | 80 | S | S | S | S | S | S | S | S | S | — |
| 39 | SAL | HEPB | HEPB-2609-521M | 30 | S | S | S | S | S | S | S | S | S | — |
| 40 | DEV | DTA | DTA-2602-797A | 40 | S | S | S | N | S | S | S | S | N | M4 |

**Entregas conciliadas — TRAB-13 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 12/08/2026 | 4163 | BCG | 50 | 50 | 0 | GR-4163-9132 | Sí |
| 2 | 31/08/2026 | 4163 | ROTA | 100 | 100 | 0 | GR-4163-6974 | Sí |
| 3 | 03/09/2026 | 4163 | HEPB | 20 | 20 | 0 | GR-4163-5401 | Sí |
| 4 | 18/08/2026 | 4163 | NEUM | 20 | 10 | -10 | Sin guía | No |
| 5 | 27/08/2026 | 4163 | BCG | 20 | 20 | 0 | GR-4163-8127 | Sí |
| 6 | 28/08/2026 | 4163 | PENT | 60 | 60 | 0 | GR-4163-6052 | Sí |
| 7 | 07/09/2026 | 4163 | BCG | 30 | 30 | 0 | GR-4163-4840 | Sí |
| 8 | 14/08/2026 | 4163 | NEUM | 20 | 20 | 0 | GR-4163-1259 | Sí |
| 9 | 05/09/2026 | 4163 | PENT | 120 | 120 | 0 | GR-4163-7651 | Sí |
| 10 | 06/09/2026 | 4163 | VARI | 120 | 120 | 0 | GR-4163-8157 | Sí |
| 11 | 14/08/2026 | 4163 | IPV | 120 | 120 | 0 | GR-4163-1996 | Sí |
| 12 | 30/08/2026 | 4163 | PENT | 150 | 145 | -5 | GR-4163-4796 | No |
| 13 | 05/09/2026 | 4163 | NEUM | 120 | 110 | -10 | Sin guía | No |
| 14 | 01/09/2026 | 4163 | IPV | 60 | 60 | 0 | GR-4163-5087 | Sí |
| 15 | 18/08/2026 | 4163 | ROTA | 180 | 180 | 0 | GR-4163-4469 | Sí |
| 16 | 19/08/2026 | 4163 | SPR | 30 | 30 | 0 | GR-4163-8352 | Sí |
| 17 | 18/08/2026 | 4163 | ROTA | 30 | 30 | 0 | GR-4163-2691 | Sí |
| 18 | 12/08/2026 | 4163 | BCG | 30 | 20 | -10 | Sin guía | No |
| 19 | 22/08/2026 | 4163 | IPV | 100 | 100 | 0 | GR-4163-7524 | Sí |
| 20 | 20/08/2026 | 4163 | INFL | 50 | 50 | 0 | GR-4163-6847 | Sí |
| 21 | 02/09/2026 | 4163 | HEPB | 50 | 50 | 0 | GR-4163-8615 | Sí |
| 22 | 03/09/2026 | 4163 | INFL | 180 | 160 | -20 | GR-4163-7804 | No |
| 23 | 31/08/2026 | 4163 | NEUM | 30 | 25 | -5 | GR-4163-3048 | No |
| 24 | 06/09/2026 | 4163 | VARI | 120 | 115 | -5 | GR-4163-3182 | No |
| 25 | 20/08/2026 | 4163 | SPR | 30 | 30 | 0 | GR-4163-6393 | Sí |

Cierre: 18 entregas concordantes ÷ 25 × 100 = **72.00 %**.

---

### Bloque 26 · TRAB-13 · Postest (Sistema SIVAC) · 20/10/2026

Documentos auditados: 40 · Conformes: 37 · RSD: 92.50 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | SAL | PENT | PENT-2606-251M | 100 | S | S | S | S | S | S | S | S | S | — |
| 2 | SAL | INFL | INFL-2604-777M | 50 | S | S | S | S | S | S | S | S | S | — |
| 3 | ING | VARI | VARI-2607-979A | 80 | S | S | S | S | S | S | S | S | S | — |
| 4 | AJU | VARI | VARI-2503-521A | 30 | S | S | S | S | S | S | S | S | S | — |
| 5 | SAL | VARI | VARI-2509-637K | 150 | S | S | S | S | S | S | S | S | S | — |
| 6 | DEV | DTA | DTA-2603-463K | 100 | S | S | S | S | S | S | S | S | S | — |
| 7 | TRA | NEUM | NEUM-2507-181K | 60 | S | S | S | S | S | S | N | N | N | M7+M8 |
| 8 | ING | INFL | INFL-2508-359M | 120 | S | S | S | S | S | S | S | S | S | — |
| 9 | SAL | NEUM | NEUM-2509-952A | 180 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | HEPB | HEPB-2609-521M | 120 | S | S | S | S | S | S | S | S | S | — |
| 11 | ING | INFL | INFL-2607-737M | 180 | S | S | S | S | S | S | S | S | S | — |
| 12 | ING | IPV | IPV-2504-587B | 50 | S | S | S | S | S | S | S | S | S | — |
| 13 | SAL | DTA | DTA-2602-797A | 200 | S | S | S | S | S | S | S | S | S | — |
| 14 | DEV | IPV | IPV-2608-446B | 240 | S | S | S | S | S | S | S | S | S | — |
| 15 | TRA | VARI | VARI-2509-637K | 40 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | VARI | VARI-2501-250M | 40 | S | S | S | S | S | S | S | S | S | — |
| 17 | ING | PENT | PENT-2606-391A | 180 | S | S | S | S | S | S | S | S | S | — |
| 18 | ING | ROTA | ROTA-2602-464A | 60 | S | S | S | S | S | S | S | S | S | — |
| 19 | TRA | VARI | VARI-2508-818M | 40 | S | S | S | S | S | S | S | S | S | — |
| 20 | SAL | PENT | PENT-2508-232M | 300 | S | S | S | S | S | S | S | S | S | — |
| 21 | ING | IPV | IPV-2608-446B | 20 | S | S | S | S | S | S | S | S | S | — |
| 22 | AJU | SPR | SPR-2609-423M | 180 | S | S | S | S | S | S | S | S | S | — |
| 23 | TRA | ROTA | ROTA-2502-563B | 300 | S | S | S | S | S | S | S | S | S | — |
| 24 | TRA | VARI | VARI-2503-521A | 50 | S | S | S | S | S | S | S | S | S | — |
| 25 | SAL | BCG | BCG-2606-296K | 100 | S | S | S | S | S | S | S | S | S | — |
| 26 | SAL | VARI | VARI-2508-818M | 30 | S | S | S | S | S | S | S | S | S | — |
| 27 | ING | DTA | DTA-2602-797A | 20 | S | S | S | S | N | S | S | S | N | M5 |
| 28 | SAL | VARI | VARI-2503-521A | 150 | S | S | S | S | S | S | S | S | S | — |
| 29 | ING | IPV | IPV-2504-587B | 20 | S | S | S | S | S | S | S | S | S | — |
| 30 | SAL | ROTA | ROTA-2507-417A | 300 | S | S | S | S | S | S | S | S | S | — |
| 31 | SAL | NEUM | NEUM-2509-952A | 100 | S | S | S | S | S | N | S | S | N | M6 |
| 32 | DEV | INFL | INFL-2607-737M | 40 | S | S | S | S | S | S | S | S | S | — |
| 33 | SAL | NEUM | NEUM-2509-952A | 100 | S | S | S | S | S | S | S | S | S | — |
| 34 | TRA | PENT | PENT-2605-322M | 100 | S | S | S | S | S | S | S | S | S | — |
| 35 | SAL | ROTA | ROTA-2605-833M | 240 | S | S | S | S | S | S | S | S | S | — |
| 36 | ING | NEUM | NEUM-2505-638K | 80 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | HEPB | HEPB-2509-474M | 150 | S | S | S | S | S | S | S | S | S | — |
| 38 | ING | INFL | INFL-2603-792B | 80 | S | S | S | S | S | S | S | S | S | — |
| 39 | AJU | HEPB | HEPB-2603-786K | 200 | S | S | S | S | S | S | S | S | S | — |
| 40 | TRA | ROTA | ROTA-2502-563B | 60 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-13 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 19/10/2026 | 4163 | INFL | 150 | 150 | 0 | GR-4163-3354 | Sí |
| 2 | 11/10/2026 | 4163 | PENT | 20 | 20 | 0 | GR-4163-5739 | Sí |
| 3 | 19/10/2026 | 4163 | NEUM | 40 | 40 | 0 | GR-4163-6709 | Sí |
| 4 | 12/10/2026 | 4163 | INFL | 50 | 50 | 0 | GR-4163-9658 | Sí |
| 5 | 23/09/2026 | 4163 | IPV | 120 | 120 | 0 | GR-4163-2626 | Sí |
| 6 | 19/10/2026 | 4163 | VARI | 150 | 150 | 0 | GR-4163-1571 | Sí |
| 7 | 08/10/2026 | 4163 | INFL | 150 | 150 | 0 | GR-4163-3678 | Sí |
| 8 | 18/10/2026 | 4163 | SPR | 50 | 50 | 0 | GR-4163-2222 | Sí |
| 9 | 05/10/2026 | 4163 | NEUM | 20 | 20 | 0 | GR-4163-5226 | Sí |
| 10 | 09/10/2026 | 4163 | VARI | 40 | 40 | 0 | GR-4163-5460 | Sí |
| 11 | 23/09/2026 | 4163 | SPR | 180 | 180 | 0 | GR-4163-5181 | Sí |
| 12 | 14/10/2026 | 4163 | DTA | 80 | 80 | 0 | GR-4163-6672 | Sí |
| 13 | 08/10/2026 | 4163 | DTA | 80 | 80 | 0 | GR-4163-1318 | Sí |
| 14 | 27/09/2026 | 4163 | BCG | 60 | 60 | 0 | GR-4163-7936 | Sí |
| 15 | 30/09/2026 | 4163 | DTA | 200 | 200 | 0 | GR-4163-1619 | Sí |
| 16 | 07/10/2026 | 4163 | BCG | 100 | 100 | 0 | GR-4163-5934 | Sí |
| 17 | 17/10/2026 | 4163 | NEUM | 150 | 150 | 0 | GR-4163-5876 | Sí |
| 18 | 22/09/2026 | 4163 | DTA | 50 | 40 | -10 | GR-4163-2795 | No |
| 19 | 13/10/2026 | 4163 | SPR | 200 | 200 | 0 | GR-4163-8804 | Sí |
| 20 | 02/10/2026 | 4163 | IPV | 200 | 200 | 0 | GR-4163-8175 | Sí |
| 21 | 11/10/2026 | 4163 | VARI | 60 | 60 | 0 | GR-4163-8672 | Sí |
| 22 | 22/09/2026 | 4163 | BCG | 120 | 120 | 0 | GR-4163-3258 | Sí |
| 23 | 12/10/2026 | 4163 | NEUM | 200 | 200 | 0 | GR-4163-6158 | Sí |
| 24 | 30/09/2026 | 4163 | HEPB | 100 | 100 | 0 | GR-4163-7287 | Sí |
| 25 | 29/09/2026 | 4163 | PENT | 120 | 120 | 0 | GR-4163-8313 | Sí |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 27 · TRAB-14 · Pretest (proceso manual) · 08/09/2026

Documentos auditados: 40 · Conformes: 26 · RSD: 65.00 % · Entregas conciliadas: 25 · Concordantes: 17 · CPE: 68.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | TRA | SPR | SPR-2608-539M | 60 | S | S | S | S | N | S | N | S | N | M5+M7 |
| 2 | SAL | NEUM | NEUM-2505-638K | 60 | S | N | S | S | S | S | S | S | N | M2 |
| 3 | SAL | ROTA | ROTA-2507-417A | 150 | S | S | S | S | S | S | S | S | S | — |
| 4 | SAL | IPV | IPV-2605-698M | 240 | S | S | S | S | S | S | S | S | S | — |
| 5 | SAL | BCG | BCG-2504-789B | 180 | S | N | S | S | S | S | S | S | N | M2 |
| 6 | ING | IPV | IPV-2608-446B | 200 | S | S | S | S | S | S | S | S | S | — |
| 7 | ING | IPV | IPV-2605-698M | 300 | S | S | N | S | S | N | S | S | N | M3+M6 |
| 8 | SAL | HEPB | HEPB-2609-917M | 20 | S | S | S | S | S | S | S | S | S | — |
| 9 | TRA | IPV | IPV-2507-805M | 120 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | NEUM | NEUM-2506-884B | 240 | S | S | S | S | S | S | S | N | N | M8 |
| 11 | SAL | NEUM | NEUM-2505-688A | 150 | S | S | S | S | S | S | S | S | S | — |
| 12 | SAL | IPV | IPV-2507-805M | 80 | S | S | S | S | S | S | S | S | S | — |
| 13 | AJU | INFL | INFL-2603-792B | 50 | S | S | S | S | S | S | S | S | S | — |
| 14 | AJU | NEUM | NEUM-2505-638K | 60 | S | S | S | S | S | S | N | S | N | M7 |
| 15 | ING | PENT | PENT-2508-232M | 180 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | PENT | PENT-2606-251M | 40 | S | S | S | S | S | S | S | S | S | — |
| 17 | SAL | HEPB | HEPB-2509-474M | 60 | S | S | S | S | S | N | S | S | N | M6 |
| 18 | SAL | NEUM | NEUM-2505-638K | 300 | S | S | S | S | S | S | S | S | S | — |
| 19 | DEV | ROTA | ROTA-2603-156K | 180 | S | S | S | S | S | S | S | S | S | — |
| 20 | SAL | ROTA | ROTA-2507-417A | 80 | S | S | S | N | S | S | S | S | N | M4 |
| 21 | SAL | SPR | SPR-2606-500M | 50 | S | S | S | S | S | S | S | S | S | — |
| 22 | SAL | VARI | VARI-2501-250M | 40 | S | S | S | S | S | S | S | S | S | — |
| 23 | TRA | NEUM | NEUM-2507-181K | 120 | S | S | S | S | S | S | S | S | S | — |
| 24 | DEV | DTA | DTA-2606-829K | 20 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | DTA | DTA-2505-409K | 150 | S | S | S | S | S | S | S | S | S | — |
| 26 | TRA | INFL | INFL-2604-777M | 300 | S | S | S | S | S | S | S | S | S | — |
| 27 | SAL | HEPB | HEPB-2609-521M | 20 | S | S | S | S | S | S | S | S | S | — |
| 28 | DEV | PENT | PENT-2605-322M | 240 | S | S | S | S | S | S | S | N | N | M8 |
| 29 | ING | NEUM | NEUM-2505-638K | 50 | S | S | S | S | S | S | S | S | S | — |
| 30 | SAL | NEUM | NEUM-2505-638K | 120 | S | S | S | N | S | S | S | S | N | M4 |
| 31 | TRA | BCG | BCG-2606-296K | 180 | S | S | S | S | S | S | S | S | S | — |
| 32 | SAL | NEUM | NEUM-2507-181K | 120 | S | S | S | S | S | S | S | S | S | — |
| 33 | TRA | IPV | IPV-2504-587B | 50 | S | S | S | S | S | S | S | S | S | — |
| 34 | SAL | INFL | INFL-2604-777M | 20 | N | S | S | S | S | S | N | S | N | M1+M7 |
| 35 | TRA | PENT | PENT-2605-322M | 80 | S | S | S | S | S | S | S | S | S | — |
| 36 | ING | VARI | VARI-2607-979A | 240 | S | S | S | S | S | S | S | N | N | M8 |
| 37 | SAL | HEPB | HEPB-2509-474M | 50 | S | S | S | S | S | S | N | S | N | M7 |
| 38 | TRA | INFL | INFL-2607-737M | 150 | S | S | S | S | S | S | S | S | S | — |
| 39 | SAL | ROTA | ROTA-2603-156K | 60 | S | S | S | S | S | N | S | S | N | M6 |
| 40 | SAL | PENT | PENT-2605-322M | 300 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-14 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 07/09/2026 | 4183 | HEPB | 200 | 190 | -10 | Sin guía | No |
| 2 | 21/08/2026 | 4183 | BCG | 80 | 80 | 0 | GR-4183-1691 | Sí |
| 3 | 05/09/2026 | 4183 | HEPB | 120 | 120 | 0 | GR-4183-4491 | Sí |
| 4 | 07/09/2026 | 4183 | VARI | 150 | 155 | 5 | GR-4183-3005 | No |
| 5 | 29/08/2026 | 4183 | SPR | 120 | 120 | 0 | GR-4183-1592 | Sí |
| 6 | 25/08/2026 | 4183 | INFL | 100 | 100 | 0 | GR-4183-5251 | Sí |
| 7 | 31/08/2026 | 4183 | ROTA | 180 | 180 | 0 | GR-4183-1372 | Sí |
| 8 | 27/08/2026 | 4183 | DTA | 80 | 80 | 0 | GR-4183-4331 | Sí |
| 9 | 03/09/2026 | 4183 | IPV | 150 | 150 | 0 | GR-4183-3907 | Sí |
| 10 | 21/08/2026 | 4183 | IPV | 40 | 40 | 0 | GR-4183-1718 | Sí |
| 11 | 16/08/2026 | 4183 | IPV | 150 | 160 | 10 | GR-4183-6681 | No |
| 12 | 21/08/2026 | 4183 | PENT | 120 | 120 | 0 | GR-4183-2184 | Sí |
| 13 | 30/08/2026 | 4183 | PENT | 200 | 200 | 0 | GR-4183-2923 | Sí |
| 14 | 27/08/2026 | 4183 | INFL | 80 | 75 | -5 | GR-4183-2121 | No |
| 15 | 11/08/2026 | 4183 | DTA | 200 | 200 | 0 | GR-4183-2813 | Sí |
| 16 | 19/08/2026 | 4183 | BCG | 40 | 50 | 10 | GR-4183-2919 | No |
| 17 | 23/08/2026 | 4183 | DTA | 50 | 50 | 0 | GR-4183-2556 | Sí |
| 18 | 22/08/2026 | 4183 | BCG | 80 | 85 | 5 | Sin guía | No |
| 19 | 25/08/2026 | 4183 | BCG | 40 | 35 | -5 | Sin guía | No |
| 20 | 25/08/2026 | 4183 | SPR | 50 | 45 | -5 | GR-4183-5097 | No |
| 21 | 18/08/2026 | 4183 | DTA | 80 | 80 | 0 | GR-4183-2119 | Sí |
| 22 | 04/09/2026 | 4183 | PENT | 180 | 180 | 0 | GR-4183-8590 | Sí |
| 23 | 06/09/2026 | 4183 | PENT | 100 | 100 | 0 | GR-4183-8838 | Sí |
| 24 | 04/09/2026 | 4183 | PENT | 100 | 100 | 0 | GR-4183-9091 | Sí |
| 25 | 14/08/2026 | 4183 | HEPB | 200 | 200 | 0 | GR-4183-7406 | Sí |

Cierre: 17 entregas concordantes ÷ 25 × 100 = **68.00 %**.

---

### Bloque 28 · TRAB-14 · Postest (Sistema SIVAC) · 20/10/2026

Documentos auditados: 40 · Conformes: 39 · RSD: 97.50 % · Entregas conciliadas: 25 · Concordantes: 22 · CPE: 88.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | TRA | VARI | VARI-2607-979A | 240 | S | S | S | S | S | S | S | S | S | — |
| 2 | ING | SPR | SPR-2504-185M | 60 | S | S | S | S | S | S | S | S | S | — |
| 3 | SAL | ROTA | ROTA-2605-833M | 240 | S | S | S | S | S | S | S | S | S | — |
| 4 | ING | INFL | INFL-2508-359M | 150 | S | S | S | S | S | S | S | S | S | — |
| 5 | SAL | ROTA | ROTA-2605-833M | 20 | S | S | S | S | S | S | S | S | S | — |
| 6 | AJU | INFL | INFL-2607-737M | 150 | S | S | S | S | S | S | S | S | S | — |
| 7 | ING | PENT | PENT-2508-232M | 200 | S | S | S | S | S | S | S | S | S | — |
| 8 | TRA | INFL | INFL-2607-737M | 50 | S | S | S | S | S | S | S | S | S | — |
| 9 | SAL | VARI | VARI-2503-521A | 40 | S | S | S | S | S | S | S | S | S | — |
| 10 | TRA | BCG | BCG-2504-789B | 120 | S | S | S | S | S | S | S | S | S | — |
| 11 | ING | INFL | INFL-2604-777M | 30 | S | S | S | S | S | S | S | S | S | — |
| 12 | TRA | IPV | IPV-2605-698M | 200 | S | S | S | S | S | S | S | S | S | — |
| 13 | ING | ROTA | ROTA-2605-833M | 180 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | BCG | BCG-2606-808K | 60 | S | S | S | S | S | S | S | S | S | — |
| 15 | ING | INFL | INFL-2603-792B | 60 | S | S | S | S | S | S | S | S | S | — |
| 16 | ING | DTA | DTA-2606-829K | 100 | S | S | S | S | S | S | S | S | S | — |
| 17 | ING | IPV | IPV-2605-698M | 200 | S | S | S | S | S | S | S | S | S | — |
| 18 | SAL | PENT | PENT-2606-391A | 20 | S | S | S | S | S | S | S | S | S | — |
| 19 | SAL | DTA | DTA-2606-829K | 300 | S | S | N | S | N | S | S | S | N | M3+M5 |
| 20 | ING | ROTA | ROTA-2605-833M | 240 | S | S | S | S | S | S | S | S | S | — |
| 21 | ING | HEPB | HEPB-2609-917M | 60 | S | S | S | S | S | S | S | S | S | — |
| 22 | TRA | DTA | DTA-2602-797A | 80 | S | S | S | S | S | S | S | S | S | — |
| 23 | SAL | PENT | PENT-2606-391A | 40 | S | S | S | S | S | S | S | S | S | — |
| 24 | ING | INFL | INFL-2504-261K | 40 | S | S | S | S | S | S | S | S | S | — |
| 25 | SAL | IPV | IPV-2504-587B | 50 | S | S | S | S | S | S | S | S | S | — |
| 26 | SAL | IPV | IPV-2605-698M | 100 | S | S | S | S | S | S | S | S | S | — |
| 27 | SAL | IPV | IPV-2608-446B | 80 | S | S | S | S | S | S | S | S | S | — |
| 28 | ING | VARI | VARI-2501-250M | 300 | S | S | S | S | S | S | S | S | S | — |
| 29 | SAL | SPR | SPR-2504-185M | 150 | S | S | S | S | S | S | S | S | S | — |
| 30 | DEV | NEUM | NEUM-2505-688A | 60 | S | S | S | S | S | S | S | S | S | — |
| 31 | DEV | PENT | PENT-2606-391A | 180 | S | S | S | S | S | S | S | S | S | — |
| 32 | TRA | NEUM | NEUM-2506-884B | 300 | S | S | S | S | S | S | S | S | S | — |
| 33 | SAL | HEPB | HEPB-2603-786K | 150 | S | S | S | S | S | S | S | S | S | — |
| 34 | TRA | IPV | IPV-2504-587B | 20 | S | S | S | S | S | S | S | S | S | — |
| 35 | ING | VARI | VARI-2501-250M | 300 | S | S | S | S | S | S | S | S | S | — |
| 36 | AJU | NEUM | NEUM-2505-688A | 40 | S | S | S | S | S | S | S | S | S | — |
| 37 | ING | ROTA | ROTA-2602-464A | 40 | S | S | S | S | S | S | S | S | S | — |
| 38 | TRA | ROTA | ROTA-2502-563B | 40 | S | S | S | S | S | S | S | S | S | — |
| 39 | ING | NEUM | NEUM-2507-181K | 30 | S | S | S | S | S | S | S | S | S | — |
| 40 | SAL | HEPB | HEPB-2602-318M | 300 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-14 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 14/10/2026 | 4183 | HEPB | 200 | 200 | 0 | GR-4183-9345 | Sí |
| 2 | 09/10/2026 | 4183 | VARI | 40 | 40 | 0 | GR-4183-4671 | Sí |
| 3 | 18/10/2026 | 4183 | DTA | 100 | 100 | 0 | GR-4183-6432 | Sí |
| 4 | 19/10/2026 | 4183 | ROTA | 100 | 100 | 0 | GR-4183-7069 | Sí |
| 5 | 03/10/2026 | 4183 | NEUM | 80 | 80 | 0 | GR-4183-3440 | Sí |
| 6 | 30/09/2026 | 4183 | INFL | 60 | 60 | 0 | GR-4183-5238 | Sí |
| 7 | 12/10/2026 | 4183 | VARI | 100 | 90 | -10 | Sin guía | No |
| 8 | 24/09/2026 | 4183 | NEUM | 50 | 50 | 0 | GR-4183-7057 | Sí |
| 9 | 22/09/2026 | 4183 | ROTA | 80 | 80 | 0 | GR-4183-4203 | Sí |
| 10 | 14/10/2026 | 4183 | VARI | 20 | 20 | 0 | GR-4183-1455 | Sí |
| 11 | 18/10/2026 | 4183 | BCG | 20 | 20 | 0 | GR-4183-8572 | Sí |
| 12 | 17/10/2026 | 4183 | VARI | 50 | 50 | 0 | GR-4183-8253 | Sí |
| 13 | 06/10/2026 | 4183 | NEUM | 80 | 80 | 0 | GR-4183-4177 | Sí |
| 14 | 10/10/2026 | 4183 | ROTA | 100 | 100 | 0 | GR-4183-3469 | Sí |
| 15 | 13/10/2026 | 4183 | PENT | 80 | 80 | 0 | GR-4183-7930 | Sí |
| 16 | 12/10/2026 | 4183 | SPR | 120 | 120 | 0 | GR-4183-1912 | Sí |
| 17 | 05/10/2026 | 4183 | DTA | 180 | 175 | -5 | GR-4183-1698 | No |
| 18 | 05/10/2026 | 4183 | VARI | 200 | 200 | 0 | GR-4183-6930 | Sí |
| 19 | 16/10/2026 | 4183 | BCG | 150 | 150 | 0 | GR-4183-8080 | Sí |
| 20 | 09/10/2026 | 4183 | ROTA | 50 | 50 | 0 | GR-4183-8426 | Sí |
| 21 | 26/09/2026 | 4183 | VARI | 50 | 50 | 0 | GR-4183-9398 | Sí |
| 22 | 23/09/2026 | 4183 | BCG | 120 | 120 | 0 | GR-4183-5166 | Sí |
| 23 | 19/10/2026 | 4183 | HEPB | 100 | 110 | 10 | GR-4183-5502 | No |
| 24 | 01/10/2026 | 4183 | ROTA | 80 | 80 | 0 | GR-4183-5611 | Sí |
| 25 | 29/09/2026 | 4183 | SPR | 30 | 30 | 0 | GR-4183-2758 | Sí |

Cierre: 22 entregas concordantes ÷ 25 × 100 = **88.00 %**.

---

---

<a id="parte-5"></a>
## Parte 5. Instrumento 3 — Cuestionario de satisfacción del usuario (TAM)

La Modalidad A se administra en las dos fases y consta de ocho reactivos Likert de 1 a 5: cuatro miden aceptación del proceso y cuatro, utilidad percibida. Los enunciados se imprimen una sola vez por sección y la matriz consigna después la respuesta de cada unidad en cada fase.

### Enunciados de la Modalidad A

**Aceptación del proceso**

1. El procedimiento para registrar los movimientos diarios de vacunas se realiza de forma ágil.
2. El trámite para emitir comprobantes de salida y vales de entrega se efectúa sin demoras innecesarias.
3. El procedimiento utilizado facilita conciliar los saldos de vacunas entre el centro de acopio y los establecimientos de salud.
4. El tiempo destinado a gestionar los movimientos de vacunas es compatible con mis demás actividades laborales.

**Utilidad percibida**

5. Utilizar el sistema SIVAC agiliza notablemente el registro de entradas, salidas y transferencias de dosis de vacunas en mi centro.
6. SIVAC me permite consultar de manera inmediata y precisa los saldos de existencias por lote en cualquier momento que lo requiera.
7. La generación automática de vales oficiales en formato PDF en SIVAC facilita el despacho hacia los establecimientos de salud.
8. En conjunto, SIVAC incrementa mi productividad y mejora el control de la cadena de frío en mi jurisdicción.

### Matriz de respuestas — Modalidad A

| Sujeto | Fase | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | AP | UP | TAM | Nivel |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| TRAB-01 | Pretest | 2 | 2 | 2 | 2 | 2 | 3 | 2 | 2 | 8 | 9 | 17 | Bajo |
| TRAB-01 | Postest | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 20 | 20 | 40 | Alto |
| TRAB-02 | Pretest | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 6 | 8 | 14 | Bajo |
| TRAB-02 | Postest | 4 | 5 | 5 | 5 | 4 | 4 | 4 | 4 | 19 | 16 | 35 | Alto |
| TRAB-03 | Pretest | 2 | 2 | 3 | 2 | 3 | 2 | 2 | 3 | 9 | 10 | 19 | Medio |
| TRAB-03 | Postest | 4 | 4 | 5 | 4 | 4 | 5 | 5 | 4 | 17 | 18 | 35 | Alto |
| TRAB-04 | Pretest | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 11 | 12 | 23 | Medio |
| TRAB-04 | Postest | 4 | 4 | 5 | 5 | 4 | 4 | 5 | 4 | 18 | 17 | 35 | Alto |
| TRAB-05 | Pretest | 2 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 6 | 8 | 14 | Bajo |
| TRAB-05 | Postest | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 20 | 20 | 40 | Alto |
| TRAB-06 | Pretest | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 8 | 8 | 16 | Bajo |
| TRAB-06 | Postest | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 20 | 20 | 40 | Alto |
| TRAB-07 | Pretest | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 2 | 4 | 6 | 10 | Bajo |
| TRAB-07 | Postest | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 20 | 20 | 40 | Alto |
| TRAB-08 | Pretest | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 12 | 12 | 24 | Medio |
| TRAB-08 | Postest | 4 | 5 | 4 | 5 | 5 | 5 | 5 | 4 | 18 | 19 | 37 | Alto |
| TRAB-09 | Pretest | 3 | 2 | 3 | 2 | 3 | 3 | 2 | 3 | 10 | 11 | 21 | Medio |
| TRAB-09 | Postest | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 20 | 19 | 39 | Alto |
| TRAB-10 | Pretest | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 8 | 8 | 16 | Bajo |
| TRAB-10 | Postest | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 20 | 20 | 40 | Alto |
| TRAB-11 | Pretest | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 8 | 8 | 16 | Bajo |
| TRAB-11 | Postest | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 16 | 16 | 32 | Alto |
| TRAB-12 | Pretest | 1 | 2 | 1 | 1 | 2 | 2 | 2 | 1 | 5 | 7 | 12 | Bajo |
| TRAB-12 | Postest | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 20 | 20 | 40 | Alto |
| TRAB-13 | Pretest | 3 | 2 | 2 | 3 | 3 | 3 | 2 | 3 | 10 | 11 | 21 | Medio |
| TRAB-13 | Postest | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 16 | 16 | 32 | Alto |
| TRAB-14 | Pretest | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 8 | 8 | 16 | Bajo |
| TRAB-14 | Postest | 4 | 4 | 4 | 5 | 4 | 5 | 4 | 4 | 17 | 17 | 34 | Alto |

*Nota.* AP es la suma de los reactivos 1 a 4; UP, la de los reactivos 5 a 8; TAM corresponde a la sumatoria global de ambos componentes. El baremo se aplica sobre el puntaje TAM. Elaboración propia.

### Módulo B — Reactivos complementarios del postest

El Módulo B se administró a los operadores en la fase de postest como instrumento complementario para explorar percepciones cualitativas sobre la usabilidad, agilidad operativa y generación de reportes del sistema SIVAC. Al constituir una batería descriptiva de exploración funcional, sus puntuaciones se presentan a nivel de caracterización complementaria y no forman parte de la contrastación de las hipótesis inferenciales principales.

B1. Utilizar el sistema SIVAC agiliza notablemente el registro de entradas, salidas y transferencias de dosis de vacunas en mi centro.
B2. SIVAC me permite consultar de manera inmediata y precisa los saldos de existencias por lote en cualquier momento que lo requiera.
B3. La generación automática de vales oficiales en formato PDF en SIVAC facilita enormemente el despacho hacia los establecimientos de salud.
B4. En conjunto, SIVAC incrementa mi productividad y mejora significativamente el control de la cadena de frío en mi jurisdicción.
B5. La interfaz gráfica de SIVAC es clara, intuitiva, limpia y sus botones y opciones de navegación son fácilmente comprensibles.
B6. Aprender a operar los módulos de movimientos, lotes y reportes de SIVAC fue sencillo y demandó poco tiempo de capacitación.
B7. Los mensajes de confirmación, validación de stock y advertencias que emite el sistema SIVAC son claros y orientan mis acciones.
B8. Me resulta fácil lograr que SIVAC ejecute con exactitud las tareas operativas que necesito realizar en mi jornada de trabajo.

| Sujeto | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| TRAB-01 | 5 | 5 | 3 | 4 | 4 | 5 | 4 | 4 |
| TRAB-02 | 4 | 4 | 3 | 3 | 4 | 4 | 3 | 4 |
| TRAB-03 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 4 |
| TRAB-04 | 4 | 4 | 3 | 4 | 4 | 4 | 3 | 3 |
| TRAB-05 | 4 | 4 | 3 | 3 | 4 | 4 | 3 | 4 |
| TRAB-06 | 5 | 5 | 4 | 5 | 5 | 5 | 4 | 5 |
| TRAB-07 | 3 | 4 | 4 | 5 | 4 | 4 | 5 | 5 |
| TRAB-08 | 5 | 5 | 4 | 5 | 5 | 5 | 4 | 5 |
| TRAB-09 | 5 | 4 | 5 | 5 | 5 | 4 | 4 | 5 |
| TRAB-10 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 4 |
| TRAB-11 | 4 | 4 | 3 | 3 | 4 | 4 | 3 | 4 |
| TRAB-12 | 4 | 5 | 3 | 4 | 4 | 5 | 4 | 4 |
| TRAB-13 | 3 | 3 | 4 | 4 | 3 | 3 | 4 | 4 |
| TRAB-14 | 4 | 4 | 4 | 5 | 4 | 4 | 5 | 5 |

*Nota.* Respuestas registradas en el instrumento complementario durante la fase de postest ( = 14$). Elaboración propia.

---

<a id="parte-6"></a>
## Parte 6. Matriz de indicadores por unidad y diferencias pareadas

Las dos matrices siguientes presentan, para cada una de las catorce unidades, los siete indicadores en cada fase. La tercera matriz presenta la diferencia pareada D = postest − pretest. En los dos indicadores de tiempo la diferencia es negativa porque un menor tiempo constituye una mejora; en los cinco restantes es positiva.

### Matriz 6.1 — Pretest

| Sujeto | T_reg | T_vale | RSD | CPE | AP | UP | TAM |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TRAB-01 | 38.50 | 18.50 | 62.50 | 64.00 | 8.00 | 9.00 | 17.00 |
| TRAB-02 | 42.00 | 22.00 | 57.50 | 64.00 | 6.00 | 8.00 | 14.00 |
| TRAB-03 | 35.00 | 16.00 | 65.00 | 72.00 | 9.00 | 10.00 | 19.00 |
| TRAB-04 | 33.50 | 15.00 | 72.50 | 76.00 | 11.00 | 12.00 | 23.00 |
| TRAB-05 | 40.00 | 20.50 | 55.00 | 60.00 | 6.00 | 8.00 | 14.00 |
| TRAB-06 | 36.50 | 17.00 | 65.00 | 68.00 | 8.00 | 8.00 | 16.00 |
| TRAB-07 | 44.00 | 24.00 | 52.50 | 56.00 | 4.00 | 6.00 | 10.00 |
| TRAB-08 | 32.00 | 14.50 | 75.00 | 80.00 | 12.00 | 12.00 | 24.00 |
| TRAB-09 | 31.50 | 15.00 | 72.50 | 76.00 | 10.00 | 11.00 | 21.00 |
| TRAB-10 | 39.00 | 19.50 | 60.00 | 64.00 | 8.00 | 8.00 | 16.00 |
| TRAB-11 | 37.00 | 18.00 | 62.50 | 68.00 | 8.00 | 8.00 | 16.00 |
| TRAB-12 | 41.50 | 21.00 | 57.50 | 60.00 | 5.00 | 7.00 | 12.00 |
| TRAB-13 | 34.00 | 16.50 | 67.50 | 72.00 | 10.00 | 11.00 | 21.00 |
| TRAB-14 | 36.00 | 17.50 | 65.00 | 68.00 | 8.00 | 8.00 | 16.00 |

*Nota.* Mediciones de línea base (pretest). T_reg y T_vale expresados en minutos; RSD y CPE en porcentaje (%); AP, UP y TAM en puntos de escala. Elaboración propia.

### Matriz 6.2 — Postest

| Sujeto | T_reg | T_vale | RSD | CPE | AP | UP | TAM |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TRAB-01 | 5.37 | 2.12 | 95.00 | 96.00 | 20.00 | 20.00 | 40.00 |
| TRAB-02 | 5.73 | 1.83 | 97.50 | 96.00 | 19.00 | 16.00 | 35.00 |
| TRAB-03 | 5.34 | 1.72 | 95.00 | 96.00 | 17.00 | 18.00 | 35.00 |
| TRAB-04 | 5.59 | 2.17 | 90.00 | 96.00 | 18.00 | 17.00 | 35.00 |
| TRAB-05 | 6.15 | 1.86 | 97.50 | 96.00 | 20.00 | 20.00 | 40.00 |
| TRAB-06 | 4.82 | 1.67 | 95.00 | 96.00 | 20.00 | 20.00 | 40.00 |
| TRAB-07 | 4.95 | 2.00 | 100.00 | 92.00 | 20.00 | 20.00 | 40.00 |
| TRAB-08 | 5.92 | 1.96 | 97.50 | 96.00 | 18.00 | 19.00 | 37.00 |
| TRAB-09 | 6.01 | 1.65 | 97.50 | 96.00 | 20.00 | 19.00 | 39.00 |
| TRAB-10 | 6.29 | 1.87 | 97.50 | 96.00 | 20.00 | 20.00 | 40.00 |
| TRAB-11 | 6.44 | 1.78 | 95.00 | 92.00 | 16.00 | 16.00 | 32.00 |
| TRAB-12 | 5.74 | 2.07 | 97.50 | 92.00 | 20.00 | 20.00 | 40.00 |
| TRAB-13 | 5.53 | 2.27 | 92.50 | 96.00 | 16.00 | 16.00 | 32.00 |
| TRAB-14 | 5.63 | 1.90 | 97.50 | 88.00 | 17.00 | 17.00 | 34.00 |

*Nota.* Mediciones finales (postest). T_reg y T_vale corresponden a la media de tres réplicas por unidad experimental. Elaboración propia.

### Matriz 6.3 — Diferencias pareadas (postest − pretest)

| Sujeto | T_reg | T_vale | RSD | CPE | AP | UP | TAM |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TRAB-01 | -33.13 | -16.38 | 32.50 | 32.00 | 12.00 | 11.00 | 23.00 |
| TRAB-02 | -36.27 | -20.17 | 40.00 | 32.00 | 13.00 | 8.00 | 21.00 |
| TRAB-03 | -29.66 | -14.28 | 30.00 | 24.00 | 8.00 | 8.00 | 16.00 |
| TRAB-04 | -27.91 | -12.83 | 17.50 | 20.00 | 7.00 | 5.00 | 12.00 |
| TRAB-05 | -33.85 | -18.64 | 42.50 | 36.00 | 14.00 | 12.00 | 26.00 |
| TRAB-06 | -31.68 | -15.33 | 30.00 | 28.00 | 12.00 | 12.00 | 24.00 |
| TRAB-07 | -39.05 | -22.00 | 47.50 | 36.00 | 16.00 | 14.00 | 30.00 |
| TRAB-08 | -26.08 | -12.54 | 22.50 | 16.00 | 6.00 | 7.00 | 13.00 |
| TRAB-09 | -25.49 | -13.35 | 25.00 | 20.00 | 10.00 | 8.00 | 18.00 |
| TRAB-10 | -32.71 | -17.63 | 37.50 | 32.00 | 12.00 | 12.00 | 24.00 |
| TRAB-11 | -30.56 | -16.22 | 32.50 | 24.00 | 8.00 | 8.00 | 16.00 |
| TRAB-12 | -35.76 | -18.93 | 40.00 | 32.00 | 15.00 | 13.00 | 28.00 |
| TRAB-13 | -28.47 | -14.23 | 25.00 | 24.00 | 6.00 | 5.00 | 11.00 |
| TRAB-14 | -30.37 | -15.60 | 32.50 | 20.00 | 9.00 | 9.00 | 18.00 |

*Nota.* Diferencias pareadas (D = postest − pretest). Una diferencia negativa en T_reg y T_vale indica reducción del tiempo operacional; un valor positivo en RSD, CPE, AP, UP y TAM indica incremento en la consistencia documental y satisfacción del usuario. Elaboración propia.

---

<a id="parte-7"></a>
## Parte 7. Tablas 35 a 43 — Resultados estadísticos inferenciales

A continuación se presentan los resultados del análisis estadístico descriptivo e inferencial organizados en las Tablas 35 a 43, siguiendo la estructura del informe de investigación. Los contrastes estadísticos evalúan el impacto de la implementación del sistema SIVAC sobre los indicadores operacionales: T_reg, T_vale, RSD, CPE, AP, UP y TAM.

### Tabla 35. Confiabilidad de consistencia interna del Cuestionario TAM (Instrumento N.° 03) mediante el coeficiente Alfa de Cronbach e intervalo de confianza del 95 %

| Momento de evaluación | Escala / subescala | N.° de ítems | Muestra (n) | Alfa de Cronbach | IC 95 % [LI, LS] | Nivel de consistencia |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| Pretest (proceso manual) | Escala global TAM (modalidad A) | 8 | 14 | 0.939 | [0.874, 0.977] | Excelente |
| Pretest (proceso manual) | Aceptación del proceso (AP) | 4 | 14 | 0.877 | [0.721, 0.956] | Buena |
| Pretest (proceso manual) | Utilidad percibida (UP) | 4 | 14 | 0.874 | [0.715, 0.955] | Buena |
| Postest (Sistema SIVAC) | Escala global TAM (modalidad A) | 8 | 14 | 0.924 | [0.845, 0.972] | Excelente |
| Postest (Sistema SIVAC) | Aceptación del proceso (AP) | 4 | 14 | 0.854 | [0.671, 0.948] | Buena |
| Postest (Sistema SIVAC) | Utilidad percibida (UP) | 4 | 14 | 0.880 | [0.730, 0.957] | Buena |

*Nota.* Intervalo de confianza al 95 % obtenido mediante el procedimiento de Feldt sobre la distribución F. Elaboración propia.

### Tabla 36. Estadística descriptiva comparativa pretest y postest para los indicadores de la Dimensión 1: Oportunidad de procesamiento (n = 14)

| Indicador | Momento | Media | DE | Mediana | RIC | Mín – Máx | Variación |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| T_reg (min) | Pretest (manual) | 37.18 | 3.83 | 36.75 | 5.50 | 31.50 – 44.00 | No aplica |
| T_reg (min) | Postest (SIVAC) | 5.68 | 0.47 | 5.68 | 0.58 | 4.82 – 6.44 | -84.7 % |
| T_reg (min) | Diferencia pareada | -31.50 | 3.93 | -31.12 | 4.90 | -39.05 – -25.49 | No aplica |
| T_vale (min) | Pretest (manual) | 18.21 | 2.87 | 17.75 | 4.12 | 14.50 – 24.00 | No aplica |
| T_vale (min) | Postest (SIVAC) | 1.92 | 0.19 | 1.89 | 0.26 | 1.65 – 2.27 | -89.5 % |
| T_vale (min) | Diferencia pareada | -16.29 | 2.86 | -15.91 | 4.14 | -22.00 – -12.54 | No aplica |

*Nota.* La variación se calcula como cambio relativo porcentual respecto del pretest. RIC = rango intercuartílico. Los tiempos corresponden a la media de tres réplicas por unidad experimental. El proceso completo de registro y emisión descendió de 55.39 a 7.60 minutos por jornada observada. Elaboración propia.

### Tabla 37. Estadística descriptiva comparativa pretest y postest para los indicadores de la Dimensión 2: Consistencia documental (n = 14)

| Indicador | Momento | Media | DE | Mediana | RIC | Mín – Máx | Variación |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Registros sin discrepancias (RSD, %) | Pretest (manual) | 63.57 | 6.77 | 63.75 | 8.75 | 52.50 – 75.00 | No aplica |
| Registros sin discrepancias (RSD, %) | Postest (SIVAC) | 96.07 | 2.54 | 97.50 | 2.50 | 90.00 – 100.00 | +32.50 pp |
| Registros sin discrepancias (RSD, %) | Diferencia pareada | 32.50 | 8.38 | 32.50 | 13.12 | 17.50 – 47.50 | No aplica |
| Concordancia programada vs entregada (CPE, %) | Pretest (manual) | 67.71 | 6.92 | 68.00 | 8.00 | 56.00 – 80.00 | No aplica |
| Concordancia programada vs entregada (CPE, %) | Postest (SIVAC) | 94.57 | 2.53 | 96.00 | 3.00 | 88.00 – 96.00 | +26.86 pp |
| Concordancia programada vs entregada (CPE, %) | Diferencia pareada | 26.86 | 6.55 | 26.00 | 11.00 | 16.00 – 36.00 | No aplica |

*Nota.* El cambio de los porcentajes se informa en puntos porcentuales (pp). En la distribución empírica del postest la media de RSD supera el 96 % y la de CPE el 94 %, con observaciones por debajo del máximo de la escala en ambos indicadores. Elaboración propia.

### Tabla 38. Estadística descriptiva comparativa pretest y postest para los indicadores de la Dimensión 3: Satisfacción del usuario (n = 14)

| Indicador | Momento | Media | DE | Mediana | RIC | Mín – Máx | Variación |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Aceptación del proceso (AP) | Pretest (manual) | 8.07 | 2.27 | 8.00 | 3.25 | 4.00 – 12.00 | No aplica |
| Aceptación del proceso (AP) | Postest (SIVAC) | 18.64 | 1.60 | 19.50 | 2.75 | 16.00 – 20.00 | +131.0 % |
| Aceptación del proceso (AP) | Diferencia pareada | 10.57 | 3.32 | 11.00 | 4.75 | 6.00 – 16.00 | No aplica |
| Utilidad percibida (UP) | Pretest (manual) | 9.00 | 1.88 | 8.00 | 2.75 | 6.00 – 12.00 | No aplica |
| Utilidad percibida (UP) | Postest (SIVAC) | 18.43 | 1.70 | 19.00 | 3.00 | 16.00 – 20.00 | +104.8 % |
| Utilidad percibida (UP) | Diferencia pareada | 9.43 | 2.90 | 8.50 | 4.00 | 5.00 – 14.00 | No aplica |
| Puntaje global TAM | Pretest (manual) | 17.07 | 4.08 | 16.00 | 6.00 | 10.00 – 24.00 | No aplica |
| Puntaje global TAM | Postest (SIVAC) | 37.07 | 3.15 | 38.00 | 5.00 | 32.00 – 40.00 | +117.2 % |
| Puntaje global TAM | Diferencia pareada | 20.00 | 6.05 | 19.50 | 8.00 | 11.00 – 30.00 | No aplica |

*Nota.* AP y UP se evalúan sobre 20 puntos; el puntaje global TAM, sobre 40 puntos, y representa la suma directa de AP y UP. Ninguna unidad presentó diferencias nulas en los reactivos: las catorce registraron incremento en las tres medidas. Elaboración propia.

### Tabla 39. Prueba de bondad de ajuste de normalidad de Shapiro-Wilk para las diferencias pareadas pretest y postest (n = 14)

| Dim. | Indicador | W | p | Decisión | Prueba |
| :---: | :--- | :---: | :---: | :--- | :--- |
| D1 | T_reg | 0.981 | .978 | Normal (p > .05) | t pareada |
| D1 | T_vale | 0.955 | .641 | Normal (p > .05) | t pareada |
| D2 | RSD | 0.979 | .970 | Normal (p > .05) | t pareada |
| D2 | CPE | 0.915 | .189 | Normal (p > .05) | t pareada |
| D3 | AP | 0.942 | .441 | Normal (p > .05) | t pareada |
| D3 | UP | 0.927 | .274 | Normal (p > .05) | t pareada |
| D3 | TAM | 0.958 | .687 | Normal (p > .05) | t pareada |

*Nota.* D1 = Oportunidad de procesamiento; D2 = Consistencia documental; D3 = Satisfacción del usuario. La evaluación de normalidad se realiza con un nivel de significancia de .05 sobre las diferencias pareadas (D = postest − pretest). Ningún indicador rechaza la normalidad distributiva según la prueba de Shapiro-Wilk (p mínimo = 0.189), por lo que la prueba t de Student pareada constituye el contraste paramétrico decisorio y la prueba de Wilcoxon se reporta como verificación de robustez no paramétrica. Elaboración propia.

### Tabla 40. Contraste inferencial de la Hipótesis Específica 1: Oportunidad de procesamiento mediante pruebas paramétricas y no paramétricas pareadas

| Indicador | Prueba | n / gl | Estadístico | p | p exacto | Tamaño del efecto | p ajustado (Holm) | Decisión |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| T_reg | t de Student pareada | 14 / 13 | t = -29.997 | < .001 | 2.18e-13 | d_z = 8.02 | 1.52e-12 | Rechazar H0 |
| T_reg | Wilcoxon (corrob.) | 14 / 13 | W = 0.0 (Z = -3.296) | < .001 | 1.22e-04 | r = 0.881 | No aplica | No aplica |
| T_vale | t de Student pareada | 14 / 13 | t = -21.320 | < .001 | 1.69e-11 | d_z = 5.70 | 1.02e-10 | Rechazar H0 |
| T_vale | Wilcoxon (corrob.) | 14 / 13 | W = 0.0 (Z = -3.296) | < .001 | 1.22e-04 | r = 0.881 | No aplica | No aplica |

*Nota.* Nivel de significancia .05. La columna «n / gl» consigna los pares válidos o grados de libertad según corresponda. La columna «p exacto» consigna el valor de probabilidad obtenido y «p» en formato estándar APA. Las dos pruebas de Wilcoxon son exactas al no registrarse empates en el valor absoluto de las diferencias ni diferencias nulas. El tamaño del efecto d_z se calcula sobre la desviación estándar de las diferencias pareadas y r como |Z| dividido entre la raíz del número de pares efectivos. Elaboración propia.

### Tabla 41. Contraste inferencial de la Hipótesis Específica 2: Consistencia documental mediante pruebas paramétricas y no paramétricas pareadas

| Indicador | Prueba | n / gl | Estadístico | p | p exacto | Tamaño del efecto | p ajustado (Holm) | Decisión |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| RSD | t de Student pareada | 14 / 13 | t = 14.515 | < .001 | 2.07e-09 | d_z = 3.88 | 8.28e-09 | Rechazar H0 |
| RSD | Wilcoxon (corrob.) | 14 / 13 | W = 105.0 (Z = 3.301) | < .001 | 9.62e-04 | r = 0.882 | No aplica | No aplica |
| CPE | t de Student pareada | 14 / 13 | t = 15.342 | < .001 | 1.04e-09 | d_z = 4.10 | 5.22e-09 | Rechazar H0 |
| CPE | Wilcoxon (corrob.) | 14 / 13 | W = 105.0 (Z = 3.311) | < .001 | 9.29e-04 | r = 0.885 | No aplica | No aplica |

*Nota.* Nivel de significancia .05. Para RSD y CPE el contraste de Wilcoxon emplea el método asintótico con corrección por empates debido a la presencia de diferencias coincidentes en la escala discreta del instrumento. Las pruebas paramétricas principales forman parte de la familia ajustada mediante Holm-Bonferroni. Elaboración propia.

### Tabla 42. Contraste inferencial de la Hipótesis Específica 3: Satisfacción del usuario mediante pruebas paramétricas y no paramétricas pareadas

| Indicador | Prueba | n / gl | Estadístico | p | p exacto | Tamaño del efecto | p ajustado (Holm) | Decisión |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| AP | t de Student pareada | 14 / 13 | t = 11.908 | < .001 | 2.29e-08 | d_z = 3.18 | 4.36e-08 | Rechazar H0 |
| AP | Wilcoxon (corrob.) | 14 / 13 | W = 105.0 (Z = 3.301) | < .001 | 9.65e-04 | r = 0.882 | No aplica | No aplica |
| UP | t de Student pareada | 14 / 13 | t = 12.160 | < .001 | 1.78e-08 | d_z = 3.25 | 4.36e-08 | Rechazar H0 |
| UP | Wilcoxon (corrob.) | 14 / 13 | W = 105.0 (Z = 3.308) | < .001 | 9.40e-04 | r = 0.884 | No aplica | No aplica |
| TAM | t de Student pareada | 14 / 13 | t = 12.367 | < .001 | 1.45e-08 | d_z = 3.31 | 4.36e-08 | Rechazar H0 |
| TAM | Wilcoxon (corrob.) | 14 / 13 | W = 105.0 (Z = 3.298) | < .001 | 9.73e-04 | r = 0.881 | No aplica | No aplica |

*Nota.* Nivel de significancia .05. Las tres medidas de la dimensión registraron diferencias no nulas en las catorce unidades, por lo que la prueba de Wilcoxon opera con la totalidad de los pares y método asintótico por empates. El puntaje TAM representa la suma directa de AP y UP. Elaboración propia.

### Tabla 43. Resumen de contrastación inferencial multivariada y regla de decisión para la Hipótesis General con ajuste secuencial de Holm-Bonferroni

| Hipótesis | Dim. | Prueba | p original | p Holm | Decisión | Impacto operativo |
| :---: | :---: | :--- | :---: | :---: | :--- | :--- |
| HE1 | D1 | t / Wilcoxon | 1.69e-11 | 1.02e-10 | Rechazar H0 | Tiempos: -84.7 % y -89.5 % |
| HE2 | D2 | t / Wilcoxon | 2.07e-09 | 8.28e-09 | Rechazar H0 | RSD 96.07 %; CPE 94.57 % |
| HE3 | D3 | t / Wilcoxon | 2.29e-08 | 4.36e-08 | Rechazar H0 | AP y UP: +131.0 % y +104.8 % |
| HG | VD | Conjuntivo | — | — | Rechazar H0 | Mejora integral en D1, D2 y D3 |

*Nota.* HE1, HE2 y HE3 designan las hipótesis específicas de D1, D2 y D3; VD es la variable dependiente y HG, la hipótesis general. Cada fila de hipótesis específica reporta el contraste más conservador de su respectiva dimensión para gobernar la decisión inferencial. La hipótesis general es conjuntiva: se sostiene al rechazar conjuntamente la hipótesis nula en la totalidad de los indicadores tras el ajuste secuencial de Holm-Bonferroni. El máximo p ajustado de los indicadores oficiales (4.36e-08) acota la decisión global. Elaboración propia.

### Síntesis de los siete contrastes

| Indicador | n válidos | W+ | Z | p exacta | Método | r de Rosenthal | p Holm |
| :--- | :---: | ---: | ---: | :---: | :---: | ---: | :---: |
| T_reg | 14 | 0.0 | -3.296 | 0.000122 | exacto | 0.881 | 1.52e-12 |
| T_vale | 14 | 0.0 | -3.296 | 0.000122 | exacto | 0.881 | 1.02e-10 |
| RSD | 14 | 105.0 | 3.301 | 0.000962 | asintótico | 0.882 | 8.28e-09 |
| CPE | 14 | 105.0 | 3.311 | 0.000929 | asintótico | 0.885 | 5.22e-09 |
| AP | 14 | 105.0 | 3.301 | 0.000965 | asintótico | 0.882 | 4.36e-08 |
| UP | 14 | 105.0 | 3.308 | 0.000940 | asintótico | 0.884 | 4.36e-08 |
| TAM | 14 | 105.0 | 3.298 | 0.000973 | asintótico | 0.881 | 4.36e-08 |

*Nota.* En los indicadores de tiempo (T_reg y T_vale) la totalidad de los catorce operadores registró reducciones en sus duraciones (W+ = 0). Al confirmarse el supuesto de normalidad en las diferencias pareadas, la inferencia decisoria se sustenta en la prueba t de Student pareada con ajuste de Holm-Bonferroni, reportándose Wilcoxon como verificación de robustez no paramétrica. Elaboración propia.

---

---

<a id="parte-8"></a>
## Parte 8. Análisis de consistencia operativa y observaciones de campo

El análisis de consistencia de los datos recolectados en campo permite corroborar la estabilidad métrica y el comportamiento empírico de las variables tras la implementación del sistema SIVAC en la red asistencial.

### Comportamiento de los indicadores y características empíricas

1. **Magnitud del impacto operativo y tamaño del efecto:** en los cinco indicadores de escala cerrada o porcentual (RSD, CPE, AP, UP y TAM) el tamaño del efecto estandarizado d_z osciló entre 3.183 y 4.100, con una amplitud de 0.918 y valores comprendidos en el rango de efecto grande según las convenciones de Cohen. En los indicadores de tiempo, la transición del soporte manual en papel a la plataforma digital produjo reducciones sustanciales: T_reg disminuyó 84.7 % (aceleración de 6.5×), pasando de una media de 37.18 min a 5.68 min; T_vale redujo su duración en 89.5 % (aceleración de 9.5×), de 18.21 min a 1.92 min (115.2 segundos). El recorrido conjunto de ambas operaciones cayó de 55.39 a 7.60 minutos por jornada observada.

2. **Concentración en el límite superior de las escalas:** las dos medidas de consistencia documental se desplazan hacia el extremo superior del instrumento, lo que constituye el resultado buscado y a la vez impone un límite a su poder discriminativo. En RSD el valor más frecuente (97.50 %) se repite en 7 de las catorce unidades y 1 operador alcanza el 100 % (TRAB-07); en CPE la moda (96.00 %) se repite en 10 unidades y ningún operador alcanza la concordancia absoluta. La concentración se documenta como efecto techo operativo: el indicador conserva capacidad de detección en la cola inferior, donde aún se registran valores de 88.00 % a 94.57 % en CPE.

3. **Dispersión en los tiempos de postest:** se registró una amplitud operacional genuina entre los operadores durante el postest: T_reg osciló entre 4.82 y 6.44 minutos, y T_vale entre 1.65 y 2.27 minutos (99 a 136 segundos). El operador con mayor duración en registro (TRAB-11) no coincidió con el de mayor duración en emisión de vales (TRAB-13), ni el más veloz en registro (TRAB-06) con el más veloz en vales (TRAB-09), lo que corrobora la heterogeneidad de destrezas operativas individuales.

4. **Respuesta singular y paridad de ganancia:** no se registró ninguna diferencia pareada nula en los siete indicadores: las catorce unidades mejoraron en todas las medidas, de modo que las pruebas de rangos con signo operan con los catorce pares informativos. El puntaje TAM global más bajo del postest correspondió a TRAB-11, TRAB-13 con 32.00 puntos, aun dentro del nivel Alto del baremo, lo que evidencia que la ganancia no dependió de un único perfil de usuario.

5. **Comportamiento homogéneo de reducción de tiempos:** en la totalidad de los catorce operadores censales se verificó una reducción efectiva en los tiempos de registro y emisión de vales (D < 0), sin ningún caso de retroceso temporal. El mayor tiempo residual en el postest correspondió a TRAB-11 con 6.44 min en T_reg, atribuido a intermitencias locales de conectividad durante la réplica; aun así registró una reducción neta de 30.56 minutos respecto de su línea base manual (37.00 min).

6. **Cumplimiento de supuestos distributivos:** la prueba de Shapiro-Wilk aplicada sobre las diferencias pareadas (D = postest − pretest) de los siete indicadores no rechazó la normalidad distributiva en ninguno de los casos (p mínimo = 0.189), lo que valida el uso de la prueba t de Student pareada como contraste paramétrico primario para la toma de decisiones sobre las hipótesis del estudio.

### Casos especiales y observaciones cualitativas de campo

| Caso | Sujeto | Indicador | Valores | Observación operativa de campo | Tratamiento estadístico |
| :--- | :---: | :---: | :---: | :--- | :--- |
| Mayor tiempo residual de registro | TRAB-11 | T_reg | 37.00 → 6.44 | Intermitencia de conectividad durante la réplica de postest. | Reducción neta favorable; evaluado con la muestra censal completa. |
| Mayor tiempo residual de emisión | TRAB-13 | T_vale | 16.50 → 2.27 | Emisión de vale sujeta a verificación manual de stock. | Reducción neta favorable; sin efecto sobre la decisión inferencial. |
| Menor puntaje TAM del postest | TRAB-11 | TAM | 16.00 → 32.00 | Operador con menor exposición previa a herramientas informáticas. | Nivel Alto del baremo; incluido sin exclusión en la muestra censal. |

*Nota.* Observaciones cualitativas registradas durante la administración de las fichas de campo. Elaboración propia.

### Matriz de consistencia de los indicadores observados

| Criterio metodológico | Parámetro evaluado | Resultado empírico observado | Estado de consistencia |
| :--- | :--- | :---: | :---: |
| Magnitud del efecto estandarizado | d_z en indicadores acotados (RSD, CPE, AP, UP, TAM) | 3.183 – 4.100 (efecto grande) | Conforme |
| Dispersión del tamaño del efecto | Amplitud de d_z en indicadores acotados | 0.918 | Conforme |
| Reducción relativa en tiempos | Optimización en T_reg y T_vale | 84.7 % (6.5×) y 89.5 % (9.5×) | Conforme |
| Concentración en el límite superior | Moda de los puntajes de postest | 7 de 14 en RSD / 10 de 14 en CPE | Documentado |
| Límites de saturación | Sujetos en el valor máximo de la escala | 1 en RSD (100 %) / 0 en CPE (96.00 % máx.) | Conforme |
| Rango empírico postest (T_reg) | Dispersión operativa observada | 4.82 – 6.44 min (amplitud: 1.62 min) | Conforme |
| Rango empírico postest (T_vale) | Dispersión operativa observada | 1.65 – 2.27 min (amplitud: 0.620 min) | Conforme |
| Casos con diferencia pareada nula | Estabilidad en la puntuación observada | 0 casos | Conforme |
| Eficacia en reducción temporal | Sujetos con reducción de tiempo en postest | 14 de 14 operadores (100 %) | Conforme |
| Caso con mayor tiempo residual | Identificación de casos singulares en campo | 1 caso (TRAB-11, T_reg postest: 6.44 min) | Conforme |
| Coherencia en percepción global | Sujetos con TAM postest en nivel Alto | 14 de 14 | Conforme |
| Parámetros descriptivos basales | Medias de T_reg y T_vale en pretest | 37.18 min y 18.21 min | Conforme |
| Parámetros descriptivos finales | Medias de T_reg y T_vale en postest | 5.68 min y 1.92 min | Conforme |
| Supuesto de normalidad | Pruebas de Shapiro-Wilk sobre diferencias (p > .05) | 7 de 7 indicadores con normalidad (p mínimo = 0.189) | Conforme |
| Precisión en cálculo de tiempos | Promedio aritmético de las tres réplicas | Coincidencia exacta con registros individuales | Conforme |

*Nota.* Verificación metodológica y consistencia del conjunto de datos de campo. Elaboración propia.
