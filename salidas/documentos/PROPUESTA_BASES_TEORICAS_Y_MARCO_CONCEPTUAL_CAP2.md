---
tipo: propuesta_capitular
fase: F3
agente: redactor-academico
squad: Squad E (Redacción, Estilo y Maquetación Editorial)
estado: consolidado_definitivo
fecha: 2026-10-07
---

# PROPUESTA DE BASES TEÓRICAS (2.2) Y MARCO CONCEPTUAL (2.3) — CAPÍTULO II

## 2.2 Bases teóricas

Las bases teóricas de la presente investigación se estructuran de forma articulada en torno a los dos ejes epistemológicos fundamentales del estudio: la variable independiente, constituida por el sistema web SIVAC, y la variable dependiente, correspondiente a la gestión de movimientos de vacunas. En el primer eje se desarrollan los fundamentos de la arquitectura de software distribuida, los sistemas de información logística sanitaria, la metodología ágil Extreme Programming (XP) y el modelo de calidad de producto de software bajo la norma internacional ISO/IEC (2023). En el segundo eje se fundamenta el marco normativo de la cadena de frío, los procesos transaccionales de control de biológicos en almacén y la sustentación teórica y psicométrica de las tres dimensiones de la gestión de movimientos de vacunas: oportunidad de procesamiento, consistencia documental y satisfacción del usuario bajo el Modelo de Aceptación Tecnológica (Davis, 1989).

### 2.2.1 Sistema web

Un sistema web es una aplicación informática distribuida cuya lógica de negocio y capas de persistencia residen centralizadas en un servidor accesible mediante navegadores a través de una red de comunicaciones, prescindiendo de instalaciones individuales en las estaciones de trabajo de los usuarios (Sommerville, 2016). Esta tipología tecnológica ofrece accesibilidad ubicua, concurrencia sincronizada y centralización de los flujos de información, características que resultan determinantes para optimizar la coordinación administrativa entre dependencias de salud físicamente dispersas (Luján Mora, 2002; Mego Navarro, 2021).

**Arquitectura web y servicios desacoplados cliente-servidor**

La arquitectura de software constituye la organización fundamental de los componentes de un sistema, sus relaciones mutuas y los principios que guían su diseño y evolución técnica (Pressman, 2010). En las aplicaciones modernas, el modelo cliente-servidor desacoplado divide las responsabilidades del sistema en tres capas bien diferenciadas: la capa de presentación (cliente web), la capa de aplicación o lógica de negocio (servidor de servicios) y la capa de acceso y persistencia de datos (gestor de base de datos relacional) (Sommerville, 2016). La capa de presentación se ejecuta en el navegador del usuario y se encarga de capturar las acciones del operador sanitario y renderizar interfaces dinámicas; la capa intermedia procesa las reglas de negocio institucionales, valida los datos de entrada y coordina las transacciones; y la capa de datos almacena de forma consistente los registros históricos de movimientos, existencias y usuarios (Luján Mora, 2002; Pressman, 2010).

La comunicación entre el cliente y el servidor se articula a través del protocolo seguro HTTPS y una Interfaz de Programación de Aplicaciones basada en el estilo arquitectural REST (Representational State Transfer) (Ruiz Barea, 2023). Bajo este enfoque, los recursos logísticos —tales como lotes de vacunas, comprobantes de salida y registros de kardex— se identifican con identificadores uniformes de recursos (URI) y se manipulan con métodos HTTP estándar (GET, POST, PUT, DELETE) empleando representaciones estructuradas en formato JSON (Ruiz Barea, 2023). La seguridad transaccional se garantiza por medio de mecanismos de autenticación sin estado soportados en tokens web JSON (JWT), los cuales viajan firmados criptográficamente en las cabeceras de cada solicitud, permitiendo implementar políticas estrictas de control de acceso basado en roles (RBAC) para salvaguardar la confidencialidad e integridad del inventario de biológicos (Ruiz Barea, 2023).

En el ámbito de la salud pública, la evolución de los sistemas transaccionales hacia plataformas de Gestión de Información Logística Electrónica (denominadas internacionalmente e-LMIS) y Sistemas de Información de Inmunizaciones (IIS) ha marcado la transición desde registros aislados en cuadernos físicos hacia entornos centralizados de visibilidad en tiempo real (Brooks et al., 2024; Duong et al., 2021). Estos sistemas organizan y consolidan la demanda, los movimientos de stock, las fechas de expiración de biológicos y las transferencias de suministros, proporcionando datos fidedignos para la toma de decisiones sanitarias y evitando la fragmentación operativa (Brooks et al., 2024).

**Tabla 1**  
*Características de los sistemas web aplicados a la gestión sanitaria*

| Característica | Definición teórica | Aplicación en la gestión sanitaria |
|---|---|---|
| Centralización de datos | Concentración de la persistencia de información en un repositorio único y normalizado (Sommerville, 2016). | Eliminación de registros manuales dispersos y hojas de cálculo desvinculadas entre almacenes. |
| Accesibilidad ubicua | Capacidad de acceder al sistema desde cualquier dispositivo autorizado mediante un navegador web (Luján Mora, 2002). | Disponibilidad inmediata de consulta de stock y saldos desde cualquier centro de acopio de la red. |
| Desacoplamiento multicapa | Separación lógica entre presentación, reglas de negocio y almacenamiento de datos (Pressman, 2010). | Modularidad técnica, facilidad de mantenimiento e independencia de las interfaces de usuario. |
| Comunicación REST y JWT | Intercambio de datos estructurados en JSON y autenticación sin estado basada en tokens firmados (Ruiz Barea, 2023). | Interoperabilidad segura y control de privilegios de acceso según roles de los operadores de salud. |
| Trazabilidad transaccional | Registro cronológico, persistente y auditable de cada operación realizada en el sistema (Brooks et al., 2024). | Identificación unívoca del usuario, fecha, lote y volumen biológico comprometido en cada movimiento. |

