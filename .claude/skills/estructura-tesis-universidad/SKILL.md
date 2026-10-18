---
name: estructura-tesis-universidad
description: Estructura formal, orden de capítulos, títulos, preliminares y maquetación OpenXML según el reglamento y modelos reales de la UNAJMA (Fany 2024 y Jhon 2026).
---

# ESTRUCTURA OFICIAL Y MAQUETACIÓN DE TESIS — UNAJMA (EPIS)

> **Marco de Referencia:** Reglamento de Grados y Títulos de la Universidad Nacional José María Arguedas (UNAJMA), Facultad de Ingeniería, Escuela Profesional de Ingeniería de Sistemas (EPIS), complementado con la síntesis de las tesis laureadas de Fany (2024, 106 p.) y Jhon (2026, 223 p.).

---

## 1. Arquitectura de Secciones y Paginación OpenXML (Word)

La tesis se divide obligatoriamente en **dos secciones desvinculadas** mediante salto de sección de página siguiente (`w:sectPr` con `header.is_linked_to_previous = False`):

### SECCIÓN 1: PÁGINAS PRELIMINARES
- **Paginación:** Números romanos en minúscula (`i`, `ii`, `iii`...) o mayúscula (`II`, `III`...), ubicados en la **esquina superior derecha**, a 2.54 cm del borde.
- **Portadas Institucionales (sin numeración impresa visible):**
  1. *Portada exterior empastada (Anexo 17):* Escudo oficial UNAJMA a color (alta resolución), nombre de la universidad en mayúsculas negrita 16 pt, facultad y escuela profesional 14 pt, título de la tesis en mayúsculas negrita 14 pt, mención del grado a optar (*"Para optar el Título Profesional de Ingeniero de Sistemas"*), autor, asesor con grado académico y registro CIP, ciudad (*Andahuaylas - Perú*) y año (*2026*).
  2. *Carátula interior:* Idéntica diagramación que la exterior.
  3. *Acta de sustentación y dictamen del jurado:* Firmas del Presidente, Primer Miembro, Segundo Miembro / Secretario y Asesor.
  4. *Certificado de conformidad del asesor de tesis.*
  5. *Declaración jurada de autenticidad y no plagio (Anexo 32):* Firmada por el tesista con porcentaje de similitud Turnitin reportado.
- **Páginas Preliminares con Paginación Visible:**
  - `ii`: **DEDICATORIA** (opcional, margen derecho o centrado, texto personal sin título de capítulo).
  - `iii`: **AGRADECIMIENTOS** (reconocimiento a la UNAJMA, EPIS, personal de la DISA Apurímac II y familiares).
  - `iv`: **ÍNDICE GENERAL** (tabla de contenido automática generada con estilos de Título 1, Título 2, Título 3 hasta 4 niveles decimales: 1.1, 1.1.1, etc.).
  - `ix`: **LISTA DE TABLAS** (tabla de ilustraciones que lista: Número de tabla, Título en cursiva y Número de página).
  - `xiii`: **LISTA DE FIGURAS** (tabla de ilustraciones que lista: Número de figura, Título en cursiva y Número de página).
  - `xvii`: **RESUMEN** (resumen estructurado en un solo párrafo justificado de **exactamente 250 palabras**, declarando objetivo, metodología, resultados cuantitativos clave y conclusión principal; seguido de 3 a 5 palabras clave separadas por comas).
  - `xviii`: **ABSTRACT** (traducción formal al inglés del resumen y keywords).
  - `xix`: **CHUMASQA** (traducción oficial al quechua chanka nativo con sus correspondientes *chawpi rimaykuna*).

---

### SECCIÓN 2: CUERPO PRINCIPAL, REFERENCIAS Y ANEXOS
- **Paginación:** Números arábigos reiniciados estrictamente en **`1`** en la primera página de la **INTRODUCCIÓN**, ubicados en la **esquina superior derecha**.
- **Desvinculación:** Se desvincula la cabecera del cuerpo principal respecto a la sección preliminar para que no herede la numeración romana.

---

## 2. Estructura Canónica de Capítulos para SIVAC (Alineación DEC-007)

### INTRODUCCIÓN (Página 1)
- Contextualización breve del problema sanitario y tecnológico.
- Formulación sintética de la propuesta (SIVAC con metodología XP).
- Estructura general capitular del informe.

### CAPÍTULO I: PLANTEAMIENTO DEL PROBLEMA
- **1.1 Realidad problemática:**
  - Contexto internacional: Directrices de la OPS/OMS sobre la digitalización de la cadena de frío y sistemas e-LMIS.
  - Contexto nacional: Normatividad del MINSA (NTS N° 196-MINSA/DGIESP-2022) y deficiencias del registro manual en el PNI.
  - Contexto regional/local: Diagnóstico situacional en el personal de inmunizaciones de la Dirección de Salud Apurímac II (Andahuaylas).
