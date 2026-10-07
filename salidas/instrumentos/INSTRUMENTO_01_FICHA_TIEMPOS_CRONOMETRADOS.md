---
tipo: instrumento_oficial_unajma
numero: 01
nombre: Ficha de Observación Sistemática y Medición de Tiempos Cronometrados
variable: Gestión de movimientos de vacunas (VD)
dimension: Oportunidad de procesamiento
indicadores:
  - Ind 1.1: Tiempo de registro de movimiento de vacunas (T_reg)
  - Ind 1.2: Tiempo de emisión de vale oficial de entrega (T_vale)
unidad_medida: Minutos y segundos (convertido a minutos decimales)
escala: Razón / Cuantitativa continua
institucion: Universidad Nacional José María Arguedas (UNAJMA)
facultad: Facultad de Ingeniería - Escuela Profesional de Ingeniería de Sistemas
autor: Bach. José Luis Quispe León
asesora: Dra. Norma Lorena Catacora Flores
version: 3.0_pmmv_blindada
fecha: 2026-10-02
---

# UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS
## FACULTAD DE INGENIERÍA — ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

---

### INSTRUMENTO DE RECOLECCIÓN DE DATOS N° 01
## FICHA DE OBSERVACIÓN SISTEMÁTICA Y MEDICIÓN DE TIEMPOS CRONOMETRADOS
**Protocolo Estandarizado de Medición PMMV y Blindaje Metodológico Anti-Pseudorreplicación**

**Proyecto de Investigación:**  
*APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II*

* **Tesista:** Bach. José Luis Quispe León  
* **Asesora:** Dra. Norma Lorena Catacora Flores  
* **Variable Evaluada:** Gestión de movimientos de vacunas (Variable Dependiente)  
* **Dimensión Oficial (DEC-007):** Oportunidad de procesamiento  
* **Técnica:** Observación sistemática estructurada directa no participante  
* **Instrumento:** Ficha de registro de tiempos cronometrados  
* **Población / Muestra:** Censal, conformada por $N = n = 14$ operadores de inmunizaciones  

---

### 1. DATOS GENERALES DE LA OBSERVACIÓN

| Campo | Registro / Información |
|---|---|
| **Código del Operador Evaluado:** | `TRAB-____` (Rango: TRAB-01 a TRAB-14) |
| **Rol Institucional:** | [  ] Responsable de Centro de Acopio / Red de Frío<br>[  ] Personal de Estrategia Sanitaria de Inmunizaciones |
| **Centro de Acopio / Sede:** | ____________________________________________________________________ |
| **Red / Microred de Salud:** | __________________________________ Provincia: Andahuaylas [  ] / Chincheros [  ] |
| **Momento de Medición:** | [  ] **PRETEST** ($O_1$: Kardex físico manual, libros de registro y hojas Excel dispersas)<br>[  ] **POSTEST** ($O_2$: Sistema web SIVAC - Arquitectura Laravel/MySQL) |
| **Fecha de la Observación:** | ______ / ______ / 2025 |
| **Evaluador Principal:** | Bach. José Luis Quispe León (Tesista EPIS-UNAJMA) |
| **Evaluador Secundario (si aplica):** | ____________________________________________________________________ |

---

### 2. PROTOCOLO DE CRONOMETRAJE Y ESTANDARIZACIÓN OPERATIVA (PMMV)

1. **Aparato de Medición:** Cronómetro digital calibrado con precisión de centésimas de segundo ($0.01 \text{ s}$).
2. **Unidad de Medida Oficial:** Minutos decimales, calculados con cuatro cifras significativas:
   $$\text{Tiempo en minutos decimales} = \text{minutos enteros} + \frac{\text{segundos}}{60}$$
