---
name: matriz-consistencia
description: Reglas metodológicas y estructura para auditar y mantener la alineación estricta de la matriz de consistencia y operacionalización en la tesis SIVAC.
---

# Matriz de Consistencia y Operacionalización — SIVAC

Esta habilidad define los principios de alineación metodológica inquebrantable entre los componentes de la investigación.

## 1. Principio de Isomorfismo y Alineación Vertical (3 Dimensiones — DEC-007)
Debe existir una correspondencia biunívoca (1 a 1) e indisoluble entre:
1. **Problema General** $\leftrightarrow$ **Objetivo General** $\leftrightarrow$ **Hipótesis General** $\leftrightarrow$ **Relación entre VI y VD**.
2. **Problemas Específicos (1 al 3)** $\leftrightarrow$ **Objetivos Específicos (1 al 3)** $\leftrightarrow$ **Hipótesis Específicas (1 al 3)** $\leftrightarrow$ **Dimensiones de la VD (1 al 3)**.

### Dimensiones de la Variable Dependiente (Fijadas por DEC-007):
- **Dimensión 1:** Oportunidad de procesamiento $\rightarrow$ Objetivo Específico 1 $\rightarrow$ Hipótesis Específica 1.
- **Dimensión 2:** Consistencia documental $\rightarrow$ Objetivo Específico 2 $\rightarrow$ Hipótesis Específica 2.
- **Dimensión 3:** Satisfacción del usuario $\rightarrow$ Objetivo Específico 3 $\rightarrow$ Hipótesis Específica 3.

## 2. Alineación de Operacionalización
Cada indicador debe desprenderse exclusivamente de su dimensión:
- **Variable Independiente (SIVAC):** Enfoque Extreme Programming (XP), evaluado con estándar ISO/IEC 25010:2023 (Adecuación funcional y usabilidad).
- **Variable Dependiente (Gestión de Movimientos de Vacunas):**
  - *Dimensión 1: Oportunidad de procesamiento:*
    - Indicador 1.1: Tiempo de registro de movimiento ($T_{reg}$, en minutos).
    - Indicador 1.2: Tiempo de emisión de vale/reporte PECOSA ($T_{vale}$, en minutos).
  - *Dimensión 2: Consistencia documental:*
    - Indicador 2.1: Registros sin discrepancias ($RSD$, porcentaje).
    - Indicador 2.2: Concordancia entre cantidad programada y cantidad entregada ($CPE$, porcentaje).
  - *Dimensión 3: Satisfacción del usuario:*
    - Indicador 3.1: Aceptación del proceso logístico ($AP$, escala Likert 1-5).
    - Indicador 3.2: Utilidad percibida del sistema ($UP$, escala Likert 1-5).

## 3. Criterios de Auditoría
Si en algún borrador se detecta que un objetivo específico no corresponde con su respectiva dimensión o hipótesis, el `guardian-consistencia` debe bloquear la aprobación y emitir una alerta de desalineación.
