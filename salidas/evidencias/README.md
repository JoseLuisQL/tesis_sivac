# CARPETA DE EVIDENCIAS CIENTÍFICAS Y OPERATIVAS — SIVAC-THESIS-LAB
> **Tesis:** APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS MENSUALES DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II  
> **Tesista:** Bach. José Luis Quispe León  
> **Asesora:** Dra. Norma Lorena Catacora Flores  
> **Universidad Nacional José María Arguedas (UNAJMA)** — Escuela Profesional de Ingeniería de Sistemas  
> **Diseño:** Preexperimental con pretest y postest en un solo grupo ($O_1 \longrightarrow X \longrightarrow O_2$)  
> **Población censal:** $N = n = 14$ trabajadores de inmunizaciones en 13 centros de acopio de la DISA Apurímac II  
> **Estado del conjunto:** `DATOS DE PRUEBA – REEMPLAZAR (DEC-007)`; la estructura y el pipeline son definitivos, los valores no son mediciones de campo.

---

## 1. Estructura del Repositorio de Evidencias

Esta carpeta consolida todos los artefactos, bases de datos, instrumentos y códigos fuente que sustentan de forma reproducible la elaboración del Informe Final de Tesis (`salidas/documentos/informe_final_v28.docx`). Todas las copias se derivan de su fuente única con `scripts/estadistica/sincronizar_evidencias.py`; las huellas SHA-256 quedan registradas en `SINCRONIZACION.json`.

### `base_de_datos/`
- **`centros_acopio_reales_sivac.json`:** Catálogo oficial extraído de la base de datos relacional PostgreSQL de producción de SIVAC, con los centros de acopio, redes y microredes de la DISA Apurímac II. La muestra usa 13 de esos centros para los 14 operadores censales.
- **`pretest_campo.csv` / `posttest_campo.csv`:** Matrices analíticas (14 × 18) de línea base y final para los 14 operadores pareados (`TRAB-01` a `TRAB-14`).
- **`datos_recolectados_pre_post.xlsx`:** Libro de cálculo con hojas `PRETEST` y `POSTTEST`, reconstruido desde los CSV.
- **`instrumento01_replicas.csv`:** 168 réplicas cronometradas (14 × 2 × 6) del Instrumento 01.
- **`instrumento02_asientos.csv`:** 1 120 asientos auditados (14 × 2 × 40) del Instrumento 02.
- **`instrumento02_despachos.csv`:** 700 despachos conciliados (14 × 2 × 25) del Instrumento 02.
- **`instrumento03_reactivos.csv`:** 224 respuestas Likert (14 × 2 × 8) del Instrumento 03 (TAM).
- **`matriz_analitica_pre_post.csv`:** Consolidado (28 × 19) por unidad y momento, con los siete indicadores.
- **`control_integridad.json`:** Recuentos, llaves y huellas del conjunto primario.
- **`SIVAC_DATOS_CAMPO.md`:** Registro integral de campo: fichas completas de los tres instrumentos, matrices de indicadores y Tablas 35–43.
- **`README_DECLARACION_DEC007.md`:** Declaración metodológica formal que rotula el conjunto como `DATOS DE PRUEBA – REEMPLAZAR (DEC-007)` (copia de `datos/recolectados/README.md`).

### `instrumentos_aplicados/`
- **`INSTRUMENTO_01_FICHA_CRONOMETRICA_PRE_POST.docx`:** Observación sistemática y cronometraje de tiempos ($T_{reg}$ y $T_{vale}$, en minutos).
- **`INSTRUMENTO_02_FICHA_AUDITORIA_PRE_POST.docx`:** Guía de auditoría y conciliación documental de lotes, kardex y comprobantes ($RSD$ y $CPE$, en porcentajes).
- **`INSTRUMENTO_03_CUESTIONARIO_TAM_MODALIDAD_A_PRETEST.docx`:** Cuestionario de satisfacción bajo el Modelo de Aceptación Tecnológica (TAM) de Davis (1989), 8 reactivos Likert (1 a 5) para Agilidad Percibida ($AP$) y Utilidad Percibida ($UP$).
- **`INSTRUMENTO_03_CUESTIONARIO_TAM_MODALIDAD_B_POSTEST.docx`:** Cuestionario complementario de usabilidad del sistema SIVAC (DEC-019).
- **`EXPEDIENTE_VALIDACION_JUICIO_EXPERTOS_MODELO_FANY.docx`:** Expediente institucional de validación por juicio de expertos según el formato UNAJMA (Modelo Fany 2024, DEC-015 y DEC-020).