3. **Puntos de Corte Operativo (Triggers de Inicio y Parada):**
   * **Tiempo de Registro ($T_{reg}$):**  
     - *Inicio ($t_0$):* Momento exacto en que el operador toma físicamente el documento fuente (guía/pecosa/remesa) o abre la interfaz para iniciar la digitación de los campos del movimiento.  
     - *Fin ($t_f$):* Momento en que el movimiento queda grabado, confirmado en la base de datos o asentado con saldo actualizado en el libro oficial.
   * **Tiempo de Emisión de Vales ($T_{vale}$):**  
     - *Inicio ($t_0$):* Momento en que el operador recibe o apertura la solicitud de pedido de biológicos para su despacho a un establecimiento de salud.  
     - *Fin ($t_f$):* Momento en que el comprobante de salida / vale oficial queda generado, visualizado, firmado digitalmente o impreso en PDF con numeración correlativa.
4. **Regla de Pausa por Factores Externos Fortuitos:** Si ocurre una interrupción imprevista no atribuible al flujo operativo del proceso evaluado (corte de energía eléctrica, sismo, llamada de emergencia sanitaria o atención médica no programada), el cronómetro se detiene. Se reanuda al normalizarse la tarea, registrando estrictamente el tiempo neto efectivo de trabajo del operador.

---

### 3. BATERÍA ESTANDARIZADA DE TAREAS Y TRATAMIENTO ANTI-PSEUDORREPLICACIÓN

#### 3.1. Batería Estandarizada del PMMV (3 Tareas por Indicador)
Para asegurar comparabilidad y control experimental riguroso entre pretest y postest, cada uno de los 14 operadores ejecuta obligatoriamente una batería estandarizada de **tres (3) tareas de registro ($T_{reg}$)** y **tres (3) tareas de emisión de vales ($T_{vale}$)**:

* **Tareas Estandarizadas de Registro ($T_{reg}$):**
  * **Tarea REG-01 (Movimiento Simple de Ingreso):** Registro de remesa nacional de 1 biológico (lote único, verificación de fecha de vencimiento y dosis totales).
  * **Tarea REG-02 (Movimiento Regular de Salida / Distribución):** Registro de despacho programado conteniendo 2 a 3 tipos de vacunas hacia un centro de salud.
  * **Tarea REG-03 (Movimiento Complejo / Redistribución):** Registro de transferencia o ajuste multibioplástico (4 a 6 ítems incluyendo jeringas y diluyentes con verificación de saldos).

* **Tareas Estandarizadas de Emisión de Vales ($T_{vale}$):**
  * **Tarea VALE-01 (Vale Simple):** Elaboración y emisión de comprobante de salida para Puesto de Salud nivel I-1/I-2 (1 a 2 ítems de vacunas).
  * **Tarea VALE-02 (Vale Regular):** Elaboración y emisión de comprobante de salida para Centro de Salud nivel I-3/I-4 (3 a 5 ítems de vacunas con insumos).
  * **Tarea VALE-03 (Vale de Emergencia / Contingencia):** Emisión prioritaria por contingencia de cadena de frío o barrido vacunal con verificación de lotes y firmas.

#### 3.2. Fundamento Bioestadístico Anti-Pseudorreplicación (Hurlbert, 1984)
* En un diseño preexperimental de medidas repetidas en un solo grupo ($O_1 \longrightarrow X \longrightarrow O_2$) con población censal ($n=14$), las tres mediciones por trabajador representan **réplicas técnicas intrasujeto** destinadas a minimizar la varianza de medición del operador, y **NO constituyen unidades muestrales independientes**.
* Tratar cada una de las 3 mediciones como unidad de análisis ($3 \times 14 = 42$ observaciones) constituiría un caso flagrante de **pseudorreplicación simple** (Hurlbert, 1984), que inflaría artificialmente los grados de libertad ($df$) y reduciría espuriamente el error estándar, aumentando inaceptablemente el riesgo de cometer un **Error de Tipo I** (falso positivo).
* **Regla de Agregación Obligatoria:** Para el análisis inferencial, los tres registros de cada participante se consolidan mediante su promedio aritmético ($\bar{T}_i$) o su mediana ($\tilde{T}_i$), produciendo exactamente **un único valor representativo por trabajador en pretest y un único valor en postest ($n = 14$ pares pareados)**:
  $$\bar{T}_{reg\_i} = \frac{1}{3} \sum_{k=1}^{3} T_{reg\_i, k} \qquad \bar{T}_{vale\_i} = \frac{1}{3} \sum_{k=1}^{3} T_{vale\_i, k}$$
