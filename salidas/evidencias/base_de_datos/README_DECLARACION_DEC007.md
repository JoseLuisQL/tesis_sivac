# DATOS RECOLECTADOS — SIVAC-THESIS-LAB
> **ESTADO:** `DATOS DE PRUEBA – REEMPLAZAR (DEC-007)`  
> **ÁMBITO:** Dirección de Salud Apurímac II — Personal de Inmunizaciones (Población Censal $N = n = 14$ operadores en 13 centros de acopio)  
> **DISEÑO:** Preexperimental con pretest y postest en un solo grupo ($O_1 \longrightarrow X \longrightarrow O_2$)

---

## 1. Declaración de Advertencia Metodológica
Los archivos contenidos en esta carpeta corresponden a un **conjunto de datos de prueba preconfigurado** para validar la ejecución íntegra, trazabilidad y reproducibilidad de los scripts bioestadísticos, pruebas inferenciales y generadores de figuras de la tesis.

Cuando el tesista disponga de las mediciones empíricas definitivas digitadas en campo:
1. Reemplace los valores en `pretest_campo.csv` y `posttest_campo.csv` (o actualice las hojas en `datos_recolectados_pre_post.xlsx`).
2. Ejecute la cadena completa de procesamiento:
   ```bash
   python scripts/estadistica/analisis_estadistico_sivac.py  # tablas, contrastes y figuras
   python scripts/estadistica/construir_registro_campo.py   # registro integral en Markdown
   python scripts/estadistica/sincronizar_evidencias.py      # copias de evidencia
   python scripts/estadistica/verificar_conjunto_datos.py    # auditoría (debe dar X/X)
   ```
3. El pipeline recomputará automáticamente todos los estadísticos descriptivos, pruebas de normalidad (Shapiro-Wilk), contrastes de hipótesis (Wilcoxon pareado y $t$-Student), tamaños del efecto ($r$ de Rosenthal y $d$ de Cohen), confiabilidad (Alfa de Cronbach con IC 95%) y figuras estadísticas a 300 DPI.

## 2. Archivos de la carpeta

| Archivo | Contenido |
|---|---|
| `pretest_campo.csv` | Matriz analítica de línea base (14 × 18): 7 indicadores en proceso manual |
| `posttest_campo.csv` | Matriz analítica final (14 × 18): mismos 7 indicadores con SIVAC |
| `datos_recolectados_pre_post.xlsx` | Libro Excel con hojas `PRETEST` y `POSTTEST` derivadas de los CSV |
| `SIVAC_DATOS_CAMPO.md` | Registro integral de campo: fichas de los tres instrumentos, matrices y Tablas 35–43 |
| `README.md` | Este documento (se copia a evidencias como `README_DECLARACION_DEC007.md`) |

Las mediciones primarias (réplicas cronometradas, asientos auditados, despachos conciliados y reactivos Likert) viven en `datos/prueba_sintetica/`; los CSV de esta carpeta son su consolidación por unidad y momento.

---

## 3. Estructura de Columnas (Diccionario de Variables)

| Columna | Tipo | Rango / Unidad | Dimensión Oficial (DEC-007) | Indicador Evaluado |
|---|---|---|---|---|
| `sujeto_id` | Texto | `TRAB-01` a `TRAB-14` | Control Censal | Identificador anónimo del operador |
| `centro_acopio` | Texto | 13 centros de acopio | Geográfico | Centro de acopio o red territorial |
| `t_reg` | Decimal | Minutos | Dimensión 1: Oportunidad | $I_{1.1}$: Tiempo de registro de movimiento de vacunas |
| `t_vale` | Decimal | Minutos | Dimensión 1: Oportunidad | $I_{1.2}$: Tiempo de emisión de comprobante de salida / vale |
| `rsd` | Decimal | Porcentaje (%) | Dimensión 2: Consistencia | $I_{2.1}$: Porcentaje de registros sin discrepancias |
| `cpe` | Decimal | Porcentaje (%) | Dimensión 2: Consistencia | $I_{2.2}$: Concordancia programada vs. entregada |
| `ap_01` a `ap_04` | Entero | Likert (1 a 5) | Dimensión 3: Satisfacción | Reactivos atómicos de Aceptación del Proceso (TAM) |
| `up_01` a `up_04` | Entero | Likert (1 a 5) | Dimensión 3: Satisfacción | Reactivos atómicos de Utilidad Percibida (TAM) |
| `score_ap` | Entero | 4 a 20 puntos | Dimensión 3: Satisfacción | Puntaje sumativo de Aceptación del Proceso |
| `score_up` | Entero | 4 a 20 puntos | Dimensión 3: Satisfacción | Puntaje sumativo de Utilidad Percibida |
| `score_tam_total` | Entero | 8 a 40 puntos | Dimensión 3: Satisfacción | Puntaje global Modalidad A (TAM) |
| `nivel_satisfaccion` | Texto | Bajo, Medio, Alto | Baremo Oficial | Baremo: Bajo (8-18), Medio (19-29), Alto (30-40) |
