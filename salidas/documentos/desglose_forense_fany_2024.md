# INFORME DE ANÁLISIS FORENSE EXHAUSTIVO Y AUDITORÍA COMPARATIVA
## MODELO INSTITUCIONAL OFICIAL UNAJMA FANY 2024 VS. INFORME FINAL SIVAC (v03)
**Escuela Profesional de Ingeniería de Sistemas — Facultad de Ingeniería — Universidad Nacional José María Arguedas**  
**Documento Fuente:** Modelo Tesis Bachiller 2024 Fany (106 páginas, SHA256 verificado)  
**Documento Auditado:** `salidas/documentos/informe_final_v03.docx` (16.2 MB, 832 párrafos, 61 tablas)  
**Agente Responsable:** `analista-documental` (Squad A / Squad E)  
**Fecha de Emisión:** 2026-10-21 | **Fase Activa:** F8_INTEGRACION_EDITORIAL  

---

## 1. RESUMEN EJECUTIVO Y HALLAZGOS ESTRUCTURALES CRÍTICOS

Se ejecutó una inspección forense exhaustiva hoja por hoja sobre el **100% de las 106 páginas** del PDF oficial de la tesis de titulación de **Fany Quispe Tello (2024)**, aprobada por la Escuela Profesional de Ingeniería de Sistemas (EPIS-UNAJMA), y se contrastó sistemáticamente frente a la arquitectura de secciones, estilos y maquetación OpenXML de `informe_final_v03.docx`.

### Métricas Globales del Modelo Fany 2024:
1. **Páginas Totales:** 106 páginas físicas (100% catalogadas en `desglose_forense_fany_2024.json`).
2. **Páginas Preliminares:** 23 páginas físicas (1 Portada oficial + 13 páginas de trámites administrativos escaneados + 9 páginas preliminares académicas numeradas de `ii` a `x`).
3. **Cuerpo Capitular:** 43 páginas físicas (Página 24 a 66 / numeradas correlativamente del `11` al `53`).
4. **Secciones Finales:** 6 páginas físicas (Conclusiones p. `54`, Recomendaciones p. `55`, Bibliografía pp. `56` a `59`).
5. **Anexos:** 34 páginas físicas (Página 73 a 106 / numeradas correlativamente del `60` al `90` + 3 páginas escaneadas finales de constancia).
6. **Orientación de Página:** 104 páginas en **Vertical (PORTRAIT)** ($595.32 \times 841.92\text{ pt}$) y 2 páginas en **Horizontal (LANDSCAPE)** ($841.92 \times 595.32\text{ pt}$, correspondientes al **Anexo 1: Matriz de Consistencia**).
7. **Paginación Impresa:** Ubicada de forma invariable en el **PIE DE PÁGINA (FOOTER), ALINEADO A LA DERECHA** ($x \approx 499.2\text{ pt}, y \approx 806.4\text{ pt}$).

---

## 2. DESGLOSE FORENSE HOJA POR HOJA DEL MODELO FANY 2024

### FASE I: PORTADA Y EXPEDIENTE ADMINISTRATIVO INSTITUCIONAL (Páginas 1 a 14)
* **Página 1 (Sin número impreso): PORTADA OFICIAL INSTITUCIONAL (Anexo 17).**
  - Contiene: Escudo oficial UNAJMA a color ($6.00 \times 4.63\text{ cm}$), títulos en mayúsculas ("UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS", "FACULTAD DE INGENIERÍA", "ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS"), título de la tesis, autora ("FANY QUISPE TELLO"), asesor ("MSc. EDWING ALCIDES MAQUERA FLORES"), grado ("INGENIERA DE SISTEMAS"), ciudad y año ("ANDAHUAYLAS - APURÍMAC - PERÚ", "2024").
  - Regla OpenXML: Cuenta como página 1 / `i` pero no imprime número (`<w:titlePg/>`).
