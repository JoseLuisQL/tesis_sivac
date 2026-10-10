---
name: formato-instrumentos-validacion
description: Plantillas, matrices psicométricas y procedimientos para diseño de instrumentos y validación por juicio de expertos según el modelo oficial del Dr. Enrique Cóndor Tinoco (EPIS-UNAJMA).
---

# FORMATO DE INSTRUMENTOS Y VALIDACIÓN POR JUICIO DE EXPERTOS — UNAJMA (EPIS)

> **Modelo Institucional Aplicado:** Guía Metodológica de Validación Psicométrica del Dr. Enrique Edgardo Cóndor Tinoco (Docente EPIS-UNAJMA), estructurada en `ejemplo_validacion/`, basada en Lawshe (1975), Tristán-López (2008) y Polit & Beck (2007).

---

## 1. Instrumentos de Recolección de Datos (3 Dimensiones — DEC-007)

El sistema SIVAC requiere tres instrumentos especializados diseñados para medir de forma independiente las 3 dimensiones oficiales de la Variable Dependiente:

### Instrumento 1: Ficha de Registro Cronométrico (Dimensión 1: Oportunidad de Procesamiento)
- **Técnica:** Observación sistemática estructurada no participante.
- **Unidad de Análisis:** Transacciones de movimiento de biológicos (entradas y salidas) ejecutadas por el personal de inmunizaciones ($n=14$).
- **Indicadores Medidos:**
  1. *Tiempo de registro de movimientos ($T_{reg}$):* Minutos transcurridos desde la recepción de la vacuna física hasta el asentamiento completo del movimiento en el sistema o libro.
  2. *Tiempo de emisión de vales de pedido / PECOSA ($T_{vale}$):* Minutos requeridos para elaborar, verificar saldos, imprimir y autorizar el vale de egreso de vacunas.
- **Estructura del Formato:** Columnas para N° de Operación, Fecha/Hora, Tipo de Movimiento (Ingreso/Egreso), Tipo de Biológico, Lote, Hora Inicio, Hora Fin, Tiempo Total (minutos) y Firma del Observador.

### Instrumento 2: Ficha de Registro Documental de Lotes (Dimensión 2: Consistencia Documental)
- **Técnica:** Análisis documental y auditoría de inventario físico vs registros.
- **Unidad de Análisis:** Registros de movimientos en kardex y actas de entrega/recepción.
- **Indicadores Medidos:**
  1. *Porcentaje de registros sin discrepancias ($RSD$):*
     $$RSD = \left( \frac{\text{Registros con saldo físico idéntico al documental}}{\text{Total de registros auditados}} \right) \times 100$$
  2. *Porcentaje de concordancia programada vs entregada ($CPE$):*
     $$CPE = \left( \frac{\text{Cantidad entregada}}{\text{Cantidad programada}} \right) \times 100$$
- **Estructura del Formato:** Columnas para Código de Auditoría, Fecha, Nombre de la Vacuna, Lote, Saldo Físico, Saldo Documental, Discrepancia Detectada (Sí/No), Tipo de Error (Omisión, Transcripción, Cálculo) y Observaciones.

### Instrumento 3: Cuestionario de Satisfacción del Usuario — Modelo TAM (Dimensión 3: Satisfacción)
- **Técnica:** Encuesta estructurada autoadministrada.
- **Población Objetivo:** Personal de inmunizaciones y cadena de frío de la DISA Apurímac II ($N=n=14$).
- **Escala Psicométrica:** Escala Likert de 5 puntos:
  - `1 = Totalmente en desacuerdo`
  - `2 = En desacuerdo`
  - `3 = Ni de acuerdo ni en desacuerdo (Neutral)`
  - `4 = De acuerdo`
  - `5 = Totalmente de acuerdo`
- **Reactivos (10 ítems balanceados):**
  - *Subdimensión A: Aceptación del Proceso (AP) — 5 ítems:* Fluidez en la operación, claridad en los pasos de registro, reducción de carga mental, adaptabilidad al flujo de trabajo y percepción de modernización del servicio.
  - *Subdimensión B: Utilidad Percibida (UP) — 5 ítems:* Facilidad para localizar lotes y vencimientos, agilidad en la generación de reportes, precisión en el control de existencias, soporte efectivo a la toma de decisiones y recomendación global de la herramienta.

---

## 2. Protocolo Oficial de Juicio de Expertos (Dr. Cóndor Tinoco)

### 2.1. Composición del Panel de Expertos
- Se requiere un panel de **tres (03) expertos** independientes con grado de Magíster o Doctor en Ingeniería de Sistemas, Informática o Gestión Tecnológica, con colegiatura vigente en el Colegio de Ingenieros del Perú (CIP).

