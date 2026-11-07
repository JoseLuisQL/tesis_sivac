# CAPA DE DATOS — SIVAC-THESIS-LAB

> **Estado del conjunto:** `DATOS DE PRUEBA – REEMPLAZAR (DEC-007)`.
> La estructura, las llaves y el pipeline son definitivos; los valores de
> `recolectados/` son un conjunto de prueba reproducible hasta que el tesista
> deposite las mediciones de campo.
>
> **Regla Canónica 01:** sin `MANIFEST.json` firmado en `datos/raw/` el
> análisis inferencial permanece `BLOQUEADO`. Ningún agente inventa, simula ni
> extrapola datos numéricos empíricos.

---

## 1. Capas y archivo canónico

| Carpeta | Rol | ¿Fuente de verdad? |
| :--- | :--- | :--- |
| `raw/` | Depósito inmutable de lo recibido de campo (CSV originales + `MANIFEST.json` firmado). | Sí, una vez firmado el manifiesto. |
| `recolectados/` | Conjunto consolidado que consume el pipeline estadístico. Es el que se reemplaza con las mediciones definitivas. | Sí para el análisis. |
| `schemas/` | Catálogo de centros de acopio y diccionario de variables (`codebook.json`). | Sí para nombres y escalas. |
| `plantillas/` | Formatos vacíos para la recolección en campo. No contienen datos. | No. |
| `prueba_sintetica/` | Conjunto determinista (semilla `20261026`) que valida el pipeline y produce `control_integridad.json`. | No: es evidencia de reproducibilidad. |
| `processed/` | Destino de las matrices limpias una vez superados los controles de calidad sobre `raw/`. | No (vacía por diseño). |

Cadena de derivación, siempre en un solo sentido:

```
raw/  ──(control de calidad)──►  processed/  ──►  recolectados/  ──►  salidas/
                                        ▲
prueba_sintetica/ ──(generar_datos_sinteticos.py, semilla 20261026)──┘
```

`recolectados/pretest_campo.csv` y `posttest_campo.csv` son idénticos a
`prueba_sintetica/pretest_sintetico.csv` y `posttest_sintetico.csv` mientras el
conjunto permanezca en estado de prueba. Al ingresar datos reales esa igualdad
deja de cumplirse: es la señal de que el pipeline ya corre sobre mediciones.

---

## 2. Inventario de archivos

La forma se declara como `filas × columnas` para los CSV; los demás archivos no
llevan forma. `scripts/estadistica/verificar_conjunto_datos.py` comprueba que
esta tabla cubra exactamente los archivos presentes en `datos/` y que las
formas declaradas coincidan con las reales (bloque L).

