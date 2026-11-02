# 3.3. METODOLOGÍA DE DESARROLLO DE SOFTWARE EXTREME PROGRAMMING (XP)

El desarrollo del Sistema de Información de Vacunas (SIVAC) se fundamentó metodológicamente en Extreme Programming (XP), enfoque ágil formulado originalmente por Beck (1999) y sustentado por Pressman (2010) y Sommerville (2016). Esta metodología se orienta a proyectos de software caracterizados por requerimientos altamente dinámicos y dependientes de flujos logísticos críticos, promoviendo ciclos cortos de retroalimentación, entregas tempranas y frecuentes de versiones funcionales, comunicación bidireccional continua con los usuarios operativos y una disciplina rigurosa de pruebas continuas. En el contexto de la Dirección de Salud Apurímac II (DISA Apurímac II), la adopción de Extreme Programming permitió articular estrechamente las necesidades operativas de la cadena de frío y el suministro de biológicos con la construcción de una plataforma web escalable, evaluada bajo los estándares internacionales de calidad de producto de software establecidos en la norma ISO/IEC 25010:2023.

A diferencia de las metodologías tradicionales en cascada (*Waterfall*) o del Proceso Unificado Racional (RUP), cuyos extensos periodos de análisis documental generan desfases temporales frente a las directivas sanitarias cambiantes del Ministerio de Salud (MINSA), Extreme Programming demostró una adaptabilidad superior en el contexto de la DISA Apurímac II. La metodología se sustentó en sus cinco valores cardinales: la comunicación fluida entre el equipo de desarrollo y el personal de enfermería; la simplicidad en el diseño arquitectural descartando funciones superfluas (*You Aren't Gonna Need It - YAGNI*); la retroalimentación inmediata derivada del uso diario de los prototipos operacionales; el coraje para acometer refactorizaciones continuas sobre algoritmos contables complejos; y el respeto profesional hacia los estándares de codificación y la preservación de la integridad de los datos sanitarios.

El ciclo de desarrollo adaptado para el sistema SIVAC abarcó cuatro fases secuenciales e iterativas: Planificación, Diseño Simple, Codificación y Pruebas, concluyendo con el despliegue físico y puesta en producción en la infraestructura de servidores de la institución. En la Figura 1 se esquematizan las fases metodológicas adaptadas y sus prácticas ingenieriles asociadas.

**Figura 1**  
*Fases del ciclo de desarrollo Extreme Programming (XP) adaptado a SIVAC*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_01.png]
```

*Nota.* Diagrama metodológico adaptado de Beck (1999) que ilustra la interacción iterativa entre la planificación basada en historias de usuario, el diseño simple, la codificación guiada por pruebas y las pruebas de aceptación con el cliente en la DISA Apurímac II.

---

## 3.3.1. Fase I: Planificación (Planning Game) y Especificación de Requerimientos

La fase de planificación constituyó el punto de partida del ciclo de vida del software, articulando las necesidades reales de los operadores de la cadena de inmunizaciones con las capacidades técnicas de la plataforma web. Esta fase integró la definición de la metáfora del sistema, el levantamiento de los requerimientos funcionales y no funcionales, la formulación del catálogo de historias de usuario y la ejecución del juego de la planificación (*Planning Game*) para definir el plan de entregas por iteraciones.

### 3.3.1.1. Metáfora del Sistema y Definición de Actores

En la metodología Extreme Programming, la metáfora del sistema representa una visión compartida de alto nivel que describe la operatividad global del software mediante conceptos intuitivos y analogías comprensibles tanto para los desarrolladores como para los usuarios finales (Beck, 1999). 

Para el sistema SIVAC, se adoptó la metáfora formal denominada: **"La Cadena Digital de Información en Tiempo Real para la Red de Frío Institucional"**.  
Así como los termos portavacunas, las cajas térmicas y las cámaras frigoríficas garantizan que la temperatura física de las vacunas jamás quebrante el rango normativo de $+2\ ^\circ\text{C}$ a $+8\ ^\circ\text{C}$ a lo largo de las quebradas y pisos ecológicos de las provincias de Andahuaylas y Chincheros, el sistema SIVAC actúa como el refrigerador digital ininterrumpido que custodia la integridad del lote biológico. La plataforma asegura la trazabilidad del insumo desde su arribo central remitido por el Centro Nacional de Abastecimiento de Recursos Estratégicos en Salud (CENARES), pasando por los once (11) centros de acopio zonales, hasta la emisión del comprobante de despacho que formaliza la entrega física a los establecimientos de salud del primer nivel de atención.

A partir de los levantamientos de campo y las sesiones de trabajo con los responsables sanitarios de la DISA Apurímac II, se formalizaron cuatro roles operativos en la Tabla 1, delimitando sus atribuciones en la plataforma web mediante un esquema de control de acceso basado en roles (RBAC).

**Tabla 1**  
*Roles de usuarios y responsabilidades operativas en la DISA Apurímac II*

| Rol en SIVAC | Actor Institucional | Responsabilidades en la Cadena de Suministro |
|---|---|---|
| Administrador General (`admin`) | Especialista de TI / Soporte Informático DISA | Parametrización territorial, gestión de cuentas de usuario, catálogo de vacunas, copias de seguridad y auditoría global. |
| Coordinador Regional (`coordinador`) | Dirección de la Estrategia de Inmunizaciones | Aprobación de la planificación anual de metas, monitoreo regional de stock, auditoría del kardex y autorización de transferencias. |
| Responsable de Centro de Acopio (`responsable_acopio`) | Personal de Enfermería en almacenes zonales (11 centros) | Registro de lotes FEFO, captura de movimientos mensuales, cálculo de entregas adicionales y emisión de vales oficiales PECOSA. |
| Operador de Establecimiento (`operador`) | Técnicos de centros y puestos de salud receptores | Verificación de recepciones físicas frente a comprobantes digitales, consulta de saldos asignados y reporte de contingencias. |

*Nota.* Clasificación funcional de actores establecida según el Manual de Organización y Funciones de la Dirección de Salud Apurímac II y el esquema de seguridad RBAC implementado en el sistema web SIVAC.

### 3.3.1.2. Requerimientos Funcionales del Sistema SIVAC

Los requerimientos funcionales especifican los comportamientos, servicios y cálculos que el sistema debe ejecutar de forma automatizada para satisfacer los objetivos del negocio sanitario. En la Tabla 2 se consolida el catálogo oficial compuesto por dieciséis requerimientos funcionales (RF-01 a RF-16).

**Tabla 2**  
*Catálogo de Requerimientos Funcionales del Sistema SIVAC*

| Código | Denominación del Requerimiento Funcional | Descripción Operativa y Criterio Técnico |
|---|---|---|
| RF-01 | Autenticación Segura y Gestión de Sesión | Validación criptográfica de identidad mediante tokens JWT firmados y contraseñas cifradas con algoritmo Bcrypt (costo 10). |
| RF-02 | Control de Acceso Basado en Roles (RBAC) | Restricción granular de rutas, menús e interfaces según los cuatro roles institucionales definidos en el sistema. |
| RF-03 | Filtrado Territorial Multi-Acopio | Aislamiento de datos en consultas operativas circunscribiendo al usuario a sus centros de acopio y establecimientos autorizados. |
| RF-04 | Mantenimiento de la Jerarquía Territorial | Registro, actualización y baja lógica de Redes de Salud, Microredes, Centros de Acopio y Establecimientos de Salud (RENIPRESS). |
| RF-05 | Catálogo Oficial de Biológicos e Insumos | Administración de vacunas del Esquema Nacional (MINSA), presentaciones, dosis por frasco, rangos térmicos y jeringas complementarias. |
| RF-06 | Recepción de Remesas y Registro de Lotes FEFO | Captura de remesas centrales, registro de lotes con fechas de vencimiento y ordenamiento visual y logístico bajo principio FEFO/PVPS. |
| RF-07 | Planificación Anual y Programación Mensual | Registro de metas anuales de vacunación y desglose en doce cuotas mensuales verificando la cuadratura matemática del ejercicio. |
| RF-08 | Registro Digital de Movimientos Mensuales | Captura de saldos iniciales, transferencias de ingreso, salidas ordinarias, transferencias de salida y entregas base en cuadrícula interactiva. |
| RF-09 | Sincronización Recursiva de Saldos Intermensuales | Cálculo automático del saldo final de cada mes y propagación como saldo inicial del mes subsiguiente ($M+1$) con cero error aritmético. |
| RF-10 | Algoritmo de Redistribución Automática de Cuotas | Compensación ordenada de variaciones mensuales en las cuotas futuras para conservar invariable la meta anual del establecimiento. |
| RF-11 | Control de Entregas Adicionales y de Emergencia | Registro de hasta cinco despachos extraordinarios por mes sustentados con justificación sanitaria ante brotes o campañas. |
| RF-12 | Emparejamiento Normado de Jeringas e Insumos | Cálculo automatizado de insumos descartables y diluyentes según factores normativos configurados por vacuna o centro de acopio. |
| RF-13 | Emisión Instantánea de Vales Oficiales (PECOSA) | Generación del comprobante de despacho con correlativo institucional único garantizando que no existan duplicidades de emisión. |
| RF-14 | Motor de Exportación en Formatos PDF y Excel | Renderizado en servidor de documentos PDF vectoriales y hojas de cálculo Excel (.xlsx) estructuradas con el membrete oficial institucional. |
| RF-15 | Kardex Físico-Valorado Cronológico por Lote | Consulta histórica e inmutable de transacciones de almacén (ingresos, salidas, transferencias y ajustes) con detalle de saldos y respaldos. |
| RF-16 | Centro de Alertas Tempranas y Semáforo MSD | Detección de lotes próximos a caducar, control de cooldown de 7 días y cálculo del semáforo de Meses de Stock Disponible (ICI-DEMID). |

*Nota.* Requerimientos relevados mediante entrevistas y grupos focales con los profesionales de inmunizaciones y auditoría de la Dirección de Salud Apurímac II.

### 3.3.1.3. Requerimientos No Funcionales según ISO/IEC 25010:2023

Los requerimientos no funcionales definen los atributos de calidad, rendimiento, seguridad y mantenibilidad de la solución tecnológica conforme a la norma internacional ISO/IEC 25010:2023. En la Tabla 3 se detallan los ocho requerimientos no funcionales formalizados para SIVAC.

**Tabla 3**  
*Catálogo de Requerimientos No Funcionales según ISO/IEC 25010:2023*

| Código | Característica de Calidad | Especificación del Requerimiento No Funcional | Métrica o Estándar de Conformidad |
|---|---|---|---|
| RNF-01 | Adecuación Funcional | Cobertura completa de la lógica de distribución de biológicos e insumos sin errores de cálculo contable. | $0.00\%$ de discrepancia aritmética en balances y $100\%$ de cobertura de procesos normados. |
| RNF-02 | Eficiencia de Desempeño | Tiempo de respuesta ágil en la consulta de inventarios y procesamiento de transacciones contables. | Latencia media de la API REST menor a 350 milisegundos en red local institucional. |
| RNF-03 | Eficiencia de Desempeño | Emisión instantánea de comprobantes de despacho y exportación de archivos oficiales para impresión. | Generación de vales en base de datos menor a 3 segundos; descarga de PDF/Excel menor a 4 segundos. |
| RNF-04 | Usabilidad | Diseño intuitivo tipo hoja de cálculo con prevención proactiva de errores y retroalimentación inmediata. | Curva de aprendizaje para nuevos operadores menor a 25 minutos; navegación por teclado habilitada. |
| RNF-05 | Fiabilidad y Consistencia | Integridad transaccional y protección contra pérdidas de datos durante operaciones concurrentes de múltiples centros. | Soporte pleno de transacciones ACID en PostgreSQL mediante bloques atómicos de Prisma ORM. |
| RNF-06 | Seguridad | Salvaguarda de la confidencialidad, autenticidad e integridad de la información institucional sanitaria. | Cifrado Bcrypt salt 10 para contraseñas, tokens JWT HMAC-SHA256 y cabeceras de seguridad Helmet. |
| RNF-07 | Mantenibilidad | Arquitectura desacoplada, código fuertemente tipado y documentación modular estructurada. | Lenguaje TypeScript estricto en frontend y backend; cobertura de pruebas unitarias automatizadas. |
| RNF-08 | Portabilidad y Despliegue | Facilidad de despliegue, migración y ejecución independiente del sistema operativo subyacente. | Contenerización completa mediante Docker y Docker Compose con servidor proxy inverso Nginx. |

*Nota.* Parámetros de calidad formulados según las directrices del modelo de calidad de producto de software ISO/IEC 25010:2023.

### 3.3.1.4. Trazabilidad Requerimientos vs Dimensiones de la Variable Dependiente

En estricta observancia de la decisión metodológica DEC-007, cada requerimiento funcional e historia de usuario se diseñó con un propósito directo sobre los indicadores de la Variable Dependiente (*Gestión de movimientos mensuales de vacunas*). En la Tabla 4 se establece la matriz de correspondencia biunívoca entre los componentes de software y las tres dimensiones del estudio.

**Tabla 4**  
*Matriz de trazabilidad entre Requerimientos Funcionales, Historias de Usuario y Dimensiones de la Variable Dependiente*

| Requerimiento Funcional | Historia de Usuario | Dimensión de la Variable Dependiente (DEC-007) | Indicador Oficial Impactado |
|---|---|---|---|
| RF-06, RF-08, RF-09 | HU-04, HU-06, HU-07 | Dimensión 1: Oportunidad de procesamiento | Indicador 1.1: Tiempo de registro de movimiento ($T_{reg}$) |
| RF-12, RF-13, RF-14 | HU-10, HU-11, HU-12 | Dimensión 1: Oportunidad de procesamiento | Indicador 1.2: Tiempo de emisión de comprobante ($T_{vale}$) |
| RF-05, RF-08, RF-09, RF-15 | HU-03, HU-06, HU-07, HU-13 | Dimensión 2: Consistencia documental | Indicador 2.1: Registros sin discrepancias ($RSD$) |
| RF-04, RF-07, RF-10 | HU-02, HU-05, HU-08 | Dimensión 2: Consistencia documental | Indicador 2.2: Concordancia programada vs entregada ($CPE$) |
| RF-01, RF-02, RF-03, RF-08 | HU-01, HU-06, HU-09 | Dimensión 3: Satisfacción del usuario | Indicador 3.1: Aceptación del proceso operativo ($AP$) |
| RF-14, RF-15, RF-16 | HU-12, HU-14, HU-15 | Dimensión 3: Satisfacción del usuario | Indicador 3.2: Utilidad percibida bajo modelo TAM ($UP$) |

*Nota.* Estructura taxonómica inmutable aprobada en la decisión DEC-007 y en la matriz de operacionalización institucional de la UNAJMA.

### 3.3.1.5. El Juego de la Planificación (Planning Game) y Estimación de Historias de Usuario

La estimación del esfuerzo de desarrollo se llevó a cabo mediante la práctica del *Planning Game*, congregando al equipo técnico y al cliente en el sitio (*On-site Customer*, representado por la Coordinación de Inmunizaciones y los Responsables de Centros de Acopio). Se empleó la técnica participativa de *Planning Poker* utilizando la serie numérica de Fibonacci modificada (1, 2, 3, 5, 8, 13 Puntos de Historia), asignando valores de esfuerzo relativo en función de la complejidad algorítmica, volumen transaccional e incertidumbre tecnológica.

El catálogo se consolidó en quince (15) Historias de Usuario ($HU_1$ a $HU_{15}$), sumando un esfuerzo global de **71 Puntos de Historia (PH)**. En la Tabla 5 se presentan las historias de usuario priorizadas por el valor de negocio aportado a la DISA Apurímac II.

**Tabla 5**  
*Matriz del Planning Game: Estimación en Puntos de Historia, Prioridad e Iteración*

| Código | Título de la Historia de Usuario | Prioridad | Estimación (PH) | Iteración | Dimensión de la VD Vinculada |
|:---:|---|:---:|:---:|:---:|:---:|
| HU-01 | Autenticación Segura y Control de Acceso RBAC | Alta | 3 PH | Iteración 1 | Dimensión 3: Satisfacción del usuario |
| HU-02 | Gestión de Estructura Territorial Jerárquica | Alta | 5 PH | Iteración 1 | Dimensión 2: Consistencia documental |
| HU-03 | Catálogo Maestro de Biológicos y Jeringas | Alta | 3 PH | Iteración 1 | Dimensión 2: Consistencia documental |
| HU-04 | Recepción de Lotes y Despacho FEFO/PVPS | Alta | 5 PH | Iteración 2 | Dimensión 1 y Dimensión 2 |
| HU-05 | Planificación Anual y Programación Mensual | Media | 4 PH | Iteración 2 | Dimensión 2: Consistencia documental |
| HU-06 | Registro Digital de Movimientos Mensuales | Muy Alta | 8 PH | Iteración 3 | Dimensión 1 y Dimensión 3 |
| HU-07 | Sincronización Automática de Saldos M+1 | Muy Alta | 5 PH | Iteración 3 | Dimensión 1 y Dimensión 2 |
| HU-08 | Redistribución Automática de Cuotas Anuales | Alta | 5 PH | Iteración 3 | Dimensión 2: Consistencia documental |
| HU-09 | Registro de Entregas Adicionales y Emergencia | Alta | 4 PH | Iteración 3 | Dimensión 1 y Dimensión 2 |
| HU-10 | Cálculo Automatizado de Jeringas por Dosis | Media | 3 PH | Iteración 3 | Dimensión 1 y Dimensión 2 |
| HU-11 | Emisión Instantánea de Vales Oficiales PECOSA | Muy Alta | 8 PH | Iteración 3 | Dimensión 1: Oportunidad |
| HU-12 | Motor de Exportación en Formatos Excel y PDF | Alta | 5 PH | Iteración 4 | Dimensión 1 y Dimensión 3 |
| HU-13 | Kardex Físico-Valorado Cronológico por Lote | Alta | 5 PH | Iteración 4 | Dimensión 2: Consistencia documental |
| HU-14 | Alertas Tempranas de Vencimiento y Stock | Media | 4 PH | Iteración 5 | Dimensión 2 y Dimensión 3 |
| HU-15 | Dashboard Ejecutivo y Módulo ICI-DEMID (MSD) | Media | 4 PH | Iteración 5 | Dimensión 3: Satisfacción del usuario |
| **Total** | **Catálogo Consolidado de 15 Historias** | — | **71 PH** | **5 Iteraciones** | **Cobertura 100% de la VD** |

*Nota.* Estimación de esfuerzo relativo acordada entre el equipo de ingeniería y los representantes de la Dirección de Salud Apurímac II.

### 3.3.1.6. Plan de Entregas e Iteraciones (Release Plan)

Con base en una velocidad de desarrollo observada de aproximadamente 14.2 Puntos de Historia por iteración, se diseñó un plan de entregas estructurado en cinco (5) iteraciones ágiles de dos semanas de duración cada una (diez semanas en total), asegurando versiones funcionales evaluables desde la primera etapa. En la Tabla 6 se detalla el cronograma de iteraciones.

**Tabla 6**  
*Plan Detallado de las Cinco Iteraciones de Extreme Programming*

| Iteración | Enfoque y Entregables Principales | HUs Asignadas | Esfuerzo (PH) | Duración |
|:---:|---|:---:|:---:|:---:|
| Iteración 1 | Cimientos de Seguridad, Arquitectura y Catálogos Maestros (RBAC, Red Sanitaria, Catálogo de Vacunas e Insumos). | HU-01, HU-02, HU-03 | 11 PH | 2 semanas |
| Iteración 2 | Gestión de Inventarios de Entrada y Línea Base de Metas (Lotes FEFO, Caducidad y Planificación Anualizada). | HU-04, HU-05 | 9 PH | 2 semanas |
| Iteración 3 | Núcleo Transaccional Contable y Despacho Oficial (Movimientos mensuales, Sincronización M+1, Vales PECOSA y Jeringas). | HU-06, HU-07, HU-08, HU-09, HU-10, HU-11 | 33 PH | 2 semanas |
| Iteración 4 | Trazabilidad Documental y Pistas de Auditoría (Motor de Exportación PDF/Excel y Kardex Digital Físico-Valorado). | HU-12, HU-13 | 10 PH | 2 semanas |
| Iteración 5 | Inteligencia Logística, Alertas y Cuadro de Mando (Alertas Tempranas con Cooldown, Módulo ICI-DEMID y Dashboard TAM). | HU-14, HU-15 | 8 PH | 2 semanas |

*Nota.* Cronograma de desarrollo validado con el personal de inmunizaciones para permitir pruebas de campo intermedias al cierre de cada iteración.

### 3.3.1.7. Diagrama de Casos de Uso General del Sistema

El comportamiento funcional del sistema y las fronteras de interacción con los actores institucionales se sintetizan en el diagrama de casos de uso UML. El sistema articula dieciséis casos de uso (CU-01 a CU-16) distribuidos en los paquetes funcionales de Seguridad, Gestión Territorial, Planificación, Inventario, Movimientos Transaccionales, Vales de Despacho y Reportes Analíticos. En la Figura 2 se exhibe el modelado visual de casos de uso.

**Figura 2**  
*Diagrama de Casos de Uso del Sistema SIVAC*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_02.png]
```

