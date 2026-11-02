# INFORME DE ÓRDENES QUIRÚRGICAS DE REDACCIÓN — INFORME FINAL SIVAC

**Documento de la comisión:** `salidas/documentos/informe_final_v06.docx` (813 párrafos, 59 tablas).
**Documento sobre el que se emiten las órdenes:** `salidas/documentos/informe_final_v07.docx`.
**Entregable:** `salidas/reportes_maquetacion/redaccion_v06_ordenes.json` (41 órdenes).
**Fecha:** 2026-10-21. **Fase:** F8_INTEGRACION_EDITORIAL. **Agente:** redactor-academico (Squad E).
**Modo:** solo lectura y emisión de órdenes. El DOCX no se modificó.

---

## 1. Dictamen general

**ORDENES_EMITIDAS.** Las tres citas no verificables quedan cubiertas en su totalidad; las variantes ortográficas enumeradas quedan cubiertas en párrafos y celdas; la revisión de prosa se limita a defectos objetivos y verificables. No se alteró ninguna cifra, resultado estadístico, dimensión, indicador ni cita verificada.

| Categoría | Órdenes |
|---|---|
| `cita_no_verificable` | 2 |
| `ortografia` | 31 |
| `prosa` | 8 |
| **Total** | **41** |

---

## 2. Cambio de base: de v06 a v07 (hallazgo estructural previo)

La comisión fijó como base el `informe_final_v06.docx`. El diagnóstico de lectura reveló que **ese archivo contenía 34 párrafos con una cola duplicada**: el texto final de cada párrafo aparecía encadenado a la porción original que el aplicador no había consumido. El defecto es un efecto del mecanismo de ancla truncada de `scripts/compiladores/aplicar_correcciones_redaccion.py`: cuando el ancla es un prefijo estricto del párrafo y termina en límite de palabra, el aplicador inserta el texto nuevo y conserva la cola original, produciendo `texto_nuevo + resto_original`.

Evidencia independiente: la auditoría de referencias ya había detectado el fenómeno en el párrafo 650 ("duplicación literal de la cláusula sobre el umbral .800 y las referencias a la Tabla 4 y a la Tabla 35"), y el diagnóstico de colas lo confirmó en 34 párrafos.

Ese defecto se recortó y se verificó antes de emitir estas órdenes:

- `salidas/reportes_maquetacion/colas_diagnostico.txt` — diagnóstico de las 34 colas.
- `salidas/reportes_maquetacion/recorte_colas_v06.json` y `puntuacion_recortes_v07.json` — 33 órdenes de recorte y puntuación.
- `salidas/reportes_maquetacion/aplicacion_recortes_v07.json` — 33 aplicadas, 0 fallidas.
- `salidas/reportes_maquetacion/verificacion_v07.txt` — v07 con 813 párrafos, 59 tablas y 2730 celdas; los 28 párrafos intervenidos cierran correctamente.

Consecuencia operativa: **las órdenes de este informe se emiten sobre el v07**, que es el estado limpio. Los índices de párrafo corresponden al v07 (mapeo derivado de `aplicacion_correcciones_v06.json`: desplazamiento +88 hasta el párrafo 196, +27 en el bloque 526-552 y +1 por párrafo en los tramos 552-628; los casos 552→579, 628→654, 696→711 y 697→712 están confirmados en el reporte de aplicación).

Si el Director prefiere aplicar sobre el v06, las 41 órdenes siguen siendo válidas salvo las dos de `cita_no_verificable`, cuyas anclas corresponden al cierre limpio y no a la versión con cola duplicada; en ese caso deberá ejecutarse primero el recorte de colas.

---

## 3. Citas no verificables neutralizadas

| # | Cita | Párrafo | Criterio aplicado | Fuente que la sustituye |
|---|---|---|---|---|
| 1 | Mamani (2023) | 711 | Reatribución a fuente verificada ya asentada | Inarotul Huda et al. (2025, p. 1244) |
| 2 | OMS y UNICEF (2021) | 711 | Reatribución a fuente verificada ya asentada | Gilbert et al. (2020, p. 564) |
| 3 | Rojas y Vargas (2022) | 712 | Supresión de la atribución y reformulación como hallazgo propio | Sin atribución bibliográfica |

