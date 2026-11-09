---
tipo: auditoria
fase: F8_INTEGRACION_EDITORIAL
squad: Squad F
agente: verificador-integridad
estado: completado
fecha: 2026-11-02
documento_auditado: salidas/archivo/REESTRUCTURACION_V22_x/CANDIDATO_EDITORIAL_V22.docx
sha256: 22b65e255ac7d656a6801d21a160f7ab5fd22571bd73fb2e980ca80fc4de169f
modo: solo_lectura
---

# BARRIDO RESIDUAL DEL ESQUEMA INSTRUMENTAL SUPRIMIDO
## Informe Final candidato v22 — auditoría de solo lectura

**Fase:** F8_INTEGRACION_EDITORIAL · **Squad:** F (Integridad) · **Agente:** `verificador-integridad` · **Fecha:** 2026-11-02

---

## 0. Objeto, método y límites

**Documento auditado:** `C:\MisInvestigaciones\tesis\sivac\salidas\archivo\REESTRUCTURACION_V22_x\CANDIDATO_EDITORIAL_V22.docx`
**Tamaño:** 16 130 599 bytes · **SHA-256:** `22b65e255ac7d656a6801d21a160f7ab5fd22571bd73fb2e980ca80fc4de169f`
**Estructura:** 858 párrafos y 59 tablas de primer nivel; cero tablas anidadas.

**Método.** Apertura del contenedor ZIP en memoria y parsing de `word/document.xml` con `lxml`. Recorrido en orden de cuerpo, indexación de párrafos (P1–P858) y tablas (T1–T59), extracción de texto por párrafo y por celda, y búsqueda con expresiones regulares sensibles a mayúsculas y a variantes ortográficas. El conteo por celda es el autoritativo: el conteo sobre el texto concatenado de una tabla subestima los códigos cuando el último carácter de una celda y el primero de la siguiente son ambos alfanuméricos (por ejemplo, `AP-01Aceptación`).

**Límites.** No se copió, modificó, convirtió ni generó PDF del documento auditado. No se accedió a `C:\Proyectos\syncova`, a `referencias\` ni a las carpetas de instrumentos v02, v03 y v04. Las cifras, ecuaciones y resultados estadísticos no se recalcularon: se transcriben tal como figuran.

**Convenciones de localización.**
- `P###` es el ordinal del párrafo en el cuerpo (1–858), no el folio impreso.
- `T##` es el ordinal de la tabla en orden de cuerpo (1–59); «Tabla N» es el rótulo impreso.
- Las tres formas del Anexo 3 son T47, T48 y T49. No llevan rótulo «Tabla N»; el rótulo «Tabla 45» que las precede pertenece a otra tabla.
- «Pasaje A–I» remite a `salidas/documentos/_borradores_v04/PROPUESTA_AJUSTE_INFORME_v04.md`.

**Clases de hallazgo.**
- `contradiccion_metodologica` (CM): el texto afirma algo incompatible con el diseño, con la evidencia disponible o con otra parte del mismo documento.
- `incoherencia_expositiva` (IE): conserva nombres, códigos o estructuras del esquema suprimido sin contradicción lógica interna.
- `residuo_menor` (RM): rastro de nomenclatura o codificación que no altera el argumento, pero debe armonizarse.
- `falso_positivo` (FP): coincidencia léxica legítima (por ejemplo, PECOSA como función del sistema en el capítulo XP).

---

## 1. Resumen ejecutivo

1. Se registraron **192 coincidencias en 98 filas**: 65 `contradiccion_metodologica`, 65 `incoherencia_expositiva`, 50 `residuo_menor` y 12 `falso_positivo`; 182 coincidencias provienen de los diez grupos y 10 son hallazgos adicionales fuera de grupo.
2. Los **diez grupos están presentes**; las ausencias literales se declaran en la sección 2: `REG-03`, `VALE-02`, `VALE-03`, `PU-02`, `PU-03`, `PE-02`, `PE-03`, los códigos `OP-02` a `OP-13` individuales, «módulo complementario», «doce componentes», «escala de uno a cuatro», «c = 4», «cuatro categorías», «coeficiente kappa» en minúscula, «concordancia interobservador», «alfa de Cronbach» en minúscula y «Trabajador N.°».
3. **Hallazgo más grave:** la sección 5.1 y la Tabla 35 presentan alfa de Cronbach de .939 (pretest) y .915 (postest) como mediciones sobre n = 14, con «población censal» y «coeficientes obtenidos»; solo la nota P654, la nota P838 y el preámbulo P648 declaran que son datos de prueba, y P650 afirma «mediciones directas de campo».
4. **Segundo hallazgo:** los tres formatos del Anexo 3 prellenan grado, especialidad, institución, lugar y año, y siguen describiendo «12 componentes» y «Modalidad A»; P821 los declara «en blanco», lo que es falso tal como están.
5. **Tercer hallazgo:** el informe afirma aplicación de instrumentos y datos de campo en P616, P612–P614, P578, P633, P650, P652, P834 y P849, contradicho por P648, P654, P838, P840 y P842.

---

## 2. Declaración de presencia y ausencia de los diez grupos

| Grupo | Términos y conteo literal | Ausencias literales | Ubicaciones principales |
|---|---|---|---|
| 1. Códigos de registro y vale | `REG-01` 3 · `REG-02` 3 · `VALE-01` 3 | `REG-03` 0 · `VALE-02` 0 · `VALE-03` 0 | P616, T34.r2c5, T35.r2c3 |
| 2. Códigos PU/PE | `PU-01` 2 · `PU-04` 2 · `PE-01` 2 · `PE-04` 2 | `PU-02` 0 · `PU-03` 0 · `PE-02` 0 · `PE-03` 0 | P616, T34.r4c5; se imprimen solo como rangos «PU-01 a PU-04» y «PE-01 a PE-04» |
| 3. Códigos AP/UP | `AP-01` 12 · `AP-02` 1 · `AP-03` 1 · `AP-04` 12 · `UP-01` 12 · `UP-02` 1 · `UP-03` 1 · `UP-04` 12 | Ninguna | P579, P603, P605, P606, P608, P616, P624, T32.r6c2, T32.r7c2, T33.r5c4, T34.r4c5, T35.r4c3, T45.r20c2, T46.r5c4, T52.r2–r9 |
| 4. Modalidades y módulos | «Modalidad A» 29 · «Modalidad B» 4 · «modalidades A y B» 1 · «módulo anexo» 1 | «módulo complementario» 0 | P616, P622, P624, P626, P630, P650, P651, P672, P674, P728, P821, P832, P837, P838, T30, T32, T34, T35, T36, T45, T47–T49 |
| 5. Escala experta y componentes | «12 componentes» 7 · «escala experta de 1 a 4» 4 | «doce componentes» 0 · «escala de uno a cuatro» 0 · «c = 4» 0 · «cuatro categorías» 0 | P626, P630, P821, T35.r5, T47–T49. Equivalente semántico: P628 «que en el formato disponible es 4» |
| 6. Concordancia | «Kappa» 2 · «kappa» 2 · «coeficiente Kappa» 2 · «concordancia interevaluador» 2 · «calibración interobservador» 1 · «inter-observador» 1 · `ICC(2,1)` 2 · «correlación intraclase» 1 | «coeficiente kappa» 0 (exacto; 2 insensible a caso) · «concordancia interobservador» 0 | P178, P620, P621, P628, T35.r2c4, T35.r3c4 |
| 7. PECOSA y escenarios | `PECOSA` 15 · «disparadores unívocos» 5 · «escenarios operativos» 1 exacto (P616) · «Escenarios operativos» 1 (T35.r2c3) · «Escenario Operativo Evaluado» 1 (T28.r1c3) | «escenario operativo» 0 exacto | PECOSA: T4, T5, T8, T9, T10, T18, T26, T27, T28, T30, T32, P594, P616, T50, T55. Disparadores: P178, P620, P621, P650 |
| 8. Códigos OP | `OP-01` 2 · `OP-14` 2 | `OP-02` a `OP-13` 0 individuales; solo el rango «OP-01 a OP-14» | P578, P644 |
| 9. Fichas y guías | «Ficha de Registro Cronométrico» 8 · «Ficha de Auditoría y Cotejo» 7 · «Guía de cotejo» 2 + «guía de cotejo» 3 + «guías de cotejo» 1 | Ninguna | P140, P152, P178, P616, P621, P650, P660, P821, P830, P833, P834, T34, T35, T45 |
| 10. Alfa de Cronbach | «Alfa de Cronbach» 10 | «alfa de Cronbach» 0 exacto (10 insensible a caso) | P121, P221, P622, P624, P651, P652, P653, P838, T36 |

**Término adicional verificado:** «Trabajador N.°» 0 ocurrencias; «Trabajador N» 0; «trabajador N.°» 0.

**Nota de lectura.** El grupo 7 requiere precisión: «escenarios operativos» en minúscula aparece una sola vez (P616, descripción del Instrumento 01); «Escenarios operativos» con mayúscula aparece en T35.r2c3 (estructura del mismo instrumento); «Escenario Operativo Evaluado» aparece en T28.r1c3 como rótulo de una prueba de aceptación XP y es un falso positivo. El grupo 6 requiere la misma precisión: «coeficiente kappa» en minúscula no aparece; «coeficiente Kappa» aparece dos veces (P178, P621).

---

