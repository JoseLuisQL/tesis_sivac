---
tipo: reporte
fase: F3
agente: analista-documental
estado: revisado
fecha_actualizacion: 2026-10-07
documento_auditado: salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V3_NORMALIZADO.docx
---

# AUDITORÍA DE ESTRUCTURA, CONCISIÓN Y CITAS — CAPÍTULOS I Y II

**Documento:** `salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V3_NORMALIZADO.docx` (511 párrafos; solo lectura, sin modificaciones).
**Contraste:** `MATRIZ_CONSISTENCIA_DEFINITIVA.md`, `CATALOGO_MAESTRO_FUENTES_ZOTERO_SIVAC.md` (26 fuentes), tesis modelo Jhon (2026) y Fany (2024), Crossref y doi.org.
**Método:** extracción párrafo a párrafo con python-docx (índices P000 base cero), detección de imágenes `w:drawing`, consulta de DOI en Crossref.

## 0. Hallazgos críticos (reverificados contra el DOCX)

| N.° | Hallazgo | Evidencia | Estado tras reverificación |
|---|---|---|---|
| 1 | Acápite 2.2.6 Inteligencia artificial cita a Alhazmi et al. (2024), fuente no catalogada en Zotero | P139 a P142; cita en P141 | **Confirmado con matiz.** La fuente existe (IEEE Access, 12, 88189-88201; doi 10.1109/ACCESS.2024.3407711, verificada en Crossref) y figura en la lista de referencias (P470). No es una alucinación: es una fuente fuera del catálogo. Además, el backend de SIVAC sí contiene un módulo de IA (asistente SiBot sobre la librería `ai`, en `backend/src/services/sibot`). La pertinencia de 2.2.6 depende de si SiBot forma parte de la intervención evaluada. |
| 2 | Nota de Figura 3 cita un blog comercial | P241: "Por SINNAPS, 2022, Sinnaps (URL de imagen jpg)" | **Confirmado.** No está en la lista de referencias ni en el catálogo. La ruta de la URL (uploads 2020-05) contradice el año 2022. |
| 3 | OPS y PATH citado como "s. f." | P169 (texto) y P505 (referencia) | **Confirmado en ambos lugares.** El catálogo registra `@opspath2020`. |
| 4 | Hiperfragmentación de 2.2 | 25 subacápites Heading 3 numerados (2.2.1 a 2.2.25) | **Confirmado.** 7 subacápites tienen un solo párrafo de 30 a 51 palabras. |
| 5 | Hiperfragmentación de 2.3 | 20 subacápites Heading 3 numerados (2.3.1 a 2.3.20) | **Confirmado.** Cada término tiene un único párrafo de 16 a 32 palabras. |
| 6 | Heading 3 vacío | P138 | **Confirmado.** Genera una entrada en blanco en el índice automático. |
| 7 | Párrafos vacíos | El borrador previo indicaba 25 | **Corregido: son 61.** 8 en el Cap. I y 53 en el Cap. II, sin contar P129, P184 y P240, que contienen las figuras. |
| 8 | **NUEVO.** Cita huérfana de Davis (1989) | P221 (nota de Tabla 3) | No figura en la lista de referencias ni en el catálogo. Rompe la correspondencia 1:1. Existe: MIS Quarterly, 13(3), 319-340, doi 10.2307/249008 (Crossref). |
| 9 | **NUEVO.** 8 referencias sin cita en el cuerpo | P471, P479, P481, P487, P488, P493, P495, P498 | Arisholm (2007), Cortés Rojas (2024), De la Torre Llorente (2010), Jain y Arora (2025), Kamran et al. (2023), Naik y Raj (2023), Pérez Peña y Ramos (2021), Romero Onofre (2016). Ninguna está catalogada. |
| 10 | **NUEVO.** DOI erróneos en el catálogo Zotero, no en el DOCX | Duong (2021) y Ndlovu (2021) | El catálogo asigna a Duong el doi 10.2196/29367, que corresponde a un artículo sobre Apple Health Records, y a Ndlovu el 10.2196/26168, que corresponde a un protocolo de app de salud mental. El DOCX usa los correctos (e28096 y e32722). Para Ndlovu, Crossref registra 2022, 6(3); el DOCX dice 2021. |
| 11 | **NUEVO.** Afirmación empírica en pasado | P094 a P095 | Afirman que el pretest se ejecutó en el último trimestre de 2024, que el postest concluyó en 2025 y que "se analizó al censo completo". Los datos de campo siguen bloqueados: requiere confirmación del tesista. |