*Nota.* Diagrama de casos de uso estructurado bajo notación UML 2.5 que delimita los permisos de interacción de los tres perfiles sanitarios y el administrador del sistema sobre los dieciséis procesos operativos de SIVAC.

---

## 3.3.2. Fase II: Diseño Simple y Modelado del Software

La fase de diseño en Extreme Programming se rige por el principio del *diseño simple*, el cual estipula que el sistema debe contener únicamente los elementos arquitecturales y estructurales indispensables para satisfacer las historias de usuario de la iteración en curso, erradicando complejidades innecesarias o anticipaciones especulativas. Para SIVAC, el diseño integró una arquitectura desacoplada en capas con API RESTful, diagramas de actividades para flujos paralelos complejos, diagramas de secuencia para procesos transaccionales y el modelado relacional en tercera forma normal (3FN) en PostgreSQL.

### 3.3.2.1. Arquitectura Lógica en Capas y Subsistemas del Sistema

La arquitectura de SIVAC se concibió bajo un patrón desacoplado en capas lógicas intercomunicadas mediante una Interfaz de Programación de Aplicaciones basada en el estilo arquitectural RESTful (De la Torre et al., 2010; Ruiz Barea, 2023). Este enfoque garantiza la independencia total entre la interfaz de usuario en el cliente y los servicios de dominio del servidor.

