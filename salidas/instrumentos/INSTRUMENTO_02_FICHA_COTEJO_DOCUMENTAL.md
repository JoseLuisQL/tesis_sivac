---
tipo: instrumento_oficial_unajma
numero: 02
nombre: Ficha de Registro y Cotejo Documental de Consistencia
variable: Gestión de movimientos de vacunas (VD)
dimension: Consistencia documental
indicadores:
  - Ind 2.1: Porcentaje de registros completos y correctos / sin discrepancias (RSD)
  - Ind 2.2: Concordancia de programación vs entrega (CPE)
unidad_medida: Porcentaje (%)
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

### INSTRUMENTO DE RECOLECCIÓN DE DATOS N° 02
## FICHA DE REGISTRO Y COTEJO DOCUMENTAL DE CONSISTENCIA
**Protocolo Estandarizado PMMV (Ventana Simétrica de 30 Días), Regla Inmutable de 8 Criterios y Calibración Kappa de Cohen**

**Proyecto de Investigación:**  
*APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II*

* **Tesista:** Bach. José Luis Quispe León  
* **Asesora:** Dra. Norma Lorena Catacora Flores  
* **Variable Evaluada:** Gestión de movimientos de vacunas (Variable Dependiente)  
* **Dimensión Oficial (DEC-007):** Consistencia documental  
* **Técnica:** Análisis documental y auditoría de registros de existencias frente a documentos fuente  
* **Instrumento:** Ficha de auditoría y cotejo documental estructurada  
* **Población Objetivo:** Movimientos y despachos de vacunas en la red de frío institucional ($N = n = 14$ operadores / centros de acopio)  

---

### 1. DATOS GENERALES DE LA AUDITORÍA DOCUMENTAL

| Campo | Registro / Información |
|---|---|
| **Código del Operador / Centro Auditado:** | `TRAB-____` (Rango: TRAB-01 a TRAB-14) |
| **Centro de Acopio Provincial / Microred:** | ____________________________________________________________________ |
| **Provincia Sanitaria:** | Andahuaylas [  ] / Chincheros [  ] |
| **Momento de Medición:** | [  ] **PRETEST** ($O_1$: Kardex manual físico, cuadernos de registro y hojas Excel)<br>[  ] **POSTEST** ($O_2$: Base de datos relacional SIVAC y vales electrónicos PDF) |
| **Ventana Temporal de Auditoría (PMMV):** | Del _____/_____/2025 al _____/_____/2025 (30 días calendario) |
| **Fecha de Ejecución de la Auditoría:** | ______ / ______ / 2025 |
| **Auditor Principal:** | Bach. José Luis Quispe León (Tesista EPIS-UNAJMA) |
| **Auditor Secundario (si aplica):** | ____________________________________________________________________ |

---

### 2. PROTOCOLO DEL PLAN DE MEDICIONES MÍNIMAS VIABLES (PMMV)

1. **Ventana Temporal Simétrica de Observación:**
   * La auditoría documental se realiza sobre una ventana simétrica estandarizada de **treinta (30) días calendario consecutivos** en el pretest y exactamente **treinta (30) días calendario consecutivos** en el postest (tras la puesta en producción y estabilización operativa del sistema SIVAC).
2. **Tamaño Muestral de Documentos Evaluados:**
   * Se audita un corpus de **40 a 60 documentos / transacciones por ventana temporal** distribuidos proporcionalmente entre los centros de acopio y nodos de la red, garantizando representatividad estadística del flujo mensual habitual de biológicos.
3. **Fuentes de Evidencia Primaria (Contraste Físico-Documental):**
   * Pretest: Cuadernos de control de cadena de frío, tarjetas de kardex físico, archivos Excel locales de los centros de acopio y archivadores de comprobantes manuales (PECOSA/Guías).
   * Postest: Registro inmutable de transacciones en la base de datos MySQL de SIVAC, reportes de kardex electrónico valorizado y comprobantes de salida / vales generados automáticamente con firma y código hash.

---

### 3. REGLA INMUTABLE DE LOS 8 CRITERIOS DE CONFORMIDAD PARA $RSD$

Para erradicar la ambigüedad y el sesgo del evaluador, la auditoría del indicador **Porcentaje de Registros sin Discrepancias ($RSD$)** se rige por una regla binaria estricta e inmutable:

