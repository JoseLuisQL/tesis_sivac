---
name: analisis-estadistico-avanzado
description: Protocolos, modelos matemáticos, scripts en Python y plantillas de reporte APA 7 para análisis estadístico descriptivo e inferencial en diseños preexperimentales (pretest-postest) para SIVAC-THESIS-LAB.
---

# ANÁLISIS ESTADÍSTICO AVANZADO — SIVAC (PRETEST - POSTEST)

> **Diseño Metodológico:** Preexperimental con pretest y postest en un solo grupo ($O_1 \longrightarrow X \longrightarrow O_2$).  
> **Población y Muestra:** Censal, compuesta por la totalidad del personal del servicio de inmunizaciones y cadena de frío de la DISA Apurímac II ($N = n = 14$).  
> **Regla Innegociable:** Prohibido inventar datos empíricos. Los contrastes inferenciales se ejecutan exclusivamente sobre los datos reales suministrados por el tesista en `datos/` o `07_ESTADISTICA_Y_DATOS/datos_campo/`.

---

## 1. Análisis Descriptivo por Variable y Dimensión

Para cada uno de los indicadores cuantitativos en Pretest ($O_1$) y Postest ($O_2$):

### 1.1. Estadísticos de Tendencia Central y Dispersión
- **Variables cuantitativas continuas (Tiempos en minutos):**
  - Media aritmética ($\bar{X}$) y Desviación Estándar ($DE$ o $s$).
  - Mediana ($Me$) y Rango Intercuartílico ($RIC = Q_3 - Q_1$).
  - Mínimo y Máximo.
- **Variables ordinales (Escala Likert TAM 1-5):**
  - Mediana ($Me$) y Rango Intercuartílico ($RIC$).
  - Frecuencias absolutas ($f$) y relativas porcentuales ($\%$).
- **Variación Porcentual Relativa ($\Delta\%$):**
  $$\Delta\% = \left( \frac{\bar{X}_{\text{post}} - \bar{X}_{\text{pre}}}{\bar{X}_{\text{pre}}} \right) \times 100$$
  O en términos de medianas si los datos no son normales:
  $$\Delta\%_{Me} = \left( \frac{Me_{\text{post}} - Me_{\text{pre}}}{Me_{\text{pre}}} \right) \times 100$$

---

## 2. Evaluación de Normalidad de las Diferencias Pareadas

Para muestras pequeñas ($n = 14 < 50$), la prueba canónica obligatoria según el reglamento de UNAJMA es la **Prueba de Normalidad de Shapiro-Wilk**.

### 2.1. Unidad de Evaluación
La normalidad en muestras relacionadas se evalúa sobre el vector de **diferencias pareadas** ($\Delta_i = X_{i,\text{post}} - X_{i,\text{pre}}$), no sobre las muestras aisladas.

### 2.2. Planteamiento de Hipótesis de Normalidad
- **Hipótesis Nula ($H_0$):** Las diferencias pareadas se distribuyen normalmente ($p > .05$).
- **Hipótesis Alterna ($H_1$):** Las diferencias pareadas no se distribuyen normalmente ($p \le .05$).

### 2.3. Criterio de Decisión Estadística
- Si $p > .05$: Se asume normalidad $\longrightarrow$ Se aplica prueba paramétrica (**Prueba $t$ de Student para muestras relacionadas**).
- Si $p \le .05$: Se rechaza la normalidad $\longrightarrow$ Se aplica prueba no paramétrica (**Prueba de Rangos con Signo de Wilcoxon**).

---

## 3. Pruebas Inferenciales de Contraste de Hipótesis

### 3.1. Prueba No Paramétrica: Rangos con Signo de Wilcoxon (Vía Principal)
Apta para variables ordinales (Likert TAM) y variables continuas que no cumplen normalidad o con muestras reducidas ($n = 14$).

1. **Cálculo de Rangos:**
   - Se calculan las diferencias pareadas $D_i = X_{i,\text{post}} - X_{i,\text{pre}}$.
   - Se eliminan las diferencias nulas ($D_i = 0$, $n_r \le n$).
   - Se asignan rangos a los valores absolutos $|D_i|$ de menor a mayor.
   - Se calcula la suma de rangos positivos ($W^+$) y negativos ($W^-$).
   - El estadístico de prueba es $W = \min(W^+, W^-)$ o $T$.
2. **Aproximación Asintótica Z:**
   $$Z = \frac{W - \mu_W}{\sigma_W} = \frac{W - \frac{n(n+1)}{4}}{\sqrt{\frac{n(n+1)(2n+1)}{24}}}$$
   (Ajustado por empates si existen).
