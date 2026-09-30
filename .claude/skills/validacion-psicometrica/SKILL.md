---
name: validacion-psicometrica
description: Algoritmos matemáticos, fórmulas psicométricas y generación automatizada de matrices de validación de instrumentos por juicio de expertos según el modelo oficial del Dr. Enrique Cóndor Tinoco (EPIS-UNAJMA) y Tristán-López (2008).
---

# VALIDACIÓN PSICOMÉTRICA DE INSTRUMENTOS — UNAJMA (EPIS)

> **Fundamento Metodológico:** Modelo de Cuantificación de Validez de Contenido del Dr. Enrique Edgardo Cóndor Tinoco (Docente EPIS-UNAJMA), basado en Lawshe (1975), Tristán-López (2008) y Polit & Beck (2007).

---

## 1. Modelo Psicométrico de Validez de Contenido

### 1.1. Los Cinco (5) Criterios de Evaluación por Ítem
Cada juez experto evalúa cada ítem del instrumento bajo 5 criterios independientes:
1. **Suficiencia:** Los ítems propuestos bastan para medir integralmente la dimensión y sus indicadores.
2. **Relevancia:** El ítem es esencial, pertinente y de alto valor para los objetivos de la investigación.
3. **Coherencia:** El ítem guarda relación lógica, unívoca y directa con la variable e indicador que pretende medir.
4. **Claridad:** La redacción es comprensible, precisa, sin ambigüedades terminológicas y con sintaxis adecuada.
5. **Redacción:** Cumple con las normas gramaticales, ortográficas y de estilo técnico académico.

### 1.2. Escala de Calificación Ordinal
- `1 = Deficiente / No cumple`
- `2 = Regular / Requiere modificaciones sustanciales`
- `3 = Bueno / Aceptable con modificaciones menores`
- `4 = Excelente / Cumple plenamente sin observaciones`

### 1.3. Dicotomización y Cuantificación de Acuerdos Faborables
Sea $X_{ijk}$ la calificación otorgada por el juez experto $j$ ($j = 1, \dots, N$) al ítem $i$ ($i = 1, \dots, M$) en el criterio $k$ ($k = 1, \dots, 5$).

La puntuación binaria de acuerdo favorable $c_{ijk}$ se define como:
$$c_{ijk} = \begin{cases} 1 & \text{si } X_{ijk} \ge 3 \text{ (Calificación 3 o 4)} \\ 0 & \text{si } X_{ijk} \le 2 \text{ (Calificación 1 o 2)} \end{cases}$$

---

## 2. Fórmulas de Cálculo del Índice de Validez de Contenido (IVC)

### 2.1. IVC por Criterio en cada Ítem ($IVC_{ik}$)
$$IVC_{ik} = \frac{\sum_{j=1}^{N} c_{ijk}}{N}$$
Para un panel de $N = 3$ jueces expertos, los valores posibles de $IVC_{ik}$ son:
- $0/3 = 0.00$ (0 acuerdos favorables)
- $1/3 = 0.33$ (1 acuerdo favorable)
- $2/3 = 0.67$ (2 acuerdos favorables)
- $3/3 = 1.00$ (3 acuerdos favorables, unanimidad)

### 2.2. IVC Promedio del Ítem ($IVC_i$)
El índice de validez de contenido de cada reactivo corresponde a la media aritmética de los 5 criterios:
$$IVC_i = \frac{1}{5} \sum_{k=1}^{5} IVC_{ik} = \frac{IVC_{i,\text{Suf}} + IVC_{i,\text{Rel}} + IVC_{i,\text{Coh}} + IVC_{i,\text{Cla}} + IVC_{i,\text{Red}}}{5}$$

### 2.3. IVC Global del Instrumento ($IVC_{total}$)
El índice de validez global del instrumento es el promedio de los $IVC_i$ de los $M$ reactivos:
$$IVC_{total} = \frac{1}{M} \sum_{i=1}^{M} IVC_i$$

---

## 3. Criterios de Decisión y Baremos según Tristán-López (2008)

Para un panel de $N = 3$ expertos evaluadores:
- **Umbral Crítico Mínimo Aceptable por Criterio/Ítem:**
  $$IVC \ge 0.58$$
  Como los valores posibles para $N=3$ son $\{0.00, 0.33, 0.67, 1.00\}$, la condición $IVC \ge 0.58$ exige matemáticamente que **al menos 2 de los 3 expertos califiquen con puntaje 3 o 4** ($IVC = 0.67$ o $1.00$).
- **Regla de Decisión por Ítem:**
  - $IVC_i \ge 0.80$: **Excelente validez.** Se mantiene el ítem sin modificaciones.
  - $0.58 \le IVC_i < 0.80$: **Aceptable.** Requiere ajustes menores sugeridos por los expertos.
  - $IVC_i < 0.58$: **Deficiente.** El ítem debe descartarse o reescribirse íntegramente.