- **1.2 Formulación del problema:**
  - *Problema General:* ¿De qué manera el sistema web SIVAC influye en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025?
  - *Problema Específico 1 (D1):* ¿De qué manera el sistema web SIVAC influye en la oportunidad de procesamiento de la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025?
  - *Problema Específico 2 (D2):* ¿De qué manera el sistema web SIVAC influye en la consistencia documental de la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025?
  - *Problema Específico 3 (D3):* ¿De qué manera el sistema web SIVAC influye en la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025?
- **1.3 Objetivos de la investigación:**
  - *Objetivo General:* Determinar la influencia del sistema web SIVAC en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025.
  - *Objetivo Específico 1 (D1):* Determinar la influencia del sistema web SIVAC en la oportunidad de procesamiento de la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025.
  - *Objetivo Específico 2 (D2):* Determinar la influencia del sistema web SIVAC en la consistencia documental de la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025.
  - *Objetivo Específico 3 (D3):* Determinar la influencia del sistema web SIVAC en la satisfacción del usuario en la gestión de movimientos de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II, Andahuaylas 2025.
- **1.4 Justificación de la investigación:** Justificación teórica, metodológica, práctica/social y tecnológica.
- **1.5 Delimitaciones de la investigación:** Delimitación temporal (2025), espacial/geográfica (DISA Apurímac II, Andahuaylas) y temática/conceptual.

### CAPÍTULO II: MARCO TEÓRICO
- **2.1 Antecedentes de la investigación:**
  - *Antecedentes Internacionales:* Shen et al. (2024), Balón (2023), Kigenza et al. (2023), Ergetie et al. (2023).
  - *Antecedentes Nacionales:* Astuhuaman & Baltazar (2024, Apurímac), Mego (2021), Garcia Villacorta & Calderón (2023).
- **2.2 Bases teóricas:**
  - *Teorías de la Variable Independiente (Sistema Web SIVAC):* Arquitectura cliente-servidor (Sommerville, 2016; Luján Mora, 2002), Metodología Extreme Programming - XP (Beck, 1999; Pressman, 2010), Historias de Usuario (Cohn, 2004), Seguridad de APIs REST y JWT (Ruiz Barea, 2023), Modelo de Calidad del Producto de Software ISO/IEC 25010:2023 (ISO/IEC, 2023; Moumane et al., 2024).
  - *Teorías de la Variable Dependiente (Gestión de Movimientos de Vacunas):* Cadena de frío e inmunizaciones en salud pública (MINSA, 2022; OPS/PATH, 2020; Champi, 2023), Sistemas de Información Logística e-LMIS (Brooks et al., 2024; Wasswa et al., 2023), Transición al registro digital de biológicos (Dang et al., 2024; Duong et al., 2021), Calidad de datos y conciliación física/documental (Chekol et al., 2023).
  - *Teorías de la Dimensión 3:* Modelo de Aceptación Tecnológica - TAM (Davis, 1989; Ndlovu et al., 2021).
- **2.3 Marco conceptual:** Glosario operativo de términos técnicos y sanitarios.
- **2.4 Hipótesis de la investigación:**
  - *Hipótesis General ($H_g$ / $H_0$):* El sistema web SIVAC influye significativamente en la gestión de movimientos de vacunas...
  - *Hipótesis Específica 1 ($H_1$):* El sistema web SIVAC influye significativamente en la oportunidad de procesamiento...
  - *Hipótesis Específica 2 ($H_2$):* El sistema web SIVAC influye significativamente en la consistencia documental...
  - *Hipótesis Específica 3 ($H_3$):* El sistema web SIVAC influye significativamente en la satisfacción del usuario...

### CAPÍTULO III: DESARROLLO DE LA SOLUCIÓN TECNOLÓGICA (METODOLOGÍA XP)
- **3.1 Fase I: Exploración:**
  - Identificación de actores y roles (Administrador, Responsable de Almacén/Cadena de Frío, Personal de Inmunizaciones).
  - Catálogo de 15 Historias de Usuario (HU-01 a HU-15) con plantilla de Cohn (2004).
  - Arquitectura tecnológica desacoplada (Frontend React, Backend Node.js/Express, Base de Datos PostgreSQL/Prisma).
- **3.2 Fase II: Planificación de la Entrega (Release):**
  - Estimación de esfuerzo en Puntos de Historia (PH), priorización de valor y asignación a 4 iteraciones.
- **3.3 Fase III: Iteraciones de Desarrollo:**
  - *Iteración 1:* Autenticación, gestión de usuarios, roles y catálogo de vacunas.
  - *Iteración 2:* Registro de ingresos de vacunas, lotes, fechas de vencimiento y kardex digital.
  - *Iteración 3:* Registro de egresos, generación y validación de vales PECOSA y transferencias.
  - *Iteración 4:* Reportes consolidados, alertas tempranas de stock y panel de control (Dashboard).
  - Modelado arquitectural: Diagrama de Casos de Uso, Diagramas de Secuencia y Diagrama de Clases.
  - Modelo de Datos: Diagrama Entidad-Relación y Diccionario de Datos normalizado (3FN).
