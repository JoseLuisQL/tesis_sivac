> # AVISO DE VIGENCIA — 2026-10-18
>
> **Este registro se conserva únicamente como documentación histórica del proceso de adaptación del modelo Cóndor Tinoco. NO describe el expediente vigente.**
>
> Por **DEC-015**, el modelo de referencia institucional pasó a ser el **modelo Fany 2024** (Anexo 2, páginas impresas 62 a 65): tabla con criterios dicotómicos Sí/No de Pertinencia, Relevancia y Claridad, más columna de Sugerencias, y bloque inferior con Observaciones, Opinión de aplicabilidad, Apellidos y nombres, DNI, Especialidad, fecha y firma.
>
> Por **DEC-016**, los formatos vigentes se emiten **íntegramente en blanco**, sin nombres, DNI, CIP, sellos, dictámenes, marcas ni fechas fijas.
>
> Por **DEC-014**, el expediente de validación y la matriz de cálculo de IVC que este registro describe contenían datos sin respaldo empírico y fueron retirados a cuarentena en `salidas/archivo/_material_apocrifo_no_usar/`.
>
> **Expediente vigente:** `salidas/documentos/anexos_fany/ANEXO_2_VALIDACION_FANY_INST03_MODALIDAD_A_VACIO.docx`, certificado único del Instrumento N.° 03 conforme a **DEC-020**
>
> **Generador vigente:** `scripts/compiladores/generar_anexo2_validacion_fany.py`
>
> En consecuencia, las secciones 4 y 5 de este documento (escala de calificación de 1 a 4 y sus instrucciones de llenado) **quedan sin efecto**. El llenado vigente consiste en marcar Sí o No en cada uno de los tres criterios, por ítem.

---

# Registro Oficial de Sustituciones y Fidelidad al Modelo Institucional

**Proyecto de Tesis:** APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II  
**Institución:** Universidad Nacional José María Arguedas (UNAJMA)  
**Facultad / Escuela:** Facultad de Ingeniería / Escuela Profesional de Ingeniería de Sistemas  
**Tesista:** Bach. José Luis Quispe León (DNI N° 70519963)  
**Asesora:** Dra. Norma Lorena Catacora Flores  
**Modelo de Referencia Oficial [SUPERADO POR DEC-015]:** Dr. Enrique Cóndor Tinoco (EPIS-UNAJMA). El modelo vigente es **Fany 2024**.  
**Archivo fuente del modelo (solo lectura):** `referencias/modelos_validacion/Formato para la validacion de instrumento por ITEM.docx`  
**Carpeta de salida oficial (`FV/`):** `salidas/instrumentos/formatos_validacion/` (ya no recibe formatos vigentes)  
**Generador determinista [REESCRITO]:** `scripts/compiladores/generar_formatos_validacion.py`. Fue reescrito tras DEC-015; su ejecución por defecto no escribe ningún archivo, de modo que ya no puede imprimir formatos obsoletos en la ruta oficial.
**Carpeta vigente de formatos:** `salidas/documentos/anexos_fany/`, que aloja el certificado único del Instrumento N.° 03 conforme a **DEC-020**.

---

## 1. Principio Rector de Fidelidad

Los formatos generados en esta carpeta reproducen de manera estricta y quirúrgica el modelo institucional del Dr. Enrique Cóndor Tinoco. Toda desviación respecto al DOCX madre del modelo está rigurosamente delimitada a las variables del proyecto SIVAC y queda registrada en la tabla de sustituciones de este documento. Cualquier elemento no listado en dicha tabla es idéntico al modelo en geometría OpenXML, estilos, tipografía, sangrías y contenido literal.

---

## 2. Inventario Exhaustivo de Sustituciones Registradas