**Correcciones al borrador previo:** el inventario de antecedentes y la matriz de citas del borrador anterior contenían títulos, cifras y ubicaciones de cita que no figuran en el DOCX. Por ejemplo, se atribuían al Cap. I citas de OMS, Brooks y MINSA, y se daban cifras inexistentes para Balón y Astuhuaman. Esta versión las sustituye íntegramente por datos extraídos del documento.

## 1. Estructura de encabezados y conteo de palabras

**Totales.** El Cap. I (P058 a P096) suma 1 533 palabras con encabezados: 1 500 de cuerpo en 21 párrafos, 10 encabezados y 8 vacíos. El Cap. II (P097 a P319) suma 4 087 palabras con encabezados y rótulos: 3 824 de cuerpo, 52 encabezados (uno vacío), 53 vacíos, 4 tablas (después de P116, P149, P220 y P261) y 3 figuras (P129, P184 y P240). El conteo de "cuerpo" excluye encabezados y rótulos e incluye las notas.

### 1.1 Capítulo I

| Nivel | Encabezado | Párrafos | Párr. texto | Palabras |
|---|---|---|---|---|
| N1 | CAPÍTULO I. PLANTEAMIENTO DEL PROBLEMA (doble espacio) | P058 | 0 | 0 |
| N2 | 1.1 Descripción del problema | P060-P065 | 4 | 490 (internacional 125, Latinoamérica 83, nacional 108, local 174) |
| N2 | 1.2 Formulación del problema (triple espacio) | P066 | 0 | 0 |
| N3 | 1.2.1 Problema General | P067-P069 | 1 | 29 |
| N3 | 1.2.2 Problemas Específicos (según corresponda) | P070-P075 | 3 | 101 |
| N2 | 1.3 Objetivos | P076 | 0 | 0 |
| N3 | 1.3.1 Objetivo General | P077-P079 | 1 | 30 |
| N3 | 1.3.2 Objetivos Específicos | P080-P084 | 3 | 104 |
| N2 | 1.4 Justificación | P085-P090 | 4 | 297 |
| N2 | 1.5 Delimitación | P091-P096 | 5 | 449 |

PG, PE1 a PE3, OG y OE1 a OE3 coinciden literalmente con la matriz definitiva: la alineación 1:1 con DEC-007 está **conforme**.

### 1.2 Capítulo II