En la Figura 3 se ilustra la arquitectura de subsistemas del sistema, organizada en tres bloques cardinales: el cliente Single Page Application (SPA), el servidor de aplicaciones Express REST API y la capa de datos y archivos en PostgreSQL y almacenamiento persistente.

**Figura 3**  
*Arquitectura Lógica en Capas y Subsistemas del Sistema SIVAC*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_03.png]
```

*Nota.* Diagrama de subsistemas que evidencia el desacoplamiento entre el cliente enriquecido en React 18, la pasarela de servicios API en Node.js/Express y los motores de persistencia en PostgreSQL 16.

Profundizando en la estructura interna del software, la solución implementó una arquitectura en cuatro capas desacopladas, conforme se detalla en la Figura 4:
1. **Capa de Presentación (Frontend SPA):** Desarrollada con la librería React 18.3.1 en TypeScript y empaquetada mediante Vite 5.4. Utiliza Tailwind CSS 3.4 para un diseño visual ergonómico adaptado a pantallas de centros de salud, React Router DOM 6.20 para la navegación interna sin recargas de página, y librerías especializadas como Recharts 2.8 y Motion 12.38 para la renderización de cuadros de mando interactivos.
2. **Capa de Aplicación y Seguridad HTTP:** Construida sobre Node.js 20 LTS y el framework Express 4.18.2. Alberga los controladores RESTful, los esquemas de validación de entradas mediante bibliotecas Zod/Joi, la suite de seguridad Helmet para cabeceras HTTP, políticas de CORS restringidas a dominios institucionales y middlewares de limitación de tasa de peticiones (*Rate Limiting*).
3. **Capa de Dominio y Lógica de Negocio:** Constituida por servicios puros en TypeScript que encapsulan las reglas sanitarias de la cadena de frío: `MovimientosCalculationService`, `MovimientosWriteService`, `ValeService`, `IciDemidService`, `AlertaAutomaticaService` y `ReporteExportService`. Esta capa es independiente de la tecnología de persistencia y ejecuta las validaciones contables y los cálculos de saldos.
4. **Capa de Persistencia e Infraestructura de Datos:** Gestionada mediante el mapeador objeto-relacional Prisma ORM 5.7.1 sobre el motor relacional PostgreSQL 16 (Alpine). Implementa transacciones ACID nativas (`prisma.$transaction`), restricciones compuestas de unicidad e integridad referencial, tipos enumerados nativos e índices B-Tree optimizados para consultas de alta concurrencia.

**Figura 4**  
*Arquitectura en Cuatro Capas del Sistema SIVAC*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_04.png]
```

*Nota.* Representación arquitectural en cuatro capas (Presentación, Seguridad/API, Dominio/Negocio y Persistencia) que garantiza la cohesión funcional y el desacoplamiento tecnológico del sistema SIVAC.

### 3.3.2.2. Diagramas de Flujo y Procesos Operativos

Para formalizar la lógica procedimental de los procesos más complejos de la gestión de vacunas, se elaboraron diagramas de actividades bajo la especificación UML 2.5.

El primer proceso crítico corresponde al **Registro Mensual de Movimientos con Validación FEFO**, modelado en la Figura 5. El flujo describe la captura de saldos, la validación de cotas no negativas y la bifurcación paralela (fork/join) en tres hilos transaccionales simultáneos:
- Hilo A: Descuento atómico del inventario del centro de acopio aplicando el algoritmo FEFO sobre los lotes con vencimiento más próximo.
- Hilo B: Persistencia del registro contable mensual y ejecución de la sincronización recursiva de saldos hacia el mes subsiguiente ($M+1$).
- Hilo C: Verificación de cupos de planificación anual y disparo del algoritmo de redistribución de cuotas en caso de observarse variaciones en la entrega física.

**Figura 5**  
*Diagrama de Actividades del Proceso de Registro de Movimientos de Vacunas con Validación FEFO*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_05.png]
```

*Nota.* Diagrama de actividades UML que detalla la sincronización de inventarios, la validación FEFO/PVPS y la concurrencia en la grabación del movimiento contable de biológicos.

El segundo proceso operativo corresponde al **Módulo de Inteligencia Logística ICI-DEMID y Clasificación Semafórica MSD**, graficado en la Figura 6. Este proceso modela la ingesta de las hojas de consumo mensual remitidas por los almacenes, el cálculo del Consumo Promedio Mensualizado (CPA), la determinación del ratio de Meses de Stock Disponible ($\text{MSD} = \frac{\text{Saldo Actual}}{\text{CPA}}$) y la ramificación semafórica estandarizada por el Ministerio de Salud: condición de Substock o Crítico ($\text{MSD} < 2.0$), Normostock ($2.0 \le \text{MSD} \le 6.0$) y Sobrestock ($\text{MSD} > 6.0$).

**Figura 6**  
*Diagrama de Actividades del Módulo de Inteligencia Logística ICI-DEMID y Clasificación Semafórica MSD*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_06.png]
```

*Nota.* Diagrama de actividades que modela el flujo de cálculo del indicador logístico de Meses de Stock Disponible (MSD) y la asignación automatizada de alertas semafóricas según la directiva DIGEMID/DEMID.

### 3.3.2.3. Diagramas de Secuencia UML de Procesos Críticos

La interacción temporal y el intercambio de mensajes entre los componentes del frontend, controladores, servicios de dominio y la base de datos se documentaron mediante diagramas de secuencia UML.

En la Figura 7 se expone el diagrama de secuencia del proceso de **Autenticación Segura y Control de Acceso RBAC Multi-Acopio**. En este flujo, el cliente SPA remite las credenciales del usuario vía HTTPS al endpoint `/api/auth/login`. El controlador invoca el servicio de autenticación, el cual recupera el registro de la tabla `usuarios`, verifica el hash de la contraseña empleando Bcrypt y extrae los centros de acopio autorizados en la tabla intermedia `usuarios_centros_acopio`. El servicio genera un token criptográfico JWT firmado que es retornado a la SPA y almacenado en memoria de sesión, permitiendo que las peticiones subsiguientes viajen con la cabecera `Authorization: Bearer <token>` interceptada por el middleware de seguridad para filtrar los datos territoriales.

**Figura 7**  
*Diagrama de Secuencia UML: Autenticación Segura y Control de Acceso RBAC*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_07.png]
```

*Nota.* Diagrama de secuencia UML 2.5 que describe la validación de credenciales con Bcrypt, la emisión del token JWT y la extracción de permisos de acopio para el filtrado multi-territorial.

Asimismo, en la Tabla 7 se detalla la matriz de privilegios y permisos de control de acceso basada en roles (RBAC) que rige las operaciones sobre cada módulo del sistema.

**Tabla 7**  
*Matriz de Control de Acceso Basado en Roles (RBAC) por Módulos y Operaciones*

| Módulo del Sistema SIVAC | Operaciones Autorizadas para Administrador | Operaciones para Coordinador Regional | Operaciones para Responsable de Acopio | Operaciones para Operador de Puesto |
|---|---|---|---|---|
| Autenticación y Seguridad | Gestión total de cuentas y reseteo | Consulta de accesos institucionales | Modificación de perfil propio | Modificación de perfil propio |
| Estructura Territorial | Alta, baja y edición de redes y EESS | Consulta de red sanitaria | Consulta de establecimientos propios | Consulta de establecimiento propio |
| Catálogo de Biológicos | Parametrización de dosis y temperaturas | Parametrización y consulta | Consulta de especificaciones técnicas | Consulta de especificaciones técnicas |
| Lotes e Inventario FEFO | Auditoría de inventario global | Consulta regional de existencias | Registro de remesas y despacho FEFO | Consulta de lotes recibidos |
| Planificación Anual | Consulta de matrices anuales | Carga y aprobación de metas | Consulta de cuotas asignadas | Consulta de cuota asignada |
| Movimientos Mensuales | Auditoría de asientos contables | Consulta de movimientos regionales | Registro de movimientos y entregas | Verificación de recepción física |
| Vales de Despacho (PECOSA) | Auditoría de comprobantes | Consulta y validación de vales | Emisión y anulación justificada | Consulta de vale digital emitido |
| Kardex Físico-Valorado | Auditoría integral de libros mayores | Consulta de trazabilidad regional | Consulta y exportación de su centro | Consulta del kardex de su posta |
| Alertas e ICI-DEMID | Parametrización de umbrales | Consulta ejecutiva y semáforos | Atención y triaje de alertas locales | Visualización de alertas de su posta |

*Nota.* Esquema de seguridad institucional aplicado estrictamente mediante middlewares en cada ruta de la API REST de SIVAC.

En la Figura 8 se presenta el diagrama de secuencia del proceso de **Registro de Entregas Adicionales, Descuento FEFO y Sincronización Intermensual**. Este proceso demuestra la transaccionalidad atómica: el responsable de acopio ingresa una entrega de emergencia; el controlador abre un bloque transaccional en PostgreSQL (`$transaction`), registra la entrega en `entregas_adicionales`, descuenta la cantidad física del lote en `lotes_vacunas` según el orden de vencimiento, recalcula la entrega total del mes y propaga el saldo resultante como saldo anterior del mes $M+1$. Cualquier inconsistencia durante la ejecución produce una reversión completa (*rollback*), impidiendo desfases en la contabilidad.

**Figura 8**  
*Diagrama de Secuencia UML: Registro de Entregas Adicionales, Descuento FEFO y Sincronización Intermensual*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_08.png]
```

