---
tipo: operacionalizacion_variables
fase: F2
fecha: 2026-10-02
version: 3.0_definitiva
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
> **Propósito:** Definir con máximo rigor metodológico la Variable Independiente (Intervención Tecnológica SIVAC) y la Variable Dependiente (Gestión de movimientos de vacunas) con sus tres dimensiones oficiales, seis indicadores cuantitativos, fórmulas matemáticas, jerarquía de unidades, unidades de medida, escalas, protocolos de confiabilidad e instrumentos de recolección para la investigación.

---

## 1. Operacionalización de la Variable Independiente (VI)

### 1.1 Definición Conceptual
El **Sistema web SIVAC** (Sistema de Información de Vacunas) es una solución tecnológica integral basada en arquitectura cliente-servidor web, desarrollada mediante la metodología ágil Extreme Programming (XP) en sus cuatro fases (Planificación, Diseño, Codificación y Pruebas) y evaluada bajo el estándar internacional de calidad de producto de software **ISO/IEC 25010:2023**, diseñada específicamente para automatizar, controlar y asegurar la trazabilidad del registro de entradas, salidas, transferencias y emisión de vales de entrega de biológicos en la red de frío de la Dirección de Salud Apurímac II.

### 1.2 Definición Operacional y Naturaleza Metodológica (Tratamiento Experimental)
En el marco de un diseño de investigación **preexperimental con pretest y postest en un solo grupo ($O_1 \longrightarrow X \longrightarrow O_2$)**, de tipo aplicada y de nivel **explicativo (con alcance evaluativo-comparativo)**, la Variable Independiente opera como un **estímulo o intervención tecnológica manipulada por presencia/ausencia**, estructurada en dos condiciones operativas:

1. **Condición Control / Basal ($X_0$ - Pretest):** Gestión tradicional no automatizada sustentada en registros físicos en cuadernos de kardex manual, hojas de balance en papel y archivos de cálculo desarticulados (Excel), propensos a lentitud de cálculo, desgaste físico y errores de transcripción.
2. **Condición Experimental ($X_1$ - Postest):** Gestión automatizada en tiempo real mediante la puesta en producción y adopción del sistema web SIVAC, con validación de reglas de negocio, control transaccional de lotes, balance automático de existencias y generación de vales electrónicos en PDF.

> **Sustento del Tratamiento Experimental:**  
> Las especificaciones técnicas del software (historias de usuario según Extreme Programming y atributos de calidad de producto de software bajo ISO/IEC 25010:2023) corresponden al desarrollo de la solución tecnológica implementada. En el marco del diseño preexperimental, el software actúa como el tratamiento experimental evaluado a través de su impacto en las dimensiones e indicadores de la gestión de movimientos de vacunas en el Capítulo V.

### 1.3 Matriz de la Variable Independiente (Intervención Tecnológica)

| Variable | Naturaleza Metodológica | Definición Conceptual | Niveles de Manipulación Experimental | Mecanismo de Aplicación / Control | Rol en el Informe de Tesis |
|---|---|---|---|---|---|
| **Variable Independiente (X):**<br>Sistema web SIVAC | Intervención tecnológica / Tratamiento experimental | Plataforma informática web desarrollada bajo Extreme Programming (XP) y estándar ISO/IEC 25010:2023 para automatizar la gestión de biológicos. | • **Nivel 0 ($X_0$ - Pretest):** Proceso manual tradicional (kardex en papel, cuadernos y Excel aislado).<br><br>• **Nivel 1 ($X_1$ - Postest):** Proceso automatizado mediante plataforma SIVAC en red de frío. | • Puesta en producción en servidor web institucional.<br>• Capacitación protocolizada a los 14 trabajadores.<br>• Migración de saldos iniciales y control de acceso por roles. | Núcleo del **Capítulo III** (Metodología XP, arquitectura cliente-servidor, modelado de datos, interfaces y pruebas funcionales). |

---

## 2. Operacionalización de la Variable Dependiente (VD)

### 2.1 Definición Conceptual
La **Gestión de movimientos de vacunas** es el conjunto estructurado de procesos técnicos y logísticos orientados a programar, registrar, despachar y conciliar el flujo de biológicos en la red de frío de la DISA Apurímac II, garantizando oportunidad operativa, consistencia documental e integridad de la cadena de frío bajo la norma técnica del MINSA.

