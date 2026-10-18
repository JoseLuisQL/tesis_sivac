# REPOSITORIO DE DATOS DE TRABAJO DE CAMPO — PROYECTO SIVAC

> **UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS**  
> **Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas**  
> **Tesis:** *APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II*  
> **Autor:** Bach. José Luis Quispe León | **Asesora:** Dra. Norma Lorena Catacora Flores  
> **Directriz Innegociable:** Constitución SIVAC — Sección 2.1: Prohibición Absoluta de Invención de Datos Empíricos.

---

## 1. Estructura de Archivos del Repositorio

En este directorio se almacenan y auditan las matrices de datos tabulares en formato CSV (delimitado por comas, codificación UTF-8 sin BOM) correspondientes a las evaluaciones de campo en los 11 centros de acopio provinciales ($N = 14$ trabajadores censales):

1. `bd_sivac_pretest.csv`: Datos de la línea base pretest (gestión manual con kardex físico y hojas Excel tradicionales).
2. `bd_sivac_postest.csv`: Datos de la evaluación postest (gestión con el sistema web SIVAC).
3. `bd_sivac_pareado.csv`: Matriz consolidada de diferencias intra-sujeto ($D_i = \text{Post}_i - \text{Pre}_i$) lista para análisis inferencial en R, Python, Jamovi o SPSS.
4. `checksums_sha256.txt`: Firmas criptográficas SHA-256 de los archivos de datos para garantizar inmutabilidad y trazabilidad ante el jurado evaluador.

---

## 2. Diccionario de Campos de la Matriz Tabular

| Columna | Tipo de Dato | Unidad / Escala | Rango Permitido | Descripción Operativa |
|---|---|---|---|---|
| `sujeto_id` | Texto (Código) | Nominal | `TRAB-01` a `TRAB-14` | Código unívoco anonimizado del trabajador |
| `centro_acopio` | Texto | Nominal | 11 centros oficiales | Establecimiento de salud sede |
| `fase` | Texto | Nominal | `PRETEST` / `POSTEST` | Momento de medición experimental |
| `t_reg` | Numérico continuo | Minutos (min) | $[0.00, 120.00]$ | Tiempo de registro de 10 establecimientos |
| `t_vale` | Numérico continuo | Minutos (min) | $[0.00, 60.00]$ | Tiempo de emisión de vale oficial |
| `rsd` | Numérico continuo | Porcentaje (%) | $[0.00, 100.00]$ | % de registros sin discrepancias (40 a 60 registros por ventana temporal) |
| `cpe` | Numérico continuo | Porcentaje (%) | `[0, 100]` | Porcentaje de entregas con cantidad física conforme sobre el total de despachos evaluados (Ecuación CPE del Capítulo IV; Instrumento 02) |
| `ap_01` a `ap_04` | Entero | Ordinal (1-5) | `{1, 2, 3, 4, 5}` | Reactivos de Aceptación del Proceso (I3.1, Modalidad A) |
| `score_ap` | Entero | Intervalar | `[4, 20]` | Sumatoria de los 4 ítems de Aceptación del Proceso |
| `up_01` a `up_04` | Entero | Ordinal (1-5) | `{1, 2, 3, 4, 5}` | Reactivos de Utilidad Percibida (I3.2, Modalidad A) |
| `score_up` | Entero | Intervalar | `[4, 20]` | Sumatoria de los 4 ítems de Utilidad Percibida |
| `score_tam_total` | Entero | Intervalar | `[8, 40]` | Puntuación total TAM del instrumento de 8 ítems (`score_ap` + `score_up`) |
| `nivel_satisfaccion` | Texto | Ordinal | `Bajo`, `Medio`, `Alto` | Categorización por terciles del puntaje global: Bajo 8-18, Medio 19-29, Alto 30-40 |

---

## 3. Protocolo de Validación Automática

Todo archivo de datos cargado es verificado mediante el script de control de calidad:
- Integridad estructural: 14 filas de datos + 1 fila de encabezado.
- Cero valores nulos (`NA`, `null`, celdas vacías).
- Rangos numéricos dentro de los límites físicos y psicométricos estipulados.
- Consistencia aritmética: $\text{score\_tam\_total} = \text{score\_ap} + \text{score\_up}$.