*Nota.* Diagrama de secuencia UML que modela la atomicidad transaccional durante el registro de despachos adicionales, el descuento de stock bajo algoritmo FEFO y la propagación de saldos a meses futuros.

### 3.3.2.4. Modelado Conceptual, Lógico y Físico de la Base de Datos

El diseño de la base de datos se desarrolló bajo el estándar relacional en tercera forma normal (3FN), asegurando la erradicación de redundancias y garantizando la consistencia referencial mediante claves foráneas e índices compuestos.

En la Figura 9 se exhibe el **Modelo Entidad-Relación Conceptual por Dominios de SIVAC**, estructurado en tres grandes áreas de gestión:
1. *Dominio Organizacional y de Seguridad:* Entidades `redes`, `microredes`, `centros_acopio`, `establecimientos`, `usuarios` y `usuarios_centros_acopio`.
2. *Dominio de Catálogos y Trazabilidad:* Entidades `vacunas`, `jeringas`, `configuracion_jeringa_vacuna`, `lotes_vacunas` y `lotes_jeringas`.
3. *Dominio Operativo y Transaccional:* Entidades `planificacion_anual`, `programacion_mensual`, `movimientos_vacunas`, `entregas_adicionales`, `vales_entrega`, `vales_detalle`, `kardex`, `ici_demid_registros` y `alertas`.

**Figura 9**  
*Modelo Entidad-Relación Conceptual por Dominios de SIVAC*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_09.png]
```

*Nota.* Modelo conceptual estructurado por dominios de negocio que refleja las dependencias funcionales entre la red territorial de salud, los catálogos normados de biológicos y los módulos de registro mensual.

En la Figura 10 se presenta el **Esquema Relacional Lógico de Entidades Principales en PostgreSQL / Prisma ORM**, mostrando la definición de llaves primarias basadas en identificadores únicos universales (UUID v4), restricciones foráneas y cardinalidades de uno a muchos (1:N) que preservan la integridad de la información institucional.

**Figura 10**  
*Esquema Relacional Lógico de Entidades Principales en PostgreSQL / Prisma ORM*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_10.png]
```

*Nota.* Esquema relacional lógico que detalla las veintidós tablas normalizadas, sus claves compuestas e índices optimizados definidos en el archivo `schema.prisma`.

En la Figura 11 se visualiza el **Diccionario Físico de Base de Datos y Relaciones Relacionales en PostgreSQL 16**, generado a partir de la inspección directa del motor de base de datos en producción.