| Nivel | Encabezado | Párrafos | Párr. texto | Palabras | Observación |
|---|---|---|---|---|---|
| N1 | CAPÍTULO II. MARCO TEÓRICO | P097 | 0 | 0 | doble espacio |
| N2 | 2.1 Antecedentes de investigación | P098 | 0 | 0 | |
| N3 | 2.1.1. Antecedentes a nivel internacional | P099-P104 | 4 | 384 | punto final inconsistente con 2.2.1 |
| N3 | 2.1.2. Antecedentes a nivel nacional | P105-P109 | 3 | 361 | |
| N2 | 2.2 Bases teóricas | P110 | 0 | 0 | |
| N3 | 2.2.1 Sistema web | P111-P118 | 4 | 116 | Tabla 1 |
| N3 | 2.2.2 Arquitectura de software | P119-P122 | 2 | 84 | |
| N3 | 2.2.3 Arquitectura cliente-servidor | P123-P131 | 4 | 104 | Figura 1; P124-P126 sin cita |
| N3 | 2.2.4 Sistema de información en salud | P132-P134 | 1 | 39 | micro-sección, sin cita |
| N3 | 2.2.5 Sistema de información de inmunización | P135-P137 | 2 | 102 | |
| N3 | (vacío) | P138 | 0 | 0 | encabezado huérfano |
| N3 | 2.2.6 Inteligencia artificial | P139-P142 | 2 | 87 | Alhazmi (2024) no catalogado |
| N3 | 2.2.7 Calidad de software | P143-P145 | 1 | 47 | micro-sección, sin cita |
| N3 | 2.2.8 Norma ISO/IEC 25010 | P146-P151 | 2 | 74 | Tabla 2; título sin ":2023" |
| N3 | 2.2.9 Funcionalidad | P152-P156 | 3 | 108 | P155 redundante |
| N3 | 2.2.10 Usabilidad | P157-P164 | 6 | 198 | P163 redundante |
| N3 | 2.2.11 Programa Nacional de Inmunizaciones | P165-P167 | 1 | 36 | micro-sección |
| N3 | 2.2.12 Gestión logística de vacunas | P168-P170 | 1 | 51 | OPS y PATH "s. f." |
| N3 | 2.2.13 Gestión de movimientos de vacunas | P171-P174 | 2 | 61 | definición de la VD sin cita |
| N3 | 2.2.14 Cadena de frío | P175-P178 | 2 | 76 | |
| N3 | 2.2.15 Conservación de vacunas | P179-P186 | 3 | 87 | Figura 2 |
| N3 | 2.2.16 Lote de vacunas | P187-P189 | 1 | 31 | micro-sección |
| N3 | 2.2.17 Inventario de vacunas | P190-P193 | 2 | 68 | |
| N3 | 2.2.18 Kardex | P194-P196 | 1 | 30 | micro-sección, sin cita |
| N3 | 2.2.19 Movimiento de vacunas | P197-P199 | 1 | 36 | micro-sección, sin cita |
| N3 | 2.2.20 Oportunidad de procesamiento | P200-P207 | 6 | 333 | D1 |
| N3 | 2.2.21 Consistencia documental | P208-P214 | 5 | 195 | D2; espacios de ancho cero en P213 |
| N3 | 2.2.22 Satisfacción del usuario | P215-P222 | 4 | 196 | D3; Tabla 3; Davis solo en la nota |
| N3 | 2.2.23 Metodología Extreme Programming (XP) | P223-P228 | 4 | 130 | "Beck (1999) dice:" |
| N3 | 2.2.24 Fases de la metodología XP | P229-P242 | 10 | 165 | Figura 3 (SINNAPS) |
| N3 | 2.2.25 Prácticas de Extreme Programming | P243-P262 | 12 | 122 | pseudo-títulos Normal de 1 a 4 palabras; Tabla 4 duplica la lista |
| N2 | 2.3 Marco conceptual | P263 | 0 | 0 | |
| N3 | 2.3.1 a 2.3.20 (20 términos) | P264-P319 | 20 | 503 | 16 a 32 palabras por término; 16 vacíos intercalados |

Términos de 2.3, con palabras: Sistema SIVAC 31, Aplicación web 27, Sistema de información de inmunización 32, Base de datos 16, API 24, Gestión de movimientos de vacunas 25, Movimiento de vacunas 28, Entrada 29, Salida 28, Saldo 25, Lote 26, Kardex digital 22, Vale de entrega 27, Centro de acopio 16, Oportunidad de procesamiento 19, Consistencia documental 26, Concordancia documental 25, Satisfacción del usuario 27, Percepción de utilidad 25 e Historia de usuario 25.

## 2. Diagnóstico de estilo y concisión frente a Jhon (2026)

**Patrón verificado en el PDF de Jhon (2026), índice y pp. 10-43:**
- El Cap. II (Antecedentes) tiene solo 2.1 Internacionales y 2.2 Nacionales.
- El Cap. III (Marco teórico) organiza 3.1 Bases teóricas en **dos ejes sin numeración decimal**: "Sistema de información" (pp. 14-30, VI) y "Gestión de procesos" (pp. 31-38, VD). Los subniveles van sin numerar (negrita con punto final y literales A., B. y a), b)).
- 3.2 Marco conceptual contiene **18 términos sin numeración decimal** (pp. 39-43).
- Cada antecedente es un párrafo narrativo: autor (año), "denominada: título", lugar, objetivo, enfoque, metodología, muestra y conclusión.
- La justificación cubre las dimensiones teórica, práctica, social y metodológica.

