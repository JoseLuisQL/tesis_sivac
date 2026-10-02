---
tipo: operacionalizacion_variables
fase: F2
fecha: 2026-10-01
version: 2.1_definitiva_limpia
dimensiones_oficiales: oportunidad_procesamiento, consistencia_documental, satisfaccion_usuario
guardian: guardian-consistencia
director: director-general
estado: definitivo_aprobado
---

# MATRIZ DE OPERACIONALIZACIÓN DE VARIABLES DEFINITIVA — SIVAC

> **Proyecto de Tesis:** *APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II*  
> **Tesista / Autor:** Bach. José Luis Quispe León  
> **Asesora:** Dra. Norma Lorena Catacora Flores  
> **Institución:** Universidad Nacional José María Arguedas (UNAJMA)  
> **Facultad:** Facultad de Ingeniería | **Escuela Profesional:** Ingeniería de Sistemas  
> **Propósito:** Definir con rigor metodológico la Variable Independiente (Intervención Tecnológica SIVAC) y la Variable Dependiente (Gestión de movimientos de vacunas) con sus tres dimensiones de estudio, seis indicadores cuantitativos, fórmulas de cálculo, unidades de medida e instrumentos de recolección para la investigación.

---

## 1. Operacionalización de la Variable Independiente (VI)

### 1.1 Definición Conceptual
El **Sistema web SIVAC** (Sistema de Información de Vacunas) es una solución tecnológica integral basada en arquitectura cliente-servidor web, desarrollada mediante la metodología ágil Extreme Programming (XP) en sus cuatro fases (Planificación, Diseño, Codificación y Pruebas) y evaluada bajo el estándar internacional de calidad de producto de software **ISO/IEC 25010:2023**, diseñada específicamente para automatizar, controlar y asegurar la trazabilidad del registro de entradas, salidas, transferencias y emisión de vales de entrega de biológicos en la red de frío de la Dirección de Salud Apurímac II.

### 1.2 Definición Operacional y Naturaleza Metodológica (Tratamiento Experimental)
En el marco de un diseño de investigación **preexperimental con pretest y postest en un solo grupo ($O_1 \longrightarrow X \longrightarrow O_2$)**, la Variable Independiente opera como un **estímulo o intervención tecnológica manipulada por presencia/ausencia**, estructurada en dos condiciones operativas:

1. **Condición Control / Basal ($X_0$ - Pretest):** Gestión tradicional no automatizada sustentada en registros físicos en cuadernos de kardex manual, hojas de balance en papel y archivos de cálculo desarticulados (Excel), propensos a lentitud de cálculo, desgaste físico y errores de transcripción.
2. **Condición Experimental ($X_1$ - Postest):** Gestión automatizada en tiempo real mediante la puesta en producción y adopción del sistema web SIVAC, con validación de reglas de negocio, control transaccional de lotes, balance automático de existencias y generación de vales electrónicos en PDF.

> **Sustento del Tratamiento Experimental:**  
> Las especificaciones técnicas del software (historias de usuario según Extreme Programming y atributos de calidad de producto de software bajo ISO/IEC 25010:2023) corresponden al desarrollo de la solución tecnológica implementada. En el marco del diseño preexperimental, el software actúa como el tratamiento experimental evaluado a través de su impacto en las dimensiones e indicadores de la gestión de movimientos de vacunas.

### 1.3 Matriz de la Variable Independiente (Intervención Tecnológica)

| Variable | Naturaleza Metodológica | Definición Conceptual | Niveles de Manipulación Experimental | Mecanismo de Aplicación / Control | Rol en el Informe de Tesis |
|---|---|---|---|---|---|
| **Variable Independiente (X):**<br>Sistema web SIVAC | Intervención tecnológica / Tratamiento experimental | Plataforma informática web desarrollada bajo Extreme Programming (XP) y estándar ISO/IEC 25010:2023 para automatizar la gestión de biológicos. | • **Nivel 0 ($X_0$ - Pretest):** Proceso manual tradicional (kardex en papel, cuadernos y Excel aislado).<br><br>• **Nivel 1 ($X_1$ - Postest):** Proceso automatizado mediante plataforma SIVAC en red de frío. | • Puesta en producción en servidor web.<br>• Capacitación protocolizada a los 14 trabajadores.<br>• Migración de saldos iniciales y control de acceso por roles. | Núcleo del **Capítulo III** (Metodología XP, arquitectura cliente-servidor, modelado de datos y pruebas funcionales). |

---

## 2. Operacionalización de la Variable Dependiente (VD)