* **Páginas 2 a 14 (13 páginas de scans en alta resolución, $2340 \times 1654\text{ px}$): DOCUMENTACIÓN ADMINISTRATIVA ESCANEADA.**
  - P2: Carátula interior oficial.
  - P3: Acta oficial de sustentación y dictamen aprobatorio del jurado calificador.
  - P4: Certificado de conformidad del Asesor de Tesis.
  - P5: Reporte de originalidad Turnitin (primera página con índice $< 25\%$, firmado por asesor).
  - P6-P14: Resoluciones de aprobación de proyecto, designación de jurados dictaminadores y Declaración Jurada de Autenticidad (Anexo 32) y Repositorio (Anexo 35).
  - *Nota Técnica:* En el flujo de producción DOCX, estas 13 páginas corresponden a marcadores de posición o se integran post-Word al ensamblar el PDF final de archivo.

### FASE II: PÁGINAS PRELIMINARES ACADÉMICAS (Páginas 15 a 23 / Hojas ii a x)
* **Página 15 (Paginación: `ii` al pie derecho): DEDICATORIA.**
  - Título: `DEDICATORIA` (Centrado, Mayúsculas, Arial-BoldMT 12 pt, $y=71.2\text{ pt}$).
  - Texto: Bloque emotivo justificado/alineado a la derecha, agradeciendo a sus padres Florencio y Julia, hermanos y familia.
* **Página 16 (Paginación: `iii` al pie derecho): AGRADECIMIENTO.**
  - Título: `AGRADECIMIENTO` (Centrado, Mayúsculas, Arial-BoldMT 12 pt, $y=71.2\text{ pt}$).
  - Texto: Reconocimiento a Dios, a la UNAJMA, docentes de la EPIS, asesor y compañeros de estudio.
* **Página 17 (Paginación: `iv` al pie derecho): ÍNDICE GENERAL (Parte 1).**
  - Título: `ÍNDICE` (Centrado, Mayúsculas, Arial-BoldMT 12 pt, $y=71.2\text{ pt}$).
  - Contenido: Lista preliminares (Dedicatoria `ii`, Agradecimiento `iii`, etc.), Introducción `11`, Capítulo I `12`, Capítulo II `16`, Capítulo III `24` hasta subsección 3.2.
* **Página 18 (Paginación: `v` al pie derecho): ÍNDICE GENERAL (Parte 2).**
  - Contenido: Continuación de Capítulo IV `35`, Capítulo V `41`, Capítulo VI `51`, Conclusiones `54`, Recomendaciones `55`, Bibliografía `56` y Anexos `60`.
* **Página 19 (Paginación: `vi` al pie derecho): ÍNDICE DE FIGURAS.**
  - Título: `ÍNDICE DE FIGURAS` (Centrado, Mayúsculas, Arial-BoldMT 12 pt, $y=71.2\text{ pt}$).
  - Contenido: Lista correlativa de 12 figuras (Figura 1 a Figura 12) con número, título descriptivo y página.
* **Página 20 (Paginación: `vii` al pie derecho): ÍNDICE DE TABLAS.**
  - Título: `ÍNDICE DE TABLAS` (Centrado, Mayúsculas, Arial-BoldMT 12 pt, $y=71.2\text{ pt}$).
  - Contenido: Lista correlativa de 19 tablas (Tabla 1 a Tabla 19) con número, título descriptivo y página.
* **Página 21 (Paginación: `viii` al pie derecho): RESUMEN.**
  - Título: `RESUMEN` (Centrado, Mayúsculas, Arial-BoldMT 12 pt, $y=71.2\text{ pt}$).
  - Estructura: Párrafo único justificado de ~250 palabras (Objetivo, Metodología XP, Resultados pretest/postest, Conclusión).
  - Cierre: `Palabras clave: Proyectos, presupuesto, software, avance físico, avance económico.`
* **Página 22 (Paginación: `ix` al pie derecho): ABSTRACT.**
  - Título: `ABSTRACT` (Centrado, Mayúsculas, Arial-BoldMT 12 pt, $y=71.2\text{ pt}$).
  - Estructura: Traducción formal al inglés del resumen en un solo párrafo.
  - Cierre: `Keywords: Projects, budget, software, physical progress, economic progress.`
