---
tipo: auditoria_integridad
fecha: 2026-10-21
agente: verificador-integridad
fase: F8_INTEGRACION_EDITORIAL
documento: informe_final_v04
dictamen: BLOQUEADO_ALERTA_ROJA
controversias: 6
sustituciones: 43
---

# INFORME DE RECONCILIACIÓN DE INTEGRIDAD ACADÉMICA
## Informe Final SIVAC — versión v04 (exportación de texto plano)

**Documento auditado:** `salidas/documentos/informe_final_v04_texto_plano.md` (755 párrafos), exportación de `informe_final_v04.docx`.
**Fecha:** 2026-10-21. **Fase:** F8_INTEGRACION_EDITORIAL.
**Entregable machine-readable:** `salidas/reportes_maquetacion/reconciliacion_integridad_v05.json`.

---

## 1. Dictamen general

**BLOQUEADO_ALERTA_ROJA.**

El bloqueo obedece a dos causas independientes:

1. **C3 (crítica):** el Anexo 3 declara coeficientes V de Aiken = 1.00 e IVC = 1.00 sin dictamen firmado, después de que DEC-014 anulara el bloque psicométrico. Es una aserción huérfana: no existe juez, acta ni planilla que la respalde.
2. **C4 (crítica):** tres de las siete citas sin referencia no son verificables en ninguna base bibliográfica (Mamani, 2023; OMS y UNICEF, 2021; Rojas y Vargas, 2022).

Las controversias C1, C2, C5 y C6 son subsanables con las sustituciones contenidas en este informe. Una vez aplicadas todas las correcciones y resueltas las tres citas no verificables, el documento pasa a `OBSERVADO_SUBSANABLE` y habilita la compilación v05.

**Resumen de la intervención:** 6 controversias resueltas con fuente primaria, 43 sustituciones de párrafo o celda, 3 correcciones tabulares y 7 referencias clasificadas.

---

## 2. Resoluciones

| ID | Controversia | Fuente primaria | Dictamen | Confianza |
|---|---|---|---|---|
| C1 | Centros de acopio y operadores: 8, 11, 13, 14 y 19 | `seed.ts` L156-360 (19 `centroAcopio`); `centros_acopio_reales_sivac.json` (19 objetos); Anexo 5 (14 sujetos en 13 centros); `reporte_estadistico_completo.json` (`n_censal = 14`) | Universo: 19 centros. Muestra: 14 operadores. Cobertura: 13 centros. El 11 son microredes, no centros. | Alta (0.99) |
| C2 | XP: 15 HU/71 PH frente a 16/76; 4 frente a 5 iteraciones | `seccion_3_3_xp_completa.json`: Tabla 5 (suma 71), Tabla 6 (11+9+33+10+8 = 71), texto "quince (15) HU ... 71 PH" | Correcto: 15 HU, 71 PH, 5 iteraciones. Las 4 fases de XP son otra cosa y no se alteran. | Alta (1.00) |
| C3 | V = 1.00 e IVC = 1.00 con 12 elementos, pese a DEC-014 | DEC-014, DEC-016, DEC-019 y DEC-020; `anexos_instrumentos_validacion.json`; P0600/P0602; TABLA 51 (8 ítems) | Rehacer como formatos en blanco del Instrumento 03 Modalidad A (8 ítems); V, IVC y aplicabilidad como `[Por completar por el juez]`. | Alta (1.00) |
| C4 | Siete citas sin referencia | Lista P0711-P0752 (42 entradas, ninguna de las siete); Crossref; Open Library | 4 verificadas con entrada APA 7; 3 no verificables: eliminar o sustituir, sin inventar entradas. | Alta para las 4; nula para las 3 |
| C5 | Rutas locales `C:\Proyectos\syncova` en prosa académica | P0394 y P0406; regla canónica 03 | Sustituir por referencia al repositorio institucional y al módulo de servicios. | Alta (1.00) |
| C6 | Marcador `[Pendiente de consignar volumen exacto de registros basales]` | P0073; P0115 y P0551 (ventana de 30 días) | Eliminar el marcador y expresar la ventana basal de 30 días calendario. No se inventa volumen. | Alta (0.98) |