* **REGISTRO CONFORME ($1$):** El registro cumple **simultáneamente y sin excepción** con los ocho (8) criterios de calidad del dato frente a la evidencia física y el documento ministerial de respaldo.
* **REGISTRO NO CONFORME ($0$):** El registro presenta al menos una omisión, borrón, enmienda ilegible, error tipográfico, desfase de cálculo o contradicción en cualquiera de los ocho criterios.

```
+===================================================================================================+
|                        REGLA DE LOS OCHO (8) CRITERIOS OBLIGATORIOS PARA RSD                      |
+===================================================================================================+
|  1. Tipo de movimiento clasificado unívocamente (Entrada por remesa, Salida a EESS o Ajuste).    |
|  2. Denominación oficial estandarizada del biológico según Esquema Regular Nacional MINSA.        |
|  3. Identificación exacta del número de lote (rotulado del frasco coincidente con documento).     |
|  4. Cantidad de dosis / viales exacta y coincidente con el stock físico y acta de recepción.     |
|  5. Fecha del movimiento consignada con formato completo (DD/MM/AAAA) y secuencia cronológica.    |
|  6. Establecimiento de origen o destino plenamente individualizado con código RENIPRESS oficial.  |
|  7. Nombre completo, firma o usuario responsable del despacho o recepción plenamente trazable.    |
|  8. Documento formal de respaldo asociado y verificado (Vale oficial, PECOSA, Guía de Remisión).  |
+===================================================================================================+
  CRITERIO DE EVALUACIÓN:
  - Si cumple Criterios 1 al 8 simultáneamente  ⟶  CONFORME (1)
  - Si incumple al menos 1 criterio (cualquiera) ⟶  NO CONFORME (0) [Discrepancia detectada]
```

---

### 4. SECCIÓN A: AUDITORÍA DE REGISTROS SIN DISCREPANCIAS ($RSD$)

**Definición Operacional:** Porcentaje de registros de movimientos de vacunas auditados durante la ventana temporal que satisfacen con rigor absoluto los ocho criterios obligatorios de integridad y concordancia.

**Fórmula Matemática Institucional:**
$$RSD = \left( \frac{N_{\text{registros conformes sin discrepancia}}}{N_{\text{total de registros auditados}}} \right) \times 100$$

#### Matriz de Auditoría de Registros de Vacunas:

| N° Reg. | Vacuna / Insumo Auditado | Lote | Cantidad | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | Veredicto Final (1 = Conforme, 0 = No Conf.) | Tipo de Discrepancia / Causa Raíz |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **01** | Vacuna BCG | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **02** | Hepatitis B Pediátrica | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **03** | Vacuna Pentavalente | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **04** | Neumococo Conjugada | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **05** | Rotavirus | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **06** | Antipolio Inactivada (IPV) | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **07** | Antipolio Oral (bOPV) | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **08** | Vacuna SPR (Sarampión-Paperas-Rubéola) | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **09** | Antiamarílica (AMA) | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **10** | Influenza Adulto | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **11** | Influenza Pediátrica | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **12** | Vacuna contra VPH | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **13** | dT Adulto (Difteria-Tétanos) | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **14** | dTpa Gestante | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **15** | Varicela | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **16** | Hepatitis A | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **17** | COVID-19 Comirnaty Bivalente | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **18** | Jeringas descartables autodesactivables | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **19** | Diluyentes específicos de biológicos | | | | | | | | | | | [  ] 1   [  ] 0 | |
| **20** | Cajas térmicas / Paquetes fríos | | | | | | | | | | | [  ] 1   [  ] 0 | |
| ... | *(Se auditan de 40 a 60 registros en la ventana)* | | | | | | | | | | | [  ] 1   [  ] 0 | |

#### Consolidado del Indicador RSD:
* Número Total de Registros Evaluados en la Ventana ($N_{\text{total\_reg}}$): **______ registros**.
* Número de Registros Conformes sin Discrepancia ($N_{\text{conf\_reg}}$): **______ registros**.
* Número de Registros con Discrepancia / Fallas ($N_{\text{disc\_reg}}$): **______ registros**.
* **Porcentaje de Registros sin Discrepancias ($RSD$):**
  $$\mathbf{\% \, RSD = \left( \frac{N_{\text{conf\_reg}}}{N_{\text{total\_reg}}} \right) \times 100 = ____________ \%}$$

---