## 3. Tabla completa de coincidencias

**Orden:** por gravedad (`CM` → `IE` → `RM` → `FP`) y, dentro de cada clase, por orden de aparición en el documento. La clase asignada es la del hallazgo dominante de la fila; cuando una fila mezcla naturalezas (por ejemplo, P178 contiene un alfa legítimo junto a un Kappa improcedente), la acción separa el tratamiento. Los fragmentos se recortan a 200 caracteres; los corchetes `[...]` indican omisión.

**Leyenda de grupos:** `1` REG/VALE · `2` PU/PE · `3` AP/UP · `4` Modalidad · `4b` módulo anexo · `5` «12 componentes» · `5b` escala 1-4 · `6` kappa · `6b` interevaluador · `6c` ICC · `6d` correlación intraclase · `7` PECOSA · `7b` escenarios · `7c` disparadores · `8` OP · `9` ficha cronométrica · `9b` ficha de auditoría · `9c` guía de cotejo · `10` alfa de Cronbach.

| # | Grav. | Ubicación | Términos (grupo) | Fragmento literal (≤200 caracteres) | Clase | Acción recomendada |
|---:|---|---|---|---|---|---|
| 1 | CM | 1.3.3 Justificación metodológica (P178) | 6/6b/7c/9c/10 — Kappa, interevaluador, disparadores, guía de cotejo, alfa | «…estandarizado de observación con disparadores unívocos y el coeficiente Kappa de Cohen para las fichas de tiempos y la guía de cotejo documental.» | `contradiccion_metodologica` | Reescribir el literal (c): retirar Kappa e interevaluador; declarar protocolo único y repetibilidad; renombrar la guía; mantener el alfa como estimación futura. |
| 2 | CM | Tabla 33, fila 4, columna 5 | 2/3/4 — PU/PE, AP/UP, Modalidad A/B | «…del postest, con 4 ítems para Utilidad percibida del software (PU-01 a PU-04) y 4 para Facilidad de uso percibida (PE-01 a PE-04). No aditiva respecto de la Modalidad A.» | `contradiccion_metodologica` | Sustituir la Tabla 33 completa (pasaje B); eliminar Modalidad B y los códigos PU/PE. |
| 3 | CM | 4.10.2 Instrumentos de recolección de datos (P616) | 1/2/3/4/4b/7/7b/7c/9/9b — REG/VALE, PU/PE, AP/UP, modalidades, PECOSA, fichas | «En correspondencia directa con las técnicas descritas, se diseñaron y aplicaron tres instrumentos de recolección de datos [...] (REG-01: registro de ingreso de lote de vacuna; REG-02: registro de sal…» | `contradiccion_metodologica` | Sustituir el párrafo por el texto del pasaje A; eliminar «se aplicaron», REG/VALE, PU/PE y Modalidad B. |
| 4 | CM | 4.11 Confiabilidad de los instrumentos (P620) | 7c — disparadores unívocos | «… se asegurará mediante un protocolo estandarizado de cronometraje con disparadores unívocos de inicio (apertura del formulario de captura) y corte (confirmación de guardado y emisión), complementado…» | `contradiccion_metodologica` | Sustituir por el texto del pasaje C; retirar la calibración interobservador y los disparadores. |
| 5 | CM | 4.11 Confiabilidad de los instrumentos (P621) | 6/6b/9c — Kappa, interevaluador, guía de cotejo | «…de la concordancia interevaluador a través del coeficiente Kappa de Cohen (proporción de concordancia observada corregida por la concordancia esperada por azar), reconociendo…» | `contradiccion_metodologica` | Sustituir por el texto del pasaje D; retirar Kappa, κ ≥ 0.80 y la guía de cotejo. |
| 6 | CM | 4.12 Validez de los instrumentos (P628) | 6/6c/6d — kappa, ICC(2,1), correlación intraclase | «…de correlación intraclase ICC(2,1) mayor o igual a 0.75 y el kappa de Cohen mayor o igual a 0.80, que son evidencias de confiabilidad y no de validez de contenido.» | `contradiccion_metodologica` | Sustituir por el texto del pasaje F; eliminar ICC(2,1), kappa y correlación intraclase. |
| 7 | CM | Tabla 34, fila 2, columna 4 | 6c — ICC(2,1) | «Confiabilidad por protocolo PMMV e ICC(2,1) ≥ 0.75 entre observadores» | `contradiccion_metodologica` | Sustituir la Tabla 34 completa (pasaje G); retirar ICC(2,1) y PMMV. |
| 8 | CM | Tabla 34, fila 3, columna 4 | 6 — kappa | «Confiabilidad por regla de 8 criterios y kappa de Cohen ≥ 0.80 entre evaluadores» | `contradiccion_metodologica` | Sustituir la Tabla 34 completa (pasaje G); retirar kappa. |
| 9 | CM | 4.12 Validez de los instrumentos, nota (P630) | 4/5/5b — Modalidad A, 12 componentes, escala 1-4 | «…AP/UP) en escala experta de 1 a 4, y el cuestionario TAM de la Modalidad A con 8 reactivos en escala Likert de 1 a 5. Para este formato, la unanimidad de calificaciones 4 comunicada co…» | `contradiccion_metodologica` | Sustituir la nota por la del pasaje F; retirar V = 1.000 e IVC = 1.000. |
| 10 | CM | 5.1 Análisis de Confiabilidad del Instrumento 03 (P650) | 9/9b — fichas cronométrica y de auditoría | «[...] los Instrumentos N.° 01 (Ficha de Registro Cronométrico de Tiempos Operativos) y N.° 02 (Ficha de Auditoría y Cotejo Documental de Lotes y Kardex) corresponden a mediciones directas de campo y…» | `contradiccion_metodologica` | Reescribir la introducción de 5.1 con los nombres v04; eliminar «mediciones directas de campo» y PMMV. |
| 11 | CM | 5.1 Análisis de Confiabilidad del Instrumento 03 (P651) | 4/10 — Modalidad A, alfa | «[...] se calculó el coeficiente Alfa de Cronbach (Cronbach, 1951) [...] la escala global TAM arrojó un coeficiente Alfa de Cronbach de .939 (IC 95%: [0.874, 0.977]) [...] en la medición del postest […» | `contradiccion_metodologica` | Reescribir 5.1: declarar que los coeficientes son de datos de prueba o diferirlos; no presentarlos como medición del pretest/postest. |
| 12 | CM | 4.10.1 Técnicas de recolección de datos (P612) | — (fuera de los 10 grupos) — afirmación de aplicación | «a) Observación directa cronometrada: Se aplicó para medir in situ y de manera no intrusiva la duración exacta de las operaciones de registro de movimientos y de emisión de vales de salida ejecutadas…» | `contradiccion_metodologica` | Reformular en futuro/diseño («se aplicará») o eliminar la afirmación de ejecución. |
| 13 | CM | 4.10.1 Técnicas de recolección de datos (P613) | — (fuera de los 10 grupos) — afirmación de aplicación | «b) Análisis documental (auditoría de registros): Se utilizó para examinar de forma sistemática y retrospectiva los asientos del kardex físico, las solicitudes de requerimiento y las guías de remisión…» | `contradiccion_metodologica` | Reformular en futuro/diseño o eliminar la afirmación de ejecución. |
| 14 | CM | 4.10.1 Técnicas de recolección de datos (P614) | — (fuera de los 10 grupos) — afirmación de aplicación | «c) Encuesta psicométrica: Se administró al personal censal de inmunizaciones con el propósito de recabar su valoración estructurada sobre la aceptación del proceso y la utilidad percibida en ambas et…» | `contradiccion_metodologica` | Reformular en futuro/diseño o eliminar la afirmación de ejecución. |
| 15 | CM | 4.8 Unidad de análisis (P578) | 8 — OP-01 a OP-14; «recolectados en campo» | «Las unidades de observación primarias correspondieron a los eventos transaccionales específicos recolectados en campo [...] la unidad de análisis estadístico quedó constituida por cada uno de los cat…» | `contradiccion_metodologica` | Eliminar «recolectados en campo»; sustituir OP-01..OP-14 por «Trabajador N.° 01 a 14». |
| 16 | CM | 4.13 Técnicas estadísticas (P633) | — (fuera de los 10 grupos) — datos recolectados | «El procesamiento estadístico de los datos recolectados en el pretest y postest se estructuró mediante rutinas computacionales reproducibles en Python (scipy.stats, statsmodels, pingouin) y el entorno…» | `contradiccion_metodologica` | Sustituir «datos recolectados» por «datos de prueba» o por el plan de procesamiento. |
| 17 | CM | 5.1 Análisis de Confiabilidad del Instrumento 03 (P652) | — (fuera de los 10 grupos) — lectura de resultados | «Los coeficientes observados superan el umbral psicométrico de .800 [...] ratifica la precisión de la estimación sobre la población censal de 14 trabajadores [...] evidenciando que los reactivos captu…» | `contradiccion_metodologica` | Eliminar la lectura de resultados sobre la población censal; remitir a la nota de datos de prueba. |
| 18 | CM | Anexo 4, nota de la Tabla 46 (P834) | — (fuera de los 10 grupos) — «ficha aplicada» | «Nota. Ficha de cronometraje aplicada a los 14 operadores en los trece (13) centros de acopio de la DISA Apurímac II.» | `contradiccion_metodologica` | Sustituir por la nota del pasaje I; eliminar «aplicada a los 14 operadores». |
| 19 | CM | Anexo 7 (P849) | — (fuera de los 10 grupos) — evidencia de aplicación | «ANEXO 7: REGISTRO FOTOGRÁFICO DE EVIDENCIA DE APLICACIÓN EN CAMPO (PENDIENTE DE INCORPORACIÓN)» | `contradiccion_metodologica` | Retitular como registro fotográfico pendiente, sin afirmar aplicación en campo. |
| 20 | CM | Tabla 34, fila 5, columna 5 | — (fuera de los 10 grupos) — V de Aiken | «1.000 comunicado (condicional)» | `contradiccion_metodologica` | Eliminar «1.000 comunicado»; sustituir la Tabla 34 (pasaje G). |
| 21 | CM | Tabla 34, fila 5, columna 6 | — (fuera de los 10 grupos) — IVC | «1.000 comunicado (condicional)» | `contradiccion_metodologica` | Eliminar «1.000 comunicado»; sustituir la Tabla 34 (pasaje G). |
| 22 | IE | Tabla 29, fila 2, columna 2 | 4/7 — Modalidad A, PECOSA | «…in situ de registros y vales PECOSA físicos, y aplicación de la Modalidad A del Instrumento N.° 03 en línea base.» | `incoherencia_expositiva` | Sustituir «Modalidad A» por «cuestionario de satisfacción» y PECOSA por «comprobante de salida o vale». |
| 23 | IE | Tabla 29, fila 5, columna 2 | 4 — modalidades A y B | «…cronometraje digital de operaciones y vales, y aplicación de las modalidades A y B del Instrumento N.° 03 tras la intervención.» | `incoherencia_expositiva` | Sustituir «modalidades A y B» por «cuestionario de satisfacción». |
| 24 | IE | Tabla 33, fila 2, columna 4 | 9 — Ficha de Registro Cronométrico | «Instrumento N.° 01:Ficha de Registro Cronométrico de Tiempos Operativos» | `incoherencia_expositiva` | Sustituir por el título v04 (pasaje B). |
| 25 | IE | Tabla 33, fila 2, columna 5 | 1/7c — REG/VALE, disparadores | «Escenarios estandarizados (REG-01, REG-02 y VALE-01) con disparadores unívocos de cronometraje» | `incoherencia_expositiva` | Sustituir por la estructura v04 (pasaje B). |
| 26 | IE | Tabla 33, fila 3, columna 4 | 9b — Ficha de Auditoría y Cotejo | «Instrumento N.° 02:Ficha de Auditoría y Cotejo Documental de Lotes y Kardex» | `incoherencia_expositiva` | Sustituir por el título v04 (pasaje B). |
| 27 | IE | Tabla 33, fila 4, columna 4 | 4 — Modalidad A | «…N.° 03:Cuestionario de Satisfacción del Usuario bajo el Modelo TAM (Modalidad A)» | `incoherencia_expositiva` | Sustituir por el título v04 (pasaje B). |
| 28 | IE | 4.11 Confiabilidad de los instrumentos (P622) | 4/10 — Modalidad A, alfa | «Para el Instrumento N.° 03, en su Modalidad A oficial de 8 ítems en escala Likert de 1 a 5, la confiabilidad por consistencia interna se determinará median…» | `incoherencia_expositiva` | Sustituir «Modalidad A» por «cuestionario de ocho reactivos» (pasaje E). |
| 29 | IE | 4.11 Confiabilidad de los instrumentos (P624) | 3/4/10 — AP/UP, modalidades, alfa | «La Modalidad B no forma parte de esa estimación y, de reportarse su consistencia interna, se presentará como indicador descriptivo separado, sin agregación con la Modalidad A.» | `incoherencia_expositiva` | Eliminar el párrafo de Modalidad B (pasaje E). |
| 30 | IE | 4.12 Validez de los instrumentos (P626) | 4/5/5b — Modalidad A, 12 componentes, escala 1-4 | «El juicio se aplicará al formato disponible, integrado por la matriz de la variable dependiente con 12 componentes (4 campos de las dimensiones 1 y 2 y 8 reactivos AP/UP) en escala experta de 1 a 4,…» | `incoherencia_expositiva` | Sustituir por el texto del pasaje F (16 ítems, c = 2). |
| 31 | IE | Tabla 34, fila 2, columna 2 | 9 — Ficha de Registro Cronométrico | «Instrumento N.° 01:Ficha de Registro Cronométrico de Tiempos Operativos» | `incoherencia_expositiva` | Sustituir la Tabla 34 (pasaje G). |
| 32 | IE | Tabla 34, fila 2, columna 3 | 1/7b/7c — REG/VALE, escenarios, disparadores | «Escenarios operativos REG-01, REG-02 y VALE-01 con disparadores unívocos de cronometraje» | `incoherencia_expositiva` | Sustituir la Tabla 34 (pasaje G). |
| 33 | IE | Tabla 34, fila 3, columna 2 | 9b — Ficha de Auditoría y Cotejo | «Instrumento N.° 02:Ficha de Auditoría y Cotejo Documental de Lotes y Kardex» | `incoherencia_expositiva` | Sustituir la Tabla 34 (pasaje G). |
| 34 | IE | Tabla 34, fila 4, columna 2 | 4 — Modalidad A | «…N.° 03:Cuestionario de Satisfacción del Usuario bajo el Modelo TAM (Modalidad A)» | `incoherencia_expositiva` | Sustituir la Tabla 34 (pasaje G). |
| 35 | IE | Tabla 34, fila 4, columna 4 | 4 — Modalidad A | «Juicio de contenido sobre el formato disponible de la Modalidad A» | `incoherencia_expositiva` | Sustituir la Tabla 34 (pasaje G). |
| 36 | IE | Tabla 34, fila 5, columna 3 | 5/5b — 12 componentes, escala 1-4 | «12 componentes (4 campos de las dimensiones 1 y 2 y 8 reactivos AP/UP) en escala experta de 1 a 4» | `incoherencia_expositiva` | Sustituir la Tabla 34 (pasaje G). |
| 37 | IE | 4.14 Consideraciones éticas (P644) | 8 — OP-01 a OP-14 | «[...] el anonimato de sus datos personales mediante la asignación de identificadores alfanuméricos correlativos (OP-01 a OP-14).» | `incoherencia_expositiva` | Sustituir OP-01..OP-14 por «Trabajador N.° 01 a 14». |
| 38 | IE | 5.2.1, nota de tabla (P660) | 9 — Ficha de Registro Cronométrico | «Nota. n = 14 operadores de la DISA Apurímac II. [...] Fuente: Ficha de Registro Cronométrico SIVAC (2026).» | `incoherencia_expositiva` | Sustituir la fuente por «Ficha de observación de tiempos (2026)». |
| 39 | IE | 5.2.2, nota de tabla (P667) | — (fuera de los 10 grupos) — Ficha de Cotejo | «Nota. n = 14 operadores censales. [...] Fuente: Ficha de Cotejo Documental de Lotes y Kardex (2026).» | `incoherencia_expositiva` | Sustituir la fuente por «Ficha de observación documental (2026)». |
| 40 | IE | 5.2.3 Dimensión 3 (P672) | 4 — Modalidad A | «[...] el Puntaje Global TAM (Modalidad A, escala sumativa de 8 a 40 puntos) evolucionó de 17.07 puntos [...] a 36.21 puntos.» | `incoherencia_expositiva` | Sustituir «Modalidad A» por «cuestionario de satisfacción». |
| 41 | IE | 5.2.3, nota de tabla (P674) | 4 — Modalidad A | «Nota. Evaluado mediante el Cuestionario TAM, Modalidad A. Escala Likert de 1 a 5. [...] Muestra censal n = 14.» | `incoherencia_expositiva` | Sustituir «Modalidad A» por «cuestionario de satisfacción». |
| 42 | IE | 5.4.3, nota de tabla (P728) | 4 — Modalidad A | «Nota. Evaluado con la Modalidad A del Instrumento 03. gl = 13. [...]» | `incoherencia_expositiva` | Sustituir «Modalidad A del Instrumento 03» por «Instrumento N.° 03». |
| 43 | IE | Tabla 35, fila 2, columna 2 | 4 — Modalidad A | «Escala Global TAM (Modalidad A)» | `incoherencia_expositiva` | Sustituir «Modalidad A» por «cuestionario de ocho reactivos». |
| 44 | IE | Tabla 35, fila 5, columna 2 | 4 — Modalidad A | «Escala Global TAM (Modalidad A)» | `incoherencia_expositiva` | Sustituir «Modalidad A» por «cuestionario de ocho reactivos». |
| 45 | IE | Tabla 44 (Anexo 1), fila 16, columna 2 | 4/9c — Modalidad A, guía de cotejo | «Instrumentos Oficiales: • Ficha de observación de tiempos (Inst. 01) • Guía de cotejo documental (Inst. 02) • Cuestionario de satisfacción y aceptación tecnológica (Inst. 03, Modalidad A)» | `incoherencia_expositiva` | Sustituir los nombres por los v04 y eliminar Modalidad A. |
| 46 | IE | Tabla 44 (Anexo 1), fila 20, columna 2 | 3/4 — AP/UP, Modalidad A | «Dimensión 3: Satisfacción del usuario • Aceptación del proceso (AP; reactivos AP-01 a AP-04 [...] ) • Utilidad percibida (UP; reactivos UP-01 a UP-04 [...] ) • Total de la dimensión sobre los 8 ítems…» | `incoherencia_expositiva` | Eliminar «Modalidad A» y referir «ocho reactivos». |
| 47 | IE | Anexo 3, párrafo introductorio (P821) | 5/5b — 12 componentes, escala 1-4 | «Se presentan los tres (3) formatos de evaluación en blanco por juicio de expertos, que remiten al formato disponible descrito en la sección 4.12: matriz de la variable dependiente con 12 componentes…» | `incoherencia_expositiva` | Sustituir por el texto del pasaje H. |
| 48 | IE | Anexo 3, Formato Juez 1 (T47), celda «Instrumentos Auditados» | 4/5 — Modalidad A, 12 componentes | «…dependiente (12 componentes, escala de 1 a 4) y Cuestionario TAM (Modalidad A, ocho ítems Likert).» | `incoherencia_expositiva` | Sustituir la celda por el texto del pasaje H; corregir además grado, especialidad, institución y fecha prellenados. |
| 49 | IE | Anexo 3, Formato Juez 2 (T48), celda «Instrumentos Auditados» | 4/5 — Modalidad A, 12 componentes | «…dependiente (12 componentes, escala de 1 a 4) y Cuestionario TAM (Modalidad A, ocho ítems Likert).» | `incoherencia_expositiva` | Sustituir la celda por el texto del pasaje H; corregir además grado, especialidad, institución y fecha prellenados. |
| 50 | IE | Anexo 3, Formato Juez 3 (T49), celda «Instrumentos Auditados» | 4/5 — Modalidad A, 12 componentes | «…dependiente (12 componentes, escala de 1 a 4) y Cuestionario TAM (Modalidad A, ocho ítems Likert).» | `incoherencia_expositiva` | Sustituir la celda por el texto del pasaje H; corregir además grado, especialidad, institución y fecha prellenados. |
| 51 | IE | Anexo 4, lista de instrumentos (P830) | 9 — Ficha de Registro Cronométrico | «1. Instrumento N.° 01: Ficha de Registro Cronométrico de Tiempos Operativos (Treg y Tvale).» | `incoherencia_expositiva` | Sustituir por el título v04. |
| 52 | IE | Anexo 4, lista de instrumentos (P831) | 9b — Ficha de Auditoría y Cotejo | «2. Instrumento N.° 02: Ficha de Auditoría y Cotejo Documental de Lotes y Kardex (RSD y CPE).» | `incoherencia_expositiva` | Sustituir por el título v04. |
| 53 | IE | Anexo 4, lista de instrumentos (P832) | 4 — Modalidad A | «3. Instrumento N.° 03: Cuestionario de Satisfacción del Usuario bajo el Modelo TAM (Modalidad A: AP y UP).» | `incoherencia_expositiva` | Sustituir por el título v04 sin Modalidad A. |
| 54 | IE | Anexo 4, título de la Tabla 46 (P833) | 9 — Ficha de Registro Cronométrico | «Tabla 46 Instrumento N.° 01: Ficha de Registro Cronométrico de Tiempos Operativos» | `incoherencia_expositiva` | Sustituir por el título del pasaje I. |
| 55 | IE | Tabla 46 (Anexo 4), fila 3, columna 3 | 7 — PECOSA | «…la orden de despacho hasta la generación física o digital del vale PECOSA» | `incoherencia_expositiva` | Sustituir «vale PECOSA» por «comprobante de salida o vale» en el cuerpo de la Tabla 46. |
| 56 | IE | Anexo 4, título de la Tabla 47 (P835) | 9b — Ficha de Auditoría y Cotejo | «Tabla 47 Instrumento N.° 02: Ficha de Auditoría y Cotejo Documental de Lotes» | `incoherencia_expositiva` | Sustituir por el título del pasaje I. |
| 57 | IE | Anexo 4, título de la Tabla 48 (P837) | 4 — Modalidad A | «… 48 Instrumento N.° 03: Cuestionario TAM de Satisfacción del Usuario (Modalidad A)» | `incoherencia_expositiva` | Sustituir por el título del pasaje I. |
| 58 | RM | Resumen (P140) | 9c — «guías de cotejo documental» | «…guías de cotejo documental bajo la NTS N.° 196-MINSA/DGIESP-2022… cuyos estadísticos definitivos de campo se encuentran en fase de consolidación postest.» | `residuo_menor` | Homologar a «ficha de observación de tiempos» y «ficha de observación documental». |
| 59 | RM | Introducción (P152) | 9c — «guía de cotejo documental» | «[...] se diseñaron tres instrumentos: una ficha de observación de tiempos cronometrados, una guía de cotejo documental de kardex y vales de salida, y un cuestionario psicométrico en escala Likert.» | `residuo_menor` | Homologar a los nombres v04. |
| 60 | RM | Lista de tablas (P121) | 10 — alfa de Cronbach | «Tabla 35 Confiabilidad de consistencia interna del Cuestionario TAM (Instrumento N.° 03) mediante el coeficiente Alfa de Cronbach e intervalo de confianza del 95%» | `residuo_menor` | Actualizar el índice de tablas tras renumerar. |
| 61 | RM | Lista de tablas (P132) | 9 — Ficha de Registro Cronométrico | «Tabla 46 Instrumento N.° 01: Ficha de Registro Cronométrico de Tiempos Operativos» | `residuo_menor` | Actualizar el índice de tablas tras renumerar. |
| 62 | RM | Lista de tablas (P133) | 9b — Ficha de Auditoría y Cotejo | «Tabla 47 Instrumento N.° 02: Ficha de Auditoría y Cotejo Documental de Lotes» | `residuo_menor` | Actualizar el índice de tablas tras renumerar. |
| 63 | RM | Lista de tablas (P134) | 4 — Modalidad A | «Tabla 48 Instrumento N.° 03: Cuestionario TAM de Satisfacción del Usuario (Modalidad A)» | `residuo_menor` | Actualizar el índice de tablas tras renumerar. |
| 64 | RM | 4.8 Unidad de análisis (P579) | 3 — AP/UP | «…subescala de 4 ítems (rango de 4 a 20 puntos), correspondiendo a AP-01 a AP-04 y a UP-01 a UP-04.» | `residuo_menor` | Mantener AP/UP si el cuestionario v04 conserva 8 reactivos; si no imprime códigos, retirar la codificación. |
| 65 | RM | Tabla 31, fila 3, columna 2 | 7 — PECOSA | «Eventos de confección y emisión de comprobantes de salida o vales PECOSA.» | `residuo_menor` | Homologar a «comprobante de salida o vale». |
| 66 | RM | Tabla 31, fila 6, columna 2 | 3/4 — AP/UP, Modalidad A | «Respuestas individuales a los reactivos AP-01 a AP-04 del cuestionario psicométrico de la Modalidad A.» | `residuo_menor` | Alinear con la codificación que imprima el cuestionario v04. |
| 67 | RM | Tabla 31, fila 7, columna 2 | 3/4 — AP/UP, Modalidad A | «Respuestas individuales a los reactivos UP-01 a UP-04 del cuestionario psicométrico de la Modalidad A.» | `residuo_menor` | Alinear con la codificación que imprima el cuestionario v04. |
| 68 | RM | Tabla 32, fila 5, columna 4 | 3 — AP/UP | «Aceptación del proceso operativo (AP: reactivos AP-01 a AP-04)Utilidad percibida para la gestión (UP: reactivos UP-01 a UP-04)» | `residuo_menor` | Alinear con la codificación que imprima el cuestionario v04. |
| 69 | RM | 4.9.2 Variable dependiente (P594) | 7 — PECOSA | «…al tiempo promedio de emisión de comprobante de salida o vale PECOSA para el operador i, se determinó a través de la Ecuación 2:» | `residuo_menor` | Homologar «vale PECOSA» a «comprobante de salida o vale». |
| 70 | RM | 4.9.2 Variable dependiente (P603) | 3 — AP/UP | «…sumativo directo obtenido por el operador i en los cuatro reactivos AP-01 a AP-04 que integran la subescala de aceptación del proceso operativo, según la Ecuación 5:» | `residuo_menor` | Mantener si el cuestionario conserva 4 + 4 reactivos; alinear códigos con el impreso. |
| 71 | RM | 4.9.2 Variable dependiente (P605) | 3 — AP/UP | «…ordinal asignada por el operador i al reactivo j (del reactivo AP-01 al reactivo AP-04) en la escala Likert de 1 a 5 puntos, arrojando un puntaje sumativo acotado en el intervalo…» | `residuo_menor` | Mantener si el cuestionario conserva 4 + 4 reactivos; alinear códigos con el impreso. |
| 72 | RM | 4.9.2 Variable dependiente (P606) | 3 — AP/UP | «…frío, calculándose como el puntaje sumativo en los cuatro reactivos UP-01 a UP-04 de la subescala correspondiente mediante la Ecuación 6:» | `residuo_menor` | Mantener si el cuestionario conserva 4 + 4 reactivos; alinear códigos con el impreso. |
| 73 | RM | 4.9.2 Variable dependiente (P608) | 3 — AP/UP | «…las puntuaciones otorgadas por el operador i a los reactivos UP-01 a UP-04 en la escala Likert de 1 a 5 puntos, configurando un puntaje sumativo individual comprendido entre 4 …» | `residuo_menor` | Mantener si el cuestionario conserva 4 + 4 reactivos; alinear códigos con el impreso. |
| 74 | RM | Tabla 34, fila 4, columna 3 | 3 — AP/UP | «8 ítems Likert de 1 a 5: AP-01 a AP-04 (Aceptación del proceso) y UP-01 a UP-04 (Utilidad percibida)» | `residuo_menor` | Se sustituye con la Tabla 34 (pasaje G). |
| 75 | RM | 5.1, título de la Tabla 35 (P653) | 10 — alfa de Cronbach | «…del Cuestionario TAM (Instrumento N.° 03) mediante el coeficiente Alfa de Cronbach e intervalo de confianza del 95%» | `residuo_menor` | Renumerar la tabla si cambia el orden. |
| 76 | RM | Tabla 35, encabezado | 10 — alfa de Cronbach | «Alfa de Cronbach» | `residuo_menor` | Mantener el encabezado; renumerar la tabla. |
| 77 | RM | Tabla 45 (Anexo 2), fila 5, columna 4 | 3 — AP/UP | «Aceptación del proceso operativo (AP: reactivos AP-01 a AP-04)Utilidad percibida para la gestión (UP: reactivos UP-01 a UP-04)» | `residuo_menor` | Alinear con la codificación que imprima el cuestionario v04. |
| 78 | RM | Tabla 48, fila 2, columna 1 | 3 — AP-01 | «AP-01» | `residuo_menor` | Si el cuestionario v04 no imprime AP/UP, sustituir la columna «Ítem» por numeración 1-8. |
| 79 | RM | Tabla 48, fila 3, columna 1 | 3 — AP-02 | «AP-02» | `residuo_menor` | Si el cuestionario v04 no imprime AP/UP, sustituir la columna «Ítem» por numeración 1-8. |
| 80 | RM | Tabla 48, fila 4, columna 1 | 3 — AP-03 | «AP-03» | `residuo_menor` | Si el cuestionario v04 no imprime AP/UP, sustituir la columna «Ítem» por numeración 1-8. |
| 81 | RM | Tabla 48, fila 5, columna 1 | 3 — AP-04 | «AP-04» | `residuo_menor` | Si el cuestionario v04 no imprime AP/UP, sustituir la columna «Ítem» por numeración 1-8. |
| 82 | RM | Tabla 48, fila 6, columna 1 | 3 — UP-01 | «UP-01» | `residuo_menor` | Si el cuestionario v04 no imprime AP/UP, sustituir la columna «Ítem» por numeración 1-8. |
| 83 | RM | Tabla 48, fila 7, columna 1 | 3 — UP-02 | «UP-02» | `residuo_menor` | Si el cuestionario v04 no imprime AP/UP, sustituir la columna «Ítem» por numeración 1-8. |
| 84 | RM | Tabla 48, fila 8, columna 1 | 3 — UP-03 | «UP-03» | `residuo_menor` | Si el cuestionario v04 no imprime AP/UP, sustituir la columna «Ítem» por numeración 1-8. |
| 85 | RM | Tabla 48, fila 9, columna 1 | 3 — UP-04 | «UP-04» | `residuo_menor` | Si el cuestionario v04 no imprime AP/UP, sustituir la columna «Ítem» por numeración 1-8. |
| 86 | RM | Anexo 4, nota de la Tabla 48 (P838) | 4/10 — Modalidad A, alfa | «Nota. Cuestionario TAM de ocho ítems (Modalidad A) remitido a juicio de expertos. [...] El coeficiente Alfa de Cronbach reportado en la Tabla 35 corresponde a un cálculo provisional sobre datos de pr…» | `residuo_menor` | Mantener la nota; ajustar la referencia a la tabla si se renumera. |
| 87 | FP | 2.2 Antecedentes nacionales (P221) | 10 — alfa de Cronbach | «… 0.95 (IC 95%: 0.84–0.98), una consistencia interna sobresaliente con Alfa de Cronbach α = 0.968 y un ajuste factorial óptimo (CFI = 1.000, TLI = 1.001); asimismo, el 81.7% de los profesionales de…» | `falso_positivo` | Sin acción: alfa reportado por un antecedente. |
| 88 | FP | Tabla 3, fila 4, columna 3 | 7 — PECOSA | «…cálculo de entregas adicionales y emisión de vales oficiales PECOSA.» | `falso_positivo` | Sin acción: PECOSA es función del sistema, no del instrumento. |
| 89 | FP | Tabla 4, fila 14, columna 2 | 7 — PECOSA | «Emisión Instantánea de Vales Oficiales (PECOSA)» | `falso_positivo` | Sin acción: PECOSA es función del sistema, no del instrumento. |
| 90 | FP | Tabla 7, fila 12, columna 2 | 7 — PECOSA | «Emisión Instantánea de Vales Oficiales PECOSA» | `falso_positivo` | Sin acción: PECOSA es función del sistema, no del instrumento. |
| 91 | FP | Tabla 8, fila 4, columna 2 | 7 — PECOSA | «… y Despacho Oficial (Movimientos mensuales, Sincronización M+1, Vales PECOSA y Jeringas).» | `falso_positivo` | Sin acción: PECOSA es función del sistema, no del instrumento. |
| 92 | FP | Tabla 9, fila 8, columna 1 | 7 — PECOSA | «Vales de Despacho (PECOSA)» | `falso_positivo` | Sin acción: PECOSA es función del sistema, no del instrumento. |
| 93 | FP | Tabla 17, fila 9, columna 5 | 7 — PECOSA | «Número de PECOSA central de CENARES o Guía de Remisión.» | `falso_positivo` | Sin acción: PECOSA es campo del modelo de datos, no del instrumento. |
| 94 | FP | Tabla 25, fila 11, columna 4 | 7 — PECOSA | «Motores de renderizado nativo para vales PECOSA y reportes contables.» | `falso_positivo` | Sin acción: PECOSA es función del sistema, no del instrumento. |
| 95 | FP | Tabla 26, fila 5, columna 3 | 7 — PECOSA | «Prevención de duplicidad de comprobantes PECOSA» | `falso_positivo` | Sin acción: PECOSA es función del sistema, no del instrumento. |
| 96 | FP | Tabla 27, fila 1, columna 3 | 7b — Escenario Operativo Evaluado | «Escenario Operativo Evaluado» | `falso_positivo` | Sin acción: escenario de prueba XP, no escenario instrumental. |
| 97 | FP | Tabla 27, fila 13, columna 4 | 7 — PECOSA | «Formato PECOSA institucional con membrete y casilleros de firma.» | `falso_positivo` | Sin acción: formato institucional simulado en la prueba de aceptación. |
| 98 | FP | Tabla 51, fila 5, columna 3 | 7 — PECOSA | «Generar comprobantes de salida de vacunas (Vales PECOSA)» | `falso_positivo` | Sin acción: historia de usuario del sistema, no instrumento. |