*Nota.* Elaboración propia a partir de Brooks et al. (2024), Luján Mora (2002), Pressman (2010), Ruiz Barea (2023) y Sommerville (2016).

La disposición estructural descrita se esquematiza en la Figura 1, en la cual se representa la interacción entre las estaciones de trabajo de los operadores de salud, la capa de servicios web seguros y el repositorio central de datos.

**Figura 1**  
*Arquitectura cliente-servidor desacoplada para sistemas web*

```text
[ Estaciones de Trabajo / Navegador ]
  • Responsable de Inmunizaciones
  • Responsable de Cadena de Frío
             |
             | Peticiones HTTPS / REST (Payload JSON con Bearer Token JWT)
             v
[ Servidor de Aplicaciones Web / API REST ]
  • Capa de Ruteo y Controladores
  • Middleware de Autenticación y Autorización (JWT / RBAC)
  • Servicios de Negocio: Movimientos, Kardex, Lotes, Vales PECOSA
             |
             | Mapeo Objeto-Relacional (ORM / Consultas SQL Transaccionales)
             v
[ Base de Datos Relacional Centralizada ]
  • Tablas Normalizadas: Lotes, Vacunas, Movimientos, Centros de Acopio, Vales
```

*Nota.* Representación esquemática de la interacción en arquitectura cliente-servidor desacoplada con servicios REST y control de acceso seguro. Adaptado de Mego Navarro (2021), Pressman (2010) y Sommerville (2016).

**Metodología ágil Extreme Programming (XP) en el contexto de sistemas de salud**

La metodología Extreme Programming (XP) es un enfoque ágil de desarrollo de software propuesto por Kent Beck (1999), diseñado específicamente para optimizar la productividad de equipos de trabajo pequeños o medianos que enfrentan requerimientos dinámicos y de alta incertidumbre operacional. XP fundamenta su práctica en cuatro valores esenciales: comunicación continua entre desarrolladores y usuarios finales, simplicidad en el diseño arquitectónico, retroalimentación constante a través de entregas funcionales frecuentes, y valentía para refactorizar y descartar soluciones ineficientes (Beck, 1999).

El ciclo de desarrollo en Extreme Programming se estructura en cuatro fases iterativas que garantizan la alineación del software con las necesidades reales del entorno operativo (Beck, 1999; Pressman, 2010; Sommerville, 2016):
1. *Fase de exploración y planificación:* Se identifican los problemas del dominio, se redactan las historias de usuario en estrecha colaboración con el personal institucional y se planifican los lanzamientos (releases) e iteraciones según la prioridad del negocio (Beck, 1999).
2. *Fase de diseño:* Se privilegia el diseño conceptual simple que satisface de forma inmediata los requerimientos vigentes, evitando sobreingeniería especulativa y recurriendo a soluciones puntuales (spikes) cuando surgen desafíos técnicos específicos (Pressman, 2010).
3. *Fase de codificación:* Se construyen los módulos incrementales aplicando prácticas clave como el desarrollo guiado por pruebas (Test-Driven Development - TDD), la programación en parejas (pair programming) y la integración continua del código (Sommerville, 2016).
4. *Fase de pruebas:* Se ejecutan de forma automatizada las pruebas unitarias y de integración para asegurar que los incrementos de software no introduzcan defectos colaterales, y se somete el sistema a pruebas de aceptación directa con los operadores para certificar que cada funcionalidad satisface plenamente sus criterios normativos (Beck, 1999; Pressman, 2010).

La especificación de los requerimientos en XP se sustenta en el estándar de Historias de Usuario formulado por Mike Cohn (2004). Una historia de usuario es una descripción concisa, formulada en lenguaje natural comprensible tanto para usuarios como para desarrolladores, estructurada según la plantilla ágil de Mike Cohn para la especificación de requerimientos orientados al usuario (Cohn, 2004). Cada historia de usuario incorpora criterios de aceptación verificables que delimitan cuándo la funcionalidad se considera terminada, permitiendo al equipo estimar el esfuerzo de desarrollo en puntos de historia y secuenciar las iteraciones de manera objetiva (Cohn, 2004; Mego Navarro, 2021).

En contextos de salud pública, la aplicación de XP ha demostrado su eficacia al promover una interacción directa entre los desarrolladores y el personal sanitario, garantizando que los módulos construidos respondan con exactitud a las exigencias normativas del flujo de trabajo institucional (Mego Navarro, 2021).

**Figura 2**  
*Fases y ciclo iterativo de la metodología Extreme Programming (XP)*

```text
  [ 1. Exploración y Planificación ]
    • Captura de Historias de Usuario (Cohn, 2004)
    • Estimación de Puntos de Historia y Plan de Release
                   |
                   v
  [ 2. Diseño Simple ] <-----------------------------+
    • Arquitectura modular desacoplada               |
    • Tarjetas CRC y Soluciones Spike                |
                   |                                 | Retroalimentación
                   v                                 | e iteración
  [ 3. Codificación Incremental ]                    | continua
    • Programación en Parejas                        |
    • Desarrollo Guiado por Pruebas (TDD)            |
    • Integración Continua y Refactorización         |
                   |                                 |
                   v                                 |
  [ 4. Pruebas de Aceptación ] ----------------------+
    • Pruebas funcionales con el usuario institucional
    • Entrega de incremento de software validado
```

*Nota.* Ciclo iterativo continuo de desarrollo ágil en Extreme Programming. Adaptado de Beck (1999) y Pressman (2010).

**Tabla 2**  
*Prácticas de ingeniería de software en Extreme Programming aplicadas a SIVAC*