* **Página 23 (Paginación: `x` al pie derecho): CHUMASQA.**
  - Título: `CHUMASQA` (Centrado, Mayúsculas, Arial-BoldMT 12 pt, $y=71.2\text{ pt}$).
  - Estructura: Traducción a la lengua originaria quechua chanka exigida por el Reglamento UNAJMA.
  - Cierre: `Sapaq simikuna: Proyectos, presupuesto, software, avance físico, avance económico.`

---

### FASE III: CUERPO CAPITULAR (Páginas 24 a 66 / Hojas 11 a 53)
* **Página 24 (Paginación: `11` al pie derecho): INTRODUCCIÓN.**
  - Título: `INTRODUCCIÓN` (Centrado, Mayúsculas, 12 pt negrita, sin número capitular, $y=71.2\text{ pt}$).
  - Estructura: Presentación de la administración de proyectos, justificación de la necesidad y síntesis capitular.
* **Páginas 25 a 28 (Paginación: `12` a `15` al pie derecho): CAPÍTULO I: PROBLEMA DE INVESTIGACIÓN.**
  - Título: `CAPITULO I: PROBLEMA DE INVESTIGACIÓN` (Centrado, Mayúsculas, 12 pt negrita, salto de página obligatorio).
  - P25 (p. 12): `1.1. Realidad problemática` (Alineado a la izquierda, 11 pt negrita, sangría de párrafo 1.25 cm). Diagnóstico internacional, nacional y local (distrito de El Porvenir).
  - P26 (p. 13): `1.2. Formulación del problema`, `1.2.1. Problema general`, `1.2.2. Problemas específicos`, `1.3. Objetivos`, `1.3.1. Objetivo general`, `1.3.2. Objetivos específicos`. (Subtítulos nivel 3 en 11 pt negrita y cursiva).
  - P27 (p. 14): `1.4. Justificación` (Teórica, práctica y tecnológica).
  - P28 (p. 15): `1.5. Hipótesis`, `1.5.1. Hipótesis general`, `1.5.2. Hipótesis específicas`.
* **Páginas 29 a 36 (Paginación: `16` a `23` al pie derecho): CAPÍTULO II: ANTECEDENTES.**
  - Título: `2. CAPITULO II: ANTECEDENTES` (Centrado, Mayúsculas, 12 pt, salto de página obligatorio).
  - P29-P31: `2.1. Antecedentes internacionales` (Estudios de Rodríguez, Balón, etc.).
  - P32-P34: `2.2. Antecedentes nacionales` (Yanqui, Gálvez, etc.).
  - P35-P36: `2.3. Antecedentes locales` (Tesis UNAJMA y región Apurímac).
  - Formato canónico: Autor (Año) + Título + Objetivo + Metodología + Resultados numéricos + Conclusión + Aporte.
* **Páginas 37 a 47 (Paginación: `24` a `34` al pie derecho): CAPÍTULO III: MARCO TEÓRICO.**
  - Título: `3. CAPITULO III: MARCO TEÓRICO` (Centrado, Mayúsculas, 12 pt, salto de página obligatorio).
  - P37: `3.1. Bases teóricas`. `3.1.1. Metodología ágil Extreme Programming (XP)`.
  - P38: `Figura 1` (*Secuencia de mapeo de procesos*), `3.1.2. Software`.
  - P39-P40: `3.1.3. Gestión de proyectos`.
  - P41-P43: `Figura 2` (*Ciclo de vida*), `Figura 3` (*Fases del proyecto*), `Figura 4` (*Triple restricción*).
  - P44-P46: `3.1.4. Inversión pública en el Perú`, `Figura 5` (*Fases del ciclo de inversión*).
  - P46-P47: `3.2. Marco conceptual` (Glosario formal ordenado alfabéticamente).
