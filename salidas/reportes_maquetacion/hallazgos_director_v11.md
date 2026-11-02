# Hallazgos de la Dirección General sobre `informe_final_v11.docx`

**Fecha:** 2026-10-21 · **Fase:** F8 — Integración editorial · **Agente:** director-general
**Base auditada:** `salidas/documentos/informe_final_v11.docx` (813 párrafos, 59 tablas, 2691 celdas)

---

## 1. Códigos internos: inventario completo (30 ocurrencias)

| Ubicación | Ocurrencia | Estado |
|---|---|---|
| P290, P351, P353, P646 (×4), P769, P772, P773, P776, T6 F0 C2, P672 | `DEC-007`, `DEC-019`, `REGLA CANÓNICA`, `datos/recolectados/`, `DATOS DE PRUEBA`, `scripts/estadistica` | Cubiertas por las 11 órdenes de `codigos_internos_v09.json` (ensayo 11/11 sobre v11) |
| **P778** | `DEC-014`, `DEC-016` | **NO cubierta.** El informe del redactor afirmó que solo figuraban en reportes internos; el barrido las localiza en prosa visible |
| **P139, P145** | `[Pendiente]` en el Resumen (español y quechua) | **NO cubierta.** Inadmisible en la cara del documento |
| P778, T46/T47/T48 | `[Por completar por el juez]` | **Se conservan.** Estado real de un dato no asentado, no código de gobernanza |
| T34 F3 C4-C6 | `[Pendiente]` | **Se conservan** (ficha de instrumento en blanco) |

Órdenes complementarias comisionadas al `redactor-academico` en `codigos_internos_extra_v11.json`.

---

## 2. Coherencia numérica verificada (sin defecto)

- Tabla 7: suma de estimaciones = 3+5+3 (Iteración 1) + 5+4 (2) + 8+5+5+4+3+8 (3) + 5+5 (4) + 4+4 (5) = **71 PH**. Coincide con el Resumen y con P359.
- Velocidad declarada 14.2 PH/iteración = 71/5. Coincide.
- Historias de usuario: **15** en Tabla 7, en P355 y en el Resumen.
- Centros de acopio: **diecinueve** mencionado 8 veces en prosa; **trece** con operadores censales, 12 veces. Sin contradicción tras la corrección de la v10.

---

## 3. Observación metodológica abierta (para QG-4)

**Distribución de carga por iteración.** P359 declara una velocidad observada de 14.2 PH por iteración y un plan de cinco iteraciones. La Tabla 7 reparte la carga así: 11, 9, **33**, 10 y 8 PH. La Iteración 3 concentra 2.3 veces la velocidad declarada.

- **No se altera por iniciativa propia:** la asignación de cada historia a su iteración proviene del registro real del proyecto y su modificación sin evidencia constituiría invención.
- **Salidas posibles:** (a) declarar en P359 que la velocidad es un promedio y que la Iteración 3 absorbió el núcleo transaccional (registro de movimientos, saldos M+1, vales PECOSA) por dependencia funcional; (b) que el tesista aporte el registro de iteraciones real para reasignar.
- **Decisión requerida del tesista.** Se eleva en el cierre de esta fase.

---

## 4. Pendientes heredados que siguen vigentes

1. Actualización de campos TOC/TOF/TOT tras las sustituciones de títulos de anexo (P769, P773).
2. Verificación de las páginas de Inarotul Huda et al. (2025, p. 1244) y Gilbert et al. (2020, p. 564).
3. Reemplazo de la marca de datos provisionales en el libro Excel de anexos (comisionado).
4. Recálculo de la r de Rosenthal con |Z|/√N (comisionado).