### 2.1 Definición Conceptual
La **Gestión de movimientos de vacunas** es el conjunto estructurado de actividades logísticas, técnicas y administrativas orientadas a programar, registrar, fiscalizar, despachar y conciliar el flujo de ingresos, egresos, mermas, saldos y transferencias de productos biológicos e insumos de vacunación entre el almacén central de la DISA Apurímac II, los centros de acopio y los establecimientos de salud ejecutores, asegurando la oportunidad operativa, la exactitud documental y la integridad de la cadena de frío bajo la normativa técnica del Ministerio de Salud (MINSA).

### 2.2 Definición Operacional
La gestión de movimientos de vacunas se evalúa de manera cuantitativa y comparativa contrastando el estado previo a la intervención ($O_1$) frente al estado posterior a la implementación de SIVAC ($O_2$), a través de las **tres (03) dimensiones de estudio**:
1. **Oportunidad de procesamiento:** Cuantificada objetivamente en minutos decimales mediante observación cronométrica digital estandarizada ($T_{reg}, T_{vale}$).
2. **Consistencia documental:** Cuantificada porcentualmente mediante auditoría de registros y vales oficiales sujeta a una regla estricta de 8 criterios obligatorios de conformidad ($RSD, CPE$).
3. **Satisfacción del usuario:** Cuantificada psicométricamente mediante un cuestionario estructurado en escala Likert de 5 puntos fundamentado en el Modelo de Aceptación Tecnológica (TAM de Fred Davis).

---

### 2.3 Matriz de la Variable Dependiente

| Variable | Definición Conceptual | Dimensiones | Indicadores Oficiales | Fórmula Matemática y Unidad de Medida | Tipo de Variable y Escala | Instrumento de Recolección |
|---|---|---|---|---|---|---|
| **Variable Dependiente (Y):**<br>Gestión de movimientos de vacunas | Proceso técnico-administrativo de control y despacho de biológicos e insumos en la red de frío de la DISA Apurímac II. | **1. Oportunidad de procesamiento** | • **Ind 1.1:** Tiempo de registro de movimiento de vacunas ($T_{reg}$).<br><br>• **Ind 1.2:** Tiempo de emisión de comprobante de salida / vale ($T_{vale}$). | $$T_{reg} = t_{\text{fin\_registro}} - t_{\text{inicio\_registro}}$$<br>*Unidad:* Minutos decimales ($\text{min}$).<br><br>$$T_{vale} = t_{\text{emision}} - t_{\text{inicio\_solicitud}}$$<br>*Unidad:* Minutos decimales ($\text{min}$). | Cuantitativa continua.<br><br>*Escala:* Razón. | **Instrumento N° 01:**<br>Ficha de observación sistemática de tiempos cronometrados (Cronómetro digital estandarizado). |
| | | **2. Consistencia documental** | • **Ind 2.1:** Porcentaje de registros sin discrepancias ($RSD$).<br><br>• **Ind 2.2:** Concordancia entre cantidad programada y cantidad entregada ($CPE$). | $$RSD = \left(\frac{N_{\text{conformes}}}{N_{\text{total}}}\right) \times 100$$<br>*Unidad:* Porcentaje ($\%$).<br><br>$$CPE = \left(\frac{\sum Q_{\text{entregada}}}{\sum Q_{\text{programada}}}\right) \times 100$$<br>*Unidad:* Porcentaje ($\%$). | Cuantitativa continua.<br><br>*Escala:* Razón / Proporción. | **Instrumento N° 02:**<br>Ficha de registro y cotejo documental de la calidad del registro (Auditoría basada en 8 criterios obligatorios de conformidad). |
| | | **3. Satisfacción del usuario** | • **Ind 3.1:** Aceptación del proceso operativo ($AP$).<br><br>• **Ind 3.2:** Utilidad percibida para la gestión sanitaria ($UP$). | Puntuación obtenida mediante suma de reactivos (4 ítems para $AP$ y 4 ítems para $UP$):<br>$$\text{Puntaje Total} = \sum_{i=1}^{8} \text{Ítem}_i$$<br>*Rango:* 8 a 40 puntos.<br>*Unidad:* Puntos en escala psicométrica. | Cuantitativa discreta / Ordinal (Tratamiento intervalar psicométrico).<br><br>*Escala:* Ordinal / Likert (1 a 5). | **Instrumento N° 03:**<br>Cuestionario de satisfacción del usuario y aceptación tecnológica (Modelo TAM). |

---

## 3. Fichas Técnicas Detalladas de los 6 Indicadores de la VD

