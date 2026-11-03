# Concordancia de los instrumentos v06 con la tesis

**Paquete:** `salidas/instrumentos/INSTRUMENTOS_DEFINITIVOS_v06/`. **Fecha:** 2026-11-03.
Cada línea: qué cambió en el instrumento, con qué parte de la tesis queda concorde y qué debe corregirse en la tesis para que no queden dos definiciones.

| # | Cambio en el instrumento | Queda concorde con | Corrección exigida en la tesis |
|---|---|---|---|
| 1 | Cuestionario con 8 reactivos: AP-01 a AP-04 y UP-01 a UP-04, escala única 1–5, rangos 4–20, 4–20 y 8–40. | Codebook (`ap_01`…`up_04`, `score_ap`, `score_up`, `score_tam_total`), Tablas 32 y 45, Ecuaciones 5 y 6, Tabla 38. | Ninguna en el cuerpo: §4.10.2(c) ya declara 8 ítems y los rangos. |
| 2 | Seis enunciados transcritos literales del expediente DEC-007 (AP-01 a AP-04, UP-02, UP-03); UP-01 y UP-04 reformulados (fila 3). | Anexo 3 y Anexo 4 del informe. | El Anexo 4 (Tabla 48) imprime una paráfrasis distinta de los ocho códigos; debe transcribir la redacción de v06. Son dos versiones del mismo instrumento. |
| 3 | UP-01 pierde «en tiempo real» (se responde sobre el kardex manual en el pretest); UP-04 deja de ser un juicio global de eficacia y pasa a una consecuencia concreta. Ningún ítem de satisfacción global se suma dentro de UP. | Estructura 4 + 4 de las Ecuaciones 5 y 6 y del baremo 8–18 / 19–29 / 30–40. | No rotular UP-04 como satisfacción general: D3 mide aceptación del proceso y utilidad percibida, no satisfacción declarada. Los puntajes y el alfa no cambian: dependen de los valores, no de la redacción. |
| 4 | Ficha documental con los 8 criterios (biológico, lote, vencimiento, cantidad, establecimiento, responsable y firmas, saldo aritmético, correlatividad temporal), regla conjuntiva y un identificador por asiento (fecha, tipo, número, lote). Se elimina la fila «unidad registrada». | Ecuación 3, Tabla 45 y Tabla 50, NTS N.° 196-MINSA/DGIESP-2022. | Ninguna: §4.10.2(b) ya enumera los ocho criterios en ese orden. |
| 5 | CPE conforme solo con igualdad exacta entre programado y entregado, en la misma unidad; el documento de ajuste pasa a observación. | Ecuación 4 (Q_entregada = Q_programada). | §4.10.2(b) debe decir que el ajuste es observación y no criterio de conformidad. |
| 6 | Ficha de tiempos con columna «Solicitud de despacho» y definición única T_vale = emisión − solicitud. | Ecuación 2 y §4.10.2(a). | §4.10.2(a) debe retirar el disparador «apertura del formulario» para el vale: el instante inicial es la solicitud. |
| 7 | Tres réplicas válidas por indicador y momento; el valor del trabajador es la mediana de las tres, fuera del formulario. | Ecuación 1 y Tabla 31, en la parte de «k operaciones». | **Pendiente:** la Ecuación 1 y la Tabla 31 dicen «promedio aritmético de las k operaciones» y el formulario fija la mediana de tres. Elegir una y alinear el otro texto; ninguna cifra publicada cambia. |
| 8 | Capacidad real: 40 documentos y 25 despachos por hoja, con «Hoja __ de __» y numeración corrida. | Tabla 31 (n = 14 operadores) y las Ecuaciones 3 y 4. | §4.10.2(b) debe fijar 40 documentos y 25 despachos por operador y momento. Una hoja de 5 filas no permitía alcanzar el 63.57 % publicado. |
| 9 | Certificado de validación en blanco, en tres secciones, con 22 ítems visibles (T-01 a T-04, D-01 a D-10, AP-01 a UP-04) y criterios dicotómicos Pertinencia / Relevancia / Claridad. Sin nombres, sin V, sin dictamen marcado y sin hipótesis de cambio. | Anexo 3. | §4.12 y la Tabla 34 deben retirar «12 componentes en escala de 1 a 4» y el «V = 1.000 comunicado»: con 22 ítems dicotómicos y tres jueces, la V de Aiken se recalcula con c = 2. |
| 10 | Guía de aplicación con los cuatro instantes, las dos fórmulas y once reglas: réplicas, interrupción externa, documento y despacho conformes, hoja de continuación, doble codificación del 20 %, trabajador ausente, dos centros, operación no ocurrida, numeración y porcentajes. | §4.10 y §4.11. | Ninguna: §4.11 ya prevé la doble verificación cruzada del 20 %. |
| 11 | Consentimiento con aprobación por comité de ética o su exención, contacto del investigador y opción de testigo o huella. | §4.13 y requisitos éticos del estudio. | Ninguna. |

## Verificación numérica

Recalculado desde `datos/recolectados/pretest_campo.csv`, `posttest_campo.csv` y el registro por bloque de `SIVAC_DATOS_CAMPO.md`, con las definiciones de los formularios v06. Los 16 chequeos pasan.

| Indicador | Pretest | Postest | Publicado |
|---|---|---|---|
| AP (4 ítems) | 8.07 ± 2.27 | 17.71 ± 1.64 | igual |
| UP (4 ítems) | 9.00 ± 1.88 | 18.50 ± 1.56 | igual |
| Total (8 ítems) | 17.07 ± 4.08 | 36.21 ± 3.09 | igual |
| Alfa total / AP / UP | 0.939 / 0.877 / 0.874 | 0.915 / 0.831 / 0.841 | igual |
| RSD (8 criterios) | 63.57 ± 12.31 | **91.96** ± 4.72 | 91.96 |
| CPE (exacto) | **67.71** ± 11.26 | **88.57** ± 5.63 | 88.57 |

## Cifras de la tesis que cambian

- Tabla 37, §5.2.2, §5.3 y las conclusiones: RSD postest **91.96 %** (no 96.00 %) y CPE **67.71 % → 88.57 %** (no 67.61 % → 95.39 %).
- Tabla 41 y §5.4.2: con esos valores, RSD t(13) = **6.468**, d = **1.73**, p = .00002; CPE t(13) = **4.945**, d = **1.32**, p = .00027. Ambas siguen bajo .001 y la decisión de rechazar H0,2 no cambia.
- Causa: las columnas `rsd` y `cpe` del CSV no son alcanzables con 40 documentos y 25 despachos; el registro por bloque sí. El instrumento no puede cerrar esta diferencia.