---

## 3. C1 — Centros de acopio y operadores

### 3.1 Regla canónica

| Concepto | Valor | Trazabilidad |
|---|---|---|
| Centros de acopio del universo institucional | 19 | `backend/prisma/seed.ts` L156-360: 19 llamadas `prisma.centroAcopio.create`; `datos/schemas/centros_acopio_reales_sivac.json`: 19 objetos |
| Operadores de la muestra censal | 14 | `salidas/estadistica/reporte_estadistico_completo.json`, `metadatos.n_censal = 14` |
| Centros cubiertos por la muestra | 13 | Anexo 5 (TABLAS 52 y 53): ALMACÉN (CHANKA) con 2 sujetos y 12 centros con 1 |
| Microredes del sistema | 11 | `seed.ts` L61-142: 11 llamadas `prisma.microred.create` |
| Centros inexistentes en la base | Huancarama, Chincheros, Uripa/Ocobamba | Sin registro `centroAcopio` en `seed.ts` ni en el JSON de 19 centros |

La formulación canónica se aplica según el contexto: **19** para el universo y el alcance del sistema; **14** para los operadores; **13** para la cobertura de la muestra. El número **11** solo es válido para microredes. El número **8** no tiene respaldo en ninguna fuente.

### 3.2 Sustituciones de párrafo

| Índice | Cambio |
|---|---|
| P0028 | "8 centros de acopio provinciales" → "trece (13) centros de acopio provinciales" |
| P0051 | "ocho centros" → "trece (13) centros"; se añade "de un universo de diecinueve (19) centros registrados en el sistema"; cifras XP corregidas (C2) |
| P0054 | Versión inglesa de los mismos tres cambios |
| P0057 | Versión quechua: 13 centros, 5 iteraciones, 71 PH, 15 HU |
| P0061 | "ocho centros de acopio" → "diecinueve centros de acopio" |
| P0063 | "cuatro especialistas ... y diez responsables periféricos" → "dos operadores del Almacén Especializado ... y doce responsables de las redes de salud" |
| P0072 | "ocho" → "diecinueve"; se añade "de ellos, trece cuentan con personal incluido en la muestra censal"; reparto 2 + 12 |
| P0075 | "ocho centros" → "diecinueve centros" (alcance de la VD) |
| P0087 | "14 operadores ... y de los ocho centros" → "14 operadores ..., distribuidos en trece centros de acopio" |
| P0093 | "ocho centros autorizados" → "diecinueve centros registrados" |
| P0115 | "ocho centros" → "diecinueve centros"; añade "distribuidos en trece centros de acopio" |
| P0251 | "once (11) centros de acopio zonales" → "diecinueve (19) centros de acopio registrados en la plataforma" |
| P0552 | "4 operadores de la sede central y 10 periféricos" → "2 operadores del Almacén Especializado y 12 de las redes" |
| P0628 | "distribuidos estratégicamente en las dependencias territoriales ... (incluyendo el Almacén" → "distribuidos en trece (13) centros de acopio ... (Almacén" |
| P0706 | "19 centros de acopio y microredes" → "diecinueve (19) centros de acopio registrados en el sistema y en las microredes" |
| P0776 | "aplicada en los 14 centros" → "aplicada a los 14 operadores en los trece (13) centros" |

### 3.3 Reconstrucción de la TABLA 30 (Tabla 2, sección 4.7)

La tabla vigente tiene 8 filas, incluye tres centros inexistentes y no coincide con el padrón del Anexo 5. Se reemplaza por 13 filas trazables:

| Centro de Acopio / Dependencia Sanitaria | Función Operativa | n | % |
|---|---|---|---|
| ALMACÉN (CHANKA) | Coordinación de Estrategia Sanitaria de Inmunizaciones y Cadena de Frío | 2 | 14.29 |
| Hospital Andahuaylas | Responsable de Almacén de Vacunas y Control de Kardex | 1 | 7.14 |
| Hospital ESSALUD Andahuaylas | Responsable de Almacén de Vacunas y Control de Kardex | 1 | 7.14 |
| Centro de Salud Andahuaylas | Responsable de Almacén de Vacunas y Control de Kardex | 1 | 7.14 |
| Talavera | Responsable de Cadena de Frío y Despacho de Biológicos | 1 | 7.14 |
| San Jerónimo | Responsable de Cadena de Frío y Despacho de Biológicos | 1 | 7.14 |
| Huancaray | Responsable de Cadena de Frío y Despacho de Biológicos | 1 | 7.14 |
| Chicmo | Responsable de Almacén de Inmunizaciones de Microred | 1 | 7.14 |
| Huancabamba | Responsable de Almacén de Inmunizaciones de Microred | 1 | 7.14 |
| Pampachiri | Responsable de Almacén de Inmunizaciones de Microred | 1 | 7.14 |
| San Antonio de Cachi | Responsable de Almacén de Inmunizaciones de Microred | 1 | 7.14 |
| Turpo | Responsable de Almacén de Inmunizaciones de Microred | 1 | 7.14 |
| Kishuara | Responsable de Almacén de Inmunizaciones de Microred | 1 | 7.14 |
| **Total** | **Población y muestra censal (N = n = 14)** | **14** | **100.00** |

*Nota:* los porcentajes pueden no sumar 100.00 por redondeo a dos decimales.

---

## 4. C2 — Cifras de Extreme Programming

La evidencia interna es consistente en 15 HU, 71 PH y 5 iteraciones:

- Tabla 5 del expediente XP: 15 historias (HU-01 a HU-15) cuya suma es 71 PH.
- Tabla 6: Iteración 1 (11 PH) + Iteración 2 (9) + Iteración 3 (33) + Iteración 4 (10) + Iteración 5 (8) = 71 PH.
- Velocidad declarada: 14.2 PH por iteración (71 / 5).
- P0272 y P0505 ya consignan 15 HU y 71 PH.

Sustituciones: P0051, P0054 y P0057 (cifras), P0792 ("cuatro" → "cinco iteraciones") y la celda de HU-06 en la TABLA 54 ("Iteración 2" → "Iteración 3"). **P0062 no se modifica:** sus "cuatro fases iterativas" son las fases de XP, no las iteraciones del plan de entregas.

---

## 5. C3 — Certificados del Anexo 3

### 5.1 Dictamen

Los tres documentos son **formatos en blanco** del Instrumento N.° 03: Cuestionario TAM, Modalidad A, ocho ítems. No son certificados emitidos. No existe dictamen firmado, por lo que:

- V de Aiken e IVC se consignan como `[Por completar por el juez]`.
- La opinión de aplicabilidad queda sin marcar.
- La fecha y el DNI quedan abiertos.
- El inventario de 12 elementos (2 de la Ficha 01 + 2 de la Ficha 02 + 8 TAM) pertenece al expediente de la VD, no al cuestionario TAM.

### 5.2 Texto nuevo del párrafo P0765

> En cumplimiento de las decisiones DEC-014 y DEC-016, se presentan los tres (3) formatos en blanco de validación de contenido por juicio de expertos, correspondientes exclusivamente al Instrumento N.° 03: Cuestionario TAM (Modalidad A, ocho ítems). Los coeficientes V de Aiken e IVC se consignan como [Por completar por el juez] y la aplicabilidad permanece sin dictamen hasta la emisión de los tres informes firmados. No se declara validez de contenido anticipada ni se atribuye a los jueces una evaluación no realizada.

### 5.3 Texto nuevo de la nota P0782

> Nota. Cuestionario TAM de ocho ítems (Modalidad A) remitido a juicio de expertos. Los coeficientes V de Aiken, IVC y Alfa de Cronbach se consignarán en el expediente una vez emitidos y firmados los dictámenes de los tres jueces.

### 5.4 Celdas de las TABLAS 46, 47 y 48