| Práctica de XP | Principio metodológico | Aplicación en el desarrollo del sistema SIVAC |
|---|---|---|
| Historias de usuario | Captura de requerimientos funcionales desde la perspectiva del usuario final (Cohn, 2004). | Formalización de 15 Historias de Usuario que modelan el registro de lotes, salidas, kardex y vales PECOSA. |
| Entregas pequeñas | Despliegue de incrementos funcionales en lapsos cortos de tiempo (Beck, 1999). | Planificación de 4 iteraciones quincenales orientadas a liberar módulos operativos independientes. |
| Diseño simple | Implementación de la solución más sencilla que satisface los requerimientos actuales (Pressman, 2010). | Estructura modular de base de datos y endpoints REST orientados estrictamente a la gestión de biológicos. |
| Pruebas continuas | Verificación automatizada de componentes antes y durante la codificación (Sommerville, 2016). | Diseño de pruebas unitarias y validación formal de criterios de aceptación con el personal de salud. |
| Refactorización | Reestructuración interna del código sin modificar su comportamiento externo (Beck, 1999). | Optimización continua de consultas de saldo de kardex y validación de reglas de consistencia de lotes. |
| Integración continua | Fusión e integración del código desarrollado de forma periódica en el repositorio (Pressman, 2010). | Detección inmediata de inconsistencias entre componentes de interfaz y servicios del backend. |

*Nota.* Elaboración propia a partir de Beck (1999), Cohn (2004), Pressman (2010) y Sommerville (2016).

**Estándar de calidad del producto de software ISO/IEC 25010:2023**

La calidad de un sistema informático comprende el conjunto de propiedades y características que determinan su aptitud para satisfacer los requisitos explícitos e implícitos de los usuarios bajo condiciones operativas determinadas (ISO/IEC, 2023). La norma internacional ISO/IEC (2023), enmarcada en la serie SQuaRE (*Systems and software Quality Requirements and Evaluation*), actualiza y redefine el modelo de calidad de producto de software clasificándolo en nueve características cardinales: adecuación funcional, eficiencia de desempeño, compatibilidad, capacidad de interacción, fiabilidad, seguridad, mantenibilidad, flexibilidad y seguridad de uso.

En la edición 2023 del estándar, se introducen ajustes taxonómicos fundamentales respecto a versiones anteriores: la característica tradicionalmente denominada usabilidad se define formalmente como capacidad de interacción (*interaction capability*), reflejando con mayor precisión la bidireccionalidad entre el usuario y la plataforma, mientras que la portabilidad se reconceptualiza como flexibilidad (*flexibility*) (ISO/IEC, 2023).

En los sistemas informáticos orientados al sector salud, las dimensiones de calidad técnica más críticas corresponden a la adecuación funcional, la capacidad de interacción y la eficiencia de desempeño (Moumane et al., 2024):
- *Adecuación funcional:* Representa el grado en que el software provee funciones que satisfacen las necesidades declaradas para el manejo del inventario sanitario. Se subdivide en completitud funcional (disponibilidad de todas las tareas requeridas, tales como registro de lotes, generación de vales y conciliación de saldos), corrección funcional (precisión exacta de los cálculos matemáticos de existencias) y pertinencia funcional (alineación del software con los objetivos logísticos de la institución) (ISO/IEC, 2023).
- *Capacidad de interacción:* Mide la facilidad con la que los operadores sanitarios pueden comprender, aprender, utilizar y controlar la aplicación. Integra las subcaracterísticas de reconocibilidad de la idoneidad, aprendibilidad, operabilidad, protección contra errores del usuario y estética de la interfaz (ISO/IEC, 2023). En entornos asistenciales, la protección contra errores cobra un papel determinante, pues previene ingresos erróneos de números de lote, cantidades negativas o fechas de caducidad expiradas (Moumane et al., 2024).
- *Eficiencia de desempeño:* Evalúa la capacidad del sistema para procesar transacciones en lapsos mínimos de respuesta y con un consumo racional de recursos de red y memoria (ISO/IEC, 2023).

La investigación empírica conducida por Moumane et al. (2024) al evaluar aplicaciones de salud mediante el estándar ISO/IEC 25010 demostró que la adecuación funcional y la capacidad de interacción son los factores determinantes que gobiernan la operabilidad, la reducción de errores humanos y la adopción sostenida de las herramientas digitales por parte de los profesionales sanitarios.

**Tabla 3**  
*Características del modelo de calidad de software según el estándar internacional (ISO/IEC, 2023)*

| Característica | Subcaracterísticas principales | Enfoque de evaluación en el sistema SIVAC |
|---|---|---|
| Adecuación funcional | Completitud funcional, corrección funcional y pertinencia funcional (ISO/IEC, 2023). | Verificación de que el sistema ejecuta sin omisiones ni errores matemáticos el registro de entradas, salidas y emisión de vales. |
| Capacidad de interacción | Reconocibilidad, aprendibilidad, operabilidad, protección contra errores y accesibilidad (ISO/IEC, 2023). | Evaluación de la facilidad de uso, claridad de formularios y validaciones automáticas que previenen digitaciones erróneas. |
| Eficiencia de desempeño | Comportamiento temporal, utilización de recursos y capacidad (ISO/IEC, 2023). | Medición de tiempos de respuesta instantáneos en la consulta de existencias y emisión de comprobantes de salida. |
| Seguridad | Confidencialidad, integridad, no repudio, autenticidad y responsabilidad (ISO/IEC, 2023). | Autenticación criptográfica mediante JWT y control de permisos por roles para proteger los datos de inventario. |
| Fiabilidad | Madurez, disponibilidad, tolerancia a fallos y capacidad de recuperación (ISO/IEC, 2023). | Estabilidad del servicio ante accesos concurrentes de los centros de acopio y persistencia consistente en la base de datos. |

*Nota.* Elaboración propia a partir de ISO/IEC (2023) y Moumane et al. (2024).

---

### 2.2.2 Gestión de movimientos de vacunas