| Criterio | Jhon (2026) | SIVAC V3 | Diagnóstico |
|---|---|---|---|
| Granularidad de bases teóricas | 2 ejes en el índice | 25 entradas N3 más 1 vacía | Hiperfragmentado; el índice crece en 26 líneas |
| Marco conceptual | 18 términos sin numerar | 20 términos con numeración decimal | Debe desnumerarse y ordenarse alfabéticamente (la guía UNAJMA indica 15-25 términos en orden alfabético) |
| Duplicación 2.2 frente a 2.3 | Sin duplicación | **10 de 20 términos duplicados** (no el 70 % que indicaba el borrador): Lote P188 y P294, Kardex P195 y P297, Movimiento P198 y P282, Gestión de movimientos P172 y P280, SII P136 y P271, Oportunidad P201 y P305, Consistencia P209 y P308, Satisfacción P216 y P313, Historia de usuario P247 y P319, Sistema web y Aplicación web P112 y P268 | Redundancia |
| Coherencia con DEC-007 en 2.3 | No aplica | P305 mide "registrar movimientos y generar reportes" (DEC-007 dice emisión de vale); P308 usa "exactitud del registro y concordancia documental" (DEC-007 dice RSD y CPE) | **Deriva de indicadores** |
| Justificación | Teórica, práctica, social y metodológica | Organizacional, metodológica, práctica y social | Falta la justificación teórica |
| Antecedentes | Párrafo canónico completo | Faltan títulos en Kigenza (P102) y Ergetie (P103); el de Astuhuaman (P106) va sin comillas; ninguno de los 7 cierra con su aporte a SIVAC ni con la conclusión del autor | Completar |

**Verbosidad y redundancia localizadas:**
1. **Párrafos de cierre que repiten el inicio de la sección** (unas 200 palabras podables): P114 (27), P126 (23), P155 (31), P163 (31), P206 (24), P213 (29) y P218 (34).
2. **Cifras de antecedentes repetidas:** el dato de Balón "3 o 4 días a 6 segundos" aparece tres veces (P062, P101, P204). Las cifras de Shen aparecen en P061 y P100; las de Mego en P063 y P107; las de Garcia Villacorta en P063 y P108. El Cap. I usa los antecedentes como diagnóstico de contexto en lugar de fuentes normativas o estadísticas (MINSA 2022 y OPS y PATH están catalogadas y no se citan en el Cap. I).
3. **P064 (diagnóstico local, 174 palabras):** los 14 trabajadores, los 11 centros de acopio y el uso de Excel aislado no tienen fuente institucional. [VERIFICAR con el tesista: oficio o informe de la DISA].
4. **Detalle operacional fuera de lugar:** P087 (110), P096 (147) y P205 (108) repiten la operacionalización (Treg, Tvale, RSD, CPE, AP, UP), que corresponde al Cap. III o IV.
5. **Fórmulas metadefensivas o infladas:** P087 ("en lugar de asumir reducciones temporales subjetivas o no parametrizadas"), P092 ("cuatro ejes canónicos del estándar institucional") y P206 ("evitando atribuciones causales..."), que además contradice el nivel explicativo.
6. **Tiempos verbales mezclados:** futuro en P086-P089, P126, P209 y P265 ("se desarrollará"); pasado en P094-P096 ("se desarrolló", "se analizó"). Debe unificarse según se trate de proyecto o de informe final.
7. **Registro de citas:** P225 dice "Beck (1999) dice:", con un bloque textual traducido en P226 seguido de "(pág. 70)". P232 cierra con "(pág. 40)" (APA 7 exige "p."). P230 es una cita secundaria ("Mego Navarro (2021) cita a Pressman (2010)") de una fuente que ya está catalogada y debe citarse de forma directa.
8. **Afirmaciones teóricas sin cita:** P124, P133, P144, P172, P176, P180, P195, P198, P201, P209 y P216.
9. **ISO/IEC 25010:2023:** P147 mezcla terminología de la edición 2011 (usabilidad, portabilidad) con la de 2023 (seguridad de uso). En la edición 2023, "capacidad de interacción" sustituye a usabilidad y "flexibilidad" a portabilidad. [VERIFICAR contra el texto normativo]. 2.2.9 y 2.2.10 usan los nombres de 2011.
10. **Plantilla y OpenXML:** "(según corresponda)" en P070; espacios múltiples en P058, P066 y P097; 2 espacios de ancho cero (U+200B) en P213; encabezado vacío en P138; 61 párrafos vacíos usados como espaciadores.
11. **TAM ausente del cuerpo:** el modelo TAM, sustento de la D3, no se explica en la prosa de 2.2.22. Davis (1989) solo aparece en la nota de la Tabla 3.