### 2.2 Definición Operacional y Jerarquía Metodológica de Unidades
La gestión de movimientos de vacunas se evalúa de manera cuantitativa y comparativa contrastando el estado basal previo a la intervención ($O_1$) frente al estado posterior a la adopción de SIVAC ($O_2$), mediante una estricta jerarquía metodológica de unidades:

1. **Unidad de Análisis Institucional:**  
   El personal de salud del área de inmunizaciones y cadena de frío de la Dirección de Salud Apurímac II, conformado censalmente por la totalidad de sus integrantes ($N = n = 14$ trabajadores: enfermeros licenciados, técnicos de enfermería y personal de soporte logístico). Constituye el sujeto institucional donde se manifiesta el fenómeno investigado.

2. **Unidades de Observación Específicas por Dimensión:**  
   Para la recolección empírica, la investigación distingue tres unidades de observación adaptadas a la naturaleza de cada dimensión:
   - *Dimensión 1 (Oportunidad de procesamiento):* Las **transacciones operativas cronometradas** de registro de movimientos en el kardex y de emisión de comprobantes de salida / vales de entrega formalizados por los operadores.
   - *Dimensión 2 (Consistencia documental):* Los **documentos de movimientos auditados** (asientos de kardex diario, reportes y vales de despacho PECOSA / actas de entrega) contrastados frente a la evidencia física del almacén y los criterios normativos.
   - *Dimensión 3 (Satisfacción del usuario):* Los **trabajadores del área de inmunizaciones encuestados** ($n = 14$), evaluados como informantes clave sobre el proceso operativo.

---

### 2.3 Matriz General de Operacionalización de la Variable Dependiente

| Variable | Definición Conceptual | Dimensiones | Indicadores y Qué Mide | Escala, Unidad e Instrumento |
|---|---|---|---|---|
| **Variable Dependiente (Y):**<br>Gestión de movimientos de vacunas | Conjunto de procesos técnicos y logísticos para programar, registrar, despachar y conciliar el flujo de biológicos en la red de frío de la DISA Apurímac II, garantizando oportunidad, consistencia documental y cadena de frío. | **1. Oportunidad de procesamiento** | • **Tiempo de registro de movimientos ($T_{reg}$):** Mide los minutos netos desde el inicio de digitación hasta su balance formal en kardex.<br><br>• **Tiempo de emisión de comprobantes ($T_{vale}$):** Mide los minutos netos desde la solicitud hasta la formalización y emisión del vale de salida o PECOSA. | • **Unidad:** Minutos decimales ($\text{min}$)<br>• **Escala:** Razón / Continua<br>• **Instrumento:** Ficha cronométrica N° 01<br>• **Confiabilidad:** $ICC(2,1) \ge 0.75$ |
| | | **2. Consistencia documental** | • **Registros sin discrepancias ($RSD$):** Mide el porcentaje de registros conformes bajo cumplimiento simultáneo de 8 criterios obligatorios de auditoría.<br><br>• **Concordancia programada vs entregada ($CPE$):** Mide el porcentaje de entregas con cantidad física conforme respecto a lo solicitado. | • **Unidad:** Porcentaje ($\%$)<br>• **Escala:** Razón / Proporción $[0, 100]\%$<br>• **Instrumento:** Ficha de cotejo N° 02<br>• **Confiabilidad:** Kappa de Cohen $\kappa \ge 0.80$ |
| | | **3. Satisfacción del usuario**<br>*(Satisfacción con el proceso)* | • **Aceptación del proceso operativo ($AP$):** Mide la complacencia, agilidad, fluidez y menor estrés laboral en el flujo de trabajo (4 ítems: 4 a 20 pts).<br><br>• **Utilidad percibida sanitaria ($UP$):** Mide la percepción de trazabilidad, control de existencias y soporte en decisiones (4 ítems: 4 a 20 pts; global: 8 a 40 pts). | • **Unidad:** Puntuación psicométrica (8 a 40 pts)<br>• **Escala:** Ordinal / Likert (1 a 5)<br>• **Instrumento:** Cuestionario TAM N° 03<br>• **Confiabilidad:** Alfa de Cronbach $\alpha \ge 0.70$ sobre los 8 ítems de la Modalidad A, con intervalo de confianza al 95 % por el método de Feldt; Omega de McDonald no estimado por insuficiencia muestral ($n = 14$) |