| # | Elemento / Campo | Texto del Modelo Original (Cóndor Tinoco) | Texto Oficial SIVAC | Motivo y Justificación |
|---|---|---|---|---|
| 1 | **Fecha de la Carta (Año)** | `Andahuaylas, …… de [tab punteado] de 2025` | `Andahuaylas, …… de [tab punteado] de 2026` | Actualización al año de ejecución del proceso de validación por expertos. |
| 2 | **Destinatario de la Carta** | `M.SC. IVAN SORIA SOLIS` / `Mag. Daniel Minaya Gutiérrez` | `                    ……………………………………………………………………………` (59 puntos) | Formato en blanco aplicable a cualquier juez experto del panel (idéntico a Carta 3 del modelo). |
| 3 | **Cargo del Destinatario** | `\t       Docente del Centro Preuniversitario “UNAJMA”` (Carta 3) | `                   Docente de la Escuela Profesional de Ingeniería de Sistemas` | Correspondencia con la escuela profesional de adscripción de los jueces evaluadores (idéntico a Cartas 1 y 2). |
| 4 | **Identificación del Tesista (Carta P008)** | `Nosotras, Guadalupe Lida Sihui Llacctarimay con DNI N° 70233314 y Miriam Velasque Ccorisoncco con DNI N° 76189071, tesistas del Programa de Maestría en Ingeniería de Sistemas con mención en Tecnologías de la Información y Comunicación, nos dirigimos a usted con el debido respeto y nos presentamos y exponemos: ` | `Yo, Bach. José Luis Quispe León con DNI N° 70519963, tesista de la Escuela Profesional de Ingeniería de Sistemas, me dirijo a usted con el debido respeto y me presento y expongo: ` | Concordancia gramatical a autor único (singular) e identificación oficial del tesista SIVAC y su escuela profesional. |
| 5 | **Título de la Investigación (Carta P009)** | `“MODELO PREDICTIVO CON MACHINE LEARNING PARA IDENTIFICAR EL NIVEL DE AUTOAPRENDIZAJE EN ESTUDIANTES DEL CENTRO PRE-UNIVERSITARIO, ANDAHUAYLAS - 2025”` | `“APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II”` | Título oficial e inmutable del proyecto de tesis aprobado por la UNAJMA. |
| 6 | **Grado / Título a Optar (Carta P009)** | `para obtener el grado de Magister en Ingeniería de Sistemas con mención en Tecnologías de la Información y Comunicación` | `para optar el Título Profesional de Ingeniero de Sistemas` | Título profesional de pregrado al que postula el tesista en la Escuela Profesional de Ingeniería de Sistemas. |
| 7 | **Documento Adjunto N° 4 (Carta P015)** | `Instrumento N° 1 Cuestionario para identificar el nivel de autoaprendizaje en estudiantes del Centro Pre Universitario – UNAJMA` | • INST01: `Instrumento N° 1 Ficha de observación sistemática y medición de tiempos cronometrados`<br>• INST02: `Instrumento N° 2 Guía de cotejo documental de consistencia de movimientos`<br>• INST03: `Instrumento N° 3 Cuestionario de satisfacción del usuario y aceptación tecnológica (modelo TAM)` | Nombre específico del instrumento sometido a validación por juicio de expertos según el expediente correspondiente. |
| 8 | **Líneas de Firma del Tesista (Carta P025-P028)** | Dos columnas de firmas de puntos, nombres, rol y DNI para Guadalupe Lida Sihui Llacctarimay y Miriam Velasque Ccorisoncco | Línea única centrada mediante espacios/NBSP:<br>`………………………………………………….…`<br>`Bach. José Luis Quispe León`<br>`Tesista`<br>`DNI N° 70519963` | Adaptación estructural a autor único manteniendo la estética visual y técnica de alineación por espacios/NBSP del modelo. |
| 9 | **Salto de Sección tras Carta (P028 sectPr)** | `<w:type w:val="continuous"/>` (sección continua) | Se retira `w:type="continuous"` para forzar `nextPage` nativo | Garantiza que la Carta de Presentación ocupe exactamente 1 página y que las Instrucciones comiencen limpiamente en página nueva. |
| 10 | **Declaración de Constancia (P103)** | `...Cuestionario para identificar el nivel de autoaprendizaje... presentado por las tesistas Miriam Velasque Ccorisoncco y Guadalupe Lida Sihui Llacctarimay. Luego revisar el instrumento...` | `...[Nombre del Instrumento SIVAC] del proyecto de investigación “APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II” para los efectos de su aplicación, presentado por el tesista Bach. José Luis Quispe León. Luego revisar el instrumento...` | Sustitución de metadatos del instrumento y tesista preservando literalmente la redacción del modelo y sus erratas. |
| 11 | **Filas de Ítems en Constancia (Feature posterior)** | 24 ítems del modelo de autoaprendizaje | • INST01: 8 ítems (9 filas con encabezado)<br>• INST02: 8 ítems (9 filas con encabezado)<br>• INST03: 16 ítems (17 filas con encabezado) | Adaptación a los 32 ítems de la tesis SIVAC (8 + 8 + 16) tomados de la fuente de verdad psicométrica (DEC-007). |