## 3. Inventario de antecedentes (texto literal del DOCX)

| N.° | Antecedente | Título en el texto | Objetivo | Metodología y muestra | Resultados reportados | Vínculo con DEC-007 | Observación |
|---|---|---|---|---|---|---|---|
| 1 | Shen et al. (2024), China; P100 | "Management of drug supply chain information based on artificial intelligence + vendor managed inventory in China" | Optimizar la cadena de suministro de medicamentos con un sistema digital basado en IA y VMI | Estudio de caso antes y después (pérdidas, discrepancias de inventario, farmacia en la nube) | Tasa de inventario hospitalario ~20 %; error anual de inventario de 0.425‰ a 0.025‰; eficiencia +42.4 % | D2 (RSD) | Medicamentos, no vacunas; sin oración de aporte |
| 2 | Balón Morejón (2023), Ecuador; P101 | "Aplicación web de gestión de citas, control de inventario y campañas de vacunación en el centro de salud Dr. José Garcés Rodríguez del cantón Salinas, en Ecuador" | Desarrollar una aplicación web con tecnologías libres | Exploratoria y diagnóstica, desarrollo incremental, entrevistas y análisis documental; muestra no declarada | Reportes estadísticos de 3 o 4 días a 6 segundos | D1 (indirecto: reportes, no Treg ni Tvale) | Cifra repetida 3 veces |
| 3 | Kigenza et al. (2023), Ruanda; P102 | **Ausente** | Fortalecer el uso del e-LMIS (mejora de calidad) | Intervención en 596 puntos de prestación, 30 almacenes y 1 296 trabajadores | Uso del e-LMIS de 55 % a 96 %; exactitud de inventario de 25 % a 85 %; desabastecimiento de 10 % a 1 % | D2 (RSD) | Falta el título |
| 4 | Ergetie et al. (2023), Etiopía; P103 | **Ausente** | Evaluar prácticas de cadena de frío | Transversal, autorreporte y observación; 50 participantes en 10 centros | Conocimiento 60 %; buenas prácticas 74 %; gestión IPLS deficiente 68 %; cumplimiento real 50 % | Contexto de la VD; sin intervención tecnológica | El vínculo más débil con la VI |
| 5 | Astuhuaman Perez y Baltazar Maza (2024), Apurímac; P106 | Implementación de un sistema web con IA para mejorar la gestión de citas médicas en el Centro de Salud de Nueva Fuerabamba, Apurímac 2024 (sin comillas) | Evaluar un sistema web asistido por IA en la gestión de citas | Aplicada, cuantitativa, preexperimental; 30 pacientes, 12 trabajadores, 30 días antes y después | Elaboración de citas de 9.97 a 8.47 min (−15.1 %, Wilcoxon p < 0.001); citas diarias de 10.90 a 12.07; registro en historia clínica de 6.10 a 4.60 min (−24.6 %) | D1 y diseño (preexperimental con Wilcoxon) | El más cercano en diseño y región; citas médicas, no vacunas |
| 6 | Mego Navarro (2021), Lima; P107 | "Implementación de un sistema web para la gestión de vacunas del Covid-19 en una entidad pública 2021, en Lima" | Sistema web para vacunas COVID-19 con XP | 40 especialistas estadísticos e informáticos; descriptivo | Acceso a la información: presencial 45 %, correo 30 %, celular 12.5 %, sistemas 12.5 %; información completa 50 %, incompleta 25 % | VI (XP) y contexto | Sin contraste pre-post |
| 7 | Garcia Villacorta y Calderón Huaman (2023), Lima; P108 | "Sistema web para el control de inventario en la Farmacia Pro, 2023, en Lima" | Mejorar el control de inventario | Preexperimental, cuantitativo; 68 registros (34 antes y 34 después) | Control de inventario de 75.42 % a 97.18 %; rotación de 76.78 % a 97.44 %; entregas a tiempo de 76.15 % a 97.77 %; compras de 73.44 % a 96.34 %; prueba Z p = 0.000 | D2 (análogo a CPE) | Farmacia privada |