3. **Cálculo del Tamaño del Efecto ($r$ de Rosenthal):**
   $$r = \frac{|Z|}{\sqrt{N}}$$
   Donde $N = 2 \times n = 28$ (número total de observaciones pareadas) o $n = 14$. Se reporta la convención aplicada.
   - **Baremos de Rosenthal / Cohen:**
     - $|r| < 0.10$: Efecto despreciable.
     - $0.10 \le |r| < 0.30$: Efecto pequeño.
     - $0.30 \le |r| < 0.50$: Efecto mediano.
     - $|r| \ge 0.50$: **Efecto grande** (Impacto sustantivo del sistema SIVAC).

### 3.2. Prueba Paramétrica: $t$ de Student para Muestras Relacionadas (Vía Alternativa)
Apta únicamente si la prueba de Shapiro-Wilk confirma normalidad estricta ($p > .05$).

1. **Estadístico de Contraste:**
   $$t = \frac{\bar{D}}{s_D / \sqrt{n}}$$
   Con $gl = n - 1 = 13$ grados de libertad.
2. **Tamaño del Efecto ($d$ de Cohen para datos pareados):**
   $$d_z = \frac{\bar{D}}{s_D}$$
   - $0.20 \le d < 0.50$: Efecto pequeño.
   - $0.50 \le d < 0.80$: Efecto moderado.
   - $d \ge 0.80$: **Efecto grande.**

---

## 4. Estilo de Reporte Académico en Prosa APA 7 (Español)

### 4.1. Plantilla de Reporte para Prueba de Wilcoxon
> "La prueba de rangos con signo de Wilcoxon evidenció una reducción estadísticamente significativa en el tiempo de registro de movimientos tras la implementación del sistema web SIVAC ($Z = -3.296$, $p < .001$), con una mediana previa de 28.5 minutos ($RIC = 6.2$) frente a una mediana posterior de 3.2 minutos ($RIC = 1.1$). El tamaño del efecto obtenido ($r = .623$) indica una magnitud de impacto grande según los criterios de Cohen (1988), demostrando la efectividad de la solución tecnológica."

### 4.2. Plantilla de Reporte para Prueba $t$ de Student
> "El análisis mediante la prueba $t$ de Student para muestras relacionadas confirmó una diferencia estadísticamente significativa entre el pretest y el postest en el porcentaje de concordancia programada vs entregada, $t(13) = 8.452$, $p < .001$, con un incremento en la media desde el 64.2% ($DE = 8.3$) hasta el 94.6% ($DE = 3.5$). La magnitud de la diferencia reflejó un tamaño del efecto muy grande ($d = 2.259$, IC 95% [1.34, 3.16])."

---

## 5. Script Maestro de Análisis en Python (`analisis_sivac.py`)

```python
import numpy as np
import pandas as pd
from scipy import stats

def ejecutar_analisis_completo(df, col_pre, col_post, nombre_indicador):
    pre = df[col_pre].values
    post = df[col_post].values
    diff = post - pre
    n = len(diff)
    
    # 1. Descriptivos
    desc = {
        "pre_media": np.mean(pre), "pre_de": np.std(pre, ddof=1),
        "pre_mediana": np.median(pre), "pre_iqr": stats.iqr(pre),
        "post_media": np.mean(post), "post_de": np.std(post, ddof=1),
        "post_mediana": np.median(post), "post_iqr": stats.iqr(post),
        "delta_pct_media": ((np.mean(post) - np.mean(pre)) / np.mean(pre)) * 100,
        "delta_pct_mediana": ((np.median(post) - np.median(pre)) / np.median(pre)) * 100
    }
    
    # 2. Normalidad Shapiro-Wilk sobre diferencias
    w_stat, p_normalidad = stats.shapiro(diff)
    desc["shapiro_w"] = w_stat
    desc["shapiro_p"] = p_normalidad
    desc["es_normal"] = p_normalidad > 0.05
    
    # 3. Inferencial
    if desc["es_normal"]:
        t_stat, p_val = stats.ttest_rel(post, pre)
        d_cohen = np.mean(diff) / np.std(diff, ddof=1)
        desc["prueba"] = "t-Student pareada"
        desc["estadistico"] = t_stat
        desc["p_valor"] = p_val
        desc["tamano_efecto"] = d_cohen
        desc["metrica_efecto"] = "d de Cohen"
    else:
        w_wilc, p_val = stats.wilcoxon(post, pre, zero_method='pratt')
        # Z approximation
        mu_w = n * (n + 1) / 4
        sigma_w = np.sqrt(n * (n + 1) * (2 * n + 1) / 24)
        z_stat = (w_wilc - mu_w) / sigma_w
        r_rosenthal = abs(z_stat) / np.sqrt(2 * n)
        desc["prueba"] = "Wilcoxon pareado"
        desc["estadistico"] = w_wilc
        desc["z_score"] = z_stat
        desc["p_valor"] = p_val
        desc["tamano_efecto"] = r_rosenthal
        desc["metrica_efecto"] = "r de Rosenthal"
        
    return desc
```