**Figura 11**  
*Diccionario Físico de Base de Datos y Relaciones Relacionales en PostgreSQL 16*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_11.png]
```

*Nota.* Representación física de las tablas de la base de datos PostgreSQL 16 generada mediante herramientas de ingeniería inversa, evidenciando las restricciones de integridad y tipos de datos nativos.

A continuación, en las Tablas 8 a 22 se documenta de forma exhaustiva el diccionario de datos de las tablas más relevantes del esquema de la base de datos de SIVAC.

**Tabla 8**  
*Diccionario de Datos: Tabla redes*

| Nombre del Campo | Tipo de Dato | Nulabilidad | Clave | Descripción y Restricciones |
|---|---|---|---|---|
| id | UUID | NOT NULL | PK | Identificador único universal autogenerado (v4). |
| codigo | VARCHAR(20) | NOT NULL | UK | Código institucional único asignado a la Red de Salud. |
| nombre | VARCHAR(100) | NOT NULL | Ninguna | Denominación oficial de la Red (ej. Red Sondor, Red JMA). |
| descripcion | TEXT | NULL | Ninguna | Información descriptiva o geográfica complementaria. |
| estado | VARCHAR(20) | NOT NULL | Ninguna | Estado del registro (activo, inactivo). Valor por defecto: activo. |
| created_at | TIMESTAMPTZ | NOT NULL | Ninguna | Fecha y hora de creación del registro. |
| updated_at | TIMESTAMPTZ | NOT NULL | Ninguna | Fecha y hora de la última modificación del registro. |

*Nota.* Tabla maestra que representa el nivel superior de la estructura sanitaria de la DISA Apurímac II.

**Tabla 9**  
*Diccionario de Datos: Tabla microredes*

| Nombre del Campo | Tipo de Dato | Nulabilidad | Clave | Descripción y Restricciones |
|---|---|---|---|---|
| id | UUID | NOT NULL | PK | Identificador único universal autogenerado. |
| codigo | VARCHAR(20) | NOT NULL | UK | Código institucional de la microred de salud. |
| nombre | VARCHAR(100) | NOT NULL | Ninguna | Nombre oficial de la microred (ej. Microred Huancaray). |
| red_id | UUID | NOT NULL | FK | Clave foránea que referencia a la tabla `redes(id)`. |
| created_at | TIMESTAMPTZ | NOT NULL | Ninguna | Marca temporal de inserción del registro. |
| updated_at | TIMESTAMPTZ | NOT NULL | Ninguna | Marca temporal de actualización del registro. |

*Nota.* Subdivisión provincial sanitaria sujeta a la restricción única compuesta `uk_microred_nombre_red`.

**Tabla 10**  
*Diccionario de Datos: Tabla centros_acopio*

| Nombre del Campo | Tipo de Dato | Nulabilidad | Clave | Descripción y Restricciones |
|---|---|---|---|---|
| id | UUID | NOT NULL | PK | Identificador único del centro de acopio. |
| codigo | VARCHAR(20) | NULL | Ninguna | Código patrimonial o de almacén asignado por la institución. |
| nombre | VARCHAR(100) | NOT NULL | Ninguna | Nombre del almacén zonal de cadena de frío (11 centros). |
| responsable | VARCHAR(150) | NULL | Ninguna | Nombre del profesional de enfermería a cargo del almacén. |
| telefono | VARCHAR(20) | NULL | Ninguna | Número de contacto de emergencia para cadena de frío. |
| microred_id | UUID | NULL | FK | Referencia foránea opcional a la tabla `microredes(id)`. |
| created_at | TIMESTAMPTZ | NOT NULL | Ninguna | Fecha y hora de creación del registro. |
| updated_at | TIMESTAMPTZ | NOT NULL | Ninguna | Fecha y hora de modificación del registro. |

*Nota.* Almacenes zonales intermedios que custodian las cámaras frías para el despacho a postas de salud.

**Tabla 11**  
*Diccionario de Datos: Tabla establecimientos*

| Nombre del Campo | Tipo de Dato | Nulabilidad | Clave | Descripción y Restricciones |
|---|---|---|---|---|
| id | UUID | NOT NULL | PK | Identificador único del establecimiento receptor. |
| codigo_renaes | VARCHAR(20) | NOT NULL | UK | Código único oficial del Registro Nacional de IPRESS (RENIPRESS). |
| nombre | VARCHAR(150) | NOT NULL | Ninguna | Nombre formal del centro de salud, puesto o posta médica. |
| tipo | VARCHAR(50) | NOT NULL | Ninguna | Nivel de categorización (Puesto de Salud, Centro de Salud, Hospital). |
| centro_acopio_id | UUID | NOT NULL | FK | Clave foránea referenciando a `centros_acopio(id)`. |
| created_at | TIMESTAMPTZ | NOT NULL | Ninguna | Marca temporal de inserción del registro. |
| updated_at | TIMESTAMPTZ | NOT NULL | Ninguna | Marca temporal de actualización del registro. |

*Nota.* Unidades operativas del primer nivel asistencial receptoras de las remesas mensuales de biológicos.

**Tabla 12**  
*Diccionario de Datos: Tablas usuarios y usuarios_centros_acopio*

| Nombre del Campo | Tipo de Dato | Nulabilidad | Clave | Descripción y Restricciones |
|---|---|---|---|---|
| id | UUID | NOT NULL | PK | Identificador único del usuario institucional. |
| usuario | VARCHAR(50) | NOT NULL | UK | Nombre de usuario alfanumérico para autenticación. |
| email | VARCHAR(100) | NOT NULL | UK | Correo electrónico institucional verificado. |
| password | VARCHAR(255) | NOT NULL | Ninguna | Contraseña cifrada mediante hash Bcrypt (salt $\ge 10$). |
| rol | VARCHAR(30) | NOT NULL | Ninguna | Rol institucional (admin, coordinador, responsable_acopio, operador). |
| nombres | VARCHAR(100) | NOT NULL | Ninguna | Nombres de pila del servidor de salud. |
| apellidos | VARCHAR(100) | NOT NULL | Ninguna | Apellidos paterno y materno del servidor de salud. |
| estado | VARCHAR(20) | NOT NULL | Ninguna | Estado de la cuenta (activo, inactivo, bloqueado). |
| ultimo_acceso | TIMESTAMPTZ | NULL | Ninguna | Registro cronológico del último inicio de sesión exitoso. |

*Nota.* La vinculación multi-acopio se implementa mediante la tabla intermedia `usuarios_centros_acopio(usuario_id, centro_acopio_id)`.

**Tabla 13**  
*Diccionario de Datos: Tabla vacunas*

| Nombre del Campo | Tipo de Dato | Nulabilidad | Clave | Descripción y Restricciones |
|---|---|---|---|---|
| id | UUID | NOT NULL | PK | Identificador único de la vacuna. |
| codigo | VARCHAR(20) | NOT NULL | UK | Código oficial estandarizado por el MINSA. |
| nombre | VARCHAR(100) | NOT NULL | Ninguna | Denominación comercial o genérica del biológico (BCG, Pentavalente). |
| tipo | VARCHAR(50) | NOT NULL | Ninguna | Clasificación técnica (bacteriana, viral, atenuada, inactivada). |
| presentacion | VARCHAR(50) | NOT NULL | Ninguna | Presentación física del envase (frasco monodosis, frasco multidosis). |
| dosis_por_frasco | INT | NOT NULL | Ninguna | Número entero de dosis contenidas por envase (1, 10, 20). |
| temperatura_min | DECIMAL(4,2) | NOT NULL | Ninguna | Cota mínima de conservación térmica (+2.00 °C). |
| temperatura_max | DECIMAL(4,2) | NOT NULL | Ninguna | Cota máxima de conservación térmica (+8.00 °C). |
| tiempo_vida_util | INT | NOT NULL | Ninguna | Vida útil del frasco abierto en horas o días según norma. |

*Nota.* Catálogo maestro normado según la NTS N° 196-MINSA/DGIESP-2022 del Esquema Regular de Vacunación.

**Tabla 14**  
*Diccionario de Datos: Tablas jeringas y configuracion_jeringa_vacuna*

| Nombre del Campo | Tipo de Dato | Nulabilidad | Clave | Descripción y Restricciones |
|---|---|---|---|---|
| id | UUID | NOT NULL | PK | Identificador único de la jeringa o insumo. |
| codigo | VARCHAR(20) | NOT NULL | UK | Código institucional de inventario del insumo descartable. |
| descripcion | VARCHAR(100) | NOT NULL | Ninguna | Detalle técnico (ej. Jeringa 1cc con aguja 27G x 1/2" autodescartable). |
| capacidad | VARCHAR(20) | NOT NULL | Ninguna | Volumen nominal (0.1 ml, 0.5 ml, 1 ml, 3 ml, 5 ml). |
| calibre_aguja | VARCHAR(20) | NOT NULL | Ninguna | Calibre y longitud de la aguja (27G x 1/2", 25G x 5/8", 23G x 1"). |
| tipo_uso | VARCHAR(30) | NOT NULL | Ninguna | Función de la jeringa (aplicacion, dilucion). |

*Nota.* La regla de correspondencia se normaliza en `configuracion_jeringa_vacuna(vacuna_id, jeringa_id, factor_multiplicador, centro_acopio_id)`.

**Tabla 15**  
*Diccionario de Datos: Tabla lotes_vacunas*

| Nombre del Campo | Tipo de Dato | Nulabilidad | Clave | Descripción y Restricciones |
|---|---|---|---|---|
| id | UUID | NOT NULL | PK | Identificador único del lote recibido. |
| numero | VARCHAR(50) | NOT NULL | Ninguna | Código alfanumérico del lote asignado por el fabricante. |
| vacuna_id | UUID | NOT NULL | FK | Clave foránea que referencia a la tabla `vacunas(id)`. |
| centro_acopio_id | UUID | NOT NULL | FK | Clave foránea que referencia al almacén receptor. |
| fecha_vencimiento | TIMESTAMPTZ | NOT NULL | Ninguna | Fecha límite de caducidad física del biológico. |
| cantidad_inicial | INT | NOT NULL | Ninguna | Unidades de dosis recibidas en la remesa original. |
| cantidad_actual | INT | NOT NULL | Ninguna | Saldo disponible en cámara fría sujeto a descuento FEFO. |
| comprobante_ingreso| VARCHAR(100) | NULL | Ninguna | Número de PECOSA central de CENARES o Guía de Remisión. |
| estado | VARCHAR(20) | NOT NULL | Ninguna | Estado del lote (activo, agotado, vencido, cuarentena). |

*Nota.* Entidad fundamental para la ejecución de la directiva de despacho prioritario First Expired, First Out.

**Tabla 16**  
*Diccionario de Datos: Tabla planificacion_anual*

| Nombre del Campo | Tipo de Dato | Nulabilidad | Clave | Descripción y Restricciones |
|---|---|---|---|---|
| id | UUID | NOT NULL | PK | Identificador único del registro de planificación. |
| establecimiento_id| UUID | NOT NULL | FK | Establecimiento sanitario asignatario de la meta. |
| vacuna_id | UUID | NOT NULL | FK | Biológico objeto de la programación. |
| anio | INT | NOT NULL | Ninguna | Año fiscal y presupuestal correspondiente (ej. 2026). |
| meta_anual | INT | NOT NULL | Ninguna | Cantidad entera consolidada de dosis programadas. |
| estado | VARCHAR(20) | NOT NULL | Ninguna | Estado del plan (borrador, aprobado, bloqueado). |

*Nota.* Protegida por la restricción de unicidad compuesta `uk_planificacion_establecimiento_vacuna_anio`.

**Tabla 17**  
*Diccionario de Datos: Tabla movimientos_vacunas*

| Nombre del Campo | Tipo de Dato | Nulabilidad | Clave | Descripción y Restricciones |
|---|---|---|---|---|
| id | UUID | NOT NULL | PK | Identificador único universal del movimiento mensual. |
| establecimiento_id| UUID | NOT NULL | FK | Clave foránea referenciando a `establecimientos(id)`. |
| vacuna_id | UUID | NOT NULL | FK | Clave foránea referenciando a `vacunas(id)`. |
| mes | INT | NOT NULL | Ninguna | Periodo mensual contable (rango entero de 1 a 12). |
| anio | INT | NOT NULL | Ninguna | Ejercicio anual contable. |
| saldo_anterior | INT | NOT NULL | Ninguna | Saldo inicial trasladado del mes previo ($M-1$). |
| trans_ingreso | INT | NOT NULL | Ninguna | Dosis ingresadas mediante transferencias inter-establecimientos. |
| salida | INT | NOT NULL | Ninguna | Dosis administradas o aplicadas en personas. |
| trans_salida | INT | NOT NULL | Ninguna | Dosis transferidas hacia otros centros o almacenes. |
| entrega | INT | NOT NULL | Ninguna | Entrega física total consolidada del mes. |
| entrega_base | INT | NOT NULL | Ninguna | Cuota programada regular correspondiente al periodo. |

*Nota.* Tabla central transaccional con restricción de unicidad `uk_movimiento_establecimiento_vacuna_mes_anio`.

**Tabla 18**  
*Diccionario de Datos: Tabla entregas_adicionales*

| Nombre del Campo | Tipo de Dato | Nulabilidad | Clave | Descripción y Restricciones |
|---|---|---|---|---|
| id | UUID | NOT NULL | PK | Identificador de la entrega extraordinaria. |
| movimiento_id | UUID | NOT NULL | FK | Clave foránea vinculada al movimiento mensual principal. |
| numero_entrega | INT | NOT NULL | Ninguna | Número correlativo del despacho (restringido de 1 a 5). |
| cantidad | INT | NOT NULL | Ninguna | Unidades de dosis adicionales suministradas. |
| justificacion | TEXT | NOT NULL | Ninguna | Motivo sanitario justificado (barrido, brote, contingencia). |
| lote_id | UUID | NULL | FK | Referencia al lote de biológico utilizado para el despacho. |
| created_at | TIMESTAMPTZ | NOT NULL | Ninguna | Fecha y hora en que se registró la entrega extraordinaria. |

*Nota.* Registros complementarios para contingencias sin alterar la cuota de entrega regular.

**Tabla 19**  
*Diccionario de Datos: Tablas vales_entrega y vales_detalle*

| Nombre del Campo | Tipo de Dato | Nulabilidad | Clave | Descripción y Restricciones |
|---|---|---|---|---|
| id | UUID | NOT NULL | PK | Identificador único del vale de despacho. |
| numero | VARCHAR(50) | NOT NULL | UK | Correlativo oficial único del comprobante (VALE-AAAA-NNNN). |
| centro_acopio_id | UUID | NOT NULL | FK | Centro de acopio emisor del comprobante de despacho. |
| mes | INT | NOT NULL | Ninguna | Mes operativo de la entrega. |
| anio | INT | NOT NULL | Ninguna | Año operativo de la entrega. |
| estado | VARCHAR(20) | NOT NULL | Ninguna | Estado del comprobante (generado, impreso, anulado). |
| tipo_vale | VARCHAR(30) | NOT NULL | Ninguna | Alcance de la entrega (completo, solo_base, solo_adicionales). |
| total_vacunas | INT | NOT NULL | Ninguna | Sumatoria total de dosis de biológicos despachadas. |
| total_insumos | INT | NOT NULL | Ninguna | Sumatoria total de jeringas y diluyentes acompañantes. |
| usuario_id | UUID | NOT NULL | FK | Servidor responsable que generó y firmó digitalmente el vale. |

*Nota.* El desglose por posta y lote se almacena en la tabla dependiente `vales_detalle(vale_id, establecimiento_id, vacuna_id, lote_id, cantidad)`.

**Tabla 20**  
*Diccionario de Datos: Tabla kardex*

| Nombre del Campo | Tipo de Dato | Nulabilidad | Clave | Descripción y Restricciones |
|---|---|---|---|---|
| id | UUID | NOT NULL | PK | Identificador único del asiento contable de kardex. |
| centro_acopio_id | UUID | NOT NULL | FK | Almacén de cadena de frío en el que ocurre el movimiento. |
| vacuna_id | UUID | NOT NULL | FK | Biológico objeto de la transacción de almacén. |
| lote_id | UUID | NOT NULL | FK | Lote específico sobre el cual se altera el inventario. |
| tipo_transaccion | VARCHAR(30) | NOT NULL | Ninguna | Naturaleza de la operación (ingreso, salida, transferencia, ajuste). |
| documento_respaldo| VARCHAR(100) | NOT NULL | Ninguna | Número de comprobante legal que respalda el movimiento. |
| saldo_anterior | INT | NOT NULL | Ninguna | Cantidad física previa a la ejecución de la transacción. |
| cantidad | INT | NOT NULL | Ninguna | Volumen de unidades que ingresan o salen del almacén. |
| saldo_actual | INT | NOT NULL | Ninguna | Balance resultante tras la operación en el libro mayor. |
| created_at | TIMESTAMPTZ | NOT NULL | Ninguna | Marca temporal inmutable del asiento contable. |

*Nota.* Pista de auditoría inmutable que respalda las inspecciones técnicas de la DEMID y órganos de control.

**Tabla 21**  
*Diccionario de Datos: Tabla ici_demid_registros*

| Nombre del Campo | Tipo de Dato | Nulabilidad | Clave | Descripción y Restricciones |
|---|---|---|---|---|
| id | UUID | NOT NULL | PK | Identificador único del reporte logístico DEMID. |
| centro_acopio_id | UUID | NOT NULL | FK | Centro de acopio al cual corresponde la evaluación. |
| vacuna_id | UUID | NOT NULL | FK | Biológico evaluado en el informe de consumo. |
| mes | INT | NOT NULL | Ninguna | Mes evaluado en el ciclo logístico. |
| anio | INT | NOT NULL | Ninguna | Año de la evaluación logística. |
| consumo_promedio | DECIMAL(10,2)| NOT NULL | Ninguna | Consumo Promedio Mensualizado (CPA) anual calculado. |
| saldo_actual | INT | NOT NULL | Ninguna | Stock total presente en las cámaras de frío al cierre. |
| meses_disponibles | DECIMAL(5,2) | NULL | Ninguna | Ratio de Meses de Stock Disponible ($\text{MSD} = \frac{\text{Saldo}}{\text{CPA}}$). |
| estado_stock | VARCHAR(30) | NOT NULL | Ninguna | Categorización semafórica (SUBSTOCK, NORMOSTOCK, SOBRESTOCK). |

*Nota.* Registros especializados para el monitoreo de disponibilidad según directivas de la DIGEMID.

**Tabla 22**  
*Diccionario de Datos: Tabla alertas*

| Nombre del Campo | Tipo de Dato | Nulabilidad | Clave | Descripción y Restricciones |
|---|---|---|---|---|
| id | UUID | NOT NULL | PK | Identificador único de la notificación de alerta. |
| tipo | VARCHAR(50) | NOT NULL | Ninguna | Categoría de la incidencia (vencimiento, quiebre_stock, desvio_termico). |
| severidad | VARCHAR(20) | NOT NULL | Ninguna | Nivel de criticidad operativa (informativa, advertencia, critica). |
| mensaje | TEXT | NOT NULL | Ninguna | Texto descriptivo de la incidencia para el operador sanitario. |
| centro_acopio_id | UUID | NULL | FK | Almacén zonal afectado por la condición de riesgo. |
| lote_id | UUID | NULL | FK | Lote biológico involucrado en la alerta preventiva. |
| parametros | JSONB | NULL | Ninguna | Metadatos en formato JSON para control de cooldown y auditoría. |
| leida | BOOLEAN | NOT NULL | Ninguna | Bandera booleana de estado de lectura (true o false). |
| created_at | TIMESTAMPTZ | NOT NULL | Ninguna | Fecha y hora exacta de emisión de la alerta por el sistema. |

*Nota.* Sistema reactivo de notificación gestionado con ventana de enfriamiento (*cooldown*) de 7 días.

---

## 3.3.3. Fase III: Codificación y Prácticas de Ingeniería Ágil

La fase de codificación en Extreme Programming se desarrolló bajo estándares técnicos rigurosos, adoptando la programación en parejas (*Pair Programming*), el desarrollo guiado por pruebas (*Test-Driven Development - TDD*), la propiedad colectiva del código y la refactorización continua (*Continuous Refactoring*) para mantener el sistema libre de deuda técnica (Beck, 1999; Sommerville, 2016).

### 3.3.3.1. Estructura del Proyecto y Stack Tecnológico

El ecosistema tecnológico de SIVAC se seleccionó priorizando el rendimiento, la robustez tipográfica y la compatibilidad con el entorno de servidores institucionales. En la Tabla 23 se sintetiza el stack de desarrollo.

**Tabla 23**  
*Stack Tecnológico de Desarrollo y Librerías del Ecosistema SIVAC*

| Capa Tecnológica | Tecnología / Biblioteca | Versión | Rol Funcional en el Sistema Web |
|---|---|---|---|
| Entorno de Ejecución Backend | Node.js | 20 LTS | Plataforma de ejecución del servidor asíncrono y no bloqueante. |
| Framework de API Web | Express | 4.18.2 | Enrutamiento RESTful, gestión de peticiones HTTP y middlewares. |
| Lenguaje de Programación | TypeScript | 5.3 / 5.5 | Tipado estricto estático tanto en servidor como en cliente. |
| Mapeo Objeto-Relacional | Prisma ORM | 5.7.1 | Acceso tipado a datos, migraciones automatizadas y transacciones ACID. |
| Motor de Base de Datos | PostgreSQL | 16 (Alpine) | Almacenamiento relacional, integridad referencial y procedimientos JSONB. |
| Biblioteca de Interfaz Cliente | React | 18.3.1 | Construcción de interfaces reactivas mediante Single Page Application. |
| Herramienta de Construcción SPA| Vite | 5.4.0 | Compilador y empaquetador ultrarrápido para desarrollo y producción. |
| Framework de Estilos CSS | Tailwind CSS | 3.4.0 | Sistema de diseño utilitario para interfaces médicas y de almacén. |
| Seguridad Criptográfica | Bcrypt / JWT | 5.1 / 9.0 | Hashing seguro de contraseñas y tokens criptográficos de sesión. |
| Generación de Documentos | PDFKit / ExcelJS | 0.14 / 4.4 | Motores de renderizado nativo para vales PECOSA y reportes contables. |
| Visualización de Gráficos | Recharts | 2.8.0 | Cuadros de mando y gráficos analíticos de cobertura de vacunación. |
| Framework de Pruebas | Jest / Supertest | 29.7 / 6.3 | Ejecución automatizada de pruebas unitarias y de integración. |

*Nota.* Ecosistema tecnológico auditado directamente en el repositorio fuente `C:\Proyectos\syncova`.

La organización modular del backend se estructuró siguiendo los principios de arquitectura limpia. En la Figura 12 se exhibe el árbol de directorios del proyecto backend en Node.js, Express y Prisma ORM.

**Figura 12**  
*Estructura del Proyecto Backend en Node.js, Express y Prisma ORM*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_12.png]
```