### Indicador 1.1: Tiempo de Registro de Movimiento de Vacunas ($T_{reg}$)
* **Dimensión:** Oportunidad de procesamiento.
* **Definición Operativa:** Lapso temporal neto en minutos transcurrido desde que el operador inicia la captura o digitación de los datos de un movimiento de vacunas (entrada, salida o transferencia) hasta que la transacción queda asentada y balanceada formalmente en el kardex institucional.
* **Fórmula:** $T_{reg} = t_{\text{fin\_registro}} - t_{\text{inicio\_registro}}$.
* **Unidad de Medida:** Minutos decimales ($\text{min} = \text{minutos} + \frac{\text{segundos}}{60}$).
* **Instrumento:** Ficha de observación cronométrica N° 01 (Sección A).
* **Protocolo de Medición:** Cronometraje digital estandarizado de 5 observaciones por participante, excluyendo interrupciones externas fortuitas.
* **Tendencia Esperada:** Reducción sustancial del tiempo medio de registro entre pretest ($X_0$) y postest ($X_1$).

---

### Indicador 1.2: Tiempo de Emisión de Comprobante de Salida / Vale ($T_{vale}$)
* **Dimensión:** Oportunidad de procesamiento.
* **Definición Operativa:** Tiempo en minutos requerido para procesar el requerimiento de biológicos de una microred, verificar lotes disponibles, generar el comprobante oficial de despacho (vale / PECOSA) y formalizar la orden imprimible o en formato PDF.
* **Fórmula:** $T_{vale} = t_{\text{emision\_documento}} - t_{\text{inicio\_solicitud}}$.
* **Unidad de Medida:** Minutos decimales ($\text{min}$).
* **Instrumento:** Ficha de observación cronométrica N° 01 (Sección B).
* **Protocolo de Medición:** Cronometraje digital estandarizado de 3 emisiones de comprobantes por participante.
* **Tendencia Esperada:** Reducción sustancial del tiempo de emisión gracias a la generación automatizada de reportes en PDF por SIVAC.

---

### Indicador 2.1: Porcentaje de Registros sin Discrepancias ($RSD$)
* **Dimensión:** Consistencia documental.
* **Definición Operativa:** Proporción porcentual de movimientos de biológicos auditados en los que la información asentada coincide plenamente con los documentos fuentes y el stock físico real, sin borrones, omisiones ni inconsistencias aritméticas.
* **Fórmula:**
  $$RSD = \left( \frac{\text{Número de Registros Conformes sin Discrepancia}}{\text{Total de Registros Auditados}} \right) \times 100$$
* **Unidad de Medida:** Porcentaje ($\%$).
* **Instrumento:** Ficha de cotejo y registro documental N° 02 (Sección A).
* **Regla Operativa de Decisión (8 Criterios Obligatorios):**
  Un registro es clasificado como **Conforme ($1$)** si y solo si satisface simultáneamente los siguientes 8 criterios de auditoría:
  1. Tipo de movimiento unívocamente tipificado (Entrada, Salida o Transferencia).
  2. Nombre normalizado de la vacuna según esquema oficial MINSA.
  3. Número de lote verificado contra el rótulo físico del frasco.
  4. Cantidad de dosis / viales exacta y coincidente con el documento de entrega.
  5. Fecha completa y cronológicamente consistente (Día, Mes, Año).
  6. Establecimiento de origen o destino plenamente individualizado.
  7. Personal responsable del despacho o recepción plenamente identificado con cargo.
  8. Documento de respaldo oficial asociado (Vale, PECOSA, Guía de Remisión o Acta).
  *Si falla cualquiera de los 8 criterios, el registro se califica como No Conforme ($0$).*
* **Tendencia Esperada:** Incremento significativo de la proporción de registros conformes hacia el 100% en el postest.

---

### Indicador 2.2: Concordancia de Cantidad Programada vs. Entregada ($CPE$)
* **Dimensión:** Consistencia documental.
* **Definición Operativa:** Grado porcentual de correspondencia entre el volumen de biológicos solicitado en los requerimientos mensuales de las microredes y la cantidad efectivamente despachada y sustentada en vales oficiales de entrega.
* **Fórmula:**
  $$CPE = \left( \frac{\text{Cantidad Total de Dosis Entregadas Conformes}}{\text{Cantidad Total de Dosis Programadas en Requerimiento}} \right) \times 100$$
* **Unidad de Medida:** Porcentaje ($\%$).
* **Instrumento:** Ficha de cotejo y registro documental N° 02 (Sección B).
* **Protocolo de Medición:** Auditoría comparativa de una muestra representativa de 10 requerimientos institucionales frente a sus respectivos vales oficiales de salida.
* **Tendencia Esperada:** Incremento en el nivel de concordancia y eliminación de desabastecimientos o sobre-despachos injustificados.

