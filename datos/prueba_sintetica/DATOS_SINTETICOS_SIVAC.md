# CONJUNTO DE DATOS SINTÉTICOS DE CAMPO — SIVAC

**Proyecto.** Aplicación del sistema «SIVAC» para mejorar la gestión de movimientos mensuales de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.

**Institución.** Universidad Nacional José María Arguedas — Escuela Profesional de Ingeniería de Sistemas.

**Diseño.** Preexperimental de un solo grupo con pretest y postest (O₁ → X → O₂), población censal de 14 operadores en 13 centros de acopio.

**Naturaleza de los datos.** Conjunto **sintético** generado con semilla fija (`20261026`) para ensayar el procesamiento estadístico completo. No corresponde a mediciones reales y debe declararse como tal en el informe.

---

## 0. Ficha técnica del conjunto

| Elemento | Descripción |
| --- | --- |
| Unidad de análisis | Operador de inmunizaciones (14 unidades censales) |
| Momentos | Pretest (proceso manual) y postest (con SIVAC) |
| Instrumento 01 | 168 réplicas cronometradas (14 × 2 × 6) |
| Instrumento 02 | 1 120 asientos auditados (14 × 2 × 40) y 700 despachos (14 × 2 × 25) |
| Instrumento 03 | 224 respuestas Likert (14 × 2 × 8) |
| Periodo de campo | 10/08/2026 al 08/09/2026 (pretest); 12/10/2026 al 20/10/2026 (postest) |
| Formato numérico | Punto decimal, sin separador de miles, UTF-8 |
| Reproducibilidad | `python scripts/estadistica/generar_datos_sinteticos.py` (semilla 20261026) |

### 0.1 · Reglas de cálculo aplicadas

1. **T_reg y T_vale** son el promedio aritmético de tres réplicas independientes por operador y momento.
2. **RSD** = asientos conformes ÷ 40 × 100; la conformidad exige los ocho criterios simultáneamente.
3. **CPE** = despachos conciliados sin diferencia ÷ 25 × 100.
4. **AP y UP** son la suma de cuatro reactivos Likert (4 a 20); el puntaje global TAM es AP + UP (8 a 40).
5. **Contraste inferencial**: Shapiro-Wilk sobre las diferencias pareadas; *t* de Student pareada si *p* > .05, Wilcoxon de rangos con signo si *p* ≤ .05.
6. **Multiplicidad**: Holm-Bonferroni sobre la familia de indicadores.

### 0.2 · Coherencia interna verificada

| Verificación | Resultado |
| --- | --- |
| Promedios de tiempos recalculados desde las réplicas | Coinciden con la matriz analítica (4 decimales) |
| RSD y CPE recalculados desde los asientos y despachos | Coinciden con la matriz analítica |
| Suma de asientos por unidad y momento | 40 en los 28 bloques |
| Suma de despachos por unidad y momento | 25 en los 28 bloques |
| Reactivos Likert por unidad y momento | 8 en los 28 bloques |
| Totales de fila de los CSV | 1 120 asientos, 700 despachos, 224 respuestas |

*Nota.* Los promedios de T_reg y T_vale se obtienen de las réplicas y pueden diferir en la cuarta cifra decimal de la matriz analítica, que se publica con dos decimales por convención del informe.

*Nota sobre la granularidad.* RSD y CPE se calculan sobre conteos enteros (40 asientos y 25 despachos), por lo que cada unidad solo puede adoptar múltiplos de 2.5 % y de 4 % respectivamente. Esa es la razón por la que los porcentajes por operador no son redondos y por la que los promedios del conjunto (95.89 % y 95.43 %) difieren en menos de un punto de los valores consolidados del informe: el crudo siempre manda sobre la cifra agregada.

### 0.3 · Archivos del conjunto y uso

| Archivo | Contenido | Filas |
| --- | --- | ---: |
| `DATOS_SINTETICOS_SIVAC.md` | Este documento: fichas completas de los tres instrumentos | — |
| `instrumento01_replicas.csv` | Réplicas cronometradas en formato largo (una fila por réplica) | 168 |
| `instrumento02_asientos.csv` | Asientos auditados con los ocho criterios y el motivo de no conformidad | 1 120 |
| `instrumento02_despachos.csv` | Despachos conciliados con programado, entregado y diferencia | 700 |
| `instrumento03_reactivos.csv` | Respuestas Likert en formato largo con dimensiones y puntajes | 224 |
| `matriz_analitica_pre_post.csv` | Matriz por sujeto y momento con todos los indicadores calculados | 28 |
| `pretest_sintetico.csv` / `posttest_sintetico.csv` | Mismos nombres y columnas que `datos/recolectados/*_campo.csv` | 14 + 14 |

Para ejecutar el pipeline real sobre este conjunto sin tocar los datos del proyecto, copie los dos últimos archivos a una carpeta temporal con los nombres `pretest_campo.csv` y `posttest_campo.csv` y apunte `DATOS_DIR` a esa carpeta; el resto del análisis (Shapiro-Wilk, *t* pareada, Holm, Cronbach, figuras) corre sin cambios.

---

## Índice