**Reconciliación de conteos.** Las 98 filas agrupan 192 coincidencias: 65 `CM` (21 filas), 65 `IE` (36 filas), 50 `RM` (29 filas) y 12 `FP` (12 filas). La diferencia entre «coincidencias» y «filas» se debe a que varias filas contienen más de un término del mismo grupo (por ejemplo, P616 concentra la mayor densidad de términos de los grupos 1, 2, 3, 4, 7 y 9).

---

## 4. Verificaciones obligatorias

### A. Sección 5.1 y Tabla 35: coeficiente, datos, redacción y declaración de datos de prueba

**Transcripción literal.**

> **P649:** «5.1. Análisis de Confiabilidad del Instrumento 03»

> **P650:** «La evaluación psicométrica de la consistencia interna constituye un requisito metodológico insoslayable para certificar la fiabilidad y estabilidad métrica de los instrumentos de recolección de datos antes de proceder a las contrastaciones inferenciales de hipótesis. En concordancia con el diseño metodológico adoptado, el análisis de confiabilidad se circunscribió al Instrumento N.° 03 (Cuestionario de Satisfacción del Usuario bajo el Modelo de Aceptación Tecnológica - TAM), dado que los Instrumentos N.° 01 (Ficha de Registro Cronométrico de Tiempos Operativos) y N.° 02 (Ficha de Auditoría y Cotejo Documental de Lotes y Kardex) corresponden a mediciones directas de campo y auditorías físicas objetivas, cuya validez se sustenta en el protocolo de calibración inter-observador PMMV.»