---

## 3. Fichas Técnicas Detalladas de los 6 Indicadores de la VD

### Indicador 1.1: Tiempo de Registro de Movimiento de Vacunas ($T_{reg}$)
* **Dimensión:** Oportunidad de procesamiento.
* **Definición Operativa:** Lapso temporal neto en minutos transcurrido desde que el operador inicia la captura o digitación de los datos de un movimiento de vacunas (entrada, salida o transferencia) hasta que la transacción queda asentada y balanceada formalmente en el kardex institucional.
* **Fórmula:** $$T_{reg} = t_{\text{fin\_registro}} - t_{\text{inicio\_registro}}$$
* **Unidad de Medida:** Minutos decimales ($\text{min} = \text{minutos} + \frac{\text{segundos}}{60}$).
* **Escala de Medición:** Razón / Cuantitativa continua.
* **Unidad de Observación:** Transacciones operativas de registro de ingresos, salidas y transferencias de biológicos ejecutadas por los operadores.
* **Instrumento:** Ficha de observación cronométrica N° 01 (Sección A).
* **Protocolo de Medición:** Cronometraje digital estandarizado de 3 observaciones por participante, excluyendo interrupciones externas fortuitas.
* **Protocolo de Confiabilidad:** Estandarización instrumental previa y Coeficiente de Correlación Intraclase $ICC(2,1) \ge 0.75$ para repetibilidad y consistencia interobservador.
* **Tendencia Esperada:** Reducción sustancial del tiempo medio de registro entre pretest ($X_0$) y postest ($X_1$).

---

### Indicador 1.2: Tiempo de Emisión de Comprobante de Salida / Vale ($T_{vale}$)
* **Dimensión:** Oportunidad de procesamiento.
* **Definición Operativa:** Tiempo en minutos requerido para procesar el requerimiento de biológicos de una microred, verificar lotes disponibles, generar el comprobante oficial de despacho (vale / PECOSA) y formalizar la orden imprimible o en formato PDF.
* **Fórmula:** $$T_{vale} = t_{\text{emision\_documento}} - t_{\text{inicio\_solicitud}}$$
* **Unidad de Medida:** Minutos decimales ($\text{min}$).
* **Escala de Medición:** Razón / Cuantitativa continua.
* **Unidad de Observación:** Transacciones de emisión de comprobantes de despacho tramitadas por los operadores.
* **Instrumento:** Ficha de observación cronométrica N° 01 (Sección B).
* **Protocolo de Medición:** Cronometraje digital estandarizado de 3 emisiones de comprobantes por participante.
* **Protocolo de Confiabilidad:** Protocolo de estandarización instrumental cronométrica y evaluación mediante Coeficiente de Correlación Intraclase $ICC(2,1) \ge 0.75$.
* **Tendencia Esperada:** Reducción sustancial del tiempo de emisión gracias a la generación automatizada de reportes en PDF por SIVAC.

---

### Indicador 2.1: Porcentaje de Registros sin Discrepancias ($RSD$)
* **Dimensión:** Consistencia documental.
* **Definición Operativa:** Proporción porcentual de movimientos de biológicos auditados en los que la información asentada coincide plenamente con los documentos fuentes y el stock físico real, sin borrones, omisiones ni inconsistencias aritméticas.
* **Fórmula:**
  $$RSD = \left( \frac{\text{Número de Registros Conformes sin Discrepancia}}{\text{Total de Registros Auditados}} \right) \times 100$$
* **Unidad de Medida:** Porcentaje ($\%$).
* **Escala de Medición:** Razón / Proporción.
* **Unidad de Observación:** Asientos de movimientos registrados en kardex físicos y digitales de los centros de acopio.
* **Instrumento:** Ficha de registro y cotejo documental N° 02 (Sección A).
* **Regla Operativa de Decisión (8 Criterios Obligatorios de Auditoría):**
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
* **Protocolo de Confiabilidad:** Auditoría ciega por dos evaluadores independientes y concordancia inter-auditor evaluada mediante Coeficiente Kappa de Cohen ($\kappa \ge 0.80$).
* **Tendencia Esperada:** Incremento significativo de la proporción de registros conformes hacia el 100% en el postest.