- **3.4 Fase IV: Puesta en Producción y Pruebas de Aceptación:**
  - Pruebas funcionales y de aceptación por historia de usuario con el personal de salud.
  - Evaluación técnica de calidad según la norma internacional ISO/IEC 25010:2023.

### CAPÍTULO IV: METODOLOGÍA DE LA INVESTIGACIÓN
- **4.1 Enfoque, tipo y diseño de investigación:**
  - Enfoque cuantitativo, tipo aplicada, nivel explicativo.
  - Diseño preexperimental con pretest y postest en un solo grupo ($O_1 \longrightarrow X \longrightarrow O_2$).
- **4.2 Población y muestra:**
  - Población censal: Totalidad del personal del servicio de inmunizaciones y cadena de frío de la DISA Apurímac II ($N = n = 14$).
- **4.3 Operacionalización de variables:** Matriz 1:1 con DEC-007 (VI, VD y sus 3 dimensiones).
- **4.4 Técnicas e instrumentos de recolección:**
  - Técnica 1: Observación sistemática cronométrica $\rightarrow$ Instrumento 1: Ficha de Registro Cronométrico.
  - Técnica 2: Análisis documental de inventarios $\rightarrow$ Instrumento 2: Ficha de Registro Documental de Lotes.
  - Técnica 3: Encuesta estructurada $\rightarrow$ Instrumento 3: Cuestionario TAM (escala Likert de 5 puntos).
- **4.5 Validación y confiabilidad de los instrumentos:**
  - Validez de contenido por Juicio de Expertos (3 ingenieros EPIS-UNAJMA) mediante el modelo Fany 2024 vigente por DEC-015 (criterios dicotómicos Sí/No) y el IVC de Tristán-López (2008) para el cálculo.
  - Confiabilidad del Cuestionario TAM mediante el coeficiente Alfa de Cronbach ($\alpha \ge 0.80$).
- **4.6 Plan de procesamiento y análisis de datos:**
  - Pruebas de normalidad mediante Shapiro-Wilk ($n=14 < 50$).
  - Prueba inferencial de Rangos con Signo de Wilcoxon (con estadístico $W$, valor $Z$ tipificado, $p$-valor bilateral y tamaño del efecto $r$ de Rosenthal).

### CAPÍTULO V: RESULTADOS Y DISCUSIÓN
- **5.1 Análisis descriptivo por dimensión:** Tablas y figuras pareadas (Pretest vs Postest, variación porcentual y boxplots).
- **5.2 Prueba de normalidad:** Resultados de Shapiro-Wilk sobre las diferencias pareadas ($\Delta$).
- **5.3 Contrastes de hipótesis:**
  - Contraste de Hipótesis Específica 1 (Oportunidad de procesamiento).
  - Contraste de Hipótesis Específica 2 (Consistencia documental).
  - Contraste de Hipótesis Específica 3 (Satisfacción del usuario).
  - Contraste de Hipótesis General (Gestión global de movimientos de vacunas).
- **5.4 Discusión de resultados:** Triangulación entre resultados empíricos de SIVAC, marco teórico y antecedentes (Astuhuaman, Balón, Shen, Kigenza, Dang).

### CONCLUSIONES (Correspondencia biunívoca 1:1)
1. Conclusión General (sobre la hipótesis general).
2. Conclusión Específica 1 (sobre la oportunidad de procesamiento).
3. Conclusión Específica 2 (sobre la consistencia documental).
4. Conclusión Específica 3 (sobre la satisfacción del usuario).

### RECOMENDACIONES (Correspondencia biunívoca 1:1)
1. Recomendación General (institucional para la DISA Apurímac II).
2. Recomendación Operativa 1 (sobre infraestructura y tiempos).
3. Recomendación Operativa 2 (sobre auditoría y consistencia documental).
4. Recomendación Operativa 3 (sobre capacitación y modelo TAM).

### REFERENCIAS BIBLIOGRÁFICAS
- Formato APA 7 en español, orden alfabético, sangría francesa de 1.27 cm, DOIs activos.

### ANEXOS
- Anexo 1: Matriz de consistencia lógica.
- Anexo 2: Matriz de operacionalización de variables.
- Anexo 3: Instrumentos de recolección de datos (Fichas 1 y 2, y Cuestionario TAM).
- Anexo 4: Paquete completo de validación por juicio de expertos (cartas, matrices IVC y certificados).
- Anexo 5: Certificado de confiabilidad (Alfa de Cronbach).
- Anexo 6: Fichas de Historias de Usuario (HU-01 a HU-15).
- Anexo 7: Diccionario de datos de la base de datos PostgreSQL.
- Anexo 8: Evidencias de implementación (capturas de pantalla SIVAC a 300 DPI).
- Anexo 9: Constancia de aplicación emitida por la Dirección de Salud Apurímac II.