La gestión de movimientos de vacunas comprende el conjunto integral de procesos técnicos, administrativos y operativos orientados a programar, recepcionar, almacenar, custodiar, despachar, registrar y conciliar el flujo físico y documental de biológicos en una red de servicios de salud (MINSA, 2022). Constituye la variable dependiente de la investigación y se fundamenta en la necesidad ineludible de mantener la trazabilidad unitaria y oportuna de los inventarios inmunológicos para garantizar el abastecimiento equitativo y la inocuidad de las dosis administradas a la población (OPS y PATH, 2020).

**Marco logístico y normativo de la cadena de frío e inmunizaciones**

En el Perú, la gestión de vacunas se encuentra regulada por la Norma Técnica de Salud NTS N° 196-MINSA/DGIESP-2022, aprobada mediante Resolución Ministerial N° 884-2022/MINSA, la cual fija el Esquema Nacional de Vacunación y norma los procedimientos obligatorios para la recepción, almacenamiento, distribución y registro de biológicos en todo el territorio nacional (MINSA, 2022). Debido a su composición biológica termolábil, las vacunas sufren desnaturalización irreversible si son expuestas a variaciones térmicas fuera de los límites de seguridad normados, situados obligatoriamente entre +2 °C y +8 °C (Champi Velásquez, 2023; MINSA, 2022).

La cadena de frío constituye el soporte técnico-logístico que asegura que los biológicos mantengan su potencia inmunológica y condiciones de calidad desde su fabricación hasta su aplicación en el usuario (Champi Velásquez, 2023). Este sistema comprende tres niveles de almacenamiento: el nivel central (almacenes nacionales), el nivel regional o intermedio (Direcciones de Salud como la DISA Apurímac II y sus centros de acopio provinciales) y el nivel local (establecimientos y puestos de salud ejecutores) (MINSA, 2022).

No obstante, como subrayan Champi Velásquez (2023) y OPS y PATH (2020), la viabilidad de la cadena de frío no depende únicamente de la existencia de cámaras frigoríficas y refrigeradoras especializadas, sino de la sincronización estricta entre la custodia física y el control documental de las operaciones. Si los movimientos de ingreso, egreso o distribución entre centros de acopio se registran con retraso o de forma incompleta en cuadernos manuales, se debilita la trazabilidad institucional y se generan distorsiones en el stock disponible, provocando despachos ciegos, sobreabastecimiento de biológicos con riesgo de vencimiento o desabastecimientos imprevistos en los puntos de vacunación (Chekol et al., 2023; Ergetie et al., 2023).

**Procesos operativos del flujo de biológicos, control de lotes y kardex**

Las operaciones del almacén de biológicos se articulan mediante transacciones logísticas bien definidas (MINSA, 2022):
1. *Ingresos de biológicos:* Entrada formal de vacunas al almacén, que demanda inspeccionar el monitoreo de temperatura durante el transporte, constatar el número de lote, verificar la fecha de vencimiento y asentar la cantidad recibida conforme a las guías de remisión (MINSA, 2022).
2. *Control de lotes y fechas de expiración:* El lote constituye el código alfanumérico normativo asignado por el fabricante que identifica a un conjunto uniforme de dosis biológicas (MINSA, 2022). La administración logística exige aplicar de forma estricta el principio PEPS (primeras entradas, primeras salidas) o PVPS (primeras en vencer, primeras en salir), priorizando el despacho de aquellos lotes cuya fecha de caducidad sea más próxima para impedir mermas biológicas (MINSA, 2022; Wasswa et al., 2023).
3. *Egresos y transferencias institucionales:* Despacho de vacunas hacia los centros de acopio y microredes ejecutoras, el cual exige formalizarse administrativamente mediante la emisión de un Pedido-Comprobante de Salida (vale PECOSA), documento oficial que certifica la transferencia de custodia del biológico (MINSA, 2022).
4. *Kardex de existencias:* Instrumento de control en el que se asientan de manera secuencial los ingresos, egresos y saldos disponibles por cada tipo de vacuna y número de lote (MINSA, 2022). La transición hacia un kardex digitalizado centralizado permite consolidar los saldos en tiempo real, erradicar la duplicidad de registros y proporcionar una fuente única de verdad para la conciliación de inventarios (Chekol et al., 2023; Wasswa et al., 2023).

**Figura 3**  
*Componentes y flujo documental de la cadena de frío de vacunas*

```text
  [ Nivel Central / Laboratorio ]
                 |
                 | Guía de Remisión y Acta de Recepción (+2 °C a +8 °C)
                 v
  [ Centro de Distribución Regional / DISA Apurímac II ]
    • Inspección Técnica y Verificación de Lote / Vencimiento
    • Asentamiento en Kardex de Biológicos (Entrada de Stock)
                 |
                 | Programación y Emisión de Comprobante de Salida / Vale PECOSA
                 v
  [ 11 Centros de Acopio Intermedios / Microredes ]
    • Recepción y Conciliación Física vs Documental
    • Actualización de Saldos en Kardex de Destino
                 |
                 | Despacho a Brigadas y Puestos de Vacunación
                 v
  [ Usuario Final / Población Protegida ]
```

*Nota.* Flujo logístico y documental integrado en los distintos eslabones de la cadena de frío sanitaria. Adaptado de Champi Velásquez (2023), MINSA (2022) y OPS y PATH (2020).

**Dimensión 1: Oportunidad de procesamiento**

La oportunidad de procesamiento se define teóricamente como la capacidad del sistema de gestión para registrar, tramitar, despachar y formalizar las operaciones logísticas sobre los biológicos dentro de lapsos temporales mínimos, asegurando la inmediata disponibilidad de la información para la toma de decisiones sanitarias (Astuhuaman Perez & Baltazar Maza, 2024; Balón Morejón, 2023). En entornos asistenciales, la latencia o retraso temporal en el procesamiento de datos genera desabastecimientos ficticios, dificulta la atención oportuna a la demanda y prolonga el tiempo de espera del personal que acude a retirar biológicos para las campañas de inmunización (Dang et al., 2024; Wasswa et al., 2023).