> **P651:** «Para determinar la homogeneidad interna de la Modalidad A del Cuestionario TAM (conformada por ocho reactivos atómicos en escala Likert de 1 a 5 puntos, distribuidos equitativamente entre las dimensiones de Aceptación del Proceso [AP] y Utilidad Percibida [UP]), se calculó el coeficiente Alfa de Cronbach (Cronbach, 1951), complementado con la estimación de los intervalos de confianza asintóticos al 95% mediante el método de distribución F desarrollado por Feldt (1965). En la evaluación del pretest (proceso operativo manual tradicional), la escala global TAM arrojó un coeficiente Alfa de Cronbach de .939 (IC 95%: [0.874, 0.977]), mientras que las subescalas de Aceptación del Proceso y Utilidad Percibida alcanzaron coeficientes de .877 (IC 95%: [0.721, 0.956]) y .874 (IC 95%: [0.715, 0.955]), respectivamente. Por su parte, en la medición del postest (tras la implantación del sistema web SIVAC), la consistencia interna global se situó en .915 (IC 95%: [0.826, 0.968]), registrando la subescala AP un valor de .831 (IC 95%: [0.618, 0.939]) y la subescala UP un valor de .841 (IC 95%: [0.640, 0.943]).»

> **P652:** «Los coeficientes observados superan el umbral psicométrico de .800 exigido por la literatura científica (George y Mallery, 2003; Hernández-Sampieri y Mendoza, 2018), categorizándose como de nivel 'Bueno' en las dimensiones específicas y de nivel 'Excelente' en el constructo general. Asimismo, la amplitud contenida de los intervalos de confianza de Feldt ratifica la precisión de la estimación sobre la población censal de 14 trabajadores de la Dirección de Salud Apurímac II, evidenciando que los reactivos capturan de manera coherente, robusta y reproducible la percepción del personal sanitario respecto a la operatividad del sistema de información. En la Tabla 35 se consolidan los coeficientes psicométricos obtenidos.»