**Vacío detectado:** ningún antecedente sustenta la D3 (satisfacción con TAM). Ndlovu et al. (2021) se usa solo en bases teóricas. No hay antecedente local de UNAJMA, aunque Jhon (2026) tampoco lo incluye.

## 4. Mapeo de bases teóricas frente a la VI y DEC-007

| Destino | Subacápites actuales | Fuentes citadas | Brecha |
|---|---|---|---|
| VI: sistema web y arquitectura | 2.2.1-2.2.3 | Sommerville (2016), Pressman (2010), Mego (2021) | 2.2.3 sin sustento teórico en el texto; API y base de datos solo en 2.3 (Ruiz Barea, 2023) |
| VI: sistemas de información en salud | 2.2.4-2.2.5 | Brooks (2024), Duong (2021) | 2.2.4 sin cita |
| VI: componente de IA | 2.2.6 | Alhazmi (2024), no catalogado | Pertinente solo si el asistente SiBot integra la intervención X. DEC-007 no contiene ningún indicador de IA |
| VI: calidad del producto | 2.2.7-2.2.10 | ISO/IEC (2023), Moumane (2024), Ndlovu (2021) | Terminología mixta 2011 y 2023; 2.2.7 sin cita |
| VI: XP | 2.2.23-2.2.25 | Sommerville, Beck, Pressman, Mego, Cohn | Cita secundaria (P230); figura con fuente comercial |
| VD: marco normativo y logístico | 2.2.11-2.2.19 | MINSA (2022), OPS y PATH (s. f.), Champi (2023), Wasswa (2023) | Definición nuclear de la VD (P172) sin cita; Kardex y Movimiento sin cita |
| **D1 Oportunidad** (Treg, Tvale) | 2.2.20 | Dang (2024), Duong (2021), Balón (2023), Astuhuaman (2024) | Conforme; P205-P206 verbosos |
| **D2 Consistencia** (RSD, CPE) | 2.2.21 | Chekol (2023), Duong (2021) | Conforme; no se citan Kigenza, Shen ni Garcia Villacorta, que la sustentan |
| **D3 Satisfacción** (AP, UP) | 2.2.22 | Ndlovu (2021); Davis (1989) solo en la nota de la Tabla 3 | **TAM no desarrollado en la prosa**; Davis sin referencia |

## 5. Citas contrastadas con el catálogo Zotero

### 5.1 Las 26 fuentes del catálogo