Esta dimensión se cuantifica a través de dos indicadores temporales de razón, medidos rigurosamente en minutos cronometrados:
- *Tiempo de registro de movimiento de vacunas (Treg):* Representa el intervalo cronometrado requerido para capturar, validar e ingresar al inventario los datos de una transacción de biológicos (ingreso o egreso por tipo de vacuna, número de lote, fecha de vencimiento y volumen) hasta la efectiva actualización de los saldos en el kardex.
- *Tiempo de emisión de comprobante de salida / vale PECOSA (Tvale):* Cuantifica el lapso cronometrado transcurrido desde la recepción y revisión de la programación de vacunas solicitada por un centro de acopio o microred hasta la generación, impresión, validación y formalización documental del comprobante oficial de despacho de los biológicos.

El sustento empírico de esta dimensión se apoya en evidencias de modernización tecnológica en salud. Balón Morejón (2023), al implementar una aplicación web para el control de inventarios y campañas de vacunación en un centro de salud de Ecuador, demostró que la sistematización de los registros manuales redujo drásticamente el tiempo de procesamiento y obtención de balances de tres a cuatro días laborables a escasos seis segundos. A nivel regional, Astuhuaman Perez y Baltazar Maza (2024), en una investigación preexperimental desarrollada en un centro de salud de la provincia de Cotabambas (Apurímac), evidenciaron que la implementación de un sistema web redujo significativamente los tiempos de elaboración y atención en salud en un 15.1% y los tiempos de asentamiento en registros en un 24.6% (Wilcoxon *p* < 0.001).

Asimismo, Dang et al. (2024), en una investigación mixta sobre la transición del registro en papel al sistema nacional digital de inmunizaciones en Vietnam, reportaron que la latencia desde la ejecución del evento hasta la disponibilidad efectiva del dato en el sistema se redujo de 18.6 a 5.7 días en zonas urbanas y de 36.1 a 11.7 días en provincias rurales (*p* < 0.001). En la misma línea, Wasswa et al. (2023) concluyeron que la implementación de plataformas e-LMIS en Uganda permitió la visibilidad de los inventarios en tiempo real, acelerando la capacidad de respuesta logística y eliminando los cuellos de botella temporales en la distribución de biológicos.

**Dimensión 2: Consistencia documental**

La consistencia documental se fundamenta en la teoría de la calidad de datos y la auditoría logística de inventarios en salud pública, definiéndose como el grado de concordancia aritmética, exactitud, completitud y apego normativo entre los registros de movimientos asentados en el sistema y las existencias y despachos físicos de biológicos ejecutados en los centros de acopio (Chekol et al., 2023; Kigenza et al., 2023; Shen et al., 2024). En los esquemas manuales tradicionales basados en cuadernos y planillas de cálculo no integradas, los errores de transcripción, las omisiones de dígitos en los números de lote y la falta de conciliación entre lo solicitado y lo entregado configuran discrepancias documentales crónicas que vulneran la trazabilidad sanitaria (Ergetie et al., 2023; Garcia Villacorta y Calderón Huaman, 2023).

La consistencia documental se operacionaliza mediante dos indicadores porcentuales de concordancia objetiva:
- *Porcentaje de registros sin discrepancias (RSD):* Mide la proporción de transacciones de biológicos auditadas que satisfacen simultáneamente y sin error alguno ocho criterios normativos de integridad: coincidencia del código del biológico, denominación correcta de la vacuna, número de lote exacto, fecha de vencimiento vigente, tipo de movimiento justificado, cantidad física coincidente con el registro, centro de origen/destino acreditado y conformidad de firmas de los responsables. Se calcula como la proporción porcentual entre los registros conformes y el total de registros auditados.
- *Porcentaje de concordancia entre cantidad programada y cantidad entregada (CPE):* Evalúa la fidelidad del abastecimiento logístico mediante la razón porcentual entre el volumen físico de biológicos efectivamente despachado conforme a requerimiento y la cantidad previamente programada y solicitada por las dependencias ejecutoras.

El respaldo empírico de esta dimensión se fundamenta en rigurosos estudios internacionales y nacionales. Shen et al. (2024), en un estudio sobre optimización de cadenas de suministro hospitalarias en China, demostraron empíricamente que la digitalización y el control sistematizado de existencias redujeron la tasa anual de error documental de 0.425‰ a 0.025‰, incrementando la eficiencia de la cadena logística en un 42.4% y eliminando las brechas entre existencias físicas y registros digitales. De forma análoga, Kigenza et al. (2023) documentaron una intervención a gran escala en 596 puntos de distribución de salud en Ruanda, reportando que el fortalecimiento del sistema electrónico e-LMIS elevó la exactitud de los datos de inventario del 25% al 85%, reduciendo simultáneamente los desabastecimientos de suministros médicos del 10% al 1%.

Por su parte, Chekol et al. (2023), al evaluar la calidad de los datos logísticos rutinarios en centros de salud de Etiopía, identificaron que los sistemas manuales alcanzaban una concordancia de apenas 74% (IC 95%: 68–78%), situándose marcadamente por debajo de los estándares sanitarios internacionales; los autores demostraron que la complejidad de los formatos en papel y la carencia de reglas de validación cruzada automática eran los principales factores causales de las inconsistencias documentales. En concordancia, Ergetie et al. (2023) observaron que el 68% de los centros de salud evaluados presentaban una gestión documental deficiente en sus registros de biológicos. En el ámbito nacional, Garcia Villacorta y Calderón Huaman (2023) demostraron que la introducción de un sistema web para el control de inventarios farmacéuticos elevó el nivel de control de 75.42% a 97.18% (prueba Z, *p* < 0.05), evidenciando que las interfaces automatizadas garantizan la consistencia documental al imponer validaciones de saldo previas al despacho.