### `scripts_estadisticos/`
- **`analisis_estadistico_sivac.py`:** Pipeline maestro reproducible en Python que ejecuta:
  1. Confiabilidad psicométrica (Alfa de Cronbach con IC 95% de Feldt).
  2. Estadística descriptiva de las 3 dimensiones (medias, desviaciones estándar, medianas, IQR, mínimos, máximos y variaciones porcentuales).
  3. Pruebas de normalidad de Shapiro-Wilk sobre diferencias pareadas ($d_i = post_i - pre_i$).
  4. Contrastes pareados ($t$-Student y Rangos con Signo de Wilcoxon con ajuste secuencial de Holm-Bonferroni).
  5. Tamaños del efecto ($d$ de Cohen y $r$ de Rosenthal).
  6. Figuras a 300 DPI con estética de salida SPSS.
- **`generar_datos_sinteticos.py`:** Generador determinista del conjunto de prueba (semilla `20261026`) con sus tres instrumentos y `control_integridad.json`.
- **`construir_registro_campo.py`:** Compone `SIVAC_DATOS_CAMPO.md` a partir de los CSV y del reporte estadístico.
- **`consultar_db_sivac.py`:** Auditoría de solo lectura contra la base PostgreSQL de SIVAC para mapear centros de acopio y usuarios reales.

Todos ellos viven en `scripts/estadistica/`, salvo `consultar_db_sivac.py`, que se mantiene en `scripts/utilidades/`. Las copias de esta carpeta conservan la versión ejecutada.

### `tablas_resultados/`
- **`reporte_estadistico_completo.json`:** Resultados numéricos completos, valores $p$, estadísticos de contraste y decisiones de hipótesis exportados por el pipeline.

### `figuras_spss_300dpi/`
- **`figura_d1_tiempos_boxplots_spss.png`:** Diagramas de cajas pareados para $T_{reg}$ y $T_{vale}$ (Dimensión 1: Oportunidad).
- **`figura_d2_consistencia_barras_spss.png`:** Barras de error con medias e IC para $RSD$ y $CPE$ (Dimensión 2: Consistencia documental).
- **`figura_d3_satisfaccion_tam_spss.png`:** Comparación TAM (Agilidad percibida, Utilidad percibida y puntaje global) pretest vs postest (Dimensión 3: Satisfacción).

### Archivos de control
- **`SINCRONIZACION.json`:** Huellas SHA-256, tamaños y recuentos de cada copia de evidencia en el momento de la última sincronización.
- **`../estadistica/AUDITORIA_DATOS.md` / `.json`:** 132 comprobaciones: estructura, recálculo, coherencia entre instrumentos, reproducibilidad estadística, sincronía de evidencias y paridad del informe final vigente (tablas 35-43, matrices del anexo y figuras embebidas) y paridad del libro de tablas de anexos (hojas, matrices, descriptivos, alfas, normalidad y contrastes) y orden de la capa de datos (mapa documental, inventario, integridad y estado de prueba).

---

## 2. Instrucciones de Reejecución

Desde la raíz del proyecto y con el entorno virtual activo:

```bash
python scripts/estadistica/generar_datos_sinteticos.py    # solo si se regenera el conjunto de prueba
python scripts/estadistica/inventario_datos.py            # inventario de datos/ (huellas y formas)
python scripts/estadistica/analisis_estadistico_sivac.py  # tablas, contrastes y figuras
python scripts/estadistica/construir_registro_campo.py    # registro integral en Markdown
python scripts/estadistica/sincronizar_evidencias.py      # copias y huellas de evidencia
python scripts/estadistica/verificar_conjunto_datos.py    # auditoría: debe cerrar 132/132
python scripts/estadistica/sincronizar_evidencias.py --verificar   # control sin escribir
```

Cuando el tesista ingrese las mediciones definitivas en `datos/recolectados/pretest_campo.csv` y `posttest_campo.csv`, la misma cadena actualiza tablas, figuras, registro y evidencias sin tocar el código.