* **Páginas 48 a 53 (Paginación: `35` a `40` al pie derecho): CAPÍTULO IV: METODOLOGÍA DE LA INVESTIGACIÓN.**
  - Título: `4. CAPITULO IV: METODOLOGÍA DE LA INVESTIGACIÓN` (Centrado, Mayúsculas, 12 pt negrita, salto de página obligatorio).
  - P48: `4.1. Tipo, nivel y diseño de investigación`, `4.1.1. Tipo de investigación` (Aplicada), `4.1.2. Nivel de investigación` (Explicativo/Aplicativo).
  - P49: `4.1.3. Diseño de investigación` (Preexperimental $O_1 \to X \to O_2$), `4.2. Población y muestra` (Censal, 28 proyectos de inversión).
  - P50: `Tabla 1.` (*Matriz de operacionalización de variables*, formato APA 7 de tres líneas horizontales).
  - P51: `Tabla 2.` (*Estados de los proyectos en ejecución*), `4.3. Técnicas e instrumentos de recolección de datos`.
  - P52: `4.4. Validez y confiabilidad de los instrumentos` (Juicio de 3 expertos con prueba dicotómica y Alfa de Cronbach).
  - P53: `4.5. Métodos y plan de análisis de datos` (Excel, SPSS, pruebas de Shapiro-Wilk y Wilcoxon).
* **Páginas 54 a 63 (Paginación: `41` a `50` al pie derecho): CAPÍTULO V: RESULTADOS.**
  - Título: `5. CAPITULO V: RESULTADOS` (Centrado, Mayúsculas, 12 pt negrita, salto de página obligatorio).
  - P54: `5.1. Descripción de los resultados obtenidos`. `Tabla 3` (*Validez de instrumentos por juicio de expertos*), `Tabla 4` (*Prueba de confiabilidad variable independiente*).
  - P55: `Tabla 5` (*Prueba de confiabilidad variable dependiente*), `Tabla 6` (*Porcentajes de proyectos culminados*).
  - P56: `Figura 6` (*Cantidad de proyectos culminados*), `Tabla 7` (*Proyectos culminados con presupuesto*).
  - P57: `Figura 7` (*Culminación proyectos con presupuesto*), `Tabla 8` (*Estado de proyectos*).
  - P58: `Figura 8` (*Histograma sobre el estado de proyectos*).
  - P59: `Tabla 9` (*Instrumento aplicado pretest*), `Figura 9` (*Histograma seguimiento pretest*).
  - P60: `Tabla 10` (*Instrumento aplicado postest*), `Figura 10` (*Histograma seguimiento postest*).
  - P61: `5.2. Análisis inferencial`. `Tabla 11` (*Prueba de normalidad Shapiro-Wilk*, $p < 0.05$ justificando Wilcoxon).
  - P62: `Contrastación de hipótesis`. `Tabla 12` (*Contrastación de hipótesis general*, Wilcoxon $Z=-3.411, p=0.001$).
  - P63: `Tabla 13` (*Contrastación hipótesis específica 1*, $Z=-3.300, p=0.001$), `Tabla 14` (*Contrastación hipótesis específica 2*, $Z=-3.413, p=0.001$).
* **Páginas 64 a 66 (Paginación: `51` a `53` al pie derecho): CAPÍTULO VI: DISCUSIÓN.**
  - Título: `CAPITULO VI: DISCUSIÓN` (Centrado, Mayúsculas, 12 pt negrita, salto de página obligatorio).
  - P64-P66: Triangulación y contraste frente a antecedentes (Gálvez, Lossio, Rodríguez) y marco teórico.

---

### FASE IV: SECCIONES FINALES COMPLEMENTARIAS (Páginas 67 a 72 / Hojas 54 a 59)
* **Página 67 (Paginación: `54` al pie derecho): CONCLUSIONES.**
  - Título: `CONCLUSIONES` (Centrado, Mayúsculas, 12 pt negrita, salto de página obligatorio).
  - Contenido: 3 conclusiones numeradas correlativamente (Conclusión General, Conclusión Específica 1, Conclusión Específica 2) con estricta correspondencia 1:1 con los objetivos.
* **Página 68 (Paginación: `55` al pie derecho): RECOMENDACIONES.**
  - Título: `RECOMENDACIONES` (Centrado, Mayúsculas, 12 pt negrita, salto de página obligatorio).
  - Contenido: 3 recomendaciones directas y operativas para la municipalidad y la universidad.
* **Páginas 69 a 72 (Paginación: `56` a `59` al pie derecho): BIBLIOGRAFÍA.**
  - Título: `BIBLIOGRAFÍA` (Centrado, Mayúsculas, 12 pt negrita, salto de página obligatorio).
  - Formato: Estricto orden alfabético, sangría francesa de 1.25 cm / 1.27 cm, interlineado 1.5, con enlaces activos.

