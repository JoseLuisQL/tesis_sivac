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

Centro de acopio: **ALMACÉN (CHANKA)** (CHANKA-001) · Observador: **OBS-01**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-CHANKA001-0358 | ROTA-2605-833M | 07:30:00 | 08:05:22 | 35.3667 | — | — | Sí |
| REG-02 | T2 | SAL-CHANKA001-2407 | VARI-2501-250M | 08:05:22 | 08:46:25 | 39.5500 | 90 | P3 | Sí |
| REG-03 | T3 | TRA-CHANKA001-2886 | ROTA-2605-833M | 08:46:25 | 09:27:00 | 40.5833 | — | — | Sí |

Cierre: 115.5000 min ÷ 3 = **38.5000 min**. Suma de las tres réplicas: 115.5000 min (6930 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-0810-8750 | — | 09:29:49 | 09:47:26 | 16.8667 | 45 | P3 | Sí |
| VALE-02 | T5 | PEC-2026-0810-8953 | — | 09:47:26 | 10:06:01 | 18.5833 | — | — | Sí |
| VALE-03 | T6 | PEC-2026-0810-9564 | — | 10:06:01 | 10:28:34 | 20.0500 | 150 | P4 | Sí |

Cierre: 55.5000 min ÷ 3 = **18.5000 min**. Suma de las tres réplicas: 55.5000 min (3330 s).

**Resumen del operador.** T_reg promedio: 38.5000 min · T_vale promedio: 18.5000 min · Réplicas válidas: 6 de 6.

---

### Bloque 2 · TRAB-01 · Postest (Sistema SIVAC) · 12/10/2026

Centro de acopio: **ALMACÉN (CHANKA)** (CHANKA-001) · Observador: **OBS-01**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-CHANKA001-0244 | SPR-2603-471K | 08:00:00 | 08:04:52 | 4.8667 | — | — | Sí |
| REG-02 | T2 | SAL-CHANKA001-0540 | BCG-2607-654A | 08:04:52 | 08:10:22 | 5.5000 | — | — | Sí |
| REG-03 | T3 | TRA-CHANKA001-3016 | VARI-2503-521A | 08:10:22 | 08:16:07 | 5.7500 | — | — | Sí |

Cierre: 16.1167 min ÷ 3 = **5.3722 min**. Suma de las tres réplicas: 16.1167 min (967 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-1012-4936 | — | 08:17:51 | 08:19:54 | 2.0500 (123 s) | — | — | Sí |
| VALE-02 | T5 | PEC-2026-1012-8235 | — | 08:19:54 | 08:21:55 | 2.0167 (121 s) | — | — | Sí |
| VALE-03 | T6 | PEC-2026-1012-9612 | — | 08:21:55 | 08:24:13 | 2.3000 (138 s) | — | — | Sí |

Cierre: 6.3667 min ÷ 3 = **2.1222 min**. Suma de las tres réplicas: 6.3667 min (382 s).

**Resumen del operador.** T_reg promedio: 5.3722 min · T_vale promedio: 2.1222 min · Réplicas válidas: 6 de 6.

---

### Bloque 3 · TRAB-02 · Pretest (proceso manual) · 10/08/2026

Centro de acopio: **ALMACÉN (CHANKA)** (CHANKA-001) · Observador: **OBS-02**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-CHANKA001-2073 | VARI-2607-979A | 07:15:00 | 07:53:07 | 37.3667 | 45 | P3 | Sí |
| REG-02 | T2 | SAL-CHANKA001-2772 | HEPB-2509-474M | 07:53:07 | 08:36:03 | 42.9333 | — | — | Sí |
| REG-03 | T3 | TRA-CHANKA001-2936 | INFL-2603-792B | 08:36:03 | 09:21:45 | 45.7000 | — | — | Sí |

Cierre: 126.0000 min ÷ 3 = **42.0000 min**. Suma de las tres réplicas: 126.0000 min (7560 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-0810-5392 | — | 09:25:29 | 09:46:06 | 20.6167 | — | — | Sí |
| VALE-02 | T5 | PEC-2026-0810-7266 | — | 09:46:06 | 10:08:35 | 22.4833 | — | — | Sí |
| VALE-03 | T6 | PEC-2026-0810-9234 | — | 10:08:35 | 10:32:29 | 22.9000 | 60 | P3 | Sí |

Cierre: 66.0000 min ÷ 3 = **22.0000 min**. Suma de las tres réplicas: 66.0000 min (3960 s).

**Resumen del operador.** T_reg promedio: 42.0000 min · T_vale promedio: 22.0000 min · Réplicas válidas: 6 de 6.

---

### Bloque 4 · TRAB-02 · Postest (Sistema SIVAC) · 12/10/2026

Centro de acopio: **ALMACÉN (CHANKA)** (CHANKA-001) · Observador: **OBS-02**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-CHANKA001-0750 | ROTA-2602-464A | 07:50:00 | 07:55:16 | 5.2667 | — | — | Sí |
| REG-02 | T2 | SAL-CHANKA001-1803 | INFL-2607-737M | 07:55:16 | 08:01:06 | 5.8333 | — | — | Sí |
| REG-03 | T3 | TRA-CHANKA001-2103 | INFL-2508-359M | 08:01:06 | 08:07:41 | 6.0833 | 30 | P2 | Sí |

Cierre: 17.1833 min ÷ 3 = **5.7278 min**. Suma de las tres réplicas: 17.1833 min (1031 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-1012-5542 | — | 08:09:10 | 08:10:58 | 1.8000 (108 s) | — | — | Sí |
| VALE-02 | T5 | PEC-2026-1012-7759 | — | 08:10:58 | 08:12:42 | 1.7333 (104 s) | — | — | Sí |
| VALE-03 | T6 | PEC-2026-1012-9189 | — | 08:12:42 | 08:14:39 | 1.9500 (117 s) | — | — | Sí |

Cierre: 5.4833 min ÷ 3 = **1.8278 min**. Suma de las tres réplicas: 5.4833 min (329 s).

**Resumen del operador.** T_reg promedio: 5.7278 min · T_vale promedio: 1.8278 min · Réplicas válidas: 6 de 6.

---

### Bloque 5 · TRAB-03 · Pretest (proceso manual) · 11/08/2026

Centro de acopio: **Hospital Andahuaylas** (S/C) · Observador: **OBS-01**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-SC-1224 | DTA-2602-236K | 07:45:00 | 08:15:41 | 30.6833 | — | — | Sí |
| REG-02 | T2 | SAL-SC-2491 | HEPB-2609-917M | 08:15:41 | 08:52:47 | 35.6000 | 90 | P2 | Sí |
| REG-03 | T3 | TRA-SC-3043 | ROTA-2603-156K | 08:52:47 | 09:31:30 | 38.7167 | — | — | Sí |

Cierre: 105.0000 min ÷ 3 = **35.0000 min**. Suma de las tres réplicas: 105.0000 min (6300 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-0811-4266 | — | 09:34:19 | 09:49:40 | 15.3500 | — | — | Sí |
| VALE-02 | T5 | PEC-2026-0811-6103 | — | 09:49:40 | 10:05:35 | 15.9167 | — | — | Sí |
| VALE-03 | T6 | PEC-2026-0811-7721 | — | 10:05:35 | 10:22:19 | 16.7333 | — | — | Sí |

Cierre: 48.0000 min ÷ 3 = **16.0000 min**. Suma de las tres réplicas: 48.0000 min (2880 s).

**Resumen del operador.** T_reg promedio: 35.0000 min · T_vale promedio: 16.0000 min · Réplicas válidas: 6 de 6.

---

### Bloque 6 · TRAB-03 · Postest (Sistema SIVAC) · 13/10/2026

Centro de acopio: **Hospital Andahuaylas** (S/C) · Observador: **OBS-01**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-SC-0520 | PENT-2504-482M | 08:15:00 | 08:19:41 | 4.6833 | — | — | Sí |
| REG-02 | T2 | SAL-SC-1437 | IPV-2504-587B | 08:19:41 | 08:25:12 | 5.5167 | — | — | Sí |
| REG-03 | T3 | TRA-SC-2634 | HEPB-2603-786K | 08:25:12 | 08:31:01 | 5.8167 | — | — | Sí |

Cierre: 16.0167 min ÷ 3 = **5.3389 min**. Suma de las tres réplicas: 16.0167 min (961 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-1013-4585 | — | 08:33:09 | 08:34:43 | 1.5667 (94 s) | — | — | Sí |
| VALE-02 | T5 | PEC-2026-1013-5669 | — | 08:34:43 | 08:36:31 | 1.8000 (108 s) | — | — | Sí |
| VALE-03 | T6 | PEC-2026-1013-6328 | — | 08:36:31 | 08:38:19 | 1.8000 (108 s) | — | — | Sí |

Cierre: 5.1667 min ÷ 3 = **1.7222 min**. Suma de las tres réplicas: 5.1667 min (310 s).

**Resumen del operador.** T_reg promedio: 5.3389 min · T_vale promedio: 1.7222 min · Réplicas válidas: 6 de 6.

---

### Bloque 7 · TRAB-04 · Pretest (proceso manual) · 11/08/2026

Centro de acopio: **Hospital ESSALUD Andahuaylas** (11214) · Observador: **OBS-02**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-11214-1271 | DTA-2602-236K | 08:00:00 | 08:32:02 | 31.0333 | 60 | P4 | Sí |
| REG-02 | T2 | SAL-11214-1395 | DTA-2606-829K | 08:32:02 | 09:06:12 | 34.1667 | — | — | Sí |
| REG-03 | T3 | TRA-11214-2308 | DTA-2603-463K | 09:06:12 | 09:42:30 | 35.3000 | 60 | P4 | Sí |

Cierre: 100.5000 min ÷ 3 = **33.5000 min**. Suma de las tres réplicas: 100.5000 min (6030 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-0811-4914 | — | 09:47:50 | 10:01:43 | 13.8833 | — | — | Sí |
| VALE-02 | T5 | PEC-2026-0811-5545 | — | 10:01:43 | 10:18:58 | 14.7500 | 150 | P2 | Sí |
| VALE-03 | T6 | PEC-2026-0811-7989 | — | 10:18:58 | 10:37:20 | 16.3667 | 120 | P4 | Sí |

Cierre: 45.0000 min ÷ 3 = **15.0000 min**. Suma de las tres réplicas: 45.0000 min (2700 s).

**Resumen del operador.** T_reg promedio: 33.5000 min · T_vale promedio: 15.0000 min · Réplicas válidas: 6 de 6.

---

### Bloque 8 · TRAB-04 · Postest (Sistema SIVAC) · 13/10/2026

Centro de acopio: **Hospital ESSALUD Andahuaylas** (11214) · Observador: **OBS-02**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-11214-0127 | ROTA-2507-417A | 08:30:00 | 08:34:57 | 4.9500 | — | — | Sí |
| REG-02 | T2 | SAL-11214-1437 | INFL-2607-737M | 08:34:57 | 08:40:41 | 5.7333 | — | — | Sí |
| REG-03 | T3 | TRA-11214-3081 | INFL-2504-261K | 08:40:41 | 08:47:46 | 6.0833 | 60 | P2 | Sí |

Cierre: 16.7666 min ÷ 3 = **5.5889 min**. Suma de las tres réplicas: 16.7666 min (1006 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-1013-7009 | — | 08:49:27 | 08:51:35 | 2.1333 (128 s) | — | — | Sí |
| VALE-02 | T5 | PEC-2026-1013-7431 | — | 08:51:35 | 08:53:45 | 2.1667 (130 s) | — | — | Sí |
| VALE-03 | T6 | PEC-2026-1013-7680 | — | 08:53:45 | 08:55:58 | 2.2167 (133 s) | — | — | Sí |

Cierre: 6.5167 min ÷ 3 = **2.1722 min**. Suma de las tres réplicas: 6.5167 min (391 s).

**Resumen del operador.** T_reg promedio: 5.5889 min · T_vale promedio: 2.1722 min · Réplicas válidas: 6 de 6.

---

### Bloque 9 · TRAB-05 · Pretest (proceso manual) · 12/08/2026

Centro de acopio: **Centro de Salud Andahuaylas** (6804) · Observador: **OBS-01**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-6804-0461 | SPR-2603-471K | 07:20:00 | 07:58:26 | 36.9333 | 90 | P3 | Sí |
| REG-02 | T2 | SAL-6804-0763 | DTA-2602-236K | 07:58:26 | 08:38:44 | 40.3000 | — | — | Sí |
| REG-03 | T3 | TRA-6804-1831 | IPV-2507-805M | 08:38:44 | 09:21:30 | 42.7667 | — | — | Sí |

Cierre: 120.0000 min ÷ 3 = **40.0000 min**. Suma de las tres réplicas: 120.0000 min (7200 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-0812-6785 | — | 09:25:35 | 09:44:26 | 18.8500 | — | — | Sí |
| VALE-02 | T5 | PEC-2026-0812-8265 | — | 09:44:26 | 10:05:20 | 20.9000 | — | — | Sí |
| VALE-03 | T6 | PEC-2026-0812-9240 | — | 10:05:20 | 10:28:35 | 21.7500 | 90 | P1 | Sí |

Cierre: 61.5000 min ÷ 3 = **20.5000 min**. Suma de las tres réplicas: 61.5000 min (3690 s).

**Resumen del operador.** T_reg promedio: 40.0000 min · T_vale promedio: 20.5000 min · Réplicas válidas: 6 de 6.

---

### Bloque 10 · TRAB-05 · Postest (Sistema SIVAC) · 14/10/2026

Centro de acopio: **Centro de Salud Andahuaylas** (6804) · Observador: **OBS-01**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-6804-0895 | SPR-2504-185M | 07:45:00 | 07:50:33 | 5.5500 | — | — | Sí |
| REG-02 | T2 | SAL-6804-2666 | HEPB-2609-521M | 07:50:33 | 07:57:00 | 6.4500 | — | — | Sí |
| REG-03 | T3 | TRA-6804-2801 | PENT-2605-322M | 07:57:00 | 08:03:27 | 6.4500 | — | — | Sí |

Cierre: 18.4500 min ÷ 3 = **6.1500 min**. Suma de las tres réplicas: 18.4500 min (1107 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-1014-4508 | — | 08:05:46 | 08:07:36 | 1.8333 (110 s) | — | — | Sí |
| VALE-02 | T5 | PEC-2026-1014-5437 | — | 08:07:36 | 08:09:29 | 1.8833 (113 s) | — | — | Sí |
| VALE-03 | T6 | PEC-2026-1014-9469 | — | 08:09:29 | 08:11:21 | 1.8667 (112 s) | — | — | Sí |

Cierre: 5.5833 min ÷ 3 = **1.8611 min**. Suma de las tres réplicas: 5.5833 min (335 s).

**Resumen del operador.** T_reg promedio: 6.1500 min · T_vale promedio: 1.8611 min · Réplicas válidas: 6 de 6.

---

### Bloque 11 · TRAB-06 · Pretest (proceso manual) · 12/08/2026

Centro de acopio: **Talavera** (4195) · Observador: **OBS-02**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4195-0868 | SPR-2606-500M | 07:40:00 | 08:14:54 | 32.4000 | 150 | P4 | Sí |
| REG-02 | T2 | SAL-4195-2781 | SPR-2608-539M | 08:14:54 | 08:51:13 | 36.3167 | — | — | Sí |
| REG-03 | T3 | TRA-4195-3182 | DTA-2505-409K | 08:51:13 | 09:33:00 | 40.7833 | 60 | P1 | Sí |

Cierre: 109.5000 min ÷ 3 = **36.5000 min**. Suma de las tres réplicas: 109.5000 min (6570 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-0812-4840 | — | 09:37:52 | 09:55:17 | 15.9167 | 90 | P4 | Sí |
| VALE-02 | T5 | PEC-2026-0812-4999 | — | 09:55:17 | 10:14:50 | 17.5500 | 120 | P2 | Sí |
| VALE-03 | T6 | PEC-2026-0812-8949 | — | 10:14:50 | 10:34:52 | 17.5333 | 150 | P4 | Sí |

Cierre: 51.0000 min ÷ 3 = **17.0000 min**. Suma de las tres réplicas: 51.0000 min (3060 s).

**Resumen del operador.** T_reg promedio: 36.5000 min · T_vale promedio: 17.0000 min · Réplicas válidas: 6 de 6.

---

### Bloque 12 · TRAB-06 · Postest (Sistema SIVAC) · 14/10/2026

Centro de acopio: **Talavera** (4195) · Observador: **OBS-02**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4195-0552 | NEUM-2506-884B | 08:10:00 | 08:14:34 | 4.5667 | — | — | Sí |
| REG-02 | T2 | SAL-4195-2242 | INFL-2607-737M | 08:14:34 | 08:19:49 | 4.5000 | 45 | P2 | Sí |
| REG-03 | T3 | TRA-4195-2733 | IPV-2504-587B | 08:19:49 | 08:25:13 | 5.4000 | — | — | Sí |

Cierre: 14.4667 min ÷ 3 = **4.8222 min**. Suma de las tres réplicas: 14.4667 min (868 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-1014-5095 | — | 08:27:08 | 08:29:38 | 1.5000 (90 s) | 60 | P2 | Sí |
| VALE-02 | T5 | PEC-2026-1014-8712 | — | 08:29:38 | 08:31:19 | 1.6833 (101 s) | — | — | Sí |
| VALE-03 | T6 | PEC-2026-1014-9586 | — | 08:31:19 | 08:33:09 | 1.8333 (110 s) | — | — | Sí |

Cierre: 5.0166 min ÷ 3 = **1.6722 min**. Suma de las tres réplicas: 5.0166 min (301 s).

**Resumen del operador.** T_reg promedio: 4.8222 min · T_vale promedio: 1.6722 min · Réplicas válidas: 6 de 6.

---

### Bloque 13 · TRAB-07 · Pretest (proceso manual) · 13/08/2026

Centro de acopio: **San Jeronimo** (4167-SJ) · Observador: **OBS-01**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4167SJ-0572 | NEUM-2506-884B | 07:30:00 | 08:09:21 | 39.3500 | — | — | Sí |
| REG-02 | T2 | SAL-4167SJ-1178 | IPV-2504-587B | 08:09:21 | 08:52:53 | 43.5333 | — | — | Sí |
| REG-03 | T3 | TRA-4167SJ-2523 | IPV-2605-698M | 08:52:53 | 09:42:00 | 49.1167 | — | — | Sí |

Cierre: 132.0000 min ÷ 3 = **44.0000 min**. Suma de las tres réplicas: 132.0000 min (7920 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-0813-7111 | — | 09:44:26 | 10:07:35 | 22.1500 | 60 | P3 | Sí |
| VALE-02 | T5 | PEC-2026-0813-7172 | — | 10:07:35 | 10:32:15 | 23.6667 | 60 | P1 | Sí |
| VALE-03 | T6 | PEC-2026-0813-8384 | — | 10:32:15 | 10:58:26 | 26.1833 | — | — | Sí |

Cierre: 72.0000 min ÷ 3 = **24.0000 min**. Suma de las tres réplicas: 72.0000 min (4320 s).

**Resumen del operador.** T_reg promedio: 44.0000 min · T_vale promedio: 24.0000 min · Réplicas válidas: 6 de 6.

---

### Bloque 14 · TRAB-07 · Postest (Sistema SIVAC) · 15/10/2026

Centro de acopio: **San Jeronimo** (4167-SJ) · Observador: **OBS-01**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4167SJ-0841 | PENT-2605-322M | 08:00:00 | 08:04:15 | 4.2500 | — | — | Sí |
| REG-02 | T2 | SAL-4167SJ-1171 | IPV-2608-446B | 08:04:15 | 08:09:54 | 4.9000 | 45 | P1 | Sí |
| REG-03 | T3 | TRA-4167SJ-2510 | VARI-2607-979A | 08:09:54 | 08:16:36 | 5.7000 | 60 | P2 | Sí |

Cierre: 14.8500 min ÷ 3 = **4.9500 min**. Suma de las tres réplicas: 14.8500 min (891 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-1015-5153 | — | 08:18:23 | 08:20:14 | 1.8500 (111 s) | — | — | Sí |
| VALE-02 | T5 | PEC-2026-1015-5178 | — | 08:20:14 | 08:22:58 | 1.9833 (119 s) | 45 | P2 | Sí |
| VALE-03 | T6 | PEC-2026-1015-5958 | — | 08:22:58 | 08:25:08 | 2.1667 (130 s) | — | — | Sí |

Cierre: 6.0000 min ÷ 3 = **2.0000 min**. Suma de las tres réplicas: 6.0000 min (360 s).

**Resumen del operador.** T_reg promedio: 4.9500 min · T_vale promedio: 2.0000 min · Réplicas válidas: 6 de 6.

---

### Bloque 15 · TRAB-08 · Pretest (proceso manual) · 13/08/2026

Centro de acopio: **Huancaray** (4158) · Observador: **OBS-02**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4158-1889 | ROTA-2502-563B | 07:15:00 | 07:44:03 | 29.0500 | — | — | Sí |
| REG-02 | T2 | SAL-4158-2067 | PENT-2605-322M | 07:44:03 | 08:17:13 | 32.1667 | 60 | P1 | Sí |
| REG-03 | T3 | TRA-4158-3158 | HEPB-2609-521M | 08:17:13 | 08:53:30 | 34.7833 | 90 | P3 | Sí |

Cierre: 96.0000 min ÷ 3 = **32.0000 min**. Suma de las tres réplicas: 96.0000 min (5760 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-0813-4773 | — | 08:59:18 | 09:12:59 | 13.6833 | — | — | Sí |
| VALE-02 | T5 | PEC-2026-0813-5834 | — | 09:12:59 | 09:27:49 | 14.0833 | 45 | P3 | Sí |
| VALE-03 | T6 | PEC-2026-0813-6321 | — | 09:27:49 | 09:46:03 | 15.7333 | 150 | P1 | Sí |

Cierre: 43.4999 min ÷ 3 = **14.5000 min**. Suma de las tres réplicas: 43.4999 min (2610 s).

**Resumen del operador.** T_reg promedio: 32.0000 min · T_vale promedio: 14.5000 min · Réplicas válidas: 6 de 6.

---

### Bloque 16 · TRAB-08 · Postest (Sistema SIVAC) · 15/10/2026

Centro de acopio: **Huancaray** (4158) · Observador: **OBS-02**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4158-0211 | IPV-2504-587B | 07:50:00 | 07:55:08 | 5.1333 | — | — | Sí |
| REG-02 | T2 | SAL-4158-0736 | PENT-2508-232M | 07:55:08 | 08:01:44 | 6.1000 | 30 | P2 | Sí |
| REG-03 | T3 | TRA-4158-2260 | ROTA-2507-417A | 08:01:44 | 08:08:16 | 6.5333 | — | — | Sí |

Cierre: 17.7666 min ÷ 3 = **5.9222 min**. Suma de las tres réplicas: 17.7666 min (1066 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-1015-4503 | — | 08:08:25 | 08:10:16 | 1.8500 (111 s) | — | — | Sí |
| VALE-02 | T5 | PEC-2026-1015-5717 | — | 08:10:16 | 08:12:16 | 2.0000 (120 s) | — | — | Sí |
| VALE-03 | T6 | PEC-2026-1015-8174 | — | 08:12:16 | 08:14:18 | 2.0333 (122 s) | — | — | Sí |

Cierre: 5.8833 min ÷ 3 = **1.9611 min**. Suma de las tres réplicas: 5.8833 min (353 s).

**Resumen del operador.** T_reg promedio: 5.9222 min · T_vale promedio: 1.9611 min · Réplicas válidas: 6 de 6.

---

### Bloque 17 · TRAB-09 · Pretest (proceso manual) · 14/08/2026

Centro de acopio: **Chicmo** (4202) · Observador: **OBS-01**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4202-0717 | NEUM-2505-688A | 07:45:00 | 08:14:19 | 29.3167 | — | — | Sí |
| REG-02 | T2 | SAL-4202-2299 | PENT-2504-482M | 08:14:19 | 08:46:16 | 30.9500 | 60 | P1 | Sí |
| REG-03 | T3 | TRA-4202-3126 | PENT-2508-232M | 08:46:16 | 09:20:30 | 34.2333 | — | — | Sí |

Cierre: 94.5000 min ÷ 3 = **31.5000 min**. Suma de las tres réplicas: 94.5000 min (5670 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-0814-4475 | — | 09:22:59 | 09:37:10 | 13.4333 | 45 | P4 | Sí |
| VALE-02 | T5 | PEC-2026-0814-7448 | — | 09:37:10 | 09:51:51 | 14.6833 | — | — | Sí |
| VALE-03 | T6 | PEC-2026-0814-8747 | — | 09:51:51 | 10:11:14 | 16.8833 | 150 | P1 | Sí |

Cierre: 44.9999 min ÷ 3 = **15.0000 min**. Suma de las tres réplicas: 44.9999 min (2700 s).

**Resumen del operador.** T_reg promedio: 31.5000 min · T_vale promedio: 15.0000 min · Réplicas válidas: 6 de 6.

---

### Bloque 18 · TRAB-09 · Postest (Sistema SIVAC) · 16/10/2026

Centro de acopio: **Chicmo** (4202) · Observador: **OBS-01**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4202-0710 | VARI-2607-979A | 08:15:00 | 08:20:38 | 5.6333 | — | — | Sí |
| REG-02 | T2 | SAL-4202-1363 | SPR-2603-471K | 08:20:38 | 08:26:55 | 6.2833 | — | — | Sí |
| REG-03 | T3 | TRA-4202-2017 | PENT-2508-232M | 08:26:55 | 08:33:02 | 6.1167 | — | — | Sí |

Cierre: 18.0333 min ÷ 3 = **6.0111 min**. Suma de las tres réplicas: 18.0333 min (1082 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-1016-9022 | — | 08:34:07 | 08:35:40 | 1.5500 (93 s) | — | — | Sí |
| VALE-02 | T5 | PEC-2026-1016-9377 | — | 08:35:40 | 08:38:24 | 1.7333 (104 s) | 60 | P2 | Sí |
| VALE-03 | T6 | PEC-2026-1016-9571 | — | 08:38:24 | 08:40:04 | 1.6667 (100 s) | — | — | Sí |

Cierre: 4.9500 min ÷ 3 = **1.6500 min**. Suma de las tres réplicas: 4.9500 min (297 s).

**Resumen del operador.** T_reg promedio: 6.0111 min · T_vale promedio: 1.6500 min · Réplicas válidas: 6 de 6.

---

### Bloque 19 · TRAB-10 · Pretest (proceso manual) · 14/08/2026

Centro de acopio: **Huancabamba** (4172) · Observador: **OBS-02**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4172-0842 | HEPB-2609-917M | 08:00:00 | 08:35:58 | 35.9667 | — | — | Sí |
| REG-02 | T2 | SAL-4172-1296 | BCG-2504-789B | 08:35:58 | 09:15:27 | 38.4833 | 60 | P4 | Sí |
| REG-03 | T3 | TRA-4172-2410 | BCG-2507-694K | 09:15:27 | 10:00:00 | 42.5500 | 120 | P2 | Sí |

Cierre: 117.0000 min ÷ 3 = **39.0000 min**. Suma de las tres réplicas: 117.0000 min (7020 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-0814-4563 | — | 10:05:51 | 10:25:39 | 17.8000 | 120 | P3 | Sí |
| VALE-02 | T5 | PEC-2026-0814-5297 | — | 10:25:39 | 10:47:05 | 19.4333 | 120 | P1 | Sí |
| VALE-03 | T6 | PEC-2026-0814-9332 | — | 10:47:05 | 11:08:21 | 21.2667 | — | — | Sí |

Cierre: 58.5000 min ÷ 3 = **19.5000 min**. Suma de las tres réplicas: 58.5000 min (3510 s).

**Resumen del operador.** T_reg promedio: 39.0000 min · T_vale promedio: 19.5000 min · Réplicas válidas: 6 de 6.

---

### Bloque 20 · TRAB-10 · Postest (Sistema SIVAC) · 16/10/2026

Centro de acopio: **Huancabamba** (4172) · Observador: **OBS-02**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4172-0857 | HEPB-2603-786K | 08:30:00 | 08:35:42 | 5.7000 | — | — | Sí |
| REG-02 | T2 | SAL-4172-1817 | DTA-2602-797A | 08:35:42 | 08:42:35 | 6.1333 | 45 | P1 | Sí |
| REG-03 | T3 | TRA-4172-2908 | ROTA-2507-417A | 08:42:35 | 08:49:37 | 7.0333 | — | — | Sí |

Cierre: 18.8666 min ÷ 3 = **6.2889 min**. Suma de las tres réplicas: 18.8666 min (1132 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-1016-5291 | — | 08:51:56 | 08:53:45 | 1.8167 (109 s) | — | — | Sí |
| VALE-02 | T5 | PEC-2026-1016-8280 | — | 08:53:45 | 08:55:37 | 1.8667 (112 s) | — | — | Sí |
| VALE-03 | T6 | PEC-2026-1016-8384 | — | 08:55:37 | 08:58:03 | 1.9333 (116 s) | 30 | P2 | Sí |

Cierre: 5.6167 min ÷ 3 = **1.8722 min**. Suma de las tres réplicas: 5.6167 min (337 s).

**Resumen del operador.** T_reg promedio: 6.2889 min · T_vale promedio: 1.8722 min · Réplicas válidas: 6 de 6.

---

### Bloque 21 · TRAB-11 · Pretest (proceso manual) · 07/09/2026

Centro de acopio: **Pampachiri** (4167) · Observador: **OBS-01**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4167-0304 | VARI-2508-818M | 07:20:00 | 07:52:35 | 32.5833 | — | — | Sí |
| REG-02 | T2 | SAL-4167-2233 | INFL-2508-359M | 07:52:35 | 08:29:52 | 37.2833 | — | — | Sí |
| REG-03 | T3 | TRA-4167-2905 | IPV-2605-698M | 08:29:52 | 09:12:30 | 41.1333 | 90 | P1 | Sí |

Cierre: 110.9999 min ÷ 3 = **37.0000 min**. Suma de las tres réplicas: 110.9999 min (6660 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-0907-5254 | — | 09:18:19 | 09:35:13 | 16.9000 | — | — | Sí |
| VALE-02 | T5 | PEC-2026-0907-5735 | — | 09:35:13 | 09:54:29 | 18.2667 | 60 | P2 | Sí |
| VALE-03 | T6 | PEC-2026-0907-6251 | — | 09:54:29 | 10:13:19 | 18.8333 | — | — | Sí |

Cierre: 54.0000 min ÷ 3 = **18.0000 min**. Suma de las tres réplicas: 54.0000 min (3240 s).

**Resumen del operador.** T_reg promedio: 37.0000 min · T_vale promedio: 18.0000 min · Réplicas válidas: 6 de 6.

---

### Bloque 22 · TRAB-11 · Postest (Sistema SIVAC) · 19/10/2026

Centro de acopio: **Pampachiri** (4167) · Observador: **OBS-01**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4167-0668 | VARI-2501-250M | 07:45:00 | 07:51:03 | 6.0500 | — | — | Sí |
| REG-02 | T2 | SAL-4167-1602 | INFL-2604-777M | 07:51:03 | 07:57:25 | 6.3667 | — | — | Sí |
| REG-03 | T3 | TRA-4167-2544 | NEUM-2509-952A | 07:57:25 | 08:04:19 | 6.9000 | — | — | Sí |

Cierre: 19.3167 min ÷ 3 = **6.4389 min**. Suma de las tres réplicas: 19.3167 min (1159 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-1019-4142 | — | 08:04:25 | 08:06:55 | 1.7500 (105 s) | 45 | P1 | Sí |
| VALE-02 | T5 | PEC-2026-1019-6535 | — | 08:06:55 | 08:09:11 | 1.7667 (106 s) | 30 | P2 | Sí |
| VALE-03 | T6 | PEC-2026-1019-9713 | — | 08:09:11 | 08:11:00 | 1.8167 (109 s) | — | — | Sí |

Cierre: 5.3334 min ÷ 3 = **1.7778 min**. Suma de las tres réplicas: 5.3334 min (320 s).

**Resumen del operador.** T_reg promedio: 6.4389 min · T_vale promedio: 1.7778 min · Réplicas válidas: 6 de 6.

---

### Bloque 23 · TRAB-12 · Pretest (proceso manual) · 07/09/2026

Centro de acopio: **San Antonio de Cachi** (4160) · Observador: **OBS-02**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4160-0677 | INFL-2603-792B | 07:40:00 | 08:19:06 | 37.1000 | 120 | P1 | Sí |
| REG-02 | T2 | SAL-4160-1201 | ROTA-2605-833M | 08:19:06 | 09:00:00 | 40.9000 | — | — | Sí |
| REG-03 | T3 | TRA-4160-2151 | INFL-2607-737M | 09:00:00 | 09:46:30 | 46.5000 | — | — | Sí |

Cierre: 124.5000 min ÷ 3 = **41.5000 min**. Suma de las tres réplicas: 124.5000 min (7470 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-0907-6370 | — | 09:50:39 | 10:11:41 | 20.0333 | 60 | P2 | Sí |
| VALE-02 | T5 | PEC-2026-0907-7152 | — | 10:11:41 | 10:33:01 | 21.3333 | — | — | Sí |
| VALE-03 | T6 | PEC-2026-0907-7929 | — | 10:33:01 | 10:54:39 | 21.6333 | — | — | Sí |

Cierre: 62.9999 min ÷ 3 = **21.0000 min**. Suma de las tres réplicas: 62.9999 min (3780 s).

**Resumen del operador.** T_reg promedio: 41.5000 min · T_vale promedio: 21.0000 min · Réplicas válidas: 6 de 6.

---

### Bloque 24 · TRAB-12 · Postest (Sistema SIVAC) · 19/10/2026

Centro de acopio: **San Antonio de Cachi** (4160) · Observador: **OBS-02**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4160-0496 | NEUM-2505-638K | 08:10:00 | 08:15:46 | 5.0167 | 45 | P1 | Sí |
| REG-02 | T2 | SAL-4160-0584 | BCG-2606-296K | 08:15:46 | 08:21:50 | 6.0667 | — | — | Sí |
| REG-03 | T3 | TRA-4160-2893 | SPR-2504-185M | 08:21:50 | 08:27:58 | 6.1333 | — | — | Sí |

Cierre: 17.2167 min ÷ 3 = **5.7389 min**. Suma de las tres réplicas: 17.2167 min (1033 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-1019-5681 | — | 08:29:03 | 08:31:57 | 1.9000 (114 s) | 60 | P2 | Sí |
| VALE-02 | T5 | PEC-2026-1019-7170 | — | 08:31:57 | 08:33:56 | 1.9833 (119 s) | — | — | Sí |
| VALE-03 | T6 | PEC-2026-1019-9225 | — | 08:33:56 | 08:36:16 | 2.3333 (140 s) | — | — | Sí |

Cierre: 6.2166 min ÷ 3 = **2.0722 min**. Suma de las tres réplicas: 6.2166 min (373 s).

**Resumen del operador.** T_reg promedio: 5.7389 min · T_vale promedio: 2.0722 min · Réplicas válidas: 6 de 6.

---

### Bloque 25 · TRAB-13 · Pretest (proceso manual) · 08/09/2026

Centro de acopio: **Turpo** (4163) · Observador: **OBS-01**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4163-2233 | ROTA-2603-156K | 07:30:00 | 08:00:33 | 30.5500 | — | — | Sí |
| REG-02 | T2 | SAL-4163-2441 | SPR-2609-423M | 08:00:33 | 08:34:45 | 34.2000 | — | — | Sí |
| REG-03 | T3 | TRA-4163-3052 | NEUM-2507-181K | 08:34:45 | 09:13:00 | 37.2500 | 60 | P1 | Sí |

Cierre: 102.0000 min ÷ 3 = **34.0000 min**. Suma de las tres réplicas: 102.0000 min (6120 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-0908-4592 | — | 09:19:00 | 09:34:21 | 15.3500 | — | — | Sí |
| VALE-02 | T5 | PEC-2026-0908-6387 | — | 09:34:21 | 09:50:26 | 16.0833 | — | — | Sí |
| VALE-03 | T6 | PEC-2026-0908-9474 | — | 09:50:26 | 10:09:30 | 18.0667 | 60 | P2 | Sí |

Cierre: 49.5000 min ÷ 3 = **16.5000 min**. Suma de las tres réplicas: 49.5000 min (2970 s).

**Resumen del operador.** T_reg promedio: 34.0000 min · T_vale promedio: 16.5000 min · Réplicas válidas: 6 de 6.

---

### Bloque 26 · TRAB-13 · Postest (Sistema SIVAC) · 20/10/2026

Centro de acopio: **Turpo** (4163) · Observador: **OBS-01**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4163-1378 | NEUM-2506-884B | 08:00:00 | 08:05:00 | 5.0000 | — | — | Sí |
| REG-02 | T2 | SAL-4163-1486 | DTA-2602-797A | 08:05:00 | 08:10:33 | 5.5500 | — | — | Sí |
| REG-03 | T3 | TRA-4163-2010 | PENT-2504-482M | 08:10:33 | 08:16:35 | 6.0333 | — | — | Sí |

Cierre: 16.5833 min ÷ 3 = **5.5278 min**. Suma de las tres réplicas: 16.5833 min (995 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-1020-4170 | — | 08:18:46 | 08:20:49 | 2.0500 (123 s) | — | — | Sí |
| VALE-02 | T5 | PEC-2026-1020-7539 | — | 08:20:49 | 08:23:02 | 2.2167 (133 s) | — | — | Sí |
| VALE-03 | T6 | PEC-2026-1020-8607 | — | 08:23:02 | 08:26:35 | 2.5500 (153 s) | 60 | P2 | Sí |

Cierre: 6.8167 min ÷ 3 = **2.2722 min**. Suma de las tres réplicas: 6.8167 min (409 s).

**Resumen del operador.** T_reg promedio: 5.5278 min · T_vale promedio: 2.2722 min · Réplicas válidas: 6 de 6.

---

### Bloque 27 · TRAB-14 · Pretest (proceso manual) · 08/09/2026

Centro de acopio: **Kishuara** (4183) · Observador: **OBS-02**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4183-2534 | VARI-2607-979A | 07:15:00 | 07:48:56 | 31.4333 | 150 | P4 | Sí |
| REG-02 | T2 | SAL-4183-2603 | ROTA-2502-563B | 07:48:56 | 08:24:46 | 35.0833 | 45 | P4 | Sí |
| REG-03 | T3 | TRA-4183-3058 | DTA-2603-463K | 08:24:46 | 09:06:15 | 41.4833 | — | — | Sí |

Cierre: 107.9999 min ÷ 3 = **36.0000 min**. Suma de las tres réplicas: 107.9999 min (6480 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-0908-4747 | — | 09:12:25 | 09:31:21 | 16.4333 | 150 | P3 | Sí |
| VALE-02 | T5 | PEC-2026-0908-5346 | — | 09:31:21 | 09:48:55 | 17.5667 | — | — | Sí |
| VALE-03 | T6 | PEC-2026-0908-6228 | — | 09:48:55 | 10:08:10 | 18.5000 | 45 | P4 | Sí |

Cierre: 52.5000 min ÷ 3 = **17.5000 min**. Suma de las tres réplicas: 52.5000 min (3150 s).

**Resumen del operador.** T_reg promedio: 36.0000 min · T_vale promedio: 17.5000 min · Réplicas válidas: 6 de 6.

---

### Bloque 28 · TRAB-14 · Postest (Sistema SIVAC) · 20/10/2026

Centro de acopio: **Kishuara** (4183) · Observador: **OBS-02**

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | ING-4183-1022 | VARI-2509-637K | 07:50:00 | 07:54:59 | 4.9833 | — | — | Sí |
| REG-02 | T2 | SAL-4183-1680 | NEUM-2505-688A | 07:54:59 | 08:00:32 | 5.5500 | — | — | Sí |
| REG-03 | T3 | TRA-4183-2151 | ROTA-2603-156K | 08:00:32 | 08:06:53 | 6.3500 | — | — | Sí |

Cierre: 16.8833 min ÷ 3 = **5.6278 min**. Suma de las tres réplicas: 16.8833 min (1013 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Documento | Lote | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | PEC-2026-1020-5647 | — | 08:07:58 | 08:09:49 | 1.8500 (111 s) | — | — | Sí |
| VALE-02 | T5 | PEC-2026-1020-5665 | — | 08:09:49 | 08:11:47 | 1.9667 (118 s) | — | — | Sí |
| VALE-03 | T6 | PEC-2026-1020-7376 | — | 08:11:47 | 08:13:40 | 1.8833 (113 s) | — | — | Sí |

Cierre: 5.7000 min ÷ 3 = **1.9000 min**. Suma de las tres réplicas: 5.7000 min (342 s).

**Resumen del operador.** T_reg promedio: 5.6278 min · T_vale promedio: 1.9000 min · Réplicas válidas: 6 de 6.

---

---

<a id="parte-4"></a>
## Parte 4. Instrumento 2 — Ficha de auditoría documental y conciliación de entregas

Cada bloque audita cuarenta documentos sobre ocho criterios binarios y concilia veinticinco despachos. La conformidad documental es conjuntiva: un documento es conforme solo si cumple los ocho criterios. La tabla emplea S y N para abreviar Sí y No, y las columnas 1 a 8 siguen el orden de los aspectos del instrumento. El motivo se codifica de M1 a M8 y se imprime solo cuando el documento no es conforme; la última columna reproduce la observación del auditor, que en la ficha impresa se escribe en la celda «Motivo · Obs.». En las entregas, Dif. es la cantidad entregada menos la programada: el signo negativo señala faltante y el positivo, exceso; la entrega es concordante solo cuando la diferencia es cero.

**Convenciones.** ING: ingreso. SAL: salida. TRA: transferencia. DEV: devolución. AJU: ajuste. BCG, PENT, IPV, ROTA, NEUM, SPR, DTA, HEPB, INFL y VARI abrevian los biológicos del catálogo. M1 a M8 remiten a los ocho aspectos en el orden impreso.

### Bloque 1 · TRAB-01 · Pretest (proceso manual) · 10/08/2026

Centro de acopio: **ALMACÉN (CHANKA)** (CHANKA-001) · Auditor: **OBS-01** · Periodo auditado: **10/07/2026 al 09/08/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 10 · RSD 50.00 %.

Documentos auditados: 40 · Conformes: 25 · RSD: 62.50 % · Entregas conciliadas: 25 · Concordantes: 16 · CPE: 64.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 10/07/2026 | AJU | AJU-CHANKA001-0237 | HEPB | HEPB-2603-786K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 11/07/2026 | ING | ING-CHANKA001-0113 | ROTA | ROTA-2605-833M | 240 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 3 | 12/07/2026 | TRA | TRA-CHANKA001-0167 | INFL | INFL-2504-261K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 12/07/2026 | SAL | SAL-CHANKA001-0135 | IPV | IPV-2507-805M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 13/07/2026 | TRA | TRA-CHANKA001-0291 | SPR | SPR-2608-539M | 240 | S | S | S | S | N | S | S | S | N | M5 | Origen o destino consignado de forma incompleta. |
| 6 | 14/07/2026 | ING | ING-CHANKA001-0169 | SPR | SPR-2606-500M | 50 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 7 | 15/07/2026 | SAL | SAL-CHANKA001-0270 | VARI | VARI-2501-250M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 15/07/2026 | TRA | TRA-CHANKA001-0610 | ROTA | ROTA-2502-563B | 40 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 9 | 16/07/2026 | SAL | SAL-CHANKA001-0283 | DTA | DTA-2606-829K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 17/07/2026 | SAL | SAL-CHANKA001-0406 | PENT | PENT-2508-232M | 40 | S | S | S | S | N | S | S | S | N | M5 | Origen o destino consignado de forma incompleta. |
| 11 | 18/07/2026 | AJU | AJU-CHANKA001-0752 | DTA | DTA-2505-409K | 30 | N | S | S | S | S | S | S | N | N | M1+M8 | Biológico consignado no corresponde al frasco físico. |
| 12 | 18/07/2026 | AJU | AJU-CHANKA001-1406 | VARI | VARI-2607-979A | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 19/07/2026 | SAL | SAL-CHANKA001-0443 | HEPB | HEPB-2509-474M | 40 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 14 | 20/07/2026 | SAL | SAL-CHANKA001-0481 | INFL | INFL-2604-777M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 21/07/2026 | TRA | TRA-CHANKA001-0785 | IPV | IPV-2605-698M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 22/07/2026 | ING | ING-CHANKA001-0365 | NEUM | NEUM-2505-638K | 60 | S | S | N | S | S | S | N | S | N | M3+M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 17 | 22/07/2026 | ING | ING-CHANKA001-0559 | VARI | VARI-2508-818M | 180 | S | S | N | S | S | S | S | S | N | M3 | Fecha de vencimiento vencida o ilegible en el asiento. |
| 18 | 23/07/2026 | ING | ING-CHANKA001-0713 | PENT | PENT-2508-232M | 30 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 19 | 24/07/2026 | ING | ING-CHANKA001-1095 | HEPB | HEPB-2609-521M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 25/07/2026 | SAL | SAL-CHANKA001-0566 | HEPB | HEPB-2609-521M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 25/07/2026 | ING | ING-CHANKA001-1179 | HEPB | HEPB-2609-917M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 26/07/2026 | TRA | TRA-CHANKA001-0935 | PENT | PENT-2606-251M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 27/07/2026 | SAL | SAL-CHANKA001-0703 | SPR | SPR-2603-471K | 150 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 24 | 28/07/2026 | SAL | SAL-CHANKA001-0835 | SPR | SPR-2609-423M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 28/07/2026 | TRA | TRA-CHANKA001-1241 | VARI | VARI-2508-818M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 29/07/2026 | DEV | DEV-CHANKA001-0218 | ROTA | ROTA-2502-563B | 20 | S | S | S | S | S | N | N | S | N | M6+M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 27 | 30/07/2026 | SAL | SAL-CHANKA001-0874 | HEPB | HEPB-2602-318M | 60 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 28 | 31/07/2026 | SAL | SAL-CHANKA001-1130 | NEUM | NEUM-2505-638K | 300 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 29 | 01/08/2026 | AJU | AJU-CHANKA001-1666 | SPR | SPR-2606-500M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 01/08/2026 | SAL | SAL-CHANKA001-1156 | PENT | PENT-2606-391A | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 02/08/2026 | DEV | DEV-CHANKA001-0300 | SPR | SPR-2609-423M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 03/08/2026 | ING | ING-CHANKA001-1210 | SPR | SPR-2609-423M | 40 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 33 | 04/08/2026 | TRA | TRA-CHANKA001-1274 | ROTA | ROTA-2502-563B | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 04/08/2026 | SAL | SAL-CHANKA001-1420 | IPV | IPV-2503-662B | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 05/08/2026 | SAL | SAL-CHANKA001-1511 | NEUM | NEUM-2505-638K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 06/08/2026 | ING | ING-CHANKA001-1755 | DTA | DTA-2603-463K | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 07/08/2026 | ING | ING-CHANKA001-2701 | ROTA | ROTA-2507-417A | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 07/08/2026 | TRA | TRA-CHANKA001-1325 | ROTA | ROTA-2602-464A | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 08/08/2026 | DEV | DEV-CHANKA001-0490 | VARI | VARI-2509-637K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 09/08/2026 | SAL | SAL-CHANKA001-1829 | ROTA | ROTA-2602-464A | 60 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-01 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 24/07/2026 | CHANKA-001 | PENT | 50 | 50 | 0 | GR-CHANKA001-6241 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 2 | 28/07/2026 | CHANKA-001 | PENT | 150 | 150 | 0 | GR-CHANKA001-4432 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 3 | 13/07/2026 | CHANKA-001 | DTA | 150 | 150 | 0 | GR-CHANKA001-3735 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 4 | 03/08/2026 | CHANKA-001 | BCG | 180 | 185 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 5 | 24/07/2026 | CHANKA-001 | IPV | 150 | 150 | 0 | GR-CHANKA001-3108 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 6 | 20/07/2026 | CHANKA-001 | HEPB | 80 | 80 | 0 | GR-CHANKA001-1676 | Sí | Conforme. Cantidad y guía coinciden. |
| 7 | 26/07/2026 | CHANKA-001 | VARI | 120 | 120 | 0 | GR-CHANKA001-2127 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 8 | 29/07/2026 | CHANKA-001 | NEUM | 120 | 110 | -10 | GR-CHANKA001-7575 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 9 | 09/08/2026 | CHANKA-001 | DTA | 200 | 200 | 0 | GR-CHANKA001-2202 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 10 | 01/08/2026 | CHANKA-001 | NEUM | 30 | 25 | -5 | GR-CHANKA001-9318 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 11 | 13/07/2026 | CHANKA-001 | VARI | 200 | 210 | 10 | GR-CHANKA001-8494 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 12 | 09/08/2026 | CHANKA-001 | INFL | 100 | 100 | 0 | GR-CHANKA001-2987 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 15/07/2026 | CHANKA-001 | DTA | 100 | 100 | 0 | GR-CHANKA001-4034 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 14 | 17/07/2026 | CHANKA-001 | BCG | 100 | 100 | 0 | GR-CHANKA001-5666 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 15 | 23/07/2026 | CHANKA-001 | VARI | 200 | 200 | 0 | GR-CHANKA001-4055 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 16 | 07/08/2026 | CHANKA-001 | HEPB | 30 | 30 | 0 | GR-CHANKA001-5775 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 17 | 28/07/2026 | CHANKA-001 | HEPB | 80 | 80 | 0 | GR-CHANKA001-6660 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 18 | 22/07/2026 | CHANKA-001 | NEUM | 80 | 80 | 0 | GR-CHANKA001-8468 | Sí | Conforme. Cantidad y guía coinciden. |
| 19 | 05/08/2026 | CHANKA-001 | SPR | 180 | 175 | -5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 20 | 28/07/2026 | CHANKA-001 | INFL | 120 | 110 | -10 | GR-CHANKA001-2123 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 21 | 21/07/2026 | CHANKA-001 | INFL | 180 | 170 | -10 | GR-CHANKA001-5216 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 22 | 23/07/2026 | CHANKA-001 | PENT | 180 | 180 | 0 | GR-CHANKA001-7823 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 23 | 07/08/2026 | CHANKA-001 | ROTA | 60 | 50 | -10 | GR-CHANKA001-4330 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 24 | 31/07/2026 | CHANKA-001 | VARI | 40 | 40 | 0 | GR-CHANKA001-1877 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 25 | 05/08/2026 | CHANKA-001 | IPV | 20 | 25 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |

Cierre: 16 entregas concordantes ÷ 25 × 100 = **64.00 %**.

---

### Bloque 2 · TRAB-01 · Postest (Sistema SIVAC) · 12/10/2026

Centro de acopio: **ALMACÉN (CHANKA)** (CHANKA-001) · Auditor: **OBS-01** · Periodo auditado: **14/09/2026 al 11/10/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 19 · RSD 95.00 %.

Documentos auditados: 40 · Conformes: 38 · RSD: 95.00 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 14/09/2026 | ING | ING-CHANKA001-0256 | NEUM | NEUM-2505-638K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 15/09/2026 | SAL | SAL-CHANKA001-0111 | NEUM | NEUM-2506-884B | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 15/09/2026 | ING | ING-CHANKA001-0393 | DTA | DTA-2603-463K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 16/09/2026 | TRA | TRA-CHANKA001-0373 | IPV | IPV-2605-698M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 17/09/2026 | ING | ING-CHANKA001-0469 | INFL | INFL-2508-359M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 17/09/2026 | TRA | TRA-CHANKA001-0436 | ROTA | ROTA-2502-563B | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 18/09/2026 | SAL | SAL-CHANKA001-0158 | HEPB | HEPB-2609-521M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 19/09/2026 | TRA | TRA-CHANKA001-0585 | NEUM | NEUM-2507-181K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 20/09/2026 | AJU | AJU-CHANKA001-0394 | HEPB | HEPB-2509-474M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 20/09/2026 | AJU | AJU-CHANKA001-0488 | BCG | BCG-2507-694K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 21/09/2026 | SAL | SAL-CHANKA001-0371 | HEPB | HEPB-2609-521M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 22/09/2026 | ING | ING-CHANKA001-0949 | BCG | BCG-2504-789B | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 22/09/2026 | AJU | AJU-CHANKA001-1117 | BCG | BCG-2606-808K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 23/09/2026 | AJU | AJU-CHANKA001-1132 | NEUM | NEUM-2506-884B | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 24/09/2026 | TRA | TRA-CHANKA001-0666 | SPR | SPR-2608-539M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 24/09/2026 | AJU | AJU-CHANKA001-1322 | INFL | INFL-2607-737M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 25/09/2026 | ING | ING-CHANKA001-1164 | SPR | SPR-2606-500M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 26/09/2026 | ING | ING-CHANKA001-1189 | PENT | PENT-2606-251M | 40 | S | N | S | S | N | S | S | S | N | M2+M5 | Lote digitado con un dígito trocado; se subsanó en el sistema. |
| 19 | 26/09/2026 | TRA | TRA-CHANKA001-1119 | VARI | VARI-2503-521A | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 27/09/2026 | ING | ING-CHANKA001-1383 | BCG | BCG-2607-654A | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 28/09/2026 | ING | ING-CHANKA001-1660 | BCG | BCG-2504-789B | 60 | S | S | S | S | S | S | N | S | N | M7 | Saldo no recalculado tras un ajuste autorizado. |
| 22 | 29/09/2026 | DEV | DEV-CHANKA001-0484 | ROTA | ROTA-2502-563B | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 29/09/2026 | AJU | AJU-CHANKA001-1332 | SPR | SPR-2609-423M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 30/09/2026 | SAL | SAL-CHANKA001-0546 | BCG | BCG-2606-808K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 01/10/2026 | SAL | SAL-CHANKA001-0639 | DTA | DTA-2602-236K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 01/10/2026 | DEV | DEV-CHANKA001-0651 | BCG | BCG-2507-694K | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 02/10/2026 | TRA | TRA-CHANKA001-1253 | INFL | INFL-2508-359M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 03/10/2026 | ING | ING-CHANKA001-1708 | INFL | INFL-2504-261K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 03/10/2026 | SAL | SAL-CHANKA001-0688 | SPR | SPR-2504-185M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 04/10/2026 | DEV | DEV-CHANKA001-0954 | HEPB | HEPB-2509-474M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 05/10/2026 | ING | ING-CHANKA001-1724 | DTA | DTA-2505-409K | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 05/10/2026 | ING | ING-CHANKA001-1733 | HEPB | HEPB-2602-318M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 06/10/2026 | SAL | SAL-CHANKA001-1209 | ROTA | ROTA-2507-417A | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 07/10/2026 | ING | ING-CHANKA001-1819 | SPR | SPR-2609-423M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 08/10/2026 | ING | ING-CHANKA001-1910 | IPV | IPV-2605-698M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 08/10/2026 | ING | ING-CHANKA001-2042 | VARI | VARI-2508-818M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 09/10/2026 | SAL | SAL-CHANKA001-1357 | BCG | BCG-2607-654A | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 10/10/2026 | TRA | TRA-CHANKA001-1345 | BCG | BCG-2504-789B | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 10/10/2026 | SAL | SAL-CHANKA001-1443 | INFL | INFL-2604-777M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 11/10/2026 | ING | ING-CHANKA001-2752 | INFL | INFL-2607-737M | 180 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-01 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 11/10/2026 | CHANKA-001 | HEPB | 200 | 200 | 0 | GR-CHANKA001-4781 | Sí | Conforme. Cantidad y guía coinciden. |
| 2 | 29/09/2026 | CHANKA-001 | BCG | 30 | 30 | 0 | GR-CHANKA001-1850 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 3 | 22/09/2026 | CHANKA-001 | INFL | 20 | 20 | 0 | GR-CHANKA001-2190 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 4 | 09/10/2026 | CHANKA-001 | NEUM | 150 | 150 | 0 | GR-CHANKA001-7585 | Sí | Conforme. Cantidad y guía coinciden. |
| 5 | 07/10/2026 | CHANKA-001 | NEUM | 50 | 50 | 0 | GR-CHANKA001-8026 | Sí | Conforme. Cantidad y guía coinciden. |
| 6 | 16/09/2026 | CHANKA-001 | PENT | 60 | 60 | 0 | GR-CHANKA001-2923 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 7 | 14/09/2026 | CHANKA-001 | INFL | 100 | 100 | 0 | GR-CHANKA001-1722 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 8 | 23/09/2026 | CHANKA-001 | NEUM | 120 | 120 | 0 | GR-CHANKA001-7582 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 9 | 25/09/2026 | CHANKA-001 | SPR | 180 | 180 | 0 | GR-CHANKA001-8022 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 10 | 28/09/2026 | CHANKA-001 | HEPB | 20 | 20 | 0 | GR-CHANKA001-7345 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 11 | 23/09/2026 | CHANKA-001 | INFL | 80 | 80 | 0 | GR-CHANKA001-4497 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 12 | 14/09/2026 | CHANKA-001 | INFL | 80 | 80 | 0 | GR-CHANKA001-3941 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 13 | 10/10/2026 | CHANKA-001 | IPV | 50 | 50 | 0 | GR-CHANKA001-1210 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 14 | 18/09/2026 | CHANKA-001 | INFL | 20 | 20 | 0 | GR-CHANKA001-3023 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 15 | 11/10/2026 | CHANKA-001 | HEPB | 80 | 80 | 0 | GR-CHANKA001-3579 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 16 | 17/09/2026 | CHANKA-001 | SPR | 50 | 50 | 0 | GR-CHANKA001-3955 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 17 | 22/09/2026 | CHANKA-001 | SPR | 180 | 175 | -5 | GR-CHANKA001-5298 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 18 | 08/10/2026 | CHANKA-001 | DTA | 80 | 80 | 0 | GR-CHANKA001-2736 | Sí | Conforme. Cantidad y guía coinciden. |
| 19 | 28/09/2026 | CHANKA-001 | IPV | 40 | 40 | 0 | GR-CHANKA001-7712 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 20 | 30/09/2026 | CHANKA-001 | DTA | 50 | 50 | 0 | GR-CHANKA001-9653 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 21 | 11/10/2026 | CHANKA-001 | PENT | 60 | 60 | 0 | GR-CHANKA001-8780 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 22 | 02/10/2026 | CHANKA-001 | INFL | 180 | 180 | 0 | GR-CHANKA001-5902 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 23 | 17/09/2026 | CHANKA-001 | VARI | 20 | 20 | 0 | GR-CHANKA001-4982 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 24 | 07/10/2026 | CHANKA-001 | ROTA | 150 | 150 | 0 | GR-CHANKA001-4411 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 25 | 30/09/2026 | CHANKA-001 | INFL | 150 | 150 | 0 | GR-CHANKA001-5857 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 3 · TRAB-02 · Pretest (proceso manual) · 10/08/2026

Centro de acopio: **ALMACÉN (CHANKA)** (CHANKA-001) · Auditor: **OBS-02** · Periodo auditado: **13/07/2026 al 09/08/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 11 · RSD 55.00 %.

Documentos auditados: 40 · Conformes: 23 · RSD: 57.50 % · Entregas conciliadas: 25 · Concordantes: 16 · CPE: 64.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 13/07/2026 | TRA | TRA-CHANKA001-0204 | BCG | BCG-2606-808K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 14/07/2026 | DEV | DEV-CHANKA001-0237 | ROTA | ROTA-2605-833M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 14/07/2026 | ING | ING-CHANKA001-0313 | INFL | INFL-2508-359M | 240 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 4 | 15/07/2026 | ING | ING-CHANKA001-0378 | VARI | VARI-2509-637K | 20 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 5 | 16/07/2026 | SAL | SAL-CHANKA001-0375 | VARI | VARI-2508-818M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 16/07/2026 | ING | ING-CHANKA001-0464 | DTA | DTA-2505-409K | 200 | N | S | S | S | S | S | S | S | N | M1 | Biológico consignado no corresponde al frasco físico. |
| 7 | 17/07/2026 | ING | ING-CHANKA001-0703 | INFL | INFL-2604-777M | 300 | S | S | S | N | S | N | S | S | N | M4+M6 | Asiento sin firma del responsable del almacén. |
| 8 | 18/07/2026 | SAL | SAL-CHANKA001-0920 | VARI | VARI-2509-637K | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 19/07/2026 | ING | ING-CHANKA001-0706 | NEUM | NEUM-2506-884B | 300 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 10 | 19/07/2026 | SAL | SAL-CHANKA001-1384 | DTA | DTA-2505-409K | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 20/07/2026 | ING | ING-CHANKA001-1098 | SPR | SPR-2609-423M | 240 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 12 | 21/07/2026 | AJU | AJU-CHANKA001-0189 | HEPB | HEPB-2609-917M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 21/07/2026 | TRA | TRA-CHANKA001-0838 | IPV | IPV-2605-698M | 30 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 14 | 22/07/2026 | SAL | SAL-CHANKA001-1683 | SPR | SPR-2603-471K | 240 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 15 | 23/07/2026 | TRA | TRA-CHANKA001-1138 | SPR | SPR-2504-185M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 23/07/2026 | SAL | SAL-CHANKA001-1694 | PENT | PENT-2605-322M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 24/07/2026 | ING | ING-CHANKA001-1240 | HEPB | HEPB-2609-917M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 25/07/2026 | ING | ING-CHANKA001-1558 | NEUM | NEUM-2505-688A | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 25/07/2026 | SAL | SAL-CHANKA001-1755 | IPV | IPV-2608-446B | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 26/07/2026 | ING | ING-CHANKA001-1607 | INFL | INFL-2603-792B | 40 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 21 | 27/07/2026 | ING | ING-CHANKA001-1654 | ROTA | ROTA-2603-156K | 300 | S | N | S | S | S | N | S | S | N | M2+M6 | Asiento sin firma del responsable del almacén. |
| 22 | 28/07/2026 | SAL | SAL-CHANKA001-1817 | INFL | INFL-2504-261K | 50 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 23 | 28/07/2026 | SAL | SAL-CHANKA001-2038 | IPV | IPV-2507-805M | 300 | S | S | S | N | S | S | S | S | N | M4 | Cantidad física menor a la registrada en el asiento. |
| 24 | 29/07/2026 | DEV | DEV-CHANKA001-0659 | PENT | PENT-2504-482M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 30/07/2026 | SAL | SAL-CHANKA001-2399 | NEUM | NEUM-2507-181K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 30/07/2026 | ING | ING-CHANKA001-1803 | IPV | IPV-2507-805M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 31/07/2026 | SAL | SAL-CHANKA001-2753 | INFL | INFL-2508-359M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 01/08/2026 | ING | ING-CHANKA001-1845 | PENT | PENT-2606-391A | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 01/08/2026 | SAL | SAL-CHANKA001-2827 | NEUM | NEUM-2505-638K | 100 | S | N | S | S | S | N | S | S | N | M2+M6 | Asiento sin firma del responsable del almacén. |
| 30 | 02/08/2026 | ING | ING-CHANKA001-1847 | ROTA | ROTA-2603-156K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 03/08/2026 | SAL | SAL-CHANKA001-3185 | ROTA | ROTA-2605-833M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 03/08/2026 | AJU | AJU-CHANKA001-0717 | SPR | SPR-2606-500M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 04/08/2026 | SAL | SAL-CHANKA001-3395 | HEPB | HEPB-2509-474M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 05/08/2026 | TRA | TRA-CHANKA001-1367 | INFL | INFL-2504-261K | 100 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 35 | 06/08/2026 | TRA | TRA-CHANKA001-1474 | HEPB | HEPB-2509-474M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 06/08/2026 | TRA | TRA-CHANKA001-1794 | HEPB | HEPB-2609-521M | 180 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 37 | 07/08/2026 | TRA | TRA-CHANKA001-2239 | ROTA | ROTA-2605-833M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 08/08/2026 | SAL | SAL-CHANKA001-3950 | VARI | VARI-2503-521A | 40 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 39 | 08/08/2026 | ING | ING-CHANKA001-1890 | NEUM | NEUM-2509-952A | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 09/08/2026 | ING | ING-CHANKA001-2266 | DTA | DTA-2505-409K | 300 | N | N | S | S | S | S | S | S | N | M1+M2 | Lote del kardex no coincide con el rotulado del frasco. |

**Entregas conciliadas — TRAB-02 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 08/08/2026 | CHANKA-001 | PENT | 60 | 50 | -10 | GR-CHANKA001-1391 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 2 | 08/08/2026 | CHANKA-001 | SPR | 180 | 180 | 0 | GR-CHANKA001-4527 | Sí | Conforme. Cantidad y guía coinciden. |
| 3 | 07/08/2026 | CHANKA-001 | BCG | 50 | 45 | -5 | GR-CHANKA001-6852 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 4 | 17/07/2026 | CHANKA-001 | PENT | 40 | 35 | -5 | GR-CHANKA001-3436 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 5 | 25/07/2026 | CHANKA-001 | SPR | 150 | 150 | 0 | GR-CHANKA001-8093 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 6 | 23/07/2026 | CHANKA-001 | IPV | 30 | 30 | 0 | GR-CHANKA001-6827 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 7 | 16/07/2026 | CHANKA-001 | BCG | 180 | 175 | -5 | GR-CHANKA001-4192 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 8 | 22/07/2026 | CHANKA-001 | NEUM | 30 | 30 | 0 | GR-CHANKA001-4466 | Sí | Conforme. Cantidad y guía coinciden. |
| 9 | 17/07/2026 | CHANKA-001 | DTA | 100 | 100 | 0 | GR-CHANKA001-3315 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 10 | 13/07/2026 | CHANKA-001 | SPR | 80 | 80 | 0 | GR-CHANKA001-8065 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 11 | 23/07/2026 | CHANKA-001 | SPR | 80 | 80 | 0 | GR-CHANKA001-9786 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 12 | 13/07/2026 | CHANKA-001 | NEUM | 40 | 40 | 0 | GR-CHANKA001-6745 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 13 | 31/07/2026 | CHANKA-001 | BCG | 20 | 15 | -5 | GR-CHANKA001-8464 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 14 | 14/07/2026 | CHANKA-001 | INFL | 20 | 20 | 0 | GR-CHANKA001-7586 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 15 | 07/08/2026 | CHANKA-001 | INFL | 200 | 195 | -5 | GR-CHANKA001-6078 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 16 | 28/07/2026 | CHANKA-001 | SPR | 80 | 85 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 17 | 14/07/2026 | CHANKA-001 | DTA | 40 | 40 | 0 | GR-CHANKA001-7464 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 18 | 29/07/2026 | CHANKA-001 | INFL | 60 | 60 | 0 | GR-CHANKA001-5236 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 19 | 02/08/2026 | CHANKA-001 | INFL | 30 | 30 | 0 | GR-CHANKA001-6589 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 20 | 07/08/2026 | CHANKA-001 | ROTA | 40 | 40 | 0 | GR-CHANKA001-4368 | Sí | Conforme. Cantidad y guía coinciden. |
| 21 | 17/07/2026 | CHANKA-001 | ROTA | 200 | 200 | 0 | GR-CHANKA001-3382 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 22 | 23/07/2026 | CHANKA-001 | ROTA | 100 | 100 | 0 | GR-CHANKA001-2232 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 23 | 30/07/2026 | CHANKA-001 | NEUM | 30 | 20 | -10 | GR-CHANKA001-8955 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 24 | 05/08/2026 | CHANKA-001 | NEUM | 200 | 200 | 0 | GR-CHANKA001-8622 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 25 | 20/07/2026 | CHANKA-001 | PENT | 40 | 45 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |

Cierre: 16 entregas concordantes ÷ 25 × 100 = **64.00 %**.

---

### Bloque 4 · TRAB-02 · Postest (Sistema SIVAC) · 12/10/2026

Centro de acopio: **ALMACÉN (CHANKA)** (CHANKA-001) · Auditor: **OBS-02** · Periodo auditado: **09/09/2026 al 11/10/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 19 · RSD 95.00 %.

Documentos auditados: 40 · Conformes: 39 · RSD: 97.50 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 09/09/2026 | TRA | TRA-CHANKA001-0442 | ROTA | ROTA-2507-417A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 10/09/2026 | SAL | SAL-CHANKA001-0224 | PENT | PENT-2605-322M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 11/09/2026 | SAL | SAL-CHANKA001-0686 | PENT | PENT-2606-391A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 11/09/2026 | DEV | DEV-CHANKA001-0265 | INFL | INFL-2607-737M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 12/09/2026 | ING | ING-CHANKA001-0340 | DTA | DTA-2602-236K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 13/09/2026 | DEV | DEV-CHANKA001-0909 | DTA | DTA-2602-797A | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 14/09/2026 | TRA | TRA-CHANKA001-0498 | ROTA | ROTA-2507-417A | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 15/09/2026 | SAL | SAL-CHANKA001-1026 | INFL | INFL-2603-792B | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 16/09/2026 | TRA | TRA-CHANKA001-0549 | PENT | PENT-2504-482M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 16/09/2026 | DEV | DEV-CHANKA001-1507 | HEPB | HEPB-2509-474M | 200 | N | S | S | S | S | S | S | N | N | M1+M8 | Correlativo duplicado por reintento de grabación. |
| 11 | 17/09/2026 | DEV | DEV-CHANKA001-1515 | IPV | IPV-2608-446B | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 18/09/2026 | SAL | SAL-CHANKA001-1385 | SPR | SPR-2606-500M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 19/09/2026 | SAL | SAL-CHANKA001-1412 | DTA | DTA-2602-236K | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 20/09/2026 | SAL | SAL-CHANKA001-1876 | ROTA | ROTA-2605-833M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 20/09/2026 | AJU | AJU-CHANKA001-0989 | IPV | IPV-2504-587B | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 21/09/2026 | SAL | SAL-CHANKA001-2035 | ROTA | ROTA-2507-417A | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 22/09/2026 | ING | ING-CHANKA001-0489 | HEPB | HEPB-2509-474M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 23/09/2026 | ING | ING-CHANKA001-0654 | INFL | INFL-2508-359M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 24/09/2026 | ING | ING-CHANKA001-0977 | DTA | DTA-2602-236K | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 25/09/2026 | DEV | DEV-CHANKA001-1601 | PENT | PENT-2606-251M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 25/09/2026 | SAL | SAL-CHANKA001-2048 | INFL | INFL-2508-359M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 26/09/2026 | AJU | AJU-CHANKA001-1150 | VARI | VARI-2508-818M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 27/09/2026 | ING | ING-CHANKA001-1034 | ROTA | ROTA-2602-464A | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 28/09/2026 | ING | ING-CHANKA001-1249 | SPR | SPR-2609-423M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 29/09/2026 | SAL | SAL-CHANKA001-2214 | SPR | SPR-2609-423M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 30/09/2026 | ING | ING-CHANKA001-1561 | NEUM | NEUM-2509-952A | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 30/09/2026 | SAL | SAL-CHANKA001-2446 | DTA | DTA-2602-236K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 01/10/2026 | ING | ING-CHANKA001-2556 | DTA | DTA-2606-829K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 02/10/2026 | SAL | SAL-CHANKA001-2624 | BCG | BCG-2507-694K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 03/10/2026 | SAL | SAL-CHANKA001-2653 | BCG | BCG-2607-654A | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 04/10/2026 | SAL | SAL-CHANKA001-2658 | INFL | INFL-2508-359M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 04/10/2026 | SAL | SAL-CHANKA001-2669 | SPR | SPR-2608-539M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 05/10/2026 | SAL | SAL-CHANKA001-3230 | HEPB | HEPB-2609-917M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 06/10/2026 | SAL | SAL-CHANKA001-3752 | HEPB | HEPB-2602-318M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 07/10/2026 | DEV | DEV-CHANKA001-2022 | ROTA | ROTA-2602-464A | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 08/10/2026 | SAL | SAL-CHANKA001-3893 | IPV | IPV-2507-805M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 09/10/2026 | ING | ING-CHANKA001-2865 | IPV | IPV-2605-698M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 09/10/2026 | DEV | DEV-CHANKA001-2330 | BCG | BCG-2504-789B | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 10/10/2026 | ING | ING-CHANKA001-3302 | BCG | BCG-2507-694K | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 11/10/2026 | TRA | TRA-CHANKA001-0586 | SPR | SPR-2504-185M | 50 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-02 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 15/09/2026 | CHANKA-001 | BCG | 120 | 120 | 0 | GR-CHANKA001-1288 | Sí | Conforme. Cantidad y guía coinciden. |
| 2 | 14/09/2026 | CHANKA-001 | SPR | 80 | 80 | 0 | GR-CHANKA001-6127 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 3 | 30/09/2026 | CHANKA-001 | NEUM | 80 | 80 | 0 | GR-CHANKA001-4433 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 4 | 22/09/2026 | CHANKA-001 | BCG | 180 | 180 | 0 | GR-CHANKA001-5996 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 5 | 19/09/2026 | CHANKA-001 | IPV | 20 | 15 | -5 | GR-CHANKA001-2687 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 6 | 28/09/2026 | CHANKA-001 | NEUM | 20 | 20 | 0 | GR-CHANKA001-4728 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 7 | 29/09/2026 | CHANKA-001 | HEPB | 60 | 60 | 0 | GR-CHANKA001-7151 | Sí | Conforme. Cantidad y guía coinciden. |
| 8 | 15/09/2026 | CHANKA-001 | INFL | 200 | 200 | 0 | GR-CHANKA001-5188 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 9 | 05/10/2026 | CHANKA-001 | VARI | 100 | 100 | 0 | GR-CHANKA001-3977 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 10 | 14/09/2026 | CHANKA-001 | VARI | 120 | 120 | 0 | GR-CHANKA001-4824 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 11 | 19/09/2026 | CHANKA-001 | HEPB | 100 | 100 | 0 | GR-CHANKA001-4811 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 12 | 14/09/2026 | CHANKA-001 | BCG | 30 | 30 | 0 | GR-CHANKA001-5989 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 13 | 07/10/2026 | CHANKA-001 | PENT | 150 | 150 | 0 | GR-CHANKA001-4803 | Sí | Conforme. Cantidad y guía coinciden. |
| 14 | 26/09/2026 | CHANKA-001 | IPV | 30 | 30 | 0 | GR-CHANKA001-4098 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 15 | 07/10/2026 | CHANKA-001 | HEPB | 200 | 200 | 0 | GR-CHANKA001-2919 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 16 | 16/09/2026 | CHANKA-001 | BCG | 80 | 80 | 0 | GR-CHANKA001-1862 | Sí | Conforme. Cantidad y guía coinciden. |
| 17 | 18/09/2026 | CHANKA-001 | DTA | 30 | 30 | 0 | GR-CHANKA001-3910 | Sí | Conforme. Cantidad y guía coinciden. |
| 18 | 17/09/2026 | CHANKA-001 | SPR | 30 | 30 | 0 | GR-CHANKA001-3523 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 19 | 06/10/2026 | CHANKA-001 | DTA | 40 | 40 | 0 | GR-CHANKA001-5900 | Sí | Conforme. Cantidad y guía coinciden. |
| 20 | 11/10/2026 | CHANKA-001 | HEPB | 150 | 150 | 0 | GR-CHANKA001-9114 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 21 | 25/09/2026 | CHANKA-001 | VARI | 120 | 120 | 0 | GR-CHANKA001-4193 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 22 | 22/09/2026 | CHANKA-001 | PENT | 150 | 150 | 0 | GR-CHANKA001-6155 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 23 | 22/09/2026 | CHANKA-001 | HEPB | 50 | 50 | 0 | GR-CHANKA001-3771 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 24 | 28/09/2026 | CHANKA-001 | DTA | 40 | 40 | 0 | GR-CHANKA001-7426 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 25 | 01/10/2026 | CHANKA-001 | HEPB | 150 | 150 | 0 | GR-CHANKA001-3253 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 5 · TRAB-03 · Pretest (proceso manual) · 11/08/2026

Centro de acopio: **Hospital Andahuaylas** (S/C) · Auditor: **OBS-01** · Periodo auditado: **15/07/2026 al 10/08/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 14 · RSD 70.00 %.

Documentos auditados: 40 · Conformes: 26 · RSD: 65.00 % · Entregas conciliadas: 25 · Concordantes: 18 · CPE: 72.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 16/07/2026 | TRA | TRA-SC-0382 | INFL | INFL-2508-359M | 150 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 2 | 17/07/2026 | SAL | SAL-SC-0232 | SPR | SPR-2603-471K | 100 | N | S | S | S | N | S | S | S | N | M1+M5 | Biológico consignado no corresponde al frasco físico. |
| 3 | 17/07/2026 | SAL | SAL-SC-0740 | INFL | INFL-2504-261K | 300 | S | S | N | S | S | N | S | S | N | M3+M6 | Asiento sin firma del responsable del almacén. |
| 4 | 18/07/2026 | ING | ING-SC-0408 | BCG | BCG-2606-296K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 19/07/2026 | AJU | AJU-SC-0886 | NEUM | NEUM-2505-688A | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 19/07/2026 | DEV | DEV-SC-0319 | ROTA | ROTA-2605-833M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 20/07/2026 | ING | ING-SC-0461 | VARI | VARI-2607-979A | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 20/07/2026 | DEV | DEV-SC-0345 | HEPB | HEPB-2609-521M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 21/07/2026 | TRA | TRA-SC-0545 | SPR | SPR-2609-423M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 22/07/2026 | SAL | SAL-SC-1244 | ROTA | ROTA-2602-464A | 100 | S | S | N | S | S | S | S | S | N | M3 | Fecha de vencimiento vencida o ilegible en el asiento. |
| 11 | 22/07/2026 | SAL | SAL-SC-1479 | INFL | INFL-2508-359M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 23/07/2026 | SAL | SAL-SC-1499 | BCG | BCG-2507-694K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 24/07/2026 | TRA | TRA-SC-0961 | ROTA | ROTA-2507-417A | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 24/07/2026 | TRA | TRA-SC-0968 | SPR | SPR-2608-539M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 25/07/2026 | ING | ING-SC-0714 | DTA | DTA-2606-829K | 120 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 16 | 26/07/2026 | SAL | SAL-SC-1955 | VARI | VARI-2607-979A | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 26/07/2026 | SAL | SAL-SC-2008 | HEPB | HEPB-2609-917M | 200 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 18 | 27/07/2026 | SAL | SAL-SC-2220 | VARI | VARI-2607-979A | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 28/07/2026 | SAL | SAL-SC-2928 | HEPB | HEPB-2509-474M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 28/07/2026 | SAL | SAL-SC-3227 | HEPB | HEPB-2609-521M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 29/07/2026 | TRA | TRA-SC-1073 | IPV | IPV-2504-587B | 100 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 22 | 29/07/2026 | SAL | SAL-SC-3473 | IPV | IPV-2504-587B | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 30/07/2026 | DEV | DEV-SC-0367 | BCG | BCG-2606-296K | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 31/07/2026 | ING | ING-SC-1274 | DTA | DTA-2602-797A | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 31/07/2026 | SAL | SAL-SC-3591 | PENT | PENT-2606-251M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 01/08/2026 | AJU | AJU-SC-0941 | BCG | BCG-2606-296K | 30 | S | S | N | S | S | N | S | S | N | M3+M6 | Asiento sin firma del responsable del almacén. |
| 27 | 02/08/2026 | ING | ING-SC-1597 | VARI | VARI-2501-250M | 60 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 28 | 02/08/2026 | TRA | TRA-SC-1643 | DTA | DTA-2602-236K | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 03/08/2026 | SAL | SAL-SC-3825 | DTA | DTA-2606-829K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 04/08/2026 | ING | ING-SC-1625 | VARI | VARI-2509-637K | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 04/08/2026 | DEV | DEV-SC-0381 | INFL | INFL-2603-792B | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 05/08/2026 | AJU | AJU-SC-1177 | NEUM | NEUM-2506-884B | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 06/08/2026 | TRA | TRA-SC-1722 | HEPB | HEPB-2609-917M | 60 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 34 | 06/08/2026 | SAL | SAL-SC-4072 | IPV | IPV-2504-587B | 200 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 35 | 07/08/2026 | SAL | SAL-SC-4188 | BCG | BCG-2606-808K | 40 | S | S | N | S | S | S | S | S | N | M3 | Fecha de vencimiento vencida o ilegible en el asiento. |
| 36 | 07/08/2026 | TRA | TRA-SC-1825 | INFL | INFL-2603-792B | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 08/08/2026 | SAL | SAL-SC-4690 | DTA | DTA-2602-797A | 40 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 38 | 09/08/2026 | SAL | SAL-SC-4698 | NEUM | NEUM-2506-884B | 240 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 39 | 09/08/2026 | SAL | SAL-SC-4729 | IPV | IPV-2507-805M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 10/08/2026 | SAL | SAL-SC-4745 | DTA | DTA-2603-463K | 20 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-03 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 30/07/2026 | S/C | SPR | 50 | 50 | 0 | GR-SC-4248 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 2 | 10/08/2026 | S/C | PENT | 150 | 150 | 0 | GR-SC-9647 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 3 | 28/07/2026 | S/C | NEUM | 30 | 30 | 0 | GR-SC-2504 | Sí | Conforme. Cantidad y guía coinciden. |
| 4 | 08/08/2026 | S/C | ROTA | 120 | 120 | 0 | GR-SC-9062 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 5 | 19/07/2026 | S/C | SPR | 120 | 110 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 6 | 25/07/2026 | S/C | SPR | 100 | 100 | 0 | GR-SC-9684 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 7 | 02/08/2026 | S/C | IPV | 20 | 20 | 0 | GR-SC-9449 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 8 | 05/08/2026 | S/C | INFL | 30 | 30 | 0 | GR-SC-3368 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 9 | 24/07/2026 | S/C | HEPB | 30 | 30 | 0 | GR-SC-5066 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 10 | 04/08/2026 | S/C | DTA | 20 | 40 | 20 | GR-SC-8635 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 11 | 29/07/2026 | S/C | PENT | 200 | 200 | 0 | GR-SC-9222 | Sí | Conforme. Cantidad y guía coinciden. |
| 12 | 28/07/2026 | S/C | ROTA | 200 | 200 | 0 | GR-SC-2905 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 27/07/2026 | S/C | SPR | 120 | 125 | 5 | GR-SC-7390 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 14 | 18/07/2026 | S/C | DTA | 100 | 100 | 0 | GR-SC-2580 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 15 | 10/08/2026 | S/C | DTA | 100 | 100 | 0 | GR-SC-1707 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 16 | 15/07/2026 | S/C | INFL | 120 | 115 | -5 | GR-SC-1956 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 17 | 29/07/2026 | S/C | HEPB | 100 | 100 | 0 | GR-SC-7610 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 18 | 31/07/2026 | S/C | IPV | 180 | 180 | 0 | GR-SC-9332 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 19 | 25/07/2026 | S/C | IPV | 100 | 90 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 20 | 24/07/2026 | S/C | DTA | 40 | 60 | 20 | GR-SC-5940 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 21 | 26/07/2026 | S/C | BCG | 50 | 50 | 0 | GR-SC-4901 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 22 | 09/08/2026 | S/C | ROTA | 100 | 100 | 0 | GR-SC-9309 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 23 | 17/07/2026 | S/C | SPR | 50 | 40 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 24 | 15/07/2026 | S/C | PENT | 40 | 40 | 0 | GR-SC-3636 | Sí | Conforme. Cantidad y guía coinciden. |
| 25 | 10/08/2026 | S/C | HEPB | 200 | 200 | 0 | GR-SC-2525 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |

Cierre: 18 entregas concordantes ÷ 25 × 100 = **72.00 %**.

---

### Bloque 6 · TRAB-03 · Postest (Sistema SIVAC) · 13/10/2026

Centro de acopio: **Hospital Andahuaylas** (S/C) · Auditor: **OBS-01** · Periodo auditado: **14/09/2026 al 12/10/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 19 · RSD 95.00 %.

Documentos auditados: 40 · Conformes: 38 · RSD: 95.00 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 14/09/2026 | ING | ING-SC-0112 | VARI | VARI-2503-521A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 15/09/2026 | SAL | SAL-SC-0217 | DTA | DTA-2603-463K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 15/09/2026 | AJU | AJU-SC-0763 | INFL | INFL-2603-792B | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 16/09/2026 | TRA | TRA-SC-0129 | ROTA | ROTA-2605-833M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 17/09/2026 | TRA | TRA-SC-0223 | DTA | DTA-2602-797A | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 18/09/2026 | ING | ING-SC-0207 | ROTA | ROTA-2603-156K | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 18/09/2026 | DEV | DEV-SC-0118 | INFL | INFL-2603-792B | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 19/09/2026 | SAL | SAL-SC-0248 | BCG | BCG-2504-789B | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 20/09/2026 | DEV | DEV-SC-0173 | NEUM | NEUM-2505-638K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 20/09/2026 | SAL | SAL-SC-0358 | SPR | SPR-2609-423M | 240 | S | S | S | S | S | S | S | N | N | M8 | Correlativo duplicado por reintento de grabación. |
| 11 | 21/09/2026 | ING | ING-SC-0293 | DTA | DTA-2602-797A | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 22/09/2026 | DEV | DEV-SC-0190 | BCG | BCG-2504-789B | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 23/09/2026 | TRA | TRA-SC-0224 | HEPB | HEPB-2603-786K | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 23/09/2026 | SAL | SAL-SC-0584 | ROTA | ROTA-2602-464A | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 24/09/2026 | TRA | TRA-SC-0314 | INFL | INFL-2603-792B | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 25/09/2026 | AJU | AJU-SC-0765 | SPR | SPR-2603-471K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 25/09/2026 | SAL | SAL-SC-0843 | NEUM | NEUM-2505-638K | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 26/09/2026 | SAL | SAL-SC-1113 | IPV | IPV-2608-446B | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 27/09/2026 | ING | ING-SC-0464 | SPR | SPR-2609-423M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 28/09/2026 | ING | ING-SC-1006 | BCG | BCG-2607-654A | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 28/09/2026 | SAL | SAL-SC-1689 | BCG | BCG-2607-654A | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 29/09/2026 | SAL | SAL-SC-2171 | BCG | BCG-2607-654A | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 30/09/2026 | SAL | SAL-SC-2406 | BCG | BCG-2607-654A | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 01/10/2026 | TRA | TRA-SC-0430 | VARI | VARI-2509-637K | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 01/10/2026 | SAL | SAL-SC-2593 | DTA | DTA-2603-463K | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 02/10/2026 | TRA | TRA-SC-0505 | INFL | INFL-2604-777M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 03/10/2026 | SAL | SAL-SC-2788 | INFL | INFL-2607-737M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 03/10/2026 | SAL | SAL-SC-2989 | PENT | PENT-2504-482M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 04/10/2026 | SAL | SAL-SC-3080 | IPV | IPV-2507-805M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 05/10/2026 | TRA | TRA-SC-0805 | INFL | INFL-2607-737M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 06/10/2026 | TRA | TRA-SC-0974 | VARI | VARI-2509-637K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 06/10/2026 | SAL | SAL-SC-3113 | HEPB | HEPB-2603-786K | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 07/10/2026 | SAL | SAL-SC-3557 | VARI | VARI-2501-250M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 08/10/2026 | DEV | DEV-SC-0373 | SPR | SPR-2603-471K | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 08/10/2026 | TRA | TRA-SC-1060 | IPV | IPV-2605-698M | 150 | N | S | S | S | S | S | S | N | N | M1+M8 | Correlativo duplicado por reintento de grabación. |
| 36 | 09/10/2026 | ING | ING-SC-1249 | HEPB | HEPB-2602-318M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 10/10/2026 | SAL | SAL-SC-4502 | HEPB | HEPB-2509-474M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 11/10/2026 | SAL | SAL-SC-5029 | IPV | IPV-2503-662B | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 11/10/2026 | ING | ING-SC-1418 | SPR | SPR-2609-423M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 12/10/2026 | ING | ING-SC-1933 | ROTA | ROTA-2502-563B | 150 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-03 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 30/09/2026 | S/C | ROTA | 80 | 80 | 0 | GR-SC-8716 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 2 | 29/09/2026 | S/C | INFL | 40 | 40 | 0 | GR-SC-9536 | Sí | Conforme. Cantidad y guía coinciden. |
| 3 | 20/09/2026 | S/C | PENT | 120 | 120 | 0 | GR-SC-8667 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 4 | 15/09/2026 | S/C | INFL | 200 | 200 | 0 | GR-SC-9230 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 5 | 30/09/2026 | S/C | IPV | 180 | 180 | 0 | GR-SC-9134 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 6 | 03/10/2026 | S/C | INFL | 40 | 40 | 0 | GR-SC-2371 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 7 | 07/10/2026 | S/C | HEPB | 60 | 60 | 0 | GR-SC-8182 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 8 | 24/09/2026 | S/C | SPR | 20 | 20 | 0 | GR-SC-4770 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 9 | 19/09/2026 | S/C | DTA | 80 | 80 | 0 | GR-SC-1217 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 10 | 26/09/2026 | S/C | VARI | 50 | 50 | 0 | GR-SC-7871 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 11 | 06/10/2026 | S/C | DTA | 40 | 40 | 0 | GR-SC-8895 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 12 | 30/09/2026 | S/C | SPR | 200 | 200 | 0 | GR-SC-1650 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 13 | 20/09/2026 | S/C | IPV | 80 | 80 | 0 | GR-SC-1202 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 14 | 22/09/2026 | S/C | SPR | 30 | 30 | 0 | GR-SC-2784 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 15 | 19/09/2026 | S/C | BCG | 100 | 100 | 0 | GR-SC-5757 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 16 | 02/10/2026 | S/C | PENT | 20 | 20 | 0 | GR-SC-1925 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 17 | 23/09/2026 | S/C | SPR | 50 | 45 | -5 | GR-SC-5460 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 18 | 24/09/2026 | S/C | INFL | 50 | 50 | 0 | GR-SC-5851 | Sí | Conforme. Cantidad y guía coinciden. |
| 19 | 29/09/2026 | S/C | PENT | 200 | 200 | 0 | GR-SC-4258 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 20 | 08/10/2026 | S/C | BCG | 50 | 50 | 0 | GR-SC-6675 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 21 | 18/09/2026 | S/C | VARI | 150 | 150 | 0 | GR-SC-8253 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 22 | 28/09/2026 | S/C | ROTA | 200 | 200 | 0 | GR-SC-6369 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 23 | 27/09/2026 | S/C | BCG | 100 | 100 | 0 | GR-SC-6547 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 24 | 22/09/2026 | S/C | HEPB | 50 | 50 | 0 | GR-SC-5518 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 25 | 04/10/2026 | S/C | HEPB | 80 | 80 | 0 | GR-SC-7852 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 7 · TRAB-04 · Pretest (proceso manual) · 11/08/2026

Centro de acopio: **Hospital ESSALUD Andahuaylas** (11214) · Auditor: **OBS-02** · Periodo auditado: **12/07/2026 al 10/08/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 13 · RSD 65.00 %.

Documentos auditados: 40 · Conformes: 29 · RSD: 72.50 % · Entregas conciliadas: 25 · Concordantes: 19 · CPE: 76.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 12/07/2026 | DEV | DEV-11214-0167 | SPR | SPR-2606-500M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 13/07/2026 | ING | ING-11214-0366 | INFL | INFL-2508-359M | 180 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 3 | 13/07/2026 | ING | ING-11214-0457 | BCG | BCG-2606-808K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 14/07/2026 | DEV | DEV-11214-0335 | HEPB | HEPB-2603-786K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 15/07/2026 | SAL | SAL-11214-0143 | VARI | VARI-2503-521A | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 16/07/2026 | TRA | TRA-11214-0163 | IPV | IPV-2608-446B | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 16/07/2026 | TRA | TRA-11214-0172 | HEPB | HEPB-2602-318M | 60 | S | S | S | S | N | S | S | S | N | M5 | Origen o destino consignado de forma incompleta. |
| 8 | 17/07/2026 | AJU | AJU-11214-0318 | BCG | BCG-2606-296K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 18/07/2026 | ING | ING-11214-0504 | INFL | INFL-2607-737M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 19/07/2026 | SAL | SAL-11214-0164 | PENT | PENT-2605-322M | 300 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 11 | 19/07/2026 | SAL | SAL-11214-0248 | DTA | DTA-2602-236K | 60 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 12 | 20/07/2026 | SAL | SAL-11214-0280 | NEUM | NEUM-2505-638K | 80 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 13 | 21/07/2026 | ING | ING-11214-0875 | VARI | VARI-2503-521A | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 22/07/2026 | DEV | DEV-11214-0385 | BCG | BCG-2606-296K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 22/07/2026 | SAL | SAL-11214-0810 | VARI | VARI-2508-818M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 23/07/2026 | SAL | SAL-11214-1235 | NEUM | NEUM-2509-952A | 240 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 17 | 24/07/2026 | SAL | SAL-11214-1294 | PENT | PENT-2606-251M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 25/07/2026 | SAL | SAL-11214-1488 | HEPB | HEPB-2603-786K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 25/07/2026 | SAL | SAL-11214-1985 | NEUM | NEUM-2505-688A | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 26/07/2026 | ING | ING-11214-1478 | INFL | INFL-2508-359M | 30 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 21 | 27/07/2026 | ING | ING-11214-2060 | HEPB | HEPB-2509-474M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 28/07/2026 | SAL | SAL-11214-2149 | PENT | PENT-2606-251M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 28/07/2026 | ING | ING-11214-2139 | VARI | VARI-2509-637K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 29/07/2026 | TRA | TRA-11214-0256 | SPR | SPR-2606-500M | 150 | S | S | N | S | S | S | S | S | N | M3 | Fecha de vencimiento vencida o ilegible en el asiento. |
| 25 | 30/07/2026 | ING | ING-11214-2632 | BCG | BCG-2504-789B | 20 | S | N | S | S | S | N | S | S | N | M2+M6 | Asiento sin firma del responsable del almacén. |
| 26 | 31/07/2026 | ING | ING-11214-3105 | NEUM | NEUM-2509-952A | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 31/07/2026 | SAL | SAL-11214-2275 | VARI | VARI-2508-818M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 01/08/2026 | ING | ING-11214-3157 | DTA | DTA-2602-797A | 120 | S | S | S | N | S | S | S | S | N | M4 | Cantidad física menor a la registrada en el asiento. |
| 29 | 02/08/2026 | SAL | SAL-11214-2466 | HEPB | HEPB-2509-474M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 03/08/2026 | ING | ING-11214-4508 | DTA | DTA-2602-236K | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 03/08/2026 | TRA | TRA-11214-0330 | ROTA | ROTA-2502-563B | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 04/08/2026 | SAL | SAL-11214-2482 | ROTA | ROTA-2603-156K | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 05/08/2026 | TRA | TRA-11214-0459 | BCG | BCG-2607-654A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 06/08/2026 | TRA | TRA-11214-0580 | HEPB | HEPB-2609-917M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 06/08/2026 | TRA | TRA-11214-0894 | BCG | BCG-2606-808K | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 07/08/2026 | TRA | TRA-11214-1129 | DTA | DTA-2505-409K | 200 | N | S | S | S | S | S | S | N | N | M1+M8 | Numeración correlativa interrumpida; falta un folio. |
| 37 | 08/08/2026 | DEV | DEV-11214-0675 | INFL | INFL-2607-737M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 09/08/2026 | SAL | SAL-11214-2834 | BCG | BCG-2507-694K | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 09/08/2026 | SAL | SAL-11214-2999 | SPR | SPR-2603-471K | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 10/08/2026 | ING | ING-11214-4677 | PENT | PENT-2606-251M | 50 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-04 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 18/07/2026 | 11214 | PENT | 180 | 180 | 0 | GR-11214-1867 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 2 | 17/07/2026 | 11214 | ROTA | 60 | 60 | 0 | GR-11214-3727 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 3 | 23/07/2026 | 11214 | INFL | 200 | 200 | 0 | GR-11214-7535 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 4 | 15/07/2026 | 11214 | BCG | 20 | 20 | 0 | GR-11214-6917 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 5 | 09/08/2026 | 11214 | HEPB | 20 | 25 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 6 | 07/08/2026 | 11214 | HEPB | 200 | 210 | 10 | GR-11214-3436 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 7 | 05/08/2026 | 11214 | INFL | 150 | 150 | 0 | GR-11214-3215 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 8 | 29/07/2026 | 11214 | INFL | 60 | 60 | 0 | GR-11214-8558 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 9 | 28/07/2026 | 11214 | SPR | 30 | 30 | 0 | GR-11214-6777 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 10 | 17/07/2026 | 11214 | BCG | 20 | 20 | 0 | GR-11214-3444 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 11 | 07/08/2026 | 11214 | SPR | 60 | 60 | 0 | GR-11214-8380 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 12 | 28/07/2026 | 11214 | HEPB | 20 | 20 | 0 | GR-11214-8787 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 13 | 05/08/2026 | 11214 | DTA | 120 | 110 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 14 | 14/07/2026 | 11214 | DTA | 200 | 200 | 0 | GR-11214-6766 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 15 | 25/07/2026 | 11214 | ROTA | 100 | 100 | 0 | GR-11214-6379 | Sí | Conforme. Cantidad y guía coinciden. |
| 16 | 04/08/2026 | 11214 | ROTA | 40 | 40 | 0 | GR-11214-7297 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 17 | 04/08/2026 | 11214 | PENT | 180 | 180 | 0 | GR-11214-4321 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 18 | 05/08/2026 | 11214 | DTA | 20 | 20 | 0 | GR-11214-1658 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 19 | 09/08/2026 | 11214 | VARI | 200 | 190 | -10 | GR-11214-3780 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 20 | 15/07/2026 | 11214 | PENT | 40 | 40 | 0 | GR-11214-1328 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 21 | 10/08/2026 | 11214 | HEPB | 80 | 80 | 0 | GR-11214-9574 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 22 | 19/07/2026 | 11214 | BCG | 100 | 95 | -5 | GR-11214-3004 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 23 | 10/08/2026 | 11214 | HEPB | 50 | 55 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 24 | 02/08/2026 | 11214 | ROTA | 200 | 200 | 0 | GR-11214-8880 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 25 | 20/07/2026 | 11214 | DTA | 180 | 180 | 0 | GR-11214-7473 | Sí | Conforme. Verificado el FEFO al momento de la carga. |

Cierre: 19 entregas concordantes ÷ 25 × 100 = **76.00 %**.

---

### Bloque 8 · TRAB-04 · Postest (Sistema SIVAC) · 13/10/2026

Centro de acopio: **Hospital ESSALUD Andahuaylas** (11214) · Auditor: **OBS-02** · Periodo auditado: **15/09/2026 al 12/10/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 20 · RSD 100.00 %.

Documentos auditados: 40 · Conformes: 36 · RSD: 90.00 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 18/09/2026 | AJU | AJU-11214-0790 | PENT | PENT-2605-322M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 19/09/2026 | SAL | SAL-11214-0471 | NEUM | NEUM-2505-688A | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 19/09/2026 | SAL | SAL-11214-0908 | INFL | INFL-2604-777M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 20/09/2026 | ING | ING-11214-0130 | DTA | DTA-2505-409K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 20/09/2026 | ING | ING-11214-0370 | VARI | VARI-2508-818M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 21/09/2026 | ING | ING-11214-0568 | INFL | INFL-2603-792B | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 22/09/2026 | TRA | TRA-11214-0662 | INFL | INFL-2607-737M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 22/09/2026 | SAL | SAL-11214-1069 | PENT | PENT-2504-482M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 23/09/2026 | SAL | SAL-11214-1433 | DTA | DTA-2505-409K | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 24/09/2026 | ING | ING-11214-0893 | VARI | VARI-2607-979A | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 24/09/2026 | AJU | AJU-11214-0858 | DTA | DTA-2505-409K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 25/09/2026 | SAL | SAL-11214-1772 | NEUM | NEUM-2505-638K | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 25/09/2026 | ING | ING-11214-1046 | PENT | PENT-2606-391A | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 26/09/2026 | ING | ING-11214-1137 | DTA | DTA-2603-463K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 27/09/2026 | SAL | SAL-11214-2079 | IPV | IPV-2608-446B | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 27/09/2026 | SAL | SAL-11214-2460 | DTA | DTA-2603-463K | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 28/09/2026 | ING | ING-11214-1402 | NEUM | NEUM-2506-884B | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 28/09/2026 | DEV | DEV-11214-0266 | ROTA | ROTA-2602-464A | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 29/09/2026 | DEV | DEV-11214-0436 | PENT | PENT-2508-232M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 30/09/2026 | ING | ING-11214-1617 | SPR | SPR-2608-539M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 30/09/2026 | DEV | DEV-11214-0532 | SPR | SPR-2606-500M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 01/10/2026 | DEV | DEV-11214-0754 | PENT | PENT-2508-232M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 02/10/2026 | TRA | TRA-11214-0830 | NEUM | NEUM-2506-884B | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 02/10/2026 | ING | ING-11214-1755 | ROTA | ROTA-2602-464A | 120 | S | N | S | S | S | S | S | N | N | M2+M8 | Lote digitado con un dígito trocado; se subsanó en el sistema. |
| 25 | 03/10/2026 | ING | ING-11214-1798 | IPV | IPV-2608-446B | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 03/10/2026 | TRA | TRA-11214-0948 | HEPB | HEPB-2603-786K | 20 | S | S | S | S | S | N | S | S | N | M6 | Firma pendiente de regularización del responsable. |
| 27 | 04/10/2026 | SAL | SAL-11214-2551 | DTA | DTA-2603-463K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 05/10/2026 | TRA | TRA-11214-1072 | VARI | VARI-2501-250M | 120 | S | S | S | N | S | S | S | S | N | M4 | Diferencia de una unidad entre conteo físico y sistema. |
| 29 | 05/10/2026 | TRA | TRA-11214-1306 | SPR | SPR-2609-423M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 06/10/2026 | SAL | SAL-11214-2869 | HEPB | HEPB-2602-318M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 06/10/2026 | SAL | SAL-11214-3840 | VARI | VARI-2607-979A | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 07/10/2026 | SAL | SAL-11214-3872 | INFL | INFL-2607-737M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 08/10/2026 | ING | ING-11214-2267 | PENT | PENT-2504-482M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 08/10/2026 | SAL | SAL-11214-4280 | VARI | VARI-2503-521A | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 09/10/2026 | DEV | DEV-11214-0847 | INFL | INFL-2508-359M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 10/10/2026 | SAL | SAL-11214-4399 | INFL | INFL-2603-792B | 30 | S | S | S | S | S | S | S | N | N | M8 | Correlativo duplicado por reintento de grabación. |
| 37 | 10/10/2026 | TRA | TRA-11214-1316 | DTA | DTA-2603-463K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 11/10/2026 | TRA | TRA-11214-2236 | DTA | DTA-2505-409K | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 11/10/2026 | SAL | SAL-11214-4435 | DTA | DTA-2606-829K | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 12/10/2026 | SAL | SAL-11214-4436 | BCG | BCG-2607-654A | 300 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-04 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 27/09/2026 | 11214 | INFL | 30 | 30 | 0 | GR-11214-8358 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 2 | 20/09/2026 | 11214 | DTA | 20 | 15 | -5 | GR-11214-2646 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 3 | 21/09/2026 | 11214 | NEUM | 30 | 30 | 0 | GR-11214-4720 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 4 | 28/09/2026 | 11214 | HEPB | 40 | 40 | 0 | GR-11214-7322 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 5 | 01/10/2026 | 11214 | DTA | 60 | 60 | 0 | GR-11214-8699 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 6 | 08/10/2026 | 11214 | PENT | 120 | 120 | 0 | GR-11214-3294 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 7 | 06/10/2026 | 11214 | INFL | 60 | 60 | 0 | GR-11214-8543 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 8 | 15/09/2026 | 11214 | IPV | 40 | 40 | 0 | GR-11214-3071 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 9 | 17/09/2026 | 11214 | SPR | 100 | 100 | 0 | GR-11214-5337 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 10 | 19/09/2026 | 11214 | INFL | 80 | 80 | 0 | GR-11214-3298 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 11 | 30/09/2026 | 11214 | NEUM | 20 | 20 | 0 | GR-11214-4903 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 12 | 02/10/2026 | 11214 | IPV | 20 | 20 | 0 | GR-11214-3021 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 26/09/2026 | 11214 | NEUM | 60 | 60 | 0 | GR-11214-6153 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 14 | 18/09/2026 | 11214 | DTA | 50 | 50 | 0 | GR-11214-9366 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 15 | 21/09/2026 | 11214 | ROTA | 50 | 50 | 0 | GR-11214-8952 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 16 | 08/10/2026 | 11214 | DTA | 150 | 150 | 0 | GR-11214-2689 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 17 | 24/09/2026 | 11214 | HEPB | 120 | 120 | 0 | GR-11214-4777 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 18 | 02/10/2026 | 11214 | SPR | 30 | 30 | 0 | GR-11214-4071 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 19 | 04/10/2026 | 11214 | INFL | 180 | 180 | 0 | GR-11214-8141 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 20 | 04/10/2026 | 11214 | PENT | 50 | 50 | 0 | GR-11214-5550 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 21 | 26/09/2026 | 11214 | DTA | 80 | 80 | 0 | GR-11214-8085 | Sí | Conforme. Cantidad y guía coinciden. |
| 22 | 24/09/2026 | 11214 | INFL | 50 | 50 | 0 | GR-11214-7863 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 23 | 22/09/2026 | 11214 | ROTA | 50 | 50 | 0 | GR-11214-5388 | Sí | Conforme. Cantidad y guía coinciden. |
| 24 | 04/10/2026 | 11214 | IPV | 20 | 20 | 0 | GR-11214-8203 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 25 | 29/09/2026 | 11214 | IPV | 60 | 60 | 0 | GR-11214-8920 | Sí | Conforme. Cantidad y guía coinciden. |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 9 · TRAB-05 · Pretest (proceso manual) · 12/08/2026

Centro de acopio: **Centro de Salud Andahuaylas** (6804) · Auditor: **OBS-01** · Periodo auditado: **09/07/2026 al 11/08/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 11 · RSD 55.00 %.

Documentos auditados: 40 · Conformes: 22 · RSD: 55.00 % · Entregas conciliadas: 25 · Concordantes: 15 · CPE: 60.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 09/07/2026 | AJU | AJU-6804-0707 | VARI | VARI-2501-250M | 150 | N | S | S | S | S | N | S | S | N | M1+M6 | Asiento sin firma del responsable del almacén. |
| 2 | 10/07/2026 | ING | ING-6804-0158 | IPV | IPV-2504-587B | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 11/07/2026 | SAL | SAL-6804-0234 | PENT | PENT-2605-322M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 12/07/2026 | SAL | SAL-6804-0373 | INFL | INFL-2504-261K | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 12/07/2026 | ING | ING-6804-1029 | IPV | IPV-2503-662B | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 13/07/2026 | DEV | DEV-6804-0157 | SPR | SPR-2608-539M | 80 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 7 | 14/07/2026 | DEV | DEV-6804-0247 | ROTA | ROTA-2605-833M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 15/07/2026 | DEV | DEV-6804-0431 | DTA | DTA-2603-463K | 180 | S | S | N | S | S | S | S | S | N | M3 | Fecha de vencimiento vencida o ilegible en el asiento. |
| 9 | 16/07/2026 | TRA | TRA-6804-0123 | IPV | IPV-2507-805M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 17/07/2026 | SAL | SAL-6804-1239 | IPV | IPV-2507-805M | 80 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 11 | 17/07/2026 | SAL | SAL-6804-1332 | BCG | BCG-2606-296K | 100 | N | S | S | S | S | S | S | S | N | M1 | Biológico consignado no corresponde al frasco físico. |
| 12 | 18/07/2026 | ING | ING-6804-1511 | SPR | SPR-2603-471K | 20 | N | S | S | S | S | S | S | S | N | M1 | Biológico consignado no corresponde al frasco físico. |
| 13 | 19/07/2026 | AJU | AJU-6804-0715 | ROTA | ROTA-2507-417A | 200 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 14 | 20/07/2026 | SAL | SAL-6804-1401 | IPV | IPV-2507-805M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 21/07/2026 | SAL | SAL-6804-1779 | BCG | BCG-2507-694K | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 22/07/2026 | SAL | SAL-6804-1814 | VARI | VARI-2501-250M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 23/07/2026 | DEV | DEV-6804-0567 | VARI | VARI-2509-637K | 120 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 18 | 23/07/2026 | SAL | SAL-6804-2140 | INFL | INFL-2504-261K | 200 | S | S | N | S | N | S | S | S | N | M3+M5 | Fecha de vencimiento vencida o ilegible en el asiento. |
| 19 | 24/07/2026 | ING | ING-6804-1513 | IPV | IPV-2504-587B | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 25/07/2026 | ING | ING-6804-1612 | NEUM | NEUM-2509-952A | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 26/07/2026 | ING | ING-6804-1998 | IPV | IPV-2605-698M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 27/07/2026 | SAL | SAL-6804-2216 | SPR | SPR-2609-423M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 28/07/2026 | ING | ING-6804-2320 | VARI | VARI-2501-250M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 28/07/2026 | SAL | SAL-6804-2243 | DTA | DTA-2606-829K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 29/07/2026 | DEV | DEV-6804-0817 | VARI | VARI-2607-979A | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 30/07/2026 | ING | ING-6804-2340 | ROTA | ROTA-2602-464A | 240 | S | S | N | S | N | S | S | S | N | M3+M5 | Origen o destino consignado de forma incompleta. |
| 27 | 31/07/2026 | ING | ING-6804-2379 | ROTA | ROTA-2603-156K | 30 | S | S | S | S | N | S | N | S | N | M5+M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 28 | 01/08/2026 | SAL | SAL-6804-2482 | IPV | IPV-2507-805M | 40 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 29 | 02/08/2026 | SAL | SAL-6804-2670 | SPR | SPR-2603-471K | 80 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 30 | 03/08/2026 | AJU | AJU-6804-1331 | ROTA | ROTA-2602-464A | 30 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 31 | 03/08/2026 | SAL | SAL-6804-2794 | VARI | VARI-2501-250M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 04/08/2026 | DEV | DEV-6804-0971 | BCG | BCG-2606-296K | 120 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 33 | 05/08/2026 | SAL | SAL-6804-3037 | PENT | PENT-2508-232M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 06/08/2026 | SAL | SAL-6804-3102 | SPR | SPR-2609-423M | 50 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 35 | 07/08/2026 | ING | ING-6804-2448 | HEPB | HEPB-2603-786K | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 08/08/2026 | TRA | TRA-6804-0128 | SPR | SPR-2606-500M | 30 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 37 | 08/08/2026 | TRA | TRA-6804-0386 | BCG | BCG-2606-296K | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 09/08/2026 | SAL | SAL-6804-3624 | SPR | SPR-2603-471K | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 10/08/2026 | ING | ING-6804-2644 | ROTA | ROTA-2507-417A | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 11/08/2026 | SAL | SAL-6804-3820 | HEPB | HEPB-2603-786K | 300 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |

**Entregas conciliadas — TRAB-05 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 31/07/2026 | 6804 | SPR | 100 | 100 | 0 | GR-6804-6088 | Sí | Conforme. Cantidad y guía coinciden. |
| 2 | 16/07/2026 | 6804 | BCG | 60 | 60 | 0 | GR-6804-9607 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 3 | 20/07/2026 | 6804 | NEUM | 80 | 70 | -10 | GR-6804-1382 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 4 | 22/07/2026 | 6804 | HEPB | 100 | 100 | 0 | GR-6804-3006 | Sí | Conforme. Cantidad y guía coinciden. |
| 5 | 31/07/2026 | 6804 | SPR | 40 | 40 | 0 | GR-6804-8690 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 6 | 17/07/2026 | 6804 | PENT | 60 | 60 | 0 | GR-6804-1790 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 7 | 28/07/2026 | 6804 | SPR | 80 | 80 | 0 | GR-6804-5929 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 8 | 20/07/2026 | 6804 | PENT | 80 | 80 | 0 | GR-6804-8048 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 9 | 10/08/2026 | 6804 | VARI | 60 | 60 | 0 | GR-6804-7842 | Sí | Conforme. Cantidad y guía coinciden. |
| 10 | 23/07/2026 | 6804 | BCG | 40 | 45 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 11 | 19/07/2026 | 6804 | SPR | 120 | 120 | 0 | GR-6804-5906 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 12 | 05/08/2026 | 6804 | ROTA | 20 | 15 | -5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 13 | 28/07/2026 | 6804 | VARI | 80 | 90 | 10 | GR-6804-6122 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 14 | 30/07/2026 | 6804 | VARI | 80 | 80 | 0 | GR-6804-9240 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 15 | 26/07/2026 | 6804 | VARI | 100 | 100 | 0 | GR-6804-6073 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 16 | 01/08/2026 | 6804 | ROTA | 100 | 90 | -10 | GR-6804-2782 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 17 | 03/08/2026 | 6804 | NEUM | 60 | 60 | 0 | GR-6804-8089 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 18 | 22/07/2026 | 6804 | ROTA | 30 | 30 | 0 | GR-6804-8501 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 19 | 20/07/2026 | 6804 | SPR | 80 | 70 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 20 | 27/07/2026 | 6804 | VARI | 50 | 50 | 0 | GR-6804-9502 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 21 | 10/08/2026 | 6804 | BCG | 40 | 40 | 0 | GR-6804-1815 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 22 | 11/08/2026 | 6804 | HEPB | 180 | 185 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 23 | 04/08/2026 | 6804 | HEPB | 40 | 30 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 24 | 15/07/2026 | 6804 | SPR | 40 | 30 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 25 | 20/07/2026 | 6804 | PENT | 30 | 25 | -5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |

Cierre: 15 entregas concordantes ÷ 25 × 100 = **60.00 %**.

---

### Bloque 10 · TRAB-05 · Postest (Sistema SIVAC) · 14/10/2026

Centro de acopio: **Centro de Salud Andahuaylas** (6804) · Auditor: **OBS-01** · Periodo auditado: **14/09/2026 al 13/10/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 20 · RSD 100.00 %.

Documentos auditados: 40 · Conformes: 39 · RSD: 97.50 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 14/09/2026 | DEV | DEV-6804-0117 | IPV | IPV-2503-662B | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 15/09/2026 | ING | ING-6804-0248 | VARI | VARI-2607-979A | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 15/09/2026 | SAL | SAL-6804-0316 | DTA | DTA-2602-236K | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 16/09/2026 | TRA | TRA-6804-0120 | NEUM | NEUM-2505-688A | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 17/09/2026 | TRA | TRA-6804-0206 | NEUM | NEUM-2509-952A | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 18/09/2026 | ING | ING-6804-0598 | IPV | IPV-2608-446B | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 18/09/2026 | DEV | DEV-6804-0233 | IPV | IPV-2608-446B | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 19/09/2026 | SAL | SAL-6804-0353 | VARI | VARI-2509-637K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 20/09/2026 | SAL | SAL-6804-0739 | SPR | SPR-2609-423M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 21/09/2026 | TRA | TRA-6804-0333 | PENT | PENT-2605-322M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 21/09/2026 | AJU | AJU-6804-0381 | DTA | DTA-2505-409K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 22/09/2026 | DEV | DEV-6804-0398 | SPR | SPR-2609-423M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 23/09/2026 | ING | ING-6804-0859 | VARI | VARI-2509-637K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 24/09/2026 | SAL | SAL-6804-1163 | NEUM | NEUM-2507-181K | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 24/09/2026 | SAL | SAL-6804-1668 | INFL | INFL-2504-261K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 25/09/2026 | TRA | TRA-6804-0397 | PENT | PENT-2606-391A | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 26/09/2026 | TRA | TRA-6804-0456 | NEUM | NEUM-2509-952A | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 27/09/2026 | SAL | SAL-6804-2679 | BCG | BCG-2507-694K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 27/09/2026 | DEV | DEV-6804-0418 | NEUM | NEUM-2505-638K | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 28/09/2026 | ING | ING-6804-1101 | VARI | VARI-2503-521A | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 29/09/2026 | ING | ING-6804-1752 | DTA | DTA-2602-236K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 30/09/2026 | DEV | DEV-6804-0473 | ROTA | ROTA-2502-563B | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 30/09/2026 | DEV | DEV-6804-0593 | IPV | IPV-2503-662B | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 01/10/2026 | SAL | SAL-6804-3236 | VARI | VARI-2607-979A | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 02/10/2026 | TRA | TRA-6804-1174 | DTA | DTA-2603-463K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 03/10/2026 | SAL | SAL-6804-3532 | SPR | SPR-2606-500M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 03/10/2026 | SAL | SAL-6804-3612 | IPV | IPV-2503-662B | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 04/10/2026 | SAL | SAL-6804-3689 | IPV | IPV-2608-446B | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 05/10/2026 | SAL | SAL-6804-3900 | BCG | BCG-2606-296K | 300 | S | S | S | S | S | N | S | N | N | M6+M8 | Firma pendiente de regularización del responsable. |
| 30 | 06/10/2026 | ING | ING-6804-2082 | IPV | IPV-2504-587B | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 06/10/2026 | TRA | TRA-6804-1236 | PENT | PENT-2606-391A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 07/10/2026 | AJU | AJU-6804-0399 | ROTA | ROTA-2603-156K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 08/10/2026 | SAL | SAL-6804-4094 | IPV | IPV-2504-587B | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 09/10/2026 | TRA | TRA-6804-2337 | HEPB | HEPB-2509-474M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 09/10/2026 | TRA | TRA-6804-2560 | IPV | IPV-2605-698M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 10/10/2026 | DEV | DEV-6804-1064 | BCG | BCG-2607-654A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 11/10/2026 | AJU | AJU-6804-0452 | SPR | SPR-2609-423M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 12/10/2026 | SAL | SAL-6804-4161 | PENT | PENT-2605-322M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 12/10/2026 | TRA | TRA-6804-2771 | INFL | INFL-2603-792B | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 13/10/2026 | ING | ING-6804-2137 | ROTA | ROTA-2605-833M | 60 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-05 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 13/10/2026 | 6804 | INFL | 40 | 40 | 0 | GR-6804-2129 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 2 | 08/10/2026 | 6804 | ROTA | 60 | 60 | 0 | GR-6804-2187 | Sí | Conforme. Cantidad y guía coinciden. |
| 3 | 18/09/2026 | 6804 | HEPB | 50 | 50 | 0 | GR-6804-4034 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 4 | 06/10/2026 | 6804 | HEPB | 180 | 180 | 0 | GR-6804-4894 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 5 | 26/09/2026 | 6804 | VARI | 100 | 100 | 0 | GR-6804-7460 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 6 | 30/09/2026 | 6804 | DTA | 30 | 30 | 0 | GR-6804-2940 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 7 | 09/10/2026 | 6804 | ROTA | 20 | 20 | 0 | GR-6804-7200 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 8 | 02/10/2026 | 6804 | VARI | 80 | 80 | 0 | GR-6804-6556 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 9 | 22/09/2026 | 6804 | SPR | 150 | 150 | 0 | GR-6804-6841 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 10 | 13/10/2026 | 6804 | DTA | 60 | 60 | 0 | GR-6804-7949 | Sí | Conforme. Cantidad y guía coinciden. |
| 11 | 13/10/2026 | 6804 | IPV | 80 | 80 | 0 | GR-6804-7297 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 12 | 06/10/2026 | 6804 | NEUM | 60 | 60 | 0 | GR-6804-2842 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 13 | 05/10/2026 | 6804 | NEUM | 30 | 30 | 0 | GR-6804-3368 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 14 | 07/10/2026 | 6804 | INFL | 80 | 70 | -10 | GR-6804-9557 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 15 | 09/10/2026 | 6804 | ROTA | 50 | 50 | 0 | GR-6804-6188 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 16 | 17/09/2026 | 6804 | BCG | 60 | 60 | 0 | GR-6804-2040 | Sí | Conforme. Cantidad y guía coinciden. |
| 17 | 17/09/2026 | 6804 | INFL | 120 | 120 | 0 | GR-6804-3347 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 18 | 23/09/2026 | 6804 | NEUM | 180 | 180 | 0 | GR-6804-9651 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 19 | 12/10/2026 | 6804 | IPV | 20 | 20 | 0 | GR-6804-5301 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 20 | 09/10/2026 | 6804 | IPV | 20 | 20 | 0 | GR-6804-4632 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 21 | 10/10/2026 | 6804 | VARI | 200 | 200 | 0 | GR-6804-2854 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 22 | 18/09/2026 | 6804 | PENT | 30 | 30 | 0 | GR-6804-9050 | Sí | Conforme. Cantidad y guía coinciden. |
| 23 | 30/09/2026 | 6804 | VARI | 180 | 180 | 0 | GR-6804-1963 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 24 | 13/10/2026 | 6804 | VARI | 200 | 200 | 0 | GR-6804-2049 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 25 | 22/09/2026 | 6804 | INFL | 80 | 80 | 0 | GR-6804-4263 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 11 · TRAB-06 · Pretest (proceso manual) · 12/08/2026

Centro de acopio: **Talavera** (4195) · Auditor: **OBS-02** · Periodo auditado: **15/07/2026 al 11/08/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 11 · RSD 55.00 %.

Documentos auditados: 40 · Conformes: 26 · RSD: 65.00 % · Entregas conciliadas: 25 · Concordantes: 17 · CPE: 68.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 18/07/2026 | TRA | TRA-4195-0163 | HEPB | HEPB-2609-917M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 19/07/2026 | AJU | AJU-4195-0112 | ROTA | ROTA-2602-464A | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 19/07/2026 | SAL | SAL-4195-0470 | IPV | IPV-2503-662B | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 20/07/2026 | AJU | AJU-4195-0240 | HEPB | HEPB-2602-318M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 20/07/2026 | SAL | SAL-4195-0903 | IPV | IPV-2503-662B | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 21/07/2026 | ING | ING-4195-0628 | IPV | IPV-2504-587B | 300 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 7 | 22/07/2026 | SAL | SAL-4195-1737 | SPR | SPR-2606-500M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 22/07/2026 | DEV | DEV-4195-0210 | DTA | DTA-2606-829K | 100 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 9 | 23/07/2026 | SAL | SAL-4195-2278 | VARI | VARI-2508-818M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 24/07/2026 | SAL | SAL-4195-2396 | DTA | DTA-2602-236K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 24/07/2026 | SAL | SAL-4195-2399 | NEUM | NEUM-2506-884B | 150 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 12 | 25/07/2026 | ING | ING-4195-0747 | PENT | PENT-2606-251M | 80 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 13 | 25/07/2026 | ING | ING-4195-0865 | VARI | VARI-2501-250M | 30 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 14 | 26/07/2026 | AJU | AJU-4195-0362 | HEPB | HEPB-2609-917M | 50 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 15 | 27/07/2026 | DEV | DEV-4195-0360 | VARI | VARI-2503-521A | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 27/07/2026 | ING | ING-4195-1176 | NEUM | NEUM-2505-638K | 180 | N | S | S | S | S | S | S | S | N | M1 | Biológico consignado no corresponde al frasco físico. |
| 17 | 28/07/2026 | ING | ING-4195-1183 | BCG | BCG-2607-654A | 100 | S | S | S | N | S | S | S | S | N | M4 | Cantidad física menor a la registrada en el asiento. |
| 18 | 28/07/2026 | TRA | TRA-4195-0246 | INFL | INFL-2607-737M | 20 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 19 | 29/07/2026 | SAL | SAL-4195-2420 | DTA | DTA-2602-236K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 30/07/2026 | ING | ING-4195-1201 | VARI | VARI-2503-521A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 30/07/2026 | DEV | DEV-4195-0543 | DTA | DTA-2602-236K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 31/07/2026 | ING | ING-4195-1291 | SPR | SPR-2606-500M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 01/08/2026 | ING | ING-4195-1332 | BCG | BCG-2507-694K | 30 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 24 | 01/08/2026 | AJU | AJU-4195-1118 | NEUM | NEUM-2506-884B | 40 | S | N | S | S | N | S | S | S | N | M2+M5 | Origen o destino consignado de forma incompleta. |
| 25 | 02/08/2026 | TRA | TRA-4195-0356 | SPR | SPR-2504-185M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 02/08/2026 | SAL | SAL-4195-2591 | BCG | BCG-2606-296K | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 03/08/2026 | TRA | TRA-4195-0418 | VARI | VARI-2501-250M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 04/08/2026 | AJU | AJU-4195-1231 | IPV | IPV-2504-587B | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 04/08/2026 | DEV | DEV-4195-0807 | VARI | VARI-2509-637K | 20 | S | S | S | S | S | S | N | N | N | M7+M8 | Saldo arrastrado no cuadra con la columna de existencias. |
| 30 | 05/08/2026 | SAL | SAL-4195-2609 | DTA | DTA-2602-797A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 05/08/2026 | SAL | SAL-4195-2782 | ROTA | ROTA-2602-464A | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 06/08/2026 | TRA | TRA-4195-0566 | SPR | SPR-2504-185M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 07/08/2026 | SAL | SAL-4195-3007 | NEUM | NEUM-2505-688A | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 07/08/2026 | DEV | DEV-4195-0976 | NEUM | NEUM-2507-181K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 08/08/2026 | TRA | TRA-4195-1004 | SPR | SPR-2608-539M | 300 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 36 | 09/08/2026 | ING | ING-4195-1360 | SPR | SPR-2603-471K | 50 | S | S | N | S | S | S | S | N | N | M3+M8 | Numeración correlativa interrumpida; falta un folio. |
| 37 | 09/08/2026 | DEV | DEV-4195-1087 | INFL | INFL-2603-792B | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 10/08/2026 | TRA | TRA-4195-1078 | SPR | SPR-2504-185M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 10/08/2026 | ING | ING-4195-1408 | VARI | VARI-2501-250M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 11/08/2026 | DEV | DEV-4195-1160 | INFL | INFL-2504-261K | 100 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-06 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 07/08/2026 | 4195 | NEUM | 80 | 70 | -10 | GR-4195-2012 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 2 | 17/07/2026 | 4195 | DTA | 20 | 20 | 0 | GR-4195-3772 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 3 | 23/07/2026 | 4195 | DTA | 120 | 110 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 4 | 28/07/2026 | 4195 | INFL | 80 | 85 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 5 | 16/07/2026 | 4195 | INFL | 200 | 200 | 0 | GR-4195-8848 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 6 | 10/08/2026 | 4195 | PENT | 20 | 20 | 0 | GR-4195-7694 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 7 | 05/08/2026 | 4195 | SPR | 60 | 55 | -5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 8 | 06/08/2026 | 4195 | SPR | 180 | 180 | 0 | GR-4195-2264 | Sí | Conforme. Cantidad y guía coinciden. |
| 9 | 11/08/2026 | 4195 | ROTA | 40 | 40 | 0 | GR-4195-7384 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 10 | 07/08/2026 | 4195 | NEUM | 180 | 175 | -5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 11 | 07/08/2026 | 4195 | SPR | 120 | 120 | 0 | GR-4195-8005 | Sí | Conforme. Cantidad y guía coinciden. |
| 12 | 27/07/2026 | 4195 | IPV | 120 | 120 | 0 | GR-4195-8916 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 28/07/2026 | 4195 | SPR | 50 | 50 | 0 | GR-4195-2347 | Sí | Conforme. Cantidad y guía coinciden. |
| 14 | 25/07/2026 | 4195 | HEPB | 80 | 80 | 0 | GR-4195-4392 | Sí | Conforme. Cantidad y guía coinciden. |
| 15 | 02/08/2026 | 4195 | HEPB | 120 | 120 | 0 | GR-4195-2406 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 16 | 20/07/2026 | 4195 | VARI | 20 | 20 | 0 | GR-4195-6789 | Sí | Conforme. Cantidad y guía coinciden. |
| 17 | 15/07/2026 | 4195 | IPV | 40 | 40 | 0 | GR-4195-9244 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 18 | 18/07/2026 | 4195 | INFL | 120 | 120 | 0 | GR-4195-4040 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 19 | 07/08/2026 | 4195 | PENT | 150 | 140 | -10 | GR-4195-3834 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 20 | 11/08/2026 | 4195 | IPV | 100 | 100 | 0 | GR-4195-1697 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 21 | 18/07/2026 | 4195 | VARI | 30 | 30 | 0 | GR-4195-4156 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 22 | 09/08/2026 | 4195 | BCG | 40 | 35 | -5 | GR-4195-3566 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 23 | 22/07/2026 | 4195 | BCG | 180 | 180 | 0 | GR-4195-1646 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 24 | 19/07/2026 | 4195 | VARI | 180 | 180 | 0 | GR-4195-1414 | Sí | Conforme. Cantidad y guía coinciden. |
| 25 | 30/07/2026 | 4195 | DTA | 200 | 190 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |

Cierre: 17 entregas concordantes ÷ 25 × 100 = **68.00 %**.

---

### Bloque 12 · TRAB-06 · Postest (Sistema SIVAC) · 14/10/2026

Centro de acopio: **Talavera** (4195) · Auditor: **OBS-02** · Periodo auditado: **16/09/2026 al 13/10/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 20 · RSD 100.00 %.

Documentos auditados: 40 · Conformes: 38 · RSD: 95.00 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 18/09/2026 | TRA | TRA-4195-0528 | PENT | PENT-2606-251M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 19/09/2026 | DEV | DEV-4195-0449 | BCG | BCG-2606-808K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 19/09/2026 | SAL | SAL-4195-0141 | BCG | BCG-2606-808K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 20/09/2026 | TRA | TRA-4195-0601 | HEPB | HEPB-2509-474M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 21/09/2026 | ING | ING-4195-0180 | INFL | INFL-2603-792B | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 21/09/2026 | DEV | DEV-4195-0669 | BCG | BCG-2606-296K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 22/09/2026 | SAL | SAL-4195-0164 | PENT | PENT-2606-391A | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 22/09/2026 | ING | ING-4195-0381 | INFL | INFL-2607-737M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 23/09/2026 | TRA | TRA-4195-1051 | DTA | DTA-2602-236K | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 24/09/2026 | TRA | TRA-4195-1086 | IPV | IPV-2605-698M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 24/09/2026 | ING | ING-4195-0644 | ROTA | ROTA-2502-563B | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 25/09/2026 | TRA | TRA-4195-1149 | DTA | DTA-2505-409K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 26/09/2026 | TRA | TRA-4195-1643 | VARI | VARI-2508-818M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 26/09/2026 | SAL | SAL-4195-0259 | BCG | BCG-2507-694K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 27/09/2026 | ING | ING-4195-0763 | IPV | IPV-2605-698M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 28/09/2026 | SAL | SAL-4195-0529 | ROTA | ROTA-2507-417A | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 28/09/2026 | ING | ING-4195-1257 | PENT | PENT-2504-482M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 29/09/2026 | SAL | SAL-4195-0708 | NEUM | NEUM-2507-181K | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 30/09/2026 | SAL | SAL-4195-0934 | ROTA | ROTA-2602-464A | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 30/09/2026 | SAL | SAL-4195-0963 | IPV | IPV-2608-446B | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 01/10/2026 | DEV | DEV-4195-0779 | IPV | IPV-2503-662B | 240 | S | S | S | S | N | N | S | S | N | M5+M6 | Firma pendiente de regularización del responsable. |
| 22 | 01/10/2026 | SAL | SAL-4195-1038 | IPV | IPV-2507-805M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 02/10/2026 | SAL | SAL-4195-1042 | IPV | IPV-2605-698M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 03/10/2026 | TRA | TRA-4195-1727 | NEUM | NEUM-2505-638K | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 03/10/2026 | SAL | SAL-4195-1052 | HEPB | HEPB-2603-786K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 04/10/2026 | ING | ING-4195-1345 | ROTA | ROTA-2602-464A | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 05/10/2026 | SAL | SAL-4195-1486 | SPR | SPR-2606-500M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 05/10/2026 | SAL | SAL-4195-1638 | BCG | BCG-2607-654A | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 06/10/2026 | AJU | AJU-4195-0267 | PENT | PENT-2606-251M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 07/10/2026 | SAL | SAL-4195-2094 | VARI | VARI-2607-979A | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 07/10/2026 | ING | ING-4195-1687 | PENT | PENT-2508-232M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 08/10/2026 | TRA | TRA-4195-1946 | IPV | IPV-2605-698M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 09/10/2026 | TRA | TRA-4195-2030 | SPR | SPR-2603-471K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 09/10/2026 | ING | ING-4195-1833 | HEPB | HEPB-2609-917M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 10/10/2026 | DEV | DEV-4195-0845 | IPV | IPV-2608-446B | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 10/10/2026 | ING | ING-4195-1896 | NEUM | NEUM-2505-688A | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 11/10/2026 | SAL | SAL-4195-2139 | DTA | DTA-2603-463K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 12/10/2026 | TRA | TRA-4195-2185 | INFL | INFL-2604-777M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 12/10/2026 | DEV | DEV-4195-1103 | IPV | IPV-2507-805M | 40 | S | S | N | S | S | S | S | S | N | M3 | Vencimiento registrado sin año; inconsistencia de digitación. |
| 40 | 13/10/2026 | TRA | TRA-4195-2256 | HEPB | HEPB-2603-786K | 150 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-06 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 09/10/2026 | 4195 | NEUM | 40 | 40 | 0 | GR-4195-7921 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 2 | 03/10/2026 | 4195 | IPV | 200 | 200 | 0 | GR-4195-5455 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 3 | 28/09/2026 | 4195 | IPV | 200 | 200 | 0 | GR-4195-4487 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 4 | 19/09/2026 | 4195 | IPV | 60 | 55 | -5 | GR-4195-4224 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 5 | 18/09/2026 | 4195 | ROTA | 60 | 60 | 0 | GR-4195-3537 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 6 | 06/10/2026 | 4195 | VARI | 30 | 30 | 0 | GR-4195-9774 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 7 | 19/09/2026 | 4195 | IPV | 30 | 30 | 0 | GR-4195-1945 | Sí | Conforme. Cantidad y guía coinciden. |
| 8 | 09/10/2026 | 4195 | INFL | 100 | 100 | 0 | GR-4195-7753 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 9 | 29/09/2026 | 4195 | NEUM | 20 | 20 | 0 | GR-4195-4157 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 10 | 03/10/2026 | 4195 | DTA | 60 | 60 | 0 | GR-4195-3093 | Sí | Conforme. Cantidad y guía coinciden. |
| 11 | 16/09/2026 | 4195 | VARI | 180 | 180 | 0 | GR-4195-7096 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 12 | 05/10/2026 | 4195 | VARI | 200 | 200 | 0 | GR-4195-7793 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 13 | 25/09/2026 | 4195 | INFL | 200 | 200 | 0 | GR-4195-8922 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 14 | 20/09/2026 | 4195 | ROTA | 150 | 150 | 0 | GR-4195-3123 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 15 | 13/10/2026 | 4195 | DTA | 60 | 60 | 0 | GR-4195-7041 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 16 | 09/10/2026 | 4195 | PENT | 50 | 50 | 0 | GR-4195-8803 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 17 | 17/09/2026 | 4195 | SPR | 40 | 40 | 0 | GR-4195-9303 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 18 | 04/10/2026 | 4195 | IPV | 50 | 50 | 0 | GR-4195-1264 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 19 | 30/09/2026 | 4195 | IPV | 40 | 40 | 0 | GR-4195-5932 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 20 | 22/09/2026 | 4195 | INFL | 40 | 40 | 0 | GR-4195-1459 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 21 | 04/10/2026 | 4195 | IPV | 20 | 20 | 0 | GR-4195-4331 | Sí | Conforme. Cantidad y guía coinciden. |
| 22 | 28/09/2026 | 4195 | VARI | 100 | 100 | 0 | GR-4195-4245 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 23 | 13/10/2026 | 4195 | ROTA | 180 | 180 | 0 | GR-4195-6745 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 24 | 27/09/2026 | 4195 | BCG | 60 | 60 | 0 | GR-4195-2894 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 25 | 13/10/2026 | 4195 | HEPB | 180 | 180 | 0 | GR-4195-5514 | Sí | Conforme. Cantidad y guía coinciden. |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 13 · TRAB-07 · Pretest (proceso manual) · 13/08/2026

Centro de acopio: **San Jeronimo** (4167-SJ) · Auditor: **OBS-01** · Periodo auditado: **11/07/2026 al 12/08/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 10 · RSD 50.00 %.

Documentos auditados: 40 · Conformes: 21 · RSD: 52.50 % · Entregas conciliadas: 25 · Concordantes: 14 · CPE: 56.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 11/07/2026 | ING | ING-4167SJ-0798 | NEUM | NEUM-2509-952A | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 12/07/2026 | ING | ING-4167SJ-1044 | DTA | DTA-2602-236K | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 13/07/2026 | TRA | TRA-4167SJ-0535 | HEPB | HEPB-2609-521M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 13/07/2026 | DEV | DEV-4167SJ-0184 | VARI | VARI-2509-637K | 200 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 5 | 14/07/2026 | SAL | SAL-4167SJ-0216 | PENT | PENT-2508-232M | 40 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 6 | 15/07/2026 | SAL | SAL-4167SJ-0260 | IPV | IPV-2504-587B | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 16/07/2026 | SAL | SAL-4167SJ-0549 | SPR | SPR-2608-539M | 100 | S | N | S | S | S | S | S | N | N | M2+M8 | Numeración correlativa interrumpida; falta un folio. |
| 8 | 17/07/2026 | AJU | AJU-4167SJ-0190 | NEUM | NEUM-2506-884B | 40 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 9 | 18/07/2026 | ING | ING-4167SJ-1118 | BCG | BCG-2507-694K | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 18/07/2026 | SAL | SAL-4167SJ-0574 | SPR | SPR-2608-539M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 19/07/2026 | TRA | TRA-4167SJ-0656 | IPV | IPV-2504-587B | 50 | S | S | N | S | S | S | S | S | N | M3 | Fecha de vencimiento vencida o ilegible en el asiento. |
| 12 | 20/07/2026 | AJU | AJU-4167SJ-0346 | PENT | PENT-2606-251M | 50 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 13 | 21/07/2026 | SAL | SAL-4167SJ-0596 | PENT | PENT-2605-322M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 22/07/2026 | SAL | SAL-4167SJ-0834 | HEPB | HEPB-2609-917M | 180 | S | S | N | S | S | S | S | S | N | M3 | Fecha de vencimiento vencida o ilegible en el asiento. |
| 15 | 22/07/2026 | SAL | SAL-4167SJ-1123 | PENT | PENT-2508-232M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 23/07/2026 | ING | ING-4167SJ-1374 | HEPB | HEPB-2609-521M | 120 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 17 | 24/07/2026 | SAL | SAL-4167SJ-1439 | DTA | DTA-2603-463K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 25/07/2026 | DEV | DEV-4167SJ-0833 | SPR | SPR-2609-423M | 120 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 19 | 26/07/2026 | ING | ING-4167SJ-1484 | PENT | PENT-2508-232M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 27/07/2026 | SAL | SAL-4167SJ-1500 | PENT | PENT-2508-232M | 80 | N | S | S | S | S | S | S | S | N | M1 | Biológico consignado no corresponde al frasco físico. |
| 21 | 27/07/2026 | SAL | SAL-4167SJ-1698 | NEUM | NEUM-2505-688A | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 28/07/2026 | DEV | DEV-4167SJ-1230 | INFL | INFL-2603-792B | 20 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 23 | 29/07/2026 | SAL | SAL-4167SJ-1706 | HEPB | HEPB-2609-521M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 30/07/2026 | SAL | SAL-4167SJ-1744 | NEUM | NEUM-2505-688A | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 31/07/2026 | ING | ING-4167SJ-1903 | SPR | SPR-2603-471K | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 01/08/2026 | ING | ING-4167SJ-2597 | NEUM | NEUM-2505-688A | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 01/08/2026 | TRA | TRA-4167SJ-0662 | ROTA | ROTA-2507-417A | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 02/08/2026 | DEV | DEV-4167SJ-1254 | IPV | IPV-2504-587B | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 03/08/2026 | SAL | SAL-4167SJ-1964 | BCG | BCG-2606-808K | 20 | S | S | N | N | S | S | S | S | N | M3+M4 | Cantidad física menor a la registrada en el asiento. |
| 30 | 04/08/2026 | SAL | SAL-4167SJ-1990 | HEPB | HEPB-2609-521M | 50 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 31 | 05/08/2026 | TRA | TRA-4167SJ-0734 | DTA | DTA-2602-236K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 05/08/2026 | DEV | DEV-4167SJ-1517 | IPV | IPV-2507-805M | 40 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 33 | 06/08/2026 | TRA | TRA-4167SJ-0808 | IPV | IPV-2504-587B | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 07/08/2026 | TRA | TRA-4167SJ-0874 | DTA | DTA-2602-236K | 150 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 35 | 08/08/2026 | DEV | DEV-4167SJ-1819 | VARI | VARI-2501-250M | 20 | S | N | S | N | S | S | S | S | N | M2+M4 | Cantidad física menor a la registrada en el asiento. |
| 36 | 09/08/2026 | ING | ING-4167SJ-2728 | PENT | PENT-2508-232M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 10/08/2026 | ING | ING-4167SJ-2779 | DTA | DTA-2505-409K | 120 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 38 | 10/08/2026 | ING | ING-4167SJ-2842 | BCG | BCG-2606-808K | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 11/08/2026 | DEV | DEV-4167SJ-2410 | PENT | PENT-2504-482M | 50 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 40 | 12/08/2026 | ING | ING-4167SJ-2879 | IPV | IPV-2608-446B | 180 | S | S | N | S | S | S | N | S | N | M3+M7 | Saldo arrastrado no cuadra con la columna de existencias. |

**Entregas conciliadas — TRAB-07 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 30/07/2026 | 4167-SJ | SPR | 40 | 40 | 0 | GR-4167SJ-8383 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 2 | 23/07/2026 | 4167-SJ | BCG | 150 | 145 | -5 | GR-4167SJ-8716 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 3 | 27/07/2026 | 4167-SJ | ROTA | 180 | 180 | 0 | GR-4167SJ-8736 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 4 | 04/08/2026 | 4167-SJ | INFL | 120 | 115 | -5 | GR-4167SJ-8022 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 5 | 09/08/2026 | 4167-SJ | NEUM | 20 | 20 | 0 | GR-4167SJ-7298 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 6 | 10/08/2026 | 4167-SJ | DTA | 60 | 60 | 0 | GR-4167SJ-4875 | Sí | Conforme. Cantidad y guía coinciden. |
| 7 | 31/07/2026 | 4167-SJ | SPR | 100 | 100 | 0 | GR-4167SJ-8432 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 8 | 31/07/2026 | 4167-SJ | DTA | 20 | 20 | 0 | GR-4167SJ-3921 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 9 | 31/07/2026 | 4167-SJ | INFL | 180 | 185 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 10 | 08/08/2026 | 4167-SJ | INFL | 180 | 170 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 11 | 26/07/2026 | 4167-SJ | IPV | 60 | 60 | 0 | GR-4167SJ-4991 | Sí | Conforme. Cantidad y guía coinciden. |
| 12 | 02/08/2026 | 4167-SJ | DTA | 100 | 100 | 0 | GR-4167SJ-5279 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 13 | 12/08/2026 | 4167-SJ | VARI | 150 | 150 | 0 | GR-4167SJ-7220 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 14 | 18/07/2026 | 4167-SJ | PENT | 40 | 40 | 0 | GR-4167SJ-8240 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 15 | 27/07/2026 | 4167-SJ | PENT | 50 | 40 | -10 | GR-4167SJ-9794 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 16 | 26/07/2026 | 4167-SJ | INFL | 50 | 55 | 5 | GR-4167SJ-3790 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 17 | 11/08/2026 | 4167-SJ | VARI | 40 | 40 | 0 | GR-4167SJ-1428 | Sí | Conforme. Cantidad y guía coinciden. |
| 18 | 27/07/2026 | 4167-SJ | PENT | 180 | 175 | -5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 19 | 10/08/2026 | 4167-SJ | HEPB | 30 | 25 | -5 | GR-4167SJ-5622 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 20 | 05/08/2026 | 4167-SJ | HEPB | 60 | 60 | 0 | GR-4167SJ-4865 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 21 | 29/07/2026 | 4167-SJ | ROTA | 180 | 180 | 0 | GR-4167SJ-2764 | Sí | Conforme. Cantidad y guía coinciden. |
| 22 | 25/07/2026 | 4167-SJ | DTA | 40 | 35 | -5 | GR-4167SJ-6281 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 23 | 30/07/2026 | 4167-SJ | SPR | 150 | 155 | 5 | GR-4167SJ-6810 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 24 | 19/07/2026 | 4167-SJ | DTA | 200 | 220 | 20 | GR-4167SJ-6169 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 25 | 25/07/2026 | 4167-SJ | HEPB | 150 | 150 | 0 | GR-4167SJ-5873 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |

Cierre: 14 entregas concordantes ÷ 25 × 100 = **56.00 %**.

---

### Bloque 14 · TRAB-07 · Postest (Sistema SIVAC) · 15/10/2026

Centro de acopio: **San Jeronimo** (4167-SJ) · Auditor: **OBS-01** · Periodo auditado: **18/09/2026 al 14/10/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 20 · RSD 100.00 %.

Documentos auditados: 40 · Conformes: 40 · RSD: 100.00 % · Entregas conciliadas: 25 · Concordantes: 23 · CPE: 92.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 19/09/2026 | SAL | SAL-4167SJ-0121 | HEPB | HEPB-2602-318M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 20/09/2026 | TRA | TRA-4167SJ-0218 | IPV | IPV-2605-698M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 20/09/2026 | TRA | TRA-4167SJ-0516 | HEPB | HEPB-2602-318M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 21/09/2026 | SAL | SAL-4167SJ-0207 | HEPB | HEPB-2609-521M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 22/09/2026 | SAL | SAL-4167SJ-0349 | PENT | PENT-2508-232M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 22/09/2026 | ING | ING-4167SJ-0169 | VARI | VARI-2503-521A | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 23/09/2026 | DEV | DEV-4167SJ-0307 | PENT | PENT-2508-232M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 23/09/2026 | SAL | SAL-4167SJ-0576 | DTA | DTA-2505-409K | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 24/09/2026 | ING | ING-4167SJ-0321 | HEPB | HEPB-2603-786K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 25/09/2026 | SAL | SAL-4167SJ-0779 | INFL | INFL-2603-792B | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 25/09/2026 | SAL | SAL-4167SJ-0901 | BCG | BCG-2504-789B | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 26/09/2026 | TRA | TRA-4167SJ-0594 | DTA | DTA-2602-236K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 27/09/2026 | ING | ING-4167SJ-0468 | VARI | VARI-2503-521A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 27/09/2026 | SAL | SAL-4167SJ-1432 | SPR | SPR-2608-539M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 28/09/2026 | TRA | TRA-4167SJ-0614 | PENT | PENT-2606-251M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 29/09/2026 | SAL | SAL-4167SJ-1455 | DTA | DTA-2603-463K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 29/09/2026 | TRA | TRA-4167SJ-0960 | BCG | BCG-2607-654A | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 30/09/2026 | ING | ING-4167SJ-0540 | NEUM | NEUM-2505-638K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 01/10/2026 | ING | ING-4167SJ-0592 | HEPB | HEPB-2602-318M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 01/10/2026 | SAL | SAL-4167SJ-1610 | INFL | INFL-2607-737M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 02/10/2026 | SAL | SAL-4167SJ-1820 | HEPB | HEPB-2609-521M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 02/10/2026 | ING | ING-4167SJ-0613 | NEUM | NEUM-2505-688A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 03/10/2026 | ING | ING-4167SJ-1103 | ROTA | ROTA-2605-833M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 04/10/2026 | TRA | TRA-4167SJ-1137 | DTA | DTA-2602-797A | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 04/10/2026 | ING | ING-4167SJ-1261 | INFL | INFL-2504-261K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 05/10/2026 | ING | ING-4167SJ-1389 | DTA | DTA-2602-236K | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 06/10/2026 | AJU | AJU-4167SJ-0117 | SPR | SPR-2608-539M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 06/10/2026 | TRA | TRA-4167SJ-1543 | NEUM | NEUM-2505-638K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 07/10/2026 | AJU | AJU-4167SJ-0249 | PENT | PENT-2606-391A | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 08/10/2026 | ING | ING-4167SJ-1691 | DTA | DTA-2603-463K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 08/10/2026 | ING | ING-4167SJ-1973 | VARI | VARI-2508-818M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 09/10/2026 | SAL | SAL-4167SJ-2158 | HEPB | HEPB-2509-474M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 10/10/2026 | TRA | TRA-4167SJ-1608 | PENT | PENT-2606-391A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 10/10/2026 | SAL | SAL-4167SJ-2368 | HEPB | HEPB-2609-917M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 11/10/2026 | TRA | TRA-4167SJ-1654 | INFL | INFL-2604-777M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 11/10/2026 | ING | ING-4167SJ-2458 | IPV | IPV-2507-805M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 12/10/2026 | TRA | TRA-4167SJ-1701 | INFL | INFL-2604-777M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 13/10/2026 | TRA | TRA-4167SJ-1779 | INFL | INFL-2604-777M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 13/10/2026 | ING | ING-4167SJ-2471 | PENT | PENT-2605-322M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 14/10/2026 | ING | ING-4167SJ-2761 | DTA | DTA-2602-797A | 60 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-07 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 05/10/2026 | 4167-SJ | HEPB | 60 | 60 | 0 | GR-4167SJ-9273 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 2 | 14/10/2026 | 4167-SJ | ROTA | 100 | 100 | 0 | GR-4167SJ-4426 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 3 | 20/09/2026 | 4167-SJ | DTA | 50 | 50 | 0 | GR-4167SJ-7589 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 4 | 18/09/2026 | 4167-SJ | SPR | 180 | 180 | 0 | GR-4167SJ-7609 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 5 | 30/09/2026 | 4167-SJ | VARI | 150 | 150 | 0 | GR-4167SJ-4013 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 6 | 19/09/2026 | 4167-SJ | BCG | 60 | 60 | 0 | GR-4167SJ-4872 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 7 | 01/10/2026 | 4167-SJ | IPV | 50 | 50 | 0 | GR-4167SJ-1468 | Sí | Conforme. Cantidad y guía coinciden. |
| 8 | 19/09/2026 | 4167-SJ | SPR | 60 | 60 | 0 | GR-4167SJ-7299 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 9 | 22/09/2026 | 4167-SJ | BCG | 80 | 80 | 0 | GR-4167SJ-6855 | Sí | Conforme. Cantidad y guía coinciden. |
| 10 | 23/09/2026 | 4167-SJ | HEPB | 50 | 50 | 0 | GR-4167SJ-7905 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 11 | 25/09/2026 | 4167-SJ | BCG | 180 | 180 | 0 | GR-4167SJ-6929 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 12 | 25/09/2026 | 4167-SJ | VARI | 50 | 55 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 13 | 05/10/2026 | 4167-SJ | BCG | 150 | 150 | 0 | GR-4167SJ-8817 | Sí | Conforme. Cantidad y guía coinciden. |
| 14 | 21/09/2026 | 4167-SJ | SPR | 40 | 40 | 0 | GR-4167SJ-3816 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 15 | 07/10/2026 | 4167-SJ | IPV | 40 | 40 | 0 | GR-4167SJ-6802 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 16 | 23/09/2026 | 4167-SJ | NEUM | 100 | 100 | 0 | GR-4167SJ-4904 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 17 | 01/10/2026 | 4167-SJ | HEPB | 80 | 80 | 0 | GR-4167SJ-6822 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 18 | 27/09/2026 | 4167-SJ | VARI | 150 | 150 | 0 | GR-4167SJ-1748 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 19 | 12/10/2026 | 4167-SJ | VARI | 40 | 40 | 0 | GR-4167SJ-4351 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 20 | 12/10/2026 | 4167-SJ | HEPB | 150 | 150 | 0 | GR-4167SJ-3571 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 21 | 30/09/2026 | 4167-SJ | DTA | 20 | 20 | 0 | GR-4167SJ-5299 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 22 | 06/10/2026 | 4167-SJ | SPR | 50 | 55 | 5 | GR-4167SJ-5135 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 23 | 25/09/2026 | 4167-SJ | ROTA | 200 | 200 | 0 | GR-4167SJ-9153 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 24 | 20/09/2026 | 4167-SJ | VARI | 40 | 40 | 0 | GR-4167SJ-6990 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 25 | 26/09/2026 | 4167-SJ | INFL | 200 | 200 | 0 | GR-4167SJ-9129 | Sí | Conforme. Cantidad y guía coinciden. |

Cierre: 23 entregas concordantes ÷ 25 × 100 = **92.00 %**.

---

### Bloque 15 · TRAB-08 · Pretest (proceso manual) · 13/08/2026

Centro de acopio: **Huancaray** (4158) · Auditor: **OBS-02** · Periodo auditado: **13/07/2026 al 12/08/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 15 · RSD 75.00 %.

Documentos auditados: 40 · Conformes: 30 · RSD: 75.00 % · Entregas conciliadas: 25 · Concordantes: 20 · CPE: 80.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 13/07/2026 | ING | ING-4158-0366 | HEPB | HEPB-2609-917M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 14/07/2026 | ING | ING-4158-0566 | DTA | DTA-2505-409K | 120 | S | S | S | S | N | S | S | S | N | M5 | Origen o destino consignado de forma incompleta. |
| 3 | 15/07/2026 | TRA | TRA-4158-0453 | PENT | PENT-2508-232M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 15/07/2026 | ING | ING-4158-0567 | IPV | IPV-2503-662B | 30 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 5 | 16/07/2026 | SAL | SAL-4158-1246 | BCG | BCG-2504-789B | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 17/07/2026 | ING | ING-4158-1231 | BCG | BCG-2607-654A | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 18/07/2026 | ING | ING-4158-1271 | SPR | SPR-2603-471K | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 18/07/2026 | ING | ING-4158-1342 | ROTA | ROTA-2603-156K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 19/07/2026 | ING | ING-4158-1433 | NEUM | NEUM-2507-181K | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 20/07/2026 | ING | ING-4158-1466 | IPV | IPV-2605-698M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 21/07/2026 | DEV | DEV-4158-0440 | INFL | INFL-2607-737M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 21/07/2026 | ING | ING-4158-1677 | IPV | IPV-2605-698M | 30 | S | N | S | S | S | N | S | S | N | M2+M6 | Lote del kardex no coincide con el rotulado del frasco. |
| 13 | 22/07/2026 | SAL | SAL-4158-1374 | NEUM | NEUM-2507-181K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 23/07/2026 | SAL | SAL-4158-1761 | VARI | VARI-2503-521A | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 24/07/2026 | SAL | SAL-4158-1840 | BCG | BCG-2607-654A | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 25/07/2026 | DEV | DEV-4158-0645 | HEPB | HEPB-2603-786K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 25/07/2026 | SAL | SAL-4158-1870 | DTA | DTA-2505-409K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 26/07/2026 | SAL | SAL-4158-1955 | IPV | IPV-2503-662B | 300 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 19 | 27/07/2026 | AJU | AJU-4158-0237 | BCG | BCG-2606-808K | 120 | S | S | S | S | N | S | S | S | N | M5 | Origen o destino consignado de forma incompleta. |
| 20 | 28/07/2026 | ING | ING-4158-1769 | INFL | INFL-2603-792B | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 28/07/2026 | SAL | SAL-4158-1988 | INFL | INFL-2607-737M | 50 | S | S | S | S | N | N | S | S | N | M5+M6 | Origen o destino consignado de forma incompleta. |
| 22 | 29/07/2026 | TRA | TRA-4158-1044 | NEUM | NEUM-2505-638K | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 30/07/2026 | SAL | SAL-4158-2020 | INFL | INFL-2504-261K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 31/07/2026 | TRA | TRA-4158-1176 | SPR | SPR-2603-471K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 31/07/2026 | AJU | AJU-4158-0243 | VARI | VARI-2501-250M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 01/08/2026 | SAL | SAL-4158-2090 | NEUM | NEUM-2505-638K | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 02/08/2026 | SAL | SAL-4158-2220 | PENT | PENT-2606-251M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 03/08/2026 | ING | ING-4158-1888 | HEPB | HEPB-2509-474M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 04/08/2026 | TRA | TRA-4158-1247 | IPV | IPV-2503-662B | 180 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 30 | 04/08/2026 | SAL | SAL-4158-2520 | HEPB | HEPB-2603-786K | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 05/08/2026 | SAL | SAL-4158-2574 | INFL | INFL-2508-359M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 06/08/2026 | ING | ING-4158-1976 | SPR | SPR-2504-185M | 30 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 33 | 07/08/2026 | SAL | SAL-4158-3058 | SPR | SPR-2603-471K | 80 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 34 | 07/08/2026 | TRA | TRA-4158-1482 | VARI | VARI-2503-521A | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 08/08/2026 | ING | ING-4158-2022 | VARI | VARI-2509-637K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 09/08/2026 | SAL | SAL-4158-3165 | NEUM | NEUM-2506-884B | 80 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 37 | 10/08/2026 | SAL | SAL-4158-3192 | SPR | SPR-2609-423M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 10/08/2026 | TRA | TRA-4158-1529 | HEPB | HEPB-2509-474M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 11/08/2026 | SAL | SAL-4158-3433 | BCG | BCG-2507-694K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 12/08/2026 | ING | ING-4158-2163 | SPR | SPR-2609-423M | 180 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-08 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 26/07/2026 | 4158 | ROTA | 150 | 150 | 0 | GR-4158-3958 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 2 | 26/07/2026 | 4158 | INFL | 120 | 120 | 0 | GR-4158-4638 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 3 | 27/07/2026 | 4158 | INFL | 50 | 50 | 0 | GR-4158-9067 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 4 | 11/08/2026 | 4158 | NEUM | 80 | 80 | 0 | GR-4158-2226 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 5 | 03/08/2026 | 4158 | BCG | 50 | 50 | 0 | GR-4158-7299 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 6 | 12/08/2026 | 4158 | NEUM | 60 | 60 | 0 | GR-4158-2464 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 7 | 03/08/2026 | 4158 | HEPB | 100 | 120 | 20 | GR-4158-5440 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 8 | 01/08/2026 | 4158 | VARI | 100 | 100 | 0 | GR-4158-6849 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 9 | 11/08/2026 | 4158 | IPV | 150 | 150 | 0 | GR-4158-1302 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 10 | 26/07/2026 | 4158 | DTA | 30 | 30 | 0 | GR-4158-8967 | Sí | Conforme. Cantidad y guía coinciden. |
| 11 | 11/08/2026 | 4158 | VARI | 100 | 100 | 0 | GR-4158-7180 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 12 | 30/07/2026 | 4158 | ROTA | 200 | 200 | 0 | GR-4158-2373 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 13 | 24/07/2026 | 4158 | HEPB | 180 | 180 | 0 | GR-4158-5162 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 14 | 31/07/2026 | 4158 | DTA | 120 | 120 | 0 | GR-4158-1939 | Sí | Conforme. Cantidad y guía coinciden. |
| 15 | 27/07/2026 | 4158 | INFL | 30 | 30 | 0 | GR-4158-1772 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 16 | 04/08/2026 | 4158 | INFL | 30 | 25 | -5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 17 | 09/08/2026 | 4158 | IPV | 80 | 75 | -5 | GR-4158-5530 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 18 | 25/07/2026 | 4158 | NEUM | 50 | 50 | 0 | GR-4158-3825 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 19 | 01/08/2026 | 4158 | INFL | 120 | 110 | -10 | GR-4158-3719 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 20 | 30/07/2026 | 4158 | ROTA | 50 | 50 | 0 | GR-4158-3752 | Sí | Conforme. Cantidad y guía coinciden. |
| 21 | 23/07/2026 | 4158 | HEPB | 100 | 100 | 0 | GR-4158-6817 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 22 | 09/08/2026 | 4158 | DTA | 50 | 50 | 0 | GR-4158-6025 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 23 | 19/07/2026 | 4158 | SPR | 150 | 150 | 0 | GR-4158-4624 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 24 | 21/07/2026 | 4158 | BCG | 20 | 20 | 0 | GR-4158-7997 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 25 | 11/08/2026 | 4158 | PENT | 180 | 170 | -10 | GR-4158-3238 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |

Cierre: 20 entregas concordantes ÷ 25 × 100 = **80.00 %**.

---

### Bloque 16 · TRAB-08 · Postest (Sistema SIVAC) · 15/10/2026

Centro de acopio: **Huancaray** (4158) · Auditor: **OBS-02** · Periodo auditado: **15/09/2026 al 14/10/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 19 · RSD 95.00 %.

Documentos auditados: 40 · Conformes: 39 · RSD: 97.50 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 15/09/2026 | DEV | DEV-4158-0594 | DTA | DTA-2505-409K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 16/09/2026 | TRA | TRA-4158-0823 | NEUM | NEUM-2505-638K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 16/09/2026 | SAL | SAL-4158-0257 | IPV | IPV-2504-587B | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 17/09/2026 | AJU | AJU-4158-0378 | PENT | PENT-2504-482M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 18/09/2026 | AJU | AJU-4158-0414 | DTA | DTA-2602-236K | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 19/09/2026 | TRA | TRA-4158-1057 | INFL | INFL-2508-359M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 19/09/2026 | AJU | AJU-4158-0716 | ROTA | ROTA-2602-464A | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 20/09/2026 | DEV | DEV-4158-0799 | VARI | VARI-2503-521A | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 21/09/2026 | SAL | SAL-4158-0410 | IPV | IPV-2503-662B | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 22/09/2026 | SAL | SAL-4158-0995 | BCG | BCG-2606-808K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 22/09/2026 | ING | ING-4158-0155 | IPV | IPV-2605-698M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 23/09/2026 | DEV | DEV-4158-0981 | SPR | SPR-2609-423M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 24/09/2026 | AJU | AJU-4158-0932 | ROTA | ROTA-2602-464A | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 25/09/2026 | AJU | AJU-4158-1303 | IPV | IPV-2608-446B | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 25/09/2026 | SAL | SAL-4158-1292 | BCG | BCG-2606-296K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 26/09/2026 | SAL | SAL-4158-1406 | INFL | INFL-2607-737M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 27/09/2026 | AJU | AJU-4158-1472 | INFL | INFL-2603-792B | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 28/09/2026 | SAL | SAL-4158-1762 | VARI | VARI-2508-818M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 28/09/2026 | SAL | SAL-4158-2059 | DTA | DTA-2603-463K | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 29/09/2026 | DEV | DEV-4158-1135 | NEUM | NEUM-2506-884B | 40 | S | S | S | S | S | N | N | S | N | M6+M7 | Saldo no recalculado tras un ajuste autorizado. |
| 21 | 30/09/2026 | SAL | SAL-4158-2218 | VARI | VARI-2508-818M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 01/10/2026 | AJU | AJU-4158-2169 | VARI | VARI-2607-979A | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 01/10/2026 | ING | ING-4158-0197 | HEPB | HEPB-2603-786K | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 02/10/2026 | DEV | DEV-4158-1220 | BCG | BCG-2606-296K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 03/10/2026 | SAL | SAL-4158-2315 | VARI | VARI-2607-979A | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 04/10/2026 | ING | ING-4158-0264 | INFL | INFL-2604-777M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 04/10/2026 | ING | ING-4158-1122 | DTA | DTA-2602-797A | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 05/10/2026 | AJU | AJU-4158-2529 | VARI | VARI-2503-521A | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 06/10/2026 | ING | ING-4158-1229 | NEUM | NEUM-2509-952A | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 07/10/2026 | DEV | DEV-4158-1516 | BCG | BCG-2606-296K | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 07/10/2026 | SAL | SAL-4158-2528 | BCG | BCG-2606-296K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 08/10/2026 | SAL | SAL-4158-2797 | HEPB | HEPB-2509-474M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 09/10/2026 | ING | ING-4158-1400 | VARI | VARI-2508-818M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 10/10/2026 | ING | ING-4158-1546 | HEPB | HEPB-2603-786K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 10/10/2026 | SAL | SAL-4158-2931 | NEUM | NEUM-2507-181K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 11/10/2026 | SAL | SAL-4158-2971 | PENT | PENT-2508-232M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 12/10/2026 | SAL | SAL-4158-3218 | BCG | BCG-2504-789B | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 13/10/2026 | DEV | DEV-4158-1847 | SPR | SPR-2608-539M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 13/10/2026 | TRA | TRA-4158-1151 | VARI | VARI-2501-250M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 14/10/2026 | ING | ING-4158-1753 | SPR | SPR-2609-423M | 300 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-08 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 14/10/2026 | 4158 | ROTA | 40 | 40 | 0 | GR-4158-3490 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 2 | 03/10/2026 | 4158 | SPR | 40 | 40 | 0 | GR-4158-7925 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 3 | 18/09/2026 | 4158 | HEPB | 150 | 150 | 0 | GR-4158-2447 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 4 | 01/10/2026 | 4158 | BCG | 40 | 40 | 0 | GR-4158-2406 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 5 | 03/10/2026 | 4158 | SPR | 30 | 30 | 0 | GR-4158-2941 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 6 | 08/10/2026 | 4158 | NEUM | 100 | 100 | 0 | GR-4158-3063 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 7 | 13/10/2026 | 4158 | HEPB | 150 | 150 | 0 | GR-4158-3339 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 8 | 20/09/2026 | 4158 | SPR | 40 | 40 | 0 | GR-4158-3012 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 9 | 12/10/2026 | 4158 | IPV | 100 | 100 | 0 | GR-4158-2705 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 10 | 14/10/2026 | 4158 | BCG | 120 | 120 | 0 | GR-4158-4511 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 11 | 10/10/2026 | 4158 | HEPB | 50 | 50 | 0 | GR-4158-2766 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 12 | 18/09/2026 | 4158 | SPR | 120 | 120 | 0 | GR-4158-9642 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 13 | 26/09/2026 | 4158 | DTA | 50 | 40 | -10 | GR-4158-8312 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 14 | 05/10/2026 | 4158 | IPV | 60 | 60 | 0 | GR-4158-8198 | Sí | Conforme. Cantidad y guía coinciden. |
| 15 | 21/09/2026 | 4158 | SPR | 20 | 20 | 0 | GR-4158-4148 | Sí | Conforme. Cantidad y guía coinciden. |
| 16 | 19/09/2026 | 4158 | BCG | 120 | 120 | 0 | GR-4158-8501 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 17 | 22/09/2026 | 4158 | BCG | 20 | 20 | 0 | GR-4158-8581 | Sí | Conforme. Cantidad y guía coinciden. |
| 18 | 01/10/2026 | 4158 | VARI | 200 | 200 | 0 | GR-4158-7008 | Sí | Conforme. Cantidad y guía coinciden. |
| 19 | 21/09/2026 | 4158 | PENT | 180 | 180 | 0 | GR-4158-7584 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 20 | 26/09/2026 | 4158 | NEUM | 180 | 180 | 0 | GR-4158-6335 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 21 | 11/10/2026 | 4158 | DTA | 80 | 80 | 0 | GR-4158-6765 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 22 | 17/09/2026 | 4158 | NEUM | 200 | 200 | 0 | GR-4158-4871 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 23 | 12/10/2026 | 4158 | SPR | 200 | 200 | 0 | GR-4158-8203 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 24 | 01/10/2026 | 4158 | SPR | 150 | 150 | 0 | GR-4158-7269 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 25 | 10/10/2026 | 4158 | BCG | 50 | 50 | 0 | GR-4158-4204 | Sí | Conforme. Verificado el FEFO al momento de la carga. |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 17 · TRAB-09 · Pretest (proceso manual) · 14/08/2026

Centro de acopio: **Chicmo** (4202) · Auditor: **OBS-01** · Periodo auditado: **17/07/2026 al 13/08/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 16 · RSD 80.00 %.

Documentos auditados: 40 · Conformes: 29 · RSD: 72.50 % · Entregas conciliadas: 25 · Concordantes: 19 · CPE: 76.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 17/07/2026 | ING | ING-4202-0142 | PENT | PENT-2508-232M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 18/07/2026 | SAL | SAL-4202-0245 | BCG | BCG-2606-296K | 60 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 3 | 18/07/2026 | SAL | SAL-4202-0372 | VARI | VARI-2503-521A | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 19/07/2026 | SAL | SAL-4202-0407 | INFL | INFL-2504-261K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 20/07/2026 | ING | ING-4202-0218 | IPV | IPV-2605-698M | 30 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 6 | 20/07/2026 | ING | ING-4202-0889 | ROTA | ROTA-2605-833M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 21/07/2026 | TRA | TRA-4202-0237 | SPR | SPR-2608-539M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 22/07/2026 | TRA | TRA-4202-0552 | NEUM | NEUM-2505-688A | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 23/07/2026 | SAL | SAL-4202-0520 | INFL | INFL-2607-737M | 150 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 10 | 23/07/2026 | DEV | DEV-4202-0285 | VARI | VARI-2509-637K | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 24/07/2026 | SAL | SAL-4202-0542 | VARI | VARI-2501-250M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 25/07/2026 | SAL | SAL-4202-0810 | SPR | SPR-2608-539M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 25/07/2026 | ING | ING-4202-0893 | HEPB | HEPB-2609-521M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 26/07/2026 | ING | ING-4202-1250 | VARI | VARI-2501-250M | 300 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 15 | 27/07/2026 | DEV | DEV-4202-0600 | BCG | BCG-2606-296K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 27/07/2026 | ING | ING-4202-1527 | ROTA | ROTA-2605-833M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 28/07/2026 | TRA | TRA-4202-0860 | VARI | VARI-2607-979A | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 29/07/2026 | ING | ING-4202-1565 | VARI | VARI-2509-637K | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 29/07/2026 | TRA | TRA-4202-1227 | PENT | PENT-2605-322M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 30/07/2026 | TRA | TRA-4202-1246 | SPR | SPR-2608-539M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 31/07/2026 | SAL | SAL-4202-0817 | IPV | IPV-2503-662B | 180 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 22 | 01/08/2026 | ING | ING-4202-1602 | DTA | DTA-2505-409K | 30 | S | S | S | S | N | S | S | N | N | M5+M8 | Numeración correlativa interrumpida; falta un folio. |
| 23 | 01/08/2026 | SAL | SAL-4202-1001 | IPV | IPV-2503-662B | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 02/08/2026 | DEV | DEV-4202-1213 | SPR | SPR-2609-423M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 03/08/2026 | TRA | TRA-4202-1288 | DTA | DTA-2602-236K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 03/08/2026 | ING | ING-4202-1960 | NEUM | NEUM-2507-181K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 04/08/2026 | ING | ING-4202-2012 | ROTA | ROTA-2603-156K | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 05/08/2026 | SAL | SAL-4202-1309 | NEUM | NEUM-2505-638K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 05/08/2026 | SAL | SAL-4202-1364 | HEPB | HEPB-2603-786K | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 06/08/2026 | ING | ING-4202-2064 | DTA | DTA-2606-829K | 100 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 31 | 07/08/2026 | TRA | TRA-4202-1884 | NEUM | NEUM-2509-952A | 30 | N | S | S | S | N | S | S | S | N | M1+M5 | Biológico consignado no corresponde al frasco físico. |
| 32 | 07/08/2026 | SAL | SAL-4202-2186 | VARI | VARI-2501-250M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 08/08/2026 | SAL | SAL-4202-2404 | ROTA | ROTA-2502-563B | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 09/08/2026 | DEV | DEV-4202-1524 | PENT | PENT-2606-251M | 240 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 35 | 10/08/2026 | TRA | TRA-4202-2501 | VARI | VARI-2509-637K | 50 | N | S | S | S | S | S | S | S | N | M1 | Biológico consignado no corresponde al frasco físico. |
| 36 | 10/08/2026 | SAL | SAL-4202-2512 | DTA | DTA-2603-463K | 60 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 37 | 11/08/2026 | ING | ING-4202-2326 | INFL | INFL-2607-737M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 12/08/2026 | ING | ING-4202-2617 | PENT | PENT-2508-232M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 12/08/2026 | SAL | SAL-4202-2654 | HEPB | HEPB-2609-917M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 13/08/2026 | ING | ING-4202-2621 | ROTA | ROTA-2605-833M | 80 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-09 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 02/08/2026 | 4202 | ROTA | 150 | 150 | 0 | GR-4202-5948 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 2 | 26/07/2026 | 4202 | DTA | 120 | 110 | -10 | GR-4202-3689 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 3 | 13/08/2026 | 4202 | VARI | 30 | 30 | 0 | GR-4202-3241 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 4 | 22/07/2026 | 4202 | DTA | 100 | 100 | 0 | GR-4202-7223 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 5 | 13/08/2026 | 4202 | PENT | 200 | 200 | 0 | GR-4202-8743 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 6 | 31/07/2026 | 4202 | DTA | 120 | 120 | 0 | GR-4202-2847 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 7 | 18/07/2026 | 4202 | VARI | 100 | 100 | 0 | GR-4202-4982 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 8 | 01/08/2026 | 4202 | VARI | 80 | 80 | 0 | GR-4202-4892 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 9 | 10/08/2026 | 4202 | ROTA | 100 | 95 | -5 | GR-4202-5538 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 10 | 27/07/2026 | 4202 | ROTA | 20 | 20 | 0 | GR-4202-9570 | Sí | Conforme. Cantidad y guía coinciden. |
| 11 | 29/07/2026 | 4202 | BCG | 30 | 30 | 0 | GR-4202-4533 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 12 | 27/07/2026 | 4202 | SPR | 120 | 120 | 0 | GR-4202-7713 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 23/07/2026 | 4202 | DTA | 40 | 45 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 14 | 31/07/2026 | 4202 | NEUM | 30 | 30 | 0 | GR-4202-4087 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 15 | 22/07/2026 | 4202 | DTA | 150 | 150 | 0 | GR-4202-5093 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 16 | 11/08/2026 | 4202 | VARI | 40 | 30 | -10 | GR-4202-8509 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 17 | 09/08/2026 | 4202 | DTA | 20 | 15 | -5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 18 | 02/08/2026 | 4202 | VARI | 80 | 80 | 0 | GR-4202-8645 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 19 | 23/07/2026 | 4202 | SPR | 50 | 40 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 20 | 28/07/2026 | 4202 | HEPB | 80 | 80 | 0 | GR-4202-5052 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 21 | 30/07/2026 | 4202 | DTA | 180 | 180 | 0 | GR-4202-2504 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 22 | 20/07/2026 | 4202 | HEPB | 200 | 200 | 0 | GR-4202-8855 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 23 | 19/07/2026 | 4202 | SPR | 60 | 60 | 0 | GR-4202-6777 | Sí | Conforme. Cantidad y guía coinciden. |
| 24 | 30/07/2026 | 4202 | INFL | 200 | 200 | 0 | GR-4202-2834 | Sí | Conforme. Cantidad y guía coinciden. |
| 25 | 12/08/2026 | 4202 | ROTA | 200 | 200 | 0 | GR-4202-8116 | Sí | Conforme. Cantidad y guía coinciden. |

Cierre: 19 entregas concordantes ÷ 25 × 100 = **76.00 %**.

---

### Bloque 18 · TRAB-09 · Postest (Sistema SIVAC) · 16/10/2026

Centro de acopio: **Chicmo** (4202) · Auditor: **OBS-01** · Periodo auditado: **17/09/2026 al 15/10/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 20 · RSD 100.00 %.

Documentos auditados: 40 · Conformes: 39 · RSD: 97.50 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 17/09/2026 | ING | ING-4202-0301 | DTA | DTA-2505-409K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 18/09/2026 | SAL | SAL-4202-0247 | ROTA | ROTA-2605-833M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 18/09/2026 | SAL | SAL-4202-0457 | HEPB | HEPB-2609-917M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 19/09/2026 | SAL | SAL-4202-0736 | BCG | BCG-2606-808K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 20/09/2026 | SAL | SAL-4202-1380 | DTA | DTA-2505-409K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 21/09/2026 | ING | ING-4202-0648 | PENT | PENT-2606-251M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 21/09/2026 | ING | ING-4202-0670 | VARI | VARI-2508-818M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 22/09/2026 | SAL | SAL-4202-1416 | INFL | INFL-2508-359M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 23/09/2026 | DEV | DEV-4202-0479 | VARI | VARI-2607-979A | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 23/09/2026 | SAL | SAL-4202-1533 | INFL | INFL-2504-261K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 24/09/2026 | ING | ING-4202-0824 | INFL | INFL-2607-737M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 25/09/2026 | SAL | SAL-4202-1610 | ROTA | ROTA-2603-156K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 26/09/2026 | ING | ING-4202-1229 | IPV | IPV-2507-805M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 26/09/2026 | SAL | SAL-4202-1923 | DTA | DTA-2505-409K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 27/09/2026 | ING | ING-4202-1267 | ROTA | ROTA-2602-464A | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 28/09/2026 | ING | ING-4202-1277 | PENT | PENT-2504-482M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 28/09/2026 | SAL | SAL-4202-2272 | PENT | PENT-2504-482M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 29/09/2026 | SAL | SAL-4202-2625 | IPV | IPV-2608-446B | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 30/09/2026 | TRA | TRA-4202-0185 | HEPB | HEPB-2602-318M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 01/10/2026 | SAL | SAL-4202-2771 | PENT | PENT-2605-322M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 01/10/2026 | ING | ING-4202-1332 | DTA | DTA-2505-409K | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 02/10/2026 | SAL | SAL-4202-2890 | BCG | BCG-2606-296K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 03/10/2026 | SAL | SAL-4202-3014 | VARI | VARI-2501-250M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 04/10/2026 | ING | ING-4202-1693 | NEUM | NEUM-2505-638K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 04/10/2026 | TRA | TRA-4202-0248 | IPV | IPV-2608-446B | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 05/10/2026 | DEV | DEV-4202-1289 | NEUM | NEUM-2507-181K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 06/10/2026 | TRA | TRA-4202-0405 | ROTA | ROTA-2602-464A | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 06/10/2026 | TRA | TRA-4202-0449 | ROTA | ROTA-2507-417A | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 07/10/2026 | ING | ING-4202-1875 | HEPB | HEPB-2609-521M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 08/10/2026 | SAL | SAL-4202-3700 | DTA | DTA-2603-463K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 09/10/2026 | AJU | AJU-4202-0227 | PENT | PENT-2508-232M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 09/10/2026 | TRA | TRA-4202-0526 | ROTA | ROTA-2605-833M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 10/10/2026 | DEV | DEV-4202-1537 | VARI | VARI-2501-250M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 11/10/2026 | ING | ING-4202-1894 | INFL | INFL-2508-359M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 11/10/2026 | SAL | SAL-4202-4040 | BCG | BCG-2504-789B | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 12/10/2026 | SAL | SAL-4202-4101 | PENT | PENT-2508-232M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 13/10/2026 | ING | ING-4202-2069 | IPV | IPV-2504-587B | 100 | S | S | S | N | S | N | S | S | N | M4+M6 | Firma pendiente de regularización del responsable. |
| 38 | 14/10/2026 | DEV | DEV-4202-1816 | NEUM | NEUM-2509-952A | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 14/10/2026 | TRA | TRA-4202-0695 | HEPB | HEPB-2509-474M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 15/10/2026 | DEV | DEV-4202-1849 | SPR | SPR-2608-539M | 240 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-09 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 29/09/2026 | 4202 | IPV | 60 | 60 | 0 | GR-4202-3659 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 2 | 07/10/2026 | 4202 | IPV | 60 | 60 | 0 | GR-4202-8307 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 3 | 24/09/2026 | 4202 | PENT | 20 | 20 | 0 | GR-4202-1582 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 4 | 30/09/2026 | 4202 | INFL | 60 | 60 | 0 | GR-4202-6429 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 5 | 03/10/2026 | 4202 | NEUM | 180 | 180 | 0 | GR-4202-4746 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 6 | 21/09/2026 | 4202 | INFL | 40 | 45 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 7 | 20/09/2026 | 4202 | BCG | 40 | 40 | 0 | GR-4202-1876 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 8 | 23/09/2026 | 4202 | NEUM | 120 | 120 | 0 | GR-4202-2415 | Sí | Conforme. Cantidad y guía coinciden. |
| 9 | 20/09/2026 | 4202 | VARI | 30 | 30 | 0 | GR-4202-8737 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 10 | 25/09/2026 | 4202 | INFL | 50 | 50 | 0 | GR-4202-3145 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 11 | 21/09/2026 | 4202 | DTA | 50 | 50 | 0 | GR-4202-6375 | Sí | Conforme. Cantidad y guía coinciden. |
| 12 | 19/09/2026 | 4202 | IPV | 120 | 120 | 0 | GR-4202-9105 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 13 | 06/10/2026 | 4202 | VARI | 60 | 60 | 0 | GR-4202-9784 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 14 | 18/09/2026 | 4202 | ROTA | 60 | 60 | 0 | GR-4202-3744 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 15 | 20/09/2026 | 4202 | IPV | 30 | 30 | 0 | GR-4202-4527 | Sí | Conforme. Cantidad y guía coinciden. |
| 16 | 14/10/2026 | 4202 | ROTA | 180 | 180 | 0 | GR-4202-3840 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 17 | 02/10/2026 | 4202 | DTA | 30 | 30 | 0 | GR-4202-6396 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 18 | 30/09/2026 | 4202 | IPV | 30 | 30 | 0 | GR-4202-4107 | Sí | Conforme. Cantidad y guía coinciden. |
| 19 | 20/09/2026 | 4202 | SPR | 150 | 150 | 0 | GR-4202-6320 | Sí | Conforme. Cantidad y guía coinciden. |
| 20 | 26/09/2026 | 4202 | INFL | 20 | 20 | 0 | GR-4202-6561 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 21 | 24/09/2026 | 4202 | NEUM | 20 | 20 | 0 | GR-4202-3006 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 22 | 24/09/2026 | 4202 | DTA | 30 | 30 | 0 | GR-4202-9143 | Sí | Conforme. Cantidad y guía coinciden. |
| 23 | 15/10/2026 | 4202 | NEUM | 80 | 80 | 0 | GR-4202-3186 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 24 | 13/10/2026 | 4202 | BCG | 100 | 100 | 0 | GR-4202-4110 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 25 | 26/09/2026 | 4202 | ROTA | 120 | 120 | 0 | GR-4202-5053 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 19 · TRAB-10 · Pretest (proceso manual) · 14/08/2026

Centro de acopio: **Huancabamba** (4172) · Auditor: **OBS-02** · Periodo auditado: **12/07/2026 al 13/08/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 13 · RSD 65.00 %.

Documentos auditados: 40 · Conformes: 24 · RSD: 60.00 % · Entregas conciliadas: 25 · Concordantes: 16 · CPE: 64.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 12/07/2026 | ING | ING-4172-0194 | NEUM | NEUM-2505-688A | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 13/07/2026 | TRA | TRA-4172-0242 | HEPB | HEPB-2602-318M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 14/07/2026 | ING | ING-4172-0381 | SPR | SPR-2608-539M | 240 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 4 | 14/07/2026 | TRA | TRA-4172-0301 | DTA | DTA-2606-829K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 15/07/2026 | DEV | DEV-4172-0403 | PENT | PENT-2508-232M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 16/07/2026 | ING | ING-4172-0996 | BCG | BCG-2607-654A | 40 | S | S | S | S | N | S | S | S | N | M5 | Origen o destino consignado de forma incompleta. |
| 7 | 17/07/2026 | DEV | DEV-4172-0423 | IPV | IPV-2605-698M | 300 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 8 | 18/07/2026 | DEV | DEV-4172-0608 | PENT | PENT-2606-251M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 19/07/2026 | DEV | DEV-4172-0762 | NEUM | NEUM-2507-181K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 19/07/2026 | TRA | TRA-4172-0371 | DTA | DTA-2603-463K | 50 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 11 | 20/07/2026 | ING | ING-4172-1594 | NEUM | NEUM-2509-952A | 50 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 12 | 21/07/2026 | DEV | DEV-4172-1482 | VARI | VARI-2503-521A | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 22/07/2026 | DEV | DEV-4172-1495 | IPV | IPV-2605-698M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 23/07/2026 | AJU | AJU-4172-0638 | NEUM | NEUM-2505-638K | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 23/07/2026 | SAL | SAL-4172-0296 | IPV | IPV-2507-805M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 24/07/2026 | ING | ING-4172-2235 | INFL | INFL-2504-261K | 240 | N | S | S | S | S | S | S | S | N | M1 | Biológico consignado no corresponde al frasco físico. |
| 17 | 25/07/2026 | AJU | AJU-4172-1665 | NEUM | NEUM-2509-952A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 26/07/2026 | DEV | DEV-4172-1518 | IPV | IPV-2504-587B | 20 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 19 | 27/07/2026 | DEV | DEV-4172-1704 | SPR | SPR-2606-500M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 28/07/2026 | AJU | AJU-4172-2428 | BCG | BCG-2606-296K | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 28/07/2026 | ING | ING-4172-2400 | NEUM | NEUM-2506-884B | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 29/07/2026 | AJU | AJU-4172-2665 | BCG | BCG-2606-808K | 120 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 23 | 30/07/2026 | AJU | AJU-4172-2883 | HEPB | HEPB-2509-474M | 150 | N | S | S | S | S | S | S | N | N | M1+M8 | Biológico consignado no corresponde al frasco físico. |
| 24 | 31/07/2026 | ING | ING-4172-2786 | DTA | DTA-2602-797A | 80 | S | S | S | S | S | N | N | S | N | M6+M7 | Asiento sin firma del responsable del almacén. |
| 25 | 01/08/2026 | DEV | DEV-4172-1924 | SPR | SPR-2608-539M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 02/08/2026 | AJU | AJU-4172-3320 | IPV | IPV-2507-805M | 300 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 27 | 02/08/2026 | TRA | TRA-4172-0868 | BCG | BCG-2606-296K | 300 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 28 | 03/08/2026 | DEV | DEV-4172-2030 | NEUM | NEUM-2507-181K | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 04/08/2026 | TRA | TRA-4172-1062 | INFL | INFL-2504-261K | 40 | S | S | S | S | S | N | N | S | N | M6+M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 30 | 05/08/2026 | DEV | DEV-4172-2319 | INFL | INFL-2603-792B | 40 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 31 | 06/08/2026 | TRA | TRA-4172-2009 | PENT | PENT-2605-322M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 06/08/2026 | ING | ING-4172-2830 | PENT | PENT-2606-251M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 07/08/2026 | SAL | SAL-4172-0517 | IPV | IPV-2605-698M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 08/08/2026 | ING | ING-4172-3223 | SPR | SPR-2606-500M | 60 | S | S | S | S | N | S | N | S | N | M5+M7 | Origen o destino consignado de forma incompleta. |
| 35 | 09/08/2026 | SAL | SAL-4172-0617 | SPR | SPR-2609-423M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 10/08/2026 | TRA | TRA-4172-2128 | BCG | BCG-2606-808K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 11/08/2026 | SAL | SAL-4172-0897 | SPR | SPR-2504-185M | 120 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 38 | 11/08/2026 | AJU | AJU-4172-3465 | IPV | IPV-2605-698M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 12/08/2026 | TRA | TRA-4172-2609 | INFL | INFL-2604-777M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 13/08/2026 | ING | ING-4172-3300 | INFL | INFL-2607-737M | 240 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-10 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 03/08/2026 | 4172 | HEPB | 200 | 200 | 0 | GR-4172-2299 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 2 | 29/07/2026 | 4172 | HEPB | 100 | 90 | -10 | GR-4172-2089 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 3 | 02/08/2026 | 4172 | ROTA | 180 | 180 | 0 | GR-4172-5744 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 4 | 13/08/2026 | 4172 | DTA | 200 | 200 | 0 | GR-4172-9379 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 5 | 09/08/2026 | 4172 | INFL | 150 | 150 | 0 | GR-4172-7524 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 6 | 17/07/2026 | 4172 | IPV | 60 | 50 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 7 | 04/08/2026 | 4172 | SPR | 200 | 205 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 8 | 30/07/2026 | 4172 | NEUM | 40 | 40 | 0 | GR-4172-3875 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 9 | 11/08/2026 | 4172 | PENT | 100 | 100 | 0 | GR-4172-4738 | Sí | Conforme. Cantidad y guía coinciden. |
| 10 | 01/08/2026 | 4172 | IPV | 20 | 20 | 0 | GR-4172-6093 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 11 | 18/07/2026 | 4172 | SPR | 60 | 50 | -10 | GR-4172-2907 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 12 | 30/07/2026 | 4172 | ROTA | 120 | 110 | -10 | GR-4172-6132 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 13 | 17/07/2026 | 4172 | DTA | 150 | 150 | 0 | GR-4172-1744 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 14 | 21/07/2026 | 4172 | NEUM | 200 | 205 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 15 | 30/07/2026 | 4172 | DTA | 150 | 155 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 16 | 10/08/2026 | 4172 | SPR | 20 | 15 | -5 | GR-4172-3281 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 17 | 11/08/2026 | 4172 | VARI | 150 | 150 | 0 | GR-4172-5488 | Sí | Conforme. Cantidad y guía coinciden. |
| 18 | 06/08/2026 | 4172 | ROTA | 40 | 40 | 0 | GR-4172-3711 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 19 | 24/07/2026 | 4172 | ROTA | 100 | 100 | 0 | GR-4172-4756 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 20 | 11/08/2026 | 4172 | SPR | 30 | 10 | -20 | GR-4172-4103 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 21 | 22/07/2026 | 4172 | IPV | 20 | 20 | 0 | GR-4172-6373 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 22 | 26/07/2026 | 4172 | ROTA | 100 | 100 | 0 | GR-4172-7563 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 23 | 13/08/2026 | 4172 | NEUM | 80 | 80 | 0 | GR-4172-9376 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 24 | 29/07/2026 | 4172 | IPV | 100 | 100 | 0 | GR-4172-9762 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 25 | 01/08/2026 | 4172 | NEUM | 20 | 20 | 0 | GR-4172-9486 | Sí | Conforme. Cantidad y guía coinciden. |

Cierre: 16 entregas concordantes ÷ 25 × 100 = **64.00 %**.

---

### Bloque 20 · TRAB-10 · Postest (Sistema SIVAC) · 16/10/2026

Centro de acopio: **Huancabamba** (4172) · Auditor: **OBS-02** · Periodo auditado: **18/09/2026 al 15/10/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 20 · RSD 100.00 %.

Documentos auditados: 40 · Conformes: 39 · RSD: 97.50 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 18/09/2026 | ING | ING-4172-0219 | BCG | BCG-2606-808K | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 19/09/2026 | DEV | DEV-4172-0138 | BCG | BCG-2607-654A | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 19/09/2026 | TRA | TRA-4172-0326 | IPV | IPV-2503-662B | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 20/09/2026 | SAL | SAL-4172-0257 | BCG | BCG-2507-694K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 21/09/2026 | TRA | TRA-4172-0465 | DTA | DTA-2603-463K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 21/09/2026 | ING | ING-4172-0451 | IPV | IPV-2605-698M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 22/09/2026 | AJU | AJU-4172-0979 | ROTA | ROTA-2605-833M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 23/09/2026 | SAL | SAL-4172-0342 | SPR | SPR-2608-539M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 24/09/2026 | SAL | SAL-4172-0578 | ROTA | ROTA-2602-464A | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 24/09/2026 | AJU | AJU-4172-0995 | ROTA | ROTA-2602-464A | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 25/09/2026 | ING | ING-4172-0456 | NEUM | NEUM-2506-884B | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 26/09/2026 | DEV | DEV-4172-0536 | IPV | IPV-2503-662B | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 26/09/2026 | SAL | SAL-4172-0863 | BCG | BCG-2504-789B | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 27/09/2026 | SAL | SAL-4172-1528 | HEPB | HEPB-2509-474M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 28/09/2026 | TRA | TRA-4172-0941 | ROTA | ROTA-2605-833M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 28/09/2026 | DEV | DEV-4172-0596 | HEPB | HEPB-2603-786K | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 29/09/2026 | TRA | TRA-4172-1005 | DTA | DTA-2602-236K | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 30/09/2026 | AJU | AJU-4172-1018 | DTA | DTA-2505-409K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 30/09/2026 | AJU | AJU-4172-1125 | HEPB | HEPB-2609-917M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 01/10/2026 | ING | ING-4172-0524 | HEPB | HEPB-2609-521M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 02/10/2026 | ING | ING-4172-0764 | INFL | INFL-2504-261K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 03/10/2026 | TRA | TRA-4172-1160 | HEPB | HEPB-2603-786K | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 03/10/2026 | TRA | TRA-4172-1456 | ROTA | ROTA-2602-464A | 150 | S | S | S | N | S | S | N | S | N | M4+M7 | Saldo no recalculado tras un ajuste autorizado. |
| 24 | 04/10/2026 | SAL | SAL-4172-1534 | INFL | INFL-2607-737M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 05/10/2026 | TRA | TRA-4172-2495 | PENT | PENT-2606-251M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 05/10/2026 | SAL | SAL-4172-1831 | INFL | INFL-2504-261K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 06/10/2026 | ING | ING-4172-1489 | IPV | IPV-2608-446B | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 07/10/2026 | ING | ING-4172-2240 | PENT | PENT-2606-391A | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 07/10/2026 | TRA | TRA-4172-3111 | PENT | PENT-2504-482M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 08/10/2026 | TRA | TRA-4172-3126 | SPR | SPR-2504-185M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 09/10/2026 | TRA | TRA-4172-3404 | PENT | PENT-2605-322M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 09/10/2026 | ING | ING-4172-2621 | IPV | IPV-2608-446B | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 10/10/2026 | SAL | SAL-4172-2034 | VARI | VARI-2501-250M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 11/10/2026 | ING | ING-4172-2788 | PENT | PENT-2606-391A | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 12/10/2026 | AJU | AJU-4172-1394 | PENT | PENT-2606-391A | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 12/10/2026 | SAL | SAL-4172-2044 | IPV | IPV-2608-446B | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 13/10/2026 | SAL | SAL-4172-2297 | PENT | PENT-2504-482M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 14/10/2026 | AJU | AJU-4172-1512 | BCG | BCG-2504-789B | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 14/10/2026 | ING | ING-4172-2867 | SPR | SPR-2504-185M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 15/10/2026 | SAL | SAL-4172-2897 | VARI | VARI-2501-250M | 150 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-10 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 03/10/2026 | 4172 | INFL | 50 | 50 | 0 | GR-4172-6210 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 2 | 20/09/2026 | 4172 | NEUM | 80 | 80 | 0 | GR-4172-2025 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 3 | 19/09/2026 | 4172 | IPV | 60 | 60 | 0 | GR-4172-7539 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 4 | 12/10/2026 | 4172 | PENT | 80 | 80 | 0 | GR-4172-6040 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 5 | 11/10/2026 | 4172 | NEUM | 200 | 200 | 0 | GR-4172-7963 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 6 | 15/10/2026 | 4172 | IPV | 30 | 30 | 0 | GR-4172-9294 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 7 | 23/09/2026 | 4172 | IPV | 30 | 30 | 0 | GR-4172-7542 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 8 | 02/10/2026 | 4172 | BCG | 50 | 50 | 0 | GR-4172-7949 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 9 | 18/09/2026 | 4172 | VARI | 50 | 45 | -5 | GR-4172-3729 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 10 | 13/10/2026 | 4172 | NEUM | 40 | 40 | 0 | GR-4172-1836 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 11 | 11/10/2026 | 4172 | IPV | 150 | 150 | 0 | GR-4172-2360 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 12 | 25/09/2026 | 4172 | DTA | 150 | 150 | 0 | GR-4172-5539 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 13 | 27/09/2026 | 4172 | DTA | 60 | 60 | 0 | GR-4172-9728 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 14 | 27/09/2026 | 4172 | VARI | 80 | 80 | 0 | GR-4172-2139 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 15 | 23/09/2026 | 4172 | DTA | 40 | 40 | 0 | GR-4172-5867 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 16 | 10/10/2026 | 4172 | ROTA | 20 | 20 | 0 | GR-4172-9450 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 17 | 03/10/2026 | 4172 | IPV | 100 | 100 | 0 | GR-4172-9047 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 18 | 11/10/2026 | 4172 | ROTA | 200 | 200 | 0 | GR-4172-6659 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 19 | 15/10/2026 | 4172 | NEUM | 20 | 20 | 0 | GR-4172-8787 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 20 | 18/09/2026 | 4172 | ROTA | 150 | 150 | 0 | GR-4172-5421 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 21 | 28/09/2026 | 4172 | ROTA | 50 | 50 | 0 | GR-4172-5820 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 22 | 01/10/2026 | 4172 | IPV | 50 | 50 | 0 | GR-4172-8083 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 23 | 06/10/2026 | 4172 | ROTA | 150 | 150 | 0 | GR-4172-2882 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 24 | 12/10/2026 | 4172 | VARI | 200 | 200 | 0 | GR-4172-2435 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 25 | 21/09/2026 | 4172 | HEPB | 180 | 180 | 0 | GR-4172-4413 | Sí | Conforme. Verificado el FEFO al momento de la carga. |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 21 · TRAB-11 · Pretest (proceso manual) · 07/09/2026

Centro de acopio: **Pampachiri** (4167) · Auditor: **OBS-01** · Periodo auditado: **09/08/2026 al 06/09/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 12 · RSD 60.00 %.

Documentos auditados: 40 · Conformes: 25 · RSD: 62.50 % · Entregas conciliadas: 25 · Concordantes: 17 · CPE: 68.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 09/08/2026 | SAL | SAL-4167-0273 | HEPB | HEPB-2609-917M | 300 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 2 | 10/08/2026 | ING | ING-4167-0326 | PENT | PENT-2605-322M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 10/08/2026 | DEV | DEV-4167-0387 | SPR | SPR-2606-500M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 11/08/2026 | ING | ING-4167-0531 | NEUM | NEUM-2507-181K | 240 | N | S | S | S | S | S | S | S | N | M1 | Biológico consignado no corresponde al frasco físico. |
| 5 | 12/08/2026 | DEV | DEV-4167-0648 | INFL | INFL-2508-359M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 13/08/2026 | SAL | SAL-4167-0564 | VARI | VARI-2501-250M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 13/08/2026 | TRA | TRA-4167-0180 | PENT | PENT-2605-322M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 14/08/2026 | SAL | SAL-4167-1271 | ROTA | ROTA-2507-417A | 100 | S | S | N | S | S | S | S | S | N | M3 | Fecha de vencimiento vencida o ilegible en el asiento. |
| 9 | 15/08/2026 | TRA | TRA-4167-0408 | DTA | DTA-2603-463K | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 15/08/2026 | TRA | TRA-4167-0441 | NEUM | NEUM-2509-952A | 80 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 11 | 16/08/2026 | ING | ING-4167-0758 | VARI | VARI-2509-637K | 40 | S | S | S | S | N | S | N | S | N | M5+M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 12 | 17/08/2026 | DEV | DEV-4167-0705 | HEPB | HEPB-2509-474M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 18/08/2026 | SAL | SAL-4167-1327 | DTA | DTA-2606-829K | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 18/08/2026 | ING | ING-4167-1157 | HEPB | HEPB-2603-786K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 19/08/2026 | ING | ING-4167-1210 | HEPB | HEPB-2609-521M | 40 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 16 | 20/08/2026 | SAL | SAL-4167-1494 | IPV | IPV-2507-805M | 20 | N | S | S | N | S | S | S | S | N | M1+M4 | Cantidad física menor a la registrada en el asiento. |
| 17 | 20/08/2026 | SAL | SAL-4167-1822 | DTA | DTA-2606-829K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 21/08/2026 | ING | ING-4167-1565 | ROTA | ROTA-2602-464A | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 22/08/2026 | ING | ING-4167-1733 | VARI | VARI-2508-818M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 23/08/2026 | TRA | TRA-4167-1415 | SPR | SPR-2608-539M | 60 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 21 | 23/08/2026 | SAL | SAL-4167-1952 | INFL | INFL-2504-261K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 24/08/2026 | SAL | SAL-4167-1982 | DTA | DTA-2602-236K | 20 | S | S | S | S | N | S | S | S | N | M5 | Origen o destino consignado de forma incompleta. |
| 23 | 25/08/2026 | TRA | TRA-4167-1514 | NEUM | NEUM-2507-181K | 180 | S | S | N | S | S | S | S | S | N | M3 | Fecha de vencimiento vencida o ilegible en el asiento. |
| 24 | 26/08/2026 | ING | ING-4167-2278 | BCG | BCG-2507-694K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 26/08/2026 | TRA | TRA-4167-1587 | VARI | VARI-2607-979A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 27/08/2026 | SAL | SAL-4167-2292 | PENT | PENT-2606-391A | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 28/08/2026 | DEV | DEV-4167-1051 | INFL | INFL-2603-792B | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 28/08/2026 | TRA | TRA-4167-1759 | HEPB | HEPB-2609-917M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 29/08/2026 | TRA | TRA-4167-1940 | VARI | VARI-2503-521A | 150 | N | S | S | S | S | S | S | S | N | M1 | Biológico consignado no corresponde al frasco físico. |
| 30 | 30/08/2026 | ING | ING-4167-2507 | ROTA | ROTA-2605-833M | 100 | S | S | S | S | N | S | S | S | N | M5 | Origen o destino consignado de forma incompleta. |
| 31 | 31/08/2026 | ING | ING-4167-2558 | BCG | BCG-2606-296K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 31/08/2026 | SAL | SAL-4167-2323 | INFL | INFL-2603-792B | 20 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 33 | 01/09/2026 | ING | ING-4167-3124 | SPR | SPR-2606-500M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 02/09/2026 | SAL | SAL-4167-2439 | ROTA | ROTA-2603-156K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 02/09/2026 | ING | ING-4167-3282 | DTA | DTA-2602-797A | 60 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 36 | 03/09/2026 | ING | ING-4167-3400 | SPR | SPR-2603-471K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 04/09/2026 | SAL | SAL-4167-2557 | VARI | VARI-2508-818M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 05/09/2026 | TRA | TRA-4167-2152 | PENT | PENT-2504-482M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 05/09/2026 | TRA | TRA-4167-2388 | INFL | INFL-2603-792B | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 06/09/2026 | ING | ING-4167-3670 | VARI | VARI-2509-637K | 150 | S | S | S | N | S | S | N | S | N | M4+M7 | Cantidad física menor a la registrada en el asiento. |

**Entregas conciliadas — TRAB-11 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 06/09/2026 | 4167 | VARI | 200 | 200 | 0 | GR-4167-1211 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 2 | 14/08/2026 | 4167 | INFL | 20 | 20 | 0 | GR-4167-7815 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 3 | 29/08/2026 | 4167 | SPR | 150 | 150 | 0 | GR-4167-4643 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 4 | 14/08/2026 | 4167 | PENT | 50 | 50 | 0 | GR-4167-8191 | Sí | Conforme. Cantidad y guía coinciden. |
| 5 | 28/08/2026 | 4167 | DTA | 120 | 120 | 0 | GR-4167-3964 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 6 | 21/08/2026 | 4167 | INFL | 30 | 30 | 0 | GR-4167-7702 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 7 | 19/08/2026 | 4167 | VARI | 50 | 50 | 0 | GR-4167-1387 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 8 | 17/08/2026 | 4167 | HEPB | 100 | 100 | 0 | GR-4167-4834 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 9 | 05/09/2026 | 4167 | INFL | 180 | 170 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 10 | 01/09/2026 | 4167 | IPV | 80 | 75 | -5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 11 | 20/08/2026 | 4167 | DTA | 60 | 55 | -5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 12 | 15/08/2026 | 4167 | ROTA | 100 | 100 | 0 | GR-4167-3772 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 05/09/2026 | 4167 | ROTA | 80 | 80 | 0 | GR-4167-3469 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 14 | 05/09/2026 | 4167 | SPR | 80 | 60 | -20 | GR-4167-3782 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 15 | 31/08/2026 | 4167 | PENT | 40 | 40 | 0 | GR-4167-4546 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 16 | 19/08/2026 | 4167 | DTA | 80 | 75 | -5 | GR-4167-4070 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 17 | 12/08/2026 | 4167 | NEUM | 180 | 180 | 0 | GR-4167-4850 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 18 | 11/08/2026 | 4167 | ROTA | 20 | 20 | 0 | GR-4167-4434 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 19 | 29/08/2026 | 4167 | DTA | 30 | 25 | -5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 20 | 11/08/2026 | 4167 | DTA | 60 | 60 | 0 | GR-4167-3263 | Sí | Conforme. Cantidad y guía coinciden. |
| 21 | 05/09/2026 | 4167 | HEPB | 40 | 40 | 0 | GR-4167-2689 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 22 | 28/08/2026 | 4167 | HEPB | 60 | 60 | 0 | GR-4167-4886 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 23 | 30/08/2026 | 4167 | INFL | 120 | 110 | -10 | GR-4167-8823 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 24 | 25/08/2026 | 4167 | HEPB | 20 | 20 | 0 | GR-4167-6865 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 25 | 14/08/2026 | 4167 | INFL | 40 | 60 | 20 | GR-4167-2484 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |

Cierre: 17 entregas concordantes ÷ 25 × 100 = **68.00 %**.

---

### Bloque 22 · TRAB-11 · Postest (Sistema SIVAC) · 19/10/2026

Centro de acopio: **Pampachiri** (4167) · Auditor: **OBS-01** · Periodo auditado: **15/09/2026 al 18/10/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 20 · RSD 100.00 %.

Documentos auditados: 40 · Conformes: 38 · RSD: 95.00 % · Entregas conciliadas: 25 · Concordantes: 23 · CPE: 92.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 15/09/2026 | SAL | SAL-4167-0225 | ROTA | ROTA-2602-464A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 16/09/2026 | ING | ING-4167-0187 | IPV | IPV-2608-446B | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 17/09/2026 | ING | ING-4167-0228 | HEPB | HEPB-2603-786K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 18/09/2026 | TRA | TRA-4167-0323 | SPR | SPR-2608-539M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 18/09/2026 | SAL | SAL-4167-0901 | BCG | BCG-2507-694K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 19/09/2026 | AJU | AJU-4167-0605 | IPV | IPV-2503-662B | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 20/09/2026 | ING | ING-4167-0266 | HEPB | HEPB-2609-521M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 21/09/2026 | SAL | SAL-4167-1023 | PENT | PENT-2504-482M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 22/09/2026 | AJU | AJU-4167-0623 | ROTA | ROTA-2605-833M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 23/09/2026 | SAL | SAL-4167-1084 | ROTA | ROTA-2605-833M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 23/09/2026 | ING | ING-4167-0894 | ROTA | ROTA-2507-417A | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 24/09/2026 | TRA | TRA-4167-0510 | HEPB | HEPB-2609-521M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 25/09/2026 | SAL | SAL-4167-1107 | DTA | DTA-2505-409K | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 26/09/2026 | TRA | TRA-4167-0605 | ROTA | ROTA-2605-833M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 27/09/2026 | SAL | SAL-4167-2153 | NEUM | NEUM-2505-688A | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 28/09/2026 | SAL | SAL-4167-2440 | ROTA | ROTA-2502-563B | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 29/09/2026 | TRA | TRA-4167-0875 | HEPB | HEPB-2603-786K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 29/09/2026 | AJU | AJU-4167-1140 | SPR | SPR-2606-500M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 30/09/2026 | AJU | AJU-4167-1153 | IPV | IPV-2503-662B | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 01/10/2026 | TRA | TRA-4167-0923 | SPR | SPR-2603-471K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 02/10/2026 | SAL | SAL-4167-2513 | ROTA | ROTA-2507-417A | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 03/10/2026 | TRA | TRA-4167-0986 | DTA | DTA-2603-463K | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 04/10/2026 | TRA | TRA-4167-1003 | BCG | BCG-2504-789B | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 04/10/2026 | ING | ING-4167-1356 | INFL | INFL-2504-261K | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 05/10/2026 | AJU | AJU-4167-1215 | VARI | VARI-2509-637K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 06/10/2026 | TRA | TRA-4167-1661 | BCG | BCG-2606-808K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 07/10/2026 | SAL | SAL-4167-2586 | IPV | IPV-2605-698M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 08/10/2026 | SAL | SAL-4167-3665 | VARI | VARI-2508-818M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 09/10/2026 | DEV | DEV-4167-1276 | NEUM | NEUM-2505-638K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 10/10/2026 | DEV | DEV-4167-1894 | BCG | BCG-2607-654A | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 10/10/2026 | TRA | TRA-4167-1702 | PENT | PENT-2504-482M | 300 | S | S | S | N | S | S | S | N | N | M4+M8 | Correlativo duplicado por reintento de grabación. |
| 32 | 11/10/2026 | ING | ING-4167-1600 | PENT | PENT-2606-391A | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 12/10/2026 | DEV | DEV-4167-2302 | DTA | DTA-2602-236K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 13/10/2026 | SAL | SAL-4167-3721 | INFL | INFL-2604-777M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 14/10/2026 | ING | ING-4167-1846 | DTA | DTA-2602-797A | 100 | S | S | S | S | S | S | S | N | N | M8 | Correlativo duplicado por reintento de grabación. |
| 36 | 15/10/2026 | SAL | SAL-4167-3838 | PENT | PENT-2606-391A | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 15/10/2026 | TRA | TRA-4167-2140 | PENT | PENT-2508-232M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 16/10/2026 | SAL | SAL-4167-4089 | BCG | BCG-2607-654A | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 17/10/2026 | SAL | SAL-4167-4095 | SPR | SPR-2603-471K | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 18/10/2026 | AJU | AJU-4167-1361 | NEUM | NEUM-2505-638K | 300 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-11 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 27/09/2026 | 4167 | SPR | 30 | 20 | -10 | GR-4167-8318 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 2 | 18/10/2026 | 4167 | DTA | 30 | 30 | 0 | GR-4167-5445 | Sí | Conforme. Cantidad y guía coinciden. |
| 3 | 11/10/2026 | 4167 | ROTA | 80 | 80 | 0 | GR-4167-4397 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 4 | 11/10/2026 | 4167 | PENT | 180 | 180 | 0 | GR-4167-5105 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 5 | 10/10/2026 | 4167 | VARI | 50 | 50 | 0 | GR-4167-2083 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 6 | 29/09/2026 | 4167 | HEPB | 50 | 50 | 0 | GR-4167-6731 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 7 | 24/09/2026 | 4167 | HEPB | 180 | 180 | 0 | GR-4167-7974 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 8 | 22/09/2026 | 4167 | HEPB | 60 | 60 | 0 | GR-4167-5938 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 9 | 29/09/2026 | 4167 | DTA | 60 | 60 | 0 | GR-4167-6730 | Sí | Conforme. Cantidad y guía coinciden. |
| 10 | 23/09/2026 | 4167 | PENT | 200 | 200 | 0 | GR-4167-2959 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 11 | 08/10/2026 | 4167 | SPR | 180 | 180 | 0 | GR-4167-2494 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 12 | 25/09/2026 | 4167 | ROTA | 40 | 40 | 0 | GR-4167-3307 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 13 | 11/10/2026 | 4167 | DTA | 150 | 150 | 0 | GR-4167-9209 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 14 | 01/10/2026 | 4167 | IPV | 30 | 30 | 0 | GR-4167-6528 | Sí | Conforme. Cantidad y guía coinciden. |
| 15 | 05/10/2026 | 4167 | SPR | 60 | 60 | 0 | GR-4167-1406 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 16 | 18/10/2026 | 4167 | ROTA | 100 | 100 | 0 | GR-4167-6920 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 17 | 15/10/2026 | 4167 | DTA | 150 | 150 | 0 | GR-4167-6556 | Sí | Conforme. Cantidad y guía coinciden. |
| 18 | 12/10/2026 | 4167 | VARI | 100 | 100 | 0 | GR-4167-5641 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 19 | 16/10/2026 | 4167 | IPV | 40 | 40 | 0 | GR-4167-7127 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 20 | 23/09/2026 | 4167 | PENT | 30 | 30 | 0 | GR-4167-7629 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 21 | 13/10/2026 | 4167 | IPV | 100 | 100 | 0 | GR-4167-9342 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 22 | 17/10/2026 | 4167 | ROTA | 50 | 70 | 20 | GR-4167-1862 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 23 | 04/10/2026 | 4167 | SPR | 100 | 100 | 0 | GR-4167-1745 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 24 | 17/10/2026 | 4167 | IPV | 80 | 80 | 0 | GR-4167-1648 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 25 | 09/10/2026 | 4167 | PENT | 50 | 50 | 0 | GR-4167-3398 | Sí | Conforme. Verificado el FEFO al momento de la carga. |

Cierre: 23 entregas concordantes ÷ 25 × 100 = **92.00 %**.

---

### Bloque 23 · TRAB-12 · Pretest (proceso manual) · 07/09/2026

Centro de acopio: **San Antonio de Cachi** (4160) · Auditor: **OBS-02** · Periodo auditado: **09/08/2026 al 06/09/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 13 · RSD 65.00 %.

Documentos auditados: 40 · Conformes: 23 · RSD: 57.50 % · Entregas conciliadas: 25 · Concordantes: 15 · CPE: 60.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 09/08/2026 | TRA | TRA-4160-0168 | DTA | DTA-2602-797A | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 10/08/2026 | ING | ING-4160-0331 | DTA | DTA-2602-797A | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 10/08/2026 | SAL | SAL-4160-0535 | SPR | SPR-2504-185M | 60 | S | S | S | S | N | S | S | S | N | M5 | Origen o destino consignado de forma incompleta. |
| 4 | 11/08/2026 | TRA | TRA-4160-0771 | ROTA | ROTA-2605-833M | 20 | S | N | N | S | S | S | S | S | N | M2+M3 | Fecha de vencimiento vencida o ilegible en el asiento. |
| 5 | 12/08/2026 | ING | ING-4160-0540 | ROTA | ROTA-2605-833M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 13/08/2026 | ING | ING-4160-0545 | SPR | SPR-2504-185M | 200 | S | N | S | S | S | S | N | S | N | M2+M7 | Lote del kardex no coincide con el rotulado del frasco. |
| 7 | 13/08/2026 | ING | ING-4160-0791 | DTA | DTA-2505-409K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 14/08/2026 | SAL | SAL-4160-0642 | BCG | BCG-2606-296K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 15/08/2026 | ING | ING-4160-1011 | VARI | VARI-2501-250M | 200 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 10 | 15/08/2026 | SAL | SAL-4160-0825 | PENT | PENT-2504-482M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 16/08/2026 | SAL | SAL-4160-1135 | VARI | VARI-2508-818M | 80 | S | S | S | S | N | S | S | S | N | M5 | Origen o destino consignado de forma incompleta. |
| 12 | 17/08/2026 | DEV | DEV-4160-0258 | NEUM | NEUM-2507-181K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 18/08/2026 | ING | ING-4160-1096 | DTA | DTA-2606-829K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 18/08/2026 | TRA | TRA-4160-1016 | ROTA | ROTA-2603-156K | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 19/08/2026 | TRA | TRA-4160-1643 | DTA | DTA-2505-409K | 150 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 16 | 20/08/2026 | ING | ING-4160-1264 | IPV | IPV-2507-805M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 20/08/2026 | TRA | TRA-4160-1675 | INFL | INFL-2604-777M | 100 | S | S | S | N | S | S | S | S | N | M4 | Cantidad física menor a la registrada en el asiento. |
| 18 | 21/08/2026 | SAL | SAL-4160-1339 | PENT | PENT-2606-251M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 22/08/2026 | SAL | SAL-4160-1593 | PENT | PENT-2605-322M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 23/08/2026 | AJU | AJU-4160-0293 | IPV | IPV-2608-446B | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 23/08/2026 | TRA | TRA-4160-1762 | VARI | VARI-2501-250M | 300 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 22 | 24/08/2026 | TRA | TRA-4160-1945 | INFL | INFL-2504-261K | 300 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 23 | 25/08/2026 | DEV | DEV-4160-0618 | HEPB | HEPB-2509-474M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 26/08/2026 | SAL | SAL-4160-1876 | SPR | SPR-2603-471K | 20 | N | N | S | S | S | S | S | S | N | M1+M2 | Biológico consignado no corresponde al frasco físico. |
| 25 | 26/08/2026 | SAL | SAL-4160-2226 | HEPB | HEPB-2609-917M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 27/08/2026 | DEV | DEV-4160-0830 | ROTA | ROTA-2507-417A | 200 | S | S | S | S | N | S | S | S | N | M5 | Origen o destino consignado de forma incompleta. |
| 27 | 28/08/2026 | ING | ING-4160-1851 | DTA | DTA-2505-409K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 28/08/2026 | AJU | AJU-4160-1037 | DTA | DTA-2606-829K | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 29/08/2026 | ING | ING-4160-1852 | NEUM | NEUM-2506-884B | 40 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 30 | 30/08/2026 | AJU | AJU-4160-1054 | BCG | BCG-2606-808K | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 31/08/2026 | TRA | TRA-4160-2295 | VARI | VARI-2503-521A | 200 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 32 | 31/08/2026 | SAL | SAL-4160-2390 | PENT | PENT-2605-322M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 01/09/2026 | DEV | DEV-4160-0845 | SPR | SPR-2504-185M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 02/09/2026 | TRA | TRA-4160-2485 | HEPB | HEPB-2509-474M | 100 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 35 | 02/09/2026 | SAL | SAL-4160-2479 | VARI | VARI-2503-521A | 60 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 36 | 03/09/2026 | SAL | SAL-4160-2683 | PENT | PENT-2504-482M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 04/09/2026 | AJU | AJU-4160-1230 | VARI | VARI-2509-637K | 50 | S | S | S | S | N | S | S | S | N | M5 | Origen o destino consignado de forma incompleta. |
| 38 | 05/09/2026 | TRA | TRA-4160-2824 | ROTA | ROTA-2602-464A | 50 | S | S | S | S | N | N | S | S | N | M5+M6 | Asiento sin firma del responsable del almacén. |
| 39 | 05/09/2026 | SAL | SAL-4160-2767 | BCG | BCG-2607-654A | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 06/09/2026 | SAL | SAL-4160-3386 | PENT | PENT-2508-232M | 200 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-12 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 18/08/2026 | 4160 | HEPB | 80 | 80 | 0 | GR-4160-9178 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 2 | 02/09/2026 | 4160 | ROTA | 100 | 100 | 0 | GR-4160-2390 | Sí | Conforme. Cantidad y guía coinciden. |
| 3 | 31/08/2026 | 4160 | HEPB | 50 | 40 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 4 | 24/08/2026 | 4160 | NEUM | 50 | 50 | 0 | GR-4160-7766 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 5 | 01/09/2026 | 4160 | ROTA | 60 | 60 | 0 | GR-4160-2946 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 6 | 03/09/2026 | 4160 | IPV | 50 | 50 | 0 | GR-4160-4738 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 7 | 04/09/2026 | 4160 | BCG | 120 | 120 | 0 | GR-4160-3216 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 8 | 10/08/2026 | 4160 | NEUM | 50 | 50 | 0 | GR-4160-2793 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 9 | 16/08/2026 | 4160 | SPR | 40 | 40 | 0 | GR-4160-5778 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 10 | 30/08/2026 | 4160 | ROTA | 200 | 205 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 11 | 23/08/2026 | 4160 | NEUM | 60 | 60 | 0 | GR-4160-1903 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 12 | 14/08/2026 | 4160 | IPV | 20 | 20 | 0 | GR-4160-7159 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 13 | 19/08/2026 | 4160 | PENT | 80 | 90 | 10 | GR-4160-2370 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 14 | 18/08/2026 | 4160 | VARI | 180 | 180 | 0 | GR-4160-5412 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 15 | 21/08/2026 | 4160 | INFL | 20 | 25 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 16 | 25/08/2026 | 4160 | NEUM | 80 | 70 | -10 | GR-4160-7730 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 17 | 14/08/2026 | 4160 | HEPB | 100 | 105 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 18 | 17/08/2026 | 4160 | ROTA | 80 | 80 | 0 | GR-4160-9764 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 19 | 14/08/2026 | 4160 | HEPB | 50 | 40 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 20 | 25/08/2026 | 4160 | PENT | 50 | 40 | -10 | GR-4160-9463 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 21 | 25/08/2026 | 4160 | PENT | 20 | 20 | 0 | GR-4160-7681 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 22 | 22/08/2026 | 4160 | NEUM | 60 | 60 | 0 | GR-4160-1619 | Sí | Conforme. Cantidad y guía coinciden. |
| 23 | 13/08/2026 | 4160 | PENT | 80 | 80 | 0 | GR-4160-1989 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 24 | 28/08/2026 | 4160 | ROTA | 120 | 140 | 20 | GR-4160-4715 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 25 | 06/09/2026 | 4160 | SPR | 80 | 85 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |

Cierre: 15 entregas concordantes ÷ 25 × 100 = **60.00 %**.

---

### Bloque 24 · TRAB-12 · Postest (Sistema SIVAC) · 19/10/2026

Centro de acopio: **San Antonio de Cachi** (4160) · Auditor: **OBS-02** · Periodo auditado: **17/09/2026 al 18/10/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 19 · RSD 95.00 %.

Documentos auditados: 40 · Conformes: 39 · RSD: 97.50 % · Entregas conciliadas: 25 · Concordantes: 23 · CPE: 92.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 17/09/2026 | TRA | TRA-4160-0234 | BCG | BCG-2507-694K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 18/09/2026 | TRA | TRA-4160-0291 | BCG | BCG-2606-296K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 19/09/2026 | SAL | SAL-4160-0354 | BCG | BCG-2607-654A | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 19/09/2026 | ING | ING-4160-0250 | DTA | DTA-2606-829K | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 20/09/2026 | ING | ING-4160-0453 | HEPB | HEPB-2609-521M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 21/09/2026 | SAL | SAL-4160-0706 | NEUM | NEUM-2506-884B | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 22/09/2026 | ING | ING-4160-0695 | HEPB | HEPB-2603-786K | 150 | S | S | S | N | S | S | N | S | N | M4+M7 | Saldo no recalculado tras un ajuste autorizado. |
| 8 | 23/09/2026 | SAL | SAL-4160-0843 | SPR | SPR-2608-539M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 23/09/2026 | AJU | AJU-4160-0174 | IPV | IPV-2605-698M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 24/09/2026 | SAL | SAL-4160-2030 | PENT | PENT-2606-391A | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 25/09/2026 | SAL | SAL-4160-2127 | BCG | BCG-2504-789B | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 26/09/2026 | ING | ING-4160-0737 | HEPB | HEPB-2509-474M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 27/09/2026 | SAL | SAL-4160-2150 | VARI | VARI-2501-250M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 27/09/2026 | SAL | SAL-4160-2288 | SPR | SPR-2606-500M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 28/09/2026 | ING | ING-4160-1429 | BCG | BCG-2507-694K | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 29/09/2026 | TRA | TRA-4160-0519 | SPR | SPR-2606-500M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 30/09/2026 | SAL | SAL-4160-2981 | DTA | DTA-2602-797A | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 01/10/2026 | ING | ING-4160-1528 | INFL | INFL-2603-792B | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 01/10/2026 | ING | ING-4160-1816 | INFL | INFL-2504-261K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 02/10/2026 | AJU | AJU-4160-0720 | ROTA | ROTA-2602-464A | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 03/10/2026 | TRA | TRA-4160-1134 | PENT | PENT-2504-482M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 04/10/2026 | AJU | AJU-4160-1385 | PENT | PENT-2606-251M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 04/10/2026 | ING | ING-4160-2210 | INFL | INFL-2504-261K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 05/10/2026 | ING | ING-4160-2321 | ROTA | ROTA-2507-417A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 06/10/2026 | SAL | SAL-4160-3055 | DTA | DTA-2602-236K | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 07/10/2026 | ING | ING-4160-2713 | PENT | PENT-2504-482M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 08/10/2026 | AJU | AJU-4160-1951 | BCG | BCG-2607-654A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 08/10/2026 | SAL | SAL-4160-3128 | HEPB | HEPB-2509-474M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 09/10/2026 | TRA | TRA-4160-1878 | INFL | INFL-2603-792B | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 10/10/2026 | SAL | SAL-4160-3184 | INFL | INFL-2508-359M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 11/10/2026 | DEV | DEV-4160-0240 | NEUM | NEUM-2505-638K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 12/10/2026 | SAL | SAL-4160-3544 | DTA | DTA-2602-797A | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 12/10/2026 | ING | ING-4160-2774 | SPR | SPR-2504-185M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 13/10/2026 | AJU | AJU-4160-1964 | NEUM | NEUM-2509-952A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 14/10/2026 | AJU | AJU-4160-2102 | NEUM | NEUM-2505-688A | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 15/10/2026 | TRA | TRA-4160-1918 | SPR | SPR-2504-185M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 16/10/2026 | ING | ING-4160-3379 | ROTA | ROTA-2507-417A | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 16/10/2026 | ING | ING-4160-3475 | ROTA | ROTA-2507-417A | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 17/10/2026 | SAL | SAL-4160-3572 | NEUM | NEUM-2509-952A | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 18/10/2026 | SAL | SAL-4160-3705 | NEUM | NEUM-2509-952A | 240 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-12 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 06/10/2026 | 4160 | PENT | 120 | 120 | 0 | GR-4160-1801 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 2 | 26/09/2026 | 4160 | SPR | 180 | 180 | 0 | GR-4160-3137 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 3 | 13/10/2026 | 4160 | ROTA | 150 | 150 | 0 | GR-4160-1641 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 4 | 22/09/2026 | 4160 | INFL | 200 | 200 | 0 | GR-4160-8194 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 5 | 04/10/2026 | 4160 | SPR | 100 | 100 | 0 | GR-4160-3844 | Sí | Conforme. Cantidad y guía coinciden. |
| 6 | 10/10/2026 | 4160 | HEPB | 200 | 200 | 0 | GR-4160-9702 | Sí | Conforme. Cantidad y guía coinciden. |
| 7 | 04/10/2026 | 4160 | IPV | 30 | 30 | 0 | GR-4160-2073 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 8 | 12/10/2026 | 4160 | PENT | 180 | 180 | 0 | GR-4160-2362 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 9 | 10/10/2026 | 4160 | INFL | 120 | 120 | 0 | GR-4160-8511 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 10 | 12/10/2026 | 4160 | PENT | 30 | 30 | 0 | GR-4160-2770 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 11 | 26/09/2026 | 4160 | VARI | 80 | 80 | 0 | GR-4160-4872 | Sí | Conforme. Cantidad y guía coinciden. |
| 12 | 04/10/2026 | 4160 | NEUM | 20 | 10 | -10 | GR-4160-8865 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 13 | 16/10/2026 | 4160 | NEUM | 30 | 20 | -10 | GR-4160-8470 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 14 | 21/09/2026 | 4160 | HEPB | 200 | 200 | 0 | GR-4160-1638 | Sí | Conforme. Cantidad y guía coinciden. |
| 15 | 03/10/2026 | 4160 | DTA | 50 | 50 | 0 | GR-4160-5542 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 16 | 09/10/2026 | 4160 | DTA | 40 | 40 | 0 | GR-4160-7068 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 17 | 12/10/2026 | 4160 | NEUM | 120 | 120 | 0 | GR-4160-5263 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 18 | 07/10/2026 | 4160 | VARI | 50 | 50 | 0 | GR-4160-8633 | Sí | Conforme. Cantidad y guía coinciden. |
| 19 | 05/10/2026 | 4160 | DTA | 120 | 120 | 0 | GR-4160-1362 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 20 | 18/10/2026 | 4160 | SPR | 30 | 30 | 0 | GR-4160-7352 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 21 | 21/09/2026 | 4160 | HEPB | 50 | 50 | 0 | GR-4160-1877 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 22 | 04/10/2026 | 4160 | PENT | 100 | 100 | 0 | GR-4160-1575 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 23 | 18/10/2026 | 4160 | NEUM | 120 | 120 | 0 | GR-4160-3586 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 24 | 05/10/2026 | 4160 | HEPB | 180 | 180 | 0 | GR-4160-1533 | Sí | Conforme. Cantidad y guía coinciden. |
| 25 | 28/09/2026 | 4160 | INFL | 100 | 100 | 0 | GR-4160-9524 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |

Cierre: 23 entregas concordantes ÷ 25 × 100 = **92.00 %**.

---

### Bloque 25 · TRAB-13 · Pretest (proceso manual) · 08/09/2026

Centro de acopio: **Turpo** (4163) · Auditor: **OBS-01** · Periodo auditado: **08/08/2026 al 07/09/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 12 · RSD 60.00 %.

Documentos auditados: 40 · Conformes: 27 · RSD: 67.50 % · Entregas conciliadas: 25 · Concordantes: 18 · CPE: 72.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 08/08/2026 | SAL | SAL-4163-0799 | ROTA | ROTA-2603-156K | 20 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 2 | 09/08/2026 | ING | ING-4163-0369 | INFL | INFL-2504-261K | 30 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 3 | 10/08/2026 | AJU | AJU-4163-0146 | HEPB | HEPB-2609-917M | 80 | S | N | S | S | S | N | S | S | N | M2+M6 | Asiento sin firma del responsable del almacén. |
| 4 | 10/08/2026 | DEV | DEV-4163-0354 | HEPB | HEPB-2609-521M | 300 | S | S | N | S | S | N | S | S | N | M3+M6 | Asiento sin firma del responsable del almacén. |
| 5 | 11/08/2026 | SAL | SAL-4163-1248 | INFL | INFL-2504-261K | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 12/08/2026 | ING | ING-4163-0541 | BCG | BCG-2606-296K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 13/08/2026 | ING | ING-4163-0676 | HEPB | HEPB-2602-318M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 13/08/2026 | SAL | SAL-4163-1477 | ROTA | ROTA-2502-563B | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 14/08/2026 | TRA | TRA-4163-0391 | HEPB | HEPB-2603-786K | 200 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 10 | 15/08/2026 | SAL | SAL-4163-1483 | ROTA | ROTA-2602-464A | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 16/08/2026 | SAL | SAL-4163-1512 | SPR | SPR-2504-185M | 20 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 12 | 16/08/2026 | SAL | SAL-4163-1536 | IPV | IPV-2605-698M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 17/08/2026 | ING | ING-4163-0898 | INFL | INFL-2604-777M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 18/08/2026 | TRA | TRA-4163-0561 | HEPB | HEPB-2603-786K | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 19/08/2026 | SAL | SAL-4163-1828 | DTA | DTA-2505-409K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 20/08/2026 | SAL | SAL-4163-2230 | IPV | IPV-2605-698M | 240 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 17 | 20/08/2026 | TRA | TRA-4163-0799 | NEUM | NEUM-2506-884B | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 21/08/2026 | TRA | TRA-4163-0919 | PENT | PENT-2605-322M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 22/08/2026 | DEV | DEV-4163-0423 | ROTA | ROTA-2602-464A | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 23/08/2026 | DEV | DEV-4163-1319 | IPV | IPV-2507-805M | 50 | S | S | S | S | N | S | S | S | N | M5 | Origen o destino consignado de forma incompleta. |
| 21 | 23/08/2026 | TRA | TRA-4163-1442 | IPV | IPV-2608-446B | 50 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 22 | 24/08/2026 | DEV | DEV-4163-1710 | NEUM | NEUM-2509-952A | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 25/08/2026 | ING | ING-4163-1109 | SPR | SPR-2504-185M | 60 | S | S | S | S | S | N | S | N | N | M6+M8 | Asiento sin firma del responsable del almacén. |
| 24 | 26/08/2026 | ING | ING-4163-1154 | SPR | SPR-2603-471K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 26/08/2026 | ING | ING-4163-1272 | HEPB | HEPB-2609-521M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 27/08/2026 | TRA | TRA-4163-1912 | PENT | PENT-2504-482M | 20 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 27 | 28/08/2026 | ING | ING-4163-1852 | BCG | BCG-2606-808K | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 29/08/2026 | ING | ING-4163-2267 | PENT | PENT-2606-251M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 30/08/2026 | DEV | DEV-4163-1781 | SPR | SPR-2609-423M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 30/08/2026 | ING | ING-4163-2365 | VARI | VARI-2501-250M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 31/08/2026 | ING | ING-4163-2553 | VARI | VARI-2501-250M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 01/09/2026 | ING | ING-4163-2992 | BCG | BCG-2507-694K | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 02/09/2026 | TRA | TRA-4163-1957 | HEPB | HEPB-2609-521M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 02/09/2026 | TRA | TRA-4163-2131 | VARI | VARI-2503-521A | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 03/09/2026 | ING | ING-4163-3485 | SPR | SPR-2603-471K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 04/09/2026 | DEV | DEV-4163-1822 | INFL | INFL-2607-737M | 50 | S | S | N | S | S | S | S | S | N | M3 | Fecha de vencimiento vencida o ilegible en el asiento. |
| 37 | 05/09/2026 | SAL | SAL-4163-3153 | INFL | INFL-2504-261K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 05/09/2026 | SAL | SAL-4163-3295 | NEUM | NEUM-2505-638K | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 06/09/2026 | SAL | SAL-4163-3352 | HEPB | HEPB-2609-521M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 07/09/2026 | DEV | DEV-4163-2150 | DTA | DTA-2602-797A | 40 | S | S | S | N | S | S | S | S | N | M4 | Cantidad física menor a la registrada en el asiento. |

**Entregas conciliadas — TRAB-13 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 12/08/2026 | 4163 | BCG | 50 | 50 | 0 | GR-4163-9132 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 2 | 31/08/2026 | 4163 | ROTA | 100 | 100 | 0 | GR-4163-6974 | Sí | Conforme. Cantidad y guía coinciden. |
| 3 | 03/09/2026 | 4163 | HEPB | 20 | 20 | 0 | GR-4163-5401 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 4 | 18/08/2026 | 4163 | NEUM | 20 | 10 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 5 | 27/08/2026 | 4163 | BCG | 20 | 20 | 0 | GR-4163-8127 | Sí | Conforme. Cantidad y guía coinciden. |
| 6 | 28/08/2026 | 4163 | PENT | 60 | 60 | 0 | GR-4163-6052 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 7 | 07/09/2026 | 4163 | BCG | 30 | 30 | 0 | GR-4163-4840 | Sí | Conforme. Cantidad y guía coinciden. |
| 8 | 14/08/2026 | 4163 | NEUM | 20 | 20 | 0 | GR-4163-1259 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 9 | 05/09/2026 | 4163 | PENT | 120 | 120 | 0 | GR-4163-7651 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 10 | 06/09/2026 | 4163 | VARI | 120 | 120 | 0 | GR-4163-8157 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 11 | 14/08/2026 | 4163 | IPV | 120 | 120 | 0 | GR-4163-1996 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 12 | 30/08/2026 | 4163 | PENT | 150 | 145 | -5 | GR-4163-4796 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 13 | 05/09/2026 | 4163 | NEUM | 120 | 110 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 14 | 01/09/2026 | 4163 | IPV | 60 | 60 | 0 | GR-4163-5087 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 15 | 18/08/2026 | 4163 | ROTA | 180 | 180 | 0 | GR-4163-4469 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 16 | 19/08/2026 | 4163 | SPR | 30 | 30 | 0 | GR-4163-8352 | Sí | Conforme. Cantidad y guía coinciden. |
| 17 | 18/08/2026 | 4163 | ROTA | 30 | 30 | 0 | GR-4163-2691 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 18 | 12/08/2026 | 4163 | BCG | 30 | 20 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 19 | 22/08/2026 | 4163 | IPV | 100 | 100 | 0 | GR-4163-7524 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 20 | 20/08/2026 | 4163 | INFL | 50 | 50 | 0 | GR-4163-6847 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 21 | 02/09/2026 | 4163 | HEPB | 50 | 50 | 0 | GR-4163-8615 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 22 | 03/09/2026 | 4163 | INFL | 180 | 160 | -20 | GR-4163-7804 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 23 | 31/08/2026 | 4163 | NEUM | 30 | 25 | -5 | GR-4163-3048 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 24 | 06/09/2026 | 4163 | VARI | 120 | 115 | -5 | GR-4163-3182 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 25 | 20/08/2026 | 4163 | SPR | 30 | 30 | 0 | GR-4163-6393 | Sí | Conforme. Verificado el FEFO al momento de la carga. |

Cierre: 18 entregas concordantes ÷ 25 × 100 = **72.00 %**.

---

### Bloque 26 · TRAB-13 · Postest (Sistema SIVAC) · 20/10/2026

Centro de acopio: **Turpo** (4163) · Auditor: **OBS-01** · Periodo auditado: **16/09/2026 al 19/10/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 19 · RSD 95.00 %.

Documentos auditados: 40 · Conformes: 37 · RSD: 92.50 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 16/09/2026 | SAL | SAL-4163-0314 | PENT | PENT-2606-251M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 17/09/2026 | SAL | SAL-4163-0374 | INFL | INFL-2604-777M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 18/09/2026 | ING | ING-4163-0141 | VARI | VARI-2607-979A | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 19/09/2026 | AJU | AJU-4163-0285 | VARI | VARI-2503-521A | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 19/09/2026 | SAL | SAL-4163-0747 | VARI | VARI-2509-637K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 20/09/2026 | DEV | DEV-4163-0220 | DTA | DTA-2603-463K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 21/09/2026 | TRA | TRA-4163-0373 | NEUM | NEUM-2507-181K | 60 | S | S | S | S | S | S | N | N | N | M7+M8 | Saldo no recalculado tras un ajuste autorizado. |
| 8 | 22/09/2026 | ING | ING-4163-0392 | INFL | INFL-2508-359M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 23/09/2026 | SAL | SAL-4163-1227 | NEUM | NEUM-2509-952A | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 24/09/2026 | SAL | SAL-4163-1819 | HEPB | HEPB-2609-521M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 24/09/2026 | ING | ING-4163-0475 | INFL | INFL-2607-737M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 25/09/2026 | ING | ING-4163-0836 | IPV | IPV-2504-587B | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 26/09/2026 | SAL | SAL-4163-1953 | DTA | DTA-2602-797A | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 27/09/2026 | DEV | DEV-4163-0293 | IPV | IPV-2608-446B | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 28/09/2026 | TRA | TRA-4163-0414 | VARI | VARI-2509-637K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 29/09/2026 | SAL | SAL-4163-1992 | VARI | VARI-2501-250M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 30/09/2026 | ING | ING-4163-1359 | PENT | PENT-2606-391A | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 30/09/2026 | ING | ING-4163-1415 | ROTA | ROTA-2602-464A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 01/10/2026 | TRA | TRA-4163-0786 | VARI | VARI-2508-818M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 02/10/2026 | SAL | SAL-4163-2196 | PENT | PENT-2508-232M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 03/10/2026 | ING | ING-4163-1505 | IPV | IPV-2608-446B | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 04/10/2026 | AJU | AJU-4163-0301 | SPR | SPR-2609-423M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 05/10/2026 | TRA | TRA-4163-0984 | ROTA | ROTA-2502-563B | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 05/10/2026 | TRA | TRA-4163-1516 | VARI | VARI-2503-521A | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 06/10/2026 | SAL | SAL-4163-2522 | BCG | BCG-2606-296K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 07/10/2026 | SAL | SAL-4163-2701 | VARI | VARI-2508-818M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 08/10/2026 | ING | ING-4163-1600 | DTA | DTA-2602-797A | 20 | S | S | S | S | N | S | S | S | N | M5 | Origen/destino incompleto en un traslado entre microredes. |
| 28 | 09/10/2026 | SAL | SAL-4163-3524 | VARI | VARI-2503-521A | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 10/10/2026 | ING | ING-4163-1756 | IPV | IPV-2504-587B | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 11/10/2026 | SAL | SAL-4163-3571 | ROTA | ROTA-2507-417A | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 11/10/2026 | SAL | SAL-4163-4011 | NEUM | NEUM-2509-952A | 100 | S | S | S | S | S | N | S | S | N | M6 | Firma pendiente de regularización del responsable. |
| 32 | 12/10/2026 | DEV | DEV-4163-0478 | INFL | INFL-2607-737M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 13/10/2026 | SAL | SAL-4163-4210 | NEUM | NEUM-2509-952A | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 14/10/2026 | TRA | TRA-4163-1611 | PENT | PENT-2605-322M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 15/10/2026 | SAL | SAL-4163-4229 | ROTA | ROTA-2605-833M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 16/10/2026 | ING | ING-4163-2366 | NEUM | NEUM-2505-638K | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 16/10/2026 | SAL | SAL-4163-4279 | HEPB | HEPB-2509-474M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 17/10/2026 | ING | ING-4163-2427 | INFL | INFL-2603-792B | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 18/10/2026 | AJU | AJU-4163-0333 | HEPB | HEPB-2603-786K | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 19/10/2026 | TRA | TRA-4163-1621 | ROTA | ROTA-2502-563B | 60 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-13 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 19/10/2026 | 4163 | INFL | 150 | 150 | 0 | GR-4163-3354 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 2 | 11/10/2026 | 4163 | PENT | 20 | 20 | 0 | GR-4163-5739 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 3 | 19/10/2026 | 4163 | NEUM | 40 | 40 | 0 | GR-4163-6709 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 4 | 12/10/2026 | 4163 | INFL | 50 | 50 | 0 | GR-4163-9658 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 5 | 23/09/2026 | 4163 | IPV | 120 | 120 | 0 | GR-4163-2626 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 6 | 19/10/2026 | 4163 | VARI | 150 | 150 | 0 | GR-4163-1571 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 7 | 08/10/2026 | 4163 | INFL | 150 | 150 | 0 | GR-4163-3678 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 8 | 18/10/2026 | 4163 | SPR | 50 | 50 | 0 | GR-4163-2222 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 9 | 05/10/2026 | 4163 | NEUM | 20 | 20 | 0 | GR-4163-5226 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 10 | 09/10/2026 | 4163 | VARI | 40 | 40 | 0 | GR-4163-5460 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 11 | 23/09/2026 | 4163 | SPR | 180 | 180 | 0 | GR-4163-5181 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 12 | 14/10/2026 | 4163 | DTA | 80 | 80 | 0 | GR-4163-6672 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 08/10/2026 | 4163 | DTA | 80 | 80 | 0 | GR-4163-1318 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 14 | 27/09/2026 | 4163 | BCG | 60 | 60 | 0 | GR-4163-7936 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 15 | 30/09/2026 | 4163 | DTA | 200 | 200 | 0 | GR-4163-1619 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 16 | 07/10/2026 | 4163 | BCG | 100 | 100 | 0 | GR-4163-5934 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 17 | 17/10/2026 | 4163 | NEUM | 150 | 150 | 0 | GR-4163-5876 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 18 | 22/09/2026 | 4163 | DTA | 50 | 40 | -10 | GR-4163-2795 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 19 | 13/10/2026 | 4163 | SPR | 200 | 200 | 0 | GR-4163-8804 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 20 | 02/10/2026 | 4163 | IPV | 200 | 200 | 0 | GR-4163-8175 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 21 | 11/10/2026 | 4163 | VARI | 60 | 60 | 0 | GR-4163-8672 | Sí | Conforme. Cantidad y guía coinciden. |
| 22 | 22/09/2026 | 4163 | BCG | 120 | 120 | 0 | GR-4163-3258 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 23 | 12/10/2026 | 4163 | NEUM | 200 | 200 | 0 | GR-4163-6158 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 24 | 30/09/2026 | 4163 | HEPB | 100 | 100 | 0 | GR-4163-7287 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 25 | 29/09/2026 | 4163 | PENT | 120 | 120 | 0 | GR-4163-8313 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 27 · TRAB-14 · Pretest (proceso manual) · 08/09/2026

Centro de acopio: **Kishuara** (4183) · Auditor: **OBS-02** · Periodo auditado: **11/08/2026 al 07/09/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 12 · RSD 60.00 %.

Documentos auditados: 40 · Conformes: 26 · RSD: 65.00 % · Entregas conciliadas: 25 · Concordantes: 17 · CPE: 68.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 14/08/2026 | TRA | TRA-4183-0126 | SPR | SPR-2608-539M | 60 | S | S | S | S | N | S | N | S | N | M5+M7 | Origen o destino consignado de forma incompleta. |
| 2 | 15/08/2026 | SAL | SAL-4183-0405 | NEUM | NEUM-2505-638K | 60 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 3 | 15/08/2026 | SAL | SAL-4183-0938 | ROTA | ROTA-2507-417A | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 16/08/2026 | SAL | SAL-4183-0989 | IPV | IPV-2605-698M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 16/08/2026 | SAL | SAL-4183-1021 | BCG | BCG-2504-789B | 180 | S | N | S | S | S | S | S | S | N | M2 | Lote del kardex no coincide con el rotulado del frasco. |
| 6 | 17/08/2026 | ING | ING-4183-0343 | IPV | IPV-2608-446B | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 18/08/2026 | ING | ING-4183-0488 | IPV | IPV-2605-698M | 300 | S | S | N | S | S | N | S | S | N | M3+M6 | Asiento sin firma del responsable del almacén. |
| 8 | 18/08/2026 | SAL | SAL-4183-1181 | HEPB | HEPB-2609-917M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 19/08/2026 | TRA | TRA-4183-0153 | IPV | IPV-2507-805M | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 20/08/2026 | SAL | SAL-4183-1190 | NEUM | NEUM-2506-884B | 240 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 11 | 20/08/2026 | SAL | SAL-4183-1536 | NEUM | NEUM-2505-688A | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 21/08/2026 | SAL | SAL-4183-1626 | IPV | IPV-2507-805M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 21/08/2026 | AJU | AJU-4183-0238 | INFL | INFL-2603-792B | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 22/08/2026 | AJU | AJU-4183-0572 | NEUM | NEUM-2505-638K | 60 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 15 | 23/08/2026 | ING | ING-4183-0514 | PENT | PENT-2508-232M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 23/08/2026 | SAL | SAL-4183-1798 | PENT | PENT-2606-251M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 24/08/2026 | SAL | SAL-4183-2220 | HEPB | HEPB-2509-474M | 60 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 18 | 24/08/2026 | SAL | SAL-4183-2749 | NEUM | NEUM-2505-638K | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 25/08/2026 | DEV | DEV-4183-0141 | ROTA | ROTA-2603-156K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 20 | 26/08/2026 | SAL | SAL-4183-2897 | ROTA | ROTA-2507-417A | 80 | S | S | S | N | S | S | S | S | N | M4 | Cantidad física menor a la registrada en el asiento. |
| 21 | 26/08/2026 | SAL | SAL-4183-2904 | SPR | SPR-2606-500M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 27/08/2026 | SAL | SAL-4183-4015 | VARI | VARI-2501-250M | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 28/08/2026 | TRA | TRA-4183-0737 | NEUM | NEUM-2507-181K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 28/08/2026 | DEV | DEV-4183-0768 | DTA | DTA-2606-829K | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 29/08/2026 | TRA | TRA-4183-1339 | DTA | DTA-2505-409K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 29/08/2026 | TRA | TRA-4183-1558 | INFL | INFL-2604-777M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 30/08/2026 | SAL | SAL-4183-4240 | HEPB | HEPB-2609-521M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 31/08/2026 | DEV | DEV-4183-0827 | PENT | PENT-2605-322M | 240 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 29 | 31/08/2026 | ING | ING-4183-0569 | NEUM | NEUM-2505-638K | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 01/09/2026 | SAL | SAL-4183-4253 | NEUM | NEUM-2505-638K | 120 | S | S | S | N | S | S | S | S | N | M4 | Cantidad física menor a la registrada en el asiento. |
| 31 | 01/09/2026 | TRA | TRA-4183-1755 | BCG | BCG-2606-296K | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 02/09/2026 | SAL | SAL-4183-4397 | NEUM | NEUM-2507-181K | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 03/09/2026 | TRA | TRA-4183-1960 | IPV | IPV-2504-587B | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 03/09/2026 | SAL | SAL-4183-4501 | INFL | INFL-2604-777M | 20 | N | S | S | S | S | S | N | S | N | M1+M7 | Biológico consignado no corresponde al frasco físico. |
| 35 | 04/09/2026 | TRA | TRA-4183-1964 | PENT | PENT-2605-322M | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 05/09/2026 | ING | ING-4183-0788 | VARI | VARI-2607-979A | 240 | S | S | S | S | S | S | S | N | N | M8 | Numeración correlativa interrumpida; falta un folio. |
| 37 | 05/09/2026 | SAL | SAL-4183-4981 | HEPB | HEPB-2509-474M | 50 | S | S | S | S | S | S | N | S | N | M7 | Saldo arrastrado no cuadra con la columna de existencias. |
| 38 | 06/09/2026 | TRA | TRA-4183-2031 | INFL | INFL-2607-737M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 06/09/2026 | SAL | SAL-4183-5211 | ROTA | ROTA-2603-156K | 60 | S | S | S | S | S | N | S | S | N | M6 | Asiento sin firma del responsable del almacén. |
| 40 | 07/09/2026 | SAL | SAL-4183-5661 | PENT | PENT-2605-322M | 300 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-14 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 07/09/2026 | 4183 | HEPB | 200 | 190 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 2 | 21/08/2026 | 4183 | BCG | 80 | 80 | 0 | GR-4183-1691 | Sí | Conforme. Cantidad y guía coinciden. |
| 3 | 05/09/2026 | 4183 | HEPB | 120 | 120 | 0 | GR-4183-4491 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 4 | 07/09/2026 | 4183 | VARI | 150 | 155 | 5 | GR-4183-3005 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 5 | 29/08/2026 | 4183 | SPR | 120 | 120 | 0 | GR-4183-1592 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 6 | 25/08/2026 | 4183 | INFL | 100 | 100 | 0 | GR-4183-5251 | Sí | Conforme. Cantidad y guía coinciden. |
| 7 | 31/08/2026 | 4183 | ROTA | 180 | 180 | 0 | GR-4183-1372 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 8 | 27/08/2026 | 4183 | DTA | 80 | 80 | 0 | GR-4183-4331 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 9 | 03/09/2026 | 4183 | IPV | 150 | 150 | 0 | GR-4183-3907 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 10 | 21/08/2026 | 4183 | IPV | 40 | 40 | 0 | GR-4183-1718 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 11 | 16/08/2026 | 4183 | IPV | 150 | 160 | 10 | GR-4183-6681 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 12 | 21/08/2026 | 4183 | PENT | 120 | 120 | 0 | GR-4183-2184 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 13 | 30/08/2026 | 4183 | PENT | 200 | 200 | 0 | GR-4183-2923 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 14 | 27/08/2026 | 4183 | INFL | 80 | 75 | -5 | GR-4183-2121 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 15 | 11/08/2026 | 4183 | DTA | 200 | 200 | 0 | GR-4183-2813 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 16 | 19/08/2026 | 4183 | BCG | 40 | 50 | 10 | GR-4183-2919 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 17 | 23/08/2026 | 4183 | DTA | 50 | 50 | 0 | GR-4183-2556 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 18 | 22/08/2026 | 4183 | BCG | 80 | 85 | 5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 19 | 25/08/2026 | 4183 | BCG | 40 | 35 | -5 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 20 | 25/08/2026 | 4183 | SPR | 50 | 45 | -5 | GR-4183-5097 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 21 | 18/08/2026 | 4183 | DTA | 80 | 80 | 0 | GR-4183-2119 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 22 | 04/09/2026 | 4183 | PENT | 180 | 180 | 0 | GR-4183-8590 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 23 | 06/09/2026 | 4183 | PENT | 100 | 100 | 0 | GR-4183-8838 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 24 | 04/09/2026 | 4183 | PENT | 100 | 100 | 0 | GR-4183-9091 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 25 | 14/08/2026 | 4183 | HEPB | 200 | 200 | 0 | GR-4183-7406 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |

Cierre: 17 entregas concordantes ÷ 25 × 100 = **68.00 %**.

---

### Bloque 28 · TRAB-14 · Postest (Sistema SIVAC) · 20/10/2026

Centro de acopio: **Kishuara** (4183) · Auditor: **OBS-02** · Periodo auditado: **22/09/2026 al 19/10/2026**

Hoja 1 (asientos 1 a 20): revisados 20 · conformes 19 · RSD 95.00 %.

Documentos auditados: 40 · Conformes: 39 · RSD: 97.50 % · Entregas conciliadas: 25 · Concordantes: 22 · CPE: 88.00 %

| Doc | Fecha | Tipo | Documento | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo | Observación |
| :---: | :---: | :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | 23/09/2026 | TRA | TRA-4183-0514 | VARI | VARI-2607-979A | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 2 | 24/09/2026 | ING | ING-4183-0268 | SPR | SPR-2504-185M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 3 | 24/09/2026 | SAL | SAL-4183-0501 | ROTA | ROTA-2605-833M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 4 | 25/09/2026 | ING | ING-4183-0653 | INFL | INFL-2508-359M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 5 | 26/09/2026 | SAL | SAL-4183-0524 | ROTA | ROTA-2605-833M | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 6 | 26/09/2026 | AJU | AJU-4183-0183 | INFL | INFL-2607-737M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 7 | 27/09/2026 | ING | ING-4183-0667 | PENT | PENT-2508-232M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 8 | 28/09/2026 | TRA | TRA-4183-0525 | INFL | INFL-2607-737M | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 9 | 28/09/2026 | SAL | SAL-4183-0930 | VARI | VARI-2503-521A | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 10 | 29/09/2026 | TRA | TRA-4183-0595 | BCG | BCG-2504-789B | 120 | S | S | S | S | S | S | S | S | S | — | — |
| 11 | 30/09/2026 | ING | ING-4183-0872 | INFL | INFL-2604-777M | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 12 | 30/09/2026 | TRA | TRA-4183-0725 | IPV | IPV-2605-698M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 13 | 01/10/2026 | ING | ING-4183-0894 | ROTA | ROTA-2605-833M | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 14 | 02/10/2026 | SAL | SAL-4183-1083 | BCG | BCG-2606-808K | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 15 | 02/10/2026 | ING | ING-4183-1171 | INFL | INFL-2603-792B | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 16 | 03/10/2026 | ING | ING-4183-1524 | DTA | DTA-2606-829K | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 17 | 04/10/2026 | ING | ING-4183-2031 | IPV | IPV-2605-698M | 200 | S | S | S | S | S | S | S | S | S | — | — |
| 18 | 04/10/2026 | SAL | SAL-4183-1114 | PENT | PENT-2606-391A | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 19 | 05/10/2026 | SAL | SAL-4183-1285 | DTA | DTA-2606-829K | 300 | S | S | N | S | N | S | S | S | N | M3+M5 | Origen/destino incompleto en un traslado entre microredes. |
| 20 | 06/10/2026 | ING | ING-4183-2072 | ROTA | ROTA-2605-833M | 240 | S | S | S | S | S | S | S | S | S | — | — |
| 21 | 06/10/2026 | ING | ING-4183-2350 | HEPB | HEPB-2609-917M | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 22 | 07/10/2026 | TRA | TRA-4183-0848 | DTA | DTA-2602-797A | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 23 | 08/10/2026 | SAL | SAL-4183-1294 | PENT | PENT-2606-391A | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 24 | 08/10/2026 | ING | ING-4183-2428 | INFL | INFL-2504-261K | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 25 | 09/10/2026 | SAL | SAL-4183-1384 | IPV | IPV-2504-587B | 50 | S | S | S | S | S | S | S | S | S | — | — |
| 26 | 10/10/2026 | SAL | SAL-4183-1673 | IPV | IPV-2605-698M | 100 | S | S | S | S | S | S | S | S | S | — | — |
| 27 | 10/10/2026 | SAL | SAL-4183-1936 | IPV | IPV-2608-446B | 80 | S | S | S | S | S | S | S | S | S | — | — |
| 28 | 11/10/2026 | ING | ING-4183-2514 | VARI | VARI-2501-250M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 29 | 12/10/2026 | SAL | SAL-4183-2725 | SPR | SPR-2504-185M | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 30 | 12/10/2026 | DEV | DEV-4183-0351 | NEUM | NEUM-2505-688A | 60 | S | S | S | S | S | S | S | S | S | — | — |
| 31 | 13/10/2026 | DEV | DEV-4183-0948 | PENT | PENT-2606-391A | 180 | S | S | S | S | S | S | S | S | S | — | — |
| 32 | 14/10/2026 | TRA | TRA-4183-0929 | NEUM | NEUM-2506-884B | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 33 | 14/10/2026 | SAL | SAL-4183-2800 | HEPB | HEPB-2603-786K | 150 | S | S | S | S | S | S | S | S | S | — | — |
| 34 | 15/10/2026 | TRA | TRA-4183-1110 | IPV | IPV-2504-587B | 20 | S | S | S | S | S | S | S | S | S | — | — |
| 35 | 16/10/2026 | ING | ING-4183-2544 | VARI | VARI-2501-250M | 300 | S | S | S | S | S | S | S | S | S | — | — |
| 36 | 16/10/2026 | AJU | AJU-4183-0804 | NEUM | NEUM-2505-688A | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 37 | 17/10/2026 | ING | ING-4183-2628 | ROTA | ROTA-2602-464A | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 38 | 18/10/2026 | TRA | TRA-4183-1473 | ROTA | ROTA-2502-563B | 40 | S | S | S | S | S | S | S | S | S | — | — |
| 39 | 18/10/2026 | ING | ING-4183-2719 | NEUM | NEUM-2507-181K | 30 | S | S | S | S | S | S | S | S | S | — | — |
| 40 | 19/10/2026 | SAL | SAL-4183-3467 | HEPB | HEPB-2602-318M | 300 | S | S | S | S | S | S | S | S | S | — | — |

**Entregas conciliadas — TRAB-14 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. | Observación |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :--- |
| 1 | 14/10/2026 | 4183 | HEPB | 200 | 200 | 0 | GR-4183-9345 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 2 | 09/10/2026 | 4183 | VARI | 40 | 40 | 0 | GR-4183-4671 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 3 | 18/10/2026 | 4183 | DTA | 100 | 100 | 0 | GR-4183-6432 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 4 | 19/10/2026 | 4183 | ROTA | 100 | 100 | 0 | GR-4183-7069 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 5 | 03/10/2026 | 4183 | NEUM | 80 | 80 | 0 | GR-4183-3440 | Sí | Conforme. Cantidad y guía coinciden. |
| 6 | 30/09/2026 | 4183 | INFL | 60 | 60 | 0 | GR-4183-5238 | Sí | Conforme. Cantidad y guía coinciden. |
| 7 | 12/10/2026 | 4183 | VARI | 100 | 90 | -10 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 8 | 24/09/2026 | 4183 | NEUM | 50 | 50 | 0 | GR-4183-7057 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 9 | 22/09/2026 | 4183 | ROTA | 80 | 80 | 0 | GR-4183-4203 | Sí | Conforme. Cantidad y guía coinciden. |
| 10 | 14/10/2026 | 4183 | VARI | 20 | 20 | 0 | GR-4183-1455 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 11 | 18/10/2026 | 4183 | BCG | 20 | 20 | 0 | GR-4183-8572 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 12 | 17/10/2026 | 4183 | VARI | 50 | 50 | 0 | GR-4183-8253 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 13 | 06/10/2026 | 4183 | NEUM | 80 | 80 | 0 | GR-4183-4177 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 14 | 10/10/2026 | 4183 | ROTA | 100 | 100 | 0 | GR-4183-3469 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 15 | 13/10/2026 | 4183 | PENT | 80 | 80 | 0 | GR-4183-7930 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 16 | 12/10/2026 | 4183 | SPR | 120 | 120 | 0 | GR-4183-1912 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 17 | 05/10/2026 | 4183 | DTA | 180 | 175 | -5 | GR-4183-1698 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 18 | 05/10/2026 | 4183 | VARI | 200 | 200 | 0 | GR-4183-6930 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 19 | 16/10/2026 | 4183 | BCG | 150 | 150 | 0 | GR-4183-8080 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 20 | 09/10/2026 | 4183 | ROTA | 50 | 50 | 0 | GR-4183-8426 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 21 | 26/09/2026 | 4183 | VARI | 50 | 50 | 0 | GR-4183-9398 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 22 | 23/09/2026 | 4183 | BCG | 120 | 120 | 0 | GR-4183-5166 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 23 | 19/10/2026 | 4183 | HEPB | 100 | 110 | 10 | GR-4183-5502 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 24 | 01/10/2026 | 4183 | ROTA | 80 | 80 | 0 | GR-4183-5611 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 25 | 29/09/2026 | 4183 | SPR | 30 | 30 | 0 | GR-4183-2758 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |

Cierre: 22 entregas concordantes ÷ 25 × 100 = **88.00 %**.

---

---

<a id="parte-5"></a>
## Parte 5. Instrumento 3 — Cuestionario de satisfacción del usuario (TAM)

La Modalidad A se administra en las dos fases y consta de ocho reactivos Likert de 1 a 5: cuatro miden aceptación del proceso y cuatro, utilidad percibida. Los enunciados se imprimen una sola vez por sección y la matriz consigna después la respuesta de cada unidad en cada fase.

### Enunciados de la Modalidad A

**Aceptación del proceso**

- **AP-01.** El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias.
- **AP-02.** La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos.
- **AP-03.** El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo.
- **AP-04.** Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores.

**Utilidad percibida**

- **UP-01.** La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas.
- **UP-02.** El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones.
- **UP-03.** La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos.
- **UP-04.** En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA.

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

*Nota.* Respuestas registradas en el instrumento complementario durante la fase de postest (N = 14). Elaboración propia.

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
