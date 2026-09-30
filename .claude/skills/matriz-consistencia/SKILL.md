---
name: matriz-consistencia
description: Reglas metodológicas y estructura para auditar y mantener la alineación estricta de la matriz de consistencia y operacionalización en la tesis SIVAC.
---

# Matriz de Consistencia y Operacionalización — SIVAC

Esta habilidad define los principios de alineación metodológica inquebrantable entre los componentes de la investigación.

## 1. Principio de Isomorfismo y Alineación Vertical
Debe existir una correspondencia biunívoca (1 a 1) e indisoluble entre:
1. **Problema General** $\leftrightarrow$ **Objetivo General** $\leftrightarrow$ **Hipótesis General** $\leftrightarrow$ **Relación entre VI y VD**.
2. **Problemas Específicos (1 al 4)** $\leftrightarrow$ **Objetivos Específicos (1 al 4)** $\leftrightarrow$ **Hipótesis Específicas (1 al 4)** $\leftrightarrow$ **Dimensiones de la VD (1 al 4)**.

### Dimensiones de la Variable Dependiente:
- **Dimensión 1:** Oportunidad de procesamiento $\rightarrow$ Objetivo Específico 1 $\rightarrow$ Hipótesis Específica 1.
- **Dimensión 2:** Fiabilidad de la información $\rightarrow$ Objetivo Específico 2 $\rightarrow$ Hipótesis Específica 2.
- **Dimensión 3:** Concordancia documental $\rightarrow$ Objetivo Específico 3 $\rightarrow$ Hipótesis Específica 3.
- **Dimensión 4:** Satisfacción del usuario $\rightarrow$ Objetivo Específico 4 $\rightarrow$ Hipótesis Específica 4.

## 2. Alineación de Operacionalización
Cada indicador debe desprenderse exclusivamente de su dimensión:
- **Variable Independiente (SIVAC):** Enfoque Extreme Programming, módulos de usuarios, lotes, entradas, salidas, kardex digital y reportes.
- **Variable Dependiente (Gestión de Movimientos):**
  - *Oportunidad:* Tiempos de registro de entradas/salidas, tiempo de generación de kardex.
  - *Fiabilidad:* Porcentaje de registros con datos correctos, tasa de discrepancia en saldos.
  - *Concordancia:* Grado de coincidencia física-documental de vales y lotes.
  - *Satisfacción:* Percepción de utilidad y facilidad de uso (escala Likert).

## 3. Criterios de Auditoría
Si en algún borrador se detecta que un objetivo específico no corresponde con su respectiva dimensión o hipótesis, el `guardian-consistencia` debe bloquear la aprobación y emitir una alerta de desalineación.