---

### Indicador 2.2: Concordancia de Cantidad Programada vs. Entregada ($CPE$)
* **Dimensión:** Consistencia documental.
* **Definición Operativa:** Porcentaje de entregas institucionales en las que la cantidad física de biológicos efectivamente despachada y sustentada en vales oficiales coincide plenamente con el volumen programado y solicitado formalmente por las microredes ejecutoras, sin quiebres de existencias ni sobre-despachos injustificados.
* **Fórmula Matemática Corregida (Acotada en $[0, 100]\%$):**
  $$CPE = \left( \frac{N_{\text{entregas\_concordantes}}}{N_{\text{total\_entregas\_evaluadas}}} \right) \times 100$$
  *Donde una entrega es concordante si y solo si $Q_{\text{entregada}} = Q_{\text{programada}}$ sin discrepancias.*
* **Unidad de Medida:** Porcentaje ($\%$).
* **Escala de Medición:** Razón / Proporción acotada en $[0, 100]\%$.
* **Unidad de Observación:** Expedientes de requerimientos de microredes y sus correspondientes vales de salida / PECOSA asociados.
* **Instrumento:** Ficha de registro y cotejo documental N° 02 (Sección B).
* **Protocolo de Medición:** Auditoría comparativa de un corpus de 40 a 60 entregas por ventana temporal de 30 días, distribuidas proporcionalmente entre los centros de acopio, frente a sus respectivos vales oficiales de salida.
* **Protocolo de Confiabilidad:** Concordancia inter-auditor independiente evaluada mediante el Coeficiente Kappa de Cohen ($\kappa \ge 0.80$).
* **Tendencia Esperada:** Incremento en el nivel de concordancia hacia el 100%, eliminando desfases entre programación y despacho.

---

### Indicador 3.1: Aceptación del Proceso Operativo ($AP$)
* **Dimensión:** Satisfacción del usuario.
* **Definición Operativa:** Nivel de acuerdo expresado por el personal respecto a la agilidad, fluidez, menor carga de estrés laboral y comodidad operativa en el flujo de trabajo de gestión de vacunas.
* **Unidad de Medida:** Puntos en escala psicométrica Likert de 1 a 5 (4 reactivos: AP-01 a AP-04).
* **Escala de Medición:** Ordinal / Likert (1 a 5).
* **Rango Escalar:** 4 a 20 puntos en la subdimensión.
* **Unidad de Observación:** Trabajadores del área de inmunizaciones ($n = 14$).
* **Instrumento:** Cuestionario de satisfacción del usuario N° 03 (Sección AP).
* **Protocolo de Confiabilidad:** Coeficiente Alfa de Cronbach de referencia sobre los 8 ítems de la Modalidad A ($\alpha \ge 0.70$), con reporte obligatorio del intervalo de confianza al 95 % por el método de Feldt, Woodruff y Salih. El Alfa de esta subescala de 4 ítems se reporta solo como exploratorio, por la razón sujeto/ítem de 1.75. El Coeficiente Omega de McDonald no se estima por insuficiencia muestral ($n = 14$).
* **Tendencia Esperada:** Aumento significativo de las puntuaciones medias entre el proceso manual (pretest) y el proceso asistido por SIVAC (postest).

---

