---
name: formato-instrumentos-validacion
description: Plantillas y procedimientos para el diseño de los instrumentos de recolección y del certificado único de validación por juicio de expertos del Instrumento N.° 03, bajo el modelo vigente Fany 2024 (DEC-015) para SIVAC-THESIS-LAB.
---

# FORMATO DE INSTRUMENTOS Y VALIDACIÓN POR JUICIO DE EXPERTOS: UNAJMA (EPIS)

> ## AVISO DE VIGENCIA: 2026-10-18
>
> **El modelo de validación vigente es el modelo Fany 2024 (DEC-015).** El protocolo Cóndor
> Tinoco quedó superado y se conserva archivado en
> `salidas/instrumentos/formatos_validacion/_archivo_condor_no_usar/`.
>
> El certificado vigente es **uno solo**, correspondiente al Instrumento N.° 03, Modalidad A,
> con los ocho reactivos literales de DEC-019 (DEC-020). Su estructura es:
>
> - Tabla con columnas N, DIMENSIONES / ítems, Pertinencia (Sí/No), Relevancia (Sí/No),
>   Claridad (Sí/No) y Sugerencias.
> - Bloque inferior con Observaciones, Opinión de aplicabilidad, Apellidos y nombres, DNI,
>   Especialidad, fecha y firma.
> - Emisión **íntegramente en blanco** (DEC-016): sin nombres, DNI, CIP, sellos, dictámenes,
>   marcas ni fechas fijas.
>
> **Generador vigente:** `scripts/compiladores/generar_anexo2_validacion_fany.py` produce
> `salidas/documentos/anexos_fany/ANEXO_2_VALIDACION_FANY_INST03_MODALIDAD_A_VACIO.docx`.
>
> **Prohibido:** reintroducir coeficientes V de Aiken o IVC atribuidos a jueces que no
> evaluaron (DEC-014). El material anulado está en
> `salidas/archivo/_material_apocrifo_no_usar/`.

---

## 1. Instrumentos de Recolección de Datos (3 Dimensiones, DEC-007)

El sistema SIVAC requiere tres instrumentos especializados diseñados para medir de forma
independiente las 3 dimensiones oficiales de la Variable Dependiente.

### Instrumento 1: Ficha de Registro Cronométrico (Dimensión 1: Oportunidad de Procesamiento)
- **Técnica:** Observación sistemática estructurada no participante.
- **Unidad de Análisis:** Transacciones de movimiento de biológicos (entradas y salidas)
  ejecutadas por el personal de inmunizaciones (n = 14).
- **Indicadores Medidos:**
  1. *Tiempo de registro de movimientos (T_reg):* minutos transcurridos desde la recepción de
     la vacuna física hasta el asentamiento completo del movimiento en el sistema o libro.
  2. *Tiempo de emisión de vales de pedido y PECOSA (T_vale):* minutos requeridos para
     elaborar, verificar saldos, imprimir y autorizar el vale de egreso de vacunas.
- **Estructura del Formato:** columnas para N° de Operación, Fecha y Hora, Tipo de Movimiento
  (Ingreso o Egreso), Tipo de Biológico, Lote, Hora Inicio, Hora Fin, Tiempo Total (minutos) y
  Firma del Observador.
- **Acreditación (DEC-020):** no se somete a juicio de contenido. Su validez se sustenta en el
  protocolo de medición de movimientos de vacunas (PMMV) y en el coeficiente de correlación
  intraclase ICC(2,1) >= 0.75 para el acuerdo interobservador.

### Instrumento 2: Ficha de Registro Documental de Lotes (Dimensión 2: Consistencia Documental)
- **Técnica:** Análisis documental y auditoría de inventario físico frente a registros.
- **Unidad de Análisis:** registros de movimientos en kardex y actas de entrega y recepción.
- **Indicadores Medidos:**
  1. *Porcentaje de registros sin discrepancias (RSD):*
     $$RSD = \left( \frac{\text{Registros con saldo físico idéntico al documental}}{\text{Total de registros auditados}} \right) \times 100$$
  2. *Porcentaje de concordancia programada frente a entregada (CPE):*
     $$CPE = \left( \frac{\text{Entregas con cantidad conforme}}{\text{Total de despachos evaluados}} \right) \times 100$$
- **Estructura del Formato:** columnas para Código de Auditoría, Fecha, Nombre de la Vacuna,
  Lote, Saldo Físico, Saldo Documental, Discrepancia Detectada (Sí/No), Tipo de Error (Omisión,
  Transcripción, Cálculo) y Observaciones.
- **Acreditación (DEC-020):** no se somete a juicio de contenido. Su validez se sustenta en el
  protocolo de medición de movimientos de vacunas (PMMV) y en el coeficiente kappa de Cohen
  >= 0.80 para la concordancia interauditor.

### Instrumento 3: Cuestionario de Satisfacción del Usuario, Modelo TAM (Dimensión 3)
- **Técnica:** Encuesta estructurada autoadministrada.
- **Población Objetivo:** personal de inmunizaciones y cadena de frío de la DISA Apurímac II
  (N = n = 14).
- **Escala Psicométrica:** Likert de 5 puntos (1 = Totalmente en desacuerdo, 2 = En desacuerdo,
  3 = Ni de acuerdo ni en desacuerdo, 4 = De acuerdo, 5 = Totalmente de acuerdo).
- **Modalidad A (oficial para HE3, DEC-019):** 8 reactivos, 4 de Aceptación del Proceso (AP-01
  a AP-04) y 4 de Utilidad Percibida (UP-01 a UP-04), aplicados en pretest y postest. Subescala
  de 4 a 20 puntos; total de 8 a 40 puntos.