| Archivo | Contenido | Forma |
| :--- | :--- | :--- |
| `raw/README.md` | Regla de inmutabilidad y bloqueo del pipeline. |  |
| `raw/validacion_expertos_declaracion_20261021.json` | Declaración del tesista sobre los puntajes de jueces (no es dato numérico de campo). |  |
| `recolectados/README.md` | Declaración metodológica DEC-007 (se copia a evidencias). |  |
| `recolectados/SIVAC_DATOS_CAMPO.md` | Registro integral de campo: fichas de los tres instrumentos, matrices y Tablas 35–43. |  |
| `recolectados/datos_recolectados_pre_post.xlsx` | Libro con hojas `PRETEST` y `POSTTEST` derivadas de los CSV. |  |
| `recolectados/pretest_campo.csv` | Matriz analítica de línea base, 7 indicadores (proceso manual). | 14 × 18 |
| `recolectados/posttest_campo.csv` | Matriz analítica final, 7 indicadores (con SIVAC). | 14 × 18 |
| `processed/README.md` | Destino de las matrices limpias tras el control de calidad (vacía por diseño). |  |
| `schemas/centros_acopio_reales_sivac.json` | Catálogo de centros, redes y microredes de la DISA Apurímac II (19 registros; la muestra usa 13). |  |
| `schemas/codebook.json` | Diccionario de las 17 variables analíticas: tipo, escala, rango y dimensión. |  |
| `plantillas/MANIFEST.plantilla.json` | Manifiesto que acompañará a los CSV de campo al depositarse en `raw/`. |  |
| `plantillas/plantilla_campo_pretest_postest.csv` | Plantilla de digitación en formato largo (una fila por unidad y momento) con el esquema de la matriz analítica. | 0 × 17 |
| `plantillas/plantilla_campo_pretest_postest.xlsx` | Plantilla ancha pretest/postest para digitación por operador (una fila por `TRAB-NN`, columnas `_pre` y `_post`). |  |
| `plantillas/plantilla_juicio_expertos_fany2024.csv` | Plantilla de juicio de expertos (Modelo Fany 2024). | 0 × 4 |
| `plantillas/plantilla_juicio_expertos_fany2024.xlsx` | Misma plantilla en Excel. |  |
| `prueba_sintetica/DATOS_SINTETICOS_SIVAC.md` | Documento técnico del generador: semilla, método y cifras del conjunto de prueba. |  |
| `prueba_sintetica/control_integridad.json` | Semilla, recuentos, huellas de los CSV y estadísticos de control. |  |
| `prueba_sintetica/instrumento01_replicas.csv` | Réplicas cronometradas del Instrumento 01 (14 × 2 × 6). | 168 × 18 |
| `prueba_sintetica/instrumento02_asientos.csv` | Asientos auditados del Instrumento 02 (14 × 2 × 40). | 1120 × 24 |
| `prueba_sintetica/instrumento02_despachos.csv` | Despachos conciliados del Instrumento 02 (14 × 2 × 25). | 700 × 14 |
| `prueba_sintetica/instrumento03_reactivos.csv` | Respuestas Likert del Instrumento 03 (14 × 2 × 8). | 224 × 13 |
| `prueba_sintetica/matriz_analitica_pre_post.csv` | Consolidado por unidad y momento (14 × 2). | 28 × 19 |
| `prueba_sintetica/pretest_sintetico.csv` | Línea base del conjunto de prueba (copia de `recolectados/pretest_campo.csv`). | 14 × 18 |
| `prueba_sintetica/posttest_sintetico.csv` | Línea final del conjunto de prueba (copia de `recolectados/posttest_campo.csv`). | 14 × 18 |

Los dos archivos de control de esta carpeta (`README.md` e `INVENTARIO.json`)
no se inventarían como datos.

---

## 3. Órdenes de la capa

```bash
python scripts/estadistica/inventario_datos.py              # reescribe datos/INVENTARIO.json
python scripts/estadistica/inventario_datos.py --verificar   # falla si quedó desactualizado
python scripts/estadistica/verificar_conjunto_datos.py       # auditoría integral (bloque L incluido)
```

`datos/INVENTARIO.json` registra bytes, SHA-256, filas y columnas de cada
archivo. Cualquier alta, baja o cambio de forma debe reejecutar el inventario y
actualizar la tabla de la sección 2; la auditoría falla si alguno de los dos
quedó atrás.

---

## 4. Qué hacer con datos reales

1. Depositar los CSV originales y el `MANIFEST.json` firmado en `raw/`.
2. Superar los cuatro niveles de control de calidad y promover a `processed/`.
3. Reemplazar `recolectados/pretest_campo.csv` y `posttest_campo.csv`. Si la
digitación se hizo en el libro de captura v22, este paso lo hace
`consolidar_libro_captura.py --escribir` (audita con solo omitir la bandera; no
escribe si alguna de las 28 sesiones está incompleta).
4. Retirar el rótulo `DATOS DE PRUEBA – REEMPLAZAR (DEC-007)` de
   `recolectados/README.md`, `SIVAC_DATOS_CAMPO.md` y `salidas/evidencias/README.md`.
5. Reejecutar la cadena: `analisis_estadistico_sivac.py` →
   `construir_registro_campo.py` → `exportar_libro_campo.py` →
   `sincronizar_evidencias.py` → `verificar_conjunto_datos.py`.
