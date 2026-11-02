# Erradicación de códigos internos de gobernanza — Informe final v09

**Documento base:** `salidas/documentos/informe_final_v09.docx` (no modificado)
**Versión destino:** `salidas/documentos/informe_final_v10.docx`
**Fase:** F8 — Integración editorial
**Agente:** redactor-academico (Squad E)
**Fecha:** 2026-10-21
**Órdenes emitidas:** 11 · **Archivo de aplicación:** `salidas/reportes_maquetacion/codigos_internos_v09.json`

---

## 1. Método

1. Barrido del texto visible completo (párrafos, rótulos, celdas, notas y anexos) contra los patrones `DEC-0xx`, `REGLA CANÓNICA`, `QG-`, `F8`, `Squad`, `[VERIFICAR`, `DATOS DE PRUEBA`, rutas de repositorio y comandos de ejecución.
2. Contraste contra los reportes de aplicación v05, v06 y v09 para separar las ocurrencias **ya neutralizadas** de las **vigentes**, evitando reordenar sustituciones consumadas que hoy fallarían por ancla inexistente.
3. Redacción de equivalentes académicos que conservan el referente conceptual (matriz de operacionalización, dimensiones de la variable dependiente, elaboración propia).
4. Verificación de unicidad de cada ancla en el documento y de ausencia de colisión con los títulos de anexo del índice en caché.
5. Cotejo de integridad: ninguna cifra, indicador, escala, baremo, cita ni referencia fue alterada.

---

## 2. Tabla de decisiones

| N.º | Índice | Ubicación | Ancla original (extracto) | Texto nuevo | Categoría | Justificación |
|---|---|---|---|---|---|---|
| 1 | 290 | Párrafo 290 | “…Luo et al. (2024) conforme a la decisión metodológica DEC-007.” | “…Luo et al. (2024), en correspondencia con la matriz de operacionalización institucional.” | Código interno | Se retira el código de decisión; la atribución bibliográfica y el anclaje metodológico permanecen idénticos. |
| 2 | 351 | Párrafo 351 | “En estricta observancia de la decisión metodológica DEC-007, cada requerimiento funcional…” | “En estricta observancia de la matriz de operacionalización institucional, cada requerimiento funcional…” | Código interno | Se nombra el instrumento metodológico verificable en lugar de la decisión administrativa. |
| 3 | 353 | Párrafo 353 | “Estructura taxonómica inmutable aprobada en la decisión DEC-007 y en la matriz de operacionalización institucional de la UNAJMA.” | “Estructura taxonómica inmutable aprobada en la matriz de operacionalización institucional de la UNAJMA.” | Código interno | Se elimina la mención redundante y se conserva el atributo de inmutabilidad de la taxonomía. |
| 4 | 351 | Tabla 6 (docx), fila 1, columna 3 | “Dimensión de la Variable Dependiente (DEC-007)” | “Dimensión de la Variable Dependiente” | Código interno | Encabezado de la matriz de trazabilidad; el código no aporta información al lector. Geometría intacta. |
| 5 | 646 | Párrafo 646 (rótulo) | “ADVERTENCIA METODOLÓGICA Y SALVAGUARDA DEONTOLÓGICA (DEC-007 / REGLA CANÓNICA 01):” | “Advertencia metodológica y salvaguarda deontológica:” | Código interno | Conserva la función de llamado de atención y la jerarquía tipográfica; suprime códigos y reglas internas. |
| 6 | 646 | Párrafo 646 (cuerpo) | “En estricta observancia del principio de probidad científica… (‘datos/recolectados/’)… ‘DATOS DE PRUEBA – REEMPLAZAR (DEC-007)’… (‘python scripts/estadistica/analisis_estadistico_sivac.py’)…” | “En estricta observancia del principio de probidad científica y de transparencia cuantitativa, se hace constar que los resultados… corresponden a un conjunto de datos provisionales de prueba. Dichos valores deben sustituirse por los registros definitivos que se recolecten en el trabajo de campo en la Dirección de Salud Apurímac II antes de la sustentación de la tesis. La arquitectura bioestadística implementada permite reejecutar íntegramente las tablas y las figuras…” | Código interno | **Salvaguarda de integridad empírica preservada en su totalidad**: los valores siguen declarados como provisionales y de sustitución obligatoria antes de la sustentación. Se eliminan código, regla, ruta, rótulo en mayúsculas y comando. |
| 7 | 677 | Párrafo 677 (nota de tabla) | “Nota. Evaluado mediante el Cuestionario TAM Modalidad A (DEC-019).” | “Nota. Evaluado mediante el Cuestionario TAM, Modalidad A.” | Código interno | Se retira el código de decisión; escala, rangos, baremos y fuente quedan intactos. |
| 8 | 769 | Párrafo 769 (título de anexo) | “ANEXO 1: MATRIZ DE CONSISTENCIA METODOLÓGICA (DEC-007)” | “ANEXO 1: MATRIZ DE CONSISTENCIA METODOLÓGICA” | Código interno | El anexo se nombra por su contenido; se conserva la caja alta institucional. |
| 9 | 772 | Párrafo 772 (nota de anexo) | “Nota. Matriz de consistencia metodológica aprobada según DEC-007. UNAJMA (2026).” | “Nota. Matriz de consistencia metodológica del estudio. Elaboración propia.” | Código interno | Sustitución por declaración de autoría conforme a APA 7 para instrumentos propios. |
| 10 | 773 | Párrafo 773 (título de anexo) | “ANEXO 2: MATRIZ DE OPERACIONALIZACIÓN DE VARIABLES (DEC-007)” | “ANEXO 2: MATRIZ DE OPERACIONALIZACIÓN DE VARIABLES” | Código interno | Misma operación que en el Anexo 1. |
| 11 | 776 | Párrafo 776 (nota de anexo) | “Nota. Operacionalización oficial fijada por la Decisión DEC-007. UNAJMA (2026).” | “Nota. Operacionalización de las variables del estudio. Elaboración propia.” | Código interno | Se retira la referencia al acto administrativo y se identifica la matriz como instrumento del estudio. |

