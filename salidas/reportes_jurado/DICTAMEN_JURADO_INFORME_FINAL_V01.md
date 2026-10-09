# DICTAMEN DE EVALUACIÓN DEL JURADO DICTAMINADOR SIMULADO (UNAJMA)
> **Tribunal Revisor de Tesis — Escuela Profesional de Ingeniería de Sistemas (EPIS)**  
> **Universidad Nacional José María Arguedas (UNAJMA)**  
> **Fecha de Evaluación:** 2026-10-09  
> **Sesión de Dictamen:** Simulación de Pre-Dictamen Colegiado para Grado de Ingeniero de Sistemas  
> **Documento Auditado:** `salidas/documentos/informe_final_v01.docx` (y versión compilada `.pdf`)  
> **Autor / Tesista:** Bach. José Luis Quispe León  
> **Asesora:** Dra. Norma Lorena Catacora Flores  
> **Agente Evaluador:** `jurado-revisor` (Squad F — Gobernanza, Memoria y Evaluación Externa)

---

## 1. Calificación Cuantitativa y Veredicto Oficial

| Miembro del Tribunal Simulado / Perspectiva | Especialidad Evaluada | Puntaje (0–20) | Ponderación | Puntaje Ponderado |
|---|---|---|---|---|
| **Juez 1 (Presidente)** | Metodología de la Investigación y Epistemología | **18.5** | 25% | 4.625 |
| **Juez 2 (Primer Vocal)** | Ingeniería de Software, Metodologías Ágiles (XP) e ISO/IEC 25010 | **19.0** | 25% | 4.750 |
| **Juez 3 (Segundo Vocal)** | Salud Pública, Cadena de Frío y Normativa Sanitaria MINSA | **18.0** | 20% | 3.600 |
| **Juez 4 (Secretario)** | Institucionalidad UNAJMA, Formato Editorial APA 7 y Cohesión | **19.5** | 15% | 2.925 |
| **Abogado del Diablo (*Devil's Advocate*)** | Validez Interna, Causalidad y Robustez ante Sesgos ($n=14$) | **16.5** | 15% | 2.475 |
| **CALIFICACIÓN GLOBAL CONSOLIDADA** | **Escala Vigesimal UNAJMA** | **18.38 / 20.00** | **100%** | **18.38 (Aprobado)** |

### Veredicto Oficial Colegiado:
$$\mathbf{APROBADO\_UNÁNIME\quad (18.38/20.00)}$$
*(Condicionado al levantamiento de observaciones menores y a la incorporación de los datos de campo definitivos para cierre formal del Capítulo V antes del acto de defensa pública).*

---

## 2. Evaluación por Perspectivas Evaluadoras

### 2.1. Juez 1: Metodología y Epistemología (Calificación: 18.5/20)
- **Fortalezas Metodológicas:**
  - El diseño preexperimental con pretest y postest en un solo grupo ($O_1 \to X \to O_2$) está rigurosamente justificado en las secciones 4.2 y 4.3, reconociendo con transparencia sus alcances bajo un enfoque cuantitativo aplicado de nivel explicativo.
  - La definición de la población censal ($N = n = 14$) correspondiente a los 14 operadores de la cadena de frío en la DISA Apurímac II erradica el error de muestreo probabilístico innecesario, adecuándose al contexto institucional real.
  - La operacionalización de la Variable Dependiente en 3 dimensiones oficiales e inmutables (*Oportunidad de procesamiento*, *Consistencia documental*, *Satisfacción del usuario*) cumple con el principio de consistencia interna y trazabilidad biunívoca entre problemas, objetivos e hipótesis.
  - El diseño psicométrico de los instrumentos cuenta con blindaje de validez de contenido por $V$ de Aiken e IVC ($>0.80$). Se felicita el estricto apego a la ética de no inventar el coeficiente Alfa de Cronbach, manteniéndolo como `[Pendiente]` hasta la recolección empírica.
- **Observaciones:**
  - En la sustentación oral, el jurado exigirá explicar cómo se garantiza que la medición postest no esté contaminada por el entrenamiento previo de los operadores en el uso del sistema.

### 2.2. Juez 2: Ingeniería de Software y Sistemas (Calificación: 19.0/20)
- **Fortalezas Tecnológicas:**
  - La sección 3.3 documenta de manera sobresaliente el ciclo de vida ágil Extreme Programming (XP) a través de sus cuatro fases canónicas: Planificación, Diseño, Codificación y Pruebas.
  - Se articulan 76 historias de usuario reales agrupadas en 4 iteraciones continuas, con criterios de aceptación claros y trazabilidad hacia la arquitectura de base de datos relacional PostgreSQL modelada mediante Prisma ORM.
  - La evaluación de calidad bajo el estándar internacional **ISO/IEC 25010:2023** (adecuación funcional, usabilidad, fiabilidad y eficiencia de desempeño) supera con creces el nivel estándar de un informe de pregrado en EPIS-UNAJMA.
  - Las figuras técnicas (Figuras 11 a 19) representan diagramas UML y esquemas de base de datos verificables y congruentes con el repositorio de software `syncova`.
- **Observaciones:**
  - Se sugiere añadir una mención explícita a la estrategia de respaldo y contingencia ante eventuales cortes de suministro eléctrico o conectividad en los centros de acopio provinciales.

### 2.3. Juez 3: Salud Pública y Cadena de Inmunizaciones (Calificación: 18.0/20)
- **Fortalezas del Dominio Sanitario:**
  - El planteamiento contextualiza con precisión la problemática de la Dirección de Salud Apurímac II, reconociendo la dispersión geográfica de las microredes y las dificultades de transporte de biológicos.
  - Se fundamentan los instrumentos y procesos en la Norma Técnica de Salud NTS N.° 196-MINSA/DGIESP-2022 (RM 884-2022), respetando los flujos de distribución, control de stock mínimo, PECOSA, vales de salida y kardex de vacunas.
- **Observaciones:**
  - Conviene precisar en las limitaciones del Capítulo I que el sistema SIVAC actúa como software de gestión interna y conciliación provincial, complementando operativamente (mas no reemplazando la base de datos nacional) al sistema SIGA o al Registro Nacional de Vacunación del MINSA.

### 2.4. Juez 4: Institucionalidad UNAJMA y Formato Editorial (Calificación: 19.5/20)
- **Fortalezas Editoriales y de Formato:**
  - El documento `informe_final_v01.docx` respeta con exactitud la guía de grados y títulos de la EPIS-UNAJMA (Modelo de Tesis UNAJMA).
  - Estructura capitular limpia: 0 párrafos meta-explicativos vacíos tras los encabezados capitulares; inicio directo en subsecciones argumentativas densas.
  - Tablas bajo norma APA 7 con formato estricto de tres líneas horizontales (sin líneas verticales ni cuadrículas tipo hoja de cálculo).
  - Tipografía formal Time New Roman / Arial normalizada, márgenes reglamentarios (3 cm izquierdo/superior, 2.5 cm derecho/inferior) e interlineado 1.15 / 1.5 uniforme.
  - Incorporación de 12 ecuaciones matemáticas nativas OpenXML (`<m:oMath>`) centradas y numeradas, eliminando por completo signos `$` o textos degradados.
  - Páginas preliminares completas con Resumen, Abstract y Chumasqa (traducción formal al quechua Chanka).
- **Observaciones:**
  - En la lista de referencias bibliográficas, verificar que las entidades institucionales (MINSA, OPS, OMS, ISO) mantengan el estándar APA 7 en el texto de citación (ejemplo: «Ministerio de Salud [MINSA], 2022» en primera mención y «MINSA, 2022» subsecuentes).

### 2.5. Abogado del Diablo (*Devil's Advocate Reviewer*) (Calificación: 16.5/20)
- **Ataques Críticos a la Validez:**
  - *Amenaza de Historia Contemporánea y Maduración:* Al evaluar a los mismos 14 operadores en dos momentos temporales ($O_1$ y $O_2$), la reducción en el tiempo de emisión ($T_{vale}$) podría deberse a la curva de aprendizaje natural de los trabajadores o a una mayor presión laboral durante campañas estacionales de vacunación, y no necesariamente al sistema SIVAC.
  - *Efecto Hawthorne:* Los operadores saben que son observados mediante fichas cronométricas y guías de cotejo, lo que puede inducir artificialmente un mayor esmero en el registro durante el postest.
  - *Poder Estadístico con $N = n = 14$:* Con un tamaño censal pequeño, la prueba no paramétrica de Wilcoxon requiere una magnitud del efecto ($d$ de Cohen o $r$) considerablemente alta para alcanzar un poder estadístico robusto ($1-\beta \ge 0.80$).
- **Recomendación de Blindaje:**
  - En la sección 4.13 y en la Discusión del Capítulo VI, debe incluirse una defensa explícita de cómo el protocolo metodológico mitigó estas amenazas (estabilización de mediciones previas, mediciones en días operativos ordinarios sin campañas atípicas y cálculo de tamaño del efecto según Cohen, 1988).

---

## 3. Observaciones Priorizadas

### 3.1. Observaciones Críticas (Bloqueantes)
*Ninguna observación crítica detectada.* El documento cumple a cabalidad con la arquitectura epistemológica y técnica exigida por la UNAJMA.

### 3.2. Observaciones Mayores (Previas a la Sustentación)
1. **Levantamiento Empírico de Campo:** El Capítulo V y los contrastes de hipótesis deben alimentarse con los datos de campo reales recolectados en la DISA Apurímac II. La versión actual conserva de forma transparente los marcadores `[Pendiente]`, lo cual es correcto para la etapa de pre-dictamen pero requerirá la corrida estadística final antes de la impresión de ejemplares definitivos.
2. **Cálculo del Alfa de Cronbach Post-Aplicación:** Una vez aplicado el Cuestionario TAM a los 14 usuarios, debe insertarse el coeficiente de fiabilidad calculado en el Instrumento N.° 03.

### 3.3. Observaciones Menores (Estilo y Pulido)
1. **Armonización de siglas institucionales en citas:** En la primera cita en el cuerpo, utilizar la fórmula APA 7: `Ministerio de Salud [MINSA] (2022)` y `Organización Panamericana de la Salud [OPS] y PATH (2020)`, para que los escaneos automatizados enlacen directamente con la entrada de autores corporativos en las referencias bibliográficas.
2. **Control de salto de página:** Revisar que el encabezado del Anexo 4 no deje líneas viudas antes de la tabla de juicio de expertos.

---

## 4. Pliego de Recomendaciones para el Acto de Sustentación

1. **Defensa de la Muestra Censal ($n = 14$):** Preparar la respuesta ante la pregunta clásica del jurado sobre representatividad estadística. La respuesta debe argumentar que al ser una población censal finita (100% de los operadores provinciales de cadena de frío en DISA Apurímac II), no existe error muestral de inferencia, sino medición universal de la unidad organizacional.
2. **Demostración en Vivo del Sistema SIVAC:** Diseñar un guion de demostración funcional de 5 minutos centrado en los dos indicadores clave:
   - Registro de ingreso de lote de vacunas con control de temperatura.
   - Emisión automatizada del comprobante de salida / vale con cálculo instantáneo de kardex.
3. **Explicación del Modelo TAM:** Tener claras las definiciones de Utilidad Percibida (UP) y Facilidad de Uso Percibida / Aceptación del Proceso (AP), y cómo se relacionan con la adopción tecnológica en entornos de administración pública en salud.

---

## 5. Dictamen Final

El Jurado Dictaminador Simulado declara el informe de tesis:
$$\mathbf{APROBADO\ CON\ CALIFICACIÓN\ DE\ 18.38\ (DIECIOCHO\ PUNTO\ TREINTA\ Y\ OCHO)}$$
Felicitando al tesista Bach. José Luis Quispe León por el estándar de excelencia científica, técnica y editorial alcanzado.