---

## 3. Erratas y Particularidades Preservadas Literalmente

En estricto cumplimiento de las directivas institucionales y de la auditoría forense (`01_especificacion_formatos_modelo.md` y VAL-FMT-012), se mantienen de manera intencionada las siguientes erratas del modelo original:

1. **"es suficientes"**: Preservada en la columna de Indicadores de la Rúbrica 6x3 (criterio Suficiencia, nivel 1: *"El ítem no es suficientes para medir el indicador"*, y nivel 4: *"El ítem es suficientes"*).
2. **"no corresponden a la dimensión"**: Preservada en la Rúbrica 6x3 (criterio Suficiencia, nivel 2: *"El ítem mide algún aspecto del indicador, pero no corresponden a la dimensión"*).
3. **"podría ser mejorado en la semántica"**: Preservada en la Rúbrica 6x3 (criterio Redacción, nivel 3: *"La redacción del ítem podría ser mejorado en la semántica"*).
4. **"Luego revisar"**: Preservada en el párrafo de declaración de la Constancia de Validación (*"Luego revisar el instrumento, puedo formular las siguientes apreciaciones:"*, sin la preposición "de").
5. **Mezcla singular/plural en despedida**: Preservada en la despedida de la Carta (*"Nos despedimos de Ud. reiterándole mis saludos y del mismo modo agradeciéndole por su debida atención a la presente"*).
6. **Tabs internos en texto de rúbrica**: Preservados en los encabezados y preguntas de la columna Descripción de la Rúbrica (*"¿El ítem está alineado con los objetivos\ty dimensiones?"*, *"¿El\títem\tes comprensible?"*, *"¿El\títem\testá correctamente redactado?"*).
7. **Referencia a constancia global inexistente**: Preservada en el punto 2 de las Instrucciones (*"...y “constancia de validación de contenido global del instrumento”..."*).

---

## 4. Garantía de Formato en Blanco y Ausencia de Elementos Extraños

Los formatos generados satisfacen rigurosamente los siguientes criterios de integridad psicométrica y documental:
- **Cero invención empírica:** Ninguna celda de calificación contiene dígitos (1 a 4), cruces (X) ni marcas prellenadas.
- **Campos del juez en blanco:** Nombre, DNI, profesión, grado y firma del juez evaluador se presentan en puntos suspensivos o líneas de firma en blanco para su llenado manuscrito.
- **Sin elementos agregados:** No se añaden códigos CIP, sellos institucionales pre-impresos, logotipos, banners fotográficos, casillas de verificación (checkboxes) ni fechas fijadas de constancia.
- **Sin encabezados ni pies visibles:** Los headers y footers existen en la estructura OpenXML pero contienen texto vacío (`text=''`), garantizando la total ausencia de números de página o membretes no presentes en el modelo.
- **Sin color ni sombreado:** Todas las tablas carecen de relleno de celda (`w:shd`) y el texto utiliza color automático/negro.

---

## 5. Instrucciones de Impresión y Aplicación de Campo

Para el tesista y los evaluadores:
1. **Soporte físico:** Imprimir en papel bond A4 de 80 g/m² en orientación vertical.
2. **Paginación:**
   - La Carta de Presentación se imprime en una página independiente (anverso) por cada juez.
   - La Hoja de Instrucciones y Rúbrica de Evaluación se imprime en una página única (reverso de la carta o página 2).
   - La Constancia de Validación por Ítem inicia en página nueva e independiente.
3. **Llenado:** Los jueces expertos deben registrar a mano con bolígrafo de tinta azul:
   - Sus datos en el párrafo de declaración (nombres, DNI, profesión y grado).
   - Las calificaciones de 1 a 4 en cada una de las 5 columnas de criterios psicométricos.
   - Observaciones específicas en caso de requerir ajustes (opcional).
   - Su firma manuscrita, sello profesional/institucional y DNI al pie de la constancia.