---

### Indicador 3.1: Aceptación del Proceso Operativo ($AP$)
* **Dimensión:** Satisfacción del usuario.
* **Definición Operativa:** Nivel de acuerdo expresado por el personal respecto a la agilidad, fluidez, menor carga de estrés y comodidad operativa en el flujo de trabajo de gestión de vacunas.
* **Unidad de Medida:** Puntos en escala psicométrica Likert de 1 a 5 (4 reactivos: AP-01 a AP-04).
* **Rango Escalar:** 4 a 20 puntos en la subdimensión.
* **Instrumento:** Cuestionario de satisfacción N° 03.
* **Tendencia Esperada:** Aumento significativo de las puntuaciones medias entre el proceso manual (pretest) y el proceso asistido por SIVAC (postest).

---

### Indicador 3.2: Utilidad Percibida para la Gestión Sanitaria ($UP$)
* **Dimensión:** Satisfacción del usuario.
* **Definición Operativa:** Percepción subjetiva del trabajador (constructo *Perceived Usefulness* del Modelo TAM de Fred Davis) sobre el grado en que el procedimiento o herramienta tecnológica optimiza la trazabilidad, disponibilidad de stock en tiempo real y seguridad en el control de la cadena de frío.
* **Unidad de Medida:** Puntos en escala psicométrica Likert de 1 a 5 (4 reactivos: UP-01 a UP-04).
* **Rango Escalar:** 4 a 20 puntos en la subdimensión.
* **Instrumento:** Cuestionario de satisfacción N° 03.
* **Tendencia Esperada:** Incremento significativo en la percepción de utilidad y soporte a la toma de decisiones sanitarias.

---

## 4. Estructura y Dualidad Operativa del Instrumento de Satisfacción (TAM)

Para garantizar consistencia institucional ante la UNAJMA y rigurosidad psicométrica, el Instrumento N° 03 cuenta con dos modalidades claramente reglamentadas:

```
                                  DIMENSIÓN 3: SATISFACCIÓN DEL USUARIO
                                                   │
                   ┌───────────────────────────────┴───────────────────────────────┐
                   ▼                                                               ▼
        [MODALIDAD A: PRETEST - POSTEST]                               [MODALIDAD B: POSTEST EXCLUSIVO]
    Constructo: Satisfacción con el Proceso                         Constructo: Aceptación Tecnológica SIVAC
    En Pretest: Evalúa flujo manual / Excel                         En Postest: Evalúa plataforma web SIVAC
    En Postest: Evalúa flujo asistido por SIVAC                     Modelo TAM de Fred Davis (1989)
    8 ítems (4 AP + 4 UP)                                           8 ítems (4 PU + 4 PEOU)
    Permite contraste inferencial de hipótesis (HE3)                Evaluación descriptiva de calidad en uso
```

### Baremo Psicométrico Unificado (8 a 40 puntos):
$$\text{Puntaje Total} = \sum_{i=1}^{8} \text{Puntuación Ítem}_i$$

| Rango de Puntuación | Porcentaje Escalar | Nivel Categorial | Interpretación Operativa en la DISA Apurímac II |
|:---:|:---:|:---:|---|
| **8 a 18 puntos** | 20.0% – 45.0% | 🔴 **Nivel Bajo (Insatisfacción / Baja Aceptación)** | Percepción de lentitud, sobrecarga laboral, dificultades operativas y desconfianza en los saldos. |
| **19 a 29 puntos** | 47.5% – 72.5% | 🟡 **Nivel Medio (Aceptación Moderada)** | Satisfacción parcial; se perciben beneficios pero persisten dificultades de manejo o trámites lentos. |
| **30 a 40 puntos** | 75.0% – 100.0% | 🟢 **Nivel Alto (Plena Satisfacción y Aceptación)** | Elevada complacencia; el flujo y/o sistema es valorado como una herramienta ágil, intuitiva, útil y segura. |

---

## 5. Control de Calidad Metodológica

El `guardian-consistencia` certifica que:
1. La Variable Independiente queda definida como intervención tecnológica sin dimensiones analíticas en el modelo causal, preservando la validez interna del diseño preexperimental.
2. La Variable Dependiente conserva de manera estricta e inmutable las tres (03) dimensiones de estudio (Oportunidad de procesamiento, Consistencia documental y Satisfacción del usuario).
3. Se mantiene la correspondencia exacta ($1 \leftrightarrow 1$) entre los 6 indicadores y los 3 instrumentos oficiales de recolección de datos aprobados para la investigación.