### 5. SECCIÓN B: AUDITORÍA DE CONCORDANCIA DE PROGRAMACIÓN VS. ENTREGA ($CPE$)

**Definición Operacional:** Proporción porcentual de despachos y entregas de vacunas evaluadas en las que la cantidad entregada coincide con la cantidad programada (dosis a dosis), o cuenta con justificación documental formal MINSA debidamente acreditada.

**Fórmula Corregida y Blindada del PMMV:**
$$CPE = \left( \frac{N_{\text{entregas concordantes}}}{N_{\text{total de entregas evaluadas}}} \right) \times 100$$

#### Criterio Oficial de Concordancia Operativa:
Una entrega o despacho se califica como **CONCORDANTE ($1$)** si y solo si cumple una de las siguientes dos condiciones formales:
1. **Concordancia Exacta Dosis a Dosis:** La cantidad despachada y asentada en el vale oficial es idéntica en número exacto de viales/dosis a la cantidad solicitada en la programación formal del establecimiento receptor ($Q_{ent} = Q_{prog}$).
2. **Ajuste Técnico Justificado MINSA:** Si la cantidad entregada difiere de la programada ($Q_{ent} \neq Q_{prog}$), existe un documento sustentatorio oficial archivado (Acta de ajuste de stock, Memorando de contingencia de cadena de frío o Directiva de racionalización biológica emitida por la Dirección Ejecutiva de Salud de las Personas / Estrategia de Inmunizaciones MINSA) que autoriza expresamente la variación.

Si no se cumple ninguna de las dos condiciones anteriores (entrega arbitraria, recorte no justificado, error de conteo o desabastecimiento sin sustento formal), el despacho se clasifica como **NO CONCORDANTE ($0$)**.

#### Matriz de Auditoría de Entregas y Vales:

| N° Ent. | Vacuna / Biológico | N° Documento / Vale | Cantidad Solicitada / Programada ($Q_{prog}$) | Cantidad Entregada Conforme ($Q_{ent}$) | Diferencia Absoluta ($|Q_{prog} - Q_{ent}|$) | Justificación Formal MINSA Acreditada (Sí/No / N/A) | Veredicto Entrega (1 = Concordante, 0 = No Conc.) | Causa Raíz del Desfase |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|---|
| **01** | Vacuna Pentavalente | Vale N°: ________ | | | | [ ] Sí [ ] No [ ] N/A | [  ] 1   [  ] 0 | |
| **02** | Neumococo Conjugada | Vale N°: ________ | | | | [ ] Sí [ ] No [ ] N/A | [  ] 1   [  ] 0 | |
| **03** | Vacuna Rotavirus | Vale N°: ________ | | | | [ ] Sí [ ] No [ ] N/A | [  ] 1   [  ] 0 | |
| **04** | Vacuna SPR | Vale N°: ________ | | | | [ ] Sí [ ] No [ ] N/A | [  ] 1   [  ] 0 | |
| **05** | Vacuna Influenza Adulto | Vale N°: ________ | | | | [ ] Sí [ ] No [ ] N/A | [  ] 1   [  ] 0 | |
| **06** | Vacuna Influenza Pediátrica | Vale N°: ________ | | | | [ ] Sí [ ] No [ ] N/A | [  ] 1   [  ] 0 | |
| **07** | Vacuna contra VPH | Vale N°: ________ | | | | [ ] Sí [ ] No [ ] N/A | [  ] 1   [  ] 0 | |
| **08** | Vacuna dT Adulto | Vale N°: ________ | | | | [ ] Sí [ ] No [ ] N/A | [  ] 1   [  ] 0 | |
| **09** | Antipolio (IPV/bOPV) | Vale N°: ________ | | | | [ ] Sí [ ] No [ ] N/A | [  ] 1   [  ] 0 | |
| **10** | Vacuna BCG | Vale N°: ________ | | | | [ ] Sí [ ] No [ ] N/A | [  ] 1   [  ] 0 | |
| **11** | Antiamarílica (AMA) | Vale N°: ________ | | | | [ ] Sí [ ] No [ ] N/A | [  ] 1   [  ] 0 | |
| **12** | Vacuna Hepatitis B | Vale N°: ________ | | | | [ ] Sí [ ] No [ ] N/A | [  ] 1   [  ] 0 | |
| ... | *(Se auditan de 40 a 60 entregas en la ventana)* | | | | | [ ] Sí [ ] No [ ] N/A | [  ] 1   [  ] 0 | |