> **P653 (rótulo):** «Tabla 35 Confiabilidad de consistencia interna del Cuestionario TAM (Instrumento N.° 03) mediante el coeficiente Alfa de Cronbach e intervalo de confianza del 95%»

> **P654 (nota):** «Nota. Resultados provisionales calculados con datos de prueba (n = 14); no constituyen mediciones de campo. Intervalo de confianza (IC) al 95% calculado según el método de distribución F asintótica de Feldt (1965). Criterios de baremación psicométrica: ≥ .90 Excelente, .80 a .89 Buena, .70 a .79 Aceptable. El intervalo de confianza se expresa como [límite inferior, límite superior]. Fuente: datos de prueba.»

**Tabla 35 (T36), transcripción de filas:**

| Momento | Escala / subescala | Ítems | n | Alfa | IC 95% | Nivel |
|---|---|---:|---:|---:|---|---|
| Pretest (Proceso manual) | Escala Global TAM (Modalidad A) | 8 | 14 | 0.939 | [0.874, 0.977] | Excelente |
| Pretest (Proceso manual) | Aceptación del Proceso (AP) | 4 | 14 | 0.877 | [0.721, 0.956] | Buena |
| Pretest (Proceso manual) | Utilidad Percibida (UP) | 4 | 14 | 0.874 | [0.715, 0.955] | Buena |
| Postest (Sistema SIVAC) | Escala Global TAM (Modalidad A) | 8 | 14 | 0.915 | [0.826, 0.968] | Excelente |
| Postest (Sistema SIVAC) | Aceptación del Proceso (AP) | 4 | 14 | 0.831 | [0.618, 0.939] | Buena |
| Postest (Sistema SIVAC) | Utilidad Percibida (UP) | 4 | 14 | 0.841 | [0.640, 0.943] | Buena |