### Indicador 3.2: Utilidad Percibida para la Gestión Sanitaria ($UP$)
* **Dimensión:** Satisfacción del usuario.
* **Definición Operativa:** Percepción subjetiva del trabajador (constructo *Perceived Usefulness* del modelo conceptual) sobre el grado en que el procedimiento de gestión optimiza la trazabilidad, disponibilidad de stock en tiempo real y seguridad en el control de la cadena de frío.
* **Unidad de Medida:** Puntos en escala psicométrica Likert de 1 a 5 (4 reactivos: UP-01 a UP-04).
* **Escala de Medición:** Ordinal / Likert (1 a 5).
* **Rango Escalar:** 4 a 20 puntos en la subdimensión.
* **Unidad de Observación:** Trabajadores del área de inmunizaciones ($n = 14$).
* **Instrumento:** Cuestionario de satisfacción del usuario N° 03 (Sección UP).
* **Protocolo de Confiabilidad:** Coeficiente Alfa de Cronbach de referencia sobre los 8 ítems de la Modalidad A ($\alpha \ge 0.70$), con reporte obligatorio del intervalo de confianza al 95 % por el método de Feldt, Woodruff y Salih. El Alfa de esta subescala de 4 ítems se reporta solo como exploratorio, por la razón sujeto/ítem de 1.75. El Coeficiente Omega de McDonald no se estima por insuficiencia muestral ($n = 14$).
* **Tendencia Esperada:** Incremento significativo en la percepción de utilidad y soporte a la toma de decisiones sanitarias.

---

## 4. Estructura Psicométrica de la Dimensión 3 y Módulo TAM Complementario

Para garantizar la coherencia metodológica entre el diseño experimental pretest-postest ($O_1 \to X \to O_2$) y la literatura de adopción tecnológica, el Instrumento N° 03 se articula en dos componentes metodológicos:

```
                        DIMENSIÓN 3: SATISFACCIÓN DEL USUARIO
                                         │
        ┌────────────────────────────────┴────────────────────────────────┐
        ▼                                                                 ▼
[MODALIDAD A: PRETEST Y POSTEST]                          [MODALIDAD B: MÓDULO ANEXO DE POSTEST]
Constructo: Satisfacción con el Proceso                   Constructo: Aceptación Tecnológica de Software
Medición: Pretest (manual) vs Postest (SIVAC)             Medición: Postest exclusivo tras uso del sistema
Estructura: 8 ítems (4 AP + 4 UP)                         Modelo TAM de Fred Davis (1989)
Rango: 8 a 40 puntos                                      8 ítems (4 PU + 4 PE)
Permite inferencia causal pareada (HE3 con Wilcoxon)      Evaluación descriptiva de calidad en uso (ISO 25010)
```

### Baremo de Interpretación por Terciles Teóricos (8 a 40 puntos):

La partición en 8 a 18, 19 a 29 y 30 a 40 constituye un tercil teórico calculado sobre el rango posible de la suma de 8 ítems Likert de 1 a 5. Esa suma adopta exactamente 33 valores enteros, del 8 al 40, y el tercil los reparte en tres grupos de 11 valores cada uno, sin residuo. Los tres rangos no constituyen puntos de corte normativos validados empíricamente, por cuanto con n = 14 no existe distribución de referencia que los sustente.

$$\text{Puntaje Total} = \sum_{i=1}^{8} \text{Puntuación Ítem}_i$$

| Rango de Puntuación | Porcentaje Escalar | Nivel Categorial | Interpretación Operativa en la DISA Apurímac II |
|:---:|:---:|:---:|---|
| **8 a 18 puntos** | 20.0% – 45.0% | **Nivel Bajo (Insatisfacción / Baja Aceptación)** | Percepción de lentitud, sobrecarga laboral, dificultades operativas y desconfianza en los saldos. |
| **19 a 29 puntos** | 47.5% – 72.5% | **Nivel Medio (Aceptación Moderada)** | Satisfacción parcial; se perciben beneficios pero persisten dificultades de manejo o trámites lentos. |
| **30 a 40 puntos** | 75.0% – 100.0% | **Nivel Alto (Plena Satisfacción y Aceptación)** | Elevada complacencia; el flujo es valorado como ágil, intuitivo, útil y seguro para la toma de decisiones. |

---

## 5. Protocolos Diferenciados de Confiabilidad y Validez Instrumental

En concordancia con las buenas prácticas psicométricas y metodológicas, se aplican protocolos de confiabilidad adaptados a la naturaleza empírica de cada instrumento:

| Instrumento | Dimensión Evaluada | Naturaleza de Variable | Protocolo de Confiabilidad | Criterio de Aceptación | Protocolo de Validez de Contenido |
|---|---|---|---|---|---|
| **Instrumento N° 01:**<br>Ficha de observación cronométrica | Dimensión 1:<br>Oportunidad de procesamiento | Cuantitativa continua (tiempos en minutos decimales) | Estandarización instrumental cronométrica y Coeficiente de Correlación Intraclase para acuerdo interobservador y repetibilidad. | $ICC(2,1) \ge 0.75$<br>(Acuerdo excelente) | **No se somete a juicio de contenido.**<br>• Validez sustentada en el protocolo de medición de movimientos de vacunas (PMMV).<br>• Calibración interobservador mediante Coeficiente de Correlación Intraclase ICC(2,1) >= 0.75. |
| **Instrumento N° 02:**<br>Ficha de registro y cotejo documental | Dimensión 2:<br>Consistencia documental | Proporción cuantitativa basada en criterios dicotómicos de auditoría | Concordancia inter-auditor independiente sobre muestra de documentos evaluados bajo la regla de 8 criterios. | Coeficiente Kappa de Cohen<br>$\kappa \ge 0.80$<br>(Concordancia casi perfecta) | **No se somete a juicio de contenido.**<br>• Validez sustentada en el protocolo de medición de movimientos de vacunas (PMMV).<br>• Concordancia interauditor mediante Coeficiente Kappa de Cohen >= 0.80. |
| **Instrumento N° 03:**<br>Cuestionario de satisfacción del usuario | Dimensión 3:<br>Satisfacción del usuario | Ordinal / Escala Likert de 5 puntos (8 ítems) | Consistencia interna psicométrica para escalas congenéricas. | Coeficiente Alfa de Cronbach sobre los 8 ítems de la Modalidad A<br>$\alpha \ge 0.70$<br>(Intervalo de confianza al 95 % por el método de Feldt, Woodruff y Salih)<br>Coeficiente Omega de McDonald: no estimado por insuficiencia muestral ($n = 14$) | **Único instrumento sometido a juicio de contenido.**<br>• Certificado único en formato Fany 2024, emitido en blanco (DEC-015 y DEC-016).<br>• Objeto: los 8 ítems de la Modalidad A de DEC-019 (AP-01 a AP-04 y UP-01 a UP-04).<br>• Criterios dicotómicos Pertinencia Sí/No, Relevancia Sí/No y Claridad Sí/No; con 3 jueces y c = 2, V = S / n.<br>• Coeficiente V de Aiken >= 0.80 e Índice de Validez de Contenido IVC >= 0.80 sobre esos 8 ítems.<br>• La Modalidad B (PU-01 a PU-04 y PE-01 a PE-04) no recibe certificado. |

---

## 6. Regla Conjuntiva de Decisión e Integridad Metodológica (DEC-007)

El `guardian-consistencia` certifica formalmente los siguientes preceptos epistemológicos:

1. **Inmutabilidad de las 3 Dimensiones y 6 Indicadores (DEC-007):**  
   La Variable Dependiente se compone de forma única y cerrada por:
   - Dimensión 1: Oportunidad de procesamiento ($T_{reg}, T_{vale}$).
   - Dimensión 2: Consistencia documental ($RSD, CPE$).
   - Dimensión 3: Satisfacción del usuario ($AP, UP$).

2. **Regla Conjuntiva de Decisión para la Hipótesis General:**  
   Para la contrastación de la Hipótesis General, se establece que la aplicación del sistema SIVAC genera una mejora integral y significativa en la gestión de movimientos de vacunas si y solo si se rechazan simultáneamente las hipótesis nulas de las tres hipótesis específicas:
   $$\text{Rechazo } H_{0\text{G}} \iff (p < 0.05 \text{ en } HE_1) \land (p < 0.05 \text{ en } HE_2) \land (p < 0.05 \text{ en } HE_3)$$
   Esta condición salvaguarda la validez interna del estudio, impidiendo que la mejora en una dimensión compense artificialmente el estancamiento o retroceso en otra.

3. **Correspondencia Biunívoca Instrumental ($1 \leftrightarrow 1$):**  
   Existe correspondencia unívoca entre las dimensiones de la Variable Dependiente, los indicadores cuantitativos, las unidades de observación y los tres instrumentos oficiales aprobados para la investigación.
