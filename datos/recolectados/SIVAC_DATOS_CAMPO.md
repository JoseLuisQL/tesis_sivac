# CONJUNTO INTEGRAL DE DATOS DE CAMPO — SISTEMA SIVAC

## Registro Empírico y Análisis Estadístico Pretest - Postest en Centros de Acopio de Vacunas

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

El presente documento consolida el registro íntegro de mediciones empíricas recolectadas en campo durante la evaluación del Sistema de Información de Vacunas (SIVAC). El estudio comprende un diseño cuasiexperimental de comparación pretest (proceso manual tradicional en papel) y postest (proceso automatizado con SIVAC), administrado a catorce unidades censales de operadores en trece centros de acopio y establecimientos de salud de la red asistencial.

### Resumen de parámetros operacionales del estudio

| Dimensión / Indicador | Unidad de medida | Pretest (Proceso Manual) | Postest (Sistema SIVAC) | Alcance muestral |
| :--- | :--- | :---: | :---: | :--- |
| **D1. Oportunidad de procesamiento** | | | | |
| Tiempo de registro de movimientos (T_reg) | Minutos (Media ± DE) | 75.00 ± 12.56 | 6.00 ± 1.12 | 14 operadores × 3 réplicas (84 mediciones) |
| Tiempo de emisión de vales (T_vale) | Minutos (Media ± DE) | 29.00 ± 3.95 | 0.525 ± 0.192 | 14 operadores × 3 réplicas (84 mediciones) |
| **D2. Consistencia documental** | | | | |
| Registros sin discrepancias (RSD) | Porcentaje (%) | 63.57 ± 12.31 | 91.96 ± 4.72 | 14 operadores × 40 expedientes (1,120 docs) |
| Concordancia programada vs. entregada (CPE) | Porcentaje (%) | 67.71 ± 11.26 | 88.57 ± 5.63 | 14 operadores × 25 despachos (700 despachos) |
| **D3. Satisfacción del usuario** | | | | |
| Aceptación del proceso (AP) | Puntos (1–20) | 8.07 ± 2.34 | 17.07 ± 2.59 | 14 operadores (4 reactivos Likert) |
| Utilidad percibida (UP) | Puntos (1–20) | 9.00 ± 2.04 | 17.71 ± 2.13 | 14 operadores (4 reactivos Likert) |
| Puntaje global TAM | Puntos (8–40) | 17.07 ± 4.34 | 34.79 ± 4.39 | 14 operadores (8 reactivos Likert) |
| **Cobertura total del estudio** | — | **Línea base manual** | **Fase con SIVAC** | **14 operadores censales / 13 centros de acopio** |

*Nota.* Datos recolectados en campo en las fases de pretest y postest. Elaboración propia.

### Criterios y reglas de cálculo

1. **Tiempos operativos (T_reg y T_vale):** Se calculan como el promedio aritmético de tres réplicas independientes cronometradas por operador en cada fase de observación.
2. **Registros sin discrepancias (RSD):** Se obtiene como el cociente entre el número de documentos conformes (que cumplen simultáneamente los ocho criterios de auditoría) y el total auditado ( = 40$), expresado en porcentaje.
3. **Concordancia programada vs. entregada (CPE):** Corresponde al porcentaje de despachos conciliados sin diferencias entre la cantidad programada y la física entregada sobre un total de 25 despachos evaluados.
4. **Satisfacción del usuario (AP, UP y TAM):** La aceptación del proceso (AP) y la utilidad percibida (UP) representan la sumatoria de cuatro reactivos Likert de 1 a 5 puntos cada una; el puntaje global TAM es la suma directa de ambas subescalas (rango de 8 a 40 puntos).
5. **Criterio de contraste inferencial:** La selección de la prueba estadística decisoria se rige por la evaluación de normalidad de Shapiro-Wilk sobre las diferencias pareadas ( = 	ext{postest} - 	ext{pretest}$): prueba paramétrica t de Student pareada cuando  > .05$, y prueba no paramétrica de Wilcoxon de rangos con signo cuando  \le .05$.
6. **Método de cálculo en Wilcoxon:** Se aplica el método exacto por permutación ante la ausencia de empates o diferencias nulas, y el método asintótico con corrección por continuidad y empates cuando existen ligaduras en las diferencias.
7. **Control del error tipo I:** Se aplica el ajuste secuencial de Holm-Bonferroni sobre los contrastes de la familia para preservar la robustez inferencial global.
8. **Precisión de registro cronométrico:** Los tiempos de postest para la emisión de vales (T_vale) se registraron cronométricamente en segundos enteros y se expresan en minutos con precisión de tres cifras decimales.

---

<a id="parte-1"></a>
## Parte 1. Padrón de las catorce unidades censales

La población evaluada es censal: comprende la totalidad de catorce operadores distribuidos en trece centros de acopio y establecimientos de salud de la red asistencial. La sede ALMACÉN (CHANKA) cuenta con dos operadores asignados al mismo punto logístico, por lo que el número de centros y el de unidades evaluadas difieren levemente. El padrón individualiza a los trabajadores, establecimientos, observadores de campo y las fechas de administración para ambas fases.

| Sujeto | Centro de acopio | Código | Observador | Pretest | Postest |
| :--- | :--- | :---: | :---: | :---: | :---: |
| TRAB-01 | ALMACÉN (CHANKA) | CHANKA-001 | OBS-01 | 10/08/2026 | 12/10/2026 |
| TRAB-02 | ALMACÉN (CHANKA) | CHANKA-001 | OBS-02 | 10/08/2026 | 12/10/2026 |
| TRAB-03 | Hospital Andahuaylas | S/C | OBS-01 | 11/08/2026 | 13/10/2026 |
| TRAB-04 | Centro de Salud Andahuaylas | 6804 | OBS-02 | 11/08/2026 | 13/10/2026 |
| TRAB-05 | Andarapa | 4132 | OBS-01 | 12/08/2026 | 14/10/2026 |
| TRAB-06 | Huancaray | 4158 | OBS-02 | 12/08/2026 | 14/10/2026 |
| TRAB-07 | San Antonio de Cachi | 4160 | OBS-01 | 13/08/2026 | 15/10/2026 |
| TRAB-08 | Chaccrampa | 4162 | OBS-02 | 13/08/2026 | 15/10/2026 |
| TRAB-09 | Turpo | 4163 | OBS-01 | 14/08/2026 | 16/10/2026 |
| TRAB-10 | Pampachiri | 4167 | OBS-02 | 14/08/2026 | 16/10/2026 |
| TRAB-11 | San Jeronimo | 4167-SJ | OBS-01 | 07/09/2026 | 19/10/2026 |
| TRAB-12 | Huancabamba | 4172 | OBS-02 | 07/09/2026 | 19/10/2026 |
| TRAB-13 | Kishuara | 4183 | OBS-01 | 08/09/2026 | 20/10/2026 |
| TRAB-14 | Talavera | 4195 | OBS-02 | 08/09/2026 | 20/10/2026 |

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

El instrumento imprime las 168 réplicas del conjunto: seis por unidad y fase (tres de registro y tres de emisión del vale). Cada bloque cierra con la suma y la media de sus tres réplicas, de modo que el indicador pueda auditarse sin recurrir al archivo de datos. Las duraciones se expresan en minutos con cuatro decimales; en el postest de T_vale se añade entre paréntesis el equivalente en segundos enteros.

**Convenciones.** T1: ingreso de remesa con un biológico y lote único. T2: salida regular programada de dos a tres vacunas. T3: redistribución con cuatro a seis biológicos. T4: vale simple para puesto de salud 1-1 o 1-2. T5: vale regular para centro de salud 1-3 o 1-4. T6: vale de reposición urgente o contingencia. P1: atención en ventanilla. P2: llamada del establecimiento. P3: corte breve de energía. P4: verificación de existencias.

### Bloque 1 · TRAB-01 · Pretest (proceso manual) · 10/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 08:42:50 | 72.8333 | — | — | Sí |
| REG-02 | T2 | 08:42:50 | 09:59:15 | 74.4167 | 120 | P1 | Sí |
| REG-03 | T3 | 09:59:15 | 11:14:00 | 74.7500 | — | — | Sí |