**Respuestas puntuales.**

1. **Coeficiente exacto:** alfa global .939 en pretest y .915 en postest; AP .877 y .831; UP .874 y .841; intervalos de confianza de Feldt al 95% según la tabla. No se inventa ni se recalcula ningún valor.
2. **¿Sobre qué datos?** La tabla declara la columna «Muestra (n)» con valor 14 y separa «Pretest (Proceso manual)» de «Postest (Sistema SIVAC)», con 8 ítems globales y 4 por subescala. Esa estructura presenta los coeficientes como mediciones de la población censal en dos momentos. La nota P654 dice que son «resultados provisionales calculados con datos de prueba» y que «no constituyen mediciones de campo».
3. **¿Con qué redacción?** El cuerpo usa «se calculó», «arrojó», «en la medición del postest», «coeficientes observados», «ratifica la precisión de la estimación sobre la población censal de 14 trabajadores» y «coeficientes psicométricos obtenidos». Esa redacción afirma resultados empíricos, no un ejercicio metodológico.
4. **¿El texto declara que son datos de prueba?** Solo en la nota P654, en la nota P838 del Anexo 4 («cálculo provisional sobre datos de prueba») y en el preámbulo P648, que declara provisional todo el capítulo V. El cuerpo P650–P652 no lo declara; P650 afirma «mediciones directas de campo» y P652 habla de «población censal» y «coeficientes obtenidos».
5. **Dictamen:** `contradiccion_metodologica`. La nota no cura la afirmación del cuerpo: el lector recibe dos relatos incompatibles sobre el mismo coeficiente.

**Acción correctiva.**
- Si 5.1 se conserva en el cuerpo: reescribir P650–P652 para decir expresamente «ejercicio psicométrico de calibración sobre datos de prueba», eliminar «población censal», «mediciones directas de campo» y «coeficientes obtenidos», y rotular la tabla como «datos de prueba».
- Si 5.1 se difiere: trasladar la sección y la Tabla 35 al Anexo 7 (salida histórica no validada) y dejar en el cuerpo solo el plan de análisis psicométrico.
- No alterar las cifras ni los intervalos sin decisión expresa del tesista.

### B. Tres formatos de evaluación del Anexo 3: campos prellenados

**Transcripción literal de los campos.**

| Campo | Juez 1 (T47) | Juez 2 (T48) | Juez 3 (T49) |
|---|---|---|---|
| Juez Validador | «____________________ (Juez 1)» | «____________________ (Juez 2)» | «____________________ (Juez 3)» |
| Grado y Especialidad | «Mg. en Ingeniería de Sistemas - Ingeniero de Sistemas / Especialista en Software y Bases de Datos» | «Mg. en Salud Pública - Licenciado en Enfermería / Especialista en Inmunizaciones y Cadena de Frío» | «Dr. en Ciencias de la Educación / Estadística - Metodólogo / Especialista en Estadística y Medición Cuantitativa» |
| Institución de Referencia | «Dirección de Salud Apurímac II / Universidad Nacional José María Arguedas» | «Dirección de Salud Apurímac II / Universidad Nacional José María Arguedas» | «Dirección de Salud Apurímac II / Universidad Nacional José María Arguedas» |
| Instrumentos Auditados | «Formato de evaluación disponible: matriz de la variable dependiente (12 componentes, escala de 1 a 4) y Cuestionario TAM (Modalidad A, ocho ítems Likert).» | Ídem | Ídem |
| Coeficiente V de Aiken | «V de Aiken: ______; IVC: ______» | Ídem | Ídem |
| Opinión Pericial Global | «[ ] Aplicable sin modificaciones [ ] Aplicable con observaciones [ ] No aplicable» | Ídem | Ídem |
| Fecha y Lugar | «Andahuaylas, Apurímac, Perú, ____ de ____________ de 2026» | Ídem | Ídem |
| Firma y DNI | «_________________________________________________________Firma y Sello del Juez Validador: Juez 1DNI: ____________________» | «_________________________________________________________Firma y Sello del Juez Validador: Juez 2DNI: ____________________» | «_________________________________________________________Firma y Sello del Juez Validador: Juez 3DNI: ____________________» |

**Respuestas puntuales.**

1. **¿Grado y especialidad prellenados?** Sí, en los tres formatos. No son campos en blanco: cada juez trae un perfil pregrabado (software, inmunizaciones, metodología/estadística).
2. **¿Nombres prellenados?** No. El campo dice «____ (Juez 1/2/3)»; el nombre está en blanco.
3. **¿DNI prellenado?** No. «DNI: ____________________» está en blanco en los tres.
4. **¿Institución prellenada?** Sí, en los tres: «Dirección de Salud Apurímac II / Universidad Nacional José María Arguedas».
5. **¿Fecha y lugar prellenados?** El lugar y el año están prellenados («Andahuaylas, Apurímac, Perú, ____ de ____________ de 2026»); el día y el mes están en blanco. No hay fecha firmada.
6. **¿Firmas?** No. Los tres formatos están sin firma y sin sello.
7. **Contradicción con P821:** P821 afirma que se presentan «los tres (3) formatos de evaluación en blanco». Tal como están, no están en blanco en grado, especialidad, institución, lugar y año. Si el texto que se adopte para el pasaje H o para la introducción del Anexo 3 conserva la expresión «en blanco» o «sin prellenar nombres, grados, documentos, marcas ni fechas», será falso mientras no se limpien esos campos.
8. **Dictamen:** `incoherencia_expositiva`, con un componente de `contradiccion_metodologica` si los perfiles prellenados se interpretan como una preasignación de jueces. La propuesta H cubre la celda «Instrumentos Auditados», pero no el prellenado de grado, especialidad, institución, lugar y año.

**Acción correctiva.** Decidir una de dos vías: (i) dejar los tres formatos realmente en blanco en grado, especialidad, institución, lugar y año, o (ii) rotular los perfiles como «propuesta de perfil del juez, no vinculante» y eliminar toda afirmación de que los formatos están «en blanco». En ambos casos, sustituir «12 componentes» y «Modalidad A» de la celda «Instrumentos Auditados» conforme al pasaje H.

### C. Sección 4.14 y códigos OP-01 a OP-14

**Transcripción literal.**