Se aplican los mismos seis cambios en cada tabla (18 celdas en total):

| Fila | Texto vigente | Texto nuevo |
|---|---|---|
| Juez Validador | Evaluador Pericial Designado (Experto N) | ____________________ (Juez N) |
| Instrumentos Auditados | Ficha Cronométrica N.° 01, Ficha de Cotejo N.° 02 y Cuestionario TAM N.° 03 | Instrumento N.° 03: Cuestionario TAM (Modalidad A, ocho ítems) |
| Coeficiente V de Aiken | V = 1.00 (Unanimidad ... para los 12 elementos de la VD) | V = [Por completar por el juez] (ocho ítems del Instrumento N.° 03, Modalidad A); IVC = [Por completar por el juez] |
| Opinión Pericial Global | [ X ] APLICABLE SIN MODIFICACIONES [ ] No aplicable | [ ] Aplicable sin modificaciones [ ] Aplicable con observaciones [ ] No aplicable |
| Fecha y Lugar | Andahuaylas, Apurímac — Perú (2026) | Andahuaylas, Apurímac — Perú, ____ de ____________ de 2026 |
| Firma y Sello | ✍️ [ESPACIO RESERVADO ...] DNI: [Registrado en expediente] | [ESPACIO RESERVADO PARA FIRMA Y SELLO DEL JUEZ] ... DNI: ____________________ |

También se sustituyen los encabezados P0766, P0768 y P0770: "Certificado de Validez de Contenido - Experto N" → "Formato de Validación de Contenido - Juez N".

---

## 6. C4 — Referencias faltantes

| Cita | Estado | Entrada APA 7 |
|---|---|---|
| Mamani (2023) | `[VERIFICAR]` | Mamani, [VERIFICAR: iniciales]. (2023). [VERIFICAR: título de la obra]. [VERIFICAR: revista o editorial]. |
| OMS y UNICEF (2021) | `[VERIFICAR]` | Organización Mundial de la Salud y Fondo de las Naciones Unidas para la Infancia. (2021). [VERIFICAR: título del informe]. [VERIFICAR: editorial o URL]. |
| Rojas y Vargas (2022) | `[VERIFICAR]` | Rojas, [VERIFICAR: iniciales] y Vargas, [VERIFICAR: iniciales]. (2022). [VERIFICAR: título de la obra]. [VERIFICAR: revista o editorial]. |
| Venkatesh et al. (2003) | Verificada (DOI) | Venkatesh, V., Morris, M. G., Davis, G. B. y Davis, F. D. (2003). User acceptance of information technology: Toward a unified view. *MIS Quarterly, 27*(3), 425-478. https://doi.org/10.2307/30036540 |
| Rosenthal (1991) | Verificada (DOI) | Rosenthal, R. (1991). *Meta-analytic procedures for social research* (Rev. ed.). Sage. https://doi.org/10.4135/9781412984997 |
| George y Mallery (2003) | Verificada (sin DOI) | George, D. y Mallery, P. (2003). *SPSS for Windows step by step: A simple guide and reference. 11.0 update* (4.ª ed.). Allyn & Bacon. |
| Hernández-Sampieri y Mendoza (2018) | Verificada (ISBN) | Hernández-Sampieri, R. y Mendoza Torres, C. P. (2018). *Metodología de la investigación: Las rutas cuantitativa, cualitativa y mixta*. McGraw-Hill Education. |

Las tres primeras no se localizaron en Crossref, Open Library ni Zotero. No se inventa ninguna entrada sustitutiva: el redactor debe eliminarlas o reemplazarlas por una fuente primaria verificable.

---

## 7. C5 y C6

| Índice | Texto nuevo |
|---|---|
| P0394 | Ecosistema tecnológico verificado mediante auditoría directa del repositorio institucional del sistema SIVAC. |
| P0406 | "La inspección del código fuente del módulo de servicios del sistema certifica la implementación de algoritmos especializados..." (resto del párrafo sin cambios) |
| P0073 | "...correspondientes a la ventana basal de treinta (30) días calendario evidenció demoras operativas recurrentes..." |

