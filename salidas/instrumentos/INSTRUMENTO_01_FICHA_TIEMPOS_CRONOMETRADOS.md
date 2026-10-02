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
version: 2.0_definitiva_blindada
fecha: 2026-10-01
---

# UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS
## FACULTAD DE INGENIERÍA — ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

---

### INSTRUMENTO DE RECOLECCIÓN DE DATOS N° 01
## FICHA DE OBSERVACIÓN SISTEMÁTICA Y MEDICIÓN DE TIEMPOS CRONOMETRADOS

**Proyecto de Investigación:**  
*APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II*

* **Tesista:** Bach. José Luis Quispe León  
* **Asesora:** Dra. Norma Lorena Catacora Flores  
* **Variable Evaluada:** Gestión de movimientos de vacunas (Variable Dependiente)  
* **Dimensión:** Oportunidad de procesamiento  
* **Técnica:** Observación sistemática directa  
* **Instrumento:** Ficha de medición de tiempos cronometrados  

---

### 1. DATOS GENERALES DE LA OBSERVACIÓN

| Campo | Registro / Información |
|---|---|
| **Código del Participante / Operador:** | `TRAB-____` (Rango: TRAB-01 a TRAB-14) |
| **Rol Institucional:** | [  ] Responsable de Centro de Acopio / Red de Frío<br>[  ] Personal de Estrategia Sanitaria de Inmunizaciones |
| **Centro de Acopio / Sede:** | ____________________________________________________________________ |
| **Microred de Salud / Red:** | __________________________________ Provincia: Andahuaylas [  ] / Chincheros [  ] |
| **Momento de Medición:** | [  ] **PRETEST** (Gestión manual, kardex físico y hojas Excel dispersas)<br>[  ] **POSTEST** (Gestión automatizada mediante módulos web de SIVAC) |
| **Fecha de la Observación:** | ______ / ______ / 2025 |
| **Observador / Evaluador:** | Bach. José Luis Quispe León (Tesista EPIS-UNAJMA) |

---

### 2. PROTOCOLO DE CRONOMETRAJE Y ESTANDARIZACIÓN OPERATIVA

1. **Instrumento de Medición:** Cronómetro digital calibrado con precisión de centésimas de segundo ($0.01 \text{ s}$).
2. **Unidad de Medida Oficial:** Minutos decimales ($\text{min} = \text{minutos} + \frac{\text{segundos}}{60}$).
3. **Regla de Exclusión de Interrupciones:** El cronómetro se pausa ante factores externos fortuitos ajenos al proceso de digitación/sistema (llamadas de emergencia, cortes de energía eléctrica, consultas de pacientes presenciales). Se registra el tiempo neto efectivo de operación.
4. **Estandarización de la Tarea:** La medición se realiza sobre operaciones estandarizadas de carga transaccional equivalente entre pretest y postest.

---

### 3. SECCIÓN A: MEDICIÓN DEL TIEMPO DE REGISTRO DE MOVIMIENTOS ($T_{reg}$)

**Definición Operacional:** Intervalo de tiempo transcurrido desde que el responsable inicia el ingreso de los datos de un movimiento de vacunas (ingreso por remesa o egreso por distribución a puesto de salud) hasta que la transacción queda asentada, balanceada y disponible en el registro oficial.

**Fórmula Matemática:**
$$T_{reg} = t_{\text{fin\_registro}} - t_{\text{inicio\_registro}}$$

#### Matriz de Observación Cronométrica de Registros:

| N° Obs. | Tipo de Movimiento | Vacuna / Biológico | N° de Lote | N° de Dosis / Viales | Hora Inicio (hh:mm:ss) | Hora Fin (hh:mm:ss) | Tiempo Neto (min : s) | $T_{reg}$ (Minutos Decimales) | Incidencias / Observaciones |
|:---:|:---:|---|---|:---:|:---:|:---:|:---:|:---:|---|
| **01** | [ ] Entrada [ ] Salida | | | | ___:___:___ | ___:___:___ | ___ min ___ s | **_________ min** | |
| **02** | [ ] Entrada [ ] Salida | | | | ___:___:___ | ___:___:___ | ___ min ___ s | **_________ min** | |
| **03** | [ ] Entrada [ ] Salida | | | | ___:___:___ | ___:___:___ | ___ min ___ s | **_________ min** | |
| **04** | [ ] Entrada [ ] Salida | | | | ___:___:___ | ___:___:___ | ___ min ___ s | **_________ min** | |
| **05** | [ ] Entrada [ ] Salida | | | | ___:___:___ | ___:___:___ | ___ min ___ s | **_________ min** | |

$$\text{Tiempo Promedio de Registro del Participante } (\bar{T}_{reg}) = \frac{\sum_{i=1}^{k} T_{reg\_i}}{k} = \mathbf{____________ \text{ min}}$$

---

### 4. SECCIÓN B: MEDICIÓN DEL TIEMPO DE EMISIÓN DE VALES DE ENTREGA ($T_{vale}$)

**Definición Operacional:** Intervalo de tiempo transcurrido desde que el responsable inicia la formulación y cálculo de un despacho de vacunas para un establecimiento de salud hasta que el comprobante de salida / vale oficial de entrega queda formalmente emitido, descargado o impreso con su numeración oficial correlativa.

**Fórmula Matemática:**
$$T_{vale} = t_{\text{emision\_documento}} - t_{\text{inicio\_solicitud}}$$

#### Matriz de Observación Cronométrica de Vales:

| N° Obs. | N° de Vale / PECOSA | Establecimiento de Salud Destino | Cantidad de Ítems / Vacunas en Vale | Hora Inicio (hh:mm:ss) | Hora Fin (hh:mm:ss) | Tiempo Neto (min : s) | $T_{vale}$ (Minutos Decimales) | Incidencias / Observaciones |
|:---:|:---:|---|:---:|:---:|:---:|:---:|:---:|---|
| **01** | Vale N°: ________ | | | ___:___:___ | ___:___:___ | ___ min ___ s | **_________ min** | |
| **02** | Vale N°: ________ | | | ___:___:___ | ___:___:___ | ___ min ___ s | **_________ min** | |
| **03** | Vale N°: ________ | | | ___:___:___ | ___:___:___ | ___ min ___ s | **_________ min** | |

$$\text{Tiempo Promedio de Emisión de Vales del Participante } (\bar{T}_{vale}) = \frac{\sum_{j=1}^{m} T_{vale\_j}}{m} = \mathbf{____________ \text{ min}}$$

---

### 5. RESUMEN DE CONFORMIDAD DE LA MEDICIÓN

* **Tiempo Promedio de Registro ($\bar{T}_{reg}$):** ____________ minutos.
* **Tiempo Promedio de Emisión de Vales ($\bar{T}_{vale}$):** ____________ minutos.

**Firma del Observador / Tesista:** ______________________________________  
**Firma / V°B° del Operador Observado:** ______________________________________  
