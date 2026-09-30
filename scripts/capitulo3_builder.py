#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SIVAC-THESIS-LAB — ENSAMBLADOR DE CAPÍTULO III: MARCO TEÓRICO Y XP (.DOCX)
Universidad Nacional José María Arguedas (UNAJMA)
Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas
================================================================================
"""

import os
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx_utilidades import (
    agregar_titulo_1, agregar_titulo_2, agregar_titulo_3,
    agregar_parrafo, agregar_item_lista, agregar_tabla_datos,
    agregar_figura_apa7
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAFICOS_DIR = os.path.join(BASE_DIR, "salidas", "recursos_graficos")

def construir_capitulo3(doc):
    agregar_titulo_1(doc, "CAPÍTULO III: MARCO TEÓRICO Y DESARROLLO DE LA SOLUCIÓN")

    agregar_parrafo(
        doc,
        "El presente capítulo expone el marco teórico, conceptual, normativo y metodológico que sustenta la "
        "investigación, articulando los fundamentos disciplinarios de la ingeniería de software con los requerimientos "
        "logísticos de la cadena de frío sanitaria. El capítulo se estructura en tres secciones fundamentales: la sección 3.1 "
        "desarrolla las bases teóricas de la arquitectura de software web, la calidad según la norma internacional ISO/IEC 25010:2023, "
        "la metodología ágil Extreme Programming (XP), la gestión de biológicos según la normativa técnica del Ministerio de "
        "Salud del Perú (MINSA) y el Modelo de Aceptación Tecnológica (TAM); la sección 3.2 define con precisión conceptual "
        "los términos básicos de la investigación; y la sección 3.3 documenta exhaustivamente el ciclo de vida de desarrollo de la "
        "solución informática SIVAC bajo las cuatro fases canónicas de XP.",
        sangria=True
    )

    # 3.1. Bases Teóricas
    agregar_titulo_2(doc, "3.1. Bases Teóricas")

    agregar_titulo_3(doc, "3.1.1. Fundamentos de Sistemas Web y Arquitectura de Software N-Capas")
    agregar_parrafo(
        doc,
        "Los sistemas de información basados en la web son aplicaciones informáticas estructuradas sobre el modelo cliente-servidor "
        "que emplean tecnologías de hipertexto, protocolos estandarizados de internet (HTTP/HTTPS) y navegadores cliente para permitir "
        "a múltiples usuarios interactuar de forma concurrente con una base de datos centralizada (Luján Mora, 2002; Pressman, 2010). "
        "En el contexto de la gestión sanitaria, estas plataformas permiten consolidar información operativa generada en sedes "
        "geográficamente distantes, eliminando los silos informativos derivados de registros manuales y hojas de cálculo individuales.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Desde la perspectiva del diseño arquitectural, las aplicaciones modernas en salud se conciben bajo el patrón de **arquitectura "
        "en capas desacopladas (N-Capas)** (De la Torre et al., 2010), en el cual se establecen fronteras lógicas nítidas entre las "
        "distintas responsabilidades del sistema:",
        sangria=True
    )
    agregar_item_lista(doc, "**Capa de Presentación (Frontend):** Responsable de la interfaz de usuario reactiva, la captura ergonómica de datos, la validación preliminar en el cliente y el renderizado dinámico de interfaces mediante frameworks modernos (React).", sangria_izq=0.5)
    agregar_item_lista(doc, "**Capa de Lógica de Negocio y Aplicación (Backend):** Implementada mediante controladores, servicios y middlewares (Node.js/Express) que procesan las reglas del dominio, calculan saldos intermensuales, validan fechas de caducidad y coordinan los flujos de autorización.", sangria_izq=0.5)
    agregar_item_lista(doc, "**Capa de Interfaces de Programación de Aplicaciones (API REST):** Mecanismo de comunicación basado en verbos HTTP (GET, POST, PUT, DELETE) que transfiere objetos JSON de manera ligera, sin estado (*stateless*) y asegurada mediante tokens criptográficos JWT (Ruiz Barea, 2023).", sangria_izq=0.5)
    agregar_item_lista(doc, "**Capa de Acceso a Datos y Persistencia:** Administrada mediante un motor de base de datos relacional (PostgreSQL) y un mapeador objeto-relacional (Prisma ORM) que garantiza el cumplimiento irrestricto de las propiedades ACID (Atomicidad, Consistencia, Aislamiento y Durabilidad) en cada transacción de inventario.", sangria_izq=0.5)

    agregar_parrafo(
        doc,
        "Sommerville (2016) subraya que la arquitectura web centralizada resulta indispensable en organizaciones con sedes distribuidas "
        "—como las redes y microredes del sector salud—, debido a que garantiza una **única fuente de verdad** (*Single Source of Truth*), "
        "eliminando las discrepancias de información derivadas del trasvase manual de datos. En el ámbito sanitario, la Organización Panamericana "
        "de la Salud y PATH (2020) señalan que un Sistema de Información de Inmunizaciones (SII) debe proveer trazabilidad continua del insumo "
        "biológico desde su recepción en el almacén hasta su administración o egreso, asegurando la visibilidad del stock en tiempo real (Brooks et al., 2024).",
        sangria=True
    )

    ruta_arq = os.path.join(GRAFICOS_DIR, "figura_arq_cliente_servidor.png")
    agregar_figura_apa7(
        doc,
        numero=3.1,
        titulo="Arquitectura cliente-servidor web N-capas desacoplada adoptada en SIVAC",
        ruta_imagen=ruta_arq,
        texto_nota="Diagrama conceptual de la arquitectura en capas desacopladas con frontend React, backend Node.js/TypeScript y persistencia relacional PostgreSQL. Adaptado de De la Torre et al. (2010)."
    )

    agregar_titulo_3(doc, "3.1.2. Calidad del Producto de Software según la Norma Internacional ISO/IEC 25010:2023")
    agregar_parrafo(
        doc,
        "Para evaluar con rigor científico y técnico la Variable Independiente (Sistema web SIVAC), se recurrió al estándar internacional "
        "**ISO/IEC 25010:2023** (*Systems and software engineering — Systems and software Quality Requirements and Evaluation [SQuaRE] — "
        "Product quality model*), el cual define un marco integral para categorizar las propiedades internas y externas que determinan la calidad "
        "de una solución de software (ISO/IEC, 2023). La actualización 2023 clasifica la calidad del producto en características medibles, de "
        "las cuales se priorizaron aquellas directamente vinculadas con el desempeño operativo de los usuarios de inmunizaciones (Cortés Rojas, 2024; Moumane et al., 2024):",
        sangria=True
    )
    agregar_item_lista(doc, "**Adecuación Funcional (*Functional Suitability*):** Grado en que el software satisface las necesidades declaradas e implícitas bajo condiciones determinadas. Comprende la **completitud funcional** (cobertura total de historias de usuario de ingresos, salidas, transferencias y emisión de vales) y la **exactitud funcional** (precisión matemática absoluta en el cálculo de saldos y balances de kardex sin discrepancias aritméticas).", sangria_izq=0.5)
    agregar_item_lista(doc, "**Usabilidad (*Usability*):** Grado en que el software puede ser entendido, aprendido, usado y resultar atractivo para los operadores bajo condiciones específicas. Comprende la **facilidad de aprendizaje** (*learnability*) y la **claridad ergonómica de la interfaz** (*operability & clarity*), minimizando el esfuerzo cognitivo en el ingreso masivo de datos.", sangria_izq=0.5)

    headers_31 = ["Característica ISO/IEC 25010", "Subcaracterística", "Criterio de Medición en SIVAC", "Indicador Asociado (VI)"]
    filas_31 = [
        ["Adecuación Funcional", "Completitud funcional", "Cobertura del 100% de requerimientos y módulos de la NTS N° 196-MINSA.", "Ind 1.1: Completitud funcional"],
        ["", "Exactitud funcional", "Tasa de error aritmético de 0.0% en balance de saldos de kardex por lote.", "Ind 1.2: Exactitud de resultados"],
        ["Usabilidad", "Facilidad de aprendizaje", "Tiempo de inducción inferior a 25 minutos para operar el registro completo.", "Ind 2.1: Facilidad de uso"],
        ["", "Claridad y operabilidad", "Organización limpia de interfaces, diseño reactivo y mitigación de errores.", "Ind 2.2: Claridad de interfaz"]
    ]
    agregar_tabla_datos(
        doc,
        numero=3.1,
        titulo="Modelo de calidad del producto de software según ISO/IEC 25010:2023 aplicado a SIVAC",
        encabezados=headers_31,
        filas=filas_31,
        nota="Adaptado de ISO/IEC (2023) y Cortés Rojas (2024)."
    )

    agregar_titulo_3(doc, "3.1.3. Metodología Ágil Extreme Programming (XP)")
    agregar_parrafo(
        doc,
        "El desarrollo del sistema SIVAC fue conducido mediante la metodología ágil **Extreme Programming (XP)**, formulada originariamente "
        "por Kent Beck (1999). XP es una disciplina de ingeniería de software diseñada para optimizar la respuesta ante requerimientos altamente "
        "cambiantes, reducir los riesgos de desfase operativo y maximizar la entrega temprana de valor funcional a través de ciclos iterativos cortos, "
        "diseño simple, refactorización continua y una estrecha retroalimentación con el cliente o usuario final (Beck, 1999; Pressman, 2010; Sommerville, 2016).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "XP se fundamenta en cinco valores esenciales: **comunicación**, **simplicidad**, **retroalimentación**, **valentía** y **respeto**. "
        "En el contexto de la DISA Apurímac II, estos valores se tradujeron en la interacción directa y permanente con el personal de inmunizaciones, "
        "el diseño modular sin complejidades superfluas, la verificación inmediata de cada entrega funcional mediante pruebas de aceptación en los "
        "almacenes de acopio y la revisión colaborativa de código (Arisholm et al., 2007; Cohn, 2004).",
        sangria=True
    )

    ruta_xp = os.path.join(GRAFICOS_DIR, "figura_fases_xp.jpeg")
    agregar_figura_apa7(
        doc,
        numero=3.2,
        titulo="Ciclo de vida y fases iterativas de la metodología Extreme Programming (XP)",
        ruta_imagen=ruta_xp,
        texto_nota="Fases canónicas de XP (Exploración, Planificación, Iteraciones y Pruebas de Aceptación) adaptadas al proyecto SIVAC. Basado en Beck (1999) y Sommerville (2016)."
    )

    headers_32 = ["Práctica Esencial de XP", "Descripción Técnica", "Aplicación Específica en SIVAC"]
    filas_32 = [
        ["Historias de Usuario", "Especificaciones breves en lenguaje del usuario con criterios de aceptación.", "15 historias de usuario (HU-01 a HU-15) articuladas 1:1 con las 3 dimensiones de la VD."],
        ["Entregas Pequeñas", "Despliegues frecuentes de versiones funcionales en intervalos de 1 a 2 semanas.", "Roadmap de 5 iteraciones incrementales con entrega progresiva de módulos."],
        ["Diseño Simple", "Mantener la arquitectura lo más simple posible que satisfaga las pruebas actuales.", "Esquema relacional normalizado en PostgreSQL enfocado en tablas de movimientos y lotes."],
        ["Programación en Parejas", "Co-diseño y revisión cruzada de código entre desarrolladores en tiempo real.", "Desarrollo conjunto de endpoints críticos de la API REST y componentes React."],
        ["Refactorización Continua", "Reestructuración de código para elevar su eficiencia sin alterar su comportamiento.", "Optimización continua de algoritmos de cálculo de saldos y generación de vales PDF."],
        ["Integración Continua", "Compilación y validación automatizada de código con cada confirmación.", "Pipelines de prueba automatizada con Jest, Supertest y Playwright Test."],
        ["Cliente en el Sitio", "Disponibilidad permanente de representantes del usuario para absolver dudas.", "Coordinación directa con la Coordinación de Inmunizaciones de la DISA Apurímac II."]
    ]
    agregar_tabla_datos(
        doc,
        numero=3.2,
        titulo="Prácticas esenciales de Extreme Programming (XP) implementadas en el proyecto SIVAC",
        encabezados=headers_32,
        filas=filas_32,
        nota="Elaboración basada en Beck (1999), Pressman (2010) y Sommerville (2016)."
    )

    agregar_titulo_3(doc, "3.1.4. Gestión Logística de Vacunas y Cadena de Suministro Sanitaria")
    agregar_parrafo(
        doc,
        "La gestión logística de productos biológicos comprende las actividades coordinadas de estimación, recepción, almacenamiento, "
        "custodia de cadena de frío, distribución, control de existencias y reporte de movimientos de vacunas (MINSA, 2022). Las vacunas son "
        "medicamentos termolábiles de estricto resguardo que demandan una conservación térmica ininterrumpida entre **+2 °C y +8 °C** para "
        "evitar su desnaturalización y la pérdida de su potencia inmunogénica (Champi Velásquez, 2023; Ergetie et al., 2023).",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "En la cadena de suministro institucional rige el principio logístico **FEFO (*First Expired, First Out* / Primero en Vencer, Primero en Salir)**, "
        "el cual impone que los lotes cuya fecha de caducidad sea más próxima deben despacharse antes que aquellos con vencimiento más lejano, "
        "previniendo mermas económicas y sanitarias (Ergetie et al., 2023). Asimismo, los instrumentos operativos oficiales de control comprenden:",
        sangria=True
    )
    agregar_item_lista(doc, "**Kardex de Vacunas:** Registro ordenado y cronológico donde se asienta cada movimiento biológico: saldo inicial de apertura, ingresos (remesas con número de pecosa), egresos (distribución con vales oficiales) y saldo final disponible por lote (Romero Onofre, 2016; Garcia & Calderón, 2023).", sangria_izq=0.5)
    agregar_item_lista(doc, "**Vale de Entrega Oficial / Pedido Comprobante de Salida (PECOSA):** Instrumento documental administrativo que formaliza la transferencia de custodia y responsabilidad patrimonial del biológico desde el centro de acopio hacia los establecimientos de salud ejecutores.", sangria_izq=0.5)

    ruta_frio = os.path.join(GRAFICOS_DIR, "figura_cadena_frio.png")
    agregar_figura_apa7(
        doc,
        numero=3.3,
        titulo="Estructura operativa de la red de frío y flujo de movimientos de vacunas en la DISA Apurímac II",
        ruta_imagen=ruta_frio,
        texto_nota="Flujo normado de custodia de cadena de frío desde el nivel central hasta los establecimientos periféricos. Adaptado de MINSA (2022) y OPS/PATH (2020)."
    )

    agregar_titulo_3(doc, "3.1.5. Dimensiones Operativas de la Variable Dependiente y Modelo TAM (DEC-007)")
    agregar_parrafo(
        doc,
        "En cumplimiento de la directriz metodológica **DEC-007**, la Variable Dependiente (*Gestión de movimientos de vacunas*) se evalúa "
        "a través de tres dimensiones operativas:",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**A. Oportunidad de Procesamiento:** Dimensión que califica la celeridad con que los datos de movimientos se capturan, procesan y "
        "emiten para la toma de decisiones sanitarias (Dang et al., 2024). Comprende el **tiempo de registro mensual ($T_{reg}$)** de 10 establecimientos "
        "adscritos (minutos cronometrados) y el **tiempo de emisión del vale oficial ($T_{vale}$)** desde la aprobación del pedido hasta la impresión del comprobante.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**B. Consistencia Documental:** Atributo que refleja la fidelidad, concordancia y ausencia de discrepancias aritméticas entre los registros lógicos, "
        "los respaldos documentales y las existencias físicas en frío (Shen et al., 2024; Chekol et al., 2023). Comprende el **porcentaje de registros sin "
        "discrepancias ($RSD$)** evaluado en una muestra representativa de 20 lotes por centro, y la **concordancia programada vs entregada ($CPE$)** en las remesas.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "**C. Satisfacción del Usuario y Modelo TAM:** Fundamentada en el **Technology Acceptance Model (TAM)** de Fred Davis (1989), uno de los marcos "
        "teóricos más validados para explicar la adopción de tecnologías de información en salud (Ndlovu et al., 2021). Postula que la satisfacción global "
        "está determinada por dos constructos cognitivos centrales: la **Aceptación del Proceso ($AP$)**, vinculada a la facilidad de uso percibida y la "
        "reducción de la carga mental; y la **Utilidad Percibida ($UP$)**, entendida como la convicción de que el sistema optimiza la productividad laboral.",
        sangria=True
    )

    # 3.2. Definición de Términos Básicos
    agregar_titulo_2(doc, "3.2. Definición de Términos Básicos")
    terminos = [
        ("Adecuación Funcional", "Característica de calidad del producto de software (ISO/IEC 25010:2023) que evalúa si el sistema provee las funciones requeridas para satisfacer las necesidades de gestión de vacunas de forma completa y correcta."),
        ("API REST (Representational State Transfer)", "Conjunto estandarizado de protocolos y mecanismos de comunicación web que permite el intercambio asíncrono y seguro de datos en formato JSON entre la interfaz cliente y el servidor central."),
        ("Biológico / Vacuna", "Suspensión de microorganismos vivos, inactivados o sus fracciones que, al ser inoculada en el ser humano, genera una respuesta inmune protectora contra enfermedades infecciosas prevenibles (MINSA, 2022)."),
        ("Cadena de Frío", "Proceso logístico ininterrumpido de almacenamiento, conservación, transporte y distribución de vacunas en condiciones térmicas normadas (+2 °C a +8 °C) desde su fabricación hasta su administración."),
        ("Censal (Población Censal)", "Tipo de investigación en la que se evalúa a la totalidad de los elementos que conforman la población diana sin realizar muestreo probabilístico, aplicable cuando el universo es finito y plenamente accesible ($N \\le 50$)."),
        ("Completitud Funcional", "Grado en que el sistema de software cubre la totalidad de las tareas y procesos operacionales requeridos en el trabajo diario de la estrategia de inmunizaciones."),
        ("Concordancia Documental", "Grado porcentual de correspondencia entre las cantidades de vacunas solicitadas en las programaciones periódicas y los volúmenes físicos efectivamente entregados en los vales oficiales."),
        ("Consistencia Documental", "Cualidad de los registros de inventario caracterizada por la fidelidad, ausencia de discrepancias aritméticas y coincidencia estricta entre el saldo registrado y el stock biológico real."),
        ("Extreme Programming (XP)", "Metodología ágil de ingeniería de software orientada a ciclos iterativos cortos, simplicidad de diseño, retroalimentación continua del usuario y adaptación flexible ante requerimientos dinámicos (Beck, 1999)."),
        ("Fecha de Vencimiento / Caducidad", "Límite temporal establecido por el laboratorio fabricante a partir del cual no se garantiza la potencia inmunogénica, seguridad ni eficacia del biológico."),
        ("Gestión de Movimientos de Vacunas", "Proceso administrativo-logístico de planificar, registrar, fiscalizar, transferir, despachar y reportar los ingresos, egresos y saldos de vacunas en una red de salud."),
        ("Historia de Usuario (HU)", "Descripción concisa en lenguaje natural de una necesidad operativa que un usuario requiere realizar dentro del sistema, acompañada de sus criterios de aceptación formales (Cohn, 2004)."),
        ("Inmunización", "Proceso biológico e institucional mediante el cual se protege a una persona contra una enfermedad infecciosa a través de la administración sistemática de una vacuna."),
        ("Kardex de Vacunas", "Registro ordenado y cronológico que controla las entradas, salidas, saldos por lote y movimientos de cada tipo de biológico en un almacén o centro de acopio."),
        ("Lote de Vacunas", "Cantidad homogénea y trazable de producto biológico elaborado en un mismo ciclo de producción bajo condiciones uniformes, identificado por un código alfanumérico único."),
        ("Modelo TAM (Technology Acceptance Model)", "Modelo teórico de comportamiento que postula que la utilidad percibida y la facilidad de uso percibida son los principales determinantes de la adopción y satisfacción con una tecnología (Davis, 1989)."),
        ("Oportunidad de Procesamiento", "Dimensión temporal que califica la prontitud, celeridad y puntualidad con que se capturan, procesan y emiten los datos de movimientos y reportes logísticos."),
        ("Pretest y Postest", "Mediciones cuantitativas de las variables de estudio realizadas antes ($O_1$) y después ($O_2$) de la introducción de una intervención o tratamiento experimental ($X$)."),
        ("Sistema Web", "Aplicación informática ejecutable en un navegador cliente que procesa datos de manera centralizada en un servidor a través de protocolos de red."),
        ("Usabilidad", "Grado en que una aplicación informática resulta fácil de aprender, intuitiva de operar y visualmente clara para los operadores en su entorno laboral cotidiano (ISO/IEC, 2023).")
    ]
    for idx, (term, desc) in enumerate(terminos, 1):
        agregar_parrafo(doc, f"**{idx}. {term}:** {desc}", sangria=True)

    # 3.3. Metodología de Desarrollo del Software SIVAC (Extreme Programming - XP)
    agregar_titulo_2(doc, "3.3. Desarrollo de la Solución Mediante la Metodología Extreme Programming (XP)")
    agregar_parrafo(
        doc,
        "En estricta observancia del modelo institucional de tesis de la Escuela Profesional de Ingeniería de Sistemas de la UNAJMA, "
        "la presente sección expone el ciclo de desarrollo de ingeniería de software de la solución SIVAC (*Sistema de Información y "
        "Control de Vacunas*), ejecutado rigurosamente bajo las cuatro fases de la metodología ágil Extreme Programming (XP): "
        "Exploración, Planificación, Iteraciones / Desarrollo y Pruebas de Aceptación (Beck, 1999; Sommerville, 2016).",
        sangria=True
    )

    agregar_titulo_3(doc, "3.3.1. Roles, Actores y Metáfora del Sistema SIVAC")
    agregar_parrafo(
        doc,
        "La **metáfora del sistema** adoptada en SIVAC fue: *“La Cadena Digital de Información en Tiempo Real para la Red de Frío Institucional”*. "
        "Así como los equipos de refrigeración física aseguran que la temperatura de las vacunas no se interrumpa fuera del rango de +2 °C a +8 °C, "
        "SIVAC actúa como el refrigerador digital que garantiza que los datos de cada lote, remesa y frasco mantengan una trazabilidad ininterrumpida "
        "desde su llegada desde el nivel central hasta su entrega en el establecimiento periférico más lejano de Andahuaylas y Chincheros.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "A partir de las sesiones de trabajo de campo en la DISA Apurímac II, se formalizaron cuatro roles operativos con control de acceso basado en roles (RBAC):",
        sangria=True
    )
    headers_roles = ["Rol en SIVAC", "Actor en la DISA Apurímac II", "Responsabilidades en la Cadena de Suministro"]
    filas_roles = [
        ["Coordinador(a) Regional", "Estrategia de Inmunizaciones (Sede Andahuaylas)", "Supervisión regional, aprobación de distribuciones, alertas de stock y autorización de transferencias."],
        ["Responsable de Acopio", "Personal de enfermería y técnicos de 11 centros", "Recepción de remesas, control de lotes en frío, balance de movimientos y emisión de vales de salida."],
        ["Operador de Establecimiento", "Personal técnico de centros y puestos periféricos", "Consulta de saldos asignados, confirmación de recepciones físicas y reporte de incidencias."],
        ["Administrador del Sistema", "Especialista de TI / Soporte Informático DISA", "Gestión integral de usuarios, parametrización de catálogos, respaldos de base de datos y auditoría."]
    ]
    agregar_tabla_datos(
        doc,
        numero=3.3,
        titulo="Roles, actores y responsabilidades operativas en el sistema web SIVAC",
        encabezados=headers_roles,
        filas=filas_roles,
        nota="Definición formal de roles de usuario según estructura orgánica de la DISA Apurímac II."
    )

    agregar_titulo_3(doc, "3.3.2. Fase de Exploración: Especificación de Historias de Usuario")
    agregar_parrafo(
        doc,
        "Durante la Fase de Exploración se capturaron las necesidades operativas de la cadena de frío, especificándose un catálogo formal "
        "de quince (15) Historias de Usuario (HU-01 a HU-15). Cada historia definió su rol, objetivo, criterios de aceptación, estimación "
        "en Puntos de Historia (PH), iteración asignada y su vinculación directa 1:1 con las 3 dimensiones de la Variable Dependiente (DEC-007):",
        sangria=True
    )

    headers_hu = ["Código", "Historia de Usuario", "Dimensión Impactada", "Prioridad", "PH", "Iteración"]
    filas_hu = [
        ["HU-01", "Autenticación segura y control de roles RBAC", "D3: Satisfacción / Seguridad", "Alta", "3", "Iteración 1"],
        ["HU-02", "Gestión territorial (Redes, Microredes, Acopios)", "D2: Consistencia documental", "Alta", "5", "Iteración 1"],
        ["HU-03", "Catálogo normado de vacunas e insumos MINSA", "D2: Consistencia documental", "Alta", "5", "Iteración 1"],
        ["HU-04", "Recepción de remesas y control de lotes FEFO", "D2: Consistencia documental", "Alta", "8", "Iteración 2"],
        ["HU-05", "Registro de ingresos con pecosa institucional", "D1: Oportunidad de procesamiento", "Alta", "5", "Iteración 2"],
        ["HU-06", "Registro de salidas y transferencias zonales", "D1: Oportunidad de procesamiento", "Alta", "5", "Iteración 2"],
        ["HU-07", "Kardex digital automatizado por lote y centro", "D2: Consistencia documental", "Alta", "8", "Iteración 3"],
        ["HU-08", "Balance mensual y migración síncrona de saldos", "D2: Consistencia documental", "Alta", "5", "Iteración 3"],
        ["HU-09", "Redistribución y compensación de cuotas anuales", "D2: Consistencia documental", "Media", "5", "Iteración 3"],
        ["HU-10", "Asignación algorítmica de jeringas por dosis", "D2: Consistencia documental", "Media", "3", "Iteración 4"],
        ["HU-11", "Generación y emisión de vales oficiales en PDF", "D1: Oportunidad de procesamiento", "Alta", "5", "Iteración 4"],
        ["HU-12", "Cálculo de factor de pérdida y frascos abiertos", "D2: Consistencia documental", "Media", "4", "Iteración 4"],
        ["HU-13", "Semáforo de alertas de vencimiento e inventario", "D3: Satisfacción / Utilidad", "Alta", "5", "Iteración 5"],
        ["HU-14", "Panel analítico y reportes ejecutivos de stock", "D3: Satisfacción / Utilidad", "Media", "5", "Iteración 5"],
        ["HU-15", "Exportación de datos de movimientos a Excel/CSV", "D1: Oportunidad / Usabilidad", "Media", "5", "Iteración 5"]
    ]
    agregar_tabla_datos(
        doc,
        numero=3.4,
        titulo="Catálogo maestro de Historias de Usuario (HU) del sistema web SIVAC",
        encabezados=headers_hu,
        filas=filas_hu,
        nota="Total acumulado: 71 Puntos de Historia (PH) distribuidos en 5 iteraciones ágiles."
    )

    agregar_titulo_3(doc, "3.3.3. Fase de Planificación: Planning Game y Estimaciones")
    agregar_parrafo(
        doc,
        "En el *Planning Game* se priorizaron las historias de usuario en función de su valor operativo para la red de frío y su riesgo técnico. "
        "El esfuerzo total se estimó en **71 Puntos de Historia (PH)**, planificándose cinco (5) iteraciones de desarrollo de 2 semanas de duración cada una:",
        sangria=True
    )
    headers_iter = ["Iteración", "Objetivo Operativo", "Historias Abordadas", "Esfuerzo (PH)", "Entregable Funcional"]
    filas_iter = [
        ["Iteración 1", "Seguridad, estructura territorial y catálogos", "HU-01, HU-02, HU-03", "13", "Módulo de autenticación JWT y configuración de los 11 centros."],
        ["Iteración 2", "Gestión de lotes FEFO y registro de movimientos", "HU-04, HU-05, HU-06", "18", "Módulo transaccional de ingresos y salidas con control de lotes."],
        ["Iteración 3", "Kardex digital y balance síncrono intermensual", "HU-07, HU-08, HU-09", "18", "Motor de cálculo automático de saldos y compensación de cuotas."],
        ["Iteración 4", "Asignación de insumos y generación de vales PDF", "HU-10, HU-11, HU-12", "12", "Módulo de emisión algorítmica de vales oficiales en formato PECOSA."],
        ["Iteración 5", "Panel analítico, alertas de caducidad y exportación", "HU-13, HU-14, HU-15", "10", "Dashboard ejecutivo, semáforos de stock y exportación tabular."]
    ]
    agregar_tabla_datos(
        doc,
        numero=3.5,
        titulo="Plan de entregas (Release Plan) e iteraciones ágiles de SIVAC",
        encabezados=headers_iter,
        filas=filas_iter,
        nota="Planificación ejecutada bajo el Planning Game de Extreme Programming."
    )

    agregar_titulo_3(doc, "3.3.4. Fase de Iteraciones: Diseño Arquitectural, Base de Datos y Código")
    agregar_parrafo(
        doc,
        "La arquitectura del sistema se implementó siguiendo un esquema N-capas desacoplado, con un frontend en React estructurado con "
        "componentes modulares de interfaz y un backend en Node.js/TypeScript gobernado por el framework Express. La comunicación entre "
        "capas se realiza mediante una API RESTful con 28 endpoints estandarizados que transfieren datos serializados en JSON.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "La base de datos relacional se diseñó e implementó en PostgreSQL administrada a través de Prisma ORM, consolidando 15 entidades "
        "normalizadas en Tercera Forma Normal (3FN): `Usuario`, `Rol`, `RedSalud`, `Microred`, `CentroAcopio`, `Establecimiento`, `Vacuna`, "
        "`Insumo`, `LoteVacuna`, `Movimiento`, `DetalleMovimiento`, `Kardex`, `BalanceMensual`, `ValeSalida` y `DetalleVale`. El motor "
        "asegura integridad referencial mediante claves foráneas y restricciones únicas compuestas (como `uk_kardex_mes_centro_lote`), "
        "impidiendo discrepancias aritméticas o saldos negativos.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Entre los algoritmos críticos codificados destacan: (a) el algoritmo de sincronización intermensual de saldos, que traslada de "
        "forma atómica el stock final de un mes como saldo inicial del periodo siguiente; (b) el algoritmo de redistribución proporcional de cuotas; "
        "y (c) el módulo de asignación automática de jeringas complementarias, el cual empareja cada dosis biológica despachada con su jeringa "
        "respectiva (0.5 ml, 0.1 ml o 1 ml) según el tipo de vacuna, eliminando errores de cálculo en la preparación de las remesas.",
        sangria=True
    )

    agregar_titulo_3(doc, "3.3.5. Fase de Pruebas de Aceptación y Evaluación ISO/IEC 25010")
    agregar_parrafo(
        doc,
        "La calidad de software se garantizó mediante una estrategia piramidal de pruebas continuas: 7 suites de pruebas unitarias y de "
        "integración automatizadas desarrolladas con Jest 29.7 y Supertest 7.1 ejecutadas sobre los controladores y servicios (`backend/src/__tests__/`), "
        "alcanzando un **100% de casos aprobados** (cero fallos en balance de saldos, deducción de lotes y asignación de jeringas); y pruebas "
        "End-to-End con Playwright Test 1.58.2 que validaron la navegación completa del usuario y la emisión de reportes.",
        sangria=True
    )
    agregar_parrafo(
        doc,
        "Finalmente, se ejecutaron las **Pruebas de Aceptación del Usuario** directamente en los 11 centros de acopio provinciales con el personal "
        "de enfermería y técnicos de la DISA Apurímac II. Las 15 historias de usuario fueron evaluadas contra sus criterios de aceptación formales, "
        "obteniéndose una aprobación unánime del **100% (15/15 HU conformes)**. La evaluación bajo el estándar ISO/IEC 25010:2023 arrojó un "
        "nivel de conformidad sobresaliente en Adecuación Funcional (100%), Usabilidad (excelente) y Eficiencia de Desempeño (tiempos de respuesta "
        "de la API inferiores a 350 ms), habilitando el pase oficial del sistema a la fase de experimentación y trabajo de campo.",
        sangria=True
    )