---

### FASE V: ANEXOS TÉCNICOS Y METODOLÓGICOS (Páginas 73 a 106 / Hojas 60 a 90 + Scans)
* **Páginas 73 a 74 (Paginación: `60` a `61` al pie derecho): ANEXO 1. MATRIZ DE CONSISTENCIA.**
  - **ORIENTACIÓN DE PÁGINA: HORIZONTAL (LANDSCAPE)** ($841.92 \times 595.32\text{ pt}$).
  - Título: `ANEXO` / `Anexo 1. Matriz de consistencia`.
  - Estructura: Tabla de 5 columnas (Problemas, Objetivos, Hipótesis, Variables, Metodología), borde superior/inferior, sin líneas verticales.
* **Páginas 75 a 80 (Paginación: `62` a `67` al pie derecho): ANEXO 2. INSTRUMENTO DE VALIDACIÓN.**
  - Retorna a **VERTICAL (PORTRAIT)** ($595.32 \times 841.92\text{ pt}$).
  - Cartas de presentación, fichas de validación por criterio y constancias firmadas por los 3 expertos.
* **Páginas 81 a 83 (Paginación: `68` a `70` al pie derecho): ANEXO 3. INSTRUMENTO DE RECOJO DE DATOS.**
  - Cuestionario de seguimiento y control de proyectos (escala Likert 1-5).
* **Páginas 84 a 90 (Paginación: `71` a `77` al pie derecho): ANEXO 4. METODOLOGÍA DE DESARROLLO XP.**
  - P84: Planificación, historias de usuario.
  - P85-P88: `Tabla 15` a `Tabla 18` (Fichas formales de Historias de Usuario HU-01 a HU-04).
  - P89-P90: `Figura 11` y `Figura 12` (Diagramas de actividades en UML).
* **Página 91 (Paginación: `78` al pie derecho): ANEXO 5. DIAGRAMA RELACIONAL DE LA BASE DE DATOS.**
  - Diagrama físico relacional de base de datos con tablas, claves primarias y relaciones.
* **Páginas 92 a 95 (Paginación: `79` a `82` al pie derecho): ANEXOS 6 A 9. DIAGRAMAS DE CASOS DE USO.**
  - Anexo 6: Casos de uso Administrador.
  - Anexo 7: Casos de uso Contratista.
  - Anexo 8: Casos de uso Supervisor.
  - Anexo 9: Casos de uso Público en general.
* **Página 96 (Paginación: `83` al pie derecho): ANEXO 10. ORGANIGRAMA INSTITUCIONAL.**
  - Estructura organizativa de la entidad intervenida.
* **Páginas 97 a 103 (Paginación: `84` a `90` al pie derecho): ANEXOS 11 A 17. EVIDENCIAS DEL SOFTWARE (INTERFACES).**
  - Capturas de pantalla e interfaces del sistema: Login, Menú principal, Gestión de proyectos, Cronograma, Avance físico y Reportes.
* **Páginas 104 a 106 (Sin número impreso, 3 scans a página completa): CONSTANCIAS INSTITUCIONALES.**
  - Documentos emitidos y sellados por la entidad beneficiaria certificando la aplicación y conformidad del software.

---

## 3. AUDITORÍA COMPARATIVA: MODELO FANY 2024 VS. INFORME FINAL SIVAC (v03)