> **P578 (4.8):** «En la arquitectura metodológica del estudio se diferenció estrictamente la unidad de observación primaria de la unidad de análisis estadístico pareado. Las unidades de observación primarias correspondieron a los eventos transaccionales específicos recolectados en campo: las operaciones cronometradas de registro y despacho, los asientos y expedientes de kardex auditados, las órdenes de distribución conciliadas y las respuestas a los cuestionarios psicométricos administrados. Por su parte, la unidad de análisis estadístico quedó constituida por cada uno de los catorce operadores (OP-01 a OP-14, N = n = 14) que gestionaron la cadena de inmunizaciones en ambos periodos de observación.»

> **P644 (4.14):** «En segundo lugar, se garantizó el principio de autonomía y voluntariedad mediante la suscripción del consentimiento informado por parte de los catorce operadores participantes, asegurando la confidencialidad estricta y el anonimato de sus datos personales mediante la asignación de identificadores alfanuméricos correlativos (OP-01 a OP-14). Asimismo, se resguardó la confidencialidad de la información estratégica institucional, restringiendo el acceso a los registros y velando porque el estudio no involucrara datos clínicos nominales de pacientes ni menores de edad, limitándose estrictamente al control transaccional y volumétrico de lotes.»

**Respuestas puntuales.**

1. **¿Se presentan OP-01 a OP-14 como códigos de operador?** Sí. P578 los usa como identificadores de la unidad de análisis («cada uno de los catorce operadores (OP-01 a OP-14, N = n = 14)»); P644 los usa como identificadores de anonimización («identificadores alfanuméricos correlativos (OP-01 a OP-14)»).
2. **¿Contradicen el «Trabajador N.°» del paquete nuevo?** El informe no usa «Trabajador N.°» en ninguna ocurrencia (0). Usa «operadores» y el código OP. Según el encargo, el paquete v04 rotula «Trabajador N.°»; por tanto, la nomenclatura del informe es incoherente con el instrumento impreso, aunque no sea una contradicción interna del informe. Clase: `incoherencia_expositiva`.
3. **Cobertura de los catorce códigos:** solo aparecen literalmente `OP-01` y `OP-14`; `OP-02` a `OP-13` no se imprimen individualmente. La sustitución del rango «OP-01 a OP-14» elimina, por tanto, todos los residuos de código en el cuerpo.

**Acción correctiva.** Sustituir «operadores (OP-01 a OP-14)» por «trabajadores (Trabajador N.° 01 a 14)» en 4.8 y 4.14, y revisar los encabezados de tabla y anexos que repliquen el código. Si se decide conservar «operador», declararlo una vez como sinónimo de «trabajador» y no mezclar ambas denominaciones.

### D. Afirmaciones de aplicación de instrumentos y de existencia de datos de campo

**Transcripción literal de las afirmaciones.**

| # | Ubicación | Transcripción | Qué afirma |
|---:|---|---|---|
| 1 | P616 (4.10.2) | «En correspondencia directa con las técnicas descritas, se diseñaron y aplicaron tres instrumentos de recolección de datos…» | Aplicación ejecutada |
| 2 | P612 (4.10.1) | «a)Observación directa cronometrada: Se aplicó para medir in situ y de manera no intrusiva la duración exacta de las operaciones de registro de movimientos y de emisión de vales de salida ejecutadas por los catorce operadores…» | Aplicación ejecutada |
| 3 | P613 (4.10.1) | «b)Análisis documental (auditoría de registros): Se utilizó para examinar de forma sistemática y retrospectiva los asientos del kardex físico… en el pretest…» | Aplicación ejecutada |
| 4 | P614 (4.10.1) | «c)Encuesta psicométrica: Se administró al personal censal de inmunizaciones…» | Aplicación ejecutada |
| 5 | P578 (4.8) | «…eventos transaccionales específicos recolectados en campo… las respuestas a los cuestionarios psicométricos administrados.» | Datos de campo existentes |
| 6 | P579 (4.8) | «…se utilizó el puntaje sumativo directo obtenido por el operador i en cada subescala de 4 ítems…» | Puntajes obtenidos |
| 7 | P633 (4.13) | «El procesamiento estadístico de los datos recolectados en el pretest y postest se estructuró mediante rutinas computacionales reproducibles…» | Datos de campo procesados |
| 8 | P650 (5.1) | «…los Instrumentos N.° 01… y N.° 02… corresponden a mediciones directas de campo y auditorías físicas objetivas…» | Medición de campo |
| 9 | P652 (5.1) | «…ratifica la precisión de la estimación sobre la población censal de 14 trabajadores… En la Tabla 35 se consolidan los coeficientes psicométricos obtenidos.» | Resultados de campo |
| 10 | P660 (5.2.1, nota) | «Fuente: Ficha de Registro Cronométrico SIVAC (2026).» | Fuente instrumental aplicada |
| 11 | P667 (5.2.2, nota) | «Fuente: Ficha de Cotejo Documental de Lotes y Kardex (2026).» | Fuente instrumental aplicada |
| 12 | P672 (5.2.3) | «…la evaluación mediante el modelo TAM evidenció un cambio sustancial… 17.07 puntos… a 36.21 puntos.» | Resultados obtenidos |
| 13 | P674 (5.2.3, nota) | «Muestra censal n = 14. Fuente: Cuestionario de Satisfacción del Usuario SIVAC (2026).» | Datos de campo |
| 14 | P728 (5.4.3, nota) | «Evaluado con la Modalidad A del Instrumento 03.» | Aplicación ejecutada |
| 15 | P834 (Anexo 4, nota) | «Ficha de cronometraje aplicada a los 14 operadores en los trece (13) centros de acopio…» | Aplicación ejecutada |
| 16 | P849 (Anexo 7) | «REGISTRO FOTOGRÁFICO DE EVIDENCIA DE APLICACIÓN EN CAMPO (PENDIENTE DE INCORPORACIÓN)» | Evidencia de aplicación |
| 17 | P140 (Resumen) | «…cuyos estadísticos definitivos de campo se encuentran en fase de consolidación postest.» | Datos de campo en consolidación |

**Contraevidencia literal.**

> **P648 (preámbulo del capítulo V):** «…se hace constar que los resultados, las matrices descriptivas, las pruebas de normalidad, los contrastes de hipótesis y las figuras presentados en este capítulo corresponden a un conjunto de datos provisionales de prueba. Dichos valores deben sustituirse por los registros definitivos que se recolecten en el trabajo de campo en la Dirección de Salud Apurímac II antes de la sustentación de la tesis.»

> **P654 (nota de la Tabla 35):** «Resultados provisionales calculados con datos de prueba (n = 14); no constituyen mediciones de campo… Fuente: datos de prueba.»

> **P838 (nota de la Tabla 48):** «El coeficiente Alfa de Cronbach reportado en la Tabla 35 corresponde a un cálculo provisional sobre datos de prueba.»

> **P840 (introducción del Anexo 5):** «Los valores numéricos consignados son datos de prueba y no constituyen mediciones de campo.»

> **P842 (nota del Anexo 5):** «Datos de prueba del pretest sobre 14 operadores y los centros de acopio registrados en SIVAC; no constituyen mediciones de campo.»

**Respuestas puntuales.**

1. **¿El informe afirma que los instrumentos se aplicaron?** Sí, de forma expresa en P616 («se diseñaron y aplicaron»), P612 («Se aplicó»), P613 («Se utilizó»), P614 («Se administró»), P834 («aplicada a los 14 operadores») y P849 («evidencia de aplicación en campo»). De forma implícita en P728 («Evaluado con…»), P660 y P667 («Fuente: Ficha…»), P674 («Fuente: Cuestionario…»).
2. **¿Afirma que existen datos de campo?** Sí: P578 («recolectados en campo»), P633 («datos recolectados»), P650 («mediciones directas de campo»), P652 («población censal» y «coeficientes obtenidos»), P672 (resultados), P140 («estadísticos definitivos de campo… en consolidación»).
3. **¿Hay declaración de datos de prueba?** Sí, pero confinada a notas y anexos: P648, P654, P838, P840 y P842. Ninguna de esas declaraciones aparece en el cuerpo de 4.10.1, 4.10.2, 4.13, 5.1 (párrafos 650–652), 5.2.1, 5.2.2, 5.2.3 ni 5.4.3.
4. **Dictamen:** `contradiccion_metodologica`. Las notas no neutralizan las afirmaciones del cuerpo: el documento sostiene simultáneamente que los instrumentos se aplicaron y que los datos son de prueba. Bajo la regla de cero alucinaciones, la afirmación del cuerpo es la que debe corregirse, no la nota.
5. **Acción correctiva:** reescribir en futuro o condicional («se aplicará», «se administrará», «se procesarán») las afirmaciones de P612–P616, P633, P650 y P834; eliminar «recolectados en campo» de P578 y P579; sustituir «población censal» y «coeficientes obtenidos» de P652; retitular P849; y añadir en cada tabla de resultados una llamada visible a la nota de datos de prueba. Si el tesista ya cuenta con datos de campo, la corrección es inversa: aportar la fuente primaria y retirar las notas de «datos de prueba». Mientras no exista esa fuente, prevalece la declaración de P648.

---

## 5. Pasajes que el maquetador debe corregir además de los nueve ya cubiertos

**Alcance.** Esta lista excluye los nueve pasajes A–I de `PROPUESTA_AJUSTE_INFORME_v04.md`. Se divide en tres bloques: (1) pasajes que la propuesta no menciona; (2) pasajes mencionados solo en el anexo de control, sin texto de reemplazo redactado; (3) acciones mecánicas o globales. La prioridad `P1` es bloqueante para la coherencia metodológica; `P2` es obligatoria para la coherencia expositiva; `P3` es de armonización.

