# CAPA 1: INSUMOS Y REFERENCIAS INMUTABLES (`referencias/`)
> **SIVAC-THESIS-LAB — Universidad Nacional José María Arguedas (UNAJMA)**  
> **Regla Cardinal:** Todo archivo contenido en este directorio es de **ESTRICTA Y EXCLUSIVA LECTURA**. Jamás se modifica ni sobrescribe.

---

## 1. Estructura de la Capa de Referencias

```text
referencias/
├── README.md                  # Este documento normativo y de consulta
├── proyecto_base/             # Insumo primario de la investigación
│   └── PROYECTO_TESIS.docx    # Proyecto de tesis original aprobado
├── modelos_tesis/             # Benchmarks de excelencia institucional UNAJMA
│   ├── Fany_Tesis_Bachiller_2024.pdf (1).pdf # Tesis modelo 2024 (Estructura y estilos)
│   └── Jhon_Tesis_Bachiller_2026 (2).pdf     # Tesis modelo 2026 (Diseño experimental y XP)
└── modelos_validacion/        # Guías y formatos oficiales de juicio de expertos
    ├── PUNTUACION IVC.xlsx    # Matriz oficial de cálculo del IVC (Tristán-López / Lawshe)
    ├── Formato para la validacion de instrumento por ITEM.docx
    ├── CORRECION DE FORMATOS.docx
    ├── EJEMPLO DE PUNTUACION DE VALIDACION.pdf
    ├── Constancias de validacion .pdf
    ├── Validacion Ing Javier Ramos.pdf
    ├── Validación Ing Daniel Minaya.pdf
    └── Validación Ing Ivan Soria .pdf
```

---

## 2. Mapeo de Agentes y Responsabilidades

- **`analista-documental` (Squad E):** Inspecciona y extrae jerarquías de títulos, estilos tipográficos y tablas de los modelos UNAJMA sin alterar ningún archivo original.
- **`especialista-instrumentos` (Squad B):** Replica minuciosamente las fórmulas de `PUNTUACION IVC.xlsx` y la ficha por ítem del Dr. Enrique Cóndor Tinoco para el paquete de validación SIVAC.
- **`guardian-consistencia` (Squad B):** Compara el constructo de `PROYECTO_TESIS.docx` frente a la decisión DEC-007 para evitar la reintroducción de dimensiones espurias.