| N.° | Citekey | Cap. I | Cap. II | Lista de referencias | Estado |
|---|---|---|---|---|---|
| 1 | @shen2024 | P061 | P100 | P502 | Conforme |
| 2 | @balon2023 | P062 | P101, P204 | P473 | Conforme (cifra triplicada) |
| 3 | @kigenza2023 | — | P102 | P503 | Observado: sin título en el texto |
| 4 | @ergetie2023 | — | P103 | P504 | Observado: sin título en el texto |
| 5 | @astuhuaman2024 | — | P106, P204 | P472 | Observado: título sin comillas |
| 6 | @mego2021 | P063 | P107, P117, P130, P230, P232 | P490 | Observado: intermediario de Pressman; "pág." |
| 7 | @garcia2023 | P063 | P108 | P483 | Conforme (el DOCX dice "Calderón Huaman") |
| 8 | @beck1999 | — | P225-P226, P262 | P474 | Observado: "dice:", "pág.", cita traducida presentada como textual [VERIFICAR] |
| 9 | @cohn2004 | — | P247, P319 | P478 | Observado: la referencia enlaza un PDF de terceros; falta la editorial |
| 10 | @sommerville2016 | — | P112, P117, P224, P236, P238, P244, P262, P268 | P500 | Conforme |
| 11 | @pressman2010 | — | P120, P227, P230, P234, P262 | P496 | Observado: URL a una copia no oficial; falta la editorial |
| 12 | @lujanmora2002 | — | P268 | P489 | Observado: el catálogo indica editorial; el DOCX usa la URL de una muestra |
| 13 | @ruizbarea2023 | — | P277 | P499 | Conforme |
| 14 | @iso25010_2023 | — | P147, P150, P153, P158, P221 | P486 | Observado: terminología mixta |
| 15 | @moumane2024 | — | P147 | P492 | Conforme |
| 16 | @minsa2022 | — | P166, P188, P294 | P491 | Observado: URL de terceros (cep.org.pe) |
| 17 | @opspath2020 | — | P169 | P505 | **Error: "s. f." en lugar de 2020** |
| 18 | @champi2023 | — | P177, P185 | P476 | Conforme |
| 19 | @brooks2024 | — | P136, P271 | P475 | Conforme |
| 20 | @dang2024 | — | P202 | P480 | Conforme |
| 21 | @duong2021 | — | P137, P203, P212 | P482 | DOCX correcto (e28096); **catálogo con DOI erróneo** |
| 22 | @chekol2023 | — | P210 | P477 | Conforme |
| 23 | @wasswa2023 | — | P192 | P501 | Conforme |
| 24 | @ndlovu2021 | — | P162, P217, P221 | P494 | DOI correcto; **año 2022 según Crossref**; catálogo con DOI erróneo |
| 25 | @sampieri2014 | — | — | P485 | Reservada para el Cap. IV (P342 y siguientes) |
| 26 | @georgemallery2003 | — | — | P484 | Reservada para el Cap. IV (P446) |

Se citan 24 de las 26 fuentes en los Cap. I y II. El Cap. I cita solo 4 fuentes (Shen, Balón, Mego y Garcia Villacorta), todas antecedentes.

### 5.2 Citas fuera del catálogo

| Cita | Párrafo | En la lista de referencias | Verificación | Acción |
|---|---|---|---|---|
| Alhazmi et al. (2024) | P141 | Sí (P470) | Existe (Crossref) | Catalogar si se conserva 2.2.6; retirarla si se elimina |
| Davis (1989) | P221 | **No** | Existe: MIS Quarterly 13(3), 319-340, doi 10.2307/249008 | Catalogar y agregar la referencia |
| SINNAPS (2022) | P241 | No | Blog comercial | Sustituir por una fuente catalogada |

### 5.3 Defectos de la lista de referencias que afectan a la correspondencia 1:1
- 8 referencias sin cita (detalle en el hallazgo 9).
- P497 es un párrafo Bibliography vacío.
- Orden no alfabético: P501-P505 (Wasswa, Shen, Kigenza, Ergetie, OPS) están añadidas al final.

## 6. Recomendaciones priorizadas