* Estos $n=14$ pares emparejados alimentan directamente la prueba no paramétrica de rangos con signo de Wilcoxon (o la prueba t de Student para muestras relacionadas si se comprueba el supuesto de normalidad mediante Shapiro-Wilk, $p > 0.05$).

---

### 4. SECCIÓN A: MEDICIÓN DEL TIEMPO DE REGISTRO DE MOVIMIENTOS ($T_{reg}$)

**Definición Operacional:** Tiempo requerido por el operador para ingresar, validar y asentar un movimiento de vacunas en el sistema o registro formal.

$$\text{Fórmula: } T_{reg} = t_{\text{fin\_registro}} - t_{\text{inicio\_registro}}$$

#### Matriz Cronométrica de Registro ($T_{reg}$):

| N° Tarea | Código de Tarea | Descripción del Movimiento Estandarizado | Biológicos / Lotes Auditados | N° Total Dosis | Hora Inicio (hh:mm:ss.cc) | Hora Fin (hh:mm:ss.cc) | Tiempo Neto (min : s) | $T_{reg}$ (Minutos Decimales) | Incidencias / Observaciones |
|:---:|:---:|---|---|:---:|:---:|:---:|:---:|:---:|---|
| **1** | **REG-01** | Ingreso simple de remesa (1 biológico) | | | ___:___:___.___ | ___:___:___.___ | ___ min ___ s | **_________ min** | |
| **2** | **REG-02** | Salida regular programada (2 a 3 vacunas) | | | ___:___:___.___ | ___:___:___.___ | ___ min ___ s | **_________ min** | |
| **3** | **REG-03** | Redistribución / Despacho multibioplástico (4 a 6 ítems) | | | ___:___:___.___ | ___:___:___.___ | ___ min ___ s | **_________ min** | |

$$\mathbf{\text{Tiempo Representativo Agregado del Operador }} (\bar{T}_{reg\_i}) = \frac{T_{reg\_1} + T_{reg\_2} + T_{reg\_3}}{3} = \mathbf{____________ \text{ min}}$$

$$\text{Mediana Intrasujeto } (\tilde{T}_{reg\_i}) = \text{Mediana}(T_{reg\_1}, T_{reg\_2}, T_{reg\_3}) = \mathbf{____________ \text{ min}}$$

---

### 5. SECCIÓN B: MEDICIÓN DEL TIEMPO DE EMISIÓN DE VALES OFICIALES ($T_{vale}$)

**Definición Operacional:** Tiempo transcurrido desde la recepción del requerimiento de vacunas hasta la emisión y formalización definitiva del vale de entrega / comprobante de salida.

$$\text{Fórmula: } T_{vale} = t_{\text{emision\_documento}} - t_{\text{inicio\_solicitud}}$$

#### Matriz Cronométrica de Vales ($T_{vale}$):

| N° Tarea | Código de Tarea | Tipo de Vale Estandarizado | N° Documento / Vale | Cantidad Ítems | Hora Inicio (hh:mm:ss.cc) | Hora Fin (hh:mm:ss.cc) | Tiempo Neto (min : s) | $T_{vale}$ (Minutos Decimales) | Incidencias / Observaciones |
|:---:|:---:|---|---|:---:|:---:|:---:|:---:|:---:|---|
| **1** | **VALE-01** | Vale simple (Puesto I-1/I-2; 1-2 biológicos) | Vale N°: ________ | | ___:___:___.___ | ___:___:___.___ | ___ min ___ s | **_________ min** | |
| **2** | **VALE-02** | Vale regular (Centro I-3/I-4; 3-5 biológicos) | Vale N°: ________ | | ___:___:___.___ | ___:___:___.___ | ___ min ___ s | **_________ min** | |
| **3** | **VALE-03** | Vale de emergencia / reposición urgente | Vale N°: ________ | | ___:___:___.___ | ___:___:___.___ | ___ min ___ s | **_________ min** | |