| Parámetro / Elemento | Modelo Oficial Fany 2024 | `informe_final_v03.docx` | Diagnóstico de Conformidad | Acción Requerida en Maquetación |
|:---|:---|:---|:---:|:---|
| **1. Secuencia de Preliminares** | Carátula -> Trámites -> Dedicatoria -> Agradecimiento -> Índices -> Resumen/Abstract/Chumasqa -> Introducción | Carátula -> Dec. Jurada -> Dedicatoria -> Agradecimiento -> **Resumen/Abstract/Chumasqa -> Índices** -> Introducción | **DISCREPANCIA DE ORDEN CRÍTICA** | **Mover Resumen, Abstract y Chumasqa para que queden DESPUÉS de los índices**, inmediatamente antes de la Introducción, tal como exige el patrón UNAJMA y Fany 2024. |
| **2. Índice de Contenidos** | Bloque de índice completo jerarquizado con títulos decimales y tabulación punteada | Párrafo aislado `ÍNDICE DE CONTENIDO` **completamente vacío** (sin entradas ni campos) | **DEFECTO CRÍTICO (VACÍO)** | Insertar campo nativo OpenXML `<w:sdt>` con instrucción `TOC \o "1-3" \h \z \u` y estilos `TOC 1`, `TOC 2`, `TOC 3`. |
| **3. Orden de Índices de Ilustraciones** | Índice de Figuras (p. `vi`) seguido de Índice de Tablas (p. `vii`) | Índice de Tablas (P[39]) colocado antes de Índice de Figuras (P[59]) | **DISCREPANCIA SECUENCIAL** | Invertir el orden para alinear con Fany 2024: colocar primero la Lista de Figuras y luego la Lista de Tablas (o viceversa según pauta de jurado, pero homogéneo). |
| **4. Ubicación de Numeración de Página** | **Pie de página (Footer), esquina inferior derecha** | **Encabezado superior (Header), esquina superior derecha** | **DISCREPANCIA DE POSICIÓN** | Evaluar con tesista si se traslada la paginación al pie derecho (modelo Fany) o si se mantiene en el encabezado superior derecho (estándar APA 7 / Jhon 2026). Ambas variantes existen en UNAJMA. |
| **5. Saltos de Página en Capítulos** | 100% de capítulos inician en nueva página con salto obligatorio | Capítulos I, II, III, IV tienen salto; **Capítulo V, Capítulo VI, Conclusiones, Recomendaciones y Anexos NO tienen salto** (`pageBreakBefore=False`) | **DEFECTO CRÍTICO DE COLISIÓN** | Inyectar `<w:pageBreakBefore/>` obligatorio en Capítulo V (P[640]), Capítulo VI (P[716]), Conclusiones (P[722]), Recomendaciones (P[727]) y Anexos (P[775]). |
| **6. Orientación de Matriz de Consistencia** | **Horizontal (LANDSCAPE)** en 2 páginas exclusivas ($841.92 \times 595.32\text{ pt}$) | **Vertical (PORTRAIT)** en tabla comprimida en P[776] | **DEFECTO DE COMPRESIÓN** | Crear una subsección con salto de sección de página siguiente (`w:sectPr` con `w:orient="landscape"` ancho 16838 dxa, alto 11906 dxa) para la Matriz de Consistencia y retornar a vertical. |
| **7. Catálogo y Orden de Anexos** | Anexo 1 (Consistencia), Anexo 2 (Validación), Anexo 3 (Instrumentos), Anexo 4 (Metodología XP) | Anexo 1 (Consistencia), Anexo 2 (Operacionalización), Anexo 3 (Validación), Anexo 4 (Instrumentos) | **ALINEADO A GUÍA UNAJMA** | `informe_final_v03.docx` incluye Operacionalización como Anexo 2 independiente conforme al estándar reglamentario V01.2025. Mantener. |
| **8. Anomalías en Tablas OpenXML** | 100% de tablas de datos con 3 líneas horizontales, `tblHeader` y `cantSplit` | 54 de 61 tablas cumplen. 7 tablas carecen de `tblHeader` y `cantSplit` | **DEFECTO MENOR** | Las 7 tablas corresponden a recuadros de una sola fila para firmas (Tablas 46, 48, 50) y fotografías de evidencia (Tablas 57-60). Inyectar `<w:cantSplit/>` para robustez geométrica. |
| **9. Tipografía y Márgenes** | Arial 11 pt, interlineado 1.5, sangría 1.25 cm, márgenes Izq 3.0, Sup 2.5, Der 2.5, Inf 2.5 | Times New Roman 12 pt, interlineado 1.5, sangría 1.27 cm, márgenes Izq 3.0, Sup 2.54, Der 2.54, Inf 2.54 | **CONFORME A CONSTITUCIÓN** | Times New Roman 12 pt es la opción principal oficial del Reglamento UNAJMA V01.2025 y de la Constitución SIVAC. Cero cambios tipográficos requeridos. |