### 5.1. Pasajes no mencionados por la propuesta (corrección obligatoria)

1. **P1 — P178 (1.3.3, Justificación metodológica).** Reescribir el literal (c): eliminar el «coeficiente Kappa de Cohen» y la «calibración interobservador» para las fichas de tiempos; declarar protocolo único y repetibilidad; sustituir «disparadores unívocos» por «criterios de inicio y corte» o retirarlo; renombrar «guía de cotejo documental»; conservar el alfa solo como estimación futura.
2. **P1 — P578 (4.8, Unidad de análisis).** Eliminar «recolectados en campo» y «cuestionarios psicométricos administrados»; sustituir «operadores (OP-01 a OP-14)» por «trabajadores (Trabajador N.° 01 a 14)».
3. **P2 — P579 (4.8).** Sustituir «puntaje sumativo directo obtenido» por «puntaje sumativo directo que se obtendrá»; mantener o retirar los códigos AP/UP según lo que imprima el cuestionario v04.
4. **P1 — P612, P613 y P614 (4.10.1, Técnicas de recolección).** Reescribir en futuro o condicional; no afirmar aplicación ejecutada.
5. **P1 — P633 (4.13, Técnicas estadísticas).** Sustituir «datos recolectados en el pretest y postest» por «datos de prueba» o por «datos que se recolectarán».
6. **P2 — P660 (5.2.1, nota).** Sustituir «Fuente: Ficha de Registro Cronométrico SIVAC (2026)» por «Fuente: Ficha de observación de tiempos (2026)» o por la denominación v04.
7. **P2 — P667 (5.2.2, nota).** Sustituir «Fuente: Ficha de Cotejo Documental de Lotes y Kardex (2026)» por «Fuente: Ficha de observación documental (2026)» o por la denominación v04.
8. **P2 — P672 (5.2.3).** Sustituir «Puntaje Global TAM (Modalidad A…)» por «Puntaje Global TAM (cuestionario de satisfacción…)»; si los valores son de prueba, añadir la llamada a la nota.
9. **P2 — P674 (5.2.3, nota).** Sustituir «Cuestionario TAM, Modalidad A» por «cuestionario de satisfacción»; mantener «Muestra censal n = 14» solo si se conserva la nota de datos de prueba.
10. **P2 — P728 (5.4.3, nota).** Sustituir «Modalidad A del Instrumento 03» por «Instrumento N.° 03».
11. **P2 — T30 (Tabla 29, protocolo de recolección).** Sustituir «Modalidad A» por «cuestionario de satisfacción» y «vales PECOSA físicos» por «comprobantes de salida o vales»; eliminar «modalidades A y B».
12. **P2 — T45 (Tabla 44, Anexo 1).** Sustituir «Ficha de observación de tiempos», «Guía de cotejo documental» y «Cuestionario… Modalidad A» por las denominaciones v04; eliminar «Modalidad A» de la fila de la Dimensión 3.
13. **P2 — P830, P831 y P832 (Anexo 4, lista de instrumentos).** Sustituir los tres títulos por las denominaciones v04; eliminar «Modalidad A: AP y UP» de P832.
14. **P1 — P834 (Anexo 4, nota de la Tabla 46).** Sustituir «Ficha de cronometraje aplicada a los 14 operadores» por «Ficha de cronometraje para los 14 operadores» o por la nota del pasaje I.
15. **P3 — P849 (Anexo 7).** Retitular como «Registro fotográfico pendiente de incorporación», sin afirmar «evidencia de aplicación en campo».
16. **P1 — P140 (Resumen) y P3 — P152 (Introducción).** Homologar «fichas de observación cronométrica», «guías de cotejo documental» y «ficha de observación de tiempos» a las denominaciones v04; en P140, sustituir «cuyos estadísticos definitivos de campo se encuentran en fase de consolidación postest» por una fórmula que no presuponga datos de campo.
17. **P3 — T50, T51 y T52 (cuerpos de las Tablas 46, 47 y 48).** Sustituir «vale PECOSA» por «comprobante de salida o vale»; alinear los códigos AP/UP con lo que imprima el cuestionario v04; eliminar «Modalidad A» de los encabezados y notas internas.

### 5.2. Pasajes mencionados solo en el anexo de control, sin texto redactado

Estos pasajes no están cubiertos por A–I, pero la propuesta los reconoce como pendientes. Requieren decisión y redacción antes de compilar.

1. **P1 — 5.1 completa y Tabla 35 (P650–P654, T36).** Decidir si se conserva como ejercicio psicométrico sobre datos de prueba o se traslada al Anexo 7. En cualquier caso: eliminar «mediciones directas de campo» (P650), «población censal» y «coeficientes obtenidos» (P652), y rotular la tabla como «datos de prueba». Ver apartado A.
2. **P1 — Anexo 3, prellenado de los tres formatos (T47–T49).** La propuesta H cubre la celda «Instrumentos Auditados», pero no el grado, la especialidad, la institución, el lugar y el año. Limpiar esos campos o rotularlos como «perfil propuesto». Ver apartado B.
3. **P1 — 4.8 y 4.14, códigos OP (P578, P644).** Sustituir por «Trabajador N.° 01 a 14» o declarar «operador» como sinónimo. Ver apartado C.
4. **P2 — Anexo 4, cuerpos de las Tablas 46, 47 y 48 (T50, T51, T52).** Alinear ítems, códigos, escalas y denominaciones con el paquete v04; no basta con cambiar títulos y notas.
5. **P2 — 4.9, ecuaciones 5–6 y Tabla 32 (T33).** Revisar la codificación AP/UP y el rango 4–20 si el cuestionario v04 no imprime códigos; mantener la coherencia con P579 y T52.
6. **P2 — Tabla 45 (T46).** Alinear los códigos AP/UP y la referencia a la Modalidad A con el cuestionario v04.

### 5.3. Acciones mecánicas o globales

1. **Renumeración.** Si el Anexo 4 gana o pierde tablas, renumerar las Tablas 46–48 y actualizar todas las referencias cruzadas; verificar que las Tablas 33–35 conserven su numeración.
2. **Índices.** Actualizar la lista de tablas (P121, P132–P134) y el campo TOC después de las ediciones; verificar que los rótulos «Tabla 33», «Tabla 34», «Tabla 35», «Tabla 46», «Tabla 47» y «Tabla 48» apunten a la tabla correcta.
3. **Barrido global de «Modalidad A» y «Modalidad B».** Reemplazar las 29 + 4 + 1 ocurrencias por «cuestionario de satisfacción» o «cuestionario de ocho reactivos»; verificar que no quede «módulo anexo».
4. **Barrido global de «PECOSA».** Conservar las 10 ocurrencias del capítulo XP y del Anexo 6 (T4, T5, T8, T9, T10, T18, T26, T27, T28, T55) porque designan una función o formato del sistema; sustituir las ocurrencias metodológicas o instrumentales (P594, P616, T30, T32, T50) por «comprobante de salida o vale».
5. **Barrido global de códigos.** Verificar que no queden `REG-01`, `REG-02`, `VALE-01`, `PU-01`, `PU-04`, `PE-01`, `PE-04`, `OP-01` ni `OP-14` en el cuerpo, las tablas o los anexos, salvo que el tesista decida conservarlos como codificación interna.
6. **Verificación del cuestionario impreso (Tabla 48).** Si el paquete v04 no imprime los códigos AP/UP, sustituir la columna «Ítem» por numeración 1–8; si imprime «Trabajador N.°», alinear el encabezado y las instrucciones.
7. **Congelamiento de cifras.** No modificar coeficientes, ecuaciones, intervalos ni resultados estadísticos hasta que el tesista decida el destino de 5.1 y del Anexo 7.
8. **Recompilación.** Generar el DOCX con el motor canónico, verificar que no haya referencias cruzadas rotas y que la nota de datos de prueba sea visible en cada tabla de resultados.

---

## 6. Conclusión de la auditoría

El informe candidato v22 no está limpio del esquema instrumental suprimido. La supresión se aplicó de forma desigual: los títulos de algunos instrumentos y varias notas ya migraron al paquete simplificado, pero el cuerpo conserva códigos, modalidades, coeficientes de concordancia y afirmaciones de aplicación que el nuevo paquete no respalda. La propuesta A–I cubre nueve pasajes y deja fuera, al menos, diecisiete ubicaciones adicionales, entre ellas la sección 5.1 completa, el prellenado de los tres formatos del Anexo 3 y los cuerpos de las Tablas 46–48.

**Dictamen:** `OBSERVADO_SUBSANABLE`, con dos alertas rojas parciales: (i) la presentación de alfa sobre datos de prueba como resultados de campo en 5.1/Tabla 35, y (ii) la afirmación de aplicación de instrumentos en P616, P612–P614 y P834. Ninguna de las dos se resuelve con una nota al pie; ambas exigen reescritura del cuerpo o decisión expresa del tesista.

**Criterio de cierre:** cero ocurrencias de los códigos suprimidos en el cuerpo y en las tablas; denominaciones v04 homogéneas; 5.1 rotulada como datos de prueba o trasladada al Anexo 7; Anexo 3 sin campos prellenados o con rotulación de perfil propuesto; y ausencia de afirmaciones de aplicación mientras no exista fuente primaria de campo.