**Dimensión 3: Satisfacción del usuario y Modelo de Aceptación Tecnológica (TAM)**

La satisfacción del usuario constituye un constructo multidimensional que describe la evaluación cognitiva, afectiva y actitudinal que realiza un operador respecto al grado en que un sistema informático responde a sus expectativas laborales, facilita sus tareas cotidianas y mejora su desempeño en la organización (Davis, 1989; Ndlovu et al., 2022). En la presente investigación, la fundamentación teórica de esta dimensión se sustenta sólidamente en el Modelo de Aceptación Tecnológica (*Technology Acceptance Model* - TAM), formulado seminalmente por Fred Davis (1989).

El modelo TAM postula que la adopción y satisfacción de los usuarios frente a una tecnología informática está determinada fundamentalmente por dos constructos cognitivos primarios (Davis, 1989):
1. *Utilidad Percibida (Perceived Usefulness - PU):* Definida como el grado en el cual una persona cree que el uso de un sistema en particular incrementará su rendimiento laboral dentro de la organización.
2. *Facilidad de Uso Percibida (Perceived Ease of Use - PEOU):* Definida como el grado en el cual una persona cree que el uso de una tecnología estará libre de esfuerzo físico o mental excesivo.

Según la formulación teórica de Davis (1989), la facilidad de uso percibida ejerce una influencia directa y positiva sobre la utilidad percibida, y ambos constructos determinan la actitud del usuario hacia el sistema, la cual a su vez predice la intención conductual de uso y el nivel sostenido de satisfacción operativa.

Para el contexto específico de los operadores sanitarios de la Dirección de Salud Apurímac II, y en estricta conformidad con el diseño preexperimental del estudio, los dos constructos del TAM se operacionalizan en dos indicadores de percepción evaluados longitudinalmente:
- *Aceptación del proceso (AP):* Derivado directamente del constructo de Facilidad de Uso Percibida (PEOU), cuantifica el grado de conformidad subjetiva, agilidad percibida y reducción de la carga cognitiva o estrés administrativo que experimenta el personal de salud al interactuar con el flujo de trabajo para registrar y distribuir vacunas.
- *Utilidad percibida (UP):* Mide el grado subjetivo en el cual el personal de salud valora que el sistema informático aporta valor práctico directo a sus funciones, garantizando la trazabilidad de los lotes, la exactitud de los saldos de biológicos y el soporte seguro para la toma de decisiones sanitarias.

Cada uno de estos indicadores se evalúa mediante cuatro reactivos psicométricos estructurados en escala Likert de 5 puntos (desde el desacuerdo absoluto hasta el acuerdo pleno), conformando un instrumento formal de 8 ítems que arroja una puntuación acumulada de 4 a 20 puntos por indicador y una escala global de 8 a 40 puntos para la dimensión global de satisfacción del usuario.

**Tabla 4**  
*Operacionalización teórica de los indicadores de satisfacción del usuario bajo el Modelo TAM*

| Indicador oficial | Constructo teórico TAM | Definición operacional en el servicio de inmunizaciones | Ponderación psicométrica |
|---|---|---|---|
| Aceptación del proceso (AP) | Facilidad de uso percibida, PEOU (Davis, 1989) | Grado en que el personal percibe que el flujo de trabajo para registrar movimientos y emitir vales es ágil, comprensible y reduce la carga operativa. | 4 reactivos tipo Likert de 1 a 5 puntos (Puntuación: 4 a 20 puntos). |
| Utilidad percibida (UP) | Utilidad percibida, PU (Davis, 1989) | Grado en que el personal valora que el sistema aporta control riguroso, trazabilidad por lote y confiabilidad para la toma de decisiones. | 4 reactivos tipo Likert de 1 a 5 puntos (Puntuación: 4 a 20 puntos). |
| Dimensión Satisfacción del Usuario | Modelo TAM Integral (Davis, 1989; Ndlovu et al., 2022) | Evaluación global de la complacencia y adopción del entorno de trabajo para la gestión de vacunas frente al método tradicional. | 8 reactivos tipo Likert de 1 a 5 puntos (Puntuación: 8 a 40 puntos). |

*Nota.* Elaboración propia fundamentada en el Modelo de Aceptación Tecnológica de Davis (1989), Ndlovu et al. (2022) y el estándar internacional ISO/IEC (2023).

La pertinencia del modelo TAM en el sector de la salud pública cuenta con sólida evidencia científica. Ndlovu et al. (2022), al investigar la aceptación de la plataforma DHIS2 por parte de trabajadores sanitarios en Botswana aplicando el modelo TAM, demostraron que la utilidad percibida y la facilidad de uso percibida son determinantes predictivos directos de la satisfacción y de la intención de adopción continua de los sistemas eHealth. De igual manera, Duong et al. (2021), en su evaluación sobre registros digitales de inmunización en 990 establecimientos de salud, hallaron que el 94.5% de los usuarios finales percibió un ahorro de tiempo sustancial y una alta satisfacción en la generación de reportes tras la digitalización. Asimismo, Brooks et al. (2024) concluyeron que los sistemas que simplifican el reporte de stock y reducen la duplicidad documental incrementan de manera sostenida la satisfacción del personal sanitario, validando la inclusión de los constructos de Davis (1989) en la evaluación de la gestión de movimientos de vacunas.

---

## 2.3 Marco conceptual

**Aceptación del proceso.** Grado de conformidad subjetiva, agilidad operativa y reducción de la sobrecarga administrativa manifestado por el personal de salud respecto al flujo de trabajo para registrar y distribuir biológicos, evaluado como constructo de satisfacción bajo el modelo de adopción tecnológica (Davis, 1989).

**Cadena de frío.** Sistema logístico articulado por infraestructura técnica, equipos de refrigeración, procedimientos estandarizados y protocolos normativos que aseguran la conservación ininterrumpida de las vacunas en el rango térmico mandatorio de +2 °C a +8 °C, desde su manufactura hasta su administración a la población (MINSA, 2022).