*Nota.* Vista de la estructura del proyecto backend evidenciando la segregación de controladores, middlewares, servicios de negocio puros y suites de pruebas en TypeScript.

Por su parte, la arquitectura del cliente web SPA se modeló mediante componentes reutilizables y contextos de estado global. En la Figura 13 se muestra el árbol de directorios del frontend en React 18, TypeScript y Vite.

**Figura 13**  
*Estructura Modular del Cliente Web SPA en React 18, TypeScript y Vite*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_13.png]
```

*Nota.* Arquitectura modular del frontend con separación de componentes funcionales (Movimientos, Inventario, Vales, Alertas) y contextos de autenticación.

### 3.3.3.2. Implementación de Algoritmos Críticos de Negocio

La inspección del código fuente auditado en `C:\Proyectos\syncova\backend\src\services\` certifica la implementación de algoritmos especializados que resuelven los problemas operativos de la DISA Apurímac II.

El primer algoritmo esencial corresponde a la **Sincronización Recursiva de Saldos Intermensuales en Cascada**, implementado en el servicio `MovimientosCalculationService.ts`. La ecuación contable formalizada en el sistema es la siguiente:
$$\text{Stock Calculado} = (\text{Saldo Anterior} + \text{Trans. Ingreso}) - \text{Salida} - \text{Trans. Salida} + \text{Entrega Total}$$

En la Figura 14 se presenta el código fuente real del servicio, donde el método `calcularEntregaTotal()` suma la entrega base con las entregas adicionales registradas, y el método `sincronizarSaldoAnteriorSiguienteMes()` traslada atómicamente el saldo calculado hacia el mes siguiente ($M+1$) en la base de datos PostgreSQL, garantizando la eliminación absoluta de desfases por transcripción manual.

**Figura 14**  
*Implementación del Algoritmo de Sincronización Recursiva de Saldos Intermensuales en TypeScript*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_14.png]
```

*Nota.* Fragmento de código fuente de `MovimientosCalculationService.ts` que implementa la synchronización recursiva de balances contables entre periodos mensuales consecutivos.

El segundo algoritmo relevante es el **Servicio de Detección Proactiva de Alertas Tempranas con Ventana de Cooldown de 7 Días**, codificado en `AlertaAutomaticaService.ts` y documentado en la Figura 15. Este componente evalúa periódicamente los inventarios de biológicos activos, computa los días restantes hasta la fecha de caducidad y, en caso de constatar un vencimiento inminente ($\le 60$ días), verifica si ya existe una alerta activa para el lote dentro de la ventana de enfriamiento (*cooldown*) de 7 días. De este modo, se garantiza la notificación oportuna a los encargados del almacén sin generar saturación innecesaria en la bandeja de avisos.

**Figura 15**  
*Servicio de Detección Proactiva de Alertas Tempranas con Ventana de Cooldown de 7 Días*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_15.png]
```

*Nota.* Implementación de la lógica preventiva de caducidad de lotes biológicos con control de duplicidad por ventana temporal en TypeScript.

El tercer componente crítico es el **Middleware de Autenticación, Verificación Criptográfica JWT y Extracción de Permisos RBAC Multi-Acopio**, codificado en `backend/src/middleware/auth.ts`. Tal como se ilustra en la Figura 16, este middleware intercepta cada petición HTTP entrante, extrae el token portador (*Bearer Token*), valida la firma criptográfica contra la clave secreta institucional y recupera los identificadores de centros de acopio autorizados para el usuario, inyectándolos en el objeto de contexto `req.user` para aislar las consultas en la base de datos.

**Figura 16**  
*Middleware de Autenticación, Verificación Criptográfica JWT y Extracción de Permisos RBAC Multi-Acopio*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_16.png]
```

*Nota.* Código fuente del middleware de seguridad en Express que implementa la verificación de tokens JSON Web Tokens y el control de alcance territorial para los usuarios sanitarios.

El cuarto algoritmo sustancial corresponde al **Cálculo de Indicadores de Disponibilidad Logística MSD y Semáforo Normativo**, implementado en `IciDemidService.ts`. En la Figura 17 se exhibe el método `calcularIndicadoresDisponibilidad()`, el cual computa el Consumo Promedio Mensualizado (CPA) a partir de la distribución anual y clasifica la disponibilidad en los estados normados `SIN_CONSUMO`, `SUBSTOCK`, `NORMOSTOCK` y `SOBRESTOCK`.

**Figura 17**  
*Algoritmo de Cálculo de Indicadores de Disponibilidad Logística MSD y Semáforo Normativo*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_17.png]
```

*Nota.* Implementación en TypeScript del cálculo matemático de Meses de Stock Disponible y la categorización de alertas según estándares del MINSA.

Adicionalmente, se codificaron en el sistema los siguientes algoritmos de negocio:
- *Algoritmo de Redistribución Automática de Cuotas Programadas (`MovimientosCalculationService.ts`):* Cuando la entrega de un mes varía en $\Delta = \text{Nueva Entrega} - \text{Entrega Anterior}$, el método ajusta ordenadamente las cuotas de los meses restantes del año fiscal para preservar la meta anual programada ante el CENARES, bloqueando variaciones que superen $\pm 10,000$ unidades.
- *Algoritmo de Emparejamiento de Jeringas e Insumos (`ConfiguracionJeringaVacunaService.ts`):* Consulta las tablas maestras de correspondencia y asocia automáticamente el número y modelo normado de jeringas de aplicación y dilución requeridas por cada frasco de vacuna suministrado (ej. BCG 10 dosis con 10 jeringas autodescartables de 1cc y 1 jeringa de dilución de 5cc).
- *Motor Documental de Exportación Oficial (`ValeExportService.ts`):* Orquesta la compilación en tiempo real de archivos PDF y Excel (.xlsx) estructurados con el membrete oficial del Gobierno Regional de Apurímac, tablas de desglose y casilleros de conformidad.

### 3.3.3.3. Interfaces Gráficas de Usuario Desarrolladas (UI)

Las interfaces gráficas de SIVAC se desarrollaron priorizando la usabilidad operativa, la legibilidad en condiciones de baja iluminación de almacén y la velocidad de captura de datos mediante el teclado. A continuación, se detallan las pantallas oficiales capturadas en el entorno funcional del sistema.

La **Pantalla de Autenticación e Inicio de Sesión de SIVAC** se presenta en la Figura 18. Esta vista proporciona un formulario minimalista y seguro que captura las credenciales del servidor de salud, ofreciendo validación reactiva de formato y prevención visual de ataques de fuerza bruta.

**Figura 18**  
*Interfaz de Usuario: Pantalla de Autenticación e Inicio de Sesión de SIVAC*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_18.png]
```

