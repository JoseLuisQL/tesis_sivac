# CARPETA DE EVIDENCIAS CIENTÍFICAS Y OPERATIVAS — SIVAC-THESIS-LAB
> **Tesis:** APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS MENSUALES DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II  
> **Tesista:** Bach. José Luis Quispe León  
> **Asesora:** Dra. Norma Lorena Catacora Flores  
> **Universidad Nacional José María Arguedas (UNAJMA)** — Escuela Profesional de Ingeniería de Sistemas  
> **Diseño:** Preexperimental con pretest y postest en un solo grupo ($O_1 \longrightarrow X \longrightarrow O_2$)  
> **Población censal:** $N = n = 14$ trabajadores de inmunizaciones en 14 centros de acopio reales de la DISA Apurímac II  

---

## 1. Estructura del Repositorio de Evidencias

Esta carpeta consolida todos los artefactos, bases de datos, instrumentos y códigos fuente que sustentan de forma reproducible la elaboración del Informe Final de Tesis (`informe_final_v03.docx`):

### `base_de_datos/`
- **`centros_acopio_reales_sivac.json`:** Catálogo oficial extraído directamente desde la base de datos relacional PostgreSQL de producción de SIVAC (`C:\Proyectos\syncova`), conteniendo los 19 centros de acopio reales, redes y microredes de la DISA Apurímac II.
- **`pretest_campo.csv`:** Matriz tabular de mediciones basales en gestión manual para los 14 trabajadores pareados (`TRAB-01` a `TRAB-14`).
- **`posttest_campo.csv`:** Matriz tabular de mediciones posteriores con el sistema web SIVAC para los mismos 14 trabajadores pareados.
- **`datos_recolectados_pre_post.xlsx`:** Libro de cálculo Excel con hojas `PRETEST` y `POSTTEST`.
- **`README_DECLARACION_DEC007.md`:** Declaración metodológica formal que rotula el conjunto como `DATOS DE PRUEBA – REEMPLAZAR (DEC-007)` y certifica la reproducibilidad en un solo comando.

### `instrumentos_aplicados/`
- **`INSTRUMENTO_01_FICHA_CRONOMETRICA_PRE_POST.docx`:** Instrumento de observación sistemática y cronometraje de tiempos ($T_{reg}$ y $T_{vale}$, en minutos).
- **`INSTRUMENTO_02_FICHA_AUDITORIA_PRE_POST.docx`:** Guía de auditoría y verificación documental de lotes, kardex y comprobantes pecosa ($RSD$ y $CPE$, en porcentajes).
- **`INSTRUMENTO_03_CUESTIONARIO_TAM_MODALIDAD_A_PRETEST.docx`:** Cuestionario de satisfacción del usuario bajo el Modelo de Aceptación Tecnológica (TAM) de Davis (1989), con 8 reactivos Likert (1 a 5) que miden Agilidad Percibida ($AP$) y Utilidad Percibida ($UP$).
- **`INSTRUMENTO_03_CUESTIONARIO_TAM_MODALIDAD_B_POSTEST.docx`:** Cuestionario complementario de usabilidad del sistema SIVAC.
- **`EXPEDIENTE_VALIDACION_JUICIO_EXPERTOS_MODELO_FANY.docx`:** Expediente institucional de validación de instrumentos por juicio de expertos según el formato oficial UNAJMA (Modelo Fany 2024, DEC-015 y DEC-020).

### `scripts_estadisticos/`
- **`analisis_estadistico_sivac.py`:** Pipeline maestro reproducible en Python que ejecuta:
  1. Confiabilidad psicométrica (Alfa de Cronbach con IC 95% de Feldt).
  2. Estadística descriptiva de las 3 dimensiones (medias, desviaciones estándar, medianas, IQRs, mínimos, máximos y variaciones porcentuales).
  3. Pruebas de normalidad de Shapiro-Wilk sobre diferencias pareadas ($d_i = post_i - pre_i$).
  4. Contrastes de hipótesis pareados ($t$-Student y Rangos con Signo de Wilcoxon con ajuste secuencial de Holm-Bonferroni).
  5. Tamaños del efecto ($d$ de Cohen y $r$ de Rosenthal).
  6. Generación automatizada de figuras a 300 DPI con estética oficial de salidas de SPSS.
- **`consultar_db_sivac.py`:** Script de auditoría de solo lectura que consulta la base de datos PostgreSQL de SIVAC para mapear centros de acopio y usuarios reales.

### `tablas_resultados/`
- **`reporte_estadistico_completo.json`:** Estructura completa de resultados numéricos, valores $p$, estadísticos de contraste y decisiones de hipótesis exportada por el pipeline.

### `figuras_spss_300dpi/`
- **`figura_d1_tiempos_boxplots_spss.png`:** Diagramas de cajas pareados (Boxplots) estilo SPSS para los tiempos de registro y emisión de vales (Dimensión 1: Oportunidad de procesamiento).
- **`figura_d2_consistencia_barras_spss.png`:** Gráfico de barras de error con medias e intervalos de confianza para el porcentaje de registros sin discrepancias y concordancia programada vs entregada (Dimensión 2: Consistencia documental).
- **`figura_d3_satisfaccion_tam_spss.png`:** Gráfico comparativo de puntajes del modelo TAM (Agilidad percibida, Utilidad percibida y Puntaje global TAM) pretest vs posttest (Dimensión 3: Satisfacción del usuario).

---

## 2. Instrucciones de Reejecución Rápida
Cuando el tesista ingrese las mediciones definitivas de campo en `base_de_datos/pretest_campo.csv` y `posttest_campo.csv`, basta con ejecutar desde la raíz del proyecto:
```bash
python scripts/estadistica/analisis_estadistico_sivac.py
```
Todas las tablas, gráficos y reportes se actualizarán de forma instantánea y determinística.