**Centro de acopio de vacunas.** Instalación sanitaria intermedia equipada con dispositivos frigoríficos y personal calificado, responsable de recibir, custodiar bajo control térmico estricto y distribuir lotes de biológicos hacia los establecimientos de salud del ámbito jurisdiccional de la Dirección de Salud Apurímac II.

**Concordancia programada vs entregada.** Indicador de consistencia documental que evalúa la proporción porcentual de transferencias institucionales en las que el volumen físico de biológicos entregado por el centro de distribución coincide con la cantidad planificada y solicitada formalmente por las microredes de salud ejecutoras.

**Consistencia documental.** Dimensión de la gestión logística referida al nivel de correspondencia aritmética, veracidad y completitud entre las transacciones asentadas en el registro digital de inventario y los movimientos físicos ejecutados, operacionalizada mediante los registros sin discrepancias y la concordancia de cantidades entregadas.

**Extreme Programming (XP).** Metodología ágil de ingeniería de software estructurada en ciclos iterativos cortos, retroalimentación continua, programación en parejas, diseño modular simple y pruebas automatizadas, orientada a desarrollar aplicaciones robustas y adaptables ante requisitos cambiantes en entornos institucionales (Beck, 1999; Pressman, 2010).

**Gestión de movimientos de vacunas.** Conjunto integral de actividades administrativas, técnicas y operativas dirigidas a programar, registrar, controlar, conciliar y auditar las entradas, salidas, transferencias y saldos de inmunobiológicos a lo largo de los eslabones de la red sanitaria institucional (MINSA, 2022).

**Inventario de vacunas.** Registro cuantitativo y cualitativo periódico de las existencias de inmunobiológicos custodiados en los centros de almacenamiento, clasificado por tipo de producto, número de lote, fecha de caducidad y ubicación frigorífica, esencial para evitar pérdidas y desabastecimientos (Wasswa et al., 2023).

**Kardex de biológicos.** Instrumento de control logístico implementado en soporte digital que asienta de forma cronológica, ordenada y verificable los ingresos, egresos y saldos disponibles de cada tipo y lote de vacuna, garantizando trazabilidad en tiempo real y conciliación contable de inventarios.

**Lote de vacunas.** Conjunto homogéneo de dosis de un biológico elaborado bajo condiciones idénticas de manufactura en un único ciclo de producción, plenamente identificado por un código alfanumérico normativo y una fecha de expiración que condiciona su orden de distribución (MINSA, 2022).

**Movimiento de vacunas.** Variación física y contable verificable en la dotación de inmunobiológicos de un establecimiento sanitario, producida por recepción, despacho, transferencia interinstitucional o ajuste justificado, la cual requiere consignar obligatoriamente fecha, responsable, cantidad, lote y documento oficial de sustento.

**Oportunidad de procesamiento.** Dimensión de la gestión logística referida a la rapidez y puntualidad con que se completan las operaciones sobre biológicos, evaluada objetivamente mediante el tiempo cronometrado de registro de movimientos en el kardex y el tiempo de emisión de comprobantes de salida.

**Registros sin discrepancias.** Indicador de consistencia documental que mide la proporción porcentual de movimientos auditados que satisfacen concurrentemente la totalidad de criterios normativos de integridad: concordancia de lote, fecha de vencimiento, tipo de biológico, cantidades coincidentes y acreditación reglamentaria de firmas responsables.

**Sistema de información de inmunización.** Estructura informática integral orientada a capturar, procesar, consolidar y reportar datos fidedignos en tiempo real sobre la cadena de frío, trazabilidad de lotes, cobertura vacunal y balances logísticos de existencias en las dependencias de salud pública (Brooks et al., 2024).

**Sistema web SIVAC.** Plataforma informática transaccional basada en arquitectura cliente-servidor desarrollada bajo Extreme Programming y evaluada mediante la norma ISO/IEC (2023), diseñada para centralizar, controlar y auditar la gestión de movimientos de biológicos en la Dirección de Salud Apurímac II.

**Utilidad percibida.** Constructo del modelo de aceptación tecnológica que expresa la convicción subjetiva de los trabajadores sanitarios respecto a que la implementación del sistema web optimiza su rendimiento, agiliza la trazabilidad documental y favorece la toma de decisiones institucionales (Davis, 1989).

---

## Referencias bibliográficas citadas

Astuhuaman Perez, S. M., & Baltazar Maza, E. J. (2024). *Implementación de un sistema web con IA para mejorar la gestión de citas médicas en el Centro de Salud de Nueva Fuerabamba, Apurímac 2024* [Tesis de titulación, Universidad Privada del Norte]. Repositorio Institucional UPN. https://hdl.handle.net/11537/43590

Balón Morejón, R. M. (2023). *Aplicación web de gestión de citas, control de inventario y campañas de vacunación en el centro de salud Dr. José Garcés Rodríguez del cantón Salinas* [Tesis de grado, Universidad Estatal Península de Santa Elena]. Repositorio Institucional UPSE. https://hdl.handle.net/46000/9257

Beck, K. (1999). Embracing change with extreme programming. *Computer*, 32(10), 70–77. https://doi.org/10.1109/2.796139

Brooks, D. J., Kim, C. I., Mboussou, F., & Danovaro-Holliday, M. C. (2024). Developing national information systems to monitor COVID-19 vaccination: A global observational study. *JMIR Public Health and Surveillance*, 10, Article e62657. https://doi.org/10.2196/62657

Champi Velásquez, J. M. (2023). *Implementación de un sistema de monitoreo inalámbrico mediante Internet de las cosas para monitorear la conservación en la cadena de frío de vacunas del servicio de inmunizaciones en el distrito de Puente Piedra* [Tesis de grado, Universidad de Ciencias y Humanidades]. Repositorio Institucional UCH. http://hdl.handle.net/20.500.12872/844