*Nota.* Formulario de acceso al sistema SIVAC con soporte para credenciales institucionales y generación de sesiones seguras mediante tokens JWT.

El **Dashboard Principal de Monitoreo PAI, Curvas de Tendencia y Cadena de Frío** se exhibe en la Figura 19. La pantalla centraliza tarjetas de resumen ejecutivo con el total de centros de acopio activos, lotes vigentes en cámaras frigoríficas, vales emitidos en el ejercicio y gráficos de avance mensual renderizados con Recharts.

**Figura 19**  
*Interfaz de Usuario: Dashboard Principal de Monitoreo PAI, Curvas de Tendencia y Cadena de Frío*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_19.png]
```

*Nota.* Panel ejecutivo de monitoreo que ilustra las curvas de avance de distribución de vacunas, distribución geográfica y métricas clave de la cadena de frío.

En la Figura 20 se observa el **Panel Inferior del Dashboard con Centros de Acopio Zonales, Alertas y Bitácora**, donde se despliega la lista de los once almacenes zonales con sus indicadores semafóricos de estado de inventario y el resumen de últimas transacciones.

**Figura 20**  
*Interfaz de Usuario: Panel Inferior del Dashboard con Centros de Acopio Zonales, Alertas y Bitácora*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_20.png]
```

*Nota.* Sección complementaria del tablero principal que lista los almacenes de cadena de frío y el registro cronológico de eventos operacionales.

El **Módulo de Inventario y Control de Lotes de Biológicos con Trazabilidad FEFO** se expone en la Figura 21. La interfaz permite consultar el stock actual por producto biológico, dosis disponibles y ordenamiento automático de lotes según su fecha de vencimiento.

**Figura 21**  
*Interfaz de Usuario: Módulo de Inventario y Control de Lotes de Biológicos con Trazabilidad FEFO*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_21.png]
```

*Nota.* Módulo de inventario del almacén zonal con trazabilidad de lotes físicos y ordenamiento prioritario bajo el estándar First Expired, First Out.

En la Figura 22 se ilustra la **Vista de Gestión de Lotes y Filtros Dinámicos por Estado y Caducidad**, que permite al responsable del almacén filtrar por rango de fechas, estado de conservación y tipo de biológico, visualizando insignias de color que alertan sobre lotes críticos.

**Figura 22**  
*Interfaz de Usuario: Vista de Gestión de Lotes y Filtros Dinámicos por Estado y Caducidad*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_22.png]
```

*Nota.* Cuadrícula de administración de lotes que facilita la búsqueda de biológicos según su vigencia temporal y estado de disponibilidad en cámara fría.

La **Matriz Contable de Movimientos Mensuales de Vacunas por Establecimiento** se muestra en la Figura 23. Esta interfaz digitaliza los libros tradicionales de kardex mediante una cuadrícula interactiva que lista los establecimientos del centro de acopio seleccionado y muestra los balances de apertura, ingresos, salidas y saldos finales.

**Figura 23**  
*Interfaz de Usuario: Matriz Contable de Movimientos Mensuales de Vacunas por Establecimiento*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_23.png]
```

*Nota.* Matriz interactiva de movimientos mensuales de biológicos para el conjunto de establecimientos de salud adscritos a un centro de acopio.

En la Figura 24 se presenta el **Registro y Cuadrícula Operativa de Movimientos con Entregas Base y Adicionales**, permitiendo el ingreso rápido de cantidades con navegación por tabulador y confirmación inmediata de saldos recalculados en pantalla.

**Figura 24**  
*Interfaz de Usuario: Registro y Cuadrícula Operativa de Movimientos con Entregas Base y Adicionales*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_24.png]
```

*Nota.* Formulario en cuadrícula para la captura de movimientos mensuales con soporte para entregas regulares y extraordinarias por establecimiento.

El **Módulo de Planificación Anual de Metas PAI y Programación Mensual Ene-Dic** se expone en la Figura 25. Permite a la Coordinación Regional cargar y autorizar la distribución mensualizada de metas para cada centro y puesto de salud, validando la cuadratura matemática del año fiscal.

**Figura 25**  
*Interfaz de Usuario: Módulo de Planificación Anual de Metas PAI y Programación Mensual Ene-Dic*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_25.png]
```

*Nota.* Interfaz para la configuración y parametrización de las metas de vacunación del Esquema Regular distribuidas en las doce mensualidades del ejercicio.

En la Figura 26 se visualiza el **Centro de Reportes y Matriz Trimestral de Seguimiento CENARES Q1-Q4**, diseñado para contrastar las entregas efectivas frente a las remesas trimestrales programadas por el nivel central.

**Figura 26**  
*Interfaz de Usuario: Centro de Reportes y Matriz Trimestral de Seguimiento CENARES Q1-Q4*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_26.png]
```

*Nota.* Matriz analítica para el seguimiento de entregas trimestrales y evaluación del cumplimiento de compromisos de gestión sanitaria.

El **Módulo de Inteligencia Logística ICI-DEMID con Semáforo de Disponibilidad MSD** se presenta en la Figura 27. Esta pantalla despliega el cálculo de Meses de Stock Disponible para cada producto biológico, clasificando visualmente las existencias en verde (Normostock), rojo (Substock) o azul (Sobrestock).

**Figura 27**  
*Interfaz de Usuario: Módulo de Inteligencia Logística ICI-DEMID con Semáforo de Disponibilidad MSD*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_27.png]
```

*Nota.* Vista de inteligencia logística según el estándar del Informe de Consumo Integrado (ICI-DEMID) con clasificación semafórica de disponibilidad.

En la Figura 28 se ilustra el **Módulo de Kardex Digital Cronológico de Movimientos por Lote y Almacén**, el cual proporciona la bitácora inmutable de auditoría para cada transacción de entrada, salida, ajuste o transferencia.

**Figura 28**  
*Interfaz de Usuario: Módulo de Kardex Digital Cronológico de Movimientos por Lote y Almacén*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_28.png]
```

*Nota.* Pantalla de consulta cronológica de transacciones de almacén con registro de comprobantes sustentatorios y saldos resultantes.

La **Vista Detallada del Kardex con Múltiples Operaciones** se exhibe en la Figura 29, mostrando el desglose histórico de asientos contables respaldados por órdenes de despacho y comprobantes de remesa.

**Figura 29**  
*Interfaz de Usuario: Vista Detallada del Kardex con Múltiples Operaciones (Ingreso, Salida y Transferencia)*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_29.png]
```

*Nota.* Vista analítica del kardex que detalla las operaciones de ingreso, salida ordinaria y transferencias inter-institucionales de biológicos.

El **Módulo de Administración de Usuarios y Asignación de Roles RBAC** se muestra en la Figura 30. Esta interfaz permite al Administrador General crear cuentas institucionales, asignar contraseñas seguras, delimitar roles y vincular a los usuarios con sus centros de acopio correspondientes.

**Figura 30**  
*Interfaz de Usuario: Módulo de Administración de Usuarios y Asignación de Roles RBAC*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_30.png]
```

*Nota.* Panel de administración de cuentas de usuario del sistema SIVAC y asignación de permisos de acceso basados en roles.

En la Figura 31 se muestra la **Gestión de Usuarios mostrando Fixture de Prueba Automatizada**, ilustrando la verificación de cuentas y la respuesta de las interfaces ante datos de validación controlados.

**Figura 31**  
*Interfaz de Usuario: Gestión de Usuarios mostrando Fixture de Prueba Automatizada*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_31.png]
```

*Nota.* Interfaz de gestión de usuarios durante la ejecución de pruebas automatizadas de creación y asignación de privilegios de acceso.

El **Centro de Alertas Tempranas y Triaje Operativo con Severidades** se expone en la Figura 32. La vista reúne las notificaciones generadas por el servicio automático, organizándolas por severidad (Crítica, Advertencia e Informativa) con botones para gestionar el descarte justificado o la acción correctiva.

**Figura 32**  
*Interfaz de Usuario: Centro de Alertas Tempranas y Triaje Operativo con Severidades*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_32.png]
```

*Nota.* Bandeja de triaje operativo de alertas tempranas con identificación visual de severidades y gestión de acciones preventivas para evitar caducidades.

Finalmente, en la Figura 33 se presenta el **Módulo de Asignación y Reglas Normativas de Jeringas e Insumos por Vacuna**, donde se configuran los factores multiplicadores y los tipos de jeringas que deben acompañar a cada biológico despachado.

**Figura 33**  
*Interfaz de Usuario: Módulo de Asignación y Reglas Normativas de Jeringas e Insumos por Vacuna*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_33.png]
```

*Nota.* Panel de configuración de reglas normativas para la asociación automatizada de insumos y jeringas de aplicación por dosis biológica.

---

## 3.3.4. Fase IV: Pruebas de Calidad del Software

La fase de pruebas en Extreme Programming constituye el pilar fundamental que garantiza la fiabilidad operativa del software. Se implementó una estrategia piramidal de aseguramiento de calidad con pruebas unitarias, pruebas de integración de API y pruebas de aceptación formal con el cliente en el sitio (*On-site Customer*).

### 3.3.4.1. Estrategia Piramidal de Pruebas Automatizadas

La suite de pruebas automatizadas se estructuró empleando el framework Jest y la librería Supertest para la simulación de peticiones HTTP en memoria. En la Figura 34 se ilustra la ejecución real de las pruebas unitarias de `MovimientosCalculationService.ts` en `backend/src/__tests__/movimientos-entrega-adicional-stock.test.ts`, validando la suma exacta de entregas base y adicionales y la propagación de saldos calculados al mes subsiguiente ($M+1$).

**Figura 34**  
*Suite de Pruebas Unitarias Automatizadas en Jest para Algoritmos de Movimientos y Stock*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_34.png]
```