### Prioridad 0: integridad (bloquea la QG-3)
1. **investigador-bibliografico:** catalogar Davis (1989) con doi 10.2307/249008 e incorporar la referencia en APA 7.
2. **investigador-bibliografico:** corregir en el catálogo Zotero los DOI de Duong (10.2196/28096, JMIR Formative Research 5(10), e28096) y de Ndlovu (10.2196/32722). Confirmar el año de Ndlovu (2022 según Crossref) y propagarlo al texto (P162, P217, P221) y a P494.
3. **investigador-bibliografico y redactor-academico:** confirmar el año 2020 de OPS y PATH y corregir P169 y P505.
4. **redactor-academico:** sustituir la fuente de la Figura 3 por "Adaptado de Beck (1999) y Pressman (2010)" y redibujar la figura si la imagen proviene del blog.
5. **Decisión del Director General y del tesista** (consultar a ingeniero-sivac): ¿forma parte el asistente SiBot de la intervención X?
   - Si forma parte: reescribir 2.2.6 como componente de la VI, con base en el código real, y catalogar Alhazmi (2024).
   - Si no forma parte: eliminar 2.2.6 y la referencia P470.
6. **investigador-bibliografico:** resolver las 8 referencias sin cita (citarlas o retirarlas), ordenar la lista alfabéticamente y eliminar P497.
7. **Tesista y redactor-academico:** confirmar las fechas de pretest y postest afirmadas en P094-P095 o reformularlas como plan. Está prohibido presentar mediciones no entregadas.

### Prioridad 1: estructura (redactor-academico; maquetador-docx a través del Director)
8. Consolidar 2.2 según el patrón de Jhon (2026), en dos ejes con subniveles sin numerar:
   - **VI:** sistemas web y arquitectura; sistemas de información en salud; [IA, condicional]; calidad ISO/IEC 25010:2023; XP.
   - **VD:** marco normativo y logístico; cadena de frío y conservación; movimientos, lote, inventario y kardex; D1; D2; D3 con TAM.
   - Efecto: el índice pasa de 26 a unas 2-3 entradas N3, y desaparecen las 7 micro-secciones.
9. Desnumerar 2.3 y ordenar sus términos alfabéticamente. Eliminar o reducir los 10 duplicados y alinear P305 y P308 con DEC-007 (Tvale; RSD y CPE).
10. **maquetador-docx:** con `docx_quirurgico.py`, sobre una copia versionada:
    - eliminar P138 y los 61 vacíos (conservando P129, P184 y P240);
    - normalizar los espacios de P058, P066 y P097;
    - homogeneizar "2.1.1." frente a "2.2.1";
    - borrar "(según corresponda)" en P070 y los U+200B de P213.

### Prioridad 2: estilo y concisión (redactor-academico)
11. Suprimir los párrafos de cierre redundantes (P114, P126, P155, P163, P206, P213, P218; unas 200 palabras) y trasladar el detalle operacional de P087, P096 y P205 al capítulo metodológico.
12. Reescribir el contexto del Cap. I (P061-P063) con MINSA (2022) y OPS y PATH (2020) en lugar de repetir cifras de antecedentes, y dar fuente institucional a P064 [VERIFICAR].
13. Agregar la justificación teórica (modelo Jhon) y unificar el tiempo verbal.
14. Aplicar el párrafo canónico UNAJMA a los 7 antecedentes:
    - añadir los títulos de Kigenza y Ergetie y las comillas en Astuhuaman;
    - cerrar cada uno con su aporte a SIVAC;
    - valorar sustituir a Ergetie y añadir un antecedente para la D3.
15. Desarrollar el TAM en la prosa de 2.2.22 (utilidad percibida, facilidad de uso percibida, intención de uso; Davis, 1989; Ndlovu et al.).
16. Normalizar las citas:
    - "Beck (1999) sostiene que", y "p." en lugar de "pág." (P226, P232);
    - cita directa de Pressman en P230;
    - fuentes catalogadas para las 11 afirmaciones sin cita;
    - terminología ISO/IEC 25010:2023 [VERIFICAR] y ":2023" en el título 2.2.8.

**Reducción estimada:** entre 450 y 600 palabras (redundancias, unas 200; duplicados de 2.3, unas 255; cifras repetidas, unas 50; 2.2.6 si se elimina, 87), sin pérdida de contenido sustantivo.