---

## 4. PLAN DE ACCIÓN QUIRÚRGICA PARA `maquetador-docx`

Para elevar `informe_final_v03.docx` al nivel de excelencia institucional y cumplir con la compuerta de calidad QG-9, `maquetador-docx` debe ejecutar la siguiente secuencia de intervenciones automatizadas:

### Tarea 1: Reordenamiento Canónico de Secciones Preliminares
- **Acción:** Trasladar los bloques de `RESUMEN` (P[29-31]), `ABSTRACT` (P[32-34]) y `CHUMASQA` (P[35-37]) para que queden situados **inmediatamente después del Índice de Figuras y antes de la Introducción**.
- **Secuencia resultante:**
  1. Portada oficial (Sección 0, sin número).
  2. Declaración Jurada de Autenticidad (Anexo 32) (p. `ii`).
  3. Dedicatoria (p. `iii`).
  4. Agradecimientos (p. `iv`).
  5. Índice de Contenido (p. `v`).
  6. Índice de Tablas (p. `vi`).
  7. Índice de Figuras (p. `vii`).
  8. Resumen (p. `viii`).
  9. Abstract (p. `ix`).
  10. Chumasqa (p. `x`).
  11. Salto de sección desvinculado -> INTRODUCCIÓN (Sección 1, p. `1` arábigo).

### Tarea 2: Poblamiento del Índice de Contenido Nativo OpenXML
- **Acción:** Reemplazar el párrafo vacío P[38] por un contenedor estructurado `<w:sdt>` con campo nativo de Word:
  ```xml
  <w:sdt>
    <w:sdtPr><w:docPartObj><w:docPartGallery w:val="Table of Contents"/><w:docPartUnique/></w:docPartObj></w:sdtPr>
    <w:sdtContent>
      <w:p><w:pPr><w:pStyle w:val="TOCHeading"/><w:jc w:val="center"/></w:pPr>
        <w:r><w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr><w:t>ÍNDICE GENERAL</w:t></w:r>
      </w:p>
      <w:p><w:fldSimple w:instr="TOC \o &quot;1-3&quot; \h \z \u"/></w:p>
    </w:sdtContent>
  </w:sdt>
  ```

### Tarea 3: Inyección de Saltos de Página Obligatorios (`w:pageBreakBefore`)
- **Acción:** En los siguientes párrafos de títulos de capítulos y secciones maestras que actualmente carecen de salto, inyectar `<w:pageBreakBefore/>` dentro de su `<w:pPr>`:
  1. P[640]: `CAPÍTULO V: RESULTADOS`
  2. P[716]: `CAPÍTULO VI: DISCUSIÓN`
  3. P[722]: `CONCLUSIONES`
  4. P[727]: `RECOMENDACIONES`
  5. P[775]: `ANEXOS`

### Tarea 4: Sección Horizontal (Landscape) para la Matriz de Consistencia (Anexo 1)
- **Acción:** Envolver el Anexo 1 (P[776] a P[780]) entre dos saltos de sección:
  1. Antes de P[776]: Salto de sección tipo página siguiente con orientación horizontal:
     `<w:sectPr><w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1701"/></w:sectPr>`
  2. Después de P[780] (antes del Anexo 2 P[781]): Salto de sección retornando a vertical:
     `<w:sectPr><w:pgSz w:w="11906" w:h="16838" w:orient="portrait"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1701"/></w:sectPr>`
  Esto otorgará un ancho útil de impresión de $14,000\text{ dxa}$ ($24.6\text{ cm}$), permitiendo que las 5 columnas de la Matriz de Consistencia se desplieguen con legibilidad editorial sin compresión.

### Tarea 5: Blindaje Geométrico en Tablas de Firmas y Evidencias
- **Acción:** En las tablas 46, 48, 50, 57, 58, 59 y 60, inyectar `<w:cantSplit/>` en el elemento `<w:trPr>` de cada fila para evitar fragmentación o desborde en compilaciones futuras.

---

*Reporte generado por el Analista Documental — Squad A / Squad E — SIVAC Thesis Lab (UNAJMA).*