### 2.2. Los Cinco (5) Criterios Psicométricos por Ítem
Cada experto evalúa cada ítem del instrumento bajo 5 criterios independientes:
1. **Suficiencia:** Los ítems propuestos bastan para medir integralmente la dimensión y sus indicadores.
2. **Relevancia:** El ítem es esencial, pertinente y de alto valor para los objetivos de la investigación.
3. **Coherencia:** El ítem guarda relación lógica, unívoca y directa con la variable e indicador que pretende medir.
4. **Claridad:** La redacción es comprensible, precisa, sin ambigüedades terminológicas y con sintaxis adecuada.
5. **Redacción:** Cumple con las normas gramaticales, ortográficas y de estilo técnico académico.

### 2.3. Escala de Calificación Ordinal y Dicotomización Binaria
- **Escala Ordinal:**
  - `1 = Deficiente / No cumple`
  - `2 = Regular / Requiere modificaciones sustanciales`
  - `3 = Bueno / Aceptable con modificaciones menores`
  - `4 = Excelente / Cumple plenamente sin observaciones`
- **Dicotomización Binaria ($c_{ijk}$):**
  $$c_{ijk} = \begin{cases} 1 & \text{si calificación } \ge 3 \text{ (Acuerdo favorable)} \\ 0 & \text{si calificación } \le 2 \text{ (Acuerdo desfavorable)} \end{cases}$$

### 2.4. Fórmulas de Cálculo del Índice de Validez de Contenido (IVC)
1. **IVC por Criterio en el Ítem $i$ ($IVC_{ik}$):**
   $$IVC_{ik} = \frac{\sum_{j=1}^{N} c_{ijk}}{N}$$
   Donde $N = 3$ (número de expertos) y $c_{ijk}$ es la calificación binaria del juez $j$ en el criterio $k$.
2. **IVC Promedio del Ítem $i$ ($IVC_i$):**
   $$IVC_i = \frac{\sum_{k=1}^{5} IVC_{ik}}{5}$$
3. **IVC Global del Instrumento ($IVC_{total}$):**
   $$IVC_{total} = \frac{\sum_{i=1}^{M} IVC_i}{M}$$
   Donde $M$ es el número total de ítems del instrumento.

### 2.5. Baremos y Umbrales de Decisión según Tristán-López (2008)
- Para $N = 3$ expertos evaluadores:
  - **Umbral crítico mínimo:** $IVC \ge 0.58$.
  - Como el cociente para 3 jueces toma valores discretos ($0/3 = 0.00$, $1/3 = 0.33$, $2/3 = 0.67$, $3/3 = 1.00$), la condición $IVC \ge 0.58$ exige que **al menos 2 de los 3 expertos califiquen favorablemente** ($IVC = 0.67$ o $1.00$).
  - Si $IVC_i \le 0.33$: El ítem queda descartado o debe reformularse íntegramente.
  - **Umbral institucional global ($IVC_{total}$):**
    - $IVC_{total} \ge 0.80$: **Válido y aplicable** según estándar UNAJMA.
    - $IVC_{total} \ge 0.90$: **Excelente validez de contenido.**

---

## 3. Estructura del Expediente Oficial de Validación

El expediente completo que se somete a cada juez evaluador contiene 6 piezas documentales articuladas:

1. **Carta Oficial de Presentación al Experto:**
   - Membrete institucional con banner oficial UNAJMA (1212x128 px).
   - Dirigida nominalmente a cada ingeniero evaluador.
   - Especifica el título oficial de la tesis, los objetivos, la población de estudio y la solicitud formal de su dictamen profesional.
2. **Ficha Técnica y Matriz de Operacionalización de Variables:**
   - Define formalmente la Variable Independiente, la Variable Dependiente y sus 3 dimensiones (DEC-007).
3. **Matriz de Evaluación por Ítem (Formato 8 Columnas):**
   - Columnas: N° Ítem, Enunciado / Reactivo, Suficiencia (1-4), Relevancia (1-4), Coherencia (1-4), Claridad (1-4), Redacción (1-4) y Sugerencias de Modificación.
4. **Matriz Automatizada de Excel (`PUNTUACION IVC.xlsx`):**
   - Hoja 1: Registro de calificaciones brutas (1-4) por experto, matriz binaria automática con fórmulas `=IF(C3>=3,1,0)`, suma de acuerdos favorables `=SUM(J3:L3)` y cálculo de IVC `=M3/3`.
   - Hoja 2: Resumen consolidado con el promedio global del instrumento.
5. **Constancia Oficial de Validación de Contenido:**
   - Formato institucional de la EPIS-UNAJMA.
   - Declaración expresa de que el instrumento ha sido evaluado bajo los 5 criterios psicométricos.
   - Cuadro resumen de calificaciones por criterio.
   - Casilla de veredicto con tres opciones excluyentes:
     - `[X] Aplicable sin modificación`
     - `[ ] Aplicable con modificaciones menores`
     - `[ ] No aplicable`
   - Lugar y fecha: *Andahuaylas, [mes] de 2025/2026*.
   - Espacio formal para firma manuscrita, sello de posgrado (Magíster/Doctor) y número de colegiatura del Colegio de Ingenieros del Perú (CIP).
6. **Muestra Digital del Instrumento:**
   - Copia limpia del cuestionario o ficha de observación con escudo UNAJMA, instrucciones éticas y formato de respuesta.
