# CAPA 3: AUTOMATIZACIÓN Y HERRAMIENTAS (`scripts/`)
> **SIVAC-THESIS-LAB — Universidad Nacional José María Arguedas (UNAJMA)**  
> **Propósito:** Pipeline reproducible de compilación editorial, inferencia estadística y generación de figuras APA 7.

---

## 1. Estructura de Módulos de Automatización

```text
scripts/
├── README.md                  # Este índice y guía de ejecución
├── compiladores/              # Generadores de secciones y compilador maestro DOCX
│   ├── capitulo1_builder.py   # Introducción y Capítulo I (Problema de Investigación)
│   ├── capitulo2_builder.py   # Capítulo II (Antecedentes y Bases Teóricas)
│   ├── capitulo3_builder.py   # Capítulo III (Marco Teórico y Sección 3.3 XP)
│   ├── capitulo4_builder.py   # Capítulo IV (Metodología de la Investigación)
│   ├── capitulo5_builder.py   # Capítulo V (Resultados Descriptivos e Inferenciales)
│   ├── capitulo6_builder.py   # Capítulo VI (Discusión, Conclusiones y Referencias)
│   └── compilar_informe_final_docx.py # Compilador maestro OpenXML
├── estadistica/               # Scripts de análisis bioestadístico e inferencial
│   ├── analisis_estadistico_sivac.py # Contrastes Shapiro-Wilk, Wilcoxon, t-Student en Python
│   ├── analisis_estadistico_sivac.R  # Contrastes inferenciales y verificación en R
│   └── crear_datos_campo.py          # Script de estructuración y verificación de esquemas
├── figuras/                   # Visualizaciones vectoriales y raster a 300 DPI
│   ├── generar_figuras_apa7.py       # Gráficos de diferencias pretest vs postest
│   └── generar_figuras_oficiales_apa7.py # Figuras oficiales de alta resolución
└── utilidades/                # Utilidades de bajo nivel OpenXML y diagnóstico
    ├── docx_utilidades.py     # Funciones de estilo, tablas APA 7 y márgenes UNAJMA
    ├── secciones_preliminares.py # Portadas, carátulas, dedicatoria, resúmenes e índices
    ├── test_docx_features.py  # Pruebas de renderizado OpenXML
    ├── test_parser.py         # Pruebas de extracción
    └── check_images.py        # Verificación de imágenes embebidas
```

---

## 2. Guía de Ejecución

Para compilar el informe final o ejecutar los contrastes, se recomienda ejecutar desde la raíz del proyecto `sivac/`:

```bash
# Ejecutar compilación completa del Informe Final en Word:
python scripts/compiladores/compilar_informe_final_docx.py

# Ejecutar análisis estadístico inferencial:
python scripts/estadistica/analisis_estadistico_sivac.py

# Generar figuras oficiales a 300 DPI:
python scripts/figuras/generar_figuras_oficiales_apa7.py
```