#### Consolidado del Indicador CPE:
* Total de Entregas / Despachos Auditados en la Ventana ($N_{\text{total\_entregas}}$): **______ entregas**.
* Número de Entregas Concordantes (Exactas o Justificadas) ($N_{\text{entregas\_concordantes}}$): **______ entregas**.
* Número de Entregas No Concordantes / Desfases Injustificados: **______ entregas**.
* **Porcentaje de Concordancia de Programación vs. Entrega ($CPE$):**
  $$\mathbf{\% \, CPE = \left( \frac{N_{\text{entregas\_concordantes}}}{N_{\text{total\_entregas}}} \right) \times 100 = ____________ \%}$$

---

### 6. PROTOCOLO DE CONFIABILIDAD INTER-EVALUADOR (KAPPA DE COHEN)

Para asegurar la objetividad, reproducibilidad y consistencia psicométrica de la ficha documental frente al criterio de auditoría, se aplica un protocolo riguroso de confiabilidad inter-evaluador:

1. **Procedimiento de Muestreo a Ciegas:**
   * Se extrae una **muestra cruzada aleatoria de treinta (30) registros documentales** tomados del archivo institucional.
   * Dos evaluadores independientes realizan la auditoría simultánea e individual de los 30 registros sin comunicación entre sí:
     - *Evaluador A (Investigador principal):* Bach. José Luis Quispe León.
     - *Evaluador B (Auditor de control de calidad):* Profesional de salud / docente evaluador independiente entrenado en los 8 criterios.
   * Cada evaluador emite un dictamen binario independiente para cada registro ($1 = \text{Conforme}$, $0 = \text{No Conforme}$).
2. **Modelo Matemático: Coeficiente Kappa de Cohen ($\kappa$):**
   * Se tabulan las decisiones de ambos jueces en una matriz de contingencia $2 \times 2$:
     $$\kappa = \frac{P_o - P_e}{1 - P_e}$$
     Donde:
     - $P_o$: Proporción de acuerdo observado entre los evaluadores:
       $$P_o = \frac{a + d}{N_{\text{muestra}}} = \frac{a + d}{30}$$
       *(siendo $a$ los acuerdos de registros conformes, y $d$ los acuerdos de registros no conformes).*
     - $P_e$: Proporción de acuerdo esperado por puro azar:
       $$P_e = \left(\frac{a + b}{30}\right)\left(\frac{a + c}{30}\right) + \left(\frac{c + d}{30}\right)\left(\frac{b + d}{30}\right)$$
3. **Criterio de Decisión y Aceptación Psicométrica (Landis & Koch, 1977; Fleiss et al., 2003):**
   * **Umbral Mínimo Exigido:** **$\kappa \ge 0.80$** (Acuerdo casi perfecto / excelente concordancia inter-evaluador).
   * **Contingencia:** Si $\kappa < 0.80$, se convoca a sesión de conciliación técnica para revisar discrepancias en la interpretación de los criterios, se recalibra la guía de auditoría y se evalúa una nueva muestra cruzada de 30 registros hasta satisfacer $\kappa \ge 0.80$.

---

### 7. RESUMEN Y CERTIFICACIÓN DE LA AUDITORÍA

| Indicador Documental Evaluado | Resultado Pretest | Resultado Postest | Variación Absoluta ($\Delta$) |
|---|:---:|:---:|:---:|
| **Porcentaje de Registros sin Discrepancias ($RSD$):** | **______ %** | **______ %** | **+ ______ %** |
| **Porcentaje de Concordancia Programada vs. Entregada ($CPE$):** | **______ %** | **______ %** | **+ ______ %** |

**Declaración Jurada Institucional:** Se deja constancia de que los valores consignados en la presente ficha corresponden fielmente a los expedientes, cuadernos de balance y bases de datos electrónicas auditadas durante el período de prueba.

---

**Firma del Auditor / Investigador:**  
Bach. José Luis Quispe León  
DNI: ________________________  
Tesista EPIS — UNAJMA  

**V°B° y Sello de la Coordinación de Inmunizaciones / Almacén Especializado:**  
Firma: ______________________________________  
Nombre del Responsable: ______________________________________  
DNI: ________________________  
Dirección de Salud Apurímac II  
