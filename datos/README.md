# CAPA 2: PIPELINE DE DATOS Y MEDICIÓN (`datos/`)
> **SIVAC-THESIS-LAB — Universidad Nacional José María Arguedas (UNAJMA)**  
> **Diseño:** Preexperimental con pretest y postest en un solo grupo ($O_1 \to X \to O_2$, $N = n = 14$)  
> **Regla Deontológica:** Prohibición absoluta de invención o simulación de datos empíricos.

---

## 1. Estructura del Pipeline de Datos

```text
datos/
├── README.md                  # Protocolo de custodia e ingesta de datos
├── raw/                       # Datos brutos de campo (inmutables una vez depositados)
│   ├── bd_sivac_pretest.csv   # Mediciones iniciales (O1) de tiempos, consistencia y TAM
│   └── bd_sivac_postest.csv  # Mediciones finales (O2) tras intervención de SIVAC
├── processed/                 # Matrices tabuladas, imputadas y normalizadas para análisis
├── plantillas/                # Fichas cronométricas y cuestionarios en blanco para recolección
└── schemas/                   # Diccionarios de variables, codebooks y formatos de captura
```

---

## 2. Variables y Unidades de Medida

| Variable / Dimensión | Indicador | Símbolo | Unidad de Medida | Fuente de Datos |
|---|---|---|---|---|
| **VI: Sistema Web SIVAC** | Extreme Programming (XP) / ISO 25010 | $X$ | Cualitativo / Fases | Auditoría de software `syncova` |
| **D1: Oportunidad de procesamiento** | Tiempo de registro de movimientos | $T_{reg}$ | Minutos | Ficha de observación cronométrica |
| **D1: Oportunidad de procesamiento** | Tiempo de emisión de vale/salida | $T_{vale}$ | Minutos | Ficha de observación cronométrica |
| **D2: Consistencia documental** | % Registros sin discrepancias | $RSD$ | Porcentaje (%) | Registro documental kardex/pecosa |
| **D2: Consistencia documental** | Concordancia programada vs entregada | $CPE$ | Porcentaje (%) | Registro documental kardex/pecosa |
| **D3: Satisfacción del usuario** | Aceptación del proceso (TAM) | $AP$ | Escala Likert (1-5) | Cuestionario psicométrico digital |
| **D3: Satisfacción del usuario** | Utilidad percibida (TAM) | $UP$ | Escala Likert (1-5) | Cuestionario psicométrico digital |

---

## 3. Protocolo de Custodia e Ingesta

1. **Ingreso:** El tesista deposita las hojas de campo o respuestas exportadas directamente en `datos/raw/`.
2. **Inmutabilidad:** Los archivos en `datos/raw/` adquieren inmediatamente condición de solo lectura.
3. **Limpieza y Validación:** `analista-estadistico` ejecuta el control de calidad, verificación de tipos y balance de casos en `datos/processed/`.