- **Modalidad B (módulo anexo, solo postest):** 8 reactivos, 4 de Utilidad Percibida del
  software (PU-01 a PU-04) y 4 de Facilidad de Uso Percibida (PE-01 a PE-04). No se barema, no
  se contrasta y no se suma a la Modalidad A.
- **Reactivos literales de la Modalidad A (los únicos que integran el certificado):**

| Código | Reactivo |
|---|---|
| AP-01 | El procedimiento actual para asentar los movimientos diarios y cierres de mes es ágil y no demanda un esfuerzo mental o físico excesivo. |
| AP-02 | El flujo de trabajo requerido para emitir comprobantes de salida y vales de entrega es fluido y está libre de demoras o trabas burocráticas. |
| AP-03 | El método empleado me permite conciliar los saldos de inventario con las microredes generando tranquilidad y reduciendo el estrés laboral. |
| AP-04 | El tiempo que dedico al registro administrativo de vacunas es equilibrado y me deja disponibilidad para mis labores sanitarias y asistenciales. |
| UP-01 | El mecanismo de registro utilizado me permite disponer de información fidedigna y en tiempo real del stock de vacunas y jeringas. |
| UP-02 | El control de números de lote y fechas de vencimiento que brinda el proceso previene oportunamente mermas o pérdidas de biológicos. |
| UP-03 | La metodología de gestión facilita la detección inmediata y rectificación de cualquier descuadre de inventario físico versus registrado. |
| UP-04 | En general, considero que el procedimiento empleado es una herramienta altamente eficaz para garantizar el abastecimiento oportuno de vacunas. |

---

## 2. Certificado Único de Validación de Contenido (Fany 2024)

### 2.1. Alcance y Sujetos
- Se emite **un único certificado**, destinado a los ocho reactivos de la Modalidad A del
  Instrumento N.° 03 (AP-01 a AP-04 y UP-01 a UP-04), conforme a DEC-020.
- Se requieren **tres jueces** independientes con grado de Magíster o Doctor en Ingeniería de
  Sistemas, Informática o Gestión Tecnológica, con colegiatura vigente.
- La Modalidad B no recibe certificado: permanece como módulo anexo de postest, sin baremación
  ni contraste inferencial.
- Los Instrumentos N.° 01 y N.° 02 no reciben certificado de contenido; se acreditan por PMMV,
  ICC(2,1) >= 0.75 y kappa de Cohen >= 0.80.

### 2.2. Estructura de la Tabla
Encabezado de dos filas:

- Fila superior: `N`, `DIMENSIONES / ítems`, `Pertinencia` con nota al pie 1, `Relevancia` con
  nota al pie 2, `Claridad` con nota al pie 3 y `Sugerencias`.
- Fila inferior: las columnas de criterio se subdividen en `Sí` y `No`.

Cuerpo de la tabla:

- Una fila de encabezado de dimensión por cada subescala: Aceptación del Proceso (I3.1) y
  Utilidad Percibida (I3.2).
- Ocho filas, una por reactivo, con el código y el enunciado literal, seis casillas vacías de
  criterio y una celda vacía de Sugerencias.
- Cero casillas numéricas, cero escalas de gradación y cero marcas preimpresas.

### 2.3. Criterios Dicotómicos
Cada juez marca una sola opción por criterio y por reactivo:

1. **Pertinencia:** el ítem corresponde al concepto teórico formulado.
2. **Relevancia:** el ítem es apropiado para representar al componente o dimensión específica
   del constructo.
3. **Claridad:** el enunciado se entiende sin dificultad alguna, es conciso, exacto y directo.

Las tres notas al pie del formato reproducen literalmente estas definiciones.

### 2.4. Bloque Inferior del Certificado
- Observaciones (precisar si hay suficiencia), como línea en blanco.
- Opinión de aplicabilidad, con las tres opciones sin marca previa: Aplicable, Aplicable
  después de corregir, No aplicable.
- Apellidos y nombres del juez validador, en blanco.
- DNI, en blanco.
- Especialidad del validador, en blanco.
- Fecha, como línea en blanco con el año 2026.
- Firma, como espacio en blanco.

**DEC-016:** queda prohibido prellenar identidades, documentos, sellos, dictámenes, marcas de
calificación o fechas fijas. El formato se imprime y se llena a mano.

---

## 3. Estructura del Expediente de Validación

El expediente que se entrega a cada juez contiene tres piezas:

1. **Carta de presentación al experto:** membrete institucional UNAJMA, título oficial de la
   tesis, objetivos, población de estudio y solicitud formal del dictamen.
2. **Certificado Único de Validación de Contenido (Fany 2024, en blanco):** el descrito en la
   sección 2, con los ocho reactivos literales de la Modalidad A.
3. **Copia limpia del Instrumento N.° 03:** cuestionario completo, con instrucciones éticas,
   escala Likert y las dos modalidades debidamente rotuladas.

No forma parte del expediente ninguna matriz de cálculo prellenada, ninguna constancia con
veredicto anticipado ni ningún cuadro de coeficientes. La matriz de captura se construye
después, solo a partir de los certificados firmados.

---

## 4. Trazabilidad y Control de Calidad

- **Correspondencia biunívoca:** cada reactivo del certificado debe coincidir carácter por
  carácter con el enunciado del Instrumento N.° 03 y con el código del codebook.
- **Conteo verificable:** 8 reactivos, 3 criterios y 2 categorías por criterio. La matriz de
  captura resultante tiene 3 x 8 x 3 = 72 registros.
- **Prohibición de deriva:** no se admite agregar reactivos, dimensiones ni criterios ajenos a
  DEC-007, DEC-015 y DEC-019.