Chekol, A., Ketemaw, A., Endale, A., Aschale, A., Endalew, B., & Asemahagn, M. (2023). Data quality and associated factors of routine health information system among health centers of West Gojjam Zone, northwest Ethiopia, 2021. *Frontiers in Health Services*, 3, Article 1059611. https://doi.org/10.3389/frhs.2023.1059611

Cohn, M. (2004). *User stories applied: For agile software development*. Addison-Wesley Professional.

Dang, T. T. T., Carnahan, E., Nguyen, L., Mvundura, M., Dao, S., Duong, T. H., Nguyen, T., Nguyen, D., Nguyen, T., Werner, L., Ryman, T. K., & Nguyen, N. (2024). Outcomes and costs of the transition from a paper-based immunization system to a digital immunization system in Vietnam: Mixed methods study. *Journal of Medical Internet Research*, 26, Article e45070. https://doi.org/10.2196/45070

Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. *Management Information Systems Quarterly*, 13(3), 319–340. https://doi.org/10.2307/249008

Duong, H., Dao, S., Dang, H., Nguyen, L., Ngo, T., Nguyen, T., Tran, L. A., Nguyen, D., Rivera, M., & Nguyen, N. (2021). The transition to an entirely digital immunization registry in Ha Noi Province and Son La Province, Vietnam: Readiness assessment study. *JMIR Formative Research*, 5(10), Article e28096. https://doi.org/10.2196/28096

Ergetie, F. S., Kassaw, A. T., & Sendekie, A. K. (2023). Vaccine cold chain management practices in primary health centers providing an expanded immunization program in Northwest Ethiopia. *Frontiers in Public Health*, 11, Article 1194807. https://doi.org/10.3389/fpubh.2023.1194807

Garcia Villacorta, M. D. M., & Calderón Huaman, J. L. O. (2023). *Sistema web para el control de inventario en la Farmacia Pro, 2023* [Tesis de titulación, Universidad Privada del Norte]. Repositorio Institucional UPN. https://hdl.handle.net/11537/33833

George, D., & Mallery, P. (2003). *SPSS for Windows step by step: A simple guide and reference* (4th ed.). Allyn & Bacon.

Hernández-Sampieri, R., Fernández-Collado, C., & Baptista-Lucio, P. (2014). *Metodología de la investigación* (6.ª ed.). McGraw-Hill Education.

ISO/IEC. (2023). *Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model* (Norma ISO/IEC 25010:2023). International Organization for Standardization. https://www.iso.org/standard/78176.html

Kigenza, R., Nsengiyumva, E., & Sabagirirwa, V. (2023). The Quality Management Improvement Approach: Successes and lessons learned from a workforce development intervention in Rwanda’s health supply chain. *Global Health: Science and Practice*, 11(4), Article e2200295. https://doi.org/10.9745/GHSP-D-22-00295

Luján Mora, S. (2002). *Programación de aplicaciones web: Historia, principios básicos y clientes web*. Editorial Club Universitario.

Mego Navarro, D. P. (2021). *Implementación de un sistema web para la gestión de vacunas del Covid-19 en una entidad pública 2021* [Trabajo de suficiencia profesional, Universidad Tecnológica del Perú]. Repositorio Institucional UTP. https://hdl.handle.net/20.500.12867/5068

MINSA. (2022). *Norma Técnica de Salud que establece el Esquema Nacional de Vacunación* (NTS N° 196-MINSA/DGIESP-2022, Resolución Ministerial N° 884-2022/MINSA). Dirección General de Intervenciones Estratégicas en Salud Pública, Ministerio de Salud. https://www.gob.pe/institucion/minsa/normas-legales/3576882-884-2022-minsa

Moumane, K., Idri, A., El Aouni, F., Laghnimi, J., Benabdellah, N. C., & Hamal, O. (2024). ISO/IEC 25010-based quality evaluation of three mobile applications for reproductive health services in Morocco. *Clinical and Experimental Obstetrics & Gynecology*, 51(4), Article 88. https://doi.org/10.31083/j.ceog5104088

Ndlovu, K., Mauco, K. L., Keetile, M., Kadimo, K., Senyatso, R. Y., Ntebela, D., Valela, B., & Murambi, C. (2022). Acceptance of the District Health Information System Version 2 platform for malaria case-based surveillance by health care workers in Botswana: Web-based survey. *JMIR Formative Research*, 6(3), Article e32722. https://doi.org/10.2196/32722

OPS y PATH. (2020). *Datos de inmunización: Evidencia para la acción. Una revisión realista de lo que funciona para mejorar el uso de datos para la inmunización*. Organización Panamericana de la Salud. https://iris.paho.org/handle/10665.2/53120

Pressman, R. S. (2010). *Ingeniería del software: Un enfoque práctico* (7.ª ed.). McGraw-Hill Interamericana.

Ruiz Barea, R. (2023). *Protección de APIs REST*. Universitat Oberta de Catalunya.

Shen, J., Bu, F., Ye, Z., Zhang, M., Ma, Q., Yan, J., & Huang, T. (2024). Management of drug supply chain information based on “artificial intelligence + vendor managed inventory” in China: Perspective based on a case study. *Frontiers in Pharmacology*, 15, Article 1373642. https://doi.org/10.3389/fphar.2024.1373642

Sommerville, I. (2016). *Ingeniería de software* (10.ª ed.). Pearson Educación.

Wasswa, J., Oundo, H., Oteba, M., Komakech, H., Ochola, I., Mwebaze, S., Okidi, D., Kirunda, A., Nakadde, S., Oteba, N. O., & Lugada, E. (2023). Leveraging electronic logistics management information systems to enhance and optimize supply chain response during public health emergencies: Lessons from COVID-19 response in Uganda. *Journal of Pharmaceutical Policy and Practice*, 16, Article 58. https://doi.org/10.1186/s40545-023-00517-4