- [Sección 1. Instrumento 01 — Tiempos](#s1)
- [Sección 2. Instrumento 02 — Auditoría documental](#s2)
- [Sección 3. Instrumento 03 — Cuestionario TAM](#s3)
- [Sección 4. Verificación estadística](#s4)

---

<a id="s1"></a>
## Sección 1. Instrumento N.° 01 — Ficha de registro de tiempos operativos

Cada bloque reproduce una ficha completa: encabezado, las tres réplicas de registro (REG-01 a REG-03), las tres réplicas de emisión del vale (VALE-01 a VALE-03) y el cierre con el promedio del operador. `T_reg` y `T_vale` se obtienen como diferencia entre la hora de corte y la hora de inicio, en minutos con cuatro decimales.

**Convenciones de escenario.** T1 ingreso de lote; T2 salida o transferencia a la red; T3 redistribución; T4 vale simple para puesto de salud; T5 vale regular para centro de salud; T6 vale de reposición o contingencia. Las pausas por causas ajenas al proceso se anotan en observaciones y la medición se repite hasta completar las tres réplicas por indicador.

### 1.1 · TRAB-01 · Pretest (proceso manual) · 10/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-01 | ALMACÉN (CHANKA) | 10/08/2026 | Pretest | OBS-01 | 10/08/2026 al 08/09/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2608-12 | 07:30:00 | 08:03:41 | 33.6833 |
| 2 | Salida o transferencia a la red (T2) | L-2608-13 | 08:03:41 | 08:41:30 | 37.8167 |
| 3 | Redistribución a la red (T3) | L-2608-14 | 08:41:30 | 09:25:30 | 44.0000 |

Cierre: 115.5000 min ÷ 3 = **38.5000 min** (6930 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-0810-040 | 09:30:55 | 09:48:10 | 17.2500 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-0810-041 | 09:48:10 | 10:06:06 | 17.9333 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-0810-042 | 10:06:06 | 10:26:25 | 20.3167 |

Cierre: 55.5000 min ÷ 3 = **18.5000 min** (3330 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 38.5000 | 18.5000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:30:00 y cerrada a las 10:26:25; se registraron los seis escenarios en jornada continua.
- Entre el bloque de registro y el de vales transcurrieron 5 min 25 s por traslado del talonario y verificación de existencias.
- El registro se realizó en el kardex físico y el vale se llenó por triplicado; se contó con el visto bueno del jefe del almacén.
- Ninguna réplica fue invalidada: las interrupciones se resolvieron dentro de la misma medición y quedaron anotadas.

---

### 1.2 · TRAB-01 · Postest (Sistema SIVAC) · 12/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-01 | ALMACÉN (CHANKA) | 12/10/2026 | Postest | OBS-01 | 12/10/2026 al 20/10/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2610-07 | 08:00:00 | 08:06:42 | 6.7000 |
| 2 | Salida o transferencia a la red (T2) | L-2610-08 | 08:06:42 | 08:14:16 | 7.5667 |
| 3 | Redistribución a la red (T3) | L-2610-09 | 08:14:16 | 08:22:30 | 8.2333 |

Cierre: 22.5000 min ÷ 3 = **7.5000 min** (1350 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-1012-045 | 08:24:14 | 08:27:08 | 2.9000 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-1012-046 | 08:27:08 | 08:30:13 | 3.0833 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-1012-047 | 08:30:13 | 08:33:14 | 3.0167 |

Cierre: 9.0000 min ÷ 3 = **3.0000 min** (540 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 7.5000 | 3.0000 | 6 |

**Observaciones**

- Sesión iniciada a las 08:00:00 y cerrada a las 08:33:14, con el operador ya familiarizado con la interfaz.
- Las tres réplicas de registro se ejecutaron sobre el módulo de movimientos y las de vales sobre el módulo de comprobantes.
- Pausa de 1 min 44 s por atención en ventanilla; no afectó la medición.
- Se verificó que el sistema emitiera el vale con numeración correlativa y descarga automática del saldo.

---

### 1.3 · TRAB-02 · Pretest (proceso manual) · 10/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-02 | ALMACÉN (CHANKA) | 10/08/2026 | Pretest | OBS-02 | 10/08/2026 al 08/09/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2608-13 | 07:15:00 | 07:54:01 | 39.0167 |
| 2 | Salida o transferencia a la red (T2) | L-2608-14 | 07:54:01 | 08:35:17 | 41.2667 |
| 3 | Redistribución a la red (T3) | L-2608-15 | 08:35:17 | 09:21:00 | 45.7167 |

Cierre: 126.0000 min ÷ 3 = **42.0000 min** (7560 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-0810-040 | 09:26:26 | 09:47:22 | 20.9333 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-0810-041 | 09:47:22 | 10:09:09 | 21.7833 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-0810-042 | 10:09:09 | 10:32:26 | 23.2833 |

Cierre: 66.0000 min ÷ 3 = **22.0000 min** (3960 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 42.0000 | 22.0000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:15:00 y cerrada a las 10:32:26; se registraron los seis escenarios en jornada continua.
- Entre el bloque de registro y el de vales transcurrieron 5 min 26 s por traslado del talonario y verificación de existencias.
- El registro se realizó en el kardex físico y el vale se llenó por triplicado; se contó con el visto bueno del jefe del almacén.
- Ninguna réplica fue invalidada: las interrupciones se resolvieron dentro de la misma medición y quedaron anotadas.

---

### 1.4 · TRAB-02 · Postest (Sistema SIVAC) · 12/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-02 | ALMACÉN (CHANKA) | 12/10/2026 | Postest | OBS-02 | 12/10/2026 al 20/10/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2610-16 | 07:50:00 | 07:57:13 | 7.2167 |
| 2 | Salida o transferencia a la red (T2) | L-2610-17 | 07:57:13 | 08:05:07 | 7.9000 |
| 3 | Redistribución a la red (T3) | L-2610-18 | 08:05:07 | 08:14:00 | 8.8833 |

Cierre: 24.0000 min ÷ 3 = **8.0000 min** (1440 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-1012-044 | 08:15:09 | 08:18:25 | 3.2667 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-1012-045 | 08:18:25 | 08:21:53 | 3.4667 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-1012-046 | 08:21:53 | 08:25:39 | 3.7667 |

Cierre: 10.5000 min ÷ 3 = **3.5000 min** (630 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 8.0000 | 3.5000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:50:00 y cerrada a las 08:25:39, con el operador ya familiarizado con la interfaz.
- Las tres réplicas de registro se ejecutaron sobre el módulo de movimientos y las de vales sobre el módulo de comprobantes.
- Pausa de 1 min 09 s por atención en ventanilla; no afectó la medición.
- Se verificó que el sistema emitiera el vale con numeración correlativa y descarga automática del saldo.

---

### 1.5 · TRAB-03 · Pretest (proceso manual) · 11/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-03 | Hospital Andahuaylas | 11/08/2026 | Pretest | OBS-01 | 10/08/2026 al 08/09/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2608-02 | 07:45:00 | 08:16:06 | 31.1000 |
| 2 | Salida o transferencia a la red (T2) | L-2608-03 | 08:16:06 | 08:52:11 | 36.0833 |
| 3 | Redistribución a la red (T3) | L-2608-04 | 08:52:11 | 09:30:00 | 37.8167 |

Cierre: 105.0000 min ÷ 3 = **35.0000 min** (6300 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-0811-052 | 09:33:36 | 09:48:05 | 14.4833 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-0811-053 | 09:48:05 | 10:04:03 | 15.9667 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-0811-054 | 10:04:03 | 10:21:36 | 17.5500 |

Cierre: 48.0000 min ÷ 3 = **16.0000 min** (2880 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 35.0000 | 16.0000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:45:00 y cerrada a las 10:21:36; se registraron los seis escenarios en jornada continua.
- Entre el bloque de registro y el de vales transcurrieron 3 min 36 s por traslado del talonario y verificación de existencias.
- El registro se realizó en el kardex físico y el vale se llenó por triplicado; se contó con el visto bueno del jefe del almacén.
- Ninguna réplica fue invalidada: las interrupciones se resolvieron dentro de la misma medición y quedaron anotadas.

---

### 1.6 · TRAB-03 · Postest (Sistema SIVAC) · 13/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-03 | Hospital Andahuaylas | 13/10/2026 | Postest | OBS-01 | 12/10/2026 al 20/10/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2610-05 | 08:15:00 | 08:20:55 | 5.9167 |
| 2 | Salida o transferencia a la red (T2) | L-2610-06 | 08:20:55 | 08:27:21 | 6.4333 |
| 3 | Redistribución a la red (T3) | L-2610-07 | 08:27:21 | 08:34:30 | 7.1500 |

Cierre: 19.5000 min ÷ 3 = **6.5000 min** (1170 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-1013-035 | 08:35:12 | 08:37:33 | 2.3500 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-1013-036 | 08:37:33 | 08:40:07 | 2.5667 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-1013-037 | 08:40:07 | 08:42:42 | 2.5833 |

Cierre: 7.5000 min ÷ 3 = **2.5000 min** (450 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 6.5000 | 2.5000 | 6 |

**Observaciones**

- Sesión iniciada a las 08:15:00 y cerrada a las 08:42:42, con el operador ya familiarizado con la interfaz.
- Las tres réplicas de registro se ejecutaron sobre el módulo de movimientos y las de vales sobre el módulo de comprobantes.
- Se verificó que el sistema emitiera el vale con numeración correlativa y descarga automática del saldo.

---

### 1.7 · TRAB-04 · Pretest (proceso manual) · 11/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-04 | Hospital ESSALUD Andahuaylas | 11/08/2026 | Pretest | OBS-02 | 10/08/2026 al 08/09/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2608-09 | 08:00:00 | 08:29:02 | 29.0333 |
| 2 | Salida o transferencia a la red (T2) | L-2608-10 | 08:29:02 | 09:03:39 | 34.6167 |
| 3 | Redistribución a la red (T3) | L-2608-11 | 09:03:39 | 09:40:30 | 36.8500 |

Cierre: 100.5000 min ÷ 3 = **33.5000 min** (6030 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-0811-052 | 09:47:11 | 10:00:40 | 13.4833 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-0811-053 | 10:00:40 | 10:15:56 | 15.2667 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-0811-054 | 10:15:56 | 10:32:11 | 16.2500 |

Cierre: 45.0000 min ÷ 3 = **15.0000 min** (2700 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 33.5000 | 15.0000 | 6 |

**Observaciones**

- Sesión iniciada a las 08:00:00 y cerrada a las 10:32:11; se registraron los seis escenarios en jornada continua.
- Entre el bloque de registro y el de vales transcurrieron 6 min 41 s por traslado del talonario y verificación de existencias.
- El registro se realizó en el kardex físico y el vale se llenó por triplicado; se contó con el visto bueno del jefe del almacén.
- Ninguna réplica fue invalidada: las interrupciones se resolvieron dentro de la misma medición y quedaron anotadas.

---

### 1.8 · TRAB-04 · Postest (Sistema SIVAC) · 13/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-04 | Hospital ESSALUD Andahuaylas | 13/10/2026 | Postest | OBS-02 | 12/10/2026 al 20/10/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2610-09 | 08:30:00 | 08:35:40 | 5.6667 |
| 2 | Salida o transferencia a la red (T2) | L-2610-10 | 08:35:40 | 08:41:46 | 6.1000 |
| 3 | Redistribución a la red (T3) | L-2610-11 | 08:41:46 | 08:48:00 | 6.2333 |

Cierre: 18.0000 min ÷ 3 = **6.0000 min** (1080 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-1013-058 | 08:48:18 | 08:50:33 | 2.2500 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-1013-059 | 08:50:33 | 08:53:03 | 2.5000 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-1013-060 | 08:53:03 | 08:55:48 | 2.7500 |

Cierre: 7.5000 min ÷ 3 = **2.5000 min** (450 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 6.0000 | 2.5000 | 6 |

**Observaciones**

- Sesión iniciada a las 08:30:00 y cerrada a las 08:55:48, con el operador ya familiarizado con la interfaz.
- Las tres réplicas de registro se ejecutaron sobre el módulo de movimientos y las de vales sobre el módulo de comprobantes.
- Se verificó que el sistema emitiera el vale con numeración correlativa y descarga automática del saldo.

---

### 1.9 · TRAB-05 · Pretest (proceso manual) · 12/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-05 | Centro de Salud Andahuaylas | 12/08/2026 | Pretest | OBS-01 | 10/08/2026 al 08/09/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2608-06 | 07:20:00 | 07:56:44 | 36.7333 |
| 2 | Salida o transferencia a la red (T2) | L-2608-07 | 07:56:44 | 08:36:54 | 40.1667 |
| 3 | Redistribución a la red (T3) | L-2608-08 | 08:36:54 | 09:20:00 | 43.1000 |

Cierre: 120.0000 min ÷ 3 = **40.0000 min** (7200 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-0812-041 | 09:22:07 | 09:41:37 | 19.5000 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-0812-042 | 09:41:37 | 10:02:36 | 20.9833 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-0812-043 | 10:02:36 | 10:23:37 | 21.0167 |

Cierre: 61.5000 min ÷ 3 = **20.5000 min** (3690 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 40.0000 | 20.5000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:20:00 y cerrada a las 10:23:37; se registraron los seis escenarios en jornada continua.
- Entre el bloque de registro y el de vales transcurrieron 2 min 07 s por traslado del talonario y verificación de existencias.
- El registro se realizó en el kardex físico y el vale se llenó por triplicado; se contó con el visto bueno del jefe del almacén.
- Ninguna réplica fue invalidada: las interrupciones se resolvieron dentro de la misma medición y quedaron anotadas.

---

### 1.10 · TRAB-05 · Postest (Sistema SIVAC) · 14/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-05 | Centro de Salud Andahuaylas | 14/10/2026 | Postest | OBS-01 | 12/10/2026 al 20/10/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2610-06 | 07:45:00 | 07:53:12 | 8.2000 |
| 2 | Salida o transferencia a la red (T2) | L-2610-07 | 07:53:12 | 08:01:53 | 8.6833 |
| 3 | Redistribución a la red (T3) | L-2610-08 | 08:01:53 | 08:12:00 | 10.1167 |

Cierre: 27.0000 min ÷ 3 = **9.0000 min** (1620 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-1014-052 | 08:13:35 | 08:17:18 | 3.7167 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-1014-053 | 08:17:18 | 08:21:20 | 4.0333 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-1014-054 | 08:21:20 | 08:25:35 | 4.2500 |

Cierre: 12.0000 min ÷ 3 = **4.0000 min** (720 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 9.0000 | 4.0000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:45:00 y cerrada a las 08:25:35, con el operador ya familiarizado con la interfaz.
- Las tres réplicas de registro se ejecutaron sobre el módulo de movimientos y las de vales sobre el módulo de comprobantes.
- Pausa de 1 min 35 s por atención en ventanilla; no afectó la medición.
- Se verificó que el sistema emitiera el vale con numeración correlativa y descarga automática del saldo.

---

### 1.11 · TRAB-06 · Pretest (proceso manual) · 12/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-06 | Talavera | 12/08/2026 | Pretest | OBS-02 | 10/08/2026 al 08/09/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2608-11 | 07:40:00 | 08:12:21 | 32.3500 |
| 2 | Salida o transferencia a la red (T2) | L-2608-12 | 08:12:21 | 08:48:44 | 36.3833 |
| 3 | Redistribución a la red (T3) | L-2608-13 | 08:48:44 | 09:29:30 | 40.7667 |

Cierre: 109.5000 min ÷ 3 = **36.5000 min** (6570 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-0812-051 | 09:35:03 | 09:50:48 | 15.7500 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-0812-052 | 09:50:48 | 10:07:19 | 16.5167 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-0812-053 | 10:07:19 | 10:26:03 | 18.7333 |

Cierre: 51.0000 min ÷ 3 = **17.0000 min** (3060 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 36.5000 | 17.0000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:40:00 y cerrada a las 10:26:03; se registraron los seis escenarios en jornada continua.
- Entre el bloque de registro y el de vales transcurrieron 5 min 33 s por traslado del talonario y verificación de existencias.
- El registro se realizó en el kardex físico y el vale se llenó por triplicado; se contó con el visto bueno del jefe del almacén.
- Ninguna réplica fue invalidada: las interrupciones se resolvieron dentro de la misma medición y quedaron anotadas.

---

### 1.12 · TRAB-06 · Postest (Sistema SIVAC) · 14/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-06 | Talavera | 14/10/2026 | Postest | OBS-02 | 12/10/2026 al 20/10/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2610-17 | 08:10:00 | 08:16:08 | 6.1333 |
| 2 | Salida o transferencia a la red (T2) | L-2610-18 | 08:16:08 | 08:23:19 | 7.1833 |
| 3 | Redistribución a la red (T3) | L-2610-19 | 08:23:19 | 08:31:00 | 7.6833 |

Cierre: 21.0000 min ÷ 3 = **7.0000 min** (1260 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-1014-039 | 08:32:12 | 08:35:05 | 2.8833 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-1014-040 | 08:35:05 | 08:38:03 | 2.9667 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-1014-041 | 08:38:03 | 08:41:12 | 3.1500 |

Cierre: 9.0000 min ÷ 3 = **3.0000 min** (540 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 7.0000 | 3.0000 | 6 |

**Observaciones**

- Sesión iniciada a las 08:10:00 y cerrada a las 08:41:12, con el operador ya familiarizado con la interfaz.
- Las tres réplicas de registro se ejecutaron sobre el módulo de movimientos y las de vales sobre el módulo de comprobantes.
- Pausa de 1 min 12 s por atención en ventanilla; no afectó la medición.
- Se verificó que el sistema emitiera el vale con numeración correlativa y descarga automática del saldo.

---

### 1.13 · TRAB-07 · Pretest (proceso manual) · 13/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-07 | San Jeronimo | 13/08/2026 | Pretest | OBS-01 | 10/08/2026 al 08/09/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2608-14 | 07:30:00 | 08:08:45 | 38.7500 |
| 2 | Salida o transferencia a la red (T2) | L-2608-15 | 08:08:45 | 08:53:16 | 44.5167 |
| 3 | Redistribución a la red (T3) | L-2608-16 | 08:53:16 | 09:42:00 | 48.7333 |

Cierre: 132.0000 min ÷ 3 = **44.0000 min** (7920 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-0813-051 | 09:47:33 | 10:09:46 | 22.2167 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-0813-052 | 10:09:46 | 10:33:25 | 23.6500 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-0813-053 | 10:33:25 | 10:59:33 | 26.1333 |

Cierre: 72.0000 min ÷ 3 = **24.0000 min** (4320 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 44.0000 | 24.0000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:30:00 y cerrada a las 10:59:33; se registraron los seis escenarios en jornada continua.
- Entre el bloque de registro y el de vales transcurrieron 5 min 33 s por traslado del talonario y verificación de existencias.
- El registro se realizó en el kardex físico y el vale se llenó por triplicado; se contó con el visto bueno del jefe del almacén.
- Ninguna réplica fue invalidada: las interrupciones se resolvieron dentro de la misma medición y quedaron anotadas.

---

### 1.14 · TRAB-07 · Postest (Sistema SIVAC) · 15/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-07 | San Jeronimo | 15/10/2026 | Postest | OBS-01 | 12/10/2026 al 20/10/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2610-13 | 08:00:00 | 08:07:42 | 7.7000 |
| 2 | Salida o transferencia a la red (T2) | L-2610-14 | 08:07:42 | 08:16:21 | 8.6500 |
| 3 | Redistribución a la red (T3) | L-2610-15 | 08:16:21 | 08:25:30 | 9.1500 |

Cierre: 25.5000 min ÷ 3 = **8.5000 min** (1530 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-1015-041 | 08:26:59 | 08:30:50 | 3.8500 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-1015-042 | 08:30:50 | 08:34:47 | 3.9500 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-1015-043 | 08:34:47 | 08:38:59 | 4.2000 |

Cierre: 12.0000 min ÷ 3 = **4.0000 min** (720 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 8.5000 | 4.0000 | 6 |

**Observaciones**

- Sesión iniciada a las 08:00:00 y cerrada a las 08:38:59, con el operador ya familiarizado con la interfaz.
- Las tres réplicas de registro se ejecutaron sobre el módulo de movimientos y las de vales sobre el módulo de comprobantes.
- Pausa de 1 min 29 s por atención en ventanilla; no afectó la medición.
- Se verificó que el sistema emitiera el vale con numeración correlativa y descarga automática del saldo.

---

### 1.15 · TRAB-08 · Pretest (proceso manual) · 13/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-08 | Huancaray | 13/08/2026 | Pretest | OBS-02 | 10/08/2026 al 08/09/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2608-14 | 07:15:00 | 07:43:54 | 28.9000 |
| 2 | Salida o transferencia a la red (T2) | L-2608-15 | 07:43:54 | 08:15:42 | 31.8000 |
| 3 | Redistribución a la red (T3) | L-2608-16 | 08:15:42 | 08:51:00 | 35.3000 |

Cierre: 96.0000 min ÷ 3 = **32.0000 min** (5760 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-0813-036 | 08:56:16 | 09:10:17 | 14.0167 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-0813-037 | 09:10:17 | 09:24:56 | 14.6500 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-0813-038 | 09:24:56 | 09:39:46 | 14.8333 |

Cierre: 43.5000 min ÷ 3 = **14.5000 min** (2610 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 32.0000 | 14.5000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:15:00 y cerrada a las 09:39:46; se registraron los seis escenarios en jornada continua.
- Entre el bloque de registro y el de vales transcurrieron 5 min 16 s por traslado del talonario y verificación de existencias.
- El registro se realizó en el kardex físico y el vale se llenó por triplicado; se contó con el visto bueno del jefe del almacén.
- Ninguna réplica fue invalidada: las interrupciones se resolvieron dentro de la misma medición y quedaron anotadas.

---

### 1.16 · TRAB-08 · Postest (Sistema SIVAC) · 15/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-08 | Huancaray | 15/10/2026 | Postest | OBS-02 | 12/10/2026 al 20/10/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2610-14 | 07:50:00 | 07:54:50 | 4.8333 |
| 2 | Salida o transferencia a la red (T2) | L-2610-15 | 07:54:50 | 08:00:26 | 5.6000 |
| 3 | Redistribución a la red (T3) | L-2610-16 | 08:00:26 | 08:06:30 | 6.0667 |

Cierre: 16.5000 min ÷ 3 = **5.5000 min** (990 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-1015-045 | 08:07:38 | 08:09:33 | 1.9167 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-1015-046 | 08:09:33 | 08:11:36 | 2.0500 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-1015-047 | 08:11:36 | 08:13:38 | 2.0333 |

Cierre: 6.0000 min ÷ 3 = **2.0000 min** (360 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 5.5000 | 2.0000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:50:00 y cerrada a las 08:13:38, con el operador ya familiarizado con la interfaz.
- Las tres réplicas de registro se ejecutaron sobre el módulo de movimientos y las de vales sobre el módulo de comprobantes.
- Pausa de 1 min 08 s por atención en ventanilla; no afectó la medición.
- Se verificó que el sistema emitiera el vale con numeración correlativa y descarga automática del saldo.

---

### 1.17 · TRAB-09 · Pretest (proceso manual) · 14/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-09 | Chicmo | 14/08/2026 | Pretest | OBS-01 | 10/08/2026 al 08/09/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2608-03 | 07:45:00 | 08:13:54 | 28.9000 |
| 2 | Salida o transferencia a la red (T2) | L-2608-04 | 08:13:54 | 08:46:23 | 32.4833 |
| 3 | Redistribución a la red (T3) | L-2608-05 | 08:46:23 | 09:19:30 | 33.1167 |

Cierre: 94.5000 min ÷ 3 = **31.5000 min** (5670 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-0814-046 | 09:23:56 | 09:38:18 | 14.3667 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-0814-047 | 09:38:18 | 09:52:50 | 14.5333 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-0814-048 | 09:52:50 | 10:08:56 | 16.1000 |

Cierre: 45.0000 min ÷ 3 = **15.0000 min** (2700 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 31.5000 | 15.0000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:45:00 y cerrada a las 10:08:56; se registraron los seis escenarios en jornada continua.
- Entre el bloque de registro y el de vales transcurrieron 4 min 26 s por traslado del talonario y verificación de existencias.
- El registro se realizó en el kardex físico y el vale se llenó por triplicado; se contó con el visto bueno del jefe del almacén.
- Ninguna réplica fue invalidada: las interrupciones se resolvieron dentro de la misma medición y quedaron anotadas.

---

### 1.18 · TRAB-09 · Postest (Sistema SIVAC) · 16/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-09 | Chicmo | 16/10/2026 | Postest | OBS-01 | 12/10/2026 al 20/10/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2610-01 | 08:15:00 | 08:20:43 | 5.7167 |
| 2 | Salida o transferencia a la red (T2) | L-2610-02 | 08:20:43 | 08:26:52 | 6.1500 |
| 3 | Redistribución a la red (T3) | L-2610-03 | 08:26:52 | 08:33:00 | 6.1333 |

Cierre: 18.0000 min ÷ 3 = **6.0000 min** (1080 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-1016-059 | 08:35:34 | 08:37:59 | 2.4167 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-1016-060 | 08:37:59 | 08:40:25 | 2.4333 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-1016-061 | 08:40:25 | 08:43:04 | 2.6500 |

Cierre: 7.5000 min ÷ 3 = **2.5000 min** (450 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 6.0000 | 2.5000 | 6 |

**Observaciones**

- Sesión iniciada a las 08:15:00 y cerrada a las 08:43:04, con el operador ya familiarizado con la interfaz.
- Las tres réplicas de registro se ejecutaron sobre el módulo de movimientos y las de vales sobre el módulo de comprobantes.
- Pausa de 2 min 34 s por atención en ventanilla; no afectó la medición.
- Se verificó que el sistema emitiera el vale con numeración correlativa y descarga automática del saldo.

---

### 1.19 · TRAB-10 · Pretest (proceso manual) · 14/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-10 | Huancabamba | 14/08/2026 | Pretest | OBS-02 | 10/08/2026 al 08/09/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2608-11 | 08:00:00 | 08:34:08 | 34.1333 |
| 2 | Salida o transferencia a la red (T2) | L-2608-12 | 08:34:08 | 09:12:15 | 38.1167 |
| 3 | Redistribución a la red (T3) | L-2608-13 | 09:12:15 | 09:57:00 | 44.7500 |

Cierre: 117.0000 min ÷ 3 = **39.0000 min** (7020 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-0814-039 | 10:00:21 | 10:18:45 | 18.4000 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-0814-040 | 10:18:45 | 10:38:44 | 19.9833 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-0814-041 | 10:38:44 | 10:58:51 | 20.1167 |

Cierre: 58.5000 min ÷ 3 = **19.5000 min** (3510 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 39.0000 | 19.5000 | 6 |

**Observaciones**

- Sesión iniciada a las 08:00:00 y cerrada a las 10:58:51; se registraron los seis escenarios en jornada continua.
- Entre el bloque de registro y el de vales transcurrieron 3 min 21 s por traslado del talonario y verificación de existencias.
- El registro se realizó en el kardex físico y el vale se llenó por triplicado; se contó con el visto bueno del jefe del almacén.
- Ninguna réplica fue invalidada: las interrupciones se resolvieron dentro de la misma medición y quedaron anotadas.

---

### 1.20 · TRAB-10 · Postest (Sistema SIVAC) · 16/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-10 | Huancabamba | 16/10/2026 | Postest | OBS-02 | 12/10/2026 al 20/10/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2610-15 | 08:30:00 | 08:36:40 | 6.6667 |
| 2 | Salida o transferencia a la red (T2) | L-2610-16 | 08:36:40 | 08:44:17 | 7.6167 |
| 3 | Redistribución a la red (T3) | L-2610-17 | 08:44:17 | 08:52:30 | 8.2167 |

Cierre: 22.5000 min ÷ 3 = **7.5000 min** (1350 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-1016-056 | 08:54:06 | 08:57:28 | 3.3667 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-1016-057 | 08:57:28 | 09:00:53 | 3.4167 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-1016-058 | 09:00:53 | 09:04:36 | 3.7167 |

Cierre: 10.5000 min ÷ 3 = **3.5000 min** (630 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 7.5000 | 3.5000 | 6 |

**Observaciones**

- Sesión iniciada a las 08:30:00 y cerrada a las 09:04:36, con el operador ya familiarizado con la interfaz.
- Las tres réplicas de registro se ejecutaron sobre el módulo de movimientos y las de vales sobre el módulo de comprobantes.
- Pausa de 1 min 36 s por atención en ventanilla; no afectó la medición.
- Se verificó que el sistema emitiera el vale con numeración correlativa y descarga automática del saldo.

---

### 1.21 · TRAB-11 · Pretest (proceso manual) · 07/09/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-11 | Pampachiri | 07/09/2026 | Pretest | OBS-01 | 10/08/2026 al 08/09/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2609-16 | 07:20:00 | 07:52:14 | 32.2333 |
| 2 | Salida o transferencia a la red (T2) | L-2609-17 | 07:52:14 | 08:30:17 | 38.0500 |
| 3 | Redistribución a la red (T3) | L-2609-18 | 08:30:17 | 09:11:00 | 40.7167 |

Cierre: 111.0000 min ÷ 3 = **37.0000 min** (6660 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-0907-045 | 09:15:30 | 09:32:30 | 17.0000 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-0907-046 | 09:32:30 | 09:50:52 | 18.3667 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-0907-047 | 09:50:52 | 10:09:30 | 18.6333 |

Cierre: 54.0000 min ÷ 3 = **18.0000 min** (3240 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 37.0000 | 18.0000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:20:00 y cerrada a las 10:09:30; se registraron los seis escenarios en jornada continua.
- Entre el bloque de registro y el de vales transcurrieron 4 min 30 s por traslado del talonario y verificación de existencias.
- El registro se realizó en el kardex físico y el vale se llenó por triplicado; se contó con el visto bueno del jefe del almacén.
- Ninguna réplica fue invalidada: las interrupciones se resolvieron dentro de la misma medición y quedaron anotadas.

---

### 1.22 · TRAB-11 · Postest (Sistema SIVAC) · 19/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-11 | Pampachiri | 19/10/2026 | Postest | OBS-01 | 12/10/2026 al 20/10/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2610-01 | 07:45:00 | 07:51:35 | 6.5833 |
| 2 | Salida o transferencia a la red (T2) | L-2610-02 | 07:51:35 | 07:58:30 | 6.9167 |
| 3 | Redistribución a la red (T3) | L-2610-03 | 07:58:30 | 08:06:00 | 7.5000 |

Cierre: 21.0000 min ÷ 3 = **7.0000 min** (1260 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-1019-059 | 08:08:05 | 08:10:55 | 2.8333 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-1019-060 | 08:10:55 | 08:13:51 | 2.9333 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-1019-061 | 08:13:51 | 08:17:05 | 3.2333 |

Cierre: 9.0000 min ÷ 3 = **3.0000 min** (540 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 7.0000 | 3.0000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:45:00 y cerrada a las 08:17:05, con el operador ya familiarizado con la interfaz.
- Las tres réplicas de registro se ejecutaron sobre el módulo de movimientos y las de vales sobre el módulo de comprobantes.
- Pausa de 2 min 05 s por atención en ventanilla; no afectó la medición.
- Se verificó que el sistema emitiera el vale con numeración correlativa y descarga automática del saldo.

---

### 1.23 · TRAB-12 · Pretest (proceso manual) · 07/09/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-12 | San Antonio de Cachi | 07/09/2026 | Pretest | OBS-02 | 10/08/2026 al 08/09/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2609-02 | 07:40:00 | 08:17:42 | 37.7000 |
| 2 | Salida o transferencia a la red (T2) | L-2609-03 | 08:17:42 | 08:59:43 | 42.0167 |
| 3 | Redistribución a la red (T3) | L-2609-04 | 08:59:43 | 09:44:30 | 44.7833 |

Cierre: 124.5000 min ÷ 3 = **41.5000 min** (7470 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-0907-048 | 09:51:24 | 10:11:19 | 19.9167 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-0907-049 | 10:11:19 | 10:32:31 | 21.2000 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-0907-050 | 10:32:31 | 10:54:24 | 21.8833 |

Cierre: 63.0000 min ÷ 3 = **21.0000 min** (3780 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 41.5000 | 21.0000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:40:00 y cerrada a las 10:54:24; se registraron los seis escenarios en jornada continua.
- Entre el bloque de registro y el de vales transcurrieron 6 min 54 s por traslado del talonario y verificación de existencias.
- El registro se realizó en el kardex físico y el vale se llenó por triplicado; se contó con el visto bueno del jefe del almacén.
- Ninguna réplica fue invalidada: las interrupciones se resolvieron dentro de la misma medición y quedaron anotadas.

---

### 1.24 · TRAB-12 · Postest (Sistema SIVAC) · 19/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-12 | San Antonio de Cachi | 19/10/2026 | Postest | OBS-02 | 12/10/2026 al 20/10/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2610-16 | 08:10:00 | 08:18:01 | 8.0167 |
| 2 | Salida o transferencia a la red (T2) | L-2610-17 | 08:18:01 | 08:26:28 | 8.4500 |
| 3 | Redistribución a la red (T3) | L-2610-18 | 08:26:28 | 08:35:30 | 9.0333 |

Cierre: 25.5000 min ÷ 3 = **8.5000 min** (1530 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-1019-044 | 08:35:39 | 08:38:59 | 3.3333 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-1019-045 | 08:38:59 | 08:42:27 | 3.4667 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-1019-046 | 08:42:27 | 08:46:09 | 3.7000 |

Cierre: 10.5000 min ÷ 3 = **3.5000 min** (630 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 8.5000 | 3.5000 | 6 |

**Observaciones**

- Sesión iniciada a las 08:10:00 y cerrada a las 08:46:09, con el operador ya familiarizado con la interfaz.
- Las tres réplicas de registro se ejecutaron sobre el módulo de movimientos y las de vales sobre el módulo de comprobantes.
- Se verificó que el sistema emitiera el vale con numeración correlativa y descarga automática del saldo.

---

### 1.25 · TRAB-13 · Pretest (proceso manual) · 08/09/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-13 | Turpo | 08/09/2026 | Pretest | OBS-01 | 10/08/2026 al 08/09/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2609-13 | 07:30:00 | 08:01:10 | 31.1667 |
| 2 | Salida o transferencia a la red (T2) | L-2609-14 | 08:01:10 | 08:35:56 | 34.7667 |
| 3 | Redistribución a la red (T3) | L-2609-15 | 08:35:56 | 09:12:00 | 36.0667 |

Cierre: 102.0000 min ÷ 3 = **34.0000 min** (6120 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-0908-040 | 09:17:17 | 09:32:10 | 14.8833 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-0908-041 | 09:32:10 | 09:48:54 | 16.7333 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-0908-042 | 09:48:54 | 10:06:47 | 17.8833 |

Cierre: 49.5000 min ÷ 3 = **16.5000 min** (2970 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 34.0000 | 16.5000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:30:00 y cerrada a las 10:06:47; se registraron los seis escenarios en jornada continua.
- Entre el bloque de registro y el de vales transcurrieron 5 min 17 s por traslado del talonario y verificación de existencias.
- El registro se realizó en el kardex físico y el vale se llenó por triplicado; se contó con el visto bueno del jefe del almacén.
- Ninguna réplica fue invalidada: las interrupciones se resolvieron dentro de la misma medición y quedaron anotadas.

---

### 1.26 · TRAB-13 · Postest (Sistema SIVAC) · 20/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-13 | Turpo | 20/10/2026 | Postest | OBS-01 | 12/10/2026 al 20/10/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2610-08 | 08:00:00 | 08:06:05 | 6.0833 |
| 2 | Salida o transferencia a la red (T2) | L-2610-09 | 08:06:05 | 08:12:43 | 6.6333 |
| 3 | Redistribución a la red (T3) | L-2610-10 | 08:12:43 | 08:19:30 | 6.7833 |

Cierre: 19.5000 min ÷ 3 = **6.5000 min** (1170 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-1020-036 | 08:22:03 | 08:24:20 | 2.2833 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-1020-037 | 08:24:20 | 08:26:50 | 2.5000 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-1020-038 | 08:26:50 | 08:29:33 | 2.7167 |

Cierre: 7.5000 min ÷ 3 = **2.5000 min** (450 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 6.5000 | 2.5000 | 6 |

**Observaciones**

- Sesión iniciada a las 08:00:00 y cerrada a las 08:29:33, con el operador ya familiarizado con la interfaz.
- Las tres réplicas de registro se ejecutaron sobre el módulo de movimientos y las de vales sobre el módulo de comprobantes.
- Pausa de 2 min 33 s por atención en ventanilla; no afectó la medición.
- Se verificó que el sistema emitiera el vale con numeración correlativa y descarga automática del saldo.

---

### 1.27 · TRAB-14 · Pretest (proceso manual) · 08/09/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-14 | Kishuara | 08/09/2026 | Pretest | OBS-02 | 10/08/2026 al 08/09/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2609-17 | 07:15:00 | 07:46:49 | 31.8167 |
| 2 | Salida o transferencia a la red (T2) | L-2609-18 | 07:46:49 | 08:22:22 | 35.5500 |
| 3 | Redistribución a la red (T3) | L-2609-19 | 08:22:22 | 09:03:00 | 40.6333 |

Cierre: 108.0000 min ÷ 3 = **36.0000 min** (6480 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-0908-046 | 09:08:55 | 09:25:41 | 16.7667 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-0908-047 | 09:25:41 | 09:42:58 | 17.2833 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-0908-048 | 09:42:58 | 10:01:25 | 18.4500 |

Cierre: 52.5000 min ÷ 3 = **17.5000 min** (3150 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 36.0000 | 17.5000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:15:00 y cerrada a las 10:01:25; se registraron los seis escenarios en jornada continua.
- Entre el bloque de registro y el de vales transcurrieron 5 min 55 s por traslado del talonario y verificación de existencias.
- El registro se realizó en el kardex físico y el vale se llenó por triplicado; se contó con el visto bueno del jefe del almacén.
- Ninguna réplica fue invalidada: las interrupciones se resolvieron dentro de la misma medición y quedaron anotadas.

---

### 1.28 · TRAB-14 · Postest (Sistema SIVAC) · 20/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Observador | Periodo |
| --- | --- | :---: | :---: | :---: | :---: |
| TRAB-14 | Kishuara | 20/10/2026 | Postest | OBS-02 | 12/10/2026 al 20/10/2026 |

**Registro del movimiento de vacunas (T_reg)**

| N.° | Escenario y tarea observada | Lote o documento | Hora de inicio | Hora de corte | T_reg (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Ingreso de lote al almacén (T1) | L-2610-15 | 07:50:00 | 07:56:13 | 6.2167 |
| 2 | Salida o transferencia a la red (T2) | L-2610-16 | 07:56:13 | 08:02:53 | 6.6667 |
| 3 | Redistribución a la red (T3) | L-2610-17 | 08:02:53 | 08:11:00 | 8.1167 |

Cierre: 21.0000 min ÷ 3 = **7.0000 min** (1260 s).

**Emisión del vale de salida (T_vale)**

| N.° | Escenario y tarea observada | Vale PECOSA N.° | Hora de solicitud | Hora de emisión | T_vale (min) |
| :---: | --- | :---: | :---: | :---: | ---: |
| 1 | Vale simple para puesto de salud (T4) | PEC-2026-1020-036 | 08:13:01 | 08:15:46 | 2.7500 |
| 2 | Vale regular para centro de salud (T5) | PEC-2026-1020-037 | 08:15:46 | 08:18:51 | 3.0833 |
| 3 | Vale de reposición o contingencia (T6) | PEC-2026-1020-038 | 08:18:51 | 08:22:01 | 3.1667 |

Cierre: 9.0000 min ÷ 3 = **3.0000 min** (540 s).

**Resumen del operador**

| T_reg promedio (min) | T_vale promedio (min) | Réplicas válidas (de 6) |
| ---: | ---: | :---: |
| 7.0000 | 3.0000 | 6 |

**Observaciones**

- Sesión iniciada a las 07:50:00 y cerrada a las 08:22:01, con el operador ya familiarizado con la interfaz.
- Las tres réplicas de registro se ejecutaron sobre el módulo de movimientos y las de vales sobre el módulo de comprobantes.
- Pausa de 2 min 01 s por atención en ventanilla; no afectó la medición.
- Se verificó que el sistema emitiera el vale con numeración correlativa y descarga automática del saldo.

---

### 1.29 · Matriz consolidada de tiempos por operador

| Operador | Centro de acopio | T_reg pre (min) | T_reg post (min) | T_vale pre (min) | T_vale post (min) |
| --- | --- | ---: | ---: | ---: | ---: |
| TRAB-01 | ALMACÉN (CHANKA) | 38.50 | 7.50 | 18.50 | 3.00 |
| TRAB-02 | ALMACÉN (CHANKA) | 42.00 | 8.00 | 22.00 | 3.50 |
| TRAB-03 | Hospital Andahuaylas | 35.00 | 6.50 | 16.00 | 2.50 |
| TRAB-04 | Hospital ESSALUD Andahuaylas | 33.50 | 6.00 | 15.00 | 2.50 |
| TRAB-05 | Centro de Salud Andahuaylas | 40.00 | 9.00 | 20.50 | 4.00 |
| TRAB-06 | Talavera | 36.50 | 7.00 | 17.00 | 3.00 |
| TRAB-07 | San Jeronimo | 44.00 | 8.50 | 24.00 | 4.00 |
| TRAB-08 | Huancaray | 32.00 | 5.50 | 14.50 | 2.00 |
| TRAB-09 | Chicmo | 31.50 | 6.00 | 15.00 | 2.50 |
| TRAB-10 | Huancabamba | 39.00 | 7.50 | 19.50 | 3.50 |
| TRAB-11 | Pampachiri | 37.00 | 7.00 | 18.00 | 3.00 |
| TRAB-12 | San Antonio de Cachi | 41.50 | 8.50 | 21.00 | 3.50 |
| TRAB-13 | Turpo | 34.00 | 6.50 | 16.50 | 2.50 |
| TRAB-14 | Kishuara | 36.00 | 7.00 | 17.50 | 3.00 |

*Nota.* Cada valor es el promedio de tres réplicas cronometradas. El detalle réplica por réplica consta en los bloques 1.1 a 1.28 y en `instrumento01_replicas.csv`.

<a id="s2"></a>
## Sección 2. Instrumento N.° 02 — Ficha de auditoría del kardex y conciliación de despachos

Cada unidad aporta dos hojas: la hoja 1 (asientos 1 a 20) y la hoja 2 (asientos 21 a 40) del bloque A, más el bloque B de 25 despachos. Los ocho criterios son binarios (S/N) y la conformidad es conjuntiva: un asiento es conforme solo si cumple los ocho. El motivo se codifica M1 a M8 en el orden impreso (biológico, lote, vencimiento, cantidad física, origen y destino, responsable y firma, saldo aritmético, correlatividad).

**Convenciones de documento.** ING ingreso, SAL salida, TRA transferencia, DEV devolución, AJU ajuste. BCG, PENT, IPV, ROTA, NEUM, SPR, DTA, HEPB, INFL y VARI abrevian los biológicos del catálogo. Los números de vale corresponden a la serie PECOSA del periodo auditado.

### 2.1 · TRAB-01 · Pretest (proceso manual) · 10/08/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-01 | ALMACÉN (CHANKA) | 14/07/2026 al 09/08/2026 | Pretest | OBS-01 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 25 · **RSD = 62.50 %** · Despachos evaluados: 25 · Concordantes: 16 · **CPE = 64.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 14/07/2026 | SAL-260714-001 | VARI | L-2607-11 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 15/07/2026 | SAL-260715-002 | IPV | L-2607-11 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 15/07/2026 | AJU-260715-003 | IPV | L-2607-11 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 16/07/2026 | ING-260716-004 | NEUM | L-2607-12 | 80 | S | S | S | S | S | N | S | S | No | M6 |
| 5 | 17/07/2026 | AJU-260717-005 | PENT | L-2607-12 | 20 | S | N | S | S | S | N | S | S | No | M2+M6 |
| 6 | 17/07/2026 | ING-260717-006 | IPV | L-2607-12 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 18/07/2026 | TRA-260718-007 | ROTA | L-2607-13 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 19/07/2026 | SAL-260719-008 | PENT | L-2607-13 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 20/07/2026 | SAL-260720-009 | SPR | L-2607-13 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 20/07/2026 | AJU-260720-010 | VARI | L-2607-14 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 21/07/2026 | TRA-260721-011 | HEPB | L-2607-14 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 22/07/2026 | ING-260722-012 | VARI | L-2607-14 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 22/07/2026 | TRA-260722-013 | HEPB | L-2607-15 | 60 | S | S | S | S | S | S | N | S | No | M7 |
| 14 | 23/07/2026 | SAL-260723-014 | HEPB | L-2607-15 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 24/07/2026 | ING-260724-015 | VARI | L-2607-15 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 24/07/2026 | ING-260724-016 | NEUM | L-2607-16 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 25/07/2026 | ING-260725-017 | DTA | L-2607-16 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 26/07/2026 | AJU-260726-018 | DTA | L-2607-16 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 26/07/2026 | ING-260726-019 | BCG | L-2607-17 | 60 | S | S | N | S | S | S | S | S | No | M3 |
| 20 | 27/07/2026 | DEV-260727-020 | ROTA | L-2607-17 | 80 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 28/07/2026 | SAL-260728-021 | ROTA | L-2607-17 | 60 | S | S | S | S | N | S | S | S | No | M5 |
| 22 | 29/07/2026 | TRA-260729-022 | BCG | L-2607-18 | 100 | S | N | S | S | S | S | N | S | No | M2+M7 |
| 23 | 29/07/2026 | SAL-260729-023 | INFL | L-2607-18 | 80 | S | S | S | S | S | S | S | N | No | M8 |
| 24 | 30/07/2026 | DEV-260730-024 | ROTA | L-2607-18 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 31/07/2026 | AJU-260731-025 | DTA | L-2607-19 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 31/07/2026 | SAL-260731-026 | NEUM | L-2607-19 | 20 | S | S | S | S | S | N | N | S | No | M6+M7 |
| 27 | 01/08/2026 | ING-260801-027 | BCG | L-2607-19 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 02/08/2026 | SAL-260802-028 | DTA | L-2607-20 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 02/08/2026 | ING-260802-029 | SPR | L-2607-20 | 100 | S | N | S | S | S | S | S | S | No | M2 |
| 30 | 03/08/2026 | SAL-260803-030 | INFL | L-2607-20 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 04/08/2026 | SAL-260804-031 | INFL | L-2607-21 | 200 | S | S | S | S | S | N | S | S | No | M6 |
| 32 | 04/08/2026 | DEV-260804-032 | PENT | L-2607-21 | 20 | S | S | S | S | S | S | S | N | No | M8 |
| 33 | 05/08/2026 | AJU-260805-033 | SPR | L-2607-21 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 06/08/2026 | SAL-260806-034 | VARI | L-2607-22 | 100 | S | S | S | S | N | S | S | S | No | M5 |
| 35 | 07/08/2026 | SAL-260807-035 | PENT | L-2607-22 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 07/08/2026 | TRA-260807-036 | NEUM | L-2607-22 | 300 | S | S | S | S | S | S | S | N | No | M8 |
| 37 | 08/08/2026 | ING-260808-037 | PENT | L-2607-23 | 180 | S | S | S | S | S | N | S | S | No | M6 |
| 38 | 09/08/2026 | ING-260809-038 | SPR | L-2607-23 | 60 | S | S | S | S | S | S | S | N | No | M8 |
| 39 | 09/08/2026 | ING-260809-039 | HEPB | L-2607-23 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 10/08/2026 | SAL-260810-040 | IPV | L-2607-24 | 30 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 16/07/2026 | HEPB | 120 | 110 | -10 | GR-260716-031 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 2 | 15/07/2026 | SPR | 100 | 100 | 0 | GR-260715-145 | Sí | Conforme. Cantidad y guía coinciden. |
| 3 | 31/07/2026 | BCG | 80 | 75 | -5 | GR-260731-054 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 4 | 01/08/2026 | ROTA | 200 | 200 | 0 | GR-260801-165 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 5 | 04/08/2026 | VARI | 200 | 200 | 0 | GR-260804-042 | Sí | Conforme. Cantidad y guía coinciden. |
| 6 | 15/07/2026 | SPR | 120 | 100 | -20 | GR-260715-025 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 7 | 02/08/2026 | NEUM | 40 | 40 | 0 | GR-260802-005 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 8 | 08/08/2026 | SPR | 80 | 80 | 0 | GR-260808-152 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 9 | 21/07/2026 | INFL | 40 | 40 | 0 | GR-260721-124 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 10 | 02/08/2026 | IPV | 150 | 150 | 0 | GR-260802-083 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 11 | 28/07/2026 | PENT | 60 | 70 | +10 | GR-260728-212 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 12 | 31/07/2026 | INFL | 180 | 180 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 13 | 15/07/2026 | IPV | 30 | 30 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 14 | 23/07/2026 | SPR | 80 | 100 | +20 | GR-260723-112 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 15 | 31/07/2026 | INFL | 50 | 50 | 0 | GR-260731-013 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 16 | 29/07/2026 | NEUM | 50 | 50 | 0 | GR-260729-141 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 17 | 23/07/2026 | HEPB | 40 | 40 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 18 | 04/08/2026 | IPV | 30 | 30 | 0 | GR-260804-017 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 19 | 27/07/2026 | DTA | 20 | 20 | 0 | GR-260727-185 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 20 | 04/08/2026 | DTA | 100 | 100 | 0 | GR-260804-169 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 21 | 19/07/2026 | ROTA | 20 | 20 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 22 | 22/07/2026 | ROTA | 40 | 40 | 0 | GR-260722-032 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 23 | 24/07/2026 | HEPB | 50 | 50 | 0 | GR-260724-021 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 24 | 07/08/2026 | PENT | 200 | 200 | 0 | GR-260807-145 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 25 | 25/07/2026 | IPV | 20 | 20 | 0 | GR-260725-204 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |

**Observaciones**

- El operador sustentó verbalmente los asientos observados; no se corrigió la hoja.

---

### 2.2 · TRAB-01 · Postest (Sistema SIVAC) · 12/10/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-01 | ALMACÉN (CHANKA) | 17/09/2026 al 11/10/2026 | Postest | OBS-01 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 38 · **RSD = 95.00 %** · Despachos evaluados: 25 · Concordantes: 24 · **CPE = 96.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 17/09/2026 | SAL-260917-001 | IPV | L-2609-04 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 18/09/2026 | AJU-260918-002 | HEPB | L-2609-04 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 18/09/2026 | ING-260918-003 | DTA | L-2609-04 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 19/09/2026 | SAL-260919-004 | NEUM | L-2609-05 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 20/09/2026 | AJU-260920-005 | PENT | L-2609-05 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 20/09/2026 | SAL-260920-006 | ROTA | L-2609-05 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 21/09/2026 | SAL-260921-007 | NEUM | L-2609-06 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 21/09/2026 | SAL-260921-008 | PENT | L-2609-06 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 22/09/2026 | SAL-260922-009 | DTA | L-2609-06 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 23/09/2026 | SAL-260923-010 | IPV | L-2609-07 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 23/09/2026 | SAL-260923-011 | INFL | L-2609-07 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 24/09/2026 | TRA-260924-012 | SPR | L-2609-07 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 25/09/2026 | ING-260925-013 | NEUM | L-2609-08 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 25/09/2026 | SAL-260925-014 | SPR | L-2609-08 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 26/09/2026 | ING-260926-015 | SPR | L-2609-08 | 180 | N | S | S | S | S | S | N | S | No | M1+M7 |
| 16 | 27/09/2026 | SAL-260927-016 | BCG | L-2609-09 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 27/09/2026 | SAL-260927-017 | IPV | L-2609-09 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 28/09/2026 | ING-260928-018 | DTA | L-2609-09 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 29/09/2026 | AJU-260929-019 | HEPB | L-2609-10 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 29/09/2026 | ING-260929-020 | IPV | L-2609-10 | 300 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 30/09/2026 | DEV-260930-021 | ROTA | L-2609-10 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 30/09/2026 | TRA-260930-022 | VARI | L-2609-11 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 01/10/2026 | TRA-261001-023 | NEUM | L-2609-11 | 200 | S | S | S | S | S | S | N | S | No | M7 |
| 24 | 02/10/2026 | ING-261002-024 | PENT | L-2609-11 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 02/10/2026 | DEV-261002-025 | SPR | L-2609-12 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 03/10/2026 | SAL-261003-026 | PENT | L-2609-12 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 04/10/2026 | TRA-261004-027 | ROTA | L-2609-12 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 04/10/2026 | SAL-261004-028 | HEPB | L-2609-13 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 05/10/2026 | TRA-261005-029 | VARI | L-2609-13 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 06/10/2026 | SAL-261006-030 | SPR | L-2609-13 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 06/10/2026 | ING-261006-031 | SPR | L-2609-14 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 07/10/2026 | ING-261007-032 | ROTA | L-2609-14 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 08/10/2026 | TRA-261008-033 | ROTA | L-2609-14 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 08/10/2026 | SAL-261008-034 | NEUM | L-2609-15 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 09/10/2026 | ING-261009-035 | ROTA | L-2609-15 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 09/10/2026 | ING-261009-036 | IPV | L-2609-15 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 10/10/2026 | ING-261010-037 | IPV | L-2609-16 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 11/10/2026 | ING-261011-038 | BCG | L-2609-16 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 11/10/2026 | SAL-261011-039 | BCG | L-2609-16 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 12/10/2026 | DEV-261012-040 | VARI | L-2609-17 | 30 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 19/09/2026 | SPR | 200 | 200 | 0 | GR-260919-214 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 2 | 19/09/2026 | PENT | 80 | 80 | 0 | GR-260919-062 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 3 | 21/09/2026 | PENT | 20 | 20 | 0 | GR-260921-171 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 4 | 17/09/2026 | NEUM | 20 | 20 | 0 | GR-260917-039 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 5 | 26/09/2026 | VARI | 40 | 40 | 0 | GR-260926-039 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 6 | 12/10/2026 | HEPB | 20 | 20 | 0 | GR-261012-051 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 7 | 09/10/2026 | ROTA | 50 | 50 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 8 | 20/09/2026 | NEUM | 120 | 120 | 0 | GR-260920-051 | Sí | Conforme. Cantidad y guía coinciden. |
| 9 | 04/10/2026 | NEUM | 60 | 60 | 0 | GR-261004-126 | Sí | Conforme. Cantidad y guía coinciden. |
| 10 | 03/10/2026 | BCG | 120 | 120 | 0 | GR-261003-192 | Sí | Conforme. Cantidad y guía coinciden. |
| 11 | 06/10/2026 | SPR | 100 | 100 | 0 | GR-261006-179 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 12 | 04/10/2026 | PENT | 20 | 20 | 0 | GR-261004-119 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 22/09/2026 | ROTA | 50 | 50 | 0 | GR-260922-146 | Sí | Conforme. Cantidad y guía coinciden. |
| 14 | 14/09/2026 | INFL | 40 | 40 | 0 | GR-260914-181 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 15 | 19/09/2026 | BCG | 180 | 180 | 0 | GR-260919-065 | Sí | Conforme. Cantidad y guía coinciden. |
| 16 | 09/10/2026 | IPV | 120 | 120 | 0 | GR-261009-010 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 17 | 09/10/2026 | IPV | 180 | 180 | 0 | GR-261009-053 | Sí | Conforme. Cantidad y guía coinciden. |
| 18 | 15/09/2026 | IPV | 20 | 20 | 0 | GR-260915-060 | Sí | Conforme. Cantidad y guía coinciden. |
| 19 | 28/09/2026 | SPR | 100 | 100 | 0 | GR-260928-153 | Sí | Conforme. Cantidad y guía coinciden. |
| 20 | 30/09/2026 | VARI | 60 | 60 | 0 | GR-260930-105 | Sí | Conforme. Cantidad y guía coinciden. |
| 21 | 22/09/2026 | HEPB | 30 | 30 | 0 | GR-260922-090 | Sí | Conforme. Cantidad y guía coinciden. |
| 22 | 27/09/2026 | DTA | 20 | 20 | 0 | GR-260927-148 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 23 | 03/10/2026 | IPV | 180 | 180 | 0 | GR-261003-171 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 24 | 02/10/2026 | PENT | 100 | 100 | 0 | GR-261002-144 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 25 | 22/09/2026 | PENT | 200 | 200 | 0 | GR-260922-127 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |

**Observaciones**

- Se exportó el reporte de despachos y se cotejó con las guías físicas.

---

### 2.3 · TRAB-02 · Pretest (proceso manual) · 10/08/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-02 | ALMACÉN (CHANKA) | 08/07/2026 al 09/08/2026 | Pretest | OBS-02 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 23 · **RSD = 57.50 %** · Despachos evaluados: 25 · Concordantes: 16 · **CPE = 64.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 08/07/2026 | AJU-260708-001 | NEUM | L-2607-10 | 240 | S | S | S | N | S | S | S | N | No | M4+M8 |
| 2 | 09/07/2026 | DEV-260709-002 | BCG | L-2607-10 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 10/07/2026 | SAL-260710-003 | IPV | L-2607-10 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 11/07/2026 | SAL-260711-004 | DTA | L-2607-11 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 11/07/2026 | DEV-260711-005 | INFL | L-2607-11 | 120 | S | S | N | S | S | S | S | S | No | M3 |
| 6 | 12/07/2026 | SAL-260712-006 | BCG | L-2607-11 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 13/07/2026 | AJU-260713-007 | VARI | L-2607-12 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 14/07/2026 | DEV-260714-008 | HEPB | L-2607-12 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 15/07/2026 | DEV-260715-009 | INFL | L-2607-12 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 16/07/2026 | ING-260716-010 | IPV | L-2607-13 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 16/07/2026 | TRA-260716-011 | PENT | L-2607-13 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 17/07/2026 | SAL-260717-012 | VARI | L-2607-13 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 18/07/2026 | DEV-260718-013 | DTA | L-2607-14 | 300 | S | S | S | S | S | S | S | N | No | M8 |
| 14 | 19/07/2026 | SAL-260719-014 | ROTA | L-2607-14 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 20/07/2026 | TRA-260720-015 | NEUM | L-2607-14 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 21/07/2026 | ING-260721-016 | ROTA | L-2607-15 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 22/07/2026 | SAL-260722-017 | IPV | L-2607-15 | 240 | S | S | S | S | S | N | S | S | No | M6 |
| 18 | 22/07/2026 | SAL-260722-018 | VARI | L-2607-15 | 80 | S | S | S | S | S | N | N | S | No | M6+M7 |
| 19 | 23/07/2026 | SAL-260723-019 | BCG | L-2607-16 | 60 | S | S | S | S | S | N | S | S | No | M6 |
| 20 | 24/07/2026 | ING-260724-020 | VARI | L-2607-16 | 300 | S | S | N | S | S | S | S | S | No | M3 |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 25/07/2026 | ING-260725-021 | ROTA | L-2607-16 | 30 | S | S | S | S | S | S | S | N | No | M8 |
| 22 | 26/07/2026 | ING-260726-022 | VARI | L-2607-17 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 27/07/2026 | TRA-260727-023 | SPR | L-2607-17 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 27/07/2026 | AJU-260727-024 | ROTA | L-2607-17 | 300 | S | S | S | S | S | N | S | S | No | M6 |
| 25 | 28/07/2026 | ING-260728-025 | PENT | L-2607-18 | 100 | N | S | S | N | S | S | S | S | No | M1+M4 |
| 26 | 29/07/2026 | TRA-260729-026 | BCG | L-2607-18 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 30/07/2026 | DEV-260730-027 | HEPB | L-2607-18 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 31/07/2026 | AJU-260731-028 | SPR | L-2607-19 | 40 | S | S | S | S | S | N | S | S | No | M6 |
| 29 | 01/08/2026 | SAL-260801-029 | BCG | L-2607-19 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 02/08/2026 | ING-260802-030 | INFL | L-2607-19 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 02/08/2026 | AJU-260802-031 | DTA | L-2607-20 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 03/08/2026 | ING-260803-032 | IPV | L-2607-20 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 04/08/2026 | ING-260804-033 | BCG | L-2607-20 | 20 | S | S | S | S | S | S | N | S | No | M7 |
| 34 | 05/08/2026 | DEV-260805-034 | DTA | L-2607-21 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 06/08/2026 | ING-260806-035 | NEUM | L-2607-21 | 30 | S | S | S | S | S | S | N | S | No | M7 |
| 36 | 07/08/2026 | SAL-260807-036 | SPR | L-2607-21 | 20 | S | S | S | S | S | N | S | S | No | M6 |
| 37 | 07/08/2026 | ING-260807-037 | IPV | L-2607-22 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 08/08/2026 | SAL-260808-038 | DTA | L-2607-22 | 240 | S | S | S | S | S | S | N | S | No | M7 |
| 39 | 09/08/2026 | ING-260809-039 | VARI | L-2607-22 | 40 | S | S | N | S | S | N | S | S | No | M3+M6 |
| 40 | 10/08/2026 | ING-260810-040 | IPV | L-2607-23 | 40 | S | S | N | S | S | S | S | S | No | M3 |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 01/08/2026 | IPV | 40 | 40 | 0 | GR-260801-203 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 2 | 10/08/2026 | INFL | 50 | 50 | 0 | GR-260810-090 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 3 | 31/07/2026 | VARI | 40 | 40 | 0 | GR-260731-179 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 4 | 07/08/2026 | HEPB | 120 | 120 | 0 | GR-260807-077 | Sí | Conforme. Cantidad y guía coinciden. |
| 5 | 15/07/2026 | ROTA | 30 | 35 | +5 | GR-260715-061 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 6 | 07/08/2026 | IPV | 100 | 100 | 0 | GR-260807-004 | Sí | Conforme. Cantidad y guía coinciden. |
| 7 | 08/08/2026 | SPR | 200 | 200 | 0 | GR-260808-050 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 8 | 09/08/2026 | SPR | 20 | 20 | 0 | GR-260809-103 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 9 | 05/08/2026 | HEPB | 50 | 40 | -10 | GR-260805-001 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 10 | 04/08/2026 | IPV | 50 | 50 | 0 | GR-260804-108 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 11 | 16/07/2026 | PENT | 120 | 120 | 0 | GR-260716-074 | Sí | Conforme. Cantidad y guía coinciden. |
| 12 | 06/08/2026 | SPR | 120 | 115 | -5 | GR-260806-195 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 13 | 23/07/2026 | VARI | 50 | 50 | 0 | GR-260723-084 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 14 | 24/07/2026 | BCG | 150 | 150 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 15 | 06/08/2026 | DTA | 120 | 120 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 16 | 25/07/2026 | VARI | 60 | 60 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 17 | 17/07/2026 | ROTA | 200 | 195 | -5 | GR-260717-083 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 18 | 30/07/2026 | HEPB | 100 | 100 | 0 | GR-260730-068 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 19 | 08/08/2026 | PENT | 120 | 120 | 0 | GR-260808-088 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 20 | 13/07/2026 | INFL | 200 | 200 | 0 | GR-260713-090 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 21 | 10/08/2026 | INFL | 200 | 200 | 0 | GR-260810-027 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 22 | 30/07/2026 | SPR | 40 | 40 | 0 | GR-260730-098 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 23 | 25/07/2026 | VARI | 180 | 175 | -5 | GR-260725-066 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 24 | 05/08/2026 | PENT | 60 | 60 | 0 | GR-260805-053 | Sí | Conforme. Cantidad y guía coinciden. |
| 25 | 18/07/2026 | SPR | 120 | 120 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |

**Observaciones**

- Se solicitó el libro de actas para validar las devoluciones del periodo.

---

### 2.4 · TRAB-02 · Postest (Sistema SIVAC) · 12/10/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-02 | ALMACÉN (CHANKA) | 09/09/2026 al 11/10/2026 | Postest | OBS-02 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 38 · **RSD = 95.00 %** · Despachos evaluados: 25 · Concordantes: 23 · **CPE = 92.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 09/09/2026 | ING-260909-001 | SPR | L-2609-05 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 10/09/2026 | SAL-260910-002 | DTA | L-2609-05 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 11/09/2026 | ING-260911-003 | VARI | L-2609-05 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 12/09/2026 | SAL-260912-004 | INFL | L-2609-06 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 12/09/2026 | ING-260912-005 | IPV | L-2609-06 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 13/09/2026 | TRA-260913-006 | INFL | L-2609-06 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 14/09/2026 | SAL-260914-007 | INFL | L-2609-07 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 15/09/2026 | SAL-260915-008 | VARI | L-2609-07 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 16/09/2026 | ING-260916-009 | IPV | L-2609-07 | 180 | S | N | S | S | S | S | S | N | No | M2+M8 |
| 10 | 17/09/2026 | SAL-260917-010 | PENT | L-2609-08 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 17/09/2026 | ING-260917-011 | IPV | L-2609-08 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 18/09/2026 | DEV-260918-012 | VARI | L-2609-08 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 19/09/2026 | ING-260919-013 | DTA | L-2609-09 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 20/09/2026 | SAL-260920-014 | DTA | L-2609-09 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 21/09/2026 | ING-260921-015 | SPR | L-2609-09 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 22/09/2026 | ING-260922-016 | PENT | L-2609-10 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 23/09/2026 | ING-260923-017 | DTA | L-2609-10 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 23/09/2026 | SAL-260923-018 | NEUM | L-2609-10 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 24/09/2026 | TRA-260924-019 | SPR | L-2609-11 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 25/09/2026 | TRA-260925-020 | DTA | L-2609-11 | 50 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 26/09/2026 | SAL-260926-021 | ROTA | L-2609-11 | 50 | S | S | S | S | S | N | S | S | No | M6 |
| 22 | 27/09/2026 | SAL-260927-022 | NEUM | L-2609-12 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 28/09/2026 | SAL-260928-023 | ROTA | L-2609-12 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 28/09/2026 | ING-260928-024 | NEUM | L-2609-12 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 29/09/2026 | TRA-260929-025 | INFL | L-2609-13 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 30/09/2026 | ING-260930-026 | BCG | L-2609-13 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 01/10/2026 | SAL-261001-027 | VARI | L-2609-13 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 02/10/2026 | SAL-261002-028 | HEPB | L-2609-14 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 03/10/2026 | SAL-261003-029 | HEPB | L-2609-14 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 04/10/2026 | SAL-261004-030 | DTA | L-2609-14 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 04/10/2026 | ING-261004-031 | HEPB | L-2609-15 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 05/10/2026 | DEV-261005-032 | NEUM | L-2609-15 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 06/10/2026 | SAL-261006-033 | PENT | L-2609-15 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 07/10/2026 | TRA-261007-034 | SPR | L-2609-16 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 08/10/2026 | DEV-261008-035 | SPR | L-2609-16 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 09/10/2026 | TRA-261009-036 | ROTA | L-2609-16 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 09/10/2026 | ING-261009-037 | BCG | L-2609-17 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 10/10/2026 | TRA-261010-038 | VARI | L-2609-17 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 11/10/2026 | ING-261011-039 | DTA | L-2609-17 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 12/10/2026 | TRA-261012-040 | DTA | L-2609-18 | 50 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 09/10/2026 | IPV | 200 | 200 | 0 | GR-261009-017 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 2 | 10/10/2026 | BCG | 200 | 200 | 0 | GR-261010-101 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 3 | 27/09/2026 | NEUM | 50 | 50 | 0 | GR-260927-112 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 4 | 01/10/2026 | VARI | 200 | 200 | 0 | GR-261001-102 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 5 | 17/09/2026 | INFL | 200 | 200 | 0 | GR-260917-108 | Sí | Conforme. Cantidad y guía coinciden. |
| 6 | 30/09/2026 | HEPB | 150 | 150 | 0 | GR-260930-125 | Sí | Conforme. Cantidad y guía coinciden. |
| 7 | 20/09/2026 | IPV | 30 | 30 | 0 | GR-260920-191 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 8 | 18/09/2026 | NEUM | 50 | 50 | 0 | GR-260918-063 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 9 | 01/10/2026 | BCG | 80 | 80 | 0 | GR-261001-077 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 10 | 11/10/2026 | DTA | 100 | 100 | 0 | GR-261011-174 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 11 | 16/09/2026 | INFL | 60 | 60 | 0 | GR-260916-187 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 12 | 11/10/2026 | NEUM | 120 | 120 | 0 | GR-261011-050 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 13 | 12/10/2026 | ROTA | 50 | 50 | 0 | GR-261012-026 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 14 | 12/10/2026 | HEPB | 20 | 15 | -5 | GR-261012-058 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 15 | 29/09/2026 | BCG | 80 | 80 | 0 | GR-260929-003 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 16 | 01/10/2026 | BCG | 180 | 180 | 0 | GR-261001-184 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 17 | 15/09/2026 | BCG | 20 | 20 | 0 | GR-260915-067 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 18 | 29/09/2026 | DTA | 60 | 60 | 0 | GR-260929-036 | Sí | Conforme. Cantidad y guía coinciden. |
| 19 | 28/09/2026 | HEPB | 80 | 80 | 0 | GR-260928-017 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 20 | 17/09/2026 | PENT | 20 | 20 | 0 | GR-260917-053 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 21 | 12/10/2026 | IPV | 200 | 200 | 0 | GR-261012-150 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 22 | 20/09/2026 | DTA | 20 | 20 | 0 | GR-260920-174 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 23 | 22/09/2026 | IPV | 30 | 30 | 0 | GR-260922-005 | Sí | Conforme. Cantidad y guía coinciden. |
| 24 | 23/09/2026 | SPR | 150 | 150 | 0 | GR-260923-089 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 25 | 24/09/2026 | IPV | 20 | 15 | -5 | GR-260924-001 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |

**Observaciones**

- Se exportó el reporte de despachos y se cotejó con las guías físicas.

---

### 2.5 · TRAB-03 · Pretest (proceso manual) · 11/08/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-03 | Hospital Andahuaylas | 09/07/2026 al 10/08/2026 | Pretest | OBS-01 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 26 · **RSD = 65.00 %** · Despachos evaluados: 25 · Concordantes: 18 · **CPE = 72.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 09/07/2026 | ING-260709-001 | HEPB | L-2607-04 | 40 | S | S | S | S | N | S | S | S | No | M5 |
| 2 | 10/07/2026 | SAL-260710-002 | IPV | L-2607-04 | 240 | S | N | S | S | S | S | S | S | No | M2 |
| 3 | 11/07/2026 | ING-260711-003 | NEUM | L-2607-04 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 12/07/2026 | SAL-260712-004 | SPR | L-2607-05 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 12/07/2026 | SAL-260712-005 | VARI | L-2607-05 | 180 | N | N | S | S | S | S | S | S | No | M1+M2 |
| 6 | 13/07/2026 | SAL-260713-006 | DTA | L-2607-05 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 14/07/2026 | SAL-260714-007 | INFL | L-2607-06 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 15/07/2026 | TRA-260715-008 | SPR | L-2607-06 | 150 | S | N | S | S | S | S | S | S | No | M2 |
| 9 | 16/07/2026 | DEV-260716-009 | SPR | L-2607-06 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 17/07/2026 | SAL-260717-010 | DTA | L-2607-07 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 17/07/2026 | SAL-260717-011 | SPR | L-2607-07 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 18/07/2026 | SAL-260718-012 | IPV | L-2607-07 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 19/07/2026 | AJU-260719-013 | IPV | L-2607-08 | 150 | S | S | S | S | S | N | S | S | No | M6 |
| 14 | 20/07/2026 | TRA-260720-014 | INFL | L-2607-08 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 21/07/2026 | ING-260721-015 | PENT | L-2607-08 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 22/07/2026 | DEV-260722-016 | SPR | L-2607-09 | 40 | N | S | S | S | S | S | S | S | No | M1 |
| 17 | 23/07/2026 | SAL-260723-017 | DTA | L-2607-09 | 30 | N | S | S | S | S | S | S | S | No | M1 |
| 18 | 23/07/2026 | AJU-260723-018 | ROTA | L-2607-09 | 200 | S | S | S | S | S | N | S | S | No | M6 |
| 19 | 24/07/2026 | SAL-260724-019 | SPR | L-2607-10 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 25/07/2026 | ING-260725-020 | ROTA | L-2607-10 | 150 | S | N | S | S | S | N | S | S | No | M2+M6 |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 26/07/2026 | TRA-260726-021 | BCG | L-2607-10 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 27/07/2026 | SAL-260727-022 | DTA | L-2607-11 | 300 | S | S | S | S | S | S | N | S | No | M7 |
| 23 | 28/07/2026 | ING-260728-023 | PENT | L-2607-11 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 28/07/2026 | TRA-260728-024 | NEUM | L-2607-11 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 29/07/2026 | AJU-260729-025 | DTA | L-2607-12 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 30/07/2026 | AJU-260730-026 | HEPB | L-2607-12 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 31/07/2026 | SAL-260731-027 | SPR | L-2607-12 | 50 | S | S | S | S | S | N | S | S | No | M6 |
| 28 | 01/08/2026 | SAL-260801-028 | IPV | L-2607-13 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 02/08/2026 | AJU-260802-029 | IPV | L-2607-13 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 03/08/2026 | ING-260803-030 | INFL | L-2607-13 | 40 | S | N | S | S | S | S | S | N | No | M2+M8 |
| 31 | 03/08/2026 | TRA-260803-031 | VARI | L-2607-14 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 04/08/2026 | ING-260804-032 | SPR | L-2607-14 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 05/08/2026 | ING-260805-033 | VARI | L-2607-14 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 06/08/2026 | SAL-260806-034 | DTA | L-2607-15 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 07/08/2026 | DEV-260807-035 | IPV | L-2607-15 | 180 | S | S | S | S | S | S | N | S | No | M7 |
| 36 | 08/08/2026 | ING-260808-036 | NEUM | L-2607-15 | 60 | S | S | S | S | S | S | S | N | No | M8 |
| 37 | 08/08/2026 | SAL-260808-037 | PENT | L-2607-16 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 09/08/2026 | AJU-260809-038 | IPV | L-2607-16 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 10/08/2026 | SAL-260810-039 | DTA | L-2607-16 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 11/08/2026 | TRA-260811-040 | VARI | L-2607-17 | 30 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 18/07/2026 | BCG | 50 | 50 | 0 | GR-260718-071 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 2 | 02/08/2026 | NEUM | 40 | 40 | 0 | GR-260802-129 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 3 | 03/08/2026 | VARI | 50 | 50 | 0 | GR-260803-180 | Sí | Conforme. Cantidad y guía coinciden. |
| 4 | 07/08/2026 | PENT | 50 | 50 | 0 | GR-260807-217 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 5 | 09/08/2026 | NEUM | 80 | 75 | -5 | GR-260809-096 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 6 | 08/08/2026 | ROTA | 20 | 20 | 0 | GR-260808-217 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 7 | 24/07/2026 | HEPB | 30 | 20 | -10 | GR-260724-138 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 8 | 31/07/2026 | SPR | 80 | 85 | +5 | GR-260731-199 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 9 | 25/07/2026 | SPR | 40 | 40 | 0 | GR-260725-172 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 10 | 31/07/2026 | PENT | 80 | 80 | 0 | GR-260731-150 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 11 | 18/07/2026 | ROTA | 50 | 50 | 0 | GR-260718-005 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 12 | 29/07/2026 | HEPB | 120 | 120 | 0 | GR-260729-071 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 13 | 14/07/2026 | NEUM | 40 | 40 | 0 | GR-260714-202 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 14 | 11/08/2026 | NEUM | 150 | 150 | 0 | GR-260811-132 | Sí | Conforme. Cantidad y guía coinciden. |
| 15 | 30/07/2026 | HEPB | 40 | 60 | +20 | GR-260730-083 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 16 | 17/07/2026 | NEUM | 20 | 20 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 17 | 15/07/2026 | SPR | 80 | 80 | 0 | GR-260715-033 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 18 | 06/08/2026 | ROTA | 180 | 180 | 0 | GR-260806-048 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 19 | 08/08/2026 | DTA | 40 | 40 | 0 | GR-260808-077 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 20 | 24/07/2026 | IPV | 100 | 100 | 0 | GR-260724-134 | Sí | Conforme. Cantidad y guía coinciden. |
| 21 | 03/08/2026 | ROTA | 20 | 20 | 0 | GR-260803-135 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 22 | 28/07/2026 | VARI | 40 | 40 | 0 | GR-260728-108 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 23 | 24/07/2026 | ROTA | 100 | 110 | +10 | GR-260724-073 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 24 | 08/08/2026 | ROTA | 180 | 180 | 0 | GR-260808-079 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 25 | 18/07/2026 | SPR | 80 | 90 | +10 | GR-260718-129 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |

**Observaciones**

- Se verificaron los 40 asientos contra las guías de remisión del archivo de almacén.

---

### 2.6 · TRAB-03 · Postest (Sistema SIVAC) · 13/10/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-03 | Hospital Andahuaylas | 10/09/2026 al 12/10/2026 | Postest | OBS-01 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 39 · **RSD = 97.50 %** · Despachos evaluados: 25 · Concordantes: 24 · **CPE = 96.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 10/09/2026 | ING-260910-001 | NEUM | L-2609-03 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 11/09/2026 | SAL-260911-002 | PENT | L-2609-03 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 12/09/2026 | ING-260912-003 | DTA | L-2609-03 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 13/09/2026 | ING-260913-004 | ROTA | L-2609-04 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 13/09/2026 | SAL-260913-005 | VARI | L-2609-04 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 14/09/2026 | TRA-260914-006 | INFL | L-2609-04 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 15/09/2026 | TRA-260915-007 | INFL | L-2609-05 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 16/09/2026 | SAL-260916-008 | SPR | L-2609-05 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 17/09/2026 | TRA-260917-009 | HEPB | L-2609-05 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 18/09/2026 | TRA-260918-010 | HEPB | L-2609-06 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 18/09/2026 | TRA-260918-011 | DTA | L-2609-06 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 19/09/2026 | SAL-260919-012 | INFL | L-2609-06 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 20/09/2026 | ING-260920-013 | DTA | L-2609-07 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 21/09/2026 | TRA-260921-014 | INFL | L-2609-07 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 22/09/2026 | TRA-260922-015 | NEUM | L-2609-07 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 23/09/2026 | SAL-260923-016 | NEUM | L-2609-08 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 24/09/2026 | TRA-260924-017 | HEPB | L-2609-08 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 24/09/2026 | ING-260924-018 | INFL | L-2609-08 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 25/09/2026 | SAL-260925-019 | PENT | L-2609-09 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 26/09/2026 | SAL-260926-020 | ROTA | L-2609-09 | 300 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 27/09/2026 | ING-260927-021 | DTA | L-2609-09 | 60 | S | S | S | S | S | S | N | N | No | M7+M8 |
| 22 | 28/09/2026 | SAL-260928-022 | VARI | L-2609-10 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 29/09/2026 | ING-260929-023 | PENT | L-2609-10 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 29/09/2026 | DEV-260929-024 | NEUM | L-2609-10 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 30/09/2026 | AJU-260930-025 | HEPB | L-2609-11 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 01/10/2026 | SAL-261001-026 | VARI | L-2609-11 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 02/10/2026 | SAL-261002-027 | BCG | L-2609-11 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 03/10/2026 | SAL-261003-028 | VARI | L-2609-12 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 04/10/2026 | SAL-261004-029 | INFL | L-2609-12 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 05/10/2026 | ING-261005-030 | INFL | L-2609-12 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 05/10/2026 | ING-261005-031 | VARI | L-2609-13 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 06/10/2026 | ING-261006-032 | INFL | L-2609-13 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 07/10/2026 | SAL-261007-033 | PENT | L-2609-13 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 08/10/2026 | TRA-261008-034 | NEUM | L-2609-14 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 09/10/2026 | SAL-261009-035 | BCG | L-2609-14 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 10/10/2026 | SAL-261010-036 | IPV | L-2609-14 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 10/10/2026 | TRA-261010-037 | IPV | L-2609-15 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 11/10/2026 | ING-261011-038 | INFL | L-2609-15 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 12/10/2026 | ING-261012-039 | SPR | L-2609-15 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 13/10/2026 | ING-261013-040 | SPR | L-2609-16 | 60 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 04/10/2026 | NEUM | 60 | 60 | 0 | GR-261004-017 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 2 | 23/09/2026 | VARI | 20 | 20 | 0 | GR-260923-161 | Sí | Conforme. Cantidad y guía coinciden. |
| 3 | 04/10/2026 | PENT | 40 | 40 | 0 | GR-261004-115 | Sí | Conforme. Cantidad y guía coinciden. |
| 4 | 07/10/2026 | HEPB | 80 | 80 | 0 | GR-261007-025 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 5 | 23/09/2026 | PENT | 200 | 200 | 0 | GR-260923-195 | Sí | Conforme. Cantidad y guía coinciden. |
| 6 | 05/10/2026 | VARI | 30 | 30 | 0 | GR-261005-071 | Sí | Conforme. Cantidad y guía coinciden. |
| 7 | 10/10/2026 | BCG | 120 | 120 | 0 | GR-261010-132 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 8 | 02/10/2026 | VARI | 60 | 60 | 0 | GR-261002-099 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 9 | 06/10/2026 | INFL | 180 | 180 | 0 | GR-261006-155 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 10 | 07/10/2026 | PENT | 80 | 80 | 0 | GR-261007-046 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 11 | 11/10/2026 | HEPB | 180 | 170 | -10 | GR-261011-009 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 12 | 23/09/2026 | BCG | 80 | 80 | 0 | GR-260923-001 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 13 | 16/09/2026 | IPV | 180 | 180 | 0 | GR-260916-113 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 14 | 08/10/2026 | PENT | 20 | 20 | 0 | GR-261008-020 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 15 | 18/09/2026 | VARI | 50 | 50 | 0 | GR-260918-057 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 16 | 20/09/2026 | BCG | 120 | 120 | 0 | GR-260920-164 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 17 | 08/10/2026 | PENT | 100 | 100 | 0 | GR-261008-066 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 18 | 08/10/2026 | IPV | 20 | 20 | 0 | GR-261008-204 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 19 | 02/10/2026 | DTA | 120 | 120 | 0 | GR-261002-212 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 20 | 26/09/2026 | SPR | 50 | 50 | 0 | GR-260926-143 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 21 | 17/09/2026 | INFL | 40 | 40 | 0 | GR-260917-075 | Sí | Conforme. Cantidad y guía coinciden. |
| 22 | 17/09/2026 | ROTA | 150 | 150 | 0 | GR-260917-097 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 23 | 25/09/2026 | ROTA | 80 | 80 | 0 | GR-260925-076 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 24 | 30/09/2026 | BCG | 80 | 80 | 0 | GR-260930-214 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 25 | 24/09/2026 | BCG | 20 | 20 | 0 | GR-260924-212 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |

**Observaciones**

- Se exportó el reporte de despachos y se cotejó con las guías físicas.

---

### 2.7 · TRAB-04 · Pretest (proceso manual) · 11/08/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-04 | Hospital ESSALUD Andahuaylas | 15/07/2026 al 10/08/2026 | Pretest | OBS-02 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 29 · **RSD = 72.50 %** · Despachos evaluados: 25 · Concordantes: 19 · **CPE = 76.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 15/07/2026 | ING-260715-001 | SPR | L-2607-12 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 16/07/2026 | AJU-260716-002 | VARI | L-2607-12 | 150 | S | S | S | S | S | N | N | S | No | M6+M7 |
| 3 | 16/07/2026 | TRA-260716-003 | BCG | L-2607-12 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 17/07/2026 | SAL-260717-004 | VARI | L-2607-13 | 30 | S | S | S | N | S | S | S | S | No | M4 |
| 5 | 18/07/2026 | ING-260718-005 | ROTA | L-2607-13 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 18/07/2026 | ING-260718-006 | DTA | L-2607-13 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 19/07/2026 | SAL-260719-007 | ROTA | L-2607-14 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 20/07/2026 | SAL-260720-008 | INFL | L-2607-14 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 21/07/2026 | SAL-260721-009 | HEPB | L-2607-14 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 21/07/2026 | TRA-260721-010 | DTA | L-2607-15 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 22/07/2026 | ING-260722-011 | DTA | L-2607-15 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 23/07/2026 | ING-260723-012 | SPR | L-2607-15 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 23/07/2026 | TRA-260723-013 | PENT | L-2607-16 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 24/07/2026 | SAL-260724-014 | DTA | L-2607-16 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 25/07/2026 | ING-260725-015 | DTA | L-2607-16 | 30 | S | S | S | S | S | N | S | S | No | M6 |
| 16 | 25/07/2026 | SAL-260725-016 | PENT | L-2607-17 | 180 | S | S | S | S | N | S | S | S | No | M5 |
| 17 | 26/07/2026 | ING-260726-017 | NEUM | L-2607-17 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 27/07/2026 | ING-260727-018 | NEUM | L-2607-17 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 27/07/2026 | DEV-260727-019 | BCG | L-2607-18 | 20 | N | S | S | S | S | S | S | S | No | M1 |
| 20 | 28/07/2026 | SAL-260728-020 | HEPB | L-2607-18 | 300 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 29/07/2026 | ING-260729-021 | NEUM | L-2607-18 | 20 | S | S | S | S | S | N | S | S | No | M6 |
| 22 | 30/07/2026 | ING-260730-022 | ROTA | L-2607-19 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 30/07/2026 | SAL-260730-023 | NEUM | L-2607-19 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 31/07/2026 | TRA-260731-024 | VARI | L-2607-19 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 01/08/2026 | TRA-260801-025 | VARI | L-2607-20 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 01/08/2026 | TRA-260801-026 | IPV | L-2607-20 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 02/08/2026 | TRA-260802-027 | NEUM | L-2607-20 | 50 | S | S | N | S | S | N | S | S | No | M3+M6 |
| 28 | 03/08/2026 | SAL-260803-028 | ROTA | L-2607-21 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 03/08/2026 | DEV-260803-029 | IPV | L-2607-21 | 50 | S | N | S | S | S | S | S | S | No | M2 |
| 30 | 04/08/2026 | SAL-260804-030 | HEPB | L-2607-21 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 05/08/2026 | TRA-260805-031 | IPV | L-2607-22 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 05/08/2026 | ING-260805-032 | HEPB | L-2607-22 | 40 | S | S | S | S | S | S | N | S | No | M7 |
| 33 | 06/08/2026 | DEV-260806-033 | BCG | L-2607-22 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 07/08/2026 | DEV-260807-034 | SPR | L-2607-23 | 120 | S | S | N | S | S | S | S | S | No | M3 |
| 35 | 08/08/2026 | SAL-260808-035 | HEPB | L-2607-23 | 20 | S | S | N | S | S | S | S | S | No | M3 |
| 36 | 08/08/2026 | ING-260808-036 | VARI | L-2607-23 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 09/08/2026 | ING-260809-037 | VARI | L-2607-24 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 10/08/2026 | SAL-260810-038 | NEUM | L-2607-24 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 10/08/2026 | SAL-260810-039 | HEPB | L-2607-24 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 11/08/2026 | AJU-260811-040 | INFL | L-2607-25 | 30 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 20/07/2026 | DTA | 80 | 80 | 0 | GR-260720-060 | Sí | Conforme. Cantidad y guía coinciden. |
| 2 | 20/07/2026 | ROTA | 20 | 20 | 0 | GR-260720-001 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 3 | 10/08/2026 | PENT | 60 | 50 | -10 | GR-260810-070 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 4 | 04/08/2026 | INFL | 180 | 175 | -5 | GR-260804-192 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 5 | 31/07/2026 | NEUM | 150 | 150 | 0 | GR-260731-027 | Sí | Conforme. Cantidad y guía coinciden. |
| 6 | 23/07/2026 | HEPB | 180 | 180 | 0 | GR-260723-204 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 7 | 10/08/2026 | DTA | 30 | 30 | 0 | GR-260810-001 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 8 | 09/08/2026 | INFL | 200 | 200 | 0 | GR-260809-211 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 9 | 11/08/2026 | BCG | 30 | 30 | 0 | GR-260811-219 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 10 | 02/08/2026 | HEPB | 150 | 150 | 0 | GR-260802-091 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 11 | 31/07/2026 | DTA | 120 | 120 | 0 | GR-260731-039 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 12 | 11/08/2026 | DTA | 100 | 95 | -5 | GR-260811-218 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 13 | 15/07/2026 | HEPB | 120 | 130 | +10 | GR-260715-177 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 14 | 20/07/2026 | ROTA | 20 | 20 | 0 | GR-260720-135 | Sí | Conforme. Cantidad y guía coinciden. |
| 15 | 24/07/2026 | SPR | 80 | 80 | 0 | GR-260724-103 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 16 | 31/07/2026 | IPV | 20 | 20 | 0 | GR-260731-125 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 17 | 23/07/2026 | VARI | 200 | 200 | 0 | GR-260723-181 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 18 | 17/07/2026 | INFL | 180 | 180 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 19 | 04/08/2026 | IPV | 20 | 20 | 0 | GR-260804-031 | Sí | Conforme. Cantidad y guía coinciden. |
| 20 | 27/07/2026 | PENT | 150 | 150 | 0 | GR-260727-036 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 21 | 11/08/2026 | INFL | 200 | 200 | 0 | GR-260811-137 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 22 | 26/07/2026 | BCG | 120 | 120 | 0 | GR-260726-165 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 23 | 15/07/2026 | PENT | 100 | 100 | 0 | GR-260715-181 | Sí | Conforme. Cantidad y guía coinciden. |
| 24 | 08/08/2026 | BCG | 150 | 150 | 0 | GR-260808-163 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 25 | 17/07/2026 | BCG | 20 | 15 | -5 | GR-260717-203 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |

**Observaciones**

- Auditoría realizada con el kardex físico y el talonario de vales del periodo.

---

### 2.8 · TRAB-04 · Postest (Sistema SIVAC) · 13/10/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-04 | Hospital ESSALUD Andahuaylas | 17/09/2026 al 12/10/2026 | Postest | OBS-02 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 39 · **RSD = 97.50 %** · Despachos evaluados: 25 · Concordantes: 25 · **CPE = 100.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 17/09/2026 | ING-260917-001 | DTA | L-2609-04 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 18/09/2026 | DEV-260918-002 | PENT | L-2609-04 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 18/09/2026 | ING-260918-003 | DTA | L-2609-04 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 19/09/2026 | SAL-260919-004 | NEUM | L-2609-05 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 20/09/2026 | ING-260920-005 | HEPB | L-2609-05 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 20/09/2026 | SAL-260920-006 | SPR | L-2609-05 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 21/09/2026 | SAL-260921-007 | HEPB | L-2609-06 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 22/09/2026 | DEV-260922-008 | BCG | L-2609-06 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 22/09/2026 | ING-260922-009 | INFL | L-2609-06 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 23/09/2026 | TRA-260923-010 | IPV | L-2609-07 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 24/09/2026 | SAL-260924-011 | INFL | L-2609-07 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 24/09/2026 | SAL-260924-012 | IPV | L-2609-07 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 25/09/2026 | AJU-260925-013 | ROTA | L-2609-08 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 26/09/2026 | SAL-260926-014 | INFL | L-2609-08 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 26/09/2026 | AJU-260926-015 | PENT | L-2609-08 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 27/09/2026 | SAL-260927-016 | HEPB | L-2609-09 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 28/09/2026 | ING-260928-017 | SPR | L-2609-09 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 28/09/2026 | ING-260928-018 | SPR | L-2609-09 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 29/09/2026 | AJU-260929-019 | VARI | L-2609-10 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 30/09/2026 | ING-260930-020 | NEUM | L-2609-10 | 40 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 30/09/2026 | SAL-260930-021 | PENT | L-2609-10 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 01/10/2026 | SAL-261001-022 | IPV | L-2609-11 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 02/10/2026 | ING-261002-023 | DTA | L-2609-11 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 02/10/2026 | TRA-261002-024 | ROTA | L-2609-11 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 03/10/2026 | ING-261003-025 | HEPB | L-2609-12 | 150 | S | S | N | S | S | S | S | N | No | M3+M8 |
| 26 | 04/10/2026 | SAL-261004-026 | NEUM | L-2609-12 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 04/10/2026 | TRA-261004-027 | BCG | L-2609-12 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 05/10/2026 | ING-261005-028 | INFL | L-2609-13 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 06/10/2026 | TRA-261006-029 | INFL | L-2609-13 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 06/10/2026 | DEV-261006-030 | ROTA | L-2609-13 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 07/10/2026 | SAL-261007-031 | NEUM | L-2609-14 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 08/10/2026 | ING-261008-032 | HEPB | L-2609-14 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 08/10/2026 | DEV-261008-033 | PENT | L-2609-14 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 09/10/2026 | SAL-261009-034 | HEPB | L-2609-15 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 10/10/2026 | DEV-261010-035 | ROTA | L-2609-15 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 10/10/2026 | TRA-261010-036 | INFL | L-2609-15 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 11/10/2026 | SAL-261011-037 | PENT | L-2609-16 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 12/10/2026 | ING-261012-038 | BCG | L-2609-16 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 12/10/2026 | TRA-261012-039 | PENT | L-2609-16 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 13/10/2026 | TRA-261013-040 | NEUM | L-2609-17 | 180 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 18/09/2026 | BCG | 100 | 100 | 0 | GR-260918-157 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 2 | 05/10/2026 | VARI | 180 | 180 | 0 | GR-261005-071 | Sí | Conforme. Cantidad y guía coinciden. |
| 3 | 17/09/2026 | SPR | 120 | 120 | 0 | GR-260917-017 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 4 | 30/09/2026 | VARI | 180 | 180 | 0 | GR-260930-020 | Sí | Conforme. Cantidad y guía coinciden. |
| 5 | 22/09/2026 | VARI | 180 | 180 | 0 | GR-260922-116 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 6 | 12/10/2026 | VARI | 20 | 20 | 0 | GR-261012-184 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 7 | 09/10/2026 | SPR | 120 | 120 | 0 | GR-261009-173 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 8 | 04/10/2026 | SPR | 80 | 80 | 0 | GR-261004-166 | Sí | Conforme. Cantidad y guía coinciden. |
| 9 | 19/09/2026 | ROTA | 40 | 40 | 0 | GR-260919-089 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 10 | 23/09/2026 | PENT | 200 | 200 | 0 | GR-260923-181 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 11 | 22/09/2026 | ROTA | 40 | 40 | 0 | GR-260922-134 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 12 | 19/09/2026 | SPR | 50 | 50 | 0 | GR-260919-170 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 05/10/2026 | BCG | 50 | 50 | 0 | GR-261005-024 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 14 | 10/10/2026 | PENT | 80 | 80 | 0 | GR-261010-073 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 15 | 13/10/2026 | IPV | 60 | 60 | 0 | GR-261013-145 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 16 | 19/09/2026 | NEUM | 180 | 180 | 0 | GR-260919-023 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 17 | 23/09/2026 | DTA | 120 | 120 | 0 | GR-260923-177 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 18 | 16/09/2026 | INFL | 40 | 40 | 0 | GR-260916-088 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 19 | 18/09/2026 | PENT | 200 | 200 | 0 | GR-260918-010 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 20 | 01/10/2026 | VARI | 30 | 30 | 0 | GR-261001-004 | Sí | Conforme. Cantidad y guía coinciden. |
| 21 | 04/10/2026 | IPV | 20 | 20 | 0 | GR-261004-158 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 22 | 10/10/2026 | HEPB | 100 | 100 | 0 | GR-261010-151 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 23 | 16/09/2026 | NEUM | 150 | 150 | 0 | GR-260916-013 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 24 | 16/09/2026 | NEUM | 200 | 200 | 0 | GR-260916-020 | Sí | Conforme. Cantidad y guía coinciden. |
| 25 | 24/09/2026 | VARI | 120 | 120 | 0 | GR-260924-137 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |

**Observaciones**

- Los asientos se contrastaron con la trazabilidad de movimientos del sistema.

---

### 2.9 · TRAB-05 · Pretest (proceso manual) · 12/08/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-05 | Centro de Salud Andahuaylas | 11/07/2026 al 11/08/2026 | Pretest | OBS-01 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 22 · **RSD = 55.00 %** · Despachos evaluados: 25 · Concordantes: 15 · **CPE = 60.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 11/07/2026 | SAL-260711-001 | INFL | L-2607-07 | 300 | S | S | S | S | S | S | S | N | No | M8 |
| 2 | 12/07/2026 | TRA-260712-002 | SPR | L-2607-07 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 13/07/2026 | ING-260713-003 | ROTA | L-2607-07 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 13/07/2026 | ING-260713-004 | BCG | L-2607-08 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 14/07/2026 | SAL-260714-005 | NEUM | L-2607-08 | 50 | S | S | N | S | N | S | S | S | No | M3+M5 |
| 6 | 15/07/2026 | ING-260715-006 | VARI | L-2607-08 | 20 | S | S | S | S | S | N | N | S | No | M6+M7 |
| 7 | 16/07/2026 | ING-260716-007 | ROTA | L-2607-09 | 240 | S | S | N | S | S | S | S | S | No | M3 |
| 8 | 17/07/2026 | SAL-260717-008 | PENT | L-2607-09 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 18/07/2026 | TRA-260718-009 | NEUM | L-2607-09 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 18/07/2026 | SAL-260718-010 | SPR | L-2607-10 | 20 | S | S | S | N | S | S | N | S | No | M4+M7 |
| 11 | 19/07/2026 | ING-260719-011 | IPV | L-2607-10 | 180 | S | S | S | S | S | S | N | S | No | M7 |
| 12 | 20/07/2026 | DEV-260720-012 | DTA | L-2607-10 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 21/07/2026 | TRA-260721-013 | SPR | L-2607-11 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 22/07/2026 | DEV-260722-014 | NEUM | L-2607-11 | 80 | S | N | S | S | S | S | N | S | No | M2+M7 |
| 15 | 22/07/2026 | ING-260722-015 | DTA | L-2607-11 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 23/07/2026 | TRA-260723-016 | NEUM | L-2607-12 | 200 | S | S | S | S | S | S | N | S | No | M7 |
| 17 | 24/07/2026 | TRA-260724-017 | HEPB | L-2607-12 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 25/07/2026 | ING-260725-018 | DTA | L-2607-12 | 40 | S | S | S | S | S | S | N | S | No | M7 |
| 19 | 26/07/2026 | TRA-260726-019 | SPR | L-2607-13 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 27/07/2026 | ING-260727-020 | SPR | L-2607-13 | 150 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 27/07/2026 | TRA-260727-021 | NEUM | L-2607-13 | 240 | S | S | S | S | S | N | S | S | No | M6 |
| 22 | 28/07/2026 | ING-260728-022 | HEPB | L-2607-14 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 29/07/2026 | ING-260729-023 | VARI | L-2607-14 | 80 | S | N | S | S | S | S | S | S | No | M2 |
| 24 | 30/07/2026 | SAL-260730-024 | HEPB | L-2607-14 | 120 | S | S | S | S | S | S | S | N | No | M8 |
| 25 | 31/07/2026 | TRA-260731-025 | SPR | L-2607-15 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 01/08/2026 | SAL-260801-026 | HEPB | L-2607-15 | 240 | S | S | S | S | S | S | N | S | No | M7 |
| 27 | 01/08/2026 | SAL-260801-027 | DTA | L-2607-15 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 02/08/2026 | SAL-260802-028 | HEPB | L-2607-16 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 03/08/2026 | ING-260803-029 | IPV | L-2607-16 | 240 | S | N | S | S | S | S | S | S | No | M2 |
| 30 | 04/08/2026 | DEV-260804-030 | NEUM | L-2607-16 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 05/08/2026 | SAL-260805-031 | HEPB | L-2607-17 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 05/08/2026 | SAL-260805-032 | PENT | L-2607-17 | 240 | S | S | S | S | N | S | S | S | No | M5 |
| 33 | 06/08/2026 | SAL-260806-033 | BCG | L-2607-17 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 07/08/2026 | TRA-260807-034 | ROTA | L-2607-18 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 08/08/2026 | SAL-260808-035 | NEUM | L-2607-18 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 09/08/2026 | ING-260809-036 | BCG | L-2607-18 | 40 | S | S | S | S | N | S | S | S | No | M5 |
| 37 | 10/08/2026 | SAL-260810-037 | BCG | L-2607-19 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 10/08/2026 | ING-260810-038 | SPR | L-2607-19 | 20 | S | S | S | S | S | N | S | S | No | M6 |
| 39 | 11/08/2026 | ING-260811-039 | DTA | L-2607-19 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 12/08/2026 | SAL-260812-040 | INFL | L-2607-20 | 40 | S | N | S | S | S | S | S | S | No | M2 |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 04/08/2026 | DTA | 120 | 120 | 0 | GR-260804-139 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 2 | 20/07/2026 | IPV | 40 | 40 | 0 | GR-260720-025 | Sí | Conforme. Cantidad y guía coinciden. |
| 3 | 30/07/2026 | PENT | 80 | 80 | 0 | GR-260730-102 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 4 | 02/08/2026 | ROTA | 50 | 45 | -5 | GR-260802-159 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 5 | 20/07/2026 | PENT | 60 | 50 | -10 | GR-260720-212 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 6 | 29/07/2026 | INFL | 100 | 100 | 0 | GR-260729-021 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 7 | 03/08/2026 | NEUM | 30 | 20 | -10 | GR-260803-080 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 8 | 06/08/2026 | NEUM | 60 | 55 | -5 | GR-260806-136 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 9 | 07/08/2026 | PENT | 120 | 120 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 10 | 20/07/2026 | ROTA | 60 | 60 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 11 | 06/08/2026 | DTA | 150 | 150 | 0 | GR-260806-217 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 12 | 05/08/2026 | VARI | 200 | 200 | 0 | GR-260805-041 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 13 | 19/07/2026 | ROTA | 200 | 200 | 0 | GR-260719-030 | Sí | Conforme. Cantidad y guía coinciden. |
| 14 | 01/08/2026 | HEPB | 60 | 60 | 0 | GR-260801-186 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 15 | 11/08/2026 | NEUM | 40 | 50 | +10 | GR-260811-181 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 16 | 29/07/2026 | INFL | 20 | 40 | +20 | GR-260729-196 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 17 | 27/07/2026 | BCG | 30 | 30 | 0 | GR-260727-025 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 18 | 29/07/2026 | SPR | 60 | 60 | 0 | GR-260729-212 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 19 | 31/07/2026 | ROTA | 50 | 45 | -5 | GR-260731-062 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 20 | 31/07/2026 | INFL | 60 | 60 | 0 | GR-260731-183 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 21 | 24/07/2026 | SPR | 20 | 20 | 0 | GR-260724-154 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 22 | 21/07/2026 | HEPB | 40 | 40 | 0 | GR-260721-033 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 23 | 02/08/2026 | DTA | 180 | 180 | 0 | GR-260802-120 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 24 | 12/08/2026 | HEPB | 20 | 20 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 25 | 19/07/2026 | VARI | 50 | 50 | 0 | GR-260719-142 | Sí | Conforme. Verificado el FEFO al momento de la carga. |

**Observaciones**

- El operador sustentó verbalmente los asientos observados; no se corrigió la hoja.

---

### 2.10 · TRAB-05 · Postest (Sistema SIVAC) · 14/10/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-05 | Centro de Salud Andahuaylas | 18/09/2026 al 13/10/2026 | Postest | OBS-01 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 37 · **RSD = 92.50 %** · Despachos evaluados: 25 · Concordantes: 23 · **CPE = 92.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 18/09/2026 | ING-260918-001 | DTA | L-2609-09 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 19/09/2026 | DEV-260919-002 | BCG | L-2609-09 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 19/09/2026 | DEV-260919-003 | ROTA | L-2609-09 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 20/09/2026 | TRA-260920-004 | INFL | L-2609-10 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 21/09/2026 | SAL-260921-005 | HEPB | L-2609-10 | 30 | S | S | S | S | S | S | S | N | No | M8 |
| 6 | 21/09/2026 | ING-260921-006 | BCG | L-2609-10 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 22/09/2026 | ING-260922-007 | VARI | L-2609-11 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 23/09/2026 | ING-260923-008 | PENT | L-2609-11 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 23/09/2026 | ING-260923-009 | INFL | L-2609-11 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 24/09/2026 | TRA-260924-010 | IPV | L-2609-12 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 25/09/2026 | AJU-260925-011 | INFL | L-2609-12 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 25/09/2026 | SAL-260925-012 | ROTA | L-2609-12 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 26/09/2026 | ING-260926-013 | SPR | L-2609-13 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 27/09/2026 | TRA-260927-014 | BCG | L-2609-13 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 27/09/2026 | AJU-260927-015 | HEPB | L-2609-13 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 28/09/2026 | ING-260928-016 | ROTA | L-2609-14 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 29/09/2026 | TRA-260929-017 | DTA | L-2609-14 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 29/09/2026 | SAL-260929-018 | SPR | L-2609-14 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 30/09/2026 | SAL-260930-019 | VARI | L-2609-15 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 01/10/2026 | SAL-261001-020 | SPR | L-2609-15 | 60 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 01/10/2026 | ING-261001-021 | IPV | L-2609-15 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 02/10/2026 | DEV-261002-022 | BCG | L-2609-16 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 03/10/2026 | SAL-261003-023 | INFL | L-2609-16 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 03/10/2026 | SAL-261003-024 | ROTA | L-2609-16 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 04/10/2026 | SAL-261004-025 | NEUM | L-2609-17 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 05/10/2026 | SAL-261005-026 | SPR | L-2609-17 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 05/10/2026 | SAL-261005-027 | DTA | L-2609-17 | 300 | S | N | S | S | S | S | S | N | No | M2+M8 |
| 28 | 06/10/2026 | AJU-261006-028 | DTA | L-2609-18 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 07/10/2026 | SAL-261007-029 | INFL | L-2609-18 | 240 | S | S | S | S | N | S | S | S | No | M5 |
| 30 | 07/10/2026 | ING-261007-030 | SPR | L-2609-18 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 08/10/2026 | TRA-261008-031 | PENT | L-2609-19 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 09/10/2026 | DEV-261009-032 | PENT | L-2609-19 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 09/10/2026 | TRA-261009-033 | IPV | L-2609-19 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 10/10/2026 | ING-261010-034 | BCG | L-2609-20 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 11/10/2026 | SAL-261011-035 | ROTA | L-2609-20 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 11/10/2026 | ING-261011-036 | VARI | L-2609-20 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 12/10/2026 | SAL-261012-037 | IPV | L-2609-21 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 13/10/2026 | ING-261013-038 | PENT | L-2609-21 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 13/10/2026 | TRA-261013-039 | IPV | L-2609-21 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 14/10/2026 | ING-261014-040 | HEPB | L-2609-22 | 60 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 26/09/2026 | SPR | 180 | 180 | 0 | GR-260926-035 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 2 | 18/09/2026 | INFL | 80 | 80 | 0 | GR-260918-143 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 3 | 12/10/2026 | HEPB | 50 | 50 | 0 | GR-261012-119 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 4 | 13/10/2026 | SPR | 180 | 185 | +5 | GR-261013-004 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 5 | 27/09/2026 | VARI | 50 | 50 | 0 | GR-260927-066 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 6 | 26/09/2026 | SPR | 20 | 20 | 0 | GR-260926-079 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 7 | 24/09/2026 | INFL | 30 | 30 | 0 | GR-260924-218 | Sí | Conforme. Cantidad y guía coinciden. |
| 8 | 28/09/2026 | DTA | 120 | 120 | 0 | GR-260928-171 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 9 | 08/10/2026 | IPV | 100 | 100 | 0 | GR-261008-108 | Sí | Conforme. Cantidad y guía coinciden. |
| 10 | 21/09/2026 | DTA | 120 | 120 | 0 | GR-260921-137 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 11 | 19/09/2026 | SPR | 40 | 40 | 0 | GR-260919-167 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 12 | 19/09/2026 | SPR | 120 | 120 | 0 | GR-260919-037 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 10/10/2026 | HEPB | 150 | 150 | 0 | GR-261010-217 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 14 | 08/10/2026 | IPV | 200 | 200 | 0 | GR-261008-040 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 15 | 29/09/2026 | DTA | 80 | 80 | 0 | GR-260929-020 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 16 | 26/09/2026 | BCG | 80 | 80 | 0 | GR-260926-021 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 17 | 02/10/2026 | NEUM | 50 | 50 | 0 | GR-261002-117 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 18 | 05/10/2026 | SPR | 100 | 100 | 0 | GR-261005-125 | Sí | Conforme. Cantidad y guía coinciden. |
| 19 | 01/10/2026 | NEUM | 180 | 180 | 0 | GR-261001-091 | Sí | Conforme. Cantidad y guía coinciden. |
| 20 | 28/09/2026 | PENT | 80 | 80 | 0 | GR-260928-031 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 21 | 04/10/2026 | IPV | 40 | 40 | 0 | GR-261004-032 | Sí | Conforme. Cantidad y guía coinciden. |
| 22 | 27/09/2026 | NEUM | 20 | 20 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 23 | 09/10/2026 | DTA | 120 | 120 | 0 | GR-261009-118 | Sí | Conforme. Cantidad y guía coinciden. |
| 24 | 17/09/2026 | NEUM | 20 | 20 | 0 | GR-260917-034 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 25 | 20/09/2026 | INFL | 180 | 180 | 0 | GR-260920-146 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |

**Observaciones**

- Se exportó el reporte de despachos y se cotejó con las guías físicas.

---

### 2.11 · TRAB-06 · Pretest (proceso manual) · 12/08/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-06 | Talavera | 16/07/2026 al 11/08/2026 | Pretest | OBS-02 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 26 · **RSD = 65.00 %** · Despachos evaluados: 25 · Concordantes: 17 · **CPE = 68.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 16/07/2026 | SAL-260716-001 | DTA | L-2607-11 | 30 | N | S | S | S | S | S | S | S | No | M1 |
| 2 | 17/07/2026 | AJU-260717-002 | DTA | L-2607-11 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 17/07/2026 | SAL-260717-003 | VARI | L-2607-11 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 18/07/2026 | ING-260718-004 | NEUM | L-2607-12 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 19/07/2026 | SAL-260719-005 | PENT | L-2607-12 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 19/07/2026 | ING-260719-006 | SPR | L-2607-12 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 20/07/2026 | SAL-260720-007 | NEUM | L-2607-13 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 21/07/2026 | SAL-260721-008 | VARI | L-2607-13 | 240 | S | N | S | S | S | S | S | S | No | M2 |
| 9 | 22/07/2026 | ING-260722-009 | PENT | L-2607-13 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 22/07/2026 | AJU-260722-010 | SPR | L-2607-14 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 23/07/2026 | DEV-260723-011 | ROTA | L-2607-14 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 24/07/2026 | ING-260724-012 | BCG | L-2607-14 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 24/07/2026 | SAL-260724-013 | PENT | L-2607-15 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 25/07/2026 | TRA-260725-014 | PENT | L-2607-15 | 40 | S | S | S | S | S | S | N | S | No | M7 |
| 15 | 26/07/2026 | TRA-260726-015 | PENT | L-2607-15 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 26/07/2026 | ING-260726-016 | PENT | L-2607-16 | 50 | S | S | S | S | N | N | S | S | No | M5+M6 |
| 17 | 27/07/2026 | TRA-260727-017 | ROTA | L-2607-16 | 20 | S | S | S | N | S | S | S | S | No | M4 |
| 18 | 28/07/2026 | ING-260728-018 | PENT | L-2607-16 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 28/07/2026 | ING-260728-019 | NEUM | L-2607-17 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 29/07/2026 | SAL-260729-020 | INFL | L-2607-17 | 240 | S | S | S | S | S | S | N | S | No | M7 |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 30/07/2026 | TRA-260730-021 | INFL | L-2607-17 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 31/07/2026 | ING-260731-022 | DTA | L-2607-18 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 31/07/2026 | ING-260731-023 | DTA | L-2607-18 | 300 | N | S | S | S | S | S | S | S | No | M1 |
| 24 | 01/08/2026 | AJU-260801-024 | IPV | L-2607-18 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 02/08/2026 | TRA-260802-025 | ROTA | L-2607-19 | 20 | S | S | S | S | S | N | S | S | No | M6 |
| 26 | 02/08/2026 | SAL-260802-026 | INFL | L-2607-19 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 03/08/2026 | ING-260803-027 | SPR | L-2607-19 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 04/08/2026 | DEV-260804-028 | PENT | L-2607-20 | 120 | S | N | S | S | S | S | N | S | No | M2+M7 |
| 29 | 04/08/2026 | TRA-260804-029 | PENT | L-2607-20 | 120 | S | S | S | S | S | S | N | S | No | M7 |
| 30 | 05/08/2026 | ING-260805-030 | IPV | L-2607-20 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 06/08/2026 | SAL-260806-031 | SPR | L-2607-21 | 30 | N | S | S | S | S | S | N | S | No | M1+M7 |
| 32 | 06/08/2026 | SAL-260806-032 | DTA | L-2607-21 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 07/08/2026 | ING-260807-033 | IPV | L-2607-21 | 50 | S | S | N | S | S | S | S | S | No | M3 |
| 34 | 08/08/2026 | SAL-260808-034 | IPV | L-2607-22 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 09/08/2026 | ING-260809-035 | SPR | L-2607-22 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 09/08/2026 | ING-260809-036 | NEUM | L-2607-22 | 100 | S | S | N | S | S | S | S | S | No | M3 |
| 37 | 10/08/2026 | SAL-260810-037 | IPV | L-2607-23 | 60 | S | S | S | S | S | N | S | S | No | M6 |
| 38 | 11/08/2026 | ING-260811-038 | BCG | L-2607-23 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 11/08/2026 | ING-260811-039 | DTA | L-2607-23 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 12/08/2026 | DEV-260812-040 | PENT | L-2607-24 | 150 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 02/08/2026 | BCG | 180 | 180 | 0 | GR-260802-144 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 2 | 22/07/2026 | SPR | 40 | 40 | 0 | GR-260722-062 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 3 | 03/08/2026 | HEPB | 80 | 70 | -10 | GR-260803-087 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 4 | 21/07/2026 | DTA | 30 | 30 | 0 | GR-260721-076 | Sí | Conforme. Cantidad y guía coinciden. |
| 5 | 03/08/2026 | DTA | 80 | 80 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 6 | 22/07/2026 | HEPB | 150 | 150 | 0 | GR-260722-010 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 7 | 07/08/2026 | INFL | 30 | 30 | 0 | GR-260807-005 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 8 | 15/07/2026 | INFL | 80 | 80 | 0 | GR-260715-147 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 9 | 10/08/2026 | PENT | 120 | 115 | -5 | GR-260810-129 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 10 | 27/07/2026 | IPV | 150 | 150 | 0 | GR-260727-159 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 11 | 27/07/2026 | INFL | 20 | 20 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 12 | 29/07/2026 | HEPB | 30 | 30 | 0 | GR-260729-215 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 18/07/2026 | ROTA | 100 | 100 | 0 | GR-260718-092 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 14 | 31/07/2026 | IPV | 180 | 180 | 0 | GR-260731-016 | Sí | Conforme. Cantidad y guía coinciden. |
| 15 | 30/07/2026 | IPV | 20 | 20 | 0 | GR-260730-213 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 16 | 12/08/2026 | BCG | 30 | 30 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 17 | 10/08/2026 | SPR | 20 | 40 | +20 | GR-260810-066 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 18 | 19/07/2026 | SPR | 80 | 80 | 0 | GR-260719-045 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 19 | 08/08/2026 | INFL | 200 | 195 | -5 | GR-260808-006 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 20 | 12/08/2026 | BCG | 80 | 80 | 0 | GR-260812-096 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 21 | 17/07/2026 | DTA | 100 | 100 | 0 | GR-260717-072 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 22 | 06/08/2026 | HEPB | 200 | 200 | 0 | GR-260806-006 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 23 | 03/08/2026 | INFL | 40 | 40 | 0 | GR-260803-002 | Sí | Conforme. Cantidad y guía coinciden. |
| 24 | 01/08/2026 | HEPB | 60 | 60 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 25 | 06/08/2026 | ROTA | 100 | 100 | 0 | GR-260806-113 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |

**Observaciones**

- El operador sustentó verbalmente los asientos observados; no se corrigió la hoja.

---

### 2.12 · TRAB-06 · Postest (Sistema SIVAC) · 14/10/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-06 | Talavera | 13/09/2026 al 13/10/2026 | Postest | OBS-02 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 39 · **RSD = 97.50 %** · Despachos evaluados: 25 · Concordantes: 24 · **CPE = 96.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 13/09/2026 | SAL-260913-001 | VARI | L-2609-05 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 14/09/2026 | DEV-260914-002 | VARI | L-2609-05 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 15/09/2026 | AJU-260915-003 | ROTA | L-2609-05 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 15/09/2026 | TRA-260915-004 | HEPB | L-2609-06 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 16/09/2026 | ING-260916-005 | VARI | L-2609-06 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 17/09/2026 | ING-260917-006 | NEUM | L-2609-06 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 18/09/2026 | ING-260918-007 | INFL | L-2609-07 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 19/09/2026 | ING-260919-008 | IPV | L-2609-07 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 19/09/2026 | ING-260919-009 | IPV | L-2609-07 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 20/09/2026 | TRA-260920-010 | PENT | L-2609-08 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 21/09/2026 | DEV-260921-011 | SPR | L-2609-08 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 22/09/2026 | TRA-260922-012 | BCG | L-2609-08 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 23/09/2026 | TRA-260923-013 | DTA | L-2609-09 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 23/09/2026 | ING-260923-014 | SPR | L-2609-09 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 24/09/2026 | DEV-260924-015 | INFL | L-2609-09 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 25/09/2026 | TRA-260925-016 | ROTA | L-2609-10 | 100 | S | N | S | S | N | S | S | S | No | M2+M5 |
| 17 | 26/09/2026 | SAL-260926-017 | NEUM | L-2609-10 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 27/09/2026 | ING-260927-018 | INFL | L-2609-10 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 27/09/2026 | ING-260927-019 | VARI | L-2609-11 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 28/09/2026 | SAL-260928-020 | IPV | L-2609-11 | 50 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 29/09/2026 | SAL-260929-021 | PENT | L-2609-11 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 30/09/2026 | AJU-260930-022 | NEUM | L-2609-12 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 30/09/2026 | DEV-260930-023 | DTA | L-2609-12 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 01/10/2026 | SAL-261001-024 | ROTA | L-2609-12 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 02/10/2026 | DEV-261002-025 | IPV | L-2609-13 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 03/10/2026 | SAL-261003-026 | DTA | L-2609-13 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 04/10/2026 | DEV-261004-027 | HEPB | L-2609-13 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 04/10/2026 | SAL-261004-028 | IPV | L-2609-14 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 05/10/2026 | SAL-261005-029 | BCG | L-2609-14 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 06/10/2026 | ING-261006-030 | PENT | L-2609-14 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 07/10/2026 | SAL-261007-031 | VARI | L-2609-15 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 08/10/2026 | SAL-261008-032 | PENT | L-2609-15 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 08/10/2026 | SAL-261008-033 | VARI | L-2609-15 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 09/10/2026 | ING-261009-034 | INFL | L-2609-16 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 10/10/2026 | TRA-261010-035 | IPV | L-2609-16 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 11/10/2026 | ING-261011-036 | BCG | L-2609-16 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 12/10/2026 | TRA-261012-037 | NEUM | L-2609-17 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 12/10/2026 | SAL-261012-038 | INFL | L-2609-17 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 13/10/2026 | TRA-261013-039 | HEPB | L-2609-17 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 14/10/2026 | SAL-261014-040 | HEPB | L-2609-18 | 80 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 14/10/2026 | VARI | 20 | 20 | 0 | GR-261014-060 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 2 | 22/09/2026 | INFL | 40 | 40 | 0 | GR-260922-131 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 3 | 27/09/2026 | DTA | 100 | 100 | 0 | GR-260927-177 | Sí | Conforme. Cantidad y guía coinciden. |
| 4 | 26/09/2026 | ROTA | 180 | 180 | 0 | GR-260926-103 | Sí | Conforme. Cantidad y guía coinciden. |
| 5 | 04/10/2026 | PENT | 150 | 150 | 0 | GR-261004-197 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 6 | 19/09/2026 | HEPB | 120 | 120 | 0 | GR-260919-110 | Sí | Conforme. Cantidad y guía coinciden. |
| 7 | 06/10/2026 | ROTA | 50 | 50 | 0 | GR-261006-131 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 8 | 24/09/2026 | HEPB | 50 | 50 | 0 | GR-260924-036 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 9 | 27/09/2026 | PENT | 80 | 80 | 0 | GR-260927-155 | Sí | Conforme. Cantidad y guía coinciden. |
| 10 | 30/09/2026 | INFL | 200 | 200 | 0 | GR-260930-113 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 11 | 14/10/2026 | INFL | 150 | 150 | 0 | GR-261014-010 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 12 | 23/09/2026 | DTA | 60 | 60 | 0 | GR-260923-213 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 27/09/2026 | VARI | 200 | 200 | 0 | GR-260927-175 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 14 | 12/10/2026 | HEPB | 80 | 80 | 0 | GR-261012-135 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 15 | 19/09/2026 | BCG | 40 | 40 | 0 | GR-260919-069 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 16 | 19/09/2026 | IPV | 150 | 150 | 0 | GR-260919-030 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 17 | 21/09/2026 | ROTA | 100 | 100 | 0 | GR-260921-089 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 18 | 07/10/2026 | DTA | 20 | 20 | 0 | GR-261007-209 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 19 | 08/10/2026 | NEUM | 30 | 30 | 0 | GR-261008-153 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 20 | 05/10/2026 | INFL | 60 | 60 | 0 | GR-261005-045 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 21 | 01/10/2026 | NEUM | 50 | 50 | 0 | GR-261001-140 | Sí | Conforme. Cantidad y guía coinciden. |
| 22 | 12/10/2026 | PENT | 20 | 20 | 0 | GR-261012-082 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 23 | 05/10/2026 | NEUM | 80 | 70 | -10 | GR-261005-132 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 24 | 04/10/2026 | NEUM | 180 | 180 | 0 | GR-261004-111 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 25 | 05/10/2026 | IPV | 50 | 50 | 0 | GR-261005-128 | Sí | Conforme. Verificado el FEFO al momento de la carga. |

**Observaciones**

- Se exportó el reporte de despachos y se cotejó con las guías físicas.

---

### 2.13 · TRAB-07 · Pretest (proceso manual) · 13/08/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-07 | San Jeronimo | 11/07/2026 al 12/08/2026 | Pretest | OBS-01 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 21 · **RSD = 52.50 %** · Despachos evaluados: 25 · Concordantes: 14 · **CPE = 56.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 11/07/2026 | ING-260711-001 | SPR | L-2607-10 | 50 | S | S | S | N | S | N | S | S | No | M4+M6 |
| 2 | 12/07/2026 | ING-260712-002 | VARI | L-2607-10 | 100 | S | S | S | S | S | S | N | S | No | M7 |
| 3 | 13/07/2026 | SAL-260713-003 | IPV | L-2607-10 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 14/07/2026 | ING-260714-004 | VARI | L-2607-11 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 14/07/2026 | SAL-260714-005 | ROTA | L-2607-11 | 200 | S | S | S | S | S | S | S | N | No | M8 |
| 6 | 15/07/2026 | SAL-260715-006 | SPR | L-2607-11 | 50 | S | S | S | N | S | S | S | S | No | M4 |
| 7 | 16/07/2026 | TRA-260716-007 | HEPB | L-2607-12 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 17/07/2026 | AJU-260717-008 | INFL | L-2607-12 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 18/07/2026 | SAL-260718-009 | IPV | L-2607-12 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 19/07/2026 | SAL-260719-010 | SPR | L-2607-13 | 200 | S | S | S | N | S | S | S | S | No | M4 |
| 11 | 19/07/2026 | AJU-260719-011 | INFL | L-2607-13 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 20/07/2026 | SAL-260720-012 | VARI | L-2607-13 | 80 | S | S | N | S | S | S | S | S | No | M3 |
| 13 | 21/07/2026 | TRA-260721-013 | INFL | L-2607-14 | 200 | S | S | S | S | S | N | S | S | No | M6 |
| 14 | 22/07/2026 | SAL-260722-014 | IPV | L-2607-14 | 80 | S | S | S | S | S | S | N | N | No | M7+M8 |
| 15 | 23/07/2026 | AJU-260723-015 | VARI | L-2607-14 | 300 | N | S | S | S | S | S | S | N | No | M1+M8 |
| 16 | 24/07/2026 | ING-260724-016 | HEPB | L-2607-15 | 180 | S | S | S | S | S | S | N | S | No | M7 |
| 17 | 25/07/2026 | ING-260725-017 | ROTA | L-2607-15 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 25/07/2026 | TRA-260725-018 | PENT | L-2607-15 | 100 | S | S | S | S | S | S | N | N | No | M7+M8 |
| 19 | 26/07/2026 | ING-260726-019 | ROTA | L-2607-16 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 27/07/2026 | ING-260727-020 | PENT | L-2607-16 | 300 | S | S | S | S | S | S | N | S | No | M7 |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 28/07/2026 | ING-260728-021 | INFL | L-2607-16 | 150 | S | S | S | S | S | S | N | S | No | M7 |
| 22 | 29/07/2026 | AJU-260729-022 | INFL | L-2607-17 | 80 | S | S | S | S | S | N | S | S | No | M6 |
| 23 | 30/07/2026 | AJU-260730-023 | DTA | L-2607-17 | 100 | S | N | S | S | S | S | S | S | No | M2 |
| 24 | 30/07/2026 | SAL-260730-024 | INFL | L-2607-17 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 31/07/2026 | SAL-260731-025 | NEUM | L-2607-18 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 01/08/2026 | DEV-260801-026 | NEUM | L-2607-18 | 200 | S | S | N | S | S | S | S | S | No | M3 |
| 27 | 02/08/2026 | ING-260802-027 | HEPB | L-2607-18 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 03/08/2026 | AJU-260803-028 | NEUM | L-2607-19 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 04/08/2026 | SAL-260804-029 | BCG | L-2607-19 | 200 | S | S | S | S | S | N | S | S | No | M6 |
| 30 | 05/08/2026 | ING-260805-030 | VARI | L-2607-19 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 05/08/2026 | AJU-260805-031 | BCG | L-2607-20 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 06/08/2026 | DEV-260806-032 | HEPB | L-2607-20 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 07/08/2026 | ING-260807-033 | ROTA | L-2607-20 | 240 | S | S | S | S | S | S | N | S | No | M7 |
| 34 | 08/08/2026 | SAL-260808-034 | DTA | L-2607-21 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 09/08/2026 | DEV-260809-035 | ROTA | L-2607-21 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 10/08/2026 | SAL-260810-036 | INFL | L-2607-21 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 10/08/2026 | TRA-260810-037 | BCG | L-2607-22 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 11/08/2026 | SAL-260811-038 | VARI | L-2607-22 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 12/08/2026 | ING-260812-039 | PENT | L-2607-22 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 13/08/2026 | TRA-260813-040 | SPR | L-2607-23 | 180 | N | S | S | S | S | S | S | S | No | M1 |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 22/07/2026 | ROTA | 30 | 30 | 0 | GR-260722-107 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 2 | 18/07/2026 | PENT | 150 | 150 | 0 | GR-260718-202 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 3 | 09/08/2026 | DTA | 100 | 120 | +20 | GR-260809-080 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 4 | 09/08/2026 | DTA | 60 | 60 | 0 | GR-260809-002 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 5 | 12/08/2026 | NEUM | 200 | 200 | 0 | GR-260812-100 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 6 | 19/07/2026 | INFL | 50 | 50 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 7 | 23/07/2026 | VARI | 200 | 200 | 0 | GR-260723-036 | Sí | Conforme. Cantidad y guía coinciden. |
| 8 | 24/07/2026 | DTA | 30 | 30 | 0 | GR-260724-071 | Sí | Conforme. Cantidad y guía coinciden. |
| 9 | 22/07/2026 | VARI | 200 | 200 | 0 | GR-260722-159 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 10 | 19/07/2026 | HEPB | 100 | 100 | 0 | GR-260719-012 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 11 | 13/08/2026 | DTA | 80 | 70 | -10 | GR-260813-129 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 12 | 03/08/2026 | VARI | 40 | 40 | 0 | GR-260803-082 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 13 | 17/07/2026 | INFL | 120 | 115 | -5 | GR-260717-214 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 14 | 30/07/2026 | NEUM | 180 | 180 | 0 | GR-260730-112 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 15 | 29/07/2026 | INFL | 60 | 50 | -10 | GR-260729-095 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 16 | 01/08/2026 | SPR | 40 | 30 | -10 | GR-260801-013 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 17 | 20/07/2026 | BCG | 150 | 150 | 0 | GR-260720-100 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 18 | 28/07/2026 | BCG | 100 | 90 | -10 | GR-260728-038 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 19 | 28/07/2026 | NEUM | 180 | 180 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 20 | 02/08/2026 | INFL | 40 | 40 | 0 | GR-260802-219 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 21 | 05/08/2026 | SPR | 40 | 40 | 0 | GR-260805-106 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 22 | 12/08/2026 | NEUM | 180 | 175 | -5 | GR-260812-181 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 23 | 26/07/2026 | HEPB | 40 | 30 | -10 | GR-260726-103 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 24 | 16/07/2026 | PENT | 150 | 150 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 25 | 13/08/2026 | DTA | 100 | 100 | 0 | GR-260813-084 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |

**Observaciones**

- Se verificaron los 40 asientos contra las guías de remisión del archivo de almacén.

---

### 2.14 · TRAB-07 · Postest (Sistema SIVAC) · 15/10/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-07 | San Jeronimo | 20/09/2026 al 14/10/2026 | Postest | OBS-01 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 37 · **RSD = 92.50 %** · Despachos evaluados: 25 · Concordantes: 23 · **CPE = 92.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 20/09/2026 | ING-260920-001 | HEPB | L-2609-03 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 21/09/2026 | AJU-260921-002 | SPR | L-2609-03 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 21/09/2026 | SAL-260921-003 | PENT | L-2609-03 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 22/09/2026 | TRA-260922-004 | DTA | L-2609-04 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 23/09/2026 | SAL-260923-005 | VARI | L-2609-04 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 23/09/2026 | ING-260923-006 | BCG | L-2609-04 | 180 | S | S | S | S | S | S | S | N | No | M8 |
| 7 | 24/09/2026 | TRA-260924-007 | HEPB | L-2609-05 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 24/09/2026 | SAL-260924-008 | IPV | L-2609-05 | 150 | S | S | S | S | S | S | S | N | No | M8 |
| 9 | 25/09/2026 | SAL-260925-009 | PENT | L-2609-05 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 26/09/2026 | ING-260926-010 | DTA | L-2609-06 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 26/09/2026 | TRA-260926-011 | DTA | L-2609-06 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 27/09/2026 | SAL-260927-012 | HEPB | L-2609-06 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 28/09/2026 | SAL-260928-013 | ROTA | L-2609-07 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 28/09/2026 | SAL-260928-014 | PENT | L-2609-07 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 29/09/2026 | SAL-260929-015 | HEPB | L-2609-07 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 30/09/2026 | SAL-260930-016 | HEPB | L-2609-08 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 30/09/2026 | SAL-260930-017 | VARI | L-2609-08 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 01/10/2026 | TRA-261001-018 | INFL | L-2609-08 | 20 | S | N | S | S | N | S | S | S | No | M2+M5 |
| 19 | 02/10/2026 | SAL-261002-019 | BCG | L-2609-09 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 02/10/2026 | DEV-261002-020 | HEPB | L-2609-09 | 20 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 03/10/2026 | DEV-261003-021 | NEUM | L-2609-09 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 03/10/2026 | SAL-261003-022 | DTA | L-2609-10 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 04/10/2026 | SAL-261004-023 | IPV | L-2609-10 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 05/10/2026 | DEV-261005-024 | VARI | L-2609-10 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 05/10/2026 | TRA-261005-025 | INFL | L-2609-11 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 06/10/2026 | TRA-261006-026 | DTA | L-2609-11 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 07/10/2026 | SAL-261007-027 | VARI | L-2609-11 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 07/10/2026 | DEV-261007-028 | NEUM | L-2609-12 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 08/10/2026 | SAL-261008-029 | ROTA | L-2609-12 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 09/10/2026 | TRA-261009-030 | INFL | L-2609-12 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 09/10/2026 | ING-261009-031 | HEPB | L-2609-13 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 10/10/2026 | TRA-261010-032 | SPR | L-2609-13 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 11/10/2026 | TRA-261011-033 | ROTA | L-2609-13 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 11/10/2026 | ING-261011-034 | PENT | L-2609-14 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 12/10/2026 | SAL-261012-035 | PENT | L-2609-14 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 12/10/2026 | TRA-261012-036 | NEUM | L-2609-14 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 13/10/2026 | AJU-261013-037 | ROTA | L-2609-15 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 14/10/2026 | AJU-261014-038 | INFL | L-2609-15 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 14/10/2026 | TRA-261014-039 | ROTA | L-2609-15 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 15/10/2026 | SAL-261015-040 | ROTA | L-2609-16 | 50 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 29/09/2026 | INFL | 60 | 60 | 0 | GR-260929-002 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 2 | 07/10/2026 | HEPB | 60 | 60 | 0 | GR-261007-212 | Sí | Conforme. Cantidad y guía coinciden. |
| 3 | 29/09/2026 | NEUM | 30 | 30 | 0 | GR-260929-182 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 4 | 15/10/2026 | BCG | 150 | 150 | 0 | GR-261015-085 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 5 | 03/10/2026 | BCG | 60 | 60 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 6 | 12/10/2026 | HEPB | 80 | 80 | 0 | GR-261012-187 | Sí | Conforme. Cantidad y guía coinciden. |
| 7 | 20/09/2026 | SPR | 150 | 150 | 0 | GR-260920-184 | Sí | Conforme. Cantidad y guía coinciden. |
| 8 | 08/10/2026 | IPV | 100 | 100 | 0 | GR-261008-008 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 9 | 22/09/2026 | HEPB | 180 | 180 | 0 | GR-260922-004 | Sí | Conforme. Cantidad y guía coinciden. |
| 10 | 01/10/2026 | SPR | 60 | 60 | 0 | GR-261001-105 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 11 | 03/10/2026 | HEPB | 40 | 40 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 12 | 26/09/2026 | SPR | 40 | 40 | 0 | GR-260926-195 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 13 | 23/09/2026 | VARI | 40 | 40 | 0 | GR-260923-191 | Sí | Conforme. Cantidad y guía coinciden. |
| 14 | 04/10/2026 | ROTA | 40 | 40 | 0 | GR-261004-039 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 15 | 18/09/2026 | INFL | 60 | 60 | 0 | GR-260918-087 | Sí | Conforme. Cantidad y guía coinciden. |
| 16 | 14/10/2026 | NEUM | 180 | 180 | 0 | GR-261014-103 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 17 | 27/09/2026 | INFL | 150 | 150 | 0 | GR-260927-094 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 18 | 15/10/2026 | INFL | 120 | 120 | 0 | GR-261015-023 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 19 | 25/09/2026 | PENT | 180 | 180 | 0 | GR-260925-220 | Sí | Conforme. Cantidad y guía coinciden. |
| 20 | 14/10/2026 | INFL | 20 | 20 | 0 | GR-261014-195 | Sí | Conforme. Cantidad y guía coinciden. |
| 21 | 21/09/2026 | ROTA | 40 | 40 | 0 | GR-260921-097 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 22 | 28/09/2026 | VARI | 150 | 150 | 0 | GR-260928-051 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 23 | 14/10/2026 | IPV | 60 | 60 | 0 | GR-261014-066 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 24 | 01/10/2026 | VARI | 30 | 30 | 0 | GR-261001-212 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 25 | 26/09/2026 | VARI | 120 | 120 | 0 | GR-260926-201 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |

**Observaciones**

- Auditoría realizada sobre el reporte de kardex emitido por el SIVAC.

---

### 2.15 · TRAB-08 · Pretest (proceso manual) · 13/08/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-08 | Huancaray | 18/07/2026 al 12/08/2026 | Pretest | OBS-02 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 30 · **RSD = 75.00 %** · Despachos evaluados: 25 · Concordantes: 20 · **CPE = 80.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 18/07/2026 | TRA-260718-001 | HEPB | L-2607-07 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 19/07/2026 | DEV-260719-002 | IPV | L-2607-07 | 100 | S | S | S | S | S | S | S | N | No | M8 |
| 3 | 19/07/2026 | DEV-260719-003 | VARI | L-2607-07 | 20 | S | S | S | S | S | S | S | N | No | M8 |
| 4 | 20/07/2026 | TRA-260720-004 | NEUM | L-2607-08 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 21/07/2026 | TRA-260721-005 | IPV | L-2607-08 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 21/07/2026 | ING-260721-006 | SPR | L-2607-08 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 22/07/2026 | AJU-260722-007 | HEPB | L-2607-09 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 23/07/2026 | TRA-260723-008 | PENT | L-2607-09 | 120 | N | S | S | S | S | S | S | S | No | M1 |
| 9 | 23/07/2026 | TRA-260723-009 | IPV | L-2607-09 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 24/07/2026 | SAL-260724-010 | NEUM | L-2607-10 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 25/07/2026 | SAL-260725-011 | BCG | L-2607-10 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 25/07/2026 | ING-260725-012 | VARI | L-2607-10 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 26/07/2026 | TRA-260726-013 | HEPB | L-2607-11 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 27/07/2026 | TRA-260727-014 | VARI | L-2607-11 | 20 | S | S | S | S | N | S | S | S | No | M5 |
| 15 | 27/07/2026 | AJU-260727-015 | IPV | L-2607-11 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 28/07/2026 | SAL-260728-016 | IPV | L-2607-12 | 80 | N | S | S | S | S | N | S | S | No | M1+M6 |
| 17 | 29/07/2026 | TRA-260729-017 | HEPB | L-2607-12 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 29/07/2026 | ING-260729-018 | IPV | L-2607-12 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 30/07/2026 | TRA-260730-019 | PENT | L-2607-13 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 31/07/2026 | SAL-260731-020 | DTA | L-2607-13 | 180 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 31/07/2026 | TRA-260731-021 | NEUM | L-2607-13 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 01/08/2026 | TRA-260801-022 | NEUM | L-2607-14 | 30 | N | S | S | S | S | S | S | S | No | M1 |
| 23 | 02/08/2026 | SAL-260802-023 | DTA | L-2607-14 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 02/08/2026 | SAL-260802-024 | DTA | L-2607-14 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 03/08/2026 | SAL-260803-025 | BCG | L-2607-15 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 04/08/2026 | AJU-260804-026 | INFL | L-2607-15 | 300 | S | S | S | S | S | N | S | S | No | M6 |
| 27 | 04/08/2026 | DEV-260804-027 | ROTA | L-2607-15 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 05/08/2026 | ING-260805-028 | VARI | L-2607-16 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 06/08/2026 | AJU-260806-029 | ROTA | L-2607-16 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 06/08/2026 | ING-260806-030 | ROTA | L-2607-16 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 07/08/2026 | SAL-260807-031 | SPR | L-2607-17 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 08/08/2026 | TRA-260808-032 | HEPB | L-2607-17 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 08/08/2026 | SAL-260808-033 | BCG | L-2607-17 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 09/08/2026 | DEV-260809-034 | DTA | L-2607-18 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 10/08/2026 | DEV-260810-035 | IPV | L-2607-18 | 60 | S | S | S | S | N | S | S | S | No | M5 |
| 36 | 10/08/2026 | SAL-260810-036 | SPR | L-2607-18 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 11/08/2026 | ING-260811-037 | ROTA | L-2607-19 | 300 | S | S | S | S | S | S | N | S | No | M7 |
| 38 | 12/08/2026 | TRA-260812-038 | IPV | L-2607-19 | 20 | S | S | N | S | S | S | S | N | No | M3+M8 |
| 39 | 12/08/2026 | TRA-260812-039 | BCG | L-2607-19 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 13/08/2026 | TRA-260813-040 | IPV | L-2607-20 | 300 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 29/07/2026 | PENT | 50 | 50 | 0 | GR-260729-207 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 2 | 29/07/2026 | NEUM | 180 | 180 | 0 | GR-260729-074 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 3 | 19/07/2026 | DTA | 80 | 80 | 0 | GR-260719-033 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 4 | 01/08/2026 | BCG | 80 | 80 | 0 | GR-260801-065 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 5 | 07/08/2026 | HEPB | 20 | 20 | 0 | GR-260807-050 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 6 | 28/07/2026 | ROTA | 20 | 20 | 0 | GR-260728-060 | Sí | Conforme. Cantidad y guía coinciden. |
| 7 | 01/08/2026 | HEPB | 20 | 20 | 0 | GR-260801-177 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 8 | 23/07/2026 | SPR | 100 | 100 | 0 | GR-260723-007 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 9 | 06/08/2026 | VARI | 40 | 45 | +5 | GR-260806-181 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 10 | 30/07/2026 | DTA | 180 | 180 | 0 | GR-260730-178 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 11 | 28/07/2026 | ROTA | 200 | 200 | 0 | GR-260728-142 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 12 | 28/07/2026 | PENT | 180 | 180 | 0 | GR-260728-138 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 13/08/2026 | BCG | 200 | 200 | 0 | GR-260813-212 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 14 | 27/07/2026 | INFL | 150 | 150 | 0 | GR-260727-157 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 15 | 22/07/2026 | NEUM | 200 | 200 | 0 | GR-260722-212 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 16 | 09/08/2026 | VARI | 150 | 150 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 17 | 30/07/2026 | SPR | 50 | 50 | 0 | GR-260730-128 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 18 | 25/07/2026 | VARI | 20 | 20 | 0 | GR-260725-219 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 19 | 03/08/2026 | HEPB | 40 | 30 | -10 | GR-260803-032 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 20 | 12/08/2026 | HEPB | 200 | 200 | 0 | GR-260812-122 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 21 | 30/07/2026 | HEPB | 40 | 40 | 0 | GR-260730-183 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 22 | 21/07/2026 | IPV | 80 | 80 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 23 | 04/08/2026 | SPR | 80 | 80 | 0 | GR-260804-062 | Sí | Conforme. Cantidad y guía coinciden. |
| 24 | 24/07/2026 | ROTA | 40 | 30 | -10 | GR-260724-131 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 25 | 31/07/2026 | ROTA | 80 | 80 | 0 | GR-260731-118 | Sí | Conforme. Verificado el FEFO al momento de la carga. |

**Observaciones**

- Dos folios del kardex estaban fuera de orden; se reconstruyó la correlatividad.

---

### 2.16 · TRAB-08 · Postest (Sistema SIVAC) · 15/10/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-08 | Huancaray | 12/09/2026 al 14/10/2026 | Postest | OBS-02 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 40 · **RSD = 100.00 %** · Despachos evaluados: 25 · Concordantes: 25 · **CPE = 100.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 12/09/2026 | SAL-260912-001 | PENT | L-2609-04 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 13/09/2026 | SAL-260913-002 | HEPB | L-2609-04 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 14/09/2026 | DEV-260914-003 | INFL | L-2609-04 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 15/09/2026 | DEV-260915-004 | HEPB | L-2609-05 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 15/09/2026 | SAL-260915-005 | IPV | L-2609-05 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 16/09/2026 | AJU-260916-006 | VARI | L-2609-05 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 17/09/2026 | ING-260917-007 | INFL | L-2609-06 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 18/09/2026 | AJU-260918-008 | ROTA | L-2609-06 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 19/09/2026 | AJU-260919-009 | NEUM | L-2609-06 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 20/09/2026 | SAL-260920-010 | SPR | L-2609-07 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 20/09/2026 | TRA-260920-011 | NEUM | L-2609-07 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 21/09/2026 | SAL-260921-012 | SPR | L-2609-07 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 22/09/2026 | DEV-260922-013 | HEPB | L-2609-08 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 23/09/2026 | DEV-260923-014 | ROTA | L-2609-08 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 24/09/2026 | TRA-260924-015 | ROTA | L-2609-08 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 25/09/2026 | AJU-260925-016 | IPV | L-2609-09 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 26/09/2026 | TRA-260926-017 | DTA | L-2609-09 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 26/09/2026 | TRA-260926-018 | ROTA | L-2609-09 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 27/09/2026 | ING-260927-019 | BCG | L-2609-10 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 28/09/2026 | TRA-260928-020 | SPR | L-2609-10 | 30 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 29/09/2026 | ING-260929-021 | NEUM | L-2609-10 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 30/09/2026 | ING-260930-022 | NEUM | L-2609-11 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 01/10/2026 | SAL-261001-023 | PENT | L-2609-11 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 01/10/2026 | ING-261001-024 | SPR | L-2609-11 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 02/10/2026 | TRA-261002-025 | SPR | L-2609-12 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 03/10/2026 | AJU-261003-026 | ROTA | L-2609-12 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 04/10/2026 | ING-261004-027 | PENT | L-2609-12 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 05/10/2026 | TRA-261005-028 | IPV | L-2609-13 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 06/10/2026 | ING-261006-029 | BCG | L-2609-13 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 07/10/2026 | ING-261007-030 | SPR | L-2609-13 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 07/10/2026 | TRA-261007-031 | INFL | L-2609-14 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 08/10/2026 | TRA-261008-032 | INFL | L-2609-14 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 09/10/2026 | ING-261009-033 | SPR | L-2609-14 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 10/10/2026 | SAL-261010-034 | DTA | L-2609-15 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 11/10/2026 | SAL-261011-035 | HEPB | L-2609-15 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 12/10/2026 | SAL-261012-036 | NEUM | L-2609-15 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 12/10/2026 | SAL-261012-037 | SPR | L-2609-16 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 13/10/2026 | SAL-261013-038 | ROTA | L-2609-16 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 14/10/2026 | AJU-261014-039 | SPR | L-2609-16 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 15/10/2026 | SAL-261015-040 | VARI | L-2609-17 | 80 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 25/09/2026 | DTA | 100 | 100 | 0 | GR-260925-160 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 2 | 29/09/2026 | INFL | 20 | 20 | 0 | GR-260929-070 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 3 | 29/09/2026 | INFL | 100 | 100 | 0 | GR-260929-167 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 4 | 18/09/2026 | BCG | 180 | 180 | 0 | GR-260918-085 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 5 | 21/09/2026 | PENT | 100 | 100 | 0 | GR-260921-141 | Sí | Conforme. Cantidad y guía coinciden. |
| 6 | 29/09/2026 | SPR | 40 | 40 | 0 | GR-260929-098 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 7 | 21/09/2026 | INFL | 50 | 50 | 0 | GR-260921-038 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 8 | 20/09/2026 | DTA | 20 | 20 | 0 | GR-260920-077 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 9 | 12/10/2026 | SPR | 20 | 20 | 0 | GR-261012-073 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 10 | 27/09/2026 | IPV | 150 | 150 | 0 | GR-260927-080 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 11 | 22/09/2026 | DTA | 30 | 30 | 0 | GR-260922-086 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 12 | 04/10/2026 | IPV | 150 | 150 | 0 | GR-261004-204 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 26/09/2026 | INFL | 60 | 60 | 0 | GR-260926-032 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 14 | 13/10/2026 | SPR | 120 | 120 | 0 | GR-261013-005 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 15 | 07/10/2026 | INFL | 100 | 100 | 0 | GR-261007-189 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 16 | 03/10/2026 | DTA | 150 | 150 | 0 | GR-261003-119 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 17 | 04/10/2026 | BCG | 120 | 120 | 0 | GR-261004-218 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 18 | 22/09/2026 | DTA | 100 | 100 | 0 | GR-260922-040 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 19 | 13/10/2026 | NEUM | 50 | 50 | 0 | GR-261013-011 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 20 | 24/09/2026 | PENT | 50 | 50 | 0 | GR-260924-111 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 21 | 12/10/2026 | VARI | 180 | 180 | 0 | GR-261012-053 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 22 | 23/09/2026 | NEUM | 20 | 20 | 0 | GR-260923-085 | Sí | Conforme. Cantidad y guía coinciden. |
| 23 | 01/10/2026 | NEUM | 150 | 150 | 0 | GR-261001-177 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 24 | 03/10/2026 | BCG | 100 | 100 | 0 | GR-261003-150 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 25 | 11/10/2026 | PENT | 150 | 150 | 0 | GR-261011-043 | Sí | Conforme. Cantidad y guía coinciden. |

**Observaciones**

- Los asientos se contrastaron con la trazabilidad de movimientos del sistema.

---

### 2.17 · TRAB-09 · Pretest (proceso manual) · 14/08/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-09 | Chicmo | 17/07/2026 al 13/08/2026 | Pretest | OBS-01 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 29 · **RSD = 72.50 %** · Despachos evaluados: 25 · Concordantes: 19 · **CPE = 76.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 17/07/2026 | TRA-260717-001 | HEPB | L-2607-03 | 20 | S | S | S | S | S | N | S | S | No | M6 |
| 2 | 18/07/2026 | DEV-260718-002 | HEPB | L-2607-03 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 18/07/2026 | SAL-260718-003 | PENT | L-2607-03 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 19/07/2026 | SAL-260719-004 | NEUM | L-2607-04 | 20 | S | S | S | S | S | S | N | S | No | M7 |
| 5 | 20/07/2026 | TRA-260720-005 | HEPB | L-2607-04 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 21/07/2026 | DEV-260721-006 | IPV | L-2607-04 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 21/07/2026 | SAL-260721-007 | BCG | L-2607-05 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 22/07/2026 | AJU-260722-008 | HEPB | L-2607-05 | 300 | S | N | S | S | S | S | S | S | No | M2 |
| 9 | 23/07/2026 | ING-260723-009 | DTA | L-2607-05 | 300 | S | S | S | S | S | N | S | S | No | M6 |
| 10 | 23/07/2026 | TRA-260723-010 | IPV | L-2607-06 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 24/07/2026 | AJU-260724-011 | INFL | L-2607-06 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 25/07/2026 | ING-260725-012 | HEPB | L-2607-06 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 26/07/2026 | TRA-260726-013 | HEPB | L-2607-07 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 26/07/2026 | ING-260726-014 | IPV | L-2607-07 | 80 | S | S | S | S | S | S | S | N | No | M8 |
| 15 | 27/07/2026 | SAL-260727-015 | HEPB | L-2607-07 | 120 | S | S | S | S | N | N | S | S | No | M5+M6 |
| 16 | 28/07/2026 | SAL-260728-016 | BCG | L-2607-08 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 28/07/2026 | SAL-260728-017 | BCG | L-2607-08 | 120 | S | S | S | S | S | S | S | N | No | M8 |
| 18 | 29/07/2026 | TRA-260729-018 | PENT | L-2607-08 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 30/07/2026 | TRA-260730-019 | VARI | L-2607-09 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 31/07/2026 | ING-260731-020 | BCG | L-2607-09 | 50 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 31/07/2026 | SAL-260731-021 | NEUM | L-2607-09 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 01/08/2026 | AJU-260801-022 | SPR | L-2607-10 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 02/08/2026 | TRA-260802-023 | VARI | L-2607-10 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 03/08/2026 | DEV-260803-024 | SPR | L-2607-10 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 03/08/2026 | AJU-260803-025 | INFL | L-2607-11 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 04/08/2026 | ING-260804-026 | PENT | L-2607-11 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 05/08/2026 | SAL-260805-027 | BCG | L-2607-11 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 05/08/2026 | ING-260805-028 | INFL | L-2607-12 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 06/08/2026 | SAL-260806-029 | INFL | L-2607-12 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 07/08/2026 | ING-260807-030 | PENT | L-2607-12 | 300 | S | S | S | N | S | S | S | S | No | M4 |
| 31 | 08/08/2026 | SAL-260808-031 | SPR | L-2607-13 | 240 | S | S | S | S | S | S | S | N | No | M8 |
| 32 | 08/08/2026 | DEV-260808-032 | ROTA | L-2607-13 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 09/08/2026 | TRA-260809-033 | SPR | L-2607-13 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 10/08/2026 | TRA-260810-034 | VARI | L-2607-14 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 10/08/2026 | SAL-260810-035 | VARI | L-2607-14 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 11/08/2026 | ING-260811-036 | SPR | L-2607-14 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 12/08/2026 | DEV-260812-037 | ROTA | L-2607-15 | 150 | S | N | S | S | S | S | S | S | No | M2 |
| 38 | 13/08/2026 | ING-260813-038 | NEUM | L-2607-15 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 13/08/2026 | ING-260813-039 | VARI | L-2607-15 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 14/08/2026 | AJU-260814-040 | NEUM | L-2607-16 | 120 | N | S | S | N | S | S | S | S | No | M1+M4 |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 02/08/2026 | NEUM | 20 | 20 | 0 | GR-260802-201 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 2 | 18/07/2026 | VARI | 30 | 30 | 0 | GR-260718-133 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 3 | 09/08/2026 | SPR | 30 | 30 | 0 | GR-260809-032 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 4 | 20/07/2026 | HEPB | 120 | 120 | 0 | GR-260720-108 | Sí | Conforme. Cantidad y guía coinciden. |
| 5 | 05/08/2026 | HEPB | 60 | 55 | -5 | GR-260805-062 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 6 | 12/08/2026 | VARI | 200 | 200 | 0 | GR-260812-170 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 7 | 28/07/2026 | INFL | 20 | 20 | 0 | GR-260728-184 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 8 | 30/07/2026 | SPR | 80 | 80 | 0 | GR-260730-203 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 9 | 06/08/2026 | BCG | 80 | 80 | 0 | GR-260806-173 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 10 | 31/07/2026 | HEPB | 20 | 0 | -20 | GR-260731-208 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 11 | 29/07/2026 | INFL | 100 | 100 | 0 | GR-260729-002 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 12 | 04/08/2026 | HEPB | 180 | 180 | 0 | GR-260804-116 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 13 | 04/08/2026 | IPV | 60 | 60 | 0 | GR-260804-215 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 14 | 13/08/2026 | PENT | 50 | 45 | -5 | GR-260813-210 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 15 | 10/08/2026 | SPR | 120 | 120 | 0 | GR-260810-045 | Sí | Conforme. Cantidad y guía coinciden. |
| 16 | 27/07/2026 | BCG | 180 | 180 | 0 | GR-260727-150 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 17 | 01/08/2026 | DTA | 80 | 80 | 0 | GR-260801-182 | Sí | Conforme. Cantidad y guía coinciden. |
| 18 | 28/07/2026 | ROTA | 180 | 180 | 0 | GR-260728-007 | Sí | Conforme. Cantidad y guía coinciden. |
| 19 | 13/08/2026 | IPV | 50 | 45 | -5 | GR-260813-003 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 20 | 21/07/2026 | HEPB | 150 | 150 | 0 | GR-260721-055 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 21 | 21/07/2026 | SPR | 150 | 150 | 0 | GR-260721-019 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 22 | 10/08/2026 | HEPB | 150 | 150 | 0 | GR-260810-100 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 23 | 08/08/2026 | DTA | 20 | 20 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 24 | 18/07/2026 | DTA | 20 | 10 | -10 | GR-260718-051 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 25 | 09/08/2026 | BCG | 150 | 150 | 0 | GR-260809-213 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |

**Observaciones**

- El operador sustentó verbalmente los asientos observados; no se corrigió la hoja.

---

### 2.18 · TRAB-09 · Postest (Sistema SIVAC) · 16/10/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-09 | Chicmo | 19/09/2026 al 15/10/2026 | Postest | OBS-01 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 39 · **RSD = 97.50 %** · Despachos evaluados: 25 · Concordantes: 24 · **CPE = 96.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 19/09/2026 | TRA-260919-001 | HEPB | L-2609-06 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 20/09/2026 | ING-260920-002 | HEPB | L-2609-06 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 20/09/2026 | ING-260920-003 | DTA | L-2609-06 | 120 | S | S | S | S | S | N | N | S | No | M6+M7 |
| 4 | 21/09/2026 | ING-260921-004 | HEPB | L-2609-07 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 22/09/2026 | SAL-260922-005 | INFL | L-2609-07 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 22/09/2026 | SAL-260922-006 | BCG | L-2609-07 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 23/09/2026 | DEV-260923-007 | DTA | L-2609-08 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 24/09/2026 | AJU-260924-008 | SPR | L-2609-08 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 25/09/2026 | SAL-260925-009 | HEPB | L-2609-08 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 25/09/2026 | AJU-260925-010 | ROTA | L-2609-09 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 26/09/2026 | DEV-260926-011 | IPV | L-2609-09 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 27/09/2026 | TRA-260927-012 | IPV | L-2609-09 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 27/09/2026 | SAL-260927-013 | HEPB | L-2609-10 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 28/09/2026 | DEV-260928-014 | VARI | L-2609-10 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 29/09/2026 | TRA-260929-015 | ROTA | L-2609-10 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 29/09/2026 | SAL-260929-016 | INFL | L-2609-11 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 30/09/2026 | TRA-260930-017 | INFL | L-2609-11 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 01/10/2026 | DEV-261001-018 | DTA | L-2609-11 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 01/10/2026 | AJU-261001-019 | BCG | L-2609-12 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 02/10/2026 | SAL-261002-020 | ROTA | L-2609-12 | 30 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 03/10/2026 | SAL-261003-021 | BCG | L-2609-12 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 04/10/2026 | SAL-261004-022 | HEPB | L-2609-13 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 04/10/2026 | ING-261004-023 | INFL | L-2609-13 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 05/10/2026 | SAL-261005-024 | INFL | L-2609-13 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 06/10/2026 | SAL-261006-025 | INFL | L-2609-14 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 06/10/2026 | SAL-261006-026 | HEPB | L-2609-14 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 07/10/2026 | ING-261007-027 | IPV | L-2609-14 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 08/10/2026 | ING-261008-028 | IPV | L-2609-15 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 08/10/2026 | ING-261008-029 | NEUM | L-2609-15 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 09/10/2026 | SAL-261009-030 | HEPB | L-2609-15 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 10/10/2026 | ING-261010-031 | HEPB | L-2609-16 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 10/10/2026 | ING-261010-032 | HEPB | L-2609-16 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 11/10/2026 | ING-261011-033 | DTA | L-2609-16 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 12/10/2026 | TRA-261012-034 | NEUM | L-2609-17 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 13/10/2026 | TRA-261013-035 | ROTA | L-2609-17 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 13/10/2026 | DEV-261013-036 | PENT | L-2609-17 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 14/10/2026 | AJU-261014-037 | ROTA | L-2609-18 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 15/10/2026 | SAL-261015-038 | NEUM | L-2609-18 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 15/10/2026 | ING-261015-039 | ROTA | L-2609-18 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 16/10/2026 | ING-261016-040 | DTA | L-2609-19 | 300 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 28/09/2026 | BCG | 180 | 170 | -10 | GR-260928-019 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 2 | 09/10/2026 | PENT | 40 | 40 | 0 | GR-261009-003 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 3 | 15/10/2026 | HEPB | 80 | 80 | 0 | GR-261015-131 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 4 | 23/09/2026 | BCG | 100 | 100 | 0 | GR-260923-029 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 5 | 03/10/2026 | BCG | 120 | 120 | 0 | GR-261003-190 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 6 | 10/10/2026 | NEUM | 50 | 50 | 0 | GR-261010-174 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 7 | 23/09/2026 | INFL | 100 | 100 | 0 | GR-260923-153 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 8 | 28/09/2026 | BCG | 20 | 20 | 0 | GR-260928-089 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 9 | 10/10/2026 | PENT | 30 | 30 | 0 | GR-261010-010 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 10 | 01/10/2026 | SPR | 60 | 60 | 0 | GR-261001-093 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 11 | 18/09/2026 | DTA | 150 | 150 | 0 | GR-260918-002 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 12 | 14/10/2026 | NEUM | 40 | 40 | 0 | GR-261014-210 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 13 | 24/09/2026 | SPR | 60 | 60 | 0 | GR-260924-120 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 14 | 21/09/2026 | VARI | 200 | 200 | 0 | GR-260921-046 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 15 | 08/10/2026 | VARI | 100 | 100 | 0 | GR-261008-197 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 16 | 21/09/2026 | ROTA | 150 | 150 | 0 | GR-260921-015 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 17 | 16/10/2026 | VARI | 100 | 100 | 0 | GR-261016-017 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 18 | 04/10/2026 | HEPB | 30 | 30 | 0 | GR-261004-191 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 19 | 16/10/2026 | NEUM | 100 | 100 | 0 | GR-261016-001 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 20 | 19/09/2026 | INFL | 40 | 40 | 0 | GR-260919-216 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 21 | 28/09/2026 | PENT | 60 | 60 | 0 | GR-260928-013 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 22 | 28/09/2026 | INFL | 180 | 180 | 0 | GR-260928-218 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 23 | 14/10/2026 | ROTA | 50 | 50 | 0 | GR-261014-204 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 24 | 08/10/2026 | NEUM | 200 | 200 | 0 | GR-261008-068 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 25 | 01/10/2026 | ROTA | 80 | 80 | 0 | GR-261001-200 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |

**Observaciones**

- Las observaciones pendientes corresponden a firmas en regularización.

---

### 2.19 · TRAB-10 · Pretest (proceso manual) · 14/08/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-10 | Huancabamba | 13/07/2026 al 13/08/2026 | Pretest | OBS-02 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 24 · **RSD = 60.00 %** · Despachos evaluados: 25 · Concordantes: 16 · **CPE = 64.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 13/07/2026 | TRA-260713-001 | VARI | L-2607-06 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 14/07/2026 | AJU-260714-002 | BCG | L-2607-06 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 15/07/2026 | ING-260715-003 | VARI | L-2607-06 | 180 | S | S | S | N | S | S | S | S | No | M4 |
| 4 | 15/07/2026 | ING-260715-004 | NEUM | L-2607-07 | 240 | S | S | S | S | N | S | S | S | No | M5 |
| 5 | 16/07/2026 | SAL-260716-005 | DTA | L-2607-07 | 150 | S | S | S | S | S | N | S | S | No | M6 |
| 6 | 17/07/2026 | AJU-260717-006 | ROTA | L-2607-07 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 18/07/2026 | SAL-260718-007 | VARI | L-2607-08 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 19/07/2026 | TRA-260719-008 | IPV | L-2607-08 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 20/07/2026 | ING-260720-009 | SPR | L-2607-08 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 20/07/2026 | SAL-260720-010 | HEPB | L-2607-09 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 21/07/2026 | SAL-260721-011 | IPV | L-2607-09 | 240 | S | S | S | S | S | S | S | N | No | M8 |
| 12 | 22/07/2026 | SAL-260722-012 | HEPB | L-2607-09 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 23/07/2026 | SAL-260723-013 | PENT | L-2607-10 | 50 | S | S | S | S | S | N | S | S | No | M6 |
| 14 | 24/07/2026 | SAL-260724-014 | DTA | L-2607-10 | 180 | S | S | S | S | S | S | N | S | No | M7 |
| 15 | 24/07/2026 | ING-260724-015 | HEPB | L-2607-10 | 100 | S | S | S | S | S | S | N | S | No | M7 |
| 16 | 25/07/2026 | SAL-260725-016 | SPR | L-2607-11 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 26/07/2026 | SAL-260726-017 | BCG | L-2607-11 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 27/07/2026 | ING-260727-018 | IPV | L-2607-11 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 28/07/2026 | SAL-260728-019 | ROTA | L-2607-12 | 120 | S | S | S | S | S | N | N | S | No | M6+M7 |
| 20 | 29/07/2026 | SAL-260729-020 | IPV | L-2607-12 | 180 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 29/07/2026 | DEV-260729-021 | PENT | L-2607-12 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 30/07/2026 | DEV-260730-022 | BCG | L-2607-13 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 31/07/2026 | SAL-260731-023 | IPV | L-2607-13 | 40 | S | S | S | S | S | S | S | N | No | M8 |
| 24 | 01/08/2026 | SAL-260801-024 | DTA | L-2607-13 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 02/08/2026 | ING-260802-025 | SPR | L-2607-14 | 150 | S | S | S | N | S | S | S | S | No | M4 |
| 26 | 03/08/2026 | ING-260803-026 | INFL | L-2607-14 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 03/08/2026 | ING-260803-027 | DTA | L-2607-14 | 120 | S | N | S | S | S | S | S | N | No | M2+M8 |
| 28 | 04/08/2026 | SAL-260804-028 | SPR | L-2607-15 | 240 | S | N | S | S | S | S | S | S | No | M2 |
| 29 | 05/08/2026 | ING-260805-029 | SPR | L-2607-15 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 06/08/2026 | SAL-260806-030 | VARI | L-2607-15 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 07/08/2026 | SAL-260807-031 | DTA | L-2607-16 | 180 | S | S | S | S | S | S | N | S | No | M7 |
| 32 | 07/08/2026 | TRA-260807-032 | ROTA | L-2607-16 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 08/08/2026 | TRA-260808-033 | VARI | L-2607-16 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 09/08/2026 | ING-260809-034 | PENT | L-2607-17 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 10/08/2026 | TRA-260810-035 | DTA | L-2607-17 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 11/08/2026 | AJU-260811-036 | SPR | L-2607-17 | 30 | S | S | S | S | S | N | S | N | No | M6+M8 |
| 37 | 12/08/2026 | DEV-260812-037 | PENT | L-2607-18 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 12/08/2026 | ING-260812-038 | IPV | L-2607-18 | 30 | S | S | S | S | S | S | S | N | No | M8 |
| 39 | 13/08/2026 | ING-260813-039 | VARI | L-2607-18 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 14/08/2026 | ING-260814-040 | NEUM | L-2607-19 | 50 | S | S | N | S | S | S | N | S | No | M3+M7 |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 28/07/2026 | VARI | 150 | 130 | -20 | GR-260728-032 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 2 | 12/08/2026 | VARI | 100 | 100 | 0 | GR-260812-071 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 3 | 31/07/2026 | ROTA | 180 | 160 | -20 | GR-260731-220 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 4 | 08/08/2026 | NEUM | 100 | 100 | 0 | GR-260808-105 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 5 | 29/07/2026 | VARI | 60 | 60 | 0 | GR-260729-047 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 6 | 12/08/2026 | PENT | 120 | 120 | 0 | GR-260812-152 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 7 | 20/07/2026 | DTA | 180 | 180 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 8 | 28/07/2026 | IPV | 200 | 190 | -10 | GR-260728-165 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 9 | 11/08/2026 | DTA | 120 | 120 | 0 | GR-260811-181 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 10 | 29/07/2026 | PENT | 60 | 60 | 0 | GR-260729-132 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 11 | 27/07/2026 | ROTA | 100 | 100 | 0 | GR-260727-192 | Sí | Conforme. Cantidad y guía coinciden. |
| 12 | 07/08/2026 | BCG | 200 | 200 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 13 | 26/07/2026 | DTA | 60 | 60 | 0 | GR-260726-087 | Sí | Conforme. Cantidad y guía coinciden. |
| 14 | 02/08/2026 | SPR | 30 | 30 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 15 | 24/07/2026 | SPR | 60 | 60 | 0 | GR-260724-143 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 16 | 27/07/2026 | ROTA | 120 | 120 | 0 | GR-260727-127 | Sí | Conforme. Cantidad y guía coinciden. |
| 17 | 08/08/2026 | IPV | 40 | 40 | 0 | GR-260808-001 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 18 | 05/08/2026 | BCG | 80 | 75 | -5 | GR-260805-090 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 19 | 21/07/2026 | VARI | 40 | 40 | 0 | GR-260721-188 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 20 | 26/07/2026 | INFL | 120 | 115 | -5 | GR-260726-168 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 21 | 19/07/2026 | NEUM | 120 | 120 | 0 | GR-260719-101 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 22 | 22/07/2026 | DTA | 150 | 150 | 0 | GR-260722-162 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 23 | 14/08/2026 | VARI | 80 | 70 | -10 | GR-260814-168 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 24 | 27/07/2026 | PENT | 30 | 30 | 0 | GR-260727-020 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 25 | 04/08/2026 | VARI | 200 | 200 | 0 | GR-260804-202 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |

**Observaciones**

- El operador sustentó verbalmente los asientos observados; no se corrigió la hoja.

---

### 2.20 · TRAB-10 · Postest (Sistema SIVAC) · 16/10/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-10 | Huancabamba | 15/09/2026 al 15/10/2026 | Postest | OBS-02 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 38 · **RSD = 95.00 %** · Despachos evaluados: 25 · Concordantes: 24 · **CPE = 96.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 15/09/2026 | AJU-260915-001 | BCG | L-2609-10 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 16/09/2026 | AJU-260916-002 | HEPB | L-2609-10 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 17/09/2026 | SAL-260917-003 | DTA | L-2609-10 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 17/09/2026 | ING-260917-004 | BCG | L-2609-11 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 18/09/2026 | AJU-260918-005 | ROTA | L-2609-11 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 19/09/2026 | DEV-260919-006 | INFL | L-2609-11 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 20/09/2026 | ING-260920-007 | DTA | L-2609-12 | 240 | S | S | S | S | S | S | N | S | No | M7 |
| 8 | 21/09/2026 | AJU-260921-008 | BCG | L-2609-12 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 21/09/2026 | TRA-260921-009 | NEUM | L-2609-12 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 22/09/2026 | TRA-260922-010 | ROTA | L-2609-13 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 23/09/2026 | AJU-260923-011 | HEPB | L-2609-13 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 24/09/2026 | TRA-260924-012 | SPR | L-2609-13 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 25/09/2026 | AJU-260925-013 | DTA | L-2609-14 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 25/09/2026 | TRA-260925-014 | IPV | L-2609-14 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 26/09/2026 | TRA-260926-015 | HEPB | L-2609-14 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 27/09/2026 | SAL-260927-016 | INFL | L-2609-15 | 60 | S | N | S | S | S | N | S | S | No | M2+M6 |
| 17 | 28/09/2026 | SAL-260928-017 | IPV | L-2609-15 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 29/09/2026 | DEV-260929-018 | VARI | L-2609-15 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 29/09/2026 | SAL-260929-019 | SPR | L-2609-16 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 30/09/2026 | TRA-260930-020 | NEUM | L-2609-16 | 300 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 01/10/2026 | SAL-261001-021 | SPR | L-2609-16 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 02/10/2026 | DEV-261002-022 | DTA | L-2609-17 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 02/10/2026 | ING-261002-023 | ROTA | L-2609-17 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 03/10/2026 | SAL-261003-024 | BCG | L-2609-17 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 04/10/2026 | TRA-261004-025 | INFL | L-2609-18 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 05/10/2026 | TRA-261005-026 | NEUM | L-2609-18 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 06/10/2026 | TRA-261006-027 | ROTA | L-2609-18 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 06/10/2026 | DEV-261006-028 | ROTA | L-2609-19 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 07/10/2026 | SAL-261007-029 | ROTA | L-2609-19 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 08/10/2026 | SAL-261008-030 | PENT | L-2609-19 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 09/10/2026 | SAL-261009-031 | VARI | L-2609-20 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 10/10/2026 | SAL-261010-032 | ROTA | L-2609-20 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 10/10/2026 | AJU-261010-033 | SPR | L-2609-20 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 11/10/2026 | DEV-261011-034 | NEUM | L-2609-21 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 12/10/2026 | SAL-261012-035 | DTA | L-2609-21 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 13/10/2026 | SAL-261013-036 | PENT | L-2609-21 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 14/10/2026 | TRA-261014-037 | VARI | L-2609-22 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 14/10/2026 | TRA-261014-038 | SPR | L-2609-22 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 15/10/2026 | TRA-261015-039 | VARI | L-2609-22 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 16/10/2026 | TRA-261016-040 | DTA | L-2609-23 | 300 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 18/09/2026 | ROTA | 50 | 50 | 0 | GR-260918-066 | Sí | Conforme. Cantidad y guía coinciden. |
| 2 | 07/10/2026 | IPV | 20 | 20 | 0 | GR-261007-110 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 3 | 02/10/2026 | IPV | 60 | 60 | 0 | GR-261002-121 | Sí | Conforme. Cantidad y guía coinciden. |
| 4 | 16/10/2026 | DTA | 200 | 200 | 0 | GR-261016-146 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 5 | 10/10/2026 | PENT | 20 | 20 | 0 | GR-261010-016 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 6 | 23/09/2026 | ROTA | 180 | 180 | 0 | GR-260923-084 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 7 | 21/09/2026 | DTA | 30 | 30 | 0 | GR-260921-170 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 8 | 21/09/2026 | PENT | 100 | 100 | 0 | GR-260921-008 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 9 | 01/10/2026 | ROTA | 80 | 80 | 0 | GR-261001-162 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 10 | 20/09/2026 | SPR | 120 | 110 | -10 | GR-260920-220 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 11 | 04/10/2026 | ROTA | 60 | 60 | 0 | GR-261004-008 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 12 | 05/10/2026 | DTA | 40 | 40 | 0 | GR-261005-132 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 13 | 18/09/2026 | INFL | 80 | 80 | 0 | GR-260918-206 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 14 | 08/10/2026 | DTA | 120 | 120 | 0 | GR-261008-023 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 15 | 20/09/2026 | NEUM | 180 | 180 | 0 | GR-260920-102 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 16 | 08/10/2026 | DTA | 40 | 40 | 0 | GR-261008-199 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 17 | 25/09/2026 | HEPB | 60 | 60 | 0 | GR-260925-048 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 18 | 16/10/2026 | IPV | 60 | 60 | 0 | GR-261016-116 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 19 | 13/10/2026 | ROTA | 180 | 180 | 0 | GR-261013-022 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 20 | 18/09/2026 | IPV | 30 | 30 | 0 | GR-260918-131 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 21 | 28/09/2026 | IPV | 30 | 30 | 0 | GR-260928-219 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 22 | 28/09/2026 | IPV | 180 | 180 | 0 | GR-260928-001 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 23 | 04/10/2026 | DTA | 180 | 180 | 0 | GR-261004-065 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 24 | 11/10/2026 | ROTA | 180 | 180 | 0 | GR-261011-201 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 25 | 26/09/2026 | IPV | 180 | 180 | 0 | GR-260926-072 | Sí | Conforme. Verificado el FEFO al momento de la carga. |

**Observaciones**

- El sistema permitió reconstruir la correlatividad sin revisar el archivo físico.

---

### 2.21 · TRAB-11 · Pretest (proceso manual) · 07/09/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-11 | Pampachiri | 06/08/2026 al 06/09/2026 | Pretest | OBS-01 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 25 · **RSD = 62.50 %** · Despachos evaluados: 25 · Concordantes: 17 · **CPE = 68.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 06/08/2026 | ING-260806-001 | NEUM | L-2608-06 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 07/08/2026 | ING-260807-002 | PENT | L-2608-06 | 80 | S | S | S | S | N | S | S | S | No | M5 |
| 3 | 08/08/2026 | SAL-260808-003 | PENT | L-2608-06 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 08/08/2026 | ING-260808-004 | VARI | L-2608-07 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 09/08/2026 | ING-260809-005 | NEUM | L-2608-07 | 150 | S | S | N | S | S | S | S | S | No | M3 |
| 6 | 10/08/2026 | TRA-260810-006 | VARI | L-2608-07 | 120 | S | S | S | S | S | S | S | N | No | M8 |
| 7 | 11/08/2026 | ING-260811-007 | DTA | L-2608-08 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 12/08/2026 | ING-260812-008 | NEUM | L-2608-08 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 13/08/2026 | TRA-260813-009 | HEPB | L-2608-08 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 13/08/2026 | ING-260813-010 | ROTA | L-2608-09 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 14/08/2026 | ING-260814-011 | IPV | L-2608-09 | 300 | S | S | S | S | S | S | N | S | No | M7 |
| 12 | 15/08/2026 | ING-260815-012 | SPR | L-2608-09 | 60 | S | N | S | S | S | S | S | S | No | M2 |
| 13 | 16/08/2026 | SAL-260816-013 | NEUM | L-2608-10 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 17/08/2026 | TRA-260817-014 | SPR | L-2608-10 | 240 | S | S | S | S | S | S | N | S | No | M7 |
| 15 | 17/08/2026 | ING-260817-015 | DTA | L-2608-10 | 200 | S | S | S | S | S | S | S | N | No | M8 |
| 16 | 18/08/2026 | ING-260818-016 | ROTA | L-2608-11 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 19/08/2026 | ING-260819-017 | PENT | L-2608-11 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 20/08/2026 | TRA-260820-018 | IPV | L-2608-11 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 21/08/2026 | SAL-260821-019 | VARI | L-2608-12 | 300 | S | S | S | N | S | S | S | S | No | M4 |
| 20 | 22/08/2026 | TRA-260822-020 | SPR | L-2608-12 | 100 | S | S | S | S | S | N | S | S | No | M6 |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 22/08/2026 | SAL-260822-021 | VARI | L-2608-12 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 23/08/2026 | ING-260823-022 | PENT | L-2608-13 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 24/08/2026 | TRA-260824-023 | INFL | L-2608-13 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 25/08/2026 | ING-260825-024 | HEPB | L-2608-13 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 26/08/2026 | SAL-260826-025 | NEUM | L-2608-14 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 27/08/2026 | SAL-260827-026 | ROTA | L-2608-14 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 27/08/2026 | SAL-260827-027 | DTA | L-2608-14 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 28/08/2026 | SAL-260828-028 | BCG | L-2608-15 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 29/08/2026 | ING-260829-029 | VARI | L-2608-15 | 150 | S | S | N | S | S | S | S | S | No | M3 |
| 30 | 30/08/2026 | TRA-260830-030 | DTA | L-2608-15 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 31/08/2026 | SAL-260831-031 | DTA | L-2608-16 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 31/08/2026 | SAL-260831-032 | NEUM | L-2608-16 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 01/09/2026 | ING-260901-033 | ROTA | L-2608-16 | 100 | S | N | S | S | N | S | S | S | No | M2+M5 |
| 34 | 02/09/2026 | SAL-260902-034 | ROTA | L-2608-17 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 03/09/2026 | TRA-260903-035 | VARI | L-2608-17 | 30 | S | N | S | S | S | S | S | S | No | M2 |
| 36 | 04/09/2026 | ING-260904-036 | SPR | L-2608-17 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 05/09/2026 | SAL-260905-037 | DTA | L-2608-18 | 120 | S | S | S | S | S | S | N | N | No | M7+M8 |
| 38 | 05/09/2026 | SAL-260905-038 | VARI | L-2608-18 | 300 | S | S | S | N | S | S | N | S | No | M4+M7 |
| 39 | 06/09/2026 | ING-260906-039 | NEUM | L-2608-18 | 20 | S | S | S | S | S | S | N | S | No | M7 |
| 40 | 07/09/2026 | AJU-260907-040 | DTA | L-2608-19 | 300 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 24/08/2026 | DTA | 150 | 150 | 0 | GR-260824-179 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 2 | 24/08/2026 | PENT | 50 | 50 | 0 | GR-260824-047 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 3 | 12/08/2026 | ROTA | 30 | 30 | 0 | GR-260812-177 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 4 | 19/08/2026 | VARI | 180 | 180 | 0 | GR-260819-042 | Sí | Conforme. Cantidad y guía coinciden. |
| 5 | 28/08/2026 | VARI | 180 | 160 | -20 | GR-260828-130 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 6 | 06/09/2026 | IPV | 100 | 100 | 0 | GR-260906-052 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 7 | 15/08/2026 | PENT | 60 | 60 | 0 | GR-260815-207 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 8 | 04/09/2026 | INFL | 80 | 80 | 0 | GR-260904-191 | Sí | Conforme. Cantidad y guía coinciden. |
| 9 | 02/09/2026 | IPV | 60 | 60 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 10 | 11/08/2026 | HEPB | 80 | 75 | -5 | GR-260811-205 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 11 | 30/08/2026 | ROTA | 150 | 150 | 0 | GR-260830-220 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 12 | 11/08/2026 | DTA | 180 | 180 | 0 | GR-260811-155 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 13 | 18/08/2026 | INFL | 30 | 30 | 0 | GR-260818-082 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 14 | 12/08/2026 | IPV | 150 | 150 | 0 | GR-260812-095 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 15 | 23/08/2026 | BCG | 100 | 100 | 0 | GR-260823-098 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 16 | 20/08/2026 | SPR | 100 | 100 | 0 | GR-260820-010 | Sí | Conforme. Cantidad y guía coinciden. |
| 17 | 01/09/2026 | BCG | 200 | 200 | 0 | GR-260901-119 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 18 | 19/08/2026 | INFL | 100 | 90 | -10 | GR-260819-173 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 19 | 27/08/2026 | BCG | 150 | 150 | 0 | GR-260827-106 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 20 | 20/08/2026 | HEPB | 120 | 120 | 0 | GR-260820-159 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 21 | 24/08/2026 | INFL | 80 | 85 | +5 | GR-260824-176 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 22 | 30/08/2026 | INFL | 40 | 35 | -5 | GR-260830-118 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 23 | 27/08/2026 | NEUM | 120 | 100 | -20 | GR-260827-004 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 24 | 02/09/2026 | PENT | 50 | 50 | 0 | GR-260902-154 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 25 | 12/08/2026 | SPR | 80 | 80 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |

**Observaciones**

- Auditoría realizada con el kardex físico y el talonario de vales del periodo.

---

### 2.22 · TRAB-11 · Postest (Sistema SIVAC) · 19/10/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-11 | Pampachiri | 18/09/2026 al 18/10/2026 | Postest | OBS-01 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 38 · **RSD = 95.00 %** · Despachos evaluados: 25 · Concordantes: 24 · **CPE = 96.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 18/09/2026 | ING-260918-001 | PENT | L-2609-11 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 19/09/2026 | ING-260919-002 | NEUM | L-2609-11 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 20/09/2026 | SAL-260920-003 | NEUM | L-2609-11 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 20/09/2026 | SAL-260920-004 | PENT | L-2609-12 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 21/09/2026 | TRA-260921-005 | IPV | L-2609-12 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 22/09/2026 | ING-260922-006 | SPR | L-2609-12 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 23/09/2026 | AJU-260923-007 | ROTA | L-2609-13 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 24/09/2026 | ING-260924-008 | VARI | L-2609-13 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 24/09/2026 | DEV-260924-009 | PENT | L-2609-13 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 25/09/2026 | TRA-260925-010 | HEPB | L-2609-14 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 26/09/2026 | SAL-260926-011 | PENT | L-2609-14 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 27/09/2026 | ING-260927-012 | IPV | L-2609-14 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 28/09/2026 | ING-260928-013 | NEUM | L-2609-15 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 28/09/2026 | ING-260928-014 | HEPB | L-2609-15 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 29/09/2026 | TRA-260929-015 | SPR | L-2609-15 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 30/09/2026 | ING-260930-016 | ROTA | L-2609-16 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 01/10/2026 | TRA-261001-017 | HEPB | L-2609-16 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 02/10/2026 | SAL-261002-018 | SPR | L-2609-16 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 02/10/2026 | ING-261002-019 | ROTA | L-2609-17 | 30 | S | S | S | N | S | S | N | S | No | M4+M7 |
| 20 | 03/10/2026 | SAL-261003-020 | HEPB | L-2609-17 | 80 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 04/10/2026 | TRA-261004-021 | SPR | L-2609-17 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 05/10/2026 | TRA-261005-022 | HEPB | L-2609-18 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 05/10/2026 | TRA-261005-023 | VARI | L-2609-18 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 06/10/2026 | ING-261006-024 | NEUM | L-2609-18 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 07/10/2026 | ING-261007-025 | HEPB | L-2609-19 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 08/10/2026 | SAL-261008-026 | SPR | L-2609-19 | 100 | S | S | S | S | S | S | N | S | No | M7 |
| 27 | 09/10/2026 | SAL-261009-027 | DTA | L-2609-19 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 09/10/2026 | ING-261009-028 | BCG | L-2609-20 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 10/10/2026 | TRA-261010-029 | NEUM | L-2609-20 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 11/10/2026 | TRA-261011-030 | SPR | L-2609-20 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 12/10/2026 | AJU-261012-031 | HEPB | L-2609-21 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 13/10/2026 | TRA-261013-032 | PENT | L-2609-21 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 13/10/2026 | SAL-261013-033 | IPV | L-2609-21 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 14/10/2026 | TRA-261014-034 | DTA | L-2609-22 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 15/10/2026 | SAL-261015-035 | INFL | L-2609-22 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 16/10/2026 | SAL-261016-036 | SPR | L-2609-22 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 17/10/2026 | SAL-261017-037 | ROTA | L-2609-23 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 17/10/2026 | ING-261017-038 | DTA | L-2609-23 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 18/10/2026 | AJU-261018-039 | INFL | L-2609-23 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 19/10/2026 | TRA-261019-040 | VARI | L-2609-24 | 60 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 29/09/2026 | BCG | 40 | 40 | 0 | GR-260929-003 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 2 | 25/09/2026 | SPR | 120 | 120 | 0 | GR-260925-074 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 3 | 12/10/2026 | ROTA | 20 | 20 | 0 | GR-261012-066 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 4 | 04/10/2026 | VARI | 80 | 80 | 0 | GR-261004-163 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 5 | 10/10/2026 | VARI | 100 | 100 | 0 | GR-261010-153 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 6 | 04/10/2026 | VARI | 150 | 150 | 0 | GR-261004-152 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 7 | 10/10/2026 | NEUM | 80 | 80 | 0 | GR-261010-060 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 8 | 16/10/2026 | ROTA | 60 | 60 | 0 | GR-261016-076 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 9 | 06/10/2026 | VARI | 200 | 200 | 0 | GR-261006-058 | Sí | Conforme. Cantidad y guía coinciden. |
| 10 | 05/10/2026 | HEPB | 80 | 80 | 0 | GR-261005-094 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 11 | 22/09/2026 | PENT | 150 | 150 | 0 | GR-260922-159 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 12 | 02/10/2026 | INFL | 60 | 60 | 0 | GR-261002-019 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 15/10/2026 | VARI | 20 | 0 | -20 | GR-261015-153 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 14 | 22/09/2026 | HEPB | 180 | 180 | 0 | GR-260922-063 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 15 | 11/10/2026 | HEPB | 40 | 40 | 0 | GR-261011-074 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 16 | 21/09/2026 | SPR | 40 | 40 | 0 | GR-260921-162 | Sí | Conforme. Cantidad y guía coinciden. |
| 17 | 17/10/2026 | PENT | 30 | 30 | 0 | GR-261017-150 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 18 | 07/10/2026 | INFL | 100 | 100 | 0 | GR-261007-014 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 19 | 15/10/2026 | HEPB | 80 | 80 | 0 | GR-261015-079 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 20 | 25/09/2026 | INFL | 60 | 60 | 0 | GR-260925-008 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 21 | 07/10/2026 | SPR | 150 | 150 | 0 | GR-261007-112 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 22 | 18/10/2026 | NEUM | 40 | 40 | 0 | GR-261018-165 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 23 | 13/10/2026 | DTA | 80 | 80 | 0 | GR-261013-113 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 24 | 16/10/2026 | NEUM | 180 | 180 | 0 | GR-261016-068 | Sí | Conforme. Cantidad y guía coinciden. |
| 25 | 28/09/2026 | PENT | 50 | 50 | 0 | GR-260928-097 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |

**Observaciones**

- Las observaciones pendientes corresponden a firmas en regularización.

---

### 2.23 · TRAB-12 · Pretest (proceso manual) · 07/09/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-12 | San Antonio de Cachi | 04/08/2026 al 06/09/2026 | Pretest | OBS-02 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 23 · **RSD = 57.50 %** · Despachos evaluados: 25 · Concordantes: 15 · **CPE = 60.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 04/08/2026 | ING-260804-001 | DTA | L-2608-04 | 30 | S | S | N | S | S | N | S | S | No | M3+M6 |
| 2 | 05/08/2026 | SAL-260805-002 | VARI | L-2608-04 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 06/08/2026 | SAL-260806-003 | ROTA | L-2608-04 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 07/08/2026 | DEV-260807-004 | HEPB | L-2608-05 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 07/08/2026 | ING-260807-005 | BCG | L-2608-05 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 08/08/2026 | ING-260808-006 | INFL | L-2608-05 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 09/08/2026 | SAL-260809-007 | BCG | L-2608-06 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 10/08/2026 | SAL-260810-008 | INFL | L-2608-06 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 11/08/2026 | SAL-260811-009 | IPV | L-2608-06 | 120 | S | S | S | N | S | N | S | S | No | M4+M6 |
| 10 | 12/08/2026 | DEV-260812-010 | IPV | L-2608-07 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 13/08/2026 | ING-260813-011 | HEPB | L-2608-07 | 200 | S | S | S | S | S | S | S | N | No | M8 |
| 12 | 14/08/2026 | SAL-260814-012 | BCG | L-2608-07 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 14/08/2026 | ING-260814-013 | IPV | L-2608-08 | 60 | S | S | S | S | S | S | S | N | No | M8 |
| 14 | 15/08/2026 | TRA-260815-014 | INFL | L-2608-08 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 16/08/2026 | ING-260816-015 | NEUM | L-2608-08 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 17/08/2026 | SAL-260817-016 | INFL | L-2608-09 | 80 | S | N | S | S | S | S | S | S | No | M2 |
| 17 | 18/08/2026 | ING-260818-017 | PENT | L-2608-09 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 19/08/2026 | TRA-260819-018 | NEUM | L-2608-09 | 80 | S | S | S | S | S | N | S | S | No | M6 |
| 19 | 20/08/2026 | DEV-260820-019 | INFL | L-2608-10 | 240 | S | S | S | S | N | S | S | S | No | M5 |
| 20 | 21/08/2026 | DEV-260821-020 | NEUM | L-2608-10 | 20 | S | S | S | S | S | N | S | S | No | M6 |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 21/08/2026 | SAL-260821-021 | BCG | L-2608-10 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 22/08/2026 | SAL-260822-022 | INFL | L-2608-11 | 60 | S | S | S | S | S | S | N | S | No | M7 |
| 23 | 23/08/2026 | AJU-260823-023 | ROTA | L-2608-11 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 24/08/2026 | DEV-260824-024 | DTA | L-2608-11 | 80 | S | S | N | S | S | S | S | S | No | M3 |
| 25 | 25/08/2026 | ING-260825-025 | BCG | L-2608-12 | 100 | S | S | S | S | S | N | S | S | No | M6 |
| 26 | 26/08/2026 | DEV-260826-026 | PENT | L-2608-12 | 80 | S | S | S | S | S | S | N | S | No | M7 |
| 27 | 27/08/2026 | SAL-260827-027 | BCG | L-2608-12 | 80 | S | S | N | S | N | S | S | S | No | M3+M5 |
| 28 | 28/08/2026 | SAL-260828-028 | BCG | L-2608-13 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 28/08/2026 | TRA-260828-029 | PENT | L-2608-13 | 60 | S | S | S | S | S | N | S | S | No | M6 |
| 30 | 29/08/2026 | ING-260829-030 | NEUM | L-2608-13 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 30/08/2026 | ING-260830-031 | VARI | L-2608-14 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 31/08/2026 | DEV-260831-032 | INFL | L-2608-14 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 01/09/2026 | ING-260901-033 | DTA | L-2608-14 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 02/09/2026 | ING-260902-034 | NEUM | L-2608-15 | 60 | S | S | S | N | S | S | S | S | No | M4 |
| 35 | 03/09/2026 | SAL-260903-035 | HEPB | L-2608-15 | 60 | S | S | S | N | S | N | S | S | No | M4+M6 |
| 36 | 04/09/2026 | AJU-260904-036 | BCG | L-2608-15 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 04/09/2026 | ING-260904-037 | HEPB | L-2608-16 | 100 | S | S | S | S | S | S | N | S | No | M7 |
| 38 | 05/09/2026 | DEV-260905-038 | DTA | L-2608-16 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 06/09/2026 | TRA-260906-039 | BCG | L-2608-16 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 07/09/2026 | TRA-260907-040 | BCG | L-2608-17 | 200 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 13/08/2026 | VARI | 60 | 60 | 0 | GR-260813-177 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 2 | 28/08/2026 | DTA | 60 | 40 | -20 | GR-260828-126 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 3 | 29/08/2026 | IPV | 40 | 40 | 0 | GR-260829-136 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 4 | 31/08/2026 | BCG | 100 | 100 | 0 | GR-260831-160 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 5 | 25/08/2026 | SPR | 100 | 95 | -5 | GR-260825-094 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 6 | 29/08/2026 | PENT | 60 | 60 | 0 | GR-260829-205 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 7 | 23/08/2026 | DTA | 180 | 175 | -5 | GR-260823-083 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 8 | 11/08/2026 | INFL | 60 | 60 | 0 | GR-260811-192 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 9 | 02/09/2026 | INFL | 180 | 175 | -5 | GR-260902-096 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 10 | 07/09/2026 | VARI | 180 | 180 | 0 | GR-260907-131 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 11 | 25/08/2026 | INFL | 30 | 30 | 0 | GR-260825-097 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 12 | 12/08/2026 | BCG | 60 | 60 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 13 | 24/08/2026 | SPR | 180 | 170 | -10 | GR-260824-126 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 14 | 30/08/2026 | HEPB | 20 | 20 | 0 | GR-260830-078 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 15 | 31/08/2026 | PENT | 180 | 180 | 0 | GR-260831-108 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 16 | 02/09/2026 | IPV | 100 | 90 | -10 | GR-260902-021 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 17 | 11/08/2026 | IPV | 50 | 50 | 0 | GR-260811-064 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 18 | 30/08/2026 | ROTA | 150 | 150 | 0 | GR-260830-124 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 19 | 04/09/2026 | SPR | 50 | 50 | 0 | GR-260904-104 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 20 | 24/08/2026 | INFL | 150 | 150 | 0 | GR-260824-090 | Sí | Conforme. Cantidad y guía coinciden. |
| 21 | 07/09/2026 | HEPB | 40 | 40 | 0 | GR-260907-081 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 22 | 22/08/2026 | IPV | 50 | 50 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 23 | 19/08/2026 | NEUM | 20 | 0 | -20 | GR-260819-122 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 24 | 22/08/2026 | IPV | 100 | 100 | 0 | GR-260822-215 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 25 | 13/08/2026 | DTA | 30 | 25 | -5 | GR-260813-107 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |

**Observaciones**

- El operador sustentó verbalmente los asientos observados; no se corrigió la hoja.

---

### 2.24 · TRAB-12 · Postest (Sistema SIVAC) · 19/10/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-12 | San Antonio de Cachi | 22/09/2026 al 18/10/2026 | Postest | OBS-02 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 37 · **RSD = 92.50 %** · Despachos evaluados: 25 · Concordantes: 23 · **CPE = 92.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 22/09/2026 | ING-260922-001 | BCG | L-2609-02 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 23/09/2026 | ING-260923-002 | BCG | L-2609-02 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 23/09/2026 | DEV-260923-003 | IPV | L-2609-02 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 24/09/2026 | TRA-260924-004 | PENT | L-2609-03 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 25/09/2026 | ING-260925-005 | ROTA | L-2609-03 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 25/09/2026 | DEV-260925-006 | INFL | L-2609-03 | 100 | S | S | S | S | S | S | S | N | No | M8 |
| 7 | 26/09/2026 | ING-260926-007 | ROTA | L-2609-04 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 27/09/2026 | AJU-260927-008 | VARI | L-2609-04 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 28/09/2026 | SAL-260928-009 | BCG | L-2609-04 | 240 | S | S | S | S | S | S | S | N | No | M8 |
| 10 | 28/09/2026 | SAL-260928-010 | BCG | L-2609-05 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 29/09/2026 | ING-260929-011 | NEUM | L-2609-05 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 30/09/2026 | ING-260930-012 | HEPB | L-2609-05 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 30/09/2026 | ING-260930-013 | NEUM | L-2609-06 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 01/10/2026 | SAL-261001-014 | IPV | L-2609-06 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 02/10/2026 | AJU-261002-015 | VARI | L-2609-06 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 02/10/2026 | TRA-261002-016 | INFL | L-2609-07 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 03/10/2026 | SAL-261003-017 | DTA | L-2609-07 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 04/10/2026 | ING-261004-018 | IPV | L-2609-07 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 04/10/2026 | ING-261004-019 | DTA | L-2609-08 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 05/10/2026 | TRA-261005-020 | SPR | L-2609-08 | 300 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 06/10/2026 | SAL-261006-021 | SPR | L-2609-08 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 07/10/2026 | DEV-261007-022 | SPR | L-2609-09 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 07/10/2026 | ING-261007-023 | NEUM | L-2609-09 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 08/10/2026 | ING-261008-024 | IPV | L-2609-09 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 09/10/2026 | DEV-261009-025 | INFL | L-2609-10 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 09/10/2026 | TRA-261009-026 | NEUM | L-2609-10 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 10/10/2026 | TRA-261010-027 | NEUM | L-2609-10 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 11/10/2026 | ING-261011-028 | VARI | L-2609-11 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 11/10/2026 | SAL-261011-029 | INFL | L-2609-11 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 12/10/2026 | SAL-261012-030 | VARI | L-2609-11 | 30 | S | N | S | S | S | S | N | S | No | M2+M7 |
| 31 | 13/10/2026 | ING-261013-031 | ROTA | L-2609-12 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 13/10/2026 | DEV-261013-032 | SPR | L-2609-12 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 14/10/2026 | TRA-261014-033 | NEUM | L-2609-12 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 15/10/2026 | ING-261015-034 | INFL | L-2609-13 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 16/10/2026 | AJU-261016-035 | HEPB | L-2609-13 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 16/10/2026 | SAL-261016-036 | INFL | L-2609-13 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 17/10/2026 | ING-261017-037 | IPV | L-2609-14 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 18/10/2026 | ING-261018-038 | HEPB | L-2609-14 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 18/10/2026 | ING-261018-039 | ROTA | L-2609-14 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 19/10/2026 | ING-261019-040 | PENT | L-2609-15 | 150 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 21/09/2026 | VARI | 180 | 180 | 0 | GR-260921-012 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 2 | 19/10/2026 | VARI | 200 | 200 | 0 | GR-261019-014 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 3 | 27/09/2026 | INFL | 80 | 75 | -5 | GR-260927-048 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 4 | 02/10/2026 | PENT | 60 | 60 | 0 | GR-261002-187 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 5 | 02/10/2026 | IPV | 50 | 50 | 0 | GR-261002-031 | Sí | Conforme. Cantidad y guía coinciden. |
| 6 | 26/09/2026 | NEUM | 200 | 200 | 0 | GR-260926-148 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 7 | 25/09/2026 | DTA | 30 | 30 | 0 | GR-260925-155 | Sí | Conforme. Cantidad y guía coinciden. |
| 8 | 28/09/2026 | HEPB | 30 | 30 | 0 | GR-260928-201 | Sí | Conforme. Cantidad y guía coinciden. |
| 9 | 29/09/2026 | BCG | 120 | 120 | 0 | GR-260929-087 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 10 | 17/10/2026 | IPV | 60 | 60 | 0 | GR-261017-126 | Sí | Conforme. Cantidad y guía coinciden. |
| 11 | 30/09/2026 | NEUM | 80 | 80 | 0 | GR-260930-137 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 12 | 13/10/2026 | NEUM | 200 | 200 | 0 | GR-261013-021 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 13 | 16/10/2026 | NEUM | 200 | 200 | 0 | GR-261016-218 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 14 | 14/10/2026 | INFL | 50 | 50 | 0 | GR-261014-213 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 15 | 08/10/2026 | BCG | 200 | 200 | 0 | GR-261008-083 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 16 | 28/09/2026 | PENT | 100 | 100 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 17 | 06/10/2026 | PENT | 200 | 200 | 0 | GR-261006-061 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 18 | 03/10/2026 | BCG | 30 | 30 | 0 | GR-261003-042 | Sí | Conforme. Cantidad y guía coinciden. |
| 19 | 01/10/2026 | PENT | 150 | 150 | 0 | GR-261001-144 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 20 | 23/09/2026 | INFL | 200 | 200 | 0 | GR-260923-111 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 21 | 17/10/2026 | INFL | 120 | 120 | 0 | GR-261017-059 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 22 | 27/09/2026 | VARI | 120 | 120 | 0 | GR-260927-212 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 23 | 17/10/2026 | NEUM | 200 | 200 | 0 | GR-261017-126 | Sí | Conforme. Cantidad y guía coinciden. |
| 24 | 23/09/2026 | NEUM | 180 | 180 | 0 | GR-260923-074 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 25 | 15/10/2026 | INFL | 20 | 20 | 0 | GR-261015-134 | Sí | Conforme. Verificado el FEFO al momento de la carga. |

**Observaciones**

- Auditoría realizada sobre el reporte de kardex emitido por el SIVAC.

---

### 2.25 · TRAB-13 · Pretest (proceso manual) · 08/09/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-13 | Turpo | 09/08/2026 al 07/09/2026 | Pretest | OBS-01 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 27 · **RSD = 67.50 %** · Despachos evaluados: 25 · Concordantes: 18 · **CPE = 72.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 09/08/2026 | TRA-260809-001 | ROTA | L-2608-03 | 150 | S | S | S | S | N | S | S | S | No | M5 |
| 2 | 10/08/2026 | DEV-260810-002 | DTA | L-2608-03 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 11/08/2026 | SAL-260811-003 | HEPB | L-2608-03 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 11/08/2026 | SAL-260811-004 | BCG | L-2608-04 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 12/08/2026 | ING-260812-005 | VARI | L-2608-04 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 13/08/2026 | DEV-260813-006 | BCG | L-2608-04 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 14/08/2026 | SAL-260814-007 | VARI | L-2608-05 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 14/08/2026 | SAL-260814-008 | DTA | L-2608-05 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 15/08/2026 | DEV-260815-009 | HEPB | L-2608-05 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 16/08/2026 | ING-260816-010 | SPR | L-2608-06 | 40 | S | S | S | S | S | S | N | S | No | M7 |
| 11 | 17/08/2026 | SAL-260817-011 | PENT | L-2608-06 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 17/08/2026 | ING-260817-012 | BCG | L-2608-06 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 18/08/2026 | DEV-260818-013 | PENT | L-2608-07 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 19/08/2026 | SAL-260819-014 | INFL | L-2608-07 | 20 | S | N | S | S | S | S | S | S | No | M2 |
| 15 | 20/08/2026 | SAL-260820-015 | PENT | L-2608-07 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 21/08/2026 | SAL-260821-016 | DTA | L-2608-08 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 21/08/2026 | ING-260821-017 | NEUM | L-2608-08 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 22/08/2026 | ING-260822-018 | BCG | L-2608-08 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 23/08/2026 | ING-260823-019 | VARI | L-2608-09 | 180 | S | S | S | S | S | N | S | S | No | M6 |
| 20 | 24/08/2026 | TRA-260824-020 | INFL | L-2608-09 | 300 | S | S | S | S | S | N | S | S | No | M6 |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 24/08/2026 | ING-260824-021 | INFL | L-2608-09 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 25/08/2026 | TRA-260825-022 | INFL | L-2608-10 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 26/08/2026 | SAL-260826-023 | NEUM | L-2608-10 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 27/08/2026 | AJU-260827-024 | VARI | L-2608-10 | 100 | S | S | S | S | S | S | N | S | No | M7 |
| 25 | 27/08/2026 | DEV-260827-025 | VARI | L-2608-11 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 28/08/2026 | SAL-260828-026 | VARI | L-2608-11 | 180 | S | N | S | S | S | S | S | S | No | M2 |
| 27 | 29/08/2026 | ING-260829-027 | VARI | L-2608-11 | 100 | N | S | S | S | S | S | S | N | No | M1+M8 |
| 28 | 30/08/2026 | ING-260830-028 | NEUM | L-2608-12 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 31/08/2026 | ING-260831-029 | BCG | L-2608-12 | 180 | S | S | S | S | S | N | S | S | No | M6 |
| 30 | 31/08/2026 | DEV-260831-030 | ROTA | L-2608-12 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 01/09/2026 | ING-260901-031 | PENT | L-2608-13 | 120 | S | N | S | S | S | S | S | S | No | M2 |
| 32 | 02/09/2026 | SAL-260902-032 | INFL | L-2608-13 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 03/09/2026 | ING-260903-033 | ROTA | L-2608-13 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 03/09/2026 | ING-260903-034 | VARI | L-2608-14 | 180 | S | N | S | S | S | S | N | S | No | M2+M7 |
| 35 | 04/09/2026 | AJU-260904-035 | SPR | L-2608-14 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 05/09/2026 | ING-260905-036 | SPR | L-2608-14 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 06/09/2026 | AJU-260906-037 | INFL | L-2608-15 | 20 | S | S | S | S | N | S | S | S | No | M5 |
| 38 | 06/09/2026 | SAL-260906-038 | ROTA | L-2608-15 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 07/09/2026 | AJU-260907-039 | NEUM | L-2608-15 | 30 | S | S | S | S | N | S | N | S | No | M5+M7 |
| 40 | 08/09/2026 | SAL-260908-040 | SPR | L-2608-16 | 150 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 01/09/2026 | HEPB | 120 | 120 | 0 | GR-260901-081 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 2 | 12/08/2026 | NEUM | 80 | 80 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 3 | 24/08/2026 | DTA | 120 | 110 | -10 | GR-260824-112 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 4 | 12/08/2026 | IPV | 60 | 60 | 0 | GR-260812-193 | Sí | Conforme. Cantidad y guía coinciden. |
| 5 | 26/08/2026 | IPV | 100 | 100 | 0 | GR-260826-195 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 6 | 08/09/2026 | SPR | 200 | 200 | 0 | GR-260908-024 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 7 | 12/08/2026 | BCG | 200 | 205 | +5 | GR-260812-203 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 8 | 29/08/2026 | DTA | 150 | 150 | 0 | GR-260829-055 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 9 | 31/08/2026 | DTA | 200 | 200 | 0 | GR-260831-130 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 10 | 07/09/2026 | DTA | 100 | 100 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 11 | 30/08/2026 | VARI | 150 | 150 | 0 | GR-260830-071 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 12 | 12/08/2026 | PENT | 150 | 150 | 0 | GR-260812-089 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 24/08/2026 | VARI | 180 | 180 | 0 | GR-260824-025 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 14 | 25/08/2026 | VARI | 50 | 45 | -5 | GR-260825-072 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 15 | 14/08/2026 | PENT | 50 | 40 | -10 | GR-260814-068 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 16 | 21/08/2026 | BCG | 50 | 50 | 0 | GR-260821-204 | Sí | Conforme. Cantidad y guía coinciden. |
| 17 | 03/09/2026 | DTA | 100 | 100 | 0 | GR-260903-139 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 18 | 07/09/2026 | SPR | 200 | 200 | 0 | GR-260907-110 | Sí | Conforme. Cantidad y guía coinciden. |
| 19 | 20/08/2026 | BCG | 200 | 200 | 0 | GR-260820-154 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 20 | 30/08/2026 | INFL | 100 | 100 | 0 | GR-260830-019 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 21 | 04/09/2026 | SPR | 80 | 70 | -10 | GR-260904-027 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 22 | 03/09/2026 | BCG | 80 | 80 | 0 | GR-260903-025 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 23 | 23/08/2026 | IPV | 40 | 40 | 0 | GR-260823-200 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 24 | 13/08/2026 | ROTA | 100 | 100 | 0 | GR-260813-098 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 25 | 14/08/2026 | BCG | 200 | 200 | 0 | GR-260814-124 | Sí | Conforme. Verificado el FEFO al momento de la carga. |

**Observaciones**

- Se solicitó el libro de actas para validar las devoluciones del periodo.

---

### 2.26 · TRAB-13 · Postest (Sistema SIVAC) · 20/10/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-13 | Turpo | 18/09/2026 al 19/10/2026 | Postest | OBS-01 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 39 · **RSD = 97.50 %** · Despachos evaluados: 25 · Concordantes: 24 · **CPE = 96.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 18/09/2026 | DEV-260918-001 | VARI | L-2609-13 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 19/09/2026 | ING-260919-002 | INFL | L-2609-13 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 20/09/2026 | SAL-260920-003 | NEUM | L-2609-13 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 20/09/2026 | ING-260920-004 | ROTA | L-2609-14 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 21/09/2026 | ING-260921-005 | IPV | L-2609-14 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 22/09/2026 | SAL-260922-006 | PENT | L-2609-14 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 23/09/2026 | SAL-260923-007 | NEUM | L-2609-15 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 24/09/2026 | SAL-260924-008 | INFL | L-2609-15 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 25/09/2026 | ING-260925-009 | HEPB | L-2609-15 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 25/09/2026 | SAL-260925-010 | NEUM | L-2609-16 | 100 | S | S | N | S | S | S | S | N | No | M3+M8 |
| 11 | 26/09/2026 | SAL-260926-011 | ROTA | L-2609-16 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 27/09/2026 | DEV-260927-012 | INFL | L-2609-16 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 28/09/2026 | ING-260928-013 | SPR | L-2609-17 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 29/09/2026 | SAL-260929-014 | INFL | L-2609-17 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 15 | 29/09/2026 | SAL-260929-015 | DTA | L-2609-17 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 30/09/2026 | SAL-260930-016 | DTA | L-2609-18 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 01/10/2026 | AJU-261001-017 | PENT | L-2609-18 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 02/10/2026 | ING-261002-018 | INFL | L-2609-18 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 03/10/2026 | SAL-261003-019 | DTA | L-2609-19 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 04/10/2026 | SAL-261004-020 | IPV | L-2609-19 | 240 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 04/10/2026 | ING-261004-021 | SPR | L-2609-19 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 05/10/2026 | DEV-261005-022 | DTA | L-2609-20 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 06/10/2026 | ING-261006-023 | ROTA | L-2609-20 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 07/10/2026 | DEV-261007-024 | DTA | L-2609-20 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 08/10/2026 | AJU-261008-025 | ROTA | L-2609-21 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 09/10/2026 | SAL-261009-026 | SPR | L-2609-21 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 09/10/2026 | SAL-261009-027 | VARI | L-2609-21 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 10/10/2026 | TRA-261010-028 | HEPB | L-2609-22 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 11/10/2026 | ING-261011-029 | PENT | L-2609-22 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 12/10/2026 | AJU-261012-030 | ROTA | L-2609-22 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 13/10/2026 | DEV-261013-031 | NEUM | L-2609-23 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 13/10/2026 | SAL-261013-032 | SPR | L-2609-23 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 14/10/2026 | SAL-261014-033 | PENT | L-2609-23 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 15/10/2026 | ING-261015-034 | IPV | L-2609-24 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 16/10/2026 | SAL-261016-035 | DTA | L-2609-24 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 17/10/2026 | ING-261017-036 | NEUM | L-2609-24 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 18/10/2026 | ING-261018-037 | IPV | L-2609-25 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 18/10/2026 | SAL-261018-038 | BCG | L-2609-25 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 19/10/2026 | ING-261019-039 | HEPB | L-2609-25 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 20/10/2026 | TRA-261020-040 | PENT | L-2609-26 | 120 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 27/09/2026 | ROTA | 30 | 30 | 0 | GR-260927-007 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 2 | 06/10/2026 | SPR | 50 | 50 | 0 | GR-261006-021 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 3 | 06/10/2026 | HEPB | 180 | 180 | 0 | GR-261006-019 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 4 | 27/09/2026 | VARI | 20 | 20 | 0 | GR-260927-088 | Sí | Conforme. Cantidad y guía coinciden. |
| 5 | 22/09/2026 | IPV | 40 | 40 | 0 | GR-260922-126 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 6 | 25/09/2026 | INFL | 120 | 120 | 0 | GR-260925-146 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 7 | 05/10/2026 | IPV | 30 | 30 | 0 | GR-261005-140 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 8 | 13/10/2026 | BCG | 40 | 40 | 0 | GR-261013-203 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 9 | 20/10/2026 | IPV | 180 | 180 | 0 | GR-261020-028 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 10 | 13/10/2026 | PENT | 20 | 20 | 0 | GR-261013-045 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 11 | 07/10/2026 | BCG | 180 | 180 | 0 | GR-261007-007 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 12 | 26/09/2026 | VARI | 180 | 180 | 0 | GR-260926-201 | Sí | Conforme. Cantidad y guía coinciden. |
| 13 | 19/10/2026 | DTA | 100 | 100 | 0 | GR-261019-173 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 14 | 20/10/2026 | IPV | 80 | 80 | 0 | GR-261020-079 | Sí | Conforme. Cantidad y guía coinciden. |
| 15 | 14/10/2026 | IPV | 120 | 120 | 0 | GR-261014-175 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 16 | 22/09/2026 | VARI | 200 | 200 | 0 | GR-260922-189 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 17 | 17/10/2026 | INFL | 80 | 80 | 0 | GR-261017-051 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 18 | 28/09/2026 | SPR | 30 | 30 | 0 | GR-260928-207 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 19 | 27/09/2026 | SPR | 120 | 120 | 0 | GR-260927-159 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 20 | 09/10/2026 | SPR | 30 | 30 | 0 | GR-261009-020 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 21 | 06/10/2026 | PENT | 80 | 80 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 22 | 07/10/2026 | INFL | 60 | 60 | 0 | GR-261007-040 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 23 | 15/10/2026 | PENT | 20 | 20 | 0 | GR-261015-168 | Sí | Conforme. Cantidad y guía coinciden. |
| 24 | 26/09/2026 | DTA | 30 | 30 | 0 | GR-260926-065 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 25 | 16/10/2026 | BCG | 150 | 150 | 0 | GR-261016-067 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |

**Observaciones**

- Auditoría realizada sobre el reporte de kardex emitido por el SIVAC.

---

### 2.27 · TRAB-14 · Pretest (proceso manual) · 08/09/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-14 | Kishuara | 06/08/2026 al 07/09/2026 | Pretest | OBS-02 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 26 · **RSD = 65.00 %** · Despachos evaluados: 25 · Concordantes: 17 · **CPE = 68.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 06/08/2026 | AJU-260806-001 | HEPB | L-2608-03 | 120 | S | S | S | S | S | N | S | S | No | M6 |
| 2 | 07/08/2026 | AJU-260807-002 | DTA | L-2608-03 | 40 | S | S | N | S | S | S | S | S | No | M3 |
| 3 | 08/08/2026 | DEV-260808-003 | VARI | L-2608-03 | 50 | S | S | S | N | S | S | S | S | No | M4 |
| 4 | 09/08/2026 | SAL-260809-004 | PENT | L-2608-04 | 60 | S | N | S | S | S | S | S | N | No | M2+M8 |
| 5 | 09/08/2026 | SAL-260809-005 | DTA | L-2608-04 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 10/08/2026 | AJU-260810-006 | DTA | L-2608-04 | 20 | S | S | S | S | S | N | S | S | No | M6 |
| 7 | 11/08/2026 | ING-260811-007 | VARI | L-2608-05 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 12/08/2026 | ING-260812-008 | HEPB | L-2608-05 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 13/08/2026 | SAL-260813-009 | SPR | L-2608-05 | 60 | S | S | S | S | S | S | S | N | No | M8 |
| 10 | 14/08/2026 | SAL-260814-010 | ROTA | L-2608-06 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 14/08/2026 | ING-260814-011 | ROTA | L-2608-06 | 30 | S | S | S | S | S | S | N | S | No | M7 |
| 12 | 15/08/2026 | SAL-260815-012 | BCG | L-2608-06 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 16/08/2026 | ING-260816-013 | PENT | L-2608-07 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 17/08/2026 | ING-260817-014 | SPR | L-2608-07 | 50 | S | S | S | S | S | N | S | S | No | M6 |
| 15 | 18/08/2026 | AJU-260818-015 | IPV | L-2608-07 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 19/08/2026 | SAL-260819-016 | BCG | L-2608-08 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 20/08/2026 | SAL-260820-017 | INFL | L-2608-08 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 20/08/2026 | SAL-260820-018 | ROTA | L-2608-08 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 21/08/2026 | TRA-260821-019 | PENT | L-2608-09 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 22/08/2026 | ING-260822-020 | SPR | L-2608-09 | 100 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 23/08/2026 | TRA-260823-021 | PENT | L-2608-09 | 120 | S | S | S | S | S | N | S | S | No | M6 |
| 22 | 24/08/2026 | SAL-260824-022 | NEUM | L-2608-10 | 150 | S | S | S | S | N | S | N | S | No | M5+M7 |
| 23 | 25/08/2026 | AJU-260825-023 | SPR | L-2608-10 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 25/08/2026 | SAL-260825-024 | IPV | L-2608-10 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 26/08/2026 | ING-260826-025 | PENT | L-2608-11 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 27/08/2026 | ING-260827-026 | DTA | L-2608-11 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 28/08/2026 | ING-260828-027 | NEUM | L-2608-11 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 29/08/2026 | ING-260829-028 | SPR | L-2608-12 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 30/08/2026 | ING-260830-029 | BCG | L-2608-12 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 31/08/2026 | SAL-260831-030 | PENT | L-2608-12 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 31/08/2026 | ING-260831-031 | PENT | L-2608-13 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 01/09/2026 | AJU-260901-032 | HEPB | L-2608-13 | 180 | S | S | N | S | S | S | N | S | No | M3+M7 |
| 33 | 02/09/2026 | SAL-260902-033 | IPV | L-2608-13 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 03/09/2026 | ING-260903-034 | IPV | L-2608-14 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 04/09/2026 | TRA-260904-035 | PENT | L-2608-14 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 05/09/2026 | SAL-260905-036 | INFL | L-2608-14 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 05/09/2026 | TRA-260905-037 | NEUM | L-2608-15 | 120 | S | S | S | S | S | S | S | N | No | M8 |
| 38 | 06/09/2026 | SAL-260906-038 | BCG | L-2608-15 | 150 | S | N | S | S | S | S | S | S | No | M2 |
| 39 | 07/09/2026 | SAL-260907-039 | HEPB | L-2608-15 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 08/09/2026 | ING-260908-040 | NEUM | L-2608-16 | 150 | S | S | S | S | N | S | S | S | No | M5 |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 17/08/2026 | ROTA | 100 | 100 | 0 | GR-260817-212 | Sí | Conforme. Cantidad y guía coinciden. |
| 2 | 29/08/2026 | IPV | 20 | 0 | -20 | GR-260829-037 | No | Entrega menor a la programada; se regulariza en el siguiente despacho. |
| 3 | 19/08/2026 | ROTA | 40 | 40 | 0 | GR-260819-007 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 4 | 14/08/2026 | DTA | 100 | 100 | 0 | GR-260814-098 | Sí | Conforme. Cantidad y guía coinciden. |
| 5 | 21/08/2026 | SPR | 100 | 100 | 0 | GR-260821-133 | Sí | Conforme. Cantidad y guía coinciden. |
| 6 | 29/08/2026 | BCG | 30 | 30 | 0 | GR-260829-198 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 7 | 15/08/2026 | PENT | 150 | 150 | 0 | GR-260815-029 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 8 | 08/09/2026 | PENT | 20 | 20 | 0 | GR-260908-131 | Sí | Conforme. Cantidad y guía coinciden. |
| 9 | 08/09/2026 | VARI | 60 | 60 | 0 | GR-260908-078 | Sí | Conforme. Cantidad y guía coinciden. |
| 10 | 15/08/2026 | INFL | 50 | 50 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 11 | 28/08/2026 | DTA | 30 | 30 | 0 | GR-260828-211 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 12 | 19/08/2026 | ROTA | 150 | 150 | 0 | GR-260819-028 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 13 | 29/08/2026 | INFL | 80 | 80 | 0 | GR-260829-097 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 14 | 23/08/2026 | BCG | 120 | 120 | 0 | GR-260823-148 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 15 | 07/09/2026 | PENT | 50 | 50 | 0 | GR-260907-196 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 16 | 02/09/2026 | PENT | 80 | 80 | 0 | Sin guía | No | Despacho sin documento de sustento al momento de la auditoría. |
| 17 | 24/08/2026 | NEUM | 200 | 200 | 0 | GR-260824-017 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 18 | 17/08/2026 | ROTA | 120 | 125 | +5 | GR-260817-060 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |
| 19 | 17/08/2026 | SPR | 30 | 30 | 0 | GR-260817-053 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 20 | 03/09/2026 | BCG | 50 | 40 | -10 | GR-260903-174 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 21 | 14/08/2026 | PENT | 180 | 175 | -5 | GR-260814-026 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 22 | 20/08/2026 | BCG | 50 | 50 | 0 | GR-260820-058 | Sí | Conforme. Cantidad y guía coinciden. |
| 23 | 03/09/2026 | NEUM | 200 | 190 | -10 | GR-260903-036 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 24 | 17/08/2026 | ROTA | 80 | 80 | 0 | GR-260817-218 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 25 | 18/08/2026 | PENT | 50 | 60 | +10 | GR-260818-116 | No | Entrega mayor a la programada; se ajusta el saldo del almacén. |

**Observaciones**

- Se solicitó el libro de actas para validar las devoluciones del periodo.

---

### 2.28 · TRAB-14 · Postest (Sistema SIVAC) · 20/10/2026

| Operador (OP) | Centro de acopio | Periodo auditado | Momento | Auditor |
| --- | --- | :---: | :---: | :---: |
| TRAB-14 | Kishuara | 25/09/2026 al 19/10/2026 | Postest | OBS-02 |

**Cierre del bloque.** Asientos revisados: 40 · Conformes: 39 · **RSD = 97.50 %** · Despachos evaluados: 25 · Concordantes: 24 · **CPE = 96.00 %**

**Hoja 1 de 2 (bloque A) — asientos 1 a 20**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 25/09/2026 | ING-260925-001 | SPR | L-2609-10 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 2 | 26/09/2026 | SAL-260926-002 | VARI | L-2609-10 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 3 | 26/09/2026 | TRA-260926-003 | INFL | L-2609-10 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 4 | 27/09/2026 | ING-260927-004 | DTA | L-2609-11 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 5 | 28/09/2026 | TRA-260928-005 | VARI | L-2609-11 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 6 | 28/09/2026 | TRA-260928-006 | HEPB | L-2609-11 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 7 | 29/09/2026 | SAL-260929-007 | ROTA | L-2609-12 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 8 | 29/09/2026 | AJU-260929-008 | IPV | L-2609-12 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 9 | 30/09/2026 | ING-260930-009 | IPV | L-2609-12 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 10 | 01/10/2026 | TRA-261001-010 | NEUM | L-2609-13 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 11 | 01/10/2026 | ING-261001-011 | ROTA | L-2609-13 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 12 | 02/10/2026 | TRA-261002-012 | IPV | L-2609-13 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 13 | 03/10/2026 | SAL-261003-013 | SPR | L-2609-14 | 200 | S | S | S | S | S | S | S | S | Sí | — |
| 14 | 03/10/2026 | ING-261003-014 | IPV | L-2609-14 | 200 | S | S | N | S | S | S | S | N | No | M3+M8 |
| 15 | 04/10/2026 | ING-261004-015 | PENT | L-2609-14 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 16 | 05/10/2026 | ING-261005-016 | IPV | L-2609-15 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 17 | 05/10/2026 | TRA-261005-017 | PENT | L-2609-15 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 18 | 06/10/2026 | AJU-261006-018 | INFL | L-2609-15 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 19 | 07/10/2026 | ING-261007-019 | INFL | L-2609-16 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 20 | 07/10/2026 | SAL-261007-020 | HEPB | L-2609-16 | 60 | S | S | S | S | S | S | S | S | Sí | — |

**Hoja 2 de 2 (bloque A) — asientos 21 a 40**

| N.° | Fecha | Documento | Biológico | Lote | Cant. | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Conf. | Motivo |
| :---: | :---: | --- | :---: | :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 21 | 08/10/2026 | ING-261008-021 | SPR | L-2609-16 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 22 | 08/10/2026 | SAL-261008-022 | NEUM | L-2609-17 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 23 | 09/10/2026 | DEV-261009-023 | VARI | L-2609-17 | 180 | S | S | S | S | S | S | S | S | Sí | — |
| 24 | 10/10/2026 | SAL-261010-024 | NEUM | L-2609-17 | 60 | S | S | S | S | S | S | S | S | Sí | — |
| 25 | 10/10/2026 | SAL-261010-025 | DTA | L-2609-18 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 26 | 11/10/2026 | SAL-261011-026 | HEPB | L-2609-18 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 27 | 12/10/2026 | TRA-261012-027 | INFL | L-2609-18 | 30 | S | S | S | S | S | S | S | S | Sí | — |
| 28 | 12/10/2026 | SAL-261012-028 | DTA | L-2609-19 | 300 | S | S | S | S | S | S | S | S | Sí | — |
| 29 | 13/10/2026 | DEV-261013-029 | NEUM | L-2609-19 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 30 | 14/10/2026 | SAL-261014-030 | PENT | L-2609-19 | 50 | S | S | S | S | S | S | S | S | Sí | — |
| 31 | 14/10/2026 | TRA-261014-031 | HEPB | L-2609-20 | 150 | S | S | S | S | S | S | S | S | Sí | — |
| 32 | 15/10/2026 | DEV-261015-032 | IPV | L-2609-20 | 120 | S | S | S | S | S | S | S | S | Sí | — |
| 33 | 16/10/2026 | ING-261016-033 | SPR | L-2609-20 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 34 | 16/10/2026 | DEV-261016-034 | ROTA | L-2609-21 | 20 | S | S | S | S | S | S | S | S | Sí | — |
| 35 | 17/10/2026 | ING-261017-035 | IPV | L-2609-21 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 36 | 17/10/2026 | ING-261017-036 | INFL | L-2609-21 | 40 | S | S | S | S | S | S | S | S | Sí | — |
| 37 | 18/10/2026 | ING-261018-037 | SPR | L-2609-22 | 80 | S | S | S | S | S | S | S | S | Sí | — |
| 38 | 19/10/2026 | ING-261019-038 | ROTA | L-2609-22 | 240 | S | S | S | S | S | S | S | S | Sí | — |
| 39 | 19/10/2026 | ING-261019-039 | VARI | L-2609-22 | 100 | S | S | S | S | S | S | S | S | Sí | — |
| 40 | 20/10/2026 | ING-261020-040 | ROTA | L-2609-23 | 20 | S | S | S | S | S | S | S | S | Sí | — |

**Bloque B — despachos conciliados**

| N.° | Fecha | Biológico | Programado | Entregado | Diferencia | Documento | Conf. | Obs. |
| :---: | :---: | :---: | ---: | ---: | ---: | --- | :---: | --- |
| 1 | 01/10/2026 | INFL | 80 | 80 | 0 | GR-261001-195 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 2 | 03/10/2026 | BCG | 60 | 60 | 0 | GR-261003-156 | Sí | Conforme. Cantidad y guía coinciden. |
| 3 | 16/10/2026 | BCG | 120 | 120 | 0 | GR-261016-145 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 4 | 29/09/2026 | BCG | 180 | 180 | 0 | GR-260929-198 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 5 | 24/09/2026 | DTA | 180 | 180 | 0 | GR-260924-008 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 6 | 06/10/2026 | DTA | 50 | 50 | 0 | GR-261006-046 | Sí | Conforme. Cantidad y guía coinciden. |
| 7 | 18/10/2026 | SPR | 30 | 25 | -5 | GR-261018-155 | No | Guía de remisión no coincide con la cantidad registrada en el kardex. |
| 8 | 10/10/2026 | NEUM | 150 | 150 | 0 | GR-261010-152 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 9 | 11/10/2026 | PENT | 50 | 50 | 0 | GR-261011-183 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 10 | 07/10/2026 | PENT | 150 | 150 | 0 | GR-261007-182 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 11 | 24/09/2026 | INFL | 200 | 200 | 0 | GR-260924-058 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 12 | 07/10/2026 | ROTA | 100 | 100 | 0 | GR-261007-001 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 13 | 01/10/2026 | ROTA | 20 | 20 | 0 | GR-261001-067 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 14 | 23/09/2026 | INFL | 30 | 30 | 0 | GR-260923-085 | Sí | Conforme. Cantidad y guía coinciden. |
| 15 | 11/10/2026 | SPR | 30 | 30 | 0 | GR-261011-198 | Sí | Conforme. Se adjuntó guía de remisión y acta de entrega. |
| 16 | 17/10/2026 | INFL | 120 | 120 | 0 | GR-261017-043 | Sí | Conforme. Cantidad y guía coinciden. |
| 17 | 14/10/2026 | HEPB | 60 | 60 | 0 | GR-261014-175 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 18 | 06/10/2026 | VARI | 80 | 80 | 0 | GR-261006-029 | Sí | Conforme. Despacho parcial autorizado y regularizado el mismo día. |
| 19 | 26/09/2026 | ROTA | 200 | 200 | 0 | GR-260926-134 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 20 | 03/10/2026 | IPV | 180 | 180 | 0 | GR-261003-134 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 21 | 10/10/2026 | HEPB | 180 | 180 | 0 | GR-261010-163 | Sí | Conforme. Cantidad y guía coinciden. |
| 22 | 22/09/2026 | ROTA | 50 | 50 | 0 | GR-260922-046 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |
| 23 | 23/09/2026 | PENT | 40 | 40 | 0 | GR-260923-134 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 24 | 15/10/2026 | SPR | 80 | 80 | 0 | GR-261015-202 | Sí | Conforme. Verificado el FEFO al momento de la carga. |
| 25 | 28/09/2026 | SPR | 120 | 120 | 0 | GR-260928-044 | Sí | Conforme. Recepción firmada por el jefe del establecimiento. |

**Observaciones**

- Los asientos se contrastaron con la trazabilidad de movimientos del sistema.

---

### 2.29 · Matriz consolidada de consistencia documental

| Operador | Centro de acopio | Conformes pre | RSD pre (%) | Conformes post | RSD post (%) | Conc. pre | CPE pre (%) | Conc. post | CPE post (%) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TRAB-01 | ALMACÉN (CHANKA) | 25 | 62.50 | 38 | 95.00 | 16 | 64.00 | 24 | 96.00 |
| TRAB-02 | ALMACÉN (CHANKA) | 23 | 57.50 | 38 | 95.00 | 16 | 64.00 | 23 | 92.00 |
| TRAB-03 | Hospital Andahuaylas | 26 | 65.00 | 39 | 97.50 | 18 | 72.00 | 24 | 96.00 |
| TRAB-04 | Hospital ESSALUD Andahuaylas | 29 | 72.50 | 39 | 97.50 | 19 | 76.00 | 25 | 100.00 |
| TRAB-05 | Centro de Salud Andahuaylas | 22 | 55.00 | 37 | 92.50 | 15 | 60.00 | 23 | 92.00 |
| TRAB-06 | Talavera | 26 | 65.00 | 39 | 97.50 | 17 | 68.00 | 24 | 96.00 |
| TRAB-07 | San Jeronimo | 21 | 52.50 | 37 | 92.50 | 14 | 56.00 | 23 | 92.00 |
| TRAB-08 | Huancaray | 30 | 75.00 | 40 | 100.00 | 20 | 80.00 | 25 | 100.00 |
| TRAB-09 | Chicmo | 29 | 72.50 | 39 | 97.50 | 19 | 76.00 | 24 | 96.00 |
| TRAB-10 | Huancabamba | 24 | 60.00 | 38 | 95.00 | 16 | 64.00 | 24 | 96.00 |
| TRAB-11 | Pampachiri | 25 | 62.50 | 38 | 95.00 | 17 | 68.00 | 24 | 96.00 |
| TRAB-12 | San Antonio de Cachi | 23 | 57.50 | 37 | 92.50 | 15 | 60.00 | 23 | 92.00 |
| TRAB-13 | Turpo | 27 | 67.50 | 39 | 97.50 | 18 | 72.00 | 24 | 96.00 |
| TRAB-14 | Kishuara | 26 | 65.00 | 39 | 97.50 | 17 | 68.00 | 24 | 96.00 |

*Nota.* RSD = asientos conformes ÷ 40 × 100; CPE = despachos concordantes ÷ 25 × 100. El detalle asiento por asiento consta en los bloques 2.1 a 2.28 y en `instrumento02_asientos.csv` / `instrumento02_despachos.csv`.

<a id="s3"></a>
## Sección 3. Instrumento N.° 03 — Cuestionario de satisfacción del usuario (TAM)

Escala Likert de cinco puntos: 1 muy en desacuerdo, 2 en desacuerdo, 3 indiferente, 4 de acuerdo, 5 totalmente de acuerdo. La aceptación del proceso (AP) suma los reactivos AP-01 a AP-04 y la utilidad percibida (UP) suma UP-01 a UP-04; el puntaje global es AP + UP (8 a 40). El baremo del codebook clasifica Bajo (8-18), Medio (19-29) y Alto (30-40).

### 3.1 · TRAB-01 · Pretest · 10/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-01 | ALMACÉN (CHANKA) | 10/08/2026 | Pretest | OBS-01 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | X | · | · | · | 2 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | X | · | · | · | 2 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | X | · | · | · | 2 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | X | · | · | · | 2 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | X | · | · | · | 2 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | X | · | · | 3 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | X | · | · | · | 2 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | X | · | · | · | 2 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 8 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 9 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **17** | 8-40 |

**Nivel de satisfacción:** Bajo · **Observación:** Cuestionario aplicado en el almacén, antes de la capacitación en el SIVAC.

---

### 3.2 · TRAB-01 · Postest · 12/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-01 | ALMACÉN (CHANKA) | 12/10/2026 | Postest | OBS-01 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | · | X | · | 4 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | · | · | · | X | 5 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | · | X | · | 4 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | · | · | X | 5 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | · | · | X | 5 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | · | · | X | 5 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | · | · | X | · | 4 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | · | · | X | 5 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 18 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 19 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **37** | 8-40 |

**Nivel de satisfacción:** Alto · **Observación:** Cuestionario aplicado tras cuatro semanas de uso continuo del SIVAC.

---

### 3.3 · TRAB-02 · Pretest · 10/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-02 | ALMACÉN (CHANKA) | 10/08/2026 | Pretest | OBS-02 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | X | · | · | · | · | 1 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | X | · | · | · | 2 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | X | · | · | · | · | 1 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | X | · | · | · | 2 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | X | · | · | · | 2 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | X | · | · | · | 2 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | X | · | · | · | 2 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | X | · | · | · | 2 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 6 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 8 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **14** | 8-40 |

**Nivel de satisfacción:** Bajo · **Observación:** El operador solicitó releer dos reactivos; se aclaró sin inducir la respuesta.

---

### 3.4 · TRAB-02 · Postest · 12/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-02 | ALMACÉN (CHANKA) | 12/10/2026 | Postest | OBS-02 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | · | X | · | 4 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | · | · | X | · | 4 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | · | X | · | 4 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | · | X | · | 4 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | · | · | X | 5 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | · | X | · | 4 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | · | · | X | · | 4 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | · | · | X | 5 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 16 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 18 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **34** | 8-40 |

**Nivel de satisfacción:** Alto · **Observación:** El operador respondió sin consultar el sistema; se garantizó el anonimato.

---

### 3.5 · TRAB-03 · Pretest · 11/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-03 | Hospital Andahuaylas | 11/08/2026 | Pretest | OBS-01 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | X | · | · | · | 2 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | X | · | · | · | 2 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | X | · | · | 3 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | X | · | · | · | 2 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | X | · | · | 3 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | X | · | · | · | 2 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | X | · | · | · | 2 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | X | · | · | 3 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 9 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 10 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **19** | 8-40 |

**Nivel de satisfacción:** Medio · **Observación:** Aplicado al término de la jornada, sin presencia de terceros.

---

### 3.6 · TRAB-03 · Postest · 13/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-03 | Hospital Andahuaylas | 13/10/2026 | Postest | OBS-01 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | · | · | X | 5 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | · | · | · | X | 5 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | · | · | X | 5 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | · | X | · | 4 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | · | · | X | 5 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | · | · | X | 5 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | · | · | · | X | 5 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | · | · | X | 5 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 19 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 20 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **39** | 8-40 |

**Nivel de satisfacción:** Alto · **Observación:** Aplicado al cierre del periodo auditado, en presencia del auditor de campo.

---

### 3.7 · TRAB-04 · Pretest · 11/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-04 | Hospital ESSALUD Andahuaylas | 11/08/2026 | Pretest | OBS-02 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | X | · | · | 3 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | · | X | · | · | 3 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | X | · | · | · | 2 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | X | · | · | 3 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | X | · | · | 3 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | X | · | · | 3 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | · | X | · | · | 3 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | X | · | · | 3 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 11 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 12 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **23** | 8-40 |

**Nivel de satisfacción:** Medio · **Observación:** Se explicó la escala Likert antes de iniciar; no hubo ítems en blanco.

---

### 3.8 · TRAB-04 · Postest · 13/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-04 | Hospital ESSALUD Andahuaylas | 13/10/2026 | Postest | OBS-02 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | · | · | X | 5 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | · | · | · | X | 5 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | · | · | X | 5 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | · | · | X | 5 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | · | · | X | 5 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | · | · | X | 5 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | · | · | · | X | 5 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | · | · | X | 5 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 20 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 20 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **40** | 8-40 |

**Nivel de satisfacción:** Alto · **Observación:** Se registraron comentarios adicionales favorables sobre el control FEFO.

---

### 3.9 · TRAB-05 · Pretest · 12/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-05 | Centro de Salud Andahuaylas | 12/08/2026 | Pretest | OBS-01 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | X | · | · | · | 2 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | X | · | · | · | · | 1 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | X | · | · | · | 2 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | X | · | · | · | · | 1 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | X | · | · | · | 2 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | X | · | · | · | 2 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | X | · | · | · | 2 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | X | · | · | · | 2 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 6 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 8 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **14** | 8-40 |

**Nivel de satisfacción:** Bajo · **Observación:** Cuestionario aplicado en el almacén, antes de la capacitación en el SIVAC.

---

### 3.10 · TRAB-05 · Postest · 14/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-05 | Centro de Salud Andahuaylas | 14/10/2026 | Postest | OBS-01 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | · | X | · | 4 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | · | · | X | · | 4 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | · | X | · | 4 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | · | X | · | 4 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | · | X | · | 4 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | · | X | · | 4 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | · | · | X | · | 4 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | · | X | · | 4 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 16 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 16 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **32** | 8-40 |

**Nivel de satisfacción:** Alto · **Observación:** Cuestionario aplicado tras cuatro semanas de uso continuo del SIVAC.

---

### 3.11 · TRAB-06 · Pretest · 12/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-06 | Talavera | 12/08/2026 | Pretest | OBS-02 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | X | · | · | · | 2 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | X | · | · | · | 2 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | X | · | · | · | 2 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | X | · | · | · | 2 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | X | · | · | · | 2 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | X | · | · | · | 2 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | X | · | · | · | 2 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | X | · | · | · | 2 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 8 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 8 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **16** | 8-40 |

**Nivel de satisfacción:** Bajo · **Observación:** El operador solicitó releer dos reactivos; se aclaró sin inducir la respuesta.

---

### 3.12 · TRAB-06 · Postest · 14/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-06 | Talavera | 14/10/2026 | Postest | OBS-02 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | · | · | X | 5 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | · | · | X | · | 4 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | · | · | X | 5 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | · | X | · | 4 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | · | · | X | 5 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | · | · | X | 5 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | · | · | X | · | 4 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | · | · | X | 5 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 18 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 19 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **37** | 8-40 |

**Nivel de satisfacción:** Alto · **Observación:** El operador respondió sin consultar el sistema; se garantizó el anonimato.

---

### 3.13 · TRAB-07 · Pretest · 13/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-07 | San Jeronimo | 13/08/2026 | Pretest | OBS-01 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | X | · | · | · | · | 1 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | X | · | · | · | · | 1 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | X | · | · | · | · | 1 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | X | · | · | · | · | 1 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | X | · | · | · | · | 1 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | X | · | · | · | 2 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | X | · | · | · | · | 1 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | X | · | · | · | 2 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 4 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 6 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **10** | 8-40 |

**Nivel de satisfacción:** Bajo · **Observación:** Aplicado al término de la jornada, sin presencia de terceros.

---

### 3.14 · TRAB-07 · Postest · 15/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-07 | San Jeronimo | 15/10/2026 | Postest | OBS-01 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | · | X | · | 4 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | · | · | X | · | 4 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | · | X | · | 4 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | · | X | · | 4 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | · | X | · | 4 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | · | X | · | 4 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | · | · | X | · | 4 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | · | X | · | 4 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 16 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 16 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **32** | 8-40 |

**Nivel de satisfacción:** Alto · **Observación:** Aplicado al cierre del periodo auditado, en presencia del auditor de campo.

---

### 3.15 · TRAB-08 · Pretest · 13/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-08 | Huancaray | 13/08/2026 | Pretest | OBS-02 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | X | · | · | 3 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | · | X | · | · | 3 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | X | · | · | 3 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | X | · | · | 3 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | X | · | · | 3 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | X | · | · | 3 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | · | X | · | · | 3 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | X | · | · | 3 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 12 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 12 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **24** | 8-40 |

**Nivel de satisfacción:** Medio · **Observación:** Se explicó la escala Likert antes de iniciar; no hubo ítems en blanco.

---

### 3.16 · TRAB-08 · Postest · 15/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-08 | Huancaray | 15/10/2026 | Postest | OBS-02 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | · | · | X | 5 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | · | · | · | X | 5 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | · | · | X | 5 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | · | · | X | 5 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | · | · | X | 5 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | · | · | X | 5 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | · | · | · | X | 5 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | · | · | X | 5 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 20 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 20 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **40** | 8-40 |

**Nivel de satisfacción:** Alto · **Observación:** Se registraron comentarios adicionales favorables sobre el control FEFO.

---

### 3.17 · TRAB-09 · Pretest · 14/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-09 | Chicmo | 14/08/2026 | Pretest | OBS-01 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | X | · | · | 3 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | X | · | · | · | 2 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | X | · | · | 3 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | X | · | · | · | 2 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | X | · | · | 3 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | X | · | · | 3 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | X | · | · | · | 2 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | X | · | · | 3 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 10 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 11 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **21** | 8-40 |

**Nivel de satisfacción:** Medio · **Observación:** Cuestionario aplicado en el almacén, antes de la capacitación en el SIVAC.

---

### 3.18 · TRAB-09 · Postest · 16/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-09 | Chicmo | 16/10/2026 | Postest | OBS-01 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | · | · | X | 5 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | · | · | · | X | 5 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | · | · | X | 5 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | · | · | X | 5 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | · | · | X | 5 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | · | · | X | 5 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | · | · | · | X | 5 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | · | · | X | 5 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 20 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 20 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **40** | 8-40 |

**Nivel de satisfacción:** Alto · **Observación:** Cuestionario aplicado tras cuatro semanas de uso continuo del SIVAC.

---

### 3.19 · TRAB-10 · Pretest · 14/08/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-10 | Huancabamba | 14/08/2026 | Pretest | OBS-02 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | X | · | · | · | 2 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | X | · | · | · | 2 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | X | · | · | · | 2 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | X | · | · | · | 2 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | X | · | · | · | 2 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | X | · | · | · | 2 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | X | · | · | · | 2 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | X | · | · | · | 2 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 8 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 8 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **16** | 8-40 |

**Nivel de satisfacción:** Bajo · **Observación:** El operador solicitó releer dos reactivos; se aclaró sin inducir la respuesta.

---

### 3.20 · TRAB-10 · Postest · 16/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-10 | Huancabamba | 16/10/2026 | Postest | OBS-02 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | · | X | · | 4 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | · | · | X | · | 4 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | · | X | · | 4 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | · | X | · | 4 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | · | X | · | 4 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | · | · | X | 5 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | · | · | X | · | 4 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | · | · | X | 5 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 16 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 18 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **34** | 8-40 |

**Nivel de satisfacción:** Alto · **Observación:** El operador respondió sin consultar el sistema; se garantizó el anonimato.

---

### 3.21 · TRAB-11 · Pretest · 07/09/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-11 | Pampachiri | 07/09/2026 | Pretest | OBS-01 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | X | · | · | · | 2 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | X | · | · | · | 2 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | X | · | · | · | 2 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | X | · | · | · | 2 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | X | · | · | · | 2 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | X | · | · | · | 2 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | X | · | · | · | 2 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | X | · | · | · | 2 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 8 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 8 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **16** | 8-40 |

**Nivel de satisfacción:** Bajo · **Observación:** Aplicado al término de la jornada, sin presencia de terceros.

---

### 3.22 · TRAB-11 · Postest · 19/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-11 | Pampachiri | 19/10/2026 | Postest | OBS-01 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | · | X | · | 4 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | · | · | X | · | 4 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | · | · | X | 5 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | · | X | · | 4 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | · | · | X | 5 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | · | X | · | 4 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | · | · | X | · | 4 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | · | · | X | 5 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 17 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 18 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **35** | 8-40 |

**Nivel de satisfacción:** Alto · **Observación:** Aplicado al cierre del periodo auditado, en presencia del auditor de campo.

---

### 3.23 · TRAB-12 · Pretest · 07/09/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-12 | San Antonio de Cachi | 07/09/2026 | Pretest | OBS-02 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | X | · | · | · | · | 1 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | X | · | · | · | 2 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | X | · | · | · | · | 1 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | X | · | · | · | · | 1 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | X | · | · | · | 2 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | X | · | · | · | 2 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | X | · | · | · | 2 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | X | · | · | · | · | 1 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 5 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 7 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **12** | 8-40 |

**Nivel de satisfacción:** Bajo · **Observación:** Se explicó la escala Likert antes de iniciar; no hubo ítems en blanco.

---

### 3.24 · TRAB-12 · Postest · 19/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-12 | San Antonio de Cachi | 19/10/2026 | Postest | OBS-02 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | · | X | · | 4 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | · | · | X | · | 4 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | · | X | · | 4 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | · | X | · | 4 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | · | X | · | 4 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | · | X | · | 4 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | · | · | X | · | 4 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | · | X | · | 4 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 16 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 16 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **32** | 8-40 |

**Nivel de satisfacción:** Alto · **Observación:** Se registraron comentarios adicionales favorables sobre el control FEFO.

---

### 3.25 · TRAB-13 · Pretest · 08/09/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-13 | Turpo | 08/09/2026 | Pretest | OBS-01 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | X | · | · | 3 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | X | · | · | · | 2 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | X | · | · | · | 2 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | X | · | · | 3 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | X | · | · | 3 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | X | · | · | 3 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | X | · | · | · | 2 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | X | · | · | 3 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 10 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 11 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **21** | 8-40 |

**Nivel de satisfacción:** Medio · **Observación:** Cuestionario aplicado en el almacén, antes de la capacitación en el SIVAC.

---

### 3.26 · TRAB-13 · Postest · 20/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-13 | Turpo | 20/10/2026 | Postest | OBS-01 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | · | · | X | 5 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | · | · | · | X | 5 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | · | · | X | 5 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | · | X | · | 4 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | · | · | X | 5 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | · | · | X | 5 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | · | · | · | X | 5 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | · | · | X | 5 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 19 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 20 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **39** | 8-40 |

**Nivel de satisfacción:** Alto · **Observación:** Cuestionario aplicado tras cuatro semanas de uso continuo del SIVAC.

---

### 3.27 · TRAB-14 · Pretest · 08/09/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-14 | Kishuara | 08/09/2026 | Pretest | OBS-02 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | X | · | · | · | 2 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | X | · | · | · | 2 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | X | · | · | · | 2 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | X | · | · | · | 2 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | X | · | · | · | 2 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | X | · | · | · | 2 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | X | · | · | · | 2 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | X | · | · | · | 2 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 8 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 8 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **16** | 8-40 |

**Nivel de satisfacción:** Bajo · **Observación:** El operador solicitó releer dos reactivos; se aclaró sin inducir la respuesta.

---

### 3.28 · TRAB-14 · Postest · 20/10/2026

| Operador (OP) | Centro de acopio | Fecha | Momento | Encuestador |
| --- | --- | :---: | :---: | :---: |
| TRAB-14 | Kishuara | 20/10/2026 | Postest | OBS-02 |

| N.° | Código | Reactivo | 1 | 2 | 3 | 4 | 5 | Valor |
| :---: | :---: | --- | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | AP-01 | El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias. | · | · | · | X | · | 4 |
| 2 | AP-02 | La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos. | · | · | · | X | · | 4 |
| 3 | AP-03 | El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo. | · | · | · | · | X | 5 |
| 4 | AP-04 | Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores. | · | · | · | X | · | 4 |
| 5 | UP-01 | La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas. | · | · | · | · | X | 5 |
| 6 | UP-02 | El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones. | · | · | · | · | X | 5 |
| 7 | UP-03 | La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos. | · | · | · | X | · | 4 |
| 8 | UP-04 | En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA. | · | · | · | · | X | 5 |

| Dimensión | Reactivos | Puntaje | Rango |
| --- | :---: | ---: | :---: |
| Aceptación del proceso (AP) | AP-01 a AP-04 | 17 | 4-20 |
| Utilidad percibida (UP) | UP-01 a UP-04 | 19 | 4-20 |
| **Puntaje global TAM** | 8 reactivos | **36** | 8-40 |

**Nivel de satisfacción:** Alto · **Observación:** El operador respondió sin consultar el sistema; se garantizó el anonimato.

---

### 3.29 · Matriz consolidada de satisfacción (forma ancha)

| Operador | Centro | pre_AP1 | pre_AP2 | pre_AP3 | pre_AP4 | pre_UP1 | pre_UP2 | pre_UP3 | pre_UP4 | AP pre | UP pre | TAM pre | Nivel pre | post_AP1 | post_AP2 | post_AP3 | post_AP4 | post_UP1 | post_UP2 | post_UP3 | post_UP4 | AP post | UP post | TAM post | Nivel post |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| TRAB-01 | ALMACÉN (CHANKA) | 2 | 2 | 2 | 2 | 2 | 3 | 2 | 2 | 8 | 9 | 17 | Bajo | 4 | 5 | 4 | 5 | 5 | 5 | 4 | 5 | 18 | 19 | 37 | Alto |
| TRAB-02 | ALMACÉN (CHANKA) | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 6 | 8 | 14 | Bajo | 4 | 4 | 4 | 4 | 5 | 4 | 4 | 5 | 16 | 18 | 34 | Alto |
| TRAB-03 | Hospital Andahuaylas | 2 | 2 | 3 | 2 | 3 | 2 | 2 | 3 | 9 | 10 | 19 | Medio | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 19 | 20 | 39 | Alto |
| TRAB-04 | Hospital ESSALUD Andahuaylas | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 11 | 12 | 23 | Medio | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 20 | 20 | 40 | Alto |
| TRAB-05 | Centro de Salud Andahuaylas | 2 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 6 | 8 | 14 | Bajo | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 16 | 16 | 32 | Alto |
| TRAB-06 | Talavera | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 8 | 8 | 16 | Bajo | 5 | 4 | 5 | 4 | 5 | 5 | 4 | 5 | 18 | 19 | 37 | Alto |
| TRAB-07 | San Jeronimo | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 2 | 4 | 6 | 10 | Bajo | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 16 | 16 | 32 | Alto |
| TRAB-08 | Huancaray | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 12 | 12 | 24 | Medio | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 20 | 20 | 40 | Alto |
| TRAB-09 | Chicmo | 3 | 2 | 3 | 2 | 3 | 3 | 2 | 3 | 10 | 11 | 21 | Medio | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 20 | 20 | 40 | Alto |
| TRAB-10 | Huancabamba | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 8 | 8 | 16 | Bajo | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 16 | 18 | 34 | Alto |
| TRAB-11 | Pampachiri | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 8 | 8 | 16 | Bajo | 4 | 4 | 5 | 4 | 5 | 4 | 4 | 5 | 17 | 18 | 35 | Alto |
| TRAB-12 | San Antonio de Cachi | 1 | 2 | 1 | 1 | 2 | 2 | 2 | 1 | 5 | 7 | 12 | Bajo | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 16 | 16 | 32 | Alto |
| TRAB-13 | Turpo | 3 | 2 | 2 | 3 | 3 | 3 | 2 | 3 | 10 | 11 | 21 | Medio | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 19 | 20 | 39 | Alto |
| TRAB-14 | Kishuara | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 8 | 8 | 16 | Bajo | 4 | 4 | 5 | 4 | 5 | 5 | 4 | 5 | 17 | 19 | 36 | Alto |

*Nota.* Los puntajes y el nivel se calculan desde los ocho reactivos; no se transcriben de forma independiente. Equivalente en formato largo en `instrumento03_reactivos.csv`.

<a id="s4"></a>
## Sección 4. Verificación estadística del conjunto

Esta sección no forma parte de los instrumentos: comprueba que el crudo generado produce el comportamiento que sustentan las hipótesis. Todos los valores se calculan desde las fichas de las secciones 1 a 3.

### 4.1 · Estadísticos descriptivos pretest–postest

| Indicador | Unidad | Pretest (M ± DE) | Postest (M ± DE) | Diferencia (M ± DE) | Cambio relativo |
| --- | :---: | ---: | ---: | ---: | ---: |
| T_reg | min | 37.18 ± 3.83 | 7.18 ± 1.05 | -30.00 ± 2.88 | -80.7 % |
| T_vale | min | 18.21 ± 2.87 | 3.04 ± 0.60 | -15.18 ± 2.32 | -83.3 % |
| RSD | % | 63.57 ± 6.77 | 95.89 ± 2.32 | +32.32 ± 4.75 | +50.8 % |
| CPE | % | 67.71 ± 6.92 | 95.43 ± 2.65 | +27.71 ± 4.83 | +40.9 % |
| AP | pts | 8.07 ± 2.27 | 17.71 ± 1.64 | +9.64 ± 1.08 | +119.5 % |
| UP | pts | 9.00 ± 1.88 | 18.50 ± 1.56 | +9.50 ± 1.02 | +105.6 % |
| TAM global | pts | 17.07 ± 4.08 | 36.21 ± 3.09 | +19.14 ± 1.61 | +112.1 % |

### 4.2 · Normalidad de las diferencias (Shapiro-Wilk)

| Indicador | W | gl | p | Decisión | Prueba adoptada |
| --- | ---: | :---: | ---: | :---: | :---: |
| T_reg | 0.9786 | 13 | 0.9657 | Normal | t de Student |
| T_vale | 0.9325 | 13 | 0.3311 | Normal | t de Student |
| RSD | 0.9066 | 13 | 0.1406 | Normal | t de Student |
| CPE | 0.9303 | 13 | 0.3078 | Normal | t de Student |
| AP | 0.9091 | 13 | 0.1530 | Normal | t de Student |
| UP | 0.8764 | 13 | 0.0516 | Normal | t de Student |
| TAM global | 0.9553 | 13 | 0.6461 | Normal | t de Student |

### 4.3 · Contrastes pareados y tamaño del efecto

| Indicador | Estadístico | p | d de Cohen | Significativo (α = .05) |
| --- | ---: | ---: | ---: | :---: |
| T_reg | -38.944 | 7.57e-15 | -10.41 | Sí |
| T_vale | -24.509 | 2.88e-12 | -6.55 | Sí |
| RSD | 25.461 | 1.77e-12 | 6.80 | Sí |
| CPE | 21.484 | 1.54e-11 | 5.74 | Sí |
| AP | 33.352 | 5.57e-14 | 8.91 | Sí |
| UP | 34.881 | 3.13e-14 | 9.32 | Sí |
| TAM global | 44.477 | 1.36e-15 | 11.89 | Sí |

*Nota.* El estadístico corresponde a la prueba adoptada según 4.2: *t* para las distribuciones normales y *W* de Wilcoxon en caso contrario. Los valores *p* se informan sin ajuste; el ajuste de Holm no altera ninguna decisión porque todos los contrastes superan holgadamente el umbral.

### 4.4 · Confiabilidad del Instrumento 03 (alfa de Cronbach)

| Momento | Escala | Ítems | n | Alfa |
| :---: | :---: | :---: | :---: | ---: |
| Pretest | global | 8 | 14 | 0.9385 |
| Pretest | AP | 4 | 14 | 0.8766 |
| Pretest | UP | 4 | 14 | 0.8737 |
| Postest | global | 8 | 14 | 0.9151 |
| Postest | AP | 4 | 14 | 0.8306 |
| Postest | UP | 4 | 14 | 0.8405 |

### 4.5 · Lectura de las hipótesis

- **HE1 — Oportunidad.** T_reg baja de 37.18 a 7.18 min (-80.7 %) y T_vale de 18.21 a 3.04 min (-83.3 %); ambas diferencias son significativas.
- **HE2 — Consistencia documental.** RSD sube de 63.57 % a 95.89 % y CPE de 67.71 % a 95.43 %; la mejora es significativa en ambos indicadores.
- **HE3 — Satisfacción.** AP pasa de 8.07 a 17.71 puntos y UP de 9.00 a 18.50; el puntaje global TAM se desplaza de la banda Baja/Media a la banda Alta.