### 3.1. Criterio de decisión

1. **Se reatribuye** solo cuando la aserción puede sostenerse con una fuente ya citada en el documento y ya asentada en la lista de Referencias, de modo que la operación no crea ninguna referencia nueva ni exige insertar asentamientos.
2. **Se reformula sin atribución** cuando la aserción se apoyaba en una cifra que únicamente la fuente inexistente sostenía. En ese caso la cifra se retira, no se reasigna: asignarla a otra obra sería una invención bibliográfica.
3. **No se elimina ninguna cifra propia del estudio.** Los seis valores de la dimensión 1 y los seis de la dimensión 2 permanecen intactos.

### 3.2. Detalle por cita

**Mamani (2023) — párrafo 711.** La auditoría de referencias consigna: "No se localizó en Crossref, Open Library ni Zotero" y advierte una posible confusión con Mamani-Pari et al. (2026), obra distinta que no contiene la cifra de 76.4%. La aserción sobre reducción del tiempo de registro bajo un sistema web se reatribuye a **Inarotul Huda et al. (2025, p. 1244)**, referencia 747, citada en el párrafo 214, que documenta la reducción del tiempo individual de registro de 7 a 10 minutos a 2 a 3 minutos por transacción en un sistema desarrollado con Extreme Programming. La cifra de 76.4% se retira con la atribución.

**OMS y UNICEF (2021) — párrafo 711.** La auditoría la califica de "atribución genérica que no identifica una publicación concreta"; la lista solo contiene World Health Organization (2021), que no es coautorada con UNICEF y que permanece citada en los párrafos 155 y 259, por lo que retirar esta mención no deja ninguna referencia huérfana. La aserción sobre la supresión de la doble transcripción manual se reatribuye a **Gilbert et al. (2020, p. 564)**, referencia 743, citada en los párrafos 213 y 265, cuya página 564 sostiene la deducción automática de existencias y el ahorro de tiempo del personal de salud.

**Rojas y Vargas (2022) — párrafo 712.** "No se localizó". La cifra de 84.5% de errores documentales por fallas aritméticas manuales no es sostenida por ninguna de las obras verificadas del corpus (Chekol et al., 2023 no reporta un hallazgo de esa naturaleza). Se retira la atribución y la cifra; el cierre del párrafo se reformula como interpretación propia anclada en los controles FEFO y de bloqueo de saldo que el mismo párrafo declara, y en la convergencia de RSD y CPE que ese párrafo reporta.

---

## 4. Ortografía unificada (31 órdenes)

| Variante | Órdenes | Ubicaciones |
|---|---|---|
| `pre-test` / `post-test` en párrafos | 24 | 14, 139, 145, 151, 177, 203, 204, 208, 216, 218, 553, 555 (dos), 559, 564, 566, 567 (tres), 569, 612, 632, 635 |
| `pre-test` / `post-test` en celdas | 6 | Tabla 29 (filas 2, 4 y 5); Tabla 31 (filas 2, 4 y 5, columna 4) |
| Idem en matriz de consistencia | 1 | Tabla 44, fila 3, columna 5 |
| `cuadro` → `tabla` | 1 | Párrafo 579 |

**Se conservan sin cambio**, por no designar un elemento tabular del informe:

- "Cuadro de Mando", en la tabla de iteraciones de XP (acepción de panel de control).
- "Cuadros de mando", en la descripción del componente de visualización.

**Ya estaba resuelto:** el párrafo 221 ("tabla de síntesis comparativa") y los párrafos 203-204, que ingresaron limpios por reemplazo íntegro.

---

## 5. Prosa (8 órdenes)

