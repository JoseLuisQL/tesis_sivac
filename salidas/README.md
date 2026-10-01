# CAPA 4: ENTREGABLES Y SALIDAS OFICIALES (`salidas/`)
> **SIVAC-THESIS-LAB — Universidad Nacional José María Arguedas (UNAJMA)**  
> **Propósito:** Custodia y versionado de los productos académicos oficiales generados por los Squads de investigación.  
> **Regla de Integridad:** Ningún documento depositado en `documentos/` se considera definitivo sin la revisión y aprobación formal del tesista humano.

---

## 1. Estructura de Entregables Oficiales (Estado Inicial Limpio)

```text
salidas/
├── README.md                  # Este protocolo de gestión de salidas
├── documentos/                # Informes finales compilados en Word y PDF (generados en Fase 9 tras aprobación)
├── figuras/                   # Visualizaciones vectoriales y raster a 300 DPI
│   └── recursos_graficos/     # Diagramas de arquitectura, metodológicos y escudo oficial UNAJMA
│       ├── escudo_unajma.png
│       ├── figura_arq_cliente_servidor.png
│       ├── figura_fases_xp.jpeg
│       └── figura_cadena_frio.png
├── instrumentos/              # Expedientes de recolección y validación por juicio de expertos (Fase 5)
├── reportes_jurado/           # Evaluaciones críticas del jurado simulado UNAJMA (Fase 8 / 9)
└── archivo/                   # Respaldo histórico y versiones sustituidas
```

---

## 2. Convención de Versionado y Aprobación

1. **Versionado Incremental:** Los informes se generan como `informe_final_v01.docx`, `informe_final_v02.docx`, etc. No se sobreescriben versiones previas aprobadas.
2. **Revisión del Tesista:** Cuando un subagente o el Director General compila una versión, se somete a la Compuerta Suprema de Calidad (revisión humana).
3. **Imágenes y Tablas:** Todas las figuras deben cumplir con la resolución mínima de 300 DPI y tablas bajo formato APA 7.ª edición (3 líneas horizontales principales, sin cuadrículas verticales).