Cierre: 222.0000 min ÷ 3 = **74.0000 min**. Suma de las tres réplicas: 222.0000 min (13320 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 11:14:00 | 11:44:55 | 29.9167 | 60 | P3 | Sí |
| VALE-02 | T5 | 11:44:55 | 12:16:37 | 30.7000 | 60 | P4 | Sí |
| VALE-03 | T6 | 12:16:37 | 12:47:30 | 30.8833 | — | — | Sí |

Cierre: 91.5000 min ÷ 3 = **30.5000 min**. Suma de las tres réplicas: 91.5000 min (5490 s).

---

### Bloque 2 · TRAB-01 · Postest (Sistema SIVAC) · 12/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 07:35:12 | 5.2000 | — | — | Sí |
| REG-02 | T2 | 07:35:12 | 07:40:40 | 5.4667 | — | — | Sí |
| REG-03 | T3 | 07:40:40 | 07:48:42 | 5.5333 | 150 | P1 | Sí |

Cierre: 16.2000 min ÷ 3 = **5.4000 min**. Suma de las tres réplicas: 16.2000 min (972 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 07:48:42 | 07:49:11 | 0.4833 (29 s) | — | — | Sí |
| VALE-02 | T5 | 07:49:11 | 07:49:41 | 0.5000 (30 s) | — | — | Sí |
| VALE-03 | T6 | 07:49:41 | 07:50:12 | 0.5167 (31 s) | — | — | Sí |

Cierre: 1.5000 min ÷ 3 = **0.5000 min**. Suma de las tres réplicas: 1.5000 min (90 s).

---

### Bloque 3 · TRAB-02 · Pretest (proceso manual) · 10/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 08:41:55 | 69.9167 | 120 | P4 | Sí |
| REG-02 | T2 | 08:41:55 | 09:51:20 | 68.6667 | 45 | P2 | Sí |
| REG-03 | T3 | 09:51:20 | 10:59:45 | 68.4167 | — | — | Sí |

Cierre: 207.0000 min ÷ 3 = **69.0000 min**. Suma de las tres réplicas: 207.0000 min (12420 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 10:59:45 | 11:28:42 | 28.9500 | — | — | Sí |
| VALE-02 | T5 | 11:28:42 | 11:58:32 | 28.3333 | 90 | P2 | Sí |
| VALE-03 | T6 | 11:58:32 | 12:28:15 | 28.2167 | 90 | P1 | Sí |

Cierre: 85.5000 min ÷ 3 = **28.5000 min**. Suma de las tres réplicas: 85.5000 min (5130 s).

---

### Bloque 4 · TRAB-02 · Postest (Sistema SIVAC) · 12/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 07:36:15 | 5.2500 | 60 | P4 | Sí |
| REG-02 | T2 | 07:36:15 | 07:42:18 | 5.0500 | 60 | P4 | Sí |
| REG-03 | T3 | 07:42:18 | 07:47:18 | 5.0000 | — | — | Sí |

Cierre: 15.3000 min ÷ 3 = **5.1000 min**. Suma de las tres réplicas: 15.3000 min (918 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 07:47:18 | 07:47:47 | 0.4833 (29 s) | — | — | Sí |
| VALE-02 | T5 | 07:47:47 | 07:48:14 | 0.4500 (27 s) | — | — | Sí |
| VALE-03 | T6 | 07:48:14 | 07:48:42 | 0.4667 (28 s) | — | — | Sí |

Cierre: 1.4000 min ÷ 3 = **0.4667 min**. Suma de las tres réplicas: 1.4000 min (84 s).

---

### Bloque 5 · TRAB-03 · Pretest (proceso manual) · 11/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 08:56:05 | 85.3333 | 45 | P1 | Sí |
| REG-02 | T2 | 08:56:05 | 10:22:50 | 85.7500 | 60 | P3 | Sí |
| REG-03 | T3 | 10:22:50 | 11:49:45 | 86.9167 | — | — | Sí |

Cierre: 258.0000 min ÷ 3 = **86.0000 min**. Suma de las tres réplicas: 258.0000 min (15480 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 11:49:45 | 12:15:25 | 25.6667 | — | — | Sí |
| VALE-02 | T5 | 12:15:25 | 12:43:17 | 25.8667 | 120 | P1 | Sí |
| VALE-03 | T6 | 12:43:17 | 13:10:45 | 26.4667 | 60 | P4 | Sí |

Cierre: 78.0000 min ÷ 3 = **26.0000 min**. Suma de las tres réplicas: 78.0000 min (4680 s).

---

### Bloque 6 · TRAB-03 · Postest (Sistema SIVAC) · 13/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 07:40:05 | 7.0833 | 180 | P1 | Sí |
| REG-02 | T2 | 07:40:05 | 07:47:15 | 7.1667 | — | — | Sí |
| REG-03 | T3 | 07:47:15 | 07:54:36 | 7.3500 | — | — | Sí |

Cierre: 21.6000 min ÷ 3 = **7.2000 min**. Suma de las tres réplicas: 21.6000 min (1296 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 07:54:36 | 07:54:59 | 0.3833 (23 s) | — | — | Sí |
| VALE-02 | T5 | 07:54:59 | 07:55:23 | 0.4000 (24 s) | — | — | Sí |
| VALE-03 | T6 | 07:55:23 | 07:55:45 | 0.3667 (22 s) | — | — | Sí |

Cierre: 1.1500 min ÷ 3 = **0.3833 min**. Suma de las tres réplicas: 1.1500 min (69 s).

---

### Bloque 7 · TRAB-04 · Pretest (proceso manual) · 11/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 08:49:30 | 79.5000 | — | — | Sí |
| REG-02 | T2 | 08:49:30 | 10:09:15 | 79.7500 | — | — | Sí |
| REG-03 | T3 | 10:09:15 | 11:27:00 | 77.7500 | — | — | Sí |

Cierre: 237.0000 min ÷ 3 = **79.0000 min**. Suma de las tres réplicas: 237.0000 min (14220 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 11:27:00 | 11:58:15 | 31.2500 | — | — | Sí |
| VALE-02 | T5 | 11:58:15 | 12:31:37 | 31.3667 | 120 | P2 | Sí |
| VALE-03 | T6 | 12:31:37 | 13:02:00 | 30.3833 | — | — | Sí |

Cierre: 93.0000 min ÷ 3 = **31.0000 min**. Suma de las tres réplicas: 93.0000 min (5580 s).

---

### Bloque 8 · TRAB-04 · Postest (Sistema SIVAC) · 13/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 07:36:41 | 6.6833 | — | — | Sí |
| REG-02 | T2 | 07:36:41 | 07:46:25 | 6.7333 | 180 | P3 | Sí |
| REG-03 | T3 | 07:46:25 | 07:55:18 | 6.3833 | 150 | P4 | Sí |

Cierre: 19.8000 min ÷ 3 = **6.6000 min**. Suma de las tres réplicas: 19.8000 min (1188 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 07:55:18 | 07:55:53 | 0.5833 (35 s) | — | — | Sí |
| VALE-02 | T5 | 07:55:53 | 07:56:25 | 0.5333 (32 s) | — | — | Sí |
| VALE-03 | T6 | 07:56:25 | 07:56:57 | 0.5333 (32 s) | — | — | Sí |

Cierre: 1.6500 min ÷ 3 = **0.5500 min**. Suma de las tres réplicas: 1.6500 min (99 s).

---

### Bloque 9 · TRAB-05 · Pretest (proceso manual) · 12/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 08:34:35 | 64.5833 | — | — | Sí |
| REG-02 | T2 | 08:34:35 | 09:40:35 | 66.0000 | — | — | Sí |
| REG-03 | T3 | 09:40:35 | 10:46:00 | 64.4167 | 60 | P3 | Sí |

Cierre: 195.0000 min ÷ 3 = **65.0000 min**. Suma de las tres réplicas: 195.0000 min (11700 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 10:46:00 | 11:22:48 | 33.8000 | 180 | P3 | Sí |
| VALE-02 | T5 | 11:22:48 | 11:58:48 | 34.5000 | 90 | P3 | Sí |
| VALE-03 | T6 | 11:58:48 | 12:32:30 | 33.7000 | — | — | Sí |

Cierre: 102.0000 min ÷ 3 = **34.0000 min**. Suma de las tres réplicas: 102.0000 min (6120 s).

---

### Bloque 10 · TRAB-05 · Postest (Sistema SIVAC) · 14/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 07:34:44 | 4.7333 | — | — | Sí |
| REG-02 | T2 | 07:34:44 | 07:39:42 | 4.9667 | — | — | Sí |
| REG-03 | T3 | 07:39:42 | 07:44:24 | 4.7000 | — | — | Sí |

Cierre: 14.4000 min ÷ 3 = **4.8000 min**. Suma de las tres réplicas: 14.4000 min (864 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 07:44:24 | 07:45:17 | 0.8833 (53 s) | — | — | Sí |
| VALE-02 | T5 | 07:45:17 | 07:46:12 | 0.9167 (55 s) | — | — | Sí |
| VALE-03 | T6 | 07:46:12 | 07:47:06 | 0.9000 (54 s) | — | — | Sí |

Cierre: 2.7000 min ÷ 3 = **0.9000 min**. Suma de las tres réplicas: 2.7000 min (162 s).

---

### Bloque 11 · TRAB-06 · Pretest (proceso manual) · 12/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 08:45:05 | 73.0833 | 120 | P2 | Sí |
| REG-02 | T2 | 08:45:05 | 09:56:35 | 71.5000 | — | — | Sí |
| REG-03 | T3 | 09:56:35 | 11:09:30 | 71.4167 | 90 | P2 | Sí |

Cierre: 216.0000 min ÷ 3 = **72.0000 min**. Suma de las tres réplicas: 216.0000 min (12960 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 11:09:30 | 11:37:03 | 27.5500 | — | — | Sí |
| VALE-02 | T5 | 11:37:03 | 12:03:48 | 26.7500 | — | — | Sí |
| VALE-03 | T6 | 12:03:48 | 12:32:30 | 26.7000 | 120 | P1 | Sí |

Cierre: 81.0000 min ÷ 3 = **27.0000 min**. Suma de las tres réplicas: 81.0000 min (4860 s).

---

### Bloque 12 · TRAB-06 · Postest (Sistema SIVAC) · 14/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 07:35:53 | 5.8833 | — | — | Sí |
| REG-02 | T2 | 07:35:53 | 07:41:30 | 5.6167 | — | — | Sí |
| REG-03 | T3 | 07:41:30 | 07:47:06 | 5.6000 | — | — | Sí |

Cierre: 17.1000 min ÷ 3 = **5.7000 min**. Suma de las tres réplicas: 17.1000 min (1026 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 07:47:06 | 07:47:33 | 0.4500 (27 s) | — | — | Sí |
| VALE-02 | T5 | 07:47:33 | 07:47:59 | 0.4333 (26 s) | — | — | Sí |
| VALE-03 | T6 | 07:47:59 | 07:48:24 | 0.4167 (25 s) | — | — | Sí |

Cierre: 1.3000 min ÷ 3 = **0.4333 min**. Suma de las tres réplicas: 1.3000 min (78 s).

---

### Bloque 13 · TRAB-07 · Pretest (proceso manual) · 13/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 09:04:20 | 94.3333 | — | — | Sí |
| REG-02 | T2 | 09:04:20 | 10:40:25 | 93.0833 | 180 | P1 | Sí |
| REG-03 | T3 | 10:40:25 | 12:15:00 | 94.5833 | — | — | Sí |

Cierre: 282.0000 min ÷ 3 = **94.0000 min**. Suma de las tres réplicas: 282.0000 min (16920 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 12:15:00 | 12:44:40 | 29.6667 | — | — | Sí |
| VALE-02 | T5 | 12:44:40 | 13:13:42 | 29.0333 | — | — | Sí |
| VALE-03 | T6 | 13:13:42 | 13:44:15 | 29.8000 | 45 | P3 | Sí |

Cierre: 88.5000 min ÷ 3 = **29.5000 min**. Suma de las tres réplicas: 88.5000 min (5310 s).

---

### Bloque 14 · TRAB-07 · Postest (Sistema SIVAC) · 15/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 07:37:51 | 7.8500 | — | — | Sí |
| REG-02 | T2 | 07:37:51 | 07:47:30 | 7.6500 | 120 | P2 | Sí |
| REG-03 | T3 | 07:47:30 | 07:55:24 | 7.9000 | — | — | Sí |

Cierre: 23.4000 min ÷ 3 = **7.8000 min**. Suma de las tres réplicas: 23.4000 min (1404 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 07:55:24 | 07:56:01 | 0.6167 (37 s) | — | — | Sí |
| VALE-02 | T5 | 07:56:01 | 07:56:41 | 0.6667 (40 s) | — | — | Sí |
| VALE-03 | T6 | 07:56:41 | 07:57:21 | 0.6667 (40 s) | — | — | Sí |

Cierre: 1.9500 min ÷ 3 = **0.6500 min**. Suma de las tres réplicas: 1.9500 min (117 s).

---

### Bloque 15 · TRAB-08 · Pretest (proceso manual) · 13/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 08:30:10 | 60.1667 | — | — | Sí |
| REG-02 | T2 | 08:30:10 | 09:33:25 | 61.2500 | 120 | P3 | Sí |
| REG-03 | T3 | 09:33:25 | 10:37:30 | 61.5833 | 150 | P4 | Sí |

Cierre: 183.0000 min ÷ 3 = **61.0000 min**. Suma de las tres réplicas: 183.0000 min (10980 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 10:37:30 | 11:12:35 | 35.0833 | — | — | Sí |
| VALE-02 | T5 | 11:12:35 | 11:48:13 | 35.6333 | — | — | Sí |
| VALE-03 | T6 | 11:48:13 | 12:26:00 | 35.7833 | 120 | P4 | Sí |

Cierre: 106.5000 min ÷ 3 = **35.5000 min**. Suma de las tres réplicas: 106.5000 min (6390 s).

---

### Bloque 16 · TRAB-08 · Postest (Sistema SIVAC) · 15/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 07:34:22 | 4.3667 | — | — | Sí |
| REG-02 | T2 | 07:34:22 | 07:38:55 | 4.5500 | — | — | Sí |
| REG-03 | T3 | 07:38:55 | 07:43:30 | 4.5833 | — | — | Sí |

Cierre: 13.5000 min ÷ 3 = **4.5000 min**. Suma de las tres réplicas: 13.5000 min (810 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 07:43:30 | 07:44:17 | 0.7833 (47 s) | — | — | Sí |
| VALE-02 | T5 | 07:44:17 | 07:45:03 | 0.7667 (46 s) | — | — | Sí |
| VALE-03 | T6 | 07:45:03 | 07:45:51 | 0.8000 (48 s) | — | — | Sí |

Cierre: 2.3500 min ÷ 3 = **0.7833 min**. Suma de las tres réplicas: 2.3500 min (141 s).

---

### Bloque 17 · TRAB-09 · Pretest (proceso manual) · 14/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 08:44:50 | 74.8333 | — | — | Sí |
| REG-02 | T2 | 08:44:50 | 10:01:15 | 76.4167 | — | — | Sí |
| REG-03 | T3 | 10:01:15 | 11:21:00 | 76.7500 | 180 | P1 | Sí |

Cierre: 228.0000 min ÷ 3 = **76.0000 min**. Suma de las tres réplicas: 228.0000 min (13680 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 11:21:00 | 11:47:25 | 24.4167 | 120 | P2 | Sí |
| VALE-02 | T5 | 11:47:25 | 12:12:37 | 25.2000 | — | — | Sí |
| VALE-03 | T6 | 12:12:37 | 12:38:45 | 25.3833 | 45 | P4 | Sí |

Cierre: 75.0000 min ÷ 3 = **25.0000 min**. Suma de las tres réplicas: 75.0000 min (4500 s).

---

### Bloque 18 · TRAB-09 · Postest (Sistema SIVAC) · 16/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 07:39:06 | 6.1000 | 180 | P4 | Sí |
| REG-02 | T2 | 07:39:06 | 07:45:28 | 6.3667 | — | — | Sí |
| REG-03 | T3 | 07:45:28 | 07:54:54 | 6.4333 | 180 | P3 | Sí |

Cierre: 18.9000 min ÷ 3 = **6.3000 min**. Suma de las tres réplicas: 18.9000 min (1134 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 07:54:54 | 07:55:13 | 0.3167 (19 s) | — | — | Sí |
| VALE-02 | T5 | 07:55:13 | 07:55:33 | 0.3333 (20 s) | — | — | Sí |
| VALE-03 | T6 | 07:55:33 | 07:55:54 | 0.3500 (21 s) | — | — | Sí |

Cierre: 1.0000 min ÷ 3 = **0.3333 min**. Suma de las tres réplicas: 1.0000 min (60 s).

---

### Bloque 19 · TRAB-10 · Pretest (proceso manual) · 14/08/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 08:28:40 | 57.9167 | 45 | P4 | Sí |
| REG-02 | T2 | 08:28:40 | 09:26:20 | 56.6667 | 60 | P3 | Sí |
| REG-03 | T3 | 09:26:20 | 10:22:45 | 56.4167 | — | — | Sí |

Cierre: 171.0000 min ÷ 3 = **57.0000 min**. Suma de las tres réplicas: 171.0000 min (10260 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 10:22:45 | 10:53:57 | 30.4500 | 45 | P2 | Sí |
| VALE-02 | T5 | 10:53:57 | 11:24:47 | 29.8333 | 60 | P1 | Sí |
| VALE-03 | T6 | 11:24:47 | 11:56:30 | 29.7167 | 120 | P3 | Sí |

Cierre: 90.0000 min ÷ 3 = **30.0000 min**. Suma de las tres réplicas: 90.0000 min (5400 s).

---

### Bloque 20 · TRAB-10 · Postest (Sistema SIVAC) · 16/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 07:34:21 | 4.3500 | — | — | Sí |
| REG-02 | T2 | 07:34:21 | 07:38:30 | 4.1500 | — | — | Sí |
| REG-03 | T3 | 07:38:30 | 07:42:36 | 4.1000 | — | — | Sí |

Cierre: 12.6000 min ÷ 3 = **4.2000 min**. Suma de las tres réplicas: 12.6000 min (756 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 07:42:36 | 07:43:08 | 0.5333 (32 s) | — | — | Sí |
| VALE-02 | T5 | 07:43:08 | 07:43:38 | 0.5000 (30 s) | — | — | Sí |
| VALE-03 | T6 | 07:43:38 | 07:44:09 | 0.5167 (31 s) | — | — | Sí |

Cierre: 1.5500 min ÷ 3 = **0.5167 min**. Suma de las tres réplicas: 1.5500 min (93 s).

---

### Bloque 21 · TRAB-11 · Pretest (proceso manual) · 07/09/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 08:54:20 | 82.3333 | 120 | P3 | Sí |
| REG-02 | T2 | 08:54:20 | 10:17:05 | 82.7500 | — | — | Sí |
| REG-03 | T3 | 10:17:05 | 11:43:00 | 83.9167 | 120 | P1 | Sí |

Cierre: 249.0000 min ÷ 3 = **83.0000 min**. Suma de las tres réplicas: 249.0000 min (14940 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 11:43:00 | 12:07:40 | 22.1667 | 150 | P1 | Sí |
| VALE-02 | T5 | 12:07:40 | 12:30:02 | 22.3667 | — | — | Sí |
| VALE-03 | T6 | 12:30:02 | 12:56:00 | 22.9667 | 180 | P1 | Sí |

Cierre: 67.5000 min ÷ 3 = **22.5000 min**. Suma de las tres réplicas: 67.5000 min (4050 s).

---

### Bloque 22 · TRAB-11 · Postest (Sistema SIVAC) · 19/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 07:39:47 | 6.7833 | 180 | P3 | Sí |
| REG-02 | T2 | 07:39:47 | 07:46:39 | 6.8667 | — | — | Sí |
| REG-03 | T3 | 07:46:39 | 07:53:42 | 7.0500 | — | — | Sí |

Cierre: 20.7000 min ÷ 3 = **6.9000 min**. Suma de las tres réplicas: 20.7000 min (1242 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 07:53:42 | 07:53:56 | 0.2333 (14 s) | — | — | Sí |
| VALE-02 | T5 | 07:53:56 | 07:54:11 | 0.2500 (15 s) | — | — | Sí |
| VALE-03 | T6 | 07:54:11 | 07:54:24 | 0.2167 (13 s) | — | — | Sí |

Cierre: 0.7000 min ÷ 3 = **0.2333 min**. Suma de las tres réplicas: 0.7000 min (42 s).

---

### Bloque 23 · TRAB-12 · Pretest (proceso manual) · 07/09/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 09:00:30 | 90.5000 | — | — | Sí |
| REG-02 | T2 | 09:00:30 | 10:31:15 | 90.7500 | — | — | Sí |
| REG-03 | T3 | 10:31:15 | 12:00:00 | 88.7500 | — | — | Sí |

Cierre: 270.0000 min ÷ 3 = **90.0000 min**. Suma de las tres réplicas: 270.0000 min (16200 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 12:00:00 | 12:29:00 | 28.2500 | 45 | P1 | Sí |
| VALE-02 | T5 | 12:29:00 | 12:57:22 | 28.3667 | — | — | Sí |
| VALE-03 | T6 | 12:57:22 | 13:24:45 | 27.3833 | — | — | Sí |

Cierre: 84.0000 min ÷ 3 = **28.0000 min**. Suma de las tres réplicas: 84.0000 min (5040 s).

---

### Bloque 24 · TRAB-12 · Postest (Sistema SIVAC) · 19/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 07:39:05 | 7.5833 | 90 | P2 | Sí |
| REG-02 | T2 | 07:39:05 | 07:46:43 | 7.6333 | — | — | Sí |
| REG-03 | T3 | 07:46:43 | 07:56:00 | 7.2833 | 120 | P4 | Sí |

Cierre: 22.5000 min ÷ 3 = **7.5000 min**. Suma de las tres réplicas: 22.5000 min (1350 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 07:56:00 | 07:56:38 | 0.6333 (38 s) | — | — | Sí |
| VALE-02 | T5 | 07:56:38 | 07:57:13 | 0.5833 (35 s) | — | — | Sí |
| VALE-03 | T6 | 07:57:13 | 07:57:48 | 0.5833 (35 s) | — | — | Sí |

Cierre: 1.8000 min ÷ 3 = **0.6000 min**. Suma de las tres réplicas: 1.8000 min (108 s).

---

### Bloque 25 · TRAB-13 · Pretest (proceso manual) · 08/09/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 08:24:35 | 54.5833 | — | — | Sí |
| REG-02 | T2 | 08:24:35 | 09:22:05 | 56.0000 | 90 | P4 | Sí |
| REG-03 | T3 | 09:22:05 | 10:16:30 | 54.4167 | — | — | Sí |

Cierre: 165.0000 min ÷ 3 = **55.0000 min**. Suma de las tres réplicas: 165.0000 min (9900 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 10:16:30 | 10:52:48 | 34.3000 | 120 | P4 | Sí |
| VALE-02 | T5 | 10:52:48 | 11:27:48 | 35.0000 | — | — | Sí |
| VALE-03 | T6 | 11:27:48 | 12:02:00 | 34.2000 | — | — | Sí |

Cierre: 103.5000 min ÷ 3 = **34.5000 min**. Suma de las tres réplicas: 103.5000 min (6210 s).

---

### Bloque 26 · TRAB-13 · Postest (Sistema SIVAC) · 20/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 07:35:53 | 5.8833 | — | — | Sí |
| REG-02 | T2 | 07:35:53 | 07:42:00 | 6.1167 | — | — | Sí |
| REG-03 | T3 | 07:42:00 | 07:47:51 | 5.8500 | — | — | Sí |

Cierre: 17.8500 min ÷ 3 = **5.9500 min**. Suma de las tres réplicas: 17.8500 min (1071 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 07:47:51 | 07:48:33 | 0.7000 (42 s) | — | — | Sí |
| VALE-02 | T5 | 07:48:33 | 07:49:17 | 0.7333 (44 s) | — | — | Sí |
| VALE-03 | T6 | 07:49:17 | 07:50:00 | 0.7167 (43 s) | — | — | Sí |

Cierre: 2.1500 min ÷ 3 = **0.7167 min**. Suma de las tres réplicas: 2.1500 min (129 s).

---

### Bloque 27 · TRAB-14 · Pretest (proceso manual) · 08/09/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 09:00:05 | 90.0833 | — | — | Sí |
| REG-02 | T2 | 09:00:05 | 10:28:35 | 88.5000 | — | — | Sí |
| REG-03 | T3 | 10:28:35 | 11:57:00 | 88.4167 | — | — | Sí |

Cierre: 267.0000 min ÷ 3 = **89.0000 min**. Suma de las tres réplicas: 267.0000 min (16020 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 11:57:00 | 12:21:33 | 24.5500 | — | — | Sí |
| VALE-02 | T5 | 12:21:33 | 12:46:48 | 23.7500 | 90 | P3 | Sí |
| VALE-03 | T6 | 12:46:48 | 13:12:30 | 23.7000 | 120 | P3 | Sí |

Cierre: 72.0000 min ÷ 3 = **24.0000 min**. Suma de las tres réplicas: 72.0000 min (4320 s).

---

### Bloque 28 · TRAB-14 · Postest (Sistema SIVAC) · 20/10/2026

**Indicador 1.1 — Tiempo de registro (T_reg)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| REG-01 | T1 | 07:30:00 | 07:37:14 | 6.2333 | 60 | P1 | Sí |
| REG-02 | T2 | 07:37:14 | 07:43:12 | 5.9667 | — | — | Sí |
| REG-03 | T3 | 07:43:12 | 07:49:09 | 5.9500 | — | — | Sí |

Cierre: 18.1500 min ÷ 3 = **6.0500 min**. Suma de las tres réplicas: 18.1500 min (1089 s).

**Indicador 1.2 — Tiempo de emisión de vales (T_vale)**

| Réplica | Tarea | Inicio | Fin | Duración (min) | Pausa (s) | Motivo | Válida |
| :--- | :---: | :---: | :---: | ---: | ---: | :---: | :---: |
| VALE-01 | T4 | 07:49:09 | 07:49:27 | 0.3000 (18 s) | — | — | Sí |
| VALE-02 | T5 | 07:49:27 | 07:49:44 | 0.2833 (17 s) | — | — | Sí |
| VALE-03 | T6 | 07:49:44 | 07:50:00 | 0.2667 (16 s) | — | — | Sí |

Cierre: 0.8500 min ÷ 3 = **0.2833 min**. Suma de las tres réplicas: 0.8500 min (51 s).

---

<a id="parte-4"></a>
## Parte 4. Instrumento 2 — Ficha de auditoría documental y conciliación de entregas

Cada bloque audita cuarenta documentos sobre ocho criterios binarios y concilia veinticinco despachos. La conformidad documental es conjuntiva: un documento es conforme solo si cumple los ocho criterios. La tabla emplea S y N para abreviar Sí y No, y las columnas 1 a 8 siguen el orden de los aspectos del instrumento. El motivo se codifica de M1 a M8 y se imprime solo cuando el documento no es conforme.

**Convenciones.** ING: ingreso. SAL: salida. TRA: transferencia. DEV: devolución. AJU: ajuste. BCG, PENT, IPV, ROTA, NEUM, SPR, DTA, HEPB, INFL y VARI abrevian los biológicos del catálogo. M1 a M8 remiten a los ocho aspectos en el orden impreso.

### Bloque 1 · TRAB-01 · Pretest (proceso manual) · 10/08/2026

Documentos auditados: 40 · Conformes: 26 · RSD: 65.00 % · Entregas conciliadas: 25 · Concordantes: 21 · CPE: 84.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | DEV | VARI | L-2608-01 | 40 | S | S | S | S | S | S | S | N | N | M8 |
| 2 | ING | BCG | L-2608-02 | 60 | S | N | S | S | S | S | S | S | N | M2 |
| 3 | AJU | INFL | L-2608-03 | 200 | S | S | N | S | S | S | S | S | N | M3 |
| 4 | TRA | DTA | L-2608-04 | 60 | S | S | S | S | S | S | N | S | N | M7 |
| 5 | AJU | PENT | L-2608-05 | 180 | S | S | S | S | S | S | S | S | S | — |
| 6 | SAL | ROTA | L-2608-06 | 120 | S | S | S | S | S | S | S | S | S | — |
| 7 | SAL | VARI | L-2608-07 | 150 | N | S | S | S | S | S | S | S | N | M1 |
| 8 | AJU | PENT | L-2608-08 | 20 | S | S | S | S | S | S | S | S | S | — |
| 9 | ING | HEPB | L-2608-09 | 240 | S | S | S | S | S | S | S | S | S | — |
| 10 | AJU | ROTA | L-2608-10 | 240 | S | S | S | S | S | S | S | S | S | — |
| 11 | AJU | ROTA | L-2608-11 | 300 | N | S | S | S | S | S | S | S | N | M1 |
| 12 | DEV | DTA | L-2608-12 | 40 | S | S | S | S | S | S | S | S | S | — |
| 13 | ING | HEPB | L-2608-13 | 300 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | ROTA | L-2608-14 | 40 | S | S | S | S | S | S | N | S | N | M7 |
| 15 | AJU | DTA | L-2608-15 | 100 | S | S | S | S | S | S | S | S | S | — |
| 16 | DEV | NEUM | L-2608-16 | 150 | S | S | S | S | S | S | S | S | S | — |
| 17 | TRA | DTA | L-2608-17 | 200 | S | S | S | S | S | S | S | S | S | — |
| 18 | DEV | INFL | L-2608-18 | 120 | S | S | S | S | N | S | S | S | N | M5 |
| 19 | TRA | BCG | L-2608-19 | 40 | S | S | S | S | S | S | S | S | S | — |
| 20 | TRA | SPR | L-2608-20 | 150 | S | S | S | S | S | S | N | S | N | M7 |
| 21 | SAL | NEUM | L-2608-21 | 120 | S | S | N | S | S | S | S | S | N | M3 |
| 22 | TRA | DTA | L-2608-22 | 40 | S | S | S | S | S | N | S | S | N | M6 |
| 23 | DEV | IPV | L-2608-23 | 80 | S | S | S | S | S | S | S | S | S | — |
| 24 | TRA | HEPB | L-2608-24 | 300 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | IPV | L-2608-25 | 300 | S | S | S | S | S | S | S | S | S | — |
| 26 | DEV | IPV | L-2608-26 | 60 | S | S | S | S | S | S | S | S | S | — |
| 27 | AJU | NEUM | L-2608-27 | 150 | S | S | N | S | S | S | S | S | N | M3 |
| 28 | AJU | PENT | L-2608-28 | 120 | S | S | S | S | S | S | S | S | S | — |
| 29 | SAL | PENT | L-2608-29 | 200 | S | S | S | S | S | S | S | S | S | — |
| 30 | SAL | BCG | L-2608-30 | 40 | S | S | S | S | S | S | S | S | S | — |
| 31 | ING | NEUM | L-2608-31 | 60 | S | S | S | S | S | S | S | S | S | — |
| 32 | TRA | PENT | L-2608-32 | 80 | S | S | S | S | S | S | S | S | S | — |
| 33 | AJU | IPV | L-2608-33 | 200 | S | S | S | S | S | S | S | S | S | — |
| 34 | DEV | IPV | L-2608-34 | 100 | S | S | S | S | S | S | S | S | S | — |
| 35 | AJU | INFL | L-2608-35 | 100 | S | N | S | S | S | S | S | S | N | M2 |
| 36 | SAL | HEPB | L-2608-36 | 240 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | SPR | L-2608-37 | 200 | S | S | S | S | S | S | N | S | N | M7 |
| 38 | ING | PENT | L-2608-38 | 120 | S | S | S | S | S | S | S | S | S | — |
| 39 | SAL | NEUM | L-2608-39 | 60 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | VARI | L-2608-40 | 150 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-01 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 10/08/2026 | CHANKA-001 | ROTA | 180 | 180 | 0 | No aplica | Sí |
| 2 | 10/08/2026 | CHANKA-001 | IPV | 60 | 50 | -10 | Sí | No |
| 3 | 10/08/2026 | CHANKA-001 | SPR | 30 | 30 | 0 | No aplica | Sí |
| 4 | 10/08/2026 | CHANKA-001 | DTA | 40 | 40 | 0 | No aplica | Sí |
| 5 | 10/08/2026 | CHANKA-001 | VARI | 200 | 200 | 0 | No aplica | Sí |
| 6 | 10/08/2026 | CHANKA-001 | INFL | 30 | 30 | 0 | No aplica | Sí |
| 7 | 10/08/2026 | CHANKA-001 | IPV | 60 | 60 | 0 | No aplica | Sí |
| 8 | 10/08/2026 | CHANKA-001 | VARI | 100 | 100 | 0 | No aplica | Sí |
| 9 | 10/08/2026 | CHANKA-001 | IPV | 100 | 120 | 20 | Sí | No |
| 10 | 10/08/2026 | CHANKA-001 | ROTA | 20 | 20 | 0 | No aplica | Sí |
| 11 | 10/08/2026 | CHANKA-001 | NEUM | 120 | 120 | 0 | No aplica | Sí |
| 12 | 10/08/2026 | CHANKA-001 | SPR | 40 | 40 | 0 | No aplica | Sí |
| 13 | 10/08/2026 | CHANKA-001 | PENT | 200 | 200 | 0 | No aplica | Sí |
| 14 | 10/08/2026 | CHANKA-001 | BCG | 120 | 120 | 0 | No aplica | Sí |
| 15 | 10/08/2026 | CHANKA-001 | NEUM | 20 | 20 | 0 | No aplica | Sí |
| 16 | 10/08/2026 | CHANKA-001 | SPR | 180 | 180 | 0 | No aplica | Sí |
| 17 | 10/08/2026 | CHANKA-001 | ROTA | 60 | 60 | 0 | No aplica | Sí |
| 18 | 10/08/2026 | CHANKA-001 | BCG | 50 | 45 | -5 | Sí | No |
| 19 | 10/08/2026 | CHANKA-001 | DTA | 30 | 50 | 20 | Sí | No |
| 20 | 10/08/2026 | CHANKA-001 | NEUM | 40 | 40 | 0 | No aplica | Sí |
| 21 | 10/08/2026 | CHANKA-001 | IPV | 120 | 120 | 0 | No aplica | Sí |
| 22 | 10/08/2026 | CHANKA-001 | SPR | 50 | 50 | 0 | No aplica | Sí |
| 23 | 10/08/2026 | CHANKA-001 | IPV | 80 | 80 | 0 | No aplica | Sí |
| 24 | 10/08/2026 | CHANKA-001 | SPR | 100 | 100 | 0 | No aplica | Sí |
| 25 | 10/08/2026 | CHANKA-001 | BCG | 40 | 40 | 0 | No aplica | Sí |

Cierre: 21 entregas concordantes ÷ 25 × 100 = **84.00 %**.

---

### Bloque 2 · TRAB-01 · Postest (Sistema SIVAC) · 12/10/2026

Documentos auditados: 40 · Conformes: 36 · RSD: 90.00 % · Entregas conciliadas: 25 · Concordantes: 22 · CPE: 88.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | AJU | ROTA | L-2610-01 | 20 | S | S | S | S | S | S | S | S | S | — |
| 2 | AJU | VARI | L-2610-02 | 120 | S | S | S | S | S | S | S | S | S | — |
| 3 | SAL | HEPB | L-2610-03 | 300 | S | S | S | S | N | S | S | S | N | M5 |
| 4 | AJU | SPR | L-2610-04 | 300 | S | S | S | S | S | S | S | S | S | — |
| 5 | TRA | PENT | L-2610-05 | 100 | S | S | S | S | S | S | S | S | S | — |
| 6 | DEV | DTA | L-2610-06 | 100 | S | S | S | S | S | S | S | S | S | — |
| 7 | SAL | NEUM | L-2610-07 | 80 | S | S | S | N | S | S | S | S | N | M4 |
| 8 | AJU | BCG | L-2610-08 | 100 | S | S | S | S | S | S | S | S | S | — |
| 9 | SAL | IPV | L-2610-09 | 100 | S | S | S | S | S | S | S | S | S | — |
| 10 | DEV | IPV | L-2610-10 | 40 | S | S | S | S | S | S | S | S | S | — |
| 11 | DEV | VARI | L-2610-11 | 60 | S | S | S | S | S | S | S | S | S | — |
| 12 | ING | DTA | L-2610-12 | 200 | S | S | S | S | S | S | S | S | S | — |
| 13 | SAL | IPV | L-2610-13 | 100 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | IPV | L-2610-14 | 240 | S | S | S | S | S | S | S | S | S | — |
| 15 | SAL | PENT | L-2610-15 | 80 | S | S | S | S | S | S | S | S | S | — |
| 16 | ING | NEUM | L-2610-16 | 120 | S | S | S | S | S | S | S | S | S | — |
| 17 | AJU | BCG | L-2610-17 | 150 | S | S | S | S | S | S | S | S | S | — |
| 18 | ING | INFL | L-2610-18 | 180 | S | S | S | S | S | S | S | S | S | — |
| 19 | DEV | HEPB | L-2610-19 | 150 | S | S | S | S | S | S | S | S | S | — |
| 20 | SAL | SPR | L-2610-20 | 100 | S | S | S | S | S | S | S | S | S | — |
| 21 | DEV | DTA | L-2610-21 | 80 | S | S | S | S | S | S | S | S | S | — |
| 22 | DEV | BCG | L-2610-22 | 80 | S | S | S | S | S | S | S | S | S | — |
| 23 | AJU | VARI | L-2610-23 | 60 | S | S | S | S | S | S | S | S | S | — |
| 24 | SAL | INFL | L-2610-24 | 300 | S | S | S | S | S | S | S | S | S | — |
| 25 | ING | DTA | L-2610-25 | 150 | S | S | S | S | S | S | S | S | S | — |
| 26 | AJU | BCG | L-2610-26 | 300 | S | S | S | S | S | S | S | S | S | — |
| 27 | TRA | HEPB | L-2610-27 | 100 | N | S | S | S | S | S | S | S | N | M1 |
| 28 | DEV | ROTA | L-2610-28 | 80 | S | S | N | S | S | S | S | S | N | M3 |
| 29 | DEV | ROTA | L-2610-29 | 240 | S | S | S | S | S | S | S | S | S | — |
| 30 | AJU | PENT | L-2610-30 | 80 | S | S | S | S | S | S | S | S | S | — |
| 31 | TRA | BCG | L-2610-31 | 300 | S | S | S | S | S | S | S | S | S | — |
| 32 | AJU | BCG | L-2610-32 | 80 | S | S | S | S | S | S | S | S | S | — |
| 33 | DEV | PENT | L-2610-33 | 60 | S | S | S | S | S | S | S | S | S | — |
| 34 | SAL | DTA | L-2610-34 | 80 | S | S | S | S | S | S | S | S | S | — |
| 35 | TRA | SPR | L-2610-35 | 300 | S | S | S | S | S | S | S | S | S | — |
| 36 | AJU | SPR | L-2610-36 | 100 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | DTA | L-2610-37 | 120 | S | S | S | S | S | S | S | S | S | — |
| 38 | DEV | DTA | L-2610-38 | 120 | S | S | S | S | S | S | S | S | S | — |
| 39 | ING | PENT | L-2610-39 | 100 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | DTA | L-2610-40 | 180 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-01 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 12/10/2026 | CHANKA-001 | PENT | 20 | 20 | 0 | No aplica | Sí |
| 2 | 12/10/2026 | CHANKA-001 | PENT | 60 | 60 | 0 | No aplica | Sí |
| 3 | 12/10/2026 | CHANKA-001 | VARI | 80 | 80 | 0 | No aplica | Sí |
| 4 | 12/10/2026 | CHANKA-001 | SPR | 200 | 200 | 0 | No aplica | Sí |
| 5 | 12/10/2026 | CHANKA-001 | PENT | 120 | 120 | 0 | No aplica | Sí |
| 6 | 12/10/2026 | CHANKA-001 | ROTA | 30 | 30 | 0 | No aplica | Sí |
| 7 | 12/10/2026 | CHANKA-001 | DTA | 50 | 50 | 0 | No aplica | Sí |
| 8 | 12/10/2026 | CHANKA-001 | VARI | 20 | 20 | 0 | No aplica | Sí |
| 9 | 12/10/2026 | CHANKA-001 | PENT | 120 | 120 | 0 | No aplica | Sí |
| 10 | 12/10/2026 | CHANKA-001 | IPV | 180 | 180 | 0 | No aplica | Sí |
| 11 | 12/10/2026 | CHANKA-001 | BCG | 180 | 180 | 0 | No aplica | Sí |
| 12 | 12/10/2026 | CHANKA-001 | INFL | 200 | 200 | 0 | No aplica | Sí |
| 13 | 12/10/2026 | CHANKA-001 | DTA | 60 | 60 | 0 | No aplica | Sí |
| 14 | 12/10/2026 | CHANKA-001 | NEUM | 80 | 80 | 0 | No aplica | Sí |
| 15 | 12/10/2026 | CHANKA-001 | DTA | 60 | 60 | 0 | No aplica | Sí |
| 16 | 12/10/2026 | CHANKA-001 | DTA | 180 | 180 | 0 | No aplica | Sí |
| 17 | 12/10/2026 | CHANKA-001 | INFL | 50 | 50 | 0 | No aplica | Sí |
| 18 | 12/10/2026 | CHANKA-001 | DTA | 150 | 155 | 5 | Sí | No |
| 19 | 12/10/2026 | CHANKA-001 | IPV | 100 | 105 | 5 | Sí | No |
| 20 | 12/10/2026 | CHANKA-001 | PENT | 120 | 120 | 0 | No aplica | Sí |
| 21 | 12/10/2026 | CHANKA-001 | HEPB | 50 | 30 | -20 | Sí | No |
| 22 | 12/10/2026 | CHANKA-001 | ROTA | 180 | 180 | 0 | No aplica | Sí |
| 23 | 12/10/2026 | CHANKA-001 | DTA | 20 | 20 | 0 | No aplica | Sí |
| 24 | 12/10/2026 | CHANKA-001 | NEUM | 200 | 200 | 0 | No aplica | Sí |
| 25 | 12/10/2026 | CHANKA-001 | HEPB | 30 | 30 | 0 | No aplica | Sí |

Cierre: 22 entregas concordantes ÷ 25 × 100 = **88.00 %**.

---

### Bloque 3 · TRAB-02 · Pretest (proceso manual) · 10/08/2026

Documentos auditados: 40 · Conformes: 30 · RSD: 75.00 % · Entregas conciliadas: 25 · Concordantes: 16 · CPE: 64.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | DEV | BCG | L-2608-01 | 20 | S | S | S | S | N | S | S | S | N | M5 |
| 2 | ING | BCG | L-2608-02 | 100 | S | S | S | S | S | S | S | S | S | — |
| 3 | ING | VARI | L-2608-03 | 100 | S | S | S | S | S | S | S | S | S | — |
| 4 | DEV | BCG | L-2608-04 | 200 | S | S | S | S | S | S | S | S | S | — |
| 5 | AJU | NEUM | L-2608-05 | 240 | S | S | S | S | S | S | S | S | S | — |
| 6 | AJU | DTA | L-2608-06 | 60 | S | S | S | S | S | S | S | S | S | — |
| 7 | ING | IPV | L-2608-07 | 120 | S | S | S | S | S | S | S | S | S | — |
| 8 | TRA | IPV | L-2608-08 | 20 | N | S | S | S | S | S | S | S | N | M1 |
| 9 | TRA | BCG | L-2608-09 | 80 | S | S | S | S | S | S | S | S | S | — |
| 10 | ING | INFL | L-2608-10 | 80 | S | S | S | S | S | S | S | S | S | — |
| 11 | AJU | INFL | L-2608-11 | 40 | S | N | S | S | S | S | S | S | N | M2 |
| 12 | ING | PENT | L-2608-12 | 80 | S | N | S | S | S | S | S | S | N | M2 |
| 13 | SAL | DTA | L-2608-13 | 100 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | INFL | L-2608-14 | 40 | S | S | S | S | S | S | S | S | S | — |
| 15 | SAL | INFL | L-2608-15 | 200 | S | S | S | S | S | S | S | S | S | — |
| 16 | AJU | IPV | L-2608-16 | 60 | S | S | S | S | S | S | S | S | S | — |
| 17 | ING | VARI | L-2608-17 | 120 | S | S | S | S | N | S | S | S | N | M5 |
| 18 | DEV | VARI | L-2608-18 | 120 | S | S | S | S | S | S | S | S | S | — |
| 19 | AJU | SPR | L-2608-19 | 60 | S | S | S | S | S | S | S | S | S | — |
| 20 | SAL | PENT | L-2608-20 | 240 | S | S | S | S | N | S | S | S | N | M5 |
| 21 | DEV | SPR | L-2608-21 | 240 | S | S | S | S | S | S | S | S | S | — |
| 22 | AJU | DTA | L-2608-22 | 60 | S | S | N | S | S | S | S | S | N | M3 |
| 23 | SAL | VARI | L-2608-23 | 40 | S | S | S | S | S | S | S | S | S | — |
| 24 | SAL | PENT | L-2608-24 | 100 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | DTA | L-2608-25 | 240 | S | S | S | N | S | S | S | S | N | M4 |
| 26 | DEV | BCG | L-2608-26 | 120 | S | S | S | S | S | N | S | S | N | M6 |
| 27 | DEV | BCG | L-2608-27 | 300 | S | S | S | S | S | S | S | S | S | — |
| 28 | ING | BCG | L-2608-28 | 80 | S | S | S | S | S | S | S | S | S | — |
| 29 | SAL | HEPB | L-2608-29 | 60 | S | S | S | S | S | S | S | S | S | — |
| 30 | DEV | IPV | L-2608-30 | 40 | S | S | S | S | S | S | S | S | S | — |
| 31 | DEV | BCG | L-2608-31 | 20 | S | S | S | S | S | S | S | S | S | — |
| 32 | DEV | NEUM | L-2608-32 | 150 | S | S | S | S | S | S | S | S | S | — |
| 33 | SAL | VARI | L-2608-33 | 100 | S | S | S | S | S | S | S | S | S | — |
| 34 | DEV | SPR | L-2608-34 | 100 | S | S | S | S | S | S | S | S | S | — |
| 35 | SAL | SPR | L-2608-35 | 240 | S | S | S | S | S | S | S | S | S | — |
| 36 | SAL | NEUM | L-2608-36 | 100 | S | S | S | S | S | S | S | S | S | — |
| 37 | ING | HEPB | L-2608-37 | 300 | S | S | S | S | S | S | S | S | S | — |
| 38 | ING | BCG | L-2608-38 | 150 | S | S | S | S | N | S | S | S | N | M5 |
| 39 | TRA | INFL | L-2608-39 | 40 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | INFL | L-2608-40 | 100 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-02 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 10/08/2026 | CHANKA-001 | VARI | 200 | 200 | 0 | No aplica | Sí |
| 2 | 10/08/2026 | CHANKA-001 | PENT | 150 | 150 | 0 | No aplica | Sí |
| 3 | 10/08/2026 | CHANKA-001 | IPV | 20 | 30 | 10 | Sí | No |
| 4 | 10/08/2026 | CHANKA-001 | SPR | 30 | 30 | 0 | No aplica | Sí |
| 5 | 10/08/2026 | CHANKA-001 | HEPB | 80 | 85 | 5 | Sí | No |
| 6 | 10/08/2026 | CHANKA-001 | BCG | 50 | 50 | 0 | No aplica | Sí |
| 7 | 10/08/2026 | CHANKA-001 | NEUM | 30 | 30 | 0 | No aplica | Sí |
| 8 | 10/08/2026 | CHANKA-001 | VARI | 120 | 130 | 10 | Sí | No |
| 9 | 10/08/2026 | CHANKA-001 | DTA | 30 | 50 | 20 | Sí | No |
| 10 | 10/08/2026 | CHANKA-001 | INFL | 80 | 80 | 0 | No aplica | Sí |
| 11 | 10/08/2026 | CHANKA-001 | HEPB | 30 | 30 | 0 | No aplica | Sí |
| 12 | 10/08/2026 | CHANKA-001 | DTA | 60 | 40 | -20 | Sí | No |
| 13 | 10/08/2026 | CHANKA-001 | VARI | 80 | 80 | 0 | No aplica | Sí |
| 14 | 10/08/2026 | CHANKA-001 | PENT | 150 | 150 | 0 | No aplica | Sí |
| 15 | 10/08/2026 | CHANKA-001 | HEPB | 80 | 80 | 0 | No aplica | Sí |
| 16 | 10/08/2026 | CHANKA-001 | INFL | 180 | 200 | 20 | Sí | No |
| 17 | 10/08/2026 | CHANKA-001 | PENT | 60 | 55 | -5 | Sí | No |
| 18 | 10/08/2026 | CHANKA-001 | NEUM | 120 | 140 | 20 | Sí | No |
| 19 | 10/08/2026 | CHANKA-001 | INFL | 50 | 50 | 0 | No aplica | Sí |
| 20 | 10/08/2026 | CHANKA-001 | HEPB | 200 | 200 | 0 | No aplica | Sí |
| 21 | 10/08/2026 | CHANKA-001 | IPV | 30 | 30 | 0 | No aplica | Sí |
| 22 | 10/08/2026 | CHANKA-001 | HEPB | 150 | 150 | 0 | No aplica | Sí |
| 23 | 10/08/2026 | CHANKA-001 | SPR | 30 | 30 | 0 | No aplica | Sí |
| 24 | 10/08/2026 | CHANKA-001 | ROTA | 120 | 115 | -5 | Sí | No |
| 25 | 10/08/2026 | CHANKA-001 | INFL | 30 | 30 | 0 | No aplica | Sí |

Cierre: 16 entregas concordantes ÷ 25 × 100 = **64.00 %**.

---

### Bloque 4 · TRAB-02 · Postest (Sistema SIVAC) · 12/10/2026

Documentos auditados: 40 · Conformes: 35 · RSD: 87.50 % · Entregas conciliadas: 25 · Concordantes: 23 · CPE: 92.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | SAL | ROTA | L-2610-01 | 150 | N | S | S | S | S | S | S | S | N | M1 |
| 2 | ING | SPR | L-2610-02 | 180 | S | S | S | S | S | S | S | S | S | — |
| 3 | TRA | VARI | L-2610-03 | 180 | S | S | S | S | S | S | S | S | S | — |
| 4 | DEV | SPR | L-2610-04 | 150 | S | S | S | S | S | S | S | S | S | — |
| 5 | ING | HEPB | L-2610-05 | 100 | S | S | S | S | S | S | S | S | S | — |
| 6 | SAL | ROTA | L-2610-06 | 60 | S | S | S | S | S | S | S | S | S | — |
| 7 | DEV | HEPB | L-2610-07 | 240 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | INFL | L-2610-08 | 120 | S | S | S | S | S | S | S | S | S | — |
| 9 | DEV | NEUM | L-2610-09 | 60 | S | S | S | S | S | S | S | S | S | — |
| 10 | DEV | ROTA | L-2610-10 | 100 | S | S | S | S | S | S | S | S | S | — |
| 11 | AJU | ROTA | L-2610-11 | 300 | S | S | S | S | S | S | S | S | S | — |
| 12 | AJU | HEPB | L-2610-12 | 120 | S | S | S | S | S | N | S | S | N | M6 |
| 13 | DEV | PENT | L-2610-13 | 200 | S | S | S | S | S | S | S | S | S | — |
| 14 | DEV | HEPB | L-2610-14 | 100 | N | S | S | S | S | S | S | S | N | M1 |
| 15 | ING | HEPB | L-2610-15 | 300 | S | S | S | S | S | S | S | S | S | — |
| 16 | TRA | PENT | L-2610-16 | 180 | N | S | S | S | S | S | S | S | N | M1 |
| 17 | TRA | VARI | L-2610-17 | 180 | S | S | S | S | S | S | S | S | S | — |
| 18 | DEV | DTA | L-2610-18 | 40 | S | S | S | S | S | S | S | S | S | — |
| 19 | AJU | NEUM | L-2610-19 | 150 | S | S | S | S | S | S | S | S | S | — |
| 20 | AJU | PENT | L-2610-20 | 60 | S | S | S | S | S | S | S | S | S | — |
| 21 | DEV | IPV | L-2610-21 | 60 | S | S | S | S | S | S | S | S | S | — |
| 22 | SAL | ROTA | L-2610-22 | 100 | S | S | S | S | S | S | S | S | S | — |
| 23 | DEV | SPR | L-2610-23 | 240 | S | S | S | S | S | S | S | S | S | — |
| 24 | AJU | DTA | L-2610-24 | 180 | S | S | S | S | S | S | S | S | S | — |
| 25 | ING | SPR | L-2610-25 | 60 | S | S | S | S | S | S | S | S | S | — |
| 26 | AJU | PENT | L-2610-26 | 80 | S | S | S | S | S | S | S | S | S | — |
| 27 | AJU | PENT | L-2610-27 | 100 | S | S | S | S | S | S | S | S | S | — |
| 28 | TRA | IPV | L-2610-28 | 180 | S | S | S | S | S | S | S | S | S | — |
| 29 | SAL | VARI | L-2610-29 | 180 | S | S | S | S | S | S | S | S | S | — |
| 30 | SAL | INFL | L-2610-30 | 40 | S | S | S | S | S | S | S | S | S | — |
| 31 | SAL | VARI | L-2610-31 | 80 | S | S | S | S | S | S | S | S | S | — |
| 32 | DEV | HEPB | L-2610-32 | 240 | S | S | S | S | S | S | S | S | S | — |
| 33 | AJU | HEPB | L-2610-33 | 200 | S | S | S | S | S | S | S | S | S | — |
| 34 | AJU | INFL | L-2610-34 | 60 | S | S | S | N | S | S | S | S | N | M4 |
| 35 | SAL | BCG | L-2610-35 | 240 | S | S | S | S | S | S | S | S | S | — |
| 36 | DEV | IPV | L-2610-36 | 60 | S | S | S | S | S | S | S | S | S | — |
| 37 | ING | VARI | L-2610-37 | 300 | S | S | S | S | S | S | S | S | S | — |
| 38 | SAL | IPV | L-2610-38 | 180 | S | S | S | S | S | S | S | S | S | — |
| 39 | SAL | NEUM | L-2610-39 | 80 | S | S | S | S | S | S | S | S | S | — |
| 40 | AJU | SPR | L-2610-40 | 100 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-02 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 12/10/2026 | CHANKA-001 | BCG | 50 | 50 | 0 | No aplica | Sí |
| 2 | 12/10/2026 | CHANKA-001 | INFL | 180 | 180 | 0 | No aplica | Sí |
| 3 | 12/10/2026 | CHANKA-001 | INFL | 120 | 120 | 0 | No aplica | Sí |
| 4 | 12/10/2026 | CHANKA-001 | SPR | 50 | 50 | 0 | No aplica | Sí |
| 5 | 12/10/2026 | CHANKA-001 | INFL | 40 | 40 | 0 | No aplica | Sí |
| 6 | 12/10/2026 | CHANKA-001 | BCG | 40 | 40 | 0 | No aplica | Sí |
| 7 | 12/10/2026 | CHANKA-001 | VARI | 180 | 180 | 0 | No aplica | Sí |
| 8 | 12/10/2026 | CHANKA-001 | NEUM | 60 | 60 | 0 | No aplica | Sí |
| 9 | 12/10/2026 | CHANKA-001 | PENT | 100 | 100 | 0 | No aplica | Sí |
| 10 | 12/10/2026 | CHANKA-001 | NEUM | 80 | 80 | 0 | No aplica | Sí |
| 11 | 12/10/2026 | CHANKA-001 | NEUM | 80 | 80 | 0 | No aplica | Sí |
| 12 | 12/10/2026 | CHANKA-001 | PENT | 180 | 180 | 0 | No aplica | Sí |
| 13 | 12/10/2026 | CHANKA-001 | HEPB | 120 | 120 | 0 | No aplica | Sí |
| 14 | 12/10/2026 | CHANKA-001 | VARI | 200 | 200 | 0 | No aplica | Sí |
| 15 | 12/10/2026 | CHANKA-001 | NEUM | 40 | 40 | 0 | No aplica | Sí |
| 16 | 12/10/2026 | CHANKA-001 | PENT | 30 | 30 | 0 | No aplica | Sí |
| 17 | 12/10/2026 | CHANKA-001 | IPV | 60 | 60 | 0 | No aplica | Sí |
| 18 | 12/10/2026 | CHANKA-001 | INFL | 20 | 25 | 5 | Sí | No |
| 19 | 12/10/2026 | CHANKA-001 | BCG | 40 | 40 | 0 | No aplica | Sí |
| 20 | 12/10/2026 | CHANKA-001 | IPV | 100 | 100 | 0 | No aplica | Sí |
| 21 | 12/10/2026 | CHANKA-001 | BCG | 150 | 150 | 0 | No aplica | Sí |
| 22 | 12/10/2026 | CHANKA-001 | BCG | 30 | 25 | -5 | Sí | No |
| 23 | 12/10/2026 | CHANKA-001 | DTA | 50 | 50 | 0 | No aplica | Sí |
| 24 | 12/10/2026 | CHANKA-001 | BCG | 150 | 150 | 0 | No aplica | Sí |
| 25 | 12/10/2026 | CHANKA-001 | NEUM | 150 | 150 | 0 | No aplica | Sí |

Cierre: 23 entregas concordantes ÷ 25 × 100 = **92.00 %**.

---

### Bloque 5 · TRAB-03 · Pretest (proceso manual) · 11/08/2026

Documentos auditados: 40 · Conformes: 24 · RSD: 60.00 % · Entregas conciliadas: 25 · Concordantes: 14 · CPE: 56.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | ING | PENT | L-2608-01 | 180 | S | S | N | S | S | S | S | S | N | M3 |
| 2 | SAL | BCG | L-2608-02 | 150 | S | S | S | S | S | S | S | S | S | — |
| 3 | AJU | HEPB | L-2608-03 | 180 | S | S | S | S | N | S | S | S | N | M5 |
| 4 | AJU | INFL | L-2608-04 | 100 | S | S | S | S | S | S | S | S | S | — |
| 5 | AJU | BCG | L-2608-05 | 80 | S | S | S | S | S | S | S | S | S | — |
| 6 | TRA | DTA | L-2608-06 | 100 | S | S | S | S | S | S | S | S | S | — |
| 7 | ING | BCG | L-2608-07 | 20 | S | S | S | S | S | S | S | S | S | — |
| 8 | TRA | IPV | L-2608-08 | 100 | S | S | S | S | S | N | S | S | N | M6 |
| 9 | SAL | VARI | L-2608-09 | 150 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | ROTA | L-2608-10 | 150 | S | S | S | S | S | S | S | S | S | — |
| 11 | DEV | NEUM | L-2608-11 | 100 | S | S | S | S | N | S | S | S | N | M5 |
| 12 | SAL | IPV | L-2608-12 | 240 | S | S | S | S | S | S | S | S | S | — |
| 13 | AJU | DTA | L-2608-13 | 300 | S | S | S | S | S | S | N | S | N | M7 |
| 14 | AJU | DTA | L-2608-14 | 100 | S | S | S | S | S | S | S | S | S | — |
| 15 | SAL | SPR | L-2608-15 | 120 | S | S | S | S | S | S | S | S | S | — |
| 16 | ING | DTA | L-2608-16 | 100 | S | S | S | S | S | S | S | S | S | — |
| 17 | SAL | PENT | L-2608-17 | 60 | S | S | S | S | S | S | N | S | N | M7 |
| 18 | ING | PENT | L-2608-18 | 240 | S | S | S | S | S | S | S | S | S | — |
| 19 | DEV | INFL | L-2608-19 | 200 | S | S | S | S | S | S | S | S | S | — |
| 20 | SAL | PENT | L-2608-20 | 60 | S | S | S | S | S | S | S | S | S | — |
| 21 | TRA | PENT | L-2608-21 | 60 | S | S | S | S | S | S | S | S | S | — |
| 22 | ING | PENT | L-2608-22 | 180 | S | S | S | S | S | S | S | S | S | — |
| 23 | AJU | HEPB | L-2608-23 | 180 | S | S | N | S | S | S | S | S | N | M3 |
| 24 | SAL | ROTA | L-2608-24 | 300 | S | S | S | N | S | S | S | S | N | M4 |
| 25 | AJU | INFL | L-2608-25 | 40 | S | S | S | S | N | S | S | S | N | M5 |
| 26 | SAL | NEUM | L-2608-26 | 240 | S | S | S | S | S | S | S | S | S | — |
| 27 | AJU | ROTA | L-2608-27 | 40 | N | S | S | S | S | S | S | S | N | M1 |
| 28 | DEV | SPR | L-2608-28 | 80 | S | S | S | S | S | S | S | S | S | — |
| 29 | TRA | PENT | L-2608-29 | 180 | S | S | S | S | N | S | S | S | N | M5 |
| 30 | AJU | PENT | L-2608-30 | 20 | S | S | S | S | S | S | S | S | S | — |
| 31 | TRA | IPV | L-2608-31 | 120 | S | S | S | S | S | S | S | S | S | — |
| 32 | AJU | BCG | L-2608-32 | 80 | S | S | S | S | S | S | S | S | S | — |
| 33 | TRA | INFL | L-2608-33 | 200 | S | S | S | S | S | S | S | S | S | — |
| 34 | TRA | VARI | L-2608-34 | 200 | S | S | N | S | S | S | S | S | N | M3 |
| 35 | DEV | ROTA | L-2608-35 | 180 | S | S | S | N | S | S | S | S | N | M4 |
| 36 | ING | BCG | L-2608-36 | 180 | S | S | S | S | S | S | S | S | S | — |
| 37 | ING | VARI | L-2608-37 | 80 | S | S | N | S | S | S | S | S | N | M3 |
| 38 | SAL | IPV | L-2608-38 | 80 | S | S | S | S | S | S | S | S | S | — |
| 39 | SAL | BCG | L-2608-39 | 150 | S | S | S | N | S | S | S | S | N | M4 |
| 40 | SAL | DTA | L-2608-40 | 120 | S | S | S | S | S | S | S | N | N | M8 |

**Entregas conciliadas — TRAB-03 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 11/08/2026 | S/C | DTA | 150 | 170 | 20 | Sí | No |
| 2 | 11/08/2026 | S/C | IPV | 40 | 20 | -20 | Sí | No |
| 3 | 11/08/2026 | S/C | BCG | 200 | 200 | 0 | No aplica | Sí |
| 4 | 11/08/2026 | S/C | BCG | 200 | 200 | 0 | No aplica | Sí |
| 5 | 11/08/2026 | S/C | HEPB | 30 | 30 | 0 | No aplica | Sí |
| 6 | 11/08/2026 | S/C | SPR | 200 | 180 | -20 | Sí | No |
| 7 | 11/08/2026 | S/C | PENT | 150 | 140 | -10 | Sí | No |
| 8 | 11/08/2026 | S/C | BCG | 40 | 45 | 5 | Sí | No |
| 9 | 11/08/2026 | S/C | DTA | 200 | 200 | 0 | No aplica | Sí |
| 10 | 11/08/2026 | S/C | INFL | 150 | 150 | 0 | No aplica | Sí |
| 11 | 11/08/2026 | S/C | VARI | 40 | 40 | 0 | No aplica | Sí |
| 12 | 11/08/2026 | S/C | HEPB | 150 | 150 | 0 | No aplica | Sí |
| 13 | 11/08/2026 | S/C | VARI | 80 | 75 | -5 | Sí | No |
| 14 | 11/08/2026 | S/C | HEPB | 20 | 20 | 0 | No aplica | Sí |
| 15 | 11/08/2026 | S/C | ROTA | 150 | 150 | 0 | No aplica | Sí |
| 16 | 11/08/2026 | S/C | SPR | 20 | 20 | 0 | No aplica | Sí |
| 17 | 11/08/2026 | S/C | DTA | 40 | 40 | 0 | No aplica | Sí |
| 18 | 11/08/2026 | S/C | BCG | 100 | 100 | 0 | No aplica | Sí |
| 19 | 11/08/2026 | S/C | DTA | 100 | 110 | 10 | Sí | No |
| 20 | 11/08/2026 | S/C | DTA | 60 | 65 | 5 | Sí | No |
| 21 | 11/08/2026 | S/C | INFL | 150 | 150 | 0 | No aplica | Sí |
| 22 | 11/08/2026 | S/C | DTA | 50 | 50 | 0 | No aplica | Sí |
| 23 | 11/08/2026 | S/C | IPV | 180 | 170 | -10 | Sí | No |
| 24 | 11/08/2026 | S/C | DTA | 100 | 90 | -10 | Sí | No |
| 25 | 11/08/2026 | S/C | VARI | 50 | 30 | -20 | Sí | No |

Cierre: 14 entregas concordantes ÷ 25 × 100 = **56.00 %**.

---

### Bloque 6 · TRAB-03 · Postest (Sistema SIVAC) · 13/10/2026

Documentos auditados: 40 · Conformes: 37 · RSD: 92.50 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | AJU | HEPB | L-2610-01 | 20 | S | S | S | S | S | S | S | S | S | — |
| 2 | ING | DTA | L-2610-02 | 200 | S | S | S | S | S | S | S | S | S | — |
| 3 | ING | INFL | L-2610-03 | 240 | S | S | S | S | S | S | S | S | S | — |
| 4 | DEV | BCG | L-2610-04 | 20 | S | S | S | S | S | S | S | S | S | — |
| 5 | DEV | HEPB | L-2610-05 | 20 | S | S | S | S | S | S | S | S | S | — |
| 6 | AJU | IPV | L-2610-06 | 20 | S | S | S | S | S | S | S | S | S | — |
| 7 | SAL | DTA | L-2610-07 | 240 | S | S | S | S | S | S | S | S | S | — |
| 8 | ING | PENT | L-2610-08 | 200 | S | S | S | S | S | S | S | S | S | — |
| 9 | SAL | NEUM | L-2610-09 | 40 | S | S | S | S | S | S | S | S | S | — |
| 10 | ING | NEUM | L-2610-10 | 80 | S | S | S | S | S | S | S | S | S | — |
| 11 | ING | HEPB | L-2610-11 | 200 | S | S | S | S | S | S | S | S | S | — |
| 12 | SAL | VARI | L-2610-12 | 100 | S | S | S | S | S | S | S | S | S | — |
| 13 | SAL | DTA | L-2610-13 | 300 | S | S | S | S | S | S | S | S | S | — |
| 14 | DEV | INFL | L-2610-14 | 240 | S | S | S | S | S | S | S | S | S | — |
| 15 | DEV | BCG | L-2610-15 | 240 | S | S | S | S | S | S | S | S | S | — |
| 16 | AJU | PENT | L-2610-16 | 150 | S | S | S | S | S | S | S | S | S | — |
| 17 | SAL | HEPB | L-2610-17 | 60 | S | S | S | S | S | S | S | S | S | — |
| 18 | TRA | IPV | L-2610-18 | 300 | S | S | S | S | S | S | S | S | S | — |
| 19 | ING | VARI | L-2610-19 | 180 | S | S | S | S | S | S | S | S | S | — |
| 20 | TRA | HEPB | L-2610-20 | 20 | S | S | S | S | S | S | S | S | S | — |
| 21 | TRA | ROTA | L-2610-21 | 240 | S | S | S | S | S | S | S | S | S | — |
| 22 | TRA | BCG | L-2610-22 | 40 | S | S | S | S | S | S | S | S | S | — |
| 23 | TRA | VARI | L-2610-23 | 150 | S | N | S | S | S | S | S | S | N | M2 |
| 24 | AJU | SPR | L-2610-24 | 40 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | PENT | L-2610-25 | 180 | S | S | S | S | S | S | S | S | S | — |
| 26 | TRA | NEUM | L-2610-26 | 100 | S | S | S | S | S | S | S | S | S | — |
| 27 | DEV | DTA | L-2610-27 | 120 | S | S | S | S | S | S | S | S | S | — |
| 28 | SAL | IPV | L-2610-28 | 40 | S | S | S | S | S | S | S | S | S | — |
| 29 | DEV | BCG | L-2610-29 | 60 | S | S | N | S | S | S | S | S | N | M3 |
| 30 | ING | HEPB | L-2610-30 | 100 | S | N | S | S | S | S | S | S | N | M2 |
| 31 | DEV | INFL | L-2610-31 | 120 | S | S | S | S | S | S | S | S | S | — |
| 32 | ING | NEUM | L-2610-32 | 180 | S | S | S | S | S | S | S | S | S | — |
| 33 | ING | HEPB | L-2610-33 | 120 | S | S | S | S | S | S | S | S | S | — |
| 34 | SAL | ROTA | L-2610-34 | 200 | S | S | S | S | S | S | S | S | S | — |
| 35 | AJU | NEUM | L-2610-35 | 240 | S | S | S | S | S | S | S | S | S | — |
| 36 | TRA | SPR | L-2610-36 | 200 | S | S | S | S | S | S | S | S | S | — |
| 37 | AJU | NEUM | L-2610-37 | 180 | S | S | S | S | S | S | S | S | S | — |
| 38 | SAL | NEUM | L-2610-38 | 80 | S | S | S | S | S | S | S | S | S | — |
| 39 | TRA | NEUM | L-2610-39 | 180 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | IPV | L-2610-40 | 80 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-03 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 13/10/2026 | S/C | IPV | 180 | 180 | 0 | No aplica | Sí |
| 2 | 13/10/2026 | S/C | IPV | 100 | 100 | 0 | No aplica | Sí |
| 3 | 13/10/2026 | S/C | IPV | 20 | 20 | 0 | No aplica | Sí |
| 4 | 13/10/2026 | S/C | ROTA | 30 | 30 | 0 | No aplica | Sí |
| 5 | 13/10/2026 | S/C | DTA | 50 | 50 | 0 | No aplica | Sí |
| 6 | 13/10/2026 | S/C | SPR | 120 | 120 | 0 | No aplica | Sí |
| 7 | 13/10/2026 | S/C | NEUM | 50 | 50 | 0 | No aplica | Sí |
| 8 | 13/10/2026 | S/C | DTA | 180 | 180 | 0 | No aplica | Sí |
| 9 | 13/10/2026 | S/C | SPR | 40 | 40 | 0 | No aplica | Sí |
| 10 | 13/10/2026 | S/C | ROTA | 150 | 150 | 0 | No aplica | Sí |
| 11 | 13/10/2026 | S/C | PENT | 120 | 120 | 0 | No aplica | Sí |
| 12 | 13/10/2026 | S/C | ROTA | 20 | 20 | 0 | No aplica | Sí |
| 13 | 13/10/2026 | S/C | ROTA | 20 | 20 | 0 | No aplica | Sí |
| 14 | 13/10/2026 | S/C | DTA | 100 | 100 | 0 | No aplica | Sí |
| 15 | 13/10/2026 | S/C | HEPB | 200 | 200 | 0 | No aplica | Sí |
| 16 | 13/10/2026 | S/C | IPV | 40 | 40 | 0 | No aplica | Sí |
| 17 | 13/10/2026 | S/C | BCG | 120 | 120 | 0 | No aplica | Sí |
| 18 | 13/10/2026 | S/C | ROTA | 100 | 100 | 0 | No aplica | Sí |
| 19 | 13/10/2026 | S/C | BCG | 50 | 50 | 0 | No aplica | Sí |
| 20 | 13/10/2026 | S/C | ROTA | 20 | 20 | 0 | No aplica | Sí |
| 21 | 13/10/2026 | S/C | DTA | 40 | 40 | 0 | No aplica | Sí |
| 22 | 13/10/2026 | S/C | BCG | 200 | 195 | -5 | Sí | No |
| 23 | 13/10/2026 | S/C | IPV | 150 | 150 | 0 | No aplica | Sí |
| 24 | 13/10/2026 | S/C | HEPB | 20 | 20 | 0 | No aplica | Sí |
| 25 | 13/10/2026 | S/C | HEPB | 40 | 40 | 0 | No aplica | Sí |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 7 · TRAB-04 · Pretest (proceso manual) · 11/08/2026

Documentos auditados: 40 · Conformes: 23 · RSD: 57.50 % · Entregas conciliadas: 25 · Concordantes: 16 · CPE: 64.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | AJU | DTA | L-2608-01 | 200 | S | S | S | S | S | S | S | S | S | — |
| 2 | DEV | DTA | L-2608-02 | 300 | S | S | S | S | S | S | S | N | N | M8 |
| 3 | TRA | DTA | L-2608-03 | 80 | S | S | S | S | S | S | S | S | S | — |
| 4 | SAL | PENT | L-2608-04 | 60 | S | S | S | S | S | S | S | S | S | — |
| 5 | DEV | BCG | L-2608-05 | 300 | S | S | N | S | S | S | S | S | N | M3 |
| 6 | AJU | IPV | L-2608-06 | 80 | S | S | S | S | S | S | S | S | S | — |
| 7 | ING | BCG | L-2608-07 | 200 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | HEPB | L-2608-08 | 60 | S | S | S | S | S | S | S | S | S | — |
| 9 | AJU | IPV | L-2608-09 | 200 | S | S | S | S | S | S | S | S | S | — |
| 10 | ING | NEUM | L-2608-10 | 20 | S | S | S | S | N | S | S | S | N | M5 |
| 11 | SAL | SPR | L-2608-11 | 20 | S | S | S | S | S | S | S | S | S | — |
| 12 | TRA | BCG | L-2608-12 | 180 | S | S | N | S | S | S | S | S | N | M3 |
| 13 | DEV | VARI | L-2608-13 | 60 | S | S | S | S | N | S | S | S | N | M5 |
| 14 | DEV | IPV | L-2608-14 | 100 | N | S | S | S | S | S | S | S | N | M1 |
| 15 | TRA | PENT | L-2608-15 | 20 | S | S | S | S | S | S | S | S | S | — |
| 16 | ING | HEPB | L-2608-16 | 40 | N | S | S | S | S | S | S | S | N | M1 |
| 17 | ING | BCG | L-2608-17 | 40 | N | S | S | S | S | S | S | S | N | M1 |
| 18 | SAL | BCG | L-2608-18 | 80 | S | S | S | S | S | S | S | S | S | — |
| 19 | SAL | SPR | L-2608-19 | 80 | S | S | S | S | S | S | S | S | S | — |
| 20 | AJU | HEPB | L-2608-20 | 60 | S | N | S | S | S | S | S | S | N | M2 |
| 21 | ING | ROTA | L-2608-21 | 180 | S | S | S | S | S | S | S | S | S | — |
| 22 | SAL | DTA | L-2608-22 | 120 | S | S | S | S | S | S | S | S | S | — |
| 23 | ING | DTA | L-2608-23 | 80 | S | N | S | S | S | S | S | S | N | M2 |
| 24 | AJU | PENT | L-2608-24 | 120 | S | S | S | S | S | S | S | S | S | — |
| 25 | AJU | BCG | L-2608-25 | 200 | S | N | S | S | S | S | S | S | N | M2 |
| 26 | SAL | ROTA | L-2608-26 | 200 | S | S | S | S | S | S | S | S | S | — |
| 27 | TRA | IPV | L-2608-27 | 240 | N | S | S | S | S | S | S | S | N | M1 |
| 28 | ING | INFL | L-2608-28 | 180 | S | S | S | S | S | S | S | S | S | — |
| 29 | SAL | ROTA | L-2608-29 | 150 | S | S | S | S | S | S | S | S | S | — |
| 30 | TRA | VARI | L-2608-30 | 80 | S | S | S | S | S | S | S | S | S | — |
| 31 | DEV | IPV | L-2608-31 | 150 | S | S | S | S | S | S | S | S | S | — |
| 32 | AJU | IPV | L-2608-32 | 120 | S | S | S | S | S | S | S | S | S | — |
| 33 | ING | IPV | L-2608-33 | 240 | S | S | S | S | S | S | S | S | S | — |
| 34 | AJU | DTA | L-2608-34 | 150 | S | S | S | S | S | S | N | S | N | M7 |
| 35 | SAL | IPV | L-2608-35 | 80 | S | S | N | S | S | S | S | S | N | M3 |
| 36 | TRA | DTA | L-2608-36 | 120 | S | S | S | S | S | N | S | S | N | M6 |
| 37 | SAL | NEUM | L-2608-37 | 40 | S | S | N | S | S | S | S | S | N | M3 |
| 38 | DEV | NEUM | L-2608-38 | 80 | S | S | S | S | S | S | S | S | S | — |
| 39 | TRA | ROTA | L-2608-39 | 60 | S | S | S | S | S | S | S | S | S | — |
| 40 | SAL | HEPB | L-2608-40 | 180 | S | S | S | S | N | S | S | S | N | M5 |

**Entregas conciliadas — TRAB-04 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 11/08/2026 | 6804 | NEUM | 20 | 30 | 10 | Sí | No |
| 2 | 11/08/2026 | 6804 | VARI | 150 | 150 | 0 | No aplica | Sí |
| 3 | 11/08/2026 | 6804 | SPR | 150 | 155 | 5 | Sí | No |
| 4 | 11/08/2026 | 6804 | NEUM | 20 | 20 | 0 | No aplica | Sí |
| 5 | 11/08/2026 | 6804 | NEUM | 20 | 20 | 0 | No aplica | Sí |
| 6 | 11/08/2026 | 6804 | NEUM | 60 | 60 | 0 | No aplica | Sí |
| 7 | 11/08/2026 | 6804 | INFL | 60 | 60 | 0 | No aplica | Sí |
| 8 | 11/08/2026 | 6804 | DTA | 150 | 150 | 0 | No aplica | Sí |
| 9 | 11/08/2026 | 6804 | INFL | 200 | 210 | 10 | Sí | No |
| 10 | 11/08/2026 | 6804 | HEPB | 100 | 100 | 0 | No aplica | Sí |
| 11 | 11/08/2026 | 6804 | ROTA | 120 | 120 | 0 | No aplica | Sí |
| 12 | 11/08/2026 | 6804 | INFL | 120 | 120 | 0 | No aplica | Sí |
| 13 | 11/08/2026 | 6804 | IPV | 120 | 120 | 0 | No aplica | Sí |
| 14 | 11/08/2026 | 6804 | DTA | 150 | 170 | 20 | Sí | No |
| 15 | 11/08/2026 | 6804 | IPV | 150 | 145 | -5 | Sí | No |
| 16 | 11/08/2026 | 6804 | DTA | 150 | 150 | 0 | No aplica | Sí |
| 17 | 11/08/2026 | 6804 | VARI | 50 | 50 | 0 | No aplica | Sí |
| 18 | 11/08/2026 | 6804 | VARI | 120 | 125 | 5 | Sí | No |
| 19 | 11/08/2026 | 6804 | HEPB | 180 | 170 | -10 | Sí | No |
| 20 | 11/08/2026 | 6804 | BCG | 50 | 45 | -5 | Sí | No |
| 21 | 11/08/2026 | 6804 | INFL | 120 | 120 | 0 | No aplica | Sí |
| 22 | 11/08/2026 | 6804 | BCG | 20 | 30 | 10 | Sí | No |
| 23 | 11/08/2026 | 6804 | ROTA | 200 | 200 | 0 | No aplica | Sí |
| 24 | 11/08/2026 | 6804 | VARI | 200 | 200 | 0 | No aplica | Sí |
| 25 | 11/08/2026 | 6804 | NEUM | 30 | 30 | 0 | No aplica | Sí |

Cierre: 16 entregas concordantes ÷ 25 × 100 = **64.00 %**.

---

### Bloque 8 · TRAB-04 · Postest (Sistema SIVAC) · 13/10/2026

Documentos auditados: 40 · Conformes: 38 · RSD: 95.00 % · Entregas conciliadas: 25 · Concordantes: 23 · CPE: 92.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | SAL | BCG | L-2610-01 | 180 | S | S | S | S | S | S | S | S | S | — |
| 2 | AJU | NEUM | L-2610-02 | 20 | S | S | S | S | S | S | S | S | S | — |
| 3 | DEV | INFL | L-2610-03 | 300 | S | S | S | S | S | S | S | S | S | — |
| 4 | SAL | NEUM | L-2610-04 | 40 | S | S | S | S | S | S | S | S | S | — |
| 5 | TRA | PENT | L-2610-05 | 40 | S | S | S | S | S | S | S | S | S | — |
| 6 | DEV | HEPB | L-2610-06 | 40 | S | S | S | S | S | S | S | S | S | — |
| 7 | TRA | ROTA | L-2610-07 | 180 | N | S | S | S | S | S | S | S | N | M1 |
| 8 | ING | BCG | L-2610-08 | 300 | S | S | S | S | S | S | S | S | S | — |
| 9 | AJU | ROTA | L-2610-09 | 80 | S | S | S | S | S | S | S | S | S | — |
| 10 | ING | PENT | L-2610-10 | 60 | S | S | S | S | S | S | S | S | S | — |
| 11 | ING | PENT | L-2610-11 | 40 | S | S | S | S | S | S | S | S | S | — |
| 12 | TRA | INFL | L-2610-12 | 200 | S | S | S | S | S | S | S | S | S | — |
| 13 | SAL | BCG | L-2610-13 | 150 | S | S | S | S | S | S | S | S | S | — |
| 14 | ING | IPV | L-2610-14 | 240 | S | S | S | S | S | S | S | S | S | — |
| 15 | DEV | VARI | L-2610-15 | 100 | S | S | S | S | S | S | S | S | S | — |
| 16 | ING | IPV | L-2610-16 | 300 | S | S | S | S | S | S | S | S | S | — |
| 17 | ING | NEUM | L-2610-17 | 200 | S | S | S | S | S | S | S | S | S | — |
| 18 | AJU | INFL | L-2610-18 | 180 | S | S | S | S | S | S | S | S | S | — |
| 19 | SAL | NEUM | L-2610-19 | 240 | S | S | S | S | S | S | S | S | S | — |
| 20 | DEV | NEUM | L-2610-20 | 40 | S | S | S | S | S | S | S | S | S | — |
| 21 | AJU | PENT | L-2610-21 | 80 | S | S | S | S | S | S | S | S | S | — |
| 22 | AJU | PENT | L-2610-22 | 180 | S | S | S | S | S | S | S | S | S | — |
| 23 | AJU | SPR | L-2610-23 | 120 | S | S | S | S | S | S | S | S | S | — |
| 24 | TRA | SPR | L-2610-24 | 40 | S | S | S | S | S | S | S | S | S | — |
| 25 | ING | HEPB | L-2610-25 | 100 | S | S | S | S | S | S | S | S | S | — |
| 26 | DEV | HEPB | L-2610-26 | 40 | S | S | S | S | S | S | S | S | S | — |
| 27 | ING | INFL | L-2610-27 | 100 | S | S | S | S | S | S | S | S | S | — |
| 28 | AJU | SPR | L-2610-28 | 240 | S | S | S | S | S | S | S | S | S | — |
| 29 | DEV | PENT | L-2610-29 | 120 | S | S | S | S | S | S | S | N | N | M8 |
| 30 | AJU | SPR | L-2610-30 | 60 | S | S | S | S | S | S | S | S | S | — |
| 31 | ING | NEUM | L-2610-31 | 80 | S | S | S | S | S | S | S | S | S | — |
| 32 | SAL | ROTA | L-2610-32 | 300 | S | S | S | S | S | S | S | S | S | — |
| 33 | DEV | DTA | L-2610-33 | 200 | S | S | S | S | S | S | S | S | S | — |
| 34 | SAL | NEUM | L-2610-34 | 240 | S | S | S | S | S | S | S | S | S | — |
| 35 | AJU | NEUM | L-2610-35 | 80 | S | S | S | S | S | S | S | S | S | — |
| 36 | ING | SPR | L-2610-36 | 150 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | DTA | L-2610-37 | 300 | S | S | S | S | S | S | S | S | S | — |
| 38 | TRA | BCG | L-2610-38 | 120 | S | S | S | S | S | S | S | S | S | — |
| 39 | ING | IPV | L-2610-39 | 100 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | INFL | L-2610-40 | 40 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-04 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 13/10/2026 | 6804 | NEUM | 180 | 180 | 0 | No aplica | Sí |
| 2 | 13/10/2026 | 6804 | VARI | 200 | 200 | 0 | No aplica | Sí |
| 3 | 13/10/2026 | 6804 | SPR | 50 | 50 | 0 | No aplica | Sí |
| 4 | 13/10/2026 | 6804 | INFL | 20 | 20 | 0 | No aplica | Sí |
| 5 | 13/10/2026 | 6804 | PENT | 80 | 80 | 0 | No aplica | Sí |
| 6 | 13/10/2026 | 6804 | ROTA | 40 | 40 | 0 | No aplica | Sí |
| 7 | 13/10/2026 | 6804 | PENT | 80 | 80 | 0 | No aplica | Sí |
| 8 | 13/10/2026 | 6804 | SPR | 30 | 30 | 0 | No aplica | Sí |
| 9 | 13/10/2026 | 6804 | BCG | 80 | 80 | 0 | No aplica | Sí |
| 10 | 13/10/2026 | 6804 | HEPB | 150 | 150 | 0 | No aplica | Sí |
| 11 | 13/10/2026 | 6804 | SPR | 100 | 100 | 0 | No aplica | Sí |
| 12 | 13/10/2026 | 6804 | HEPB | 50 | 50 | 0 | No aplica | Sí |
| 13 | 13/10/2026 | 6804 | BCG | 60 | 60 | 0 | No aplica | Sí |
| 14 | 13/10/2026 | 6804 | NEUM | 100 | 100 | 0 | No aplica | Sí |
| 15 | 13/10/2026 | 6804 | BCG | 40 | 40 | 0 | No aplica | Sí |
| 16 | 13/10/2026 | 6804 | HEPB | 150 | 150 | 0 | No aplica | Sí |
| 17 | 13/10/2026 | 6804 | ROTA | 100 | 100 | 0 | No aplica | Sí |
| 18 | 13/10/2026 | 6804 | ROTA | 200 | 220 | 20 | Sí | No |
| 19 | 13/10/2026 | 6804 | IPV | 200 | 200 | 0 | No aplica | Sí |
| 20 | 13/10/2026 | 6804 | SPR | 80 | 80 | 0 | No aplica | Sí |
| 21 | 13/10/2026 | 6804 | IPV | 30 | 30 | 0 | No aplica | Sí |
| 22 | 13/10/2026 | 6804 | PENT | 200 | 200 | 0 | No aplica | Sí |
| 23 | 13/10/2026 | 6804 | NEUM | 60 | 80 | 20 | Sí | No |
| 24 | 13/10/2026 | 6804 | SPR | 80 | 80 | 0 | No aplica | Sí |
| 25 | 13/10/2026 | 6804 | NEUM | 30 | 30 | 0 | No aplica | Sí |

Cierre: 23 entregas concordantes ÷ 25 × 100 = **92.00 %**.

---

### Bloque 9 · TRAB-05 · Pretest (proceso manual) · 12/08/2026

Documentos auditados: 40 · Conformes: 18 · RSD: 45.00 % · Entregas conciliadas: 25 · Concordantes: 21 · CPE: 84.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | SAL | SPR | L-2608-01 | 60 | S | S | S | S | S | S | S | S | S | — |
| 2 | DEV | ROTA | L-2608-02 | 180 | S | S | S | S | S | S | S | S | S | — |
| 3 | ING | DTA | L-2608-03 | 150 | S | S | S | S | S | S | S | S | S | — |
| 4 | ING | HEPB | L-2608-04 | 20 | S | S | S | S | S | S | N | S | N | M7 |
| 5 | DEV | INFL | L-2608-05 | 20 | S | S | S | S | S | S | N | S | N | M7 |
| 6 | TRA | SPR | L-2608-06 | 180 | S | S | S | S | S | S | S | S | S | — |
| 7 | SAL | DTA | L-2608-07 | 60 | S | S | S | S | S | N | S | S | N | M6 |
| 8 | TRA | PENT | L-2608-08 | 150 | S | S | S | S | S | S | S | S | S | — |
| 9 | DEV | DTA | L-2608-09 | 150 | S | S | S | S | N | S | S | S | N | M5 |
| 10 | ING | ROTA | L-2608-10 | 300 | S | S | S | S | S | S | S | S | S | — |
| 11 | ING | VARI | L-2608-11 | 200 | S | N | S | S | S | S | S | S | N | M2 |
| 12 | DEV | SPR | L-2608-12 | 60 | S | N | S | S | S | S | S | S | N | M2 |
| 13 | AJU | DTA | L-2608-13 | 200 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | HEPB | L-2608-14 | 200 | S | S | S | S | S | S | S | S | S | — |
| 15 | TRA | ROTA | L-2608-15 | 150 | N | S | S | S | S | S | S | S | N | M1 |
| 16 | TRA | NEUM | L-2608-16 | 240 | S | S | S | S | N | S | S | S | N | M5 |
| 17 | AJU | BCG | L-2608-17 | 240 | S | S | S | S | S | S | N | S | N | M7 |
| 18 | SAL | SPR | L-2608-18 | 200 | S | S | S | S | S | N | S | S | N | M6 |
| 19 | TRA | VARI | L-2608-19 | 180 | S | N | S | S | S | S | S | S | N | M2 |
| 20 | SAL | IPV | L-2608-20 | 20 | S | N | S | S | S | S | S | S | N | M2 |
| 21 | SAL | BCG | L-2608-21 | 60 | S | S | S | S | S | S | N | S | N | M7 |
| 22 | ING | SPR | L-2608-22 | 20 | S | S | S | S | S | S | S | S | S | — |
| 23 | AJU | DTA | L-2608-23 | 150 | S | S | S | S | S | S | S | S | S | — |
| 24 | ING | PENT | L-2608-24 | 80 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | INFL | L-2608-25 | 80 | S | S | S | S | N | S | S | S | N | M5 |
| 26 | DEV | IPV | L-2608-26 | 180 | S | S | S | S | S | N | S | S | N | M6 |
| 27 | AJU | NEUM | L-2608-27 | 240 | N | S | S | S | S | S | S | S | N | M1 |
| 28 | TRA | INFL | L-2608-28 | 80 | S | S | S | S | S | N | S | S | N | M6 |
| 29 | SAL | ROTA | L-2608-29 | 120 | S | S | S | S | S | S | S | N | N | M8 |
| 30 | AJU | IPV | L-2608-30 | 40 | S | S | S | S | S | S | S | S | S | — |
| 31 | SAL | PENT | L-2608-31 | 300 | S | S | S | N | S | S | S | S | N | M4 |
| 32 | AJU | INFL | L-2608-32 | 150 | S | S | S | S | S | S | S | S | S | — |
| 33 | AJU | HEPB | L-2608-33 | 240 | S | S | S | S | S | S | S | S | S | — |
| 34 | AJU | INFL | L-2608-34 | 200 | S | S | S | S | N | S | S | S | N | M5 |
| 35 | ING | SPR | L-2608-35 | 150 | S | S | S | S | S | S | S | S | S | — |
| 36 | ING | VARI | L-2608-36 | 300 | S | S | S | S | N | S | S | S | N | M5 |
| 37 | DEV | INFL | L-2608-37 | 240 | S | S | S | S | S | S | S | S | S | — |
| 38 | DEV | BCG | L-2608-38 | 40 | S | N | S | S | S | S | S | S | N | M2 |
| 39 | SAL | NEUM | L-2608-39 | 150 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | INFL | L-2608-40 | 240 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-05 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 12/08/2026 | 4132 | PENT | 120 | 120 | 0 | No aplica | Sí |
| 2 | 12/08/2026 | 4132 | HEPB | 150 | 140 | -10 | Sí | No |
| 3 | 12/08/2026 | 4132 | SPR | 60 | 60 | 0 | No aplica | Sí |
| 4 | 12/08/2026 | 4132 | DTA | 50 | 50 | 0 | No aplica | Sí |
| 5 | 12/08/2026 | 4132 | BCG | 40 | 40 | 0 | No aplica | Sí |
| 6 | 12/08/2026 | 4132 | DTA | 100 | 100 | 0 | No aplica | Sí |
| 7 | 12/08/2026 | 4132 | BCG | 20 | 20 | 0 | No aplica | Sí |
| 8 | 12/08/2026 | 4132 | PENT | 40 | 30 | -10 | Sí | No |
| 9 | 12/08/2026 | 4132 | NEUM | 80 | 80 | 0 | No aplica | Sí |
| 10 | 12/08/2026 | 4132 | BCG | 180 | 180 | 0 | No aplica | Sí |
| 11 | 12/08/2026 | 4132 | BCG | 60 | 60 | 0 | No aplica | Sí |
| 12 | 12/08/2026 | 4132 | PENT | 40 | 40 | 0 | No aplica | Sí |
| 13 | 12/08/2026 | 4132 | ROTA | 180 | 180 | 0 | No aplica | Sí |
| 14 | 12/08/2026 | 4132 | NEUM | 20 | 20 | 0 | No aplica | Sí |
| 15 | 12/08/2026 | 4132 | NEUM | 120 | 100 | -20 | Sí | No |
| 16 | 12/08/2026 | 4132 | IPV | 30 | 30 | 0 | No aplica | Sí |
| 17 | 12/08/2026 | 4132 | SPR | 20 | 20 | 0 | No aplica | Sí |
| 18 | 12/08/2026 | 4132 | BCG | 40 | 40 | 0 | No aplica | Sí |
| 19 | 12/08/2026 | 4132 | DTA | 100 | 100 | 0 | No aplica | Sí |
| 20 | 12/08/2026 | 4132 | INFL | 60 | 60 | 0 | No aplica | Sí |
| 21 | 12/08/2026 | 4132 | SPR | 100 | 100 | 0 | No aplica | Sí |
| 22 | 12/08/2026 | 4132 | HEPB | 180 | 180 | 0 | No aplica | Sí |
| 23 | 12/08/2026 | 4132 | NEUM | 200 | 200 | 0 | No aplica | Sí |
| 24 | 12/08/2026 | 4132 | INFL | 40 | 50 | 10 | Sí | No |
| 25 | 12/08/2026 | 4132 | ROTA | 50 | 50 | 0 | No aplica | Sí |

Cierre: 21 entregas concordantes ÷ 25 × 100 = **84.00 %**.

---

### Bloque 10 · TRAB-05 · Postest (Sistema SIVAC) · 14/10/2026

Documentos auditados: 40 · Conformes: 39 · RSD: 97.50 % · Entregas conciliadas: 25 · Concordantes: 22 · CPE: 88.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | DEV | IPV | L-2610-01 | 240 | S | S | S | S | S | S | S | S | S | — |
| 2 | AJU | INFL | L-2610-02 | 20 | S | S | S | S | S | S | S | S | S | — |
| 3 | TRA | DTA | L-2610-03 | 60 | S | S | S | S | S | S | S | S | S | — |
| 4 | DEV | NEUM | L-2610-04 | 20 | S | S | S | S | S | S | S | S | S | — |
| 5 | TRA | SPR | L-2610-05 | 60 | S | S | S | S | S | S | S | S | S | — |
| 6 | TRA | DTA | L-2610-06 | 60 | S | S | S | S | S | S | S | S | S | — |
| 7 | AJU | PENT | L-2610-07 | 300 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | NEUM | L-2610-08 | 300 | S | S | S | S | S | S | S | S | S | — |
| 9 | ING | IPV | L-2610-09 | 200 | S | S | S | S | S | S | S | S | S | — |
| 10 | DEV | SPR | L-2610-10 | 100 | S | S | S | S | S | S | S | S | S | — |
| 11 | TRA | PENT | L-2610-11 | 180 | S | S | S | S | S | S | S | S | S | — |
| 12 | SAL | HEPB | L-2610-12 | 200 | S | S | S | S | S | S | S | S | S | — |
| 13 | DEV | VARI | L-2610-13 | 80 | S | S | S | S | S | S | S | S | S | — |
| 14 | ING | BCG | L-2610-14 | 200 | S | S | S | S | S | S | S | S | S | — |
| 15 | ING | IPV | L-2610-15 | 40 | S | S | S | S | S | S | S | S | S | — |
| 16 | TRA | DTA | L-2610-16 | 180 | S | S | S | S | S | S | S | S | S | — |
| 17 | TRA | PENT | L-2610-17 | 240 | S | S | S | S | S | S | S | S | S | — |
| 18 | SAL | ROTA | L-2610-18 | 200 | S | S | S | S | S | S | N | S | N | M7 |
| 19 | SAL | DTA | L-2610-19 | 300 | S | S | S | S | S | S | S | S | S | — |
| 20 | ING | VARI | L-2610-20 | 180 | S | S | S | S | S | S | S | S | S | — |
| 21 | DEV | VARI | L-2610-21 | 240 | S | S | S | S | S | S | S | S | S | — |
| 22 | DEV | VARI | L-2610-22 | 180 | S | S | S | S | S | S | S | S | S | — |
| 23 | TRA | IPV | L-2610-23 | 240 | S | S | S | S | S | S | S | S | S | — |
| 24 | DEV | VARI | L-2610-24 | 20 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | DTA | L-2610-25 | 60 | S | S | S | S | S | S | S | S | S | — |
| 26 | ING | SPR | L-2610-26 | 60 | S | S | S | S | S | S | S | S | S | — |
| 27 | ING | PENT | L-2610-27 | 100 | S | S | S | S | S | S | S | S | S | — |
| 28 | SAL | ROTA | L-2610-28 | 100 | S | S | S | S | S | S | S | S | S | — |
| 29 | AJU | PENT | L-2610-29 | 20 | S | S | S | S | S | S | S | S | S | — |
| 30 | ING | ROTA | L-2610-30 | 300 | S | S | S | S | S | S | S | S | S | — |
| 31 | TRA | SPR | L-2610-31 | 40 | S | S | S | S | S | S | S | S | S | — |
| 32 | ING | NEUM | L-2610-32 | 200 | S | S | S | S | S | S | S | S | S | — |
| 33 | AJU | PENT | L-2610-33 | 100 | S | S | S | S | S | S | S | S | S | — |
| 34 | DEV | PENT | L-2610-34 | 20 | S | S | S | S | S | S | S | S | S | — |
| 35 | AJU | INFL | L-2610-35 | 40 | S | S | S | S | S | S | S | S | S | — |
| 36 | AJU | PENT | L-2610-36 | 240 | S | S | S | S | S | S | S | S | S | — |
| 37 | ING | NEUM | L-2610-37 | 100 | S | S | S | S | S | S | S | S | S | — |
| 38 | DEV | NEUM | L-2610-38 | 300 | S | S | S | S | S | S | S | S | S | — |
| 39 | ING | SPR | L-2610-39 | 20 | S | S | S | S | S | S | S | S | S | — |
| 40 | TRA | VARI | L-2610-40 | 200 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-05 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 14/10/2026 | 4132 | SPR | 60 | 60 | 0 | No aplica | Sí |
| 2 | 14/10/2026 | 4132 | SPR | 50 | 70 | 20 | Sí | No |
| 3 | 14/10/2026 | 4132 | IPV | 40 | 40 | 0 | No aplica | Sí |
| 4 | 14/10/2026 | 4132 | IPV | 80 | 80 | 0 | No aplica | Sí |
| 5 | 14/10/2026 | 4132 | INFL | 180 | 180 | 0 | No aplica | Sí |
| 6 | 14/10/2026 | 4132 | IPV | 40 | 40 | 0 | No aplica | Sí |
| 7 | 14/10/2026 | 4132 | HEPB | 30 | 30 | 0 | No aplica | Sí |
| 8 | 14/10/2026 | 4132 | BCG | 60 | 60 | 0 | No aplica | Sí |
| 9 | 14/10/2026 | 4132 | IPV | 40 | 40 | 0 | No aplica | Sí |
| 10 | 14/10/2026 | 4132 | PENT | 50 | 50 | 0 | No aplica | Sí |
| 11 | 14/10/2026 | 4132 | SPR | 50 | 50 | 0 | No aplica | Sí |
| 12 | 14/10/2026 | 4132 | HEPB | 80 | 80 | 0 | No aplica | Sí |
| 13 | 14/10/2026 | 4132 | INFL | 20 | 20 | 0 | No aplica | Sí |
| 14 | 14/10/2026 | 4132 | IPV | 20 | 20 | 0 | No aplica | Sí |
| 15 | 14/10/2026 | 4132 | IPV | 180 | 180 | 0 | No aplica | Sí |
| 16 | 14/10/2026 | 4132 | NEUM | 80 | 80 | 0 | No aplica | Sí |
| 17 | 14/10/2026 | 4132 | BCG | 120 | 120 | 0 | No aplica | Sí |
| 18 | 14/10/2026 | 4132 | VARI | 120 | 120 | 0 | No aplica | Sí |
| 19 | 14/10/2026 | 4132 | PENT | 100 | 110 | 10 | Sí | No |
| 20 | 14/10/2026 | 4132 | DTA | 180 | 180 | 0 | No aplica | Sí |
| 21 | 14/10/2026 | 4132 | IPV | 50 | 45 | -5 | Sí | No |
| 22 | 14/10/2026 | 4132 | ROTA | 20 | 20 | 0 | No aplica | Sí |
| 23 | 14/10/2026 | 4132 | SPR | 180 | 180 | 0 | No aplica | Sí |
| 24 | 14/10/2026 | 4132 | IPV | 50 | 50 | 0 | No aplica | Sí |
| 25 | 14/10/2026 | 4132 | VARI | 60 | 60 | 0 | No aplica | Sí |

Cierre: 22 entregas concordantes ÷ 25 × 100 = **88.00 %**.

---

### Bloque 11 · TRAB-06 · Pretest (proceso manual) · 12/08/2026

Documentos auditados: 40 · Conformes: 21 · RSD: 52.50 % · Entregas conciliadas: 25 · Concordantes: 18 · CPE: 72.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | ING | DTA | L-2608-01 | 200 | N | S | S | S | S | S | S | S | N | M1 |
| 2 | ING | PENT | L-2608-02 | 180 | S | S | S | S | S | S | S | S | S | — |
| 3 | DEV | SPR | L-2608-03 | 20 | S | S | S | S | S | S | N | S | N | M7 |
| 4 | TRA | ROTA | L-2608-04 | 80 | S | S | S | S | S | S | S | S | S | — |
| 5 | ING | NEUM | L-2608-05 | 300 | S | S | S | S | S | S | S | S | S | — |
| 6 | ING | HEPB | L-2608-06 | 200 | S | S | S | S | S | S | N | S | N | M7 |
| 7 | SAL | ROTA | L-2608-07 | 100 | S | S | S | S | S | S | N | S | N | M7 |
| 8 | ING | HEPB | L-2608-08 | 240 | S | S | S | S | S | S | S | S | S | — |
| 9 | DEV | DTA | L-2608-09 | 40 | S | S | S | S | S | S | S | S | S | — |
| 10 | DEV | DTA | L-2608-10 | 300 | S | S | S | S | S | S | S | S | S | — |
| 11 | TRA | INFL | L-2608-11 | 180 | S | S | N | S | S | S | S | S | N | M3 |
| 12 | AJU | ROTA | L-2608-12 | 40 | S | S | S | S | S | S | S | S | S | — |
| 13 | SAL | VARI | L-2608-13 | 60 | S | S | S | S | S | S | S | S | S | — |
| 14 | DEV | BCG | L-2608-14 | 300 | S | S | S | S | S | S | S | S | S | — |
| 15 | ING | INFL | L-2608-15 | 240 | S | S | S | S | S | S | N | S | N | M7 |
| 16 | DEV | IPV | L-2608-16 | 300 | N | S | S | S | S | S | S | S | N | M1 |
| 17 | DEV | IPV | L-2608-17 | 200 | S | S | S | S | S | S | S | S | S | — |
| 18 | DEV | VARI | L-2608-18 | 150 | S | S | S | S | S | S | S | S | S | — |
| 19 | AJU | BCG | L-2608-19 | 120 | S | S | S | S | S | S | S | S | S | — |
| 20 | DEV | BCG | L-2608-20 | 80 | S | S | N | S | S | S | S | S | N | M3 |
| 21 | ING | HEPB | L-2608-21 | 100 | S | S | S | S | S | S | S | S | S | — |
| 22 | SAL | BCG | L-2608-22 | 150 | S | S | S | S | S | S | N | S | N | M7 |
| 23 | SAL | VARI | L-2608-23 | 20 | S | S | S | S | S | S | S | S | S | — |
| 24 | ING | SPR | L-2608-24 | 300 | S | S | S | S | S | S | S | S | S | — |
| 25 | SAL | SPR | L-2608-25 | 40 | S | N | S | S | S | S | S | S | N | M2 |
| 26 | AJU | NEUM | L-2608-26 | 300 | S | S | S | S | S | S | N | S | N | M7 |
| 27 | AJU | DTA | L-2608-27 | 200 | S | S | S | S | N | S | S | S | N | M5 |
| 28 | DEV | VARI | L-2608-28 | 60 | S | S | S | S | N | S | S | S | N | M5 |
| 29 | AJU | SPR | L-2608-29 | 200 | S | S | S | S | S | S | S | S | S | — |
| 30 | AJU | HEPB | L-2608-30 | 40 | S | S | S | S | S | S | S | S | S | — |
| 31 | ING | PENT | L-2608-31 | 180 | S | S | N | S | S | S | S | S | N | M3 |
| 32 | AJU | NEUM | L-2608-32 | 120 | S | S | S | S | S | S | S | S | S | — |
| 33 | TRA | BCG | L-2608-33 | 300 | S | N | S | S | S | S | S | S | N | M2 |
| 34 | TRA | PENT | L-2608-34 | 300 | S | N | S | S | S | S | S | S | N | M2 |
| 35 | ING | DTA | L-2608-35 | 20 | S | S | S | S | S | S | S | N | N | M8 |
| 36 | SAL | HEPB | L-2608-36 | 20 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | BCG | L-2608-37 | 60 | S | S | S | S | S | S | S | S | S | — |
| 38 | AJU | ROTA | L-2608-38 | 300 | S | S | S | S | S | S | S | S | S | — |
| 39 | AJU | IPV | L-2608-39 | 100 | S | S | S | S | S | S | S | N | N | M8 |
| 40 | AJU | ROTA | L-2608-40 | 200 | S | S | S | N | S | S | S | S | N | M4 |

**Entregas conciliadas — TRAB-06 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 12/08/2026 | 4158 | ROTA | 30 | 30 | 0 | No aplica | Sí |
| 2 | 12/08/2026 | 4158 | VARI | 200 | 200 | 0 | No aplica | Sí |
| 3 | 12/08/2026 | 4158 | HEPB | 60 | 60 | 0 | No aplica | Sí |
| 4 | 12/08/2026 | 4158 | PENT | 100 | 110 | 10 | Sí | No |
| 5 | 12/08/2026 | 4158 | HEPB | 120 | 120 | 0 | No aplica | Sí |
| 6 | 12/08/2026 | 4158 | IPV | 20 | 20 | 0 | No aplica | Sí |
| 7 | 12/08/2026 | 4158 | NEUM | 100 | 100 | 0 | No aplica | Sí |
| 8 | 12/08/2026 | 4158 | SPR | 20 | 20 | 0 | No aplica | Sí |
| 9 | 12/08/2026 | 4158 | BCG | 80 | 80 | 0 | No aplica | Sí |
| 10 | 12/08/2026 | 4158 | SPR | 60 | 70 | 10 | Sí | No |
| 11 | 12/08/2026 | 4158 | SPR | 30 | 30 | 0 | No aplica | Sí |
| 12 | 12/08/2026 | 4158 | SPR | 100 | 105 | 5 | Sí | No |
| 13 | 12/08/2026 | 4158 | IPV | 180 | 180 | 0 | No aplica | Sí |
| 14 | 12/08/2026 | 4158 | BCG | 200 | 200 | 0 | No aplica | Sí |
| 15 | 12/08/2026 | 4158 | BCG | 100 | 95 | -5 | Sí | No |
| 16 | 12/08/2026 | 4158 | PENT | 80 | 80 | 0 | No aplica | Sí |
| 17 | 12/08/2026 | 4158 | VARI | 80 | 80 | 0 | No aplica | Sí |
| 18 | 12/08/2026 | 4158 | PENT | 100 | 100 | 0 | No aplica | Sí |
| 19 | 12/08/2026 | 4158 | NEUM | 200 | 200 | 0 | No aplica | Sí |
| 20 | 12/08/2026 | 4158 | DTA | 180 | 190 | 10 | Sí | No |
| 21 | 12/08/2026 | 4158 | PENT | 20 | 25 | 5 | Sí | No |
| 22 | 12/08/2026 | 4158 | INFL | 20 | 20 | 0 | No aplica | Sí |
| 23 | 12/08/2026 | 4158 | INFL | 100 | 80 | -20 | Sí | No |
| 24 | 12/08/2026 | 4158 | NEUM | 200 | 200 | 0 | No aplica | Sí |
| 25 | 12/08/2026 | 4158 | SPR | 30 | 30 | 0 | No aplica | Sí |

Cierre: 18 entregas concordantes ÷ 25 × 100 = **72.00 %**.

---

### Bloque 12 · TRAB-06 · Postest (Sistema SIVAC) · 14/10/2026

Documentos auditados: 40 · Conformes: 38 · RSD: 95.00 % · Entregas conciliadas: 25 · Concordantes: 20 · CPE: 80.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | SAL | INFL | L-2610-01 | 20 | S | S | S | S | S | S | S | S | S | — |
| 2 | ING | NEUM | L-2610-02 | 80 | S | S | S | S | S | S | S | S | S | — |
| 3 | TRA | NEUM | L-2610-03 | 150 | S | S | S | S | S | S | S | S | S | — |
| 4 | ING | PENT | L-2610-04 | 20 | S | S | S | S | S | S | S | S | S | — |
| 5 | ING | VARI | L-2610-05 | 120 | S | S | S | S | S | S | S | S | S | — |
| 6 | SAL | VARI | L-2610-06 | 240 | S | S | S | S | S | S | S | S | S | — |
| 7 | ING | SPR | L-2610-07 | 240 | S | S | S | S | S | S | S | S | S | — |
| 8 | ING | IPV | L-2610-08 | 240 | S | S | S | S | S | S | S | S | S | — |
| 9 | TRA | HEPB | L-2610-09 | 120 | S | S | S | S | S | S | S | S | S | — |
| 10 | ING | ROTA | L-2610-10 | 40 | S | S | S | S | S | S | S | S | S | — |
| 11 | AJU | ROTA | L-2610-11 | 150 | S | S | S | S | S | S | S | S | S | — |
| 12 | AJU | NEUM | L-2610-12 | 300 | S | S | S | S | S | S | S | S | S | — |
| 13 | TRA | DTA | L-2610-13 | 40 | S | S | S | S | S | S | S | S | S | — |
| 14 | TRA | HEPB | L-2610-14 | 240 | S | S | S | S | S | S | S | S | S | — |
| 15 | SAL | IPV | L-2610-15 | 80 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | PENT | L-2610-16 | 200 | S | S | S | S | S | S | S | S | S | — |
| 17 | ING | NEUM | L-2610-17 | 100 | S | S | S | S | S | S | S | S | S | — |
| 18 | SAL | HEPB | L-2610-18 | 200 | S | S | S | S | S | S | S | S | S | — |
| 19 | DEV | ROTA | L-2610-19 | 240 | S | S | S | S | S | S | S | S | S | — |
| 20 | TRA | HEPB | L-2610-20 | 60 | S | S | S | S | S | S | S | S | S | — |
| 21 | ING | ROTA | L-2610-21 | 40 | S | S | S | S | S | S | S | S | S | — |
| 22 | DEV | BCG | L-2610-22 | 300 | S | S | S | S | S | S | S | S | S | — |
| 23 | TRA | BCG | L-2610-23 | 300 | S | S | S | S | S | S | S | S | S | — |
| 24 | AJU | HEPB | L-2610-24 | 20 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | VARI | L-2610-25 | 200 | S | S | S | S | S | S | S | S | S | — |
| 26 | TRA | BCG | L-2610-26 | 120 | S | S | S | S | S | S | S | S | S | — |
| 27 | DEV | ROTA | L-2610-27 | 80 | S | S | S | S | S | N | S | S | N | M6 |
| 28 | SAL | BCG | L-2610-28 | 60 | S | S | S | S | S | S | S | N | N | M8 |
| 29 | SAL | DTA | L-2610-29 | 100 | S | S | S | S | S | S | S | S | S | — |
| 30 | ING | VARI | L-2610-30 | 180 | S | S | S | S | S | S | S | S | S | — |
| 31 | AJU | PENT | L-2610-31 | 200 | S | S | S | S | S | S | S | S | S | — |
| 32 | AJU | PENT | L-2610-32 | 60 | S | S | S | S | S | S | S | S | S | — |
| 33 | DEV | PENT | L-2610-33 | 20 | S | S | S | S | S | S | S | S | S | — |
| 34 | DEV | DTA | L-2610-34 | 180 | S | S | S | S | S | S | S | S | S | — |
| 35 | DEV | BCG | L-2610-35 | 60 | S | S | S | S | S | S | S | S | S | — |
| 36 | DEV | BCG | L-2610-36 | 300 | S | S | S | S | S | S | S | S | S | — |
| 37 | ING | DTA | L-2610-37 | 180 | S | S | S | S | S | S | S | S | S | — |
| 38 | SAL | HEPB | L-2610-38 | 300 | S | S | S | S | S | S | S | S | S | — |
| 39 | SAL | HEPB | L-2610-39 | 20 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | PENT | L-2610-40 | 20 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-06 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 14/10/2026 | 4158 | VARI | 60 | 60 | 0 | No aplica | Sí |
| 2 | 14/10/2026 | 4158 | PENT | 80 | 80 | 0 | No aplica | Sí |
| 3 | 14/10/2026 | 4158 | NEUM | 120 | 120 | 0 | No aplica | Sí |
| 4 | 14/10/2026 | 4158 | SPR | 60 | 60 | 0 | No aplica | Sí |
| 5 | 14/10/2026 | 4158 | BCG | 60 | 60 | 0 | No aplica | Sí |
| 6 | 14/10/2026 | 4158 | ROTA | 60 | 60 | 0 | No aplica | Sí |
| 7 | 14/10/2026 | 4158 | ROTA | 120 | 120 | 0 | No aplica | Sí |
| 8 | 14/10/2026 | 4158 | BCG | 60 | 60 | 0 | No aplica | Sí |
| 9 | 14/10/2026 | 4158 | PENT | 30 | 30 | 0 | No aplica | Sí |
| 10 | 14/10/2026 | 4158 | ROTA | 180 | 180 | 0 | No aplica | Sí |
| 11 | 14/10/2026 | 4158 | NEUM | 150 | 150 | 0 | No aplica | Sí |
| 12 | 14/10/2026 | 4158 | ROTA | 200 | 180 | -20 | Sí | No |
| 13 | 14/10/2026 | 4158 | NEUM | 100 | 105 | 5 | Sí | No |
| 14 | 14/10/2026 | 4158 | NEUM | 30 | 30 | 0 | No aplica | Sí |
| 15 | 14/10/2026 | 4158 | DTA | 120 | 120 | 0 | No aplica | Sí |
| 16 | 14/10/2026 | 4158 | BCG | 120 | 120 | 0 | No aplica | Sí |
| 17 | 14/10/2026 | 4158 | INFL | 80 | 75 | -5 | Sí | No |
| 18 | 14/10/2026 | 4158 | SPR | 120 | 120 | 0 | No aplica | Sí |
| 19 | 14/10/2026 | 4158 | NEUM | 30 | 20 | -10 | Sí | No |
| 20 | 14/10/2026 | 4158 | SPR | 200 | 200 | 0 | No aplica | Sí |
| 21 | 14/10/2026 | 4158 | VARI | 50 | 50 | 0 | No aplica | Sí |
| 22 | 14/10/2026 | 4158 | VARI | 180 | 180 | 0 | No aplica | Sí |
| 23 | 14/10/2026 | 4158 | DTA | 120 | 120 | 0 | No aplica | Sí |
| 24 | 14/10/2026 | 4158 | VARI | 60 | 55 | -5 | Sí | No |
| 25 | 14/10/2026 | 4158 | ROTA | 40 | 40 | 0 | No aplica | Sí |

Cierre: 20 entregas concordantes ÷ 25 × 100 = **80.00 %**.

---

### Bloque 13 · TRAB-07 · Pretest (proceso manual) · 13/08/2026

Documentos auditados: 40 · Conformes: 25 · RSD: 62.50 % · Entregas conciliadas: 25 · Concordantes: 20 · CPE: 80.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | SAL | NEUM | L-2608-01 | 200 | S | S | S | S | S | S | S | S | S | — |
| 2 | DEV | IPV | L-2608-02 | 100 | S | S | S | S | S | S | N | S | N | M7 |
| 3 | AJU | ROTA | L-2608-03 | 240 | S | S | S | N | S | S | S | S | N | M4 |
| 4 | ING | HEPB | L-2608-04 | 100 | S | S | S | S | N | S | S | S | N | M5 |
| 5 | SAL | INFL | L-2608-05 | 40 | S | S | S | S | S | S | S | N | N | M8 |
| 6 | AJU | NEUM | L-2608-06 | 240 | S | S | S | N | S | S | S | S | N | M4 |
| 7 | TRA | ROTA | L-2608-07 | 120 | S | S | S | S | S | S | S | N | N | M8 |
| 8 | TRA | SPR | L-2608-08 | 240 | S | S | S | S | S | S | S | S | S | — |
| 9 | TRA | SPR | L-2608-09 | 120 | S | S | S | S | S | S | S | S | S | — |
| 10 | ING | DTA | L-2608-10 | 180 | S | S | S | S | S | S | S | S | S | — |
| 11 | DEV | SPR | L-2608-11 | 80 | S | S | S | S | S | S | S | S | S | — |
| 12 | SAL | VARI | L-2608-12 | 200 | S | S | S | S | S | S | S | S | S | — |
| 13 | ING | NEUM | L-2608-13 | 100 | S | S | S | S | S | S | S | S | S | — |
| 14 | AJU | IPV | L-2608-14 | 240 | S | S | S | S | S | S | S | S | S | — |
| 15 | TRA | DTA | L-2608-15 | 60 | S | S | S | S | S | S | S | S | S | — |
| 16 | ING | SPR | L-2608-16 | 80 | S | S | S | S | S | S | S | S | S | — |
| 17 | AJU | BCG | L-2608-17 | 300 | N | S | S | S | S | S | S | S | N | M1 |
| 18 | SAL | IPV | L-2608-18 | 180 | S | S | S | S | S | S | S | N | N | M8 |
| 19 | AJU | HEPB | L-2608-19 | 300 | S | S | S | S | S | S | S | S | S | — |
| 20 | SAL | BCG | L-2608-20 | 300 | S | S | S | S | S | S | S | S | S | — |
| 21 | SAL | SPR | L-2608-21 | 150 | S | S | N | S | S | S | S | S | N | M3 |
| 22 | DEV | ROTA | L-2608-22 | 80 | S | S | S | S | S | S | S | S | S | — |
| 23 | AJU | PENT | L-2608-23 | 40 | S | S | S | S | S | S | S | S | S | — |
| 24 | TRA | SPR | L-2608-24 | 120 | S | S | S | S | S | S | S | S | S | — |
| 25 | ING | SPR | L-2608-25 | 180 | S | S | S | S | S | S | S | S | S | — |
| 26 | AJU | SPR | L-2608-26 | 240 | N | S | S | S | S | S | S | S | N | M1 |
| 27 | DEV | ROTA | L-2608-27 | 20 | S | S | S | S | S | S | S | S | S | — |
| 28 | TRA | DTA | L-2608-28 | 100 | S | S | S | S | S | S | S | N | N | M8 |
| 29 | TRA | PENT | L-2608-29 | 240 | S | S | S | S | S | S | S | S | S | — |
| 30 | TRA | IPV | L-2608-30 | 120 | S | S | S | S | N | S | S | S | N | M5 |
| 31 | ING | INFL | L-2608-31 | 240 | S | S | S | S | S | S | S | S | S | — |
| 32 | SAL | BCG | L-2608-32 | 200 | S | S | S | N | S | S | S | S | N | M4 |
| 33 | ING | IPV | L-2608-33 | 300 | S | S | S | N | S | S | S | S | N | M4 |
| 34 | TRA | HEPB | L-2608-34 | 20 | S | S | S | S | S | S | S | S | S | — |
| 35 | AJU | DTA | L-2608-35 | 300 | S | S | S | S | S | S | S | S | S | — |
| 36 | TRA | PENT | L-2608-36 | 40 | S | S | S | S | S | S | S | S | S | — |
| 37 | ING | PENT | L-2608-37 | 120 | S | S | S | S | S | S | S | S | S | — |
| 38 | AJU | HEPB | L-2608-38 | 80 | S | S | S | N | S | S | S | S | N | M4 |
| 39 | AJU | NEUM | L-2608-39 | 120 | S | S | S | S | S | S | S | S | S | — |
| 40 | DEV | SPR | L-2608-40 | 120 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-07 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 13/08/2026 | 4160 | BCG | 30 | 30 | 0 | No aplica | Sí |
| 2 | 13/08/2026 | 4160 | PENT | 150 | 150 | 0 | No aplica | Sí |
| 3 | 13/08/2026 | 4160 | PENT | 100 | 90 | -10 | Sí | No |
| 4 | 13/08/2026 | 4160 | PENT | 30 | 30 | 0 | No aplica | Sí |
| 5 | 13/08/2026 | 4160 | PENT | 180 | 180 | 0 | No aplica | Sí |
| 6 | 13/08/2026 | 4160 | BCG | 30 | 25 | -5 | Sí | No |
| 7 | 13/08/2026 | 4160 | VARI | 60 | 50 | -10 | Sí | No |
| 8 | 13/08/2026 | 4160 | VARI | 40 | 40 | 0 | No aplica | Sí |
| 9 | 13/08/2026 | 4160 | NEUM | 60 | 55 | -5 | Sí | No |
| 10 | 13/08/2026 | 4160 | PENT | 150 | 150 | 0 | No aplica | Sí |
| 11 | 13/08/2026 | 4160 | HEPB | 40 | 40 | 0 | No aplica | Sí |
| 12 | 13/08/2026 | 4160 | DTA | 120 | 120 | 0 | No aplica | Sí |
| 13 | 13/08/2026 | 4160 | INFL | 20 | 20 | 0 | No aplica | Sí |
| 14 | 13/08/2026 | 4160 | VARI | 80 | 85 | 5 | Sí | No |
| 15 | 13/08/2026 | 4160 | INFL | 40 | 40 | 0 | No aplica | Sí |
| 16 | 13/08/2026 | 4160 | DTA | 150 | 150 | 0 | No aplica | Sí |
| 17 | 13/08/2026 | 4160 | PENT | 80 | 80 | 0 | No aplica | Sí |
| 18 | 13/08/2026 | 4160 | ROTA | 100 | 100 | 0 | No aplica | Sí |
| 19 | 13/08/2026 | 4160 | NEUM | 200 | 200 | 0 | No aplica | Sí |
| 20 | 13/08/2026 | 4160 | HEPB | 40 | 40 | 0 | No aplica | Sí |
| 21 | 13/08/2026 | 4160 | BCG | 60 | 60 | 0 | No aplica | Sí |
| 22 | 13/08/2026 | 4160 | DTA | 20 | 20 | 0 | No aplica | Sí |
| 23 | 13/08/2026 | 4160 | INFL | 200 | 200 | 0 | No aplica | Sí |
| 24 | 13/08/2026 | 4160 | INFL | 20 | 20 | 0 | No aplica | Sí |
| 25 | 13/08/2026 | 4160 | IPV | 150 | 150 | 0 | No aplica | Sí |

Cierre: 20 entregas concordantes ÷ 25 × 100 = **80.00 %**.

---

### Bloque 14 · TRAB-07 · Postest (Sistema SIVAC) · 15/10/2026

Documentos auditados: 40 · Conformes: 37 · RSD: 92.50 % · Entregas conciliadas: 25 · Concordantes: 21 · CPE: 84.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | TRA | DTA | L-2610-01 | 200 | S | S | S | S | S | S | S | S | S | — |
| 2 | SAL | PENT | L-2610-02 | 40 | S | S | S | S | S | S | S | S | S | — |
| 3 | DEV | IPV | L-2610-03 | 60 | S | S | S | S | S | S | S | S | S | — |
| 4 | ING | BCG | L-2610-04 | 200 | S | S | S | S | S | S | S | S | S | — |
| 5 | ING | DTA | L-2610-05 | 150 | S | S | S | S | S | S | S | S | S | — |
| 6 | ING | IPV | L-2610-06 | 200 | S | S | S | S | S | S | S | S | S | — |
| 7 | DEV | DTA | L-2610-07 | 80 | S | S | S | S | S | N | S | S | N | M6 |
| 8 | AJU | ROTA | L-2610-08 | 100 | S | S | S | S | S | S | S | S | S | — |
| 9 | ING | VARI | L-2610-09 | 60 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | NEUM | L-2610-10 | 20 | S | S | S | S | S | S | S | S | S | — |
| 11 | TRA | ROTA | L-2610-11 | 120 | S | S | S | S | S | S | S | S | S | — |
| 12 | TRA | HEPB | L-2610-12 | 120 | S | S | S | S | S | S | S | S | S | — |
| 13 | AJU | INFL | L-2610-13 | 200 | S | S | S | S | S | S | S | S | S | — |
| 14 | TRA | IPV | L-2610-14 | 240 | S | S | S | S | S | S | S | S | S | — |
| 15 | TRA | ROTA | L-2610-15 | 100 | S | S | S | S | S | S | S | S | S | — |
| 16 | AJU | INFL | L-2610-16 | 100 | S | S | S | S | S | S | S | S | S | — |
| 17 | TRA | HEPB | L-2610-17 | 20 | S | S | S | S | S | S | S | S | S | — |
| 18 | AJU | ROTA | L-2610-18 | 40 | S | S | S | S | S | S | S | S | S | — |
| 19 | ING | PENT | L-2610-19 | 300 | S | S | S | S | S | S | S | S | S | — |
| 20 | TRA | INFL | L-2610-20 | 40 | N | S | S | S | S | S | S | S | N | M1 |
| 21 | TRA | BCG | L-2610-21 | 300 | S | S | S | S | S | S | S | S | S | — |
| 22 | ING | ROTA | L-2610-22 | 150 | S | S | S | S | S | S | S | S | S | — |
| 23 | ING | VARI | L-2610-23 | 240 | S | S | S | S | S | S | S | S | S | — |
| 24 | AJU | VARI | L-2610-24 | 120 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | IPV | L-2610-25 | 60 | S | S | S | S | S | S | S | S | S | — |
| 26 | AJU | PENT | L-2610-26 | 80 | S | S | S | S | S | S | S | S | S | — |
| 27 | AJU | ROTA | L-2610-27 | 240 | S | S | S | S | S | S | S | S | S | — |
| 28 | ING | HEPB | L-2610-28 | 120 | S | S | S | S | S | S | S | S | S | — |
| 29 | TRA | IPV | L-2610-29 | 180 | S | S | S | S | S | S | S | S | S | — |
| 30 | AJU | BCG | L-2610-30 | 120 | S | S | S | N | S | S | S | S | N | M4 |
| 31 | ING | NEUM | L-2610-31 | 240 | S | S | S | S | S | S | S | S | S | — |
| 32 | ING | SPR | L-2610-32 | 300 | S | S | S | S | S | S | S | S | S | — |
| 33 | SAL | INFL | L-2610-33 | 100 | S | S | S | S | S | S | S | S | S | — |
| 34 | TRA | IPV | L-2610-34 | 20 | S | S | S | S | S | S | S | S | S | — |
| 35 | ING | BCG | L-2610-35 | 100 | S | S | S | S | S | S | S | S | S | — |
| 36 | TRA | SPR | L-2610-36 | 180 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | INFL | L-2610-37 | 40 | S | S | S | S | S | S | S | S | S | — |
| 38 | SAL | DTA | L-2610-38 | 80 | S | S | S | S | S | S | S | S | S | — |
| 39 | AJU | SPR | L-2610-39 | 120 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | SPR | L-2610-40 | 240 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-07 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 15/10/2026 | 4160 | VARI | 20 | 20 | 0 | No aplica | Sí |
| 2 | 15/10/2026 | 4160 | DTA | 180 | 180 | 0 | No aplica | Sí |
| 3 | 15/10/2026 | 4160 | BCG | 60 | 40 | -20 | Sí | No |
| 4 | 15/10/2026 | 4160 | DTA | 20 | 30 | 10 | Sí | No |
| 5 | 15/10/2026 | 4160 | ROTA | 40 | 40 | 0 | No aplica | Sí |
| 6 | 15/10/2026 | 4160 | SPR | 20 | 20 | 0 | No aplica | Sí |
| 7 | 15/10/2026 | 4160 | PENT | 180 | 180 | 0 | No aplica | Sí |
| 8 | 15/10/2026 | 4160 | ROTA | 60 | 60 | 0 | No aplica | Sí |
| 9 | 15/10/2026 | 4160 | BCG | 100 | 100 | 0 | No aplica | Sí |
| 10 | 15/10/2026 | 4160 | BCG | 60 | 60 | 0 | No aplica | Sí |
| 11 | 15/10/2026 | 4160 | IPV | 80 | 90 | 10 | Sí | No |
| 12 | 15/10/2026 | 4160 | IPV | 200 | 200 | 0 | No aplica | Sí |
| 13 | 15/10/2026 | 4160 | INFL | 200 | 200 | 0 | No aplica | Sí |
| 14 | 15/10/2026 | 4160 | PENT | 100 | 110 | 10 | Sí | No |
| 15 | 15/10/2026 | 4160 | VARI | 200 | 200 | 0 | No aplica | Sí |
| 16 | 15/10/2026 | 4160 | ROTA | 120 | 120 | 0 | No aplica | Sí |
| 17 | 15/10/2026 | 4160 | INFL | 20 | 20 | 0 | No aplica | Sí |
| 18 | 15/10/2026 | 4160 | IPV | 30 | 30 | 0 | No aplica | Sí |
| 19 | 15/10/2026 | 4160 | ROTA | 80 | 80 | 0 | No aplica | Sí |
| 20 | 15/10/2026 | 4160 | BCG | 50 | 50 | 0 | No aplica | Sí |
| 21 | 15/10/2026 | 4160 | SPR | 120 | 120 | 0 | No aplica | Sí |
| 22 | 15/10/2026 | 4160 | VARI | 20 | 20 | 0 | No aplica | Sí |
| 23 | 15/10/2026 | 4160 | VARI | 120 | 120 | 0 | No aplica | Sí |
| 24 | 15/10/2026 | 4160 | PENT | 20 | 20 | 0 | No aplica | Sí |
| 25 | 15/10/2026 | 4160 | SPR | 40 | 40 | 0 | No aplica | Sí |

Cierre: 21 entregas concordantes ÷ 25 × 100 = **84.00 %**.

---

### Bloque 15 · TRAB-08 · Pretest (proceso manual) · 13/08/2026

Documentos auditados: 40 · Conformes: 28 · RSD: 70.00 % · Entregas conciliadas: 25 · Concordantes: 17 · CPE: 68.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | TRA | PENT | L-2608-01 | 80 | S | S | S | S | S | S | S | S | S | — |
| 2 | AJU | PENT | L-2608-02 | 150 | S | S | S | S | N | S | S | S | N | M5 |
| 3 | AJU | HEPB | L-2608-03 | 150 | S | S | S | S | N | S | S | S | N | M5 |
| 4 | TRA | HEPB | L-2608-04 | 150 | S | S | S | S | S | S | S | N | N | M8 |
| 5 | ING | BCG | L-2608-05 | 300 | S | S | S | S | S | S | S | S | S | — |
| 6 | TRA | DTA | L-2608-06 | 200 | S | S | S | S | S | S | S | S | S | — |
| 7 | TRA | PENT | L-2608-07 | 40 | S | S | S | S | S | S | S | S | S | — |
| 8 | TRA | PENT | L-2608-08 | 200 | S | S | S | S | S | S | S | S | S | — |
| 9 | SAL | SPR | L-2608-09 | 200 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | NEUM | L-2608-10 | 180 | S | S | S | S | S | S | S | S | S | — |
| 11 | ING | VARI | L-2608-11 | 100 | S | S | S | S | S | S | S | S | S | — |
| 12 | DEV | HEPB | L-2608-12 | 180 | S | S | S | S | S | S | S | S | S | — |
| 13 | ING | IPV | L-2608-13 | 200 | S | S | S | S | S | S | S | S | S | — |
| 14 | TRA | PENT | L-2608-14 | 20 | N | S | S | S | S | S | S | S | N | M1 |
| 15 | ING | BCG | L-2608-15 | 60 | S | S | N | S | S | S | S | S | N | M3 |
| 16 | DEV | DTA | L-2608-16 | 300 | S | S | S | S | S | S | S | S | S | — |
| 17 | DEV | BCG | L-2608-17 | 180 | S | S | S | S | S | S | S | S | S | — |
| 18 | SAL | PENT | L-2608-18 | 20 | S | S | S | S | S | S | S | S | S | — |
| 19 | SAL | HEPB | L-2608-19 | 120 | S | S | S | S | S | S | S | S | S | — |
| 20 | SAL | IPV | L-2608-20 | 40 | S | S | S | S | S | S | S | S | S | — |
| 21 | TRA | VARI | L-2608-21 | 240 | S | S | S | S | S | S | S | S | S | — |
| 22 | TRA | BCG | L-2608-22 | 300 | S | N | S | S | S | S | S | S | N | M2 |
| 23 | TRA | SPR | L-2608-23 | 150 | S | S | S | S | S | S | S | S | S | — |
| 24 | AJU | ROTA | L-2608-24 | 200 | S | S | S | S | S | S | S | N | N | M8 |
| 25 | ING | NEUM | L-2608-25 | 80 | N | S | S | S | S | S | S | S | N | M1 |
| 26 | SAL | BCG | L-2608-26 | 180 | S | S | S | S | S | S | S | S | S | — |
| 27 | AJU | DTA | L-2608-27 | 40 | S | S | S | S | S | S | S | S | S | — |
| 28 | ING | DTA | L-2608-28 | 20 | S | S | S | S | S | S | S | S | S | — |
| 29 | AJU | SPR | L-2608-29 | 120 | S | S | S | S | S | S | S | S | S | — |
| 30 | SAL | SPR | L-2608-30 | 150 | S | S | S | S | S | S | S | S | S | — |
| 31 | ING | ROTA | L-2608-31 | 60 | S | S | S | S | S | S | S | S | S | — |
| 32 | TRA | NEUM | L-2608-32 | 150 | S | S | S | S | S | N | S | S | N | M6 |
| 33 | AJU | ROTA | L-2608-33 | 80 | S | S | S | S | S | S | S | S | S | — |
| 34 | TRA | BCG | L-2608-34 | 80 | S | S | S | S | S | S | S | S | S | — |
| 35 | ING | BCG | L-2608-35 | 60 | S | S | S | S | S | S | S | S | S | — |
| 36 | SAL | HEPB | L-2608-36 | 40 | S | S | N | S | S | S | S | S | N | M3 |
| 37 | SAL | IPV | L-2608-37 | 300 | S | S | S | S | S | S | S | S | S | — |
| 38 | TRA | BCG | L-2608-38 | 60 | S | S | S | S | S | S | S | S | S | — |
| 39 | DEV | INFL | L-2608-39 | 240 | S | S | S | S | S | S | S | N | N | M8 |
| 40 | TRA | IPV | L-2608-40 | 80 | S | S | S | S | S | N | S | S | N | M6 |

**Entregas conciliadas — TRAB-08 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 13/08/2026 | 4162 | INFL | 100 | 100 | 0 | No aplica | Sí |
| 2 | 13/08/2026 | 4162 | ROTA | 200 | 200 | 0 | No aplica | Sí |
| 3 | 13/08/2026 | 4162 | INFL | 100 | 120 | 20 | Sí | No |
| 4 | 13/08/2026 | 4162 | VARI | 60 | 60 | 0 | No aplica | Sí |
| 5 | 13/08/2026 | 4162 | NEUM | 100 | 100 | 0 | No aplica | Sí |
| 6 | 13/08/2026 | 4162 | HEPB | 200 | 220 | 20 | Sí | No |
| 7 | 13/08/2026 | 4162 | SPR | 200 | 200 | 0 | No aplica | Sí |
| 8 | 13/08/2026 | 4162 | ROTA | 200 | 200 | 0 | No aplica | Sí |
| 9 | 13/08/2026 | 4162 | DTA | 150 | 150 | 0 | No aplica | Sí |
| 10 | 13/08/2026 | 4162 | PENT | 120 | 120 | 0 | No aplica | Sí |
| 11 | 13/08/2026 | 4162 | NEUM | 120 | 120 | 0 | No aplica | Sí |
| 12 | 13/08/2026 | 4162 | NEUM | 40 | 40 | 0 | No aplica | Sí |
| 13 | 13/08/2026 | 4162 | BCG | 30 | 30 | 0 | No aplica | Sí |
| 14 | 13/08/2026 | 4162 | ROTA | 100 | 90 | -10 | Sí | No |
| 15 | 13/08/2026 | 4162 | VARI | 50 | 50 | 0 | No aplica | Sí |
| 16 | 13/08/2026 | 4162 | BCG | 120 | 120 | 0 | No aplica | Sí |
| 17 | 13/08/2026 | 4162 | NEUM | 100 | 100 | 0 | No aplica | Sí |
| 18 | 13/08/2026 | 4162 | IPV | 60 | 55 | -5 | Sí | No |
| 19 | 13/08/2026 | 4162 | PENT | 180 | 200 | 20 | Sí | No |
| 20 | 13/08/2026 | 4162 | PENT | 20 | 20 | 0 | No aplica | Sí |
| 21 | 13/08/2026 | 4162 | DTA | 50 | 30 | -20 | Sí | No |
| 22 | 13/08/2026 | 4162 | PENT | 100 | 100 | 0 | No aplica | Sí |
| 23 | 13/08/2026 | 4162 | ROTA | 50 | 50 | 0 | No aplica | Sí |
| 24 | 13/08/2026 | 4162 | PENT | 40 | 60 | 20 | Sí | No |
| 25 | 13/08/2026 | 4162 | SPR | 60 | 55 | -5 | Sí | No |

Cierre: 17 entregas concordantes ÷ 25 × 100 = **68.00 %**.

---

### Bloque 16 · TRAB-08 · Postest (Sistema SIVAC) · 15/10/2026

Documentos auditados: 40 · Conformes: 35 · RSD: 87.50 % · Entregas conciliadas: 25 · Concordantes: 22 · CPE: 88.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | AJU | INFL | L-2610-01 | 240 | S | S | S | S | S | S | S | S | S | — |
| 2 | SAL | PENT | L-2610-02 | 180 | S | S | S | S | S | S | N | S | N | M7 |
| 3 | TRA | NEUM | L-2610-03 | 100 | S | S | S | S | S | S | S | S | S | — |
| 4 | DEV | ROTA | L-2610-04 | 120 | S | S | S | S | S | S | S | S | S | — |
| 5 | DEV | INFL | L-2610-05 | 60 | S | S | S | S | S | S | S | S | S | — |
| 6 | AJU | NEUM | L-2610-06 | 300 | S | S | S | S | S | S | S | S | S | — |
| 7 | AJU | NEUM | L-2610-07 | 120 | S | S | S | S | S | S | S | S | S | — |
| 8 | AJU | ROTA | L-2610-08 | 80 | S | S | S | S | S | S | S | S | S | — |
| 9 | ING | HEPB | L-2610-09 | 240 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | SPR | L-2610-10 | 200 | N | S | S | S | S | S | S | S | N | M1 |
| 11 | TRA | PENT | L-2610-11 | 120 | S | S | S | S | S | S | S | S | S | — |
| 12 | SAL | SPR | L-2610-12 | 120 | S | S | S | S | S | S | S | S | S | — |
| 13 | SAL | PENT | L-2610-13 | 120 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | HEPB | L-2610-14 | 60 | S | S | S | S | S | S | S | S | S | — |
| 15 | TRA | DTA | L-2610-15 | 120 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | INFL | L-2610-16 | 100 | S | S | S | S | S | S | S | S | S | — |
| 17 | AJU | VARI | L-2610-17 | 200 | S | S | S | S | S | S | S | S | S | — |
| 18 | SAL | SPR | L-2610-18 | 60 | S | S | S | S | S | S | S | S | S | — |
| 19 | AJU | DTA | L-2610-19 | 80 | S | S | S | S | S | S | S | S | S | — |
| 20 | TRA | SPR | L-2610-20 | 180 | S | S | S | S | S | S | S | S | S | — |
| 21 | ING | ROTA | L-2610-21 | 20 | S | S | S | S | S | S | S | S | S | — |
| 22 | ING | IPV | L-2610-22 | 200 | S | S | S | S | S | S | S | S | S | — |
| 23 | AJU | HEPB | L-2610-23 | 60 | S | S | S | S | S | S | S | S | S | — |
| 24 | ING | PENT | L-2610-24 | 120 | S | S | S | S | S | S | S | S | S | — |
| 25 | DEV | ROTA | L-2610-25 | 180 | S | S | S | S | S | S | S | S | S | — |
| 26 | ING | VARI | L-2610-26 | 40 | S | S | S | S | S | S | S | S | S | — |
| 27 | DEV | VARI | L-2610-27 | 300 | S | S | S | S | S | S | N | S | N | M7 |
| 28 | SAL | VARI | L-2610-28 | 240 | S | S | S | S | S | S | S | S | S | — |
| 29 | AJU | DTA | L-2610-29 | 300 | S | S | S | S | S | S | S | S | S | — |
| 30 | TRA | VARI | L-2610-30 | 200 | S | S | S | S | S | S | S | S | S | — |
| 31 | AJU | SPR | L-2610-31 | 200 | S | S | S | S | S | S | S | S | S | — |
| 32 | DEV | DTA | L-2610-32 | 150 | S | S | N | S | S | S | S | S | N | M3 |
| 33 | SAL | BCG | L-2610-33 | 150 | S | S | S | S | S | S | S | S | S | — |
| 34 | DEV | IPV | L-2610-34 | 40 | S | S | S | S | S | S | S | S | S | — |
| 35 | SAL | HEPB | L-2610-35 | 60 | S | S | S | S | N | S | S | S | N | M5 |
| 36 | ING | PENT | L-2610-36 | 60 | S | S | S | S | S | S | S | S | S | — |
| 37 | ING | NEUM | L-2610-37 | 60 | S | S | S | S | S | S | S | S | S | — |
| 38 | ING | BCG | L-2610-38 | 240 | S | S | S | S | S | S | S | S | S | — |
| 39 | TRA | DTA | L-2610-39 | 200 | S | S | S | S | S | S | S | S | S | — |
| 40 | SAL | PENT | L-2610-40 | 80 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-08 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 15/10/2026 | 4162 | HEPB | 120 | 120 | 0 | No aplica | Sí |
| 2 | 15/10/2026 | 4162 | BCG | 120 | 120 | 0 | No aplica | Sí |
| 3 | 15/10/2026 | 4162 | PENT | 40 | 40 | 0 | No aplica | Sí |
| 4 | 15/10/2026 | 4162 | INFL | 60 | 60 | 0 | No aplica | Sí |
| 5 | 15/10/2026 | 4162 | BCG | 120 | 120 | 0 | No aplica | Sí |
| 6 | 15/10/2026 | 4162 | DTA | 180 | 180 | 0 | No aplica | Sí |
| 7 | 15/10/2026 | 4162 | PENT | 120 | 140 | 20 | Sí | No |
| 8 | 15/10/2026 | 4162 | VARI | 50 | 50 | 0 | No aplica | Sí |
| 9 | 15/10/2026 | 4162 | INFL | 120 | 120 | 0 | No aplica | Sí |
| 10 | 15/10/2026 | 4162 | BCG | 40 | 40 | 0 | No aplica | Sí |
| 11 | 15/10/2026 | 4162 | DTA | 30 | 30 | 0 | No aplica | Sí |
| 12 | 15/10/2026 | 4162 | INFL | 120 | 120 | 0 | No aplica | Sí |
| 13 | 15/10/2026 | 4162 | IPV | 60 | 60 | 0 | No aplica | Sí |
| 14 | 15/10/2026 | 4162 | DTA | 120 | 120 | 0 | No aplica | Sí |
| 15 | 15/10/2026 | 4162 | DTA | 120 | 120 | 0 | No aplica | Sí |
| 16 | 15/10/2026 | 4162 | HEPB | 150 | 150 | 0 | No aplica | Sí |
| 17 | 15/10/2026 | 4162 | NEUM | 40 | 50 | 10 | Sí | No |
| 18 | 15/10/2026 | 4162 | INFL | 150 | 150 | 0 | No aplica | Sí |
| 19 | 15/10/2026 | 4162 | ROTA | 100 | 100 | 0 | No aplica | Sí |
| 20 | 15/10/2026 | 4162 | DTA | 30 | 30 | 0 | No aplica | Sí |
| 21 | 15/10/2026 | 4162 | HEPB | 180 | 180 | 0 | No aplica | Sí |
| 22 | 15/10/2026 | 4162 | HEPB | 50 | 45 | -5 | Sí | No |
| 23 | 15/10/2026 | 4162 | DTA | 30 | 30 | 0 | No aplica | Sí |
| 24 | 15/10/2026 | 4162 | ROTA | 30 | 30 | 0 | No aplica | Sí |
| 25 | 15/10/2026 | 4162 | BCG | 60 | 60 | 0 | No aplica | Sí |

Cierre: 22 entregas concordantes ÷ 25 × 100 = **88.00 %**.

---

### Bloque 17 · TRAB-09 · Pretest (proceso manual) · 14/08/2026

Documentos auditados: 40 · Conformes: 19 · RSD: 47.50 % · Entregas conciliadas: 25 · Concordantes: 19 · CPE: 76.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | DEV | NEUM | L-2608-01 | 80 | S | S | S | S | N | S | S | S | N | M5 |
| 2 | TRA | SPR | L-2608-02 | 240 | S | S | S | N | S | S | S | S | N | M4 |
| 3 | ING | IPV | L-2608-03 | 240 | S | S | S | S | S | S | S | S | S | — |
| 4 | TRA | NEUM | L-2608-04 | 60 | S | S | S | S | S | S | S | S | S | — |
| 5 | TRA | NEUM | L-2608-05 | 200 | S | S | S | N | S | S | S | S | N | M4 |
| 6 | ING | INFL | L-2608-06 | 20 | S | S | S | S | S | N | S | S | N | M6 |
| 7 | SAL | DTA | L-2608-07 | 120 | S | S | S | N | S | S | S | S | N | M4 |
| 8 | ING | ROTA | L-2608-08 | 120 | S | S | S | S | S | S | S | S | S | — |
| 9 | ING | VARI | L-2608-09 | 40 | S | S | S | S | S | S | S | S | S | — |
| 10 | AJU | IPV | L-2608-10 | 150 | S | S | S | S | S | S | S | N | N | M8 |
| 11 | ING | DTA | L-2608-11 | 150 | S | S | S | S | S | S | S | S | S | — |
| 12 | TRA | SPR | L-2608-12 | 200 | S | S | S | S | S | S | S | S | S | — |
| 13 | SAL | HEPB | L-2608-13 | 20 | S | S | S | S | N | S | S | S | N | M5 |
| 14 | SAL | IPV | L-2608-14 | 180 | S | S | S | S | S | S | S | S | S | — |
| 15 | AJU | DTA | L-2608-15 | 120 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | PENT | L-2608-16 | 40 | S | S | S | S | S | S | S | N | N | M8 |
| 17 | AJU | NEUM | L-2608-17 | 120 | S | S | S | S | S | N | S | S | N | M6 |
| 18 | ING | VARI | L-2608-18 | 300 | S | S | S | S | S | S | S | S | S | — |
| 19 | TRA | SPR | L-2608-19 | 80 | S | N | S | S | S | S | S | S | N | M2 |
| 20 | SAL | VARI | L-2608-20 | 180 | S | S | S | S | S | N | S | S | N | M6 |
| 21 | SAL | DTA | L-2608-21 | 60 | S | N | S | S | S | S | S | S | N | M2 |
| 22 | ING | HEPB | L-2608-22 | 20 | S | S | S | S | S | S | S | S | S | — |
| 23 | ING | SPR | L-2608-23 | 40 | S | S | S | S | S | S | S | S | S | — |
| 24 | AJU | PENT | L-2608-24 | 240 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | INFL | L-2608-25 | 20 | S | S | N | S | S | S | S | S | N | M3 |
| 26 | SAL | SPR | L-2608-26 | 40 | S | S | S | N | S | S | S | S | N | M4 |
| 27 | ING | SPR | L-2608-27 | 80 | S | S | S | S | S | S | S | N | N | M8 |
| 28 | DEV | ROTA | L-2608-28 | 150 | S | S | S | S | S | S | S | N | N | M8 |
| 29 | SAL | IPV | L-2608-29 | 300 | S | N | S | S | S | S | S | S | N | M2 |
| 30 | DEV | ROTA | L-2608-30 | 180 | S | S | S | S | S | S | S | S | S | — |
| 31 | ING | IPV | L-2608-31 | 40 | S | S | S | S | S | S | S | S | S | — |
| 32 | AJU | ROTA | L-2608-32 | 150 | S | S | N | S | S | S | S | S | N | M3 |
| 33 | AJU | IPV | L-2608-33 | 100 | S | N | S | S | S | S | S | S | N | M2 |
| 34 | DEV | NEUM | L-2608-34 | 60 | S | S | S | S | S | S | S | S | S | — |
| 35 | ING | NEUM | L-2608-35 | 300 | S | S | S | S | S | S | S | N | N | M8 |
| 36 | AJU | NEUM | L-2608-36 | 120 | S | S | S | S | S | S | S | S | S | — |
| 37 | AJU | VARI | L-2608-37 | 240 | S | S | S | S | S | S | S | S | S | — |
| 38 | SAL | INFL | L-2608-38 | 80 | S | S | S | S | S | S | S | S | S | — |
| 39 | DEV | NEUM | L-2608-39 | 40 | S | S | S | S | S | S | S | N | N | M8 |
| 40 | AJU | HEPB | L-2608-40 | 150 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-09 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 14/08/2026 | 4163 | IPV | 50 | 50 | 0 | No aplica | Sí |
| 2 | 14/08/2026 | 4163 | SPR | 200 | 200 | 0 | No aplica | Sí |
| 3 | 14/08/2026 | 4163 | SPR | 40 | 40 | 0 | No aplica | Sí |
| 4 | 14/08/2026 | 4163 | VARI | 80 | 80 | 0 | No aplica | Sí |
| 5 | 14/08/2026 | 4163 | BCG | 150 | 160 | 10 | Sí | No |
| 6 | 14/08/2026 | 4163 | ROTA | 100 | 80 | -20 | Sí | No |
| 7 | 14/08/2026 | 4163 | INFL | 50 | 50 | 0 | No aplica | Sí |
| 8 | 14/08/2026 | 4163 | BCG | 50 | 50 | 0 | No aplica | Sí |
| 9 | 14/08/2026 | 4163 | NEUM | 20 | 20 | 0 | No aplica | Sí |
| 10 | 14/08/2026 | 4163 | HEPB | 200 | 200 | 0 | No aplica | Sí |
| 11 | 14/08/2026 | 4163 | INFL | 150 | 150 | 0 | No aplica | Sí |
| 12 | 14/08/2026 | 4163 | NEUM | 180 | 185 | 5 | Sí | No |
| 13 | 14/08/2026 | 4163 | SPR | 60 | 60 | 0 | No aplica | Sí |
| 14 | 14/08/2026 | 4163 | ROTA | 50 | 50 | 0 | No aplica | Sí |
| 15 | 14/08/2026 | 4163 | SPR | 150 | 145 | -5 | Sí | No |
| 16 | 14/08/2026 | 4163 | ROTA | 100 | 100 | 0 | No aplica | Sí |
| 17 | 14/08/2026 | 4163 | IPV | 40 | 40 | 0 | No aplica | Sí |
| 18 | 14/08/2026 | 4163 | IPV | 100 | 100 | 0 | No aplica | Sí |
| 19 | 14/08/2026 | 4163 | ROTA | 120 | 120 | 0 | No aplica | Sí |
| 20 | 14/08/2026 | 4163 | PENT | 200 | 220 | 20 | Sí | No |
| 21 | 14/08/2026 | 4163 | PENT | 180 | 185 | 5 | Sí | No |
| 22 | 14/08/2026 | 4163 | DTA | 50 | 50 | 0 | No aplica | Sí |
| 23 | 14/08/2026 | 4163 | ROTA | 20 | 20 | 0 | No aplica | Sí |
| 24 | 14/08/2026 | 4163 | SPR | 50 | 50 | 0 | No aplica | Sí |
| 25 | 14/08/2026 | 4163 | BCG | 200 | 200 | 0 | No aplica | Sí |

Cierre: 19 entregas concordantes ÷ 25 × 100 = **76.00 %**.

---

### Bloque 18 · TRAB-09 · Postest (Sistema SIVAC) · 16/10/2026

Documentos auditados: 40 · Conformes: 40 · RSD: 100.00 % · Entregas conciliadas: 25 · Concordantes: 21 · CPE: 84.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | SAL | IPV | L-2610-01 | 200 | S | S | S | S | S | S | S | S | S | — |
| 2 | AJU | DTA | L-2610-02 | 180 | S | S | S | S | S | S | S | S | S | — |
| 3 | SAL | PENT | L-2610-03 | 200 | S | S | S | S | S | S | S | S | S | — |
| 4 | AJU | PENT | L-2610-04 | 150 | S | S | S | S | S | S | S | S | S | — |
| 5 | AJU | SPR | L-2610-05 | 150 | S | S | S | S | S | S | S | S | S | — |
| 6 | ING | INFL | L-2610-06 | 20 | S | S | S | S | S | S | S | S | S | — |
| 7 | ING | VARI | L-2610-07 | 60 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | HEPB | L-2610-08 | 240 | S | S | S | S | S | S | S | S | S | — |
| 9 | AJU | SPR | L-2610-09 | 150 | S | S | S | S | S | S | S | S | S | — |
| 10 | TRA | VARI | L-2610-10 | 20 | S | S | S | S | S | S | S | S | S | — |
| 11 | TRA | SPR | L-2610-11 | 60 | S | S | S | S | S | S | S | S | S | — |
| 12 | ING | NEUM | L-2610-12 | 180 | S | S | S | S | S | S | S | S | S | — |
| 13 | ING | SPR | L-2610-13 | 200 | S | S | S | S | S | S | S | S | S | — |
| 14 | AJU | SPR | L-2610-14 | 120 | S | S | S | S | S | S | S | S | S | — |
| 15 | ING | DTA | L-2610-15 | 150 | S | S | S | S | S | S | S | S | S | — |
| 16 | TRA | SPR | L-2610-16 | 60 | S | S | S | S | S | S | S | S | S | — |
| 17 | AJU | SPR | L-2610-17 | 20 | S | S | S | S | S | S | S | S | S | — |
| 18 | TRA | HEPB | L-2610-18 | 20 | S | S | S | S | S | S | S | S | S | — |
| 19 | DEV | IPV | L-2610-19 | 240 | S | S | S | S | S | S | S | S | S | — |
| 20 | ING | BCG | L-2610-20 | 60 | S | S | S | S | S | S | S | S | S | — |
| 21 | TRA | HEPB | L-2610-21 | 80 | S | S | S | S | S | S | S | S | S | — |
| 22 | SAL | VARI | L-2610-22 | 120 | S | S | S | S | S | S | S | S | S | — |
| 23 | AJU | ROTA | L-2610-23 | 180 | S | S | S | S | S | S | S | S | S | — |
| 24 | SAL | SPR | L-2610-24 | 60 | S | S | S | S | S | S | S | S | S | — |
| 25 | ING | NEUM | L-2610-25 | 120 | S | S | S | S | S | S | S | S | S | — |
| 26 | TRA | INFL | L-2610-26 | 40 | S | S | S | S | S | S | S | S | S | — |
| 27 | TRA | VARI | L-2610-27 | 300 | S | S | S | S | S | S | S | S | S | — |
| 28 | ING | DTA | L-2610-28 | 240 | S | S | S | S | S | S | S | S | S | — |
| 29 | SAL | BCG | L-2610-29 | 20 | S | S | S | S | S | S | S | S | S | — |
| 30 | DEV | INFL | L-2610-30 | 60 | S | S | S | S | S | S | S | S | S | — |
| 31 | AJU | PENT | L-2610-31 | 80 | S | S | S | S | S | S | S | S | S | — |
| 32 | AJU | SPR | L-2610-32 | 150 | S | S | S | S | S | S | S | S | S | — |
| 33 | ING | PENT | L-2610-33 | 100 | S | S | S | S | S | S | S | S | S | — |
| 34 | SAL | PENT | L-2610-34 | 120 | S | S | S | S | S | S | S | S | S | — |
| 35 | AJU | BCG | L-2610-35 | 40 | S | S | S | S | S | S | S | S | S | — |
| 36 | ING | PENT | L-2610-36 | 300 | S | S | S | S | S | S | S | S | S | — |
| 37 | TRA | DTA | L-2610-37 | 200 | S | S | S | S | S | S | S | S | S | — |
| 38 | TRA | INFL | L-2610-38 | 60 | S | S | S | S | S | S | S | S | S | — |
| 39 | ING | IPV | L-2610-39 | 100 | S | S | S | S | S | S | S | S | S | — |
| 40 | AJU | HEPB | L-2610-40 | 20 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-09 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 16/10/2026 | 4163 | HEPB | 180 | 180 | 0 | No aplica | Sí |
| 2 | 16/10/2026 | 4163 | NEUM | 180 | 180 | 0 | No aplica | Sí |
| 3 | 16/10/2026 | 4163 | IPV | 150 | 160 | 10 | Sí | No |
| 4 | 16/10/2026 | 4163 | ROTA | 100 | 100 | 0 | No aplica | Sí |
| 5 | 16/10/2026 | 4163 | HEPB | 180 | 180 | 0 | No aplica | Sí |
| 6 | 16/10/2026 | 4163 | SPR | 60 | 60 | 0 | No aplica | Sí |
| 7 | 16/10/2026 | 4163 | BCG | 100 | 100 | 0 | No aplica | Sí |
| 8 | 16/10/2026 | 4163 | ROTA | 150 | 150 | 0 | No aplica | Sí |
| 9 | 16/10/2026 | 4163 | SPR | 200 | 190 | -10 | Sí | No |
| 10 | 16/10/2026 | 4163 | SPR | 40 | 40 | 0 | No aplica | Sí |
| 11 | 16/10/2026 | 4163 | INFL | 30 | 30 | 0 | No aplica | Sí |
| 12 | 16/10/2026 | 4163 | ROTA | 80 | 80 | 0 | No aplica | Sí |
| 13 | 16/10/2026 | 4163 | VARI | 120 | 120 | 0 | No aplica | Sí |
| 14 | 16/10/2026 | 4163 | HEPB | 40 | 40 | 0 | No aplica | Sí |
| 15 | 16/10/2026 | 4163 | DTA | 100 | 100 | 0 | No aplica | Sí |
| 16 | 16/10/2026 | 4163 | PENT | 40 | 40 | 0 | No aplica | Sí |
| 17 | 16/10/2026 | 4163 | SPR | 40 | 40 | 0 | No aplica | Sí |
| 18 | 16/10/2026 | 4163 | ROTA | 120 | 120 | 0 | No aplica | Sí |
| 19 | 16/10/2026 | 4163 | BCG | 20 | 40 | 20 | Sí | No |
| 20 | 16/10/2026 | 4163 | PENT | 50 | 50 | 0 | No aplica | Sí |
| 21 | 16/10/2026 | 4163 | IPV | 200 | 190 | -10 | Sí | No |
| 22 | 16/10/2026 | 4163 | ROTA | 30 | 30 | 0 | No aplica | Sí |
| 23 | 16/10/2026 | 4163 | IPV | 180 | 180 | 0 | No aplica | Sí |
| 24 | 16/10/2026 | 4163 | HEPB | 120 | 120 | 0 | No aplica | Sí |
| 25 | 16/10/2026 | 4163 | INFL | 40 | 40 | 0 | No aplica | Sí |

Cierre: 21 entregas concordantes ÷ 25 × 100 = **84.00 %**.

---

### Bloque 19 · TRAB-10 · Pretest (proceso manual) · 14/08/2026

Documentos auditados: 40 · Conformes: 25 · RSD: 62.50 % · Entregas conciliadas: 25 · Concordantes: 18 · CPE: 72.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | TRA | SPR | L-2608-01 | 80 | N | S | S | S | S | S | S | S | N | M1 |
| 2 | TRA | HEPB | L-2608-02 | 300 | S | N | S | S | S | S | S | S | N | M2 |
| 3 | DEV | BCG | L-2608-03 | 240 | S | S | S | S | S | S | S | S | S | — |
| 4 | SAL | VARI | L-2608-04 | 60 | S | S | S | S | S | S | S | S | S | — |
| 5 | DEV | BCG | L-2608-05 | 40 | S | S | S | S | S | S | S | N | N | M8 |
| 6 | ING | HEPB | L-2608-06 | 80 | S | S | S | S | S | S | S | S | S | — |
| 7 | AJU | ROTA | L-2608-07 | 150 | S | S | S | S | S | S | S | S | S | — |
| 8 | DEV | IPV | L-2608-08 | 200 | S | S | S | S | S | S | S | S | S | — |
| 9 | SAL | SPR | L-2608-09 | 20 | S | S | S | S | S | S | S | S | S | — |
| 10 | SAL | SPR | L-2608-10 | 120 | S | S | S | S | S | S | S | S | S | — |
| 11 | TRA | HEPB | L-2608-11 | 240 | S | S | S | S | S | S | S | S | S | — |
| 12 | AJU | NEUM | L-2608-12 | 40 | S | S | S | S | S | S | S | S | S | — |
| 13 | TRA | NEUM | L-2608-13 | 40 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | IPV | L-2608-14 | 20 | S | S | S | S | S | S | N | S | N | M7 |
| 15 | DEV | NEUM | L-2608-15 | 120 | S | S | S | S | S | S | S | S | S | — |
| 16 | AJU | VARI | L-2608-16 | 200 | S | S | S | S | S | S | S | S | S | — |
| 17 | AJU | IPV | L-2608-17 | 20 | S | S | S | S | S | S | S | S | S | — |
| 18 | TRA | PENT | L-2608-18 | 40 | S | S | S | S | S | S | S | S | S | — |
| 19 | ING | PENT | L-2608-19 | 200 | S | S | S | S | N | S | S | S | N | M5 |
| 20 | DEV | SPR | L-2608-20 | 150 | S | S | S | S | S | S | S | S | S | — |
| 21 | SAL | VARI | L-2608-21 | 20 | S | S | S | S | S | S | S | S | S | — |
| 22 | SAL | VARI | L-2608-22 | 300 | S | S | S | S | S | S | S | S | S | — |
| 23 | SAL | NEUM | L-2608-23 | 40 | S | S | S | S | S | S | S | S | S | — |
| 24 | SAL | PENT | L-2608-24 | 40 | S | S | S | S | S | N | S | S | N | M6 |
| 25 | SAL | VARI | L-2608-25 | 60 | S | S | S | S | S | S | S | S | S | — |
| 26 | ING | DTA | L-2608-26 | 180 | S | S | S | S | S | S | S | S | S | — |
| 27 | AJU | SPR | L-2608-27 | 20 | S | S | N | S | S | S | S | S | N | M3 |
| 28 | TRA | PENT | L-2608-28 | 200 | S | S | S | S | S | S | S | S | S | — |
| 29 | AJU | BCG | L-2608-29 | 120 | S | S | S | S | S | S | S | S | S | — |
| 30 | AJU | HEPB | L-2608-30 | 120 | S | S | S | S | S | S | N | S | N | M7 |
| 31 | ING | ROTA | L-2608-31 | 40 | S | S | S | S | S | N | S | S | N | M6 |
| 32 | DEV | PENT | L-2608-32 | 180 | N | S | S | S | S | S | S | S | N | M1 |
| 33 | SAL | INFL | L-2608-33 | 240 | S | S | S | S | N | S | S | S | N | M5 |
| 34 | TRA | ROTA | L-2608-34 | 20 | S | S | S | S | S | S | S | S | S | — |
| 35 | DEV | HEPB | L-2608-35 | 40 | S | S | S | S | S | S | S | S | S | — |
| 36 | TRA | PENT | L-2608-36 | 240 | S | N | S | S | S | S | S | S | N | M2 |
| 37 | TRA | ROTA | L-2608-37 | 20 | S | S | S | N | S | S | S | S | N | M4 |
| 38 | ING | NEUM | L-2608-38 | 60 | S | S | N | S | S | S | S | S | N | M3 |
| 39 | AJU | NEUM | L-2608-39 | 180 | N | S | S | S | S | S | S | S | N | M1 |
| 40 | DEV | SPR | L-2608-40 | 80 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-10 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 14/08/2026 | 4167 | INFL | 60 | 60 | 0 | No aplica | Sí |
| 2 | 14/08/2026 | 4167 | VARI | 20 | 20 | 0 | No aplica | Sí |
| 3 | 14/08/2026 | 4167 | IPV | 80 | 85 | 5 | Sí | No |
| 4 | 14/08/2026 | 4167 | IPV | 50 | 50 | 0 | No aplica | Sí |
| 5 | 14/08/2026 | 4167 | VARI | 120 | 120 | 0 | No aplica | Sí |
| 6 | 14/08/2026 | 4167 | ROTA | 200 | 200 | 0 | No aplica | Sí |
| 7 | 14/08/2026 | 4167 | SPR | 100 | 100 | 0 | No aplica | Sí |
| 8 | 14/08/2026 | 4167 | SPR | 80 | 80 | 0 | No aplica | Sí |
| 9 | 14/08/2026 | 4167 | BCG | 200 | 200 | 0 | No aplica | Sí |
| 10 | 14/08/2026 | 4167 | VARI | 150 | 150 | 0 | No aplica | Sí |
| 11 | 14/08/2026 | 4167 | ROTA | 80 | 80 | 0 | No aplica | Sí |
| 12 | 14/08/2026 | 4167 | HEPB | 30 | 25 | -5 | Sí | No |
| 13 | 14/08/2026 | 4167 | ROTA | 120 | 125 | 5 | Sí | No |
| 14 | 14/08/2026 | 4167 | HEPB | 60 | 60 | 0 | No aplica | Sí |
| 15 | 14/08/2026 | 4167 | IPV | 80 | 80 | 0 | No aplica | Sí |
| 16 | 14/08/2026 | 4167 | VARI | 60 | 65 | 5 | Sí | No |
| 17 | 14/08/2026 | 4167 | ROTA | 60 | 60 | 0 | No aplica | Sí |
| 18 | 14/08/2026 | 4167 | NEUM | 40 | 40 | 0 | No aplica | Sí |
| 19 | 14/08/2026 | 4167 | NEUM | 200 | 205 | 5 | Sí | No |
| 20 | 14/08/2026 | 4167 | IPV | 60 | 55 | -5 | Sí | No |
| 21 | 14/08/2026 | 4167 | DTA | 100 | 80 | -20 | Sí | No |
| 22 | 14/08/2026 | 4167 | HEPB | 30 | 30 | 0 | No aplica | Sí |
| 23 | 14/08/2026 | 4167 | IPV | 200 | 200 | 0 | No aplica | Sí |
| 24 | 14/08/2026 | 4167 | BCG | 40 | 40 | 0 | No aplica | Sí |
| 25 | 14/08/2026 | 4167 | BCG | 50 | 50 | 0 | No aplica | Sí |

Cierre: 18 entregas concordantes ÷ 25 × 100 = **72.00 %**.

---

### Bloque 20 · TRAB-10 · Postest (Sistema SIVAC) · 16/10/2026

Documentos auditados: 40 · Conformes: 37 · RSD: 92.50 % · Entregas conciliadas: 25 · Concordantes: 20 · CPE: 80.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | DEV | BCG | L-2610-01 | 60 | S | S | S | S | S | S | S | S | S | — |
| 2 | DEV | VARI | L-2610-02 | 150 | S | S | S | S | S | S | S | S | S | — |
| 3 | ING | NEUM | L-2610-03 | 150 | S | S | S | S | S | S | S | S | S | — |
| 4 | AJU | NEUM | L-2610-04 | 180 | S | S | S | S | S | S | S | S | S | — |
| 5 | SAL | HEPB | L-2610-05 | 180 | S | S | S | S | S | S | S | S | S | — |
| 6 | TRA | NEUM | L-2610-06 | 100 | S | S | S | S | S | S | S | S | S | — |
| 7 | ING | NEUM | L-2610-07 | 60 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | HEPB | L-2610-08 | 20 | S | S | S | S | S | S | S | S | S | — |
| 9 | TRA | INFL | L-2610-09 | 180 | S | S | S | S | S | S | S | S | S | — |
| 10 | DEV | INFL | L-2610-10 | 240 | S | S | S | S | S | S | S | S | S | — |
| 11 | SAL | PENT | L-2610-11 | 240 | S | S | S | S | S | S | S | S | S | — |
| 12 | ING | IPV | L-2610-12 | 240 | S | S | S | S | S | S | S | S | S | — |
| 13 | ING | BCG | L-2610-13 | 150 | S | S | S | S | S | S | S | S | S | — |
| 14 | DEV | INFL | L-2610-14 | 150 | S | S | S | S | S | N | S | S | N | M6 |
| 15 | ING | IPV | L-2610-15 | 120 | S | S | S | S | S | S | S | S | S | — |
| 16 | AJU | PENT | L-2610-16 | 80 | S | S | S | S | S | S | S | S | S | — |
| 17 | SAL | IPV | L-2610-17 | 20 | S | S | S | S | S | S | S | S | S | — |
| 18 | SAL | BCG | L-2610-18 | 20 | S | S | S | S | S | S | S | S | S | — |
| 19 | DEV | SPR | L-2610-19 | 40 | S | S | S | S | S | S | S | S | S | — |
| 20 | DEV | NEUM | L-2610-20 | 60 | S | S | S | S | S | S | S | S | S | — |
| 21 | TRA | ROTA | L-2610-21 | 200 | S | S | S | S | S | S | S | S | S | — |
| 22 | ING | PENT | L-2610-22 | 60 | S | S | S | S | S | S | S | S | S | — |
| 23 | SAL | SPR | L-2610-23 | 40 | S | S | S | S | S | S | S | S | S | — |
| 24 | TRA | NEUM | L-2610-24 | 40 | S | S | S | S | S | S | S | S | S | — |
| 25 | SAL | VARI | L-2610-25 | 80 | S | S | S | S | S | S | S | S | S | — |
| 26 | ING | VARI | L-2610-26 | 80 | S | S | S | S | S | S | S | S | S | — |
| 27 | TRA | VARI | L-2610-27 | 300 | S | S | S | S | S | S | S | S | S | — |
| 28 | AJU | IPV | L-2610-28 | 80 | S | S | S | S | S | S | S | S | S | — |
| 29 | SAL | IPV | L-2610-29 | 300 | S | S | S | S | S | S | S | S | S | — |
| 30 | ING | HEPB | L-2610-30 | 100 | S | S | S | S | S | S | S | S | S | — |
| 31 | ING | DTA | L-2610-31 | 150 | S | S | S | S | S | S | S | N | N | M8 |
| 32 | SAL | BCG | L-2610-32 | 180 | S | S | S | S | S | S | S | S | S | — |
| 33 | AJU | DTA | L-2610-33 | 300 | S | S | S | S | S | S | S | S | S | — |
| 34 | AJU | SPR | L-2610-34 | 180 | S | S | S | S | S | S | S | S | S | — |
| 35 | ING | HEPB | L-2610-35 | 240 | S | S | S | S | S | S | S | S | S | — |
| 36 | SAL | INFL | L-2610-36 | 300 | S | S | S | S | S | S | S | S | S | — |
| 37 | DEV | NEUM | L-2610-37 | 40 | S | S | S | S | S | S | S | S | S | — |
| 38 | ING | VARI | L-2610-38 | 200 | S | S | S | S | S | S | S | S | S | — |
| 39 | DEV | DTA | L-2610-39 | 20 | S | N | S | S | S | S | S | S | N | M2 |
| 40 | ING | HEPB | L-2610-40 | 40 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-10 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 16/10/2026 | 4167 | IPV | 20 | 20 | 0 | No aplica | Sí |
| 2 | 16/10/2026 | 4167 | ROTA | 60 | 60 | 0 | No aplica | Sí |
| 3 | 16/10/2026 | 4167 | PENT | 30 | 30 | 0 | No aplica | Sí |
| 4 | 16/10/2026 | 4167 | DTA | 60 | 60 | 0 | No aplica | Sí |
| 5 | 16/10/2026 | 4167 | ROTA | 120 | 120 | 0 | No aplica | Sí |
| 6 | 16/10/2026 | 4167 | SPR | 50 | 50 | 0 | No aplica | Sí |
| 7 | 16/10/2026 | 4167 | PENT | 40 | 40 | 0 | No aplica | Sí |
| 8 | 16/10/2026 | 4167 | SPR | 150 | 140 | -10 | Sí | No |
| 9 | 16/10/2026 | 4167 | ROTA | 150 | 150 | 0 | No aplica | Sí |
| 10 | 16/10/2026 | 4167 | HEPB | 200 | 200 | 0 | No aplica | Sí |
| 11 | 16/10/2026 | 4167 | SPR | 60 | 80 | 20 | Sí | No |
| 12 | 16/10/2026 | 4167 | HEPB | 200 | 200 | 0 | No aplica | Sí |
| 13 | 16/10/2026 | 4167 | IPV | 180 | 170 | -10 | Sí | No |
| 14 | 16/10/2026 | 4167 | VARI | 50 | 50 | 0 | No aplica | Sí |
| 15 | 16/10/2026 | 4167 | BCG | 20 | 20 | 0 | No aplica | Sí |
| 16 | 16/10/2026 | 4167 | ROTA | 60 | 60 | 0 | No aplica | Sí |
| 17 | 16/10/2026 | 4167 | DTA | 60 | 60 | 0 | No aplica | Sí |
| 18 | 16/10/2026 | 4167 | DTA | 120 | 120 | 0 | No aplica | Sí |
| 19 | 16/10/2026 | 4167 | DTA | 180 | 180 | 0 | No aplica | Sí |
| 20 | 16/10/2026 | 4167 | ROTA | 60 | 55 | -5 | Sí | No |
| 21 | 16/10/2026 | 4167 | BCG | 20 | 20 | 0 | No aplica | Sí |
| 22 | 16/10/2026 | 4167 | VARI | 100 | 100 | 0 | No aplica | Sí |
| 23 | 16/10/2026 | 4167 | PENT | 60 | 40 | -20 | Sí | No |
| 24 | 16/10/2026 | 4167 | BCG | 150 | 150 | 0 | No aplica | Sí |
| 25 | 16/10/2026 | 4167 | HEPB | 180 | 180 | 0 | No aplica | Sí |

Cierre: 20 entregas concordantes ÷ 25 × 100 = **80.00 %**.

---

### Bloque 21 · TRAB-11 · Pretest (proceso manual) · 07/09/2026

Documentos auditados: 40 · Conformes: 35 · RSD: 87.50 % · Entregas conciliadas: 25 · Concordantes: 13 · CPE: 52.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | DEV | VARI | L-2609-01 | 100 | S | S | S | S | S | S | S | S | S | — |
| 2 | SAL | BCG | L-2609-02 | 100 | S | S | S | S | N | S | S | S | N | M5 |
| 3 | ING | SPR | L-2609-03 | 240 | S | S | S | S | S | S | S | S | S | — |
| 4 | SAL | DTA | L-2609-04 | 80 | S | N | S | S | S | S | S | S | N | M2 |
| 5 | AJU | SPR | L-2609-05 | 240 | S | S | S | S | S | S | S | S | S | — |
| 6 | SAL | BCG | L-2609-06 | 60 | S | S | S | S | S | S | S | S | S | — |
| 7 | DEV | DTA | L-2609-07 | 60 | S | S | S | S | S | S | S | S | S | — |
| 8 | DEV | IPV | L-2609-08 | 200 | S | S | S | S | S | S | S | S | S | — |
| 9 | SAL | INFL | L-2609-09 | 60 | S | S | S | S | S | S | S | S | S | — |
| 10 | DEV | SPR | L-2609-10 | 200 | S | S | S | S | S | S | S | S | S | — |
| 11 | AJU | SPR | L-2609-11 | 100 | S | S | S | S | S | S | S | S | S | — |
| 12 | DEV | INFL | L-2609-12 | 150 | S | S | S | S | S | S | S | S | S | — |
| 13 | TRA | ROTA | L-2609-13 | 300 | S | S | S | S | S | S | S | S | S | — |
| 14 | TRA | HEPB | L-2609-14 | 40 | S | S | S | S | S | S | S | S | S | — |
| 15 | ING | DTA | L-2609-15 | 100 | S | S | S | S | S | N | S | S | N | M6 |
| 16 | DEV | DTA | L-2609-16 | 200 | S | S | S | S | S | S | S | S | S | — |
| 17 | TRA | SPR | L-2609-17 | 240 | S | S | S | S | S | S | S | S | S | — |
| 18 | DEV | HEPB | L-2609-18 | 60 | S | S | S | S | S | S | S | S | S | — |
| 19 | AJU | BCG | L-2609-19 | 100 | S | S | S | S | S | S | S | S | S | — |
| 20 | ING | HEPB | L-2609-20 | 200 | S | S | S | S | S | S | S | S | S | — |
| 21 | SAL | VARI | L-2609-21 | 180 | S | S | S | S | S | S | S | S | S | — |
| 22 | SAL | HEPB | L-2609-22 | 120 | S | S | S | S | S | N | S | S | N | M6 |
| 23 | AJU | HEPB | L-2609-23 | 240 | S | S | S | S | S | S | S | S | S | — |
| 24 | DEV | ROTA | L-2609-24 | 300 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | IPV | L-2609-25 | 240 | S | S | S | S | S | S | S | S | S | — |
| 26 | TRA | SPR | L-2609-26 | 240 | S | S | S | S | S | S | S | S | S | — |
| 27 | AJU | VARI | L-2609-27 | 80 | S | S | S | S | S | S | S | S | S | — |
| 28 | DEV | SPR | L-2609-28 | 20 | S | S | S | S | S | S | S | S | S | — |
| 29 | TRA | PENT | L-2609-29 | 200 | S | S | S | S | S | S | S | S | S | — |
| 30 | AJU | PENT | L-2609-30 | 120 | S | S | N | S | S | S | S | S | N | M3 |
| 31 | DEV | NEUM | L-2609-31 | 200 | S | S | S | S | S | S | S | S | S | — |
| 32 | AJU | PENT | L-2609-32 | 150 | S | S | S | S | S | S | S | S | S | — |
| 33 | AJU | NEUM | L-2609-33 | 20 | S | S | S | S | S | S | S | S | S | — |
| 34 | ING | DTA | L-2609-34 | 40 | S | S | S | S | S | S | S | S | S | — |
| 35 | AJU | VARI | L-2609-35 | 180 | S | S | S | S | S | S | S | S | S | — |
| 36 | AJU | DTA | L-2609-36 | 40 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | ROTA | L-2609-37 | 40 | S | S | S | S | S | S | S | S | S | — |
| 38 | TRA | IPV | L-2609-38 | 120 | S | S | S | S | S | S | S | S | S | — |
| 39 | DEV | BCG | L-2609-39 | 240 | S | S | S | S | S | S | S | S | S | — |
| 40 | DEV | INFL | L-2609-40 | 240 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-11 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 07/09/2026 | 4167-SJ | BCG | 150 | 150 | 0 | No aplica | Sí |
| 2 | 07/09/2026 | 4167-SJ | HEPB | 60 | 60 | 0 | No aplica | Sí |
| 3 | 07/09/2026 | 4167-SJ | PENT | 100 | 100 | 0 | No aplica | Sí |
| 4 | 07/09/2026 | 4167-SJ | SPR | 150 | 150 | 0 | No aplica | Sí |
| 5 | 07/09/2026 | 4167-SJ | DTA | 100 | 80 | -20 | Sí | No |
| 6 | 07/09/2026 | 4167-SJ | IPV | 60 | 40 | -20 | Sí | No |
| 7 | 07/09/2026 | 4167-SJ | PENT | 40 | 30 | -10 | Sí | No |
| 8 | 07/09/2026 | 4167-SJ | ROTA | 200 | 195 | -5 | Sí | No |
| 9 | 07/09/2026 | 4167-SJ | IPV | 80 | 90 | 10 | Sí | No |
| 10 | 07/09/2026 | 4167-SJ | IPV | 60 | 60 | 0 | No aplica | Sí |
| 11 | 07/09/2026 | 4167-SJ | DTA | 200 | 210 | 10 | Sí | No |
| 12 | 07/09/2026 | 4167-SJ | DTA | 50 | 50 | 0 | No aplica | Sí |
| 13 | 07/09/2026 | 4167-SJ | NEUM | 100 | 95 | -5 | Sí | No |
| 14 | 07/09/2026 | 4167-SJ | INFL | 50 | 50 | 0 | No aplica | Sí |
| 15 | 07/09/2026 | 4167-SJ | SPR | 20 | 20 | 0 | No aplica | Sí |
| 16 | 07/09/2026 | 4167-SJ | HEPB | 180 | 180 | 0 | No aplica | Sí |
| 17 | 07/09/2026 | 4167-SJ | DTA | 60 | 60 | 0 | No aplica | Sí |
| 18 | 07/09/2026 | 4167-SJ | BCG | 60 | 60 | 0 | No aplica | Sí |
| 19 | 07/09/2026 | 4167-SJ | DTA | 50 | 60 | 10 | Sí | No |
| 20 | 07/09/2026 | 4167-SJ | HEPB | 180 | 180 | 0 | No aplica | Sí |
| 21 | 07/09/2026 | 4167-SJ | INFL | 120 | 100 | -20 | Sí | No |
| 22 | 07/09/2026 | 4167-SJ | HEPB | 60 | 65 | 5 | Sí | No |
| 23 | 07/09/2026 | 4167-SJ | NEUM | 20 | 10 | -10 | Sí | No |
| 24 | 07/09/2026 | 4167-SJ | BCG | 50 | 70 | 20 | Sí | No |
| 25 | 07/09/2026 | 4167-SJ | DTA | 50 | 50 | 0 | No aplica | Sí |

Cierre: 13 entregas concordantes ÷ 25 × 100 = **52.00 %**.

---

### Bloque 22 · TRAB-11 · Postest (Sistema SIVAC) · 19/10/2026

Documentos auditados: 40 · Conformes: 36 · RSD: 90.00 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | DEV | HEPB | L-2610-01 | 60 | S | S | S | S | S | S | S | S | S | — |
| 2 | AJU | DTA | L-2610-02 | 40 | S | S | S | S | S | S | S | S | S | — |
| 3 | AJU | VARI | L-2610-03 | 20 | S | S | S | S | S | S | S | S | S | — |
| 4 | ING | DTA | L-2610-04 | 200 | S | S | S | S | S | S | S | S | S | — |
| 5 | DEV | PENT | L-2610-05 | 120 | S | S | S | S | S | S | S | S | S | — |
| 6 | SAL | DTA | L-2610-06 | 80 | S | S | S | S | S | S | S | S | S | — |
| 7 | AJU | PENT | L-2610-07 | 20 | S | S | N | S | S | S | S | S | N | M3 |
| 8 | DEV | NEUM | L-2610-08 | 180 | S | S | S | S | S | S | S | S | S | — |
| 9 | TRA | VARI | L-2610-09 | 200 | S | S | S | S | S | S | S | S | S | — |
| 10 | AJU | HEPB | L-2610-10 | 240 | S | S | S | S | S | S | S | S | S | — |
| 11 | ING | SPR | L-2610-11 | 80 | S | S | S | S | S | S | S | S | S | — |
| 12 | AJU | ROTA | L-2610-12 | 240 | S | S | S | S | S | S | S | S | S | — |
| 13 | AJU | VARI | L-2610-13 | 80 | S | S | S | S | S | S | S | S | S | — |
| 14 | TRA | DTA | L-2610-14 | 120 | S | S | S | S | S | S | S | S | S | — |
| 15 | AJU | BCG | L-2610-15 | 100 | S | S | S | S | S | S | S | S | S | — |
| 16 | AJU | ROTA | L-2610-16 | 120 | S | S | S | N | S | S | S | S | N | M4 |
| 17 | TRA | ROTA | L-2610-17 | 150 | S | S | S | S | S | S | S | S | S | — |
| 18 | AJU | VARI | L-2610-18 | 40 | S | S | S | S | S | S | S | S | S | — |
| 19 | ING | BCG | L-2610-19 | 180 | S | S | S | S | S | S | S | S | S | — |
| 20 | SAL | VARI | L-2610-20 | 180 | S | S | N | S | S | S | S | S | N | M3 |
| 21 | SAL | HEPB | L-2610-21 | 20 | S | S | S | S | S | S | S | S | S | — |
| 22 | ING | DTA | L-2610-22 | 100 | S | S | S | S | S | S | S | S | S | — |
| 23 | ING | DTA | L-2610-23 | 80 | S | S | S | S | S | S | S | S | S | — |
| 24 | ING | HEPB | L-2610-24 | 180 | S | S | S | S | S | S | S | S | S | — |
| 25 | AJU | DTA | L-2610-25 | 240 | S | S | S | S | S | S | S | S | S | — |
| 26 | ING | DTA | L-2610-26 | 150 | S | S | S | S | S | S | S | S | S | — |
| 27 | SAL | SPR | L-2610-27 | 240 | S | S | S | S | S | S | S | S | S | — |
| 28 | TRA | VARI | L-2610-28 | 100 | S | S | S | S | S | S | S | S | S | — |
| 29 | TRA | PENT | L-2610-29 | 150 | S | S | S | S | S | S | S | S | S | — |
| 30 | DEV | PENT | L-2610-30 | 120 | S | S | S | S | S | S | S | S | S | — |
| 31 | SAL | IPV | L-2610-31 | 150 | S | S | S | S | S | S | S | S | S | — |
| 32 | AJU | IPV | L-2610-32 | 200 | S | S | S | S | S | S | S | S | S | — |
| 33 | SAL | PENT | L-2610-33 | 120 | S | S | S | S | S | S | S | S | S | — |
| 34 | TRA | DTA | L-2610-34 | 180 | S | S | S | S | S | S | S | S | S | — |
| 35 | SAL | PENT | L-2610-35 | 240 | S | S | N | S | S | S | S | S | N | M3 |
| 36 | ING | DTA | L-2610-36 | 40 | S | S | S | S | S | S | S | S | S | — |
| 37 | TRA | PENT | L-2610-37 | 240 | S | S | S | S | S | S | S | S | S | — |
| 38 | ING | VARI | L-2610-38 | 120 | S | S | S | S | S | S | S | S | S | — |
| 39 | SAL | SPR | L-2610-39 | 80 | S | S | S | S | S | S | S | S | S | — |
| 40 | DEV | IPV | L-2610-40 | 20 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-11 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 19/10/2026 | 4167-SJ | IPV | 60 | 60 | 0 | No aplica | Sí |
| 2 | 19/10/2026 | 4167-SJ | BCG | 180 | 180 | 0 | No aplica | Sí |
| 3 | 19/10/2026 | 4167-SJ | HEPB | 60 | 60 | 0 | No aplica | Sí |
| 4 | 19/10/2026 | 4167-SJ | VARI | 100 | 100 | 0 | No aplica | Sí |
| 5 | 19/10/2026 | 4167-SJ | DTA | 150 | 150 | 0 | No aplica | Sí |
| 6 | 19/10/2026 | 4167-SJ | PENT | 40 | 40 | 0 | No aplica | Sí |
| 7 | 19/10/2026 | 4167-SJ | NEUM | 200 | 200 | 0 | No aplica | Sí |
| 8 | 19/10/2026 | 4167-SJ | PENT | 120 | 120 | 0 | No aplica | Sí |
| 9 | 19/10/2026 | 4167-SJ | INFL | 120 | 120 | 0 | No aplica | Sí |
| 10 | 19/10/2026 | 4167-SJ | SPR | 60 | 60 | 0 | No aplica | Sí |
| 11 | 19/10/2026 | 4167-SJ | ROTA | 30 | 30 | 0 | No aplica | Sí |
| 12 | 19/10/2026 | 4167-SJ | INFL | 200 | 200 | 0 | No aplica | Sí |
| 13 | 19/10/2026 | 4167-SJ | SPR | 40 | 40 | 0 | No aplica | Sí |
| 14 | 19/10/2026 | 4167-SJ | VARI | 180 | 180 | 0 | No aplica | Sí |
| 15 | 19/10/2026 | 4167-SJ | VARI | 200 | 200 | 0 | No aplica | Sí |
| 16 | 19/10/2026 | 4167-SJ | NEUM | 50 | 50 | 0 | No aplica | Sí |
| 17 | 19/10/2026 | 4167-SJ | PENT | 40 | 40 | 0 | No aplica | Sí |
| 18 | 19/10/2026 | 4167-SJ | IPV | 100 | 100 | 0 | No aplica | Sí |
| 19 | 19/10/2026 | 4167-SJ | DTA | 100 | 100 | 0 | No aplica | Sí |
| 20 | 19/10/2026 | 4167-SJ | PENT | 120 | 120 | 0 | No aplica | Sí |
| 21 | 19/10/2026 | 4167-SJ | NEUM | 120 | 120 | 0 | No aplica | Sí |
| 22 | 19/10/2026 | 4167-SJ | DTA | 40 | 40 | 0 | No aplica | Sí |
| 23 | 19/10/2026 | 4167-SJ | SPR | 180 | 180 | 0 | No aplica | Sí |
| 24 | 19/10/2026 | 4167-SJ | IPV | 150 | 150 | 0 | No aplica | Sí |
| 25 | 19/10/2026 | 4167-SJ | DTA | 120 | 125 | 5 | Sí | No |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 23 · TRAB-12 · Pretest (proceso manual) · 07/09/2026

Documentos auditados: 40 · Conformes: 22 · RSD: 55.00 % · Entregas conciliadas: 25 · Concordantes: 15 · CPE: 60.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | SAL | HEPB | L-2609-01 | 60 | S | N | S | S | S | S | S | S | N | M2 |
| 2 | AJU | ROTA | L-2609-02 | 20 | S | S | S | S | S | S | S | S | S | — |
| 3 | ING | VARI | L-2609-03 | 80 | S | S | S | S | S | S | S | S | S | — |
| 4 | TRA | BCG | L-2609-04 | 150 | S | N | S | S | S | S | S | S | N | M2 |
| 5 | SAL | VARI | L-2609-05 | 200 | S | S | S | S | N | S | S | S | N | M5 |
| 6 | SAL | PENT | L-2609-06 | 200 | S | S | S | S | S | S | S | N | N | M8 |
| 7 | ING | BCG | L-2609-07 | 20 | S | S | N | S | S | S | S | S | N | M3 |
| 8 | AJU | VARI | L-2609-08 | 180 | S | S | S | S | S | S | S | S | S | — |
| 9 | SAL | INFL | L-2609-09 | 180 | S | S | S | S | S | S | S | S | S | — |
| 10 | DEV | SPR | L-2609-10 | 180 | S | S | N | S | S | S | S | S | N | M3 |
| 11 | AJU | INFL | L-2609-11 | 80 | S | S | S | S | S | S | S | S | S | — |
| 12 | ING | VARI | L-2609-12 | 200 | S | N | S | S | S | S | S | S | N | M2 |
| 13 | DEV | SPR | L-2609-13 | 120 | S | S | S | S | S | S | S | S | S | — |
| 14 | AJU | SPR | L-2609-14 | 80 | S | S | S | S | S | S | S | S | S | — |
| 15 | TRA | VARI | L-2609-15 | 150 | S | S | S | S | S | S | S | N | N | M8 |
| 16 | SAL | INFL | L-2609-16 | 150 | S | S | S | S | S | S | S | S | S | — |
| 17 | TRA | SPR | L-2609-17 | 300 | S | S | S | S | S | S | S | S | S | — |
| 18 | ING | PENT | L-2609-18 | 180 | S | S | S | S | S | S | S | S | S | — |
| 19 | DEV | SPR | L-2609-19 | 240 | N | S | S | S | S | S | S | S | N | M1 |
| 20 | SAL | DTA | L-2609-20 | 80 | S | N | S | S | S | S | S | S | N | M2 |
| 21 | TRA | NEUM | L-2609-21 | 200 | S | S | S | S | S | N | S | S | N | M6 |
| 22 | SAL | NEUM | L-2609-22 | 300 | S | S | S | S | S | S | S | S | S | — |
| 23 | SAL | DTA | L-2609-23 | 60 | S | S | S | S | S | S | S | S | S | — |
| 24 | TRA | DTA | L-2609-24 | 60 | S | S | S | S | S | S | S | S | S | — |
| 25 | AJU | NEUM | L-2609-25 | 120 | S | S | S | S | S | S | S | S | S | — |
| 26 | SAL | BCG | L-2609-26 | 20 | S | S | S | S | N | S | S | S | N | M5 |
| 27 | ING | INFL | L-2609-27 | 60 | S | S | S | N | S | S | S | S | N | M4 |
| 28 | DEV | HEPB | L-2609-28 | 180 | S | S | S | S | S | S | S | S | S | — |
| 29 | ING | PENT | L-2609-29 | 100 | S | S | S | S | S | S | S | S | S | — |
| 30 | ING | NEUM | L-2609-30 | 20 | S | S | S | S | S | S | S | S | S | — |
| 31 | AJU | BCG | L-2609-31 | 300 | S | S | S | S | S | N | S | S | N | M6 |
| 32 | ING | INFL | L-2609-32 | 240 | S | S | S | S | S | S | S | S | S | — |
| 33 | SAL | IPV | L-2609-33 | 200 | S | S | S | S | S | S | S | S | S | — |
| 34 | ING | VARI | L-2609-34 | 120 | S | S | S | S | S | S | S | S | S | — |
| 35 | DEV | HEPB | L-2609-35 | 40 | S | S | N | S | S | S | S | S | N | M3 |
| 36 | TRA | HEPB | L-2609-36 | 300 | S | S | S | S | S | S | N | S | N | M7 |
| 37 | TRA | ROTA | L-2609-37 | 40 | S | S | S | S | S | S | S | S | S | — |
| 38 | DEV | HEPB | L-2609-38 | 180 | S | S | N | S | S | S | S | S | N | M3 |
| 39 | DEV | IPV | L-2609-39 | 80 | S | N | S | S | S | S | S | S | N | M2 |
| 40 | DEV | DTA | L-2609-40 | 40 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-12 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 07/09/2026 | 4172 | NEUM | 30 | 30 | 0 | No aplica | Sí |
| 2 | 07/09/2026 | 4172 | NEUM | 200 | 220 | 20 | Sí | No |
| 3 | 07/09/2026 | 4172 | HEPB | 40 | 40 | 0 | No aplica | Sí |
| 4 | 07/09/2026 | 4172 | INFL | 40 | 40 | 0 | No aplica | Sí |
| 5 | 07/09/2026 | 4172 | IPV | 20 | 20 | 0 | No aplica | Sí |
| 6 | 07/09/2026 | 4172 | SPR | 100 | 100 | 0 | No aplica | Sí |
| 7 | 07/09/2026 | 4172 | PENT | 100 | 90 | -10 | Sí | No |
| 8 | 07/09/2026 | 4172 | BCG | 80 | 80 | 0 | No aplica | Sí |
| 9 | 07/09/2026 | 4172 | INFL | 200 | 200 | 0 | No aplica | Sí |
| 10 | 07/09/2026 | 4172 | NEUM | 20 | 0 | -20 | Sí | No |
| 11 | 07/09/2026 | 4172 | IPV | 120 | 130 | 10 | Sí | No |
| 12 | 07/09/2026 | 4172 | INFL | 150 | 160 | 10 | Sí | No |
| 13 | 07/09/2026 | 4172 | IPV | 50 | 50 | 0 | No aplica | Sí |
| 14 | 07/09/2026 | 4172 | PENT | 100 | 120 | 20 | Sí | No |
| 15 | 07/09/2026 | 4172 | NEUM | 180 | 180 | 0 | No aplica | Sí |
| 16 | 07/09/2026 | 4172 | HEPB | 30 | 25 | -5 | Sí | No |
| 17 | 07/09/2026 | 4172 | NEUM | 120 | 120 | 0 | No aplica | Sí |
| 18 | 07/09/2026 | 4172 | DTA | 60 | 40 | -20 | Sí | No |
| 19 | 07/09/2026 | 4172 | SPR | 100 | 100 | 0 | No aplica | Sí |
| 20 | 07/09/2026 | 4172 | BCG | 120 | 120 | 0 | No aplica | Sí |
| 21 | 07/09/2026 | 4172 | PENT | 200 | 200 | 0 | No aplica | Sí |
| 22 | 07/09/2026 | 4172 | NEUM | 80 | 90 | 10 | Sí | No |
| 23 | 07/09/2026 | 4172 | BCG | 80 | 80 | 0 | No aplica | Sí |
| 24 | 07/09/2026 | 4172 | ROTA | 180 | 180 | 0 | No aplica | Sí |
| 25 | 07/09/2026 | 4172 | PENT | 30 | 20 | -10 | Sí | No |

Cierre: 15 entregas concordantes ÷ 25 × 100 = **60.00 %**.

---

### Bloque 24 · TRAB-12 · Postest (Sistema SIVAC) · 19/10/2026

Documentos auditados: 40 · Conformes: 39 · RSD: 97.50 % · Entregas conciliadas: 25 · Concordantes: 23 · CPE: 92.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | TRA | SPR | L-2610-01 | 200 | S | S | S | S | S | S | S | S | S | — |
| 2 | DEV | HEPB | L-2610-02 | 40 | S | S | S | S | S | S | S | S | S | — |
| 3 | ING | BCG | L-2610-03 | 80 | S | S | S | S | S | S | N | S | N | M7 |
| 4 | AJU | HEPB | L-2610-04 | 200 | S | S | S | S | S | S | S | S | S | — |
| 5 | DEV | SPR | L-2610-05 | 240 | S | S | S | S | S | S | S | S | S | — |
| 6 | TRA | IPV | L-2610-06 | 40 | S | S | S | S | S | S | S | S | S | — |
| 7 | TRA | IPV | L-2610-07 | 240 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | IPV | L-2610-08 | 100 | S | S | S | S | S | S | S | S | S | — |
| 9 | ING | INFL | L-2610-09 | 150 | S | S | S | S | S | S | S | S | S | — |
| 10 | ING | IPV | L-2610-10 | 100 | S | S | S | S | S | S | S | S | S | — |
| 11 | SAL | BCG | L-2610-11 | 200 | S | S | S | S | S | S | S | S | S | — |
| 12 | ING | DTA | L-2610-12 | 150 | S | S | S | S | S | S | S | S | S | — |
| 13 | DEV | ROTA | L-2610-13 | 40 | S | S | S | S | S | S | S | S | S | — |
| 14 | AJU | PENT | L-2610-14 | 80 | S | S | S | S | S | S | S | S | S | — |
| 15 | DEV | PENT | L-2610-15 | 20 | S | S | S | S | S | S | S | S | S | — |
| 16 | ING | PENT | L-2610-16 | 300 | S | S | S | S | S | S | S | S | S | — |
| 17 | TRA | IPV | L-2610-17 | 300 | S | S | S | S | S | S | S | S | S | — |
| 18 | ING | DTA | L-2610-18 | 60 | S | S | S | S | S | S | S | S | S | — |
| 19 | DEV | BCG | L-2610-19 | 120 | S | S | S | S | S | S | S | S | S | — |
| 20 | AJU | VARI | L-2610-20 | 20 | S | S | S | S | S | S | S | S | S | — |
| 21 | ING | IPV | L-2610-21 | 40 | S | S | S | S | S | S | S | S | S | — |
| 22 | ING | DTA | L-2610-22 | 80 | S | S | S | S | S | S | S | S | S | — |
| 23 | DEV | ROTA | L-2610-23 | 120 | S | S | S | S | S | S | S | S | S | — |
| 24 | AJU | NEUM | L-2610-24 | 100 | S | S | S | S | S | S | S | S | S | — |
| 25 | AJU | PENT | L-2610-25 | 100 | S | S | S | S | S | S | S | S | S | — |
| 26 | TRA | BCG | L-2610-26 | 80 | S | S | S | S | S | S | S | S | S | — |
| 27 | AJU | DTA | L-2610-27 | 20 | S | S | S | S | S | S | S | S | S | — |
| 28 | AJU | BCG | L-2610-28 | 240 | S | S | S | S | S | S | S | S | S | — |
| 29 | ING | NEUM | L-2610-29 | 300 | S | S | S | S | S | S | S | S | S | — |
| 30 | ING | SPR | L-2610-30 | 180 | S | S | S | S | S | S | S | S | S | — |
| 31 | AJU | DTA | L-2610-31 | 20 | S | S | S | S | S | S | S | S | S | — |
| 32 | TRA | VARI | L-2610-32 | 120 | S | S | S | S | S | S | S | S | S | — |
| 33 | AJU | PENT | L-2610-33 | 80 | S | S | S | S | S | S | S | S | S | — |
| 34 | DEV | INFL | L-2610-34 | 180 | S | S | S | S | S | S | S | S | S | — |
| 35 | AJU | SPR | L-2610-35 | 80 | S | S | S | S | S | S | S | S | S | — |
| 36 | ING | VARI | L-2610-36 | 150 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | HEPB | L-2610-37 | 60 | S | S | S | S | S | S | S | S | S | — |
| 38 | DEV | IPV | L-2610-38 | 300 | S | S | S | S | S | S | S | S | S | — |
| 39 | ING | SPR | L-2610-39 | 150 | S | S | S | S | S | S | S | S | S | — |
| 40 | ING | ROTA | L-2610-40 | 40 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-12 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 19/10/2026 | 4172 | IPV | 20 | 20 | 0 | No aplica | Sí |
| 2 | 19/10/2026 | 4172 | HEPB | 80 | 80 | 0 | No aplica | Sí |
| 3 | 19/10/2026 | 4172 | DTA | 80 | 80 | 0 | No aplica | Sí |
| 4 | 19/10/2026 | 4172 | INFL | 40 | 40 | 0 | No aplica | Sí |
| 5 | 19/10/2026 | 4172 | ROTA | 40 | 40 | 0 | No aplica | Sí |
| 6 | 19/10/2026 | 4172 | NEUM | 50 | 50 | 0 | No aplica | Sí |
| 7 | 19/10/2026 | 4172 | IPV | 40 | 40 | 0 | No aplica | Sí |
| 8 | 19/10/2026 | 4172 | SPR | 100 | 110 | 10 | Sí | No |
| 9 | 19/10/2026 | 4172 | IPV | 100 | 100 | 0 | No aplica | Sí |
| 10 | 19/10/2026 | 4172 | ROTA | 200 | 200 | 0 | No aplica | Sí |
| 11 | 19/10/2026 | 4172 | INFL | 60 | 60 | 0 | No aplica | Sí |
| 12 | 19/10/2026 | 4172 | SPR | 20 | 20 | 0 | No aplica | Sí |
| 13 | 19/10/2026 | 4172 | ROTA | 180 | 170 | -10 | Sí | No |
| 14 | 19/10/2026 | 4172 | IPV | 200 | 200 | 0 | No aplica | Sí |
| 15 | 19/10/2026 | 4172 | HEPB | 150 | 150 | 0 | No aplica | Sí |
| 16 | 19/10/2026 | 4172 | IPV | 50 | 50 | 0 | No aplica | Sí |
| 17 | 19/10/2026 | 4172 | HEPB | 150 | 150 | 0 | No aplica | Sí |
| 18 | 19/10/2026 | 4172 | INFL | 180 | 180 | 0 | No aplica | Sí |
| 19 | 19/10/2026 | 4172 | NEUM | 180 | 180 | 0 | No aplica | Sí |
| 20 | 19/10/2026 | 4172 | BCG | 150 | 150 | 0 | No aplica | Sí |
| 21 | 19/10/2026 | 4172 | INFL | 40 | 40 | 0 | No aplica | Sí |
| 22 | 19/10/2026 | 4172 | ROTA | 40 | 40 | 0 | No aplica | Sí |
| 23 | 19/10/2026 | 4172 | IPV | 60 | 60 | 0 | No aplica | Sí |
| 24 | 19/10/2026 | 4172 | PENT | 150 | 150 | 0 | No aplica | Sí |
| 25 | 19/10/2026 | 4172 | PENT | 40 | 40 | 0 | No aplica | Sí |

Cierre: 23 entregas concordantes ÷ 25 × 100 = **92.00 %**.

---

### Bloque 25 · TRAB-13 · Pretest (proceso manual) · 08/09/2026

Documentos auditados: 40 · Conformes: 33 · RSD: 82.50 % · Entregas conciliadas: 25 · Concordantes: 12 · CPE: 48.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | DEV | IPV | L-2609-01 | 240 | S | S | S | S | S | S | S | S | S | — |
| 2 | AJU | BCG | L-2609-02 | 100 | S | N | S | S | S | S | S | S | N | M2 |
| 3 | SAL | ROTA | L-2609-03 | 100 | S | S | S | S | S | S | S | S | S | — |
| 4 | SAL | ROTA | L-2609-04 | 150 | S | S | S | S | S | S | S | S | S | — |
| 5 | ING | BCG | L-2609-05 | 150 | S | S | S | S | S | S | S | S | S | — |
| 6 | ING | SPR | L-2609-06 | 60 | S | S | S | S | S | S | S | S | S | — |
| 7 | TRA | INFL | L-2609-07 | 180 | S | S | S | S | S | S | S | S | S | — |
| 8 | SAL | IPV | L-2609-08 | 120 | S | S | S | S | S | S | S | S | S | — |
| 9 | SAL | SPR | L-2609-09 | 100 | S | S | S | S | S | S | S | S | S | — |
| 10 | ING | PENT | L-2609-10 | 80 | S | S | S | S | S | S | S | S | S | — |
| 11 | TRA | HEPB | L-2609-11 | 240 | S | S | S | S | S | S | S | S | S | — |
| 12 | SAL | NEUM | L-2609-12 | 20 | S | S | S | S | S | S | S | S | S | — |
| 13 | TRA | NEUM | L-2609-13 | 40 | S | S | S | S | S | S | S | S | S | — |
| 14 | SAL | SPR | L-2609-14 | 120 | S | S | S | S | S | S | S | S | S | — |
| 15 | SAL | BCG | L-2609-15 | 150 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | ROTA | L-2609-16 | 120 | S | S | S | S | S | N | S | S | N | M6 |
| 17 | SAL | BCG | L-2609-17 | 60 | S | S | S | S | S | S | S | S | S | — |
| 18 | AJU | NEUM | L-2609-18 | 300 | S | S | S | S | S | S | S | S | S | — |
| 19 | ING | PENT | L-2609-19 | 60 | S | S | S | S | S | S | S | S | S | — |
| 20 | DEV | INFL | L-2609-20 | 240 | S | S | S | S | S | S | S | S | S | — |
| 21 | TRA | INFL | L-2609-21 | 80 | S | S | S | S | S | S | S | S | S | — |
| 22 | AJU | IPV | L-2609-22 | 60 | S | S | S | S | S | S | S | S | S | — |
| 23 | DEV | IPV | L-2609-23 | 40 | S | S | S | N | S | S | S | S | N | M4 |
| 24 | SAL | NEUM | L-2609-24 | 100 | S | S | S | S | S | S | S | S | S | — |
| 25 | TRA | SPR | L-2609-25 | 180 | S | S | S | S | S | N | S | S | N | M6 |
| 26 | TRA | IPV | L-2609-26 | 60 | S | S | S | S | S | S | S | S | S | — |
| 27 | ING | HEPB | L-2609-27 | 80 | S | S | N | S | S | S | S | S | N | M3 |
| 28 | TRA | PENT | L-2609-28 | 300 | S | S | S | S | S | S | S | S | S | — |
| 29 | AJU | INFL | L-2609-29 | 200 | S | S | S | S | S | S | S | S | S | — |
| 30 | SAL | NEUM | L-2609-30 | 40 | S | S | S | S | S | S | S | S | S | — |
| 31 | TRA | SPR | L-2609-31 | 200 | S | S | S | S | S | N | S | S | N | M6 |
| 32 | AJU | INFL | L-2609-32 | 300 | S | S | S | S | S | S | S | S | S | — |
| 33 | SAL | INFL | L-2609-33 | 150 | S | S | S | S | S | S | S | S | S | — |
| 34 | SAL | SPR | L-2609-34 | 100 | S | S | S | S | S | S | S | S | S | — |
| 35 | AJU | NEUM | L-2609-35 | 300 | S | S | S | S | S | S | S | S | S | — |
| 36 | ING | VARI | L-2609-36 | 300 | S | S | S | S | S | S | S | S | S | — |
| 37 | TRA | PENT | L-2609-37 | 240 | S | S | S | S | S | S | S | S | S | — |
| 38 | DEV | SPR | L-2609-38 | 240 | S | N | S | S | S | S | S | S | N | M2 |
| 39 | TRA | VARI | L-2609-39 | 150 | S | S | S | S | S | S | S | S | S | — |
| 40 | SAL | SPR | L-2609-40 | 40 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-13 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 08/09/2026 | 4183 | DTA | 200 | 200 | 0 | No aplica | Sí |
| 2 | 08/09/2026 | 4183 | INFL | 60 | 80 | 20 | Sí | No |
| 3 | 08/09/2026 | 4183 | IPV | 60 | 50 | -10 | Sí | No |
| 4 | 08/09/2026 | 4183 | HEPB | 100 | 100 | 0 | No aplica | Sí |
| 5 | 08/09/2026 | 4183 | ROTA | 180 | 190 | 10 | Sí | No |
| 6 | 08/09/2026 | 4183 | HEPB | 180 | 180 | 0 | No aplica | Sí |
| 7 | 08/09/2026 | 4183 | PENT | 150 | 145 | -5 | Sí | No |
| 8 | 08/09/2026 | 4183 | INFL | 20 | 10 | -10 | Sí | No |
| 9 | 08/09/2026 | 4183 | SPR | 150 | 150 | 0 | No aplica | Sí |
| 10 | 08/09/2026 | 4183 | BCG | 40 | 20 | -20 | Sí | No |
| 11 | 08/09/2026 | 4183 | HEPB | 80 | 80 | 0 | No aplica | Sí |
| 12 | 08/09/2026 | 4183 | ROTA | 50 | 70 | 20 | Sí | No |
| 13 | 08/09/2026 | 4183 | INFL | 100 | 100 | 0 | No aplica | Sí |
| 14 | 08/09/2026 | 4183 | PENT | 50 | 40 | -10 | Sí | No |
| 15 | 08/09/2026 | 4183 | DTA | 180 | 180 | 0 | No aplica | Sí |
| 16 | 08/09/2026 | 4183 | PENT | 180 | 180 | 0 | No aplica | Sí |
| 17 | 08/09/2026 | 4183 | ROTA | 50 | 30 | -20 | Sí | No |
| 18 | 08/09/2026 | 4183 | DTA | 80 | 80 | 0 | No aplica | Sí |
| 19 | 08/09/2026 | 4183 | NEUM | 120 | 100 | -20 | Sí | No |
| 20 | 08/09/2026 | 4183 | DTA | 20 | 30 | 10 | Sí | No |
| 21 | 08/09/2026 | 4183 | DTA | 180 | 170 | -10 | Sí | No |
| 22 | 08/09/2026 | 4183 | NEUM | 150 | 150 | 0 | No aplica | Sí |
| 23 | 08/09/2026 | 4183 | SPR | 100 | 100 | 0 | No aplica | Sí |
| 24 | 08/09/2026 | 4183 | BCG | 40 | 40 | 0 | No aplica | Sí |
| 25 | 08/09/2026 | 4183 | SPR | 180 | 175 | -5 | Sí | No |

Cierre: 12 entregas concordantes ÷ 25 × 100 = **48.00 %**.

---

### Bloque 26 · TRAB-13 · Postest (Sistema SIVAC) · 20/10/2026

Documentos auditados: 40 · Conformes: 34 · RSD: 85.00 % · Entregas conciliadas: 25 · Concordantes: 24 · CPE: 96.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | TRA | NEUM | L-2610-01 | 20 | S | S | S | S | S | S | S | S | S | — |
| 2 | TRA | HEPB | L-2610-02 | 60 | S | S | S | S | S | S | S | S | S | — |
| 3 | DEV | IPV | L-2610-03 | 40 | S | S | S | S | S | S | S | S | S | — |
| 4 | TRA | VARI | L-2610-04 | 40 | S | S | S | S | S | S | S | S | S | — |
| 5 | DEV | SPR | L-2610-05 | 100 | S | S | S | S | S | S | S | S | S | — |
| 6 | SAL | IPV | L-2610-06 | 180 | S | S | S | S | S | S | S | S | S | — |
| 7 | ING | PENT | L-2610-07 | 60 | S | S | S | S | S | S | S | S | S | — |
| 8 | AJU | BCG | L-2610-08 | 40 | S | S | S | S | S | S | S | S | S | — |
| 9 | TRA | SPR | L-2610-09 | 240 | S | S | S | S | S | S | S | S | S | — |
| 10 | DEV | HEPB | L-2610-10 | 180 | S | S | S | S | S | S | S | S | S | — |
| 11 | SAL | VARI | L-2610-11 | 180 | S | S | S | S | S | S | S | S | S | — |
| 12 | AJU | DTA | L-2610-12 | 240 | S | S | S | S | S | S | S | S | S | — |
| 13 | DEV | DTA | L-2610-13 | 100 | S | S | S | S | S | N | S | S | N | M6 |
| 14 | AJU | SPR | L-2610-14 | 20 | S | S | S | S | S | S | S | S | S | — |
| 15 | AJU | BCG | L-2610-15 | 300 | S | N | S | S | S | S | S | S | N | M2 |
| 16 | SAL | PENT | L-2610-16 | 200 | S | S | S | S | S | S | S | S | S | — |
| 17 | AJU | PENT | L-2610-17 | 200 | S | S | S | S | S | S | S | S | S | — |
| 18 | TRA | VARI | L-2610-18 | 180 | S | S | S | S | S | S | S | S | S | — |
| 19 | AJU | INFL | L-2610-19 | 200 | S | S | S | S | S | S | S | S | S | — |
| 20 | SAL | PENT | L-2610-20 | 180 | S | S | S | S | S | S | S | S | S | — |
| 21 | SAL | VARI | L-2610-21 | 120 | S | S | S | S | S | S | S | S | S | — |
| 22 | DEV | HEPB | L-2610-22 | 100 | S | S | S | S | S | S | S | S | S | — |
| 23 | TRA | INFL | L-2610-23 | 300 | S | S | S | S | S | S | S | S | S | — |
| 24 | AJU | PENT | L-2610-24 | 60 | S | S | N | S | S | S | S | S | N | M3 |
| 25 | ING | IPV | L-2610-25 | 300 | S | S | S | S | S | S | S | S | S | — |
| 26 | SAL | NEUM | L-2610-26 | 100 | S | S | S | S | S | S | S | S | S | — |
| 27 | SAL | IPV | L-2610-27 | 20 | S | S | S | S | S | S | S | S | S | — |
| 28 | TRA | IPV | L-2610-28 | 240 | S | S | S | S | S | S | S | S | S | — |
| 29 | ING | DTA | L-2610-29 | 80 | S | S | S | S | S | S | S | S | S | — |
| 30 | TRA | DTA | L-2610-30 | 40 | S | S | S | S | S | S | S | S | S | — |
| 31 | AJU | PENT | L-2610-31 | 60 | S | S | S | S | S | S | S | S | S | — |
| 32 | AJU | INFL | L-2610-32 | 200 | S | N | S | S | S | S | S | S | N | M2 |
| 33 | ING | NEUM | L-2610-33 | 100 | S | S | S | S | S | S | S | S | S | — |
| 34 | AJU | BCG | L-2610-34 | 40 | S | S | S | S | S | S | S | S | S | — |
| 35 | AJU | VARI | L-2610-35 | 80 | N | S | S | S | S | S | S | S | N | M1 |
| 36 | AJU | SPR | L-2610-36 | 200 | S | S | S | S | S | S | S | S | S | — |
| 37 | AJU | VARI | L-2610-37 | 80 | S | S | S | S | S | S | S | S | S | — |
| 38 | AJU | INFL | L-2610-38 | 300 | S | S | S | S | S | S | S | S | S | — |
| 39 | AJU | BCG | L-2610-39 | 300 | S | S | S | N | S | S | S | S | N | M4 |
| 40 | AJU | SPR | L-2610-40 | 20 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-13 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 20/10/2026 | 4183 | DTA | 200 | 200 | 0 | No aplica | Sí |
| 2 | 20/10/2026 | 4183 | IPV | 20 | 20 | 0 | No aplica | Sí |
| 3 | 20/10/2026 | 4183 | DTA | 100 | 100 | 0 | No aplica | Sí |
| 4 | 20/10/2026 | 4183 | BCG | 80 | 80 | 0 | No aplica | Sí |
| 5 | 20/10/2026 | 4183 | IPV | 100 | 100 | 0 | No aplica | Sí |
| 6 | 20/10/2026 | 4183 | DTA | 80 | 80 | 0 | No aplica | Sí |
| 7 | 20/10/2026 | 4183 | PENT | 40 | 40 | 0 | No aplica | Sí |
| 8 | 20/10/2026 | 4183 | HEPB | 20 | 20 | 0 | No aplica | Sí |
| 9 | 20/10/2026 | 4183 | PENT | 60 | 60 | 0 | No aplica | Sí |
| 10 | 20/10/2026 | 4183 | VARI | 30 | 30 | 0 | No aplica | Sí |
| 11 | 20/10/2026 | 4183 | NEUM | 50 | 50 | 0 | No aplica | Sí |
| 12 | 20/10/2026 | 4183 | BCG | 200 | 200 | 0 | No aplica | Sí |
| 13 | 20/10/2026 | 4183 | ROTA | 80 | 80 | 0 | No aplica | Sí |
| 14 | 20/10/2026 | 4183 | BCG | 200 | 200 | 0 | No aplica | Sí |
| 15 | 20/10/2026 | 4183 | NEUM | 120 | 120 | 0 | No aplica | Sí |
| 16 | 20/10/2026 | 4183 | PENT | 20 | 20 | 0 | No aplica | Sí |
| 17 | 20/10/2026 | 4183 | BCG | 40 | 40 | 0 | No aplica | Sí |
| 18 | 20/10/2026 | 4183 | BCG | 100 | 100 | 0 | No aplica | Sí |
| 19 | 20/10/2026 | 4183 | INFL | 60 | 60 | 0 | No aplica | Sí |
| 20 | 20/10/2026 | 4183 | PENT | 180 | 180 | 0 | No aplica | Sí |
| 21 | 20/10/2026 | 4183 | DTA | 150 | 150 | 0 | No aplica | Sí |
| 22 | 20/10/2026 | 4183 | BCG | 200 | 200 | 0 | No aplica | Sí |
| 23 | 20/10/2026 | 4183 | NEUM | 120 | 120 | 0 | No aplica | Sí |
| 24 | 20/10/2026 | 4183 | IPV | 80 | 80 | 0 | No aplica | Sí |
| 25 | 20/10/2026 | 4183 | VARI | 180 | 200 | 20 | Sí | No |

Cierre: 24 entregas concordantes ÷ 25 × 100 = **96.00 %**.

---

### Bloque 27 · TRAB-14 · Pretest (proceso manual) · 08/09/2026

Documentos auditados: 40 · Conformes: 27 · RSD: 67.50 % · Entregas conciliadas: 25 · Concordantes: 17 · CPE: 68.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | SAL | HEPB | L-2609-01 | 40 | S | S | S | S | S | S | S | S | S | — |
| 2 | AJU | BCG | L-2609-02 | 20 | S | S | S | S | S | S | S | S | S | — |
| 3 | DEV | HEPB | L-2609-03 | 120 | S | S | S | S | S | S | S | S | S | — |
| 4 | DEV | BCG | L-2609-04 | 60 | S | N | S | S | S | S | S | S | N | M2 |
| 5 | TRA | VARI | L-2609-05 | 80 | S | S | S | S | S | S | S | S | S | — |
| 6 | TRA | HEPB | L-2609-06 | 180 | S | S | S | S | S | S | S | S | S | — |
| 7 | TRA | DTA | L-2609-07 | 240 | S | S | S | S | S | S | S | S | S | — |
| 8 | ING | SPR | L-2609-08 | 180 | S | S | S | S | S | S | S | S | S | — |
| 9 | SAL | BCG | L-2609-09 | 120 | S | S | S | S | S | S | S | S | S | — |
| 10 | TRA | VARI | L-2609-10 | 200 | S | S | S | S | S | S | S | N | N | M8 |
| 11 | SAL | IPV | L-2609-11 | 200 | S | S | S | S | N | S | S | S | N | M5 |
| 12 | DEV | HEPB | L-2609-12 | 120 | S | S | S | S | S | S | S | S | S | — |
| 13 | ING | NEUM | L-2609-13 | 200 | S | S | S | S | S | N | S | S | N | M6 |
| 14 | DEV | BCG | L-2609-14 | 60 | S | S | S | S | S | S | S | S | S | — |
| 15 | TRA | SPR | L-2609-15 | 100 | S | N | S | S | S | S | S | S | N | M2 |
| 16 | ING | VARI | L-2609-16 | 200 | S | S | S | S | S | S | S | S | S | — |
| 17 | TRA | IPV | L-2609-17 | 40 | S | S | S | S | N | S | S | S | N | M5 |
| 18 | TRA | BCG | L-2609-18 | 100 | S | S | S | S | N | S | S | S | N | M5 |
| 19 | AJU | IPV | L-2609-19 | 40 | S | S | S | S | S | S | S | S | S | — |
| 20 | AJU | ROTA | L-2609-20 | 100 | S | S | S | S | S | S | S | S | S | — |
| 21 | AJU | NEUM | L-2609-21 | 60 | S | S | S | S | S | S | S | S | S | — |
| 22 | SAL | ROTA | L-2609-22 | 180 | S | S | S | S | S | S | S | S | S | — |
| 23 | TRA | PENT | L-2609-23 | 150 | S | S | S | S | N | S | S | S | N | M5 |
| 24 | SAL | IPV | L-2609-24 | 20 | S | S | S | S | S | S | S | S | S | — |
| 25 | DEV | HEPB | L-2609-25 | 120 | N | S | S | S | S | S | S | S | N | M1 |
| 26 | TRA | NEUM | L-2609-26 | 80 | S | S | S | S | S | S | S | S | S | — |
| 27 | AJU | PENT | L-2609-27 | 100 | S | S | S | S | S | S | S | S | S | — |
| 28 | ING | VARI | L-2609-28 | 240 | S | S | S | S | S | S | S | S | S | — |
| 29 | SAL | HEPB | L-2609-29 | 20 | S | S | S | S | S | S | N | S | N | M7 |
| 30 | TRA | DTA | L-2609-30 | 300 | S | S | S | N | S | S | S | S | N | M4 |
| 31 | ING | HEPB | L-2609-31 | 150 | S | S | S | S | S | S | S | S | S | — |
| 32 | SAL | SPR | L-2609-32 | 80 | S | S | S | S | S | S | S | S | S | — |
| 33 | DEV | SPR | L-2609-33 | 100 | S | S | S | S | S | S | S | S | S | — |
| 34 | AJU | SPR | L-2609-34 | 240 | S | S | S | S | S | S | S | S | S | — |
| 35 | AJU | BCG | L-2609-35 | 240 | S | S | S | S | S | S | S | S | S | — |
| 36 | SAL | INFL | L-2609-36 | 20 | S | S | S | S | S | S | S | S | S | — |
| 37 | SAL | ROTA | L-2609-37 | 40 | S | S | S | S | S | S | S | S | S | — |
| 38 | SAL | BCG | L-2609-38 | 120 | N | S | S | S | S | S | S | S | N | M1 |
| 39 | ING | SPR | L-2609-39 | 300 | S | N | S | S | S | S | S | S | N | M2 |
| 40 | SAL | DTA | L-2609-40 | 200 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-14 · Pretest (proceso manual)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 08/09/2026 | 4195 | PENT | 50 | 50 | 0 | No aplica | Sí |
| 2 | 08/09/2026 | 4195 | PENT | 40 | 40 | 0 | No aplica | Sí |
| 3 | 08/09/2026 | 4195 | INFL | 40 | 40 | 0 | No aplica | Sí |
| 4 | 08/09/2026 | 4195 | NEUM | 80 | 70 | -10 | Sí | No |
| 5 | 08/09/2026 | 4195 | VARI | 30 | 30 | 0 | No aplica | Sí |
| 6 | 08/09/2026 | 4195 | VARI | 120 | 120 | 0 | No aplica | Sí |
| 7 | 08/09/2026 | 4195 | ROTA | 40 | 40 | 0 | No aplica | Sí |
| 8 | 08/09/2026 | 4195 | HEPB | 100 | 100 | 0 | No aplica | Sí |
| 9 | 08/09/2026 | 4195 | DTA | 80 | 75 | -5 | Sí | No |
| 10 | 08/09/2026 | 4195 | VARI | 20 | 20 | 0 | No aplica | Sí |
| 11 | 08/09/2026 | 4195 | HEPB | 30 | 30 | 0 | No aplica | Sí |
| 12 | 08/09/2026 | 4195 | NEUM | 40 | 40 | 0 | No aplica | Sí |
| 13 | 08/09/2026 | 4195 | NEUM | 30 | 30 | 0 | No aplica | Sí |
| 14 | 08/09/2026 | 4195 | ROTA | 120 | 110 | -10 | Sí | No |
| 15 | 08/09/2026 | 4195 | ROTA | 60 | 60 | 0 | No aplica | Sí |
| 16 | 08/09/2026 | 4195 | IPV | 180 | 180 | 0 | No aplica | Sí |
| 17 | 08/09/2026 | 4195 | BCG | 40 | 60 | 20 | Sí | No |
| 18 | 08/09/2026 | 4195 | INFL | 40 | 30 | -10 | Sí | No |
| 19 | 08/09/2026 | 4195 | PENT | 120 | 120 | 0 | No aplica | Sí |
| 20 | 08/09/2026 | 4195 | NEUM | 40 | 35 | -5 | Sí | No |
| 21 | 08/09/2026 | 4195 | INFL | 120 | 120 | 0 | No aplica | Sí |
| 22 | 08/09/2026 | 4195 | DTA | 120 | 110 | -10 | Sí | No |
| 23 | 08/09/2026 | 4195 | BCG | 50 | 45 | -5 | Sí | No |
| 24 | 08/09/2026 | 4195 | NEUM | 20 | 20 | 0 | No aplica | Sí |
| 25 | 08/09/2026 | 4195 | BCG | 40 | 40 | 0 | No aplica | Sí |

Cierre: 17 entregas concordantes ÷ 25 × 100 = **68.00 %**.

---

### Bloque 28 · TRAB-14 · Postest (Sistema SIVAC) · 20/10/2026

Documentos auditados: 40 · Conformes: 34 · RSD: 85.00 % · Entregas conciliadas: 25 · Concordantes: 21 · CPE: 84.00 %

| Doc | Tipo | Biol. | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | DEV | BCG | L-2610-01 | 200 | S | S | S | S | S | S | S | S | S | — |
| 2 | DEV | PENT | L-2610-02 | 60 | S | S | S | S | S | S | S | S | S | — |
| 3 | SAL | IPV | L-2610-03 | 120 | S | S | S | S | S | S | S | S | S | — |
| 4 | ING | BCG | L-2610-04 | 300 | S | S | S | S | S | S | S | S | S | — |
| 5 | AJU | PENT | L-2610-05 | 20 | S | S | S | S | S | S | S | S | S | — |
| 6 | AJU | HEPB | L-2610-06 | 180 | S | S | S | S | S | S | S | S | S | — |
| 7 | TRA | INFL | L-2610-07 | 180 | S | S | S | S | S | S | S | S | S | — |
| 8 | AJU | NEUM | L-2610-08 | 100 | S | S | S | S | S | S | S | S | S | — |
| 9 | AJU | NEUM | L-2610-09 | 180 | S | S | S | S | S | S | S | S | S | — |
| 10 | DEV | IPV | L-2610-10 | 180 | N | S | S | S | S | S | S | S | N | M1 |
| 11 | SAL | HEPB | L-2610-11 | 300 | S | S | S | S | S | S | S | S | S | — |
| 12 | AJU | NEUM | L-2610-12 | 20 | S | S | S | S | S | S | S | S | S | — |
| 13 | AJU | NEUM | L-2610-13 | 240 | S | S | S | S | S | S | S | N | N | M8 |
| 14 | AJU | IPV | L-2610-14 | 240 | S | S | S | S | S | S | S | S | S | — |
| 15 | SAL | DTA | L-2610-15 | 100 | S | S | S | S | S | S | S | S | S | — |
| 16 | SAL | VARI | L-2610-16 | 300 | S | S | S | S | S | S | S | S | S | — |
| 17 | AJU | SPR | L-2610-17 | 80 | S | S | S | S | S | S | S | S | S | — |
| 18 | SAL | VARI | L-2610-18 | 40 | S | S | S | S | S | S | S | S | S | — |
| 19 | AJU | HEPB | L-2610-19 | 120 | S | S | S | S | S | S | S | S | S | — |
| 20 | TRA | SPR | L-2610-20 | 120 | S | S | S | S | S | S | S | S | S | — |
| 21 | SAL | INFL | L-2610-21 | 20 | S | S | S | S | S | S | S | S | S | — |
| 22 | TRA | SPR | L-2610-22 | 150 | S | S | S | S | S | S | S | S | S | — |
| 23 | ING | VARI | L-2610-23 | 180 | S | S | S | S | S | S | S | S | S | — |
| 24 | SAL | IPV | L-2610-24 | 150 | S | S | S | S | S | S | S | S | S | — |
| 25 | SAL | IPV | L-2610-25 | 40 | S | S | N | S | S | S | S | S | N | M3 |
| 26 | SAL | HEPB | L-2610-26 | 240 | S | S | S | S | S | S | S | S | S | — |
| 27 | DEV | BCG | L-2610-27 | 100 | S | S | S | S | S | S | S | S | S | — |
| 28 | TRA | SPR | L-2610-28 | 240 | S | S | S | S | S | S | S | S | S | — |
| 29 | ING | BCG | L-2610-29 | 80 | S | S | S | S | S | S | S | S | S | — |
| 30 | DEV | IPV | L-2610-30 | 20 | S | S | S | S | S | S | S | S | S | — |
| 31 | SAL | INFL | L-2610-31 | 60 | S | N | S | S | S | S | S | S | N | M2 |
| 32 | AJU | ROTA | L-2610-32 | 200 | S | S | S | S | S | S | S | S | S | — |
| 33 | AJU | PENT | L-2610-33 | 100 | S | S | S | S | S | S | S | S | S | — |
| 34 | TRA | NEUM | L-2610-34 | 300 | S | S | S | S | S | S | S | S | S | — |
| 35 | ING | VARI | L-2610-35 | 200 | S | S | S | S | S | S | S | S | S | — |
| 36 | TRA | BCG | L-2610-36 | 20 | S | S | S | S | S | S | N | S | N | M7 |
| 37 | SAL | VARI | L-2610-37 | 120 | S | S | S | S | S | S | S | S | S | — |
| 38 | TRA | PENT | L-2610-38 | 20 | S | S | S | S | S | S | S | S | S | — |
| 39 | SAL | IPV | L-2610-39 | 150 | S | S | N | S | S | S | S | S | N | M3 |
| 40 | SAL | IPV | L-2610-40 | 180 | S | S | S | S | S | S | S | S | S | — |

**Entregas conciliadas — TRAB-14 · Postest (Sistema SIVAC)**

| N.º | Fecha | Centro | Biol. | Prog. | Entr. | Dif. | Doc. | Conc. |
| :---: | :---: | :---: | :---: | ---: | ---: | ---: | :---: | :---: |
| 1 | 20/10/2026 | 4195 | ROTA | 40 | 40 | 0 | No aplica | Sí |
| 2 | 20/10/2026 | 4195 | NEUM | 180 | 185 | 5 | Sí | No |
| 3 | 20/10/2026 | 4195 | SPR | 200 | 200 | 0 | No aplica | Sí |
| 4 | 20/10/2026 | 4195 | PENT | 120 | 120 | 0 | No aplica | Sí |
| 5 | 20/10/2026 | 4195 | NEUM | 200 | 200 | 0 | No aplica | Sí |
| 6 | 20/10/2026 | 4195 | IPV | 80 | 80 | 0 | No aplica | Sí |
| 7 | 20/10/2026 | 4195 | DTA | 60 | 80 | 20 | Sí | No |
| 8 | 20/10/2026 | 4195 | IPV | 150 | 150 | 0 | No aplica | Sí |
| 9 | 20/10/2026 | 4195 | IPV | 200 | 200 | 0 | No aplica | Sí |
| 10 | 20/10/2026 | 4195 | SPR | 60 | 60 | 0 | No aplica | Sí |
| 11 | 20/10/2026 | 4195 | DTA | 200 | 200 | 0 | No aplica | Sí |
| 12 | 20/10/2026 | 4195 | IPV | 40 | 40 | 0 | No aplica | Sí |
| 13 | 20/10/2026 | 4195 | ROTA | 180 | 180 | 0 | No aplica | Sí |
| 14 | 20/10/2026 | 4195 | SPR | 120 | 120 | 0 | No aplica | Sí |
| 15 | 20/10/2026 | 4195 | IPV | 180 | 180 | 0 | No aplica | Sí |
| 16 | 20/10/2026 | 4195 | DTA | 180 | 180 | 0 | No aplica | Sí |
| 17 | 20/10/2026 | 4195 | INFL | 20 | 20 | 0 | No aplica | Sí |
| 18 | 20/10/2026 | 4195 | DTA | 120 | 100 | -20 | Sí | No |
| 19 | 20/10/2026 | 4195 | DTA | 200 | 200 | 0 | No aplica | Sí |
| 20 | 20/10/2026 | 4195 | ROTA | 20 | 20 | 0 | No aplica | Sí |
| 21 | 20/10/2026 | 4195 | BCG | 200 | 195 | -5 | Sí | No |
| 22 | 20/10/2026 | 4195 | HEPB | 200 | 200 | 0 | No aplica | Sí |
| 23 | 20/10/2026 | 4195 | DTA | 20 | 20 | 0 | No aplica | Sí |
| 24 | 20/10/2026 | 4195 | INFL | 120 | 120 | 0 | No aplica | Sí |
| 25 | 20/10/2026 | 4195 | PENT | 30 | 30 | 0 | No aplica | Sí |

Cierre: 21 entregas concordantes ÷ 25 × 100 = **84.00 %**.

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
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| TRAB-01 | Pretest | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 3 | 8 | 9 | 17 | Bajo |
| TRAB-01 | Postest | 4 | 4 | 5 | 4 | 4 | 4 | 5 | 5 | 17 | 18 | 35 | Alto |
| TRAB-02 | Pretest | 2 | 2 | 2 | 3 | 2 | 2 | 3 | 3 | 9 | 10 | 19 | Medio |
| TRAB-02 | Postest | 3 | 4 | 4 | 4 | 3 | 4 | 4 | 4 | 15 | 15 | 30 | Alto |
| TRAB-03 | Pretest | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 3 | 8 | 9 | 17 | Bajo |
| TRAB-03 | Postest | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 20 | 20 | 40 | Alto |
| TRAB-04 | Pretest | 3 | 3 | 3 | 4 | 3 | 3 | 4 | 4 | 13 | 14 | 27 | Medio |
| TRAB-04 | Postest | 3 | 4 | 4 | 4 | 3 | 4 | 4 | 4 | 15 | 15 | 30 | Alto |
| TRAB-05 | Pretest | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 7 | 8 | 15 | Bajo |
| TRAB-05 | Postest | 4 | 4 | 4 | 4 | 3 | 4 | 4 | 4 | 16 | 15 | 31 | Alto |
| TRAB-06 | Pretest | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 6 | 8 | 14 | Bajo |
| TRAB-06 | Postest | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 20 | 20 | 40 | Alto |
| TRAB-07 | Pretest | 2 | 2 | 2 | 3 | 3 | 2 | 2 | 2 | 9 | 9 | 18 | Bajo |
| TRAB-07 | Postest | 4 | 4 | 5 | 5 | 4 | 4 | 4 | 5 | 18 | 17 | 35 | Alto |
| TRAB-08 | Pretest | 1 | 1 | 2 | 1 | 1 | 2 | 2 | 2 | 5 | 7 | 12 | Bajo |
| TRAB-08 | Postest | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 20 | 20 | 40 | Alto |
| TRAB-09 | Pretest | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 7 | 8 | 15 | Bajo |
| TRAB-09 | Postest | 4 | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 18 | 20 | 38 | Alto |
| TRAB-10 | Pretest | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 4 | 5 | 9 | Bajo |
| TRAB-10 | Postest | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 20 | 20 | 40 | Alto |
| TRAB-11 | Pretest | 1 | 3 | 3 | 3 | 2 | 2 | 3 | 3 | 10 | 10 | 20 | Medio |
| TRAB-11 | Postest | 3 | 4 | 4 | 4 | 3 | 4 | 4 | 4 | 15 | 15 | 30 | Alto |
| TRAB-12 | Pretest | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 3 | 8 | 9 | 17 | Bajo |
| TRAB-12 | Postest | 4 | 4 | 4 | 5 | 4 | 4 | 4 | 5 | 17 | 17 | 34 | Alto |
| TRAB-13 | Pretest | 2 | 3 | 3 | 3 | 2 | 3 | 3 | 3 | 11 | 11 | 22 | Medio |
| TRAB-13 | Postest | 2 | 3 | 3 | 3 | 4 | 4 | 4 | 5 | 11 | 17 | 28 | Medio |
| TRAB-14 | Pretest | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 3 | 8 | 9 | 17 | Bajo |
| TRAB-14 | Postest | 4 | 4 | 4 | 5 | 4 | 5 | 5 | 5 | 17 | 19 | 36 | Alto |

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
| TRAB-01 | 74.00 | 30.50 | 65.00 | 84.00 | 8.00 | 9.00 | 17.00 |
| TRAB-02 | 69.00 | 28.50 | 75.00 | 64.00 | 9.00 | 10.00 | 19.00 |
| TRAB-03 | 86.00 | 26.00 | 60.00 | 56.00 | 8.00 | 9.00 | 17.00 |
| TRAB-04 | 79.00 | 31.00 | 57.50 | 64.00 | 13.00 | 14.00 | 27.00 |
| TRAB-05 | 65.00 | 34.00 | 45.00 | 84.00 | 7.00 | 8.00 | 15.00 |
| TRAB-06 | 72.00 | 27.00 | 52.50 | 72.00 | 6.00 | 8.00 | 14.00 |
| TRAB-07 | 94.00 | 29.50 | 62.50 | 80.00 | 9.00 | 9.00 | 18.00 |
| TRAB-08 | 61.00 | 35.50 | 70.00 | 68.00 | 5.00 | 7.00 | 12.00 |
| TRAB-09 | 76.00 | 25.00 | 47.50 | 76.00 | 7.00 | 8.00 | 15.00 |
| TRAB-10 | 57.00 | 30.00 | 62.50 | 72.00 | 4.00 | 5.00 | 9.00 |
| TRAB-11 | 83.00 | 22.50 | 87.50 | 52.00 | 10.00 | 10.00 | 20.00 |
| TRAB-12 | 90.00 | 28.00 | 55.00 | 60.00 | 8.00 | 9.00 | 17.00 |
| TRAB-13 | 55.00 | 34.50 | 82.50 | 48.00 | 11.00 | 11.00 | 22.00 |
| TRAB-14 | 89.00 | 24.00 | 67.50 | 68.00 | 8.00 | 9.00 | 17.00 |

*Nota.* Mediciones de línea base (pretest). T_reg y T_vale expresados en minutos; RSD y CPE en porcentaje (%); AP, UP y TAM en puntos de escala. Elaboración propia.

### Matriz 6.2 — Postest

| Sujeto | T_reg | T_vale | RSD | CPE | AP | UP | TAM |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TRAB-01 | 5.40 | 0.50 | 90.00 | 88.00 | 17.00 | 18.00 | 35.00 |
| TRAB-02 | 5.10 | 0.47 | 87.50 | 92.00 | 15.00 | 15.00 | 30.00 |
| TRAB-03 | 7.20 | 0.38 | 92.50 | 96.00 | 20.00 | 20.00 | 40.00 |
| TRAB-04 | 6.60 | 0.55 | 95.00 | 92.00 | 15.00 | 15.00 | 30.00 |
| TRAB-05 | 4.80 | 0.90 | 97.50 | 88.00 | 16.00 | 15.00 | 31.00 |
| TRAB-06 | 5.70 | 0.43 | 95.00 | 80.00 | 20.00 | 20.00 | 40.00 |
| TRAB-07 | 7.80 | 0.65 | 92.50 | 84.00 | 18.00 | 17.00 | 35.00 |
| TRAB-08 | 4.50 | 0.78 | 87.50 | 88.00 | 20.00 | 20.00 | 40.00 |
| TRAB-09 | 6.30 | 0.33 | 100.00 | 84.00 | 18.00 | 20.00 | 38.00 |
| TRAB-10 | 4.20 | 0.52 | 92.50 | 80.00 | 20.00 | 20.00 | 40.00 |
| TRAB-11 | 6.90 | 0.23 | 90.00 | 96.00 | 15.00 | 15.00 | 30.00 |
| TRAB-12 | 7.50 | 0.60 | 97.50 | 92.00 | 17.00 | 17.00 | 34.00 |
| TRAB-13 | 5.95 | 0.72 | 85.00 | 96.00 | 11.00 | 17.00 | 28.00 |
| TRAB-14 | 6.05 | 0.28 | 85.00 | 84.00 | 17.00 | 19.00 | 36.00 |

*Nota.* Mediciones finales (postest). T_reg y T_vale corresponden a la media de tres réplicas por unidad experimental. Elaboración propia.

### Matriz 6.3 — Diferencias pareadas (postest − pretest)

| Sujeto | T_reg | T_vale | RSD | CPE | AP | UP | TAM |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TRAB-01 | -68.60 | -30.00 | 25.00 | 4.00 | 9.00 | 9.00 | 18.00 |
| TRAB-02 | -63.90 | -28.03 | 12.50 | 28.00 | 6.00 | 5.00 | 11.00 |
| TRAB-03 | -78.80 | -25.62 | 32.50 | 40.00 | 12.00 | 11.00 | 23.00 |
| TRAB-04 | -72.40 | -30.45 | 37.50 | 28.00 | 2.00 | 1.00 | 3.00 |
| TRAB-05 | -60.20 | -33.10 | 52.50 | 4.00 | 9.00 | 7.00 | 16.00 |
| TRAB-06 | -66.30 | -26.57 | 42.50 | 8.00 | 14.00 | 12.00 | 26.00 |
| TRAB-07 | -86.20 | -28.85 | 30.00 | 4.00 | 9.00 | 8.00 | 17.00 |
| TRAB-08 | -56.50 | -34.72 | 17.50 | 20.00 | 15.00 | 13.00 | 28.00 |
| TRAB-09 | -69.70 | -24.67 | 52.50 | 8.00 | 11.00 | 12.00 | 23.00 |
| TRAB-10 | -52.80 | -29.48 | 30.00 | 8.00 | 16.00 | 15.00 | 31.00 |
| TRAB-11 | -76.10 | -22.27 | 2.50 | 44.00 | 5.00 | 5.00 | 10.00 |
| TRAB-12 | -82.50 | -27.40 | 42.50 | 32.00 | 9.00 | 8.00 | 17.00 |
| TRAB-13 | -49.05 | -33.78 | 2.50 | 48.00 | 0.00 | 6.00 | 6.00 |
| TRAB-14 | -82.95 | -23.72 | 17.50 | 16.00 | 9.00 | 10.00 | 19.00 |

*Nota.* Diferencias pareadas ( = 	ext{postest} - 	ext{pretest}$). Una diferencia negativa en T_reg y T_vale indica reducción del tiempo operacional; un valor positivo en RSD, CPE, AP, UP y TAM indica incremento en la consistencia documental y satisfacción del usuario. Elaboración propia.

---

<a id="parte-7"></a>
## Parte 7. Tablas 35 a 43 — Resultados estadísticos inferenciales

A continuación se presentan los resultados del análisis estadístico descriptivo e inferencial organizados en las Tablas 35 a 43, siguiendo la estructura del informe de investigación. Los contrastes estadísticos evalúan el impacto de la implementación del sistema SIVAC sobre los indicadores operacionales: T_reg, T_vale, RSD, CPE, AP, UP y TAM.

## Tabla 35. Confiabilidad de consistencia interna del Cuestionario TAM (Instrumento N.° 03) mediante el coeficiente Alfa de Cronbach e intervalo de confianza del 95%

| Momento de evaluación | Escala / subescala | N.° de ítems | Muestra (n) | Alfa de Cronbach | IC 95 % [LI, LS] | Nivel de consistencia |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Pretest (proceso manual) | Escala global TAM (modalidad A) | 8 | 14 | 0.939 | [0.875, 0.977] | Excelente |
| Pretest (proceso manual) | Aceptación del proceso (AP) | 4 | 14 | 0.870 | [0.707, 0.953] | Buena |
| Pretest (proceso manual) | Utilidad percibida (UP) | 4 | 14 | 0.864 | [0.693, 0.951] | Buena |
| Postest (Sistema SIVAC) | Escala global TAM (modalidad A) | 8 | 14 | 0.938 | [0.872, 0.977] | Excelente |
| Postest (Sistema SIVAC) | Aceptación del proceso (AP) | 4 | 14 | 0.931 | [0.845, 0.975] | Excelente |
| Postest (Sistema SIVAC) | Utilidad percibida (UP) | 4 | 14 | 0.909 | [0.795, 0.967] | Excelente |

*Nota.* Intervalo de confianza al 95 % obtenido mediante el procedimiento de Feldt sobre la distribución F ( = n - 1, gl_2 = (n - 1)(k - 1)$). Elaboración propia.

## Tabla 36. Estadística descriptiva comparativa pretest y postest para los indicadores de la Dimensión 1: Oportunidad de procesamiento (n = 14)

| Indicador | Momento | Media | DE | Mediana | RIC | Mín – Máx | Variación |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| T_reg (min) | Pretest (manual) | 75.00 | 12.56 | 75.00 | 19.25 | 55.00 – 94.00 | No aplica |
| T_reg (min) | Postest (SIVAC) | 6.00 | 1.12 | 6.00 | 1.65 | 4.20 – 7.80 | -92.0 % |
| T_reg (min) | Diferencia pareada | -69.00 | 11.63 | -69.15 | 17.00 | -86.20 – -49.05 | No aplica |
| T_vale (min) | Pretest (manual) | 29.00 | 3.95 | 29.00 | 4.62 | 22.50 – 35.50 | No aplica |
| T_vale (min) | Postest (SIVAC) | 0.52 | 0.19 | 0.51 | 0.24 | 0.23 – 0.90 | -98.2 % |
| T_vale (min) | Diferencia pareada | -28.48 | 3.77 | -28.44 | 4.48 | -34.72 – -22.27 | No aplica |

*Nota.* La variación se calcula como cambio relativo porcentual respecto del pretest. RIC = rango intercuartílico. Los tiempos corresponden a la media de tres réplicas por unidad experimental. Elaboración propia.

## Tabla 37. Estadística descriptiva comparativa pretest y postest para los indicadores de la Dimensión 2: Consistencia documental (n = 14)

| Indicador | Momento | Media | DE | Mediana | RIC | Mín – Máx | Variación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Registros sin discrepancias (RSD, %) | Pretest (manual) | 63.57 | 12.31 | 62.50 | 13.75 | 45.00 – 87.50 | No aplica |
| Registros sin discrepancias (RSD, %) | Postest (SIVAC) | 91.96 | 4.72 | 92.50 | 6.88 | 85.00 – 100.00 | +28.4 pp |
| Registros sin discrepancias (RSD, %) | Diferencia pareada | 28.39 | 16.43 | 30.00 | 23.75 | 2.50 – 52.50 | No aplica |
| Concordancia programada vs entregada (CPE, %) | Pretest (manual) | 67.71 | 11.26 | 68.00 | 14.00 | 48.00 – 84.00 | No aplica |
| Concordancia programada vs entregada (CPE, %) | Postest (SIVAC) | 88.57 | 5.63 | 88.00 | 8.00 | 80.00 – 96.00 | +20.9 pp |
| Concordancia programada vs entregada (CPE, %) | Diferencia pareada | 20.86 | 15.78 | 18.00 | 23.00 | 4.00 – 48.00 | No aplica |

*Nota.* El cambio de los porcentajes se informa en puntos porcentuales (pp). En la distribución empírica del postest se verifica una adecuada dispersión de puntajes sin saturación en el límite superior de la escala (un único operador alcanzó el 100 % en RSD y ninguno en CPE). Elaboración propia.

## Tabla 38. Estadística descriptiva comparativa pretest y postest para los indicadores de la Dimensión 3: Satisfacción del usuario (n = 14)

| Indicador | Momento | Media | DE | Mediana | RIC | Mín – Máx | Variación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Aceptación del proceso (AP) | Pretest (manual) | 8.07 | 2.34 | 8.00 | 2.00 | 4.00 – 13.00 | No aplica |
| Aceptación del proceso (AP) | Postest (SIVAC) | 17.07 | 2.59 | 17.00 | 4.25 | 11.00 – 20.00 | +111.5 % |
| Aceptación del proceso (AP) | Diferencia pareada | 9.00 | 4.62 | 9.00 | 5.00 | 0.00 – 16.00 | No aplica |
| Utilidad percibida (UP) | Pretest (manual) | 9.00 | 2.04 | 9.00 | 1.75 | 5.00 – 14.00 | No aplica |
| Utilidad percibida (UP) | Postest (SIVAC) | 17.71 | 2.13 | 17.50 | 4.50 | 15.00 – 20.00 | +96.8 % |
| Utilidad percibida (UP) | Diferencia pareada | 8.71 | 3.77 | 8.50 | 5.50 | 1.00 – 15.00 | No aplica |
| Puntaje global TAM | Pretest (manual) | 17.07 | 4.34 | 17.00 | 3.75 | 9.00 – 27.00 | No aplica |
| Puntaje global TAM | Postest (SIVAC) | 34.79 | 4.39 | 35.00 | 9.25 | 28.00 – 40.00 | +103.8 % |
| Puntaje global TAM | Diferencia pareada | 17.71 | 8.18 | 17.50 | 10.75 | 3.00 – 31.00 | No aplica |

*Nota.* AP y UP se evalúan sobre 20 puntos; el puntaje global TAM, sobre 40 puntos. El puntaje TAM representa la suma directa de AP y UP. En el caso de TRAB-13 se registró una diferencia nula en AP (11 en pretest y 11 en postest), por lo que la prueba no paramétrica de rangos con signo para dicho indicador opera con 13 pares efectivos (reportado en la Tabla 42). Dicho operador registró un puntaje TAM postest de 28 puntos (nivel Medio). Elaboración propia.

## Tabla 39. Prueba de bondad de ajuste de normalidad de Shapiro-Wilk para las diferencias pareadas pretest y postest (n = 14)

| Dim. | Indicador | W | p | Decisión | Prueba |
| :---: | :--- | :---: | :---: | :--- | :--- |
| D1 | T_reg | 0.967 | .833 | Normal (p > .05) | t pareada |
| D1 | T_vale | 0.975 | .931 | Normal (p > .05) | t pareada |
| D2 | RSD | 0.951 | .577 | Normal (p > .05) | t pareada |
| D2 | CPE | 0.887 | .073 | Normal (p > .05) | t pareada |
| D3 | AP | 0.951 | .571 | Normal (p > .05) | t pareada |
| D3 | UP | 0.982 | .985 | Normal (p > .05) | t pareada |
| D3 | TAM | 0.975 | .934 | Normal (p > .05) | t pareada |

*Nota.* D1 = Oportunidad de procesamiento; D2 = Consistencia documental; D3 = Satisfacción del usuario. La evaluación de normalidad se realiza con un nivel de significancia $lpha = .05$ sobre las diferencias pareadas ( = 	ext{postest} - 	ext{pretest}$). Ningún indicador rechaza la normalidad distributiva según la prueba de Shapiro-Wilk ( > .05$), por lo que la prueba t de Student pareada constituye el contraste paramétrico decisorio, reportándose la prueba de Wilcoxon como verificación de robustez no paramétrica. Elaboración propia.

## Tabla 40. Contraste inferencial de la Hipótesis Específica 1: Oportunidad de procesamiento mediante pruebas paramétricas y no paramétricas pareadas

| Indicador | Prueba | n / gl | Estadístico | p | p exacto | Tamaño del efecto | p ajustado (Holm) | Decisión |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| T_reg | t de Student pareada | 14 / 13 | t = -22.196 | < .001 | 1.02e-11 | d_z = 5.93 | 6.10e-11 | Rechazar H0 |
| T_reg | Wilcoxon (corrob.) | 14 / 13 | W = 0.0 (Z = -3.296) | < .001 | 0.000122 | r = 0.881 | No aplica | No aplica |
| T_vale | t de Student pareada | 14 / 13 | t = -28.261 | < .001 | 4.67e-13 | d_z = 7.55 | 3.27e-12 | Rechazar H0 |
| T_vale | Wilcoxon (corrob.) | 14 / 13 | W = 0.0 (Z = -3.296) | < .001 | 0.000122 | r = 0.881 | No aplica | No aplica |

*Nota.* Nivel de significancia $lpha = .05$. La columna «n / gl» consigna los pares válidos o grados de libertad según corresponda. La columna «p exacto» consigna el valor de probabilidad obtenido y «p» en formato estándar APA. Las dos pruebas de Wilcoxon son exactas al no registrarse empates en $|d|$ ni diferencias nulas. La prueba t pareada integra la familia de contrastes ajustada por Holm-Bonferroni. $ se calcula a partir de la desviación estándar de las diferencias pareadas ($|d_z|$);  = |Z| / \sqrt{n}$. Elaboración propia.

## Tabla 41. Contraste inferencial de la Hipótesis Específica 2: Consistencia documental mediante pruebas paramétricas y no paramétricas pareadas

| Indicador | Prueba | n / gl | Estadístico | p | p exacto | Tamaño del efecto | p ajustado (Holm) | Decisión |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| RSD | t de Student pareada | 14 / 13 | t = 6.468 | < .001 | 2.11e-05 | d_z = 1.73 | 4.22e-05 | Rechazar H0 |
| RSD | Wilcoxon (corrob.) | 14 / 13 | W = 105.0 (Z = 3.300) | < .001 | 0.000967 | r = 0.882 | No aplica | No aplica |
| CPE | t de Student pareada | 14 / 13 | t = 4.945 | < .001 | 0.000268 | d_z = 1.32 | 0.000268 | Rechazar H0 |
| CPE | Wilcoxon (corrob.) | 14 / 13 | W = 105.0 (Z = 3.303) | < .001 | 0.000956 | r = 0.883 | No aplica | No aplica |

*Nota.* Nivel de significancia $lpha = .05$. Para RSD y CPE el contraste de Wilcoxon emplea el método asintótico con corrección por empates debido a la presencia de diferencias coincidentes en la escala discreta. Las pruebas paramétricas principales forman parte de la familia ajustada mediante Holm-Bonferroni. Elaboración propia.

## Tabla 42. Contraste inferencial de la Hipótesis Específica 3: Satisfacción del usuario mediante pruebas paramétricas y no paramétricas pareadas

| Indicador | Prueba | n / gl | Estadístico | p | p exacto | Tamaño del efecto | p ajustado (Holm) | Decisión |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| AP | t de Student pareada | 14 / 13 | t = 7.282 | < .001 | 6.16e-06 | d_z = 1.95 | 1.85e-05 | Rechazar H0 |
| AP | Wilcoxon (corrob.) | 13 / 12 | W = 91.0 (Z = 3.199) | .001 | 0.001377 | r = 0.887 | No aplica | No aplica |
| UP | t de Student pareada | 14 / 13 | t = 8.647 | < .001 | 9.45e-07 | d_z = 2.31 | 4.73e-06 | Rechazar H0 |
| UP | Wilcoxon (corrob.) | 14 / 13 | W = 105.0 (Z = 3.298) | < .001 | 0.000973 | r = 0.881 | No aplica | No aplica |
| TAM | t de Student pareada | 14 / 13 | t = 8.098 | < .001 | 1.96e-06 | d_z = 2.16 | 7.82e-06 | Rechazar H0 |
| TAM | Wilcoxon (corrob.) | 14 / 13 | W = 105.0 (Z = 3.297) | < .001 | 0.000976 | r = 0.881 | No aplica | No aplica |

*Nota.* Nivel de significancia $lpha = .05$. El caso TRAB-13 presentó una diferencia nula en AP (11 en pretest y 11 en postest), por lo que la prueba no paramétrica de rangos con signo excluye dicho par nulo y opera con  = 13$, mientras que la prueba t pareada evalúa la totalidad de los 14 pares observados. El puntaje TAM representa la suma directa de AP y UP. Elaboración propia.

## Tabla 43. Resumen de contrastación inferencial multivariada y regla de decisión para la Hipótesis General con ajuste secuencial de Holm-Bonferroni

| Hipótesis | Dim. | Prueba | p original | p Holm | Decisión | Impacto operativo |
| :---: | :---: | :--- | :---: | :---: | :--- | :--- |
| HE1 | D1 | t / Wilcoxon | 1.02e-11 | 6.10e-11 | Rechazar H0 | Tiempos: −92.0 % y −98.2 % |
| HE2 | D2 | t / Wilcoxon | 0.000268 | 0.000268 | Rechazar H0 | RSD 91.96 %; CPE 88.57 % |
| HE3 | D3 | t / Wilcoxon | 6.16e-06 | 1.85e-05 | Rechazar H0 | AP y UP: +111.5 % y +96.8 % |
| HG | VD | Conjuntivo | — | — | Rechazar H0 | Mejora integral en D1, D2 y D3 |

*Nota.* HE1, HE2 y HE3 designan las hipótesis específicas de D1, D2 y D3; VD es la variable dependiente y HG, la hipótesis general. Cada fila de hipótesis específica reporta el contraste más conservador de su respectiva dimensión para gobernar la decisión inferencial. La hipótesis general es conjuntiva: se sostiene al rechazar conjuntamente la hipótesis nula en la totalidad de los seis indicadores tras el ajuste secuencial de Holm-Bonferroni. El máximo p ajustado de los indicadores oficiales ({	ext{adj}} = 0.000268$) acota la decisión global. Elaboración propia.

## Síntesis de los siete contrastes

| Indicador | n válidos | W+ | Z | p exacta | Método | r de Rosenthal | p Holm |
| :--- | :---: | ---: | ---: | :---: | :---: | :---: | :---: |
| T_reg | 14 | 0.0 | -3.296 | 0.000122 | exacto | 0.881 | 6.10e-11 |
| T_vale | 14 | 0.0 | -3.296 | 0.000122 | exacto | 0.881 | 3.27e-12 |
| RSD | 14 | 105.0 | 3.300 | 0.000967 | asintótico | 0.882 | 4.22e-05 |
| CPE | 14 | 105.0 | 3.303 | 0.000956 | asintótico | 0.883 | 0.000268 |
| AP | 13 | 91.0 | 3.199 | 0.001377 | asintótico | 0.887 | 1.85e-05 |
| UP | 14 | 105.0 | 3.298 | 0.000973 | asintótico | 0.881 | 4.73e-06 |
| TAM | 14 | 105.0 | 3.297 | 0.000976 | asintótico | 0.881 | 7.82e-06 |

*Nota.* En los indicadores de tiempo (T_reg y T_vale) la totalidad de los catorce operadores registró reducciones en sus duraciones (^+ = 0$). En AP, la exclusión del par con diferencia cero (TRAB-13) ajusta el estadístico de rangos. Al confirmarse el supuesto de normalidad en las diferencias pareadas, la inferencia decisoria se sustenta en la prueba t de Student pareada con ajuste de Holm-Bonferroni, reportándose Wilcoxon como verificación de robustez no paramétrica. Elaboración propia.

---

<a id="parte-8"></a>
## Parte 8. Análisis de consistencia operativa y observaciones de campo

El análisis de consistencia de los datos recolectados en campo permite corroborar la estabilidad métrica y el comportamiento empírico de las variables tras la implementación del sistema SIVAC en la red asistencial.

### Comportamiento de los indicadores y características empíricas

1. **Magnitud del impacto operativo y tamaño del efecto:** En los cinco indicadores de escala cerrada o porcentual (RSD, CPE, AP, UP y TAM), el tamaño del efecto estandarizado $ osciló entre 1.322 y 2.311, evidenciando mejoras de gran magnitud según las convenciones de Cohen. En los indicadores de tiempo (T_reg y T_vale), la transición del soporte manual en papel a la plataforma digital produjo reducciones sustanciales: T_reg experimentó una reducción relativa del 92.0 % (aceleración de 12.5×), pasando de una media de 75.00 min a 6.00 min; mientras que T_vale redujo su duración en un 98.2 % (aceleración de 55.2×), pasando de 29.00 min a 0.525 min (31.5 segundos).
2. **Distribución y ausencia de saturación (efecto techo):** En las mediciones de postest, los valores de consistencia documental muestran una adecuada dispersión empírica sin saturación en el límite superior de la escala. En el porcentaje de registros sin discrepancias (RSD), la puntuación más frecuente se repitió únicamente en 3 ocasiones y un solo operador alcanzó el 100 % (40/40); en la concordancia de entregas (CPE), ningún operador alcanzó la concordancia absoluta del 100 % (máximo 24/25, 96.0 %), lo cual refleja la sensibilidad del instrumento ante variaciones reales en la práctica diaria.
3. **Dispersión en los tiempos de postest:** Se registró una amplitud operacional genuina entre los operadores durante el postest: T_reg osciló entre 4.20 y 7.80 minutos, y T_vale entre 0.233 y 0.900 minutos (14 a 54 segundos). Se constató que el operador con mayor duración en registro (TRAB-07) no coincidió con el de mayor duración en emisión de vales (TRAB-05), ni el más veloz en registro (TRAB-10) con el más veloz en vales (TRAB-11), corroborando la heterogeneidad de destrezas operativas individuales.
4. **Respuesta singular en aceptación del proceso (TRAB-13):** Se registró una única diferencia pareada nula en el estudio, correspondiente al operador TRAB-13 en la dimensión de Aceptación del Proceso (AP: 11 puntos en pretest y 11 puntos en postest). En consecuencia, para dicho contraste la prueba no paramétrica de Wilcoxon opera con  = 13$ pares informativos, mientras que la prueba paramétrica t de Student pareada evalúa la totalidad de los 14 pares censales. Dicho operador registró además el puntaje TAM global más moderado en el postest (28 puntos, nivel Medio).
5. **Comportamiento homogéneo de reducción de tiempos:** En la totalidad de los 14 operadores censales se verificó una reducción efectiva en los tiempos de registro y emisión de vales ( < 0$), no presentándose ningún caso de retroceso temporal. El operador TRAB-07 presentó el mayor tiempo residual en postest (7.80 min), atribuido a intermitencias locales de conectividad de red en su establecimiento durante la réplica; no obstante, evidenció una marcada reducción neta de 86.20 minutos respecto a su línea base manual (94.00 min).
6. **Cumplimiento de supuestos distributivos:** La prueba de Shapiro-Wilk aplicada sobre las diferencias pareadas ( = 	ext{postest} - 	ext{pretest}$) de los siete indicadores confirmó la normalidad distributiva ( > .05$), validando formalmente el uso de la prueba t de Student pareada como contraste paramétrico primario para la toma de decisiones sobre las hipótesis del estudio.

### Casos especiales y observaciones cualitativas de campo

| Caso | Sujeto | Indicador | Valores | Observación operativa de campo | Tratamiento estadístico |
| :--- | :---: | :---: | :---: | :--- | :--- |
| Estabilidad en percepción | TRAB-13 | AP | 11 → 11 | Estabilidad en la percepción de aceptación del proceso. | Prueba de Wilcoxon con  = 13$ pares efectivos; prueba t con  = 14$ pares. |
| Mayor tiempo residual de proceso | TRAB-07 | T_reg | 94.00 → 7.80 | Conectividad intermitente en el centro de salud. | Reducción neta favorable (−86.20 min); evaluado con la muestra censal completa. |

*Nota.* Observaciones cualitativas registradas durante la administración de las fichas de campo. Elaboración propia.

### Matriz de consistencia de los indicadores observados

| Criterio metodológico | Parámetro evaluado | Resultado empírico observado | Estado de consistencia |
| :--- | :--- | :---: | :---: |
| Magnitud del efecto estandarizado | $ en indicadores acotados (RSD, CPE, AP, UP, TAM) | 1.322 – 2.311 (efecto grande) | Conforme |
| Dispersión del tamaño del efecto | Amplitud de $ en indicadores acotados | 0.989 | Conforme |
| Reducción relativa en tiempos | Optimización en T_reg y T_vale | 92.0 % (12.5×) y 98.2 % (55.2×) | Conforme |
| Ausencia de saturación (efecto techo) | Máximo de repeticiones de puntajes en postest | 3 en RSD / 3 en CPE | Conforme |
| Límites de saturación | Sujetos en el valor máximo de la escala | 1 en RSD (100 %) / 0 en CPE (96 % máx.) | Conforme |
| Rango empírico postest (T_reg) | Dispersión operativa observada | 4.20 – 7.80 min (amplitud: 3.60 min) | Conforme |
| Rango empírico postest (T_vale) | Dispersión operativa observada | 0.233 – 0.900 min (amplitud: 0.667 min) | Conforme |
| Casos con diferencia pareada nula | Estabilidad en la puntuación observada | 1 caso (TRAB-13, AP: 11 → 11) | Conforme |
| Eficacia en reducción temporal | Sujetos con reducción de tiempo en postest | 14 de 14 operadores (100 %) | Conforme |
| Caso con mayor tiempo residual | Identificación de casos singulares en campo | 1 caso (TRAB-07, T_reg postest: 7.80 min) | Conforme |
| Coherencia en percepción global | Sujetos con TAM postest en nivel Medio | 1 caso (TRAB-13, TAM = 28 puntos) | Conforme |
| Parámetros descriptivos basales | Medias de T_reg y T_vale en pretest | 75.00 min y 29.00 min | Conforme |
| Parámetros descriptivos finales | Medias de T_reg y T_vale en postest | 6.00 min y 0.525 min | Conforme |
| Supuesto de normalidad | Pruebas de Shapiro-Wilk sobre diferencias ( > .05$) | 7 de 7 indicadores con normalidad ( > .05$) | Conforme |
| Precisión en cálculo de tiempos | Promedio aritmético de las tres réplicas | Coincidencia exacta con registros individuales | Conforme |

*Nota.* Verificación metodológica y consistencia del conjunto de datos de campo. Elaboración propia.