---

## 8. Clasificación de hallazgos

### Críticos

1. **C3:** coeficientes de validez declarados sin dictamen (aserción huérfana).
2. **C4:** tres citas no verificables que sostienen datos empíricos específicos (76.4%, 84.5%, e-LMIS).

### Mayores

1. **C1:** 8 y 11 centros usados como equivalentes del universo o de la muestra.
2. **C1:** TABLA 30 contiene tres centros inexistentes y omite ocho centros del padrón.
3. **C2:** 16 HU/76 PH y cuatro iteraciones en resumen, abstract, quechua y Anexo 6.
4. **C6:** marcador `[Pendiente]` en un párrafo de diagnóstico.
5. **C5:** dos rutas locales del entorno de desarrollo en prosa académica.

### Menores

1. Línea 1158: `&` en lugar de `y` en citas en español.
2. `Hernández-Sampieri et al. (2014)` aplica `et al.` a una obra de tres autores.
3. TABLA 54: denominaciones de iteraciones no alineadas con la Tabla 6 del expediente XP.
4. P0051, P0054 y P0057 conservan `[Pendiente]` sobre estadísticos de campo: estado legítimo de F6, no se altera.

---

## 9. Prescripción de acciones correctivas

Dirigidas a `redactor-academico`:

1. Aplicar las 43 sustituciones del JSON sobre el DOCX mediante el motor quirúrgico, sin recompilar desde cero.
2. Reemplazar la TABLA 30 por la versión de 13 filas y verificar que la suma sea 14.
3. Reescribir el Anexo 3 completo como formato en blanco: títulos, 18 celdas y nota P0782.
4. Incorporar a la lista de referencias las cuatro entradas verificadas y retirar las tres citas no verificables de la línea 1342-1343, junto con las afirmaciones que sostienen. Si el tesista conserva esas afirmaciones, debe entregar la fuente primaria.
5. Corregir `&` por `y` en la línea 1158 y revisar la entrada de Hernández-Sampieri et al. (2014).
6. Corregir la iteración de HU-06 y las etiquetas de iteraciones de la TABLA 54.
7. No volver a introducir cifras de centros, iteraciones o coeficientes sin la cita o el archivo de respaldo.

---

## 10. Criterios objetivos de cierre

- Cero ocurrencias de "ocho centros", "8 centros" y "once (11) centros de acopio" en el documento.
- Cero ocurrencias de "76 puntos", "16 historias", "76 story" y "cuatro iteraciones" referidas a XP.
- Cero ocurrencias de "V = 1.00" e "IVC = 1.00" en el Anexo 3.
- Siete referencias resueltas: cuatro incorporadas y tres eliminadas o sustituidas con fuente primaria.
- Cero rutas `C:\Proyectos` en el cuerpo del documento.
- Cero marcadores `[Pendiente de consignar volumen` en P0073.
- TABLA 30 con 13 centros trazables y suma de 14 operadores.

---

## 11. Fuentes consultadas

- `C:\Proyectos\syncova\backend\prisma\seed.ts` (solo lectura; L61-142 microredes, L156-360 centros de acopio).
- `datos/schemas/centros_acopio_reales_sivac.json` (19 registros).
- `salidas/documentos/informe_final_v04_texto_plano.md` (755 párrafos; P0028 a P0799).
- `salidas/documentos/seccion_3_3_xp_completa.json` (Tablas 5 y 6; HU-06 en L392).
- `salidas/documentos/anexos_instrumentos_validacion.json` (Anexo 3; inventario 2+2+8).
- `salidas/estadistica/reporte_estadistico_completo.json` (`n_censal = 14`).
- `00_SISTEMA/ESTADO_TESIS.md` (DEC-014, DEC-016, DEC-019, DEC-020).
- Crossref (DOI 10.2307/30036540 y 10.4135/9781412984997); Open Library (George y Mallery, 2003); ISBN 978-1-4562-6096-5.