*Nota.* Consola de ejecución de la suite de pruebas unitarias en Jest demostrando el cumplimiento del 100% de los casos de prueba transaccionales sin discrepancias.

En la Tabla 24 se resume la cobertura y distribución de las suites de pruebas automatizadas implementadas en el backend de SIVAC.

**Tabla 24**  
*Resumen de Suites de Pruebas Automatizadas Unitarias y de Integración en Jest*

| Suite de Pruebas | Archivo de Especificación | Componente Evaluado | Casos Ejecutados | Resultado |
|---|---|---|:---:|:---:|
| Pruebas de Movimientos y Stock | `movimientos-entrega-adicional-stock.test.ts` | Algoritmos de cálculo de saldos y sincronización M+1 | 8 casos | 100% Exitoso |
| Pruebas de Seguridad y RBAC | `auth-middleware.test.ts` | Validación de tokens JWT y extracción de permisos | 6 casos | 100% Exitoso |
| Pruebas de Control de Acceso | `permission-readonly.test.ts` | Restricción de escritura en perfiles de solo lectura | 5 casos | 100% Exitoso |
| Pruebas de Unicidad de Vales | `vales-generation.test.ts` | Prevención de duplicidad de comprobantes PECOSA | 6 casos | 100% Exitoso |
| Pruebas de Cooldown de Alertas | `alerta-automatica.test.ts` | Supresión de alertas redundantes en ventana de 7 días | 4 casos | 100% Exitoso |
| Pruebas de Formato ICI-DEMID | `ici-demid-calculation.test.ts` | Cálculo de Consumo Promedio y semáforo MSD | 5 casos | 100% Exitoso |

*Nota.* Cobertura automatizada que garantiza la estabilidad del software ante refactorizaciones o actualizaciones normativas.

### 3.3.4.2. Pruebas de Aceptación con el Cliente (DISA Apurímac II)

Las pruebas de aceptación fueron diseñadas y ejecutadas conjuntamente con el personal de inmunizaciones de la DISA Apurímac II, evaluando cada una de las quince historias de usuario ($HU_1$ a $HU_{15}$) mediante casos de prueba de aceptación formales ($CP_1$ a $CP_{15}$). En la Tabla 25 se consolidan los resultados observados durante las sesiones de homologación técnica.

**Tabla 25**  
*Matriz de Casos de Prueba de Aceptación con el Usuario (CP-01 a CP-15)*

| Caso de Prueba | Historia Asociada | Escenario Operativo Evaluado | Criterio de Éxito | Resultado Observado en SIVAC | Dictamen |
|:---:|:---:|---|---|---|:---:|
| CP-01 | HU-01 | Autenticación de responsable con JWT y bloqueo de acceso no autorizado. | Emisión de token válido y código 403 ante ruta no asignada. | Autenticación exitosa en < 1 s; bloqueo 403 verificado. | Aprobado |
| CP-02 | HU-02 | Alta de nuevo puesto de salud y verificación de integridad referencial. | Registro en jerarquía y rechazo de duplicados de RENIPRESS. | Creación conforme; rechazo de clave duplicada verificado. | Aprobado |
| CP-03 | HU-03 | Parametrización de vacuna BCG (10 dosis) y jeringa autodescartable. | Registro de rangos térmicos (+2 a +8 °C) y factor de dilución. | Parámetros técnicos consolidados según NTS N° 196. | Aprobado |
| CP-04 | HU-04 | Ingreso de lotes con fechas escalonadas y selección para despacho. | Asignación prioritaria del lote más próximo a caducar (FEFO). | Despacho automático del lote más antiguo verificado. | Aprobado |
| CP-05 | HU-05 | Carga de meta anual (1,200 dosis) y distribución en doce mensualidades. | Suma aritmética de meses igual a la meta anual fijada. | Validación matemática estricta antes del guardado. | Aprobado |
| CP-06 | HU-06 | Captura digital de movimientos mensuales en cuadrícula interactiva. | Persistencia en base de datos en tiempo inferior a 2 minutos. | Tiempo medio de registro: 1.15 min (antes 14.8 min). | Aprobado |
| CP-07 | HU-07 | Consolidación de mes $m$ y verificación de saldo inicial en mes $m+1$. | Traslado automático exacto del saldo final como saldo inicial. | Cero discrepancias matemáticas ($0.00\%$ error). | Aprobado |
| CP-08 | HU-08 | Incremento de 50 dosis en mayo y redistribución en meses futuros. | Compensación automática en meses restantes (meta intacta). | Descuento ordenado en junio y julio verificado. | Aprobado |
| CP-09 | HU-09 | Registro de remesa extraordinaria ante brote distrital de influenza. | Grabación de entrega adicional vinculada sin bloqueo contable. | Registro exitoso y recálculo de entrega total conforme. | Aprobado |
| CP-10 | HU-10 | Despacho de 200 dosis de vacuna y asignación automática de jeringas. | Asociación de 200 jeringas autodescartables en el vale. | Asignación exacta según norma técnica sin cálculo manual. | Aprobado |
| CP-11 | HU-11 | Emisión de vale mensual para postas adscritas con correlativo único. | Comprobante emitido en menos de 3 s con cero duplicidad. | Vale emitido en 1.45 s con correlativo seguro. | Aprobado |
| CP-12 | HU-12 | Exportación de comprobante oficial a formato PDF y hoja Excel. | Formato PECOSA institucional con membrete y casilleros de firma. | Documentos generados idénticos al formato MINSA en 3.2 s. | Aprobado |
| CP-13 | HU-13 | Consulta cronológica de movimientos de almacén en kardex digital. | Asientos inmutables de entrada, salida y saldos correlativos. | Trazabilidad histórica completa; 100% coincidente con físico. | Aprobado |
| CP-14 | HU-14 | Simulación de lote con 25 días restantes y stock bajo mínimo. | Notificación de alerta visual roja en campana de interfaz. | Alerta crítica inmediata emitida con control de cooldown. | Aprobado |
| CP-15 | HU-15 | Visualización de avance de metas y semáforo MSD en dashboard. | Despliegue interactivo de gráficos y semáforos en < 2 s. | Carga veloz de tableros Recharts y semáforos DEMID. | Aprobado |

*Nota.* Pruebas de aceptación ejecutadas en las instalaciones de la DISA Apurímac II con participación de los usuarios finales de la cadena de frío.

### 3.3.4.3. Evaluación de Calidad del Software según ISO/IEC 25010:2023

La evaluación de la calidad de SIVAC se fundamentó en el estándar internacional ISO/IEC 25010:2023, examinando las cuatro características de calidad esenciales para sistemas de gestión sanitaria: adecuación funcional, usabilidad, eficiencia de desempeño, y fiabilidad y seguridad. En la Tabla 26 se sintetizan los resultados de la evaluación.

**Tabla 26**  
*Matriz de Evaluación de Calidad del Producto de Software según ISO/IEC 25010:2023*

| Característica ISO/IEC 25010 | Subcaracterística Evaluada | Métrica Evaluada en SIVAC | Valor Observado | Nivel de Conformidad |
|---|---|---|---|:---:|
| Adecuación Funcional | Completitud funcional | Cobertura de procesos normados de distribución | 100% de procesos cubiertos | Excelente |
| Adecuación Funcional | Corrección funcional | Tasa de error aritmético en balance de saldos | $0.00\%$ de error observado | Excelente |
| Usabilidad | Capacidad de aprendizaje | Tiempo promedio de inducción de operadores | Menos de 25 minutos | Excelente |
| Usabilidad | Protección contra errores | Tasa de transacciones rechazadas por validación | 100% de datos inválidos bloqueados | Excelente |
| Eficiencia de Desempeño | Comportamiento temporal | Tiempo de respuesta medio de endpoints de API | 185 milisegundos | Excelente |
| Eficiencia de Desempeño | Comportamiento temporal | Tiempo de emisión de comprobantes de despacho | 1.45 segundos | Excelente |
| Fiabilidad | Madurez y tolerancia | Recuperación ante fallos transaccionales | Cero registros corruptos (ACID) | Excelente |
| Seguridad | Confidencialidad y control | Robustez criptográfica de credenciales y tokens | Bcrypt salt 10 / JWT HMAC-SHA256 | Excelente |

*Nota.* Matriz consolidada de evaluación de calidad de producto de software bajo el estándar ISO/IEC 25010:2023.

---

## 3.3.5. Fase V: Despliegue Físico y Puesta en Producción

Concluida la fase de pruebas de aceptación y homologación técnica, se ejecutó el despliegue físico del software en la infraestructura de servidores de la Dirección de Salud Apurímac II.

### 3.3.5.1. Topología de Red, Contenedores Docker y Orquestación

Para asegurar la alta disponibilidad, la replicabilidad de entornos y la independencia del hardware físico, SIVAC se desplegó mediante una arquitectura de contenedores orquestada con **Docker Compose**. En la Figura 35 se detalla el diagrama de despliegue físico y topología de red en producción.

**Figura 35**  
*Diagrama de Despliegue Físico y Topología de Red en Producción con Docker y Nginx*

```
[Ver figura original en: salidas/figuras/software_xp/imagen_xp_35.png]
```

*Nota.* Topología de red que ilustra el aislamiento de los contenedores Docker en una subred privada virtual, la terminación TLS en el proxy inverso Nginx y la persistencia de datos en PostgreSQL 16.

La infraestructura se diseñó considerando tres niveles de aislamiento:
1. **Servidor Proxy Inverso (Nginx):** Recibe las conexiones entrantes desde la red institucional de la DISA Apurímac II en los puertos estándar 80 (HTTP) y 443 (HTTPS). Se encarga de la terminación criptográfica TLS 1.3, compresión gzip de respuestas web, gestión de cabeceras de seguridad y despacho de los archivos estáticos de la Single Page Application (SPA).
2. **Servidor de Aplicaciones Backend (Node.js 20):** Ejecutado en un contenedor Docker optimizado sobre distribución Alpine Linux. Se comunica de forma exclusiva con el proxy Nginx a través de una red virtual privada interna (`app-network`), exponiendo los servicios RESTful en el puerto interno 3000 sin exposición directa a la red externa.
3. **Servidor de Base de Datos (PostgreSQL 16):** Contenedor de base de datos relacional aislado en la subred interna, accesible únicamente por el backend mediante credenciales protegidas inyectadas por variables de entorno. La persistencia física se garantiza mediante volúmenes montados en el almacenamiento seguro del servidor anfitrión (`sivac_pgdata`), complementado con tareas programadas diarias de copia de seguridad automatizada (`pg_dump`) archivadas en almacenamiento cifrado externo.