- **Regla de Decisión Global del Instrumento ($IVC_{total}$):**
  - $IVC_{total} \ge 0.90$: **Excelente validez de contenido.** Aplicable sin modificaciones.
  - $0.80 \le IVC_{total} < 0.90$: **Buena validez de contenido.** Aplicable con ajustes menores.
  - $IVC_{total} < 0.80$: **Validez insuficiente.** Requiere reformulación del instrumento.

---

## 4. Matriz Automatizada de Excel (`PUNTUACION IVC.xlsx`)

La estructura de la hoja de cálculo institucional replicada de `ejemplo_validacion/PUNTUACION IVC.xlsx` se modela mediante `openpyxl` con las siguientes fórmulas nativas:

### 4.1. Arquitectura de Columnas en Hoja 1: `PUNTUACIÓN`
| Columna | Campo | Descripción |
|---|---|---|
| A | `N°` | Número correlativo del ítem (1 a $M$) |
| B | `ENUNCIADO` | Texto literal del ítem o indicador |
| C, D, E | `Juez 1`, `Juez 2`, `Juez 3` | Calificación bruta (1-4) en Suficiencia |
| F, G, H | `Juez 1`, `Juez 2`, `Juez 3` | Calificación bruta (1-4) en Relevancia |
| I, J, K | `Juez 1`, `Juez 2`, `Juez 3` | Calificación bruta (1-4) en Coherencia |
| L, M, N | `Juez 1`, `Juez 2`, `Juez 3` | Calificación bruta (1-4) en Claridad |
| O, P, Q | `Juez 1`, `Juez 2`, `Juez 3` | Calificación bruta (1-4) en Redacción |
| R a V | `Acuerdos J1..J3` | Fórmulas binarias: `=IF(C3>=3,1,0)` |
| W a AA | `Suma Acuerdos` | `=SUM(R3:T3)` por cada criterio |
| AB a AF | `IVC Criterio` | `=W3/3` por cada criterio |
| AG | `IVC_Item` | Promedio del ítem: `=AVERAGE(AB3:AF3)` |
| AH | `Decisión` | `=IF(AG3>=0.8,"VÁLIDO",IF(AG3>=0.58,"MODIFICAR","DESCARTAR"))` |

### 4.2. Hoja 2: `RESUMEN GLOBAL`
- Fila de Criterio: Promedio de Suficiencia, Relevancia, Coherencia, Claridad y Redacción.
- Casilla Destacada: `IVC_TOTAL = AVERAGE(AG3:AG[M+2])`.
- Veredicto Institucional: `=IF(B10>=0.8,"INSTRUMENTO APLICABLE Y VÁLIDO","NO APLICABLE")`.

---

## 5. Medición Complementaria: Coeficiente V de Aiken

Para contrastar con la literatura nacional (Escurra, 1988), se calcula la V de Aiken sobre una escala politómica de 1 a 4 ($c = 4$):
$$V = \frac{S}{n \cdot (c - 1)} = \frac{\sum (X_j - 1)}{N \cdot (4 - 1)} = \frac{\sum (X_j - 1)}{3 \times 3} = \frac{\sum (X_j - 1)}{9}$$
- Rango de $V$: $[0, 1]$.
- Intervalo de confianza de Penfield & Giacobbi (2004) al 95%:
  $$L = \frac{2 n k V + Z^2 - 1 - Z \sqrt{Z^2 - 2 - \frac{1}{n k} + 4 n k V (1 - V)}}{2 (n k + Z^2)}$$
- Criterio de significancia estadística: El límite inferior $L \ge 0.50$ con $p < .05$.

---

## 6. Confiabilidad Psicométrica: Alfa de Cronbach

Para el Instrumento 3 (Cuestionario TAM de 10 ítems):
$$\alpha = \frac{K}{K - 1} \left( 1 - \frac{\sum_{i=1}^{K} s_i^2}{s_t^2} \right)$$
Donde:
- $K = 10$ (número de reactivos).
- $s_i^2$: Varianza de las puntuaciones en el ítem $i$.
- $s_t^2$: Varianza del puntaje total del cuestionario.

### Baremo de Confiabilidad (George & Mallery, 2003):
- $\alpha \ge 0.90$: **Excelente.**
- $0.80 \le \alpha < 0.90$: **Buena** (Estándar meta para SIVAC).
- $0.70 \le \alpha < 0.80$: **Aceptable.**
- $0.60 \le \alpha < 0.70$: **Cuestionable.**
- $\alpha < 0.60$: **Inaceptable.**