| Párrafo | Defecto | Intervención |
|---|---|---|
| 179 | Redundancia `coadyuvó a respaldar` | Sustitución por `respaldó` |
| 179 | Gerundio encadenado que cierra una oración de más de 60 palabras | División y restitución del valor finalístico |
| 192 | Relleno `En atención a que`; perífrasis `se encuentra conformada` | `Dado que`; `está conformada` |
| 192 | Oración única de más de 60 palabras | División en dos oraciones |
| 571 | Serie enumerativa sin determinación articulada | Se completa la serie |
| 571 | Gerundio `ascendiendo` con la magnitud poblacional al final de un periodo largo | División en dos oraciones |
| 577 | Repetición inmediata de `pareado`; relleno `de manera invariable` | Supresión de ambos |
| 654 | Código interno `DEC-007` en la prosa | Sustitución por "las tres dimensiones normativas inmutables fijadas para la variable dependiente" |

Criterio rector: se intervinieron únicamente defectos objetivos, con anclas cortas y verificables. No se reescribió por reescribir, no se añadió ninguna cita y no se modificó ningún valor numérico.

---

## 6. Pendientes y marcas `[VERIFICAR]`

1. **[VERIFICAR: página exacta del dato]** Inarotul Huda et al. (2025) abarca las páginas 1244-1259; la orden cita la página 1244 por corresponder al inicio de la exposición del caso. Confirmar en el PDF antes de la compuerta QG-8.
2. **[VERIFICAR: página exacta del dato]** Gilbert et al. (2020) abarca las páginas 562-569; la deducción automática de existencias consta en la página 564. Confirmar en el PDF.
3. **Citas metodológicas epónimas sin asentamiento** (párrafos 649, 677, 679 y 683): Cronbach (1951), Feldt (1965), Shapiro-Wilk (1965), Razali y Wah (2011), Wilcoxon (1945) y Holm (1979). Ajenas a esta comisión; requieren decisión uniforme del Director: asentar la obra primaria o tratar el rótulo como nombre de prueba sin año.
4. **Fany (2024)** (párrafo 630): atribución de formato institucional sin entrada en Referencias. Requiere decisión (asentar la tesis modelo UNAJMA o reformular como formato institucional sin cita).
5. **Referencias sin cita en el texto**: Arisholm et al. (2007) y Dolan et al. (2020). Decidir entre citarlas o retirarlas de la lista.
6. **Códigos internos en notas de tabla y anexos**: persisten en el párrafo 779 (nota de matriz de consistencia) y en las notas de los expedientes. Fuera del alcance de prosa narrativa, pero deben erradicarse antes de la compilación final.
7. **Contradicciones de alcance no resueltas**: número de centros de acopio (8, 11, 13, 14 y 19 según la sección) y número de iteraciones e historias de usuario (cuatro frente a cinco iteraciones; quince y 71 puntos frente a dieciséis y 76). Son decisiones de contenido reservadas al tesista.
8. **Advertencia de integridad empírica**: el Capítulo V conserva la marca "DATOS DE PRUEBA – REEMPLAZAR". No se editó; exige decisión expresa del tesista.

---

## 7. Nota técnica para el aplicador

- Todas las anclas de párrafo son únicas en el documento y de longitud equivalente al texto nuevo, por lo que no reproducen la configuración que causó la duplicación de cola (ancla que es prefijo estricto del párrafo con texto nuevo más largo).
- Las anclas de celda son únicas dentro de la tabla, fila y columna declaradas; se evitaron deliberadamente los caracteres de subíndice en las anclas de celda para no depender de la codificación del run.
- Los índices se ofrecen como pista; la resolución debe recaer en la búsqueda global del ancla.
- Tras la aplicación, la verificación mínima es: 813 párrafos y 59 tablas sin variación; cero ocurrencias de "pre-test", "post-test", "Pre-test" y "Post-test"; cero ocurrencias de "Mamani (2023)", "OMS y UNICEF (2021)" y "Rojas y Vargas (2022)"; y ausencia de toda repetición inmediata de cláusulas en los párrafos intervenidos.