El texto íntegro de cada ancla y de cada reemplazo consta en el JSON; la tabla presenta extractos para lectura.

---

## 3. Verificación de anclas

- Las once anclas son literales y únicas en el documento. Las órdenes 5 y 6 operan sobre el mismo párrafo en tramos disjuntos (rótulo y cuerpo), preservando el salto de línea interno del bloque de advertencia.
- Las órdenes 1 y 4 declaran índice 290 y 351 respectivamente como pista; la resolución efectiva se produce por ancla única y por ubicación tabular (tabla 6, fila 1, columna 3), no por índice.
- Las órdenes 2 y 3 comparten el párrafo 353 como zona de influencia, pero sus anclas no se solapan.
- El índice de contenido en caché no incluye los títulos de anexo (alcanza hasta nivel 3 y cierra en Referencias), por lo que las órdenes 8 y 10 no generan ocurrencias residuales en el índice.

## 4. Ocurrencias ya neutralizadas (no se reordenan)

Párrafos 284, 370, 648, 654, 683 y 711; Anexo 3 introductorio; rutas locales de los párrafos 448 y 458. Sus anclas ya no existen en v09: reordenarlas produciría fallos espurios.

## 5. Códigos no localizados en prosa visible

`Squad`, `QG-`, `F8` y `[VERIFICAR`: cero ocurrencias. `REGLA CANÓNICA`: una sola ocurrencia, en el rótulo cubierto por la orden 5. `DEC-014` y `DEC-016` solo figuran en reportes internos de auditoría, no en el documento.

## 6. Observaciones sin cambio

1. **Tablas 44 y 45 (Anexos 1 y 2):** las celdas no contienen códigos internos; las ocurrencias se alojan exclusivamente en las notas al pie, cubiertas por las órdenes 9 y 11.
2. **Tablas 46 y 47 (certificados de validación):** sin códigos internos en celdas ni en notas.
3. **Marcadores de plantilla** (`[Pendiente]`, `[Por completar por el juez]`): no son códigos de gobernanza, sino estado real de un dato de campo no asentado. Se conservan y se reportan al Director General.

## 7. Riesgos

1. **Índices de párrafo:** el campo `indice_docx` es una pista con tolerancia de ±3. Si una orden falla, debe corregirse la orden, nunca forzarse el documento.
2. **Campos de Word:** tras la sustitución conviene actualizar los campos al abrir el documento para que las remisiones internas reflejen los títulos de anexo sin el código.

## 8. Aplicación

```text
python scripts/compiladores/aplicar_correcciones_redaccion.py \
  --entrada salidas/documentos/informe_final_v09.docx \
  --salida  salidas/documentos/informe_final_v10.docx \
  --json    salidas/reportes_maquetacion/codigos_internos_v09.json \
  --reporte salidas/reportes_maquetacion/aplicacion_codigos_internos_v10.json
```

Resultado esperado: 11 aplicadas, 0 omitidas, 0 fallidas. Se recomienda una pasada previa con `--solo-verificar`.