$$\mathbf{\text{Tiempo Representativo Agregado del Operador }} (\bar{T}_{vale\_i}) = \frac{T_{vale\_1} + T_{vale\_2} + T_{vale\_3}}{3} = \mathbf{____________ \text{ min}}$$

$$\text{Mediana Intrasujeto } (\tilde{T}_{vale\_i}) = \text{Mediana}(T_{vale\_1}, T_{vale\_2}, T_{vale\_3}) = \mathbf{____________ \text{ min}}$$

---

### 6. PROTOCOLO DE CONFIABILIDAD INTEROBSERVADOR (CALIBRACIÓN PREVIA)

Para blindar la confiabilidad instrumental frente a potenciales objeciones de subjetividad en el cronometraje, se aplica un protocolo riguroso de calibración interobservador antes del inicio de la recolección definitiva:

1. **Diseño de la Prueba de Calibración:**
   * Se ejecutan **15 observaciones cronométricas simultáneas e independientes** a ciegas entre dos evaluadores:
     - *Evaluador 1:* Bach. José Luis Quispe León (Investigador principal).
     - *Evaluador 2:* Observador técnico independiente previamente entrenado en los triggers de inicio y parada.
   * Ambos evaluadores se ubican en posiciones visuales que permiten observar la pantalla y los documentos sin comunicarse verbalmente ni observar el cronómetro del otro.
2. **Modelo Matemático: Coeficiente de Correlación Intraclase ICC(2,1):**
   * Se utiliza el modelo de efectos aleatorios bidireccional, acuerdo absoluto, medidas simples según la formulación canónica de Shrout & Fleiss (1979) y las directrices de Koo & Li (2016):
     $$ICC(2,1) = \frac{MS_R - MS_E}{MS_R + (k - 1)MS_E + \frac{k}{n}(MS_C - MS_E)}$$
     Donde:
     - $MS_R$: Cuadrado medio entre filas (sujetos/tareas observadas, $n = 15$).
     - $MS_E$: Cuadrado medio residual de error.
     - $MS_C$: Cuadrado medio entre columnas (jueces/evaluadores, $k = 2$).
3. **Criterios de Aceptación Psicométrica y Tolerancia:**
   * **Umbral de Confiabilidad:** $ICC(2,1) \ge 0.75$ (indica confiabilidad interobservador buena a excelente; Landis & Koch, 1977; Koo & Li, 2016).
   * **Tolerancia de Discrepancia Absoluta:** La diferencia absoluta entre ambos cronómetros en cada observación no debe superar los 5 segundos:
     $$|\Delta t| = |t_{\text{Evaluador 1}} - t_{\text{Evaluador 2}}| < 5 \text{ segundos} \quad (\approx 0.083 \text{ min})$$
   * **Regla de Contingencia:** Si más de 1 de las 15 observaciones ($> 6.67\%$) presenta $|\Delta t| \ge 5\text{ s}$ o si $ICC(2,1) < 0.75$, se anula la sesión, se revisan los puntos de corte operativo y se repite la ronda de 15 calibraciones hasta alcanzar la convergencia psicométrica requerida.

---

### 7. RESUMEN DE CONFORMIDAD Y FIRMAS

| Indicador | Promedio Agregado del Operador ($\bar{T}_i$) | Mediana Agregada del Operador ($\tilde{T}_i$) |
|---|:---:|:---:|
| **Tiempo de Registro ($T_{reg}$):** | **____________ minutos** | **____________ minutos** |
| **Tiempo de Emisión de Vales ($T_{vale}$):** | **____________ minutos** | **____________ minutos** |

Declaración de conformidad: Se certifica que la presente toma de tiempos se llevó a cabo respetando los puntos de inicio y finalización del protocolo PMMV, garantizando la fidelidad y veracidad de los datos registrados.

---

**Firma del Investigador / Evaluador:**  
Bach. José Luis Quispe León  
DNI: ________________________  
Tesista EPIS — UNAJMA  

**V°B° del Operador Observado:**  
Nombre: ______________________________________  
DNI: ________________________  
Cargo: ______________________________________  
Sede / Centro de Acopio: ________________________  
